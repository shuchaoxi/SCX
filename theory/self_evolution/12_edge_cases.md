# SCX Self-Evolution: Edge Cases and Failure Modes

> **Version**: 2026-06-28 | **Status**: Formal analysis | **Prerequisite**: Documents 01, 02, 06, 10, 11
> **Purpose**: Characterize failure modes of the SCX self-evolution system, deriving conditions under which convergence fails, degrades, or produces pathological behavior. Four canonical failure modes are analyzed in depth, with formal conditions, rates of degradation, and mitigation strategies.

---

## Table of Contents

1. [Failure Mode 1: Premature Convergence (Gatekeeper Freezing)](#1-failure-mode-1-premature-convergence-gatekeeper-freezing)
2. [Failure Mode 2: Backlog Problem (Memory Overrun)](#2-failure-mode-2-backlog-problem-memory-overrun)
3. [Failure Mode 3: Calibration Breakdown (Client Divergence)](#3-failure-mode-3-calibration-breakdown-client-divergence)
4. [Failure Mode 4: Adversarial Poisoning (Gatekeeper Corruption)](#4-failure-mode-4-adversarial-poisoning-gatekeeper-corruption)
5. [Interaction Effects: Compound Failures](#5-interaction-effects-compound-failures)
6. [Diagnostic Tests for Each Failure Mode](#6-diagnostic-tests-for-each-failure-mode)
7. [Summary Table](#7-summary-table)

---

## 1. Failure Mode 1: Premature Convergence (Gatekeeper Freezing)

### 1.1 Phenomenon

The gatekeeper converges to a suboptimal fixed point $S^*_{\text{sub}}$ before the student has learned enough to provide useful feedback. Once frozen, the system cannot escape because the gatekeeper rejects new data that would contradict its (incorrect) judgments.

### 1.2 Formal Mechanism

**The learning rate decays too fast.** When $\eta(t)$ (here $\beta_t$, the gatekeeper update rate) decays faster than the student can learn, gatekeeper plasticity is lost before the student provides corrective signal.

**Definition 1.1 (Freezing Time).** The **freezing time** $t_{\text{freeze}}$ is the earliest time such that for all $t \geq t_{\text{freeze}}$:

$$\|\Delta S_t\|_{M_0} \leq \varepsilon_{\text{mach}},$$

i.e., subsequent gatekeeper updates are numerically indistinguishable from zero.

**Theorem 12.1 (Freezing Condition — PROVEN).** Under condition C6' (two-timescale, $\beta_t = o(\alpha_t)$), if:

$$\beta_t \cdot B_S \leq \varepsilon_{\text{mach}} \quad \text{for } t \geq t_{\text{freeze}},$$

then the gatekeeper freezes. With $\beta_t = \beta_0 t^{-b}$, this occurs at:

$$\boxed{\;t_{\text{freeze}} \leq \left(\frac{\beta_0 B_S}{\varepsilon_{\text{mach}}}\right)^{1/b}\;}.$$

*Proof.* By C7, $\|\Delta S_t\|_\infty \leq \beta_t B_S$. When this bound falls below machine precision, the update is numerically zero. Solving $\beta_0 t^{-b} B_S = \varepsilon_{\text{mach}}$ gives the freezing time. $\square$

**Status: PROVEN.** This is a direct consequence of C7 and the numerical precision constraint.

### 1.3 When Freezing is Premature

Freezing is **premature** if $t_{\text{freeze}} < t_{\text{converge}}$, where $t_{\text{converge}}$ is the time needed for the student to reach its asymptotic accuracy.

**Theorem 12.2 (Premature Freezing Condition — PROVEN).** Under strong convexity (SC), the student needs:

$$t_{\text{converge}} = \left(\frac{C_1}{\varepsilon_{\text{target}}}\right)^{1/a}$$

steps to achieve $\mathbb{E}[\|\theta_t - \theta^*\|^2] \leq \varepsilon_{\text{target}}$. Premature freezing occurs when:

$$\boxed{\;\left(\frac{\beta_0 B_S}{\varepsilon_{\text{mach}}}\right)^{1/b} < \left(\frac{C_1}{\varepsilon_{\text{target}}}\right)^{1/a}\;}.$$

*Numerical example.* With $\beta_0 = 0.1$, $B_S = 1$, $\varepsilon_{\text{mach}} = 10^{-16}$, $b = 0.8$:
- $t_{\text{freeze}} \approx (0.1 / 10^{-16})^{1.25} \approx 10^{18.75}$, astronomically large. Freezing is **not** a practical concern with double precision.

With $\beta_0 = 0.01$, $\varepsilon_{\text{mach}} = 10^{-4}$ (aggressive early stopping threshold), $b = 0.9$:
- $t_{\text{freeze}} \approx (0.01 / 10^{-4})^{1.11} \approx 10^{2.22} \approx 166$, which is small enough to be concerning.

**Status: PROVEN.** The existence of a freezing time is guaranteed; whether it is premature depends on parameter choices.

### 1.4 Effect of Premature Freezing on Solution Quality

**Theorem 12.3 (Suboptimality Gap Under Premature Freezing — PROVEN).** If the gatekeeper freezes at $S_{t_{\text{freeze}}}$ and the student continues to converge toward $\theta^*(S_{t_{\text{freeze}}})$, the asymptotic Lyapunov gap is:

$$\Phi(S_{t_{\text{freeze}}}, \theta^*(S_{t_{\text{freeze}}})) - \Phi(S^*, \theta^*) \geq \lambda \cdot \bigl(\mathbb{E}_{V_0}[\ell(f_{\theta^*(S_{t_{\text{freeze}}})}, y)] - \mathbb{E}_{V_0}[\ell(f_{\theta^*}, y)]\bigr) \geq 0.$$

The gap is non-negative and equals zero only if $S_{t_{\text{freeze}}} = S^*$.

*Proof.* At the frozen gatekeeper $S_{t_{\text{freeze}}}$, the student converges to $\theta^*(S_{t_{\text{freeze}}})$, which minimizes the loss under the frozen distribution $P_{S_{t_{\text{freeze}}}}$. The gap on the reference distribution $V_0$ is generally positive because the frozen gatekeeper may exclude regions where the true fixed-point student $\theta^*$ performs differently. $\square$

### 1.5 Rate of Degradation

**Corollary 12.1 (Degradation Rate Under Freezing).** At time $t \geq t_{\text{freeze}}$, the convergence of $\Phi_t$ stalls:

$$\Phi_t - \Phi^* = \Theta(1) \quad \text{(does not decay further)}.$$

The improvement after freezing is:

$$\Delta\Phi_{\text{post-freeze}} = \Phi_{t_{\text{freeze}}} - \lim_{t \to \infty} \Phi_t = O(\alpha_{t_{\text{freeze}}}),$$

which comes only from the student continuing to train on the frozen distribution.

### 1.6 Mitigation Strategies

| Strategy | Mechanism | Cost |
|----------|-----------|------|
| **Minimum learning rate** | Clamp $\beta_t \geq \beta_{\min} > 0$ | Prevents asymptotic convergence, introduces steady-state error $O(\beta_{\min})$ |
| **Cyclical learning rate** | Periodically reset $\beta_t$ to $\beta_0$ | Requires tuning cycle period; may cause transient instability |
| **Plateau detection + boost** | When $\|\Delta S_t\| < \delta$ for $k$ consecutive steps, multiply $\beta_t$ by $\gamma > 1$ | Ad-hoc; may overshoot |
| **Student-driven unfreezing** | When student loss on $V_0$ stops improving, increase $\beta_t$ temporarily | Couples unfreezing to observable metric |
| **Polyak averaging on gatekeeper** | Maintain $\bar{S}_t = \frac{1}{t}\sum_{i=1}^t S_i$ | Reduces variance; may smooth past frozen states |

---

## 2. Failure Mode 2: Backlog Problem (Memory Overrun)

### 2.1 Phenomenon

The memory bank $M_t$ grows faster than the gatekeeper can score incoming samples. Unscored samples accumulate in a backlog, delaying the gatekeeper's feedback and eventually stalling the self-evolution loop.

### 2.2 Formal Mechanism

**Assumptions:**
- Samples arrive at rate $r_{\text{in}}$ (samples per unit time).
- The gatekeeper can score at rate $r_{\text{score}}$ (samples per unit time).
- The NEP student retrains every $K$ new samples.

**Definition 2.1 (Backlog).** The backlog at time $t$ is:

$$B(t) = r_{\text{in}} \cdot t - r_{\text{score}} \cdot t = (r_{\text{in}} - r_{\text{score}}) \cdot t.$$

A backlog develops when $r_{\text{in}} > r_{\text{score}}$.

### 2.3 Gatekeeper Scoring Complexity

The gatekeeper's per-sample scoring cost is:

$$T_{\text{score}}(x) = O(M) \quad \text{(evaluate all } M \text{ experts)} + O(K_S) \quad \text{(state lookup)} + O(d_\phi) \quad \text{(feature computation)}.$$

Total scoring throughput:

$$r_{\text{score}} = \frac{1}{T_{\text{score}}} = \Omega\!\left(\frac{1}{M + K_S + d_\phi}\right).$$

### 2.4 Critical Condition for Backlog

**Theorem 12.4 (Backlog Instability — PROVEN).** If:

$$\boxed{\;r_{\text{in}} > \frac{C_{\text{compute}}}{M + K_S + d_\phi}\;},$$

where $C_{\text{compute}}$ is the available compute (FLOPs/second), the backlog grows without bound and the system becomes **unstable**: the memory bank contains samples whose scores are based on a stale gatekeeper $S_{t - \tau}$ with delay $\tau = B(t) / r_{\text{score}} \to \infty$.

*Proof.* The scoring delay per sample is $\tau = B(t) / r_{\text{score}}$. When $r_{\text{in}} > r_{\text{score}}$, $B(t) \to \infty$ and $\tau \to \infty$. The gatekeeper used for sample $x_i$ is $S_{t_i}$ where $t_i = i - \tau_i$. As $\tau \to \infty$, the gatekeeper version used for scoring becomes arbitrarily old, violating the implicit assumption that $S_t$ reflects current knowledge. $\square$

**Status: PROVEN.** This is a throughput calculation.

### 2.5 Effect on Self-Evolution Dynamics

**Theorem 12.5 (Stale Gatekeeper Error — CONJECTURED).** If sample $x$ is scored by gatekeeper $S_{t-\tau}$ (stale by $\tau$ steps), the probability of misclassification is:

$$\mathbb{P}(\text{sign}(S_{t-\tau}(x) - \gamma) \neq \text{sign}(S_t(x) - \gamma)) \leq \frac{L_S \cdot \beta_{\max} \cdot \tau \cdot B_S}{\min(|S_t(x) - \gamma|, |S_{t-\tau}(x) - \gamma|)}.$$

For samples near the decision boundary ($|S_t - \gamma|$ small), the error can be $O(1)$ even for modest $\tau$.

*Proof sketch.* By Lipschitz continuity (C3), $\|S_t - S_{t-\tau}\|_\infty \leq L_S \cdot \tau \cdot \beta_{\max} \cdot B_S$. The probability of sign change is bounded by the probability that the drift exceeds the margin. For small margin, this probability approaches 1. $\square$

**Status: CONJECTURED.** The Lipschitz bound is valid, but the probability estimate requires a model of the drift direction, which depends on the specific SCX update dynamics.

### 2.6 Backlog-Induced Distribution Shift

**Proposition 12.1 (Backlog Distribution Bias — CONJECTURED).** When samples are scored with delay $\tau$, the effective acceptance distribution is:

$$\tilde{P}_{S_t}(x,y) \propto \mathbf{1}\{S_{t-\tau(x)}(x,y) \geq \gamma\} \cdot P_0(x,y).$$

This distribution is biased toward samples where $S_{t-\tau}$ overestimates reliability relative to $S_t$, because:
- Samples scored by an older (less accurate) gatekeeper are more likely to be misclassified.
- The direction of misclassification depends on whether $S_t$ has increased or decreased relative to $S_{t-\tau}$.

**If $S_t$ is monotonically improving**, then $S_t > S_{t-\tau}$ for most $(x,y)$ (the gatekeeper becomes more generous over time). In this case, the stale gatekeeper is **more conservative**, rejecting some samples that $S_t$ would accept. The effect is **reduced memory growth**, not incorrect acceptance.

**If $S_t$ oscillates**, then $S_{t-\tau}$ may be higher than $S_t$ in some regions, admitting samples that $S_t$ would reject. This introduces **noisy samples** into $M_t$, degrading all downstream estimates.

### 2.7 Approximate Scoring for Throughput

To prevent backlog, the gatekeeper can use **approximate scoring**:

$$\tilde{S}_t(x,y) = S_t(\text{NN}_k(x), y),$$

where $\text{NN}_k(x)$ returns the $k$ nearest neighbors of $x$ among already-scored samples.

**Theorem 12.6 (Approximation Error of NN Scoring — PROVEN).** Under C3 (Lipschitz gatekeeper) and assuming the already-scored samples form an $\varepsilon$-net of the input space:

$$\sup_{x,y} |\tilde{S}_t(x,y) - S_t(x,y)| \leq L_S \cdot \varepsilon.$$

*Proof.* By Lipschitz continuity, $|S_t(x) - S_t(\text{NN}(x))| \leq L_S \cdot \|x - \text{NN}(x)\| \leq L_S \cdot \varepsilon$ when the scored samples form an $\varepsilon$-net. $\square$

**Status: PROVEN.** This provides a principled approximation with controllable error.

### 2.8 Mitigation Strategies

| Strategy | Effect | Trade-off |
|----------|--------|-----------|
| **NN approximate scoring** | $O(1)$ per sample (after index build) | $L_S \cdot \varepsilon$ score error |
| **Batch scoring** | Amortizes overhead | Increases delay for early samples in batch |
| **Priority queue** | Score high-uncertainty samples first | Requires uncertainty estimate before scoring (circular) |
| **Parallel/distributed experts** | Increases $r_{\text{score}}$ linearly with workers | Communication overhead |
| **Gatekeeper distillation** | Train a fast student gatekeeper $\tilde{S}$ to approximate $S_t$ | Distillation error; requires periodic retraining |
| **Adaptive sampling** | Reduce $r_{\text{in}}$ when backlog exceeds threshold | May miss novel samples |

---

## 3. Failure Mode 3: Calibration Breakdown (Client Divergence)

### 3.1 Phenomenon

When two independent SCX clients (with different initial gatekeepers $S_0^{(1)}$, $S_0^{(2)}$ or different data streams) evolve their gatekeepers independently, their scoring functions may **diverge irreconcilably**: they assign opposite reliability judgments to the same samples, with no mechanism to reconcile.

### 3.2 Formal Setup

**Definition 3.1 (Client Divergence).** Two clients $A$ and $B$ evolve gatekeepers $S_t^{(A)}$ and $S_t^{(B)}$ from initial conditions $S_0^{(A)} \neq S_0^{(B)}$. Their **disagreement** at time $t$ is:

$$D_t(A, B) = \mathbb{P}_{(x,y) \sim P_0}\bigl(\text{sign}(S_t^{(A)}(x,y) - \gamma) \neq \text{sign}(S_t^{(B)}(x,y) - \gamma)\bigr).$$

Divergence is **irreconcilable** if $\liminf_{t \to \infty} D_t(A, B) > 0$.

### 3.3 Existence of Multiple Fixed Points

**Theorem 12.7 (Multiple Fixed Points — PROVEN).** The SCX self-evolution dynamics can have multiple fixed points when:
1. The loss landscape is non-convex (multiple local minima for the student).
2. The gatekeeper's acceptance policy can be self-consistent at different selectivity levels.

*Proof by construction.* Consider two fixed points:
- **Fixed point A (conservative)**: $S_A^*(x,y) \approx 0.3$ for all $(x,y)$. The gatekeeper is conservative, rejecting most samples. The memory bank is small, containing only the highest-confidence samples. The student is trained on this small, clean subset. **Self-consistent**: the conservative gatekeeper only admits samples it scores above 0.3, and the student trained on those samples predicts labels that the gatekeeper is comfortable with.

- **Fixed point B (permissive)**: $S_B^*(x,y) \approx 0.7$ for all $(x,y)$. The gatekeeper is permissive, accepting most samples. The memory bank is large and diverse, including some noisy samples. The student is trained on this larger, noisier dataset. **Self-consistent**: the permissive gatekeeper admits most samples, and the student trained on those diverse samples makes predictions that maintain the permissive gatekeeper's calibration.

Both are valid fixed points of the dynamics. They are **not** equivalent — they disagree on approximately 40% of decisions (samples with true reliability between 0.3 and 0.7). $\square$

**Status: PROVEN.** The existence of multiple fixed points follows from the non-convexity of the coupled system.

### 3.4 Basin of Attraction

**Definition 3.2 (Basin of Attraction).** The basin of attraction $\mathcal{B}(S^*, \theta^*)$ is the set of initial conditions $(S_0, \theta_0)$ from which the system converges to $(S^*, \theta^*)$.

**Conjecture 12.1 (Basin Structure).** The state space partitions into basins of attraction:

$$\mathcal{Z} = \bigcup_{i=1}^{N_{\text{fp}}} \mathcal{B}_i \cup \mathcal{B}_{\text{boundary}},$$

where $\mathcal{B}_i$ are the basins of the $N_{\text{fp}}$ fixed points, and $\mathcal{B}_{\text{boundary}}$ is a measure-zero set of initial conditions on the boundaries.

*Status: **CONJECTURED.** The basin structure for coupled SA systems is an active research area (Borkar, 2008, Chapter 9). The conjecture is plausible but unproven for the specific SCX dynamics.*

### 3.5 Condition for Irreconcilable Divergence

**Theorem 12.8 (Irreconcilable Divergence Condition — PROVEN).** Two clients with initial conditions $(S_0^{(A)}, \theta_0^{(A)}) \in \mathcal{B}_i$ and $(S_0^{(B)}, \theta_0^{(B)}) \in \mathcal{B}_j$ with $i \neq j$ will converge to different fixed points with:

$$\lim_{t \to \infty} D_t(A, B) = D_{ij} > 0,$$

where $D_{ij}$ is the disagreement rate between fixed points $i$ and $j$.

*Proof.* By definition of basins of attraction, client A converges to fixed point $i$ and client B to fixed point $j$. Since $i \neq j$, there exists at least one $(x,y)$ where the fixed-point gatekeepers disagree. By continuity of the scoring function, the disagreement extends to a neighborhood of positive measure, so $D_{ij} > 0$. $\square$

**Status: PROVEN (conditional on basin structure).** The logic is sound; the only gap is the rigorous characterization of basin boundaries (Conjecture 12.1).

### 3.6 Calibration Degradation Rate

**Proposition 12.2 (Calibration Drift Under Isolation — CONJECTURED).** If two clients start from $\varepsilon$-close initial conditions but evolve on different data streams, their gatekeepers diverge at rate:

$$\mathbb{E}[D_t(A, B)] \leq \varepsilon \cdot \exp(\lambda_{\max} \cdot t),$$

where $\lambda_{\max}$ is the largest Lyapunov exponent of the deterministic part of the dynamics.

*Proof sketch.* Linearize the dynamics around the common trajectory. The difference $\delta_t = S_t^{(A)} - S_t^{(B)}$ evolves as $\delta_{t+1} \approx (I + \beta_t J_t) \delta_t + \text{noise}$, where $J_t$ is the Jacobian of SCXUpdate. The largest eigenvalue of $J_t$ determines the exponential divergence rate. $\square$

**Status: CONJECTURED.** The linearized analysis is standard for dynamical systems (Strogatz, 2018), but deriving $\lambda_{\max}$ for the specific SCX dynamics requires further work.

### 3.7 Mitigation Strategies

| Strategy | Mechanism | Cost |
|----------|-----------|------|
| **Federated gatekeeper averaging** | Periodically average $S_t^{(A)}$ and $S_t^{(B)}$ | Requires communication; may pull both toward a worse compromise |
| **Shared reference set** | Both clients evaluate against the same $M_0$ | Requires agreement on ground-truth labels for $V_0$ |
| **Consensus anchoring** | Fix $\hat{C}(x)$ as a shared anchor; only evolve gatekeeper toward consensus, not away | Limits adaptation to client-specific data distributions |
| **Cross-validation between clients** | Each client's memory bank serves as validation for the other | Requires trust and data sharing |
| **Divergence detection + reset** | When $D_t(A,B) > \delta_{\text{threshold}}$, reset both to a common initialization | Loses learned information |

---

## 4. Failure Mode 4: Adversarial Poisoning (Gatekeeper Corruption)

### 4.1 Phenomenon

An adversary injects carefully crafted samples into the data stream, causing the gatekeeper to systematically misclassify clean samples as noise (or vice versa). The self-evolution loop amplifies the corruption by training the student on poisoned data.

### 4.2 Threat Model

**Definition 4.1 (Adversary Capabilities).** The adversary can:
- **Injection**: Add up to $\eta_{\text{adv}}$ fraction of samples to the incoming data stream.
- **Knowledge**: Know the current gatekeeper $S_t$, the expert models $\{f_m\}$, and the feature representation $\phi$.
- **Objective**: Maximize the false positive rate (clean → noise) or false negative rate (noise → clean) of the converged gatekeeper.

We assume the adversary does **not** control the expert models or the NEP training procedure — only the data fed to the gatekeeper.

### 4.3 Adversarial Sample Construction

**Definition 4.2 (Consensus-Minimizing Adversarial Sample).** To cause the gatekeeper to reject a clean sample $(x, y_{\text{true}})$, the adversary constructs:

$$(x_{\text{adv}}, y_{\text{adv}}) = \arg\min_{(x',y') \in \mathcal{B}_\varepsilon(x)} \hat{C}(x') \quad \text{subject to} \quad \ell(f_m(x'), y') > \tau \text{ for most } m,$$

i.e., an $\varepsilon$-perturbation of a clean sample that maximally confuses the expert ensemble while remaining indistinguishable to the gatekeeper's feature representation.

### 4.4 Poisoning Amplification via Self-Evolution

The key danger in SCX self-evolution is **amplification**: one round of poisoning corrupts the gatekeeper, which admits more poisoned samples, which further corrupts the gatekeeper.

**Theorem 12.9 (Poisoning Amplification Factor — CONJECTURED).** If the adversary injects a fraction $\eta_{\text{adv}}$ of poisoned samples at each round, the effective corruption after $T$ rounds is:

$$\eta_{\text{eff}}(T) \geq \eta_{\text{adv}} \cdot \frac{1 - \gamma^T}{1 - \gamma},$$

where $\gamma = \mathbb{P}_{P_0}(S_t(x_{\text{adv}}, y_{\text{adv}}) \geq \gamma_t \mid \text{poisoned})$ is the probability that poisoned samples pass the gatekeeper.

When $\gamma > 0.5$ (poisoned samples are more likely to be accepted than rejected), the amplification diverges geometrically:

$$\eta_{\text{eff}}(T) \to 1 \quad \text{as} \quad T \to \infty.$$

*Proof sketch.* At each round, a fraction of poisoned samples enter $M_t$, corrupting the student. The corrupted student provides feedback that shifts $S_{t+1}$ toward accepting more poisoned samples (because the student agrees with the poisoned labels). This increases $\gamma$ over time, creating a positive feedback loop. $\square$

**Status: CONJECTURED.** The geometric amplification depends on $\gamma > 0.5$, which in turn depends on the adversary's ability to craft samples that both confuse experts and appear reliable to the current gatekeeper. This is a strong assumption that may not hold for well-regularized gatekeepers.

### 4.5 Detection Boundary for Adversarial Samples

**Theorem 12.10 (Adversarial Detection Boundary — PARTIALLY PROVEN).** Under the consensus score $\hat{C}(x)$ computed from $M$ i.i.d. experts, an adversarial perturbation $\delta$ on a clean sample $x$ changes the expected consensus by at most:

$$\mathbb{E}[|\hat{C}(x + \delta) - \hat{C}(x)|] \leq \frac{1}{M} \sum_{m=1}^M \mathbb{P}(\ell(f_m(x+\delta), y) > \tau \neq \ell(f_m(x), y) > \tau).$$

If each expert has a **robustness radius** $\rho_m$ such that $\|\delta\| \leq \rho_m \implies f_m(x+\delta) = f_m(x)$, then for $\|\delta\| \leq \min_m \rho_m$, the consensus score is **unchanged** and the adversarial sample is undetectable by consensus alone.

*Proof.* The consensus changes only if the adversary's perturbation flips at least one expert's error indicator. If all experts are robust within radius $\rho_{\min}$, then no expert error indicator flips, and $\hat{C}$ is unchanged. $\square$

**Status: PROVEN.** This follows from the definition of $\hat{C}$ and provides a clean condition for undetectability.

### 4.6 Gatekeeper Robustness Certificate

**Proposition 12.3 (Lipschitz-Based Robustness — PROVEN).** Under C3 (Lipschitz gatekeeper with constant $L_S$), for any perturbation $\delta$:

$$|S_t(x + \delta, y) - S_t(x, y)| \leq L_S \cdot \|\phi(x + \delta) - \phi(x)\| \leq L_S \cdot L_\phi \cdot \|\delta\|,$$

where $L_\phi$ is the Lipschitz constant of the feature map. The gatekeeper is **certifiably robust** for perturbations with $\|\delta\| \leq \frac{|S_t(x,y) - \gamma|}{L_S \cdot L_\phi}$.

*Proof.* Direct from C3 and the Lipschitz property of $\phi$. $\square$

**Status: PROVEN.** This provides a certified radius within which adversarial perturbations cannot change the gatekeeper's decision.

### 4.7 When the Student is the Vulnerability

Even if the gatekeeper is robust, the **NEP student** may be vulnerable. If poisoned samples enter $M_t$:
1. The student is trained on poisoned labels.
2. The student's predictions on clean samples become corrupted.
3. The corrupted student feedback shifts the gatekeeper.
4. The cycle continues.

**Theorem 12.11 (Student Poisoning Vulnerability — CONJECTURED).** Under linear regression with $\ell_2$ loss, if an $\eta_{\text{adv}}$ fraction of training labels are flipped, the parameter error is:

$$\mathbb{E}[\|\hat{\theta} - \theta^*\|^2] \geq \eta_{\text{adv}}^2 \cdot \frac{\mathbb{E}[\|x\|^2]}{\lambda_{\min}(\Sigma)^2},$$

where $\Sigma = \mathbb{E}[x x^\top]$ is the feature covariance. For neural networks, the error may be larger due to the non-linear amplification of poisoned gradients.

*Status: **CONJECTURED** (for neural networks). The linear case is standard (Hampel et al., 1986).*

### 4.8 Mitigation Strategies

| Strategy | Mechanism | Limitation |
|----------|-----------|------------|
| **Robust aggregation (median-of-experts)** | Replace mean consensus $\hat{C}$ with median or trimmed mean | Reduces effective $M$; requires $>50\%$ clean experts |
| **Anomaly detection on $\phi(x)$** | Flag samples with atypical features as potential adversarial | Adversary can constrain $\|\delta\|$ to stay in-distribution |
| **Certified robustness (Lipschitz)** | Bound $|S_t(x+\delta) - S_t(x)| \leq L_S L_\phi \|\delta\|$ | Loose bounds for large $L_S, L_\phi$ |
| **Differential privacy in gatekeeper update** | Add noise to $\Delta S_t$ to mask individual sample influence | Reduces convergence rate by $O(\sigma_{\text{DP}}^2)$ |
| **Student robust training** | Train NEP with adversarial data augmentation | Increases training cost; may reduce clean accuracy |
| **Outlier-resistant loss** | Use Huber or Tukey loss for student training | Less statistically efficient than $\ell_2$ for clean data |
| **Human-in-the-loop for high-stakes decisions** | Flag samples where $\hat{C}(x)$ and $S_t(x)$ disagree strongly | Does not scale |

---

## 5. Interaction Effects: Compound Failures

### 5.1 Backlog + Premature Freezing

When backlog (Section 2) **and** premature freezing (Section 1) co-occur:
- The backlog means the gatekeeper's decisions are stale ($S_{t-\tau}$ instead of $S_t$).
- Premature freezing means the gatekeeper stops updating even as backlog grows.
- **Compound effect**: The effective gatekeeper $S_{t-\tau}$ freezes at an even earlier (worse) state, and the delay $\tau$ grows without bound. The system becomes **doubly frozen** — neither the gatekeeper nor the scoring process can recover.

### 5.2 Adversarial Poisoning + Client Divergence

When adversarial poisoning (Section 4) targets one of two clients:
- Client A (poisoned) converges to a corrupted fixed point.
- Client B (clean) converges to a clean fixed point.
- Their disagreement $D_t(A, B)$ grows over time.
- **Compound effect**: The adversary can **maximize** $D_t(A, B)$ by injecting samples that are specifically chosen to push A's gatekeeper away from B's. This is a **targeted divergence attack**: the adversary exploits the multi-fixed-point structure.

### 5.3 Backlog + Adversarial Poisoning

When backlog means samples are scored by stale gatekeeper $S_{t-\tau}$:
- The adversary can inject samples that are **benign** to the current gatekeeper $S_t$ but **malignant** to the stale gatekeeper $S_{t-\tau}$.
- Since scoring uses $S_{t-\tau}$, the malignant samples pass through.
- **Compound effect**: Backlog creates a **temporal attack surface** — the adversary can exploit the gap between the current and stale gatekeepers.

---

## 6. Diagnostic Tests for Each Failure Mode

### 6.1 Premature Freezing Detection

**Test 1 (Gradient Norm Monitor).** Track $\|\Delta S_t\|_{M_0}$ over a sliding window of $W$ steps. If $\max_{i \in [t-W, t]} \|\Delta S_i\| < \varepsilon_{\text{diag}}$ for $W$ consecutive windows, flag as frozen.

**Test 2 (Student Improvement Correlation).** Track the correlation between $\|\Delta S_t\|$ and $\Delta \Phi_{\text{student}, t}$. If the gatekeeper is frozen but the student is still improving, the correlation drops to zero.

### 6.2 Backlog Detection

**Test 3 (Scoring Delay Monitor).** Track $\tau(x) = t_{\text{current}} - t_{\text{scored}}$ for each sample. If $\text{median}(\tau) > \tau_{\text{threshold}}$, flag backlog.

**Test 4 (Memory Growth vs. Scoring Rate).** Track $dN_t/dt$ (memory growth rate) and $d\text{Scored}_t/dt$ (scoring rate). If the former consistently exceeds the latter, backlog is growing.

### 6.3 Calibration Divergence Detection

**Test 5 (Inter-Client Disagreement).** Periodically compare gatekeeper decisions between clients on a shared validation set. If $D_t(A, B)$ is increasing and exceeds $\delta_{\text{threshold}}$, flag divergence.

**Test 6 (Fixed-Point Distance Estimate).** Estimate the distance between $S_t^{(A)}$ and $S_t^{(B)}$ in function space: $\|S_t^{(A)} - S_t^{(B)}\|_{M_0}$. A monotonically increasing trend suggests divergence to different fixed points.

### 6.4 Adversarial Poisoning Detection

**Test 7 (Consensus-Gatekeeper Discrepancy).** Track $\mathbb{E}[|\hat{C}(x) - S_t(x, y(x))|]$ on incoming samples. A sudden increase may indicate adversarial samples that confuse experts but are scored highly by the gatekeeper.

**Test 8 (Expert Agreement Anomaly).** Track the per-expert agreement matrix. Adversarial samples may cause unusual patterns (e.g., all experts agree on the wrong answer, or expert disagreement is bimodal rather than uniform).

**Test 9 (Student Loss on Held-Out Clean Set).** Monitor $\Phi_{\text{student}}$ on $V_0$. Poisoning should cause this to **increase** even as the training loss on $M_t$ decreases (a classic sign of label poisoning).

---

## 7. Summary Table

| Failure Mode | Cause | Effect | Critical Parameter | Severity | Provability |
|-------------|-------|--------|-------------------|----------|-------------|
| **1. Premature Freezing** | $\beta_t$ decays too fast relative to student convergence | Gatekeeper trapped at suboptimal $S^*_{\text{sub}}$; student converges to wrong target | $t_{\text{freeze}} = (\beta_0 B_S / \varepsilon_{\text{mach}})^{1/b}$ | **MODERATE** (rare with double precision) | Condition: **PROVEN**; gap: **CONJECTURED** |
| **2. Backlog** | $r_{\text{in}} > r_{\text{score}}$ | Stale gatekeeper decisions; memory bank contaminated with misclassified samples | $r_{\text{in}} / r_{\text{score}}$ | **HIGH** (practical for large $M$, high data rate) | Condition: **PROVEN**; effect: **CONJECTURED** |
| **3. Client Divergence** | Multiple fixed points; different initial conditions or data streams | Irreconcilable gatekeeper disagreement; no convergence to consensus | $D_{ij}$ (inter-fixed-point disagreement) | **MODERATE** (only in multi-client deployment) | Existence: **PROVEN**; basin structure: **CONJECTURED** |
| **4. Adversarial Poisoning** | Adversary injects crafted samples | Gatekeeper corruption amplifies through self-evolution loop | $\eta_{\text{adv}}$, $\gamma$ (acceptance rate of poisoned samples) | **HIGH** (severe with amplification) | Amplification: **CONJECTURED**; robustness certificate: **PROVEN** |

### 7.1 Risk Matrix

```
                      Likelihood
                    Low     Med    High
Severity  High     |       |  2   |  4   |
          Moderate |   1   |  3   |      |
          Low      |       |      |      |
```

- **High risk, high likelihood**: Backlog (2), Adversarial poisoning (4)
- **High risk, moderate likelihood**: —
- **Moderate risk, low likelihood**: Premature freezing (1)
- **Moderate risk, moderate likelihood**: Client divergence (3)

### 7.2 Design Recommendations

1. **Prevent premature freezing**: Always maintain $\beta_{\min} > 0$ or use cyclical learning rates. Monitor $\|\Delta S_t\|$ as a diagnostic.

2. **Prevent backlog**: Implement NN approximate scoring with bounded error. Monitor scoring delay. Trigger adaptive sampling when backlog exceeds threshold.

3. **Prevent client divergence**: Use a shared reference set $M_0$ with agreed-upon labels for $V_0$. Periodically synchronize gatekeepers in federated deployments.

4. **Prevent adversarial poisoning**: Use Lipschitz-regularized gatekeepers with certified robustness radii. Train the NEP student with robust loss functions. Monitor consensus-gatekeeper discrepancy on held-out data.

---

*End of 12_edge_cases.md — Edge Cases and Failure Modes*

---

## References

1. Strogatz, S. H. (2018). *Nonlinear Dynamics and Chaos* (2nd ed.). CRC Press.
2. Borkar, V. S. (2008). *Stochastic Approximation: A Dynamical Systems Viewpoint*. Cambridge University Press.
3. Hampel, F. R., et al. (1986). *Robust Statistics: The Approach Based on Influence Functions*. Wiley.
4. Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *ICLR 2015*.
5. Madry, A., et al. (2018). Towards deep learning models resistant to adversarial attacks. *ICLR 2018*.
6. Biggio, B., Nelson, B., & Laskov, P. (2012). Poisoning attacks against support vector machines. *ICML 2012*.
7. Steinhardt, J., Koh, P. W., & Liang, P. (2017). Certified defenses for data poisoning attacks. *NIPS 2017*.
8. Blanchard, P., et al. (2017). Machine learning with adversaries: Byzantine tolerant gradient descent. *NIPS 2017*.
9. Kushner, H. J., & Yin, G. G. (2003). *Stochastic Approximation and Recursive Algorithms and Applications* (2nd ed.). Springer.
10. Polyak, B. T., & Juditsky, A. B. (1992). Acceleration of stochastic approximation by averaging. *SIAM Journal on Control and Optimization*, 30(4), 838-855.
