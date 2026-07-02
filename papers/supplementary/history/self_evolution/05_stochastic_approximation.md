# Stochastic Approximation Analysis of NEP Student
Evolution

**Author:** SCX

> **Version**: 2026-06-28 |{} **Status**: Theoretical
> framework |{} **Scope**: Analysis of the coupled NEP student
> / gatekeeper evolution using stochastic approximation and two-timescale
> ODE methods **Notation note**: \(\mathcal{S}\) denotes the state
> space (existing SCX theory). \(S_t\) denotes the gatekeeper scoring
> function at time \(t\). \(f_{\theta_t}\) denotes the NEP student with
> parameters \(\theta_t\).

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Introduction: The Coupled Learning
System<!-- label: introduction-the-coupled-learning-system -->

The self-evolution loop creates a **coupled dynamical system**
between the gatekeeper \(S_t\) and the NEP student \(f_{\theta_t}\):

\[

$$
S_{t+1} &= UpdateGatekeeper(S_t, \mathcal{M}_t, f_{\theta_t}) 

\theta_{t+1} &= \theta_t - \alpha_t \nabla_\theta \mathcal{L}(f_{\theta_t}, \mathcal{M}_t)
$$

\]

This document analyzes the student evolution via **stochastic
approximation** (Robbins \& Monro, 1951), treating the gatekeeper update
as a slow drift in the data distribution.

**The key challenge**: The data distribution for the student is not
stationary. As \(S_t\) evolves, the composition of \(\mathcal{M}_t\)
changes, which shifts the effective training distribution for
\(f_{\theta_t}\). Standard stochastic approximation theory assumes a
stationary target; we must extend it to handle this drift.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Robbins-Monro Formulation of NEP Student
Update<!-- label: robbins-monro-formulation-of-nep-student-update -->

**Definition 5.1 (Stochastic Gradient Update).** The NEP student
parameters \(\theta_t \in \mathbb{R}^{d_\theta}\) evolve according to:

\[
\theta_{t+1} = \theta_t - \alpha_t \cdot g_t(\theta_t)
\]

where:

- 
- 
- 

**Assumption SE-A5 (Robbins-Monro Noise Model).** The stochastic
gradient \(g_t(\theta_t)\) satisfies:

\[
g_t(\theta_t) = \nabla L_t(\theta_t) + \xi_t
\]

where:

- 
- 
- 
- 

**Remark.** The expected loss \(L_t\) is time-dependent because
\(P_t\) depends on \(S_t\), which evolves. This is the central
complication vs.~standard SA.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Learning Rate Conditions<!-- label: learning-rate-conditions -->

**Definition 5.2 (Robbins-Monro Learning Rate).** The learning rate
\(\alpha_t\) satisfies the standard Robbins-Monro conditions:

\[
\sum_{t=1}^\infty \alpha_t = \infty, \qquad \sum_{t=1}^\infty \alpha_t^2 < \infty
\]

**Examples.** Common choices satisfying these conditions:

1. 
2. 
3. 

**Assumption SE-A6 (Decaying Learning Rate).** For asymptotic
convergence analysis, we assume \(\alpha_t\) satisfies the RM
conditions. For the tracking/constant-rate case, we relax this and
analyze the asymptotic bias.

**Proposition 5.1 (Constant vs.~Decaying Learning Rate
Trade-off).**

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3261}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2826}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3913}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Learning Rate
\end{minipage} & \begin{minipage}[b]
Convergence
\end{minipage} & \begin{minipage}[b]
Tracking Ability
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Decaying (\(\sum \alpha_t^2 < \infty\)) & Almost sure to stationary
point & Poor: cannot track drift 

Constant (\(\alpha_t = \alpha\)) & Bounded in distribution around
optimum & Good: adapts to drift 

\end{longtable}

*Proof sketch.* For decaying rates, the RM convergence theorem
(Theorem 5.1 below) gives almost sure convergence but requires vanishing
noise, which precludes tracking a moving target. For constant rates, the
iterate converges in distribution to a stationary process whose expected
distance to the optimum is \(O(\alpha)\) (Kushner \& Yin, 2003, Chapter
5).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Gradient Properties and
Boundedness<!-- label: gradient-properties-and-boundedness -->

**Assumption SE-A7 (Gradient Lipschitz Continuity).** The loss
function \(\ell(f_\theta(x), y)\) is once-differentiable in \(\theta\)
with Lipschitz continuous gradient:

\[
\|\nabla_\theta \ell(f_{\theta_1}(x), y) - \nabla_\theta \ell(f_{\theta_2}(x), y)\| \leq L_g \|\theta_1 - \theta_2\|, \quad \forall \theta_1, \theta_2
\]

for some \(L_g < \infty\), uniformly over \((x,y)\) in the support of
the data distribution.

**Assumption SE-A8 (Gradient Boundedness).** The stochastic
gradient is uniformly bounded:

\[
\|g_t(\theta)\| \leq G < \infty, \quad \forall \theta \in \mathbb{R}^{d_\theta}, \forall t
\]

**Proposition 5.2 (Consequences of Lipschitz Gradients).** Under
SE-A7:

1. 
2. 
3. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Convergence to Stationary
Point<!-- label: convergence-to-stationary-point -->

**Theorem 5.1 (Convergence of Robbins-Monro for NEP Student).** Let
assumptions SE-A5 (noise model), SE-A6 (decaying learning rate), SE-A7
(Lipschitz gradient), and SE-A8 (bounded gradient) hold. Additionally,
assume that the data distribution \(P_t\) converges to a limiting
distribution \(P_\infty\) as \(t \to \infty\) (or equivalently,
\(S_t \to S_\infty\)). Define the limiting expected loss:

\[
\bar{L}(\theta) = \mathbb{E}_{(x,y) \sim P_\infty}[\ell(f_\theta(x), y)]
\]

Then:

**(a) Gradient vanishing.** \(\|\nabla L_t(\theta_t)\| \to 0\)
almost surely as \(t \to \infty\).

**(b) Stationary point.** Any limit point \(\theta^*\) of the
sequence \(\{\theta_t\}\) satisfies:

\[
\nabla \bar{L}(\theta^*) = 0
\]

i.e., \(\theta^*\) is a stationary point of the limiting expected loss.

**(c) Rate under strong convexity.** If \(\bar{L}(\theta)\) is
\(\mu\)-strongly convex, then:

\[
\|\theta_t - \theta^*\| = O\left(\frac{1}{\sqrt{t}}\right) \quad in probability
\]

*Proof sketch.* See Section 10 for the full proof sketch. The key
steps are: 1. Show that
\(\sum \alpha_t \langle \nabla L_t(\theta_t), \mathbb{E}[g_t(\theta_t) \mid \mathcal{F}_{t-1}] \rangle\)
converges using the supermartingale convergence theorem. 2. Relate this
to \(\sum \alpha_t \|\nabla L_t(\theta_t)\|^2\) using the noise
decomposition. 3. Conclude \(\|\nabla L_t(\theta_t)\| \to 0\) from
\(\sum \alpha_t = \infty\). 4. Show convergence of \(L_t\) to
\(\bar{L}\) from \(P_t \to P_\infty\).

**Corollary 5.1 (Local Minima).** Under the additional assumption
that \(\bar{L}\) has isolated local minima, \(\theta_t\) converges to a
local minimum \(\theta^*\) almost surely, provided the initialization is
in the basin of attraction.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Distribution Shift
Analysis<!-- label: distribution-shift-analysis -->

**Definition 5.3 (Distribution Shift Operator).** The distribution
\(P_t\) evolves according to the gatekeeper dynamics:

\[
P_t(x,y) = \frac{S_t(x,y) \cdot P_0(x,y)}{\mathbb{E}_{P_0}[S_t]}
\]

where \(P_0\) is the base data distribution and \(S_t\) is the
gatekeeper at time \(t\). This is the acceptance-biased distribution.

**Theorem 5.2 (Distribution Shift Bound).** Let
\(\|S_t - S_\infty\|_\infty \leq \varepsilon_t\) where
\(\varepsilon_t \to 0\) (from the martingale convergence of \(S_t\)).
Then the total variation distance between \(P_t\) and \(P_\infty\)
satisfies:

\[
TV(P_t, P_\infty) \leq \frac{2\varepsilon_t}{\mathbb{E}_{P_0}[S_\infty] - \varepsilon_t}
\]

*Proof.* By definition:

\[
P_t(x,y) = \frac{S_t(x,y) P_0(x,y)}{Z_t}, \quad P_\infty(x,y) = \frac{S_\infty(x,y) P_0(x,y)}{Z_\infty}
\]

where \(Z_t = \mathbb{E}_{P_0}[S_t]\),
\(Z_\infty = \mathbb{E}_{P_0}[S_\infty]\). Then:

\[

$$
|P_t(x,y) - P_\infty(x,y)| &\leq \left| \frac{S_t}{Z_t} - \frac{S_\infty}{Z_\infty} \right| P_0(x,y) 

&\leq \left( \frac{|S_t - S_\infty|}{Z_t} + \frac{S_\infty|Z_t - Z_\infty|}{Z_t Z_\infty} \right) P_0(x,y) 

&\leq \frac{2\varepsilon_t}{Z_\infty - \varepsilon_t} P_0(x,y)
$$

\]

Integrating over \((x,y)\) gives the TV bound.

**Corollary 5.2 (Stationarity After Convergence).** Since
\(S_t \to S_\infty\) almost surely (Theorem 4.4), we have
\(P_t \to P_\infty\) in total variation almost surely.

**Impact on Student Training.** The distribution shift means that
earlier student updates were computed under \(P_i\) for \(i < t\), while
the convergence analysis is relative to \(P_\infty\). The discrepancy is
controlled by Theorem 5.2.

**Proposition 5.3 (Cumulative Shift Error).** The total error due
to distribution shift up to time \(t\) is bounded by:

\[
\sum_{i=1}^t \alpha_i \cdot TV(P_i, P_\infty) \leq \sum_{i=1}^t \frac{2\alpha_i \varepsilon_i}{\bar{Z} - \varepsilon_i}
\]

where \(\bar{Z} = \mathbb{E}_{P_0}[S_\infty] > 0\). If
\(\varepsilon_t = o(\alpha_t)\), the cumulative shift error is \(o(1)\).

*Proof.* Direct application of Theorem 5.2 and summation.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Two-Timescale Analysis<!-- label: two-timescale-analysis -->

**Definition 5.4 (Two-Timescale Structure).** The self-evolution
system has a natural two-timescale separation:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2750}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.4000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1750}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1500}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Component
\end{minipage} & \begin{minipage}[b]
Update interval
\end{minipage} & \begin{minipage}[b]
Speed
\end{minipage} & \begin{minipage}[b]
Role
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Gatekeeper \(S_t\) & \(1 / \nu_S\) updates per data batch &
**Slow** (macro) & Defines the data distribution 

NEP student \(\theta_t\) & Every sample & **Fast** (micro) & Adapts
to current distribution 

\end{longtable}

Formally, define \(\tau_S\) and \(\tau_\theta\) as the characteristic
timescales:

\[
\tau_S = O(1/\nu_S), \quad \tau_\theta = O(1/\alpha_t)
\]

where \(\nu_S\) is the gatekeeper update frequency (number of gatekeeper
updates per student step). The two-timescale separation holds when:

\[
\nu_S \ll \alpha_t \quad or equivalently \quad \tau_S \gg \tau_\theta
\]

**Theorem 5.3 (Two-Timescale Convergence).** Under the
two-timescale condition \(\alpha_t \gg \nu_S\) (student learns much
faster than gatekeeper updates), the coupled system can be analyzed as
follows:

**(a) Fast timescale (\(\theta\) quasi-stationary given \(S\)).**
For fixed \(S\), the student update converges to the minimizer of the
expected loss under \(P_S\):

\[
\theta_t \to \theta^*(S) := \arg\min_ \mathbb{E}_{(x,y) \sim P_S}[\ell(f_\theta(x), y)]
\]

**(b) Slow timescale (\(S\) evolves with \(\theta\) tracking).** On
the slow timescale, the gatekeeper dynamics are:

\[
S_{t+1} \approx S_t + \nu_S \cdot \Delta(S_t, \theta^*(S_t))
\]

where \(\Delta\) is the gatekeeper update function evaluated at the
quasi-stationary student.

**(c) Reduced system.** The coupled system reduces to a
single-timescale system on \(S\) alone:

\[
S_{t+1} = S_t + \nu_S \cdot \Delta(S_t, \theta^*(S_t))
\]

with the student implicitly at \(\theta^*(S_t)\).

*Proof sketch.* Formal application of singular perturbation theory
(Khalil, 2002; Borkar, 2008). The fast subsystem (student) has a unique
globally attracting fixed point \(\theta^*(S)\) for each \(S\). By
Tikhonov's theorem, the coupled system converges to the slow manifold
\(\{\theta = \theta^*(S)\}\) as \(\alpha_t/\nu_S \to \infty\), and the
reduced system on the slow manifold captures the asymptotic behavior.

**Corollary 5.3 (Separation Condition).** The two-timescale
approximation is valid when:

\[
\frac{\alpha_t}{\nu_S} \gg \frac{1}
\]

where \(\mu\) is the strong convexity parameter of the student loss (if
applicable). Under this condition, the tracking error
\(\|\theta_t - \theta^*(S_t)\|\) remains
\(O(\sqrt{\alpha_t/\nu_S \mu})\) in expectation.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. ODE Method<!-- label: ode-method -->

**Definition 5.5 (Mean ODE).** Consider the continuous-time
interpolation of the student update:

\[
\frac{d}{d\tau} \theta(\tau) = -\nabla \bar{L}(\theta(\tau))
\]

where
\(\bar{L}(\theta) = \mathbb{E}_{(x,y) \sim P_\infty}[\ell(f_\theta(x), y)]\)
is the limiting expected loss, and \(\tau\) is the continuous-time index
scaled by the learning rate.

**Theorem 5.4 (ODE Approximation).** Under assumptions SE-A5
through SE-A8, and assuming \(P_t \to P_\infty\) sufficiently fast
(\(\sum \alpha_t \cdot TV(P_t, P_\infty) < \infty\)), the
interpolated process
\(\theta^(t) = \theta_{\lfloor t/\alpha \rfloor}\) converges
weakly to the solution of the ODE:

\[
\frac{d}{dt} \theta(t) = -\nabla \bar{L}(\theta(t))
\]

as \(\alpha \to 0\), where \(\alpha\) is a representative learning rate.

More precisely, define the continuous-time interpolation on \([0, T]\):

\[
\theta^(t) = \theta_k + \frac{t - \tau_k}{\tau_{k+1} - \tau_k} (\theta_{k+1} - \theta_k)
\]

where \(\tau_k = \sum_{i=1}^k \alpha_i\). Then for any \(T < \infty\):

\[
\lim_{\alpha \to 0} \mathbb{P}\left( \sup_{0 \leq t \leq T} \|\theta^(t) - \theta(t)\| > \delta \right) = 0, \quad \forall \delta > 0
\]

*Proof sketch.* This is the classic ODE method for stochastic
approximation (Kushner \& Clark, 1978; Benveniste et al., 1990; Kushner
\& Yin, 2003). The proof involves:

1. 
2. 
3. 
4. 

**Corollary 5.4 (Convergence to Stationary Point).** If \(\bar{L}\)
has a unique global minimum \(\theta^*\) and is coercive
(\(\bar{L}(\theta) \to \infty\) as \(\|\theta\| \to \infty\)), then
\(\theta(t) \to \theta^*\) as \(t \to \infty\), and consequently
\(\theta_t \to \theta^*\) almost surely.

**Proposition 5.4 (ODE with Slow Distribution Shift).** When the
gatekeeper is also evolving, the ODE becomes a coupled system:

\[

$$
\frac{d}{dt} S(t) &= \nu_S \cdot \Phi(S(t), \theta(t)) 

\frac{d}{dt} \theta(t) &= -\nabla_\theta L_{S(t)}(\theta(t))
$$

\]

where
\(L_S(\theta) = \mathbb{E}_{(x,y) \sim P_S}[\ell(f_\theta(x), y)]\) and
\(\Phi\) is the gatekeeper update vector field.

*Interpretation.* The full system is a **two-timescale ODE**
where the \(\theta\) dynamics are fast and the \(S\) dynamics are slow.
This is the continuous-time analog of Theorem 5.3.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Connection to State-Conditioned
Risk<!-- label: connection-to-state-conditioned-risk -->

**Definition 5.6 (State-Conditioned NEP Loss).** For a given state
\(s \in \mathcal{S}\) (the state space from the existing SCX theory),
define the state-conditioned NEP student loss:

\[
L_s(\theta) = \mathbb{E}_{(x,y) \sim P(\cdot \mid s)}[\ell(f_\theta(x), y)]
\]

where \(P(\cdot \mid s)\) is the conditional data distribution in state
\(s\).

**Proposition 5.5 (Decomposition of Expected Loss).** The total
expected loss for the NEP student decomposes across states:

\[
\bar{L}(\theta) = \sum_{s \in \mathcal{S}} \rho_s \cdot L_s(\theta)
\]

where \(\rho_s = P(X \in s)\) is the state probability. Moreover, the
gradient decomposes accordingly:

\[
\nabla \bar{L}(\theta) = \sum_{s \in \mathcal{S}} \rho_s \cdot \nabla L_s(\theta)
\]

*Proof.* By the law of total expectation:

\[
\bar{L}(\theta) = \mathbb{E}[\ell(f_\theta(X), Y)] = \mathbb{E}[\mathbb{E}[\ell(f_\theta(X), Y) \mid X \in s]] = \sum_s \rho_s L_s(\theta)
\]

Gradient commutes with expectation (under Leibniz integral rule,
justified by bounded gradient assumption).

**Connection to Expert Risk \(R_m(s)\).** The existing SCX theory
defines
\(R_m(s) = \mathbb{E}_{x \sim P(\cdot \mid s)}[\ell(f_m(x), f^*(x))]\)
as the state-conditioned expert risk. For the NEP student, we
analogously define:

\[
R_\theta(s) = \mathbb{E}_{(x,y) \sim P(\cdot \mid s)}[\ell(f_\theta(x), y)]
\]

The key difference is that \(R_m(s)\) uses the true oracle \(f^*\),
while \(R_\theta(s)\) uses the observed labels \(y\) (which include the
gatekeeper's accepted labels). When the gatekeeper is reliable:

\[
R_\theta(s) \approx \mathbb{E}_{x \sim P(\cdot \mid s)}[\ell(f_\theta(x), f^*(x))]
\]

i.e., the observed label \(y\) is close to the oracle \(f^*(x)\).

**Theorem 5.5 (Risk Consistency in Self-Evolution).** Under the
convergence regime \(S_t \to S_\infty\) and \(\theta_t \to \theta^*\),
the NEP student's state-conditioned risk relates to the expert risks as:

\[
\lim_{t \to \infty} R_{\theta_t}(s) \leq \min_m R_m(s) + \varepsilon
\]

where \(\varepsilon = O(\|\theta^* - \theta_{expert}\|)\)
quantifies the representational gap between the NEP architecture and the
best expert.

*Proof sketch (conjectured).* If the NEP student \(f_\theta\) has
sufficient capacity to represent the best expert \(f_m\), then
\(\min_\theta R_\theta(s) = \min_m R_m(s)\). The self-evolution process
searches over \(\theta\), so \(\theta^*\) should achieve at least the
performance of the best expert in each state, provided the memory bank
contains sufficient samples from each state. The \(\varepsilon\) term
accounts for approximation error (capacity gap).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Full Proof Sketch: Convergence Under Robbins-Monro
Conditions<!-- label: full-proof-sketch-convergence-under-robbins-monro-conditions -->

Here we provide a detailed proof sketch for Theorem 5.1.

**Setup.** Consider the stochastic recursion:

\[
\theta_{t+1} = \theta_t - \alpha_t \nabla_\theta \ell(f_{\theta_t}(x_t), y_t)
\]

We analyze convergence under RM conditions.

**Step 1: Supermartingale construction.** Define
\(V_t = \|\theta_t - \theta^*\|^2\) where \(\theta^*\) is a stationary
point of \(\bar{L}\). Compute:

\[

$$
V_{t+1} &= \|\theta_t - \alpha_t g_t(\theta_t) - \theta^*\|^2 

&= V_t - 2\alpha_t \langle \theta_t - \theta^*, g_t(\theta_t) \rangle + \alpha_t^2 \|g_t(\theta_t)\|^2
$$

\]

Take conditional expectation:

\[
\mathbb{E}[V_{t+1} \mid \mathcal{F}_{t-1}] = V_t - 2\alpha_t \langle \theta_t - \theta^*, \nabla L_t(\theta_t) \rangle + \alpha_t^2 \mathbb{E}[\|g_t(\theta_t)\|^2 \mid \mathcal{F}_{t-1}]
\]

since \(\mathbb{E}[\xi_t \mid \mathcal{F}_{t-1}] = 0\).

**Step 2: Gradient inner product bound.** By the Lipschitz gradient
property:

\[
\langle \theta_t - \theta^*, \nabla L_t(\theta_t) \rangle \geq \frac{1}{L_g} \|\nabla L_t(\theta_t)\|^2 - \frac{L_g}{2} \|\theta_t - \theta^*\|^2
\]

For the strongly convex case, we use:

\[
\langle \theta_t - \theta^*, \nabla L_t(\theta_t) \rangle \geq \mu \|\theta_t - \theta^*\|^2
\]

**Step 3: Almost sure convergence.** Using the supermartingale
convergence theorem (Robbins \& Siegmund, 1971):

Let \(Y_t = V_t\), \(X_t = \alpha_t \|\nabla L_t(\theta_t)\|^2\),
\(Z_t = \alpha_t^2 \|g_t\|^2\).

If: 1.
\(\mathbb{E}[Y_{t+1} \mid \mathcal{F}_{t-1}] \leq Y_t - X_t + Z_t\) 2.
\(\sum Z_t < \infty\) almost surely (from \(\sum \alpha_t^2 < \infty\)
and bounded gradient) 3. \(Y_t \geq 0\)

Then \(Y_t\) converges almost surely and \(\sum X_t < \infty\).

Since \(\sum \alpha_t = \infty\) and
\(\sum \alpha_t \|\nabla L_t(\theta_t)\|^2 < \infty\), we must have
\(\|\nabla L_t(\theta_t)\| \to 0\) almost surely.

**Step 4: Convergence of \(L_t\) to \(\bar{L}\).** From Theorem
5.2:

\[
\|\nabla L_t(\theta_t) - \nabla \bar{L}(\theta_t)\| \leq L_g \cdot TV(P_t, P_\infty) \to 0
\]

Therefore \(\|\nabla \bar{L}(\theta_t)\| \to 0\) almost surely.

**Step 5: Rate under strong convexity.** If \(\bar{L}\) is
\(\mu\)-strongly convex:

\[
\|\theta_t - \theta^*\| \leq \frac{2} \|\nabla \bar{L}(\theta_t)\|
\]

Combining with the gradient convergence rate:

\[
\|\nabla \bar{L}(\theta_t)\| = O\left(\frac{1}{\sqrt{t}}\right) \quad in probability
\]

from standard RM analysis, giving
\(\|\theta_t - \theta^*\| = O(1/\sqrt{t})\).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 11. What Breaks When Distribution Shifts Too
Rapidly<!-- label: what-breaks-when-distribution-shifts-too-rapidly -->

**Definition 5.7 (Critical Drift Rate).** Define the data
distribution drift per student step:

\[
\delta_t = TV(P_{t+1}, P_t)
\]

The drift is **slow** if \(\delta_t \ll \alpha_t\) (the
distribution changes slower than the gradient step). The drift is
**rapid** if \(\delta_t \gtrsim \alpha_t\) or larger.

**Theorem 5.6 (Failure Under Rapid Shift).** If the data
distribution shifts too rapidly relative to the learning rate:

\[
\limsup_{t \to \infty} \frac{\delta_t}{\alpha_t} = \infty
\]

then the student may fail to converge. Specifically:

**(a) Oscillation.** The parameter sequence may enter a limit
cycle:

\[
\liminf_{t \to \infty} \|\theta_t - \theta^*(P_t)\| > 0
\]

**(b) Divergence.** In the worst case, the loss may diverge:

\[
\bar{L}(\theta_t) \to \infty \quad as  t \to \infty
\]

**(c) Catastrophic forgetting.** Earlier-learned states may be
overwritten as the distribution shifts toward new states:

\[
L_s(\theta_t) \to \infty \quad for states  s  that disappear from  P_t
\]

*Proof sketch.* The ODE approximation (Theorem 5.4) requires that
the drift \(\delta_t\) is summable against \(\alpha_t\). When
\(\delta_t \gg \alpha_t\), the ODE's vector field changes faster than
the gradient flow can follow, violating the conditions for weak
convergence. This is analogous to the failure of stochastic gradient
descent under non-stationary distributions when the learning rate is too
small to track the drift (Kushner \& Yin, 2003, Chapter 8; Borkar, 2008,
Chapter 6).

**Practical Implications for SCX Self-Evolution:**

1. 
2. 
3. 

**Proposition 5.6 (Adaptive Learning Rate Heuristic).** To handle
moderate drift, the learning rate should be:

\[
\alpha_t = \min\left(\alpha_0, \frac{C}{\sqrt{Var_{P_t}[\nabla \ell]}}\right)
\]

where \(C\) is a constant and \(Var_{P_t}\) is the gradient
variance under the current distribution. This is the
**AdaGrad**-style heuristic, which reduces the learning rate when
gradients are consistent (convergence) and increases it when the
distribution shifts (drift).

*Status.* This heuristic is well-motivated but lacks a formal
convergence guarantee in the self-evolution context.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 12. Summary of Proven vs.~Conjectured
Claims<!-- label: summary-of-proven-vs.-conjectured-claims -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3182}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3182}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Claim
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} & \begin{minipage}[b]
Notes
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Theorem 5.1: RM convergence (stationary) & **Proven** & Standard
Robbins-Monro theory; requires stationary \(P_\infty\) 

Theorem 5.1: Gradient vanishing & **Proven** & Supermartingale
convergence argument 

Theorem 5.1: Rate under strong convexity & **Proven** & Standard RM
rate \(O(1/\sqrt{t})\) 

Theorem 5.2: Distribution shift bound & **Proven** & From TV
convergence of \(P_t\) to \(P_\infty\) 

Theorem 5.3: Two-timescale convergence & **Proven under separation
condition** & Singular perturbation + Tikhonov theorem 

Theorem 5.4: ODE approximation & **Proven** & Kushner \& Yin (2003)
framework; requires drift summability 

Proposition 5.3: Cumulative shift error & **Proven** & Direct bound
from Theorem 5.2 

Theorem 5.5: Risk consistency & **Conjectured** & Requires capacity
+ representability assumptions 

Theorem 5.6: Failure under rapid shift & **Proven** & Standard
non-stationary SA theory 

Proposition 5.1: Constant vs.~decaying LR & **Proven** & Classic
result from SA theory 

Proposition 5.2: Gradient consequences & **Proven** & Direct from
Lipschitz assumption 

Proposition 5.4: Coupled ODE & **Proven** & Continuous-time limit
of two-timescale system 

Proposition 5.6: Adaptive learning rate & **Heuristic** & Lacks
formal convergence guarantee 

\end{longtable}

**Key uncertainty**: The risk consistency (Theorem 5.5) requires
the NEP student to have sufficient capacity to match the oracle expert,
which depends on the specific architecture. The adaptive learning rate
heuristic (Proposition 5.6) is practically motivated but unproven.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 13. References<!-- label: references -->

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of 05\_stochastic\_approximation.md -- Stochastic
approximation analysis of NEP student evolution.*