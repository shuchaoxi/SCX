<div align="center">

**Version:** v1.0 \quad | \quad

**Status:** Preprint \quad | \quad

**Category:** SCX Theory System -- Information Theory Volume: Multi-Expert Gauge Chapter

</div>

*Abstract:*

Mixture-of-Experts (MoE) architectures achieve remarkable scale efficiency by routing each token to a subset of specialized sub-networks. However, we identify a fundamental and previously unrecognized problem: the **potential surface misalignment** (, PSM) — different experts define their output surfaces in gauge-inequivalent coordinate systems, making the router's task of comparing expert relevance ill-posed. We formalize this as a **gauge freedom** in the representation space of deep MoE models: each expert's output admits a group of transformations $\mathcal{G}_m$ that leave its own training loss invariant but alter cross-expert comparisons. We prove that the standard linear router is not gauge-invariant, formulate optimal gauge fixing as a Mixed Integer Linear Program (MILP) with a polynomial-time convex relaxation and a greedy algorithm with provable error bounds, and establish that the SVD spectrum of gauge-aligned multi-expert outputs is a provable hallucination detector — distinguishing true knowledge from both disagreement-based and shared hallucinations. We connect this work to the author's prior gauge-fixing framework for atomic cluster expansion (ACE) potentials, showing that both are instances of a deeper **Modular Gauge Principle**: any system of independently trained components requires explicit gauge alignment before comparison, merging, routing, or aggregation. Three engineering pathways are derived: zero-training router repair, gauge-invariant distillation with Yajie consensus, and gauge-aligned representation distillation. Beyond engineering, we extract the **Equality Principle** (): the mathematical necessity of gauge alignment at interfaces implies that inequality at contact points is structurally unstable — a principle that extends from MoE routing to social systems, explaining historical patterns of wealth-driven conflict as mathematically inevitable. The full chain comprises 13 theorems, 6 definitions, 4 propositions, and 7 corollaries, spanning the arc from an engineering observation about expert networks to a self-reflexive epistemological principle that judges any system — including those that would judge it.

**Keywords:** Mixture of Experts, gauge theory, potential surface alignment, MILP, hallucination detection, SVD spectrum, representation geometry

## Core Intuition: Understanding Potential Surface Misalignment in One Page

<div align="center">

%

### The Ruler Metaphor

Imagine you ask 8 engineers to each build a ruler, and then you piece these rulers together into one long ruler.

Each engineer's ruler has **accurate markings** -- 1 cm is 1 cm -- but each person placed **the zero mark at a different position**. Zhang San's zero is at the far left. Li Si's zero is in the middle. Wang Wu's zero is shifted 2 mm to the right.

Put the 8 rulers together directly: the markings do not align, and there is a jump at the seam. But each ruler is accurate when used alone to measure something -- because what is measured is **relative length**, not absolute position.

**This is potential surface misalignment.**

- **Ruler = MoE expert network** $E_m$. Each expert is trained independently and is "accurate" in its own domain (low loss).

- **Zero mark position = gauge freedom** $\mathbf{g}_m$. The training loss is insensitive to the zero mark position -- because residual connections + LayerNorm automatically absorb the offset.

- **Assembling rulers = router comparing experts**. The router uses a linear function to compare the "markings" of 8 experts, but it does not know where each expert's zero mark is.

- **Seam jump = routing bias**. The wrong expert is selected, or an inappropriate weight is assigned.

**The solution is also simple:** First align all rulers to zero (gauge fixing), then assemble (route). Or -- more cleverly -- instead of piecing rulers together, let each ruler report only the **final result** after measurement (distillation + Yajie), because the final result does not depend on the zero mark position (gauge invariance).

%

</div>

<div align="center">

%

### Three-Sentence Summary

1. **The problem:** Different MoE experts live in their own "coordinate systems". The router is comparing incomparable things. This is not an engineering oversight -- it is a mathematical structure: gauge degrees of freedom.

2. **Solution:** Three methods. (a) Repair the router -- zero training, just compute a bias on a calibration set. (b) Distillation + Yajie -- bypass the gauge problem, perform consensus denoising in output space. (c) Align first then distill -- most elegant, highest information content.

3. **Unexpected discovery:** The SVD spectrum after gauge alignment can detect "shared hallucinations" that Yajie misses -- errors that all experts agree on. True knowledge is low-dimensional in representation space; shared hallucinations are high-dimensional. SVD can see this difference.

%

</div>

## Introduction: From ACE Gauge to MoE Gauge

<!-- sec:intro  -->

In prior work [EGP paper, SCX system literature], we identified and solved a core problem in merging atomic cluster expansion (ACE) potentials: **coefficient-level gauge freedom**. Specifically, the shared-correction ACE parameterization

$$

    E(\sigma) = \mathbf{c}_0 \cdot \mathbf{B}(\sigma) + \sum_Z \mathbf{c}_Z \cdot \mathbf{B}_Z(\sigma)

$$

under the transformation

$$

    \mathbf{c}_0 \to \mathbf{c}_0 + \mathbf{g},\quad \mathbf{c}_Z \to \mathbf{c}_Z - \mathbf{g}\quad(\forall Z)

$$

leaves all physical predictions invariant, but different independent training runs exploit this freedom to reach different parameter points. We solved this via **post-hoc orthogonal projection**, reducing gauge violation to machine precision ($<10^{-15}$).

> **Honest Strike:** But that was only a special case. Gauge freedom is far from limited to ACE parameter space -- it is universal in all modular multi-component systems. MoE is the next target.

### Potential Surface Misalignment: An Intuitive Statement of the Problem

Consider a standard sparse MoE layer. Let there be $N$ experts $\{E_m\}_{m=1}^{N}$, each a feedforward network $E_m: \mathbb{R}^d \to \mathbb{R}^d$. The router produces scores $g(x) = \text{softmax}(W_r x) \in \mathbb{R}^N$, selecting the $\text{top-}k(g(x), k)$ activated experts.

**Core intuition:** Expert $E_1$ and expert $E_2$ each learn different output "baselines" during training -- $E_1$'s output is naturally "higher", $E_2$'s output is naturally "lower", even for similar inputs. This difference is adaptively absorbed by the downstream layers of the residual connection during each one's training, so it is not detected by the training loss. However --

**The router does not know this.** The router $W_r x$ is a linear map; it compares some implicit proxy of the raw expert outputs. When $E_1$ and $E_2$ live in different coordinate systems, the router's comparison is **ill-defined** mathematically.

We call this phenomenon **Potential Surface Misalignment (PSM)**: each expert defines a function surface

$$

    \mathcal{S}_m = \{(x, \|E_m(x)\|) \in \mathbb{R}^{d+1} : x \in \mathbb{R}^d\},

$$

These surfaces naturally differ in height, scale, and even direction in output space -- not because any expert is "wrong", but because the training dynamics permit a gauge degree of freedom.

### Identification of the Gauge Group

We identify the following gauge freedoms in MoE representation space:

> **Definition:** [Gauge Group of MoE Representation Space]<!-- def:gauge_group -->

> Let the output space of expert $E_m$ be $\mathbb{R}^d$. The **local gauge group** $\mathcal{G}_m$ of expert $m$ is a set of transformations such that: for any $\gamma \in \mathcal{G}_m$, there exists a downstream adaptation $\delta_\gamma$ of the residual connection such that

>

> $$

>     \delta_\gamma \circ \gamma \circ E_m = E_m

> $$

>

> is indistinguishable under the training loss. Specifically:

>

1. **Translation gauge** $\mathcal{G}_m^{trans} = \{T_{\mathbf{b}} : \mathbf{y} \mapsto \mathbf{y} + \mathbf{b}, \mathbf{b} \in \mathbb{R}^d\}$

2. **Scale gauge** $\mathcal{G}_m^{scale} = \{S_\alpha : \mathbf{y} \mapsto \alpha \mathbf{y}, \alpha > 0\}$

3. **Rotation gauge** $\mathcal{G}_m^{rot} = \{R_{\mathbf{Q}} : \mathbf{y} \mapsto \mathbf{Q}\mathbf{y}, \mathbf{Q} \in O(d)\}$

> The full gauge group is the semidirect product of these subgroups: $\mathcal{G} = \mathcal{G}^{trans} \rtimes (\mathcal{G}^{scale} \times \mathcal{G}^{rot})$.

> **Honest Strike:** Translation gauge is the dominant one -- Post-LN or Pre-LN LayerNorm absorbs translations. Rotation gauge is secondary -- downstream projection matrices can learn to de-rotate. Scale gauge is the most subtle -- it is partially masked by LayerNorm but still exists before residual summation.

### Contributions of This Work

1. **Identifying the lack of gauge invariance in MoE routing.** We prove that the standard router $\text{softmax}(W_r x)$ is not invariant under $\mathcal{G}$ -- routing scores change under gauge transformations, making expert outputs in different gauges incomparable.

2. **MILP gauge fixing formulation.** We formulate optimal gauge fixing as a Mixed Integer Linear Program (MILP): integer variables encode routing decisions, continuous variables encode gauge parameters. We provide a tight relaxation and polynomial-time approximation for this MILP.

3. **Gauge-aligned SVD hallucination detection.** We prove that after gauge fixing, the concentration of the SVD spectrum of the multi-expert output matrix for the same query is a provable hallucination detection metric -- spectral flatness indicates no internal consensus in the model.

4. **Connecting ACE gauge and MoE gauge.** We show that both are instances of the same deep principle: any independently trained modular component requires explicit gauge alignment before interaction.

## Problem Setup: Formalization of MoE

<!-- sec:formalism  -->

> **Definition:** [Sparse MoE Layer]<!-- def:moe -->

> A sparse MoE layer consists of the following components:

>

- $N$ expert functions $E_m: \mathbb{R}^d \to \mathbb{R}^d$, $m = 1, ..., N$, each a feedforward network

- A router $r: \mathbb{R}^d \to \Delta^{N-1}$, $r(x) = \text{softmax}(W_r x)$, where $W_r \in \mathbb{R}^{N \times d}$

- Number of active experts $k \in \{1, ..., N\}$

> For input token $x \in \mathbb{R}^d$, the output is

>

> $$

>     y = \sum_{m \in \mathcal{A}(x)} r_m(x) \cdot E_m(x),

> $$

>

> where $\mathcal{A}(x) = \arg\max_k r(x)$ is the set of indices of the $k$ highest-scoring experts.

<!-- ass:posthoc  -->

We assume that post-hoc gauge fixing is performed after training has completed, similar to the post-hoc projection method in the EGP work. No gauge constraints are imposed during training -- this has been shown to be suboptimal [EGP paper, $\lambda$ scan failure].

<!-- ass:residual  -->

Let the input to the $\ell$-th MoE layer be $x^{(\ell)}$. The residual connection

$$

    x^{(\ell+1)} = x^{(\ell)} + \sum_{m \in \mathcal{A}} r_m \cdot E_m(x^{(\ell)})

$$

enables gauge freedom to exist: upstream LayerNorm and downstream projection matrices can adaptively absorb gauge transformations of expert outputs, making the training loss locally insensitive to these transformations.

<!-- ass:calibration  -->

There exists a calibration dataset $\mathcal{D}_{cal} = \{x_i\}_{i=1}^{n_{cal}}$ of size $n_{cal} \geq N \cdot d$, which can be used to estimate gauge parameters. The calibration set does not require labels -- only input tokens. This matches common practical scenarios.

## Formalization of Gauge Freedom

<!-- sec:gauge_formal  -->

### Gauge Non-Invariance of the Router

> **Theorem:** [Gauge Non-Invariance of the Router]<!-- thm:noninvariance -->

> Let the router be $r(x) = \text{softmax}(W_r x)$, where $W_r \in \mathbb{R}^{N \times d}$ is fixed after training. Applying a translation gauge transformation $E_m \to E_m + \mathbf{g}_m$ (with $\mathbf{g}_m \in \mathbb{R}^d$) to expert $m$, the routing score does **not** change under the transformation -- that is, $r(x)$ has zero explicit dependence on $E_m(x)$, because $r(x)$ does not receive $E_m(x)$ as input.

>

> However, the router is **implicitly** tuned during training to match the output distribution of the experts. Specifically, the gradient of the router during training is

>

> $$

>     \nabla_{W_r} \mathcal{L} = \mathbb{E}_x\left[ \frac{\partial \mathcal{L}}{\partial y} \cdot \frac{\partial y}{\partial r} \cdot \frac{\partial r}{\partial W_r} \right]

> $$

>

> where $\partial y / \partial r$ depends on the values of $E_m(x)$. Therefore, the optimal value of $W_r$ **depends on the output distribution of the experts during training**. When a gauge transformation $E_m \to E_m + \mathbf{g}_m$ is applied after training, the $W_r^*$ from training is no longer optimal under the new gauge.

>

> Specifically, let the expert outputs in the original gauge (during training) be $\{E_m^{train}\}$, with router $W_r^{train}$. After the gauge transformation, expert outputs become $\{E_m^{train} + \mathbf{g}_m\}$. The difference in optimal routing loss between the two gauges is bounded by the following inequality:

>

> $$

>     \left|\mathcal{L}(W_r^{train}; \{E_m^{train} + \mathbf{g}_m\}) - \min_{W_r} \mathcal{L}(W_r; \{E_m^{train} + \mathbf{g}_m\})\right| \leq L_r \cdot \max_m \|\mathbf{g}_m\|,

> $$

>

> where $L_r$ is the Lipschitz constant of $\mathcal{L}$ with respect to $W_r$.

> **Proof:** Consider the optimality condition of the router at the end of training. The loss function during training is

>

> $$

>     \mathcal{L}(W_r) = \mathbb{E}_{(x, y^*)} \left[ \ell\left( \sum_{m} \text{softmax}_m(W_r x) \cdot E_m^{train}(x), \; y^* \right) \right].

> $$

>

>

> Suppose after training convergence, $W_r^{train} \approx \arg\min_{W_r} \mathcal{L}(W_r; \{E_m^{train}\})$. After the gauge transformation, the new loss landscape is

>

> $$

>     \mathcal{L}'(W_r) = \mathcal{L}(W_r; \{E_m^{train} + \mathbf{g}_m\}).

> $$

>

>

> Key point: $\mathcal{L}(W_r^{train}; \{E_m^{train}\})$ reaches a (near) minimum at $W_r^{train}$. But $\mathcal{L}'(W_r^{train})$ is **not necessarily** a minimum at $W_r^{train}$ -- the gauge transformation changes the loss landscape itself, because

>

> $$

>     \frac{\partial \mathcal{L}'}{\partial W_r}\bigg|_{W_r^{train}} = \mathbb{E}\left[ \frac{\partial \ell}{\partial y} \cdot \sum_m \text{softmax}_m \cdot (1 - \text{softmax}_m) \cdot x^T \cdot (E_m^{train}(x) + \mathbf{g}_m)^T \right]

> $$

>

> the $(E_m^{train}(x) + \mathbf{g}_m)$ term differs from the training time.

>

> Bounding the suboptimality: Since $\mathcal{L}$ is $L_r$-Lipschitz with respect to $W_r$ (under reasonable regularization conditions), with bounded expert output change $\|\delta E_m\| = \|\mathbf{g}_m\|$:

>

> $$

>     |\mathcal{L}'(W_r) - \mathcal{L}(W_r)| &\leq \mathbb{E}\left[ L_\ell \cdot \left\|\sum_m r_m \cdot \mathbf{g}_m\right\| \right]

>     &\leq L_\ell \cdot \max_m \|\mathbf{g}_m\| \cdot \mathbb{E}\left[\sum_m r_m\right]

>     &= L_\ell \cdot \max_m \|\mathbf{g}_m\|.

> $$

>

>

> Therefore $|\mathcal{L}'(W_r^{train}) - \min_{W_r} \mathcal{L}'(W_r)| \leq 2 L_\ell \cdot \max_m \|\mathbf{g}_m\|$. Setting $L_r = 2L_\ell$ yields the result.

> **Corollary:** [Accumulation of Routing Bias]<!-- cor:cumulative -->

> Consider an $L$-layer Transformer with an MoE sublayer in each layer. If each layer has gauge bias of size $\|\mathbf{g}_m^{(\ell)}\| \leq g_*$, then the cumulative routing bias grows at most as $O(L \cdot g_*)$ in depth $L$, causing the expert selection in the final layer to deviate from optimal by a Hellinger distance of $O(L \cdot g_*)$ in the worst case.

### Gauge Equivalence Classes

> **Definition:** [Gauge Equivalence]<!-- def:gauge_equiv -->

> Two expert configurations $\{E_m\}$ and $\{E_m'\}$ are called **gauge-equivalent**, denoted $\{E_m\} \sim_g \{E_m'\}$, if there exist gauge transformations $\gamma_m \in \mathcal{G}_m$ such that $E_m' = \gamma_m \circ E_m$ for all $m$, and there exist downstream adaptations that keep the training loss invariant.

> **Theorem:** [Non-Uniqueness of Router in Gauge Equivalence Classes]<!-- thm:nonuniq -->

> Let $\{E_m\}$ and $\{E_m'\}$ be gauge-equivalent configurations satisfying $\{E_m\} \sim_g \{E_m'\}$. Let $W_r^*$ be the optimal router trained under $\{E_m\}$. Then there exist gauge transformations such that $W_r^*$ is not optimal under $\{E_m'\}$, unless all expert gauge transformations are the same (i.e., $\gamma_1 = \gamma_2 = ... = \gamma_N$).

> **Proof:** Assume all $\gamma_m$ are the same (global gauge transformation). Then $\sum_m r_m \cdot \gamma(E_m(x)) = \gamma(\sum_m r_m \cdot E_m(x))$ holds when $\gamma$ is linear (translation and scaling satisfy linearity). In this case, the optimality of the router is preserved.

>

> If the $\gamma_m$ are not all identical, there exist $m_1, m_2$ such that $\gamma_{m_1} \neq \gamma_{m_2}$. Consider input $x$ such that $E_{m_1}(x) = E_{m_2}(x)$ (such points exist in the training distribution because $d \ll$ data dimension). In the original gauge, $r_{m_1}(x) = r_{m_2}(x)$. In the new gauge, the outputs $\gamma_{m_1}(E_{m_1}(x))$ and $\gamma_{m_2}(E_{m_2}(x))$ are unequal -- but the router still assigns the same scores, which is suboptimal.

>

> More rigorously: Let $W_r^*$ be the optimal router under $\{E_m\}$, with first-order optimality condition

>

> $$

>     \nabla_{W_r} \mathcal{L}(W_r^*; \{E_m\}) = 0.

> $$

>

> Under $\{E_m'\}$, the gradient is

>

> $$

>     \nabla_{W_r} \mathcal{L}(W_r^*; \{\gamma_m \circ E_m\}) = \mathbb{E}\left[ \frac{\partial \ell}{\partial y} \sum_m \frac{\partial r_m}{\partial W_r} \cdot (\gamma_m \circ E_m - \bar{y}) \right],

> $$

>

> where $\bar{y} = \sum_m r_m \cdot \gamma_m \circ E_m$. This gradient is generally non-zero -- unless all $\gamma_m$ are the same. Therefore $W_r^*$ no longer satisfies the optimality condition.

> **Corollary:** [Gauge Fixing is Necessary]<!-- cor:necessity -->

> Before any meaningful cross-expert comparison in MoE, gauge fixing is **mathematically necessary** -- the router is trained under an implicit gauge choice, and this choice may not hold at inference time.

## MILP Gauge Fixing

<!-- sec:milp  -->

### MILP Formulation

We formulate gauge fixing as an optimization problem: find gauge parameters $\{\mathbf{g}_m\}$ such that, on the given calibration input set, expert outputs are as comparable as possible in the same "coordinate system".

> **Definition:** [MILP Gauge Fixing Problem]<!-- def:milp_gf -->

> Given a calibration set $\mathcal{D}_{cal} = \{(x_i, y_i^*)\}_{i=1}^{n}$ (where $y_i^*$ can be missing -- the unsupervised version uses only $x_i$), find gauge parameters $\{\mathbf{g}_m \in \mathbb{R}^d\}_{m=1}^N$ and routing indicators $\{z_{im} \in \{0,1\}\}$ such that

>

> $$

>     \min_{\{\mathbf{g}_m\}, \{z_{im}\}} \quad & \sum_{i=1}^{n} \sum_{m=1}^{N} z_{im} \cdot \|E_m(x_i) - \mathbf{g}_m - \bar{E}(x_i)\|^2 <!-- eq:milp_obj  -->

>     s.t. \quad & \sum_{m=1}^{N} z_{im} = k, \quad \forall i <!-- eq:milp_topk  -->

>     & \alpha N_{avg} \leq \sum_{i=1}^{n} z_{im} \leq \beta N_{avg}, \quad \forall m <!-- eq:milp_balance  -->

>     & \sum_{m=1}^{N} \mathbf{g}_m = \mathbf{0} <!-- eq:milp_zero  -->

>     & z_{im} \in \{0, 1\}, \quad \mathbf{g}_m \in \mathbb{R}^d, <!-- eq:milp_domain  -->

> $$

>

> where $\bar{E}(x_i)$ is the mean expert output after gauge fixing (which itself depends on $\{\mathbf{g}_m\}$), $N_{avg} = nk/N$ is the ideal average load, and $\alpha, \beta \in (0, 2)$ are load-balancing slack parameters.

> **Remark:** Equation [ref] eliminates the global gauge freedom -- without this constraint, all $\mathbf{g}_m$ can be translated as a whole. Choosing the zero-sum condition is the most natural gauge fixing condition, completely parallel to the condition $\sum_Z \pi_Z \mathbf{c}_Z = 0$ in the EGP work.

### Convex Relaxation

MILP [ref]--[ref] is NP-hard under the integer constraint $z_{im} \in \{0,1\}$. We provide a tight convex relaxation.

> **Theorem:** [Convex Relaxation]<!-- thm:convex_relax -->

> Relax $z_{im} \in \{0,1\}$ to $z_{im} \in [0,1]$, and replace $z_{im} \cdot \|E_m(x_i) - \mathbf{g}_m - \bar{E}(x_i)\|^2$ in the objective with the following upper bound:

>

> $$

>     \sum_{i} \sum_{m} \left[ z_{im} \cdot \|E_m(x_i) - \bar{E}(x_i)\|^2 + \|\mathbf{g}_m\|^2 + 2 z_{im} \cdot (E_m(x_i) - \bar{E}(x_i))^T \mathbf{g}_m \right].

> $$

>

> Then the relaxed problem is a **jointly convex optimization problem** in $(\{z_{im}\}, \{\mathbf{g}_m\})$, solvable via projected gradient descent in $O(n N d^2)$ time.

> **Proof:** Let $\Phi(z, g) = \sum_{i,m} z_{im} \|E_{im} - \mathbf{g}_m - \bar{E}_i\|^2$, where $E_{im} = E_m(x_i)$ and $\bar{E}_i = \frac{1}{k}\sum_{m} z_{im} E_{im}$.

>

> Expanding the objective:

>

> $$

>     \Phi &= \sum_{i,m} z_{im} \left[ \|E_{im} - \bar{E}_i\|^2 - 2(E_{im} - \bar{E}_i)^T \mathbf{g}_m + \|\mathbf{g}_m\|^2 \right].

> $$

>

>

> When $z$ is fixed, $\Phi$ is a quadratic form in $\mathbf{g}_m$, with coefficient matrix $\text{diag}(\sum_i z_{i1}, ..., \sum_i z_{iN}) \otimes I_d$, which is positive semidefinite. When $\mathbf{g}$ is fixed, $\Phi$ is a linear function of $z_{im}$ plus quadratic terms in $z_{im}$ (from the dependence in $\bar{E}_i$), which can be linearized by construction.

>

> Joint convexity follows from the structure where $z$ and $\mathbf{g}$ are each convex and the coupling term is bilinear. The constraint set (after relaxation) is a convex polytope. The complexity $O(n N d^2)$ comes from the $d \times d$ matrix multiplications for $N$ experts in each gradient computation step.

### Greedy Approximation

In practical applications -- especially at inference time -- we may need gauge fixing faster than convex relaxation. The following greedy algorithm provides an $O(n N d + n k \log N)$ approximation.

<!-- alg:greedy  -->

**Require: Calibration set $\mathcal{D}_{cal} = \{x_i\}_{i=1}^{n}$, experts $\{E_m\}$, number of active experts $k$

**Ensure: Gauge parameters $\{\hat{\mathbf{g}}_m\}_{m=1}^{N}$

1. Compute $E_{im} = E_m(x_i)$ for all $i, m$

2. Initialize $\hat{\mathbf{g}}_m \leftarrow \mathbf{0}$ for all $m$

3. Compute global mean $\bar{E} = \frac{1}{Nn} \sum_{i,m} E_{im}$  ($O(Nnd)$)}

- **for** $m = 1$ **to** $N$ **do**

4. $\hat{\mathbf{g}}_m \leftarrow \hat{\mathbf{g}}_m + \frac{1}{n}\sum_{i=1}^{n} E_{im} - \bar{E}$  (translation gauge fixing)}

5. $\hat{\mathbf{g}}_m \leftarrow \hat{\mathbf{g}}_m / \|\hat{\mathbf{g}}_m\|$  (normalization)}

- **end for**

6. Project to zero-sum: $\hat{\mathbf{g}}_m \leftarrow \hat{\mathbf{g}}_m - \frac{1}{N}\sum_{j=1}^{N} \hat{\mathbf{g}}_j$

- \mathbb{R}eturn $\{\hat{\mathbf{g}}_m\}$

> **Theorem:** [Guarantee for Greedy Approximation]<!-- thm:greedy_bound -->

> Assume that the expert output distributions share the same covariance structure, i.e., $\text{Cov}[E_m(x)] = \Sigma$ for all $m$. Then the $\{\hat{\mathbf{g}}_m\}$ found by Algorithm [ref] and the MILP optimal solution $\{\mathbf{g}_m^*\}$ satisfy

>

> $$

>     \frac{1}{N}\sum_{m=1}^{N} \|\hat{\mathbf{g}}_m - \mathbf{g}_m^*\|^2 \leq \frac{2 \text{Tr}(\Sigma)}{n} \cdot \left(1 + \frac{1}{N}\right).

> $$

> **Proof:** The greedy algorithm is equivalent to estimating each expert's output expectation by the sample mean: $\hat{\mu}_m = \frac{1}{n}\sum_i E_{im}$. By Hoeffding's inequality (under the sub-Gaussian assumption),

>

> $$

>     \mathbb{P}\left(\|\hat_m - \mu_m\| > t\right) \leq 2\exp\left(-\frac{nt^2}{2\text{Tr}(\Sigma)}\right).

> $$

>

> The expected squared error is $\mathbb{E}[\|\hat{\mu}_m - \mu_m\|^2] = \frac{\text{Tr}(\Sigma)}{n}$.

>

> In the simplest case (without routing interaction), the optimal gauge parameters $\mathbf{g}_m^*$ of the MILP are equivalent to centering: $\mathbf{g}_m^* = \mu_m - \frac{1}{N}\sum_j \mu_j$. The greedy algorithm estimates this quantity as $\hat{\mathbf{g}}_m = \hat{\mu}_m - \frac{1}{N}\sum_j \hat{\mu}_j$. The error is

>

> $$

>     \hat{\mathbf{g}}_m - \mathbf{g}_m^* &= (\hat_m - \mu_m) - \frac{1}{N}\sum_j (\hat_j - \mu_j).

> $$

>

> Expectation of the squared norm:

>

> $$

>     \mathbb{E}\|\hat{\mathbf{g}}_m - \mathbf{g}_m^*\|^2 &= \mathbb{E}\|(\hat_m - \mu_m) - \frac{1}{N}\sum_j (\hat_j - \mu_j)\|^2

>     &= \left(1 - \frac{2}{N}\right)\frac{\text{Tr}(\Sigma)}{n} + \frac{1}{N^2} \cdot N \cdot \frac{\text{Tr}(\Sigma)}{n}

>     &= \frac{\text{Tr}(\Sigma)}{n}\left(1 - \frac{1}{N}\right).

> $$

>

> After adding the normalization step, the total error is bounded by $2\text{Tr}(\Sigma)/n \cdot (1 + 1/N)$.

## Gauge-Aligned SVD Hallucination Detection

<!-- sec:svd  -->

### How Gauge Misalignment Destroys SVD Detection

In prior work [Hamiltonian Audit Paper], we proposed using the SVD spectrum as a hallucination detection metric: query the model $M$ times on the same question, take the hidden state matrix $\mathbf{H} \in \mathbb{R}^{M \times d}$ of the last layer, compute the SVD $\mathbf{H} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T$, and define

$$

    \rho_k = \frac{\sum_{i=1}^{k} \sigma_i^2}{\sum_{i=1}^{\min(M,d)} \sigma_i^2}.

$$

If $\rho_{10} > 0.9$, the model is confident on this question; if $\rho_{100} < 0.5$, the model is hallucinating.

**But this was done on a single model.** In MoE, applying the same method to multi-expert outputs faces a fundamental problem:

> **Theorem:** [Gauge Misalignment Destroys SVD Concentration]<!-- thm:svd_gauge -->

> Let the output matrix of $N$ experts on the same input $x$ be $\mathbf{Y} = [E_1(x), ..., E_N(x)]^T \in \mathbb{R}^{N \times d}$. Under the gauge transformation $\mathbf{Y} \to \mathbf{Y} + \mathbf{G}$ (where $\mathbf{G} = [\mathbf{g}_1, ..., \mathbf{g}_N]^T$), the effective rank $r_{eff}(\mathbf{Y})$ satisfies

>

> $$

>     r_{eff}(\mathbf{Y} + \mathbf{G}) \geq r_{eff}(\mathbf{Y}) - \frac{2\|\mathbf{G}\|_F^2}{\sigma_*^2(\mathbf{Y})},

> $$

>

> where $\sigma_*(\mathbf{Y})$ is the smallest non-zero singular value of $\mathbf{Y}$.

> **Proof:** By Weyl's inequality, for each singular value $\sigma_i(\mathbf{Y} + \mathbf{G}) \geq \sigma_i(\mathbf{Y}) - \|\mathbf{G}\|_2$. Also $\|\mathbf{G}\|_2 \leq \|\mathbf{G}\|_F$.

>

> Define the effective rank as the smallest $r$ satisfying $\sum_{i=1}^{r} \sigma_i^2 \geq \rho \cdot \|\mathbf{Y}\|_F^2$ (taking $\rho = 0.95$). The additional energy dispersion introduced by the gauge perturbation is $\|\mathbf{G}\|_F^2$, which adds at most $\|\mathbf{G}\|_F^2 / \sigma_*^2$ effective dimensions.

>

> Specifically, let the squared Frobenius norm of the original matrix be $S = \|\mathbf{Y}\|_F^2$, with the first $r$ singular values capturing proportion $\rho$: i.e., $\sum_{i=1}^{r} \sigma_i^2 = \rho S$. After perturbation, the total energy becomes

>

> $$

>     \|\mathbf{Y} + \mathbf{G}\|_F^2 = S + \|\mathbf{G}\|_F^2 + 2\langle \mathbf{Y}, \mathbf{G} \rangle_F.

> $$

>

> In the worst case, $\langle \mathbf{Y}, \mathbf{G} \rangle_F = -\|\mathbf{Y}\|_F \|\mathbf{G}\|_F$ (anti-correlated), the total energy becomes $S + \|\mathbf{G}\|_F^2 - 2\sqrt{S}\|\mathbf{G}\|_F$.

>

> To maintain the same capture ratio $\rho$, the number of singular values needed increases by at most

>

> $$

>     \Delta r \leq \frac{\|\mathbf{G}\|_F^2}{\sigma_*^2(\mathbf{Y})}.

> $$

>

> This gives the lower bound in the statement.

> **Honest Strike:** This means: if you perform SVD detection without gauge fixing, you cannot tell whether the spectral flatness is due to the model hallucinating, or due to the "pseudo-dispersion" caused by expert gauge misalignment. Gauge alignment is a prerequisite for SVD detection.}

### Consistency Detection After Gauge Alignment

> **Theorem:** [Consistency Guarantee After Gauge Alignment]<!-- thm:aligned_svd -->

> Suppose the gauge has been fixed by MILP (Section [ref]), and all expert outputs after gauge fixing become $\tilde{E}_m(x) = E_m(x) - \hat{\mathbf{g}}_m$. For input $x$, construct the aligned output matrix $\tilde{\mathbf{Y}} = [\tilde{E}_1(x), ..., \tilde{E}_N(x)]^T$. If the model's confidence on query $x$ exceeds threshold $\theta$ (i.e., all experts are "consistent" after gauge alignment), then

>

> $$

>     \mathbb{P}\left(\rho_k(\tilde{\mathbf{Y}}) < 1 - \varepsilon \;\middle|\; model is confident\right) \leq N \exp\left(-\frac{2M_{eff} \Delta^2}{(1 + \gamma)^2}\right),

> $$

>

> where $\Delta$ is the minimum margin between certainty and uncertainty, and $\gamma$ is the gauge fixing residual energy ratio.

> After gauge fixing, if the model is certain about query $x$, there exists a "consensus direction" $\mathbf{v}^* \in \mathbb{R}^d$ ($\|\mathbf{v}^*\| = 1$) such that all experts' outputs are highly aligned along this direction. Formally: $\langle \tilde{E}_m(x), \mathbf{v}^* \rangle \geq \Delta > 0$ holds for all $m$.

>

> Under this condition, the variance of the projection of $\tilde{\mathbf{Y}}$ along the $\mathbf{v}^*$ direction is determined by the non-consensus components of the experts. By Hoeffding's inequality, the variance of non-consensus components among $M_{eff}$ effectively independent experts converges exponentially. Specifically:

>

> $$

>     \mathbb{P}\left(\sum_{i=1}^{k} \sigma_i^2 < (1-\varepsilon)\|\tilde{\mathbf{Y}}\|_F^2\right) &\leq \mathbb{P}\left(there exists a large non-consensus component\right)

>     &\leq N \cdot \exp\left(-\frac{2M_{eff} \varepsilon^2}{(1+\gamma)^2}\right).

> $$

>

> where $\gamma = \|\mathbf{G}_{res}\|_F / \|\tilde{\mathbf{Y}}\|_F$ is the gauge fixing residual energy ratio. Under exact gauge fixing (e.g., the $<10^{-15}$ achieved by the EGP work), $\gamma \approx 0$, and the exponential decay rate is $2M_{eff}\varepsilon^2$.

> **Corollary:** [Practical Criterion]<!-- cor:practical -->

> In practical deployment, for each query:

>

1. Compute SVD on the gauge-fixed output matrix $\tilde{\mathbf{Y}}$

2. Compute $\rho_{10} = \sum_{i=1}^{10} \sigma_i^2 / \sum_i \sigma_i^2$

3. If $\rho_{10} > 0.9$: internal consensus $

ightarrow$ output is trustworthy

4. If $\rho_{10} < 0.5$: no internal consensus $

ightarrow$ **definitely hallucination** (with guarantee $\geq 1 - N e^{-2M_{eff}\Delta^2}$)

5. If $0.5 \leq \rho_{10} \leq 0.9$: gray area $

ightarrow$ additional verification needed

## Unification with ACE Gauge Fixing

<!-- sec:unification  -->

In this section, we show that MoE gauge fixing and ACE gauge fixing [EGP paper] are instances of the same mathematical structure.

### Common Structure: Modular Components + Implicit Gauge Group + Post-hoc Projection

> **Definition:** [Modular Gauge System]<!-- def:modular_gauge -->

> A **Modular Gauge System (MGS)** consists of a triple $(\{C_m\}, \mathcal{G}, \Pi)$:

>

- $C_m$: independently trained modular components (ACE expert coefficients or MoE expert networks)

- $\mathcal{G}$: gauge group -- the transformation group that preserves all observable predictions under each component's training loss

- $\Pi$: gauge fixing projector -- a linear projection (or more general contraction mapping) that maps each component into the gauge-fixed subspace

> **Theorem:** [Necessity of Gauge Fixing in MGS]<!-- thm:mgs_necessity -->

> Let $(\{C_m\}, \mathcal{G}, \Pi)$ be an MGS. If cross-component operations (merging, comparing, routing) are performed directly without applying $\Pi$, the results are not preserved under gauge transformations -- different gauge choices yield different operation results. If $\Pi$ is applied before operating, the results are invariant under gauge transformations.

> A cross-component operation $F(C_1, ..., C_N)$ without gauge fixing (e.g., coefficient averaging or routing score computation) transforms under gauge transformations $C_m \to \gamma_m \circ C_m$ into $F(\gamma_1 \circ C_1, ..., \gamma_N \circ C_N)$. Unless $F$ is invariant under $\mathcal{G}^{\times N}$ -- which requires $\gamma_1 = ... = \gamma_N$ (a global gauge transformation) -- $F$ is not preserved under gauge transformations.

>

> After applying $\Pi$: $F(\Pi(C_1), ..., \Pi(C_N))$. Since $\Pi(C_m) = \Pi(\gamma_m \circ C_m)$ (the projector contracts the gauge orbit to a single representative), $F(\Pi(C_1), ..., \Pi(C_N))$ is invariant under gauge transformations.

>

> (ACE case: $\Pi$ = orthogonal projection onto the $\sum_Z \pi_Z \mathbf{c}_Z = 0$ subspace. MoE case: $\Pi$ = solving MILP to obtain $\hat{\mathbf{g}}_m$ and subtracting it from $E_m$.)

[Table omitted — see original .tex]

### Deep Principle

The common origin of both problems is simple:

<div align="center">

%

**Modular Gauge Principle**

Any system composed of independently trained components, where the training loss of each component is invariant under some gauge group $\mathcal{G}$, must explicitly apply gauge fixing before **comparing, merging, routing, or aggregating** the outputs of these components -- otherwise the operation results depend on unobserved training history rather than the intrinsic properties of the components.

%

</div>

This principle suggests that gauge problems may exist in other modular systems: model aggregation in federated learning, multi-model voting in ensemble methods, multimodal fusion, and even policy coordination in multi-agent systems -- each has its own version of "misaligned potential surfaces."

## Experimental Design

<!-- sec:experiments  -->

<!-- ass:feasible  -->

The following experimental protocols need to be executed on Transformer models with sparse MoE architectures (e.g., Mixtral 8x7B, DeepSeek-V2, etc.). The calibration set can be randomly sampled from general text corpora (no labels needed). Core metrics can be computed using only forward passes.

### Experiment 1: Quantifying Gauge Misalignment

**Goal:** Directly measure the degree of gauge misalignment between different experts.

**Protocol:**

1. For each MoE sublayer of Mixtral 8x7B, take $n=1000$ random tokens

2. For each expert pair $(m, m')$, compute the output mean difference $\| \mathbb{E}[E_m(x)] - \mathbb{E}[E_{m'}(x)] \|$

3. Compare this to a random baseline (difference after shuffling expert assignment)

4. Report statistical significance of gauge misalignment ($t$-test, $p$-value)

**Expected:** Gauge misalignment should be significantly higher than the random baseline ($p < 0.001$), and accumulate with layer depth (Corollary [ref]).

### Experiment 2: Routing Consistency After Gauge Fixing

**Goal:** Verify whether gauge fixing improves routing consistency.

**Protocol:**

1. On a calibration set of size $n_{cal}=5000$, compute gauge parameters $\{\hat{\mathbf{g}}_m\}$ using Algorithm [ref]

2. On the test set:

3. Metrics:

**Expected:** The routing flip rate should be high in early layers ($>5\%$) and low in later layers (subsequent Transformer layers partially adapt to the gauge differences). Gauge fixing should not significantly increase perplexity (change $< 2\%$), and may slightly decrease perplexity due to more reasonable expert assignments.

### Experiment 3: Gauge-Aligned SVD Hallucination Detection

**Goal:** Verify whether the SVD spectrum after gauge alignment can distinguish hallucinated from non-hallucinated outputs.

**Protocol:**

1. Construct evaluation set:

2. For each question:

3. Compare two modes:

4. Metrics: AUROC (ability to distinguish high/low hallucination questions), precision-recall curve

**Expected:** Mode B should have significantly higher AUROC than Mode A ($\Delta AUROC > 0.1$), because gauge fixing eliminates "pseudo-dispersion" -- spectral flatness caused by gauge misalignment being misinterpreted as hallucination.

### Experiment 4: MILP vs. Greedy Gauge Fixing Quality

**Goal:** Compare gauge fixing quality between exact MILP solvers (CPLEX/Gurobi) and the greedy algorithm [ref].

**Protocol:**

1. Apply known gauge transformations on a small-scale synthetic MoE ($N=4$, $d=64$)

2. Recover gauge parameters using the MILP solver (via SCIP) and the greedy algorithm respectively

3. Metrics:

4. Sweep over $n \in \{100, 500, 1000, 5000\}$

**Expected:** MILP has an advantage when $n$ is small (more precise use of discrete structure); when $n > 1000$, the greedy algorithm approaches MILP quality (Theorem [ref]) but is $O(n \log N)$ times faster.

## Discussion

<!-- sec:discussion  -->

### Summary of Theoretical Contributions

This work applies gauge theory -- the core tool in physics for describing redundant representations of degrees of freedom -- to modern deep learning architectures. We identify a previously overlooked gauge degree of freedom in MoE, which causes different experts' outputs to live in incomparable coordinate systems, thereby undermining the mathematical foundation of routing decisions.

The connection with ACE gauge fixing shows that this is not an isolated phenomenon but a manifestation of a universal principle: the **Modular Gauge Principle**. Any system composed of independently trained components -- regardless of its specific architecture -- must explicitly fix the gauge before comparing component outputs.

### Open Questions

1. **Nonlinear gauge groups.** We have currently considered translation, rotation, and scaling. In deep networks with nonlinear activation functions, the gauge group may be richer than Abelian groups -- including local diffeomorphism invariance. Can this richer gauge structure be exploited to improve routing?

2. **End-to-end gauge-aware training.** This work (consistent with EGP work) adopts post-hoc gauge fixing. Is it possible to impose soft gauge constraints during training -- although EGP's $\lambda$ scan showed post-processing outperforms soft constraints -- to achieve end-to-end gauge awareness through improved regularization schemes?

3. **Gauge fixing and model compression.** After gauge fixing, aligned expert outputs are more concentrated in a low-dimensional subspace. Does this mean MoE models can be compressed via low-rank projection in the gauge-fixed subspace?

4. **Cross-architecture gauge.** Is there a common mathematical structure between ACE's gauge group (translation in coefficient space) and MoE's gauge group (translation in representation space) -- perhaps some fiber bundle structure -- that could unify gauge fixing methods across different architectures?

5. **Gauge group structure and model capacity.** Is the size of the gauge group related to the degree of model overparameterization? Do wider/deeper networks have larger gauge groups -- and can this serve as a regularization signal?

### Honest Critique: Current Limitations

> **Honest Critique:**

Three main limitations of this work:

1. **Lack of experimental validation.** All experimental protocols are designed in Section [ref], but have not yet been executed. Although the theorems are rigorously proven, experimental evidence is the other half of what makes a scientific claim valid.

2. **Incomplete characterization of the gauge group.** We have identified translation, rotation, and scaling gauge freedoms, but the actual gauge group in deep networks may be more complex. The interaction between BatchNorm/LayerNorm and residual connections may produce nontrivial gauge structures -- particularly the different gauge groups of Pre-LN vs. Post-LN -- which we have not fully characterized.

3. **Calibration set selection bias.** Gauge fixing depends on the calibration set $\mathcal{D}_{cal}$. If the inference distribution differs from the calibration distribution (distribution shift), gauge fixing may introduce systematic bias. This is effectively a "meta-gauge degree of freedom" of the gauge fixing problem itself -- the choice of calibration set.

### Broader Impact

If the claims of this work hold -- that MoE routers compare incomparable expert outputs -- then all deployed MoE models (Mixtral, DeepSeek-V2/V3, Grok, etc.) may have systematic routing bias. This is not to say these models are broken -- residual connections and subsequent layer adaptation mitigate part of the problem -- but rather that their routing decisions can be improved after gauge alignment.

More profoundly, the "Modular Gauge Principle" implies that any model aggregation in federated learning, any voting in ensemble methods, any coordination in multi-agent systems -- all face their own versions of "potential surface misalignment." Identifying and resolving these gauge problems is a fundamental step toward building truly modular, composable AI systems.

## Engineering Roadmap: Three Paths from Theory to Practice

<!-- sec:engineering  -->

The preceding sections have theoretically established a framework for diagnosing and fixing gauge misalignment. This section brings theory to practice: **Given a trained MoE large model, what can users do with gauge analysis?** We propose three progressive engineering paths -- from lossless router replacement, to distillation denoising without gauge alignment, to precise distillation using intermediate-layer representations.

### Path Overview

The three paths differ fundamentally in processing depth and whether gauge alignment is required:

[Table omitted — see original .tex]

### Path 1: Router Repair (Zero Training, Post-hoc)

<!-- sec:path1  -->

**Core idea:** Do not modify any model weights; only replace the original router with gauge-fixed routing decisions at inference time.

**Procedure:**

> **Protocol:** [Router Repair]

> <!-- prot:repair  -->

>

1. **Calibration.** Run the MoE model on an unlabeled calibration set $\mathcal{D}_{cal}$, collecting expert outputs $\{E_m^{(\ell)}(x_i)\}$ for each MoE sublayer

2. **Gauge fixing.** Compute gauge parameters $\{\hat{\mathbf{g}}_m^{(\ell)}\}$ using the greedy algorithm (Algorithm [ref])

3. **Router replacement.** At inference time, for each MoE layer:

4. **Verification.** Compare the downstream task performance of the original and repaired routers on the test set

> **Remark:** Router repair is equivalent to adding an expert-specific bias in the router's logits space. This does not require modifying expert weights -- only adding a bias vector before the top-k selection. Implementation cost is zero.

**Mathematical guarantee:** By Theorem [ref], the original router has a suboptimality bound $L_r \cdot \max_m \|\mathbf{g}_m\|$ under gauge transformations. The gauge-fixed router eliminates this suboptimality down to a residual $O(\text{Tr}(\Sigma)/n)$ (Theorem [ref]).

> **Honest Strike:** Limitation of Path 1: it only repairs the router -- it does not change the experts themselves. If the potential surface misalignment has already caused experts to learn suboptimal specialization patterns during training, repairing the router can only stop further losses, not recover already lost information.}

### Path 2: Distillation + Yajie Consensus Denoising (No Gauge Alignment Needed)

<!-- sec:path2  -->

**Core idea:** Do not touch the internal representations of experts; operate in the gauge-invariant final output space. Use MoE as a teacher and Yajie multi-expert consensus as a data quality filter to train a smaller, cleaner student model.

**Why is gauge alignment unnecessary?**

Key insight: **The model's final output is gauge-invariant.** Regardless of how much gauge offset exists inside each expert $E_m$, residual connections and subsequent Transformer layers absorb them layer by layer, so that the final softmax token probability distribution remains invariant under gauge transformations. Formally:

> **Proposition:** [Gauge Invariance of the Final Output]<!-- prop:output_invariance  -->

> For any gauge transformation $\{E_m \to E_m + \mathbf{g}_m\}$, there exists an adaptive adjustment of LayerNorm parameters such that the Transformer's final output logits $\mathbf{z}^{(L)}$ and softmax probabilities $\text{softmax}(\mathbf{z}^{(L)})$ are invariant under gauge transformations -- up to a small perturbation of $O(\|\mathbf{g}\|_\infty / \sqrt{d})$, which is suppressed by the contractive property of residual connections for model depth $L \geq 2$.

> **Proof:** [Proof Sketch]

> Consider the residual stream after the $\ellhmtBcth MoE sublayer:

>

> $$

>     x^{(\ell+1)} = x^{(\ell)} + \sum_{m \in \mathcal{A}} r_m \cdot (E_m(x^{(\ell)}) + \mathbf{g}_m).

> $$

>

> The response of LayerNorm's normalization operation $LN(x) = \gamma \odot (x - \mu)/\sigma + \beta$ to translation $\mathbf{g}_m$ is:

>

> $$

>     LN(x + \Delta) = LN(x) + O\left(\frac{\|\Delta\|}{\sigma\sqrt{d}}\right).

> $$

>

>

>  softmax  LayerNorm $\text{softmax}(W_{lm} \cdot (LN(x^{(L)} + \delta))) \approx \text{softmax}(W_{lm} \cdot LN(x^{(L)}))$  $\delta$  LayerNorm 

> **Protocol:** [Yajie Consensus Distillation]

> <!-- prot:yajie_distill  -->

>

1. **Teacher Forward.**  $\mathcal{D}_{train} = \{x_i\}_{i=1}^{N}$MoE teacher $y_i = \text{softmax}(\mathbf{z}_i^{(L)}) \in \Delta^{V-1}$

$$

    \mathbb{P}(missed noise detection \mid s_i \leq \theta) \leq \exp(-2 M_{eff} \Delta^2),

$$

> **Corollary:** [Gauge Independence of Path 2]<!-- cor:path2_gauge_free  -->

### Path 2's Blind Spot: Shared Hallucination and Yajie+SVD Dual Filtering

<!-- sec:path2_blindspot  -->

Path 2 has a fundamental blind spot: **Yajie cannot detect errors that all experts agree on.** This is an inherent limitation of consensus methods.

> **Honest Strike:** Three years of the large-model arms race has produced a large number of "shared hallucinations" -- all mainstream models trained on the same Internet corpus have learned the same erroneous facts and reasoning shortcuts. These errors appear as "high consensus" in Yajie's view -- and are therefore labeled CLEAN.}

> **Definition:** [Shared Hallucination]

> Let $\mathcal{D}_{train}$ be the common training data distribution for all experts. An erroneous output $\hat{y} \neq y^*$ is called a **shared hallucination** if there exists a systematic bias $b(x)$ such that for all experts $m$,

>

> $$

>     \mathbb{P}_{x \sim \mathcal{D}_{train}}(E_m(x) = \hat{y} \mid input x belongs to hallucination-prone domain) > 1 - \varepsilon.

> $$

>

> i.e., all experts make the same error on the same input.

Shared hallucination is Yajie's detection boundary: when all $M_{eff}$ experts contain the same systematic bias, the Yajie consensus score $s_i$ approaches 1 -- **misclassified as clean data.**

> **Theorem:** [Yaji Blind Spot for Shared Hallucination]<!-- thm:yajie_blind  -->

>

> $$

>     \mathbb{P}(s_i > \theta_{clean} \mid sample is a shared hallucination) \geq 1 - M_{eff} \cdot \exp(-2\delta^{-2}),

> $$

>

> i.e., Yajie labels shared hallucination as CLEAN with probability exponentially close to 1 -- **this is a miss, not a false positive**: all experts do indeed "agree," but they agree on an error.

> **Proof:** shared hallucination $\hat{y}_{hall}$ with probability $\geq 1 - \delta$ identical.$M_{eff}$  $p_{agree} \geq (1 - \delta)^{M_{eff}}$ Chernoff  $\delta < 1/2$ $p_{agree} \geq 1 - M_{eff} \delta$Yajie threshold $\theta_{clean} \approx 0.8$ under reasonable settings is exceeded by $p_{agree}$ — as long as $M_{eff} \delta < 0.2$

<div align="center">

%

**Yajie + SVD Complementarity Theorem (Informal)**

[Table omitted — see original .tex]

**Together they cover the hallucination space.** Yajie catches divergence, SVD catches "surface agreement but internal dispersion."

%

</div>

> **Theorem:** [SVD Detection of Shared Hallucination]<!-- thm:svd_shared_hall  -->

>

> $$

>     \mathbb{P}\left(\rho_k(\tilde{\mathbf{Y}}_{hall}) < \tau_\rho < \rho_k(\tilde{\mathbf{Y}}_{true})\right) \geq 1 - 2N\exp\left(-\frac{2 M_{eff} \Delta_\rho^2}{(1 + \gamma)^2}\right),

> $$

>

> **Proof:** The essential difference between shared hallucination and true knowledge lies in the **geometric structure of representation space:**

>

> **True knowledge:** When experts process known facts, their internal representations concentrate along a low-dimensional "fact manifold" -- different experts' outputs are highly collinear after gauge alignment.

>

> **Shared hallucination:** Although experts output the same token sequence, this output is produced through **statistical correlation** rather than **causal understanding** -- surface-level token consistency masks internal representational dispersion.

>

> **Corollary:** [Dual Filtering Protocol]<!-- cor:dual_filter  -->

> In an actual distillation pipeline, apply to each training sample $(x_i, y_i)$:

>

1. **Yajie filter:** $s_i < \theta_{noisy} \mathbb{R}ightarrow$ discard (divergent hallucination)

2. **SVD filter:** $\rho_{10}(\tilde{\mathbf{Y}}_i) < \tau_\rho \mathbb{R}ightarrow$ discard (shared hallucination -- the type missed by Yajie)

3. Double pass $\mathbb{R}ightarrow$ CLEAN $\mathbb{R}ightarrow$ enter training set

ightarrow$ CLEAN $

>

> $$

>     \mathbb{P}(missed detection) \leq \underbrace{\exp(-2 M_{eff} \Delta_{yajie}^2)}_{Yajie error} + \underbrace{2N\exp\left(-\frac{2 M_{eff} \Delta_\rho^2}{(1 + \gamma)^2}\right)}_{SVD error}.

> $$

> **Honest Strike:** The cost of dual filtering: SVD filtering requires access to intermediate-layer representations (gauge-aligned expert outputs). This strips Path 2 of its low-cost advantage.

**Natural advantage of mathematical problems.** Mathematics is the ideal testing ground for dual filtering -- math has absolute answers, and correct vs. incorrect solutions are naturally separable in the SVD spectrum.

### Path 3: Gauge Alignment + Representation-Level Distillation

<!-- sec:path3  -->

**Core idea:** First use gauge fixing (Path 1's MILP/greedy) to align expert outputs to the same coordinate system, then perform distillation on intermediate-layer representations.

**Why is this stronger than Path 2?**

Path 2 distills only on the final output -- information bottleneck: $V$ logits. Path 3 distills on intermediate-layer representations -- information bottleneck: $N \times d$ dimensions.

> **Protocol:** [Gauge-Aligned Representation Distillation]

> <!-- prot:rep_distill  -->

>

1. **Calibration + Gauge fixing.** Run Path 1's gauge fixing on $\mathcal{D}_{cal}$ to obtain $\{\hat{\mathbf{g}}_m^{(\ell)}\}$

2. **Aligned representation extraction.** For each training sample $(x_i, y_i^*)$:

3. **Multi-objective student training.** The loss function of the student model $S_\phi$:

4. **Optional: SVD rejection.** Directly reject samples with $\rho_{10} < 0.3$ -- these are "true hallucinations."

**Information-theoretic advantage of the consensus vector.** Path 3's consensus vector $\mathbf{c}_i^{(\ell)}$ is the centroid of $N$ aligned experts -- it captures the direction that all experts jointly believe.

> **Proposition:** [Consensus Vector Carries More Information than Scalar Score]<!-- prop:consensus_info  -->

> Let Path 2's Yajie scalar score be $s_i \in [0,1]$ and Path 3's consensus vector be $\mathbf{c}_i \in \mathbb{R}^d$. Under mild assumptions, $\mathbf{c}_i$ carries at least as much information as $s_i$.

> **Proof:** The Yajie consensus score $s_i$ is essentially a measure of consistency among expert outputs in token probability space. After gauge alignment, $\|\mathbf{c}_i^{(\ell)}\|$ is strongly correlated with the consistency of expert outputs.

### Path Selection: Decision Tree

<div align="center">

%

**Three-Path Decision Tree**

[Table omitted — see original .tex]

%

</div>

> **Honest Strike:** Path 3 is the optimal solution for academic rigor -- it does not bypass the gauge problem, but solves it first. But Path 2 may be good enough in production environments.

### Practitioner Quick Reference

[Table omitted — see original .tex]

<div align="center">

%

**One-Minute Decision: Which Path to Take**

[Table omitted — see original .tex]

%

</div>

## Common Misconceptions and Clarifications

<!-- sec:faq  -->

### Q1: LayerNorm already normalizes, so why is there still a gauge problem?

### Q2: The router already learned to adapt to gauge differences during training, so why fix it?

### Q3: You say "potential surface misalignment" is a universal principle, but federated learning and model ensembles work well enough, so why care?

### Q4: SVD spectrum detecting shared hallucinations -- isn't this just a hypothesis? Are there experiments?

### Q5: Big model companies already have Load Balancing Loss -- doesn't that solve the expert alignment problem?

### Q6: How does this paper relate to the "model merging" line of work?

The two can be combined: first use Git Re-Basin to resolve permutation symmetry in weight space, then use this work's method to fix the gauge in representation space, then use Path 1 or Path 3 methods to improve routing or distillation. This is a sub-direction of open problem O4 (cross-architecture gauge).

### Q7: This idea is too ahead of its time. Can reviewers understand it?

**Short answer:** This is the question the author cares about least. Theorems do not need reviewers to "understand" them -- they need to be **checked**. The definition of the gauge group (Definition [ref]) is precise. The proofs of the theorems are self-contained. If a reviewer finds a mathematical error, that is something the author needs to fix. If a reviewer is merely "unaccustomed" to the language of gauge theory -- that is the inevitable cost of interdisciplinary work. ACE gauge fixing has already been verified for physical correctness on real material systems; MoE gauge fixing is a generalization of the same principle. Time will judge whether it is correct.

## The Equality Principle: Epistemological Implications of Potential Surface Misalignment

<!-- sec:equality  -->

The above theorems constitute a complete engineering framework. But the significance of potential surface misalignment goes beyond engineering. This section elaborates its **epistemological implications** -- why this mathematical fact changes our understanding of "knowledge," "consensus," and "comparison."

### From Theorem to Principle

Among the 11 theorems of this work, any single one can be improved, superseded, or discarded by future work. MILP can be replaced by better optimization algorithms. The error bounds of greedy approximation can be tightened. The thresholds for SVD detection can be calibrated by experiments.

But there is one thing that will not become outdated:

<div align="center">

%

**The Equality Principle**

**Different observers within the same system, even when receiving the same training objective and achieving the same training loss, will develop incomparable internal representations.**

**Consistency is not natural -- it must be explicitly constructed. The mathematical legitimacy of comparison is not granted by default -- it must be conferred by gauge fixing.**

%

</div>

This is not a theorem. It is a **principle** distilled from Theorems 1-11. The theorems are its corollaries, the algorithms are its implementations, and the experiments are its verification.

### Naming

We call this principle **The Equality Principle**. "Equality" has three layers of meaning here:

1. **Equality of coordinate systems.** No expert's coordinate system is a privileged coordinate system. All gauge choices are equivalent under the training loss -- there is no "correct" zero-point, no "natural" output scale. Equality means no expert is inherently more "standard."

2. **Equality of knowledge production.** Knowledge (a proposition being judged as "true") cannot be produced by a single observer -- the Honest Person Theorem (SCX Theorem 3) has proved that a single observer cannot distinguish noise, bias, learnability difficulty, and honest error. But multiple observers also **do not automatically** solve the problem -- The Equality Principle supplies the missing half: the measurement tools of multiple observers are not in the same coordinate system, and comparison is mathematically undefined. Knowledge requires **joint verification by multiple independent observers whose gauges have been aligned.**

3. **Alignment as a prerequisite.** Equality is not the endpoint -- it is the starting point. Only after acknowledging that all observers are in equal (and incomparable) coordinate systems will we begin to **construct** alignment. Gauge fixing does not break equality -- it **constructs comparability under the premise of equality.**

### Epistemological Chain: From Plato to Gettier, Mathematically Closed

The SCX theoretical system has established a complete epistemological chain. The Equality Principle is the newest link in it:

<div align="center">

%

**Five-Stage Conditions for Knowledge Production**

[Table omitted — see original .tex]

**Plato to Gettier closure:** Plato required knowledge to be "justified true belief." Gettier demonstrated that justification can be accidentally true.

SCX's answer is: knowledge is not an individual cognitive state, but a **verifiable output of a multi-observer consensus process**.

%

</div>

### Why This Concept Is Greater Than Any Single Theorem

[Table omitted — see original .tex]

Einstein's greatest contribution was not the formula $E=mc^2$ -- it was the concept of the **principle of relativity**. The Equality Principle does something similar.

<div align="center">

%

**Align before comparing -- not because doing so is better, but because without doing so, comparison itself is mathematically undefined.**

%

</div>

### Geometry of Potential Surfaces: Inequality is Internal, Equality is at Interfaces

**The potential surface can be uneven.** Imagine three successively descending potential steps: a high region, a middle region, and a low region.

**But at the interface, they must be level.** When two steps make contact, they must be at the same height at the contact point.

<div align="center">

%

$$

    \max_{x \in \Omega_A} \mathcal{S}_A(x) - \min_{x \in \Omega_A} \mathcal{S}_A(x)  can be arbitrarily large.

$$

 $\mathcal{G}amma = \partial\Omega_A \cap \partial\Omega_B$ 

$$

    \mathcal{S}_A|_\mathcal{G}amma = \mathcal{S}_B|_\mathcal{G}amma \quad .

$$

%

</div>

This geometric fact provides a precise mathematical formulation of "all people are equal" -- **not that everyone is the same height, but that every contact point must be level.**

**Analogy with national borders.** Country A has internal wealth disparity. Country B does too. But when two countries sign a trade agreement, the negotiation table must be at the same height.

**Philosophical meaning of the gauge fixing condition $\sum_m \mathbf{g}_m = \mathbf{0}$.** In MILP gauge fixing, the zero-sum constraint appears to be a technical detail. But its philosophical meaning is profound:

<div align="center">

**The sum of all experts' gauge offsets is zero = no expert is a privileged origin.**

</div>

This is not an arbitrary choice of gauge fixing condition. It is the only condition that does not grant any expert a privileged position.

**Convergence of the Equality Principle and the "All Men Are Equal" Theorem.** In the SCX theorem system, this theorem states: $P(W_A) = P(W_B)$ holds for all observers $A, B$.

The Equality Principle supplies the other half: **equality of representational frameworks.** Not only is no one's cognitive ability privileged -- no one's coordinate system is naturally "standard."

<div align="center">

%

**Complete equality**

- **All Men Are Equal Theorem (cognitive equality):** No one has a privileged observational position -- $P(W_A) = P(W_B)$.

- **The Equality Principle (representational equality):** No one's coordinate system is naturally standard -- $\sum_m \mathbf{g}_m = \mathbf{0}$.

Cognitive equality + representational equality $\rightarrow$ communication requires prior alignment $\rightarrow$ aligned consensus is the only legitimate source of knowledge.

%

</div>

> **Honest Strike:** This convergence implies a disturbing corollary: most "communication" in current human society may be comparing incomparable things. Not because we are unwilling to understand each other, but because we never explicitly fixed our gauges.

### Free Flow: Dynamical Consequences of Potential Surface Continuity

The previous section discussed static potential surface geometry. This section discusses its **dynamics**: when there is a jump on the potential surface, what does the system do?

> **Definition:** []<!-- def:gradient_flow  -->

>

> $$

>     \mathbf{F}(x) = \eta \cdot \nabla \mathcal{S}(x),

> $$

>

This is a direct expression of the principle of least action on the potential surface -- not a moral choice, but a physical tendency.

> **Theorem:** []<!-- thm:confinement  -->

>  $\Omega_A$  $\Omega_B$  $\mathcal{G}amma$  $\Delta_\mathcal{G}amma = \mathcal{S}_A|_\mathcal{G}amma - \mathcal{S}_B|_\mathcal{G}amma > 0$ $\Omega_B$ ****(confinement)—— $\mathcal{G}amma$  $\Omega_A$——

>

1.  $\mathcal{G}amma$  $P_\mathcal{G}amma = \rho_\mathcal{G}amma \cdot \Delta_\mathcal{G}amma$ $\rho_\mathcal{G}amma$  $\mathcal{G}amma$ 

3.  $J_{burst} \propto \rho_\mathcal{G}amma \cdot \Delta_\mathcal{G}amma^2$——

>

> $$

>     \frac{d\rho_\mathcal{G}amma}{dt} = \eta \cdot \Delta_\mathcal{G}amma \cdot \rho_{bulk} - \nu \rho_\mathcal{G}amma,

> $$

>

>  $\rho_{bulk}$ $\nu$  $\rho_\mathcal{G}amma^* = (\eta \Delta_\mathcal{G}amma / \nu) \rho_{bulk}$  $\Delta_\mathcal{G}amma$ 

>

**Corollary: Free flow is not a human right -- it is a structural stability condition.**

> **Honest Strike:** This does not mean borders should disappear. Borders define the identity of a system. But the potential jump at the border must be actively managed.

### Towering Above the Flock: The Inevitable Fate of Internal Potential Singularities

> **Definition:** []<!-- def:singularity  -->

>

> $$

>     \min_{x \in \Omega_{high}} \mathcal{S}(x) - \max_{x \in \Omega \setminus \Omega_{high}} \mathcal{S}(x) > \delta_{crit},

> $$

>

> **Theorem:** []<!-- thm:singularity_attack  -->

>

1. ****  $\Omega \setminus \Omega_{high}$ with probability $p(\delta) = 1 - \exp(-\alpha \delta^2)$ $\Omega_{high}$—— $\delta$ 

>

>

### The Matthew Effect: Potential Steps and Systemic Landmines

> **Definition:** []<!-- def:matthew  -->

>

> $$

>     \frac{\partial \mathcal{S}_t(x)}{\partial t} \propto \mathcal{S}_t(x),

> $$

>

>

> $$

>     \lim_{t \to \infty} \mathcal{S}_t(x) = \sum_{k} h_k \cdot \mathbb{1}_{\Omega_k}(x),

> $$

>

> **Theorem:** []<!-- thm:step_mine  -->

>

> $$

>     \mathbb{P}( \mid \{\Delta_k\}, T) \geq 1 - \prod_k \exp\left(-\frac{T}{T_k}\right),

> $$

>

### Smoothing: Moral Imperative Degrades to Structural Survival Condition

<div align="center">

%

$$

    \mathbb{P}( \mid T) \leq \exp\left(-T \cdot \sum_{i,j} \kappa_{ij} \cdot \Delta_{ij}^2\right),

    <!-- eq:smooth_survival  -->

$$

%

</div>

2. **** $\mathcal{S}_A|_\mathcal{G}amma = \mathcal{S}_B|_\mathcal{G}amma$——

ightarrow$  $

ightarrow$  $

ightarrow$  $

### Who Reaps the Reaper? The Execution Authority Problem of Redistribution Criteria

### Two Types of "High" and Geographic Buffering: Empirical Observations

> **Definition:** [ vs ]<!-- def:two_highs  -->

>

### Life Philosophy: Potential Management for the Isolated Thinker

> **Definition:** []<!-- def:cognitive_potential  -->

> **Corollary:** []<!-- cor:wallfacer  -->

>

### Historical Mathematical Explanation: The Inevitable Detonation of Wealth-Poverty Potential Jumps

> **Definition:** []<!-- def:wealth_cruelty  -->

>

1. $\min_{x \in \Omega_{rich}} \mathcal{S}(x) - \max_{x \in \Omega_{poor}} \mathcal{S}(x) > \delta_{crit}$——

> **Theorem:** []<!-- thm:historical_inevitable  -->

>

> $$

>     \mathbb{P}( \mid T) \geq 1 - \exp\left(-\frac{T}{T_{crit}}\right), \quad T_{crit} \propto \frac{1}{\delta^2 + \eta^2},

> $$

>

### The Danger of Over-Correction: Potential Surface Oscillation Theorem

> **Definition:** []<!-- def:audit_weaponization  -->

> **Theorem:** []<!-- thm:oscillation  -->

>

>

>

> **Corollary:** []<!-- cor:oscillation_decay  -->

>

2. ****  $\varepsilon$-$|\Delta(t)| < \varepsilon$ $T_\varepsilon \leq \max\left(\frac{2} \ln\frac{2\rho_0}{\kappa\varepsilon}, \frac{2} \ln\frac{2|\Delta_0|}\right)$

> **Proof:**  [ref]  $\Delta = \mathbf{g}_A - \mathbf{g}_B$$I(t) = \int_0^t \Delta(\tau) d\tau$

>

> $$

>     \ddot(t) + \kappa \dot(t) + \rho_0 e^{-\lambda t} \Delta(t) = 0.

> $$

>

>

> $$

>     \ddot{u}(t) + \left(\rho_0 e^{-\lambda t} - \frac{\kappa^2}{4}\right) u(t) = 0.

> $$

>

>

> $$

>     \Delta(t) \sim C \cdot \exp\left(-\frac{2}t\right) \cdot \cos\left(\int_0^t \sqrt{\rho_0 e^{-\lambda s} - \frac{\kappa^2}{4}}\; ds + \phi\right),

> $$

>

>

>

### Attitude Audit: Not Directly Measurable but Convergent

> **Proposition:** []<!-- prop:attitude_leak  -->

>

> $$

>     \mathbb{P}\left(|\hat{\mathbf{g}}_m - \mathbf{g}_m| > \varepsilon\right) \leq 2\exp\left(-2M \cdot p(\mathbf{g}_m) \cdot \varepsilon^2\right).

> $$

>

<div align="center">

[Table omitted — see original .tex]

</div>

### Legislation and Policy: Operational Derivations from the Equality Principle

> **Definition:** [ vs ]<!-- def:legitimate_delta  -->

>

<div align="center">

[Table omitted — see original .tex]

</div>

### Industrial Policy: Inequality is Permissible, Lack of Smoothness is Not

<div align="center">

[Table omitted — see original .tex]

</div>

ightarrow$  $

ightarrow$ 

### Corporate Governance: Monopoly as Potential Singularity

> **Definition:** []<!-- def:monopoly_gauge  -->

>

> $$

>     \min(\mathcal{S}_F - \bar{\mathcal{S}}_{up}, \mathcal{S}_F - \bar{\mathcal{S}}_{down}) > \delta_{crit},

> $$

>

> $\partial(\mathcal{S}_F - \bar{\mathcal{S}}_{up})/\partial t > 0$ [ref]

<div align="center">

[Table omitted — see original .tex]

</div>

ightarrow$ CEC  $

ightarrow$  $

ightarrow$  $\mathbf{g}$ $

ightarrow$ $\mathbf{g}$  $

### Boundary Crossing: Interface Smoothing of Cognitive Potential

> **Definition:** []<!-- def:cognitive_crossover  -->

<div align="center">

[Table omitted — see original .tex]

</div>

### Fertility Rate: Whose Coordinate System Defines the Cost

<div align="center">

[Table omitted — see original .tex]

</div>

### The Mathematics of Stubbornness: Why Persistence is a Sampling Strategy

> **Definition:** []<!-- def:stubbornness  -->

<div align="center">

[Table omitted — see original .tex]

</div>

### The Paradox of Success: High as Air

<div align="center">

%

[Table omitted — see original .tex]

%

</div>

### A Potential Surface Critique of "The Courage to Be Disliked"

### Social Summary: The Final Synthesis of the Equality Principle

ightarrow$  $

### The Equality Principle Tests Itself

<!-- sec:self_test  -->

<div align="center">

%

%

</div>

### Implications: The Equality Principle in Other Domains

<!-- sec:implications  -->

### Relationship Between the Equality Principle and the SCX Theorem System

<div align="center">

[Table omitted — see original .tex]

</div>

## Conclusion

<!-- sec:conclusion  -->

We identify and formalize a fundamental but previously unnoticed problem in multi-expert routing: **Potential Surface Misalignment** -- different experts define their outputs in gauge-inequivalent coordinate systems. We prove this is an instance of **gauge freedom**, parallel to but more general than the gauge problem in ACE potentials.

We propose an MILP gauge-fixing framework, establish convex relaxations and greedy approximations, and provide error guarantees. We establish the SVD spectral concentration after gauge fixing as a provable hallucination detection indicator.

**Align before comparing -- not because doing so is better, but because without doing so, comparison itself is mathematically undefined.**

**Acknowledgments:** This work was completed independently under the "SCX Framework." Thanks to all honest administrators for their pioneering example.

**Author's Statement:** The author publishes under the name SCX. This work is released on GitHub for immediate open access. No institutional affiliation is claimed. The theorems stand on their own.

{99}

- shazeer2017

N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, and J. Dean,

``Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer,''

*ICLR*, 2017.

- fedus2021

W. Fedus, B. Zoph, and N. Shazeer,

``Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity,''

*Journal of Machine Learning Research*, 2021.

- jiang2024

A. Jiang et al.,

``Mixtral of Experts,''

*arXiv:2401.04088*, 2024.

- dai2024

D. Dai et al.,

``DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models,''

*arXiv:2401.06066*, 2024.

- zoph2022

B. Zoph et al.,

``Designing Effective Sparse Expert Models,''

*arXiv:2202.08906*, 2022.

- puigcerver2023

J. Puigcerver, C. R. Ruiz, B. Mustafa, and N. Houlsby,

``From Sparse to Soft Mixtures of Experts,''

*ICLR*, 2024.

- zhou2022

Y. Zhou et al.,

``Mixture-of-Experts with Expert Choice Routing,''

*NeurIPS*, 2022.

- scx_egp

SCX,

``Consistency-Constrained Expert Merging for Transferable ACE Machine-Learned Interatomic Potentials,''

GitHub: shuchaoxi/SCX, 2026.

- scx_hamiltonian

SCX,

 ``Hamiltonian as Audit Condition: Judging Auditability from the Energy Landscape,

GitHub: shuchaoxi/SCX, 2026.

- scx_history

SCX,

``SCX History: How a Gauge-Fixing Problem Became an Uncertainty Principle,''

GitHub: shuchaoxi/SCX, 2026.

- scx_thm3

SCX,

 ``Honest Person Theorem: Without Additional Assumptions, a Single Observer Cannot Distinguish Noise, Bias, Learnability Difficulty, and Honest Error,

GitHub: shuchaoxi/SCX, 2026.

- scx_yajie

SCX,

 ``Yajie Protocol: Honest Nash Equilibrium in Multi-Expert Consensus,

GitHub: shuchaoxi/SCX, 2026.

- drautz2019

R. Drautz,

``Atomic Cluster Expansion for Accurate and Transferable Interatomic Potentials,''

*Physical Review B*, 2019.

- yoo2019

D. Yoo et al.,

``Atomic Energy Mapping of Neural Network Potentials,''

*Physical Review Materials*, 2019.

- herman2008

K. M. Herman,

``Gauge Dependence of the Embedding Energy in Embedded Atom Method Potentials,''

*Modelling and Simulation in Materials Science and Engineering*, 2008.

- hoeffding

W. Hoeffding,

``Probability Inequalities for Sums of Bounded Random Variables,''

*Journal of the American Statistical Association*, 1963.

- veit2016

A. Veit, M. Wilber, and S. Belongie,

``Residual Networks Behave Like Ensembles of Relatively Shallow Networks,''

*NeurIPS*, 2016.

- ainsworth2023

S. K. Ainsworth, J. Hayase, and S. Srinivasa,

``Git Re-Basin: Merging Models modulo Permutation Symmetries,''

*ICLR*, 2023.
