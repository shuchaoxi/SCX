#!/usr/bin/env python
"""Quick SCX-Compress v2: SCX vs Random only, no Coreset."""
import os, sys, json, numpy as np
import torch, torch.nn as nn, torch.optim as optim

_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script_dir, '..', '..', 'src'))
sys.path.insert(0, os.path.join(_script_dir, '..', '..', '..', 'src'))

from scx_health.data_loader import load_medmnist, extract_features
from scx_health.encoder import create_encoder
from scx.state.discovery import StateDiscovery
from scx.action.compress import CompressStrategy
from scx.valuation.redundancy import RedundancyScore

DATA_ROOT = "G:/Xiaogan_Supercomputing_data/SCX/scx-health/data"
OUTPUT_DIR = "G:/Xiaogan_Supercomputing_data/SCX/scx-health/results/compress"
BATCH_SIZE = 128
EPOCHS = 15
N_STATES = 10
SEED = 42
RATES = [0.0, 0.2, 0.3, 0.4, 0.5]

device = 'cpu'
torch.manual_seed(SEED)
np.random.seed(SEED)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total = 0
    for x, y in loader:
        x, y = x.to(device), y.to(device).view(-1)
        optimizer.zero_grad()
        criterion(model(x), y).backward()
        optimizer.step()
        total += 1
    return total

@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = total = 0
    for x, y in loader:
        x, y = x.to(device), y.to(device).view(-1)
        correct += (model(x).argmax(1) == y).sum().item()
        total += y.size(0)
    return correct / total

@torch.no_grad()
def compute_residuals(model, loader, device):
    model.eval()
    all_res = []
    for x, y in loader:
        x, y = x.to(device), y.to(device).view(-1)
        loss = nn.functional.cross_entropy(model(x), y, reduction='none')
        all_res.append(loss.cpu().numpy())
    return np.concatenate(all_res)

def scx_compute_redundancy(features, residuals, n_states=10, seed=42):
    discovery = StateDiscovery(method='kmeans', n_states=n_states, random_state=seed)
    state_labels = discovery.fit_predict(features)
    centroids = discovery.get_centroids()
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
    return scores, state_labels

def scx_compress_indices(scores, state_labels, residuals, rate, n_states=10, seed=42):
    N = len(scores)
    keep = np.zeros(N, dtype=bool)
    rng = np.random.RandomState(seed)
    for s in range(n_states):
        mask = state_labels == s
        idx = np.where(mask)[0]
        n_s = len(idx)
        if n_s <= 1:
            keep[idx] = True
            continue
        n_keep = max(1, int(n_s * (1.0 - rate)))
        res_s = residuals[mask]
        threshold = float(np.percentile(res_s, 80)) if n_s > 1 else 0.0
        is_boundary = res_s >= threshold
        boundary_idx = idx[is_boundary]
        non_boundary_idx = idx[~is_boundary]
        keep[boundary_idx] = True
        remaining = n_keep - int(is_boundary.sum())
        if remaining > 0 and len(non_boundary_idx) > 0:
            nb_scores = scores[non_boundary_idx]
            info = np.clip(1.0 - nb_scores, 0.0, None)
            prob = info / info.sum() if info.sum() > 1e-10 else np.ones(len(non_boundary_idx)) / len(non_boundary_idx)
            chosen = rng.choice(non_boundary_idx, size=min(remaining, len(non_boundary_idx)), replace=False, p=prob)
            keep[chosen] = True
        elif remaining <= 0 and int(is_boundary.sum()) > n_keep:
            b_scores = scores[boundary_idx]
            order = np.argsort(b_scores)
            to_drop = boundary_idx[order[-(int(is_boundary.sum()) - n_keep):]]
            keep[to_drop] = False
    return keep

def random_compress_indices(labels, rate, seed=42):
    rng = np.random.RandomState(seed)
    N = len(labels)
    keep = np.zeros(N, dtype=bool)
    for cls in np.unique(labels):
        cls_idx = np.where(labels == cls)[0]
        n_keep = max(1, int(len(cls_idx) * (1.0 - rate)))
        chosen = rng.choice(cls_idx, n_keep, replace=False)
        keep[chosen] = True
    return keep

print("=== SCX-Compress v2 Quick ===")
print(f"Loading PathMNIST...")
loaders = load_medmnist('pathmnist', root=DATA_ROOT, batch_size=BATCH_SIZE)
train_set = loaders['train'].dataset
val_loader = loaders['val']
test_loader = loaders['test']
print(f"  Train: {len(train_set)}, Val: {len(val_loader.dataset)}, Test: {len(test_loader.dataset)}")

print(f"Training baseline ({EPOCHS} epochs)...")
model = create_encoder('simple_cnn', 3, 9).to(device)
opt = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
criterion = nn.CrossEntropyLoss()
for ep in range(EPOCHS):
    train_epoch(model, loaders['train'], opt, criterion, device)
    if (ep+1) % 5 == 0:
        va = evaluate(model, val_loader, device)
        ta = evaluate(model, loaders['train'], device)
        print(f"  Epoch {ep+1}/{EPOCHS} | Train: {ta:.4f} | Val: {va:.4f}")

baseline_acc = evaluate(model, test_loader, device)
print(f"Baseline test acc: {baseline_acc:.4f}")

print("Extracting features...")
features, labels = extract_features(model, loaders['train'], device)
print(f"Features: {features.shape}")

print("Computing residuals...")
residuals = compute_residuals(model, loaders['train'], device)

print("SCX redundancy scoring...")
scores, state_labels = scx_compute_redundancy(features, residuals, n_states=N_STATES, seed=SEED)

results = {'baseline_accuracy': float(baseline_acc), 'compression_results': []}
for rate in RATES:
    print(f"\nRate {rate*100:.0f}%")
    if rate == 0.0:
        results['compression_results'].append({
            'rate': 0.0, 'n_train_kept': len(train_set),
            'scx_accuracy': float(baseline_acc), 'scx_delta': 0.0,
            'random_accuracy': float(baseline_acc), 'random_delta': 0.0,
        })
        continue

    # SCX
    scx_keep = scx_compress_indices(scores, state_labels, residuals, rate, N_STATES, SEED)
    scx_set = torch.utils.data.Subset(train_set, np.where(scx_keep)[0])
    scx_loader = torch.utils.data.DataLoader(scx_set, BATCH_SIZE, shuffle=True)
    sm = create_encoder('simple_cnn', 3, 9).to(device)
    so = optim.Adam(sm.parameters(), lr=1e-3, weight_decay=1e-4)
    for _ in range(EPOCHS):
        train_epoch(sm, scx_loader, so, criterion, device)
    scx_acc = evaluate(sm, test_loader, device)

    # Random
    rnd_keep = random_compress_indices(labels, rate, SEED)
    rnd_set = torch.utils.data.Subset(train_set, np.where(rnd_keep)[0])
    rnd_loader = torch.utils.data.DataLoader(rnd_set, BATCH_SIZE, shuffle=True)
    rm = create_encoder('simple_cnn', 3, 9).to(device)
    ro = optim.Adam(rm.parameters(), lr=1e-3, weight_decay=1e-4)
    for _ in range(EPOCHS):
        train_epoch(rm, rnd_loader, ro, criterion, device)
    rnd_acc = evaluate(rm, test_loader, device)

    print(f"  SCX: {scx_acc:.4f} (delta={scx_acc-baseline_acc:+.4f})  Random: {rnd_acc:.4f} (delta={rnd_acc-baseline_acc:+.4f})")
    results['compression_results'].append({
        'rate': rate, 'n_train_kept': len(np.where(scx_keep)[0]),
        'scx_accuracy': float(scx_acc), 'scx_delta': float(scx_acc - baseline_acc),
        'random_accuracy': float(rnd_acc), 'random_delta': float(rnd_acc - baseline_acc),
    })

outpath = os.path.join(OUTPUT_DIR, 'compress_results.json')
with open(outpath, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to {outpath}")
