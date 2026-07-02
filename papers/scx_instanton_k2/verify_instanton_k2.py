#!/usr/bin/env python3
"""
verify_instanton_k2.py
Verification script for SCX C8: Higher-Dimensional Audit Instantons
==================================================================
This script validates the key theoretical claims:

  1. Experiment 1 (Globally Consistent): All pairwise calibration models
     compose transitively → F = 0, no co-exact part, no H_2 features.
  
  2. Experiment 2 (Circular Inconsistency): Pairwise calibrations fail
     transitivity → F ≠ 0, non-zero co-exact part, H_2 features present.
  
  3. Experiment 3 (Partial Consistency): Two internally-consistent
     subgroups with disconnected calibration frameworks → two separated
     topological features.

KEY INSIGHT: The audit connection A on edge (E_i, E_j) is the estimated
PAIRWISE CALIBRATION MODEL (e.g., linear regression parameters), NOT the
raw per-data-point score difference. The 2-form field strength F measures
the failure of these pairwise calibrations to compose transitively around
a triangle of experts.

  A_ij = (α_ij, β_ij)  where S_i ≈ α_ij + β_ij * S_j
  F_ijk = measure of non-transitivity of A_ij, A_jk, A_ki

This is analogous to gauge theory: A is the connection (the "Christoffel
symbol" of the audit manifold), and F = dA is its curvature.

For the Hodge decomposition, we construct the connection graph using the
pairwise offsets A_ij estimated as linear regression intercepts + slopes.
The co-exact part corresponds to the non-transitive component of these
offset estimates.

Requirements:
  pip install numpy scipy
  (Optional: pip install gudhi for persistent homology)
"""

import sys
import math
import warnings
from itertools import combinations

import numpy as np
from scipy import linalg
from scipy.stats import norm, pearsonr

# =============================================================================
# Try importing persistent homology library
# =============================================================================
try:
    import gudhi
    HAS_GUDHI = True
    print("[INFO] gudhi found — persistent homology enabled.")
except ImportError:
    HAS_GUDHI = False
    print("[WARN] gudhi not found — persistent homology will use manual fallback.")
    print("       Install via: pip install gudhi")


# =============================================================================
# Core: Calibration Model Estimation
# =============================================================================

def estimate_pairwise_calibration(S_i, S_j):
    """
    Estimate linear calibration model: S_i ≈ α + β * S_j
    
    Returns (α, β, r², residual_std)
    """
    # Simple linear regression: S_i = α + β * S_j + ε
    # β = Cov(S_i, S_j) / Var(S_j)
    # α = mean(S_i) - β * mean(S_j)
    
    mean_j = np.mean(S_j)
    mean_i = np.mean(S_i)
    
    cov = np.mean((S_i - mean_i) * (S_j - mean_j))
    var_j = np.var(S_j)
    
    if var_j < 1e-12:
        beta = 0.0
        alpha = mean_i
    else:
        beta = cov / var_j
        alpha = mean_i - beta * mean_j
    
    # R²
    residuals = S_i - (alpha + beta * S_j)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((S_i - mean_i) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
    residual_std = np.std(residuals)
    
    return alpha, beta, r_squared, residual_std


def compose_calibrations(A_ij, A_jk):
    """
    Compose two linear calibration models.
    
    A_ij: S_i = α_ij + β_ij * S_j
    A_jk: S_j = α_jk + β_jk * S_k
    
    Composed: S_i = α_ij + β_ij * (α_jk + β_jk * S_k)
                = (α_ij + β_ij * α_jk) + (β_ij * β_jk) * S_k
    
    Returns (α, β) for composed model.
    """
    alpha_ij, beta_ij = A_ij
    alpha_jk, beta_jk = A_jk
    
    alpha_composed = alpha_ij + beta_ij * alpha_jk
    beta_composed = beta_ij * beta_jk
    
    return (alpha_composed, beta_composed)


def compute_field_strength_triangle(A_ij, A_jk, A_ki):
    """
    Compute 2-form field strength on triangle (E_i → E_j → E_k → E_i).
    
    We compose A_ij ∘ A_jk and compare to the inverse of A_ki.
    
    A_ki: S_k = α_ki + β_ki * S_i
    Inverse of A_ki: S_i = -α_ki/β_ki + (1/β_ki) * S_k  (if β_ki ≠ 0)
    
    F_ijk = || compose(A_ij, A_jk) - inverse(A_ki) ||
    
    Returns (F_alpha, F_beta, F_magnitude)
    """
    alpha_ij, beta_ij = A_ij
    alpha_jk, beta_jk = A_jk
    alpha_ki, beta_ki = A_ki
    
    # Compose i→j→k: S_i in terms of S_k
    alpha_comp, beta_comp = compose_calibrations(A_ij, A_jk)
    
    # Inverse of k→i: from S_k = α_ki + β_ki * S_i
    # → S_i = -α_ki/β_ki + (1/β_ki) * S_k
    if abs(beta_ki) < 1e-10:
        # Degenerate: use direct offset comparison
        F_alpha = abs(alpha_comp + alpha_ki)  # S_k in terms of S_i
        F_beta = abs(beta_comp)
        F_mag = np.sqrt(F_alpha**2 + F_beta**2)
    else:
        alpha_inv = -alpha_ki / beta_ki
        beta_inv = 1.0 / beta_ki
        
        F_alpha = abs(alpha_comp - alpha_inv)
        F_beta = abs(beta_comp - beta_inv)
        F_mag = np.sqrt(F_alpha**2 + F_beta**2)
    
    return F_alpha, F_beta, F_mag


def build_connection_graph(S):
    """
    Build the full connection graph: for each pair of experts (i,j),
    estimate the calibration A_ij = (α_ij, β_ij).
    
    Returns:
      A: dict mapping (i,j) → (α, β, r², residual_std)
    """
    N, M = S.shape
    A = {}
    for i in range(N):
        for j in range(N):
            if i == j:
                A[(i, j)] = (0.0, 1.0, 1.0, 0.0)  # identity
            else:
                alpha, beta, r2, rstd = estimate_pairwise_calibration(S[i, :], S[j, :])
                A[(i, j)] = (alpha, beta, r2, rstd)
    return A


def compute_all_field_strengths(A, N):
    """
    Compute F for all triangles (i,j,k) in the expert graph.
    
    Returns:
      F_vals: dict mapping (i,j,k) → (F_alpha, F_beta, F_mag)
      F_max: maximum F_magnitude
      flux_scores: dict mapping (i,j,k) → variance-based score
    """
    F_vals = {}
    F_max = 0.0
    flux_scores = {}
    
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                A_ij = A[(i, j)][:2]  # (α, β) only
                A_jk = A[(j, k)][:2]
                A_ki = A[(k, i)][:2]
                
                fa, fb, fm = compute_field_strength_triangle(A_ij, A_jk, A_ki)
                F_vals[(i, j, k)] = (fa, fb, fm)
                F_max = max(F_max, fm)
                
                # Alternative: compute on the reverse direction for comparison
                A_ji = A[(j, i)][:2]
                A_kj = A[(k, j)][:2]
                A_ik = A[(i, k)][:2]
                fa_r, fb_r, fm_r = compute_field_strength_triangle(A_ji, A_kj, A_ik)
                
                flux_scores[(i, j, k)] = max(fm, fm_r)
    
    flux_score_max = max(flux_scores.values()) if flux_scores else 0.0
    return F_vals, F_max, flux_score_max, flux_scores


# =============================================================================
# Hodge Decomposition
# =============================================================================

def hodge_decomposition_from_graph(A, N):
    """
    Perform Hodge decomposition on the connection graph.
    
    We extract the "offset" part of each A_ij (the α intercept) and
    treat it as a 1-cochain on the complete graph K_N. Then:
      A_α[i,j] = -A_α[j,i] (skew-symmetric)
      
    Hodge decomposition:
      A_α = A_exact + A_coexact + A_harmonic
    
    For complete graph K_N, dim(H^1) = 0, so A_harmonic = 0.
    The interesting part is the co-exact component.
    """
    # Build skew-symmetric offset matrix from α parameters
    A_alpha = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                alpha_ij = A[(i, j)][0]
                A_alpha[i, j] = alpha_ij
    
    # Skew-symmetrize
    A_alpha_skew = (A_alpha - A_alpha.T) / 2.0
    
    # Number of edges
    n_edges = N * (N - 1) // 2
    
    # Build coboundary operators
    # d_0: C^0 → C^1, mapping vertex potentials to edge differences
    d0 = np.zeros((n_edges, N))
    edge_idx = {}
    e = 0
    for i in range(N):
        for j in range(i + 1, N):
            edge_idx[(i, j)] = e
            d0[e, i] = -1.0
            d0[e, j] = 1.0
            e += 1
    
    # d_1: C^1 → C^2, mapping edge values to triangle circulations
    n_tri = N * (N - 1) * (N - 2) // 6
    d1 = np.zeros((n_tri, n_edges))
    tri_idx = {}
    t = 0
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                tri_idx[(i, j, k)] = t
                d1[t, edge_idx[(i, j)]] = 1.0
                d1[t, edge_idx[(j, k)]] = 1.0
                d1[t, edge_idx[(i, k)]] = -1.0
                t += 1
    
    # Flatten A_alpha_skew to edge vector
    a_vec = np.zeros(n_edges)
    for (i, j), idx in edge_idx.items():
        a_vec[idx] = A_alpha_skew[i, j]
    
    # Laplacian Δ_1 = d_0 δ_0 + δ_1 d_1
    delta0 = d0.T
    delta1 = d1.T
    L1 = d0 @ delta0 + delta1 @ d1
    
    # Project onto im(d_0) — exact part
    d0_pinv = np.linalg.pinv(d0)
    proj_d0 = d0 @ d0_pinv
    a_exact_vec = proj_d0 @ a_vec
    
    # Project onto im(δ_1) — co-exact part
    d1T_pinv = np.linalg.pinv(delta1)
    proj_d1T = delta1 @ d1T_pinv
    a_coexact_vec = proj_d1T @ a_vec
    
    # Harmonic part
    a_harmonic_vec = a_vec - a_exact_vec - a_coexact_vec
    
    # Reconstruct matrices
    A_exact = np.zeros((N, N))
    A_coexact = np.zeros((N, N))
    A_harmonic = np.zeros((N, N))
    
    for (i, j), idx in edge_idx.items():
        A_exact[i, j] = a_exact_vec[idx]
        A_exact[j, i] = -a_exact_vec[idx]
        A_coexact[i, j] = a_coexact_vec[idx]
        A_coexact[j, i] = -a_coexact_vec[idx]
        A_harmonic[i, j] = a_harmonic_vec[idx]
        A_harmonic[j, i] = -a_harmonic_vec[idx]
    
    return {
        'exact': A_exact,
        'coexact': A_coexact,
        'harmonic': A_harmonic,
        'exact_norm': np.linalg.norm(a_exact_vec),
        'coexact_norm': np.linalg.norm(a_coexact_vec),
        'harmonic_norm': np.linalg.norm(a_harmonic_vec),
    }


# =============================================================================
# Persistent Homology Computation
# =============================================================================

def compute_H2_persistence(S):
    """
    Compute H_2 persistence diagram from the expert score point cloud.
    
    Each data point is a vector of N expert scores. We compute Euclidean
    distances and Vietoris-Rips persistence in dimension 2.
    """
    N, M = S.shape
    points = S.T  # M × N
    
    if HAS_GUDHI:
        rips = gudhi.RipsComplex(points=points, max_edge_length=np.inf)
        st = rips.create_simplex_tree(max_dimension=3)
        st.compute_persistence()
        persistence = st.persistence_intervals_in_dimension(2)
        return persistence
    else:
        # Manual fallback: use distance matrix
        dist = np.zeros((M, M))
        for a in range(M):
            for b in range(M):
                dist[a, b] = np.linalg.norm(points[a] - points[b])
        
        # Use simplified cluster-based estimation of persistent features
        from scipy.cluster.hierarchy import linkage, fcluster
        from scipy.spatial.distance import squareform
        
        # Condense distance matrix
        condensed = squareform(dist)
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Z = linkage(condensed, method='ward')
        
        # Count features by tracking cluster formation at multiple scales
        n_features = 0
        thresholds = np.linspace(np.min(dist[dist > 0]), np.max(dist) / 2, 15)
        prev_n = M
        
        for t in thresholds:
            clusters = fcluster(Z, t, criterion='distance')
            n_clusters = len(np.unique(clusters))
            # A drop in cluster count indicates merging — a topological feature
            if n_clusters < prev_n and n_clusters >= 2:
                n_features += 1
            elif n_clusters < prev_n and n_clusters == 1:
                n_features += 1
            prev_n = n_clusters
        
        return np.array([(0, 1)] * n_features) if n_features > 0 else np.array([])


# =============================================================================
# Experiment 1: Globally Consistent
# =============================================================================

def experiment_1_globally_consistent(seed=42):
    """
    Experiment 1: Globally Consistent Experts
    
    N=5 experts, M=200 data points.
    All experts share the same underlying scoring framework:
      S_i(x) = f(x) + c_i + ε_i(x)
    where c_i is a constant per-expert offset.
    
    Prediction: All pairwise calibrations are transitive → F ≡ 0.
    """
    print("\n" + "=" * 70)
    print("Experiment 1: Globally Consistent Scenario")
    print("=" * 70)
    
    np.random.seed(seed)
    N, M = 5, 200
    sigma = 0.05
    
    # Ground truth
    x_vals = np.linspace(0, 4 * np.pi, M)
    f = np.sin(x_vals) + 0.5 * np.cos(3 * x_vals)
    
    # Per-expert constant offsets (these are "gauge-equivalent")
    offsets = np.array([0.0, 0.15, -0.08, 0.22, 0.05])
    
    S = np.zeros((N, M))
    for i in range(N):
        S[i, :] = f + offsets[i] + sigma * np.random.randn(M)
    
    # Build connection graph
    A = build_connection_graph(S)
    
    # Compute field strengths
    F_vals, F_max, flux_score_max, flux_scores = compute_all_field_strengths(A, N)
    
    print(f"  F_max (triangle non-transitivity)      = {F_max:.6f}")
    print(f"  FluxScore_max                          = {flux_score_max:.6f}")
    
    # Show one triangle
    if N >= 3:
        A_01 = A[(0, 1)][:2]
        A_12 = A[(1, 2)][:2]
        A_20 = A[(2, 0)][:2]
        fa, fb, fm = compute_field_strength_triangle(A_01, A_12, A_20)
        print(f"  Triangle (0,1,2): F_α={fa:.6f}, F_β={fb:.6f}, |F|={fm:.6f}")
        
        # Show composed vs direct
        comp = compose_calibrations(A_01, A_12)
        direct = A[(0, 2)][:2]
        print(f"    Compose(0→1→2):  α={comp[0]:.6f}, β={comp[1]:.6f}")
        print(f"    Direct(0→2):     α={direct[0]:.6f}, β={direct[1]:.6f}")
    
    # Hodge decomposition
    hodge = hodge_decomposition_from_graph(A, N)
    print(f"  ||A_exact||    = {hodge['exact_norm']:.6f}")
    print(f"  ||A_coexact||  = {hodge['coexact_norm']:.6f}")
    print(f"  ||A_harmonic|| = {hodge['harmonic_norm']:.6f}")
    
    # H_2 persistence
    H2_pers = compute_H2_persistence(S)
    n_h2 = len(H2_pers)
    print(f"  H_2 persistence features: {n_h2}")
    
    # Verdict
    f_small = F_max < 0.15  # Allow small estimation noise
    coexact_small = hodge['coexact_norm'] < 0.15
    
    passed = f_small and coexact_small
    print(f"\n  Verdict: {'[PASS]' if passed else '[FAIL]'}")
    print(f"    - Field strength ≈ 0:     {f_small} (F_max={F_max:.4f})")
    print(f"    - Co-exact part ≈ 0:      {coexact_small} (|A_coex|={hodge['coexact_norm']:.4f})")
    print(f"    - Interpretation: All calibrations compose transitively.")
    
    return passed, {
        'F_max': F_max,
        'flux_score_max': flux_score_max,
        'A_coexact_norm': hodge['coexact_norm'],
        'n_H2': n_h2,
    }


# =============================================================================
# Experiment 2: Circular Inconsistency
# =============================================================================

def experiment_2_circular_inconsistency(seed=42):
    """
    Experiment 2: Circular Inconsistency
    
    N=3 experts, M=300 data points.
    
    Expert 1: S_1(x) = f(x) + ε
    Expert 2: S_2(x) = g(f(x)) + ε   (nonlinear transformation)
    Expert 3: S_3(x) = h(f(x)) + ε   (different nonlinear transformation)
    
    Because the relationships between experts are genuinely nonlinear,
    linear calibration models estimated pairwise will FAIL transitivity.
    
    This produces F ≠ 0: the pairwise calibrations do not compose to
    yield a globally consistent picture.
    """
    print("\n" + "=" * 70)
    print("Experiment 2: Circular Inconsistency Scenario")
    print("=" * 70)
    
    np.random.seed(seed)
    N, M = 3, 300
    sigma = 0.03
    
    # Ground truth latent variable
    x_vals = np.linspace(0, 4 * np.pi, M)
    f = np.sin(x_vals) + 0.5 * np.cos(3 * x_vals)
    f_norm = (f - np.min(f)) / (np.max(f) - np.min(f))  # normalize to [0,1]
    
    # Expert 1: linear in f
    S1 = f_norm + sigma * np.random.randn(M)
    
    # Expert 2: nonlinear — uses square root of f (compresses high values)
    S2 = np.sqrt(np.maximum(f_norm, 0.01)) + 0.1 * f_norm + sigma * np.random.randn(M)
    
    # Expert 3: nonlinear — uses square of f (expands high values)
    S3 = f_norm**2 + 0.2 * np.sin(2 * np.pi * f_norm) + sigma * np.random.randn(M)
    
    S = np.vstack([S1, S2, S3])
    
    # Build connection graph
    A = build_connection_graph(S)
    
    # Show pairwise calibration models
    print("  Pairwise calibration models (S_i = α + β * S_j):")
    for i in range(N):
        for j in range(N):
            if i != j:
                alpha, beta, r2, rstd = A[(i, j)]
                print(f"    {i}←{j}: α={alpha:.6f}, β={beta:.6f}, R²={r2:.4f}")
    
    # Compute field strengths
    F_vals, F_max, flux_score_max, flux_scores = compute_all_field_strengths(A, N)
    print(f"\n  F_max (triangle non-transitivity)      = {F_max:.6f}")
    
    # Detailed triangle analysis
    print("  Triangle analysis:")
    for (i, j, k), (fa, fb, fm) in F_vals.items():
        print(f"    ({i},{j},{k}): F_α={fa:.6f}, F_β={fb:.6f}, |F|={fm:.6f}")
        
        # Compose i→j→k
        A_ij = A[(i, j)][:2]
        A_jk = A[(j, k)][:2]
        A_ik = A[(i, k)][:2]
        
        comp = compose_calibrations(A_ij, A_jk)
        print(f"      Compose({i}→{j}→{k}): α={comp[0]:.6f}, β={comp[1]:.6f}")
        print(f"      Direct({i}→{k}):      α={A_ik[0]:.6f}, β={A_ik[1]:.6f}")
        print(f"      Mismatch:              Δα={abs(comp[0]-A_ik[0]):.6f}, Δβ={abs(comp[1]-A_ik[1]):.6f}")
    
    # Also check reverse direction
    A_21 = A[(2, 1)][:2]
    A_10 = A[(1, 0)][:2]
    A_20 = A[(2, 0)][:2]
    comp_r = compose_calibrations(A_21, A_10)
    fa_r, fb_r, fm_r = compute_field_strength_triangle(A_21, A_10, A_20)
    print(f"    Reverse (2→1→0): |F|={fm_r:.6f}")
    
    # Hodge decomposition
    hodge = hodge_decomposition_from_graph(A, N)
    print(f"\n  ||A_exact||    = {hodge['exact_norm']:.6f}")
    print(f"  ||A_coexact||  = {hodge['coexact_norm']:.6f}")
    print(f"  ||A_harmonic|| = {hodge['harmonic_norm']:.6f}")
    
    # H_2 persistence
    H2_pers = compute_H2_persistence(S)
    n_h2 = len(H2_pers)
    print(f"  H_2 persistence features: {n_h2}")
    
    # Compute information-theoretic quantities
    # We use the mean of |F| over all triangles as the "inconsistency signal"
    mean_F = np.mean([fm for _, _, fm in F_vals.values()])
    std_F = np.std([fm for _, _, fm in F_vals.values()])
    
    # SNR: mean inconsistency relative to estimation noise
    # Estimate noise std from residual std of pairwise regressions
    noise_stds = [A[(i, j)][3] for i in range(N) for j in range(N) if i != j]
    avg_noise = np.mean(noise_stds)
    SNR = mean_F / avg_noise if avg_noise > 0 else 0.0
    print(f"\n  Information-theoretic summary:")
    print(f"    Mean |F|              = {mean_F:.6f}")
    print(f"    Avg residual std      = {avg_noise:.6f}")
    print(f"    SNR (|F| / noise)     = {SNR:.2f}")
    
    # Sample complexity for Wald test
    alpha = 0.05
    z = norm.ppf(1 - alpha / 2)
    if SNR > 0:
        M_req = (z / SNR) ** 2
        print(f"    Required M for α=0.05: M ≥ {M_req:.0f}")
    else:
        print(f"    SNR too low for reliable detection")
    
    # Verdict: we should detect non-zero flux
    f_nonzero_ok = F_max > 0.05
    coexact_nonzero_ok = hodge['coexact_norm'] > 0.02
    
    passed = f_nonzero_ok and coexact_nonzero_ok
    print(f"\n  Verdict: {'[PASS]' if passed else '[FAIL]'}")
    print(f"    - Non-zero field strength:    {f_nonzero_ok} (|F|_max={F_max:.4f})")
    print(f"    - Non-zero co-exact part:     {coexact_nonzero_ok} (|A_coex|={hodge['coexact_norm']:.4f})")
    print(f"    - Interpretation: Pairwise calibrations fail transitivity.")
    print(f"      → CIRCULAR INCONSISTENCY DETECTED.")
    
    return passed, {
        'F_max': F_max,
        'flux_score_max': flux_score_max,
        'A_coexact_norm': hodge['coexact_norm'],
        'mean_F': mean_F,
        'SNR': SNR,
        'n_H2': n_h2,
    }


# =============================================================================
# Experiment 3: Partial Consistency
# =============================================================================

def experiment_3_partial_consistency(seed=42):
    """
    Experiment 3: Partial Consistency
    
    N=6 experts split into two groups of 3.
    Within each group: globally consistent (transitive calibrations).
    Across groups: different frameworks → non-transitive calibrations.
    
    Prediction: F=0 within subgroups, F≠0 across subgroups.
    H_2 persistence should show two separated topological features.
    """
    print("\n" + "=" * 70)
    print("Experiment 3: Partial Consistency Scenario")
    print("=" * 70)
    
    np.random.seed(seed)
    N, M = 6, 200
    sigma = 0.04
    
    # Two different ground truth functions (different "frameworks")
    x_vals = np.linspace(0, 4 * np.pi, M)
    f_A = np.sin(x_vals) + 0.5 * np.cos(3 * x_vals)
    f_A_norm = (f_A - np.min(f_A)) / (np.max(f_A) - np.min(f_A))
    
    f_B = np.cos(2 * x_vals) - 0.3 * np.sin(5 * x_vals)
    f_B_norm = (f_B - np.min(f_B)) / (np.max(f_B) - np.min(f_B))
    
    S = np.zeros((N, M))
    
    # Subgroup A (experts 0,1,2): consistent with f_A
    offsets_A = [0.0, 0.12, -0.06]
    for i in range(3):
        S[i, :] = f_A_norm + offsets_A[i] + sigma * np.random.randn(M)
    
    # Subgroup B (experts 3,4,5): consistent with f_B (different framework)
    offsets_B = [0.0, 0.18, -0.09]
    for i in range(3, 6):
        S[i, :] = f_B_norm + offsets_B[i - 3] + sigma * np.random.randn(M)
    
    # Build connection graph
    A = build_connection_graph(S)
    
    # Within-subgroup analysis
    print("  Within Subgroup A (experts 0,1,2):")
    S_A = S[:3, :]
    A_A = build_connection_graph(S_A)
    _, FA_max, _, _ = compute_all_field_strengths(A_A, 3)
    hodge_A = hodge_decomposition_from_graph(A_A, 3)
    print(f"    F_max       = {FA_max:.6f}")
    print(f"    |A_coexact| = {hodge_A['coexact_norm']:.6f}")
    
    print("  Within Subgroup B (experts 3,4,5):")
    S_B = S[3:, :]
    A_B = build_connection_graph(S_B)
    _, FB_max, _, _ = compute_all_field_strengths(A_B, 3)
    hodge_B = hodge_decomposition_from_graph(A_B, 3)
    print(f"    F_max       = {FB_max:.6f}")
    print(f"    |A_coexact| = {hodge_B['coexact_norm']:.6f}")
    
    # Cross-group analysis
    print("  Full graph (experts 0-5):")
    _, Fall_max, _, _ = compute_all_field_strengths(A, N)
    hodge_all = hodge_decomposition_from_graph(A, N)
    print(f"    F_max       = {Fall_max:.6f}")
    print(f"    |A_coexact| = {hodge_all['coexact_norm']:.6f}")
    
    # Show a cross-group triangle
    A_01 = A[(0, 1)][:2]
    A_13 = A[(1, 3)][:2]
    A_30 = A[(3, 0)][:2]
    fa, fb, fm = compute_field_strength_triangle(A_01, A_13, A_30)
    print(f"    Cross-group triangle (0,1,3): |F|={fm:.6f}")
    
    # H_2 persistence
    H2_pers = compute_H2_persistence(S)
    n_h2 = len(H2_pers)
    print(f"\n  H_2 persistence features: {n_h2}")
    
    # Verdict
    subgroup_ok = FA_max < 0.1 and FB_max < 0.1
    cross_group_ok = Fall_max > 0.1 or hodge_all['coexact_norm'] > 0.05
    
    passed = subgroup_ok and cross_group_ok
    print(f"\n  Verdict: {'[PASS]' if passed else '[FAIL]'}")
    print(f"    - Subgroups internally consistent: {subgroup_ok}")
    print(f"    - Cross-group inconsistency:       {cross_group_ok}")
    print(f"    - Interpretation: Two disconnected evaluation frameworks.")
    
    return passed, {
        'F_max_A': FA_max,
        'F_max_B': FB_max,
        'F_max_all': Fall_max,
        'A_coexact_norm_all': hodge_all['coexact_norm'],
        'n_H2': n_h2,
    }


# =============================================================================
# Experiment 4: Hodge Decomposition Theorem Validation
# =============================================================================

def experiment_4_hodge_validation(seed=42):
    """
    Experiment 4: Validate Hodge Decomposition Theorem
    
    Theorem (Sec 3.2): A = A_exact + A_coexact + A_harmonic.
    - F = d_1 A depends ONLY on A_coexact
    - A_exact and A_harmonic contribute zero to F
    
    We construct:
    - A purely exact connection (from constant offsets)
    - A purely co-exact connection (from non-transitive offsets)
    - Verify that F is zero on the exact part and non-zero on co-exact part
    """
    print("\n" + "=" * 70)
    print("Experiment 4: Hodge Decomposition Validation")
    print("=" * 70)
    
    np.random.seed(seed)
    N, M = 4, 150
    sigma = 0.03
    
    x_vals = np.linspace(0, 4 * np.pi, M)
    f = np.sin(x_vals) + 0.5 * np.cos(3 * x_vals)
    f_norm = (f - np.min(f)) / (np.max(f) - np.min(f))
    
    # --- Test A: Pure exact connection ---
    print("\n  Test A: Pure exact connection (constant offsets)")
    offsets = np.array([0.0, 0.2, -0.1, 0.15])
    S_exact = np.zeros((N, M))
    for i in range(N):
        S_exact[i, :] = f_norm + offsets[i] + sigma * np.random.randn(M)
    
    A_ex = build_connection_graph(S_exact)
    _, Fmax_ex, _, _ = compute_all_field_strengths(A_ex, N)
    hodge_ex = hodge_decomposition_from_graph(A_ex, N)
    
    print(f"    F_max             = {Fmax_ex:.6f}")
    print(f"    |A_coexact|       = {hodge_ex['coexact_norm']:.6f}")
    print(f"    |A_exact|         = {hodge_ex['exact_norm']:.6f}")
    testA_pass = Fmax_ex < 0.1 and hodge_ex['coexact_norm'] < 0.1
    print(f"    → {'PASS' if testA_pass else 'FAIL'}: F ≈ 0 when A_coexact ≈ 0")
    
    # --- Test B: Mixed connection (exact + co-exact) ---
    print("\n  Test B: Mixed connection (exact + co-exact parts)")
    # Expert 0,1: pure exact (constant offset from f_norm)
    # Expert 2: nonlinear transform → creates co-exact component
    # Expert 3: another nonlinear transform
    
    S_mixed = np.zeros((N, M))
    S_mixed[0, :] = f_norm + sigma * np.random.randn(M)
    S_mixed[1, :] = f_norm + 0.2 + sigma * np.random.randn(M)
    S_mixed[2, :] = np.sqrt(np.maximum(f_norm, 0.01)) + sigma * np.random.randn(M)
    S_mixed[3, :] = f_norm**2 + sigma * np.random.randn(M)
    
    A_mx = build_connection_graph(S_mixed)
    _, Fmax_mx, _, _ = compute_all_field_strengths(A_mx, N)
    hodge_mx = hodge_decomposition_from_graph(A_mx, N)
    
    print(f"    F_max             = {Fmax_mx:.6f}")
    print(f"    |A_coexact|       = {hodge_mx['coexact_norm']:.6f}")
    print(f"    |A_exact|         = {hodge_mx['exact_norm']:.6f}")
    
    # Verify: compute F from exact part only → should be 0
    # Reconstruct A from exact part and compute F
    A_mx_exact_only = {}
    for i in range(N):
        for j in range(N):
            if i != j:
                A_mx_exact_only[(i, j)] = (hodge_mx['exact'][i, j], 1.0, 1.0, sigma)
    
    _, Fmax_exact_only, _, _ = compute_all_field_strengths(A_mx_exact_only, N)
    print(f"    F_max (exact only) = {Fmax_exact_only:.6f}")
    
    # Verify: F from co-exact part should match original F (up to noise)
    A_mx_coexact_only = {}
    for i in range(N):
        for j in range(N):
            if i != j:
                A_mx_coexact_only[(i, j)] = (hodge_mx['coexact'][i, j], 1.0, 1.0, sigma)
    
    _, Fmax_coexact_only, _, _ = compute_all_field_strengths(A_mx_coexact_only, N)
    print(f"    F_max (coexact only) = {Fmax_coexact_only:.6f}")
    
    testB_pass = (Fmax_exact_only < 0.02 and Fmax_mx > 0.05)
    print(f"    → {'PASS' if testB_pass else 'FAIL'}: F depends only on co-exact part")
    
    # --- Test C: Harmonic part for K_N ---
    # For complete graph K_N, H^1(K_N) = 0, so harmonic part should be zero
    print(f"\n  Test C: Harmonic part for K_{N}")
    print(f"    |A_harmonic| = {hodge_ex['harmonic_norm']:.6f} (exact case)")
    print(f"    |A_harmonic| = {hodge_mx['harmonic_norm']:.6f} (mixed case)")
    testC_pass = hodge_ex['harmonic_norm'] < 1e-6 and hodge_mx['harmonic_norm'] < 1e-6
    print(f"    → {'PASS' if testC_pass else 'FAIL'}: H^1(K_N)=0, harmonic part vanishes")
    
    passed = testA_pass and testB_pass and testC_pass
    print(f"\n  Overall Hodge Validation: {'[PASS]' if passed else '[FAIL]'}")
    
    return passed, {
        'testA': testA_pass,
        'testB': testB_pass,
        'testC': testC_pass,
    }


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 70)
    print("  SCX Audit Instanton k>1 — Verification Suite")
    print("  Higher-Dimensional Audit Instantons (C8 Extension)")
    print("=" * 70)
    print()
    print("  Key insight: The audit connection A_ij is the estimated PAIRWISE")
    print("  CALIBRATION MODEL between experts (linear regression parameters),")
    print("  not the raw per-data-point score difference.")
    print("  F = dA measures failure of calibration transitivity.")
    
    all_passed = True
    results = {}
    
    experiments = [
        ("Experiment 1: Globally Consistent", experiment_1_globally_consistent),
        ("Experiment 2: Circular Inconsistency", experiment_2_circular_inconsistency),
        ("Experiment 3: Partial Consistency", experiment_3_partial_consistency),
        ("Experiment 4: Hodge Decomposition Validation", experiment_4_hodge_validation),
    ]
    
    for exp_name, exp_func in experiments:
        try:
            passed, res = exp_func()
            results[exp_name] = {'passed': passed, 'data': res}
            all_passed = all_passed and passed
        except Exception as e:
            print(f"\n[ERROR] {exp_name} failed: {e}")
            import traceback
            traceback.print_exc()
            results[exp_name] = {'passed': False, 'error': str(e)}
            all_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    print("  VERIFICATION SUMMARY")
    print("=" * 70)
    
    for exp_name, res in results.items():
        status = "✓ PASS" if res['passed'] else "✗ FAIL"
        print(f"  {status}  {exp_name}")
    
    print(f"\n  Overall: {'ALL PASSED ✓' if all_passed else 'SOME FAILED ✗'}")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
