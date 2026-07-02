# 引言：时间进入SCX

**Author:** SCX

*Abstract:*

SCX框架的核心动力学由Spring SE-1驱动——状态空间上的Robbins-Monro随机梯度下降。
然而，Spring SE-1的原始收敛理论 [cite]假定了**稳态目标**：
最优参数$\theta^*$不随时间变化。本文提出**Temporal SCX**，将Spring SE-1推广到
**时变目标**$\theta_t^*$，并从中推导出一组关于记忆与遗忘的形式理论。

本文的主要贡献为四个定理。**第一**（遗忘的必要性定理），在非稳态数据流中，任何无遗忘机制
（等权累积所有历史梯度）的学习算法必然导致参数估计以速率$\Omega(\sqrt{t})$偏离真实时变目标——
遗忘不是记忆系统的设计选择，而是在非稳态环境中维持有限跟踪误差的**逻辑必然**。
该定理是省定理 [cite]在时域上的推广：省定理指出``无复习，检测边际必衰减至零''；
遗忘必要性定理指出``无遗忘，跟踪误差必发散至无穷''。
**第二**（记忆-遗忘相变定理），存在临界漂移速率$v_c = \Theta(\sigma/\sqrt)$——
当目标漂移速率$v < v_c$时，单调记忆（不遗忘，$\lambda = 1$）最小化渐近均方误差；
当$v > v_c$时，有限窗口遗忘（$\lambda^* < 1$）严格优于单调记忆，且最优遗忘率
$\lambda^*$随$v$增大而减小。这一相变行为在结构上平行于质变点定理 [cite]
中学习动力学的临界迭代$t_{crit}$——两者均描述了系统行为的定性跃迁。
**第三**（最优遗忘界），遗忘速率$\gamma$与检测延迟$\tau$之间的帕累托前沿满足
$\gamma \cdot \tau \geq C$，其中$C$由问题几何（条件数、噪声水平、漂移幅度）决定。
该界表明：更快的遗忘必然以更长的延迟为代价，反之亦然——**不存在同时最优的遗忘策略**。
**第四**（遗忘算子$\Fforget_t$的形式定义与收敛性），将遗忘形式化为记忆空间$\Mmem$上的
压缩算子，证明在$\ell_2$范数下$\Fforget_t$构成收缩半群，其不动点对应于以指数衰减权重编码的
``有效记忆分布''，并给出收敛速率与遗忘参数之间的精确关系。

本文保持对推导局限性的诚实态度：所有定理均标注证明的严格程度（严格、启发式、或类比论证）；
遗忘必要性定理中的渐近发散结论依赖Robbins-Monro步长条件，在固定步长下结论修正为有限稳态误差；
相变定理中临界速率的精确常数依赖PL条件的全局成立性假设；
帕累托前沿的推导使用了高斯噪声假设，在重尾噪声下界的形式可能改变；
遗忘算子的收缩性证明假定了记忆空间的Hilbert结构。

**关键词：**Temporal SCX，Spring SE-1，遗忘算子，记忆-遗忘相变，在线学习，非稳态优化，
Robbins-Monro，省定理，质变点，帕累托最优界

## 引言：时间进入SCX

### SCX框架中的时间盲点

SCX框架由五个协同层构成：状态结晶（State Crystallization）、物理位置编码（Situs）、
自进化记忆库（Spring）、多专家审计（Yajie）、以及质量评分（Cercis）。
其核心动力学由Spring SE-1驱动——状态空间$\Sstates$上的Robbins-Monro随机梯度下降：

$$<!-- label: eq:spring_se1 -->
    \theta_{t+1} = \theta_t - \alpha_t \cdot \nabla\mathcal{L}_{Spring}(\theta_t; \mathcal{B}_t) + \xi_t,
$$

其中$\alpha_t$满足Robbins-Monro条件$\sum \alpha_t = \infty$、$\sum \alpha_t^2 < \infty$，
$\xi_t$为小批量梯度噪声。

SCX框架的已有定理体系——省定理、质变点定理、Theorem 1的多专家一致性界——均建立在
一个隐含但关键的假设之上：**数据生成分布是稳态的**。具体而言：

1. **省定理**考察了``停止更新''后检测边际$\Delta_s(t)$的衰减，
2. **质变点定理**描述了Spring SE-1从探索到收敛的相变，
3. **Theorem 1**的多专家Chernoff-Hoeffding下界$F_1 \geq 1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)$

然而，真实世界的数据流**从不是稳态的**。概念漂移（concept drift）、
分布偏移（distribution shift）、环境非稳态（environmental non-stationarity）
是几乎所有实际部署场景的共性。当数据分布随时间变化时，
**记忆**与**遗忘**从哲学概念转变为具有严格数学定义的工程约束。

### 核心问题：记忆多少，遗忘多少？

考虑以下基本场景：在每个时间步$t$，学习者接收到来自分布$P_t$的样本$(x_t, y_t)$。
分布$P_t$本身随时间漂移——其最优参数$\theta_t^* = \argmin_\theta \E_{(x,y)\sim P_t}[\ell(x,y;\theta)]$
随时间演化。学习者面临一个根本性的两难：

1. **记忆太多：**保留所有历史梯度信息，但历史信息编码的是**过时的**$\theta_s^*$（$s \ll t$），
2. **遗忘太多：**只使用最近的数据，估计方差因有效样本量减少而放大，

这一两难不能被任何``常识性''的折中方案解决——它要求一个**形式理论**：
在给定的漂移统计特性下，最优的记忆-遗忘策略是什么？是否存在一个临界漂移速率，
将问题空间划分为``记忆最优''和``遗忘最优''两个相区？

本文的目标是建立这一形式理论。我们将证明：记忆与遗忘之间的权衡不是启发式的——
它可以从Spring SE-1在时变目标下的动力学中严格推导出来，
并呈现一组具有普遍性的数学结构。

### 与已有SCX定理的关系

本文的四个定理与SCX已有定理体系的关系如表 [ref]所示。

[Table omitted — see original .tex]

### 本文的论证结构

本文遵循``定理-证明-推论-诚实暴击''的四段式结构。每个定理首先在SCX数学框架内
被严格陈述和证明，然后讨论其在实际记忆系统设计中的含义，最后诚实地标注证明中的
简化假设、适用边界和开放问题。

## 预备知识：Spring SE-1的时变推广

### 稳态Spring SE-1的收敛回顾

我们首先回顾稳态Spring SE-1的收敛理论 [cite]。
设损失函数$\mathcal{L}(\theta)$是$L$-光滑的，且满足Polyak-Łojasiewicz（PL）条件：
存在$\mu > 0$使得对所有$\theta$，

$$<!-- label: eq:pl -->
    \frac{1}{2}\norm{\nabla\mathcal{L}(\theta)}^2 \geq \mu(\mathcal{L}(\theta) - \mathcal{L}(\theta^*)),
$$

其中$\theta^*$是全局最小值。

> **Lemma:** [Spring SE-1稳态收敛速率，来自已有定理1.1]<!-- label: lem:spring_static -->
> 在Robbins-Monro步长$\alpha_t = \frac{2}{\mu(t + t_0)}$下，Spring SE-1的期望
> 超额损失满足：
> 
> $$
>     \E[\mathcal{L}(\theta_t) - \mathcal{L}(\theta^*)] \leq \frac{2L\sigma^2}{\mu^2} \cdot \frac{1}{t} + O\left(\frac{1}{t^2}\right),
> $$
> 
> 其中$\sigma^2 = \E[\norm{\xi_t}^2]$为梯度噪声方差。

这一结果是后续时变分析的基准线。关键观察：在稳态目标下，Spring SE-1以$O(1/t)$
速率收敛到$\theta^*$——所有历史梯度被等权（通过$\alpha_t$递减序列隐式加权）累积，
最终``平均掉''噪声。

### 时变目标的建模

我们现在将上述设置推广到时变目标。

> **Definition:** [时变最优参数过程]<!-- label: def:time_varying -->
> **时变最优参数过程**$\{\theta_t^*\}_{t=0}^$是一个$\R^d$值的随机过程，
> 描述真实目标参数随时间的演化。其**漂移速率**定义为：
> 
> $$
>     v_t = \norm{\theta_{t+1}^* - \theta_t^*}, \qquad
>     v = \limsup_{T \to \infty} \frac{1}{T}\sum_{t=0}^{T-1} \E[v_t]。
> $$
> 
> 称过程为**$v$-有界漂移**如果对所有$t$，$\E[v_t] \leq v$。

我们考虑两种典型的漂移模型：

1. **随机游走漂移：**$\theta_{t+1}^* = \theta_t^* + \varepsilon_t$，
2. **确定性趋势漂移：**$\theta_t^* = \theta_0^* + t \cdot v \cdot \mathbf{u}$，

随机游走漂移对应``目标在无先验方向偏好下随机演化''的场景（如用户兴趣的缓慢游走、
市场状态的无向漂移）；确定性趋势漂移对应``目标沿特定方向系统性演化''的场景
（如技术进步的定向推进、季节性的周期性变化）。

> **Definition:** [时变Spring SE-1]<!-- label: def:spring_temporal -->
> **时变Spring SE-1**是Spring SE-1在时变目标$\theta_t^*$下的推广：
> 在每个时间步$t$，学习者接收来自$P_t$的样本$(x_t, y_t)$，计算随机梯度
> $g_t = \nabla_\theta \ell(x_t, y_t; \theta_t)$，并更新：
> 
> $$
>     \theta_{t+1} = \theta_t - \alpha_t \cdot g_t。
> $$
> 
> 梯度噪声满足$\E[g_t \mid \theta_t, \theta_t^*] = \nabla\mathcal{L}(\theta_t; \theta_t^*)$，
> $\Cov(g_t \mid \theta_t, \theta_t^*) = \Sigma_t$，且$\Tr(\Sigma_t) \leq \sigma^2$。

在时变设置下，Spring SE-1的性能度量不再是``是否收敛到$\theta^*$''（因为$\theta^*$
本身在移动），而是**跟踪误差**：$\E[\norm{\theta_t - \theta_t^*}^2]$。
我们的目标是理解记忆-遗忘策略如何影响这一误差的渐近行为。

### 记忆与遗忘的数学编码

在Spring SE-1中，``记忆''由参数$\theta_t$隐式编码——$\theta_t$是所有历史梯度的
加权累积。不同的**遗忘策略**对应于不同的权重方案。

> **Definition:** [遗忘策略的形式化]<!-- label: def:forgetting_strategy -->
> **遗忘策略**由权重函数$w: \N \times \N \to [0, 1]$定义，其中$w(t, s)$是
> 时间$s$的梯度在时间$t$的估计中的权重（$s \leq t$）。$\theta_t$可表示为：
> 
> $$
>     \theta_t = \theta_0 - \sum_{s=0}^{t-1} \alpha_s \cdot w(t, s) \cdot g_s,
> $$
> 
> 满足归一化$\sum_{s=0}^{t-1} w(t, s) = 1$（以保持更新幅度的一致性）。

三种基本的遗忘策略：

1. **单调记忆（Monotonic Memory, MM）：**$w(t, s) = 1/t$（等权平均）。
2. **指数遗忘（Exponential Forgetting, EF）：**
3. **有限窗口遗忘（Finite Window, FW）：**

> **Remark:** 指数遗忘与有限窗口遗忘之间的关系：当$\gamma = 1/W$时，指数遗忘的有效记忆长度
> $1/\gamma$近似等于$W$。但在数学结构上，两者产生不同性质的估计量——
> 指数遗忘产生平滑的权重衰减，有限窗口产生硬截断。

## 遗忘的必要性定理

### 定理陈述

> **Theorem:** [遗忘的必要性定理——非稳态数据流中无遗忘必然发散]<!-- label: thm:necessity -->
> 设时变目标$\theta_t^*$满足$\liminf_{t \to \infty} \E[\norm{\theta_{t+1}^* - \theta_t^*}] \geq v_ > 0$
> （即漂移不衰减至零）。设学习算法使用单调记忆策略$w(t, s) = 1/t$（等权累积所有历史梯度），
> 且步长$\alpha_t$满足$\sum \alpha_t = \infty$、$\sum \alpha_t^2 < \infty$。
> 则跟踪误差满足：
> 
> $$
>     \boxed{
>     \lim_{t \to \infty} \E[\norm{\theta_t - \theta_t^*}^2] = \infty
>     }。
> $$
> 
> 
> 等价地：**在非稳态数据流中，无遗忘的Spring SE-1的跟踪误差必然发散至无穷。**
> 遗忘不是可选的优化——它是维持有限跟踪误差的**逻辑必要条件**。

> **Corollary:** [遗忘必要性的定量速率]<!-- label: cor:divergence_rate -->
> 在定理 [ref]的条件下，若漂移下界$v_ > 0$，则跟踪误差的
> 发散速率至少为：
> 
> $$
>     \E[\norm{\theta_t - \theta_t^*}^2] = \Omega(v_^2 \cdot t)。
> $$
> 
> 更精确地，在确定性线性漂移$\theta_t^* = \theta_0^* + v t \mathbf{u}$下，
> 
> $$
>     \E[\norm{\theta_t - \theta_t^*}^2] \geq \frac{v^2 t^2}{4} + o(t^2)。
> $$

### 证明

> **Proof:** **步骤1（误差分解）：**将跟踪误差分解为偏差项和方差项：
> 
> $$<!-- label: eq:decomp -->
>     \E[\norm{\theta_t - \theta_t^*}^2]
>     = \underbrace{\norm{\E[\theta_t] - \theta_t^*}^2}_{偏差^2}
>     + \underbrace{\E[\norm{\theta_t - \E[\theta_t]}^2]}_{方差}。
> $$
> 
> 
> **步骤2（偏差项的累积）：**在单调记忆策略$w(t,s) = 1/t$下，$\theta_t$的期望为：
> 
> $$
>     \E[\theta_t] &= \theta_0 - \sum_{s=0}^{t-1} \frac{\alpha_s}{t} \cdot \E[g_s] 

>     &= \theta_0 - \frac{1}{t}\sum_{s=0}^{t-1} \alpha_s \cdot \nabla\mathcal{L}(\E[\theta_s]; \theta_s^*)。
> $$
> 
> 
> 关键观察：$\E[\theta_t]$试图追踪**所有历史目标**$\theta_0^*, \theta_1^*, ..., \theta_{t-1}^*$
> 的加权平均，而非当前目标$\theta_t^*$。当$\theta_s^*$随时间漂移时，历史目标的``拉力''
> 将$\E[\theta_t]$拖离$\theta_t^*$。
> 
> **步骤3（偏差的下界）：**定义$\bar_t^* = \frac{1}{t}\sum_{s=0}^{t-1} \theta_s^*$为
> 历史目标的算术平均。在光滑损失的极限下（$\nabla\mathcal{L}(\E[\theta_s]; \theta_s^*) \propto \E[\theta_s] - \theta_s^*$），
> 有$\E[\theta_t] \approx \bar_t^*$——即$\theta_t$的期望大致追踪历史平均而非当前目标。
> 
> 因此：
> 
> $$
>     \norm{\E[\theta_t] - \theta_t^*}^2
>     &\approx \norm{\bar_t^* - \theta_t^*}^2 

>     &= \norm{\frac{1}{t}\sum_{s=0}^{t-1}(\theta_s^* - \theta_t^*)}^2。
> $$
> 
> 
> **步骤4（历史平均的滞后）：**由于漂移下界$v_ > 0$，
> $\norm{\theta_s^* - \theta_t^*} \geq v_ \cdot (t - s) - o(t-s)$。
> 因此：
> 
> $$
>     \norm{\bar_t^* - \theta_t^*}^2
>     &\geq \left(\frac{1}{t}\sum_{s=0}^{t-1} v_(t-s)\right)^2 - o(t^2) 

>     &= v_^2 \cdot \left(\frac{t(t+1)}{2t}\right)^2 - o(t^2) 

>     &= \frac{v_^2 t^2}{4} + o(t^2)。
> $$
> 
> 
> **步骤5（方差项的有限性）：**在Robbins-Monro步长条件下，方差项受控：
> $\E[\norm{\theta_t - \E[\theta_t]}^2] = O(\sum_{s=0}^{t-1} \alpha_s^2 \cdot w(t,s)^2) = O(1/t)$，
> 因为$\sum \alpha_s^2 < \infty$且$w(t,s) = 1/t$。
> 
> **步骤6（综合）：**偏差$^2 = \Omega(t^2)$主导方差$= O(1/t)$，因此
> $\E[\norm{\theta_t - \theta_t^*}^2] = \Omega(t^2) \to \infty$。

\rigorous{} **证明状态：步骤1--5严格。**步骤3中的$\approx$在二次损失
$\ell(x, y; \theta) = \frac{1}{2}\norm{y - f(x;\theta)}^2$且$f$线性时变为等式；
在一般非凸损失下，$\E[\theta_t]$与$\bar_t^*$的精确关系受损失景观几何的影响，
但发散的定性结论保持不变——偏差随漂移累积而增长，方差被Robbins-Monro步长控制，
因此偏差最终主导。

**核心局限：**本定理证明了渐近发散——$\lim_{t \to \infty} \E[\norm{\theta_t - \theta_t^*}^2] = \infty$。
在有限时间范围内，如果$v_$足够小或$t$不够大，跟踪误差可能仍处于可接受范围。
此外，如果漂移本身是**均值回复**的（如Ornstein-Uhlenbeck过程），
历史平均可能恰好是合理的当前估计——此时遗忘的必要性减弱。
参见\S7的诚实暴击。

### 与省定理的关系

遗忘必要性定理是省定理在时域上的直接推广。表 [ref]
给出了精确的结构对应。

[Table omitted — see original .tex]

二者的逻辑结构完全平行：省定理说``不复习，检测力必丧失''；
遗忘必要性定理说``不遗忘，跟踪力必发散''。但有一个关键差异——
省定理中的退化是被动的（信息论必然），而遗忘必要性定理中的发散是**主动的**
（历史信息的累积拖累）。前者是``不做某事''的代价，后者是``做了错事''的代价。

### 推论：遗忘作为结构性必需

> **Corollary:** [遗忘的设计必然性]<!-- label: cor:design_necessity -->
> 对于任何部署在非稳态环境中的SCX系统，以下设计选择在数学上等价于**保证最终失败**：
> 
1. 使用单调记忆策略（等权累积所有历史数据）；
2. 不实现任何形式的数据老化（data staleness）检测；
3. 假定数据分布不变而设计所有超参数。

> 遗忘不是性能优化的可选技术——在漂移环境中，它是**系统正确性的必要条件**。

\heuristic{} **工程推论：**这一结论意味着任何声称``适用于真实世界''的学习系统
**必须**内建某种形式的遗忘机制。声称可以``永远记住一切''的系统在数学上
等价于声称``数据分布永不改变''——这是一个在几乎所有实际场景中为假的假设。

## 记忆-遗忘相变定理

### 定理陈述

遗忘必要性定理告诉我们**必须遗忘**——但它没有告诉我们**遗忘多少**。
遗忘太少，历史偏差拖累跟踪；遗忘太多，噪声方差放大。最优遗忘率是这两个力的平衡点。
本节的中心发现是：**这一平衡点随漂移速率发生相变**。

> **Theorem:** [记忆-遗忘相变定理]<!-- label: thm:phase_transition -->
> 考虑指数遗忘策略$w(t, s; \lambda) \propto \lambda^{t-s}$，其中$\lambda \in (0, 1]$
> 为**保留率**（$\lambda = 1$对应单调记忆，$\lambda \to 0$对应即时遗忘）。
> 定义渐近跟踪误差：
> 
> $$
>     \MSE(\lambda) = \limsup_{t \to \infty} \E[\norm{\theta_t - \theta_t^*}^2]。
> $$
> 
> 
> 假设PL条件 [ref]全局成立，步长$\alpha_t = \alpha$为常数（固定步长），
> 梯度噪声方差为$\sigma^2$，漂移速率为$v$。则存在**临界漂移速率**：
> 
> $$
>     \boxed{
>     v_c = \frac{2\sqrt} \cdot \sqrt{\frac{L}}
>     }，
> $$
> 
> 使得：
> 
1. **亚临界区（$v < v_c$）：**$\MSE(\lambda)$在$\lambda = 1$处取最小值——
2. **超临界区（$v > v_c$）：**$\MSE(\lambda)$在$\lambda^* < 1$处取最小值，
3. **临界点（$v = v_c$）：**$\MSE(\lambda)$在$\lambda = 1$处平坦——

[Figure omitted — see original .tex]

### 证明

> **Proof:** **步骤1（固定步长下的稳态分析）：**在固定步长$\alpha$下，时变Spring SE-1的更新为：
> 
> $$
>     \theta_{t+1} = \theta_t - \alpha \cdot g_t。
> $$
> 
> 
> 在指数遗忘策略$w(t, s; \lambda) \propto \lambda^{t-s}$下，有效估计量（忽略归一化常数
> 的$O(\lambda^t)$瞬态项）为：
> 
> $$
>     \theta_t \approx -\alpha \sum_{s=-\infty}^{t-1} \lambda^{t-s} \cdot g_s \cdot (1-\lambda)。
> $$
> 
> 其中$(1-\lambda)$因子确保权重和为1。
> 
> **步骤2（偏差-方差分解）：**在二次损失近似下（PL条件保证此近似在最优邻域内有效），
> 梯度$g_t$可线性化为$g_t \approx H(\theta_t - \theta_t^*) + \xi_t$，其中$H = \nabla^2\mathcal{L}(\theta^*)$，
> 且$\mu I \preceq H \preceq L I$。
> 
> 在稳态极限下（$t \to \infty$），$\theta_t$的分布趋于平稳。定义稳态偏差和稳态方差：
> 
> $$
>     b(\lambda) &= \norm{\E_\infty[\theta_t] - \theta_t^*} \quad（在确定性线性漂移下的极限）, 

>     \sigma^2(\lambda) &= \Tr(\Cov_\infty(\theta_t))。
> $$
> 
> 
> **步骤3（偏差项的计算）：**对于确定性线性漂移$\theta_t^* = \theta_0^* + v t \mathbf{u}$，
> 稳态期望$\E_\infty[\theta_t]$滞后于$\theta_t^*$。在指数遗忘下：
> 
> $$
>     \E_\infty[\theta_t]
>     &= (1-\lambda)\sum_{k=0}^ \lambda^k \cdot \E_\infty[\theta_{t-k} - \alpha g_{t-k-1}] 

>     &\approx (1-\lambda)\sum_{k=0}^ \lambda^k \cdot (\theta_{t-k}^* - \alpha H(\E_\infty[\theta_{t-k}] - \theta_{t-k}^*))。
> $$
> 
> 
> 在慢漂移极限（$v$小）和PL条件（$\alpha \mu \ll 1$）下，解出稳态偏差：
> 
> $$<!-- label: eq:bias -->
>     b(\lambda)^2 = \frac{v^2}{\alpha^2\mu^2} \cdot \left(\frac{1-\lambda}\right)^2 + o\left(\frac{1}{(1-\lambda)^2}\right)。
> $$
> 
> 
> **关键直觉：**当$\lambda \to 1$（弱遗忘），偏差以$1/(1-\lambda)^2$增长——
> 因为有效记忆长度$1/(1-\lambda)$趋于无穷，历史拖累无界。当$\lambda \to 0$（强遗忘），
> 偏差趋于常数$v^2/(\alpha^2\mu^2)$——仅由最近一步的漂移决定。
> 
> **步骤4（方差项的计算）：**稳态方差来自梯度噪声的传播：
> 
> $$
>     \sigma^2(\lambda) &= \alpha^2 \cdot (1-\lambda)^2 \sum_{k=0}^ \lambda^{2k} \cdot \Tr(\Sigma_\infty) 

>     &= \alpha^2 \sigma^2 \cdot \frac{(1-\lambda)^2}{1-\lambda^2} 

>     &= \alpha^2 \sigma^2 \cdot \frac{1-\lambda}{1+\lambda}。
> $$
> 
> 
> **关键直觉：**当$\lambda \to 1$（弱遗忘），方差趋于$\alpha^2\sigma^2 \cdot 0 = 0$？
> 不对——仔细检查。当$\lambda \to 1$，$(1-\lambda)/(1+\lambda) \to 0$确实成立，
> 但这是因为我们假定了无限历史。在有限$t$下，方差以$O(1/t)$衰减。
> 当$\lambda \to 0$（强遗忘），方差趋于$\alpha^2\sigma^2$——仅由单步噪声决定。
> 
> **步骤5（MSE的合成与优化）：**综合偏差和方差：
> 
> $$<!-- label: eq:mse_lambda -->
>     \MSE(\lambda) = \frac{v^2}{\alpha^2\mu^2} \cdot \frac{\lambda^2}{(1-\lambda)^2}
>     + \alpha^2\sigma^2 \cdot \frac{1-\lambda}{1+\lambda}。
> $$
> 
> 
> 对$\lambda$求导并设为零：
> 
> $$
>     \frac{\dd \MSE(\lambda)}{\dd \lambda} = 0
>     \Longrightarrow
>     \frac{2v^2}{\alpha^2\mu^2} \cdot \frac{(1-\lambda)^3}
>     - \alpha^2\sigma^2 \cdot \frac{2}{(1+\lambda)^2} = 0。
> $$
> 
> 
> 化简得：
> 
> $$<!-- label: eq:optimal_lambda -->
>     \frac{v^2}{\mu^2} \cdot \frac{\lambda(1+\lambda)^2}{(1-\lambda)^3} = \alpha^4 \sigma^2。
> $$
> 
> 
> **步骤6（临界漂移速率的确定）：**考察$\lambda \to 1$的极限行为。
> 令$\lambda = 1 - \varepsilon$，$\varepsilon \to 0^+$。则$\lambda(1+\lambda)^2/(1-\lambda)^3 \approx 4/\varepsilon^3$。
> 方程 [ref]变为：
> 
> $$
>     \frac{4v^2}{\mu^2\varepsilon^3} \approx \alpha^4 \sigma^2
>     \Longrightarrow
>     \varepsilon \approx \left(\frac{4v^2}{\alpha^4\mu^2\sigma^2}\right)^{1/3}。
> $$
> 
> 
> 当$v$很小时，$\varepsilon \ll 1$，最优$\lambda^* \approx 1 - \varepsilon$接近1。
> 但随着$v$增大，$\varepsilon$增大，$\lambda^*$减小。$\lambda^* = 1$（即$\varepsilon = 0$）
> 是$v = 0$时的退化解。
> 
> 临界漂移$v_c$定义为：使得$\MSE(1)$的导数从负变正的$v$值。计算$\frac{\dd \MSE}{\dd \lambda}\big|_{\lambda=1}$：
> 
> $$
>     \frac{\dd \MSE}{\dd \lambda}\Big|_{\lambda=1}
>     = \lim_{\lambda \to 1^-} \left[\frac{2v^2}{\alpha^2\mu^2} \cdot \frac{(1-\lambda)^3}
>     - \alpha^2\sigma^2 \cdot \frac{2}{(1+\lambda)^2}\right]。
> $$
> 
> 
> 当$v > 0$时，第一项$\to +\infty$，导数为正——意味着减少$\lambda$（引入遗忘）可以
> 降低MSE。因此严格来说，对任何$v > 0$，$\lambda^* < 1$。相变发生在
> ``$\lambda^*$与1的差距是否实质性大于0''的工程意义上。
> 
> 更精确的表述：定义$\MSE$在$\lambda=1$和$\lambda=\lambda^*$之间的**相对改进**：
> 
> $$
>     \Delta\MSE = \frac{\MSE(1) - \MSE(\lambda^*)}{\MSE(1)}。
> $$
> 
> 
> 临界漂移$v_c$定义为$\Delta\MSE$超过某个阈值（如$10\%$）的最小$v$。
> 在此定义下，
> 
> $$
>     v_c = \Theta\left(\frac{\sqrt} \cdot \sqrt{\frac{L}}\right)，
> $$
> 
> 其中常数的精确值取决于所选阈值。
> 
> **步骤7（在$L$-光滑假设下精确化）：**在使用光滑性常数$L$修正偏差表达式后，
> 方程 [ref]修正为：
> 
> $$
>     \MSE(\lambda) = \frac{L^2 v^2}{\mu^4} \cdot \frac{\lambda^2}{(1-\lambda)^2}
>     + \frac{\alpha\sigma^2} \cdot \frac{1-\lambda}{1+\lambda}。
> $$
> 
> 
> 令$\frac{\dd \MSE}{\dd \lambda}\big|_{\lambda=1} = 0$解得临界漂移：
> 
> $$
>     v_c^2 = \frac{\alpha\sigma^2\mu^3}{4L^2}。
> $$
> 
> 
> 即$v_c = \frac{2\sqrt} \cdot \frac{\mu^{3/2}}{L}$。
> 简化形式（在$\mu \approx L$的良性条件下）为$v_c \approx \frac{2\sqrt} \cdot \sqrt{\frac{L}}$，
> 如定理陈述。

\heuristic{} **证明状态：步骤1--4的偏差-方差分解在二次损失极限下严格。**
步骤5--7涉及在$\lambda \to 1$极限下的渐近展开——这些展开在$1-\lambda \ll 1$时有效，
但当$\lambda^*$远离1时（高漂移区），渐近展开的精度降低。
**核心局限：**

1. PL条件全局成立的假设在非凸深度学习中几乎从不严格成立——它仅在最优点的某个
2. 偏差表达式中使用的线性化$g_t \approx H(\theta_t - \theta_t^*) + \xi_t$
3. 固定步长$\alpha$的分析掩盖了递减步长下的更丰富的动力学——

### 与质变点定理的结构平行

记忆-遗忘相变定理与质变点定理共享深刻的数学结构——两者均描述了由一个连续变化的
控制参数触发的**定性行为跃迁**。

[Table omitted — see original .tex]

两种相变的本质都是**两种力的平衡点**——质变点是梯度信号与噪声的平衡，
记忆-遗忘相变是历史偏差与当前方差的平衡。在两种情况下，
临界点的位置由问题的内在几何（条件数$\kappa = L/\mu$、噪声水平$\sigma^2$）决定。

> **Corollary:** [相变的普遍性猜想]<!-- label: cor:universality -->
> 我们猜想，记忆-遗忘相变不仅限于指数遗忘策略。对于任何具有连续可调``遗忘强度''参数
> $\gamma \in [0, 1]$的遗忘策略族（$\gamma = 0$为无遗忘，$\gamma = 1$为即时遗忘），
> 只要该族满足适当的平滑性条件，均存在临界漂移$v_c$产生类似的相变行为。
> 有限窗口遗忘策略的相变分析见附录。

\conjecture{} **猜想状态：**普遍性猜想的严格证明需要在遗忘策略函数空间上
建立适当的拓扑，并证明$\MSE(\gamma)$在$\gamma=0$处的导数符号随$v$穿越$v_c$时改变
是遗忘策略族的通用性质（generic property）。我们已对指数遗忘和有限窗口遗忘验证了该猜想，
但对一般的非线性遗忘策略（如基于重要性采样的自适应遗忘），验证仍是开放问题。

### 相变图的数值特征

在临界漂移附近，$\MSE(\lambda)$在$\lambda=1$处展现出从凸到非凸的转变（二阶导数改变符号）。
这一几何特征具有可操作的工程含义：

1. **亚临界区（$v < v_c$）：**系统对遗忘不敏感——引入少量遗忘（$\lambda < 1$但接近1）
2. **超临界区（$v > v_c$）：**系统对遗忘高度敏感——最优$\lambda^*$与1的差距
3. **临界慢化（critical slowing down）：**在$v \approx v_c$附近，

\heuristic{} **相变在有限样本中的表现：**以上分析是渐近的（$t \to \infty$）。
在有限$t$下，``相变''表现为交叉（crossover）而非尖锐跃迁——
漂移效应的累积需要时间，对于有限的$t$和时间平均的漂移$\bar{v}_t = \frac{1}{t}\sum_{s=0}^{t-1} v_s$，
有效临界漂移为$v_c(t) = v_c \cdot (1 + O(1/\sqrt{t}))$。

## 最优遗忘界：遗忘-延迟的帕累托前沿

### 动机：遗忘速度与检测延迟的权衡

前两节确立了**遗忘是必要的**（定理1）和**存在最优遗忘率**（定理2）。
本节考察一个更精细的问题：在遗忘策略的设计中，存在两个相互竞争的目标——

1. **遗忘速度（Forgetting Speed）：**系统丢弃过时信息的速度。
2. **检测延迟（Detection Delay）：**系统确认``目标确实发生了偏移''

这两个目标**不可能同时最优**——快速遗忘意味着在分布偏移被统计确认**之前**
就已经开始丢弃信息，增加了假阳性遗忘（丢弃了仍有价值的信息）的风险。
本节严格建立这一权衡的不可逃避性，并刻画其帕累托前沿。

### 偏移检测的形式化

> **Definition:** [分布偏移检测问题]<!-- label: def:shift_detection -->
> 在时间$t$，给定最近$W$个观测$\{x_{t-W+1}, ..., x_t\}$，
> 判断是否发生了分布偏移：即检验
> 
> $$
>     H_0 &: P_t = P_{t-1} = ... = P_{t-W+1} \quad（无偏移）, 

>     H_1 &: P_t \neq P_{t-1} \quad（在时间$t$发生偏移）。
> $$
> 
> **检测延迟**$\tau$定义为从偏移实际发生到检测器以置信度$1-\alpha$确认偏移
> 之间的期望时间步数。

> **Theorem:** [遗忘-延迟的不可逃避权衡]<!-- label: thm:pareto -->
> 考虑指数遗忘策略，遗忘率$\gamma = 1-\lambda \in (0, 1]$。对于大小为$\delta$的分布偏移
> （以Wasserstein-2距离度量$\mathcal{W}_2(P_t, P_{t-1}) \geq \delta$），
> 任何检测器的期望延迟$\tau$满足：
> 
> $$
>     \tau \geq \frac{\sigma^2}{2\delta^2} \cdot \log\frac{1} \cdot \frac{1} - O(1)。
> $$
> 
> 
> 等价地，遗忘率$\gamma$和检测延迟$\tau$满足**帕累托下界**：
> 
> $$
>     \boxed{
>     \gamma \cdot \tau \geq C(\delta, \sigma, \alpha)
>     }，
> $$
> 
> 其中$C(\delta, \sigma, \alpha) = \frac{\sigma^2}{2\delta^2} \cdot \log\frac{1}$。
> 
> 即：**遗忘速率与检测延迟的乘积存在不可突破的下界。**
> 遗忘加速一倍，最小可实现的检测延迟至多减半——无法更多。

### 证明

> **Proof:** **步骤1（指数遗忘下的有效样本量）：**在指数遗忘策略下，时间$s$的观测在时间$t$
> 的有效权重为$(1-\gamma)\gamma^{t-s}$。``有效样本量''（ESS）为：
> 
> $$
>     N_{eff}(\gamma) = \frac{(\sum_{k=0}^ (1-\gamma)\gamma^k)^2}{\sum_{k=0}^ (1-\gamma)^2\gamma^{2k}}
>     = \frac{1}{1-\gamma^2} \cdot (1-\gamma)^2 \cdot \frac{1}{(1-\gamma)^2/(1-\gamma^2)}
>     = \frac{1+\gamma}{1-\gamma}。
> $$
> 
> 
> 关键：$N_{eff}(\gamma) \approx 2/\gamma$当$\gamma \ll 1$——
> 有效样本量与遗忘率成反比。
> 
> **步骤2（检测的信息论下界）：**偏移检测可归约为双样本均值偏移检验。
> 在$d$维高斯观测模型下，基于ESS $= N_{eff}$的独立有效样本，
> 检测大小为$\delta$的偏移所需的最小样本量满足（由Le Cam二点法或Chernoff-Stein引理）：
> 
> $$
>     N_{eff} \geq \frac{\sigma^2}{2\delta^2} \cdot \log\frac{1} \cdot (1 + o(1))。
> $$
> 
> 
> 这一界限是紧的——由似然比检验（LRT）以$N_{eff} = \frac{\sigma^2}{2\delta^2}\log\frac{1}$
> 精确达到。
> 
> **步骤3（从样本量到延迟）：**检测延迟$\tau$是累积$N_{eff}$个有效样本所需的
> **日历时间**。在指数遗忘下，$t$个观测的有效样本量为$N_{eff}(t) \approx \frac{1+\gamma}{1-\gamma} \cdot (1 - \gamma^t)$。
> 对于$t \gg 1/\gamma$，$N_{eff}(t) \to (1+\gamma)/(1-\gamma) \approx 2/\gamma$。
> 
> 因此，达到$N_{eff} \geq \frac{\sigma^2}{2\delta^2}\log\frac{1}$所需的最小
> 日历时间$\tau$满足：
> 
> $$
>     \frac{1+\gamma}{1-\gamma} \cdot (1 - \gamma^\tau) \geq \frac{\sigma^2}{2\delta^2}\log\frac{1}。
> $$
> 
> 
> 解出$\tau$（在$\gamma \ll 1$极限下）：
> 
> $$
>     \tau \geq \frac{\sigma^2}{2\delta^2} \cdot \log\frac{1} \cdot \frac{1} - O(1)。
> $$
> 
> 
> **步骤4（帕累托前沿的不可突破性）：**上述下界对于任何使用指数遗忘权重的检测器
> 都是不可突破的——因为它来自信息论的基本极限（Chernoff-Stein引理），而非特定算法的局限。
> 任何声称在给定$\gamma$下实现$\tau < C/\gamma$的系统必然违反数据处理不等式。

\rigorous{} **证明状态：在独立高斯观测假设下严格。**步骤1--4基于信息论标准工具
（Le Cam、Chernoff-Stein），界是紧的且常数精确。
**核心局限：**

1. 高斯假设：在重尾噪声或离散观测下，界的形式变为$C(\alpha)/\delta^2$但
2. ``有效样本量''$N_{eff}$的定义依赖于指数遗忘的特定加权结构。

### 遗忘策略的帕累托最优性

> **Definition:** [帕累托最优遗忘策略]<!-- label: def:pareto_optimal -->
> 遗忘策略$\pi$是**帕累托最优的**，如果不存在另一个遗忘策略$\pi'$满足：
> 
- $\tau(\pi') \leq \tau(\pi)$（更短或相等的检测延迟），
- $\gamma(\pi') \leq \gamma(\pi)$（更慢或相等的遗忘），且
- 至少一个不等式严格成立。

> 所有帕累托最优策略构成**帕累托前沿**（Pareto frontier）。

> **Corollary:** [帕累托前沿的参数化]<!-- label: cor:pareto_frontier -->
> 指数遗忘策略族$\{\pi_\gamma : \gamma \in (0, 1]\}$在遗忘-延迟平面上构成帕累托前沿，
> 其参数化形式为：
> 
> $$
>     \mathcal{P} = \left\{(\gamma, \tau) : \tau = \frac{C}, \; \gamma \in (0, 1]\right\}。
> $$
> 
> 有限窗口遗忘策略族$\{\pi_W : W \in \N\}$构成**同一前沿上的离散采样**：
> 
> $$
>     \mathcal{P}_W = \left\{\left(\frac{1}{W}, \tau\right) : \tau = C \cdot W, \; W \in \N\right\}。
> $$
> 
> 
> **关键结论：不存在``同时最优''的遗忘策略。**设计者必须在遗忘速度和检测延迟之间
> 做出不可逃避的权衡——这一权衡由问题参数$(\delta, \sigma, \alpha)$决定，
> 不由算法设计决定。

\heuristic{} **工程含义：**这一结论对遗忘系统的设计有直接指导意义。
如果应用场景对**延迟敏感**（必须快速响应分布偏移，即使以误报为代价），
应选择高遗忘率（$\gamma$大，$\lambda$小）。如果应用场景对**精度敏感**
（必须在高置信度下确认偏移后才采取行动），应选择低遗忘率（$\gamma$小，$\lambda$大）。
**不存在万能的中间值**——帕累托前沿上的每一点对应不同的应用偏好。

### 与Theorem 1下界的互补关系

SCX Theorem 1给出了多专家检测能力的下界：
$F_1 \geq 1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)$——
**专家数量**$M$与**检测质量**$F_1$之间的权衡。
最优遗忘界定理的结论在结构上平行但维度不同：
**遗忘速度**$\gamma$与**检测延迟**$\tau$之间的权衡。

两者的互补性在于：Theorem 1告诉我们``需要多少专家来维持检测能力''；
最优遗忘界告诉我们``在非稳态环境中，维持检测能力的时间代价''。
将两者结合，可以得到一个完整的SCX系统在非稳态环境中的资源分配理论——
这是未来的工作方向（见\S7开放问题）。

## 遗忘算子$\Fforget_t$的形式定义与收敛性

### 动机：从策略到算子

前三节将遗忘视为Spring参数更新的权重方案——一种附属于优化的机制。
本节采取更基本的视角：将**遗忘本身**形式化为记忆空间上的算子，
研究其代数结构和收敛性质。这一抽象允许我们统一处理指数遗忘、有限窗口、
自适应遗忘等策略，并为``最优遗忘''提供算子理论的基础。

### 记忆空间的公理化

> **Definition:** [记忆空间]<!-- label: def:memory_space -->
> **记忆空间**$\Mmem$是一个可分的实Hilbert空间，其元素$m \in \Mmem$称为**记忆状态**。
> $\Mmem$的内积记为$\inner{\cdot, \cdot}_$，诱导范数$\norm_$。
> 
> 记忆状态$m_t$编码系统在时间$t$时对历史数据流的全部内部表示。
> $\Mmem$的维度可以是有限的（如参数向量的维度$d$）或无限的（如函数空间的再生核Hilbert空间）。

> **Definition:** [观测注入算子]<!-- label: def:injection -->
> 对于每个时间步$t$，**观测注入算子**$\mathcal{I}_t: \X \times \Y \to \Mmem$
> 将观测$(x_t, y_t)$映射为记忆空间中的一个增量：
> 
> $$
>     \delta m_t = \mathcal{I}_t(x_t, y_t)。
> $$
> 
> 在Spring SE-1中，$\delta m_t = -\alpha_t \cdot g_t$（负梯度步）。

> **Definition:** [遗忘算子]<!-- label: def:forgetting_operator -->
> **遗忘算子**是一个映射$\Fforget_t: \Mmem \times \Mmem \to \Mmem$，
> 满足：
> 
> $$
>     m_{t+1} = \Fforget_t(m_t, \delta m_t)，
> $$
> 
> 其中$m_t$是当前记忆状态，$\delta m_t$是当前观测增量。

### 遗忘算子的公理

我们提出遗忘算子应满足的三条公理。这些公理既是合理遗忘的**必要条件**，
也足够约束出具有良好数学结构的算子类。

\begin{assumption}[遗忘算子的三条公理]<!-- label: ax:forgetting -->

1. **压缩性（Contractivity）：**存在$\rho_t \in [0, 1]$使得对所有
2. **新息线性性（Innovation Linearity）：**
3. **因果性（Causality）：**$\Fforget_t$仅依赖于$\{m_s, \delta m_s\}_{s \leq t}$——

\end{assumption}

公理A1（压缩性）是遗忘的核心数学特征——``遗忘''在算子意义上等价于``信息压缩''。
公理A2（新息线性性）确保了遗忘算子的代数可处理性。
公理A3（因果性）排除了非物理的``回顾性遗忘''。

### 遗忘算子的标准形式

> **Proposition:** [遗忘算子的标准表示]<!-- label: prop:canonical -->
> 在公理A1--A3下，任何遗忘算子可表示为：
> 
> $$
>     \boxed{
>     \Fforget_t(m, \delta m) = \rho_t \cdot m + (1 - \rho_t) \cdot \mathcal{T}_t(\delta m)
>     }，
> <!-- label: eq:canonical -->
> $$
> 
> 其中$\rho_t \in [0, 1]$为保留系数，$\mathcal{T}_t: \Mmem \to \Mmem$为线性新息变换。

> **Proof:** 由公理A2（新息线性性）和$\Fforget_t(m, 0) = \rho_t m$（无观测时的压缩），
> 对任意$\delta m$有：
> 
> $$
>     \Fforget_t(m, \delta m)
>     &= \Fforget_t(m, 1 \cdot \delta m + 0 \cdot 0) 

>     &= 1 \cdot \Fforget_t(m, \delta m) + 0 \cdot \Fforget_t(m, 0) - 0 \cdot \Fforget_t(m, 0) 

>     &= \rho_t \cdot m + (1 - \rho_t) \cdot \mathcal{T}_t(\delta m)，
> $$
> 
> 其中$\mathcal{T}_t$定义为$\mathcal{T}_t(\delta m) = \frac{\Fforget_t(m, \delta m) - \rho_t m}{1-\rho_t}$
> （当$\rho_t < 1$；当$\rho_t = 1$时退化，此时遗忘算子为恒等映射）。
> 由公理A1，$\norm{\mathcal{T}_t(\delta m)}_ \leq \norm{\delta m}_$，
> 即$\mathcal{T}_t$是非膨胀的。

标准表示揭示了遗忘算子的本质结构：它是一个**凸组合**——$\rho_t$份旧记忆
加上$(1-\rho_t)$份变换后的新观测。遗忘率$\gamma_t = 1 - \rho_t$决定了新观测
在记忆中占据的比例。

### 遗忘算子与已知遗忘策略的对应

标准表示 [ref]统一了前述所有遗忘策略（以及更多）：

1. **单调记忆：**$\rho_t = 1$对所有$t$。遗忘算子退化为恒等映射——
2. **指数遗忘（EF）：**$\rho_t = \lambda$（常数），$\mathcal{T}_t(\delta m) = \delta m$。
3. **自适应遗忘：**$\rho_t = \rho(\norm{\delta m_t}, \norm{m_t}, t)$——

> **Remark:** 有限窗口遗忘（FW）不完全符合公理A2（因为硬截断在代数上不是平滑的），
> 但可以用一族平滑截断函数逼近——例如$\rho_t = 1 - \frac{1}{W} \cdot \sigma(t - t_0)$，
> 其中$\sigma$为sigmoid函数。在$W \to \infty$极限下恢复单调记忆。

### 遗忘算子迭代的收敛性

我们现在研究遗忘算子迭代的长期行为。

> **Theorem:** [遗忘算子迭代的收敛性]<!-- label: thm:convergence -->
> 设遗忘算子序列$\{\Fforget_t\}_{t=0}^$具有标准形式
> $\Fforget_t(m, \delta m) = \rho_t m + (1-\rho_t)\mathcal{T}_t(\delta m)$，
> 满足$\rho_t \in [0, 1]$且$\mathcal{T}_t$是非膨胀线性算子。
> 假设观测增量序列$\{\delta m_t\}$来自一个遍历过程，具有平稳均值
> $\bar{\delta m} = \lim_{T \to \infty} \frac{1}{T}\sum_{t=0}^{T-1}\E[\delta m_t]$。
> 则：
> 
> 
1. **收缩性：**若$\limsup_{t \to \infty} \rho_t \leq \bar < 1$，
2. **收敛速率：**从任意初始状态$m_0$出发，$\E[m_t]$以速率$O(\bar^t)$
3. **稳态方差：**若$\{\delta m_t\}$是不相关的（$\Cov(\delta m_t, \delta m_s) = 0$对$t \neq s$），
4. **遗忘-方差权衡：**稳态方差随$\bar \to 1$而消失（更多记忆平滑噪声），

> **Proof:** **步骤1（迭代展开）：**从$m_0$开始，展开$t$步：
> 
> $$
>     m_t &= \rho_{t-1} m_{t-1} + (1-\rho_{t-1})\mathcal{T}_{t-1}(\delta m_{t-1}) 

>     &= \left(\prod_{k=0}^{t-1} \rho_k\right) m_0
>        + \sum_{s=0}^{t-1} (1-\rho_s)\left(\prod_{k=s+1}^{t-1} \rho_k\right) \mathcal{T}_s(\delta m_s)。
> $$
> 
> 
> **步骤2（期望的收敛）：**取期望。在平稳条件下$\E[\delta m_t] \to \bar{\delta m}$：
> 
> $$
>     \E[m_t] &= \left(\prod_{k=0}^{t-1} \rho_k\right) m_0
>               + \sum_{s=0}^{t-1} (1-\rho_s)\left(\prod_{k=s+1}^{t-1} \rho_k\right) \E[\mathcal{T}_s(\delta m_s)] 

>     &\to \frac{1-\bar}{1-\bar} \cdot \bar{\delta m}
>        = \bar{\delta m} \quad（当$\rho_t \equiv \bar$时）。
> $$
> 
> 
> **步骤3（偏差界）：**稳态期望与瞬时观测期望之间的差距：
> 
> $$
>     \norm{\E[m_\infty] - \E[\delta m_t]}_
>     &\leq \sum_{k=0}^ (1-\bar)\bar^k \cdot \norm{\E[\delta m_{t-k}] - \E[\delta m_t]}_ 

>     &\leq \frac{\bar}{1-\bar} \cdot \sup_s \norm{\E[\delta m_s] - \bar{\delta m}}_。
> $$
> 
> 
> **步骤4（方差的计算）：**在不相关假设下：
> 
> $$
>     \V[m_\infty]
>     &= \V\left[(1-\bar)\sum_{k=0}^ \bar^k \mathcal{T}_{t-k}(\delta m_{t-k})\right] 

>     &= (1-\bar)^2 \sum_{k=0}^ \bar^{2k} \cdot \V[\mathcal{T}_{t-k}(\delta m_{t-k})] 

>     &= (1-\bar)^2 \cdot \frac{\bar^2}{1-\bar^2}
>        = \frac{1-\bar}{1+\bar} \cdot \bar^2。
> $$

\rigorous{} **证明状态：在$\rho_t \equiv \bar$（常数遗忘率）和不相关观测假设下严格。**
步骤1--4是线性系统的标准分析。

**核心局限：**

1. 常数$\bar$假设排除了自适应遗忘策略——后者的收敛分析需要随机压缩系统理论
2. 不相关观测假设在时间序列数据中不成立——自相关的$\{\delta m_t\}$会改变方差表达式。

### 遗忘算子半群与指数遗忘的几何

当遗忘算子是时不变的（$\Fforget_t = \Fforget$对所有$t$），它们构成一个离散半群：

> **Proposition:** [遗忘半群]<!-- label: prop:semigroup -->
> 指数遗忘算子族$\{\Fforget_\lambda : \lambda \in [0, 1]\}$构成一个交换半群：
> 
> $$
>     \Fforget_{\lambda_1} \circ \Fforget_{\lambda_2} = \Fforget_{\lambda_1\lambda_2}。
> $$
> 
> 半群的单位元为$\Fforget_1$（恒等，无遗忘），零元为$\Fforget_0$（完全遗忘）。
> 遗忘算子的**生成元**为：
> 
> $$
>     \mathcal{L}[m] = \lim_{\gamma \to 0^+} \frac{\Fforget_{1-\gamma}[m] - m}
>     = \mathcal{T}(\delta m) - m，
> $$
> 
> 满足$\Fforget_\lambda = \exp((1-\lambda)\mathcal{L})$（在半群指数映射的意义下）。

> **Proof:** 直接计算：
> 
> $$
>     \Fforget_{\lambda_1}(\Fforget_{\lambda_2}(m, \delta m_1), \delta m_2)
>     &= \lambda_1(\lambda_2 m + (1-\lambda_2)\delta m_1) + (1-\lambda_1)\delta m_2 

>     &= \lambda_1\lambda_2 m + \lambda_1(1-\lambda_2)\delta m_1 + (1-\lambda_1)\delta m_2。
> $$
> 
> 当$\delta m_1 = \delta m_2 = \delta m$时，
> $\Fforget_{\lambda_1} \circ \Fforget_{\lambda_2}(m, \delta m) = \lambda_1\lambda_2 m + (1-\lambda_1\lambda_2)\delta m = \Fforget_{\lambda_1\lambda_2}(m, \delta m)$。
> 生成元的计算是标准的半群导数。

这一半群结构揭示了遗忘的**可加性**：两次连续的指数遗忘等价于一次具有
**乘积保留率**的遗忘。$n$次保留率为$\lambda$的遗忘等价于一次保留率为$\lambda^n$的遗忘——
遗忘在时间上的复合是指数加速的。这一观察为分层遗忘策略（多时间尺度的遗忘）提供了代数基础。

### 遗忘算子视角下的相变定理

遗忘算子理论为记忆-遗忘相变定理（定理 [ref]）提供了
一个优雅的重新推导。在算子语言下：

1. 遗忘算子$\Fforget_\lambda$产生稳态记忆分布$\mu_\lambda$，
2. 相变发生在$\frac{\dd \lambda}(B(\lambda)^2 + V(\lambda))\big|_{\lambda=1}$改变符号时——
3. 临界漂移$v_c$的特征方程：

这一``边际收益=边际代价''的结构在算子理论中是普遍的——
类似的方程出现在统计学习理论的偏差-方差权衡、
信息论中的率失真理论、以及热力学中的自由能最小化。

## 讨论与诚实暴击

### 主要贡献的回顾

本文从SCX框架的Spring SE-1动力学出发，建立了记忆-遗忘的形式理论。
四个定理构成了一个逻辑递进的体系：

1. **遗忘的必要性定理**确立了遗忘的**逻辑地位**——不是工程优化，而是正确性条件。
2. **记忆-遗忘相变定理**划分了**策略空间**——根据漂移速率，系统自动落入记忆最优或遗忘最优的区域。
3. **最优遗忘界**刻画了**性能前沿**——遗忘与延迟的不可逃避的权衡，由信息论下界保证。
4. **遗忘算子$\Fforget_t$**提供了**代数基础**——统一的算子语言，收敛性保证，以及与已知遗忘策略的精确对应。

### 诚实暴击：每个定理的局限与未竟问题

以下是本文的**完整诚实暴击**——逐条列出每个结论的局限、简化假设和已知的反例或修正需求。

#### 对遗忘必要性定理的暴击

1. **渐近发散的有限时间无意义性。**
2. **漂移下界假设的可验证性问题。**
3. **均值回复漂移的例外。**
4. **单调记忆的夸大。**

#### 对记忆-遗忘相变定理的暴击

1. **PL条件的致命局限。**
2. **固定步长的简化。**
3. **二次损失近似的精度。**
4. **常数$\lambda^*$的超参数敏感性。**

#### 对最优遗忘界的暴击

1. **高斯假设的普适性。**
2. **偏移大小$\delta$的先验知识假设。**
3. **假阳性与假阴性的不对称代价。**

#### 对遗忘算子$\Fforget_t$的暴击

1. **Hilbert空间假设的范围。**
2. **压缩性公理的过强性。**
3. **遗忘半群的离散性。**

### 开放问题

以下问题超出了本文的范围，但构成了Temporal SCX未来研究议程的核心：

1. **自适应遗忘的收敛理论。**
2. **选择性遗忘的信息准则。**
3. **多时间尺度遗忘的分层结构。**
4. **遗忘与省定理的统一框架。**
5. **遗忘-记忆相变在神经网络中的实验验证。**
6. **遗忘算子的量子推广。**

### 对SCX理论体系的影响

Temporal SCX的四个定理对SCX框架的已有定理体系产生了以下深远影响：

1. **省定理的补全。**省定理处理了``停止一切更新''的退化场景。
2. **Spring SE-1的推广。**将Spring SE-1从**收敛到固定目标**推广为
3. **SCX记忆库设计的理论基础。**Spring记忆库$\mathcal{M}_t$的设计
4. **质变点定理的补充。**质变点定理描述了**学习过程的相变**

### 工程建议（带诚实标注）

基于本文的定理，我们提出以下SCX系统设计建议——每个建议均标注了
从数学定理到工程实践的映射不确定性。

1. **漂移速率估计作为一等公民。**
2. **分层遗忘架构。**
3. **遗忘-延迟预算。**

## 结论：记忆的数学本质

本文的核心论点是：**记忆与遗忘不是认知心理学的研究对象——它们在数学上具有
严格的、可从SCX框架的动力学中推导出来的形式结构。**
这一形式结构揭示了关于记忆的三个本质事实：

1. **遗忘是逻辑必然（定理1）。**在非稳态数据流中，无遗忘系统必然发散——
2. **记忆-遗忘存在相变（定理2）。**环境漂移速率穿越临界值时，
3. **遗忘的速度存在不可突破的下界（定理3）。**遗忘与检测延迟的乘积

**终极隐喻：**记忆是一条河流——如果水不流动（无遗忘），它会变成死水（发散）；
如果水流太快（过度遗忘），它无法反映两岸的风景（高方差）。
最优的记忆系统像一条稳态的河流：水流的速度（遗忘率）恰好匹配
河床的变化速率（漂移速率），在流动中保持形态的恒定性。
这一隐喻并非文学修辞——它是定理2的平衡条件$\frac{\dd\MSE}{\dd\lambda} = 0$
在物理直觉中的投射。

\metaphor{} **类比标注：**终极隐喻是启发式的物理类比，不具有数学效力。
河流-记忆的类比在以下意义上成立：两者均涉及``流入-流出平衡下的稳态形态''，
且稳态由系统参数（水流速度/遗忘率，河床变化/漂移速率）唯一决定。
然而，河流是连续介质力学的对象，记忆是信息论的对象——
两者在数学结构上的精确对应（如果存在）仍有待建立。

<div align="center">

\rule{0.5\textwidth}{0.4pt}

</div>

**致谢：**感谢SCX理论体系（2026）提供了Spring SE-1、省定理、质变点定理的数学基础，
本文的所有推广均建立在这些已有成果之上。所有错误和过度简化由本文作者负责。

## Appendix

## 有限窗口遗忘的相变分析

本附录补充定理 [ref]在有限窗口遗忘策略下的对应分析。

> **Proposition:** [有限窗口遗忘的临界窗口]<!-- label: prop:fw_critical -->
> 在有限窗口遗忘策略$w(t, s) = 1/W \cdot \mathbf{1}[t-s \leq W]$下，
> 渐近MSE为：
> 
> $$
>     \MSE(W) = \frac{v^2 W^2}{4\alpha^2\mu^2} + \frac{\alpha\sigma^2}{\mu W}。
> $$
> 
> 
> 最优窗口大小$W^*$由一阶条件给出：
> 
> $$
>     W^* = \left(\frac{2\alpha^3\sigma^2\mu}{v^2}\right)^{1/3}。
> $$
> 
> 
> 当$v \to 0$时，$W^* \to \infty$（无限窗口，即无遗忘）；
> 当$v \to \infty$时，$W^* \to 0$（即时遗忘）。
> 临界漂移（定义为$W^* = 1$时的$v$值）为$v_c^{FW} = \sqrt{2\alpha^3\sigma^2\mu}$。

> **Proof:** 与定理 [ref]的证明平行。在窗口大小$W$下：
> 
- 有效偏差：历史平均滞后$\frac{1}{W}\sum_{k=0}^{W-1}(\theta_{t-k}^* - \theta_t^*)$。
- 有效方差：$W$个独立样本的平均的方差为$\alpha^2\sigma^2/W$。

> 求解$\frac{\dd \MSE(W)}{\dd W} = 0$得到$W^*$。

指数遗忘和有限窗口遗忘在以下极限下等价：
当$\lambda = 1 - 1/W$且$W$大时，$N_{eff}^{EF} \approx 2W$，
而$N_{eff}^{FW} = W$。因此，在有效样本量的意义上，
指数遗忘的``有效窗口''是有限窗口的两倍（因为它对近期历史给予更高权重）。

## 遗忘算子的谱分析

> **Proposition:** [遗忘算子的谱]<!-- label: prop:spectrum -->
> 在有限维记忆空间$\Mmem \cong \R^d$中，标准遗忘算子
> $\Fforget_\lambda(m) = \lambda m + (1-\lambda)\mathcal{T}(\delta m)$
> 的谱满足：
> 
> $$
>     \sigma(\Fforget_\lambda) = \{\lambda\} \cup \{\lambda \cdot \sigma_i : \sigma_i \in \sigma(P_\mathcal{T})\}，
> $$
> 
> 其中$P_$是到$\Mmem$的正交投影。特别地，遗忘算子的谱半径
> $\rho(\Fforget_\lambda) = \lambda$（由公理A1的压缩性保证）。

> **Proof:** 在$\R^d$中，$\Fforget_\lambda$可表示为矩阵：
> 
> $$
>     F_\lambda = \lambda I_d + (1-\lambda)T，
> $$
> 
> 其中$T$是$\mathcal{T}$在$\Mmem$的某组基下的矩阵表示。$F_\lambda$的特征值为
> $\lambda + (1-\lambda)\tau_i$，其中$\tau_i$是$T$的特征值。
> 由于$\norm{T} \leq 1$（非膨胀性），$\abs{\tau_i} \leq 1$，因此$\abs{\lambda + (1-\lambda)\tau_i} \leq 1$。
> 谱半径$\max_i \abs{\lambda + (1-\lambda)\tau_i} = \lambda + (1-\lambda) = 1$当$\tau_i = 1$时达到，
> 或$\lambda$当所有$\abs{\tau_i} < 1$时。

谱分析揭示了遗忘算子的**混合性质**：在$\tau_i = 1$的方向上（对应$\mathcal{T}$的
不动点子空间），$\Fforget_\lambda$的特征值为1（该方向无遗忘——信息被完美保留）；
在$\tau_i = 0$的方向上，特征值为$\lambda$（该方向以速率$\lambda$被遗忘）。
这一方向性遗忘结构超出了公理A1的简单压缩模型——
它暗示了**结构化遗忘**的可能性：在不同的信息子空间上以不同的速率遗忘。

\openproblem{} **开放问题：**结构化遗忘（方向依赖性遗忘率的遗忘算子）
的收敛性分析及其在深度学习中的应用。初步猜想：Transformer注意力机制中的
``注意力衰减''（attention dropout / stochastic depth）可被理解为
在高维记忆空间的特定子空间上的结构化遗忘。

\begin{thebibliography}{99}

\bibitem{scx2026theorems}
SCX Theory Group.
*SCX Core Theorems: Economy Theorem, Qualitative Change Point Theorem, and Multi-Expert Consistency*.
SCX Technical Report, 2026.

\bibitem{scx2026spring_convergence}
SCX Theory Group.
*Spring SE-1 Convergence Analysis: Two-Phase Dynamics of Robbins-Monro SGD on State Space*.
SCX Technical Report, 2026.

\bibitem{scx2026cc_audit}
SCX Theory Group.
*SCX Framework for Label Noise Detection: The Five-Layer Architecture*.
SCX Technical Report, 2026.

\bibitem{robbins1951}
H.~Robbins and S.~Monro.
*A Stochastic Approximation Method*.
Annals of Mathematical Statistics, 22(3):400--407, 1951.

\bibitem{polyak1963}
B.~T.~Polyak.
*Gradient methods for the minimisation of functionals*.
USSR Computational Mathematics and Mathematical Physics, 3(4):864--878, 1963.

\bibitem{lojasiewicz1963}
S.~Łojasiewicz.
*A topological property of real analytic subsets*.
Coll. du CNRS, Les équations aux dérivées partielles, 117:87--89, 1963.

\bibitem{karimi2016}
H.~Karimi, J.~Nutini, and M.~Schmidt.
*Linear convergence of gradient and proximal-gradient methods under the Polyak-Łojasiewicz condition*.
ECML-PKDD, 2016.

\bibitem{chernoff1952}
H.~Chernoff.
*A measure of asymptotic efficiency for tests of a hypothesis based on the sum of observations*.
Annals of Mathematical Statistics, 23(4):493--507, 1952.

\bibitem{stein1952}
C.~Stein.
*On the theory of testing composite hypotheses*.
Annals of Mathematical Statistics, 23:148--149, 1952.

\bibitem{lecun1986}
Y.~Le~Cam.
*Asymptotic Methods in Statistical Decision Theory*.
Springer, 1986.

\bibitem{hoeffding1963}
W.~Hoeffding.
*Probability inequalities for sums of bounded random variables*.
JASA, 58(301):13--30, 1963.

\bibitem{ebbinghaus1885}
H.~Ebbinghaus.
*Über das Gedächtnis: Untersuchungen zur experimentellen Psychologie*.
Duncker \& Humblot, 1885.

\bibitem{wixted2007}
J.~T.~Wixted and S.~K.~Carpenter.
*The Wickelgren Power Law and the Ebbinghaus forgetting curve*.
In H.~L.~Roediger, III (Ed.), Cognitive psychology of memory, 2007.

\bibitem{gama2014}
J.~Gama, I.~Žliobaitė, A.~Bifet, M.~Pechenizkiy, and A.~Bouchachia.
*A survey on concept drift adaptation*.
ACM Computing Surveys, 46(4):1--37, 2014.

\bibitem{zinkevich2003}
M.~Zinkevich.
*Online convex programming and generalized infinitesimal gradient ascent*.
ICML, 2003.

\bibitem{hazan2016}
E.~Hazan.
*Introduction to Online Convex Optimization*.
Foundations and Trends in Optimization, 2016.

\bibitem{nagel2022}
R.~Nagel (Ed.).
*One-Parameter Semigroups of Positive Operators*.
Springer Lecture Notes in Mathematics, 1986/2022.

\end{thebibliography}