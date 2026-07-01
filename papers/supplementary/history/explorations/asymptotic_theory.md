# Asymptotic Theory for SCX: Feasibility Analysis

> SCX has three growing parameters (K, M, n) and currently only finite-sample
> (non-asymptotic) concentration bounds. This document assesses whether it is
> feasible, valuable, and tractable to develop asymptotic theory as these
> parameters jointly go to infinity.

**Date**: 2026-06-27
**Status**: Exploration / feasibility assessment

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current Theoretical Landscape](#2-current-theoretical-landscape)
3. [Feasibility by Regime](#3-feasibility-by-regime)
4. [Low-Hanging Fruit: What Can Be Proved with Standard Tools](#4-low-hanging-fruit-what-can-be-proved-with-standard-tools)
5. [Hard Problems: What Requires New Theory](#5-hard-problems-what-requires-new-theory)
6. [Phase Transition Conjectures](#6-phase-transition-conjectures)
7. [Would Reviewers Care?](#7-would-reviewers-care)
8. [Estimated Effort](#8-estimated-effort)
9. [Recommended First Step](#9-recommended-first-step)
10. [References](#10-references)

---

## 1. Executive Summary

**Verdict**: Asymptotic theory for SCX is feasible in limited regimes (M -> oo
alone; n -> oo alone) but the triple-asymptotic regime (K, M, n -> oo
simultaneously) is PhD-thesis-level work and not recommended as a near-term
goal. The finite-sample bounds already provide stronger guarantees than
asymptotic theory would (exponential convergence rates via Hoeffding, covering
non-identically-distributed summands via Lindeberg-Feller). For the current
paper sequence (AISTATS/TMLR), non-asymptotic bounds are the norm and are
preferred. Asymptotic theory could add value at a later stage (e.g., for
optimal-K selection rules or phase transition characterization), but should
not be a priority.

### Bottom Line

| Regime | Feasibility | Value | Priority |
|--------|------------|-------|----------|
| M -> oo (fixed K, n) | **Trivial** — CLT on C(x) | Low (Hoeffding is tighter) | Low |
| n -> oo (fixed K, M) | **Easy** — consistency of R_m(s) | Low (already have PAC bounds) | Low |
| K -> oo (fixed M, n) | **Moderate** — clustering consistency | Medium (partition recovery) | Medium |
| (K, n) -> oo jointly | **Hard** — clustering + estimation | Medium-High | Medium |
| (K, M, n) -> oo jointly | **PhD-level** — triple asymptotics | High but costly | Low (defer) |

---

## 2. Current Theoretical Landscape

### What Already Exists

The SCX framework currently has three theorems and six propositions, all
finite-sample (non-asymptotic):

| Result | Type | Key Tool | Rate |
|--------|------|----------|------|
| Thm 1: Noise detection guarantee | F1 >= 1 - (1/eta) * exp(-2M*Delta^2) | Hoeffding | Exponential in M |
| Thm 2: Weak feature failure | AUC <= AUC_base + O(sqrt(delta)) | Pinsker + DPI | O(sqrt(delta)) |
| Thm 3: Unidentifiability | Construction-based, no rates | Information theory | N/A |
| Prop 1: Regret lower bound | Regret >= P(bad) * delta_min | Construction | No rate |
| Prop 3: State-conditioned weighting | R_SC <= R_global | Jensen/Gibbs | No rate |
| Prop 4: Compression fidelity | | Rademacher | O(sqrt(d/n')) |

### Key Quantities

The SCX framework has three estimands that could benefit from asymptotic
characterization:

1. **State-conditional risk**: R_m(s) = P(ell(f_m(X), f*(X)) < tau | X in s)
   - Currently: PAC bound via Hoeffding: |R_hat - R| <= L * sqrt(log(2/delta) / (2*n_s))

2. **Consistency score**: C(x) = (1/M) * sum e_m(x)
   - Currently: Exponential concentration via Hoeffding/Chernoff

3. **State discovery**: k-means on phi(X) -> K states
   - Currently: Fano lower bound (Thm 2), no positive result

4. **Noise score**: NS(x) = r(x) * rho(s)^{-1} * (1 - C(s))
   - Currently: no distributional theory for NS(x) itself

### Gap Analysis

The existing theory is strong on **concentration** (how fast estimates converge
to their means) but weak on:
- **Distributional shape**: what does the sampling distribution look like?
- **Joint asymptotics**: how do estimation errors compound across stages?
- **Optimal tuning**: what K is information-theoretically optimal?
- **Phase transitions**: is there a sharp threshold where SCX stops working?

---

## 3. Feasibility by Regime

### 3.1 M -> oo Only (Fixed K, n)

**Setup**: Fix the input distribution, the state partition, and the number of
samples per state. Let the number of experts M grow.

**Target**: C(x) = (1/M) * sum_m e_m(x, y).

**Current status**: Theorem 1 already gives F1 >= 1 - (1/eta) * exp(-2M*Delta^2),
which is an exponential bound. A CLT would give C(x) ~ N(mu, sigma^2/M) for
large M, but this is a **weaker** guarantee (polynomial in 1/sqrt(M) rather
than exponential in M).

**Assessment**: Feasible but not valuable. The Hoeffding/Chernoff bounds are
strictly stronger than any CLT could provide. The CLT would add knowledge
about the shape of the distribution (Gaussian around the mean), but the
concentration is already known to be exponentially fast.

**Difficulty**: Trivial. Standard CLT (or Lindeberg-Feller if experts are
heterogeneous). The only subtlety is the weak dependence induced by label
noise: under (A4), noise samples share a label, creating a common cause.
Solution: condition on the noise label, or note that the dependence is
vanishing as M grows (each expert's error is independent given x and the
noise label).

### 3.2 n -> oo Only (Fixed K, M)

**Setup**: Fix the number of states K and experts M. Let the number of
samples per state n_s grow.

**Target**: R_m(s), SCX_m(s).

**Current status**: PAC bounds give |R_hat - R| = O(1/sqrt(n_s)). As
n_s -> oo, R_hat_m(s) -> R_m(s) almost surely by the strong law of large
numbers.

**What asymptotic theory would add**:
- CLT for R_hat_m(s): sqrt(n_s) * (R_hat - R) -> N(0, sigma^2(s))
- This enables confidence intervals for R_m(s)
- Delta method for w_m(x) = exp(-alpha * R_hat_m(s)): the asymptotic
  distribution of the routing weights

**Assessment**: Feasible and moderately useful (confidence intervals are
practical), but does not add conceptual depth. The existing PAC bounds
already cover the consistency story.

**Difficulty**: Easy. Standard CLT + delta method. The only complication is
that n_s grows endogenously (samples fall into states based on clustering),
but if we condition on the state partition, n_s is just a random variable
with mean n * P(s).

### 3.3 K -> oo Only (Fixed M, n)

**Setup**: Fix the number of experts M and the total sample size n. Let the
number of states K grow.

**Target**: The state partition itself.

**Current status**: Theorem 2 gives a lower bound (if features are weak,
you can't recover states) but no positive result about when state discovery
works.

**What asymptotic theory would add**:
- As K grows, the states become finer, so within-state homogeneity improves
- But each state has fewer samples, so within-state estimates become noisier
- This is a classic bias-variance tradeoff for state discovery
- A consistent partition estimator would prove that as phi(x) becomes
  increasingly informative (e.g., I(phi; S) grows with dimensionality), the
  estimated partition recovers the true partition

**Framework**: This is a clustering consistency problem. For k-means:
- Pollard (1981) gives sqrt(n) consistency for centroids in fixed-K setting
- For growing K, the problem connects to high-dimensional clustering and
  rate-distortion theory
- The relevant quantity is I(phi; S) / (K * log M) — how much information
  is available per cell

**Assessment**: Moderately feasible for *consistency* (does the partition
converge?), harder for *rates* (how fast?). The key difficulty is that the
"true" state partition is itself a modeling choice, not a ground truth
uniquely determined by the data distribution.

**Difficulty**: Hard but tractable. Pollard-style arguments can be extended
to growing K under regularity conditions on the feature distribution (e.g.,
the density is smooth and K grows no faster than n^{1/3}).

### 3.4 (M, n) -> oo Jointly

**Setup**: Both experts and samples grow simultaneously. The canonical
scaling question: what's the optimal ratio between M and n?

**Target**: The interaction between two stages of estimation:
- C(x) = (1/M) * sum e_m(x) becomes more reliable as M grows
- R_m(s) = average loss in state s becomes more reliable as n_s grows

**What asymptotic theory would add**:
- To achieve SCX reliability estimates with error epsilon, need
  M = Omega(log(1/epsilon) / Delta^2) (from Theorem 1) and
  n_s = Omega(K * log M) (from estimation of mu_s)
- The joint scaling M = O(n^alpha) for some alpha determines which error
  source dominates
- An optimal allocation: given total computational budget (M * n = B),
  what split minimizes the F1 error?

**Key technical issue**: The quality of the state partition is itself a
function of n (more data -> better clustering). As n grows, the states
become better estimated, which tightens Assumption (A5) (state homogeneity),
which increases Delta, which reduces the M needed.

**Assessment**: Harder than each in isolation, but there is a literature
on double asymptotics in high-dimensional statistics (Bai & Silverstein,
random matrix theory) and in semi-supervised learning (the "smoothness"
and "cluster" assumptions interact with label propagation).

**Difficulty**: Substantial. Would need to model the feedback from
clustering quality to reliability estimation. The existing Theorem 1
already factors this in implicitly (Delta depends on the state partition
quality, which depends on n and phi). Making this explicit and deriving
joint rates is nontrivial.

### 3.5 (K, M, n) -> oo Jointly

**Setup**: All three parameters grow. The "full SCX limit."

**Target**:
- K grows (finer partition) -> states more homogeneous (A5 tighter) -> Delta increases
- But K grows -> fewer samples per state -> reliability estimates noisier
- M grows -> C(x) and mu_s better estimated -> compensates for noise
- n grows -> states better estimated AND within-state sample size increases

**What asymptotic theory would add**:
- Characterization of the optimal K as a function of M and n
- Phase diagram: (1/delta) - (1/rho) plane where SCX works
- Information-theoretic limits: given I(phi; S), what's the best achievable
  F1 in the limit?
- Connection to universal consistency of state-conditioned rules

**Why this is PhD-level**:

1. **Three-parameter asymptotics are rare in the literature**. Even
   double asymptotics (K, n -> oo) in clustering is active research.
   Triple asymptotics (K, M, n -> oo) with the specific SCX dependency
   structure is essentially novel.

2. **The state partition is not a fixed object**. As K changes, the
   "true" state distribution changes. There's no single limiting object
   — it's a sequence of different models indexed by K.

3. **Interacting error sources**. The state discovery error (K dimension),
   the reliability estimation error (n dimension), and the consistency
   aggregation error (M dimension) compound in a non-additive way.

4. **Missing mathematical infrastructure**. The standard tools (empirical
   process theory, random matrix theory, high-dimensional statistics) each
   handle two-parameter asymptotics but not three. A triple-asymptotic
   result would likely require novel techniques.

**Assessment**: The difficulty is genuinely at the level of a 3-5 year PhD
project. Not recommended as a near-term goal. However, a **partial**
characterization (e.g., phase transition for the special case of binary
states and symmetric experts) could be achievable in 6-12 months.

**Difficulty**: Extremely hard. Would represent a genuine contribution to
statistical learning theory.

---

## 4. Low-Hanging Fruit: What Can Be Proved with Standard Tools

Despite the difficulty of triple asymptotics, there are several results that
can be obtained with off-the-shelf tools and would add value to the SCX
theoretical framework.

### 4.1 Asymptotic Normality of C(x) (Fixed K, n, M -> oo)

**Claim**: Under (A1)-(A3), for any fixed x and any threshold tau, as
M -> oo:

  sqrt(M) * (C(x) - mu(x)) -> N(0, sigma^2(x))

where mu(x) = E[e_m(x) | x] and sigma^2(x) = Var(e_m(x) | x).

**Tools**: Lindeberg-Feller CLT. The Bernoulli variables e_m are independent
given x (by A2) but not identically distributed (different experts have
different error probabilities). The Lindeberg condition is satisfied because
e_m in [0,1] are bounded.

**Value**: Low. The Hoeffding bound already gives P(|C - mu| > t) <=
2 exp(-2 M t^2), which is stronger than what the CLT gives (the CLT says
P(|C - mu| > t) ~ 2 * Phi(-sqrt(M) * t / sigma), which decays as
exp(-M t^2 / (2 sigma^2)) — a similar rate but with a variance-dependent
constant in the exponent).

**However**: The CLT provides the asymptotic distribution, which enables
hypothesis testing. For example, testing H0: "x is clean" vs H1: "x is
noisy" can be done using the asymptotic distribution of C(x).

### 4.2 Confidence Intervals for SCX_m(s) (Fixed K, M, n -> oo)

**Claim**: As n_s -> oo:

  sqrt(n_s) * (SCX_hat_m(s) - SCX_m(s)) -> N(0, SCX_m(s) * (1 - SCX_m(s)))

**Tools**: Standard CLT for binomial proportions. SCX_hat_m(s) is simply the
empirical proportion of successes (error < tau) in state s.

**Note**: The "number of samples in state s" n_s is itself a random variable
(stochastic cluster assignment). But if the state assignment converges as
n -> oo (see 4.3), the conditional CLT holds.

**Value**: Moderate. Enables standard error bars on SCX reliability plots.
Useful for practitioners.

### 4.3 Consistency of k-means State Discovery (n, K -> oo)

**Claim**: Under suitable regularity conditions on phi(X) and the true state
partition, as n -> oo with K = o(n^{1/3}):

  d_H(S_hat, S) -> 0 in probability

where d_H is the Hausdorff distance between the estimated and true cluster
centers, or the misclassification rate if states are well-separated.

**Tools**:
- Pollard (1981, 1982) for k-means consistency with fixed K
- Extensions to growing K: when K grows, need the "excess risk" of
  k-means to vanish, which requires K * log K / n -> 0 (for well-separated
  clusters) or stronger separation conditions
- For the SCX setting, the relevant metric is the partition error rate,
  P(s(x) != s_hat(x)). This is bounded via Fano (Thm 2) but a positive
  consistency result would write:

  P(s != s_hat) -> 0  when I(phi; S) / log K -> oo (i.e., delta << log K)

**Value**: High. This would be the first *positive* result about state
discovery in SCX (Thm 2 only gives a negative result). It would answer:
when does the SCX state discovery procedure actually work?

**Difficulty**: Moderate for well-separated states (standard cluster
consistency). Hard for overlapping states (the typical SCX case).

### 4.4 Delta Method for Expert Routing Weights

**Claim**: As n_s -> oo for all s, the empirical routing weights:

  w_hat_m(x) = exp(-alpha * sum_s gamma_s(x) * R_hat_m(s))

converge in distribution to a log-normal limit (approximately).

**Tools**: Delta method applied to the softmax function. If
sqrt(n) * (R_hat - R) -> N(0, Sigma), then:

  sqrt(n) * (w_hat - w) -> N(0, J * Sigma * J^T)

where J is the Jacobian of the softmax transformation.

**Value**: Moderate. Provides asymptotic confidence intervals for routing
weights. Useful for understanding routing uncertainty.

### 4.5 The Optimal K: Bias-Variance Tradeoff

This is the most valuable "low-hanging fruit" — a precise characterization
of the optimal number of states for SCX.

**Setup**: As K increases:
- Within-state homogeneity improves: sup_{x in s} |P(Y|X=x) - P(Y|X in s)| decreases
  -> mu_s decreases -> Delta increases -> F1 improves
- But sample size per state decreases: n_s ≈ n/K
  -> estimation variance increases -> R_hat_m(s) becomes noisier

**Claim**: Under regularity conditions (Lipschitz conditional distribution
P(Y|X=x) in x), the SCX F1 is optimized at:

  K* ≈ (n * c / log M)^{1/3}

for some constant c depending on the smoothness of P(Y|X=x) and the
geometry of the feature space.

**Derivation sketch**:
- F1 >= 1 - (1/eta) * exp(-2M * Delta^2)
- Delta = (1/2) * (1 - mu * K/(K-1)) ≈ (1/2) * (1 - mu) for large K
- mu_s = average expert error rate in state s
- Bias term: mu_s = mu_global + O(1/K) (as K grows, states homogenize)
  -> mu_s <= c_bias / K -> Delta >= 1/2 - c_bias/(2K)
- Variance term: estimation error in mu_s scales as Var(mu_hat) = O(1/n_s) = O(K/n)
- Worst-case Delta = 1/2 - c_bias/(2K) - c_var * sqrt(K/n)
- Optimizing over K: d/dK [c_bias/K + c_var * sqrt(K/n)] = 0
  -> -c_bias/K^2 + c_var / (2 * sqrt(K * n)) = 0
  -> K* = (2 * c_bias / c_var)^{2/3} * n^{1/3}

**Imposing the M requirement**: For the F1 guarantee to be tight, we also
need M > 1/(2*Delta^2) * log(2/(eta*epsilon)). With K* = O(n^{1/3}),
Delta = Omega(1), the M requirement is asymptotically constant (does not grow
with n).

**Value**: Very high. This would give practitioners a principled way to
choose K given n and M. It would be a practically useful theorem.

---

## 5. Hard Problems: What Requires New Theory

### 5.1 Joint Distribution of the SCX Score

**Problem**: Characterize the joint asymptotic distribution of
(SCX_1(s), ..., SCX_M(s), C(x), NS(x)) as all parameters grow.

**Why it's hard**: The SCX score is a two-stage estimator:
1. First stage: estimate the state partition (clustering)
2. Second stage: estimate within-state reliability (averaging)

These stages share data (the same n samples are used for both), creating
complex dependence that standard asymptotics cannot handle. The state
partition is a function of the full data, making all subsequent estimates
conditionally dependent even after conditioning on the true states.

**Known results in related areas**:
- "Post-clustering inference" (Lockhart et al., 2014; Lee et al., 2016):
  selective inference after model selection. But this is for regression
  coefficients after LASSO, not for plug-in estimates after clustering.
- "Double dipping" (Kriegeskorte et al., 2009): a known problem in
  neuroscience where the same data is used for selection and estimation.

**Difficulty**: PhD thesis level. Would require novel selective inference
tools for clustering-based two-stage estimation.

### 5.2 Optimal Scaling Rates for Triple Asymptotics

**Problem**: Find the optimal scaling relationship between K, M, and n such
that SCX achieves consistency (F1 -> 1) at the fastest possible rate.

**The information-theoretic question**: Given:
- A fixed total sample budget T = M * n (total training samples across all experts)
- A fixed feature space dimensionality d
- A data distribution P with true state structure

What scaling K = f(T, d), M = g(T, d), n = h(T, d) minimizes the asymptotic
F1 error?

**Why it's hard**:
1. Three-way tradeoff: M controls detection power, n controls estimation
   precision, K controls partitioning granularity
2. All three consume resources: more experts means fewer samples per expert
   (if total data fixed); more states means fewer samples per state
3. The optimal scaling likely depends on the smoothness of P(Y|X) and the
   clusterability of phi(X)
4. This is a constrained optimization problem over the space of
   (K, M, n) -> F1, where F1 is a complex function of all three

**Connection to known results**:
- In high-dimensional classification, the optimal rate involves
  n / (d * log p) scaling (Fan & Fan, 2008). This is a two-parameter problem.
- In clustering, the optimal K scales as n^{d/(d+2)} for density-based
  clustering (the "silverman" bandwidth rule). But SCX is not density-based.
- The SCX triple is structurally more complex than either of these.

**Difficulty**: Open research problem. Would be a significant theoretical
contribution if solved.

### 5.3 Asymptotic Distribution under Model Misspecification

**Problem**: What happens to SCX when the state partition model is wrong?
Specifically, when the true distribution P(Y|X) does not factor through a
finite-state partition.

**The issue**: SCX assumes P(Y|X) ≈ P(Y|phi(X)) where phi(X) is discrete
with K states. If this assumption is false (e.g., Y depends on X in a
continuous way that no finite partition can capture), what does the SCX
estimator converge to?

**What happens in the limit**:
- As K -> oo, any continuous function can be approximated arbitrarily well
  by a step function (the partition becomes a Riemann sum approximation).
  So SCX should be "universally consistent" as K -> oo with n -> oo
  (provided K grows at the right rate).
- But as K -> oo with fixed n, the within-state estimates become
  inconsistent (no samples per state).

**Why it's hard**: Proving universal consistency of SCX requires:
1. Showing that the excess risk due to state discretization vanishes as
   K -> oo (approximation error)
2. Showing that within-state estimation error vanishes as n -> oo
   (estimation error)
3. Balancing K and n to minimize the sum

This is a **nonparametric regression with state discretization** problem.
The rate would be analogous to nonparametric rate for partitioning
estimators, but with the additional complexity of the multi-expert
aggregation.

**Difficulty**: Hard but tractable. Follows the standard sieve/penalized
M-estimation framework (Grenander, 1981; Shen & Wong, 1994).

### 5.4 Phase Transition in the (delta, eta, K) Space

**Problem**: Characterize the sharp threshold where SCX goes from "works"
to "fails" as a function of feature-information delta, noise rate eta,
and number of states K.

**Conjecture**: There is a sharp phase transition in the (delta, eta) plane,
separated by a curve delta_c(eta, K). Below this curve, F1 -> F1_base
(SCX does not help). Above it, F1 -> 1 (SCX works perfectly).

**Why it's hard**:
1. Phase transitions in statistical learning are rare (e.g., the
   "all-or-nothing" phenomenon in compressed sensing). Most learning
   problems have smooth transitions.
2. The SCX phase transition (if it exists) is in the F1 score, which is
   a discrete metric (it involves thresholded decisions). Continuous
   metrics like AUC may not show sharp transitions.
3. Proving a phase transition requires: (a) existence of a threshold where
   behavior changes, (b) showing the transition is sharp (gap vanishes in
   the limit), (c) characterizing the threshold location.
4. The triple-parameter space makes this even harder.

**Difficulty**: Extremely hard for rigorous proof. Moderate for heuristic
or physics-style analysis (e.g., replica method or cavity method).

---

## 6. Phase Transition Conjectures

Despite the difficulty of rigorous proof, we can conjecture the phase
diagram based on the existing finite-sample bounds.

### 6.1 The (K, M, n) Phase Diagram

SCX "works" (F1 -> 1 asymptotically) in the following regime:

```
Condition 1 (State recovery):  I(phi; S) / log K -> oo  (features carry
                                enough information to resolve K states)

Condition 2 (Detection power): M * Delta^2 / log M -> oo  (enough experts
                                to separate clean from noisy)

Condition 3 (Estimation):      n * P_min / (K * log M) -> oo  (enough
                                samples to estimate within-state rates)
```

where P_min = min_s P(s) is the minimum state probability, and Delta is the
mean separation gap from Theorem 1.

If any of these conditions fail, SCX degrades in a specific way:
- Condition 1 fails (delta >> log K): states are unrecoverable, SCX noise
  detection degenerates to loss baseline (Thm 2 regime)
- Condition 2 fails (M * Delta^2 small): C(x) is too noisy to separate
  clean from noisy; F1 stuck below some constant < 1
- Condition 3 fails (n * P_min small): within-state estimates are pure noise;
  state-conditioned weighting becomes worse than global weighting

### 6.2 The Sharpness Conjecture

The most likely candidate for a sharp phase transition is in **Condition 2**
(the detection phase transition), because:

1. Theorem 1 gives F1 >= 1 - (1/eta) * exp(-2M * Delta^2)
2. This shows that F1 -> 1 **exponentially fast** when M * Delta^2 -> oo
3. Conversely, when M * Delta^2 -> 0, the bound becomes trivial (F1 >= -oo)
4. But is there a converse? If M * Delta^2 is small, is F1 bounded away from
   1? A minimax lower bound would confirm a phase transition.

**Conjectured minimax lower bound**: There exists a data distribution
satisfying (A1)-(A6) such that, for any detection algorithm:

  E[F1] <= 1 - c * exp(-C * M * Delta^2)

for some constants c, C > 0. This would show that the exponential rate in
Theorem 1 is tight (up to constants) and that M * Delta^2 is the correct
phase transition parameter.

**Proof approach**: Construct a Le Cam two-point testing problem where
the null is "all samples clean" and the alternative is "eta-fraction
noisy." The minimax risk of testing these two hypotheses is
exp(-M * KL(C_clean || C_noisy)) which scales as exp(-M * Delta^2).

### 6.3 The Triple Phase Transition

The full phase transition (K, M, n jointly) would have the form:

```
Phase 1 (SCX works):    K * log(K) / n << 1    AND  M * Delta^2 / log M >> 1
Phase 2 (State failure):  K * log K / n >> 1    (features too weak or K too
                                                  large for given n)
Phase 3 (Detection failure): M * Delta^2 / log M << 1  (too few experts)
Phase 4 (Double failure): Both Phase 2 and Phase 3 hold
```

In Phase 2, SCX noise detection works no better than the loss baseline
(Thm 2 applies). In Phase 3, the detection guarantee fails but the state
discovery may still be valid (SCX can still be useful for expert routing,
just not for noise detection). In Phase 4, SCX entirely fails for all tasks.

---

## 7. Would Reviewers Care?

### 7.1 AISTATS / TMLR / NeurIPS Norms

**Current norm**: Non-asymptotic (finite-sample) bounds are standard and
preferred in top ML venues. The majority of learning theory papers at
NeurIPS, ICML, COLT, and AISTATS use PAC-style bounds.

**Why finite-sample is preferred**:
1. **Non-asymptotic bounds are stronger**: they hold for any finite n, M, K,
   not just "in the limit." A reviewer who sees both a CLT (asymptotic) and
   a Hoeffding bound (finite-sample) will correctly note that the Hoeffding
   bound is strictly more informative for practical sample sizes.
2. **Rate-sharpness is the focus**: what matters is how fast the error
   decays in n/M/K, not the limiting distribution. The exponential rate
   in M from Theorem 1 is more impactful than a CLT would be.
3. **Asymptotic arguments can hide complexity**: Dependencies that matter
   at finite sample sizes wash out in the limit. Reviewers are suspicious
   of asymptotic arguments that ignore these dependencies.

### 7.2 When Asymptotics Add Value

There are specific scenarios where asymptotic results strengthen a paper:

1. **Minimax lower bounds**: These are often asymptotic (n -> oo for
   fixed d, or d -> oo with n) but provide fundamental limits. A minimax
   lower bound for SCX (e.g., "no algorithm can achieve F1 > constant
   unless M * Delta^2 > threshold") would be a strong contribution.

2. **Phase transitions**: The compressed sensing literature (Donoho,
   Candes, Tao) was hugely influential precisely because it characterized
   a sharp phase transition. If SCX has a provable phase transition, it
   would be a major selling point.

3. **Optimal scaling**: A result like "the optimal K scales as
   K* ~ (n / log M)^{1/3}" would be practically useful and theoretically
   interesting. It would show that the theory has actionable implications.

4. **Asymptotic equivalence**: Showing that SCX is asymptotically
   equivalent to some well-studied procedure (e.g., the Bayes classifier
   for the state-conditional model) would legitimize the approach.

### 7.3 Recommended Position for Current Papers

**For the first SCX paper** (primary submission):
- Keep the current finite-sample bounds (Theorems 1-3)
- Add the following asymptotic *conjectures* as open problems in the
  discussion section (not as main results):
  - "The optimal number of states K* is conjectured to scale as O(n^{1/3})"
  - "A phase transition in M * Delta^2 is conjectured"
- This shows the authors are aware of the asymptotic questions without
  requiring full proofs

**For the second SCX paper** (follow-up):
- One clean asymptotic result (e.g., the optimal K scaling or a minimax
  lower bound) would strengthen the theoretical contribution
- By then, the framework will be established, and the asymptotic question
  will be a natural next step

### 7.4 Review Criteria

What a reviewer would look for in asymptotic theory:

| Criterion | What they want | How SCX scores |
|-----------|---------------|----------------|
| Novelty | Is this a new result or an application of an existing technique? | Moderate-high (unique triple structure) |
| Cleanliness | Is the result clean and interpretable? | Potentially high (phase transitions are inherently clean) |
| Assumptions | Are assumptions justified? | Tricky (asymptotics require stronger assumptions) |
| Practicality | Does the result help practitioners? | High if optimal K is derived |
| Technical depth | Is the proof nontrivial? | Would be, for triple asymptotics |

---

## 8. Estimated Effort

### Feasibility Matrix: Effort vs. Impact

| Result | Effort | Impact | Ratio | Priority |
|--------|--------|--------|-------|----------|
| CLT for C(x) (M -> oo) | 1-2 days | Low | Low | 4 |
| CI for SCX_m(s) (n -> oo) | 2-3 days | Low-Moderate | Medium | 3 |
| k-means consistency (n, K -> oo) | 2-4 weeks | High | High | **1** |
| Optimal K scaling | 2-4 weeks | Very high | Very high | **1** |
| Delta method for routing weights | 1 week | Low-Moderate | Low | 4 |
| Minimax lower bound (M vs F1) | 2-4 weeks | High | High | **2** |
| Joint (M, n) asymptotics | 1-3 months | Medium-High | Medium | 5 |
| Triple (K, M, n) asymptotics | 3-12 months | Very high | Low (cost) | 6 |
| Phase transition (full) | 3-12 months | Very high | Low (cost) | 6 |
| Post-clustering inference for SCX | 3-6 months | High | Medium | 5 |
| Universal consistency (nonparametric) | 2-6 months | High | Medium | 5 |

### Recommended Priority Order

**Phase 1 (before first paper submission, 1-2 months)**:
1. Cluster consistency: prove that k-means on phi(X) recovers the true
   partition as n, K -> oo, under appropriate conditions (informally:
   "the SCX state discovery procedure is consistent")
2. Optimal K scaling: derive K* ≈ (n / log M)^{1/dimension} from the
   bias-variance tradeoff (informally: "K should grow slowly with n")

**Phase 2 (between submission and revision, 1-2 months)**:
3. Minimax lower bound for F1: show that no detector can exceed
   F1 > 1 - c * exp(-C * M * Delta^2), proving Theorem 1 optimal up to
   constants (informally: "SCX's detection rate is fundamentally optimal")

**Phase 3 (for follow-up paper, 3-6 months)**:
4. One clean triple-asymptotic result for a restricted setting
   (e.g., binary states, symmetric experts, Gaussian features)

### Total Time

- **Phase 1**: 1-2 months (1 competent theoretician, or 1 month full-time)
- **Phase 1 + 2**: 2-4 months
- **All phases**: 6-12 months (or a dedicated PhD student over 2 years)

---

## 9. Recommended First Step

### Choose One Regime: Cluster Consistency for State Discovery

The single most valuable and tractable asymptotic result is:

**"Consistency of k-means State Discovery in SCX"**

**Statement**: For the SCX state discovery procedure (k-means clustering on
feature vectors phi(x_i)), as the number of training samples n -> oo and the
number of states K grows with n:

  If K = o(n^{1/3}) and the features are regular enough (the "true"
  partition has well-separated components in phi-space), then:

  lim_{n -> oo} P(estimated partition != true partition) = 0

  Furthermore, if K scales as K* ~ C * n^{1/3} (for a known constant C
  depending on cluster geometry), the bias-variance tradeoff is optimized.

**Why this is the right first step**:
1. It addresses a real gap: Thm 2 only gives negative results for state
   discovery. A positive consistency result is long overdue.
2. It connects to a mature literature (Pollard, 1981; Von Luxburg, 2007;
   Rakhlin & Caponnetto, 2007) so the technical path is clear.
3. It produces a practically useful output (guidance on choosing K).
4. It can be written as a self-contained result that doesn't require
   simultaneous asymptotic analysis of M and n.

### What the Proof Would Need

1. **Assumptions**:
   - The "true" state partition corresponds to K well-separated components
     in phi-space (e.g., the level sets of a density, or Voronoi cells of
     K centroids)
   - The feature map phi is Lipschitz continuous
   - The within-state homogeneity (A5) is satisfied exactly at the true
     partition, with Delta > 0

2. **Steps**:
   a. Show that k-means minimizes an empirical risk function
   b. Show that this risk converges uniformly to its population version
      (via uniform laws of large numbers / Glivenko-Cantelli)
   c. Show that the population risk minimizer corresponds to the true
      partition (identifiability)
   d. Conclude that the empirical minimizer converges to the truth
   e. Derive rates: typically O_p(K * log K / n) for the misclustering rate

3. **Standard references**:
   - Pollard (1981, Annals of Statistics): "Strong consistency of k-means
     clustering" — the classic result for fixed K
   - Rakhlin & Caponnetto (2007, NIPS): "Stability of k-means clustering"
     — covers growing K but requires well-separated clusters
   - Von Luxburg (2007, Statistics and Computing): "A tutorial on spectral
     clustering" — includes consistency results

### Deliverable

A 2-3 page proof (or a section in the existing Thm 2 document) showing:

1. **Theorem (SCX State Discovery Consistency)**:
   Under conditions (sufficient feature information, well-separated true
   states, K growing slowly enough), the k-means state discovery procedure
   used in SCX recovers the true state partition with probability -> 1.

2. **Corollary (Optimal K)**:
   The number of states K* that minimizes the expected misclassification
   rate scales as O(n^{1/3}). This is derived from balancing the
   approximation error (bias from using a finite K) against the estimation
   error (variance from finite samples per state).

3. **Practical guidance**:
   For SCX practitioners: choose K ≈ n^{1/3} as a default, and check
   sensitivity by running with K/2 and 2K.

---

## 10. References

### Existing SCX Theory

- Theorem 1: Multi-Expert Consistency Guarantees for Label Noise Detection
  (`theory/theorems/01_noise_detection_guarantee.md`)
- Theorem 2: Weak Feature Failure Lower Bound
  (`theory/theorems/02_weak_feature_failure.md`)
- Theorem 3: Unidentifiability of Noise vs. Learnable Difficulty
  (`theory/theorems/03_unidentifiability_theorem.md`)

### Asymptotic Clustering Theory

- Pollard, D. (1981). Strong consistency of k-means clustering. *Annals of
  Statistics*, 9(1), 135-140.
- Pollard, D. (1982). A central limit theorem for k-means clustering.
  *Annals of Statistics*, 10(3), 919-926.
- Rakhlin, A., & Caponnetto, A. (2007). Stability of k-means clustering.
  *NIPS*.
- Von Luxburg, T. (2007). A tutorial on spectral clustering. *Statistics
  and Computing*, 17(4), 395-416.
- Lei, J., & Rinaldo, A. (2015). Consistency of spectral clustering in
  stochastic block models. *Annals of Statistics*, 43(1), 215-237.

### High-Dimensional and Double Asymptotics

- Bai, Z. D., & Silverstein, J. W. (2010). *Spectral Analysis of Large
  Dimensional Random Matrices* (2nd ed.). Springer.
- Fan, J., & Fan, Y. (2008). High-dimensional classification using features
  annealed independence rules. *Annals of Statistics*, 36(6), 2605-2637.
- Wainwright, M. J. (2019). *High-Dimensional Statistics: A Non-Asymptotic
  Viewpoint*. Cambridge University Press.

### Selective Inference / Post-Clustering

- Lockhart, R., Taylor, J., Tibshirani, R. J., & Tibshirani, R. (2014).
  A significance test for the LASSO. *Annals of Statistics*, 42(2), 413-468.
- Lee, J. D., Sun, D. L., Sun, Y., & Taylor, J. E. (2016). Exact post-
  selection inference, with application to the LASSO. *Annals of
  Statistics*, 44(3), 907-927.
- Benjamini, Y., & Heller, R. (2007). False discovery rates for spatial
  signals. *Journal of the American Statistical Association*.

### Nonparametric Sieve Estimation

- Grenander, U. (1981). *Abstract Inference*. Wiley.
- Shen, X., & Wong, W. H. (1994). Convergence rate of sieve estimates.
  *Annals of Statistics*, 22(2), 580-615.
- van de Geer, S. (2000). *Empirical Processes in M-Estimation*.
  Cambridge University Press.

### Phase Transitions in Learning

- Donoho, D. L., & Tanner, J. (2009). Observed universality of phase
  transitions in high-dimensional geometry. *PNAS*, 106(51), 21641-21645.
- Candes, E. J., & Tao, T. (2005). Decoding by linear programming. *IEEE
  Transactions on Information Theory*, 51(12), 4203-4215.
- Wainwright, M. J. (2009). Sharp thresholds for high-dimensional and noisy
  sparsity recovery. *IEEE Transactions on Information Theory*, 55(5),
  2183-2202.

---

## Appendix: Quick Reference — Parameter Roles in SCX

| Parameter | Role | Grows -> Effect | Finite-sample result | Asymptotic target |
|-----------|------|-----------------|---------------------|-------------------|
| K | Number of states | Finer partition, fewer samples per state | Thm 2: Fano bound on recovery | Optimal K* scaling |
| M | Number of experts | More reliable consistency score | Thm 1: F1 exp(-M * Delta^2) | Minimax lower bound |
| n | Samples per state | More precise within-state estimates | PAC: O(1/sqrt(n_s)) | CLT for SCX_m(s) |
| eta | Noise rate | More detectable noise | Appears in F1 bound | Phase boundary |
| delta | Feature info | Better state recovery | Thm 2: AUC <= baseline + O(sqrt(delta)) | Phase boundary |

The key mathematical quantities and their asymptotic behavior:

```
SCX_m(s) = P(ell(f_m(x), y) < tau | x in s)
  As n_s -> oo: sqrt(n_s) * (SCX_hat - SCX) ~ N(0, SCX * (1-SCX))

C(x) = (1/M) * sum e_m(x)
  As M -> oo: C(x) -> mu(x) a.s.;  sqrt(M) * (C - mu) ~ N(0, sigma^2)

F1 >= 1 - (1/eta) * exp(-2M * Delta^2)
  As M * Delta^2 -> oo: F1 -> 1 at exponential rate

K* ≈ (n / log M)^{1/3}  [conjectured optimal scaling]
```
