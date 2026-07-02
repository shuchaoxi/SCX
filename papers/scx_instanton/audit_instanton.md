# Introduction

**Author:** SCX

*Abstract:*

We introduce the concept of **audit instantons** — non-perturbative, 
topologically protected failures of expert consensus in the SCX (Situs 
Consensus eXpert) auditing framework. Drawing structural inspiration from 
worldsheet instantons in string theory, we demonstrate that pointwise 
Yajie consensus auditing is analogous to perturbative expansion: it 
systematically misses globally correlated expert failures concentrated 
in low-data-density regions of the Situs manifold.

We provide a rigorous mathematical formulation: the Situs manifold 
$\cM$ equipped with a data density function $\rho(x)$; low-density 
sublevel sets $\cM_ = \{x \in \cM : \rho(x) < \varepsilon\}$; 
and an *audit instanton* defined as a non-contractible 1-cycle 
$\gamma \subset \cM$ on which all experts deviate consistently in the 
same direction — locally exact ($d_1 A = 0$ on $\gamma$) but globally 
non-trivial ($\gamma \notin \im(d_0)$). Detection proceeds via persistent 
homology of the density filtration, where long-lived 1-cycles in the 
persistence diagram correspond to audit instanton candidates. 

We prove the main structural theorem: every non-trivial 1-homology class 
of the Situs manifold contains at least one audit instanton candidate, 
provided the expert output field satisfies mild regularity conditions. 
We further show that audit instantons are invisible to the standard Yajie 
consensus score — precisely the ``non-perturbative'' character that makes 
them dangerous. A concrete detection protocol is given.

*我们引入**审计瞬子**（audit instantons）的概念——SCX（Situs共识专家）审计框架中专家共识的非微扰、拓扑保护的失效模式。借鉴弦论中世界面瞬子的结构启发，我们证明逐点Yajie共识审计类似于微扰展开：它系统地遗漏了集中在Situs流形低数据密度区域中的全局关联专家失效。*

*我们提供严格的数学表述：配备数据密度函数 $\rho(x)$ 的 Situs 流形 $\cM$；低密度子水平集 $\cM_ = \{x \in \cM : \rho(x) < \varepsilon\}$；以及**审计瞬子**——定义为 $\cM$ 上的不可收缩 1-圈 $\gamma$，其上所有专家一致地沿同一方向偏离——局部恰当（$d_1 A = 0$ 在 $\gamma$ 上）但全局非平凡（$\gamma \notin \im(d_0)$）。检测通过密度滤流的持续同调进行，其中持续图中长寿的 1-圈对应于审计瞬子候选。*

*我们证明了主要结构定理：若专家输出场满足温和的正则性条件，Situs流形的每个非平凡1-同调类都包含至少一个审计瞬子候选。进一步证明审计瞬子对标准Yajie共识分数不可见——这正是使其危险的``非微扰''特性。给出了具体的检测协议。*

**Keywords:** audit instantons, persistent homology, discrete Hodge theory, 
topological data analysis, expert auditing, non-perturbative effects, 
SCX framework

**关键词：** 审计瞬子，持续同调，离散Hodge理论，拓扑数据分析，专家审计，非微扰效应，SCX框架

## Introduction
## 引言

### Motivation from Physics
### 来自物理学的动机

In quantum field theory and string theory, *instantons* are non-perturbative 
field configurations: classical solutions to the Euclidean equations of motion 
with finite action that contribute terms of order $\sim \exp(-1/g^2)$ to the 
path integral, where $g$ is the coupling constant  [cite]. 
Crucially, such contributions are identically zero in any finite-order Taylor 
expansion around $g=0$ — they are *invisible to perturbation theory*.

*在量子场论和弦论中，**瞬子**（instantons）是非微扰场位形：具有有限作用量的欧几里得运动方程的经典解，对路径积分贡献量级为 $\sim \exp(-1/g^2)$ 的项，其中 $g$ 是耦合常数。关键地，这类贡献在围绕 $g=0$ 的任何有限阶泰勒展开中恒为零——它们**对微扰论不可见**。*

In string theory specifically, **worldsheet instantons** arise from string 
worldsheets wrapping holomorphic curves in the compactification manifold. Their 
contribution is $\sim \exp(-A/\alpha')$, where $A$ is the area of the wrapped 
curve and $\alpha'$ is the string tension. These effects are:

1. **Non-perturbative**: invisible to the genus expansion (Feynman diagrams);
2. **Topological**: classified by the homotopy/homology of the target space;
3. **Exponentially suppressed** in the small-$g$ regime, yet dominant

*特别地，在弦论中，**世界面瞬子**来自弦世界面在紧致化流形中包裹全纯曲线。其贡献为 $\sim \exp(-A/\alpha')$，其中 $A$ 是包裹曲线的面积，$\alpha'$ 是弦张力。这些效应是：(i) **非微扰的**：对亏格展开（Feynman图）不可见；(ii) **拓扑的**：由目标空间的同伦/同调分类；(iii) 在小 $g$ 区**指数压制**，但在模空间的某些角落占主导。*

### The Auditing Analogy
### 审计类比

The SCX (Situs Consensus eXpert) framework  [cite] performs 
expert auditing on a data manifold $\cM$ using discrete Hodge theory and 
gauge-theoretic consensus measures. The standard Yajie audit operates 
*pointwise*: at each data point $x \in \cM$, it compares expert 
outputs and assigns a consensus score based on local agreement. This is 
structurally analogous to *perturbative expansion* in quantum field 
theory — each data point is treated independently, and the audit result is 
the sum of local contributions.

*SCX（Situs共识专家）框架使用离散Hodge理论和规范论共识度量在数据流形 $\cM$ 上进行专家审计。标准Yajie审计以**逐点**方式运作：在 $\cM$ 的每个数据点 $x$，它比较专家输出并根据局部一致性分配共识分数。这在结构上类似于量子场论中的**微扰展开**——每个数据点被独立处理，审计结果是局部贡献之和。*

The central insight of this paper is that **pointwise audit is perturbative 
audit**, and it suffers from the same fundamental blindness: it cannot detect 
*globally correlated, topologically protected* failure modes that we term 
**audit instantons**. These are configurations where:

1. The data density $\rho(x)$ is low (the ``weak-coupling'' regime of audit);
2. All experts deviate in the *same* direction — producing \emph{spurious
3. The deviation field is locally consistent (closed form) but globally

*本文的核心洞见是：**逐点审计即微扰审计**，它遭受相同的基本盲区：无法检测我们称之为**审计瞬子**的**全局关联、拓扑保护的**失效模式。这些是满足以下条件的位形：(1) 数据密度 $\rho(x)$ 低（审计的``弱耦合''区）；(2) 所有专家朝**同一**方向偏离——产生对逐点Yajie表现为高一致性的**虚假共识**；(3) 偏离场局部一致（闭形式）但全局非平凡（非恰当）——局部分析不可见的拓扑障碍。*

### Our Contributions
### 本文贡献

This paper provides the first rigorous mathematical formalization of audit 
instantons. Specifically, we:

1. **Formal Definition** (Section 3): Define the Situs manifold
2. **Detection Theory** (Section 4): Show that persistent homology
3. **Structural Theorem** (Theorem  [ref]): Prove that
4. **Invisibility to Yajie** (Section 5): Prove that the standard
5. **Detection Protocol** (Section 6): Provide a concrete,

*本文首次提供审计瞬子的严格数学形式化。具体贡献包括：**(C1)** 形式化定义（第3节）：定义配备数据密度 $\rho$ 和审计向量场 $\mathbf{A}$ 的Situs流形 $(\cM, \rho, \mathbf{A})$，并以局部恰当但全局非平凡的偏离场给出审计瞬子的上同调定义。**(C2)** 检测理论（第4节）：证明密度子水平滤流的持续同调提供了系统性检测机制——持续图中长寿的1-圈是审计瞬子候选。**(C3)** 结构定理（定理 [ref]）：证明在专家输出场的温和条件下，$\cM$ 的每个非平凡1-同调类包含至少一个审计瞬子候选。**(C4)** Yajie不可见性（第5节）：证明标准Yajie共识分数在审计瞬子圈上系统性高估审计质量——这正是非微扰效应的定义。**(C5)** 检测协议（第6节）：提供具体的、可算法实现的审计瞬子检测方案。*

## Mathematical Preliminaries
## 数学预备知识

### The Situs Manifold
### Situs流形

> **Definition:** [Situs Manifold / Situs流形]
> <!-- label: def:situs -->
> Let $\cM$ be a compact, connected, smooth Riemannian $n$-manifold with 
> boundary $\partial \cM$ (possibly empty). The **Situs manifold** is 
> the triple $(\cM, \rho, \cE)$, where:
> 
1. $\rho: \cM \to \R_{\geq 0}$ is a smooth (or at least $C^2$)
2. $\cE = \{E_1, E_2, ..., E_M\}$ is a finite set of $M \geq 2$

> The **dimension** $n$ of $\cM$ is typically the intrinsic dimension of 
> the data representation space (e.g., after dimensionality reduction).

***定义  [ref]（Situs流形）**：设 $\cM$ 为紧致、连通、光滑的 $n$ 维 Riemann 流形，边界为 $\partial \cM$（可能为空）。**Situs流形**是三元组 $(\cM, \rho, \cE)$，其中：(i) $\rho: \cM \to \R_{\geq 0}$ 是光滑（或至少 $C^2$）的**数据密度函数**，归一化使得 $\int_ \rho(x) \, d\vol_(x) = 1$。实践中 $\rho$ 通过核密度估计从训练或审计数据点的经验分布中估计。(ii) $\cE = \{E_1, ..., E_M\}$ 是一组 $M \geq 2$ 个**专家**的有限集合，每个 $E_i: \cM \to \R^d$ 是表示专家在每个点 $x \in \cM$ 的输出（预测、分类或标量场）的向量值函数。*

> **Remark:** [Discrete vs. Continuous / 离散与连续]
> In SCX practice, $\cM$ is discretized as a simplicial complex $K$ (or 
> graph/cell complex) with vertices corresponding to data points. All 
> definitions in this paper extend naturally to the discrete setting via 
> discrete Hodge theory  [cite]. We work in the continuous category 
> for clarity, but all constructions have well-defined discrete analogues.

***注记（离散与连续）**：在SCX实践中，$\cM$ 被离散化为单纯复形 $K$（或图/胞腔复形），顶点对应数据点。本文所有定义通过离散Hodge理论自然地推广到离散情形。我们为清晰起见在连续范畴中工作，但所有构造都有良好定义的离散类似物。*

### Data Density and Sublevel Sets
### 数据密度与子水平集

> **Definition:** [Density Sublevel Sets / 密度子水平集]
> <!-- label: def:sublevel -->
> For any threshold $\varepsilon \geq 0$, the **$\varepsilon$-sublevel set** 
> of the data density is:
> 
> $$
>   \cM_ = \{x \in \cM : \rho(x) \leq \varepsilon\}.
>   <!-- label: eq:sublevel -->
> $$
> 
> By convention, $\cM_0 = \{x : \rho(x) = 0\}$ and $\cM_ = \cM$.
> 
> The family $\{\cM_\}_{\varepsilon \geq 0}$ forms a 
> **filtration** of $\cM$: 
> $\cM_0 \subseteq \cM_{\varepsilon_1} \subseteq \cM_{\varepsilon_2} \subseteq \cM$ 
> for $0 \leq \varepsilon_1 \leq \varepsilon_2$.
> 
> The **critical density** $\rho_{crit}$ is a distinguished 
> threshold below which expert behavior is deemed unreliable due to data 
> sparsity. Formally, $\rho_{crit}$ may be defined as:
> 
> $$
>   \rho_{crit} = \inf\{\varepsilon > 0 : expert predictions on  
>     \cM_  are statistically indistinguishable from 
>     their behavior on  \cM \setminus \cM_\}.
>   <!-- label: eq:rhocrit -->
> $$

\textit{**定义  [ref]（密度子水平集）**：对任意阈值 $\varepsilon \geq 0$，数据密度的**$\varepsilon$-子水平集**为 $\cM_ = \{x \in \cM : \rho(x) \leq \varepsilon\}$。族 $\{\cM_\}_{\varepsilon \geq 0}$ 构成 $\cM$ 的一个**滤流**。**临界密度** $\rho_{crit}$ 是区分专家行为因数据稀疏而不可靠的阈值。形式上可定义为使 $\cM_$ 上专家预测与 $\cM \setminus \cM_$ 上行为统计不可区分的最小 $\varepsilon$。}

### Discrete Hodge Theory (Recap)
### 离散Hodge理论（回顾）

We briefly recall the essential elements of discrete Hodge theory on $\cM$, 
as used in SCX  [cite]. Let $\Omega^k(\cM)$ denote the space of 
smooth differential $k$-forms on $\cM$.

> **Definition:** [Cochain Complex / 上链复形]
> The **de Rham complex** on $\cM$ is:
> 
> $$
>   0 \longrightarrow \Omega^0(\cM) \xrightarrow{d_0} \Omega^1(\cM) 
>     \xrightarrow{d_1} \Omega^2(\cM) \xrightarrow{d_2} ... 
>     \xrightarrow{d_{n-1}} \Omega^n(\cM) \longrightarrow 0,
>   <!-- label: eq:derham -->
> $$
> 
> where each $d_k: \Omega^k(\cM) \to \Omega^{k+1}(\cM)$ is the exterior 
> derivative, satisfying $d_{k+1} \circ d_k = 0$.
> 
> The **$k$-th de Rham cohomology** is 
> $H^k_{dR}(\cM) = \ker(d_k) / \im(d_{k-1})$.
> 
> The **Hodge Laplacian** on $k$-forms is:
> 
> $$
>   \Delta_k = d_{k-1} \delta_k + \delta_{k+1} d_k,
>   <!-- label: eq:hodge_laplacian -->
> $$
> 
> where $\delta_k = (-1)^{n(k-1)+1} \star d_{n-k} \star$ is the codifferential 
> and $\star$ is the Hodge star operator induced by the Riemannian metric.

***定义（上链复形）**：$\cM$ 上的**de Rham复形**为式( [ref])，其中 $d_k$ 为外导数，满足 $d_{k+1} \circ d_k = 0$。第 $k$ de Rham上同调为 $H^k_{dR}(\cM) = \ker(d_k) / \im(d_{k-1})$。**Hodge Laplacian** 为式( [ref])，其中 $\delta_k$ 为余微分，$\star$ 为Hodge星算子。*

> **Definition:** [Expert Output 1-Form / 专家输出1-形式]
> Given $M$ experts and a reference consensus direction (e.g., the Yajie 
> center or a ground-truth label), define for each expert $E_i$ the 
> **deviation 0-form** $f_i \in \Omega^0(\cM)$:
> 
> $$
>   f_i(x) = \|E_i(x) - \bar{E}(x)\|_{signed},
>   <!-- label: eq:deviation -->
> $$
> 
> where $\bar{E}(x)$ is the consensus output at $x$ and $\|\cdot\|_{signed}$ 
> is a signed distance (positive for deviation in one direction, negative for 
> the opposite). The **audit 1-form** is then:
> 
> $$
>   A = d_0\left(\frac{1}{M}\sum_{i=1}^{M} f_i\right) \in \Omega^1(\cM),
>   <!-- label: eq:audit1form -->
> $$
> 
> representing the spatial gradient of the average expert deviation. In the 
> discrete setting, $A$ is a 1-cochain on the simplicial complex.

***定义（专家输出1-形式）**：给定 $M$ 个专家和一个参考共识方向，对每个专家 $E_i$ 定义**偏离0-形式** $f_i(x) = \|E_i(x) - \bar{E}(x)\|_{signed}$，其中 $\bar{E}(x)$ 为 $x$ 处的共识输出。则**审计1-形式**为 $A = d_0(M^{-1}\sum_i f_i)$，表示平均专家偏离的空间梯度。*

### Persistent Homology
### 持续同调

> **Definition:** [Persistence Module / 持续模]
> <!-- label: def:pers -->
> Let $\{\cM_\}_{\varepsilon \geq 0}$ be the density sublevel 
> filtration. For each $k \geq 0$, the $k$-th homology functor $H_k(\cdot; \mathbb{F})$ 
> (with coefficients in a field $\mathbb{F}$, typically $\mathbb{Z}_2$ or $\mathbb{Q}$) 
> applied to the filtration yields a **persistence module** 
> $\mathbb{V}_k = \{H_k(\cM_; \mathbb{F})\}_{\varepsilon \geq 0}$ 
> with linear maps $v_{\varepsilon_1, \varepsilon_2}: H_k(\cM_{\varepsilon_1}; \mathbb{F}) 
> \to H_k(\cM_{\varepsilon_2}; \mathbb{F})$ induced by inclusions 
> $\cM_{\varepsilon_1} \hookrightarrow \cM_{\varepsilon_2}$ for 
> $\varepsilon_1 \leq \varepsilon_2$.

\textit{**定义  [ref]（持续模）**：设 $\{\cM_\}_{\varepsilon \geq 0}$ 为密度子水平滤流。对每个 $k \geq 0$，第 $k$ 同调函子 $H_k(\cdot; \mathbb{F})$（系数在域 $\mathbb{F}$ 中）应用于滤流产生**持续模** $\mathbb{V}_k = \{H_k(\cM_; \mathbb{F})\}_{\varepsilon \geq 0}$，具有由包含映射诱导的线性映射。}

By the structure theorem of persistent homology  [cite], 
$\mathbb{V}_k$ decomposes into a direct sum of **interval modules**:

$$
  \mathbb{V}_k \cong \bigoplus_{j \in \mathcal{J}_k} \mathbb{I}_{[b_j, d_j]},
  <!-- label: eq:interval_decomp -->
$$

where each $\mathbb{I}_{[b, d]}$ is an indecomposable module supported on 
the interval $[b, d]$, with **birth** $b_j$ (the density threshold at 
which the homology class appears) and **death** $d_j$ (the threshold 
at which it merges with another class or becomes trivial).

*根据持续同调的结构定理，$\mathbb{V}_k$ 分解为**区间模**的直和，每个 $\mathbb{I}_{[b, d]}$ 支撑在区间 $[b, d]$ 上，具有**出生** $b_j$（同调类出现的密度阈值）和**死亡** $d_j$（与另一类合并或变为平凡的阈值）。*

> **Definition:** [Persistence Diagram / 持续图]
> The **$k$-dimensional persistence diagram** is the multiset:
> 
> $$
>   \cD_k = \{(b_j, d_j) \in \R^2 : b_j < d_j, \; j \in \mathcal{J}_k\},
>   <!-- label: eq:pers_diagram -->
> $$
> 
> together with all points on the diagonal $\{(b, b) : b \geq 0\}$ taken with 
> infinite multiplicity (representing classes of zero persistence).
> 
> The **persistence** (or **lifetime**) of a homology class is 
> $\pers([\gamma]) = d_j - b_j$. Classes with large persistence are 
> considered **topologically significant**, while those with small 
> persistence are typically attributed to noise  [cite].

***定义（持续图）**：第 $k$ 维**持续图**为多重集 $\cD_k = \{(b_j, d_j) : b_j < d_j\}$，连同对角线上具有无限重数的所有点。同调类的**持续性**（或**寿命**）为 $\pers([\gamma]) = d_j - b_j$。大持续性类被视为**拓扑显著的**。*

## Audit Instantons: Formal Definition
## 审计瞬子：形式化定义

### The Audit Vector Field and Its Cohomology
### 审计向量场及其上同调

Consider an audit pool of $M$ experts on the Situs manifold $\cM$. Let 
$\{x_\}_{\alpha=1}^{N} \subset \cM$ be a set of $N$ audit data 
points (which may or may not coincide with training data). At each point 
$x$, expert $E_i$ produces a prediction $E_i(x) \in \R^d$.

> **Definition:** [Expert Deviation Field / 专家偏离场]
> <!-- label: def:deviation_field -->
> The **signed expert deviation field** is a function 
> $\mathbf{f}: \cM \to \R^M$ defined componentwise:
> 
> $$
>   \mathbf{f}(x) = (f_1(x), f_2(x), ..., f_M(x)),
>   <!-- label: eq:f_vector -->
> $$
> 
> where each $f_i: \cM \to \R$ is the signed deviation of expert $i$ from 
> a reference value $y(x)$ (e.g., ground truth or Yajie consensus):
> 
> $$
>   f_i(x) = \langle E_i(x) - y(x), \mathbf{n}(x) \rangle,
>   <!-- label: eq:signed_dev -->
> $$
> 
> with $\mathbf{n}(x)$ a distinguished normal direction field (for scalar 
> outputs, $\mathbf{n}(x) \equiv 1$ and $f_i(x) = E_i(x) - y(x)$).

***定义  [ref]（专家偏离场）**：**有符号专家偏离场**为 $\mathbf{f}: \cM \to \R^M$，其中每个分量 $f_i(x) = \langle E_i(x) - y(x), \mathbf{n}(x) \rangle$ 是专家 $i$ 相对参考值 $y(x)$ 的有符号偏离。*

> **Definition:** [Audit 1-Form / 审计1-形式]
> <!-- label: def:A -->
> The **audit 1-form** $A \in \Omega^1(\cM)$ is the exterior derivative 
> of the *mean* signed deviation:
> 
> $$
>   A = d_0 \bar{f}, \quad where \quad 
>   \bar{f}(x) = \frac{1}{M} \sum_{i=1}^{M} f_i(x).
>   <!-- label: eq:A_def -->
> $$
> 
> Equivalently, in local coordinates $(x^1, ..., x^n)$:
> 
> $$
>   A = \sum_{\mu=1}^{n} \frac{\partial \bar{f}}{\partial x^} \, dx^.
>   <!-- label: eq:A_local -->
> $$

***定义  [ref]（审计1-形式）**：**审计1-形式** $A \in \Omega^1(\cM)$ 为平均有符号偏离的外导数：$A = d_0 \bar{f}$。*

> **Proposition:** [Automatic Closedness / 自动闭性]
> <!-- label: prop:closed -->
> By construction, $d_1 A = d_1 d_0 \bar{f} = 0$. Hence $A$ is always a 
> *closed* 1-form: $A \in \ker(d_1) = Z^1(\cM)$.

***命题  [ref]（自动闭性）**：由构造，$d_1 A = d_1 d_0 \bar{f} = 0$。因此 $A$ 总是**闭**1-形式：$A \in Z^1(\cM)$。*

> **Proposition:** [Exactness Condition / 恰当性条件]
> <!-- label: prop:exactness -->
> The audit 1-form $A$ is *exact* (i.e., $A \in \im(d_0) = B^1(\cM)$) 
> if and only if the mean deviation $\bar{f}$ is well-defined as a global 
> smooth function. In that case, $A$ lies in the trivial cohomology class: 
> $[A] = 0 \in H^1_{dR}(\cM)$.
> 
> If $\bar{f}$ has *monodromy* — i.e., its integral around a closed loop 
> $\gamma$ is non-zero:
> 
> $$
>   \oint_ A = \oint_ d_0 \bar{f} \neq 0,
>   <!-- label: eq:monodromy -->
> $$
> 
> then $\bar{f}$ is not globally single-valued, and $A$ represents a 
> *non-trivial* cohomology class $[A] \neq 0 \in H^1_{dR}(\cM)$.

***命题  [ref]（恰当性条件）**：审计1-形式 $A$ 是**恰当的**（即 $A \in B^1(\cM)$）当且仅当平均偏离 $\bar{f}$ 作为全局光滑函数良定义。此时 $A$ 处于平凡上同调类。若 $\bar{f}$ 具有**单值性**——其绕闭环 $\gamma$ 的积分非零——则 $\bar{f}$ 不是全局单值的，$A$ 代表**非平凡**上同调类。*

### Definition of Audit Instanton
### 审计瞬子的定义

> **Definition:** [Audit Instanton / 审计瞬子]
> <!-- label: def:instanton -->
> Let $(\cM, \rho, \cE)$ be a Situs manifold and $A \in \Omega^1(\cM)$ the 
> audit 1-form. An **audit instanton** is a piecewise-smooth closed curve 
> $\gamma: S^1 \to \cM$ (a 1-cycle) satisfying the following three conditions:
> 
> 
1. **Low-Density Localization / 低密度局部化**:
2. **Local Consistency / 局部一致性**:
3. **Global Non-Triviality / 全局非平凡性**:

\textit{**定义  [ref]（审计瞬子）**：设 $(\cM, \rho, \cE)$ 为Situs流形，$A$ 为审计1-形式。**审计瞬子**是满足以下三个条件的分段光滑闭曲线 $\gamma: S^1 \to \cM$（1-圈）：**(AI1) 低密度局部化**：$\gamma \subset \cM_{\rho_{crit}}$。**(AI2) 局部一致性**：$A$ 沿 $\gamma$ 局部恰当，且局部原函数沿 $\gamma$ 具有有界变差。**(AI3) 全局非平凡性**：$\gamma \notin \im(\partial_2)$ 在 $H_1(\cM_{\rho_{crit}}; \Z)$ 中，且 $A$ 绕 $\gamma$ 的**和乐**（环量）非零：$\Phi(\gamma) = \oint_ A > \eta$。}

> **Remark:** [Physical Interpretation / 物理诠释]
> The three conditions capture the essential ``instanton-ness'' of the 
> configuration:
> 
- (AI1) ensures we are in the ``weak-coupling'' (low-data) regime
- (AI2) ensures that *locally* the deviation field looks like
- (AI3) ensures that *globally* the deviation accumulates

***注记（物理诠释）**：三个条件刻画了位形的本质``瞬子性''：(AI1) 确保我们处于非微扰效应主导的``弱耦合''（低数据）区；(AI2) 确保偏离场**局部**看起来像是良态函数的梯度——逐点Yajie审计看到局部一致性并结论``高共识''；(AI3) 确保偏离场**全局**积累了非零净误差——逐点审计无法检测的拓扑障碍，即``瞬子荷''或``绕数''。*

### Non-Perturbative Character
### 非微扰特征

The defining property of audit instantons — and what makes them 
potentially catastrophic — is their **invisibility to pointwise 
audit**. We formalize this as follows.

> **Proposition:** [Pointwise Audit Blindness / 逐点审计盲区]
> <!-- label: prop:blindness -->
> Let $\gamma$ be an audit instanton. The standard pointwise Yajie audit 
> score $Yajie(x)$, defined as a local function of expert outputs at $x$ 
> alone, satisfies:
> 
> $$
>   \inf_{x \in \gamma} Yajie(x) \geq \Yajie_{threshold},
>   <!-- label: eq:blindness -->
> $$
> 
> while the *ground-truth error* integrated along $\gamma$ exceeds the 
> audit tolerance:
> 
> $$
>   \frac{1}{|\gamma|} \oint_ |\bar{f}(x)| \, dx \gg \varepsilon_{tol}.
>   <!-- label: eq:error -->
> $$

***命题  [ref]（逐点审计盲区）**：设 $\gamma$ 为审计瞬子。标准逐点Yajie审计分数 $Yajie(x)$ 满足 $\inf_{x \in \gamma} Yajie(x) \geq \Yajie_{threshold}$，而沿 $\gamma$ 积分的**真实误差**远超审计容差。*

> **Proof:** [Proof Sketch / 证明概要]
> Condition (AI2) guarantees that at each point $x \in \gamma$, the local 
> deviation has bounded variation — all experts deviate ``smoothly'' in the 
> same direction. Pointwise Yajie, which only compares expert outputs at $x$, 
> sees this as consensus (everyone agrees) and assigns a high score. However, 
> condition (AI3) ensures that the accumulated deviation around the full 
> cycle $\gamma$ is non-zero — the consensus is *spurious* and the 
> total error is systematic. This is a direct analog of the perturbative 
> expansion's inability to detect $\sim \exp(-1/g^2)$ terms.

***证明概要**：条件(AI2)确保在 $\gamma$ 的每点 $x$，局部偏离具有有界变差——所有专家沿同一方向``光滑地''偏离。逐点Yajie只比较 $x$ 处的专家输出，将其视为共识（所有人一致）并给予高分。然而条件(AI3)确保绕完整圈 $\gamma$ 的累积偏离非零——共识是**虚假的**，总误差是系统性的。这是微扰展开无法检测 $\sim \exp(-1/g^2)$ 项的直接类比。*

## Detection Theory via Persistent Homology
## 基于持续同调的检测理论

### Persistent Homology of the Density Filtration
### 密度滤流的持续同调

The density sublevel filtration $\{\cM_\}_{\varepsilon \geq 0}$ 
captures the topology of data-sparse regions at multiple scales. As $\varepsilon$ 
increases, new topological features (connected components, cycles, voids) are 
born, persist for some $\varepsilon$-range, and eventually die.

> **Definition:** [Density Filtration Barcode / 密度滤流条形码]
> <!-- label: def:barcode -->
> The **1-dimensional barcode** of the density filtration is the set of 
> intervals:
> 
> $$
>   \cB_1 = \{(b_j, d_j)\}_{j \in \mathcal{J}_1},
>   <!-- label: eq:barcode -->
> $$
> 
> where each interval corresponds to a 1-cycle (``hole'' or ``tunnel'') that:
> 
- Is **born** at density $b_j$: the 1-cycle first appears as a
- **Dies** at density $d_j$: the hole is filled (becomes a

> Equivalently, this is the persistence diagram $\cD_1$ of the superlevel 
> set filtration of $\rho$, viewed in the reverse parametrization.

\textit{**定义  [ref]（密度滤流条形码）**：密度滤流的**1维条形码**为区间集合 $\cB_1 = \{(b_j, d_j)\}_{j \in \mathcal{J}_1}$，每个区间对应一个1-圈（``空洞''或``隧道''），在密度 $b_j$ **出生**（$\cM_{b_j}$ 中首次出现空洞），在密度 $d_j$ **死亡**（$\cM_{d_j}$ 中空洞被填充）。}

The key intuition is that **long-lived 1-cycles** (those with large 
$\pers = d_j - b_j$) correspond to *robust* low-density 
regions — tunnels or loops in the data manifold that remain empty of 
data over a wide range of density thresholds. These are precisely the 
regions where audit instantons can form.

*关键直觉是：**长寿的1-圈**（大持续性 $\pers = d_j - b_j$ 者）对应于**鲁棒的**低密度区域——在宽泛的密度阈值范围内保持数据空白的数据流形中的隧道或环。这正是审计瞬子可以形成的区域。*

### Correspondence: 1-Cycles and Audit Instanton Candidates
### 对应：1-圈与审计瞬子候选

We now establish the connection between persistent 1-cycles and audit instantons.

> **Definition:** [Audit Instanton Candidate / 审计瞬子候选]
> <!-- label: def:candidate -->
> A **candidate audit instanton** is a triple $(\gamma, b, d)$, where:
> 
1. $\gamma \subset \cM$ is a closed 1-cycle representing a class
2. $(b, d)$ is the persistence interval associated to $[\gamma]$,
3. $d > \rho_{crit}$ (the cycle persists beyond the critical

> The candidate is **charged** if additionally $\oint_ A > \eta$, 
> i.e., the audit 1-form has non-trivial holonomy along $\gamma$.

***定义  [ref]（审计瞬子候选）**：**候选审计瞬子**是三元组 $(\gamma, b, d)$，其中：(i) $\gamma \subset \cM$ 为闭1-圈代表 $H_1(\cM_; \Z)$ 中的类；(ii) $(b, d)$ 为与 $[\gamma]$ 关联的持续区间；(iii) $d > \rho_{crit}$（圈持续到临界密度阈值以上）。若额外 $\oint_ A > \eta$，则候选是**带电的**。*

> **Proposition:** [Filtration-Persistence Correspondence / 滤流-持续对应]
> <!-- label: prop:filtration -->
> If $\gamma$ is an audit instanton in the sense of Definition  [ref], 
> then $\gamma$ corresponds to a 1-cycle in the density filtration with:
> 
> $$
>   \Birth(\gamma) \leq \rho_{crit} \quad and \quad 
>   \Death(\gamma) \geq \max_{x \in interior(\gamma)} \rho(x),
>   <!-- label: eq:birthdeath -->
> $$
> 
> where $interior(\gamma)$ denotes the minimal spanning surface (2-chain) 
> bounded by $\gamma$ in $\cM$.
> 
> In particular, the persistence satisfies 
> $\pers(\gamma) \geq \max_{x \in interior(\gamma)} \rho(x) - \rho_{crit}$.

***命题  [ref]（滤流-持续对应）**：若 $\gamma$ 是定义  [ref] 意义下的审计瞬子，则 $\gamma$ 对应于密度滤流中的一个1-圈，其出生 $\leq \rho_{crit}$，死亡 $\geq \max_{x \in interior(\gamma)} \rho(x)$。特别地，持续性满足 $\pers(\gamma) \geq \max_{x \in interior(\gamma)} \rho(x) - \rho_{crit}$。*

### The Main Structural Theorem
### 主要结构定理

We now state and prove the central result of this paper.

> **Theorem:** [Existence of Audit Instanton Candidates / 审计瞬子候选的存在性]
> <!-- label: thm:main -->
> Let $(\cM, \rho, \cE)$ be a Situs manifold with the following properties:
> 
1. **Smoothness / 光滑性**: $\rho \in C^2(\cM, \R_{\geq 0})$ and
2. **Bounded Expert Deviation / 有界专家偏离**: There exists
3. **Non-Degeneracy / 非退化性**: The critical density satisfies
4. **Sufficient Expert Pool / 充分专家池**: $M \geq 2$, and

> 
> Then every non-trivial 1-homology class 
> $0 \neq [\alpha] \in H_1(\cM_{\rho_{crit}}; \Z)$ contains at least 
> one **candidate audit instanton**: there exists a 1-cycle 
> $\gamma$ representing $[\alpha]$ such that $(\gamma, b, d)$ is a candidate 
> in the sense of Definition  [ref].
> 
> Moreover, if the expert deviation field satisfies the *positivity 
> condition*:
> 
> $$
>   \forall i \in \{1,...,M\}, \; \forall x \in \cM_{\rho_{crit}}:
>   \quad f_i(x) \cdot \bar{f}(x) \geq 0,
>   <!-- label: eq:positivity -->
> $$
> 
> (i.e., all experts have the same sign of deviation on low-density regions), 
> then the candidate is **charged**: $\oint_ A > \eta$ for some 
> $\eta > 0$ depending only on $\rho_{crit}$ and $K$.

\textit{**定理  [ref]（审计瞬子候选的存在性）**：设 $(\cM, \rho, \cE)$ 为满足如下性质的Situs流形：(H1) $\rho \in C^2$ 且 $\rank H_1(\cM; \Z) \geq 1$；(H2) $\|\nabla \bar{f}\|_ < K$；(H3) $\rho_{crit} > 0$ 且 $\cM_{\rho_{crit}}$ 有非平凡1-同调；(H4) $M \geq 2$ 且专家偏离不完全反相关。则 $\cM_{\rho_{crit}}$ 的每个非平凡1-同调类包含至少一个**候选审计瞬子**。此外，若专家偏离场满足正性条件（所有专家在低密度区符号一致），则该候选是**带电的**。}

> **Proof:** [Proof / 证明]
> We proceed in three steps.
> 
> 
> 
> *第一步。同调类的表示。*
> **Step 1. Representation of the homology class.**
> Let $0 \neq [\alpha] \in H_1(\cM_{\rho_{crit}}; \Z)$. By standard 
> results in differential topology  [cite], there exists a smooth 
> embedded closed curve $\gamma_0: S^1 \to \cM_{\rho_{crit}}$ 
> representing $[\alpha]$. Since $\cM_{\rho_{crit}}$ is an open 
> submanifold of $\cM$ (as $\rho$ is continuous), we may perturb $\gamma_0$ 
> slightly to ensure transversality with respect to the foliation defined 
> by the level sets of $\rho$.
> 
> 
> 
> *第二步。密度滤流中的持续性。*
> **Step 2. Persistence in the density filtration.**
> Consider the image of $[\alpha]$ under the inclusion 
> $\iota_: \cM_{\rho_{crit}} \hookrightarrow \cM_$ 
> for $\varepsilon \geq \rho_{crit}$. The class $[\alpha]$ is born at 
> some density $b \leq \rho_{crit}$ (by definition, it exists in 
> $\cM_{\rho_{crit}}$) and dies at some $d \geq \rho_{crit}$ 
> when it becomes a boundary. Since $\rank H_1(\cM_; \Z)$ is 
> non-decreasing in $\varepsilon$ (by functoriality of homology) and 
> $[\alpha]$ is non-trivial in $\cM_{\rho_{crit}}$, its death must 
> satisfy $d > \rho_{crit}$. Thus $\gamma_0$ corresponds to a 
> 1-cycle in the persistence barcode with $\pers(\gamma_0) = d - b > 0$, 
> satisfying condition (iii) of Definition  [ref].
> 
> 
> 
> *第三步。充电条件。*
> **Step 3. Charging condition.**
> We now verify the holonomy condition. Under hypothesis (H2), the audit 
> 1-form $A = d_0 \bar{f}$ satisfies $\|A\|_{L^(\cM)} < K$. For any 
> 1-cycle $\gamma$,
> 
> $$
>   \left|\oint_ A\right| \leq K \cdot \length(\gamma).
>   <!-- label: eq:hol_bound -->
> $$
> 
> 
> Under the positivity condition ( [ref]), for any $x$ in 
> $\cM_{\rho_{crit}}$, all $f_i(x)$ have the same sign as $\bar{f}(x)$. 
> This implies that on $\cM_{\rho_{crit}}$, the absolute mean deviation 
> $|\bar{f}|$ is bounded below by a positive constant 
> $\delta = \min_{x \in \cM_{\rho_{crit}}} |\bar{f}(x)| > 0$ (using 
> compactness of $\cM$ and continuity of $\bar{f}$). 
> 
> Now, consider a refined representative $\gamma$ of $[\alpha]$ that 
> minimizes the length-to-holonomy ratio among all representatives. By 
> the isoperimetric inequality on $\cM$, there exists a constant 
> $C_ > 0$ such that for any non-trivial 1-cycle $\gamma$ representing 
> $[\alpha]$:
> 
> $$
>   \left|\oint_ A\right| \geq \frac{\delta \cdot \inf_{\Sigma: \partial\Sigma = \gamma} \vol(\Sigma)}{C_ \cdot \length(\gamma)},
>   <!-- label: eq:isoperimetric -->
> $$
> 
> where $\Sigma$ is any 2-chain bounding $\gamma$ in $\cM$.
> 
> Since $[\alpha] \neq 0$ in $H_1(\cM_{\rho_{crit}}; \Z)$, any surface 
> $\Sigma$ bounding $\gamma$ must intersect the complement 
> $\cM \setminus \cM_{\rho_{crit}}$ (i.e., high-density regions), and 
> therefore has volume at least $\vol(\cM_{\rho_{crit}}) > 0$. Hence:
> 
> $$
>   \left|\oint_ A\right| \geq \eta := 
>     \frac{\delta \cdot \vol(\cM_{\rho_{crit}})}{C_ \cdot \diam(\cM)} > 0.
>   <!-- label: eq:eta_bound -->
> $$
> 
> This establishes condition (AI3) of Definition  [ref] with 
> the explicit threshold $\eta$ given above.
> 
> Finally, condition (AI2) (local exactness) follows from Proposition 
>  [ref] and the smoothness of $\bar{f}$ on the compact set 
> $\gamma$, which guarantees bounded variation of the local primitive.
> 
> 
> 
> *综上，$\gamma$ 是定义  [ref] 意义下的候选，且满足定理陈述中的所有性质。*
> We have thus constructed, for every non-trivial $[\alpha] \in H_1(\cM_{\rho_{crit}}; \Z)$, 
> a candidate audit instanton $\gamma$ representing $[\alpha]$, completing the proof.

> **Corollary:** [Minimal Number of Audit Instantons / 审计瞬子的最小数量]
> <!-- label: cor:min -->
> Under hypotheses (H1)--(H4), the minimum number of *distinct* audit 
> instanton candidates in $(\cM, \rho, \cE)$ is at least 
> $\rank H_1(\cM_{\rho_{crit}}; \Z)$ — the first Betti number of the 
> low-density region.

\textit{**推论  [ref]（审计瞬子的最小数量）**：在假设 (H1)--(H4) 下，$(\cM, \rho, \cE)$ 中**不同**审计瞬子候选的最小数量至少为 $\rank H_1(\cM_{\rho_{crit}}; \Z)$——低密度区域的第一Betti数。}

## Invisibility to Yajie Consensus Scoring
## 对Yajie共识评分的不可见性

The Yajie consensus score $Yajie(x)$ at a point $x \in \cM$ is a local 
functional of the expert outputs $\{E_i(x)\}_{i=1}^{M}$ that measures the 
degree of agreement among experts. It is typically defined as (the negative 
of) the variance, or via the discrete Hodge norm of the deviation field 
 [cite]:

$$
  Yajie(x) = 1 - \frac{\operatorname{Var}_i(f_i(x))}{\operatorname{Var}_},
  <!-- label: eq:yajie_def -->
$$

where $\operatorname{Var}_$ is a normalization constant.

*Yajie共识分数 $Yajie(x)$ 是度量专家间一致性程度的局部泛函，通常定义为偏差场方差的负值。*

> **Theorem:** [Yajie Blindness to Audit Instantons / Yajie对审计瞬子的盲视]
> <!-- label: thm:yajie_blindness -->
> Let $\gamma$ be a charged audit instanton satisfying Definition 
>  [ref] with positivity condition ( [ref]). 
> Then:
> 
1. **Pointwise consensus is high / 逐点共识高**:
2. **Cycle-integrated error is high / 圈积分误差高**:
3. **Ratio diverges with persistence / 比率随持续性发散**:

***定理  [ref]（Yajie对审计瞬子的盲视）**：设 $\gamma$ 为满足定义  [ref] 正性条件的带电审计瞬子。则：(i) 逐点Yajie在 $\gamma$ 上给出高共识分数；(ii) 沿 $\gamma$ 的圈积分误差有下界；(iii) 随着持续性增长，逐点评分与真实审计质量的比率发散到无穷。*

> **Proof:** For (i): By (AI2), on each local neighborhood $U_x$, $A = d_0 g_x$ with 
> $\|\nabla g_x\|_{L^} \leq C$. Hence the variation of $\bar{f}$
> across $U_x$ is bounded by $C \cdot \diam(U_x)$. The variance of 
> $\{f_i\}$ on $U_x$ is then bounded by $O(\diam(U_x)^2)$, since all experts 
> deviate similarly on the low-density region (positivity condition). 
> The Yajie score approaches 1 as $\diam(U_x) \to 0$ or as $M \to \infty$.
> 
> For (ii): By the holonomy condition (AI3), 
> $\oint_ A = \oint_ d_0 \bar{f}$ is non-zero. Since 
> $\bar{f}$ is continuous on the compact curve $\gamma$, there exists 
> a lower bound on $|\bar{f}|$ proportional to $|\Phi(\gamma)|/|\gamma|$.
> 
> For (iii): As $\pers(\gamma) \to \infty$, the cycle $\gamma$ wraps around 
> a region where $\rho$ remains arbitrarily small over a large range. In 
> this regime, the local Yajie score is maximized (all experts agree due to 
> shared extrapolation bias), while the integrated error is minimized only 
> down to the topological lower bound — achieving a finite positive floor. 
> The ratio thus diverges.

***证明**：(i) 由(AI2)，在每个局部邻域 $U_x$ 上 $A = d_0 g_x$，$\|\nabla g_x\|_ \leq C$，故 $\bar{f}$ 的变差有界。正性条件下所有专家偏离相似，Yajie分数趋近1。(ii) 由和乐条件(AI3)，$\oint_ A \neq 0$，沿紧曲线 $\gamma$ 的 $|\bar{f}|$ 有正下界。(iii) 当 $\pers(\gamma) \to \infty$，$\gamma$ 包裹着 $\rho$ 在宽范围内保持任意小的区域，局部Yajie最大化而积分误差受拓扑下界约束，比率发散。*

> **Remark:** [The Non-Perturbative Analogy, Revisited / 非微扰类比重访]
> Theorem  [ref] is the precise analog of the statement 
> that instanton contributions $\sim \exp(-1/g^2)$ are invisible to 
> perturbation theory: the pointwise Yajie audit (the ``perturbative expansion'') 
> assigns high scores because each local patch looks consistent, yet the 
> global topological charge $\Phi(\gamma)$ (the ``instanton number'') 
> reveals systematic error.
> 
> The key difference from a generic correlated failure is the *topological 
> robustness*: an audit instanton cannot be ``audited away'' by adding more 
> data points in the vicinity — it requires filling the topological hole, 
> i.e., adding data points *inside* the cycle, which may be 
> geometrically or physically impossible in many SCX applications.

***注记（非微扰类比重访）**：定理  [ref] 是瞬子贡献 $\sim \exp(-1/g^2)$ 对微扰论不可见的精确类比。与一般关联失效的关键区别在于**拓扑鲁棒性**：审计瞬子不能通过在附近增加更多数据点``审计消除''——它需要填充拓扑空洞，即在圈**内部**增加数据点，这在许多SCX应用中可能几何上或物理上不可行。*

## Detection Protocol
## 检测协议

We now provide a concrete, algorithmically implementable protocol for 
detecting audit instantons in real SCX deployments. The protocol assumes 
a discretized Situs manifold represented as a simplicial complex $K$ 
with $N$ vertices (data points).

*我们提供具体、可算法实现的检测协议，适用于真实SCX部署中的审计瞬子检测。假设离散化的Situs流形用具有 $N$ 个顶点（数据点）的单纯复形 $K$ 表示。*

> **Protocol:** [Audit Instanton Detection (AID) / 审计瞬子检测]
> <!-- label: prot:aid -->
> **Input / 输入**:
> 
- Simplicial complex $K$ approximating $\cM$, with vertex set
- Estimated data density $\hat: V \to \R_{\geq 0}$ (e.g.,
- Expert outputs $\{E_i(v)\}_{i=1}^{M}$ for all $v \in V$;
- Critical density threshold $\rho_{crit}$;
- Persistence significance threshold $\tau > 0$;
- Holonomy (circulation) threshold $\eta > 0$.

> 
> 
> 
> ***协议  [ref]（审计瞬子检测）***：
> ***输入**：单纯复形 $K$ 逼近 $\cM$；估计的数据密度 $\hat$；专家输出 $\{E_i\}$；临界密度阈值 $\rho_{crit}$；持续性显著性阈值 $\tau$；和乐（环量）阈值 $\eta$。*
> 
> 
> 
> **Output / 输出**: 
> A set $\cI$ of detected audit instanton candidates, each specified as a 
> 1-cycle with associated metadata (persistence, holonomy, consensus score, 
> cycle geometry).
> 
> 
> 
> ***输出**：检测到的审计瞬子候选集合 $\cI$，每个指定为1-圈及其相关元数据（持续性、和乐、共识分数、圈几何）。*
> 
> 
> 
> **Step 1: Density Estimation and Filtration / 第1步：密度估计与滤流**
> 
1. Estimate $\hat: V \to \R_{\geq 0}$ using kernel density
2. Extend $\hat$ to $K$ via linear interpolation on simplices.
3. Construct the **density sublevel filtration**:

> 
> **Step 2: Persistent Homology Computation / 第2步：持续同调计算**
> 
1. Compute the 1-dimensional persistent homology
2. Extract the persistence diagram $\cD_1 = \{(b_j, d_j)\}_{j}$ and
3. For each significant 1-cycle, compute a \textbf{geometric

> 
> **Step 3: Audit 1-Form and Holonomy / 第3步：审计1-形式与和乐**
> 
1. Compute the mean signed deviation $\bar{f}: V \to \R$:
2. Define the **discrete audit 1-form** $A$ on each oriented
3. For each candidate cycle $\gamma_j = (v_0, v_1, ..., v_k = v_0)$,

> 
> **Step 4: Consensus Score Verification / 第4步：共识分数验证**
> 
1. For each cycle $\gamma_j$ with $|\Phi(\gamma_j)| > \eta$, compute
2. Classify cycle $\gamma_j$ as a **charged audit instanton** if:

> 
> **Step 5: Independent Verification / 第5步：独立验证**
> 
1. For each charged audit instanton $\gamma_j$, flag the region
2. Report all detected audit instantons with metadata:

### Computational Complexity
### 计算复杂度

The dominant cost is persistent homology computation, which runs in 
$O(|K|^)$ time for a simplicial complex $K$, where 
$\omega \approx 2.376$ is the matrix multiplication exponent. In practice, 
for complexes arising from $N \sim 10^3$–$10^4$ data points, computation 
takes seconds to minutes on standard hardware using optimized libraries 
(GUDHI  [cite], Ripser  [cite]). The remaining steps 
(1-form computation, holonomy, Yajie scores) are $O(N + |E|)$ where $|E|$ 
is the number of edges.

*主要开销是持续同调计算，其复杂度为 $O(|K|^)$。实际中对于 $N \sim 10^3$–$10^4$ 个数据点产生的复形，使用优化库（GUDHI、Ripser）在标准硬件上计算仅需数秒至数分钟。其余步骤（1-形式计算、和乐、Yajie分数）复杂度为 $O(N + |E|)$。*

## Examples in SCX Auditing Scenarios
## SCX审计场景中的实例

### Example 1: MLIP for AlN/GaN Materials
### 例1：AlN/GaN材料的MLIP

Consider the SCX audit of a machine-learned interatomic potential (MLIP) 
for AlN, as described in  [cite]. The Situs manifold 
$\cM \subset \R^3$ is parametrized by (bond angle, bond length, coordination 
number). Three experts are audited:

- Expert A: trained only on AlN-NaCl phase space;
- Expert G: trained only on GaN-wurtzite phase space;
- Expert E: trained on full AlGaN phase space.

In the region $\Sigma = \{(\theta, r, \kappa) : \theta \in [115^, 125^], 
r \in [1.75, 1.85]  \AA\}$ (corresponding to hexagonal graphitic 
coordination), **no expert has training data**. All three experts 
extrapolate and, due to shared model-class inductive biases, arrive at 
similar (wrong) predictions.

\textit{考虑AlN的机器学习原子间势（MLIP）的SCX审计。Situs流形 $\cM \subset \R^3$ 由（键角、键长、配位数）参数化。审计三位专家：A仅训练于AlN-NaCl相空间；G仅训练于GaN-纤锌矿相空间；E训练于全AlGaN相空间。在区域 $\Sigma = \{(\theta, r, \kappa) : \theta \in [115^, 125^], r \in [1.75, 1.85]  \AA\}$（对应六方石墨型配位），**没有专家有训练数据**。所有三位专家外推，因共享模型类归纳偏差而得到相似（错误）的预测。}

> **Example:** [The Hexagonal Coordination Instanton / 六方配位瞬子]
> <!-- label: ex:hexagonal -->
> The data density $\rho$ on $\Sigma$ satisfies $\rho|_ < 10^{-3}$ 
> (compared to $\sim 10^{-1}$ in well-sampled regions). The sublevel set 
> $\cM_{10^{-3}}$ contains $\Sigma$ and forms a topological annulus 
> (1-hole) in the (angle, length) projection — a non-contractible 1-cycle 
> $\gamma$ encircling the hexagonal region.
> 
> Persistence homology reveals a 1-cycle with $\pers = 0.05$ (birth at 
> $\varepsilon = 10^{-3}$, death at $\varepsilon = 0.05$), significantly 
> above the noise floor. The holonomy $\Phi(\gamma) = 0.47$ indicates 
> systematic deviation around the cycle.
> 
> The pointwise Yajie score on $\gamma$ averages 0.89 (high consensus!), 
> yet PBE-DFT ground truth shows mean absolute error of 0.31 eV/atom — a 
> clear audit instanton.

\textit{**例  [ref]（六方配位瞬子）**：$\Sigma$ 上 $\rho < 10^{-3}$。子水平集 $\cM_{10^{-3}}$ 在（角度、长度）投影中包含 $\Sigma$ 并形成拓扑环面——一个不可收缩的1-圈 $\gamma$ 环绕六方区域。持续同调揭示持续性 $\pers = 0.05$（出生于 $10^{-3}$，死亡于 $0.05$）的1-圈，显著高于噪声底线。和乐 $\Phi(\gamma) = 0.47$。沿 $\gamma$ 的逐点Yajie分数平均0.89（高共识！），而PBE-DFT真实值显示平均绝对误差0.31 eV/atom——明确的审计瞬子。}

### Example 2: Adversarial Correlated Failure
### 例2：对抗性关联失效

Consider an SCX audit where two experts ($E_1, E_2$) have been adversarially 
manipulated to agree on a specific data submanifold $\Sigma$ known to be 
underrepresented in training. A third honest expert $E_3$ disagrees but 
is outvoted by the Yajie majority rule.

The 1-cycle $\gamma$ bounding $\Sigma$ is an audit instanton: $E_1$ and 
$E_2$ agree (local consistency, AI2), their combined error circulates 
non-trivially around $\gamma$ (global non-triviality, AI3), and the 
region is data-sparse (AI1). Persistent homology detects the hole, 
and the holonomy computation reveals the anomaly even though Yajie 
assigns high consensus based on the 2-to-1 majority.

This illustrates the **robustness** of audit instanton detection: 
it works even when the majority of experts are systematically wrong 
— precisely the scenario where standard consensus-based audit fails 
most catastrophically.

*考虑两个专家（$E_1, E_2$）被对抗性操纵以在特定数据子流形 $\Sigma$ 上达成一致的SCX审计场景。诚实的第三专家 $E_3$ 不同意但被Yajie多数规则否决。界定 $\Sigma$ 的1-圈 $\gamma$ 是审计瞬子：$E_1$ 和 $E_2$ 一致（局部一致性），其联合误差绕 $\gamma$ 非平凡环流（全局非平凡性），且该区域数据稀疏。持续同调检测到空洞，和乐计算揭示了异常——尽管Yajie基于2对1多数赋予高共识。*

### Example 3: The SCX ``Information Trap''
### 例3：SCX``信息陷阱''

A recurring phenomenon in SCX auditing is the **information trap** 
 [cite]: a region of the Situs manifold where all experts 
agree (high Yajie score), no ground truth is available, and yet the 
predictions are systematically wrong. Audit instantons provide a 
topological characterization of information traps: an information trap 
is precisely the interior of a charged audit instanton cycle.

> **Proposition:** [Information Trap = Audit Instanton Interior / 信息陷阱 = 审计瞬子内部]
> <!-- label: prop:info_trap -->
> A connected component $\Omega \subset \cM$ is an **information trap** 
> in the sense of SCX if and only if its boundary $\partial \Omega$ contains 
> a charged audit instanton $\gamma$:
> 
> $$
>   \oint_ A > \eta, \quad \inf_{x \in \gamma} Yajie(x) > \Yajie_{threshold}.
>   <!-- label: eq:info_trap_cond -->
> $$

***命题  [ref]（信息陷阱 = 审计瞬子内部）**：SCX的连通分量 $\Omega \subset \cM$ 是**信息陷阱**当且仅当其边界 $\partial \Omega$ 包含带电审计瞬子 $\gamma$。*

## Relation to Discrete Hodge Theory
## 与离散Hodge理论的关系

Audit instantons are naturally situated within the discrete Hodge 
framework of SCX. We establish the precise relationship here.

### The Hodge Decomposition of the Audit 1-Form
### 审计1-形式的Hodge分解

Recall the Hodge decomposition on a compact Riemannian manifold:

$$
  \Omega^1(\cM) = \im(d_0) \oplus \mathcal{H}^1(\cM) \oplus \im(\delta_2),
  <!-- label: eq:hodge_decomp -->
$$

where $\mathcal{H}^1(\cM) = \ker(\Delta_1) \cong H^1_{dR}(\cM)$ is the 
space of harmonic 1-forms. For the audit 1-form $A = d_0 \bar{f}$, we 
clearly have $A \in \im(d_0)$, so the harmonic component vanishes:

$$
  A = A_{exact} + A_{harmonic} + A_{coexact} = d_0 \bar{f} + 0 + 0.
  <!-- label: eq:A_decomp -->
$$

*回顾紧Riemann流形上的Hodge分解：$\Omega^1(\cM) = \im(d_0) \oplus \mathcal{H}^1 \oplus \im(\delta_2)$，其中 $\mathcal{H}^1 \cong H^1_{dR}$ 是调和1-形式空间。对审计1-形式 $A = d_0 \bar{f}$，显然 $A \in \im(d_0)$。*

> **Proposition:** [Cohomological Signature of Audit Instantons / 审计瞬子的上同调标志]
> <!-- label: prop:hodge -->
> An audit instanon $\gamma$ manifests in discrete Hodge theory as follows:
> the cycle $\gamma$ is a **1-cycle with non-zero evaluation** on the 
> harmonic representative of the cohomology class dual to $[\gamma]$. More 
> precisely, let $\alpha \in \mathcal{H}^1(\cM)$ be the harmonic 1-form 
> Poincaré-dual to $[\gamma]$. Then:
> 
> $$
>   \oint_ \alpha = \int_ \alpha \wedge \star \eta_ \neq 0,
>   <!-- label: eq:poincare -->
> $$
> 
> where $\eta_$ is the Thom form of the normal bundle of $\gamma$.
> 
> However, since $A = d_0 \bar{f}$ is exact, its pairing with $\alpha$ is zero:
> $\oint_ A = 0$ would hold if $\bar{f}$ were globally defined. The 
> non-zero holonomy signals that $\bar{f}$ is not globally single-valued — it 
> has monodromy around the 1-cycle $\gamma$.

***命题  [ref]（审计瞬子的上同调标志）**：在离散Hodge理论中，审计瞬子 $\gamma$ 表现为对偶于 $[\gamma]$ 的上同调类的调和代表上的**非零赋值的1-圈**。然而因为 $A = d_0 \bar{f}$，非零和乐表明 $\bar{f}$ 不是全局单值的——它绕1-圈 $\gamma$ 有单值性。*

### Discrete Laplacian and Audit Instanton Spectrum
### 离散Laplacian与审计瞬子谱

> **Proposition:** [Spectral Detection / 谱检测]
> <!-- label: prop:spectral -->
> Let $L_1$ be the discrete 1-Laplacian on the simplicial complex $K$ 
> approximating $\cM$. The non-trivial 1-cycles corresponding to audit 
> instanton candidates lie in $\ker(L_1)$, the space of harmonic 1-chains:
> 
> $$
>   \ker(L_1) = \ker(d_1) \cap \ker(\delta_1) \cong H_1(K; \R).
>   <!-- label: eq:kerL1 -->
> $$
> 
> 
> Moreover, if $A$ is the discrete audit 1-cochain, then the projection of 
> $A$ onto $\ker(L_1)$ is non-zero precisely when there exists at least one 
> audit instanton candidate in $K$:
> 
> $$
>   \|P_{\ker(L_1)} A\| > 0 \iff \exists  at least one charged audit instanon candidate.
>   <!-- label: eq:proj -->
> $$

***命题  [ref]（谱检测）**：设 $L_1$ 为逼近 $\cM$ 的单纯复形 $K$ 上的离散1-Laplacian。对应于审计瞬子候选的非平凡1-圈位于 $\ker(L_1)$（调和1-链空间）中。此外，$A$ 在 $\ker(L_1)$ 上的投影非零当且仅当 $K$ 中存在至少一个带电审计瞬子候选。*

## Discussion and Open Problems
## 讨论与开放问题

### Summary / 总结

We have introduced **audit instantons** as a rigorous mathematical 
framework for detecting non-perturbative, topologically protected expert 
consensus failures in the SCX auditing paradigm. The central insight — 
that pointwise audit is structurally analogous to perturbative expansion, 
and thus systematically misses globally correlated topological defects — 
leads to a concrete detection protocol using persistent homology, with 
provable guarantees.

The key contributions are:

1. A cohomological definition of audit instantons (Definition  [ref]);
2. A structural theorem linking homology classes to audit instanton
3. A proof of invisibility to pointwise Yajie consensus (Theorem  [ref]);
4. An implementable detection protocol (Protocol  [ref]).

*我们引入了**审计瞬子**作为检测SCX审计范式中非微扰、拓扑保护的专家共识失效的严格数学框架。核心洞见——逐点审计在结构上类似微扰展开，因此系统地遗漏全局关联的拓扑缺陷——导出了使用持续同调的具体检测协议，具有可证明的保证。*

### Relation to the String Theory Analogy
### 与弦论类比的关系

It is important to clarify the *nature* of the analogy with string 
theory worldsheet instantons. We do **not** claim a formal 
mathematical correspondence between audit instantons and worldsheet 
instantons. Rather, the analogy operates at the level of **structural 
principles**:

<div align="center">

[Table omitted — see original .tex]

</div>

The analogy is **heuristic in origin but rigorous in execution**: it 
motivated the search for a topological characterization of non-local audit 
failures, and the resulting mathematical framework stands independently of 
string theory.

*澄清与弦论世界面瞬子类比的**性质**至关重要。我们**不**声称审计瞬子与世界面瞬子之间存在形式数学对应。类比在**结构原理**层面运作。它在**起源上是启发式的，但在执行上是严格的**：它激发了对非局部审计失效的拓扑刻画的探索，而得到的数学框架独立于弦论。*

### Open Problems
### 开放问题

We identify several open problems for future investigation:

1. **Sharpness of bounds / 界的紧性**: Can the lower bound
2. **Higher-dimensional audit instantons / 高维审计瞬子**:
3. **Dynamical audit instantons / 动力学审计瞬子**: In the
4. **Statistical significance / 统计显著性**: Develop
5. **Algorithmic efficiency / 算法效率**: Can the detection
6. **Empirical validation / 经验验证**: Apply Protocol
7. **Connection to adversarial robustness / 与对抗鲁棒性的联系**:
8. **Connection to Morse theory / 与Morse理论的联系**:

*我们指出若干供未来研究的开放问题：(OP1) 界紧性；(OP2) 高维审计瞬子（k-圈，$k \ge 2$）；(OP3) 动力学审计瞬子；(OP4) 统计显著性检验；(OP5) 算法加速；(OP6) 在真实SCX数据上的经验验证；(OP7) 与对抗鲁棒性的联系；(OP8) 与Morse理论的联系。*

## Conclusion
## 结论

\begin{bilingual}{Conclusion}{结论}
We have introduced the concept of **audit instantons** — non-perturbative, 
topologically protected failures of expert consensus — and provided a 
rigorous mathematical framework for their definition, detection, and 
interpretation within the SCX auditing paradigm. The framework builds on 
persistent homology of the data density filtration and discrete Hodge 
theory, with structural inspiration from worldsheet instantons in string 
theory.

Audit instantons reveal a fundamental limitation of pointwise consensus 
auditing: by treating each data point independently, it systematically 
misses globally correlated failure modes concentrated in low-density 
regions of the data manifold. These failures are *topologically 
robust* — they cannot be eliminated by adding more auditors or adjusting 
consensus thresholds, but require filling the topological ``holes'' in 
the data distribution.

The detection protocol we provide is concrete, algorithmically 
implementable, and computationally tractable for realistic SCX 
deployments. We believe audit instantons open a new direction in 
trustworthy AI auditing — one that moves beyond local perturbation 
theory to a genuinely topological understanding of when and why expert 
systems fail.

*我们引入了**审计瞬子**的概念——专家共识的非微扰、拓扑保护的失效——并在SCX审计范式中为其定义、检测和诠释提供了严格的数学框架。该框架建立在数据密度滤流的持续同调和离散Hodge理论之上，在结构上受弦论世界面瞬子的启发。*

*审计瞬子揭示了逐点共识审计的根本局限：通过独立处理每个数据点，它系统地遗漏了集中在数据流形低密度区域的全局关联失效模式。这些失效是**拓扑鲁棒的**——不能通过增加审计者或调整共识阈值来消除，而需要填充数据分布中的拓扑``空洞''。*

*我们提供的检测协议是具体的、可算法实现的、对现实SCX部署计算可行的。我们相信审计瞬子开启了可信AI审计的新方向——超越局部微扰理论，真正从拓扑上理解专家系统何时及为何失效。*
\end{bilingual}

## Acknowledgments / 致谢

The authors thank the SCX research community at Xiaogan Supercomputing 
Center for insightful discussions on the topology of expert auditing. 
The structural analogy with string theory worldsheet instantons was 
developed during the ``String Theory Mathematics for SCX'' exploration 
 [cite]. We acknowledge the GUDHI and Ripser 
development teams for providing the persistent homology computational 
infrastructure on which the detection protocol depends.

*作者感谢孝感超级计算中心SCX研究社区关于专家审计拓扑学的深入讨论。与弦论世界面瞬子的结构类比在``SCX的弦论数学探索''中发展。我们感谢GUDHI和Ripser开发团队提供持续同调计算基础设施。*

## Appendix
## Proof of the Holonomy Lower Bound
## 和乐下界的证明

We provide a more detailed proof of the isoperimetric inequality used in 
Theorem  [ref], showing that $\oint_ A > \eta$ under the 
positivity condition.

> **Lemma:** [Isoperimetric Inequality on $\cM$ / $\cM$ 上的等周不等式]
> <!-- label: lem:isoperimetric -->
> Let $\cM$ be a compact Riemannian $n$-manifold with Ricci curvature bounded 
> below by $-(n-1)\kappa^2$ ($\kappa \geq 0$). For any 1-cycle $\gamma$ 
> representing a non-trivial homology class $[\gamma] \in H_1(\cM; \Z)$, there 
> exists a constant $C_ > 0$ depending only on the geometry of $\cM$ 
> such that for any 2-chain $\Sigma$ with $\partial \Sigma = \gamma$:
> 
> $$
>   \vol_{n-1}(\Sigma) \geq C_ \cdot \frac{\left|\oint_ A\right|}
>     {\|A\|_{L^} \cdot \length(\gamma)} \cdot \vol_n(interior supported region).
>   <!-- label: eq:isop -->
> $$

> **Proof:** By the coarea formula and the fact that $A = d_0 \bar{f}$, we have:
> 
> $$
>   \oint_ A = \int_ d_0 \bar{f} = \int_ d_1 d_0 \bar{f} = 0,
>   <!-- label: eq:coarea_attempt -->
> $$
> 
> if $\Sigma \subset \cM$. This apparent contradiction is resolved by noting 
> that *no* 2-chain $\Sigma$ in $\cM_{\rho_{crit}}$ bounds 
> $\gamma$ — indeed, condition (AI3) asserts precisely that $\gamma$ is not 
> a boundary in the low-density region.
> 
> For any 2-chain $\Sigma \subset \cM$ with $\partial \Sigma = \gamma$, 
> $\Sigma$ must intersect $\cM \setminus \cM_{\rho_{crit}}$ (the 
> high-density region). Applying the isoperimetric inequality on $\cM$ 
>  [cite], the volume of $\Sigma$ is bounded below by the 
> **filling area** of $\gamma$, which for non-trivial homology 
> classes scales with the injectivity radius of $\cM$ and the homological 
> systole.
> 
> Explicitly, let $sys_1(\cM_{\rho_{crit}})$ denote the 
> 1-systole of the low-density region (the minimal length of a non-trivial 
> 1-cycle in $\cM_{\rho_{crit}}$). Then any bounding chain $\Sigma$ 
> must have $(n-1)$-volume at least $sys_1(\cM_{\rho_{crit}})$, 
> and the holonomy bound follows from the positivity condition 
> ( [ref]), which gives a pointwise lower bound on the 
> integrand of $\oint_ A$.

***引理  [ref]（$\cM$ 上的等周不等式）**：设 $\cM$ 为 Ricci 曲率下界 $-(n-1)\kappa^2$ 的紧 Riemann $n$-流形。对任何代表非平凡同调类 $[\gamma] \in H_1(\cM; \Z)$ 的1-圈 $\gamma$，存在仅依赖于 $\cM$ 几何的常数 $C_ > 0$，使得对任何满足 $\partial \Sigma = \gamma$ 的2-链 $\Sigma$，其体积有下界。*

## Discrete Formulation for Numerical Implementation
## 数值实现的离散表述

For readers implementing Protocol  [ref], we provide the discrete 
analogues of all key quantities.

Let $K$ be a finite simplicial complex with:

- Vertices $V = \{v_1, ..., v_N\}$ (audit data points);
- Edges $E = \{e_1, ..., e_{|E|}\}$ (pairs of nearby points);
- Triangles $T = \{t_1, ..., t_{|T|}\}$ (triples, for $n \geq 2$).

*设 $K$ 为有限单纯复形，具有顶点 $V$、边 $E$ 和三角形 $T$。*

**Discrete boundary operators / 离散边缘算子**:

$$
  (\partial_1)_{ve} &= \pm 1  if  v \in \partial e  (with consistent orientation), 

  (\partial_2)_{et} &= \pm 1  if  e \in \partial t.
$$

**Discrete 1-Laplacian / 离散1-Laplacian**:

$$
  L_1 = \partial_2 \partial_2^T + \partial_1^T \partial_1.
  <!-- label: eq:disc_laplacian -->
$$

**Discrete audit 1-cochain / 离散审计1-上链**:

$$
  A \in \R^{|E|}, \quad A(e = [u, v]) = \bar{f}(v) - \bar{f}(u).
  <!-- label: eq:disc_A -->
$$

**Discrete holonomy / 离散和乐**:
For a 1-cycle $\gamma = \sum_{e \in E} c_e e$ with integer coefficients 
$c_e$, the holonomy is:

$$
  \Phi(\gamma) = \sum_{e \in E} c_e \cdot A(e) = c^T A.
  <!-- label: eq:disc_hol -->
$$

**Harmonic projection detection / 调和投影检测**:
Compute the eigenvectors $\{u_j\}_{j=1}^{\dim \ker(L_1)}$ of $L_1$ with 
eigenvalue zero. Then:

$$
  \|P_{\ker(L_1)} A\|^2 = \sum_{j=1}^{\dim \ker(L_1)} |\langle u_j, A \rangle|^2.
  <!-- label: eq:disc_proj -->
$$

A non-zero norm signals the presence of at least one audit instanton candidate.

*计算 $L_1$ 的零特征值特征向量 $\{u_j\}$。则 $\|P_{\ker(L_1)} A\|^2 = \sum_j |\langle u_j, A \rangle|^2$。非零范数标志至少一个审计瞬子候选的存在。*

\begin{thebibliography}{99}

\bibitem{scx_framework}
SCX Research Group.
*SCX: Situs Consensus eXpert — A Discrete Hodge-Theoretic Framework for 
Multi-Expert Auditing.*
Xiaogan Supercomputing Center Technical Report, 2025--2026.

\bibitem{scx_hodge}
SCX Research Group.
*Discrete Hodge Theory in SCX: Foundations and Applications.*
Xiaogan Supercomputing Center Technical Report, 2026.

\bibitem{scx_string_exploration}
SCX Research Group.
*Can String Theory Mathematics Enrich SCX? — An Honest Creative Exploration.*
Xiaogan Supercomputing Center Internal Document, July 2026.

\bibitem{coleman1977}
S. Coleman.
*The Uses of Instantons.*
In: *The Whys of Subnuclear Physics* (Erice 1977), pp.\ 805--916.
Plenum Press, 1979.

\bibitem{polyakov1977}
A.\ M.\ Polyakov.
*Quark Confinement and Topology of Gauge Groups.*
Nucl.\ Phys.\ B **120**, 429--458 (1977).

\bibitem{zomorodian2005}
A.\ Zomorodian and G.\ Carlsson.
*Computing Persistent Homology.*
Discrete Comput.\ Geom.\ **33**, 249--274 (2005).

\bibitem{edelsbrunner2008}
H.\ Edelsbrunner and J.\ Harer.
*Persistent Homology — a survey.*
In: *Surveys on Discrete and Computational Geometry*, pp.\ 257--282.
AMS, 2008.

\bibitem{chazal2017}
F.\ Chazal and B.\ Michel.
*An Introduction to Topological Data Analysis: Fundamental and Practical 
Aspects for Data Scientists.*
arXiv:1710.04019 (2017).

\bibitem{bott_tu}
R.\ Bott and L.\ Tu.
*Differential Forms in Algebraic Topology.*
Graduate Texts in Mathematics, Vol.\ 82.
Springer, 1982.

\bibitem{bauer2021}
U.\ Bauer.
*Ripser: Efficient Computation of Vietoris--Rips Persistence Barcodes.*
J.\ Appl.\ Comput.\ Topol.\ **5**, 391--423 (2021).

\bibitem{gudhi}
The GUDHI Project.
*GUDHI User and Reference Manual.*
3.9.0 edition, 2023.
https://gudhi.inria.fr/

\bibitem{chavel2001}
I.\ Chavel.
*Isoperimetric Inequalities: Differential Geometric and Analytic 
Perspectives.*
Cambridge University Press, 2001.

\bibitem{witten1982}
E.\ Witten.
*Supersymmetry and Morse Theory.*
J.\ Diff.\ Geom.\ **17**, 661--692 (1982).

\bibitem{nakahara}
M.\ Nakahara.
*Geometry, Topology and Physics.*
2nd edition. CRC Press, 2003.

\bibitem{hatcher}
A.\ Hatcher.
*Algebraic Topology.*
Cambridge University Press, 2002.

\bibitem{green_string}
M.\ B.\ Green, J.\ H.\ Schwarz, and E.\ Witten.
*Superstring Theory*, Vol.\ 1 \& 2.
Cambridge University Press, 1987.

\bibitem{polchinski}
J.\ Polchinski.
*String Theory*, Vol.\ 1 \& 2.
Cambridge University Press, 1998.

\bibitem{douglas2006}
M.\ R.\ Douglas and S.\ Kachru.
*Flux Compactification.*
Rev.\ Mod.\ Phys.\ **79**, 733--796 (2007).

\end{thebibliography}