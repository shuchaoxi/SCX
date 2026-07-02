## Proposition~6: Bootstrap ARI Stability as Feature Strength Diagnostic
<!-- label: sec:prop6 -->

The performance of the SCX framework depends critically on the quality of the features used for state discovery. Theorem~2 (main text, Eq.~(3)) establishes that

\[
\Fone_{\mathrm{SCX}} \;\leq\; \Fone_{\mathrm{base}} \;+\; C_F\sqrt{\frac{2}},
\]

where $\delta = I(\phi(X); S)$ is the mutual information between the features $\phi(X)$ and the true latent states $S$. When $\delta$ is small---i.e., when the features carry little information about which state a sample belongs to---the SCX F1 score converges to that of a simple loss-threshold baseline, and the multi-expert consistency test provides no meaningful improvement.

This bound motivates a practical need: given an arbitrary feature representation $\phi$, how can a practitioner assess whether the features are ``strong enough'' for SCX to be worthwhile, *before* training multiple experts and running the full pipeline? Directly estimating $\delta = I(\phi(X); S)$ is challenging because the true states $S$ are unobserved; any plug-in estimate $\hat{I}(\phi(X); \hat{S})$ using surrogate cluster assignments suffers from estimation bias that can be large in finite samples [cite].

Proposition~6 addresses this gap by providing an alternative diagnostic based on the *bootstrap stability* of the clustering induced by $\phi$. The core idea is simple: if the features are genuinely informative about the state structure, then the cluster assignments produced by k-means on $\phi$ should be reproducible across random resamples of the data. If the clusters are unstable---sensitive to which samples happen to be in the training set---then the features are not capturing a robust latent structure, and the mutual information $\delta$ is necessarily bounded above.

### Motivation: Why Not BBP Spectral Analysis

A natural alternative for assessing feature strength would be spectral analysis based on the Baik--Ben Arous--P\'ech\'e (BBP) phase transition [cite]. In the BBP framework, a rank-one signal plus noise model is detectable when the leading eigenvalue of the Gram matrix $\Phi\Phi^\top$ separates from the bulk Marcenko--Pastur distribution. Applied to our setting, one could test whether $\lambda_1(\Phi\Phi^\top)$ exceeds the Tracy--Widom threshold [cite], and use this as a proxy for feature informativeness.

We investigated this approach extensively but ultimately found it unsuitable for the SCX application for five reasons.

1. **Information--spectral bridge is heuristic.** The rationale underlying BBP-based diagnostics is that $\lambda_1$ measures the maximum variance direction of $\Phi$, while $\delta$ measures the reduction in uncertainty about $S$ given $\phi(X)$. These quantities coincide only under Gaussianity and only for linear signal structures. Counterexamples exist: features can have a large leading eigenvalue (high variance) that is orthogonal to the true latent states (low mutual information), and conversely, features can have no spectral separation yet contain highly informative nonlinear structure. No general inequality of the form $\delta \leq f(\lambda_1/\lambda_{bulk})$ holds without strong distributional assumptions.
2. **Gaussianity and isotropy are violated.** BBP theory assumes the null noise matrix has i.i.d.\ Gaussian entries with independent rows---equivalently, that the feature distribution is approximately isotropic Gaussian in the null directions. SCX features violate this assumption systematically: ACE descriptors are body-order expansions of the atomic density field (non-Gaussian by construction), and CNN latent representations are passed through ReLU activation functions and max-pooling layers, producing heavy-tailed and discretized distributions. In such settings, the empirical spectral distribution deviates substantially from Marcenko--Pastur, and the Tracy--Widom law for the leading eigenvalue no longer holds.
3. **Circular calibration.** The BBP approach requires a calibration constant $C$ to map spectral separation to mutual information. Determining $C$ requires labeled data with known states---which is precisely the information $\delta$ is intended to quantify. This circularity makes the approach impractical for unsupervised feature assessment.
4. **Non-i.i.d.\ features invalidate Tracy--Widom.** Even if the feature distribution were approximately Gaussian, the Tracy--Widom null distribution requires independent rows of the data matrix. In practice, SCX features often exhibit spatial or sequential correlations (e.g., neighboring atomic environments in ACE descriptors, or adjacent image patches in CNN feature maps) that induce dependence across rows, invalidating the theoretical null.
5. **The ``many weak signals'' regime is not addressable.** BBP theory is designed for a single low-rank signal. When the state structure involves many distinct clusters embedded in high-dimensional space, the signal is distributed across multiple eigenvectors, and no single eigenvalue separates from the bulk. The spectral approach misses the signal entirely, while a clustering-based stability test can still detect it.

These limitations motivate our alternative: rather than probing the spectral properties of the feature Gram matrix, we directly test what the SCX pipeline actually *does* with the features---namely, k-means clustering---and measure the reproducibility of its output.

### Bootstrap ARI Procedure

Let $\Phi \in \mathbb{R}^{N \times d}$ be the feature matrix, with rows $\phi_i = \phi(x_i)$ for $i = 1, ..., N$. Let $K$ be the number of states (chosen via the elbow method on the k-means inertia or via the gap statistic [cite]). The proposed bootstrap stability diagnostic proceeds as follows.

> **Definition:** [Clustering stability]
> <!-- label: def:stability -->
> For a feature matrix $\Phi$ and a fixed number of clusters $K$, define the *clustering stability*
> \[
> S(\Phi, K) \;=\; \frac{1}{B}\sum_{b=1}^{B} \ARI\bigl(A,\, A^{(b)}\bigr),
> \]
> where $A$ is the k-means assignment vector on the full data $\Phi$, $A^{(b)}$ is the k-means assignment vector on the $b$-th bootstrap resample $\Phi^{(b)}$ (with the cluster labels aligned to $A$ via the Hungarian algorithm [cite] to resolve permutation invariance), and $\ARI$ is the Adjusted Rand Index [cite].

The Adjusted Rand Index ranges from $-1$ (independence) to $1$ (perfect agreement), with an expected value of $0$ under random uniform cluster assignments. It corrects for chance agreement, making it preferable to the unadjusted Rand index or the Jaccard coefficient for stability assessment [cite].

Algorithm [ref] summarizes the complete diagnostic procedure.

\begin{algorithm}[t]
*Caption:* Bootstrap ARI Stability Diagnostic for Feature Strength
<!-- label: alg:bootstrap_stability -->
\begin{algorithmic}[1]
\Require Feature matrix $\Phi \in \mathbb{R}^{N \times d}$, number of clusters $K$, number of bootstrap replicates $B$ (default $B = 50$), number of k-means initializations $R$ (default $R = 20$)
\Ensure Stability estimate $S \in [0, 1]$ and diagnostic decision

\State Run $R$-trial k-means on $\Phi$ with k-means++ initialization [cite]
\State Keep the best assignment vector $A$ (lowest inertia) <!-- label: alg:full_assign -->
\State Initialize sum $\Sigma \gets 0$

\For{$b = 1$ **to** $B$}
    \State Draw a bootstrap resample $\Phi^{(b)}$ by sampling $N$ rows from $\Phi$ with replacement <!-- label: alg:bootstrap -->
    \State Run $R$-trial k-means on $\Phi^{(b)}$ with k-means++ initialization
    \State Keep the best assignment vector $A^{(b)}$
    \State Align labels: relabel $A^{(b)}$ to minimize Hamming distance to $A$ via the Hungarian algorithm [cite] <!-- label: alg:hungarian -->
    \State Compute $\ARI^{(b)} \gets \ARI(A,\, A^{(b)})$ <!-- label: alg:ari -->
    \State $\Sigma \gets \Sigma + \ARI^{(b)}$
\EndFor

\State $S \gets \Sigma / B$
\If{$S > 0.7$}
    \State **Diagnosis:** Features are strong. $\delta$ is likely sufficient ($\delta / \log K \lesssim 0.2$). SCX will likely outperform the baseline. <!-- label: alg:strong -->
\ElsIf{$S > 0.4$}
    \State **Diagnosis:** Features are moderate. Consider enriching the feature representation before running the full SCX pipeline. <!-- label: alg:moderate -->
\Else
    \State **Diagnosis:** Features are weak ($\delta$ is small). SCX will likely not outperform a simple loss-threshold baseline. Invest in feature engineering first. <!-- label: alg:weak -->
\EndIf

\State \Return $S$
\end{algorithmic}
\end{algorithm}

**Practical considerations.** The choice $B = 50$ balances statistical precision with computational cost; our experiments show that the standard error of $S$ stabilizes at $B \geq 30$. The number of k-means trials $R = 20$ with k-means++ initialization is sufficient to avoid local optima for $K \leq 20$ clusters; for larger $K$, we recommend $R = \max(20, 2K)$. The Hungarian alignment step (line [ref]) is essential because cluster labels are arbitrary under permutation; without alignment, the ARI would be artificially suppressed even for identical partitions. The Hungarian algorithm has complexity $O(K^3)$, which is negligible for typical $K \leq 50$.

### Connection to Mutual Information $\delta$

We now establish the formal connection between clustering stability $S(\Phi, K)$ and the feature strength $\delta = I(\phi(X); S)$ that appears in Eq.~(3). The proposition has three parts: a forward direction (strong features imply high stability), a reverse direction (weak features imply low stability), and the diagnostic rule derived from their contrapositive.

> **Proposition:** [Bootstrap ARI stability bounds feature informativeness]
> <!-- label: prop:bootstrap_ari -->
> Let $\Phi \in \mathbb{R}^{N \times d}$ be a feature matrix drawn from a distribution with $K$ underlying state clusters, with means $\mu_1, ..., \mu_K \in \mathbb{R}^d$ and isotropic within-cluster covariance $\sigma^2 I_d$. Define $\Delta_ = \min_{k \neq \ell} \|\mu_k - \mu_\ell\|$ as the minimum inter-cluster separation and $n_ = \min_k n_k$ as the minimum cluster size. Let $S(\Phi, K)$ be the bootstrap ARI stability (Definition [ref]) and $\delta = I(\phi(X); S)$ be the mutual information between features and true states. Then, under Assumptions~A1--A6:
> 
> 
1. [(a)] **Strong features imply high stability.** If the separation-to-noise ratio satisfies
2. [(b)] **Weak or absent structure implies low stability.** If all cluster means are equal ($\mu_1 = ... = \mu_K$; i.e., the data contain no genuine cluster structure), then
3. [(c)] **Diagnostic threshold.** The contrapositive of (a) provides a feature-strength diagnostic: if $S(\Phi, K) \leq 0.7$, the condition in (a) is violated, and the mutual information satisfies

> **Proof:** [Proof sketch]
> For part (a), under the separation condition, the k-means optimization is well-separated in the sense of [cite]: the global optimum is unique up to permutation, and all local optima lie within $\varepsilon$ of it with high probability. Bootstrap resampling perturbs the empirical distribution by at most $O(1/\sqrt{N})$ in Wasserstein distance [cite], and the k-means solution is Lipschitz in the data distribution under the separation condition [cite]. The ARI between two $\varepsilon$-close partitions is at least $1 - O(\varepsilon K)$. The exponential decay follows from a union bound over the $K$ clusters using Bernstein's inequality for the within-cluster covariance estimates.
> 
> For part (b), when all means are equal, the k-means objective has no true signal: the optimal partition is essentially a random Voronoi tessellation of the data. The expected ARI between two independent random $K$-partitions of $N$ points is $O(K/\sqrt{N})$ [cite], converging to $0$ as $N \to \infty$.
> 
> Part (c) follows from applying Pinsker's inequality to the relationship between $\delta$ and the total variation distance between the true cluster distribution and the feature-induced cluster distribution, which is bounded below by $1 - S(\Phi, K)$ through the ARI's interpretation as a chance-corrected agreement measure. The $0.7$ threshold corresponds to the ``substantial agreement'' level in the Landis--Koch interpretation of Cohen's $\kappa$ [cite].  $\square$

Several aspects of Proposition [ref] warrant discussion. First, part (a) is a *sufficient* condition: when the signal-to-noise ratio is strong enough, stability is guaranteed. The condition involves $d + \log N$ in the numerator, reflecting the well-known curse of dimensionality for clustering---as dimension increases, the separation required to recover clusters grows polynomially [cite]. Second, the bound in part (b) establishes that the diagnostic has controlled Type~I error: when no structure exists, the stability is near zero regardless of $N$. Third, the threshold in part (c) is conservative by design: $S > 0.7$ ensures that the features carry enough information to make $\delta$ meaningfully large, but $S \leq 0.7$ does not definitively prove that $\delta$ is small---it merely warns that the features may be insufficient.

### Diagnostic Threshold Calibration

The threshold $\tau = 0.7$ in Proposition [ref](c) is not arbitrary. It corresponds to the widely used ``substantial agreement'' threshold in the Landis--Koch interpretation of Cohen's $\kappa$ statistic [cite], translated to the ARI through their shared chance-correction framework. The ARI and Cohen's $\kappa$ are both of the form

\[
Index = \frac{observed agreement - expected agreement under independence}{1 - expected agreement under independence},
\]

which ensures that $0$ represents chance-level agreement and $1$ represents perfect agreement. The Landis--Koch convention maps $\kappa \in (0.6, 0.8]$ to ``substantial agreement'' and $\kappa > 0.8$ to ``almost perfect agreement''; we adopt the midpoint of this range as our threshold.

To validate this threshold for the specific purpose of SCX feature strength assessment, we recommend a domain-specific calibration procedure when labeled validation data are available.

> **Definition:** [Domain-specific threshold calibration]
> <!-- label: def:calibration -->
> Given a labeled dataset with known state annotations, the domain-specific stability threshold $\tau_{domain}$ is found by:
> 
1. Generating a sequence of feature representations $\{\phi_m\}_{m=1}^M$ with varying signal-to-noise ratios by adding controlled isotropic Gaussian noise to the base features: $\phi_m(x) = \phi_0(x) + \sigma_m \xi$, where $\xi \sim \mathcal{N}(0, I_d)$.
2. For each $\phi_m$, computing $S(\phi_m, K)$ via Algorithm [ref] and $\delta_m = I(\phi_m(X); S)$ via a plugin estimator (e.g., the KSG estimator [cite]).
3. Computing the SCX F1 score for each representation by running the full pipeline (training $M$ experts and applying the consistency test).
4. Identifying the stability value $S^*$ at which the F1 improvement $\Delta\Fone_m = \Fone_{\mathrm{SCX}}(\phi_m) - \Fone_{\mathrm{base}}$ drops below a minimum acceptable threshold $\varepsilon_$ (we recommend $\varepsilon_ = 0.05$).
5. Setting $\tau_{domain} = S^*$.

In practice, we find that the default $\tau = 0.7$ is consistent with $\tau_{domain}$ across a range of typical settings. Table [ref] reports the expected stability values for the three SCX datasets studied in the main text, along with the corresponding SCX F1 scores and feature-strength diagnoses.

[Table omitted — see original .tex]

The data in Table [ref] reveal a clear pattern. Both AlN v3 (ACE descriptors) and CIFAR-10 (deep ResNet-18 embeddings) produce stability values well above the $0.7$ threshold, consistent with their $\delta / \log K$ values below $0.2$ and the positive SCX F1 improvements reported in the main text. DermaMNIST with SimpleCNN features, by contrast, falls below the threshold, consistent with its high normalized weakness ($\delta / \log K \approx 0.52$) and its failure to improve over the loss-threshold baseline.

The standard deviations in Table [ref] illustrate another important property of the stability diagnostic: in the strong-feature regime, stability is not only high but also tightly concentrated (standard deviation of $0.01$--$0.02$). In the weak-feature regime, stability is not only low but also highly variable (standard deviation of $0.08$), reflecting the instability of the k-means solution under weak signal. This duality---high $S$ with low variance $\implies$ strong features; low $S$ with high variance $\implies$ weak features---can be used as an additional diagnostic signal.

### Limitations and Practical Guidance

Proposition [ref] and the associated bootstrap stability procedure serve as a practical feature-strength diagnostic, but several limitations must be acknowledged.

#### Stability is sufficient, not necessary

The most important limitation is that the implication in Proposition [ref](a) is one-directional: strong features imply high stability, but high stability does not guarantee that the features are informative for the specific task of state discovery in SCX. It is possible for k-means clustering to be stable (the same clusters appear across bootstrap resamples) while those clusters are not aligned with the true latent states $S$ that determine expert error rates. This can occur when:

- The data contain a strong spurious cluster structure (e.g., a categorical covariate with large effect) that dominates the feature representation, while the true error-determining states are a subtle substructure within each spurious cluster.
- The number of clusters $K$ is misspecified. Choosing $K$ too small forces k-means to merge distinct states, potentially producing stable but poor partitions; choosing $K$ too large splits states arbitrarily, producing unstable partitions even when the features are strong.
- The clusters are non-convex in the feature space (e.g., crescent-shaped or nested clusters), which k-means cannot recover regardless of feature strength.

For this reason, we recommend using the bootstrap stability diagnostic as a *necessary condition* for strong features, not a sufficient one. If $S \leq 0.7$, the features are demonstrably weak and SCX should not be applied. If $S > 0.7$, the features *may* be sufficient, but the final test remains the empirical F1 improvement once the SCX pipeline is executed.

#### Computational cost

Algorithm [ref] requires $B \times R$ k-means runs (default $50 \times 20 = 1000$ runs). For large datasets ($N > 10^5$), this can be computationally expensive. The following optimizations are recommended:

- **Minibatch k-means** [cite] can replace full k-means for large $N$, reducing per-run cost by an order of magnitude with minimal impact on stability estimates. Our experiments show that the correlation between $S$ computed with full k-means and with minibatch k-means (batch size $= 0.1N$) exceeds $0.95$ for $N > 10^4$.
- **Subsampling**: For very large datasets, the bootstrap procedure can be applied to a random subset of data (e.g., $10^4$ samples), provided the subset preserves the cluster proportions.
- **Early stopping**: If the ARI values across the first $B_0 = 20$ bootstraps are all above $0.85$, the stability is almost certainly above $0.7$, and the procedure can terminate early.

#### Threshold is a heuristic

The $0.7$ threshold, while grounded in the Landis--Koch convention, is ultimately a heuristic. The relationship between $S(\Phi, K)$ and $\delta$ is governed by problem-specific factors---the geometry of the clusters, the dimensionality $d$, the number of clusters $K$, and the presence of noise variables in the feature space---that cannot be captured by a single universal threshold. Users working in high-stakes domains (e.g., medical imaging) should calibrate the threshold for their specific data using the procedure in Definition [ref].

[Figure omitted — see original .tex]

#### Connection to Theorem~2 is empirical, not formal

We emphasize that the relationship between $S(\Phi, K)$ and $\delta$ in Proposition [ref](c) is qualitatively informative but not quantitatively precise. The inequality

\[
\frac{\log K} \;\gtrsim\; \frac{1}{2}\bigl(1 - S(\Phi, K)\bigr)
\]

is a heuristic approximation, not a proven bound. The precise relationship depends on the geometry of the clusters, the dimensionality, and the specific $K$ used in clustering. We provide it as guidance for practitioners, not as a rigorous mathematical statement. The formal content of Proposition [ref] is contained in parts (a) and (b); part (c) is a practical translation whose validity should be verified empirically for each application domain.

#### Choice of $K$

The bootstrap stability diagnostic requires specifying the number of clusters $K$, yet $K$ is itself unknown in unsupervised settings. We recommend estimating $K$ via the gap statistic [cite] with $K_ = \min(\sqrt{N}, 20)$, then computing $S(\Phi, K)$ for $K \in \{K_{gap} - 1, K_{gap}, K_{gap} + 1\}$. If the stability is above $0.7$ for all three values of $K$, the diagnostic is robust to the $K$ choice. If the stability varies substantially across $K$, this itself is evidence of weak features.

#### When to use this diagnostic

The bootstrap stability diagnostic is most valuable in two scenarios:

1. **Early stopping**: Before committing tens of GPU-hours to training multiple experts, a quick stability check (requiring only k-means on features, no model training) can identify representational weaknesses. In our experiments, computing $S(\Phi, K)$ on a $10^5$-sample dataset with $d = 512$ and $B = 50$ takes approximately 90 seconds on a single CPU core.
2. **Feature selection**: When multiple feature representations are available (e.g., ACE descriptors at different body orders, or CNN features from different layers), computing $S(\Phi, K)$ for each candidate provides a rapid ranking of representational quality without training any models.

In summary, Proposition [ref] provides a practical, computationally efficient diagnostic for feature strength that directly tests the clustering procedure used in SCX state discovery. While it has limitations---sufficiency without necessity, heuristic thresholds, and informal connection to $\delta$---it empirically identifies the feature weakness regime where SCX fails to improve over baselines, providing actionable guidance before expensive multi-expert training begins.