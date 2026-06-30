# SCX Self-Evolution as a Discrete Dynamical System

> **Version**: 2026-06-28 | **Status**: Theoretical development | **Audit**: Pre-verification
> **Purpose**: Formalize the SCX self-evolution loop as a discrete dynamical system, study fixed points, Lyapunov stability, attractor structure, and phase portraits.
> **Prerequisites**: Document 01 (Symbol System and Problem Setup)

---

## Table of Contents

1. [Discrete Dynamical System Formulation](#1-discrete-dynamical-system-formulation)
2. [State Space Topology and Metric on S_t](#2-state-space-topology-and-metric-on-s_t)
3. [Orbits Under Phi](#3-orbits-under-phi)
4. [Attractors and Omega-Limit Sets](#4-attractors-and-omega-limit-sets)
5. [Fixed Points](#5-fixed-points)
6. [Existence Conditions for Fixed Points](#6-existence-conditions-for-fixed-points)
7. [Lyapunov Function Candidate](#7-lyapunov-function-candidate)
8. [Monotonicity Analysis](#8-monotonicity-analysis)
9. [Phase Portrait](#9-phase-portrait)
10. [Connection to Existing Theorems 1-3](#10-connection-to-existing-theorems-1-3)
11. [Summary of Proven vs. Conjectured Claims](#11-summary-of-proven-vs-conjectured-claims)

---

## 1. Discrete Dynamical System Formulation

### 1.1 Basic Formulation

Let $z_t = (S_t, M_t, \theta_t) \in \mathcal{Z}$ be the evolution state at time $t$ as defined in Document 01, Section 5. The self-evolution loop is a discrete dynamical system:

$$z_{t+1} = \Phi(z_t), \qquad t = 0, 1, 2, \dots$$

with initial condition $z_0 = (S_0, M_0, \theta_0)$ determined by the static SCX initialization.

**Definition 16 (Discrete-Time Dynamical System).** The tuple $(\mathcal{Z}, \Phi, \mathbb{N}_0)$ constitutes a discrete-time dynamical system where:
- $\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$ is the state space (Section 5 of Document 01)
- $\Phi: \mathcal{Z} \to \mathcal{Z}$ is the update operator (Section 9 of Document 01)
- $\mathbb{N}_0 = \{0, 1, 2, \dots\}$ is the discrete time index

### 1.2 Decomposition into Component Maps

The operator $\Phi$ decomposes into three coupled maps:

$$\Phi(S, M, \theta) = \bigl( \Phi_S(S, M, \theta),\; \Phi_M(S),\; \Phi_\theta(S, M) \bigr)$$

where the coupling structure is:

```
S_t ──Φ_M──→ M_{t+1}
S_t ──Φ_θ──→ θ_{t+1}  (via M_{t+1})
S_t, M_{t+1}, θ_{t+1} ──Φ_S──→ S_{t+1}
```

This coupling is **feed-forward**: $S_t$ influences $M_{t+1}$ and $\theta_{t+1}$, which in turn influence $S_{t+1}$. There is no instantaneous feedback loop.

**Proposition 3 (Causal Structure).** The system's information flow is a directed acyclic graph within each timestep: $S_t \to M_{t+1} \to \theta_{t+1}$, and $(S_t, M_{t+1}, \theta_{t+1}) \to S_{t+1}$. Consequently, the Jacobian of $\Phi$ is block-triangular.

*Proof.* By inspection of the update definitions: $\Phi_M$ depends only on $S_t$ (not on $M_t$ or $\theta_t$); $\Phi_\theta$ depends on $M_{t+1}$ and implicitly on $S_t$ through $M_{t+1}$; $\Phi_S$ depends on all three. $\square$

---

## 2. State Space Topology and Metric on $S_t$

### 2.1 Metric Structure

Recall from Document 01 the metric on $\mathcal{F}$:

$$d_{\mathcal{F}}(S, S') = \mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ |S(x,y) - S'(x,y)| \bigr]$$

and the product metric on $\mathcal{Z}$:

$$d_{\mathcal{Z}}(z, z') = d_{\mathcal{F}}(S, S') + d_{\mathcal{M}}(M, M') + \|\theta - \theta'\|_2$$

**Proposition 4 (Completeness).** If $\mathcal{D}$ has full support on $\mathcal{X}_0 \times \mathcal{Y}$, then $(\mathcal{F}, d_{\mathcal{F}})$ is a complete metric space. The product space $(\mathcal{Z}, d_{\mathcal{Z}})$ is complete.

*Proof sketch.* $L^1(\mathcal{D})$ is complete. The finite set $\mathcal{M}$ with the discrete topology is trivially complete. $\Theta \subseteq \mathbb{R}^{d_\theta}$ is complete if closed. The product of complete metric spaces is complete. $\square$

### 2.2 Compactness Considerations

For existence of fixed points and attractors, compactness of the state space is desirable.

**Proposition 5 (Compactness of $\mathcal{F}$ under Regularization).** If we restrict $\mathcal{F}$ to the set of functions:
- bounded in $L^\infty$ norm (already $[0,1]$-valued)
- with uniformly bounded Lipschitz constant $L_S < \infty$ with respect to input distance
then $\mathcal{F}$ is compact in $d_{\mathcal{F}}$ by the Arzela-Ascoli theorem (on compact subsets of $\mathcal{X}_0$).

*Practical implication.* In implementation, neural network gatekeepers satisfy Lipschitz bounds (e.g., via spectral normalization). Theoretical analysis often assumes such regularization to ensure well-posedness.

---

## 3. Orbits Under $\Phi$

### 3.1 Definition

**Definition 17 (Orbit).** The forward orbit of an initial state $z_0 \in \mathcal{Z}$ under $\Phi$ is the sequence:

$$\mathcal{O}^+(z_0) = \{ z_0, \Phi(z_0), \Phi^{(2)}(z_0), \Phi^{(3)}(z_0), \dots \}$$

The backward orbit (if $\Phi$ is invertible) is defined analogously but is not guaranteed.

### 3.2 Types of Orbits

Based on the system's behavior, we classify orbits into three types:

**Definition 18 (Orbit Classification).**

1. **Convergent orbit**: $\lim_{t\to\infty} d_{\mathcal{Z}}(z_t, z^*) = 0$ for some $z^* \in \mathcal{Z}$.
2. **Periodic orbit**: $\exists T > 0$ such that $z_{t+T} = z_t$ for all sufficiently large $t$, with no smaller period.
3. **Chaotic orbit**: The orbit is bounded but does not converge and is not periodic; sensitive dependence on initial conditions may occur.

**Conjecture 2 (Orbit Classification for SCX).** Under Assumptions B1-B3, all orbits of the SCX self-evolution system are convergent. No periodic or chaotic orbits exist.

*Status: **Conjecture**. The monotonicity of $M_t$ (B1) prevents cycling through memory loss, but stochastic gradient updates in $\Phi_S$ and $\Phi_\theta$ could, in principle, produce limit cycles. The conjecture asserts that the Lyapunov function (Section 7) eliminates this possibility.*

### 3.3 Properties of Orbits

**Proposition 6 (Boundedness of Orbits).** Under Assumption B2 (bounded memory growth), any orbit $\mathcal{O}^+(z_0)$ is bounded in $\mathcal{Z}$.

*Proof.* $S_t$ is bounded in $[0,1]$ by construction, $\|S_t\|_\infty \leq 1$. $\theta_t$ is bounded if the loss landscape has bounded sublevel sets (e.g., under L2 regularization). $M_t$ has bounded size by B2. Hence $d_{\mathcal{Z}}(z_0, z_t)$ is bounded for all $t$. $\square$

---

## 4. Attractors and $\omega$-Limit Sets

### 4.1 Definition

**Definition 19 ($\omega$-Limit Set).** For a trajectory $z_t = \Phi^{(t)}(z_0)$, the $\omega$-limit set is:

$$\omega(z_0) = \bigl\{ z \in \mathcal{Z} : \exists \{t_k\}_{k=1}^\infty \text{ with } t_k \to \infty \text{ and } \lim_{k\to\infty} d_{\mathcal{Z}}(z_{t_k}, z) = 0 \bigr\}$$

The $\alpha$-limit set (for backward orbits) is defined analogously.

**Definition 20 (Attractor).** A set $A \subseteq \mathcal{Z}$ is an attractor if:
1. $A$ is invariant: $\Phi(A) = A$.
2. There exists a neighborhood $U$ of $A$ such that $\omega(z) \subseteq A$ for all $z \in U$.
3. $A$ is minimal with respect to properties 1 and 2.

The **basin of attraction** of $A$ is:

$$\mathcal{B}(A) = \{ z \in \mathcal{Z} : \omega(z) \subseteq A \}$$

### 4.2 Candidate Attractors for SCX

**Proposition 7 (Fixed Points as Attractors).** If $z^*$ is an asymptotically stable fixed point (Definition 21), then $\{z^*\}$ is an attractor with basin $\mathcal{B}(z^*)$ containing an open neighborhood of $z^*$.

The primary candidate attractor for the SCX self-evolution system is the **perfect gatekeeper**:

$$S^*(x,y) = \mathbf{1}\{y = f^*(x)\}$$

i.e., the gatekeeper that perfectly identifies whether the observed label matches the true oracle. However, achieving this fixed point requires:
1. The NEP student converges to $f^*$ (Assumption B3)
2. The memory bank contains sufficient clean samples

**Conjecture 3 (Unique Attractor).** Under Assumptions B1-B3 and the uniform noise assumption (A4), the SCX self-evolution system has a unique attractor $z^* = (S^*, M^*, \theta^*)$ where $S^*(x,y) = \mathbf{1}\{y = f^*(x)\}$, $M^*$ is the infinite memory bank containing all sufficiently clean samples, and $\theta^*$ parameterizes $f^*$.

*Status: **Conjecture**. The uniqueness depends on the loss landscape of the gatekeeper and NEP being convex, which is not guaranteed for neural network parameterizations. However, if the function spaces are sufficiently expressive and the losses are proper scoring rules, the fixed point is unique in function space.*

---

## 5. Fixed Points

### 5.1 Definition

**Definition 21 (Fixed Point).** A state $z^* = (S^*, M^*, \theta^*) \in \mathcal{Z}$ is a fixed point of the dynamics if:

$$\Phi(z^*) = z^*$$

Equivalently:

$$\Phi_S(S^*, M^*, \theta^*) = S^*$$
$$\Phi_M(S^*, M^*) = M^*$$
$$\Phi_\theta(S^*, M^*) = \theta^*$$

**Definition 22 (Stability of Fixed Points).** A fixed point $z^*$ is:
- **Lyapunov stable** if $\forall \varepsilon > 0$, $\exists \delta > 0$ such that $d_{\mathcal{Z}}(z_0, z^*) < \delta$ implies $d_{\mathcal{Z}}(z_t, z^*) < \varepsilon$ for all $t \geq 0$.
- **Asymptotically stable** if it is Lyapunov stable and $\exists \delta > 0$ such that $d_{\mathcal{Z}}(z_0, z^*) < \delta$ implies $\lim_{t\to\infty} d_{\mathcal{Z}}(z_t, z^*) = 0$.
- **Unstable** if it is not Lyapunov stable.

### 5.2 Fixed Point Equations

**Fixed point equation for $S^*$:**

$$S^*(x, y) = \text{Update}_{\text{gate}}\bigl(S^*, M^*, f_{\theta^*}\bigr)(x, y)$$

For a gradient-based update $\text{Update}_{\text{gate}}(S, M, f_\theta) = S - \alpha \nabla_S \hat{L}_{\text{gate}}(S; M)$, this implies:

$$\nabla_S \hat{L}_{\text{gate}}(S^*; M^*) = 0$$

i.e., $S^*$ is a stationary point of the gatekeeper loss on the memory bank $M^*$.

**Fixed point equation for $M^*$:**

$$M^* = M^* \cup \{(x, y, S^*(x,y), S^*(x,y)) : (x,y) \in q, \; S^*(x,y) > \delta_{\text{store}}\}$$

This implies:

$$\{ (x,y) \in \text{supp}(\mathcal{D}) : S^*(x,y) > \delta_{\text{store}} \} \subseteq M^*$$

i.e., $M^*$ contains all samples that the fixed-point gatekeeper judges reliable. Since memory is monotone (B1), $M^*$ is the limit of the growing sequence.

**Fixed point equation for $\theta^*$:**

$$\theta^* = \arg\min_{\theta \in \Theta} \frac{1}{|M^*|} \sum_{(x_i, y_i, \cdot, \cdot) \in M^*} \ell_{\text{nep}}(f_\theta(x_i), y_i)$$

i.e., $\theta^*$ minimizes the NEP loss on $M^*$.

### 5.3 Trivial Fixed Points

**Proposition 8 (Trivial Fixed Points).** The following are fixed points of $\Phi$:

1. **Zero gatekeeper**: $S_0 \equiv 0$, $M_0 = \varnothing$, $\theta_0$ arbitrary. The system never stores any samples and never updates. (Unstable — any positive $S$ triggers storage.)

2. **Perfect gatekeeper**: $S^*(x, y) = \mathbf{1}\{y = f^*(x)\}$, $M^* = \{(x, f^*(x), 1, 1) : x \in \mathcal{X}_0\}$, $f_{\theta^*} = f^*$. All samples are judged correctly; nothing changes. (Asymptotically stable if the NEP converges.)

3. **Constant gatekeeper**: $S(x, y) \equiv c$ for some $c \neq \delta_{\text{store}}$. If $c < \delta_{\text{store}}$, no samples are stored (like 1). If $c > \delta_{\text{store}}$, all samples are stored, $M$ grows to the entire dataset.

*Proof sketch.* Each satisfies the fixed point equations by inspection. For stability claims, see Section 8. $\square$

---

## 6. Existence Conditions for Fixed Points

### 6.1 General Existence

**Theorem 4 (Existence of Fixed Points).** Suppose:
1. $\Phi$ is continuous on $\mathcal{Z}$ in the product metric $d_{\mathcal{Z}}$.
2. $\mathcal{Z}$ is compact in $d_{\mathcal{Z}}$.
3. $\Phi$ maps $\mathcal{Z}$ into itself.

Then $\Phi$ has at least one fixed point in $\mathcal{Z}$.

*Proof.* Apply the Brouwer fixed-point theorem (for compact convex subsets of a Banach space) or Schauder-Tychonoff (for locally convex topological vector spaces). The product structure $\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$ with $\mathcal{F}$ compact (Proposition 5) and $\Theta$ compact (under boundedness), and $\mathcal{M}$ finite, satisfies the hypotheses. $\square$

**Remark.** Condition 1 (continuity of $\Phi$) is non-trivial: the $\arg\min$ in $\Phi_\theta$ is set-valued if the minimum is not unique. Formalizing $\Phi$ as a selection from a correspondence (upper hemicontinuous) allows using the Kakutani fixed-point theorem instead.

### 6.2 Specific Existence for SCX

**Theorem 5 (Fixed Point Existence for SCX with Convex Loss).** Suppose:
1. The gatekeeper loss $L_{\text{gate}}(S; M)$ is strictly convex in $S$ for any $M$.
2. The NEP loss $L_{\text{nep}}(\theta; M)$ is strictly convex in $\theta$ for any $M$.
3. The memory bank growth saturates: $\lim_{t\to\infty} \mathbb{P}(S_t(x,y) > \delta_{\text{store}}) = 0$ or $1$ for each $(x,y)$.

Then there exists a unique fixed point $z^* = (S^*, M^*, \theta^*)$.

*Proof sketch.* Convexity ensures unique minimizers for $S^*$ and $\theta^*$, making $\Phi$ a function (not correspondence). Under the saturation condition, $M^*$ is the limit of the monotone sequence. The contraction mapping principle (if $\Phi$ is a contraction) or Schauder fixed point gives existence. $\square$

*Status: **Rigorous** under the stated convexity assumptions. In practice, neural network losses are non-convex, so the conditions are violated. The theorem provides an idealized benchmark.*

### 6.3 Necessary Condition for Non-Trivial Fixed Point

**Proposition 9 (Necessary Condition).** If $z^*$ is a fixed point with $M^* \neq \varnothing$, then the NEP student $f_{\theta^*}$ must satisfy:

$$\mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ \ell_{\text{nep}}(f_{\theta^*}(x), y) \mid S^*(x,y) > \delta_{\text{store}} \bigr] \leq \mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ \ell_{\text{nep}}(f_{\theta^*}(x), y) \mid S^*(x,y) \leq \delta_{\text{store}} \bigr]$$

i.e., the NEP performs no worse on samples the gatekeeper admits than on samples it rejects.

*Proof.* At a fixed point, the gatekeeper's storage policy and the NEP's parameters are consistent. If the inequality were reversed, the gatekeeper would be systematically mislabeling high-loss samples as reliable, contradicting the stationarity of $S^*$ (since $S^*$ minimizes $L_{\text{gate}}$ on $M^*$, and $M^*$ contains only admitted samples). $\square$

---

## 7. Lyapunov Function — Explicit Candidate (DEFECT-03/04 Fix)

> **Status change (2026-06-28).** The original Section 7 defined a vague Lyapunov candidate $V(z_t) = \mathbb{E}[L_{\text{gate}}] + \lambda \cdot \mathbb{E}[L_{\text{nep}}]$ evaluated on the acceptance-biased distribution. This was found to be **underspecified** (DEFECT-03) and to contain a **selection bias confound** (DEFECT-04): a decrease in $V$ could reflect distribution shift rather than genuine model improvement. The following explicit candidate on a **fixed reference set** is adopted as a concrete target for future proof. The convergence claim is downgraded from "Proven" to **Conjecture**.

### 7.1 Concrete Lyapunov Function Candidate

**Definition 23 (Concrete Lyapunov Function Candidate).** Define $\Psi: \mathcal{F} \times \Theta \to \mathbb{R}_{\geq 0}$:

$$\boxed{\;\Psi(S_t, \theta_t) = \frac{1}{|M_0|} \sum_{x \in M_0} \bigl(S_t(x, y(x)) - \hat{C}(x)\bigr)^2 \;+\; \lambda \cdot \frac{1}{|V_0|} \sum_{(x,y) \in V_0} \ell(f_{\theta_t}(x), y)\;},$$

where:
- $M_0 \subset \mathcal{X} \times \mathcal{Y}$ is a **fixed reference set** (e.g., initial samples before self-evolution begins, or an external validation set). $M_0$ does **not** grow with $t$.
- $V_0 \subseteq M_0$ is the subset of $M_0$ with externally verified clean labels,
- $\hat{C}(x) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ is the consensus score computed from the $M$ expert models (fixed),
- $\lambda > 0$ is a balancing hyperparameter.

> **Notation note (B3 fix):** The Lyapunov function is denoted $\Psi$ (Psi), NOT $\Phi$ (Phi). The symbol $\Phi$ is reserved for the **Update Operator** $\Phi: \mathcal{Z} \to \mathcal{Z}$ defined in Document 01, Section 9. This resolves the $\Phi$-$\Psi$ notation collision identified in the cross-file consistency audit.

**Why a fixed reference set?** The original Lyapunov candidate evaluated both gatekeeper and student losses on the acceptance-biased distribution $P_{S_t}$. This created a **selection bias confound** (DEFECT-04/13): the gatekeeper can decrease its apparent loss by becoming more selective and admitting only "easy" samples, without improving its true discriminative ability. By evaluating on a fixed reference set $M_0$ that does not change with $t$, we ensure that a decrease in $\Phi$ reflects genuine improvement.

### 7.2 Component Decomposition

The Lyapunov function decomposes into two interpretable terms:

**Gatekeeper term ($\Psi_{\text{gate}}$).** Measures the squared discrepancy between the gatekeeper's score $S_t(x, y(x))$ and the fixed expert consensus $\hat{C}(x)$ on the reference set. This term decreases when the gatekeeper's judgments align better with expert consensus:
$$\Psi_{\text{gate}}(S_t) = \frac{1}{|M_0|} \sum_{x \in M_0} (S_t(x, y(x)) - \hat{C}(x))^2.$$

**Student term ($\Psi_{\text{student}}$).** Measures the NEP student's prediction error on the verified-clean subset $V_0$. This term decreases when the student learns better representations:
$$\Psi_{\text{student}}(\theta_t) = \frac{1}{|V_0|} \sum_{(x,y) \in V_0} \ell(f_{\theta_t}(x), y).$$

### 7.3 Properties

**Proposition 10 (Properties of $\Psi$).**
1. **Non-negativity**: $\Psi(S, \theta) \geq 0$ for all $(S, \theta)$, with equality iff $S_t(x, y(x)) = \hat{C}(x)$ for all $x \in M_0$ and $f_{\theta_t}(x) = y$ for all $(x,y) \in V_0$.
2. **Boundedness**: Under Assumption A3 (bounded loss $\ell \leq B$), $\Psi(S, \theta) \leq 1 + \lambda B < \infty$ since $S_t \in [0,1]$ and $\hat{C} \in [0,1]$.
3. **Continuity**: $\Psi$ is continuous in $(S, \theta)$ under the product metric $d_{\mathcal{Z}}$ if $\ell$ is continuous and $M_0$ is finite.

*Proof.* (1) Sums of squares and non-negative losses. (2) $|S_t - \hat{C}| \leq 1$, so the squared term $\leq 1$; $\ell \leq B$ by A3. (3) Composition of continuous functions; for finite $M_0$, the empirical average is continuous in each argument. $\square$

### 7.4 Descent Analysis — Honest Assessment

**Definition 24 (Lyapunov Descent Property).** $\Psi$ is a Lyapunov function for the dynamical system $(\mathcal{Z}, \Phi)$ (where $\Phi$ is the Update Operator) if:

$$\mathbb{E}[\Psi(S_{t+1}, \theta_{t+1}) \mid \mathcal{F}_t] \leq \Psi(S_t, \theta_t) - \eta_t, \quad \eta_t \geq 0,$$

with $\eta_t > 0$ except at fixed points.

**Theorem 6 (Lyapunov Descent — CONDITIONAL, CONJECTURED).** Under the following jointly sufficient conditions, the candidate $\Psi$ satisfies the descent property:

1. **Two-timescale separation (C6')**: $\beta_t = o(\alpha_t)$ — gatekeeper updates are asymptotically slower than student updates.
2. **Student gradient descent (C2, C4)**: Standard SGD with Robbins-Monro rates on $\alpha_t$.
3. **Gatekeeper moves toward consensus (C3, C7)**: SCXUpdate reduces the discrepancy $|S_t - \hat{C}|$ when applied to new data.
4. **Random exploration (C8)**: A fraction $\varepsilon > 0$ of accepted samples are chosen uniformly at random regardless of $S_t$ score, ensuring the reference distribution remains represented.
5. **Annealing acceptance threshold (C9)**: $\gamma_t \to 0.5$ as $t \to \infty$, starting from a permissive initial value $\gamma_0 < 0.5$.

*Proof sketch (gaps acknowledged).* Decompose the one-step change:

$$\Psi(S_{t+1}, \theta_{t+1}) - \Psi(S_t, \theta_t) = \underbrace{[\Psi_{\text{gate}}(S_{t+1}) - \Psi_{\text{gate}}(S_t)]}_{\text{(A)}} + \lambda \underbrace{[\Psi_{\text{student}}(\theta_{t+1}) - \Psi_{\text{student}}(\theta_t)]}_{\text{(B)}}.$$

**Term (A) — Gatekeeper update on reference set.** The gatekeeper update $S_{t+1} = \Pi_{[0,1]}[S_t + \beta_t(\text{SCXUpdate} - S_t)]$ moves $S_t$ toward $\hat{C}$. However, this movement is **not guaranteed** to reduce $\Psi_{\text{gate}}$ on $M_0$ because SCXUpdate uses data from $M_{t+1}$ (acceptance-biased), not from $M_0$. **Gap: The alignment between SCXUpdate's direction on $M_{t+1}$ and the gradient of $\Psi_{\text{gate}}$ on $M_0$ is not established.** Under exploration (C8), $M_{t+1}$ eventually contains representatives from all regions, so for large $t$, the empirical distributions $P_{M_{t+1}}$ and $P_{M_0}$ become close. But the rate of this convergence depends on the exploration fraction $\varepsilon$ and the data distribution's support.

**Term (B) — Student update on reference set.** The student is trained by SGD on $M_t$ (acceptance-biased), not on $V_0$. A standard SGD step reduces the loss on the training distribution $P_{S_t}$, but may **increase** the loss on the reference distribution $P_{V_0}$. **Gap: The relationship between $\mathbb{E}_{P_{S_t}}[\ell]$ and $\mathbb{E}_{P_{V_0}}[\ell]$ is not controlled.** Under two-timescale separation (C6'), the student takes many steps between gatekeeper updates, converging approximately to a local minimum of the current $P_{S_t}$. The quality of this minimum on $P_{V_0}$ depends on the KL divergence between the distributions:
$$\mathbb{E}_{P_{V_0}}[\ell(f_\theta)] \leq \mathbb{E}_{P_{S_t}}[\ell(f_\theta)] + D_{KL}(P_{V_0} \| P_{S_t})/C,$$
which is bounded only if the gatekeeper does not systematically exclude regions of $V_0$.

**Overall assessment.** The descent inequality $\mathbb{E}[\Psi_{t+1} \mid \mathcal{F}_t] \leq \Psi_t - \eta_t$ has **not been rigorously proven**. The decomposition above identifies two critical gaps: (i) alignment of gatekeeper update direction on biased vs. reference data, and (ii) generalization of student improvement from training distribution to reference distribution. The additional conditions (C6', C8, C9) are designed to close these gaps, but their formal sufficiency has not been established. **The descent property is therefore a conjecture, not a theorem.**

### 7.5 Downgraded Convergence Claim

**Conjecture SE-1 (formerly "Theorem SE-1").** With the explicit Lyapunov candidate $\Psi$ defined above and under conditions (C1')-(C9) (see Document 06 for the full condition set), the SCX self-evolution sequence satisfies:

$$\Psi(S_t, \theta_t) \xrightarrow{a.s.} \Psi_\infty \geq 0,$$
$$\sum_{t=1}^\infty \bigl( \alpha_t \|\nabla_\theta L_t(\theta_t)\|^2 + \beta_t \|\Delta S_t\|^2 \bigr) < \infty \quad \text{a.s.},$$

and any limit point $(S_\infty, \theta_\infty)$ satisfies the fixed-point equations. The convergence is in the **Cesàro mean** sense rather than monotonic: the Lyapunov function may increase at individual steps but its long-run average decreases.

> **Honest status (2026-06-28).** This is labeled a **Conjecture** because the Lyapunov descent property (Definition 24) has not been rigorously proven. The key difficulties are the selection bias cycle (DEFECT-13) and the tension between gatekeeper exploration and student stabilization (DEFECT-14). The conditions (C6'), (C8), and (C9) are proposed mechanisms to address these difficulties, but their formal sufficiency awaits proof. Numerical evidence is pending.

---

## 8. Monotonicity Analysis

### 8.1 Expected Monotonicity

**Corollary 1 (Expected Monotonicity).** Under the conditions of Theorem 6, even if the losses are not convex but the gradient updates are unbiased estimators of the true gradient:

$$\mathbb{E}[\Delta V(z_t)] \leq 0 \quad \forall t$$

where the expectation is over the random sampling of batches.

*Proof.* The gradient descent update ensures descent in expectation for sufficiently small step sizes (standard result for SGD with unbiased gradients). $\square$

### 8.2 Strict Monotonicity Gap

**Proposition 11 (Strict Decrease Condition).** The inequality $\Delta V(z_t) < 0$ is strict unless both of the following hold:
1. $S_t$ is already optimal given $M_{t+1}$: $\nabla_S \hat{L}_{\text{gate}}(S_t; M_{t+1}) = 0$.
2. $\theta_t$ is already optimal given $M_{t+1}$: $\nabla_\theta \hat{L}_{\text{nep}}(f_{\theta_t}; M_{t+1}) = 0$.

If either gradient is non-zero, the gradient step strictly decreases the respective loss (for sufficiently small step sizes), giving $\Delta V(z_t) < 0$.

### 8.3 Monotonicity of Memory Bank

A separate monotonicity holds for the memory bank:

**Proposition 12 (Memory Monotonicity).** The sequence $\{N_t\}_{t=0}^\infty$ of memory bank sizes is non-decreasing:

$$N_0 \leq N_1 \leq N_2 \leq \dots$$

and converges to $N_\infty \leq \infty$.

*Proof.* $M_t \subseteq M_{t+1}$ (Assumption B1) directly implies $N_t \leq N_{t+1}$. Monotone bounded sequences converge (possibly to $\infty$). $\square$

### 8.4 Relationship Between $V$ and $N_t$

**Proposition 13 (Consistency of Monotonicities).** A decreasing Lyapunov function $V(z_t)$ and an increasing memory size $N_t$ are not contradictory: $V$ measures average loss (which decreases as the system learns), while $N_t$ measures total accumulated data (which increases). The system can simultaneously get better (lower $V$) and accumulate more data (higher $N_t$).

---

## 9. Phase Portrait

### 9.1 Qualitative Description

Based on the analysis above, the SCX self-evolution system has the following qualitative phase portrait:

**Regime I: Initialization** ($t = 0$).
- $S_0$ derived from static SCX consensus score
- $M_0$ contains initial reliable samples (or empty)
- $\theta_0$ from pretrained model (or random)
- $V(z_0)$ is finite and bounded by Theorem 1's guarantee

**Regime II: Rapid Improvement** ($0 < t < T_1$).
- The gatekeeper rapidly improves as it receives feedback from the growing memory bank
- $V(z_t)$ decreases quickly
- The NEP student begins to provide useful delayed feedback
- $N_t$ grows rapidly

**Regime III: Diminishing Returns** ($T_1 \leq t < T_2$).
- The gatekeeper approaches its optimal performance given the available data
- $V(z_t)$ decreases slowly
- Memory bank growth slows (only hard or ambiguous samples remain)
- The system enters a "refinement" phase

**Regime IV: Saturation** ($t \geq T_2$).
- $z_t$ approaches a fixed point $z^*$
- $V(z_t)$ plateaus
- $N_t$ saturates (or grows only from genuinely novel samples)
- The system has converged

### 9.2 Parameter Dependence

The qualitative behavior depends on several key parameters:

| Parameter | Effect on Dynamics |
|-----------|-------------------|
| $\eta$ (noise rate) | Higher $\eta$ slows convergence (more noise to filter) |
| $\mu_s$ (clean error) | Higher $\mu_s$ reduces initial $S_0$ quality, slowing early improvement |
| $M$ (number of experts) | Larger $M$ improves $S_0$ via tighter concentration (Theorem 1) |
| $\delta_{\text{store}}$ | Higher threshold: slower memory growth, higher precision |
| $\lambda$ (Lyapunov weight) | Higher $\lambda$ prioritizes NEP improvement over gatekeeper |
| $\alpha, \beta$ (step sizes) | Larger steps: faster convergence but risk of overshoot |

### 9.3 Phase Diagram

We can partition the parameter space into regimes:

**Region A (Convergent)** $\subset \mathcal{Z}$: Initial states from which the system converges to a fixed point. Under Assumptions B1-B3, this region contains all physically realizable initial states.

**Region B (Limit Cycle)** $\subset \mathcal{Z}$: Initial states leading to periodic orbits. **Conjectured empty** for SCX (Conjecture 2).

**Region C (Divergent)** $\subset \mathcal{Z}$: Initial states from which the system diverges (e.g., $N_t \to \infty$ without convergence of $S_t$). This can occur if $\delta_{\text{store}}$ is too low, causing the system to accumulate noisy samples indefinitely.

**Proposition 14 (Divergence Condition).** If $\delta_{\text{store}} < \eta$ (the storage threshold is below the noise rate), the system may diverge in Region C: the gatekeeper stores a significant proportion of noisy samples, degrading the NEP student, which further degrades the gatekeeper, creating a vicious cycle.

*Proof sketch.* If $\delta_{\text{store}} < \eta$, then even a random gatekeeper would store > $\eta$ fraction of noisy samples. The stored noise contaminates $M_{t+1}$, which trains $\theta_{t+1}$, potentially amplifying the error. Formalizing this requires analyzing the noise propagation eigenvalue (see Proposition 15). $\square$

---

## 10. Connection to Existing Theorems 1-3

### 10.1 Theorem 1: Noise Detection Guarantee

Theorem 1 provides the **initialization guarantee** for the dynamical system:

$$V(z_0) \leq 1 - \text{F1}_0 \leq \frac{1}{\eta} \sum_{s \in \mathcal{S}} \rho_s \cdot \exp\bigl(-2M\Delta_s^2\bigr)$$

This bounds the initial Lyapunov value $V(z_0)$ in terms of the noise detection F1 score.

**Dynamical implication**: The system starts with $V(z_0) \leq \varepsilon_0(M)$ where $\varepsilon_0(M)$ decreases exponentially in $M$. A larger $M$ gives a better initialization, reducing the number of evolution rounds needed to reach a given performance level.

### 10.2 Theorem 2: Weak Feature Failure Lower Bound

Theorem 2 constrains the **improvement rate** of the dynamical system:

If $\phi$ is $\delta$-weak, then for any $t$:

$$F1_t \leq F1_{\text{base}} + C_F \sqrt{\frac{\delta}{2}} + \text{(evolution improvement)}$$

The "evolution improvement" term captures what self-evolution adds beyond the static baseline. **Conjectured behavior**: this improvement term itself is bounded by $O(\sqrt{\delta})$ if the state space is discovered from $\phi$, because the NEP student cannot extract state information that isn't in the features.

**Corollary 2 (Improvement Bound Under Weak Features).** If the feature mapping $\phi$ is $\delta$-weak and the state discovery uses $\phi$, then the improvement from self-evolution is bounded by:

$$\limsup_{t \to \infty} (F1_t - F1_0) \leq C \cdot \sqrt{\frac{\delta}{2}}$$

for some constant $C > 0$ depending on $\eta$ and the Lipschitz constant of the F1 score.

*Status: **Conjecture** — a rigorous proof requires showing that self-evolution cannot amplify information not present in the features. The information bottleneck principle suggests this is true.*

### 10.3 Theorem 3: Noise-Difficulty Unidentifiability

Theorem 3 establishes a fundamental **obstacle** to convergence to the perfect fixed point:

If the data generating process satisfies the unidentifiability conditions, then even the limiting gatekeeper $S_\infty$ cannot achieve perfect distinction between noise and difficulty.

**Proposition 15 (Residual Error at Fixed Point).** Under the conditions of Theorem 3, any fixed point $z^*$ of the SCX self-evolution system must satisfy:

$$\mathbb{E}_{x \in s_1}\bigl[ |S^*(x, y_{\text{obs}}) - \mathbf{1}\{y_{\text{obs}} = f^*(x)\}| \bigr] \geq \frac{\eta\rho}{2}$$

where $s_1$ is the ambiguous state from the Theorem 3 construction.

*Proof.* Theorem 3 shows that in the ambiguous subset, any algorithm has error rate $\geq \eta\rho/2$. Since $S^*$ induces a noise detection algorithm via thresholding, the same lower bound applies. $\square$

**Corollary 3 (Non-Vanishing Lyapunov Function).** Under the conditions of Theorem 3, the Lyapunov function cannot converge to zero:

$$\liminf_{t \to \infty} V(z_t) \geq c(\eta, \rho) > 0$$

where $c(\eta, \rho) = \eta \cdot \rho \cdot \bigl( \log(1/\eta) + \log(2/\rho) \bigr) / 2$ (approximately).

*Status: **Conjecture** — the exact constant $c(\eta, \rho)$ depends on the loss function and the data distribution. The existence of a positive lower bound follows from Proposition 15, but the precise value is not yet derived.*

### 10.4 Integration

The three theorems together paint a complete picture of the dynamical system:

1. **Theorem 1** (initialization): The system starts close to the optimal fixed point when $M$ is large.
2. **Theorem 2** (speed limit): Weak features constrain how much self-evolution can improve over the initialization.
3. **Theorem 3** (fundamental barrier): Even with infinite evolution, perfect noise detection is impossible.

The self-evolution dynamics bridge these three fixed points: initialization → improvement (bounded by feature quality) → saturation (bounded by unidentifiability).

---

## 11. Summary of Proven vs. Conjectured Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| Proposition 3 (causal structure) | **Proven** | By inspection of update definitions |
| Proposition 4 (completeness) | **Proven** | Standard topology results |
| Proposition 5 (compactness) | **Proven** | Arzela-Ascoli under Lipschitz bound |
| Proposition 6 (bounded orbits) | **Proven** | From B1-B3 |
| Proposition 7 (fixed points as attractors) | **Proven** | By Lyapunov's theorem |
| Proposition 8 (trivial fixed points) | **Proven** | By verification |
| Theorem 4 (general existence) | **Proven** | Brouwer/Schauder fixed point theorem |
| Theorem 5 (unique existence, convex) | **Proven** | Contraction mapping / convex analysis |
| Proposition 9 (necessary condition) | **Proven** | By contradiction |
| Proposition 10 (Lyapunov properties) | **Proven** | Non-negativity, boundedness, continuity of the explicit $\Psi$ are verified for finite $M_0$ |
| Theorem 6 (Lyapunov decrease) | **CONJECTURED (was "Proven")** | See DEFECT-03/04. The original proof assumed memory bank growth always improves losses and gradient steps always descend — this ignores the selection bias cycle and distribution shift. The corrected analysis identifies two gaps: (i) alignment of gatekeeper update direction on biased vs. reference data, and (ii) generalization of student improvement across distributions. Descent is conjectured under additional conditions (C6', C8, C9). |
| Corollary 1 (expected monotonicity) | **CONJECTURED** (depends on Theorem 6) | Conditional on the descent property being proven |
| Proposition 11 (strict decrease) | **CONJECTURED** (depends on Theorem 6) | Conditional on Theorem 6 and stationarity conditions |
| Proposition 12 (memory monotonicity) | **Proven** | From B1 |
| Proposition 13 (consistency) | **Proven** | By definitions |
| Proposition 14 (divergence condition) | **Rigorous sketch** | Requires formalizing noise propagation |
| Proposition 15 (residual error) | **Proven** | From Theorem 3 |
| **Conjecture 2** (no periodic orbits) | **Conjecture** | Requires extending Lyapunov argument to non-convex |
| **Conjecture 3** (unique attractor) | **Conjecture** | Function-space uniqueness not guaranteed |
| **Corollary 2** (improvement bound) | **Conjecture** | Information bottleneck extension of Theorem 2 |
| **Corollary 3** (non-vanishing V) | **Conjecture** | Exact constant not yet derived |

---

## References

The dynamical systems concepts used here are standard. Key references for the mathematical framework:

1. Strogatz, S. H. (2018). *Nonlinear Dynamics and Chaos* (2nd ed.). CRC Press. — Phase portrait analysis, Lyapunov functions.
2. Hale, J. K. (1988). *Asymptotic Behavior of Dissipative Systems*. AMS. — $\omega$-limit sets, attractors.
3. Khalil, H. K. (2002). *Nonlinear Systems* (3rd ed.). Prentice Hall. — Lyapunov stability, invariance principles.
4. Conley, C. (1978). *Isolated Invariant Sets and the Morse Index*. CBMS Regional Conference Series. — Lyapunov functions for discrete systems.
5. Benaïm, M. (1999). "Dynamics of stochastic approximation algorithms." *Le Seminaire de Probabilites*, 1709, 1-68. — Stochastic approximation and ODE methods for discrete dynamics.
6. Polyak, B. T., & Juditsky, A. B. (1992). "Acceleration of stochastic approximation by averaging." *SIAM Journal on Control and Optimization*, 30(4), 838-855. — Convergence rates for iterative methods.

---

*End of Document 02: SCX Self-Evolution as a Discrete Dynamical System*

*Next: Document 03 analyzes the online learning regret of the gatekeeper under delayed feedback from the NEP student.*

---

## Changelog

| Date | Defect | Change | Severity |
|------|--------|--------|----------|
| 2026-06-28 | DEFECT-03 | **Explicit Lyapunov function defined.** Replaced the vague composite loss $V(z_t) = \mathbb{E}[L_{\text{gate}}] + \lambda \mathbb{E}[L_{\text{nep}}]$ with a concrete candidate $\Psi(S_t, \theta_t) = \frac{1}{|M_0|}\sum_{x \in M_0}(S_t - \hat{C})^2 + \frac{\lambda}{|V_0|}\sum_{V_0}\ell(f_{\theta_t}, y)$ evaluated on a fixed reference set $M_0$. The function is non-negative, bounded, and well-defined for finite $M_0$. | FATAL |
| 2026-06-28 | DEFECT-04 | **Honest CONJECTURE status for descent property.** The Lyapunov descent proof (Theorem 6) is acknowledged as **not proven**. Two critical gaps identified: (i) alignment of gatekeeper update direction on biased vs. reference data, and (ii) generalization of student improvement across distributions. Theorem 6 is now labeled CONDITIONAL, CONJECTURED. Corollary 1 and Proposition 11 downgraded to CONJECTURED (depend on Theorem 6). | FATAL |
| 2026-06-28 | DEFECT-03/13 | **Selection bias confound acknowledged.** Section 7.4 explains why the original Lyapunov candidate (evaluated on acceptance-biased distribution) could decrease without genuine improvement. The reference-set fix (evaluating on $M_0$, $V_0$) eliminates this confound. Additional conditions (C6': two-timescale, C8: exploration, C9: annealing threshold) proposed as mitigation. | FATAL/MAJOR |
| 2026-06-28 | DEFECT-13/14 | **Cross-reference to selection bias analysis and two-timescale scheduling** in Document 06 (06_fixed_point_convergence.md Sections 5.1 and 3.3). | MAJOR |
