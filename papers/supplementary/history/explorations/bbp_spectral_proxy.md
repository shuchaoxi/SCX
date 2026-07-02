\section{BBP Spectral Proxy: A Computable Alternative to SCX Theorem 2's
Mutual
Information}<!-- label: bbp-spectral-proxy-a-computable-alternative-to-scx-theorem-2s-mutual-information -->

> **Status:** Proposal |{} **Date:** 2026-06-27
> **Purpose:** Develop a computable spectral proxy for the mutual
> information delta in Theorem 2, grounded in the Baik-Ben Arous-Peche
> (BBP) phase transition for spiked covariance models. **Relation:**
> Builds on `random\_matrix\_connection.md` (Object B: Feature Gram
> Matrix)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Table of Contents<!-- label: table-of-contents -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 
11. 
12. 
13. 
14. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{1. The Problem: Why Mutual Information Is Not
Enough}<!-- label: the-problem-why-mutual-information-is-not-enough -->

#### 1.1 Theorem 2 in Brief<!-- label: theorem-2-in-brief -->

Theorem 2 (Weak Feature Failure Lower Bound) establishes that when the
feature mapping phi carries limited information about the true state
partition S, SCX noise detection cannot meaningfully outperform the loss
baseline:

\[F1_{SCX} \leq F1_{base} + C_F \cdot \sqrt{2\delta}\]

where delta = I(phi(X); S) is the mutual information between features
and states. The proof is clean: it constructs a null distribution
tilde(P) where phi and S are independent, applies Pinsker's inequality
to bound TV(P, tilde(P)) \textless= sqrt(delta/2), and uses
data-processing to transfer this to detection performance.

\subsubsection{1.2 The Computational
Obstacle}<!-- label: the-computational-obstacle -->

Delta = I(phi(X); S) is mathematically elegant but practically
intractable for three reasons:

1. 
2. 
3. 

\subsubsection{1.3 What a Proxy Must
Deliver}<!-- label: what-a-proxy-must-deliver -->

A usable proxy for delta must be: - **Computable** from finite data
with standard numerical linear algebra - **Interpretable** in SCX's
vocabulary (weak vs.~strong features) - **Calibrated** to the
mutual information delta via known constants - **Diagnostic** ---
it must tell practitioners whether SCX will work

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. The BBP Phase Transition in a
Nutshell}<!-- label: the-bbp-phase-transition-in-a-nutshell -->

\subsubsection{2.1 Setup: The Spiked Covariance
Model}<!-- label: setup-the-spiked-covariance-model -->

Let Phi be an N x d feature matrix whose rows phi(x\_i) in R\^{}d are
drawn from a K-component mixture model satisfying SCX's Assumption A5
(state homogeneity):

\[\phi(x_i) \mid S = k \sim \mathcal{N}(\mu_k, \sigma^2 I_d)\]

with state proportions rho\_k = P(S = k), state means mu\_k, and common
isotropic within-state variance sigma\^{}2. The population covariance of
phi(x) is:

\[\Sigma = \mathbb{E}[\phi\phi^T] = \sigma^2 I_d + \underbrace{\sum_{k=1}^K \rho_k (\mu_k - \bar)(\mu_k - \bar)^T}_{between-state scatter  B}\]

where bar(mu) = sum\_k rho\_k mu\_k is the global mean. The matrix B is
rank-(K-1) at most, reflecting the low-dimensional state structure.

The sample Gram matrix (the central object of SCX's k-means state
discovery) is:

\[K = \frac{1}{N} \Phi \Phi^T \quad (N \times N)\]

\subsubsection{2.2 The Marchenko-Pastur
Law}<!-- label: the-marchenko-pastur-law -->

In the null case where there is no state structure (all mu\_k equal, so
B = 0), the entries of Phi are i.i.d. N(0, sigma\^{}2). As N, d
-\textgreater{} infinity with d/N -\textgreater{} gamma, the empirical
spectral distribution of K converges almost surely to the
Marchenko-Pastur law with density:

\[\rho(\lambda) = \frac{1}{2\pi \gamma \sigma^2} \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}} \cdot \mathbf{1}_{[\lambda_-, \lambda_+]}(\lambda)\]

with support edges:

\[\lambda_\pm = \sigma^2 (1 \pm \sqrt)^2\]

The bulk of eigenvalues concentrates in {[}lambda\_-, lambda\_+{]}. The
largest eigenvalue lambda\_1 converges to lambda\_+ almost surely.

\subsubsection{2.3 The BBP Phase
Transition}<!-- label: the-bbp-phase-transition -->

Now introduce a rank-1 ``spike'' into the population covariance: Sigma =
sigma\^{}2 I + theta * vv\^{}T, where theta is the spike magnitude and v
is a unit-norm direction (representing the separation between two state
means). The BBP transition (Baik, Ben Arous, Peche, 2005) states:

- 
- 

The phase transition is **sharp**: there is no intermediate regime
where the spike is partially detectable.

\subsubsection{2.4 Extension to Rank-K
Spikes}<!-- label: extension-to-rank-k-spikes -->

For K states, the between-state scatter B has rank r = K-1 (assuming
distinct means). The eigenvalues of B/sigma\^{}2 are theta\_1
\textgreater= ...{} \textgreater= theta\_r \textgreater= 0. The BBP
transition applies to each spike independently (under the ``separated
spikes'' condition that the theta\_j are distinct and sufficiently
spaced). Each theta\_j \textgreater{} sqrt(gamma) produces a detectable
eigenvalue. The critical threshold sqrt(gamma) is universal (does not
depend on K).

#### 2.5 Why This Maps to SCX<!-- label: why-this-maps-to-scx -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
SCX Concept
\end{minipage} & \begin{minipage}[b]
BBP Analog
\end{minipage} & \begin{minipage}[b]
Rationale
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
delta = I(phi; S) (mutual info) & Effective spike magnitude theta\_eff =
& 

delta \textless{} delta\_c (weak features) & theta\_eff \textless=
sqrt(gamma) (subcritical) & Spike hidden in MP bulk 

delta \textgreater= delta\_c (strong features) & theta\_eff
\textgreater{} sqrt(gamma) (supercritical) & Spike emerges; states
detectable 

Feature dimension d & gamma = d/N (aspect ratio) & d/N determines
critical threshold 

N samples & N (Gram matrix dimension) & Sample size governs spectral
resolution 

State discovery = k-means on phi & Spectral clustering on K's
eigenvectors & k-means = PCA on Gram (Ding \& He, 2004) 

Theorem 2 failure regime & BBP subcritical regime & Same condition:
insufficient signal 

\end{longtable}

The critical threshold sqrt(gamma) depends only on the aspect ratio d/N,
not on the details of the state distribution. This is both a strength
(it's universal) and a weakness (it may be loose for specific state
geometries; see Section 13).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Effective Signal Strength: The Bridge Between I(phi; S)
and Spectral
Structure}<!-- label: effective-signal-strength-the-bridge-between-iphi-s-and-spectral-structure -->

#### 3.1 Defining Theta<!-- label: defining-theta -->

Let the between-state scatter matrix be:

\[B = \sum_{k=1}^K \rho_k (\mu_k - \bar)(\mu_k - \bar)^T\]

Define the **effective signal strength** as the maximum eigenvalue
of B normalized by within-state variance:

\[\theta = \frac{\lambda_(B)}{\sigma^2}\]

In the homoscedastic Gaussian mixture model (Assumption A5 with
isotropy), this is the signal-to-noise ratio for the most separated pair
of state means.

\subsubsection{3.2 Relating Theta to I(phi;
S)}<!-- label: relating-theta-to-iphi-s -->

Under the isotropic Gaussian mixture model:

1. 
2. 
3. 

\subsubsection{3.3 The Key Inequality: Theta Implies
Delta}<!-- label: the-key-inequality-theta-implies-delta -->

For the isotropic Gaussian mixture:

\[\delta = I(\phi; S) \geq \frac{1}{2} \log\left(1 + \frac{K-1}\right)\]

when B has K-1 equal nonzero eigenvalues (equi-separated means). More
generally:

\[\delta \geq \frac{1}{2} \sum_{j=1}^{K-1} \left[ \frac{\theta_j}{1+\theta_j} - \log(1+\theta_j) \right]\]

where theta\_j are the eigenvalues of B/sigma\^{}2. In the weak-signal
regime (theta\_j \textless\textless{} 1), this gives:

\[\delta \geq \frac{1}{4} \sum_{j=1}^{K-1} \theta_j^2 + O(\theta_j^3)\]

\subsubsection{3.4 The Reverse Direction: From Theta to an Upper Bound
on
Delta}<!-- label: the-reverse-direction-from-theta-to-an-upper-bound-on-delta -->

In the strong-signal regime (theta \textgreater\textgreater{} 1), the
mutual information between phi and S is approximately:

\[I(\phi; S) \approx H(S) - \sum_k \rho_k \cdot \frac{d}{2} \log\left(1 + \frac{\|\mu_k - \bar\|^2}{\sigma^2 d}\right)\]

which saturates at H(S) as theta -\textgreater{} infinity. The
one-dimensional projection capturing the spike direction accounts for at
most:

\[I(\langle \phi, v_1 \rangle; S) \leq I(\phi; S) \leq I(\langle \phi, v_1 \rangle; S) + (K-2) \cdot small terms\]

where v\_1 is the top eigenvector of B. The first inequality is equality
when B is rank-1 (the most important separation direction).

**Bottom line:** The effective signal strength theta and the mutual
information delta are **monotonically related** under the isotropic
Gaussian mixture. A supercritical spike (theta \textgreater{}
sqrt(gamma)) implies a non-vanishing delta, and a vanishing delta
implies subcriticality. The mapping is not one-to-one (theta can be
large while delta saturates at log K), but it is a valid sufficient
condition.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4. BBP Spectral Proxy
Theorem}<!-- label: bbp-spectral-proxy-theorem -->

#### 4.1 Theorem Statement<!-- label: theorem-statement -->

**Theorem (BBP Spectral Proxy for SCX Feature Strength).** Let Phi
be an N x d feature matrix whose rows phi(x\_i) are i.i.d. from a
K-state isotropic Gaussian mixture satisfying SCX Assumption A5, with
within-state variance sigma\^{}2 and between-state scatter B. Let
gamma\_N = d/N -\textgreater{} gamma in (0, 1{]} as N -\textgreater{}
infinity. Define:

- 
- 
- 
- 

Then:

**Part (a) --- Phase transition.** With probability 1 - o(1) as N,
d -\textgreater{} infinity:

\[\lambda_1 \begin{cases}
\xrightarrow{a.s.} MP_+ & if  \theta \leq \sqrt  (weak features) 
> MP_+ + \varepsilon & if  \theta > \sqrt  (strong features)
\end{cases}\]

where epsilon = sigma\^{}2 * (theta - sqrt(gamma))\^{}2 / (1 + theta) +
o(1) \textgreater{} 0.

**Part (b) --- Spectral proxy.** Define the spectral proxy for the
mutual information delta:

\[\hat = \max\left(0,\; \frac{\lambda_1 - MP_+}{C_N}\right)\]

where C\_N is a calibration constant (see Section 8). Then for any
epsilon \textgreater{} 0, with probability approaching 1:

\[\hat \leq \delta + o(1)\]

and if theta \textgreater{} sqrt(gamma) (strong features):

\[\hat \geq c(\theta) \cdot \delta + o(1)\]

for some constant c(theta) in (0,1{]}.

**Part (c) --- Plug-in diagnostic for Theorem 2.** Replacing delta
by hat(delta) in Theorem 2 gives:

\[F1_{SCX} \leq F1_{base} + C_F \cdot \sqrt{2\hat} + \varepsilon_N\]

where epsilon\_N = o(1) is a higher-order term from the spectral
estimation error, and the bound holds with probability 1 - o(1).

**Part (d) --- Finite-sample relaxation.** For finite N, d, the
following hold with probability at least 1 - delta (in the sense of a
confidence bound):

\[\hat \leq \delta + O\left(\sqrt{\frac{\log(1/\delta')}{N}}\right)\]

provided the features are sub-Gaussian. The Tracy-Widom fluctuations of
lambda\_1 around its limit are O(N\^{}\{-2/3\}) (see Section 5.2).

#### 4.2 Proof Sketch<!-- label: proof-sketch -->

**Part (a)** follows directly from the BBP phase transition (Baik,
Ben Arous, Peche, 2005, Theorem 1.1). The population Gram matrix
E{[}K{]} = sigma\^{}2 * I\_N + (1/N) * Phi\_mean Phi\_mean\^{}T where
Phi\_mean is the N x d matrix of state means. Under the isotropic
Gaussian mixture, the sample covariance has the spiked structure studied
by BBP.

The condition theta \textless= sqrt(gamma) places the spike in the
subcritical regime where the sample eigenvalue does not separate from
the MP bulk. The condition theta \textgreater{} sqrt(gamma) places it in
the supercritical regime where lambda\_1 pops out.

**Part (b)** requires connecting the excess eigenvalue (lambda\_1 -
MP\_+) to the mutual information delta. Under the isotropic Gaussian
mixture:

1. 
2. 
3. 

**Part (c)** follows from applying Theorem 2's proof with
hat(delta) in place of delta, plus an extra error term epsilon\_N from
the spectral estimation. Since hat(delta) \textless= delta + o(1) with
high probability, the bound remains valid. See Section 6 for the
detailed argument.

**Part (d)** relies on Tracy-Widom fluctuation theory (Johnstone,
2001; Soshnikov, 2002) for the largest eigenvalue of a sample covariance
matrix. The fluctuations of lambda\_1 around its limit are of order
N\^{}\{-2/3\} with a Tracy-Widom limiting distribution. For finite N,
the convergence rate of lambda\_1 to MP\_+ (under the null) or to the
BBP spike limit (under the alternative) is O(N\^{}\{-2/3\}).

\subsubsection{4.3 Corollary: Spectral Sufficient Condition for SCX
Applicability}<!-- label: corollary-spectral-sufficient-condition-for-scx-applicability -->

**Corollary 1 (Spectral Diagnostic).** Let hat(delta) be the
spectral proxy. If:

\[\hat > \frac{1}{2} \left(\frac{\Delta_}{C_F}\right)^2\]

where Delta\_min is the minimum improvement over baseline that the
practitioner cares about, then the features are spectrally detectable
and SCX's state discovery can potentially succeed.

Equivalently, if lambda\_1 exceeds (1 + sqrt(gamma))\^{}2 by more than
C\_N * (Delta\_min\^{}2 / (2 C\_F\^{}2)), the features are strong
enough.

**Corollary 2 (Failure Diagnostic).** If lambda\_1 \textless= (1 +
sqrt(gamma))\^{}2 (within TW fluctuations), then hat(delta) = 0 and the
spectral proxy says ``no detectable state structure.'' Theorem 2 applies
in full force: SCX cannot improve over the loss baseline by more than
the residual term epsilon\_N.

This is the **operational diagnostic** that directly answers the
practitioner's question: ``Will SCX work for my data?''

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Effective Null Hypothesis and Test
Procedure}<!-- label: effective-null-hypothesis-and-test-procedure -->

#### 5.1 The Spectral Test<!-- label: the-spectral-test -->

The BBP spectral proxy yields a concrete hypothesis test:

**Null H\_0 (weak features):** theta\_eff \textless= sqrt(gamma)
--- no spike separates from the MP bulk.

**Alternative H\_1 (strong features):** theta\_eff \textgreater{}
sqrt(gamma) --- a spike is detectable.

Test statistic: T = lambda\_1(K) where K = (1/N) Phi Phi\^{}T.

Rejection region: T \textgreater{} (1 + sqrt(d/N))\^{}2 +
epsilon\_N(alpha) where epsilon\_N(alpha) is a size-alpha critical value
from the Tracy-Widom distribution.

\subsubsection{5.2 Tracy-Widom Critical
Values}<!-- label: tracy-widom-critical-values -->

Under the null (no spike), the centered and scaled largest eigenvalue
converges to the Tracy-Widom distribution of order 1 (TW\_1, for
real-valued data). Specifically:

\[\frac{\lambda_1 - \mu_{N,d}}{\sigma_{N,d}} \xrightarrow{d} TW_1\]

where:

\[\mu_{N,d} = \left(1 + \sqrt{\frac{d}{N}}\right)^2 \quad (the MP upper edge)\]

\[\sigma_{N,d} = \left(1 + \sqrt{\frac{d}{N}}\right) \left(\frac{1}{\sqrt{N}} + \frac{1}{\sqrt{d}}\right)^{2/3}\]

The correction epsilon\_N(alpha) = sigma\_\{N,d\} * q\_alpha where
q\_alpha is the (1-alpha) quantile of TW\_1:

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
alpha & q\_alpha (TW\_1) 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.10 & 0.45 

0.05 & 0.98 

0.01 & 2.02 

0.001 & 3.27 

\end{longtable}

For a test at significance level alpha = 0.05:

\[Reject  H_0  if  \lambda_1 > \left(1 + \sqrt{\frac{d}{N}}\right)^2 + 0.98 \cdot \left(1 + \sqrt{\frac{d}{N}}\right) \left(\frac{1}{\sqrt{N}} + \frac{1}{\sqrt{d}}\right)^{2/3}\]

\subsubsection{5.3 Practical
Implementation}<!-- label: practical-implementation -->

In practice, since sigma\^{}2 is unknown, we must estimate it. The
natural estimator is the median or trimmed mean of the bulk eigenvalues:

\[\hat^2 = \frac{1}{m} \sum_{j=J+1}^{J+m} \lambda_j\]

where we discard the top J eigenvalues (candidate spikes) and use the
remaining bulk eigenvalues. Under the spiked model, this is consistent
as long as the number of spikes is o(d) (Paul \& Aue, 2014).

Algorithmically: 1. Compute eigenvalues of K = (1/N) Phi Phi\^{}T 2.
Estimate the number of spikes r using the ``elbow'' method or a
threshold rule (lambda\_j \textgreater{} 2 * median(lambda)) 3. Set
hat(sigma)\^{}2 = mean of the smallest N - r - 10 eigenvalues (robust to
trailing outliers) 4. Compute the MP upper edge with hat(sigma)\^{}2 5.
Apply the TW test

#### 5.4 Power Analysis<!-- label: power-analysis -->

The test's statistical power depends on how far theta is above
sqrt(gamma). For a spike of strength theta = sqrt(gamma) + epsilon, the
excess eigenvalue is:

\[\lambda_1 - MP_+ \approx \sigma^2 \cdot \frac{\epsilon^2}{1 + \sqrt + \epsilon}\]

The test detects this excess when it exceeds the TW critical value. The
**detectable gap** is approximately:

\[\epsilon_{detect} \approx \sqrt{ \frac{\sigma_{N,d} \cdot q_\alpha}{\sigma^2} }\]

For typical SCX data regimes: - AlN v3 (d=12, N=534, gamma=0.022):
sigma\_\{N,d\} ≈ 0.075, epsilon\_detect ≈ 0.27 - CIFAR-10 (d=128,
N=50000, gamma=0.0026): sigma\_\{N,d\} ≈ 0.014, epsilon\_detect ≈ 0.12 -
DermaMNIST (d=64, N=10000, gamma=0.0064): sigma\_\{N,d\} ≈ 0.028,
epsilon\_detect ≈ 0.17

All three datasets have ample power to detect moderate spikes above the
MP edge.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{6. Connecting the Proxy Back to Theorem
2}<!-- label: connecting-the-proxy-back-to-theorem-2 -->

#### 6.1 The Bridge Inequality<!-- label: the-bridge-inequality -->

Theorem 2's proof uses total variation to bound the F1 degradation:

\[Step 2:  TV(P, \tilde{P}) \leq \sqrt{\frac{I(\phi; S)}{2}}\]

\[Step 5:  |F1_P(h) - F1_{\tilde{P}}(h)| \leq C_F \cdot TV(P, \tilde{P})\]

The spectral proxy enters by providing an upper bound on TV(P, tilde(P))
without computing I(phi; S). Under the spiked covariance model:

\[TV(P, \tilde{P}) \leq \sqrt{\frac{\hat}{2}} + O(N^{-1/3})\]

where hat(delta) is defined as in Part (b) of the Spectral Proxy
Theorem.

**Proof sketch:** 1. Under the isotropic Gaussian mixture, the
total variation between P and tilde(P) (where phi and S are forced
independent) depends on the signal strength theta. 2. By the Hellinger
bound for Gaussian mixtures: TV(P, tilde(P)) \textless= sqrt(1 -
exp(-I(phi;S))) \textless= sqrt(I(phi;S)/2) (the same Pinsker bound used
in Theorem 2). 3. The spectral excess (lambda\_1 - MP\_+) provides a
lower bound on theta (via the BBP phase transition), and through theta,
a lower bound on I(phi; S). 4. This gives: TV(P, tilde(P)) \textless=
sqrt(hat(delta)/2) + error, where the error vanishes as N, d
-\textgreater{} infinity.

#### 6.2 Plug-In Bound<!-- label: plug-in-bound -->

Substituting hat(delta) into Theorem 2's F1 bound:

\[F1_{SCX} \leq F1_{base} + C_F \cdot \sqrt{2\hat} + C_F \cdot \varepsilon_N\]

where epsilon\_N = O(N\^{}\{-2/3\}) (Tracy-Widom fluctuations).

This bound: - Is **valid** with probability 1 - o(1)
(asymptotically) - Is **computable** from the Gram matrix alone -
Requires **no knowledge** of the true state partition S - Provides
the same qualitative message as Theorem 2: small hat(delta) implies SCX
cannot improve over baseline

\subsubsection{6.3 Finite-Sample
Correction}<!-- label: finite-sample-correction -->

For finite N, d, the bound becomes:

\[F1_{SCX} \leq F1_{base} + C_F \cdot \sqrt{2\hat} + C_F \cdot \Delta_{TW}(\alpha) + o_P(1)\]

where Delta\_TW(alpha) = sigma\_\{N,d\} * q\_alpha is the Tracy-Widom
critical value at level alpha. This additional term accounts for the
uncertainty in lambda\_1 due to finite-sample fluctuations.

\subsubsection{6.4 The Key Difference from Theorem
2}<!-- label: the-key-difference-from-theorem-2 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1194}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3134}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5672}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
Theorem 2 (Original)
\end{minipage} & \begin{minipage}[b]
BBP Spectral Proxy (This Document)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Input & I(phi; S) --- unknown, uncomputable & lambda\_1(K) --- computed
from data 

Regime & Any distribution (general) & Spiked covariance + isotropy 

Bound type & Deterministic (all distributions) & Asymptotic (N, d
-\textgreater{} infinity) 

Finite-sample precision & Exact (Pinsker) & Approximate + TW
fluctuations 

Practitioner action & ``Estimate I(phi; S)'' (hard) & ``Compute
lambda\_1, compare to MP edge'' (easy) 

Conservatism & Always valid & Valid with high probability for large N,
d 

\end{longtable}

The spectral proxy trades **universality** for
**computability**: it works only under the spiked covariance
assumption, but when that assumption holds, it gives an actionable
diagnostic that the original Theorem 2 cannot provide.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Practical Algorithm<!-- label: practical-algorithm -->

\subsubsection{7.1 Algorithm: BBP Spectral Proxy for
SCX}<!-- label: algorithm-bbp-spectral-proxy-for-scx -->

\begin{verbatim}
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
\end{verbatim}

#### 7.2 Complexity<!-- label: complexity -->

- 
- 
- 

\item
  **Memory:** O(N\^{}2) for the full Gram matrix. For large N, use
  sketching or incremental SVD.
\item
  **Recommended:** For N \textgreater{} 50000, compute only top-k
  eigenvalues via ARPACK/Lanczos.
\end{itemize}

#### 7.3 Implementation Notes<!-- label: implementation-notes -->

**Preprocessing:** - Standardizing features to unit variance is
recommended unless features share a natural scale (e.g., ACE
descriptors). Without standardization, a single high-variance feature
can dominate lambda\_1 even if state-relevant variation is distributed
across multiple features. - For non-Gaussian features, the MP law still
holds as long as features have finite fourth moment. The BBP transition
is universal for sub-Gaussian distributions (Pechhe, 2006).

**When N \textless{} d:** The Gram matrix K = (1/N) Phi Phi\^{}T is
convenient because it is N x N. If d \textgreater{} N, use the dual
formulation: compute the top eigenvalues of Phi Phi\^{}T (N x N) rather
than Phi\^{}T Phi (d x d). The non-zero eigenvalues are the same.

**Missing data:** The spectral proxy requires complete features. If
data are missing, impute or use a robust eigendecomposition method.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{8. Calibration Constant C: Derivation and
Estimation}<!-- label: calibration-constant-c-derivation-and-estimation -->

\subsubsection{8.1 Theoretical Calibration Under the Gaussian
Mixture}<!-- label: theoretical-calibration-under-the-gaussian-mixture -->

The calibration constant C in hat(delta) = (lambda\_1 - MP\_+) / C maps
the spectral excess to mutual information units. Under the isotropic
Gaussian mixture:

For the **binary state case** (K=2, balanced), the spike magnitude
is:

\[\theta = \frac{\|\mu_1 - \mu_2\|^2}{4\sigma^2}\]

The mutual information has an exact closed form:

\[\delta = I(\phi; S) = \frac{d}{2} \log\left(1 + \frac{d}\right) - \frac{1}{2} \log\left(1 + \frac{d \cdot \theta}{1 + \theta}\right) + o(1)\]

For large d (high-dimensional features), delta ≈ theta/2 (first-order
expansion). For small d, the exact formula should be used.

The spectral excess (when theta \textgreater{} sqrt(gamma)) is:

\[\Delta\lambda = \lambda_1 - MP_+ = \sigma^2 \left( \frac{(\theta - \sqrt)^2}{1 + \theta} \right) + o(1)\]

Therefore, the calibration constant is:

\[C = \frac{\Delta\lambda} \approx \frac{2 \cdot \sigma^2 \cdot (\theta - \sqrt)^2}{\theta \cdot (1 + \theta)}\]

This depends on theta, creating a circular dependence. In practice, we
estimate C by plugging in a rough estimate of theta from lambda\_1.

\subsubsection{8.2 Self-Consistent Estimation of
C}<!-- label: self-consistent-estimation-of-c -->

Given that C depends on the unknown theta, we use the sample estimate:

1. 
2. 
3. 

\subsubsection{8.3 Practical Default: C =
2}<!-- label: practical-default-c-2 -->

For most practical purposes, C = 2 gives a reasonable calibration: -
From the binary Gaussian mixture: delta ≈ theta/2 and Delta\_lambda /
sigma\^{}2 ≈ theta (for theta \textgreater\textgreater{} sqrt(gamma) and
gamma small). So C ≈ 2 sigma\^{}2. - After normalizing sigma\^{}2 to 1,
C ≈ 2. - This gives: delta\_hat = (lambda\_1 - MP\_+) / 2.

**When to adjust:** - For large gamma (\textgreater{} 0.1): C
increases because the MP edge is higher. Use the full calibration
formula (Section 8.2). - For K \textgreater{} 10 states: C may need to
be larger because multiple spikes share the spectral budget. Use the
multiple-spike calibration (Section 8.4).

#### 8.4 Multiple Spikes: Calibrating with K \textgreater{ 2
States}<!-- label: multiple-spikes-calibrating-with-k-2-states -->

When K \textgreater{} 2, the between-state scatter B has rank K-1. The
leading eigenvalue lambda\_1 captures only the strongest separation
direction, while delta aggregates information from all (K-1) directions.
The spectral proxy using only lambda\_1 will underestimate delta when
state structure is multi-dimensional.

**Multi-spike proxy:** Use the sum of excess eigenvalues:

\[\hat_{multi} = \max\left(0,\; \frac{\sum_{j=1}^r (\lambda_j - MP_+)}{C_{multi}}\right)\]

where r = K-1 is the number of detectable spikes (estimated from the
data) and C\_multi is a calibration constant for the aggregate excess.

**Conservative single-spike proxy:** The single-spike proxy
hat(delta) = (lambda\_1 - MP\_+) / C is always a lower bound on the
multi-spike version, so using it in Theorem 2 is conservative (the bound
with hat(delta)\_single is tighter than with hat(delta)\_multi).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{9. Validation Predictions for Three SCX
Datasets}<!-- label: validation-predictions-for-three-scx-datasets -->

\subsubsection{9.1 AlN v3 (ACE
Descriptors)}<!-- label: aln-v3-ace-descriptors -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
Parameter & Value 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Description & Aluminum nitride MLIP, ACE descriptors 

N (samples) & 534 

d (features) & ~100-200 (ACE, depending on body order) 

gamma = d/N & ~0.2-0.4 

MP\_+ = (1+sqrt(gamma))\^{}2 & ~1.6-2.0 (after
normalization) 

SCX F1 improvement & +0.16 over baseline 

\end{longtable}

**Prediction:** Lambda\_1 is expected to be significantly above the
MP upper edge (\textgreater{} 3.0). The spectral proxy should flag
``strong features.''

**Rationale:** ACE descriptors are known to capture local atomic
environments with high fidelity. The between-state variation (defects
vs.~perfect crystal vs.~surface) is large relative to within-state
noise. The high d (100-200) relative to N (534) means gamma is not tiny,
but the signal is strong enough to supercritical.

**Expected result:** - lambda\_1 / sigma\^{}2\_hat
\textgreater\textgreater{} (1 + sqrt(gamma))\^{}2 - p\_value
\textless\textless{} 0.001 - hat(delta) significantly positive -
Verdict: ``Features strong'' --- consistent with SCX working

\subsubsection{9.2 CIFAR-10 (Deep
Embeddings)}<!-- label: cifar-10-deep-embeddings -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
Parameter & Value 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Description & CIFAR-10 image classification, deep CNN embeddings 

N (samples) & 50000 

d (features) & 128 (penultimate layer) or 512 (last conv) 

gamma = d/N & ~0.0026-0.010 

MP\_+ = (1+sqrt(gamma))\^{}2 & ~1.11-1.21 

SCX F1 improvement & Moderate (~0.05-0.10) 

\end{longtable}

**Prediction:** Lambda\_1 is expected to be well above the MP upper
edge. The spectral proxy should flag ``strong features.''

**Rationale:** Deep embeddings on CIFAR-10 are highly informative
(near state-of-the-art classification accuracy). The 10 classes form
natural ``states'' in the embedding space. The between-class separation
is large. The extremely small gamma (0.0026-0.01) makes the MP edge very
close to 1, so any non-trivial between-class variation produces a
detectable spike.

**Expected result:** - lambda\_1 / sigma\^{}2\_hat
\textgreater\textgreater{} (1 + sqrt(gamma))\^{}2 - p\_value
\textless\textless{} 0.001 - hat(delta) \textgreater\textgreater{} 0 -
Verdict: ``Features strong'' --- SCX should work

\subsubsection{9.3 DermaMNIST (SimpleCNN
Features)}<!-- label: dermamnist-simplecnn-features -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
Parameter & Value 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Description & Dermatology MNIST, SimpleCNN features 

N (samples) & 10000 

d (features) & 64 (SimpleCNN output) 

gamma = d/N & 0.0064 

MP\_+ = (1+sqrt(gamma))\^{}2 & ~1.16 

SCX F1 improvement & ~0.01-0.03 (essentially baseline) 

\end{longtable}

**Prediction:** Lambda\_1 may be near or slightly above the MP
upper edge, but the excess is small. The spectral proxy will likely give
a **borderline** verdict.

**Rationale:** DermaMNIST is known to have weak features (Theorem
2's motivating example). The SimpleCNN features do not strongly separate
the 7 disease classes in a way that correlates with noise detection. The
between-class separation in the embedding space is modest --- deep
learning on DermaMNIST achieves only ~70-75\% accuracy.
The gamma is very small (0.0064), so the MP edge is close to 1. Whether
lambda\_1 spikes above it depends on the signal-to-noise ratio of the
between-class variation, which is known to be weak from the SCX-Health
experiment results.

**Expected result:** - lambda\_1 / sigma\^{}2\_hat near (1 +
sqrt(gamma))\^{}2, possibly slightly above - p\_value in range 0.01-0.10
(borderline) - hat(delta) very small (possibly 0 after calibration) -
Verdict: ``Weak features'' or ``borderline'' --- consistent with SCX
failing to improve over baseline

#### 9.4 Validation Protocol<!-- label: validation-protocol -->

For each dataset: 1. Extract features phi using the established SCX
pipeline 2. Compute the Gram matrix and lambda\_1 3. Compute the
spectral proxy hat(delta) using Algorithm 7.1 4. Compare hat(delta) to
the observed SCX F1 improvement over baseline 5. If hat(delta) is small,
Theorem 2 predicts small or zero improvement. If hat(delta) is large,
SCX may improve (but is not guaranteed to --- redundancy and expert
quality also matter).

\subsubsection{9.5 Expected Cross-Dataset
Behavior}<!-- label: expected-cross-dataset-behavior -->

\begin{verbatim}
Dataset       | gamma  | lambda_1 | lambda_1/MP_+ | delta_hat | SCX delta_F1
--------------|--------|----------|---------------|-----------|-------------
AlN v3 (ACE)  | 0.3    | >> MP    | > 2.0         | high      | +0.16
CIFAR-10 (emb)| 0.003  | >> MP    | > 5.0         | high      | moderate
DermaMNIST    | 0.006  | ≈ MP     | 1.0-1.1       | small     | ~0.01-0.03
\end{verbatim}

The spectral proxy should correctly rank-order the datasets by their SCX
improvement. This is a qualitative validation, not a quantitative one
(F1 depends on expert redundancy and noise structure, not just feature
strength).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Literature Calibration<!-- label: literature-calibration -->

#### 10.1 Core References<!-- label: core-references -->

**BBP Phase Transition (2005)** - Baik, J., Ben Arous, G., \&
Peche, S. (2005). Phase transition of the largest eigenvalue for nonnull
complex sample covariance matrices. *Annals of Probability*, 33(5),
1643-1697. - **What it gives us:** The critical threshold
sqrt(gamma) and the limiting distribution of lambda\_1 above and below
it. - **What it does NOT give us:** Finite-sample rates, the
connection to mutual information, or the mapping to SCX's specific
setting (state-structured features, k-means downstream use). -
**Our addition:** Using the BBP threshold as a proxy for I(phi; S)
rather than as a standalone spectral result.

**Marchenko-Pastur Law (1967)** - Marchenko, V. A., \& Pastur, L.
A. (1967). Distribution of eigenvalues for some sets of random matrices.
*Matematicheskii Sbornik*, 114(4), 507-536. - **What it
gives:** The limiting spectral density of sample covariance matrices. -
**Used for:** The null distribution of the bulk eigenvalues.

**Tracy-Widom Fluctuations (1996/2001)** - Johnstone, I. M. (2001).
On the distribution of the largest eigenvalue in principal components
analysis. *Annals of Statistics*, 29(2), 295-327. - **What it
gives:** The centering and scaling for lambda\_1, enabling the hypothesis
test. - **Used for:** The p-value computation in Algorithm 7.1.

**Spiked Covariance Model Reviews** - Paul, D., \& Aue, A. (2014).
Random matrix theory in statistics: A review. *Journal of
Statistical Planning and Inference*, 150, 1-29. - **What it
gives:** A comprehensive overview of the spiked covariance literature,
including the BBP transition, eigenvector inconsistency, and extensions
to non-Gaussian data. - **Our addition:** Connecting the spectral
spike to an information-theoretic quantity (mutual information) rather
than to estimation of the spike direction.

**K-means Spectral Connection** - Ding, C., \& He, X. (2004).
K-means clustering via principal component analysis. *ICML 2004*. -
**What it gives:** The proof that PCA on the Gram matrix is
equivalent to continuous relaxation of k-means. - **Used for:**
Justifying why the eigendecomposition of K = Phi Phi\^{}T is relevant to
SCX's state discovery.

\subsubsection{10.2 SCX-Relevant Spectral Clustering
Literature}<!-- label: scx-relevant-spectral-clustering-literature -->

**Lei \& Zhu (2018)** - Lei, J., \& Zhu, L. (2018). A general
spectral method for high-dimensional k-means clustering. *Annals of
Statistics*, 46(6B), 3181-3216. - **What they do:** Propose a
spectral method for k-means clustering and prove consistency and
misclassification rates under a spiked covariance model. -
**Overlap with SCX:** Their setting (k-means on high-dimensional
data with a low-dimensional signal structure) is nearly identical to
SCX's state discovery. Their Theorem 2.1 provides misclassification
rates as a function of the eigengap. - **What's different:** SCX
does spectral clustering on the GRAM matrix (N x N) while Lei \& Zhu
work with the feature covariance matrix (d x d). The N x N formulation
is more natural for SCX's setting (sample-level clustering). -
**Our addition:** Connecting the spectral phase transition to the
noise detection F1 bound (Theorem 2), not just to clustering accuracy.

**Von Luxburg (2007)** - Von Luxburg, U. (2007). A tutorial on
spectral clustering. *Statistics and Computing*, 17(4), 395-416. -
**What it gives:** The foundational connection between spectral
graph partitioning and k-means. - **Used for:** The conceptual link
between SCX's k-means state discovery and the eigendecomposition of the
Gram matrix.

\subsubsection{10.3 Information-Theoretic-Spectral Bridge
Literature}<!-- label: information-theoretic-spectral-bridge-literature -->

**Bickel \& Sarkar (2016)** - Bickel, P. J., \& Sarkar, P. (2016).
Hypothesis testing for automated community detection in networks.
*JRSS-B*, 78(1), 253-273. - **What they do:** Connect
information-theoretic detectability thresholds for community detection
to spectral testability. They show that the threshold for spectral
community detection coincides with the Kesten-Stigum threshold --- the
information-theoretic limit for reconstruction. - **Relevance to
SCX:** This establishes the template: ``spectral detectability threshold
= information-theoretic detectability threshold.'' The BBP proxy for SCX
is the analog for feature-based state discovery rather than network
community detection. - **What's different:** SCX's ``network'' is
the Gram matrix, not a graph adjacency matrix. The additive noise model
(spiked covariance) differs from the stochastic block model (community
detection).

**Donoho \& Jin (2004)** - Donoho, D., \& Jin, J. (2004). Higher
criticism for detecting sparse heterogeneous mixtures. *Annals of
Statistics*, 32(3), 962-994. - **What they do:** Develop the
``higher criticism'' test for detecting whether a mixture of two
distributions is present. - **Relevance:** The SCX problem (are
features strong enough?) is similar: test whether the feature
distribution is a mixture of state-conditioned distributions. Higher
criticism would be an alternative to the spectral approach, but it
requires a per-feature test statistic and is less suited to
high-dimensional feature vectors.

**Gao, van der Vaart, \& Zhou (2016)** - Gao, C., van der Vaart, A.
W., \& Zhou, H. H. (2016). Asymptotic minimax estimation of the largest
eigenvalue for spiked covariance models. *Statistica Sinica*,
26(3), 1021-1043. - **What they do:** Study the minimax estimation
of lambda\_1 in spiked models, giving optimal rates. -
**Relevance:** Provides the theoretical basis for how precisely
lambda\_1 can be estimated, which informs the calibration of C and the
TW test.

\subsubsection{10.4 What Is Already Known vs.~What Is New
Here}<!-- label: what-is-already-known-vs.-what-is-new-here -->

**Already known:** 1. The BBP phase transition for spiked
covariance models (Baik et al., 2005). 2. The connection between k-means
and PCA on the Gram matrix (Ding \& He, 2004). 3. The consistency of
spectral clustering under spiked models (Lei \& Zhu, 2018). 4. The
Tracy-Widom test for sphericity (Johnstone, 2001). 5. The weak feature
failure bound (SCX Theorem 2).

**New in this document:** 1. **The mapping** from the BBP
effective signal strength theta to the mutual information delta,
enabling the spectral proxy. 2. **The calibration** of the spectral
excess (lambda\_1 - MP\_+) into mutual information units, with explicit
formulas and a self-consistent estimation procedure. 3. **The
plug-in diagnostic** that connects the spectral test to Theorem 2's F1
bound, creating an operational criterion for practitioners. 4.
**The multi-spike extension** that accounts for K \textgreater{} 2
states by summing excess eigenvalues. 5. **The finite-sample
relaxation** using Tracy-Widom fluctuations to bound the error in the
spectral estimate.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{11. Honest Novelty
Assessment}<!-- label: honest-novelty-assessment -->

#### 11.1 What Is Genuinely New<!-- label: what-is-genuinely-new -->

1. 
2. 
3. 

#### 11.2 What Is NOT New<!-- label: what-is-not-new -->

1. 
2. 
3. 

#### 11.3 Novelty Score<!-- label: novelty-score -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3438}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2812}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3750}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Component
\end{minipage} & \begin{minipage}[b]
Novelty
\end{minipage} & \begin{minipage}[b]
Assessment
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
BBP phase transition & **0/5** & Known result, cited correctly 

k-means = PCA on Gram & **0/5** & Known (Ding \& He, 2004) 

Spiked covariance model & **0/5** & Standard model 

Spectral clustering consistency & **0/5** & Known (Lei \& Zhu,
2018) 

Tracy-Widom test for spikes & **1/5** & Standard in PCA, new for
SCX context 

Mapping theta -\textgreater{} delta (SCX-specific) & **3/5** &
Novel derivation, but follows from known identities 

Calibration C estimation & **3/5** & Technical contribution,
bounded novelty 

Plug-in diagnostic for Thm 2 & **4/5** & Genuinely new connection
between two frameworks 

Multi-spike proxy & **2/5** & Natural extension, modest novelty 

Spectral proxy algorithm & **3/5** & Practical contribution,
combines known pieces 

**Overall** & **~2.5/5** & **Useful
synthesis but not a foundational result** 

\end{longtable}

#### 11.4 Publication Potential<!-- label: publication-potential -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3043}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2174}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4783}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Venue
\end{minipage} & \begin{minipage}[b]
Fit
\end{minipage} & \begin{minipage}[b]
Rationale
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
SCX paper (JMLR) itself & **Good** & A 2-3 page addendum;
strengthens the practical applicability of Theorem 2 

Standalone short paper (e.g., IEEE SPL, Stat) & **Moderate** &
Would need more extensive empirical validation across \textgreater10
datasets 

Workshop paper (e.g., NeurIPS RMT workshop) & **Good** & Natural
fit for a workshop on random matrix theory in ML 

Standalone full paper & **Weak** & Not enough novelty for a full
paper at any top venue 

\end{longtable}

The spectral proxy is best positioned as a **practical extension**
within the SCX framework, not as a standalone publication. It adds
operational value to Theorem 2 without claiming to be a new mathematical
result.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{12. Practical Value: Does This Actually Help SCX
Users?}<!-- label: practical-value-does-this-actually-help-scx-users -->

#### 12.1 Yes, for Three Reasons<!-- label: yes-for-three-reasons -->

**Reason 1: It replaces an impossible computation with a feasible
one.** A practitioner who wants to know whether SCX will work for their
data currently faces an impossible choice: (a) run SCX and see
(expensive), or (b) estimate I(phi; S) to apply Theorem 2 (impossible
without knowing S). The spectral proxy gives a third option: compute
lambda\_1 of the Gram matrix, compare to the MP edge, and get an answer
in minutes.

**Reason 2: It provides calibrated guidance.** The proxy hat(delta)
tells the practitioner not just ``features are weak'' but by how much.
Even a small positive hat(delta) indicates that SCX might provide some
improvement, though the magnitude depends on other factors (expert
redundancy, noise rate). The plug-in into Theorem 2 gives a quantitative
F1 bound.

**Reason 3: Its failure mode is conservative.** If the spiked
covariance assumption is violated (features are non-Gaussian,
within-state covariance is not isotropic), the spectral proxy may
underestimate delta (miss a detectable signal). But it will rarely
overestimate it: an eigenvalue spike can only appear if there genuinely
is between-state variation. False positives (claiming strong features
when SCX fails) are possible (e.g., features separate states that are
irrelevant to noise detection), but false negatives (claiming weak
features when SCX works) are the conservative error direction.

#### 12.2 No, for Two Reasons<!-- label: no-for-two-reasons -->

**Reason 1: The spectral proxy is a sufficient condition, not a
necessary one.** If lambda\_1 is below the MP edge, it does NOT guarantee
SCX will fail. Non-isotropic within-state covariance can create multiple
small spikes that sum to a detectable signal without any single
eigenvalue exceeding the MP edge. More importantly, even weak features
can carry enough mutual information for SCX to work when combined with
other strengths (high expert redundancy, high noise rate).

**Reason 2: SCX success depends on more than feature strength.**
Even with strong features (lambda\_1 \textgreater\textgreater{} MP\_+),
SCX can fail if: - Experts are not redundant (Assumption A2 violated:
experts fail independently) - The consistency score is not informative
(noise does not affect expert agreement) - The noise rate is too low to
learn from

The spectral proxy only diagnoses one necessary condition (feature
strength). It does not provide a complete SCX feasibility diagnostic.

\subsubsection{12.3 Decision Flow for
Practitioners}<!-- label: decision-flow-for-practitioners -->

\begin{verbatim}
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
\end{verbatim}

\subsubsection{12.4 Comparison to Existing Diagnostics in Theorem
2}<!-- label: comparison-to-existing-diagnostics-in-theorem-2 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2857}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4524}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2619}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Diagnostic
\end{minipage} & \begin{minipage}[b]
Theorem 2 Approach
\end{minipage} & \begin{minipage}[b]
BBP Proxy
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
State consistency convergence & Check if Var(\{C(s)\}) is small & Check
if lambda\_1 \textgreater{} MP\_+ 

Random baseline comparison & Compare AUC to 0.5 & Not provided by proxy
alone 

Supervised state ARI & Requires labeled state samples & Not needed 

Mutual information estimation & Kraskov/MINE (expensive, unreliable) &
Not needed 

Computational cost & Hours (MI estimation) or impossible & Minutes (one
eigendecomposition) 

Recommends stronger features? & Indirectly (need larger delta) &
Directly (need larger lambda\_1) 

\end{longtable}

The spectral proxy strictly dominates the mutual information estimation
approach for diagnostic purposes, though it relies on additional
assumptions (spiked covariance, approximate isotropy) that mutual
information does not.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 13. Limitations and Caveats<!-- label: limitations-and-caveats -->

#### 13.1 Assumption Dependence<!-- label: assumption-dependence -->

The spectral proxy relies on three main assumptions:

1. 
2. 
3. 

**Mitigation:** Use robust sigma\^{}2 estimation (median of bulk
eigenvalues, which is MP-distribution-dependent). Validate with
synthetic data where the true spike structure is known.

\subsubsection{13.2 The ``Non-Isotropic''
Problem}<!-- label: the-non-isotropic-problem -->

When within-state covariance is not isotropic, the MP law no longer
describes the null eigenvalue distribution. The eigenvalues are now a
free convolution of the MP law with the population eigenvalue
distribution of Sigma\_W. This creates several issues:

1. 
2. 
3. 

**Solutions:** - **Pre-whiten features:** Estimate the
within-state covariance (roughly, using the bulk) and apply a whitening
transformation. This requires a consistent estimate of the bulk
covariance structure. - **Use a data-driven null:** Permute the
labels to break state structure and compute the eigenvalue distribution
under the null. Compare the observed lambda\_1 to this empirical null. -
**Use a robust test:** The ``double spiked'' model (spikes in both
mean and variance) has known phase transitions (Berthet \& Rigollet,
2013), but this is an active research area.

\subsubsection{13.3 The ``Weak Signal but Detectable''
Regime}<!-- label: the-weak-signal-but-detectable-regime -->

For K states with small but balanced separation in many directions, the
total mutual information I(phi; S) may be non-negligible even though no
single eigenvalue exceeds the MP edge. This is the ``many weak signals''
regime:

- 
- 
- 

**How bad is this?** For d-dimensional features with K states, the
worst case is when state means are uniformly distributed on a sphere of
radius R. The leading eigenvalue of B is approximately R\^{}2 / K (each
mean contributes 1/K of the variance). For K \textgreater= d, the total
sum of eigenvalues is R\^{}2, but each individual eigenvalue is O(R\^{}2
/ K). If R\^{}2/K \textless= sqrt(gamma), all subcritical but delta
~{} (R\^{}2/2) * tr(B) / sigma\^{}2 could be large.

**Mitigation:** Use the multi-spike proxy (Section 8.4) which sums
excess eigenvalues. This still misses the case where all eigenvalues are
subcritical but the sum of tiny excesses is detectable. In this regime,
the BBP proxy is genuinely limited, and alternative diagnostics (e.g.,
permutation testing of the full eigenvalue distribution) would be
needed.

#### 13.4 Finite-Sample Issues<!-- label: finite-sample-issues -->

For small N (N \textless{} 100), the Tracy-Widom approximations are
unreliable and the MP law is a poor description of the eigenvalue
distribution. The spectral proxy should only be used when N
\textgreater= 100 and d/N is not extreme (0.01 \textless{} gamma
\textless{} 10).

For very high-dimensional features (d \textgreater\textgreater{} N), the
Gram matrix is rank-deficient and the spectral proxy must use the dual
formulation. The MP law still applies (with gamma = d/N, potentially
\textgreater{} 1), but the bulk edge formula changes.

\subsubsection{13.5 The ``Signal in the Bulk''
Problem}<!-- label: the-signal-in-the-bulk-problem -->

The spectral proxy assumes that state-relevant information is captured
by the leading eigenvalues. However, in some settings, the structure
relevant to SCX (state separation that correlates with noise detection)
may be encoded in the eigenvectors, not the eigenvalues. For example:

- 
- 
- 

In such cases, lambda\_1 may be well above the MP edge even though the
features are not useful for SCX's specific downstream task (noise
detection conditioned on state discovery).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 14. References<!-- label: references -->

\subsubsection{Core RMT and Spiked
Covariance}<!-- label: core-rmt-and-spiked-covariance -->

1. 
2. 
3. 
4. 
5. 
6. 

\subsubsection{Spectral Clustering and
K-means}<!-- label: spectral-clustering-and-k-means -->

1. 
2. 
3. 

\subsubsection{Phase Transitions in Detection and
Clustering}<!-- label: phase-transitions-in-detection-and-clustering -->

1. 
2. 
3. 

#### SCX Theory<!-- label: scx-theory -->

1. 
2. 
3. 

#### Eigenvector Asymptotics<!-- label: eigenvector-asymptotics -->

1. 
2. 

\subsubsection{Estimation of Mutual Information (Context for Why We Need
a
Proxy)}<!-- label: estimation-of-mutual-information-context-for-why-we-need-a-proxy -->

1. 
2. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Appendix A: Relationship to the Broader SCX
Theory}<!-- label: appendix-a-relationship-to-the-broader-scx-theory -->

\subsubsection{A.1 Where the Spectral Proxy Sits in the
Architecture}<!-- label: a.1-where-the-spectral-proxy-sits-in-the-architecture -->

\begin{verbatim}
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
\end{verbatim}

\subsubsection{A.2 Interaction with Other SCX
Results}<!-- label: a.2-interaction-with-other-scx-results -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.1905}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.8095}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Result
\end{minipage} & \begin{minipage}[b]
How the Spectral Proxy Interacts
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Theorem 1 (Noise Detection) & Proxy diagnoses the feature-strength
precondition; doesn't affect the M-based bound 

Theorem 2 (Weak Feature) & Proxy gives a computable version of the delta
bound 

Theorem 3 (Unidentifiability) & No direct interaction (different
problem) 

Proposition 3 (State-Weighting) & Proxy's lambda\_1 correlates with
state discoverability, a precondition for Proposition 3 

Proposition 4 (Compression) & No direct interaction 

Two-Layer Descriptor & The second layer (error-driven features) should
produce a larger lambda\_1 than the first layer, measurable by the
proxy 

\end{longtable}

\subsubsection{A.3 Relationship to the Minimax and Asymptotic
Explorations}<!-- label: a.3-relationship-to-the-minimax-and-asymptotic-explorations -->

The spectral proxy is **orthogonal** to the minimax lower bound
effort (explored in `minimax\_optimality.md`): - The minimax
project asks: ``What is the optimal rate in M (number of experts)?'' -
The spectral proxy asks: ``Are features strong enough for state
discovery?'' - They address different bottlenecks: M-regime
vs.~delta-regime.

The spectral proxy benefits from the asymptotic theory
(`asymptotic\_theory.md`) by providing a rigorous foundation for
the N, d -\textgreater{} infinity regime. The Tracy-Widom corrections
handle finite-sample deviations.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of document.*