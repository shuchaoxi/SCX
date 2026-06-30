"""
SCX vs DFT: AlN v3 Comparative Analysis
Produces all metrics needed for the comparison report.
"""
import sys, os
import numpy as np
import pandas as pd
import gzip
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

from ase.io import read
from collections import Counter, defaultdict
from scx.encoders.mlip import MLIPEncoder
from scx.encoders.error_driven import ErrorDrivenEncoder
from scx.state import StateDiscovery, TwoLayerStateDiscovery
from scx.valuation import NoiseScore, RedundancyScore, DataClassifier, AdaptiveThreshold

# ============================================================
# 0. Configuration
# ============================================================
DATA_PATH = (
    'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/extracted_labels_successful/labels_bulk_core.extxyz'
)
NOISE_FMAX_THRESHOLD = 5.0
K_LAYER1 = 20
K_LAYER2 = 15

# ============================================================
# 1. Load data & run SCX pipeline
# ============================================================
print("=" * 70)
print("SCX vs DFT COMPARATIVE ANALYSIS: AlN v3")
print("=" * 70)

frames = read(DATA_PATH, index=":")
print(f"\nTotal frames loaded: {len(frames)}")

batch_of = np.array([f.info.get("batch", "unknown") for f in frames])
structure_id_of = np.array([f.info.get("structure_id", "?") for f in frames])
fmax = np.array([np.linalg.norm(f.get_forces(), axis=1).max() for f in frames])
y_noise = (fmax > NOISE_FMAX_THRESHOLD).astype(int)
print(f"fmax range: {fmax.min():.4f} – {fmax.max():.4f} eV/A")
print(f"Noise frames (fmax>5): {y_noise.sum()}")

# Encode
encoder = MLIPEncoder()
features = np.stack([encoder.encode(f) for f in frames])

# Layer 1
l1_discovery = StateDiscovery(method="kmeans", n_states=K_LAYER1, random_state=42)
l1_labels = l1_discovery.fit_predict(features)

# Layer 2
error_encoder = ErrorDrivenEncoder(
    layer1_encoder=encoder, n_error_states=K_LAYER2,
    feature_selection="mutual_info", selected_dims_ratio=1.0/3.0)
error_encoder.fit_error_states(frames, residuals=fmax, layer1_labels=l1_labels)

two_layer = TwoLayerStateDiscovery(layer1_encoder=encoder, error_encoder=error_encoder)
result = two_layer.discover(frames, residuals=fmax, layer1_k=K_LAYER1, layer2_k=K_LAYER2,
                             use_layer1_clusters=True, method="kmeans", random_state=42)
l2_labels = result["layer2_labels"]

# Noise scores
ns = NoiseScore()
rs = RedundancyScore()
l2_noise_scores = np.zeros(len(frames))
for s in np.unique(l2_labels):
    mask = l2_labels == s
    fmax_s = fmax[mask]
    prop = mask.sum() / len(frames)
    consistency = 1.0 / (1.0 + fmax_s.std() / max(fmax_s.mean(), 1e-8))
    l2_noise_scores[mask] = ns.compute(np.array([fmax_s.mean()]), prop, consistency)


# ============================================================
# 2. OVERLAP: SCX detected noise frames vs REPORT worst frames
# ============================================================
print("\n" + "=" * 70)
print("SECTION 2: OVERLAP WITH REPORT WORST FORCE FRAMES")
print("=" * 70)

report_worst_ids = [
    "AlN_wz_thermal_strained_1500K_r01", "AlN_wz_thermal_1500K_r06",
    "AlN_wz_thermal_strained_1200K_r06", "AlN_wz_thermal_strained_1200K_r10",
    "AlN_wz_thermal_1500K_r03", "AlN_wz_thermal_strained_1500K_r12",
    "AlN_wz_thermal_1200K_r04", "AlN_wz_thermal_strained_1200K_r05",
    "AlN_wz_thermal_0900K_r11", "AlN_wz_thermal_strained_1200K_r02",
    "AlN_wz_thermal_0900K_r02", "AlN_wz_thermal_strained_0900K_r10",
]

def precision_recall_intersection(pred_set, gt_set):
    intersect = pred_set & gt_set
    precision = len(intersect) / max(len(pred_set), 1)
    recall = len(intersect) / max(len(gt_set), 1)
    iou = len(intersect) / max(len(pred_set | gt_set), 1)
    return precision, recall, iou, intersect

report_set = set(report_worst_ids)
print(f"\nReport worst frames: {len(report_set)}")

# SCX Top-K vs Report worst frames
print(f"\n{'K':>5} {'Overlap':>8} {'Precision':>12} {'Recall':>10} {'IOU':>8} {'Union frames':>15}")
print("-" * 60)
for k in [5, 8, 10, 12, 15, 20, 30, 50, 74]:
    scx_topk_idx = np.argsort(l2_noise_scores)[-k:][::-1]
    scx_topk_ids = set(structure_id_of[i] for i in scx_topk_idx)
    p, r, iou, overlap = precision_recall_intersection(scx_topk_ids, report_set)
    print(f"{k:>5d} {len(overlap):>8d} {p:>12.4f} {r:>10.4f} {iou:>8.4f} {len(scx_topk_ids | report_set):>15d}")

# Also show all 12 worst frames with their SCX rank
print(f"\nDetailed: Each report worst frame's SCX rank")
for sid in report_worst_ids:
    idx = np.where(structure_id_of == sid)[0]
    if len(idx) == 0:
        print(f"  {sid:50s} NOT IN TRAINING DATA")
        continue
    idx = idx[0]
    rank = np.sum(l2_noise_scores > l2_noise_scores[idx])
    print(f"  {sid:50s} fmax={fmax[idx]:.4f} SCX_rank={rank}/{len(frames)} noise_score={l2_noise_scores[idx]:.4f}")


# ============================================================
# 3. PER-BATCH NOISE DISTRIBUTION
# ============================================================
print("\n" + "=" * 70)
print("SECTION 3: PER-BATCH NOISE DISTRIBUTION")
print("=" * 70)

batches = sorted(np.unique(batch_of))
# Map batch short names
batch_short = {
    "00_equilibrium": "00_eq",
    "01_eos_hydrostatic_static": "01_EOS",
    "02_elastic_strain_static": "02_elastic",
    "03_strain_displacement_cross_static": "03_cross",
    "04_phonon_displacement_static": "04_phonon",
    "05_thermal_snapshot_static": "05_thermal",
    "08_stress10_mlmd_snapshot_static": "08_MLMD",
}

print(f"\n{'Batch':>35} {'Total':>6} {'fmax>5':>7} {'Noise%':>7} {'fmax_mean':>9} {'fmax_med':>9} {'SCX_Top2':>9}")
print("-" * 90)
# SCX L2 top-2 noisy states
l2_state_means = [(s, fmax[l2_labels==s].mean()) for s in np.unique(l2_labels)]
l2_sorted = sorted(l2_state_means, key=lambda x: -x[1])
l2_top2_mask = np.zeros(len(frames), dtype=bool)
for s, _ in l2_sorted[:2]:
    l2_top2_mask[l2_labels == s] = True

for batch_name in batches:
    mask = batch_of == batch_name
    n = mask.sum()
    n_noise = (fmax[mask] > NOISE_FMAX_THRESHOLD).sum()
    pct_noise = n_noise / n * 100
    fm_mean = fmax[mask].mean()
    fm_med = np.median(fmax[mask])
    n_scx = l2_top2_mask[mask].sum()
    print(f"{batch_name:>35s} {n:>6d} {n_noise:>7d} {pct_noise:>6.1f}% {fm_mean:>9.4f} {fm_med:>9.4f} {n_scx:>9d}")

# Noise sources identification
print(f"\nNoise sources: which batches contain fmax>5 frames?")
noise_batches = [b for b in batches if (fmax[batch_of==b] > NOISE_FMAX_THRESHOLD).sum() > 0]
for b in noise_batches:
    mask = batch_of == b
    n_noise = (fmax[mask] > NOISE_FMAX_THRESHOLD).sum()
    noise_ids = [structure_id_of[i] for i in np.where(mask & (fmax > NOISE_FMAX_THRESHOLD))[0]]
    print(f"\n  {b} ({n_noise} noise frames):")
    for sid in noise_ids:
        idx = np.where(structure_id_of == sid)[0][0]
        print(f"    {sid:55s} fmax={fmax[idx]:.2f}")


# ============================================================
# 4. ONE-LAYER vs TWO-LAYER NOISE DETECTION
# ============================================================
print("\n" + "=" * 70)
print("SECTION 4: ONE-LAYER vs TWO-LAYER COMPARISON")
print("=" * 70)

def compute_metrics(y_true, y_pred):
    tp = ((y_pred == 1) & (y_true == 1)).sum()
    fp = ((y_pred == 1) & (y_true == 0)).sum()
    fn = ((y_pred == 0) & (y_true == 1)).sum()
    tn = ((y_pred == 0) & (y_true == 0)).sum()
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    return precision, recall, f1, tp, fp, fn, tn

thresholds = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0]
print(f"\n{'Threshold':>10} {'L1_Prec':>10} {'L1_Rec':>8} {'L1_F1':>8} {'L2_Prec':>10} {'L2_Rec':>8} {'L2_F1':>8} {'F1_gain':>8}")
print("-" * 75)

for th in thresholds:
    l1_pred = np.zeros(len(frames))
    for s in np.unique(l1_labels):
        mask = l1_labels == s
        if fmax[mask].mean() > th:
            l1_pred[mask] = 1
    l1_p, l1_r, l1_f, *_ = compute_metrics(y_noise, l1_pred)

    l2_pred = np.zeros(len(frames))
    for s in np.unique(l2_labels):
        mask = l2_labels == s
        if fmax[mask].mean() > th:
            l2_pred[mask] = 1
    l2_p, l2_r, l2_f, *_ = compute_metrics(y_noise, l2_pred)

    print(f"{th:>10.1f} {l1_p:>10.4f} {l1_r:>8.4f} {l1_f:>8.4f} {l2_p:>10.4f} {l2_r:>8.4f} {l2_f:>8.4f} {l2_f-l1_f:>+8.4f}")

# Top-K capture rate
print(f"\nTop-K high-error state capture rate (ground truth: 74 noise frames)")
print(f"{'K':>5} {'L1_capture':>12} {'L1_rate':>8} {'L2_capture':>12} {'L2_rate':>8} {'gain':>8}")
print("-" * 55)
for k in range(1, 11):
    l1_sorted_states = sorted([(s, fmax[l1_labels==s].mean()) for s in np.unique(l1_labels)], key=lambda x: -x[1])
    l2_sorted_states = sorted([(s, fmax[l2_labels==s].mean()) for s in np.unique(l2_labels)], key=lambda x: -x[1])

    l1_topk = np.zeros(len(frames), dtype=bool)
    for s, _ in l1_sorted_states[:k]:
        l1_topk[l1_labels == s] = True
    l1_cap = (l1_topk & (y_noise == 1)).sum()

    l2_topk = np.zeros(len(frames), dtype=bool)
    for s, _ in l2_sorted_states[:k]:
        l2_topk[l2_labels == s] = True
    l2_cap = (l2_topk & (y_noise == 1)).sum()

    print(f"{k:>5d} {l1_cap:>12d} {l1_cap/74*100:>7.1f}% {l2_cap:>12d} {l2_cap/74*100:>7.1f}% {l2_cap-l1_cap:>+8d}")


# ============================================================
# 5. REDUNDANCY & COMPRESSION ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("SECTION 5: REDUNDANCY & COMPRESSION ANALYSIS")
print("=" * 70)

# Per-batch L2 state purity and fmax
print(f"\nPer-batch SCX state analysis:")
for batch_name in batches:
    mask = batch_of == batch_name
    n = mask.sum()
    l2_in_batch = l2_labels[mask]
    unique_l2 = len(np.unique(l2_in_batch))
    dominant_l2 = Counter(l2_in_batch).most_common(1)[0]
    purity = dominant_l2[1] / n

    # Which L2 states host this batch?
    state_dist = Counter(l2_in_batch).most_common()
    top3_states = [(s, c/n*100) for s, c in state_dist[:3]]
    print(f"  {batch_name[:35]:>35s}: n={n:>3d} L2_states={unique_l2:>2d} "
          f"purity={purity:.3f} top3={top3_states}")

# fmax>5 frames per batch
print(f"\nIf we remove all fmax>5 frames ({y_noise.sum()} total):")
clean_mask = ~(y_noise.astype(bool))
print(f"  Remaining training data: {clean_mask.sum()} frames ({100*clean_mask.sum()/len(frames):.1f}%)")
for batch_name in batches:
    mask = batch_of == batch_name
    n = mask.sum()
    n_noise = (fmax[mask] > NOISE_FMAX_THRESHOLD).sum()
    n_keep = n - n_noise
    print(f"  {batch_name[:35]:>35s}: {n} -> {n_keep} ({100*n_keep/n:.0f}% kept)")

# If we remove SCX L2 top-2 states
print(f"\nIf we remove SCX L2 top-2 noisy states:")
remove_mask = np.zeros(len(frames), dtype=bool)
for s, _ in l2_sorted[:2]:
    remove_mask[l2_labels == s] = True
print(f"  Frames removed: {remove_mask.sum()} ({100*remove_mask.sum()/len(frames):.1f}%)")
print(f"  Noise frames correctly removed: {(remove_mask & (y_noise==1)).sum()} / {y_noise.sum()}")
print(f"  Clean frames wrongly removed: {(remove_mask & (y_noise==0)).sum()}")


# ============================================================
# 6. ESTIMATED RMSE IMPROVEMENT
# ============================================================
print("\n" + "=" * 70)
print("SECTION 6: ESTIMATED RMSE IMPROVEMENT AFTER NOISE REMOVAL")
print("=" * 70)

# Test set metrics from REPORT
from collections import OrderedDict
test_metrics_batch = OrderedDict([
    ("01_eos_hydrostatic_static", {"force_rmse_eV_A": 0.01521, "frames": 6, "atoms": 24}),
    ("02_elastic_strain_static", {"force_rmse_eV_A": 0.01113, "frames": 26, "atoms": 104}),
    ("03_strain_displacement_cross_static", {"force_rmse_eV_A": 0.02901, "frames": 16, "atoms": 512}),
    ("04_phonon_displacement_static", {"force_rmse_eV_A": 0.00793, "frames": 24, "atoms": 768}),
    ("05_thermal_snapshot_static", {"force_rmse_eV_A": 0.07689, "frames": 21, "atoms": 672}),
    ("08_stress10_mlmd_snapshot_static", {"force_rmse_eV_A": 0.03616, "frames": 10, "atoms": 320}),
])

overall_rmse = 0.04513
overall_frames = 103
overall_atoms = 2400

total_atoms = sum(d["atoms"] for d in test_metrics_batch.values())
current_var = sum(d["force_rmse_eV_A"]**2 * d["atoms"] for d in test_metrics_batch.values())
current_rmse = np.sqrt(current_var / total_atoms)
print(f"\nCurrent weighted force RMSE (check): {current_rmse:.5f} eV/A (report: {overall_rmse})")
print(f"Current per-batch force RMSE:")
for b, d in test_metrics_batch.items():
    print(f"  {b:40s}: {d['force_rmse_eV_A']:.5f}")

# 74 noise frames all in thermal+MLMD in training data
# In test set, thermal batch has 3.4x higher RMSE than average
# Assume thermal test RMSE can improve from 0.077 to 0.040 (similar to cross)
# Assume MLMD test RMSE can improve from 0.036 to 0.020 (towards elastic)

scenarios = [
    ("conservative", {"thermal": 0.050, "mlmd": 0.030}),
    ("moderate", {"thermal": 0.040, "mlmd": 0.025}),
    ("aggressive", {"thermal": 0.032, "mlmd": 0.020}),
]

for name, adj in scenarios:
    new_var = sum(
        (d["force_rmse_eV_A"]**2 if b not in ["05_thermal_snapshot_static", "08_stress10_mlmd_snapshot_static"]
         else (adj["thermal"]**2 if "thermal" in b else adj["mlmd"]**2))
        * d["atoms"]
        for b, d in test_metrics_batch.items()
    )
    new_rmse = np.sqrt(new_var / total_atoms)
    print(f"\n{name.capitalize():>15s}: thermal={adj['thermal']:.3f}, MLMD={adj['mlmd']:.3f}")
    print(f"  Projected force RMSE: {new_rmse:.5f} eV/A (improvement: {(overall_rmse-new_rmse)/overall_rmse*100:.1f}%)")

# Energy RMSE estimation
print(f"\nEnergy RMSE estimation (currently {0.0144} eV/atom):")
# Energy RMSE is dominated by EOS batch (0.059)
# Thermal has 0.003 energy RMSE, so noise removal mainly helps force
test_energy_rmse = {
    "01_eos_hydrostatic_static": 0.05917,
    "02_elastic_strain_static": 0.00184,
    "03_strain_displacement_cross_static": 0.00320,
    "04_phonon_displacement_static": 0.00154,
    "05_thermal_snapshot_static": 0.00295,
    "08_stress10_mlmd_snapshot_static": 0.00037,
}
overall_e_rmse = 0.01445
total_atoms_e = 2400
current_e_var = sum(v**2 * test_metrics_batch[b]["atoms"] for b, v in test_energy_rmse.items() for b2, d in test_metrics_batch.items() if b == b2)
print(f"  Energy RMSE per batch:")
for b, v in test_energy_rmse.items():
    print(f"    {b:40s}: {v:.5f} eV/atom")
print(f"  Thermal energy RMSE is already low ({test_energy_rmse['05_thermal_snapshot_static']:.5f}).")
print(f"  Noise removal mainly affects force RMSE, not energy RMSE.")


# ============================================================
# 7. DATA POISONING CHECK
# ============================================================
print("\n" + "=" * 70)
print("SECTION 7: DATA POISONING CHECK")
print("=" * 70)

# Are there frames with suspiciously high force errors that suggest VASP script errors?
# Check: frames with fmax > 10 (extreme)
extreme_mask = fmax > 10.0
print(f"\nFrames with fmax > 10.0 eV/A (possible script error):")
extreme_count = extreme_mask.sum()
if extreme_count > 0:
    for idx in np.where(extreme_mask)[0]:
        print(f"  {structure_id_of[idx]:55s} batch={batch_of[idx]:35s} fmax={fmax[idx]:.2f}")
print(f"Total extreme frames: {extreme_count}")

# Check: frames with fmax > 8
vhigh_mask = fmax > 8.0
print(f"\nFrames with fmax > 8.0 eV/A:")
for idx in np.where(vhigh_mask)[0]:
    print(f"  {structure_id_of[idx]:55s} batch={batch_of[idx]:35s} fmax={fmax[idx]:.2f}")

# Check: are noisy frames concentrated in specific structures?
print(f"\nNoise frames grouped by structure prefix:")
prefixes = [sid.rsplit("_r", 1)[0] if "_r" in sid else sid for sid in structure_id_of]
for batch_name in batches:
    if "thermal" in batch_name or "mlmd" in batch_name:
        mask = batch_of == batch_name
        noise_mask = mask & (fmax > NOISE_FMAX_THRESHOLD)
        batch_noise_ids = [structure_id_of[i] for i in np.where(noise_mask)[0]]
        print(f"\n  {batch_name} ({len(batch_noise_ids)} noise frames):")
        for sid in batch_noise_ids:
            idx = np.where(structure_id_of == sid)[0][0]
            print(f"    {sid} fmax={fmax[idx]:.2f}")


# ============================================================
# 8. EXECUTIVE SUMMARY TABLE
# ============================================================
print("\n" + "=" * 70)
print("EXECUTIVE SUMMARY")
print("=" * 70)

print(f"""
Key Metrics:
  Total training frames: {len(frames)}
  Noise frames (fmax>5): {y_noise.sum()} ({100*y_noise.sum()/len(frames):.1f}%)
  L1 states: {len(np.unique(l1_labels))}
  L2 states: {len(np.unique(l2_labels))}

Overlap Analysis:
  SCX top-12 vs REPORT worst-12 overlap: {len(set(structure_id_of[i] for i in np.argsort(l2_noise_scores)[-12:][::-1]) & set(report_worst_ids))}/12

Best Noise Detection:
  L2 Top-2 capture rate: {(sum(1 for s,_ in l2_sorted[:2] for i in np.where(l2_labels==s)[0] if y_noise[i]==1))}/74
  L2 F1 (th=4.0): ... (see above)

Compression:
  Remove fmax>5: keep {100*(len(frames)-y_noise.sum())/len(frames):.1f}%
  Remove SCX top-2 states: remove {100*remove_mask.sum()/len(frames):.1f}%

RMSE Impact:
  Current: {overall_rmse} eV/A
  Conservative: ...
  Moderate: ...
  Aggressive: ...
""")

print("\nDONE.")
