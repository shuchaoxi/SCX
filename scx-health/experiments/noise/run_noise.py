#!/usr/bin/env python
"""SCX-Noise: distinguish noisy labels from hard cases on MedMNIST.

Workflow:
  1. Load DermaMNIST (small, challenging dataset)
  2. Inject synthetic label noise (10%, 20%, 40% random flips)
  3. Train model on noisy data
  4. Extract features and compute SCX NoiseScore per sample
  5. Evaluate: can NoiseScore separate noisy from clean samples?
  6. Compare: SCX-Noise vs loss-based filtering vs random
"""

import os
import sys
import argparse
import json
from dataclasses import dataclass, field, asdict
from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import roc_auc_score, average_precision_score

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from scx_health.data_loader import load_medmnist, extract_features
from scx_health.encoder import create_encoder


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class NoiseConfig:
    dataset: str = 'dermamnist'
    data_root: str = './data'
    model: str = 'resnet18'
    in_channels: int = 1
    num_classes: int = 7
    batch_size: int = 64
    epochs: int = 30
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    noise_rates: list = field(default_factory=lambda: [0.0, 0.1, 0.2, 0.4])
    output_dir: str = './results/noise'
    seed: int = 42


# ──────────────────────────────────────────────
# Noise injection
# ──────────────────────────────────────────────

def inject_label_noise(
    labels: torch.Tensor,
    noise_rate: float,
    num_classes: int,
    seed: int,
) -> torch.Tensor:
    """Randomly flip a fraction of labels.

    Returns:
        (noisy_labels, noise_mask) where noise_mask[i] = 1 if label was flipped.
    """
    rng = np.random.RandomState(seed)
    n = len(labels)
    noisy = labels.clone()
    noise_mask = torch.zeros(n, dtype=torch.bool)

    n_flip = int(n * noise_rate)
    flip_indices = rng.choice(n, n_flip, replace=False)

    for idx in flip_indices:
        original = int(labels[idx])
        # Flip to a different random class
        choices = [c for c in range(num_classes) if c != original]
        noisy[idx] = rng.choice(choices)
        noise_mask[idx] = True

    return noisy, noise_mask


# ──────────────────────────────────────────────
# Training
# ──────────────────────────────────────────────

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * inputs.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct, total = 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        preds = outputs.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)
    return correct / total


# ──────────────────────────────────────────────
# SCX-Noise core (placeholder)
# ──────────────────────────────────────────────

def compute_noise_scores(
    features: np.ndarray,
    labels: np.ndarray,
    per_class: bool = True,
) -> np.ndarray:
    """Placeholder for SCX NoiseScore computation.

    TODO: Replace with actual SCX NoiseScore (prototype consistency).

    Returns:
        Array of noise scores (higher = more likely to be noisy).
    """
    # Mock: use distance from class centroid (farther = more likely noisy)
    scores = np.zeros(len(features))
    classes = np.unique(labels)
    for cls in classes:
        mask = labels == cls
        cls_feats = features[mask]
        if len(cls_feats) < 2:
            scores[mask] = 0.5
            continue
        centroid = cls_feats.mean(axis=0, keepdims=True)
        dists = np.linalg.norm(cls_feats - centroid, axis=1)
        max_dist = dists.max() + 1e-8
        # Normalize to [0, 1]; higher = more likely noisy
        scores[mask] = dists / max_dist
    return scores


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_noise_detection(cfg: NoiseConfig) -> dict:
    """Run the noise detection experiment."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Noise Experiment ===")
    print(f"Dataset: {cfg.dataset}")
    print(f"Model:   {cfg.model}")
    print(f"Device:  {cfg.device}")
    print()

    # 1. Load clean data
    print("[1/5] Loading dataset...")
    loaders = load_medmnist(
        name=cfg.dataset,
        root=cfg.data_root,
        batch_size=cfg.batch_size,
    )
    train_set = loaders['train'].dataset
    test_loader = loaders['test']
    print(f"  Train: {len(train_set)} samples")
    print(f"  Test:  {len(test_loader.dataset)} samples")
    print()

    all_results = {}

    for noise_rate in cfg.noise_rates:
        print(f"\n{'='*60}")
        print(f"  Noise Rate: {noise_rate*100:.0f}%")
        print(f"{'='*60}")

        # 2. Inject noise
        print(f"\n[2/5] Injecting {noise_rate*100:.0f}% label noise...")
        clean_labels = torch.tensor(train_set.labels if hasattr(train_set, 'labels')
                                    else train_set.label)
        noisy_labels, noise_mask = inject_label_noise(
            clean_labels, noise_rate, cfg.num_classes, seed=cfg.seed,
        )

        # Patch dataset with noisy labels
        train_set_noisy = train_set
        if hasattr(train_set_noisy, 'labels'):
            train_set_noisy.labels = noisy_labels.numpy().tolist()

        noisy_loader = torch.utils.data.DataLoader(
            train_set_noisy, batch_size=cfg.batch_size, shuffle=True,
        )
        print(f"  Actually noisy: {noise_mask.sum().item()} / {len(noise_mask)}")

        # 3. Train on noisy data
        print(f"\n[3/5] Training on noisy data...")
        model = create_encoder(
            model_name=cfg.model,
            in_channels=cfg.in_channels,
            num_classes=cfg.num_classes,
            pretrained=False,
        ).to(cfg.device)

        optimizer = optim.Adam(model.parameters(), lr=cfg.lr,
                              weight_decay=cfg.weight_decay)
        criterion = nn.CrossEntropyLoss()

        for epoch in range(cfg.epochs):
            loss = train_epoch(model, noisy_loader, optimizer, criterion, cfg.device)
            if (epoch + 1) % 10 == 0:
                val_acc = evaluate(model, loaders['val'], cfg.device)
                print(f"  Epoch {epoch+1:2d}/{cfg.epochs} | Loss: {loss:.4f} | "
                      f"Val Acc: {val_acc:.4f}")

        test_acc = evaluate(model, test_loader, cfg.device)
        print(f"  Test Accuracy (noisy train): {test_acc:.4f}")

        # 4. Extract features & compute noise scores
        print(f"\n[4/5] Computing SCX noise scores...")
        features, pred_labels = extract_features(model, noisy_loader, cfg.device)
        noise_scores = compute_noise_scores(features, pred_labels)

        # 5. Evaluate detection
        print(f"\n[5/5] Evaluating noise detection...")
        y_true = noise_mask.numpy().astype(int)
        y_score = noise_scores

        # ROC-AUC
        if len(np.unique(y_true)) > 1:
            roc_auc = roc_auc_score(y_true, y_score)
            pr_auc = average_precision_score(y_true, y_score)
            noise_auc = roc_auc
        else:
            roc_auc = float('nan')
            pr_auc = float('nan')
            noise_auc = float('nan')

        print(f"  ROC-AUC: {roc_auc:.4f}")
        print(f"  PR-AUC:  {pr_auc:.4f}")

        all_results[f'noise_rate_{noise_rate:.0%}'] = {
            'noise_rate': noise_rate,
            'test_accuracy': float(test_acc),
            'roc_auc': float(roc_auc),
            'pr_auc': float(pr_auc),
        }

    # Save results
    output_path = os.path.join(cfg.output_dir, 'noise_results.json')
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    return all_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SCX-Noise on MedMNIST')
    parser.add_argument('--dataset', default='dermamnist',
                        choices=['pathmnist', 'dermamnist', 'bloodmnist'])
    parser.add_argument('--data-root', default='./data')
    parser.add_argument('--model', default='resnet18',
                        choices=['simple_cnn', 'resnet18'])
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--output-dir', default='./results/noise')
    args = parser.parse_args()

    cfg = NoiseConfig(
        dataset=args.dataset,
        data_root=args.data_root,
        model=args.model,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=args.lr,
        output_dir=args.output_dir,
    )
    run_noise_detection(cfg)
