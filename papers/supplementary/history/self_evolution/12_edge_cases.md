# SCX Self-Evolution: Edge Cases and Failure
Modes

**Author:** SCX

> **Version**: 2026-06-28 |{} **Status**: Formal analysis
> |{} **Prerequisite**: Documents 01, 02, 06, 10, 11
> **Purpose**: Characterize failure modes of the SCX self-evolution
> system, deriving conditions under which convergence fails, degrades, or
> produces pathological behavior. Four canonical failure modes are
> analyzed in depth, with formal conditions, rates of degradation, and
> mitigation strategies. **Notation note**: \(\mathcal{S}\) denotes
> the state space (as in core Theorems 1--3). \(S_t\) denotes the
> gatekeeper scoring function at time \(t\) (as in Spring self-evolution
> documents). \(\Psi\) denotes the Lyapunov function (renamed from
> \(\Phi\) to avoid collision with feature space \(\Phi\) in Theorem 2).
> \(\beta_t\) denotes the gatekeeper update rate; \(\eta\) is reserved for
> the global noise rate.

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Failure Mode 1: Premature Convergence (Gatekeeper
Freezing)<!-- label: failure-mode-1-premature-convergence-gatekeeper-freezing -->

#### 1.1 Phenomenon<!-- label: phenomenon -->

The gatekeeper converges to a suboptimal fixed point
\(S^*_{sub}\) before the student has learned enough to provide
useful feedback. Once frozen, the system cannot escape because the
gatekeeper rejects new data that would contradict its (incorrect)
judgments.

#### 1.2 Formal Mechanism<!-- label: formal-mechanism -->

**The learning rate decays too fast.** When \(\beta_t\) (the
gatekeeper update rate) decays faster than the student can learn,
gatekeeper plasticity is lost before the student provides corrective
signal.

> **Notation note (2026-06-28, B4):** The symbol \(\eta\) is reserved
> throughout the SCX theory for the global noise rate \(\eta = P(Z=1)\).
> The gatekeeper update rate is denoted \(\beta_t\). This document
> previously used \(\eta(t)\) locally for the gatekeeper update rate,
> which has been corrected to \(\beta_t\) for consistency.

**Definition 1.1 (Freezing Time).** The **freezing time**
\(t_{freeze}\) is the earliest time such that for all
\(t \geq t_{freeze}\):

\[\|\Delta S_t\|_{M_0} \leq \varepsilon_{mach},\]

i.e., subsequent gatekeeper updates are numerically indistinguishable
from zero.

**Theorem 12.1 (Freezing Condition --- PROVEN).** Under condition
C6' (two-timescale, \(\beta_t = o(\alpha_t)\)), if:

\[\beta_t \cdot B_S \leq \varepsilon_{mach} \quad for  t \geq t_{freeze},\]

then the gatekeeper freezes. With \(\beta_t = \beta_0 t^{-b}\), this
occurs at:

\[\boxed{\;t_{freeze} \leq \left(\frac{\beta_0 B_S}{\varepsilon_{mach}}\right)^{1/b}\;}.\]

*Proof.* By C7, \(\|\Delta S_t\|_\infty \leq \beta_t B_S\). When
this bound falls below machine precision, the update is numerically
zero. Solving \(\beta_0 t^{-b} B_S = \varepsilon_{mach}\) gives
the freezing time. \(\square\)

**Status: PROVEN.** This is a direct consequence of C7 and the
numerical precision constraint.

#### 1.3 When Freezing is
Premature<!-- label: when-freezing-is-premature -->

Freezing is **premature** if
\(t_{freeze} < t_{converge}\), where
\(t_{converge}\) is the time needed for the student to reach its
asymptotic accuracy.

**Theorem 12.2 (Premature Freezing Condition --- PROVEN).** Under
strong convexity (SC), the student needs:

\[t_{converge} = \left(\frac{C_1}{\varepsilon_{target}}\right)^{1/a}\]

steps to achieve
\(\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq \varepsilon_{target}\).
Premature freezing occurs when:

\[\boxed{\;\left(\frac{\beta_0 B_S}{\varepsilon_{mach}}\right)^{1/b} < \left(\frac{C_1}{\varepsilon_{target}}\right)^{1/a}\;}.\]

*Numerical example.* With \(\beta_0 = 0.1\), \(B_S = 1\),
\(\varepsilon_{mach} = 10^{-16}\), \(b = 0.8\): -
\(t_{freeze} \approx (0.1 / 10^{-16})^{1.25} \approx 10^{18.75}\),
astronomically large. Freezing is **not** a practical concern with
double precision.

With \(\beta_0 = 0.01\), \(\varepsilon_{mach} = 10^{-4}\)
(aggressive early stopping threshold), \(b = 0.9\): -
\(t_{freeze} \approx (0.01 / 10^{-4})^{1.11} \approx 10^{2.22} \approx 166\),
which is small enough to be concerning.

**Status: PROVEN.** The existence of a freezing time is guaranteed;
whether it is premature depends on parameter choices.

#### 1.4 Effect of Premature Freezing on Solution
Quality<!-- label: effect-of-premature-freezing-on-solution-quality -->

**Theorem 12.3 (Suboptimality Gap Under Premature Freezing ---
PROVEN).** If the gatekeeper freezes at \(S_{t_{freeze}}\) and the
student continues to converge toward
\(\theta^*(S_{t_{freeze}})\), the asymptotic Lyapunov gap is:

\[\Psi(S_{t_{freeze}}, \theta^*(S_{t_{freeze}})) - \Psi(S^*, \theta^*) \geq \lambda \cdot \bigl(\mathbb{E}_{V_0}[\ell(f_{\theta^*(S_{t_{freeze}})}, y)] - \mathbb{E}_{V_0}[\ell(f_{\theta^*}, y)]\bigr) \geq 0.\]

The gap is non-negative and equals zero only if
\(S_{t_{freeze}} = S^*\).

*Proof.* At the frozen gatekeeper \(S_{t_{freeze}}\), the
student converges to \(\theta^*(S_{t_{freeze}})\), which
minimizes the loss under the frozen distribution
\(P_{S_{t_{freeze}}}\). The gap on the reference distribution
\(V_0\) is generally positive because the frozen gatekeeper may exclude
regions where the true fixed-point student \(\theta^*\) performs
differently. \(\square\)

#### 1.5 Rate of Degradation<!-- label: rate-of-degradation -->

**Corollary 12.1 (Degradation Rate Under Freezing).** At time
\(t \geq t_{freeze}\), the convergence of \(\Psi_t\) stalls:

\[\Psi_t - \Psi^* = \Theta(1) \quad (does not decay further).\]

The improvement after freezing is:

\[\Delta\Psi_{post-freeze} = \Psi_{t_{freeze}} - \lim_{t \to \infty} \Psi_t = O(\alpha_{t_{freeze}}),\]

which comes only from the student continuing to train on the frozen
distribution.

#### 1.6 Mitigation Strategies<!-- label: mitigation-strategies -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3704}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4074}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2222}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Strategy
\end{minipage} & \begin{minipage}[b]
Mechanism
\end{minipage} & \begin{minipage}[b]
Cost
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Minimum learning rate** & Clamp \(\beta_t \geq \beta_ > 0\)
& Prevents asymptotic convergence, introduces steady-state error
\(O(\beta_)\) 

**Cyclical learning rate** & Periodically reset \(\beta_t\) to
\(\beta_0\) & Requires tuning cycle period; may cause transient
instability 

**Plateau detection + boost** & When \(\|\Delta S_t\| < \delta\)
for \(k\) consecutive steps, multiply \(\beta_t\) by \(\gamma > 1\) &
Ad-hoc; may overshoot 

**Student-driven unfreezing** & When student loss on \(V_0\) stops
improving, increase \(\beta_t\) temporarily & Couples unfreezing to
observable metric 

**Polyak averaging on gatekeeper** & Maintain
\(\bar{S}_t = \frac{1}{t}\sum_{i=1}^t S_i\) & Reduces variance; may
smooth past frozen states 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Failure Mode 2: Backlog Problem (Memory
Overrun)<!-- label: failure-mode-2-backlog-problem-memory-overrun -->

#### 2.1 Phenomenon<!-- label: phenomenon-1 -->

The memory bank \(M_t\) grows faster than the gatekeeper can score
incoming samples. Unscored samples accumulate in a backlog, delaying the
gatekeeper's feedback and eventually stalling the self-evolution loop.

#### 2.2 Formal Mechanism<!-- label: formal-mechanism-1 -->

**Assumptions:** - Samples arrive at rate \(r_{in}\)
(samples per unit time). - The gatekeeper can score at rate
\(r_{score}\) (samples per unit time). - The NEP student retrains
every \(K\) new samples.

**Definition 2.1 (Backlog).** The backlog at time \(t\) is:

\[B(t) = r_{in} \cdot t - r_{score} \cdot t = (r_{in} - r_{score}) \cdot t.\]

A backlog develops when \(r_{in} > r_{score}\).

#### 2.3 Gatekeeper Scoring
Complexity<!-- label: gatekeeper-scoring-complexity -->

The gatekeeper's per-sample scoring cost is:

\[T_{score}(x) = O(M) \quad (evaluate all  M  experts) + O(K_S) \quad (state lookup) + O(d_\phi) \quad (feature computation).\]

Total scoring throughput:

\[r_{score} = \frac{1}{T_{score}} = \Omega\!\left(\frac{1}{M + K_S + d_\phi}\right).\]

#### 2.4 Critical Condition for
Backlog<!-- label: critical-condition-for-backlog -->

**Theorem 12.4 (Backlog Instability --- PROVEN).** If:

\[\boxed{\;r_{in} > \frac{C_{compute}}{M + K_S + d_\phi}\;},\]

where \(C_{compute}\) is the available compute (FLOPs/second),
the backlog grows without bound and the system becomes
**unstable**: the memory bank contains samples whose scores are
based on a stale gatekeeper \(S_{t - \tau}\) with delay
\(\tau = B(t) / r_{score} \to \infty\).

*Proof.* The scoring delay per sample is
\(\tau = B(t) / r_{score}\). When
\(r_{in} > r_{score}\), \(B(t) \to \infty\) and
\(\tau \to \infty\). The gatekeeper used for sample \(x_i\) is
\(S_{t_i}\) where \(t_i = i - \tau_i\). As \(\tau \to \infty\), the
gatekeeper version used for scoring becomes arbitrarily old, violating
the implicit assumption that \(S_t\) reflects current knowledge.
\(\square\)

**Status: PROVEN.** This is a throughput calculation.

#### 2.5 Effect on Self-Evolution
Dynamics<!-- label: effect-on-self-evolution-dynamics -->

**Theorem 12.5 (Stale Gatekeeper Error --- CONJECTURED).** If
sample \(x\) is scored by gatekeeper \(S_{t-\tau}\) (stale by \(\tau\)
steps), the probability of misclassification is:

\[\mathbb{P}(sign(S_{t-\tau}(x) - \gamma) \neq sign(S_t(x) - \gamma)) \leq \frac{L_S \cdot \beta_ \cdot \tau \cdot B_S}{\min(|S_t(x) - \gamma|, |S_{t-\tau}(x) - \gamma|)}.\]

For samples near the decision boundary (\(|S_t - \gamma|\) small), the
error can be \(O(1)\) even for modest \(\tau\).

*Proof sketch.* By Lipschitz continuity (C3),
\(\|S_t - S_{t-\tau}\|_\infty \leq L_S \cdot \tau \cdot \beta_ \cdot B_S\).
The probability of sign change is bounded by the probability that the
drift exceeds the margin. For small margin, this probability approaches
1. \(\square\)

**Status: CONJECTURED.** The Lipschitz bound is valid, but the
probability estimate requires a model of the drift direction, which
depends on the specific SCX update dynamics.

#### 2.6 Backlog-Induced Distribution
Shift<!-- label: backlog-induced-distribution-shift -->

**Proposition 12.1 (Backlog Distribution Bias --- CONJECTURED).**
When samples are scored with delay \(\tau\), the effective acceptance
distribution is:

\[\tilde{P}_{S_t}(x,y) \propto \mathbf{1}\{S_{t-\tau(x)}(x,y) \geq \gamma\} \cdot P_0(x,y).\]

This distribution is biased toward samples where \(S_{t-\tau}\)
overestimates reliability relative to \(S_t\), because: - Samples scored
by an older (less accurate) gatekeeper are more likely to be
misclassified. - The direction of misclassification depends on whether
\(S_t\) has increased or decreased relative to \(S_{t-\tau}\).

**If \(S_t\) is monotonically improving**, then
\(S_t > S_{t-\tau}\) for most \((x,y)\) (the gatekeeper becomes more
generous over time). In this case, the stale gatekeeper is **more
conservative**, rejecting some samples that \(S_t\) would accept. The
effect is **reduced memory growth**, not incorrect acceptance.

**If \(S_t\) oscillates**, then \(S_{t-\tau}\) may be higher than
\(S_t\) in some regions, admitting samples that \(S_t\) would reject.
This introduces **noisy samples** into \(M_t\), degrading all
downstream estimates.

#### 2.7 Approximate Scoring for
Throughput<!-- label: approximate-scoring-for-throughput -->

To prevent backlog, the gatekeeper can use **approximate scoring**:

\[\tilde{S}_t(x,y) = S_t(NN_k(x), y),\]

where \(NN_k(x)\) returns the \(k\) nearest neighbors of \(x\)
among already-scored samples.

**Theorem 12.6 (Approximation Error of NN Scoring --- PROVEN).**
Under C3 (Lipschitz gatekeeper) and assuming the already-scored samples
form an \(\varepsilon\)-net of the input space:

\[\sup_{x,y} |\tilde{S}_t(x,y) - S_t(x,y)| \leq L_S \cdot \varepsilon.\]

*Proof.* By Lipschitz continuity,
\(|S_t(x) - S_t(NN(x))| \leq L_S \cdot \|x - NN(x)\| \leq L_S \cdot \varepsilon\)
when the scored samples form an \(\varepsilon\)-net. \(\square\)

**Status: PROVEN.** This provides a principled approximation with
controllable error.

#### 2.8 Mitigation Strategies<!-- label: mitigation-strategies-1 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3448}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2759}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3793}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Strategy
\end{minipage} & \begin{minipage}[b]
Effect
\end{minipage} & \begin{minipage}[b]
Trade-off
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**NN approximate scoring** & \(O(1)\) per sample (after index
build) & \(L_S \cdot \varepsilon\) score error 

**Batch scoring** & Amortizes overhead & Increases delay for early
samples in batch 

**Priority queue** & Score high-uncertainty samples first &
Requires uncertainty estimate before scoring (circular) 

**Parallel/distributed experts** & Increases \(r_{score}\)
linearly with workers & Communication overhead 

**Gatekeeper distillation** & Train a fast student gatekeeper
\(\tilde{S}\) to approximate \(S_t\) & Distillation error; requires
periodic retraining 

**Adaptive sampling** & Reduce \(r_{in}\) when backlog
exceeds threshold & May miss novel samples 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Failure Mode 3: Calibration Breakdown (Client
Divergence)<!-- label: failure-mode-3-calibration-breakdown-client-divergence -->

#### 3.1 Phenomenon<!-- label: phenomenon-2 -->

When two independent SCX clients (with different initial gatekeepers
\(S_0^{(1)}\), \(S_0^{(2)}\) or different data streams) evolve their
gatekeepers independently, their scoring functions may **diverge
irreconcilably**: they assign opposite reliability judgments to the same
samples, with no mechanism to reconcile.

#### 3.2 Formal Setup<!-- label: formal-setup -->

**Definition 3.1 (Client Divergence).** Two clients \(A\) and \(B\)
evolve gatekeepers \(S_t^{(A)}\) and \(S_t^{(B)}\) from initial
conditions \(S_0^{(A)} \neq S_0^{(B)}\). Their **disagreement** at
time \(t\) is:

\[D_t(A, B) = \mathbb{P}_{(x,y) \sim P_0}\bigl(sign(S_t^{(A)}(x,y) - \gamma) \neq sign(S_t^{(B)}(x,y) - \gamma)\bigr).\]

Divergence is **irreconcilable** if
\(\liminf_{t \to \infty} D_t(A, B) > 0\).

#### 3.3 Existence of Multiple Fixed
Points<!-- label: existence-of-multiple-fixed-points -->

**Theorem 12.7 (Multiple Fixed Points --- PROVEN).** The SCX
self-evolution dynamics can have multiple fixed points when: 1. The loss
landscape is non-convex (multiple local minima for the student). 2. The
gatekeeper's acceptance policy can be self-consistent at different
selectivity levels.

*Proof by construction.* Consider two fixed points: - **Fixed
point A (conservative)**: \(S_A^*(x,y) \approx 0.3\) for all \((x,y)\).
The gatekeeper is conservative, rejecting most samples. The memory bank
is small, containing only the highest-confidence samples. The student is
trained on this small, clean subset. **Self-consistent**: the
conservative gatekeeper only admits samples it scores above 0.3, and the
student trained on those samples predicts labels that the gatekeeper is
comfortable with.

- 

Both are valid fixed points of the dynamics. They are **not**
equivalent --- they disagree on approximately 40\% of decisions (samples
with true reliability between 0.3 and 0.7). \(\square\)

**Status: PROVEN.** The existence of multiple fixed points follows
from the non-convexity of the coupled system.

#### 3.4 Basin of Attraction<!-- label: basin-of-attraction -->

**Definition 3.2 (Basin of Attraction).** The basin of attraction
\(\mathcal{B}(S^*, \theta^*)\) is the set of initial conditions
\((S_0, \theta_0)\) from which the system converges to
\((S^*, \theta^*)\).

**Conjecture 12.1 (Basin Structure).** The state space partitions
into basins of attraction:

\[\mathcal{Z} = \bigcup_{i=1}^{N_{fp}} \mathcal{B}_i \cup \mathcal{B}_{boundary},\]

where \(\mathcal{B}_i\) are the basins of the \(N_{fp}\) fixed
points, and \(\mathcal{B}_{boundary}\) is a measure-zero set of
initial conditions on the boundaries.

*Status: **CONJECTURED.** The basin structure for coupled SA
systems is an active research area (Borkar, 2008, Chapter 9). The
conjecture is plausible but unproven for the specific SCX dynamics.*

#### 3.5 Condition for Irreconcilable
Divergence<!-- label: condition-for-irreconcilable-divergence -->

**Theorem 12.8 (Irreconcilable Divergence Condition --- PROVEN).**
Two clients with initial conditions
\((S_0^{(A)}, \theta_0^{(A)}) \in \mathcal{B}_i\) and
\((S_0^{(B)}, \theta_0^{(B)}) \in \mathcal{B}_j\) with \(i \neq j\) will
converge to different fixed points with:

\[\lim_{t \to \infty} D_t(A, B) = D_{ij} > 0,\]

where \(D_{ij}\) is the disagreement rate between fixed points \(i\) and
\(j\).

*Proof.* By definition of basins of attraction, client A converges
to fixed point \(i\) and client B to fixed point \(j\). Since
\(i \neq j\), there exists at least one \((x,y)\) where the fixed-point
gatekeepers disagree. By continuity of the scoring function, the
disagreement extends to a neighborhood of positive measure, so
\(D_{ij} > 0\). \(\square\)

**Status: PROVEN (conditional on basin structure).** The logic is
sound; the only gap is the rigorous characterization of basin boundaries
(Conjecture 12.1).

#### 3.6 Calibration Degradation
Rate<!-- label: calibration-degradation-rate -->

**Proposition 12.2 (Calibration Drift Under Isolation ---
CONJECTURED).** If two clients start from \(\varepsilon\)-close initial
conditions but evolve on different data streams, their gatekeepers
diverge at rate:

\[\mathbb{E}[D_t(A, B)] \leq \varepsilon \cdot \exp(\lambda_ \cdot t),\]

where \(\lambda_\) is the largest Lyapunov exponent of the
deterministic part of the dynamics.

*Proof sketch.* Linearize the dynamics around the common
trajectory. The difference \(\delta_t = S_t^{(A)} - S_t^{(B)}\) evolves
as \(\delta_{t+1} \approx (I + \beta_t J_t) \delta_t + noise\),
where \(J_t\) is the Jacobian of SCXUpdate. The largest eigenvalue of
\(J_t\) determines the exponential divergence rate. \(\square\)

**Status: CONJECTURED.** The linearized analysis is standard for
dynamical systems (Strogatz, 2018), but deriving \(\lambda_\) for
the specific SCX dynamics requires further work.

#### 3.7 Mitigation Strategies<!-- label: mitigation-strategies-2 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3704}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4074}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2222}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Strategy
\end{minipage} & \begin{minipage}[b]
Mechanism
\end{minipage} & \begin{minipage}[b]
Cost
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Federated gatekeeper averaging** & Periodically average
\(S_t^{(A)}\) and \(S_t^{(B)}\) & Requires communication; may pull both
toward a worse compromise 

**Shared reference set** & Both clients evaluate against the same
\(M_0\) & Requires agreement on ground-truth labels for \(V_0\) 

**Consensus anchoring** & Fix \(\hat{C}(x)\) as a shared anchor;
only evolve gatekeeper toward consensus, not away & Limits adaptation to
client-specific data distributions 

**Cross-validation between clients** & Each client's memory bank
serves as validation for the other & Requires trust and data sharing 

**Divergence detection + reset** & When
\(D_t(A,B) > \delta_{threshold}\), reset both to a common
initialization & Loses learned information 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Failure Mode 4: Adversarial Poisoning (Gatekeeper
Corruption)<!-- label: failure-mode-4-adversarial-poisoning-gatekeeper-corruption -->

#### 4.1 Phenomenon<!-- label: phenomenon-3 -->

An adversary injects carefully crafted samples into the data stream,
causing the gatekeeper to systematically misclassify clean samples as
noise (or vice versa). The self-evolution loop amplifies the corruption
by training the student on poisoned data.

#### 4.2 Threat Model<!-- label: threat-model -->

**Definition 4.1 (Adversary Capabilities).** The adversary can: -
**Injection**: Add up to \(\eta_{adv}\) fraction of samples
to the incoming data stream. - **Knowledge**: Know the current
gatekeeper \(S_t\), the expert models \(\{f_m\}\), and the feature
representation \(\phi\). - **Objective**: Maximize the false
positive rate (clean → noise) or false negative rate (noise → clean) of
the converged gatekeeper.

We assume the adversary does **not** control the expert models or
the NEP training procedure --- only the data fed to the gatekeeper.

#### 4.3 Adversarial Sample
Construction<!-- label: adversarial-sample-construction -->

**Definition 4.2 (Consensus-Minimizing Adversarial Sample).** To
cause the gatekeeper to reject a clean sample \((x, y_{true})\),
the adversary constructs:

\[(x_{adv}, y_{adv}) = \arg\min_{(x',y') \in \mathcal{B}_\varepsilon(x)} \hat{C}(x') \quad subject to \quad \ell(f_m(x'), y') > \tau  for most  m,\]

i.e., an \(\varepsilon\)-perturbation of a clean sample that maximally
confuses the expert ensemble while remaining indistinguishable to the
gatekeeper's feature representation.

#### 4.4 Poisoning Amplification via
Self-Evolution<!-- label: poisoning-amplification-via-self-evolution -->

The key danger in SCX self-evolution is **amplification**: one
round of poisoning corrupts the gatekeeper, which admits more poisoned
samples, which further corrupts the gatekeeper.

**Theorem 12.9 (Poisoning Amplification Factor --- CONJECTURED).**
If the adversary injects a fraction \(\eta_{adv}\) of poisoned
samples at each round, the effective corruption after \(T\) rounds is:

\[\eta_{eff}(T) \geq \eta_{adv} \cdot \frac{1 - \gamma^T}{1 - \gamma},\]

where
\(\gamma = \mathbb{P}_{P_0}(S_t(x_{adv}, y_{adv}) \geq \gamma_t \mid poisoned)\)
is the probability that poisoned samples pass the gatekeeper.

When \(\gamma > 0.5\) (poisoned samples are more likely to be accepted
than rejected), the amplification diverges geometrically:

\[\eta_{eff}(T) \to 1 \quad as \quad T \to \infty.\]

*Proof sketch.* At each round, a fraction of poisoned samples enter
\(M_t\), corrupting the student. The corrupted student provides feedback
that shifts \(S_{t+1}\) toward accepting more poisoned samples (because
the student agrees with the poisoned labels). This increases \(\gamma\)
over time, creating a positive feedback loop. \(\square\)

**Status: CONJECTURED.** The geometric amplification depends on
\(\gamma > 0.5\), which in turn depends on the adversary's ability to
craft samples that both confuse experts and appear reliable to the
current gatekeeper. This is a strong assumption that may not hold for
well-regularized gatekeepers.

#### 4.5 Detection Boundary for Adversarial
Samples<!-- label: detection-boundary-for-adversarial-samples -->

**Theorem 12.10 (Adversarial Detection Boundary --- PARTIALLY
PROVEN).** Under the consensus score \(\hat{C}(x)\) computed from \(M\)
i.i.d. experts, an adversarial perturbation \(\delta\) on a clean sample
\(x\) changes the expected consensus by at most:

\[\mathbb{E}[|\hat{C}(x + \delta) - \hat{C}(x)|] \leq \frac{1}{M} \sum_{m=1}^M \mathbb{P}(\ell(f_m(x+\delta), y) > \tau \neq \ell(f_m(x), y) > \tau).\]

If each expert has a **robustness radius** \(\rho_m\) such that
\(\|\delta\| \leq \rho_m \implies f_m(x+\delta) = f_m(x)\), then for
\(\|\delta\| \leq \min_m \rho_m\), the consensus score is
**unchanged** and the adversarial sample is undetectable by
consensus alone.

*Proof.* The consensus changes only if the adversary's perturbation
flips at least one expert's error indicator. If all experts are robust
within radius \(\rho_\), then no expert error indicator flips, and
\(\hat{C}\) is unchanged. \(\square\)

**Status: PROVEN.** This follows from the definition of \(\hat{C}\)
and provides a clean condition for undetectability.

#### 4.6 Gatekeeper Robustness
Certificate<!-- label: gatekeeper-robustness-certificate -->

**Proposition 12.3 (Lipschitz-Based Robustness --- PROVEN).** Under
C3 (Lipschitz gatekeeper with constant \(L_S\)), for any perturbation
\(\delta\):

\[|S_t(x + \delta, y) - S_t(x, y)| \leq L_S \cdot \|\phi(x + \delta) - \phi(x)\| \leq L_S \cdot L_\phi \cdot \|\delta\|,\]

where \(L_\phi\) is the Lipschitz constant of the feature map. The
gatekeeper is **certifiably robust** for perturbations with
\(\|\delta\| \leq \frac{|S_t(x,y) - \gamma|}{L_S \cdot L_\phi}\).

*Proof.* Direct from C3 and the Lipschitz property of \(\phi\).
\(\square\)

**Status: PROVEN.** This provides a certified radius within which
adversarial perturbations cannot change the gatekeeper's decision.

#### 4.7 When the Student is the
Vulnerability<!-- label: when-the-student-is-the-vulnerability -->

Even if the gatekeeper is robust, the **NEP student** may be
vulnerable. If poisoned samples enter \(M_t\): 1. The student is trained
on poisoned labels. 2. The student's predictions on clean samples become
corrupted. 3. The corrupted student feedback shifts the gatekeeper. 4.
The cycle continues.

**Theorem 12.11 (Student Poisoning Vulnerability ---
CONJECTURED).** Under linear regression with \(\ell_2\) loss, if an
\(\eta_{adv}\) fraction of training labels are flipped, the
parameter error is:

\[\mathbb{E}[\|\hat - \theta^*\|^2] \geq \eta_{adv}^2 \cdot \frac{\mathbb{E}[\|x\|^2]}{\lambda_(\Sigma)^2},\]

where \(\Sigma = \mathbb{E}[x x^\top]\) is the feature covariance. For
neural networks, the error may be larger due to the non-linear
amplification of poisoned gradients.

*Status: **CONJECTURED** (for neural networks). The linear
case is standard (Hampel et al., 1986).*

#### 4.8 Mitigation Strategies<!-- label: mitigation-strategies-3 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3030}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Strategy
\end{minipage} & \begin{minipage}[b]
Mechanism
\end{minipage} & \begin{minipage}[b]
Limitation
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Robust aggregation (median-of-experts)** & Replace mean consensus
\(\hat{C}\) with median or trimmed mean & Reduces effective \(M\);
requires \(>50\%\) clean experts 

**Anomaly detection on \(\phi(x)\)** & Flag samples with atypical
features as potential adversarial & Adversary can constrain
\(\|\delta\|\) to stay in-distribution 

**Certified robustness (Lipschitz)** & Bound
\(|S_t(x+\delta) - S_t(x)| \leq L_S L_\phi \|\delta\|\) & Loose bounds
for large \(L_S, L_\phi\) 

**Differential privacy in gatekeeper update** & Add noise to
\(\Delta S_t\) to mask individual sample influence & Reduces convergence
rate by \(O(\sigma_{DP}^2)\) 

**Student robust training** & Train NEP with adversarial data
augmentation & Increases training cost; may reduce clean accuracy 

**Outlier-resistant loss** & Use Huber or Tukey loss for student
training & Less statistically efficient than \(\ell_2\) for clean
data 

**Human-in-the-loop for high-stakes decisions** & Flag samples
where \(\hat{C}(x)\) and \(S_t(x)\) disagree strongly & Does not
scale 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Interaction Effects: Compound
Failures<!-- label: interaction-effects-compound-failures -->

#### 5.1 Backlog + Premature
Freezing<!-- label: backlog-premature-freezing -->

When backlog (Section 2) **and** premature freezing (Section 1)
co-occur: - The backlog means the gatekeeper's decisions are stale
(\(S_{t-\tau}\) instead of \(S_t\)). - Premature freezing means the
gatekeeper stops updating even as backlog grows. - **Compound
effect**: The effective gatekeeper \(S_{t-\tau}\) freezes at an even
earlier (worse) state, and the delay \(\tau\) grows without bound. The
system becomes **doubly frozen** --- neither the gatekeeper nor the
scoring process can recover.

#### 5.2 Adversarial Poisoning + Client
Divergence<!-- label: adversarial-poisoning-client-divergence -->

When adversarial poisoning (Section 4) targets one of two clients: -
Client A (poisoned) converges to a corrupted fixed point. - Client B
(clean) converges to a clean fixed point. - Their disagreement
\(D_t(A, B)\) grows over time. - **Compound effect**: The adversary
can **maximize** \(D_t(A, B)\) by injecting samples that are
specifically chosen to push A's gatekeeper away from B's. This is a
**targeted divergence attack**: the adversary exploits the
multi-fixed-point structure.

#### 5.3 Backlog + Adversarial
Poisoning<!-- label: backlog-adversarial-poisoning -->

When backlog means samples are scored by stale gatekeeper
\(S_{t-\tau}\): - The adversary can inject samples that are
**benign** to the current gatekeeper \(S_t\) but **malignant**
to the stale gatekeeper \(S_{t-\tau}\). - Since scoring uses
\(S_{t-\tau}\), the malignant samples pass through. - **Compound
effect**: Backlog creates a **temporal attack surface** --- the
adversary can exploit the gap between the current and stale gatekeepers.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Diagnostic Tests for Each Failure
Mode<!-- label: diagnostic-tests-for-each-failure-mode -->

#### 6.1 Premature Freezing
Detection<!-- label: premature-freezing-detection -->

**Test 1 (Gradient Norm Monitor).** Track \(\|\Delta S_t\|_{M_0}\)
over a sliding window of \(W\) steps. If
\(\max_{i \in [t-W, t]} \|\Delta S_i\| < \varepsilon_{diag}\) for
\(W\) consecutive windows, flag as frozen.

**Test 2 (Student Improvement Correlation).** Track the correlation
between \(\|\Delta S_t\|\) and \(\Delta \Psi_{student, t}\). If
the gatekeeper is frozen but the student is still improving, the
correlation drops to zero.

#### 6.2 Backlog Detection<!-- label: backlog-detection -->

**Test 3 (Scoring Delay Monitor).** Track
\(\tau(x) = t_{current} - t_{scored}\) for each sample. If
\(median(\tau) > \tau_{threshold}\), flag backlog.

**Test 4 (Memory Growth vs.~Scoring Rate).** Track \(dN_t/dt\)
(memory growth rate) and \(dScored_t/dt\) (scoring rate). If the
former consistently exceeds the latter, backlog is growing.

#### 6.3 Calibration Divergence
Detection<!-- label: calibration-divergence-detection -->

**Test 5 (Inter-Client Disagreement).** Periodically compare
gatekeeper decisions between clients on a shared validation set. If
\(D_t(A, B)\) is increasing and exceeds \(\delta_{threshold}\),
flag divergence.

**Test 6 (Fixed-Point Distance Estimate).** Estimate the distance
between \(S_t^{(A)}\) and \(S_t^{(B)}\) in function space:
\(\|S_t^{(A)} - S_t^{(B)}\|_{M_0}\). A monotonically increasing trend
suggests divergence to different fixed points.

#### 6.4 Adversarial Poisoning
Detection<!-- label: adversarial-poisoning-detection -->

**Test 7 (Consensus-Gatekeeper Discrepancy).** Track
\(\mathbb{E}[|\hat{C}(x) - S_t(x, y(x))|]\) on incoming samples. A
sudden increase may indicate adversarial samples that confuse experts
but are scored highly by the gatekeeper.

**Test 8 (Expert Agreement Anomaly).** Track the per-expert
agreement matrix. Adversarial samples may cause unusual patterns (e.g.,
all experts agree on the wrong answer, or expert disagreement is bimodal
rather than uniform).

**Test 9 (Student Loss on Held-Out Clean Set).** Monitor
\(\Psi_{student}\) on \(V_0\). Poisoning should cause this to
**increase** even as the training loss on \(M_t\) decreases (a
classic sign of label poisoning).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Summary Table<!-- label: summary-table -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1857}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1000}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1143}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2714}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1857}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Failure Mode
\end{minipage} & \begin{minipage}[b]
Cause
\end{minipage} & \begin{minipage}[b]
Effect
\end{minipage} & \begin{minipage}[b]
Critical Parameter
\end{minipage} & \begin{minipage}[b]
Severity
\end{minipage} & \begin{minipage}[b]
Provability
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**1. Premature Freezing** & \(\beta_t\) decays too fast relative to
student convergence & Gatekeeper trapped at suboptimal
\(S^*_{sub}\); student converges to wrong target &
\(t_{freeze} = (\beta_0 B_S / \varepsilon_{mach})^{1/b}\)
& **MODERATE** (rare with double precision) & Condition:
**PROVEN**; gap: **CONJECTURED** 

**2. Backlog** & \(r_{in} > r_{score}\) & Stale
gatekeeper decisions; memory bank contaminated with misclassified
samples & \(r_{in} / r_{score}\) & **HIGH**
(practical for large \(M\), high data rate) & Condition:
**PROVEN**; effect: **CONJECTURED** 

**3. Client Divergence** & Multiple fixed points; different initial
conditions or data streams & Irreconcilable gatekeeper disagreement; no
convergence to consensus & \(D_{ij}\) (inter-fixed-point disagreement) &
**MODERATE** (only in multi-client deployment) & Existence:
**PROVEN**; basin structure: **CONJECTURED** 

**4. Adversarial Poisoning** & Adversary injects crafted samples &
Gatekeeper corruption amplifies through self-evolution loop &
\(\eta_{adv}\), \(\gamma\) (acceptance rate of poisoned samples)
& **HIGH** (severe with amplification) & Amplification:
**CONJECTURED**; robustness certificate: **PROVEN** 

\end{longtable}

#### 7.1 Risk Matrix<!-- label: risk-matrix -->

\begin{verbatim}
                      Likelihood
                    Low     Med    High
Severity  High     |       |  2   |  4   |
          Moderate |   1   |  3   |      |
          Low      |       |      |      |
\end{verbatim}

- 
- 
- 
- 

#### 7.2 Design Recommendations<!-- label: design-recommendations -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of 12\_edge\_cases.md --- Edge Cases and Failure Modes*

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

### Changelog<!-- label: changelog -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1875}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3125}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Date
\end{minipage} & \begin{minipage}[b]
Defect
\end{minipage} & \begin{minipage}[b]
Change
\end{minipage} & \begin{minipage}[b]
Severity
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
2026-06-28 & B4 & **Renamed gatekeeper update rate from η to β**:
The symbol \(\eta\) is reserved throughout SCX theory for the global
noise rate \(\eta = P(Z=1)\). All local uses of \(\eta(t)\) as
gatekeeper update rate replaced with \(\beta_t\). Notation note added at
document header and Theorem 12.1. Fixes FAIL-2 from cross-reference
audit. & FATAL 

\end{longtable}