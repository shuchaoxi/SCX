# SCX Self-Evolution: Symbol System and Problem Setup

> **Version**: 2026-06-28 | **Status**: Foundational | **Audit**: Pre-verification
> **Purpose**: Define notation, problem structure, and formal setup for the SCX self-evolution framework.
> **Relationship to existing theory**: Extends the notation of THEOREMS_UNIFIED.md (Sections 0.1-0.2) into the self-evolution regime.

---

## Table of Contents

1. [Introduction and Scope](#1-introduction-and-scope)
2. [Preliminary: Inherited Notation from Core SCX Theory](#2-preliminary-inherited-notation-from-core-scx-theory)
3. [New Objects for Self-Evolution](#3-new-objects-for-self-evolution)
4. [Structure Space X](#4-structure-space-x)
5. [Evolution State Space](#5-evolution-state-space)
6. [Scoring Function S_t](#6-scoring-function-s_t)
7. [Memory Bank M_t](#7-memory-bank-m_t)
8. [NEP Student f_theta_t](#8-nep-student-f_theta_t)
9. [Update Operator Phi](#9-update-operator-phi)
10. [Loss Functions](#10-loss-functions)
11. [Evaluation Metrics](#11-evaluation-metrics)
12. [Relationship to Existing Definitions](#12-relationship-to-existing-definitions)
13. [Assumption Catalog for Self-Evolution (B1-B6)](#13-assumption-catalog-for-self-evolution-b1-b6)
14. [Summary of Notation](#14-summary-of-notation)

---

## 1. Introduction and Scope

The SCX self-evolution framework extends the static SCX noise detection pipeline into a closed-loop learning system. In the static setting (Theorem 1-6 of the core theory), the gatekeeper function $S$ is fixed after initial training, and the expert models $\{f_m\}_{m=1}^M$ remain static. In the self-evolution setting, the gatekeeper iteratively refines its scoring function, accumulates a memory bank, and trains a student model (NEP) that provides delayed feedback.

The core iteration is:

$$\text{judge} \;\to\; \text{store} \;\to\; \text{update SCX} \;\to\; \text{re-judge} \;\to\; \text{re-update} \;\to\; \dots$$

This document formalizes the objects, spaces, and assumptions needed to analyze this dynamics. Subsequent documents study the dynamical system properties (Document 02) and the online learning regret (Document 03).

---

## 2. Preliminary: Inherited Notation from Core SCX Theory

We inherit the following from THEOREMS_UNIFIED.md. Any symbol not redefined below retains its meaning from the core theory.

| Symbol | Meaning | Reference |
|--------|---------|-----------|
| $\mathcal{X}$ | Input space | Thm 1-6 |
| $\mathcal{Y}$ | Label space, $|\mathcal{Y}| = K_{\mathcal{Y}}$ | Thm 1, 3 |
| $\mathcal{S}$ | State space (index set), $|\mathcal{S}| = K_{\mathcal{S}}$ | Thm 1-6 |
| $s(x): \mathcal{X} \to \mathcal{S}$ | True state assignment | Thm 1-6 |
| $f^*: \mathcal{X} \to \mathcal{Y}$ | True oracle (unobserved) | Thm 1, 3 |
| $\{f_m\}_{m=1}^M$ | Expert models, $M$ experts | Thm 1-6 |
| $\ell: \mathcal{Y} \times \mathcal{Y} \to [0,B]$ | Bounded loss, $B < \infty$ | Thm 1 |
| $\tau > 0$ | Expert error threshold | Thm 1 |
| $e_m(x,y) = \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ | Expert error indicator | Thm 1 |
| $C(x) = \frac{1}{M}\sum_{m=1}^M e_m(x,y)$ | Consensus score | Thm 1 |
| $\eta$ | Global noise rate | Thm 1-4' |
| $\rho_s = \mathbb{P}(X \in s)$ | State probability | Thm 1 |
| $\mu_s$ | State-$s$ clean error upper bound | Thm 1 |
| $R_m(s)$ | State-conditioned expert risk | Tech report |
| $\text{SCX}_m(s)$ | Reliability score $\mathbb{P}(\ell(f_m(x), y) < \tau \mid x \in s)$ | Tech report |
| $\hat{s}(x)$ | Estimated state assignment | Thm 2, 5 |
| $\phi: \mathcal{X} \to \mathbb{R}^{d_\phi}$ | Feature representation | Thm 2, 5 |
| $\theta$ (detection) | Detection threshold (static setting) | Thm 1, 4' |

> **Notation warning (B3 fix — cross-reference):** $\mathcal{S}$ (calligraphic) denotes the **state space** (a finite index set). $S_t$ (italic with time subscript $t$) denotes the **gatekeeper scoring function** $S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]$ at time $t$, defined in §6. These are entirely distinct objects. In the core SCX theory (Theorems 1-3), $S$ refers to the state random variable; in self-evolution docs, $S_t$ refers to the evolving gatekeeper. **Context disambiguates**: $\mathcal{S}$ = state space; $S_t$ = gatekeeper at time $t$.

---

## 3. New Objects for Self-Evolution

The self-evolution framework introduces the following new objects:

| Symbol | Name | Definition |
|--------|------|------------|
| $\mathcal{X}$ | Structure space | All possible SCX configurations (Section 4) |
| $S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]$ | Gatekeeper scoring function at time $t$ | Section 6 |
| $M_t$ | Memory bank at time $t$ | Section 7 |
| $f_{\theta_t}: \mathcal{X} \to \mathcal{Y}$ | NEP student with parameters $\theta_t$ | Section 8 |
| $\Phi$ | Update operator | Section 9 |
| $L_{\text{gate}}$ | Gatekeeper loss | Section 10 |
| $L_{\text{nep}}$ | NEP student loss | Section 10 |

**Time index convention**: $t = 0, 1, 2, \dots$ indexes discrete evolution rounds. $t=0$ is the initialization round (before any self-evolution). Time advances forward as the loop executes.

---

## 4. Structure Space $\mathcal{X}$

### 4.1 Definition

Let $\mathcal{X}$ denote the **structure space**: the set of all feasible SCX configurations over the input space $\mathcal{X}_0$, label space $\mathcal{Y}$, and state space $\mathcal{S}$.

**Definition 1 (Structure Space).** A configuration $x \in \mathcal{X}$ is a tuple:

$$x = \bigl( \mathcal{X}_0, \mathcal{Y}, \mathcal{S}, s(\cdot), \{f_m\}_{m=1}^M, \phi(\cdot), \hat{s}(\cdot), \ell, \tau \bigr)$$

where each component satisfies the standard SCX definitions from THEOREMS_UNIFIED.md Section 0.1.

**Remarks:**
- The structure space is a product of function spaces: $\mathcal{X} = \mathcal{P}(\mathcal{X}_0) \times \mathcal{P}(\mathcal{Y}) \times \cdots$ (abusing notation for the Cartesian product of the component spaces).
- In practice, we never enumerate $\mathcal{X}$ explicitly; we reason about the **support** of the data distribution's structural parameters.
- The key structural variable for the self-evolution analysis is the pair $(\mathcal{S}, s(\cdot))$ (the state partition) because errors in state discovery propagate to all downstream estimates.

### 4.2 Metric on Structure Space

For theoretical analysis, we endow $\mathcal{X}$ with a metric induced by the total variation distance between the implied consensus score distributions.

**Definition 2 (Structure Metric).** For two configurations $x, x' \in \mathcal{X}$, define:

$$d_{\mathcal{X}}(x, x') = \sup_{A \subseteq \mathcal{X}_0} \bigl| \mathbb{P}_{X \sim P_x}(C(X) \in A) - \mathbb{P}_{X \sim P_{x'}}(C(X) \in A) \bigr|$$

where $P_x$ is the implied distribution of $(X, Y, \{f_m\})$ under configuration $x$.

This metric captures the notion that two structures are "close" if they induce similar consensus score distributions. It is relevant for analyzing how small changes in the structure (e.g., updated state estimates) affect gatekeeper decisions.

---

## 5. Evolution State Space

### 5.1 Definition

The **evolution state** at time $t$ is the triple representing the complete system state:

$$z_t = (S_t, M_t, \theta_t) \in \mathcal{Z}$$

where $\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$ is the evolution state space, with:

- $\mathcal{F}$: space of measurable functions $\mathcal{X}_0 \times \mathcal{Y} \to [0,1]$ (all possible gatekeeper scoring functions)
- $\mathcal{M}$: space of finite labeled datasets (all possible memory banks)
- $\Theta \subseteq \mathbb{R}^{d_\theta}$: parameter space for the NEP student

### 5.2 Topology on $\mathcal{F}$

We equip $\mathcal{F}$ with the topology of pointwise convergence, equivalently the product topology. For analysis, the relevant metric is:

**Definition 3 (Gatekeeper Metric).** For $S, S' \in \mathcal{F}$:

$$d_{\mathcal{F}}(S, S') = \mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ |S(x,y) - S'(x,y)| \bigr]$$

where $\mathcal{D}$ is the data distribution.

This metric captures the average disagreement between two scoring functions. Under standard regularity conditions (e.g., $S$ is Lipschitz in its parameters), $d_{\mathcal{F}}$ is equivalent to the $L^1(\mathcal{D})$ distance.

### 5.3 Topology on $\mathcal{M}$

The memory bank $M_t$ is a finite multiset. We equip $\mathcal{M}$ with the metric induced by the Hausdorff distance on the feature-label-confidence space:

**Definition 4 (Memory Metric).** For $M, M' \in \mathcal{M}$ with $|M| = N$, $|M'| = N'$, suppose $N = N'$ (balanced case). Define:

$$d_{\mathcal{M}}(M, M') = \frac{1}{N} \sum_{i=1}^N \bigl\| \psi(x_i, y_i, v_i, c_i) - \psi(x'_i, y'_i, v'_i, c'_i) \bigr\|_2$$

where $\psi$ is an embedding of the memory entry into $\mathbb{R}^{d_\psi}$. For unequal sizes, extend using optimal transport (Earth Mover's Distance).

**Simplification for analysis**: In practice, we often reason about the **empirical distribution** $\hat{P}_t$ induced by $M_t$ rather than the set itself, allowing standard measure-theoretic tools.

### 5.4 Product Space Topology

The evolution state space $\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$ is equipped with the product metric:

$$d_{\mathcal{Z}}(z, z') = d_{\mathcal{F}}(S, S') + d_{\mathcal{M}}(M, M') + \|\theta - \theta'\|_2$$

---

## 6. Scoring Function $S_t$

### 6.1 Definition

**Definition 5 (Gatekeeper Scoring Function).** At time $t$, the gatekeeper is a function:

$$S_t: \mathcal{X}_0 \times \mathcal{Y} \to [0,1]$$

that maps an input-label pair $(x, y)$ to a reliability score $S_t(x, y)$, interpreted as $\mathbb{P}(\ell(f_m(x), y) < \tau \mid x, \text{clean})$ — the probability that the label $y$ for sample $x$ is correct (i.e., not noise).

**Initialization (t=0).** The initial scoring function $S_0$ is derived from the static SCX framework:

$$S_0(x, y) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) < \tau\}$$

i.e., the proportion of experts that agree with label $y$ within tolerance $\tau$. This is the standard SCX reliability estimate.

**Evolution rule.** For $t \geq 1$, $S_t$ is updated using information from $M_{t-1}$ and $f_{\theta_{t-1}}$:

$$S_t = \text{Update}(S_{t-1}, M_{t-1}, f_{\theta_{t-1}})$$

where $\text{Update}$ is a learning algorithm (e.g., gradient descent on a calibrated loss). The exact form depends on the implementation.

### 6.2 Parameterized Form

For practical analysis, we often assume $S_t$ is parameterized by weights $w_t \in \mathbb{R}^{d_w}$:

$$S_t(x, y) = \sigma\bigl( w_t^\top \psi(x, y) \bigr)$$

where $\sigma: \mathbb{R} \to [0,1]$ is a sigmoid (e.g., logistic) and $\psi: \mathcal{X}_0 \times \mathcal{Y} \to \mathbb{R}^{d_w}$ is a fixed feature map.

### 6.3 Interpretation

The scoring function serves as:
1. **Noise filter**: samples with $S_t(x, y) < \delta$ (for some threshold $\delta$) are flagged as potentially noisy
2. **Memory gatekeeper**: samples with high $S_t$ are stored in $M_t$ as reliable reference data
3. **NEP training signal**: the scoring function's decisions provide training targets for the NEP student

---

## 7. Memory Bank $M_t$

### 7.1 Definition

**Definition 6 (Memory Bank).** The memory bank at time $t$ is a collection of labeled samples with associated metadata:

$$M_t = \bigl\{ (x_i, y_i, v_i, c_i) \bigr\}_{i=1}^{N_t}$$

where:
- $x_i \in \mathcal{X}_0$: input sample
- $y_i \in \mathcal{Y}$: observed label
- $v_i \in \{0, 1\}$: **verdict** at time of storage ($v_i = 1$ if the sample was judged reliable, $v_i = 0$ otherwise)
- $c_i \in [0,1]$: **confidence** of the gatekeeper at time of storage ($c_i = S_{t_i}(x_i, y_i)$ where $t_i$ is the storage time)

**Monotonicity property**:

$$M_t \subseteq M_{t+1} \quad \forall t \geq 0$$

Memory only grows; samples are never deleted. This is a design choice that prevents forgetting but raises questions about staleness (see Proposition 1 below).

### 7.2 Empirical Distribution

Define the empirical distribution over the memory bank:

$$\hat{P}_t(x, y, v, c) = \frac{1}{N_t} \sum_{i=1}^{N_t} \delta_{(x_i, y_i, v_i, c_i)}$$

As $t \to \infty$, if the data distribution has finite support or if we assume sufficient exploration, $\hat{P}_t$ converges to a limiting empirical distribution $\hat{P}_\infty$.

### 7.3 Memory Growth Dynamics

The growth of $N_t$ depends on the gatekeeper's decisions:

**Definition 7 (Memory Flow).** Let $q_t$ be the incoming sample batch at time $t$. The gatekeeper $S_t$ selects a subset for inclusion:

$$\Delta M_t = \bigl\{ (x, y, S_t(x,y), S_t(x,y)) \mid (x,y) \in q_t, \; S_t(x,y) > \delta_{\text{store}} \bigr\}$$

where $\delta_{\text{store}} \in (0,1)$ is a storage threshold. Then:

$$M_{t+1} = M_t \cup \Delta M_t, \qquad N_{t+1} = N_t + |\Delta M_t|$$

**Proposition 1 (Memory Growth Rate).** Under Assumptions B1-B3 (defined in Section 13), the expected growth rate satisfies:

$$\mathbb{E}[N_{t+1} - N_t] \geq |q_t| \cdot \mathbb{P}_{(x,y) \sim \mathcal{D}}\bigl( S_t(x,y) > \delta_{\text{store}} \bigr)$$

If the scoring function $S_t$ is improving (becoming more accurate), the growth rate may decrease initially (more false positives filtered) then increase (more true positives retained). The exact dynamics depend on the noise rate $\eta$ and the clean error rate $\mu_s$.

*Proof sketch.* Each sample in batch $q_t$ is included independently with probability $\mathbb{P}(S_t(x,y) > \delta_{\text{store}})$, conditional on the sample's features. The expected increment follows by linearity of expectation. $\square$

---

## 8. NEP Student $f_{\theta_t}$

### 8.1 Definition

**Definition 8 (NEP Student).** The NEP (Noise-Equivariant Predictor) student at time $t$ is a function:

$$f_{\theta_t}: \mathcal{X}_0 \to \mathcal{Y}$$

parameterized by $\theta_t \in \Theta \subseteq \mathbb{R}^{d_\theta}$. The student is trained on the memory bank $M_t$ to predict the true label given an input.

**Training objective**:

$$\theta_{t+1} = \arg\min_{\theta \in \Theta} \frac{1}{N_t} \sum_{i=1}^{N_t} \ell_{\text{nep}}\bigl( f_\theta(x_i), y_i \bigr) + \lambda \cdot \mathcal{R}(\theta)$$

where $\ell_{\text{nep}}$ is the NEP loss (Section 10), and $\mathcal{R}(\theta)$ is a regularization term.

### 8.2 NEP as Delayed Oracle

The NEP student serves as a **delayed ground-truth oracle** for the gatekeeper. After training on $M_t$, the student can provide feedback on samples that were previously ambiguous:

$$\text{feedback}_t(x) = \begin{cases}
f_{\theta_t}(x) & \text{if } \text{Confidence}(f_{\theta_t}(x)) > \delta_{\text{nep}} \\
\emptyset & \text{otherwise (abstain)}
\end{cases}$$

This feedback is used to update the scoring function $S_{t+1}$.

### 8.3 Initialization

At $t=0$, the NEP student is initialized with pre-trained weights (e.g., from supervised learning on a clean subset):

$$f_{\theta_0} = \text{pretrained model}$$

If no pre-training is available, $\theta_0$ is randomly initialized and $M_0$ is populated with expert consensus labels.

---

## 9. Update Operator $\Phi$

### 9.1 Definition

**Definition 9 (Self-Evolution Update Operator).** The update operator is a mapping:

$$\Phi: \mathcal{Z} \to \mathcal{Z}$$

that advances the system state by one evolution round:

$$\Phi(S_t, M_t, \theta_t) = (S_{t+1}, M_{t+1}, \theta_{t+1})$$

The operator decomposes into three component updates:

$$\Phi = (\Phi_S, \Phi_M, \Phi_\theta)$$

where:

1. **Memory update** $\Phi_M$:
   $$M_{t+1} = M_t \cup \{(x, y, S_t(x,y), S_t(x,y)) : (x,y) \in q_t, \; S_t(x,y) > \delta_{\text{store}}\}$$

2. **NEP update** $\Phi_\theta$:
   $$\theta_{t+1} = \arg\min_{\theta \in \Theta} \frac{1}{N_{t+1}} \sum_{(x_i,y_i,\cdot,\cdot) \in M_{t+1}} \ell_{\text{nep}}(f_\theta(x_i), y_i) + \lambda \mathcal{R}(\theta)$$

3. **Gatekeeper update** $\Phi_S$:
   $$S_{t+1} = \text{Update}_{\text{gate}}(S_t, M_{t+1}, f_{\theta_{t+1}})$$

   where $\text{Update}_{\text{gate}}$ is a learning procedure that minimizes the gatekeeper loss $L_{\text{gate}}$ on the augmented memory bank, using the NEP student's output to generate training targets for samples with ambiguous labels.

### 9.2 Deferred Update Variant

In practice, updates may be applied at different frequencies. Define the **update interval** $\Delta_t$ as the number of evolution rounds between NEP retraining. The gatekeeper update $\Phi_S$ may be applied every round (online), while $\Phi_\theta$ is applied every $\Delta_t$ rounds (batch).

For the theoretical analysis in Documents 02 and 03, we primarily consider the synchronous update where all three components update at each round.

### 9.3 Composition

Let $\Phi^{(k)}$ denote $k$ successive applications:

$$\Phi^{(k)}(z_0) = \underbrace{\Phi \circ \Phi \circ \cdots \circ \Phi}_{k \text{ times}}(z_0) = z_k$$

---

## 10. Loss Functions

### 10.1 Gatekeeper Loss $L_{\text{gate}}$

**Definition 10 (Gatekeeper Loss).** For a scoring function $S$ and a sample $(x, y)$ with (possibly unknown) ground-truth noise status $z \in \{0,1\}$ (0 = clean, 1 = noise), the gatekeeper loss is:

$$L_{\text{gate}}(S; x, y, z) = -z \cdot \log(1 - S(x,y)) - (1-z) \cdot \log S(x,y)$$

This is the standard binary cross-entropy loss, treating $S(x,y)$ as the predicted probability that the sample is clean.

**Empirical risk** on a memory bank $M_t$ (with verdict $v_i$ as a proxy for $z_i$):

$$\hat{L}_{\text{gate}}(S; M_t) = -\frac{1}{N_t} \sum_{i=1}^{N_t} \bigl[ v_i \cdot \log S(x_i, y_i) + (1-v_i) \cdot \log(1 - S(x_i, y_i)) \bigr]$$

The **expected gatekeeper loss** is:

$$L_{\text{gate}}^*(S) = \mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ -\eta \cdot \log(1 - S(x,y)) - (1-\eta) \cdot \log S(x,y) \bigr]$$

where $\eta$ is the global noise rate.

**Proposition 2 (Optimal Gatekeeper).** The gatekeeper $S^*$ minimizing $L_{\text{gate}}^*$ satisfies:

$$S^*(x, y) = \frac{1-\eta}{\eta} \cdot \frac{\mathbb{P}(y \mid x, \text{clean})}{\mathbb{P}(y \mid x, \text{noise})}$$

when the ratio is well-defined. Under the uniform noise assumption (A4), this simplifies to:

$$S^*(x, y) \propto \mathbb{P}(y \mid x, \text{clean})$$

*Proof sketch.* The binary cross-entropy optimum is the conditional probability $\mathbb{P}(z=0 \mid x, y)$. Applying Bayes' rule gives the expression. Under A4, $\mathbb{P}(y \mid x, \text{noise})$ is uniform, simplifying the ratio. $\square$

### 10.2 NEP Student Loss $L_{\text{nep}}$

**Definition 11 (NEP Student Loss).** The NEP student is trained with a noise-robust loss function:

$$L_{\text{nep}}(f_\theta; x, y) = \ell_{\text{CE}}(f_\theta(x), y) + \beta \cdot \ell_{\text{cons}}(f_\theta(x), f_{\text{expert}}(x))$$

where:
- $\ell_{\text{CE}}$ is the standard cross-entropy loss
- $\ell_{\text{cons}}$ is a consistency regularization term encouraging agreement with expert consensus
- $\beta \geq 0$ is a trade-off parameter
- $f_{\text{expert}}(x)$ is the expert consensus prediction (e.g., majority vote)

The **empirical NEP loss** on memory bank $M_t$:

$$\hat{L}_{\text{nep}}(f_\theta; M_t) = \frac{1}{N_t} \sum_{i=1}^{N_t} \ell_{\text{CE}}(f_\theta(x_i), y_i) + \frac{\beta}{N_t} \sum_{i=1}^{N_t} \ell_{\text{cons}}(f_\theta(x_i), f_{\text{expert}}(x_i))$$

### 10.3 Composite Loss for Self-Evolution

The overall objective guiding self-evolution is:

$$L_{\text{total}}(z_t) = \mathbb{E}\bigl[ L_{\text{gate}}(S_t) \bigr] + \lambda \cdot \mathbb{E}\bigl[ L_{\text{nep}}(f_{\theta_t}) \bigr]$$

where $\lambda > 0$ is a hyperparameter balancing the two components. This composite loss serves as a Lyapunov function candidate in Document 02.

---

## 11. Evaluation Metrics

### 11.1 Consistency Score

**Definition 12 (Evolutionary Consistency Score).** The consistency score at time $t$ is the agreement rate between the gatekeeper and the NEP student on a held-out validation set $V$:

$$\text{Consistency}_t = \frac{1}{|V|} \sum_{(x,y) \in V} \mathbf{1}\bigl\{ \text{sign}(S_t(x,y) - \delta_{\text{gate}}) = \text{sign}(\text{Confidence}(f_{\theta_t}(x)) - \delta_{\text{nep}}) \bigr\}$$

This measures whether the gatekeeper and NEP converge to similar judgments.

### 11.2 Coverage

**Definition 13 (Gatekeeper Coverage).** The coverage at time $t$ is the proportion of samples that the gatekeeper judges with sufficient confidence:

$$\text{Coverage}_t = \mathbb{P}_{(x,y) \sim \mathcal{D}} \bigl( S_t(x,y) > \delta_{\text{cover}} \bigr)$$

where $\delta_{\text{cover}} \in (0,1)$ is a coverage threshold (typically $\delta_{\text{cover}} = 0.5$).

**Evolutionary behavior**: As $S_t$ improves, coverage should increase because more samples can be confidently classified.

### 11.3 Detection Rate

**Definition 14 (Noise Detection Rate).** The detection rate at time $t$ for a fixed noise threshold $\delta_{\text{noise}}$:

$$\text{DetectionRate}_t = \mathbb{P}_{(x,y) \sim \mathcal{D}} \bigl( S_t(x,y) < \delta_{\text{noise}} \mid z = 1 \bigr)$$

where $z=1$ indicates the sample is noise. This is the true positive rate (recall) of the noise detection function.

**Relationship to Theorem 1**: The detection rate is bounded below by Theorem 1's guarantee when $S_t$ is derived from expert consensus. As $S_t$ evolves, the detection rate may improve beyond the static bound.

### 11.4 F1 Score (Dynamic)

**Definition 15 (Dynamic F1).** At time $t$:

$$\text{F1}_t = \frac{2 \cdot \text{Precision}_t \cdot \text{Recall}_t}{\text{Precision}_t + \text{Recall}_t}$$

where:
- $\text{Recall}_t = \text{DetectionRate}_t$
- $\text{Precision}_t = \mathbb{P}(z = 1 \mid S_t(x,y) < \delta_{\text{noise}})$

---

## 12. Relationship to Existing Definitions

### 12.1 From Static to Dynamic

The existing SCX theory (THEOREMS_UNIFIED.md) provides guarantees for a **static** gatekeeper $S_{\text{static}}$ defined as:

$$S_{\text{static}}(x, y) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) < \tau\}$$

The dynamic gatekeeper $S_t$ generalizes this:

$$S_t(x, y) = \begin{cases}
S_{\text{static}}(x, y) & t = 0 \text{ (initialization)} \\
\text{Update}(S_{t-1}, M_{t-1}, f_{\theta_{t-1}}) & t \geq 1
\end{cases}$$

### 12.2 Connection to State-Conditioned Risk

The expert risk $R_m(s)$ and reliability score $\text{SCX}_m(s)$ from the static theory appear in the initialization:

$$S_0(x, y) = \frac{1}{M} \sum_{m=1}^M \text{SCX}_m(s(x)) \cdot \frac{\mathbb{P}(f_m(x) = y \mid x \in s(x))}{\text{SCX}_m(s(x))}$$

where $\text{SCX}_m(s) = \mathbb{P}(\ell(f_m(x), y) < \tau \mid x \in s)$.

### 12.3 Connection to Consensus Score

The consensus score $C(x)$ is related to $S_0$ via:

$$S_0(x, y) = 1 - \frac{1}{M} \sum_{m=1}^M e_m(x, y) = 1 - C(x) \quad \text{(when } y = y_{\text{obs}} \text{ is the observed label)}$$

This gives the key insight: the initial gatekeeper is the **inverse** of the consensus score. High consensus among experts that the sample is erroneous ($C(x)$ near 1) means low gatekeeper score ($S_0$ near 0), flagging the sample as potentially noisy.

### 12.4 Theorems 1-3 in the Dynamic Setting

- **Theorem 1** provides an **initialization guarantee**: $\text{F1}_0 \geq 1 - O(e^{-2M\Delta^2})$.
- **Theorem 2** warns that **weak features limit improvement**: if $\phi$ is $\delta$-weak, the rate of improvement in $\text{F1}_t$ is bounded by $O(\sqrt{\delta})$.
- **Theorem 3** establishes that **unidentifiability persists**: even with an evolving gatekeeper, the fundamental ambiguity between noise and intrinsic difficulty cannot be resolved without additional assumptions (which self-evolution may partially address through the NEP's inductive bias — see Conjecture 1 below).

**Conjecture 1 (Self-Evolution Breaks Unidentifiability Under Model Correctness).** If the NEP student $f_{\theta_t}$ converges to the true oracle $f^*$ as $t \to \infty$ (i.e., $\lim_{t\to\infty} \mathbb{P}(f_{\theta_t}(x) = f^*(x)) = 1$), then the limiting gatekeeper $S_\infty$ can distinguish noise from difficulty with error rate below the Theorem 3 bound. However, this requires that the NEP's model class is well-specified and $M_t$ contains sufficient clean samples.

*Status: **Conjecture** — not yet proven.*

### 12.5 Assumption A2: Untestability and Violation Degradation (DEFECT-07 Fix)

**Original claim.** Assumption A2 jointly requires **both** requirements: (i) experts are trained on disjoint data (ensuring training-set independence via A1), **and** (ii) expert errors $e_m(x, y)$ are conditionally independent given the input $x$ when the sample is clean. The original text claimed that A2 is "testable" [可检验] and that Assumption A1 (disjoint training sets) alone **guarantees** A2 — it does not; both requirements must be independently satisfied and neither alone suffices.

**Corrected understanding.** A2 is a **structural assumption** about the expert training process, not an empirically testable condition:

1. **Untestability in practice.** For a continuous input space $\mathcal{X}$, each input $x$ appears at most once in any finite dataset. The joint distribution $P(e_1, \dots, e_M \mid x)$ is therefore unobservable — we cannot estimate pairwise correlations $P(e_i, e_j \mid x)$ from a single observation per $x$. A2 is justified by the experimental design (disjoint training sets, independent initializations) but cannot be verified from the data that the SCX pipeline processes.

2. **A1 does not guarantee A2.** Even with perfectly disjoint training sets, experts trained on similar data distributions (e.g., ImageNet-trained models applied to medical images) exhibit correlated errors on out-of-distribution samples. The correlation arises from shared inductive biases, not shared training data.

3. **Practical expert correlation.** For typical deep ensembles:
   - Independent initialization + same architecture: pairwise error correlation $\bar{\rho} \approx 0.1$–$0.3$
   - Different architectures + same training data: $\bar{\rho} \approx 0.2$–$0.5$
   - Fine-tuned from same pre-trained model: $\bar{\rho} \approx 0.3$–$0.6$

**Degradation when A2 is violated.** When experts are positively correlated, the consensus score $C(x) = \frac{1}{M}\sum_m e_m(x,y)$ behaves as if there are fewer independent experts. The effective sample size degrades from $M$ to $M_{\text{eff}}$:

$$\boxed{\;M_{\text{eff}} \approx \frac{M}{1 + (M-1)\bar{\rho}}\;},$$

where $\bar{\rho}$ is the average pairwise correlation of expert error indicators. The Hoeffding concentration bound in Theorem 1 degrades from $\exp(-2M\Delta^2)$ to $\exp(-2M_{\text{eff}}\Delta^2)$.

**Quantitative impact (examples):**
- $M = 10$, $\bar{\rho} = 0.1$: $M_{\text{eff}} \approx 10/(1+0.9) \approx 5.3$ (moderate degradation)
- $M = 10$, $\bar{\rho} = 0.3$: $M_{\text{eff}} \approx 10/(1+2.7) \approx 2.7$ (severe degradation — effective number of experts is < 3)
- $M = 10$, $\bar{\rho} = 0.5$: $M_{\text{eff}} \approx 10/(1+4.5) \approx 1.8$ (catastrophic — barely better than 1 expert)

**Recommendation for practitioners.** When applying SCX, estimate $\bar{\rho}$ from expert predictions on a held-out validation set via the mutual information $I(e_i; e_j)$ or the phi coefficient. Use $M_{\text{eff}}$ in place of $M$ in Theorem 1's bound for a conservative guarantee. If $M_{\text{eff}} \leq 2$, the consensus score is unreliable and SCX should be used with caution or with additional diversity-enforcing mechanisms.

**Revised A2 statement.** A2 is now stated as: "Expert errors are conditionally independent given $x$ for clean samples, as justified by disjoint training sets (A1) and independent initialization. **This assumption is not empirically testable from the SCX pipeline's data.** When violated (e.g., due to shared inductive biases), replace $M$ with $M_{\text{eff}}$ in all concentration bounds."

## 13. Assumption Catalog for Self-Evolution (B1-B6)

These assumptions extend the core A1-A6 into the self-evolution regime.

| # | Assumption | Formal Statement | Used in | Notes |
|---|-----------|-----------------|---------|-------|
| **B1** | **Memory Monotonicity** | $M_t \subseteq M_{t+1}$, $\forall t \geq 0$ | Doc 02, 03 | Design assumption; no deletion |
| **B2** | **Bounded Memory Growth** | $\exists G_{\max} < \infty$ s.t. $\mathbb{E}[N_{t+1} - N_t] \leq G_{\max}$, $\forall t$ | Doc 02, 03 | Prevents explosion |
| **B3** | **NEP Convergence** | $\forall \varepsilon > 0$, $\exists T(\varepsilon)$ s.t. $\forall t \geq T$: $\mathbb{E}[\ell(f_{\theta_t}(x), f^*(x))] \leq \varepsilon$ | Doc 02 | Assumes well-specified model |
| **B4** | **Gatekeeper Lipschitz Continuity** | $|S_t(x,y) - S_t(x,y')| \leq L_S \cdot \|y - y'\|$ for some $L_S < \infty$ | Doc 03 | Needed for regret bound |
| **B5** | **Bounded Gradient** | $\|\nabla_w \ell_t(S_t)\|_2 \leq G$ for all $t$, where $\ell_t$ is the per-round loss | Doc 03 | Standard OGD assumption |
| **B6** | **Delayed Feedback Bound** | $d_t \leq D_{\max} < \infty$ almost surely, where $d_t$ is feedback delay | Doc 03 | For delay analysis |

### 13.1 Relationship to Core Assumptions A1-A6

The core assumptions A1-A6 operate at the level of individual expert models and sample statistics. The self-evolution assumptions B1-B6 operate at the system level. They are complementary:

- **A1-A6** guarantee the **initial** SCX noise detector works (Theorem 1)
- **B1-B6** guarantee the **evolutionary** improvement is well-behaved
- Neither set implies the other; a system can satisfy A1-A6 without B1-B6 and vice versa

**Note on A2 degradation (DEFECT-07 fix).** Assumption A2 jointly requires: **(i) disjoint training data** (A1), and **(ii) conditionally independent expert errors** given $x$ for clean samples. When requirement (ii) is violated — as is common in practice due to shared inductive biases — the effective number of independent experts degrades from $M$ to $M_{\text{eff}} = M/(1+(M-1)\bar{\rho})$. All concentration bounds in both the static theory (Theorem 1) and the self-evolution framework (Proposition SE-1.4) should use $M_{\text{eff}}$ in place of $M$. See Section 12.5 for the full analysis. Neither requirement (i) nor (ii) alone is sufficient; both must hold for the original concentration bounds to apply at full strength. A2 is not empirically testable from the SCX pipeline's data; it is a structural assumption justified by the experimental design.

---

## 14. Summary of Notation

| Symbol | Meaning | Defined In | Existing Core? |
|--------|---------|-----------|----------------|
| $x$ | SCX configuration | Section 4 | No (new) |
| $z_t = (S_t, M_t, \theta_t)$ | Evolution state | Section 5 | No (new) |
| $\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$ | Evolution state space | Section 5 | No (new) |
| $S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]$ | Gatekeeper scoring function | Section 6 | No (new) |
| $M_t$ | Memory bank | Section 7 | No (new) |
| $f_{\theta_t}: \mathcal{X} \to \mathcal{Y}$ | NEP student | Section 8 | No (new) |
| $\Phi: \mathcal{Z} \to \mathcal{Z}$ | Update operator | Section 9 | No (new) |
| $L_{\text{gate}}$ | Gatekeeper loss | Section 10 | No (new) |
| $L_{\text{nep}}$ | NEP student loss | Section 10 | No (new) |
| $\text{Consistency}_t$ | Evolutionary consistency | Section 11 | No (new) |
| $\text{Coverage}_t$ | Gatekeeper coverage | Section 11 | No (new) |
| $\text{DetectionRate}_t$ | Noise detection rate | Section 11 | No (new) |
| $d_{\mathcal{X}}, d_{\mathcal{F}}, d_{\mathcal{M}}, d_{\mathcal{Z}}$ | Metrics | Sections 4-5 | No (new) |
| $\mathcal{D}$ | Data distribution | Inherited | Yes |
| $C(x)$ | Consensus score | Inherited | Yes |
| $\eta$ | Noise rate | Inherited | Yes |
| $\mu_s$ | State-$s$ clean error bound | Inherited | Yes |
| $\mathcal{S}, s(x)$ | State space, assignment | Inherited | Yes |
| $\{f_m\}_{m=1}^M$ | Expert models | Inherited | Yes |
| $\rho_s$ | State probability | Inherited | Yes |

---

*End of Document 01: Symbol System and Problem Setup*

*Preparation for Document 02: The next document will formalize the iteration $z_{t+1} = \Phi(z_t)$ as a discrete dynamical system, analyze fixed points, Lyapunov functions, and attractors.*

*Preparation for Document 03: The following document will analyze the gatekeeper's online learning regret under delayed feedback from the NEP student.*

---

## Changelog

| Date | Defect | Change | Severity |
|------|--------|--------|----------|
| 2026-06-28 | DEFECT-07 | **Added A2 untestability and degradation analysis** (Section 12.5). Acknowledged that Assumption A2 (conditional independence of expert errors given $x$) is not empirically testable from SCX pipeline data — for continuous $\mathcal{X}$, each $x$ appears at most once. A1 (disjoint training) does not guarantee A2 when experts share inductive biases. Added quantitative degradation: effective sample size $M_{\text{eff}} = M/(1+(M-1)\bar{\rho})$ where $\bar{\rho}$ is average pairwise error correlation. For $M=10$, $\bar{\rho}=0.3$, $M_{\text{eff}} \approx 2.7$ (severe). Recommendation: estimate $\bar{\rho}$ on held-out validation set and use $M_{\text{eff}}$ in Theorem 1. | MAJOR |
| 2026-06-28 | — | **Updated Assumption Catalog** (Section 13.1) with cross-reference to A2 degradation analysis. | — |
| 2026-06-28 | B1 | **A2 statement now consistently states BOTH requirements** (§12.5, §13.1): (i) experts trained on disjoint data, AND (ii) conditionally independent errors. Previously some references mentioned only one requirement. | MAJOR |
| 2026-06-28 | B3 | **Added explicit notation note** (§2): $\mathcal{S}$ (calligraphic) = state space (finite index set) vs. $S_t$ (italic with subscript) = gatekeeper scoring function at time $t$. These are entirely distinct objects; context disambiguates. | MINOR |
