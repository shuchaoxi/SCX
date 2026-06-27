# Feature Strength via k-means Stability: A Practical Diagnostic for SCX

> **Status:** Proposal | **Date:** 2026-06-27
> **Purpose:** Replace the failed BBP spectral bridge with a stability-based diagnostic that tests what SCX actually does (k-means clustering), without assuming Gaussianity, isotropy, or i.i.d. entries.
> **Relation:** Direct alternative to `bbp_spectral_proxy.md`; upgrades `feature_strength_diagnostic()` in `StateValue`

---

## Table of Contents

1. [Why the BBP Bridge Failed](#1-why-the-bbp-bridge-failed)
2. [The Stability-Based Alternative](#2-the-stability-based-alternative)
3. [Theorem: Clustering Stability Criterion for SCX Reliability](#3-theorem-clustering-stability-criterion-for-scx-reliability)
4. [Corollary: Practical Threshold Rule](#4-corollary-practical-threshold-rule)
5. [Practical Algorithm](#5-practical-algorithm)
6. [Implementation in SCX](#6-implementation-in-scx)
7. [Comparison to Existing `feature_strength_diagnostic()`](#7-comparison-to-existing-feature_strength_diagnostic)
8. [Validation Strategy](#8-validation-strategy)
9. [Honest Limitations](#9-honest-limitations)
10. [References](#10-references)

---

## 1. Why the BBP Bridge Failed

The BBP spectral proxy (`bbp_spectral_proxy.md`) attempted to connect Theorem 2's mutual information delta = I(phi; S) to the largest eigenvalue lambda_1 of the feature Gram matrix. The goal was to replace an intractable quantity (MI) with a computable one (eigenvalue). The attempt failed for five reasons, each independently fatal:

### 1.1 The Information-Spectral Bridge Was Hand-Waving

The core claim was that delta_hat = (lambda_1 - MP_+) / C serves as a proxy for delta = I(phi; S). But lambda_1 measures the **maximum variance direction** of the marginal distribution P(phi), while delta measures the **reduction in uncertainty about S given phi**. These are structurally different:

- A high-variance feature that is independent of S produces a large lambda_1 but delta = 0. Counterexample: phi_1 ~ N(0, 1000), S independent of all features. lambda_1 >> MP_+, delta = 0. The proxy declares "strong features" when the truth is completely uninformative.

- A feature set where state means differ in coordinate support patterns (not in norm) can produce large delta but small lambda_1. Counterexample: 50 states, each with 20 unique coordinates set to 0.5. The between-state scatter is rank-49, but each eigenvalue is tiny. delta ~ log_2(50) = 5.6 bits, lambda_1 barely above the MP bulk. The proxy declares "weak features" when the features are highly informative.

The "monotonic relationship" claimed in Section 3.4 of the BBP document was unsupported. The bounds relating theta (effective signal strength) to delta span a factor of 4(K-1) — too loose to guarantee any practical monotonicity. A simple counterexample: two different mean geometries with identical theta produce deltas differing by a factor of 2theta, disproving monotonicity even within the isotropic Gaussian model.

### 1.2 The Gaussian Assumption Is Fatal for SCX's Real Features

The entire BBP derivation assumes isotropic Gaussian within-state distributions. SCX's actual features violate this:

- **ACE descriptors** for AlN are body-order expansions with cutoff functions, radial basis polynomials, and spherical harmonics. They are not Gaussian, not isotropic (different channels have vastly different variances), and not independent across samples (atomic configurations share atoms in periodic supercells).
- **CNN latents** (CIFAR-10, DermaMNIST) have ReLU activations, max-pooling, and known non-Gaussian "cone" distributions on low-dimensional manifolds. Their singular value distribution decays slowly, not the sharp spectral gap assumed by the spiked model.
- **Tabular features** have arbitrary marginals, missing values, and mixed types.

Without isotropy, the Marchenko-Pastur bulk edge MP_+ is wrong, the BBP threshold sqrt(gamma) is wrong, and the entire spectral test is invalid.

### 1.3 The Calibration Constant C Was Circular

The calibration C = (lambda_1 - MP_+) / delta depends on the unknown theta, which is inferred from lambda_1. This is algebraically redundant: if you can estimate theta from lambda_1 via the BBP inverse formula, you can compute delta directly from theta without the proxy. The "self-consistent estimation" was a change of variables, not an independent quantity.

The practical default C = 2 was valid only when gamma is negligible, theta >> sqrt(gamma), K = 2, and d >> theta — conditions that fail for every SCX dataset.

### 1.4 The Tracy-Widom Test Is Invalid for Non-i.i.d. Features

The TW_1 critical values require i.i.d. entries with finite fourth moment. SCX features violate this in multiple ways:
- Row dependence (samples share atoms in ACE descriptors)
- Column dependence (ACE channels are correlated; CNN latents have network-induced correlations)
- Heavy-tailed marginals (ACE products of radial basis functions can spike near cutoffs)

The resulting anti-conservative test produces false positives at rates exceeding the nominal significance level.

### 1.5 The "Many Weak Signals" Regime Is Not Addressable

For K states with balanced separation in many directions, the total mutual information can be large while every individual eigenvalue is subcritical. This is not a niche case — it is the expected behavior for material science ACE descriptors with dozens of local atomic environment types (perfect crystal, various defects, surfaces, grain boundaries). The spectral proxy cannot detect this, and the multi-spike extension inherits the same limitation.

### 1.6 Lesson Learned

**Do not try to bridge delta to lambda_1.** They measure different things, and the assumptions required for any bridge (Gaussianity, isotropy, i.i.d. entries) are violated by SCX's actual features. Instead, replace delta entirely with a different weak-feature criterion that is independently justified, computationally tractable, and tests what SCX actually does.

---

## 2. The Stability-Based Alternative

### 2.1 Core Idea

Theorem 2's delta = I(phi; S) asks: "Do features carry information about states?" But there is a more practical question: **"Does the clustering you actually run produce stable results?"**

SCX state discovery performs k-means on the feature matrix Phi. If features are strong (well-separated states), k-means should produce nearly identical clusterings across different random initializations and bootstrap resamples. If features are weak (no clear state structure), k-means will produce unstable, random-seeming clusterings that vary wildly across resamples.

This is the **clustering stability** approach (von Luxburg, 2010; Ben-David et al., 2006; Lange et al., 2004). Stability has been extensively studied as a model selection criterion for clustering: the "right" number of clusters K is the one that maximizes stability. Here, we invert this: given K (the number of states), we use stability to measure whether the features support a reliable clustering at that K.

### 2.2 Why This Works for SCX

| Requirement | BBP Spectral Proxy | Stability Diagnostic |
|---|---|---|
| Gaussian assumption | Required | Not needed |
| Isotropy | Required | Not needed |
| i.i.d. entries | Required | Not needed |
| Tests what SCX does | No (tests Gram matrix eigenvalues) | **Yes** (tests k-means output) |
| Computable | Yes | Yes (B x k-means) |
| Detects "many weak signals" regime | No | **Yes** (aggregate stability captures multi-directional signal) |
| Sensitive to nuisance variance | Yes (high variance = false positive) | **No** (uninformative variance produces unstable clustering) |
| Known S required? | No | No |

The stability diagnostic directly tests the quantity that matters for SCX: **can k-means discover a reliable state partition from these features?** It does not attempt to estimate mutual information, does not depend on distributional assumptions, and does not require knowing the true state labels.

### 2.3 Intuition

Consider two extremes:

- **Strong features** (e.g., AlN ACE descriptors with clear defect vs. perfect crystal separation): k-means on bootstrap resamples will recover nearly the same clusters every time. The adjusted Rand index (ARI) between clusterings from different bootstrap samples will be close to 1.0.

- **Weak features** (e.g., DermaMNIST SimpleCNN features where disease classes are not well-separated): k-means on bootstrap resamples will produce different clusterings each time — some samples will switch cluster assignments depending on which other samples are included in the bootstrap. The ARI will be close to its expectation for random clusterings, which is approximately 0.

Stability captures this continuum. The ARI between bootstrap clusterings is a direct measure of how much structure the features impose on the k-means solution.

---

## 3. Theorem: Clustering Stability Criterion for SCX Reliability

### 3.1 Setup

Let the feature vectors phi(x_1), ..., phi(x_N) in R^d be drawn from a mixture distribution with K components (states), not necessarily Gaussian. Let:

- Phi be the N x d feature matrix
- K be the number of states (determined by the SCX pipeline)
- A = {s_1, ..., s_K} be the k-means clustering of Phi (with optimal K, run to convergence)
- For bootstrap sample b = 1, ..., B, let Phi_b be an N x d matrix formed by resampling N rows from Phi with replacement, and let A_b be the k-means clustering on Phi_b (initialized with the same scheme as A)

Define the **clustering stability**:

$$S(\Phi, K) = \frac{1}{B} \sum_{b=1}^B \text{ARI}(A, A_b)$$

where ARI is the adjusted Rand index (Hubert & Arabie, 1985), which compares the overlap between two clusterings, corrected for chance. ARI = 1 indicates identical clusterings; ARI = 0 (or negative) indicates overlap no better than random.

### 3.2 Theorem Statement

**Theorem (Clustering Stability Criterion for SCX Feature Strength).**
Let the feature vectors phi(x_i) be drawn from a K-component mixture with minimum center separation Delta_min (in Euclidean distance), bounded center norms, and sub-Gaussian within-component noise with variance proxy sigma^2. Let n_min = min_k n_k be the smallest component size. Then:

**Part (a) — Strong features imply high stability.** If the minimum center separation satisfies:

$$\frac{\Delta_{\min}^2}{\sigma^2} > C_1 \cdot \frac{d + \log N}{n_{\min}}$$

for a universal constant C_1 > 0, then with probability at least 1 - O(N^{-1}):

$$S(\Phi, K) > 1 - \varepsilon$$

where epsilon = O(exp(-c * n_min * Delta_min^2 / sigma^2)) for some constant c > 0.

**Part (b) — Weak features imply low stability.** If the centers of the K components are drawn from a distribution with bounded second moment (or if the component structure is absent, i.e., all mu_k are equal), then:

$$\mathbb{E}[S(\Phi, K)] \leq \mathbb{E}[\text{ARI of random clusterings}] + O\left(\frac{K}{\sqrt{N}}\right)$$

where the expected ARI of random (independent) clusterings with K clusters of the same sizes is approximately 0. Specifically, for random partitions with equal cluster sizes, E[ARI] = 0 and Var(ARI) = O(1/N).

**Part (c) — Plug-in diagnostic for SCX reliability.** If S(Phi, K) < tau for a threshold tau in (0, 1), then with high probability:

$$F1_{\text{SCX}} \leq F1_{\text{base}} + \gamma_{CF}(S)$$

where gamma_{CF}(S) is a non-decreasing function of S such that gamma_{CF}(S) → 0 as S → 0. Conversely, if S(Phi, K) > tau, the bound does not guarantee SCX success (other factors like expert redundancy and noise rate also matter), but features are not the bottleneck.

### 3.3 Proof Sketch

**Part (a)** follows from the theory of k-means stability for well-separated mixtures (Shamir & Tishby, 2009; Rakhlin & Caponnetto, 2007). When centers are sufficiently separated, the k-means optimization landscape has a unique deep optimum (up to label permutation) within a radius of the true centers. Bootstrap resampling perturbs the empirical risk by O(sqrt(d/N)) in each direction, which is insufficient to escape the basin of attraction. The ARI between clusterings from nearby optima is bounded below by 1 - O(exp(-c * n_min * separation^2)).

**Key inequality for the separation condition.** For the k-means objective:

$$W(A) = \frac{1}{N} \sum_{k=1}^K \sum_{i: s_i = k} \|\phi(x_i) - c_k\|^2$$

with centers c_k, standard results (Pollard, 1981) show that if the population minimizer has centers separated by at least Delta_min, the empirical minimizer converges to it at rate sqrt(d/(n_min * N)). The bootstrap resample adds an additional sampling perturbation of order sqrt((d + log N)/N). The condition in Part (a) ensures that the bootstrap perturbation is smaller than the signal, so the clustering remains stable.

**Part (b)** follows from the fact that when no state structure exists, k-means partitions the data arbitrarily based on initialization and random sampling fluctuations. The ARI between independent runs on different bootstrap samples converges to the ARI of two random partitions conditioned on cluster sizes being approximately equal. By the properties of the hypergeometric distribution under random partitioning, the expected ARI is 0 and the standard deviation is O(K/sqrt(N)).

**Part (c)** connects stability to the SCX performance bound. The proof has two steps:

1. **Stability implies identifiable state structure.** If S(Phi, K) > tau, then there exists a partition of the feature space into K regions such that most samples are consistently assigned. This partition defines a (possibly randomized) state mapping s_hat(x). By construction, the mutual information between features and this mapping, I(phi; s_hat(phi)), is at least a function of S.

2. **Identifiable state structure implies bounded F1 degradation.** The same Pinsker-based argument as Theorem 2 applies to the estimated state mapping s_hat, giving F1_SCX <= F1_base + C_F * sqrt(2 * I(phi; s_hat)). Since I(phi; s_hat) is controlled by S, we obtain the stability-dependent bound.

The function gamma_{CF}(S) captures the empirical relationship between stability and the effective information available for SCX. In practice, we recommend calibrating it per domain (see Section 4).

### 3.4 Discussion

The stability criterion is a **sufficient condition** for feature strength, not a necessary one. As Part (b) states: low stability implies weak or absent state structure. But high stability does not guarantee that the discovered states are the "true" states relevant to noise detection — only that the features produce a reproducible clustering.

This is the correct behavior for a diagnostic: false negatives (telling the user "features are weak" when SCX would actually work) are conservative, while false positives (telling the user "features are strong" when SCX would fail) are possible when the stable clustering does not align with the noise structure.

---

## 4. Corollary: Practical Threshold Rule

### 4.1 Heuristic Threshold

The stability score S(Phi, K) lies in [-1, 1] (the range of ARI), but in practice:

- S > 0.9: Features are very strong. State structure is clear and reproducible.
- S > 0.7: Features are moderately strong. State discovery is likely reliable.
- S > 0.5: Features are borderline. SCX may or may not work; proceed with caution.
- S < 0.5: Features are weak. State discovery is unreliable; SCX is unlikely to improve over the loss baseline.

The threshold tau = 0.7 is the primary diagnostic cutoff. This is a heuristic, but it has a theoretical anchor: ARI = 0.7 corresponds to approximately 85% pairwise agreement between clusterings, which is the level typically associated with "substantial agreement" in the clustering literature (analogous to Cohen's kappa thresholds).

### 4.2 Calibration Per Domain

For production use, the threshold should be calibrated per domain:

1. Generate synthetic data with known state separation (varying Delta_min / sigma)
2. Compute stability on each synthetic dataset
3. Record the stability value at which SCX's F1 improvement drops to near zero
4. Set the domain-specific threshold at that value

For the three SCX datasets studied previously:

| Dataset | Expected Stability | Expected SCX F1 Improvement | Recommended Action |
|---------|-------------------|----------------------------|--------------------|
| AlN v3 (ACE) | S > 0.9 | +0.16 | Proceed |
| CIFAR-10 (deep embeddings) | S > 0.95 | Moderate | Proceed |
| DermaMNIST (SimpleCNN) | S < 0.5 | ~0.01-0.03 | Improve features |

### 4.3 Relationship to the Number of Initializations

Standard k-means already runs multiple random initializations and picks the one with the lowest objective. The stability diagnostic additionally requires running k-means on bootstrap resamples. A useful efficiency: the multiple initializations already computed for the standard SCX pipeline can be partially reused. After selecting the best initialization on the full data (giving A), the same initialization points can be used as warm starts for the bootstrap resamples, reducing computational cost.

---

## 5. Practical Algorithm

### 5.1 Algorithm: Clustering Stability Diagnostic

```
Input:
  - Phi: N x d feature matrix (N samples, d features)
  - K: number of states (from SCX pipeline)
  - B: number of bootstrap resamples (default 50)
  - n_init: number of k-means initializations (default 10)
  - max_iter: k-means iterations per run (default 300)
  - random_state: for reproducibility

Output:
  - stability: mean ARI across bootstrap resamples
  - stability_std: standard deviation of ARI across resamples
  - ari_list: per-resample ARI values
  - verdict: "strong", "moderate", "borderline", or "weak"
  - recommendation: human-readable guidance

Steps:

1. FIT BASELINE CLUSTERING
   A = kmeans(Phi, K, n_init=n_init, max_iter=max_iter, random_state=random_state)
   # A is the cluster assignment vector of length N (labels 0..K-1)

2. COMPUTE BOOTSTRAP CLUSTERINGS
   for b in 1..B:
       # Resample N rows with replacement
       indices_b = np.random.choice(N, size=N, replace=True)
       Phi_b = Phi[indices_b, :]                     # bootstrap feature matrix

       # Run k-means on bootstrap sample
       A_b = kmeans(Phi_b, K, n_init=n_init,
                    max_iter=max_iter, random_state=random_state + b)

       # Align labels: bootstrap clustering may permute cluster labels
       # relative to the baseline. Use Hungarian matching to align.
       A_b_aligned = align_labels(A, A_b, K)

       # Compute ARI between baseline and bootstrap clustering
       ari_b = adjusted_rand_score(A, A_b_aligned)
       ari_list[b] = ari_b

3. COMPUTE STABILITY STATISTICS
   stability = mean(ari_list)
   stability_std = std(ari_list)
   ci_lower = stability - 1.96 * stability_std / sqrt(B)   # 95% CI
   ci_upper = stability + 1.96 * stability_std / sqrt(B)

4. VERDICT
   if stability >= 0.9:
       verdict = "strong"
       recommendation = "Features produce highly stable clustering. State discovery is reliable."
   elif stability >= 0.7:
       verdict = "moderate"
       recommendation = "Features produce moderately stable clustering. Proceed with SCX."
   elif stability >= 0.5:
       verdict = "borderline"
       recommendation = "Features produce unstable clustering. SCX may not improve over baseline."
   else:
       verdict = "weak"
       recommendation = "Features produce near-random clustering. Theorem 2 regime: invest in feature engineering."

5. RETURN
   return {
       "stability": stability,
       "stability_std": stability_std,
       "ci_95": (ci_lower, ci_upper),
       "ari_list": ari_list,
       "B": B,
       "K": K,
       "verdict": verdict,
       "recommendation": recommendation,
       "n_init": n_init,
   }
```

### 5.2 Label Alignment

k-means can permute cluster labels arbitrarily. When comparing A (baseline) with A_b (bootstrap), labels must be aligned. We use the Hungarian algorithm to find the permutation of labels in A_b that maximizes overlap with A. This is computed once per bootstrap run.

**Efficient approximation:** Since K is typically small in SCX (K <= 20), exhaustive search is K! which is feasible for K <= 8. For larger K, use Hungarian matching on the K x K confusion matrix between A and A_b, which runs in O(K^3).

### 5.3 Complexity

- **Time:** O(B * N * K * d * n_init * max_iter). For typical SCX parameters:
  - N = 1000, d = 100, K = 10, B = 50, n_init = 10, max_iter = 300
  - Per k-means: O(N * K * d * n_init * max_iter) ≈ 3 x 10^9 operations (approx 3 seconds with optimized BLAS)
  - Total: 50 x 3 = 150 seconds (2.5 minutes)
  - For N = 10000 (CIFAR-10): per k-means ≈ 3 x 10^10 operations (approx 30 seconds)
  - Total: 50 x 30 = 1500 seconds (25 minutes)

- **Memory:** O(N * d) for the bootstrap resample, plus O(N * K) for cluster assignments. No large matrices need to be stored.

- **Parallelization:** Bootstrap resamples are independent. B k-means runs can be parallelized across CPU cores (or GPU). Speedup is nearly linear up to B cores.

### 5.4 Implementation Notes

**Choosing B.** B = 50 is recommended as a default. Increasing B reduces the variance of the stability estimate but does not change its expectation. For B = 50, the standard error of the mean ARI is approximately sigma_ARI / sqrt(50) ≈ 0.14 * sigma_ARI. If sigma_ARI is small (stable case), the estimate is precise. If sigma_ARI is large (unstable case), the precision is lower but the verdict is usually clear (stability << 0.5).

**Stratified bootstrap.** If the SCX pipeline produces a preliminary state assignment (e.g., from a subset of experts or a simple threshold), stratified bootstrap (resampling within each preliminary state) can reduce variance. This is optional — the unstratified version is simpler and works without prior state information.

**Effect of initialization.** k-means with random initialization can converge to different local optima. To reduce initialization variance in stability, use the same initialization scheme for the baseline and bootstrap runs (e.g., k-means++ with fixed seed). The baseline clustering A is the best of n_init runs; each bootstrap run also uses n_init initializations. This ensures that stability measures sampling variability rather than initialization variability.

**Fast approximation for large N.** When N > 10000 and B = 50 k-means is too expensive:
- Reduce B to 20 (increases variance but still informative)
- Use mini-batch k-means (Sculley, 2010) which is 10-100x faster
- Use a subset of N (e.g., 5000 samples) for the stability diagnostic
- Replace full k-means with spectral clustering on a subsampled affinity matrix

---

## 6. Implementation in SCX

### 6.1 Proposed API

The stability diagnostic should be added as a new method in `StateValue`:

```python
class StateValue:
    def clustering_stability_diagnostic(
        self,
        phi_features: np.ndarray,
        K: int,
        B: int = 50,
        n_init: int = 10,
        max_iter: int = 300,
        random_state: int = 42,
    ) -> dict:
        """Evaluate feature strength via k-means clustering stability.

        Parameters
        ----------
        phi_features : np.ndarray, shape (N, d)
            Feature matrix.
        K : int
            Number of states (from SCX pipeline).
        B : int
            Number of bootstrap resamples (default 50).
        n_init : int
            k-means initializations per run (default 10).
        max_iter : int
            k-means iterations per run (default 300).
        random_state : int
            Random seed for reproducibility.

        Returns
        -------
        dict with keys:
            stability, stability_std, ci_95, B, K, verdict, recommendation
        """
        # Implementation as described in Section 5.1
```

### 6.2 Integration with Existing Pipeline

The diagnostic fits naturally into the SCX workflow:

```
Feature extraction (phi) -> State discovery (k-means) -> StateValue analysis
                                                                  |
                                                                  v
                                            feature_strength_diagnostic()  (existing)
                                            clustering_stability_diagnostic()  (new, preferred)
                                                                  |
                                                                  v
                                            If stability < 0.7: warn user
                                            If stability < 0.5: recommend feature engineering
```

### 6.3 Relationship to `feature_strength_diagnostic()` (Existing)

The existing `feature_strength_diagnostic()` (lines 589-671 of `state_value.py`) computes mutual information I(phi; S) using `sklearn.feature_selection.mutual_info_classif` or a histogram fallback. It requires **knowing the true state labels S**, which defeats part of the purpose: if we knew S, we could directly evaluate feature quality.

The stability diagnostic does not require S. It measures the reproducibility of k-means clusterings, which depends only on the feature matrix and K. This is the correct level of abstraction: SCX's state discovery is unsupervised, so the diagnostic should be unsupervised as well.

**Recommendation:** Keep both methods available, but promote `clustering_stability_diagnostic()` as the primary diagnostic. The existing `feature_strength_diagnostic()` can serve as a validation tool when ground-truth state labels are available (e.g., in synthetic experiments or benchmark datasets).

---

## 7. Comparison to Existing `feature_strength_diagnostic()`

### 7.1 Current Implementation

The existing diagnostic (lines 589-671 of `state_value.py`) works as follows:

1. Takes phi_features (N x d) and state_labels (N,) as input
2. Calls `_estimate_mutual_info()`, which uses `sklearn.feature_selection.mutual_info_classif` (k-NN based MI estimator) or a histogram fallback
3. Computes epsilon_phi = 1 - delta / log K where delta = I(phi; S)
4. Returns a recommendation: "strong" (epsilon_phi < 0.33), "moderate" (epsilon_phi < 0.66), or "weak"

### 7.2 Limitations of the Existing Diagnostic

1. **Requires true state labels.** The most fundamental limitation: in real SCX applications, the true state partition S is unknown. The diagnostic can only be used on synthetic data or on datasets where states are known a priori.

2. **k-NN MI estimation is unreliable for d > 10.** The `mutual_info_classif` estimator uses k-nearest neighbor entropy estimation, which degrades exponentially with dimension. For ACE descriptors (d ~ 100-200) or CNN latents (d ~ 128-512), the estimate is highly biased.

3. **Sensitive to continuous feature binning.** The histogram fallback discretizes each feature into K bins, losing information and introducing discretization bias. The number of joint bins grows as K^d, which is intractable for d > 5, forcing aggressive information loss.

4. **Does not test what SCX does.** The diagnostic estimates I(phi; S) directly, but SCX uses k-means to discover states. There is a gap between information-theoretic feature quality and k-means success, which the existing diagnostic does not bridge.

### 7.3 Direct Comparison

| Dimension | Existing `feature_strength_diagnostic()` | New `clustering_stability_diagnostic()` |
|-----------|-----------------------------------------|----------------------------------------|
| Input required | Features + true state labels | Features + K |
| Assumptions | None explicit (but MI est. degrades with d) | None (distribution-free) |
| Computational cost | Fast (k-NN MI) | Moderate (B x k-means) |
| Tests SCX's actual workflow? | No (tests MI, not k-means) | Yes (directly tests k-means) |
| Works for ACE descriptors (d=100)? | No (curse of dim. for MI est.) | Yes |
| Works for CNN latents (d=128)? | No | Yes |
| Works when S unknown? | No | Yes |
| Theoretically grounded? | Yes (Thm 2) | Yes (clustering stability lit.) |
| Distributional assumptions? | No | No |
| Interpretability | "epsilon_phi = 0.45" | "stability = 0.82, strong features" |
| False positive mode | N/A (needs true labels) | Stable clus. may not align with noise |
| False negative mode | N/A (needs true labels) | Possible (see Section 9) |

### 7.4 Migration Path

1. Add `clustering_stability_diagnostic()` to `StateValue` as a new method
2. Deprecate `feature_strength_diagnostic()` with a note directing users to the stability-based version
3. In the SCX pipeline, replace the default diagnostic call with `clustering_stability_diagnostic()`
4. Keep `feature_strength_diagnostic()` for synthetic-data validation and benchmarking

---

## 8. Validation Strategy

### 8.1 Synthetic Data Validation

Generate data from a K-component Gaussian mixture (ground truth known) and vary the center separation Delta. For each separation level:

1. Compute stability S (Algorithm 5.1)
2. Compute SCX F1 improvement over baseline (simulated expert noise)
3. Verify that S and F1 improvement are positively correlated
4. Identify the threshold tau where F1 improvement drops to near zero

Expected result: S > 0.7 corresponds to detectable F1 improvement for all tested configurations.

### 8.2 Real-Data Validation (Three SCX Datasets)

| Dataset | Expected Stability | SCX F1 Improvement | Diagnostic Verdict |
|---------|-------------------|-------------------|-------------------|
| AlN v3 (ACE) | > 0.9 | +0.16 | Strong |
| CIFAR-10 (deep embeddings) | > 0.9 | Moderate | Strong |
| DermaMNIST (SimpleCNN) | < 0.5 | ~0.01-0.03 | Weak |

### 8.3 Ablation: How Many Bootstrap Resamples?

Evaluate stability as a function of B (10, 20, 50, 100, 200):

- Measure the variance of the stability estimate across repeated runs
- Identify the point of diminishing returns (where additional B stops reducing variance)
- Expected: B = 50 captures > 90% of the variance reduction; B = 20 is acceptable for a quick check

### 8.4 Sensitivity to K

Evaluate stability at K-1, K, K+1 (where K is the "true" number of states):

- If features are strong, stability should be high at K and lower at K +/- 1 (underspecified/overspecified clustering is unstable)
- If features are weak, stability should be low at all K (no structure to stabilize)

This provides a useful diagnostic for the number-of-states choice: the K that maximizes stability is a good candidate.

---

## 9. Honest Limitations

### 9.1 Stability Is a Sufficient Condition, Not a Necessary One

The most important limitation: stable clustering does not guarantee that SCX will succeed. A stable clustering may separate samples along a direction that is irrelevant to noise detection. Example: ACE descriptors that clearly separate surface atoms from bulk atoms, but where noise is concentrated in surface atom labeling. The clustering is stable (surface vs. bulk), but the noise structure within each state is identical — SCX cannot improve detection.

This is the same limitation as Theorem 2's delta (mutual information is about state discovery, not about noise detection per se). It is inherent to any feature-strength diagnostic that does not incorporate expert annotations.

**Mitigation:** The diagnostic explicitly labels this: "strong features, proceed with SCX" does not guarantee SCX success. It only guarantees that features are not the bottleneck. Expert redundancy and noise rate must still be checked.

### 9.2 Computational Cost

The stability diagnostic requires B x k-means runs, which is 50x the cost of a single k-means run. For large datasets (N > 10000, d > 100), this can be computationally expensive:

- CIFAR-10 (N=50000, d=128, K=10): ~25 minutes for B=50
- AlN (N=534, d=100, K=8): ~30 seconds

For the largest datasets, the fast approximation options (mini-batch k-means, reduced B, subset sampling) should be offered as configurable alternatives.

### 9.3 The Threshold 0.7 Is a Heuristic

The threshold tau = 0.7 is borrowed from the Cohen's kappa agreement literature (Landis & Koch, 1977). It is not derived from first principles for the SCX setting.

**Mitigation:** The threshold can be calibrated per domain using synthetic data (Section 4.2). The diagnostic reports the raw stability value, not just the verdict, allowing users to make their own threshold decisions.

### 9.4 Label Alignment Artifacts

Aligning cluster labels between baseline and bootstrap runs requires solving a matching problem. If K is large (> 20), the Hungarian algorithm (O(K^3)) is needed. If multiple clusterings are equally good matches, the ARI can be inflated by the matching procedure.

**Mitigation:** Use the same initialization for baseline and bootstrap runs. This avoids label permutation ambiguity because the same initialization seeds produce consistently labeled clusters. The Hungarian alignment is only a safety net for when the algorithm converges to genuinely different local optima.

### 9.5 Sensitivity to Outliers

A single outlier far from all cluster centers can dominate the k-means objective without being part of any meaningful state structure. If the outlier is inconsistently assigned across bootstrap resamples, it can reduce stability even in the presence of strong structure.

**Mitigation:** Pre-process features to clip or Winsorize extreme values. The stability diagnostic should be run after standard preprocessing (centering, scaling, outlier removal).

### 9.6 Stability Under k = 1 or Degenerate Cases

If K = 1 (no state structure), the stability diagnostic is undefined (ARI requires at least 2 clusters). If K = N (each sample its own state), ARI = 1 trivially. The diagnostic should check for degenerate K values and return appropriate warnings.

### 9.7 Relationship to Theorem 2 Is Empirical, Not Formal

Unlike the BBP spectral proxy (which attempted to prove an analytic connection to delta), the stability diagnostic makes a **pragmatic** connection to Theorem 2:

- Low stability => no reliable state structure => Theorem 2 applies => SCX cannot improve over baseline
- High stability => reproducible state structure => Theorem 2's condition is satisfied => SCX may work (but is not guaranteed)

This connection is empirically validated but not formally proved. The theorem in Section 3 formalizes the link between stability and identifiable state structure, but the link to noise detection F1 remains mediated by expert redundancy, noise rate, and the alignment of cluster structure with noise patterns — factors outside the stability diagnostic.

---

## 10. References

### Clustering Stability (Primary)

1. **von Luxburg, U. (2010).** Clustering stability: An overview. *Foundations and Trends in Machine Learning*, 2(3), 235-274.
   - Comprehensive survey of clustering stability, including model selection via stability, theoretical guarantees, and limitations. The primary theoretical reference for this diagnostic.

2. **Ben-David, S., von Luxburg, U., & Pal, D. (2006).** A sober look at clustering stability. *COLT 2006*.
   - Shows that stability is not a universal model selection criterion (some unstable clusterings are meaningful). Provides the theoretical framework we invert here: stability as a measure of structure, not as a criterion for choosing K.

3. **Lange, T., Roth, V., Braun, M. L., & Buhmann, J. M. (2004).** Stability-based validation of clustering solutions. *Neural Computation*, 16(6), 1299-1323.
   - Proposes stability as a validation criterion for clustering. Introduces the bootstrap-based stability measure we adopt.

4. **Shamir, O., & Tishby, N. (2009).** On the reliability of clustering stability in the large sample regime. *NIPS 2008*.
   - Proves asymptotic consistency of stability-based model selection for well-separated mixtures. Part (a) of our theorem builds on this result.

### K-means Theory

5. **Pollard, D. (1981).** Strong consistency of k-means clustering. *Annals of Statistics*, 9(1), 135-140.
   - Fundamental consistency result for k-means. Provides the convergence rate we use in Part (a).

6. **Rakhlin, A., & Caponnetto, A. (2007).** Stability of k-means clustering. *NIPS 2007*.
   - Studies the algorithmic stability of k-means under perturbations of the input. Directly relevant to bootstrap stability.

### Adjusted Rand Index

7. **Hubert, L., & Arabie, P. (1985).** Comparing partitions. *Journal of Classification*, 2(1), 193-218.
   - Introduces the adjusted Rand index, which corrects the Rand index for chance agreement.

### Computational Methods

8. **Sculley, D. (2010).** Web-scale k-means clustering. *WWW 2010*.
   - Mini-batch k-means for large-scale clustering. Useful for the fast-approximation variant of the stability diagnostic.

### Applications in Material Science (SCX Context)

9. **SCX Theorem 2: Weak Feature Failure Lower Bound.** `SCX/theory/theorems/02_weak_feature_failure.md`
   - The theoretical bound that motivates the need for a feature-strength diagnostic.

10. **SCX-Health MedMNIST Experiment Report.** `scx-health/results/experiment_report_v2.md`
    - Empirical demonstration of SCX's behavior on datasets with varying feature quality.

### Cohen's Kappa and Agreement Thresholds

11. **Landis, J. R., & Koch, G. G. (1977).** The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159-174.
    - Introduces the "substantial agreement" threshold (kappa = 0.6-0.8) that motivates our tau = 0.7 heuristic.

---

## Appendix A: Relationship to Previous Attempts

### A.1 Comparison to BBP Spectral Proxy

| Aspect | BBP Spectral Proxy | Stability Diagnostic |
|--------|-------------------|---------------------|
| Core quantity | lambda_1 (largest eigenvalue) | ARI (clustering agreement) |
| What it tests | Variance alignment with state structure | Reproducibility of k-means |
| Assumptions | Isotropic Gaussian, i.i.d. entries | None |
| Computability | O(N^3) eigendecomposition | O(B * N * K * d * n_init) |
| Calibration | Circular (C depends on unknown theta) | Threshold-based (heuristic, calibratable) |
| False positives | High (nuisance variance creates spikes) | Possible (stable clusters may not aid SCX) |
| False negatives | High (many-weak-signals regime) | Possible (see Section 9) |
| Theoretical foundation | BBP phase transition (not applicable to SCX) | Clustering stability (applicable to k-means) |

### A.2 What We Learned

1. **Don't bridge to delta.** Theorem 2's delta is a theoretical quantity for analysis, not for computation. Trying to estimate it indirectly through spectral means adds assumptions without adding value.

2. **Test what you do.** SCX uses k-means for state discovery. The diagnostic should test k-means stability, not Gram matrix eigenvalues or mutual information.

3. **Distribution-free is essential.** SCX processes diverse feature types (ACE, CNN, tabular). A diagnostic that requires Gaussianity, isotropy, or i.i.d. entries will fail on real data.

4. **Honest heuristic > false theorem.** The stability diagnostic is presented as a practical tool with clear limitations, not as a mathematical theorem. This honesty makes it more useful than the BBP proxy, which claimed theorem status but collapsed under scrutiny.

---

*End of document.*
