"""
SCX-Routing on CIFAR-100: State-conditioned expert selection.

Pipeline:
1. Split CIFAR-100 into 5 coarse category groups
2. Train 5 ResNet-18 experts, each specialized on one group
3. Extract features, discover states (K=20)
4. SCX ExpertReliability -> R_m(s) matrix (expert loss per state)
5. SCX ExpertRouter -> route test samples to best expert
6. Compare: SCX-Routing vs Uniform Ensemble vs Best Single Expert

Expected: SCX-Routing accuracy > Uniform Ensemble > Best Single Expert
"""

import os
import sys
import time
import copy
from typing import Optional

import numpy as np

# Add SCX to path
SCX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
if SCX_PATH not in sys.path:
    sys.path.insert(0, SCX_PATH)

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Subset, DataLoader, Dataset
from torchvision import datasets

# SCX imports
from scx.state.discovery import StateDiscovery
from scx.expert.reliability import ExpertReliability
from scx.expert.router import ExpertRouter
from scx.expert.registry import ExpertRegistry, ExpertInfo

# Local utilities
from utils import (
    DEVICE, SimpleCNN, get_resnet18, get_cifar100_transforms,
    CIFAR100_COARSE5,
    train_model, evaluate, extract_features,
    make_dataloader, subset_dataset, print_header, save_results,
)


def build_cifar100_subset(
    full_dataset: Dataset,
    class_list: list[int],
) -> Subset:
    """Create a subset of CIFAR-100 containing only the specified classes.

    Returns a Subset where labels are remapped to 0..len(class_list)-1.
    """
    indices = []
    label_map = {orig: new for new, orig in enumerate(class_list)}
    for i, (_, label) in enumerate(full_dataset):
        if label in class_list:
            indices.append(i)
    return Subset(full_dataset, indices)


class RemappedDataset(Dataset):
    """Wrapper that remaps labels and only keeps samples from specified classes."""

    def __init__(self, base_dataset, class_list: list[int]):
        self.base_dataset = base_dataset
        self.class_list = class_list
        self.label_map = {orig: new for new, orig in enumerate(class_list)}
        self.indices = [i for i, (_, label) in enumerate(base_dataset) if label in class_list]

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
        img, label = self.base_dataset[self.indices[idx]]
        return img, self.label_map[label]


def train_expert(
    group_name: str,
    class_list: list[int],
    full_train_dataset: Dataset,
    test_dataset: Dataset,
    epochs: int = 10,
    use_simple_cnn: bool = False,
) -> tuple[nn.Module, float, int]:
    """Train an expert on a coarse group of CIFAR-100 classes.

    Returns (model, accuracy, num_classes).
    """
    num_classes = len(class_list)
    print(f"\n  Training expert '{group_name}' ({num_classes} classes)...")

    # Create datasets
    train_subset = RemappedDataset(full_train_dataset, class_list)
    # All test samples (expert votes on all 100, but we only care about its classes)
    test_loader = make_dataloader(test_dataset, batch_size=256, shuffle=False)

    train_loader = make_dataloader(train_subset, batch_size=128)

    model_fn = lambda: SimpleCNN(num_classes=num_classes) if use_simple_cnn \
        else get_resnet18(num_classes=num_classes)

    model = model_fn()
    history = train_model(model, train_loader, None, epochs=epochs, verbose=True)

    return model, history["train_acc"][-1], num_classes


def group_accuracy(
    model: nn.Module,
    group_classes: list[int],
    test_dataset: Dataset,
    device: torch.device = DEVICE,
) -> float:
    """Evaluate model accuracy only on the classes in its group.

    The model was trained on remapped labels 0..len(group)-1.
    We filter test samples belonging to these classes and remap labels.
    """
    model.eval()
    correct = 0
    total = 0
    label_map = {orig: new for new, orig in enumerate(group_classes)}

    # Build a filtered test loader
    filtered_indices = [i for i, (_, label) in enumerate(test_dataset) if label in group_classes]
    filtered_dataset = Subset(test_dataset, filtered_indices)
    filtered_loader = make_dataloader(filtered_dataset, batch_size=256, shuffle=False)

    with torch.no_grad():
        for images, labels in filtered_loader:
            images = images.to(device)
            orig_labels = labels.numpy()
            remapped = torch.tensor([label_map[l] for l in orig_labels.tolist()], device=device)

            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(remapped).sum().item()

    return 100.0 * correct / total if total > 0 else 0.0


def full_accuracy_100(
    model: nn.Module,
    test_dataset: Dataset,
    device: torch.device = DEVICE,
) -> float:
    """Standard top-1 accuracy on full CIFAR-100."""
    test_loader = make_dataloader(test_dataset, batch_size=256, shuffle=False)
    return evaluate(model, test_loader, device)


def predict_with_ensemble(
    models: list[nn.Module],
    group_classes: list[list[int]],
    test_dataset: Dataset,
    device: torch.device = DEVICE,
) -> float:
    """Uniform voting ensemble: each expert votes only on its classes.

    For each test sample, each expert produces a prediction. If the expert
    predicted class c (in its own remapped space), that maps to original class
    group_classes[i][c]. The final prediction is the class with the most votes.
    """
    test_loader = make_dataloader(test_dataset, batch_size=256, shuffle=False)

    for m in models:
        m.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            batch_size = images.size(0)

            # Each expert: (batch_size,) predictions in original label space
            all_votes = np.zeros((batch_size, 100), dtype=np.int32)

            for expert_idx, model in enumerate(models):
                outputs = model(images)
                _, preds = outputs.max(1)
                preds = preds.cpu().numpy()
                # Map to original label space
                for b in range(batch_size):
                    orig_label = group_classes[expert_idx][preds[b]]
                    all_votes[b, orig_label] += 1

            # Ensemble prediction = argmax vote
            ensemble_preds = np.argmax(all_votes, axis=1)
            correct += (ensemble_preds == labels.cpu().numpy()).sum()
            total += batch_size

    return 100.0 * correct / total


def run_cifar100_routing(
    n_states: int = 20,
    epochs: int = 10,
    use_simple_cnn: bool = False,
):
    """Run SCX-Routing on CIFAR-100."""
    print_header("SCX-Routing on CIFAR-100")

    # ------------------------------------------------------------------
    # 1. Data loading
    # ------------------------------------------------------------------
    print("\n[1/7] Loading CIFAR-100...")
    train_transform, test_transform = get_cifar100_transforms()
    full_train_dataset = datasets.CIFAR100("./data", train=True, download=True, transform=train_transform)
    test_dataset = datasets.CIFAR100("./data", train=False, download=True, transform=test_transform)

    # Coarse groups
    groups = CIFAR100_COARSE5
    group_names = list(groups.keys())
    group_class_lists = list(groups.values())

    total_classes = sum(len(cls) for cls in group_class_lists)
    print(f"  {len(groups)} groups, {total_classes} classes total")

    # ------------------------------------------------------------------
    # 2. Train 5 experts
    # ------------------------------------------------------------------
    print("\n[2/7] Training {len(groups)} experts (one per coarse group)...")
    experts = []
    expert_accs = []

    for i, (name, class_list) in enumerate(groups.items()):
        model, acc, nc = train_expert(
            name, class_list, full_train_dataset, test_dataset,
            epochs=epochs, use_simple_cnn=use_simple_cnn,
        )
        experts.append(model)
        expert_accs.append(acc)

    # Evaluate each expert on full CIFAR-100
    print("\n  Evaluating experts on full CIFAR-100...")
    full_accs = []
    group_accs = []
    for i, (name, class_list) in enumerate(groups.items()):
        gacc = group_accuracy(experts[i], class_list, test_dataset, DEVICE)
        facc = full_accuracy_100(experts[i], test_dataset, DEVICE)
        group_accs.append(gacc)
        full_accs.append(facc)
        print(f"  Expert '{name}': group_acc={gacc:.2f}%, full_acc={facc:.2f}%")

    best_single_idx = int(np.argmax(full_accs))
    best_single_acc = full_accs[best_single_idx]
    print(f"\n  Best single expert: '{group_names[best_single_idx]}' with full acc={best_single_acc:.2f}%")

    # ------------------------------------------------------------------
    # 3. Extract features from all experts
    # ------------------------------------------------------------------
    print("\n[3/7] Extracting features for state discovery...")
    # Use the best expert's features for state discovery
    best_expert = experts[best_single_idx]
    train_loader_eval = make_dataloader(full_train_dataset, batch_size=256, shuffle=False)
    features, labels, _ = extract_features(best_expert, train_loader_eval, DEVICE)
    print(f"  Features shape: {features.shape}")

    # ------------------------------------------------------------------
    # 4. SCX State Discovery
    # ------------------------------------------------------------------
    print(f"\n[4/7] SCX State Discovery (KMeans, K={n_states})...")
    discoverer = StateDiscovery(method="kmeans", n_states=n_states, random_state=42)
    state_labels = discoverer.fit_predict(features)
    unique, counts = np.unique(state_labels, return_counts=True)
    for s, c in zip(unique, counts):
        print(f"  State {s}: {c} samples ({c/len(features)*100:.1f}%)")

    centroids = discoverer.get_centroids()

    # ------------------------------------------------------------------
    # 5. SCX ExpertReliability -> R_m(s) matrix
    # ------------------------------------------------------------------
    print("\n[5/7] SCX ExpertReliability -> R(s) matrix...")

    # Create ExpertRegistry
    registry = ExpertRegistry()
    for i, name in enumerate(group_names):
        expert_info = ExpertInfo(
            expert_id=i,
            name=name,
            model=experts[i],
            description=f"Expert on {name} ({len(group_class_lists[i])} classes)",
        )
        registry.add_expert(expert_info)

    # Compute per-expert, per-state loss
    n_experts = len(experts)
    R_matrix = np.zeros((n_experts, n_states))
    state_counts = np.zeros(n_states, dtype=int)

    # For each state, compute each expert's loss
    for s in range(n_states):
        state_mask = state_labels == s
        state_idx = np.where(state_mask)[0]

        if len(state_idx) < 10:
            state_counts[s] = len(state_idx)
            R_matrix[:, s] = 1.0  # high loss if insufficient data
            continue

        state_counts[s] = len(state_idx)

        # Get samples in this state
        # We'll create a small subset dataloader for this state
        state_subset = Subset(full_train_dataset, state_idx.tolist())
        state_loader = make_dataloader(state_subset, batch_size=256, shuffle=False)

        for e_idx, expert in enumerate(experts):
            expert.eval()
            class_list = group_class_lists[e_idx]
            label_map = {orig: new for new, orig in enumerate(class_list)}
            correct = 0
            total = 0

            with torch.no_grad():
                for images, labels in state_loader:
                    images = images.to(device)
                    # Filter to samples in this expert's domain
                    batch_orig_labels = labels.numpy()
                    mask = np.isin(batch_orig_labels, class_list)
                    if mask.sum() == 0:
                        continue
                    # Only evaluate on samples whose classes this expert knows
                    filtered_images = images[mask]
                    remapped_labels = torch.tensor(
                        [label_map[l] for l in batch_orig_labels[mask]],
                        device=device,
                    )
                    outputs = expert(filtered_images)
                    _, preds = outputs.max(1)
                    correct += preds.eq(remapped_labels).sum().item()
                    total += mask.sum()

            # Error rate = 1 - accuracy
            if total > 0:
                R_matrix[e_idx, s] = 1.0 - correct / total
            else:
                R_matrix[e_idx, s] = 1.0  # maximum uncertainty

    print("  R_matrix (expert x state):")
    for e in range(n_experts):
        row_str = "  ".join(f"{R_matrix[e, s]:.3f}" for s in range(min(n_states, 10)))
        print(f"    Expert {e}: {row_str}...")

    # Compute SCX matrix (reliability = low loss = good)
    # For ExpertReliability, we need to use its SCX transformation
    reliability_estimator = ExpertReliability(method="supervised")
    scx_matrix = reliability_estimator.compute_scx_from_risk(R_matrix)

    # ------------------------------------------------------------------
    # 6. SCX ExpertRouter -> route test samples
    # ------------------------------------------------------------------
    print("\n[6/7] SCX ExpertRouter -> routing test samples...")

    # Create router
    router = ExpertRouter(registry=registry)
    # For router, we need R_matrix as reliability metric

    # We'll implement SCX routing:
    # For state s, choose expert e with lowest R_matrix[e, s]
    # If routing doesn't improve, fall back to best expert

    # Get test features
    test_loader_eval = make_dataloader(test_dataset, batch_size=256, shuffle=False)
    test_features, test_labels, _ = extract_features(best_expert, test_loader_eval, DEVICE)
    test_state_labels = discoverer.predict(test_features)

    # SCX-Routing: for each test sample, route to best expert for its state
    # Best expert for state s = argmin_e R_matrix[e, s]
    best_expert_per_state = np.argmin(R_matrix, axis=0)  # (n_states,)

    # SCX-Routed predictions
    router_correct = 0
    total = 0
    test_labels_np = np.array(test_dataset.targets)

    with torch.no_grad():
        for images, labels in test_loader_eval:
            images = images.to(device)
            batch_state_labels = discoverer.predict(
                extract_features_batch(best_expert, images, DEVICE)
            )

            for b in range(images.size(0)):
                s = batch_state_labels[b]
                e_idx = best_expert_per_state[s]
                expert = experts[e_idx]
                class_list = group_class_lists[e_idx]
                label_map = {orig: new for new, orig in enumerate(class_list)}

                # Get expert prediction
                img = images[b:b+1]
                output = expert(img)
                _, pred = output.max(1)
                pred_class = pred.item()

                # Map to original label
                if pred_class < len(class_list):
                    orig_pred = class_list[pred_class]
                else:
                    orig_pred = pred_class  # fallback

                if orig_pred == labels[b].item():
                    router_correct += 1
                total += 1

    routing_acc = 100.0 * router_correct / total
    print(f"  SCX-Routed accuracy: {routing_acc:.2f}%")

    # Uniform ensemble
    print("  Computing uniform ensemble accuracy...")
    ensemble_acc = predict_with_ensemble(experts, group_class_lists, test_dataset, DEVICE)
    print(f"  Uniform ensemble accuracy: {ensemble_acc:.2f}%")

    # ------------------------------------------------------------------
    # 7. Compare
    # ------------------------------------------------------------------
    print("\n[7/7] Comparison:")
    print("-" * 60)
    print(f"  {'Method':<30s} {'Accuracy':<10s}")
    print("-" * 60)
    print(f"  {'Best Single Expert':<30s} {best_single_acc:<10.2f}")
    print(f"  {'Uniform Ensemble':<30s} {ensemble_acc:<10.2f}")
    print(f"  {'SCX-Routing':<30s} {routing_acc:<10.2f}")
    print("-" * 60)

    results = {
        "n_states": n_states,
        "groups": group_names,
        "best_single_expert": {
            "name": group_names[best_single_idx],
            "accuracy": round(best_single_acc, 2),
        },
        "uniform_ensemble": round(ensemble_acc, 2),
        "scx_routing": round(routing_acc, 2),
        "expert_accuracies": {
            name: {"group_acc": round(ga, 2), "full_acc": round(fa, 2)}
            for name, ga, fa in zip(group_names, group_accs, full_accs)
        },
        "R_matrix": R_matrix.tolist(),
    }

    save_results("cifar100_routing", results)
    print("\n[Done] Results saved to results/cifar100_routing.json")
    return results


def extract_features_batch(
    model: nn.Module,
    images: torch.Tensor,
    device: torch.device = DEVICE,
) -> np.ndarray:
    """Extract features for a single batch of images."""
    model.eval()
    features_list = []
    with torch.no_grad():
        # Register hook on avgpool
        penultimate = []

        def hook_fn(module, input, output):
            penultimate.append(output.detach().cpu())

        handle = None
        if isinstance(model, SimpleCNN):
            handle = model.fc[-3].register_forward_hook(hook_fn)
        else:
            for name, module in model.named_modules():
                if name == "avgpool":
                    handle = module.register_forward_hook(hook_fn)
                    break

        _ = model(images)

        if handle is not None:
            handle.remove()

        if len(penultimate) > 0:
            features = torch.cat(penultimate, dim=0).numpy()
        else:
            if isinstance(model, SimpleCNN):
                _, feats = model(images, return_features=True)
            else:
                feats = model.avgpool(model.layer4(images))
                feats = feats.view(feats.size(0), -1)
            features = feats.cpu().numpy()

    return features


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SCX-Routing on CIFAR-100")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--n-states", type=int, default=20)
    parser.add_argument("--simple-cnn", action="store_true")
    parser.add_argument("--resnet", action="store_true", default=True,
                        help="Use ResNet-18 (recommended for CIFAR-100)")
    args = parser.parse_args()

    use_cnn = args.simple_cnn and not args.resnet
    run_cifar100_routing(n_states=args.n_states, epochs=args.epochs, use_simple_cnn=use_cnn)
