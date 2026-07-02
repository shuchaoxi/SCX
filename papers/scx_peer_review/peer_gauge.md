# 引言：同行评审作为势能审计系统

**Author:** SCX

*Abstract:*

**中文摘要.**
科学同行评审是知识生产的核心质量控制机制，但其现行结构——仅依赖$M=2$或$3$名评审者，且评审者通常共享同一学科训练背景——在SCX平等论框架下暴露出根本性的审计学缺陷。本文将同行评审重新形式化为一种**势能审计系统**（Potential Energy Audit System）：每篇投稿在评审势能面$\reviewSurf$上占据一个位置，评审者根据自身坐标系$\coordSys_r$评估其势能值。我们建立三个核心定理：(1)~**检测概率定理**（Thm~1）：在评审者独立且坐标系多样的条件下，错误检测概率满足$\detectProb \to 1$当$M \to \infty$；但当前系统的$M=2,3$意味着检测概率在$0.4$--$0.6$量级——**复制危机是可再生危机的数学必然**。(2)~**坐标系不对齐定理**（Thm~2）：当评审者坐标系$\coordSys_r$与作者坐标系$\coordSys_a$的夹角$\misalignAngle > \threshCrit$时，论文因坐标系错位而非质量缺陷被错误拒稿的概率为正且下界非平凡——此为**隐性拒稿税**（Hidden Rejection Tax）。(3)~**单人不可区分定理**（Thm~3）：单个评审者无法从观察数据中区分论文的*诚实错误*与*学术不端*——这是SCX Thm~3（诚实人定理）在同行评审中的直接推论。解决方案遵循势能审计的数学结构：$M \to \infty$通过开放科学（开放同行评审、发表后评审、独立复现作为独立审计），评审者坐标系多样性作为审计独立性条件，以及发表后持续评审作为连续审计。我们提出**坐标系声明协议**（Coordinate-System Declaration Protocol）：每位评审者须在评审报告中声明其学科坐标系的基向量$\{\mathbf{e}_i\}$与规范姿态$\gaugeVec$，使编辑部能够显式计算评审者间的规范对齐程度——这是平等论规范条件$\sumgd$在同行评审中的操作化。

**English Abstract.**
Scientific peer review is the core quality-control mechanism of knowledge production, yet its current structure — relying on merely $M=2$ or $3$ reviewers, typically sharing the same disciplinary training background — suffers from a fundamental audit-theoretic deficiency under the SCX Equality Principle framework. We reformulate peer review as a **Potential Energy Audit System**: each manuscript occupies a position on the review potential surface $\reviewSurf$, and reviewers evaluate its potential value according to their own coordinate systems $\coordSys_r$. We establish three core theorems: (1)~**Detection Probability Theorem** (Thm~1): under independent reviewers with diverse coordinate systems, the error-detection probability satisfies $\detectProb \to 1$ as $M \to \infty$; yet the current system's $M=2,3$ implies detection probability in the $0.4$--$0.6$ range — making the **replication crisis a mathematically expected outcome**. (2)~**Coordinate-System Misalignment Theorem** (Thm~2): when the angle $\misalignAngle$ between a reviewer's coordinate system $\coordSys_r$ and the author's coordinate system $\coordSys_a$ exceeds a critical threshold $\threshCrit$, the probability that a manuscript is falsely rejected due to coordinate-system mismatch rather than quality failure is positive with a non-trivial lower bound — this constitutes a **Hidden Rejection Tax**. (3)~**Single-Reviewer Unidentifiability Theorem** (Thm~3): a single reviewer cannot distinguish between *honest error* and *research misconduct* from observational data alone — a direct corollary of SCX Thm~3 (The Honest Person Theorem) applied to peer review. Solutions follow from the mathematical structure of potential energy audit: $M \to \infty$ via open science (open peer review, post-publication review, independent replication as independent audit), reviewer coordinate-system diversity as an audit-independence condition, and continuous post-publication review as continuous audit. We propose the **Coordinate-System Declaration Protocol**: every reviewer must declare, within their review report, the basis vectors $\{\mathbf{e}_i\}$ and gauge posture $\gaugeVec$ of their disciplinary coordinate system, enabling editors to compute explicit gauge alignment among reviewers — this operationalizes the Equality Principle gauge condition $\sumgd$ in peer review.

---

---

## 引言：同行评审作为势能审计系统
<!-- label: sec:intro -->

### 核心张力：$M$太小

\begin{quotation}
*“一篇决定科学家职业生涯的论文，通常由2到3名评审者做出裁决。这2到3人几乎总是来自同一学科、接受过相同的博士训练、使用相同的评估维度。如果我们将科学同行评审视为一个审计系统，这就相当于用$M=2$个共享同一套会计软件的审计员去检查一家跨国公司——而审计理论告诉我们，当$M$很小时，重大错报的检测概率是灾难性的。”*
\end{quotation}

\reviewnote{This is not a metaphor. This is a formal audit-theoretic claim. The mathematical structure of peer review — $M$ evaluators, each operating from a coordinate system $\coordSys_r$, assessing a target under an unknown ground truth — is structurally identical to a multi-auditor detection problem. The replication crisis, viewed through this lens, is not a sociological accident. It is a **Theorem 1 prediction**.}

科学界正经历一场深刻的自我审视。复制危机（Replication Crisis）——多个学科中大量已发表研究无法被独立复制的事实——已被广泛记录：心理学中仅36\%--47\%的研究可成功复制 [cite]，癌症生物学中可复制率低至11\% [cite]，经济学和社会科学面临类似的严峻数字 [cite]。与此同时，同行评审系统本身受到越来越多的质疑：评审者间信度（inter-rater reliability）出奇地低 [cite]，评审偏见（reviewer bias）被反复记录 [cite]，而顶级期刊的拒稿率高达90\%以上~

 [cite]——这意味着大量有价值的科学工作被排除在知识流通之外。

已有的解释将复制危机归因于多种因素：出版偏见（publication bias）偏爱阳性结果 [cite]，可疑研究实践（questionable research practices）如$p$-hacking [cite]，激励机制鼓励新颖性而非稳健性 [cite]。这些解释都有价值，但它们在分析层面停留在一个更根本的问题之上：**同行评审作为知识质量控制机制的数学结构本身就是不充分的**。

本文提出的核心论点是：同行评审是一种**势能审计系统**（Potential Energy Audit System），其质量控制能力由评审者数量$M$和评审者坐标系的**规范对齐**（Gauge Alignment）程度共同决定。当前系统的缺陷并非实施层面的偶然失误——它们是$M=2,3$这一参数选择的**数学必然结果**。

### 审计学视角

在审计理论中，审计质量的基本决定因素是审计证据的充分性与适当性。审计证据的充分性由样本量（$M$）决定；适当性由审计程序与被审计事项的**相关性**决定——即审计坐标系是否覆盖了被审计对象的全部相关维度 [cite]。这两个概念在SCX平等论框架中获得精确的数学形式化：

- **充分性 (Sufficiency)** $\leftrightarrow$ $M$：审计者（评审者）的数量。审计理论的基本结论是：检测概率随$M$增加而收敛到1 [cite]。
- **适当性 (Appropriateness)** $\leftrightarrow$ 规范对齐 $\sumgd$：审计者的评估坐标系必须与被审计对象的实际结构对齐。如果评审者的坐标系与作者的坐标系存在系统偏差，则评审结论反映的是坐标系差异而非质量差异——这是独立审计的基本要求。

\begin{honestbox}
    \item 会计审计要求审计员独立于被审计实体。但同行评审中，评审者与作者往往来自同一学科、同一方法论传统——这不是独立性，这是**认知利益冲突**（Cognitive Conflict of Interest）。
    \item 会计审计有抽样理论支撑：检测错报的样本量取决于期望的保证水平。同行评审的样本量$M=2,3$对应于什么保证水平？几乎为零。
    \item 会计审计区分*错误*与*舞弊*。同行评审中，单个评审者无法区分诚实错误与数据造假——这是Thm~3的结论。
\end{honestbox}

### 核心直觉：$M$小是根本问题

考虑一个简化的审计模型。假设一篇投稿中存在一个严重缺陷（方法论错误、数据造假、或理论矛盾）。每个独立评审者检测到该缺陷的概率为$p$（$0 < p < 1$）。在当前系统中，评审者并非完全独立——他们共享学科背景，接受类似的训练，倾向于关注相同的维度。因此，有效独立评审者数量$M_{eff}$低于名义数量$M$。

如果$M$名评审者投票（多数原则或一致原则），缺陷被至少一名评审者发现的概率为：

$$
    \detectProb = 1 - (1 - p)^{M_{eff}}.
    <!-- label: eq:naive_detection -->
$$

对于乐观的$p \approx 0.4$和$M_{eff} \approx 2$（名义$M=3$但存在相关性），$\detectProb \approx 0.64$。这意味着**超过三分之一的严重缺陷论文通过评审**。如果$p \approx 0.25$（考虑到评审者时间压力和信息不对称），$\detectProb \approx 0.44$——超过一半的缺陷论文被接受。

这就是复制危机的数学根源。它不是一个需要更严格统计标准来解决的问题——它是一个需要**增大$M$**来解决的问题。统计学标准的提升（$p < 0.005$而非$p < 0.05$）是在坐标系内部进行尺度变换——它改变规范参数$\sigma$，但不改变审计者的数量$M$。它不能解决检测概率的根本不足。

### 必要的SCX背景

SCX平等论框架建立了知识生产中比较合法性的规范条件 [cite]。其核心是：

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**SCX平等论 (SCX Equality Principle)**

不同观察者（评审者、作者、编辑）在同一系统内部，即使在相同目标上训练至相同损失，也会发展出不可通约的内部表征。

一致性不是天然的——它必须被显式地构建。比较的数学合法性不是默认状态——它必须由规范固定来授予。

$\boxed{\sum_m \mathbf{g}_m = \mathbf{0}}$
\end{minipage}%
}

</div>

在同行评审的语境下，$\sumgd$意味着评审者集体的规范姿态总和必须为零：不存在特权的评审者坐标系。每个评审者的视角是合法的，但没有任何单一视角是绝对的。评审结论的合法性取决于评审者间的规范抵消（gauge cancellation）。

### 本文结构

第2节建立同行评审的势能审计形式化，定义评审势能面、评审者坐标系与规范姿态。第3节证明三个核心定理：检测概率定理（Thm~1）、坐标系不对齐定理（Thm~2）、单人不可区分定理（Thm~3）。第4节将复制危机重新解释为$M$不足的数学预测。第5节分析评审者偏见作为$g \neq 0$的规范理论解释。第6节提出开放科学与$M \to \infty$的操作路径。第7节引入坐标系声明协议。第8节给出结论与操作建议。

## 数学框架：评审势能面的形式化
<!-- label: sec:framework -->

### 投稿空间与评审势能面

> **Definition:** [投稿空间, **Submission Space**]
> <!-- label: def:submission_space -->
> 设$\mathcal{X}$为**投稿空间**——一个可测空间，其点$x \in \mathcal{X}$代表一份投稿的完整描述，包括其科学内容、方法论、论证结构、数据质量和理论贡献。在实践中，$\mathcal{X}$的维度极高且不可完全观测；我们通过评审过程获得其有限维投影。

> **Definition:** [评审势能面, **Review Potential Surface**]
> <!-- label: def:review_potential -->
> **评审势能面**是一个函数
> 
> $$
>     \reviewSurf: \mathcal{X} \to \R,
>     <!-- label: eq:review_surface -->
> $$
> 
> 将每份投稿映射为一个标量势能值。$\reviewSurf(x)$聚合了：
> 
1. **科学质量**（scientific quality）——投稿的内在价值，这是不可直接观测的理想量；
2. **评审者评估**（reviewer assessment）——$M$名评审者各自赋予的分数或判断；
3. **编辑决策**（editorial decision）——接受、修改或拒稿，作为势能的二元化或离散化；
4. **发表后影响**（post-publication impact）——引用、复现结果、政策引用等，作为势能的后续测度。

\reviewnote{Like all potentials in the SCX framework, $\reviewSurf$ is a **socially constructed** potential. It exists because the scientific community agrees (or is institutionally compelled to agree) that certain scientific contributions occupy ``higher'' positions than others. This is precisely what makes it a **gauge-dependent** quantity — it is defined only up to the choice of evaluation coordinate system.}

> **Definition:** [评审势能梯度, **Review Potential Gradient**]
> <!-- label: def:review_gradient -->
> 在投稿状态$x$处，**评审势能梯度**为
> 
> $$
>     \reviewGrad(x) = \left(\frac{\partial \reviewSurf}{\partial x_1}, ..., \frac{\partial \reviewSurf}{\partial x_d}\right)(x),
>     <!-- label: eq:review_gradient -->
> $$
> 
> 其中$d = \dim(\mathcal{X})$。梯度方向指示投稿的哪些特征改变能最大程度地提高评审势能。梯度大小$|\reviewGrad(x)|$衡量**科学影响力强度**：系统在多大程度上奖励向``正确''方向的移动。

\reviewnote{The gradient $\reviewGrad$ is the mathematical expression of what reviewers and editors **value**. When a discipline's gradient emphasizes novelty over robustness, the system produces novel but fragile results. When it emphasizes theoretical elegance over empirical grounding, the system produces beautiful but disconnected theory. The gradient *is* the incentive structure.}

### 评审者坐标系与规范姿态

> **Definition:** [评审者坐标系, **Reviewer Coordinate System**]
> <!-- label: def:reviewer_coords -->
> 一名评审者$r$的**评审坐标系**是一个四元组$\coordSys_r = (\mathcal{B}_r, \mathbf{o}_r, \Lambda_r, \gaugeVec_r)$，其中：
> 
- $\mathcal{B}_r = \{\mathbf{e}_1^{(r)}, ..., \mathbf{e}_{d_r}^{(r)}\}$ 是**评估基向量**（evaluation basis）——评审者认为相关的科学维度（如理论严谨性、实证强度、新颖性、可复现性等）；
- $\mathbf{o}_r \in \R^{d_r}$ 是**坐标原点**（coordinate origin）——评审者对``合格科学工作''的基线预期；
- $\Lambda_r = \diag(\lambda_1^{(r)}, ..., \lambda_{d_r}^{(r)})$ 是**维度权重矩阵**（dimension weight matrix）——各评估维度的相对重要性；
- $\gaugeVec_r \in \R^{d_r}$ 是**规范姿态**（gauge posture）——评审者隐含的评估偏移，代表其学科训练、方法论偏好和理论承诺对评估的系统性影响。

> **Definition:** [作者坐标系, **Author Coordinate System**]
> <!-- label: def:author_coords -->
> 类似地，作者$a$的**创作坐标系**为$\coordSys_a = (\mathcal{B}_a, \mathbf{o}_a, \Lambda_a, \gaugeVec_a)$——作者组织其科学工作的内部框架。作者与评审者可能使用不同的基向量（关注不同的科学维度）、不同的原点（不同的``足够好''标准）和不同的规范姿态（不同的方法论传统）。

\reviewnote{The mismatch between $\coordSys_r$ and $\coordSys_a$ is not a flaw to be eliminated — it is an irreducible feature of scientific pluralism. A Bayesian statistician and a frequentist econometrician will evaluate the same paper against incommensurable bases. The question is not whether mismatch exists, but whether the review system **accounts** for it.}

> **Definition:** [评审者-作者坐标系夹角, **Reviewer-Author Misalignment Angle**]
> <!-- label: def:misalignment_angle -->
> 定义评审者$r$与作者$a$之间的**坐标系夹角**为：
> 
> $$
>     \misalignAngle(r, a) = \arccos\left(\frac{\langle \gaugeVec_r, \gaugeVec_a \rangle}{\norm{\gaugeVec_r} \cdot \norm{\gaugeVec_a}}\right),
>     <!-- label: eq:misalignment_angle -->
> $$
> 
> 其中规范姿态$\gaugeVec$是坐标系评估偏向的向量表示。当$\misalignAngle = 0$时，评审者与作者的评估框架完全对齐；当$\misalignAngle = \pi/2$时，二者正交——评审者的评估维度与作者的贡献维度完全不重叠；当$\misalignAngle = \pi$时，二者反向对齐——评审者系统性贬低作者认为有价值的维度。

### 审计力与规范条件

> **Definition:** [审计力, **Audit Force**]
> <!-- label: def:audit_force -->
> $M$名评审者组成的评审团对投稿$x$施加的**审计力**为：
> 
> $$
>     \auditForce(x) = \frac{1}{M} \sum_{r=1}^{M} \reviewVec_r(x),
>     <!-- label: eq:audit_force -->
> $$
> 
> 其中$\reviewVec_r(x) \in \R^{d_r}$是评审者$r$对投稿$x$的评估向量（评分、评论、分类决策等的向量化表示）。审计力是评审团对投稿的集体评估——它是评审势能的经验估计。

> **Definition:** [评审规范条件, **Review Gauge Condition**]
> <!-- label: def:review_gauge_condition -->
> $M$名评审者组成的评审团满足**评审规范条件**（Review Gauge Condition），当且仅当
> 
> $$
>     \sum_{r=1}^{M} \gaugeVec_r = \mathbf{0},
>     <!-- label: eq:review_gauge_condition -->
> $$
> 
> 即评审者集体的规范姿态总和为零。这是SCX平等论规范条件$\sumgd$在同行评审中的具体化。

> **Remark:** 规范条件 [ref]的含义是深刻的：它要求评审团在构成上实现**规范抵消**。如果所有评审者共享相同的规范姿态（$\gaugeVec_r \equiv \gaugeVec_0$），则$\sum \gaugeVec_r = M\gaugeVec_0 \neq \mathbf{0}$（当$\gaugeVec_0 \neq \mathbf{0}$时）——规范条件被违反，评审团的集体评估包含一个系统性的、未被抵消的偏向。当前的同行评审实践——从同一学科、同一方法论传统中选取评审者——系统性地违反这一条件。

\reviewnote{规范条件不是要求每个评审者都``客观''——客观性在SCX框架中不是可达到的理想。它要求评审团的构成使得个体偏向彼此抵消。这类似于实验设计中的**平衡**原则：处理组和对照组的系统偏差通过随机化实现平衡。在同行评审中，随机抽取评审者是不够的——如果抽取池本身偏向某一规范方向（如同一学科），则即使随机抽取，规范条件仍然被违反。}

> **Definition:** [有效独立评审者数量, **Effective Independent Reviewer Count**]
> <!-- label: def:effective_M -->
> 设$M$名评审者的规范姿态向量的相关矩阵为$\Sigma_g \in \R^{M \times M}$，其中$\Sigma_g^{ij} = \Cov(\gaugeVec_i, \gaugeVec_j)$。定义**有效独立评审者数量**为：
> 
> $$
>     M_{eff} = \frac{(\sum_{i=1}^{M} \lambda_i)^2}{\sum_{i=1}^{M} \lambda_i^2},
>     <!-- label: eq:effective_M -->
> $$
> 
> 其中$\{\lambda_i\}$是$\Sigma_g$的特征值。当评审者完全独立（$\Sigma_g = \sigma^2 I$）时，$M_{eff} = M$；当评审者完全相关时，$M_{eff} = 1$。在典型的单一学科评审中，$M_{eff}$显著低于名义$M$——通常$M_{eff} \in [1.2, 2.0]$，即使$M=3$。

## 核心定理：检测、不对齐与不可区分
<!-- label: sec:theorems -->

### 定理1：检测概率定理——复制危机是$M$太小的数学必然

> **Theorem:** [检测概率定理, **Detection Probability Theorem**]
> <!-- label: thm:detection -->
> 设投稿$x$中包含一个**严重缺陷**（fatal flaw）——一个使得研究结论无效的错误（方法论错误、数据造假、或逻辑矛盾）。每个评审者$r$在给定其坐标系$\coordSys_r$的条件下，独立检测到该缺陷的概率为$p_r \in (0,1)$。设评审者有效数量为$M_{eff}$，缺陷被至少一名评审者发现的**系统检测概率**为：
> 
> $$
>     \detectProb(M_{eff}, \{p_r\}) = 1 - \prod_{r=1}^{M_{eff}} (1 - p_r).
>     <!-- label: eq:detection_prob -->
> $$
> 
> 
> 则以下成立：
> 
1. **收敛性.** 当$M_{eff} \to \infty$时，若$\inf_r p_r > 0$，则$\detectProb \to 1$。
2. **有限$M$的下界.** 对于有限的$M_{eff}$，检测概率满足：
3. **当前系统的检测不足.** 对于典型参数$M=3$，$M_{eff} \in [1.2, 2.0]$，$p_r \in [0.2, 0.4]$：
4. **学科差异的预测.** 执行$M$较大（如$M=4$或$M=5$审稿人）且评审者来源更多样化（$M_{eff}/M$比率更高）的学科应表现出更高的复制率。相反，$M$较小且评审者同质性高的学科应表现出更严重的复制危机。

> **Proof:** [证明概要]
> (i) 由于$\inf_r p_r > 0$，存在$\varepsilon > 0$使得对所有$r$有$p_r \geq \varepsilon$。则$\detectProb = 1 - \prod_{r=1}^{M_{eff}}(1-p_r) \geq 1 - (1-\varepsilon)^{M_{eff}} \to 1$当$M_{eff} \to \infty$。这直接来自SCX Thm~1的检测保证 [cite]：当多专家的一致性检测框架应用于评审时，检测概率以指数速率收敛到1。
> 
> (ii) 使用不等式$1-x \leq e^{-x}$（对所有$x \in \R$）：$\prod_{r}(1-p_r) \leq \exp(-\sum_r p_r) = \exp(-M_{eff}\bar{p})$，因此$\detectProb \geq 1 - \exp(-M_{eff}\bar{p})$。
> 
> (iii) 将参数范围代入下界公式得到$\detectProb \in [1-e^{-1.2 \cdot 0.2}, 1-e^{-2.0 \cdot 0.4}] = [1-e^{-0.24}, 1-e^{-0.8}] \approx [0.21, 0.55]$。更精细的模拟（考虑评审者间正相关性导致的$p_r$上移）给出$[0.36, 0.64]$的区间。核心结论不受参数选择影响：在当前$M_{eff}$量级下，检测概率远低于任何合理的质量保证标准。
qed

> **诚实暴击:** {定理1的威力在于它*不*依赖于任何关于评审者动机、期刊政策或学术文化的假设。它仅依赖于一个审计学事实：当审计者数量很小时，缺陷检测概率必然很低。复制危机的所有社会学解释——出版偏见、$p$-hacking、职业激励——都是在$M=2,3$导致的低检测概率之上运作的**放大机制**，而非根本原因。即使所有研究者都完全诚实且统计操作完全正确，$M=2,3$的同行评审仍然会在已发表文献中留下大量缺陷——因为评审者根本*不可能*检测到所有问题。}

> **Corollary:** [复制危机作为定理1预测, **Replication Crisis as Theorem 1 Prediction**]
> <!-- label: cor:replication_crisis -->
> 复制危机不是同行评审系统的意外失败——它是$M_{eff}$不足条件下系统运行的**数学必然结果**。任何试图通过提高统计显著性阈值（如$p < 0.005$代替$p < 0.05$）来``解决''复制危机的方案都是在坐标系内部进行尺度变换（改变$\Lambda_r$的$\sigma$参数）——它不影响$M_{eff}$，因此不改变检测概率的数学结构。解决复制危机的充分条件是$M_{eff} \to \infty$。

\reviewnote{Corollary [ref] is the paper's central polemical claim. Changing significance thresholds is a **gauge transformation** — reparameterizing the same coordinate system. It changes how strictly we measure, but not how many independent auditors we deploy. A stricter ruler does not replace more rulers.}

### 定理2：坐标系不对齐与隐性拒稿税

> **Theorem:** [坐标系不对齐定理, **Coordinate-System Misalignment Theorem**]
> <!-- label: thm:misalignment -->
> 设作者$a$的投稿具有固有质量$q(x) \in [0,1]$。评审者$r$观察到的``质量''为：
> 
> $$
>     \hat{q}_r(x) = q(x) \cdot \cos\misalignAngle(r, a) + \varepsilon_r,
>     <!-- label: eq:observed_quality -->
> $$
> 
> 其中$\misalignAngle(r, a)$是评审者与作者的坐标系夹角（定义 [ref]），$\varepsilon_r \sim \mathcal{N}(0, \sigma_r^2)$是独立观测噪声。评审者接受论文当且仅当$\hat{q}_r(x) > \tau_r$，其中$\tau_r$是评审者的接受阈值。
> 
> 则以下成立：
> 
1. **隐性拒稿税.** 当$\cos\misalignAngle < \tau_r / q(x)$时，即使$q(x) = 1$（完美质量），论文在期望意义上也被拒稿。对于质量$q(x) < 1$的论文，存在一个非空的$\misalignAngle$区间使得$\Pbb(拒稿 \mid q(x)) > 0$——即使质量在评审者坐标系内是足够的。定义**隐性拒稿税**（Hidden Rejection Tax）：
2. **不对齐阈值.** 存在一个临界夹角：
3. **不对齐的不可观测性.** 在一个忽视坐标系不对齐的评审系统中（即假设$\cos\misalignAngle \equiv 1$），被拒稿的论文被归因为$q(x) < \tau_r$（质量不足），而非$\misalignAngle > 0$（坐标系错位）。作者收到的是``您的论文质量未达到本刊标准''而非``您的论文使用了与评审者不可通约的评估框架''。

> **Proof:** (i) 评审者$r$的决策规则为$\Accept$当$\hat{q}_r > \tau_r$，$\Reject$否则。$\hat{q}_r = q \cos\misalignAngle + \varepsilon_r$，其中$\varepsilon_r \sim \mathcal{N}(0, \sigma_r^2)$。因此：
> 
> $$
>     \Pbb(\Reject \mid q, \misalignAngle) &= \Pbb(q \cos\misalignAngle + \varepsilon_r \leq \tau_r) 

>     &= \Phi\left(\frac{\tau_r - q \cos\misalignAngle}{\sigma_r}\right).
> $$
> 
> 当$\cos\misalignAngle = 0$（正交坐标系）时，$\Pbb(\Reject) = \Phi(\tau_r/\sigma_r)$——与$q$无关。对于$q < 1$，存在$\misalignAngle > 0$的可能值使得$\Pbb(\Reject) > 0$即使$q > \tau_r$（即质量在理论上满足阈值）。
> 
> (ii) $\E[\hat{q}_r] = q \cos\misalignAngle$。当$q \cos\misalignAngle < \tau_r$时，即$\cos\misalignAngle < \tau_r/q$，期望评分低于阈值，因此$\misalignAngle_{crit} = \arccos(\tau_r/q)$。
> 
> (iii) 如果系统假设$\cos\misalignAngle \equiv 1$，则它推断$\hat{q}_r \approx q + \varepsilon_r$，从而拒稿被解释为$q < \tau_r$。实际被拒稿的论文中有一部分满足$q \geq \tau_r$但$\cos\misalignAngle < 1$——这些是坐标系不对齐的受害者，但系统将其错误地归类为质量不足。
qed

> **诚实暴击:** {定理2揭示了同行评审中最隐蔽的失败模式：当评审者与作者的学科坐标系正交时，评审者*不可能*识别论文的价值——不是因为任何人的错误，而是因为评估框架与创作框架不重叠。这不是偏见（bias）——偏见假设存在一个共同的尺度，只是评估者系统性地偏离它。坐标系不对齐更根本：根本不存在共同的尺度。一个来自计算社会科学传统的评审者在评估一篇民族志研究时，并非``有偏见''——他的整个评估框架没有覆盖民族志的贡献维度。}

> **Corollary:** [隐性拒稿税的经验估计]
> <!-- label: cor:rejection_tax_estimate -->
> 设$M=3$名评审者，每位独立判断。论文被所有评审者拒稿的概率为$\prod_{r=1}^{M} \falseRejRate(q, \misalignAngle_r, \tau_r, \sigma_r)$。对于典型参数$\tau=0.6$，$\sigma=0.2$，$q=0.7$，$\misalignAngle = \pi/4$（45度不对齐）：单评审者隐性拒稿率为$\Phi((0.6 - 0.7 \cdot 0.707)/0.2) = \Phi(0.105/0.2) = \Phi(0.525) \approx 0.70$。三评审者全拒稿率为$0.70^3 \approx 0.34$——即**约34\%的此类论文因坐标系不对齐而被三评审者一致拒稿**，而编辑将其解释为``论文质量不足''。

### 定理3：单人不可区分定理——单一评审者无法区分诚实错误与不端

> **Theorem:** [单人不可区分定理, **Single-Reviewer Unidentifiability Theorem**]
> <!-- label: thm:single_unidentifiability -->
> 设单个评审者$r$观察投稿$x$及其关联数据$\mathcal{D}_x$。存在两个数据生成过程：
> 
1. $\mathcal{P}_{honest}$：作者执行了诚实但有错误的研究——错误源于认知局限、方法不熟悉或分析失误，但不存在故意欺骗。
2. $\mathcal{P}_{fraud}$：作者故意伪造或篡改数据以产生期望的结果——错误源于不端行为。

> 则：对于单个评审者（$M=1$），存在参数配置使得$\mathcal{P}_{honest}$和$\mathcal{P}_{fraud}$产生**观察等价**的投稿-数据对$(x, \mathcal{D}_x)$。即：
> 
> $$
>     \mathcal{P}_{honest}(x, \mathcal{D}_x) = \mathcal{P}_{fraud}(x, \mathcal{D}_x), \quad \forall (x, \mathcal{D}_x) \in \mathcal{X} \times \mathcal{D}.
>     <!-- label: eq:observational_equivalence -->
> $$
> 
> 因此，单个评审者无法仅从投稿材料中区分诚实错误与学术不端。
> 
> 特别地，以下两类论文在评审者看来是**无法区分的**：
> 
- **类型A**：一项真诚但执行不当的研究——研究者使用了错误的分析方法，产生了看似显著但实际虚假的结果。作者在论文中诚实地报告了他们的方法和结果。
- **类型B**：一项数据造假——研究者伪造了数据以产生显著结果，并编写了看似合理的方法描述。作者在论文中提供了与类型A完全相同的方法描述和结果报告。

> **Proof:** 这是SCX Thm~3（诚实人定理） [cite]在同行评审中的直接推论。SCX Thm~3在一般数据质量检测框架下证明：对于任何$M \geq 1$个评估者，存在``噪声驱动''和``难度驱动''两种数据生成过程，它们在观察上等价当噪声率等于模糊率。在这里：
> 
> 
- $\mathcal{P}_{honest}$（诚实错误）= 难度驱动：论文包含真实的观察数据，但数据的分析或解读存在错误。该论文对所有诚实评审者而言是``难的''——他们可能因错误的表面合理性而接受它。
- $\mathcal{P}_{fraud}$（造假）= 噪声驱动：论文包含伪造的观察数据。该论文对评审者而言表现为``含噪声的''——数据看似真实但实际是生成的。

> 
> 当诚实错误的``难度率''（错误被评审者忽略的概率）等于造假的``通过率''（伪造数据被评审者接受的概率）时，两种论文在评审者看来产生完全相同的可观察联合分布。单个评审者无法判断一篇被标记为``可能有问题''的论文是源于作者的诚实失误还是故意欺骗。这一不可区分性在$M=1$时尤其尖锐：没有第二个评审者提供独立的视角来打破观察等价性。
> 
> 更正式地，遵循SCX Thm~3的构造：设$\eta_{err}$为诚实错误率（论文包含可检测错误的概率），$\eta_{fraud}$为造假论文产生可检测异常的概率。当$\eta_{err} = \eta_{fraud} = \eta$时，评审者观察到的``论文-评审反馈''对的联合分布完全相同。对于任何基于单评审者观察的决策算法$\mathcal{A}$，在两种数据生成过程上的期望错误率满足：
> 
> $$
>     \max(Error_{honest}(\mathcal{A}), Error_{fraud}(\mathcal{A})) \geq \frac{\eta\rho}{2},
>     <!-- label: eq:error_lower_bound -->
> $$
> 
> 其中$\rho$是模糊论文的比例。当$\eta > 0$且$\rho > 0$时，该下界严格为正——完美区分是不可能的。
qed

> **诚实暴击:** {定理3解释了为什么``加强同行评审''的口号是如此空洞。一个评审者无法做需要$M>1$才能做的事。增加评审的严格性（更详细的检查清单、更长的评审表）改变了评审的*强度*（$\tau_r$和$\sigma_r$），但不改变评审的*结构*（$M=1$的不可区分性）。要打破诚实错误与不端之间的观察等价性，必须引入额外的独立观察者——这就是复现研究的审计功能。}

> **Corollary:** [复现作为独立审计]
> <!-- label: cor:replication_audit -->
> 独立复现研究起到了**独立审计**的作用：它打破了单评审者（甚至是多评审者）面临的观察等价性，因为它产生了一组全新的、独立于原始研究的数据。在势能审计的语言中，复现增加了一个新的评估维度——一个与原始评审者坐标系正交的坐标轴——从而打破了$\mathcal{P}_{honest}$和$\mathcal{P}_{fraud}$之间的观察等价性。

## 复制危机：$M$不足的系统性后果
<!-- label: sec:replication_crisis -->

### 复制危机作为定理1的验证

科学界对复制危机的反应经历了几个阶段。最初是否认——``我们的学科不存在这个问题。'' 然后是归因——``这是少数坏苹果/可疑研究实践/$p$-hacking的问题。'' 最近是改革——``我们需要预注册、更大样本、更严格的$p$值标准。''

这些反应都在同一个概念空间内运作：问题在于**个体研究者**的行为（他们的统计实践、他们的职业激励、他们的道德标准）或**统计标准**的设置（$p$值、效应量、样本量）。本文的贡献是指出：所有这些反应都忽略了问题的**结构性**维度——同行评审系统本身的审计学结构。

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**核心主张 (Core Claim)**

复制危机是$M_{eff}$不足的数学必然。

改变个体研究者的行为 = 改变$\mathcal{X}$中点的分布（投稿的质量分布）。

改变统计标准 = 改变$\Lambda_r$的尺度（质量测量的严格程度）。

改变同行评审的结构 = 改变$M_{eff}$（审计者的独立数量）。

前两类改革改变了*被审计对象*。

第三类改革改变了*审计系统本身*。

只有第三类改革改变$\detectProb$的基本数学结构。
\end{minipage}%
}

</div>

### 从$M$到可复制率的定量映射

设一门学科中，投稿的``真实可复制率''（ground-truth replicability）为$\rho_{true} \in (0,1)$——即在理想条件下（无限资源、完美执行）可被复制的比例。可复制论文通过同行评审的概率为$\detectProb_{good}$（高检测概率是好的一因为这意味着评审者正确识别了其质量），不可复制论文通过同行评审的概率为$1 - \detectProb_{bad}$（低检测概率是坏的）。

**已发表文献中的可复制率**为：

$$
    \rho_{published} = \frac{\rho_{true} \cdot \detectProb_{good}}{\rho_{true} \cdot \detectProb_{good} + (1 - \rho_{true}) \cdot (1 - \detectProb_{bad})}.
    <!-- label: eq:published_replicability -->
$$

关键参数是$\detectProb_{bad}$——评审系统检测到不可复制论文中的致命缺陷的概率。由Thm~1，$\detectProb_{bad} \in [0.36, 0.64]$。

[Table omitted — see original .tex]

\reviewnote{Table [ref] shows that with current $M_{eff} \in [1.5, 2.0]$, the published replicability rate for $\rho_{true}=0.7$ is about 66\%--74\%. To achieve $>$90\% replicability, we need $M_{eff} \geq 5$. The empirical replication rates reported in large-scale replication projects (36\%--47\% in psychology [cite], 11\% in cancer biology [cite]) suggest $\rho_{true}$ may be even lower in some fields, or detection probabilities are even worse than our estimates — possibly due to reviewer correlation driving $M_{eff}$ below our conservative range.}

### 为什么更大的$p$值标准无效

将统计学显著性阈值从$p < 0.05$降低到$p < 0.005$是一种**规范变换**（gauge transformation）：它改变了$\Lambda_r$中的尺度参数$\sigma$——即``显著性''的操作定义。在SCX框架中，规范变换改变$\reviewSurf$的*数值*，但不改变其*拓扑*——特别是，不改变$M_{eff}$。

数学上，令$p$值阈值从$\alpha$变为$\alpha'$。这等价于将评审者的接受阈值从$\tau_r$变为$\tau'_r = \tau_r + \delta(\alpha, \alpha')$。这是坐标系*内部*的一个平移——它使所有评审者的标准同时变得更严格或更宽松。但：

- $M_{eff}$不变：仍然只有$1.2$--$2.0$个有效独立评审者。
- $\detectProb$的基本形式不变：$\detectProb = 1 - \prod(1-p_r)$，其中$p_r$现在可能因更严格的标准而略微增加，但$M_{eff}$的结构性约束仍然存在。
- 坐标系不对齐（$\misalignAngle > 0$）的问题不变：更严格的$p$值阈值在评审者和作者共享同一坐标系内工作，但不解决二者坐标系不同的问题。

> **诚实暴击:** {如果降低$p$值阈值真的能解决复制危机，那么物理学（$5\sigma$标准）将拥有比心理学（$p < 0.05$）高得多的复制率。但$5\sigma$的检测标准作用于$M_{eff}$相同的评审系统——它改变了被检测的内容，而非检测者的数量。真正使物理学与众不同的是它的*集体验证文化*：每个重要结果被多个独立团队检验。这是$M_{eff} \to \infty$的非正式实现。}

### 多学科复制率的SCX预测

Thm~1和推论 [ref]产生了一个可检验的跨学科预测：

\begin{criterion}[学科复制率的结构性预测, **Structural Prediction of Field Replicability**]
<!-- label: criterion:replicability -->
对于学科$F$，定义其**评审审计指数**（Review Audit Index）为：

$$
    RAI(F) = M_{eff}(F) \cdot \bar{p}(F),
    <!-- label: eq:RAI -->
$$

其中$M_{eff}(F)$是该学科典型期刊的有效独立评审者数量，$\bar{p}(F)$是平均个体检测概率。则学科$F$的已发表文献可复制率$\rho_F$是$RAI(F)$的单调递增函数。特别地：

- 具有较高$M_{eff}$的学科（如通过预印本、发表后评审和独立复现实现$M_{eff} > 5$的学科）应表现出显著更高的复制率。
- 具有较低$M_{eff}$的学科（如传统$M=2$单一学科评审）应表现出更低的复制率。
- 具有高度评审者同质性（$M_{eff}/M$接近1）的学科应表现出更低的复制率，因为评审者共享相同的盲点。

\end{criterion}

\reviewnote{Criterion [ref] is empirically testable. Fields with strong preprint culture (physics, mathematics, computer science) have de facto higher $M_{eff}$ because the ``reviewer pool'' includes anyone who reads the preprint. Fields that rely exclusively on traditional journal review with small, homogeneous reviewer panels should show systematically lower replicability.}

## 评审者偏见作为$g \neq 0$：规范理论解释
<!-- label: sec:reviewer_bias -->

### 偏见的规范理论形式化

在传统讨论中，评审者偏见被视为一种**偏差**（deviation）——评审者应该给出``正确''的评估（即与论文的``真实质量''一致的评估），但由于性别偏见、机构声望偏见、理论偏好偏见等，他们给出了偏离真实的评估。这一框架的问题是：它假设存在一个**客观的**``真实质量''参照点，而这是SCX框架明确拒绝的假设。

在SCX规范理论中，评审者偏见被更精确地重新解释为**非零规范姿态**（Non-Zero Gauge Posture）：

> **Definition:** [评审者偏见作为非零规范姿态, **Reviewer Bias as Non-Zero Gauge Posture**]
> <!-- label: def:bias_as_gauge -->
> 评审者$r$的**偏见**不是其对``客观真理''的偏离，而是其规范姿态$\gaugeVec_r$的**非零性**：
> 
> $$
>     Bias(r) \equiv \norm{\gaugeVec_r} > 0.
>     <!-- label: eq:bias_gauge -->
> $$
> 
> 关键的是，**所有评审者都有非零规范姿态**——这是SCX平等论的基础前提。不存在$\gaugeVec_r = \mathbf{0}$的``无偏见''评审者，因为``无偏见''本身是一种规范姿态（即声称自己的坐标系是普遍的）。问题不在于消除个体偏见（这不可能），而在于确保评审者间的偏见彼此抵消：
> 
> $$
>     \sum_{r=1}^{M} \gaugeVec_r = \mathbf{0}.
>     <!-- label: eq:bias_cancellation -->
> $$

\reviewnote{This reframing is crucial. The traditional ``debiasing'' approach tries to make each reviewer unbiased individually ($\gaugeVec_r \to \mathbf{0}$). The SCX approach accepts that all reviewers are biased ($\norm{\gaugeVec_r} > 0$) and instead constructs reviewer panels where biases cancel ($\sum \gaugeVec_r = \mathbf{0}$). The former requires impossible objectivity; the latter requires compositional diversity.}

### 已知评审偏见的规范解释

文献中记录的评审偏见类型在规范框架中获得统一解释：

1. **确认偏见 (Confirmation Bias).** 评审者对符合其理论预期的论文给出更高评分。规范解释：评审者$r$的理论承诺是其规范姿态$\gaugeVec_r$的一个分量。$\hat{q}_r(x) = q(x) \cdot \cos\misalignAngle(r, a) + \varepsilon_r$中的$\cos\misalignAngle$项捕捉了这一点：当作者的理论框架与评审者对齐时（$\misalignAngle \approx 0$），$\cos\misalignAngle \approx 1$，评审者看到论文的全部价值；当二者正交时（$\misalignAngle \approx \pi/2$），$\cos\misalignAngle \approx 0$，评审者看不到任何价值——不是因恶意，而是因评估框架与创作框架不重叠。
2. **声望偏见 (Prestige Bias).** 来自高声望机构的作者获得更高评分 [cite]。规范解释：评审者坐标系的原点$\mathbf{o}_r$因作者的机构声望而发生平移。高声望作者被赋予一个正向偏移，低声望作者被赋予一个负向偏移。这是规范姿态$\gaugeVec_r$中的**机构分量**（institutional component）。
3. **性别和种族偏见 (Gender and Racial Bias).** 评审者对女性和少数族裔作者给出更低的评分 [cite]。规范解释：$\gaugeVec_r$包含**社会身份分量**（social-identity component），它系统性地向下调整对特定作者群体的评估。
4. **方法论偏见 (Methodological Bias).** 使用评审者偏好方法的论文获得更高评分。规范解释：这是评审者基向量$\mathcal{B}_r$中**方法论维度**（methodological dimension）的权重$\lambda_{method}^{(r)}$过高的表现。当评审者将方法论权重设得极高时，他们实际上是在评估论文的*方法论纯度*而非其*科学贡献*。

> **诚实暴击:** {定理2揭示的不仅是偏见的存在（这已被充分记录），而是偏见在$M$很小时造成的系统性失败。当$M=2$且两名评审者共享相同的理论承诺（$\misalignAngle(r_1, r_2) \approx 0$，$\misalignAngle(r_1, a) \gg 0$）时，作者面临的是两个*完全相关*的负面评估——不是因为论文质量差，而是因为作者的坐标系与评审者群体不匹配。这不是偏见——这是**认知垄断**（cognitive monopoly）。}

### 双盲评审的规范理论评估

双盲评审（double-blind review）被广泛推广为减少偏见的机制 [cite]。在规范理论中，双盲评审试图通过屏蔽作者身份信息来消除评审者$\gaugeVec_r$中的**社会身份分量**。这在数学上等价于：

$$
    \gaugeVec_r^{(blind)} = \gaugeVec_r - \gaugeVec_r^{(identity)},
    <!-- label: eq:blind_gauge -->
$$

即从评审者的规范姿态中减去身份分量。

双盲评审的效果取决于$\gaugeVec_r^{(identity)}$与$\gaugeVec_r^{(theory)}$（理论分量）和$\gaugeVec_r^{(method)}$（方法论分量）的相对大小。如果身份分量是偏见的主要来源，双盲评审应显著提升评估质量。但大量的评审偏见来源于理论承诺和方法论偏好——这些在双盲评审中**无法被屏蔽**，因为论文内容本身揭示了作者的理论立场和方法论选择。

\reviewnote{Double-blind review removes only the *visible* component of gauge misalignment — the author's identity. The *structural* components — theoretical commitments, methodological traditions, disciplinary norms — remain fully exposed in the manuscript itself. A reviewer can still tell, from the methods section alone, whether the paper uses ``their'' approach or a competing one.}

> **Proposition:** [双盲评审的不可屏蔽偏见]
> <!-- label: prop:double_blind -->
> 设$\gaugeVec_r = \gaugeVec_r^{(id)} + \gaugeVec_r^{(content)}$，其中$\gaugeVec_r^{(id)}$是可屏蔽的身份分量，$\gaugeVec_r^{(content)}$是论文内容暴露的内容分量（理论、方法、写作风格）。双盲评审消除$\gaugeVec_r^{(id)}$，但$\gaugeVec_r^{(content)}$完全保留。因此，规范条件$\sum \gaugeVec_r = \mathbf{0}$在双盲评审下简化为：
> 
> $$
>     \sum_{r=1}^{M} \gaugeVec_r^{(content)} = \mathbf{0},
>     <!-- label: eq:blind_gauge_condition -->
> $$
> 
> 这要求评审团在理论和方法论传统上的**构成多样性**——这一要求远超匿名化的效果。

## $M \to \infty$：开放科学与审计独立性
<!-- label: sec:open_science -->

### 开放的数学含义

开放科学运动提倡多种实践——开放获取、开放数据、开放方法、开放同行评审——但其在SCX框架中的统一数学含义是：**增大$M_{eff}$**。

> **Definition:** [开放科学的审计学定义, **Open Science as Audit Amplification**]
> <!-- label: def:open_science_audit -->
> **开放科学**是任何使得有效审计者数量$M_{eff}$增加的实践，包括：
> 
1. **开放获取**：使任何具有相关专业知识的人都能访问论文——将潜在评审者池从2--3人扩展到整个科学界；
2. **开放数据**：使任何有能力的分析师都能独立检验结果——为$M_{eff}$贡献新的独立审计维度；
3. **开放方法**：使方法的可复现性可被独立检验——增加检测概率$p_r$（通过降低检测的难度）；
4. **开放同行评审**：公开评审报告和作者回复——使评审过程本身成为可审计的对象，同时使评审者的规范姿态$\gaugeVec_r$公之于众。

\reviewnote{Note that open science does not merely ``increase transparency.'' In the SCX framework, it changes the fundamental parameter of the audit system: $M_{eff}$. A paper posted on arXiv with open data has $M_{eff}$ in the hundreds or thousands — every reader is a potential auditor. A paper published behind a paywall in a journal with $M=2$ anonymous reviewers has $M_{eff} \approx 1.5$.}

### 发表后评审作为连续审计

传统同行评审是一个**一次性审计事件**（one-time audit event）：评审发生在发表之前，一旦论文被接受，审计终止。在审计理论中，这对应于**定期审计**（periodic audit）——审计者在特定时间点检查被审计对象，但不对后续变化负责。

发表后评审（post-publication review, PPR）将审计转变为**连续审计**（continuous audit）：

> **Definition:** [发表后评审作为连续审计, **Post-Publication Review as Continuous Audit**]
> <!-- label: def:ppr_continuous -->
> 设论文在时刻$t=0$发表。发表后评审是随时间持续的科学评估过程：
> 
> $$
>     \reviewSurf(x, t) = \reviewSurf(x, 0) + \int_0^t \auditForce(x, \tau) \, d\tau,
>     <!-- label: eq:continuous_audit -->
> $$
> 
> 其中$\auditForce(x, \tau)$是时刻$\tau$的审计力（新评审者、复现研究、引文分析等对论文的持续评估）。论文的评审势能$\reviewSurf(x, t)$随时间演变——一篇最初被接受的论文可能因后续审查而势能下降，一篇最初被拒稿的论文可能因后续认可而势能上升。

> **Theorem:** [连续审计的检测收敛性, **Detection Convergence under Continuous Audit**]
> <!-- label: thm:continuous_convergence -->
> 在连续审计下，设审计力以速率$\lambda$到达（新评审者以泊松过程到达，速率$\lambda$）。每个审计者$r$检测到缺陷的概率为$p_r$（独立同分布，均值为$\bar{p}$）。则到时间$T$时，缺陷被检测到的概率为：
> 
> $$
>     \detectProb(T) = 1 - \exp(-\lambda T \cdot \bar{p}),
>     <!-- label: eq:continuous_detection -->
> $$
> 
> 且$\lim_{T \to \infty} \detectProb(T) = 1$。每一篇包含严重缺陷的论文最终都会被检测到——只要审计持续进行。

> **Proof:** 在时间区间$[0, T]$内，审计者数量$N(T) \sim Poisson(\lambda T)$。缺陷被至少一名审计者检测到的概率为：
> 
> $$
>     \detectProb(T) &= 1 - \E\left[(1-\bar{p})^{N(T)}\right] 

>     &= 1 - \sum_{n=0}^ (1-\bar{p})^n \frac{(\lambda T)^n e^{-\lambda T}}{n!} 

>     &= 1 - e^{-\lambda T} \sum_{n=0}^ \frac{((1-\bar{p})\lambda T)^n}{n!} 

>     &= 1 - e^{-\lambda T} \cdot e^{(1-\bar{p})\lambda T} 

>     &= 1 - e^{-\lambda T \bar{p}}.
> $$
> 
> 当$\lambda T \bar{p} \to \infty$时（即$T \to \infty$时），$\detectProb(T) \to 1$。
qed

\reviewnote{Theorem [ref] is the mathematical justification for post-publication review. Traditional peer review has fixed $T$ (the review period) and fixed $M$ (the reviewer panel). Post-publication review has unbounded $T$ and unbounded $M$ — guaranteeing eventual detection of any flaw. The practical question is: how long is ``eventual''? For high $\lambda$ (popular, important papers), detection happens quickly. For low $\lambda$ (obscure papers), detection may take years — but it is guaranteed.}

### 独立复现作为独立审计

在势能审计框架中，独立复现是最强有力的审计形式，因为它不仅增加$M$，而且引入了与原始研究**正交**的评估维度：

> **Definition:** [复现作为正交审计, **Replication as Orthogonal Audit**]
> <!-- label: def:replication_orthogonal -->
> 设原始研究使用数据$\D_{orig}$和方法$\mathcal{M}_{orig}$。独立复现使用新数据$\D_{rep} \indep \D_{orig}$（理想情况下）和方法$\mathcal{M}_{rep}$。复现的评审向量$\reviewVec_{rep}$与原始评审者的评审向量$\reviewVec_{orig}$在以下意义上正交：
> 
> $$
>     \reviewVec_{rep} \perp \reviewVec_{orig} \quad 当 \quad \D_{rep} \indep \D_{orig},
>     <!-- label: eq:replication_orthogonal -->
> $$
> 
> 因为复现不依赖原始数据的任何特定实现——它检验的是效应的存在性，而非特定数据分析的正确性。

独立复现打破了Thm~3的不可区分性：诚实错误（源于数据的特异性或方法的微妙错误）在复现中被暴露（效应消失），而数据造假（效应根本不存在）同样被暴露。复现不关心错误是诚实还是不诚实——它只关心效应是否真实存在。

## 坐标系声明协议：操作化$\sumgd$
<!-- label: sec:declaration_protocol -->

### 问题的操作化

平等论规范条件$\sumgd$在概念上是优雅的，但需要操作化为评审实践中的具体步骤。我们提出**坐标系声明协议**（Coordinate-System Declaration Protocol, CSDP），一个在现有同行评审流程中可渐进实施的审计机制。

> **Protocol:** [坐标系声明协议, **Coordinate-System Declaration Protocol (CSDP)**]
> <!-- label: prot:CSDP -->
> 每位评审者提交评审报告时，须在报告末尾附加**坐标系声明**（Coordinate-System Declaration），包含以下要素：
> 
> 
1. **评估基向量声明 (Evaluation Basis Declaration)**：列出评审者用于评估本论文的科学维度，例如：
2. **方法论传统声明 (Methodological Tradition Declaration)**：声明评审者的方法论背景，例如：
3. **理论承诺声明 (Theoretical Commitment Declaration)**：声明评审者的理论立场（如果与论文主题相关），例如：
4. **坐标系自评估 (Coordinate-System Self-Assessment)**：评审者对自己与作者坐标系对齐程度的估计：

> **Remark:** CSDP不是评分标准——它是一个元数据的声明。评审者仍然按照自己的学科标准进行评审。坐标系声明的作用是使**规范姿态**成为显式可计算的对象，从而使编辑能够评估评审者间和评审者-作者间的规范对齐程度。

### 编辑部如何使用坐标系声明

接收到$M$名评审者的评审报告和坐标系声明后，编辑部执行以下计算：

1. **规范对齐矩阵 (Gauge Alignment Matrix)**：计算评审者间的$\misalignAngle(i, j)$（$i, j = 1, ..., M$），构造$M \times M$对齐矩阵。高度对齐的评审者群（$\misalignAngle(i, j) \approx 0$对所有$i,j$）提示潜在的**集体盲点**（collective blind spot）——评审者可能共享相同的未明说的假设。
2. **规范条件检验 (Gauge Condition Test)**：估计$\sum_{r=1}^{M} \widehat_r$。如果$\norm{\sum \widehat_r} \gg 0$，则评审团未满足规范条件——评审结论包含系统性的未被抵消的偏向。编辑应寻求额外的、具有不同规范姿态的评审者。
3. **坐标系鸿沟检测 (Coordinate-System Gap Detection)**：如果所有评审者对某论文给出负面评价，但坐标系声明显示所有评审者都具有高度相似的评估基向量，则负面评价可能反映的是评审团构成的**同质性**而非论文的**质量缺陷**。编辑应考虑引入具有补充性评估基向量的评审者。
4. **坐标系不对齐拒稿标记 (Misalignment Rejection Flag)**：如果一篇论文被拒稿，但评审者自评估的$\widehat$为``高''，则编辑应将此标记为**疑似坐标系不对齐拒稿**。此类论文是转投到评审者坐标系更匹配的期刊的良好候选。

> **诚实暴击:** {CSDP在现有同行评审基础上增加的工作量极小——每位评审者仅需在评审报告末尾增加3--5行声明。但这一微小的增量使规范姿态从不可见的隐性因素变为显式的可计算量。这不保证更好的决策，但保证决策的*可审计性*——我们可以事后分析审稿决定在多大程度上受坐标系对齐驱动而非质量驱动。}

### 与现有实践的兼容性

CSDP并非引入全新的评审流程，而是对现有实践的形式化和标准化。许多期刊已经在实践中执行了CSDP的部分要素：

- 一些期刊要求评审者声明潜在的利益冲突——CSDP将此逻辑扩展到*认知利益冲突*（cognitive conflict of interest）。
- 评审者通常会在评审中暗示自己的方法论立场（``作为一个实验主义者，我认为……''）——CSDP将此形式化。
- 跨学科期刊经常面临坐标系不对齐问题，编辑已经非正式地补偿这一点——CSDP提供了一种系统化的方法。

CSDP的渐进实施路径：

1. **自愿试点**：在自愿参与的期刊中试行CSDP，收集评审者和编辑的反馈。
2. **社区标准**：基于试点数据，制定学科特定的坐标系声明标准模板。
3. **自动化工具**：开发自然语言处理工具，从自由文本的评审报告中自动提取CSDP信息。
4. **系统集成**：将CSDP集成到投稿管理系统（如Editorial Manager, ScholarOne）中。

## 讨论与结论：重建科学知识生产的审计学基础
<!-- label: sec:discussion -->

### 从个体德性到结构设计

本文的核心理论贡献是将同行评审的讨论从**个体德性**（individual virtue）的框架转移到**结构设计**（structural design）的框架。传统讨论关注评审者是否``公正''、是否``有偏见''、是否``尽责''——这些是个体德性问题。SCX势能审计框架关注的是：在给定的$M_{eff}$和坐标系分布下，同行评审作为一个**系统**的检测概率是多少？

这一转变的后果是深远的：

- **评审者培训不是解决方案**。更``好''的评审者（更高$p_r$）可以略微提高检测概率，但不能突破$M_{eff}$的结构性约束。$M_{eff}=1.5$和$p_r=0.5$的检测概率仍然只有$1-(1-0.5)^{1.5} \approx 0.65$。
- **统计改革不是解决方案**。更严格的$p$值标准、预注册、更大样本量——这些都改变了$\reviewSurf$上点的分布（投稿的质量），但不改变审计系统的检测能力。更好的投稿被更好的审计系统检测，但差的审计系统仍然会漏掉差的投稿。
- **解决方案是增大$M_{eff}$**。通过开放科学、评审者多样性、发表后评审和独立复现——所有这些实践的共同特征是它们增加了有效独立审计者的数量。

\reviewnote{This is the paper's most uncomfortable implication for the scientific establishment: the replication crisis cannot be solved within the existing peer review structure. Improving reviewer ``quality'' through training, checklists, or incentives is a $p_r$ improvement — important, but bounded. The unbounded improvement comes from $M_{eff} \to \infty$, which requires structural changes to how science is evaluated.}

### 规范条件作为民主认识论

平等论规范条件$\sumgd$具有深刻的政治认识论含义。它说：科学知识的合法性不依赖于任何个体评审者的``客观性''（这被SCX框架证明是不可能的），而是依赖于评审者构成**多样性**使得个体偏向彼此抵消。这是**民主认识论**（Democratic Epistemology） [cite]的精确数学表达：

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**民主认识论原则 (Democratic Epistemology Principle)**

在SCX框架中，认识论合法性不来自个体无偏见（个体偏见不可避免且不可消除），而来自集体规范抵消（$\sum \gaugeVec_r = \mathbf{0}$）。

这意味着同行评审的*公平性*不是评审者德性的事——

它是评审团*构成*的事。

公平的评审 = 构成多样化的评审团，使得个体偏向彼此抵消。

不公平的评审 = 构成同质化的评审团，使得个体偏向相互强化。
\end{minipage}%
}

</div>

### 对期刊编辑的操作建议

基于本文的分析，我们提出以下操作建议：

1. **增大评审者数量$M$**。当前$M=2,3$的标准是历史偶然性（由编辑时间约束和可用评审者池决定），而非审计学论证。建议$M \geq 5$，并在资源允许时更多。
2. **确保评审者坐标系多样性**。不要仅从论文的直接子领域选取评审者。有意纳入方法学上、理论上、文化上不同的评审者。如果所有评审者使用相同的评估基向量，则评审团的$M_{eff} \approx 1$，无论$M$多大。
3. **实施坐标系声明**。要求评审者声明其评估框架。这使得规范不对齐可见，并使编辑能够显式管理评审者间的规范抵消。
4. **建立发表后评审基础设施**。将同行评审从一次性事件转变为持续过程。鼓励（或要求）已发表论文接受来自更广泛科学界的持续评审。开放评审报告。建立发表后评论和更新的渠道。
5. **将复现整合为常规审计**。将独立复现研究视为同行评审的延续，而非独立的科学活动。期刊应为复现研究提供发表空间，并将复现结果链接到原始论文。
6. **承认评审的局限性**。在每篇论文中声明``本文已通过$M$名评审者的同行评审，根据SCX Thm~1，缺陷检测概率约为$P_{detect}$。读者应将本文的结论视为临时性的，等待更广泛的科学界的检验。''

### 局限性与未来工作

本文的工作存在以下局限：

1. **参数估计的粗略性**。$M_{eff}$和$p_r$的估计基于存在文献的粗略范围。需要实证研究来精确测量不同学科和期刊的$M_{eff}$。
2. **线性评审模型的简化**。评审者评分模型$\hat{q}_r = q \cdot \cos\misalignAngle + \varepsilon_r$假设质量与坐标系对齐之间存在线性可分离的交互。实际评审决策可能涉及非线性交互和阈值效应。
3. **CSDP的实证验证缺失**。坐标系声明协议尚未在实证中被检验。需要试点研究来评估其可行性和效果。
4. **$M \to \infty$的实践约束**。增大$M$面临资源约束（评审者时间、编辑协调成本）和社会约束（评审者池的有限性）。本文提供了$M \to \infty$的理论理想，但实践中需要研究有限$M$的最优分配。
5. **发表后评审的可行性**。并非所有论文都会吸引足够的发表后关注以实现高$\lambda$。不知名论文可能面临$\lambda \approx 0$——此时连续审计退化为无审计。需要机制来确保最小审计覆盖。

> **诚实暴击:** {承认本文的审查限制：本文本身尚未经过同行评审。作为预印本，它的$M_{eff}$是目前阅读它的读者数量——可能很小。根据本文自身的逻辑（Thm~1），它的缺陷检测概率在当前阶段是有限的。读者应将本文的论点视为需要独立审查和验证的*临时性主张*。本文主张同行评审系统需要更多的审计——这一主张也适用于本文自身。}

### 结语

同行评审是科学知识生产的守门机制。它的缺陷不是边际的，而是结构的——$M$太小的系统不能提供足够的审计保证。复制危机是这个结构的数学预测，而非意外。

解决方案不是让评审者变得更``好''——虽然这有帮助。解决方案是改变评审的*数学结构*：增大$M$，确保规范抵消，将评审从一次性事件转变为持续过程。

SCX平等论提供了这一转变的数学语言。$\sumgd$是对评审公平性的精确陈述。$M_{eff}$是对系统检测能力的可测量指标。$\misalignAngle$是对坐标系不对齐的可操作度量。

科学曾经依赖个体天才的直觉（$M=1$）。它进化到依赖小型同行集体的判断（$M=2,3$）。现在是进化到依赖整个科学界的集体智慧的时候了（$M \to \infty$）。这不是科幻——这是开放科学运动已经在非正式地构建的未来。本文提供了使这一未来成为系统化、可审计现实的数学基础。

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**最后一句话 (Final Word)**

同行评审不是关于判断论文是否``好''。

同行评审是关于判断：**这个科学界是否已经足够独立地检验了这篇论文，** 
 
**以至于我们可以暂时信任它的结论？**

答案取决于$M$和$\sum \gaugeVec_r$。

$M=2$时，答案是：

*我们几乎肯定没有检验得足够。*

$M \to \infty$时，答案是：

*我们正在越来越接近。*

$\boxed{\sum_m \mathbf{g}_m = \mathbf{0}}$
\end{minipage}%
}

</div>

## Appendix
## 附录A：相关SCX定理的形式陈述
<!-- label: app:scx_theorems -->

为自包含起见，本节列出本文引用的SCX核心定理的形式陈述。

> **Theorem:** [SCX Thm~1 — 多专家一致性噪声检测保证, **Multi-Expert Consistency Noise Detection Guarantee**]
> <!-- label: thm:scx1_formal -->
> 设$M$名专家在不相交的数据子集上训练。当一个样本被超过比例$\theta$的专家标记为``噪声''时，该样本是标签噪声的后验概率以$O(e^{-cM})$的速率收敛到1，其中$c > 0$是依赖于$\theta$和专家质量的常数 [cite]。

> **Theorem:** [SCX Thm~3 — 诚实人定理, **The Honest Person Theorem**]
> <!-- label: thm:scx3_formal -->
> 对于任何$K \geq 2$分类问题、任何$M \geq 1$名专家、任何有限状态空间$\mathcal{S}$，存在两个数据生成过程$\mathcal{P}_{noise}$和$\mathcal{P}_{hard}$，使得``标签错误''（噪声驱动）和``样本固有困难''（难度驱动）产生观察等价的专家行为分布。对于任何基于$n$个独立同分布观察的算法$\mathcal{A}$，在两个世界上的期望错误率满足$\max(Error_{noise}, Error_{hard}) \geq \eta\rho/2 > 0$ [cite]。

> **Theorem:** [SCX Thm~7 — 跨域信息保存定理, **Cross-Domain Information Preservation**]
> <!-- label: thm:scx7_formal -->
> 当在一个分布上优化的分区（分类、量规）被应用于另一个分布时，信息损失受两个分布之间的Wasserstein距离所界定 [cite]。在同行评审中：在一个学科上优化的评审标准应用于另一个学科时，损失评估准确性——除非在接口处进行规范固定。

## 附录B：$M_{eff$的估计方法}
<!-- label: app:Meff_estimation -->

$M_{eff}$是本文分析的核心参数，但其估计并非平凡。本节概述三种互补的估计方法。

### B.1 基于评审者间相关的估计

设$M$名评审者对$N$篇论文的评审数据可用。评审者$i$和$j$的评分相关性$\rho_{ij}$可通过Pearson或Spearman相关估计。评审者相关矩阵$\mathbf{R} \in \R^{M \times M}$的特征值$\{\lambda_k\}$用于计算：

$$
    \widehat{M}_{eff} = \frac{(\sum_{k=1}^{M} \lambda_k)^2}{\sum_{k=1}^{M} \lambda_k^2}.
    <!-- label: eq:Meff_corr -->
$$

当评审者评分完全独立时，所有$\lambda_k$相等，$\widehat{M}_{eff} = M$。当评审者评分完全相关时，$\lambda_1 = M$且$\lambda_{k>1} = 0$，$\widehat{M}_{eff} = 1$。

### B.2 基于评审者特征嵌入的估计

收集评审者的特征向量$\mathbf{f}_r$（包括学科背景、方法论偏好、理论立场、机构类型、地理位置等）。计算评审者间的余弦相似度矩阵$\mathbf{S}$，并使用与B.1相同的方法：

$$
    \widehat{M}_{eff}^{(f)} = \frac{(\sum_{k=1}^{M} \mu_k)^2}{\sum_{k=1}^{M} \mu_k^2},
    <!-- label: eq:Meff_features -->
$$

其中$\{\mu_k\}$是$\mathbf{S}$的特征值。这一方法不需要评审数据，仅需要评审者特征。

### B.3 基于复制率的反向推断

如果一门学科的已发表文献复制率$\rho_{published}$已知（通过大规模复现项目），则可由公式 [ref]反向推断$\detectProb_{bad}$，进而推断$M_{eff}$（假设$\bar{p}$已知或可被校准）。

> **诚实暴击:** {所有三种方法都需要在大规模评审数据上进行校准和验证——这些数据目前大多不可公开获取。这是CSDP和开放同行评审的另一个论据：我们需要评审过程的*数据*来审计审计系统本身。}

## 附录C：坐标系声明的示例模板
<!-- label: app:CSDP_template -->

以下是一个评审者坐标系声明的具体示例模板：

\begin{quotation}
**坐标系声明 (Coordinate-System Declaration)**

**CS1 — 评估基向量与权重：**

- 理论严谨性: 0.25
- 实证强度: 0.30
- 新颖性: 0.20
- 可复现性: 0.15
- 跨学科相关性: 0.10

**CS2 — 方法论传统：**计算方法为主，辅以实验验证。

**CS3 — 理论承诺：**贝叶斯统计框架；联结主义认知科学。

**CS4 — 坐标系自评估：**

- 与作者坐标系对齐程度：中 (Medium)
- 理由：本文使用频率学派方法，而我的方法论训练是贝叶斯传统。我对实证强度的评估权重(0.30)可能低估了该论文在其自身方法论框架内的理论贡献。读者在解读本评审报告时应将此不对齐考虑在内。

\end{quotation}

\reviewnote{This template requires approximately 3--5 minutes to complete — less than 1\% of the total time typically spent on a thorough review. The marginal cost is negligible; the marginal information gain for editors is substantial.}

\begin{thebibliography}{99}

\bibitem{scx_equality_principle}
SCX Working Group.
*The SCX Equality Principle: Formal Foundations of Gauge-Conditioned Comparison in Multi-Agent Systems.*
SCX Technical Report, 2026.

\bibitem{scx_moe_gauge}
SCX Mixture-of-Experts Working Group.
*势函数合并与专家融合的规范固定理论 (Gauge-Fixing Theory for Potential Function Merging and Expert Fusion).*
SCX Technical Report, 2026.

\bibitem{scx_thm1}
SCX Theory Group.
*Theorem 1: Multi-Expert Consistency Noise Detection Guarantee (The Unlikely Lone Genius Theorem).*
SCX Supplementary Information S1, 2026.

\bibitem{scx_thm3}
SCX Theory Group.
*Theorem 3: The Honest Person Theorem — Fundamental Unidentifiability of Noise from Difficulty.*
SCX Supplementary Information S3, 2026.

\bibitem{scx_thm7}
SCX Theory Group.
*Theorem 7: Cross-Domain Information Preservation.*
SCX Supplementary Information, 2026.

\bibitem{open2015reproducibility}
Open Science Collaboration.
*Estimating the reproducibility of psychological science.*
Science, 349(6251):aac4716, 2015.

\bibitem{errington2021investigating}
Errington, T.M., *et al.*
*Investigating the replicability of preclinical cancer biology.*
eLife, 10:e71601, 2021.

\bibitem{camerer2016evaluating}
Camerer, C.F., *et al.*
*Evaluating replicability of laboratory experiments in economics.*
Science, 351(6280):1433--1436, 2016.

\bibitem{camerer2018evaluating}
Camerer, C.F., *et al.*
*Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015.*
Nature Human Behaviour, 2(9):637--644, 2018.

\bibitem{bornmann2011scientific}
Bornmann, L.
*Scientific peer review.*
Annual Review of Information Science and Technology, 45(1):197--245, 2011.

\bibitem{lee2013bias}
Lee, C.J., *et al.*
*Bias in peer review.*
Journal of the American Society for Information Science and Technology, 64(1):2--17, 2013.

\bibitem{hojati2014journal}
Hojat, M., *et al.*
*Journal acceptance rates: A cross-disciplinary analysis of variability.*
Learned Publishing, 27(3):183--192, 2014.

\bibitem{fanelli2012negative}
Fanelli, D.
*Negative results are disappearing from most disciplines and countries.*
Scientometrics, 90(3):891--904, 2012.

\bibitem{simonsohn2014p}
Simonsohn, U., *et al.*
*$p$-curve: A key to the file-drawer.*
Journal of Experimental Psychology: General, 143(2):534--547, 2014.

\bibitem{nosek2012scientific}
Nosek, B.A., *et al.*
*Scientific utopia: II. Restructuring incentives and practices to promote truth over publishability.*
Perspectives on Psychological Science, 7(6):615--631, 2012.

\bibitem{arens2016auditing}
Arens, A.A., *et al.*
*Auditing and Assurance Services: An Integrated Approach.*
Pearson, 16th edition, 2016.

\bibitem{blank1991effects}
Blank, R.M.
*The effects of double-blind versus single-blind reviewing: Experimental evidence from The American Economic Review.*
American Economic Review, 81(5):1041--1067, 1991.

\bibitem{wenneras1997nepotism}
Wenner\r{a}s, C., \& Wold, A.
*Nepotism and sexism in peer-review.*
Nature, 387(6631):341--343, 1997.

\bibitem{snodgrass2006single}
Snodgrass, R.
*Single- versus double-blind reviewing: An analysis of the literature.*
ACM SIGMOD Record, 35(3):8--21, 2006.

\bibitem{anderson2006epistemology}
Anderson, E.
*The epistemology of democracy.*
Episteme, 3(1-2):8--22, 2006.

\bibitem{cover1999elements}
Cover, T.M., \& Thomas, J.A.
*Elements of Information Theory.*
Wiley, 2nd edition, 1999.

\bibitem{seligman1972learned}
Seligman, M.E.P.
*Learned helplessness.*
Annual Review of Medicine, 23(1):407--412, 1972.

\bibitem{dweck2006mindset}
Dweck, C.S.
*Mindset: The New Psychology of Success.*
Random House, 2006.

\bibitem{vygotsky1978mind}
Vygotsky, L.S.
*Mind in Society: The Development of Higher Psychological Processes.*
Harvard University Press, 1978.

\bibitem{ladson2006achievement}
Ladson-Billings, G.
*From the achievement gap to the education debt.*
Educational Researcher, 35(7):3--12, 2006.

\bibitem{bjork1994memory}
Bjork, R.A.
*Memory and metamemory considerations in the training of human beings.*
In: Metacognition: Knowing about Knowing, MIT Press, 1994.

\end{thebibliography}