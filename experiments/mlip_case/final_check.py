"""Final check: verify test-report frames exist in training data, and compare their SCX status."""
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
from scx.valuation import NoiseScore, RedundancyScore, DataClassifier, AdaptiveThreshold

DATA_PATH = ('G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/extracted_labels_successful/labels_bulk_core.extxyz')
K_LAYER1 = 20
K_LAYER2 = 15

frames = read(DATA_PATH, index=":")
batch_of = np.array([f.info.get("batch", "unknown") for f in frames])
structure_id_of = np.array([f.info.get("structure_id", "?") for f in frames])
fmax = np.array([np.linalg.norm(f.get_forces(), axis=1).max() for f in frames])

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

# Load test set
test_path = ('G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/reports/datasets/v3_bulk_core_grouped_test_predicted.pkl.gz')
with gzip.open(test_path, 'rb') as f:
    test_df = pd.read_pickle(f)

# Test structure IDs
test_ids = test_df['structure_id'].tolist()
print(f"Test set has {len(test_ids)} frames")

# REPORT worst-12 frames
report_worst_ids = [
    "AlN_wz_thermal_strained_1500K_r01", "AlN_wz_thermal_1500K_r06",
    "AlN_wz_thermal_strained_1200K_r06", "AlN_wz_thermal_strained_1200K_r10",
    "AlN_wz_thermal_1500K_r03", "AlN_wz_thermal_strained_1500K_r12",
    "AlN_wz_thermal_1200K_r04", "AlN_wz_thermal_strained_1200K_r05",
    "AlN_wz_thermal_0900K_r11", "AlN_wz_thermal_strained_1200K_r02",
    "AlN_wz_thermal_0900K_r02", "AlN_wz_thermal_strained_0900K_r10",
]

# Check: are all report worst frames in the test set?
print("\n--- REPORT worst frames in test set ---")
for sid in report_worst_ids:
    if sid in test_ids:
        row = test_df[test_df['structure_id'] == sid].iloc[0]
        print(f"  {sid}: test force_rmse={row.get('forces_predicted', 'N/A')} ")
    else:
        print(f"  {sid}: NOT IN test set")

# Check: are all report worst frames in the TRAINING data?
print("\n--- REPORT worst frames in TRAINING data ---")
training_ids_set = set(structure_id_of)
for sid in report_worst_ids:
    if sid in training_ids_set:
        idx = list(structure_id_of).index(sid)
        print(f"  {sid}: TRAINING fmax={fmax[idx]:.4f}, l2_state={l2_labels[idx]}")
    else:
        print(f"  {sid}: NOT IN training data")

# Compare: Are these frames in the test set also in training?
train_test_overlap = training_ids_set & set(test_ids)
print(f"\nTrain-Test structure_id overlap: {len(train_test_overlap)} / {len(test_ids)}")

# Actually check the test data more carefully
print("\n--- Test set samples ---")
print(f"Columns: {test_df.columns.tolist()}")
sample = test_df.iloc[0]
print(f"Sample structure_id: {sample['structure_id']}")
print(f"Sample batch: {sample['batch']}")
# Check if struture_ids are identical to training
for sid in test_ids[:5]:
    idx = np.where(structure_id_of == sid)[0]
    if len(idx) > 0:
        print(f"  {sid}: IN BOTH (train fmax={fmax[idx[0]]:.4f})")
    else:
        print(f"  {sid}: TEST ONLY")

# What's the overall picture: Are test frames held out from training?
# The naming convention might differ (e.g., "r01" vs different batch splits)
print(f"\n--- Unique test batches ---")
print(test_df['batch'].value_counts().to_string())
print(f"\n--- Unique train batches ---")
print(Counter(batch_of))

# Test set per-batch fmax distribution
print("\n--- Test set per-batch fmax ---")
for b in test_df['batch'].unique():
    subset = test_df[test_df['batch'] == b]
    print(f"  {b}: n={len(subset)}")

# Check AlN_wz_thermal_strained_1500K_r01 specifically
print("\n--- Detailed check for AlN_wz_thermal_strained_1500K_r01 ---")
# In training
idx_train = np.where(structure_id_of == 'AlN_wz_thermal_strained_1500K_r01')[0]
if len(idx_train) > 0:
    i = idx_train[0]
    print(f"  TRAINING: fmax={fmax[i]:.4f}, L2_state={l2_labels[i]}, batch={batch_of[i]}")
    train_fmax = fmax[i]
# In test
if 'AlN_wz_thermal_strained_1500K_r01' in test_ids:
    row = test_df[test_df['structure_id'] == 'AlN_wz_thermal_strained_1500K_r01'].iloc[0]
    forces_dft = row['forces']
    forces_pred = row['forces_predicted']
    fmax_dft = np.linalg.norm(forces_dft, axis=1).max()
    fmax_err = np.linalg.norm(forces_dft - forces_pred, axis=1).max()
    print(f"  TEST: DFT_fmax={fmax_dft:.4f}, prediction_error_max={fmax_err:.4f}")

# Key analysis: For the test set frames that correspond to training noise frames,
# what is their prediction error?
print("\n--- Correlation: Training fmax vs Test prediction error ---")
results = []
for sid in test_ids:
    idx = np.where(structure_id_of == sid)[0]
    if len(idx) == 0:
        continue
    i = idx[0]
    train_fmax_val = fmax[i]
    row = test_df[test_df['structure_id'] == sid].iloc[0]
    dft_forces = row['forces']
    pred_forces = row['forces_predicted']
    force_err = np.linalg.norm(dft_forces - pred_forces, axis=1).max()
    l2s = l2_labels[i]
    l2_mean = fmax[l2_labels == l2s].mean()
    results.append((sid, train_fmax_val, force_err, l2s, l2_mean, batch_of[i]))

results.sort(key=lambda x: -x[1])  # sort by training fmax desc
print(f"{'Structure ID':<55} {'Train_fmax':>10} {'Test_err_max':>12} {'L2_state':>8} {'L2_mean_fmax':>13} {'Batch':<30}")
print("-" * 135)
for sid, tfm, terr, l2s, l2mean, batch in results[:30]:
    print(f"{sid:<55} {tfm:>10.4f} {terr:>12.4f} {l2s:>8d} {l2mean:>13.4f} {batch:<30}")

print("\nCorrelation coefficient (training fmax vs test error):")
x = np.array([r[1] for r in results])
y = np.array([r[2] for r in results])
corr = np.corrcoef(x, y)[0, 1]
print(f"  r = {corr:.4f}")

print("\nDONE.")
