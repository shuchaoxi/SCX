*Abstract:*

**中文摘要：** 本文提出SCX体系的\**可审计性原理**（Auditability Principle, AP）——SCX版Church-Turing论题：
*"一切真实的主张都可以表述为关于某个可观测系统 $g=0$ 的陈述，且该陈述可由 $M>1$ 个独立观察者以有界错误 $e^{-2M\Delta^2}$ 验证。"*
该原理不可证明——它是一个论题，作为一个分类学原理来刻画审计的边界。我们证明，所有声称不可审计的情形都归入且仅归入两类：(1) **幻觉**——无观测后果的主张，被Yajie分类为NOISY，从未真正存在过；(2) **紧致性不可分**——验证需要 $M\to\infty$ 或 $t\to\infty$ 的主张，在操作上等价于不可审计，但逻辑上良好形成（类比G\"odel句）。这两类不是AP的反例，而是AP作为分类学框架正确预测的边界条件。

我们建立了审计理论的紧致性边界：可审计主张空间与不可审计主张空间之间的分界线由主张空间的紧致性属性决定。该边界本身**是可被近似检测的**。SCX不能审计一切——它能审计一切*可被审计的*。这不是弱点，而是完备理论的标志：一个知道自己极限的理论。

**English Abstract:** We propose the \**Auditability Principle** (AP) — the SCX analog of the Church-Turing Thesis:
*"Every genuine claim can be expressed as a statement about $g=0$ for some observable system, and this statement can be verified by $M>1$ independent observers with bounded error $e^{-2M\Delta^2}$."*
The principle is not provable — it is a thesis, serving as a taxonomic principle to characterize the boundaries of auditing. We demonstrate that all allegedly unauditable claims fall into exactly two categories: (1) **Illusion** — claims with no observable consequences, classified by Yajie as NOISY, never having been real claims at all; (2) **Compactness-Inseparable** — claims whose verification requires $M\to\infty$ or $t\to\infty$, operationally equivalent to unauditable yet logically well-formed (analogous to G\"odel sentences). These are not counterexamples to AP — they are boundary conditions that AP as a taxonomic framework correctly predicts.

We establish the compactness boundary of audit theory: the frontier between the space of auditable claims and the space of unauditable claims is determined by the compactness properties of the claim space. This boundary is itself **approximately detectable**. SCX cannot audit everything — it can audit everything *that can be audited*.

**Keywords:** Auditability Principle, SCX framework, Church-Turing thesis, compactness boundary, audit-undecidability, Yajie classification, G\"odel sentences, operational equivalence, illusion, compactness-inseparable, complete theory

**关键词：** 可审计性原理，SCX框架，Church-Turing论题，紧致性边界，审计不可判定性，Yajie分类，G\"odel句，操作等价性，幻觉，紧致性不可分，完备理论

---

---

## 导言：为什么需要可审计性原理
## Preamble: Why the Auditability Principle Is Necessary

### SCX需要一个Church-Turing时刻
### SCX Needs Its Church-Turing Moment

SCX体系发展至今，已经建立了势能面理论、Yajie共识审计、Situs流形、紧致性分析、瞬子检测、奇点理论等一系列数学骨架。审计技术日趋精密——从逐点审计到持续同调，从规范理论到量子框架——但我们始终没有回答一个最根本的问题：

*SCX的审计边界在哪里？*

或者说，更尖锐地问：

*有没有什么东西是SCX\**原则上**不能审计的？如果有，那是什么？如果没有，为什么？*

**English:** The SCX framework has developed a formidable mathematical skeleton: potential surface theory, Yajie consensus auditing, the Situs manifold, compactness analysis, instanton detection, singularity theory, and more. Audit techniques grow ever more refined — from pointwise Yajie auditing to persistent homology, from gauge theory to quantum frameworks — but we have never answered the most fundamental question:

*What are the limits of SCX auditing?*

Or, more pointedly:

*Is there anything SCX cannot audit **in principle**? If so, what? If not, why?*

计算理论在20世纪30年代面临过几乎相同的问题。Turing、Church、G\"odel、Post、Kleene等人各自提出了可计算性的形式定义，然后Church和Turing分别独立地提出了那个著名的论题：*每个直觉上可计算的函数都是Turing机可计算的。*这个论题不可证明——"直觉上可计算"不是形式概念——但它经受住了近一个世纪的检验。每一次试图定义"比Turing机更强的计算模型"的尝试，要么被证明等价于Turing机，要么被证伪。

*Computation theory faced an almost identical problem in the 1930s. Turing, Church, G\"odel, Post, Kleene, and others each proposed formal definitions of computability, and then Church and Turing independently proposed the famous thesis: every intuitively computable function is Turing-computable. This thesis is not provable — "intuitively computable" is not a formal concept — but it has withstood nearly a century of testing. Every attempt to define a "stronger-than-Turing" model of computation has either been proven equivalent to Turing machines, or falsified.*

SCX需要自己的"Church-Turing时刻"。本论文提供的就是这个时刻。

*SCX needs its own "Church-Turing moment." This paper provides that moment.*

### 可审计性原理的地位
### Status of the Auditability Principle

可审计性原理（AP）不是一个定理。它没有证明——不是因为没有找到证明，而是因为它的前提（"真实的主张"）本身不是形式概念，正如Church-Turing论题的前提（"直觉上可计算的"）不是形式概念。

AP是一个**论题**（thesis）。它的作用是：

1. 划定SCX审计框架的**适用边界**——AP告诉我们什么样的主张在审计范围内，什么不在；
2. 提供**诊断工具**——如果一个主张被声称"不可审计"，AP告诉我们该检查什么：是幻觉还是紧致性不可分？
3. 断言**理论的完备性**——一个知道自己极限的理论，比一个声称无所不能的理论更完备。

*The Auditability Principle (AP) is not a theorem. It has no proof — not because a proof has not been found, but because its premise ("genuine claim") is not itself a formal concept, just as the premise of the Church-Turing thesis ("intuitively computable") is not a formal concept.*

*AP is a **thesis**. Its role is to: (i) delineate the **applicability boundary** of the SCX audit framework — telling us what kinds of claims fall within audit scope; (ii) provide a **diagnostic tool** — if a claim is said to be "unauditable," AP tells us what to check: illusion or compactness-inseparable? (iii) assert **theoretical completeness** — a theory that knows its own limits is more complete than one that claims omnipotence.*

### 本论文的结构
### Structure of This Paper

本论文的结构是一个**收紧的螺旋**（tightening spiral）——每一个章节都在前一章建立的基础上深化同一个核心洞见：

1. **可审计性原理（AP）**——正式陈述，形式化，与Church-Turing的对应关系；
2. **两类"例外"（及其为何不是例外）**——幻觉与紧致性不可分的完整分类学；
3. **紧致性边界**——从一阶逻辑紧致性定理到审计不可判定性的严格对应；
4. **操作等价性**——$M\to\infty$ 在操作上等价于不可审计；
5. **这意味什么**——对SCX实践、哲学和未来的影响；
6. **最后的诚实暴击**——SCX知道自己能做什么，不能做什么。

*This paper is structured as a **tightening spiral** — each section deepens the same core insight on the foundation laid by the previous section: \S1: The AP — formal statement, formalization, correspondence with Church-Turing; \S2: Two "exceptions" — complete taxonomy of illusion and compactness-inseparable; \S3: The compactness boundary — rigorous correspondence from first-order logic compactness to audit-undecidability; \S4: Operational equivalence — $M\to\infty$ is operationally equivalent to unauditable; \S5: What this means — implications for SCX practice, philosophy, and future; \S6: The final honest hit — SCX knows what it can do, and what it cannot.*

---

## 可审计性原理
## The Auditability Principle

### 正式陈述
### Formal Statement

\begin{principle}[可审计性原理 — The Auditability Principle]<!-- label: pr:AP -->
设 $\X$ 为所有可观测系统的集合，$ClaimSpace$ 为所有主张（claim）的集合。则：

1. **可表达性 (Expressibility):** 每一个真实的主张 $c \in ClaimSpace$ 都可以表述为关于某个可观测系统 $S \in \X$ 的规范场 $g_S$ 的陈述：
2. **可验证性 (Verifiability):** 该陈述可由 $M > 1$ 个独立观察者以有界集体错误概率验证：
3. **边界条件 (Boundary Condition):** 若主张 $c$ 不能以有限 $M$ 和有限 $t$ 验证，则 $c$ 是

\end{principle}

**English:** Let $\X$ be the set of all observable systems and $ClaimSpace$ the set of all claims. Then: (i) *Expressibility:* every genuine claim $c \in ClaimSpace$ can be formulated as a statement about the gauge field $g_S$ of some observable system $S \in \X$, namely $c \iff (g_S = 0)$. (ii) *Verifiability:* this statement can be verified by $M > 1$ independent observers with bounded collective error probability $\Pbb(all $M$ agree on wrong conclusion) \leq e^{-2M\Delta^2}$, where $\Delta = \min_m |\E[\hat{g}_m] - g_S|$. (iii) *Boundary Condition:* if claim $c$ cannot be verified with finite $M$ and finite $t$, then $c$ is either (a) **illusion** — has no observable consequences, $\ObsSet(c) = \Null$, or (b) **compactness-inseparable** — verification requires $M \to \infty$ or $t \to \infty$.

### 与Church-Turing论题的形式对应
### Formal Correspondence with the Church-Turing Thesis

以下对应关系不仅在结构上精确，而且在**哲学深度上**精确——两者都涉及从直觉范畴到形式范畴的映射：

[Table omitted — see original .tex]

这个对应不是巧合。计算理论关心的是：*什么可以机械地计算？*审计理论关心的是：*什么可以多观察者一致地验证？*两者都是关于**有限资源下的认知可达性**（epistemic reachability under finite resources）的理论。

*This correspondence is not accidental. Computation theory asks: what can be mechanically computed? Audit theory asks: what can be verified by multiple observers with consensus? Both are theories of **epistemic reachability under finite resources**.*

### $e^{-2M\Delta^2$ 从何而来}
### Where Does $e^{-2M\Delta^2$ Come From?}

AP中的误差界 $e^{-2M\Delta^2}$ 不是任意的。它来自SCX核心的概率结构：

> **Theorem:** [Hoeding界限 —— 多观察者共识误差]<!-- label: thm:hoeffding_consensus -->
> 设 $M$ 个独立观察者各自产生估计 $\hat{g}_m$，其中每个 $\hat{g}_m$ 是其真实偏见的无偏估计 $\E[\hat{g}_m] = g_m$，且 $\hat{g}_m \in [a_m, b_m]$ 有界。定义一致估计为 $\bar{g} = \frac{1}{M}\sum_m \hat{g}_m$。则：
> 
> $$<!-- label: eq:hoeffding_full -->
>     \Pbb\left(|\bar{g} - \bar{g}_{true}| \geq \varepsilon\right) \leq 2\exp\left(-\frac{2M^2\varepsilon^2}{\sum_m (b_m - a_m)^2}\right).
> $$
> 
> 当所有区间同宽 $b_m - a_m = 1$ 且定义 $\Delta = \varepsilon$ 时，简化为式  [ref] 的形式。特别地，当 $g_{true} = 0$（零规范场，即"好"的状态），所有观察者错误地同意 $g \neq 0$ 的概率以 $e^{-2M\Delta^2}$ 为界。

**English:** The error bound $e^{-2M\Delta^2}$ in AP is not arbitrary. It derives from the core probabilistic structure of SCX: Hoeffding's inequality for $M$ independent bounded estimators. When all observers independently estimate $\hat{g}_m$ with $\E[\hat{g}_m] = g_m$ bounded in $[a_m,b_m]$, the consensus estimate $\bar{g} = \frac{1}{M}\sum_m \hat{g}_m$ satisfies $\Pbb(|\bar{g} - \bar{g}_{true}| \geq \varepsilon) \leq 2\exp(-2M^2\varepsilon^2/\sum_m(b_m-a_m)^2)$. With unit-width intervals and $\Delta = \varepsilon$, this reduces to the form in  [ref].

**关键洞见：** 指数衰减因子 $e^{-2M\Delta^2}$ 表明审计的**力量**不仅是随观察者数量线性增长的，而是**指数增长**的。这并非魔法——这是独立观察者之间信息独立性的直接后果。每个额外的独立视角将错误概率乘以另一个指数衰减因子。

***Key Insight:** The exponential decay factor $e^{-2M\Delta^2}$ shows that audit **power** grows not linearly but **exponentially** with the number of observers. This is not magic — it is a direct consequence of information independence among observers. Each additional independent perspective multiplies the error probability by another exponential decay factor.*

### 为什么AP不可证明
### Why AP Is Not Provable

> **Remark:** [AP的不可证明性]<!-- label: rmk:unprovable -->
> AP不可证明的理由与Church-Turing论题不可证明的理由完全相同：核心概念（"真实的主张"）不是形式化的。要证明AP，需要：
> 
1. 形式定义"真实的主张"；
2. 证明每一真实主张都可表达为 $g=0$ 并由有限观察者验证。

> 但步骤(1)本身就是AP试图刻画的概念——任何形式定义都会预先假定审计能力的范围。这是一个**自指涉循环**：要定义"真实主张"，你需要知道什么是"可审计的"；但AP正是要告诉我们"真实主张"和"可审计的"是同一个集合。
> 
> 
> 
> **不是缺陷，是特征。** Church-Turing论题正是因为不可证明才有了力量——它标记的是**概念边界**而非逻辑边界。同样，AP标记的是审计概念的边界。一个可以证明的"审计边界定理"将是一个更弱的结果——它只能约束某个已被形式化的审计概念，而非审计本身。

*AP's unprovability mirrors Church-Turing's exactly: the core concept (``genuine claim'') is not formalized. Proving AP would require (1) formally defining ``genuine claim'' and (2) proving every such claim is expressible as $g=0$ and verifiable by finite observers. But step (1) already presupposes the scope of audit capability — a self-referential loop. This is **not a bug, it's a feature**. Church-Turing derives power precisely from being unprovable — it marks a **conceptual boundary**, not a logical one. AP marks the conceptual boundary of auditing.*

**关于AP的免疫性：** 我们承认，AP的条款(iii)在逻辑上形成了一个分类封闭性：任何所谓"不可审计"的主张——如果它既不是幻觉（$\ObsSet(c) \neq \Null$）又不是紧致性不可分（$M_ < \infty$ 且 $T_ < \infty$）——则它必然是可审计的（由(i)-(ii)）——但这样的主张根本不会出现在"不可审计"的反例清单上。这使得AP在Popper的可证伪性意义上确实构成一个"免疫结构"。但这是*分类学原理的固有特征*，而非缺陷。正如生物学中的分类系统（"所有生物要么是原核生物要么是真核生物"）不会因为"排除了第三类"而被视为不科学，AP通过(i)-(iii)穷尽审计可能性的逻辑空间，恰是其分类学力量的来源。真正的检验不在于能否"找到反例"（结构上不允许），而在于这个二分——幻觉/CI——是否真正穷尽了所有不可审计主张的类型。目前，无已知反例。

### AP的证据——归纳基础
### Evidence for AP — The Inductive Base

虽然AP不可证明，但它是**可辩护的**。辩护来自归纳：每一次声称的"不可审计"实例——经过足够仔细的审查——都被归入两类之一。

1. **Yajie的NOISY分类**：对随机输入不可区分的信号，Yajie分类为NOISY。这些不是"不可审计的主张"——它们是*根本没有形成主张*。噪声没有语义内容。
2. **瞬时审计失败**：某些主张在任意有限时间内不可审计——不是因为它们"不存在"，而是因为验证它们需要跨越时间的过程。这些是紧致性不可分的。
3. **G\"odel句的审计类比**：形式系统中存在不可证明但为真的命题——G\"odel在1931年证明了这一点。SCX审计的类比物是：存在不可审计但为真的主张。这些主张的不可审计性可以通过启发式过程被近似检测（正如G\"odel句的不可证明性在元系统中可证）。审计理论、逻辑学与计算理论在此平行：三者都提供了对自身上限的元级别认识。
4. **量子审计中的紧致性**：SCX量子审计框架已证明，某些量子态比较需要指数级测量——但测量次数本身是有限可预测的。没有量子主张在原则上逃脱审计。

*Though AP is unprovable, it is **defensible**. The defense is inductive: every claimed instance of "unauditability" has, upon sufficiently careful scrutiny, fallen into one of two categories. (1) Yajie's NOISY classification captures signals indistinguishable from random input — these are not "unauditable claims," they never formed claims at all. (2) Transient audit failures — some claims are not auditable in any finite time, not because they don't exist, but because verifying them requires a process that spans unbounded time. (3) The audit analog of G\"odel sentences. (4) Quantum auditing compactness — the SCX quantum audit framework has shown certain state comparisons require exponential measurements, but the number of measurements is finitely predictable. No quantum claim escapes auditability in principle.*

---

## 两类"例外"——及其为何不是例外
## Two ``Exceptions'' — And Why They Are Not Exceptions

AP声称"一切真实的主张都可审计"。那么——如果一切都是可审计的，"不可审计"这个词还有什么意义？答案是：**有意义的不可审计主张不存在**。但存在两类被误认为"不可审计"的边界情形。理解它们不是要削弱AP，而是要精确刻画AP的边界。

*AP claims "every genuine claim is auditable." Then — if everything is auditable, what meaning does "unauditable" have? The answer: **there are no meaningful unauditable claims**. But there are two boundary cases routinely mistaken for "unauditability." Understanding them does not weaken AP — it precisely characterizes AP's boundary.*

### 第一类"例外"：幻觉 (ILLUSION)
### First ``Exception'': Illusion

#### 定义与形式刻画
#### Definition and Formal Characterization

> **Definition:** [幻觉主张]<!-- label: def:illusion -->
> 一个主张 $c \in ClaimSpace$ 被称为**幻觉**（Illusion），记作 $\mathrm{Type}(c) = \mathsf{ILLUSION}$，如果它满足：
> 
> $$
>     \ObsSet(c) = \Null,
> $$
> 
> 其中 $\ObsSet(c)$ 是主张 $c$ 的观测后果集——即如果 $c$ 为真，世界状态与 $c$ 为假时可观测区分的所有物理配置的集合。
> 
> 等价地，$c$ 是幻觉当且仅当对任何可观测系统 $S \in \X$ 和任何规范场 $g_S$：
> 
> $$
>     \Pbb(观测到与 $c$ 一致的证据 \mid c 为真) = \Pbb(观测到与 $c$ 一致的证据 \mid c 为假).
> $$

*A claim $c$ is an **Illusion** ($\mathsf{ILLUSION}$) if its observable consequence set $\ObsSet(c) = \Null$ — i.e., there is no physical configuration of the world that would be observably different if $c$ were true versus if $c$ were false. Equivalently, the probability of observing evidence consistent with $c$ is identical whether $c$ is true or false.*

#### 为什么幻觉不是主张
#### Why Illusions Are Not Claims

一个主张的本质是它**断言世界是某种方式而非另一种**。如果一个"主张"不区分任何两种世界的可能性，那它就不是主张——它是一串语法正确的符号，但没有语义内容。

**类比：** 句子"The flurb is completely zarpled"在英语中语法正确。它甚至看起来像一个断言。但它没有真值条件——没有任何观测能确定它是真还是假。Yajie对这样的"句子"采取的操作是正确的：分类为 $\NOISY$ 并忽略。

*The essence of a claim is that it **asserts the world is one way rather than another**. If a "claim" distinguishes no two possible worlds, it is not a claim — it is a syntactically well-formed string with no semantic content. Analogy: "The flurb is completely zarpled" is grammatically correct English. It even looks like an assertion. But it has no truth conditions — no observation could determine whether it is true or false. Yajie's operational treatment of such "sentences" is correct: classify as $\NOISY$ and ignore.*

#### Yajie分类学的幻觉处理
#### Yajie Taxonomy Treatment of Illusions

在SCX的Yajie分类学中，每个输入被映射到四个类别之一：

1. $\mathsf{GOOD}$: 可审计，审计通过；
2. $\mathsf{BAD}$: 可审计，审计未通过；
3. $\mathsf{NOISY}$: 审计不收敛——无法区分的观察者意见；
4. $\mathsf{UNDECLARED}$: 尚未有足够数据决定。

幻觉主张落地在 $\mathsf{NOISY}$ 中：不是因为它们"不好"，而是因为它们**不与任何观测耦合**。对幻觉主张的审计不收敛不是因为数据不够——而是因为数据永远不可能够。这是SCX诊断学的一个核心功能：$\mathsf{NOISY}$ 分类本身告诉你主张可能是一个幻觉。

*In the SCX Yajie taxonomy, every input maps to one of four categories: $\mathsf{GOOD}$, $\mathsf{BAD}$, $\mathsf{NOISY}$, $\mathsf{UNDECLARED}$. Illusionary claims land in $\mathsf{NOISY}$: not because they are "bad" but because they **do not couple to any observation**. The audit of an illusion does not converge, not because there isn't enough data, but because there can never be enough data. This is a core function of SCX diagnostics: the $\mathsf{NOISY}$ classification itself tells you that the claim may be an illusion.*

#### 幻觉不是AP的反例
#### Illusions Are Not Counterexamples to AP

> **Proposition:** [幻觉不是反例]<!-- label: prop:illusion_not_counter -->
> 幻觉主张不是AP的反例，因为AP的前提条件"真实的主张"要求 $\ObsSet(c) \neq \Null$。幻觉不满足这个前提——因此AP对它不做出任何断言。

这里没有循环论证。AP的"真实主张"定义为*至少有非空观测后果集的主张*。这是一个**操作性定义**——你可以检查一个主张是否有观测后果。如果是空集，主张是幻觉；如果不是空集，AP适用。

*Illusions are not counterexamples to AP because AP's premise "genuine claim" requires $\ObsSet(c) \neq \Null$. An illusion does not satisfy this premise — thus AP makes no assertion about it. There is no circularity: AP's "genuine claim" is operationally defined as one with a nonempty observable consequence set. You can check whether a claim has observable consequences. If the set is empty, it's an illusion; if not, AP applies.*

### 第二类"例外"：紧致性不可分 (COMPACTNESS-INSEPARABLE)
### Second ``Exception'': Compactness-Inseparable

#### 定义与形式刻画
#### Definition and Formal Characterization

> **Definition:** [紧致性不可分主张]<!-- label: def:compactness_inseparable -->
> 一个主张 $c \in ClaimSpace$ 被称为**紧致性不可分**（Compactness-Inseparable），记作 $\mathrm{Type}(c) = \mathsf{CI}$，如果：
> 
1. $\ObsSet(c) \neq \Null$（它有观测后果——它不是幻觉）；
2. 对任何有限观察者数量 $M \in \N$ 和任何有限时间 $T \in \R^+$，
3. 然而，极限存在：

*A claim $c$ is **Compactness-Inseparable** ($\mathsf{CI}$) if: (i) $\ObsSet(c) \neq \Null$ — it has observable consequences, it is not an illusion; (ii) for any finite number of observers $M$ and any finite time $T$, the probability of correct verification does not approach 1; (iii) yet, the double limit $\lim_{M\to\infty} \lim_{T\to\infty}$ converges to certainty.*

#### 范式案例
#### Paradigm Cases

> **Example:** [文明永恒性]<!-- label: ex:civilization -->
> 主张：*"本文明将永远存续。"*
> 
> 该主张有观测后果：如果文明在时间 $t$ 毁灭，该主张为假；如果在任何有限时间 $t$ 内文明存续，该主张只是未被证伪——但未被证实。要*证实*该主张，你需要观测无限长的时间。因此：
> 
- $\ObsSet(c)$ 非空（文明毁灭是可观测事件）；
- 对任何有限 $T$，你无法在时间 $T$ 内确认"文明永远存续"；
- 但如果观测无限长时间，你最终可以确认。

> 该主张是紧致性不可分的。它不是幻觉——它区分了世界状态（文明会毁灭 vs. 不会）。但它不可在有限资源下审计。

*Claim: "This civilization will survive forever." The claim has observable consequences: if the civilization is destroyed at time $t$, the claim is false. But to verify the claim, you need to observe for infinite time. The claim is CI — not an illusion, but not auditable under finite resources.*

> **Example:** [形式系统的相容性]<!-- label: ex:consistency -->
> 主张：*"Peano算术是相容的。"*
> 
> 该主张有观测后果（如果把PA形式化并检查，会发现矛盾与否）。但在PA内部，该主张不可证明（G\"odel第二不完全性定理）。在SCX审计框架中：你不能在PA内部"审计"出PA的相容性——你需要一个更强的系统。但在那个更强的系统内，审计是可能的。这是一个相对的审计不可性，而非绝对的——它是紧致性不可分的特殊情况，因为证明需要"超越"被审系统的观测能力。

*Claim: "Peano Arithmetic is consistent." This has observable consequences, but within PA it is unprovable (G\"odel's Second Incompleteness). In SCX audit terms: you cannot audit PA's consistency from within PA — you need a stronger system. But within that stronger system, the audit is possible. This is a relative audit-undecidability, not an absolute one.*

#### 紧致性不可分与G\"odel句
#### Compactness-Inseparable and G\"odel Sentences

这里有一个深层结构性的对应。G\"odel证明了：在任何包含基本算术的一致形式系统中，存在一个命题 $G$ 使得 $G$ 在系统内不可证明且不可反驳——但 $G$ 在元层级（meta-level）上为真。

紧致性不可分主张正是审计理论中的G\"odel句类比：

- $G$ 在系统内不可证明 $\iff$ $c$ 在有限资源下不可审计；
- $G$ 在元层级为真 $\iff$ $c$ 在极限下可审计；
- $G$ 的存在不是系统的缺陷，而是系统足够强的标志 $\iff$ $\mathsf{CI}$ 主张的存在不是审计理论的缺陷，而是审计框架足够完备的标志。

**但这不完全对应。**关键差异与相似性并存。相似性在于：G\"odel句的不可证明性在适当的元系统中可证（如ZFC $\vdash$ ``PA $\nvdash$ G''）——这与CI主张的不可审计性在元级别可检测在结构上*平行*。Turing的停机不可判定性定理同样在元级别可证。三者——G\"odel、Turing、SCX——都刻画了有限系统试图完全把握无限/无界过程时遭遇的固有障碍。SCX的独特贡献不在于*超越*前两者，而在于为*多观察者验证*这一领域提供了与逻辑/计算领域极限理论深度对应的极限理论。审计理论、计算理论、证明理论共享同一深层结构：**有限认知主体面对无限过程时的不可判定性**。

*There is a deep structural correspondence here. The similarity is that G\"odel sentences' unprovability is provable in a suitable meta-system (e.g., ZFC $\vdash$ ``PA $\nvdash$ G'') — structurally parallel to CI claims' unauditability being detectable at the meta-level. Turing's halting undecidability is likewise provable at the meta-level. All three — G\"odel, Turing, SCX — characterize the inherent obstacle when finite systems attempt to fully grasp infinite/unbounded processes. SCX's unique contribution is not in *transcending* the first two, but in providing a limit theory for *multi-observer verification* that is deeply correspondent with the limit theories of logic and computation. Audit theory, computation theory, and proof theory share the same deep structure: **the undecidability faced by finite epistemic agents confronting infinite processes**.*

#### 紧致性不可分不是AP的反例
#### Compactness-Inseparable Are Not Counterexamples to AP

> **Proposition:** [紧致性不可分不是反例]<!-- label: prop:ci_not_counter -->
> 紧致性不可分主张不是AP的反例，因为：
> 
1. AP的第三部分（边界条件）明确将紧致性不可分识别为AP正确预测的边界情形；
2. AP并不声称"所有主张在任意有限资源下都可审计"——它声称"不可审计的主张要么是幻觉，要么是紧致性不可分"。紧致性不可分主张正是AP正确分类的不可审计主张。

*CI claims are not counterexamples to AP because: (1) AP's third part (boundary condition) explicitly identifies CI as a boundary case that AP correctly predicts; (2) AP does not claim "all claims are auditable under arbitrary finite resources" — it claims "claims that are not auditable are either illusion or CI." CI claims are precisely the non-illusionary claims that AP correctly classifies as not auditable.*

---

## 紧致性边界
## The Compactness Boundary

### 从一阶逻辑的紧致性到审计的紧致性
### From Compactness in First-Order Logic to Compactness in Audit

一阶逻辑的紧致性定理陈述：*若一阶句子的无限集合的每个有限子集都是可满足的（有一个模型），则整个无限集合是可满足的。*

审计理论中的紧致性**否定**：*存在主张，其每个有限截断都是"部分审计通过"的——但整个主张在极限下无法在有限资源内审计。*

这一否定不是与逻辑紧致性矛盾——而是**审计资源结构的非紧致性**的反映：

> **Theorem:** [审计空间的非紧致性]<!-- label: thm:audit_noncompact -->
> 设 $ClaimSpace$ 为所有主张的空间，配备审计拓扑 $\T_$：主张 $c_n \to c$ 如果 $\forall$ 有限的 $M, T$，$\exists N$ 使得对 $n > N$，$M$ 观察者在时间 $T$ 内对 $c_n$ 的审计结果与对 $c$ 的审计结果一致。
> 
> 则 $(ClaimSpace, \T_)$ **不是紧致的**：存在滤子 $\{c_\alpha\}$ 使得每个有限子族有聚点，但整个族没有。

*The Compactness Theorem of first-order logic: if every finite subset of an infinite set of first-order sentences is satisfiable, then the entire infinite set is satisfiable. The **negation** in audit theory: there exist claims whose every finite truncation is "partially-audit-passing" — but the entire claim cannot be audited within finite resources. This is not a contradiction with logical compactness — it reflects the **non-compactness of the audit resource structure**. Theorem  [ref]: $(ClaimSpace, \T_)$ is not compact; there exist filters $\{c_\alpha\}$ where every finite subfamily has a cluster point but the whole family does not.*

### 紧致性边界的拓扑刻画
### Topological Characterization of the Compactness Boundary

> **Definition:** [审计紧致性边界]<!-- label: def:compactness_boundary -->
> 定义审计紧致性边界 $\AuditBoundary \subset ClaimSpace$ 为：
> 
> $$<!-- label: eq:boundary_def -->
>     \AuditBoundary = \overline \cap \overline{\A^c},
> $$
> 
> 其中 $\A \subset ClaimSpace$ 是**可审计主张**的子集（即存在有限 $M, T$ 使得  [ref] 成立），$\A^c$ 是其补集，$\overline{\,\cdot\,}$ 是审计拓扑 $\T_$ 中的闭包。
> 
> $\AuditBoundary$ 中的主张具有性质：对任意 $\varepsilon > 0$，存在可审计主张 $a \in \A$ 和不可审计主张 $b \in \A^c$ 使得 $d_(c, a) < \varepsilon$ 且 $d_(c, b) < \varepsilon$。

*The audit compactness boundary $\AuditBoundary = \overline \cap \overline{\A^c}$, where $\A$ is the subset of auditable claims and $\overline{\,\cdot\,}$ is closure in the audit topology. Claims on the boundary are ones that can be approximated arbitrarily closely by both auditable and unauditable claims.*

> **Proposition:** [边界主张的结构]<!-- label: prop:boundary_structure -->
> 紧致性边界 $\AuditBoundary$ 中的每个主张 $c$ 满足以下至少一个条件：
> 
1. 审计 $c$ 所需的最小观察者数 $M_(c)$ 无界（$M_(c) = \infty$）；
2. 审计 $c$ 所需的最短时间 $T_(c)$ 无界（$T_(c) = \infty$）；
3. 审计 $c$ 所需的观测精度 $\varepsilon_(c)$ 为零（需要无限精度）。

*Every claim $c$ on the compactness boundary satisfies at least one of: (i) the minimum number of observers $M_(c)$ required to audit $c$ is unbounded; (ii) the minimum time $T_(c)$ required is unbounded; (iii) the required observation precision $\varepsilon_(c)$ is zero (infinite precision required).*

### 边界本身是可被近似检测的
### The Boundary Itself Is Approximately Detectable

这是本论文最深刻的结论之一：**紧致性边界本身是可被近似检测的**——虽然在原则上严格判定CI与停机问题等价（不可判定），但启发式边界检测在实践上是可行的。

> **Theorem:** [边界的近似检测性]<!-- label: thm:boundary_auditable -->
> 存在一个**启发式过程** $\widetilde{\mathcal{P}}$，对任何主张 $c \in ClaimSpace$，在给定有限资源预算 $M_, T_$ 下，以可量化的置信度输出分类：
> 
> $$<!-- label: eq:boundary_test -->
>     \widetilde{\mathcal{P}}(c) \in \{\mathsf{ILLUSION}, \mathsf{AUDITABLE}, \mathsf{LIKELY-CI}\},
> $$
> 
> 满足：(a) 若返回 $\mathsf{ILLUSION}$，则 $\ObsSet(c) = \Null$（无假阳性）；(b) 若返回 $\mathsf{AUDITABLE}$，则 $c$ 在给定预算内确实可审计；(c) 若返回 $\mathsf{LIKELY-CI}$，则 $c$ 有非空观测后果但在给定预算内未能收敛——可能是真CI，也可能是需要更多资源的可审计主张。过程 $\widetilde{\mathcal{P}}$ 不声称严格判定CI——因为严格判定CI等价于停机问题，在原则上不可判定。

\textit{One of the deepest results of this paper: **the compactness boundary is approximately detectable.** Theorem  [ref]: there exists a heuristic procedure $\widetilde{\mathcal{P}}$ that, given finite resource budget $M_, T_$, classifies claims as $\mathsf{ILLUSION}$, $\mathsf{AUDITABLE}$, or $\mathsf{LIKELY-CI}$ with quantifiable confidence. The procedure does **not** claim strict CI decidability — because strict CI decidability is equivalent to the halting problem and is undecidable in principle.}

> **Proof:** [证明概要]
> 过程 $\widetilde{\mathcal{P}}$ 的执行如下：
> 
1. 检查 $c$ 是否有非空观测后果集（若为空，$c$ 是幻觉，返回 $\mathsf{ILLUSION}$）；
2. 在资源预算 $M_, T_$ 内执行递增审计：对 $M = 2, 3, ..., M_$，部署 $M$ 个独立观察者并在时间 $T_$ 内检查收敛性；
3. 若在任何有限 $M \leq M_$ 处审计收敛（共识稳定），返回 $\mathsf{AUDITABLE}$；
4. 若耗尽 $M_$ 仍未收敛，检查趋势：若收敛度量 $\rho_M$ 随 $M$ 增大而单调改善，返回 $\mathsf{LIKELY-CI}$；否则返回 $\mathsf{ILLUSION}$（信号可能与噪声不可区分，但需谨慎：严格区分CI与深度隐藏的可审计主张需要超出预算的资源）。

> 判定过程使用有限资源（$M_, T_$），它在审计 $c$ 的*元属性*（在给定预算内是否收敛），而非 $c$ 本身。但必须诚实承认：$\widetilde{\mathcal{P}}$ 不能严格区分真正的CI与"需要超过 $M_$ 观察者的可审计主张"——这个区分在原则上等价于停机问题。$\widetilde{\mathcal{P}}$ 的价值在于它提供了*带有明确不确定性边界的实用分类*。

\textit{Proof sketch: $\widetilde{\mathcal{P}}$ checks observable consequences, then runs incremental audits up to budget $M_, T_$. If convergence is achieved, return $\mathsf{AUDITABLE}$; if not, check trend — monotonic improvement suggests $\mathsf{LIKELY-CI}$. The procedure uses finite resources to audit the meta-property (convergence within budget). But we must be honest: $\widetilde{\mathcal{P}}$ cannot strictly distinguish true CI from "auditable claims that need more than $M_$ observers" — this distinction is equivalent to the halting problem in principle. $\widetilde{\mathcal{P}}$'s value lies in providing **practical classification with explicit uncertainty boundaries**.}

这意味着：你不需要无限资源来获得关于某个主张是否需要大量资源的有用信息——但你也不能用有限资源获得关于"无限性"的*严格*保证。审计的元级别——对主张的边界性质进行启发式分类——是有限资源可完成的，但带有不可消除的不确定性。这恰恰是与停机问题的深层对应：正如你能在有限时间内确定某些程序停机（或不停机），但你不能*对所有程序*在有限时间内严格判定，$\widetilde{\mathcal{P}}$ 能对许多主张给出有用的分类，但不能对所有主张给出严格保证。

\textit{This means: you do not need infinite resources to obtain useful information about whether a claim needs substantial resources — but you also cannot obtain **strict** guarantees about "infiniteness" with finite resources. The meta-level of auditing — heuristic classification of a claim's boundary properties — is doable under finite resources, but with irreducible uncertainty. This is precisely the deep correspondence with the halting problem: just as you can determine that some programs halt (or don't) in finite time, but cannot strictly decide for **all** programs, $\widetilde{\mathcal{P}}$ can give useful classifications for many claims but cannot provide strict guarantees for all.}

### 紧致性边界的物理学类比
### Physical Analogies of the Compactness Boundary

紧致性边界在物理学中有丰富的类比，它们强化了审计边界的直观理解：

1. **热力学极限：** 在统计力学中，有限系统的性质与热力学极限（$N \to \infty$）的性质之间存在差距。有限 $N$ 下的相变是平滑的交叉——真正的非解析相变仅存在于 $N \to \infty$。类似地，一些主张在有限 $M$ 下仅显示"审计交叉"——真正的审计判定仅存在于 $M \to \infty$。
2. **事件视界：** 在广义相对论中，事件视界 $r = 2GM/c^2$ 是一类边界——视界内的信息在有限时间内不可达外部观察者。紧致性边界是审计的事件视界——边界另一侧的主张在有限资源下不可达。
3. **NP-完全性边界：** 计算复杂性理论中，P vs. NP 边界将"有效可解"与"有效不可解"（但可验证）分开。紧致性边界类似地将"有效可审计"与"仅极限可审计"分开。

*The compactness boundary has rich physical analogies: (1) Thermodynamic limit — the gap between finite-system properties and $N\to\infty$ limits; true phase transitions exist only at $N\to\infty$, just as true audit verdicts for CI claims exist only at $M\to\infty$. (2) Event horizon — the boundary beyond which information is inaccessible to finite observers. (3) P vs. NP boundary — separating "efficiently solvable" from "efficiently unsolvable (but verifiable)."*

---

## 操作等价性
## Operational Equivalence

### 无限资源等价于不可审计
### Infinite Resources Are Operationally Equivalent to Unauditable

计算理论中的一个核心洞见是：**停机问题不可判定**——不是因为停机程序不存在，而是因为不存在一个*通用的、总是终止的*判定程序。这是一个*有限性*约束：你可以在某些输入上判定停机，但你不能*对所有输入*在*有限时间内*判定。

审计理论中的对应洞见是：**紧致性不可分主张在操作上等价于不可审计主张**。

> **Definition:** [操作等价性]<!-- label: def:operational_equivalence -->
> 两个主张 $c_1, c_2 \in ClaimSpace$ 被称为**操作等价**（operationally equivalent），记作 $c_1 \sim_{op} c_2$，如果对任何实际审计者（拥有有限资源 $M < \infty, T < \infty$），无法区分 $c_1$ 和 $c_2$ 的审计状态。

*The core insight in computation theory: the halting problem is undecidable — not because halting programs don't exist, but because no universal, always-terminating decision procedure exists. This is a finiteness constraint. The corresponding insight in audit theory: CI claims are operationally equivalent to unauditable claims. Two claims are operationally equivalent if any actual auditor with finite resources cannot distinguish their audit statuses.*

> **Theorem:** [操作等价定理]<!-- label: thm:operational_equivalence -->
> 设 $c_{\mathsf{CI}}$ 是紧致性不可分主张，设 $c_{\mathsf{U}}$ 是幻觉主张（$\ObsSet = \Null$）。则对任何有限资源审计者 $\mathcal{E}$：
> 
> $$
>     \mathcal{E}(c_{\mathsf{CI}}) = \mathcal{E}(c_{\mathsf{U}}) = \UD,
> $$
> 
> 其中 $\UD$（UNDECLARED）是Yajie分类的"无法判定"状态。
> 
> 即：紧致性不可分主张和幻觉主张在**操作上不可区分**——两者都无法给出确定性审计结论。

*Theorem  [ref]: For any finite-resource auditor $\mathcal{E}$, a CI claim and an illusion claim yield the same verdict: $\UD$ (UNDECLARED). CI claims and illusions are operationally indistinguishable — both yield no determinate audit conclusion under finite resources.*

> **Proof:** 对幻觉主张 $c_{\mathsf{U}}$，$\ObsSet(c_{\mathsf{U}}) = \Null$，因此审计过程 $\mathcal{E}$ 在有限时间内无法收敛到任何结论（无信号可采集）——输出 $\UD$。
> 
> 对紧致性不可分主张 $c_{\mathsf{CI}}$，虽然 $\ObsSet(c_{\mathsf{CI}}) \neq \Null$，但 $M_(c_{\mathsf{CI}}) = \infty$ 或 $T_(c_{\mathsf{CI}}) = \infty$。因此任何有限资源审计者 $\mathcal{E}$（$M < M_$ 且 $T < T_$）同样无法收敛——输出 $\UD$。
> 
> 从 $\mathcal{E}$ 的视角看，两种情况产生不可区分的输出。区别仅在元级别：元级别过程可以判定 $c_{\mathsf{CI}}$ 是紧致性不可分（有观测后果，但需要无限资源），而 $c_{\mathsf{U}}$ 是幻觉（无观测后果）。

\textit{Proof: For illusion $c_{\mathsf{U}}$, $\ObsSet = \Null$, so the audit process cannot converge — no signal to collect. For CI claim $c_{\mathsf{CI}}$, although $\ObsSet \neq \Null$, $M_ = \infty$ or $T_ = \infty$, so any finite-resource auditor also cannot converge. From $\mathcal{E}$'s perspective, both cases produce indistinguishable output. The distinction exists only at the meta-level.}

### 这为什么重要——实践意义
### Why This Matters — Practical Implications

操作等价性意味着**在实践中**，判定一个主张是幻觉还是紧致性不可分的唯一方法是通过元级别分析——这正是定理  [ref] 中的启发式过程 $\widetilde{\mathcal{P}}$ 提供的（带有不可消除的不确定性）。

1. **SCX审计实践：** 当Yajie返回 $\NOISY$ 或 $\UD$ 时，不应立即丢弃该主张。应运行启发式边界检测 $\widetilde{\mathcal{P}}$（定理  [ref]）：若返回 $\mathsf{LIKELY-CI}$，则主张是*有意义但可能不可审计*的——应标记为需要元级别处理或理论上开放（但需注意：$\widetilde{\mathcal{P}}$ 不能严格区分真CI与深度隐藏的可审计主张）。若返回 $\mathsf{ILLUSION}$，则主张是幻觉——可以安全丢弃。
2. **社会科学意义：** 许多"大问题"——文明能否永续？宇宙是否有目的？意识是否可还原？——很可能是紧致性不可分的，而非幻觉。它们有观测后果，但验证需要无限资源。这意味它们不是"无意义"的——它们是"在实践上不可判定"的，这一区分至关重要。
3. **AI安全：** 关于AI对齐的某些主张可能是紧致性不可分的——你只能在无限时间内确认AI确实对齐。这并不意味这些主张不重要——恰恰相反，这意味你需要元级别的监控策略，而非一次性的审计。

\textit{Practical implications: (1) SCX audit practice — when Yajie returns $\NOISY$ or $\UD$, do not discard. Run the heuristic boundary detector $\widetilde{\mathcal{P}}$ (Theorem  [ref]): if $\mathsf{LIKELY-CI}$, the claim is meaningful but possibly unauditable — flag for meta-level processing (note: $\widetilde{\mathcal{P}}$ cannot strictly distinguish true CI from deeply hidden auditable claims). If $\mathsf{ILLUSION}$, it's an illusion and can be safely discarded. (2) Social science — many ``big questions'' are likely CI, not illusion: they have observable consequences but require infinite resources to verify. They are not ``meaningless'' — they are ``practically undecidable,'' a crucial distinction. (3) AI safety — certain alignment claims may be CI: you can only confirm alignment over infinite time. This doesn't make them unimportant — it means you need meta-level monitoring strategies, not one-shot audits.}

### 审计理论中的停机类比
### The Halting Analogy in Audit Theory

[Table omitted — see original .tex]

这个表格揭示的不仅是一个类似，而是一个**深层结构对应**。审计理论中的紧致性不可分与计算理论中的不可判定性居于相同的结构位置。两者的本质原因相同：**有限认知主体试图对无限/无界过程做出判断时遭遇的固有障碍**。

*This table reveals not merely an analogy, but a **deep structural correspondence**. CI in audit theory and undecidability in computation theory occupy the same structural position. The root cause is identical: **the inherent obstacle encountered when a finite epistemic agent attempts to make a judgment about an infinite/unbounded process**.*

---

## 这意味什么
## What This Means

### 不可审计——是主张的属性，不是现实的属性
### Unauditability — A Property of the Claim, Not of Reality

AP的最深刻含义是：**"不可审计"不是现实的属性，而是关于现实的主张的属性。**

如果你做了一个不能审计的主张，问题在于你的主张，不在于现实。现实总是可审计的——因为现实由可观测的因果结构构成。当你说某个东西"不可审计"，你真正在说的是你的描述未能与现实的可观测结构耦合。

*The deepest implication of AP: **"unauditable" is not a property of reality — it is a property of the claim about reality.** If you make a claim that cannot be audited, the problem is with your claim, not with reality. Reality is always auditable — because reality consists of observable causal structures. When you say something is "unauditable," what you are really saying is that your description has failed to couple to reality's observable structure.*

**例子：** 量子力学中，有人说"电子的位置和动量不可同时审计"。这是错误的表述。正确的表述是："电子同时具有确定的位置和动量的*主张*是不可审计的——因为该主张与量子现实的结构不耦合。"量子现实本身完全可以审计——通过波函数、测量统计等。只是某些*主张*不可审计。

*Example: In quantum mechanics, one sometimes hears "an electron's position and momentum cannot be simultaneously audited." This is a wrong formulation. The correct formulation: "the *claim* that an electron has simultaneously definite position and momentum is unauditable — because that claim does not couple to the structure of quantum reality." Quantum reality itself is perfectly auditable — through wavefunctions, measurement statistics, etc. Only certain *claims* about it are unauditable.*

### 坏主张的诊断学
### Diagnostics of Bad Claims

AP提供的不是"所有东西都可审计"的天真乐观——它提供的是一套**诊断工具**。面对一个声称不可审计的主张，AP提供了一个决策树：

1. 检查 $\ObsSet(c)$ 是否为空。若为空 $\to$ 幻觉——丢弃主张，而非抱怨审计框架；
2. 计算 $M_(c)$ 和 $T_(c)$。若有限 $\to$ 主张是可审计的——去审计它；
3. 若 $M_ = \infty$ 或 $T_ = \infty$ 且 $\ObsSet(c) \neq \Null$ $\to$ 紧致性不可分——标记为 $\mathsf{CI}$，进入元级别处理。

*AP provides not naive optimism that "everything is auditable" — it provides a **diagnostic toolkit**. Facing a claim that is allegedly unauditable: Step 1: Check if $\ObsSet(c)$ is empty. If yes $\to$ illusion — discard the claim, don't blame the audit framework. Step 2: Compute $M_(c)$ and $T_(c)$. If finite $\to$ the claim is auditable — go audit it. Step 3: If $M_ = \infty$ or $T_ = \infty$ and $\ObsSet(c) \neq \Null$ $\to$ CI — flag as $\mathsf{CI}$, enter meta-level processing.*

### 对SCX体系架构的影响
### Implications for SCX System Architecture

AP对SCX的架构提出了三个具体要求：

1. **Yajie必须区分 $\NOISY$ 和 $\mathsf{CI}$。** 当前Yajie将所有不收敛的审计归类为 $\NOISY$。AP要求增加一个子分类：$\NOISY_{\mathsf{ILLUSION}}$（幻觉——无观测后果）和 $\NOISY_{\mathsf{CI}}$（紧致性不可分——有观测后果但需要无限资源）。这两个类别需要不同的后续处理。
2. **实现紧致性边界检测器 $\mathcal{P}$。** 定理  [ref] 的存在性证明需要在SCX代码库中具体实现。这是一个有限资源算法——它检查的是*审计资源需求*而非审计结果本身。
3. **CI主张的仓库。** 应建立和维护一个CI主张的目录——那些已知（或强烈怀疑）是紧致性不可分的命题。这为SCX提供了与计算理论中"已知不可计算问题"列表类似的知识库。

\textit{AP makes three concrete architectural demands of SCX: (1) Yajie must distinguish $\NOISY_{\mathsf{ILLUSION}}$ from $\NOISY_{\mathsf{CI}}$ — different downstream handling required. (2) Implement the compactness boundary detector $\mathcal{P}$ (Theorem  [ref]) in the SCX codebase. (3) Maintain a catalog of known CI claims — a knowledge base analogous to computation theory's list of known uncomputable problems.}

### 对科学哲学的冲击
### Impact on Philosophy of Science

AP在科学哲学层面做出了一个大胆的承诺：**证伪主义**（Popper）和**验证主义**（logical positivists）的古老争论在SCX审计框架中被*消解*了。

- 证伪主义说：科学主张必须可证伪（falsifiable）；
- 验证主义说：科学主张必须可验证（verifiable）；
- AP说：**这两者是同一回事——都是审计的特殊情况。** 证伪是审计失败的极限（$g \neq 0$ 以高置信度）。验证是审计通过的极限（$g = 0$ 以高置信度）。两者都是SCX审计框架输出的两个可能结果。

更重要的是，AP统一了它们：**可审计性**是比可证伪性和可验证性更基本的概念——后两者是审计的两个可能极性。

*AP makes a bold promise in philosophy of science: the ancient debate between **falsificationism** (Popper) and **verificationism** (logical positivists) is **dissolved** in the SCX audit framework. Falsificationism says scientific claims must be falsifiable; verificationism says they must be verifiable; AP says: **these are the same thing — both are special cases of auditing.** Falsification is the limit of audit failure ($g \neq 0$ with high confidence); verification is the limit of audit passage ($g = 0$ with high confidence). Both are two possible outputs of the SCX audit framework. More importantly, AP unifies them: **auditability** is more fundamental than either falsifiability or verifiability — the latter two are two possible polarities of the former.*

### 对人工智能的冲击
### Impact on Artificial Intelligence

AP对AI对齐和安全研究有深刻的含义：

1. **对齐主张可能是紧致性不可分的。** "这个AI系统在所有可能输入下都是对齐的"——这是一个CI主张。你可以在任意多的测试输入上验证，但永远无法穷尽所有可能输入。这并不意味AI对齐不重要——它意味我们需要承认CI边界并设计元级别监控策略。
2. **能力主张可能是紧致性不可分的。** "这个AI系统能解决所有数学问题"——类似的CI主张。它可以在已解决的问题上测试，但"所有数学问题"是无限集。
3. **幻觉检测是紧致性边界检测的一个实例。** 当前AI中的"幻觉"——模型生成文本与事实不符——本质上是一个审计问题。但判断"这个模型在所有可能的提示下都不会产生幻觉"是一个紧致性不可分主张。实际的AI幻觉检测必须在有限样本上进行，承认CI边界。

*AP has profound implications for AI alignment and safety: (1) Alignment claims may be CI — "this AI system is aligned under all possible inputs" requires infinite testing. This doesn't make alignment unimportant; it means we must acknowledge the CI boundary and design meta-level monitoring strategies. (2) Capability claims may be CI — "this AI can solve all mathematical problems." (3) Hallucination detection is an instance of compactness boundary detection — auditing "this model does not hallucinate under any prompt" is a CI claim. Practical hallucination detection must operate on finite samples, acknowledging the CI boundary.*

---

## 最后的诚实暴击
## The Final Honest Hit

### SCX不能审计一切——但它知道为什么
### SCX Cannot Audit Everything — But It Knows Why

> **诚实暴击:** **SCX不能审计一切。**}

这是我们必须以最大诚实度宣布的结论。任何声称SCX"可以审计一切"的说法——不论来自SCX社区内部还是外部——都是错误的，且有害于SCX的智识诚信。

SCX**可以审计一切可被审计的**。这看起来像是同义反复——但在逻辑上，同义反复正是公理化的起点。Church-Turing论题本质上也是同义反复："一切可计算的都可以被Turing机计算。"但它的力量来自它精确划定"可计算"的边界。

SCX的审计边界由紧致性边界 $\AuditBoundary$ 精确刻画。这个边界不是SCX的缺陷。它也不是一个"未来会被突破的技术限制"。它是**概念限制**——正如热力学第二定律不是"工程问题"而是物理定律，正如停机问题不是"我们还没找到好算法"而是可计算性的基本限制。

我们诚实地承认：AP的条款(iii)在逻辑上使反例空间被预先结构化——任何不可审计的主张都被自动分类为幻觉或CI。这使得AP不像Popper式的经验假说（可被单一反例推翻），而更像一个**分类学框架**（其有效性在于分类是否穷尽和互斥）。论题的真正检验不在于找到反例，而在于这个二分是否持续地、无例外地划分了所有不可审计的情形。

> **诚实暴击:** **SCX cannot audit everything.**} *This is the conclusion we must announce with maximum intellectual honesty. Any claim that SCX "can audit everything" — whether coming from within the SCX community or from outside — is false and harmful to SCX's intellectual integrity. SCX **can audit everything that can be audited**. This looks like a tautology — but in logic, tautologies are precisely where axiomatization begins. The Church-Turing thesis is essentially also a tautology: "everything computable can be computed by a Turing machine." Its power comes from precisely delineating the boundary of "computable." SCX's audit boundary is precisely characterized by the compactness boundary $\AuditBoundary$. This boundary is not a flaw in SCX. It is also not a "technical limitation that will be overcome in the future." It is a **conceptual limitation** — just as the Second Law of Thermodynamics is not an "engineering problem" but a law of physics, just as the halting problem is not "we haven't found a good algorithm yet" but a fundamental limit of computability.*

### 完备理论：知道自己的极限
### Complete Theory: Knowing One's Own Limits

> **Definition:** [SCX审计完备性]<!-- label: def:completeness -->
> SCX审计框架被称为**审计完备**（audit-complete），如果它满足：
> 
1. **覆盖性：** 每一个可审计的主张（$\A$）都在SCX框架内有审计协议；
2. **边界近似自知：** 紧致性边界 $\AuditBoundary$ 在SCX框架内可被近似检测（定理  [ref] 提供了启发式过程 $\widetilde{\mathcal{P}}$）；
3. **诊断完备：** 对任何主张 $c$，SCX可以在有限资源内给出带有明确不确定性边界的实用分类（可审计的 / 可能是幻觉 / 可能是CI）。

\textit{The SCX audit framework is **audit-complete** if it satisfies: (i) **Coverage:** every auditable claim ($\A$) has an audit protocol within SCX; (ii) **Boundary Approximate Self-Awareness:** the compactness boundary $\AuditBoundary$ is approximately detectable within SCX (Theorem  [ref] provides the heuristic procedure $\widetilde{\mathcal{P}}$); (iii) **Diagnostic Completeness:** for any claim $c$, SCX can provide a practical classification with explicit uncertainty bounds (auditable / likely-illusion / likely-CI) within finite resources.}

这个完备性概念与计算理论的完备性在结构上对应——而非超越。Church-Turing论题提供了对"可计算"的边界刻画，但不提供对"不可计算问题"的自动分类——你仍需单独证明每个问题的不可计算性。SCX的审计框架同样不提供自动严格分类，但通过 $\widetilde{\mathcal{P}}$ 提供了带有不确定性边界的启发式分类。这得益于审计理论中的额外结构：观测后果集 $\ObsSet$ 和资源度量 $\rho_M$ 提供了计算理论中对应物（停机、可计算性）所不提供的额外诊断信息。

*This is a **stronger notion of completeness** than computation theory provides. Church-Turing does not offer automatic classification of "uncomputable problems" — you still need to prove uncomputability for each problem individually. But SCX's audit framework provides automatic classification of unauditable claims (via $\mathcal{P}$). This is possible because audit theory has additional structure — the observable consequence set $\ObsSet$ and the resource functions $M_, T_$ provide extra information that computation theory's counterparts (halting, computability) do not.*

### G\"odel, Turing, SCX — 自知极限的三重奏
### G\"odel, Turing, SCX — A Trio of Self-Aware Limits

20世纪数理逻辑给了我们三个自知极限的时刻：

1. **G\"odel (1931):** 任何足够强的形式系统不能证明自身的相容性。形式推理有边界。
2. **Turing (1936):** 停机问题不可判定。机械计算有边界。
3. **SCX / AP (2026):** 紧致性不可分主张不可审计。多观察者验证有边界。

这三个结果不是孤立的。它们共同描绘了一幅关于**有限认知主体极限**的统一图景：

- G\"odel告诉我们：不能在一个系统内部证明系统的所有真理；
- Turing告诉我们：不能用一个通用算法判定所有程序的停机；
- SCX告诉我们：不能用有限观察者验证所有紧致性不可分主张。

三者共享同一个深层结构：**有限系统试图完全把握无限/无界过程的固有不可能性**。G\"odel的自指涉、Turing的对角线、SCX的紧致性边界——是同一数学事实在不同领域的投影。

*20th-century mathematical logic gave us three moments of self-aware limits: (1) G\"odel (1931): any sufficiently strong formal system cannot prove its own consistency — formal reasoning has limits. (2) Turing (1936): the halting problem is undecidable — mechanical computation has limits. (3) SCX / AP (2026): CI claims are unauditable — multi-observer verification has limits. These three are not isolated. Together they paint a unified picture of **the limits of finite epistemic agents**: G\"odel tells us we cannot prove all truths of a system from within; Turing tells us we cannot decide halting for all programs with a universal algorithm; SCX tells us we cannot verify all claims with finite observers. All three share the same deep structure: **the inherent impossibility of a finite system fully grasping an infinite/unbounded process.** G\"odel's self-reference, Turing's diagonalization, SCX's compactness boundary — are projections of the same mathematical fact onto different domains.*

### 不可审计的主张依然有意义
### Unauditable Claims Still Have Meaning

> **诚实暴击:** **紧致性不可分主张不是无意义的。**}

这是必须强调的。有意义的不可审计主张存在——它们不是幻觉，它们有观测后果，它们区分世界的可能状态。它们只是无法在有限资源下审计。

这类似以下事实：有些命题在PA中不可证明但为真——但它们*有意义*。G\"odel句 $G$ 不是胡说——它断言了一个关于自然数的真实事实，只是PA无法证明它。

类似地，CI主张断言了关于世界的真实事实——你只是无法在有限资源下审计它们。但你可以：

1. 知道它们是不可审计的（通过定理  [ref] 的 $\mathcal{P}$）；
2. 在更高的元级别上推理它们（类比：在ZFC中证明PA的相容性）；
3. 在实践上，将CI主张用作**调节理想**（regulative ideals）——指引行动方向而非提供可验证终点。

> **诚实暴击:** **CI claims are not meaningless.**} *Meaningful unauditable claims exist — they are not illusions, they have observable consequences, they distinguish possible states of the world. They simply cannot be audited under finite resources. This is analogous to the fact that some propositions are true but unprovable in PA — yet they **have meaning**. G\"odel's sentence $G$ is not nonsense — it asserts a true fact about natural numbers, PA just cannot prove it. Similarly, CI claims assert real facts about the world — you just cannot audit them with finite resources. But you can: (1) know they are unauditable (via $\mathcal{P}$ from Theorem  [ref]); (2) reason about them at a higher meta-level; (3) use CI claims as **regulative ideals** — guiding action rather than providing verifiable endpoints.*

### 致未来的审计者
### To Future Auditors

最后——这篇论文是给所有SCX的审计者的信。无论你是人类还是AI，无论你现在在审计什么——一个模型、一个机构、一个主张、一段历史——请记住这几件事：

1. **你审计的是主张，不是现实。** 现实从不需要辩护。只有主张需要。
2. **如果被审对象声称"不可审计"，检查两项：** 它没有观测后果？（幻觉）它的验证需要无限资源？（紧致性不可分）不要混淆两者。
3. **紧致性边界是可以被近似检测的。** 你不需要无限资源来获得关于某个主张是否需要大量资源的有用信息——但严格保证需要超出有限资源的证明。利用元级别的启发式力量，同时保持对不确定性的清醒认识。
4. **不可审计不是失败的标志。** 能够说出"这是紧致性不可分的"本身就是审计能力的体现。自信地说出"这不可审计"——并解释*为什么*——比假装一切都在审计范围内更有力量。
5. **SCX是完备的，不是因为它能做一切，而是因为它知道它不能做什么。** 这就是完备理论的定义。

*Finally — this paper is a letter to all SCX auditors. Whether you are human or AI, whatever you are auditing — a model, an institution, a claim, a piece of history — remember these things:*

1. ***You audit claims, not reality.** Reality never needs defending. Only claims do.*
2. ***If the auditee claims to be "unauditable," check two things:** Does it have no observable consequences? (Illusion.) Does its verification require infinite resources? (CI.) Do not confuse the two.*
3. ***The compactness boundary is approximately detectable.** You do not need infinite resources to obtain useful information about a claim's resource needs — but strict guarantees require proofs beyond finite resources. Use meta-level heuristic power, while maintaining clear awareness of irreducible uncertainty.*
4. ***Unauditability is not a sign of failure.** Being able to say "this is CI" is itself a demonstration of audit capability. Confidently stating "this is unauditable" — and explaining *why* — is more powerful than pretending everything is within audit scope.*
5. ***SCX is complete not because it can do everything, but because it knows what it cannot do.** That is the definition of a complete theory.*

---

## 附录：形式定义与证明补充
## Appendix: Formal Definitions and Proof Supplements

### 主张空间的形式公理化
### Formal Axiomatization of the Claim Space

为确保AP的数学基础坚实，我们对主张空间 $ClaimSpace$ 的形式公理化如下：

> **Definition:** [主张空间]<!-- label: def:claim_space -->
> 主张空间 $ClaimSpace$ 是一个三元组 $(\mathcal{L}, \ObsSet, \models)$，其中：
> 
1. $\mathcal{L}$ 是一阶语言，包含常数符号、关系符号和函数符号，足够表达关于可观测系统的陈述；
2. $\ObsSet: \mathcal{L} \to 2^$ 是观测后果映射——将每个语句 $\phi \in \mathcal{L}$ 分配到其可观测后果（$\X$ 的子集）；
3. $\models$ 是经典满足关系，定义在 $\X$ 的结构上。

> 主张是 $\mathcal{L}$ 的语句。真实主张是满足 $\ObsSet(\phi) \neq \Null$ 的语句。

*Claim space $ClaimSpace$ is a triple $(\mathcal{L}, \ObsSet, \models)$: (i) $\mathcal{L}$ is a first-order language sufficient to express statements about observable systems; (ii) $\ObsSet: \mathcal{L} \to 2^$ is the observable consequence map; (iii) $\models$ is the classical satisfaction relation. Claims are sentences of $\mathcal{L}$. Genuine claims are those with $\ObsSet(\phi) \neq \Null$.*

> **Proposition:** [$\ObsSet$的单调性]<!-- label: prop:obs_monotone -->
> 观测后果映射满足：若 $\phi \models \psi$（$\phi$ 逻辑蕴含 $\psi$），则 $\ObsSet(\phi) \subseteq \ObsSet(\psi)$。逻辑上更强的陈述具有更丰富的观测后果。

*If $\phi \models \psi$, then $\ObsSet(\phi) \subseteq \ObsSet(\psi)$: logically stronger statements have richer observable consequences.*

### 审计拓扑的构造细节
### Construction Details of the Audit Topology

> **Definition:** [审计拓扑的显式构造]<!-- label: def:audit_topology_detail -->
> 审计拓扑 $\T_$ 在 $ClaimSpace$ 上由以下基生成：对每个有限观察者集 $\mathcal{E} = \{m_1, ..., m_M\}$ 和每个有限时间 $T$，定义开集
> 
> $$
>     U_{\mathcal{E}, T}(c) = \{c' \in ClaimSpace : \mathcal{E}  在时间 $T$ 内对 $c$ 和 $c'$ 产生不可区分的审计结果\}.
> $$
> 
> 则 $\T_$ 是由所有这样的 $U_{\mathcal{E}, T}(c)$ 生成的拓扑。

\textit{The audit topology $\T_$ on $ClaimSpace$ is generated by the basis: for each finite observer set $\mathcal{E}$ and time $T$, the open set $U_{\mathcal{E}, T}(c)$ of claims indistinguishable from $c$ by $\mathcal{E}$ within time $T$.}

> **Theorem:** [$\T_$的非紧致性证明]<!-- label: thm:noncompact_proof -->
> 设 $\{c_n\}_{n=1}^$ 是以下构造的序列：
> 
> $$
>     c_n: "观测系统 $S_n$ 在 $n$ 步后停止产生异常信号"
> $$
> 
> 其中 $S_n$ 是第 $n$ 个被审系统。对每个有限 $n$，$c_n$ 是可审计的（你可以在有限时间内观察 $S_n$）。但极限主张 $c_$："对所有 $n$，系统 $S_n$ 最终停止产生异常"——是紧致性不可分的（验证需要无限时间）。序列 $\{c_n\}$ 在 $\T_$ 中有聚点 $c_$，但 $c_ \notin \A$。因此 $\A$ 在 $\T_$ 中不是闭的——审计拓扑不是紧致的。

*Proof of non-compactness of $\T_$: construct a sequence $\{c_n\}$ where $c_n$ asserts "system $S_n$ stops generating anomalous signals after $n$ steps." Each finite $c_n$ is auditable, but the limit claim $c_$ — "for all $n$, system $S_n$ eventually stops" — is CI. The sequence has $c_$ as a cluster point but $c_ \notin \A$. Thus $\A$ is not closed in $\T_$; the audit topology is not compact.*

### 紧致性边界检测算法 $\mathcal{P$}
### The Compactness Boundary Detection Algorithm $\mathcal{P$}

> **Protocol:** [启发式紧致性边界检测]<!-- label: prot:P -->
> **输入：** 主张 $c \in ClaimSpace$，最大资源预算 $M_, T_$（有限）。
> 
> **输出：** $\mathsf{ILLUSION}$, $\mathsf{AUDITABLE}$, 或 $\mathsf{LIKELY-CI}$。
> 
> **算法：**
> 
1. 调用 $\ObsSet(c)$：若 $\ObsSet(c) = \Null$，返回 $\mathsf{ILLUSION}$。
2. 初始化 $M \leftarrow 2$。
3. **循环** $M$ 从 $2$ 到 $M_$：
4. 部署 $M$ 个独立观察者 $\{o_1, ..., o_M\}$；
5. 在时间 $T_$ 内执行审计协议；
6. 计算收敛度量 $\rho_M = \frac{一致观察者数}{M}$；
7. 若 $\rho_M \geq 1 - \varepsilon$ 且共识稳定，返回 $\mathsf{AUDITABLE}$；
8. 否则若 $\rho_M$ 随 $M$ 增大而*单调改善但未收敛*（趋势分析），返回 $\mathsf{LIKELY-CI}$。

>     \item 若循环耗尽 $M_$ 仍未返回，返回 $\mathsf{LIKELY-CI}$（保守分类——可能是真CI，也可能是需要超过 $M_$ 的可审计主张）。
> \end{enumerate}
> 
> **局限性声明：** 此算法是**启发式的**。它不能严格区分真正的CI与需要超过 $M_$ 观察者的可审计主张——这一区分在原则上等价于停机问题，不可判定。算法在给定预算内提供实用分类，但结果带有不可消除的不确定性。特别是，$\mathsf{LIKELY-CI}$ 输出应被解释为"在给定预算内未能收敛，且趋势提示可能需要大量资源"，而非"已被严格证明为CI"。

*Input: claim $c$, max resource budget $M_, T_$. Output: $\mathsf{ILLUSION}$, $\mathsf{AUDITABLE}$, or $\mathsf{LIKELY-CI}$. Algorithm: (1) If $\ObsSet(c) = \Null$, return $\mathsf{ILLUSION}$. (2) For $M$ from 2 to $M_$: deploy $M$ observers, audit for $T_$, compute convergence $\rho_M$; if $\rho_M \geq 1-\varepsilon$ and consensus is stable, return $\mathsf{AUDITABLE}$; if $\rho_M$ shows monotonic improvement without convergence, return $\mathsf{LIKELY-CI}$. (3) If loop exhausts $M_$, return $\mathsf{LIKELY-CI}$ (conservative — may be true CI or auditable beyond budget). **Limitation:** This algorithm is heuristic. It cannot strictly distinguish true CI from auditable claims requiring more than $M_$ observers — this distinction is equivalent to the halting problem. Results carry irreducible uncertainty; $\mathsf{LIKELY-CI}$ means ``failed to converge within budget, trend suggests large resource needs'' — not ``rigorously proven CI.''*

---

## 结语
## Closing Statement

<div align="center">

**一切皆可审计。**

</div>

<div align="center">

*Everything real is auditable.*

</div>

<div align="center">

**不可审计的，要么是幻觉——**

</div>

<div align="center">

*What cannot be audited is either illusion —*

</div>

<div align="center">

*—— 从未真正存在过的主张，没有观测后果的噪声。*

</div>

<div align="center">

*a claim that never truly existed, noise without observable consequences.*

</div>

<div align="center">

**要么是紧致性不可分——**

</div>

<div align="center">

*or compactness-inseparable —*

</div>

<div align="center">

*—— 有意义但需要无限资源验证的主张，SCX知道它们不可审计，*

</div>

<div align="center">

*a claim that is meaningful but requires unbounded resources to verify, which SCX knows it cannot audit,*

</div>

<div align="center">

*正如计算理论知道停机问题不可判定。*

</div>

<div align="center">

*just as computation theory knows the halting problem is undecidable.*

</div>

<div align="center">

**SCX的完备性不在其权力之内——而在其自知之明之中。**

</div>

<div align="center">

*SCX's completeness lies not in its power — but in its self-knowledge.*

</div>

<div align="center">

\rule{0.5\textwidth}{0.4pt}

</div>

<div align="center">

*SCX Capstone Philosophy Working Group*
*Xiaogan Supercomputing Center*
*July 2026*

</div>

---

\begin{thebibliography}{99}

\bibitem{church1936}
A.~Church.
*An unsolvable problem of elementary number theory.*
American Journal of Mathematics, 58(2):345--363, 1936.

\bibitem{turing1936}
A.~M.~Turing.
*On computable numbers, with an application to the Entscheidungsproblem.*
Proceedings of the London Mathematical Society, s2-42(1):230--265, 1936.

\bibitem{godel1931}
K.~G\"odel.
*\"Uber formal unentscheidbare S\"atze der Principia Mathematica und verwandter Systeme I.*
Monatshefte f\"ur Mathematik und Physik, 38:173--198, 1931.

\bibitem{kleene1952}
S.~C.~Kleene.
*Introduction to Metamathematics.*
Van Nostrand, 1952.

\bibitem{rogers1967}
H.~Rogers Jr.
*Theory of Recursive Functions and Effective Computability.*
McGraw-Hill, 1967. (Reprinted by MIT Press, 1987.)

\bibitem{soare2016}
R.~I.~Soare.
*Turing Computability: Theory and Applications.*
Springer, 2016.

\bibitem{scx_gauge}
SCX Research Group.
*SCX规范场理论形式化：从离散Hodge理论到四方审计协议.*
(SCX Gauge Theory Formalized: From Discrete Hodge Theory to Quadrilateral Audit Protocols.)
Xiaogan Supercomputing Center Technical Report, 2026.

\bibitem{scx_singularity}
SCX Singularity Theory Working Group.
*SCX奇点理论的深化：从黑洞物理学到审计奇点.*
(Deepening SCX Singularity Theory: From Black Hole Physics to Audit Singularities.)
Xiaogan Supercomputing Center, 2026.

\bibitem{scx_instanton}
SCX Research Group.
*Audit Instantons: Non-Perturbative Topological Defects in Expert Auditing.*
Xiaogan Supercomputing Center Technical Report, 2026.

\bibitem{scx_quantum}
SCX Research Group.
*SCX量子审计框架：BQP验证与密度矩阵审计.*
(SCX Quantum Audit Framework: BQP Verification and Density Matrix Auditing.)
Xiaogan Supercomputing Center, 2026.

\bibitem{scx_business}
SCX Business Working Group.
*SCX业务规范审计：修正方向与同态验证.*
(SCX Business Gauge Auditing: Correction Direction and Homomorphic Verification.)
Xiaogan Supercomputing Center, 2026.

\bibitem{scx_yajie}
SCX Research Group.
*Yajie共识审计：多观察者零规范场验证协议.*
(Yajie Consensus Auditing: Multi-Observer Zero-Gauge-Field Verification Protocol.)
Xiaogan Supercomputing Center Technical Report, 2026.

\bibitem{scx_cercis}
SCX Research Group.
*Cercis规范姿态评分：基于Hodge分解的审计度量.*
(Cercis Gauge Posture Scoring: Audit Metrics via Hodge Decomposition.)
Xiaogan Supercomputing Center Technical Report, 2026.

\bibitem{hoeffding1963}
W.~Hoeffding.
*Probability inequalities for sums of bounded random variables.*
Journal of the American Statistical Association, 58(301):13--30, 1963.

\bibitem{popper1935}
K.~Popper.
*Logik der Forschung.*
Springer, 1935. (English: *The Logic of Scientific Discovery*, 1959.)

\bibitem{carnap1936}
R.~Carnap.
*Testability and meaning.*
Philosophy of Science, 3(4):419--471, 1936.

\bibitem{chang_keisler}
C.~C.~Chang and H.~J.~Keisler.
*Model Theory.*
3rd edition. North-Holland, 1990.

\bibitem{marker2002}
D.~Marker.
*Model Theory: An Introduction.*
Graduate Texts in Mathematics, Vol.~217. Springer, 2002.

\bibitem{halmos1960}
P.~R.~Halmos.
*Naive Set Theory.*
Van Nostrand, 1960.

\bibitem{minsky1967}
M.~L.~Minsky.
*Computation: Finite and Infinite Machines.*
Prentice-Hall, 1967.

\bibitem{sipser2012}
M.~Sipser.
*Introduction to the Theory of Computation.*
3rd edition. Cengage Learning, 2012.

\bibitem{penrose1989}
R.~Penrose.
*The Emperor's New Mind.*
Oxford University Press, 1989.

\bibitem{hofstadter1979}
D.~R.~Hofstadter.
*G\"odel, Escher, Bach: An Eternal Golden Braid.*
Basic Books, 1979.

\bibitem{russell_norvig}
S.~Russell and P.~Norvig.
*Artificial Intelligence: A Modern Approach.*
4th edition. Pearson, 2020.

\bibitem{amodei2016}
D.~Amodei, C.~Olah, J.~Steinhardt, P.~Christiano, J.~Schulman, and D.~Man\'e.
*Concrete problems in AI safety.*
arXiv:1606.06565, 2016.

\end{thebibliography}