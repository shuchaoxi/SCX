# Connections Between SCX Self-Evolution and Known
Theories

**Author:** SCX

> **Part of the SCX Self-Evolution Theory Series** **Status**:
> Formal comparison |{} **Audit**: Pre-review
> **Prerequisites**: THEOREMS\_UNIFIED.md, self-evolution definitions
> (Files 1-7)

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. AlphaZero Self-Play<!-- label: alphazero-self-play -->

#### 1.1 Overview<!-- label: overview -->

AlphaZero (Silver et al., 2017, 2018) learns to play board games through
self-play reinforcement learning. The agent plays games against itself,
using Monte Carlo Tree Search (MCTS) to generate training data, which is
then used to update a deep neural network. The network has two heads: a
policy head \(p(s)\) predicting move probabilities and a value head
\(V(s)\) predicting the expected outcome from state \(s\).

The self-play loop is:
\[\pi_{\theta_{old}} \xrightarrow{MCTS} \{self-play games\} \xrightarrow{training} \pi_\theta \xrightarrow{evaluation} \pi_{\theta_{new}}\]

#### 1.2 Formal Mapping<!-- label: formal-mapping -->

The SCX self-evolution loop maps to AlphaZero as follows:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3279}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4918}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1803}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
AlphaZero Component
\end{minipage} & \begin{minipage}[b]
SCX Self-Evolution Component
\end{minipage} & \begin{minipage}[b]
Rationale
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Policy network \(\pi_\theta\) & Gatekeeper \(S_t\) & Both select
actions: \(\pi_\theta\) selects moves, \(S_t\) selects data for
validation 

Self-play games & NEP student \(f_{\theta_t}\) predictions & Both
generate training targets through interaction with a fixed
environment 

MCTS search & SCX state-conditioned aggregation
\(\hat{R}_m(s), SCX_m(s)\) & Both refine raw evaluations through
structured computation 

Value network \(V(s)\) & SCX state value function
\(V(s) = \mathbb{E}[improvement \mid s]\) & Both estimate the
long-term value of states/decisions 

Replay buffer & Memory bank \(M_t\) & Both store experience for future
training 

Evaluation against previous version & Lyapunov descent check
\(\Phi(S_t) < \Phi(S_{t-1})\) & Both compare new policy against old to
ensure monotonic improvement 

Opponent (fixed rules) & True physical law \(f^*\) + current data
\(\mathcal{D}_t\) & Both provide the fixed, non-learnable environment 

Training loss
\(L(\theta) = L_{policy} + L_{value} + L_{reg}\) &
Lyapunov function \(\Phi(S_t, M_t, f_{\theta_t})\) & Both provide the
scalar signal for optimization 

\end{longtable}

#### 1.3 Key Similarities<!-- label: key-similarities -->

1. 
2. 
3. 
4. 

#### 1.4 Key Differences<!-- label: key-differences -->

1. 
2. 
3. 
4. 
5. 

#### 1.5 Convergence Comparison<!-- label: convergence-comparison -->

**AlphaZero (policy iteration)**:
\[Performance(\pi_{t+1}) \geq Performance(\pi_t)\]
Convergence to optimal policy \(\pi^*\) under sufficient capacity and
exploration (proven for tabular case; empirically observed for neural
networks).

**SCX (Lyapunov descent)**:
\[\Phi(S_{t+1}, M_{t+1}, f_{\theta_{t+1}}) \leq \Phi(S_t, M_t, f_{\theta_t})\]
Convergence to fixed point \(q_{T^*}\) in finite time (Theorem SE-2).
The fixed point is self-consistent but not necessarily optimal in a
global sense.

**Comparison**: Both guarantee monotonic improvement. AlphaZero's
guarantee is stronger (convergence to optimal play under certain
conditions) but relies on a fully known environment. SCX's guarantee is
weaker (convergence to a self-consistent fixed point) but operates in an
environment with unknown ground truth.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Bayesian Optimization<!-- label: bayesian-optimization -->

#### 2.1 Overview<!-- label: overview-1 -->

Bayesian optimization (BO) (Mockus, 1975; Jones et al., 1998) optimizes
a black-box function \(f: \mathcal{X} \to \mathbb{R}\) by building a
probabilistic surrogate model \(g\) (typically a Gaussian process) and
using an acquisition function \(\alpha\) to select the next evaluation
point:

\[x_{t+1} = \arg\max_{x \in \mathcal{X}} \alpha(x \mid g_{1:t})\]

where \(\alpha\) balances exploration (points with high uncertainty) and
exploitation (points with high predicted value).

#### 2.2 Formal Mapping<!-- label: formal-mapping-1 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2407}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5556}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2037}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
BO Component
\end{minipage} & \begin{minipage}[b]
SCX Self-Evolution Component
\end{minipage} & \begin{minipage}[b]
Rationale
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Black-box function \(f\) & True physical law \(f^*\) & Both are unknown,
expensive to evaluate 

Surrogate model \(g\) & NEP student \(f_\theta\) & Both approximate the
unknown ground truth 

Acquisition function \(\alpha\) & Gatekeeper \(S_t\) & Both guide the
selection of the next evaluation point 

Evaluation budget & NEP validation budget & Both have limited
evaluations (BO: function evaluations; SCX: DFT/experiment budget) 

Posterior \(p(f \mid \mathcal{D}_{1:t})\) & Memory bank \(M_t\) +
student \(f_{\theta_t}\) & Both represent accumulated knowledge about
the unknown function 

Regret \(r_t = f(x^*) - f(x_t)\) & Lyapunov gap
\(\Phi(q_t) - \Phi_{opt}\) & Both measure suboptimality of the
current state 

\end{longtable}

#### 2.3 Formal Comparison: Acquisition
Functions<!-- label: formal-comparison-acquisition-functions -->

**BO's Expected Improvement (EI)**:
\[\alpha_{EI}(x) = \mathbb{E}\left[\max(0, f(x) - f_{best}) \mid \mathcal{D}_{1:t}\right]\]

**SCX's State Data Value**:
\[V(s) = \underbrace{\hat{R}(s)}_{expert disagreement} \cdot \underbrace{\rho(s)}_{state proportion} \cdot \underbrace{(1 - C(s))}_{uncertainty}\]

where \(C(s) = \frac{1}{M}\sum_m \mathbf{1}\{\ell(f_m(x), y) > \tau\}\)
is the consensus score (Theorem 1).

Both EI and SCX's \(V(s)\) balance: - **Exploitation** (high
predicted improvement / high expert disagreement \(\hat{R}(s)\)) -
**Exploration** (high posterior uncertainty / low consensus
\(C(s)\))

**Key difference**: EI operates on a continuous input space and is
formalized as an expectation under a Gaussian process posterior. SCX's
\(V(s)\) operates on a discrete state space (partition of
\(\mathcal{X}\) into \(K_S\) states) and uses frequentist estimates of
within-state disagreement.

#### 2.4 Convergence Rates<!-- label: convergence-rates -->

**BO convergence** (Srinivas et al., 2010): For a GP with kernel
\(k\), the cumulative regret is bounded by:

\[R_T = \sum_{t=1}^T r_t \leq \sqrt{T \cdot \gamma_T \cdot C}\]

where \(\gamma_T\) is the maximum information gain after \(T\)
evaluations. For the squared exponential kernel,
\(\gamma_T = O((\log T)^{d+1})\), giving
\(R_T = O(\sqrt{T (\log T)^{d+1}})\).

**SCX convergence** (Theorem SE-1, SE-2): For the Lyapunov function
\(\Phi\), the gap decays as:

\[\Phi(q_t) - \Phi_{opt} \leq \Phi(q_0) \cdot \exp(-\lambda t)\]

under the contraction condition, or in worst case:

\[T^* \leq \frac{\Phi_0}{\varepsilon_{mach}}\]

**Comparison**: BO provides cumulative regret bounds that depend on
the information-theoretic complexity of the function class. SCX provides
a finite-time termination bound that depends on the Lyapunov descent
rate and machine precision. BO's bounds are more informative for
sub-exponential convergence; SCX's guarantee is stronger (exact
termination).

#### 2.5 Key Similarities<!-- label: key-similarities-1 -->

1. 
2. 
3. 
4. 

#### 2.6 Key Differences<!-- label: key-differences-1 -->

1. 
2. 
3. 
4. 
5. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Active Learning<!-- label: active-learning -->

#### 3.1 Overview<!-- label: overview-2 -->

Active learning (AL) (Settles, 2009) aims to reduce labeling effort by
selectively querying labels for the most informative unlabeled examples.
Given a labeled pool \(\mathcal{L}\), an unlabeled pool \(\mathcal{U}\),
and a model \(h\), the query strategy \(Q(x \mid h)\) selects the next
sample(s) to label.

#### 3.2 Formal Mapping<!-- label: formal-mapping-2 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2407}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5556}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2037}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
AL Component
\end{minipage} & \begin{minipage}[b]
SCX Self-Evolution Component
\end{minipage} & \begin{minipage}[b]
Rationale
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Model \(h\) & NEP student \(f_\theta\) & Both are the predictive model
being improved 

Oracle \(O\) (labeler) & NEP simulator + DFT validation & Both provide
ground-truth labels 

Query strategy \(Q(x \mid h)\) & Gatekeeper \(S_t\) + state-value
scoring & Both select which samples to label/validate 

Labeled pool \(\mathcal{L}\) & Memory bank \(M_t\) & Both store
labeled/validated data 

Unlabeled pool \(\mathcal{U}\) & Candidate pool \(\mathcal{C}_t\) & Both
contain unlabeled samples 

Labeling budget & NEP validation budget & Both have finite labeling
capacity 

\end{longtable}

#### 3.3 Comparison of Query
Strategies<!-- label: comparison-of-query-strategies -->

**Standard AL strategies**:

1. 
2. 
3. 

**SCX's approach (state-certified active learning)**:

\[a^*(s) = \arg\max_{a \in \mathcal{A}} U(a, s)\]

where
\(\mathcal{A} = \{validate, discard, defer, ...\}\)
and \(U(a, s)\) is the expected utility of action \(a\) for state \(s\).
The utility is computed from state-level statistics:

\[U(validate, s) = \underbrace{\hat{R}(s)}_{expert disagreement} \cdot \underbrace{(1 - SCX(s))}_{reliability gap} \cdot \underbrace{\rho(s)}_{state size}\]

#### 3.4 Comparison of Query
Strategies<!-- label: comparison-of-query-strategies-1 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1852}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2778}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2407}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2963}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Strategy
\end{minipage} & \begin{minipage}[b]
AL Counterpart
\end{minipage} & \begin{minipage}[b]
SCX Version
\end{minipage} & \begin{minipage}[b]
Key Difference
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Uncertainty sampling & \(1 - \max_y P(y \mid x)\) & \(1 - C(s)\) where
\(C(s)\) is state consensus & SCX uses multi-expert consensus instead of
single-model uncertainty 

Query-by-committee & Vote entropy among ensemble & SCX reliability gap
\(SCX(s)\) & SCX uses state-conditioned expert reliability, not
raw vote entropy 

Expected model change &
\(\|\nabla L(\theta \cup (x,y)) - \nabla L(\theta)\|\) &
\(V(s) = \hat{R}(s) \cdot \rho(s) \cdot (1 - C(s))\) & SCX's value
function operates at state level, not point level 

Density-weighted & \(\frac{1}{n}\sum_{i=1}^n sim(x, x_i)\) &
\(\rho(s)\) (state proportion) & Both weight by representativeness 

Diversity sampling & Coreset selection & Discard redundant states via
SCX-Compress & Both aim for coverage 

\end{longtable}

#### 3.5 SCX's State-Certified Active
Learning<!-- label: scxs-state-certified-active-learning -->

The key innovation of SCX's approach is the **state-level
certification**. Unlike point-wise active learning, which treats each
sample independently:

1. 
2. 
3. 

#### 3.6 Sample Complexity
Comparison<!-- label: sample-complexity-comparison -->

**Standard AL sample complexity** (Balcan et al., 2009): Under the
disagreement coefficient \(\theta\), active learning achieves label
complexity:

\[N_{AL}(\varepsilon) = O\left(\theta \cdot d \cdot \log\frac{1}\right)\]

where \(d\) is the VC dimension of the hypothesis class.

**SCX sample complexity** (derived from Theorem 1 and Proposition
2): The number of validation labels needed per state \(s\) to achieve
reliability \(SCX_m(s) > 1 - \delta\) is:

\[n_{SCX}(s, \delta) = O\left(\frac{1}{\Delta_s^2} \log\frac{1}\right)\]

where \(\Delta_s\) is the state-level separation gap (Theorem 1).
Aggregating over \(K_S\) states:

\[N_{SCX}(\varepsilon) = O\left(K_S \cdot \frac{1}{\Delta_^2} \log\frac{1}\right)\]

where \(\Delta_ = \min_s \Delta_s\).

**Comparison**: Standard AL avoids the \(K_S\) multiplicative
factor but requires the disagreement coefficient \(\theta\) to be small.
SCX's factor of \(K_S\) is the cost of operating without a single
discriminative model --- SCX uses multiple experts and must characterize
each state independently.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Solomonoff Induction<!-- label: solomonoff-induction -->

#### 4.1 Overview<!-- label: overview-3 -->

Solomonoff induction (Solomonoff, 1964) is a theoretical framework for
inductive inference. Given a sequence of observations, the posterior
probability of a continuation is:

\[P(x_{n+1} \mid x_1, ..., x_n) = \frac{\sum_{p: p(x_1,...,x_n) = x_1,...,x_n} 2^{-|p|} \cdot P(x_{n+1} \mid p)}{\sum_{p: p(x_1,...,x_n) = x_1,...,x_n} 2^{-|p|}}\]

where \(p\) ranges over all programs for a universal Turing machine,
\(|p|\) is program length, and \(P(x_{n+1} \mid p)\) is the continuation
probability under program \(p\). The universal prior
\(M(x) = \sum_p 2^{-|p|} \cdot \mathbf{1}\{p(\varepsilon) = x\}\)
assigns higher probability to strings generated by shorter programs
(Occam's razor).

#### 4.2 Formal Analogy<!-- label: formal-analogy -->

**Claim (SE-A1)**: The limiting SCX gatekeeper
\(S_\infty(x) = \lim_{t\to\infty} S_t(x)\) approximates a Solomonoff
predictor for the question ``Is this label correct?''

The analogy proceeds as follows:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2683}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4634}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2683}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Solomonoff
\end{minipage} & \begin{minipage}[b]
SCX Self-Evolution
\end{minipage} & \begin{minipage}[b]
Rationale
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Universal prior
\(M(x) = \sum_p 2^{-|p|}\mathbf{1}\{p(\varepsilon) = x\}\) & State
partition \(\mathcal{S}\) with prior \(\rho_s = \mathbb{P}(X \in s)\) &
Both define prior beliefs over hypotheses 

Programs \(p\) & Expert models \(\{f_m\}\) & Both are candidate
explanations of observed data 

Program length \(|p|\) (Occam penalty) & Expert complexity (implicit in
training data requirement) & Both penalize complexity 

Likelihood \(P(data \mid p)\) & Consensus score
\(C(x) = \frac{1}{M}\sum_m \mathbf{1}\{\ell(f_m(x), y) > \tau\}\) & Both
measure how well the hypothesis explains the observation 

Posterior \(P(x_{n+1} \mid data)\) & Gatekeeper score \(S_t(x)\)
& Both represent the current belief about an unseen property 

Accumulated evidence & Memory bank \(M_t\) & Both store the history of
observations 

Convergence as \(n \to \infty\) & Convergence as \(t \to \infty\)
(Theorem SE-2) & Both converge to fixed points given sufficient
evidence 

\end{longtable}

#### 4.3 Formal Correspondence<!-- label: formal-correspondence -->

The Solomonoff posterior for the proposition ``\(x\) is clean'' (i.e.,
\(y = f^*(x)\)) is:

\[P(clean \mid \mathcal{D}) = \frac{\sum_p 2^{-|p|} \cdot P(\mathcal{D} \mid p) \cdot \mathbf{1}\{p  predicts clean at  x\}}{\sum_p 2^{-|p|} \cdot P(\mathcal{D} \mid p)}\]

The SCX gatekeeper's score for \(x\) at state \(s(x)\) is:

\[S_t(x) = \frac{1}{M}\sum_{m=1}^M \underbrace{SCX_m(s(x))}_{expert reliability in state  s} \cdot \underbrace{\mathbf{1}\{\ell(f_m(x), y) < \tau\}}_{expert  m  agrees with label}\]

The correspondence is: - **Hypothesis class**: Solomonoff sums over
all computable functions; SCX sums over the finite set of \(M\) experts.
- **Prior**: Solomonoff uses the universal prior \(2^{-|p|}\); SCX
uses state proportions \(\rho_s\) (experts are implicitly weighted by
their state-conditioned reliability). - **Convergence**: Solomonoff
converges to the truth with probability 1 for any computable environment
(Hutter, 2005). SCX converges to a fixed point (Theorem SE-2) but may
not converge to the truth (Theorem 3).

#### 4.4 Key Limitations of the
Analogy<!-- label: key-limitations-of-the-analogy -->

1. 
2. 
3. 
4. 

#### 4.5 Occam's Razor in SCX<!-- label: occams-razor-in-scx -->

While SCX does not explicitly implement Occam's razor, simpler state
structures are implicitly preferred through:

- 
- 
- 

This implicit Occam bias is weaker than Solomonoff's explicit prior
\(2^{-|p|}\) but serves a similar function: it prevents the gatekeeper
from overfitting to noise in the expert consensus signals.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Comprehensive Comparison
Table<!-- label: comprehensive-comparison-table -->

#### 5.1 Unified Comparison<!-- label: unified-comparison -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1100}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1100}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2100}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1700}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2100}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1900}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Dimension
\end{minipage} & \begin{minipage}[b]
AlphaZero
\end{minipage} & \begin{minipage}[b]
Bayesian Optimization
\end{minipage} & \begin{minipage}[b]
Active Learning
\end{minipage} & \begin{minipage}[b]
Solomonoff Induction
\end{minipage} & \begin{minipage}[b]
SCX Self-Evolution
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Core Mechanism** & Policy iteration + MCTS + neural network &
Surrogate model + acquisition function & Query strategy + oracle
labeling & Universal prior + Bayesian update & Lyapunov descent + memory
bank + gatekeeper 

**Exploration Strategy** & Dirichlet noise + MCTS visit counts &
Posterior variance (GP) & Uncertainty/disagreement/diversity sampling &
Universal prior over all programs & State value function \(V(s)\) +
consensus uncertainty 

**Convergence Guarantee** & Monotonic policy improvement; optimal
for tabular case & \(\sqrt{T \cdot \gamma_T}\) cumulative regret; no
exact termination & \(\tilde{O}(\theta \cdot d)\) label complexity;
VC-based & Convergence to truth with prob 1 for computable environments
& Finite-time fixed point (Theorem SE-2); Lyapunov descent (Theorem
SE-1) 

**Regret Bound** & \(V^* - V^{\pi_t} \leq unknown\)
(empirically fast) & \(R_T = O(\sqrt{T \cdot \gamma_T})\) (GP) & Label
complexity \(O(\theta \cdot d \cdot \log(1/\varepsilon))\) & Optimal but
incomputable &
\(\Phi(q_t) - \Phi_{opt} \leq \Phi(q_0) e^{-\lambda t}\) (under
contraction) 

**Computational Cost** & \(O(N_{sim} \cdot d_{net})\)
per iteration & \(O(T \cdot (n^3 + dn))\) for GP & \(O(n \cdot d)\) per
query & Incomputable & \(O(M \cdot K_S \cdot N + K_S \cdot d_\phi)\) per
iteration 

**Key Difference from SCX** & Synthetic data; known environment;
stronger convergence & Static black-box; point-wise; single objective &
Point-wise queries; single model; no state aggregation & Universal class
but incomputable; complete convergence & Real data; unknown \(f^*\);
state-level; multi-objective; finite compute 

**Environment** & Fully known (game rules) & Partially known (GP
prior) & Partially known (labeled pool) & Unknown but computable &
Unknown physical law (uncomputable in general) 

\end{longtable}

#### 5.2 Detailed Metric
Comparison<!-- label: detailed-metric-comparison -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2051}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2821}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1282}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1282}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1282}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1282}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Metric
\end{minipage} & \begin{minipage}[b]
AlphaZero
\end{minipage} & \begin{minipage}[b]
BO
\end{minipage} & \begin{minipage}[b]
AL
\end{minipage} & \begin{minipage}[b]
SI
\end{minipage} & \begin{minipage}[b]
SCX
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Per-iteration data cost** & Free (synthetic) & \(O(1)\) function
evaluation & \(O(b)\) labels per batch & None & \(O(b)\) NEP
validations 

**Scalability (\(X\) dimension)** & High (neural nets) & Low (GP:
\(O(n^3)\)) & Medium & None (incomputable) & Medium (k-means:
\(O(N d_\phi K_S)\)) 

**Theoretical maturity** & Empirical (except tabular) & Strong (GP
regret) & Strong (disagreement coeff.) & Complete (incomputable) &
Partial (this work) 

**Applicability to physical sciences** & Not designed (game domain)
& High (materials, chemistry) & Medium (active labeling) & None
(incomputable) & High (designed for NEP) 

**Handles label noise** & No (synthetic data) & No (GP assumes
clean) & Partially (oracle assumed clean) & Yes (Bayesian) & Yes
(primary design goal) 

**Uncertainty quantification** & Value head variance & GP posterior
& Model confidence & Full posterior & Multi-expert consensus 

**Memory of past data** & Replay buffer (bounded) & All past
evaluations (\(O(n)\)) & Labeled pool & All past data & Memory bank
\(M_t\) 

**Formal convergence proof** & Partial (tabular) & Yes (GP regret)
& Yes (label complexity) & Yes (incomputable) & Yes (SE-1, SE-2) 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Synthesis: What Is and Is Not
New<!-- label: synthesis-what-is-and-is-not-new -->

#### 6.1 Aspects That Are Novel<!-- label: aspects-that-are-novel -->

1. 
2. 
3. 
4. 

#### 6.2 Aspects That Are Not
Novel<!-- label: aspects-that-are-not-novel -->

1. 
2. 
3. 
4. 

#### 6.3 The SCX Synthesis<!-- label: the-scx-synthesis -->

The SCX self-evolution framework occupies a **unique position** in
the theory landscape:

- 
- 
- 
- 

The most accurate description is: **SCX is a restricted-domain,
computationally tractable approximation of Solomonoff induction,
operationalized through BO-inspired acquisition on a state space
discovered by AL-like clustering, stabilized by AlphaZero-inspired
monotonic improvement.**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### References<!-- label: references -->

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

*End of 08\_theory\_connections.md*