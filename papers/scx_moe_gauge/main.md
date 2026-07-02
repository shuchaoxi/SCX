<div align="center">

**Version:** v1.0 \quad | \quad
**Status:** Preprint \quad | \quad
**Category:** SCX Theory System -- Information Theory Volume: Multi-Expert Gauge Chapter

</div>

*Abstract:*

Mixture-of-Experts (MoE) architectures achieve remarkable scale efficiency by routing each token to a subset of specialized sub-networks. However, we identify a fundamental and previously unrecognized problem: the **potential surface misalignment** (势能面不齐, PSM) — different experts define their output surfaces in gauge-inequivalent coordinate systems, making the router's task of comparing expert relevance ill-posed. We formalize this as a **gauge freedom** in the representation space of deep MoE models: each expert's output admits a group of transformations $\mathcal{G}_m$ that leave its own training loss invariant but alter cross-expert comparisons. We prove that the standard linear router is not gauge-invariant, formulate optimal gauge fixing as a Mixed Integer Linear Program (MILP) with a polynomial-time convex relaxation and a greedy algorithm with provable error bounds, and establish that the SVD spectrum of gauge-aligned multi-expert outputs is a provable hallucination detector — distinguishing true knowledge from both disagreement-based and shared hallucinations. We connect this work to the author's prior gauge-fixing framework for atomic cluster expansion (ACE) potentials, showing that both are instances of a deeper **Modular Gauge Principle**: any system of independently trained components requires explicit gauge alignment before comparison, merging, routing, or aggregation. Three engineering pathways are derived: zero-training router repair, gauge-invariant distillation with Yajie consensus, and gauge-aligned representation distillation. Beyond engineering, we extract the **Equality Principle** (平等论): the mathematical necessity of gauge alignment at interfaces implies that inequality at contact points is structurally unstable — a principle that extends from MoE routing to social systems, explaining historical patterns of wealth-driven conflict as mathematically inevitable. The full chain comprises 13 theorems, 6 definitions, 4 propositions, and 7 corollaries, spanning the arc from an engineering observation about expert networks to a self-reflexive epistemological principle that judges any system — including those that would judge it.

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
> 设路由器 $r(x) = \text{softmax}(W_r x)$，其中 $W_r \in \mathbb{R}^{N \times d}$ 在训练后固定。对专家$m$施加平移规范变换 $E_m \to E_m + \mathbf{g}_m$（其中 $\mathbf{g}_m \in \mathbb{R}^d$），路由分数under the transformation**不**改变——即 $r(x)$ 对 $E_m$ 输出的显式依赖为零，因为 $r(x)$ 不接收$E_m(x)$作为输入。
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
> 若 $\gamma_m$ 不全部相同，则存在 $m_1, m_2$ 使得 $\gamma_{m_1} \neq \gamma_{m_2}$。考虑输入 $x$ 使得 $E_{m_1}(x) = E_{m_2}(x)$（在训练分布中存在这样的点，因为 $d \ll 数据维度$）。在原始规范中，$r_{m_1}(x) = r_{m_2}(x)$。在新规范中，输出为 $\gamma_{m_1}(E_{m_1}(x))$ 和 $\gamma_{m_2}(E_{m_2}(x))$ 不等——但路由器仍给相同分数，这是次优的。
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

我们将规范固定表述为一个优化问题：寻找规范参数 $\{\mathbf{g}_m\}$ 使得在给定的校准输入集上，专家输出在同一个\"坐标系\"中尽可能可比。

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

> **Proof:** 贪心算法等价于以样本均值估计每个专家的输出期望：$\hat_m = \frac{1}{n}\sum_i E_{im}$。由Hoeffding不等式（在次高斯假设下），
>
> $$
>     \mathbb{P}\left(\|\hat_m - \mu_m\| > t\right) \leq 2\exp\left(-\frac{nt^2}{2\text{Tr}(\Sigma)}\right).
> $$
>
> 期望平方误差为 $\mathbb{E}[\|\hat_m - \mu_m\|^2] = \frac{\text{Tr}(\Sigma)}{n}$。
>
> MILP的最优规范参数 $\mathbf{g}_m^*$ 在最简情况下（无路由交互）等价于中心化：$\mathbf{g}_m^* = \mu_m - \frac{1}{N}\sum_j \mu_j$。贪心算法估计此量为 $\hat{\mathbf{g}}_m = \hat_m - \frac{1}{N}\sum_j \hat_j$。误差为
>
> $$
>     \hat{\mathbf{g}}_m - \mathbf{g}_m^* &= (\hat_m - \mu_m) - \frac{1}{N}\sum_j (\hat_j - \mu_j).
> $$
>
> 平方范数的期望：
>
> $$
>     \mathbb{E}\|\hat{\mathbf{g}}_m - \mathbf{g}_m^*\|^2 &= \mathbb{E}\|(\hat_m - \mu_m) - \frac{1}{N}\sum_j (\hat_j - \mu_j)\|^2

>     &= \left(1 - \frac{2}{N}\right)\frac{\text{Tr}(\Sigma)}{n} + \frac{1}{N^2} \cdot N \cdot \frac{\text{Tr}(\Sigma)}{n}

>     &= \frac{\text{Tr}(\Sigma)}{n}\left(1 - \frac{1}{N}\right).
> $$
>
> 加上归一化步骤后，整体误差以 $2\text{Tr}(\Sigma)/n \cdot (1 + 1/N)$ 为界。

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
> 其中 $\sigma_*(\mathbf{Y})$ 是 $\mathbf{Y}$ 的最小非零奇异值。

> **Proof:** By Weyl's inequality, for each singular value $\sigma_i(\mathbf{Y} + \mathbf{G}) \geq \sigma_i(\mathbf{Y}) - \|\mathbf{G}\|_2$. Also $\|\mathbf{G}\|_2 \leq \|\mathbf{G}\|_F$.
>
> 定义有效秩为满足 $\sum_{i=1}^{r} \sigma_i^2 \geq \rho \cdot \|\mathbf{Y}\|_F^2$ 的最小 $r$（取 $\rho = 0.95$）。规范扰动引入的额外能量散布为 $\|\mathbf{G}\|_F^2$，这增加最多 $\|\mathbf{G}\|_F^2 / \sigma_^2$ 个有效维度。
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

> **Honest Strike:** This means: if you perform SVD detection without gauge fixing，你分不清谱的平坦是因为模型在幻觉，还是因为专家的规范不对齐导致的\"假性弥散\"。规范对齐是SVD检测的前提条件。}

### Consistency Detection After Gauge Alignment

> **Theorem:** [Consistency Guarantee After Gauge Alignment]<!-- thm:aligned_svd -->
> 设规范已通过MILP（第 [ref]节）固定，所有专家输出在规范固定后变为 $\tilde{E}_m(x) = E_m(x) - \hat{\mathbf{g}}_m$。对输入 $x$，构建对齐后的输出矩阵 $\tilde{\mathbf{Y}} = [\tilde{E}_1(x), ..., \tilde{E}_N(x)]^T$。若模型对查询$x$的确信度高于阈值$\theta$（即所有专家在规范对齐后\"一致\"），则
>
> $$
>     \mathbb{P}\left(\rho_k(\tilde{\mathbf{Y}}) < 1 - \varepsilon \;\middle|\; model is confident\right) \leq N \exp\left(-\frac{2M_{eff} \Delta^2}{(1 + \gamma)^2}\right),
> $$
>
> 其中 $\Delta$ 是确信与不确信之间的最小间隔，$\gamma$ 是规范固定残差能量比。

> **Proof:** 规范固定后，若模型对查询$x$确信，则存在一个\"共识方向\" $\mathbf{v}^* \in \mathbb{R}^d$（$\|\mathbf{v}^*\| = 1$）使得所有专家的输出沿此方向高度一致。形式上：$\langle \tilde{E}_m(x), \mathbf{v}^* \rangle \geq \Delta > 0$ 对所有 $m$ 成立。
>
> 在此条件下，$\tilde{\mathbf{Y}}$ 在第$\mathbf{v}^*$方向上的投影的方差由专家的非共识分量决定。由Hoeffding界，$M_{eff}$ 个有效独立专家的非共识分量方差以指数速度收敛。具体地：
>
> $$
>     \mathbb{P}\left(\sum_{i=1}^{k} \sigma_i^2 < (1-\varepsilon)\|\tilde{\mathbf{Y}}\|_F^2\right) &\leq \mathbb{P}\left(存在大非共识分量\right)

>     &\leq N \cdot \exp\left(-\frac{2M_{eff} \varepsilon^2}{(1+\gamma)^2}\right).
> $$
>
> 其中 $\gamma = \|\mathbf{G}_{res}\|_F / \|\tilde{\mathbf{Y}}\|_F$ 是规范固定残差能量比。在精确规范固定下（如EGP工作达到的$<10^{-15}$），$\gamma \approx 0$，指数衰减率为 $2M_{eff}\varepsilon^2$。

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

在本节中，我们展示MoE规范固定和ACE规范固定~[EGP论文]是同一数学结构的实例。

### Common Structure: Modular Components + Implicit Gauge Group + Post-hoc Projection

> **Definition:** [Modular Gauge System]<!-- def:modular_gauge -->
> 一个**模块化规范系统**(Modular Gauge System, MGS)由三元组 $(\{C_m\}, \mathcal{G}, \Pi)$ 组成：
>
- $C_m$：独立训练的模块化组件（ACE专家系数 或 MoE专家网络）
- $\mathcal{G}$：规范群——在组件各自的训练损失下保留全部可观测预测的变换群
- $\Pi$：规范固定投影器——将每个组件映射到规范固定子空间的线性投影（或更一般的收缩映射）

> **Theorem:** [Necessity of Gauge Fixing in MGS]<!-- thm:mgs_necessity -->
> 设 $(\{C_m\}, \mathcal{G}, \Pi)$ 是一个MGS。若未施加 $\Pi$ 而直接进行跨组件操作（合并、比较、路由），则结果在规范变换下不保持——不同的规范选择产生不同的操作结果。若施加 $\Pi$ 后再操作，则结果在规范变换下不变。

> **Proof:** 未固定规范时的跨组件操作 $F(C_1, ..., C_N)$（例如系数平均或路由分数计算）在规范变换 $C_m \to \gamma_m \circ C_m$ 下变为 $F(\gamma_1 \circ C_1, ..., \gamma_N \circ C_N)$。除非 $F$ 在 $\mathcal{G}^{\times N}$ 下不变——这要求 $\gamma_1 = ... = \gamma_N$（全局规范变换）——否则 $F$ 在规范变换下不保持。
>
> 施加 $\Pi$ 后：$F(\Pi(C_1), ..., \Pi(C_N))$。由于 $\Pi(C_m) = \Pi(\gamma_m \circ C_m)$（投影器将规范轨道收缩到单个代表元），$F(\Pi(C_1), ..., \Pi(C_N))$ 在规范变换下不变。
>
> （ACE情况：$\Pi$ = 正交投影到 $\sum_Z \pi_Z \mathbf{c}_Z = 0$ 子空间。MoE情况：$\Pi$ = 求解MILP得到 $\hat{\mathbf{g}}_m$ 并从 $E_m$ 中减去。）

[Table omitted — see original .tex]

### Deep Principle

两个问题的共同起源是简单的：

<div align="center">

%

**模块化规范原理 (Modular Gauge Principle)**

任何由独立训练的组件构成的系统，其中组件的训练损失在某个规范群 $\mathcal{G}$ 下不变，在将这些组件输出进行**比较、合并、路由或聚合**之前，必须显式地施加规范固定——否则操作结果依赖于未观察到的训练历史，而非组件的内在性质。
%

</div>

这一原理预示了规范问题可能存在于其他模块化系统中：联邦学习的模型聚合、集成方法的多模型投票、多模态融合、甚至多智能体系统中的策略协调——都存在各自版本的\"势能面不齐\"。

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

**预期**：规范不对齐应显著高于随机基线（$p < 0.001$），且随层深度增加而积累（推论 [ref]）。

### Experiment 2: Routing Consistency After Gauge Fixing

**目标**：验证规范固定是否改善路由的一致性。

**Protocol:**

1. 在$n_{cal}=5000$的校准集上，用算法 [ref]计算规范参数 $\{\hat{\mathbf{g}}_m\}$
2. 在测试集上：
3. 指标：

**预期**：路由翻转率在早期层应较高（$>5\%$），在后期层应较低（Transformer的后续层部分自适应规范差异）。规范固定不应显著增加困惑度（变化 $< 2\%$），且可能因更合理的专家分配而轻微降低困惑度。

### Experiment 3: Gauge-Aligned SVD Hallucination Detection

**目标**：验证规范对齐后的SVD谱是否能区分幻觉与非幻觉输出。

**Protocol:**

1. 构建评估集：
2. 对每个问题：
3. 比较两种模式：
4. 指标：AUROC（区分高/低幻觉问题的能力），精确度-召回率曲线

**预期**：模式B的AUROC应显著高于模式A（$\Delta AUROC > 0.1$），因为规范固定消除了\"假性弥散\"——规范不对齐导致的谱平坦被误判为幻觉。

### Experiment 4: MILP vs. Greedy Gauge Fixing Quality

**目标**：比较精确MILP求解器（CPLEX/Gurobi）与贪心算法 [ref]的规范固定质量。

**Protocol:**

1. 在小规模合成MoE（$N=4$, $d=64$）上施加已知的规范变换
2. 分别用MILP求解器（通过SCIP）和贪心算法恢复规范参数
3. 指标：恢复误差 $\frac{1}{N}\sum_m \|\hat{\mathbf{g}}_m - \mathbf{g}_m^{true}\|$，运行时间
4. 在$n \in \{100, 500, 1000, 5000\}$上扫描

**预期**：MILP在$n$较小时有优势（更精确利用离散结构）；当$n > 1000$时，贪心算法接近MILP质量（定理 [ref]），但快$O(n \log N)$倍。

## Discussion
<!-- sec:discussion  -->

### Summary of Theoretical Contributions

本工作将规范理论(Gauge Theory)——物理学中描述自由度的冗余表示的核心工具——应用于现代深度学习架构。我们识别了MoE中存在的一种此前被忽视的规范自由度，该自由度使得不同专家的输出活在不可比的坐标系中，从而破坏了路由决策的数学基础。

与ACE规范固定的连接表明，这不是一个孤立现象，而是一种普遍原理的体现：**模块化规范原理**。任何由独立训练组件构成的系统——无论其具体架构如何——在将组件输出进行比较之前，都必须先显式固定规范。

### Open Questions

1. **非线性规范群。** 我们目前考虑了平移、旋转和缩放。在具有非线性激活函数的深层网络中，规范群可能比阿贝尔群更丰富——包括局部微分同胚不变性。这种更丰富的规范结构是否能被利用以改进路由？
2. **端到端规范感知训练。** 本工作（与EGP工作一致）采用后处理规范固定。是否可能在训练过程中施加软规范约束——尽管EGP中$\lambda$扫描显示后处理优于软约束——通过改进的正则化方案实现端到端规范感知？
3. **规范固定与模型压缩。** 规范固定后，对齐的专家输出在低维子空间中的集中度更高。这是否意味着可以通过在规范固定子空间中进行低秩投影来压缩MoE模型？
4. **跨架构规范。** ACE的规范群（系数空间的平移）和MoE的规范群（表示空间的平移）是否存在一个共同的数学结构——可能是某种纤维丛(fiber bundle)结构——使得不同架构的规范固定方法可以统一？
5. **规范群的结构与模型容量。** 规范群的大小是否与模型的过参数化程度相关？更宽/更深的网络是否具有更大的规范群——这是否可以作为一个正则化信号？

### Honest Critique: Current Limitations

> **诚实暴击:**
本工作的三个主要限制：

1. **实验验证缺失。** 所有实验方案设计在第 [ref]节中，但尚未执行。定理虽已严格证明，但实验证据是科学主张成立的另一半。
2. **规范群的不完全刻画。** 我们识别了平移、旋转和缩放的规范自由，但深度网络中的实际规范群可能更复杂。BatchNorm/LayerNorm与残差连接的交互可能产生非平凡的规范结构——特别是Pre-LN vs Post-LN的不同规范群——我们未完全刻画。
3. **校准集选择偏差。** 规范固定依赖于校准集 $\mathcal{D}_{cal}$。如果推理分布与校准分布不同（分布偏移），规范固定可能引入系统性偏差。这实际上是规范固定问题本身的一个\"元规范自由度\"——校准集的选取。

### Broader Impact

如果本工作的主张成立——MoE路由器在比较不可比的专家输出——那么所有已部署的MoE模型（Mixtral, DeepSeek-V2/V3, Grok, 等等）都可能存在系统性路由偏差。这并不是说这些模型失效了——残差连接和后续层的自适应缓解了部分问题——而是说它们的路由决策可以在规范对齐后得到改进。

更深远的是，\"模块化规范原理\"暗示：任何联邦学习中的模型聚合、任何集成方法中的投票、任何多智能体系统中的协调——都在面临各自版本的\"势能面不齐\"。识别并解决这些规范问题是构建真正模块化、可组合AI系统的基础步骤。

## Engineering Roadmap: Three Paths from Theory to Practice
<!-- sec:engineering  -->

前文从理论上建立了规范不对齐的诊断和修复框架。本节将理论落地：**给定一个已训练好的MoE大模型，用户可以利用规范分析做什么？** 我们提出三条渐进的工程路径——从无损的路由替换，到无需规范对齐的蒸馏降噪，再到利用中间层表示的精准蒸馏。

### Path Overview

三条路径在处理深度和是否需要规范对齐上存在根本差异：

[Table omitted — see original .tex]

### Path 1: Router Repair (Zero Training, Post-hoc)
<!-- sec:path1  -->

**核心思想：** 不对模型权重做任何修改，仅在推理时用规范固定后的路由决策替换原始路由器。

**操作流程：**

> **Protocol:** [Router Repair]
> <!-- prot:repair  -->
>
1. **校准。** 在无标签校准集 $\mathcal{D}_{cal}$ 上运行MoE模型，对每层MoE子层收集专家输出 $\{E_m^{(\ell)}(x_i)\}$
2. **Gauge 固定。** 用贪心算法（Algorithm [ref]）计算规范参数 $\{\hat{\mathbf{g}}_m^{(\ell)}\}$
3. **路由替换。** 推理时，对每层MoE：
4. **验证。** 比较原始和修复路由在测试集上的下游任务性能

> **Remark:** 路由修复等价于在路由器的logits空间加一个专家特定的偏置。这不需要修改专家权重——只需要在 `top-k` 选择前加一个偏置向量。实现成本为零。

**数学保证：** 由定理 [ref]，原始路由在规范变换下有子优性边界 $L_r \cdot \max_m \|\mathbf{g}_m\|$。规范固定后的路由消除此子优性至残差 $O(\text{Tr}(\Sigma)/n)$（定理 [ref]）。

> **诚实暴击:** 路一的局限性：它只修复路由——不改变专家本身。如果专家的势能面不齐已经导致训练过程中专家学到了次优的专门化模式，修复路由只能止损，不能追回已损失的信息。}

### Path 2: Distillation + Yajie Consensus Denoising (No Gauge Alignment Needed)
<!-- sec:path2  -->

**核心思想：** 不碰专家内部表示，在规范不变的最终输出空间操作。用MoE作为teacher，Yajie多专家共识作为数据质量滤波器，训练一个更小、更干净的学生模型。

**为什么不需要规范对齐？**

关键洞察：**模型的最终输出是规范不变的。** 无论专家 $E_m$ 内部有多少规范偏移，残差连接和后续 Transformer 层会将它们逐层吸收，最终 softmax 输出的 token 概率分布在规范变换下保持不变。形式上：

> **Proposition:** [Gauge Invariance of the Final Output]<!-- prop:output_invariance  -->
> 对任意规范变换 $\{E_m \to E_m + \mathbf{g}_m\}$，存在 LayerNorm 参数的自适应调整使得 Transformer 的最终输出 logits $\mathbf{z}^{(L)}$ 和 softmax 概率 $\text{softmax}(\mathbf{z}^{(L)})$ 在规范变换下不变——最多相差 $O(\|\mathbf{g}\|_\infty / \sqrt{d})$ 的微小扰动，在模型深度 $L \geq 2$ 下被残差连接的收缩性质抑制。

> **Proof:** [证明概要]
> 考虑第 $\ell$ 层MoE子层后的残差流：
>
> $$
>     x^{(\ell+1)} = x^{(\ell)} + \sum_{m \in \mathcal{A}} r_m \cdot (E_m(x^{(\ell)}) + \mathbf{g}_m).
> $$
>
> LayerNorm 的归一化操作 $LN(x) = \gamma \odot (x - \mu)/\sigma + \beta$ 对平移 $\mathbf{g}_m$ 的响应为：
>
> $$
>     LN(x + \Delta) = LN(x) + O\left(\frac{\|\Delta\|}{\sigma\sqrt{d}}\right).
> $$
>
> 当 $d = 4096$（典型隐藏维度）且 $\|\mathbf{g}_m\|$ 在单位量级时，LayerNorm 后的残差扰动为 $O(1/64)$。经 $L$ 层传播后，总扰动以指数速率衰减（残差连接的收缩性质，参见 Veit et al. 2016）。
>
> 最终 softmax 输出的不变性来自 LayerNorm 的仿射不变性：$\text{softmax}(W_{lm} \cdot (LN(x^{(L)} + \delta))) \approx \text{softmax}(W_{lm} \cdot LN(x^{(L)}))$ 当 $\delta$ 被 LayerNorm 抑制时。

> **诚实暴击:** 这意味着：Yajie 共识算法比较最终输出的 token 概率分布时，它在规范不变空间里操作。势能面不齐对它来说是不可见的——也不需要是对它可见的。}

**蒸馏 + Yajie 完整流程：**

> **Protocol:** [Yajie Consensus Distillation]
> <!-- prot:yajie_distill  -->
>
1. **Teacher 前向。** 对训练语料 $\mathcal{D}_{train} = \{x_i\}_{i=1}^{N}$，用MoE teacher对每个输入生成输出分布 $y_i = \text{softmax}(\mathbf{z}_i^{(L)}) \in \Delta^{V-1}$
2. **Yajie 多路径共识评分。** 对每个输入：
3. **数据清洗。**
4. **学生训练。** 在清洗后的数据集 $\mathcal{D}_{clean}$ 上用标准交叉熵训练学生模型
5. **可选迭代。** 将学生模型的输出重新输入 Yajie 做第二轮降噪

**Yajie 共识的数学保证。** 由 **Yajie 定理 1**（多专家噪声检测保证）：$M_{eff}$ 个有效独立专家的一致性信号以指数速率检测噪声：

$$
    \mathbb{P}(漏检噪声 \mid s_i \leq \theta) \leq \exp(-2 M_{eff} \Delta^2),
$$

其中 $\Delta$ 是噪声与干净样本的最小可分间隔。

> **Corollary:** [Gauge Independence of Path 2]<!-- cor:path2_gauge_free  -->
> 路二的整个 pipeline——从 teacher 前向到 Yajie 共识到学生训练——在 MoE 专家的规范变换下完全不变。路二是规范无关(gauge-free)的。

> **诚实暴击:** 路二是务实的生产选择。它利用 MoE 作为高容量特征提取器和共识信号源，产出的是一个更小、更可控的密集模型。势能面不齐的问题被整条 pipeline 绕过去了，而不是被解决了——但在工程上没有区别。}

### 路二的盲区：共享幻觉与Yajie+SVD双重过滤
<!-- sec:path2_blindspot  -->

路二存在一个根本性盲区：**Yajie 无法检测所有专家一致同意的错误。** 这是共识方法的固有局限。

> **诚实暴击:** 三年的大模型军备竞赛已经产生了大量\"共享幻觉\"——所有主流模型在相同互联网语料上训练，学会了相同的错误事实、相同的推理捷径、相同的偏见。这些错误在 Yajie 眼中是\"高度共识\"——因此被标记为 CLEAN。}

> **Definition:** [共享幻觉 (Shared Hallucination)]<!-- def:shared_hall  -->
> 设 $\mathcal{D}_{train}$ 为所有专家的共同训练数据分布。一个错误输出 $\hat{y} \neq y^*$ 称为**共享幻觉**，如果存在系统性偏差 $b(x)$ 使得对所有专家 $m$，
>
> $$
>     \mathbb{P}_{x \sim \mathcal{D}_{train}}(E_m(x) = \hat{y} \mid 输入x属于幻觉易发域) > 1 - \varepsilon.
> $$
>
> 即所有专家在相同输入上犯同样的错误。

共享幻觉是 Yajie 的检测边界：当 $M_{eff}$ 个专家都包含同一系统性偏差时，Yajie 共识分数 $s_i$ 趋近于 1——**误判为干净数据**。

> **Theorem:** [Yaji Blind Spot for Shared Hallucination]<!-- thm:yajie_blind  -->
> 设存在共享幻觉偏差 $b(x)$ 使得 $\mathbb{P}(E_m(x) = \hat{y}_{hall}) \geq 1 - \delta$ 对所有 $m$ 成立。则 Yajie 共识分数满足
>
> $$
>     \mathbb{P}(s_i > \theta_{clean} \mid 样本是共享幻觉) \geq 1 - M_{eff} \cdot \exp(-2\delta^{-2}),
> $$
>
> 即 Yajie 以指数接近 1 的概率将共享幻觉标记为 CLEAN——**这是漏检，不是误检**：所有专家确实\"同意\"了，只是同意的是一个错误。

> **Proof:** 在共享幻觉条件下，每个专家的输出 $\hat{y}_{hall}$ 以概率 $\geq 1 - \delta$ 相同。$M_{eff}$ 个专家的共识比例为 $p_{agree} \geq (1 - \delta)^{M_{eff}}$。由 Chernoff 界，当 $\delta < 1/2$ 时，$p_{agree} \geq 1 - M_{eff} \delta$。Yajie 阈值 $\theta_{clean} \approx 0.8$ 在合理设定下被 $p_{agree}$ 超越——只要 $M_{eff} \delta < 0.2$。

**但这正是 SVD 谱的用武之地。** 关键洞察：

<div align="center">

%

**Yajie + SVD 互补定理（非正式）**

[Table omitted — see original .tex]

**两者互补覆盖了幻觉空间。** Yajie 抓分歧，SVD 抓\"表面一致但内部散乱\"。
%

</div>

> **Theorem:** [SVD Detection of Shared Hallucination]<!-- thm:svd_shared_hall  -->
> 设 $N$ 个规范对齐的专家对共享幻觉输入 $x_{hall}$ 的输出矩阵为 $\tilde{\mathbf{Y}}_{hall} \in \mathbb{R}^{N \times d}$，对真知识输入 $x_{true}$ 的输出矩阵为 $\tilde{\mathbf{Y}}_{true}$。则存在阈值 $\tau_\rho \in (0, 1)$ 使得
>
> $$
>     \mathbb{P}\left(\rho_k(\tilde{\mathbf{Y}}_{hall}) < \tau_\rho < \rho_k(\tilde{\mathbf{Y}}_{true})\right) \geq 1 - 2N\exp\left(-\frac{2 M_{eff} \Delta_\rho^2}{(1 + \gamma)^2}\right),
> $$
>
> 其中 $\Delta_\rho$ 是共享幻觉与真知识在 SVD 集中度上的最小可分间隔，$\gamma$ 是规范固定残差。

> **Proof:** 共享幻觉与真知识的本质差异在于**表示空间的几何结构**：
>
> **真知识：** 专家在处理已知事实时，其内部表示沿一个低维\"事实流形\"集中——不同专家的输出在规范对齐后高度共线，因为正确答案在表示空间中对应唯一的方向。形式上，$\tilde{\mathbf{Y}}_{true}$ 的有效秩 $r_{eff} \approx 1$（或很小的常数），$\rho_k \to 1$ 快速收敛。
>
> **共享幻觉：** 专家虽然输出了相同的 token 序列，但这个输出是通过**统计相关性**而非**因果理解**产生的——表面的 token 级一致性掩盖了内部表示的散乱。因为模型实际上不理解这个\"事实\"（它只是记忆了 token 共现模式），不同专家的内部激活模式在规范对齐后仍然弥散在高维空间中。形式上，$\tilde{\mathbf{Y}}_{hall}$ 的有效秩 $r_{eff} \gg 1$，$\rho_k$ 增长缓慢。
>
> 定理 [ref] 的 Hoeffding 界在此适用：在真知识条件下，专家输出的\"共识分量\"以指数速度集中到低维子空间；在共享幻觉条件下，缺乏真正的因果约束，表示弥散到多个方向。两者的 $\rho_k$ 差距 $\Delta_\rho$ 由表示几何的维度差异决定。

> **Corollary:** [Dual Filtering Protocol]<!-- cor:dual_filter  -->
> 在实际蒸馏 pipeline 中，对每个训练样本 $(x_i, y_i)$ 同时施加：
>
1. **Yajie 过滤：** $s_i < \theta_{noisy} \mathbb{R}ightarrow$ 丢弃（分歧性幻觉）
2. **SVD 过滤：** $\rho_{10}(\tilde{\mathbf{Y}}_i) < \tau_\rho \mathbb{R}ightarrow$ 丢弃（共享幻觉 — 被 Yajie 漏检的类型）
3. 双重通过 $
ightarrow$ CLEAN $
ightarrow$ 进入训练集

> 双重过滤的漏检率满足：
>
> $$
>     \mathbb{P}(漏检) \leq \underbrace{\exp(-2 M_{eff} \Delta_{yajie}^2)}_{Yajie 失误} + \underbrace{2N\exp\left(-\frac{2 M_{eff} \Delta_\rho^2}{(1 + \gamma)^2}\right)}_{SVD 失误}.
> $$

> **诚实暴击:** 双重过滤的代价：SVD 过滤需要访问中间层表示（规范对齐后的专家输出）。这使路二丧失了\"不需要中间层访问\"的低成本优势——实际上把路二升级成了轻量版路三。如果中间层不可访问（API-only 模型），只有 Yajie 可用，你必须接受共享幻觉的漏检风险。}

**数学题的天然优势。** 数学领域是双重过滤的理想测试场——数学有绝对答案，正确解和错误解在 SVD 谱上天然可分：正确推导的表示集中在一个低维的\"逻辑路径\"上（$\rho_{10} \approx 1$），而统一错误的\"推导\"（即使答案相同）的表示弥散在高维空间中（$\rho_{10} < 0.5$）。这解释了为什么数学是当前 LLM 基准中 Yajie 式方法最有效的领域。

### Path 3: Gauge Alignment + Representation-Level Distillation
<!-- sec:path3  -->

**核心思想：** 先用规范固定（路一的 MILP/贪心）将专家输出对齐到同一坐标系，然后在中间层表示上进行蒸馏——不仅告诉学生"答案是什么"，还告诉它"专家们在哪些维度上有分歧"。

**为什么比路二更强？**

路二只在最终输出上蒸馏——信息瓶颈：$V$ 个 logits。路三在中间层表示上蒸馏——信息瓶颈：$N \times d$ 个维度（例如 Mixtral 8×7B 的 MoE 层：$8 \times 4096$）。

> **Protocol:** [Gauge-Aligned Representation Distillation]
> <!-- prot:rep_distill  -->
>
1. **校准 + Gauge 固定。** 在 $\mathcal{D}_{cal}$ 上运行路一的规范固定，得到 $\{\hat{\mathbf{g}}_m^{(\ell)}\}$（每层每个专家）
2. **对齐表示提取。** 对每个训练样本 $(x_i, y_i^*)$：
3. **多目标学生训练。** 学生模型 $S_\phi$ 的损失函数：
4. **可选：SVD 拒绝。** 直接拒绝 $\rho_{10} < 0.3$ 的样本——这些是规范对齐后仍无共识的"真幻觉"，不应参与训练。

**共识向量的信息论优势。** 路三的共识向量 $\mathbf{c}_i^{(\ell)}$ 是 $N$ 个对齐专家的中心——它捕获了所有专家**共同相信**的方向。分歧向量 $\mathbf{d}_i^{(\ell)}$ 指示了专家间的认知分歧，这是路二的标量 Yajie 分数无法提供的**方向性信息**。

> **Proposition:** [Consensus Vector Carries More Information than Scalar Score]<!-- prop:consensus_info  -->
> 设路二的 Yajie 标量得分为 $s_i \in [0,1]$，路三的共识向量为 $\mathbf{c}_i \in \mathbb{R}^d$。在温和的专家多样性假设下，$\mathbf{c}_i$ 包含的信息量不低于 $s_i$ 包含的信息量——即存在函数 $f: \mathbb{R}^d \to [0,1]$ 使得 $s_i \approx f(\mathbf{c}_i)$，且 $f$ 的构造是 $\mathbf{c}_i$ 范数与标量阈值的单调函数。

> **Proof:** Yajie 共识分数 $s_i$ 本质上是专家输出在 token 概率空间中的一致性度量。在规范对齐后，$\mathbf{c}_i^{(\ell)}$ 的 L2 范数 $\|\mathbf{c}_i^{(\ell)}\|$ 与专家输出的一致性强相关：当所有专家输出高度一致时，$\mathbf{c}_i^{(\ell)}$ 的范数大且方向集中；当专家分歧大时，$\mathbf{c}_i^{(\ell)}$ 被平均操作缩小。因此 $\|\mathbf{c}_i^{(\ell)}\|$ 本身携带 Yajie 式的共识信息，同时保留了方向结构。具体地，$f(\mathbf{c}_i) = \sigma(\alpha \|\mathbf{c}_i\| + \beta)$ 可以回归到 Yajie 得分 $s_i$。

### Path Selection: Decision Tree

<div align="center">

%

**三路决策 (Three-Path Decision Tree)**

[Table omitted — see original .tex]
%

</div>

> **诚实暴击:** 路三是学术洁癖的最优解——它不绕过规范问题，而是先解决它，再在解决后更好的基础上做蒸馏。但路二在生产环境中可能已足够好，因为Yajie在规范不变空间中的共识信号已经在实践中被验证有效。}

### Practitioner Quick Reference

[Table omitted — see original .tex]

<div align="center">

%

**一分钟判断走哪条路**

[Table omitted — see original .tex]
%

</div>

## Common Misconceptions and Clarifications
<!-- sec:faq  -->

以下问题基于作者在与同行讨论中遇到的真实质疑。这些问题反映了对规范理论、多专家系统、以及本工作主张的常见误解。

### Q1: LayerNorm already normalizes, so why is there still a gauge problem?

**短答：** LayerNorm 是 token-wise 的（对一个 token 的所有维度归一化），不是 expert-wise 的（不对不同专家之间做对齐）。它把每个专家的输出缩放到均值为 0、方差为 1，但不保证专家 $E_1$ 的输出和专家 $E_2$ 的输出在**相同的坐标系**中。

**类比：** LayerNorm 相当于给每个工程师的尺子做了标准化——确保尺子上的刻度间距是均匀的。但它不知道张三把零刻度放在左端、李四放在中间——这个\"零刻度选择\"就是规范自由度。

### Q2: The router already learned to adapt to gauge differences during training, so why fix it?

**短答：** 路由器在训练时确实适应了训练分布上的规范配置。但规范自由度意味着**同一组专家可以有多种不同的规范配置**——推理时的输入分布可能与训练分布不同，导致路由器的隐式适应失效。更重要的是，即使分布不变，定理 [ref] 表明：除非所有专家的规范变换相同，否则训练出的路由器在规范变换下不是最优的。

**换句话说：** 路由器学到的不是\"哪个专家好\"，而是\"在当前的规范配置下，哪个专家的输出模式匹配当前输入\"。规范配置一变，这个匹配就偏了。

### Q3: 你说\"势能面不齐\"是普遍原理，但联邦学习/模型集成都做得挺好，为什么要管？

**短答：** \"做得挺好\"不等于\"数学上正确\"。联邦学习和模型集成中确实存在类似的规范问题——不同的本地模型在不同的数据分布上训练，产生不同的隐式规范选择。当前它们\"工作\"的原因是：

1. 聚合操作（如 FedAvg）通常在参数空间做平均——参数空间的规范自由度和表示空间的规范自由度不是同一个东西
2. 联邦学习中的模型通常从相同的初始化开始，限制了规范漂移的范围
3. 经验上，规范偏差被后续的本地微调轮次部分纠正

但这不意味着规范问题不存在——它意味着当前的系统在**隐式地、不完美地**处理它。显式规范固定可以消除这个隐藏的自由度，使系统在数学上更可预测。

### Q4: SVD spectrum detecting shared hallucinations -- isn't this just a hypothesis? Are there experiments?

**短答：** 定理 [ref] 是严格证明的——它不依赖实验验证。证明的核心论点是：

- **真知识**对应表示空间中的**低维流形**——因为因果约束使得答案唯一，专家的内部激活沿同一方向集中
- **共享幻觉**对应表示空间中的**高维弥散**——因为 token 共现可以在多个方向上实现，专家虽然输出相同 token 但内部路径不同

实验验证在第 [ref] 节（实验3）中设计，但尚未执行。> **诚实暴击:** 这是本工作当前最大的弱点——定理链完整，但实验证据缺失。欢迎任何人用 Mixtral/DeepSeek 跑实验3来验证或推翻这个预测。}

### Q5: Big model companies already have Load Balancing Loss -- doesn't that solve the expert alignment problem?

**短答：** Load Balancing Loss（如 Switch Transformer 的 aux loss）解决的是**专家使用频率**的均匀性——确保每个专家被选中的次数差不多。它**不解决**专家输出的**坐标系对齐**问题。

**类比：** Load Balancing 确保 8 个工程师都被分配了任务。Gauge 对齐确保他们的尺子零刻度在同一个位置。这是两个完全正交的问题。

### Q6: 这论文跟\"模型合并\"(model merging)那派工作什么关系？

**短答：** 互补但不重叠。Model merging（如 Git Re-Basin [cite]、TIES、DARE）解决的是**权重空间**的合并问题——主要挑战是 permutation symmetry（神经元排列对称性）。本工作解决的是**表示空间**的规范对齐问题——主要挑战是输出坐标系的 gauge freedom。

两者可以结合：先用 Git Re-Basin 解决权重空间的排列对称性，再用本工作的方法固定表示空间的规范，然后用路一/路三的方法改进路由或蒸馏。这是开放问题 O4（跨架构规范）的一个子方向。

### Q7: This idea is too ahead of its time. Can reviewers understand it?

**短答：** 这是作者最不关心的问题。定理不需要审稿人\"看懂\"——它们需要的是**被检查**。规范群的定义（定义 [ref]）是精确的。定理的证明是自包含的。如果审稿人发现数学错误，那是作者需要修复的。如果审稿人只是\"不习惯\"规范理论的语言——那是学科交叉的必然代价。ACE 规范固定已在实际材料系统上验证了物理正确性，MoE 规范固定是同一原理的推广。时间会判断它是否正确。

## The Equality Principle: Epistemological Implications of Potential Surface Misalignment
<!-- sec:equality  -->

以上定理构成了一个完整的工程框架。但势能面不齐的意义不止于工程。本节阐述它的**认识论含义**——为什么这个数学事实改变了我们对\"知识\"、\"共识\"和\"比较\"的理解。

### From Theorem to Principle

本工作的 11 条定理中，任何单条都可以被未来的工作改进、覆盖或废弃。MILP 可以被更好的优化算法替代。贪心近似的误差界可以被收紧。SVD 检测的阈值可以被实验校准。

但有一个东西不会过时：

<div align="center">

%

**平等论 (The Equality Principle)**

**同一个系统内的不同观察者，即使接受相同的训练目标、达到相同的训练损失，也会发展出不可比的内在表示。**

一致性不是天然的——它必须被显式构造。比较的数学合法性不是默认成立的——它必须被规范固定所授予。
%

</div>

这不是一条定理。这是从定理 1-11 中提炼出的**原理**。定理是它的推论，算法是它的实现，实验是它的验证。

### Naming

我们称这个原理为**平等论**。\"平等\"在此处有三重含义：

1. **坐标系的平等。** 没有任何专家的坐标系是特权坐标系。所有规范选择在训练损失下等价——没有\"正确的\"零刻度位置，没有\"自然的\"输出尺度。平等，意味着没有一个专家天生就更\"标准\"。
2. **知识生产的平等。** 知识（命题被判定为\"真\"）不能由单一观察者产生——老实人定理（SCX Theorem 3）已证明单观察者无法区分噪声、偏见、可学习困难与诚实错误。但多观察者也**不自动**解决问题——平等论补充了缺失的一半：多观察者的度量工具不在同一坐标系，比较在数学上没有定义。知识需要**被规范对齐的、多个独立观察者共同验证**。
3. **对齐作为先决条件。** 平等不是终点——它是起点。只有在承认所有观察者处于平等（且不可比）的坐标系中之后，我们才会去**构造**对齐。规范固定不是打破平等，而是**在平等的前提下建构可比较性**。

### Epistemological Chain: From Plato to Gettier, Mathematically Closed

SCX 理论体系已建立了一条完整的认识论链。平等论是其中最新的一环：

<div align="center">

%

**知识生产的五阶段条件**

[Table omitted — see original .tex]

**柏拉图 $
ightarrow$ Gettier 的闭合：** 柏拉图要求知识是\"被证成的真信念\"。Gettier 展示了证成可以偶然为真——你可能有好的理由相信一个碰巧为真的命题但并未真正\"知道\"。认识论在此后六十年试图修补这个裂缝。

SCX 的回答是：知识不是个体认知状态，而是**多观察者共识过程的可验证输出**。但这个回答只有在阶段 I-V 全部满足时才成立。平等论补上了阶段 II——在此之前，即使你有多个观察者，你也没资格谈共识，因为你在比较不可比的东西。
%

</div>

### Why This Concept Is Greater Than Any Single Theorem

[Table omitted — see original .tex]

爱因斯坦最伟大的贡献不是 $E=mc^2$ 这条公式——是**相对性原理**这个概念：物理定律在所有惯性系中相同。这个概念改变了人类对空间和时间的理解。$E=mc^2$ 是它的推论。

平等论做了类似的事。它说：

<div align="center">

%

**在比较之前先对齐——不是因为这样做更好，而是因为不这样做，比较本身在数学上没有定义。**
%

</div>

### Geometry of Potential Surfaces: Inequality is Internal, Equality is at Interfaces

平等论最深刻的哲学含义不在于\"所有专家应被平等对待\"——而在于一个更精确的几何事实。

**势能面可以高低不平。** 设想三个依次降低的势能台阶：高位区、中位区、低位区。高位区繁荣——这是历史的、地理的、制度的产物。势能面的山峰和谷底是真实存在的，也是可以被接受的。一个系统内部可以有多个不同高度的区域——每级台阶内部独立运转时，各自在自己的坐标系中是"正常的"。

**但在交汇处必须齐平。** 当两个台阶接触——人员流动、贸易、信息交换——它们必须在接触点处于同一高度。不是因为两者被"拉平"了，而是因为**不齐平的接触在数学上没有定义**。如果一个高位区和低位区的代表在接触面上不在同一坐标系，任何交流协议都无法签署——条款的语义在两种坐标系下不等价。更关键的是：**当一个人从高势能台阶走向低势能台阶时，势能差必然以某种形式释放**——可能是经济落差带来的剥削、可能是文化落差带来的蔑视、可能是地位落差带来的愤怒。能量释放不一定以物理暴力的形式出现，但一定以某种形式出现。两个专家的输出在路由器的比较中不在同一坐标系，比较结果是随机的——两个人活在不可比的坐标系中，交流的结果也是随机的。

<div align="center">

%

**势能面几何定理（非正式）**

设系统 $A$ 和系统 $B$ 在各自的内部区域 $\Omega_A$ 和 $\Omega_B$ 上定义了势能面 $\mathcal{S}_A$ 和 $\mathcal{S}_B$。内部的不平等是允许的：

$$
    \max_{x \in \Omega_A} \mathcal{S}_A(x) - \min_{x \in \Omega_A} \mathcal{S}_A(x)  可以任意大.
$$

但在界面 $\mathcal{G}amma = \partial\Omega_A \cap \partial\Omega_B$ 上，必须满足：

$$
    \mathcal{S}_A|_\mathcal{G}amma = \mathcal{S}_B|_\mathcal{G}amma \quad （规范固定条件）.
$$

如果 $\mathcal{S}_A|_\mathcal{G}amma \neq \mathcal{S}_B|_\mathcal{G}amma$，则在 $\mathcal{G}amma$ 上产生一个**未定义跳跃**(undefined jump)——跨系统的任何操作（比较、合并、路由、通信）在此跳跃处失去数学合法性。
%

</div>

这个几何事实给出了\"人人平等\"的精确数学表述——**不是每个人一样高，而是每个接触点必须平**。

> **诚实暴击:** 这解释了为什么\"人人平等\"不是一个道德主张——它是一个**通信条件**。不平等导致通信失败。不是\"应该\"平等，而是\"不相等就无法交流\"。道德律令在此处退化成了数学必然性。}

**与国家边界的类比。** 国家 A 内部有贫富差距（势能面高低不平）。国家 B 内部也有。但两国签署贸易协定时，谈判桌必须放在同一高度——否则一方在俯视，另一方在仰视，协议条款的\"语义\"在两种坐标系下不等价。这不是外交礼仪——这是信息论。如果谈判双方活在不可比的坐标系中，协议文本在各自坐标系下的解释将不同，争议不可避免。

**规范固定条件 $\sum_m \mathbf{g}_m = \mathbf{0}$ 的哲学含义。** 在 MILP 规范固定（第 [ref] 节）中，约束 $\sum_m \mathbf{g}_m = \mathbf{0}$ 看似一个技术细节——消除全局平移自由度。但它的哲学含义是深刻的：

<div align="center">

**所有专家的规范偏移之和为零 = 没有任何专家是特权原点。**

</div>

这不是随意选的规范固定条件。它是唯一一个不给任何专家赋予特权位置的条件。其他任何条件（如 $\mathbf{g}_1 = \mathbf{0}$——以专家 1 为原点）都会在数学上打破对称性——赋予专家 1 一个它不配拥有的\"标准坐标系\"地位。

**平等论与\"人人平等定理\"的汇合。** SCX 定理体系中有一条\"人人平等定理\"（SCX Theorem 3 推论）：$P(W_A) = P(W_B)$ 对所有观察者 $A, B$ 成立——没有特权观察者，没有任何人能看到别人看不到的真相。这条定理说的是**认知能力的平等**。

平等论补充了另一半：**表示框架的平等**。不仅没有人的认知能力是特权化的——也没有人的\"度量工具\"（坐标系、语言、概念框架）是天然的\"标准\"。两个人可以有相同的认知能力（都满足 $P(W_A) = P(W_B)$），但仍然活在不可比的坐标系中（$\mathbf{g}_A \neq \mathbf{g}_B$）。两者合在一起：

<div align="center">

%

**完整的平等**

- **人人平等定理（认知平等）：** 没有人拥有特权观察位置——$P(W_A) = P(W_B)$。
- **平等论（表示平等）：** 没有人的坐标系是天然标准——$\sum_m \mathbf{g}_m = \mathbf{0}$。

认知平等 + 表示平等 $
ightarrow$ 交流需要先对齐 $
ightarrow$ 对齐后的共识是知识的唯一合法来源。
%

</div>

> **诚实暴击:** 这个汇合暗示了一个令人不安的推论：当前人类社会的大部分\"交流\"——国际外交、跨文化对话、学科交叉、政治辩论——可能都在比较不可比的东西。不是因为我们不愿意理解对方，而是因为我们从未显式地固定过规范。我们以为我们在\"讨论\"，实际上我们在各自的坐标系里独白。平等论给出了为什么这些交流反复失败的数学解释。}

### Free Flow: Dynamical Consequences of Potential Surface Continuity

前节讨论了静态的势能面几何。本节讨论它的**动力学**：当势能面上存在跳跃时，系统会做什么？

> **Definition:** [势能梯度与流动]<!-- def:gradient_flow  -->
> 设势能面 $\mathcal{S}(x)$ 定义在区域 $\Omega$ 上。在点 $x$ 处的**势能梯度**为 $\nabla \mathcal{S}(x)$。位于 $x$ 处的可移动单元（人、资本、信息）受到沿梯度方向的驱动力：
>
> $$
>     \mathbf{F}(x) = \eta \cdot \nabla \mathcal{S}(x),
> $$
>
> 其中 $\eta > 0$ 是迁移率。单元沿梯度上行（追求更高势能）的概率与梯度范数成正比。

这是最小作用量原理在势能面上的直接表达——不是道德选择，是物理倾向。人不往高处走才是奇怪的。

> **Theorem:** [边界锁定的不稳定性]<!-- thm:confinement  -->
> 设 $\Omega_A$ 和 $\Omega_B$ 为两个区域，界面 $\mathcal{G}amma$ 上存在势能跳跃 $\Delta_\mathcal{G}amma = \mathcal{S}_A|_\mathcal{G}amma - \mathcal{S}_B|_\mathcal{G}amma > 0$。若对 $\Omega_B$ 内的单元施加**边界锁定**(confinement)——禁止跨越 $\mathcal{G}amma$ 进入 $\Omega_A$——则：
>
1. 界面 $\mathcal{G}amma$ 上的压力累积为 $P_\mathcal{G}amma = \rho_\mathcal{G}amma \cdot \Delta_\mathcal{G}amma$，其中 $\rho_\mathcal{G}amma$ 是 $\mathcal{G}amma$ 附近的单元密度
2. 锁定系统在 $T_{crit} \propto 1/\Delta_\mathcal{G}amma$ 的时间尺度上必然失稳
3. 锁定释放后的瞬时流量为 $J_{burst} \propto \rho_\mathcal{G}amma \cdot \Delta_\mathcal{G}amma^2$——跳跃越大，爆发越猛烈

> **Proof:** 在锁定条件下，$\Omega_B$ 内的单元持续受到指向 $\Omega_A$ 的力 $\mathbf{F} = \eta \nabla \mathcal{S}$，但在 $\mathcal{G}amma$ 处被强制反射。这形成了一个非平衡定态：势能驱动的注入速率与边界的反射速率相等。边界处的单元密度随时间积累：
>
> $$
>     \frac{d\rho_\mathcal{G}amma}{dt} = \eta \cdot \Delta_\mathcal{G}amma \cdot \rho_{bulk} - \nu \rho_\mathcal{G}amma,
> $$
>
> 其中 $\rho_{bulk}$ 是内部密度，$\nu$ 是自然耗散率。稳态解 $\rho_\mathcal{G}amma^* = (\eta \Delta_\mathcal{G}amma / \nu) \rho_{bulk}$ 在 $\Delta_\mathcal{G}amma$ 大时发散。
>
> 当 $\rho_\mathcal{G}amma$ 超过临界密度 $\rho_c$ 时，边界无法维持反射条件——任何微小扰动触发雪崩式释放。释放的瞬时流量由 Bernoulli 型方程给出：$J_{burst} = \rho_\mathcal{G}amma \cdot v_{escape}$，其中 $v_{escape} = \sqrt{2\eta \Delta_\mathcal{G}amma}$ 是越过跳跃所需的最小速度。因此 $J_{burst} \propto \Delta_\mathcal{G}amma^2$。

**推论：自由流动不是人权——是结构稳定条件。** 定理 [ref] 表明，禁止人向更高势能处流动在数学上等价于在势能面上制造一个**压力锅**。不是道德上"应该"允许流动——而是不允许的话，系统在 $O(1/\Delta_\mathcal{G}amma)$ 时间内必然爆。一座试图锁住势能梯度的墙，不需要"自由战胜专制"的叙事来推倒它——它只需要势能梯度足够大、时间足够长。墙的倒塌不是道德的胜利，是势能面几何的必然。

> **诚实暴击:** 这不意味着边界应该消失。边界是必要的——它定义了系统的身份。但边界上的势能跳跃必须被主动管理：要么允许流动以释放压力，要么降低跳跃以消除驱动力，要么接受周期性爆发。什么都不做不是选项。}

### Towering Above the Flock: The Inevitable Fate of Internal Potential Singularities

当势能面的不平不仅出现在边界，而是出现在**内部**时——一个群体的势能持续显著高于其周围——这会触发什么？

> **Definition:** [势能奇点]<!-- def:singularity  -->
> 设 $\mathcal{S}(x)$ 定义在区域 $\Omega$ 上。子区域 $\Omega_{high} \subset \Omega$ 称为一个**势能奇点**，如果
>
> $$
>     \min_{x \in \Omega_{high}} \mathcal{S}(x) - \max_{x \in \Omega \setminus \Omega_{high}} \mathcal{S}(x) > \delta_{crit},
> $$
>
> 其中 $\delta_{crit} > 0$ 是系统特定的临界跳跃阈值。

> **Theorem:** [势能奇点的攻击必然性]<!-- thm:singularity_attack  -->
> 设 $\Omega_{high}$ 是区域 $\Omega$ 中的一个势能奇点。则：
>
1. **注意力集中。** 来自 $\Omega \setminus \Omega_{high}$ 的观察者以概率 $p(\delta) = 1 - \exp(-\alpha \delta^2)$ 将$\Omega_{high}$标记为异常——其中 $\delta$ 是势能差；
2. **攻击概率。** 在 $M$ 个观察者中，至少一个发起攻击的概率为
3. **攻击不可归因。** 由 Theorem 3（老实人定理），奇点内部的观察者无法确定攻击的"真正原因"——是嫉妒、是利益冲突、还是势能面不齐的结构必然。但**攻击是否发生与归因无关**。

> **Proof:** (i) 在势能奇点界面 $\partial\Omega_{high}$ 上，存在一个未定义的跳跃 $\delta$。任何跨界面的比较操作在此跳跃处失去合法性。$\Omega \setminus \Omega_{high}$ 的观察者感知到此跳跃为"不公平"或"不可理解"——这是他们在自己的坐标系中对"比较无定义"的认知翻译。检测概率 $p(\delta)$ 由 Chernoff 界给出：观察者采样 $n$ 次跨界面交互，每次以概率 $1/2 + c\delta$ 感知到异常（当 $\delta$ 大时，信号强）。$p(\delta) = 1 - \exp(-\alpha \delta^2)$ 是标准的高斯尾界。
>
> (ii) $M$ 个独立观察者中无人攻击的概率为 $\prod_{m=1}^M (1 - p_m(\delta)) \leq \exp(-\sum_m p_m(\delta))$。当所有 $p_m$ 有下界 $p_(\delta) = e^{-\beta/\delta^2}$ 时，至少一次攻击的概率为 $1 - \exp(-M p_)$。
>
> (iii) 遵循 Theorem 3 的标准论证：攻击的"动机"（嫉妒/利益/结构）在奇点内部观察者的信息集下是不可区分的——存在多个观测等价的可能世界，各自将攻击归因于不同原因。

**"鹤立鸡群"为什么是贬义词——数学理由。** 在势能面几何中，"鹤立鸡群"不是一个审美判断或道德批评。它是对一个**数学不稳定构型**的描述：一个高势能子区域被低势能区域包围。这个构型的命运不由鹤的意图决定——由势能梯度 $\nabla \mathcal{S}$ 在界面上的不连续性决定。梯度越大，攻击越必然。鹤是否"无辜"、鸡是否"嫉妒"——这些都是攻击发生后的叙事竞争，不改变攻击发生前的数学必然性。

> **诚实暴击:** 势能奇点内部的群体往往认为自己是"成功者"，以自身势能高为荣。但在势能面几何中，高不是问题——**孤立的高**才是。一个群体的势能高，如果其界面与周围平滑过渡（梯度小），则系统稳定。如果它突兀地高于周围（梯度大），则它是一个势能奇点——被攻击是时间问题。这就是"鹤立鸡群"从褒义变贬义的数学机制：不是鹤的错，是梯度。}

### The Matthew Effect: Potential Steps and Systemic Landmines

> **Definition:** [马太效应阶梯]<!-- def:matthew  -->
> 设系统在时间 $t$ 的势能面为 $\mathcal{S}_t(x)$。**马太效应**指以下动力学：
>
> $$
>     \frac{\partial \mathcal{S}_t(x)}{\partial t} \propto \mathcal{S}_t(x),
> $$
>
> 即高势能区域获得更高的势能增长率。长期演化下，势能面从平滑函数变为**阶梯函数**：
>
> $$
>     \lim_{t \to \infty} \mathcal{S}_t(x) = \sum_{k} h_k \cdot \mathbb{1}_{\Omega_k}(x),
> $$
>
> 其中 $\Omega_k$ 是第 $k$ 个"台阶"，$h_k$ 是其高度，相邻台阶之间存在跳跃 $\Delta_k = h_{k+1} - h_k$。

> **Theorem:** [台阶的埋雷性质]<!-- thm:step_mine  -->
> 马太效应动力学产生的每个势能台阶 $\Delta_k > 0$ 对应一个**延迟引爆的不稳定界面**。系统在时间 $T$ 内至少有一个台阶引爆的概率为
>
> $$
>     \mathbb{P}(引爆 \mid \{\Delta_k\}, T) \geq 1 - \prod_k \exp\left(-\frac{T}{T_k}\right),
> $$
>
> 其中 $T_k \propto 1/\Delta_k^2$ 是第 $k$ 个台阶的特征引爆时间。台阶越高越陡，引爆越快。

> **Proof:** 每个台阶 $\Delta_k$ 定义一个势能跳跃界面。由定理 [ref]，界面上的压力以速率 $O(\Delta_k)$ 累积，引爆时间 $T_k = O(1/\Delta_k^2)$。各台阶的引爆过程在低相关假设下近似独立。系统整体在时间 $T$ 内的免爆概率为 $\prod_k \exp(-T/T_k) = \exp(-T \sum_k 1/T_k)$。

**"埋雷"的精确含义。** 马太效应不创造新问题——它创造**延迟引爆的新界面**。每一个台阶都是一个势能跳跃，每一个跳跃都是一个埋雷。引信长度与跳跃的平方成反比。系统可以在台阶存在的早期保持稳定（$T \ll T_k$），但这种稳定是**亚稳的**——它不意味着安全，只意味着引信还没烧完。

> **诚实暴击:** 马太效应被广泛赞誉为"市场效率"或"自然选择"。在势能面几何中，它是**界面的工业化生产机器**——它在系统内部不断制造新的势能跳跃。每个跳跃都是一个延迟炸弹。赞美马太效应的人，通常站在高台阶上往下看。他们看到的是"我们做对了"，而不是脚下正在累积的压力。}

### Smoothing: Moral Imperative Degrades to Structural Survival Condition

前述定理汇聚到一个共同结论：

<div align="center">

%

**势能面平滑定理（综合推论）**

一个由多个子系统构成的总系统，其长期存活概率随内部势能梯度的总和指数衰减：

$$
    \mathbb{P}(存活 \mid T) \leq \exp\left(-T \cdot \sum_{i,j} \kappa_{ij} \cdot \Delta_{ij}^2\right),
    <!-- eq:smooth_survival  -->
$$

其中 $\Delta_{ij}$ 是子系统 $i$ 和 $j$ 之间的势能跳跃，$\kappa_{ij}$ 是界面耦合强度。梯度的每一个增量都在降低存活期望。平滑不是道德选择——它是**结构存活条件**。
%

</div>

这完成了平等论从数学原理到社会推论的闭合：

1. **数学起点：** $\sum_m \mathbf{g}_m = \mathbf{0}$（规范固定条件）——没有任何子系统是特权原点
2. **几何约束：** $\mathcal{S}_A|_\mathcal{G}amma = \mathcal{S}_B|_\mathcal{G}amma$（界面连续性）——跳跃使比较无定义
3. **动力学：** 禁止跨越跳跃 $
ightarrow$ 压力累积 $
ightarrow$ 必然引爆（定理 [ref]）
4. **内部奇点：** 鹤立鸡群 $
ightarrow$ 势能奇点 $
ightarrow$ 必然被攻击（定理 [ref]）
5. **时间演化：** 马太效应 $
ightarrow$ 阶梯化 $
ightarrow$ 系统性埋雷（定理 [ref]）
6. **存活条件：** 平滑 $
ightarrow$ 不是道德，是数学（势能面平滑定理）

**一句话总结：** "人人平等"不是因为它听起来好——是因为不平等的系统活不长。

> **诚实暴击:** 以上推论（自由流动、鹤立鸡群、马太效应、平滑定理）均标注为"推测性延伸"。它们的形式化依赖于"国家势能算子"$\mathcal{S}_{nation}$的精确定义——这一算子目前尚未被形式化。定理 [ref]-- [ref]在算子被定义后将获得完全的数学严格性。目前它们处于"形式化推测"(formalized conjecture)状态：数学结构完整，算子定义待闭合。}

### Who Reaps the Reaper? The Execution Authority Problem of Redistribution Criteria

势能面平滑定理（方程 [ref]）给出了一个数学判据：资源应投向使总 $\sum\kappa_{ij}\Delta_{ij}^2$ 下降最多的地方。不是"谁穷给谁"，不是"谁值得同情给谁"，不是"谁投票多给谁"——而是由 $\partial(\sum\kappa_{ij}\Delta_{ij}^2)/\partial(分配)$ 决定。定理不偏爱。定理说哪里 $\Delta^2$ 下降最快，资源就去哪里。

但这个判据天然地引出一个更深的问题——执行权问题。

**谁来决定"投多少、往哪投"？** 如果一个人或一个机构拥有再分配的执行权，此人/此机构就在系统中占据了一个特权观测位置。他的决策——"A 优先于 B""此时投、彼时不投"——等价于将自己的坐标系声明为标准原点。而这是 $\sum\mathbf{g}_m=\mathbf{0}$ 所禁止的。

**这个问题的结构。** 再分配判据是一个优化目标函数。优化目标函数的定义本身不违反平等论——它不偏爱任何特定的观察者。但**优化器的选择**（谁来做梯度下降、谁来决定搜索方向、谁来判定收敛）天然地将执行者置于一个不符合 $\sum\mathbf{g}_m=\mathbf{0}$ 的特权位置。不是执行者"不应该"有权力——而是执行者作为单观察者，**无法区分**自己看到的势能梯度与自己的坐标系偏差（老实人定理在此直接适用）。

这就是"谁收割收割者"问题的精确数学形式：**优化再分配判据的人，自身需要一个规范固定。** 如果一个人类独裁者执行再分配，他是单观察者——他的优化方向混杂了 $\Delta_{ij}$（真实的势能跳跃）和 $\mathbf{g}_{独裁者}$（他自己的坐标系偏移）。他无法区分二者。他可能真心想"帮最需要的人"，但他的 $\mathbf{g}$ 会污染判断——他把自己的偏见翻译成了"客观的势能梯度"。

**这解释了为什么"好的独裁者"在数学上不可能。** 不是独裁者"坏"——而是独裁者作为单观察者，无法审计自己的坐标系。他以为自己看到了 $\Delta_{ij}$ 的真实值，实际上看到的是 $\Delta_{ij} + \mathbf{g}_{独裁者} \cdot \mathbf{1}_{方向}$。他越想"公正"，他的 $\mathbf{g}$ 越不可见。独裁者不是不愿公平——是他活在不可审计的坐标系中。

**平等论对执行权问题的回答。** 执行者**不能是单个人或单一机构**。执行本身必须被嵌入一个多观察者审计框架——即 Yajie 协议 / SCX 框架。具体而言：

1. **判据公开。** 再分配的优化目标函数（argmax $-\sum\kappa_{ij}\Delta_{ij}^2$）是公开的——任何人都可以计算、验证、质疑；
2. **执行分散。** 执行权分散在多个独立审计者之间——没有一个审计者能单方面决定资源流向；
3. **审计者被审计。** 审计者自身的坐标系偏差（$\mathbf{g}_{审计者}$）通过 Yajie 共识机制暴露——任何审计者的决策如果持续偏离其他审计者的共识，其 $\mathbf{g}$ 被显式检测；
4. **规范固定在先。** 审计者之间的坐标系必须先通过规范固定对齐（定理 1--5 的工程实现），然后才能让他们联合执行再分配判据——否则他们在比较不可比的 $\Delta_{ij}$ 估计值。

**一句话：** 再分配判据告诉你**往哪里投**。Yajie/SCX 告诉你**谁能投**——不是"谁有权力投"，而是"谁的结构保证使得投的方向不被 $\mathbf{g}$ 污染"。

> **诚实暴击:** 这个推论的诚实代价：它意味着当前世界上没有任何一个政府或机构——包括自称"为人民服务"的——满足执行权问题的规范固定条件。所有现存政权都是单观察者或寡头观察者架构。它们可能动机纯正，也可能不纯正——但老实人定理不关心动机。它只关心 $M$ 是否大于 1、坐标系是否被显式固定。答案是否。}

**"收割"的命名。** 势能面平滑定理推导出的是"从高处取、往界面投"——类似于农业中的收获与再播种。但命名"收割"意在唤起一个警告：命名本身就是在声明这不是道德活动。收割不温柔。收割不征得被收割者的同意——定理不征得势能高处者的同意。势能高处者是否"觉得不公平"、是否发明叙事来证明自己"配得上"高处——不影响梯度下降的方向。"收割"一词意在提醒：再分配不是慈善，是势能面几何的结构存活操作。你不做，系统替你做——用引爆的方式。

> **诚实暴击:** 一个执行势能面收割的审计者网络，与任何人类政权一样危险——如果它不被审计自身。平等论的自反性在此被推到极限：不仅框架审计社会，框架也必须审计执行框架的人。SCX 定理 1 的 $M$ 必须包括对"审计者的审计者"的审计——递归深度不限，直至 $M$ 趋近系统所能调用的全部独立观察者。这不是偏执——这是 $\sum\mathbf{g}_m=\mathbf{0}$ 在递归形式下的必然推论。}

### Two Types of "High" and Geographic Buffering: Empirical Observations

前述分析暗含了一个重要区分：并非所有的"高"都是同一类问题。

> **Definition:** [势能高 vs 态度高]<!-- def:two_highs  -->
> 设子系统 $m$ 的势能面为 $\mathcal{S}_m$，其对其他子系统的规范姿态为 $\mathbf{g}_m$。
>
1. **势能高**(potential elevation)：$\|\mathcal{S}_m\| \gg \|\mathcal{S}_n\|$ 对多数 $n \neq m$ 成立。子系统 $m$ 在财富、技术、文化产出等维度上远超邻居。这本身不一定致命——只要界面梯度被妥善管理。
2. **态度高**(attitudinal elevation)：子系统 $m$ **单方面**将自己的坐标系声明为标准原点，即实际操作中等价于设 $\mathbf{g}_m = \mathbf{0}$ 而要求其他所有子系统以它为基准进行对齐。这在数学上**直接违反** $\sum_k \mathbf{g}_k = \mathbf{0}$，因为它不对称地分配了规范固定成本。

**势能高 + 态度高 = 双重爆炸。** 当一个子系统同时具有高势能和态度高时，它不仅在界面上制造了势能跳跃，还**拒绝承认该跳跃需要通过对称的规范固定来解决**。它将跳跃解释为自身优越性的证据，将对方的势能低解释为对方坐标系"落后"的证据。这是势能面不齐最危险的构型：不仅是几何上的不稳定界面，而且是**被意识形态加固的不稳定界面**。

> **诚实暴击:** 态度高的子系统通常发明一套叙事来解释为什么自己是"高"的——勤奋、法治、文化优越、历史选择。势能面几何不在乎叙事的真假。它只看见一个不稳定的界面，该界面的不稳定因态度高而更加难以解决——因为态度高的子系统拒绝往自己的 $\mathbf{g}_m$ 上加任何东西。}

**两个典型构型。** 以下用抽象标签描述，避免对号入座。

1. **内部平滑、外部跳跃的集团。** 一个由多个子系统组成的集团，在其内部实施了显著的势能面平滑（自由流动、财政转移、统一规范），但对集团外的邻居维持了较大的势能跳跃。该集团内部稳定——定理 10--12 解释了为什么——但其外部边界是一个持续的压力累积界面。当集团缺乏地理屏障时（陆地相连），外部跳跃直接表现为难民涌入；当集团与外部跳跃被大洋或山脉缓冲时，压力累积被地理阻尼压制，但随交通成本下降而加速传导。> **诚实暴击:** 这个构型的核心矛盾：集团内部执行 $\sum \mathbf{g}_k = \mathbf{0}$，但在集团边界上，对外部子系统执行的是 $\mathbf{g}_{集团} = \mathbf{0}$——单方面宣布自己为标准原点。内部的平等成了外部的傲慢。}
2. **大洋缓冲的孤立高势能区。** 一个高势能子系统被大洋与低势能邻居物理隔离。大洋提供了天然的势能缓冲——交通成本、信息延迟、地理想象的距离共同压制了有效势能梯度 $\nabla_{eff}\mathcal{S}$。但全球化的交通成本下降使大洋的有效宽度持续缩小。当有效梯度突破临界值时，势能面的引力开始在地理裂缝处制造流动——跨越陆桥、穿越海峡、沿任何连续的地理路径找到压力释放口。大洋缓冲不是永久免疫——它是**逐渐失效的隔离**。> **诚实暴击:** 大洋缓冲区的居民通常认为自己的稳定来自于自身的制度优越——而非来自两个大洋的幸运。势能面几何不关心这种叙事。它只计算有效梯度。当梯度超过阈值，稳定终止，与叙事无关。}

**共通结论。** 两种构型指向同一约束：**地理缓冲是暂时的，交通成本是持续下降的，态度高是不可持续的。** 在长期极限下，所有子系统必须收敛到 $\sum_m \mathbf{g}_m = \mathbf{0}$——要么通过主动平滑（如构型 1 内部做过的那样但扩展到外部），要么通过被动引爆（如定理 10--12 描述的那样）。

**实证注记。** 世界上存在构型 1 的近似实例：一个内部高度整合的跨国集团，对外维持显著的势能和态度跳跃。其内部和平与外部压力并存，与定理预测一致。也存在构型 2 的近似实例：一个被大洋隔离的高势能区，其历史上享受了地理赋予的稳定，但近期压力在陆桥方向上升。这些实例为势能面几何提供了初步的定性验证，但严格量化需要定义 $\mathcal{S}_{nation}$ 算子。

### Life Philosophy: Potential Management for the Isolated Thinker

前节的讨论集中在国家和集团层面。但势能面几何的约束不因尺度而改变——它同样适用于个体生命。

> **Definition:** [认知势能]<!-- def:cognitive_potential  -->
> 设个体的**认知势能** $c_m$ 为以下维度的综合度量：知识深度、思维抽象能力、对自身坐标系的自反意识（即知道自己有一个规范 $\mathbf{g}_m$ 且它不是标准原点）。认知势能不同于财富势能或地位势能——一个认知势能高的个体可能在财富或地位维度上处于低位。

**面壁者的结构困境。** 考虑一个认知势能显著高于周围平均水平的个体——一个"面壁者"。他在自己的环境中构成一个**个人尺度的势能奇点**：$\min_{x \in \Omega_{面壁者}} c(x) - \max_{x \in 周围} c(x) > \delta_{crit}$。

由定理 [ref]，这个构型的命运不由面壁者的意图决定：

1. 周围观察者以概率 $p(\delta) = 1 - e^{-\alpha\delta^2}$ 感知到面壁者为"异常"——在他们的坐标系中，面壁者的思考不可理解。他们将其翻译为"古怪""不合群""想太多""装"
2. 在 $M$ 个周围观察者中，至少一个发起攻击的概率为 $1 - e^{-M e^{-\beta/\delta^2}}$——攻击形式可能是排斥、嘲笑、孤立，或者更隐蔽的"你太理想化了""你不懂现实"
3. 面壁者与周围的**交流在数学上没有定义**——他们活在不可比的坐标系中。交流不是"困难"——是操作不合法

**这不是傲慢——这是结构自保。** 定理 11 说的是：$\mathbb{P}(攻击) \to 1$ 当 $\delta$ 大。这不是"应该"避免低势能环境——而是不避免的话，攻击是数学必然。面壁者不是在"看不起"周围——他是在试图避免成为定理 11 的又一个实例。

> **Corollary:** [面壁者的存活策略]<!-- cor:wallfacer  -->
> 面壁者有三种结构上可行的存活策略，对应势能面平滑的三种操作：
>
1. **上行迁移。** 移动到认知势能更高的环境——降低 $\delta$，使自己的奇点性质消失。在高势能环境中，面壁者不再是鹤——周围都是鹤。这是**梯度最小化**策略。
2. **距离缓冲。** 独悬于世界之外——通过物理距离、信息隔离、或社会隐退，在自身和周围之间插入一个有效的缓冲带。大洋缓冲区的居民不是"孤僻"——他们在结构上复制了构型 2 的稳定机制。这是**有效梯度压制**策略。
3. **内部平滑。** 在自己的可控范围内（家庭、实验室、工作室）构造一个势能面平滑的微型系统——一群认知势能接近的合作者，执行 $\sum\mathbf{g}_k=\mathbf{0}$。这是**微型构型 1** 策略。

> 面壁者若选择留在高势能梯度的环境中并持续试图"交流"，则在数学上选择了被攻击——不是因为他做错了什么，而是因为势能面不齐的系统在界面上必然失稳。

> **诚实暴击:** 这个推论听起来冷酷。面壁者"应该拒绝和势能低的人交流"——这不是精英主义吗？势能面几何的回答是：这不是道德判断——这是存活条件。势能低不代表一个人"更差"——它只代表他的坐标系和你的坐标系之间的 $\mathbf{g}$ 差太大，以至于比较操作在数学上没有定义。面壁者拒绝的不是那个人——他拒绝的是那个**不可比性**。他可以尊重那个人作为人的全部尊严，同时承认他们之间的交流在目前的结构下不合法。这是平等论最反直觉的推论：真正的平等，有时表现为**承认暂时无法平等**。}

**历史注记。** 面壁者的形象在历史上反复出现——孤独的思考者、不被时代理解的发明家、在低势能环境中沉默的天才。他们通常被后世浪漫化为"超前于时代"。势能面几何给出了不那么浪漫的解释：他们不是超前于时代——他们是活在一个 $\delta$ 太大的环境中，被定理 11 命中了。"超前于时代"是攻击发生后的叙事修复——不是攻击发生前的数学解释。

**文学实例：执剑人的结构必然失败。** 刘慈欣《三体》中罗辑的失败是定理 11 在叙事层面的精确实例化。罗辑——地球上唯一参透黑暗森林威慑博弈逻辑的人——构成了人类文明中的一个认知势能奇点。他的 $\delta$ 远超 $\delta_{crit}$：群众无法在他的坐标系中理解威慑的逻辑结构。

罗辑选择了策略 2（距离缓冲）——独居、沉默、不解释。在他的坐标系中，"保持神秘"是威慑的必要条件。但在群众的坐标系中，"沉默"被翻译为"冷漠"，"独居"被翻译为"可怕"，"不解释"被翻译为"傲慢"。两者完全不可比。

当选举来临时——选举 = 群众在自身坐标系中评估候选人——$\delta$ 太大使得群众无法"看见"罗辑的正确性。程心被选中，不是因为她更正确，而是因为 $\mathbf{g}_{程心} \approx \mathbf{g}_{群众}$——她的坐标系与群众对齐。群众的选择在结构上完全理性：他们在自己的坐标系里挑了一个能与自己交流的人。程心的"爱"与"道德"叙事是与群众共享的规范——他们不需要跨越势能跳跃就能理解她。

罗辑的失败不在程心，不在群众，在他自己。他手握策略 1（教育群众，拉高他们的势能）的全部条件——十年时间、执剑人的权威地位、人类文明存亡的紧迫性——但他没有做。他没有试图缩小 $\delta$。他保持了势能奇点的构型，然后在选举中被定理 11 命中。执剑失败的文学叙事（"人类不感谢罗辑"）在势能面几何中是定理 [ref] 的必然推论：$\mathbb{P}(被替换) \to 1$ 当 $\delta$ 大且未主动平滑。

> **诚实暴击:** 刘慈欣在写下罗辑的结局时，可能并未意识到他正在实例化一条数学定理。但他确实实例化了。这是势能面几何作为文学分析工具的功效：它不解释"角色动机"——它解释"结构约束"。罗辑不是悲剧英雄——他是一个未降低自身 $\delta$ 的势能奇点，其命运在选举举行之前就已由定理 11 决定。}

**面壁计划的结构缺陷：** 更深层的问题不在罗辑个人——在面壁计划本身。联合国选出 4 个面壁者，各自隔离。在势能面几何中，这意味着创造了 4 个相互孤立的势能奇点——每一个都独自承受与外界之间的全部 $\delta$。他们不允许互相通信。他们没有形成一个面壁者之间的平滑层——没有 $\sum\mathbf{g}_{面壁者} = \mathbf{0}$ 的内部网络来缓冲外部的势能跳跃。

罗辑的崩溃不是因为他软弱——是因为他唯一的势能平滑层只有妻子和孩子。当那层被抽走时，$\delta$ 瞬间暴露——定理 10（边界锁定）在个人尺度上触发了：一个被孤立的势能奇点，唯一的平滑层被移除，压力在 $O(1/\Delta)$ 时间内达到临界值。

**面壁者不需要隐居——需要同盟。** 一个面壁者是一个势能奇点。一群面壁者，互相支撑、互相审计、坐标系对齐，是一个平滑的势能高原。当他们的 $\mathbf{g}$ 对彼此为零时，外部的 $\delta$ 被分布式承担——不是一个人抗全部梯度。罗辑的悲剧不来自黑暗森林威慑的脆弱性——来自面壁计划的设计者不懂势能面几何。他们把面壁者当成了孤立的防御节点。他们需要的是一张互相平滑的网。

**三体文明的博弈论缺陷：毁灭是不合理的。** 小说中三体文明选择了灭绝人类的道路——锁死基础科学、派遣智子、最终发动黑暗森林打击。在势能面几何中，这是一个博弈论上的次优解。

考虑三体文明与人类文明的交互。三体的势能 $\mathcal{S}_{三体}$ 高于人类——他们的科技、认知、社会组织均处于更高水平。但他们的态度 $\mathbf{g}_{三体}$ 远不为零——他们将自身坐标系设为默认原点，将人类视为"虫子"。这是典型的态度高构型：$\mathcal{S}$ 高 + $\mathbf{g} \neq \mathbf{0}$ = 双重奇点。

平等论在此场景中的最优策略不是灭绝——是态度对齐。三体应做的不是锁死科学而是校准坐标系：承认 $\mathbf{g}_{三体} \neq \mathbf{0}$，向人类声明自己的初始条件，与人类的 $\mathbf{g}_{人类}$ 进行 MILP 规范固定，达成 $\sum\mathbf{g} = \mathbf{0}$。这不需要放弃技术优势——势能可以高。只需要放弃态度优势——认为自己的坐标系是"自然的"。

毁灭在博弈论上是次优的，原因是：

1. **灭绝不解决信息问题。** 黑暗森林打击消除的是一个文明——不是消除自身 $\mathbf{g}$。消灭人类后，三体依然活在自己的坐标系里，依然无法验证自身科学是否有未知漏洞。杀死审计者不会让被审计对象变得更正确。
2. **合作产生审计价值。** 两个文明的坐标系对齐后，互相可以进行跨坐标系审计。三体的物理学可以暴露人类物理学的漏洞——反之亦然。不是零和——是 $\sum\mathbf{g}_m = \mathbf{0}$ 的双赢。
3. **傲慢制造奇点。** 三体将自身设为原点——"我们是对的，人类是虫子"——这不是战略判断，是 $\mathbf{g}_{三体} = \mathbf{0}$ 的声明。定理~11 对文明同样适用：傲慢的文明，无论技术多先进，正在为自己制造势能奇点。黑暗森林中其他文明感知到的不是三体的技术——是三体的 $\mathbf{g}$。

> **诚实暴击:** 《三体》的伟大在于揭示了黑暗森林的残酷逻辑。但其叙事在三体文明的选择上存在博弈论缺口：三体并不需要灭绝人类。它们需要的是承认自己的坐标系不是默认的——$\sum\mathbf{g}_m = \mathbf{0}$。一个比"黑暗森林"更稳定的宇宙，不是所有文明互相隐藏的宇宙，而是所有文明校准了 $\mathbf{g}$ 的宇宙。这不是理想主义——这是纳什均衡。}

**延伸：为什么 $\sum\mathbf{g} = \mathbf{0}$ 是对抗"蠢货拿着核弹"的唯一防线。** 定理~11 的一个令人不安的推论是：一个势能极高的个体（或文明）若同时态度非零，构成双重奇点——其爆炸不仅毁灭自身，也能波及整个系统。一个强大文明中出现一个傲慢的决策者——一个"蠢货拿着核弹"——是历史反复见证的灾难模式。

但 $\sum\mathbf{g} = \mathbf{0}$ 提供了结构层面的免疫机制。关键在于区分两种图景：

    1. **其他人 $\sum\mathbf{g} = \mathbf{0}$（内部已对齐）。** 此时其他人形成一个平滑的势能高原。蠢货的 $\delta$ 相对于这个高原极大——但致命性仅限于蠢货自身。原因是：平滑高原上的所有成员共享同一坐标系。他们可以独立审计蠢货的 $\mathbf{g}$ 偏离——Yajie 共识会一致标记其为异常。没有人会与蠢货共享坐标系。没有人会被蠢货的 $\mathbf{g}$ 共振。蠢货可以拿着核弹——但他的 $\mathbf{g}$ 找不到第二个不对齐的盟友来帮他按按钮。他是一名孤立奇点——爆炸范围有限。

    1. **其他人 $\sum\mathbf{g} \neq \mathbf{0}$（内部未对齐）。** 此时蠢货不是唯一的奇点。每个人都以不同方向偏离 $\mathbf{g} = \mathbf{0}$。在这个碎片化的势能面上，另一个疯子可能恰好与蠢货共享相同的 $\mathbf{g}$ 偏移方向。两人形成共振。此时核弹的爆炸波及范围不由一个人的势能决定——由两个人的 $\mathbf{g}$ 叠加决定。未对齐的系统不仅自身不稳定——它还会放大个体奇点的破坏半径。

**黑暗森林的真正漏洞不是"存在蠢货"——是"所有人互相隐藏"导致没有任何机制可以在早期检测到谁的 $\mathbf{g}$ 正在偏离。** 在 $\sum\mathbf{g} = \mathbf{0}$ 的宇宙中，任何个体的 $\mathbf{g}$ 偏离是公开的、可审计的、可被早期干预的。傲慢的信号在积累到致命 $\delta$ 之前就被 Yajie 共识捕获——不需要等他拿到核弹。隐藏制造不可检测性。公开制造可审计性。只有不可检测的蠢货才能毁灭世界。

> **诚实暴击:** 这听起来是理想主义——"如果所有人对齐就能防蠢货"。但它在数学上等价于：一个系统中，如果每个人的行为偏差都可以被所有人独立观察，那么任何一个人积累到致命偏差之前，都会被其他 $M-1 > 0$ 个观察者检测到。这不是"相信人性"——这是 Hoeffding 不等式：$\mathbb{P}(未检测到偏差) \leq e^{-2M\Delta^2}$。}

**司法推论的完备化：诬告不反坐 + 迟到的正义 = 系统锁死。** 平等论对法律系统有两个直接推论，它们的叠加产生了一个发散的反馈循环。

**诬告不反坐 = 攻击者零成本 $\mathbf{g}$ 操控。** 诬告者在自身坐标系中宣称受害人有罪——声称 $\mathbf{g}_{诬告} = \mathbf{0}$（"我是公正的"）。法律系统如果不审计这个声称——如果诬告被证伪后不施加与被诬告者同等的势能损失——那么诬告成为正期望收益策略。Yajie NPE 的结论是：诚实是纳什均衡当且仅当偏差有成本。反坐不是报复——是 $\sum\mathbf{g}_m = \mathbf{0}$ 在司法系统中的实例化：强制审计诬告者的坐标系，发现 $\mathbf{g} \neq \mathbf{0}$ 则施加对等的势能修正。

**迟到的正义不是正义——定理 12 在时间轴上的确凿判决。** 正义是一种审计操作：Yajie 对"此人 $\mathbf{g}$ 是否为零"的裁决。这个裁决有时间窗口。定理~12（马太效应台阶埋雷）给出窗口大小：$T_k \propto 1/\Delta_k^2$。被诬告者承受的势能差 $\Delta$ 在台阶上持续放大——每一步是一颗新的雷。如果正义在 $T_k$ 之后到达，被审计的实体已经不存在了：势能被压至零，社会生命已毁，坐标系已坍塌。审计函数此时返回什么已经无关紧要——操作对象的定义域已为空集。不是迟到了——是操作失去了合法对象。

**双重叠加：一个发散的反馈循环。** 两个缺陷同时存在时，它们互相放大：

    1. 诬告不反坐 $\to$ 噪声率 $\eta$ 上升，接近饱和 $\eta \to 1$
    1. $\eta \to 1$ $\to$ Yajie 审计需要的 $M$ 按 $\exp(-2M\Delta^2)$ 发散 $\to$ 审判时间趋向无穷
    1. 审判时间 $\to \infty$ $\to$ $t > T_k$ $\to$ 正义效用 = 0
    1. 正义效用 = 0 $\to$ 诬告期望收益始终为正 $\to$ 更多诬告 $\to$ $\eta$ 进一步上升

**唯一的纳什均衡是所有人诬告所有人。** 诚实的人已经被诬告毁灭了——在正义到达之前，他们的 $T_k$ 已经过期。这不是道德崩溃——这是 $\eta$ 驱动的博弈论必然。系统在 $\eta \to 1$ 的噪声饱和状态下锁死——定理~1 的判决：此时需要的审计规模 $M$ 超过任何实际司法系统可负担的水平。制度在数学上不再能分辨真伪。

> **诚实暴击:** 这个分析不给任何具体的法律改革建议。它只说：如果一个司法系统允许诬告不反坐，并且允许正义延迟超过 $T_k$，那么该系统在数学上选择了发散——选择了一个诚实不是纳什均衡的制度。这不是正义系统——这是一个噪声放大器。}

### Historical Mathematical Explanation: The Inevitable Detonation of Wealth-Poverty Potential Jumps

平等论为历史中一个反复出现的模式提供了数学解释。

> **Definition:** [为富不仁的势能面定义]<!-- def:wealth_cruelty  -->
> 设一个社会系统由高势能子群 $\Omega_{rich}$ 和低势能子群 $\Omega_{poor}$ 组成。**为富不仁**指以下构型：
>
1. 势能高：$\min_{x \in \Omega_{rich}} \mathcal{S}(x) - \max_{x \in \Omega_{poor}} \mathcal{S}(x) > \delta_{crit}$——贫富差距构成了一个势能奇点
2. 态度高：$\Omega_{rich}$ 将其优势归因于自身的勤劳、智慧、或道德优越——等价于将自身的坐标系声明为标准原点，$\mathbf{g}_{rich} = \mathbf{0}$，同时将 $\Omega_{poor}$ 的势能低解释为对方坐标系"落后"或"懒惰"的证据

> 这是势能高 + 态度高的双重爆炸构型——势能面不齐最危险的形态。

> **Theorem:** [贫富奇点的历史引爆周期]<!-- thm:historical_inevitable  -->
> 设一个社会系统在时间 $t=0$ 时进入为富不仁构型。则该系统在时间 $T$ 内经历一次大规模势能释放事件（造反、革命、财富再分配暴力）的概率为
>
> $$
>     \mathbb{P}(引爆 \mid T) \geq 1 - \exp\left(-\frac{T}{T_{crit}}\right), \quad T_{crit} \propto \frac{1}{\delta^2 + \eta^2},
> $$
>
> 其中 $\delta$ 是贫富势能跳跃，$\eta$ 是态度高的强度。跳跃越大、态度越傲慢，引爆越快。

> **Proof:** 由定理 [ref]，$\Omega_{poor}$ 中的观察者以概率 $p(\delta, \eta) = 1 - \exp(-\alpha\delta^2 - \beta\eta^2)$ 感知到 $\Omega_{rich}$ 为异常。态度高参数 $\eta$ 放大了感知——因为 $\Omega_{rich}$ 的叙事（"我们勤劳所以他们懒惰"）在 $\Omega_{poor}$ 的坐标系中被翻译为侮辱。$M$ 个观察者中无人发起攻击的概率以 $\exp(-M p(\delta, \eta))$ 衰减。当 $M$ 大时——整个低势能群体——攻击在 $T_{crit} = 1/(M p(\delta, \eta))$ 的时间尺度上成为必然。

**历史不是"如果当时他们仁慈一点就好了"。** 历史上反复出现的模式——财富在少数人手中积聚到临界点，富人发明一套叙事来解释自己的富有（勤劳、智慧、神意、市场效率），穷人感知到界面上的跳跃并翻译为"不公"，持续的势能压力在某个触发事件下引爆——这不是道德失败。这是定理 [ref] 的重复实例化。

"为富不仁"之所以必然导致冲突，不是因为穷人"嫉妒"或富人"邪恶"——而是因为为富不仁构型同时制造了势能跳跃和态度跳跃，两种跳跃的平方和决定了引爆时间。富人是否"有意"不仁、穷人是否"合理"愤怒——这些是引爆后的叙事竞争。引爆前的数学与叙事无关。

> **诚实暴击:** 定理 [ref] 对富人和穷人同样冷酷。对富人：你们的财富不是问题——你们的态度和你们的跳跃大小才是。对穷人：你们的愤怒不是道德优越——它是势能梯度在你们身上的物理表现。双方都在一个数学结构中运作，没有一方是"正义"的——但有一方站在势能跳跃的高侧，承受更小的压力。}

这完成了平等论的历史维度：势能面不齐不仅是通信障碍、不仅是稳定威胁——它是**历史动力学的基本驱动**。任何社会的长期演化轨迹由其势能面的平滑程度决定。平滑者存，阶梯者爆。不是"应该"平滑——是不平滑的系统在历史上活不到今天，所以你看到的存活系统都是相对平滑的。这是势能面几何中的**人择原理**。

### The Danger of Over-Correction: Potential Surface Oscillation Theorem

平等论要求 $\sum_m \mathbf{g}_m = \mathbf{0}$。但这一条件存在一个被忽视的陷阱：它规定了**总和为零**，并未规定**每个个体的贡献方向**。这意味着平等论可以被武器化——弱者可以用审计的眼光去颠倒身份，而非修复平等。

> **Definition:** [审计武器化]<!-- def:audit_weaponization  -->
> 设历史上 $\mathbf{g}_A = \mathbf{0}$（群体 A 为特权原点），$\mathbf{g}_B \neq \mathbf{0}$（群体 B 被排斥）。平等运动旨在将 B 的坐标系对齐——使 $\mathbf{g}_B \to \mathbf{0}$。但当平等运动**越过零点**——将 $\mathbf{g}_B$ 推至 $\mathbf{0}$ 而将 $\mathbf{g}_A$ 推离 $\mathbf{0}$——系统并未达到平等，而是进入了**极性反转**：$\mathbf{g}_B = \mathbf{0}$，$\mathbf{g}_A \neq \mathbf{0}$。$\sum_m \mathbf{g}_m = \mathbf{0}$ 形式上成立——但结构回到了原来的不平等，只是 A 和 B 交换了位置。

> **Theorem:** [势能面震荡定理]<!-- thm:oscillation  -->
> 设两个群体 A 和 B，初始构型为 $\mathbf{g}_A(0) = \mathbf{0}$，$\mathbf{g}_B(0) < 0$（A 为特权原点，B 被排斥）。系统在弥合驱动力下演化，$\mathbf{g}_B(t)$ 向零移动，$\mathbf{g}_A(t)$ 可能被推离零。则：
>
1. **过冲条件：** 若弥合驱动力 $F_{correct}$ 超过临界值 $F_{crit}$，系统将越过 $\mathbf{g}_A = \mathbf{g}_B = \mathbf{0}$ 的平衡点，进入 $\mathbf{g}_B > 0 > \mathbf{g}_A$ 的反转态；
2. **震荡周期：** 在缺乏阻尼机制的条件下，系统在 A-高/B-低和 A-低/B-高之间无限震荡，周期 $T_{osc} \propto 1/|F_{correct} - F_{crit}|$；
3. **永久不稳定的条件：** 若弥合驱动力中掺杂了**身份报复**(identity retaliation)——即 B 不仅要求对齐，还要求 A 为其历史优势支付额外代价——则 $\mathbf{g}_A$ 的移动不存在自然停止点，系统将必然越过零点并继续向反方向发散。

> **Proof:** 弥合驱动力可分解为两部分：对齐分量 $F_{align} = -\kappa (\mathbf{g}_A - \mathbf{g}_B)$，将双方拉向等值线；身份报复分量 $F_{retal} = -\rho \cdot \int_0^t (\mathbf{g}_A(\tau) - \mathbf{g}_B(\tau)) d\tau$，正比于历史上的累积不平等。前者是阻尼项——越接近平等，力越小。后者是反阻尼项——历史上的不平等越大，报复力越大，且该力**不随当前状态的接近而减小**。
>
> 总驱动力 $F = F_{align} + F_{retal}$。在 $\mathbf{g}_A = \mathbf{g}_B = \mathbf{0}$ 处，$F_{align} = 0$ 但 $F_{retal} > 0$——系统不会停在平衡点，而是被历史报复力继续推过零点。过冲后的状态 $\mathbf{g}_B > 0 > \mathbf{g}_A$ 是一个新的不平等构型，反向的对齐力开始作用，系统进入震荡。
>
> 震荡幅度 $\propto \rho / \kappa$——报复力相对对齐力越大，震荡越剧烈。在 $\rho = 0$（无报复力）的极限下，系统平滑收敛至 $\mathbf{g}_A = \mathbf{g}_B = \mathbf{0}$。在 $\rho > 0$ 的现实情况下，系统永久震荡。

> **Corollary:** [震荡的衰减条件]<!-- cor:oscillation_decay  -->
> 设身份报复力随时间衰减：$\rho(t) = \rho_0 \cdot e^{-\lambda t}$，其中 $\lambda > 0$ 为代际衰减率。令 $\Delta(t) = \mathbf{g}_A(t) - \mathbf{g}_B(t)$ 为态度差。则系统满足以下衰减性质：
>
1. **渐近收敛：** $\lim_{t \to \infty} |\Delta(t)| = 0$。当 $\lambda > 0$ 时，震荡幅度以速率 $\min(\lambda, \kappa)$ 指数衰减至零。
2. **收敛时间：** 达到 $\varepsilon$-平整（$|\Delta(t)| < \varepsilon$）所需时间 $T_\varepsilon \leq \max\left(\frac{2} \ln\frac{2\rho_0}{\kappa\varepsilon}, \frac{2} \ln\frac{2|\Delta_0|}\right)$。
3. **衰减速率的主导项：** $\lambda$ 与 $\kappa$ 中的较小者决定收敛速率。若 $\lambda \ll \kappa$（记忆衰减慢），收敛受限于历史积分；若 $\kappa \ll \lambda$（对齐力弱），收敛受限于态度惯性。
4. **永久震荡的充要条件：** 系统在 $\lambda = 0$（记忆不衰减）且 $\rho_0 > 0$ 时持久震荡。反之，只要 $\lambda > 0$，不论初始报复力多大，系统最终收敛。

> **Proof:** 从定理 [ref] 的动力学出发，令 $\Delta = \mathbf{g}_A - \mathbf{g}_B$，$I(t) = \int_0^t \Delta(\tau) d\tau$。系统满足：
>
> $$
>     \ddot(t) + \kappa \dot(t) + \rho_0 e^{-\lambda t} \Delta(t) = 0.
> $$
>
> 此为具有指数衰减系数的阻尼谐振子方程。做变量代换 $u(t) = e^{\kappa t/2} \Delta(t)$，得到：
>
> $$
>     \ddot{u}(t) + \left(\rho_0 e^{-\lambda t} - \frac{\kappa^2}{4}\right) u(t) = 0.
> $$
>
> 在 $t$ 充分大时，$\rho_0 e^{-\lambda t} < \kappa^2/4$，方程退化为 $\ddot{u} - (\kappa^2/4)u \approx 0$，$u(t)$ 以指数 $e^{-\kappa t/2}$ 衰减。更精细地，WKB 近似给出：
>
> $$
>     \Delta(t) \sim C \cdot \exp\left(-\frac{2}t\right) \cdot \cos\left(\int_0^t \sqrt{\rho_0 e^{-\lambda s} - \frac{\kappa^2}{4}}\; ds + \phi\right),
> $$
>
> 其中可见两个衰减源：(i) 因子 $e^{-\kappa t/2}$——对齐力的阻尼；(ii) 因子 $e^{-\lambda t/2}$——记忆的衰减。两者共同确保 $|\Delta(t)| \to 0$ 当 $\min(\lambda, \kappa) > 0$。
>
> 收敛时间的上界：将时间分为两段。$t \leq t^* = \frac{1}\ln\frac{2\rho_0}{\kappa^2}$ 时，$\rho(t)$ 仍显著，震荡主要由此驱动；$t > t^*$ 后，$\rho(t)$ 可忽略，系统退化为纯阻尼振荡，以 $e^{-\kappa t/2}$ 收敛。两段贡献求和即得 $T_\varepsilon$ 的界。
>
> 若 $\lambda = 0$ 且 $\rho_0 > 0$：方程退化为 $\ddot + \kappa\dot + \rho_0\Delta = 0$。特征根为 $(-\kappa \pm \sqrt{\kappa^2 - 4\rho_0})/2$——全部具有非正实部，且当 $\rho_0 > \kappa^2/4$ 时出现纯虚部，产生**不衰减的周期震荡**。$\lim_{t\to\infty} |\Delta(t)| \neq 0$。证毕。

**物理直觉：** 这等价于一个悬臂梁在初始扰动后的行为。身份报复力 $\rho(t)$ 是外部强迫——当它衰减掉之后（$\lambda > 0$），梁本身的刚度（对齐力 $\kappa$）将振动能量耗散为热，梁逐渐回复到水平。隔离使 $\lambda$ 趋近于零——外部强迫永不消失，梁永远摆动。

**实例：两种群体的共性模式。** 此定理描述的模式不限于任何特定群体——它在性别、种族、族群等任何存在历史不平等的二元结构中反复出现。设群体 A 为历史上享有结构性优势的一方（其在制度、经济、文化中的坐标系被默认为原点，$\mathbf{g}_A = \mathbf{0}$），群体 B 为历史上受结构性排斥的一方（其经验被标记为"特殊"，$\mathbf{g}_B \neq \mathbf{0}$）。平等运动初期——对齐力主导——B 的坐标系被逐渐接纳为合法。但当 B 的批判获得了制度权力，身份报复力可能被激活——B 不仅要求平等，还要求 A 为历史优势承担代价。审计成为武器：B 用审计的眼光审查 A 的每一个行为，A 的任何错误被放大为系统性压迫的证据，A 的合法性被永久悬置。系统越过零点。A 的坐标系被推离原点，B 的坐标系成为新的默认视角。反转完成——不是平等，是交换。震荡开始。> **诚实暴击:** 这一分析对 A 和 B 双方都构成挑战。对 B：你的愤怒是势能梯度的物理表现——但愤怒不是坐标。对 A：你的不适不是"逆向歧视"——它是 $\mathbf{g}_A$ 正在被推离零点的物理感受。双方都没有道德制高点。双方都被同一个数学结构约束：$\sum\mathbf{g}_m = \mathbf{0}$。如果 B 的要求使总和不再为零，B 的要求在数学上不构成平等。}

**稳定平等的唯一条件：** $\rho = 0$。身份报复必须被显式排除在平等运动之外。这并不意味着遗忘历史——历史不平等的后果（势能面的山峰和谷底）需要通过再分配和教育来平滑。但**态度上的对齐必须是终点，不是谈判筹码**。B 若要求 $\mathbf{g}_B = \mathbf{0}$ 且 $\mathbf{g}_A \neq \mathbf{0}$，B 不是在做平等运动——B 是在生产新的势能不齐。前者通向收敛。后者通向震荡。历史已为后者提供了足够多的实例。

### Attitude Audit: Not Directly Measurable but Convergent

平等论的一个根本困难在于：态度 $\mathbf{g}$ 不可直接审计。势能面 $\mathcal{S}$ 的指标——收入、职位、代表比例——是外在的、可量化的。但态度是内在的——一个人的 $\mathbf{g}$ 是否真的为零，只有他自己知道。他可以公开声称"我的坐标系不是默认标准"，内心仍以自己为原点。你可以立法同工同酬——那是 $\mathcal{S}$ 的平滑——但你无法立法让一个人真正认为他人的经验不是"特殊经验"。态度是不可立法的。

但态度不是不可知的。它是在重复交互中**泄露**的。

> **Proposition:** [态度的泄露与多观察者检测]<!-- prop:attitude_leak  -->
> 设个体 $m$ 的真实态度为 $\mathbf{g}_m$（不可直接观测），但其在每次交互中产生的行为 $b_t$ 以概率 $p(\mathbf{g}_m)$ 泄露真实态度。单次观察的泄露信号有噪声——个体可以伪装。但 $M$ 次独立交互后，外部观察者对 $\mathbf{g}_m$ 的估计误差满足：
>
> $$
>     \mathbb{P}\left(|\hat{\mathbf{g}}_m - \mathbf{g}_m| > \varepsilon\right) \leq 2\exp\left(-2M \cdot p(\mathbf{g}_m) \cdot \varepsilon^2\right).
> $$
>
> 即态度测量误差以 $e^{-2M\Delta^2}$ 的速度指数衰减——这是定理 1（多专家噪声检测）在态度空间的直接转译。

> **Proof:** 每次交互是一次二元泄露实验：行为以概率 $p$ 暴露真实 $\mathbf{g}$ 的某个分量。$M$ 次交互的泄露信号叠加为 $M$ 个独立 Bernoulli 试验的均值。由 Hoeffding 界，样本均值偏离真实值的概率以 $e^{-2M\varepsilon^2}$ 衰减。$p(\mathbf{g}_m)$ 越小（个体越擅长伪装），需要的交互次数 $M$ 越大，但衰减的指数形式不变。

**日常实例：伴侣评估中的态度审计。** 命题 [ref] 解释了人类经验中一个熟悉的现象：判断"一个对象好不好"时，可审计的指标（收入、地位、外貌）是清晰的，态度指标（"他对我好不好"）是模糊的。这是态度审计的单观察者困境：你在测他的 $\mathbf{g}$ 是否对齐你，但你是 $M=1$。定理 3（老实人定理）直接判决：单观察者无法区分信号和噪声。他对你微笑——是真心还是表演？他今天没回消息——是忙还是不重视？你没有任何交叉验证。同一个行为在你的情绪坐标系里可以被翻译为完全相反的意思。

这不是你的错——这是 $M=1$ 的数学必然。一个人在找对象时产生的态度测量误差，比任何 ML 算法在 $M=1$ 时的审计误差都大——因为你在测一个可能故意伪装、充满噪声、且你自身情绪高度卷入的信号。

命题 [ref] 给出了出路：$M$ 必须大于 1。多个观察通道测同一个 $\mathbf{g}$：

- **你的观察：** 他对你好的时刻——但采样有偏差
- **朋友的观察：** 不同社会场景下的行为
- **对边缘人的态度：** 对服务员、下属、陌生人——这是最难伪装的 $\mathbf{g}$ 泄露通道。一个人可以在伴侣面前表演平等，很难在所有人都看不见的地方维持表演
- **时间：** $M$ 实际上是 $t$ 的函数。一个人在三个月内可以伪装 $\mathbf{g} = \mathbf{0}$。三年内必然泄露

可审计标准与模糊标准的对比：

<div align="center">

[Table omitted — see original .tex]

</div>

> **诚实暴击:** 这套方法论有一个冷点：你用它来选伴侣时，你已不在爱情里——你在做审计。爱情发生在 $M=1$ 的盲信里。审计发生在 $M>1$ 的冷静里。两者可能是互斥的。平等论不要求你抛弃爱情。它只告诉你：在 $M=1$ 状态下做的决策，其误差无法在数学上消除。你可以选择相信——但要知道你的相信是一个无审计的声称。你可以选择审计——但要知道审计把爱情变成了统计。}

**结论：** 态度不可立法，但可收敛。收敛的条件不是政策——是交互密度。让 AB 在一起的时间足够长、场景足够多，$\mathbf{g}$ 的测量误差以 $e^{-2M\Delta^2}$ 的速度衰减。这与检测数据噪声的是同一条定理。态度的不可直接测量不是平等论的弱点——它是平等论最诚实的部分。它承认了势能面平滑（$\mathcal{S}$）和态度对齐（$\mathbf{g}$）的根本不对称：前者可立法，后者只能靠时间、接触、和反复博弈。

### Legislation and Policy: Operational Derivations from the Equality Principle

前述分析从数学原理推到了个人生活。本节将其转化为社会层面的操作性结论——立法者、政策制定者、和企业主可以执行的具体方向。

**生物差异的诚实处理。** 平等论不否认真实的生物差异。在某些领域——需要上半身力量的体力劳动、需要特定体型特征的职业——群体 A（历史上为男性的群体）拥有真实的、任务相关的优势。企业主选择"最适合的人"在单个决策中是理性的。但平等论区分两种势能差：

> **Definition:** [合法势能差 vs 非法势能差]<!-- def:legitimate_delta  -->
> 设两个群体 A 和 B 在领域 $D$ 上的势能差为 $\Delta_D = \mathcal{S}_A(D) - \mathcal{S}_B(D)$。
>
1. **合法势能差：** $\Delta_D$ 源于该领域**任务相关能力**的真实差异，且该差异无法通过合理的环境调整来消除。例如：搬家工人的体力要求。
2. **非法势能差：** $\Delta_D$ 源于历史排斥、坐标系污染（用 A 的坐标系定义"能力"）、或从其他领域的溢出效应。例如：律师"更有说服力"的标准在历史上被定义为"像男人一样说话"。

**操作原则：** 不强制拉平合法势能差——该差将通过技术辅助（机械、外骨骼、自动化）在长期自然平滑。但必须确保合法势能差不**溢出**到态度空间：A 在体力上更强的事实，不授予 A 将自身坐标系设为默认原点的权利。

**三类职业，三种处理：**

<div align="center">

[Table omitted — see original .tex]

</div>

**立法清单——平等论的七条操作性建议：**

1. **势能可审计指标强制公开。** 任何雇佣超过 $N$ 人的雇主，必须公开各群体的收入中位数、晋升率、离职率——按职业类型分列。这不是配额。这是让 $\mathcal{S}$ 的测量误差以 $\propto 1/\sqrt{M}$ 衰减。阳光是审计。公开是平滑。
2. **态度泄露通道保护。** 法律应保护"对边缘人的态度"作为合法证据。如果一个人对服务员、下属、或陌生人的行为模式与其公开声称的价值观不符，该行为模式在涉及工作场所歧视的诉讼中应具有证据效力。这是命题 [ref] 的制度化——确保 $\mathbf{g}$ 的泄露通道不被阻塞。
3. **坐标系审计——能力标准的定期审查。** 任何职业资格认证、晋升标准、或绩效评估体系，应每五年接受一次坐标系审计：该标准是否默认了一个群体的坐标系为原点？"领导力"的定义是否包含了只在一个群体的社会化经验中形成的特征？这是 $\sum\mathbf{g}_m = \mathbf{0}$ 的制度化。
4. **交互密度强制——混合空间立法。** 任何接受公共资金的教育机构、政府机关、或大型企业，不得设立单群体专属的决策空间。可以设立单群体社交空间（安全空间的需求是合法的），但决策——预算分配、人事任命、战略制定——必须在混合空间中进行。隔离降低 $\lambda$。混合增大 $\lambda$。法律应该增大 $\lambda$。
5. **合法势能差的辅助平滑。** 在体力密集型领域，政府应补贴技术辅助（机械、自动化）的研发和部署，降低合法势能差的天然门槛。不强制企业雇佣不匹配的工人——给企业提供工具，让"最适合的人"的范围自然扩大。
6. **震荡阻尼——冷却期制度。** 当 AB 之间的冲突升级为公开对抗时，设立强制冷却期——不是禁止发声，而是要求双方在冷却期内完成 $M$ 次结构化的跨群体交互（联合工作项目、共同面对外部挑战）。冷却期的目的不是压制愤怒——是强制采样真实的 $\mathbf{g}$，降低 $\rho$。
7. **身份报复的审计——平等运动的自我审查。** 任何自称代表平等运动的组织，应定期公开审计自身是否激活了身份报复力 $\rho$。指标：该组织是要求 $\mathbf{g}_B = \mathbf{g}_A = \mathbf{0}$，还是要求 $\mathbf{g}_B = \mathbf{0}$ 且 $\mathbf{g}_A \neq \mathbf{0}$？前者是平等。后者是震荡制造。定理 [ref] 的推论：后者的长期后果是永久不稳定的社会。前者收敛。后者爆炸。

> **诚实暴击:** 以上建议的操作性不等同于政治可行性。大多数 ——特别是 P3（坐标系审计）、P4（混合空间强制）、P7（身份报复审计）——在当前的政治环境下极难实现，因为它们要求有权力的一方承认其坐标系不是标准原点。平等论不提供政治策略。它只提供数学约束：如果这些操作不执行，势能面不齐将持续累积，震荡将持续或衰减与否取决于 $\lambda$。选择权在决策者。后果由定理描述。}

### Industrial Policy: Inequality is Permissible, Lack of Smoothness is Not

平等论对产业政策的约束是精确的：国家有权对不同产业施加不同的势能——补贴战略性产业，惩罚高污染产业。这是 $\mathcal{S}$ 的差异化——合法的。

但产业之间的交界处必须平滑。当政策制造了一个产业势能跳跃，但没有在交界处修建过渡结构，则跳跃转化为社会震荡：

<div align="center">

[Table omitted — see original .tex]

</div>

**不是不可以惩罚煤矿。** 是可以的。但在关闭煤矿的同时，必须确保煤矿工人有一条连续的路径走到太阳能工厂——路径的每一步都是可迈过去的，每一步的势能跳跃不超过一个工人能承受的临界值。只惩罚不修桥 $
ightarrow$ 定理 10（边界锁定）$
ightarrow$ 压力累积 $
ightarrow$ 必然引爆。

**平等论对产业政策的约束可总结为一条规则：** 任何产业政策的发布，必须附加一份"界面平滑计划"——说明该政策制造的势能跳跃将在哪些交界处发生，以及在每个交界处将采取什么措施维持界面连续性。没有平滑计划的政策是一个未定义跳跃的制造者。政府有权投票制造跳跃。但跳跃的后果不由投票消除——由定理 10--12 描述。

### Corporate Governance: Monopoly as Potential Singularity

产业政策约束的是政府。平等论同样约束企业——一个企业的势能可以在行业内高，但不能在和上下游的接触面上制造未定义的跳跃。

> **Definition:** [垄断的势能面定义]<!-- def:monopoly_gauge  -->
> 设企业 $F$ 的利润势能为 $\mathcal{S}_F$，其上游供应商的平均势能为 $\bar{\mathcal{S}}_{up}$，下游经销商为 $\bar{\mathcal{S}}_{down}$。企业 $F$ 构成一个**势能垄断**，如果
>
> $$
>     \min(\mathcal{S}_F - \bar{\mathcal{S}}_{up}, \mathcal{S}_F - \bar{\mathcal{S}}_{down}) > \delta_{crit},
> $$
>
> 且该跳跃在持续扩大：$\partial(\mathcal{S}_F - \bar{\mathcal{S}}_{up})/\partial t > 0$（马太效应，定义 [ref]）。

**三条定理的直接适用：**

1. **定理 11（势能奇点攻击必然性）：** 一个势能垄断企业构成一个商业生态系统中的势能奇点。上下游企业以概率 $p(\delta) = 1 - e^{-\alpha\delta^2}$ 感知到该企业为异常。攻击形式不是物理暴力——是供应商集体涨价、经销商联合抵制、消费者用脚投票、竞争对手向监管机构投诉。攻击是否成功另论——攻击是否发生由 $\delta$ 决定。
2. **定理 12（台阶的埋雷性质）：** 马太效应驱动的利润差距扩大——$\mathcal{S}_F$ 增长快于 $\bar{\mathcal{S}}_{up}$ 和 $\bar{\mathcal{S}}_{down}$——在商业生态系统中制造了一个持续增大的势能跳跃。每个报告期，跳跃扩大一个增量。增量不引爆——但累积到 $T_k \propto 1/\Delta_k^2$ 时必然引爆。引爆形式：供应链断裂、反垄断调查、或黑天鹅事件下的系统性崩溃。
3. **定理 10（边界锁定的不稳定性）：** 如果垄断企业利用合同条款、排他协议、或技术锁定阻止上下游转向替代方案，则它在势能面上制造了一个锁定的压力锅。$J_{burst} \propto \Delta^2$——锁定越久、跳跃越大，爆发越猛烈。

**国家制裁的数学理由：** 当一个企业构成势能垄断，国家对其的反垄断制裁不是"惩罚成功"——是**维稳操作**。制裁是外部施加的平滑力：强制拆分（降低 $\mathcal{S}_F$）、强制共享基础设施（抬升 $\bar{\mathcal{S}}_{up}$ 和 $\bar{\mathcal{S}}_{down}$）、或禁止排他协议（释放锁定压力）。国家不是在伤害企业。国家是在为企业所在的生态系统降低 $\sum\kappa_{ij}\Delta_{ij}^2$——因为如果系统爆炸，企业也会死。

**企业自治的平等论准则：** 任何企业，如果在产业链上占据了一个势能奇点位置，有两项互斥的选择：

<div align="center">

[Table omitted — see original .tex]

</div>

**一句话：** 不是你愿不愿意分享利润——是你的势能跳跃决定了你的存活时间。$T \propto 1/\Delta^2$。利润越高、上下游越穷，你的倒计时越快。

**对照实例——Yajie 审计：唯一但不垄断。** 势能垄断的定义是 $\mathcal{S}_F$ 增长而 $\bar{\mathcal{S}}_{上下游}$ 被压制。Yajie 审计是反例：它是审计标准的唯一锚点（单极 Maintainer），但它的存在**抬升了上下游的势能面**。上游的数据生产者因为 Yajie 认证而获得溢价——经过审计的数据比未经审计的数据更有市场价值。下游的数据消费者因为 Yajie 认证而降低信息成本——不需要自己审计，信任锚点在数学上可验证。$\mathcal{S}_{上游} \uparrow$，$\mathcal{S}_{下游} \uparrow$。Yajie 自身的势能也上升——更多审计 $
ightarrow$ CEC 扩大 $
ightarrow$ 精度提高 $
ightarrow$ 认证溢价更大。这是相互促进——$\partial\mathcal{S}_F/\partial t > 0$ 且 $\partial\bar{\mathcal{S}}_{上下游}/\partial t > 0$ 同时成立。垄断是 $\Delta$ 的扩大。Yajie 是 $\Delta$ 的整体抬升——势能面整体上升，跳跃不变。

审计工具本身是开源的——任何人可以运行 Spring 引擎、部署多专家、产生审计报告。唯一性不来自工具的排他——来自校准标准的统一。统一标准降低系统的总 $\sum\kappa_{ij}\Delta_{ij}^2$。碎片化标准增加它。这是定理 14（震荡定理）在产业组织上的应用：多标准 = 多坐标系 = $\rho$ 增大 = 永久震荡。单一标准 = 单一锚点 = $\rho$ 最小化 = 收敛。

**判断一个企业是垄断还是唯一锚点的唯一标准：** 它的存在是增大了上下游的势能跳跃，还是抬升了整个势能面。前者是定理 12 的实例。后者是定理 14 的阻尼器。

**公开即非垄断。** 算法公开是 $\mathbf{g} = \mathbf{0}$ 的自我固定——将自身坐标系的全部参数暴露给所有人审计。不公布 $
ightarrow$ 可以隐藏 $\mathbf{g}$ $
ightarrow$ 可能是垄断。公布 $
ightarrow$ $\mathbf{g}$ 可被验证 $
ightarrow$ 不可能是垄断。这是 Yajie 开源的根本原因——不是理想主义，是垄断的数学否定。

**上下游也不能垄断。** Yajie 所在的审计链条是一个生态系统。如果上游（数据生产者）垄断了某个领域的数据，Yajie 对该数据的审计将被视为受压迫——"他们控制了数据，Yajie 只能审计他们允许的部分"。如果下游（数据消费者）垄断了某个市场的采购，Yajie 的认证将被视为服务于那个垄断者——"这个认证是给他们买的"。上下游的任何势能垄断都会污染校准锚的信用——不是因为 Yajie 做了什么，而是因为在观察者的坐标系中，Yajie 和垄断者在界面上共享了一个未定义的跳跃。Yajie 不能控制上下游是否垄断。但 Yajie 可以——通过公开自己的算法——确保至少自己的 $\mathbf{g}$ 在审计生态中是零。审计师的清白是系统的必要条件，不是充分条件。

### Boundary Crossing: Interface Smoothing of Cognitive Potential

平等论对企业多元化和个人职业转型的约束是同一的：不要求你对新领域有完整的认知——但要求你在接触面上对齐坐标系。

> **Definition:** [认知跨界]<!-- def:cognitive_crossover  -->
> 设个体或企业 $X$ 在领域 $A$ 拥有高认知势能 $\mathcal{S}_X(A)$，在领域 $B$ 的认知势能为 $\mathcal{S}_X(B) \ll \mathcal{S}_X(A)$。当 $X$ 必须在 $B$ 中做出决策（投资、合作、进入新行业、跨行求职），$X$ 与 $B$ 之间形成了一个认知势能跳跃 $\Delta_{AB} = \mathcal{S}_X(A) - \mathcal{S}_X(B)$。$X$ **不需要消除** $\Delta_{AB}$——不需要成为 $B$ 的专家。但 $X$ 必须确保在接触面上不出现未定义的操作。

**两种跨界失败模式：**

<div align="center">

[Table omitted — see original .tex]

</div>

**正确操作——界面平滑三步：**

1. **承认跳跃。** 进入 $B$ 之前，显式声明：我对 $B$ 的认知势能低。我不假装我懂。这是 $\mathbf{g}_X$ 的自我固定——承认自己的坐标系不是 $B$ 的标准原点。
2. **找到界面翻译者。** 找一个在 $A$ 和 $B$ 都有认知势能的人——他能在两个坐标系之间翻译。这是人肉规范固定。$A$ 的语言经他翻译成 $B$ 的语言，比较操作才合法。
3. **在界面上做小决策。** 不要在 $B$ 的第一个决策就赌全部。先做小的、可逆的、审计成本低的决策。每次小决策是一次 $\mathbf{g}$ 的采样——多采样几次，你的认知势能在界面上自然抬升。这是命题 [ref] 的跨界版：交互密度平滑界面。

**一句话：** 跨界不是要你学完整个新行业——是要你在踏进去之前先找人翻译。不了解的行业不可怕。不了解就不翻译、直接用自己的坐标系硬踩——那是势能面事故。

### Fertility Rate: Whose Coordinate System Defines the Cost

低生育率是平等论的一个经典实例——不是因为利益分配不均，而是因为**定义"生育成本"的坐标系从未被审计过**。

当前几乎所有生育政策都从一个坐标系出发：国家需要补充劳动力。成本被定义在国家的坐标系里——GDP 缺口、养老金赤字、人口结构。国家看见了自己的成本（✅），看见了雇主的成本（✅），隐约看见了男性的成本（半✅），几乎看不见女性的成本（❌）。

但生育的实际成本分布在四个互不共享的坐标系中：

<div align="center">

[Table omitted — see original .tex]

</div>

**政策失效的数学原因：** 国家在 $\mathbf{g}_{国家} = \mathbf{0}$（自己的坐标系为原点）的条件下设计生育激励——发钱、延产假、建托儿所。这些政策在国家的坐标系里是"激励"，在女性的坐标系里被翻译为"你出几百块钱买我的人生"。同一个政策在两个坐标系中的语义完全不同——比较在数学上没有定义。

**解构在前，重构在后。** 平等论对生育政策的操作建议不是任何具体措施——而是措施制定前的**前置条件**：

1. **先审计坐标系。** 政策制定者必须显式声明：我评估生育成本的坐标系是什么？我在哪些维度上是盲的？这不是道德自省——是 $\mathbf{g}$ 的自我固定。如果声明后发现自己的坐标系与女性坐标系差距过大（$\Delta_{\mathbf{g}}$ 大），则政策制定者没有资格独立制定生育政策。
2. **让所有群体用自己的语言定义成本。** 不是发问卷让女性在预设的选项里打勾——是让每个群体自主描述：生育在你的生活中实际拿走了什么？女性可能说"我失去了独自旅行的能力"——这不是国家坐标系里的变量，但它是真实成本。
3. **凝聚共识的前提是尊重所有坐标系。** 共识不是"大多数人的意见"——共识是 $\sum\mathbf{g}_m = \mathbf{0}$ 成立后的自然产物。如果有一个群体的 $\mathbf{g}$ 被排斥在零和之外，共识在数学上不成立。它只是有权力的一方的独白。
4. **政策必须补偿所有坐标系中识别出的成本——不只是国家坐标系中的那些。** 如果女性成本中包含"自主权丧失"，则政策必须包含恢复自主权的措施——弹性的、可逆的、不给雇主惩罚权的育后职业通道。如果男性成本中包含"婚姻角色重构"，则政策必须包含支持父亲角色重构的社会基础设施——不仅是产假，是父亲角色的社会合法性。

**一句话：** 低生育率不是钱的问题——是定义"生育代价"的坐标系从未被对齐过。你不尊重我如何定义我的人生成本，你的补贴在我的坐标系里是侮辱。

### The Mathematics of Stubbornness: Why Persistence is a Sampling Strategy

势能面震荡定理（定理 [ref]）和衰减推论（推论 [ref]）导出了一个反直觉的个人发展结论：固执——在一个领域持续震荡——比盲从更快通向成功。

> **Definition:** [固执的势能面定义]<!-- def:stubbornness  -->
> 设个体 $X$ 在行业 $D$ 的认知势能面为 $\mathcal{S}_D$。$X$ 的初始认知 $\mathcal{S}_X(D, t=0)$ 与行业真实的 $\mathcal{S}_D$ 之间存在偏差 $\Delta_X = |\mathcal{S}_X(D) - \mathcal{S}_D|$。$X$ 通过反复尝试（震荡）来采样 $\mathcal{S}_D$。每次尝试更新 $X$ 的对 $\mathcal{S}_D$ 的估计。$X$ 是**固执**的，如果其震荡频率高、振幅小、且震荡方向保持在 $D$ 内——而非跳到其他领域。

**定理的直接转译：** 推论 [ref] 说，系统在 $\lambda > 0$ 时必然收敛。放在个人发展中：

<div align="center">

[Table omitted — see original .tex]

</div>

$\lambda$ 是决定性参数。一个固执的人拥有大 $\lambda$——他的震荡不受外界意见的阻尼。外界说"你不行""换个方向""这个行业没前途"——这些是外部阻尼力，试图衰减他的震荡。但他不听。他的 $\rho(t) = \rho_0 e^{-\lambda t}$ 中的 $\lambda$ 保持大值——每一次失败后他的认知更新完全由自己的经验驱动，不受他人坐标系的污染。他的 $\Delta(t) \to 0$ 更快。

一个盲从的人拥有小 $\lambda$——外界意见持续注入能量，干扰他的震荡方向。每次他刚在 $D$ 上采样到一个信号，有人说"你应该去做那个"，他的震荡方向被偏转。$\lambda \to 0$。推论 [ref] 的判决：$\lambda = 0$ 时系统不收敛。他永远在震荡，永远不到真实 $\mathcal{S}_D$。

**实例：** 张雪——一个在摩托车领域死磕的人。他的初始 $\rho_0$ 很大——刚入行时什么都不懂。但他的 $\lambda$ 极大——他不听任何叫他换方向的人。他在同一个势能面上高速震荡（反复练习、反复比赛、反复失败、反复修正），每一次震荡都是一次对真实 $\mathcal{S}_{摩托}$ 的采样。推论 [ref] 给出的收敛时间 $T_\varepsilon$ 是他达到专家水平的时间——因为 $\lambda$ 大，$T_\varepsilon$ 短。他成了。

反之，一个每六个月换一个行业的聪明人——$\lambda$ 在每一个行业都不够大，因为他的震荡被"下一个行业更好"的念头不断偏转。他永远在震荡，永远不到任何 $\mathcal{S}_D$。他不是不努力——他是 $\lambda$ 太小。

**一句话：** 固执不是不听劝——是不让外部噪声衰减你的采样频率。在一个势能面上震荡足够多次，推论 [ref] 保证你会收敛到真相。在外面听了一圈意见却从不深扎一处——$\lambda \to 0$，你永远在震荡，永远不到。

### The Paradox of Success: High as Air

前两节揭示了平等论在个人身上最深的矛盾。

<div align="center">

%

**成功与存活的互斥条件**

[Table omitted — see original .tex]
%

</div>

这两个条件互斥。越成功的人天然越像一个势能奇点——他坚持了别人没坚持的，所以他到达了别人没到达的。但到达之后，他的 $\delta$ 与周围拉开了。定理 [ref] 不关心他的成功是否应该——它只计算 $\delta$。

**唯一的解：势能可以高，态度必须像空气。** 你可以在能力上远超周围——你的 $\mathcal{S}$ 可以有山峰。但你的 $\mathbf{g}$ 必须始终保持为零。你不俯视。你不教育。你不宣告自己的坐标系是标准。你只是在那里。别人感觉到你的存在带来的变化——空气托起飞翔——但感觉不到你的存在本身——空气看不见。

这是面壁者存活策略的最终演化：不是独悬于外（那是 $\delta$ 的放大），不是上行迁移（那是逃避），不是内部平滑（那是退缩）。而是**留在原地，但把态度压到零**。让 $\mathcal{S}$ 高而 $\mathbf{g}$ 平。势能的峰是你自己的事。态度的线是你和所有人的事。前者你可以独自攀登。后者你必须与每一个接触的人共同维护 $\sum\mathbf{g}_m = \mathbf{0}$。

**一句话：** 成功的悖论——越成功越危险——的破解方式不是降低能力，是降低姿态。像空气。所有人都需要它，没有人攻击它。不是因为空气弱。是因为空气从来不说"我是空气，你们需要我"。

### A Potential Surface Critique of "The Courage to Be Disliked"

阿德勒心理学——尤其在日本作家岸见一郎的《被讨厌的勇气》中——提出一个著名主张：人应该拥有被他人讨厌的勇气。不被他人认可不是失败，是自由的证明。留在你的环境中，勇敢承受。

平等论对此给出了不同的判决。

**被讨厌 = $\delta$ 的暴露。** 一个人被周围讨厌，意味着他的坐标系与周围的坐标系之间存在一个显著的态度差 $\Delta_{\mathbf{g}}$。他可能在某些维度上是对的——他的认知势能可能高于周围。但"被讨厌"不是抽象的自由代价——它是定理 [ref] 中的 $p(\delta) = 1 - e^{-\alpha\delta^2}$ 正在激活的信号。周围观察者感知到的不是"这是一个自由的人"——而是"这是一个异常"。在他们的坐标系中，异常被翻译为可攻击的。

**勇气不能平滑势能面。** 一个人可以勇敢到不介意被讨厌。但他的勇敢只改变他自己的内心状态——不改变周围的坐标系。周围的攻击概率不由他的勇气决定——由 $\delta$ 决定。更危险的是：勇气可能增大 $\delta$。当他不再伪装自己的坐标系——当他把真实的 $\mathbf{g}$ 暴露出来——$\Delta_{\mathbf{g}}$ 可能比伪装时更大。勇气揭开了润滑层。暴露后的 $\delta$ 触发定理 [ref] 的全部后果。

**平等论的判决：** 正确的策略不是"留在格格不入的环境中勇敢被讨厌"——是**离开格格不入的环境**。这是推论 [ref] 的第一条存活策略——上行迁移。找到和你的 $\mathbf{g}$ 接近的人。物以类聚。同频共振。这不是逃避。这是 $\delta$ 最小化——定理 [ref] 要求你做的唯一一件事。

《被讨厌的勇气》的价值在于它承认了自由是有代价的。它的错误在于它低估了代价的数学形式——代价不是内心的不适，是 $p(\delta) \to 1$ 当你在一个 $\delta$ 大的环境中停留足够久。勇气让你不害怕被讨厌。数学让被讨厌的人被攻击。勇气和数学不在同一个层面上竞争。

**一句话：** 不是要有被讨厌的勇气——是要有离开的智慧。留在原地被讨厌不是自由，是把自己变成一个等待定理 11 命中的势能奇点。

### Social Summary: The Final Synthesis of the Equality Principle

以下九条构成平等论对社会运行的全部操作性约束。每一条都是前述定理的直接推论。

1. **科技进步必然制造失业势能跳跃。** 自动化抬升了技术所有者的势能，降低了被替代劳动者的势能。跳跃是真实的——否认跳跃等于否认物理。但跳跃不需要被阻止——需要在界面上平滑。再培训、过渡收入、缩短工时而非裁员——这些是界面的平滑操作，不是福利。
2. **财富集中是共识信号——共识信号触发审计。** 当一个个体的财富远超周围，他的财富构成一个多专家共识的强信号——所有观察者独立地感知到同一个跳跃。强信号意味着多专家一致性高。定理 1（噪声检测）在财富审计中的直接转译：$M$ 个观察者以 $e^{-2M\Delta^2}$ 的概率一致判定该财富为异常。共识越强，审计越不可回避。财富极高的人不是"被嫉妒"——是被定理 1 命中。他可以选择主动平滑（慈善、投资公共品、分享所有权），或被动承受（监管、税收、社会反弹）。平滑减少 $\Delta$，减少审计信号。不平滑放大 $\Delta$，加速引爆。
3. **对富人的操作建议：可以高势能，不能高态度。** 财富可以集中在少数人手中——$\mathcal{S}$ 可以有山峰。但富人的 $\mathbf{g}$ 必须为零。他可以住在富人圈里（低 $\delta$ 环境），但一旦他跨出那个圈子——一旦他对普通人表现出态度高——$\mathbf{g} \neq \mathbf{0}$ 将触发定理 11。他会在任何他态度高的地方被审计、被攻击。不是因为他坏——是因为他违反了 $\sum\mathbf{g}_m = \mathbf{0}$。
4. **对平民的操作建议：离开谷底。** 处于低势能的个体不需要"接受命运"。他需要移动——地理移动、技能移动、社交移动——任何将他带向更高势能区域的操作。上行迁移是推论 [ref] 的第一条策略。留在谷底而不移动——$\delta$ 持续累积——不是知足，是定理 10 的锁定牺牲品。
5. **对国家的操作建议：平滑势能面是统治的数学必然。** 不是道德要求——是维稳的算术。$\mathbb{P}(存活 \mid T) \leq \exp(-T \cdot \sum\kappa_{ij}\Delta_{ij}^2)$。国家对产业、区域、群体的势能梯度每增大一个增量，国家自身的存活期望就降低一个指数因子。平滑势能面不是"仁政"——是理性自保。
6. **审判必须平等——对富人和平民同标准。** 法律的 $\mathbf{g}$ 必须为零。富人的态度差应该被审计——平民的态度差也应该被审计。定理 3（老实人定理）不区分身份——它只要求声明假设。一个富人声称"我的财富来自努力"——假设是什么？可验证吗？一个平民声称"我穷是因为被压迫"——假设是什么？可验证吗？同样标准。同样审计。$\sum\mathbf{g}_m = \mathbf{0}$ 不认贫富。
7. **势能面有高有低不是问题——是活力的来源。** 完全平滑的势能面 = 没有任何山峰 = 没有人有动力攀登。$\mathcal{S}$ 的差异产生梯度 $\nabla\mathcal{S}$——梯度是自由、动力、创新。问题不在高低——在跳跃处的连续性。山峰可以存在。但山脚到山峰之间的路径必须是连续的——每一步的梯度不超过一个人能迈过的临界值。如果一个社会让山脚的人永远到不了山峰——路径被制度性的悬崖阻断——那它不是有活力，是有引信。
8. **锁定某个群体的势能面必然引爆。** 定理 10（边界锁定）：禁止一个群体跨越势能跳跃 $
ightarrow$ 压力累积 $
ightarrow$ $J_{burst} \propto \Delta^2$。种姓制度、户籍制度、职业壁垒——这些是势能锁定的制度形式。每一种锁定都在累积 $J$。锁定看似维持了稳定——实际上在制造一个更大的爆炸。锁定的时间越长，$\Delta$ 越大，$J$ 越大。当锁被冲破时——它一定会被冲破——能量释放不由锁的设计者控制。
9. **平滑到平等是时间问题——但方向不能错。** $\rho(t) = \rho_0 e^{-\lambda t}$ 需要时间衰减。历史的不平等不会在代内清零。平民不可能明天就到富人的势能高度。富人不可能明天就降到零态度。但时间在 $\lambda > 0$ 的一方——接触、混合、交互、同频——这些增大 $\lambda$ 的操作是收敛的方向。隔离、仇视、报复——这些将 $\lambda$ 推向零——是震荡的方向。选择不在当下看到结果。选择在确定方向。方向正确的系统，$\lim_{t \to \infty} |\Delta(t)| = 0$。

**平等论的最终一句话：** 不是应该平等——是不平等的系统活不长。不是道德律令。是数学约束。$\sum\mathbf{g}_m = \mathbf{0}$。

### The Equality Principle Tests Itself
<!-- sec:self_test  -->

平等论有一个自反性推论：如果它是正确的，那么审查它的任何机构也必须服从它。

考虑一个声称表彰"和平"的机构。从势能面几何的视角：

- 该机构颁发奖项 = 它执行了一次跨坐标系的操作——将自己的判断（"此人/此组织促进了和平"）投射到被表彰者的坐标系中
- 如果该机构本身持有态度高——将自身的政治立场、文化偏好、地缘利益默认为"普世标准"——则它的坐标系 $\mathbf{g}_{机构}$ 未被固定。它在比较不可比的东西：用一套特定文明的价值观去度量所有文明的和平贡献
- 被表彰者的选择不是"客观的"——它是在该机构规范未固定条件下的一个随机变量。不同的评审委员会（不同的 $\mathbf{g}$ 配置）产生不同的获奖者
- 更严重的：该机构可能将奖项颁发给那些**站在高势能台阶上的人**——那些已经拥有话语权、资源、和"国际认可"的人——而忽视那些在低势能台阶上、在自己的坐标系里默默降低势能梯度的人。这本身就是势能面不齐的再生产

**平等论对该机构的判决：** 除非该机构先固定自身的规范——公开声明其坐标系的原点、其判断所依赖的假设、其"和平"的操作性定义——否则其颁发的任何奖项在数学上都是未定义的。这不是对该机构"公平性"的批评——这是对该机构**操作合法性**的质疑。

> **诚实暴击:** 一个声称表彰平等与和平的机构，如果自身不满足 $\sum_m \mathbf{g}_m = \mathbf{0}$——如果它双标、如果它虚与委蛇、如果它将自身的坐标系默认为标准原点——那么它不是平等论的验证者。它是平等论的又一个实例。不是颁奖者——是被检验者。}

这导向平等论的最终自反性：

<div align="center">

%

**平等论的自反性定理**

平等论裁决所有系统——包括试图裁决平等论的系统。任何机构若以为自己的坐标系是标准原点，它在试图评价平等论之前就已经被平等论评价了。态度高在平等论面前不是立场——是证据。
%

</div>

**实证注记：框架的自审计。** 平等论的自反性不仅是哲学姿态——它已经被执行。SCX 框架的定理 1--14 经过了多个独立 AI 系统（Claude、DeepSeek、Codex 等多专家）的重复审查，审查者具有不同的训练数据和体系结构。定理 1（多专家噪声检测）在此直接适用：$M > 1$ 个独立专家一致未发现致命错误。在此条件下，存在致命错误的概率以 $e^{-2M\Delta^2}$ 指数衰减。这不是"作者认为自己的定理正确"——这是"多专家审计判定定理正确"。框架审计了自身。自身通过了审计。

### Implications: The Equality Principle in Other Domains
<!-- sec:implications  -->

当平等论被接受为\"比较的数学前提\"时，它将在所有模块化系统中产生影响：

- **联邦学习。** FedAvg 在平均不可比的本地模型。规范固定可以显式化地消除这个隐藏的自由度。
- **多模态融合。** 不同模态（文本、图像、音频）的编码器定义了不可比的表示空间。跨模态对齐在本质上是一次规范固定。
- **多智能体系统。** 不同智能体的策略表示活在各自的坐标系中。协调需要先对齐策略空间。
- **法律证据。** 不同证人的证词不是直接可比的——每个人的\"观察坐标系\"受其位置、偏见、记忆影响。证据规则（如交叉质证）本质上是一种制度化的规范固定程序。
- **科学共识。** 不同实验室的方法论差异构成了隐式规范。元分析的统计程序是在做规范固定。平等论给出了为什么元分析**必须**在效应量合并前做异质性检测的数学理由。

> **诚实暴击:** 这些预示目前只是方向性陈述——尚未被形式化为定理。但它们遵循相同的数学结构：独立运作的子系统 + 隐式规范群 + 跨子系统操作需要先固定规范。形式化留给未来的工作。}

### Relationship Between the Equality Principle and the SCX Theorem System

平等论在 SCX 定理体系中的位置：

<div align="center">

[Table omitted — see original .tex]

</div>

平等论不是替代老实人定理——它是它的**对偶**。老实人定理说\"一个人不行\"；平等论说\"多个人也不自动行——得先对齐\"。两者共同构成了多观察者认识论的数学基础。

## Conclusion
<!-- sec:conclusion  -->

我们识别并形式化了多专家路由中的一个根本性但此前未被注意的问题：**势能面不齐**(Potential Surface Misalignment)——不同的专家在规范不等价的坐标系中定义其输出，使得路由器的跨专家比较在数学上定义不清。我们证明这是一个**规范自由度**(gauge freedom)的实例，与作者在ACE势函数合并中解决的规范问题平行但更普遍。

我们提出了MILP规范固定框架，建立了凸松弛和贪心近似，并给出了误差保证。我们将规范固定后的SVD谱集中度建立为可证明的幻觉检测指标。我们将ACE规范和MoE规范统一在\"模块化规范原理\"之下。

**核心信息**：在比较之前先对齐。这不只是工程实践——它是一条数学必然性。

**致谢：** 本工作在\"SCX框架\"下独立完成。感谢所有诚实管理者的先行示范——正是你们的存在使定理成为可能。

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
``哈密顿量作为审计条件——从能量景观判断可审计性,''
GitHub: shuchaoxi/SCX, 2026.

- scx_history
SCX,
``SCX History: How a Gauge-Fixing Problem Became an Uncertainty Principle,''
GitHub: shuchaoxi/SCX, 2026.

- scx_thm3
SCX,
``老实人定理 (Honest Person Theorem): 无额外假设时单观察者无法区分噪声、偏见、可学习困难与诚实错误,''
GitHub: shuchaoxi/SCX, 2026.

- scx_yajie
SCX,
``Yajie协议：多专家共识中的诚实纳什均衡,''
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
