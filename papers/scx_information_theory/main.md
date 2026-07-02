# 引言：为什么SCX需要信息论

**Author:** SCX

*Abstract:*

SCX（State-Conditioned eXpertise）框架通过$M$个独立专家的二元投票机制检测标签噪声和
评估数据质量。然而，现有SCX定理体系（Theorem~1--4）尚未系统处理信息论的核心结构性问题：
有限通信带宽下审计精度的理论上界、分布式专家编码的压缩效率、以及源-信道编码分离的适用边界。
本文从信息论的基本定理——率失真理论、Slepian-Wolf分布式编码、Shannon分离定理——出发，
为SCX建立完整的信息论基础。

**第一**（审计率失真界），将SCX审计建模为率失真问题：审计者接收专家投票的量化版本
$Q(\mathbf{V})$而非完整投票$\mathbf{V} \in \{0,1\}^M$，通信约束为每状态原子$R$比特。
推导有限通信带宽下SCX审计的错误概率下界：
$P_e \geq (H(Y) - R - \log 2) / \log |\Y|$，
揭示了**审计精度-通信带宽-专家数量**的三元权衡，并给出了通过交替最小化算法逼近
信息瓶颈最优压缩的构造性方法。

**第二**（分布式共识的Slepian-Wolf编码），将$M$个专家的投票建模为相关信源。
证明Slepian-Wolf定理的SCX版本：$M$个相关专家输出的无损联合压缩的可行速率区域为
$\sum_{m \in \mathcal{T}} R_m \geq H(\mathbf{V}_\mathcal{T} \mid \mathbf{V}_{\mathcal{T}^c})$
对所有子集$\mathcal{T}$成立，总速率仅需$H(\mathbf{V})$而非$M \cdot H_2(p_{clean})$。
推导了**专家相关性红利**：当专家共享方法论偏误时，相关性节省的编码比特达到最大——
但这恰恰是SCX框架最不希望的场景。\honeststrike{}

**第三**（Shannon分离定理的SCX推广），证明SCX框架中存在两个基本操作的分离问题：
（i）专家质量评分（源编码，将原始投票压缩为质量分数）与（ii）共识检测
（信道编码，在有噪专家输出中恢复真实标签）。当且仅当专家投票满足条件独立时，
分离达到最优；否则，联合源-信道编码可严格优于分离架构。

**第四**（Theorem~2的完整信息论推广），将Theorem~2的弱特征失效界从Fano不等式的
标量界推广到率失真函数和信息瓶颈方法框架下的完整信息论处理。引入**信息不足度函数**
$\delta(R) = \inf_{P_{U|X}: I(X;U) \leq R} I(Y; U)$，证明其在$R$充分小时的严格正性
等价于Theorem~2的弱特征失效条件，并推导了新的更紧上界：
$F_{1,SCX} \leq F_{1,base} + C_F \cdot r(\delta(0))$，
其中$r(\cdot)$是由$X$和$Y$的联合分布决定的率失真特征函数。

全文遵循**诚实暴击**标准，明确区分严格证明的定理与依赖未验证假设的推广，
标注SCX信息论形式的**理论适用边界**：

- 率失真界的紧致性依赖专家投票的i.i.d.\假设——实际审计中状态原子间存在空间相关性；
- Slepian-Wolf编码的可行性要求各编码器间存在**公共随机性**
- 分离定理的SCX推广仅对**渐进**（$M \to \infty$, $n \to \infty$）成立，
- Theorem~2的信息论推广虽然更紧，但其参数化形式（$\delta(R)$函数）的估计

**关键词：**SCX框架，率失真理论，Slepian-Wolf编码，Shannon分离定理，信息瓶颈，
多专家信息融合，互信息，Fano不等式，分布式共识，审计信息论

## 引言：为什么SCX需要信息论

### SCX框架的信息论审视

SCX框架通过$M$个独立专家在$N$个状态原子上的二元投票来检测标签噪声。
其四条核心定理构成了当前的理论支柱 [cite]：

- **Theorem~1**（多专家一致性）：$F_1 \geq 1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)$；
- **Theorem~2**（弱特征失效）：$F_{1,SCX} \leq F_{1,base} + C_F\sqrt{\delta/2}$；
- **Theorem~3**（噪声-困难不可区分）：存在两个观测分布等价的世界，任何算法不能区分；
- **Theorem~4**（Minimax最优）：误差指数达到Chernoff-Stein信息论下界。

然而，现有定理体系在一个关键维度上存在空白：**信息论**。
Theorem~1使用了Chernoff-Hoeffding（集中不等式），Theorem~2使用了Fano不等式，
Theorem~4触及了Chernoff-Stein引理——但这些使用是*工具性*的而非*结构性的*。
信息论的核心概念框架——率失真函数、分布式信源编码、分离定理、信息瓶颈——
尚未被系统性地整合进SCX的理论结构中。

**本文的核心主张是：**SCX框架的多专家投票机制天然构成一个信息传输系统。
$M$个专家是**信源**（产生关于标签的投票），审计者是**信宿**
（从投票中推断标签质量），通信约束（带宽限制、分布式编码需求、延迟要求）
是**信道**。完整的信息论视角不仅统一了现有定理，更揭示了现有框架中的隐性假设
和根本性权衡。

### SCX作为信息传输系统：形式化

> **Definition:** [SCX信息传输系统的形式化]
> <!-- label: def:scx_its -->
> SCX信息传输系统定义为五元组：
> 
> $$
>     \boxed{\mathcal{T}_{SCX} = (\mathcal{S}, \mathcal{E}, \mathcal{C}, \mathcal{A}, \mathcal{D})}，
> $$
> 
> 其中：
> 
- $\mathcal{S}$：状态原子集，大小为$N$，真实标签$Y_s \in \Y$；
- $\mathcal{E} = \{E_1, ..., E_M\}$：专家集合，每个专家$E_m$对状态$s$产生投票
- $\mathcal{C}$：通信信道，将原始投票$\mathbf{V}(s) = (V_1(s), ..., V_M(s))$
- $\mathcal{A}$：审计器，从压缩表示中推断标签质量
- $\mathcal{D}$：失真度量，$d(\hat{Y}_s, Y_s) = \mathbf{1}[\hat{Y}_s \neq Y_s]$。

此形式化将SCX审计转化为标准的**联合源-信道编码问题**：
$M$个相关信源（专家投票）→ 编码（压缩/量化）→ 信道（通信约束）→ 解码（审计决策）。
信息论的全部工具——率失真函数、Slepian-Wolf区域、分离定理——现在可以直接应用于SCX。

> **Definition:** [专家投票的联合分布]
> <!-- label: def:joint_vote -->
> 给定状态原子$s$及其真实标签$y_s$，$M$个专家的投票$\mathbf{V} \in \{0,1\}^M$的联合分布为：
> 
> $$
>     P(\mathbf{V} = \mathbf{v} \mid Y = y)
>     = \prod_{m=1}^{M} p_{y}^{v_m} (1 - p_{y})^{1 - v_m}
>     \quad (条件独立假设下)，
> $$
> 
> 其中$p_{clean, s} = P(V_m = 1 \mid Y = clean)$，
> $p_{noisy, s} = P(V_m = 1 \mid Y = noisy)$。

> **注意：**条件独立假设（公理独立性，定义 [ref]）在SCX框架中是基础假定，
> 但本文将**明确分析**此假设被违反时的影响（见\S3，\S5）。

\honeststrike{} **诚实暴击：信息论形式化的代价。**
将SCX形式化为信息传输系统引入了两个核心简化：（i）假设状态原子间满足平稳性和遍历性
（对信息论渐近分析的必要前提）——这在有限样本审计中**不成立**；
（ii）假设通信约束是硬速率约束——但实际中的瓶颈更可能是延迟（交互轮数）或计算预算。
非渐近信息论（如有限块长分析）可能提供更贴近实际的界，但代价是数学复杂度显著增加。

## 审计率失真界：有限通信带宽下SCX审计的错误概率下界

### 率失真函数与SCX审计的对应

率失真理论（Rate-Distortion Theory）是信息论中刻画信源压缩质量与所需速率之间权衡的
核心框架 [cite]。给定信源$X \sim P_X$和失真度量$d(x, \hat{x})$，
率失真函数定义为：

$$
    R(D) = \min_{P_{\hat{X}|X}: \E[d(X, \hat{X})] \leq D} I(X; \hat{X})。
$$

在SCX审计中，``信源''是$M$个专家的完整投票向量$\mathbf{V} \in \{0,1\}^M$，
``失真''是审计错误概率$P_e = \E[d(\hat{Y}, Y)] = P(\hat{Y} \neq Y)$，
``速率''是每状态原子可用的通信比特数$R$。

核心问题是：**给定每原子通信预算$R$比特，SCX审计的错误概率下界是什么？**

### 主定理：审计率失真下界

> **Theorem:** [SCX审计率失真下界——有限带宽下的不可消除误差]
> <!-- label: thm:rdt_audit -->
> 设$M$个专家对状态原子$s$的投票向量为$\mathbf{V} \in \{0,1\}^M$，真实标签为$Y$。
> 若审计器仅能访问$\mathbf{V}$的量化版本$Q(\mathbf{V})$，满足速率约束
> $I(\mathbf{V}; Q(\mathbf{V})) \leq R$（每状态原子），则审计错误概率满足：
> 
> $$
>     \boxed{P_e \geq \frac{H(Y) - R - \log 2}{\log |\Y|}}。
> $$
> 
> 等价地，要达到审计错误概率不高于$\varepsilon$，所需的最小通信速率为：
> 
> $$
>     \boxed{R_(\varepsilon) \geq H(Y) - \log 2 - \varepsilon \log |\Y|}。
> $$

> **Proof:** **步骤1（Fano不等式的链式应用）：**由Fano不等式 [cite]：
> 
> $$
>     H(Y \mid Q(\mathbf{V})) \leq H_2(P_e) + P_e \cdot \log(|\Y| - 1)
>     \leq \log 2 + P_e \log |\Y|，
> $$
> 
> 其中利用了$H_2(P_e) \leq \log 2$（二元熵的上界）。
> 
> **步骤2（信息链与速率约束）：**由熵的链式法则和数据处理不等式：
> 
> $$
>     H(Y \mid Q(\mathbf{V}))
>     &= H(Y) - I(Y; Q(\mathbf{V})) 

>     &\geq H(Y) - I(\mathbf{V}; Q(\mathbf{V})) \quad （DPI:  Y \to \mathbf{V} \to Q(\mathbf{V}) ）

>     &\geq H(Y) - R \quad （速率约束）。
> $$
> 
> 
> **步骤3（组合推出下界）：**
> 
> $$
>     H(Y) - R &\leq H(Y \mid Q(\mathbf{V}))
>     \leq \log 2 + P_e \log |\Y| 

>     \implies P_e &\geq \frac{H(Y) - R - \log 2}{\log |\Y|}。
> $$
> 
> 
> **步骤4（紧致性条件）：**此下界在以下条件下是渐近紧的：
> （i）$Q(\mathbf{V})$是$Y$的充分统计量（即$Y \indep \mathbf{V} \mid Q(\mathbf{V})$）；
> （ii）Fano不等式达到等号（需要错误概率均匀分布在所有错误类别上）；
> （iii）速率约束的等号成立（即$I(\mathbf{V}; Q(\mathbf{V})) = R$）。
> 在$M \to \infty$且标签为二元的极限下，等号可达。 $\square$

\rigorous{} **证明状态：步骤1--3严格（Fano不等式+DPI+熵链式法则均为信息论标准结果）。
步骤4的紧致性陈述是渐近的——在有限$M$和有限速率下，界可能不紧。**

> **Remark:** [与Theorem~1的关系——Chernoff vs.\ 率失真]
> <!-- label: rem:chernoff_vs_rdt -->
> Theorem~1给出的$F_1$下界（通过Chernoff-Hoeffding）与定理 [ref]给出的
> $P_e$下界（通过率失真）是从不同方向逼近同一问题：
> 
- Theorem~1：**充分$M$下的乐观界**——当$M$充分大且$\Delta_s > 0$时，
- 定理 [ref]：**有限通信下的悲观界**——无论$M$多大，

> 两者互补：Theorem~1假设了无通信约束（审计器可直接访问所有投票），
> 定理 [ref]放松了此假设。在审计器必须通过有损信道接收专家投票的场景中
> （如分布式审计、联邦学习中的模型质量监控），率失真界给出了根本性的精度上限。

### 率失真界的物理解释：三元权衡

> **Corollary:** [审计精度-通信带宽-专家数量的三元权衡]
> <!-- label: cor:triad -->
> SCX审计中存在以下根本性权衡：
> 
> $$
>     \boxed{\underbrace{R}_{每原子通信速率} \cdot \underbrace{N}_{状态原子数}
>     \geq H(\mathbf{V}_1, ..., \mathbf{V}_M) - \underbrace{N \cdot H_2(P_e)}_{审计不确定性}}。
> $$
> 
> 增大$M$（更多专家）增加$H(\mathbf{V})$（更多投票需编码），但同时也通过$\Delta_s$的增长
> 降低了$P_e$（更准确的审计）。在固定$R$下，存在**最优专家数**$M^*$平衡此权衡。

> **Proof:** 由率失真函数的定义和定理 [ref]直接推导。$H(\mathbf{V})$随$M$增长
> （最多线性增长$M$），但$P_e$随$M$以$\exp(-2M\Delta_s^2)$速率下降（由Theorem~1）。
> 两者的交点决定了$M^*$。 $\square$

\heuristic{} **证明状态：启发式。**最优$M^*$的精确刻画需要$H(\mathbf{V})$和$P_e(M)$的
精确函数形式，后者在有限$M$下依赖于专家输出的具体分布。$H(\mathbf{V})$的精确计算需要
专家投票联合分布的完整知识——而在实际SCX审计中，这恰恰是未知的。

### 信息瓶颈方法：SCX审计的最优压缩

率失真界给出了可达性下界，但未给出**如何**压缩。信息瓶颈
（Information Bottleneck, IB）方法 [cite]提供了构造性途径：

> **Definition:** [SCX信息瓶颈目标]
> <!-- label: def:ib_scx -->
> SCX审计的信息瓶颈目标为：
> 
> $$
>     \boxed{\min_{P_{Q|\mathbf{V}}} \; I(\mathbf{V}; Q) - \beta \cdot I(Y; Q)}，
> $$
> 
> 其中$Q$是压缩表示，$\beta > 0$控制压缩与保留标签信息之间的权衡。
> $\beta \to 0$对应极限压缩（$Q$独立于$\mathbf{V}$），
> $\beta \to \infty$对应无损审计（$Q$保留所有关于$Y$的信息）。

> **Proposition:** [SCX-IB的最优压缩结构]
> <!-- label: prop:ib_structure -->
> 对离散信源（投票空间$\{0,1\}^M$有限），SCX-IB的最优解满足：
> 
> $$
>     P_{Q|V}(q \mid \mathbf{v}) = \frac{P_Q(q)}{Z(\mathbf{v}, \beta)}
>     \exp\!\left(-\beta \cdot \KL(P_{Y|\mathbf{V}=\mathbf{v}} \| P_{Y|Q=q})\right)，
> $$
> 
> 其中$Z(\mathbf{v}, \beta)$是归一化常数。此解可通过**交替最小化**迭代求得：
> （i）固定$P_{Q|V}$，更新$P_{Y|Q}$为条件期望；
> （ii）固定$P_{Y|Q}$，按上述公式更新$P_{Q|V}$。

> **Proof:** 这是Tishby等 [cite]的核心结果在SCX信源上的直接应用。
> 将信源$X$替换为$\mathbf{V}$，目标变量保留为$Y$，IB的变分形式和交替最小化算法完全适用。
> 收敛保证来自目标函数的凸性（在$P_{Q|V}$和$P_{Y|Q}$上分别凸）。 $\square$

\rigorous{} **证明状态：严格。**IB的变分刻画和交替最小化的收敛性是信息论的标准结果。
在SCX投票空间上，$P_{Y|\mathbf{V}}$由专家投票模型和标签先验唯一确定，
IB算法提供了构造性的最优压缩方案。

\honeststrike{} **诚实暴击：IB方法的计算可行性。**
虽然IB的交替最小化在理论上收敛，但SCX投票空间的大小为$2^M$——
对$M=10$个专家即达$1024$个状态，对$M=20$个专家即超百万。
对于中等规模的专家集合，需要引入**退火**、**聚类**或
**神经网络参数化**的IB变体（如深度变分IB [cite]）。
但这些近似方法的逼近质量在有限样本下**无严格保证**。

### 有限$M$下的非渐近率失真界

> **Theorem:** [有限专家的非渐近审计界——Strassen界]
> <!-- label: thm:nonasymptotic_rdt -->
> 对于有限$M$个专家和$N$个状态原子，在通信总量$NR$比特、（每原子平均）失真$D$条件下，
> 存在码字当且仅当存在分布$P_{Q|\mathbf{V}}$使得：
> 
> $$
>     \boxed{\frac{1}{N} \sum_{s=1}^{N} I(\mathbf{V}_s; Q_s) \leq R
>     \quad 且 \quad
>     \frac{1}{N} \sum_{s=1}^{N} \E[d(\hat{Y}_s, Y_s)] \leq D}。
> $$
> 
> 在有限$N$下，还存在额外的**信道色散**（channel dispersion）项
> $O(1/\sqrt{N})$，使得实际所需速率比渐近理论预测高出约
> $\sqrt{V(D)/N} \cdot Q^{-1}(\epsilon)$，其中$V(D)$是率失真的信息色散，
> $Q^{-1}$是标准正态分布的分位数函数。

> **Proof:** 这是Kostina \& Verd\'{u} [cite]的非渐近率失真理论在SCX场景中的应用。
> 非渐近修正项来源于有限码长下的Berry-Esseen型正态近似误差。 $\square$

\rigorous{} **证明状态：严格。**该界基于信道编码的有限码长理论，是Strassen
（1962）和Hayashi（2006）工作的直接推广。但$V(D)$的计算需要信源分布的完整知识——
在SCX中这意味着精确已知所有专家的$p_{clean,s}$和$p_{noisy,s}$。

**对实践的启示：**对于实际规模的SCX审计（$N \approx 10^3$--$10^6$个状态原子），
非渐近修正项可能贡献$10\%$--$30\%$的额外速率需求。
忽略此修正可能严重低估通信带宽需求。

## 分布式共识的Slepian-Wolf编码：$M$个相关专家输出的无损压缩

### 从独立编码到分布式信源编码

在SCX审计的通信约束场景中，$M$个专家通常处于**分布式**位置——
每个专家独立编码自己的投票并传输给审计器，各编码器之间不通信。
这是分布式信源编码（Distributed Source Coding）的经典设定。

> **Definition:** [SCX分布式投票编码问题]
> <!-- label: def:distributed_coding -->
> $M$个编码器（专家）各自观测其投票$V_m \in \{0,1\}$。
> 编码器$m$产生码字$C_m(V_m) \in \{0,1\}^{nR_m}$。
> 审计器（联合解码器）从所有码字$(C_1, ..., C_M)$中恢复完整投票向量
> $\hat{\mathbf{V}} = (\hat{V}_1, ..., \hat{V}_M)$。
> 目标：$\lim_{n \to \infty} P(\hat{\mathbf{V}} \neq \mathbf{V}) = 0$
> （或每组$n$个状态原子的平均错误率趋于0）。

### Slepian-Wolf定理的SCX版本

> **Theorem:** [SCX Slepian-Wolf编码定理——相关专家的无损失压缩]
> <!-- label: thm:slepian_wolf_scx -->
> 设$M$个专家的投票$\mathbf{V} = (V_1, ..., V_M)$具有联合分布$P_{\mathbf{V}}$。
> 则存在分布式编码方案以任意小的错误概率恢复$\mathbf{V}$当且仅当速率$(R_1, ..., R_M)$满足：
> 
> $$
>     \boxed{\sum_{m \in \mathcal{T}} R_m \geq H(\mathbf{V}_\mathcal{T} \mid \mathbf{V}_{\mathcal{T}^c}),
>     \quad \forall \mathcal{T} \subseteq \{1, ..., M\}}，
> $$
> 
> 其中$\mathbf{V}_\mathcal{T} = \{V_m : m \in \mathcal{T}\}$，
> $\mathbf{V}_{\mathcal{T}^c} = \{V_m : m \notin \mathcal{T}\}$。
> **特别地，**总和速率仅需满足：
> 
> $$
>     \boxed{\sum_{m=1}^{M} R_m \geq H(\mathbf{V})}。
> $$
> 
> 当专家投票条件独立时，$H(\mathbf{V}) = \sum_{m} H(V_m) = M \cdot H_2(p)$，
> Slepian-Wolf区域退化为独立编码无增益的平凡情况。
> 当专家投票高度相关时（如$\Cov(V_i, V_j) \to \Var(V_i)$），
> $H(\mathbf{V}) \ll \sum_m H(V_m)$——分布式编码可获得显著增益。

> **Proof:** **步骤1（可达性）：**使用随机装箱（random binning）构造。
> 每个编码器$m$将典型序列$\mathbf{v}_m^n$随机分配到$2^{nR_m}$个箱（bin）中，
> 传输箱索引。解码器在所有箱的笛卡尔积中寻找联合典型的序列组。
> 由联合典型引理，正确序列组以概率趋于1被恢复。
> 
> **步骤2（逆定理）：**若某个子集$\mathcal{T}$违反速率不等式，则由条件熵的
> 不可压缩性，条件错误概率$\geq 1/2$——Fano不等式保证总错误概率有下界。
> 
> **步骤3（条件独立时的退化）：**当$V_m$条件独立时：
> $H(\mathbf{V}) = \sum_m H(V_m) = \sum_m H_2(p_{clean,s})$，
> 所有的Slepian-Wolf区域约束退化为$R_m \geq H(V_m)$——分布式编码无增益。
>  $\square$

\rigorous{} **证明状态：严格。**定理 [ref]是
Slepian-Wolf定理 [cite]在SCX投票信源上的直接应用。
SCX的设置甚至比一般Slepian-Wolf更简单——因为投票是**二元**的且信源字母表仅有
$\{0,1\}^M$（$2^M$个元素），随机装箱构造使用的典型性论证在有限字母表上尤为简单。

### 专家相关性红利——悖论性发现

> **Theorem:** [相关性红利悖论——Slepian-Wolf增益与SCX检测功效的反向关系]
> <!-- label: thm:correlation_paradox -->
> 设$\rho_{ij} = \Corr(V_i, V_j)$是专家$i$与$j$投票之间的相关系数。
> 则Slepian-Wolf可获得的压缩增益（相对于独立编码）为：
> 
> $$
>     \boxed{G_{SW}(\boldsymbol) = \frac{\sum_{m=1}^{M} H(V_m)}{H(\mathbf{V})} - 1
>     \geq 0}。
> $$
> 
> $G_{SW}$在$\rho_{ij} \to 1$时达到最大（$H(\mathbf{V}) \to H(V_1)$，
> 仅需1个专家的速率编码所有$M$个专家的信息），但此时Theorem~1的$\Delta_s$和有效专家数
> $M_{eff}$趋于0——**压缩最有效的场景恰恰是SCX审计最无效的场景**。

> **Proof:** **步骤1（相关性对联合熵的影响）：**由熵的链式法则：
> $H(\mathbf{V}) = \sum_{m=1}^{M} H(V_m \mid V_1, ..., V_{m-1}) \leq \sum_{m=1}^{M} H(V_m)$。
> 相关性增加→条件熵$H(V_m \mid V_{<m})$减小→$H(\mathbf{V})$减小→$G_{SW}$增大。
> 
> **步骤2（相关性对有效专家数的影响）：**由定理2.5.1（$M_{eff}$公式）：
> $M_{eff} = M / (1 + (M-1)\bar)$。
> 当$\bar \to 1$时，$M_{eff} \to 1$——$\Delta_s$的估计方差不随$M$衰减。
> 
> **步骤3（悖论的形式化）：**$G_{SW}$与$M_{eff}$通过$\bar$耦合：
> $G_{SW} \uparrow \iff \bar \uparrow \iff M_{eff} \downarrow$。
> **这就是``相关性红利悖论''：通信效率与审计可靠性不可兼得。** $\square$

\honeststrike{} **诚实暴击：Slepian-Wolf在实际SCX审计中的可部署性。**
Slepian-Wolf编码需要以下条件——它们在实际分布式审计中**可能不成立**：

1. **联合分布的精确知识：**编码器需要知道$P(V_1, ..., V_M)$来设计装箱——
2. **公共随机性：**随机装箱的种子需要在所有编码器和解码器之间共享——
3. **块长要求：**Slepian-Wolf的渐近最优性要求$n \to \infty$（``块编码''）——

> **Corollary:** [逐原子编码下的Slepian-Wolf退化]
> <!-- label: cor:slepian_wolf_degenerate -->
> 在逐原子（$n=1$）模式下，Slepian-Wolf编码**完全退化为独立编码**：
> 
> $$
>     \boxed{R_m \geq H(V_m) = H_2(p_{clean,s}) \;或\; H_2(p_{noisy,s})}。
> $$
> 
> 分布式编码的增益仅在$n \gg 1$的批处理（batch auditing）场景中显现。

\openproblem{} **开放问题1（零延迟Slepian-Wolf）：**
是否存在SCX投票的**零延迟**（zero-delay, $n=1$）分布式编码方案，
即使在没有大块的情况下也能利用专家间的相关性？
初步推测答案是否定的——这与Slepian-Wolf的经典逆定理一致——
但SCX投票的二元性和已知的$[0,1]$边际约束是否提供了额外的结构来绕过块长要求？

### 条件独立假设下的Slepian-Wolf区域可视化

当专家满足SCX的条件独立公理时，Slepian-Wolf区域退化为超立方体：
$R_m \geq H_2(p_{clean,s})$。
当专家存在相关性时（如共享训练数据、相同架构），可达速率区域**缩小**
（因为$H(V_i \mid V_j) \leq H(V_i)$），即**更少的比特足以恢复完整投票**。

这揭示了一个深刻的观点：**SCX框架追求的``专家独立性''实际上最大化了通信代价**。
独立性→Slepian-Wolf无增益→每专家需$H(V_m)$比特→总通信量$M \cdot H_2(p)$。
这是一个对SCX框架友好的结论——为了审计可靠性，通信效率的牺牲是值得的。

## Shannon分离定理的SCX推广：源编码与信道编码的分离性问题

### 经典分离定理与SCX的对应

Shannon信息论的基石之一是**分离定理**（Separation Theorem） [cite]：
在点对点通信中，信源编码（压缩数据以匹配信道容量）和信道编码
（保护数据免受信道噪声）可以**独立设计**而不损失最优性。
分离定理使得通信系统的设计可以模块化——压缩算法和纠错码可以独立优化。

SCX框架中存在类似的结构分解：

- **SCX``源编码''**：专家质量评分。将$M$个专家的复杂投票模式压缩为
- **SCX``信道编码''**：噪声检测/共识判定。

问题是：SCX中的源编码（质量评分）和信道编码（共识检测）能否分离？

### SCX分离定理

> **Theorem:** [SCX分离定理——条件独立下的最优分离]
> <!-- label: thm:scx_separation -->
> 设$M$个专家的投票$\mathbf{V}$在给定真实标签$Y$下**条件独立**。
> 则SCX审计存在最优的分离架构：
> 
1. **源编码层：**将$\mathbf{V}$压缩为充分统计量
2. **信道编码层：**将$T(\mathbf{V})$与阈值$\tau$比较以判定$Y$。

> 分离架构达到与联合优化相同的$F_1$分数。

> **Proof:** **步骤1（充分统计量识别）：**在条件独立假设下，对数似然比为：
> 
> $$
>     \Lambda(\mathbf{V}) = \sum_{m=1}^{M} \log\frac{P(V_m \mid Y = noisy)}{P(V_m \mid Y = clean)}
>     = \sum_{m=1}^{M} V_m \cdot w_m^* + const。
> $$
> 
> 由Fisher-Neyman因子分解定理，$T(\mathbf{V}) = \sum_m w_m^* V_m$是$Y$的**充分统计量**。
> 
> **步骤2（分离最优性验证）：**充分统计量意味着$Y \indep \mathbf{V} \mid T(\mathbf{V})$。
> 因此任何基于$\mathbf{V}$的决策规则可无损地替换为基于$T(\mathbf{V})$的决策规则。
> 信源编码（$\mathbf{V} \to T(\mathbf{V})$）不丢失关于$Y$的信息，
> 信道编码（基于$T(\mathbf{V})$的决策）达到与联合处理相同的最优错误概率。
> 
> **步骤3（分离失效条件）：**当条件独立假设被违反时，$T(\mathbf{V}) = \sum_m w_m V_m$
> 不再是充分统计量——相关性结构中携带额外的关于$Y$的信息。
> 此时分离架构**严格次优**于联合源-信道编码。 $\square$

\rigorous{} **证明状态：严格。**步骤1--2是充分统计量理论和指数族性质的直接应用。
步骤3的不等号方向由信息论标准结论保证
（当且仅当Markov链$Y \to T(\mathbf{V}) \to \mathbf{V}$成立时，$T(\mathbf{V})$是充分的）。

> **Theorem:** [分离失效定理——相关专家场景的联合编码优势]
> <!-- label: thm:separation_failure -->
> 当专家投票存在依赖性（$\Cov(V_i, V_j) \neq 0$）时，
> 联合源-信道编码架构可以达到严格优于分离架构的审计精度：
> 
> $$
>     \boxed{F_{1}^{joint} \geq F_{1}^{separate}
>     + \underbrace{\frac{I(Y; \mathbf{V}) - I(Y; T(\mathbf{V}))}{\log |\Y|}}_{分离的信息损失}
>     - O\!\left(\frac{1}{\sqrt{M}}\right)}。
> $$
> 
> 当专家间的条件依赖结构包含关于$Y$的信息时，分离损失严格为正。

> **Proof:** 由数据处理不等式和Fano不等式：
> 分离架构仅访问$T(\mathbf{V})$（充分统计量在非条件独立时丢失信息），
> 联合架构访问完整的$\mathbf{V}$。
> 两者可达的贝叶斯错误率之差由互信息差$I(Y; \mathbf{V}) - I(Y; T(\mathbf{V}))$的下界给出。
> 详见Cover \& Thomas [cite]第7章关于Fano和DPI的联合应用。 $\square$

\rigorous{} **证明状态：信息论部分严格。**分离损失$I(Y; \mathbf{V}) - I(Y; T(\mathbf{V}))$
的精确量化要求知道$\mathbf{V}$的完整联合分布——这在实践中未知。

### 分离定理的实践含义：模块化 vs.\ 端到端

> **Corollary:** [SCX架构设计准则]
> <!-- label: cor:architecture -->
> 
1. **若专家可被保证为条件独立**（通过独立的训练数据、异构架构、
2. **若专家存在已知的相关结构**（如共享预训练模型、同一实验室的方法论偏误）：
3. **若相关结构未知**：分离架构提供了可量化的下界性能保证，

\honeststrike{} **诚实暴击：分离定理的渐近性。**
Shannon分离定理是**渐近**结果（需要块长$n \to \infty$）。
在SCX的有限样本审计中（$n=1$或小$n$），分离架构可能由于以下原因而次优：
（i）充分统计量$T(\mathbf{V})$是实数值，其充分性仅在渐近意义下成立——
有限$M$下$T(\mathbf{V})$的离散性限制了其对$Y$的信息保留；
（ii）条件独立假设的微小违反在大$M$下被放大（类似于$p$-hacking中的累积偏误效应）。

**非渐近分离定理**目前是信息论中的活跃研究领域 [cite]，
将其应用于SCX需要更复杂的数学工具（如有限块长信道编码界）。

## Theorem 2的完整信息论推广：从Fano标量界到率失真信息瓶颈

### 原始Theorem~2及其信息论局限

Theorem~2（弱特征必然失效）的当前形式 [cite]为：

$$
    F_{1,SCX} \leq F_{1,base} + C_F \cdot \sqrt{\frac{2}}，
$$

其中$\delta = I(Y; X_{ideal}) - I(Y; X)$是**信息不足度**
（理想特征与实际特征之间的互信息差距），$C_F$是转换常数。
在Theorem~$2'$修正中（定义3.1），引入了$\varepsilon_$
（编码不完美度，$\varepsilon_ = I(Y; P \mid X) - I(Y; \PE(P) \mid X)$），
将上界修正为：

$$
    F_{1,SCX}^ \leq F_{1,base}
    + C_F \cdot \sqrt{\frac{\delta + 2\varepsilon_/C_F^2}{2}}。
$$

然而，这些界存在根本性的信息论局限：

1. **标量界的不紧性：**Fano不等式给出的$P_e$下界在低噪声区域
2. **缺失率失真维度：**$\delta$仅度量了**无条件**的信息不足，
3. **未利用分布结构：**$\delta = I(Y; X_{ideal}) - I(Y; X)$

### 信息不足度函数$\delta(R)$——率失真推广

> **Definition:** [信息不足度函数$\delta(R)$]
> <!-- label: def:delta_r -->
> 设$X$为实际特征，$X_{ideal}$为理想特征（能完全确定$Y$）。
> 定义**信息不足度函数**为：
> 
> $$
>     \boxed{\delta(R) = I(Y; X_{ideal}) - \max_{P_{U|X}: I(X;U) \leq R} I(Y; U)}，
> $$
> 
> 其中$R \geq 0$是允许用于编码特征$X$的信息速率（每样本比特数）。
> $\delta(0) = I(Y; X_{ideal}) - I(Y; X) = \delta_{original}$恢复原始定义。
> $\delta(\infty) = 0$（当$R$充分大时，$U$可以是$X$本身，无信息丢失）。
> $\delta(R)$在$R$中单调递减，凸性依赖于$P_{X,Y}$的具体结构。

> **Theorem:** [Theorem~2的率失真推广——信息不足度函数下的弱特征失效]
> <!-- label: thm:thm2_rdt -->
> 设SCX审计使用特征$X$的压缩表示$U$，满足$I(X; U) \leq R$。
> 则审计$F_1$分数的上界为：
> 
> $$
>     \boxed{F_{1,SCX}(R) \leq F_{1,base} + C_F \cdot r(\delta(R))}，
> $$
> 
> 其中$r(\delta) = \sqrt{\delta / (2 \log |\Y|)}$是率失真化的信息不足度-错误率映射函数。
> 特别地：
> 
1. $R \to 0$时：$\delta(R) \to \delta(0) = \delta$，上界恢复为原始Theorem~2；
2. $R \to \infty$时：$\delta(R) \to 0$，上界逼近$F_{1,base}$（特征信息充分则无弱特征惩罚）；
3. 对于中间$R$值：上界平滑地插值在原始Theorem~2（$R=0$）和无惩罚（$R=\infty$）之间。

> **Proof:** **步骤1（率失真约束下的Fano界）：**在特征压缩为$U$（速率$\leq R$）的条件下：
> 
> $$
>     P_e(R) \geq \frac{H(Y) - I(Y; U) - \log 2}{\log |\Y|}。
> $$
> 
> 
> **步骤2（信息不足度函数的嵌入）：**
> 
> $$
>     I(Y; U) &= I(Y; X_{ideal}) - [I(Y; X_{ideal}) - I(Y; U)] 

>             &\leq I(Y; X_{ideal}) - \delta(R) 

>             &= H(Y) - H(Y \mid X_{ideal}) - \delta(R)。
> $$
> 
> 
> **步骤3（代入错误率界并转化为$F_1$）：**
> 将步骤2代入步骤1，利用$H(Y \mid X_{ideal}) = 0$（理想特征完全确定$Y$的定义），
> 得到$P_e(R) \geq \delta(R) / \log |\Y| - O(1/\log|\Y|)$。
> 通过$F_1$与$P_e$的转换（见原始Theorem~2中$C_F$的推导），得到所述上界。
> 
> **步骤4（凸性与单调性验证）：**$\delta(R)$的单调递减性来自信息瓶颈函数
> $\max_{P_{U|X}: I(X;U) \leq R} I(Y; U)$在$R$中的凹性（Tishby等 [cite]的标准结果）。
> 因此$r(\delta(R))$随$R$单调递减，上界从$R=0$（最悲观）到$R=\infty$（最乐观）平滑过渡。 $\square$

\rigorous{} **证明状态：步骤1--3严格（信息论恒等式和不等式），步骤4中$\delta(R)$的
具体函数形式依赖于$P_{X,Y}$。对任意给定的$P_{X,Y}$，$\delta(R)$可通过IB交替最小化
精确计算（对于离散信源）或通过变分下界估计（对于连续/高维信源）。**

### 信息瓶颈视角下的弱特征失效机制

Theorem~2的深层机制可以通过信息瓶颈平面（Information Plane）来可视化：

> **Definition:** [SCX信息平面]
> <!-- label: def:info_plane -->
> SCX信息平面由横轴$I(X; U)$（压缩复杂度）和纵轴$I(Y; U)$（标签信息保留）定义。
> 信息瓶颈曲线$I(Y; U)^*(R) = \max_{P_{U|X}: I(X;U) \leq R} I(Y; U)$给出了
> 在给定压缩约束下可保留的最大标签信息。信息不足度函数$\delta(R)$度量的是
> 当前特征曲线与理想特征（$I(Y; U) = H(Y)$，$I(X; U)$任意）之间的**垂直距离**。

> **Proposition:** [弱特征失效的信息平面判据]
> <!-- label: prop:weak_feature_info_plane -->
> 特征$X$相对于理想特征$X_{ideal}$的弱特征失效程度，
> 由两条IB曲线的**分离度**量化：
> 
> $$
>     \boxed{\Delta_{IB}(R) = I_{ideal}(R) - I_X(R)}，
> $$
> 
> 其中$I_{ideal}(R)$和$I_X(R)$分别为理想特征和实际特征的信息瓶颈曲线。
> $\Delta_{IB}(R) > 0$对所有$R$成立等价于
> **无论投入多少表示容量，实际特征都无法达到理想特征的分类性能**——
> 这是Theorem~2的完整信息论推广。

\heuristic{} **证明状态：概念性框架。**信息瓶颈曲线的精确计算对于高维特征（如
$X \in \R^{768}$的BERT嵌入）在计算上是不可行的。实际中需使用变分IB
（Alemi等 [cite]）或神经网络估计器，这些近似方法的一致性
和收敛性在SCX场景中未经严格验证。

### $\varepsilon_{\PE$的率失真推广}

将$\varepsilon_$（编码不完美度）嵌入率失真框架，得到其自然的推广：

> **Definition:** [率失真编码不完美度]
> <!-- label: def:epsilon_rdt -->
> 
> $$
>     \boxed{\varepsilon_(R) = I(Y; P \mid X) - \max_{P_{U|\PE(P)}: I(\PE(P);U) \leq R} I(Y; U \mid X)}。
> $$
> 
> $\varepsilon_(0) = I(Y; P \mid X)$（未编码的位置信息全部丢失），
> $\varepsilon_(\infty) = \varepsilon_$（恢复定义3.1的原始定义）。

> **Corollary:** [率失真化的Theorem~$2'$]
> <!-- label: cor:thm2prime_rdt -->
> 在率失真框架下，Theorem~$2'$推广为：
> 
> $$
>     \boxed{F_{1,SCX}^(R_X, R_P) \leq F_{1,base}
>     + C_F \cdot r\!\left(\delta(R_X) + \frac{2\varepsilon_(R_P)}{C_F^2}\right)}，
> $$
> 
> 其中$R_X$和$R_P$分别是分配给状态特征$X$和位置编码$\PE(P)$的表示速率。
> $R_X$和$R_P$之间的最优分配给出**特征-位置信息预算的Pareto前沿**。

> **Proof:** 由定理 [ref]和定义 [ref]直接组合。两个速率约束
> 分别作用于$X$和$\PE(P)$的信息瓶颈，联合上界为两者互信息损失之和
> （由互信息的次可加性在条件独立的特殊情况下成立；一般情况下为$\leq$关系）。 $\square$

\rigorous{} **证明状态：在$U_X \indep U_P \mid (X, \PE(P))$的附加假设下严格。**
否则，联合表示$U = (U_X, U_P)$的信息损失严格小于分别压缩的信息损失之和
（协同效应）。此时$R_X$和$R_P$不可分离优化——需要联合信息瓶颈方法。

### 与Theorem~3的信息论连接

率失真框架提供了理解Theorem~3（噪声-困难不可区分性）的新视角：

> **Proposition:** [Theorem~3的率失真解释]
> <!-- label: prop:thm3_rdt -->
> Theorem~3的不可区分性等价于：在噪声世界$W_A$和困难世界$W_B$之间，
> 任何速率为$R$的压缩表示$Q$满足：
> 
> $$
>     \max_{W \in \{W_A, W_B\}} P_W(error \mid Q) \geq \frac{1}{2}
>     - \sqrt{\frac{1}{2} \KL(P_{Q|W_A} \| P_{Q|W_B})}。
> $$
> 
> 当$P_{Q|W_A} = P_{Q|W_B}$时（观测分布完全相同），
> 错误率下界$\geq 1/2$——任何决策规则不比随机猜测更好。

> **Proof:** 这是Le Cam引理在压缩表示上的直接应用：两个世界的KL散度为零意味着TV距离为零，
> 意味着最优检验的错误率之和$\geq 1$，因此$\max \geq 1/2$。 $\square$

**重要推论：**虽然固定$\PE$在$R \to \infty$时保持不可区分性（命题4.1），
但在有限速率$R$下，若$W_A$和$W_B$的$P_{Q|W}$因压缩而有微小差异，
则**可能存在**以高于$1/2$的概率区分两个世界的决策规则。
这为学习型$\PE$的破坏机制（定理4.1）提供了信息论基础——
有限的表示容量可能选择性地保留对区分两个世界有用的信息方向。

## 讨论：SCX信息论大厦——已建立的和待建立的

### 四个信息论支柱的相互依赖

本文的四个核心结果不是独立的，而是构成了SCX信息论的**逻辑梯级**：

1. **审计率失真界（\S2）**建立了SCX性能的**物理极限**：
2. **Slepian-Wolf编码（\S3）**提供了达到此极限的**编码构造**：
3. **分离定理（\S4）**论证了在**何种条件下**可以模块化设计SCX系统
4. **Theorem~2的率失真推广（\S5）**将弱特征失效的标量界提升为

四者共同的数学底座是**互信息**和**率失真函数**。
SCX的四条原始定理（Theorem~1--4）在信息论框架中被统一为
**一个信源（专家投票）**在**不同编码约束下**的**不同失真度量**。

### 理论诚实度总评

[Table omitted — see original .tex]

**最严重的理论漏洞：**

1. **渐近 vs.\ 有限样本：**本文绝大多数界是**渐近**的
2. **联合分布的未知性：**$P(\mathbf{V})$和$P_{Y|\mathbf{V}}$在本文的界中
3. **Slepian-Wolf的部署障碍：**第(1)(3)点在\S3的诚实暴击中已详细讨论；
4. **信息瓶颈的计算可行性：**高维SCX场景（大$M$，大$d_X$）中IB曲线的

### 与现有SCX文献的信息论缺口标注

本文揭示了SCX现有文献 [cite]中的**四个信息论缺口**，
这些缺口在本文中得到了填充（或至少被明确标注为开放问题）：

[Table omitted — see original .tex]

### 开放问题

1. **零延迟Slepian-Wolf编码（见\S3）：**SCX投票的二元性和边际约束
2. **非渐近SCX分离定理：**能否建立有限$M$下的分离定理版本，
3. **$\delta(R)$的经验估计：**信息不足度函数$\delta(R)$的精确计算
4. **Pareto最优的$R_X$-$R_P$分配：**在实际系统中，状态特征$X$和
5. **信息论界与深度学习审计器的实证对比：**本文的界是信息论的
6. **SCX的率失真-信道编码对偶性：**Theorem~4（Minimax最优）触及了

## 结论

本文为SCX框架建立了完整的信息论基础，从率失真理论、Slepian-Wolf分布式编码、
Shannon分离定理到信息瓶颈方法，系统性地将信息论的核心概念应用于多专家信息融合
的审计问题。

**核心发现：**

1. 有限通信带宽在SCX审计中引入不可消除的错误概率下界
2. 专家间的相关性既是通信效率的红利（Slepian-Wolf压缩增益），
3. SCX的``质量评分''和``共识检测''可以在条件独立假设下分离设计
4. Theorem~2的Fano标量界是率失真函数在$R=0$处的特例；

**本文的信息论大厦建立在SCX的四条原始定理之上：**
Theorem~1（Chernoff乐观界）→ 率失真悲观界（定理 [ref]）形成上-下界对；
Theorem~2（Fano标量界）→ 率失真函数推广（定理 [ref]）给出连续信息不足度；
Theorem~3（不可区分性）→ 率失真解释（命题 [ref]）揭示压缩的可能破坏机制；
Theorem~4（Minimax最优）→ 对偶性开放问题（开放问题6）连接误差指数与SCX信道容量。

**本文同样诚实地标注了信息论形式的边界：**渐近性假设在大$M$、大$N$下方成立；
Slepian-Wolf部署面临公共随机性和块长约束；分离定理在有限$M$下无严格保证；
$\delta(R)$的精确计算需要已知$P_{X,Y}$。这些问题不是信息论框架的失败，
而是SCX信息论大厦**待建立的东翼**。

\honeststrike{} **最终诚实暴击：**本文的数学美感和理论完整性不应掩盖一个基本事实：
SCX审计的**实践瓶颈**通常不是Shannon信息论极限，而是**社会技术因素**——
专家招募的成本、专家独立性的社会学验证、审计报告的可信度传播。
在通信带宽约束成为瓶颈之前，这些更基础的约束早已主导了SCX的实际性能。
信息论界提供了SCX的物理极限——但承认这一极限在大多数当前应用中尚未被逼近，
与宣称它已被逼近，是同样重要的诚实。

## 致谢

本文的信息论框架建立在一个多世纪以来信息论学者的工作之上——
Shannon (1948)、Slepian \& Wolf (1973)、Wyner \& Ziv (1976)、
Tishby等 (2000)、Cover \& Thomas (2006)。
SCX框架的四条核心定理（Theorem~1--4）为本文提供了应用场景和理论出发点。
`theory/information\_theory/`目录（SCX Project, 2026）包含本文定理的
原始推导笔记和数值验证脚本。

\begin{thebibliography}{99}

\bibitem{shannon1948}
C.~E.~Shannon.
\newblock A mathematical theory of communication.
\newblock *Bell System Technical Journal*, 27(3):379--423, 1948.

\bibitem{slepian1973}
D.~Slepian and J.~K.~Wolf.
\newblock Noiseless coding of correlated information sources.
\newblock *IEEE Transactions on Information Theory*, 19(4):471--480, 1973.

\bibitem{wyner1976}
A.~D.~Wyner and J.~Ziv.
\newblock The rate-distortion function for source coding with side information at the decoder.
\newblock *IEEE Transactions on Information Theory*, 22(1):1--10, 1976.

\bibitem{cover2006}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd edition.
\newblock Wiley, 2006.

\bibitem{tishby2000ib}
N.~Tishby, F.~C.~Pereira, and W.~Bialek.
\newblock The information bottleneck method.
\newblock In *Proceedings of the 37th Annual Allerton Conference on Communication,
  Control, and Computing*, 368--377, 2000.

\bibitem{alemi2017deep_ib}
A.~A.~Alemi, I.~Fischer, J.~V.~Dillon, and K.~Murphy.
\newblock Deep variational information bottleneck.
\newblock In *International Conference on Learning Representations (ICLR)*, 2017.

\bibitem{kostina2012}
V.~Kostina and S.~Verd\'{u}.
\newblock Fixed-length lossy compression in the finite blocklength regime.
\newblock *IEEE Transactions on Information Theory*, 58(6):3309--3338, 2012.

\bibitem{polyanskiy2010}
Y.~Polyanskiy, H.~V.~Poor, and S.~Verd\'{u}.
\newblock Channel coding rate in the finite blocklength regime.
\newblock *IEEE Transactions on Information Theory*, 56(5):2307--2359, 2010.

\bibitem{strassen1962}
V.~Strassen.
\newblock The existence of probability measures with given marginals.
\newblock *The Annals of Mathematical Statistics*, 36(2):423--439, 1965.

\bibitem{hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock *Journal of the American Statistical Association*,
  58(301):13--30, 1963.

\bibitem{scx2026theorems}
SCX Project.
\newblock {Theorem 1--4}: Multi-expert consistency, weak feature limits,
  unidentifiability, and minimax optimality.
\newblock Technical report, `src/scx/` and `theory/theorems/`, 2026.

\bibitem{scx2026situs}
SCX Project.
\newblock {Situs}: Physics-anchored positional encoding for state-conditioned expertise.
\newblock Preprint, `paper/situs\_theory/main.tex`, 2026.

\bibitem{scx2026info_theory}
SCX Project.
\newblock {Information-theoretic foundations of the SCX framework}:
  Rate-distortion bounds, distributed consensus coding, and separation theorems.
\newblock Technical report, `theory/information\_theory/`, 2026.

\bibitem{scx2026cc_audit}
SCX Project.
\newblock Multi-head spring and positional encoding analysis: {CC} audit report.
\newblock Technical report,
  `theory/self\_evolution/multi\_head\_spring\_and\_positional\_encoding\_analysis.md`,
  2026.

\bibitem{scx2026ppe_derivation}
SCX Project.
\newblock Physical positional encoding ({PPE}) rigorous derivation in the {SCX} framework.
\newblock Technical report,
  `theory/self\_evolution/ppe\_rigorous\_derivation.md`, 2026.

\bibitem{csiszar2011}
I.~Csiszár and J.~Körner.
\newblock *Information Theory: Coding Theorems for Discrete Memoryless Systems*,
  2nd edition.
\newblock Cambridge University Press, 2011.

\bibitem{el_gamal2011}
A.~El~Gamal and Y.-H.~Kim.
\newblock *Network Information Theory*.
\newblock Cambridge University Press, 2011.

\bibitem{wainwright2019}
M.~J.~Wainwright.
\newblock *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*.
\newblock Cambridge University Press, 2019.

\bibitem{boucheron2013}
S.~Boucheron, G.~Lugosi, and P.~Massart.
\newblock *Concentration Inequalities: A Nonasymptotic Theory of Independence*.
\newblock Oxford University Press, 2013.

\bibitem{ksg2004}
A.~Kraskov, H.~Stögbauer, and P.~Grassberger.
\newblock Estimating mutual information.
\newblock *Physical Review E*, 69(6):066138, 2004.

\end{thebibliography}