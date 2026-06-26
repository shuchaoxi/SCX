#!/usr/bin/env python
"""SCX-Routing: state-conditioned expert selection on MedMNIST.

Uses real SCX library calls:
  - scx.state.discovery.StateDiscovery for state discovery
  - scx.expert.registry.ExpertRegistry for managing multiple experts
  - scx.expert.reliability.ExpertReliability for state-conditioned reliability
  - scx.expert.router.ExpertRouter for state-conditioned routing

Workflow:
  1. Load BloodMNIST (8-class blood cell classification)
  2. Train N experts (ResNet-18 with different initializations)
  3. Extract features and define "diagnostic states" via SCX StateDiscovery
  4. Evaluate: SCX-Routing vs Uniform Ensemble vs Single Best Expert
"""

import os
import sys
import argparse
import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Callable

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
from scx.state.assignment import StateAssignment
from scx.expert.registry import ExpertRegistry
from scx.expert.reliability import ExpertReliability
from scx.expert.router import ExpertRouter


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class RoutingConfig:
    dataset: str = 'bloodmnist'
    data_root: str = './data'
    model: str = 'resnet18'
    in_channels: int = 3
    num_classes: int = 8
    n_experts: int = 5
    n_states: int = 8
    batch_size: int = 64
    expert_epochs: int = 30
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    output_dir: str = './results/routing'
    seed: int = 42


# ──────────────────────────────────────────────
# Training helpers
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


def train_expert(
    loaders: dict,
    num_classes: int,
    device: str,
    epochs: int,
    lr: float,
    weight_decay: float,
    seed: int,
    model_name: str = 'resnet18',
) -> nn.Module:
    """Train a single expert model."""
    torch.manual_seed(seed)
    model = create_encoder(
        model_name=model_name,
        in_channels=3,
        num_classes=num_classes,
        pretrained=False,
    ).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss()
    for epoch in range(epochs):
        train_epoch(model, loaders['train'], optimizer, criterion, device)
    return model


# ──────────────────────────────────────────────
# Raw image collector for ExpertRegistry
# ──────────────────────────────────────────────

@torch.no_grad()
def collect_raw_data(
    loader: torch.utils.data.DataLoader,
    device: str,
) -> tuple:
    """Collect raw image arrays and labels from a DataLoader.

    Returns:
        (images_np, labels_np)
        images_np: np.ndarray, shape (N, C, H, W)
        labels_np: np.ndarray, shape (N,)
    """
    all_imgs, all_labels = [], []
    for inputs, targets in loader:
        all_imgs.append(inputs.cpu().numpy())
        all_labels.append(targets.cpu().numpy().ravel())
    return np.concatenate(all_imgs, axis=0), np.concatenate(all_labels, axis=0)


# ──────────────────────────────────────────────
# SCX-Routing evaluation — real SCX calls
# ──────────────────────────────────────────────

def logit_cross_entropy_loss(y_pred_logits: np.ndarray, y_true: np.ndarray) -> np.ndarray:
    """Per-sample cross-entropy loss from logits and integer labels.

    y_pred_logits: (N, C) — raw logits
    y_true: (N,) — integer class labels
    Returns: (N,) per-sample loss
    """
    y_pred = np.asarray(y_pred_logits, dtype=float)
    y_true = np.asarray(y_true, dtype=int).ravel()
    # Numerically stable softmax
    shifted = y_pred - y_pred.max(axis=1, keepdims=True)
    softmax = np.exp(shifted) / np.exp(shifted).sum(axis=1, keepdims=True)
    n = len(y_true)
    return -np.log(softmax[np.arange(n), y_true] + 1e-10)


def make_expert_predict_fn(
    model: nn.Module,
    device: str,
) -> Callable:
    """Wrap a PyTorch model as a numpy-compatible predict_fn for ExpertRegistry.

    Input: numpy array of shape (N, C, H, W) -- raw images.
    Output: numpy array of shape (N, num_classes) -- logits.
    """
    def predict_fn(X: np.ndarray) -> np.ndarray:
        model.eval()
        # Ensure 4D input (N, C, H, W)
        if X.ndim == 3:
            X = X[np.newaxis, ...]
        X_t = torch.tensor(X, dtype=torch.float32, device=device)
        with torch.no_grad():
            logits = model(X_t).cpu().numpy()
        return logits
    return predict_fn


def scx_routing_evaluation(
    experts: List[nn.Module],
    train_state_assignments: np.ndarray,
    n_states: int,
    X_val_images: np.ndarray,
    y_val: np.ndarray,
    X_test_images: np.ndarray,
    y_test: np.ndarray,
    val_state_assignments: np.ndarray,
    test_state_assignments: np.ndarray,
    device: str,
) -> dict:
    """Evaluate SCX-Routing using SCX ExpertRegistry, ExpertReliability, ExpertRouter.

    Pipeline:
      1. Register experts in ExpertRegistry
      2. Estimate state-conditioned reliability via ExpertReliability (val set)
      3. Route via ExpertRouter (weighted mode vs hard mode vs uniform)
      4. Compare routing strategies on test set
    """
    # 1. Register experts
    registry = ExpertRegistry()
    for i, expert in enumerate(experts):
        registry.register(
            name=f'expert_{i}',
            predict_fn=make_expert_predict_fn(expert, device),
            cost=1.0,
        )
    M = len(registry)
    print(f"  Registered {M} experts in SCX ExpertRegistry")

    # 2. Estimate state-conditioned reliability on validation set
    reliability = ExpertReliability(method='supervised', alpha=1.0, min_samples=5)
    result = reliability.estimate(
        registry,
        X=X_val_images,
        y=y_val,
        state_assignments=val_state_assignments,
        n_states=n_states,
        loss_fn=logit_cross_entropy_loss,
    )
    R_matrix = result['R_matrix']
    SCX_matrix = result['SCX_matrix']
    n_per_state = result['n_per_state']
    print(f"  ExpertReliability: R_matrix shape={R_matrix.shape}")
    print(f"  Per-state val samples: {n_per_state}")

    # 3. Setup ExpertRouter
    router = ExpertRouter(registry, reliability, alpha=1.0)

    # 4. Evaluate all strategies on test set
    N_test = len(y_test)

    # ── a) Uniform ensemble ──
    all_preds = registry.predict_all(X_test_images)  # (M, N, C)
    uniform_logits = all_preds.mean(axis=0)
    uniform_preds = np.argmax(uniform_logits, axis=1)
    ensemble_acc = float(np.mean(uniform_preds == y_test))

    # ── b) Single best expert ──
    expert_accs = []
    for m in range(M):
        preds_m = np.argmax(all_preds[m], axis=1)
        acc_m = float(np.mean(preds_m == y_test))
        expert_accs.append(acc_m)
    single_best_acc = max(expert_accs)
    worst_expert_acc = min(expert_accs)

    # ── c) SCX-Weighted Routing ──
    weights = router.route_weighted(X_test_images, test_state_assignments, R_matrix)
    w_reshaped = weights.T.reshape(M, N_test, 1)
    weighted_logits = np.sum(w_reshaped * all_preds, axis=0)
    weighted_preds = np.argmax(weighted_logits, axis=1)
    routing_weighted_acc = float(np.mean(weighted_preds == y_test))

    # ── d) SCX-Hard Routing ──
    expert_ids = router.route_hard(X_test_images, test_state_assignments, R_matrix)
    hard_correct = 0
    for i in range(N_test):
        eid = expert_ids[i]
        info = registry.get(eid)
        single_X = X_test_images[i:i+1]
        pred = info.predict_fn(single_X)
        if pred.ndim > 1:
            pred_class = int(np.argmax(pred[0]))
        else:
            pred_class = int(pred[0])
        hard_correct += int(pred_class == y_test[i])
    routing_hard_acc = hard_correct / N_test

    print(f"\n  === SCX-Routing Evaluation ===")
    print(f"  Worst Expert:          {worst_expert_acc:.4f}")
    print(f"  Single Best Expert:    {single_best_acc:.4f}")
    print(f"  Uniform Ensemble:      {ensemble_acc:.4f}")
    print(f"  SCX-Hard Routing:      {routing_hard_acc:.4f}")
    print(f"  SCX-Weighted Routing:  {routing_weighted_acc:.4f}")
    print(f"  Weighted vs Best:      {routing_weighted_acc - single_best_acc:+.4f}")
    print(f"  Weighted vs Ensemble:  {routing_weighted_acc - ensemble_acc:+.4f}")

    return {
        'n_experts': M,
        'n_states': n_states,
        'worst_expert_accuracy': worst_expert_acc,
        'single_best_expert_accuracy': single_best_acc,
        'ensemble_accuracy': ensemble_acc,
        'scx_hard_routing_accuracy': routing_hard_acc,
        'scx_weighted_routing_accuracy': routing_weighted_acc,
        'improvement_vs_best': float(routing_weighted_acc - single_best_acc),
        'improvement_vs_ensemble': float(routing_weighted_acc - ensemble_acc),
        'expert_test_accuracies': expert_accs,
    }


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_routing(cfg: RoutingConfig) -> dict:
    """Run the routing experiment with real SCX calls."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Routing Experiment ===")
    print(f"Dataset:  {cfg.dataset}")
    print(f"Experts:  {cfg.n_experts} ({cfg.model})")
    print(f"States:   {cfg.n_states}")
    print(f"Device:   {cfg.device}")
    print()

    # 1. Load data
    print("[1/6] Loading dataset...")
    loaders = load_medmnist(
        name=cfg.dataset,
        root=cfg.data_root,
        batch_size=cfg.batch_size,
    )
    train_loader = loaders['train']
    val_loader = loaders['val']
    test_loader = loaders['test']
    print(f"  Train: {len(train_loader.dataset)} samples")
    print(f"  Val:   {len(val_loader.dataset)} samples")
    print(f"  Test:  {len(test_loader.dataset)} samples")
    print()

    # 2. Train experts
    print("[2/6] Training experts...")
    experts = []
    for i in range(cfg.n_experts):
        expert_seed = cfg.seed + i * 100
        print(f"  Training expert {i+1}/{cfg.n_experts} (seed={expert_seed})...")
        expert = train_expert(
            loaders, cfg.num_classes, cfg.device,
            cfg.expert_epochs, cfg.lr, cfg.weight_decay, expert_seed,
            model_name=cfg.model,
        )
        experts.append(expert)
        acc = evaluate(expert, val_loader, cfg.device)
        print(f"    Val accuracy: {acc:.4f}")
    print()

    # 3. Discover states via SCX StateDiscovery
    print("[3/6] Discovering diagnostic states via SCX StateDiscovery...")
    train_features, train_labels = extract_features(
        experts[0], train_loader, cfg.device
    )
    print(f"  Train features: {train_features.shape}")

    discovery = StateDiscovery(
        method='kmeans', n_states=cfg.n_states, random_state=cfg.seed
    )
    train_state_assignments = discovery.fit_predict(train_features)
    centroids = discovery.get_centroids()
    print(f"  State distribution: {np.bincount(train_state_assignments)}")
    print()

    # 4. Extract features for val and test + collect raw images
    print("[4/6] Extracting features & collecting raw images...")

    # State assignments for val/test via nearest-centroid projection
    val_features, val_labels = extract_features(experts[0], val_loader, cfg.device)
    test_features, test_labels = extract_features(experts[0], test_loader, cfg.device)

    val_state_assignments = discovery.predict(val_features)
    test_state_assignments = discovery.predict(test_features)

    print(f"  Val state dist:  {np.bincount(val_state_assignments, minlength=cfg.n_states)}")
    print(f"  Test state dist: {np.bincount(test_state_assignments, minlength=cfg.n_states)}")

    # Collect raw images for ExpertRegistry
    X_val_raw, y_val_raw = collect_raw_data(val_loader, cfg.device)
    X_test_raw, y_test_raw = collect_raw_data(test_loader, cfg.device)
    print(f"  Raw val images:  {X_val_raw.shape}")
    print(f"  Raw test images: {X_test_raw.shape}")
    print()

    # 5. SCX Routing evaluation
    print("[5/6] Evaluating SCX-Routing...")
    routing_results = scx_routing_evaluation(
        experts=experts,
        train_state_assignments=train_state_assignments,
        n_states=cfg.n_states,
        X_val_images=X_val_raw,
        y_val=y_val_raw,
        X_test_images=X_test_raw,
        y_test=y_test_raw,
        val_state_assignments=val_state_assignments,
        test_state_assignments=test_state_assignments,
        device=cfg.device,
    )
    print()

    # 6. Save results
    print("[6/6] Saving results...")
    results = {
        'config': asdict(cfg),
        **routing_results,
    }

    output_path = os.path.join(cfg.output_dir, 'routing_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_path}")

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SCX-Routing on MedMNIST')
    parser.add_argument('--dataset', default='bloodmnist',
                        choices=['pathmnist', 'dermamnist', 'bloodmnist'])
    parser.add_argument('--data-root', default='./data')
    parser.add_argument('--model', default='resnet18',
                        choices=['simple_cnn', 'resnet18'])
    parser.add_argument('--n-experts', type=int, default=5)
    parser.add_argument('--n-states', type=int, default=8)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--expert-epochs', type=int, default=30)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--output-dir', default='./results/routing')
    args = parser.parse_args()

    cfg = RoutingConfig(
        dataset=args.dataset,
        data_root=args.data_root,
        model=args.model,
        n_experts=args.n_experts,
        n_states=args.n_states,
        batch_size=args.batch_size,
        expert_epochs=args.expert_epochs,
        lr=args.lr,
        output_dir=args.output_dir,
    )
    run_routing(cfg)
