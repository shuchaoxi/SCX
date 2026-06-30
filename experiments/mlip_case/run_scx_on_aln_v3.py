"""Run SCX analysis on AlN v3 training data with real DFT labels."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
import numpy as np
from ase.io import read
from collections import Counter
from scx.state import StateDiscovery
from scx.valuation import LearnabilityScore, NoiseScore, RedundancyScore, DataClassifier, StateValue
from scx.encoders.mlip import MLIPEncoder

# ── Load data ──
path = 'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces/AlN_ModelB_v3_rich_physics/extracted_labels_successful/labels_bulk_core.extxyz'
frames = read(path, index=':')
print(f'{"="*60}')
print(f'SCX Analysis: AlN v3 Training Data')
print(f'{"="*60}')
print(f'Frames: {len(frames)}')

# ── Extract features ──
encoder = MLIPEncoder()
features = np.stack([encoder.encode(f) for f in frames])
print(f'Feature dim: {features.shape[1]}')

# ── State discovery ──
discovery = StateDiscovery(method='kmeans', n_states=20)
labels = discovery.fit_predict(features)
centroids = discovery.get_centroids()
state_counts = Counter(labels)
print(f'\nState distribution (K=10):')
for s in sorted(state_counts):
    print(f'  State {s}: {state_counts[s]:4d} frames ({state_counts[s]/len(frames)*100:.1f}%)')

# ── Compute residuals (proxy: force max per frame) ──
fmax = np.array([np.linalg.norm(f.get_forces(), axis=1).max() for f in frames])

# ── Per-state analysis ──
print(f'\n{"="*60}')
print(f'Per-State Analysis')
print(f'{"="*60}')
print(f'{"State":>6} {"n":>5} {"fmax_mean":>10} {"fmax_max":>10} {"consistency":>12} {"noise_risk":>10} {"redundancy":>10} {"class":>15}')
print(f'{"-"*80}')

ls = LearnabilityScore()
ns = NoiseScore()
rs = RedundancyScore()
classifier = DataClassifier()

results = []
for s in sorted(state_counts):
    mask = labels == s
    X_s = features[mask]
    fmax_s = fmax[mask]
    n_s = len(fmax_s)
    prop = n_s / len(frames)

    r_bar = fmax_s.mean()
    # Consistency: use force variance within state (1 - normalized std)
    force_std = np.std(fmax_s) / (np.mean(fmax_s) + 1e-8)
    consistency = 1.0 / (1.0 + force_std)  # higher variance → lower consistency
    noise = ns.compute_state_level(r_bar, prop, consistency)
    similarity = rs.state_similarity(X_s)
    boundary = rs.boundary_score(X_s, centroids, s)
    redundancy = rs.redundancy(prop, r_bar, similarity, boundary)

    # Expert gap proxy: variance of fmax within state
    expert_gap = np.std(fmax_s) / (np.mean(fmax_s) + 1e-8)

    state_class = classifier.classify_state(
        r_bar, prop, consistency, redundancy, noise, expert_gap
    )
    action = classifier.recommend_action(state_class)

    results.append({
        'state': s, 'n': n_s, 'fmax_mean': r_bar, 'fmax_max': fmax_s.max(),
        'consistency': consistency, 'noise': noise, 'redundancy': redundancy,
        'class': state_class, 'action': action
    })

    print(f'{s:>6} {n_s:>5} {r_bar:>10.4f} {fmax_s.max():>10.4f} {consistency:>12.4f} {noise:>10.4f} {redundancy:>10.4f} {state_class:>15}')

# ── Summary ──
print(f'\n{"="*60}')
print(f'Data Classification Summary')
print(f'{"="*60}')
class_counts = Counter(r['class'] for r in results)
total_frames_classified = 0
for c in ['valuable', 'redundant', 'noisy', 'expert_dependent']:
    n_states = class_counts.get(c, 0)
    n_frames = sum(r['n'] for r in results if r['class'] == c)
    total_frames_classified += n_frames
    action = classifier.recommend_action(c)
    print(f'  {c:>20}: {n_states} states, {n_frames} frames ({n_frames/len(frames)*100:.1f}%) → {action}')

# ── Compression estimate ──
redundant_frames = sum(r['n'] for r in results if r['class'] == 'redundant')
noisy_frames = sum(r['n'] for r in results if r['class'] == 'noisy')
valuable_frames = sum(r['n'] for r in results if r['class'] == 'valuable')
print(f'\nCompression potential:')
print(f'  Keep (valuable+expert): {valuable_frames} frames ({valuable_frames/len(frames)*100:.1f}%)')
print(f'  Compress (redundant):   {redundant_frames} frames ({redundant_frames/len(frames)*100:.1f}%)')
print(f'  Review (noisy):         {noisy_frames} frames ({noisy_frames/len(frames)*100:.1f}%)')
print(f'  Estimated savings:      {redundant_frames} frames could be compressed')
print(f'  Keep ratio:             {valuable_frames/len(frames)*100:.1f}%')

# ── Top noisy frames ──
print(f'\n{"="*60}')
print(f'Top 10 Potential Noisy Frames')
print(f'{"="*60}')
noise_scores = np.array([ns.compute(np.array([fm]), prop, 0.5)[0]
    if prop > 0 else 0 for fm, prop in zip(fmax, [state_counts[l]/len(frames) for l in labels])])
top_noisy = np.argsort(noise_scores)[-10:][::-1]
for i, idx in enumerate(top_noisy):
    f = frames[idx]
    sid = f.info.get('structure_id', '?')
    batch = f.info.get('batch', '?')
    print(f'  #{i+1}: {sid} | batch={batch} | fmax={fmax[idx]:.4f} | noise_score={noise_scores[idx]:.4f}')

print(f'\nDone.')
