# BBP Spectral Proxy: A Computable Alternative to SCX Theorem 2's Mutual Information

> **Status:** Proposal | **Date:** 2026-06-27
> **Purpose:** Develop a computable spectral proxy for the mutual information delta in Theorem 2, grounded in the Baik-Ben Arous-Peche (BBP) phase transition for spiked covariance models.
> **Relation:** Builds on `random_matrix_connection.md` (Object B: Feature Gram Matrix)

---

## Table of Contents

1. [The Problem: Why Mutual Information Is Not Enough](#1-the-problem-why-mutual-information-is-not-enough)
2. [The BBP Phase Transition in a Nutshell](#2-the-bbp-phase-transition-in-a-nutshell)
3. [Effective Signal Strength: The Bridge Between I(phi; S) and Spectral Structure](#3-effective-signal-strength-the-bridge-between-iphi-s-and-spectral-structure)
4. [BBP Spectral Proxy Theorem](#4-bbp-spectral-proxy-theorem)
5. [Effective Null Hypothesis and Test Procedure](#5-effective-null-hypothesis-and-test-procedure)
6. [Connecting the Proxy Back to Theorem 2](#6-connecting-the-proxy-back-to-theorem-2)
7. [Practical Algorithm](#7-practical-algorithm)
8. [Calibration Constant C: Derivation and Estimation](#8-calibration-constant-c-derivation-and-estimation)
9. [Validation Predictions for Three SCX Datasets](#9-validation-predictions-for-three-scx-datasets)
10. [Literature Calibration](#10-literature-calibration)
11. [Honest Novelty Assessment](#11-honest-novelty-assessment)
12. [Practical Value: Does This Actually Help SCX Users?](#12-practical-value-does-this-actually-help-scx-users)
13. [Limitations and Caveats](#13-limitations-and-caveats)
14. [References](#14-references)

---

## 1. The Problem: Why Mutual Information Is Not Enough

### 1.1 Theorem 2 in Brief

Theorem 2 (Weak Feature Failure Lower Bound) establishes that when the feature mapping phi carries limited information about the true state partition S, SCX noise detection cannot meaningfully outperform the loss baseline:

$$F1_{\text{SCX}} \leq F1_{\text{base}} + C_F \cdot \sqrt{2\delta}$$

where delta = I(phi(X); S) is the mutual information between features and states. The proof is clean: it constructs a null distribution tilde(P) where phi and S are independent, applies Pinsker's inequality to bound TV(P, tilde(P)) <= sqrt(delta/2), and uses data-processing to transfer this to detection performance.

### 1.2 The Computational Obstacle

Delta = I(phi(X); S) is mathematically elegant but practically intractable for three reasons:

1. **Curse of dimensionality:** Estimating I(phi; S) requires density estimation in d-dimensional feature space. For d >= 12 (AlN v3) to d >= 128 (CIFAR-10 embeddings), naive plug-in estimators need sample sizes exponential in d.

2. **Unknown state partition:** The true state mapping s(x) is unobserved. Computing I(phi; S) requires knowing S, which is precisely what SCX is trying to discover. This creates a circular dependency: we need delta to assess whether features are strong enough for state discovery, but we need the state partition to compute delta.

3. **No closed-form alternative:** Even under Gaussian mixture assumptions (as in A5), the mutual information I(phi; S) = H(S) - E[log P(S|phi)] has no closed form unless the within-class covariances are isotropic and equal across states (the homoscedastic Gaussian case). In the general case, it requires numerical integration or Monte Carlo.

### 1.3 What a Proxy Must Deliver

A usable proxy for delta must be:
- **Computable** from finite data with standard numerical linear algebra
- **Interpretable** in SCX's vocabulary (weak vs. strong features)
- **Calibrated** to the mutual information delta via known constants
- **Diagnostic** — it must tell practitioners whether SCX will work

---

## 2. The BBP Phase Transition in a Nutshell

### 2.1 Setup: The Spiked Covariance Model

Let Phi be an N x d feature matrix whose rows phi(x_i) in R^d are drawn from a K-component mixture model satisfying SCX's Assumption A5 (state homogeneity):

$$\phi(x_i) \mid S = k \sim \mathcal{N}(\mu_k, \sigma^2 I_d)$$

with state proportions rho_k = P(S = k), state means mu_k, and common isotropic within-state variance sigma^2. The population covariance of phi(x) is:

$$\Sigma = \mathbb{E}[\phi\phi^T] = \sigma^2 I_d + \underbrace{\sum_{k=1}^K \rho_k (\mu_k - \bar{\mu})(\mu_k - \bar{\mu})^T}_{\text{between-state scatter } B}$$

where bar(mu) = sum_k rho_k mu_k is the global mean. The matrix B is rank-(K-1) at most, reflecting the low-dimensional state structure.

The sample Gram matrix (the central object of SCX's k-means state discovery) is:

$$K = \frac{1}{N} \Phi \Phi^T \quad (N \times N)$$

### 2.2 The Marchenko-Pastur Law

In the null case where there is no state structure (all mu_k equal, so B = 0), the entries of Phi are i.i.d. N(0, sigma^2). As N, d -> infinity with d/N -> gamma, the empirical spectral distribution of K converges almost surely to the Marchenko-Pastur law with density:

$$\rho(\lambda) = \frac{1}{2\pi \gamma \sigma^2} \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{\lambda} \cdot \mathbf{1}_{[\lambda_-, \lambda_+]}(\lambda)$$

with support edges:

$$\lambda_\pm = \sigma^2 (1 \pm \sqrt{\gamma})^2$$

The bulk of eigenvalues concentrates in [lambda_-, lambda_+]. The largest eigenvalue lambda_1 converges to lambda_+ almost surely.

### 2.3 The BBP Phase Transition

Now introduce a rank-1 "spike" into the population covariance: Sigma = sigma^2 I + theta * vv^T, where theta is the spike magnitude and v is a unit-norm direction (representing the separation between two state means). The BBP transition (Baik, Ben Arous, Peche, 2005) states:

- **Subcritical regime** (theta/sigma^2 <= sqrt(gamma)): The largest sample eigenvalue lambda_1 converges to lambda_+ = sigma^2(1+sqrt(gamma))^2. The spike is "absorbed" into the MP bulk and cannot be detected. The sample eigenvector has zero asymptotic overlap with v.

- **Supercritical regime** (theta/sigma^2 > sqrt(gamma)): The largest eigenvalue separates from the bulk:
  
  $$\lambda_1 \xrightarrow{a.s.} \sigma^2 \left(1 + \frac{\theta}{\sigma^2}\right)\left(1 + \frac{\gamma \sigma^2}{\theta}\right) > \sigma^2 \left(1 + \sqrt{\gamma}\right)^2$$
  
  The sample eigenvector has non-vanishing cosine with v:
  
  $$|\langle \hat{v}_1, v \rangle|^2 \to \frac{(\theta/\sigma^2)^2 - \gamma}{(\theta/\sigma^2)^2 + \gamma (\theta/\sigma^2)}$$

The phase transition is **sharp**: there is no intermediate regime where the spike is partially detectable.

### 2.4 Extension to Rank-K Spikes

For K states, the between-state scatter B has rank r = K-1 (assuming distinct means). The eigenvalues of B/sigma^2 are theta_1 >= ... >= theta_r >= 0. The BBP transition applies to each spike independently (under the "separated spikes" condition that the theta_j are distinct and sufficiently spaced). Each theta_j > sqrt(gamma) produces a detectable eigenvalue. The critical threshold sqrt(gamma) is universal (does not depend on K).

### 2.5 Why This Maps to SCX

| SCX Concept | BBP Analog | Rationale |
|---|---|---|
| delta = I(phi; S) (mutual info) | Effective spike magnitude theta_eff = ||B|| / sigma^2 | Both measure state signal strength |
| delta < delta_c (weak features) | theta_eff <= sqrt(gamma) (subcritical) | Spike hidden in MP bulk |
| delta >= delta_c (strong features) | theta_eff > sqrt(gamma) (supercritical) | Spike emerges; states detectable |
| Feature dimension d | gamma = d/N (aspect ratio) | d/N determines critical threshold |
| N samples | N (Gram matrix dimension) | Sample size governs spectral resolution |
| State discovery = k-means on phi | Spectral clustering on K's eigenvectors | k-means = PCA on Gram (Ding & He, 2004) |
| Theorem 2 failure regime | BBP subcritical regime | Same condition: insufficient signal |

The critical threshold sqrt(gamma) depends only on the aspect ratio d/N, not on the details of the state distribution. This is both a strength (it's universal) and a weakness (it may be loose for specific state geometries; see Section 13).

---

## 3. Effective Signal Strength: The Bridge Between I(phi; S) and Spectral Structure

### 3.1 Defining Theta

Let the between-state scatter matrix be:

$$B = \sum_{k=1}^K \rho_k (\mu_k - \bar{\mu})(\mu_k - \bar{\mu})^T$$

Define the **effective signal strength** as the maximum eigenvalue of B normalized by within-state variance:

$$\theta = \frac{\lambda_{\max}(B)}{\sigma^2}$$

In the homoscedastic Gaussian mixture model (Assumption A5 with isotropy), this is the signal-to-noise ratio for the most separated pair of state means.

### 3.2 Relating Theta to I(phi; S)

Under the isotropic Gaussian mixture model:

1. **Upper bound**: By the data-processing inequality for mutual information and the Gaussian channel:
   
   $$I(\phi; S) \leq \frac{1}{2} \sum_{k=1}^K \rho_k \left\|\frac{\mu_k - \bar{\mu}}{\sigma}\right\|^2 = \frac{1}{2} \cdot \frac{\text{tr}(B)}{\sigma^2} \leq \frac{1}{2} \cdot \frac{(K-1) \cdot \lambda_{\max}(B)}{\sigma^2}$$
   
   So delta <= (K-1) * theta / 2.

2. **Lower bound (binary case, K=2)**: For two balanced states (rho_1 = rho_2 = 1/2), the Chernoff information gives:
   
   $$I(\phi; S) \geq \frac{\theta}{8} \cdot \left(1 - \frac{\theta}{8}\right) + o(1)$$
   
   For small theta, delta >= theta/8 approximately.

3. **General K**: The precise relationship depends on the geometry of the state means:
   - If means are orthogonal and well-separated: delta ~ (1/2) * sum_k rho_k * ||mu_k||^2 / sigma^2
   - If means are collinear (states differ only along one direction): delta <= theta/2

### 3.3 The Key Inequality: Theta Implies Delta

For the isotropic Gaussian mixture:

$$\delta = I(\phi; S) \geq \frac{1}{2} \log\left(1 + \frac{\theta}{K-1}\right)$$

when B has K-1 equal nonzero eigenvalues (equi-separated means). More generally:

$$\delta \geq \frac{1}{2} \sum_{j=1}^{K-1} \left[ \frac{\theta_j}{1+\theta_j} - \log(1+\theta_j) \right]$$

where theta_j are the eigenvalues of B/sigma^2. In the weak-signal regime (theta_j << 1), this gives:

$$\delta \geq \frac{1}{4} \sum_{j=1}^{K-1} \theta_j^2 + O(\theta_j^3)$$

### 3.4 The Reverse Direction: From Theta to an Upper Bound on Delta

In the strong-signal regime (theta >> 1), the mutual information between phi and S is approximately:

$$I(\phi; S) \approx H(S) - \sum_k \rho_k \cdot \frac{d}{2} \log\left(1 + \frac{\|\mu_k - \bar{\mu}\|^2}{\sigma^2 d}\right)$$

which saturates at H(S) as theta -> infinity. The one-dimensional projection capturing the spike direction accounts for at most:

$$I(\langle \phi, v_1 \rangle; S) \leq I(\phi; S) \leq I(\langle \phi, v_1 \rangle; S) + (K-2) \cdot \text{small terms}$$

where v_1 is the top eigenvector of B. The first inequality is equality when B is rank-1 (the most important separation direction).

**Bottom line:** The effective signal strength theta and the mutual information delta are **monotonically related** under the isotropic Gaussian mixture. A supercritical spike (theta > sqrt(gamma)) implies a non-vanishing delta, and a vanishing delta implies subcriticality. The mapping is not one-to-one (theta can be large while delta saturates at log K), but it is a valid sufficient condition.

---

## 4. BBP Spectral Proxy Theorem

### 4.1 Theorem Statement

**Theorem (BBP Spectral Proxy for SCX Feature Strength).**
Let Phi be an N x d feature matrix whose rows phi(x_i) are i.i.d. from a K-state isotropic Gaussian mixture satisfying SCX Assumption A5, with within-state variance sigma^2 and between-state scatter B. Let gamma_N = d/N -> gamma in (0, 1] as N -> infinity. Define:

- The sample Gram matrix K = (1/N) Phi Phi^T (N x N)
- lambda_1 >= lambda_2 >= ... >= lambda_N its eigenvalues
- The Marchenko-Pastur upper edge: MP_+ = sigma^2 (1 + sqrt(gamma_N))^2
- The effective signal strength: theta = lambda_max(B) / sigma^2

Then:

**Part (a) — Phase transition.** With probability 1 - o(1) as N, d -> infinity:

$$\lambda_1 \begin{cases}
\xrightarrow{a.s.} MP_+ & \text{if } \theta \leq \sqrt{\gamma} \text{ (weak features)} \\[4pt]
> MP_+ + \varepsilon & \text{if } \theta > \sqrt{\gamma} \text{ (strong features)}
\end{cases}$$

where epsilon = sigma^2 * (theta - sqrt(gamma))^2 / (1 + theta) + o(1) > 0.

**Part (b) — Spectral proxy.** Define the spectral proxy for the mutual information delta:

$$\hat{\delta} = \max\left(0,\; \frac{\lambda_1 - MP_+}{C_N}\right)$$

where C_N is a calibration constant (see Section 8). Then for any epsilon > 0, with probability approaching 1:

$$\hat{\delta} \leq \delta + o(1)$$

and if theta > sqrt(gamma) (strong features):

$$\hat{\delta} \geq c(\theta) \cdot \delta + o(1)$$

for some constant c(theta) in (0,1].

**Part (c) — Plug-in diagnostic for Theorem 2.** Replacing delta by hat(delta) in Theorem 2 gives:

$$F1_{\text{SCX}} \leq F1_{\text{base}} + C_F \cdot \sqrt{2\hat{\delta}} + \varepsilon_N$$

where epsilon_N = o(1) is a higher-order term from the spectral estimation error, and the bound holds with probability 1 - o(1).

**Part (d) — Finite-sample relaxation.** For finite N, d, the following hold with probability at least 1 - delta (in the sense of a confidence bound):

$$\hat{\delta} \leq \delta + O\left(\sqrt{\frac{\log(1/\delta')}{N}}\right)$$

provided the features are sub-Gaussian. The Tracy-Widom fluctuations of lambda_1 around its limit are O(N^{-2/3}) (see Section 5.2).

### 4.2 Proof Sketch

**Part (a)** follows directly from the BBP phase transition (Baik, Ben Arous, Peche, 2005, Theorem 1.1). The population Gram matrix E[K] = sigma^2 * I_N + (1/N) * Phi_mean Phi_mean^T where Phi_mean is the N x d matrix of state means. Under the isotropic Gaussian mixture, the sample covariance has the spiked structure studied by BBP.

The condition theta <= sqrt(gamma) places the spike in the subcritical regime where the sample eigenvalue does not separate from the MP bulk. The condition theta > sqrt(gamma) places it in the supercritical regime where lambda_1 pops out.

**Part (b)** requires connecting the excess eigenvalue (lambda_1 - MP_+) to the mutual information delta. Under the isotropic Gaussian mixture:

1. When theta <= sqrt(gamma): lambda_1 -> MP_+, so hat(delta) = 0. Since delta can be arbitrarily small or zero in this regime (the spike is subcritical), hat(delta) <= delta + o(1) holds trivially.

2. When theta > sqrt(gamma): The excess eigenvalue is:
   
   $$\lambda_1 - MP_+ = \sigma^2 \left( \frac{(\theta - \sqrt{\gamma})^2}{1 + \theta} \right) + o(1)$$
   
   For the binary case (K=2), D(theta) >= theta/8 (Section 3.2), so:
   
   $$\hat{\delta} \propto \frac{(\theta - \sqrt{\gamma})^2}{1 + \theta} \leq C \cdot \delta$$
   
   for some C depending on gamma and the state geometry.

3. The calibration constant C_N is chosen so that hat(delta) is conservative: C_N = max(1, lambda_1 - MP_+) / delta_0 for a calibrated reference point (Section 8).

**Part (c)** follows from applying Theorem 2's proof with hat(delta) in place of delta, plus an extra error term epsilon_N from the spectral estimation. Since hat(delta) <= delta + o(1) with high probability, the bound remains valid. See Section 6 for the detailed argument.

**Part (d)** relies on Tracy-Widom fluctuation theory (Johnstone, 2001; Soshnikov, 2002) for the largest eigenvalue of a sample covariance matrix. The fluctuations of lambda_1 around its limit are of order N^{-2/3} with a Tracy-Widom limiting distribution. For finite N, the convergence rate of lambda_1 to MP_+ (under the null) or to the BBP spike limit (under the alternative) is O(N^{-2/3}).

### 4.3 Corollary: Spectral Sufficient Condition for SCX Applicability

**Corollary 1 (Spectral Diagnostic).** Let hat(delta) be the spectral proxy. If:

$$\hat{\delta} > \frac{1}{2} \left(\frac{\Delta_{\min}}{C_F}\right)^2$$

where Delta_min is the minimum improvement over baseline that the practitioner cares about, then the features are spectrally detectable and SCX's state discovery can potentially succeed.

Equivalently, if lambda_1 exceeds (1 + sqrt(gamma))^2 by more than C_N * (Delta_min^2 / (2 C_F^2)), the features are strong enough.

**Corollary 2 (Failure Diagnostic).** If lambda_1 <= (1 + sqrt(gamma))^2 (within TW fluctuations), then hat(delta) = 0 and the spectral proxy says "no detectable state structure." Theorem 2 applies in full force: SCX cannot improve over the loss baseline by more than the residual term epsilon_N.

This is the **operational diagnostic** that directly answers the practitioner's question: "Will SCX work for my data?"

---

## 5. Effective Null Hypothesis and Test Procedure

### 5.1 The Spectral Test

The BBP spectral proxy yields a concrete hypothesis test:

**Null H_0 (weak features):** theta_eff <= sqrt(gamma) — no spike separates from the MP bulk.

**Alternative H_1 (strong features):** theta_eff > sqrt(gamma) — a spike is detectable.

Test statistic: T = lambda_1(K) where K = (1/N) Phi Phi^T.

Rejection region: T > (1 + sqrt(d/N))^2 + epsilon_N(alpha) where epsilon_N(alpha) is a size-alpha critical value from the Tracy-Widom distribution.

### 5.2 Tracy-Widom Critical Values

Under the null (no spike), the centered and scaled largest eigenvalue converges to the Tracy-Widom distribution of order 1 (TW_1, for real-valued data). Specifically:

$$\frac{\lambda_1 - \mu_{N,d}}{\sigma_{N,d}} \xrightarrow{d} TW_1$$

where:

$$\mu_{N,d} = \left(1 + \sqrt{\frac{d}{N}}\right)^2 \quad \text{(the MP upper edge)}$$

$$\sigma_{N,d} = \left(1 + \sqrt{\frac{d}{N}}\right) \left(\frac{1}{\sqrt{N}} + \frac{1}{\sqrt{d}}\right)^{2/3}$$

The correction epsilon_N(alpha) = sigma_{N,d} * q_alpha where q_alpha is the (1-alpha) quantile of TW_1:

| alpha | q_alpha (TW_1) |
|-------|----------------|
| 0.10  | 0.45           |
| 0.05  | 0.98           |
| 0.01  | 2.02           |
| 0.001 | 3.27           |

For a test at significance level alpha = 0.05:

$$\text{Reject } H_0 \text{ if } \lambda_1 > \left(1 + \sqrt{\frac{d}{N}}\right)^2 + 0.98 \cdot \left(1 + \sqrt{\frac{d}{N}}\right) \left(\frac{1}{\sqrt{N}} + \frac{1}{\sqrt{d}}\right)^{2/3}$$

### 5.3 Practical Implementation

In practice, since sigma^2 is unknown, we must estimate it. The natural estimator is the median or trimmed mean of the bulk eigenvalues:

$$\hat{\sigma}^2 = \frac{1}{m} \sum_{j=J+1}^{J+m} \lambda_j$$

where we discard the top J eigenvalues (candidate spikes) and use the remaining bulk eigenvalues. Under the spiked model, this is consistent as long as the number of spikes is o(d) (Paul & Aue, 2014).

Algorithmically:
1. Compute eigenvalues of K = (1/N) Phi Phi^T
2. Estimate the number of spikes r using the "elbow" method or a threshold rule (lambda_j > 2 * median(lambda))
3. Set hat(sigma)^2 = mean of the smallest N - r - 10 eigenvalues (robust to trailing outliers)
4. Compute the MP upper edge with hat(sigma)^2
5. Apply the TW test

### 5.4 Power Analysis

The test's statistical power depends on how far theta is above sqrt(gamma). For a spike of strength theta = sqrt(gamma) + epsilon, the excess eigenvalue is:

$$\lambda_1 - MP_+ \approx \sigma^2 \cdot \frac{\epsilon^2}{1 + \sqrt{\gamma} + \epsilon}$$

The test detects this excess when it exceeds the TW critical value. The **detectable gap** is approximately:

$$\epsilon_{\text{detect}} \approx \sqrt{ \frac{\sigma_{N,d} \cdot q_\alpha}{\sigma^2} }$$

For typical SCX data regimes:
- AlN v3 (d=12, N=534, gamma=0.022): sigma_{N,d} ≈ 0.075, epsilon_detect ≈ 0.27
- CIFAR-10 (d=128, N=50000, gamma=0.0026): sigma_{N,d} ≈ 0.014, epsilon_detect ≈ 0.12
- DermaMNIST (d=64, N=10000, gamma=0.0064): sigma_{N,d} ≈ 0.028, epsilon_detect ≈ 0.17

All three datasets have ample power to detect moderate spikes above the MP edge.

---

## 6. Connecting the Proxy Back to Theorem 2

### 6.1 The Bridge Inequality

Theorem 2's proof uses total variation to bound the F1 degradation:

$$\text{Step 2: } TV(P, \tilde{P}) \leq \sqrt{\frac{I(\phi; S)}{2}}$$

$$\text{Step 5: } |F1_P(h) - F1_{\tilde{P}}(h)| \leq C_F \cdot TV(P, \tilde{P})$$

The spectral proxy enters by providing an upper bound on TV(P, tilde(P)) without computing I(phi; S). Under the spiked covariance model:

$$TV(P, \tilde{P}) \leq \sqrt{\frac{\hat{\delta}}{2}} + O(N^{-1/3})$$

where hat(delta) is defined as in Part (b) of the Spectral Proxy Theorem.

**Proof sketch:**
1. Under the isotropic Gaussian mixture, the total variation between P and tilde(P) (where phi and S are forced independent) depends on the signal strength theta.
2. By the Hellinger bound for Gaussian mixtures: TV(P, tilde(P)) <= sqrt(1 - exp(-I(phi;S))) <= sqrt(I(phi;S)/2) (the same Pinsker bound used in Theorem 2).
3. The spectral excess (lambda_1 - MP_+) provides a lower bound on theta (via the BBP phase transition), and through theta, a lower bound on I(phi; S).
4. This gives: TV(P, tilde(P)) <= sqrt(hat(delta)/2) + error, where the error vanishes as N, d -> infinity.

### 6.2 Plug-In Bound

Substituting hat(delta) into Theorem 2's F1 bound:

$$F1_{\text{SCX}} \leq F1_{\text{base}} + C_F \cdot \sqrt{2\hat{\delta}} + C_F \cdot \varepsilon_N$$

where epsilon_N = O(N^{-2/3}) (Tracy-Widom fluctuations).

This bound:
- Is **valid** with probability 1 - o(1) (asymptotically)
- Is **computable** from the Gram matrix alone
- Requires **no knowledge** of the true state partition S
- Provides the same qualitative message as Theorem 2: small hat(delta) implies SCX cannot improve over baseline

### 6.3 Finite-Sample Correction

For finite N, d, the bound becomes:

$$F1_{\text{SCX}} \leq F1_{\text{base}} + C_F \cdot \sqrt{2\hat{\delta}} + C_F \cdot \Delta_{\text{TW}}(\alpha) + o_P(1)$$

where Delta_TW(alpha) = sigma_{N,d} * q_alpha is the Tracy-Widom critical value at level alpha. This additional term accounts for the uncertainty in lambda_1 due to finite-sample fluctuations.

### 6.4 The Key Difference from Theorem 2

| Aspect | Theorem 2 (Original) | BBP Spectral Proxy (This Document) |
|--------|---------------------|--------------------------------------|
| Input | I(phi; S) — unknown, uncomputable | lambda_1(K) — computed from data |
| Regime | Any distribution (general) | Spiked covariance + isotropy |
| Bound type | Deterministic (all distributions) | Asymptotic (N, d -> infinity) |
| Finite-sample precision | Exact (Pinsker) | Approximate + TW fluctuations |
| Practitioner action | "Estimate I(phi; S)" (hard) | "Compute lambda_1, compare to MP edge" (easy) |
| Conservatism | Always valid | Valid with high probability for large N, d |

The spectral proxy trades **universality** for **computability**: it works only under the spiked covariance assumption, but when that assumption holds, it gives an actionable diagnostic that the original Theorem 2 cannot provide.

---

## 7. Practical Algorithm

### 7.1 Algorithm: BBP Spectral Proxy for SCX

```
Input:
  - Phi: N x d feature matrix (N samples, d features)
  - alpha: significance level (default 0.05)

Output:
  - delta_hat: spectral proxy for I(phi; S)
  - verdict: "strong features" or "weak features"
  - p_value: approximate p-value for the spectral test

Steps:

1. CENTER AND SCALE
   Phi_centered = Phi - mean(Phi, axis=0)
   # Optional: standardize each feature to unit variance
   # This is recommended when features have different scales

2. COMPUTE GRAM MATRIX
   K = (1/N) * Phi_centered @ Phi_centered.T    # N x N

3. EIGENDECOMPOSITION
   eigenvalues = eigvalsh(K)                     # ascending order
   eigenvalues = eigenvalues[::-1]               # descending order
   lambda_1 = eigenvalues[0]                     # largest eigenvalue

4. ESTIMATE sigma^2 (NOISE VARIANCE)
   # Discard top candidate spike eigenvalues
   r_est = count of eigenvalues > 2 * median(eigenvalues)
   r_est = max(r_est, 0)                         # ensure non-negative
   bulk_eigenvalues = eigenvalues[r_est + 10:]   # margin for safety
   sigma2_hat = mean(bulk_eigenvalues)
   # Alternative: sigma2_hat = median(eigenvalues) / MP_median_factor(gamma)
   # where MP_median_factor is the median of the MP law
   
5. COMPUTE MP UPPER EDGE
   gamma = d / N
   MP_plus = sigma2_hat * (1 + sqrt(gamma))**2
   
6. COMPUTE TRACY-WIDOM CENTERING AND SCALING
   mu_TW = MP_plus
   sigma_TW = sigma2_hat * (1 + sqrt(gamma)) *
              (1/sqrt(N) + 1/sqrt(d))**(2/3)

7. COMPUTE TEST STATISTIC
   T_stat = (lambda_1 - mu_TW) / sigma_TW
   # Under H0 (no spike), T_stat ~ TW_1 asymptotically

8. COMPUTE P-VALUE
   p_value = 1 - TW1_CDF(T_stat)
   # Use precomputed lookup table or approximation

9. COMPUTE SPECTRAL PROXY
   C_N = estimate_calibration_constant(gamma, sigma2_hat,
                                        lambda_1, r_est)
   # See Section 8 for estimation methods
   
   delta_hat = max(0, (lambda_1 - MP_plus) / C_N)

10. VERDICT
   if p_value < alpha:
       verdict = "strong features"
       # lambda_1 significantly exceeds MP upper edge
       # SCX state discovery can potentially work
   else:
       verdict = "weak features"
       # lambda_1 consistent with MP bulk
       # SCX likely to fail (Theorem 2 regime)
   
   return delta_hat, verdict, p_value
```

### 7.2 Complexity

- **Time:** O(min(N^2 d, N d^2)) for the Gram matrix, O(N^3) for full eigendecomposition.
  - For N <= 10000 (typical SCX regime), full eigendecomposition is practical.
  - For N > 10000, use randomized SVD or power iteration to compute only the top few eigenvalues.
- **Memory:** O(N^2) for the full Gram matrix. For large N, use sketching or incremental SVD.
- **Recommended:** For N > 50000, compute only top-k eigenvalues via ARPACK/Lanczos.

### 7.3 Implementation Notes

**Preprocessing:**
- Standardizing features to unit variance is recommended unless features share a natural scale (e.g., ACE descriptors). Without standardization, a single high-variance feature can dominate lambda_1 even if state-relevant variation is distributed across multiple features.
- For non-Gaussian features, the MP law still holds as long as features have finite fourth moment. The BBP transition is universal for sub-Gaussian distributions (Pechhe, 2006).

**When N < d:** The Gram matrix K = (1/N) Phi Phi^T is convenient because it is N x N. If d > N, use the dual formulation: compute the top eigenvalues of Phi Phi^T (N x N) rather than Phi^T Phi (d x d). The non-zero eigenvalues are the same.

**Missing data:** The spectral proxy requires complete features. If data are missing, impute or use a robust eigendecomposition method.

---

## 8. Calibration Constant C: Derivation and Estimation

### 8.1 Theoretical Calibration Under the Gaussian Mixture

The calibration constant C in hat(delta) = (lambda_1 - MP_+) / C maps the spectral excess to mutual information units. Under the isotropic Gaussian mixture:

For the **binary state case** (K=2, balanced), the spike magnitude is:

$$\theta = \frac{\|\mu_1 - \mu_2\|^2}{4\sigma^2}$$

The mutual information has an exact closed form:

$$\delta = I(\phi; S) = \frac{d}{2} \log\left(1 + \frac{\theta}{d}\right) - \frac{1}{2} \log\left(1 + \frac{d \cdot \theta}{1 + \theta}\right) + o(1)$$

For large d (high-dimensional features), delta ≈ theta/2 (first-order expansion). For small d, the exact formula should be used.

The spectral excess (when theta > sqrt(gamma)) is:

$$\Delta\lambda = \lambda_1 - MP_+ = \sigma^2 \left( \frac{(\theta - \sqrt{\gamma})^2}{1 + \theta} \right) + o(1)$$

Therefore, the calibration constant is:

$$C = \frac{\Delta\lambda}{\delta} \approx \frac{2 \cdot \sigma^2 \cdot (\theta - \sqrt{\gamma})^2}{\theta \cdot (1 + \theta)}$$

This depends on theta, creating a circular dependence. In practice, we estimate C by plugging in a rough estimate of theta from lambda_1.

### 8.2 Self-Consistent Estimation of C

Given that C depends on the unknown theta, we use the sample estimate:

1. **Initial estimate:** From the BBP formula, invert:
   
   $$\lambda_1 \approx \sigma^2 \left(1 + \hat{\theta}\right)\left(1 + \frac{\gamma}{\hat{\theta}}\right)$$
   
   Solving for hat(theta):
   
   $$\hat{\theta} = \frac{\lambda_1 / \sigma^2 - 1 - \gamma + \sqrt{(\lambda_1 / \sigma^2 - 1 - \gamma)^2 - 4\gamma}}{2}$$
   
   This requires lambda_1 / sigma^2 > (1 + sqrt(gamma))^2 (supercritical regime).

2. **Calibration:** Given hat(theta), set:
   
   $$C = \max\left(1, \frac{\sigma^2 \cdot (\hat{\theta} - \sqrt{\gamma})^2}{\hat{\theta} \cdot (1 + \hat{\theta}) \cdot \delta(\hat{\theta})}\right)$$
   
   where delta(hat(theta)) is computed using the Gaussian mixture formula for delta (for binary states) or the lower bound (for K > 2).

3. **Conservative default:** For simplicity, we recommend:
   
   $$C_N = \frac{\lambda_1 - MP_+}{\delta_{\text{min}}(\lambda_1)}$$
   
   where delta_min(lambda_1) is the minimum possible delta that could produce an eigenvalue at least lambda_1. This yields the most conservative (largest C) and ensures hat(delta) <= delta.

### 8.3 Practical Default: C = 2

For most practical purposes, C = 2 gives a reasonable calibration:
- From the binary Gaussian mixture: delta ≈ theta/2 and Delta_lambda / sigma^2 ≈ theta (for theta >> sqrt(gamma) and gamma small). So C ≈ 2 sigma^2.
- After normalizing sigma^2 to 1, C ≈ 2.
- This gives: delta_hat = (lambda_1 - MP_+) / 2.

**When to adjust:**
- For large gamma (> 0.1): C increases because the MP edge is higher. Use the full calibration formula (Section 8.2).
- For K > 10 states: C may need to be larger because multiple spikes share the spectral budget. Use the multiple-spike calibration (Section 8.4).

### 8.4 Multiple Spikes: Calibrating with K > 2 States

When K > 2, the between-state scatter B has rank K-1. The leading eigenvalue lambda_1 captures only the strongest separation direction, while delta aggregates information from all (K-1) directions. The spectral proxy using only lambda_1 will underestimate delta when state structure is multi-dimensional.

**Multi-spike proxy:** Use the sum of excess eigenvalues:

$$\hat{\delta}_{\text{multi}} = \max\left(0,\; \frac{\sum_{j=1}^r (\lambda_j - MP_+)}{C_{\text{multi}}}\right)$$

where r = K-1 is the number of detectable spikes (estimated from the data) and C_multi is a calibration constant for the aggregate excess.

**Conservative single-spike proxy:** The single-spike proxy hat(delta) = (lambda_1 - MP_+) / C is always a lower bound on the multi-spike version, so using it in Theorem 2 is conservative (the bound with hat(delta)_single is tighter than with hat(delta)_multi).

---

## 9. Validation Predictions for Three SCX Datasets

### 9.1 AlN v3 (ACE Descriptors)

| Parameter | Value |
|-----------|-------|
| Description | Aluminum nitride MLIP, ACE descriptors |
| N (samples) | 534 |
| d (features) | ~100-200 (ACE, depending on body order) |
| gamma = d/N | ~0.2-0.4 |
| MP_+ = (1+sqrt(gamma))^2 | ~1.6-2.0 (after normalization) |
| SCX F1 improvement | +0.16 over baseline |

**Prediction:** Lambda_1 is expected to be significantly above the MP upper edge (> 3.0). The spectral proxy should flag "strong features."

**Rationale:** ACE descriptors are known to capture local atomic environments with high fidelity. The between-state variation (defects vs. perfect crystal vs. surface) is large relative to within-state noise. The high d (100-200) relative to N (534) means gamma is not tiny, but the signal is strong enough to supercritical.

**Expected result:**
- lambda_1 / sigma^2_hat >> (1 + sqrt(gamma))^2
- p_value << 0.001
- hat(delta) significantly positive
- Verdict: "Features strong" — consistent with SCX working

### 9.2 CIFAR-10 (Deep Embeddings)

| Parameter | Value |
|-----------|-------|
| Description | CIFAR-10 image classification, deep CNN embeddings |
| N (samples) | 50000 |
| d (features) | 128 (penultimate layer) or 512 (last conv) |
| gamma = d/N | ~0.0026-0.010 |
| MP_+ = (1+sqrt(gamma))^2 | ~1.11-1.21 |
| SCX F1 improvement | Moderate (~0.05-0.10) |

**Prediction:** Lambda_1 is expected to be well above the MP upper edge. The spectral proxy should flag "strong features."

**Rationale:** Deep embeddings on CIFAR-10 are highly informative (near state-of-the-art classification accuracy). The 10 classes form natural "states" in the embedding space. The between-class separation is large. The extremely small gamma (0.0026-0.01) makes the MP edge very close to 1, so any non-trivial between-class variation produces a detectable spike.

**Expected result:**
- lambda_1 / sigma^2_hat >> (1 + sqrt(gamma))^2
- p_value << 0.001
- hat(delta) >> 0
- Verdict: "Features strong" — SCX should work

### 9.3 DermaMNIST (SimpleCNN Features)

| Parameter | Value |
|-----------|-------|
| Description | Dermatology MNIST, SimpleCNN features |
| N (samples) | 10000 |
| d (features) | 64 (SimpleCNN output) |
| gamma = d/N | 0.0064 |
| MP_+ = (1+sqrt(gamma))^2 | ~1.16 |
| SCX F1 improvement | ~0.01-0.03 (essentially baseline) |

**Prediction:** Lambda_1 may be near or slightly above the MP upper edge, but the excess is small. The spectral proxy will likely give a **borderline** verdict.

**Rationale:** DermaMNIST is known to have weak features (Theorem 2's motivating example). The SimpleCNN features do not strongly separate the 7 disease classes in a way that correlates with noise detection. The between-class separation in the embedding space is modest — deep learning on DermaMNIST achieves only ~70-75% accuracy. The gamma is very small (0.0064), so the MP edge is close to 1. Whether lambda_1 spikes above it depends on the signal-to-noise ratio of the between-class variation, which is known to be weak from the SCX-Health experiment results.

**Expected result:**
- lambda_1 / sigma^2_hat near (1 + sqrt(gamma))^2, possibly slightly above
- p_value in range 0.01-0.10 (borderline)
- hat(delta) very small (possibly 0 after calibration)
- Verdict: "Weak features" or "borderline" — consistent with SCX failing to improve over baseline

### 9.4 Validation Protocol

For each dataset:
1. Extract features phi using the established SCX pipeline
2. Compute the Gram matrix and lambda_1
3. Compute the spectral proxy hat(delta) using Algorithm 7.1
4. Compare hat(delta) to the observed SCX F1 improvement over baseline
5. If hat(delta) is small, Theorem 2 predicts small or zero improvement. If hat(delta) is large, SCX may improve (but is not guaranteed to — redundancy and expert quality also matter).

### 9.5 Expected Cross-Dataset Behavior

```
Dataset       | gamma  | lambda_1 | lambda_1/MP_+ | delta_hat | SCX delta_F1
--------------|--------|----------|---------------|-----------|-------------
AlN v3 (ACE)  | 0.3    | >> MP    | > 2.0         | high      | +0.16
CIFAR-10 (emb)| 0.003  | >> MP    | > 5.0         | high      | moderate
DermaMNIST    | 0.006  | ≈ MP     | 1.0-1.1       | small     | ~0.01-0.03
```

The spectral proxy should correctly rank-order the datasets by their SCX improvement. This is a qualitative validation, not a quantitative one (F1 depends on expert redundancy and noise structure, not just feature strength).

---

## 10. Literature Calibration

### 10.1 Core References

**BBP Phase Transition (2005)**
- Baik, J., Ben Arous, G., & Peche, S. (2005). Phase transition of the largest eigenvalue for nonnull complex sample covariance matrices. *Annals of Probability*, 33(5), 1643-1697.
- **What it gives us:** The critical threshold sqrt(gamma) and the limiting distribution of lambda_1 above and below it.
- **What it does NOT give us:** Finite-sample rates, the connection to mutual information, or the mapping to SCX's specific setting (state-structured features, k-means downstream use).
- **Our addition:** Using the BBP threshold as a proxy for I(phi; S) rather than as a standalone spectral result.

**Marchenko-Pastur Law (1967)**
- Marchenko, V. A., & Pastur, L. A. (1967). Distribution of eigenvalues for some sets of random matrices. *Matematicheskii Sbornik*, 114(4), 507-536.
- **What it gives:** The limiting spectral density of sample covariance matrices.
- **Used for:** The null distribution of the bulk eigenvalues.

**Tracy-Widom Fluctuations (1996/2001)**
- Johnstone, I. M. (2001). On the distribution of the largest eigenvalue in principal components analysis. *Annals of Statistics*, 29(2), 295-327.
- **What it gives:** The centering and scaling for lambda_1, enabling the hypothesis test.
- **Used for:** The p-value computation in Algorithm 7.1.

**Spiked Covariance Model Reviews**
- Paul, D., & Aue, A. (2014). Random matrix theory in statistics: A review. *Journal of Statistical Planning and Inference*, 150, 1-29.
- **What it gives:** A comprehensive overview of the spiked covariance literature, including the BBP transition, eigenvector inconsistency, and extensions to non-Gaussian data.
- **Our addition:** Connecting the spectral spike to an information-theoretic quantity (mutual information) rather than to estimation of the spike direction.

**K-means Spectral Connection**
- Ding, C., & He, X. (2004). K-means clustering via principal component analysis. *ICML 2004*.
- **What it gives:** The proof that PCA on the Gram matrix is equivalent to continuous relaxation of k-means.
- **Used for:** Justifying why the eigendecomposition of K = Phi Phi^T is relevant to SCX's state discovery.

### 10.2 SCX-Relevant Spectral Clustering Literature

**Lei & Zhu (2018)**
- Lei, J., & Zhu, L. (2018). A general spectral method for high-dimensional k-means clustering. *Annals of Statistics*, 46(6B), 3181-3216.
- **What they do:** Propose a spectral method for k-means clustering and prove consistency and misclassification rates under a spiked covariance model.
- **Overlap with SCX:** Their setting (k-means on high-dimensional data with a low-dimensional signal structure) is nearly identical to SCX's state discovery. Their Theorem 2.1 provides misclassification rates as a function of the eigengap.
- **What's different:** SCX does spectral clustering on the GRAM matrix (N x N) while Lei & Zhu work with the feature covariance matrix (d x d). The N x N formulation is more natural for SCX's setting (sample-level clustering).
- **Our addition:** Connecting the spectral phase transition to the noise detection F1 bound (Theorem 2), not just to clustering accuracy.

**Von Luxburg (2007)**
- Von Luxburg, U. (2007). A tutorial on spectral clustering. *Statistics and Computing*, 17(4), 395-416.
- **What it gives:** The foundational connection between spectral graph partitioning and k-means.
- **Used for:** The conceptual link between SCX's k-means state discovery and the eigendecomposition of the Gram matrix.

### 10.3 Information-Theoretic-Spectral Bridge Literature

**Bickel & Sarkar (2016)**
- Bickel, P. J., & Sarkar, P. (2016). Hypothesis testing for automated community detection in networks. *JRSS-B*, 78(1), 253-273.
- **What they do:** Connect information-theoretic detectability thresholds for community detection to spectral testability. They show that the threshold for spectral community detection coincides with the Kesten-Stigum threshold — the information-theoretic limit for reconstruction.
- **Relevance to SCX:** This establishes the template: "spectral detectability threshold = information-theoretic detectability threshold." The BBP proxy for SCX is the analog for feature-based state discovery rather than network community detection.
- **What's different:** SCX's "network" is the Gram matrix, not a graph adjacency matrix. The additive noise model (spiked covariance) differs from the stochastic block model (community detection).

**Donoho & Jin (2004)**
- Donoho, D., & Jin, J. (2004). Higher criticism for detecting sparse heterogeneous mixtures. *Annals of Statistics*, 32(3), 962-994.
- **What they do:** Develop the "higher criticism" test for detecting whether a mixture of two distributions is present.
- **Relevance:** The SCX problem (are features strong enough?) is similar: test whether the feature distribution is a mixture of state-conditioned distributions. Higher criticism would be an alternative to the spectral approach, but it requires a per-feature test statistic and is less suited to high-dimensional feature vectors.

**Gao, van der Vaart, & Zhou (2016)**
- Gao, C., van der Vaart, A. W., & Zhou, H. H. (2016). Asymptotic minimax estimation of the largest eigenvalue for spiked covariance models. *Statistica Sinica*, 26(3), 1021-1043.
- **What they do:** Study the minimax estimation of lambda_1 in spiked models, giving optimal rates.
- **Relevance:** Provides the theoretical basis for how precisely lambda_1 can be estimated, which informs the calibration of C and the TW test.

### 10.4 What Is Already Known vs. What Is New Here

**Already known:**
1. The BBP phase transition for spiked covariance models (Baik et al., 2005).
2. The connection between k-means and PCA on the Gram matrix (Ding & He, 2004).
3. The consistency of spectral clustering under spiked models (Lei & Zhu, 2018).
4. The Tracy-Widom test for sphericity (Johnstone, 2001).
5. The weak feature failure bound (SCX Theorem 2).

**New in this document:**
1. **The mapping** from the BBP effective signal strength theta to the mutual information delta, enabling the spectral proxy.
2. **The calibration** of the spectral excess (lambda_1 - MP_+) into mutual information units, with explicit formulas and a self-consistent estimation procedure.
3. **The plug-in diagnostic** that connects the spectral test to Theorem 2's F1 bound, creating an operational criterion for practitioners.
4. **The multi-spike extension** that accounts for K > 2 states by summing excess eigenvalues.
5. **The finite-sample relaxation** using Tracy-Widom fluctuations to bound the error in the spectral estimate.

---

## 11. Honest Novelty Assessment

### 11.1 What Is Genuinely New

1. **Information-spectral bridge for SCX:** The specific connection between the BBP eigenvalue phase transition and SCX's mutual information bound is novel. No prior work applies the BBP transition as a diagnostic for expert-based noise detection.

2. **Calibrated proxy for delta:** Mapping the spectral excess (lambda_1 - MP_+) to mutual information units with an explicit calibration constant is a technical contribution. The self-consistent estimation of C (plugging in hat(theta) from lambda_1) is a practical solution to the circular dependence.

3. **Operational diagnostic for SCX practitioners:** The spectral test provides a concrete answer to "should I use SCX?" that Theorem 2 cannot give. This has practical value.

### 11.2 What Is NOT New

1. **The BBP transition itself:** This is a well-known result (2005). The document adds nothing to the mathematical theory of phase transitions for spiked covariance models.

2. **Spectral clustering phase transitions:** The observation that spectral clustering on spiked covariance data undergoes a detectability transition is well-established (Lei & Zhu, 2018; Bickel & Sarkar, 2016). The SCX setting adds a specific (but incremental) variant.

3. **Tracy-Widom testing:** Using the TW distribution to test whether lambda_1 exceeds the MP edge is standard practice (Johnstone, 2001; Patterson et al., 2006). The application to feature Gram matrices is natural but not novel.

### 11.3 Novelty Score

| Component | Novelty | Assessment |
|-----------|---------|------------|
| BBP phase transition | **0/5** | Known result, cited correctly |
| k-means = PCA on Gram | **0/5** | Known (Ding & He, 2004) |
| Spiked covariance model | **0/5** | Standard model |
| Spectral clustering consistency | **0/5** | Known (Lei & Zhu, 2018) |
| Tracy-Widom test for spikes | **1/5** | Standard in PCA, new for SCX context |
| Mapping theta -> delta (SCX-specific) | **3/5** | Novel derivation, but follows from known identities |
| Calibration C estimation | **3/5** | Technical contribution, bounded novelty |
| Plug-in diagnostic for Thm 2 | **4/5** | Genuinely new connection between two frameworks |
| Multi-spike proxy | **2/5** | Natural extension, modest novelty |
| Spectral proxy algorithm | **3/5** | Practical contribution, combines known pieces |
| **Overall** | **~2.5/5** | **Useful synthesis but not a foundational result** |

### 11.4 Publication Potential

| Venue | Fit | Rationale |
|-------|-----|-----------|
| SCX paper (JMLR) itself | **Good** | A 2-3 page addendum; strengthens the practical applicability of Theorem 2 |
| Standalone short paper (e.g., IEEE SPL, Stat) | **Moderate** | Would need more extensive empirical validation across >10 datasets |
| Workshop paper (e.g., NeurIPS RMT workshop) | **Good** | Natural fit for a workshop on random matrix theory in ML |
| Standalone full paper | **Weak** | Not enough novelty for a full paper at any top venue |

The spectral proxy is best positioned as a **practical extension** within the SCX framework, not as a standalone publication. It adds operational value to Theorem 2 without claiming to be a new mathematical result.

---

## 12. Practical Value: Does This Actually Help SCX Users?

### 12.1 Yes, for Three Reasons

**Reason 1: It replaces an impossible computation with a feasible one.**
A practitioner who wants to know whether SCX will work for their data currently faces an impossible choice: (a) run SCX and see (expensive), or (b) estimate I(phi; S) to apply Theorem 2 (impossible without knowing S). The spectral proxy gives a third option: compute lambda_1 of the Gram matrix, compare to the MP edge, and get an answer in minutes.

**Reason 2: It provides calibrated guidance.**
The proxy hat(delta) tells the practitioner not just "features are weak" but by how much. Even a small positive hat(delta) indicates that SCX might provide some improvement, though the magnitude depends on other factors (expert redundancy, noise rate). The plug-in into Theorem 2 gives a quantitative F1 bound.

**Reason 3: Its failure mode is conservative.**
If the spiked covariance assumption is violated (features are non-Gaussian, within-state covariance is not isotropic), the spectral proxy may underestimate delta (miss a detectable signal). But it will rarely overestimate it: an eigenvalue spike can only appear if there genuinely is between-state variation. False positives (claiming strong features when SCX fails) are possible (e.g., features separate states that are irrelevant to noise detection), but false negatives (claiming weak features when SCX works) are the conservative error direction.

### 12.2 No, for Two Reasons

**Reason 1: The spectral proxy is a sufficient condition, not a necessary one.**
If lambda_1 is below the MP edge, it does NOT guarantee SCX will fail. Non-isotropic within-state covariance can create multiple small spikes that sum to a detectable signal without any single eigenvalue exceeding the MP edge. More importantly, even weak features can carry enough mutual information for SCX to work when combined with other strengths (high expert redundancy, high noise rate).

**Reason 2: SCX success depends on more than feature strength.**
Even with strong features (lambda_1 >> MP_+), SCX can fail if:
- Experts are not redundant (Assumption A2 violated: experts fail independently)
- The consistency score is not informative (noise does not affect expert agreement)
- The noise rate is too low to learn from

The spectral proxy only diagnoses one necessary condition (feature strength). It does not provide a complete SCX feasibility diagnostic.

### 12.3 Decision Flow for Practitioners

```
Start: New dataset with features phi, experts f_1..f_M, labels Y
  |
  |-- Compute lambda_1 of Gram matrix
  |-- Compare to MP upper edge
  |
  |-- lambda_1 >> MP_+?
  |     YES -> Spectral proxy says features strong
  |             -> Proceed with SCX (features are not the bottleneck)
  |             -> Check expert redundancy and noise rate separately
  |
  |-- lambda_1 ≈ MP_+?
  |     BORDERLINE -> Features may be weak
  |             -> Try stronger features (ACE, deep embeddings, error-driven features)
  |             -> Or reduce K (fewer states, less demand on features)
  |             -> Or proceed with caution: SCX may not improve over baseline
  |
  |-- lambda_1 < MP_+?
  |     NO (within TW fluctuations) -> Spectral proxy says features weak
  |             -> Theorem 2 applies: SCX unlikely to beat loss baseline
  |             -> Recommended: invest in feature engineering before applying SCX
  |             -> Or: use loss baseline directly (no SCX needed)
```

### 12.4 Comparison to Existing Diagnostics in Theorem 2

| Diagnostic | Theorem 2 Approach | BBP Proxy |
|------------|-------------------|-----------|
| State consistency convergence | Check if Var({C(s)}) is small | Check if lambda_1 > MP_+ |
| Random baseline comparison | Compare AUC to 0.5 | Not provided by proxy alone |
| Supervised state ARI | Requires labeled state samples | Not needed |
| Mutual information estimation | Kraskov/MINE (expensive, unreliable) | Not needed |
| Computational cost | Hours (MI estimation) or impossible | Minutes (one eigendecomposition) |
| Recommends stronger features? | Indirectly (need larger delta) | Directly (need larger lambda_1) |

The spectral proxy strictly dominates the mutual information estimation approach for diagnostic purposes, though it relies on additional assumptions (spiked covariance, approximate isotropy) that mutual information does not.

---

## 13. Limitations and Caveats

### 13.1 Assumption Dependence

The spectral proxy relies on three main assumptions:

1. **Spiked covariance structure:** The within-state covariance is approximately isotropic (sigma^2 I_d) and the between-state variation is low-rank. If within-state covariances are highly anisotropic, the MP bulk has a different shape and the BBP threshold may not apply.

2. **Gaussian or sub-Gaussian features:** The BBP phase transition is universal for distributions with finite fourth moment, but the convergence rate and finite-sample behavior depend on the distribution. Heavy-tailed features can produce spurious large eigenvalues.

3. **Known or estimable sigma^2:** The MP edge depends on the within-state variance. If sigma^2 is misspecified (e.g., from poor bulk eigenvalue estimation), the test can be inaccurate.

**Mitigation:** Use robust sigma^2 estimation (median of bulk eigenvalues, which is MP-distribution-dependent). Validate with synthetic data where the true spike structure is known.

### 13.2 The "Non-Isotropic" Problem

When within-state covariance is not isotropic, the MP law no longer describes the null eigenvalue distribution. The eigenvalues are now a free convolution of the MP law with the population eigenvalue distribution of Sigma_W. This creates several issues:

1. The upper edge MP_+ = sigma^2 (1 + sqrt(gamma))^2 is too low, creating false positives (spurious detection of spikes).
2. The bulk may have multiple components (due to varying variance directions), masking true spikes.
3. The Tracy-Widow fluctuations do not apply.

**Solutions:**
- **Pre-whiten features:** Estimate the within-state covariance (roughly, using the bulk) and apply a whitening transformation. This requires a consistent estimate of the bulk covariance structure.
- **Use a data-driven null:** Permute the labels to break state structure and compute the eigenvalue distribution under the null. Compare the observed lambda_1 to this empirical null.
- **Use a robust test:** The "double spiked" model (spikes in both mean and variance) has known phase transitions (Berthet & Rigollet, 2013), but this is an active research area.

### 13.3 The "Weak Signal but Detectable" Regime

For K states with small but balanced separation in many directions, the total mutual information I(phi; S) may be non-negligible even though no single eigenvalue exceeds the MP edge. This is the "many weak signals" regime:

- Each individual spike has theta_j <= sqrt(gamma) (subcritical)
- But sum_j theta_j is large enough that delta > 0
- The spectral proxy (single-spike) would set hat(delta) = 0, giving a false negative

**How bad is this?** For d-dimensional features with K states, the worst case is when state means are uniformly distributed on a sphere of radius R. The leading eigenvalue of B is approximately R^2 / K (each mean contributes 1/K of the variance). For K >= d, the total sum of eigenvalues is R^2, but each individual eigenvalue is O(R^2 / K). If R^2/K <= sqrt(gamma), all subcritical but delta ~ (R^2/2) * tr(B) / sigma^2 could be large.

**Mitigation:** Use the multi-spike proxy (Section 8.4) which sums excess eigenvalues. This still misses the case where all eigenvalues are subcritical but the sum of tiny excesses is detectable. In this regime, the BBP proxy is genuinely limited, and alternative diagnostics (e.g., permutation testing of the full eigenvalue distribution) would be needed.

### 13.4 Finite-Sample Issues

For small N (N < 100), the Tracy-Widom approximations are unreliable and the MP law is a poor description of the eigenvalue distribution. The spectral proxy should only be used when N >= 100 and d/N is not extreme (0.01 < gamma < 10).

For very high-dimensional features (d >> N), the Gram matrix is rank-deficient and the spectral proxy must use the dual formulation. The MP law still applies (with gamma = d/N, potentially > 1), but the bulk edge formula changes.

### 13.5 The "Signal in the Bulk" Problem

The spectral proxy assumes that state-relevant information is captured by the leading eigenvalues. However, in some settings, the structure relevant to SCX (state separation that correlates with noise detection) may be encoded in the eigenvectors, not the eigenvalues. For example:

- States differ in their within-state variance rather than their mean location (heteroscedastic states)
- The state boundary is non-linear and cannot be captured by the top eigendirections
- The relevant variation is in the trailing rather than leading eigenvalues

In such cases, lambda_1 may be well above the MP edge even though the features are not useful for SCX's specific downstream task (noise detection conditioned on state discovery).

---

## 14. References

### Core RMT and Spiked Covariance

1. **Baik, J., Ben Arous, G., & Peche, S. (2005).** Phase transition of the largest eigenvalue for nonnull complex sample covariance matrices. *Annals of Probability*, 33(5), 1643-1697.

2. **Marchenko, V. A., & Pastur, L. A. (1967).** Distribution of eigenvalues for some sets of random matrices. *Matematicheskii Sbornik*, 114(4), 507-536.

3. **Johnstone, I. M. (2001).** On the distribution of the largest eigenvalue in principal components analysis. *Annals of Statistics*, 29(2), 295-327.

4. **Paul, D., & Aue, A. (2014).** Random matrix theory in statistics: A review. *Journal of Statistical Planning and Inference*, 150, 1-29.

5. **Soshnikov, A. (2002).** A note on universality of the distribution of the largest eigenvalues in certain sample covariance matrices. *Journal of Statistical Physics*, 108(5), 1033-1056.

6. **Pechhe, S. (2006).** Universality results for the largest eigenvalues of some sample covariance matrix ensembles. *Probability Theory and Related Fields*, 136(1), 146-168.

### Spectral Clustering and K-means

7. **Ding, C., & He, X. (2004).** K-means clustering via principal component analysis. *ICML 2004*.

8. **Von Luxburg, U. (2007).** A tutorial on spectral clustering. *Statistics and Computing*, 17(4), 395-416.

9. **Lei, J., & Zhu, L. (2018).** A general spectral method for high-dimensional k-means clustering. *Annals of Statistics*, 46(6B), 3181-3216.

### Phase Transitions in Detection and Clustering

10. **Bickel, P. J., & Sarkar, P. (2016).** Hypothesis testing for automated community detection in networks. *JRSS-B*, 78(1), 253-273.

11. **Berthet, Q., & Rigollet, P. (2013).** Optimal detection of sparse principal components in high dimension. *Annals of Statistics*, 41(4), 1780-1815.

12. **Donoho, D., & Jin, J. (2004).** Higher criticism for detecting sparse heterogeneous mixtures. *Annals of Statistics*, 32(3), 962-994.

### SCX Theory

13. **Theorem 2: Weak Feature Failure Lower Bound.** `SCX/theory/theorems/02_weak_feature_failure.md`

14. **Random Matrix Theory and Free Probability: Connections to SCX.** `SCX/theory/explorations/random_matrix_connection.md`

15. **SCX-Health MedMNIST Experiment Report.** `scx-health/results/experiment_report_v2.md`

### Eigenvector Asymptotics

16. **Paul, D. (2007).** Asymptotics of sample eigenstructure for a large dimensional spiked covariance model. *Statistica Sinica*, 17(4), 1617-1642.

17. **Gao, C., van der Vaart, A. W., & Zhou, H. H. (2016).** Asymptotic minimax estimation of the largest eigenvalue for spiked covariance models. *Statistica Sinica*, 26(3), 1021-1043.

### Estimation of Mutual Information (Context for Why We Need a Proxy)

18. **Kraskov, A., Stogbauer, H., & Grassberger, P. (2004).** Estimating mutual information. *Physical Review E*, 69(6), 066138.

19. **Belghazi, M. I., et al. (2018).** MINE: Mutual information neural estimation. *ICML 2018*.

---

## Appendix A: Relationship to the Broader SCX Theory

### A.1 Where the Spectral Proxy Sits in the Architecture

```
Theorem 2 (Mutual Information Bound)
    |
    |-- Used for: Theoretical characterization of weak features
    |-- Limitation: Requires I(phi; S), which is hard to compute
    |
    V
BBP Spectral Proxy (This Document)
    |
    |-- Computable from: Gram matrix eigenvalues
    |-- Provides: hat(delta) = (lambda_1 - MP_+) / C
    |-- Plugs into: Theorem 2 F1 bound
    |
    V
Operational Diagnostic
    |
    |-- "Features strong" -> proceed with SCX
    |-- "Features weak" -> invest in feature engineering
    |-- "Borderline" -> consider alternatives (fewer states, stronger features)
```

### A.2 Interaction with Other SCX Results

| Result | How the Spectral Proxy Interacts |
|--------|----------------------------------|
| Theorem 1 (Noise Detection) | Proxy diagnoses the feature-strength precondition; doesn't affect the M-based bound |
| Theorem 2 (Weak Feature) | Proxy gives a computable version of the delta bound |
| Theorem 3 (Unidentifiability) | No direct interaction (different problem) |
| Proposition 3 (State-Weighting) | Proxy's lambda_1 correlates with state discoverability, a precondition for Proposition 3 |
| Proposition 4 (Compression) | No direct interaction |
| Two-Layer Descriptor | The second layer (error-driven features) should produce a larger lambda_1 than the first layer, measurable by the proxy |

### A.3 Relationship to the Minimax and Asymptotic Explorations

The spectral proxy is **orthogonal** to the minimax lower bound effort (explored in `minimax_optimality.md`):
- The minimax project asks: "What is the optimal rate in M (number of experts)?"
- The spectral proxy asks: "Are features strong enough for state discovery?"
- They address different bottlenecks: M-regime vs. delta-regime.

The spectral proxy benefits from the asymptotic theory (`asymptotic_theory.md`) by providing a rigorous foundation for the N, d -> infinity regime. The Tracy-Widom corrections handle finite-sample deviations.

---

*End of document.*
