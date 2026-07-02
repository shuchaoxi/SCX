# Referee Report: ``BBP Spectral Proxy: A Computable Alternative
to SCX Theorem 2's Mutual
Information''

**Author:** SCX

**Review requested by:** Editor-in-Chief (hostile review mode)
**Venue:** Annals of Statistics (imagined) **Recommendation:**
REJECT

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Executive Summary<!-- label: executive-summary -->

This document attempts to bridge two mathematical frameworks: (1) the
BBP phase transition for spiked covariance matrices, and (2) the SCX
Theorem 2 bound connecting mutual information I(phi;S) to F1 detection
performance. The goal is admirable --- replace an intractable quantity
(mutual information) with a computable one (the largest eigenvalue of
the Gram matrix). However, the mathematical bridge is not viable. At
every critical juncture, the argument either assumes what it needs to
prove, relies on conditions that the target application manifestly
violates, or substitutes heuristics for theorems. I detail the fatal
flaws below.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. The Information-Spectral Bridge is Fundamentally
Misconceived<!-- label: the-information-spectral-bridge-is-fundamentally-misconceived -->

The core claim is that delta\_hat = max(0, (lambda\_1 - MP\_+)/C) serves
as a proxy for delta = I(phi; S). This conflates two quantities that
measure fundamentally different things.

**Mutual information** I(phi; S) measures the reduction in
uncertainty about the state labels S given the features phi. It is a
functional of the full joint distribution P(phi, S) and depends on every
dimension of phi, every interaction between dimensions, and the detailed
geometry of the conditional distributions.

**The largest eigenvalue** lambda\_1 measures the maximum variance
direction of the feature distribution. It is a one-dimensional summary
statitstic of the marginal distribution P(phi). It does not, on its own,
tell you whether that variance is aligned with the state labels.

**Counterexample 1A: Large lambda\_1, small I(phi; S).** Let S be a
binary label independent of all features. Construct phi such that the
first coordinate is Z ~{} N(0, 1000) and coordinates
2... d are i.i.d. N(0,1). The population covariance is Sigma =
diag(1000, 1, ..., 1). The largest eigenvalue is 1000, far exceeding
the MP bulk. The BBP test declares ``strong features.'' Yet I(phi; S) =
0 because phi and S are independent. The spectral proxy gives a large
positive delta\_hat while the true delta is zero. This is not a
pathology --- it is the expected behavior whenever the dominant variance
direction is not the state-separating direction. The author implicitly
assumes that the top eigenvector of the covariance matrix aligns with
the state separation, which is exactly the assumption that needs to be
tested, not assumed.

**Counterexample 1B: Small lambda\_1, large I(phi; S).** Let S be a
50-state categorical variable. For each state k, construct the state
mean mu\_k as a vector in R\^{}\{1000\} where exactly 20 randomly chosen
coordinates are set to 0.5 and the rest are 0. The state means differ in
their support patterns, not in their overall norm. The between-state
scatter B has rank at most 49, but each eigenvalue of B is small
(approximately 0.5\^{}2 * 20/1000 = 0.005 per coordinate, times a
multiplicity factor). The largest eigenvalue of B/sigma\^{}2 may be well
below sqrt(gamma) even for modest gamma. Yet the mutual information
between phi and S is substantial: the 20 non-zero coordinates provide
nearly perfect state discrimination because each state's support pattern
is unique. The spectral proxy returns delta\_hat = 0. The true delta is
approximately log\_2(50) = 5.6 bits. False negative: catastrophic.

**The defense in Section 12.1** (``an eigenvalue spike can only
appear if there genuinely is between-state variation'') is incorrect, as
Counterexample 1A shows. A high-variance feature independent of S
produces a spike just as effectively as a state-separating feature. The
spectral proxy cannot distinguish between ``signal-relevant variance''
and ``nuisance variance.''

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. The ``Monotonic Relationship'' Claim is
Unsupported<!-- label: the-monotonic-relationship-claim-is-unsupported -->

Section 3.4 states: ``The effective signal strength theta and the mutual
information delta are **monotonically related** under the isotropic
Gaussian mixture.''

The supporting evidence is:

1. 
2. 
3. 

These bounds do not establish monotonicity. They establish that delta
lives in the interval {[}theta/8, (K-1)theta/2{]} for binary states,
which spans a factor of 4(K-1). Monotonicity would require proving that
for any two parameter configurations (theta\_1, mean geometry\_1) and
(theta\_2, mean geometry\_2), if theta\_1 \textgreater{} theta\_2 then
delta\_1 \textgreater{} delta\_2. The provided bounds are too loose to
guarantee this.

**A concrete failure of monotonicity under the author's own
model.** Consider two configurations, both binary Gaussian mixtures with
isotropic noise:

- 
- 

Same theta, different deltas --- monotonicity is false even within the
isotropic Gaussian mixture model. The relationship between theta and
delta depends not just on theta but on the **geometry** of the
state means, which the spectral proxy discards.

The sentence ``The mapping is not one-to-one (theta can be large while
delta saturates at log K), but it is a valid sufficient condition'' is a
hedge that admits the mapping is not injective, which is exactly the
problem. A sufficient condition that says ``if the spectral spike is
large, features might be strong, or then again they might not be'' is
not a theorem --- it is a heuristic.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. The Gaussian Mixture Assumption is Fatal for SCX's Actual
Features<!-- label: the-gaussian-mixture-assumption-is-fatal-for-scxs-actual-features -->

The entire derivation assumes:

- 
- 
- 

**SCX's actual features violate every one of these assumptions:**

1. 
2. 
3. 

**The author acknowledges these violations in Section 13.2** but
offers only hand-wavy mitigations: ``pre-whiten,'' ``permutation test,''
``robust test.'' None of these are part of the theoretical bridge. The
``pre-whiten'' suggestion requires estimating the within-state
covariance, which is what we're trying to avoid computing (it requires
knowing the state partition). The ``permutation test'' suggestion
replaces the parametric spectral test with a nonparametric one, which
abandons the Tracy-Widom theory entirely. The ``robust test'' suggestion
(citing Berthet \& Rigollet, 2013) addresses a different problem (sparse
PCA, not general non-Gaussian features).

**The core issue**: Under misspecification, the MP bulk edge MP\_+
is no longer correct. For anisotropic within-state covariance, the
limiting spectral distribution of the Gram matrix is a free convolution
of the MP law with the population eigenvalue distribution of Sigma\_W.
The upper edge can be arbitrarily far from sigma\^{}2
(1+sqrt(gamma))\^{}2. The BBP threshold sqrt(gamma) depends on the
isotropy assumption. Without isotropy, both the null distribution and
the phase transition location are unknown.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. The Tracy-Widom Test is Invalid for SCX
Features<!-- label: the-tracy-widom-test-is-invalid-for-scx-features -->

The test statistic uses TW\_1 critical values derived for the largest
eigenvalue of a sample covariance matrix whose entries are i.i.d. with
finite 4th moment.

**SCX features violate the i.i.d. entry assumption in multiple
ways:**

1. 
2. 
3. 
4. 

**The power analysis in Section 5.4** computes ``detectable gaps''
for the three datasets, assuming TW\_1 applies perfectly. These numbers
(epsilon\_detect of 0.12-0.27) are optimistic precisely because they
ignore the excess variance from non-i.i.d. features.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. The Calibration Constant C is a Free
Parameter<!-- label: the-calibration-constant-c-is-a-free-parameter -->

The treatment of C is the weakest part of the paper, revealing that the
``theorem'' is not a theorem at all.

**Step 1: Theoretical derivation (Section 8.1).** The author
derives C = 2 * sigma\^{}2 * (theta - sqrt(gamma))\^{}2 / (theta *
(1+theta)). But this depends on the unknown theta, which is what we're
trying to infer from lambda\_1. Circular.

**Step 2: Self-consistent estimation (Section 8.2).** The author
proposes inverting the BBP formula to estimate theta from lambda\_1,
then plugging theta into C. But this is algebraically redundant: if you
already have theta from lambda\_1 via the BBP inverse formula, you don't
need the spectral proxy at all --- you can compute delta directly from
theta (under the Gaussian model). The ``self-consistent estimation''
reveals that the proxy is just a complicated change of variables, not an
independent quantity.

**Step 3: Practical default C = 2 (Section 8.3).** The
justification is: ``From the binary Gaussian mixture: delta ≈ theta/2
and Delta\_lambda / sigma\^{}2 ≈ theta. So C ≈ 2 sigma\^{}2. After
normalizing sigma\^{}2 to 1, C ≈ 2.'' This is valid only in the regime
where: - gamma is negligibly small (so sqrt(gamma) ≈ 0 and the full
formula collapses) - theta \textgreater\textgreater{} sqrt(gamma) (so
the ``(theta - sqrt(gamma))\^{}2/(1+theta)'' term simplifies to theta) -
K = 2 (binary states only) - The feature dimension d is large enough
that delta ≈ theta/2 (which requires d \textgreater\textgreater{} theta,
so the Gaussian mixture mutual information formula linearizes)

All four conditions fail for typical SCX data. For DermaMNIST with gamma
= 0.0064, sqrt(gamma) = 0.08 --- not negligible relative to small theta
values. For K = 7 classes (DermaMNIST), the single-spike proxy misses 6
dimensions of state separation.

**What is the worst-case error if C=2 but the true value is C=5?**
Then delta\_hat = (lambda\_1 - MP\_+)/2 instead of (lambda\_1 -
MP\_+)/5, overestimating delta by a factor of 2.5. The plug-in F1 bound
becomes: - F1\_SCX \textless= F1\_base + C\_F * sqrt(2 *
delta\_hat\_true * 2.5) ≈ F1\_base + 1.58 * C\_F *
sqrt(delta\_hat\_true)

This is 58\% larger than the correct bound, meaning the diagnostic is
optimistic --- it says ``SCX might work'' when the true bound says it
won't. False positives in the non-conservative direction.

**If C=2 but the true value is C=0.5?** Then delta\_hat
underestimates delta by a factor of 4, making the diagnostic overly
conservative --- it rejects SCX when SCX would work. The false negative
rate is uncontrolled.

The document provides **no** bound on | C\_true -
C\_used|, **no** sensitivity analysis, and **no** error
propagation. This is not a theorem --- it is an ad-hoc calibration.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. The ``Sufficient but Not Necessary'' Defense Acknowledges
the Fatal
Flaw<!-- label: the-sufficient-but-not-necessary-defense-acknowledges-the-fatal-flaw -->

Section 12.2 admits: ``If lambda\_1 is below the MP edge, it does NOT
guarantee SCX will fail.'' This is not a minor caveat --- it is the core
failure mode of the diagnostic.

**How conservative is the test?** This depends on the dataset and
requires specifying: - The number of states K - The geometry of the
state means (are they collinear, orthogonal, or uniformly distributed?)
- The noise level sigma\^{}2 - The aspect ratio gamma

For the worst-case scenario of K = 50 states with means uniformly
distributed on a sphere in R\^{}d, the leading eigenvalue of
B/sigma\^{}2 is approximately R\^{}2/(K * sigma\^{}2) * (1 + (d-1)/K) ≈
R\textsuperscript{2/(K*sigma\^{}2) for large d.~The mutual
information is approximately (R\^{}2/(2*sigma}2)) * tr(B) / sigma\^{}2 ≈
R\^{}2/(2*sigma\^{}2) * K *
(R\textsuperscript{2/(K*sigma\^{}2)) = R\^{}4/(2*sigma}4). For
R\textsuperscript{2/sigma}2 ≈ 10 (moderate signal), K = 50, gamma = 0.1,
d = 100:

- 
- 

This is a false negative rate of 100\% for this configuration. The
diagnostic says ``weak features, don't use SCX'' for a scenario where
the features are actually highly informative.

**Quantification attempt.** Let B ~{} Wishart(K-1,
diag(theta\_1, ..., theta\_\{K-1\})). The largest eigenvalue of B
follows a Tracy-Widom distribution around theta\_1. The condition for
non-detection is:

theta\_1 \textless= sqrt(gamma) = sqrt(d/N)

For K large with approximately equal separation in all directions,
theta\_1 ≈ (mean separation per direction) * (d/K). If K \textgreater{}
d/sqrt(gamma), then theta\_1 \textless{} sqrt(gamma) even when the total
signal is strong. The false negative probability is approximately:

P(false negative |{} total signal strong) ≈ 1 for K
\textgreater{} d / sqrt(d/N) = sqrt(N*d)

For SCX regimes: N = 500, d = 100 -\textgreater{} sqrt(500*100) ≈ 224.
If K \textgreater{} 224 (which is unrealistic for SCX). For more typical
K = 10, the false negative condition is less extreme but still possible
when means are nearly collinear with small separation along each
direction.

The document does not provide this calculation, presumably because it
exposes the severity of the conservatism problem.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. The Sigma\^{2 Estimation is Biased and the Bias is Not
Corrected}<!-- label: the-sigma2-estimation-is-biased-and-the-bias-is-not-corrected -->

MP\_+ = sigma\^{}2 (1 + sqrt(gamma))\^{}2 requires sigma\^{}2. The
author estimates sigma\^{}2 from trailing eigenvalues (Section 5.3, step
3): hat(sigma)\^{}2 = mean of bulk eigenvalues after discarding spikes.

**Problem 1: Signal contamination.** Under the spiked model, the
total sample variance is:

tr(hat(Sigma)) = (1/N) * tr(Phi Phi\^{}T) = sigma\^{}2 * d/N + (1/N) *
tr(Phi\_mean Phi\_mean\^{}T)

The sample bulk eigenvalues are not exactly sigma\^{}2 --- they are
sigma\^{}2 * (eigenvalues of a d-N(0,I) Wishart matrix) perturbed by the
spikes. Even after removing the top r eigenvalues, the remaining bulk
eigenvalues have expectation:

E{[}lambda\_\{r+1\}{]} = sigma\^{}2 * (1 + gamma * eta\_j) where eta\_j
depends on the spike strengths

The bias is E{[}hat(sigma)\^{}2{]} - sigma\^{}2 = sigma\^{}2 * gamma *
(1/N) * sum\_\{j=r+1\}\^{}d eta\_j, which is positive. This inflates
MP\_+, making the test conservative --- but the **amount** of
conservatism is dataset-dependent and not quantified.

**Problem 2: The ``elbow'' method for counting spikes is
unreliable.** Algorithm step 2 uses a threshold rule (lambda\_j
\textgreater{} 2 * median(lambda)) to count spikes. This is a heuristic
with no theoretical justification. For weak spikes near the detection
threshold, the count r\_est is wrong, contaminating the bulk estimate.

**Problem 3: The bulk trimming is arbitrary.** The algorithm
discards ``r\_est + 10'' eigenvalues. The ``+10'' is a guess. If r\_est
is incorrect by more than 10 (plausible for complex spectral structure),
the bulk estimate is contaminated.

**Problem 4: The alternative estimator (median /
MP\_median\_factor) has its own issues.** The median of the MP
distribution is a known function of gamma, but for finite N, the sample
median deviates from the population median, and this deviation is
comparable to the bulk fluctuation scale.

The combined effect: for AlN with d ≈ 100, N = 534, gamma ≈ 0.19, if the
true sigma\^{}2 = 1 but estimate yields hat(sigma)\^{}2 = 1.15 (15\%
relative bias, plausible with signal contamination), then MP\_+ is
inflated by 15\%, making the critical value (1+sqrt(0.19))\^{}2 ≈ 1.64
become ≈ 1.89. This 15\% increase in the threshold can mask a moderately
strong spike (theta = 0.5, lambda\_1 ≈ 1.8) as subcritical.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. The Comparison to Lei \& Zhu (2018) Reveals No
Mathematical
Contribution<!-- label: the-comparison-to-lei-zhu-2018-reveals-no-mathematical-contribution -->

Lei \& Zhu (2018) already proved:

1. 
2. 
3. 

**What this document adds beyond Lei \& Zhu:**

Claimed novelty (Section 10.2): ``SCX does spectral clustering on the
GRAM matrix (N x N) while Lei \& Zhu work with the feature covariance
matrix (d x d).'' This is mathematically vacuous. The non-zero
eigenvalues of Phi Phi\^{}T (N x N) and Phi\^{}T Phi (d x d) are
identical up to scaling. Working with the Gram matrix is a computational
convenience, not a mathematical difference.

Claimed novelty (Section 10.1, item ``Our addition''): ``Connecting the
spectral spike to an information-theoretic quantity (mutual
information).'' But this connection is: - Not proved (it relies on the
heuristic calibration C, as shown in Point 5) - Not needed (Lei \& Zhu's
eigengap condition is already a valid sufficient condition for
clustering success) - Not robust to model misspecification (as shown in
Point 3)

Claimed novelty (Section 11.1): ``The specific connection between the
BBP eigenvalue phase transition and SCX's mutual information bound is
novel.'' Novel and false are not mutually exclusive. The connection does
not survive mathematical scrutiny.

**The honest assessment comes from the author's own novelty table
(Section 11.3):** - ``BBP phase transition'': 0/5 (known) - ``k-means =
PCA on Gram'': 0/5 (known) - ``Spiked covariance model'': 0/5 (known) -
``Spectral clustering consistency'': 0/5 (known) - ``Tracy-Widom test
for spikes'': 1/5 (standard) - ``Mapping theta -\textgreater{} delta'':
3/5 (but this is the part I've shown to be unsupported) - ``Calibration
C estimation'': 3/5 (but this is circular, as shown) - ``Plug-in
diagnostic for Thm 2'': 4/5 (but it inherits all the flaws of the
upstream connections) - ``Multi-spike proxy'': 2/5 (natural extension) -
``Spectral proxy algorithm'': 3/5 (combines known pieces)

The weighted novelty is even lower than the author's estimate, because
the highest-scoring items (``Mapping theta -\textgreater{} delta'' and
``Calibration C'') are the ones with the most serious mathematical
defects. When these collapse, the ``Plug-in diagnostic for Thm 2''
collapses with them.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Additional Mathematical
Issues<!-- label: additional-mathematical-issues -->

#### 9. The ``Proof Sketch'' is Not a
Proof<!-- label: the-proof-sketch-is-not-a-proof -->

Section 4.2 calls itself a ``proof sketch'' but contains no proof. It
consists of: - Part (a): ``follows directly from the BBP phase
transition'' --- correct, but this is just restating BBP, not connecting
to SCX. - Part (b): ``requires connecting the excess eigenvalue to the
mutual information delta'' --- this is the statement of what needs to be
proved, not a proof. The subsequent bullet points do not constitute a
proof: - Bullet 1: When theta \textless= sqrt(gamma), delta\_hat = 0 and
``delta can be arbitrarily small or zero in this regime.'' This is
false. Delta can be non-zero even when theta \textless= sqrt(gamma)
(Counterexample 1B). - Bullet 2: The excess eigenvalue formula is
correct, but the inequality ``delta\_hat \textless= C * delta'' is not
derived --- it's asserted with the qualifier ``for some C depending on
gamma and the state geometry.'' - Bullet 3: The calibration constant is
chosen ``so that delta\_hat is conservative.'' But this is circular: C
is defined as (lambda\_1 - MP\_+) / delta\_0, where delta\_0 is a
``calibrated reference point.'' The choice of delta\_0 determines the
conservatism, and there is no principled way to choose it without
knowing the true delta.

- 
- 

#### 10. Part (b) of the Theorem is Internally
Contradictory<!-- label: part-b-of-the-theorem-is-internally-contradictory -->

The theorem states two inequality claims: - (b1) delta\_hat \textless=
delta + o(1) {[}upper bound: proxy is conservative{]} - (b2) delta\_hat
\textgreater= c(theta) * delta + o(1) {[}lower bound: proxy is
proportional{]}

For (b1) to hold when theta \textless= sqrt(gamma), we need delta\_hat =
0 \textless= delta + o(1), i.e., delta \textgreater= 0. This is true
(mutual information is non-negative). But for (b2) to hold when theta
\textgreater{} sqrt(gamma), we need delta\_hat to be a non-trivial
fraction of delta. The constant c(theta) is not specified. For theta
just above sqrt(gamma), the spectral excess is O((theta -
sqrt(gamma))\^{}2), while delta is O(theta). Therefore c(theta) =
O((theta - sqrt(gamma))\^{}2 / theta) -\textgreater{} 0 as theta
-\textgreater{} sqrt(gamma)\^{}+. The ``lower bound'' becomes
vanishingly small exactly when we need it most --- near the detection
boundary.

#### 11. The Plug-in to Theorem 2 (Section 6) is
Circular<!-- label: the-plug-in-to-theorem-2-section-6-is-circular -->

The bound is: F1\_SCX \textless= F1\_base + C\_F * sqrt(2 * delta\_hat)
+ error

The author claims this is ``valid with probability 1 - o(1)
(asymptotically).'' But: - Theorem 2's original bound uses delta =
I(phi; S) and is a deterministic inequality valid for ALL distributions.
- The proxy version replaces delta with delta\_hat, which is a random
variable depending on the sample. - The claimed validity requires
delta\_hat \textless= delta + o(1) with high probability (Part b1),
which is NOT proved. - The error term epsilon\_N = O(N\^{}\{-2/3\}) from
TW fluctuations is dwarfed by the calibration error O(1) from C.

The statement ``The bound remains valid'' assumes the conclusion.

#### 12. The Validation Predictions (Section 9) are
Tautological<!-- label: the-validation-predictions-section-9-are-tautological -->

The three datasets are chosen to match the expected outcomes: - AlN
(strong SCX improvement) -\textgreater{} ``strong features'' - CIFAR-10
(moderate SCX improvement) -\textgreater{} ``strong features'' (safe
prediction because gamma is tiny) - DermaMNIST (weak SCX improvement)
-\textgreater{} ``weak features'' (safe prediction because SCX doesn't
work)

The document proposes comparing delta\_hat to ``observed SCX F1
improvement'' but does not compute either quantity for any dataset. The
``cross-dataset behavior'' table (Section 9.5) has no actual numbers for
lambda\_1 or delta\_hat --- they're all placeholders
(``\textgreater\textgreater{} MP'', ``\textgreater{} 5.0'', ``high'').
The table's ``delta\_hat'' column is filled with qualitative labels, not
numbers.

This is not validation. It is storytelling.

#### 13. The ``Many Weak Signals'' Regime (Section 13.3) is
Dismissed Too
Quickly<!-- label: the-many-weak-signals-regime-section-13.3-is-dismissed-too-quickly -->

The author acknowledges that for K states with small but balanced
separation, all eigenvalues can be subcritical while the total mutual
information is large. The proposed mitigation is the ``multi-spike
proxy'' (Section 8.4), which sums excess eigenvalues.

But the multi-spike proxy inherits the same problem: if each lambda\_j -
MP\_+ is negative or zero (all eigenvalues within the bulk), the sum is
zero. The ``many weak signals'' regime is not addressed by summing ---
it requires detecting structure BELOW the MP edge, which the spiked
model explicitly cannot do.

The author's worst-case analysis (Section 13.3) uses the example of K
\textgreater= d with means on a sphere. The analysis shows that each
eigenvalue is O(R\^{}2/K). For K \textgreater= d/sqrt(gamma), all
eigenvalues are subcritical. The author admits: ``The spectral proxy
(single-spike) would set delta\_hat = 0, giving a false negative.'' The
mitigation offered is the multi-spike proxy, but the multi-spike proxy
fails in the same regime because all eigenvalues are subcritical.

**This is not a niche case.** For SCX's actual use case of material
science with ACE descriptors, the ``states'' are local atomic
environments: perfect crystal, various defect types, surface sites,
grain boundaries. There can be dozens of distinct states. The state
means lie on a low-dimensional manifold embedded in a high-dimensional
descriptor space. Individual eigenvalues of B may well be small. The
spectral proxy would diagnose ``weak features'' even when the
descriptors are highly informative.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Conclusion<!-- label: conclusion -->

The document claims to build a mathematical bridge between the BBP phase
transition and SCX's mutual information bound. The bridge is not built.
What exists is:

1. 
2. 
3. 
4. 
5. 

The author's own novelty assessment (2.5/5) and publication potential
assessment (``weak'' for a full paper) are more honest than the theorem
statements suggest. The spectral proxy may have practical value as a
heuristic screening tool, but the document's framing as a mathematical
theorem with Parts (a)-(d), Corollaries, and rigorous asymptotic claims
is misleading. The ``theorem'' is not a theorem --- it is a collection
of insights from random matrix theory assembled around a heuristic
proxy, held together by unvalidated assumptions and circular reasoning.

**Recommendation: Reject. Do not resubmit in current form.**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of review.*