"""
SCX Two-Layer State Discovery on AlN v3 Training Data.

Re-analyzes AlN v3 with:
  Layer 1: MLIPEncoder (12-dim) coarse clustering
  Layer 2: ErrorDrivenEncoder — refines in error-correlated subspace

Compared to old single-layer approach:
  - Old: 12-dim KMeans → 50% frames in one state, 93.8% expert_dependent
  - New: Layer 1 coarse cluster → Layer 2 error-driven refine → finer states

Usage:
  python experiments/mlip_case/run_scx_two_layer.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

import numpy as np
from ase.io import read
from collections import Counter, defaultdict

from scx.state import StateDiscovery, TwoLayerStateDiscovery
from scx.valuation import (
    LearnabilityScore, NoiseScore, RedundancyScore,
    DataClassifier, StateValue, AdaptiveThreshold
)
from scx.encoders.mlip import MLIPEncoder
from scx.encoders.error_driven import ErrorDrivenEncoder

# =====================================================================
# 0.  Configuration
# =====================================================================
DATA_PATH = (
    'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/extracted_labels_successful/labels_bulk_core.extxyz'
)

# Ground truth noise: fmax > 5 eV/A (same as v3 training downweight threshold)
NOISE_FMAX_THRESHOLD = 5.0

# Number of layer-1 states (matching old experiment)
K_LAYER1 = 20

# Number of layer-2 error states per coarse cluster
K_LAYER2 = 15

# Number of runs for statistical comparison
N_RUNS = 5

# =====================================================================
# 1.  Load data
# =====================================================================
print("=" * 70)
print("SCX TWO-LAYER ANALYSIS: AlN v3 Training Data")
print("=" * 70)

frames = read(DATA_PATH, index=':')
print(f"\nTotal frames loaded: {len(frames)}")

# Extract metadata
batch_of = np.array([f.info.get('batch', 'unknown') for f in frames])
structure_id_of = np.array([f.info.get('structure_id', '?') for f in frames])

# Force max per frame (our error proxy)
fmax = np.array([np.linalg.norm(f.get_forces(), axis=1).max() for f in frames])
print(f"fmax range:  {fmax.min():.4f} – {fmax.max():.4f} eV/A")
print(f"fmax mean:   {fmax.mean():.4f}  median: {np.median(fmax):.4f}")
print(f"fmax > 5:    {(fmax > NOISE_FMAX_THRESHOLD).sum()} frames (noise candidates)")

# Noise ground truth
y_noise = (fmax > NOISE_FMAX_THRESHOLD).astype(int)

# Batch distribution
batch_counts = Counter(batch_of)
print(f"\nBatch distribution ({len(batch_counts)} batches):")
for b, c in sorted(batch_counts.items()):
    n_noise = sum(1 for i in range(len(frames)) if batch_of[i] == b and fmax[i] > NOISE_FMAX_THRESHOLD)
    print(f"  {b}: {c:4d} frames ({n_noise:3d} noise)")


# =====================================================================
# 2.  Encode all frames with Layer-1 encoder (12-dim MLIP)
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 2: Encode with MLIPEncoder (12-dim)")
print(f"{'=' * 70}")

encoder = MLIPEncoder()
features = np.stack([encoder.encode(f) for f in frames])
print(f"Feature matrix shape: {features.shape}")

# =====================================================================
# 3.  Pure Layer 1 analysis (replicate old approach)
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 3: Pure Layer-1 Clustering (old single-layer approach)")
print(f"{'=' * 70}")

l1_discovery = StateDiscovery(method='kmeans', n_states=K_LAYER1, random_state=42)
l1_labels = l1_discovery.fit_predict(features)
l1_centroids = l1_discovery.get_centroids()

l1_state_counts = Counter(l1_labels)
print(f"\nLayer-1 state distribution (K={K_LAYER1}):")
for s in sorted(l1_state_counts):
    n = l1_state_counts[s]
    noise_in_state = (fmax[l1_labels == s] > NOISE_FMAX_THRESHOLD).sum()
    print(f"  State {s:>2}: {n:>4d} frames ({n / len(frames) * 100:>5.1f}%), "
          f"fmax_mean={fmax[l1_labels == s].mean():.3f}, noise={noise_in_state}")


# =====================================================================
# 4.  Layer 2: ErrorDrivenEncoder
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 4: Error-Driven State Discovery (Layer 2)")
print(f"{'=' * 70}")

# Instantiate ErrorDrivenEncoder
error_encoder = ErrorDrivenEncoder(
    layer1_encoder=encoder,
    n_error_states=K_LAYER2,
    feature_selection='mutual_info',   # select dims correlated with error
    selected_dims_ratio=1.0 / 3.0,
)

# Discover error-driven states
error_states = error_encoder.fit_error_states(
    frames,
    residuals=fmax,
    layer1_labels=l1_labels
)

# Print error-driven state summary
print(f"\nError-driven states discovered: {len(error_states)}")
error_summary = error_encoder.summary()
print(f"Mean error (fmax) distribution: {error_summary['mean_error_mean']:.4f} +/- {error_summary['mean_error_std']:.4f}")
print(f"Selected error-correlated dims: {error_summary['top_error_dims']}")
print(f"High-error states: {error_summary['n_high_error_states']} (IDs: {error_summary['high_error_state_ids']})")

# Per error state
print(f"\nPer error-state detail:")
all_sorted = sorted(error_states.items(), key=lambda x: x[1]['mean_error'], reverse=True)
for sid, sdata in all_sorted:
    print(f"  ErrorState {sid:>2}: n={sdata['n_samples']:>4d}, "
          f"mean_fmax={sdata['mean_error']:.4f}, "
          f"desc=[{sdata['description']}]")


# =====================================================================
# 5.  Complete Two-Layer Pipeline
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 5: Full TwoLayerStateDiscovery")
print(f"{'=' * 70}")

two_layer = TwoLayerStateDiscovery(
    layer1_encoder=encoder,
    error_encoder=error_encoder
)

result = two_layer.discover(
    frames,
    residuals=fmax,
    layer1_k=K_LAYER1,
    layer2_k=K_LAYER2,
    use_layer1_clusters=True,
    method='kmeans',
    random_state=42,
)

l2_labels = result['layer2_labels']
n_unique_l2 = len(np.unique(l2_labels))
print(f"\nTwo-layer states: {n_unique_l2} (Layer 1: {K_LAYER1}, combined)")
l2_state_counts = Counter(l2_labels)
print(f"Distribution:")
for s in sorted(l2_state_counts):
    n = l2_state_counts[s]
    mask = l2_labels == s
    noise_in_state = (fmax[mask] > NOISE_FMAX_THRESHOLD).sum()
    batch_in_state = Counter(batch_of[mask])
    top_batch = batch_in_state.most_common(3)
    print(f"  State {s:>3}: {n:>4d} frames ({n / len(frames) * 100:>5.1f}%), "
          f"fmax_mean={fmax[mask].mean():.3f}, noise={noise_in_state}, "
          f"batches={[b for b, _ in top_batch]}")


# =====================================================================
# 6.  Comparison: Layer 1 vs Two-Layer
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 6: Layer 1 vs Two-Layer Comparison")
print(f"{'=' * 70}")

# 6a. Error spread
def compute_state_error_spread(labels, residuals):
    """Compute per-state error statistics."""
    states = {}
    for s in np.unique(labels):
        mask = labels == s
        n = mask.sum()
        r = residuals[mask]
        states[int(s)] = {
            'n': n,
            'mean': float(r.mean()),
            'std': float(r.std()),
            'max': float(r.max()),
            'min': float(r.min()),
            'noise_count': int((r > NOISE_FMAX_THRESHOLD).sum()),
            'noise_frac': float((r > NOISE_FMAX_THRESHOLD).mean()),
        }
    return states

l1_state_errors = compute_state_error_spread(l1_labels, fmax)
l2_state_errors = compute_state_error_spread(l2_labels, fmax)

# Compute overall metrics
l1_mean_errors = np.array([s['mean'] for s in l1_state_errors.values()])
l2_mean_errors = np.array([s['mean'] for s in l2_state_errors.values()])
l1_std_errors = np.array([s['std'] for s in l1_state_errors.values()])
l2_std_errors = np.array([s['std'] for s in l2_state_errors.values()])

print("\n--- Error Spread ---")
print(f"{'Metric':>30} {'Layer 1':>12} {'Two-Layer':>12} {'Improvement':>12}")
print("-" * 70)

l1_spread = float(np.std(l1_mean_errors))
l2_spread = float(np.std(l2_mean_errors))
print(f"{'Std of state mean errors':>30} {l1_spread:>12.4f} {l2_spread:>12.4f} "
      f"{(l2_spread / max(l1_spread, 1e-12)):>12.4f}x")

l1_mmr = float(max(l1_mean_errors) / max(min(l1_mean_errors), 1e-12))
l2_mmr = float(max(l2_mean_errors) / max(min(l2_mean_errors), 1e-12))
print(f"{'Max/min mean error ratio':>30} {l1_mmr:>12.2f} {l2_mmr:>12.2f} "
      f"{(l2_mmr / max(l1_mmr, 1e-12)):>12.2f}x")

l1_within_std = float(np.mean(l1_std_errors))
l2_within_std = float(np.mean(l2_std_errors))
print(f"{'Mean within-state fmax std':>30} {l1_within_std:>12.4f} {l2_within_std:>12.4f} "
      f"{(l2_within_std / max(l1_within_std, 1e-12)):>12.4f}x")

# Count how many states have fmax > 5 (noise states)
l1_noise_states = sum(1 for s in l1_state_errors.values() if s['noise_count'] > 0)
l2_noise_states = sum(1 for s in l2_state_errors.values() if s['noise_count'] > 0)
print(f"{'States containing noise frames':>30} {l1_noise_states:>12d} {l2_noise_states:>12d}")


# 6b. State-level metrics: Learnability, Noise, Redundancy, Classification
print(f"\n--- Classification with Adaptive Thresholds ---")

# Use AdaptiveThreshold to get MLIP-calibrated thresholds
at = AdaptiveThreshold(target_metric='f1')
auto_thresholds = at.auto_threshold(
    features,
    {s: {'mean_residual': d['mean'], 'proportion': d['n'] / len(frames)}
     for s, d in l1_state_errors.items()},
    method='percentile'
)
print(f"Adaptive thresholds (percentile): {auto_thresholds}")

# Create MLIP-specific classifier
mlip_classifier = DataClassifier(config=auto_thresholds)

classifier = DataClassifier(config=auto_thresholds)
ls = LearnabilityScore()
ns = NoiseScore()
rs = RedundancyScore()

# --- Layer 1 classification ---
print(f"\n--- Layer 1 Classification (K={len(l1_state_errors)}) ---")
l1_results = []
for s in sorted(l1_state_errors):
    sd = l1_state_errors[s]
    prop = sd['n'] / len(frames)
    consistency = 1.0 / (1.0 + sd['std'] / max(sd['mean'], 1e-8))

    r_bar = sd['mean']
    noise = ns.compute_state_level(r_bar, prop, consistency)
    sim = rs.state_similarity(features[l1_labels == s])
    # boundary score: not meaningful for single layer, use fixed value
    redundancy = rs.redundancy(prop, r_bar, sim, 0.5)
    expert_gap = sd['std'] / max(sd['mean'], 1e-8)

    cat = classifier.classify_state(r_bar, prop, consistency, redundancy, noise, expert_gap)
    action = classifier.recommend_action(cat)
    l1_results.append({'state': s, 'n': sd['n'], 'fmax_mean': r_bar,
                       'fmax_max': sd['max'], 'consistency': consistency,
                       'noise': noise, 'redundancy': redundancy,
                       'class': cat, 'action': action})
    print(f"  S{s:>2}: n={sd['n']:>4d} fmax={r_bar:.3f} cons={consistency:.3f} "
          f"noise={noise:.3f} red={redundancy:.3f} → {cat}")

# --- Layer 2 (Two-Layer) classification ---
print(f"\n--- Two-Layer Classification (K={len(l2_state_errors)}) ---")
l2_results = []
for s in sorted(l2_state_errors):
    sd = l2_state_errors[s]
    prop = sd['n'] / len(frames)
    consistency = 1.0 / (1.0 + sd['std'] / max(sd['mean'], 1e-8))

    r_bar = sd['mean']
    noise = ns.compute_state_level(r_bar, prop, consistency)
    sim = rs.state_similarity(features[l2_labels == s])
    redundancy = rs.redundancy(prop, r_bar, sim, 0.5)

    cat = classifier.classify_state(r_bar, prop, consistency, redundancy, noise)
    action = classifier.recommend_action(cat)
    l2_results.append({'state': s, 'n': sd['n'], 'fmax_mean': r_bar,
                       'fmax_max': sd['max'], 'consistency': consistency,
                       'noise': noise, 'redundancy': redundancy,
                       'class': cat, 'action': action})
    print(f"  S{s:>3}: n={sd['n']:>4d} fmax={r_bar:.3f} cons={consistency:.3f} "
          f"noise={noise:.3f} red={redundancy:.3f} → {cat}")


# 6c. Classification summary
def summarize_classification(results, total_frames):
    """Aggregate classification counts."""
    class_counts = Counter(r['class'] for r in results)
    summary = {}
    for c in ['valuable', 'redundant', 'noisy', 'expert_dependent']:
        n_states = class_counts.get(c, 0)
        n_frames = sum(r['n'] for r in results if r['class'] == c)
        pct = n_frames / total_frames * 100
        summary[c] = {'n_states': n_states, 'n_frames': n_frames, 'pct': pct}
    return summary

l1_summary = summarize_classification(l1_results, len(frames))
l2_summary = summarize_classification(l2_results, len(frames))

print(f"\n{'=' * 70}")
print("CLASSIFICATION SUMMARY: Layer 1 vs Two-Layer")
print(f"{'=' * 70}")
print(f"{'Category':>20} {'Layer 1':>25} {'Two-Layer':>25}")
print("-" * 70)
for c in ['valuable', 'redundant', 'noisy', 'expert_dependent']:
    l1 = l1_summary[c]
    l2 = l2_summary[c]
    print(f"{c:>20}: "
          f"L1: {l1['n_states']} states, {l1['n_frames']} frames ({l1['pct']:.1f}%) | "
          f"L2: {l2['n_states']} states, {l2['n_frames']} frames ({l2['pct']:.1f}%)")


# =====================================================================
# 7.  Noise Detection Performance (fmax > 5 as ground truth)
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 7: Noise Detection Performance")
print(f"{'=' * 70}")

def compute_noise_detection_metrics(state_ids, labels, y_true, state_errors):
    """Compute precision/recall/F1 for noise frame detection.

    Strategy: a state is flagged "noisy" if its mean fmax > threshold
    or if classifier labeled it as noisy.
    """
    # Method 1: Flag frames in states classified as 'noisy' by SCX
    predicted_noisy = np.zeros(len(y_true), dtype=int)
    for r in state_ids:
        if r['class'] == 'noisy':
            mask = labels == r['state']
            predicted_noisy[mask] = 1

    # Method 2: Flag frames with fmax > threshold directly
    predicted_by_fmax = (fmax > NOISE_FMAX_THRESHOLD).astype(int)

    # Metrics for SCX-based detection
    tp = ((predicted_noisy == 1) & (y_true == 1)).sum()
    fp = ((predicted_noisy == 1) & (y_true == 0)).sum()
    fn = ((predicted_noisy == 0) & (y_true == 1)).sum()
    tn = ((predicted_noisy == 0) & (y_true == 0)).sum()

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    specificity = tn / max(tn + fp, 1)

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'specificity': specificity,
        'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
    }

l1_noise_metrics = compute_noise_detection_metrics(l1_results, l1_labels, y_noise, l1_state_errors)
l2_noise_metrics = compute_noise_detection_metrics(l2_results, l2_labels, y_noise, l2_state_errors)

print(f"\nNoise Detection (fmax > {NOISE_FMAX_THRESHOLD} eV/A, ground truth: {(y_noise == 1).sum()} noise frames)")
print(f"{'Metric':>20} {'Layer 1':>12} {'Two-Layer':>12} {'Improvement':>12}")
print("-" * 65)
for metric in ['precision', 'recall', 'f1', 'specificity']:
    v1 = l1_noise_metrics[metric]
    v2 = l2_noise_metrics[metric]
    impr = v2 - v1
    arrow = "↑" if impr > 0 else ("↓" if impr < 0 else "→")
    print(f"{metric:>20} {v1:>10.4f}  {v2:>10.4f}  {arrow} {impr:>+.4f}")

print(f"\nConfusion matrices:")
print(f"  Layer 1:    TP={l1_noise_metrics['tp']:>3d} FP={l1_noise_metrics['fp']:>3d} "
      f"FN={l1_noise_metrics['fn']:>3d} TN={l1_noise_metrics['tn']:>3d}")
print(f"  Two-Layer:  TP={l2_noise_metrics['tp']:>3d} FP={l2_noise_metrics['fp']:>3d} "
      f"FN={l2_noise_metrics['fn']:>3d} TN={l2_noise_metrics['tn']:>3d}")


# =====================================================================
# 8.  Redundancy & Compression Analysis
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 8: Redundancy & Compression Analysis")
print(f"{'=' * 70}")

# Compute per-batch redundancy scores
print(f"\n--- Per-Batch Redundancy Analysis ---")
batch_redundancy = {}
for batch_name in sorted(batch_counts):
    mask = batch_of == batch_name
    n = mask.sum()
    if n < 3:
        continue
    b_fmax = fmax[mask]
    b_features = features[mask]
    b_labels_l2 = l2_labels[mask]

    # How many unique states cover this batch's frames?
    unique_states = len(np.unique(b_labels_l2))
    # How many frames per state on average?
    state_density = n / max(unique_states, 1)
    # Mean fmax
    b_fmax_mean = float(b_fmax.mean())
    # Is this batch mostly low-error?
    is_low_error = b_fmax_mean < np.percentile(fmax, 25)

    # State similarity: high similarity within batch → more redundancy
    sim = rs.state_similarity(b_features)

    batch_redundancy[batch_name] = {
        'n': n, 'unique_states': unique_states,
        'frames_per_state': state_density,
        'mean_fmax': b_fmax_mean,
        'similarity': sim,
        'redundant_candidate': is_low_error and sim > 0.7,
    }
    print(f"  {batch_name[:30]:>30s}: n={n:>3d} states={unique_states:>2d} "
          f"f/state={state_density:>5.1f} sim={sim:.3f} "
          f"{'REDUNDANT' if batch_redundancy[batch_name]['redundant_candidate'] else ''}")

# Compression estimate
print(f"\n--- Compression Estimate ---")
l2_redundant_frames = sum(r['n'] for r in l2_results if r['class'] == 'redundant')
l2_noisy_frames = sum(r['n'] for r in l2_results if r['class'] == 'noisy')
l2_valuable_frames = sum(r['n'] for r in l2_results if r['class'] == 'valuable')
l2_expert_frames = sum(r['n'] for r in l2_results if r['class'] == 'expert_dependent')

l1_redundant_frames = sum(r['n'] for r in l1_results if r['class'] == 'redundant')
l1_noisy_frames = sum(r['n'] for r in l1_results if r['class'] == 'noisy')
l1_valuable_frames = sum(r['n'] for r in l1_results if r['class'] == 'valuable')

print(f"\n{'Component':>25} {'Layer 1':>15} {'Two-Layer':>15}")
print("-" * 55)
print(f"{'Keep (valuable+expert)':>25} {l1_valuable_frames:>10d} ({l1_valuable_frames/len(frames)*100:>4.1f}%)  "
      f"{l2_valuable_frames + l2_expert_frames:>10d} ({(l2_valuable_frames + l2_expert_frames)/len(frames)*100:>4.1f}%)")
print(f"{'Compress (redundant)':>25} {l1_redundant_frames:>10d} ({l1_redundant_frames/len(frames)*100:>4.1f}%)  "
      f"{l2_redundant_frames:>10d} ({l2_redundant_frames/len(frames)*100:>4.1f}%)")
print(f"{'Review (noisy)':>25} {l1_noisy_frames:>10d} ({l1_noisy_frames/len(frames)*100:>4.1f}%)  "
      f"{l2_noisy_frames:>10d} ({l2_noisy_frames/len(frames)*100:>4.1f}%)")
print(f"{'Expert-dependent':>25} {'':>15}  "
      f"{l2_expert_frames:>10d} ({l2_expert_frames/len(frames)*100:>4.1f}%)")

# More realistic compression: low-fmax frames in low-fmax batches
print(f"\n--- Batch-Level Compression Potential ---")
# Identify low-error batches (mean fmax < global median)
global_median_fmax = np.median(fmax)
compressible_batches = [
    b for b, d in batch_redundancy.items()
    if d['mean_fmax'] < global_median_fmax and d['similarity'] > 0.7
]
compressible_frames = sum(d['n'] for b, d in batch_redundancy.items()
                          if b in compressible_batches)
print(f"Batches with mean fmax < median ({global_median_fmax:.2f}) "
      f"and high similarity: {compressible_batches}")
print(f"Total compressible frames (batch-level estimate): {compressible_frames} "
      f"({compressible_frames/len(frames)*100:.1f}%)")


# =====================================================================
# 9.  Per-State Deep Dive (Two-Layer States)
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 9: Per-State Deep Dive (Two-Layer)")
print(f"{'=' * 70}")

print(f"\n{'ID':>4} {'n':>5} {'fmax_mean':>10} {'fmax_std':>9} {'consist':>8} "
      f"{'noise':>8} {'redund':>7} {'class':>15} {'Top Batch(es)':>40}")
print("-" * 110)

for s in sorted(l2_state_errors):
    sd = l2_state_errors[s]
    prop = sd['n'] / len(frames)
    consistency = 1.0 / (1.0 + sd['std'] / max(sd['mean'], 1e-8))
    r_bar = sd['mean']
    noise = ns.compute_state_level(r_bar, prop, consistency)
    sim = rs.state_similarity(features[l2_labels == s])
    redundancy = rs.redundancy(prop, r_bar, sim, 0.5)

    mask = l2_labels == s
    batch_in_state = Counter(batch_of[mask])
    top_batches = ', '.join(f'{b}({c})' for b, c in batch_in_state.most_common(3))
    cat = classifier.classify_state(r_bar, prop, consistency, redundancy, noise)
    print(f"{s:>4} {sd['n']:>5d} {r_bar:>10.4f} {sd['std']:>9.4f} {consistency:>8.4f} "
          f"{noise:>8.4f} {redundancy:>7.4f} {cat:>15} {top_batches[:40]:>40}")


# =====================================================================
# 10.  Top Noisy Frames
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 10: Top Noisy Frames Detection")
print(f"{'=' * 70}")

# Compute per-frame noise scores using the two-layer states
l2_noise_scores = np.zeros(len(frames))
for s in sorted(l2_state_errors):
    sd = l2_state_errors[s]
    mask = l2_labels == s
    prop = sd['n'] / len(frames)
    consistency = 1.0 / (1.0 + sd['std'] / max(sd['mean'], 1e-8))
    l2_noise_scores[mask] = ns.compute(np.array([sd['mean']]), prop, consistency)

top_noisy_idx = np.argsort(l2_noise_scores)[-15:][::-1]
print(f"\nTop 15 High-Noise Frames (Two-Layer):")
print(f"{'#':>2} {'Structure ID':>50} {'Batch':>35} {'fmax':>8} {'L1_State':>9} {'L2_State':>9} {'NoiseScore':>10}")
print("-" * 130)
for i, idx in enumerate(top_noisy_idx):
    sid = structure_id_of[idx]
    b = batch_of[idx]
    l1s = l1_labels[idx]
    l2s = l2_labels[idx]
    print(f"{i+1:>2} {sid[:50]:>50} {b[:35]:>35} {fmax[idx]:>8.4f} {l1s:>9d} {l2s:>9d} {l2_noise_scores[idx]:>10.4f}")


# =====================================================================
# 11.  Summary stats for report
# =====================================================================
print(f"\n{'=' * 70}")
print("SUMMARY STATISTICS FOR REPORT")
print(f"{'=' * 70}")

# How many frames changed classification?
l1_to_cat = {i: c for r in l1_results for i in np.where(l1_labels == r['state'])[0] for c in [r['class']]}
l2_to_cat = {i: c for r in l2_results for i in np.where(l2_labels == r['state'])[0] for c in [r['class']]}

changed = sum(1 for i in range(len(frames)) if l1_to_cat.get(i) != l2_to_cat.get(i))
print(f"Frames that changed classification: {changed} / {len(frames)} ({changed/len(frames)*100:.1f}%)")

# Most improved batch
print(f"\nPer-batch classification change:")
for batch_name in sorted(batch_counts):
    mask = batch_of == batch_name
    l1_cats = [l1_to_cat[i] for i in np.where(mask)[0]]
    l2_cats = [l2_to_cat[i] for i in np.where(mask)[0]]
    l1_noise_count = sum(1 for c in l1_cats if c == 'noisy')
    l2_noise_count = sum(1 for c in l2_cats if c == 'noisy')
    l1_red_count = sum(1 for c in l1_cats if c == 'redundant')
    l2_red_count = sum(1 for c in l2_cats if c == 'redundant')
    changed_b = sum(1 for i in range(2) if False)
    changed_b = sum(1 for c1, c2 in zip(l1_cats, l2_cats) if c1 != c2)
    print(f"  {batch_name[:30]:>30s}: {len(l1_cats):>3d} frames, "
          f"changed={changed_b:>3d}, "
          f"L1_noise={l1_noise_count:>2d}→L2_noise={l2_noise_count:>2d}, "
          f"L1_red={l1_red_count:>2d}→L2_red={l2_red_count:>2d}")

# Error spread comparison from TwoLayerStateDiscovery
comparison = two_layer.compare_with_pure_layer1(
    frames, fmax, layer1_k=K_LAYER1, layer2_k=K_LAYER2
)
print(f"\nStructured comparison (from TwoLayerStateDiscovery):")
print(f"  Layer 1:     n_states={comparison['layer1']['n_states']}, "
      f"error_spread={comparison['layer1']['state_error_spread']:.4f}, "
      f"maxmin_ratio={comparison['layer1']['max_min_error_ratio']:.2f}")
print(f"  Two-Layer:   n_states={comparison['two_layer']['n_states']}, "
      f"error_spread={comparison['two_layer']['state_error_spread']:.4f}, "
      f"maxmin_ratio={comparison['two_layer']['max_min_error_ratio']:.2f}")
print(f"  Improvement: error_spread_ratio={comparison['improvement']['error_spread_ratio']:.4f}, "
      f"high_error_states_resolved={comparison['improvement']['high_error_states_resolved']}")


# =====================================================================
# 12.  Redundancy-focus: EOS and phonon
# =====================================================================
print(f"\n{'=' * 70}")
print("STEP 12: Focus — EOS / Phonon Redundancy")
print(f"{'=' * 70}")

for target_batch in ['01_eos_hydrostatic_static', '04_phonon_displacement_static']:
    mask = batch_of == target_batch
    n = mask.sum()
    if n == 0:
        continue
    print(f"\n{target_batch} ({n} frames):")
    l2_states_in_batch = Counter(l2_labels[mask])
    for s, c in l2_states_in_batch.most_common():
        smask = l2_labels == s
        bmask = mask & smask
        n_overlap = bmask.sum()
        also_in_other_batches = Counter(batch_of[smask & ~mask])
        other_batches_str = ', '.join(f'{b}({c2})' for b, c2 in also_in_other_batches.most_common(3))
        print(f"  L2 State {s:>3}: {c:>3d}/{n:>3d} frames ({c/n*100:>5.1f}%)"
              f"{' — also in: ' + other_batches_str if other_batches_str else ''}")


print(f"\n{'=' * 70}")
print("DONE.")
print(f"{'=' * 70}")
