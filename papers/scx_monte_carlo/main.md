<div align="center">

[Diagram omitted — see original .tex]

{ 万物可采样 万象皆收敛}
{ *All things are samplable. All phenomena converge.*}

</div>

> **审计即采样。Audit is sampling.**
> 
> SCX 审计的核心问题——多专家共识、在线审计更新、Cercis 校准——
> 本质上都是高维概率分布上的采样问题。本文建立了一套完整的蒙特卡洛
> 方法论，将五个互补的 MCMC 方法系统化地应用于 SCX 审计框架。
> 这不是简单的数值工具，而是对审计过程本身的概率性形式化。
> 
> The core problems of SCX auditing — multi-expert consensus, online audit updates,
> Cercis calibration — are fundamentally sampling problems on high-dimensional
> probability distributions. This paper establishes a complete Monte Carlo
> methodology, systematically applying five complementary MCMC methods to the
> SCX audit framework. This is not merely a numerical toolkit, but a probabilistic
> formalization of the audit process itself.

---

---

*Abstract:*

**English Abstract:** We present a unified Monte Carlo framework for SCX
(Supercomputing Claim eXamination) audit problems, encompassing five complementary
Markov Chain Monte Carlo (MCMC) methodologies: (1) **Hamiltonian Monte Carlo
on the Situs manifold** — we equip the expert-configuration space with the Situs
metric as a mass matrix, enabling efficient HMC sampling from the Boltzmann
distribution $P(E) \propto \exp(-\beta \cdot Cercis(E))$, and prove ergodicity
under mild conditions; (2) **Sequential Monte Carlo for online audit** —
as new data arrives, particle filters update the posterior over expert
reliability via importance resampling, with a rigorous effective sample size
bound; (3) **Thermodynamic integration for Cercis calibration** — we
anneal from high-SNR (easy) to low-SNR (hard) audit problems, extracting the
Cercis score as a free-energy difference; (4) **Replica exchange for
multi-expert consensus** — parallel tempering with replicas at different
temperatures explores distinct modes of the expert-configuration space,
escaping local optima via replica swaps; (5) **Convergence diagnostics**
— we formalize audit convergence via the Gelman-Rubin $\Rhat$ statistic and
effective sample size (ESS), establishing that an audit is ``converged'' when
$\Rhat < 1.01$ for all gauge parameters $g_i$.

**中文摘要：** 本文提出 SCX（超级计算声明审查）审计问题的统一蒙特卡洛框架，
涵盖五种互补的马尔可夫链蒙特卡洛（MCMC）方法：(1) **Situs 流形上的哈密顿
蒙特卡洛**——以 Situs 度规为质量矩阵配置专家空间，从 Boltzmann 分布
$P(E) \propto \exp(-\beta \cdot Cercis(E))$ 中高效采样，并在温和条件下证明
遍历性；(2) **在线审计的序贯蒙特卡洛**——随新数据到达，粒子滤波器通过
重要性重采样更新专家可靠性的后验分布，导出严格的有效样本量界；
(3) **Cercis 校准的热力学积分**——从高信噪比（易）退火至低信噪比（难）
审计问题，以自由能差的形式提取 Cercis 分数；(4) **多专家共识的副本交换**
——不同温度副本的并行回火探索专家配置空间的不同模态，通过副本交换逃离局部
最优；(5) **收敛诊断**——通过 Gelman-Rubin $\Rhat$ 统计量和有效样本量
（ESS）形式化审计收敛，建立所有规范参数 $g_i$ 满足 $\Rhat < 1.01$ 的审计
收敛标准。

**Keywords:** Hamiltonian Monte Carlo, Sequential Monte Carlo, Thermodynamic
Integration, Replica Exchange, Convergence Diagnostics, Situs Manifold, Cercis,
SCX, MCMC, Audit

**关键词：** 哈密顿蒙特卡洛，序贯蒙特卡洛，热力学积分，副本交换，收敛诊断，
Situs流形，Cercis，SCX，MCMC，审计

---

## 预备知识：SCX 审计的概率框架
## Preliminaries: Probabilistic Framework of SCX Audit
\addcontentsline{toc}{section}{0. Preliminaries: Probabilistic Framework of SCX Audit}

### 核心结构 Core Structures

SCX 审计的核心对象包括以下数学结构：

> **Definition:** [专家配置空间 Expert Configuration Space]
> 令 $\Situs$ 为 Situs 流形，即所有可能专家配置 (expert configuration) 的黎曼流形。
> 对于 $n$ 个专家评估 $m$ 个声明，每个专家 $j$ 对声明 $i$ 给出规范姿态
> $g_{ij} \in \R$，满足 $\sum_i g_{ij} = 0$（规范约束）。则一个配置为向量
> 
> 
> $$<!-- label: eq:config -->
>     E = (g_{11}, ..., g_{m1}, g_{12}, ..., g_{m2}, ..., g_{mn}) \in \R^{mn-n}
> $$
> 
> 
> $\Situs$ 配备 Situs 度规 $h_$，由势能 Hessian 定义：
> $h_ = \nabla^2 \mathcal{S}_{total}$，其中
> $\mathcal{S}_{total}$ 为总势能面。

> **Definition:** [Cercis 分数 Cercis Score]
> Cercis 分数 $Cercis: \Situs \to \R$ 是规范不变的可观测量，定义为
> 
> 
> $$<!-- label: eq:cercis -->
>     Cercis(E) = \frac{1}{2} \sum_{i,j} g_{ij}^2 - \lambda \sum_{i} \left( \sum_{j} g_{ij} \right)^2
> $$
> 
> 
> 其中 $\lambda > 0$ 为规范固定参数。Cercis 分数衡量专家配置的"不协调程度"：
> $Cercis(E) = 0$ 对应于完美的 $\sum g = 0$ 共识；$Cercis(E)$ 越大，配置越偏离
> 共识。

> **Definition:** [Boltzmann 分布 Boltzmann Distribution]
> 在逆温度 $\beta = 1/T$ 下，Situs 流形上的 Boltzmann 分布为
> 
> 
> $$<!-- label: eq:boltzmann -->
>     \pi_\beta(E) = \frac{1}{Z(\beta)} \exp\!\big(-\beta \cdot Cercis(E)\big),\quad
>     Z(\beta) = \int_ e^{-\beta \cdot Cercis(E)} \, d\Vol_(E)
> $$
> 
> 
> 其中 $Z(\beta)$ 为配分函数，$d\Vol_(E)$ 为 Situs 度规诱导的体积元。

> **Remark:** $\pi_\beta$ 是 SCX 审计的**核心采样目标**。低 $\beta$（高温）对应弱约束，
> 配置空间广泛探索；高 $\beta$（低温）对应强约束，采样集中在 $Cercis$ 的低谷
> （高共识区域）。极限 $\beta \to \infty$ 恢复确定性审计结果。

### 蒙特卡洛审计原理 The Monte Carlo Audit Principle

\begin{principle}[蒙特卡洛审计原理 MC Audit Principle]
审计即从 Boltzmann 分布 $\pi_\beta(E)$ 中采样。给定 $N$ 个独立样本
$\{E^{(k)}\}_{k=1}^N \sim \pi_\beta$：

- **点估计：** $\hat{g}_{ij} = \frac{1}{N} \sum_{k=1}^N g_{ij}^{(k)}$
- **不确定度：** $\widehat[g_{ij}] = \frac{1}{N-1} \sum_{k=1}^N (g_{ij}^{(k)} - \hat{g}_{ij})^2$
- **共识概率：** $\widehat[\sum_j g_{ij} \approx 0] = \frac{1}{N} \sum_{k=1}^N \mathbb{1}[|\sum_j g_{ij}^{(k)}| < \epsilon]$

当 $N \to \infty$ 时，这些估计以概率 1 收敛于真实后验量（大数定律）。
\end{principle}

---

# 第一部分：Situs 流形上的哈密顿蒙特卡洛
# Part I: Hamiltonian Monte Carlo on the Situs Manifold
\addcontentsline{toc}{part}{Part I: Hamiltonian Monte Carlo on the Situs Manifold}

## HMC 理论框架
## HMC Theoretical Framework
\addcontentsline{toc}{section}{1. HMC Theoretical Framework}

### 从欧几里得到 Situs：为什么需要流形上的 HMC？

标准 HMC 假设状态空间为 $\R^d$ 配备欧几里得度规 $M = I$。在 SCX 审计中，
专家配置空间 $\Situs$ 并非平坦：Situs 度规 $h_ = \nabla^2 \mathcal{S}$
在势能面陡峭处收缩，在平缓处扩张。忽略此几何结构导致以下问题：

1. **采样效率低下：** 在高度弯曲区域，欧几里得 HMC 需要极小步长
2. **混合缓慢：** 无法利用 Situs 度规提供的自然坐标
3. **遍历性丧失风险：** 欧几里得步长可能导致链被"困在"高弯曲区域

**解决方案：** 将 Situs 度规作为 HMC 的质量矩阵，即 $M \equiv h_$。

### 黎曼流形上的哈密顿动力学

令 $q \in \Situs$ 为配置空间坐标（对应 $E = (g_{ij})$），$p \in T_q^*\Situs$ 为
共轭动量。定义哈密顿量：

$$<!-- label: eq:hamiltonian -->
    H(q, p) = \frac{1}{2} p^\top M(q)^{-1} p + U(q),\quad
    U(q) = \beta \cdot Cercis(q)
$$

其中 $M(q) = h_(q)$ 为位置依赖的质量矩阵（即 Situs 度规）。

\begin{keyeq}
**黎曼 HMC 的运动方程：**

$$
    \dv{q}{t} &= M(q)^{-1} p <!-- label: eq:eom_q --> 

    \dv{p}{t} &= -\nabla_q U(q) + \frac{1}{2} \nabla_q \big[ p^\top M(q)^{-1} p \big] <!-- label: eq:eom_p -->
$$

方程  [ref] 中的第二项是**度量修正项**，补偿位置依赖质量矩阵
对流形的弯曲。这是黎曼 HMC 与欧几里得 HMC 的核心区别。
\end{keyeq}

### 数值积分：广义蛙跳法

\begin{algorithm-env}[广义蛙跳积分器 Generalized Leapfrog Integrator]
给定步长 $\epsilon$ 和步数 $L$，黎曼流形上的蛙跳积分：

\begin{algorithmic}[1]
\State **输入:** 当前位置 $q$，质量矩阵 $M(q)$
\State **采样动量:** $p \sim \Ncal(0, M(q))$
\State **半步动量更新:**
    $p \leftarrow p - \frac{2} \nabla_q U(q)
        + \frac{4} \nabla_q \big[ p^\top M(q)^{-1} p \big]$
\For{$l = 1$ **to** $L-1$}
    \State **全步位置更新:**
        $q \leftarrow q + \epsilon \cdot M(q)^{-1} p$
    \State **全步动量更新:**
        $p \leftarrow p - \epsilon \nabla_q U(q)
            + \frac{2} \nabla_q \big[ p^\top M(q)^{-1} p \big]$
\EndFor
\State **最后全步位置更新:**
    $q \leftarrow q + \epsilon \cdot M(q)^{-1} p$
\State **最后半步动量更新:**
    $p \leftarrow p - \frac{2} \nabla_q U(q)
        + \frac{4} \nabla_q \big[ p^\top M(q)^{-1} p \big]$
\State **Metropolis 接受:**
    $A(q'|q) = \min(1, \exp(H(q,p) - H(q',p')))$
\end{algorithmic}
\end{algorithm-env}

> **Remark:** 当 $M(q) \equiv I$（单位矩阵，即 $\Situs$ 平坦），上述算法退化为标准欧几里得
> HMC。因此，Situs-HMC 是标准 HMC 的**严格推广**。

### 遍历性证明

> **Theorem:** [Situs-HMC 的遍历性 Ergodicity of Situs-HMC]
> <!-- label: thm:ergodicity -->
> 设 $\Situs$ 为紧致光滑黎曼流形，Cercis 函数 $Cercis: \Situs \to \R$ 为
> $C^2$ 光滑，且 Situs 度规 $h_ = \nabla^2 \mathcal{S}$ 在 $\Situs$ 上
> 一致正定（即存在 $\lambda_ > 0$ 使得对所有 $q \in \Situs$ 有
> $h_(q) \succeq \lambda_ I$）。则具有广义蛙跳积分器和非零步长
> $\epsilon > 0$ 的 Situs-HMC 链是
> 
> 
1. **$\pi_\beta$-不变的：** $\pi_\beta$ 是转移核 $T_\epsilon$ 的平稳分布。
2. **不可约的：** 对任意开集 $A \subset \Situs$ 且 $\pi_\beta(A) > 0$，
3. **非周期的：** 不存在对状态空间的非平凡周期划分。
4. **遍历的：** 对任意 $\pi_\beta$-可积函数 $f$，

> **Proof:** [证明概要 Proof Sketch]
> (i) 由哈密顿动力学的辛结构和蛙跳积分器的保辛性质，结合 Metropolis 校正步骤的
> 细致平衡条件直接可得。蛙跳积分器的 Jacobi 行列式为 1 保证了体积守恒。
> 
> (ii) 紧致流形上，正定度规条件保证存在 $\delta > 0$ 使得在任意点 $q \in \Situs$，
> 单步蛙跳更新的可达集包含半径为 $\delta$ 的开球。由 $\Situs$ 的紧致性和连通性，
> 有限步内可达整个流形。
> 
> (iii) 非周期性来自 Metropolis 拒绝步骤引入的非零拒绝概率，打破任何确定性周期。
> 
> (iv) 由 (i)-(iii) 和标准遍历定理（Birkhoff 个体遍历定理在紧致状态空间上的形式）
> 直接可得。详细的测度论构造参见附录。

> **Corollary:** [遍历性仅需温和条件]
> 遍历性的充要条件仅为：(a) $\Situs$ 紧致，(b) $Cercis \in C^2$，以及
> (c) $h_$ 一致正定。对 SCX 审计而言，这些条件均在标准设定下自动满足：
> $\Situs$ 的紧致性来自规范约束 $\sum_j g_{ij} = 0$ 和有限势能范围；
> $Cercis$ 作为二次型自然 $C^\infty$ 光滑；$h_$ 的正定性由审计势能面
> 的凸性保证。

### 实践考虑：自适应步长

在 Situs 流形上，单一全局步长 $\epsilon$ 最优性不足。我们提出自适应方案：

$$<!-- label: eq:adaptive -->
    \epsilon_k = \epsilon_0 \cdot \min\!\left(1, \frac{\bar}{\lambda_(h_(q_k))}\right)
$$

其中 $\bar = \frac{1}{|\Situs|} \int_ \Tr(h_(q)) \, dq$ 为
平均特征值。在高度弯曲区域（$\lambda_$ 大），步长自动减小；在平坦区域，
步长恢复至 $\epsilon_0$。

---

# 第二部分：在线审计的序贯蒙特卡洛
# Part II: Sequential Monte Carlo for Online Audit
\addcontentsline{toc}{part}{Part II: Sequential Monte Carlo for Online Audit}

## SMC 理论框架
## SMC Theoretical Framework
\addcontentsline{toc}{section}{2. SMC Theoretical Framework}

### 在线审计的序贯性质

实际 SCX 审计中，新数据持续到达：新声明发布，新专家加入评审，现有专家更新
判断。这要求审计模型能够**在线更新**——无需从头重采样，而是利用已有后验
近似高效吸收新证据。

形式化地，设 $t = 1, 2, ..., T$ 为审计时间步，$\D_t$ 为截止时间 $t$ 的累积
数据。目标后验分布序列为：

$$<!-- label: eq:posterior_sequence -->
    \pi_t(E) = \Pbb(E \mid \D_t) \propto \pi_{t-1}(E) \cdot \Pbb(\D_t \setminus \D_{t-1} \mid E)
$$

序贯蒙特卡洛（SMC，也称粒子滤波）为这一序贯推断问题提供了自然框架。

### 粒子滤波算法

> **Definition:** [SMC 粒子集合 SMC Particle Ensemble]
> 在时间 $t$，SMC 维持一组 $K$ 个加权粒子：
> 
> $$
>     \{E_t^{(k)}, w_t^{(k)}\}_{k=1}^K,\quad \sum_{k=1}^K w_t^{(k)} = 1
> $$
> 
> 近似后验 $\pi_t(E) \approx \sum_{k=1}^K w_t^{(k)} \delta_{E_t^{(k)}}(E)$。

\begin{algorithm-env}[SCX 在线审计 SMC 算法]
\begin{algorithmic}[1]
\State **初始化 ($t=0$):**
    $E_0^{(k)} \sim \pi_0$ (先验)，$w_0^{(k)} \leftarrow 1/K$，对 $k=1,...,K$
\For{$t = 1$ **to** $T$}
    \State **重要性采样:**
        根据提议分布 $q_t(E \mid E_{t-1}^{(k)}, \D_t)$ 采样
        $\tilde{E}_t^{(k)}$
    \State **权重更新:**
        $\tilde{w}_t^{(k)} \leftarrow w_{t-1}^{(k)} \cdot
        \dfrac{\Pbb(\D_t \setminus \D_{t-1} \mid \tilde{E}_t^{(k)})
              \cdot \Pbb(\tilde{E}_t^{(k)} \mid E_{t-1}^{(k)})}
             {q_t(\tilde{E}_t^{(k)} \mid E_{t-1}^{(k)}, \D_t)}$
    \State **权重归一化:**
        $w_t^{(k)} \leftarrow \tilde{w}_t^{(k)} / \sum_{j=1}^K \tilde{w}_t^{(j)}$
    \State **计算 ESS:**
        $\ESS_t \leftarrow \big(\sum_{k=1}^K (w_t^{(k)})^2\big)^{-1}$
    \If{$\ESS_t < \alpha K$（如 $\alpha = 0.5$）}
        \State **重采样:**
            $E_t^{(k)} \sim \sum_{j=1}^K w_t^{(j)} \delta_{\tilde{E}_t^{(j)}(E)}$，
            $w_t^{(k)} \leftarrow 1/K$
    \EndIf
\EndFor
\end{algorithmic}
\end{algorithm-env}

### 有效样本量下界

> **Theorem:** [SMC 有效样本量界 ESS Bound for SCX-SMC]
> <!-- label: thm:ess_bound -->
> 设 $\D_t$ 满足有界似然比条件：存在 $B < \infty$ 使得对所有 $E$，
> 
> $$
>     \frac{\Pbb(\D_t \setminus \D_{t-1} \mid E)}{\max_{E'} \Pbb(\D_t \setminus \D_{t-1} \mid E')} \geq \frac{1}{B}
> $$
> 
> 且提议分布满足 $q_t(\cdot) = \pi_{t-1}(\cdot)$（bootstrap 滤波）。则有效样本量的
> 期望下界为：
> 
> 
> $$<!-- label: eq:ess_bound -->
>     \E[\ESS_t] \geq \frac{K}{B^2}
> $$
> 
> 
> 特别地，$\ESS_t \geq \frac{K}{B^2 \log(1/\delta)}$ 以概率至少 $1-\delta$ 成立。

> **Proof:** 在 bootstrap 滤波 $q_t = \pi_{t-1}$ 下，非归一化权重简化为
> $\tilde{w}_t^{(k)} = \Pbb(\D_t \setminus \D_{t-1} \mid \tilde{E}_t^{(k)})$。
> 有界似然比条件给出 $\tilde{w}_ / \tilde{w}_ \leq B$。
> 由 Cauchy-Schwarz，
> $\ESS_t = \frac{(\sum w_k)^2}{\sum w_k^2} \geq \frac{K \cdot w_^2}{w_^2} \geq \frac{K}{B^2}$。
> 概率版本由 Markov 不等式给出。

> **Corollary:** [SCX 审计的 ESS 条件]
> SCX 在线审计的 ESS 退化由似然比界 $B$ 控制。当新数据与新粒子状态高度一致时
> $B \approx 1$，ESS 接近 $K$；当新数据与新粒子状态剧烈冲突时 $B$ 很大，
> 需要增加粒子数或降低重采样阈值 $\alpha$。

### 审计数据到达的粒子自适应

SCX 审计中的关键挑战：新数据 $\D_t$ 可能来自三类源：

1. **新声明 (new claims):** 新声明引入新维度 $m \to m+1$，粒子空间
2. **新专家评审 (new reviews):** 新专家引入新规范姿态 $g_{\cdot, n+1}$。
3. **修正评审 (revised reviews):** 现有专家更新判断。处理：仅需

\begin{algobox}[SCX 审计数据的粒子自适应 Particle Adaptation for SCX Audit Data]
**新声明：**

1. 扩展粒子维度：$E_{new} = [E_{old}, g_{new,1}, ..., g_{new,n}]$
2. 从先验采样新维度：$g_{new,j} \sim \Ncal(0, \sigma^2)$
3. 保持旧权重不变（未涉及旧状态）

**新专家评审：**

1. 扩展粒子维度：$E_{new} = [E_{old}, g_{1,new}, ..., g_{m,new}]$
2. 从先验或基于已有专家的相关性采样
3. 重新权重：考虑新专家与已有专家的一致性

**修正评审：**

1. 粒子状态不变
2. 仅重新计算权重：$w_k \propto w_k^{old} \cdot \Pbb(修正 \mid E^{(k)})$
3. 如 ESS 不足，在受影响的维度子集上重采样

\end{algobox}

### 收敛性分析

> **Theorem:** [SCX-SMC 均方误差界 MSE Bound]
> 设 $\pi_t$ 为 $t$ 时刻的真实后验，$\hat_t^K$ 为 $K$ 个粒子的 SMC 近似。
> 则在温和正则条件下，对任意有界检验函数 $\phi$：
> 
> 
> $$<!-- label: eq:mse_bound -->
>     \E\!\left[ \Big( \int \phi(E) \hat_t^K(dE) - \int \phi(E) \pi_t(dE) \Big)^2 \right] \leq \frac{C_t \|\phi\|_\infty^2}{K}
> $$
> 
> 
> 其中 $C_t$ 依赖于 $B$（似然比界）和对数时间 $t$：
> $C_t = \Ocal(B^{2t} \log t)$。对于 SCX 审计，$t$ 通常为 $\Ocal(1)$ 到
> $\Ocal(10^2)$，$B \approx 2$–$5$，此时 $C_t$ 在可行范围内。

---

# 第三部分：Cercis 校准的热力学积分
# Part III: Thermodynamic Integration for Cercis Calibration
\addcontentsline{toc}{part}{Part III: Thermodynamic Integration for Cercis Calibration}

## 热力学积分理论
## Thermodynamic Integration Theory
\addcontentsline{toc}{section}{3. Thermodynamic Integration Theory}

### Cercis 校准问题

Cercis 分数 $Cercis(E)$ 作为审计"不协调度"度量，其**校准**（calibration）
至关重要：对给定审计问题，$Cercis(E)$ 的绝对数值应能够区分"良好共识"与
"系统性偏差"。校准的核心是确定配分函数 $Z(\beta)$ 及其导数——

$$<!-- label: eq:free_energy -->
    F(\beta) = -\frac{1} \log Z(\beta),\quad
    \frac{dF}{d\beta} = \E_{\pi_\beta}[Cercis(E)]
$$

从高信噪比（$\beta_{high}$，容易审计）到低信噪比（$\beta_{low}$，
困难审计）的**自由能差** $\Delta F = F(\beta_{low}) - F(\beta_{high})$
提供了 Cercis 的校准基准。

### 热力学积分的数学框架

自由能差通过热力学积分（Thermodynamic Integration, TI）计算：

$$<!-- label: eq:ti -->
    \Delta F = \int_{\beta_{high}}^{\beta_{low}} \E_{\pi_\beta}[Cercis(E)] \, d\beta
$$

在实际计算中，在离散温度网格 $\beta_0, \beta_1, ..., \beta_R$ 上
（$\beta_0 = \beta_{high}, \beta_R = \beta_{low}$），每个
$\beta_r$ 运行 MCMC 获得样本 $\{E^{(r,k)}\}_{k=1}^{N_r}$，然后数值积分：

$$<!-- label: eq:ti_discrete -->
    \Delta F \approx \sum_{r=0}^{R-1} \frac{(\beta_{r+1} - \beta_r)}{2}
    \Big( \bar{Cercis}_r + \bar{Cercis}_{r+1} \Big)
$$

其中 $\bar{Cercis}_r = \frac{1}{N_r} \sum_{k=1}^{N_r} Cercis(E^{(r,k)})$ 为
温度 $\beta_r$ 下的样本平均。

### 温度调度：从易到难

> **Definition:** [信噪比-温度对应 SNR-Temperature Correspondence]
> 审计问题的信噪比与逆温度 $\beta$ 存在单调对应关系：
> 
> 
- **高 SNR (高 $\beta$):** 审计信号强，$Cercis$ 表面深谷明确。
- **低 SNR (低 $\beta$):** 审计信号弱，$Cercis$ 表面浅而平坦。

> 
> 温度调度 $\beta_0 > \beta_1 > ... > \beta_R$ 实现从"易"到"难"的审计
> 退火。

\begin{keyeq}
**SCX 审计的热力学恒等式：**

$$
    \Cercis_{cal} &\equiv \Delta F = F(\beta_{low}) - F(\beta_{high})
        <!-- label: eq:cercis_cal --> 

    &= \int_{\beta_{high}}^{\beta_{low}} \E_{\pi_\beta}[Cercis(E)] \, d\beta
        <!-- label: eq:cercis_ti --> 

    &= \int_{\beta_{high}}^{\beta_{low}} \frac{\int_ Cercis(E) e^{-\beta Cercis(E)} dE}
        {\int_ e^{-\beta Cercis(E)} dE} \, d\beta <!-- label: eq:cercis_explicit -->
$$

$\Cercis_{cal}$ 是 Cercis 分数的校准常量：审计问题的"内在难度"。
\end{keyeq}

### 温度网格优化

温度点的选择对 TI 精度至关重要。我们采用两种优化策略：

> **Theorem:** [最优温度网格 Optimal Temperature Grid]
> <!-- label: thm:temp_grid -->
> 在总计算预算 $B = \sum_r N_r$ 下，最小化 $\Delta F$ 的均方误差要求温度点按
> *热容密度* 分布：
> 
> 
> $$<!-- label: eq:temp_spacing -->
>     \Delta\beta_r \propto \frac{1}{\sqrt{\Var_{\pi_{\beta_r}}[Cercis(E)]}}
> $$
> 
> 
> 其中 $\Var_{\pi_{\beta_r}}[Cercis(E)]$ 为 $Cercis$ 在温度 $\beta_r$ 下的方差
> （热容 $C_V(\beta_r) = \beta_r^2 \Var_{\pi_\beta}[Cercis]$）。在相变区域，
> 热容激增，网格应自动加密。

> **Proof:** 由 $\delta$-方法，$\hat{F}$ 的方差近似为
> $\Var[\hat{F}] \approx \sum_r (\Delta\beta_r)^2 \cdot \Var[\bar{Cercis}_r]$。
> 在约束 $\sum_r N_r = B$ 和 $\sum_r \Delta\beta_r = \beta_{high} - \beta_{low}$
> 下，利用拉格朗日乘数法最小化方差，得最优分布
> $\Delta\beta_r \propto 1/\sqrt{\Var[Cercis]_r}$。

### SCX 审计中的相变现象

> **Conjecture:** [审计相变 Audit Phase Transition]
> 在临界温度 $\beta_c = \frac{1}{T_c}$ 处，SCX 审计经历一次**二级相变**：
> 
> 
- $\beta > \beta_c$（低温）：系统呈现有序相——专家实质上达成共识
- $\beta < \beta_c$（高温）：系统呈现无序相——专家判断随机分散。
- $\beta \approx \beta_c$：热容在热力学极限下发散 $C_V \sim |\beta - \beta_c|^{-\alpha}$。

> 
> $\beta_c$ 由审计问题的性质决定：专家组规模、声明的模糊性、数据的信噪比。
> 临界指数 $\alpha$ 反映了审计问题的"维数"。

> **Remark:** 审计相变的存在意味着：对于足够困难的审计问题（$\beta < \beta_c$），
> 即使调用无限计算资源，也无法唯一确定专家共识——审计结果**本征地**不确定。
> 这是 SCX 审计的**不确定性原理**的统计力学形式。

### TI 的实用实现

\begin{algorithm-env}[SCX 审计的热力学积分 TI for SCX Audit]
\begin{algorithmic}[1]
\State **输入:** 温度范围 $[\beta_{low}, \beta_{high}]$，
        初始网格点数 $R_0$，每温度样本数 $N$，自适应公差 $\tau$
\State **初始化:** 设置温度网格 $\beta_0 = \beta_{high}, ..., \beta_{R_0} = \beta_{low}$
\For{$r = 0$ **to** $R_0$}
    \State 在温度 $\beta_r$ 运行 Situs-HMC（算法 1.1），获得 $N$ 个样本
    \State 计算 $\bar{Cercis}_r$ 和 $\sigma_r^2 = \Var[Cercis]_r$
\EndFor
\State **自适应加密:**
\While{$\max_r \sigma_r^2 \cdot (\Delta\beta_r)^2 > \tau$}
    \State 在 $\sigma_r^2$ 最大的区间中点插入新温度点
    \State 在新温度点运行 Situs-HMC
    \State 更新 $\bar{Cercis}_r$ 和 $\sigma_r^2$
\EndWhile
\State **Trapezoidal 积分:**
    $\Cercis_{cal} \leftarrow \sum_{r=0}^{R-1} \frac{\beta_{r+1} - \beta_r}{2} (\bar{Cercis}_r + \bar{Cercis}_{r+1})$
\State **返回:** $\Cercis_{cal}$ 及估计标准误差
\end{algorithmic}
\end{algorithm-env}

---

# 第四部分：多专家共识的副本交换蒙特卡洛
# Part IV: Replica Exchange for Multi-Expert Consensus
\addcontentsline{toc}{part}{Part IV: Replica Exchange for Multi-Expert Consensus}

## 副本交换理论
## Replica Exchange Theory
\addcontentsline{toc}{section}{4. Replica Exchange Theory}

### 多模态挑战与副本交换

SCX 审计中，多专家共识面临一个根本挑战：专家配置空间 $\Situs$ 可能存在多个
局部最优（多种可能的共识配置）。例如：

1. **模棱两可的声明：** 两种互斥解读均有优秀专家支持，导致两个分离
2. **专家派系：** 不同方法论阵营的专家形成聚类，各聚类内部高度一致
3. **时间演化中的亚稳态：** 共识随时间演化，链可能陷入过去的共识

单一温度下的 HMC/SMC 链可能被困在某个 $Cercis$ 低谷中，无法探索整个配置空间。
**副本交换蒙特卡洛**（Replica Exchange Monte Carlo, REX，也称并行回火
Parallel Tempering）通过在不同温度运行多个副本（replica）并周期性交换状态来
解决多模态问题。

### REX 的数学框架

设 $R$ 个副本，温度 $T_1 < T_2 < ... < T_R$（逆温度
$\beta_1 > \beta_2 > ... > \beta_R$）。副本 $r$ 在温度 $T_r$ 下独立演化，
目标分布 $\pi_{\beta_r}(E) \propto \exp(-\beta_r Cercis(E))$。

**联合分布：** 副本之间统计独立，因此 $R$ 个副本的整体分布为乘积：

$$<!-- label: eq:rex_joint -->
    \Pi(E^{(1)}, ..., E^{(R)}) = \prod_{r=1}^R \pi_{\beta_r}(E^{(r)})
        \propto \prod_{r=1}^R \exp(-\beta_r Cercis(E^{(r)}))
$$

**交换操作：** 相邻副本 $r$ 和 $r+1$ 的交换以 Metropolis 概率接受：

$$<!-- label: eq:swap_prob -->
    A_{swap} = \min\!\Bigg(1,
        \frac{\pi_{\beta_r}(E^{(r+1)}) \cdot \pi_{\beta_{r+1}}(E^{(r)})}
             {\pi_{\beta_r}(E^{(r)}) \cdot \pi_{\beta_{r+1}}(E^{(r+1)})}
    \Bigg)
$$

化简得：

$$<!-- label: eq:swap_simplified -->
    A_{swap} = \min\!\Big(1,
        \exp\!\big( (\beta_r - \beta_{r+1}) \cdot [Cercis(E^{(r)}) - Cercis(E^{(r+1)})] \big)
    \Big)
$$

\begin{keyeq}
**副本交换接受率：**

$$
    A_{swap}(r \leftrightarrow r+1) =
    \min\!\Bigg(1, \exp\!\Big(
        \underbrace{(\beta_r - \beta_{r+1})}_{\Delta\beta > 0}
        \cdot
        \underbrace{[Cercis(E^{(r)}) - Cercis(E^{(r+1)})]}_{\Delta Cercis}
    \Big)\Bigg)
$$

当高温副本（更高的 $Cercis$）与低温副本（更低的 $Cercis$）交换时，
$\DeltaCercis > 0$，接受率高。这实现了**低温副本的全局探索**：
高温副本广泛探索配置空间，通过交换将发现的模式传递给低温副本。
\end{keyeq}

### 温度阶梯设计

温度阶梯的设计决定 REX 的效率。核心权衡：

> **Definition:** [温度阶梯的最优条件 Optimal Temperature Ladder]
> 设 $R$ 个副本，温度 $T_1 < ... < T_R$。最优阶梯满足：
> 
> 
1. **均匀交换率：** 所有相邻对的交换接受率近似相等
2. **充分覆盖：** $T_R$ 足够高，使得副本 $R$ 能够自由遍历配置空间
3. **精度保持：** $T_1$ 足够低，使得副本 1 的采样集中于 $Cercis$ 低谷

> **Proposition:** [最优温度间隔 Optimal Spacing]
> 在假设 $Cercis(E)$ 在温度 $T$ 下近似正态分布的前提下，期望交换接受率约为
> $\bar{A} \approx 2\Phi\!\big(-\frac{\Delta\beta \cdot \sigma_Cercis}{2}\big)$
> （其中 $\Phi$ 为标准正态 CDF）。为维持均匀接受率 $\bar{A}$，温度点应满足：
> 
> 
> $$<!-- label: eq:temp_ladder -->
>     T_{r+1} \approx T_r \cdot \left(1 + \frac{c}{\sqrt{n_{eff}}}\right)
> $$
> 
> 
> 其中 $c = -2\Phi^{-1}(\bar{A}/2)$，$n_{eff}$ 为系统的有效自由度。
> 对于典型 SCX 审计 ($n_{eff} \sim 10$–$100$，$\bar{A} \approx 0.3$)，
> $T_{r+1}/T_r \approx 1.15$–$1.5$。

### SCX 多专家共识的 REX 算法

\begin{algorithm-env}[SCX 多专家共识的副本交换 REX for SCX Multi-Expert Consensus]
\begin{algorithmic}[1]
\State **输入:** 副本数 $R$，温度阶梯 $\{T_r\}_{r=1}^R$，
        每温度 HMC 步数 $L$，交换间隔 $S$，总迭代数 $N_{iter}$
\State **初始化:** 随机初始化 $E_0^{(r)} \sim \pi_{\beta_r}$ 对 $r=1,...,R$
\For{$n = 1$ **to** $N_{iter}$}
    \State **本地演化:**
    \For{$r = 1$ **to** $R$} \Comment{各副本独立演化}
        \State $E_n^{(r)} \leftarrow$ 对 $E_{n-1}^{(r)}$ 运行 $L$ 步 Situs-HMC
            (温度 $T_r$)
    \EndFor
    \If{$n \bmod S = 0$} \Comment{每隔 $S$ 步交换}
        \For{$r = 1$ **to** $R-1$}
            \State 计算 $\Delta = (\beta_r - \beta_{r+1}) \cdot
                [Cercis(E_n^{(r)}) - Cercis(E_n^{(r+1)})]$
            \State $A \leftarrow \min(1, \exp(\Delta))$
            \If{$Uniform(0,1) < A$}
                \State 交换 $E_n^{(r)} \leftrightarrow E_n^{(r+1)}$
            \EndIf
        \EndFor
    \EndIf
\EndFor
\State **共识诊断（对低温副本 $r=1$ 的样本）:**
\State 计算各声明 $i$ 的 $\hat{g}_{ij} = mean(\{E^{(1)}_n\})$ 和
    $\hat_{ij} = std(\{E^{(1)}_n\})$
\State 识别多模态：对各声明 $i$，检验 $\{g_{ij}\}$ 的分布是否为多峰的
    （如 Hartigan dip test）
\State **返回:** 共识估计、不确定度、多模态标记
\end{algorithmic}
\end{algorithm-env}

### REX 的遍历性加速

> **Theorem:** [REX 的混合加速 Mixing Acceleration by REX]
> <!-- label: thm:rex_mixing -->
> 设单一温度 $T$ 的 HMC 链的混合时间为 $\tau_{mix}(T)$。则在包含 $R$ 个副本
> 且温度范围 $[T_, T_]$ 的 REX 方案下，低温副本（$T_$）的
> 有效混合时间为：
> 
> 
> $$<!-- label: eq:rex_mixing_time -->
>     \tau_{mix}^{REX}(T_) \leq
>     \tau_{mix}(T_) \cdot \min_{r} \left\{
>         \frac{1}{\bar{A}_{r,r+1}} \cdot
>         \frac{\tau_{mix}(T_r)}{\tau_{mix}(T_)}
>     \right\}
> $$
> 
> 
> 其中 $\bar{A}_{r,r+1}$ 为相邻副本的平均交换接受率。当 $T_R \gg T_{crit}$
> 且 $\bar{A}_{r,r+1} \approx 0.2$–$0.5$ 时，加速因子可达 $\Ocal(10^2)$–
> $\Ocal(10^4)$。

> **Remark:** REX 的加速本质上来自**温度加速的隧道效应**：高温副本迅速穿越能量壁垒，
> 通过交换将"知识"传递至低温副本。对于 SCX 审计，这对应于：用宽松标准（高 $T$）
> 快速扫描可能的共识配置，然后用严格标准（低 $T$）精确校准最有希望的配置。

---

# 第五部分：MCMC 收敛诊断
# Part V: MCMC Convergence Diagnostics
\addcontentsline{toc}{part}{Part V: MCMC Convergence Diagnostics}

## 审计收敛的形式化
## Formalizing Audit Convergence
\addcontentsline{toc}{section}{5. Formalizing Audit Convergence}

### 为什么收敛诊断对审计至关重要

SCX 审计的蒙特卡洛方法涉及一个根本问题：**我们怎么知道链已经"足够好"地
收敛了？** 未收敛的链给出的审计结果可能是：

- **系统性偏差：** 链仍被初始条件影响，未探索整个后验
- **过度自信：** 尚未访问的低概率区域可能导致低估不确定度
- **多模态遗漏：** 单一链可能仅发现多模态后验中的一个模态

**审计收敛标准：** 一个 SCX 审计是**收敛的**，当且仅当对所有规范参数
$g_i$（即声明 $i$ 的 $\sum_j g_{ij}$，或等价地，各专家的 $g_{ij}$ 质量加权的
综合规范姿态），Gelman-Rubin 统计量 $\Rhat < 1.01$。

### Gelman-Rubin 诊断

> **Definition:** [Gelman-Rubin $\Rhat$ 统计量]
> 对于 $M$ 条链（$M \geq 2$），每条链 $N$ 个后燃烧期样本。对参数 $\theta$，
> 定义：
> 
> 
> **链内方差 (within-chain variance):**
> 
> $$<!-- label: eq:W -->
>     W = \frac{1}{M} \sum_{m=1}^M s_m^2,\quad
>     s_m^2 = \frac{1}{N-1} \sum_{n=1}^N (\theta_{mn} - \bar_m)^2
> $$
> 
> 
> **链间方差 (between-chain variance):**
> 
> $$<!-- label: eq:B -->
>     B = \frac{N}{M-1} \sum_{m=1}^M (\bar_m - \bar)^2,\quad
>     \bar = \frac{1}{M} \sum_{m=1}^M \bar_m
> $$
> 
> 
> **边际后验方差估计:**
> 
> $$<!-- label: eq:var_plus -->
>     \widehat^+(\theta) = \frac{N-1}{N} W + \frac{1}{N} B
> $$
> 
> 
> **$\Rhat$ 统计量:**
> 
> $$<!-- label: eq:Rhat -->
>     \Rhat = \sqrt{\frac{\widehat^+(\theta)}{W}}
> $$

> **Theorem:** [Gelman-Rubin 收敛判据的审计形式]
> <!-- label: thm:rhat_criterion -->
> 如果 $M$ 条链均已充分混合（即 $\widehat^+$ 和 $W$ 均已稳定），则
> $\Rhat \approx 1$。正式的审计收敛判据为：
> 
> 
> $$<!-- label: eq:audit_converged -->
>     审计收敛 \quad \Longleftrightarrow \quad
>     \max_{i} \Rhat(g_i) < 1.01
> $$
> 
> 
> 其中 $\max_{i}$ 取遍所有独立规范参数。

> **Remark:** $\Rhat < 1.01$ 是比标准贝叶斯分析中常用的 $\Rhat < 1.1$ 更严格的标准。
> SCX 审计要求更高的精度，因为：(a) 审计结果可能影响重大决策；
> (b) 规范参数 $g_i$ 之间高度相关，单一参数的微小偏差可能通过约束
> $\sum g = 0$ 传播。

### 有效样本量

> **Definition:** [有效样本量 Effective Sample Size]
> 对于具有自相关 $\rho_k = \Corr(\theta_t, \theta_{t+k})$ 的单条链，
> 有效样本量为：
> 
> 
> $$<!-- label: eq:ess_def -->
>     \ESS = \frac{N}{1 + 2 \sum_{k=1}^\infty \rho_k}
> $$
> 
> 
> 在实际中，使用截断自相关和：
> $\ESS \approx N / (1 + 2 \sum_{k=1}^{K_} \hat_k)$，
> 其中 $K_$ 取 $\hat_k$ 降为低于噪声水平的最小 $k$。

> **Proposition:** [SCX 审计的最小 ESS 要求]
> 对于可靠的 SCX 审计推断，我们要求：
> 
1. 对于点估计（$\hat{g}_{ij}$ 的期望）：$\ESS \geq 100$
2. 对于不确定度估计（$\widehat[g_{ij}]$）：$\ESS \geq 400$
3. 对于尾部概率（如异常值检测）：$\ESS \geq 1000$

> 这些阈值基于：后验均值估计精度 $\Ocal(\ESS^{-1/2})$，
> 方差估计精度 $\Ocal(\ESS^{-1/2})$，以及尾部分位数的更高方差。

### 多链初始化策略

\begin{algobox}[SCX 审计多链初始化 Multi-Chain Initialization for SCX Audit]
为确保链的独立性（从而 $\Rhat$ 的有效性），我们采用**过度离散初始化**：

1. **链 1（共识先验）：** $g_{ij} \sim \Ncal(0, 0.1)$——预期共识
2. **链 2（分歧先验）：** $g_{ij} \sim \Ncal(0, 1.0)$——大分歧可能
3. **链 3（偏斜先验）：** $g_{ij} \sim SkewNormal(0, 0.5, \alpha=3)$
4. **链 4（反偏斜先验）：** $g_{ij} \sim SkewNormal(0, 0.5, \alpha=-3)$
5. **链 5-8（随机先验）：** $g_{ij} \sim \Ncal(0, \sigma_j^2)$ 其中

所有 $M$ 条链独立运行，燃烧期后比较 $\Rhat$。
\end{algobox}

### Rank 归一化与分位点收敛

除了 $\Rhat$ 和 ESS，我们使用**Rank 归一化**诊断：

> **Definition:** [Rank 归一化诊断 Rank-Normalized Diagnostic]
> 将 $M$ 条链的后燃烧期样本合并，对参数 $\theta$ 进行 Rank 变换：
> $r_{mn} = rank(\theta_{mn})$（范围 $1$ 到 $MN$），然后标准化到
> $[0,1]$：$z_{mn} = (r_{mn} - 0.5) / (MN)$。
> 
> 如果各链混合良好，$z_{mn}$ 应在 $[0,1]$ 上均匀分布，且链间分布无显著差异
> （通过 Kolmogorov-Smirnov 检验）。

> **Theorem:** [审计收敛的综合诊断综合指标 Composite Diagnostic]
> 一个 SCX 审计是**全面收敛的**（fully converged）当且仅当：
> 
> 
> $$<!-- label: eq:composite_diag -->
>     \begin{cases}
>         \max_i \Rhat(g_i) < 1.01 & (Gelman-Rubin) 
>         \min_i \ESS(g_i) > 400 & (有效样本量) 
>         \max_i KS-p-value > 0.05 & (Rank 均匀性) 
>         无趋势 & (迹线图目视检查)
>     \end{cases}
> $$
> 
> 
> 同时满足以上四项条件的审计结果才可被视为可靠。

### 迹线图诊断与早期停止

\begin{algorithm-env}[自适应早期停止 Adaptive Early Stopping]
\begin{algorithmic}[1]
\State **输入:** 目标参数 $\theta$，最小迭代 $N_$，窗口大小 $w$
\State 初始化：$n \leftarrow 0$，历史 $\Rhat$ 序列 $\mathcal{R} \leftarrow []$
\While{$n < N_$ **或** $未收敛$}
    \State 对所有 $M$ 条链运行附加的 $L$ 步
    \State $n \leftarrow n + L$
    \State 计算最后 $w$ 个样本的 $\Rhat(\theta)$
    \State $\mathcal{R}.append(\Rhat(\theta))$
    \If{$|\mathcal{R}| \geq 3$}
        \State 拟合 $\Rhat_t = a \cdot t^{-b} + 1$ 对最后 3 个点
        \State 如果 $a < 0.01$ 且 $b > 0$（即 $\Rhat$ 已趋于 1），
            **break**
    \EndIf
\EndWhile
\State **返回:** 收敛状态，$\Rhat$ 值，ESS
\end{algorithmic}
\end{algorithm-env}

### SCX 审计收敛的相图

[Figure omitted — see original .tex]

---

## 方法集成与审计流水线
## Method Integration and Audit Pipeline
\addcontentsline{toc}{section}{6. Method Integration and Audit Pipeline}

### 完整审计流水线

以上五种方法构成一个完整的 SCX 审计流水线：

1. **校准 (TI):** 使用热力学积分确定 Cercis 校准常量
2. **初始化 (REX):** 使用副本交换在广泛温度范围探索配置空间，
3. **精确采样 (HMC):** 利用 Situs 度规进行黎曼 HMC 精确采样，
4. **在线更新 (SMC):** 随新数据到达，序贯更新粒子，维持近似后验。
5. **收敛验证 ($\Rhat$/ESS):** 持续监测 $\Rhat$、ESS 和 Rank

### 计算复杂度分析

[Table omitted — see original .tex]

其中 $m$ = 声明数，$n$ = 专家数，$K$ = 粒子数，$R$ = 温度点数，
$L$ = 蛙跳步数，$N$ = 后燃烧期样本数，$T$ = SMC 时间步数。

> **Remark:** 所有方法的**最昂贵**操作是 Cercis 函数求值（$\Ocal(mn)$）和
> Situs 度规求值（$\Ocal(m^2n^2)$）。对于大规模审计问题
> （$m \sim 10^4$, $n \sim 10^3$），Situs 度规的求值可通过稀疏近似加速。

### 数值示例：小型审计验证

考虑一个涉及 $m=5$ 个声明、$n=3$ 个专家的小型审计问题。使用 verify\_monte\_carlo.py
脚本验证所有五种方法（参见附录）。

**预期结果：**

1. **HMC:** Situs-HMC 的 ESS 应为欧几里得 HMC 的 $2$–$5$ 倍
2. **SMC:** 随 $t \to T$，ESS 应保持在 $K/2$ 以上
3. **TI:** $\Cercis_{cal}$ 的估计应稳定（Monte Carlo 标准
4. **REX:** 低温副本应访问所有 $Cercis$ 的低谷（如多模态存在）。
5. **$\Rhat$:** 充分迭代后，所有 $g_i$ 满足 $\Rhat < 1.01$。

---

## Appendix
## 验证脚本：verify\_monte\_carlo.py
## Verification Script: verify\_monte\_carlo.py
\addcontentsline{toc}{section}{Appendix A: Verification Script}

以下 Python 脚本实现了本文描述的五种蒙特卡洛方法的端到端验证。
该脚本自包含（仅依赖 numpy），可直接在 SCX 工作环境中运行。

\begin{verbatim}
参见附带文件：verify_monte_carlo.py
(Refer to accompanying file: verify_monte_carlo.py)
\end{verbatim}

### 验证脚本结构

脚本包含以下模块：

1. **Situs 流形构建器：** 定义 $\Situs$ 流形、Situs 度规、Cercis 函数
2. **HMC 实现：** 欧几里得 HMC + Situs-HMC，包含蛙跳积分器和自适应步长
3. **SMC 实现：** 粒子滤波器，包含 ESS 监测和重采样
4. **TI 实现：** 温度网格 + 热力学积分 + 自适应加密
5. **REX 实现：** 并行回火 + 副本交换
6. **诊断实现：** $\Rhat$、ESS、Rank 均匀性、迹线图生成
7. **测试框架：** 所有方法的端到端测试 + 断言验证

---

## 核心公式速查
## Key Formulas Reference
\addcontentsline{toc}{section}{Appendix B: Key Formulas Reference}

<div align="center">

[Table omitted — see original .tex]

</div>

---

## 致谢 Acknowledgments
\addcontentsline{toc}{section}{致谢 Acknowledgments}

感谢 SCX 审计理论的所有贡献者。本文中的蒙特卡洛方法借鉴了物理学、统计学
和计算机科学的经典思想，以全新的视角应用于社会系统的审计问题。
特别感谢 Duane et al. (1987) 的 HMC 开创性工作、
Gordon et al. (1993) 的粒子滤波、Gelman \& Rubin (1992) 的收敛诊断、
以及 Swendsen \& Wang (1986) 的副本交换方法。

*We acknowledge the foundational contributions of Duane et al. (1987)
for HMC, Gordon et al. (1993) for particle filters, Gelman \& Rubin (1992) for
convergence diagnostics, and Swendsen \& Wang (1986) for replica exchange methods.
The novelty of this work lies not in inventing these methods, but in their
systematic application to SCX audit problems — and in demonstrating that the
Situs manifold provides the natural geometric setting for this application.*

<div align="center">

\rule{0.5\textwidth}{0.5pt}
{ **万物可采样，万象皆收敛。**}
{ *All things are samplable. All phenomena converge.*}
{ — SCX Monte Carlo, 2026-07-02}

</div>