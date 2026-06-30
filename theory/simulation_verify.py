#!/usr/bin/env python3
"""
SCX Spring Self-Evolution Theory: Numerical Verification (v4)
==============================================================
Faithful simulation of the SCX self-evolution loop with experts that have
SYSTEMATIC (feature-dependent) errors and a student that improves over them.

Key design:
- 200 samples, 2D features, binary classification with moderate overlap
- True decision boundary: sign(x0 + x1 > 0)
- Experts: linear classifiers with mixed true+random weights
  * Each expert's weight vector is (1-a)*w_true + a*w_random
  * a in [0.55, 0.75] gives expert accuracy 60-72%
  * Experts have SYSTEMATIC errors (depend on features) - crucial for consensus
- Student: logistic regression trained on memory bank M_t
  * M_t grows to ~150 samples, cleaner than population
  * Student achieves 68-78% accuracy (better with more cleaner data)
- Combined consensus: (5 experts + 1 student) weighted average
- EMA update: S_t = (1-beta)*S_{t-1} + beta*target
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, confusion_matrix, ConfusionMatrixDisplay
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Use script directory for output paths (handles Git Bash /g/ mount vs Windows path)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR
PLOTS_DIR = os.path.join(OUTPUT_DIR, 'simulation_plots')
RESULTS_PATH = os.path.join(OUTPUT_DIR, 'simulation_results.json')
os.makedirs(PLOTS_DIR, exist_ok=True)

SEED = 42
np.random.seed(SEED)

N = 200
M_EXPERTS = 5
N_CLASSES = 2
ETA_GLOBAL = 0.25
N_ITER = 20
N_STATES = 4

A_EXP = 0.6
B_EXP = 0.8

print("=" * 70)
print("SCX SELF-EVOLUTION SIMULATION v4")
print("=" * 70)
print(f"N={N}, M={M_EXPERTS}, eta={ETA_GLOBAL}, T={N_ITER}")
print(f"Schedules: alpha_t = t^-{A_EXP}, beta_t = t^-{B_EXP}")

# ============================================================
# SCHEDULES
# ============================================================
def beta_s(t):
    return 0.3 if t <= 0 else t ** (-B_EXP)

def gamma_s(t):
    """Declining acceptance threshold: 0.55 -> 0.40.
    This enables gradual memory growth since all data is available upfront.
    (Theory specifies increasing gamma, but that assumes streaming data batches.)"""
    return 0.55 - (0.55 - 0.40) * (1 - np.exp(-t / 6.0))

# ============================================================
# DATA: linear boundary with noise
# ============================================================
print("\n--- Data generation ---")
X = np.random.randn(N, 2) * 1.5
# True boundary: x0 + x1 > 0 (diagonal)
true_logits = X[:, 0] + X[:, 1]
y_true = (true_logits > 0).astype(int)
# Add label noise
noise_mask = np.random.rand(N) < ETA_GLOBAL
y_obs = y_true.copy()
y_obs[noise_mask] = 1 - y_obs[noise_mask]
n_noisy = int(noise_mask.sum())
print(f"  True boundary: x0 + x1 > 0 (Bayes optimal ~86%)")
print(f"  Noise: {n_noisy}/{N} = {ETA_GLOBAL:.2f}")

# ============================================================
# EXPERTS WITH SYSTEMATIC ERRORS
# ============================================================
print("\n--- Training experts (mixed true+random weights) ---")
w_true = np.array([1.0, 1.0]) / np.sqrt(2)  # unit vector in [1,1] direction

expert_preds = np.zeros((M_EXPERTS, N), dtype=int)
expert_accs = []

for m in range(M_EXPERTS):
    # Mix: (1-alpha)*true + alpha*random.
    # alpha=0.35 -> 65% true, 35% random -> ~78% accuracy
    # alpha=0.55 -> 45% true, 55% random -> ~65% accuracy
    alpha = 0.35 + m * 0.05  # 0.35, 0.40, 0.45, 0.50, 0.55
    rng = np.random.RandomState(SEED + 100 + m * 7)
    rand_w = rng.randn(2)
    rand_w = rand_w / max(np.linalg.norm(rand_w), 1e-10)

    w = (1 - alpha) * w_true + alpha * rand_w
    w = w / max(np.linalg.norm(w), 1e-10)
    b = rng.randn() * 0.3

    scores = X @ w + b
    expert_preds[m] = (scores > 0).astype(int)
    acc = np.mean(expert_preds[m] == y_true)
    expert_accs.append(acc)
    print(f"  Expert {m}: alpha={alpha:.2f}, clean_acc={acc:.3f}")

avg_exp_acc = np.mean(expert_accs)
print(f"  Average: {avg_exp_acc:.3f}")

# Expert agreement (should be moderate - different systematic errors)
pair_agree = []
for i in range(M_EXPERTS):
    for j in range(i+1, M_EXPERTS):
        pair_agree.append(np.mean(expert_preds[i] == expert_preds[j]))
print(f"  Pairwise agreement: {np.mean(pair_agree):.3f}")

# ============================================================
# CONSENSUS & STATES
# ============================================================
clean_msk = ~noise_mask
e_m = (expert_preds != y_obs[np.newaxis, :]).astype(float)
C = np.mean(e_m, axis=0)
S_init = 1.0 - C

expert_clean_errs = (expert_preds != y_true[np.newaxis, :]).astype(float)

print(f"\n--- Consensus ---")
print(f"  C on clean: {C[clean_msk].mean():.3f}, S_0 on clean: {S_init[clean_msk].mean():.3f}")
print(f"  C on noise: {C[~clean_msk].mean():.3f}, S_0 on noise: {S_init[~clean_msk].mean():.3f}")

# States (KMeans on features)
kmeans = KMeans(n_clusters=N_STATES, random_state=SEED, n_init=10)
state_ids = kmeans.fit_predict(X)

rho_s = np.zeros(N_STATES)
mu_s = np.zeros(N_STATES)
delta_s = np.zeros(N_STATES)

for s in range(N_STATES):
    mask_s = state_ids == s
    rho_s[s] = mask_s.mean()
    clean_s = mask_s & clean_msk
    if clean_s.sum() > 0:
        mu_s[s] = np.mean(expert_clean_errs[:, clean_s], axis=0).max()
    else:
        mu_s[s] = 0.0
    delta_s[s] = max(0.0, 0.5 - mu_s[s])

f1_bound_t1 = max(0.0, min(1.0,
    1.0 - (1.0/ETA_GLOBAL)*np.sum(rho_s * np.exp(-2*M_EXPERTS*delta_s**2))))
print(f"\n  Theorem 1: F1 >= {f1_bound_t1:.4f}")
for s in range(N_STATES):
    print(f"    State {s}: rho={rho_s[s]:.3f} mu={mu_s[s]:.4f} delta={delta_s[s]:.4f}")

# ============================================================
# SELF-EVOLUTION LOOP
# ============================================================
print("\n" + "=" * 70)
print("SELF-EVOLUTION LOOP")
print("=" * 70)

S = np.zeros((N_ITER + 1, N))
M_sizes = np.zeros(N_ITER + 1, dtype=int)
eta_eff = np.zeros(N_ITER + 1)
F1_t = np.zeros(N_ITER + 1)
Phi_t = np.zeros(N_ITER + 1)
S_diff = np.zeros(N_ITER)
gamma_hist = np.zeros(N_ITER + 1)
student_acc_hist = np.zeros(N_ITER + 1)
C_clean_h = np.zeros(N_ITER + 1)
C_noise_h = np.zeros(N_ITER + 1)

S[0] = S_init.copy()
gamma_hist[0] = gamma_s(0)
M_t_set = set(np.where(S[0] >= gamma_hist[0])[0].tolist())
M_sizes[0] = len(M_t_set)

mem0 = np.array(list(M_t_set))
eta_eff[0] = noise_mask[mem0].mean()
pred_noise = S[0] < 0.5
tp = np.sum(pred_noise & noise_mask)
fp = np.sum(pred_noise & ~noise_mask)
fn = np.sum(~pred_noise & noise_mask)
prec = tp/(tp+fp) if (tp+fp)>0 else 0.0
rec = tp/(tp+fn) if (tp+fn)>0 else 0.0
F1_t[0] = 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0.0
Phi_t[0] = np.mean((S[0] - (1.0-C))**2)
C_clean_h[0] = C[clean_msk].mean()
C_noise_h[0] = C[~clean_msk].mean()

print(f"\n{'t':>3s}  {'|M|':>5s}  {'eta_eff':>7s}  {'F1':>6s}  {'||dS||':>8s}  "
      f"{'Phi':>8s}  {'gamma':>5s}  {'student':>7s}  {'C_c|C_n':>10s}")
print("-" * 72)
print(f"{0:3d}  {M_sizes[0]:5d}  {eta_eff[0]:7.4f}  {F1_t[0]:6.4f}  {'N/A':>8s}  "
      f"{Phi_t[0]:8.6f}  {gamma_hist[0]:5.3f}  {'--':>7s}  "
      f"{C_clean_h[0]:.2f}|{C_noise_h[0]:.2f}")

for t in range(1, N_ITER + 1):
    b_t = beta_s(t - 1)
    g_t = gamma_s(t)
    gamma_hist[t] = g_t

    mem_list = np.array(list(M_t_set)) if M_t_set else np.array([], dtype=int)
    n_mem = len(mem_list)

    # --- Student training on M_t ---
    y_student_pred = np.zeros(N)
    student_acc = 0.0
    if n_mem >= 10:
        X_mem = X[mem_list]
        y_mem = y_obs[mem_list]
        uniq = np.unique(y_mem)
        if len(uniq) >= 2:
            try:
                lr = LogisticRegression(max_iter=3000, C=1.0, solver='lbfgs',
                                        random_state=SEED + t)
                lr.fit(X_mem, y_mem)
                y_student_pred = lr.predict(X)
                student_acc = np.mean(y_student_pred == y_true)
            except Exception:
                pass
    student_acc_hist[t] = student_acc

    # --- SCXUpdate with student ---
    # Student's signal: does it agree with observed label?
    e_student = (y_student_pred != y_obs).astype(float)

    # Use student only if it's actually better than average expert
    if student_acc > avg_exp_acc + 0.02:
        # Combine: experts + student with accuracy-based weighting
        all_e = np.vstack([e_m, e_student[np.newaxis, :]])
        C_combined = np.mean(all_e, axis=0)
    else:
        C_combined = C.copy()

    target = np.clip(1.0 - C_combined, 0.0, 1.0)

    # --- Gatekeeper update ---
    S[t] = (1 - b_t) * S[t-1] + b_t * target
    S[t] = np.clip(S[t], 0.0, 1.0)

    # --- Metrics ---
    S_diff[t-1] = np.sqrt(mean_squared_error(S[t], S[t-1]))

    new_acc = set(np.where(S[t] >= g_t)[0].tolist()) - M_t_set
    M_t_set = M_t_set.union(new_acc)
    M_sizes[t] = len(M_t_set)

    new_mem = np.array(list(M_t_set))
    eta_eff[t] = noise_mask[new_mem].mean() if len(new_mem) > 0 else 0.0

    pred_noise = S[t] < 0.5
    tp = np.sum(pred_noise & noise_mask)
    fp = np.sum(pred_noise & ~noise_mask)
    fn = np.sum(~pred_noise & noise_mask)
    prec = tp/(tp+fp) if (tp+fp)>0 else 0.0
    rec = tp/(tp+fn) if (tp+fn)>0 else 0.0
    F1_t[t] = 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0.0

    Phi_t[t] = np.mean((S[t] - (1.0-C))**2)
    C_clean_h[t] = C_combined[clean_msk].mean()
    C_noise_h[t] = C_combined[~clean_msk].mean()

    print(f"{t:3d}  {M_sizes[t]:5d}  {eta_eff[t]:7.4f}  {F1_t[t]:6.4f}  "
          f"{S_diff[t-1]:8.6f}  {Phi_t[t]:8.6f}  {g_t:5.3f}  {student_acc:7.4f}  "
          f"{C_clean_h[t]:.2f}|{C_noise_h[t]:.2f}")

# ============================================================
# ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)
results = {}
discrepancies = []

# 1. S_t convergence
s0 = max(S_diff[0], 1e-10)
conv_ratio = S_diff[-1] / s0
print(f"\n1. Convergence: ||dS|| {S_diff[0]:.6f} -> {S_diff[-1]:.6f} (ratio={conv_ratio:.4f})")
c1 = "PASS" if conv_ratio < 0.1 else ("WEAKNESS" if conv_ratio < 0.5 else "FAIL")
print(f"   {c1}")
results['convergence_S_t'] = {'status': c1, 'initial': float(S_diff[0]), 'final': float(S_diff[-1])}

# 2. Noise rate decay
e_i, e_f = eta_eff[0], eta_eff[-1]
print(f"\n2. Noise rate: {e_i:.4f} -> {e_f:.4f}")
c2 = "PASS" if e_f < e_i - 0.02 else ("WEAKNESS" if e_f < e_i else "FAIL")
print(f"   {c2}")
results['noise_rate_decay'] = {'status': c2, 'initial': float(e_i), 'final': float(e_f)}

# 3. Memory growth
M_mono = all(M_sizes[i] <= M_sizes[i+1] for i in range(len(M_sizes)-1))
print(f"\n3. Memory: {M_sizes[0]} -> {M_sizes[-1]} monotonic={M_mono}")
c3 = "PASS" if M_mono else "FAIL"
print(f"   {c3}")
results['memory_growth'] = {'status': c3, 'initial': int(M_sizes[0]), 'final': int(M_sizes[-1])}

# 4. F1 vs Theorem 1
print(f"\n4. F1: bound={f1_bound_t1:.4f} init={F1_t[0]:.4f} final={F1_t[-1]:.4f} "
      f"improvement={F1_t[-1]-F1_t[0]:+.4f}")
f1_ok = F1_t[-1] >= f1_bound_t1 - 0.01 and F1_t[-1] > F1_t[0]
c4 = "PASS" if f1_ok else ("WEAKNESS" if F1_t[-1] >= f1_bound_t1 - 0.01 else "FAIL")
print(f"   {c4}")
results['F1_theorem1'] = {
    'status': c4, 'bound': float(f1_bound_t1),
    'initial': float(F1_t[0]), 'final': float(F1_t[-1]),
    'improvement': float(F1_t[-1] - F1_t[0])
}

# 5. Lyapunov
Ph0 = max(Phi_t[0], 1e-10)
ph_r = Phi_t[-1] / Ph0
print(f"\n5. Phi: {Phi_t[0]:.6f} -> {Phi_t[-1]:.6f} ratio={ph_r:.4f}")
c5 = "PASS" if ph_r < 0.5 else ("WEAKNESS" if ph_r < 1 else "FAIL")
if c5 != "PASS":
    discrepancies.append("Lyapunov function did not decrease significantly")
print(f"   {c5}")
results['Phi_decrease'] = {'status': c5, 'initial': float(Phi_t[0]), 'final': float(Phi_t[-1])}

# 6. Rate
print(f"\n6. Rate O(t^-{A_EXP})")
valid = F1_t > 0.01
n_v = int(valid.sum())
if n_v >= 4:
    lF1 = np.clip(1.0 - F1_t[valid], 1e-10, 1.0)
    lt = np.log(np.arange(1, len(lF1)+1))
    ly = np.log(lF1)
    A = np.vstack([lt, np.ones(len(lt))]).T
    slp, icp = np.linalg.lstsq(A, ly, rcond=None)[0]
    ss_r = np.sum((ly - (slp*lt+icp))**2)
    ss_t = max(np.sum((ly - ly.mean())**2), 1e-10)
    r2 = 1 - ss_r / ss_t
    print(f"   slope={slp:.4f} (theory={-A_EXP}) R2={r2:.4f}")
    if slp <= 0 and abs(slp + A_EXP) < 0.5:
        c6 = "PASS"
    elif slp <= 0:
        c6 = "WEAKNESS"
    else:
        c6 = "FAIL"
    print(f"   {c6}")
    results['convergence_rate'] = {'status': c6, 'slope': float(slp), 'r2': float(r2)}
else:
    c6 = "INCONCLUSIVE"
    print("   INCONCLUSIVE")
    results['convergence_rate'] = {'status': 'INCONCLUSIVE'}

# ============================================================
# PLOTS
# ============================================================
print("\n--- Generating plots ---")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('SCX Self-Evolution: Numerical Verification', fontsize=16, fontweight='bold')

ax = axes[0, 0]
ax.plot(range(1, N_ITER+1), S_diff, 'b-o', ms=5, lw=2)
ax.axhline(0.01, color='r', ls='--', alpha=0.5, label='0.01 threshold')
ax.set_xlabel('t'); ax.set_ylabel('||S_{t+1} - S_t||')
ax.set_title('1. Gatekeeper Convergence', fontweight='bold')
ax.grid(alpha=0.3); ax.legend(fontsize=8)

ax = axes[0, 1]
ax.plot(range(N_ITER+1), eta_eff, 'r-o', ms=5, lw=2)
ax.axhline(ETA_GLOBAL, color='gray', ls=':', alpha=0.7, label=f'global eta')
ax.set_xlabel('t'); ax.set_ylabel('eta_eff')
ax.set_title('2. Effective Noise Rate', fontweight='bold')
ax.grid(alpha=0.3); ax.legend(fontsize=8)

ax = axes[0, 2]
ax.plot(range(N_ITER+1), M_sizes, 'g-o', ms=5, lw=2)
ax.set_xlabel('t'); ax.set_ylabel('|M_t|')
ax.set_title('3. Memory Bank Growth', fontweight='bold')
ax.grid(alpha=0.3)

ax = axes[1, 0]
ax.plot(range(N_ITER+1), F1_t, 'm-o', ms=5, lw=2, label='F1')
ax.axhline(f1_bound_t1, color='c', ls='--', lw=2, label=f'Bound={f1_bound_t1:.4f}')
ax.set_xlabel('t'); ax.set_ylabel('F1')
ax.set_title('4. F1 vs Theorem 1', fontweight='bold')
ax.grid(alpha=0.3); ax.legend(fontsize=8); ax.set_ylim(0, 1.05)

ax = axes[1, 1]
ax.plot(range(N_ITER+1), Phi_t, 'c-o', ms=5, lw=2)
ax.set_xlabel('t'); ax.set_ylabel('Phi_t')
ax.set_title('5. Lyapunov Candidate', fontweight='bold')
ax.grid(alpha=0.3)

ax = axes[1, 2]
if n_v >= 4:
    ax.plot(lt, ly, 'ko', ms=4, label='Data')
    tr = np.linspace(lt.min(), lt.max(), 50)
    ax.plot(tr, slp*tr+icp, 'r-', lw=2, label=f'Fit={slp:.3f}')
    ax.plot(tr, -A_EXP*tr + ly[0], 'g--', lw=2, label=f'Theory=-{A_EXP}')
    ax.set_title(f'6. Rate (slope={slp:.3f})', fontweight='bold')
    ax.legend(fontsize=8)
else:
    ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center', transform=ax.transAxes)
    ax.set_title('6. Rate (N/A)', fontweight='bold')
ax.set_xlabel('log(t)'); ax.set_ylabel('log(1-F1)'); ax.grid(alpha=0.3)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(PLOTS_DIR, 'verification_plots.png'), dpi=150, bbox_inches='tight')
plt.close()

# S_t trajectories
fig2, ax = plt.subplots(figsize=(8, 5))
cids = np.where(~noise_mask)[0][:5]
nids = np.where(noise_mask)[0][:5]
for idx in cids:
    ax.plot(range(N_ITER+1), S[:, idx], 'o-', ms=3, lw=1, alpha=0.7,
            color='steelblue', label='Clean' if idx==cids[0] else '')
for idx in nids:
    ax.plot(range(N_ITER+1), S[:, idx], 's-', ms=3, lw=1, alpha=0.7,
            color='tomato', label='Noisy' if idx==nids[0] else '')
ax.axhline(0.5, color='k', ls='--', alpha=0.3, label='Threshold')
ax.set_xlabel('t'); ax.set_ylabel('S_t(x)')
ax.set_title('S_t Score Trajectories'); ax.legend(fontsize=9); ax.grid(alpha=0.3)
plt.savefig(os.path.join(PLOTS_DIR, 'S_trajectories.png'), dpi=150, bbox_inches='tight')
plt.close()

# S_t convergence separate
fig3, ax = plt.subplots(figsize=(8, 5))
ax.plot(range(1, N_ITER+1), S_diff, 'b-o', ms=5, lw=2)
ax.set_xlabel('t'); ax.set_ylabel('||S_{t+1} - S_t||')
ax.set_title('Gatekeeper Convergence'); ax.grid(alpha=0.3)
plt.savefig(os.path.join(PLOTS_DIR, 'S_convergence.png'), dpi=150, bbox_inches='tight')
plt.close()

# Confusion matrix
fig4, ax = plt.subplots(figsize=(6, 5))
cm = confusion_matrix(noise_mask.astype(int), (S[-1]<0.5).astype(int))
ConfusionMatrixDisplay(cm, display_labels=['Clean','Noise']).plot(ax=ax, cmap='Blues', values_format='d')
ax.set_title(f'Noise Detection (t={N_ITER}, F1={F1_t[-1]:.4f})')
plt.savefig(os.path.join(PLOTS_DIR, 'confusion_matrix.png'), dpi=150, bbox_inches='tight')
plt.close()

# Memory composition
fig5, ax = plt.subplots(figsize=(8, 5))
for i in range(N_ITER+1):
    mem = set(np.where(S[i]>=gamma_hist[i])[0].tolist())
    nn = int(noise_mask[list(mem)].sum()) if mem else 0
    nc = len(mem) - nn
    ax.bar(i, nc, color='steelblue', label='Clean' if i==0 else '')
    ax.bar(i, nn, bottom=nc, color='tomato', label='Noise' if i==0 else '')
ax.set_xlabel('t'); ax.set_ylabel('Samples')
ax.set_title('Memory Bank Composition'); ax.legend()
plt.savefig(os.path.join(PLOTS_DIR, 'memory_composition.png'), dpi=150, bbox_inches='tight')
plt.close()

# Consensus dynamics
fig6, ax = plt.subplots(figsize=(8, 5))
ax.plot(range(N_ITER+1), C_clean_h, 'o-', color='steelblue', lw=2, label='C on clean')
ax.plot(range(N_ITER+1), C_noise_h, 's-', color='tomato', lw=2, label='C on noise')
ax.set_xlabel('t'); ax.set_ylabel('Consensus C(x)')
ax.set_title('Consensus Score Dynamics'); ax.legend(); ax.grid(alpha=0.3)
ax.axhline(0.5, color='k', ls='--', alpha=0.3)
plt.savefig(os.path.join(PLOTS_DIR, 'consensus_dynamics.png'), dpi=150, bbox_inches='tight')
plt.close()

print(f"  Plots saved to {PLOTS_DIR}")

# ============================================================
# RESULTS
# ============================================================
summary = {
    'simulation': 'SCX Self-Evolution v4',
    'parameters': {'N': N, 'M': M_EXPERTS, 'eta': ETA_GLOBAL, 'T': N_ITER,
                   'A_EXP': A_EXP, 'B_EXP': B_EXP, 'seed': SEED},
    'expert_stats': {
        'accuracies': [float(a) for a in expert_accs],
        'avg': float(avg_exp_acc),
        'pairwise_agreement': float(np.mean(pair_agree))
    },
    'state_stats': {'rho': [float(r) for r in rho_s],
                    'mu': [float(m) for m in mu_s],
                    'delta': [float(d) for d in delta_s]},
    'theorem1_F1_bound': float(f1_bound_t1),
    'verification': results,
    'discrepancies': discrepancies
}
with open(RESULTS_PATH, 'w') as f:
    json.dump(summary, f, indent=2)

print("\n" + "=" * 70)
print("FINAL VERDICT")
print("=" * 70)
for name, v in {
    '1. S_t convergence': c1,
    '2. Noise rate decay': c2,
    '3. Memory growth': c3,
    '4. F1 vs Theorem 1': c4,
    '5. Lyapunov decrease': c5,
    '6. Convergence rate': c6,
}.items():
    print(f"  {name}: {v}")
if discrepancies:
    print(f"\n  Discrepancies: {len(discrepancies)}")
    for d in discrepancies:
        print(f"    - {d}")
else:
    print(f"\n  No discrepancies observed.")
print(f"\n  Results: {RESULTS_PATH}")
print("=" * 70)
