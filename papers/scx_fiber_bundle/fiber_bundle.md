# 引言：从连续假象到离散本质 / Introduction: From Continuous Pretense to Discrete Reality

**Author:** SCX

*Abstract:*

{\bf 中文摘要.}
本文将 SCX (Self-Consistent eXpert) 多专家系统的规范理论建立在图上的离散霍奇（Hodge）理论之上，
完全放弃连续微分几何的纤维丛框架，转而直接处理实际计算中所用的离散数学结构。
我们将专家之间的成对位移视为有向图 $\grph = (\verts, \edgs)$ 上的边赋值 $A_e$，
将曲率定义为沿基本回路的和乐（holonomy），
将规范固定形式化为寻找顶点势 $g_v$ 以极小化残差 $\sum_{e} \|A_e - (g_w - g_v)\|^2$ 的最小二乘问题。
我们严格区分{\bf 零模固定}条件 $\sum_v g_v = 0$（消除整体平移自由度，使解唯一）与连续 Coulomb 规范 $\partial_\mu A^\mu = 0$（对联络的散度约束），
并承认本丛在拓扑上是平凡的这一事实（$G \cong \R^{Md}$ 可缩，底空间可缩，所有陈类为零）。
Cercis 分数定义为规范固定后的{\bf 残差范数}——即最优顶点势下的极小化目标函数值——直接匹配 SCX 的实际实现。
该框架是自包含的、严格正确定义的，且与 SCX 代码逐行进行着相同的计算。

{\bf English Abstract.}
This paper grounds the gauge theory of the SCX (Self-Consistent eXpert) multi-expert system
in discrete Hodge theory on graphs, abandoning the continuous fiber bundle preamble entirely
in favor of the discrete mathematical structures that the actual computation employs.
We treat pairwise expert displacements as edge assignments $A_e$ on a directed graph
$\grph = (\verts, \edgs)$, define curvature as holonomy around elementary loops,
and formalize gauge-fixing as the least-squares problem of finding vertex potentials $g_v$
that minimize the residual $\sum_{e} \|A_e - (g_w - g_v)\|^2$.
We carefully distinguish the {\bf zero-mode fixing} condition $\sum_v g_v = 0$
(which removes the overall translation degree of freedom to ensure solution uniqueness)
from the continuous Coulomb gauge $\partial_\mu A^\mu = 0$ (a divergence constraint on the connection),
and we acknowledge upfront that the bundle is topologically trivial
($G \cong \R^{Md}$ contractible, base contractible, all Chern classes vanish).
The Cercis Score is defined as the {\bf residual norm after gauge-fixing} —
the minimized objective value under the optimal vertex potentials — directly matching
the actual SCX implementation.
This framework is self-contained, rigorously defined, and performs the identical
computation as the SCX code line-by-line.

---

## 引言：从连续假象到离散本质 / Introduction: From Continuous Pretense to Discrete Reality

### 问题的核心 / The Core Problem

在多专家 SCX 框架中，我们有 $M$ 个专家，每个专家在一组 $N$ 个参数构型
$\{x^1, ..., x^N\} \subset \mathcal{X}$ 上产生预测。
专家 $m$ 在构型 $k$ 处的原始输出记作 $\tilde{x}_m^k \in \R^d$。

核心问题是：由于每个专家拥有独立的平移自由度（即可以选择自己的坐标原点），
原始坐标 $\tilde{x}_m^k$ 并非物理上有意义的量——它们依赖于每个专家私下选择的``规范''（gauge）。
两个专家 $i$ 和 $j$ 在同一构型 $k$ 上的预测差
$\delta_{ij}^k := \tilde{x}_i^k - \tilde{x}_j^k$
既反映了真实的物理差异，也包含了各自规范选择的任意性。

以下两个基本问题驱动了本文的全部分析：

1. {\bf 全局对齐问题 (Global Alignment Problem):}
2. {\bf 不一致性度量问题 (Inconsistency Quantification Problem):}

In the multi-expert SCX framework, we have $M$ experts, each producing predictions
on a set of $N$ parameter configurations $\{x^1, ..., x^N\} \subset \mathcal{X}$.
The raw output of expert $m$ at configuration $k$ is denoted $\tilde{x}_m^k \in \R^d$.

The core problem is this: since each expert possesses an independent translational
degree of freedom (the freedom to choose its own coordinate origin),
the raw coordinates $\tilde{x}_m^k$ are not physically meaningful quantities —
they depend on the ``gauge'' privately chosen by each expert.
The difference $\delta_{ij}^k := \tilde{x}_i^k - \tilde{x}_j^k$ between experts $i$
and $j$ at the same configuration $k$ reflects both genuine physical differences
and the arbitrariness of their respective gauge choices.

Two fundamental questions drive the entire analysis of this paper:

1. {\bf Global Alignment Problem:}
2. {\bf Inconsistency Quantification Problem:}

### 为什么不用连续纤维丛 / Why Not Continuous Fiber Bundles

此前的工作尝试将上述问题嵌入连续微分几何的框架——主纤维丛、Ehresmann 联络、
曲率 $2$-形式等。然而，这种嵌入存在若干根本性的困难：

1. {\bf 联络从未被构造。}
2. {\bf 曲率定义自相矛盾。}
3. {\bf 拓扑是平凡的。}
4. {\bf Coulomb 规范被错误识别。}

鉴于上述困难，本文采用一个完全不同的路径：
{\bf 在图上直接使用离散霍奇理论。}
这正是 SCX 代码实际执行的数学——我们只是将其显式地、诚实地、系统地表述出来。

Previous work attempted to embed the above problem into the framework of continuous
differential geometry — principal fiber bundles, Ehresmann connections,
curvature $2$-forms, etc. However, this embedding suffers from several fundamental
difficulties:

1. {\bf The connection was never constructed.}
2. {\bf Curvature definitions are incompatible.}
3. {\bf The topology is trivial.}
4. {\bf Coulomb gauge is misidentified.}

In light of these difficulties, this paper takes an entirely different path:
{\bf we work directly in discrete Hodge theory on graphs.}
This is the mathematics that SCX code actually performs — we are simply making it
explicit, honest, and systematic.

### 本文的路线图 / Roadmap of This Paper

- 第~2~节建立图上离散霍奇理论的基本工具：边赋值、外导数 $d_0, d_1$、
- 第~3~节构造 SCX 图：将专家对构型的比较映射为有向图上的边赋值，
- 第~4~节形式化规范固定问题：顶点势的最小二乘拟合，
- 第~5~节给出 Cercis 分数的正确定义：规范固定后的残差范数，
- 第~6~节承认拓扑平凡性，解释为何这并不削弱理论的内容。
- 第~7~节给出数值算法。
- 第~8~节总结。

- Section~2 develops the basic tools of discrete Hodge theory on graphs:
- Section~3 constructs the SCX graph: mapping expert-configuration
- Section~4 formalizes the gauge-fixing problem: least-squares fitting of
- Section~5 gives the correct definition of the Cercis Score:
- Section~6 acknowledges topological triviality and explains why this
- Section~7 provides numerical algorithms.
- Section~8 concludes.

---

## 图上的离散霍奇理论 / Discrete Hodge Theory on Graphs

本节建立一个自包含的、图上的离散霍奇理论工具箱。
所有后续构造——SCX 规范图、曲率计算、规范固定、Cercis 残差——均建立在此基础之上。
无需连续微分几何的任何知识。

### 有向图 / Directed Graphs

> **Definition:** [有向图]
> 一个{\bf 有向图} $\grph = (\verts, \edgs)$ 由以下组成：
> 
- $\verts$：有限顶点集，$|\verts| = n$；
- $\edgs \subseteq \verts \times \verts$：有向边集，$|\edgs| = m$。

> 每条有向边 $e = (u \to v)$ 表示从源顶点 $u$ 到目标顶点 $v$ 的有序对。
> 我们允许重边（多个边连接同一对顶点），但不允许自环（$u \neq v$）。

A {\bf directed graph} $\grph = (\verts, \edgs)$ consists of:

- $\verts$: a finite set of vertices, $|\verts| = n$;
- $\edgs \subseteq \verts \times \verts$: a set of directed edges, $|\edgs| = m$.

Each directed edge $e = (u \to v)$ is an ordered pair from source vertex $u$ to
target vertex $v$. We allow multiple edges between the same pair of vertices
but not self-loops ($u \neq v$).

### 离散微分形式：顶点函数与边赋值 / Discrete Differential Forms: Vertex Functions and Edge Assignments

图上的离散外微分演算将标量函数（$0$-形式）与边赋值（$1$-形式）联系起来。

> **Definition:** [顶点空间与边空间]
> 定义以下实向量空间：
> 
- {\bf $0$-形式空间} $\Omega^0(\grph)$：所有顶点函数 $f: \verts \to \R$，维数 $n$。
- {\bf $1$-形式空间} $\Omega^1(\grph)$：所有边赋值 $\alpha: \edgs \to \R$，维数 $m$。

> 对于 $d$ 维向量值情形，我们取 $d$ 个拷贝的直和：
> $\Omega^k(\grph; \R^d) := \bigoplus_{a=1}^d \Omega^k(\grph)$。

Define the following real vector spaces:

- {\bf $0$-form space} $\Omega^0(\grph)$: all vertex functions $f: \verts \to \R$,
- {\bf $1$-form space} $\Omega^1(\grph)$: all edge assignments $\alpha: \edgs \to \R$,

For $d$-dimensional vector-valued forms, we take the direct sum of $d$ copies:
$\Omega^k(\grph; \R^d) := \bigoplus_{a=1}^d \Omega^k(\grph)$.

### 离散外导数 / Discrete Exterior Derivatives

> **Definition:** [关联矩阵与 $d_0$]
> 图 $\grph$ 的{\bf 关联矩阵 (incidence matrix)} $B \in \R^{m \times n}$ 定义为：
> 对每条边 $e = (u \to v)$ 和每个顶点 $w$，
> \[
>     B_{e,w} = 
>     \begin{cases}
>         +1, & 若  w = v （目标）, 

>         -1, & 若  w = u （源）, 

>         0,  & 否则.
>     \end{cases}
> \]
> 
> {\bf 离散外导数} $d_0: \Omega^0(\grph) \to \Omega^1(\grph)$ 定义为 $d_0 := B$，
> 即对 $f \in \Omega^0(\grph)$ 和边 $e = (u \to v)$：
> \[
>     (d_0 f)_e = f_v - f_u.
> \]
> 换言之，$d_0 f$ 计算 $f$ 沿每条边的差分。

The {\bf incidence matrix} $B \in \R^{m \times n}$ of $\grph$ is defined by:
for each edge $e = (u \to v)$ and each vertex $w$,
$B_{e,w} = +1$ if $w = v$ (target), $-1$ if $w = u$ (source), $0$ otherwise.

The {\bf discrete exterior derivative} $d_0: \Omega^0(\grph) \to \Omega^1(\grph)$
is defined as $d_0 := B$, i.e., for $f \in \Omega^0(\grph)$ and edge $e = (u \to v)$:
$(d_0 f)_e = f_v - f_u$.
In words, $d_0 f$ computes the difference of $f$ along each edge.

> **Definition:** [回路的离散外导数 $d_1$]
> 设 $\mathcal{L}$ 为图 $\grph$ 的一组{\bf 基本回路 (elementary loops)}（例如，由某一生成树
> 的补边所确定的循环基）。令 $C \in \R^{|\mathcal{L}| \times m}$ 为{\bf 回路矩阵 (cycle matrix)}，
> 对每个回路 $\gamma \in \mathcal{L}$ 和每条边 $e \in \edgs$：
> \[
>     C_{\gamma,e} = 
>     \begin{cases}
>         +1, & 若边  e  沿回路  \gamma  的正方向, 

>         -1, & 若边  e  沿回路  \gamma  的负方向, 

>         0,  & 否则.
>     \end{cases}
> \]
> 
> {\bf 离散外导数} $d_1: \Omega^1(\grph) \to \Omega^2(\grph)$ 定义为 $d_1 := C$，
> 其中 $\Omega^2(\grph) \cong \R^{|\mathcal{L}|}$ 是回路空间。
> 对 $\alpha \in \Omega^1(\grph)$ 和回路 $\gamma = (e_1, e_2, ..., e_k)$：
> \[
>     (d_1 \alpha)_\gamma = \sum_{e \in \gamma} \sigma_e \, \alpha_e,
> \]
> 其中 $\sigma_e \in \{+1, -1\}$ 是边 $e$ 相对回路方向的符号。

Let $\mathcal{L}$ be a set of {\bf elementary loops} of $\grph$
(e.g., the cycle basis determined by the complement edges of a spanning tree).
Let $C \in \R^{|\mathcal{L}| \times m}$ be the {\bf cycle matrix},
where for each loop $\gamma \in \mathcal{L}$ and each edge $e \in \edgs$:
$C_{\gamma,e} = +1$ if $e$ follows $\gamma$'s positive direction,
$-1$ if opposite, $0$ otherwise.

The {\bf discrete exterior derivative} $d_1: \Omega^1(\grph) \to \Omega^2(\grph)$
is defined as $d_1 := C$, where $\Omega^2(\grph) \cong \R^{|\mathcal{L}|}$ is the loop space.
For $\alpha \in \Omega^1(\grph)$ and loop $\gamma = (e_1, e_2, ..., e_k)$:
$(d_1 \alpha)_\gamma = \sum_{e \in \gamma} \sigma_e \, \alpha_e$,
where $\sigma_e \in \{+1, -1\}$ is the sign of edge $e$ relative to the loop orientation.

> **Theorem:** [基本恒等式：$d_1 \circ d_0 = 0$]
> <!-- label: thm:d1d0 -->
> 关联矩阵与回路矩阵满足：
> \[
>     d_1 \circ d_0 = C B = 0.
> \]
> 换言之，$\im(d_0) \subseteq \ker(d_1)$。
> 这是连续情形 $\dif^2 = 0$ 的离散类比。
> 
> {\bf 证明.} 对任意 $f \in \Omega^0(\grph)$ 和任意回路 $\gamma = (v_0 \to v_1 \to ... \to v_k = v_0)$：
> \[
>     (d_1 d_0 f)_\gamma = \sum_{i=0}^{k-1} (f_{v_{i+1}} - f_{v_i}) = f_{v_k} - f_{v_0} = 0.
> \]
> 因为求和是一个伸缩和，起点与终点重合故抵消。$\square$

{\bf Theorem [ref] (Fundamental identity: $d_1 \circ d_0 = 0$).}
The incidence and cycle matrices satisfy: $d_1 \circ d_0 = C B = 0$.
Equivalently, $\im(d_0) \subseteq \ker(d_1)$.
This is the discrete analog of $\dif^2 = 0$ in the continuous setting.

{\bf Proof.} For any $f \in \Omega^0(\grph)$ and any loop
$\gamma = (v_0 \to v_1 \to ... \to v_k = v_0)$:
$(d_1 d_0 f)_\gamma = \sum_{i=0}^{k-1} (f_{v_{i+1}} - f_{v_i}) = f_{v_k} - f_{v_0} = 0$,
since the sum telescopes and $v_k = v_0$. $\square$

### 离散霍奇分解 / Discrete Hodge Decomposition

要使外导数成为真正的霍奇理论的一部分，我们需要内积和伴随算子。

> **Definition:** [内积与伴随算子]
> 在 $\Omega^0(\grph)$ 上定义标准内积（以顶点权重 $\mathbf{w}_0 \in \R^n_{>0}$）：
> \[
>     \langle f, g \rangle_0 := \sum_{v \in \verts} w_{0,v} \, f_v \, g_v.
> \]
> 在 $\Omega^1(\grph)$ 上定义内积（以边权重 $\mathbf{w}_1 \in \R^m_{>0}$）：
> \[
>     \langle \alpha, \beta \rangle_1 := \sum_{e \in \edgs} w_{1,e} \, \alpha_e \, \beta_e.
> \]
> 
> 离散外导数 $d_0$ 关于这些内积的{\bf 形式伴随 (formal adjoint)} 为
> $\dzeroT := d_0^*: \Omega^1(\grph) \to \Omega^0(\grph)$，
> 由下式确定：
> \[
>     \langle d_0 f, \alpha \rangle_1 = \langle f, \dzeroT \alpha \rangle_0,
>     \quad \forall f \in \Omega^0(\grph), \; \alpha \in \Omega^1(\grph).
> \]
> 
> 显式地，$\dzeroT = W_0^{-1} B^T W_1$，其中
> $W_0 = \diag(\mathbf{w}_0)$，$W_1 = \diag(\mathbf{w}_1)$。
> 若无权重（$W_0 = I_n$, $W_1 = I_m$），则 $\dzeroT = B^T$，
> 其对顶点 $v$ 的作用为：
> \[
>     (\dzeroT \alpha)_v = \sum_{e: 入边到  v} \alpha_e \;-\; \sum_{e: 出边自  v} \alpha_e.
> \]
> 这正好是 $v$ 处的{\bf 离散散度 (discrete divergence)}（入边减出边）。

Define the standard inner product on $\Omega^0(\grph)$ (with vertex weights
$\mathbf{w}_0 \in \R^n_{>0}$):
$\langle f, g \rangle_0 := \sum_{v \in \verts} w_{0,v} \, f_v \, g_v$.
On $\Omega^1(\grph)$ (with edge weights $\mathbf{w}_1 \in \R^m_{>0}$):
$\langle \alpha, \beta \rangle_1 := \sum_{e \in \edgs} w_{1,e} \, \alpha_e \, \beta_e$.

The {\bf formal adjoint} of $d_0$ with respect to these inner products is
$\dzeroT := d_0^*: \Omega^1(\grph) \to \Omega^0(\grph)$, determined by:
$\langle d_0 f, \alpha \rangle_1 = \langle f, \dzeroT \alpha \rangle_0$.

Explicitly, $\dzeroT = W_0^{-1} B^T W_1$, where
$W_0 = \diag(\mathbf{w}_0)$, $W_1 = \diag(\mathbf{w}_1)$.
In the unweighted case ($W_0 = I_n$, $W_1 = I_m$), $\dzeroT = B^T$, whose action
on vertex $v$ is:
$(\dzeroT \alpha)_v = \sum_{e: incoming to  v} \alpha_e \;-\; \sum_{e: outgoing from  v} \alpha_e$.
This is precisely the {\bf discrete divergence} at $v$ (incoming minus outgoing).

> **Definition:** [图拉普拉斯算子]
> {\bf 图 $0$-拉普拉斯}（组合 Laplace--Beltrami 算子）为：
> \[
>     \Lzero := \dzeroT d_0 = W_0^{-1} B^T W_1 B.
> \]
> 在无权情形下，$\Lzero = B^T B$ 即为经典的组合拉普拉斯矩阵：
> \[
>     (\Lzero)_{uv} = 
>     \begin{cases}
>         \deg(v), & u = v, 

>         -1,      & (u, v)  或  (v, u) \in \edgs, 

>         0,       & 否则.
>     \end{cases}
> \]
> 
> {\bf 图 $1$-拉普拉斯}（全 Hodge 拉普拉斯）为：
> \[
>     \Lone := d_0 \dzeroT + \doneT d_1 = B W_0^{-1} B^T W_1 + C^T W_2 C W_1^{-1},
> \]
> 其中 $W_2$ 是回路空间 $\Omega^2(\grph)$ 上的（可选）权重矩阵。
> 在无权情形下简化为 $\Lone = B B^T + C^T C$。

The {\bf graph $0$-Laplacian} (combinatorial Laplace--Beltrami operator) is:
$\Lzero := \dzeroT d_0 = W_0^{-1} B^T W_1 B$.
In the unweighted case, $\Lzero = B^T B$ is the classical combinatorial Laplacian.

The {\bf graph $1$-Laplacian} (full Hodge Laplacian) is:
$\Lone := d_0 \dzeroT + \doneT d_1 = B W_0^{-1} B^T W_1 + C^T W_2 C W_1^{-1}$,
which in the unweighted case reduces to $\Lone = B B^T + C^T C$.

> **Theorem:** [离散霍奇分解定理]
> <!-- label: thm:hodge_decomp -->
> 对于任意连通图 $\grph$，$\Omega^1(\grph)$ 有正交分解：
> \[
>     \Omega^1(\grph) = \im(d_0) \oplus \ker(\Lone) \oplus \im(\doneT),
> \]
> 其中：
> 
- $\im(d_0)$：{\bf 正合 $1$-形式}（梯度的像）——可以写为某个顶点函数的差分；
- $\ker(\Lone) = \ker(d_1) \cap \ker(\dzeroT)$：{\bf 调和 $1$-形式}——
- $\im(\doneT)$：{\bf 余正合 $1$-形式}（离散余微分的像）。

> 
> 等价地，每条边赋值 $\alpha \in \Omega^1(\grph)$ 有唯一分解：
> \[
>     \alpha = d_0 f + h + \doneT \beta,
> \]
> 其中 $f \in \Omega^0(\grph)$, $h \in \ker(\Lone)$, $\beta \in \Omega^2(\grph)$。
> 分量 $d_0 f$ 称为 $\alpha$ 的{\bf 梯度部分 (gradient part)}，
> $h$ 称为{\bf 调和部分 (harmonic part)}。

{\bf Theorem [ref] (Discrete Hodge Decomposition).}
For any connected graph $\grph$, $\Omega^1(\grph)$ admits the orthogonal decomposition:
$\Omega^1(\grph) = \im(d_0) \oplus \ker(\Lone) \oplus \im(\doneT)$, where:

- $\im(d_0)$: {\bf exact $1$-forms} (image of gradient) — expressible as differences of a vertex function;
- $\ker(\Lone) = \ker(d_1) \cap \ker(\dzeroT)$: {\bf harmonic $1$-forms} — both divergence-free and curl-free;
- $\im(\doneT)$: {\bf coexact $1$-forms} (image of discrete co-differential).

Equivalently, every edge assignment $\alpha \in \Omega^1(\grph)$ has a unique decomposition:
$\alpha = d_0 f + h + \doneT \beta$,
where $f \in \Omega^0(\grph)$, $h \in \ker(\Lone)$, $\beta \in \Omega^2(\grph)$.
The component $d_0 f$ is called the {\bf gradient part},
$h$ the {\bf harmonic part}.

> **Remark:** [关于 $1$-拉普拉斯的两部分]
> 全 Hodge $1$-拉普拉斯 $\Lone = d_0 \dzeroT + \doneT d_1$ 包含两项：
> 
- {\bf 下 (down) 部分} $d_0 \dzeroT = B B^T$（在无权情形）：出现在法方程和规范固定问题中。$\ker(d_0 \dzeroT) = \ker(\dzeroT)$。
- {\bf 上 (up) 部分} $\doneT d_1 = C^T C$：编码回路约束。$\ker(\doneT d_1) = \ker(d_1)$。

> 只有全拉普拉斯满足 $\ker(\Lone) = \ker(d_1) \cap \ker(\dzeroT)$——即调和 $1$-形式的空间。
> 下部分 $d_0 \dzeroT$ 单独使用时，其核仅为 $\ker(\dzeroT)$（余闭形式），
> 不包含 $\ker(d_1)$ 条件。SCX 的计算（法方程 $B^T B g = B^T A$）仅涉及下部分 $B^T B$，
> 但调和分解（定理 [ref]）和残差的调和分量识别需要全拉普拉斯。

{\bf Remark on the two parts of the $1$-Laplacian.}
The full Hodge $1$-Laplacian $\Lone = d_0 \dzeroT + \doneT d_1$ has two parts:
the {\bf down} part $d_0 \dzeroT = B B^T$ (unweighted), appearing in the normal equations
and gauge-fixing problem, with $\ker(d_0 \dzeroT) = \ker(\dzeroT)$;
and the {\bf up} part $\doneT d_1 = C^T C$, encoding loop constraints, with
$\ker(\doneT d_1) = \ker(d_1)$.
Only the full Laplacian satisfies $\ker(\Lone) = \ker(d_1) \cap \ker(\dzeroT)$ — the space
of harmonic $1$-forms. The down part alone has kernel $\ker(\dzeroT)$ (co-closed forms),
without the $\ker(d_1)$ condition. SCX's computation (normal equations $B^T B g = B^T A$)
uses only the down part $B^T B$, but the harmonic decomposition (Theorem [ref])
and identification of the harmonic residual component require the full Laplacian.

> **Remark:** [$1$-形式何时是正合的？]
> $\alpha \in \Omega^1(\grph)$ 是正合的（即存在 $f$ 使得 $\alpha = d_0 f$）
> 当且仅当 $\alpha$ 沿{\bf 所有}回路 $\gamma$ 的和为零：
> \[
>     \alpha = d_0 f \;\Longleftrightarrow\; d_1 \alpha = 0 \;\Longleftrightarrow\;
>     \sum_{e \in \gamma} \sigma_e \alpha_e = 0 \quad \forall \gamma \in \mathcal{L}.
> \]
> 这给出了离散版本的 Poincaré 引理：闭 $1$-形式（无边、无环量和）在一连通图上
> 是正合的{\bf 当且仅当图无环}（即图是树）。
> 若图有环，则 $\ker(d_1)$ 严格大于 $\im(d_0)$，差额正是调和 $1$-形式的空间。

$\alpha \in \Omega^1(\grph)$ is exact (i.e., exists $f$ with $\alpha = d_0 f$)
iff the sum of $\alpha$ along {\bf all} loops $\gamma$ vanishes:
$\alpha = d_0 f \Longleftrightarrow d_1 \alpha = 0 \Longleftrightarrow
\sum_{e \in \gamma} \sigma_e \alpha_e = 0$ for all $\gamma \in \mathcal{L}$.
This is the discrete Poincaré lemma: a closed $1$-form (curl-free) on a connected
graph is exact {\bf iff the graph is a tree}. If the graph has cycles,
$\ker(d_1)$ is strictly larger than $\im(d_0)$, the difference being
the space of harmonic $1$-forms.

---

## SCX 图：构造与曲率 / The SCX Graph: Construction and Curvature

### 专家比较图 / The Expert Comparison Graph

SCX 计算的原始数据是所有成对专家位移的集合。
我们将这些数据组织为有向图上的边赋值。

> **Definition:** [SCX 专家比较图]
> SCX 专家比较图 $\grph_{SCX} = (\verts, \edgs)$ 构造如下：
> 
> 
- {\bf 顶点集 $\verts$：} 每个顶点对应一对（构型，专家）：
- {\bf 边集 $\edgs$：} 包含两类边：
- {\bf 参数边 (parameter edges)：}
- {\bf 专家边 (expert edges)：}
- {\bf 总边集：} $\edgs = \edgs_{par} \cup \edgs_{exp}$。

The SCX expert comparison graph $\grph_{SCX} = (\verts, \edgs)$ is constructed as follows:

- {\bf Vertex set $\verts$:} Each vertex corresponds to a (configuration, expert) pair:
- {\bf Edge set $\edgs$:} Two types:
- {\bf Parameter edges:} $\edgs_{par} = \{(k, m) \to (k+1, m)\}$,
- {\bf Expert edges:} $\edgs_{exp} = \{(k, i) \to (k, j)\}$,
- {\bf Total edges:} $\edgs = \edgs_{par} \cup \edgs_{exp}$.

[Figure omitted — see original .tex]

### 边赋值：成对专家位移 / Edge Assignments: Pairwise Expert Displacements

> **Definition:** [SCX 边赋值 $A$]
> 定义边赋值映射 $A: \edgs \to \R^d$ 如下：
> 
- 对于参数边 $e = (k, m) \to (k+1, m)$：
- 对于专家边 $e = (k, i) \to (k, j)$：

> 
> $A \in \Omega^1(\grph_{SCX}; \R^d)$ 是 $d$ 维向量值的图 $1$-形式，
> 即图 $\grph_{SCX}$ 上每个坐标维度的边赋值。

Define the edge assignment map $A: \edgs \to \R^d$ as follows:

- For parameter edges $e = (k, m) \to (k+1, m)$:
- For expert edges $e = (k, i) \to (k, j)$:

$A \in \Omega^1(\grph_{SCX}; \R^d)$ is the $d$-dimensional vector-valued
graph $1$-form — the edge assignment in each coordinate dimension.

> **Remark:** [边赋值是直接数据，非推演所得]
> 关键点：$A$ 并非从某个连续联络 $\omega$ ``拉回''或``离散化''而得。
> $A$ {\bf 就是}原始数据——成对专家位移的集合，直接编码为图上的边赋值。
> 连续纤维丛框架在此是多余的，甚至是有害的，因为它暗示了并不存在的构造。

Crucially: $A$ is not ``pulled back'' or ``discretized'' from some continuous
connection $\omega$. $A$ {\bf is} the raw data — the collection of pairwise expert
displacements, directly encoded as edge assignments on a graph.
The continuous fiber bundle framework is superfluous here, and even harmful,
because it suggests constructions that do not exist.

### 规范变换作为顶点函数 / Gauge Transformations as Vertex Functions

> **Definition:** [顶点势（规范参数）]
> 一个{\bf 顶点势}（或{\bf 规范参数}）是函数 $g: \verts \to \R^d$，
> 为每个（构型，专家）对分配一个平移向量 $g_m^k \in \R^d$。
> 
> 物理上，$g_m^k$ 是应用于专家 $m$ 在构型 $k$ 处的规范平移：
> 对齐后的坐标为 $\hat{x}_m^k = \tilde{x}_m^k - g_m^k$。

A {\bf vertex potential} (or {\bf gauge parameter}) is a function
$g: \verts \to \R^d$, assigning to each (configuration, expert) pair a
translation vector $g_m^k \in \R^d$. Physically, $g_m^k$ is the gauge translation
applied to expert $m$ at configuration $k$:
$\hat{x}_m^k = \tilde{x}_m^k - g_m^k$.

> **Proposition:** [边赋值的规范变换]
> 在顶点势 $g$ 的规范变换下，边赋值 $A$ 按以下方式变换：
> 对每条边 $e = (u \to v)$，其中 $u = (k, i)$, $v = (\ell, j)$：
> \[
>     A'_e = A_e - (g_v - g_u) = A_e - (d_0 g)_e.
> \]
> 即 $A' = A - d_0 g$。
> 这是连续 Abel 规范变换 $A'_\mu = A_\mu - \partial_\mu \Lambda$ 的离散精确类比。
> 
> {\bf 证明.} 对齐后，专家 $i$ 在构型 $k$ 的坐标为 $\tilde{x}_i^k - g_i^k$。
> 变换后的边赋值为：
> \[
>     A'_e = (\tilde{x}_j^\ell - g_j^\ell) - (\tilde{x}_i^k - g_i^k)
>          = (\tilde{x}_j^\ell - \tilde{x}_i^k) - (g_j^\ell - g_i^k)
>          = A_e - (d_0 g)_e. \quad \square
> \]

Under a gauge transformation by vertex potential $g$, the edge assignment $A$
transforms as: for each edge $e = (u \to v)$, $A'_e = A_e - (g_v - g_u) = A_e - (d_0 g)_e$,
i.e., $A' = A - d_0 g$.
This is the discrete exact analog of the continuous abelian gauge transformation
$A'_\mu = A_\mu - \partial_\mu \Lambda$.

### 曲率：沿基本回路的和乐 / Curvature: Holonomy around Elementary Loops

> **Definition:** [SCX 基本回路]
> 图 $\grph_{SCX}$ 的{\bf 基本四边形回路}具有以下形式：
> 对每对相邻构型 $k, k+1$ 和每对不同专家 $i, j$（$i \neq j$）：
> \[
>     \gamma_{k,i,j} := (k,i) \xrightarrow{专家} (k,j)
>                     \xrightarrow{参数} (k{+}1,j)
>                     \xrightarrow{专家} (k{+}1,i)
>                     \xrightarrow{参数} (k,i).
> \]
> 注意：从 $(k{+}1,j)$ 到 $(k{+}1,i)$ 的专家边方向是反向的（$j \to i$），
> 从 $(k{+}1,i)$ 到 $(k,i)$ 的参数边方向也是反向的。

The {\bf elementary quadrilateral loops} of $\grph_{SCX}$ have the form:
for each adjacent configuration pair $k, k+1$ and each distinct expert pair $i, j$:
$\gamma_{k,i,j} := (k,i) \to (k,j) \to (k{+}1,j) \to (k{+}1,i) \to (k,i)$.

> **Definition:** [离散曲率：沿回路的和乐]
> 沿四边形回路 $\gamma_{k,i,j}$ 的{\bf 离散曲率}（{\bf 和乐}）定义为边赋值
> 沿该回路的代数和（注意边的方向）：
> \[
> 
> $$
>     \curv(\gamma_{k,i,j})
>     &:= \sum_{e \in \gamma_{k,i,j}} \sigma_e \, A_e 

>     &= A_{(k,i) \to (k,j)} + A_{(k,j) \to (k+1,j)} 

>     &\quad + A_{(k+1,j) \to (k+1,i)} + A_{(k+1,i) \to (k,i)}.
> $$
> 
> \]
> 
> 代入边赋值的定义：
> \[
> 
> $$
>     \curv(\gamma_{k,i,j})
>     &= \delta_{ij}^k \;+\; (\tilde{x}_j^{k+1} - \tilde{x}_j^k) 

>     &\quad +\; \delta_{ji}^{k+1} \;+\; (\tilde{x}_i^k - \tilde{x}_i^{k+1}) 

>     &= (\tilde{x}_i^k - \tilde{x}_j^k) + (\tilde{x}_j^{k+1} - \tilde{x}_j^k)
>        + (\tilde{x}_j^{k+1} - \tilde{x}_i^{k+1}) + (\tilde{x}_i^k - \tilde{x}_i^{k+1}).
> $$
> 
> \]
> 
> 简化后：
> \[
>     \curv(\gamma_{k,i,j}) = (\tilde{x}_i^k - \tilde{x}_i^{k+1}) - (\tilde{x}_j^k - \tilde{x}_j^{k+1}).
> \]
> 
> {\bf 几何解释：} $\curv(\gamma_{k,i,j})$ 度量了专家 $i$ 与专家 $j$ 在参数
> $k \to k+1$ 之间的预测变化量之{\bf 差}。
> 若两个专家的预测在参数变化下以完全相同的方式变化，
> 则该四边形回路的曲率为零。

The {\bf discrete curvature} ({\bf holonomy}) around the quadrilateral loop
$\gamma_{k,i,j}$ is the algebraic sum of edge assignments along the loop:
\[
    \curv(\gamma_{k,i,j})
    = \delta_{ij}^k + (\tilde{x}_j^{k+1} - \tilde{x}_j^k)
      + \delta_{ji}^{k+1} + (\tilde{x}_i^k - \tilde{x}_i^{k+1}).
\]

Simplifying:
\[
    \curv(\gamma_{k,i,j}) = (\tilde{x}_i^k - \tilde{x}_i^{k+1}) - (\tilde{x}_j^k - \tilde{x}_j^{k+1}).
\]

{\bf Geometric interpretation:} $\curv(\gamma_{k,i,j})$ measures the
{\bf difference} in how expert $i$'s and expert $j$'s predictions change
between parameters $k$ and $k+1$. If the two experts' predictions change
in exactly the same way under the parameter variation, the curvature
of this quadrilateral loop is zero.

> **Proposition:** [曲率的规范不变性]
> <!-- label: prop:curv_gauge_inv -->
> 离散曲率 $\curv(\gamma)$ 是规范不变的：
> 对任意顶点势 $g$，有 $\curv'(\gamma) = \curv(\gamma)$。
> 
> {\bf 证明.} 对任意回路 $\gamma$，
> $\curv'(\gamma) = \sum_e \sigma_e A'_e = \sum_e \sigma_e (A_e - (d_0 g)_e)
> = \curv(\gamma) - \sum_e \sigma_e (d_0 g)_e$。
> 但 $\sum_e \sigma_e (d_0 g)_e = (d_1 d_0 g)_\gamma = 0$（由定理 [ref]，$d_1 d_0 = 0$）。
> 故 $\curv'(\gamma) = \curv(\gamma)$。$\square$
> 
> 这是连续 Abel 理论中 $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ 的规范不变性
> 的离散类比。

{\bf Proposition [ref] (Gauge invariance of curvature).}
$\curv(\gamma)$ is gauge-invariant: for any vertex potential $g$,
$\curv'(\gamma) = \curv(\gamma)$.

{\bf Proof.} $\curv'(\gamma) = \sum_e \sigma_e A'_e
= \sum_e \sigma_e (A_e - (d_0 g)_e) = \curv(\gamma) - (d_1 d_0 g)_\gamma
= \curv(\gamma)$, since $d_1 d_0 = 0$ (Theorem [ref]). $\square$

> **Definition:** [曲率向量]
> 将所有基本四边形的曲率值收集为单个向量
> $\boldsymbol \in \R^{|\mathcal{L}| \times d}$（因为每个回路 $d$ 个坐标维度的曲率），
> 或简写为 $\boldsymbol \in \Omega^2(\grph_{SCX}; \R^d)$。
> 形式上，对每个坐标 $a = 1, ..., d$：
> \[
>     \boldsymbol_a = d_1 A_a = C \, \mathbf{A}_a,
> \]
> 其中 $\mathbf{A}_a \in \R^m$ 是所有边在第 $a$ 坐标上的赋值向量，
> $C$ 是回路矩阵。

Collect all elementary quadrilateral curvatures into a single vector
$\boldsymbol \in \R^{|\mathcal{L}| \times d}$,
or $\boldsymbol \in \Omega^2(\grph_{SCX}; \R^d)$.
Formally, for each coordinate $a = 1, ..., d$:
$\boldsymbol_a = d_1 A_a = C \, \mathbf{A}_a$.

### 平坦性条件 / Flatness Condition

> **Theorem:** [SCX 平坦性判别准则]
> <!-- label: thm:flatness -->
> 以下条件等价：
> 
1. 对所有基本回路 $\gamma \in \mathcal{L}$，有 $\curv(\gamma) = 0$；
2. 边赋值 $A$ 是正合的：存在顶点势 $g$ 使得 $A = d_0 g$；
3. 存在全局规范对齐：对齐后的坐标 $\hat{x}_m^k = \tilde{x}_m^k - g_m^k$

> 
> {\bf 证明.} $(i) \Leftrightarrow (ii)$ 由离散霍奇理论（$d_1 A = 0 \Rightarrow A \in \ker(d_1)$，
> 但需注意图有回路时 $\ker(d_1) = \im(d_0) \oplus \ker(\Lone)$。
> 对所有{\it 四边形}回路 $d_1 A = 0$ 保证了 $A$ 没有四边形回路分量。
> 若图仅由四边形回路生成（如 SCX 图），则这等价于 $A \in \ker(d_1)$。
> 然而，若调和分量非零，$A$ 仍可满足 $d_1 A = 0$ 但不是正合的。
> 对于 SCX 图的特定拓扑结构，我们将在下文分析此细微之处。）
> 
> $(ii) \Rightarrow (iii)$：若 $A = d_0 g$，则对专家边 $e = (k,i) \to (k,j)$：
> $A_e = g_j^k - g_i^k$。但 $A_e = \delta_{ij}^k = \tilde{x}_i^k - \tilde{x}_j^k$。
> 故 $\tilde{x}_i^k - \tilde{x}_j^k = g_j^k - g_i^k$，
> 即 $\tilde{x}_i^k - g_i^k = \tilde{x}_j^k - g_j^k$。
> 因此对齐后的坐标 $\hat{x}_i^k = \hat{x}_j^k$ 对所有 $i,j,k$ 成立。
> 
> $(iii) \Rightarrow (ii)$：反向同理。$\square$

{\bf Theorem [ref] (SCX Flatness Criterion).}
The following are equivalent:
(i) $\curv(\gamma) = 0$ for all elementary loops $\gamma \in \mathcal{L}$;
(ii) $A$ is exact: there exists a vertex potential $g$ with $A = d_0 g$;
(iii) Global gauge alignment exists: the aligned coordinates
$\hat{x}_m^k = \tilde{x}_m^k - g_m^k$ make all expert edge assignments vanish
(all experts output the same coordinates at the same configuration).

### 非平坦性与势能面不齐 / Non-Flatness and PES Misalignment

> **Theorem:** [势能面不齐的离散刻画]
> <!-- label: thm:pes_misalignment -->
> 若存在基本回路 $\gamma$ 使得 $\curv(\gamma) \neq 0$（即边赋值 $A$ 不是正合的），
> 则不存在顶点势 $g$ 能够同时使所有专家边赋值为零。
> 换言之，不存在单一全局规范选择能够完美对齐所有专家。
> 此即{\bf 势能面不齐 (PES misalignment)} 的离散表述。
> 
> 更一般地，$\curv(\gamma) \neq 0$ 意味着：
> 至少存在一对专家 $(i,j)$ 和一对相邻构型 $(k, k+1)$，
> 使得专家 $i$ 与专家 $j$ 在 $(k \to k+1)$ 之间的预测变化不一致。
> 其几何图像为：两个势能面在参数空间中以不同的方式弯曲。

{\bf Theorem [ref] (Discrete characterization of PES misalignment).}
If there exists an elementary loop $\gamma$ with $\curv(\gamma) \neq 0$
(i.e., $A$ is not exact), then no vertex potential $g$ can simultaneously
zero all expert edge assignments — no single global gauge choice can perfectly
align all experts. This is the discrete formulation of
{\bf 势能面不齐 (PES misalignment)}.

---

## 规范固定：最小二乘与零模 / Gauge-Fixing: Least Squares and the Zero-Mode

### 规范固定作为最小二乘问题 / Gauge-Fixing as a Least-Squares Problem

当曲率非零时，不存在精确满足 $A = d_0 g$ 的顶点势 $g$。
此时我们可以寻找一个``最佳近似''——极小化 $A$ 与其正合逼近 $d_0 g$
之间的 $L^2$ 距离的顶点势。此即{\bf 规范固定}的离散形式化。

> **Definition:** [最小二乘规范固定问题]
> 给定边赋值 $A \in \Omega^1(\grph_{SCX}; \R^d)$，
> 寻找顶点势 $g: \verts \to \R^d$ 极小化残差范数的平方：
> \[
>     \min_{g \in \R^{n \times d}} \; \mathcal{R}[g] := \sum_{e \in \edgs} \|A_e - (d_0 g)_e\|^2.
> \]
> 
> 其中 $\|\cdot\|$ 是 $\R^d$ 上的欧氏范数。
> 展开目标函数：
> \[
>     \mathcal{R}[g] = \sum_{a=1}^{d} \sum_{e \in \edgs} (A_{e,a} - (d_0 g_a)_e)^2
>     = \sum_{a=1}^{d} \|\mathbf{A}_a - B \mathbf{g}_a\|^2,
> \]
> 其中 $\mathbf{A}_a \in \R^m$ 是所有边在第 $a$ 维坐标上的赋值向量，
> $\mathbf{g}_a \in \R^n$ 是所有顶点上的第 $a$ 维规范参数，
> $B \in \R^{m \times n}$ 是图 $\grph_{SCX}$ 的关联矩阵。

Given edge assignment $A \in \Omega^1(\grph_{SCX}; \R^d)$,
find vertex potential $g: \verts \to \R^d$ minimizing the squared residual norm:
$\min_{g \in \R^{n \times d}} \; \mathcal{R}[g] := \sum_{e \in \edgs} \|A_e - (d_0 g)_e\|^2$.

Expanding: $\mathcal{R}[g] = \sum_{a=1}^{d} \sum_{e \in \edgs} (A_{e,a} - (d_0 g_a)_e)^2
= \sum_{a=1}^{d} \|\mathbf{A}_a - B \mathbf{g}_a\|^2$.

### 法方程与零模 / Normal Equations and the Zero-Mode

> **Proposition:** [法方程]
> <!-- label: prop:normal_eq -->
> 极小化问题 $\min_g \|\mathbf{A} - B\mathbf{g}\|^2$ 的最优性条件为法方程：
> \[
>     B^T B \, \mathbf{g} = B^T \mathbf{A}.
> \]
> 即（对每个坐标维独立）：
> \[
>     \Lzero \, \mathbf{g} = \dzeroT \mathbf{A},
> \]
> 其中 $\Lzero = B^T B$ 是图拉普拉斯矩阵（无权情形）。

The optimality condition for $\min_g \|\mathbf{A} - B\mathbf{g}\|^2$ is the
normal equation: $B^T B \, \mathbf{g} = B^T \mathbf{A}$, i.e.,
$\Lzero \, \mathbf{g} = \dzeroT \mathbf{A}$.

> **Remark:** [零模：解的非唯一性]
> 图拉普拉斯 $\Lzero = B^T B$ 总是奇异的（对于连通图，$\ker(\Lzero) = \operatorname{span}(\mathbf{1})$，
> 即全一向量）。其物理解释为：若 $g$ 是最优规范参数，则
> $g + c$（对所有专家和构型加上同一个常数平移 $c \in \R^d$）给出完全相同的残差，
> 因为 $(d_0(g + c))_e = (d_0 g)_e + (c - c) = (d_0 g)_e$。
> 
> 该非唯一性——称为{\bf 零模 (zero-mode)}——对应于所有专家共享的``整体平移''自由度。
> 并没有物理内容与之关联（所有成对位移在此变换下不变），
> 但它使得最小二乘问题没有唯一解，需要在数值上加以固定。

The graph Laplacian $\Lzero = B^T B$ is always singular (for a connected graph,
$\ker(\Lzero) = \operatorname{span}(\mathbf{1})$, the all-ones vector).
Physically: if $g$ is an optimal gauge parameter, then $g + c$
(adding the same constant translation $c \in \R^d$ to all experts and configurations)
gives the identical residual, since $(d_0(g + c))_e = (d_0 g)_e$.

This non-uniqueness — called the {\bf zero-mode} — corresponds to the
``overall translation'' degree of freedom shared by all experts.
It carries no physical content (all pairwise displacements are invariant),
but makes the least-squares problem ill-posed and must be fixed numerically.

### 零模固定：$\sum g_v = 0$（不是 Coulomb 规范！） / Zero-Mode Fixing: $\sum g_v = 0$ (Not Coulomb Gauge!)

现在我们来到一个关键的辨明点。

> **Theorem:** [$\sum_v g_v = 0$ 是零模固定，不是 Coulomb 规范]
> <!-- label: thm:zero_mode -->
> 约束
> \[
>     \sum_{v \in \verts} g_v = 0
> \]
> （或等价地 $\langle g, \mathbf{1} \rangle = 0$，即 $g \perp \mathbf{1}$）
> 的功能是{\bf 消除零模以保证解的唯一性}。它{\bf 不是}连续 Coulomb 规范
> $\partial_\mu A^\mu = 0$ 的离散类比。
> 
> {\bf 理由.} 
> 
1. {\bf 约束的对象不同。}
2. {\bf 数学类型不同。}
3. {\bf 连续类比不同。}
4. {\bf 在计算中扮演的角色不同。}

{\bf Theorem [ref] ($\sum_v g_v = 0$ is zero-mode fixing, not Coulomb gauge).}
The constraint $\sum_{v \in \verts} g_v = 0$ serves to {\bf eliminate the zero-mode
to ensure solution uniqueness}. It is {\bf not} the discrete analog of the
continuous Coulomb gauge $\partial_\mu A^\mu = 0$.

{\bf Reasons:}

1. {\bf Different object being constrained.}
2. {\bf Different mathematical type.}
3. {\bf Different continuous analog.}
4. {\bf Different role in computation.}

> **Remark:** [什么是真正的离散 Coulomb 规范？]
> 如果我们要在图上定义真正的 Coulomb 规范类比，它应当是：
> \[
>     \dzeroT A = 0 \quad 或 \quad \dzeroT (A - d_0 g) = 0,
> \]
> 即要求规范固定后的边赋值的离散散度为零。
> 这是一个完全不同的方程，涉及 $\Lone$ 而非 $\Lzero$，
> 且在 SCX 的计算中{\bf 从未被使用}。
> SCX 的解 $g$ 满足 $B^T B g = B^T A$ 加上 $\sum g = 0$，
> 但并不保证 $B^T (A - B g) = 0$（实际上后者{\it 就是}法方程本身，而非附加条件）。

A genuine discrete Coulomb gauge analog would be:
$\dzeroT A = 0$ or $\dzeroT (A - d_0 g) = 0$,
i.e., requiring the discrete divergence of the gauge-fixed edge assignment to vanish.
This is an entirely different equation, involving $\Lone$ rather than $\Lzero$,
and is {\bf never used} in the SCX computation.

### 规范固定问题的求解 / Solving the Gauge-Fixing Problem

> **Proposition:** [零模固定下的闭式解]
> <!-- label: prop:solution -->
> 加上零模固定约束 $\sum_v g_v = 0$（对每个坐标维分别施加）的最小二乘问题：
> \[
>     \min_{g: \sum_v g_{v,a} = 0} \sum_{a=1}^d \| \mathbf{A}_a - B \mathbf{g}_a \|^2
> \]
> 的解由伪逆给出：
> \[
>     \mathbf{g}_a^* = (B^T B)^+ \, B^T \mathbf{A}_a,
> \]
> 其中 $(B^T B)^+$ 是 $B^T B$ 的 Moore-Penrose 伪逆。
> 等价地，$\mathbf{g}_a^*$ 是最小范数解，满足 $\mathbf{g}_a^* \perp \mathbf{1}$
> （即自动满足 $\sum_v g_{v,a}^* = 0$）。
> 
> 数值上，可以通过求解增广系统：
> \[
>     \begin{pmatrix}
>         B^T B & \mathbf{1} 

>         \mathbf{1}^T & 0
>     \end{pmatrix}
>     \begin{pmatrix}
>         \mathbf{g}_a 
 \lambda
>     \end{pmatrix}
>     =
>     \begin{pmatrix}
>         B^T \mathbf{A}_a 
 0
>     \end{pmatrix}
> \]
> 来获得解，其中 $\lambda$ 是拉格朗日乘子。

With zero-mode fixing $\sum_v g_{v,a} = 0$, the solution is given by the
pseudo-inverse: $\mathbf{g}_a^* = (B^T B)^+ \, B^T \mathbf{A}_a$,
which is the minimum-norm solution satisfying $\mathbf{g}_a^* \perp \mathbf{1}$.

### 解的几何解释 / Geometric Interpretation of the Solution

> **Proposition:** [规范固定作为正交投影]
> <!-- label: prop:projection -->
> 最优顶点势 $g^*$ 满足：
> \[
>     d_0 g^* = proj_{\im(B)}(\mathbf{A}),
> \]
> 即 $B g^*$（$d_0 g^*$ 的向量形式）是 $\mathbf{A}$ 到 $\im(B)$（$B$ 的列空间）的
> 正交投影。
> 
> 因此，规范固定将边赋值 $A$ 分解为两部分：
> 
- {\bf 可规范消除部分：} $d_0 g^* \in \im(d_0) \subseteq \Omega^1$ ——
- {\bf 不可消除残差：} $A - d_0 g^* \perp \im(d_0)$ ——

The optimal vertex potential $g^*$ satisfies:
$d_0 g^* = proj_{\im(B)}(\mathbf{A})$,
i.e., $B g^*$ is the orthogonal projection of $\mathbf{A}$ onto $\im(B)$,
the column space of $B$.

Thus gauge-fixing decomposes the edge assignment $A$ into:

- {\bf Gauge-removable part:} $d_0 g^* \in \im(d_0) \subseteq \Omega^1$ — the component
- {\bf Ineliminable residual:} $A - d_0 g^* \perp \im(d_0)$ — the component

> **Remark:** [与霍奇分解的关系]
> 残差 $A - d_0 g^*$ 落在 $\im(d_0)^\perp$ 中。
> 由离散霍奇分解（定理 [ref]）：
> $\im(d_0)^\perp = \ker(\Lone) \oplus \im(\doneT)$。
> 即规范固定后的残差包含了{\bf 调和部分}和{\bf 余正合部分}，
> 它们共同度量了 $A$ 中``不可由梯度消除''的内容。
> 
> 特别地，$\ker(\Lone)$ 的维数等于图的圈数 (cyclomatic number) $|\mathcal{L}|$，
> 即独立基本回路的个数。调和分量精确地对应了非零环路和乐——即非零离散曲率。

The residual $A - d_0 g^*$ lies in $\im(d_0)^\perp$.
By the discrete Hodge decomposition (Theorem [ref]):
$\im(d_0)^\perp = \ker(\Lone) \oplus \im(\doneT)$.
The post-gauge-fixing residual thus contains a {\bf harmonic part} and a
{\bf coexact part}, jointly measuring the content of $A$ that is
``not removable by a gradient.''

In particular, $\dim \ker(\Lone)$ equals the cyclomatic number $|\mathcal{L}|$
of the graph — the number of independent elementary loops.
The harmonic component precisely corresponds to non-zero loop holonomies —
i.e., non-zero discrete curvature.

---

## Cercis 分数：规范固定后的残差范数 / The Cercis Score: Residual Norm after Gauge-Fixing

### 定义：残差，而非 Yang-Mills 泛函 / Definition: Residual, not Yang-Mills Functional

我们现在给出 Cercis 分数的{\bf 唯一定义}，该定义直接匹配 SCX 的实际计算。

> **Definition:** [Cercis 分数]
> <!-- label: def:cercis -->
> 令 $g^*$ 为零模固定最小二乘问题（命题 [ref]）的最优顶点势。
> 定义{\bf Cercis 分数}为规范固定后的{\bf 残差范数}：
> \[
>     \cercis := \mathcal{R}[g^*] = \sum_{e \in \edgs} \|A_e - (d_0 g^*)_e\|^2.
> \]
> 
> 展开为分量形式（每个坐标维）：
> \[
>     \cercis = \sum_{a=1}^{d} \|\mathbf{A}_a - B \mathbf{g}_a^*\|^2
>           = \sum_{a=1}^{d} \|\mathbf{A}_a - B (B^T B)^+ B^T \mathbf{A}_a\|^2.
> \]
> 
> 令 $P = B (B^T B)^+ B^T$ 为到 $\im(B)$ 的正交投影矩阵，
> $P^\perp = I - P$ 为到 $\im(B)^\perp$ 的投影。
> 则简洁地：
> \[
>     \cercis = \sum_{a=1}^{d} \|P^\perp \mathbf{A}_a\|^2
>           = \sum_{a=1}^{d} \mathbf{A}_a^T P^\perp \mathbf{A}_a.
> \]

Let $g^*$ be the optimal vertex potential from the zero-mode-fixed least-squares
problem. The {\bf Cercis Score} is the {\bf residual norm after gauge-fixing}:
\[
    \cercis := \mathcal{R}[g^*] = \sum_{e \in \edgs} \|A_e - (d_0 g^*)_e\|^2.
\]

With $P = B (B^T B)^+ B^T$ the orthogonal projector onto $\im(B)$:
$\cercis = \sum_{a=1}^{d} \|P^\perp \mathbf{A}_a\|^2
= \sum_{a=1}^{d} \mathbf{A}_a^T P^\perp \mathbf{A}_a$.

> **Remark:** [Cercis 不是 Yang-Mills 泛函]
> 本文中的 Cercis 分数 {\bf 不是} Yang-Mills 泛函 $\int \|F\|^2$。
> 它不是曲率范数的平方和，不是 $d_1 A$ 的 $L^2$ 范数。
> Cercis 是规范固定后的{\bf 残差}，即 $A$ 到 $\im(d_0)$ 的距离的平方。
> 
> 曲率 $\boldsymbol = d_1 A$ 满足 $\boldsymbol = d_1(A - d_0 g^*)$
> （因为 $d_1 d_0 = 0$），故曲率仅由残差 $A - d_0 g^*$ 决定。
> 但 Cercis 是残差的{\it 全部}范数，而不仅限于其调和分量（即曲率）。
> 具体地，若残差 $r = A - d_0 g^*$，则：
> \[
>     \cercis = \|r\|^2 = \|r_{harm}\|^2 + \|r_{coexact}\|^2,
> \]
> 而 Yang-Mills 型泛函仅捕获调和范数 $\|d_1 r\|^2 = \|d_1 r_{harm}\|^2$。
> 二者不同，且 Cercis 才是 SCX 实际使用的量。

The Cercis Score in this paper is {\bf not} the Yang-Mills functional $\int \|F\|^2$.
It is not the sum of squared curvature norms, not the $L^2$ norm of $d_1 A$.
Cercis is the {\bf residual} after gauge-fixing — the squared distance from $A$ to $\im(d_0)$.

The curvature $\boldsymbol = d_1 A$ satisfies $\boldsymbol = d_1(A - d_0 g^*)$
(since $d_1 d_0 = 0$), so curvature is determined solely by the residual
$A - d_0 g^*$. But Cercis is the {\it total} norm of the residual,
not just its harmonic component (i.e., curvature).
Specifically, if $r = A - d_0 g^*$, then:
$\cercis = \|r\|^2 = \|r_{harm}\|^2 + \|r_{coexact}\|^2$,
whereas a Yang-Mills-type functional would only capture
$\|d_1 r\|^2 = \|d_1 r_{harm}\|^2$. These are different,
and Cercis is the quantity actually used by SCX.

### 规范不变性 / Gauge Invariance

> **Theorem:** [Cercis 的规范不变性]
> <!-- label: thm:cercis_inv -->
> Cercis 分数 $\cercis$ 是规范不变的：
> 在规范变换 $A \mapsto A' = A - d_0 h$ 下（其中 $h$ 为任意顶点势），
> 有 $\cercis' = \cercis$。
> 
> {\bf 证明.} 令 $g^*$ 为原始 $A$ 的最优顶点势。
> 则在变换后的边赋值 $A' = A - d_0 h$ 下，最优点为 $g'^* = g^* - h$，
> （因为 $A' - d_0 g'^* = (A - d_0 h) - d_0(g^* - h) = A - d_0 g^*$）。
> 故残差不变：$\|A' - d_0 g'^*\|^2 = \|A - d_0 g^*\|^2$。
> 因此 $\cercis' = \cercis$。$\square$

{\bf Theorem [ref] (Gauge invariance of Cercis).}
$\cercis$ is gauge-invariant: under $A \mapsto A' = A - d_0 h$, $\cercis' = \cercis$.

{\bf Proof.} The optimal potential shifts as $g'^* = g^* - h$, leaving the
residual unchanged: $\|A' - d_0 g'^*\|^2 = \|A - d_0 g^*\|^2$. $\square$

> **Remark:** [规范不变性的直觉]
> 因为 $\cercis$ 定义为残差范数，即 $A$ 到子空间 $\im(d_0)$ 的（平方）距离，
> 而 $\im(d_0)$ 是整个规范轨道的切线空间（事实上就是轨道本身，因为群是 Abel 的），
> 所以该距离在规范变换下不变。

### Cercis 的判别性质 / Discriminative Properties of Cercis

> **Theorem:** [$\cercis = 0$ 的刻画]
> <!-- label: thm:cercis_zero -->
> 以下条件等价：
> 
1. $\cercis = 0$；
2. 边赋值 $A$ 是正合的：存在 $g$ 使得 $A = d_0 g$；
3. $A \in \im(d_0)$，即 $A$ 完全由梯度部分构成；
4. 存在完美全局对齐：所有专家在所有构型下输出一致的坐标；
5. 对所有四边形基本回路 $\gamma$，$\curv(\gamma) = 0$，且

> 
> 注意：(v) 中的第二个条件（余正合分量为零）是必须的：$d_1 A = 0$ 本身
> 仅排除调和分量，但不能保证 $A$ 是正合的（见定理 [ref]的注记）。
> 在 SCX 的实际计算中，若图具有非平凡的余正合分量，
> 即使曲率为零也可能 $\cercis > 0$。

{\bf Theorem [ref] (Characterization of $\cercis = 0$).}
The following are equivalent:
(i) $\cercis = 0$; (ii) $A$ is exact; (iii) $A \in \im(d_0)$;
(iv) perfect global alignment exists; (v) all loop curvatures vanish
{\it and} the coexact component of $A$ is zero.

### Cercis 作为一致性度量 / Cercis as a Consistency Measure

> **Corollary:** Cercis 分数提供了多专家系统规范一致性的客观度量：
> 
- $\cercis = 0$：系统是{\bf 规范一致的 (gauge-consistent)}。
- $\cercis > 0$：系统是{\bf 规范不一致的 (gauge-inconsistent)}。

> 
> Cercis 的归一化版本可定义为：
> \[
>     \bar := \frac{\|A\|^2},
> \]
> 取值范围在 $[0, 1]$ 之间，其中 $0$ 对应完美一致性，$1$ 对应完全不一致
> （即 $A$ 完全正交于 $\im(d_0)$）。

Cercis provides an objective measure of gauge consistency:

- $\cercis = 0$: {\bf gauge-consistent} — a set of gauge translations exists
- $\cercis > 0$: {\bf gauge-inconsistent} — the residual magnitude

---

## 拓扑平凡性的诚实承认 / Honest Acknowledgment of Topological Triviality

### 所有陈类均为零 / All Chern Classes Vanish

我们现在诚实地面对一个被先前工作所回避的基本事实。

> **Proposition:** [SCX 丛是拓扑平凡的]
> <!-- label: prop:trivial -->
> 从连续主丛的角度看（如果非要建立的话）：
> 
1. {\bf 结构群 $G \cong \R^{Md}$ 是可缩的。}
2. {\bf 底空间 $\mathcal{X} \subset \R^K$ 是可缩的。}
3. {\bf 分类空间是平凡的。}
4. {\bf 所有特征类为零。}

> 
> 因此，不存在任何拓扑障碍。不存在拓扑不变量。不存在非平凡丛。
> SCX 主丛（如果我们要建立的话）只是平凡的直积 $\bun \cong G \times \mathcal{X}$。

{\bf Proposition [ref] (The SCX bundle is topologically trivial).}

1. $G \cong \R^{Md}$ is contractible (a vector space);
2. $\mathcal{X}$ is contractible (typically a convex subset of $\R^K$);
3. $[\mathcal{X}, BG] = \{*\}$, so all $G$-principal bundles are trivial;
4. All characteristic classes vanish ($H^k(\mathcal{X}) = 0$ for $k > 0$).

There are no topological obstructions. No topological invariants.
No non-trivial bundles.

### 内容在几何，而非拓扑 / The Content is Geometric, Not Topological

这削弱了理论吗？不。原因如下。

> **Remark:** [真正的区分：平坦 vs.\ 非平坦联络]
> 拓扑学处理的是何时一个丛不能约化为平凡丛的问题。
> 对于 SCX，丛{\bf 总是}平凡的——这没有任何疑问。
> 
> 真正的内容是{\bf 几何}的：在给定的边赋值 $A$ 下，
> $A$ 是否落在 $\im(d_0)$ 中（即 $A$ 是否平坦 / 正合）？
> 这是一个关于 $A$ 与子空间 $\im(d_0)$ 之间关系的{\it 线性代数}问题，
> 而非拓扑问题。
> 
> 即使丛是平凡的，边赋值 $A$ 仍可具有非零的曲率分量（调和 $1$-形式）。
> 这正是 $A \notin \im(d_0)$ 的情形——即规范不一致性浮现的时刻。
> 该现象是几何的（度量了 $A$ 离 $\im(d_0)$ 有多远），
> 而非拓扑的（不涉及扭曲积或转换函数）。
> 
> 类比：在 $\R^3$（可缩，平凡的）上，矢量场 $\mathbf{v}$ 可以是无旋的
> （$\nabla \times \mathbf{v} = 0$，$\mathbf{v} = \nabla \phi$）或非无旋的。
> 这并非拓扑陈述——$\R^3$ 的拓扑未曾改变过。
> 同理，SCX 的规范一致性问题涉及 $A$ 在给定（平凡）图上的分解，
> 而非丛的非平凡性。

{\bf The true distinction: flat vs.\ non-flat connections.}
Topology asks: when can a bundle not be reduced to the trivial bundle?
For SCX, the bundle is {\bf always} trivial — this is uncontroversial.

The real content is {\bf geometric}: given an edge assignment $A$,
does $A$ lie in $\im(d_0)$ (is $A$ flat / exact)?
This is a {\it linear algebra} question about the relationship between $A$
and the subspace $\im(d_0)$, not a topological question.

Even though the graph (bundle) is trivial, $A$ can still have non-zero
curvature components (harmonic $1$-forms). This is the case when
$A \notin \im(d_0)$ — the moment gauge inconsistency appears.
The phenomenon is geometric (measuring how far $A$ is from $\im(d_0)$),
not topological (involving twisted products or transition functions).

Analogy: on $\R^3$ (contractible, trivial), a vector field $\mathbf{v}$
may be curl-free ($\nabla \times \mathbf{v} = 0$, $\mathbf{v} = \nabla \phi$)
or not. This is not a topological statement — the topology of $\R^3$ never changes.
Similarly, SCX's gauge consistency problem concerns the decomposition of $A$
on the given (trivial) graph, not the non-triviality of a bundle.

### 图视角下的拓扑内容 / Topological Content in the Graph Perspective

在图的视角下，唯一的``拓扑''内容是图本身的 Betti 数。

> **Proposition:** [图同调]
> 图 $\grph_{SCX}$ 的（实系数）同调群为：
> 
- $H_0(\grph) \cong \R^c$，其中 $c$ 是连通分支数（通常为 $1$）；
- $H_1(\grph) \cong \R^{|\mathcal{L}|}$，其中 $|\mathcal{L}|$ 是基本回路数
- $H_k(\grph) = 0$ 对所有 $k \geq 2$。

> 
> $H_1(\grph) \cong \ker(\Lone)$ 是调和 $1$-形式的空间。
> $H_1$ 的非零维数表示图中有 $|\mathcal{L}|$ 个独立回路，
> 每个回路承载着非平凡和乐的可能性。
> 但这不是丛的拓扑——这只是图的圈结构。

The (real) homology of $\grph_{SCX}$ is:
$H_0(\grph) \cong \R^c$ ($c$ = number of connected components),
$H_1(\grph) \cong \R^{|\mathcal{L}|}$ (cyclomatic number),
$H_k(\grph) = 0$ for $k \geq 2$.

$H_1(\grph) \cong \ker(\Lone)$ is the space of harmonic $1$-forms.
A non-zero $H_1$ means the graph has $|\mathcal{L}|$ independent loops,
each capable of carrying non-trivial holonomy.
But this is not bundle topology — it is merely the cycle structure of the graph.

---

## 数值算法 / Numerical Algorithm

### 数据结构与算法概览 / Data Structures and Algorithm Overview

SCX 规范的完整数值流程由以下步骤组成。
每一步均直接对应前文所述的数学结构。

\begin{algorithm}[H]
*Caption:* SCX 规范固定与 Cercis 计算
<!-- label: alg:scx -->

1. {\bf 输入：} $M$ 个专家在 $N$ 个构型上的原始预测
2. {\bf 构造图 $\grph_{SCX}$：}
3. {\bf 构建关联矩阵 $B \in \R^{m \times n}$：}
4. {\bf 组装边赋值向量 $\mathbf{A}_a \in \R^m$：}（对每个坐标维 $a = 1,...,d$）
5. {\bf 计算图拉普拉斯与右端项：}
6. {\bf 解带零模固定的法方程：}
7. {\bf 计算残差与 Cercis 分数：}
8. {\bf 输出对齐后的预测（可选）：}

\end{algorithm}

### 与原始 MILP 的关系 / Relation to the Original MILP

原始 SCX 的实现使用了 MILP（混合整数线性规划）进行规范固定。
本文的最小二乘公式等价于 MILP 的{\it 连续松弛}：当所有整数约束被移除后，
MILP 即约化为求解法方程 $B^T B g = B^T A$ 带约束 $\sum g = 0$。

若需要整数约束（例如，$g_m^k$ 限制在整数格点上），
可以在最小二乘解的基础上进行舍入或分支定界。
然而，对于大多数应用场景，连续最小二乘解已提供足够精度的规范固定。

The original SCX implementation uses MILP (Mixed-Integer Linear Programming)
for gauge-fixing. The least-squares formulation here is equivalent to the
{\it continuous relaxation} of MILP: when all integer constraints are removed,
MILP reduces to solving $B^T B g = B^T A$ with constraint $\sum g = 0$.

### 计算复杂度 / Computational Complexity

> **Proposition:** [复杂度分析]
> 
- 图构造：$O(N M^2)$（每条专家边需计算一个成对位移）；
- 拉普拉斯组装：$O(m) = O(N M^2)$（非零元插入）；
- 法方程求解：$O(n^{3/2})$ 至 $O(n^2)$ 取决于求解器
- Cercis 计算：$O(m d) = O(N M^2 d)$。

> 
> 对于典型的参数设置（$M \sim 10^1$--$10^2$，$N \sim 10^2$--$10^3$，$d \leq 3$），
> 全部流程可在现代硬件上于数秒至数分钟内完成。

- Graph construction: $O(N M^2)$;
- Laplacian assembly: $O(m) = O(N M^2)$;
- Normal equation solve: $O(n^{3/2})$ to $O(n^2)$ depending on solver;
- Cercis computation: $O(m d) = O(N M^2 d)$.

---

## 与先前工作的关系 / Relationship to Prior Work

本节明确本文的表述与先前连续纤维丛表述之间的关系，
并诚实地指出后者的错误。

### 对应关系 / Correspondences

<div align="center">

[Table omitted — see original .tex]

</div>

### 先前表述中的错误 / Errors in Prior Formulation

1. {\bf F1: $\sum g_m = 0$ 不是 Coulomb 规范。}
2. {\bf F2: 联络 $\omega$ 从未被构造。}
3. {\bf F3: Cercis 定义不一致。}
4. {\bf F4: 拓扑被误述。}

---

## 离散霍奇与连续微分几何的比较 / Discrete Hodge vs.\ Continuous Differential Geometry
<!-- label: sec:comparison -->

本节对离散图霍奇方法与连续微分几何（纤维丛）方法进行系统性比较，
阐明各自的能力边界，并解释为何离散方法是 SCX 的正确选择。

### 两种形式化 / Two Formalisms

<div align="center">

[Table omitted — see original .tex]

</div>

### 连续微分几何能做什么 / What Continuous Differential Geometry Can Do

连续微分几何（纤维丛、联络、曲率）在以下方面是强大的：

1. {\bf 全局拓扑分类。}
2. {\bf 分析工具。}
3. {\bf 局部到全局的整合。}
4. {\bf 成熟的理论生态。}

### 连续微分几何不能做什么 / What Continuous Differential Geometry Cannot Do

然而，对于 SCX 的具体问题，连续微分几何有以下根本性局限：

1. {\bf 无法从离散数据构造联络。}
2. {\bf 所有拓扑不变量恒为零。}
3. {\bf 连续形式化与计算无关。}
4. {\bf 术语混淆。}

### 为何离散方法是正确的选择 / Why Discrete is the Right Choice

离散图霍奇方法的优势源于以下原则：

1. {\bf 本体论诚实 (Ontological Honesty)。}
2. {\bf 计算对应 (Computational Correspondence)。}
3. {\bf 数学自足 (Mathematical Self-Sufficiency)。}
4. {\bf 可证伪性 (Falsifiability)。}
5. {\bf 自然的推广路径 (Natural Generalization Path)。}

### 连续形式化若要成为有效需要什么条件 / What the Continuous Formalism Would Need to Become Valid

如果未来的工作坚持使用连续微分几何框架，至少需要完成以下步骤：

1. {\bf C1：从离散数据显式构造联络。}
2. {\bf C2：证明离散化的一致性。}
3. {\bf C3：建立非平凡拓扑。}
4. {\bf C4：将 Cercis 与 Yang-Mills 泛函精确关联。}
5. {\bf C5：正确定义 Coulomb 规范类比。}

{\bf 总结.}
离散图霍奇理论与连续纤维丛理论并非竞争关系——它们是不同层次的形式化，
适用于不同的问题。
对于 SCX，数据天然是离散的，计算天然是离散的，
因此离散形式化是{\bf 唯一与计算一致}的形式化。
连续框架只有在完成上述 C1--C5 步骤后才可能被视为有效的替代方案。
在此之前，离散霍奇理论应被视为 SCX 规范理论的{\bf 权威表述}。

---

## 推广与展望 / Generalizations and Outlook

### 加权图与更一般的度量 / Weighted Graphs and More General Metrics

本文中我们使用了无权图（所有边权重相等）。
更一般地，可以为边赋予权重以反映对某些专家或构型比较的置信度：
\[
    \mathcal{R}_W[g] := \sum_{e \in \edgs} w_e \, \|A_e - (d_0 g)_e\|^2.
\]
加权拉普拉斯 $L_W = B^T W B$ 替换无权版本，所有理论结果保持不变。

加权版本允许将 Cercis 调整为对重要专家对或关键构型区域更敏感。

We used unweighted graphs. More generally, edge weights $w_e$ reflecting
confidence in certain expert/config comparisons yield:
$\mathcal{R}_W[g] := \sum_{e \in \edgs} w_e \, \|A_e - (d_0 g)_e\|^2$,
with $L_W = B^T W B$. All theory carries through.

### 非 Abel 专家对称性 / Non-Abelian Expert Symmetries

若专家的规范群扩展为包含旋转和缩放的群（如 $\mathrm{SE}(d)$），
图的边赋值变为群值而非向量值。此时：

- 规范变换 $g$ 是群值顶点函数；
- 边赋值变换为 $A'_e = g_v \circ A_e \circ g_u^{-1}$；
- 规范固定变为群值最小二乘问题，
- 曲率仍可定义为回路上的群乘积。

本文的图论框架为这些推广提供了自然的基础。

If the gauge group extends to rotations and scaling (e.g., $\mathrm{SE}(d)$):
edge assignments become group-valued; gauge-fixing becomes a group-valued
least-squares problem on homogeneous spaces. The graph-theoretic framework
provides a natural foundation for such extensions.

### 与持续同调的联系 / Connection to Persistent Homology

Cercis 分数可以解释为持续同调（persistent homology）中的一种持续性度量：

- 非零离散曲率回路对应 $1$-维条形码中的``洞''；
- Cercis 的调和分量 $\|r_{harm}\|^2$ 可视为
- 规范固定等价于寻找最优上边缘以``填补''这些 $1$-维空洞。

Cercis can be interpreted through persistent homology:
non-zero curvature loops correspond to $H_1$ ``holes'';
the harmonic component of Cercis is a persistence-weighted sum of $H_1$ classes;
gauge-fixing is the search for optimal coboundaries to ``fill'' these holes.

### 无穷维极限 / Infinite-Dimensional Limit

当 $M \to \infty$ 且 $N \to \infty$ 时，图 $\grph_{SCX}$ 趋于一个
乘积空间 $[0,1] \times [0,1]$ 上的连续网格。此时的极限偏微分方程
涉及两个方向的导数（参数方向和专家方向），与二维规范场论有自然联系。
严格分析这一极限仍在进行中。

As $M, N \to \infty$, the SCX graph tends to a continuous grid on $[0,1] \times [0,1]$.
The limiting PDE involves derivatives in both parameter and expert directions,
with natural connections to 2D gauge theories. Rigorous analysis is ongoing.

---

## 结论 / Conclusion

### 主要结果 / Main Results

本文在图上建立了 SCX 多专家系统规范理论的完整离散形式化。主要贡献如下：

1. {\bf 图霍奇框架：}
2. {\bf 曲率作为回路和乐：}
3. {\bf 规范固定的最小二乘形式化：}
4. {\bf 零模固定 $\neq$ Coulomb 规范：}
5. {\bf Cercis 分数的唯一定义：}
6. {\bf 拓扑平凡性的诚实承认：}

This paper establishes a complete discrete formalization of SCX gauge theory
on graphs. Main contributions:

1. {\bf Graph Hodge framework:} SCX mathematics is discrete Hodge theory
2. {\bf Curvature as loop holonomy:} Discrete curvature is defined as the
3. {\bf Gauge-fixing as least squares:} Gauge-fixing is rigorously formalized
4. {\bf Zero-mode fixing $\neq$ Coulomb gauge:} Strictly distinguishes
5. {\bf Unique Cercis definition:} Cercis Score = residual norm $\|P^\perp A\|^2$
6. {\bf Honest topological triviality:} Acknowledges contractible $G$ and

### 最终评注 / Final Remark

SCX 框架的数学核心是优雅而简洁的：它只是图上的离散霍奇分解。
给定一组成对专家位移（边赋值 $A$），问题归结为判断 $A$ 与梯度子空间
$\im(d_0)$ 之间的距离。
规范一致性意味着该距离为零（$A$ 是正合的）；不一致性意味着距离为正，
Cercis 分数精确地量化了这一距离。

连续微分几何的引入——纤维丛、联络、曲率形式——对此问题而言是多余的，
甚至是有害的，因为它引入的术语（Coulomb 规范、Yang-Mills 作用量、Chern 类）
与实际的离散计算并不对应。

我们主张：清晰、诚实、且数学上确切的离散表述，
总是比不准确的、与计算无关联的连续类比更为可取得多。

The mathematical core of SCX is elegant and simple: it is just discrete Hodge
decomposition on a graph. Given a set of pairwise expert displacements (edge
assignment $A$), the problem reduces to determining the distance between $A$
and the gradient subspace $\im(d_0)$. Gauge consistency means this distance is
zero ($A$ is exact); inconsistency means it is positive, and Cercis precisely
quantifies that distance.

The introduction of continuous differential geometry — fiber bundles,
connections, curvature forms — is superfluous for this problem and even harmful,
because it introduces terminology (Coulomb gauge, Yang-Mills action, Chern classes)
that does not correspond to the actual discrete computation.

We advocate: a clear, honest, and mathematically precise discrete formulation
is always preferable to an inaccurate continuous analogy disconnected from
the computation.

\begin{thebibliography}{99}

\bibitem{lim2020}
L.-H.~Lim.
``Hodge Laplacians on Graphs.''
*SIAM Review*, 62(3):685--715, 2020.

\bibitem{jiang2011}
X.~Jiang, L.-H.~Lim, Y.~Yao, and Y.~Ye.
``Statistical ranking and combinatorial Hodge theory.''
*Mathematical Programming*, 127(1):203--244, 2011.

\bibitem{chung1997}
F.~R.~K.~Chung.
*Spectral Graph Theory*.
American Mathematical Society, 1997.

\bibitem{grady2011}
L.~J.~Grady and J.~R.~Polimeni.
*Discrete Calculus: Applied Analysis on Graphs for Computational Science*.
Springer, 2011.

\bibitem{desbrun2005}
M.~Desbrun, A.~N.~Hirani, M.~Leok, and J.~E.~Marsden.
``Discrete Exterior Calculus.''
*arXiv:math/0508341*, 2005.

\bibitem{hirani2003}
A.~N.~Hirani.
*Discrete Exterior Calculus*.
PhD thesis, California Institute of Technology, 2003.

\bibitem{crane2013}
K.~Crane, F.~de Goes, M.~Desbrun, and P.~Schröder.
``Digital Geometry Processing with Discrete Exterior Calculus.''
*ACM SIGGRAPH 2013 Courses*, 2013.

\bibitem{kobayashi1963}
S.~Kobayashi and K.~Nomizu.
*Foundations of Differential Geometry, Vol.~I*.
Wiley-Interscience, 1963.

\bibitem{nakahara2003}
M.~Nakahara.
*Geometry, Topology and Physics*, 2nd ed.
Taylor \& Francis, 2003.

\bibitem{bott1982}
R.~Bott and L.~Tu.
*Differential Forms in Algebraic Topology*.
Springer, 1982.

\bibitem{hatcher2002}
A.~Hatcher.
*Algebraic Topology*.
Cambridge University Press, 2002.

\bibitem{bleecker1981}
D.~Bleecker.
*Gauge Theory and Variational Principles*.
Addison-Wesley, 1981.

\bibitem{husemoller1966}
D.~Husemoller.
*Fibre Bundles*.
McGraw-Hill, 1966 (3rd ed., Springer, 1994).

\bibitem{gao2019}
T.~Gao, J.~Brockschmidt, and N.~Kohli.
``Hodge and Laplacian: From Graphs to Manifolds.''
*ICLR Workshop on Representation Learning on Graphs and Manifolds*, 2019.

\bibitem{schaub2020}
M.~T.~Schaub, A.~R.~Benson, P.~Horn, G.~Lippner, and A.~Jadbabaie.
``Random Walks on Simplicial Complexes and the normalized Hodge 1-Laplacian.''
*SIAM Review*, 62(2):353--391, 2020.

\end{thebibliography}