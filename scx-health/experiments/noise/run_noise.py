#!/usr/bin/env python
"""SCX-Noise: distinguish noisy labels from hard cases on MedMNIST.

Uses real SCX library calls:
  - scx.state.discovery.StateDiscovery for state discovery
  - scx.valuation.noise_score.NoiseScore for per-sample noise scoring
  - scx.valuation.learnability.LearnabilityScore for state-level consistency

Workflow:
  1. Load DermaMNIST (small, challenging dataset)
  2. Inject synthetic label noise (10%, 20%, 40% random flips)
  3. Also inject per-class (non-uniform) noise for harder detection
  4. Train model on noisy data
  5. Extract features and compute SCX NoiseScore per sample
  6. Evaluate: can NoiseScore separate noisy from clean samples?
  7. Compare: SCX-Noise vs Loss-based vs Confidence-based vs ErrorDriven
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
    model: str = 'simple_cnn'
    in_channels: int = 3
    num_classes: int = 7
    batch_size: int = 128
    epochs: int = 30
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    n_states: int = 8
    noise_rates: list = field(default_factory=lambda: [0.0, 0.1, 0.2, 0.4])
    output_dir: str = './results/noise'
    seed: int = 42
    per_class_noise: bool = False  # Non-uniform per-class noise


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
# Per-class (non-uniform) noise injection
# ──────────────────────────────────────────────

def inject_per_class_label_noise(
    labels: torch.Tensor,
    base_noise_rate: float,
    num_classes: int,
    seed: int,
    factor_range: tuple = (0.3, 2.5),
) -> tuple:
    """Inject non-uniform label noise.

    Each class gets a different noise rate drawn from
    base_noise_rate * factor, where factor varies per class.
    This simulates real-world conditions where some classes
    are noisier than others.

    Returns:
        (noisy_labels, noise_mask)
    """
    rng = np.random.RandomState(seed)
    n = len(labels)
    noisy = labels.clone()
    noise_mask = torch.zeros(n, dtype=torch.bool)

    # Per-class noise factors
    factors = rng.uniform(factor_range[0], factor_range[1], size=num_classes)

    for cls in range(num_classes):
        cls_mask = (labels == cls).numpy().ravel()
        cls_idx = np.where(cls_mask)[0]
        cls_rate = base_noise_rate * factors[cls]
        cls_rate = min(cls_rate, 0.8)  # Cap at 80%
        n_flip = max(1, int(len(cls_idx) * cls_rate))

        flip_idx = rng.choice(cls_idx, n_flip, replace=False)
        for idx in flip_idx:
            choices = [c for c in range(num_classes) if c != int(labels[idx])]
            noisy[idx] = rng.choice(choices)
            noise_mask[idx] = True

    return noisy, noise_mask


# ──────────────────────────────────────────────
# Confidence-based detection
# ──────────────────────────────────────────────

def confidence_based_detection(
    logits: np.ndarray,
) -> tuple:
    """Use softmax confidence as noise proxy.

    Low-confidence samples (softmax probability < threshold)
    are flagged as potentially noisy.

    Returns:
        (confidence_scores, flagged_indices)
    """
    # Softmax
    shifted = logits - logits.max(axis=1, keepdims=True)
    softmax = np.exp(shifted) / np.exp(shifted).sum(axis=1, keepdims=True)
    confidence = softmax.max(axis=1)  # max probability per sample

    # IQR-based threshold on low confidence
    low_conf = 1.0 - confidence
    q3 = float(np.percentile(low_conf, 75))
    iqr = float(np.percentile(low_conf, 75) - np.percentile(low_conf, 25))
    threshold = q3 + 1.5 * iqr
    flagged = np.where(low_conf > threshold)[0]

    return confidence, flagged


# ──────────────────────────────────────────────
# ErrorDriven detection
# ──────────────────────────────────────────────

def error_driven_detection(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    device: str,
    n_perturbations: int = 3,
) -> tuple:
    """ErrorDriven: measure prediction instability under small model perturbations.

    The idea: noisy-label samples have unstable predictions because the model
    is memorizing wrong labels.  By injecting small random noise into the
    model parameters and observing prediction changes, we can detect samples
    whose predictions are fragile (i.e., likely noisy).

    This is inspired by the "Error-Driven Detection" paradigm:
    samples with high prediction variance under model perturbation are
    likely to be noisy.

    Returns:
        (instability_scores, flagged_indices)
    """
    model.eval()
    orig_state = {k: v.clone() for k, v in model.state_dict().items()}

    N = len(loader.dataset)
    all_preds = []
    rng_state = torch.get_rng_state()

    for p_idx in range(n_perturbations):
        # Restore original weights
        model.load_state_dict(orig_state)

        # Add small noise to classifier weights
        with torch.no_grad():
            for name, param in model.named_parameters():
                if 'classifier' in name or 'fc' in name:
                    noise = torch.randn_like(param) * 0.01
                    param.add_(noise)

        # Predict on all samples
        epoch_preds = []
        for inputs, _ in loader:
            inputs = inputs.to(device)
            with torch.no_grad():
                outputs = model(inputs)
                preds = outputs.argmax(dim=1).cpu().numpy()
            epoch_preds.append(preds)
        all_preds.append(np.concatenate(epoch_preds))

    # Restore original model state
    model.load_state_dict(orig_state)
    torch.set_rng_state(rng_state)

    # Compute prediction instability: fraction of perturbations where
    # prediction differs from the majority vote
    all_preds = np.stack(all_preds, axis=0)  # (n_perturbations, N)
    majority = np.zeros(N, dtype=int)
    for i in range(N):
        votes = np.bincount(all_preds[:, i])
        majority[i] = np.argmax(votes)

    instability = np.mean(all_preds != majority, axis=0)  # fraction disagreeing

    # Flag samples with instability > 0 (at least 1 perturbation disagrees)
    flagged = np.where(instability > 0.0)[0]

    return instability, flagged


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_noise_detection(cfg: NoiseConfig) -> dict:
    """Run the noise detection experiment with real SCX calls."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Noise Experiment (v2) ===")
    print(f"Dataset: {cfg.dataset}")
    print(f"Model:   {cfg.model}")
    print(f"Device:  {cfg.device}")
    print(f"States:  {cfg.n_states}")
    print(f"Per-class noise: {cfg.per_class_noise}")
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

        if cfg.per_class_noise and noise_rate > 0:
            # Non-uniform per-class noise
            noisy_labels, noise_mask = inject_per_class_label_noise(
                clean_labels, noise_rate, cfg.num_classes, seed=cfg.seed,
            )
            # Print per-class noise statistics
            for cls in range(cfg.num_classes):
                cls_mask = (clean_labels == cls).numpy().ravel()
                cls_noisy = noise_mask.numpy()[cls_mask]
                if len(cls_noisy) > 0:
                    cls_rate = cls_noisy.mean()
                    print(f"    Class {cls}: {cls_rate*100:.1f}% noisy ({cls_noisy.sum()}/{len(cls_noisy)})")
        else:
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

        # 4. Extract features & compute noise scores from all methods
        print(f"\n[4/5] Computing noise detection scores...")
        features, pred_labels = extract_features(model, noisy_loader, cfg.device)
        residuals = compute_residuals(model, noisy_loader, cfg.device)

        # ── a) SCX Noise detection ──
        noise_scores, state_labels, noisy_indices, state_metrics = \
            scx_compute_noise_scores(
                features, noisy_labels.numpy(), residuals,
                n_states=cfg.n_states, seed=cfg.seed,
            )

        # ── b) Loss-based detection ──
        loss_scores, loss_noisy_idx = loss_based_detection(residuals)

        # ── c) Confidence-based detection ──
        # Collect logits for all training samples
        model.eval()
        all_logits = []
        with torch.no_grad():
            for inputs, _ in noisy_loader:
                inputs = inputs.to(cfg.device)
                logits = model(inputs).cpu().numpy()
                all_logits.append(logits)
        all_logits = np.concatenate(all_logits, axis=0)
        conf_scores, conf_noisy_idx = confidence_based_detection(all_logits)

        # ── d) ErrorDriven detection ──
        inst_scores, errdriven_noisy_idx = error_driven_detection(
            model, noisy_loader, cfg.device, n_perturbations=3,
        )

        n_scx_detected = len(noisy_indices)
        n_scx_actually_noisy = int(noise_mask.numpy()[noisy_indices].sum()) if n_scx_detected > 0 else 0
        print(f"  SCX flagged {n_scx_detected} samples as noisy "
              f"({n_scx_actually_noisy} actually noisy)")

        # 5. Evaluate detection
        print(f"\n[5/5] Evaluating noise detection...")
        y_true = noise_mask.numpy().astype(int)

        def safe_auc(y_true, scores):
            if len(np.unique(y_true)) > 1:
                return (
                    float(roc_auc_score(y_true, scores)),
                    float(average_precision_score(y_true, scores)),
                )
            return float('nan'), float('nan')

        scx_roc_auc, scx_pr_auc = safe_auc(y_true, noise_scores)
        loss_roc_auc, loss_pr_auc = safe_auc(y_true, loss_scores)
        conf_roc_auc, conf_pr_auc = safe_auc(y_true, 1.0 - conf_scores)  # invert confidence
        errdriven_roc_auc, errdriven_pr_auc = safe_auc(y_true, inst_scores)

        print(f"  SCX-Noise        ROC-AUC: {scx_roc_auc:.4f}  PR-AUC: {scx_pr_auc:.4f}")
        print(f"  Loss-based       ROC-AUC: {loss_roc_auc:.4f}  PR-AUC: {loss_pr_auc:.4f}")
        print(f"  Confidence-based ROC-AUC: {conf_roc_auc:.4f}  PR-AUC: {conf_pr_auc:.4f}")
        print(f"  ErrorDriven      ROC-AUC: {errdriven_roc_auc:.4f}  PR-AUC: {errdriven_pr_auc:.4f}")

        all_results[f'noise_rate_{noise_rate:.0%}'] = {
            'noise_rate': noise_rate,
            'per_class_noise': cfg.per_class_noise,
            'test_accuracy': float(test_acc),
            'scx_roc_auc': scx_roc_auc,
            'scx_pr_auc': scx_pr_auc,
            'loss_roc_auc': loss_roc_auc,
            'loss_pr_auc': loss_pr_auc,
            'confidence_roc_auc': conf_roc_auc,
            'confidence_pr_auc': conf_pr_auc,
            'errdriven_roc_auc': errdriven_roc_auc,
            'errdriven_pr_auc': errdriven_pr_auc,
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
    parser.add_argument('--model', default='simple_cnn',
                        choices=['simple_cnn', 'resnet18'])
    parser.add_argument('--batch-size', type=int, default=128)
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--n-states', type=int, default=8)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--output-dir', default='./results/noise')
    parser.add_argument('--per-class-noise', action='store_true',
                        help='Use non-uniform per-class noise injection')
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
        per_class_noise=args.per_class_noise,
    )
    run_noise_detection(cfg)
