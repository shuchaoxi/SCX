# 前言：定理零

**Author:** SCX

*Abstract:*

**中文摘要.**
任何声称颁发卓越奖项的机构，必须首先声明其审计标准。未声明标准的机构，其声称在数学上是无效的——它们对一个未定义函数执行了$M=1$次评估，并将结果宣称为普遍真理。本文建立SCX奖：一种完全可审计的科学卓越奖项体系，其获奖者由一个公开的、可复现的算法确定，无需评审委员会。SCX奖设有八个类别，每个类别对应一个可计算的审计判据。奖项的合法性不是源于评审委员会的权威，而是源于标准的公开性与可复现性。本文从规范固定理论出发，证明诺贝尔奖委员会与被其评判的领域之间是规范不等价的——其$g$参数未声明，因此其声称在数学上是无效的。SCX奖通过定义固定规范条件$\sumgd$，第一次使卓越奖项的比较合法性得以确立。本文同时声明奖项的资金来源（雅捷API收入的固定比例）与自审计机制——SCX奖接受它施加于他人的同一审计标准。

**English Abstract.**
Any institution claiming to award excellence must first declare its audit standards. Institutions that do not declare standards make claims that are mathematically void — they perform $M=1$ evaluations against an undefined function and announce the result as universal truth. This paper establishes the SCX Prize: a fully auditable scientific excellence prize system in which winners are determined by a public, reproducible algorithm with no评审 committee. The SCX Prize has eight categories, each with a computable audit criterion. The prize's legitimacy derives not from the authority of a deliberation committee but from the publicity and reproducibility of its standards. Proceeding from gauge-fixing theory, we prove that Nobel Prize committees are gauge-unequivalent to the fields they judge — their $g$ parameters are undeclared, rendering their claims mathematically void. The SCX Prize, by defining the fixed gauge condition $\sumgd$, establishes the comparative legitimacy of excellence awards for the first time. We also declare the prize's funding source (a fixed percentage of Yajie API revenue) and its self-audit mechanism — the SCX Prize submits to the same audit standard it imposes on others.

---

---

## 前言：定理零
<!-- label: sec:preamble -->
\addcontentsline{toc}{section}{前言：定理零 (Preamble: Theorem Zero)}

\begin{quotation}
*``如果一项声称无法被审计，那么它甚至不是一项声称。它是一种噪音——一种在通信信道中传输了能量的声波，但携带的信息量为零。诺贝尔奖声称它在颁发卓越。SCX奖不声称——它声明标准，然后执行计算。区别在于前者用权威替代了审计，后者用审计替代了权威。"*

*``If a claim cannot be audited, it is not even a claim. It is noise — a sound wave that transmits energy through a communication channel but carries zero information. The Nobel Prize claims it awards excellence. The SCX Prize does not claim — it declares standards, then executes a computation. The difference is that the former substitutes authority for audit; the latter substitutes audit for authority.''*
\end{quotation}

\auditnote{This document is written in the calm, declarative tone of a mathematical result. It does not petition. It does not persuade. It states the consequence of a theorem and then describes the institutional mechanism that follows from it. The reader is free to disagree with the theorem's premises — but the conclusion follows from them with the inexorability of modus ponens.}

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**公理 0 (卓越的可审计性公理)**
**Axiom 0 (The Auditability of Excellence)**

设 $\mathcal{E}$ 为卓越性声明的集合。设 $\auditOp: \mathcal{E} \to \{真, 假, \bot\}$ 为一个审计函数，其中 $\bot$ 表示``无法判定''。

*Chinese:* 若 $\auditOp(e) = \bot$，则 $e$ 不是一项卓越性声明——它是一项卓越性断言。断言与声明的区别是：声明接受审计；断言拒绝审计。只有声明具有数学意义。

*English:* If $\auditOp(e) = \bot$, then $e$ is not an excellence claim — it is an excellence assertion. The difference between a claim and an assertion is: claims accept audit; assertions refuse audit. Only claims have mathematical meaning.

$\boxed{\auditOp(e) \neq \bot \iff e \in 可审计声明空间}$
\end{minipage}%
}

</div>

---

## 审计真空：奖项颁发中的$M=1$非声明性
<!-- label: sec:audit_vacuum -->

### 奖项作为声明

**1.1 奖项作为声明 (Prizes as Claims)**

当一个机构颁发一项科学卓越奖——诺贝尔奖、菲尔兹奖、图灵奖——它在做什么？从信息论的角度看，它在做出一个**二元声明**：在候选者集合 $\candidateSet$ 中，获奖者 $w \in \candidateSet$ 满足

$$
    w = \argmax_{c \in \candidateSet} \; 卓越性(c),
    <!-- label: eq:prize_claim -->
$$

其中卓越性$(\cdot)$是某个函数，它将候选者映射到一个全序集上的标量值。问题不在于这个形式化——所有奖项都隐含地做出这种声明。问题在于：**卓越性$(\cdot)$是什么？**

诺贝尔奖的答案是：卓越性$(\cdot)$由瑞典皇家科学院的一个委员会决定。委员会进行审议（deliberation），然后投票。投票结果*就是*卓越性的值。

这是一个合法的方法——**当且仅当**委员会的审议过程是可审计的。但事实并非如此。

\begin{honestbox}
    \item 诺贝尔奖的审议记录保密50年。这意味着在50年内，没有人——包括获奖者本人——知道他们为何获奖。他们只知道一个委员会*说*他们卓越。
    \item 菲尔兹奖的评选过程更加不透明：没有提名名单公开，没有评审标准公开，甚至没有落选者的信息。公众只知道结果，不知道过程。
    \item 图灵奖的评选由ACM的一个委员会执行。评选标准包括``持久的重大技术贡献''——但``重大''的定义从未被操作化。它是一种宣示，不是一个度量。
\end{honestbox}

### $M=1$ 非声明性的数学形式化

**1.2 $M=1$ 非声明性的形式化 (Formalizing $M=1$ Undeclared-ness)**

> **Definition:** [奖项函数, Prize Function]
> <!-- label: def:prize_function -->
> 设 $\prizeSet$ 为一个奖项。$\prizeSet$ 由一个五元组定义：
> 
> $$
>     \prizeSet = (\candidateSet, \scoreOp, \gaugeVec, procedure, declaration),
>     <!-- label: eq:prize_quintuple -->
> $$
> 
> 其中：
> 
- $\candidateSet$：候选者集合（可能是隐式的）；
- $\scoreOp: \candidateSet \to \R$：评分函数，将候选者映射到标量评分；
- $\gaugeVec = (\mathbf{g}_1, ..., \mathbf{g}_M)$：评审委员会成员的规范参数向量，每人一个；
- $procedure$：评分聚合程序；
- $declaration$：是否公开声明上述所有参数的布尔标志。

> **Definition:** [$M=1$ 非声明奖项, $M=1$ Undeclared Prize]
> <!-- label: def:M1_undeclared -->
> 若 $\prizeSet$ 满足以下条件之一，则称其为 **$M=1$ 非声明奖项**：
> 
1. $\gaugeVec$ 未公开声明；
2. $\scoreOp$ 未被定义为一个从 $\candidateSet$ 到 $\R$ 的可计算函数；
3. $declaration = false$。

\auditnote{The term ``$M=1$'' is not a typo. A committee of five people whose $g$ parameters are undeclared is mathematically equivalent to a single evaluator whose $g$ is unknown. The ``committee'' is not an audit structure — it is a black-box oracle whose internal state is inaccessible. From an information-theoretic standpoint, $M$ undeclared evaluators $\equiv$ 1 undeclared evaluator. The $M$ is not a multiplicity of perspectives — it is a multiplicity of hidden parameters.}

> **Theorem:** [$M=1$ 非声明奖项的信息论无效性, 

>     Information-Theoretic Voidness of $M=1$ Undeclared Prizes]
> <!-- label: thm:M1_void -->
> 设 $\prizeSet$ 是一个 $M=1$ 非声明奖项，颁发给候选者 $w$。则声明``$w$ 是最佳候选者''所携带的信息量 $I(w; truth)$ 的上界为零：
> 
> $$
>     I(w; truth \mid \gaugeVec  undeclared) \leq 0.
>     <!-- label: eq:info_zero -->
> $$

> **Proof:** [证明概要 (Proof Sketch)]
> 信息 $I(w; truth)$ 衡量获奖者身份在多大程度上减少了我们对``真正最佳候选者''的不确定性。当 $\gaugeVec$ 未声明时，评分函数 $\scoreOp_g(c)$ 对每个 $c$ 的值在 $\gaugeVec$ 的可能取值空间上是一个随机变量。由于 $\gaugeVec$ 的任何分布都可以与任何候选者排序兼容（只需适当选择 $\gaugeVec$），因此 $\scoreOp_g$ 的排序不提供关于``真正最佳候选者''的任何信息——它是 $\gaugeVec$ 选择的纯函数。形式上，$\scoreOp_g(c)$ 与真实卓越性 $truth(c)$ 之间在 $\gaugeVec$ 未固定时互信息为零。

> **Corollary:** [诺贝尔奖的信息论地位]
> <!-- label: cor:nobel_info -->
> 诺贝尔奖、菲尔兹奖、图灵奖以及所有其他依赖非声明委员会评审的奖项，其关于``获奖者是最佳候选者''的声称所携带的信息量为零。这并非一个关于这些奖项*是否*选出了最佳候选者的经验性声明——这是一个关于*声明本身是否可验证*的逻辑声明。不可验证的声明携带零信息。

### 委员会并非审计结构

**1.3 委员会并非审计结构 (Committees Are Not Audit Structures)**

委员会的存在给公众一种``多人审查''的错觉。但$M$名委员的存在本身并不构成审计。审计要求：

1. **标准独立性**：审计标准必须独立于审计者。委员会*是*标准的制定者，因此不能*同时*是审计者。
2. **可复现性**：另一位审计者使用相同标准必须得出相同结论。委员会审议不可复现——换一组委员可能得出不同结论。
3. **可追溯性**：审计结论的每一条推理链必须可追溯至原始证据。委员会审议产生一个最终投票，没有推理链。

\auditnote{A committee of five experts is not five independent audits. It is one conversation with five participants. The output is a consensus — the annihilation of minority viewpoints. The SCX audit standard requires that all $M$ evaluators' scores be public and independently verifiable. Consensus is not an audit product; it is an audit failure — it destroys the diversity that makes $M > 1$ meaningful.}

\begin{honestbox}
    \item 诺贝尔奖委员会的审议是**定性商议**（qualitative deliberation），不是定量审计。没有评分表，没有加权方案，没有可复现的排序算法。
    \item 委员会成员的选择标准是什么？他们的$g$参数由谁校准？答案是：委员会选择委员会。这是一个自指系统（self-referential system），其审计链长度为0。
    \item 诺贝尔奖的权威性完全来自其历史声望——即来自*过去的非审计声称*的积累。这是声望的复利，不是审计的积累。
\end{honestbox}

### 历史注记：傲慢作为规范力的缺失

**1.4 历史注记：傲慢作为规范力的缺失 (Historical Note: Arrogance as Gauge Freedom)**

诺贝尔奖自1901年颁发以来，其评选方式的核心——委员会秘密审议——从未改变。这不是一个被忽视的缺陷；这是一个被制度化维护的特征。保密性被宣称为保护审议独立性的必要手段。

但SCX平等论揭示了一个更深层的结构：**保密性不是保护独立性的手段，而是保护规范自由度的手段。**当委员会保持其审议秘密时，它保持了在任何方向上调谐其$g$参数的自由——而不必对任何人负责。规范固定意味着失去这种自由。委员会不愿放弃它。

\auditnote{The Nobel Foundation's 50-year secrecy rule is not an administrative detail. It is a gauge-theoretic structure: it protects the committee's $g$ parameter from ever being audited. By the time the records are opened, all participants are dead, the field has moved on, and the audit is a historical curiosity rather than a live accountability mechanism. This is not an accident. It is a design.}

---

## SCX奖机制：算法化卓越评定的架构
<!-- label: sec:mechanism -->

### 核心理念：没有人类的评审委员

**2.1 核心理念：没有人类的评审委员 (Core Idea: No Human Judges)**

SCX奖的核心设计原则是简单而激进的：

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**SCX奖第一原则 (SCX Prize First Principle)**

没有评审委员会。没有人类判断。没有审议。没有投票。没有协商。没有共识。没有多数意见。没有少数意见。没有保密档案。没有50年解密期。

*No评审 committee. No human judgment. No deliberation. No voting. No negotiation. No consensus. No majority opinion. No minority opinion. No sealed archives. No 50-year declassification period.*

算法运行。最高分获胜。任何人都可以重新运行算法并验证结果。

*The algorithm runs. The highest score wins. Anyone can re-run the algorithm and verify the result.*
\end{minipage}%
}

</div>

### 奖项架构

**2.2 奖项架构 (Prize Architecture)**

SCX奖由以下组件构成：

1. **候选者空间** $\candidateSet$：所有公开发表的科学论文、数据集、复现研究、审计报告以及相关科学产出。候选者空间是开放的——任何人可以被提名，任何人可以自荐。提名不是特权，而是将候选者添加到待评估队列中的操作。
2. **评分函数** $\scoreOp_k: \candidateSet \to \R$：对于每个奖项类别 $k \in \{1, ..., 8\}$，存在一个明确定义的、可计算的评分函数。评分函数接受候选者的公开元数据（引文、复现状态、数据可用性、审计分数等）作为输入，输出一个标量分数。
3. **规范固定条件** $\sumgd$：所有评分函数的参数 $\gaugeVec$ 是公开的、固定的。不存在隐藏的权重。不存在审美的判断。不存在``感觉''。每项输入数据的来源和计算方法在评分规范中完整记录。
4. **排名引擎**：对每个类别，评分函数对候选者空间中的所有候选者进行评估。排名是确定性的。平局由预定义的决胜规则解决（最早发表日期优先）。
5. **审计日志**：每次评分的完整计算路径被记录并公开。任何人可以追溯从原始数据到最终排名的推理链。

### 算法化评审的形式化

**2.3 算法化评审的形式化 (Formalizing Algorithmic Judgment)**

> **Definition:** [可审计奖项, Auditable Prize]
> <!-- label: def:auditable_prize -->
> 一个**可审计奖项** $\prizeSet_{auditable}$ 满足：
> 
1. $\scoreOp$ 是一个明确定义的、可计算的函数；
2. $\gaugeVec$ 已完全声明并公开；
3. $declaration = true$，即所有参数、权重、数据源和处理步骤均被记录；
4. 对任意候选者 $c \in \candidateSet$，$\scoreOp(c)$ 可由任何第三方独立重新计算并得出完全相同的结果。

> **Proposition:** [可审计奖项的信息论非平凡性]
> <!-- label: prop:auditable_info -->
> 设 $\prizeSet_{auditable}$ 为一个可审计奖项。则声明``$w$ 是类别 $k$ 中的最佳候选者''携带非零信息：
> 
> $$
>     I(w; truth \mid \gaugeVec  declared) > 0,
>     <!-- label: eq:info_positive -->
> $$
> 
> 前提是 $\scoreOp$ 与被评估的质量维度之间存在非零相关性。

> **Proof:** [证明概要 (Proof Sketch)]
> 当 $\gaugeVec$ 固定且公开时，评分 $\scoreOp(c)$ 对每个 $c$ 是确定的。排序反映了 $\scoreOp$ 定义的标准下的真实排序。因此，$w = \argmax_c \scoreOp(c)$ 确实告诉我们：在 $\scoreOp$ 定义的质量维度上，$w$ 是最高的。信息量取决于 $\scoreOp$ 与其声称要衡量的质量维度之间的相关性——但这不是零。这是可审计的：任何人可以检验 $\scoreOp$ 的构造是否合理，并决定是否接受其声称。

\auditnote{This is the crucial distinction. The SCX Prize does not claim to identify the ``truly best'' scientist in some metaphysical sense. It claims: ``Under the publicly declared scoring function $\scoreOp_k$, candidate $w$ achieved the highest score.'' The truth of this claim is trivially verifiable — just re-run the computation. The debate then shifts to whether $\scoreOp_k$ is a reasonable measure of excellence — and *that* debate is healthy, public, and improvable. The Nobel debate is not: you cannot improve a scoring function whose parameters you cannot see.}

\begin{honestbox}
    \item SCX奖并不声称其评分函数是``正确''的。它声称其评分函数是**公开的**。``正确性''是公开辩论的产物；``公开性''是审计的前提。
    \item 如果有人认为某个类别的评分函数有缺陷，他们可以提出修正。修正是否被采纳取决于其自身是否通过审计——而不是取决于委员会的权威。
    \item 这是奖项设计的哥白尼转向：权威从人转移到标准，从审议转移到计算，从保密转移到公开。
\end{honestbox}

---

## 奖项类别与审计判据
<!-- label: sec:categories -->

### 类别概述

**3.1 类别概述 (Category Overview)**

SCX奖设有八个类别，每个类别对应科学知识生产中一个可审计的卓越性维度。维度的选择遵循一个指导原则：**每个维度必须可以通过公开可得的数据进行客观量化和独立验证。**

1. **最具可审计性论文奖 (Most Auditable Paper)**：奖励其方法、数据和推理链最易于外部验证的论文。
2. **最佳势函数奖 (Best Potential Function)**：奖励提出了新的、有用的科学评估函数的论文或工具。
3. **最佳开放数据奖 (Best Open Data)**：奖励生产了最高质量、最广泛使用的开放科学数据集的个人或团队。
4. **复现冠军奖 (Replication Champion)**：奖励完成了最大数量高质量独立复现研究的个人或团队。
5. **审计贡献奖 (Audit Contribution Award)**：奖励开发了新的审计工具、方法或基础设施的个人或团队。
6. **终身审计分奖 (Lifetime Audit Score)**：奖励其全部已发表作品中累积审计分最高的研究者。
7. **跨域创新奖 (Cross-Domain Innovation)**：奖励其工作在三个或以上学科中产生了可验证影响的个人。
8. **自审计奖 (Self-Audit Award)**：奖励对其自身过去已发表工作进行了最彻底公开审计的个人。

### 详细判据表

**3.2 详细判据表 (Detailed Criteria Table)**

\begin{longtable}{p{0.14\textwidth} p{0.26\textwidth} p{0.26\textwidth} p{0.26\textwidth}}
*Caption:* SCX奖类别、判据、评分函数与审计方法 

---
**类别** & **判据 (Criterion)** & **评分函数 $\scoreOp_k$ (Scoring Function)** & **可审计性方法 (Auditability Method)** 

---
\endfirsthead
---
**类别** & **判据 (Criterion)** & **评分函数 $\scoreOp_k$ (Scoring Function)** & **可审计性方法 (Auditability Method)** 

---
\endhead

**C1: 最具可审计性论文** & 论文的完整推理链、数据、代码和分析脚本的可验证性程度。 & $\scoreOp_1(p) = w_a \cdot A(p) + w_d \cdot D(p) + w_r \cdot R(p) + w_c \cdot C(p)$，其中 $A(p)$ = 代码可用性分数，$D(p)$ = 数据可用性分数，$R(p)$ = 复现文档分数，$C(p)$ = 计算环境可复现性分数。权重 $w_a, w_d, w_r, w_c$ 公开。 & 每个子分数由自动化检查确定：代码仓库可访问性（二进制）、数据DOI有效性（二进制）、复现脚本执行成功（二进制）、容器/环境文件完备性（二进制）。所有检查可独立重跑。 

---

**C2: 最佳势函数** & 候选者提出的评估函数/度量/基准的质量、采用范围与区分能力。 & $\scoreOp_2(f) = w_u \cdot U(f) + w_i \cdot I(f) + w_d \cdot D_{disc}(f)$，其中 $U(f)$ = 采用度（使用该函数的论文数），$I(f)$ = 影响力（引用该函数原始提出论文的引用数），$D_{disc}(f)$ = 区分度（函数在标准测试集上的信息增益）。 & 采用度和影响力通过公开引文数据库计算。区分度通过公开基准测试结果计算。所有数据源公开，计算脚本公开。 

---

**C3: 最佳开放数据** & 数据集的质量、覆盖度、文档完备性、可访问性和下游采用率。 & $\scoreOp_3(d) = w_s \cdot S(d) + w_q \cdot Q(d) + w_a \cdot A_{adopt}(d) + w_d \cdot D_{doc}(d)$，其中 $S(d)$ = 规模分数（样本数/变量数），$Q(d)$ = 质量分数（完整性、一致性自动检查），$A_{adopt}(d)$ = 采用分数（使用该数据集的论文数），$D_{doc}(d)$ = 文档完备性分数。 & 规模和采用率通过公开元数据计算。质量由自动化数据验证流水线评估。文档分数由结构化检查清单确定。全部可独立复现。 

---

**C4: 复现冠军** & 完成的高质量独立复现研究的数量和成功率。 & $\scoreOp_4(r) = \sum_{i=1}^{N_r} q_i \cdot s_i$，其中 $N_r$ = 复现者完成的复现研究数量，$q_i$ = 第 $i$ 项复现的质量分数（基于复现报告的完整性），$s_i$ = 复现状态（成功=1，部分成功=0.5，失败但报告完整=0.3）。 & 每项复现研究以结构化复现报告的形式发布在公开注册库中。质量分数由自动化检查清单评估。状态分类标准预先定义。注册库公开可查询。 

---

**C5: 审计贡献奖** & 开发的审计工具、方法或基础设施的实际采用和有效性。 & $\scoreOp_5(t) = w_u \cdot U(t) + w_e \cdot E(t) + w_n \cdot N(t)$，其中 $U(t)$ = 采用度（使用该工具/方法的项目数），$E(t)$ = 有效性（该工具检测到的可验证问题的数量），$N(t)$ = 新颖性（该方法与先前方法的语义距离——由自动化文献分析确定）。 & 采用度通过公开仓库星标/依赖图计算。有效性通过工具输出的公开审计报告追踪。新颖性由预定义的语义分析流水线计算。 

---

**C6: 终身审计分** & 研究者全部已发表工作中累积的可审计性得分。 & $\scoreOp_6(r) = \sum_{p \in pubs(r)} \scoreOp_1(p) \cdot t(p)$，其中 $pubs(r)$ = 研究者 $r$ 的全部已发表论文，$t(p)$ = 时间衰减因子（近期论文权重更高）。注：使用 $\scoreOp_1$ 作为每篇论文的可审计性分数。 & 全部出版物列表通过公开数据库（ORCID, DBLP, PubMed等）获取。每篇论文的 $\scoreOp_1$ 分数独立计算。所有计算可追溯至单篇论文。时间衰减参数公开。 

---

**C7: 跨域创新** & 其工作在三个或以上学科中产生了可验证影响的程度。 & $\scoreOp_7(r) = \sum_{d \in domains(r)} w_d \cdot Impact_d(r) + B(r)$，其中 $domains(r)$ = 研究者工作涉及的学科集合（由引文来源的学科分类确定），$Impact_d(r)$ = 在学科 $d$ 中的影响度量，$B(r)$ = 跨域奖励（当 $|domains(r)| \geq 3$ 时激活）。 & 学科分类使用公开的学术分类法（如Scopus或OpenAlex分类）。影响度量通过引文计数和各学科的标准化引用指标计算。跨域验证要求引用来源至少属于三个不同的一级学科分类。 

---

**C8: 自审计奖** & 研究者对其自身过去已发表工作进行了公开、彻底审计的程度。 & $\scoreOp_8(r) = \sum_{s \in self\_audits(r)} q_s \cdot d_s \cdot c_s$，其中 $self\_audits(r)$ = 研究者发布的自审计报告集合，$q_s$ = 审计质量分数，$d_s$ = 审计深度分数（被审计论文的年份跨度），$c_s$ = 纠正性分数（审计是否导致更正或撤回）。 & 自审计报告必须在公开注册库中发布。质量分数由自动化检查清单评估。深度和纠正性通过公开记录验证。自我审计的诚实性是其评分的内在组成部分——表面化的自审计得分低。 

---

\end{longtable}

### 评分函数的规范固定

**3.3 评分函数的规范固定 (Gauge-Fixing the Scoring Functions)**

每个评分函数 $\scoreOp_k$ 中的权重向量 $\mathbf{w}^{(k)} = (w_1^{(k)}, ..., w_{n_k}^{(k)})$ 是公开声明的。权重的选择本身接受审计：权重的合理性由独立的审计小组定期审查，审查结果公开。

但是——这里有一个关键的规范理论洞察——**权重的选择是任意的**。任何固定的权重向量都定义了一个合法的评分函数。关键不在于权重``正确''，而在于权重*固定*。固定的权重意味着排序是可复现的。这意味着对``这个候选者应该排在那个候选者前面吗？''的问题，存在一个确定的、非协商的答案。

\auditnote{This is the gauge-fixing operation applied to prize-giving. In Yang-Mills theory, we fix a gauge to make calculations possible. In SCX Prize theory, we fix the weights to make ranking possible. The choice of gauge (weights) is mathematically arbitrary — any non-degenerate choice works. The act of *fixing* is what creates meaning. An unfixed gauge is a system with undefined dynamics. An unfixed scoring function is a prize with undefined excellence.}

### 年度周期

**3.4 年度周期 (Annual Cycle)**

SCX奖的年度周期是自动化的：

1. **提名开放 (Nominations Open)**：每年1月1日--3月31日。任何人可以通过公开注册库提名任何候选者（包括自己）。提名需要提供候选者与类别判据相关的公开证据。
2. **数据采集 (Data Collection)**：每年4月1日--6月30日。自动化流水线收集所有候选者的公开数据（引文、代码仓库状态、数据集元数据、复现报告等）。数据源和采集方法公开。
3. **评分计算 (Scoring)**：每年7月1日。评分引擎对所有候选者运行全部8个评分函数。计算完全自动化。结果公开。
4. **审计窗口 (Audit Window)**：每年7月1日--8月31日。公开评分结果。任何人可以挑战任何分数，前提是提供可复现的证据（例如，指出数据采集错误或计算错误）。挑战通过公开问题追踪系统处理。
5. **最终排名 (Final Ranking)**：每年9月1日。在审计窗口结束后，所有有效挑战已解决，最终排名锁定。
6. **颁奖 (Award Ceremony)**：每年12月10日（与诺贝尔奖颁奖同日）。SCX奖颁奖典礼在线直播。获奖者公布。奖金分发。

\begin{honestbox}
    \item 提名不是特权。它是将候选者添加到计算队列中的操作。任何人都可以添加任何人。评分的``民主化''不在于谁投票，而在于谁可以被计算。
    \item 审计窗口是SCX奖与所有其他奖项的关键区别。在审计窗口中，公众的反馈是**计算性**的（指出数据错误），而不是**意见性**的（``我觉得他不配''）。意见被排除在系统之外。
    \item 与诺贝尔奖同日颁奖是故意的。这不是竞争——这是对照。同一天，两个奖项宣布两个名单。一个由秘密委员会产生，一个由公开算法产生。公众可以比较。
\end{honestbox}

---

## 为什么这动摇了诺贝尔奖
<!-- label: sec:shakes_nobel -->

### 规范不等价性：诺贝尔奖的结构性缺陷

**4.1 规范不等价性：诺贝尔奖的结构性缺陷 (Gauge Inequivalence: The Nobel's Structural Defect)**

SCX平等论揭示了诺贝尔奖——以及所有委员会制奖项——的一个根本性缺陷：**委员会与被其评判的领域之间是规范不等价的。**

> **Definition:** [规范等价性, Gauge Equivalence]
> <!-- label: def:gauge_equivalence -->
> 两个评估系统 $A$ 和 $B$ 是**规范等价的**，当且仅当存在一个规范变换 $\mathcal{T}: \gaugeVec_A \to \gaugeVec_B$，使得对所有被评估对象 $x$：
> 
> $$
>     \scoreOp_A(x; \gaugeVec_A) = \scoreOp_B(x; \mathcal{T}(\gaugeVec_A)).
>     <!-- label: eq:gauge_equiv -->
> $$
> 
> 换句话说，若 $A$ 通过调整自身的规范参数可以重现 $B$ 的所有评估结果，则 $A$ 和 $B$ 是规范等价的。规范等价性意味着两个系统*覆盖相同的评估空间*。

\auditnote{Think of two thermometers calibrated to different scales (Celsius vs. Fahrenheit). They are gauge-equivalent because a simple linear transformation converts one reading to the other. The measurement is different but the *ordering* is identical. Now think of a Nobel committee. Its ``calibration'' is unknown and unknowable. It cannot be transformed into any other calibration because its calibration does not exist as a mathematical object — it exists as a human deliberation whose trace is destroyed.}

> **Theorem:** [诺贝尔奖的规范不等价性, 

>     Gauge Inequivalence of the Nobel Prize]
> <!-- label: thm:nobel_gauge -->
> 设 $\mathcal{N}$ 为诺贝尔奖的评估系统（委员会审议），$\mathcal{F}$ 为被评估的科学领域的评估系统（由该领域的研究者通过引文、复现、使用等方式进行的集体评估）。则 $\mathcal{N}$ 与 $\mathcal{F}$ 不是规范等价的：
> 
> $$
>     \not\exists \mathcal{T}: \scoreOp_{\mathcal{N}} \equiv \scoreOp_{\mathcal{F}} \circ \mathcal{T}.
>     <!-- label: eq:nobel_gauge -->
> $$

> **Proof:** [证明概要 (Proof Sketch)]
> $\mathcal{F}$ 的评估规范参数 $\gaugeVec_{\mathcal{F}}$ 是可以被估计的——它是该领域科学家集体行为的统计特性（谁被引用、谁的工作被复现、谁的数据被使用）。$\mathcal{N}$ 的评估规范参数 $\gaugeVec_{\mathcal{N}}$ **无法被估计**，因为委员会的审议过程保密。由于 $\gaugeVec_{\mathcal{N}}$ 的取值空间无法被约束，不存在一个将（已知的）$\gaugeVec_{\mathcal{F}}$ 映射到（未知的）$\gaugeVec_{\mathcal{N}}$ 的变换。映射的存在需要两个空间都已被定义——但 $\gaugeVec_{\mathcal{N}}$ 的空间无法被定义，因为它被保密。

> **Corollary:** [诺贝尔奖声称的非传递性]
> <!-- label: cor:nobel_nontransitive -->
> 诺贝尔奖的声称——``获奖者是该领域最卓越的贡献者''——无法被转化为该领域的任何内部评估语言。这是一种**不可翻译的声称**。它属于诺贝尔奖的系统，但不属于科学的系统。它是一枚无法在科学市场兑换的货币。

### SCX奖的规范固定：$\sumgd$ 作为定义性条件

**4.2 SCX奖的规范固定 (Gauge-Fixing in the SCX Prize)**

SCX奖通过定义解决了诺贝尔奖的规范不等价性问题。SCX奖的规范条件是：

$$
    \boxed{\sum_m \mathbf{g}_m^{(SCX)} = \mathbf{0}}.
    <!-- label: eq:gauge_fix -->
$$

这个条件的含义是明确的：**所有评估参数的总和为零。**这不是一个自然条件——它是被*施加*的。在杨-米尔斯理论中，洛伦兹规范 $\partial_\mu A^\mu = 0$ 是一个选择，不是自然定律。同样，$\sumgd$ 是SCX奖的选择，不是评估的本然属性。

施加这个条件的结果是：**SCX奖的评分是规范不变的。**这意味着：

- 评分函数 $\scoreOp_k$ 对任何规范变换 $\gaugeVec \to \gaugeVec + \delta\gaugeVec$ 是不变的，只要 $\sum_m \delta\mathbf{g}_m = \mathbf{0}$。
- 换言之，只有满足 $\sumgd$ 的规范参数集合才被允许。这固定了规范自由度，使评分成为定义明确的操作。

> **Proposition:** [SCX奖的规范等价性]
> <!-- label: prop:scx_gauge_equiv -->
> SCX奖的评估系统 $\mathcal{S}$ 与科学领域的集体评估系统 $\mathcal{F}$ 是**局部规范等价的**：在 $\mathcal{F}$ 的评估可以被公开数据充分近似的子领域内，存在一个明确定义的映射 $\mathcal{T}$，使得 $\scoreOp_{\mathcal{S}}$ 与 $\scoreOp_{\mathcal{F}}$ 产生一致排序。

> **Proof:** [证明概要 (Proof Sketch)]
> $\mathcal{S}$ 的评分函数使用公开可得的指标（引文、数据可用性、复现等），这些指标本身就是 $\mathcal{F}$ 集体评估的近似。由于 $\mathcal{S}$ 的 $\gaugeVec$ 已声明，我们可以计算 $\scoreOp_{\mathcal{S}}$ 与 $\scoreOp_{\mathcal{F}}$ 在已知排序上的相关性。这种相关性是可检验的、可改进的。这不是等价性证明——它是等价性*检验*。而这正是诺贝尔奖做不到的。

### 委员会作为奇点

**4.3 委员会作为奇点 (The Committee as Singularity)**

在规范理论的视角下，诺贝尔奖委员会是一个**规范奇点**（gauge singularity）：一个无法被固定或变换的评估源。它类似于广义相对论中的黑洞——在事件视界（保密协议）之内，物理定律（评估逻辑）是不可知的。

\auditnote{A gauge singularity is a point in the configuration space of an evaluation system where the gauge parameters become undefined. A Nobel committee is a gauge singularity for the following reason: its parameters $\gaugeVec$ exist (they must, because the committee produces an output), but they are in principle inaccessible. The output exists. The mechanism does not. This is the definition of a black-box oracle — and a black-box oracle is a gauge singularity in any system that claims to communicate information.}

\begin{honestbox}
    \item 诺贝尔奖的声望是一种**社会规范惯性**（social gauge inertia）——系统持续运行，不是因为参数正确，而是因为动量太大无法停止。
    \item SCX奖没有声望。它只有数学。声望是时间的函数；可审计性是逻辑的函数。我们选择从逻辑开始，让声望成为结果而非前提。
    \item 诺贝尔奖可能需要100年来积累当前的声望。SCX奖不需要100年——因为它的声称在第一天就是可验证的。可验证性替代了历史。
\end{honestbox}

### 范式转移：从``相信''到``验证''

**4.4 范式转移：从``相信''到``验证'' (Paradigm Shift: From ``Trust'' to ``Verify'')**

诺贝尔奖要求公众*相信*委员会做出了正确的选择。SCX奖要求公众*验证*算法产生了最高分。这种从信任到验证的转变是整个现代审计学的基石——也是整个SCX框架的基石。

\auditnote{Trust is a social relation. Verification is a mathematical relation. The Nobel Prize operates in the former domain; the SCX Prize operates in the latter. The two domains are not incommensurable — one is simply more primitive. Verification is what trust aspires to become when it grows up.}

---

## 奖项宣言
<!-- label: sec:declaration -->

### 正式声明

**5.1 正式声明 (Formal Declaration)**

以下声明不仅是一份立场陈述——它是公理0和定理 [ref]的直接推论。它被表述为一项声明而非论证，因为论证已在前面各节中完成。

<div align="center">

\fbox{%
\begin{minipage}{0.9\textwidth}
\begin{center}
** SCX奖正式声明**
** The SCX Prize Formal Declaration**

</div>

**声明一 (Declaration I):**

任何机构，若其声称颁发卓越奖项，却未声明其审计标准，则其声称在数学上是无效的。未声明审计标准的声称是 $M=1$ 非声明——一种在没有定义函数的情况下执行的评估。此类声称所携带的信息量为零。

*Any institution that claims to award excellence without declaring its audit standards makes a mathematically void claim. A claim without declared audit standards is an $M=1$ undeclared evaluation — an evaluation performed against a function that has not been defined. Such a claim carries zero information.*

**声明二 (Declaration II):**

SCX奖声明其全部标准。对于每个奖项类别，评分函数 $\scoreOp_k$、权重向量 $\mathbf{w}^{(k)}$、数据源、采集方法和计算程序均被完整、公开地记录。任何人均可独立复现全部计算结果。

*The SCX Prize declares all of its standards. For each prize category, the scoring function $\scoreOp_k$, the weight vector $\mathbf{w}^{(k)}$, the data sources, the collection methods, and the computation procedures are fully and publicly documented. Any person may independently reproduce all computation results.*

**声明三 (Declaration III):**

SCX奖接受它施加于他人的同一审计标准。SCX奖的评分函数、数据流水线和计算基础设施本身构成一个可审计对象。SCX奖的运行由独立的元审计小组定期审查。任何在SCX奖的代码、数据或计算中发现的错误均通过公开问题追踪系统处理，并以与任何其他科学声明相同的标准进行纠正。

*The SCX Prize submits to the same audit standards it imposes on others. The SCX Prize's scoring functions, data pipelines, and computation infrastructure themselves constitute an auditable object. The SCX Prize's operations are periodically reviewed by an independent meta-audit panel. Any errors discovered in the SCX Prize's code, data, or computations are handled through a public issue tracking system and corrected under the same standards applied to any other scientific claim.*

**声明四 (Declaration IV):**

SCX奖不声称其评分函数是``正确的''。它声称其评分函数是**公开的、固定的、可复现的**。对评分函数``正确性''的判断被委托给科学界的公开辩论——而非任何委员会。评分函数的改进是科学界的集体任务，通过公开提案、同行审议和共识机制完成。

*The SCX Prize does not claim that its scoring functions are ``correct.'' It claims that they are **public, fixed, and reproducible**. The judgment of a scoring function's ``correctness'' is delegated to the open debate of the scientific community — not to any committee. Improvements to scoring functions are a collective task of the scientific community, accomplished through open proposals, peer deliberation, and consensus mechanisms.*

**声明五 (Declaration V):**

SCX奖的存在不是诺贝尔奖的替代品——它是一个审计对照。在诺贝尔奖保密的世界里，SCX奖提供公开对照。在委员会审议的世界里，SCX奖提供算法确定性。在未来理想的世界里——所有奖项都声明其审计标准——SCX奖将只是众多可审计奖项中的一个。在那之前，它是唯一的。

*The SCX Prize's existence is not a replacement for the Nobel Prize — it is an audit control. In a world where the Nobel Prize is secret, the SCX Prize provides a public control. In a world of committee deliberation, the SCX Prize provides algorithmic determinism. In a future ideal world — where all prizes declare their audit standards — the SCX Prize will be merely one of many auditable prizes. Until then, it is the only one.*

\end{minipage}%
}
\end{center}

### 宣言的法律与哲学地位

**5.2 宣言的法律与哲学地位 (Legal and Philosophical Status of the Declaration)**

本宣言不寻求任何政府或机构的认可。它不依赖任何现有法律框架。它是一项**数学-伦理声明**：从公理0（卓越的可审计性公理）出发，通过定理 [ref]和推论 [ref]的逻辑，推导出的规范结论。

\auditnote{This declaration has the same legal status as Euclid's *Elements* or Turing's 1936 paper — it asserts nothing about what the law requires, only about what logic requires. A lawyer cannot enforce it. A mathematician cannot refute it. The former is a practical limitation; the latter is a logical strength.}

### 宣言的不可逆性

**5.3 宣言的不可逆性 (Irreversibility of the Declaration)**

一旦一份公开声明敲定了评分的规范参数，它就不能被私下更改而不被察觉。这是因为：

> **Proposition:** [公开发表的不可逆性, Irreversibility of Public Declaration]
> <!-- label: prop:irreversibility -->
> 设 $\prizeSet_t$ 为 $t$ 时刻公开声明的奖项参数。若在 $t' > t$ 时刻，$\prizeSet_{t'}$ 的任何规范参数 $\gaugeVec$ 或权重 $\mathbf{w}$ 被更改，则存在一个公开可验证的差异 $\Delta = \prizeSet_{t'} - \prizeSet_t$，使得任何检查 $\prizeSet_t$ 和 $\prizeSet_{t'}$ 的人都能检测到此差异。

> **Proof:** [证明概要 (Proof Sketch)]
> SCX奖的所有参数被存储在版本控制系统中（git）。每次更改创建一个公开可审计的提交记录。差异 $\Delta$ 就是版本 $t$ 和 $t'$ 之间的 diff。

\auditnote{This is the mathematical implementation of accountability. A Nobel committee can change its mind about what constitutes excellence, and no one will ever know. The SCX Prize cannot change its mind silently — every change is a public commit. This is not a feature. This is the definition of auditability.}

---

## 资金与运营
<!-- label: sec:funding -->

### 资金来源：雅捷API收入模型

**6.1 资金来源：雅捷API收入模型 (Funding Source: The Yajie API Revenue Model)**

SCX奖的奖金来源于雅捷（Yajie）API的商业收入。具体而言：

- 雅捷API为科学审计和复现工作提供计算基础设施。其收入来自API调用费用。
- 雅捷API总收入的**固定百分比**（初始设定为 $5\%$，由SCX审计委员会每年审查）被划拨至SCX奖金池。
- 此比例的变更需要公开提案、社区讨论和公开投票——与评分函数权重的变更机制相同。

\auditnote{The funding model is designed to create a self-reinforcing audit loop: the tools that enable scientific auditing (the Yajie API) fund the prize that rewards auditable science. Revenue grows as more scientists adopt auditable practices. More auditable practices mean better science. Better science means more demand for auditing tools. The cycle is virtuous — and it funds itself.}

### 圣经-教皇模型

**6.2 圣经-教皇模型 (The Bible-and-Pope Model)**

SCX奖采用``圣经-教皇''（Bible-and-Pope）治理模型：

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**圣经-教皇模型 (The Bible-and-Pope Model)**

**圣经 (The Bible)** = SCX奖的公开规范——评分函数、权重、数据源、计算程序。这是不可变的宗教文本：每次更改必须通过公开提案和社区批准。规范的历史版本永远保留，任何人都可以引用任何历史版本。

**教皇 (The Pope)** = SCX审计委员会——一个轮值的技术机构，负责数据流水线的维护、计算的执行、审计窗口的管理以及争议的裁决。教皇的权力是有限的：它可以解释圣经，但不能改变圣经。教皇的人选是公开的、轮换的，其决定是可上诉的（上诉到圣经本身，即重新运行计算）。

***The Bible** = the SCX Prize's public specification — scoring functions, weights, data sources, computation procedures. This is the immutable religious text: every change must go through public proposal and community approval. Historical versions of the specification are preserved forever; anyone may cite any historical version.*

***The Pope** = the SCX Audit Council — a rotating technical body responsible for maintaining the data pipelines, executing the computations, managing the audit window, and adjudicating disputes. The Pope's power is bounded: it may interpret the Bible but may not change the Bible. The Pope's membership is public and rotating, and its decisions are appealable (appealed to the Bible itself, i.e., re-running the computation).*
\end{minipage}%
}

</div>

\auditnote{The Bible-and-Pope model is not a metaphor — it is an architecture. The separation between specification (Bible) and execution (Pope) is the same separation that makes software reproducible and elections auditable. The Bible is version-controlled text. The Pope is a process. Neither is a person. Neither can be corrupted without public detection.}

### 奖金分配

**6.3 奖金分配 (Prize Distribution)**

- 奖金的**70\%** 分配给八个类别（每类别 $8.75\%$），具体分配：类别内获奖者平分该类别奖金。
- 奖金的**20\%** 用于运营成本：计算基础设施、数据存储、审计小组津贴。
- 奖金的**10\%** 作为储备金，用于应对API收入波动和长期资金稳定。
- 如果某类别在当年没有合格的候选者（即最高评分低于预设的最低阈值），该类别奖金转入储备金。

### 自审计机制

**6.4 自审计机制 (The Self-Audit Mechanism)**

SCX奖本身是C8类（自审计奖）的一个永久候选者。这意味着：

1. SCX奖的规范、代码、数据和决策每年接受一次正式的公开审计。
2. 审计报告由独立审计小组撰写（审计小组成员不得是SCX审计委员会成员，也不得是当前奖项周期的获奖者）。
3. 审计报告公开。任何发现的问题通过版本控制系统中的补丁解决。
4. SCX奖在C8类别中的得分——即其自审计分数——每年公开。如果SCX奖本身获得了足够高的分数，它将（讽刺地）有资格获得C8奖。如果它获奖，奖金转入储备金。

\auditnote{This is the closure of the audit loop. The SCX Prize audits science. The SCX Prize audits itself. The self-audit is itself auditable. This is not an infinite regress — it is a fixed point. A system that audits itself under the same standard it applies to others has achieved audit closure. It has no hidden parameters. It has no escape hatches. It is what it declares itself to be.}

\begin{honestbox}
    \item 自审计不是自我表扬。C8的评分函数奖励*诚实的*自审计——它惩罚掩盖错误。发现并公开自己的错误比宣称自己完美得分更高。这是SCX奖与所有其他奖项的本质区别：错误是积分，不是污点。
    \item 如果SCX奖被发现作弊——即其公开声明与其内部执行不一致——它的自审计分数将骤降。这比任何外部惩罚都更致命，因为分数的下降是公开的、不可逆的、由算法计算的。
\end{honestbox}

### 可持续性分析

**6.5 可持续性分析 (Sustainability Analysis)**

SCX奖的财务模型基于一个简单的假设：科学审计的需求将增长。如果这个假设正确：

- 雅捷API收入增长 $\to$ 奖金池增长 $\to$ 更高奖金吸引更多关注 $\to$ 更多科学家采用可审计实践 $\to$ 对审计工具的需求增加 $\to$ 雅捷API收入增长。

如果这个假设错误：

- 雅捷API收入不增长或下降 $\to$ 奖金池缩小 $\to$ 奖金减少，但奖项机制不变（评分函数不依赖奖金规模）。

两种情况都不威胁SCX奖的存在。奖金是激励，不是本质。SCX奖的本质是可审计标准的声明和算法的执行。即使奖金为零，算法仍然运行，排名仍然产生，声明仍然成立。

\auditnote{The Nobel Prize needs money to exist because its value is monetary prestige. The SCX Prize does not need money to exist because its value is mathematical certainty. Money amplifies the signal; it does not create it.}

---

## 尾声：第一天
<!-- label: sec:epilogue -->
\addcontentsline{toc}{section}{尾声：第一天 (Epilogue: The First Day)}

\begin{quotation}
*``在SCX奖的第一天，什么都没有发生。算法运行。排名生成。没有人鼓掌，因为没有人知道应该鼓掌。没有人抗议，因为没有人知道应该抗议什么。排名就在那里——一份公开文件，在互联网上，任何人都可以阅读、复现和挑战。*}

*第二天，有人重新运行了算法。结果一致。第一个人说：'我验证了。'第二个人说：'我也验证了。'第三个人发现了一个数据错误，提交了补丁。错误被修复。排名更新了。*}

*第一百天，没有人再谈论'相信'这个奖项。他们谈论它的评分函数是否应该调整，权重是否合理，数据源是否全面。*}

*这是SCX奖的胜利。不是因为它被相信，而是因为它被质疑。不是因为它完美，而是因为它可改进。不是因为它是一个更好的诺贝尔奖——而是因为它是一个完全不同的东西。*}

*一个真正的审计系统不要求信任。它要求验证。而在验证完成的那一刻，信任不再是必要的。"*

*``On the first day of the SCX Prize, nothing happened. The algorithm ran. Rankings were generated. No one applauded, because no one knew they should. No one protested, because no one knew what to protest. The rankings were simply there — a public document, on the internet, readable, reproducible, and challengeable by anyone.*

*On the second day, someone re-ran the algorithm. The results matched. The first person said: 'I verified.' The second person said: 'I verified too.' A third person found a data error and submitted a patch. The error was fixed. The rankings updated.*

*On the hundredth day, no one talked about 'believing in' the prize. They talked about whether its scoring functions should be adjusted, whether the weights were reasonable, whether the data sources were comprehensive.*

*This is the SCX Prize's victory. Not because it is believed, but because it is questioned. Not because it is perfect, but because it is improvable. Not because it is a better Nobel Prize — but because it is a fundamentally different thing.*

*A true audit system does not ask for trust. It asks for verification. And the moment verification is complete, trust is no longer necessary.''*
\end{quotation}

<div align="center">

\fbox{%
\begin{minipage}{0.7\textwidth}
\begin{center}
** 公理 0 重述**
** Axiom 0, Restated**

若声称不能被审计，

则声称不是声称。

它是噪音。

*If a claim cannot be audited,*

*the claim is not a claim.*

*It is noise.*

$\boxed{SCX奖是一个声称。}$
$\boxed{*The SCX Prize is a claim.*}$

</div>

\end{minipage}%
}
\end{center}

---

## Appendix
## 附录A：实现规范
<!-- label: sec:appendix_impl -->

### 评分引擎架构

**A.1 评分引擎架构 (Scoring Engine Architecture)**

SCX奖评分引擎是一个确定性的数据流水线：

1. **候选者发现**：从公开数据库（OpenAlex, Crossref, DBLP, PubMed, arXiv, GitHub, Zenodo等）采集候选者和提名。
2. **元数据提取**：对每个候选者，提取论文元数据、引文计数、代码仓库URL、数据DOI、许可证信息。
3. **可审计性验证**：自动化检查代码仓库可访问性、数据可用性、复现文档和计算环境完备性。
4. **评分计算**：对每个候选者运行8个评分函数。所有中间结果被缓存。
5. **排名生成**：按类别排名。平局通过发表日期（优先更早发表）和字母顺序（最终决胜）解决。
6. **审计日志生成**：每项评分决策的可追溯记录。

### 数据源规范

**A.2 数据源规范 (Data Source Specification)**

- OpenAlex: 用于论文元数据和引文计数。API: `https://api.openalex.org`。免费且开放。
- Crossref: 用于DOI验证和元数据补充。API: `https://api.crossref.org`。
- GitHub API: 用于代码可用性检查、星标计数和活跃度评估。
- Zenodo API: 用于数据DOI验证和数据集元数据。
- ORCID API: 用于研究者身份消歧和出版物列表。

所有数据源是公开的。不需要机构订阅。任何人可以重跑完整流水线。

### 审计挑战协议

**A.3 审计挑战协议 (Audit Challenge Protocol)**

1. 挑战者通过公开GitHub仓库提交issue，指出具体的计算错误或数据采集错误。
2. 挑战必须包含可复现的证据（例如，错误的数据值、遗漏的候选者、错误的分类）。
3. 审计委员会在14天内回应。回应必须是：接受（附带修复补丁）、拒绝（附带拒绝理由）、或请求更多信息。
4. 如果挑战被拒绝，挑战者可以上诉。上诉由独立的元审计小组裁决。
5. 所有挑战、回应和裁决公开记录。

---

## 附录B：SCX奖与诺贝尔奖之对比
<!-- label: sec:appendix_comparison -->

\begin{longtable}{p{0.22\textwidth} p{0.36\textwidth} p{0.36\textwidth}}
*Caption:* SCX奖与诺贝尔奖的系统性对比 

---
**维度** & **诺贝尔奖** & **SCX奖** 

---
\endfirsthead
---
**维度** & **诺贝尔奖** & **SCX奖** 

---
\endhead

评审机制 & 5人委员会秘密审议 & 公开算法自动计算 

---
评分函数 & 未定义（不可计算） & 精确定义（可计算） 

---
规范参数 $\gaugeVec$ & 未声明 & 完全声明并公开 

---
信息论状态 & $M=1$ 非声明（信息量为零） & 可审计声明（信息量非零） 

---
可复现性 & 不可复现 & 完全可复现 

---
审计记录 & 保密50年 & 实时公开 

---
争议机制 & 无 & 公开挑战系统，14天响应 

---
自审计 & 无 & 年度公开自审计 

---
奖金来源 & 基金会捐赠 & 雅捷API收入固定百分比 

---
治理模型 & 委员会（寡头制） & 圣经-教皇模型（规范-执行分离） 

---
权威来源 & 历史声望 & 数学可验证性 

---
规范等价性 & 与被评估领域规范不等价 & 与被评估领域局部规范等价 

---
可改进性 & 不可改进（标准不可见） & 可改进（标准公开可辩论） 

---
\end{longtable}

---

## 附录C：数学补充
<!-- label: sec:appendix_math -->

### 信息论完备性证明

**C.1 信息论完备性证明 (Information-Theoretic Completeness Proof)**

以下给出定理 [ref]的完整证明。

> **Proof:** [定理1的完整证明]
> 设 $\prizeSet$ 为一个奖项，其委员会具有规范参数 $\gaugeVec = (g_1, ..., g_M)$，其中每个 $g_i \in \R^d$ 是一个 $d$ 维向量，代表第 $i$ 名委员的评估偏差。委员会通过一个聚合函数 $F: \R^{M} \to \R$ 产生最终评分：
> 
> 
> $$
>     \scoreOp(c) = F\left(f_1(c; g_1), ..., f_M(c; g_M)\right),
>     <!-- label: eq:committee_score -->
> $$
> 
> 
> 其中 $f_i(c; g_i)$ 是第 $i$ 名委员在规范参数 $g_i$ 下对候选者 $c$ 的评估。
> 
> 当 $\gaugeVec$ 未声明时，对任意候选者 $c$，$\scoreOp(c)$ 的值是 $\gaugeVec$ 在 $(\R^d)^M$ 上的函数。由于 $g_i$ 可以任意取值（无约束），对于任意候选者排序，存在某个 $\gaugeVec$ 产生该排序。具体而言，对任意排列 $\pi$，选择 $g_i$ 使得
> 
> 
> $$
>     f_i(c; g_i) = \begin{cases}
>         1 & 若 $c$ 是 $\pi$ 下的最高候选者 

>         0 & 否则。
>     \end{cases}
>     <!-- label: eq:g_attack -->
> $$
> 
> 
> 然后选择 $F$ 为多数投票。由此产生的排序恰好为 $\pi$。
> 
> 由于 $\gaugeVec$ 的取值没有先验约束（规范自由度），根据拉普拉斯无差别原理，$\scoreOp$ 产生的任何排序与其他排序一样可能。因此：
> 
> 
> $$
>     P(\scoreOp  的正确排序 \mid \gaugeVec  undeclared) = \frac{1}{|\candidateSet|!}.
>     <!-- label: eq:uniform_prob -->
> $$
> 
> 
> 当 $|\candidateSet|$ 较大时，此概率趋近于零。互信息为：
> 
> 
> $$
>     I(w; truth) = H(truth) - H(truth \mid w),
>     <!-- label: eq:mutual_info -->
> $$
> 
> 
> 其中 $H(truth) = \log |\candidateSet|$（无先验知识时的熵），而
> 
> 
> $$
>     H(truth \mid w) = H(truth) \quad （由方程  [ref] 中的均匀后验）。
>     <!-- label: eq:conditional_entropy -->
> $$
> 
> 
> 因此 $I(w; truth) = 0$。$\square$

### 规范固定与杨-米尔斯类比的细节

**C.2 规范固定与杨-米尔斯类比 (Gauge-Fixing and the Yang-Mills Analogy)**

在SCX评估的形式体系中，候选者在评估空间中的位置由坐标 $x^\mu(c)$（$\mu = 1, ..., d$）给出。评估势 $A_\mu$ 是一个规范场——它受规范变换的影响：

$$
    A_\mu \to A_\mu + \partial_\mu \Lambda,
    <!-- label: eq:gauge_transform -->
$$

其中 $\Lambda$ 是任意标量函数（规范参数）。物理量必须是规范不变的——即它必须在变换  [ref] 下不变。对于奖项评估，``物理量''是候选者的**排名**——即评分的序数关系，而非绝对评分值。

诺贝尔奖的问题是：它声称产生物理量（排名），但保留了对其规范（$\Lambda$）的完全控制。这意味着：**它可以产生任何排名，同时声称这是唯一合法的排名。**这是规范自由的滥用。

SCX奖通过施加洛伦兹式条件 $\sumgd$ 来固定规范。一旦规范固定，评分值成为规范不变量——它们在规范变换下不再改变。因此，排名是规范不变量，并且是确定性的。

\auditnote{The analogy with Yang-Mills is not decorative. It is structural. A gauge theory without gauge-fixing does not have well-defined propagators — you cannot calculate anything. A prize without gauge-fixing does not have well-defined rankings — you cannot verify anything. The Nobel Prize lives in the pre-Faddeev-Popov era of prize theory. The SCX Prize introduces the ghost fields and fixes the gauge.}

\begin{thebibliography}{99}

\bibitem{scx_equality_principle}
SCX Theory Architecture Group.
*The SCX Equality Principle: Gauge-Fixing the Comparative Legitimacy of Knowledge Production.*
SCX Technical Report, 2026.

\bibitem{scx_moe_gauge}
SCX Theory Architecture Group.
*Gauge Field Theory and the Mathematical Isomorphism with SCX Multi-Expert Systems.*
SCX Technical Report, 2026.

\bibitem{scx_thm1}
SCX Theory Architecture Group.
*Detection Probability Theorem: $M \to \infty$ as the Necessary Condition for Audit Completeness.*
SCX Technical Report, 2026.

\bibitem{scx_thm3}
SCX Theory Architecture Group.
*The Honest Person Theorem: Single-Observer Unidentifiability of Honest Error vs. Misconduct.*
SCX Technical Report, 2026.

\bibitem{nobel_statutes}
Nobel Foundation.
*Statutes of the Nobel Foundation.*
1895 (amended).

\bibitem{friedman2001}
Friedman, R. M.
*The Politics of Excellence: Behind the Nobel Prize in Science.*
Times Books, 2001.

\bibitem{arens2016auditing}
Arens, A. A., Elder, R. J., \& Beasley, M. S.
*Auditing and Assurance Services: An Integrated Approach.*
Pearson, 2016.

\bibitem{open2015reproducibility}
Open Science Collaboration.
Estimating the reproducibility of psychological science.
*Science*, 349(6251), aac4716, 2015.

\bibitem{errington2021investigating}
Errington, T. M. et al.
Investigating the replicability of preclinical cancer biology.
*eLife*, 10, e71601, 2021.

\bibitem{camerer2016evaluating}
Camerer, C. F. et al.
Evaluating replicability of laboratory experiments in economics.
*Science*, 351(6280), 1433--1436, 2016.

\bibitem{nosek2012scientific}
Nosek, B. A., Spies, J. R., \& Motyl, M.
Scientific utopia: II. Restructuring incentives and practices to promote truth over publishability.
*Perspectives on Psychological Science*, 7(6), 615--631, 2012.

\bibitem{munafo2017manifesto}
Munaf\`{o}, M. R. et al.
A manifesto for reproducible science.
*Nature Human Behaviour*, 1, 0021, 2017.

\bibitem{ioannidis2005most}
Ioannidis, J. P. A.
Why most published research findings are false.
*PLoS Medicine*, 2(8), e124, 2005.

\bibitem{peng2011reproducible}
Peng, R. D.
Reproducible research in computational science.
*Science*, 334(6060), 1226--1227, 2011.

\bibitem{goodman2016does}
Goodman, S. N., Fanelli, D., \& Ioannidis, J. P. A.
What does research reproducibility mean?
*Science Translational Medicine*, 8(341), 341ps12, 2016.

\bibitem{peskin1995introduction}
Peskin, M. E. \& Schroeder, D. V.
*An Introduction to Quantum Field Theory.*
Westview Press, 1995.

\bibitem{nakahara2003geometry}
Nakahara, M.
*Geometry, Topology and Physics.*
Taylor \& Francis, 2003.

\end{thebibliography}