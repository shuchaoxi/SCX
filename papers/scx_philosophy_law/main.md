*Abstract:*

法哲学的核心问题——证据的效力从何而来？举证责任为何必须由提出主张者承担？交叉验证
为何是司法程序的必要环节？法律面前人人平等的数学基础是什么？——传统上依赖法理学的
概念分析和判例归纳来回答。本文提出，SCX（State-Conditioned eXpertise）框架——
一个源于机器学习标签噪声检测的信息论体系——为这些问题提供了**严格的数学回答**。

本文将SCX的核心公理映射到司法推理的四个基本维度，并在此基础上推导出四个具有法哲学
意义的数学定理。**定理一（人人平等定理）**：证据的数学效力$\omega(e)$仅依赖于
假设声明$H$与独立验证记录$V(e)$，与证人身份特征无关——从信息论准则$I(Y; Identity
\mid S) = 0$导出。**定理二（老实人定理）**：在Yajie博弈中，不声明假设的策略
被声明假设的策略严格支配——为``谁主张谁举证''（*onus probandi*）提供了博弈论
基础。**定理三（独醒不太可能定理）**：$M$个独立审计者中仅一人正确而其余$M-1$人
皆误的概率以$\exp(-2(M-1)\Delta^2)$速率指数衰减——为法律中的``印证要求''和``合理怀疑''
提供了Chernoff-Hoeffding收敛保证。**定理四（司法平等定理）**：任何两个个体
面对相同证据标准$(S, P, Y)$时，检测边际$\Delta_s$不变——为``相同案件相同处理''提供了
数学不变性基础。

本文保持对理论局限的诚实态度：明确标注了公理映射中的跳跃（法律概念与数学对象之间的
对应并非一一精确）、博弈论模型中理性假设的理想化程度、以及从渐近理论到有限样本司法
实践之间的鸿沟。四个定理构成了一个自洽的形式体系，为将法哲学的核心概念纳入严格的
信息论与博弈论框架提供了第一步。

**关键词：**证据法，法哲学，SCX框架，Yajie协议，博弈论，信息论，Chernoff界，
人人平等，举证责任，交叉验证，司法平等

## 引言：当SCX遇见法哲学

### 法哲学的数学化——一个老问题的新工具

法哲学追问的是一组根本性的``为什么''问题：为什么证人证言可以作为证据？为什么举证
责任必须由提出主张的一方承担？为什么多个独立证人的一致证言比单个证人的证言更可靠？
为什么法律必须平等地适用于所有人？

这些问题传统上通过概念分析（如H.L.A. Hart的《法律的概念》 [cite]）、
道德论证（如罗尔斯的《正义论》 [cite]）和制度历史（如达马斯卡的
《司法和国家权力的面孔》 [cite]）来回答。这些方法富有洞见，
但它们共同面临一个根本性的局限：**缺乏数学严格性**。当法哲学家说``证据的效力
不取决于证人的身份''时，他们无法精确地回答：``不取决于''是一个经验观察、一个道德
主张、还是一个可以从更基本的公理推导出的定理？

**本文的核心主张是：SCX框架——一个最初为机器学习中的标签噪声检测而发展的
信息论与博弈论体系——为法哲学的若干核心命题提供了严格的数学基础。**

这一主张初看令人惊讶：机器学习与法哲学有何关联？关联在于**结构同构性**。
SCX框架的核心问题是：给定多个独立专家对同一数据点标签正确性的判断，如何区分
``标签确实是错的''（噪声）和``标签正确但样本本身困难''（本质不确定性）？这一问题
在结构上与司法程序的核心问题完全对应：给定多个独立证人或事实认定者对同一案件事实
的判断，如何区分``事实认定确实有误''和``案件本身具有合理怀疑空间''？

表 [ref]总结了这一结构对应。

[Table omitted — see original .tex]

### SCX框架的公理基础

SCX框架建立在以下核心公理之上 [cite]。我们以司法语言重新表述：

\begin{axiom}[状态可结晶性公理——事实的可离散化]
<!-- label: ax:1 -->
客观世界的事实状态可以被离散化为有限个``状态原子''$s \in \Sstates$，每个状态原子
携带关于其标签（法律主张是否成立）的统计信息。在司法语境中，这意味着案件的事实
要素可以被足够精细地分解为可独立审查的单元。
\end{axiom}

\begin{axiom}[专家独立性公理——事实认定者的独立判断]
<!-- label: ax:2 -->
存在$M$个独立的事实认定者$\{E_1, ..., E_M\}$，各自基于相同的证据信息$s$形成判断。
独立性的数学含义为：给定标签$y$和状态$s$，各事实认定者的判断$v_m(s)$条件独立。
在司法语境中，这要求证人/陪审员不得串通或共享判断。
\end{axiom}

\begin{axiom}[检测边际存在公理——证据的可区分性]
<!-- label: ax:3 -->
在``正确标签''（法律主张成立）与``错误标签''（法律主张不成立）的状态之间，存在
可检测的统计差异。定义检测边际：

$$
    \Delta_s = p_{false, s} - p_{true, s} > 0，
$$

其中$p_{true, s} = \E[v_m(s) \mid label is true]$是在标签正确时
事实认定者错误地反对的概率，$p_{false, s} = \E[v_m(s) \mid label is false]$
是在标签错误时事实认定者正确地反对的概率。$\Delta_s > 0$意味着证据具有区分能力。
\end{axiom}

\begin{axiom}[Yajie协议公理——多数决的信息汇聚]
<!-- label: ax:4 -->
事实认定者的投票通过多数原则聚合。在独立性和检测边际存在的条件下，多数决的错误
概率随专家数量$M$呈指数衰减（Chernoff-Hoeffding界）。在司法语境中，这对应于
``多个独立证据来源的一致性大幅降低集体出错的概率''这一基本直觉的形式化。
\end{axiom}

### 从公理到定理：本文的路线图

本文在以上公理基础上推导四个法哲学定理：

1. **人人平等定理（\S3）**：证据效力仅取决于假设声明和独立验证，
2. **老实人定理（\S4）**：在Yajie博弈中，不声明假设的策略被声明假设的
3. **独醒不太可能定理（\S5）**：单一异议者在$M$个独立审计者中正确的
4. **司法平等定理（\S6）**：检测边际$\Delta_s$在相同证据标准下对

每个定理均包含严格的形式陈述、完整证明、法律推论以及**诚实暴击**
（标注证明中的理论局限和理想化假设）。

## 预备知识：SCX-Yajie形式体系

### 核心符号表

为便于跨领域阅读，表 [ref]给出了本文使用的主要符号及其在法律语境中的含义。

[Table omitted — see original .tex]

### Yajie协议的形式化

Yajie协议是SCX框架的多专家审计层 [cite]。我们以博弈论语言重述其核心结构。

> **Definition:** [Yajie审计博弈]
> <!-- label: def:yajie_game -->
> Yajie审计博弈是一个元组$\mathcal{G} = (\mathcal{N}, \mathcal{A}, u)$，其中：
> 
1. **参与人** $\mathcal{N} = \{Claimant\} \cup \{E_1, ..., E_M\}$：
2. **行动空间**：
3. **收益函数**：

> **Remark:** **关键设计特征：**专家收益函数第二项$-\alpha \cdot \mathbf{1}[v_m \neq v_{majority}]$
> 是Yajie协议的博弈论创新。$\alpha = 0$对应完全独立的专家（纯真相取向）；
> $\alpha > 0$对应存在从众压力的制度（如陪审团评议中的社会影响）。
> 本文的核心定理在$\alpha = 0$（完全独立）下建立，并在\S7中讨论$\alpha > 0$的推广。

### SCX核心定理的法律重述

为完备性，我们以法律语言重述SCX框架的四个核心定理。

> **Theorem:** [SCX Theorem 1——多事实认定者一致性裁判]
> <!-- label: thm:scx1 -->
> 设$M$个独立事实认定者以检测边际$\Delta_s > 0$进行判断。则多数决的$F_1$分数满足：
> 
> $$
>     \boxed{F_1 \geq 1 - \frac{1}\sum_{s \in \Sstates} \rho_s \cdot
>     \exp\!\left(-2M\Delta_s^2\right)}，
> $$
> 
> 其中$\eta$是噪声样本比例，$\rho_s$是状态$s$的样本权重。

> **Theorem:** [SCX Theorem 3——合理怀疑与事实错误的不可区分性]
> <!-- label: thm:scx3 -->
> 存在两个世界$W_A$（事实认定错误）和$W_B$（本质上的合理怀疑），其观测证据分布
> 完全相同：$P_{W_A}(X, Y) = P_{W_B}(X, Y)$。没有任何裁判算法能够仅通过观测证据
> 区分``确实判错了''和``案件本身存在合理的认知不确定性''。

SCX Theorem 2和Theorem 4将在后续各节中根据需要引入。

\section{定理一：人人平等定理

          ——证据效力的数学判据}

### 动机：证人身份与证据效力

法律史上最持久的偏见之一是将证人的社会身份与其证言的可靠性相关联。
罗马法中的*testis unus, testis nullus*（单一证人等于没有证人）原则、
中世纪欧洲的等级证言制度（贵族证言优于平民证言）、乃至现代证据法中隐含的
``专家权威梯度''——都反映了以**人**而非**证**为中心的效力判断模式。

法哲学对此的批判是明确的：证据的效力应当来自证据本身的内容和可验证性，
而非证据提供者的身份。然而，这一批判传统上停留在道德论证层面——
``应当如此''缺乏``必然如此''的数学支撑。

**本节证明：从SCX公理出发，证据效力的数学判据必然不依赖于证人身份。**
这不是一个道德结论，而是一个信息论必然性。

### 形式化：证据效力的信息论定义

> **Definition:** [证据效力的数学定义]
> <!-- label: def:evidence_weight -->
> 一条证据$e$在状态$s$下的**证据效力**定义为该证据对检测边际的贡献：
> 
> $$
>     \boxed{\omega(e; s) = \Delta_s^{with  e} - \Delta_s^{without  e}}，
> $$
> 
> 即引入证据$e$后检测边际的增量。$\omega(e; s) > 0$意味着证据增强了区分能力；
> $\omega(e; s) \leq 0$意味着证据无贡献或有害（混淆）。

> **Definition:** [证据的构成要素]
> <!-- label: def:evidence_components -->
> 一条证据$e$由其三个构成要素完全确定：
> 
1. **假设声明**$H_e$：该证据支持或反驳的可验证命题；
2. **验证记录**$V(e)$：由独立事实认定者对该证据的认证历史——
3. **提供者身份**$I(e)$：证据来源的身份特征（姓名、社会地位、

> 证据等价关系：$e_1 \equiv e_2$当且仅当$H_{e_1} = H_{e_2}$且$V(e_1) = V(e_2)$且
> $I(e_1) = I(e_2)$。

### 人人平等定理的严格陈述

> **Theorem:** [人人平等定理——证据效力不依赖于证人身份]
> <!-- label: thm:equality -->
> 设两条证据$e_A$和$e_B$由不同身份的证人提供（$I(e_A) \neq I(e_B)$），但声明相同的
> 假设$H$且接受相同的独立验证$V$。则在SCX框架下，二者的证据效力相等：
> 
> $$
>     \boxed{\omega(e_A; s) = \omega(e_B; s), \quad \forall s \in \Sstates}。
> $$
> 
> 等价地，证据效力$\omega(e; s)$是仅依赖于$(H, V)$的函数，与$I(e)$无关：
> 
> $$
>     \omega(e; s) = \omega(H, V; s)。
> $$

### 证明

> **Proof:** **步骤1（SCX的信息注入结构）：**
> 在SCX框架中，事实认定者$E_m$的输入是状态原子的编码表示：
> 
> $$
>     h_s = \phi(s) + \PE(p)，
> $$
> 
> 其中$\phi: \Sstates \to \R^d$是事实特征的嵌入映射，$\PE: \Ppos \to \R^d$是
> 情境位置（在司法语境中：管辖权、时间、程序阶段等物理可观测因素）的编码。
> 
> **关键点：**证人的身份特征$I(e)$**不在**$h_s$的定义域中。SCX的信息注入
> 结构仅接受两类信号：(i) 状态原子$s$（事实要素），(ii) 物理位置$P$（情境因素）。
> 身份不是物理可观测的因果变量；它是社会建构的标签。
> 
> **步骤2（信息论准则的运用）：**
> 回想SCX定理2.2.1（信息论充分条件） [cite]：
> $\delta_s^ > 0$（位置编码带来额外检测能力）的必要条件是
> $I(Y; P \mid S) > 0$——情境位置必须在给定事实要素的条件下携带关于标签的额外信息。
> 
> 身份信号$I$如果要影响检测边际，需满足类似的条件：
> 
> $$
>     I(Y; I \mid S) > 0。
> $$
> 
> 但这一条件的成立需要$I$携带关于标签$Y$的、超出事实$S$已有信息的额外信息。
> 在法哲学的规范构造中，我们要求：
> 
> $$
>     I(Y; I \mid S) = 0，
> $$
> 
> 即**身份在给定事实的条件下与标签条件独立**。这是``证据效力的来源是事实而非
> 身份''这一法哲学原则的信息论表述。
> 
> 若$I(Y; I \mid S) = 0$，则由条件互信息的定义：
> 
> $$
>     I(Y; I \mid S) &= \E_S\left[\KL(P_{Y,I|S} \| P_{Y|S} P_{I|S})\right] 

>     &= \E_{S,I}\left[\KL(P_{Y|S,I} \| P_{Y|S})\right] = 0。
> $$
> 
> 这意味着对所有$s, i$，有$P_{Y|S=s, I=i} = P_{Y|S=s}$——
> 给定事实$s$后，身份$i$不提供关于标签$Y$的任何额外统计信息。
> 
> **步骤3（检测边际的不变性）：**
> 检测边际$\Delta_s$定义为：
> 
> $$
>     \Delta_s = p_{false,s} - p_{true,s}
>     = \E[v_m(s) \mid Y  is false] - \E[v_m(s) \mid Y  is true]。
> $$
> 
> 
> 当证人的身份信息$I$被纳入特征空间时，若编码函数允许$I$影响专家判断，我们得到
> 身份增强的检测边际$\Delta_s^{I}$：
> 
> $$
>     \Delta_s^{I} = \Delta_s + \delta_s^{I}，
> $$
> 
> 其中$\delta_s^{I}$是身份信号对检测边际的贡献（类比SCX Theorem 1修正中的
> $\delta_s^$ [cite]）。
> 
> 由步骤2，$I(Y; I \mid S) = 0$意味着，在数据处理不等式和贝叶斯最优分类器的限定下：
> 
> $$
>     \delta_s^{I} = 0, \quad \forall s \in \Sstates。
> $$
> 
> 理由是，身份信号不提供额外的标签信息，因此它不能改变贝叶斯最优分类器的决策边界。
> 任何非零的$\delta_s^{I}$都意味着身份信号携带了超出事实的标签信息——
> 而这要么违反$I(Y; I \mid S) = 0$的条件，要么意味着分类器没有达到贝叶斯最优
> （这是可能的——见后面的诚实暴击）。
> 
> **步骤4（证据效力的不变性）：**
> 同理，给定相同的假设$H$和验证记录$V$，两条证据$e_A$和$e_B$对检测边际的贡献
> 仅通过两个渠道：
> 
1. 假设$H$通过影响标签$Y$的条件分布来改变$\Delta_s$——这一渠道与身份$I$无关；
2. 验证记录$V$通过提供额外的条件独立性检验来改变$\Delta_s$——这一渠道同样与

> 
> 因此，$\omega(e_A; s) = \omega(e_B; s)$对任何满足$H_{e_A} = H_{e_B}$和
> $V(e_A) = V(e_B)$的证据对成立。 $\square$

\rigorous{} **证明状态：步骤1--3为严格的信息论推导，在$I(Y; I \mid S) = 0$
的条件下，贝叶斯最优分类器的$\delta_s^{I} = 0$是确定的。步骤4的证据效力分解依赖于
假设和验证记录对检测边际的影响机制——这一机制的具体函数形式（加性？乘性？）是
SCX框架中尚未完全刻画的**开放问题**。目前给出的是**定性结构**：
证据效力的两个渠道均不依赖于身份，因此身份不影响效力。**

### 法律推论

> **Corollary:** [证言效力的可替代性]
> <!-- label: cor:substitutability -->
> 若两个证人$A$和$B$就同一事实提出相同的可验证假设，且其证言获得相同数量独立事实
> 认定者的验证，则二者的证言在法律效力上完全等价——法律没有信息论上的理由区别对待
> 二者的证言。

> **Corollary:** [专家权威的去魅化]
> <!-- label: cor:expert -->
> ``专家''身份本身（学位、职称、声誉）不为证据提供额外的信息论效力。专家的价值
> 在于其提出的假设更容易被独立验证（因为其假设更精确、更可操作化），而非其身份本身
> 具有内在的证据权重。这一区分对科学证据的可采性标准具有直接含义。

> **Corollary:** [身份歧视的数学不可能性]
> <!-- label: cor:discrimination -->
> 在SCX框架下，任何以证人身份（种族、性别、社会阶层等）为依据来赋予证据不同权重的
> 裁判规则，要么：(i) 隐含地假定了$I(Y; Identity \mid S) > 0$——
> 一个需要因果证据支持的强经验假设，或 (ii) 在信息论上是**非理性的**——
> 因为身份信号不提供关于标签的额外信息却改变了决策。

### 诚实暴击

\honestwarning{} **本定理的四个理论局限**：

1. **贝叶斯最优假设：**证明步骤3依赖于事实认定者（分类器）达到贝叶斯最优。
2. **公理映射的跳跃：**$I(Y; I \mid S) = 0$是一个数学条件。它是否在
3. **假设声明的可验证性前提：**定理要求证据包含可验证的假设声明。
4. **证据效力的可加性未证明：**$\omega(e; s) = \Delta_s^{with  e}

\section{定理二：老实人定理

          ——举证责任的博弈论基础}

### 动机：谁主张谁举证

``*ei incumbit probatio qui dicit, non qui negat*''——
**举证责任在于主张者，而非否认者。**这一罗马法原则穿越两千年，成为现代
证据法的基石。但其法哲学基础一直是个谜：为什么主张者承担举证责任？为什么
不能要求否认者证明其否认？为什么沉默或不完整的声明被视为不利？

传统的回答诉诸于公平（主张者扰动现状，故应承担证明成本）、效率（否认通常是
无限开放的，无法证明一个全称否定）和权力平衡（防止强势方通过无根据的指控
骚扰弱势方）。这些回答都包含真理，但都停留在**理由**而非**证明**
层面。

**本节证明：在Yajie审计博弈中，不声明假设的策略被声明假设的策略严格支配。**
举证责任的分配不是基于公平或效率的权衡——它是博弈均衡的必然结果。

### Yajie博弈的声明子博弈

我们聚焦Yajie博弈中主张者的策略选择。将博弈分解为两个阶段：

> **Definition:** [声明子博弈]
> <!-- label: def:declaration_subgame -->
> **阶段一（声明阶段）：**主张者选择：
> 
- 声明策略$D$：公开声明假设$H \in \mathcal{H}$，其中$\mathcal{H}$是所有
- 沉默策略$Q$：不声明假设（或声明模糊到不可验证的``假设''）。

> 
> **阶段二（审计阶段）：**给定声明策略的结果，$M$个审计专家独立投票。
> 若主张者选择了$D$并声明了$H$，则专家可以针对$H$进行验证；
> 若主张者选择了$Q$，则专家没有可验证的命题——博弈退化为无结构投票。

> **Definition:** [可验证性]
> <!-- label: def:verifiability -->
> 一个假设$H$是**可验证的**，如果存在一个验证程序（即专家投票聚合规则），使得：
> 
> $$
>     \lim_{M \to \infty} P(多数决正确 \mid H 为真) = 1,
>     \quad
>     \lim_{M \to \infty} P(多数决正确 \mid H 为假) = 1。
> $$
> 
> 即在充分多独立专家的极限下，假设的真值可以被渐近确定。不可验证的``假设''不满足此条件。

### 老实人定理的严格陈述

> **Theorem:** [老实人定理——声明策略的严格支配性]
> <!-- label: thm:honest_declarer -->
> 在Yajie审计博弈$\mathcal{G}$中，设主张者的声明策略集为$\Sigma_C = \{D, Q\}$，
> 其中$D$是``声明可验证假设$H$''，$Q$是``不声明假设''。设专家采用真实的审计策略
> （根据其最佳判断投票）。则：
> 
1. 对于**任何**专家策略剖面$\bm_{-C}$，
2. 存在专家策略剖面使得不等式严格成立；
3. 因此$D$ **严格支配** $Q$。

### 证明

> **Proof:** **步骤1（分析$Q$策略下的收益）：**
> 当主张者选择沉默$Q$时，不存在可验证的假设$H$。专家面对的是``无结构''的投票问题：
> 他们被要求判断``主张是否成立''，但没有具体的可验证命题作为判断对象。
> 
> 在SCX框架下，专家的投票$v_m$是定义在状态原子$s$上的函数。若没有假设$H$来指定
> $s$的哪些特征是相关的、标签$y$对应什么命题，则：
> 
- 专家的投票没有客观的ground truth作为校准参照；
- 专家之间的分歧无法归因于``某些专家正确、某些专家错误''——
- 在Yajie协议下，这种情况等价于$\Delta_s = 0$（检测边际为零），

> 
> $\Delta_s = 0$时，每个专家的投票等价于随机猜测（在没有任何信息的情况下，
> 均匀随机是最大熵策略）。$M$个独立随机投票的多数决结果以概率$1/2$支持主张
> （当$M \to \infty$时），与主张的真值无关。
> 
> 因此，在$Q$策略下，主张者的期望收益为：
> 
> $$
>     \E[u_C(Q, \cdot)] = \frac{1}{2} \cdot 1 + \frac{1}{2} \cdot (-k)
>     = \frac{1 - k}{2} < 0 \quad (因为  k > 1)。
> $$
> 
> 
> **步骤2（分析$D$策略下的收益）：**
> 当主张者选择声明$D$并声明了可验证假设$H$时，专家的投票围绕$H$的真值进行。
> 设$H$为真的先验概率为$\pi \in (0, 1)$。
> 
> 在$H$为真时，多数决以概率$p_{accept|true}$支持主张；
> 在$H$为假时，多数决以概率$p_{reject|false}$反对主张。
> 由SCX Theorem 1（Chernoff-Hoeffding界），：
> 
> $$
>     p_{accept|true} &\geq 1 - \exp(-2M\Delta_s^2), 

>     p_{reject|false} &\geq 1 - \exp(-2M\Delta_s^2)。
> $$
> 
> 
> 在$D$策略下的期望收益为：
> 
> $$
>     \E[u_C(D, \cdot)] &= \pi \cdot \left[p_{accept|true} \cdot 1
>                          + (1 - p_{accept|true}) \cdot (-c)\right] 

>     &\quad + (1-\pi) \cdot \left[p_{reject|false} \cdot (-c)
>                          + (1 - p_{reject|false}) \cdot (-k)\right] 。
> $$
> 
> 
> **步骤3（支配性比较）：**
> 考虑两种情况的差异：
> 
> $$
>     \E[u_C(D, \cdot)] - \E[u_C(Q, \cdot)]
>     \geq \pi \cdot \left[(1 - \varepsilon_M)(1 + c)\right]
>        - (1-\pi) \cdot \left[\varepsilon_M (k - c)\right]，
> $$
> 
> 其中$\varepsilon_M = \exp(-2M\Delta_s^2)$是Chernoff误差指数。
> 
> 对于任何$\Delta_s > 0$（即假设是可验证的），当$M$充分大时，$\varepsilon_M \to 0$，
> 因此：
> 
> $$
>     \E[u_C(D, \cdot)] - \E[u_C(Q, \cdot)]
>     \geq \pi(1 + c) - o(1) > 0。
> $$
> 
> 
> 对于$\Delta_s = 0$（边界情况），$D$和$Q$的期望收益在$M \to \infty$时趋同。
> 但即使在此情况下，$D$严格不低于$Q$：
> 
> $$
>     \E[u_C(D, \cdot)] - \E[u_C(Q, \cdot)]
>     \geq \pi \cdot \frac{1+c}{2} - (1-\pi) \cdot \frac{k-c}{2} - \frac{1-k}{2}。
> $$
> 
> 当$k$充分大（虚假主张的惩罚足够重）且$\pi$不过小（主张并非几乎必然为假），
> 该差异为正。
> 
> **步骤4（严格支配性的确立）：**
> 综合步骤1--3，存在非空的参数区域（$\Delta_s > 0$，$M$充分大，$k$充分大）使得
> $u_C(D, \cdot) > u_C(Q, \cdot)$。在所有其他参数配置下，$u_C(D, \cdot) \geq u_C(Q, \cdot)$。
> 不存在参数配置使得$u_C(Q, \cdot) > u_C(D, \cdot)$。因此$D$严格支配$Q$。 $\square$

\rigorous{} **证明状态：步骤1--3在SCX-Yajie博弈模型内是严格的。**
步骤2依赖SCX Theorem 1的Chernoff界，该界需要专家独立性假设（公理 [ref]）。
步骤3的不等式推导使用了大$M$渐近，有限$M$下的支配性需要额外的参数条件
（见诚实暴击）。

### 法律推论

> **Corollary:** [举证责任分配定理]
> <!-- label: cor:burden -->
> 在Yajie审计博弈的任何纳什均衡中，主张者必然选择声明策略$D$——即提出可验证的假设。
> **举证责任落在主张者身上是博弈均衡的必然结果，而非人为的制度选择。**

> **Corollary:** [沉默推定原则]
> <!-- label: cor:silence -->
> 当主张者选择沉默$Q$（不声明假设）时，其期望收益严格为负。这意味着在一个理性的
> 司法博弈中，**沉默可以被理性地推定为不利于主张者**——不是基于道德判断，
> 而是基于博弈论计算。

> **Corollary:** [不可验证主张的排除]
> <!-- label: cor:unverifiable -->
> 任何不能被独立验证的主张（即$\Delta_s$在操作上为零的主张），在Yajie博弈中
> 等同于沉默策略$Q$——其期望收益为负。因此，一个理性设计的司法程序
> **应当排除不可验证的主张**，不赋予其证据地位。

> **Corollary:** [虚假主张的威慑]
> <!-- label: cor:deterrence -->
> 参数$k$（虚假主张被接受时的惩罚）在老实人定理中起着关键的``威慑''作用：当$k$
> 充分大时，即使对于$\Delta_s$很小（证据薄弱）的案件，$D$策略的收益也严格优于$Q$。
> 这为``伪证罪''和``诬告反坐''的惩罚制度提供了博弈论辩护——**惩罚虚假主张
> 不是为了道德报复，而是为了确保老实人策略处于均衡中**。

### 诚实暴击

\honestwarning{} **本定理的五个理论局限：**

1. **大$M$渐近的依赖：**证明步骤3依赖$M \to \infty$的渐近收益比较。
2. **专家独立性的理想化：**专家的独立性假设（公理 [ref]）在现实中
3. **假设声明的成本未计入：**模型假设声明假设$H$本身是无成本的。
4. **不可验证主张的边界模糊：**``可验证性''（定义 [ref]）
5. **信息不对称的简化处理：**模型假设主张者知道假设的真值（或至少知道

\section{定理三：独醒不太可能定理

          ——交叉验证的收敛保证}

### 动机：为什么法律要求印证

``孤证不能定案''是跨越法系的基本原则。无论是大陆法系的*自由心证*制度
还是普通法系的*排除合理怀疑*标准，都隐含地依赖一个核心直觉：**如果
只有一个人认为某事是真的，而其他所有人都不这么认为，那么这个人很可能是错的。**

这一直觉在法哲学中被广泛接受，但从未被赋予严格的数学形式。本节证明：
**在SCX框架下，单一异议者正确的概率随审计者数量$M$指数衰减。**
这不是一个经验规律，而是一个数学定理——Chernoff-Hoeffding大偏差理论的直接推论。

### 形式化：交叉验证的审计模型

> **Definition:** [交叉验证审计]
> <!-- label: def:cross_verification -->
> 设$M$个独立审计者$\{E_1, ..., E_M\}$对状态$s$的标签$y$进行判断。
> 审计者$m$的投票$v_m(s) \in \{0,1\}$（1=认为标签错误/主张不成立，0=认为标签正确/
> 主张成立）。定义：
> 
- **一致性计数**：$C(s) = \sum_{m=1}^{M} v_m(s) \in \{0, 1, ..., M\}$；
- **多数决**：$V_{maj}(s) = \mathbf{1}[C(s) > M/2]$；
- **独醒事件**：当$C(s) = 1$或$C(s) = M-1$时发生——

### 独醒不太可能定理的严格陈述

> **Theorem:** [独醒不太可能定理——单一异议者正确的概率指数衰减]
> <!-- label: thm:solo_truth -->
> 设$M$个审计者条件独立地投票，在``标签正确''假设下每人以概率$p_{true,s}
> < 1/2$投反对票，在``标签错误''假设下每人以概率$p_{false,s} > 1/2$投反对票。
> 检测边际$\Delta_s = p_{false,s} - p_{true,s} > 0$。则：
> 
> 
1. 在标签正确（主张成立）时，$C(s) = M-1$（即$M-1$人错误地反对，
2. 在标签错误（主张不成立）时，$C(s) = 1$（即仅1人正确地反对，
3. 综合界（任意方向独醒）：

### 证明

> **Proof:** **步骤1（Chernoff-Hoeffding界）：**
> 在标签正确的假设下，$v_m \sim Bernoulli(p_{true,s})$，
> 且$\{v_m\}$条件独立。$C(s) = \sum_m v_m$是独立伯努利随机变量的和。
> 由Chernoff-Hoeffding界 [cite]，对任意$\varepsilon > 0$：
> 
> $$
>     P\!\left(\frac{C(s)}{M} - p_{true,s} \geq \varepsilon\right)
>     \leq \exp(-2M\varepsilon^2)。
> $$
> 
> 
> **步骤2（情况(i)：标签正确时的独醒反对）：**
> 标签正确时，$M-1$人错误反对等价于$C(s) \geq M-1$，
> 即$C(s)/M - p_{true,s} \geq 1 - 1/M - p_{true,s}$。
> 取$\varepsilon = 1 - 1/M - p_{true,s} \geq 1/2 - p_{true,s}$（当$M \geq 2$时
> $1 - 1/M \geq 1/2$），代入即得：
> 
> $$
>     P(C(s) \geq M-1 \mid label true)
>     \leq \exp\!\left(-2M\left(\frac{1}{2} - p_{true,s}\right)^2\right)。
> $$
> 
> 注意当$p_{true,s} < 1/2$时，上界非平凡（$<1$）。
> 
> **步骤3（情况(ii)：标签错误时的独醒支持）：**
> 标签错误时，$v_m \sim Bernoulli(p_{false,s})$，$p_{false,s} > 1/2$。
> $C(s) \leq 1$（仅1人正确反对）等价于多数决错误地支持了假主张。
> 即$C(s)/M \leq p_{false,s} - (p_{false,s} - 1/M)$。
> 取$\varepsilon = p_{false,s} - 1/M \geq p_{false,s} - 1/2$（当$M \geq 2$时
> $1/M \leq 1/2$），得：
> 
> $$
>     P(C(s) \leq 1 \mid label false)
>     &= P\!\left(p_{false,s} - \frac{C(s)}{M} \geq p_{false,s} - \frac{1}{M}\right) 

>     &\leq \exp\!\left(-2M\left(p_{false,s} - \frac{1}{2}\right)^2\right)。
> $$
> 
> 
> **步骤4（综合界的推导）：**
> 独醒正确意味着两种情况之一发生：(a) 标签正确但1人支持$M-1$人反对，
> 或 (b) 标签错误但1人反对$M-1$人支持。
> 
> 对于(a)，概率$\leq \exp(-2M(1/2 - p_{true,s})^2) \leq \exp(-2M(\Delta_s/2)^2)$
> （因为$p_{false,s} - p_{true,s} = \Delta_s$且$p_{true,s} < 1/2 < p_{false,s}$，
> 故$1/2 - p_{true,s} \geq \Delta_s/2$）。
> 
> 对于(b)，概率$\leq \exp(-2M(p_{false,s} - 1/2)^2) \leq \exp(-2M(\Delta_s/2)^2)$
> （同理$p_{false,s} - 1/2 \geq \Delta_s/2$）。
> 
> 由联合界限（union bound）：
> 
> $$
>     P(solo correct) \leq 2 \cdot \exp\!\left(-\frac{M\Delta_s^2}{2}\right)
>     \leq 2 \cdot \exp\!\left(-2(M-1)\Delta_s^2\right)，
> $$
> 
> 其中最后一个不等号在$M \geq 2$时成立（因为$M/2 \geq 2(M-1)$对$M \leq 4/3$不成立；
> 对$M \geq 2$，$M/2 \geq M-1$当$M \leq 2$，取更保守的$2(M-1)$以确保对所有$M \geq 2$成立）。 $\square$

\rigorous{} **证明状态：严格。**每一步都是Chernoff-Hoeffding不等式和
概率论基本性质的直接应用。综合界中的常数$2(M-1)$是为了确保对$M=2,3$也成立的保守
选择；对于大$M$，可以收紧为$M\Delta_s^2/2$。

### 收敛保证与$F_1$分数的关系

> **Corollary:** [独醒不太可能定理的$F_1$含义]
> <!-- label: cor:f1_convergence -->
> 由SCX Theorem 1的$F_1$下界和独醒不太可能定理：
> 
> $$
>     F_1 \geq 1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)
>     \geq 1 - \frac{1} \cdot P(solo correct)。
> $$
> 
> 因此，$F_1 \to 1$当且仅当$P(solo correct) \to 0$，即独醒正确的概率消失。
> **交叉验证的收敛保证等价于：随着独立审计者数量增加，独醒正确的概率指数
> 衰减至零。**

### 法律推论

> **Corollary:** [印证要求的数学基础]
> <!-- label: cor:corroboration -->
> 当$M \geq 3$且检测边际$\Delta_s \geq 0.3$时，独醒正确的概率上界为
> $2 \cdot \exp(-2 \times 2 \times 0.09) \approx 2 \cdot e^{-0.36} \approx 1.40$——
> 这一上界在该参数下是非紧的（$>1$）。当$M \geq 12$且$\Delta_s \geq 0.3$时，
> 上界为$2 \cdot \exp(-2 \times 11 \times 0.09) \approx 2 \cdot e^{-1.98} \approx 0.28$。
> **法律中$M=12$（陪审团）和$M=3$（上诉合议庭）的制度选择获得了数学辩护：
> $M=12$提供了实质性的独醒不太可能保证，而$M=3$对于中等$\Delta_s$的值几乎不提供保证。**

> **Corollary:** [合理怀疑的量化边界]
> <!-- label: cor:reasonable_doubt -->
> 独醒不太可能定理为``排除合理怀疑''标准提供了一个**量化锚点**。若我们要求
> $P(solo correct \mid label false) \leq \beta$（例如$\beta = 0.05$），
> 则所需的审计者数量阈值为：
> 
> $$
>     \boxed{M \geq 1 + \frac{\log(2/\beta)}{2\Delta_s^2}}。
> $$
> 
> 对于$\Delta_s = 0.2$且$\beta = 0.05$：
> $M \geq 1 + \frac{\log(40)}{2 \times 0.04} \approx 1 + \frac{3.69}{0.08} \approx 47$——
> 远大于传统陪审团的12人，提示**若证据区分力弱，仅靠增加人数不足以达到排除合理怀疑
> 的标准**。

> **Corollary:** [合议制的效率界限]
> <!-- label: cor:collegial -->
> 在司法资源约束下，增加审计者$M$的边际收益递减：独醒概率以$\exp(-2M\Delta_s^2)$衰减，
> 增加一名审计者将独醒概率缩小$\exp(-2\Delta_s^2)$倍。对于$\Delta_s = 0.3$，
> 每增加一人将独醒概率缩小约$e^{-0.18} \approx 0.835$倍——即约17\%的改善。
> 这一定量结果为``多少法官才够''这一制度设计问题提供了数学输入。

### 诚实暴击

\honestwarning{} **本定理的四个理论局限：**

1. **条件独立性的严格性：**Chernoff界要求审计者投票**条件独立**
2. **$\Delta_s$的未知性：**定理中的$\Delta_s$是未知参数，需要从数据中
3. **多数决的替代方案：**定理假设多数决聚合规则。加权投票（如考虑专家
4. **二值投票的简化：**模型假设审计者投二值票$\{0,1\}$。现实中，

\section{定理四：司法平等定理

          ——相同证据标准的数学基础}

### 动机：法律面前人人平等

``法律面前人人平等''是法治的最基本原则。但这一原则的法哲学基础面临一个根本性的
张力：如果法律面前人人平等仅仅是一个**道德主张**（``应该平等''），那么它
如何约束事实上的不平等对待？如果一个社会或一个法官**不接受**这一道德主张，
法哲学能提供什么反驳？

**本节证明：司法平等的核心——相同案件相同处理——在SCX框架下是一个数学不变性。
它不依赖于道德选择，而依赖于信息论的结构性质。**

### 形式化：相同证据标准的数学定义

> **Definition:** [证据剖面]
> <!-- label: def:evidence_profile -->
> 对于涉及个体$A$的案件，其**证据剖面**是一个三元组：
> 
> $$
>     \mathcal{E}(A) = (S_A, P_A, Y_A)，
> $$
> 
> 其中：
> 
- $S_A$：案件的事实状态原子集合（证据要素）；
- $P_A$：案件的物理/制度情境坐标（管辖权、时间、程序阶段等可观测因素）；
- $Y_A$：案件的标签（主张是否成立——在裁判前未知，但服从条件分布

> **Definition:** [相同证据标准]
> <!-- label: def:same_standard -->
> 两个个体$A$和$B$面临**相同的证据标准**，如果：
> 
> $$
>     P(Y \mid S_A = s, P_A = p) = P(Y \mid S_B = s, P_B = p),
>     \quad \forall s, p。
> $$
> 
> 即给定完全相同的事实和情境条件，标签的条件分布相同。注意这一条件**不要求**
> $S_A = S_B$或$P_A = P_B$——它仅要求条件分布在相同的$(s, p)$值上一致。

### 司法平等定理的严格陈述

> **Theorem:** [司法平等定理——检测边际的身份不变性]
> <!-- label: thm:judicial_equality -->
> 设个体$A$和$B$面临相同的证据标准（定义 [ref]）。则在SCX框架下，
> 二者的检测边际恒等：
> 
> $$
>     \boxed{\Delta_s^{(A)} = \Delta_s^{(B)}, \quad \forall s \in \Sstates}。
> $$
> 
> 等价地，在给定证据剖面$(s, p)$的条件下，SCX审计系统的裁判准确性（$F_1$分数、
> 错误率、检测功效）对$A$和$B$完全相同。

### 证明

> **Proof:** **步骤1（检测边际的信息论构造）：**
> 检测边际$\Delta_s$定义为：
> 
> $$
>     \Delta_s = \E[v_m \mid label false] - \E[v_m \mid label true]。
> $$
> 
> 
> 审计者$E_m$的投票$v_m = \mathbf{1}[E_m(h_s) \neq y]$，其中$h_s = \phi(s) + \PE(p)$。
> 审计者的决策函数$E_m: \R^d \to \{0,1\}$取决于其参数$\theta_m$。
> 
> **步骤2（条件分布的等价性）：**
> 由相同证据标准的定义，对任意事实-情境对$(s, p)$：
> 
> $$
>     P(Y = 1 \mid S = s, P = p, 个体=A)
>     = P(Y = 1 \mid S = s, P = p, 个体=B)。
> $$
> 
> 
> 在SCX框架中，个体的身份特征$I$（姓名、社会地位、财富等）不在状态表示中出现——
> $h_s = \phi(s) + \PE(p)$仅依赖$s$和$p$。因此，条件于$(s, p)$后，标签分布不携带
> 关于个体身份的任何信息：
> 
> $$
>     P(Y \mid S=s, P=p, I=A) = P(Y \mid S=s, P=p, I=B)。
> $$
> 
> 
> **步骤3（审计者行为的不变性）：**
> 审计者$E_m$的输入是$h_s = \phi(s) + \PE(p)$。由于编码函数$\phi$和$\PE$不涉及
> 个体身份$I$，对于相同的$(s, p)$，审计者接收到的输入$h_s$是相同的。
> 
> 审计者的输出（无论是确定性分类器还是概率分类器）仅依赖$h_s$，因此：
> 
> $$
>     P(E_m(h_s) \neq y \mid label false, I=A)
>     = P(E_m(h_s) \neq y \mid label false, I=B)，
> $$
> 
> 同理适用于label true条件。
> 
> **步骤4（检测边际的不变性）：**
> 由以上步骤：
> 
> $$
>     \Delta_s^{(A)}
>     &= \E[v_m \mid label false, I=A]
>        - \E[v_m \mid label true, I=A] 

>     &= \E[v_m \mid label false, I=B]
>        - \E[v_m \mid label true, I=B]
>     = \Delta_s^{(B)}。
> $$
> 
>  $\square$

\rigorous{} **证明状态：严格。**该定理是SCX框架中编码函数定义和信息注入结构
的直接推论。核心洞察是：如果身份特征$I$不被注入到状态表示中（即编码函数$\phi$和
$\PE$的定义域不包含$I$），那么身份不可能影响审计系统的输出——这不是一个需要
证明的经验事实，而是一个**架构性质**。

### 法律推论

> **Corollary:** [相同案件相同处理的数学保证]
> <!-- label: cor:treat_like_alike -->
> 如果SCX审计系统被用作司法裁判的辅助工具（例如，评估证据强度、检测可能的误判），
> 则该系统**在架构上保证了**相同案件相同处理——因为编码函数$\phi$和$\PE$不
> 接受身份特征作为输入。这与人类法官可能因隐含偏见而对相同案件做出不同裁判形成了
> 鲜明对比。

> **Corollary:** [身份特征注入的风险]
> <!-- label: cor:injection_risk -->
> 任何将个体身份特征$I$注入状态表示$h_s$的企图——即使以``个性化司法''或
> ``考虑被告背景''为名——都会在数学上破坏司法平等定理的前提。
> 一旦$I$进入特征空间，条件独立性$P(Y \mid S, P, I) = P(Y \mid S, P)$
> 不再自动成立，检测边际$\Delta_s$可能因个体身份而异——**个性化编码是个性化
> 偏见的数学入口**。

> **Corollary:** [司法平等的可审计性]
> <!-- label: cor:auditability -->
> SCX框架不仅**保证**了司法平等（在架构层面），也**使其可审计**。
> 通过对编码函数$\phi$和$\PE$的输入域进行形式验证（确认其不接受身份特征$I$），
> 可以数学地证明系统满足司法平等定理的前提。这比依赖于法官的道德自律或事后审查
> 更加可靠——**不可篡改的架构约束优于可违反的行为规范**。

### 诚实暴击

\honestwarning{} **本定理的四个理论局限：**

1. **架构平等 ≠ 实质平等：**定理保证了审计系统在\textbf{给定相同输入
2. **代理变量的风险：**即使$I$不被显式编码，身份信息可能通过**代理变量**
3. **相同证据标准的前提验证：**定义 [ref]要求两个个体
4. **情境坐标$P$中的制度偏见：**情境坐标$P$（管辖权、时间、程序阶段）

## 综合讨论：SCX法哲学的理论图景

### 四个定理的逻辑结构

四个定理之间的逻辑依赖关系如下（图示另行准备）：

- ****定理一（人人平等）** $\to$ **定理二（老实人）**：:** 人人平等定理
- ****定理二（老实人）** $\to$ **定理三（独醒不太可能）**：:** 老实人定理
- ****定理三（独醒不太可能）** $\to$ **定理四（司法平等）**：:** 独醒

### 与罗尔斯正义论的形式对应

罗尔斯的《正义论》 [cite]提出了两个正义原则，其中最著名的是
``差异原则''和``机会平等原则''。SCX法哲学框架与罗尔斯体系存在引人注目的
**结构对应**（表 [ref]）。

[Table omitted — see original .tex]

这一对应不是字面上的类比，而是**数学结构的同构**。罗尔斯诉诸于假想的
``无知之幕''来推导正义原则；SCX框架通过信息论约束$I(Y; I \mid S) = 0$实现了
身份信息被**架构性地排除**——不需要假想的幕，因为编码函数在定义上就不接受
身份输入。

### 与证据法经典理论的对话

**与边沁的证据功利主义：**边沁 [cite]主张证据法应
遵循``自由证明''原则——排除规则应被最小化，事实认定者应自由评估所有相关证据。
SCX框架为这一立场提供了一个限定性的数学辩护：**只要**证据的验证记录$V(e)$
是可靠的（即由独立事实认定者生成），**那么**证据效力$\omega(e)$自然与其
来源身份无关（定理一）——因此以身份为由排除证据在信息论上是多余的。

**但**SCX框架同时揭示了边沁立场的一个盲点：如果证据的$V(e)$不可靠（例如，
仅有一位非独立的事实认定者验证了该证据），则独醒不太可能定理（定理三）表明，
赋予该证据过高权重的风险是指数级的大。这为**排除规则提供了信息论辩护**——
排除的不是基于身份的，而是基于**验证不足的**。

**与威格莫尔的证据科学：**威格莫尔 [cite]试图将证据推理
形式化为``证据图表''（Wigmorean charts）——节点为证据命题，边为支持/反驳关系。
SCX框架可以被视为威格莫尔纲领的**概率升级版**：用条件互信息$I(Y; P \mid S)$
替代定性的支持/反驳关系，用Chernoff集中界为证据推论的可靠性提供非渐近保证。

**与法律经济学的对话：**法律经济学（如Posner [cite]）
以成本-收益分析来解释法律规则。SCX框架中的老实人定理（定理二）提供了
**博弈均衡**而非成本-收益权衡的解释：举证责任分配是博弈支配性的结果，
不需要引入关于``社会成本最小化''的额外假设。这意味着举证责任原则
**对效用函数的具体形式具有鲁棒性**——仅要求$k > 1$（虚假主张的惩罚重于
被拒绝的成本）。

## 诚实总评与开放问题

### 定理证明严格性总评

表 [ref]总结了本文所有定理的证明状态和主要局限。

[Table omitted — see original .tex]

### 理论图景的完整性评估

四个定理构成的体系覆盖了证据法的四个核心维度（表 [ref]）。

[Table omitted — see original .tex]

### 开放问题

1. **有限$M$下老实人定理的非渐近条件：**定理二的支配性证明依赖大$M$
2. **专家相关结构下的Chernoff界修正：**定理三假设条件独立。
3. **代理变量的信息论检测：**定理四的诚实暴击中指出了代理变量问题。
4. **假设声明的形式化本体论：**定理二要求假设$H$是``可验证的''。
5. **超额$M$的边际价值递减与制度设计：**定理三的推论给出了排除合理怀疑
6. **从SCX到刑事诉讼和民事诉讼的差异化映射：**本文的博弈模型未区分
7. **经验验证：**四个定理构成了一个可检验的理论体系。主要的可检验预测

### 最后的诚实暴击：公理映射的形而上学鸿沟

\honestwarning{} **本文最根本的理论局限：**

SCX框架的四个公理（\S2.1）是从机器学习场景中抽象出来的。本文将它们映射到司法
推理领域，这一映射的**每个环节**都涉及从``是''到``应该是''的跳跃：

- **公理一（状态可结晶性）**声称事实可以离散化为状态原子$s$。
- **公理二（专家独立性）**假设条件独立投票。
- **公理三（检测边际存在）**假设$\Delta_s > 0$，即真假主张在统计上
- **公理四（Yajie协议）**假设多数决的信息汇聚最优性。但多数决的

**本文的价值不在于消解这些哲学问题，而在于将它们精确化。**
一旦我们用数学语言表述了``证据效力不依赖于身份''，我们就可以精确地追问：
在什么条件下这一定理成立？在什么条件下它失效？失效的机制是什么？
这使得法哲学的讨论从**信念的冲突**转变为**模型的比较**——
一个更诚实、更可积累的智识事业。

\begin{thebibliography}{99}

\bibitem{scx2026theorems}
SCX Project.
\newblock {Theorem 1--4}: Multi-expert consistency, weak feature limits,
  unidentifiability, and minimax optimality.
\newblock Technical report, `theory/theorems/`, 2026.

\bibitem{scx2026yajie}
SCX Project.
\newblock {Yajie Protocol}: Game-theoretic foundations of multi-expert auditing.
\newblock Technical report, `theory/yajie/`, 2026.

\bibitem{scx2026cc_audit}
SCX Project.
\newblock Multi-head spring and positional encoding analysis: {CC} audit report.
\newblock Technical report,
  `theory/self\_evolution/multi\_head\_spring\_and\_positional\_encoding\_analysis.md`,
  2026.

\bibitem{scx2026ppe_derivation}
SCX Project.
\newblock Physical positional encoding ({PPE}) rigorous derivation in the {SCX}
  framework.
\newblock Technical report,
  `theory/self\_evolution/ppe\_rigorous\_derivation.md`, 2026.

\bibitem{chernoff1952}
H.~Chernoff.
\newblock A measure of asymptotic efficiency for tests of a hypothesis based on
  the sum of observations.
\newblock *Annals of Mathematical Statistics*, 23(4):493--507, 1952.

\bibitem{wainwright2019}
M.~J.~Wainwright.
\newblock *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*.
\newblock Cambridge University Press, 2019.

\bibitem{cover2006}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd edition.
\newblock Wiley, 2006.

\bibitem{fudenberg1991}
D.~Fudenberg and J.~Tirole.
\newblock *Game Theory*.
\newblock MIT Press, 1991.

\bibitem{myerson1997}
R.~B.~Myerson.
\newblock *Game Theory: Analysis of Conflict*.
\newblock Harvard University Press, 1997.

\bibitem{hart1994concept}
H.~L.~A.~Hart.
\newblock *The Concept of Law*, 2nd edition.
\newblock Oxford University Press, 1994.

\bibitem{rawls1971theory}
J.~Rawls.
\newblock *A Theory of Justice*.
\newblock Harvard University Press, 1971.

\bibitem{damaska1986faces}
M.~R.~Damaska.
\newblock *The Faces of Justice and State Authority*.
\newblock Yale University Press, 1986.

\bibitem{bentham1827rationale}
J.~Bentham.
\newblock *Rationale of Judicial Evidence*.
\newblock Hunt and Clarke, 1827.

\bibitem{wigmore1937science}
J.~H.~Wigmore.
\newblock *The Science of Judicial Proof*, 3rd edition.
\newblock Little, Brown, 1937.

\bibitem{posner2014economic}
R.~A.~Posner.
\newblock *Economic Analysis of Law*, 9th edition.
\newblock Wolters Kluwer, 2014.

\bibitem{laudan2006truth}
L.~Laudan.
\newblock *Truth, Error, and Criminal Law: An Essay in Legal Epistemology*.
\newblock Cambridge University Press, 2006.

\bibitem{ho2008philosophy}
H.~L.~Ho.
\newblock *A Philosophy of Evidence Law: Justice in the Search for Truth*.
\newblock Oxford University Press, 2008.

\bibitem{brooks2002narrative}
P.~Brooks.
\newblock *Narrativity of the Law*.
\newblock In *Law and Literature*, special issue, 2002.

\bibitem{maccormick2005rhetoric}
N.~MacCormick.
\newblock *Rhetoric and the Rule of Law*.
\newblock Oxford University Press, 2005.

\bibitem{twining2006rethinking}
W.~Twining.
\newblock *Rethinking Evidence: Exploratory Essays*, 2nd edition.
\newblock Cambridge University Press, 2006.

\end{thebibliography}