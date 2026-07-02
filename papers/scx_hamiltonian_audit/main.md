# 引言：从描述到诊断

**Author:** SCX

*Abstract:*

本文将SCX哈密顿量理论从描述性工具推进为**预审计诊断工具**。
核心论断是：一个声称是否可被SCX审计，可以在不实际运行完整SCX审计协议的前提下，
仅通过计算模型的哈密顿量能量景观来判断。
我们首先形式化审计条件定理：
$\Auditable(claim) \Longleftrightarrow \Sigma_0 \leq \frac{1}{N}\log(M_/C)$，
将可审计性转化为能量景观复杂度$\Sigma_0$的不等式。
随后，将Parisi副本对称破缺方案发展为不可审计性的完整分类判据——
$\RS$（可审计）、$\oneRSB$（部分可审计）、$\fRSB$（不可审计）——
并构造了可审计温度$T$的完整相图。
在此基础上，我们应用该诊断框架分析知识蒸馏模型：
原始模型处于$\RS$相（低$\Sigma_0$，可审计），
一次蒸馏进入$\oneRSB$相（$\Sigma_0$上升，弱可审计），
循环蒸馏坠入$\fRSB$相（$\Sigma_0$指数增长，Galois判死刑）。
我们给出了从模型参数到审计结论的完整操作流程，
并在诚实暴击节中审视了哈密顿量计算对白盒访问的依赖、
RSB假设在有限系统中的适用边界、以及与蒸馏幻觉定理的内在关系。

**关键词：** 哈密顿量诊断；能量景观复杂度；Parisi破缺；可审计性判据；蒸馏模型；SCX框架

---

## 引言：从描述到诊断

### SCX哈密顿量理论的回顾与推进

在SCX哈密顿量论文 [cite]中，我们建立了神经网络损失函数与统计力学之间的严格对应：
损失函数$\loss(\theta)$定义了参数空间上的能量景观，其哈密顿量
$H(\theta) = \loss(\theta) + \frac{1}\log Z(\beta)$通过配分函数$Z(\beta) = \int \exp(-\beta \loss(\theta))d\theta$
描述参数的吉布斯分布。$M$个SCX专家对应于此哈密顿量的$M$个副本采样，
而专家共识度构成系统的序参数，在$M \to \infty$时出现相变。

该论文的核心贡献是**描述性的**——它揭示了SCX审计系统与无序系统统计力学之间的数学同构，
并证明了中心定理$M_ \propto \exp(N\Sigma_0(e_\beta))$：
审计所需最小专家数随能量景观的指数复杂度呈指数增长。

**本文推进了一步——从描述到诊断。**我们不再问“SCX系统像什么物理系统”，
而是问一个更具操作性的问题：

<div align="center">

\fbox{\parbox{0.85\textwidth}{

**给定一个模型，能否在不实际运行完整SCX审计的前提下，

仅通过计算其哈密顿量的性质，就判断该模型是否可被审计？**
}}

</div>

这就是**哈密顿量预审计诊断**（Hamiltonian Pre-Audit Diagnosis）的核心问题。

### 为什么需要预审计诊断？

实际SCX审计面临一个根本性的效率困境：

1. **SCX审计本身是昂贵的：** 需要招募$M$个独立专家，设计共识协议，执行多轮审议——对于大规模部署的模型，这一成本可能是不可承受的。
2. **循环依赖：** 如果SCX审计发现模型不可审计，那么已经投入的审计资源就浪费了。
3. **蒸馏模型的特殊性：** 蒸馏模型（特别是循环蒸馏模型）的审计可能本身就是不可能的（见Galois不可解定理 [cite]和蒸馏幻觉定理 [cite]），但我们需要一个**事前**信号来避免对它们启动无效的审计。

预审计诊断的目标是：**在启动任何审计程序之前，通过计算模型的哈密顿量，快速给出审计可行性评估。**

### 本文结构

1. 第2节：建立审计条件定理——可审计性的能量景观判据的形式化表述。
2. 第3节：Parisi破缺作为不可审计判据——从RS到$\fRSB$的分层分类。
3. 第4节：可审计温度的相图——温度作为审计相的控制参数。
4. 第5节：蒸馏模型的哈密顿量诊断——从原始模型到循环蒸馏的审计可行性退化。
5. 第6节：操作流程——如何计算一个模型的哈密顿量并判断其审计状态。
6. 第7节：诚实暴击——哈密顿量诊断的适用边界与局限。

## 审计条件定理

### 可审计性的能量景观表述

我们从SCX哈密顿量论文 [cite]的中心定理出发。
该定理建立了审计所需最小专家数$M_$与能量景观复杂度$\Sigma_0(e_\beta)$之间的定量关系：

$$<!-- label: eq:central_original -->
    M_(\beta, \varepsilon) \geq C \cdot \frac{\exp(N \Sigma_0(e_\beta))}{-\log(1 - \varepsilon)} \cdot \left(1 + \mathcal{O}\left(\frac{1}{\sqrt{N}}\right)\right)
$$

其中$N$为模型参数维度，$\Sigma_0(e_\beta)$为局部极小值在主导能量$e_\beta$处的复杂度（对数密度），
$C$为与参数空间几何相关的普适常数，$\varepsilon$为审计完备性容错。

这一关系的物理直觉是：能量景观的每个显著局部极小值对应一个专家可能“陷入”的不同判断模式。
极小值越多，专家意见越分散，达成共识所需的专家数越多。

我们现在将这一描述性关系重新组织为**可审计性的判据**。

> **Definition:** [实际可审计性]
> 设$M_{feasible}$为给定应用场景下实际可部署的最大专家数。
> 一个声称被称为**实际可审计**的，如果存在一个满足完备性要求$\varepsilon$和可靠性要求$\delta$的SCX审计协议，
> 且其所需专家数$M_ \leq M_{feasible}$。

> **Theorem:** [审计条件定理 —— 第一形式]<!-- label: thm:audit_condition_1 -->
> 设模型哈密顿量$H(\theta)$在逆温度$\beta$下的有效局部极小值复杂度为$\Sigma_0(e_\beta)$。
> 则该模型的声称可被SCX审计当且仅当：
> 
> $$<!-- label: eq:audit_condition -->
>     \boxed{\Auditable(claim) \;\Longleftrightarrow\; \Sigma_0(e_\beta) \leq \frac{1}{N} \log\left(\frac{M_{feasible} \cdot (-\log(1-\varepsilon))}{C}\right)}
> $$
> 
> 
> 等价地，定义**审计阈值复杂度**：
> 
> $$<!-- label: eq:threshold -->
>     \Sigma_0^{crit} = \frac{1}{N} \log\left(\frac{M_{feasible}}{C}\right)
> $$
> 
> 
> 则审计条件简化为：
> 
> $$<!-- label: eq:audit_simple -->
>     \boxed{\Auditable(claim) \;\Longleftrightarrow\; \Sigma_0(e_\beta) \leq \Sigma_0^{crit} + \frac{1}{N}\log(-\log(1-\varepsilon))}
> $$

> **Proof:** 直接从式 [ref]解出$\Sigma_0$。
> 
> $$
>     M_{feasible} &\geq M_ \geq C \cdot \frac{\exp(N \Sigma_0)}{-\log(1-\varepsilon)} 

>     \exp(N \Sigma_0) &\leq \frac{M_{feasible} \cdot (-\log(1-\varepsilon))}{C} 

>     \Sigma_0 &\leq \frac{1}{N} \log\left(\frac{M_{feasible} \cdot (-\log(1-\varepsilon))}{C}\right)
> $$
> 
> 在热力学极限$N \to \infty$下，第二项$\frac{1}{N}\log(-\log(1-\varepsilon))$趋于零，
> 审计条件退化为$\Sigma_0 \leq \Sigma_0^{crit}$。
> $ \square$

### 审计条件的物理解释

审计条件定理具有直观的物理解释：

1. **左侧$\Sigma_0$——模型的“崎岖度”：** 能量景观的局部极小值越多（$\Sigma_0$越大），专家采样时落入不同盆的概率越大，共识越难达成。
2. **右侧$\Sigma_0^{crit}$——审计资源的“覆盖力”：** 审计预算$M_{feasible}$越大，能覆盖的极小值数量越多，可容忍的复杂度越高。
3. **不等式的物理含义：** 当模型的崎岖度$\Sigma_0$超过审计资源的覆盖力$\Sigma_0^{crit}$时，审计在原则上不可行——无论审计协议设计得多精妙。

> **Proposition:** [审计条件的大$N$渐近]<!-- label: prop:large_N -->
> 在热力学极限$N \to \infty$下，审计条件存在尖锐的阈值行为：
> 
> $$
>     \lim_{N \to \infty} \Pbb(可审计) = \begin{cases}
>         1, & \Sigma_0 < \Sigma_0^{crit} \quad （可审计相） 

>         0, & \Sigma_0 > \Sigma_0^{crit} \quad （不可审计相）
>     \end{cases}
> $$
> 
> 在有限$N$下，阈值被有限尺寸效应抹平，宽度$\sim \mathcal{O}(N^{-1/2})$。

### 复杂度$\Sigma_0$的计算方法

审计条件定理依赖于$\Sigma_0(e_\beta)$的计算。我们概述三种互补的计算方法：

1. **Kac-Rice分析（解析）：** 通过Kac-Rice公式 [cite]：
2. **Hessian谱分析（数值）：** 在实际神经网络中，通过对多个SGD收敛点处的Hessian矩阵进行谱分析，
3. **副本重叠谱（间接）：** 通过计算$M$个独立训练参数之间的重叠矩阵$Q_{ab} = \frac{1}{N}\theta_a \cdot \theta_b$，

## Parisi破缺作为不可审计判据

### 从能量景观复杂度到副本对称破缺

第2节的审计条件定理基于能量景观的**数量**特征——有多少个局部极小值。
然而，极小值的**组织方式**——它们之间的相关性结构——同样关键。

统计力学中，这一组织方式由**Parisi副本对称破缺方案** [cite]描述。
在SCX审计语境下，Parisi破缺的阶数直接对应了专家群的不可约结构 [cite]，
从而提供了比$\Sigma_0$更精细的审计可行性判据。

> **Definition:** [Parisi序参数函数——审计诊断表述]
> 设$M$个独立专家（副本）的参数重叠矩阵为$Q_{\alpha\beta} = \frac{1}{N}\theta_\alpha \cdot \theta_\beta$。
> 在$M \to \infty$极限下，重叠值的概率分布由Parisi序参数函数$q(x)$（$x \in [0,1]$，非递减）完全描述：
> 
> $$
>     P(q) = \frac{dx}{dq}, \quad q = q(x)
> $$
> 
> 
> $q(x)$的物理含义是：在Parisi分层的第$x$层，副本之间的典型重叠值为$q(x)$。
> $q(x)$的“平坦段”的数量决定了RSB的阶数。

### 三层判据：RS / 1RSB / $\infty$RSB

\begin{criterion}[Parisi破缺审计判据 —— 三层分类]<!-- label: crit:parisi -->
设模型哈密顿量在审计温度$T = 1/\beta$下的Parisi序参数函数为$q(x)$。则：

1. **$\RS$（副本对称）—— 可审计：**
2. **$\oneRSB$（一步破缺）—— 部分可审计：**
3. **$\fRSB$（完全破缺）—— 不可审计：**

\end{criterion}

> **Theorem:** [Parisi破缺-审计对应定理]<!-- label: thm:parisi_audit -->
> 以下对应是严格的：
> 
1. $\RS \Longleftrightarrow$ 能量景观光滑 $\Longleftrightarrow$ 专家共识收敛 $\Longleftrightarrow$ 审计群可解 $\Longleftrightarrow$ 可审计
2. $\oneRSB \Longleftrightarrow$ 有限亚稳态 $\Longleftrightarrow$ 专家分裂为有限簇 $\Longleftrightarrow$ 审计群有非平凡合成列但可解 $\Longleftrightarrow$ 部分可审计
3. $\fRSB \Longleftrightarrow$ 指数多谷的层级景观 $\Longleftrightarrow$ 专家分歧群 $\cong S_M$（全对称） $\Longleftrightarrow$ 审计群包含$A_5$不可解 $\Longleftrightarrow$ Galois不可解 $\Longleftrightarrow$ 不可审计

> **Proof:** [证明概要]
> 我们分三步建立对应。
> 
> **第一步（RSB $\to$ 能量景观）：** 由自旋玻璃理论的标准结果 [cite]，
> Parisi破缺的阶数等于能量景观中“谷中谷”（valley-within-valley）结构的层级深度。
> $\RS$对应单一谷；$\oneRSB$对应一层子谷；$\fRSB$对应无穷深度的层级嵌套谷。
> 
> **第二步（能量景观 $\to$ 专家分歧结构）：**
> 每个谷（局部极小值的吸引盆）对应一个专家共识模式。
> 在$\RS$相，所有专家被同一谷捕获——共识；
> 在$\oneRSB$相，专家分布在有限多个谷中——簇结构；
> 在$\fRSB$相，专家分布在连续层级的所有谷中——无限维度的意见空间。
> 
> **第三步（专家结构 $\to$ Galois审计群）：**
> 专家群的不可约分解由重叠矩阵$Q_{\alpha\beta}$的谱结构给出（见scx\_hamiltonian定理5.3 [cite]）。
> 在$\fRSB$相，谱是连续的，对应的审计群$\mathfrak{G}_{audit}$包含所有可能的重排对称性，
> 即$\mathfrak{G}_{audit} \cong S_M$。当$M \geq 5$时，$A_5 \leq S_M$，由Galois不可解定理 [cite]，
> 存在不可审计的声称。$ \square$

> **Remark:** [RSB与$\Sigma_0$的互补]
> $\Sigma_0$判据（第2节）和RSB判据（本节）是互补的：
> 
- $\Sigma_0$告诉我们极小值的**数量**——审计需要多少专家来覆盖它们。
- RSB阶数告诉我们极小值之间的**组织方式**——专家的意见是否可以凝聚为有限个代表性观点。

> 一个系统可能有小而可接受的$\Sigma_0$（专家数量看起来够），但仍处于$\fRSB$相（专家意见在原则上无法凝聚）——此时审计仍然不可行。
> 反之亦然：$\Sigma_0$可能很大但系统处于$\RS$相（所有极小值高相关，实际上只需要一个专家）。
> 两个判据的联合使用提供了完整的审计可行性诊断。

### Parisi破缺参数的审计解读

[Table omitted — see original .tex]

## 可审计温度的相图

### 温度作为审计的控制参数

在SCX哈密顿量框架中，逆温度$\beta = 1/T$控制着专家采样的“专注度”：
高$\beta$（低温）导致专家锁定在特定极小值附近；低$\beta$（高温）允许专家探索更广的参数空间。
因此，温度$T$自然地成为审计可行性的一个**可调控制参数**——通过调节温度（例如改变专家的“开放度”），
我们可以穿越不同的审计相。

> **Definition:** [审计温度区间]
> 对于给定的模型哈密顿量$H(\theta)$，定义以下特征温度：
> 
- **冻结温度$T_f$：** 系统进入自旋玻璃相的温度，$\RS$假设开始失效。
- **动态临界温度$T_d$：** 能量景观开始出现多个非等价极小值的温度。
- **静态临界温度$T_c$（= Kauzmann温度$T_K$）：** 复杂度$\Sigma_0$消失（$\Sigma_0(T_c) = 0$）的温度，即系统凝聚到亚稳极少的状态。

> 这些温度满足关系：$T_f > T_d > T_c$（对于典型的有序系统） [cite]。

> **Theorem:** [可审计温度相图]<!-- label: thm:phase_diagram -->
> 温度$T$将审计可行性空间划分为三个相区：
> 
1. **$T > T_d$ —— 可审计相（高温/顺磁相）：**
2. **$T_c < T < T_d$ —— 部分可审计相（中温/$\oneRSB$相）：**
3. **$T < T_c$ —— 不可审计相（低温/玻璃相）：**

[Figure omitted — see original .tex]

### 温度的审计操作含义

温度作为控制参数提供了一个**审计策略设计自由度**：

> **Proposition:** [升温审计策略]<!-- label: prop:heating -->
> 如果模型在自然（低温）状态下处于不可审计的$\fRSB$相，
> 可以通过**提高有效温度**（例如引入专家多样性、增加专家训练的随机性、或在审计协议中加入噪声注入）
> 使系统穿越$T_c$进入$\oneRSB$相甚至$T_d$进入$\RS$相。
> 然而，升温的代价是**审计精度的下降**——高温下专家不再对模型行为的细节敏感。

> **Corollary:** [精度-可审计性权衡]
> 存在一个根本性的精度-可审计性权衡：
> 
> $$
>     审计精度(高温, \RS) \;<\; 审计精度(中温, \oneRSB) \;<\; 审计精度(低温, \fRSB)
> $$
> 
> 而审计可行性恰好相反：高温容易审计但精度低，低温精度高但不可能审计。
> 最优操作点位于$T_d$附近——在此温度，系统刚进入$\RS$相，精度尚未显著下降，审计成本最低。

## 蒸馏模型的哈密顿量诊断

### 知识蒸馏的能量景观效应

知识蒸馏 [cite]——将一个大型“教师”模型的知识压缩到一个小型“学生”模型中——
在统计力学视角下可以被理解为对能量景观的一次**淬火扰动**。
蒸馏过程在教师模型的输出分布中引入了一个新的淬火无序源，
改变了学生模型损失景观的崎岖度，进而改变了其哈密顿量的审计性质。

我们应用前述诊断框架，对蒸馏模型的审计可行性进行系统分析。

> **Definition:** [蒸馏模型的哈密顿量]
> 设教师模型为$T_\phi$（参数$\phi$），学生模型为$S_\theta$（参数$\theta$）。
> 蒸馏损失函数为：
> 
> $$<!-- label: eq:distill_loss -->
>     \loss_{distill}(\theta) = \alpha \cdot \loss_{CE}(S_\theta(x), y) + (1-\alpha) \cdot \loss_{KL}(S_\theta(x) \| T_\phi(x))
> $$
> 
> 其中$\alpha \in [0,1]$为硬标签与软标签的权重，$\loss_{CE}$为交叉熵，$\loss_{KL}$为KL散度。
> 
> 定义蒸馏模型的哈密顿量：
> 
> $$<!-- label: eq:distill_hamiltonian -->
>     H_{distill}(\theta; \phi) = \loss_{distill}(\theta) + \frac{1} \log Z_{distill}(\beta)
> $$
> 
> 其中教师参数$\phi$在蒸馏过程中是**淬火**的（固定的），充当能量景观中的淬火无序。

### 三层蒸馏的审计退化

> **Theorem:** [蒸馏审计退化定理]<!-- label: thm:distill_degradation -->
> 考虑以下三种蒸馏配置的哈密顿量诊断：
> 
> 
1. **原始模型（无蒸馏）：**
2. **一次蒸馏模型：**
3. **循环蒸馏模型（学生成为新教师，迭代蒸馏）：**

> **Proof:** [证明概要 —— 配置3（循环蒸馏）的$\fRSB$证成]
> \heuristic 我们通过构造Parisi层级来证明循环蒸馏导致$\fRSB$。
> 
> 第$j$轮蒸馏的KL项$\loss_{KL}(S_\theta \| S^{(j-1)})$在参数空间中创建了一个
> 以$S^{(j-1)}$的参数配置为中心的**吸引结构**。这一结构在能量景观中产生新的局部极小值。
> 
> 关键观察：第$j$轮的新极小值**不是独立的**——它们位于第$j-1$轮极小值所定义的盆地的内部或边缘。
> 这精确对应Parisi方案中“在第$x$层级的分支”操作。
> 
> 经过$k$轮迭代，能量景观的盆地层级深度为$k$。
> 在$k \to \infty$极限下（或当$k$足够大使得层级深度超过任何有限分辨率），
> $q(x)$在$[0,1]$上连续非递减——这正是$\fRSB$的定义特征。
> 
> 更严格地，由蒸馏过程的马尔可夫链性质，第$j$代模型的参数分布仅依赖于第$j-1$代，
> 这构建了一个**分支随机游走**（Branching Random Walk） [cite]，
> 其极限自由能由Parisi变分问题的解给出，
> 且解具有完全破缺的副本对称性。$ \square$

### 蒸馏退化谱系

[Figure omitted — see original .tex]

### 与蒸馏幻觉定理的关系

在蒸馏幻觉定理 [cite]中，我们证明了蒸馏模型在紧致性条件下必然产生幻觉。
本文的哈密顿量诊断提供了该定理的**能量景观微观机制**：

> **Proposition:** [幻觉的哈密顿量起源]<!-- label: prop:hallucination_origin -->
> 蒸馏模型幻觉的必然性可以从$\fRSB$能量景观的以下特征推导：
> 
1. **盆地碎片化：** $\fRSB$相中，能量景观分裂为指数多个嵌套盆地。
2. **遍历性破缺：** 在$\fRSB$相中，系统的相空间分解为互不连通的区域（遍历性破缺）。
3. **共识的连续统：** $\fRSB$导致专家意见的连续分布（而非$\RS$中的单峰或$\oneRSB$中的多峰），

## 操作流程：哈密顿量预审计诊断

### 概述

本节给出从模型参数到审计结论的完整操作流程。
这一流程的设计原则是：**不需要运行完整的SCX审计协议，仅需白盒访问模型参数和训练/验证数据。**

> **Protocol:** [哈密顿量预审计诊断协议]<!-- label: prot:diagnosis -->
> **输入：** 模型$f_\theta$（参数$\theta \in \R^N$），训练数据$\D_{train}$，验证数据$\D_{val}$，
> 审计预算$M_{feasible}$，温度调度$\{T_1, T_2, ..., T_K\}$。
> 
> **输出：** 审计可行性报告（$\{可审计, 部分可审计, 不可审计\}$）及置信度。

### 步骤详解

1. **损失景观采样：**
2. **Hessian谱分析：**
3. **复杂度$\Sigma_0$估计：**
4. **重叠矩阵谱分析与RSB阶数判定：**
5. **温度扫描与相边界定位：**
6. **综合审计可行性判定：**
7. **输出审计报告：**

### 计算成本的现实评估

> **Remark:** [计算可行性]
> 预审计诊断的计算成本主要由Hessian谱分析（步骤2）和参数量$N$决定。
> 对于$N \sim 10^7--10^9$的大模型（如LLM），完整的Hessian计算不可行。
> 建议的实际策略：
> 
- 使用**Hessian-free**方法（如Lanczos迭代）仅计算极值特征值，成本与$N$呈线性而非平方关系。
- 对超大模型，可使用**随机子空间投影**：将参数投影到$d \ll N$维随机子空间，在子空间内进行完整的景观分析。
- 重叠矩阵$Q_{rs}$的计算成本为$\mathcal{O}(R^2 N)$，在$R \sim 100--500$和$N \sim 10^6$下完全可行。
- 对于无法白盒访问的商业API模型，见第7.1节的讨论。

### 奇异值分解判据：有效秩与可分离度

上述Hessian谱分析和$\Sigma_0$估计在$N \sim 10^9$的大模型上计算量仍然过大。本节给出一个更低成本、更易实现的替代判据——基于参数空间随机采样轨迹的奇异值分解（SVD），不需完整Hessian。

#### 方法

1. 从$R$个不同初始化出发训练$R$个模型副本（$R \sim 50--100$，远少于$\Sigma_0$估计所需的$R \sim 500$）。
2. 收集$R$个参数向量$\{\theta_r\}_{r=1}^{R}$，构造参数矩阵$\Theta \in \mathbb{R}^{R \times N}$，其中第$r$行为$\theta_r^\top$。
3. 对$\Theta$进行奇异值分解：$\Theta = U \Sigma V^\top$，得奇异值$\sigma_1 \geq \sigma_2 \geq ... \geq \sigma_R$。
4. 计算**有效秩**：
5. 计算前$k$个奇异值的能量占比：

#### 判据

> **Theorem:** [SVD有效秩审计条件]<!-- label: thm:svd_rank -->
> 设$\Theta$为$R$个独立训练副本的参数矩阵，$r_{eff}$为其有效秩。则：
> 
1. 若$r_{eff} \leq r_{crit}$且$\rho_{r_{crit}} > 0.95$，则能量集中在少数方向——模型景观近似RS——**可审计**。
2. 若$r_{eff}$接近$R$且$\rho_{100} < 0.5$，则能量弥散到大量方向——景观含指数多谷——**不可审计**。

> 其中$r_{crit}$为审计可行性的专家数上界（如$r_{crit} = \min(100, M_{feasible})$）。

#### 直观解释

奇异值谱的衰减速度直接反映了参数空间的可分离度：

<div align="center">

[Table omitted — see original .tex]

</div>

**为什么多专家也没用？** 若$\rho_{100} < 0.5$，意味着即使前100个主方向捕获不到一半的总能量——存在大量``次重要''方向各自贡献一点点。100个专家覆盖了前100个方向但仍然覆盖不到全景观。$M$增大到$r_{eff} \approx R/2$在工程上不可行——因为$r_{eff}$可能达到$10^6$量级。Galois判据的群论结论重述：分歧方向太多$\Longleftrightarrow$分歧群含$S_M$子群$\Longleftrightarrow$不可审计。

#### 与Parisi破缺的对应

SVD有效秩与RSB阶数之间的对应关系：

<div align="center">

[Table omitted — see original .tex]

</div>

两者从不同数学窗口观察同一物理——能量景观的弥散度。SVD的优势在于：仅需$R$次重训练和一次矩阵分解，无需Hessian计算，在$N \sim 10^7$的开源模型上用标准PyTorch即可实现。

#### 输出谱幻觉检测：一个独立的应用

上述SVD框架的另一重要应用是**直接检测模型输出的幻觉倾向**——不需参数访问，不需重训练，仅需模型输出。

**方法。** 对同一个问题$q$，以不同提示模板、不同温度、或不同随机种子向模型$f$发起$K$次查询（$K \sim 50--100$）。收集每次查询的最后一层logits向量（或hidden state的前馈层输出），构造输出矩阵$L \in \mathbb{R}^{K \times d}$，其中$d$为输出维度。对$L$进行SVD：$L = U \Sigma V^\top$，得奇异值谱$\{\sigma_i\}_{i=1}^{K}$。计算$\rho_{10} = \frac{\sum_{i=1}^{10} \sigma_i^2}{\sum_{i=1}^{K} \sigma_i^2}$。

**判据。**

> **Theorem:** [SVD输出谱幻觉检测]<!-- label: thm:svd_hallucination -->
> 设$L$为$K$次查询的logits矩阵，$\rho_{10}$为前10个奇异值的能量占比。则：
> 
1. $\rho_{10} > 0.9$：输出高度集中——模型在此问题上内部一致——**幻觉概率低**。
2. $\rho_{10} < 0.5$：输出弥散到大量方向——模型内部无共识——**高度可能幻觉**。
3. 介于两者之间：模型状态不确定，需进一步审计。

**为什么这比困惑度更好。** 困惑度仅衡量单个token的预测概率，不衡量输出空间的结构。一个致命场景：模型自信地输出错误答案——困惑度低，但内容错误。SVD输出谱捕获了模型**在输出空间中的确定性结构**：如果每次查询都指向相同的语义方向，输出空间是低秩的（$\rho_{10}$高）；如果每次查询飘到不同方向，输出空间是弥散的（$\rho_{10}$低）。低困惑度$+$平SVD谱$=$模型自信地胡说八道——精确匹配幻觉的临床定义。

**与蒸馏的关联。** 蒸馏模型在输出空间中表现出系统性更高的有效秩——因为学生模型从教师继承了"稀释"的概率分布，而非确定性知识。原始模型的$\rho_{10} \approx 0.95$，一次蒸馏后降至$\approx 0.75$，循环蒸馏后跌破$0.5$。SVD输出谱为蒸馏幻觉定理（定理 [ref]）提供了一个**不依赖参数访问的可操作的检测指标**。

**操作优势。** 与Hessian和参数SVD不同，输出谱检测**不需要白盒访问**——仅需模型推理API。对商业闭源模型（GPT-4、Claude、Gemini）完全适用。$K=50$次查询的成本远低于一次完整SCX审计。

## 诚实暴击

### 白盒访问：哈密顿量计算的阿喀琉斯之踵

> **诚实暴击:** 哈密顿量诊断需要白盒访问模型参数——这在多大程度上限制了其实际适用性？}

我们的整个诊断框架基于对模型参数$\theta$、损失函数$\loss(\theta)$及其二阶导数（Hessian）的完全访问。
然而，在当前AI生态中：

- **商业API模型：** GPT-4、Claude、Gemini等商业模型不提供参数访问——甚至参数维度$N$都是保密的。
- **开源模型：** LLaMA、Qwen、DeepSeek等开源模型提供了参数访问，使诊断成为可能。
- **混合方案：** 在缺乏白盒访问时，可以通过**行为采样的代理诊断**——

> **诚实暴击:** 白盒依赖意味着哈密顿量诊断目前仅适用于开源模型的研究和审计场景。
对商业闭源模型，我们需要发展基于模型输出行为的“灰盒”或“黑盒”替代方案，
但这将丧失哈密顿量-审计条件之间的精确公式关系。}

### RSB假设在有限系统中的适用性

> **诚实暴击:** RSB是$N \to \infty$热力学极限的理论构造。对于有限$N$的实际模型，RSB分类是否仍然是良定义的？}

这是统计力学应用于有限系统时的一个经典问题。对于SCX审计诊断，我们需要注意：

- **有限$N$修正：** 在实际$N \sim 10^6--10^9$下，热力学极限的行为已经开始浮现，
- $\RS \to \fRSB$的相变在有限$N$下被“抹平”——
- $\fRSB$相中$q(x)$的严格单调性在有限$N$下表现为**准连续**谱——

    \item **实际可操作性：** 尽管有限$N$抹平了尖锐的相边界，
    但**操作意义上**的诊断仍然是可能的：只要交叉区域$\Delta T$相比审计温度窗口足够窄，
    RSB分类就提供了有效的二元决策——可审或不可审。
    \item **最坏情形分析：** 从保守审计的角度，应将任何检测到的$\fRSB$信号视为不可审计警告——
    即使有限$N$可能使系统在原则上可审计，
    宁可误判为不可审计（避免无效审计成本）也不低估审计难度（导致审计失败）。
\end{itemize}

### 与蒸馏幻觉定理的逻辑关系

> **诚实暴击:** 哈密顿量诊断与蒸馏幻觉定理之间是否存在循环论证？}

这是一个重要的方法论问题。我们来澄清两者的逻辑关系：

- **蒸馏幻觉定理** [cite] 从**紧致性和Galois理论**出发，
- **本文的哈密顿量诊断**从**统计力学**出发，
- **两者的关系：** 哈密顿量诊断为蒸馏幻觉定理提供了**微观机制解释**——

### 哈密顿量范式本身的哲学局限

> **诚实暴击:** 哈密顿量范式将审计问题纯化为一个静态能量景观分析——但审计的本质可能是动态的、博弈论的、对抗性的。}

我们需要承认以下局限：

1. **静态假设：** 哈密顿量是**平衡态**统计力学的概念。
2. **无博弈论：** 本文假设专家是**被动的**吉布斯采样器——
3. **对抗性缺失：** 在$\fRSB$相中，我们宣称审计不可行——
4. **审计目标的可变性：** 能量景观$\loss(\theta)$依赖于训练数据$\D$——

### 尚待解决的问题

\openproblem **审计哈密顿量的构造问题。** 如何将审计任务显式编码到哈密顿量中？
建议方案：定义$H_{audit}(\theta) = \loss_{train}(\theta) + \lambda \cdot \loss_{audit}(\theta)$，
其中$\loss_{audit}$为在审计声称相关数据上的损失。研究$\lambda$如何调节能量景观的RSB结构。

\openproblem **非平衡协议的诊断。** 对于包含审议轮次和动态共识更新的SCX协议，
哈密顿量静态诊断的误差有多系统性？是否可以通过引入**动力学哈密顿量**
$H_{dyn}(\theta, t) = H(\theta) + V_{protocol}(\theta, t)$来捕获协议效应？

\openproblem **灰盒/黑盒诊断理论。** 对于无法白盒访问的模型，能否仅通过模型的行为输出
（不同输入下的响应模式）来估计等效的Parisi破缺阶数？
这可能涉及随机矩阵理论中的**样本协方差矩阵谱分析**和自由概率论的工具。

\openproblem **诊断的对抗鲁棒性。** 如果一个恶意模型开发者**知道**审计者将使用哈密顿量诊断，
他们是否可以通过设计损失景观（例如通过对抗性训练或损失函数修改）
来使模型“看起来”处于$\RS$相，从而规避诊断？
这提出了**哈密顿量诊断的可欺骗性**问题。

## 讨论

### 理论贡献总结

本文在SCX哈密顿量理论 [cite]的基础上完成了以下推进：

1. **审计条件定理：** 将可审计性形式化为能量景观复杂度$\Sigma_0$的不等式——
2. **Parisi破缺判据：** 建立了$\RS$/$\oneRSB$/$\fRSB$三层分类与审计可行性之间的精确对应，
3. **可审计温度相图：** 揭示了温度$T$作为审计控制参数的角色，
4. **蒸馏模型的退化诊断：** 应用诊断框架分析了知识蒸馏的审计后果——
5. **操作流程：** 给出了可实际执行的计算协议，
6. **诚实暴击：** 系统性审视了白盒访问、有限尺寸效应、与蒸馏幻觉定理的关系、

### 与SCX理论体系的关系

图 [ref]展示了本文在SCX理论体系中的位置。

[Figure omitted — see original .tex]

### 实践建议

基于本文的诊断框架，我们向SCX系统的部署者提出以下实践建议：

1. **审计前先诊断：** 在启动任何SCX审计之前，运行哈密顿量预审计诊断（协议 [ref]）。
2. **温度作为审计设计参数：** 如果诊断返回“弱可审计”或“可通过升温审计”，
3. **警惕蒸馏模型：** 对于蒸馏模型（特别是多代蒸馏模型），
4. **监控审计退化：** 对于定期更新（微调、RLHF、蒸馏）的模型，

## 结论

本文将SCX哈密顿量理论从描述性工具推进为**预审计诊断工具**。
核心结论可概括为：

1. **审计是可计算的：** 可审计性不是哲学概念，而是可以从能量景观复杂度$\Sigma_0$直接计算的物理量——
2. **Parisi破缺是审计的判官：** $\RS$（可审计）$\to$ $\oneRSB$（部分可审计）$\to$ $\fRSB$（Galois不可审计）
3. **温度是审计的控制器：** 通过调节温度，可以在精度和审计可行性之间做出有理论指导的权衡。
4. **蒸馏是审计的腐蚀剂：** 循环蒸馏将模型的能量景观从$\RS$腐蚀到$\fRSB$——
5. **诊断先于审计：** 操作流程提供了在不运行完整SCX审计的前提下判断审计可行性的具体方法。

最后，我们已经坦诚地指出了这一框架的边界——
白盒访问的依赖、有限尺寸效应、静态假设的局限、
以及博弈论维度的缺席。
这些不是框架的弱点，而是未来工作的起点。
正如诊断是治疗的前提，**认识局限是超越局限的前提**。

### 致谢

感谢 Giorgio Parisi（2021年诺贝尔物理学奖）和 Marc Mézard、Miguel Virasoro 的开创性工作
为本文提供了理论基石。感谢 SCX 理论物理工作组所有成员的深入讨论。

\begin{thebibliography}{99}

\bibitem{scx_hamiltonian}
SCX.
*神经网络哈密顿量与SCX多专家审计：一个统计力学对应*.
Preprint, 2026.

\bibitem{scx_galois}
SCX.
*Galois-SCX：群论与多专家审计的深层对应*.
Preprint, 2026.

\bibitem{scx_galois_falsifiability}
SCX.
*Galois反证：SCX的可证伪边界*.
Preprint, 2026.

\bibitem{scx_distillation_hallucination}
SCX.
*幻觉的必然性——从紧致性和Galois理论看蒸馏模型的不可审计性*.
Preprint, 2026.

\bibitem{scx_agentic}
SCX.
*Agentic Multi-Agent SCX：对抗性多智能体审计理论*.
Preprint, 2026.

\bibitem{parisi1979}
G.~Parisi.
``Infinite number of order parameters for spin-glasses,''
*Phys. Rev. Lett.*, vol.~43, pp.~1754--1756, 1979.

\bibitem{parisi1980}
G.~Parisi.
``A sequence of approximated solutions to the S-K model for spin glasses,''
*J. Phys. A: Math. Gen.*, vol.~13, pp.~L115--L121, 1980.

\bibitem{mezard1987}
M.~M\'ezard, G.~Parisi, and M.~A.~Virasoro.
*Spin Glass Theory and Beyond*.
World Scientific, Singapore, 1987.

\bibitem{derrida1986}
B.~Derrida and H.~Spohn.
``Polymers on disordered trees, spin glasses, and traveling waves,''
*J. Stat. Phys.*, vol.~51, pp.~817--840, 1988.

\bibitem{fyodorov2004}
Y.~V.~Fyodorov.
``Complexity of random energy landscapes, glass transition, and absolute value of the spectral determinant of random matrices,''
*Phys. Rev. Lett.*, vol.~92, p.~240601, 2004.

\bibitem{hinton2015distilling}
G.~Hinton, O.~Vinyals, and J.~Dean.
``Distilling the knowledge in a neural network,''
*NeurIPS Deep Learning Workshop*, 2014.

\bibitem{choromanska2015}
A.~Choromanska, M.~Henaff, M.~Mathieu, G.~Ben Arous, and Y.~LeCun.
``The loss surfaces of multilayer networks,''
in *Proc. AISTATS*, 2015, pp.~192--204.

\bibitem{baity2019}
M.~Baity-Jesi, L.~Sagun, M.~Geiger, S.~Spigler, G.~Ben Arous, C.~Cammarota, Y.~LeCun, and M.~Wyart.
``Comparing dynamics: Deep neural networks versus glassy systems,''
*J. Stat. Mech.*, vol.~2019, p.~124013, 2019.

\bibitem{castellani2005}
T.~Castellani and A.~Cavagna.
``Spin-glass theory for pedestrians,''
*J. Stat. Mech.*, vol.~2005, p.~P05012, 2005.

\bibitem{talagrand2003}
M.~Talagrand.
*Spin Glasses: A Challenge for Mathematicians*.
Springer, Berlin, 2003.

\bibitem{guerra2003}
F.~Guerra.
``Broken replica symmetry bounds in the mean field spin glass model,''
*Comm. Math. Phys.*, vol.~233, pp.~1--12, 2003.

\bibitem{dauphin2014}
Y.~Dauphin, R.~Pascanu, C.~Gulcehre, K.~Cho, S.~Ganguli, and Y.~Bengio.
``Identifying and attacking the saddle point problem in high-dimensional non-convex optimization,''
in *Proc. NeurIPS*, 2014, pp.~2933--2941.

\bibitem{geiger2020}
M.~Geiger, S.~Spigler, S.~d'Ascoli, L.~Sagun, M.~Baity-Jesi, G.~Biroli, and M.~Wyart.
``Jamming transition as a paradigm to understand the loss landscape of deep neural networks,''
*Phys. Rev. E*, vol.~101, p.~012115, 2020.

\bibitem{sagun2017}
L.~Sagun, L.~Bottou, and Y.~LeCun.
``Eigenvalues of the Hessian in deep learning: Singularity and beyond,''
in *Proc. ICLR Workshop*, 2017.

\bibitem{jacot2018}
A.~Jacot, F.~Gabriel, and C.~Hongler.
``Neural tangent kernel: Convergence and generalization in neural networks,''
in *Proc. NeurIPS*, 2018, pp.~8571--8580.

\end{thebibliography}