"""
Additional analysis: Understand SCX vs REPORT overlap discrepancy
and compute structure-by-structure fmax for All frames
"""
import sys, os
import numpy as np
import pandas as pd
import gzip
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

from ase.io import read
from collections import Counter
from scx.encoders.mlip import MLIPEncoder
from scx.encoders.error_driven import ErrorDrivenEncoder
from scx.state import StateDiscovery, TwoLayerStateDiscovery
from scx.valuation import NoiseScore

DATA_PATH = ('G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/extracted_labels_successful/labels_bulk_core.extxyz')
K_LAYER1 = 20
K_LAYER2 = 15

frames = read(DATA_PATH, index=":")
batch_of = np.array([f.info.get("batch", "unknown") for f in frames])
structure_id_of = np.array([f.info.get("structure_id", "?") for f in frames])
fmax = np.array([np.linalg.norm(f.get_forces(), axis=1).max() for f in frames])
y_noise = (fmax > 5.0).astype(int)

encoder = MLIPEncoder()
features = np.stack([encoder.encode(f) for f in frames])

l1_discovery = StateDiscovery(method="kmeans", n_states=K_LAYER1, random_state=42)
l1_labels = l1_discovery.fit_predict(features)

error_encoder = ErrorDrivenEncoder(layer1_encoder=encoder, n_error_states=K_LAYER2,
    feature_selection="mutual_info", selected_dims_ratio=1.0/3.0)
error_encoder.fit_error_states(frames, residuals=fmax, layer1_labels=l1_labels)
two_layer = TwoLayerStateDiscovery(layer1_encoder=encoder, error_encoder=error_encoder)
result = two_layer.discover(frames, residuals=fmax, layer1_k=K_LAYER1, layer2_k=K_LAYER2,
                             use_layer1_clusters=True, method="kmeans", random_state=42)
l2_labels = result["layer2_labels"]

ns = NoiseScore()
l2_noise_scores = np.zeros(len(frames))
for s in np.unique(l2_labels):
    mask = l2_labels == s
    fmax_s = fmax[mask]
    prop = mask.sum() / len(frames)
    consistency = 1.0 / (1.0 + fmax_s.std() / max(fmax_s.mean(), 1e-8))
    l2_noise_scores[mask] = ns.compute(np.array([fmax_s.mean()]), prop, consistency)

print("=" * 70)
print("SCX TOP-20 NOISY FRAMES (by noise_score)")
print("=" * 70)
scx_top20 = np.argsort(l2_noise_scores)[-20:][::-1]
print(f"{'Rank':>4} {'Structure ID':<55} {'Batch':<35} {'fmax':>8} {'fmax>5?':>7} {'L2_State':>8} {'NoiseScore':>10}")
print("-" * 130)
for i, idx in enumerate(scx_top20):
    sid = structure_id_of[idx]
    b = batch_of[idx]
    fm = fmax[idx]
    l2s = l2_labels[idx]
    ns_val = l2_noise_scores[idx]
    noisy = "YES" if fm > 5 else "no"
    print(f"{i+1:>4d} {sid:<55} {b:<35} {fm:>8.4f} {noisy:>7} {l2s:>8d} {ns_val:>10.4f}")

print("\n")
print("=" * 70)
print("REPORT WORST-12 vs SCX noise_score comparison")
print("=" * 70)
report_worst_ids = [
    "AlN_wz_thermal_strained_1500K_r01", "AlN_wz_thermal_1500K_r06",
    "AlN_wz_thermal_strained_1200K_r06", "AlN_wz_thermal_strained_1200K_r10",
    "AlN_wz_thermal_1500K_r03", "AlN_wz_thermal_strained_1500K_r12",
    "AlN_wz_thermal_1200K_r04", "AlN_wz_thermal_strained_1200K_r05",
    "AlN_wz_thermal_0900K_r11", "AlN_wz_thermal_strained_1200K_r02",
    "AlN_wz_thermal_0900K_r02", "AlN_wz_thermal_strained_0900K_r10",
]
print(f"{'Structure ID':<55} {'fmax':>8} {'SCX_rank':>9} {'SCX_noise_score':>16} {'L2_state':>8} {'L2_fmax_mean':>14}")
print("-" * 115)
for sid in report_worst_ids:
    idx = np.where(structure_id_of == sid)[0]
    if len(idx) == 0:
        print(f"{sid:<55} NOT FOUND")
        continue
    idx = idx[0]
    rank = np.sum(l2_noise_scores > l2_noise_scores[idx])
    l2s = l2_labels[idx]
    l2_mean = fmax[l2_labels == l2s].mean()
    l2_n = (l2_labels == l2s).sum()
    scx_noise = l2_noise_scores[idx]
    print(f"{sid:<55} {fmax[idx]:>8.4f} {rank:>9d}/{len(frames)} {scx_noise:>16.4f} {l2s:>8d} {l2_mean:>14.4f} (n={l2_n})")

# Detailed: why does REPORT rank frames differently from SCX?
# The key insight is the REPORT ranks by per-frame fmax, while SCX ranks by state-level noise score
print("\n\nEXPLANATION:")
print("  REPORT: Ranks frames by per-frame fmax (force_max_eV_A_atomnorm)")
print("  SCX: Ranks frames by state-level noise score = f(state_mean_fmax, proportion, consistency)")
print()
print("  Frames in the same L2 state get IDENTICAL noise scores")
print("  This is why many REPORT worst frames share SCX ranks 18 or 122")
print("  (They're in the same L2 noisy state)")

# What is the actual fmax distribution of L2 state 7 (the top noise state)?
print("\n\nL2 State 7 (highest fmax mean) - all 35 frames:")
s7_mask = l2_labels == 7
s7_indices = np.where(s7_mask)[0]
s7_sorted = sorted(s7_indices, key=lambda i: -fmax[i])
print(f"{'Structure ID':<55} {'fmax':>8} {'fmax>5?':>7} {'Batch':<35}")
print("-" * 110)
for idx in s7_sorted:
    sid = structure_id_of[idx]
    b = batch_of[idx]
    fm = fmax[idx]
    noisy = "YES" if fm > 5 else "no"
    print(f"{sid:<55} {fm:>8.4f} {noisy:>7} {b:<35}")

# And L2 state 0 (second highest)
print("\n\nL2 State 0 (second highest fmax mean) - all 55 frames:")
s0_mask = l2_labels == 0
s0_indices = np.where(s0_mask)[0]
s0_sorted = sorted(s0_indices, key=lambda i: -fmax[i])
print(f"{'Structure ID':<55} {'fmax':>8} {'fmax>5?':>7} {'Batch':<35}")
print("-" * 110)
for idx in s0_sorted:
    sid = structure_id_of[idx]
    b = batch_of[idx]
    fm = fmax[idx]
    noisy = "YES" if fm > 5 else "no"
    print(f"{sid:<55} {fm:>8.4f} {noisy:>7} {b:<35}")

# Summary table: all L2 states
print("\n\nALL L2 STATES SUMMARY:")
print(f"{'State':>6} {'n':>5} {'fmax_mean':>10} {'fmax_median':>12} {'fmax_std':>9} {'noise_count':>12} {'noise_pct':>10}")
print("-" * 70)
for s in sorted(np.unique(l2_labels)):
    mask = l2_labels == s
    n = mask.sum()
    fm = fmax[mask]
    noise_c = (fm > 5).sum()
    noise_pct = noise_c / n * 100
    print(f"{s:>6d} {n:>5d} {fm.mean():>10.4f} {np.median(fm):>12.4f} {fm.std():>9.4f} {noise_c:>12d} {noise_pct:>9.1f}%")

# Also check: if we use per-frame fmax as SCX signal (not state-level), what's the overlap?
print("\n\nSCORING BY PER-FRAME fmax (Oracle baseline):")
scx_fmax_top12 = np.argsort(fmax)[-12:][::-1]
scx_fmax_top12_ids = set(structure_id_of[i] for i in scx_fmax_top12)
report_ids_set = set(report_worst_ids)
overlap_fmax = scx_fmax_top12_ids & report_ids_set
print(f"  fmax-top-12 vs REPORT worst-12: {len(overlap_fmax)} overlap")
print(f"  {overlap_fmax}")

print("\nDONE.")
