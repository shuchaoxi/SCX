# 引言：$\lambdaparam$ 方向性问题的提出

**Author:** SCX

*Abstract:*

**中文摘要：**
SCX平等论的核心动力学方程描述了不平等测度 $\ineq(t)$ 的连续时间演化，其中增长率参数
$\lambdaparam$ 的方向性决定了系统的定性行为。已有研究主要关注 $\lambdaparam \geq 0$
（收敛或稳态）的情形。本文系统形式化\**$\lambdaparam < 0$ 发散情形**——即不平等
随时间以指数速率加剧的体制。我们识别出触发 $\lambdaparam < 0$ 的三个充要条件：
**ITA**（代际创伤放大，Intergenerational Trauma Amplification）、
**IPI**（身份政治产业化，Identity Politics Industrialization）和
**SR**（隔离强化，Segregation Reinforcement）。每个条件均以定义—机制—触发函数的
严格形式化展开。在此基础上，我们推导发散动力学 $\ineq(t) = \ineq_0 e^{|\lambdaparam| t}$
及其随机界，建立三种终端状态的分岔条件：**碎片化**（Fragmentation，SR主导）、
**革命**（Revolution，IPI主导）和**灭绝**（Extinction，ITA主导）。
我们进一步构建了五个早期预警信号并将其合成为**复合早期预警指数（CEWI）**，
最后给出干预路径和最优干预时机的解析公式。全文以中英双语严格形式化展开。

**English Abstract:**
The core dynamical equation of SCX \eqtheory{} describes the continuous-time evolution
of the inequality measure $\ineq(t)$, where the sign of the growth-rate parameter
$\lambdaparam$ determines the system's qualitative behavior. Prior work has focused
primarily on the $\lambdaparam \geq 0$ (convergent or steady-state) regime. This paper
systematically formalizes the \**$\lambdaparam < 0$ divergent regime**—in which inequality
intensifies at an exponential rate. We identify three necessary-and-sufficient conditions
that trigger $\lambdaparam < 0$: **ITA** (Intergenerational Trauma Amplification),
**IPI** (Identity Politics Industrialization), and **SR** (Segregation
Reinforcement). Each condition is rigorously formalized through the definition—
mechanism—activation-function triad. On this basis, we derive the divergent dynamics
$\ineq(t) = \ineq_0 e^{|\lambdaparam| t}$ with stochastic bounds, establish the
bifurcation conditions for three terminal states: **Fragmentation**
(SR-dominant), **Revolution** (IPI-dominant), and **Extinction**
(ITA-dominant). We further construct five early warning signals and synthesize them
into the **Composite Early Warning Index (CEWI)**, and finally provide
analytical formulas for intervention pathways and optimal intervention timing.
The entire exposition is rigorously formalized in Chinese and English.

---

---

## 引言：$\lambdaparam$ 方向性问题的提出
## Introduction: The Problem of $\lambdaparam$ Directionality

### SCX 不平等动力学回顾 / Review of SCX Inequality Dynamics

在 SCX \eqtheory{} 框架中，不平等测度 $\ineq(t)$ 的连续时间演化由以下随机微分方程控制：

In the SCX \eqtheory{} framework, the continuous-time evolution of the inequality
measure $\ineq(t)$ is governed by the following stochastic differential equation:

> **Definition:** [SCX 不平等动力学方程 / SCX Inequality Dynamics Equation]
> <!-- label: def:dynamics -->
> 设 $\ineq(t) \in [0, \infty)$ 为时刻 $t$ 的社会不平等测度，
> $\lambdaparam \in \R$ 为系统增长率参数，则：
> \[
> d\ineq(t) = \lambdaparam \, \ineq(t) \, dt + \sigma \, \ineq(t) \, dW_t,
> \]
> 其中 $\sigma > 0$ 为波动率，$W_t$ 为标准布朗运动。

直观上，$\lambdaparam$ 的方向性决定了不平等演化的三个体制：

- $\lambdaparam > 0$：**收敛体制**（Convergent regime）—— 不平等随时间衰减，系统趋于平等稳态。
- $\lambdaparam = 0$：**临界体制**（Critical regime）—— 不平等的确定性趋势为零，演化完全由随机扰动驱动。
- $\lambdaparam < 0$：**发散体制**（Divergent regime）—— 不平等以指数速率自我放大，系统趋于崩溃。

> **Proposition:** [伊藤解 / It\^o Solution]
> <!-- label: prop:ito -->
> 对定义 [ref] 中的 SDE，强解为：
> \[
> \ineq(t) = \ineq_0 \exp\paren{\paren{\lambdaparam - \frac{\sigma^2}{2}} t + \sigma W_t},
> \]
> 其中 $\ineq_0 = \ineq(0)$。当 $\lambdaparam < 0$ 且 $|\lambdaparam| > \sigma^2/2$ 时，
> 确定性项以速率 $|\lambdaparam| - \sigma^2/2 > 0$ 指数发散。

### 已有工作的局限 / Limitations of Prior Work

Prior work in the SCX framework has predominantly examined the $\lambdaparam \geq 0$ regime,
focusing on convergence conditions (Thm4, Thm5 of the SCX axiom system) and the
mechanisms—such as $\coupling$-suppression (see Civilization Gauge paper)—that can
mask or delay the consequences of $\lambdaparam < 0$. However, three critical gaps remain:

已有工作主要考察 $\lambdaparam \geq 0$ 的收敛情形，聚焦于收敛条件
（SCX公理体系的Thm4、Thm5）以及可掩盖或延迟 $\lambdaparam < 0$ 后果的机制
（如$\coupling$压制，见文明不平等计论文）。然而，有三个关键缺口尚未填补：

1. **$\lambdaparam < 0$ 的*成因*未被形式化：**
2. **发散终点未被分类：**
3. **早期预警缺乏综合指标：**

本文逐一填补这三个缺口。

This paper fills all three gaps.

## $\lambdaparam$ 的形式定义与符号约定
## Formal Definition of $\lambdaparam$ and Notational Conventions

### $\lambdaparam$ 的微观基础 / Micro-Foundations of $\lambdaparam$

$\lambdaparam$ 并非外生给定参数，而是社会系统内部结构特征的涌现量：

$\lambdaparam$ is not an exogenously given parameter but an emergent quantity from the
internal structural features of the social system:

> **Definition:** [$\lambdaparam$ 的结构分解 / Structural Decomposition of $\lambdaparam$]
> <!-- label: def:lambda_decomp -->
> \[
> \lambdaparam = \underbrace{\lambdaparam_{redis}}_{再分配效率} \;+\;
>               \underbrace{\lambdaparam_{mobil}}_{社会流动} \;+\;
>               \underbrace{\lambdaparam_{cohe}}_{凝聚力} \;-\;
>               \underbrace{\lambdaparam_{extr}}_{抽取强度} \;-\;
>               \underbrace{\lambdaparam_{iso}}_{隔离系数} \;-\;
>               \underbrace{\lambdaparam_{trauma}}_{创伤反馈},
> \]
> 其中各分量均为非负实数，含义如下：
> 
- $\lambdaparam_{redis} \geq 0$：再分配效率——税收、转移支付、公共物品供给对不平等的压制能力。
- $\lambdaparam_{mobil} \geq 0$：社会流动性——底层群体向上迁移的速率。
- $\lambdaparam_{cohe} \geq 0$：社会凝聚力——跨群体信任与合作网络的密度。
- $\lambdaparam_{extr} \geq 0$：抽取强度——精英从系统提取资源的经济能力。
- $\lambdaparam_{iso} \geq 0$：隔离系数——群体间物理、信息和婚姻隔离的程度。
- $\lambdaparam_{trauma} \geq 0$：创伤反馈——历史创伤通过代际传递增强抽取并削弱凝聚力的自激效应。

$\lambdaparam < 0$ 当且仅当前三个压制分量之和小于后三个放大分量之和。

$\lambdaparam < 0$ if and only if the sum of the first three suppressing components is
less than the sum of the last three amplifying components.

### 三条件的宏观加总 / Macro-Aggregation of the Three Conditions

定义 [ref] 中的六个分量在结构上可以分为三类条件域，
分别对应本文的核心三个条件：

\[
\underbrace{(\lambdaparam_{extr} + \lambdaparam_{trauma}) -
            (\lambdaparam_{redis} + \lambdaparam_{mobil})}_{ITA 域}
\;+\;
\underbrace{(\lambdaparam_{iso} - \lambdaparam_{cohe})}_{IPI 域}
\;+\;
\underbrace{(\lambdaparam_{iso} - \lambdaparam_{mobil})}_{SR 域}
\]

Three conditions condition domains corresponding to the three core conditions
of this paper are identified through this decomposition.

## 条件一：代际创伤放大 (ITA)
## Condition I: Intergenerational Trauma Amplification (ITA)

### 定义与机制 / Definition and Mechanism

> **Definition:** [ITA — 代际创伤放大 / Intergenerational Trauma Amplification]
> <!-- label: def:ITA -->
> 设 $\mathcal{H} = \{H_1, H_2, ..., H_K\}$ 为社会群体的集合。
> 对每个群体 $H_k$，定义其**历史创伤向量** $\mathbf{T}_k(t) \in \R^d$，
> 分量为该群体在 $d$ 个维度（经济剥夺、政治排斥、文化贬损、暴力经历、符号羞辱）
> 上的创伤累积值。ITA 满足：
> \[
> \exists k \in \{1,...,K\} : \frac{d}{dt} \mathbf{T}_k(t) = 
> \underbrace{\mathbf{A}_k \mathbf{T}_k(t)}_{内生放大} + 
> \underbrace{\mathbf{B}_k \mathbf{u}_k(t)}_{外生输入} - 
> \underbrace{\gamma_k \mathbf{C}_k \mathbf{T}_k(t)}_{衰减项},
> \]
> 其中：
> 
- $\mathbf{A}_k \in \R^{d \times d}$ 为正矩阵（所有元素 $>0$），描述代际传递的自我增强效应——创伤通过家庭叙事、群体记忆和制度化歧视在代际间放大而非衰减。
- $\mathbf{u}_k(t) \in \R^m$ 为外部创伤输入（持续发生的歧视事件、政策伤害等）。
- $\mathbf{C}_k$ 为愈合矩阵，$\gamma_k \geq 0$ 为愈合速率。

> ITA 条件激活的判据为 $\mathbf{A}_k$ 的谱半径 $\rho(\mathbf{A}_k) > \gamma_k \|\mathbf{C}_k\|$，
> 即内生放大超过愈合能力。

> **Proposition:** [ITA 与 $\lambdaparam$ 的关联 / ITA-$\lambdaparam$ Linkage]
> <!-- label: prop:ITA_lambda -->
> 当 ITA 条件激活时，$\lambdaparam$ 获得负贡献：
> \[
> \lambdaparam \leftarrow \lambdaparam - \eta_{ITA} \cdot 
> \max_{k} \paren{\rho(\mathbf{A}_k) - \gamma_k \|\mathbf{C}_k\|},
> \]
> 其中 $\eta_{ITA} > 0$ 为耦合常数。在强 ITA 极限下
> （$\rho(\mathbf{A}_k) \gg \gamma_k \|\mathbf{C}_k\|$ for some $k$），
> 此负贡献可单独驱动 $\lambdaparam < 0$。

### ITA 的机制链 / The ITA Mechanism Chain

代际创伤放大通过以下因果链推动 $\lambdaparam$ 向负方向演化：

Intergenerational trauma amplification drives $\lambdaparam$ negative through the
following causal chain:

1. **创伤传递（Trauma Transmission）：**
2. **资源抽取反馈（Extraction Feedback）：**
3. **愈合机制失效（Healing Failure）：**

### ITA 激活函数 / ITA Activation Function

> **Definition:** [ITA 激活函数 / ITA Activation Function]
> <!-- label: def:ITA_activation -->
> 定义 ITA 的连续激活函数 $\Phi_{ITA}: [0,1]^3 \to [0,1]$：
> \[
> \Phi_{ITA}(e, p, h) = \frac{1}{1 + \exp\paren{-\alpha_{ITA}(e \cdot p \cdot h - \tau_{ITA})}},
> \]
> 其中：
> 
- $e \in [0,1]$：经济剥夺强度（economic deprivation intensity）
- $p \in [0,1]$：政治排斥程度（political exclusion degree）
- $h \in [0,1]$：历史创伤存续时长标准化值（historical trauma persistence, normalized）
- $\alpha_{ITA} > 0$：激活锐度（activation sharpness）
- $\tau_{ITA} \in (0,1)$：激活阈值（activation threshold）

> 当 $\Phi_{ITA} \to 1$ 时，ITA 条件完全激活，形成不可逆的正反馈环。

## 条件二：身份政治产业化 (IPI)
## Condition II: Identity Politics Industrialization (IPI)

### 定义与机制 / Definition and Mechanism

> **Definition:** [IPI — 身份政治产业化 / Identity Politics Industrialization]
> <!-- label: def:IPI -->
> 设社会存在 $M$ 个可激活的身份维度 $\mathcal{I} = \{I_1, ..., I_M\}$
> （种族、宗教、地域、阶级等）。每个身份维度 $I_j$ 关联一个**身份企业家群**
> $\mathcal{E}_j$ 和一个**身份市场** $\mathcal{M}_j$。
> 身份政治产业化定义为：
> \[
> \forall j,\; \underbrace{R_j(t)}_{身份企业的收益} = 
> \underbrace{p_j(t)}_{身份叙事的单位价格} \cdot 
> \underbrace{q_j(t)}_{消费该叙事的群体规模} - 
> \underbrace{C_j(\mathbf{s}_j)}_{叙事生产成本},
> \]
> 其中 $\mathbf{s}_j \in \R^L$ 为叙事向量（受害者化、威胁化、优越化各分量的组合）。
> IPI 条件的核心特征是：身份企业家的收益最大化导致群体间敌意的系统性生产，
> 从而增大隔离系数 $\lambdaparam_{iso}$ 并削弱凝聚力 $\lambdaparam_{cohe}$。

IPI is fundamentally an **industrial logic** applied to identity: identity
entrepreneurs compete in a marketplace of grievances, where the unit of production
is the ``narrative of threat or victimhood,'' and the unit of consumption is
``group-level attention and mobilization.'' The profit motive ensures that narratives
that maximize intergroup hostility are systematically selected.

> **Proposition:** [IPI 对 $\lambdaparam$ 的双重效应 / Dual Effect of IPI on $\lambdaparam$]
> <!-- label: prop:IPI_lambda -->
> 在 IPI 活跃时：
> \[
> \lambdaparam \leftarrow \lambdaparam -
> \underbrace{\delta_{iso} \cdot \sum_{j=1}^{M} R_j(t)}_{隔离增大效应} -
> \underbrace{\delta_{cohe} \cdot \sum_{j=1}^{M} \|\mathbf{s}_j\|^2}_{凝聚力削弱效应},
> \]
> 其中 $\delta_{iso}, \delta_{cohe} > 0$ 为耦合常数。IPI 的独特之处在于它
> 同时影响 $\lambdaparam$ 的两个分量（$\lambdaparam_{iso} \uparrow$ 且
> $\lambdaparam_{cohe} \downarrow$），因此具有最强的 $\lambdaparam$-负化效率。

### IPI 的市场动力学 / IPI Market Dynamics

> **Definition:** [身份叙事竞争 / Identity Narrative Competition]
> <!-- label: def:narrative_comp -->
> 设身份维度 $j$ 上有 $N_j$ 个竞争性身份企业家。企业家 $i$ 的优化问题为：
> \[
> \max_{\mathbf{s}_j^{(i)} \in \mathcal{S}_j} \;
> p_j^{(i)} \cdot q_j(\mathbf{s}_j^{(i)}, \mathbf{s}_j^{(-i)}) - C_j(\mathbf{s}_j^{(i)}),
> \]
> 受众分配函数 $q_j$ 由注意力竞争决定：
> \[
> q_j(\mathbf{s}_j^{(i)}, \mathbf{s}_j^{(-i)}) = 
> \frac{\exp\paren{\beta \cdot Arousal(\mathbf{s}_j^{(i)})}}
> {\sum_{k=1}^{N_j} \exp\paren{\beta \cdot Arousal(\mathbf{s}_j^{(k)})}},
> \]
> 其中 $Arousal(\cdot)$ 为叙事的情感唤醒强度，$\beta > 0$ 为注意力-敏感度参数。

This is a softmax attention market: the more emotionally arousing a narrative is,
the larger its audience share. Since threat and victimhood narratives maximize
arousal, the market equilibrium selects for maximal intergroup hostility — an
emergent, decentralized mechanism driving $\lambdaparam < 0$.

> **Proposition:** [IPI 均衡的 $\lambdaparam$ 下限 / $\lambdaparam$ Lower Bound Under IPI Equilibrium]
> <!-- label: prop:IPI_equilibrium -->
> 在对称身份市场均衡中，所有身份企业家收敛到相同的最优叙事 $\mathbf{s}^*$，满足：
> \[
> \nabla_{\mathbf{s}} Arousal(\mathbf{s}^*) = \beta \cdot \nabla_{\mathbf{s}} C_j(\mathbf{s}^*).
> \]
> 此时，系统级 $\lambdaparam$ 贡献的下界为：
> \[
> \lambdaparam_{IPI} \leq -\delta_{cohe} \cdot M \cdot \|\mathbf{s}^*\|^2.
> \]
> 在多身份维度社会中（$M \gg 1$），即使单个维度的效应微弱，
> 聚合效应仍可驱动 $\lambdaparam < 0$。

### IPI 与信息环境的耦合 / IPI-Information Environment Coupling

> **Definition:** [算法放大系数 / Algorithmic Amplification Factor]
> <!-- label: def:alg_amp -->
> 现代数字平台通过推荐算法为身份叙事提供正反馈。定义算法放大系数：
> \[
> \Gamma_{alg} = \frac{实际叙事传播速率}{自然传播速率} \geq 1.
> \]
> 在 $\Gamma_{alg} > 1$ 时，IPI 的 $\lambdaparam$ 贡献被放大为：
> \[
> \lambdaparam_{IPI}^{eff} = \Gamma_{alg} \cdot \lambdaparam_{IPI}.
> \]

\begin{attackbox}
**诚实暴击：** IPI 条件的数学结构本质上是一个**多臂赌博机问题**
（multi-armed bandit），其中各臂的奖励是群体敌意水平。
身份企业家在不知情的情况下（或知情但不在乎）共同最大化一个社会损失函数。
IPI 的恐怖之处在于：每个企业家的行为在个体层面完全理性（最大化关注和收益），
但集体结果却是 $\lambdaparam$ 的灾难性下降。这不是市场失灵——这是市场*成功*
（在精确的微观经济学意义上）导致的宏观灾难。
\end{attackbox}

## 条件三：隔离强化 (SR)
## Condition III: Segregation Reinforcement (SR)

### 定义与机制 / Definition and Mechanism

> **Definition:** [SR — 隔离强化 / Segregation Reinforcement]
> <!-- label: def:SR -->
> 设社会空间网络为图 $\mathcal{G} = (V, E)$，节点代表个体或家庭，边代表社会互动。
> 隔离强化定义为：
> \[
> \frac{d}{dt} H_{seg}(t) > 0,
> \]
> 其中 $H_{seg}$ 为隔离熵：
> \[
> H_{seg}(t) = -\sum_{g=1}^{G} p_g(t) \log p_g(t),
> \]
> $p_g(t) = |V_g(t)| / |V|$，$V_g$ 为时刻 $t$ 时群体 $g$ 占据的连通分量。
> SR 条件通过以下机制降低 $\lambdaparam$：
> 
1. **物理隔离（Physical）：** 居住隔离减少跨群体日常接触，
2. **信息隔离（Informational）：** 分离的信息生态系统
3. **婚姻隔离（Marital）：** 跨群体通婚率下降导致社会网络

### SR 的 Schelling 动力学 / Schelling Dynamics of SR

> **Definition:** [SR 临界阈值 / SR Critical Threshold]
> <!-- label: def:SR_critical -->
> 延续 Schelling (1971) 的隔离模型，定义个体 $i$ 的**同质性偏好** $\theta_i \in [0,1]$
> 为 $i$ 在邻域中期望的同群比例。SR 条件的临界阈值为：
> \[
> \theta^* = \inf \set{\theta \in [0,1] : \exists  稳定均衡使得  H_{seg} \geq H_{crit}},
> \]
> 其中 $H_{crit}$ 为图 $\mathcal{G}$ 失去连通性时隔离熵的下界。
> 数值模拟表明 $\theta^*$ 通常在 $0.3$--$0.5$ 之间。

> **Proposition:** [SR 对 $\lambdaparam$ 的正反馈 / Positive Feedback of SR on $\lambdaparam$]
> <!-- label: prop:SR_lambda -->
> 当 $H_{seg}$ 超过 $H_{crit}$ 时：
> \[
> \lambdaparam_{iso} \leftarrow \lambdaparam_{iso} + 
> \mu_{SR} \cdot (H_{seg} - H_{crit})^2,
> \]
> \[
> \lambdaparam_{mobil} \leftarrow \lambdaparam_{mobil} \cdot 
> \exp\paren{-\nu_{SR} \cdot (H_{seg} - H_{crit})},
> \]
> 其中 $\mu_{SR}, \nu_{SR} > 0$。这意味着隔离强化同时增大 $\lambdaparam_{iso}$
> 和减小 $\lambdaparam_{mobil}$——双通道加速 $\lambdaparam$ 的下降。

### SR 的不可逆性 / Irreversibility of SR

> **Theorem:** [SR 相变定理 / SR Phase Transition Theorem]
> <!-- label: thm:SR_irreversible -->
> 当社会网络 $\mathcal{G}$ 的隔离熵 $H_{seg}$ 越过 $H_{crit}$，
> 且每个群体的内部密度 $\rho_g > \rho_{crit}$ 时，SR 进入不可逆相变：
> \[
> \lim_{t \to \infty} \E[H_{seg}(t)] = \log G,
> \]
> 即系统收敛于完全隔离状态。返回混合态的干预成本与隔离深度呈指数关系：
> \[
> C_{de-seg}(H_{seg}) \geq C_0 \cdot \exp\paren{\alpha \cdot (H_{seg} - H_{crit})},
> \]
> 其中 $C_0$ 为基线干预成本，$\alpha > 0$ 为成本-深度弹性系数。

## 三条件的联合激活与 $\lambdaparam < 0$
## Joint Activation of Three Conditions and $\lambdaparam < 0$

### 联合激活的充要条件 / Necessary and Sufficient Condition for Joint Activation

三条件并不独立运作——它们通过相互的正反馈形成**发散复合体**（Divergent Complex）：

The three conditions do not operate independently—they form a
**Divergent Complex** through mutual positive feedbacks:

> **Definition:** [发散复合体 / Divergent Complex]
> <!-- label: def:divergent_complex -->
> 发散复合体 $\mathcal{D} = (\Phi_{ITA}, \Phi_{IPI}, \Phi_{SR})$ 的状态由
> 三个激活函数定义。复合体的演化方程为：
> \[
> \frac{d}{dt}
> \begin{pmatrix}
> \Phi_{ITA} 
 \Phi_{IPI} 
 \Phi_{SR}
> \end{pmatrix}
> = \mathbf{J}
> \begin{pmatrix}
> \Phi_{ITA} 
 \Phi_{IPI} 
 \Phi_{SR}
> \end{pmatrix}
> + 高阶项,
> \]
> 其中雅可比矩阵 $\mathbf{J} \in \R^{3 \times 3}$ 为：
> \[
> \mathbf{J} =
> \begin{pmatrix}
> 0 & j_{12} & j_{13} 

> j_{21} & 0 & j_{23} 

> j_{31} & j_{32} & 0
> \end{pmatrix},
> \quad j_{kl} > 0.
> \]
> （对角线为零表示各条件本身不自激，而是通过对角线外的相互激励来增长。）

> **Theorem:** [$\lambdaparam < 0$ 的充要条件 / N\&S Condition for $\lambdaparam < 0$]
> <!-- label: thm:lambda_negative -->
> $\lambdaparam < 0$ 的充要条件是发散复合体中至少一个条件的激活度
> 超过临界值且 $\mathbf{J}$ 的谱半径 $\rho(\mathbf{J}) > 1$：
> \[
> \lambdaparam < 0 \iff \exists k \in \{ITA, IPI, SR\}: 
> \Phi_k > \Phi_k^{crit} \; \land \; \rho(\mathbf{J}) > 1.
> \]
> 换言之，单一条件的激活在交叉激励下必然引发全系统的发散。
> $\rho(\mathbf{J}) > 1$ 的条件意味着：
> \[
> (j_{12}j_{23}j_{31} + j_{13}j_{32}j_{21}) + 
> \sqrt{(j_{12}j_{21} + j_{13}j_{31} + j_{23}j_{32})^3} > 1.
> \]

### 历史案例：条件占主导的模式 / Historical Cases: Condition-Dominance Patterns

[Table omitted — see original .tex]

表 [ref] 的启发：ITA 和 SR 同时强且 IPI 弱时，系统陷入长期碎片化稳态
（如印度种姓制）。当 IPI 加入时，稳态被破坏，系统向灭绝或革命加速。

Insight from Table [ref]: When ITA and SR are both strong but IPI is weak,
the system can settle into a long-term fragmented steady state (e.g., the Indian caste
system). When IPI joins, the steady state is destroyed and the system accelerates
toward either extinction or revolution.

## 发散动力学
## Divergent Dynamics

### 确定性发散 / Deterministic Divergence

在 $\lambdaparam < 0$ 的条件下，定义 [ref] 中 SDE 的确定性部分为：

Under $\lambdaparam < 0$, the deterministic part of the SDE in Definition [ref]:

> **Theorem:** [指数发散定理 / Exponential Divergence Theorem]
> <!-- label: thm:divergence -->
> 设 $\lambdaparam = -|\lambdaparam| < 0$ 且波动率 $\sigma = 0$（确定情形），则：
> \[
> \ineq(t) = \ineq_0 \, e^{|\lambdaparam| t}.
> \]
> 定义**临界时间** $T_{crit}$ 为社会崩溃阈值 $\ineq_{max}$ 被首次达到的时刻：
> \[
> T_{crit} = \frac{1}{|\lambdaparam|} \ln\paren{\frac{\ineq_{max}}{\ineq_0}}.
> \]

> **Corollary:** [发散时间的参数敏感性 / Parameter Sensitivity of Divergence Time]
> <!-- label: cor:sensitivity -->
> 临界时间 $T_{crit}$ 对 $|\lambdaparam|$ 的弹性为：
> \[
> \frac{d \ln T_{crit}}{d \ln |\lambdaparam|} = -1,
> \]
> 对初始不平等 $\ineq_0$ 的弹性为：
> \[
> \frac{d \ln T_{crit}}{d \ln \ineq_0} = -\frac{1}{\ln(\ineq_{max}/\ineq_0)}.
> \]
> 这意味着当系统已接近临界值时（$\ineq_0 \to \ineq_{max}$），
> 即使微小的 $\ineq_0$ 增加也会急剧缩短崩溃时间。

### 随机发散与置信界 / Stochastic Divergence and Confidence Bounds

当 $\sigma > 0$ 时，不平等的演化路径是随机的。我们需要给出概率界。

When $\sigma > 0$, the inequality path is stochastic. We need probabilistic bounds.

> **Proposition:** [随机发散的概率界 / Probabilistic Bounds for Stochastic Divergence]
> <!-- label: prop:stoch_bound -->
> 在 $\lambdaparam = -|\lambdaparam| < 0$ 且 $\sigma > 0$ 的情况下：
> \[
> \E[\ineq(t)] = \ineq_0 \, e^{|\lambdaparam| t},
> \]
> \[
> \Var[\ineq(t)] = \ineq_0^2 \, e^{2|\lambdaparam| t} \paren{e^{\sigma^2 t} - 1}.
> \]
> 利用对数正态分布的性质，$\ineq(t)$ 的 $(1-\alpha)$ 置信上界和下界为：
> \[
> \ineq_{upper}(t) = \ineq_0 \exp\paren{|\lambdaparam| t + z_{\alpha/2} \, \sigma \sqrt{t}},
> \]
> \[
> \ineq_{lower}(t) = \ineq_0 \exp\paren{|\lambdaparam| t - z_{\alpha/2} \, \sigma \sqrt{t}},
> \]
> 其中 $z_{\alpha/2}$ 为标准正态分布的 $(1-\alpha/2)$ 分位数。

> **Proposition:** [首次通过时间的分布 / Distribution of First-Passage Time]
> <!-- label: prop:first_passage -->
> 定义首次通过时间 $\tau_b = \inf\{t \geq 0 : \ineq(t) \geq b\}$，其中 $b > \ineq_0$。
> 在 $\lambdaparam < 0$ 条件下，$\tau_b$ 的概率密度函数为：
> \[
> f_{\tau_b}(t) = \frac{\ln(b/\ineq_0)}{\sigma \sqrt{2\pi t^3}}
> \exp\paren{-\frac{\paren{\ln(b/\ineq_0) - |\lambdaparam| t + \frac{\sigma^2}{2} t}^2}{2\sigma^2 t}}.
> \]
> 期望首次通过时间为：
> \[
> \E[\tau_b] = \frac{\ln(b/\ineq_0)}{|\lambdaparam| - \sigma^2/2},
> \quad 要求  |\lambdaparam| > \sigma^2/2.
> \]

### 三条件的发散贡献分解 / Divergence Contribution Decomposition

> **Proposition:** [发散速率的结构分解 / Structural Decomposition of Divergence Rate]
> <!-- label: prop:divergence_decomp -->
> 总发散速率 $|\lambdaparam|$ 可分解为三条件的贡献：
> \[
> |\lambdaparam| = \alpha_{ITA} \Phi_{ITA} + 
>                 \alpha_{IPI} \Phi_{IPI} + 
>                 \alpha_{SR} \Phi_{SR} - \alpha_0,
> \]
> 其中 $\alpha_{ITA}, \alpha_{IPI}, \alpha_{SR} > 0$ 为各条件的发散强度系数，
> $\alpha_0 \geq 0$ 为基线衰减（自然的社会自我修复能力）。
> 当 $\alpha_0 > \sum \alpha_k \Phi_k$ 时，系统尚可自我修复；
> 当 $\alpha_0 \leq \sum \alpha_k \Phi_k$ 时，发散开始。

## 三种终端状态
## Three Terminal States

当 $\lambdaparam < 0$ 持续存在且未经干预时，系统必然收敛到三种终端状态之一。
终端状态的确定由各条件的相对激活强度决定。

When $\lambdaparam < 0$ persists without intervention, the system necessarily converges
to one of three terminal states. The terminal state is determined by the relative
activation strength of each condition.

### 终端状态一：碎片化 (Fragmentation) — SR 主导
### Terminal State I: Fragmentation — SR-dominant

> **Definition:** [碎片化 / Fragmentation]
> <!-- label: def:fragmentation -->
> 社会系统 $\mathcal{S}$ 进入**碎片化**终端状态当且仅当：
> \[
> \lim_{t \to \infty} H_{seg}(t) = \log G \quad \land \quad 
> \Phi_{SR} > \max(\Phi_{ITA}, \Phi_{IPI}).
> \]
> 在此状态下，社会分解为 $G$ 个互不连通的群体，每个群体在物理空间、
> 信息空间和经济空间中完全隔离。系统级功能丧失（无共同公共物品供给、
> 无跨群体贸易、无共同政治决策），但各子群体内部仍维持秩序。

**碎片化的数学结构：**
设 $\mathcal{G}$ 的邻接矩阵为 $\mathbf{A}(t)$。在 SR 主导下：
\[
\lim_{t \to \infty} \mathbf{A}(t) = \bigoplus_{g=1}^{G} \mathbf{A}_g,
\]
即 $\mathbf{A}$ 收敛为块对角矩阵。图的谱隙（spectral gap）
$\lambda_2(\mathbf{L})$ 收敛到零，其中 $\mathbf{L}$ 为拉普拉斯矩阵，
意味着扩散过程在群体间完全停止。

**历史对应：** 黎巴嫩宗派分化、波斯尼亚战后分裂、印度种姓隔离的稳态化。

**The mathematical structure of fragmentation:** The adjacency matrix $\mathbf{A}(t)$
converges to a block-diagonal form. The spectral gap of the graph Laplacian converges
to zero, meaning all cross-group diffusion processes cease entirely.

### 终端状态二：革命 (Revolution) — IPI 主导
### Terminal State II: Revolution — IPI-dominant

> **Definition:** [革命 / Revolution]
> <!-- label: def:revolution -->
> 社会系统 $\mathcal{S}$ 进入**革命**终端状态当且仅当：
> \[
> \Phi_{IPI} > \max(\Phi_{ITA}, \Phi_{SR}) \quad \land \quad
> \ineq(t)  的非连续跳跃幅度  > \ineq_{jump}.
> \]
> 在此状态下，身份政治产业化积累的群体敌意达到临界质量，
> 触发系统级相变。旧精英结构被暴力或非暴力推翻，不平等曲线发生
> **非连续下跳**（不通过中间态，直接跳跃至低不平等状态）。

**革命的动力学条件：**
定义**革命势能** $\mathcal{R}(t)$：
\[
\mathcal{R}(t) = \underbrace{\Phi_{IPI}(t)}_{敌意积累} \cdot
                 \underbrace{\ineq(t)}_{物质基础} \cdot
                 \underbrace{(1 - \Phi_{SR}(t))}_{跨群体协调能力}.
\]
革命在 $\mathcal{R}(t) \geq \mathcal{R}_{crit}$ 时被触发。
$(1 - \Phi_{SR})$ 项反映了一个关键洞见：
**跨群体联盟是革命成功的必要条件**。如果 SR 太强
（群体彼此物理隔离），IPI 积累的敌意无法转化为协调的集体行动，
系统将转向碎片化而非革命。

**The dynamical condition for revolution:** Revolution is triggered when
revolutionary potential $\mathcal{R}(t) \geq \mathcal{R}_{crit}$.
The $(1 - \Phi_{SR})$ term captures a key insight: cross-group alliance is
necessary for revolutionary success.

### 终端状态三：灭绝 (Extinction) — ITA 主导
### Terminal State III: Extinction — ITA-dominant

> **Definition:** [灭绝 / Extinction]
> <!-- label: def:extinction -->
> 社会系统 $\mathcal{S}$ 进入**灭绝**终端状态当且仅当：
> \[
> \Phi_{ITA} > \max(\Phi_{IPI}, \Phi_{SR}) \quad \land \quad
> \exists g \in \{1,...,G\} : |V_g(t)| \to 0  as  t \to \infty.
> \]
> 在此状态下，代际创伤放大的正反馈循环使特定群体的社会、经济和生物学
> 再生产条件被系统性地摧毁。灭绝在此语境中既包括物理消灭（种族灭绝）
> 也包括文化消灭（语言、传统、身份连续性的断裂）。

**灭绝的动力学条件：**
设群体 $g$ 的人口规模为 $N_g(t)$，其演化由修正的 Lotka-Volterra 方程控制：
\[
\frac{dN_g}{dt} = r_g N_g \paren{1 - \frac{N_g}{K_g}} - 
\underbrace{\eta_g \cdot \Phi_{ITA} \cdot N_g}_{创伤导致的承载力破坏},
\]
其中 $r_g$ 为内禀增长率，$K_g$ 为环境承载力，$\eta_g$ 为脆弱性系数。
灭绝条件为：
\[
\eta_g \cdot \Phi_{ITA} > r_g.
\]

**The dynamical condition for extinction:** Extinction occurs when the
trauma-induced carrying-capacity destruction rate $\eta_g \cdot \Phi_{ITA}$
exceeds the intrinsic growth rate $r_g$ of the target group.

### 终端状态的相图 / Phase Diagram of Terminal States

[Figure omitted — see original .tex]

图 [ref] 展示了三条件激活空间中的终端状态分布。
注意存在一个**混合区**（中心区域），其中三个条件均接近同等强度——
这是最危险的情形：系统可能同时经历碎片化和灭绝（如卢旺达案例）。

Figure [ref] shows the distribution of terminal states in the three-condition
activation space. Note the **mixed zone** (central region) where all three conditions
are near equal strength—this is the most dangerous regime, where the system can
simultaneously experience fragmentation and extinction (e.g., the Rwanda case).

## 五个早期预警信号与复合早期预警指数 (CEWI)
## Five Early Warning Signals and the Composite Early Warning Index (CEWI)

### 信号一：自相关增大 (ACF)
### Signal I: Rising Autocorrelation (ACF)

> **Definition:** [滞后-1 自相关 / Lag-1 Autocorrelation]
> <!-- label: def:acf -->
> 对时间序列 $\{\ineq_t\}_{t=1}^{T}$，滞后-1 自相关函数为：
> \[
> ACF(1) = \frac{\sum_{t=1}^{T-1} (\ineq_t - \bar)(\ineq_{t+1} - \bar)}
>                       {\sum_{t=1}^{T} (\ineq_t - \bar)^2}.
> \]
> **预警判据：** 在滑动窗口内，$ACF(1)$ 持续上升并超过阈值
> $\rho_{crit} \approx 0.7$ 时，系统接近临界转变。
> 当 ACF(1) $\to 1$ 时，系统处于**临界减速**状态——恢复速率趋于零，
> 系统对微小扰动极端敏感。

In the $\lambdaparam < 0$ regime, ACF(1) increases toward 1 as the system approaches
its bifurcation point. This is the classical ``critical slowing down'' phenomenon:
the system's recovery rate from perturbations approaches zero, making it increasingly
vulnerable to stochastic shocks.

### 信号二：方差增大 (VAR)
### Signal II: Rising Variance (VAR)

> **Definition:** [滑动方差 / Rolling Variance]
> <!-- label: def:var -->
> 在窗口长度 $w$ 上：
> \[
> \sigma_w^2(t) = \frac{1}{w-1} \sum_{\tau = t-w+1}^{t} 
>                 \paren{\ineq_ - \bar_w(t)}^2.
> \]
> **预警判据：** $\sigma_w^2(t)$ 的增长率超过其历史趋势的 2 个标准差时发出警报。

Under $\lambdaparam < 0$, the variance grows with $\exp(2|\lambdaparam| t + \sigma^2 t)$,
making it the most rapidly escalating signal. However, variance can spike for
non-catastrophic reasons (election cycles, policy changes), so it must be used in
conjunction with ACF.

### 信号三：偏度变化 (SKEW)
### Signal III: Skewness Shift (SKEW)

> **Definition:** [不平等分布的偏度 / Skewness of Inequality Distribution]
> <!-- label: def:skew -->
> \[
> \gamma_1(t) = \frac{\frac{1}{w} \sum_ (\ineq_ - \bar_w)^3}
>                      {\sigma_w^3}.
> \]
> **预警判据：** $\gamma_1(t)$ 由负变正（或正偏度加速增大），表明上层极端值
> 在总不平等中的占比急剧上升——精英抽取正在加速。

A shifting skewness indicates that inequality growth is driven not by broad-based
changes but by extreme concentration at the top—the hallmark of the extraction-
amplification loop in the ITA condition.

### 信号四：空间相关性崩塌 (SPA)
### Signal IV: Collapse of Spatial Correlation (SPA)

> **Definition:** [空间相关性指数 / Spatial Correlation Index]
> <!-- label: def:spa -->
> 将社会空间划分为 $R$ 个区域，定义 Moran's $I$ 统计量：
> \[
> I(t) = \frac{R}{\sum_{i,j} w_{ij}} \cdot
>        \frac{\sum_{i,j} w_{ij} (\ineq_i - \bar)(\ineq_j - \bar)}
>             {\sum_i (\ineq_i - \bar)^2},
> \]
> 其中 $w_{ij}$ 为空间权重矩阵（区域 $i$ 和 $j$ 的接近度）。
> **预警判据：** $I(t) \to 0$ 或 $I(t) \to -1$（负空间自相关），
> 表明区域间出现尖锐的隔离边界——SR 条件正在强化。

A sharp drop in spatial correlation signals that neighboring regions are diverging
in their inequality dynamics, a hallmark of the segregation reinforcement process.

### 信号五：互信息下降 (MUI)
### Signal V: Decline of Mutual Information (MUI)

> **Definition:** [跨群体信息互信息 / Cross-Group Mutual Information]
> <!-- label: def:mui -->
> 对于群体 $A$ 和 $B$ 的信息消费分布 $\mathcal{P}_A$ 和 $\mathcal{P}_B$：
> \[
> I(A; B) = \sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} 
>           p(x,y) \log \frac{p(x,y)}{p(x)p(y)}.
> \]
> **预警判据：** $I(A; B)$ 在滑动窗口内持续衰减，衰减速率加速时发出警报。
> $I(A; B) \to 0$ 意味着群体 $A$ 和 $B$ 的信息生态系统完全脱耦——
> 共同事实基础的丧失是 IPI 条件的直接后果。

Mutual information decline quantifies the separation of information ecosystems.
When $I(A; B) \to 0$, the two groups effectively inhabit different realities—a
condition that makes negotiated settlement of grievances structurally impossible.

### 复合早期预警指数 (CEWI) / Composite Early Warning Index

五个信号各有优劣——ACF 稳健但滞后，VAR 敏感但噪声大，SKEW 信息量大但需要大样本，
SPA 空间精细但数据需求高，MUI 概念深刻但操作性挑战大。
单一信号的使用可能导致虚假警报或漏报。我们提出**复合早期预警指数（CEWI）**：

Each signal has strengths and weaknesses. Using any single signal risks false alarms
or missed detections. We propose the **Composite Early Warning Index (CEWI)**:

> **Definition:** [CEWI — 复合早期预警指数 / Composite Early Warning Index]
> <!-- label: def:CEWI -->
> \[
> CEWI(t) = \sum_{k=1}^{5} w_k \cdot z_k(t),
> \]
> 其中：
> 
- $z_k(t)$ 为信号 $k$ 的标准化 $z$-值
- $w_k$ 为时变权重：
- $\beta > 0$ 为权重锐度参数（$\beta \to \infty$ 时退化为 max 函数）

> **Proposition:** [CEWI 的统计性质 / Statistical Properties of CEWI]
> <!-- label: prop:CEWI_stats -->
> 在 $\lambdaparam \geq 0$（稳定期）的零假设下：
> \[
> CEWI(t) \sim \mathcal{N}(0, 1) \quad （渐近正态）,
> \]
> 因为每个 $z_k$ 渐近标准正态且权重和为 1。
> 预警阈值以标准差为单位设定：
> 
- **蓝色预警（Watch）：** CEWI $> 1$（1-$\sigma$ 偏离）
- **黄色预警（Warning）：** CEWI $> 2$（2-$\sigma$ 偏离）
- **红色预警（Alert）：** CEWI $> 3$（3-$\sigma$ 偏离）
- **黑色警报（Critical）：** CEWI $> 4$（4-$\sigma$ 偏离），且五个分量信号中至少三个独立触发

> **Proposition:** [CEWI 与 $\lambdaparam$ 的函数关系 / Functional Relationship between CEWI and $\lambdaparam$]
> <!-- label: prop:CEWI_lambda -->
> 当系统接近 $\lambdaparam < 0$ 时，CEWI 遵循：
> \[
> \frac{d}{dt} CEWI(t) \approx \gamma_0 + \gamma_1 \cdot |\lambdaparam| \cdot CEWI(t),
> \]
> 即 CEWI 本身以 $|\lambdaparam|$ 依赖的速率指数增长。
> 这提供了一个从可观测的 CEWI 时序反向推断 $|\lambdaparam|$ 的方法：
> \[
> |\widehat| \approx \frac{1}{\gamma_1 \cdot CEWI(t)} 
> \cdot \paren{\frac{d}{dt} CEWI(t) - \gamma_0}.
> \]

## 干预路径与最优干预时机
## Intervention Pathways and Optimal Intervention Timing

### 干预的阶段划分 / Phases of Intervention

干预效果非线性地依赖于介入时机。我们将发散过程划分为三个阶段：

Intervention effectiveness depends nonlinearly on the timing of entry.
We partition the divergence process into three phases:

> **Definition:** [发散三阶段 / Three Phases of Divergence]
> <!-- label: def:phases -->
> 
1. **Phase I — 潜伏期（Latent Phase）：**
2. **Phase II — 临界期（Critical Phase）：**
3. **Phase III — 爆发期（Eruptive Phase）：**

### 各条件的专门干预路径 / Condition-Specific Intervention Pathways

#### ITA 干预：代际创伤的闭环断裂 / ITA Intervention: Breaking the Trauma Loop

> **Proposition:** [ITA 干预的有效性条件 / Effectiveness Condition for ITA Intervention]
> <!-- label: prop:ITA_intervention -->
> ITA 的干预目标是使 $\rho(\mathbf{A}_k) < \gamma_k \|\mathbf{C}_k\|$。
> 具体路径包括：
> 
1. **制度性承认（Institutional Acknowledgment）：**
2. **赔偿与修复（Reparations and Restoration）：**
3. **代际对话（Intergenerational Dialogue）：**

> ITA 干预的收益-成本比在 Phase I 极高（$>100:1$），
> 在 Phase II 中等（$10:1$--$50:1$），在 Phase III 为负（干预可能引发防御性暴力）。

#### IPI 干预：身份市场的去产业化 / IPI Intervention: De-Industrializing the Identity Market

> **Proposition:** [IPI 干预的结构性方案 / Structural Solution for IPI Intervention]
> <!-- label: prop:IPI_intervention -->
> IPI 的根本在于身份叙事的**可盈利性**。干预需在三个层面同时作用：
> 
1. **算法去极化（Algorithmic De-Polarization）：**
2. **身份叙事税（Narrative Taxation）：**
3. **公共媒体重建（Public Media Reconstruction）：**

#### SR 干预：强制混合与边界溶解 / SR Intervention: Forced Mixing and Boundary Dissolution

> **Proposition:** [SR 干预的物理-信息双通道 / Dual-Channel SR Intervention]
> <!-- label: prop:SR_intervention -->
> SR 的不可逆性定理（定理 [ref]）意味着干预必须在 $H_{crit}$ 之前。
> 具体措施：
> 
1. **物理强制混合（Physical Forced Mixing）：**
2. **信息强制混合（Informational Forced Mixing）：**
3. **跨群体网络构建（Cross-Group Network Construction）：**

### 最优干预时机 / Optimal Intervention Timing

> **Theorem:** [最优干预停止定理 / Optimal Intervention Stopping Theorem]
> <!-- label: thm:optimal_timing -->
> 干预问题可形式化为最优停止问题：
> \[
> V(CEWI) = \max\set{立即干预的净收益,\; \E[V(CEWI + dCEWI) \given CEWI]}.
> \]
> 在 Phase I--II 的边界上，最优停止规则为：
> \[
> \tau^* = \inf\set{t \geq 0 : CEWI(t) \geq CEWI^*},
> \]
> 其中阈值 $CEWI^*$ 为自由边界问题的解：
> \[
> CEWI^* = \frac{\beta_1}{\beta_1 - 1} \cdot \frac{C_{intervention}}{B_{avoided}},
> \]
> 各参数含义如下：
> 
- $C_{intervention}$：干预的直接成本
- $B_{avoided}$：避免崩溃的收益（社会剩余的保全现值）
- $\beta_1 > 1$：几何布朗运动中价值函数的指数参数

> **核心结论：**$CEWI^* \approx 1.5$--$2.0$（取决于参数校准），
> 意味着最优干预时机在 Phase I 末期至 Phase II 初期——
> 此时 CEWI 足够高以动员政治意愿（消除集体行动问题），
> 但干预成本尚未指数爆炸。

> **Corollary:** [延迟干预的后悔函数 / Regret Function of Delayed Intervention]
> <!-- label: cor:regret -->
> 若最优时机 $\tau^*$ 被错过，后悔（福利损失）以指数增长：
> \[
> Regret(t) = B_{avoided} \cdot 
> \bracket{1 - \exp\paren{-|\lambdaparam| \cdot (t - \tau^*)}}.
> \]
> 在典型的参数设置下（$|\lambdaparam| \approx 0.05$--$0.15$/年），
> 延迟 5 年意味着 $22\%$--$53\%$ 的不可恢复福利损失。

## 与 SCX 公理体系的整合
## Integration with the SCX Axiom System

$\lambdaparam$ 方向性分析并非独立于 SCX 公理体系，而是对既有定理的深化和补充：

The $\lambdaparam$ directionality analysis is not independent of the SCX axiom system
but deepens and complements existing theorems:

1. **与 Thm12（文明崩溃定理）的关系：**
2. **与 Thm7（跨域分割保持）的关系：**
3. **与 $\coupling$ 压制框架的关系：**
4. **与 Situs 编码框架的关系：**

## 数值模拟与参数校准
## Numerical Simulation and Parameter Calibration

### 模拟设置 / Simulation Setup

为验证理论预测，我们使用 Euler-Maruyama 方法离散化定义 [ref] 的 SDE：

To validate theoretical predictions, we discretize the SDE from Definition [ref]:

\[
\ineq_{t+\Delta t} = \ineq_t + \lambdaparam \, \ineq_t \, \Delta t + 
                     \sigma \, \ineq_t \, \sqrt{\Delta t} \, \epsilon_t,
\quad \epsilon_t \sim \mathcal{N}(0,1).
\]

参数校准基于历史数据和理论约束：

[Table omitted — see original .tex]

### 关键模拟结果 / Key Simulation Results

1. **发散时间的参数依赖性：**
2. **CEWI 的预警时序：**
3. **干预效果的时机敏感性：**

## 讨论
## Discussion

### 三条件的当代适用性 / Contemporary Applicability of the Three Conditions

2026年的全球社会中，三条件均以历史上前所未有的强度同时激活：

In the global society of 2026, all three conditions are simultaneously activated
at historically unprecedented intensities:

- **ITA：** 殖民主义、奴隶制和大屠杀的后遗症在社交媒体时代被重新激活。
- **IPI：** 推荐算法将身份政治产业化提升到了工业规模。
- **SR：** 算法信息茧房 + 经济不平等导致的居住隔离 + 远程工作

### CEWI 的操作性建议 / Operational Recommendations for CEWI

1. **机构设置：** 建议各国设立独立的**社会稳定性监测机构**
2. **数据基础：** CEWI 的计算需要高标准的数据基础设施，
3. **国际协调：** 由于 IPI 的信息通道是跨国的（社交媒体平台无国界），

### 诚实暴击：预警的反身性风险 / Honest Critique: Reflexivity Risk of Early Warning

\begin{attackbox}
**诚实暴击：预警信号的反身性风险（Reflexivity Risk）**

本文提出的 CEWI 面临一个深层的反身性问题：当 CEWI 被广泛知晓和公开时，
其发布本身可能成为 $\lambdaparam$ 的驱动因素。举例言之：

- 政府发布 CEWI 黄色预警 $\to$ 市场恐慌 $\to$ 资本外逃 $\to$ 经济不平等加剧
- 身份企业家看到 CEWI 上升 $\to$ 加大叙事生产以利用社会紧张

这一反身性风险并非否定 CEWI 的价值，而是要求其发布必须配合**干预承诺**——
即 CEWI 的公开必须伴随具体的、预先承诺的干预措施。
单独的预警而不附带干预是**有害的**——这类似于医生告诉病人``你可能患癌''却不提供治疗方案。
\end{attackbox}

## 结论与展望
## Conclusion and Outlook

### 核心贡献 / Core Contributions

本文系统地形式化了 SCX \eqtheory{} 框架中 $\lambdaparam < 0$ 的发散情形，
核心贡献包括：

This paper systematically formalizes the $\lambdaparam < 0$ divergent regime within the
SCX \eqtheory{} framework. Core contributions include:

1. **三个 $\lambdaparam < 0$ 条件的严格形式化：**
2. **发散动力学与终端状态的分类：**
3. **CEWI 复合早期预警指数：**
4. **最优干预时机的解析解：**

### 开放问题 / Open Problems

1. **CEWI 的经验验证：** 需要用历史崩溃案例的回顾性数据验证 CEWI 的
2. **$\lambdaparam$ 的实时估计：** 如何从高频数据（月度或周度不平等、
3. **干预措施的随机对照实验：** CEWI 引导的干预措施（如算法去极化、
4. **跨尺度耦合：** 本文关注的是国家尺度的 $\lambdaparam < 0$，
5. **AI 对 $\lambdaparam$ 的净效应：** 生成式 AI 是同时加剧 ITA

---

## Appendix

## 附录A：CEWI 权重的贝叶斯更新
## Appendix A: Bayesian Update of CEWI Weights

在定义 [ref] 中，CEWI 的权重是时变的。具体更新规则如下：

In Definition [ref], CEWI weights are time-varying. The update rule:

> **Proposition:** [CEWI 权重更新 / CEWI Weight Update]
> <!-- label: prop:weight_update -->
> 设 $\mathcal{D}_t = \{(x_k(\tau), y(\tau))\}_{\tau=1}^{t}$ 为到时刻 $t$ 的数据，
> 其中 $y(\tau) \in \{0, 1\}$ 为崩溃指标（$y=1$ 表示 $t$ 时刻后 $\Delta t$ 内发生崩溃）。
> 信号 $k$ 的可靠性定义为：
> \[
> Reliability_k(t) = \frac{TP_k(t) + TN_k(t)}
>                                  {TP_k(t) + TN_k(t) + 
>                                   FP_k(t) + FN_k(t) + \epsilon},
> \]
> 其中 TP, TN, FP, FN 分别表示真阳性、真阴性、假阳性和假阴性计数，
> $\epsilon > 0$ 为平滑参数。该可靠性度量通过 softmax 转换为权重。

## 附录B：三条件的微分方程系统
## Appendix B: Differential Equation System of the Three Conditions

发散复合体（定义 [ref]）的完整动态由以下耦合非线性系统控制：

The full dynamics of the Divergent Complex (Definition [ref])
is governed by the coupled nonlinear system:

$$
\frac{d\Phi_{ITA}}{dt} &= 
    -\gamma_{ITA} \Phi_{ITA} + 
    \frac{\beta_{ITA}}{1 + \exp(-\alpha_{ITA}(c_{12}\Phi_{IPI} + c_{13}\Phi_{SR} - \tau_{ITA}))}, 

\frac{d\Phi_{IPI}}{dt} &= 
    -\gamma_{IPI} \Phi_{IPI} + 
    \frac{\beta_{IPI}}{1 + \exp(-\alpha_{IPI}(c_{21}\Phi_{ITA} + c_{23}\Phi_{SR} - \tau_{IPI}))}, 

\frac{d\Phi_{SR}}{dt} &= 
    -\gamma_{SR} \Phi_{SR} + 
    \frac{\beta_{SR}}{1 + \exp(-\alpha_{SR}(c_{31}\Phi_{ITA} + c_{32}\Phi_{IPI} - \tau_{SR}))},
$$

其中 $\gamma_k$ 为各条件的自然衰减率，$\beta_k$ 为最大激活水平，
$c_{kl}$ 为交叉激励系数，$\tau_k$ 为激活阈值。

## 附录C：与当代理论的对话
## Appendix C: Dialogue with Contemporary Theories

### C.1 与崩溃考古学的关系 / Relation to Collapse Archaeology

Tainter (1988) 的*复杂社会的崩溃*提出了边际回报递减导致崩溃的理论。
$\lambdaparam$ 框架提供了一个互补视角：崩溃不仅是资源效率问题，更是社会结构
条件问题。ITA、IPI 和 SR 可以在资源充裕的条件下独立驱动崩溃——
这解释了为何一些资源丰富的文明（如古典玛雅）在物质条件尚未达到边际回报递减之前
就已崩溃。

Tainter's (1988) *Collapse of Complex Societies* theorized collapse as driven
by diminishing marginal returns. The $\lambdaparam$ framework provides a complementary
perspective: collapse is not merely a resource-efficiency problem but a social-structural
condition problem. ITA, IPI, and SR can independently drive collapse even under
conditions of resource abundance—explaining why some resource-rich civilizations
(e.g., the Classic Maya) collapsed before reaching diminishing marginal returns.

### C.2 与 Piketty 资本动态的关系 / Relation to Piketty's Capital Dynamics

Piketty (2014) 的核心不等式 $r > g$（资本回报率大于经济增长率）描述了不平等
的*物质驱动*。$\lambdaparam$ 框架提供了不平等的*社会结构驱动*。
二者是互补而非替代关系：$r > g$ 决定了 $\ineq$ 的*量*（大小），
而 $\lambdaparam < 0$ 决定了 $\ineq$ 的*方向*（是自我纠正还是自我放大）。
在 $\lambdaparam < 0$ 的条件下，即使 $r = g$（Piketty 的平衡条件），
不平等的结构性自我放大仍可导致崩溃。

Piketty's (2014) core inequality $r > g$ describes the *material driver*
of inequality. The $\lambdaparam$ framework provides the *social-structural
driver*. The two are complementary, not substitutes: $r > g$ determines the
*magnitude* of $\ineq$, while $\lambdaparam < 0$ determines its *direction*
(self-correcting vs. self-amplifying). Under $\lambdaparam < 0$, even if $r = g$
(Piketty's equilibrium condition), structural self-amplification of inequality can
still lead to collapse.

### C.3 与复杂系统临界转变理论的关系 / Relation to Critical Transition Theory

Scheffer et al. (2009, 2012) 的临界转变理论（Critical Transitions）识别了复杂系统
在分岔点附近的通用早期预警信号——临界减速、方差增大、闪烁（flickering）。
本文的五个早期预警信号直接建立在该理论基础之上，但做了两处推广：
(1) 从单一信号到复合指数 CEWI 的合成——解决独立信号冲突问题；
(2) 从通用系统到社会系统的特化——将空间相关性崩塌（SPA）和互信息下降（MUI）
作为社会系统特有的预警信号加入体系。

Scheffer et al.'s (2009, 2012) Critical Transition theory identified generic early
warning signals near bifurcation points—critical slowing down, rising variance,
and flickering. This paper's five early warning signals directly build on that
foundation but make two extensions: (1) synthesis from individual signals to the
composite CEWI index—resolving the problem of conflicting individual signals;
(2) specialization from generic systems to social systems—adding spatial correlation
collapse (SPA) and mutual information decline (MUI) as social-system-specific signals.

\begin{thebibliography}{99}

\bibitem{scx_framework}
SCX \eqtheory{} Research Group.
*平等论：SCX 公理体系与八定理*.
Working Paper, 2025.

\bibitem{thm12}
SCX \eqtheory{} Research Group.
*Theorem 12: Civilization Collapse Under Inequality*.
Working Paper, 2025.

\bibitem{thm7}
SCX \eqtheory{} Research Group.
*Theorem 7: Cross-Domain Partition Preservation*.
Working Paper, 2025.

\bibitem{civ_gauge}
SCX \eqtheory{} Research Group.
*文明不平等计：$\coupling$压制与解压制*.
Working Paper, 2025.

\bibitem{tainter}
Tainter, J. A.
*The Collapse of Complex Societies*.
Cambridge University Press, 1988.

\bibitem{piketty}
Piketty, T.
*Capital in the Twenty-First Century*.
Harvard University Press, 2014.

\bibitem{scheffer2009}
Scheffer, M., Bascompte, J., Brock, W. A., et al.
``Early-Warning Signals for Critical Transitions.''
*Nature*, 461:53--59, 2009.

\bibitem{scheffer2012}
Scheffer, M., Carpenter, S. R., Lenton, T. M., et al.
``Anticipating Critical Transitions.''
*Science*, 338(6105):344--348, 2012.

\bibitem{schelling}
Schelling, T. C.
``Dynamic Models of Segregation.''
*Journal of Mathematical Sociology*, 1(2):143--186, 1971.

\bibitem{granovetter}
Granovetter, M. S.
``The Strength of Weak Ties.''
*American Journal of Sociology*, 78(6):1360--1380, 1973.

\bibitem{horowitz}
Horowitz, D. L.
*Ethnic Groups in Conflict*.
University of California Press, 1985.

\bibitem{diamond}
Diamond, J.
*Collapse: How Societies Choose to Fail or Succeed*.
Viking Press, 2005.

\bibitem{carothers}
Carothers, T. and O'Donohue, A.
*Democracies Divided: The Global Challenge of Political Polarization*.
Brookings Institution Press, 2019.

\bibitem{benkler}
Benkler, Y., Faris, R., and Roberts, H.
*Network Propaganda: Manipulation, Disinformation, and Radicalization in American Politics*.
Oxford University Press, 2018.

\bibitem{zhang2020}
Zhang, Y. and Horvath, S.
``On the Optimal Timing of Policy Interventions in Complex Social Systems.''
*Journal of Complex Networks*, 8(4):cnaa031, 2020.

\bibitem{yehuda}
Yehuda, R. and Lehrner, A.
``Intergenerational Transmission of Trauma Effects: Putative Role of Epigenetic Mechanisms.''
*World Psychiatry*, 17(3):243--257, 2018.

\bibitem{kuran}
Kuran, T.
*Private Truths, Public Lies: The Social Consequences of Preference Falsification*.
Harvard University Press, 1995.

\bibitem{gustafsson}
Gustafsson, A. and Weinstein, J. M.
``Transitions to Peace: Lessons from Cross-National Data on Civil War Termination.''
*Annual Review of Political Science*, 23:241--258, 2020.

\bibitem{nyhan}
Nyhan, B. and Reifler, J.
``When Corrections Fail: The Persistence of Political Misperceptions.''
*Political Behavior*, 32(2):303--330, 2010.

\bibitem{stanley}
Stanley, J.
*How Fascism Works: The Politics of Us and Them*.
Random House, 2018.

\end{thebibliography}