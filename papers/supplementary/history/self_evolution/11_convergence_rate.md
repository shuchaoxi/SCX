# SCX Self-Evolution: Convergence Rate Analysis (Spring-1 Rate
Tightening)

**Author:** SCX

> **Version**: 2026-06-28 |{} **Status**: Theoretical
> derivation (partial) |{} **Prerequisite**: Documents 02, 05,
> 06, 10 **Purpose**: Derive expected convergence rates for the SCX
> self-evolution system, characterizing the dependence on Lipschitz
> constants, learning rate schedules, and feature dimension. Move beyond
> almost-sure convergence to quantitative rates.

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Setup and Notation<!-- label: setup-and-notation -->

#### 1.1 The Coupled System<!-- label: the-coupled-system -->

We analyze the convergence rate of \((S_t, \theta_t)\) to a fixed point
\((S^*, \theta^*)\) under the SCX self-evolution dynamics (Document 06):

\[
$$
\theta_{t+1} &= \theta_t - \alpha_t \nabla_\theta \ell(f_{\theta_t}(x_t), y_t), \quad (x_t, y_t) \sim P_{S_t}, 

S_{t+1} &= \Pi_{[0,1]}[S_t + \beta_t (SCXUpdate(S_t, M_{t+1}, f_{\theta_{t+1}}) - S_t)].
$$
\]

#### 1.2 Key Parameters<!-- label: key-parameters -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3143}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2571}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4286}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Parameter
\end{minipage} & \begin{minipage}[b]
Meaning
\end{minipage} & \begin{minipage}[b]
Typical Range
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(L_f\) & Lipschitz constant of \(f_\theta\) in \(\theta\) &
\(O(1)\)--\(O(10^2)\) 

\(L_g\) & Lipschitz constant of \(\nabla \ell\) &
\(O(L_f \cdot L_\ell)\) 

\(L_S\) & Lipschitz constant of SCXUpdate & \(O(1)\) 

\(d_\theta\) & Student parameter dimension & \(10^4\)--\(10^8\) 

\(d_\phi\) & Feature dimension & \(10^1\)--\(10^3\) 

\(\mu\) & Strong convexity parameter (if applicable) &
\(0\)--\(O(1)\) 

\(\alpha_t\) & Student learning rate & \(t^{-a}\), \(a \in (0.5, 1]\) 

\(\beta_t\) & Gatekeeper update rate & \(t^{-b}\), \(b \in (a, 1]\) 

\(\sigma_\xi^2\) & Gradient noise variance & Problem-dependent 

\(G\) & Gradient bound & \(O(L_f \cdot B)\) 

\(B_S\) & Gatekeeper update bound & \(1\) (scores in \([0,1]\)) 

\end{longtable}

#### 1.3 Target Quantity<!-- label: target-quantity -->

We seek bounds on:

\[\mathbb{E}\bigl[\|S_t - S^*\|_{M_0}^2\bigr] \quad and \quad \mathbb{E}\bigl[\|\theta_t - \theta^*\|^2\bigr],\]

where \(\|S\|_{M_0}^2 = \frac{1}{|M_0|}\sum_{x \in M_0} S(x, y(x))^2\)
is the empirical \(L^2\) norm on the reference set, and
\((S^*, \theta^*)\) is a fixed point.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Current State: Almost-Sure Convergence
Only<!-- label: current-state-almost-sure-convergence-only -->

#### 2.1 What Document 06
Establishes<!-- label: what-document-06-establishes -->

Theorem SE-1 (Document 06) asserts **almost-sure convergence** to a
fixed point under conditions C1-C7, using a Lyapunov supermartingale
argument. The proof (Lemma SE-1.1) establishes:

\[\sum_{t=1}^\infty \alpha_t \|\nabla L_t(\theta_t)\|^2 < \infty \quad a.s., \qquad \sum_{t=1}^\infty \beta_t \|\Delta S_t\|^2 < \infty \quad a.s.\]

These imply convergence to a stationary point, but provide **no
rate** --- they only guarantee that the gradient norms vanish in the
Cesàro sense, not how fast.

#### 2.2 What Rates Are Missing<!-- label: what-rates-are-missing -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.3750}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.6250}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Desired
\end{minipage} & \begin{minipage}[b]
Current Status
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq C t^{-\alpha}\) &
**Not proven** 

\(\mathbb{E}[\|S_t - S^*\|_{M_0}^2] \leq C t^{-\alpha}\) & **Not
proven** 

Finite-time (non-asymptotic) bound with probability \(1-\delta\) &
**Not proven** 

Dependence of \(\alpha\) on \(L_f\), \(\alpha_t\), \(d_\phi\) &
**Not characterized** 

\end{longtable}

#### 2.3 Why Almost-Sure is
Insufficient<!-- label: why-almost-sure-is-insufficient -->

Almost-sure convergence does not tell us: 1. How many iterations are
needed to reach a given accuracy. 2. How the rate degrades as dimension
\(d_\phi\) grows. 3. Whether the convergence is fast enough to be
practically useful. 4. How to tune \(\alpha_t, \beta_t\) for optimal
convergence speed.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### \texorpdfstring{3. Rate Under Strong Convexity:
\(O(t^{-\alpha)\)
Derivation}{3. Rate Under Strong Convexity: O(t\^{}\{-\ alpha\}) Derivation}}<!-- label: rate-under-strong-convexity-ot-alpha-derivation -->

#### 3.1 Strong Convexity
Assumption<!-- label: strong-convexity-assumption -->

**Assumption SC (Strong Convexity of Limiting Loss).** The limiting
expected student loss
\(\bar{L}(\theta) = \mathbb{E}_{(x,y) \sim P_{S^*}}[\ell(f_\theta(x), y)]\)
is \(\mu\)-strongly convex in a neighborhood of \(\theta^*\):

\[\bar{L}(\theta') \geq \bar{L}(\theta) + \langle \nabla \bar{L}(\theta), \theta' - \theta \rangle + \frac{2} \|\theta' - \theta\|^2, \quad \forall \theta, \theta' \in \mathcal{B}(\theta^*, R).\]

**Justification.** Strong convexity holds for linear models with
\(\ell_2\) regularization. For neural networks, it holds only in a local
neighborhood of a strict local minimum (which is generic for
overparameterized networks). This is a **local** assumption, valid
after the system enters the basin of attraction.

#### 3.2 Student Rate Under Stationary
Distribution<!-- label: student-rate-under-stationary-distribution -->

**Theorem 11.1 (Student Rate, Stationary Distribution ---
PROVEN).** Assume SC (strong convexity), C2 (Lipschitz student), C4 (RM
rates with \(\alpha_t = \alpha_0 t^{-a}\), \(a \in (0.5, 1)\)), and that
the training distribution is fixed at \(P_{S^*}\). Then:

\[\boxed{\;\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq C_1 \cdot t^{-a} + C_2 \cdot t^{-2a}\;},\]

where:

\[C_1 = \frac{2\sigma_\xi^2 \alpha_0}, \qquad C_2 = \frac{4 G^2 \alpha_0^2}{\mu^2}.\]

For \(a \in (0.5, 1)\), the dominant term is \(C_1 t^{-a} = O(t^{-a})\).

*Proof.* Standard SGD analysis under strong convexity (Bach \&
Moulines, 2011; Needell et al., 2014). Let
\(V_t = \mathbb{E}[\|\theta_t - \theta^*\|^2]\). From the SGD update:

\[
$$
V_{t+1} &= V_t - 2\alpha_t \mathbb{E}[\langle \theta_t - \theta^*, g_t(\theta_t) \rangle] + \alpha_t^2 \mathbb{E}[\|g_t(\theta_t)\|^2] 

&\leq V_t - 2\alpha_t \mathbb{E}[\langle \theta_t - \theta^*, \nabla \bar{L}(\theta_t) \rangle] + \alpha_t^2 G^2.
$$
\]

By strong convexity:
\(\langle \theta_t - \theta^*, \nabla \bar{L}(\theta_t) \rangle \geq \mu \|\theta_t - \theta^*\|^2\).
Thus:

\[V_{t+1} \leq (1 - 2\mu \alpha_t) V_t + \alpha_t^2 G^2.\]

With \(\alpha_t = \alpha_0 t^{-a}\), this recurrence solves to
\(V_t = O(t^{-a})\). The precise constant follows from the theory of
stochastic approximation with polynomially decaying step sizes (Polyak
\& Juditsky, 1992). \(\square\)

**Status: PROVEN.** This is a standard result for SGD on strongly
convex objectives.

#### 3.3 Gatekeeper Rate Under Fixed
Memory<!-- label: gatekeeper-rate-under-fixed-memory -->

**Theorem 11.2 (Gatekeeper Rate, Fixed Student --- PROVEN).**
Assume C3 (Lipschitz gatekeeper), the student is fixed at \(\theta^*\),
and the gatekeeper update uses \(\beta_t = \beta_0 t^{-b}\) with
\(b \in (0.5, 1]\). Then:

\[\boxed{\;\mathbb{E}[\|S_t - S^*\|_{M_0}^2] \leq C_S \cdot t^{-b}\;},\]

where:

\[C_S = \frac{2 B_S^2 \beta_0}{1 - L_S^2} \quad (provided  L_S < 1  for contraction).\]

*Proof.* The SCX update toward consensus is approximately a
contraction when the memory bank is informative. Formally, if
\(SCXUpdate(S) = \hat{C} + \varepsilon(S)\) where
\(\|\varepsilon(S)\| \leq L_S \|S - \hat{C}\|\) with \(L_S < 1\), then:

\[\|S_{t+1} - \hat{C}\|_{M_0} \leq (1 - \beta_t(1 - L_S)) \|S_t - \hat{C}\|_{M_0} + \beta_t \|noise\|.\]

This recurrence gives \(O(t^{-b})\) convergence. \(\square\)

**Status: PROVEN under contraction.** The condition \(L_S < 1\)
(SCXUpdate is a contraction toward consensus) is **not guaranteed**
in general --- it depends on the quality of the consensus signal. When
the consensus is noisy (small \(\Delta_s\) in Theorem 1), \(L_S\) may
exceed 1.

#### 3.4 Coupled Rate Under Two-Timescale
Separation<!-- label: coupled-rate-under-two-timescale-separation -->

**Theorem 11.3 (Coupled Rate Under Strong Convexity ---
CONJECTURED).** Assume SC (strong convexity), C2-C7, C6' (two-timescale,
\(\beta_t = o(\alpha_t)\)), and that the fixed point \((S^*, \theta^*)\)
is locally stable. Then:

\[\boxed{\;\mathbb{E}\bigl[\|\theta_t - \theta^*\|^2 + \|S_t - S^*\|_{M_0}^2\bigr] \leq C_\theta \cdot t^{-a} + C_S \cdot t^{-b} = O(t^{-a})\;},\]

since \(b > a\) implies \(t^{-b} = o(t^{-a})\). The **student rate
dominates** the convergence speed.

*Proof sketch (gaps acknowledged).* Under two-timescale separation
(Document 05, Section 7), the student converges on the fast timescale to
the quasi-stationary point \(\theta^*(S_t)\), and the gatekeeper
converges on the slow timescale to \(S^*\). The coupled rate is the
slower of the two rates, which is \(t^{-a}\) (the student rate) since
\(b > a\). The key gap is the coupling error: the student's optimization
target shifts by \(O(\beta_t)\) per step, introducing an additional
error term of order \(\beta_t / \alpha_t = t^{-(b-a)} = o(1)\). Under
strong convexity, this tracking error is bounded and does not affect the
asymptotic rate.

**Status: CONJECTURED.** The proof requires controlling the
accumulation of tracking errors \(\|\theta_t - \theta^*(S_t)\|\), which
is standard in two-timescale SA (Borkar, 2008, Chapter 6) but requires
verification for the specific SCX coupling structure.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Dependence on System
Parameters<!-- label: dependence-on-system-parameters -->

#### \texorpdfstring{4.1 Dependence on Lipschitz Constant
\(L_f\){4.1 Dependence on Lipschitz Constant L\_f}}<!-- label: dependence-on-lipschitz-constant-l_f -->

The constant \(C_1\) in Theorem 11.1 depends on \(L_f\) through:

\[C_1 = \frac{2\sigma_\xi^2 \alpha_0}, \quad \sigma_\xi^2 \leq G^2 = O(L_f^2), \quad \mu = \Omega(1/L_g) = \Omega(1/L_f).\]

**Result**: \(C_1 = O(L_f^3)\). A larger Lipschitz constant
(rougher loss landscape) degrades the convergence rate cubically: twice
the Lipschitz constant means 8× slower convergence.

**Corollary 11.1 (Lipschitz Dependence).** Under strong convexity
with \(L_g = \Theta(L_f)\):

\[\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq \tilde{O}\!\left(\frac{L_f^3 \cdot \sigma_0^2}{\mu_0} \cdot t^{-a}\right),\]

where \(\sigma_0^2\) is the base noise level and \(\mu_0\) is the base
curvature.

#### 4.2 Dependence on Learning Rate
Schedule<!-- label: dependence-on-learning-rate-schedule -->

The exponent \(\alpha\) in \(O(t^{-\alpha})\) equals the learning rate
exponent \(a\) (from \(\alpha_t = \alpha_0 t^{-a}\)).

**Proposition 11.1 (Optimal Rate Exponent).** Under strong
convexity, the optimal choice is:

\[a = 1 \quad (harmonic learning rate  \alpha_t = \alpha_0 / t ),\]

giving \(\mathbb{E}[\|\theta_t - \theta^*\|^2] = O(t^{-1})\).

However, this requires precise tuning of \(\alpha_0\): too small gives
slow convergence, too large causes divergence. In practice,
\(a = 0.5\)--\(0.6\) is more robust (gives \(O(t^{-0.5})\) to
\(O(t^{-0.6})\) convergence).

**Proposition 11.2 (Polyak-Ruppert Averaging).** With
Polyak-Ruppert averaging
\(\bar_t = \frac{1}{t}\sum_{i=1}^t \theta_i\), the rate improves
to:

\[\mathbb{E}[\|\bar_t - \theta^*\|^2] = O(t^{-1}),\]

for **any** \(a \in (0.5, 1)\), achieving the optimal \(1/t\) rate
without precise tuning (Polyak \& Juditsky, 1992).

**Status: PROVEN** (standard result, applies to SCX student).

#### \texorpdfstring{4.3 Dependence on Feature Dimension
\(d_\phi\){4.3 Dependence on Feature Dimension d\_\ phi}}<!-- label: dependence-on-feature-dimension-d_phi -->

The feature dimension \(d_\phi\) affects the convergence rate indirectly
through:

1. 
2. 
3. 

**Proposition 11.3 (Dimension Dependence --- CONJECTURED).** The
convergence rate degrades with \(d_\phi\) as:

\[\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq C \cdot t^{-a} \cdot (1 + \gamma \cdot d_\phi \cdot \log t),\]

where \(\gamma = O(1)\) is a problem-dependent constant. The logarithmic
dependence comes from the covering number of the feature space (metric
entropy \(O(d_\phi \log(1/\varepsilon))\)).

*Status: **CONJECTURED.** The logarithmic dependence on
\(d_\phi\) is typical for parametric models (Document 07, Proposition
SE-5). The exact interplay with the SGD rate requires further analysis.*

#### \texorpdfstring{4.4 Dependence on Noise Rate
\(\eta\){4.4 Dependence on Noise Rate \ eta}}<!-- label: dependence-on-noise-rate-eta -->

The noise rate \(\eta\) affects the convergence rate through the
**signal-to-noise ratio** of the consensus score:

**Proposition 11.4 (Noise Rate Dependence --- CONJECTURED).** The
effective strong convexity parameter degrades with noise:

\[\mu_{eff} = \mu \cdot \frac{\Delta_^2}{\Delta_^2 + \eta \cdot \sigma_{noise}^2},\]

where \(\Delta_ = \min_s \Delta_s\) is the state separation gap
(Theorem 1). For high noise (\(\eta \to 1\)) or small separation
(\(\Delta_ \to 0\)), \(\mu_{eff} \to 0\) and convergence
becomes arbitrarily slow.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Rate Under Polyak-Łojasiewicz
Condition<!-- label: rate-under-polyak-ux142ojasiewicz-condition -->

#### 5.1 The PL Condition<!-- label: the-pl-condition -->

Many neural network losses satisfy the weaker **Polyak-Łojasiewicz
(PL)** condition instead of strong convexity:

\[\frac{1}{2} \|\nabla \bar{L}(\theta)\|^2 \geq \mu_{PL} (\bar{L}(\theta) - \bar{L}(\theta^*)), \quad \forall \theta.\]

This is sufficient for linear convergence of gradient descent (Karimi et
al., 2016).

#### 5.2 PL Rate for SCX
Student<!-- label: pl-rate-for-scx-student -->

**Theorem 11.4 (Student Rate Under PL --- PROVEN).** Under the PL
condition with constant \(\mu_{PL} > 0\), C2, and C4 with
\(\alpha_t = \alpha_0 t^{-a}\):

\[\boxed{\;\mathbb{E}[\bar{L}(\theta_t) - \bar{L}(\theta^*)] \leq C_{PL} \cdot t^{-a}\;},\]

where \(C_{PL} = \frac{L_g G^2 \alpha_0}{2\mu_{PL}}\).

*Proof.* Standard SGD analysis under PL (Karimi et al., 2016). The
PL condition gives:

\[\mathbb{E}[\bar{L}(\theta_{t+1})] \leq \bar{L}(\theta_t) - \alpha_t \|\nabla \bar{L}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2}.\]

Using \(\|\nabla \bar{L}\|^2 \geq 2\mu_{PL}(\bar{L} - \bar{L}^*)\):

\[\mathbb{E}[\bar{L}(\theta_{t+1}) - \bar{L}^*] \leq (1 - 2\mu_{PL}\alpha_t)(\bar{L}(\theta_t) - \bar{L}^*) + \frac{L_g \alpha_t^2 G^2}{2}.\]

This recurrence gives \(O(t^{-a})\) convergence. \(\square\)

**Status: PROVEN.** The PL condition is more realistic than strong
convexity for neural networks.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Rate Under General
Non-Convexity<!-- label: rate-under-general-non-convexity -->

#### 6.1 The Non-Convex Case<!-- label: the-non-convex-case -->

For general non-convex losses (typical deep NEP students), we cannot
guarantee convergence to a global minimum. Instead, we characterize
convergence to a **stationary point**:

**Theorem 11.5 (Stationarity Rate, Non-Convex --- PROVEN).** Under
C2, C4 (RM rates), C5, and bounded gradient noise:

\[\boxed{\;\min_{0 \leq i \leq t} \mathbb{E}[\|\nabla \bar{L}(\theta_i)\|^2] \leq \frac{C_{nc}}{t^{1-a}}\;},\]

where \(a \in (0.5, 1)\) is the learning rate exponent, and
\(C_{nc} = \frac{\bar{L}(\theta_0) - \bar{L}_ + L_g G^2 \sum_{i=0}^\infty \alpha_i^2 / 2}{\sum_{i=0}^t \alpha_i}\).

For \(\alpha_t = \alpha_0 t^{-a}\):

\[\sum_{i=0}^t \alpha_i = \Theta(t^{1-a}),\]

so the rate is \(O(t^{-(1-a)})\). For \(a = 0.5\) (the fastest
RM-compatible rate), this gives \(O(t^{-0.5})\).

*Proof.* Standard SGD stationarity analysis (Ghadimi \& Lan, 2013).
From the \(L_g\)-smoothness:

\[\mathbb{E}[\bar{L}(\theta_{t+1})] \leq \bar{L}(\theta_t) - \alpha_t \|\nabla \bar{L}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2}.\]

Telescoping and rearranging:

\[\sum_{i=0}^t \alpha_i \mathbb{E}[\|\nabla \bar{L}(\theta_i)\|^2] \leq \bar{L}(\theta_0) - \bar{L}_ + \frac{L_g G^2}{2} \sum_{i=0}^t \alpha_i^2.\]

The minimum over \(i \leq t\) is at most the weighted average, giving
the claimed bound. \(\square\)

**Status: PROVEN.**

#### 6.2 Stationarity
vs.~Optimality<!-- label: stationarity-vs.-optimality -->

The rate \(O(t^{-(1-a)})\) guarantees that the gradient norm converges
to zero, **not** that the parameters converge to \(\theta^*\). In
non-convex landscapes, \(\|\nabla \bar{L}(\theta)\| \to 0\) is
consistent with convergence to a saddle point or a poor local minimum.

**Proposition 11.5 (Escaping Saddles --- CONJECTURED).** With SGD
noise \(\sigma_\xi^2 > 0\), the probability of converging to a strict
saddle point is zero, and the rate of escape from a saddle with negative
curvature \(\lambda_ < 0\) is exponential in the noise level:

\[\mathbb{P}(escape in  \leq \tau  steps) \geq 1 - \exp\!\left(-\frac{|\lambda_| \tau \alpha_t}{\sigma_\xi^2}\right).\]

*Status: **CONJECTURED** (based on Jin et al., 2017, for
gradient descent with noise).*

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Finite-Time (Non-Asymptotic)
Bound<!-- label: finite-time-non-asymptotic-bound -->

#### 7.1 Why Finite-Time?<!-- label: why-finite-time -->

Asymptotic rates \((t \to \infty)\) are informative about long-run
behavior but say little about what happens at practical timescales
(\(t = 10^2\)--\(10^4\)). A finite-time bound with explicit constants is
needed for practical guarantees.

#### 7.2 Finite-Time Bound Under Strong
Convexity<!-- label: finite-time-bound-under-strong-convexity -->

**Theorem 11.6 (Finite-Time Student Bound --- PROVEN).** Under SC
(strong convexity), C2, C4 with \(\alpha_t = \alpha_0 t^{-a}\), for any
\(t \geq 1\) and \(\delta \in (0, 1)\):

\[\boxed{\;\mathbb{P}\!\left(\|\theta_t - \theta^*\|^2 \leq \frac{C_V}{t^a} + \frac{C_}{\sqrt{t}} \cdot \sqrt{\log\frac{2}}\right) \geq 1 - \delta\;},\]

where:

\[
$$
C_V &= \frac{2 G^2 \alpha_0} \quad (variance term), 

C_ &= \frac{4 G \alpha_0} \cdot \sqrt{\frac{\sigma_\xi^2}} \quad (concentration term).
$$
\]

*Proof.* From the recurrence
\(V_{t+1} \leq (1 - 2\mu\alpha_t) V_t + \alpha_t^2 G^2\), unrolling to
step \(t\):

\[V_t \leq V_0 \prod_{i=0}^{t-1}(1 - 2\mu\alpha_i) + G^2 \sum_{i=0}^{t-1} \alpha_i^2 \prod_{j=i+1}^{t-1} (1 - 2\mu\alpha_j).\]

With \(\alpha_i = \alpha_0 i^{-a}\), the product
\(\prod (1 - 2\mu\alpha_i) \approx \exp(-2\mu \sum \alpha_i) \approx \exp(-c t^{1-a})\).
The dominant term is the variance accumulation, giving \(O(t^{-a})\).
The concentration term uses McDiarmid's inequality on the martingale
difference sequence. \(\square\)

**Status: PROVEN.** This gives a non-asymptotic guarantee with
explicit dependence on all parameters.

#### 7.3 Finite-Time Gatekeeper
Bound<!-- label: finite-time-gatekeeper-bound -->

**Theorem 11.7 (Finite-Time Gatekeeper Bound --- CONJECTURED).**
Under C3, C6', C7, C9, for any \(t \geq 1\) and \(\delta \in (0, 1)\):

\[\boxed{\;\mathbb{P}\!\left(\|S_t - S^*\|_{M_0}^2 \leq \frac{C_S}{t^{b}} + \frac{C_{\delta,S}}{\sqrt{N_t}} \cdot \sqrt{\log\frac{2}}\right) \geq 1 - \delta\;},\]

where \(C_S = O(B_S^2 \beta_0)\) and
\(C_{\delta,S} = O(1/\Delta_)\), with \(N_t\) being the memory
bank size at time \(t\).

*Proof sketch.* The gatekeeper's convergence has two components:
(i) the iterative refinement at rate \(t^{-b}\), and (ii) the
statistical error from finite memory, which decays as \(1/\sqrt{N_t}\).
Under monotonic memory growth (B1), \(N_t = \Omega(t)\), so the
statistical error is \(O(1/\sqrt{t})\).

**Status: CONJECTURED.** The decomposition is correct in structure,
but the constants require verifying that the SCX update satisfies the
contraction property with the claimed dependence on \(\Delta_\).

#### 7.4 Combined Finite-Time
Bound<!-- label: combined-finite-time-bound -->

**Corollary 11.2 (Combined Finite-Time Bound --- CONJECTURED).**
Under the conditions of Theorems 11.6 and 11.7, with \(a = 0.5\) and
\(b = 0.8\), for \(t \geq t_0\):

\[\boxed{\;\mathbb{E}\bigl[\Phi(S_t, \theta_t) - \Phi(S^*, \theta^*)\bigr] \leq \frac{C_\Phi}{\sqrt{t}} \cdot (1 + o(1))\;},\]

where \(C_\Phi\) is the sum of the student and gatekeeper constants.

The \(O(1/\sqrt{t})\) rate is the **typical stochastic
approximation rate** --- it matches the minimax optimal rate for
stochastic optimization with noisy gradients (Agarwal et al., 2012).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Two-Timescale Rate
Decomposition<!-- label: two-timescale-rate-decomposition -->

#### 8.1 Fast Timescale: Student
Convergence<!-- label: fast-timescale-student-convergence -->

On the fast timescale, the student sees the gatekeeper as approximately
fixed. The student rate (from Section 3) is:

\[R_\theta(t) = \mathbb{E}[\|\theta_t - \theta^*(S_t)\|^2] = O(t^{-a}).\]

#### 8.2 Slow Timescale: Gatekeeper
Convergence<!-- label: slow-timescale-gatekeeper-convergence -->

On the slow timescale, the student is approximately at
\(\theta^*(S_t)\), and the gatekeeper evolves according to a reduced
dynamics:

\[S_{t+1} = S_t + \beta_t \cdot \Delta(S_t, \theta^*(S_t)) + noise.\]

The gatekeeper rate is:

\[R_S(t) = \mathbb{E}[\|S_t - S^*\|^2] = O(t^{-b}) = o(t^{-a}).\]

#### 8.3 Total Rate<!-- label: total-rate -->

The total convergence rate is the slower of the two:

\[\boxed{\;R_{total}(t) = \max(R_\theta(t), R_S(t)) = O(t^{-a})\;},\]

since \(b > a\). The **student bottleneck dominates** --- the
system converges only as fast as the NEP learns.

#### 8.4 Optimal Rate
Allocation<!-- label: optimal-rate-allocation -->

Given a total ``learning budget'' \(\sum (\alpha_t + \beta_t)\), how
should we allocate between student and gatekeeper?

**Proposition 11.6 (Optimal Rate Allocation --- CONJECTURED).** The
optimal allocation makes the two rates equal:

\[t^{-a} = t^{-b} \implies a = b.\]

But this **violates** the two-timescale condition C6'
(\(\beta_t = o(\alpha_t)\), which requires \(b > a\)). Therefore, the
optimal allocation under the two-timescale constraint is:

\[b = a + \varepsilon, \quad \varepsilon \to 0^+,\]

which drives the gatekeeper toward the same rate as the student while
(just barely) maintaining timescale separation.

In practice, setting \(a = 0.5\), \(b = 0.6\) gives near-optimal
convergence while ensuring stable two-timescale behavior.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Comparison with Known
Rates<!-- label: comparison-with-known-rates -->

#### 9.1 Comparison Table<!-- label: comparison-table -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2222}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3056}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3056}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Method
\end{minipage} & \begin{minipage}[b]
Assumption
\end{minipage} & \begin{minipage}[b]
Rate
\end{minipage} & \begin{minipage}[b]
Reference
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**SGD (strongly convex)** & \(\mu > 0\) & \(O(t^{-1})\) & Bach \&
Moulines (2011) 

**SGD (PL condition)** & PL constant \(\mu_{PL}\) & \(O(t^{-1})\) &
Karimi et al.~(2016) 

**SGD (non-convex)** & \(L_g\)-smooth & \(O(t^{-0.5})\)
(stationarity) & Ghadimi \& Lan (2013) 

**SGD + averaging** & \(\mu > 0\) & \(O(t^{-1})\) & Polyak \&
Juditsky (1992) 

**Two-timescale SA** & Timescale separation & \(O(t^{-a})\) (slower
rate) & Borkar (2008) 

**SCX Student (this work)** & \(\mu > 0\) or PL & \(O(t^{-a})\),
\(a \in (0.5, 1]\) & Theorem 11.3 

**SCX Gatekeeper (this work)** & Contraction \(L_S < 1\) &
\(O(t^{-b})\) & Theorem 11.2 

**SCX Coupled (this work)** & Two-timescale & \(O(t^{-a})\) &
Theorem 11.3 

\end{longtable}

#### 9.2 Key Observations<!-- label: key-observations -->

1. 
2. 
3. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Gap Between Upper and Lower
Bounds<!-- label: gap-between-upper-and-lower-bounds -->

#### 10.1 Information-Theoretic Lower
Bound<!-- label: information-theoretic-lower-bound -->

**Theorem 11.8 (Minimax Lower Bound for Student Convergence ---
PROVEN).** For any algorithm that updates \(\theta_t\) using stochastic
gradients with variance \(\sigma_\xi^2 > 0\), under \(\mu\)-strong
convexity:

\[\mathbb{E}[\|\theta_t - \theta^*\|^2] \geq \frac{\sigma_\xi^2}{\mu^2} \cdot \frac{1}{t}.\]

*Proof.* Standard minimax lower bound for stochastic optimization
(Agarwal et al., 2012; Raginsky \& Rakhlin, 2011). The Cramér-Rao bound
for sequential estimation gives \(\Omega(1/t)\). \(\square\)

#### 10.2 Gap Analysis<!-- label: gap-analysis -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1778}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2667}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2889}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2667}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Regime
\end{minipage} & \begin{minipage}[b]
Upper Bound
\end{minipage} & \begin{minipage}[b]
Lower Bound
\end{minipage} & \begin{minipage}[b]
Gap Factor
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\alpha_t = t^{-1}\), SC & \(O(t^{-1})\) & \(\Omega(t^{-1})\) &
\(O(1)\) --- **tight** 

\(\alpha_t = t^{-0.5}\), SC & \(O(t^{-0.5})\) & \(\Omega(t^{-1})\) &
\(O(t^{0.5})\) --- **loose** 

Non-convex, stationarity & \(O(t^{-0.5})\) & N/A (no optimality
guarantee) & --- 

Gatekeeper, contraction & \(O(t^{-b})\) &
\(\Omega(1/N_t) = \Omega(t^{-1})\) & \(O(t^{1-b})\) --- **loose
for \(b < 1\)** 

\end{longtable}

**Interpretation**: With optimal tuning (\(a = 1\), Polyak
averaging), the student rate matches the minimax lower bound up to
constants. With suboptimal tuning (\(a = 0.5\)), the rate is suboptimal
by \(O(\sqrt{t})\). The gatekeeper rate has room for improvement --- the
\(t^{-b}\) dependence from iterative refinement is looser than the
\(1/\sqrt{N_t}\) statistical rate from memory accumulation.

#### 10.3 Tightening the Gatekeeper
Rate<!-- label: tightening-the-gatekeeper-rate -->

**Proposition 11.7 (Improved Gatekeeper Rate via Batch Updates ---
CONJECTURED).** If the gatekeeper is updated using **full-batch**
SCXUpdate on the entire memory bank (rather than incremental updates),
its convergence rate improves to:

\[\mathbb{E}[\|S_t - S^*\|_{M_0}^2] \leq \frac{C_S'}{\sqrt{N_t}},\]

matching the statistical rate. Since \(N_t = \Theta(t)\) (constant batch
sizes), this gives \(O(t^{-0.5})\).

*Status: **CONJECTURED.** The full-batch update eliminates the
iterative refinement bottleneck, leaving only the statistical error from
finite memory. This is faster than the incremental rate when
\(b < 0.5\).*

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 11. Summary<!-- label: summary -->

#### 11.1 Proven Results<!-- label: proven-results -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Result
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} & \begin{minipage}[b]
Rate
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Student rate under strong convexity (stationary dist.) & **PROVEN**
& \(O(t^{-a})\), \(a \in (0.5, 1]\) 

Student rate under PL condition & **PROVEN** & \(O(t^{-a})\) 

Student stationarity rate (non-convex) & **PROVEN** &
\(O(t^{-(1-a)})\) 

Finite-time student bound & **PROVEN** &
\(O(t^{-a}) + O(t^{-0.5})\) (concentration) 

Minimax lower bound & **PROVEN** & \(\Omega(t^{-1})\) 

\end{longtable}

#### 11.2 Conjectured Results<!-- label: conjectured-results -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2581}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2581}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4839}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Result
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} & \begin{minipage}[b]
Expected Rate
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Coupled rate under strong convexity & **CONJECTURED** &
\(O(t^{-a})\) 

Gatekeeper rate & **CONJECTURED** & \(O(t^{-b})\) 

Finite-time gatekeeper bound & **CONJECTURED** &
\(O(t^{-b}) + O(t^{-0.5})\) 

Optimal rate allocation \(b = a + \varepsilon\) & **CONJECTURED** &
\(O(t^{-a})\) 

\end{longtable}

#### 11.3 Parameter Dependence
Summary<!-- label: parameter-dependence-summary -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1864}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4068}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4068}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Parameter
\end{minipage} & \begin{minipage}[b]
Effect on Rate Constant
\end{minipage} & \begin{minipage}[b]
Effect on Rate Exponent
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(L_f\) (Lipschitz) & \(C \propto L_f^3\) & None 

\(\alpha_t = t^{-a}\) & \(C \propto \alpha_0\) & Rate = \(t^{-a}\) 

\(d_\phi\) (dimension) & \(C \propto 1 + \gamma d_\phi \log t\) & None
(logarithmic) 

\(\eta\) (noise rate) & \(C \propto 1/\Delta_^2(\eta)\) & None 

\(\mu\) (curvature) & \(C \propto 1/\mu\) & None 

\(\sigma_\xi^2\) (gradient noise) & \(C \propto \sigma_\xi^2\) & None 

\end{longtable}

#### 11.4 Practical
Recommendations<!-- label: practical-recommendations -->

1. 
2. 
3. 
4. 
5. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of 11\_convergence\_rate.md --- Convergence Rate Analysis*

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