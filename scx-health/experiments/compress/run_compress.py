#!/usr/bin/env python
"""SCX-Compress on MedMNIST: reduce training set while maintaining accuracy.

Uses real SCX library calls:
  - scx.state.discovery.StateDiscovery for state discovery
  - scx.action.compress.CompressStrategy for per-sample redundancy scoring
  - SCX per-state stratified compression with boundary retention

Workflow:
  1. Load PathMNIST
  2. Train baseline SimpleCNN
  3. Extract penultimate-layer features + per-sample residuals
  4. Run SCX StateDiscovery + CompressStrategy.redundancy_score
  5. Compress training set per-state (20%, 30%, 40%, 50%)
  6. Retrain on compressed set + evaluate
  7. Compare: SCX-Compress vs Random vs Coreset vs Full data
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

# Add src to path (scx_health + scx framework)
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, '..', '..', 'src'))       # scx_health
sys.path.insert(0, os.path.join(_script_dir, '..', '..', '..', 'src')) # scx framework

from scx_health.data_loader import load_medmnist, extract_features
from scx_health.encoder import create_encoder

# ── SCX imports ─────────────────────────────────────
from scx.state.discovery import StateDiscovery
from scx.action.compress import CompressStrategy
from scx.valuation.redundancy import RedundancyScore


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class CompressConfig:
    dataset: str = 'pathmnist'
    data_root: str = './data'
    model: str = 'simple_cnn'
    in_channels: int = 3
    num_classes: int = 9
    batch_size: int = 128
    epochs: int = 30
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    n_states: int = 10
    compression_rates: list = field(default_factory=lambda: [0.0, 0.2, 0.3, 0.4, 0.5])
    output_dir: str = './results/compress'
    seed: int = 42
    augment: bool = False


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
        targets = targets.view(-1)  # MedMNIST labels are (N, 1)
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
        targets = targets.view(-1)  # MedMNIST labels are (N, 1)
        outputs = model(inputs)
        preds = outputs.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)
    return correct / total


# ──────────────────────────────────────────────
# SCX-Compress — real SCX library calls
# ──────────────────────────────────────────────

@torch.no_grad()
def compute_residuals(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    device: str,
) -> np.ndarray:
    """Compute per-sample cross-entropy loss as residual signal.

    Higher residual → higher prediction error → more informative.
    """
    model.eval()
    all_residuals = []
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        targets = targets.view(-1)  # MedMNIST labels are (N, 1)
        outputs = model(inputs)
        per_sample = nn.functional.cross_entropy(outputs, targets, reduction='none')
        all_residuals.append(per_sample.cpu().numpy())
    return np.concatenate(all_residuals, axis=0)


def scx_compute_redundancy(
    features: np.ndarray,
    residuals: np.ndarray,
    n_states: int = 10,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute per-sample redundancy using SCX StateDiscovery + CompressStrategy.

    Returns:
        (scores, state_labels, centroids)
         scores[i]      — redundancy score (higher = more redundant)
         state_labels[i] — discovered state assignment
         centroids      — K state centroids
    """
    # Step 1: State discovery via SCX
    discovery = StateDiscovery(method='kmeans', n_states=n_states, random_state=seed)
    state_labels = discovery.fit_predict(features)
    centroids = discovery.get_centroids()

    # Step 2: Per-state redundancy scoring via SCX CompressStrategy
    compressor = CompressStrategy(method='weighted_random')
    N = len(features)
    scores = np.zeros(N)

    for s in range(n_states):
        mask = state_labels == s
        n_s = mask.sum()
        if n_s == 0:
            continue
        X_s = features[mask]
        res_s = residuals[mask]
        state_proportion = n_s / N
        s_scores = compressor.redundancy_score(X_s, res_s, state_proportion)
        scores[mask] = s_scores

    # Also compute per-state state-level metrics via RedundancyScore
    # for diagnostic output
    state_metrics = {}
    rs = RedundancyScore()
    for s in range(n_states):
        mask = state_labels == s
        n_s = mask.sum()
        if n_s == 0:
            continue
        X_s = features[mask]
        state_proportion = n_s / N
        res_s = residuals[mask]
        mean_residual = float(np.mean(res_s))
        sim = rs.state_similarity(X_s)
        boundary = rs.boundary_score(X_s, centroids, s)
        D = rs.redundancy(state_proportion, mean_residual, sim, boundary)
        state_metrics[s] = {
            'proportion': state_proportion,
            'mean_residual': mean_residual,
            'similarity': sim,
            'boundary': boundary,
            'redundancy': D,
        }

    return scores, state_labels, centroids


def scx_compress_indices(
    scores: np.ndarray,
    state_labels: np.ndarray,
    residuals: np.ndarray,
    rate: float,
    n_states: int = 10,
    seed: int = 42,
) -> np.ndarray:
    """SCX-Compress: per-state stratified compression.

    For each state:
      - Boundary samples (high residual, top 20%) are forcibly retained.
      - From the rest, samples are chosen inversely proportional to redundancy
        (i.e., low-redundancy = high-information-gain samples are preferred).

    Args:
        scores: Per-sample redundancy scores (higher = more redundant).
        state_labels: SCX state assignments.
        residuals: Per-sample residuals.
        rate: Compression rate (0.2 = remove 20% of training data).
        n_states: Number of discovered states.
        seed: Random seed.

    Returns:
        keep_mask: Boolean array, True for samples to keep.
    """
    N = len(scores)
    keep_mask = np.zeros(N, dtype=bool)
    rng = np.random.RandomState(seed)

    for s in range(n_states):
        mask = state_labels == s
        state_indices = np.where(mask)[0]
        n_s = len(state_indices)
        if n_s <= 1:
            keep_mask[state_indices] = True
            continue

        # Target: keep (1 - rate) fraction per state (stratified)
        n_keep_s = max(1, int(n_s * (1.0 - rate)))

        # Boundary samples: top 20% by residual
        res_s = residuals[mask]
        threshold = float(np.percentile(res_s, 80)) if n_s > 1 else 0.0
        is_boundary = res_s >= threshold

        boundary_idx = state_indices[is_boundary]
        non_boundary_idx = state_indices[~is_boundary]

        # Keep all boundary samples first
        keep_mask[boundary_idx] = True
        remaining = n_keep_s - int(np.sum(is_boundary))

        if remaining > 0 and len(non_boundary_idx) > 0:
            # From non-boundary, select inversely proportional to redundancy
            nb_scores = scores[non_boundary_idx]
            info_weights = np.clip(1.0 - nb_scores, 0.0, None)
            if info_weights.sum() > 1e-10:
                prob = info_weights / info_weights.sum()
            else:
                prob = np.ones(len(non_boundary_idx)) / len(non_boundary_idx)

            chosen = rng.choice(
                non_boundary_idx,
                size=min(remaining, len(non_boundary_idx)),
                replace=False,
                p=prob,
            )
            keep_mask[chosen] = True

        elif remaining <= 0 and int(np.sum(is_boundary)) > n_keep_s:
            # Too many boundary samples, trim by keeping lowest-redundancy ones
            b_scores = scores[boundary_idx]
            order = np.argsort(b_scores)  # ascending = lowest redundancy first
            excess = int(np.sum(is_boundary)) - n_keep_s
            to_drop = boundary_idx[order[-excess:]]
            keep_mask[to_drop] = False

    return keep_mask


# ──────────────────────────────────────────────
# Random compression baseline
# ──────────────────────────────────────────────

def random_compress_indices(
    labels: np.ndarray,
    rate: float,
    seed: int = 42,
) -> np.ndarray:
    """Stratified random compression baseline."""
    rng = np.random.RandomState(seed)
    N = len(labels)
    keep_mask = np.zeros(N, dtype=bool)
    for cls in np.unique(labels):
        cls_mask = labels == cls
        cls_idx = np.where(cls_mask)[0]
        n_keep = max(1, int(len(cls_idx) * (1.0 - rate)))
        chosen = rng.choice(cls_idx, size=n_keep, replace=False)
        keep_mask[chosen] = True
    return keep_mask


# ──────────────────────────────────────────────
# Coreset baseline (k-center greedy)
# ──────────────────────────────────────────────

def coreset_compress_indices(
    features: np.ndarray,
    labels: np.ndarray,
    rate: float,
    seed: int = 42,
    max_sample: int = 3000,  # limit for greedy search
) -> np.ndarray:
    """Coreset selection via k-center greedy, stratified by class.

    For very large classes (>max_sample), first subsamples to max_sample,
    runs greedy k-center on the subsample, then uses nearest-neighbor
    assignment for the full set.

    Args:
        features: (N, D) feature vectors.
        labels: (N,) class labels.
        rate: Compression rate (0.2 = remove 20%).
        seed: Random seed.
        max_sample: Max samples per class for greedy search.

    Returns:
        keep_mask: (N,) bool array, True for samples to keep.
    """
    N = len(features)
    keep_mask = np.zeros(N, dtype=bool)
    rng = np.random.RandomState(seed)

    for cls in np.unique(labels):
        cls_mask = labels == cls
        cls_idx = np.where(cls_mask)[0]
        n_cls = len(cls_idx)
        n_keep = max(1, int(n_cls * (1.0 - rate)))

        if n_keep >= n_cls:
            keep_mask[cls_idx] = True
            continue

        X_cls = features[cls_idx]

        if n_cls <= max_sample:
            # ── Greedy k-center on full class ──
            idx_map = np.arange(n_cls)
            sub_X = X_cls
        else:
            # ── Subsample, then nearest-neighbor project ──
            sub_idx = rng.choice(n_cls, size=max_sample, replace=False)
            sub_idx.sort()
            idx_map = sub_idx
            sub_X = X_cls[sub_idx]

        # Greedy k-center on (sub)set
        n_sub = len(sub_X)
        n_keep_sub = max(1, int(n_sub * (1.0 - rate)))

        first = rng.randint(n_sub)
        selected_local = [first]
        dists = np.full(n_sub, np.inf)

        while len(selected_local) < n_keep_sub:
            newest = selected_local[-1]
            d_new = np.linalg.norm(sub_X - sub_X[newest], axis=1)
            dists = np.minimum(dists, d_new)
            cand = np.argmax(dists)
            selected_local.append(cand)

        selected_indices = cls_idx[idx_map[np.array(selected_local)]]

        if n_cls > max_sample:
            # Nearest-neighbor assignment for remaining samples
            sub_selected = sub_X[np.array(selected_local)]
            # For each non-selected sample, find nearest selected
            remaining = np.setdiff1d(np.arange(n_cls), idx_map[selected_local])
            if len(remaining) > 0:
                X_rem = X_cls[remaining]
                # Compute distances to all selected points
                nn_dists = np.linalg.norm(X_rem[:, None] - sub_selected[None, :], axis=2)
                nearest = np.argmin(nn_dists, axis=1)
                # Keep the nearest samples to each selected center
                for s_idx in range(len(selected_local)):
                    assigned = remaining[nearest == s_idx]
                    assigned_sorted = assigned[np.argsort(np.linalg.norm(X_cls[assigned] - sub_selected[s_idx], axis=1))]
                    # Keep up to original n_keep_sub per cluster (spread evenly)
                    per_cluster_budget = max(1, (n_keep - len(selected_indices)) // len(selected_local))
                    take = assigned_sorted[:per_cluster_budget]
                    selected_indices = np.concatenate([selected_indices, cls_idx[take]])

            selected_indices = selected_indices[:n_keep]

        keep_mask[selected_indices] = True

    return keep_mask


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_compress(cfg: CompressConfig) -> dict:
    """Run the compression experiment with real SCX calls."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Compress Experiment (v2) ===")
    print(f"Dataset: {cfg.dataset}")
    print(f"Model:   {cfg.model}")
    print(f"Device:  {cfg.device}")
    print(f"States:  {cfg.n_states}")
    print(f"Augment: {cfg.augment}")
    print()

    # 1. Load data (with optional augmentation)
    print("[1/7] Loading dataset...")
    import torchvision.transforms as T
    base_transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.5], std=[0.5]),
    ])
    if cfg.augment:
        train_transform = T.Compose([
            T.RandomHorizontalFlip(p=0.5),
            T.RandomRotation(degrees=10),
            T.ToTensor(),
            T.Normalize(mean=[0.5], std=[0.5]),
        ])
    else:
        train_transform = base_transform

    loaders = load_medmnist(
        name=cfg.dataset,
        root=cfg.data_root,
        batch_size=cfg.batch_size,
        transform=base_transform,
    )
    # Re-create train loader with optional augmentation transform
    DatasetClass = None
    import medmnist
    for name_c, cls in [('pathmnist', medmnist.PathMNIST),
                         ('dermamnist', medmnist.DermaMNIST),
                         ('bloodmnist', medmnist.BloodMNIST)]:
        if cfg.dataset.lower() == name_c:
            DatasetClass = cls
            break
    train_set_aug = DatasetClass(split='train', transform=train_transform, download=False, root=cfg.data_root)
    train_loader_aug = torch.utils.data.DataLoader(
        train_set_aug, batch_size=cfg.batch_size, shuffle=True,
    )
    loaders['train'] = train_loader_aug
    train_set = loaders['train'].dataset
    val_loader = loaders['val']
    test_loader = loaders['test']
    print(f"  Train: {len(train_set)} samples")
    print(f"  Val:   {len(val_loader.dataset)} samples")
    print(f"  Test:  {len(test_loader.dataset)} samples")
    print()

    # 2. Train baseline
    print("[2/7] Training baseline model...")
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
    print("[3/7] Extracting penultimate-layer features...")
    features, labels = extract_features(baseline, loaders['train'], cfg.device)
    print(f"  Features shape: {features.shape}")
    print()

    # 4. Compute residuals (per-sample cross-entropy loss)
    print("[4/7] Computing per-sample residuals...")
    residuals = compute_residuals(baseline, loaders['train'], cfg.device)
    print(f"  Residual stats: mean={residuals.mean():.4f}, std={residuals.std():.4f}")
    print()

    # 5. SCX redundancy scoring
    print("[5/7] Running SCX StateDiscovery + redundancy scoring...")
    scores, state_labels, centroids = scx_compute_redundancy(
        features, residuals, n_states=cfg.n_states, seed=cfg.seed,
    )
    print(f"  State distribution: {np.bincount(state_labels)}")
    print(f"  Redundancy scores: min={scores.min():.4f}, max={scores.max():.4f}")
    print()

    # 6. Compress and retrain
    print("[6/7] Compressing and retraining...")
    results = {
        'baseline_accuracy': float(baseline_test_acc),
        'compression_results': [],
    }

    for rate in cfg.compression_rates:
        print(f"\n  --- Compression rate: {rate*100:.0f}% ---")

        if rate == 0.0:
            results['compression_results'].append({
                'rate': rate,
                'n_train_kept': len(train_set),
                'scx_accuracy': float(baseline_test_acc),
                'scx_delta': 0.0,
                'random_accuracy': float(baseline_test_acc),
                'random_delta': 0.0,
                'coreset_accuracy': float(baseline_test_acc),
                'coreset_delta': 0.0,
            })
            continue

        # ---- SCX-Compress ----
        scx_keep = scx_compress_indices(
            scores, state_labels, residuals, rate,
            n_states=cfg.n_states, seed=cfg.seed,
        )
        scx_indices = np.where(scx_keep)[0]
        scx_subset = torch.utils.data.Subset(train_set, scx_indices)
        scx_loader = torch.utils.data.DataLoader(
            scx_subset, batch_size=cfg.batch_size, shuffle=True,
        )

        scx_model = create_encoder(
            model_name=cfg.model,
            in_channels=cfg.in_channels,
            num_classes=cfg.num_classes,
            pretrained=False,
        ).to(cfg.device)
        scx_opt = optim.Adam(scx_model.parameters(), lr=cfg.lr,
                              weight_decay=cfg.weight_decay)
        for epoch in range(cfg.epochs):
            train_epoch(scx_model, scx_loader, scx_opt, criterion, cfg.device)
        scx_acc = evaluate(scx_model, test_loader, cfg.device)
        print(f"  SCX-Compress:  {scx_acc:.4f} (delta: {scx_acc - baseline_test_acc:+.4f})")

        # ---- Random baseline ----
        rnd_keep = random_compress_indices(labels, rate, seed=cfg.seed)
        rnd_indices = np.where(rnd_keep)[0]
        rnd_subset = torch.utils.data.Subset(train_set, rnd_indices)
        rnd_loader = torch.utils.data.DataLoader(
            rnd_subset, batch_size=cfg.batch_size, shuffle=True,
        )
        rnd_model = create_encoder(
            model_name=cfg.model,
            in_channels=cfg.in_channels,
            num_classes=cfg.num_classes,
            pretrained=False,
        ).to(cfg.device)
        rnd_opt = optim.Adam(rnd_model.parameters(), lr=cfg.lr,
                              weight_decay=cfg.weight_decay)
        for epoch in range(cfg.epochs):
            train_epoch(rnd_model, rnd_loader, rnd_opt, criterion, cfg.device)
        rnd_acc = evaluate(rnd_model, test_loader, cfg.device)
        print(f"  Random:        {rnd_acc:.4f} (delta: {rnd_acc - baseline_test_acc:+.4f})")

        # ---- Coreset baseline ----
        coreset_keep = coreset_compress_indices(features, labels, rate, seed=cfg.seed)
        coreset_indices = np.where(coreset_keep)[0]
        coreset_subset = torch.utils.data.Subset(train_set, coreset_indices)
        coreset_loader = torch.utils.data.DataLoader(
            coreset_subset, batch_size=cfg.batch_size, shuffle=True,
        )
        coreset_model = create_encoder(
            model_name=cfg.model,
            in_channels=cfg.in_channels,
            num_classes=cfg.num_classes,
            pretrained=False,
        ).to(cfg.device)
        coreset_opt = optim.Adam(coreset_model.parameters(), lr=cfg.lr,
                                  weight_decay=cfg.weight_decay)
        for epoch in range(cfg.epochs):
            train_epoch(coreset_model, coreset_loader, coreset_opt, criterion, cfg.device)
        coreset_acc = evaluate(coreset_model, test_loader, cfg.device)
        print(f"  Coreset:       {coreset_acc:.4f} (delta: {coreset_acc - baseline_test_acc:+.4f})")

        results['compression_results'].append({
            'rate': rate,
            'n_train_kept': len(scx_indices),
            'scx_accuracy': float(scx_acc),
            'scx_delta': float(scx_acc - baseline_test_acc),
            'random_accuracy': float(rnd_acc),
            'random_delta': float(rnd_acc - baseline_test_acc),
            'coreset_accuracy': float(coreset_acc),
            'coreset_delta': float(coreset_acc - baseline_test_acc),
        })

    print()

    # 7. Summarize
    print("[7/7] Summary:")
    print(f"  Baseline (100%): {results['baseline_accuracy']:.4f}")
    for r in results['compression_results']:
        if r['rate'] == 0.0:
            continue
        rate_pct = int(r['rate'] * 100)
        print(f"  Rate {rate_pct}% | SCX: {r['scx_accuracy']:.4f} (delta={r['scx_delta']:+.4f})"
              f" | Random: {r['random_accuracy']:.4f} (delta={r['random_delta']:+.4f})"
              f" | Coreset: {r['coreset_accuracy']:.4f} (delta={r['coreset_delta']:+.4f})")

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
    parser.add_argument('--n-states', type=int, default=10)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--device', default=None)
    parser.add_argument('--output-dir', default='./results/compress')
    parser.add_argument('--augment', action='store_true', help='Enable data augmentation')
    args = parser.parse_args()

    cfg = CompressConfig(
        dataset=args.dataset,
        data_root=args.data_root,
        model=args.model,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=args.lr,
        n_states=args.n_states,
        output_dir=args.output_dir,
        augment=args.augment,
    )
    if args.device:
        cfg.device = args.device

    run_compress(cfg)
