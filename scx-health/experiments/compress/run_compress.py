#!/usr/bin/env python
"""SCX-Compress on MedMNIST: reduce training set while maintaining accuracy.

Workflow:
  1. Load PathMNIST
  2. Train baseline ResNet-18
  3. Extract penultimate-layer features
  4. Run SCX StateDiscovery + RedundancyScore
  5. Compress training set (20%, 30%, 40%, 50%)
  6. Retrain on compressed set
  7. Compare: SCX-Compress vs Random vs Coreset vs Full
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

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from scx_health.data_loader import load_medmnist, extract_features
from scx_health.encoder import create_encoder


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class CompressConfig:
    dataset: str = 'pathmnist'
    data_root: str = './data'
    model: str = 'resnet18'
    in_channels: int = 1
    num_classes: int = 9
    batch_size: int = 64
    epochs: int = 30
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    compression_rates: list = field(default_factory=lambda: [0.0, 0.2, 0.3, 0.4, 0.5])
    output_dir: str = './results/compress'
    seed: int = 42


# ──────────────────────────────────────────────
# Training utilities
# ──────────────────────────────────────────────

def train_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    device: str,
) -> float:
    """Train for one epoch, return average loss."""
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
def evaluate(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    device: str,
) -> float:
    """Evaluate accuracy on a DataLoader."""
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
# SCX-Compress core (placeholder)
# ──────────────────────────────────────────────

def compute_redundancy_scores(
    features: np.ndarray,
    labels: np.ndarray,
) -> np.ndarray:
    """Placeholder for SCX RedundancyScore computation.

    TODO: Replace with actual SCX StateDiscovery + RedundancyScore.

    Returns:
        Array of redundancy scores (higher = more redundant).
    """
    # Mock: use inverse of distance to class centroid as redundancy
    scores = np.zeros(len(features))
    for cls in np.unique(labels):
        mask = labels == cls
        cls_feats = features[mask]
        centroid = cls_feats.mean(axis=0, keepdims=True)
        dists = np.linalg.norm(cls_feats - centroid, axis=1)
        # Samples close to centroid are more redundant
        max_dist = dists.max() + 1e-8
        scores[mask] = 1.0 - (dists / max_dist)
    return scores


def compress_dataset(
    scores: np.ndarray,
    labels: np.ndarray,
    rate: float,
    seed: int = 42,
) -> np.ndarray:
    """Return indices to keep after compression.

    Args:
        scores: Redundancy scores per sample.
        labels: Class labels per sample.
        rate: Compression rate (0.0 = keep all, 0.3 = remove 30%).
        seed: Random seed for reproducibility.

    Returns:
        Boolean mask of samples to keep.
    """
    rng = np.random.RandomState(seed)
    keep_mask = np.ones(len(scores), dtype=bool)
    n_remove = int(len(scores) * rate)

    if n_remove == 0:
        return keep_mask

    # Remove highest-redundancy samples
    remove_order = np.argsort(-scores)  # most redundant first
    keep_mask[remove_order[:n_remove]] = False
    return keep_mask


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_compress(cfg: CompressConfig) -> dict:
    """Run the compression experiment."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Compress Experiment ===")
    print(f"Dataset: {cfg.dataset}")
    print(f"Model:   {cfg.model}")
    print(f"Device:  {cfg.device}")
    print()

    # 1. Load data
    print("[1/6] Loading dataset...")
    loaders = load_medmnist(
        name=cfg.dataset,
        root=cfg.data_root,
        batch_size=cfg.batch_size,
    )
    train_set = loaders['train'].dataset
    val_loader = loaders['val']
    test_loader = loaders['test']
    print(f"  Train: {len(train_set)} samples")
    print(f"  Val:   {len(val_loader.dataset)} samples")
    print(f"  Test:  {len(test_loader.dataset)} samples")
    print()

    # 2. Train baseline
    print("[2/6] Training baseline model...")
    baseline = create_encoder(
        model_name=cfg.model,
        in_channels=cfg.in_channels,
        num_classes=cfg.num_classes,
        pretrained=False,
    ).to(cfg.device)

    optimizer = optim.Adam(baseline.parameters(), lr=cfg.lr,
                          weight_decay=cfg.weight_decay)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(cfg.epochs):
        loss = train_epoch(baseline, loaders['train'], optimizer, criterion, cfg.device)
        train_acc = evaluate(baseline, loaders['train'], cfg.device)
        val_acc = evaluate(baseline, val_loader, cfg.device)
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1:2d}/{cfg.epochs} | Loss: {loss:.4f} | "
                  f"Train Acc: {train_acc:.4f} | Val Acc: {val_acc:.4f}")

    baseline_test_acc = evaluate(baseline, test_loader, cfg.device)
    print(f"  Baseline Test Accuracy: {baseline_test_acc:.4f}")
    print()

    # 3. Extract features
    print("[3/6] Extracting penultimate-layer features...")
    features, labels = extract_features(baseline, loaders['train'], cfg.device)
    print(f"  Features shape: {features.shape}")
    print()

    # 4. Compute redundancy scores
    print("[4/6] Computing SCX redundancy scores...")
    scores = compute_redundancy_scores(features, labels)
    print(f"  Score range: [{scores.min():.4f}, {scores.max():.4f}]")
    print()

    # 5. Compress and retrain
    print("[5/6] Compressing and retraining...")
    results = {
        'baseline_accuracy': float(baseline_test_acc),
        'compression_results': [],
    }

    for rate in cfg.compression_rates:
        print(f"\n  --- Compression rate: {rate*100:.0f}% ---")

        # Get subset indices
        keep_mask = compress_dataset(scores, labels, rate, seed=cfg.seed)
        kept_indices = np.where(keep_mask)[0]
        compressed_set = torch.utils.data.Subset(train_set, kept_indices)
        compressed_loader = torch.utils.data.DataLoader(
            compressed_set, batch_size=cfg.batch_size, shuffle=True,
        )

        # Retrain from scratch
        model = create_encoder(
            model_name=cfg.model,
            in_channels=cfg.in_channels,
            num_classes=cfg.num_classes,
            pretrained=False,
        ).to(cfg.device)

        opt = optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)

        for epoch in range(cfg.epochs):
            train_epoch(model, compressed_loader, opt, criterion, cfg.device)

        test_acc = evaluate(model, test_loader, cfg.device)
        print(f"  Compressed Test Accuracy: {test_acc:.4f} "
              f"(delta: {test_acc - baseline_test_acc:+.4f})")

        results['compression_results'].append({
            'rate': rate,
            'n_train_kept': len(kept_indices),
            'test_accuracy': float(test_acc),
            'accuracy_delta': float(test_acc - baseline_test_acc),
        })

    print()

    # 6. Summarize
    print("[6/6] Summary:")
    print(f"  Baseline: {results['baseline_accuracy']:.4f}")
    for r in results['compression_results']:
        rate_pct = int(r['rate'] * 100)
        print(f"  Compress {rate_pct}%: {r['test_accuracy']:.4f} "
              f"(delta={r['accuracy_delta']:+.4f})")

    # Save results
    output_path = os.path.join(cfg.output_dir, 'compress_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    return results


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SCX-Compress on MedMNIST')
    parser.add_argument('--dataset', default='pathmnist',
                        choices=['pathmnist', 'dermamnist', 'bloodmnist'])
    parser.add_argument('--data-root', default='./data')
    parser.add_argument('--model', default='resnet18',
                        choices=['simple_cnn', 'resnet18'])
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--device', default=None)
    parser.add_argument('--output-dir', default='./results/compress')
    args = parser.parse_args()

    cfg = CompressConfig(
        dataset=args.dataset,
        data_root=args.data_root,
        model=args.model,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=args.lr,
        output_dir=args.output_dir,
    )
    if args.device:
        cfg.device = args.device

    run_compress(cfg)
