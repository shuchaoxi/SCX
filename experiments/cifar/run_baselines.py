"""
Baseline sampling methods for CIFAR-10/100.

Provides:
1. Random sampling
2. Uncertainty sampling (entropy of predictions)
3. Diversity sampling (farthest-point in feature space)
4. Coreset selection (K-Center greedy)
5. High-loss sampling

All methods follow the same interface:
    select(X, y=None, n_select=None, ratio=0.5, **kwargs) -> indices
"""

import os
import sys
import time
import math
from typing import Optional

import numpy as np
from sklearn.metrics import pairwise_distances

# Add SCX to path
SCX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
if SCX_PATH not in sys.path:
    sys.path.insert(0, SCX_PATH)

import torch
from torch.utils.data import DataLoader, Subset, TensorDataset

from utils import (
    DEVICE, SimpleCNN, get_resnet18, get_cifar10_transforms,
    train_model, evaluate, evaluate_with_loss, extract_features,
    make_dataloader, subset_dataset, print_header, save_results,
)


# ---------------------------------------------------------------------------
# Sampling strategies
# ---------------------------------------------------------------------------

def random_sample(
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
    n_select: Optional[int] = None,
    ratio: float = 0.5,
    random_state: int = 42,
    **kwargs,
) -> np.ndarray:
    """Random uniform sampling."""
    rng = np.random.RandomState(random_state)
    n = len(X)
    if n_select is None:
        n_select = max(1, int(n * ratio))
    n_select = min(n_select, n)
    indices = rng.choice(n, n_select, replace=False)
    return np.sort(indices)


def uncertainty_sample(
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
    n_select: Optional[int] = None,
    ratio: float = 0.5,
    probabilities: Optional[np.ndarray] = None,
    model: Optional[torch.nn.Module] = None,
    dataloader: Optional[DataLoader] = None,
    device: torch.device = DEVICE,
    **kwargs,
) -> np.ndarray:
    """Uncertainty sampling via predictive entropy.

    Either provide `probabilities` (N, C) or `model` + `dataloader`.
    """
    n = len(X)
    if n_select is None:
        n_select = max(1, int(n * ratio))
    n_select = min(n_select, n)

    if probabilities is None and model is not None and dataloader is not None:
        model.eval()
        all_probs = []
        with torch.no_grad():
            for images, _ in dataloader:
                images = images.to(device)
                logits = model(images)
                probs = torch.softmax(logits, dim=1)
                all_probs.append(probs.cpu().numpy())
        probabilities = np.concatenate(all_probs, axis=0)

    if probabilities is None:
        raise ValueError("Need probabilities or model+dataloader")

    # Entropy: H(p) = -sum p * log(p)
    eps = 1e-12
    entropy = -np.sum(probabilities * np.log(probabilities + eps), axis=1)
    indices = np.argsort(entropy)[::-1][:n_select]
    return np.sort(indices)


def diversity_sample(
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
    n_select: Optional[int] = None,
    ratio: float = 0.5,
    **kwargs,
) -> np.ndarray:
    """Diversity sampling via farthest-point traversal (in feature space)."""
    n = len(X)
    if n_select is None:
        n_select = max(1, int(n * ratio))
    n_select = min(n_select, n)

    # Subsample if too large for pairwise distance matrix
    if n > 10000:
        rng = np.random.RandomState(42)
        subset_idx = rng.choice(n, 10000, replace=False)
        X_sub = X[subset_idx]
        mapping = subset_idx
    else:
        X_sub = X
        mapping = np.arange(n)

    n_sub = len(X_sub)
    actual_select = min(n_select, n_sub)

    # Farthest-point traversal
    rng = np.random.RandomState(42)
    selected = [rng.randint(0, n_sub)]
    dists = pairwise_distances(X_sub[selected], X_sub, metric="euclidean").flatten()

    for _ in range(1, actual_select):
        idx = np.argmax(dists)
        selected.append(idx)
        new_dists = pairwise_distances(X_sub[[idx]], X_sub, metric="euclidean").flatten()
        dists = np.minimum(dists, new_dists)

    indices = np.sort(mapping[selected])
    return indices


def coreset_sample(
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
    n_select: Optional[int] = None,
    ratio: float = 0.5,
    **kwargs,
) -> np.ndarray:
    """K-Center greedy coreset selection.

    Selects points that minimize the maximum distance to the nearest selected point.
    This is the classic coreset algorithm (Sener & Savarese, 2018).
    """
    n = len(X)
    if n_select is None:
        n_select = max(1, int(n * ratio))
    n_select = min(n_select, n)

    # Subsample for large datasets
    if n > 10000:
        rng = np.random.RandomState(42)
        subset_idx = rng.choice(n, 10000, replace=False)
        X_sub = X[subset_idx]
        mapping = subset_idx
    else:
        X_sub = X
        mapping = np.arange(n)

    n_sub = len(X_sub)
    actual_select = min(n_select, n_sub)

    rng = np.random.RandomState(42)
    selected = [rng.randint(0, n_sub)]
    dists = pairwise_distances(X_sub[selected], X_sub, metric="euclidean").flatten()

    for _ in range(1, actual_select):
        idx = np.argmax(dists)
        selected.append(idx)
        new_dists = pairwise_distances(X_sub[[idx]], X_sub, metric="euclidean").flatten()
        dists = np.minimum(dists, new_dists)

    indices = np.sort(mapping[selected])
    return indices


def highloss_sample(
    X: np.ndarray,
    y: np.ndarray,
    n_select: Optional[int] = None,
    ratio: float = 0.5,
    losses: Optional[np.ndarray] = None,
    model: Optional[torch.nn.Module] = None,
    dataloader: Optional[DataLoader] = None,
    device: torch.device = DEVICE,
    **kwargs,
) -> np.ndarray:
    """Select samples with highest loss.

    Either provide `losses` array or `model` + `dataloader`.
    """
    n = len(X)
    if n_select is None:
        n_select = max(1, int(n * ratio))
    n_select = min(n_select, n)

    if losses is None and model is not None and dataloader is not None:
        _, losses = evaluate_with_loss(model, dataloader, device)

    if losses is None:
        raise ValueError("Need losses or model+dataloader")

    indices = np.argsort(losses)[::-1][:n_select]
    return np.sort(indices)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
BASELINE_METHODS = {
    "random": random_sample,
    "uncertainty": uncertainty_sample,
    "diversity": diversity_sample,
    "coreset": coreset_sample,
    "highloss": highloss_sample,
}


# ---------------------------------------------------------------------------
# Evaluation on CIFAR-10
# ---------------------------------------------------------------------------
def evaluate_baselines_on_cifar10(
    ratios: list[float] = [0.2, 0.3, 0.4, 0.5],
    epochs: int = 10,
    use_simple_cnn: bool = True,
):
    """Train models on subsets selected by each baseline method and compare."""
    print_header("Baseline Methods Comparison on CIFAR-10")

    # Data
    train_transform, test_transform = get_cifar10_transforms()
    train_dataset = datasets.CIFAR10("./data", train=True, download=True, transform=train_transform)
    test_dataset = datasets.CIFAR10("./data", train=False, download=True, transform=test_transform)
    test_loader = make_dataloader(test_dataset, batch_size=256, shuffle=False)

    # Model
    num_classes = 10
    if use_simple_cnn:
        model_cls = lambda: SimpleCNN(num_classes=num_classes)
    else:
        model_cls = lambda: get_resnet18(num_classes=num_classes)

    # Step 1: Train full model
    print("\n[Step 1] Training model on full CIFAR-10...")
    full_model = model_cls()
    full_history = train_model(full_model, make_dataloader(train_dataset, batch_size=128),
                               test_loader, epochs=min(epochs, 5), verbose=True)
    full_acc = full_history["test_acc"][-1] if full_history["test_acc"] else 0
    print(f"Full dataset accuracy: {full_acc:.2f}%")

    # Step 2: Extract features and get losses for baselines
    print("\n[Step 2] Extracting features and losses...")
    train_loader = make_dataloader(train_dataset, batch_size=256, shuffle=False)
    features, labels, _ = extract_features(full_model, train_loader, DEVICE)
    _, per_sample_losses = evaluate_with_loss(full_model, train_loader, DEVICE)

    # Get probabilities for uncertainty
    full_model.eval()
    all_probs = []
    with torch.no_grad():
        for images, _ in train_loader:
            logits = full_model(images.to(DEVICE))
            probs = torch.softmax(logits, dim=1)
            all_probs.append(probs.cpu().numpy())
    probabilities = np.concatenate(all_probs, axis=0)

    X_all = features
    y_all = labels

    # Step 3: Evaluate each method at each ratio
    results = {}
    methods_to_test = list(BASELINE_METHODS.keys())

    for method_name in methods_to_test:
        print(f"\n[Method] {method_name}")
        results[method_name] = {"ratios": {}, "accuracies": []}

        for ratio in ratios:
            # Select subset
            if method_name == "uncertainty":
                idx = BASELINE_METHODS[method_name](
                    X_all, y_all, ratio=ratio, probabilities=probabilities,
                    model=full_model, dataloader=train_loader, device=DEVICE,
                )
            elif method_name == "highloss":
                idx = BASELINE_METHODS[method_name](
                    X_all, y_all, ratio=ratio, losses=per_sample_losses,
                )
            else:
                idx = BASELINE_METHODS[method_name](X_all, y_all, ratio=ratio)

            # Create subset
            subset_indices = idx
            subset = Subset(train_dataset, subset_indices.tolist())
            subset_loader = make_dataloader(subset, batch_size=128)

            # Train on subset
            t0 = time.time()
            sub_model = model_cls()
            sub_history = train_model(sub_model, subset_loader, test_loader,
                                      epochs=epochs, verbose=False)
            sub_acc = sub_history["test_acc"][-1] if sub_history["test_acc"] else 0
            dt = time.time() - t0

            keep_ratio = len(subset) / len(train_dataset)
            results[method_name]["ratios"][ratio] = {
                "accuracy": round(sub_acc, 2),
                "n_samples": len(subset),
                "keep_ratio": round(keep_ratio, 3),
            }
            results[method_name]["accuracies"].append(round(sub_acc, 2))

            print(f"  Ratio={ratio:.0%} ({len(subset)} samples): acc={sub_acc:.2f}% [{dt:.1f}s]")

    # Full baseline
    results["full"] = {"accuracy": round(full_acc, 2)}

    # Summary table
    print("\n" + "=" * 70)
    print("  SUMMARY: Accuracy at different compression ratios")
    print("=" * 70)
    header = f"{'Method':<15s}" + "".join(f"{r:>8.0%}" for r in ratios)
    print(header)
    print("-" * 70)
    for method_name in methods_to_test:
        accs = results[method_name]["accuracies"]
        row = f"{method_name:<15s}" + "".join(f"{a:>8.2f}" for a in accs)
        print(row)
    print(f"{'Full':<15s}{full_acc:>8.2f}")
    print("-" * 70)

    save_results("baselines_cifar10", results)
    print("[done] Results saved to results/baselines_cifar10.json")
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs per run")
    parser.add_argument("--simple-cnn", action="store_true", default=True,
                        help="Use SimpleCNN for speed")
    parser.add_argument("--resnet", action="store_true",
                        help="Use ResNet-18 (slower but better)")
    args = parser.parse_args()

    use_cnn = args.simple_cnn and not args.resnet
    evaluate_baselines_on_cifar10(epochs=args.epochs, use_simple_cnn=use_cnn)
