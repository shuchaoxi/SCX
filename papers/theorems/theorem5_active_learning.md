# Introduction

**Author:** SCX

*Abstract:*

We derive the optimal sampling distribution and a closed-form optimal sampling
rate for active learning when the objective is to maximize expected $F_1$ gain.
Starting from the Cercis Score $S(x)=Q(x)+\eta\,N(x)$, which decomposes
sample value into a *quality* component $Q(x)$ (model confidence,
correctness proxy) and a *novelty* component $N(x)$ (information
diversity, coverage gain), we formulate the batch active learning problem as
a constrained variational optimization over the sampling distribution
$p(x)$.  The principal result is a closed-form expression for the optimal
sampling rate
\[
\rho^* = \frac{\eta\sum_{k} w_k\,\overline_k}
         {\eta\sum_{k} w_k\,\overline_k
          + \sum_{k} w_k\,\V[\Gamma_k]},
\]
where $\Gamma_k$ is the per-class expected $F_1$ gain, $\V[\Gamma_k]$ its
variance, and $w_k$ are class weights.  The theorem provides a principled,
hyperparameter-free rule for deciding *how many* samples to draw and
*which* samples to select.  We prove consistency of the estimator and
demonstrate that the Cercis-optimal policy interpolates between pure
uncertainty sampling ($\eta\to0$) and pure diversity sampling
($\eta\to\infty$).  Numerical experiments on benchmark datasets confirm that
the closed-form rate tracks the empirical optimal budget closely, reducing
annotation cost by 15--40\% compared to fixed-budget heuristics.

## Introduction

Active learning seeks to maximize model performance while minimizing the
number of labeled examples by selecting the most informative instances for
annotation [cite].  The field has produced a rich family of
query strategies: uncertainty sampling [cite],
query-by-committee [cite], expected error
reduction [cite], and density-weighted
methods [cite].  Despite this diversity, two fundamental
questions remain partially open:

1. **Which** samples should be selected? — the *ranking*
2. **How many** samples should be selected? — the *budget*

Most existing work treats the budget as an exogenous hyperparameter and
concentrates exclusively on the ranking problem.  In this paper we address
both questions simultaneously within a unified variational framework built on
the **Cercis Score**.

**The Cercis Score.**
Introduced in the SCX framework [cite], the Cercis Score
assigns to each unlabeled instance $x$ a scalar value

$$<!-- label: eq:cercis-def -->
    S(x) = Q(x) + \eta\,N(x),
$$

where $Q(x)\in[0,1]$ measures *quality* — the model's (inverse)
confidence or expected correctness improvement from labeling $x$ — and
$N(x)\in[0,1]$ measures *novelty* — the dissimilarity of $x$ to
already-labeled instances.  The hyperparameter $\eta\geq0$ controls the
exploration--exploitation trade-off.  The Cercis Score unifies several
popular acquisition functions as special cases: uncertainty sampling
($\eta=0$), diversity sampling ($\eta\to\infty$), and their convex
combinations for finite $\eta$.

**Contributions.**

1. We formulate active learning as maximizing expected $F_1$ gain
2. We derive a closed-form expression for the optimal sampling rate
3. We prove that the empirical plug-in estimator of $\rho^*$ is
4. We show that $\rho^*$ recovers known limits: $\rho^*\to0$ as

## Preliminaries

### Notation

Let $\cX$ be the instance space and $\cY=\{1,...,K\}$ the label space.
The unlabeled pool is $\cD_U=\{x_i\}_{i=1}^{N_U}$ drawn i.i.d.\ from an
unknown distribution $P_X$.  A classifier $h_\theta:\cX\to\Delta^{K-1}$
(outputting a probability simplex) is trained on a labeled set
$\cD_L\subset\cX\times\cY$.  The active learning loop proceeds in rounds
$t=1,2,...,T$; at each round a batch $B_t\subset\cD_U$ is selected,
labeled by an oracle, and added to $\cD_L$.

**$F_1$ score.**
For multi-class problems, the macro-averaged $F_1$ is

$$<!-- label: eq:f1-def -->
    F_1 = \frac{1}{K}\sum_{k=1}^{K}
    \frac{2\,Prec_k\cdotRec_k}{Prec_k+Rec_k},
$$

where $Prec_k$ and $Rec_k$ are per-class precision and recall
on a held-out test set.

**Cercis components.**
For an instance $x$, let $\hat{p}_\theta(y\mid x)$ be the model's predictive
distribution.  We define

$$
    Q(x) &= 1 - \max_{y}\,\hat{p}_\theta(y\mid x),
           <!-- label: eq:quality --> 
    N(x) &= \min_{x'\in\cD_L} d(x,x'),
           <!-- label: eq:novelty -->
$$

where $d(\cdot,\cdot)$ is a suitable metric on $\cX$ (e.g., Euclidean
distance in a representation space).  Both $Q$ and $N$ are normalized to
$[0,1]$.  The Cercis Score is then $S(x)=Q(x)+\eta N(x)$ with
$\eta\geq0$.

### Expected $F_1$ Gain

After labeling instance $x$ with true label $y$, the model is updated from
$\theta$ to $\theta'=\theta'(x,y)$.  The resulting change in $F_1$ on the
test distribution is

$$<!-- label: eq:gain -->
    \Gamma(x,y) = F_1(\theta') - F_1(\theta).
$$

Since the true label $y$ is unknown before querying, the *expected*
$F_1$ gain is

$$<!-- label: eq:expected-gain -->
    \overline(x) =
    \E_{y\sim\hat{p}_\theta(\cdot\mid x)}[\Gamma(x,y)].
$$

**Per-class decomposition.**
For macro-averaged $F_1$, the gain decomposes across classes:

$$<!-- label: eq:decomp -->
    \overline(x) =
    \frac{1}{K}\sum_{k=1}^{K} \overline_k(x),
$$

where $\overline_k(x)$ is the expected improvement in class-$k$
$F_1$.  We write

$$<!-- label: eq:class-gain-moments -->
    \overline_k = \E_{x\sim P_X}[\overline_k(x)],\qquad
    \V[\Gamma_k] = \V_{x\sim P_X}[\overline_k(x)].
$$

## Variational Formulation

We cast batch active learning as finding a sampling distribution
$p\in\Delta(\cD_U)$ over the unlabeled pool that maximizes expected $F_1$
gain while remaining close to a prior $\pi$ (e.g., the uniform distribution
or the raw density $P_X$).  The ``closeness'' penalty, implemented via KL
divergence, prevents the sampling distribution from collapsing onto a few
atypical high-gain points and stabilizes finite-sample estimation.

> **Definition:** [Cercis-Regularized Objective]
> <!-- label: def:objective -->
> Given a prior $\pi\in\Delta(\cD_U)$ and a regularization parameter
> $\lambda>0$, the optimal sampling distribution solves
> 
> $$<!-- label: eq:variational -->
>     p^* = \argmax_{p\in\Delta(\cD_U)}\;
>     \E_{x\sim p}\big[\overline(x)\big]
>     \;-\; \lambda\,\KL(p\,\|\,\pi).
> $$

The KL-regularized objective [ref] is concave in $p$ (the
entropy term $-\KL(p\|\pi)$ is concave; the linear expectation is
affine), so the maximizer is unique and characterized by first-order
optimality conditions.

> **Lemma:** [Gibbs形式的最优采样分布]
> <!-- label: lem:gibbs -->
> 在 A3（有界损失）下，变分问题 [ref] 的解为：
> 
> $$<!-- label: eq:gibbs-sol -->
>     p^*(x) = \frac{\pi(x)\,\exp\!\big(\overline(x)/\lambda\big)}
>                   {Z(\lambda)},
> $$
> 
> 其中 $Z(\lambda)=\sum_{x\in\cD_U}\pi(x)\,
> \exp\big(\overline(x)/\lambda\big)$。

> **Proof:** **严格性等级:** \rigorous \quad（在 A3 下，无需额外公理）
> 
> **所需公理:** A3（有界损失 $\ell\in[0,B]$，保证 $\overline(x)$ 有界）
> 
> 考虑定义在概率单纯形 $\Delta(\cD_U)$ 上的泛函
> \[
> F(p) = \E_{x\sim p}[\overline(x)] - \lambda\,\KL(p\|\pi),\quad p\in\Delta(\cD_U),\;\lambda>0.
> \]
> 
> **步骤1: 严格凹性验证.**
> 将 $F(p)$ 分解为线性项 $L(p)=\E_p[\overline]$ 和正则项 $R(p)=-\lambda\KL(p\|\pi)$。
> KL散度 $\KL(p\|\pi)=\sum_x p(x)\log(p(x)/\pi(x))$ 关于 $p$ 是**严格凸**的（由Jensen不等式，对任意 $p_1\neq p_2\in\Delta(\cD_U)$ 和 $t\in(0,1)$ 有严格不等式），因此 $-\KL(p\|\pi)$ 严格凹。线性项 $L(p)$ 既是凸的也是凹的。严格凹函数之和仍严格凹，故 $F(p)$ 在 $\Delta(\cD_U)$ 上严格凹。
> 
> 等价的Hessian验证：将 $p$ 视为 $\mathbb{R}^{|\cD_U|}$ 中向量，在概率单纯形内部有：
> \[
> \frac{\partial F}{\partial p(x)} = \overline(x)
> - \lambda\Big(\log\frac{p(x)}{\pi(x)}+1\Big),\qquad
> \frac{\partial^2 F}{\partial p(x)\partial p(x')} = -\frac{p(x)}\delta_{xx'}.
> \]
> Hessian为对角矩阵，对角元 $-\lambda/p(x)<0$（因 $\lambda>0,\;p(x)>0$），故负定，$F$ 严格凹。
> 
> **步骤2: 拉格朗日乘子法.**
> 引入等式约束 $\sum_x p(x)=1$ 的Lagrange乘子 $\mu$：
> \[
> \mathcal{L}(p,\mu) = \sum_x p(x)\overline(x)
> - \lambda\sum_x p(x)\log\frac{p(x)}{\pi(x)}
> - \mu\Big(\sum_x p(x)-1\Big).
> \]
> 
> KKT条件（Slater条件成立，因约束仿射且概率单纯形内部非空）：
> 
> $$
> \frac{\partial\mathcal{L}}{\partial p(x)}
> &= \overline(x)
> - \lambda\Big(\log\frac{p(x)}{\pi(x)}+1\Big) - \mu = 0,\quad \forall x,

> \frac{\partial\mathcal{L}}{\partial\mu}
> &= \sum_x p(x) - 1 = 0.
> $$
> 
> 
> 由第一个方程：
> \[
> \overline(x) - \lambda - \mu = \lambda\log\frac{p(x)}{\pi(x)},
> \quad\Rightarrow\quad
> \log\frac{p(x)}{\pi(x)} = \frac{\overline(x)} - 1 - \frac,
> \]
> \[
> p(x) = \pi(x)\exp\!\Big(\frac{\overline(x)}\Big)
> \cdot\exp\!\Big(-1-\frac\Big).
> \]
> 
> 令 $A = \exp(-1-\mu/\lambda)$，得 $p(x) = A\,\pi(x)\exp(\overline(x)/\lambda)$。
> 由归一化条件 $\sum_x p(x)=1$：
> \[
> A\sum_x \pi(x)\exp(\overline(x)/\lambda) = 1,\quad
> A = \frac{1}{Z(\lambda)},\quad
> Z(\lambda)=\sum_x \pi(x)\exp\!\Big(\frac{\overline(x)}\Big).
> \]
> 
> 故：
> \[
> p^*(x) = \frac{\pi(x)\exp(\overline(x)/\lambda)}{Z(\lambda)}.
> \]
> 
> **步骤3: 唯一性.**
> 由 $F(p)$ 的严格凹性，KKT条件是全局极大值的充分必要条件，$p^*$ 是唯一全局极大值点。

### Connecting the Cercis Score to $F_1$ Gain

The central empirical observation motivating our work is that the expected
$F_1$ gain is well approximated by an affine function of the Cercis Score:

\begin{assumption}[Cercis--Gain Affinity]
<!-- label: ass:affinity -->
There exist constants $\alpha>0,\beta\in\R$ such that

$$<!-- label: eq:affinity -->
    \overline(x) = \alpha\,S(x) + \beta
    = \alpha\big(Q(x)+\eta N(x)\big) + \beta,
$$

with approximation error bounded by
$\E[(\overline(x)-\alpha S(x)-\beta)^2]\leq\varepsilon_0^2$.
\end{assumption}

Assumption [ref] is supported by the following intuition: (i)
$Q(x)$ captures model uncertainty — high-uncertainty points yield larger
information gains; (ii) $N(x)$ captures representational diversity —
sampling diverse regions prevents redundant information; (iii) the affine
form emerges from a first-order Taylor expansion of the $F_1$ surface around
the current model parameters [cite].  In the SCX framework, this
affinity is formalized as a structural property of the Cercis operator; we
treat it as an empirically verifiable modeling choice.

Under Assumption [ref], the Gibbs distribution [ref]
becomes

$$<!-- label: eq:p-star -->
    p^*(x) \propto \pi(x)\,
    \exp\!\Big(\frac\big(Q(x)+\eta N(x)\big)\Big).
$$

## Main Results

### Optimal Sampling Distribution

> **Theorem:** [最优采样分布（Gibbs形式）]
> <!-- label: thm:optimal-dist -->
> 设 $\pi$ 为 $\cD_U$ 上的先验分布，$\lambda>0$ 为正则化参数，$S(x)=Q(x)+\eta N(x)$ 为 Cercis Score。在 A1--A6 及 Assumption [ref] 下，变分问题 [ref] 的唯一最大化器为：
> 
> $$<!-- label: eq:thm-dist -->
>     p^*(x) = \frac{1}{Z_\eta}\,
>     \pi(x)\,\exp\!\Big(\fracS(x)\Big),
> $$
> 
> 其中 $Z_\eta=\sum_{x}\pi(x)\exp(\alpha S(x)/\lambda)$。此外：
> 
1. 当 $\lambda\to\infty$ 时，$p^*\to\pi$（退化为先验均匀采样）；
2. 当 $\lambda\to0$ 时，$p^*\to\delta_{x^*}$，
3. 对任意 $\lambda\in(0,\infty)$，$\KL(p^*\|\pi)$ 关于 $\lambda$ 严格递减。

\begin{proof}
**严格性等级:** \rigorous \quad（在 A1--A6、Assumption [ref] 下）

**所需公理:** A3（有界损失），Assumption [ref]（Cercis-Gain 仿射关系）

**存在性与唯一性.**
由 Lemma [ref]，目标泛函
\[
F(p)=\E_p[\overline] - \lambda\KL(p\|\pi)
\]
在 $\Delta(\cD_U)$ 上严格凹，KKT 条件给出唯一解：
\[
p^*(x) = \frac{\pi(x)\exp(\overline(x)/\lambda)}{Z(\lambda)}.
\]
代入 Assumption [ref] 的仿射关系 $\overline(x)=\alpha S(x)+\beta$：
\[
\exp(\overline(x)/\lambda) = \exp(\beta/\lambda)\cdot\exp(\alpha S(x)/\lambda).
\]
常数因子 $\exp(\beta/\lambda)$ 在归一化时被吸收，故：
\[
p^*(x) = \frac{1}{Z_\eta}\,\pi(x)\,\exp\!\Big(\fracS(x)\Big),\quad
Z_\eta = \sum_x \pi(x)\exp(\alpha S(x)/\lambda).
\]

**极限性质 (i): $\lambda\to\infty$.**
当 $\lambda\to\infty$，对任意 $x$ 有 $\alpha S(x)/\lambda\to 0$，故 $\exp(\alpha S(x)/\lambda)\to 1$。于是：
\[
Z_\eta \to \sum_x \pi(x) = 1,\qquad p^*(x) \to \pi(x).
\]

**极限性质 (ii): $\lambda\to 0$.**
设 $S^* = \max_x S(x)$，$\cD^* = \{x: S(x)=S^*\}$。
对任意 $x\notin\cD^*$，存在 $\delta>0$ 使 $S(x)\le S^*-\delta$，则：
\[
\frac{\exp(\alpha S(x)/\lambda)}{\sum_{x'}\pi(x')\exp(\alpha S(x')/\lambda)}
\le \frac{\exp(\alpha(S^*-\delta)/\lambda)}{\pi_\exp(\alpha S^*/\lambda)}
= \frac{\exp(-\alpha\delta/\lambda)}{\pi_} \xrightarrow{\lambda\to0} 0,
\]
其中 $\pi_=\min_x\pi(x)>0$（假设 $\pi$ 在 $\cD_U$ 上严格正）。
对 $x\in\cD^*$，$p^*(x)\to \pi(x)/\sum_{x'\in\cD^*}\pi(x')$。
当 $|\cD^*|=1$ 时，$p^*\to\delta_{x^*}$。

**性质 (iii): $\KL(p^*\|\pi)$ 的单调性.**
记 $q_\lambda = p^*$，即 $q_\lambda(x) = \pi(x)\exp(\overline(x)/\lambda)/Z(\lambda)$。
则：
\[
\KL(q_\lambda\|\pi) = \sum_x q_\lambda(x)\log\frac{q_\lambda(x)}{\pi(x)}
= \frac{\E_{q_\lambda}[\overline]} - \log Z(\lambda).
\]

对 $\lambda$ 求导。首先计算：
\[
\frac{\partial Z}{\partial\lambda}
= \sum_x \pi(x)\exp\!\Big(\frac{\overline(x)}\Big)\cdot\Big(-\frac{\overline(x)}{\lambda^2}\Big)
= -\frac{Z}{\lambda^2}\E_{q_\lambda}[\overline],
\]
故 $\frac{1}{Z}\frac{\partial Z}{\partial\lambda} = -\frac{\E_{q_\lambda}[\overline]}{\lambda^2}$。

其次，$q_\lambda$ 对 $\lambda$ 的微分：
\[
\frac{\partial q_\lambda(x)}{\partial\lambda}
= q_\lambda(x)\,\frac{\E_{q_\lambda}[\overline]-\overline(x)}{\lambda^2}.
\]

因此：
\[
\frac{\partial\lambda}\E_{q_\lambda}[\overline]
= \sum_x \overline(x)\,\frac{\partial q_\lambda(x)}{\partial\lambda}
= \frac{1}{\lambda^2}\Big(\E_{q_\lambda}[\overline]^2 - \E_{q_\lambda}[\overline^2]\Big)
= -\frac{\V_{q_\lambda}[\overline]}{\lambda^2}.
\]

综合：

$$
\frac{\partial\lambda}\KL(q_\lambda\|\pi)
&= \frac{\partial\lambda}\Big(\frac{\E[\overline]}\Big)
- \frac{\partial\lambda}\log Z(\lambda) 

&= \frac{-\V/\lambda^2\cdot\lambda - \E[\overline]}{\lambda^2}
+ \frac{\E[\overline]}{\lambda^2}
= -\frac{\V_{q_\lambda}[\overline]}{\lambda^3}.
$$

由于 $\V_{q_\lambda}[\overline]\ge 0$，且等号仅当 $\overline$ 在 $q_\lambda$ 下为常数时成立（平凡情形），一般有 $\V>0$，故：
\[
\frac{\partial\lambda}\KL(p^*\|\pi) < 0,
\]
即 $\KL(p^*\|\pi)$ 关于 $\lambda$ 严格递减。$\square$

\begin{critique}

1. Assumption [ref]（Cercis-Gain仿射关系）是本定理最关键的未验证假设。线性关系 $\overline(x)=\alpha S(x)+\beta$ 虽受一阶Taylor展开启发，但其精确度和误差界 $\varepsilon_0$ 在实践中需逐数据集验证。
2. 极限 (ii) 要求 $\pi$ 在全局最大值点处有正概率质量，否则集中点集需修正为 $\cD^*$ 中 $\pi$ 支集的子集。若最大值不唯一，$p^*$ 集中在 $\cD^*$ 上的条件分布，而非单点 $\delta_{x^*}$。
3. 性质 (iii) 的导数恒负性要求 $\V_{q_\lambda}[\overline]>0$；当 $\overline(x)$ 在 $\cD_U$ 上为常数时，$\KL(p^*\|\pi)=0$ 恒成立，此时 $\lambda$ 不影响采样分布。

\end{critique}

**Applications:**
Theorem [ref] provides the optimal sampling distribution for
active learning under any continuously differentiable acquisition objective.
Practitioners can use the Gibbs-form distribution $p^*(x)$ with their preferred
prior $\pi$ and Cercis Score $S(x)$ to perform importance-weighted sampling of
the unlabeled pool.  In cold-start active learning where no labeled data exists,
setting $\pi$ to the uniform distribution and $\lambda$ large recovers random
sampling as a safe default.  In fine-tuning scenarios with a pre-existing labeled
set, $\pi$ can be set to the empirical density of already-labeled instances,
ensuring the new batch complements rather than duplicates existing annotations.
The $\lambda$-tunable interpolation between uniform and hard-max sampling enables
practitioners to control the exploration--exploitation balance without modifying
the underlying Cercis Score computation.

### Closed-Form Optimal Sampling Rate

The sampling *distribution* $p^*$ determines relative selection
probabilities.  The sampling *rate* $\rho^*\in[0,1]$ determines the
fraction of the unlabeled pool to query.  We derive $\rho^*$ by an
expected-value-of-information argument.

**Setup.**
Consider a batch of size $B=\rho N_U$ drawn i.i.d.\ from $p^*$.
The total expected $F_1$ gain is

$$<!-- label: eq:total-gain -->
    G(\rho) = \E\Big[\sum_{i=1}^{\rho N_U} \overline(x_i)\Big]
    = \rho N_U\sum_{k=1}^K w_k\overline_k,
$$

where $w_k=1/K$ for macro-averaging (or arbitrary class weights for
weighted $F_1$).

The *cost* of sampling arises from annotation expense and from the
risk of labeling instances whose gain realizations fall below expectation.
The expected shortfall (downside risk) for class $k$ is proportional to
the variance $\V[\Gamma_k]$.  We formalize this through the Cercis novelty
trade-off: each sampled instance incurs a novelty ``debt'' because it
reduces the unexplored region, diminishing future gains.  This
debt is priced at $\eta$ per unit of novelty consumed.

> **Theorem:** [最优采样率闭式解]
> <!-- label: thm:optimal-rate -->
> 在 A1--A6 及 Assumption [ref] 下，最大化风险调节后期望 $F_1$ 增益的最优采样率为
> 
> $$<!-- label: eq:rho-star -->
>     \boxed{\;
>     \rho^* =
>     \frac{\eta\sum_{k=1}^{K} w_k\,\overline_k}
>          {\eta\sum_{k=1}^{K} w_k\,\overline_k
>           + \sum_{k=1}^{K} w_k\,\V[\Gamma_k]}
>     \;},
> $$
> 
> 其中 $\overline_k=\E[\overline_k(x)]$ 为类平均增益，
> $\V[\Gamma_k]=\E[(\overline_k(x)-\overline_k)^2]$ 为类内增益方差，
> $w_k\geq0$ 满足 $\sum_k w_k=1$ 为类重要性权重。

\begin{proof}
**严格性等级:** \conditionallyrigorous
\quad（在 A1--A6、Assumption [ref] 及下述额外建模假设下）

**所需公理:** A3（有界损失），A4（均匀独立噪声），A5（状态同质性），
Assumption [ref]

**总体框架.**
给定采样率 $\rho\in[0,1]$，批大小 $B=\rho N_U$。
从 Theorem [ref] 的最优分布 $p^*$ 中不放回抽取 $B$ 个样本，
总 $F_1$ 增益为：
\[
G_{total}(\rho) = \sum_{i=1}^B \overline(x_i)
= \sum_{i=1}^B \sum_{k=1}^K w_k\,\overline_k(x_i).
\]

**步骤1: 期望总增益.**
记 $G = \E_{p^*}[\overline] = \sum_k w_k\overline_k$。
忽略放回效应，期望总增益为：
\[
\E[G_{total}(\rho)] = B\cdot G = \rho N_U G.
\]

**步骤2: 边际收益递减（二阶展开）.**
不放回采样导致已被选中的高增益点不再出现在候选池中，边际增益随 $\rho$ 递减。
将期望总增益视为 $\rho$ 的函数 $T(\rho)$，在 $\rho=0$ 处 Taylor 展开：
\[
T(\rho) = T(0) + T'(0)\rho + \tfrac12 T''(0)\rho^2 + o(\rho^2).
\]
显然 $T(0)=0$，$T'(0)=N_U G$。

在均匀衰减模型下（排序后的第 $t$ 个样本的边际增益近似为 $G(1-t/N_U)$），有：
\[
T''(0) = -N_U\cdot G.
\]
因此 $T(\rho) = \rho N_U G - \tfrac12\rho^2 N_U G + o(\rho^2)$。

**步骤3: 风险惩罚项.**
采用风险厌恶决策者框架。设决策者具有常绝对风险厌恶（CARA）效用函数
$u(g)=-\exp(-\gamma g)$，$\gamma>0$ 为风险厌恶系数。
对总增益 $G_{total}(\rho)$，确定性等价的二阶近似为：
\[
\CE(\rho) = \E[G_{total}(\rho)] - \frac\gamma2\,\V[G_{total}(\rho)] + o(\gamma^2).
\]

在 $p^*$ 下不放回采样，忽略有限总体校正的高阶项，方差的主项为：
\[
\V[G_{total}(\rho)] = B\cdot\sum_k w_k\,\V[\Gamma_k] + O(\rho^2)
= \rho N_U V + O(\rho^2),
\]
其中 $V = \sum_k w_k\,\V[\Gamma_k]$。

将风险厌恶系数与 Cercis 参数 $\eta$ 关联：$\gamma = 1/\eta$。
此赋值的依据：$\eta\to0$（纯开发）时 $\gamma\to\infty$（极端风险厌恶$\Rightarrow$不采样）；
$\eta\to\infty$（纯探索）时 $\gamma\to0$（风险中性$\Rightarrow$全采样），与直观一致。

**步骤4: 综合目标函数.**
结合步骤2和3，忽略 $o(\rho^2)$ 项，净收益函数为：
\[
\Phi(\rho) = \rho N_U G - \tfrac12\rho^2 N_U G - \tfrac1{2\eta}\rho^2 N_U V.
\]

除以正常数 $N_U$（不影响最优化）：
\[
\tilde\Phi(\rho) = \rho G - \tfrac12\rho^2 G - \tfrac1{2\eta}\rho^2 V.
\]

**步骤5: 一阶条件.**
\[
\tilde\Phi'(\rho) = G - \rho G - \tfrac1\eta\rho V
= G - \rho\big(G + V/\eta\big).
\]
令 $\tilde\Phi'(\rho)=0$：
\[
\rho^* = \frac{G}{G + V/\eta}
= \frac{\eta G}{\eta G + V}.
\]

**步骤6: 二阶条件.**
\[
\tilde\Phi''(\rho) = -(G + V/\eta) < 0,
\]
故 $\rho^*$ 为唯一全局极大值点。

**步骤7: 边界分析.**

- $\eta\to0^+$：$\rho^*\to0$（纯开发，仅采最高分样本）；
- $\eta\to\infty$：$\rho^*\to1$（纯探索，全池多样性采样）；
- $\eta=1$：$\rho^* = G/(G+V)$（均衡模式）；
- 固定 $\eta>0$：$\rho^*$ 随 $G$ 递增（高期望增益$\Rightarrow$多采），

这些极限行为与主动学习的直观一致。$\square$

\begin{critique}

1. **核心建模选择：** 目标函数 $\Phi(\rho)$ 中的二次惩罚项
2. **风险厌恶标定：** $\gamma=1/\eta$ 是便利标定（convenient calibration），
3. **CARA-均值-方差近似：** 确定性等价的二阶近似仅在增益分布接近正态
4. **有限总体校正：** 推导忽略了不放回采样的有限总体校正因子
5. **条件严格性：** 本定理标注为 \conditionallyrigorous，

\end{critique}

**Applications:**
Theorem [ref] eliminates the need for manual budget
specification in active learning.  The closed-form rate $\rho^*$ can be
computed from a pilot labeled set of modest size ($m\approx 50$--$100$ samples)
and used to automatically determine how many instances to query in each
active learning round.  This is particularly valuable in production ML pipelines
where annotation budgets vary across datasets and manual tuning is impractical.
In medical imaging, where annotation costs are high and class imbalance is
severe, the class-weighted version of $\rho^*$ automatically allocates more
queries to rare classes with high variance.  In NLP, the rate can be
recomputed per annotation round, adapting to the model's improving confidence
as labeled data accumulates.  The formula also provides a diagnostic: if
$\rho^*$ is close to 0, the model is already near-optimal and additional
labeling yields diminishing returns; if $\rho^*$ is close to 1, the model
is data-starved and aggressive labeling is warranted.

> **Corollary:** [Budget-Free Operation]
> <!-- label: cor:budget-free -->
> The optimal batch size is $B^* = \lceil\rho^* N_U\rceil$.  When $\rho^*$ is
> estimated from pilot samples, the algorithm requires no manual budget
> specification.

### Estimation and Consistency

In practice, $\overline_k$ and $\V[\Gamma_k]$ are unknown and must
be estimated from a pilot labeled set of size $m$.

> **Definition:** [Plug-in Estimator]
> <!-- label: def:plugin -->
> Let $\widehat_k = \frac{1}{m}\sum_{i=1}^m \overline_k(x_i)$
> and $\widehat{V}_k = \frac{1}{m-1}\sum_{i=1}^m
> (\overline_k(x_i)-\widehat_k)^2$.  The plug-in estimator is
> 
> $$<!-- label: eq:plugin -->
>     \hat^*_m =
>     \frac{\eta\sum_{k} w_k \widehat_k}
>          {\eta\sum_{k} w_k \widehat_k
>           + \sum_{k} w_k \widehat{V}_k}.
> $$

> **Theorem:** [估计量的一致性]
> <!-- label: thm:consistency -->
> 设 $\E[\overline_k(x)^4]<\infty$ 对任意 $k$ 成立，且 $\sum_k w_k\overline_k>0$。
> 在 A3（有界损失）下，plug-in 估计量 $\hat^*_m$ 满足：
> \[
> \hat^*_m \xrightarrow{p} \rho^*,\qquad
> \sqrt{m}(\hat^*_m - \rho^*) \xrightarrow{d} \mathcal{N}(0,\sigma^2_\rho),
> \]
> 其中渐近方差 $\sigma^2_\rho$ 的显式表达式由证明给出。

\begin{proof}
**严格性等级:** \rigorous \quad（在所述矩条件下）

**所需公理:** A3（有界损失，保证矩条件 $\E[\overline_k^4]<\infty$ 合理）

**符号约定.**
设 $\mu_k = \overline_k$，$v_k = \V[\Gamma_k]$。
定义 $G = \sum_k w_k \mu_k$，$V = \sum_k w_k v_k$，$D = \eta G + V > 0$。
则 $\rho^* = \eta G / D$。

估计量：
\[
\hat\mu_k = \frac1m\sum_{i=1}^m \overline_k(x_i),\quad
\hat v_k = \frac1{m-1}\sum_{i=1}^m (\overline_k(x_i)-\hat\mu_k)^2.
\]
plug-in 估计量 $\hat\rho^*_m = \eta\hat G / (\eta\hat G + \hat V)$，
其中 $\hat G = \sum_k w_k \hat\mu_k$，$\hat V = \sum_k w_k \hat v_k$。

**步骤1: $\sqrt{m}$-联合渐近正态性.**
将各阶矩估计量堆叠为 $2K$ 维向量：
\[
\hat{\bm\theta}_m = (\hat\mu_1,...,\hat\mu_K,\hat v_1,...,\hat v_K)^\top,\quad
{\bm\theta} = (\mu_1,...,\mu_K,v_1,...,v_K)^\top.
\]

对任意 $k$，由 $\E[\overline_k^4]<\infty$ 知 $\overline_k(x)$ 的四阶矩有限，
从而样本均值 $\hat\mu_k$ 和样本方差 $\hat v_k$ 的方差有限。对样本方差，注意到：
\[
\hat v_k = \frac1{m-1}\sum_{i=1}^m (\overline_k(x_i)-\hat\mu_k)^2
= \frac1{m-1}\sum_{i=1}^m \big((\overline_k(x_i)-\mu_k) - (\hat\mu_k-\mu_k)\big)^2,
\]
其渐近等价于 $\frac1m\sum_{i=1}^m (\overline_k(x_i)-\mu_k)^2$，偏差为 $O_p(m^{-1})$。

由多元中心极限定理：
\[
\sqrt{m}(\hat{\bm\theta}_m - {\bm\theta}) \xrightarrow{d}
\mathcal{N}(0, \bm\Sigma),
\]
其中 $\bm\Sigma$ 是 $2K\times 2K$ 渐近协方差矩阵，其分块结构为：
\[
\bm\Sigma =
\begin{pmatrix}
\bm\Sigma_{\mu\mu} & \bm\Sigma_{\mu v} 

\bm\Sigma_{v\mu} & \bm\Sigma_{vv}
\end{pmatrix},
\]
其中对 $k,j\in\{1,...,K\}$：

$$
[\bm\Sigma_{\mu\mu}]_{kj} &= \Cov(\overline_k(x), \overline_j(x)),

[\bm\Sigma_{\mu v}]_{kj} &= \E[(\overline_k(x)-\mu_k)(\overline_j(x)-\mu_j)^2],

[\bm\Sigma_{vv}]_{kj} &= \E[(\overline_k(x)-\mu_k)^2(\overline_j(x)-\mu_j)^2] - v_k v_j.
$$

（交叉协方差 $\bm\Sigma_{v\mu} = \bm\Sigma_{\mu v}^\top$。）

**步骤2: 相合性.**
由强大数律，$\hat\mu_k \xrightarrow{a.s.} \mu_k$、$\hat v_k \xrightarrow{a.s.} v_k$。
由连续映射定理（Continuous Mapping Theorem），函数
\[
f(g,v) = \frac{\eta g}{\eta g + v}
\]
在 $(G,V)$ 处连续（因 $D = \eta G + V > 0$），故：
\[
\hat\rho^*_m = f(\hat G, \hat V) \xrightarrow{p} f(G, V) = \rho^*.
\]

**步骤3: Delta Method 给出渐近正态性.**
应用 Delta Method 于函数 $f(g,v) = \eta g/(\eta g+v)$：
\[
\sqrt{m}(\hat\rho^*_m - \rho^*) \xrightarrow{d}
\mathcal{N}\!\big(0,\; \nabla f(G,V)^\top \bm\Sigma_{red} \nabla f(G,V)\big),
\]
其中 $\bm\Sigma_{red}$ 是 $(\hat G,\hat V)$ 的 $2\times2$ 渐近协方差矩阵
（通过权重向量 $\bm w = (w_1,...,w_K)$ 从 $\bm\Sigma$ 约化得到）。

**步骤4: 显式梯度.**
计算 $f(g,v) = \eta g/(\eta g+v)$ 的梯度：

$$
\frac{\partial f}{\partial g} &= \frac{\eta(\eta g+v) - \eta g\cdot\eta}{(\eta g+v)^2}
= \frac{\eta v}{(\eta g+v)^2},

\frac{\partial f}{\partial v} &= -\frac{\eta g}{(\eta g+v)^2}.
$$

在真实值 $(G,V)$ 处：
\[
\frac{\partial f}{\partial g}\Big|_{(G,V)} = \frac{\eta V}{D^2},\qquad
\frac{\partial f}{\partial v}\Big|_{(G,V)} = -\frac{\eta G}{D^2},
\]
其中 $D = \eta G + V$。

**步骤5: 约化协方差矩阵.**
$(\hat G, \hat V)$ 的渐近协方差矩阵 $\bm\Sigma_{red}$ 的元素为：

$$
\sigma^2_G &= \sum_{k,j} w_k w_j \Cov(\overline_k, \overline_j),

\sigma^2_V &= \sum_{k,j} w_k w_j\big(\E[(\overline_k-\mu_k)^2(\overline_j-\mu_j)^2] - v_k v_j\big),

\sigma_{GV} &= \sum_{k,j} w_k w_j \E[(\overline_k-\mu_k)(\overline_j-\mu_j)^2].
$$

**步骤6: 渐近方差 $\sigma^2_\rho$ 的闭式.**
综合：

$$
\sigma^2_\rho
&= \Big(\frac{\partial f}{\partial g}\Big)^2 \sigma^2_G
+ \Big(\frac{\partial f}{\partial v}\Big)^2 \sigma^2_V
+ 2\Big(\frac{\partial f}{\partial g}\Big)\Big(\frac{\partial f}{\partial v}\Big) \sigma_{GV} 

&= \frac{\eta^2 V^2}{D^4}\,\sigma^2_G
+ \frac{\eta^2 G^2}{D^4}\,\sigma^2_V
- \frac{2\eta^2 G V}{D^4}\,\sigma_{GV} 

&= \frac{\eta^2}{D^4}\Big(V^2\sigma^2_G + G^2\sigma^2_V - 2GV\sigma_{GV}\Big).
$$

其中 $D = \eta G + V = \eta\sum_k w_k\overline_k + \sum_k w_k\V[\Gamma_k]$。

因此 $\sqrt{m}(\hat\rho^*_m - \rho^*) \xrightarrow{d} \mathcal{N}(0,\sigma^2_\rho)$。$\square$

\begin{critique}

1. **四阶矩条件：** $\E[\overline_k^4]<\infty$ 是 Delta Method 中样本方差渐近正态性的充分条件。当增益分布呈现重尾时（如某些深度学习环境），此条件可能不成立，此时 bootstrap 等重采样方法更为稳健。
2. **有限样本偏差：** plug-in 估计量 $\hat\rho^*_m$ 是矩估计量的非线性比值，对有限 $m$ 存在 $O(m^{-1})$ 偏差（由 Jensen 不等式，$E[\hat G/(\hat G+\hat V/\eta)] \neq G/(G+V/\eta)$）。当 $m$ 较小（如 $m<50$）时，偏差校正（如 Jackknife 或 delta-method 偏差校正）是必要的。
3. **梯度非退化条件：** Delta Method 要求 $\nabla f(G,V) \neq \bm 0$。由 $\partial f/\partial g = \eta V/D^2$ 和 $\partial f/\partial v = -\eta G/D^2$ 知，当且仅当 $G>0$ 且 $V>0$ 时梯度非退化。若 $G=0$（无期望增益）或 $V=0$（零方差），则分布退化为边界情况，需改用更精细的渐近理论（如自归一化 CLT）。
4. **高维协方差估计：** $\bm\Sigma$ 包含 $K(2K+1)$ 个独立参数，其估计本身需要大量样本（$m\gg K^2$）。在高维分类问题（$K>100$）中，需引入稀疏结构假设或正则化协方差估计。
5. **跨轮依赖：** 在主动学习的多轮设定中，不同轮的 $\hat\rho^*_m$ 基于同一模型更新路径计算，存在序列依赖性。本定理的单轮渐近分析忽略了跨轮相关性，实际置信区间可能偏窄。

\end{critique}

**Applications:**
Theorem [ref] guarantees that the plug-in estimator
$\hat^*_m$ is reliable for practical deployment.  The
$\sqrt{m}$-consistency ensures that the estimation error of the optimal
sampling rate decays at the parametric rate, meaning a modest pilot sample
suffices for accurate rate estimation.  This is essential for real-time active
learning systems (e.g., robotics, online advertising) where the sampling rate
must be recomputed frequently as new data arrives.  The asymptotic normality
result further enables the construction of confidence intervals for $\rho^*$,
allowing practitioners to report uncertainty-aware batch sizes (e.g.,
``query 230~$\pm$~15 samples this round'').  In safety-critical applications
such as medical diagnosis, the confidence interval provides a
risk-management tool: one can select the upper confidence bound of $B^*$
to ensure sufficient coverage, or the lower bound to minimize cost.

## Algorithm

Algorithm [ref] summarizes the complete Cercis active learning
procedure.  The key innovation is that the batch size $B^*$ is
*derived*, not tuned.

\begin{algorithm}[tb]
*Caption:* Cercis Optimal Active Learning (COAL)
<!-- label: alg:cercis-al -->
\begin{algorithmic}[1]
\Require Unlabeled pool $\cD_U$, initial labeled set $\cD_L$ (size $m_0$),
         Cercis parameter $\eta$, regularization $\lambda$
\Ensure Augmented labeled set $\cD_L$

\State Train model $h_\theta$ on $\cD_L$
\For{$x\in\cD_U$}
    \State Compute $Q(x)=1-\max_y\hat{p}_\theta(y\mid x)$
    \State Compute $N(x)=\min_{x'\in\cD_L} d(x,x')$
    \State $S(x)\gets Q(x)+\eta N(x)$
\EndFor

\State Estimate $\widehat_k,\widehat{V}_k$ via pilot evaluation
       on hold-out or cross-validation
\State Compute $\hat^*$ via [ref]
\State $B^* \gets \lceil\hat^*|\cD_U|\rceil$

\State Compute $p^*(x)\propto\pi(x)\exp(S(x)/\lambda)$ for all $x\in\cD_U$
\State Draw $B^*$ samples without replacement from $p^*$, obtain labels,
       append to $\cD_L$

\State Retrain $h_\theta$ on augmented $\cD_L$
\State \Return $\cD_L$
\end{algorithmic}
\end{algorithm}

**Computational complexity.**
Computing $N(x)$ naively costs $O(|\cD_U|\cdot|\cD_L|)$ per round.
This can be reduced to $O(|\cD_U|\log|\cD_L|)$ using ball trees or
locality-sensitive hashing in representation space.
The Gibbs distribution $p^*$ can be sampled efficiently via
the Gumbel-max trick: draw $g_x\simGumbel(0,1)$ i.i.d.\ for each
$x$ and select the top-$B^*$ instances according to
$\log\pi(x)+S(x)/\lambda+g_x$.

## Experiments

We evaluate COAL on three standard benchmarks: CIFAR-10 (image
classification, $K=10$), AG News (text classification, $K=4$), and
Cora (node classification, $K=7$).  Baselines include Random sampling,
Uncertainty sampling ($\eta=0$), Diversity sampling via Coreset
($\eta\to\infty$ limit), BADGE [cite], and a fixed-budget
oracle that uses the empirically optimal $\rho$ found by grid search.

**Results.**
Table [ref] reports $F_1$ after 1\,000 acquired labels and the
average batch size $B^*$ selected by COAL.  COAL matches or exceeds the
fixed-budget oracle while automatically adapting the sampling rate.
Across all datasets, COAL reduces annotation cost by 15--40\% relative to
a fixed budget of 10\% of the pool, without sacrificing $F_1$.

[Table omitted — see original .tex]

## Related Work

The Cercis Score originates in the SCX axiomatic system for supervised
learning [cite], where it serves as the objective function
for the Cercis operator that governs optimal data acquisition.  Our
contribution is the closed-form sampling rate, which is not present in the
original SCX treatment.

The variational formulation in [ref] relates to the
KL-regularized policy optimization literature [cite]
and to the information-theoretic active learning framework of
 [cite].  The Gibbs-form solution connects to
exponential-family sampling distributions previously studied in the context
of importance sampling [cite].

The closed-form $\rho^*$ parallels the optimal stopping rules derived in the
optimal experimental design literature [cite], but is
specialized to the $F_1$ metric and the Cercis decomposition, which is what
makes the closed form possible.

## Conclusion

We have derived, from the Cercis Score $S=Q+\eta N$, both the optimal
sampling distribution $p^*(x)$ and a closed-form expression for the
optimal sampling rate $\rho^*$ in active learning.  The rate formula
$\rho^*=\eta G/(\eta G+V)$ with $G=\sum_k w_k\overline_k$ and
$V=\sum_k w_k\V[\Gamma_k]$
provides a principled answer to the long-standing question of how many
samples to label.  The theoretical results are supported by consistency
guarantees and empirical validation.

Future directions include extending the closed form to cost-sensitive
active learning (where labeling costs vary across instances), to
semi-supervised settings where unlabeled data informs the prior $\pi$, and
to online settings where $\eta$ is adapted from streaming feedback.

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{settles2009active}
B.~Settles.
\newblock ``Active learning literature survey,''
\newblock *Computer Sciences Technical Report 1648*, University of
Wisconsin--Madison, 2009.

\bibitem{lewis1994sequential}
D.~D.~Lewis and W.~A.~Gale.
\newblock ``A sequential algorithm for training text classifiers,''
\newblock in *SIGIR*, 1994.

\bibitem{seung1992query}
H.~S.~Seung, M.~Opper, and H.~Sompolinsky.
\newblock ``Query by committee,''
\newblock in *COLT*, 1992.

\bibitem{roy2001toward}
N.~Roy and A.~McCallum.
\newblock ``Toward optimal active learning through sampling estimation of
error reduction,''
\newblock in *ICML*, 2001.

\bibitem{settles2008multiple}
B.~Settles and M.~Craven.
\newblock ``An analysis of active learning strategies for
sequence labeling tasks,''
\newblock in *EMNLP*, 2008.

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{ash2020warm}
J.~T.~Ash, C.~Zhang, A.~Krishnamurthy, J.~Langford, and A.~Agarwal.
\newblock ``Deep batch active learning by diverse, uncertain gradient lower
bounds,''
\newblock in *ICLR*, 2020.

\bibitem{ash2020badge}
J.~Ash, S.~Goel, A.~Krishnamurthy, and S.~Kakade.
\newblock ``Gone fishing: Neural active learning with Fisher embeddings,''
\newblock in *NeurIPS*, 2020.

\bibitem{levine2018reinforcement}
S.~Levine.
\newblock ``Reinforcement learning and control as probabilistic inference:
Tutorial and review,''
\newblock *arXiv:1805.00909*, 2018.

\bibitem{houlsby2011bayesian}
N.~Houlsby, F.~Husz\'ar, Z.~Ghahramani, and M.~Lengyel.
\newblock ``Bayesian active learning for classification and preference
learning,''
\newblock *arXiv:1112.5745*, 2011.

\bibitem{liu2016stein}
Q.~Liu and D.~Wang.
\newblock ``Stein variational gradient descent: A general purpose Bayesian
inference algorithm,''
\newblock in *NeurIPS*, 2016.

\bibitem{pukelsheim2006optimal}
F.~Pukelsheim.
\newblock *Optimal Design of Experiments*.
\newblock SIAM, 2006.

\end{thebibliography}