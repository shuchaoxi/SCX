"""
Shared utilities for SCX CIFAR-10/100 experiments.

Provides:
- SimpleCNN: lightweight CNN for fast CPU/GPU training
- get_resnet18: ResNet-18 with configurable num_classes
- train_model: standard training loop
- evaluate: accuracy / loss evaluation
- extract_features: penultimate-layer feature extraction
- CIFAR100_GROUPS: coarse superclass groupings for CIFAR-100 routing
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Optional, Callable

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset, TensorDataset, Dataset
from torchvision import datasets, transforms


# ---------------------------------------------------------------------------
# Device detection
# ---------------------------------------------------------------------------
def get_device() -> torch.device:
    """Return cuda if available, else cpu."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


DEVICE = get_device()


# ---------------------------------------------------------------------------
# Data transforms
# ---------------------------------------------------------------------------
def get_cifar10_transforms():
    """Standard CIFAR-10 transforms with augmentation."""
    train_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    return train_transform, test_transform


def get_cifar100_transforms():
    """Standard CIFAR-100 transforms with augmentation."""
    train_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761)),
    ])
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761)),
    ])
    return train_transform, test_transform


# ---------------------------------------------------------------------------
# CIFAR-100 coarse superclass groups (5 groups of 20 classes each)
# Based on the official CIFAR-100 coarse labels.
# ---------------------------------------------------------------------------
CIFAR100_GROUPS = {
    "aquatic_mammals": [4, 30, 55, 72, 95],
    "fish": [1, 32, 67, 73, 91],
    "flowers": [7, 51, 53, 85, 97],
    "food_containers": [16, 28, 44, 62, 79],
    "fruit_vegetables": [0, 12, 38, 57, 83],
    "household_electrical": [22, 39, 40, 86, 94],
    "household_furniture": [5, 20, 25, 84, 93],
    "insects": [3, 42, 55, 64, 73],
    "large_carnivores": [6, 7, 19, 23, 33],
    "large_manmade": [13, 26, 43, 49, 52],
    "large_natural": [8, 21, 41, 60, 66],
    "large_omnivores_herbivores": [9, 12, 18, 28, 38],
    "medium_mammals": [2, 11, 34, 46, 98],
    "non_insect_invertebrates": [15, 17, 24, 31, 58],
    "people": [14, 24, 29, 47, 76],

    # Flatten to 5 meta-groups for our experiments
}

# 5 coarse groups for routing experiment (manually consolidated)
CIFAR100_COARSE5 = {
    "nature":       [4, 30, 55, 72, 95, 1, 32, 67, 73, 91,  # aquatic + fish
                     3, 42, 55, 64, 73, 8, 21, 41, 60, 66],  # insects + large_natural
    "plants_food":  [7, 51, 53, 85, 97, 0, 12, 38, 57, 83],  # flowers + fruit_vegetables
    "household":    [16, 28, 44, 62, 79, 22, 39, 40, 86, 94,  # food_containers + electrical
                     5, 20, 25, 84, 93],                       # furniture
    "animals":      [6, 7, 19, 23, 33, 9, 12, 18, 28, 38,     # large_carnivores + omnivores
                     2, 11, 34, 46, 98, 15, 17, 24, 31, 58],   # medium_mammals + invertebrates
    "people_vehicles": [14, 24, 29, 47, 76, 13, 26, 43, 49, 52],  # people + large_manmade
}


# ---------------------------------------------------------------------------
# SimpleCNN — lightweight model for CPU training
# ---------------------------------------------------------------------------
class SimpleCNN(nn.Module):
    """A lightweight CNN for CIFAR-10/100 (3 conv layers + 2 FC)."""

    def __init__(self, num_classes: int = 10, feature_dim: int = 256):
        super().__init__()
        self.feature_dim = feature_dim
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 16x16

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 8x8

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 4x4
        )
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Sequential(
            nn.Linear(256, feature_dim),
            nn.BatchNorm1d(feature_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
        )
        self.classifier = nn.Linear(feature_dim, num_classes)

    def forward(self, x, return_features: bool = False):
        x = self.conv_layers(x)
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        features = self.fc(x)
        logits = self.classifier(features)
        if return_features:
            return logits, features
        return logits


# ---------------------------------------------------------------------------
# ResNet-18 (using torchvision)
# ---------------------------------------------------------------------------
def get_resnet18(num_classes: int = 10, pretrained: bool = False) -> nn.Module:
    """Create a ResNet-18 with CIFAR-10/100-appropriate stem."""
    try:
        from torchvision.models import resnet18, ResNet18_Weights
        if pretrained:
            model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        else:
            model = resnet18(weights=None)
    except ImportError:
        from torchvision.models import resnet18
        model = resnet18(pretrained=pretrained)

    # CIFAR stem: replace 7x7 conv with 3x3, remove MaxPool
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()

    # Adjust FC
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    test_loader: Optional[DataLoader] = None,
    epochs: int = 10,
    lr: float = 0.01,
    weight_decay: float = 5e-4,
    device: torch.device = DEVICE,
    verbose: bool = True,
    scheduler_step: int = 30,
    save_path: Optional[str] = None,
) -> dict:
    """Train a model with SGD + cosine LR schedule.

    Returns dict with training history: {'train_loss': [...], 'train_acc': [...],
    'test_acc': [...], 'best_acc': float}
    """
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    history = {"train_loss": [], "train_acc": [], "test_acc": []}
    best_acc = 0.0

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        t0 = time.time()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        scheduler.step()

        train_loss = running_loss / total
        train_acc = 100.0 * correct / total
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)

        if test_loader is not None:
            test_acc = evaluate(model, test_loader, device)
            history["test_acc"].append(test_acc)
            if test_acc > best_acc:
                best_acc = test_acc
                if save_path:
                    torch.save(model.state_dict(), save_path)
        else:
            history["test_acc"].append(0.0)

        if verbose:
            dt = time.time() - t0
            log = f"Epoch {epoch:2d}/{epochs} | loss={train_loss:.4f} | train_acc={train_acc:.2f}%"
            if test_loader is not None:
                log += f" | test_acc={test_acc:.2f}%"
            log += f" | {dt:.1f}s"
            print(log)

    history["best_acc"] = best_acc
    return history


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
def evaluate(
    model: nn.Module,
    test_loader: DataLoader,
    device: torch.device = DEVICE,
) -> float:
    """Return top-1 accuracy percentage."""
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    return 100.0 * correct / total


def evaluate_with_loss(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device = DEVICE,
) -> tuple[float, np.ndarray]:
    """Return (accuracy_%, per_sample_losses)."""
    model.eval()
    criterion = nn.CrossEntropyLoss(reduction="none")
    correct = 0
    total = 0
    all_losses = []
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            losses = criterion(outputs, labels)
            all_losses.append(losses.cpu().numpy())
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    return 100.0 * correct / total, np.concatenate(all_losses)


# ---------------------------------------------------------------------------
# Feature extraction (penultimate layer)
# ---------------------------------------------------------------------------
def extract_features(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device = DEVICE,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Extract penultimate-layer features.

    Returns:
        features: (N, d) numpy array
        labels:   (N,) numpy array
        logits:   (N, num_classes) numpy array
    """
    model.eval()
    all_features = []
    all_labels = []
    all_logits = []

    # Register hook to grab penultimate-layer output
    penultimate_out = []

    def hook_fn(module, input, output):
        penultimate_out.append(output.detach().cpu())

    handle = None
    # Try to find penultimate layer: for SimpleCNN, it's fc[-1] (ReLU output)
    # For ResNet, it's avgpool output (before FC)
    if isinstance(model, SimpleCNN):
        handle = model.fc[-3].register_forward_hook(hook_fn)  # After the Linear
    else:
        # ResNet: register hook on avgpool
        for name, module in model.named_modules():
            if name == "avgpool":
                handle = module.register_forward_hook(hook_fn)
                break
        if handle is None:
            # Fallback: use second-to-last layer
            for name, module in model.named_modules():
                if name == "layer4":
                    handle = module.register_forward_hook(hook_fn)
                    break

    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            _ = model(images)
            all_labels.append(labels.cpu().numpy())

    if handle is not None:
        handle.remove()

    if len(penultimate_out) > 0:
        features = torch.cat(penultimate_out, dim=0).numpy()
    else:
        # Fallback: run full forward with return_features
        model.eval()
        features_list = []
        with torch.no_grad():
            for images, labels in dataloader:
                images = images.to(device)
                if isinstance(model, SimpleCNN):
                    _, feats = model(images, return_features=True)
                else:
                    _ = model(images)
                    # Get from avgpool
                    feats = model.avgpool(model.layer4(images))
                    feats = feats.view(feats.size(0), -1)
                features_list.append(feats.cpu().numpy())
        features = np.concatenate(features_list, axis=0)

    labels = np.concatenate(all_labels)
    return features, labels, None


# ---------------------------------------------------------------------------
# Noise injection utilities
# ---------------------------------------------------------------------------
def inject_label_noise(
    labels: np.ndarray,
    noise_rate: float,
    num_classes: int,
    random_state: int = 42,
) -> np.ndarray:
    """Inject symmetric label noise.

    For each sample with probability noise_rate, flip to a random other class.
    Returns noisy labels.
    """
    rng = np.random.RandomState(random_state)
    noisy = labels.copy()
    n = len(labels)
    mask = rng.rand(n) < noise_rate
    for i in np.where(mask)[0]:
        candidates = [c for c in range(num_classes) if c != labels[i]]
        noisy[i] = rng.choice(candidates)
    return noisy


def get_noise_mask(original: np.ndarray, noisy: np.ndarray) -> np.ndarray:
    """Return boolean mask where original != noisy (i.e., noise was injected)."""
    return original != noisy


# ---------------------------------------------------------------------------
# Subset dataset helpers
# ---------------------------------------------------------------------------
def subset_dataset(dataset: Dataset, indices: np.ndarray) -> Subset:
    """Create a Subset from given indices."""
    return Subset(dataset, indices.tolist())


def make_dataloader(
    dataset: Dataset,
    batch_size: int = 128,
    shuffle: bool = True,
    num_workers: int = 0,
) -> DataLoader:
    return DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle,
        num_workers=num_workers, pin_memory=torch.cuda.is_available(),
    )


# ---------------------------------------------------------------------------
# Classification accuracy for numpy predictions
# ---------------------------------------------------------------------------
def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean(y_true == y_pred) * 100.0


# ---------------------------------------------------------------------------
# Save / load results
# ---------------------------------------------------------------------------
RESULTS_DIR = Path(__file__).parent / "results"


def save_results(name: str, data: dict):
    """Save experiment results as JSON."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / f"{name}.json"

    # Convert numpy types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, cls=NumpyEncoder)
    print(f"[save] Results saved to {path}")
    return path


def load_results(name: str) -> dict:
    """Load experiment results."""
    path = RESULTS_DIR / f"{name}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------------------
# Print section headers
# ---------------------------------------------------------------------------
def print_header(title: str):
    """Print a section header."""
    width = 70
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)
