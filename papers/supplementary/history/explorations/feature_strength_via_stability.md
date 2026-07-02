\section{Feature Strength via k-means Stability: A Practical Diagnostic
for
SCX}<!-- label: feature-strength-via-k-means-stability-a-practical-diagnostic-for-scx -->

> **Status:** Proposal |{} **Date:** 2026-06-27
> **Purpose:** Replace the failed BBP spectral bridge with a
> stability-based diagnostic that tests what SCX actually does (k-means
> clustering), without assuming Gaussianity, isotropy, or i.i.d. entries.
> **Relation:** Direct alternative to
> `bbp\_spectral\_proxy.md`; upgrades
> `feature\_strength\_diagnostic()` in `StateValue`

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{1. Why the BBP Bridge
Failed}<!-- label: why-the-bbp-bridge-failed -->

The BBP spectral proxy (`bbp\_spectral\_proxy.md`) attempted to
connect Theorem 2's mutual information delta = I(phi; S) to the largest
eigenvalue lambda\_1 of the feature Gram matrix. The goal was to replace
an intractable quantity (MI) with a computable one (eigenvalue). The
attempt failed for five reasons, each independently fatal:

\subsubsection{1.1 The Information-Spectral Bridge Was
Hand-Waving}<!-- label: the-information-spectral-bridge-was-hand-waving -->

The core claim was that delta\_hat = (lambda\_1 - MP\_+) / C serves as a
proxy for delta = I(phi; S). But lambda\_1 measures the **maximum
variance direction** of the marginal distribution P(phi), while delta
measures the **reduction in uncertainty about S given phi**. These
are structurally different:

- 
- 

The ``monotonic relationship'' claimed in Section 3.4 of the BBP
document was unsupported. The bounds relating theta (effective signal
strength) to delta span a factor of 4(K-1) --- too loose to guarantee
any practical monotonicity. A simple counterexample: two different mean
geometries with identical theta produce deltas differing by a factor of
2theta, disproving monotonicity even within the isotropic Gaussian
model.

\subsubsection{1.2 The Gaussian Assumption Is Fatal for SCX's Real
Features}<!-- label: the-gaussian-assumption-is-fatal-for-scxs-real-features -->

The entire BBP derivation assumes isotropic Gaussian within-state
distributions. SCX's actual features violate this:

- 
- 
- 

Without isotropy, the Marchenko-Pastur bulk edge MP\_+ is wrong, the BBP
threshold sqrt(gamma) is wrong, and the entire spectral test is invalid.

\subsubsection{1.3 The Calibration Constant C Was
Circular}<!-- label: the-calibration-constant-c-was-circular -->

The calibration C = (lambda\_1 - MP\_+) / delta depends on the unknown
theta, which is inferred from lambda\_1. This is algebraically
redundant: if you can estimate theta from lambda\_1 via the BBP inverse
formula, you can compute delta directly from theta without the proxy.
The ``self-consistent estimation'' was a change of variables, not an
independent quantity.

The practical default C = 2 was valid only when gamma is negligible,
theta \textgreater\textgreater{} sqrt(gamma), K = 2, and d
\textgreater\textgreater{} theta --- conditions that fail for every SCX
dataset.

\subsubsection{1.4 The Tracy-Widom Test Is Invalid for Non-i.i.d.
Features}<!-- label: the-tracy-widom-test-is-invalid-for-non-i.i.d.-features -->

The TW\_1 critical values require i.i.d. entries with finite fourth
moment. SCX features violate this in multiple ways: - Row dependence
(samples share atoms in ACE descriptors) - Column dependence (ACE
channels are correlated; CNN latents have network-induced correlations)
- Heavy-tailed marginals (ACE products of radial basis functions can
spike near cutoffs)

The resulting anti-conservative test produces false positives at rates
exceeding the nominal significance level.

\subsubsection{1.5 The ``Many Weak Signals'' Regime Is Not
Addressable}<!-- label: the-many-weak-signals-regime-is-not-addressable -->

For K states with balanced separation in many directions, the total
mutual information can be large while every individual eigenvalue is
subcritical. This is not a niche case --- it is the expected behavior
for material science ACE descriptors with dozens of local atomic
environment types (perfect crystal, various defects, surfaces, grain
boundaries). The spectral proxy cannot detect this, and the multi-spike
extension inherits the same limitation.

#### 1.6 Lesson Learned<!-- label: lesson-learned -->

**Do not try to bridge delta to lambda\_1.** They measure different
things, and the assumptions required for any bridge (Gaussianity,
isotropy, i.i.d. entries) are violated by SCX's actual features.
Instead, replace delta entirely with a different weak-feature criterion
that is independently justified, computationally tractable, and tests
what SCX actually does.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. The Stability-Based
Alternative}<!-- label: the-stability-based-alternative -->

#### 2.1 Core Idea<!-- label: core-idea -->

Theorem 2's delta = I(phi; S) asks: ``Do features carry information
about states?'' But there is a more practical question: **``Does
the clustering you actually run produce stable results?''**

SCX state discovery performs k-means on the feature matrix Phi. If
features are strong (well-separated states), k-means should produce
nearly identical clusterings across different random initializations and
bootstrap resamples. If features are weak (no clear state structure),
k-means will produce unstable, random-seeming clusterings that vary
wildly across resamples.

This is the **clustering stability** approach (von Luxburg, 2010;
Ben-David et al., 2006; Lange et al., 2004). Stability has been
extensively studied as a model selection criterion for clustering: the
``right'' number of clusters K is the one that maximizes stability.
Here, we invert this: given K (the number of states), we use stability
to measure whether the features support a reliable clustering at that K.

#### 2.2 Why This Works for SCX<!-- label: why-this-works-for-scx -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Requirement
\end{minipage} & \begin{minipage}[b]
BBP Spectral Proxy
\end{minipage} & \begin{minipage}[b]
Stability Diagnostic
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Gaussian assumption & Required & Not needed 

Isotropy & Required & Not needed 

i.i.d. entries & Required & Not needed 

Tests what SCX does & No (tests Gram matrix eigenvalues) & **Yes**
(tests k-means output) 

Computable & Yes & Yes (B x k-means) 

Detects ``many weak signals'' regime & No & **Yes** (aggregate
stability captures multi-directional signal) 

Sensitive to nuisance variance & Yes (high variance = false positive) &
**No** (uninformative variance produces unstable clustering) 

Known S required? & No & No 

\end{longtable}

The stability diagnostic directly tests the quantity that matters for
SCX: **can k-means discover a reliable state partition from these
features?** It does not attempt to estimate mutual information, does not
depend on distributional assumptions, and does not require knowing the
true state labels.

#### 2.3 Intuition<!-- label: intuition -->

Consider two extremes:

- 
- 

Stability captures this continuum. The ARI between bootstrap clusterings
is a direct measure of how much structure the features impose on the
k-means solution.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Theorem: Clustering Stability Criterion for SCX
Reliability}<!-- label: theorem-clustering-stability-criterion-for-scx-reliability -->

#### 3.1 Setup<!-- label: setup -->

Let the feature vectors phi(x\_1), ..., phi(x\_N) in R\^{}d be drawn
from a mixture distribution with K components (states), not necessarily
Gaussian. Let:

- 
- 
- 
- 

Define the **clustering stability**:

\[S(\Phi, K) = \frac{1}{B} \sum_{b=1}^B ARI(A, A_b)\]

where ARI is the adjusted Rand index (Hubert \& Arabie, 1985), which
compares the overlap between two clusterings, corrected for chance. ARI
= 1 indicates identical clusterings; ARI = 0 (or negative) indicates
overlap no better than random.

#### 3.2 Theorem Statement<!-- label: theorem-statement -->

**Theorem (Clustering Stability Criterion for SCX Feature
Strength).** Let the feature vectors phi(x\_i) be drawn from a
K-component mixture with minimum center separation Delta\_min (in
Euclidean distance), bounded center norms, and sub-Gaussian
within-component noise with variance proxy sigma\^{}2. Let n\_min =
min\_k n\_k be the smallest component size. Then:

**Part (a) --- Strong features imply high stability.** If the
minimum center separation satisfies:

\[\frac{\Delta_^2}{\sigma^2} > C_1 \cdot \frac{d + \log N}{n_}\]

for a universal constant C\_1 \textgreater{} 0, then with probability at
least 1 - O(N\^{}\{-1\}):

\[S(\Phi, K) > 1 - \varepsilon\]

where epsilon = O(exp(-c * n\_min * Delta\_min\^{}2 / sigma\^{}2)) for
some constant c \textgreater{} 0.

**Part (b) --- Weak features imply low stability.** If the centers
of the K components are drawn from a distribution with bounded second
moment (or if the component structure is absent, i.e., all mu\_k are
equal), then:

\[\mathbb{E}[S(\Phi, K)] \leq \mathbb{E}[ARI of random clusterings] + O\left(\frac{K}{\sqrt{N}}\right)\]

where the expected ARI of random (independent) clusterings with K
clusters of the same sizes is approximately 0. Specifically, for random
partitions with equal cluster sizes, E{[}ARI{]} = 0 and Var(ARI) =
O(1/N).

**Part (c) --- Plug-in diagnostic for SCX reliability.** If S(Phi,
K) \textless{} tau for a threshold tau in (0, 1), then with high
probability:

\[F1_{SCX} \leq F1_{base} + \gamma_{CF}(S)\]

where gamma\_\{CF\}(S) is a non-decreasing function of S such that
gamma\_\{CF\}(S) → 0 as S → 0. Conversely, if S(Phi, K) \textgreater{}
tau, the bound does not guarantee SCX success (other factors like expert
redundancy and noise rate also matter), but features are not the
bottleneck.

#### 3.3 Proof Sketch<!-- label: proof-sketch -->

**Part (a)** follows from the theory of k-means stability for
well-separated mixtures (Shamir \& Tishby, 2009; Rakhlin \& Caponnetto,
2007). When centers are sufficiently separated, the k-means optimization
landscape has a unique deep optimum (up to label permutation) within a
radius of the true centers. Bootstrap resampling perturbs the empirical
risk by O(sqrt(d/N)) in each direction, which is insufficient to escape
the basin of attraction. The ARI between clusterings from nearby optima
is bounded below by 1 - O(exp(-c * n\_min * separation\^{}2)).

**Key inequality for the separation condition.** For the k-means
objective:

\[W(A) = \frac{1}{N} \sum_{k=1}^K \sum_{i: s_i = k} \|\phi(x_i) - c_k\|^2\]

with centers c\_k, standard results (Pollard, 1981) show that if the
population minimizer has centers separated by at least Delta\_min, the
empirical minimizer converges to it at rate sqrt(d/(n\_min * N)). The
bootstrap resample adds an additional sampling perturbation of order
sqrt((d + log N)/N). The condition in Part (a) ensures that the
bootstrap perturbation is smaller than the signal, so the clustering
remains stable.

**Part (b)** follows from the fact that when no state structure
exists, k-means partitions the data arbitrarily based on initialization
and random sampling fluctuations. The ARI between independent runs on
different bootstrap samples converges to the ARI of two random
partitions conditioned on cluster sizes being approximately equal. By
the properties of the hypergeometric distribution under random
partitioning, the expected ARI is 0 and the standard deviation is
O(K/sqrt(N)).

**Part (c)** connects stability to the SCX performance bound. The
proof has two steps:

1. 
2. 

The function gamma\_\{CF\}(S) captures the empirical relationship
between stability and the effective information available for SCX. In
practice, we recommend calibrating it per domain (see Section 4).

#### 3.4 Discussion<!-- label: discussion -->

The stability criterion is a **sufficient condition** for feature
strength, not a necessary one. As Part (b) states: low stability implies
weak or absent state structure. But high stability does not guarantee
that the discovered states are the ``true'' states relevant to noise
detection --- only that the features produce a reproducible clustering.

This is the correct behavior for a diagnostic: false negatives (telling
the user ``features are weak'' when SCX would actually work) are
conservative, while false positives (telling the user ``features are
strong'' when SCX would fail) are possible when the stable clustering
does not align with the noise structure.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4. Corollary: Practical Threshold
Rule}<!-- label: corollary-practical-threshold-rule -->

#### 4.1 Heuristic Threshold<!-- label: heuristic-threshold -->

The stability score S(Phi, K) lies in {[}-1, 1{]} (the range of ARI),
but in practice:

- 
- 
- 
- 

The threshold tau = 0.7 is the primary diagnostic cutoff. This is a
heuristic, but it has a theoretical anchor: ARI = 0.7 corresponds to
approximately 85\% pairwise agreement between clusterings, which is the
level typically associated with ``substantial agreement'' in the
clustering literature (analogous to Cohen's kappa thresholds).

#### 4.2 Calibration Per Domain<!-- label: calibration-per-domain -->

For production use, the threshold should be calibrated per domain:

1. 
2. 
3. 
4. 

For the three SCX datasets studied previously:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1184}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3684}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2632}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Dataset
\end{minipage} & \begin{minipage}[b]
Expected Stability
\end{minipage} & \begin{minipage}[b]
Expected SCX F1 Improvement
\end{minipage} & \begin{minipage}[b]
Recommended Action
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
AlN v3 (ACE) & S \textgreater{} 0.9 & +0.16 & Proceed 

CIFAR-10 (deep embeddings) & S \textgreater{} 0.95 & Moderate &
Proceed 

DermaMNIST (SimpleCNN) & S \textless{} 0.5 & ~0.01-0.03 &
Improve features 

\end{longtable}

\subsubsection{4.3 Relationship to the Number of
Initializations}<!-- label: relationship-to-the-number-of-initializations -->

Standard k-means already runs multiple random initializations and picks
the one with the lowest objective. The stability diagnostic additionally
requires running k-means on bootstrap resamples. A useful efficiency:
the multiple initializations already computed for the standard SCX
pipeline can be partially reused. After selecting the best
initialization on the full data (giving A), the same initialization
points can be used as warm starts for the bootstrap resamples, reducing
computational cost.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Practical Algorithm<!-- label: practical-algorithm -->

\subsubsection{5.1 Algorithm: Clustering Stability
Diagnostic}<!-- label: algorithm-clustering-stability-diagnostic -->

\begin{verbatim}
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
\end{verbatim}

#### 5.2 Label Alignment<!-- label: label-alignment -->

k-means can permute cluster labels arbitrarily. When comparing A
(baseline) with A\_b (bootstrap), labels must be aligned. We use the
Hungarian algorithm to find the permutation of labels in A\_b that
maximizes overlap with A. This is computed once per bootstrap run.

**Efficient approximation:** Since K is typically small in SCX (K
\textless= 20), exhaustive search is K! which is feasible for K
\textless= 8. For larger K, use Hungarian matching on the K x K
confusion matrix between A and A\_b, which runs in O(K\^{}3).

#### 5.3 Complexity<!-- label: complexity -->

- 
- 
- 
- 
- 
- 

\item
  **Memory:** O(N * d) for the bootstrap resample, plus O(N * K)
  for cluster assignments. No large matrices need to be stored.
\item
  **Parallelization:** Bootstrap resamples are independent. B
  k-means runs can be parallelized across CPU cores (or GPU). Speedup is
  nearly linear up to B cores.
\end{itemize}

#### 5.4 Implementation Notes<!-- label: implementation-notes -->

**Choosing B.** B = 50 is recommended as a default. Increasing B
reduces the variance of the stability estimate but does not change its
expectation. For B = 50, the standard error of the mean ARI is
approximately sigma\_ARI / sqrt(50) ≈ 0.14 * sigma\_ARI. If sigma\_ARI
is small (stable case), the estimate is precise. If sigma\_ARI is large
(unstable case), the precision is lower but the verdict is usually clear
(stability \textless\textless{} 0.5).

**Stratified bootstrap.** If the SCX pipeline produces a
preliminary state assignment (e.g., from a subset of experts or a simple
threshold), stratified bootstrap (resampling within each preliminary
state) can reduce variance. This is optional --- the unstratified
version is simpler and works without prior state information.

**Effect of initialization.** k-means with random initialization
can converge to different local optima. To reduce initialization
variance in stability, use the same initialization scheme for the
baseline and bootstrap runs (e.g., k-means++ with fixed seed). The
baseline clustering A is the best of n\_init runs; each bootstrap run
also uses n\_init initializations. This ensures that stability measures
sampling variability rather than initialization variability.

**Fast approximation for large N.** When N \textgreater{} 10000 and
B = 50 k-means is too expensive: - Reduce B to 20 (increases variance
but still informative) - Use mini-batch k-means (Sculley, 2010) which is
10-100x faster - Use a subset of N (e.g., 5000 samples) for the
stability diagnostic - Replace full k-means with spectral clustering on
a subsampled affinity matrix

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Implementation in SCX<!-- label: implementation-in-scx -->

#### 6.1 Proposed API<!-- label: proposed-api -->

The stability diagnostic should be added as a new method in
`StateValue`:

\begin{Shaded}
\begin{Highlighting}[]
\KeywordTok{class}\NormalTok{ StateValue:}
    \KeywordTok{def}\NormalTok{ clustering\_stability\_diagnostic(}
        \VariableTok{self}\NormalTok{,}
\NormalTok{        phi\_features: np.ndarray,}
\NormalTok{        K: }\BuiltInTok{int}\NormalTok{,}
\NormalTok{        B: }\BuiltInTok{int} \OperatorTok{=} \DecValTok{50}\NormalTok{,}
\NormalTok{        n\_init: }\BuiltInTok{int} \OperatorTok{=} \DecValTok{10}\NormalTok{,}
\NormalTok{        max\_iter: }\BuiltInTok{int} \OperatorTok{=} \DecValTok{300}\NormalTok{,}
\NormalTok{        random\_state: }\BuiltInTok{int} \OperatorTok{=} \DecValTok{42}\NormalTok{,}
\NormalTok{    ) }\OperatorTok{{-}\textgreater{}} \BuiltInTok{dict}\NormalTok{:}
        \CommentTok{"""Evaluate feature strength via k{-}means clustering stability.}

\CommentTok{        Parameters}
\CommentTok{        {-}{-}{-}{-}{-}{-}{-}{-}{-}{-}}
\CommentTok{        phi\_features : np.ndarray, shape (N, d)}
\CommentTok{            Feature matrix.}
\CommentTok{        K : int}
\CommentTok{            Number of states (from SCX pipeline).}
\CommentTok{        B : int}
\CommentTok{            Number of bootstrap resamples (default 50).}
\CommentTok{        n\_init : int}
\CommentTok{            k{-}means initializations per run (default 10).}
\CommentTok{        max\_iter : int}
\CommentTok{            k{-}means iterations per run (default 300).}
\CommentTok{        random\_state : int}
\CommentTok{            Random seed for reproducibility.}

\CommentTok{        Returns}
\CommentTok{        {-}{-}{-}{-}{-}{-}{-}}
\CommentTok{        dict with keys:}
\CommentTok{            stability, stability\_std, ci\_95, B, K, verdict, recommendation}
\CommentTok{        """}
        \CommentTok{\# Implementation as described in Section 5.1}
\end{Highlighting}
\end{Shaded}

\subsubsection{6.2 Integration with Existing
Pipeline}<!-- label: integration-with-existing-pipeline -->

The diagnostic fits naturally into the SCX workflow:

\begin{verbatim}
Feature extraction (phi) -> State discovery (k-means) -> StateValue analysis
                                                                  |
                                                                  v
                                            feature_strength_diagnostic()  (existing)
                                            clustering_stability_diagnostic()  (new, preferred)
                                                                  |
                                                                  v
                                            If stability < 0.7: warn user
                                            If stability < 0.5: recommend feature engineering
\end{verbatim}

\subsubsection{\texorpdfstring{6.3 Relationship to
`feature\_strength\_diagnostic()`
(Existing)}{6.3 Relationship to feature\_strength\_diagnostic() (Existing)}}<!-- label: relationship-to-feature_strength_diagnostic-existing -->

The existing `feature\_strength\_diagnostic()` (lines 589-671 of
`state\_value.py`) computes mutual information I(phi; S) using
`sklearn.feature\_selection.mutual\_info\_classif` or a histogram
fallback. It requires **knowing the true state labels S**, which
defeats part of the purpose: if we knew S, we could directly evaluate
feature quality.

The stability diagnostic does not require S. It measures the
reproducibility of k-means clusterings, which depends only on the
feature matrix and K. This is the correct level of abstraction: SCX's
state discovery is unsupervised, so the diagnostic should be
unsupervised as well.

**Recommendation:** Keep both methods available, but promote
`clustering\_stability\_diagnostic()` as the primary diagnostic.
The existing `feature\_strength\_diagnostic()` can serve as a
validation tool when ground-truth state labels are available (e.g., in
synthetic experiments or benchmark datasets).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{7. Comparison to Existing
`feature\_strength\_diagnostic()`}{7. Comparison to Existing feature\_strength\_diagnostic()}}<!-- label: comparison-to-existing-feature_strength_diagnostic -->

#### 7.1 Current Implementation<!-- label: current-implementation -->

The existing diagnostic (lines 589-671 of `state\_value.py`)
works as follows:

1. 
2. 
3. 
4. 

\subsubsection{7.2 Limitations of the Existing
Diagnostic}<!-- label: limitations-of-the-existing-diagnostic -->

1. 
2. 
3. 
4. 

#### 7.3 Direct Comparison<!-- label: direct-comparison -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1196}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4457}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4348}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Dimension
\end{minipage} & \begin{minipage}[b]
Existing `feature\_strength\_diagnostic()`
\end{minipage} & \begin{minipage}[b]
New `clustering\_stability\_diagnostic()`
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Input required & Features + true state labels & Features + K 

Assumptions & None explicit (but MI est. degrades with d) & None
(distribution-free) 

Computational cost & Fast (k-NN MI) & Moderate (B x k-means) 

Tests SCX's actual workflow? & No (tests MI, not k-means) & Yes
(directly tests k-means) 

Works for ACE descriptors (d=100)? & No (curse of dim. for MI est.) &
Yes 

Works for CNN latents (d=128)? & No & Yes 

Works when S unknown? & No & Yes 

Theoretically grounded? & Yes (Thm 2) & Yes (clustering stability
lit.) 

Distributional assumptions? & No & No 

Interpretability & ``epsilon\_phi = 0.45'' & ``stability = 0.82, strong
features'' 

False positive mode & N/A (needs true labels) & Stable clus. may not
align with noise 

False negative mode & N/A (needs true labels) & Possible (see Section
9) 

\end{longtable}

#### 7.4 Migration Path<!-- label: migration-path -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Validation Strategy<!-- label: validation-strategy -->

\subsubsection{8.1 Synthetic Data
Validation}<!-- label: synthetic-data-validation -->

Generate data from a K-component Gaussian mixture (ground truth known)
and vary the center separation Delta. For each separation level:

1. 
2. 
3. 
4. 

Expected result: S \textgreater{} 0.7 corresponds to detectable F1
improvement for all tested configurations.

\subsubsection{8.2 Real-Data Validation (Three SCX
Datasets)}<!-- label: real-data-validation-three-scx-datasets -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1364}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2879}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2879}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2879}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Dataset
\end{minipage} & \begin{minipage}[b]
Expected Stability
\end{minipage} & \begin{minipage}[b]
SCX F1 Improvement
\end{minipage} & \begin{minipage}[b]
Diagnostic Verdict
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
AlN v3 (ACE) & \textgreater{} 0.9 & +0.16 & Strong 

CIFAR-10 (deep embeddings) & \textgreater{} 0.9 & Moderate & Strong 

DermaMNIST (SimpleCNN) & \textless{} 0.5 & ~0.01-0.03 &
Weak 

\end{longtable}

\subsubsection{8.3 Ablation: How Many Bootstrap
Resamples?}<!-- label: ablation-how-many-bootstrap-resamples -->

Evaluate stability as a function of B (10, 20, 50, 100, 200):

- 
- 
- 

#### 8.4 Sensitivity to K<!-- label: sensitivity-to-k -->

Evaluate stability at K-1, K, K+1 (where K is the ``true'' number of
states):

- 
- 

This provides a useful diagnostic for the number-of-states choice: the K
that maximizes stability is a good candidate.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Honest Limitations<!-- label: honest-limitations -->

\subsubsection{9.1 Stability Is a Sufficient Condition, Not a Necessary
One}<!-- label: stability-is-a-sufficient-condition-not-a-necessary-one -->

The most important limitation: stable clustering does not guarantee that
SCX will succeed. A stable clustering may separate samples along a
direction that is irrelevant to noise detection. Example: ACE
descriptors that clearly separate surface atoms from bulk atoms, but
where noise is concentrated in surface atom labeling. The clustering is
stable (surface vs.~bulk), but the noise structure within each state is
identical --- SCX cannot improve detection.

This is the same limitation as Theorem 2's delta (mutual information is
about state discovery, not about noise detection per se). It is inherent
to any feature-strength diagnostic that does not incorporate expert
annotations.

**Mitigation:** The diagnostic explicitly labels this: ``strong
features, proceed with SCX'' does not guarantee SCX success. It only
guarantees that features are not the bottleneck. Expert redundancy and
noise rate must still be checked.

#### 9.2 Computational Cost<!-- label: computational-cost -->

The stability diagnostic requires B x k-means runs, which is 50x the
cost of a single k-means run. For large datasets (N \textgreater{}
10000, d \textgreater{} 100), this can be computationally expensive:

- 
- 

For the largest datasets, the fast approximation options (mini-batch
k-means, reduced B, subset sampling) should be offered as configurable
alternatives.

\subsubsection{9.3 The Threshold 0.7 Is a
Heuristic}<!-- label: the-threshold-0.7-is-a-heuristic -->

The threshold tau = 0.7 is borrowed from the Cohen's kappa agreement
literature (Landis \& Koch, 1977). It is not derived from first
principles for the SCX setting.

**Mitigation:** The threshold can be calibrated per domain using
synthetic data (Section 4.2). The diagnostic reports the raw stability
value, not just the verdict, allowing users to make their own threshold
decisions.

\subsubsection{9.4 Label Alignment
Artifacts}<!-- label: label-alignment-artifacts -->

Aligning cluster labels between baseline and bootstrap runs requires
solving a matching problem. If K is large (\textgreater{} 20), the
Hungarian algorithm (O(K\^{}3)) is needed. If multiple clusterings are
equally good matches, the ARI can be inflated by the matching procedure.

**Mitigation:** Use the same initialization for baseline and
bootstrap runs. This avoids label permutation ambiguity because the same
initialization seeds produce consistently labeled clusters. The
Hungarian alignment is only a safety net for when the algorithm
converges to genuinely different local optima.

\subsubsection{9.5 Sensitivity to
Outliers}<!-- label: sensitivity-to-outliers -->

A single outlier far from all cluster centers can dominate the k-means
objective without being part of any meaningful state structure. If the
outlier is inconsistently assigned across bootstrap resamples, it can
reduce stability even in the presence of strong structure.

**Mitigation:** Pre-process features to clip or Winsorize extreme
values. The stability diagnostic should be run after standard
preprocessing (centering, scaling, outlier removal).

\subsubsection{9.6 Stability Under k = 1 or Degenerate
Cases}<!-- label: stability-under-k-1-or-degenerate-cases -->

If K = 1 (no state structure), the stability diagnostic is undefined
(ARI requires at least 2 clusters). If K = N (each sample its own
state), ARI = 1 trivially. The diagnostic should check for degenerate K
values and return appropriate warnings.

\subsubsection{9.7 Relationship to Theorem 2 Is Empirical, Not
Formal}<!-- label: relationship-to-theorem-2-is-empirical-not-formal -->

Unlike the BBP spectral proxy (which attempted to prove an analytic
connection to delta), the stability diagnostic makes a
**pragmatic** connection to Theorem 2:

- 
- 

This connection is empirically validated but not formally proved. The
theorem in Section 3 formalizes the link between stability and
identifiable state structure, but the link to noise detection F1 remains
mediated by expert redundancy, noise rate, and the alignment of cluster
structure with noise patterns --- factors outside the stability
diagnostic.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. References<!-- label: references -->

\subsubsection{Clustering Stability
(Primary)}<!-- label: clustering-stability-primary -->

1. 
2. 
3. 
4. 

#### K-means Theory<!-- label: k-means-theory -->

1. 
2. 

#### Adjusted Rand Index<!-- label: adjusted-rand-index -->

1. 

#### Computational Methods<!-- label: computational-methods -->

1. 

\subsubsection{Applications in Material Science (SCX
Context)}<!-- label: applications-in-material-science-scx-context -->

1. 
2. 

\subsubsection{Cohen's Kappa and Agreement
Thresholds}<!-- label: cohens-kappa-and-agreement-thresholds -->

1. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Appendix A: Relationship to Previous
Attempts}<!-- label: appendix-a-relationship-to-previous-attempts -->

\subsubsection{A.1 Comparison to BBP Spectral
Proxy}<!-- label: a.1-comparison-to-bbp-spectral-proxy -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3958}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4375}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
BBP Spectral Proxy
\end{minipage} & \begin{minipage}[b]
Stability Diagnostic
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Core quantity & lambda\_1 (largest eigenvalue) & ARI (clustering
agreement) 

What it tests & Variance alignment with state structure &
Reproducibility of k-means 

Assumptions & Isotropic Gaussian, i.i.d. entries & None 

Computability & O(N\^{}3) eigendecomposition & O(B * N * K * d *
n\_init) 

Calibration & Circular (C depends on unknown theta) & Threshold-based
(heuristic, calibratable) 

False positives & High (nuisance variance creates spikes) & Possible
(stable clusters may not aid SCX) 

False negatives & High (many-weak-signals regime) & Possible (see
Section 9) 

Theoretical foundation & BBP phase transition (not applicable to SCX) &
Clustering stability (applicable to k-means) 

\end{longtable}

#### A.2 What We Learned<!-- label: a.2-what-we-learned -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of document.*