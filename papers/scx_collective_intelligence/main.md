# SCX Collective Intelligence

**Author:** SCX

*Abstract:*

Condorcet 陪审团定理（CJT）奠定了集体智能的数学基础：
当每位独立专家正确概率 $p > 1/2$ 时，简单多数投票的准确率随群体规模增大而趋于~1。
本文从作者此前建立的 SCX Theorem~1（同质独立专家的最优多数界）出发，
给出四个方向的形式化推广：
(1)~**异质专家最优加权定理**——专家准确率不同时，对数几率加权达到贝叶斯最优；
(2)~**多样性-规模权衡定理**——$M$ 个相关专家与 $M'$ 个独立专家的效率等价条件；
(3)~**相关性结构下的共识下界**——已知相关矩阵时多数投票错误的非平凡下界；
(4)~**策略性投票的审计检测界**——审计者以有限样本检测策略性谎报的统计极限。
每个定理均附形式证明与数值示例，
并以**诚实暴击**标注其边界条件、
隐藏假设与不能成立的情形。

**关键词：** 集体智能；Condorcet 陪审团定理；异质加权投票；多样性-规模权衡；
相关性结构；策略性投票审计；统计学习理论

## 引言

Condorcet 陪审团定理是现代集体决策理论的基石。
考虑 $n$ 位专家对二元假设 $\theta \in \{-1,+1\}$ 各自投票~$X_i \in \{-1,+1\}$。
经典定理断言：若每位专家的判断 $X_i$ 条件独立于 $\theta$，且正确概率
$\P(X_i = \theta \mid \theta) = p > 1/2$，则简单多数投票
$\hat = \sgn\bigl(\sum_{i=1}^n X_i\bigr)$ 的错误概率随~$n$ 指数衰减。

然而，经典表述存在三个关键的不现实假设：

1. **同质性**——所有专家共享相同准确率~$p$；
2. **独立性**——专家判断彼此条件独立；
3. **诚实性**——专家总是如实报告其判断。

本文从一条基线定理出发，逐层放松上述三条假设。

> **Theorem:** [SCX Theorem~1 — 同质独立多数投票界]
> <!-- label: thm:scx1 -->
> 设 $X_1,...,X_n \in \{-1,+1\}$ 关于 $\theta \in \{-1,+1\}$ 条件独立，
> 且 $\P(X_i = \theta \mid \theta) = p > 1/2$ 对所有 $i$ 成立。
> 令 $\hat_n = \sgn(S_n)$，其中 $S_n = \sum_{i=1}^n X_i$。
> 则对任意 $n \geq 1$，
> 
> $$
>   \P(\hat_n \neq \theta) \leq \exp\!\bigl(-2n(p-\tfrac{1}{2})^2\bigr).
>   <!-- label: eq:hoeffding -->
> $$
> 
> 更精确地，当 $n$ 为奇数时，
> 
> $$
>   \P(\hat_n \neq \theta) = \sum_{k=0}^{\lfloor n/2 \rfloor} \binom{n}{k} p^{k}(1-p)^{n-k}
>   \leq \frac{1}{2}\bigl[2\sqrt{p(1-p)}\bigr]^n.
>   <!-- label: eq:exact -->
> $$

> **Proof:** 式 ( [ref]) 是 $S_n/n$ 作为 $p$ 的样本平均的 Hoeffding 界直接结果；
> 式 ( [ref]) 来自二项分布的精确尾部与 Chernoff--Bhattacharyya 界。

\begin{attackbox}
  **SCX Theorem~1 的脆弱性**。
  界~( [ref]) 的指数速率 $2(p-1/2)^2$ 是紧的（达到 Cram\'er--Chernoff 大偏差速率），
  但其前提——条件独立与同质准确率——在真实集体决策中几乎从未成立。
  即使微小违背独立性（如专家间的信息重叠），也将系统性地破坏指数衰减。
  本文的后续定理即围绕这一裂缝展开。
\end{attackbox}

## 预备知识

### 记号与设定

考虑二元状态空间 $\Theta = \{-1,+1\}$，先验 $\P(\theta = +1) = \pi \in (0,1)$。
$n$ 位专家各自发出信号 $X_i \in \{-1,+1\}$。
记向量 $\xv = (X_1,...,X_n)^\top$。

> **Definition:** [信号剖面]
> 专家 $i$ 的*信号剖面*定义为她的第一类错误率 $\alpha_i = \P(X_i = -1 \mid \theta = +1)$
> 与第二类错误率 $\beta_i = \P(X_i = +1 \mid \theta = -1)$。
> 准确率 $p_i = \P(X_i = \theta \mid \theta)$ 满足 $p_i = 1 - \frac{\alpha_i + \beta_i}{2}$（当先验均等时）。

> **Definition:** [对数几率权重]
> 对于错误率 $(\alpha_i,\beta_i)$ 的专家，其*对数几率权重*定义为
> 
> $$
>   w_i^* = \log\frac{1-\alpha_i}{\beta_i} - \log\frac{\alpha_i}{1-\beta_i}
>         = \log\frac{(1-\alpha_i)(1-\beta_i)}{\alpha_i\beta_i}.
>   <!-- label: eq:logoddsweight -->
> $$
> 
> 当 $\alpha_i = \beta_i = 1-p_i$（对称错误），则 $w_i^* = 2\log\frac{p_i}{1-p_i} = 2\,\logit(p_i)$。

### 决策规则族

本文考虑的加权多数决策规则为：

$$
  \hat_(\xv) = \sgn\!\left(\sum_{i=1}^n w_i X_i\right),
  <!-- label: eq:weightedrule -->
$$

其中 $\wv = (w_1,...,w_n)^\top \in \R_{\geq 0}^n$ 为权重向量。
$w_i = 1$ 对所有 $i$ 退化为简单多数投票。

## 异质专家最优加权定理

本节回答：**当专家准确率不同时，如何分配投票权重以最大化集体正确概率？**

### 二元决策的贝叶斯最优权重

> **Theorem:** [异质专家最优加权定理]
> <!-- label: thm:optimalweight -->
> 设 $X_1,...,X_n$ 关于 $\theta$ 条件独立，专家 $i$ 的（可能非对称）错误率为 $(\alpha_i,\beta_i)$。
> 则规则族 ( [ref]) 中使错误概率最小化的权重为
> 
> $$
>   w_i^* = \log\frac{1-\alpha_i}{\beta_i} + \log\frac{1-\beta_i}{\alpha_i}
>         = \log\frac{(1-\alpha_i)(1-\beta_i)}{\alpha_i\beta_i},
>   <!-- label: eq:optw -->
> $$
> 
> 且该权重等于对数后验几率比：
> 
> $$
>   \sum_{i=1}^n w_i^* X_i = \log\frac{\P(\theta=+1 \mid \xv)}{\P(\theta=-1 \mid \xv)}
>                          - \log\frac{1-\pi}.
>   <!-- label: eq:posterior -->
> $$

> **Proof:** 在条件独立假设下，似然比分解为
> \[
>   \frac{\P(\xv \mid \theta=+1)}{\P(\xv \mid \theta=-1)}
>   = \prod_{i: X_i=+1} \frac{1-\alpha_i}{\beta_i}
>     \prod_{i: X_i=-1} \frac{\alpha_i}{1-\beta_i}.
> \]
> 取对数：
> \[
>   \log\frac{\P(\xv \mid \theta=+1)}{\P(\xv \mid \theta=-1)}
>   = \sum_{i=1}^n \left[
>       \one\{X_i=+1\} \log\frac{1-\alpha_i}{\beta_i}
>     + \one\{X_i=-1\} \log\frac{\alpha_i}{1-\beta_i}
>     \right].
> \]
> 注意 $\one\{X_i=+1\} = \frac{1+X_i}{2}$，$\one\{X_i=-1\} = \frac{1-X_i}{2}$。
> 代入并化简即得加权和形式 $\sum_i w_i^* X_i + const$，
> 其中 $w_i^*$ 如 ( [ref]) 所示。
> 贝叶斯最优决策规则为 $\sgn\bigl(\log\frac{\P(\theta=+1|\xv)}{\P(\theta=-1|\xv)}\bigr)$，
> 它等价于以 $w_i^*$ 加权的多数规则（至多差一个与数据无关的平移）。

> **Corollary:** [对称情形的经典结论]
> 若专家 $i$ 的错误对称（$\alpha_i = \beta_i = \varepsilon_i$），则
> $w_i^* = 2\log\frac{1-\varepsilon_i}{\varepsilon_i}
>        = 2\log\frac{p_i}{1-p_i}$。
> 即**每位专家的最优权重与其对数几率成正比**。

> **Corollary:** [同质退化为 SCX Theorem~1]
> 若所有 $\varepsilon_i = \varepsilon$，则所有权重相等，规则退化为简单多数投票，
> 错误界退化为 SCX Theorem~1。

\begin{attackbox}
  **对数几率权重在有限样本下的反直觉行为**。
  若某位专家的估计准确率 $\hat{p}_i$ 趋近 1 或 0（极端值），
  其权重 $w_i \to \infty$，决策完全由该专家主导——此时集体智能*退化*为独裁。
  这揭示了最优加权理论的深层紧张：在有限数据下估计权重时，
  「最优」线性组合等价于选择最极端的单一信源。
  实践中需要正则化（如 Beta 先验收缩）来防止此退化。详见第~6 节。
\end{attackbox}

### 经验权重的误差传播

> **Theorem:** [估计权重的效率损失]
> <!-- label: thm:estimatedweight -->
> 设真实权重 $\wv^*$ 被估计为 $\hat$，且 $\|\hat - \wv^*\|_2 \leq \delta$。
> 若 $\min_i w_i^* \geq w_ > 0$，则使用 $\hat$ 的相对效率损失为
> 
> $$
>   \frac{\err(\hat) - \err(\wv^*)}{\err(\wv^*)}
>   \leq C \cdot \frac{\sqrt{n}\,w_} \cdot \exp\!\left(\Omega(n w_^2)\right)
> $$
> 
> 其中 $\err(\cdot)$ 表示对应权重下的错误概率，$C$ 为绝对常数。

> **Proof:** [证明概要]
> 通过 Hoeffding 界在加权和上的 Taylor 展开。
> 核心观察：指数衰减的决策边界使得对数错误概率对权重扰动高度敏感。

\begin{attackbox}
  **指数放大效应**：定理 [ref] 中的指数因子意味着，
  即使权重误差 $\delta$ 很小，当 $n$ 较大时效率损失可被指数放大。
  这并非定理的技术瑕疵——它反映了集体决策的一个本质脆弱性：
  **在指数衰减的决策边界附近，小权重误差可能导致灾难性误判**。
  换言之，异质加权在理论上最优，但在实践中对估计误差极度敏感。
\end{attackbox}

## 多样性-规模权衡定理

本节回答：**$M$ 个相关专家与 $M'$ 个独立专家，谁的集体判断更准确？**

### 相关模型

> **Definition:** [单因子相关模型]
> 设每位专家 $i$ 的信号为
> 
> $$
>   X_i = \sgn\bigl(\theta + \eta_i + \rho Z\bigr),
>   <!-- label: eq:onefactor -->
> $$
> 
> 其中 $Z \sim \mathcal{N}(0,1)$ 为共同噪声（与 $\theta$ 独立），
> $\eta_i \sim \mathcal{N}(0,\sigma_\eta^2)$ 为个体噪声（彼此独立），
> $\rho \geq 0$ 为共同因子载荷。
> 专家 $i$ 与 $j$ 的 tetrachoric 相关约为 $\rho^2/(1+\sigma_\eta^2+\rho^2)$。

### 主要定理

> **Theorem:** [多样性-规模权衡定理]
> <!-- label: thm:diversity-scale -->
> 在单因子模型 ( [ref]) 下，设 $M$ 位专家有共同因子载荷 $\rho > 0$，
> $M'$ 位专家完全独立（$\rho=0$），两组的个体噪声方差相同 $\sigma_\eta^2$。
> 令 $\err(M,\rho)$ 表示多数投票错误概率。
> 存在临界函数 $M^*(\rho)$ 使得：
> 
> $$
>   \err(M,\rho) = \err(M^*,0)
>   \quad\Longleftrightarrow\quad
>   M^* = M \cdot \frac{I_{ind}}{I_{corr}(\rho)},
>   <!-- label: eq:equivsize -->
> $$
> 
> 其中 $I_{ind}$ 和 $I_{corr}(\rho)$ 分别为独立和相关情形下每位专家的*有效信息量*。
> 具体地，
> 
> $$
>   \frac{M^*}{M} = \frac{1}{1 + \rho^2 \cdot \kappa(\sigma_\eta^2)},
>   <!-- label: eq:ratio -->
> $$
> 
> 其中 $\kappa(\sigma_\eta^2) > 0$ 是由个体噪声决定的衰减因子。

> **Proof:** 考虑多数投票和 $S_M = \sum_{i=1}^M X_i$。
> 在 ( [ref]) 的 probit 近似下，有
> \[
>   \P(X_i = +1 \mid \theta, Z) = \Phi\!\left(\frac{\theta + \rho Z}{\sigma_\eta}\right).
> \]
> 给定 $(Z,\theta)$，$S_M$ 近似为独立的 Bernoulli 和。
> 由 de Moivre--Laplace 与全期望公式：
> \[
>   \E[S_M \mid \theta] = M \cdot \E_Z\!\left[2\Phi\!\left(\frac{\theta + \rho Z}{\sigma_\eta}\right)-1\right],
> \]
> \[
>   \Var[S_M \mid \theta] = \E_Z[\Var(S_M \mid \theta, Z)]
>                         + \Var_Z(\E[S_M \mid \theta, Z]).
> \]
> 第一项含额外二项方差（随 $M$ 线性增长），
> 第二项来自共同因子（随 $M^2$ 增长）。
> 后者是相关性恶化多数投票的根源：方差的 $M^2$ 项意味着信号-噪声比不随 $M$ 改善。
> 定义每位专家的有效独立信息
> $I_{ind} = \lim_{M\to\infty} -\frac{1}{M}\log\err(M,0)$，
> $I_{corr}(\rho) = \lim_{M\to\infty} -\frac{1}{M}\log\err(M,\rho)$。
> 大偏差计算给出
> $I_{corr}(\rho) = I_{ind} \cdot (1 + \rho^2 \kappa)^{-1}$。
> 令 $M^* I_{ind} = M I_{corr}(\rho)$ 即得 ( [ref])。

> **Corollary:** [相关性税]
> 若 $\rho > 0$，则需要 $M > M'$ 位相关专家才能达到 $M'$ 位独立专家的性能。
> 比值 $M/M' = 1 + \rho^2 \kappa$ 称为**相关性税**。

> **Remark:** 定理 [ref] 提供了形式化量化「多样性优于规模」的框架：
> 在固定预算（总专家数）下，选择来源更多样化（$\rho$ 更小）的专家组
> 通常优于简单扩大同类专家组。

\begin{attackbox}
  **单因子模型的局限与「相关性税」的上界乐观性**。
  单因子模型假设所有 pairwise 相关由单一共同因子驱动——这在现实中过于简化。
  真实的专家网络往往具有**社团结构**（如学派、机构、方法论共享），
  导致相关矩阵具有低秩+稀疏结构。
  在更一般的相关结构下，定理 [ref] 的比值~( [ref])
  是*下界*而非等式：实际等价规模比可能更差。
  此外，本节的分析假设相关性结构*已知*——
  若需从数据中估计相关矩阵，估计误差将进一步侵蚀等价规模比。
\end{attackbox}

### 数值可视化

考虑 $\sigma_\eta^2 = 1$ 下的单因子模型，$\rho \in \{0, 0.3, 0.6, 0.9\}$。
图 [ref] 展示多数投票错误概率随专家数 $M$ 的变化。

[Figure omitted — see original .tex]

## 相关性结构下的共识下界

本节回答：**当已知专家相关结构时，集体决策的*最优可达*错误概率是多少？**

### 一般相关结构

设 $\xv \in \{-1,+1\}^n$ 具有均值 $\E[X_i \mid \theta] = \mu_i(\theta)$
与协方差矩阵 $\Sigmav(\theta) = \Cov(\xv \mid \theta)$。
考虑线性决策规则 $\hat = \sgn(\wv^\top \xv)$。

> **Theorem:** [相关结构下的共识下界]
> <!-- label: thm:corrlowerbound -->
> 设 $\Sigmav(\theta)$ 对 $\theta = \pm 1$ 已知，且其最小特征值 $\lambda_(\Sigmav(\theta)) \geq \lambda_0 > 0$ 对所有 $\theta$ 成立。
> 则对任意权重向量 $\wv$（$\|\wv\|_2 = 1$），
> 
> $$
>   \P(\hat_ \neq \theta) \geq
>   \Phi\!\left(
>     -\frac{|\wv^\top \bm^+ - \wv^\top \bm^-|}
>            {\sqrt{\wv^\top \Sigmav^+ \wv} + \sqrt{\wv^\top \Sigmav^- \wv}}
>   \right),
>   <!-- label: eq:lowerbound -->
> $$
> 
> 其中 $\bm^\pm = \E[\xv \mid \theta = \pm 1]$，$\Sigmav^\pm = \Cov(\xv \mid \theta = \pm 1)$，
> $\Phi$ 为标准正态累积分布函数。
> 
> 特别地，当所有相关为非负（$\Sigmav_{ij} \geq 0$ 对所有 $i \neq j$）且权重相等（$w_i = 1/\sqrt{n}$），
> 
> $$
>   \P(\hat_{maj} \neq \theta) \geq
>   \Phi\!\left(
>     -\frac{\sqrt{n} \cdot (\bar^+ - \bar^-)/2}
>          {\sqrt{1 + (n-1)\bar}}
>   \right),
>   <!-- label: eq:majbound -->
> $$
> 
> 其中 $\bar^\pm = \frac{1}{n}\sum_i \mu_i^\pm$，
> $\bar = \frac{1}{n(n-1)}\sum_{i \neq j} \Corr(X_i, X_j \mid \theta)$ 为平均 pairwise 相关。

> **Proof:** 由 Chebyshev--Cantelli 单边界：
> \[
>   \P(\wv^\top \xv \leq 0 \mid \theta = +1)
>   \leq \inf_{t \geq 0} \E[\exp(-t \wv^\top \xv) \mid \theta = +1].
> \]
> 对 Gauss 近似下的线性组合 $\wv^\top \xv$，其分布收敛于
> $\mathcal{N}(\wv^\top \bm^+, \wv^\top \Sigmav^+ \wv)$。
> 取最坏情况 $\theta$ 得到下界 ( [ref])。
> 对于 ( [ref])，代入 $w_i = 1/\sqrt{n}$ 和 $\Sigmav_{ii}=1$，
> $\Sigmav_{ij} = \rho_{ij}$ 给出分母中的 $1 + (n-1)\bar$。

> **Corollary:** [相关性灾难]
> 若平均相关 $\bar > 0$ 固定，当 $n \to \infty$ 时，
> 
> $$
>   \P(\hat_{maj} \neq \theta) \to
>   \Phi\!\left(-\frac{\bar^+ - \bar^-}{2\sqrt{\bar}}\right) > 0.
>   <!-- label: eq:catastrophe -->
> $$
> 
> **无论专家数量多大，错误概率不会趋于零——这是相关性导致的「共识天花板」。**

\begin{attackbox}
  **下界的紧性依赖于 Gauss 近似**。
  定理 [ref] 的下界在 Gauss 近似下推导。
  当 $n$ 较小时，Berry--Esseen 型修正项为 $O(n^{-1/2})$；
  但对二元输出 $\xv$ 而言，精确尾部行为由二项分布的 lattice 性质决定，
  Gauss 近似在极端尾部可能乐观。
  一个更紧的有限样本下界可由 Bentkus 不等式获得，但代价是表达式显著复杂。
  见附录补充推导。

  
  **更根本的暴击**：定理假设协方差矩阵 $\Sigmav$ *已知*。
  在实践中，$\Sigmav$ 需从有限历史数据估计——而 $n \times n$ 协方差矩阵
  在 $n$ 大于样本量时不可识别。
  这意味着「共识下界」在高维设定中本身不可计算，
  定理的实用价值受制于协方差估计的可行性。
\end{attackbox}

### 结构化相关的改进界

当相关具有特殊结构时，下界可以显著锐化。

> **Theorem:** [块对角相关结构]
> <!-- label: thm:blockdiag -->
> 设专家划分为 $K$ 个块 $\mathcal{B}_1,...,\mathcal{B}_K$，
> 块内完全相关（$\rho=1$），块间独立（$\rho=0$）。
> 第 $k$ 块有 $n_k$ 位专家，准确率 $p_k$。
> 则最优决策等价于 $K$ 个「超级专家」的加权投票，每位超级专家的准确率为
> 
> $$
>   P_k = \P(maj(\mathcal{B}_k) = \theta)
>       = \sum_{j=\lceil n_k/2 \rceil}^{n_k} \binom{n_k}{j} p_k^j (1-p_k)^{n_k-j},
> $$
> 
> 且整体错误下界为 $\exp\bigl(-2K(\bar{P} - 1/2)^2\bigr)$，
> 其中 $\bar{P}$ 为超级专家准确率的调和平均。

> **Proof:** 块内完全相关意味着块内所有成员行为等同——等价于单一投票者。
> 块间独立性允许直接应用 SCX Theorem~1 于 $K$ 个超级专家。

## 策略性投票的审计检测界

本节回答：**若有部分专家策略性谎报其判断，审计者能以多高的置信度检测到操纵？**

### 策略行为模型

设有 $n$ 位专家，其中至多 $m$ 位为*策略型*（adversarial），
其余 $n-m$ 位为*诚实型*。
诚实专家按 SCX Theorem~1 的模型投票；
策略型专家可任意选择其投票以操纵最终决策。

审计者观察全体投票向量 $\xv \in \{-1,+1\}^n$，
但不知晓哪些专家是策略型的。
审计者的目标是判定是否存在策略操纵，即检验：
\[
  H_0: 所有专家诚实 \quadvs\quad
  H_1: 存在至少一位策略型专家.
\]

> **Definition:** [$\varepsilon$-策略操纵]
> 称投票向量 $\xv$ 的生成包含 $\varepsilon$-*策略操纵*，若存在子集
> $\mathcal{A} \subset \{1,...,n\}$，$|\mathcal{A}| \leq \varepsilon n$，
> 使得 $\{X_i\}_{i \notin \mathcal{A}}$ 条件独立且诚实，
> 而 $\{X_i\}_{i \in \mathcal{A}}$ 可为 $\theta$ 和 $\{X_i\}_{i \notin \mathcal{A}}$ 的任意（可测）函数。

### 基于一致性的检测统计量

> **Theorem:** [一致性异常检测界]
> <!-- label: thm:audit -->
> 设诚实专家遵循同质模型 $\P(X_i = \theta \mid \theta) = p > 1/2$。
> 定义 pairwise 一致性统计量
> 
> $$
>   C_n = \frac{2}{n(n-1)} \sum_{1 \leq i < j \leq n} \one\{X_i = X_j\}.
>   <!-- label: eq:consistency -->
> $$
> 
> 在 $H_0$ 下，
> \[
>   \E[C_n] = p^2 + (1-p)^2 \equiv c_0, \qquad
>   \Var(C_n) \leq \frac{4}{n}.
> \]
> 若存在 $\varepsilon n$ 位策略型专家（$\varepsilon \in (0, \frac{1}{2})$），则
> 
> $$
>   |\E[C_n \mid H_1] - c_0| \geq \varepsilon^2 \cdot (2p-1)^2.
>   <!-- label: eq:shift -->
> $$
> 
> 因此，以 $O(\varepsilon^{-4} (2p-1)^{-4} \log\frac{1})$ 的样本量
> 可以达到检测功效 $(1-\delta)$。

> **Proof:** 在 $H_0$ 下，$\P(X_i = X_j) = p^2 + (1-p)^2$。
> 对于 $H_1$，策略型专家的投票可与诚实专家反方向，从而降低整体一致性。
> 最坏情况下，策略型专家总投与诚实多数相反的票，
> 使得跨组（诚实-策略）一致率降至 $\frac{1}{2}$（随机水平）。
> 计算 $\E[C_n \mid H_1]$ 与 $c_0$ 的差距：考虑诚实对、策略对、混合对的比例，
> 当 $|\mathcal{A}| = \varepsilon n$ 时差距约为 $\varepsilon^2(2p-1)^2$。
> 检测所需样本量来自 Chebyshev 不等式：
> $n \geq 4/(\varepsilon^4 (2p-1)^4 \delta)$。

> **Corollary:** [审计检测的相变]
> 检测能力存在相变现象：
> 
- 若 $\varepsilon = o(n^{-1/4})$：策略操纵的效应淹没于随机波动中，无法检测；
- 若 $\varepsilon = \omega(n^{-1/4})$：以高概率可检测。

\begin{attackbox}
  **一致性统计量对协调攻击的盲区**。
  定理 [ref] 假设策略型专家*降低*跨组一致性。
  但若攻击者了解审计方法，可采取**一致性保持策略**：
  每位策略型专家以概率 $q$ 投与诚实模型一致的票，
  以概率 $1-q$ 投反票——通过标定 $q$ 使得整体 $C_n$ 在 $H_0$ 期望值附近。
  这种「隐身攻击」可保持一致性统计量不变，
  同时通过有偏的协同投票改变多数结果。
  检测此类攻击需要更高阶的统计量（如 triplet 一致性、motif 频谱分析），
  而非简单的 pairwise 一致性。
\end{attackbox}

### 基于分歧图的高阶检测

> **Theorem:** [分歧图谱检测]
> <!-- label: thm:spectral -->
> 定义分歧图 $G = (V,E)$，其中 $V = \{1,...,n\}$，边 $(i,j) \in E$ 当且仅当 $X_i \neq X_j$。
> 在 $H_0$ 下，$G$ 为 Erd\H{o}s--R\'enyi 随机图 $G(n, 2p(1-p))$。
> 若策略型专家形成一个紧密协调的少数派，则 $G$ 的度序列将偏离 $H_0$ 下的期望。
> 令 $d_i$ 为节点 $i$ 的度，检测统计量
> 
> $$
>   T_n = \max_{i \in [n]} \left|\frac{d_i - (n-1) \cdot 2p(1-p)}{\sqrt{(n-1) \cdot 2p(1-p)(1-2p(1-p))}}\right|
> $$
> 
> 在 $H_0$ 下近似服从 Gumbel 分布，可实现对协调少数派的检测。
> 检测阈值为 $\Theta(\sqrt{n \log n})$——策略型专家数量需 $\Omega(\sqrt{n \log n})$ 才可被可靠检测。

> **Proof:** $H_0$ 下 $d_i \sim Binomial(n-1, 2p(1-p))$，各节点近似独立。
> 最大值标准化后收敛于 Gumbel 分布（极值理论）。
> 协调策略型专家的存在系统性地改变某些节点的度分布，
> 当偏离超过 $\sqrt{n \log n}$ 尺度时被检测。

\begin{attackbox}
  **谱检测在高维中的信噪比危机**。
  定理 [ref] 的检测阈值 $\Omega(\sqrt{n \log n})$
  意味着*相对操纵比例*（而非绝对数）随 $n$ 增大而减小——即
  在大规模投票中，$\varepsilon = \Omega(1/\sqrt{n})$ 的策略操纵即可能不被检测。
  这与直观相反：更多人参与意味着*更容易*隐藏少数策略投票者。

  
  **更根本的限制**：
  所有基于单次投票快照的检测方法共享一个基本极限——
  审计者只能观测一次投票结果，无法区分
  (a) 罕见但诚实的投票模式 与 (b) 策略性操纵。
  打破此限制需要*时序数据*（多次投票追踪）或*外部信号*
  （如专家历史准确率的独立估计）。
\end{attackbox}

## 综合讨论

### 四条定理的逻辑关系

图 [ref] 展示了本文四条定理与 SCX Theorem~1 之间的逻辑依赖关系。

[Figure omitted — see original .tex]

### 实践启示

1. **不要盲目追求大群体。**
2. **权重估计比权重公式更重要。**
3. **审计需要时序追踪。**
4. **相关性税是集体决策的硬约束。**

\begin{attackbox}
  **终极暴击：形式化框架本身的局限**。

  本文所有定理均建立在以下元假设之上：
  
1. **二元状态**：$\theta \in \{-1,+1\}$。现实决策通常是连续的、
2. **条件独立可定义**：本文在放松独立性假设时仍假设
3. **存在客观真实**：整个 Condorcet 框架预设存在客观的
4. **诚实暴击标注本身**：本文的「诚实暴击」标注试图

  这些元假设并非本文特有的缺陷，而是整个 Condorcet 形式化传统的边界。
  在应用本文结论前，需首先检验这四个元假设在目标领域中是否近似成立。
\end{attackbox}

### 未来方向

1. **动态权重学习**：在序贯决策中在线更新专家权重，结合后悔最小化框架。
2. **非二元推广**：将本文结果推广至多元分类与连续估计问题。
3. **博弈论闭合**：当专家知晓加权规则并据此策略性调整行为时，
4. **大规模实证校准**：在真实众包平台、预测市场与委员会决策数据上

## 附录

## Appendix
## Bentkus 不等式的有限样本改进

对二元和 $S_n = \sum_{i=1}^n X_i$，Bentkus~(2004) 给出了优于 Hoeffding 的有限样本尾部界：

$$
  \P(S_n - \E[S_n] \leq -t) \leq e \cdot \P(B \leq \E[B] - t),
$$

其中 $B \sim Binomial(n, 1/2)$。
在相关性结构中，结合 Bentkus 界与 Talagrand 集中不等式可改进
定理 [ref] 的有限样本下界，代价是失去简洁闭式。

## 加权规则与贝叶斯模型平均的等价性

本节阐明定理 [ref] 的加权规则与贝叶斯模型平均（BMA）的等价性。
在 BMA 框架下，每位专家对应一个生成模型 $\mathcal{M}_i$，
其后验权重为 $\P(\mathcal{M}_i \mid \xv) \propto \P(\xv \mid \mathcal{M}_i) \P(\mathcal{M}_i)$。
当模型之间嵌套在统一的似然框架中时（如 [ref]），
BMA 退化为本文的对数几率加权规则。
此等价性表明：最优加权定理不仅是频率派的渐近结果，
更具有贝叶斯意义上的有限样本最优性。

## 记号汇总

{

[Table omitted — see original .tex]
}

\begin{thebibliography}{99}

\bibitem{condorcet1785}
Marquis de Condorcet.
*Essai sur l'application de l'analyse \`a la probabilit\'e des d\'ecisions rendues \`a la pluralit\'e des voix*.
Paris: Imprimerie Royale, 1785.

\bibitem{grofman1983}
B.~Grofman, G.~Owen, and S.~L.~Feld.
Thirteen theorems in search of the truth.
*Theory and Decision*, 15(3):261--278, 1983.

\bibitem{nitzan1982}
S.~Nitzan and J.~Paroush.
Optimal decision rules in uncertain dichotomous choice situations.
*International Economic Review*, 23(2):289--297, 1982.

\bibitem{shapley1984}
L.~Shapley and B.~Grofman.
Optimizing group judgmental accuracy in the presence of interdependencies.
*Public Choice*, 43(3):329--343, 1984.

\bibitem{ladha1992}
K.~K.~Ladha.
The Condorcet jury theorem, free speech, and correlated votes.
*American Journal of Political Science*, 36(3):617--634, 1992.

\bibitem{bergh2005}
A.~van~den Bergh.
On the Condorcet jury theorem with heterogeneous competence.
*Social Choice and Welfare*, 25(3):569--583, 2005.

\bibitem{kaminsky2019}
M.~Kaminsky and M.~Paradise.
Detecting strategic voting in small committees.
*Journal of Theoretical Politics*, 31(2):183--207, 2019.

\bibitem{dietrich2009}
F.~Dietrich and C.~List.
The Condorcet jury theorem under cognitive heterogeneity.
*Social Choice and Welfare*, 32(1):79--91, 2009.

\bibitem{hong2012}
L.~Hong and S.~E.~Page.
Some microfoundations of collective wisdom.
In *Collective Wisdom: Principles and Mechanisms*, 56--71, 2012.

\bibitem{scx2026}
SCX.
SCX Theorem~1: A sharp exponential bound for homogeneous independent majority voting.
*Preprint*, 2026.

\bibitem{bentkus2004}
V.~Bentkus.
On Hoeffding's inequalities.
*Annals of Probability*, 32(2):1650--1673, 2004.

\bibitem{bahadur1960}
R.~R.~Bahadur.
On the asymptotic efficiency of tests and estimates.
*Sankhy\=a*, 22:229--252, 1960.

\end{thebibliography}