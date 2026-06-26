#!/usr/bin/env python
"""SCX-Noise: distinguish noisy labels from hard cases on MedMNIST.

Uses real SCX library calls:
  - scx.state.discovery.StateDiscovery for state discovery
  - scx.valuation.noise_score.NoiseScore for per-sample noise scoring
  - scx.valuation.learnability.LearnabilityScore for state-level consistency

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

# Add src to path (scx_health + scx framework)
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, '..', '..', 'src'))       # scx_health
sys.path.insert(0, os.path.join(_script_dir, '..', '..', '..', 'src')) # scx framework

from scx_health.data_loader import load_medmnist, extract_features
from scx_health.encoder import create_encoder

# ── SCX imports ─────────────────────────────────────
from scx.state.discovery import StateDiscovery
from scx.valuation.noise_score import NoiseScore
from scx.valuation.learnability import LearnabilityScore


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class NoiseConfig:
    dataset: str = 'dermamnist'
    data_root: str = './data'
    model: str = 'resnet18'
    in_channels: int = 3
    num_classes: int = 7
    batch_size: int = 64
    epochs: int = 30
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    n_states: int = 8
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
) -> tuple:
    """Randomly flip a fraction of labels.

    Returns:
        (noisy_labels, noise_mask) where noise_mask[i] = True if label was flipped.
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
        targets = targets.view(-1)  # MedMNIST labels are (N, 1)
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
        targets = targets.view(-1)  # MedMNIST labels are (N, 1)
        outputs = model(inputs)
        preds = outputs.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)
    return correct / total


@torch.no_grad()
def compute_residuals(model, loader, device):
    """Compute per-sample cross-entropy loss as residual."""
    model.eval()
    all_res = []
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        targets = targets.view(-1)  # MedMNIST labels are (N, 1)
        outputs = model(inputs)
        loss = nn.functional.cross_entropy(outputs, targets, reduction='none')
        all_res.append(loss.cpu().numpy())
    return np.concatenate(all_res, axis=0)


# ──────────────────────────────────────────────
# SCX-Noise core — real SCX calls
# ──────────────────────────────────────────────

def scx_compute_noise_scores(
    features: np.ndarray,
    noisy_labels: np.ndarray,
    residuals: np.ndarray,
    n_states: int = 8,
    seed: int = 42,
) -> tuple:
    """Compute per-sample noise scores using SCX NoiseScore + LearnabilityScore.

    Pipeline:
      1. StateDiscovery on feature space
      2. For each state: compute consistency via LearnabilityScore
      3. Compute per-sample noise score via NoiseScore.compute()
      4. Detect noisy samples via NoiseScore.detect_noisy_samples()

    Returns:
        (noise_scores, state_labels, noisy_indices, state_metrics)
    """
    # 1. State discovery
    discovery = StateDiscovery(method='kmeans', n_states=n_states, random_state=seed)
    state_labels = discovery.fit_predict(features)
    centroids = discovery.get_centroids()

    # 2. Per-state noise scoring
    noise_eval = NoiseScore()
    learn_eval = LearnabilityScore()

    N = len(features)
    noise_scores = np.zeros(N)
    state_metrics = {}

    for s in range(n_states):
        mask = state_labels == s
        n_s = mask.sum()
        if n_s == 0:
            continue

        X_s = features[mask]
        y_s = noisy_labels[mask]
        res_s = residuals[mask]
        state_proportion = n_s / N

        # Compute state consistency using labels (label-based purity)
        # High C(s) = labels are consistent within state
        C_s = learn_eval.consistency(X_s, y_s=y_s)

        # Compute per-sample noise score
        # NoiseScore(x_i) = r_i / (rho(s) + eps) * (1 - C(s))
        scores_s = noise_eval.compute(
            residuals=res_s,
            state_proportion=state_proportion,
            consistency=C_s,
        )
        noise_scores[mask] = scores_s
        state_metrics[s] = {
            'n_samples': int(n_s),
            'proportion': float(state_proportion),
            'consistency': float(C_s),
            'mean_noise_score': float(np.mean(scores_s)),
        }

    # 3. Detect noisy samples using IQR threshold
    noisy_indices = noise_eval.detect_noisy_samples(noise_scores)

    return noise_scores, state_labels, noisy_indices, state_metrics


# ──────────────────────────────────────────────
# Loss-based baseline
# ──────────────────────────────────────────────

def loss_based_detection(residuals: np.ndarray, threshold: float = None):
    """Use raw loss as noise proxy (baseline)."""
    if threshold is None:
        q3 = float(np.percentile(residuals, 75))
        iqr = float(np.percentile(residuals, 75) - np.percentile(residuals, 25))
        threshold = q3 + 1.5 * iqr
    return residuals, np.where(residuals > threshold)[0]


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_noise_detection(cfg: NoiseConfig) -> dict:
    """Run the noise detection experiment with real SCX calls."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Noise Experiment ===")
    print(f"Dataset: {cfg.dataset}")
    print(f"Model:   {cfg.model}")
    print(f"Device:  {cfg.device}")
    print(f"States:  {cfg.n_states}")
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
            train_set_noisy.labels = noisy_labels.numpy().ravel()

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

        # 4. Extract features & compute SCX noise scores
        print(f"\n[4/5] Computing SCX noise scores...")
        features, pred_labels = extract_features(model, noisy_loader, cfg.device)
        residuals = compute_residuals(model, noisy_loader, cfg.device)

        # Real SCX noise detection
        noise_scores, state_labels, noisy_indices, state_metrics = \
            scx_compute_noise_scores(
                features, noisy_labels.numpy(), residuals,
                n_states=cfg.n_states, seed=cfg.seed,
            )

        # Baseline: raw loss-based detection
        loss_scores, loss_noisy_idx = loss_based_detection(residuals)

        n_scx_detected = len(noisy_indices)
        n_scx_actually_noisy = int(noise_mask.numpy()[noisy_indices].sum()) if n_scx_detected > 0 else 0
        print(f"  SCX flagged {n_scx_detected} samples as noisy "
              f"({n_scx_actually_noisy} actually noisy)")

        # 5. Evaluate detection
        print(f"\n[5/5] Evaluating noise detection...")
        y_true = noise_mask.numpy().astype(int)

        # SCX-Noise ROC-AUC
        if len(np.unique(y_true)) > 1:
            scx_roc_auc = roc_auc_score(y_true, noise_scores)
            scx_pr_auc = average_precision_score(y_true, noise_scores)
        else:
            scx_roc_auc = float('nan')
            scx_pr_auc = float('nan')

        # Loss-based ROC-AUC
        if len(np.unique(y_true)) > 1:
            loss_roc_auc = roc_auc_score(y_true, loss_scores)
            loss_pr_auc = average_precision_score(y_true, loss_scores)
        else:
            loss_roc_auc = float('nan')
            loss_pr_auc = float('nan')

        print(f"  SCX-Noise  ROC-AUC: {scx_roc_auc:.4f}  PR-AUC: {scx_pr_auc:.4f}")
        print(f"  Loss-based ROC-AUC: {loss_roc_auc:.4f}  PR-AUC: {loss_pr_auc:.4f}")

        all_results[f'noise_rate_{noise_rate:.0%}'] = {
            'noise_rate': noise_rate,
            'test_accuracy': float(test_acc),
            'scx_roc_auc': float(scx_roc_auc),
            'scx_pr_auc': float(scx_pr_auc),
            'loss_roc_auc': float(loss_roc_auc),
            'loss_pr_auc': float(loss_pr_auc),
            'n_flagged_scx': n_scx_detected,
            'n_actually_noisy': int(noise_mask.sum().item()),
            'state_metrics': {str(k): v for k, v in state_metrics.items()},
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
    parser.add_argument('--n-states', type=int, default=8)
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
        n_states=args.n_states,
        output_dir=args.output_dir,
    )
    run_noise_detection(cfg)
