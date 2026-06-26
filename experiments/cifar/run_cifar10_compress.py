"""
SCX-Compress on CIFAR-10: Reduce training set while maintaining accuracy.

Pipeline:
1. Train baseline ResNet-18 (or SimpleCNN) on full CIFAR-10
2. Extract features (penultimate layer)
3. SCX StateDiscovery (KMeans, K=10) -> state labels
4. SCX RedundancyScore -> per-sample redundancy
5. Compress training set (20%, 30%, 40%, 50%)
6. Retrain on compressed set
7. Compare: SCX vs Random vs Coreset (K-Center) vs Full

Expected: SCX-Compress at 50% compression < 3% accuracy drop
"""

import os
import sys
import time
import warnings
from typing import Optional

import numpy as np

# Add SCX to path
SCX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
if SCX_PATH not in sys.path:
    sys.path.insert(0, SCX_PATH)

import torch
from torch.utils.data import Subset, DataLoader
from torchvision import datasets

# SCX imports
from scx.state.discovery import StateDiscovery
from scx.action.compress import CompressStrategy

# Local utilities
from utils import (
    DEVICE, SimpleCNN, get_resnet18, get_cifar10_transforms,
    train_model, evaluate, extract_features,
    make_dataloader, subset_dataset, print_header, save_results,
)
from run_baselines import random_sample, coreset_sample


warnings.filterwarnings("ignore")


def compute_residuals(
    model: torch.nn.Module,
    dataloader: DataLoader,
    device: torch.device = DEVICE,
) -> np.ndarray:
    """Compute per-sample cross-entropy loss (residuals)."""
    model.eval()
    criterion = torch.nn.CrossEntropyLoss(reduction="none")
    all_losses = []
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            losses = criterion(outputs, labels)
            all_losses.append(losses.cpu().numpy())
    return np.concatenate(all_losses)


def scx_compress(
    X: np.ndarray,
    y: np.ndarray,
    residuals: np.ndarray,
    state_labels: np.ndarray,
    n_states: int,
    compression_ratio: float,
    centroids: Optional[np.ndarray] = None,
    random_state: int = 42,
) -> np.ndarray:
    """SCX-guided compression: remove redundant samples per state.

    Uses CompressStrategy.redundancy_score to identify and remove
    the most redundant samples at the specified compression ratio.
    """
    rng = np.random.RandomState(random_state)
    compressor = CompressStrategy(method="weighted_random")
    keep_indices = []

    for s in range(n_states):
        state_mask = state_labels == s
        state_idx = np.where(state_mask)[0]

        if len(state_idx) == 0:
            continue

        X_s = X[state_idx]
        residual_s = residuals[state_idx]

        # State proportion
        state_proportion = len(state_idx) / len(X)

        # Number to keep
        n_keep = max(1, int(len(state_idx) * (1.0 - compression_ratio)))

        if n_keep >= len(state_idx):
            keep_indices.append(state_idx)
            continue

        # Compute per-sample redundancy scores via CompressStrategy
        scores = compressor.redundancy_score(X_s, residual_s, state_proportion)

        # Keep the least redundant samples (lower score = less redundant)
        sorted_idx = np.argsort(scores)  # lowest redundancy first
        keep_local = sorted_idx[:n_keep]
        keep_indices.append(state_idx[keep_local])

    keep_indices = np.concatenate(keep_indices)
    return np.sort(keep_indices)


def run_cifar10_compress(
    compression_ratios: list[float] = None,
    n_states: int = 10,
    epochs: int = 10,
    use_simple_cnn: bool = True,
):
    """Run the full SCX-Compress experiment on CIFAR-10."""
    if compression_ratios is None:
        compression_ratios = [0.2, 0.3, 0.4, 0.5]

    print_header("SCX-Compress on CIFAR-10")

    # ------------------------------------------------------------------
    # 1. Data loading
    # ------------------------------------------------------------------
    print("\n[1/7] Loading CIFAR-10...")
    train_transform, test_transform = get_cifar10_transforms()
    train_dataset = datasets.CIFAR10("./data", train=True, download=True, transform=train_transform)
    test_dataset = datasets.CIFAR10("./data", train=False, download=True, transform=test_transform)
    test_loader = make_dataloader(test_dataset, batch_size=256, shuffle=False)

    num_classes = 10
    model_fn = lambda: SimpleCNN(num_classes=num_classes) if use_simple_cnn else get_resnet18(num_classes=num_classes)

    # ------------------------------------------------------------------
    # 2. Train baseline model on full dataset
    # ------------------------------------------------------------------
    print("\n[2/7] Training baseline model on full CIFAR-10...")
    full_model = model_fn()
    train_loader_full = make_dataloader(train_dataset, batch_size=128)
    full_history = train_model(full_model, train_loader_full, test_loader,
                               epochs=epochs, verbose=True)
    full_acc = full_history.get("test_acc", [0])[-1]
    print(f"  Full dataset accuracy: {full_acc:.2f}%")

    # ------------------------------------------------------------------
    # 3. Extract features and compute residuals
    # ------------------------------------------------------------------
    print("\n[3/7] Extracting features (penultimate layer)...")
    train_loader_eval = make_dataloader(train_dataset, batch_size=256, shuffle=False)
    features, labels, _ = extract_features(full_model, train_loader_eval, DEVICE)
    print(f"  Features shape: {features.shape}")

    print("  Computing residuals (per-sample loss)...")
    residuals = compute_residuals(full_model, train_loader_eval, DEVICE)
    print(f"  Residuals shape: {residuals.shape}, mean={residuals.mean():.4f}")

    # ------------------------------------------------------------------
    # 4. SCX State Discovery
    # ------------------------------------------------------------------
    print(f"\n[4/7] SCX State Discovery (KMeans, K={n_states})...")
    discoverer = StateDiscovery(method="kmeans", n_states=n_states, random_state=42)
    state_labels = discoverer.fit_predict(features)

    # Count samples per state
    unique, counts = np.unique(state_labels, return_counts=True)
    for s, c in zip(unique, counts):
        print(f"  State {s}: {c} samples ({c/len(features)*100:.1f}%)")

    centroids = discoverer.get_centroids()
    print(f"  Centroids shape: {centroids.shape}")

    # ------------------------------------------------------------------
    # 5. SCX Redundancy Score & Compression at each ratio
    # ------------------------------------------------------------------
    print(f"\n[5/7] SCX-guided compression at ratios: {compression_ratios}")
    results = {
        "full_accuracy": round(full_acc, 2),
        "n_states": n_states,
        "n_samples_full": len(train_dataset),
        "compression_ratios": compression_ratios,
        "scx": [],
        "random": [],
        "coreset": [],
    }

    for ratio in compression_ratios:
        print(f"\n  --- Compression ratio: {ratio:.0%} ---")

        # ---- SCX Compress ----
        t0 = time.time()
        scx_idx = scx_compress(
            features, labels, residuals, state_labels, n_states,
            compression_ratio=ratio, centroids=centroids,
        )
        scx_subset = Subset(train_dataset, scx_idx.tolist())
        scx_loader = make_dataloader(scx_subset, batch_size=128)

        scx_model = model_fn()
        scx_history = train_model(scx_model, scx_loader, test_loader,
                                  epochs=epochs, verbose=False)
        scx_acc = scx_history.get("test_acc", [0])[-1]
        dt_scx = time.time() - t0

        print(f"    SCX:     acc={scx_acc:.2f}% ({len(scx_subset)} samples, {dt_scx:.1f}s)")

        # ---- Random Compress ----
        t0 = time.time()
        rand_idx = random_sample(features, labels, ratio=ratio)
        rand_subset = Subset(train_dataset, rand_idx.tolist())
        rand_loader = make_dataloader(rand_subset, batch_size=128)

        rand_model = model_fn()
        rand_history = train_model(rand_model, rand_loader, test_loader,
                                    epochs=epochs, verbose=False)
        rand_acc = rand_history.get("test_acc", [0])[-1]
        dt_rand = time.time() - t0
        print(f"    Random:  acc={rand_acc:.2f}% ({len(rand_subset)} samples, {dt_rand:.1f}s)")

        # ---- Coreset Compress ----
        t0 = time.time()
        coreset_idx = coreset_sample(features, labels, ratio=ratio)
        coreset_subset = Subset(train_dataset, coreset_idx.tolist())
        coreset_loader = make_dataloader(coreset_subset, batch_size=128)

        coreset_model = model_fn()
        coreset_history = train_model(coreset_model, coreset_loader, test_loader,
                                       epochs=epochs, verbose=False)
        coreset_acc = coreset_history.get("test_acc", [0])[-1]
        dt_coreset = time.time() - t0
        print(f"    Coreset: acc={coreset_acc:.2f}% ({len(coreset_subset)} samples, {dt_coreset:.1f}s)")

        results["scx"].append(round(scx_acc, 2))
        results["random"].append(round(rand_acc, 2))
        results["coreset"].append(round(coreset_acc, 2))

    # ------------------------------------------------------------------
    # 6. Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  SUMMARY: Accuracy at different compression ratios")
    print("=" * 70)
    header = f"{'Method':<15s}" + "".join(f"{r:>8.0%}" for r in compression_ratios)
    print(header)
    print("-" * 70)
    print(f"{'SCX':<15s}" + "".join(f"{a:>8.2f}" for a in results["scx"]))
    print(f"{'Random':<15s}" + "".join(f"{a:>8.2f}" for a in results["random"]))
    print(f"{'Coreset':<15s}" + "".join(f"{a:>8.2f}" for a in results["coreset"]))
    print(f"{'Full':<15s}{full_acc:>8.2f}")
    print("-" * 70)

    # Accuracy drops
    print("\n  Accuracy drop from full:")
    print(f"{'Method':<15s}" + "".join(f"{r:>8.0%}" for r in compression_ratios))
    print("-" * 70)
    print(f"{'SCX':<15s}" + "".join(f"{full_acc - a:>8.2f}" for a in results["scx"]))
    print(f"{'Random':<15s}" + "".join(f"{full_acc - a:>8.2f}" for a in results["random"]))
    print(f"{'Coreset':<15s}" + "".join(f"{full_acc - a:>8.2f}" for a in results["coreset"]))

    save_results("cifar10_compress", results)
    print("\n[Done] Results saved to results/cifar10_compress.json")
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SCX-Compress on CIFAR-10")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs")
    parser.add_argument("--n-states", type=int, default=10, help="Number of SCX states")
    parser.add_argument("--simple-cnn", action="store_true", default=True)
    parser.add_argument("--resnet", action="store_true")
    args = parser.parse_args()

    use_cnn = args.simple_cnn and not args.resnet
    run_cifar10_compress(epochs=args.epochs, n_states=args.n_states, use_simple_cnn=use_cnn)
