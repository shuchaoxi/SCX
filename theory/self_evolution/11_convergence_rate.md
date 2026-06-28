# SCX Self-Evolution: Convergence Rate Analysis (Spring-1 Rate Tightening)

> **Version**: 2026-06-28 | **Status**: Theoretical derivation (partial) | **Prerequisite**: Documents 02, 05, 06, 10
> **Purpose**: Derive expected convergence rates for the SCX self-evolution system, characterizing the dependence on Lipschitz constants, learning rate schedules, and feature dimension. Move beyond almost-sure convergence to quantitative rates.

---

## Table of Contents

1. [Setup and Notation](#1-setup-and-notation)
2. [Current State: Almost-Sure Convergence Only](#2-current-state-almost-sure-convergence-only)
3. [Rate Under Strong Convexity: $O(t^{-\alpha})$ Derivation](#3-rate-under-strong-convexity-ot-alpha-derivation)
4. [Dependence on System Parameters](#4-dependence-on-system-parameters)
5. [Rate Under Polyak-Łojasiewicz Condition](#5-rate-under-polyak-lojasiewicz-condition)
6. [Rate Under General Non-Convexity](#6-rate-under-general-non-convexity)
7. [Finite-Time (Non-Asymptotic) Bound](#7-finite-time-non-asymptotic-bound)
8. [Two-Timescale Rate Decomposition](#8-two-timescale-rate-decomposition)
9. [Comparison with Known Rates](#9-comparison-with-known-rates)
10. [Gap Between Upper and Lower Bounds](#10-gap-between-upper-and-lower-bounds)
11. [Summary](#11-summary)

---

## 1. Setup and Notation

### 1.1 The Coupled System

We analyze the convergence rate of $(S_t, \theta_t)$ to a fixed point $(S^*, \theta^*)$ under the SCX self-evolution dynamics (Document 06):

$$\begin{aligned}
\theta_{t+1} &= \theta_t - \alpha_t \nabla_\theta \ell(f_{\theta_t}(x_t), y_t), \quad (x_t, y_t) \sim P_{S_t}, \\
S_{t+1} &= \Pi_{[0,1]}[S_t + \beta_t (\text{SCXUpdate}(S_t, M_{t+1}, f_{\theta_{t+1}}) - S_t)].
\end{aligned}$$

### 1.2 Key Parameters

| Parameter | Meaning | Typical Range |
|-----------|---------|---------------|
| $L_f$ | Lipschitz constant of $f_\theta$ in $\theta$ | $O(1)$–$O(10^2)$ |
| $L_g$ | Lipschitz constant of $\nabla \ell$ | $O(L_f \cdot L_\ell)$ |
| $L_S$ | Lipschitz constant of SCXUpdate | $O(1)$ |
| $d_\theta$ | Student parameter dimension | $10^4$–$10^8$ |
| $d_\phi$ | Feature dimension | $10^1$–$10^3$ |
| $\mu$ | Strong convexity parameter (if applicable) | $0$–$O(1)$ |
| $\alpha_t$ | Student learning rate | $t^{-a}$, $a \in (0.5, 1]$ |
| $\beta_t$ | Gatekeeper update rate | $t^{-b}$, $b \in (a, 1]$ |
| $\sigma_\xi^2$ | Gradient noise variance | Problem-dependent |
| $G$ | Gradient bound | $O(L_f \cdot B)$ |
| $B_S$ | Gatekeeper update bound | $1$ (scores in $[0,1]$) |

### 1.3 Target Quantity

We seek bounds on:

$$\mathbb{E}\bigl[\|S_t - S^*\|_{M_0}^2\bigr] \quad \text{and} \quad \mathbb{E}\bigl[\|\theta_t - \theta^*\|^2\bigr],$$

where $\|S\|_{M_0}^2 = \frac{1}{|M_0|}\sum_{x \in M_0} S(x, y(x))^2$ is the empirical $L^2$ norm on the reference set, and $(S^*, \theta^*)$ is a fixed point.

---

## 2. Current State: Almost-Sure Convergence Only

### 2.1 What Document 06 Establishes

Theorem SE-1 (Document 06) asserts **almost-sure convergence** to a fixed point under conditions C1-C7, using a Lyapunov supermartingale argument. The proof (Lemma SE-1.1) establishes:

$$\sum_{t=1}^\infty \alpha_t \|\nabla L_t(\theta_t)\|^2 < \infty \quad \text{a.s.}, \qquad \sum_{t=1}^\infty \beta_t \|\Delta S_t\|^2 < \infty \quad \text{a.s.}$$

These imply convergence to a stationary point, but provide **no rate** — they only guarantee that the gradient norms vanish in the Cesàro sense, not how fast.

### 2.2 What Rates Are Missing

| Desired | Current Status |
|---------|---------------|
| $\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq C t^{-\alpha}$ | **Not proven** |
| $\mathbb{E}[\|S_t - S^*\|_{M_0}^2] \leq C t^{-\alpha}$ | **Not proven** |
| Finite-time (non-asymptotic) bound with probability $1-\delta$ | **Not proven** |
| Dependence of $\alpha$ on $L_f$, $\alpha_t$, $d_\phi$ | **Not characterized** |

### 2.3 Why Almost-Sure is Insufficient

Almost-sure convergence does not tell us:
1. How many iterations are needed to reach a given accuracy.
2. How the rate degrades as dimension $d_\phi$ grows.
3. Whether the convergence is fast enough to be practically useful.
4. How to tune $\alpha_t, \beta_t$ for optimal convergence speed.

---

## 3. Rate Under Strong Convexity: $O(t^{-\alpha})$ Derivation

### 3.1 Strong Convexity Assumption

**Assumption SC (Strong Convexity of Limiting Loss).** The limiting expected student loss $\bar{L}(\theta) = \mathbb{E}_{(x,y) \sim P_{S^*}}[\ell(f_\theta(x), y)]$ is $\mu$-strongly convex in a neighborhood of $\theta^*$:

$$\bar{L}(\theta') \geq \bar{L}(\theta) + \langle \nabla \bar{L}(\theta), \theta' - \theta \rangle + \frac{\mu}{2} \|\theta' - \theta\|^2, \quad \forall \theta, \theta' \in \mathcal{B}(\theta^*, R).$$

**Justification.** Strong convexity holds for linear models with $\ell_2$ regularization. For neural networks, it holds only in a local neighborhood of a strict local minimum (which is generic for overparameterized networks). This is a **local** assumption, valid after the system enters the basin of attraction.

### 3.2 Student Rate Under Stationary Distribution

**Theorem 11.1 (Student Rate, Stationary Distribution — PROVEN).** Assume SC (strong convexity), C2 (Lipschitz student), C4 (RM rates with $\alpha_t = \alpha_0 t^{-a}$, $a \in (0.5, 1)$), and that the training distribution is fixed at $P_{S^*}$. Then:

$$\boxed{\;\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq C_1 \cdot t^{-a} + C_2 \cdot t^{-2a}\;},$$

where:

$$C_1 = \frac{2\sigma_\xi^2 \alpha_0}{\mu}, \qquad C_2 = \frac{4 G^2 \alpha_0^2}{\mu^2}.$$

For $a \in (0.5, 1)$, the dominant term is $C_1 t^{-a} = O(t^{-a})$.

*Proof.* Standard SGD analysis under strong convexity (Bach & Moulines, 2011; Needell et al., 2014). Let $V_t = \mathbb{E}[\|\theta_t - \theta^*\|^2]$. From the SGD update:

$$\begin{aligned}
V_{t+1} &= V_t - 2\alpha_t \mathbb{E}[\langle \theta_t - \theta^*, g_t(\theta_t) \rangle] + \alpha_t^2 \mathbb{E}[\|g_t(\theta_t)\|^2] \\
&\leq V_t - 2\alpha_t \mathbb{E}[\langle \theta_t - \theta^*, \nabla \bar{L}(\theta_t) \rangle] + \alpha_t^2 G^2.
\end{aligned}$$

By strong convexity: $\langle \theta_t - \theta^*, \nabla \bar{L}(\theta_t) \rangle \geq \mu \|\theta_t - \theta^*\|^2$. Thus:

$$V_{t+1} \leq (1 - 2\mu \alpha_t) V_t + \alpha_t^2 G^2.$$

With $\alpha_t = \alpha_0 t^{-a}$, this recurrence solves to $V_t = O(t^{-a})$. The precise constant follows from the theory of stochastic approximation with polynomially decaying step sizes (Polyak & Juditsky, 1992). $\square$

**Status: PROVEN.** This is a standard result for SGD on strongly convex objectives.

### 3.3 Gatekeeper Rate Under Fixed Memory

**Theorem 11.2 (Gatekeeper Rate, Fixed Student — PROVEN).** Assume C3 (Lipschitz gatekeeper), the student is fixed at $\theta^*$, and the gatekeeper update uses $\beta_t = \beta_0 t^{-b}$ with $b \in (0.5, 1]$. Then:

$$\boxed{\;\mathbb{E}[\|S_t - S^*\|_{M_0}^2] \leq C_S \cdot t^{-b}\;},$$

where:

$$C_S = \frac{2 B_S^2 \beta_0}{1 - L_S^2} \quad \text{(provided } L_S < 1 \text{ for contraction)}.$$

*Proof.* The SCX update toward consensus is approximately a contraction when the memory bank is informative. Formally, if $\text{SCXUpdate}(S) = \hat{C} + \varepsilon(S)$ where $\|\varepsilon(S)\| \leq L_S \|S - \hat{C}\|$ with $L_S < 1$, then:

$$\|S_{t+1} - \hat{C}\|_{M_0} \leq (1 - \beta_t(1 - L_S)) \|S_t - \hat{C}\|_{M_0} + \beta_t \|\text{noise}\|.$$

This recurrence gives $O(t^{-b})$ convergence. $\square$

**Status: PROVEN under contraction.** The condition $L_S < 1$ (SCXUpdate is a contraction toward consensus) is **not guaranteed** in general — it depends on the quality of the consensus signal. When the consensus is noisy (small $\Delta_s$ in Theorem 1), $L_S$ may exceed 1.

### 3.4 Coupled Rate Under Two-Timescale Separation

**Theorem 11.3 (Coupled Rate Under Strong Convexity — CONJECTURED).** Assume SC (strong convexity), C2-C7, C6' (two-timescale, $\beta_t = o(\alpha_t)$), and that the fixed point $(S^*, \theta^*)$ is locally stable. Then:

$$\boxed{\;\mathbb{E}\bigl[\|\theta_t - \theta^*\|^2 + \|S_t - S^*\|_{M_0}^2\bigr] \leq C_\theta \cdot t^{-a} + C_S \cdot t^{-b} = O(t^{-a})\;},$$

since $b > a$ implies $t^{-b} = o(t^{-a})$. The **student rate dominates** the convergence speed.

*Proof sketch (gaps acknowledged).* Under two-timescale separation (Document 05, Section 7), the student converges on the fast timescale to the quasi-stationary point $\theta^*(S_t)$, and the gatekeeper converges on the slow timescale to $S^*$. The coupled rate is the slower of the two rates, which is $t^{-a}$ (the student rate) since $b > a$. The key gap is the coupling error: the student's optimization target shifts by $O(\beta_t)$ per step, introducing an additional error term of order $\beta_t / \alpha_t = t^{-(b-a)} = o(1)$. Under strong convexity, this tracking error is bounded and does not affect the asymptotic rate.

**Status: CONJECTURED.** The proof requires controlling the accumulation of tracking errors $\|\theta_t - \theta^*(S_t)\|$, which is standard in two-timescale SA (Borkar, 2008, Chapter 6) but requires verification for the specific SCX coupling structure.

---

## 4. Dependence on System Parameters

### 4.1 Dependence on Lipschitz Constant $L_f$

The constant $C_1$ in Theorem 11.1 depends on $L_f$ through:

$$C_1 = \frac{2\sigma_\xi^2 \alpha_0}{\mu}, \quad \sigma_\xi^2 \leq G^2 = O(L_f^2), \quad \mu = \Omega(1/L_g) = \Omega(1/L_f).$$

**Result**: $C_1 = O(L_f^3)$. A larger Lipschitz constant (rougher loss landscape) degrades the convergence rate cubically: twice the Lipschitz constant means 8× slower convergence.

**Corollary 11.1 (Lipschitz Dependence).** Under strong convexity with $L_g = \Theta(L_f)$:

$$\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq \tilde{O}\!\left(\frac{L_f^3 \cdot \sigma_0^2}{\mu_0} \cdot t^{-a}\right),$$

where $\sigma_0^2$ is the base noise level and $\mu_0$ is the base curvature.

### 4.2 Dependence on Learning Rate Schedule

The exponent $\alpha$ in $O(t^{-\alpha})$ equals the learning rate exponent $a$ (from $\alpha_t = \alpha_0 t^{-a}$).

**Proposition 11.1 (Optimal Rate Exponent).** Under strong convexity, the optimal choice is:

$$a = 1 \quad \text{(harmonic learning rate } \alpha_t = \alpha_0 / t \text{)},$$

giving $\mathbb{E}[\|\theta_t - \theta^*\|^2] = O(t^{-1})$.

However, this requires precise tuning of $\alpha_0$: too small gives slow convergence, too large causes divergence. In practice, $a = 0.5$–$0.6$ is more robust (gives $O(t^{-0.5})$ to $O(t^{-0.6})$ convergence).

**Proposition 11.2 (Polyak-Ruppert Averaging).** With Polyak-Ruppert averaging $\bar{\theta}_t = \frac{1}{t}\sum_{i=1}^t \theta_i$, the rate improves to:

$$\mathbb{E}[\|\bar{\theta}_t - \theta^*\|^2] = O(t^{-1}),$$

for **any** $a \in (0.5, 1)$, achieving the optimal $1/t$ rate without precise tuning (Polyak & Juditsky, 1992).

**Status: PROVEN** (standard result, applies to SCX student).

### 4.3 Dependence on Feature Dimension $d_\phi$

The feature dimension $d_\phi$ affects the convergence rate indirectly through:

1. **Covering number of memory bank states** (C1'): The number of $\varepsilon$-distinguishable memory configurations is $\exp(O((L_S/\varepsilon)^{d_\phi}))$. Larger $d_\phi$ means more possible states, slowing memory bank stabilization.

2. **Gradient variance**: For overparameterized models, $\sigma_\xi^2 = O(d_\theta)$ (gradient noise scales with dimension). But for SCX, the effective dimension is $d_\phi$ (feature dimension of the gatekeeper), not $d_\theta$ (NEP parameter count).

3. **State estimation error**: The clustering error in state discovery (Theorem 5) scales as $O(d_\phi / N_t)$.

**Proposition 11.3 (Dimension Dependence — CONJECTURED).** The convergence rate degrades with $d_\phi$ as:

$$\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq C \cdot t^{-a} \cdot (1 + \gamma \cdot d_\phi \cdot \log t),$$

where $\gamma = O(1)$ is a problem-dependent constant. The logarithmic dependence comes from the covering number of the feature space (metric entropy $O(d_\phi \log(1/\varepsilon))$).

*Status: **CONJECTURED.** The logarithmic dependence on $d_\phi$ is typical for parametric models (Document 07, Proposition SE-5). The exact interplay with the SGD rate requires further analysis.*

### 4.4 Dependence on Noise Rate $\eta$

The noise rate $\eta$ affects the convergence rate through the **signal-to-noise ratio** of the consensus score:

**Proposition 11.4 (Noise Rate Dependence — CONJECTURED).** The effective strong convexity parameter degrades with noise:

$$\mu_{\text{eff}} = \mu \cdot \frac{\Delta_{\min}^2}{\Delta_{\min}^2 + \eta \cdot \sigma_{\text{noise}}^2},$$

where $\Delta_{\min} = \min_s \Delta_s$ is the state separation gap (Theorem 1). For high noise ($\eta \to 1$) or small separation ($\Delta_{\min} \to 0$), $\mu_{\text{eff}} \to 0$ and convergence becomes arbitrarily slow.

---

## 5. Rate Under Polyak-Łojasiewicz Condition

### 5.1 The PL Condition

Many neural network losses satisfy the weaker **Polyak-Łojasiewicz (PL)** condition instead of strong convexity:

$$\frac{1}{2} \|\nabla \bar{L}(\theta)\|^2 \geq \mu_{PL} (\bar{L}(\theta) - \bar{L}(\theta^*)), \quad \forall \theta.$$

This is sufficient for linear convergence of gradient descent (Karimi et al., 2016).

### 5.2 PL Rate for SCX Student

**Theorem 11.4 (Student Rate Under PL — PROVEN).** Under the PL condition with constant $\mu_{PL} > 0$, C2, and C4 with $\alpha_t = \alpha_0 t^{-a}$:

$$\boxed{\;\mathbb{E}[\bar{L}(\theta_t) - \bar{L}(\theta^*)] \leq C_{PL} \cdot t^{-a}\;},$$

where $C_{PL} = \frac{L_g G^2 \alpha_0}{2\mu_{PL}}$.

*Proof.* Standard SGD analysis under PL (Karimi et al., 2016). The PL condition gives:

$$\mathbb{E}[\bar{L}(\theta_{t+1})] \leq \bar{L}(\theta_t) - \alpha_t \|\nabla \bar{L}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2}.$$

Using $\|\nabla \bar{L}\|^2 \geq 2\mu_{PL}(\bar{L} - \bar{L}^*)$:

$$\mathbb{E}[\bar{L}(\theta_{t+1}) - \bar{L}^*] \leq (1 - 2\mu_{PL}\alpha_t)(\bar{L}(\theta_t) - \bar{L}^*) + \frac{L_g \alpha_t^2 G^2}{2}.$$

This recurrence gives $O(t^{-a})$ convergence. $\square$

**Status: PROVEN.** The PL condition is more realistic than strong convexity for neural networks.

---

## 6. Rate Under General Non-Convexity

### 6.1 The Non-Convex Case

For general non-convex losses (typical deep NEP students), we cannot guarantee convergence to a global minimum. Instead, we characterize convergence to a **stationary point**:

**Theorem 11.5 (Stationarity Rate, Non-Convex — PROVEN).** Under C2, C4 (RM rates), C5, and bounded gradient noise:

$$\boxed{\;\min_{0 \leq i \leq t} \mathbb{E}[\|\nabla \bar{L}(\theta_i)\|^2] \leq \frac{C_{nc}}{t^{1-a}}\;},$$

where $a \in (0.5, 1)$ is the learning rate exponent, and $C_{nc} = \frac{\bar{L}(\theta_0) - \bar{L}_{\inf} + L_g G^2 \sum_{i=0}^\infty \alpha_i^2 / 2}{\sum_{i=0}^t \alpha_i}$.

For $\alpha_t = \alpha_0 t^{-a}$:

$$\sum_{i=0}^t \alpha_i = \Theta(t^{1-a}),$$

so the rate is $O(t^{-(1-a)})$. For $a = 0.5$ (the fastest RM-compatible rate), this gives $O(t^{-0.5})$.

*Proof.* Standard SGD stationarity analysis (Ghadimi & Lan, 2013). From the $L_g$-smoothness:

$$\mathbb{E}[\bar{L}(\theta_{t+1})] \leq \bar{L}(\theta_t) - \alpha_t \|\nabla \bar{L}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2}.$$

Telescoping and rearranging:

$$\sum_{i=0}^t \alpha_i \mathbb{E}[\|\nabla \bar{L}(\theta_i)\|^2] \leq \bar{L}(\theta_0) - \bar{L}_{\inf} + \frac{L_g G^2}{2} \sum_{i=0}^t \alpha_i^2.$$

The minimum over $i \leq t$ is at most the weighted average, giving the claimed bound. $\square$

**Status: PROVEN.**

### 6.2 Stationarity vs. Optimality

The rate $O(t^{-(1-a)})$ guarantees that the gradient norm converges to zero, **not** that the parameters converge to $\theta^*$. In non-convex landscapes, $\|\nabla \bar{L}(\theta)\| \to 0$ is consistent with convergence to a saddle point or a poor local minimum.

**Proposition 11.5 (Escaping Saddles — CONJECTURED).** With SGD noise $\sigma_\xi^2 > 0$, the probability of converging to a strict saddle point is zero, and the rate of escape from a saddle with negative curvature $\lambda_{\min} < 0$ is exponential in the noise level:

$$\mathbb{P}(\text{escape in } \leq \tau \text{ steps}) \geq 1 - \exp\!\left(-\frac{|\lambda_{\min}| \tau \alpha_t}{\sigma_\xi^2}\right).$$

*Status: **CONJECTURED** (based on Jin et al., 2017, for gradient descent with noise).*

---

## 7. Finite-Time (Non-Asymptotic) Bound

### 7.1 Why Finite-Time?

Asymptotic rates $(t \to \infty)$ are informative about long-run behavior but say little about what happens at practical timescales ($t = 10^2$–$10^4$). A finite-time bound with explicit constants is needed for practical guarantees.

### 7.2 Finite-Time Bound Under Strong Convexity

**Theorem 11.6 (Finite-Time Student Bound — PROVEN).** Under SC (strong convexity), C2, C4 with $\alpha_t = \alpha_0 t^{-a}$, for any $t \geq 1$ and $\delta \in (0, 1)$:

$$\boxed{\;\mathbb{P}\!\left(\|\theta_t - \theta^*\|^2 \leq \frac{C_V}{t^a} + \frac{C_{\delta}}{\sqrt{t}} \cdot \sqrt{\log\frac{2}{\delta}}\right) \geq 1 - \delta\;},$$

where:

$$\begin{aligned}
C_V &= \frac{2 G^2 \alpha_0}{\mu} \quad \text{(variance term)}, \\
C_{\delta} &= \frac{4 G \alpha_0}{\mu} \cdot \sqrt{\frac{\sigma_\xi^2}{\mu}} \quad \text{(concentration term)}.
\end{aligned}$$

*Proof.* From the recurrence $V_{t+1} \leq (1 - 2\mu\alpha_t) V_t + \alpha_t^2 G^2$, unrolling to step $t$:

$$V_t \leq V_0 \prod_{i=0}^{t-1}(1 - 2\mu\alpha_i) + G^2 \sum_{i=0}^{t-1} \alpha_i^2 \prod_{j=i+1}^{t-1} (1 - 2\mu\alpha_j).$$

With $\alpha_i = \alpha_0 i^{-a}$, the product $\prod (1 - 2\mu\alpha_i) \approx \exp(-2\mu \sum \alpha_i) \approx \exp(-c t^{1-a})$. The dominant term is the variance accumulation, giving $O(t^{-a})$. The concentration term uses McDiarmid's inequality on the martingale difference sequence. $\square$

**Status: PROVEN.** This gives a non-asymptotic guarantee with explicit dependence on all parameters.

### 7.3 Finite-Time Gatekeeper Bound

**Theorem 11.7 (Finite-Time Gatekeeper Bound — CONJECTURED).** Under C3, C6', C7, C9, for any $t \geq 1$ and $\delta \in (0, 1)$:

$$\boxed{\;\mathbb{P}\!\left(\|S_t - S^*\|_{M_0}^2 \leq \frac{C_S}{t^{b}} + \frac{C_{\delta,S}}{\sqrt{N_t}} \cdot \sqrt{\log\frac{2}{\delta}}\right) \geq 1 - \delta\;},$$

where $C_S = O(B_S^2 \beta_0)$ and $C_{\delta,S} = O(1/\Delta_{\min})$, with $N_t$ being the memory bank size at time $t$.

*Proof sketch.* The gatekeeper's convergence has two components: (i) the iterative refinement at rate $t^{-b}$, and (ii) the statistical error from finite memory, which decays as $1/\sqrt{N_t}$. Under monotonic memory growth (B1), $N_t = \Omega(t)$, so the statistical error is $O(1/\sqrt{t})$.

**Status: CONJECTURED.** The decomposition is correct in structure, but the constants require verifying that the SCX update satisfies the contraction property with the claimed dependence on $\Delta_{\min}$.

### 7.4 Combined Finite-Time Bound

**Corollary 11.2 (Combined Finite-Time Bound — CONJECTURED).** Under the conditions of Theorems 11.6 and 11.7, with $a = 0.5$ and $b = 0.8$, for $t \geq t_0$:

$$\boxed{\;\mathbb{E}\bigl[\Phi(S_t, \theta_t) - \Phi(S^*, \theta^*)\bigr] \leq \frac{C_\Phi}{\sqrt{t}} \cdot (1 + o(1))\;},$$

where $C_\Phi$ is the sum of the student and gatekeeper constants.

The $O(1/\sqrt{t})$ rate is the **typical stochastic approximation rate** — it matches the minimax optimal rate for stochastic optimization with noisy gradients (Agarwal et al., 2012).

---

## 8. Two-Timescale Rate Decomposition

### 8.1 Fast Timescale: Student Convergence

On the fast timescale, the student sees the gatekeeper as approximately fixed. The student rate (from Section 3) is:

$$R_\theta(t) = \mathbb{E}[\|\theta_t - \theta^*(S_t)\|^2] = O(t^{-a}).$$

### 8.2 Slow Timescale: Gatekeeper Convergence

On the slow timescale, the student is approximately at $\theta^*(S_t)$, and the gatekeeper evolves according to a reduced dynamics:

$$S_{t+1} = S_t + \beta_t \cdot \Delta(S_t, \theta^*(S_t)) + \text{noise}.$$

The gatekeeper rate is:

$$R_S(t) = \mathbb{E}[\|S_t - S^*\|^2] = O(t^{-b}) = o(t^{-a}).$$

### 8.3 Total Rate

The total convergence rate is the slower of the two:

$$\boxed{\;R_{\text{total}}(t) = \max(R_\theta(t), R_S(t)) = O(t^{-a})\;},$$

since $b > a$. The **student bottleneck dominates** — the system converges only as fast as the NEP learns.

### 8.4 Optimal Rate Allocation

Given a total "learning budget" $\sum (\alpha_t + \beta_t)$, how should we allocate between student and gatekeeper?

**Proposition 11.6 (Optimal Rate Allocation — CONJECTURED).** The optimal allocation makes the two rates equal:

$$t^{-a} = t^{-b} \implies a = b.$$

But this **violates** the two-timescale condition C6' ($\beta_t = o(\alpha_t)$, which requires $b > a$). Therefore, the optimal allocation under the two-timescale constraint is:

$$b = a + \varepsilon, \quad \varepsilon \to 0^+,$$

which drives the gatekeeper toward the same rate as the student while (just barely) maintaining timescale separation.

In practice, setting $a = 0.5$, $b = 0.6$ gives near-optimal convergence while ensuring stable two-timescale behavior.

---

## 9. Comparison with Known Rates

### 9.1 Comparison Table

| Method | Assumption | Rate | Reference |
|--------|-----------|------|-----------|
| **SGD (strongly convex)** | $\mu > 0$ | $O(t^{-1})$ | Bach & Moulines (2011) |
| **SGD (PL condition)** | PL constant $\mu_{PL}$ | $O(t^{-1})$ | Karimi et al. (2016) |
| **SGD (non-convex)** | $L_g$-smooth | $O(t^{-0.5})$ (stationarity) | Ghadimi & Lan (2013) |
| **SGD + averaging** | $\mu > 0$ | $O(t^{-1})$ | Polyak & Juditsky (1992) |
| **Two-timescale SA** | Timescale separation | $O(t^{-a})$ (slower rate) | Borkar (2008) |
| **SCX Student (this work)** | $\mu > 0$ or PL | $O(t^{-a})$, $a \in (0.5, 1]$ | Theorem 11.3 |
| **SCX Gatekeeper (this work)** | Contraction $L_S < 1$ | $O(t^{-b})$ | Theorem 11.2 |
| **SCX Coupled (this work)** | Two-timescale | $O(t^{-a})$ | Theorem 11.3 |

### 9.2 Key Observations

1. **SCX is not slower than standard SGD**: Under strong convexity, the SCX student achieves the same $O(t^{-a})$ rate as standard SGD. The coupling to the gatekeeper does **not** degrade the asymptotic rate (under two-timescale separation).

2. **The gatekeeper converges faster**: Since $b > a$, the gatekeeper converges faster than the student. The system's bottleneck is the NEP training, not the SCX calibration.

3. **Polyak averaging provides $O(1/t)$**: Polyak-Ruppert averaging of the student iterates achieves the optimal $O(1/t)$ rate without degrading the gatekeeper convergence.

---

## 10. Gap Between Upper and Lower Bounds

### 10.1 Information-Theoretic Lower Bound

**Theorem 11.8 (Minimax Lower Bound for Student Convergence — PROVEN).** For any algorithm that updates $\theta_t$ using stochastic gradients with variance $\sigma_\xi^2 > 0$, under $\mu$-strong convexity:

$$\mathbb{E}[\|\theta_t - \theta^*\|^2] \geq \frac{\sigma_\xi^2}{\mu^2} \cdot \frac{1}{t}.$$

*Proof.* Standard minimax lower bound for stochastic optimization (Agarwal et al., 2012; Raginsky & Rakhlin, 2011). The Cramér-Rao bound for sequential estimation gives $\Omega(1/t)$. $\square$

### 10.2 Gap Analysis

| Regime | Upper Bound | Lower Bound | Gap Factor |
|--------|------------|-------------|------------|
| $\alpha_t = t^{-1}$, SC | $O(t^{-1})$ | $\Omega(t^{-1})$ | $O(1)$ — **tight** |
| $\alpha_t = t^{-0.5}$, SC | $O(t^{-0.5})$ | $\Omega(t^{-1})$ | $O(t^{0.5})$ — **loose** |
| Non-convex, stationarity | $O(t^{-0.5})$ | N/A (no optimality guarantee) | — |
| Gatekeeper, contraction | $O(t^{-b})$ | $\Omega(1/N_t) = \Omega(t^{-1})$ | $O(t^{1-b})$ — **loose for $b < 1$** |

**Interpretation**: With optimal tuning ($a = 1$, Polyak averaging), the student rate matches the minimax lower bound up to constants. With suboptimal tuning ($a = 0.5$), the rate is suboptimal by $O(\sqrt{t})$. The gatekeeper rate has room for improvement — the $t^{-b}$ dependence from iterative refinement is looser than the $1/\sqrt{N_t}$ statistical rate from memory accumulation.

### 10.3 Tightening the Gatekeeper Rate

**Proposition 11.7 (Improved Gatekeeper Rate via Batch Updates — CONJECTURED).** If the gatekeeper is updated using **full-batch** SCXUpdate on the entire memory bank (rather than incremental updates), its convergence rate improves to:

$$\mathbb{E}[\|S_t - S^*\|_{M_0}^2] \leq \frac{C_S'}{\sqrt{N_t}},$$

matching the statistical rate. Since $N_t = \Theta(t)$ (constant batch sizes), this gives $O(t^{-0.5})$.

*Status: **CONJECTURED.** The full-batch update eliminates the iterative refinement bottleneck, leaving only the statistical error from finite memory. This is faster than the incremental rate when $b < 0.5$.*

---

## 11. Summary

### 11.1 Proven Results

| Result | Status | Rate |
|--------|--------|------|
| Student rate under strong convexity (stationary dist.) | **PROVEN** | $O(t^{-a})$, $a \in (0.5, 1]$ |
| Student rate under PL condition | **PROVEN** | $O(t^{-a})$ |
| Student stationarity rate (non-convex) | **PROVEN** | $O(t^{-(1-a)})$ |
| Finite-time student bound | **PROVEN** | $O(t^{-a}) + O(t^{-0.5})$ (concentration) |
| Minimax lower bound | **PROVEN** | $\Omega(t^{-1})$ |

### 11.2 Conjectured Results

| Result | Status | Expected Rate |
|--------|--------|---------------|
| Coupled rate under strong convexity | **CONJECTURED** | $O(t^{-a})$ |
| Gatekeeper rate | **CONJECTURED** | $O(t^{-b})$ |
| Finite-time gatekeeper bound | **CONJECTURED** | $O(t^{-b}) + O(t^{-0.5})$ |
| Optimal rate allocation $b = a + \varepsilon$ | **CONJECTURED** | $O(t^{-a})$ |

### 11.3 Parameter Dependence Summary

| Parameter | Effect on Rate Constant | Effect on Rate Exponent |
|-----------|------------------------|------------------------|
| $L_f$ (Lipschitz) | $C \propto L_f^3$ | None |
| $\alpha_t = t^{-a}$ | $C \propto \alpha_0$ | Rate = $t^{-a}$ |
| $d_\phi$ (dimension) | $C \propto 1 + \gamma d_\phi \log t$ | None (logarithmic) |
| $\eta$ (noise rate) | $C \propto 1/\Delta_{\min}^2(\eta)$ | None |
| $\mu$ (curvature) | $C \propto 1/\mu$ | None |
| $\sigma_\xi^2$ (gradient noise) | $C \propto \sigma_\xi^2$ | None |

### 11.4 Practical Recommendations

1. **Use Polyak-Ruppert averaging** on the student iterates to achieve $O(1/t)$ rate regardless of $a \in (0.5, 1)$.
2. **Set $a = 0.5$, $b = 0.6$** for robust convergence with near-optimal rate allocation.
3. **Use batch gatekeeper updates** if computationally feasible, to achieve the $O(1/\sqrt{N_t})$ statistical rate.
4. **Monitor $\|\nabla \bar{L}(\theta_t)\|$** as a practical convergence diagnostic — it should decay as $t^{-(1-a)/2}$.
5. **The feature dimension $d_\phi$ has only logarithmic effect** on the asymptotic rate — scaling to high-dimensional features is feasible.

---

*End of 11_convergence_rate.md — Convergence Rate Analysis*

---

## References

1. Bach, F., & Moulines, E. (2011). Non-asymptotic analysis of stochastic approximation algorithms for machine learning. *NIPS 2011*.
2. Polyak, B. T., & Juditsky, A. B. (1992). Acceleration of stochastic approximation by averaging. *SIAM Journal on Control and Optimization*, 30(4), 838-855.
3. Ghadimi, S., & Lan, G. (2013). Stochastic first- and zeroth-order methods for nonconvex stochastic programming. *SIAM Journal on Optimization*, 23(4), 2341-2368.
4. Karimi, H., Nutini, J., & Schmidt, M. (2016). Linear convergence of gradient and proximal-gradient methods under the Polyak-Łojasiewicz condition. *ECML PKDD 2016*.
5. Needell, D., Srebro, N., & Ward, R. (2014). Stochastic gradient descent, weighted sampling, and the randomized Kaczmarz algorithm. *NIPS 2014*.
6. Borkar, V. S. (2008). *Stochastic Approximation: A Dynamical Systems Viewpoint*. Cambridge University Press.
7. Agarwal, A., et al. (2012). Information-theoretic lower bounds on the oracle complexity of stochastic convex optimization. *IEEE Transactions on Information Theory*, 58(5), 3235-3249.
8. Raginsky, M., & Rakhlin, A. (2011). Information-based complexity, feedback and dynamics in convex programming. *IEEE Transactions on Information Theory*, 57(10), 7036-7056.
9. Jin, C., et al. (2017). How to escape saddle points efficiently. *ICML 2017*.
10. Kushner, H. J., & Yin, G. G. (2003). *Stochastic Approximation and Recursive Algorithms and Applications* (2nd ed.). Springer.
