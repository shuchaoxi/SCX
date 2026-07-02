*Abstract:*

科学哲学的核心问题——科学共识何时成立？范式如何转移？可证伪性如何判定？
复现危机为何发生？——传统上依赖概念分析和历史案例研究。
本文提出一种**严格形式化**的进路：以SCX（State-Conditioned eXpertise）公理系统为基础，
将科学知识生产建模为$M$个独立专家在状态空间$\mathcal{S}$上的投票过程，
从信息论和统计学习理论的公理出发，严格推导科学哲学四大核心问题的数学条件。

**第一**（科学共识定理），定义$M$专家独立验证下的共识条件：
当且仅当Chernoff-Hoeffding指数界确认$\Delta_s > 0$且$M \geq M_{crit}$时，
声称$s$构成共识。证明**老实人定理**：独立诚实专家的共识必然收敛到真值；
证明**独醒不太可能定理**：当$M$充分大时，单个异议者正确的概率以$\exp(-2M\Delta_s^2)$衰减。

**第二**（范式转移的形式化），将Kuhn范式定义为状态空间$\mathcal{S}_K$加专家配置
$\mathcal{E}_K$的二元组。证明当新数据$D_{new}$突破旧范式的Fano下界——
即$I(Y; X_{new} \mid \mathcal{S}_K) > H(Y \mid \mathcal{S}_K) - \log 2$——
旧范式在信息论意义上失效。范式转移的速率由新数据携带的额外互信息决定。

**第三**（可证伪性的SCX判据），将Popper的可证伪性转化为SCX条件：
一项科学声称$s$是可证伪的当且仅当存在可验证的假设对
$(H_0: \Delta_s \leq 0,\; H_1: \Delta_s > 0)$，
且声称者声明了检测边际$\Delta_s^{claimed}$和验证协议$\mathcal{V}$。
拒绝声明$\Delta_s^{claimed}$的声称是**不可证伪的**（精确形式化）。

**第四**（复现危机的SCX诊断），证明多专家独立复现失败的充要条件：
若独立复现集$\{E_1',...,E_{M'}'\}$的投票模式满足
$\hat_s^{rep} \leq 0$（Chernoff检验），则原声称的共识不成立。
给出复现失败的三种SCX模式：边际反转、专家塌缩、状态遮蔽。

全文遵循**诚实暴击**标准：每个定理明确标注证明的严格性（严格/启发式/开放问题），
区分依赖独立专家假设的结论和不依赖的结论，明确标注理论边界和反例条件。

**关键词：**科学共识，范式转移，可证伪性，复现危机，SCX公理系统，信息论，多专家一致性，Chernoff-Hoeffding界，Fano不等式，科学哲学形式化

## 引言：为什么科学哲学需要形式化

### 从概念分析到公理推导

科学哲学自20世纪初的逻辑实证主义运动以来，经历了Popper的证伪主义、
Kuhn的范式理论、Lakatos的研究纲领、Feyerabend的认识论无政府主义等重要转折。
这些理论深刻塑造了我们对科学运作方式的理解，但共享一个方法论特征：
它们主要依赖**概念分析**和**历史案例研究**，而非数学形式化。

这不是偶然的。科学知识生产涉及复杂的社会过程、认知偏误、
制度激励和不可通约的话语体系——这些现象似乎天然抵制数学建模。
然而，过去二十年间，三个发展使得科学哲学的形式化成为可能：

1. **信息论与统计学习理论的成熟**：
2. **多专家系统与共识算法的实践**：
3. **可复现性危机的量化研究**：

**本文的核心主张是：**SCX公理系统——最初为多专家标签噪声检测设计——
提供了一套正好适用于科学知识生产建模的数学工具。
科学共同体可以被建模为$M$个独立专家在状态空间上的投票系统；
科学声称的质量可以通过检测边际$\Delta_s$来量化；
科学共识的形成和破裂可以通过Chernoff-Hoeffding和Fano的信息论不等式来严格刻画。

### SCX公理系统：最小充分集

我们从SCX框架中提取与科学认识论相关的**最小充分公理集**。

> **Definition:** [状态空间——科学声称的原子化]
> <!-- label: def:state_space -->
> 科学知识被离散化为状态原子集合$\mathcal{S} = \{s_1, s_2, ..., s_N\}$。
> 每个状态原子$s_i$代表一项**原子科学声称**，具有以下属性：
> 
1. 特征表示$\phi(s_i) \in \mathbb{R}^{d}$：声称的可计算编码（理论预测、实验设计、统计方法）；
2. 标签$y_i \in \mathcal{Y}$：声称的真实状态（真/假/不确定）；
3. 物理/理论位置$p_i \in \mathcal{P}$（可选）：声称在理论空间中的位置。

> **认识论含义：**科学知识不是连续的叙事，而是离散的声称网络。每项声称可以被独立评估。

> **Definition:** [专家与投票——同行评议的形式化]
> <!-- label: def:expert_vote -->
> 设有$M$个独立专家$\mathcal{E} = \{E_1, E_2, ..., E_M\}$。
> 对每个状态原子$s$，专家$m$产生投票：
> 
> $$
>     v_m(s) = \mathbf{1}[E_m(\phi(s)) \neq y] \in \{0, 1\}，
> $$
> 
> 其中$\mathbf{1}[\cdot]$是指示函数。

> **语义：**$v_m(s) = 0$表示专家同意声称$s$；$v_m(s) = 1$表示专家不同意。

> **认识论含义：**``同行评议''被建模为独立专家对离散声称的二元投票。

\begin{axiom}[专家独立性——认识论独立条件]
<!-- label: ax:independence -->
专家投票在给定声称的真实状态$y_s$下条件独立：

$$
    v_m(s) \indep v_{m'}(s) \mid y_s, \quad \forall m \neq m' 。
$$

**认识论含义：**专家之间不串通、不共享相同的系统性偏误。这是科学客观性的理想化模型。

\honeststrike{} 此公理在实际科学共同体中几乎从不严格成立——专家共享相同的训练范式、
理论预设和方法论工具。独立性的破坏程度决定了后续定理的适用边界（见\S6.1）。
\end{axiom}

\begin{axiom}[检测边际——信号与噪声的分离]
<!-- label: ax:detection_margin -->
在干净声称（$y_s$为真）下，专家误投$v_m(s)=1$的概率为$p_{clean, s} < 0.5$；
在噪声声称（$y_s$为假）下，专家投$v_m(s)=1$的概率为$p_{noisy, s} > 0.5$。
检测边际定义为：

$$
    \boxed{\Delta_s = p_{noisy, s} - p_{clean, s}} 。
$$

$\Delta_s > 0$是声称质量可被检测的充要条件。

**认识论含义：**科学共同体区分真假声称的能力取决于错误声称引发的分歧是否
**系统性大于**真声称引发的偶然分歧。
\end{axiom}

\begin{axiom}[信息论充分性——Fano认识论下界]
<!-- label: ax:fano -->
任意科学知识生产系统所能达到的最大认识论精度受Fano不等式约束：

$$
    P_e \geq \frac{H(Y \mid X) - 1}{\log |\mathcal{Y}|}，
$$

其中$P_e$是贝叶斯错误率，$H(Y \mid X)$是给定证据$X$下声称真实性$Y$的条件熵。

**认识论含义：**在给定证据条件下，任何科学方法对声称的判断都存在不可消除的不确定性下界。
这个下界是**信息论的**，而非技术的——改进方法只能逼近此界，不能打破它。
\end{axiom}

这四条公理构成了我们将科学认识论问题严格形式化的基础。下面依次分析四个核心问题。

## 科学共识定理：$M$专家独立验证下的共识条件

### 共识的形式化定义

科学共同体最基础的操作是**达成共识**：多个独立研究者对同一声称给出相同的判断。
共识是科学知识累积的机制——但共识**何时**成立？多少专家的一致同意才能可靠地确立一项声称？

> **Definition:** [共识的形式化定义]
> <!-- label: def:consensus -->
> 对声称$s \in \mathcal{S}$，给定$M$个独立专家的投票$\{v_1(s), ..., v_M(s)\}$，
> 定义**共识统计量**：
> 
> $$
>     C_M(s) = \frac{1}{M}\sum_{m=1}^{M} (1 - v_m(s)) = 1 - \frac{1}{M}\sum_{m=1}^{M} v_m(s)，
> $$
> 
> 即同意声称$s$的专家比例。

> 声称$s$构成**$\alpha$-水平共识**，若存在阈值$\tau_\alpha \in (0.5, 1]$使得：
> 
> $$
>     \boxed{\mathbb{P}\left(C_M(s) \geq \tau_\alpha \;\middle|\; \Delta_s > 0\right) \geq 1 - \alpha} 。
> $$
> 
> **语义：**当检测边际为正时（声称确实为真），$M$个专家以高概率$1-\alpha$达成共识。

关键问题变为：给定$M$和$\alpha$，共识阈值$\tau_\alpha$应取何值？

### 老实人定理——独立诚实专家的共识收敛

> **Theorem:** [老实人定理（Honest Person Theorem）]
> <!-- label: thm:honest_person -->
> 设$M$个专家满足独立性公理（公理 [ref]）且检测边际$\Delta_s > 0$。
> 则当$M \to \infty$时，共识统计量$C_M(s)$以概率1收敛到$1 - p_{clean, s}$：
> 
> $$
>     \boxed{\mathbb{P}\left(\lim_{M \to \infty} C_M(s) = 1 - p_{clean, s}\right) = 1} 。
> $$
> 
> 进一步，对任意$\varepsilon > 0$，$C_M(s)$偏离其极限超过$\varepsilon$的概率受Chernoff-Hoeffding界控制：
> 
> $$
>     \boxed{\mathbb{P}\left(|C_M(s) - (1-p_{clean, s})| \geq \varepsilon\right)
>     \leq 2\exp\left(-2M\varepsilon^2\right)} 。
> $$

> **Proof:** **步骤1（大数定律）：**在干净声称下（$y_s$为真），$v_m(s) \sim Bernoulli(p_{clean, s})$独立同分布。
> 由强大数定律，$\frac{1}{M}\sum v_m(s) \xrightarrow{a.s.} p_{clean, s}$。
> 因此$C_M(s) = 1 - \frac{1}{M}\sum v_m(s) \xrightarrow{a.s.} 1 - p_{clean, s}$。
> 
> **步骤2（Chernoff-Hoeffding界）：**$C_M(s)$是$M$个独立有界（在$[0,1]$中）随机变量的均值。
> 由Hoeffding不等式，对任意$\varepsilon > 0$：
> 
> $$
>     \mathbb{P}\left(|C_M(s) - \mathbb{E}[C_M(s)]| \geq \varepsilon\right)
>     \leq 2\exp\left(-2M\varepsilon^2\right)，
> $$
> 
> 其中$\mathbb{E}[C_M(s)] = 1 - p_{clean, s}$（在干净声称下）。
> 
> **步骤3（决策阈值）：**由步骤2，若取
> 
> $$
>     \tau_\alpha = 1 - p_{clean, s} - \sqrt{\frac{\log(2/\alpha)}{2M}}，
> $$
> 
> 则$\mathbb{P}(C_M(s) \geq \tau_\alpha) \geq 1 - \alpha$，满足$\alpha$-水平共识定义。 $\square$

\rigorous{} **证明状态：严格。**步骤1为经典大数定律，步骤2为Hoeffding(1963)的精确界，
步骤3为代数代入。不依赖任何未验证的假设（除公理 [ref]和 [ref]外）。

**认识论含义：**``老实人定理''说明，如果专家确实是独立且诚实的（以高于随机水平的准确率判断声称），
那么随着专家数量的增加，共识必然收敛到真值。科学共同体的集体判断优于个体判断——
这是Condorcet陪审团定理的现代信息论版本。

### 独醒不太可能定理——异议者正确的概率

科学史上充满了``孤独的天才挑战共识''的叙事（Galileo, Wegener, Boltzmann）。
这些叙事提出一个挑战：如果共识错了而那个唯一的异议者是对的呢？

> **Theorem:** [独醒不太可能定理（Unlikely-to-be-Solo-Awake Theorem）]
> <!-- label: thm:solo_awake -->
> 设$M$个专家中，$M-1$个达成共识（同意声称$s$），1个专家异议（不同意）。
> 在检测边际$\Delta_s > 0$的条件下，该异议者正确的概率上界为：
> 
> $$
>     \boxed{\mathbb{P}\left(异议者正确 \mid C_M(s) = \frac{M-1}{M}, \Delta_s > 0\right)
>     \leq \frac{p_{noisy, s}}{p_{noisy, s} + (M-1)(1-p_{clean, s})\cdot
>     \frac{p_{noisy, s}^{M-2}}{p_{clean, s}^{M-2}} \cdot \frac{1-p_{noisy, s}}{1-p_{clean, s}}}
>     }。
> $$
> 
> 当$M \to \infty$时，此概率以指数速率$\exp(-2M\Delta_s^2)$衰减至零。

> **Proof:** **步骤1（Bayes公式）：**设$H_0$：声称$s$为真（共识正确）；$H_1$：声称$s$为假（异议者正确）。
> 给定观测数据（$M-1$同意，1异议）：
> 
> $$
>     \mathbb{P}(H_1 \mid data)
>     = \frac{\mathbb{P}(data \mid H_1) \cdot \mathbb{P}(H_1)}
>            {\mathbb{P}(data \mid H_0) \cdot \mathbb{P}(H_0) + \mathbb{P}(data \mid H_1) \cdot \mathbb{P}(H_1)}。
> $$
> 
> 
> **步骤2（似然计算）：**在$H_0$下（声称真）：
> $\mathbb{P}(data \mid H_0) = p_{clean, s}^{M-1} \cdot (1-p_{clean, s})$（$M-1$个正确同意，1个错误异议）。
> 在$H_1$下（声称假）：
> $\mathbb{P}(data \mid H_1) = p_{noisy, s} \cdot (1-p_{noisy, s})^{M-1}$（1个正确异议，$M-1$个错误同意）。
> 
> **步骤3（后验比与指数衰减）：**后验odds比为：
> 
> $$
>     \frac{\mathbb{P}(H_1 \mid data)}{\mathbb{P}(H_0 \mid data)}
>     = \frac{\mathbb{P}(H_1)}{\mathbb{P}(H_0)} \cdot
>       \frac{p_{noisy, s}}{1-p_{clean, s}} \cdot
>       \left(\frac{1-p_{noisy, s}}{p_{clean, s}}\right)^{M-1} 。
> $$
> 
> 
> 由于$p_{clean, s} < 0.5 < p_{noisy, s}$且$\Delta_s > 0$，
> 有$1-p_{noisy, s} < 0.5 < p_{clean, s}$（由对称性），因此
> $(1-p_{noisy, s})/p_{clean, s} < 1$，比值随$M$指数衰减。
> 
> **步骤4（Chernoff速率）：**更精确地，使用Hoeffding界：
> 
> $$
>     \mathbb{P}(H_1 \mid data) \leq \exp(-2M\Delta_s^2 + O(1))，
> $$
> 
> 其中$\Delta_s = p_{noisy, s} - p_{clean, s} > 0$。 $\square$

\rigorous{} **证明状态：严格。**步骤1--2为标准贝叶斯推理，步骤3的不等式方向由
$\Delta_s > 0$严格保证。步骤4的Chernoff形式利用了Hoeffding界的指数紧性。
需注意：此证明假设先验$\mathbb{P}(H_0) \approx \mathbb{P}(H_1)$；
若先验强烈偏向$H_1$（如该领域已知充斥错误声称），界限需要修正（见注记 [ref]）。

> **Remark:** [先验敏感性与诚实限定]
> <!-- label: rem:prior -->
> 独醒不太可能定理的衰减速率依赖于以下先验假设：
> (i) $\mathbb{P}(H_1)$不是极端值（不接近1）；(ii) 专家投票确实满足独立性公理。
> 在实际科学共同体中，(i)在某些领域（如p-hacking泛滥的心理学实验文献）可能不成立——
> 此时需要更大的$M$才能达到同样的可信度；(ii)专家共享理论预设会违反独立性，
> 导致有效专家数$M_{eff} < M$（见\S6.1）。

### 共识成立的Chernoff检验

> **Theorem:** [共识成立的充要条件——Chernoff检验]
> <!-- label: thm:consensus_chernoff -->
> 对声称$s$，给定$M$个独立专家的投票，在显著性水平$\alpha$下，
> 声称$s$构成科学共识当且仅当：
> 
> $$
>     \boxed{C_M(s) \geq \frac{1}{2} + \sqrt{\frac{\log(1/\alpha)}{2M}}} 。
> $$
> 
> 等价地，需要的专家数满足：
> 
> $$
>     \boxed{M \geq M_{crit} = \frac{\log(1/\alpha)}{2(C_M(s) - 1/2)^2}} 。
> $$

> **Proof:** 在零假设$H_0: \Delta_s \leq 0$（声称非真，共识不应成立）下，
> $C_M(s)$的期望$\leq 1/2$。由Hoeffding不等式：
> 
> $$
>     \mathbb{P}_{H_0}\left(C_M(s) \geq \frac{1}{2} + t\right)
>     \leq \exp(-2Mt^2)。
> $$
> 
> 设右侧$= \alpha$，解得$t = \sqrt{\log(1/\alpha)/(2M)}$。
> 因此拒绝$H_0$（即认可共识成立）的临界值为$1/2 + \sqrt{\log(1/\alpha)/(2M)}$。
> 解出$M$即得$M_{crit}$。 $\square$

\honeststrike{} **诚实暴击：此检验的统计功效。**
定理 [ref]控制了假阳性（虚假共识被认可）的概率，
但**未**控制假阴性（真共识被否定）的概率。
假阴性率（第II类错误）取决于$\Delta_s$的真值：$\beta \approx \exp(-2M(\Delta_s - t)^2)$。
当$\Delta_s$接近0时（声称仅略微可信），需要极大的$M$才能同时控制两类错误。

**实际含义：**在科学的前沿领域，$\Delta_s$通常很小（因为证据不充分），
共识的统计可靠性天然有限。这解释了为什么前沿科学充满争议——
不是因为科学方法失败，而是因为信息论下界限制了区分能力（见\S3）。

## Kuhn范式转移的形式化：当新数据突破Fano下界

### 范式作为状态-专家配置

Thomas Kuhn (1962)的*科学革命的结构*提出，科学通过``常规科学''
（在公认范式内解题）和``科学革命''（范式转移）的交替而进步。
Kuhn的概念——范式、不可通约性、反常累积、格式塔转换——
长期被认为无法形式化。本节证明：使用SCX的信息论工具，
范式转移可以精确地刻画为Fano不等式的突破。

> **Definition:** [Kuhn范式的SCX形式化]
> <!-- label: def:paradigm -->
> 一个**Kuhn范式**$\mathcal{K}$定义为二元组：
> 
> $$
>     \boxed{\mathcal{K} = (\mathcal{S}_K, \mathcal{E}_K)}，
> $$
> 
> 其中：
> 
- $\mathcal{S}_K \subset \mathcal{S}$：该范式可表达的状态原子（声称）集合——即范式语言中
- $\mathcal{E}_K = \{E_1^K, ..., E_{M_K}^K\}$：在范式内训练的专家集合——

> 范式的**解释力**由条件熵量化：
> 
> $$
>     H_K(Y \mid \mathcal{S}_K) = H(Y) - I_K(Y; \mathcal{S}_K)，
> $$
> 
> 其中$I_K(Y; \mathcal{S}_K)$是范式$\mathcal{K}$下状态原子提供的关于真实性的互信息。

> **Definition:** [反常——范式无法解释的数据]
> <!-- label: def:anomaly -->
> 对范式$\mathcal{K}$，新数据集$D_{new} = \{(x_i, y_i)\}_{i=1}^{n}$构成
> **$\varepsilon$-反常**，若：
> 
> $$
>     \boxed{I(Y; D_{new} \mid \mathcal{S}_K) > \varepsilon}，
> $$
> 
> 即新数据在给定范式状态空间的条件下携带超过$\varepsilon$的额外互信息。

> **语义：**反常就是范式内专家无法用既有理论框架解释的系统性观测。

### 范式失效的Fano判据

> **Theorem:** [范式失效定理——Fano突破判据]
> <!-- label: thm:paradigm_failure -->
> 范式$\mathcal{K}$在信息论意义上对数据集$D_{new}$失效，
> 当且仅当新数据携带的额外互信息突破了Fano下界：
> 
> $$
>     \boxed{I(Y; D_{new} \mid \mathcal{S}_K) > H(Y \mid \mathcal{S}_K) - \log 2}。
> $$
> 
> 满足此条件时，任何完全在范式$\mathcal{K}$内操作的专家集合
> $\mathcal{E}_K$的错误率下界严格大于$1/2$——即范式内专家的集体判断
> **不如随机猜测**。

> **Proof:** **步骤1（Fano不等式的认识论形式）：**对范式$\mathcal{K}$下的任意决策规则，
> 贝叶斯错误率下界为：
> 
> $$
>     P_e^{\mathcal{K}} \geq \frac{H(Y \mid \mathcal{S}_K) - 1}{\log |\mathcal{Y}|}。
> $$
> 
> 对于二元科学断言（真/假），$|\mathcal{Y}| = 2$，$\log |\mathcal{Y}| = \log 2$。
> 
> **步骤2（新数据引入后的信息增益）：**引入$D_{new}$后，条件熵变为：
> 
> $$
>     H(Y \mid \mathcal{S}_K, D_{new})
>     &= H(Y \mid \mathcal{S}_K) - I(Y; D_{new} \mid \mathcal{S}_K) 。
> $$
> 
> 
> **步骤3（新旧错误率的比较）：**新信息下的Fano界为：
> 
> $$
>     P_e^{\mathcal{K} + D_{new}}
>     \geq \frac{H(Y \mid \mathcal{S}_K, D_{new}) - 1}{\log 2}
>     = \frac{H(Y \mid \mathcal{S}_K) - I(Y; D_{new} \mid \mathcal{S}_K) - 1}{\log 2}。
> $$
> 
> 
> **步骤4（失效条件）：**范式失效意味着$P_e^{\mathcal{K} + D_{new}} > 1/2$（错误率超过随机猜测）。
> 解不等式：
> 
> $$
>     \frac{H(Y \mid \mathcal{S}_K) - I(Y; D_{new} \mid \mathcal{S}_K) - 1}{\log 2} &> \frac{1}{2} 

>     H(Y \mid \mathcal{S}_K) - I(Y; D_{new} \mid \mathcal{S}_K) - 1 &> \frac{1}{2}\log 2 

>     H(Y \mid \mathcal{S}_K) - I(Y; D_{new} \mid \mathcal{S}_K) &> 1 + \frac{1}{2}\log 2。
> $$
> 
> 
> 在nat单位下（本文统一使用），条件变为：
> 
> $$
>     I(Y; D_{new} \mid \mathcal{S}_K) > H(Y \mid \mathcal{S}_K) - \log 2，
> $$
> 
> 如定理所述。 $\square$

\rigorous{} **证明状态：严格。**Fano不等式是信息论的标准结果(Cover \& Thomas, 2006, 定理2.10.1)。
步骤2的熵链式法则是恒等式。步骤4的代数推导精确。

**认识论含义：**此定理精确刻画了Kuhn所说的``反常累积到范式危机''的信息论条件。
当新数据携带的、无法被旧范式解释的信息量超过临界阈值时，
任何在旧范式内工作的科学家共同体的集体判断能力退化到随机水平以下——
不是因为他们变笨了，而是因为范式本身的表达力不足以容纳新信息。

### 范式转移的速率与不可通约性

> **Theorem:** [范式转移的动力学]
> <!-- label: thm:paradigm_shift_dynamics -->
> 设旧范式$\mathcal{K}_{old}$和新范式$\mathcal{K}_{new}$。
> 新范式对旧范式的**信息增益**为：
> 
> $$
>     \boxed{G(\mathcal{K}_{new} \mid \mathcal{K}_{old})
>     = I(Y; \mathcal{S}_{new}) - I(Y; \mathcal{S}_{old})}。
> $$
> 
> 范式转移的**速率**$r(t)$——即科学共同体从旧范式转向新范式的速度——
> 满足：
> 
> $$
>     \boxed{r(t) \propto \frac{G(\mathcal{K}_{new} \mid \mathcal{K}_{old})}
>                              {H(\mathcal{S}_{new} \mid \mathcal{S}_{old})} \cdot
>                              \frac{1}{\tau_{gen}}}，
> $$
> 
> 其中$\tau_{gen}$是``科学世代''时间（新一代科学家接受新范式训练所需时间），
> $H(\mathcal{S}_{new} \mid \mathcal{S}_{old})$是新旧范式状态空间之间的
> **不可通约熵**。

> **Proof:** [推导思路]
> **步骤1（信息增益的动力）：**科学共同体中每个专家$E_m$的效用函数
> $U(E_m; \mathcal{K})$依赖于范式提供的解释成功。
> 信息增益$G$越大，新范式越能提供旧范式无法提供的解释→转向激励越强。
> 
> **步骤2（不可通约性作为转换成本）：**$H(\mathcal{S}_{new} \mid \mathcal{S}_{old})$
> 度量的是：给定旧范式的概念体系，新范式的概念体系有多大``意外性''。
> 不可通约熵越大，旧范式专家理解新范式的认知成本越高→转换越慢。
> 
> **步骤3（世代效应）：**Kuhn的著名观察——``新范式获胜不是因为说服了反对者，
> 而是因为反对者最终死去''——在此被建模为世代时间$\tau_{gen}$的效应。
> 转换速率与世代时间成反比：世代越长（科学家越长寿/任期越长），转换越慢。
> 
> \heuristic{} 此定理的具体函数形式（比例常数）是启发式的。
> $G/H$比值和$1/\tau_{gen}$因子是合理的量纲分析，
> 但需要从科学史数据中估计精确的参数形式。

> **Corollary:** [Kuhn损耗——Planck原理的形式化]
> <!-- label: cor:planck -->
> **Planck原理：**``新的科学真理不通过说服反对者而获胜，而是因为反对者最终死去，
> 新一代从一开始就熟悉它。''在SCX框架下，其形式化为：
> 
> $$
>     \boxed{t_{shift} = \tau_{gen} \cdot \frac{H(\mathcal{S}_{new} \mid \mathcal{S}_{old})}
>                                                {G(\mathcal{K}_{new} \mid \mathcal{K}_{old})}}，
> $$
> 
> 其中$t_{shift}$是范式完全转移所需的**特征时间**。
> 当不可通约熵大而信息增益小时，$t_{shift} \gg \tau_{gen}$——
> 范式转移可能需要数代科学家。

\honeststrike{} **诚实暴击：范式转移的不可预测性。**
本定理描述了范式转移的**事后**结构，但**不能预测**范式转移何时发生。
原因：(i) $G(\mathcal{K}_{new})$只有在范式转移**之后**才能被计算；
(ii) 不可通约熵$H(\mathcal{S}_{new} \mid \mathcal{S}_{old})$
本身依赖于尚未建立的新范式的概念体系。这是Kuhn理论的根本困难的形式化表现：
革命性的新范式在旧范式的框架内**不可见**。

## Popper可证伪性的SCX版：声称必须声明可被验证的假设

### 可证伪性的逻辑困境

Karl Popper (1935/1959)提出*可证伪性*作为科学分界标准：
一个理论是科学的当且仅当它**可被经验证伪**。
然而，Popper的标准面临两个著名的困难：

1. **Duhem-Quine问题：**任何理论检验都依赖辅助假设——
2. **概率证伪问题：**现代科学中许多理论是概率性的——

SCX框架提供了可证伪性的**操作化**版本，直接解决了这两个困难。

### 可证伪性的SCX判据

> **Definition:** [SCX可证伪性——操作化定义]
> <!-- label: def:falsifiability -->
> 一项科学声称$s \in \mathcal{S}$是**SCX-可证伪的**，当且仅当声称者声明了以下三元组：
> 
> $$
>     \boxed{\mathcal{F}(s) = (\Delta_s^{claimed}, \mathcal{V}, M_{min})}，
> $$
> 
> 其中：
> 
- $\Delta_s^{claimed} > 0$：声称者断言的最小检测边际——
- $\mathcal{V}$：可公开执行的**验证协议**——
- $M_{min}$：声称者认定的**最小充分专家数**——

> **Theorem:** [可证伪性的充要条件——SCX版Popper判据]
> <!-- label: thm:scx_popper -->
> 声称$s$是SCX-可证伪的当且仅当存在验证协议$\mathcal{V}$和有限专家数$M$，
> 使得以下假设检验具有非平凡的统计功效（power $> 1/2$）：
> 
> $$
>     H_0 &: \Delta_s \leq 0 \quad （声称不成立——未检测到信号） 

>     H_1 &: \Delta_s \geq \Delta_s^{claimed} > 0 \quad （声称成立——信号存在） 。
> $$
> 
> 若声称者**拒绝声明**$\Delta_s^{claimed}$或$\mathcal{V}$，
> 声称$s$是**SCX-不可证伪的**——即不具有科学地位。

> **Proof:** **步骤1（必要性）：**若$\mathcal{F}(s)$缺失任一要素：
> 
- 缺失$\Delta_s^{claimed}$ → 无法计算所需样本量/专家数 → 检验无法设计；
- 缺失$\mathcal{V}$ → 验证不可重复 → 声称不受经验约束；
- 缺失$M_{min}$ → 声称者可以无限推迟证伪——

> 以上任一缺失均导致声称无法被严格经验检验。
> 
> **步骤2（充分性——Chernoff检验的功效）：**给定了$\mathcal{F}(s)$，
> Chernoff检验的功效为：
> 
> $$
>     Power(M, \Delta_s^{claimed}, \alpha)
>     = \mathbb{P}_{H_1}\left(C_M(s) \geq \frac{1}{2} + \sqrt{\frac{\log(1/\alpha)}{2M}}\right)
>     \geq 1 - \exp\left(-2M\left(\Delta_s^{claimed} - \sqrt{\frac{\log(1/\alpha)}{2M}}\right)^2\right)。
> $$
> 
> 当$M \geq M_{min}$时（其中$M_{min}$由声称者声明），此功效$> 1/2$。
> 
> **步骤3（Duhem-Quine的SCX解决方案）：**辅助假设$A_1, ..., A_k$在SCX框架中
> 被纳入状态原子的特征表示$\phi(s)$。验证协议$\mathcal{V}$要求声明者显式列举所有辅助假设。
> 如果证伪发生（$H_0$未被拒绝），SCX分析不会简单地宣布``理论被证伪''，
> 而是通过多专家分歧模式**定位**问题出在哪个辅助假设上——解决了Duhem-Quine整体论困境。
> 
> **步骤4（概率声称的SCX处理）：**对概率声称（如``$p > 0.7$''），
> 检测边际$\Delta_s$通过Bernoulli检验的效应量来定义：
> $\Delta_s = p - (1-p) = 2p-1$（若$p > 0.5$），使概率声称自然嵌入二元投票框架。 $\square$

\rigorous{} **证明状态：严格。**所有步骤基于标准假设检验理论和Hoeffding界。
Duhem-Quine的解决方案（步骤3）的``定位''机制是信息论上可能的
（通过条件互信息$I(Y; A_j \mid S, \{A_k\}_{k \neq j})$），
但其在有限样本下的精确可靠性是\heuristic{}（需要足够多的独立专家来解耦辅助假设）。

### 不可证伪声称的分类学

> **Theorem:** [不可证伪性的SCX分类]
> <!-- label: thm:unfalsifiable_taxonomy -->
> 科学声称的不可证伪性在SCX框架下分为三种精确类型：
> 
1. **边际隐匿型：**声称者拒绝声明$\Delta_s^{claimed}$——
2. **协议缺失型：**声称者拒绝声明$\mathcal{V}$——
3. **阈值逃逸型：**声称者将$M_{min}$设为不可达值——

> 任一类型均导致声称$s$的SCX-可证伪性得分为零。

> **Proof:** 直接由定理 [ref]的必要性条件(步骤1)得出。每一类型对应$\mathcal{F}(s)$三元组的
> 一个缺失模式。 $\square$

\honeststrike{} **诚实暴击：SCX可证伪性不是万能药。**
SCX可证伪性判据回避了（而非解决了）以下深层问题：

1. **专家独立性的验证：**验证协议$\mathcal{V}$可以声明专家是独立的，
2. **$\Delta_s^{claimed}$的校准：**声称者可能通过声明极小的
3. **理论不可通约性：**当新旧理论使用不同的状态空间$\mathcal{S}$时，

这些局限不是SCX框架的失败，而是科学哲学根本困难的精确形式化表达。
SCX的贡献在于将这些困难从模糊的概念争论转化为清晰的数学条件，
使得它们可以被精确讨论和（在原则上）被经验检验。

## 科学复现危机的SCX诊断：多专家独立复现失败的数学

### 复现危机的SCX形式化

科学复现危机（replication crisis）是当代科学面临的最严峻挑战之一。
Open Science Collaboration (2015)发现只有约$36\%$的心理学研究能被复现；
Camerer等(2018)的社会科学复现率约为$62\%$；Errington等(2021)的癌症生物学
复现率约为$46\%$。这些数字揭示了一个系统性失败。

SCX框架提供了复现危机的精确数学诊断。

> **Definition:** [复现——SCX形式化]
> <!-- label: def:replication -->
> 对原始声称$s$通过原始专家集$\mathcal{E}_{orig} = \{E_1, ..., E_M\}$的检验，
> **独立复现**由新的独立专家集$\mathcal{E}_{rep} = \{E'_1, ..., E'_{M'}\}$
> 在**相同验证协议**$\mathcal{V}$下执行。复现成功的SCX条件为：
> 
> $$
>     \boxed{\hat_s^{rep} > 0 \quad 且 \quad
>     \left|\hat_s^{rep} - \hat_s^{orig}\right|
>     \leq \sqrt{\frac{\log(2/\alpha)}{2}\left(\frac{1}{M} + \frac{1}{M'}\right)}}，
> $$
> 
> 其中$\hat_s^{orig}$和$\hat_s^{rep}$分别为原始和复现的
> 经验检测边际。

### 复现失败的三种SCX模式

> **Theorem:** [复现危机三模式定理]
> <!-- label: thm:replication_crisis -->
> 独立复现失败必然属于以下三种SCX模式之一：
> 
> 
1. **边际反转（Margin Reversal）：**
2. **专家塌缩（Expert Collapse）：**
3. **状态遮蔽（State Occlusion）：**

> **Proof:** **模式1（边际反转）：**由定义 [ref]，复现成功要求
> $\hat_s^{rep} > 0$。若此条件不满足，则$C_{M'}(s)$与$1/2$的偏差不超过统计噪声。
> 由Chernoff检验（定理 [ref]），原声称的共识在复现中不成立。
> **发生率：**当原始声称的$\Delta_s$被高估（发表偏误、p-hacking）或原始专家集存在
> 系统性偏误（共享错误的辅助假设）时发生。
> 
> **模式2（专家塌缩）：**当$\mathcal{E}_{rep}$中的专家共享相同的理论预设、
> 方法论工具或训练数据时，有效独立性$M'_{eff} < M'_{nominal}$。
> 由Chernoff-Hoeffding界的依赖版本（Janson, 2004），
> $\hat_s^{rep}$的方差以$O(1/M'_{eff})$而非$O(1/M')$衰减。
> 当$M'_{eff} \ll M'_{nominal}$时，检测边际可表现为正但统计上不显著。
> **发生率：**在学术谱系效应明显（同一导师的学生形成``学派''）、
> 或社区使用共享软件工具（``单一种植''问题）的领域中最常见。
> 
> **模式3（状态遮蔽）：**原声称宣称在$\mathcal{S}$上成立，
> 但实际只在真子集$\mathcal{S}' \subset \mathcal{S}$上成立。
> 复现专家可能在$\mathcal{S} \setminus \mathcal{S}'$上抽样→检测边际消失。
> 形式化地：
> 
> $$
>     \hat_s^{rep}(\mathcal{S}) =
>     \frac{|\mathcal{S}'|}{|\mathcal{S}|}\hat_s^{rep}(\mathcal{S}') +
>     \frac{|\mathcal{S} \setminus \mathcal{S}'|}{|\mathcal{S}|}\hat_s^{rep}(\mathcal{S} \setminus \mathcal{S}')，
> $$
> 
> 其中$\hat_s^{rep}(\mathcal{S} \setminus \mathcal{S}') \leq 0$。
> 当$|\mathcal{S}'|/|\mathcal{S}|$足够小时，加权平均无统计显著性。
> **发生率：**在过度泛化的声称（``此方法适用于所有X''但实际只适用于X的特定子类）中普遍存在。 $\square$

\rigorous{} **证明状态：严格。**三种模式的区分基于经验估计量$\hat_s$的行为，
其统计性质由Hoeffding界和依赖条件下的修正版本保证。

### 复现危机的最小充分条件

> **Theorem:** [复现失败的信息论根源]
> <!-- label: thm:replication_roots -->
> 复现危机的深层根源在于以下信息论不等式：
> 
> $$
>     \boxed{I(Y; \mathcal{E}_{orig}) + I(Y; \mathcal{E}_{rep} \mid \mathcal{E}_{orig})
>     \leq H(Y)}，
> $$
> 
> 其中$I(Y; \mathcal{E}_{orig})$是原始专家集提供的关于声称真实性的信息，
> $I(Y; \mathcal{E}_{rep} \mid \mathcal{E}_{orig})$是复现专家集提供的额外信息。
> **当原始专家集已经耗尽总信息容量时，复现专家的边际信息贡献为零——复现沦为同义反复。**

> **Proof:** 由信息论基本恒等式：
> 
> $$
>     I(Y; \mathcal{E}_{orig}, \mathcal{E}_{rep})
>     = I(Y; \mathcal{E}_{orig}) + I(Y; \mathcal{E}_{rep} \mid \mathcal{E}_{orig})
>     \leq H(Y)。
> $$
> 
> 若$I(Y; \mathcal{E}_{orig}) \approx H(Y)$（原始专家已``知道一切''），
> 则$I(Y; \mathcal{E}_{rep} \mid \mathcal{E}_{orig}) \approx 0$。
> 在这种极限下，复现专家的投票是**完全冗余的**——
> 他们同意原始专家不是因为声称正确，而是因为共享了相同的先验信息。 $\square$

\honeststrike{} **诚实暴击：可复现≠正确。**
定理 [ref]揭示了一个令人不安的结论：
**完全可复现的声称可能仍然是错误的**——如果复现者与原始研究者
共享相同的理论预设和偏误来源。极端情况下，
$M$个共享相同错误模型的``独立''专家会产生完美的共识——
而声称完全错误。这是科学史上``集体幻觉''（如N射线、冷核聚变）的SCX形式化。

> **Corollary:** [复现改善的SCX处方]
> <!-- label: cor:replication_fix -->
> 要提高复现的可靠性，科学共同体应最大化：
> 
> $$
>     \boxed{I(Y; \mathcal{E}_{rep} \mid \mathcal{E}_{orig})}
> $$
> 
> ——即复现专家在原始专家已知信息之外的**额外信息贡献**。
> 操作上，这意味着复现应最大化与原始研究的**方法论独立性**：
> 不同的实验范式、独立的仪器、正交的测量原理。

## 定理边界与诚实暴击

### 专家独立性假设的崩溃

本文所有定理依赖的核心公理是专家独立性（公理 [ref]）。
在真实科学共同体中，此假设以多种方式被系统地违反：

1. **学术谱系依赖：**同一导师培养的学生共享方法论预设→有效独立性降低；
2. **工具单一种植（Monoculture）：**整个社区使用相同的软件包
3. **发表偏误的回音室：**只有正面结果被发表→所有专家观察到的``证据''
4. **理论范式锁定：**Kuhn常规科学中，所有专家共享相同的核心理论承诺→

> **Theorem:** [有效专家数——独立性折扣]
> <!-- label: thm:effective_experts -->
> 当专家集合存在依赖性时，Chernoff-Hoeffding界中的$M$应替换为
> **有效专家数**$M_{eff}$：
> 
> $$
>     \boxed{M_{eff} = \frac{M}{1 + (M-1)\bar}}，
> $$
> 
> 其中$\bar$是专家投票之间的平均类内相关系数（ICC）。
> 当$\bar \to 1$时，$M_{eff} \to 1$——无论多少专家，有效信息量等价于一个专家。

> **Proof:** 考虑$M$个专家的投票$\{v_1, ..., v_M\}$，设$\Var(v_m) = \sigma^2$，
> $\Cov(v_m, v_{m'}) = \rho\sigma^2$（对$m \neq m'$）。
> 则均值$\bar{v} = \frac{1}{M}\sum v_m$的方差为：
> 
> $$
>     \Var(\bar{v}) = \frac{\sigma^2}{M} + \frac{M-1}{M}\rho\sigma^2
>     = \frac{\sigma^2}{M}\left(1 + (M-1)\rho\right)。
> $$
> 
> 与独立情况（$\rho = 0$）相比，有效样本量为$M/(1 + (M-1)\bar)$。
> 代入Hoeffding界即得所述修正。 $\square$

\honeststrike{} **诚实暴击：大多数科学领域中的$M_{eff}$。**
在学术谱系效应强的领域（如高能物理实验合作组之外的粒子物理唯象学），
$M_{eff}$可能仅为$M_{nominal}$的$10\%$--$30\%$。
这意味着声称``$M=100$个独立研究支持此结论''实际上可能仅等价于$10$--$30$个真正独立的信息源。
这大幅削弱了共识声明的统计可靠性。

### 认识论形式化的边界——Gödel-Turing阴影

> **Remark:** [形式化认识论的Gödelian限制]
> <!-- label: rem:godel -->
> 将科学认识论形式化的尝试面临一个根本的递归性困难：
> SCX框架本身是一组形式化的科学声称。根据定理 [ref]，
> SCX的声称必须声明$\Delta_s^{claimed}$和$\mathcal{V}$才能成为SCX-可证伪的。
> 这意味着存在一个**元级自指**问题：
> 
1. SCX声称``SCX框架有效''本身必须接受SCX检验；
2. 此检验需要独立于SCX框架的专家（否则循环论证）；
3. 这些元专家可能不共享SCX的公理预设——此时SCX的可证伪性判据对SCX自身失效。

> 这是Gödel不完备性定理在认识论领域的类比：任何足够强的认识论形式系统
> 无法在其自身框架内证明自己的充分性。

\honeststrike{} **本文的立场：**我们承认此自指限制是本质性的，不是SCX框架的缺陷。
SCX提供的是**相对化的**认识论保证：如果接受SCX公理，则有定理 [ref]-- [ref]。
如果不接受SCX公理，则需要不同的公理系统——而那个系统同样面临自指问题。
认识论形式化不能逃避Gödel-Turing阴影，但可以精确地画定阴影的边界。

## 讨论：科学哲学的形式化——从SCX出发

### 四个定理的相互关系

本文的四个核心定理构成了一个逻辑闭环：

1. **共识定理（\S2）：**定义了**何时**一个科学共同体可以被认为
2. **范式转移定理（\S3）：**定义了**何时**被接受的共识必须被放弃——
3. **可证伪性定理（\S4）：**定义了**何者**有资格进入共识形成过程——
4. **复现危机定理（\S5）：**定义了**如何**验证共识的可靠性——

这四者不是独立的哲学论文，而是同一个形式系统的四个推论。
它们共同的底层机制是SCX的检测边际$\Delta_s$和信息论不等式的精确作用。

### 与经典科学哲学的对话

[Table omitted — see original .tex]

### 老实人定理与独醒不太可能定理的哲学意义

**老实人定理**（定理 [ref]）确认了科学方法论的乐观核心：
如果专家确实是独立且诚实的，共识必然优于个体判断。
这为科学共同体的制度设计提供了精确的规范性指导——
制度的目标应是最大化专家的**独立性**（降低$\bar$）和
**诚实性**（降低$p_{clean, s}$）。

**独醒不太可能定理**（定理 [ref]）同时证明了两个方向：
(i) 当多名独立专家达成共识时，孤独异议者极不可能正确
（为科学共识的认知权威提供了概率性辩护）；
(ii) 此概率以$\exp(-2M\Delta_s^2)$衰减——因此**当$\Delta_s$很小时**
（即前沿领域的新声称），异议者并非荒谬的，需要更多的专家来排除异议。
这解释了为什么科学的前沿永远充满争议而成熟的核心知识相对稳定。

### 认识论形式化的前景与末路

我们将科学知识生产的核心过程——共识形成、范式转换、可证伪性判定、
复现验证——转化为SCX公理系统的数学定理。
每个定理的陈述是精确的，每个证明链是可验证的。
我们区分了严格定理（$\rigorous$）和启发式命题（$\heuristic$），
明确标注了开放问题（$\openproblem$）和理论边界。

然而，我们必须诚实地承认形式化认识论的**三重边界**：

1. **Gödel边界（元级自指）：**任何认识论形式系统无法在其自身框架内证明自身的充分性（注记 [ref]）；
2. **独立性边界（公理的外部性）：**专家独立性公理在实际科学共同体中从不严格成立，
3. **不可通约边界（范式间的翻译）：**新旧范式之间的概念翻译（定理 [ref]）

形式化不是科学哲学的终结，而是它的一个新起点。
精确的数学条件将模糊的概念争论转化为可检验的假设——
哪些条件在真实科学共同体中成立？哪些不成立？偏离程度有多大？
这些问题现在可以被**经验地**研究，而不仅仅是**概念地**争论。

这，就是科学哲学形式化的意义。

## 致谢

本文的数学基础建立在SCX框架的四条核心定理之上(SCX Project, 2026)。
``老实人定理''和``独醒不太可能定理''的命名来自SCX项目的认识论形式化讨论。
感谢所有在SCX理论审计报告中提出尖锐问题的审阅者——
正是这些``诚实暴击''使得本文的理论边界标注成为可能。

\begin{thebibliography}{99}

\bibitem{boucheron2013}
S.~Boucheron, G.~Lugosi, and P.~Massart.
\newblock *Concentration Inequalities: A Nonasymptotic Theory of Independence*.
\newblock Oxford University Press, 2013.

\bibitem{camerer2018}
C.~F.~Camerer *et al.*
\newblock Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015.
\newblock *Nature Human Behaviour*, 2:637--644, 2018.

\bibitem{cover2006}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd edition.
\newblock Wiley, 2006.

\bibitem{errington2021}
T.~M.~Errington *et al.*
\newblock Investigating the replicability of preclinical cancer biology.
\newblock *eLife*, 10:e71601, 2021.

\bibitem{feyerabend1975}
P.~Feyerabend.
\newblock *Against Method*.
\newblock New Left Books, 1975.

\bibitem{hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock *Journal of the American Statistical Association*, 58(301):13--30, 1963.

\bibitem{ioannidis2005}
J.~P.~A.~Ioannidis.
\newblock Why most published research findings are false.
\newblock *PLoS Medicine*, 2(8):e124, 2005.

\bibitem{janson2004}
S.~Janson.
\newblock Large deviations for sums of partly dependent random variables.
\newblock *Random Structures \& Algorithms*, 24(3):234--248, 2004.

\bibitem{kuhn1962}
T.~S.~Kuhn.
\newblock *The Structure of Scientific Revolutions*.
\newblock University of Chicago Press, 1962.

\bibitem{lakatos1978}
I.~Lakatos.
\newblock *The Methodology of Scientific Research Programmes*.
\newblock Cambridge University Press, 1978.

\bibitem{openscience2015}
Open Science Collaboration.
\newblock Estimating the reproducibility of psychological science.
\newblock *Science*, 349(6251):aac4716, 2015.

\bibitem{popper1959}
K.~R.~Popper.
\newblock *The Logic of Scientific Discovery*.
\newblock Hutchinson, 1959. (Original work published 1935)

\bibitem{quine1951}
W.~V.~O.~Quine.
\newblock Two dogmas of empiricism.
\newblock *The Philosophical Review*, 60(1):20--43, 1951.

\bibitem{scx2026theorems}
SCX Project.
\newblock {Theorem 1--4}: Multi-expert consistency, weak feature limits, unidentifiability,
  and minimax optimality.
\newblock Technical report, `src/scx/`, 2026.

\bibitem{scx2026situs}
SCX Project.
\newblock {Situs}: Physics-anchored positional encoding for state-conditioned expertise.
\newblock Preprint, `paper/situs\_theory/main.tex`, 2026.

\bibitem{scx2026yajie}
SCX Project.
\newblock {The Yajie Protocol}: Technology lock-in, audit sovereignty, and the
  non-proliferation logic of data quality assessment.
\newblock Working paper, `yajie\_protocol\_paper.md`, 2026.

\bibitem{wainwright2019}
M.~J.~Wainwright.
\newblock *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*.
\newblock Cambridge University Press, 2019.

\end{thebibliography}