#!/usr/bin/env python
"""SCX-Routing: state-conditioned expert selection on MedMNIST.

Workflow:
  1. Load BloodMNIST (8-class blood cell classification)
  2. Train N experts (ResNet-18 with different initializations)
  3. Extract validation features and define "diagnostic states"
     via SCX StateDiscovery
  4. Train a routing network to assign each state to the best expert
  5. Evaluate: SCX-Routing vs Uniform Ensemble vs Single Best Expert
"""

import os
import sys
import argparse
import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.cluster import KMeans

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from scx_health.data_loader import load_medmnist, extract_features
from scx_health.encoder import create_encoder


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

@dataclass
class RoutingConfig:
    dataset: str = 'bloodmnist'
    data_root: str = './data'
    model: str = 'resnet18'
    in_channels: int = 1
    num_classes: int = 8
    n_experts: int = 5
    n_states: int = 8  # number of routing states (clusters)
    batch_size: int = 64
    expert_epochs: int = 30
    router_epochs: int = 20
    lr: float = 1e-3
    weight_decay: float = 1e-4
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    output_dir: str = './results/routing'
    seed: int = 42


# ──────────────────────────────────────────────
# Router network
# ──────────────────────────────────────────────

class StateRouter(nn.Module):
    """Learns to route a state embedding to the best expert."""

    def __init__(self, feat_dim: int, n_states: int, n_experts: int):
        super().__init__()
        self.router = nn.Sequential(
            nn.Linear(feat_dim, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, n_states),
        )
        # State-to-expert assignment matrix (learned)
        self.state_to_expert = nn.Parameter(
            torch.zeros(n_states, n_experts)
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """Return expert weights per sample."""
        state_logits = self.router(features)
        state_weights = torch.softmax(state_logits, dim=-1)
        # Soft assignment from states to experts
        expert_weights = state_weights @ torch.softmax(self.state_to_expert, dim=-1)
        return expert_weights


# ──────────────────────────────────────────────
# Training helpers
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


def train_expert(
    loaders: dict,
    num_classes: int,
    device: str,
    epochs: int,
    lr: float,
    weight_decay: float,
    seed: int,
) -> nn.Module:
    """Train a single expert model."""
    torch.manual_seed(seed)
    model = create_encoder(
        model_name='resnet18',
        in_channels=1,
        num_classes=num_classes,
        pretrained=False,
    ).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss()
    for epoch in range(epochs):
        train_epoch(model, loaders['train'], optimizer, criterion, device)
    return model


# ──────────────────────────────────────────────
# SCX-Routing core (placeholder)
# ──────────────────────────────────────────────

def discover_states(
    features: np.ndarray,
    n_states: int,
    seed: int = 42,
) -> np.ndarray:
    """Placeholder for SCX StateDiscovery.

    TODO: Replace with actual SCX StateDiscovery (Bayesian nonparametric).

    Returns:
        State assignments for each sample.
    """
    kmeans = KMeans(n_clusters=n_states, random_state=seed, n_init=10)
    return kmeans.fit_predict(features)


# ──────────────────────────────────────────────
# Ensemble / Routing evaluation
# ──────────────────────────────────────────────

@torch.no_grad()
def evaluate_ensemble(
    experts: List[nn.Module],
    loader: torch.utils.data.DataLoader,
    device: str,
) -> float:
    """Uniform ensemble: average predictions across all experts."""
    for expert in experts:
        expert.eval()

    correct, total = 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        all_logits = []
        for expert in experts:
            logits = expert(inputs)
            all_logits.append(logits)
        avg_logits = torch.stack(all_logits).mean(dim=0)
        preds = avg_logits.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)
    return correct / total


@torch.no_grad()
def evaluate_routing(
    experts: List[nn.Module],
    router: StateRouter,
    loader: torch.utils.data.DataLoader,
    device: str,
) -> float:
    """SCX-Routing: router selects expert weights per sample."""
    for expert in experts:
        expert.eval()
    router.eval()

    correct, total = 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # Get router weights
        with torch.no_grad():
            # Use first expert as feature extractor for routing
            features = experts[0].forward_features(inputs)
        expert_weights = router(features)

        # Weighted ensemble
        all_logits = []
        for expert in experts:
            logits = expert(inputs)
            all_logits.append(logits)
        stacked = torch.stack(all_logits, dim=-1)  # (B, C, N)
        weights = expert_weights.unsqueeze(1)      # (B, 1, N)
        weighted = (stacked * weights).sum(dim=-1)
        preds = weighted.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)
    return correct / total


# ──────────────────────────────────────────────
# Main experiment
# ──────────────────────────────────────────────

def run_routing(cfg: RoutingConfig) -> dict:
    """Run the routing experiment."""
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    print(f"=== SCX-Routing Experiment ===")
    print(f"Dataset:  {cfg.dataset}")
    print(f"Experts:  {cfg.n_experts}")
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
    val_loader = loaders['val']
    test_loader = loaders['test']
    print(f"  Train: {len(loaders['train'].dataset)} samples")
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
        )
        experts.append(expert)
        acc = evaluate(expert, val_loader, cfg.device)
        print(f"    Val accuracy: {acc:.4f}")
    print()

    # 3. Discover states
    print("[3/6] Discovering diagnostic states...")
    # Extract features using first expert
    feats, _ = extract_features(experts[0], loaders['train'], cfg.device)
    state_assignments = discover_states(feats, cfg.n_states, cfg.seed)
    print(f"  State distribution: {np.bincount(state_assignments)}")
    print()

    # 4. Train router
    print("[4/6] Training state-conditioned router...")
    feat_dim = feats.shape[1]
    router = StateRouter(feat_dim, cfg.n_states, cfg.n_experts).to(cfg.device)
    router_opt = optim.Adam(router.parameters(), lr=cfg.lr)

    # Create state label mapping for router training
    # (learn to predict which expert is best per sample)
    for epoch in range(cfg.router_epochs):
        router.train()
        total_loss = 0.0
        for inputs, targets in loaders['train']:
            inputs, targets = inputs.to(cfg.device), targets.to(cfg.device)

            # Get features from first expert
            with torch.no_grad():
                features = experts[0].forward_features(inputs)

            # Compute per-expert accuracy on this batch as routing target
            with torch.no_grad():
                expert_correct = []
                for expert in experts:
                    logits = expert(inputs)
                    preds = logits.argmax(dim=1)
                    expert_correct.append((preds == targets).float())
                # Best expert index per sample
                best_expert = torch.stack(expert_correct).argmax(dim=0)

            # Router predicts expert weights
            expert_weights = router(features)
            router_loss = nn.CrossEntropyLoss()(expert_weights, best_expert)

            router_opt.zero_grad()
            router_loss.backward()
            router_opt.step()
            total_loss += router_loss.item() * inputs.size(0)

        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1:2d}/{cfg.router_epochs} | "
                  f"Router Loss: {total_loss/len(loaders['train'].dataset):.4f}")
    print()

    # 5. Evaluate
    print("[5/6] Evaluating...")
    single_best_acc = max(
        evaluate(expert, test_loader, cfg.device) for expert in experts
    )
    ensemble_acc = evaluate_ensemble(experts, test_loader, cfg.device)
    routing_acc = evaluate_routing(experts, router, test_loader, cfg.device)

    print(f"\n  Single Best Expert:  {single_best_acc:.4f}")
    print(f"  Uniform Ensemble:    {ensemble_acc:.4f}")
    print(f"  SCX-Routing:         {routing_acc:.4f}")
    print()

    # 6. Save results
    print("[6/6] Saving results...")
    results = {
        'config': asdict(cfg),
        'single_best_accuracy': float(single_best_acc),
        'ensemble_accuracy': float(ensemble_acc),
        'routing_accuracy': float(routing_acc),
        'routing_improvement_vs_best': float(routing_acc - single_best_acc),
        'routing_improvement_vs_ensemble': float(routing_acc - ensemble_acc),
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
    parser.add_argument('--n-experts', type=int, default=5)
    parser.add_argument('--n-states', type=int, default=8)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--expert-epochs', type=int, default=30)
    parser.add_argument('--router-epochs', type=int, default=20)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--output-dir', default='./results/routing')
    args = parser.parse_args()

    cfg = RoutingConfig(
        dataset=args.dataset,
        data_root=args.data_root,
        n_experts=args.n_experts,
        n_states=args.n_states,
        batch_size=args.batch_size,
        expert_epochs=args.expert_epochs,
        router_epochs=args.router_epochs,
        lr=args.lr,
        output_dir=args.output_dir,
    )
    run_routing(cfg)
