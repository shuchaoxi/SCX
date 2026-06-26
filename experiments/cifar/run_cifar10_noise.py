"""
SCX-Noise on CIFAR-10: Distinguish label noise from hard examples.

Pipeline:
1. Inject symmetric label noise (10%, 20%, 30%) into CIFAR-10 training set
2. Train model on noisy data
3. Extract features, discover states
4. SCX NoiseScore -> detect noisy samples
5. Evaluate: precision/recall/F1 of noise detection
6. Compare: SCX-Noise vs Confidence-based vs Loss-based detection

Expected: SCX-Noise better at distinguishing noise from hard-but-correct samples
"""

import os
import sys
import time
from typing import Optional

import numpy as np
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score

# Add SCX to path
SCX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
if SCX_PATH not in sys.path:
    sys.path.insert(0, SCX_PATH)

import torch
from torch.utils.data import Subset, DataLoader, TensorDataset
from torchvision import datasets

# SCX imports
from scx.state.discovery import StateDiscovery
from scx.valuation.noise_score import NoiseScore
from scx.valuation.learnability import LearnabilityScore

# Local utilities
from utils import (
    DEVICE, SimpleCNN, get_resnet18, get_cifar10_transforms,
    train_model, evaluate, extract_features, inject_label_noise, get_noise_mask,
    make_dataloader, print_header, save_results,
)


def compute_confidence(
    model: torch.nn.Module,
    dataloader: DataLoader,
    device: torch.device = DEVICE,
) -> np.ndarray:
    """Compute per-sample max prediction confidence (softmax probability)."""
    model.eval()
    all_confs = []
    with torch.no_grad():
        for images, _ in dataloader:
            images = images.to(device)
            logits = model(images)
            probs = torch.softmax(logits, dim=1)
            conf, _ = probs.max(dim=1)
            all_confs.append(conf.cpu().numpy())
    return np.concatenate(all_confs)


def compute_loss(
    model: torch.nn.Module,
    dataloader: DataLoader,
    labels: np.ndarray,
    device: torch.device = DEVICE,
) -> np.ndarray:
    """Compute per-sample cross-entropy loss."""
    model.eval()
    criterion = torch.nn.CrossEntropyLoss(reduction="none")
    all_losses = []
    idx = 0
    with torch.no_grad():
        for images, _ in dataloader:
            batch_size = images.size(0)
            images = images.to(device)
            batch_labels = torch.tensor(labels[idx:idx + batch_size], device=device)
            outputs = model(images)
            losses = criterion(outputs, batch_labels)
            all_losses.append(losses.cpu().numpy())
            idx += batch_size
    return np.concatenate(all_losses)


def compute_learnability(
    features: np.ndarray,
    labels: np.ndarray,
    state_labels: np.ndarray,
    n_states: int,
) -> np.ndarray:
    """Compute per-sample learnability score (residual-based, aggregated per state)."""
    # A simple learnability: negative of state-conditional loss residual
    learnability = np.zeros(len(features))
    for s in range(n_states):
        mask = state_labels == s
        if mask.sum() == 0:
            continue
        # Higher loss = lower learnability within the state
        state_losses = np.zeros(len(features))
        # Per-sample: just use negative residual as learnability proxy
    # For simplicity, treat higher-confidence as higher learnability
    return learnability


def detect_noise_confidence(
    model: torch.nn.Module,
    dataloader: DataLoader,
    device: torch.device = DEVICE,
) -> np.ndarray:
    """Detect noisy samples using confidence threshold.

    Returns boolean mask where True = predicted as noisy.
    Uses a threshold based on the confidence distribution (bottom 10% = noisy).
    """
    confidences = compute_confidence(model, dataloader, device)
    threshold = np.percentile(confidences, 10)
    return confidences < threshold


def detect_noise_loss(
    model: torch.nn.Module,
    dataloader: DataLoader,
    labels: np.ndarray,
    device: torch.device = DEVICE,
) -> np.ndarray:
    """Detect noisy samples using loss threshold.

    Samples with loss in top 10% are flagged as noisy.
    Uses IQR-based thresholding.
    """
    losses = compute_loss(model, dataloader, labels, device)
    # Use IQR rule: values above Q3 + 1.5*IQR are outliers
    q75, q25 = np.percentile(losses, [75, 25])
    iqr = q75 - q25
    threshold = q75 + 1.5 * iqr
    return losses > threshold


def detect_noise_scx(
    features: np.ndarray,
    residuals: np.ndarray,
    state_labels: np.ndarray,
    n_states: int,
) -> np.ndarray:
    """SCX NoiseScore-based noise detection.

    Uses residual consistency within each state: samples with anomalously high
    residual compared to their state-mates are flagged.
    """
    noise_detected = np.zeros(len(features), dtype=bool)

    for s in range(n_states):
        mask = state_labels == s
        state_idx = np.where(mask)[0]

        if len(state_idx) < 5:
            continue

        state_residuals = residuals[state_idx]

        # Within-state z-score based detection
        mean_r = state_residuals.mean()
        std_r = state_residuals.std() + 1e-8
        z_scores = (state_residuals - mean_r) / std_r

        # Flag samples with z > 2 (anomalously high residual)
        flagged = z_scores > 2.0
        noise_detected[state_idx[flagged]] = True

    return noise_detected


def evaluate_detection(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict:
    """Compute detection metrics: precision, recall, F1, AUC."""
    # Handle edge case: no predictions or all same class
    if len(np.unique(y_pred)) < 2:
        return {
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "auc": 0.5,
        }

    prec, rec, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )

    try:
        auc = roc_auc_score(y_true, y_pred.astype(float))
    except ValueError:
        auc = 0.5

    return {
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "auc": round(auc, 4),
    }


def run_cifar10_noise(
    noise_rates: list[float] = None,
    n_states: int = 10,
    epochs: int = 10,
    use_simple_cnn: bool = True,
):
    """Run the full SCX-Noise experiment on CIFAR-10."""
    if noise_rates is None:
        noise_rates = [0.1, 0.2, 0.3]

    print_header("SCX-Noise on CIFAR-10: Label Noise Detection")

    # ------------------------------------------------------------------
    # 1. Data loading
    # ------------------------------------------------------------------
    print("\n[1/7] Loading CIFAR-10...")
    train_transform, test_transform = get_cifar10_transforms()
    clean_train_dataset = datasets.CIFAR10("./data", train=True, download=True, transform=train_transform)
    test_dataset = datasets.CIFAR10("./data", train=False, download=True, transform=test_transform)
    test_loader = make_dataloader(test_dataset, batch_size=256, shuffle=False)

    # Get clean labels
    clean_labels = np.array(clean_train_dataset.targets)
    num_classes = 10
    model_fn = lambda: SimpleCNN(num_classes=num_classes) if use_simple_cnn else get_resnet18(num_classes=num_classes)

    # ------------------------------------------------------------------
    # 2-4. Run for each noise rate
    # ------------------------------------------------------------------
    all_results = {}

    for noise_rate in noise_rates:
        print(f"\n{'=' * 60}")
        print(f"  Noise Rate: {noise_rate:.0%}")
        print(f"{'=' * 60}")

        # Inject noise
        noisy_labels = inject_label_noise(clean_labels, noise_rate, num_classes, random_state=42)
        noise_mask = get_noise_mask(clean_labels, noisy_labels)

        # Replace labels in dataset
        noisy_train_dataset = datasets.CIFAR10("./data", train=True, download=True, transform=train_transform)
        noisy_train_dataset.targets = noisy_labels.tolist()

        # Train model on noisy data
        print(f"\n  [Step 2] Training on noisy data (noise rate={noise_rate:.0%})...")
        noisy_model = model_fn()
        train_loader = make_dataloader(noisy_train_dataset, batch_size=128)
        noisy_history = train_model(noisy_model, train_loader, test_loader,
                                    epochs=epochs, verbose=True)
        noisy_acc = noisy_history.get("test_acc", [0])[-1]
        print(f"  Test accuracy: {noisy_acc:.2f}%")

        # Extract features and residuals
        print("  [Step 3] Extracting features...")
        eval_loader = make_dataloader(noisy_train_dataset, batch_size=256, shuffle=False)
        features, labels, _ = extract_features(noisy_model, eval_loader, DEVICE)
        residuals = compute_loss(noisy_model, eval_loader, noisy_labels, DEVICE)

        # State Discovery
        print(f"  [Step 4] SCX State Discovery (K={n_states})...")
        discoverer = StateDiscovery(method="kmeans", n_states=n_states, random_state=42)
        state_labels = discoverer.fit_predict(features)

        # ------------------------------------------------------------------
        # 5. Noise Detection Methods
        # ------------------------------------------------------------------
        print("  [Step 5] Noise detection...")

        # Method A: SCX NoiseScore
        print("    Running SCX-Noise...")
        scx_pred = detect_noise_scx(features, residuals, state_labels, n_states)
        scx_metrics = evaluate_detection(noise_mask, scx_pred)
        print(f"      SCX: F1={scx_metrics['f1']:.3f}, "
              f"Prec={scx_metrics['precision']:.3f}, "
              f"Rec={scx_metrics['recall']:.3f}")

        # Method B: Confidence-based
        print("    Running Confidence-based...")
        conf_pred = detect_noise_confidence(noisy_model, eval_loader, DEVICE)
        conf_metrics = evaluate_detection(noise_mask, conf_pred)
        print(f"      Confidence: F1={conf_metrics['f1']:.3f}, "
              f"Prec={conf_metrics['precision']:.3f}, "
              f"Rec={conf_metrics['recall']:.3f}")

        # Method C: Loss-based
        print("    Running Loss-based...")
        loss_pred = detect_noise_loss(noisy_model, eval_loader, noisy_labels, DEVICE)
        loss_metrics = evaluate_detection(noise_mask, loss_pred)
        print(f"      Loss: F1={loss_metrics['f1']:.3f}, "
              f"Prec={loss_metrics['precision']:.3f}, "
              f"Rec={loss_metrics['recall']:.3f}")

        # Store
        all_results[f"noise_{noise_rate:.0%}"] = {
            "test_accuracy": round(noisy_acc, 2),
            "noise_rate": noise_rate,
            "n_noisy": int(noise_mask.sum()),
            "n_clean": int((~noise_mask).sum()),
            "scx": scx_metrics,
            "confidence": conf_metrics,
            "loss": loss_metrics,
        }

    # ------------------------------------------------------------------
    # 6. Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  SUMMARY: Noise Detection F1 Scores")
    print("=" * 70)
    header = f"{'Method':<15s}" + "".join(f"{r:>10.0%}" for r in noise_rates)
    print(header)
    print("-" * 70)
    for method in ["scx", "confidence", "loss"]:
        row = f"{method:<15s}"
        for nr in noise_rates:
            row += f"{all_results[f'noise_{nr:.0%}'][method]['f1']:>10.3f}"
        print(row)
    print("-" * 70)

    save_results("cifar10_noise", all_results)
    print("[Done] Results saved to results/cifar10_noise.json")
    return all_results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SCX-Noise on CIFAR-10")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--n-states", type=int, default=10)
    parser.add_argument("--simple-cnn", action="store_true", default=True)
    parser.add_argument("--resnet", action="store_true")
    args = parser.parse_args()

    use_cnn = args.simple_cnn and not args.resnet
    run_cifar10_noise(epochs=args.epochs, n_states=args.n_states, use_simple_cnn=use_cnn)
