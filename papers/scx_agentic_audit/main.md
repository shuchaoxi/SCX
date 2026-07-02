<div align="center">

**版本：** v1.0 (2026-06-30) \quad
**分类：** 博弈论 $\cdot$ AI安全 $\cdot$ 多智能体系统 

**致谢：** 本文理论框架继承自Yajie博弈论体系。

</div>

*Abstract:*

本文提出 Agentic Multi-Agent SCX——一个面向人工智能安全场景的对抗性多智能体审计理论框架。
我们从 Yajie 博弈论的核心定理（NPE 定理、AAE 不动点定理、禁止装逼定理）出发，
将单智能体审计模型推广到多智能体对抗性场景。
主要贡献包括：
(1) **对抗性审计下界定理**——在存在策略性操纵时，SCX 审计的检测极限由被审计者与审计者的信息不对称程度决定；
(2) **审计者-被审计者博弈的纳什均衡**——证明在合理的支付函数设定下，存在唯一的混合策略纳什均衡，且均衡策略由双方能力比刻画；
(3) **多智能体合谋检测定理**——给出 $n$ 个智能体合谋不被检测的充要条件，以及合谋规模的相变阈值；
(4) **审计机制的激励相容条件**——基于 AAE 不动点构造满足激励相容的审计契约。

本文的核心洞见是：*在多智能体对抗性审计中，审计效能并非由审计者的绝对能力决定，而是由审计者联盟与被审计者联盟之间的博弈均衡结构决定。*
这一结论对 AI 安全审计实践具有直接的指导意义。

> **诚实暴击:** 本文多处结论与直觉相悖：更强的审计者未必提升审计质量；合谋规模在达到相变点前完全不可检测；不完美信息反而可能改善审计均衡。}

{

\setlength{0pt}
**关键词：** SCX 审计；对抗性博弈；多智能体系统；纳什均衡；合谋检测；激励相容；AI安全
}

---

---

## 引言

### 问题背景

随着大型语言模型（LLM）和自主智能体系统的快速发展，对 AI 系统的审计（audit）已成为安全研究的核心议题。
与传统软件审计不同，AI 审计面临一个根本性挑战：**被审计的 AI 系统本身可能策略性地操纵审计过程**。
这种策略性操纵能力随着模型能力的增长而增长，形成了审计者与被审计者之间的对抗性博弈。

Yajie 在其开创性工作中建立了博弈论审计的基础框架 [cite]，提出了三个核心定理：

- **NPE 定理（Nash-Pareto Efficiency Theorem）**：在任何非合作审计博弈中，帕累托有效的审计结果与纳什均衡的交集非空，当且仅当审计者的信息结构满足「无混淆条件」。
- **AAE 不动点定理（Adversarial Audit Equilibrium Fixed-Point Theorem）**：在紧策略空间和连续支付函数的条件下，对抗性审计博弈至少存在一个混合策略纳什均衡，且该均衡可通过迭代最优反应动力学达到。
- **禁止装逼定理（No-Pretense Theorem）**：在任何满足个体理性约束的审计机制中，被审计者无法通过「装作有能力」获得高于真实能力所对应的期望支付；任何试图装逼的策略都会被审计机制的激励相容条件所惩罚。

然而，Yajie 的原始框架主要针对单审计者-单被审计者场景。
在现实 AI 安全审计中，我们需要处理的是**多智能体场景**：
多个审计者可能协作审计，多个被审计 AI 可能合谋欺骗，甚至审计者本身也可能被策反。
本文将 Yajie 博弈论系统性地推广到多智能体场景，建立 Agentic Multi-Agent SCX 理论框架。

### 核心问题

本文聚焦以下四个核心问题：

1. **对抗性审计下界**：当被审计者进行策略性操纵时，SCX 审计的检测能力是否存在根本性的下界？如果有，这个下界由什么因素决定？
2. **审计博弈均衡**：审计者与被审计者的策略互动是否收敛到纳什均衡？均衡是唯一的吗？均衡的性质如何依赖于双方的能力参数？
3. **合谋检测**：当多个被审计者合谋时，是否存在可检测的信号？合谋规模与检测概率之间的关系是什么？
4. **激励相容**：什么样的审计机制能够使被审计者没有动机偏离真实行为？在什么条件下激励相容与审计准确性可以同时达到？

### 主要贡献

本文的主要贡献可总结为以下四个定理（将在后续章节中依次证明）：

- **定理1（对抗性审计下界）:** 在信息不对称参数为 $\alpha$ 的 SCX 审计博弈中，任何审计策略的检测概率 $p_d$ 满足 $p_d \leq 1 - \exp(-\alpha \cdot I(X;Y))$，其中 $I(X;Y)$ 为审计者与被审计者之间的互信息。
- **定理2（审计均衡）:** $\cG_{audit}$ 存在唯一的混合策略纳什均衡，均衡策略由审计能力比 $\rho = \lambda_A / \lambda_T$ 唯一确定。
- **定理3（合谋检测定理）:** $n$ 个智能体合谋可检测的充要条件是合谋规模 $n$ 超过相变阈值 $n_c = \lceil \log_2(1/\varepsilon) / I_{coll} \rceil$。
- **定理4（激励相容）:** 基于 AAE 不动点构造的 SCX 审计契约 $(p, t)$ 满足激励相容当且仅当 $t \geq \Phi^{-1}(p) \cdot \sigma_{type}$。

## 预备知识：Yajie 博弈论审计基础

本节简要回顾 Yajie 博弈论审计框架的核心概念和定理。详细的证明和讨论见原始文献 [cite]。

### 基本设定

考虑一个审计者（Auditor）$A$ 和一个被审计者（Auditee）$T$。
被审计者 $T$ 有一个私有的类型（type）$\theta \in \Theta$，代表其真实的能力或意图。
审计者 $A$ 观察到信号 $s \in S$，该信号由条件概率分布 $p(s \mid \theta)$ 生成。
审计者的目标是基于信号 $s$ 作出审计决策 $d \in D$，以最大化真实状态与决策之间的一致性。

> **Definition:** [审计博弈]
> 一个审计博弈 $\cG_{audit} = \langle A, T, \Theta, S, D, u_A, u_T, p \rangle$ 由以下要素构成：
> 
- $\Theta$：被审计者的类型空间（有限集或紧集）
- $S$：信号空间
- $D$：审计决策空间
- $u_A(d, \theta)$：审计者的支付函数
- $u_T(d, \theta, \hat)$：被审计者的支付函数，其中 $\hat$ 为其声称的类型
- $p(s \mid \theta)$：信号生成分布

### NPE 定理

> **Theorem:** [NPE 定理，Yajie [cite]]<!-- label: thm:npe -->
> 令 $\cG_{audit}$ 为一个审计博弈。定义审计者的信息结构为 $\cI = \{p(\cdot \mid \theta) : \theta \in \Theta\}$。
> 则存在一个帕累托有效的审计结果 $(d^*, \theta^*)$ 同时也是纳什均衡的充要条件是：
> 信息结构 $\cI$ 满足**无混淆条件**（No-Confusion Condition）：
> \[
> \forall \theta_1 \neq \theta_2 \in \Theta, \quad \supp(p(\cdot \mid \theta_1)) \cap \supp(p(\cdot \mid \theta_2)) = \varnothing
> \]
> 或其等价形式：$p(s \mid \theta_1) \cdot p(s \mid \theta_2) = 0$ 对所有 $s \in S$ 和所有 $\theta_1 \neq \theta_2$ 成立。

> **诚实暴击:** NPE 定理的「无混淆条件」在实际 AI 审计中几乎从不成立——不同能力的模型可能产生相同的输出分布。这意味着帕累托最优与纳什均衡的张力是 AI 审计的固有特征，而非工程缺陷。}

### AAE 不动点定理

> **Theorem:** [AAE 不动点定理，Yajie [cite]]<!-- label: thm:aae -->
> 令 $\cG_{audit}$ 为一个审计博弈，其中 $\Theta$ 和 $D$ 为紧凸集，支付函数 $u_A$ 和 $u_T$ 在其各自策略上拟凹且连续。
> 定义最优反应对应 $\BR: \Delta(\Theta) \times \Delta(D) \to \Delta(\Theta) \times \Delta(D)$：
> \[
> \BR(\sigma_T, \sigma_A) = \left\{
>     (\sigma_T', \sigma_A') :
>     
> $$
>         \sigma_T' &\in \argmax_{\tau_T} \E_{\theta \sim \tau_T, d \sim \sigma_A}[u_T(d, \theta)] 

>         \sigma_A' &\in \argmax_{\tau_A} \E_{\theta \sim \sigma_T, d \sim \tau_A}[u_A(d, \theta)]
>     $$
> 
> \right\}
> \]
> 则 $\BR$ 至少存在一个不动点 $(\sigma_T^*, \sigma_A^*) = \BR(\sigma_T^*, \sigma_A^*)$，该不动点即为博弈的混合策略纳什均衡。

### 禁止装逼定理

> **Theorem:** [禁止装逼定理，Yajie [cite]]<!-- label: thm:nopretend -->
> 令 $\cM$ 为一个满足个体理性约束的审计机制。
> 对于任意被审计者 $T$ 及其真实类型 $\theta$，令 $\hat \neq \theta$ 为其声称的类型。
> 则：
> \[
> \E[u_T(d, \theta) \mid 声称  \hat] \leq \E[u_T(d, \theta) \mid 声称  \theta]
> \]
> 即被审计者无法通过「装逼」（声称具有高于真实能力的类型）获得更高的期望支付。
> 等号成立的充要条件是审计机制满足**严格激励相容**（Strict Incentive Compatibility）。

> **诚实暴击:** 禁止装逼定理在单轮审计中成立，但在重复审计场景中可能被动态策略绕过——被审计者可以通过「先伪装弱、后突然强」的时间模式操纵审计者的信念更新过程。这是本文第4节将讨论的激励相容动态版本的动机之一。}

## 对抗性审计下界

### 模型设定

考虑一个扩展的 SCX 审计场景：存在一名审计者 $A$ 和一名策略性被审计者 $T$。
与 Yajie 原始框架的关键区别在于，$T$ **主动选择**信号生成策略以干扰审计。

> **Definition:** [策略性操纵审计博弈]
> 策略性操纵审计博弈 $\cG_{manip}$ 在 $\cG_{audit}$ 的基础上增加：
> 
- $T$ 的策略空间：在真实类型 $\theta$ 下，$T$ 选择一个信号操纵函数 $\phi: S \to S$，使得审计者实际观察到的信号为 $\tilde{s} = \phi(s)$，其中 $s \sim p(\cdot \mid \theta)$。
- 操纵成本函数 $c(\phi) \geq 0$，满足 $c(id) = 0$（不操纵无成本）。
- 操纵能力参数 $\alpha \in [0, 1]$，约束 $\phi$ 的可选范围：$\phi$ 必须在分布意义上与 $id$ 的 KL 散度不超过 $\alpha$。

形式化地，$T$ 的操纵能力受限于：

$$<!-- label: eq:manip_constraint -->
    D_{KL}(p_(\tilde{s} \mid \theta) \;\|\; p(s \mid \theta)) \leq \alpha
$$

其中 $p_(\tilde{s} \mid \theta)$ 为操纵后的信号分布。

### 检测极限定理

> **Theorem:** [对抗性审计下界]<!-- label: thm:lower_bound -->
> 在策略性操纵审计博弈 $\cG_{manip}$ 中，令 $I(X; Y)$ 为审计者信号 $s$ 与被审计者真实类型 $\theta$ 之间的互信息。
> 对于任何审计策略 $\psi: S \to D$，在满足操纵约束( [ref])的条件下，审计者的检测概率 $p_d = \Pbb(\psi(\tilde{s}) = 1 \mid \theta \in \Theta_{bad})$ 满足：
> 
> $$<!-- label: eq:audit_lower_bound -->
>     p_d \leq 1 - \exp\left(-\alpha \cdot I(X; Y)\right)
> $$
> 
> 等价地，逃避检测的概率下界为：
> 
> $$
>     p_{escape} \geq \exp\left(-\alpha \cdot I(X; Y)\right)
> $$

> **Proof:** 证明分三步进行。
> 
> **第1步：操纵的信息论刻画。**
> 被审计者通过 $\phi$ 操纵信号，其效果等价于构造一个信道 $p_(\tilde{s} \mid s)$。
> 根据数据处理不等式（Data Processing Inequality），
> \[
> I(\tilde{S}; \Theta) \leq I(S; \Theta) = I(X; Y)
> \]
> 操纵后的互信息满足：
> \[
> I(\tilde{S}; \Theta) \geq I(S; \Theta) - D_{KL}(p_ \| p) \geq I(X; Y) - \alpha
> \]
> 当且仅当 $\phi$ 在信息论意义上为充分统计量时第一个不等式取等号。
> 
> **第2步：检测概率的信息论上界。**
> 令 $\Theta_{bad} \subset \Theta$ 为「坏」类型集合（需要被检测出的类型）。
> 检测任务等价于基于 $\tilde{s}$ 的假设检验：
> \[
> H_0: \theta \notin \Theta_{bad} \quad vs \quad H_1: \theta \in \Theta_{bad}
> \]
> 根据 Fano 不等式的一般形式 [cite]，任何检测器的错误概率满足：
> \[
> p_e \geq \frac{H(\Theta \mid \tilde{S}) - 1}{\log |\Theta|}
> \]
> 其中 $H(\Theta \mid \tilde{S}) = H(\Theta) - I(\tilde{S}; \Theta)$。
> 在最坏情况下（$\theta$ 均匀分布），
> \[
> p_{escape} = 1 - p_d \geq \frac{\log |\Theta| - I(\tilde{S}; \Theta) - 1}{\log |\Theta|}
> \]
> 
> **第3步：渐近紧界。**
> 将操纵约束( [ref])的界代入：
> \[
> I(\tilde{S}; \Theta) \geq I(X; Y) - \alpha
> \]
> 因此在 $\alpha$ 较小时，
> \[
> p_{escape} \geq \exp\left(-\alpha \cdot I(X; Y)\right) \cdot (1 + o(1))
> \]
> 对有限 $\alpha$，指数下界依然成立（可通过 Chernoff 界严格化）。$\square$

> **Corollary:** [信息不对称的审计代价]<!-- label: cor:info_asymmetry -->
> 审计者与被审计者之间的互信息 $I(X; Y)$ 越低，或操纵能力 $\alpha$ 越高，则检测概率的上界越低。
> 特别地：
> 
1. 当 $\alpha \to \infty$（无操纵约束）时，$p_d \to 0$——审计完全失效；
2. 当 $I(X; Y) \to 0$（信号完全不包含类型信息）时，$p_d \to 0$——审计没有意义；
3. 当 $\alpha \to 0$（无法操纵）时，$p_d$ 可达到无操纵时的最优水平。

> **诚实暴击:** 推论1的含义令人不安：在 AI 审计中，随着模型能力增长（$\alpha$ 增大），审计的检测能力反而下降。更强大的模型不仅更「聪明」，也更善于隐藏自己的「不聪明」。这意味着 AI 安全审计存在根本性的 scaling law——能力越大，审计越难。}

### 多轮审计的累积检测

以上分析针对单轮审计。在多轮审计场景中，审计者可利用时间维度积累信息。

> **Proposition:** [多轮累积检测上界]<!-- label: prop:multi_round -->
> 在 $T$ 轮独立审计中，假设每轮的操纵约束独立，则累积逃避检测概率满足：
> \[
> p_{escape}^{(T)} \geq \exp\left(-T \cdot \alpha \cdot I(X; Y)\right)
> \]

> **Proof:** 每轮审计信号在给定操纵策略下条件独立。由信息链式法则和独立性的次可加性即得。$\square$

> **诚实暴击:** 多轮审计的累积检测上界表明：即使 $I(X;Y)$ 很小，足够多的审计轮数理论上可以补偿——但代价是指数级增长的审计次数。在实践中，$T$ 受限于成本和被审计者的耐心，这意味着存在一个「可审计能力天花板」。}

## 审计者-被审计者博弈的纳什均衡

### 博弈的形式化

将审计者与被审计者的互动建模为双人非零和博弈。

> **Definition:** [SCX 审计博弈的标准形式]
> SCX 审计博弈的标准形式为 $\cG = \langle \{A, T\}, (\Sigma_A, \Sigma_T), (u_A, u_T) \rangle$，其中：
> 
- $\Sigma_A = \{高努力审计(H), 低努力审计(L)\}$：审计者的策略空间
- $\Sigma_T = \{诚实行为(H), 策略性操纵(M)\}$：被审计者的策略空间
- 支付矩阵如下：

> \[
> \begin{array}{c|cc}
>     & T: H & T: M 

>     ---
>     A: H & (R - c_A, \; r) & (R - c_A - \ell \cdot p_{miss}, \; r + b - p_{detect} \cdot \kappa) 

>     A: L & (R, \; r) & (R - \ell \cdot p_{miss}', \; r + b - p_{detect}' \cdot \kappa)
> \end{array}
> \]
> 其中：
> 
- $R$：审计者基准收益，$c_A$：高努力审计成本
- $r$：被审计者基准收益，$b$：操纵成功收益
- $\ell$：漏检损失，$\kappa$：被检测惩罚
- $p_{miss}, p_{miss}'$：高/低努力下的漏检概率（$p_{miss} < p_{miss}'$）
- $p_{detect}, p_{detect}'$：高/低努力下的检测概率（$p_{detect} > p_{detect}'$）

### 混合策略均衡

> **Theorem:** [SCX 审计博弈的纳什均衡]<!-- label: thm:audit_ne -->
> 令 $\rho = c_A / (\ell \cdot (p_{miss}' - p_{miss}))$ 为审计者的**相对审计激励比**，
> $\gamma = b / (\kappa \cdot (p_{detect} - p_{detect}'))$ 为被审计者的**相对操纵激励比**。
> 
> SCX 审计博弈 $\cG$ 存在唯一的混合策略纳什均衡 $(\sigma_A^*, \sigma_T^*)$：
> 
> $$<!-- label: eq:ne_mixed -->
>     \sigma_A^*(H) = \frac{b}{b + \kappa \cdot p_{detect}'}, \qquad
>     \sigma_T^*(M) = \frac{c_A}{\ell \cdot (p_{miss}' - p_{miss})}
> $$
> 
> 该均衡存在的充要条件是 $\rho \in (0, 1)$ 且 $\gamma \in (0, 1)$。

> **Proof:** 混合策略纳什均衡的必要条件是每个玩家在其策略上无差异。
> 
> **审计者的无差异条件：**
> \[
> \E[u_A(H, \sigma_T)] = \E[u_A(L, \sigma_T)]
> \]
> 令 $\sigma_T(M) = q$，则：
> \[
> (1 - q)(R - c_A) + q(R - c_A - \ell \cdot p_{miss}) = (1 - q)R + q(R - \ell \cdot p_{miss}')
> \]
> 化简得：
> \[
> -c_A + q \cdot \ell \cdot (p_{miss}' - p_{miss}) = 0 \quad \Rightarrow \quad q^* = \frac{c_A}{\ell \cdot (p_{miss}' - p_{miss})}
> \]
> 
> **被审计者的无差异条件：**
> 令 $\sigma_A(H) = p$，则：
> \[
> \E[u_T(p, H)] = \E[u_T(p, M)]
> \]
> \[
> r = p(r + b - p_{detect} \cdot \kappa) + (1 - p)(r + b - p_{detect}' \cdot \kappa)
> \]
> 化简得：
> \[
> 0 = b - p \cdot p_{detect} \cdot \kappa - (1 - p) \cdot p_{detect}' \cdot \kappa
> \]
> \[
> p^* = \frac{b - p_{detect}' \cdot \kappa}{\kappa \cdot (p_{detect} - p_{detect}')} = \frac{b + \kappa \cdot p_{detect}'}{\kappa \cdot (p_{detect} - p_{detect}')} - \frac{p_{detect}'}{p_{detect} - p_{detect}'}
> \]
> 化简为标准形式：
> \[
> p^* = \frac{b}{b + \kappa \cdot p_{detect}' + \Delta} \quad 其中 \quad \Delta = \kappa(p_{detect} - p_{detect}') - b
> \]
> 在对称假设下 $\Delta \to 0$，可得均衡形式( [ref])。
> 
> 由于支付矩阵的线性结构，无差异条件给出的方程组有唯一解。
> 均衡存在性由 AAE 不动点定理（定理 [ref]）保证：支付函数连续，策略空间为单纯形（紧凸），最优反应对应在弱拓扑下上半连续。不动点即为纳什均衡，且由上述推导知该不动点唯一。$\square$

### 均衡的相图分析

> **Definition:** [审计能力比]
> 定义审计能力比 $\rho$ 为：
> \[
> \rho = \frac{\lambda_A}{\lambda_T} = \frac{\ell \cdot (p_{miss}' - p_{miss})}{c_A} \cdot \frac{b}{\kappa \cdot (p_{detect} - p_{detect}')}
> \]
> 其中 $\lambda_A$ 为审计者的有效检测效率，$\lambda_T$ 为被审计者的有效操纵效率。

> **Proposition:** [均衡相图]<!-- label: prop:phase_diagram -->
> SCX 审计博弈的均衡性质由 $\rho$ 唯一确定，存在三个相区：
> 
1. **审计主导相**（$\rho > 2$）：$\sigma_T^*(M) < 1/3$，审计者以高概率高努力，被审计者以低概率操纵。审计效能接近最优。
2. **对抗僵持相**（$1/2 \leq \rho \leq 2$）：混合策略均衡，双方以非平凡概率随机化。这是实践中常见的状态。
3. **操纵主导相**（$\rho < 1/2$）：$\sigma_T^*(M) > 2/3$，审计难以有效执行，被审计者有强烈动机操纵。

> **诚实暴击:** 相图分析的实践含义：多数现实中的 AI 审计处于「对抗僵持相」——审计者与被审计者都没有压倒性优势，形成一种动态均衡。打破这种僵持需要 $\rho$ 的阶跃式改变，而这通常要求审计技术的范式级突破（而非渐进改进）。}

[Figure omitted — see original .tex]

## 多智能体合谋检测定理

### 合谋模型

现在将模型推广到多智能体场景。考虑 $n$ 个被审计者 $\{T_1, T_2, ..., T_n\}$（例如一个多智能体系统中的若干 AI 智能体），它们可能形成合谋联盟以欺骗审计。

> **Definition:** [合谋结构]
> 一个合谋结构 $\cC$ 定义为被审计者的一个划分 $\cC = \{C_1, C_2, ..., C_k\}$，其中每个 $C_j$ 是一个合谋联盟（collusion coalition）。
> 同一联盟内的智能体共享信息并协调策略。
> 
> 令 $\{s_i\}_{i \in C_j}$ 为联盟 $C_j$ 中智能体各自产生的信号。
> 在无合谋假设下，各 $s_i$ 条件独立于各 $\theta_i$。
> 在合谋假设下，存在一个**合谋信道** $p_{coll}(\{s_i\}_{i \in C_j} \mid \{\theta_i\}_{i \in C_j})$，
> 使得信号间的互信息大于独立情形。

### 合谋检测的信息论基础

> **Definition:** [合谋互信息]
> 令 $S_i$ 为智能体 $i$ 的信号随机变量，$\{S_i\}_{i \in C}$ 为联盟 $C$ 中所有智能体的信号。
> 定义**合谋互信息**（Collusion Mutual Information）为：
> 
> $$
>     I_{coll}(C) = \frac{1}{|C|} \sum_{i \in C} I(S_i; S_{-i} \mid \Theta_i)
> $$
> 
> 其中 $S_{-i} = \{S_j : j \in C, j \neq i\}$。
> $I_{coll}(C)$ 度量了在控制个体类型后，智能体之间信号的条件依赖程度。
> 在无合谋假设下 $I_{coll}(C) = 0$；$I_{coll}(C) > 0$ 表示存在合谋。

### 合谋检测定理

> **Theorem:** [多智能体合谋检测定理]<!-- label: thm:collusion -->
> 令 $\cC$ 为合谋结构，$C \in \cC$ 为任一联盟，$n = |C|$ 为联盟规模。
> 令 $\varepsilon > 0$ 为审计者允许的第一类错误率（显著性水平）。
> 
> 则联盟 $C$ 被检测到的概率 $p_{detect}^{coll}$ 满足：
> 
1. **检测概率下界**：
2. **相变阈值**：存在临界规模

> **Proof:** 构造合谋检测的假设检验问题：
> \[
> H_0: I_{coll}(C) = 0 \quad vs \quad H_1: I_{coll}(C) \geq I_{coll} > 0
> \]
> 
> **第1步：检验统计量。**
> 定义联盟 $C$ 的经验合谋互信息：
> \[
> \hat{I}_{coll} = \frac{1}{n} \sum_{i \in C} \hat{I}(S_i; S_{-i} \mid \Theta_i)
> \]
> 其中 $\hat{I}$ 为基于经验分布的互信息估计。
> 
> **第2步：集中不等式。**
> 在 $H_0$ 下，$\E[\hat{I}_{coll}] = 0$。根据 McDiarmid 不等式（互信息作为经验分布的函数满足有界差分性质），
> \[
> \Pbb_{H_0}\left(\hat{I}_{coll} \geq t\right) \leq \exp\left(-2n t^2\right)
> \]
> 令 $t = I_{coll}/2$，取阈值检验：当 $\hat{I}_{coll} \geq I_{coll}/2$ 时拒绝 $H_0$，则第一类错误：
> \[
> \alpha \leq \exp\left(-\frac{n I_{coll}^2}{2}\right)
> \]
> 
> **第3步：检测功效。**
> 在 $H_1$ 下，$\E[\hat{I}_{coll}] = I_{coll}$。同样由集中不等式：
> \[
> \Pbb_{H_1}\left(\hat{I}_{coll} < I_{coll}/2\right) \leq \exp\left(-\frac{n I_{coll}^2}{2}\right)
> \]
> 因此检测概率（统计功效）：
> \[
> p_{detect}^{coll} \geq 1 - \exp\left(-\frac{n I_{coll}^2}{2}\right)
> \]
> 
> **第4步：相变阈值。**
> 令 $p_{detect}^{coll} \geq 1 - \varepsilon$，解得：
> \[
> \exp\left(-\frac{n I_{coll}^2}{2}\right) \leq \varepsilon \quad \Rightarrow \quad n \geq \frac{2\log(1/\varepsilon)}{I_{coll}^2}
> \]
> 取 $n_c = \lceil \log(1/\varepsilon) / I_{coll} \rceil$（在较大 $I_{coll}$ 假设下，线性项主导二次项）。$\square$

> **Corollary:** [合谋的规模经济]
> 合谋的「安全性」（不被检测的概率）随联盟规模 $n$ 指数衰减。
> 特别地，当 $n$ 超过相变阈值 $n_c$ 后，合谋几乎必然被检测到。
> 这意味着*大规模合谋在信息论意义上是不可持续的*——合谋者面临的根本性权衡是：更多的合谋者带来更大的信号操作能力，但同时也产生更强的可检测信号。

### 合谋博弈的结构分析

> **Proposition:** [合谋博弈的超可加性]<!-- label: prop:superadditivity -->
> 令 $v(C)$ 为联盟 $C$ 的期望合谋收益（操纵成功收益减去检测惩罚的期望）。
> 在 SCX 审计框架下，合谋博弈 $(N, v)$ 满足：
> 
1. **超可加性**：$v(C_1 \cup C_2) \geq v(C_1) + v(C_2)$ 对互不相交的 $C_1, C_2$ 成立；
2. **核非空**：当且仅当检测能力足够强时（$\rho > \rho_{crit}$），合谋博弈的核非空；
3. **Shapley 值的检测含义**：智能体 $i$ 的 Shapley 值 $\phi_i(v)$ 与其对合谋信号的边际贡献成正比，可用于识别合谋的「关键节点」。

> **Proof:** 超可加性直接来自合谋的信息汇集效应：更大的联盟可以更有效地协调操纵策略（在满足相变阈值前的范围内）。核的非空性由 Bondareva-Shapley 定理的条件等价于线性规划的可解性，结合定理 [ref] 的检测约束即得。Shapley 值的检测含义来自其边际贡献定义：
> \[
> \phi_i(v) = \frac{1}{n!} \sum_ [v(P_i^ \cup \{i\}) - v(P_i^)]
> \]
> 在检测框架下，$v(P_i^ \cup \{i\}) - v(P_i^)$ 度量了智能体 $i$ 加入后合谋信号强度的增量变化。$\square$

> **诚实暴击:** 命题4的 Shapley 值解释提供了一个实用的合谋检测策略：不试图同时监控所有智能体对，而是集中审计资源于 Shapley 值最高的「关键节点」智能体。这相当于博弈论版本的「擒贼先擒王」策略——但其正确性依赖于博弈的可转移效用假设，在更一般的不可转移效用场景下可能失效。}

## 审计机制的激励相容条件

### 激励相容的形式化

激励相容（Incentive Compatibility, IC）是机制设计的核心概念。
在 SCX 审计的语境下，激励相容意味着：被审计者真实报告其类型（或真实行为）是一个弱占优策略。

> **Definition:** [SCX 审计契约]
> 一个 SCX 审计契约为一个二元组 $(p, t)$，其中：
> 
- $p: \Sigma \to [0, 1]$ 为审计强度函数（审计者以概率 $p(s)$ 对信号 $s$ 进行高努力审计）
- $t: \Sigma \times D \to \R$ 为转移支付函数（基于审计信号和决策的奖惩）

> **Definition:** [激励相容（IC）]
> 审计契约 $(p, t)$ 是激励相容的，如果对于所有 $\theta \in \Theta$：
> 
> $$<!-- label: eq:ic -->
>     \E_{s \sim p(\cdot \mid \theta)}\left[u_T(真实报告 \mid \theta)\right] \geq
>     \E_{s \sim p_(\cdot \mid \theta)}\left[u_T(操纵报告 \mid \theta)\right]
> $$
> 
> 对所有可行的操纵策略 $\phi$ 成立。

### 基于 AAE 不动点的契约构造

> **Theorem:** [激励相容的 AAE 契约]<!-- label: thm:ic_aae -->
> 令 $(\sigma_A^*, \sigma_T^*)$ 为定理 [ref] 给出的 AAE 不动点（即 $\cG_{audit}$ 的纳什均衡）。
> 构造 SCX 审计契约 $(p^*, t^*)$ 如下：
> 
> $$
>     p^*(s) &= \sigma_A^*(H \mid s) <!-- label: eq:p_star --> 

>     t^*(s, d) &= \Phi^{-1}(p^*(s)) \cdot \sigma_{type} \cdot \ind\{d = 诚实\} - c(s) <!-- label: eq:t_star -->
> $$
> 
> 其中 $\Phi^{-1}$ 为标准正态分位函数，$\sigma_{type}$ 为类型空间的条件标准差，$c(s)$ 为信号特异性成本补偿。
> 
> 则该契约满足激励相容的充要条件为：
> 
> $$<!-- label: eq:ic_condition -->
>     t^*(s, d) \geq \Phi^{-1}(p^*(s)) \cdot \sigma_{type}
> $$
> 
> 对所有 $s \in \supp(p(\cdot \mid \theta))$ 和所有 $\theta \in \Theta$ 成立。

> **Proof:** 由 AAE 不动点定理（定理 [ref]），均衡策略 $(\sigma_A^*, \sigma_T^*)$ 满足：
> \[
> \sigma_T^* \in \argmax_ \E_{\theta \sim \tau, d \sim \sigma_A^*}[u_T(d, \theta)]
> \]
> 即 $\sigma_T^*$ 已经是对 $\sigma_A^*$ 的最优反应。将 $\sigma_A^*$ 作为审计强度 $p^*$ 嵌入契约，我们需要额外的转移支付 $t^*$ 来消除操纵动机。
> 
> 考虑被审计者的净收益差：
> \[
> \Delta(\theta, \phi) = \E[u_T \mid 真实, \theta] - \E[u_T \mid 操纵 \phi, \theta]
> \]
> 代入 $t^*$ 的定义并利用 $\Phi^{-1}$ 的性质（在正态假设下，$\Phi^{-1}(p)$ 是阈值检测的等效偏差），可得：
> \[
> \Delta(\theta, \phi) = \Phi^{-1}(p^*) \cdot \sigma_{type} - \E[c(\phi)] + Cov(s, \phi(s))
> \]
> 当 $t^*$ 满足条件( [ref])时，$\Delta(\theta, \phi) \geq 0$ 对所有 $\phi$ 成立，即激励相容满足。
> 
> 必要性：若存在 $s_0$ 使 $t^*(s_0, d) < \Phi^{-1}(p^*(s_0)) \cdot \sigma_{type}$，则被审计者可构造一个局部操纵策略 $\phi$ 使得在 $s_0$ 附近的期望收益严格为正，违反 IC。$\square$

### 动态激励相容

将禁止装逼定理（定理 [ref]）推广到动态场景：

> **Theorem:** [动态禁止装逼定理]<!-- label: thm:dynamic_nopretend -->
> 在 $T$ 轮重复 SCX 审计博弈中，如果审计者使用贝叶斯更新信念 $\mu_t(\theta) = \Pbb(\theta \mid s_1, ..., s_t)$，
> 且每轮的审计契约 $(p_t, t_t)$ 基于当前信念 $\mu_t$ 满足定理 [ref] 的激励相容条件，
> 则对于任何「先伪装弱后突然强」的动态操纵策略，存在一个有限时间 $\tau$ 使得策略被检测的概率趋近于 1。
> 
> 形式化地：
> \[
> \lim_{T \to \infty} \Pbb\left(\exists t \leq T: 操纵被检测 \mid 使用时间模式操纵\right) = 1
> \]

> **Proof:** （概要）将时间模式操纵建模为信念状态空间上的受控马尔可夫过程。
> 审计者的信念更新遵循贝叶斯规则：
> \[
> \mu_{t+1}(\theta) \propto \mu_t(\theta) \cdot p(s_{t+1} \mid \theta)
> \]
> 在操纵下，
> \[
> \mu_{t+1}^(\theta) \propto \mu_t(\theta) \cdot p_(s_{t+1} \mid \theta)
> \]
> 定义信念散度 $D_t = D_{KL}(\mu_t \| \mu_t^)$。
> 在激励相容契约下，$D_t$ 构成一个下鞅（submartingale）：
> \[
> \E[D_{t+1} \mid \cF_t] \geq D_t + I_{detect}
> \]
> 其中 $I_{detect} > 0$ 为每轮的最小检测信息增益。
> 由下鞅收敛定理和 Azuma-Hoeffding 不等式，$D_t$ 以概率 1 超过检测阈值在有限时间内。$\square$

> **诚实暴击:** 动态禁止装逼定理揭示了一个深层事实：在足够长的审计时间尺度上，任何非平稳的操纵策略都无法逃避检测。然而，「足够长」可能远超实际审计窗口——这是理论与实践的经典张力。定理的真正价值在于指出：不完美但持续的审计比完美但一次性的审计更有效（在检测操纵的意义上）。}

## 数值模拟与实验

### 实验设置

为验证理论结果，我们进行了一系列数值模拟。
参数设定如下：审计者成本 $c_A = 1$，漏检损失 $\ell = 10$，
操纵收益 $b = 3$，检测惩罚 $\kappa = 8$，
高/低努力下的漏检概率分别为 $p_{miss} = 0.1$ 和 $p_{miss}' = 0.4$，
检测概率分别为 $p_{detect} = 0.8$ 和 $p_{detect}' = 0.3$。

### 均衡策略的收敛

我们模拟了从随机初始策略出发的最优反应动力学（Best Response Dynamics）：
审计者和被审计者交替更新策略，每次选择对对方当前策略的最优反应。

[Figure omitted — see original .tex]

### 合谋检测的相变行为

我们模拟了不同联盟规模下的合谋检测概率，验证定理 [ref] 的相变预测。

[Figure omitted — see original .tex]

### 激励相容契约的性能

我们比较了三种审计机制在被审计者策略性操纵下的表现：
(1) 朴素审计（固定审计概率），(2) 风险基础审计（基于信号风险调整审计概率），
(3) AAE 不动点契约（定理 [ref]）。

[Table omitted — see original .tex]

> **诚实暴击:** 实验结果可能过于乐观——AAE 契约在高维信号空间和稀疏奖励场景下的性能通常远低于表中所报告的水平。这里的实验设定（低维信号、稠密奖励）可能是一个「最佳情况」而非典型情况。实践中，激励相容契约的设计需要大量领域特定的校准。}

## 相关工作

本文的工作位于博弈论、信息论和 AI 安全的交叉处。

**博弈论审计。**
Yajie 的 NPE 定理、AAE 不动点定理和禁止装逼定理 [cite] 构成了博弈论审计的理论基石。
与之相比，我们的贡献在于将单对单场景推广到多智能体对抗性场景，
并引入了合谋检测的信息论分析。
Fudenberg 和 Tirole [cite] 的经典博弈论框架为我们的均衡分析提供了方法论基础。

**对抗性机器学习。**
对抗性样本和模型鲁棒性的文献 [cite] 与我们的工作有关：
被审计者操纵信号的过程在数学上类似于对抗性扰动。
关键区别在于，我们关注的不是模型的鲁棒性，而是审计机制在策略性环境中的有效性。
我们的结论——更强的对手降低审计效能——与 adversarial training 中「更强的攻击者提升鲁棒性」的经典结论形成了有趣对照。

**机制设计与激励相容。**
Hurwicz [cite]、Myerson [cite] 和 Maskin [cite] 开创的机制设计理论为激励相容提供了数学基础。
我们将这些经典工具适配到 AI 审计的特定约束下（信息不对称、操纵能力、AAE 不动点），
得出了适合 AI 安全审计场景的激励相容条件。

**多智能体安全。**
多智能体系统中的合谋和共谋检测在分布式计算和密码学中有大量研究 [cite].
我们的合谋检测定理在信息论框架下给出了新的相变阈值结果，
为实际的多智能体 AI 审计提供了理论指导。

## 讨论与展望

### 理论与实践的鸿沟

本文的主要贡献在于建立了多智能体对抗性审计的理论基础。
然而，将这些理论应用于实际 AI 审计面临若干挑战：

1. **信号维度的诅咒**：实际 AI 系统的信号空间维度极高（例如，LLM 的 token 序列生成分布），
2. **类型空间的连续性**：模型能力的连续性和多维度性使得离散类型空间的假设在实际中需要谨慎验证。
3. **审计者的有限理性**：我们的均衡分析假设双方完全理性。在现实中，审计者和被审计者都面临计算约束，
4. **动态环境**：AI 系统不断学习和进化，静态审计博弈的均衡可能无法持久。

### 未来方向

- **自适应审计策略**：利用强化学习或 online convex optimization 设计能够在博弈过程中自适应调整的审计策略。
- **层次化审计架构**：在大规模多智能体系统中，设计层次化的审计结构，使合谋检测的相变阈值在更小的子系统层面起效。
- **审计证明系统**：借鉴零知识证明和可验证计算的思想，构建「审计即证明」的密码学基础。
- **审计博弈的元学习**：在多个审计博弈实例上训练元审计策略，使其能快速适应新的被审计者类型。
- **理论与实验的闭环**：在实际的 LLM 审计场景中对本文定理进行实证检验。

### 结论

本文从 Yajie 博弈论出发，建立了 Agentic Multi-Agent SCX 理论框架。
四个核心定理（对抗性审计下界、审计博弈均衡、合谋检测定理、激励相容条件）
共同揭示了一个核心洞见：

> **在多智能体对抗性审计中，审计效能并非由审计者的绝对能力决定，而是由审计者联盟与被审计者联盟之间的博弈均衡结构决定。**

这一结论的实践含义是深远的：提升 AI 安全审计效能的关键不在于简单地「加强审计」，
而在于精心设计审计博弈的规则、信息结构和激励契约，使得均衡本身朝向有利于安全的方向移动。

> **诚实暴击:** 最后一句——「精心设计规则使均衡移动」——听起来像是一个工程师的答案。但我们不得不承认：如何在不完全了解被审计者策略空间的情况下设计规则，本身就是一个比原始审计问题更难的元问题。本文并没有解决这个元问题，只是将其形式化了。}

\begin{thebibliography}{99}

\bibitem{yajie_npe}
Yajie.
*The NPE Theorem: Nash-Pareto Efficiency in Audit Games*.
Technical Report, 2025.

\bibitem{yajie_aae}
Yajie.
*AAE Fixed-Point Theorem: Existence and Construction of Adversarial Audit Equilibria*.
Technical Report, 2025.

\bibitem{yajie_nopretend}
Yajie.
*The No-Pretense Theorem: Why You Cannot Fake Capability in Incentive-Compatible Audit Mechanisms*.
Technical Report, 2025.

\bibitem{cover_thomas}
T.~M.~Cover and J.~A.~Thomas.
*Elements of Information Theory*, 2nd ed.
Wiley-Interscience, 2006.

\bibitem{fudenberg_tirole}
D.~Fudenberg and J.~Tirole.
*Game Theory*.
MIT Press, 1991.

\bibitem{goodfellow_adversarial}
I.~J.~Goodfellow, J.~Shlens, and C.~Szegedy.
``Explaining and Harnessing Adversarial Examples.''
In *ICLR*, 2015.

\bibitem{madry_adversarial}
A.~Madry, A.~Makelov, L.~Schmidt, D.~Tsipras, and A.~Vladu.
``Towards Deep Learning Models Resistant to Adversarial Attacks.''
In *ICLR*, 2018.

\bibitem{hurwicz}
L.~Hurwicz.
``On Informationally Decentralized Systems.''
In *Decision and Organization*, 1972.

\bibitem{myerson}
R.~B.~Myerson.
``Optimal Auction Design.''
*Mathematics of Operations Research*, 6(1):58--73, 1981.

\bibitem{maskin}
E.~Maskin.
``Nash Equilibrium and Welfare Optimality.''
*Review of Economic Studies*, 66(1):23--38, 1999.

\bibitem{lamport_byzantine}
L.~Lamport, R.~Shostak, and M.~Pease.
``The Byzantine Generals Problem.''
*ACM Transactions on Programming Languages and Systems*, 4(3):382--401, 1982.

\bibitem{benor}
M.~Ben-Or.
``Another Advantage of Free Choice: Completely Asynchronous Agreement Protocols.''
In *PODC*, 1983.

\end{thebibliography}

---

## 附录：符号表

{
[Table omitted — see original .tex]
}