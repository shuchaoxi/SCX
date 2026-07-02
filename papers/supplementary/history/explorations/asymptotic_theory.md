# Asymptotic Theory for SCX: Feasibility
Analysis

**Author:** SCX

> SCX has three growing parameters (K, M, n) and currently only
> finite-sample (non-asymptotic) concentration bounds. This document
> assesses whether it is feasible, valuable, and tractable to develop
> asymptotic theory as these parameters jointly go to infinity.

**Date**: 2026-06-27 **Status**: Exploration / feasibility
assessment

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

### 1. Executive Summary<!-- label: executive-summary -->

**Verdict**: Asymptotic theory for SCX is feasible in limited
regimes (M -\textgreater{} oo alone; n -\textgreater{} oo alone) but the
triple-asymptotic regime (K, M, n -\textgreater{} oo simultaneously) is
PhD-thesis-level work and not recommended as a near-term goal. The
finite-sample bounds already provide stronger guarantees than asymptotic
theory would (exponential convergence rates via Hoeffding, covering
non-identically-distributed summands via Lindeberg-Feller). For the
current paper sequence (AISTATS/TMLR), non-asymptotic bounds are the
norm and are preferred. Asymptotic theory could add value at a later
stage (e.g., for optimal-K selection rules or phase transition
characterization), but should not be a priority.

#### Bottom Line<!-- label: bottom-line -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2162}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3243}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1892}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2703}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Regime
\end{minipage} & \begin{minipage}[b]
Feasibility
\end{minipage} & \begin{minipage}[b]
Value
\end{minipage} & \begin{minipage}[b]
Priority
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
M -\textgreater{} oo (fixed K, n) & **Trivial** --- CLT on C(x) &
Low (Hoeffding is tighter) & Low 

n -\textgreater{} oo (fixed K, M) & **Easy** --- consistency of
R\_m(s) & Low (already have PAC bounds) & Low 

K -\textgreater{} oo (fixed M, n) & **Moderate** --- clustering
consistency & Medium (partition recovery) & Medium 

(K, n) -\textgreater{} oo jointly & **Hard** --- clustering +
estimation & Medium-High & Medium 

(K, M, n) -\textgreater{} oo jointly & **PhD-level** --- triple
asymptotics & High but costly & Low (defer) 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Current Theoretical
Landscape<!-- label: current-theoretical-landscape -->

#### What Already Exists<!-- label: what-already-exists -->

The SCX framework currently has three theorems and six propositions, all
finite-sample (non-asymptotic):

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2667}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Result
\end{minipage} & \begin{minipage}[b]
Type
\end{minipage} & \begin{minipage}[b]
Key Tool
\end{minipage} & \begin{minipage}[b]
Rate
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Thm 1: Noise detection guarantee & F1 \textgreater= 1 - (1/eta) *
exp(-2M*Delta\^{}2) & Hoeffding & Exponential in M 

Thm 2: Weak feature failure & AUC \textless= AUC\_base + O(sqrt(delta))
& Pinsker + DPI & O(sqrt(delta)) 

Thm 3: Unidentifiability & Construction-based, no rates & Information
theory & N/A 

Prop 1: Regret lower bound & Regret \textgreater= P(bad) * delta\_min &
Construction & No rate 

Prop 3: State-conditioned weighting & R\_SC \textless= R\_global &
Jensen/Gibbs & No rate 

Prop 4: Compression fidelity & & Rademacher & O(sqrt(d/n')) 

\end{longtable}

#### Key Quantities<!-- label: key-quantities -->

The SCX framework has three estimands that could benefit from asymptotic
characterization:

1. 
2. 
3. 
4. 

#### Gap Analysis<!-- label: gap-analysis -->

The existing theory is strong on **concentration** (how fast
estimates converge to their means) but weak on: - **Distributional
shape**: what does the sampling distribution look like? - **Joint
asymptotics**: how do estimation errors compound across stages? -
**Optimal tuning**: what K is information-theoretically optimal? -
**Phase transitions**: is there a sharp threshold where SCX stops
working?

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Feasibility by Regime<!-- label: feasibility-by-regime -->

#### 3.1 M -\textgreater{ oo Only (Fixed K,
n)}<!-- label: m---oo-only-fixed-k-n -->

**Setup**: Fix the input distribution, the state partition, and the
number of samples per state. Let the number of experts M grow.

**Target**: C(x) = (1/M) * sum\_m e\_m(x, y).

**Current status**: Theorem 1 already gives F1 \textgreater= 1 -
(1/eta) * exp(-2M*Delta\^{}2), which is an exponential bound. A CLT
would give C(x) ~{} N(mu, sigma\^{}2/M) for large M, but
this is a **weaker** guarantee (polynomial in 1/sqrt(M) rather than
exponential in M).

**Assessment**: Feasible but not valuable. The Hoeffding/Chernoff
bounds are strictly stronger than any CLT could provide. The CLT would
add knowledge about the shape of the distribution (Gaussian around the
mean), but the concentration is already known to be exponentially fast.

**Difficulty**: Trivial. Standard CLT (or Lindeberg-Feller if
experts are heterogeneous). The only subtlety is the weak dependence
induced by label noise: under (A4), noise samples share a label,
creating a common cause. Solution: condition on the noise label, or note
that the dependence is vanishing as M grows (each expert's error is
independent given x and the noise label).

#### 3.2 n -\textgreater{ oo Only (Fixed K,
M)}<!-- label: n---oo-only-fixed-k-m -->

**Setup**: Fix the number of states K and experts M. Let the number
of samples per state n\_s grow.

**Target**: R\_m(s), SCX\_m(s).

**Current status**: PAC bounds give | R\_hat - R|{} =
O(1/sqrt(n\_s)). As n\_s -\textgreater{} oo, R\_hat\_m(s)
-\textgreater{} R\_m(s) almost surely by the strong law of large
numbers.

**What asymptotic theory would add**: - CLT for R\_hat\_m(s):
sqrt(n\_s) * (R\_hat - R) -\textgreater{} N(0, sigma\^{}2(s)) - This
enables confidence intervals for R\_m(s) - Delta method for w\_m(x) =
exp(-alpha * R\_hat\_m(s)): the asymptotic distribution of the routing
weights

**Assessment**: Feasible and moderately useful (confidence
intervals are practical), but does not add conceptual depth. The
existing PAC bounds already cover the consistency story.

**Difficulty**: Easy. Standard CLT + delta method. The only
complication is that n\_s grows endogenously (samples fall into states
based on clustering), but if we condition on the state partition, n\_s
is just a random variable with mean n * P(s).

#### 3.3 K -\textgreater{ oo Only (Fixed M,
n)}<!-- label: k---oo-only-fixed-m-n -->

**Setup**: Fix the number of experts M and the total sample size
n.~Let the number of states K grow.

**Target**: The state partition itself.

**Current status**: Theorem 2 gives a lower bound (if features are
weak, you can't recover states) but no positive result about when state
discovery works.

**What asymptotic theory would add**: - As K grows, the states
become finer, so within-state homogeneity improves - But each state has
fewer samples, so within-state estimates become noisier - This is a
classic bias-variance tradeoff for state discovery - A consistent
partition estimator would prove that as phi(x) becomes increasingly
informative (e.g., I(phi; S) grows with dimensionality), the estimated
partition recovers the true partition

**Framework**: This is a clustering consistency problem. For
k-means: - Pollard (1981) gives sqrt(n) consistency for centroids in
fixed-K setting - For growing K, the problem connects to
high-dimensional clustering and rate-distortion theory - The relevant
quantity is I(phi; S) / (K * log M) --- how much information is
available per cell

**Assessment**: Moderately feasible for *consistency* (does
the partition converge?), harder for *rates* (how fast?). The key
difficulty is that the ``true'' state partition is itself a modeling
choice, not a ground truth uniquely determined by the data distribution.

**Difficulty**: Hard but tractable. Pollard-style arguments can be
extended to growing K under regularity conditions on the feature
distribution (e.g., the density is smooth and K grows no faster than
n\^{}\{1/3\}).

#### 3.4 (M, n) -\textgreater{ oo
Jointly}<!-- label: m-n---oo-jointly -->

**Setup**: Both experts and samples grow simultaneously. The
canonical scaling question: what's the optimal ratio between M and n?

**Target**: The interaction between two stages of estimation: -
C(x) = (1/M) * sum e\_m(x) becomes more reliable as M grows - R\_m(s) =
average loss in state s becomes more reliable as n\_s grows

**What asymptotic theory would add**: - To achieve SCX reliability
estimates with error epsilon, need M = Omega(log(1/epsilon) /
Delta\^{}2) (from Theorem 1) and n\_s = Omega(K * log M) (from
estimation of mu\_s) - The joint scaling M = O(n\^{}alpha) for some
alpha determines which error source dominates - An optimal allocation:
given total computational budget (M * n = B), what split minimizes the
F1 error?

**Key technical issue**: The quality of the state partition is
itself a function of n (more data -\textgreater{} better clustering). As
n grows, the states become better estimated, which tightens Assumption
(A5) (state homogeneity), which increases Delta, which reduces the M
needed.

**Assessment**: Harder than each in isolation, but there is a
literature on double asymptotics in high-dimensional statistics (Bai \&
Silverstein, random matrix theory) and in semi-supervised learning (the
``smoothness'' and ``cluster'' assumptions interact with label
propagation).

**Difficulty**: Substantial. Would need to model the feedback from
clustering quality to reliability estimation. The existing Theorem 1
already factors this in implicitly (Delta depends on the state partition
quality, which depends on n and phi). Making this explicit and deriving
joint rates is nontrivial.

#### 3.5 (K, M, n) -\textgreater{ oo
Jointly}<!-- label: k-m-n---oo-jointly -->

**Setup**: All three parameters grow. The ``full SCX limit.''

**Target**: - K grows (finer partition) -\textgreater{} states more
homogeneous (A5 tighter) -\textgreater{} Delta increases - But K grows
-\textgreater{} fewer samples per state -\textgreater{} reliability
estimates noisier - M grows -\textgreater{} C(x) and mu\_s better
estimated -\textgreater{} compensates for noise - n grows
-\textgreater{} states better estimated AND within-state sample size
increases

**What asymptotic theory would add**: - Characterization of the
optimal K as a function of M and n - Phase diagram: (1/delta) - (1/rho)
plane where SCX works - Information-theoretic limits: given I(phi; S),
what's the best achievable F1 in the limit? - Connection to universal
consistency of state-conditioned rules

**Why this is PhD-level**:

1. 
2. 
3. 
4. 

**Assessment**: The difficulty is genuinely at the level of a 3-5
year PhD project. Not recommended as a near-term goal. However, a
**partial** characterization (e.g., phase transition for the
special case of binary states and symmetric experts) could be achievable
in 6-12 months.

**Difficulty**: Extremely hard. Would represent a genuine
contribution to statistical learning theory.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Low-Hanging Fruit: What Can Be Proved with Standard
Tools<!-- label: low-hanging-fruit-what-can-be-proved-with-standard-tools -->

Despite the difficulty of triple asymptotics, there are several results
that can be obtained with off-the-shelf tools and would add value to the
SCX theoretical framework.

#### 4.1 Asymptotic Normality of C(x) (Fixed K, n, M
-\textgreater{ oo)}<!-- label: asymptotic-normality-of-cx-fixed-k-n-m---oo -->

**Claim**: Under (A1)-(A3), for any fixed x and any threshold tau,
as M -\textgreater{} oo:

sqrt(M) * (C(x) - mu(x)) -\textgreater{} N(0, sigma\^{}2(x))

where mu(x) = E{[}e\_m(x) |{} x{]} and sigma\^{}2(x) =
Var(e\_m(x) |{} x).

**Tools**: Lindeberg-Feller CLT. The Bernoulli variables e\_m are
independent given x (by A2) but not identically distributed (different
experts have different error probabilities). The Lindeberg condition is
satisfied because e\_m in {[}0,1{]} are bounded.

**Value**: Low. The Hoeffding bound already gives P(| C -
mu|{} \textgreater{} t) \textless= 2 exp(-2 M t\^{}2), which is
stronger than what the CLT gives (the CLT says P(| C -
mu|{} \textgreater{} t) ~{} 2 * Phi(-sqrt(M) * t /
sigma), which decays as exp(-M t\^{}2 / (2 sigma\^{}2)) --- a similar
rate but with a variance-dependent constant in the exponent).

**However**: The CLT provides the asymptotic distribution, which
enables hypothesis testing. For example, testing H0: ``x is clean'' vs
H1: ``x is noisy'' can be done using the asymptotic distribution of
C(x).

#### 4.2 Confidence Intervals for SCX\_m(s) (Fixed K, M, n
-\textgreater{
oo)}<!-- label: confidence-intervals-for-scx_ms-fixed-k-m-n---oo -->

**Claim**: As n\_s -\textgreater{} oo:

sqrt(n\_s) * (SCX\_hat\_m(s) - SCX\_m(s)) -\textgreater{} N(0, SCX\_m(s)
* (1 - SCX\_m(s)))

**Tools**: Standard CLT for binomial proportions. SCX\_hat\_m(s) is
simply the empirical proportion of successes (error \textless{} tau) in
state s.

**Note**: The ``number of samples in state s'' n\_s is itself a
random variable (stochastic cluster assignment). But if the state
assignment converges as n -\textgreater{} oo (see 4.3), the conditional
CLT holds.

**Value**: Moderate. Enables standard error bars on SCX reliability
plots. Useful for practitioners.

#### 4.3 Consistency of k-means State Discovery (n, K
-\textgreater{
oo)}<!-- label: consistency-of-k-means-state-discovery-n-k---oo -->

**Claim**: Under suitable regularity conditions on phi(X) and the
true state partition, as n -\textgreater{} oo with K = o(n\^{}\{1/3\}):

d\_H(S\_hat, S) -\textgreater{} 0 in probability

where d\_H is the Hausdorff distance between the estimated and true
cluster centers, or the misclassification rate if states are
well-separated.

**Tools**: - Pollard (1981, 1982) for k-means consistency with
fixed K - Extensions to growing K: when K grows, need the ``excess
risk'' of k-means to vanish, which requires K * log K / n
-\textgreater{} 0 (for well-separated clusters) or stronger separation
conditions - For the SCX setting, the relevant metric is the partition
error rate, P(s(x) != s\_hat(x)). This is bounded via Fano (Thm 2) but a
positive consistency result would write:

P(s != s\_hat) -\textgreater{} 0 when I(phi; S) / log K -\textgreater{}
oo (i.e., delta \textless\textless{} log K)

**Value**: High. This would be the first *positive* result
about state discovery in SCX (Thm 2 only gives a negative result). It
would answer: when does the SCX state discovery procedure actually work?

**Difficulty**: Moderate for well-separated states (standard
cluster consistency). Hard for overlapping states (the typical SCX
case).

#### 4.4 Delta Method for Expert Routing
Weights<!-- label: delta-method-for-expert-routing-weights -->

**Claim**: As n\_s -\textgreater{} oo for all s, the empirical
routing weights:

w\_hat\_m(x) = exp(-alpha * sum\_s gamma\_s(x) * R\_hat\_m(s))

converge in distribution to a log-normal limit (approximately).

**Tools**: Delta method applied to the softmax function. If sqrt(n)
* (R\_hat - R) -\textgreater{} N(0, Sigma), then:

sqrt(n) * (w\_hat - w) -\textgreater{} N(0, J * Sigma * J\^{}T)

where J is the Jacobian of the softmax transformation.

**Value**: Moderate. Provides asymptotic confidence intervals for
routing weights. Useful for understanding routing uncertainty.

#### 4.5 The Optimal K: Bias-Variance
Tradeoff<!-- label: the-optimal-k-bias-variance-tradeoff -->

This is the most valuable ``low-hanging fruit'' --- a precise
characterization of the optimal number of states for SCX.

**Setup**: As K increases: - Within-state homogeneity improves:
sup\_\{x in s\} | P(Y| X=x) - P(Y| X in
s)|{} decreases -\textgreater{} mu\_s decreases -\textgreater{}
Delta increases -\textgreater{} F1 improves - But sample size per state
decreases: n\_s ≈ n/K -\textgreater{} estimation variance increases
-\textgreater{} R\_hat\_m(s) becomes noisier

**Claim**: Under regularity conditions (Lipschitz conditional
distribution P(Y| X=x) in x), the SCX F1 is optimized at:

K* ≈ (n * c / log M)\^{}\{1/3\}

for some constant c depending on the smoothness of P(Y| X=x) and
the geometry of the feature space.

**Derivation sketch**: - F1 \textgreater= 1 - (1/eta) * exp(-2M *
Delta\^{}2) - Delta = (1/2) * (1 - mu * K/(K-1)) ≈ (1/2) * (1 - mu) for
large K - mu\_s = average expert error rate in state s - Bias term:
mu\_s = mu\_global + O(1/K) (as K grows, states homogenize)
-\textgreater{} mu\_s \textless= c\_bias / K -\textgreater{} Delta
\textgreater= 1/2 - c\_bias/(2K) - Variance term: estimation error in
mu\_s scales as Var(mu\_hat) = O(1/n\_s) = O(K/n) - Worst-case Delta =
1/2 - c\_bias/(2K) - c\_var * sqrt(K/n) - Optimizing over K: d/dK
{[}c\_bias/K + c\_var * sqrt(K/n){]} = 0 -\textgreater{} -c\_bias/K\^{}2
+ c\_var / (2 * sqrt(K * n)) = 0 -\textgreater{} K* = (2 * c\_bias /
c\_var)\^{}\{2/3\} * n\^{}\{1/3\}

**Imposing the M requirement**: For the F1 guarantee to be tight,
we also need M \textgreater{} 1/(2*Delta\^{}2) *
log(2/(eta*epsilon)). With K* = O(n\^{}\{1/3\}), Delta = Omega(1),
the M requirement is asymptotically constant (does not grow with n).

**Value**: Very high. This would give practitioners a principled
way to choose K given n and M. It would be a practically useful theorem.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Hard Problems: What Requires New
Theory<!-- label: hard-problems-what-requires-new-theory -->

#### 5.1 Joint Distribution of the SCX
Score<!-- label: joint-distribution-of-the-scx-score -->

**Problem**: Characterize the joint asymptotic distribution of
(SCX\_1(s), ..., SCX\_M(s), C(x), NS(x)) as all parameters grow.

**Why it's hard**: The SCX score is a two-stage estimator: 1. First
stage: estimate the state partition (clustering) 2. Second stage:
estimate within-state reliability (averaging)

These stages share data (the same n samples are used for both), creating
complex dependence that standard asymptotics cannot handle. The state
partition is a function of the full data, making all subsequent
estimates conditionally dependent even after conditioning on the true
states.

**Known results in related areas**: - ``Post-clustering inference''
(Lockhart et al., 2014; Lee et al., 2016): selective inference after
model selection. But this is for regression coefficients after LASSO,
not for plug-in estimates after clustering. - ``Double dipping''
(Kriegeskorte et al., 2009): a known problem in neuroscience where the
same data is used for selection and estimation.

**Difficulty**: PhD thesis level. Would require novel selective
inference tools for clustering-based two-stage estimation.

#### 5.2 Optimal Scaling Rates for Triple
Asymptotics<!-- label: optimal-scaling-rates-for-triple-asymptotics -->

**Problem**: Find the optimal scaling relationship between K, M,
and n such that SCX achieves consistency (F1 -\textgreater{} 1) at the
fastest possible rate.

**The information-theoretic question**: Given: - A fixed total
sample budget T = M * n (total training samples across all experts) - A
fixed feature space dimensionality d - A data distribution P with true
state structure

What scaling K = f(T, d), M = g(T, d), n = h(T, d) minimizes the
asymptotic F1 error?

**Why it's hard**: 1. Three-way tradeoff: M controls detection
power, n controls estimation precision, K controls partitioning
granularity 2. All three consume resources: more experts means fewer
samples per expert (if total data fixed); more states means fewer
samples per state 3. The optimal scaling likely depends on the
smoothness of P(Y| X) and the clusterability of phi(X) 4. This is
a constrained optimization problem over the space of (K, M, n)
-\textgreater{} F1, where F1 is a complex function of all three

**Connection to known results**: - In high-dimensional
classification, the optimal rate involves n / (d * log p) scaling (Fan
\& Fan, 2008). This is a two-parameter problem. - In clustering, the
optimal K scales as n\^{}\{d/(d+2)\} for density-based clustering (the
``silverman'' bandwidth rule). But SCX is not density-based. - The SCX
triple is structurally more complex than either of these.

**Difficulty**: Open research problem. Would be a significant
theoretical contribution if solved.

#### 5.3 Asymptotic Distribution under Model
Misspecification<!-- label: asymptotic-distribution-under-model-misspecification -->

**Problem**: What happens to SCX when the state partition model is
wrong? Specifically, when the true distribution P(Y| X) does not
factor through a finite-state partition.

**The issue**: SCX assumes P(Y| X) ≈ P(Y| phi(X))
where phi(X) is discrete with K states. If this assumption is false
(e.g., Y depends on X in a continuous way that no finite partition can
capture), what does the SCX estimator converge to?

**What happens in the limit**: - As K -\textgreater{} oo, any
continuous function can be approximated arbitrarily well by a step
function (the partition becomes a Riemann sum approximation). So SCX
should be ``universally consistent'' as K -\textgreater{} oo with n
-\textgreater{} oo (provided K grows at the right rate). - But as K
-\textgreater{} oo with fixed n, the within-state estimates become
inconsistent (no samples per state).

**Why it's hard**: Proving universal consistency of SCX requires:
1. Showing that the excess risk due to state discretization vanishes as
K -\textgreater{} oo (approximation error) 2. Showing that within-state
estimation error vanishes as n -\textgreater{} oo (estimation error) 3.
Balancing K and n to minimize the sum

This is a **nonparametric regression with state discretization**
problem. The rate would be analogous to nonparametric rate for
partitioning estimators, but with the additional complexity of the
multi-expert aggregation.

**Difficulty**: Hard but tractable. Follows the standard
sieve/penalized M-estimation framework (Grenander, 1981; Shen \& Wong,
1994).

#### 5.4 Phase Transition in the (delta, eta, K)
Space<!-- label: phase-transition-in-the-delta-eta-k-space -->

**Problem**: Characterize the sharp threshold where SCX goes from
``works'' to ``fails'' as a function of feature-information delta, noise
rate eta, and number of states K.

**Conjecture**: There is a sharp phase transition in the (delta,
eta) plane, separated by a curve delta\_c(eta, K). Below this curve, F1
-\textgreater{} F1\_base (SCX does not help). Above it, F1
-\textgreater{} 1 (SCX works perfectly).

**Why it's hard**: 1. Phase transitions in statistical learning are
rare (e.g., the ``all-or-nothing'' phenomenon in compressed sensing).
Most learning problems have smooth transitions. 2. The SCX phase
transition (if it exists) is in the F1 score, which is a discrete metric
(it involves thresholded decisions). Continuous metrics like AUC may not
show sharp transitions. 3. Proving a phase transition requires: (a)
existence of a threshold where behavior changes, (b) showing the
transition is sharp (gap vanishes in the limit), (c) characterizing the
threshold location. 4. The triple-parameter space makes this even
harder.

**Difficulty**: Extremely hard for rigorous proof. Moderate for
heuristic or physics-style analysis (e.g., replica method or cavity
method).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Phase Transition
Conjectures<!-- label: phase-transition-conjectures -->

Despite the difficulty of rigorous proof, we can conjecture the phase
diagram based on the existing finite-sample bounds.

#### 6.1 The (K, M, n) Phase
Diagram<!-- label: the-k-m-n-phase-diagram -->

SCX ``works'' (F1 -\textgreater{} 1 asymptotically) in the following
regime:

\begin{verbatim}
Condition 1 (State recovery):  I(phi; S) / log K -> oo  (features carry
                                enough information to resolve K states)

Condition 2 (Detection power): M * Delta^2 / log M -> oo  (enough experts
                                to separate clean from noisy)

Condition 3 (Estimation):      n * P_min / (K * log M) -> oo  (enough
                                samples to estimate within-state rates)
\end{verbatim}

where P\_min = min\_s P(s) is the minimum state probability, and Delta
is the mean separation gap from Theorem 1.

If any of these conditions fail, SCX degrades in a specific way: -
Condition 1 fails (delta \textgreater\textgreater{} log K): states are
unrecoverable, SCX noise detection degenerates to loss baseline (Thm 2
regime) - Condition 2 fails (M * Delta\^{}2 small): C(x) is too noisy to
separate clean from noisy; F1 stuck below some constant \textless{} 1 -
Condition 3 fails (n * P\_min small): within-state estimates are pure
noise; state-conditioned weighting becomes worse than global weighting

#### 6.2 The Sharpness
Conjecture<!-- label: the-sharpness-conjecture -->

The most likely candidate for a sharp phase transition is in
**Condition 2** (the detection phase transition), because:

1. 
2. 
3. 
4. 

**Conjectured minimax lower bound**: There exists a data
distribution satisfying (A1)-(A6) such that, for any detection
algorithm:

E{[}F1{]} \textless= 1 - c * exp(-C * M * Delta\^{}2)

for some constants c, C \textgreater{} 0. This would show that the
exponential rate in Theorem 1 is tight (up to constants) and that M *
Delta\^{}2 is the correct phase transition parameter.

**Proof approach**: Construct a Le Cam two-point testing problem
where the null is ``all samples clean'' and the alternative is
``eta-fraction noisy.'' The minimax risk of testing these two hypotheses
is exp(-M * KL(C\_clean ||{} C\_noisy)) which scales as
exp(-M * Delta\^{}2).

#### 6.3 The Triple Phase
Transition<!-- label: the-triple-phase-transition -->

The full phase transition (K, M, n jointly) would have the form:

\begin{verbatim}
Phase 1 (SCX works):    K * log(K) / n << 1    AND  M * Delta^2 / log M >> 1
Phase 2 (State failure):  K * log K / n >> 1    (features too weak or K too
                                                  large for given n)
Phase 3 (Detection failure): M * Delta^2 / log M << 1  (too few experts)
Phase 4 (Double failure): Both Phase 2 and Phase 3 hold
\end{verbatim}

In Phase 2, SCX noise detection works no better than the loss baseline
(Thm 2 applies). In Phase 3, the detection guarantee fails but the state
discovery may still be valid (SCX can still be useful for expert
routing, just not for noise detection). In Phase 4, SCX entirely fails
for all tasks.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Would Reviewers Care?<!-- label: would-reviewers-care -->

#### 7.1 AISTATS / TMLR / NeurIPS
Norms<!-- label: aistats-tmlr-neurips-norms -->

**Current norm**: Non-asymptotic (finite-sample) bounds are
standard and preferred in top ML venues. The majority of learning theory
papers at NeurIPS, ICML, COLT, and AISTATS use PAC-style bounds.

**Why finite-sample is preferred**: 1. **Non-asymptotic
bounds are stronger**: they hold for any finite n, M, K, not just ``in
the limit.'' A reviewer who sees both a CLT (asymptotic) and a Hoeffding
bound (finite-sample) will correctly note that the Hoeffding bound is
strictly more informative for practical sample sizes. 2.
**Rate-sharpness is the focus**: what matters is how fast the error
decays in n/M/K, not the limiting distribution. The exponential rate in
M from Theorem 1 is more impactful than a CLT would be. 3.
**Asymptotic arguments can hide complexity**: Dependencies that
matter at finite sample sizes wash out in the limit. Reviewers are
suspicious of asymptotic arguments that ignore these dependencies.

#### 7.2 When Asymptotics Add
Value<!-- label: when-asymptotics-add-value -->

There are specific scenarios where asymptotic results strengthen a
paper:

1. 
2. 
3. 
4. 

#### 7.3 Recommended Position for Current
Papers<!-- label: recommended-position-for-current-papers -->

**For the first SCX paper** (primary submission): - Keep the
current finite-sample bounds (Theorems 1-3) - Add the following
asymptotic *conjectures* as open problems in the discussion section
(not as main results): - ``The optimal number of states K* is
conjectured to scale as O(n\^{}\{1/3\})'' - ``A phase transition in M *
Delta\^{}2 is conjectured'' - This shows the authors are aware of the
asymptotic questions without requiring full proofs

**For the second SCX paper** (follow-up): - One clean asymptotic
result (e.g., the optimal K scaling or a minimax lower bound) would
strengthen the theoretical contribution - By then, the framework will be
established, and the asymptotic question will be a natural next step

#### 7.4 Review Criteria<!-- label: review-criteria -->

What a reviewer would look for in asymptotic theory:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2619}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3571}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3810}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Criterion
\end{minipage} & \begin{minipage}[b]
What they want
\end{minipage} & \begin{minipage}[b]
How SCX scores
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Novelty & Is this a new result or an application of an existing
technique? & Moderate-high (unique triple structure) 

Cleanliness & Is the result clean and interpretable? & Potentially high
(phase transitions are inherently clean) 

Assumptions & Are assumptions justified? & Tricky (asymptotics require
stronger assumptions) 

Practicality & Does the result help practitioners? & High if optimal K
is derived 

Technical depth & Is the proof nontrivial? & Would be, for triple
asymptotics 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Estimated Effort<!-- label: estimated-effort -->

#### Feasibility Matrix: Effort
vs.~Impact<!-- label: feasibility-matrix-effort-vs.-impact -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1951}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1951}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1951}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1707}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2439}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Result
\end{minipage} & \begin{minipage}[b]
Effort
\end{minipage} & \begin{minipage}[b]
Impact
\end{minipage} & \begin{minipage}[b]
Ratio
\end{minipage} & \begin{minipage}[b]
Priority
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
CLT for C(x) (M -\textgreater{} oo) & 1-2 days & Low & Low & 4 

CI for SCX\_m(s) (n -\textgreater{} oo) & 2-3 days & Low-Moderate &
Medium & 3 

k-means consistency (n, K -\textgreater{} oo) & 2-4 weeks & High & High
& **1** 

Optimal K scaling & 2-4 weeks & Very high & Very high & **1** 

Delta method for routing weights & 1 week & Low-Moderate & Low & 4 

Minimax lower bound (M vs F1) & 2-4 weeks & High & High & **2** 

Joint (M, n) asymptotics & 1-3 months & Medium-High & Medium & 5 

Triple (K, M, n) asymptotics & 3-12 months & Very high & Low (cost) &
6 

Phase transition (full) & 3-12 months & Very high & Low (cost) & 6 

Post-clustering inference for SCX & 3-6 months & High & Medium & 5 

Universal consistency (nonparametric) & 2-6 months & High & Medium &
5 

\end{longtable}

#### Recommended Priority
Order<!-- label: recommended-priority-order -->

**Phase 1 (before first paper submission, 1-2 months)**: 1. Cluster
consistency: prove that k-means on phi(X) recovers the true partition as
n, K -\textgreater{} oo, under appropriate conditions (informally: ``the
SCX state discovery procedure is consistent'') 2. Optimal K scaling:
derive K* ≈ (n / log M)\^{}\{1/dimension\} from the bias-variance
tradeoff (informally: ``K should grow slowly with n'')

**Phase 2 (between submission and revision, 1-2 months)**: 3.
Minimax lower bound for F1: show that no detector can exceed F1
\textgreater{} 1 - c * exp(-C * M * Delta\^{}2), proving Theorem 1
optimal up to constants (informally: ``SCX's detection rate is
fundamentally optimal'')

**Phase 3 (for follow-up paper, 3-6 months)**: 4. One clean
triple-asymptotic result for a restricted setting (e.g., binary states,
symmetric experts, Gaussian features)

#### Total Time<!-- label: total-time -->

- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Recommended First Step<!-- label: recommended-first-step -->

#### Choose One Regime: Cluster Consistency for State
Discovery<!-- label: choose-one-regime-cluster-consistency-for-state-discovery -->

The single most valuable and tractable asymptotic result is:

**``Consistency of k-means State Discovery in SCX''**

**Statement**: For the SCX state discovery procedure (k-means
clustering on feature vectors phi(x\_i)), as the number of training
samples n -\textgreater{} oo and the number of states K grows with n:

If K = o(n\^{}\{1/3\}) and the features are regular enough (the ``true''
partition has well-separated components in phi-space), then:

lim\_\{n -\textgreater{} oo\} P(estimated partition != true partition) =
0

Furthermore, if K scales as K* ~{} C * n\^{}\{1/3\} (for a
known constant C depending on cluster geometry), the bias-variance
tradeoff is optimized.

**Why this is the right first step**: 1. It addresses a real gap:
Thm 2 only gives negative results for state discovery. A positive
consistency result is long overdue. 2. It connects to a mature
literature (Pollard, 1981; Von Luxburg, 2007; Rakhlin \& Caponnetto,
2007) so the technical path is clear. 3. It produces a practically
useful output (guidance on choosing K). 4. It can be written as a
self-contained result that doesn't require simultaneous asymptotic
analysis of M and n.

#### What the Proof Would
Need<!-- label: what-the-proof-would-need -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 

\item
  **Standard references**:

  
- 
- 
- 

\end{enumerate}

#### Deliverable<!-- label: deliverable -->

A 2-3 page proof (or a section in the existing Thm 2 document) showing:

1. 
2. 
3. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. References<!-- label: references -->

#### Existing SCX Theory<!-- label: existing-scx-theory -->

- 
- 
- 

#### Asymptotic Clustering
Theory<!-- label: asymptotic-clustering-theory -->

- 
- 
- 
- 
- 

#### High-Dimensional and Double
Asymptotics<!-- label: high-dimensional-and-double-asymptotics -->

- 
- 
- 

#### Selective Inference /
Post-Clustering<!-- label: selective-inference-post-clustering -->

- 
- 
- 

#### Nonparametric Sieve
Estimation<!-- label: nonparametric-sieve-estimation -->

- 
- 
- 

#### Phase Transitions in
Learning<!-- label: phase-transitions-in-learning -->

- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Appendix: Quick Reference --- Parameter Roles in
SCX<!-- label: appendix-quick-reference-parameter-roles-in-scx -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1486}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.0811}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2297}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2838}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2568}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Parameter
\end{minipage} & \begin{minipage}[b]
Role
\end{minipage} & \begin{minipage}[b]
Grows -\textgreater{} Effect
\end{minipage} & \begin{minipage}[b]
Finite-sample result
\end{minipage} & \begin{minipage}[b]
Asymptotic target
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
K & Number of states & Finer partition, fewer samples per state & Thm 2:
Fano bound on recovery & Optimal K* scaling 

M & Number of experts & More reliable consistency score & Thm 1: F1
exp(-M * Delta\^{}2) & Minimax lower bound 

n & Samples per state & More precise within-state estimates & PAC:
O(1/sqrt(n\_s)) & CLT for SCX\_m(s) 

eta & Noise rate & More detectable noise & Appears in F1 bound & Phase
boundary 

delta & Feature info & Better state recovery & Thm 2: AUC \textless=
baseline + O(sqrt(delta)) & Phase boundary 

\end{longtable}

The key mathematical quantities and their asymptotic behavior:

\begin{verbatim}
SCX_m(s) = P(ell(f_m(x), y) < tau | x in s)
  As n_s -> oo: sqrt(n_s) * (SCX_hat - SCX) ~ N(0, SCX * (1-SCX))

C(x) = (1/M) * sum e_m(x)
  As M -> oo: C(x) -> mu(x) a.s.;  sqrt(M) * (C - mu) ~ N(0, sigma^2)

F1 >= 1 - (1/eta) * exp(-2M * Delta^2)
  As M * Delta^2 -> oo: F1 -> 1 at exponential rate

K* ≈ (n / log M)^{1/3}  [conjectured optimal scaling]
\end{verbatim}