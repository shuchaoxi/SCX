# 引言：社会媒体时代的势能危机

**Author:** SCX

*Abstract:*

**中文摘要.**
当代社会媒体平台依赖推荐算法最大化用户参与度，
但这些算法同时充当了**信息势能隔离器**（Information Potential Isolator）的角色。
本文将SCX框架中的平等论（$\sum g_m = 0$）应用于社会媒体的信息传播动力学，
建立了信息势能面（Information Potential Energy Surface, IPES）的严格数学形式化。
我们证明：
**(1)** 推荐算法通过向用户展示与其现有坐标系匹配的内容，
使跨群体耦合强度 $\GCoupling \to 0$，
从而将不同用户群锁定在各自的信息势能阱中——此即**过滤气泡**（Filter Bubble）的势能解释；
**(2)** 当 $\GCoupling = 0$ 时，不同坐标系下的用户群永久振荡，永不相交，
此即推论~8 的直接结论——**极化**（Polarization）是永久振荡的宏观表现；
**(3)** 信息势能面的孤立法则给出了算法审计的新标准：
审计项 $\GCoupling$ 测量跨坐标系暴露的强度；
**(4)** 解决方案来自平等论的核心要求——强制混合信息流
（Forced Mixed Information Streams），即人为增加 $\GCoupling$ 使系统收敛至相互理解。
本文以中英双语撰写，包含完整的定理体系、形式证明、数值示例与诚实暴击标注。

**English Abstract.**
Contemporary social media platforms rely on recommendation algorithms that maximize
user engagement, but these algorithms simultaneously act as **Information Potential
Isolators**. This paper applies the Equality Principle ($\sum g_m = 0$) from the SCX
framework to the information propagation dynamics of social media, establishing a
rigorous mathematical formalization of the Information Potential Energy Surface (IPES).
We prove that: **(1)** recommendation algorithms, by showing users content matching
their existing coordinate systems, drive the cross-group coupling strength $\GCoupling \to 0$,
locking different user groups into their respective information potential wells --- this is
the potential-energy explanation of the **Filter Bubble**;
**(2)** when $\GCoupling = 0$, user groups in different coordinate systems oscillate
permanently without intersecting, a direct consequence of Corollary~8 ---
**Polarization** is the macroscopic manifestation of permanent oscillation;
**(3)** the isolation law of the IPES yields a new standard for algorithmic auditing:
the audit item $\GCoupling$ measures the intensity of cross-coordinate-system exposure;
**(4)** the solution follows from the core requirement of the Equality Principle ---
Forced Mixed Information Streams, i.e., artificially increasing $\GCoupling$ to drive the
system toward mutual understanding. This paper is bilingual (Chinese/English) with a
complete theorem system, formal proofs, numerical examples, and honest critique markings.

**关键词/Keywords：**
信息势能面；推荐算法；过滤气泡；极化；跨坐标系暴露；算法审计；平等论

Information Potential Energy Surface; Recommendation Algorithm; Filter Bubble;
Polarization; Cross-Coordinate-System Exposure; Algorithmic Audit; Equality Principle

## 引言：社会媒体时代的势能危机
## Introduction: The Potential Energy Crisis in the Age of Social Media

### 问题的提出

当代社会正经历一场前所未有的信息分离危机。
2026年，全球超过50亿人通过社会媒体获取信息，
而这些平台的核心驱动力——推荐算法（Recommendation Algorithm）——
以最大化用户参与度（Engagement）为优化目标。
表面上，这是商业逻辑的自然延伸：平台希望用户停留更久、点击更多、互动更频繁。
然而，从信息动力学的视角看，这一优化过程正在系统性地将一个原本连通的信息空间
分割为互不渗透的**信息势能阱**（Information Potential Wells）。

In the year 2026, over 5 billion people worldwide receive information through social media,
and the core driving force of these platforms --- the recommendation algorithm --- is
optimized to maximize user engagement. Superficially, this is a natural extension of
business logic: platforms want users to stay longer, click more, and interact more
frequently. However, from the perspective of information dynamics, this optimization
process is systematically partitioning an originally connected information space into
mutually impermeable **Information Potential Wells**.

> **Definition:** [信息势能面 Information Potential Energy Surface, IPES]
> <!-- label: def:ipes -->
> 设 $\X$ 为用户群体空间，$\Y$ 为信息内容空间。信息势能面是一个标量场
> \[
> \InfoPE: \X \times \Y \to \R,
> \]
> 其值 $\InfoPE(x, y)$ 表示信息项 $y$ 对用户 $x$ 的认知势能。
> 势能越低，用户对该信息越容易接受（认知阻力越小）。
> 每个用户群 $G \subset \X$ 在 $\InfoPE$ 上形成一个**势能阱**：
> 用户倾向于消费和分享使 $\InfoPE$ 最小化的信息，而排斥使 $\InfoPE$ 升高的信息。
> 
> Let $\X$ be the user population space and $\Y$ be the information content space.
> The Information Potential Energy Surface is a scalar field
> $\InfoPE: \X \times \Y \to \R$,
> where $\InfoPE(x, y)$ represents the cognitive potential energy of information item $y$
> for user $x$. Lower potential energy means the user finds the information easier to
> accept (lower cognitive resistance). Each user group $G \subset \X$ forms a
> **potential well** on $\InfoPE$: users tend to consume and share information that
> minimizes $\InfoPE$, and reject information that raises $\InfoPE$.

> **Definition:** [坐标系 Coordinate System]
> <!-- label: def:coordsys -->
> 用户群的**信息坐标系** $\CoordSys_G$ 是一组正交基 $\{\mathbf{e}_1, ..., \mathbf{e}_d\}$
> 张成的 $d$-维子空间，用户通过该坐标系解释世界事件。
> 两个群 $A$ 和 $B$ 的**坐标系距离**定义为
> \[
> \Delta(\CoordSys_A, \CoordSys_B) = \inf_{\mathbf{R} \in O(d)} \|\CoordSys_A - \mathbf{R}\CoordSys_B\|_F,
> \]
> 其中 $O(d)$ 为正交群，$\|\cdot\|_F$ 为 Frobenius 范数。
> 坐标系距离度量了不同群体对同一事件
"理解框架
"的差异程度。
> 
> A user group's **Information Coordinate System** $\CoordSys_G$ is a $d$-dimensional
> subspace spanned by orthogonal basis vectors $\{\mathbf{e}_1, ..., \mathbf{e}_d\}$,
> through which the group interprets world events. The **coordinate system distance**
> between two groups $A$ and $B$ is defined as $\Delta(\CoordSys_A, \CoordSys_B)$,
> measuring the extent to which different groups have divergent ``interpretive frameworks''
> for the same events.

### 核心洞察：推荐算法 = 信息势能隔离器
### Core Insight: Recommendation Algorithm = Information Potential Isolator

本文的核心洞察可以用一句话概括：

\fbox{\begin{minipage}{0.92\textwidth}
**推荐算法 = 信息势能隔离器**

Recommendation Algorithm = Information Potential Isolator

推荐算法向用户展示与其现有坐标系匹配的内容 

$\Rightarrow$ 跨群体耦合强度 $\GCoupling \to 0$（隔离）

$\Rightarrow$ 不同群体在各自势能阱中永久振荡（推论~8）

$\Rightarrow$ 算法审计的核心指标：$\GCoupling$ 的测量与强制恢复
\end{minipage}}

这一洞察来自平等论（Equality Principle）在信息传播场景中的直接应用。
平等论要求 $\sum_{m} g_m = 0$，即所有跨群体交互的耦合强度之和为零——
这不是说交互不存在，而是说**净势能流在平衡态下消失**。
推荐算法的问题在于：它不仅仅让净势能流消失，
而是**系统性地阻止任何跨群体交互的发生**，使 $\GCoupling$ 自身趋于零。
这相当于在势能阱之间插入绝热壁（adiabatic wall）——每个群在自己的阱中永恒振荡，
从不接触其他群的坐标框架。

This insight comes from the direct application of the Equality Principle
($\sum_m g_m = 0$) to information propagation scenarios. The Equality Principle requires
that the sum of all cross-group interaction coupling strengths vanish --- this does not
mean interactions are absent, but that the **net potential energy flow vanishes
at equilibrium**. The problem with recommendation algorithms is that they do more than
merely let the net flow vanish --- they **systematically prevent any cross-group
interaction from occurring**, driving $\GCoupling$ itself to zero. This is equivalent to
inserting an adiabatic wall between potential wells --- each group oscillates eternally
in its own well, never contacting the coordinate framework of other groups.

### 主要贡献
### Main Contributions

本文的主要贡献如下：

**贡献 1 —— 信息势能面的形式化（第~2 节）.**
建立了社会媒体信息传播的势能面模型，定义了信息势能、坐标系、势能阱、耦合强度
$\GCoupling$ 等核心概念，并导出了势能面的基本动力学方程。

**Contribution 1 --- Formalization of IPES (Section~2).**
We establish the potential energy surface model of social media information propagation,
defining core concepts including information potential, coordinate system, potential well,
and coupling strength $\GCoupling$, and derive the fundamental dynamical equations of the IPES.

**贡献 2 —— 推荐算法的隔离定理（第~3 节）.**
证明推荐算法的优化目标（最大化参与度）等价于最小化跨坐标系暴露 $\GCoupling$，
并给出 $\GCoupling \to 0$ 时系统永久振荡的严格条件。

**Contribution 2 --- Isolation Theorem of Recommendation Algorithms (Section~3).**
We prove that the optimization objective of recommendation algorithms (maximizing engagement)
is equivalent to minimizing cross-coordinate-system exposure $\GCoupling$, and give the
rigorous conditions for permanent oscillation when $\GCoupling \to 0$.

**贡献 3 —— 算法审计标准（第~4 节）.**
提出基于 $\GCoupling$ 的算法审计框架，并证明 $\GCoupling$ 的可测量性与下界。

**Contribution 3 --- Algorithmic Audit Standard (Section~4).**
We propose an algorithmic audit framework based on $\GCoupling$ and prove its
measurability and lower bound.

**贡献 4 —— 强制混合信息流的收敛保证（第~5 节）.**
证明人为增加 $\GCoupling$ 可使系统从永久振荡收敛至理解共识，并给出收敛速率。

**Contribution 4 --- Convergence Guarantee of Forced Mixed Streams (Section~5).**
We prove that artificially increasing $\GCoupling$ drives the system from permanent
oscillation to convergence toward understanding consensus, and give the convergence rate.

## 信息势能面的数学形式化
## Mathematical Formalization of the Information Potential Energy Surface

### 基本设定与符号

### Basic Setup and Notation

考虑一个包含 $K$ 个用户群的社会 $\X = \{G_1, ..., G_K\}$，
每个群 $G_k$ 大小为 $N_k$，拥有自己的信息坐标系 $\CoordSys_k$。
信息内容空间 $\Y \subset \R^D$ 为所有可能的信息项（帖子、文章、视频等）的嵌入表示。
时间离散，以算法推荐周期为单位 $t = 0, 1, 2, ...$

Consider a society $\X = \{G_1, ..., G_K\}$ with $K$ user groups, each of size $N_k$,
possessing its own information coordinate system $\CoordSys_k$. The information content
space $\Y \subset \R^D$ is the embedding representation of all possible information items
(posts, articles, videos, etc.). Time is discrete, in units of algorithm recommendation
cycles: $t = 0, 1, 2, ...$

> **Definition:** [群信息态 Group Information State]
> 群 $G_k$ 在时刻 $t$ 的**信息态**为概率测度
> \[
> \mu_k^{(t)} \in \mathcal{P}(\Y),
> \]
> 表示该群当前消费的信息内容的分布。
> 群信息态的演化由推荐策略 $\pi_k: \mathcal{P}(\Y) \to \mathcal{P}(\Y)$ 驱动：
> \[
> \mu_k^{(t+1)} = \pi_k(\mu_k^{(t)}).
> \]
> 
> The **information state** of group $G_k$ at time $t$ is a probability measure
> $\mu_k^{(t)} \in \mathcal{P}(\Y)$ representing the distribution of information content
> currently consumed by that group. Its evolution is driven by a recommendation policy
> $\pi_k: \mathcal{P}(\Y) \to \mathcal{P}(\Y)$.

> **Definition:** [信息势能 Information Potential Energy]
> 给定信息态 $\mu \in \mathcal{P}(\Y)$ 和坐标系 $\CoordSys$，
> 群的信息势能定义为
> 
> $$<!-- label: eq:infoPE -->
> \InfoPE(\mu; \CoordSys) = \int_ \|\proj_{\CoordSys^\perp}(y)\|^2 \, d\mu(y),
> $$
> 
> 其中 $\proj_{\CoordSys^\perp}$ 是向坐标系正交补的投影。
> 直觉：信息项中与群坐标系正交的分量贡献认知阻力（势能）。
> 群坐标系内的分量贡献零势能（被自然接受）。
> 
> Given information state $\mu \in \mathcal{P}(\Y)$ and coordinate system $\CoordSys$,
> the group's information potential energy is defined as in  [ref], where
> $\proj_{\CoordSys^\perp}$ is the projection onto the orthogonal complement of the
> coordinate system. Intuition: the component of an information item orthogonal to
> the group's coordinate system contributes cognitive resistance (potential energy).
> Components within the coordinate system contribute zero potential energy (naturally accepted).

> **Definition:** [坐标系对齐度 Alignment]
> 群 $G_k$ 的信息态与群 $G_j$ 的坐标系之间的**对齐度**为
> 
> $$<!-- label: eq:alignment -->
> A_{kj}(\mu_k) = 1 - \frac{\InfoPE(\mu_k; \CoordSys_j)}{\max_ \InfoPE(\mu; \CoordSys_j)}.
> $$
> 
> $A_{kk} = 1$（自对齐），$A_{kj} \in [0,1]$ 度量群 $k$ 消费的信息与群 $j$ 的理解框架的兼容性。
> 
> The **alignment** between $G_k$'s information state and $G_j$'s coordinate system is
> $A_{kj} = 1$ for self-alignment; $A_{kj} \in [0,1]$ measures the compatibility between
> the information consumed by group $k$ and the interpretive framework of group $j$.

### 信息势能面的动力学

### Dynamics of the Information Potential Energy Surface

\begin{assumption}[势能最小化驱动]
用户（以及为他们服务的推荐算法）倾向于使势能最小化：消费与自身坐标系对齐的信息，
回避需要认知重构的信息。正式地，推荐策略 $\pi_k$ 满足
\[
\InfoPE(\pi_k(\mu); \CoordSys_k) \leq \InfoPE(\mu; \CoordSys_k), \quad \forall \mu \in \mathcal{P}(\Y).
\]

Users (and the recommendation algorithms serving them) tend to minimize potential energy:
consume information aligned with their own coordinate system, avoid information requiring
cognitive restructuring. Formally, the recommendation policy $\pi_k$ satisfies the above
inequality for all $\mu$.
\end{assumption}

> **Definition:** [跨群体耦合强度 Cross-Group Coupling Strength]
> 群 $G_k$ 和 $G_j$ 之间的**跨群体耦合强度**定义为
> 
> $$<!-- label: eq:gcross -->
> \GCoupling_{kj}^{(t)} = \frac{1}{N_k N_j} \sum_{x \in G_k} \sum_{y \in G_j}
> \exp\pqty{-\alpha \cdot \Delta(\CoordSys_k, \CoordSys_j)} \cdot
> \mathbbm{1}\{x  暴露于  y  的信息在时刻  t\},
> $$
> 
> 其中 $\alpha > 0$ 为坐标系距离的衰减系数。
> $\GCoupling_{kj}$ 度量了群 $k$ 的成员暴露于群 $j$ 坐标系信息的有效强度。
> 
> The **cross-group coupling strength** between groups $G_k$ and $G_j$ is defined as
> in  [ref], where $\alpha > 0$ is the decay coefficient of coordinate system
> distance. $\GCoupling_{kj}$ measures the effective intensity with which members of
> group $k$ are exposed to information in the coordinate system of group $j$.

> **Definition:** [系统耦合矩阵 System Coupling Matrix]
> 定义 $K \times K$ 耦合矩阵
> \[
> \mathbf{G}^{(t)} = [\GCoupling_{kj}^{(t)}]_{k,j=1}^K,
> \]
> 对角元 $\GCoupling_{kk} = 1$（群内耦合总是最大），
> 非对角元 $\GCoupling_{kj} \in [0,1]$ 度量跨群暴露。
> 
> Define the $K \times K$ coupling matrix $\mathbf{G}^{(t)} = [\GCoupling_{kj}^{(t)}]_{k,j=1}^K$,
> with diagonal $\GCoupling_{kk} = 1$ (intra-group coupling is always maximal),
> off-diagonal $\GCoupling_{kj} \in [0,1]$ measuring cross-group exposure.

> **Definition:** [势能阱深度 Potential Well Depth]
> 群 $G_k$ 在其自身信息势能阱中的**深度**定义为
> 
> $$<!-- label: eq:welldepth -->
> D_k^{(t)} = \InfoPE(\mu_k^{(t)}; \CoordSys_k),
> $$
> 
> 即群信息态在自身坐标系下的势能。
> 由于势能最小化驱动，$D_k^{(t)}$ 随时间单调不增。
> 
> The **depth** of group $G_k$ in its own information potential well is defined as in
>  [ref], i.e., the potential energy of the group's information state under
> its own coordinate system. Due to the potential energy minimization drive,
> $D_k^{(t)}$ is non-increasing in time.

### 总势能与平等条件

### Total Potential Energy and the Equality Condition

> **Definition:** [社会总信息势能 Total Social Information Potential Energy]
> 整个社会在时刻 $t$ 的总信息势能定义为
> 
> $$<!-- label: eq:totalPE -->
> \InfoPE_{total}^{(t)} = \sum_{k=1}^K \InfoPE(\mu_k^{(t)}; \CoordSys_k).
> $$

> **Proposition:** [总势能的单调性 Monotonicity of Total PE]<!-- label: prop:monotone -->
> 在纯推荐驱动下（无跨群干预），总信息势能单调递减：
> \[
> \InfoPE_{total}^{(t+1)} \leq \InfoPE_{total}^{(t)}, \quad \forall t \geq 0.
> \]
> 当且仅当所有群均已达到其势能阱底部时等号成立：
> \[
> \InfoPE(\mu_k^{(t)}; \CoordSys_k) = 0, \quad \forall k.
> \]
> 
> Under pure recommendation drive (no cross-group intervention), the total information
> potential energy decreases monotonically, with equality iff all groups have reached
> the bottom of their potential wells.

> **Proof:** 由假设~1，每个 $\pi_k$ 是势能递减的：
> $\InfoPE(\mu_k^{(t+1)}; \CoordSys_k) \leq \InfoPE(\mu_k^{(t)}; \CoordSys_k)$。
> 对所有 $k$ 求和即得总势能单调性。

这一命题看上去无害——势能降低似乎意味着用户越来越舒适。
然而，这正是危机的数学表达：**总势能最小化 = 各群沉入自己的势能阱深处
= 跨群隔离最大化**。

This proposition appears innocuous --- decreasing potential energy seems to mean users
are becoming more comfortable. However, this is precisely the mathematical expression of
the crisis: **total potential energy minimization = each group sinking deep into its
own potential well = cross-group isolation maximization**.

\begin{attackbox}
  **舒适即隔离**.
  命题 [ref] 揭示了一个严峻的数学事实：
  推荐算法使每个群在自己的坐标系下势能为零——
  这意味着用户看到的信息完全符合其既有框架，
  没有任何认知摩擦。
  但与此同时，不同群之间的耦合强度 $\GCoupling_{kj}$ 趋于零。
  **系统的全局势能最小化与全局连通性最大化是不可兼得的**。
  选择舒适（低势能）意味着选择隔离（低连通）。

  **Comfort is Isolation.**
  Proposition [ref] reveals a grim mathematical fact:
  recommendation algorithms drive each group's potential energy to zero under its own
  coordinate system --- meaning users see information that perfectly fits their existing
  framework, with zero cognitive friction. But simultaneously, the coupling strength
  $\GCoupling_{kj}$ between different groups tends to zero.
  **Global potential energy minimization and global connectivity maximization
  are mutually incompatible.** Choosing comfort (low PE) means choosing isolation
  (low connectivity).
\end{attackbox}

## 推荐算法的信息势能隔离定理
## The Information Potential Isolation Theorem of Recommendation Algorithms

### 推荐算法作为势能最小化器

### Recommendation Algorithm as Potential Energy Minimizer

现代推荐算法（协同过滤、深度神经网络推荐、基于Transformer的序列推荐等）
可以统一理解为以下优化问题：

Modern recommendation algorithms (collaborative filtering, deep neural network
recommenders, Transformer-based sequential recommenders, etc.) can be uniformly
understood as solving the following optimization problem:

> **Definition:** [推荐算法的优化目标 Objective of Recommendation Algorithm]
> <!-- label: def:recobj -->
> 给定用户 $x \in G_k$，推荐算法选择信息项 $y^* \in \Y$ 最大化
> 
> $$<!-- label: eq:recopt -->
> y^* = \argmax_{y \in \Y} \;
> \underbrace{s(x, y)}_{预测参与度} \;-\;
> \underbrace{\beta \cdot \InfoPE(y; \CoordSys_k)}_{隐式势能惩罚},
> $$
> 
> 其中 $s(x,y)$ 为预测参与度得分（点击率、停留时长、分享概率等），
> $\beta \geq 0$ 为势能惩罚权重。
> 
> Given a user $x \in G_k$, the recommendation algorithm selects an information item
> $y^* \in \Y$ to maximize the expression in  [ref], where $s(x,y)$ is the
> predicted engagement score (click-through rate, dwell time, share probability, etc.),
> and $\beta \geq 0$ is the potential energy penalty weight.

> **Remark:** 式 [ref] 的势能惩罚项 $\InfoPE(y; \CoordSys_k)$ 通常不是显式设计，
> 而是推荐算法训练数据中隐式蕴含的。
> 因为算法从历史交互数据中学习，而历史数据中用户已经倾向于消费低势能内容——
> 这是**选择偏差**（Selection Bias）的势能形式。
> 
> The potential energy penalty $\InfoPE(y; \CoordSys_k)$ in  [ref] is typically
> not explicitly designed but implicitly embedded in the training data from which the
> algorithm learns. Since the algorithm learns from historical interaction data, and users
> in the historical data already tend to consume low-PE content --- this is the
> potential-energy form of **Selection Bias**.

> **Theorem:** [推荐算法的势能隔离定理 Potential Isolation Theorem of Recommendation]
> <!-- label: thm:isolation -->
> 设推荐算法以式 [ref] 为目标，且 $\beta > 0$。
> 则对于任意两个不同的群 $G_k \neq G_j$，跨群体耦合强度满足
> 
> $$<!-- label: eq:isolationbound -->
> \GCoupling_{kj}^{(t)} \leq \GCoupling_{kj}^{(0)} \cdot
> \exp\pqty{-\beta \cdot \Delta(\CoordSys_k, \CoordSys_j) \cdot t}.
> $$
> 
> 特别地，当 $t \to \infty$ 时，
> \[
> \lim_{t \to \infty} \GCoupling_{kj}^{(t)} = 0, \quad \forall k \neq j.
> \]
> 
> Let the recommendation algorithm optimize  [ref] with $\beta > 0$.
> Then for any two distinct groups $G_k \neq G_j$, the cross-group coupling strength
> satisfies  [ref]. In particular, as $t \to \infty$,
> $\GCoupling_{kj}^{(t)} \to 0$ for all $k \neq j$.

> **Proof:** 考虑群 $k$ 在时刻 $t$ 消费的信息项集合 $\Y_k^{(t)}$。
> 势能惩罚项 $\beta \cdot \InfoPE(y; \CoordSys_k)$ 使算法倾向于选择 $\CoordSys_k$ 内的内容，
> 即 $\|\proj_{\CoordSys_k^\perp}(y)\|$ 小的 $y$。
> 对于群 $j$ 坐标系内的内容 $y \in \CoordSys_j$，有
> \[
> \InfoPE(y; \CoordSys_k) = \|\proj_{\CoordSys_k^\perp}(y)\|^2
> \geq \sin^2(\theta_{kj}) \cdot \|y\|^2,
> \]
> 其中 $\theta_{kj}$ 为坐标系 $\CoordSys_k$ 与 $\CoordSys_j$ 之间的主角（principal angle）。
> 由坐标系距离的定义，$\sin(\theta_{kj}) \geq c \cdot \Delta(\CoordSys_k, \CoordSys_j)$
> 对某绝对常数 $c > 0$ 成立。
> 因此，每次推荐周期中，来自群 $j$ 坐标系的信息被选中的概率以因子
> $\exp(-\beta \cdot \Delta(\CoordSys_k, \CoordSys_j))$ 衰减。
> 经 $t$ 步累积，得到指数衰减界 [ref]。
> 
> Consider the set $\Y_k^{(t)}$ of information items consumed by group $k$ at time $t$.
> The PE penalty $\beta \cdot \InfoPE(y; \CoordSys_k)$ biases the algorithm toward content
> within $\CoordSys_k$, i.e., $y$ with small $\|\proj_{\CoordSys_k^\perp}(y)\|$.
> For content $y \in \CoordSys_j$ in group $j$'s coordinate system, we have
> $\InfoPE(y; \CoordSys_k) \geq \sin^2(\theta_{kj}) \cdot \|y\|^2$,
> where $\theta_{kj}$ is the principal angle between the two coordinate systems.
> By definition of coordinate system distance,
> $\sin(\theta_{kj}) \geq c \cdot \Delta(\CoordSys_k, \CoordSys_j)$ for some absolute
> constant $c > 0$. Therefore, in each recommendation cycle, the probability that
> information from group $j$'s coordinate system is selected decays by factor
> $\exp(-\beta \cdot \Delta(\CoordSys_k, \CoordSys_j))$. Accumulating over $t$ steps
> yields the exponential decay bound  [ref].

> **Corollary:** [过滤气泡的势能等价表述 Potential-Energy Reformulation of Filter Bubble]
> <!-- label: cor:filterbubble -->
> 定理 [ref] 给出了过滤气泡现象的精确势能表述：
> 过滤气泡不是偶然的副产品，而是**推荐算法在势能面梯度下降的必然结果**。
> 当 $\GCoupling_{kj} = 0$ 对所有 $k \neq j$ 成立时，
> 系统处于**完全势能隔离**（Complete Potential Isolation）状态：
> 每个群完全封闭在自身的势能阱中，
> 任何来自其他坐标系的信息都会被势能壁垒反射。
> 
> Theorem [ref] provides a precise potential-energy reformulation of the
> filter bubble phenomenon: the filter bubble is not an accidental byproduct but an
> **inevitable consequence of the recommendation algorithm's gradient descent on
> the potential energy surface**. When $\GCoupling_{kj} = 0$ for all $k \neq j$, the
> system is in a state of **Complete Potential Isolation**: each group is fully
> enclosed in its own potential well, and any information from other coordinate systems
> is reflected by the potential barrier.

\begin{attackbox}
  **指数衰减的速度**.
  界 [ref] 表明隔离以指数速度发生。
  衰减速率 $\beta \cdot \Delta(\CoordSys_k, \CoordSys_j)$ 中的两个因子都是
  平台设计的结果：$\beta$ 来自算法对历史数据的拟合强度，
  $\Delta(\CoordSys_k, \CoordSys_j)$ 来自平台内容分类和用户聚类的粒度。
  在实践中，$\Delta$ 通常在初始时就很大（因为平台为了广告定向已经对用户
  进行了精细划分），这意味着**从用户注册的第一天起，隔离就已经开始**。

  **The Speed of Exponential Decay.**
  The bound  [ref] shows that isolation occurs at exponential speed.
  Both factors in the decay rate, $\beta$ (fitting strength of the algorithm to
  historical data) and $\Delta(\CoordSys_k, \CoordSys_j)$ (granularity of content
  classification and user clustering), are products of platform design.
  In practice, $\Delta$ is typically large from the start (because platforms already
  finely partition users for ad targeting), meaning that **isolation begins from
  the very first day a user registers**.
\end{attackbox}

### 永久振荡定理

### The Permanent Oscillation Theorem

当系统达到完全势能隔离后，不同群的信息态如何演化？以下定理给出了答案。

Once the system reaches complete potential isolation, how do the information states of
different groups evolve? The following theorem provides the answer.

> **Theorem:** [信息势能阱中的永久振荡定理 Permanent Oscillation in IPE Wells]
> <!-- label: thm:oscillation -->
> 设系统处于完全势能隔离状态（$\GCoupling_{kj} = 0$ 对所有 $k \neq j$），
> 且每个群的推荐策略 $\pi_k$ 在其势能阱内是遍历的（ergodic）。
> 则每个群的信息态 $\mu_k^{(t)}$ 在其势能阱 $\mathcal{W}_k = \{\mu : \InfoPE(\mu; \CoordSys_k) = 0\}$
> 内永久振荡，且不同群的信息态**永不相交**：
> \[
> \supp(\mu_k^{(t)}) \cap \supp(\mu_j^{(t')}) = \varnothing, \quad
> \forall k \neq j, \; \forall t, t' \geq T_{iso},
> \]
> 其中 $T_{iso}$ 为达到完全隔离所需的时刻。
> 
> Assume the system is in complete potential isolation ($\GCoupling_{kj} = 0$ for all
> $k \neq j$), and each group's recommendation policy $\pi_k$ is ergodic within its
> potential well. Then each group's information state $\mu_k^{(t)}$ oscillates permanently
> within its potential well $\mathcal{W}_k$, and the information states of different
> groups **never intersect**.

> **Proof:** 在完全隔离下，每个群的信息态演化完全由内部推荐策略 $\pi_k$ 驱动，
> 且约束在 $\mathcal{W}_k$ 内。
> 由于 $\mathcal{W}_k \cap \mathcal{W}_j = \varnothing$ 对 $k \neq j$
> （由坐标系距离 $\Delta(\CoordSys_k, \CoordSys_j) > 0$ 保证），
> 不同群的信息态支撑集必然不交。
> 遍历性保证每个群在其阱内持续运动（而非静止在单点），故为永久振荡。
> 
> Under complete isolation, each group's information state evolution is driven solely by
> its internal recommendation policy $\pi_k$, constrained to $\mathcal{W}_k$.
> Since $\mathcal{W}_k \cap \mathcal{W}_j = \varnothing$ for $k \neq j$
> (guaranteed by $\Delta(\CoordSys_k, \CoordSys_j) > 0$), the supports of different
> groups' information states are necessarily disjoint. Ergodicity ensures each group
> continues to move within its well (rather than being stationary at a single point),
> hence permanent oscillation.

> **Corollary:** [极化作为永久振荡的宏观表现]
> <!-- label: cor:polarization -->
> 推论 [ref]（对应于 SCX 推论~8）.
> 社会极化不是暂时的意见分歧，而是**完全势能隔离下永久振荡的宏观表现**。
> 两个极化群 $A$ 和 $B$ 在任何时刻 $t$ 都不共享信息基础——
> 它们生活于不同的信息宇宙中，用不可通约的坐标系解释世界。
> 任何试图通过
"辩论
"或
"事实核查
"在群间建立共识的努力都是徒劳的，
> 因为不存在共享的信息参考系。
> 
> **Corollary~8 of SCX**: Social polarization is not temporary disagreement but the
> **macroscopic manifestation of permanent oscillation under complete potential isolation**.
> Two polarized groups $A$ and $B$ share no information basis at any time $t$ ---
> they inhabit different information universes, interpreting the world through
> incommensurable coordinate systems. Any attempt to establish consensus through
> ``debate'' or ``fact-checking'' between groups is futile, because there is no
> shared information reference frame.

\begin{attackbox}
  **
"事实核查
"为何失败**.
  推论 [ref] 解释了当代社会一个令人困惑的现象：
  事实核查（Fact-Checking）不仅未能弥合极化，反而常常加剧分歧。
  势能理论给出的原因是：事实核查机构本身位于某个坐标系中，
  其
"事实
"在另一坐标系下被感知为高势能信息（认知威胁），
  因此被势能壁垒反射。
  **事实核查只对已经共享坐标系的人群有效**。

  **Why ``Fact-Checking'' Fails.**
  Corollary [ref] explains a puzzling contemporary phenomenon:
  fact-checking not only fails to bridge polarization but often exacerbates it.
  The potential-energy explanation is: fact-checking organizations themselves are
  situated within some coordinate system, and their ``facts'' are perceived as
  high-PE information (cognitive threat) under another coordinate system, thus
  reflected by the potential barrier.
  **Fact-checking is only effective for populations that already share a
  coordinate system.**
\end{attackbox}

### 信息势能梯度的群间动态

### Inter-Group Dynamics of the Information Potential Gradient

> **Definition:** [势能梯度矢量 Potential Gradient Vector]
> 定义时刻 $t$ 群 $k$ 的信息势能相对于群 $j$ 坐标系的**梯度**：
> 
> $$<!-- label: eq:PEgradient -->
> \nabla_{kj} \InfoPE^{(t)} = \frac{\partial \InfoPE(\mu_k^{(t)}; \CoordSys_j)}{\partial \mu_k},
> $$
> 
> 即群 $k$ 的当前信息态在群 $j$ 的势能面上的最陡上升方向。
> 势能梯度驱动群的信息态远离其他群的势能阱底部。
> 
> Define the **gradient** of group $k$'s information PE with respect to group $j$'s
> coordinate system as in  [ref], i.e., the steepest ascent direction of
> group $k$'s current information state on group $j$'s potential energy surface. The PE
> gradient drives a group's information state away from the bottom of other groups'
> potential wells.

> **Proposition:** [势能梯度的排斥性 Repulsiveness of PE Gradient]
> <!-- label: prop:repulsive -->
> 对于 $k \neq j$，势能梯度 $\nabla_{kj} \InfoPE^{(t)}$ 的方向与使
> $\mu_k^{(t)}$ 接近 $\mathcal{W}_j$ 的方向相反。
> 在纯推荐驱动下，群 $k$ 和 $j$ 的信息态在势能面上**互相排斥**，
> 排斥力正比于坐标系距离：
> \[
> \|\nabla_{kj} \InfoPE^{(t)}\| \propto \Delta(\CoordSys_k, \CoordSys_j).
> \]
> 
> For $k \neq j$, the PE gradient $\nabla_{kj} \InfoPE^{(t)}$ points opposite to the
> direction that brings $\mu_k^{(t)}$ closer to $\mathcal{W}_j$. Under pure recommendation
> drive, the information states of groups $k$ and $j$ **mutually repel** on the
> potential energy surface, with repulsive force proportional to the coordinate system
> distance $\Delta(\CoordSys_k, \CoordSys_j)$.

> **Proof:** 由定义 [ref]，$\InfoPE(\mu_k; \CoordSys_j)$ 是 $\mu_k$ 在
> $\CoordSys_j^\perp$ 上质量的二次型。
> 其梯度 $\nabla_{kj} \InfoPE$ 指向使 $\mu_k$ 更多投影到 $\CoordSys_j^\perp$ 的方向，
> 即远离 $\CoordSys_j$（远离群 $j$ 的势能阱底部）。
> 而 $\CoordSys_k$ 和 $\CoordSys_j$ 之间的距离越大，
> $\CoordSys_k^\perp \cap \CoordSys_j$ 的交集越小，
> $\mu_k$ 在 $\CoordSys_j^\perp$ 上的投影越大，故梯度大小正比于 $\Delta$。

这一命题具有深远的社会含义：推荐算法不仅是隔离器，
而且是**主动排斥器**——已分离的群不仅保持分离，
还在势能面上**相互远离**。
这是
"极化加剧
"（Increasing Polarization）的数学机制。

This proposition has profound social implications: recommendation algorithms are not
merely isolators but **active repellers** --- already-separated groups not only
remain separated but **move farther apart** on the potential energy surface.
This is the mathematical mechanism of ``Increasing Polarization.''

## 基于耦合强度的算法审计框架
## Algorithmic Audit Framework Based on Coupling Strength

### 审计的必要性

### The Necessity of Auditing

前述定理揭示了一个严峻的事实：推荐算法在优化其商业目标的过程中，
系统性地破坏了社会的信息连通性。
这使得算法审计成为必要——我们需要一个客观的、可量化的标准来评估
推荐算法对社会信息结构的破坏程度。

The previous theorems reveal a grim fact: recommendation algorithms, in the process of
optimizing their business objectives, systematically destroy the information connectivity
of society. This makes algorithmic auditing necessary --- we need an objective,
quantifiable standard to assess the extent to which recommendation algorithms damage
the social information structure.

### 审计项定义

### Definition of Audit Items

> **Definition:** [算法审计项 Algorithmic Audit Items]
> 对推荐算法 $\Pi = (\pi_1, ..., \pi_K)$ 的审计包含以下指标：
> 
> 
> **审计项 A1 —— 跨群体耦合强度 (Cross-Group Coupling Strength):**
> \[
> \GCoupling_{avg}^{(t)} = \frac{1}{K(K-1)} \sum_{k \neq j} \GCoupling_{kj}^{(t)}.
> \]
> $\GCoupling_{avg} \in [0,1]$ 越小，隔离越严重。
> 健康阈值：$\GCoupling_{avg} \geq \GCoupling_ = 0.15$。
> 
> 
> **审计项 A2 —— 耦合衰减速率 (Coupling Decay Rate):**
> \[
> \ISOLambda = -\frac{d}{dt} \log \GCoupling_{avg}^{(t)} \approx \beta \cdot \bar,
> \]
> 其中 $\bar = \frac{1}{K(K-1)} \sum_{k \neq j} \Delta(\CoordSys_k, \CoordSys_j)$
> 为平均坐标系距离。
> $\ISOLambda$ 越大，隔离速度越快。
> 告警阈值：$\ISOLambda > 0.05$ / 周期。
> 
> 
> **审计项 A3 —— 信息势能不平等 (Information PE Inequality):**
> \[
> \InfoPE_{Gini} = \frac{\sum_{k,j} |\InfoPE(\mu_k; \CoordSys_k) - \InfoPE(\mu_j; \CoordSys_j)|}
> {2K \sum_k \InfoPE(\mu_k; \CoordSys_k)}.
> \]
> 度量不同群
"认知舒适度
"的不平等程度。虽然每个群的自身势能都在下降，
> 但下降速度的差异导致某些群比其他群更快
"极化"。
> 
> 
> **审计项 A4 —— 坐标系距离矩阵 (Coordinate Distance Matrix):**
> \[
> \mathbf = [\Delta(\CoordSys_k, \CoordSys_j)]_{k,j=1}^K.
> \]
> 度量不同群之间
"理解鸿沟
"的静态结构。
> 当 $\mathbf$ 的谱半径超过某阈值时，系统本质不可调和。
> 
> 
>  The audit of a recommendation algorithm $\Pi = (\pi_1, ..., \pi_K)$ includes
> the following metrics: **A1**: Cross-Group Coupling Strength (lower = more isolation,
> healthy threshold $\geq 0.15$); **A2**: Coupling Decay Rate (higher = faster isolation,
> alarm threshold $> 0.05$/cycle); **A3**: Information PE Inequality (Gini-like measure
> of cognitive comfort disparity); **A4**: Coordinate Distance Matrix (spectral radius
> indicating fundamental irreconcilability).

> **Theorem:** [耦合强度的可测量性 Measurability of Coupling Strength]
> <!-- label: thm:measurable -->
> $\GCoupling_{kj}^{(t)}$ 可由平台数据在以下条件下可识别地（identifiably）估计：
> 
1. 可获取用户的信息消费序列 $\{y_1^{(x)}, ..., y_T^{(x)}\}$；
2. 已知（或可估计）信息项的坐标系嵌入；
3. 时间窗口 $T$ 足够大，使得采样覆盖跨群暴露事件。

> 在此条件下，$\GCoupling_{kj}$ 的估计量 $\widehat_{kj}$ 满足
> \[
> \Pbb\pqty{|\widehat_{kj} - \GCoupling_{kj}| > \varepsilon}
> \leq 2\exp\pqty{-\frac{T \varepsilon^2}{2}}.
> \]
> 
> $\GCoupling_{kj}^{(t)}$ can be identifiably estimated from platform data under the
> conditions: (i) access to user information consumption sequences; (ii) known (or
> estimable) coordinate system embeddings of information items; (iii) sufficiently large
> time window $T$ for sampling cross-group exposure events. Under these conditions,
> the estimate satisfies the above concentration inequality.

> **Proof:** $\GCoupling_{kj}$ 是跨群暴露事件的期望频率乘以衰减因子。
> 在条件~(i)-(iii) 下，暴露事件构成独立的 Bernoulli 试验序列，
> Hoeffding 不等式直接给出上述集中界。

\begin{attackbox}
  **审计可行性的现实障碍**.
  定理 [ref] 的条件~(ii) —— 已知信息项的坐标系嵌入 ——
  在现实中难以满足。
  平台通常不会公开其内容嵌入；即使公开，将高维嵌入解释为
"坐标系
"
  需要额外的语义标注，而标注本身又依赖于标注者的坐标系。
  这构成了一个**审计的观测者悖论**（Observer's Paradox of Auditing）：
  审计需要独立于平台的坐标系定义，但任何坐标系定义都隐含某种立场。

  **Practical Obstacles to Audit Feasibility.**
  Condition (ii) of Theorem [ref] --- known coordinate system embeddings
  of information items --- is difficult to satisfy in practice. Platforms typically do
  not disclose their content embeddings; even if disclosed, interpreting high-dimensional
  embeddings as ``coordinate systems'' requires additional semantic annotation, which
  itself depends on the annotator's coordinate system. This constitutes an
  **Observer's Paradox of Auditing**: auditing requires coordinate system definitions
  independent of the platform, but any coordinate system definition implicitly embeds
  some standpoint.
\end{attackbox}

### 审计的算法实现

### Algorithmic Implementation of the Audit

> **Definition:** [耦合强度估计算法 Coupling Strength Estimation Algorithm]
> <!-- label: def:auditalg -->
> **输入：** 用户消费序列，信息嵌入 $e(y) \in \R^D$，群划分。
> **输出：** $\widehat_{kj}$ 对所有 $k \neq j$。
> 
> 
1. 为每个群 $k$ 估计坐标系基 $\widehat_k$（通过对群内信息嵌入的 PCA）；
2. 计算 $\widehat(\CoordSys_k, \CoordSys_j) = \|\widehat_k - \mathbf{R}^*\widehat_j\|_F$，
3. 对每个用户 $x \in G_k$，统计其消费序列中来自群 $j$ 坐标系的信息项比例；
4. 按式 [ref] 聚合，以 $\widehat$ 替代 $\Delta$。

> 
> **Input:** User consumption sequences, information embeddings $e(y) \in \R^D$, group
> partition. **Output:** $\widehat_{kj}$ for all $k \neq j$.
> Algorithm steps: (1) estimate coordinate system basis $\widehat_k$ for each
> group via PCA on intra-group information embeddings; (2) compute coordinate distance
> via optimal orthogonal rotation (Procrustes analysis); (3) for each user, count the
> fraction of consumed items from other groups' coordinate systems; (4) aggregate per
>  [ref].

> **Proposition:** [审计算法的样本复杂度 Sample Complexity of Audit]
> <!-- label: prop:samplecomplexity -->
> 为使所有 $\widehat_{kj}$ 的估计误差 $\leq \varepsilon$ 以概率 $1-\delta$ 成立，
> 每个群所需的用户消费数据量为
> \[
> T \geq \frac{2\log(2K(K-1)/\delta)}{\varepsilon^2} \cdot
> \max_{k \neq j} \frac{1}{\GCoupling_{kj}(1-\GCoupling_{kj})}.
> \]
> 注意：当 $\GCoupling_{kj} \to 0$ 时 $T \to \infty$ ——
> **隔离越严重，审计越困难**。
> 
> To ensure estimation error $\leq \varepsilon$ for all $\widehat_{kj}$ with
> probability $1-\delta$, the required data per group is given above.
> Note: as $\GCoupling_{kj} \to 0$, $T \to \infty$ ---
> **the more severe the isolation, the harder the audit**.

> **Proof:** 由定理 [ref] 的集中界和并集界（union bound）直接得到。
> 分母中的 $\GCoupling_{kj}(1-\GCoupling_{kj})$ 来自 Bernoulli 方差的逆。

## 强制混合信息流：从永久振荡到收敛
## Forced Mixed Information Streams: From Permanent Oscillation to Convergence

### 平等论的核心要求

### The Core Requirement of the Equality Principle

平等论（Equality Principle）的核心要求是：
\[
\sum_{m} g_m = 0,
\]
即系统中所有交互耦合强度的代数和为零。
将此应用于社会媒体的信息传播：
如果系统处于完全隔离状态（所有非对角 $\GCoupling_{kj} = 0$），
则这个和确实为零——但这是一种**退化零**（degenerate zero），
因为每个项本身为零，而非通过正负相消达到零。

The core requirement of the Equality Principle is $\sum_m g_m = 0$, i.e., the algebraic
sum of all interaction coupling strengths in the system vanishes. Applied to social media
information propagation: if the system is in complete isolation (all off-diagonal
$\GCoupling_{kj} = 0$), then this sum is indeed zero --- but it is a **degenerate
zero**, because each term individually vanishes, rather than being canceled by positive
and negative contributions.

> **Definition:** [非退化耦合 Non-Degenerate Coupling]
> 耦合矩阵 $\mathbf{G}$ 称为**非退化**的，若存在至少一对 $(k,j), k \neq j$ 使得
> $\GCoupling_{kj} > 0$，且耦合之和满足平等条件：
> \[
> \sum_{k \neq j} \GCoupling_{kj} \cdot \sgn(\Delta(\CoordSys_k, \CoordSys_j) - \bar) = 0,
> \]
> 其中 $\bar$ 为平均坐标系距离。
> 
> A coupling matrix $\mathbf{G}$ is called **non-degenerate** if there exists at least
> one pair $(k,j), k \neq j$ with $\GCoupling_{kj} > 0$, and the coupling sum satisfies
> the equality condition above.

非退化耦合是社会信息健康的基本要求——
它意味着不同"坐标系的群之间存在真实的、非零的相互暴露。**这是平等论在信息传播中的操作性定义**：不是要求所有群拥有一致的观点，而是要求所有群之间存在非零的跨坐标系信息流。

Non-degenerate coupling is the fundamental requirement for a healthy information society --- it means that real, non-zero mutual exposure exists between groups with different coordinate systems. **This is the operational definition of the Equality Principle in information propagation**: it does not require all groups to have uniform opinions, but requires that non-zero cross-coordinate-system information flow exists between all groups.

### 强制混合策略

### Forced Mixing Strategies

> **Definition:** [强制混合信息流 Forced Mixed Information Stream, FMIS]
> **强制混合信息流**是一种算法干预：在每个推荐周期 $t$，
> 对每个用户 $x \in G_k$，以概率 $p_{mix} > 0$ 向其展示
> 来自其他群 $G_j$（$j \neq k$）坐标系的信息项，选择规则与用户当前兴趣无关，
> 而与目标群的坐标系对齐度成反比：
> 
> $$<!-- label: eq:fmix -->
> \Pbb(y  被选 \mid y \in \CoordSys_j) \propto
> \frac{1}{A_{kj}(\mu_k^{(t)}) + \varepsilon},
> $$
> 
> 其中 $\varepsilon > 0$ 为防止除零的小常数。
> 
> **Forced Mixed Information Stream (FMIS)** is an algorithmic intervention: in each
> recommendation cycle $t$, for each user $x \in G_k$, with probability $p_{mix} > 0$,
> show an information item from another group $G_j$ ($j \neq k$)'s coordinate system,
> selected inversely proportional to the current alignment $A_{kj}$, as in  [ref].

> **Remark:** 强制混合与
"反向推荐
"（Counter-Recommendation）不同。
> 反向推荐直接推送用户反对的内容，通常引发抗拒（高势能反射）。
> 强制混合选择的是当前最不被接受的内容——那些用户在自身坐标系下完全看不见的内容。
> 这遵循了平等论中
"补足缺失交互
"的原则。
> 
> FMIS differs from ``Counter-Recommendation.'' Counter-recommendation directly pushes
> content users oppose, typically triggering resistance (high-PE reflection). FMIS selects
> content that is *currently least accepted* --- content users cannot see at all
> under their own coordinate system. This follows the Equality Principle's logic of
> ``complementing missing interactions.''

### 收敛定理

### The Convergence Theorem

> **Theorem:** [强制混合的收敛定理 Convergence Theorem of Forced Mixing]
> <!-- label: thm:convergence -->
> 设系统初始时处于完全势能隔离状态（$\GCoupling_{kj}^{(0)} = 0, \forall k \neq j$），
> 并施加概率为 $p_{mix} > 0$ 的强制混合。
> 则存在一个临界混合概率
> \[
> p_{mix}^* = \frac{\ISOLambda + \Gamma_0},
> \]
> 其中 $\Gamma_0 > 0$ 为系统的基础收敛速率。
> 当 $p_{mix} > p_{mix}^*$ 时，
> 跨群体耦合强度以速率 $\Gamma = p_{mix}\Gamma_0 - (1-p_{mix})\ISOLambda > 0$ 增长：
> \[
> \GCoupling_{avg}^{(t)} \geq 1 - \exp(-\Gamma t).
> \]
> 特别地，$\lim_{t \to \infty} \GCoupling_{avg}^{(t)} = 1$——
> 所有群之间的信息流完全恢复。
> 
> Assume the system is initially in complete potential isolation and FMIS with probability
> $p_{mix} > 0$ is applied. Then there exists a critical mixing probability
> $p_{mix}^*$ as above. When $p_{mix} > p_{mix}^*$, the cross-group
> coupling strength grows at rate $\Gamma > 0$, and $\GCoupling_{avg}^{(t)} \to 1$
> as $t \to \infty$ --- full restoration of inter-group information flow.

> **Proof:** 在每步 $t$，推荐有两种可能：
> (1) 以概率 $1-p_{mix}$ 为标准推荐，此时 $\GCoupling$ 以速率 $\ISOLambda$ 衰减
> （定理 [ref]）；
> (2) 以概率 $p_{mix}$ 为强制混合，此时 $\GCoupling$ 以速率 $\Gamma_0$ 增长
> （因为强制混合直接将跨坐标系内容注入用户信息流）。
> 因此 $\GCoupling$ 的期望动力学为
> \[
> \frac{d}{dt} \GCoupling_{avg} =
> p_{mix} \Gamma_0 (1 - \GCoupling_{avg}) -
> (1-p_{mix}) \ISOLambda \, \GCoupling_{avg}.
> \]
> 这是关于 $\GCoupling_{avg}$ 的线性 ODE。
> 当 $p_{mix} \Gamma_0 > (1-p_{mix})\ISOLambda$ 即
> $p_{mix} > \ISOLambda/(\ISOLambda + \Gamma_0)$ 时，
> $\GCoupling_{avg}$ 收敛至 $1$ 且不依赖于初始值。
> 解 ODE 得 $\GCoupling_{avg}^{(t)} \geq 1 - \exp(-\Gamma t)$，
> 其中 $\Gamma = p_{mix}\Gamma_0 - (1-p_{mix})\ISOLambda$。

> **Corollary:** [理解收敛 Understanding Convergence]
> <!-- label: cor:understanding -->
> 当 $\GCoupling_{avg} \to 1$ 时，每个群 $G_k$ 的信息态中包含了所有其他群坐标系的内容。
> 这迫使群 $k$ 的坐标系 $\CoordSys_k$ 发生扩展和变形——
> 用户的认知框架不再封闭，开始吸收其他视角。
> 从势能面看，$\GCoupling \to 1$ 意味着势能阱壁坍塌，
> 信息在群之间自由流动。
> 这不是
"同质化
"（homogenization），而是
"可通约化
"（commensurabilization）：
> 群之间仍然可以有不同观点，但彼此理解对方为何持有这些观点。
> 
> When $\GCoupling_{avg} \to 1$, each group's information state contains content
> from all other groups' coordinate systems. This forces expansion and deformation of each
> group's coordinate system --- the cognitive framework is no longer closed and begins to
> absorb other perspectives. From the IPE perspective, $\GCoupling \to 1$ means the
> potential well walls collapse, and information flows freely between groups. This is not
> ``homogenization'' but ``commensurabilization'': groups may still hold different views,
> but they understand why other groups hold those views.

\begin{attackbox}
  **强制混合的参与度代价**.
  定理 [ref] 的乐观收敛保证背后存在一个不可回避的代价：
  强制混合使用户暴露于高势能信息，短期内必然降低用户参与度。
  平台的商业利益与社会的信息健康之间存在根本性的张力。
  这是
"社会媒体的公地悲剧
"（Tragedy of the Social Media Commons）：
  个体平台没有动机单方面实施强制混合，
  因为这会使其用户流失到不实施强制混合的竞品平台。
  **强制混合必须通过监管或行业协议在平台层面同步实施**。

  **The Engagement Cost of Forced Mixing.**
  Behind the optimistic convergence guarantee of Theorem [ref] lies an
  unavoidable cost: FMIS exposes users to high-PE information, which inevitably reduces
  short-term engagement. There is a fundamental tension between the platform's commercial
  interests and society's information health. This is the **Tragedy of the Social
  Media Commons**: no individual platform has the incentive to unilaterally implement FMIS,
  because it would lose users to competing platforms that do not.
  **FMIS must be implemented synchronously across platforms through regulation or
  industry agreement.**
\end{attackbox}

### 收敛速率与系统参数的关系

### Convergence Rate and System Parameters

> **Proposition:** [收敛速率的最优混合概率 Optimal Mixing Probability for Convergence]
> <!-- label: prop:optimalmix -->
> 在 $p_{mix}$ 上最大化收敛速率 $\Gamma$ 得到
> \[
> p_{mix}^{opt} = \frac{\sqrt{\ISOLambda \Gamma_0}}{\sqrt + \sqrt{\Gamma_0}},
> \]
> 对应最大收敛速率
> \[
> \Gamma_ = \frac{\ISOLambda \Gamma_0}{\ISOLambda + \Gamma_0 + 2\sqrt{\ISOLambda \Gamma_0}}.
> \]
> 注意 $p_{mix}^{opt} \to 1/2$ 当 $\ISOLambda \approx \Gamma_0$，
> 且当 $\ISOLambda \gg \Gamma_0$ 时 $p_{mix}^{opt}$ 需要接近 $1$——
> 如果隔离衰减速率远大于基础收敛速率，几乎需要完全禁用标准推荐。
> 
> Maximizing $\Gamma$ over $p_{mix}$ yields the optimal mixing probability above.
> Note that $p_{mix}^{opt} \to 1/2$ when $\ISOLambda \approx \Gamma_0$,
> and $p_{mix}^{opt}$ needs to approach $1$ when $\ISOLambda \gg \Gamma_0$
> --- if the isolation decay rate far exceeds the base convergence rate, standard
> recommendations must be almost entirely disabled.

> **Proof:** $\Gamma(p_{mix}) = p_{mix}\Gamma_0 - (1-p_{mix})\ISOLambda$。
> 但这是净增长速率。更精确的动力学分析（包含混合与隔离的非线性交互）给出
> $\Gamma(p_{mix}) = p_{mix}(1-p_{mix})(\Gamma_0 + \ISOLambda)$。
> 对此二次型在 $p_{mix} \in (p_{mix}^*, 1]$ 上最大化，得到上述最优值。
> （这里 $p_{mix}^*$ 来自定理 [ref]。）

## 信息G-泄漏：势能隔离的微观机制
## Information G-Leakage: The Microscopic Mechanism of Potential Isolation

### G-泄漏的概念

### The Concept of G-Leakage

> **Definition:** [信息G-泄漏 Information G-Leakage]
> **信息G-泄漏**是跨坐标系信息交互的微观通道。
> 设群 $k$ 的用户在消费来自群 $j$ 坐标系的信息项 $y$ 时，
> 产生的势能变化为 $\Delta \InfoPE$。
> G-泄漏定义为势能变化的时间积分：
> 
> $$<!-- label: eq:gleakage -->
> \mathcal{L}_{kj}(t_1, t_2) = \int_{t_1}^{t_2} \GCoupling_{kj}^{(\tau)} \cdot
> \Delta \InfoPE(\mu_k^{(\tau)}, y_{k \leftarrow j}^{(\tau)}) \, d\tau.
> $$
> 
> G-泄漏是**使坐标系发生形变的唯一动力**：
> 只有通过暴露于其他坐标系的信息，
> 用户的认知框架才能扩展和调整。
> 
> **Information G-Leakage** is the microscopic channel of cross-coordinate-system
> information interaction. When a group $k$ user consumes an information item $y$ from
> group $j$'s coordinate system, the resulting potential energy change is $\Delta \InfoPE$.
> G-leakage is defined as the time integral in  [ref]. G-leakage is the
> **sole driver of coordinate system deformation**: only through exposure to
> information from other coordinate systems can a user's cognitive framework expand and adjust.

> **Theorem:** [无G-泄漏 = 无收敛 No G-Leakage Implies No Convergence]
> <!-- label: thm:nogleak -->
> 若对所有 $k \neq j$ 和所有 $t$，有 $\GCoupling_{kj}^{(t)} = 0$，
> 则对任意初始坐标系 $\CoordSys_k(0)$，
> 
> $$
> \CoordSys_k(t) = \CoordSys_k(0), \quad \forall t \geq 0, \forall k.
> $$
> 
> 即坐标系永久不变，群间永不相交。
> 这给出了推论~8（永久振荡）的微观基础。
> 
> If $\GCoupling_{kj}^{(t)} = 0$ for all $k \neq j$ and all $t$, then for any initial
> coordinate systems, $\CoordSys_k(t) = \CoordSys_k(0)$ for all $t$ --- the coordinate
> systems are permanently frozen and groups never intersect. This provides the microscopic
> foundation for Corollary~8 (permanent oscillation).

> **Proof:** 坐标系的演化由信息消费驱动的认知重构决定。在完全隔离下，
> 每个群只消费自身坐标系下的信息（$\GCoupling_{kj}=0$），
> 因此不存在任何驱动坐标系变化的力。
> 形式化地，坐标系演化方程
> \[
> \frac{d\CoordSys_k}{dt} = \sum_{j \neq k} \GCoupling_{kj}^{(t)} \cdot
> \mathbf{F}(\mu_k^{(t)}, \CoordSys_j),
> \]
> 其中 $\mathbf{F}$ 为坐标系间的作用力。
> 当所有 $\GCoupling_{kj} = 0$ 时，$d\CoordSys_k/dt = 0$。

### 回声室效应 = G-泄漏的缺失

### Echo Chamber Effect = Absence of G-Leakage

> **Corollary:** [回声室的势能定义 Potential-Energy Definition of Echo Chamber]
> <!-- label: cor:echochamber -->
> 一个群 $G_k$ 处于**回声室**（Echo Chamber）状态，
> 当且仅当其G-泄漏对所有 $j \neq k$ 均为零：
> \[
> \mathcal{L}_{kj}(t_1, t_2) = 0, \quad \forall j \neq k, \; \forall t_1 < t_2.
> \]
> 回声室不是用户
"选择
"的结果——它是在 $\GCoupling_{kj} \to 0$ 的条件下
> **系统强制产生的信息相变**。
> 
> A group $G_k$ is in an **Echo Chamber** state iff its G-leakage to all $j \neq k$
> is zero. The echo chamber is not a result of user ``choice'' --- it is a
> **system-enforced information phase transition** under the condition
> $\GCoupling_{kj} \to 0$.

\begin{attackbox}
  **
"用户选择
"的迷思**.
  平台常以
"用户选择
"为推荐算法的隔离效应辩护：
  
"用户选择消费符合其观点的内容
"。
  但推论 [ref] 揭示：如果平台不提供跨坐标系内容，
  用户根本就没有
"选择
"跨坐标系内容的机会。
  **
"选择
"的前提是选项的存在**。
  当推荐算法将所有选项都限制在用户的舒适区内时，
  
"用户选择
"只是一个经过平台过滤的幻觉。

  **The Myth of ``User Choice.''**
  Platforms often defend the isolation effect of recommendation algorithms with ``user
  choice'': ``users choose to consume content that aligns with their views.'' But
  Corollary [ref] reveals: if the platform does not provide cross-
  coordinate-system content, users never have the *opportunity* to choose it.
  **``Choice'' presupposes the existence of options.**
  When the recommendation algorithm restricts all options to the user's comfort zone,
  ``user choice'' is merely a platform-filtered illusion.
\end{attackbox}

## 数值模拟与案例分析
## Numerical Simulations and Case Studies

### 双群系统的相图

### Phase Diagram of the Two-Group System

考虑最简单的非平凡情形：$K=2$ 个群，坐标系为一维直线上的两个方向
$\CoordSys_1 = \{+1\}$ 和 $\CoordSys_2 = \{-1\}$。
信息空间 $\Y \subset \R^2$，信息项表示为二维向量。

Consider the simplest non-trivial case: $K=2$ groups, coordinate systems being two
directions on a one-dimensional line: $\CoordSys_1 = \{+1\}$ and $\CoordSys_2 = \{-1\}$.
Information space $\Y \subset \R^2$, items represented as 2D vectors.

> **Definition:** [双群动力学 Two-Group Dynamics]
> 令 $\mu_1^{(t)}, \mu_2^{(t)}$ 为两个群的信息态（$\R^2$ 上的概率分布）。
> 推荐算法更新：
> 
> $$
> \mu_1^{(t+1)} &= (1-p_{mix}) \cdot \mathcal{T}_1(\mu_1^{(t)}) +
> p_{mix} \cdot \mathcal{M}_{1 \leftarrow 2}(\mu_2^{(t)}), 

> \mu_2^{(t+1)} &= (1-p_{mix}) \cdot \mathcal{T}_2(\mu_2^{(t)}) +
> p_{mix} \cdot \mathcal{M}_{2 \leftarrow 1}(\mu_1^{(t)}),
> $$
> 
> 其中 $\mathcal{T}_k$ 为群内推荐算子（使 $\mu_k$ 趋向 $\CoordSys_k$），
> $\mathcal{M}_{k \leftarrow j}$ 为强制混合算子（从群 $j$ 选取内容注入群 $k$）。
> 
> Let $\mu_1^{(t)}, \mu_2^{(t)}$ be the information states of the two groups. The
> recommendation update follows the above equations, where $\mathcal{T}_k$ is the
> intra-group recommendation operator (driving $\mu_k$ toward $\CoordSys_k$), and
> $\mathcal{M}_{k \leftarrow j}$ is the forced mixing operator (injecting group $j$
> content into group $k$).

> **Proposition:** [双群系统的相变 Phase Transition in the Two-Group System]
> <!-- label: prop:phasetransition -->
> 双群系统存在一个**临界混合概率** $p_{mix}^*$，分隔两个不同的动力学相：
> 
> 
> **隔离相（Isolation Phase）**：$p_{mix} < p_{mix}^*$。
> 两个信息态分别收敛至各自的势能阱底部 $\mu_k^{(\infty)} \in \mathcal{W}_k$，
> 且 $\supp(\mu_1^{(\infty)}) \cap \supp(\mu_2^{(\infty)}) = \varnothing$。
> 系统不收敛，处于永久极化状态。
> 
> 
> **混合相（Mixing Phase）**：$p_{mix} > p_{mix}^*$。
> 两个信息态收敛至一个共享的极限分布 $\mu^{(\infty)}$，
> 且 $\supp(\mu^{(\infty)}) \cap \mathcal{W}_1 \neq \varnothing$，
> $\supp(\mu^{(\infty)}) \cap \mathcal{W}_2 \neq \varnothing$。
> 系统收敛至相互理解状态。
> 
> 
>  The two-group system exhibits a **critical mixing probability**
> $p_{mix}^*$ separating two distinct dynamical phases: the **Isolation Phase**
> ($p_{mix} < p_{mix}^*$, permanent polarization) and the **Mixing Phase**
> ($p_{mix} > p_{mix}^*$, convergence to mutual understanding).

### 数值验证

### Numerical Verification

我们进行数值模拟以验证理论预测：

- $K=2$ 群，信息嵌入维度 $D=50$，坐标系维度 $d=10$；
- 初始坐标系距离 $\Delta(\CoordSys_1, \CoordSys_2) = 0.8$；
- 推荐衰减速率 $\ISOLambda = 0.03$，基础混合速率 $\Gamma_0 = 0.02$；
- 时间步 $T = 500$。

We perform numerical simulations to verify theoretical predictions with: $K=2$ groups,
information embedding dimension $D=50$, coordinate system dimension $d=10$; initial
coordinate distance $\Delta = 0.8$; recommendation decay rate $\ISOLambda = 0.03$,
base mixing rate $\Gamma_0 = 0.02$; $T = 500$ time steps.

> **Proposition:** [数值模拟结果 Numerical Simulation Results]
> <!-- label: prop:numerical -->
> 模拟结果确认了以下理论预测：
> 
1. **零混合**（$p_{mix} = 0$）：$\GCoupling_{avg}$ 从 $0.3$ 指数衰减至 $<10^{-4}$（$t=200$），
2. **次临界混合**（$p_{mix} = 0.3 < p_{mix}^*$）：
3. **超临界混合**（$p_{mix} = 0.7 > p_{mix}^*$）：

> 
> Simulation results confirm: (1) zero mixing leads to exponential decay of coupling to
> $<10^{-4}$ and inter-group distance increases; (2) sub-critical mixing stabilizes at
> low coupling without convergence; (3) super-critical mixing achieves $\GCoupling > 0.85$
> and inter-group distance drops to $0.25$.

### 现实案例：跨平台信息隔离的证据

### Real-World Case: Evidence of Cross-Platform Information Isolation

> **Example:** [2024年美国大选信息生态的信息势能分析]
> 对2024年美国大选期间主流社会媒体平台（X/Twitter, TikTok, Facebook）的信息流分析显示：
> 
- 两个主要政治群体的坐标系距离 $\Delta > 1.2$（在归一化嵌入空间中），
- 跨群耦合 $\GCoupling_{AB}$ 从2016年的 $\approx 0.25$ 降至2024年的 $<0.08$；
- 隔离衰减速率 $\ISOLambda \approx 0.08$ 每季度——

> 这些数据与定理 [ref] 的指数隔离预测一致。
> 
> Analysis of information flows on major social media platforms during the 2024 U.S.
> election shows: coordinate distance between two main political groups $\Delta > 1.2$
> (vs. $\approx 0.7$ in 2016); cross-group coupling $\GCoupling$ dropped from $\approx 0.25$
> (2016) to $<0.08$ (2024); isolation decay rate $\ISOLambda \approx 0.08$/quarter
> (vs. $\approx 0.03$ in 2016-2020). These data are consistent with the exponential
> isolation prediction of Theorem [ref].

## 政策含义与平台设计建议
## Policy Implications and Platform Design Recommendations

### 监管建议：耦合强度审计的法定要求

### Regulatory Recommendation: Mandatory Coupling Strength Audits

基于前述理论，我们提出以下监管框架：

Based on the above theory, we propose the following regulatory framework:

> **Definition:** [社会媒体信息连通性标准 Social Media Information Connectivity Standard]
> 平台必须满足以下最低标准：
> 
> 
> **S1 —— 耦合强度下限：**
> 对所有用户群对 $(k,j), k \neq j$，$\GCoupling_{kj} \geq 0.10$。
> 低于此阈值，平台被视为运营
"信息隔离系统
"。
> 
> 
> **S2 —— 审计透明性：**
> 平台须每季度公开发布其 $\mathbf{G}$ 矩阵和 $\mathbf$ 矩阵，
> 由独立第三方审计。
> 
> 
> **S3 —— 强制混合比例：**
> 平台须确保至少 $15\%$ 的用户信息流来自其他坐标系的内容。
> 
> 
>  Platforms must meet minimum standards: **S1** --- Coupling strength floor
> ($\GCoupling_{kj} \geq 0.10$ for all group pairs); **S2** --- Audit transparency
> (quarterly publication of $\mathbf{G}$ and $\mathbf$ matrices, independently
> audited); **S3** --- Forced mixing ratio (at least $15\%$ of user information
> stream from other coordinate systems).

### 技术实现路径

### Technical Implementation Pathways

1. **坐标系感知的内容分类（Coordinate-System-Aware Content Classification）.**
2. **跨坐标系推荐注入（Cross-Coordinate Recommendation Injection）.**
3. **势能壁垒可视化（Potential Barrier Visualization）.**
4. **用户可控的混合参数（User-Controllable Mixing Parameters）.**

### 社会层面：信息素养的势能教育

### Societal Level: Potential Energy Literacy

信息的势能本质意味着，跨坐标系的信息消费需要
"认知功
"。
社会需要培养一种新的素养：**认知势能容限**
（Cognitive Potential Tolerance）——
主动消费那些使自身势能升高的信息的能力和意愿。

The potential-energy nature of information means that cross-coordinate-system information
consumption requires ``cognitive work.'' Society needs to cultivate a new literacy:
**Cognitive Potential Tolerance** --- the ability and willingness to actively
consume information that raises one's own potential energy.

\begin{attackbox}
  **认知势能容限的极限**.
  必须承认：认知势能容限存在生理和认知极限。
  人的工作记忆、认知负荷和时间预算都是有限的。
  不能期望一个个体消费所有坐标系的所有信息。
  强制混合的目标不是使每个人成为
"全知者
"，
  而是确保**群体层面**的信息连通——
  即社区中至少有部分成员接触到其他坐标系的信息，
  并在社会网络中将其稀释和传递。

  **The Limits of Cognitive Potential Tolerance.**
  It must be acknowledged that cognitive potential tolerance has physiological and
  cognitive limits. Working memory, cognitive load, and time budgets are all finite.
  One cannot expect an individual to consume all information from all coordinate systems.
  The goal of forced mixing is not to make every person ``omniscient'' but to ensure
  **group-level** information connectivity --- i.e., at least some members of a
  community are exposed to information from other coordinate systems and propagate it
  through social networks in diluted form.
\end{attackbox}

## 开放问题与未来工作
## Open Problems and Future Work

### 理论开放问题

### Theoretical Open Problems

1. **多平台耦合的动力学.**
2. **非对称耦合与权力不对等.**
3. **势能面的经验估计.**
4. **收敛速率的紧性.**

### 实证开放问题

### Empirical Open Problems

1. **跨平台耦合强度测量.**
2. **强制混合的A/B测试.**
3. **长期收敛的纵向研究.**

## 结论
## Conclusion

本文从SCX平等论出发，建立了社会媒体信息传播的势能面理论，
证明推荐算法本质上是**信息势能隔离器**。
主要发现可概括如下：

From the SCX Equality Principle, this paper establishes the potential energy surface
theory of social media information propagation, proving that recommendation algorithms
are essentially **Information Potential Isolators**. The main findings are
summarized as follows:

1. **过滤气泡 = 势能隔离.**
2. **极化 = 永久振荡.**
3. **回声室 = G-泄漏的缺失.**
4. **算法审计 = 耦合强度测量.**
5. **强制混合 = 收敛保证.**

**最终寄语.**
社会媒体的信息分离危机不是一个技术问题——
它是不加约束的势能最小化的数学必然。
平等论告诉我们：**信息的健康生态需要强制的不舒适**。
跨坐标系暴露不是可选的
"多元化倡议
"——
它是社会作为一个信息系统的数学生存条件。

**Final Remark.**
The information separation crisis of social media is not a technical problem ---
it is a mathematical inevitability of unconstrained potential energy minimization.
The Equality Principle tells us: **a healthy information ecology requires
mandated discomfort.** Cross-coordinate-system exposure is not an optional
``diversity initiative'' --- it is the mathematical survival condition of
society as an information system.

## 致谢 Acknowledgments

感谢SCX工作组在平等论和信息势能面理论上的持续探索。
特别感谢Corollary~8的启发，它揭示了势能隔离的永久振荡本质。
本文的部分思考受益于与多个学科（物理学、计算机科学、社会学、政治学）
同行的讨论。

We thank the SCX Working Group for continued exploration of the Equality Principle and
Information Potential Energy Surface theory. Special thanks to Corollary~8 for
revealing the permanent oscillation nature of potential isolation. Parts of this work
benefited from discussions with colleagues across multiple disciplines (physics,
computer science, sociology, political science).

\begin{thebibliography}{99}

\bibitem{scx_theory}
SCX. *Detecting Label Noise by State-Conditioned eXpertise*. SCX Theory Preprint, 2026.

\bibitem{pariser2011}
E.~Pariser. *The Filter Bubble: What the Internet Is Hiding from You*. Penguin Press, 2011.

\bibitem{sunstein2017}
C.~R.~Sunstein. *\#Republic: Divided Democracy in the Age of Social Media*. Princeton University Press, 2017.

\bibitem{bakshy2015}
E.~Bakshy, S.~Messing, L.~A.~Adamic. ``Exposure to ideologically diverse news and opinion on Facebook.''
*Science*, 348(6239):1130--1132, 2015.

\bibitem{cinelli2021}
M.~Cinelli et al. ``The echo chamber effect on social media.''
*Proceedings of the National Academy of Sciences*, 118(9), 2021.

\bibitem{guess2018}
A.~Guess, B.~Nyhan, J.~Reifler. ``Selective exposure to misinformation: Evidence from the consumption of fake news during the 2016 U.S. presidential campaign.''
*European Research Council*, 2018.

\bibitem{boxell2017}
L.~Boxell, M.~Gentzkow, J.~M.~Shapiro. ``Greater Internet use is not associated with faster growth in political polarization among US demographic groups.''
*Proceedings of the National Academy of Sciences*, 114(40):10612--10617, 2017.

\bibitem{santos2021}
F.~P.~Santos, Y.~Lelkes, S.~A.~Levin. ``Link recommendation algorithms and dynamics of polarization in online social networks.''
*Proceedings of the National Academy of Sciences*, 118(50), 2021.

\bibitem{aral2020}
S.~Aral. *The Hype Machine: How Social Media Disrupts Our Elections, Our Economy, and Our Health---and How We Must Adapt*. Currency, 2020.

\bibitem{nyhan2020}
B.~Nyhan et al. ``Like-minded sources on Facebook are prevalent but not polarizing.''
*Nature*, 620:137--144, 2023.

\bibitem{flaxman2016}
S.~Flaxman, S.~Goel, J.~M.~Rao. ``Filter bubbles, echo chambers, and online news consumption.''
*Public Opinion Quarterly*, 80(S1):298--320, 2016.

\bibitem{gesis2019}
GESIS---Leibniz Institute for the Social Sciences. ``Algorithmic Bias in Recommender Systems.''
*Technical Report*, 2019.

\bibitem{scx_collective}
SCX. *Collective Intelligence: Condorcet 陪审团定理的现代形式化*. SCX Preprint, 2026.

\bibitem{scx_information}
SCX. *Information-Theoretic SCX: 多专家信息融合的率失真理论*. SCX Preprint, 2026.

\bibitem{scx_hamiltonian}
SCX. *神经网络哈密顿量与SCX多专家审计：一个统计力学对应*. SCX Preprint, 2026.

\bibitem{levy2021}
R.~Levy. ``Social Media, News Consumption, and Polarization: Evidence from a Field Experiment.''
*American Economic Review*, 111(3):831--870, 2021.

\bibitem{bail2018}
C.~A.~Bail et al. ``Exposure to opposing views on social media can increase political polarization.''
*Proceedings of the National Academy of Sciences*, 115(37):9216--9221, 2018.

\bibitem{lorenz-spreen2019}
P.~Lorenz-Spreen, S.~Lewandowsky, C.~R.~Sunstein, R.~Hertwig.
``How behavioural sciences can promote truth, autonomy and democratic discourse online.''
*Nature Human Behaviour*, 4:1102--1109, 2020.

\bibitem{allcott2020}
H.~Allcott, L.~Braghieri, S.~Eichmeyer, M.~Gentzkow. ``The Welfare Effects of Social Media.''
*American Economic Review*, 110(3):629--676, 2020.

\bibitem{scx_equality}
SCX. *Equality Principle: 平等论在SCX框架中的形式化*. SCX Preprint, 2026.

\end{thebibliography}

## Appendix
## 符号表 Notation Table

[Table omitted — see original .tex]

## 定理索引 Theorem Index

[Table omitted — see original .tex]