#!/usr/bin/env python3
"""
Prepare SCX-cleaned training datasets and ACE retraining experiment.

Creates:
  1. SCX-cleaned extxyz files (conservative / moderate / strict)
  2. Training workspace with comparison configs
  3. VASP re-submission list for extreme noise frames
"""
import os, sys, json, shutil
import numpy as np
from ase.io import read, write
from collections import Counter
from pathlib import Path

# ── Paths ──
SRC_EXTXYZ = (
    'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/extracted_labels_successful/labels_bulk_core.extxyz'
)
SRC_SUMMARY = (
    'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/'
    'AlN_ModelB_v3_rich_physics/extracted_labels_successful/summary.csv'
)

OUT_DIR = Path('G:/Xiaogan_Supercomputing_data/SCX/experiments/mlip_case/scx_retrain')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# VASP job paths (for re-submission)
VASP_JOBS_BASE = (
    'W:/simu_data/vasp/EGP/_archived_deprecated/'
    'AlN_ModelB_v3_rich_physics_full'
)

# ── Load data ──
print('=' * 60)
print('SCX-Cleaned Training Data Preparation')
print('=' * 60)

frames = read(SRC_EXTXYZ, index=':')
print(f'\nLoaded {len(frames)} frames from labels_bulk_core.extxyz')

# Compute fmax
fmax = np.array([np.linalg.norm(f.get_forces(), axis=1).max() for f in frames])
batch_of = np.array([f.info.get('batch', 'unknown') for f in frames])
sid_of = np.array([f.info.get('structure_id', '?') for f in frames])

# ── Classification ──
mask_extreme = fmax > 10.0       # 14 frames: non-physical, MUST remove
mask_moderate = (fmax > 5.0) & (fmax <= 10.0)  # 60 frames: downweight
mask_clean = fmax <= 5.0          # 460 frames: keep as-is

n_extreme = mask_extreme.sum()
n_moderate = mask_moderate.sum()
n_clean = mask_clean.sum()

print(f'\nSCX Classification of {len(frames)} frames:')
print(f'  Extreme noise (fmax>10):     {n_extreme:3d} frames — REMOVE')
print(f'  Moderate noise (fmax 5-10):   {n_moderate:3d} frames — DOWNWEIGHT')
print(f'  Clean (fmax<=5):              {n_clean:3d} frames — KEEP')
print(f'  Total:                        {n_extreme+n_moderate+n_clean}')

# ── Per-batch breakdown ──
print(f'\nPer-batch breakdown:')
for batch in sorted(set(batch_of)):
    bm = batch_of == batch
    n_e = (bm & mask_extreme).sum()
    n_m = (bm & mask_moderate).sum()
    n_c = (bm & mask_clean).sum()
    print(f'  {batch}: {bm.sum():3d} total | {n_e:2d} extreme + {n_m:2d} moderate + {n_c:3d} clean')

# ── 1. Create SCX-cleaned extxyz files ──
print(f'\n{"="*60}')
print('Creating SCX-cleaned extxyz files')
print(f'{"="*60}')

# Conservative: remove extreme only
frames_conservative = [f for i, f in enumerate(frames) if not mask_extreme[i]]
path_cons = OUT_DIR / 'labels_scx_conservative.extxyz'
write(str(path_cons), frames_conservative)
print(f'  Conservative (remove 14 extreme): {len(frames_conservative)} frames → {path_cons.name}')

# Moderate: remove extreme, flag moderate for downweight
frames_moderate = [f for i, f in enumerate(frames) if not mask_extreme[i]]
# Add SCX weight info
for i, f in enumerate(frames_moderate):
    orig_idx = [j for j in range(len(frames))
                if frames[j].info.get('structure_id') == f.info.get('structure_id')][0]
    if mask_moderate[orig_idx]:
        weight = 5.0 / fmax[orig_idx]  # same as v3 strategy
        f.info['scx_weight'] = min(weight, 1.0)
    else:
        f.info['scx_weight'] = 1.0
path_mod = OUT_DIR / 'labels_scx_moderate.extxyz'
write(str(path_mod), frames_moderate)
n_downweighted = sum(1 for f in frames_moderate if f.info.get('scx_weight', 1.0) < 1.0)
print(f'  Moderate (remove 14 + downweight {n_downweighted}): {len(frames_moderate)} frames → {path_mod.name}')

# Strict: remove all fmax>5
frames_strict = [f for i, f in enumerate(frames) if mask_clean[i]]
path_strict = OUT_DIR / 'labels_scx_strict.extxyz'
write(str(path_strict), frames_strict)
print(f'  Strict (remove all 74 fmax>5): {len(frames_strict)} frames → {path_strict.name}')

# ── 2. List of frames to remove ──
print(f'\n{"="*60}')
print('Extreme Noise Frames (fmax > 10 eV/A) — for VASP re-submission')
print(f'{"="*60}')

extreme_info = []
for i in np.where(mask_extreme)[0]:
    f = frames[i]
    extreme_info.append({
        'structure_id': sid_of[i],
        'batch': batch_of[i],
        'fmax': fmax[i],
        'natoms': len(f),
        'formula': f.get_chemical_formula(),
    })

# Sort by fmax descending
extreme_info.sort(key=lambda x: x['fmax'], reverse=True)

for j, info in enumerate(extreme_info):
    print(f'  #{j+1}: {info["structure_id"]:50s} | {info["batch"]:20s} | '
          f'fmax={info["fmax"]:.2f} | {info["natoms"]} atoms | {info["formula"]}')

# Save as CSV
import csv
csv_path = OUT_DIR / 'extreme_noise_frames_for_resubmit.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['#', 'structure_id', 'batch', 'fmax_eV_A', 'natoms', 'formula', 'action'])
    writer.writeheader()
    for j, info in enumerate(extreme_info):
        info['#'] = j + 1
        info['fmax_eV_A'] = info.pop('fmax')
        info['action'] = 'Re-submit with constrained perturbation (max_disp < 0.1A, min_dist > 1.5A)'
        writer.writerow(info)
print(f'\n  CSV saved: {csv_path}')

# ── 3. Training comparison manifest ──
print(f'\n{"="*60}')
print('Training Comparison Experiment Design')
print(f'{"="*60}')

manifest = {
    'experiment': 'SCX-ACE retraining comparison',
    'date': '2026-06-26',
    'base_data': 'AlN v3 rich_physics bulk_core (534 DFT frames)',
    'comparisons': [
        {
            'name': 'baseline_full',
            'description': 'Original full dataset (534 frames) — Single ACE baseline',
            'extxyz': 'labels_bulk_core.extxyz',
            'n_frames': 534,
            'expected_force_rmse': '0.045 eV/A',
        },
        {
            'name': 'scx_conservative',
            'description': 'SCX-conservative: remove 14 extreme (fmax>10)',
            'extxyz': str(path_cons),
            'n_frames': len(frames_conservative),
            'expected_force_rmse': '0.038 eV/A (est. -15%)',
        },
        {
            'name': 'scx_moderate',
            'description': 'SCX-moderate: remove 14 extreme + downweight 60 (fmax>5)',
            'extxyz': str(path_mod),
            'n_frames': len(frames_moderate),
            'expected_force_rmse': '0.032 eV/A (est. -29%)',
            'notes': f'{n_downweighted} frames downweighted',
        },
        {
            'name': 'scx_strict',
            'description': 'SCX-strict: remove all 74 fmax>5 frames',
            'extxyz': str(path_strict),
            'n_frames': len(frames_strict),
            'expected_force_rmse': '0.023 eV/A (est. -48%)',
        },
    ],
    'training_config': {
        'preset': 'LINEAR',
        'elements': ['Al', 'N'],
        'lmax': 3, 'n_rad_max': 14, 'n_rad_base': 8,
        'max_order': 3, 'embedding_size': 24,
        'cutoff': 6.0,
        'target_updates': 2000,
        'energy_weight': 1.0, 'force_weight': 50.0, 'stress_weight': 10.0,
        'lr': 0.005, 'batch_size': 8,
    },
    'validation': [
        'Same test set (103 frames) across all comparisons',
        'Per-batch force/energy/stress RMSE',
        'EOS B0, V0 comparison',
        'Elastic constants C11-C66',
        'Phonon force RMSE',
    ],
    'expected_outcome': (
        'SCX cleaning should improve force RMSE on thermal/MLMD batches '
        'without degrading performance on clean batches (EOS/elastic/cross/phonon). '
        'The conservative approach (removing only fmax>10) is the safest first step.'
    ),
}

manifest_path = OUT_DIR / 'training_manifest.json'
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'  Manifest: {manifest_path}')

# ── 4. Summary ──
print(f'\n{"="*60}')
print('SUMMARY')
print(f'{"="*60}')
print(f'  Original:        534 frames (force RMSE ~0.045 eV/A)')
print(f'  SCX Conservative: {len(frames_conservative)} frames (removed {n_extreme} extreme)')
print(f'  SCX Moderate:     {len(frames_moderate)} frames (removed {n_extreme} + downweighted {n_downweighted})')
print(f'  SCX Strict:       {len(frames_strict)} frames (removed {n_extreme+n_moderate} all fmax>5)')
print(f'')
print(f'  Output directory: {OUT_DIR}')
print(f'  Files:')
for f in sorted(OUT_DIR.iterdir()):
    sz = f.stat().st_size
    print(f'    {f.name} ({sz/1024:.0f} KB)' if sz > 1024 else f'    {f.name} ({sz} B)')
print(f'\nNext step: Submit ACE training on each extxyz using the baseline input.yaml config.')
print(f'           Compare force RMSE, elastic constants, and EOS across all 4 conditions.')
