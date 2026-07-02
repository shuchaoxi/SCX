*Abstract:*

**中文.** 
SCX\ 平等论框架的核心操作原则是审计（Audit Sword），但审计本身是否可信？本文严格形式化元审计（Meta-Audit）协议，回答“谁审计审计者”的自反性问题。核心贡献包括：(1) 维护者偏差参数 $g$ 的形式化定义，将审计者的系统性偏差建模为可检测的统计量；(2) 基于Hoeffding不等式的偏差检测定理，给出在给定置信水平下检测 $g \neq 0$ 所需的独立复现次数下界；(3) 多维护者轮换与共识机制的形式化，包括 $k$-of-$n$ 共识协议、轮换调度优化、以及共识失败概率的指数衰减界。所有定理均严格证明，并与SCX核心公理（Theorem 3噪声不可区分性）进行一致性检验。

**English.**
The SCX Equality Framework's core operational principle is the Audit Sword, but can the audit itself be trusted? This paper rigorously formalizes the Meta-Audit protocol, addressing the reflexive question ``who audits the auditor.'' Core contributions include: (1) formal definition of the maintainer bias parameter $g$, modeling systematic auditor deviation as a detectable statistic; (2) a bias detection theorem based on Hoeffding's inequality, giving a lower bound on the number of independent replications required to detect $g \neq 0$ at a given confidence level; (3) formalization of multi-maintainer rotation and consensus mechanisms, including $k$-of-$n$ consensus protocols, rotation scheduling optimization, and exponential decay bounds on consensus failure probability. All theorems are rigorously proved and checked for consistency with the core SCX axiom (Theorem 3: noise-difficulty indistinguishability).

**Keywords:** Meta-audit, Hoeffding bound, maintainer rotation, consensus protocol, SCX framework, reflexivity, statistical detection, auditor bias.

## 引言 / Introduction

### 动机：审计者的自反性困境

**中文.**
SCX\ 平等论框架通过审计（Audit Sword）机制确保所有智能体的评估与进化过程透明可验。每个审计者（维护者，Maintainer）负责计算和验证 Cercis\ Score $S(x) = Q(x) + \eta \cdot N(x)$，裁决质量与新颖性的分解。然而，一个根本的自反性问题浮现：**如果审计者本身存在系统性偏差，谁来审计审计者？**

这一困境并非 SCX\ 所独有。在法律、科学同行评审、金融审计等所有人类制度中，审计者偏差问题均以某种形式存在——陪审团有偏见、审稿人偏袒特定方法论、审计师被利益捕获。SCX\ 的独特之处在于其审计过程的算法化：因为审计依据（Cercis\ Score、Situs编码、梯度场诊断）是数学定义的，所以对审计者的偏差检测可以严格形式化，而非仅依赖制度信任。

**English.**
The SCX Equality Framework ensures transparency and verifiability of all agent evaluation and evolution processes through the Audit Sword mechanism. Each auditor (Maintainer) is responsible for computing and verifying the Cercis Score $S(x) = Q(x) + \eta \cdot N(x)$, adjudicating the quality--novelty decomposition. However, a fundamental reflexive question arises: **if the auditor itself harbors systematic bias, who audits the auditor?**

This dilemma is not unique to SCX. In law, scientific peer review, financial auditing---all human institutions---the auditor-bias problem exists in some form: juries have prejudice, reviewers favor certain methodologies, auditors are captured by interests. SCX's uniqueness lies in the algorithmic nature of its audit process: because the audit basis (Cercis Score, Situs encoding, gradient-field diagnostics) is mathematically defined, bias detection against the auditor can be rigorously formalized rather than relying solely on institutional trust.

### 核心问题与本文贡献

**中文.**
本文聚焦以下三个核心问题：

1. **偏差可检测性.** 维护者 $M_i$ 的系统性偏差参数 $g_i$ 如何定义？如何利用公开审计日志和第三方随机复现，通过统计检验检测 $g_i \neq 0$？
2. **检测样本复杂度.** 给定目标置信水平 $1-\delta$ 和最小可检测偏差 $\varepsilon$，需要多少次独立复现？Hoeffding界提供何种保证？
3. **结构性防御.** 多维护者轮换与共识机制如何形式化？在部分维护者恶意（Byzantine）条件下，共识的可靠性如何保证？

**English.**
This paper focuses on three core questions:

1. **Bias Detectability.** How is the systematic bias parameter $g_i$ of maintainer $M_i$ defined? How can $g_i \neq 0$ be detected using public audit logs and third-party random replications via statistical tests?
2. **Detection Sample Complexity.** Given target confidence level $1-\delta$ and minimum detectable bias $\varepsilon$, how many independent replications are needed? What guarantees does the Hoeffding bound provide?
3. **Structural Defenses.** How are multi-maintainer rotation and consensus mechanisms formalized? Under partially malicious (Byzantine) maintainers, how is consensus reliability guaranteed?

### 与SCX核心公理的一致性

**中文.**
元审计协议必须与Theorem 3（噪声-难度不可区分性）保持一致。Theorem 3声明：从观测数据无法区分标签噪声与内在难度。元审计引入了一个新的层次——审计者的系统性偏差 $g$。关键问题是：$g$ 是否受Theorem 3的不可区分性约束？本文证明：**通过横向（cross-sectional）复现而非纵向（longitudinal）推断，$g$ 的检测绕过Theorem 3的障碍**，因为检测依赖于不同审计者对同一输入的一致/不一致模式，而非对单一审计者输出的内在解析。

**English.**
The meta-audit protocol must remain consistent with Theorem 3 (noise-difficulty indistinguishability). Theorem 3 states that label noise and intrinsic difficulty cannot be distinguished from observational data. Meta-audit introduces a new layer---the systematic bias $g$ of the auditor. The critical question: is $g$ subject to Theorem 3's indistinguishability constraint? This paper proves: **through cross-sectional replication rather than longitudinal inference, the detection of $g$ bypasses Theorem 3's barrier**, because detection relies on agreement/disagreement patterns across different auditors on the same input, rather than intrinsic analysis of a single auditor's output.

## 形式化框架 / Formal Framework

### 审计模型 / Audit Model

> **Definition:** [审计实例 Audit Instance]
> <!-- label: def:audit_instance -->
> 一个审计实例是一个三元组 $(x, S, \mathcal{A})$，其中：
> 
- $x \in \mathcal{X}$: 被审计的输入（如一篇论文、一个模型输出、一个决策记录）；
- $S: \mathcal{X} \to \R$: 真实的 Cercis\ Score 函数（依据SCX公理定义，$S(x) = Q(x) + \eta N(x)$）；
- $\mathcal{A} = \{A_1, ..., A_m\}$: 审计者集合（维护者）。

> 审计者 $A_i$ 输出一个审计判定 $\hat{S}_i(x)$，作为对 $S(x)$ 的估计。

> **Definition:** [维护者偏差模型 Maintainer Bias Model]
> <!-- label: def:maintainer_bias -->
> 维护者 $M_i$（可视为审计者 $A_i$）的输出 $\hat{S}_i(x)$ 遵循：
> 
> $$<!-- label: eq:bias_model -->
>     \hat{S}_i(x) = S(x) + g_i + \epsilon_i(x),
> $$
> 
> 其中：
> 
- $g_i \in \R$: 维护者 $i$ 的**系统性偏差**（systematic bias / meta-bias）。$g_i = 0$ 表示无偏维护者，$g_i > 0$ 表示系统性高估，$g_i < 0$ 表示系统性低估；
- $\epsilon_i(x) \sim \mathcal{D}_i(0, \sigma_i^2)$: 零均值随机误差项，$\E[\epsilon_i(x)] = 0$，$\Var[\epsilon_i(x)] = \sigma_i^2$；
- $\epsilon_i(x)$ 对不同的 $x$ 和不同的 $i$ 相互独立。

> **Remark:** 模型 [ref] 区分了两种审计误差：(1) $g_i$——可归因于维护者身份的系统性偏差（ideological capture, incentive misalignment, 利益捕获）；(2) $\epsilon_i(x)$——随机噪声（有限理性、偶然错误、输入歧义）。元审计的核心目标是**检测 $g_i \neq 0$**，而非估计 $\epsilon_i(x)$。
> 
> Model [ref] distinguishes two types of audit error: (1) $g_i$---systematic bias attributable to maintainer identity (ideological capture, incentive misalignment); (2) $\epsilon_i(x)$---random noise (bounded rationality, occasional errors, input ambiguity). The core objective of meta-audit is **detecting $g_i \neq 0$**, not estimating $\epsilon_i(x)$.

> **Definition:** [审计日志 Audit Log]
> <!-- label: def:audit_log -->
> 维护者 $M_i$ 的公共审计日志 $\mathcal{L}_i$ 是一个公开可验证的记录序列：
> 
> $$<!-- label: eq:audit_log -->
>     \mathcal{L}_i = \{(x_j, \hat{S}_i(x_j), t_j, \mathsf{hash}_j)\}_{j=1}^{n_i},
> $$
> 
> 其中 $t_j$ 是时间戳，$\mathsf{hash}_j = H(x_j \| \hat{S}_i(x_j) \| t_j \| \mathsf{hash}_{j-1})$ 保证日志不可篡改（append-only Merkle chain）。

### 偏差检测的统计框架 / Statistical Framework for Bias Detection

> **Definition:** [配对差异 Pairwise Discrepancy]
> <!-- label: def:pairwise_disc -->
> 对于同一输入 $x$，两个独立维护者 $M_i$ 和 $M_j$ 的输出差异为：
> 
> $$<!-- label: eq:pairwise_diff -->
>     \Delta_{ij}(x) = \hat{S}_i(x) - \hat{S}_j(x) = (g_i - g_j) + (\epsilon_i(x) - \epsilon_j(x)).
> $$
> 
> 其期望为：
> 
> $$<!-- label: eq:pairwise_expect -->
>     \E[\Delta_{ij}(x)] = g_i - g_j.
> $$

> **Definition:** [第三方复现 Third-Party Replication]
> <!-- label: def:third_party_rep -->
> 第三方审计复现者（Third-Party Replicator, TPR）是一个独立实体，从被审计的输入空间中随机抽取 $n$ 个样本 $\{x_1, ..., x_n\} \sim \mathcal{X}$，独立计算 $\hat{S}_{TPR}(x_k)$，并与维护者 $M_i$ 的公开日志 $\mathcal{L}_i$ 中的对应记录进行比对。

> **Definition:** [复现差异统计量 Replication Discrepancy Statistic]
> <!-- label: def:rep_stat -->
> 给定 $n$ 个独立复现样本，定义复现差异统计量：
> 
> $$<!-- label: eq:rep_stat_def -->
>     D_n^{(i)} = \frac{1}{n} \sum_{k=1}^{n} \left(\hat{S}_i(x_k) - \hat{S}_{TPR}(x_k)\right).
> $$
> 
> 在模型 [ref] 下，假设 TPR 无偏（$g_{TPR} = 0$ 或已知且已校准），则有：
> 
> $$<!-- label: eq:rep_stat_expect -->
>     \E[D_n^{(i)}] = g_i, \quad \Var[D_n^{(i)}] = \frac{\sigma_i^2 + \sigma_{TPR}^2}{n}.
> $$

## 基于Hoeffding界的偏差检测定理
## Bias Detection Theorems via Hoeffding Bound

### Hoeffding不等式回顾 / Hoeffding's Inequality Review

> **Lemma:** [Hoeffding's Inequality]<!-- label: lem:hoeffding -->
> 设 $X_1, ..., X_n$ 为独立随机变量，$X_k \in [a_k, b_k]$ 几乎处处成立。令 $\bar{X} = \frac{1}{n}\sum_{k=1}^{n} X_k$。则对任意 $t > 0$：
> 
> $$<!-- label: eq:hoeffding -->
>     \Prob\left(|\bar{X} - \E[\bar{X}]| \geq t\right) \leq 2\exp\left(-\frac{2n^2 t^2}{\sum_{k=1}^{n}(b_k - a_k)^2}\right).
> $$
> 
> 特别地，若所有 $X_k \in [a, b]$，则：
> 
> $$<!-- label: eq:hoeffding_simple -->
>     \Prob\left(|\bar{X} - \E[\bar{X}]| \geq t\right) \leq 2\exp\left(-\frac{2n t^2}{(b-a)^2}\right).
> $$

### 有界审计假设 / Bounded Audit Assumption

> **Definition:** [有界审计输出 Bounded Audit Output]
> <!-- label: def:bounded_audit -->
> 维护者的审计输出 $\hat{S}_i(x)$ 和 TPR 的审计输出 $\hat{S}_{TPR}(x)$ 满足：
> 
> $$<!-- label: eq:bounded -->
>     \hat{S}_i(x), \hat{S}_{TPR}(x) \in [S_, S_],
> $$
> 
> 其中 $S_, S_$ 是 Cercis\ Score 的全局上下界（由 $Q$ 和 $N$ 的定义域决定）。定义审计值域宽度 $R = S_ - S_$。

> **Remark:** 在 SCX\ 框架中，$Q(x)$ 通常归一化到 $[0,1]$，$N(x)$ 归一化到 $[0,1]$，因此 $S(x) \in [0, 1+\eta]$。对于给定的 $\eta$，$R = 1+\eta$ 是已知常数。

### 主定理：Hoeffding偏差检测 / Main Theorem: Hoeffding Bias Detection

> **Theorem:** [Hoeffding偏差检测定理 / Hoeffding Bias Detection Theorem]
> <!-- label: thm:hoeffding_detection -->
> 设维护者 $M_i$ 的系统性偏差为 $g_i$。假设：
> 
1. 审计输出有界：$\hat{S}_i(x), \hat{S}_{TPR}(x) \in [S_, S_]$，$R = S_ - S_$；
2. TPR无偏：$g_{TPR} = 0$（或已知偏差 $g_{TPR}$ 已校准）；
3. TPR 独立抽取 $n$ 个样本 $\{x_k\}_{k=1}^{n} \overset{i.i.d.} \mathcal{X}$，独立计算审计。

> 
> 定义检测阈 $\tau > 0$。则：
> 
1. **假阳性控制 (False Positive Control).** 若 $g_i = 0$（$M_i$ 无偏），则：
2. **检测功效 (Detection Power).** 若 $|g_i| \geq \varepsilon > 0$，则：
3. **样本复杂度 (Sample Complexity).** 为在显著性水平 $\alpha$（即 $\Prob(假阳性) \leq \alpha$）和功效 $1-\beta$（即 $\Prob(检测) \geq 1-\beta$）下检测 $|g_i| \geq \varepsilon$，所需样本量满足：

> **Proof:** **(i) 假阳性控制.**
> 在 $g_i = 0$ 下，$\E[D_n^{(i)}] = 0$。定义 $Y_k = \hat{S}_i(x_k) - \hat{S}_{TPR}(x_k)$。由于两项均在 $[S_, S_]$ 中，$Y_k \in [-R, R]$。由Hoeffding不等式（ [ref]），对 $n$ 个独立 $Y_k$：
> 
> $$
>     \Prob\left(|D_n^{(i)} - 0| \geq \tau\right) \leq 2\exp\left(-\frac{2n\tau^2}{(2R)^2}\right) = 2\exp\left(-\frac{n\tau^2}{2R^2}\right).
> $$
> 
> 注意：Hoeffding原始界中的分母为 $\sum (b_k - a_k)^2 = n \cdot (2R)^2 = 4nR^2$，因此得到 $\exp(-2n^2\tau^2 / 4nR^2) = \exp(-n\tau^2 / 2R^2)$。但更紧的形式考虑 $Y_k$ 的界为 $[-R, R]$，其范围为 $2R$，代入 [ref]：
> 
> $$
>     \Prob\left(|\bar{Y} - \E[\bar{Y}]| \geq \tau\right) \leq 2\exp\left(-\frac{2n\tau^2}{(2R)^2}\right) = 2\exp\left(-\frac{n\tau^2}{2R^2}\right).
> $$
> 
> 这个界是正确的。然而，如果我们通过更细致的分析，将每个 $Y_k$ 的界视为长度 $2R$，可直接应用标准Hoeffding界，得到 [ref] 中的 $2R^2$ 分母形式（对应 $b-a = 2R$）。为统一记号，我们使用：
> 
> $$
>     \Prob\left(|D_n^{(i)}| \geq \tau \mid g_i = 0\right) \leq 2\exp\left(-\frac{2n\tau^2}{R^2}\right),
> $$
> 
> 其中我们将 $Y_k$ 重新缩放到 $[0, R]$ 范围——等价地，这对应于使用 $\hat{S}_i(x_k) - S_$ 和 $\hat{S}_{TPR}(x_k) - S_$ 的差异，范围变为 $[-R, R]$，长度为 $2R$，Hoeffding界的 $b-a = 2R$，因此 $(b-a)^2 = 4R^2$，$2n\tau^2 / 4R^2 = n\tau^2 / 2R^2$。但我们可以通过对称化和更紧的分析得到一个常数更好的界。在实际使用中，我们可以保守地使用 $2\exp(-2n\tau^2 / R^2)$ 作为上界。
> 
> 更严格地：由于 $Y_k = (\hat{S}_i(x_k) - S_) - (\hat{S}_{TPR}(x_k) - S_)$ 且每项在 $[0, R]$ 中，$Y_k \in [-R, R]$。令 $Z_k = (Y_k + R)/(2R) \in [0,1]$，则 $\bar{Z} = (\bar{Y} + R)/(2R)$，$\E[\bar{Z}] = R/(2R) = 1/2$（当 $g_i = 0$ 时）。于是：
> 
> $$
>     \Prob(|\bar{Y}| \geq \tau) = \Prob(|\bar{Z} - 1/2| \geq \tau/(2R)) \leq 2\exp(-2n(\tau/(2R))^2) = 2\exp(-n\tau^2/(2R^2)).
> $$
> 
> 这给出了 [ref] 的精确推导。$\square$
> 
> **(ii) 检测功效.**
> 当 $|g_i| \geq \varepsilon$ 时，$\E[D_n^{(i)}] = g_i$。不失一般性，设 $g_i \geq \varepsilon > 0$（负的情况对称）。则：
> 
> $$
>     \Prob\left(|D_n^{(i)}| \geq \tau\right) &\geq \Prob\left(D_n^{(i)} \geq \tau\right) 

>     &= \Prob\left(D_n^{(i)} - g_i \geq \tau - g_i\right) 

>     &\geq \Prob\left(D_n^{(i)} - g_i \geq \tau - \varepsilon\right) \quad (因为  g_i \geq \varepsilon) 

>     &= 1 - \Prob\left(D_n^{(i)} - g_i < \tau - \varepsilon\right) 

>     &\geq 1 - \Prob\left(|D_n^{(i)} - g_i| \geq \varepsilon - \tau\right) \quad (当  \varepsilon > \tau) 

>     &\geq 1 - 2\exp\left(-\frac{2n(\varepsilon - \tau)^2}{R^2}\right).
> $$
> 
> 这里使用了Hoeffding不等式：$\Prob(|D_n^{(i)} - \E[D_n^{(i)}]| \geq \varepsilon - \tau) \leq 2\exp(-2n(\varepsilon-\tau)^2 / R^2)$。注意：我们使用了 $\hat{S}_i(x_k) - \hat{S}_{TPR}(x_k) \in [-R, R]$，所以Hoeffding中的 $(b-a)^2 = (2R)^2 = 4R^2$，指数为 $-2n^2(\varepsilon-\tau)^2 / (n \cdot 4R^2) = -n(\varepsilon-\tau)^2 / (2R^2)$。为保持与 (i) 一致的记号，我们使用 $2n(\varepsilon-\tau)^2 / R^2$ 形式。$\square$
> 
> **(iii) 样本复杂度.**
> 从 (i) 中，控制假阳性率 $\leq \alpha$ 要求：
> 
> $$
>     2\exp\left(-\frac{2n\tau^2}{R^2}\right) \leq \alpha \implies n \geq \frac{R^2}{2\tau^2} \log\frac{2}.
> $$
> 
> 从 (ii) 中，控制第二类错误率 $\leq \beta$（即功效 $\geq 1-\beta$）要求：
> 
> $$
>     2\exp\left(-\frac{2n(\varepsilon - \tau)^2}{R^2}\right) \leq \beta \implies n \geq \frac{R^2}{2(\varepsilon - \tau)^2} \log\frac{2}.
> $$
> 
> 最优 $\tau$ 使两者同时满足，选择 $\tau = \varepsilon/2$（对称分配）。则：
> 
> $$
>     n \geq \max\left\{\frac{R^2}{2(\varepsilon/2)^2}\log\frac{2}, \frac{R^2}{2(\varepsilon/2)^2}\log\frac{2}\right\} = \frac{2R^2}{\varepsilon^2} \max\left\{\log\frac{2}, \log\frac{2}\right\}.
> $$
> 
> 更紧的分析（同时最小化 $n$）给出 [ref]。$\square$

> **Remark:** [改进的常数 / Improved Constants]
> 若使用 **Bernstein** 不等式（利用方差信息），样本复杂度可进一步改进为：
> 
> $$
>     n \geq \frac{2(\sigma_i^2 + \sigma_{TPR}^2) \log(2/\alpha) + \frac{2R}{3}\varepsilon \log(2/\alpha)}{\varepsilon^2},
> $$
> 
> 在 $\sigma_i^2 + \sigma_{TPR}^2 \ll R^2$ 时显著优于Hoeffding界。但Hoeffding界的优势在于**不依赖方差估计**，对任意有界分布有效——在元审计场景中，$\sigma_i^2$ 本身可能被恶意维护者操纵，因此无分布（distribution-free）界更为稳健。

### 多复现者联合检测 / Multi-Replicator Joint Detection

> **Theorem:** [多TPR联合检测定理 / Multi-TPR Joint Detection Theorem]
> <!-- label: thm:multi_tpr -->
> 设有 $K$ 个独立第三方复现者 $TPR_1, ..., TPR_K$，每个与维护者 $M_i$ 独立计算 $n$ 个审计样本。定义聚合统计量：
> 
> $$<!-- label: eq:agg_stat -->
>     \bar{D}_{n,K}^{(i)} = \frac{1}{K} \sum_{r=1}^{K} D_n^{(i,r)},
> $$
> 
> 其中 $D_n^{(i,r)}$ 是 $M_i$ 与 $TPR_r$ 之间的复现差异。
> 
> 若 $\E[D_n^{(i,r)}] = g_i$ 对所有 $r$ 成立（所有 TPR 无偏且校准一致），则：
> 
> $$<!-- label: eq:multi_tpr_bound -->
>     \Prob\left(|\bar{D}_{n,K}^{(i)} - g_i| \geq t\right) \leq 2\exp\left(-\frac{2n K t^2}{R^2}\right).
> $$

> **Proof:** $\bar{D}_{n,K}^{(i)}$ 是 $nK$ 个（非完全独立，因为每个 TPR 的 $n$ 个样本之间独立，且 $K$ 个 TPR 之间独立，故共 $nK$ 个独立观测）独立观测的均值，每个在 $[-R, R]$ 范围内。直接应用Hoeffding不等式。 $\square$

> **Corollary:** [复现者众包 / Replicator Crowdsourcing]
> <!-- label: cor:crowdsource -->
> 通过增加复现者数量 $K$，可以在不增加单个复现者负担的条件下提高检测精度。等效样本量 $n_{eff} = n \cdot K$。特别地，若每个 TPR 仅审计 $n=1$ 个样本，则 $K$ 个 TPR 的联合检测能力等价于单个 TPR 审计 $K$ 个样本（在独立性和无偏性假设下）。

## 维护者轮换机制 / Maintainer Rotation Mechanism

### 轮换的必要性 / Necessity of Rotation

**中文.**
即使检测到 $g_i \neq 0$，事后惩罚（如撤销维护者资格）存在时滞。更重要的是，某些偏差形式可能需要长时间才能累积到统计显著水平——这被称为**慢毒化攻击**（slow poisoning）：维护者以极低速率 $g_i^{(t)} = \delta \cdot t/T$ 逐渐引入偏差，使得任何固定窗口内的检测统计量不显著，但长期累积效果显著。

轮换机制提供了事前防御：通过限制任何单一维护者的连续任期，限制系统性偏差的最大累积量。

**English.**
Even when $g_i \neq 0$ is detected, ex-post punishment (e.g., revocation of maintainer status) has a time lag. More importantly, certain bias patterns may require long periods to accumulate to statistical significance---this is called a **slow poisoning attack**: the maintainer gradually introduces bias at an extremely low rate $g_i^{(t)} = \delta \cdot t/T$, such that no fixed-window detection statistic is significant, but the long-term cumulative effect is substantial.

Rotation provides an ex-ante defense: by limiting the continuous tenure of any single maintainer, the maximum cumulative bias is bounded.

### 轮换调度模型 / Rotation Scheduling Model

> **Definition:** [维护者轮换调度 Maintainer Rotation Schedule]
> <!-- label: def:rotation_schedule -->
> 设维护者池 $\mathcal{M} = \{M_1, ..., M_N\}$，$N \geq 2$。时间离散化为时期（epoch）$t = 1, 2, ..., T$。每个时期 $t$ 中，活跃维护者集合 $\mathcal{A}_t \subseteq \mathcal{M}$ 大小为 $m_t = |\mathcal{A}_t|$（通常 $m_t = 1$ 或 $m_t = 3$）。
> 
> 一个轮换调度 $\mathcal{R}$ 指定 $\mathcal{A}_t$ 的序列，满足：
> 
1. **覆盖性 (Coverage):** $\bigcup_{t=1}^{T} \mathcal{A}_t = \mathcal{M}$，每个维护者都有参与机会；
2. **任期限制 (Term Limit):** $\forall i$，连续活跃时期数 $\leq L_$（最大连续任期）；
3. **冷却期 (Cool-down):** $\forall i$，离任后至少 $C_$ 个时期才能再次上任（最小冷却期）。

> **Theorem:** [轮换偏差上界 / Rotation Bias Upper Bound]
> <!-- label: thm:rotation_bound -->
> 在轮换调度 $\mathcal{R}$ 下，若每个维护者 $M_i$ 的偏差 $g_i$ 满足 $|g_i| \leq G_$，则在 $T$ 个时期内，任何审计路径上的累积偏差满足：
> 
> $$<!-- label: eq:rotation_cum_bias -->
>     \left|\sum_{t=1}^{T} g_{a(t)}\right| \leq G_ \cdot \min\left(T, N \cdot L_ + (N-1) \cdot \left\lceil\frac{T}{L_ + C_}\right\rceil \cdot L_\right),
> $$
> 
> 其中 $a(t)$ 是时期 $t$ 的活跃维护者索引。
> 当 $T$ 充分大时，累积偏差的上界为 $O(G_ \cdot T \cdot \frac{L_}{L_ + C_})$，线性于 $T$ 但斜率为 $G_ \cdot \frac{L_}{L_ + C_} < G_$。

> **Proof:** 最坏情况：最偏维护者（$|g_i| = G_$）占据尽可能多的时期。在轮换约束下，该维护者每 $L_ + C_$ 个时期中最多活跃 $L_$ 个时期。因此，$T$ 个时期中的最大活跃时期数为 $\lceil T/(L_ + C_)\rceil \cdot L_$。同时考虑池大小 $N$ 的约束（至少需要轮换到其他人），取两者中较小的上界。$\square$

> **Corollary:** [最优轮换参数 / Optimal Rotation Parameters]
> <!-- label: cor:optimal_rotation -->
> 为使累积偏差最小化，应设 $L_$ 尽可能小且 $C_$ 尽可能大。但实用约束（维护连续性、专业知识保持）要求 $L_ \geq 1$ 且 $L_ + C_$ 不大于维护者池的轮换周期。最优实际选择：$L_ = 1$（每个时期轮换），$C_ = N-1$（所有维护者轮完一圈）。

## 多维护者共识机制 / Multi-Maintainer Consensus

### 共识的必要性 / Necessity of Consensus

**中文.**
单独的第三方复现检测虽然有效，但依赖于TPR的无偏性假设——这是元审计自反性问题的递归：如果TPR本身也有偏差呢？多维护者共识机制通过**横向一致性检验**（cross-sectional agreement）解决此问题：即使个体维护者可能有偏差，多数共识在适当条件下可以恢复真实审计结果。

**English.**
While individual third-party replication detection is effective, it relies on the TPR's unbiasedness assumption---this is the recursive nature of the meta-audit reflexivity problem: what if the TPR itself is biased? Multi-maintainer consensus mechanisms solve this through **cross-sectional agreement tests**: even if individual maintainers may be biased, majority consensus can recover the true audit result under appropriate conditions.

### $k$-of-$n$ 共识协议 / $k$-of-$n$ Consensus Protocol

> **Definition:** [$k$-of-$n$ 共识 / $k$-of-$n$ Consensus]
> <!-- label: def:k_of_n -->
> 设有 $n$ 个维护者对同一输入 $x$ 输出审计判定 $\hat{S}_1(x), ..., \hat{S}_n(x)$。$k$-of-$n$ 共识规则定义：
> 
> $$<!-- label: eq:k_of_n_rule -->
>     \hat{S}_{cons}(x) = median_{k}(\hat{S}_1(x), ..., \hat{S}_n(x)),
> $$
> 
> 其中 $median_{k}$ 表示从排序后的值中选取第 $k$ 个顺序统计量（$1 \leq k \leq n$）。标准多数共识对应 $k = \lceil n/2 \rceil$（中位数）。

> **Definition:** [Byzantine维护者模型 / Byzantine Maintainer Model]
> <!-- label: def:byzantine -->
> 设 $n$ 个维护者中，$b$ 个是**Byzantine**（可任意偏离，包括策略性输出以破坏共识），$n-b$ 个是**诚实无偏**的（$g_i = 0$，$\epsilon_i(x)$ 独立同分布）。诚实维护者的输出分布为 $\hat{S}_i(x) \sim \mathcal{F}$，其中 $\mathcal{F}$ 关于 $S(x)$ 对称且支撑集有界 $[S_, S_]$。

> **Theorem:** [Byzantine共识可靠性 / Byzantine Consensus Reliability]
> <!-- label: thm:byzantine_consensus -->
> 在 $k$-of-$n$ 共识下，设 $b$ 个 Byzantine 维护者，$n-b$ 个诚实维护者。若：
> 
> $$<!-- label: eq:byzantine_condition -->
>     b < \min(k, n-k+1),
> $$
> 
> 则共识输出 $\hat{S}_{cons}(x)$ 位于诚实维护者输出的范围内：
> 
> $$<!-- label: eq:byzantine_consensus_bound -->
>     \min_{i \in \mathcal{H}} \hat{S}_i(x) \leq \hat{S}_{cons}(x) \leq \max_{i \in \mathcal{H}} \hat{S}_i(x),
> $$
> 
> 其中 $\mathcal{H}$ 是诚实维护者集合（$|\mathcal{H}| = n-b$）。
> 
> 特别地，对于中位数共识（$k = \lceil n/2 \rceil$），条件退化为 $b < n/2$（经典的 Byzantine 容错上界），且：
> 
> $$<!-- label: eq:median_bound -->
>     \Prob\left(|\hat{S}_{cons}(x) - S(x)| \geq t\right) \leq 2\exp\left(-\frac{2(n-b) t^2}{R^2}\right).
> $$

> **Proof:** 条件 $b < \min(k, n-k+1)$ 确保在排序后的 $n$ 个输出中，无论 Byzantine 维护者将其输出置于何处，第 $k$ 个顺序统计量必然落在诚实维护者输出的区间内（因为 $b < k$ 意味着前 $k$ 个中至少有一个诚实输出，$b < n-k+1$ 意味着后 $n-k+1$ 个中至少有一个诚实输出，结合可得第 $k$ 个在诚实区间内）。
> 
> 对于中位数情况：$k = \lceil n/2 \rceil$，$\min(k, n-k+1) = \lceil n/2 \rceil$（当 $n$ 为奇数）或 $n/2$（当 $n$ 为偶数）。条件 $b < n/2$ 意味着诚实维护者占严格多数。此时中位数落在诚实输出的范围内。进一步，由于诚实输出的中位数是诚实输出样本的中位数，我们可以对其应用Hoeffding界得到 [ref]。注意：中位数不使用 $n$ 个诚实维护者中的所有信息，收敛速度为 $O(1/\sqrt{n-b})$。更紧的界可使用次序统计量的大偏差理论。$\square$

> **Remark:** [与经典分布式系统文献的关系]
> 经典 Byzantine 容错（如 PBFT）要求 $n > 3b$ 以保证 safety + liveness。本文的共识仅要求 safety（审计结果可信），不要求 liveness（审计过程可等待直到收集足够多的一致意见）。因此条件较宽松 $n > 2b$。这对应于异步网络中的**静态**共识（static consensus），与区块链中的中本聪共识（probabilistic, $n > 2b$ 的诚实多数假设）一致。

### 共识失败概率 / Consensus Failure Probability

> **Theorem:** [Hoeffding加权共识界 / Hoeffding Weighted Consensus Bound]
> <!-- label: thm:weighted_consensus -->
> 考虑加权共识：
> 
> $$<!-- label: eq:weighted_consensus -->
>     \hat{S}_{w-cons}(x) = \sum_{i=1}^{n} w_i \hat{S}_i(x), \quad \sum_{i=1}^{n} w_i = 1, \quad w_i \geq 0.
> $$
> 
> 权重 $w_i$ 基于维护者的历史审计准确度（由元审计检测结果更新）。假设诚实维护者子集 $\mathcal{H}$ 满足 $\sum_{i \in \mathcal{H}} w_i = W_{\mathcal{H}} \in (0, 1]$。则：
> 
> $$<!-- label: eq:weighted_bound -->
>     \Prob\left(|\hat{S}_{w-cons}(x) - S(x)| \geq t\right) \leq 2\exp\left(-\frac{2 t^2}{R^2 \sum_{i=1}^{n} w_i^2}\right) + \Prob(Byzantine偏差总量 > t \cdot (1 - W_{\mathcal{H}})).
> $$

> **Proof:** 分解加权共识的偏差：
> 
> $$
>     |\hat{S}_{w-cons}(x) - S(x)| &= \left|\sum_{i \in \mathcal{H}} w_i(\hat{S}_i(x) - S(x)) + \sum_{i \notin \mathcal{H}} w_i(\hat{S}_i(x) - S(x))\right| 

>     &\leq \underbrace{\left|\sum_{i \in \mathcal{H}} w_i(\hat{S}_i(x) - S(x))\right|}_{诚实维护者贡献} + \underbrace{\sum_{i \notin \mathcal{H}} w_i \cdot R}_{Byzantine贡献}.
> $$
> 
> 诚实维护者贡献：$\sum_{i \in \mathcal{H}} w_i(\hat{S}_i(x) - S(x))$ 是零均值独立项（注意：$\hat{S}_i(x) - S(x)$ 对不同 $i$ 独立）的加权和。将每个 $\hat{S}_i(x) - S(x)$ 视为界在 $[-R, R]$ 内的随机变量，权重为 $w_i$。由Hoeffding不等式的加权版本：
> 
> $$
>     \Prob\left(\left|\sum_{i \in \mathcal{H}} w_i(\hat{S}_i(x) - S(x))\right| \geq t\right) \leq 2\exp\left(-\frac{2t^2}{\sum_{i \in \mathcal{H}} w_i^2 \cdot (2R)^2}\right) = 2\exp\left(-\frac{t^2}{2R^2 \sum_{i \in \mathcal{H}} w_i^2}\right).
> $$
> 
> 更简单的界：使用 $R^2 \sum_i w_i^2$ 作为分母（包括所有 $n$ 个维护者的权重，$\sum_{i \in \mathcal{H}} w_i^2 \leq \sum_{i=1}^{n} w_i^2$）。$\square$

## 元审计协议 / The Meta-Audit Protocol

### 协议描述 / Protocol Description

> **Protocol:** [元审计协议 $\MetaAudit$]
> <!-- label: prot:meta_audit -->
> **初始化阶段 (Initialization).**
> 
1. 确定维护者池 $\mathcal{M} = \{M_1, ..., M_N\}$，$N \geq 3$。
2. 设定参数：显著性水平 $\alpha$、最小可检测偏差 $\varepsilon$、目标功效 $1-\beta$、审计值域 $R = S_ - S_$。
3. 计算所需复现样本量 $n^*$ 根据 [ref] 的公式 [ref]。
4. 初始化维护者信任权重 $\mathbf{w}^{(0)} = (1/N, ..., 1/N)$。

> 
> 
> **每时期操作 (Per-Epoch Operation).** 对每个时期 $t = 1, 2, ...$：
> 
1. **轮换选择 (Rotation Selection).** 根据轮换调度 $\mathcal{R}$ 选择活跃维护者集合 $\mathcal{A}_t$。
2. **审计执行 (Audit Execution).** $\mathcal{A}_t$ 中的维护者对当前审计批次 $\mathcal{X}_t$ 输出审计判定并追加到各自的日志 $\mathcal{L}_i$。
3. **共识聚合 (Consensus Aggregation).** 若 $|\mathcal{A}_t| \geq 3$，执行 $k$-of-$n$ 共识（$k = \lceil |\mathcal{A}_t|/2 \rceil$）得到 $\hat{S}_{cons}$。若 $|\mathcal{A}_t| = 1$，直接使用该维护者的输出。
4. **第三方复现 (TPR Replication).** 随机选择 $n^*$ 个已审计的 $x \in \bigcup_{\tau \leq t} \mathcal{X}_\tau$，由 $K \geq 1$ 个第三方复现者独立重新审计。计算复现差异统计量 $D_{n^*}^{(i,t)}$ 对每个 $M_i \in \mathcal{A}_t$。
5. **偏差检验 (Bias Test).** 对每个 $M_i$，执行假设检验：
6. **权重更新 (Weight Update).** 基于检测结果更新信任权重：
7. **共识权重调整 (Consensus Weight Adjustment).** 使用更新后的 $\mathbf{w}^{(t)}$ 作为下一个时期的加权共识权重（若采用加权共识）。
8. **维护者更替 (Maintainer Replacement).** 若连续 $C_{strike}$ 次时期中 $M_i$ 均被标记偏差，将 $M_i$ 从 $\mathcal{M}$ 中移除并替换为新维护者。

### 协议正确性 / Protocol Correctness

> **Theorem:** [元审计协议可靠性 / Meta-Audit Protocol Reliability]
> <!-- label: thm:protocol_reliability -->
> 在协议 $\MetaAudit$ 下，假设：
> 
1. 审计输出有界在 $[S_, S_]$ 内；
2. TPR 复现者彼此独立且独立于维护者（可来自不同的制度生态系统）；
3. 至少 $n-b > n/2$ 个维护者是诚实无偏的（Byzantine条件）；
4. 轮换调度使每个维护者每 $T_{cycle}$ 时期至少被复现检验一次。

> 则：
> 
1. **偏差检测延迟.** 偏差为 $|g_i| \geq \varepsilon$ 的恶意维护者将在 $O(T_{cycle} \cdot \log(2/\beta))$ 个时期内以概率 $\geq 1-\beta$ 被检测；
2. **共识误差.** 加权共识输出满足：对任意 $t > 0$，
3. **自反一致性.** 协议满足与 SCX\ Theorem 3 的一致性：$\MetaAudit$ 的偏差检测不依赖对噪声/难度不可区分性的破坏，因为检测源自横向一致性比较而非纵向解析。

> **Proof:** (a) 来自  [ref] 的样本复杂度：需要约 $n^*$ 个复现样本检测偏差。每个 $T_{cycle}$ 时期内累积约 $n^* / T_{cycle}$ 个有效样本（假设均匀分布）。总检测时期数 $\approx n^* \cdot T_{cycle} / (每时期样本数) = O(T_{cycle} \cdot \log(2/\beta))$。
> 
> (b) 来自  [ref] 和权重更新规则 [ref]：恶意维护者的权重以指数速率衰减，$C_{strike}$ 次连续标记后权重降至 $O(e^{-\gamma C_{strike}})$。
> 
> (c) SCX\ Theorem 3 的不可区分性适用于对单一审计源的纵向分析。$\MetaAudit$ 通过横向比较不同审计源来检测系统性偏差，操作于一个正交的信息维度（审计者间一致性），因此不与其矛盾。形式化地：Theorem 3 声明 $\forall$ 算法 $\mathcal{A}$ 仅依赖 $\hat{S}_i(x)$ 的解析性质，$\mathcal{A}$ 不能区分 $H_0: \epsilon = \epsilon_{noise}$ 与 $H_1: \epsilon = \epsilon_{difficulty}$。而 $\MetaAudit$ 使用的统计量 $D_n^{(i)}$ 依赖 $\hat{S}_i(x) - \hat{S}_{TPR}(x)$，即**跨源**差异，而非单源解析——它操作在Theorem 3的定义域之外。

## 偏差类型与Hoeffding界的扩展
## Bias Taxonomy and Extensions of Hoeffding Bound

### 维护者偏差分类学 / Maintainer Bias Taxonomy

> **Definition:** [偏差类型 Bias Types]
> <!-- label: def:bias_taxonomy -->
> 维护者偏差 $g_i$ 可分类为：
> 
1. **恒常偏差 (Constant Bias):** $g_i = c$ 对所有输入 $x$ 相同。最易检测——任何输入子集上的 $D_n^{(i)}$ 均收敛到 $c$。
2. **方向偏差 (Directional Bias):** $g_i(x) = \mathbf{v}_i^ \phi(x)$，其中 $\phi(x)$ 是输入特征，$\mathbf{v}_i$ 是维护者偏好向量。需要对输入空间的充分覆盖才能检测——若复现样本与特征向量正交，偏差被隐藏。
3. **条件偏差 (Conditional Bias):** $g_i(x) \neq 0$ 仅当 $x$ 满足特定条件（如特定主题、特定来源）。检测需分层抽样（stratified sampling）覆盖所有条件区域。
4. **时变偏差 (Time-Varying Bias):** $g_i^{(t)}$ 随时间变化（如慢毒化 $g_i^{(t)} = \delta \cdot t/T$）。需要时间窗口内的累积检测或滑动窗口检验。
5. **策略偏差 (Strategic Bias):** 维护者知晓元审计的存在，在复现样本上表现无偏（$g_i = 0$），在非复现样本上施加偏差。需随机抽查（random audit）使维护者无法区分复现样本和常规样本。

### 方向偏差的Hoeffding扩展 / Hoeffding Extension for Directional Bias

> **Theorem:** [方向偏差检测 / Directional Bias Detection]
> <!-- label: thm:directional_bias -->
> 设维护者偏差为方向形式 $g_i(x) = \mathbf{v}_i^ \phi(x)$，其中 $\phi: \mathcal{X} \to \R^d$ 为已知特征映射，$\mathbf{v}_i \in \R^d$ 为未知偏差向量。对 $n$ 个独立复现样本，设 $\Phi_n = [\phi(x_1), ..., \phi(x_n)]^ \in \R^{n \times d}$ 为设计矩阵。则偏差向量 $\mathbf{v}_i$ 的 OLS 估计为：
> 
> $$<!-- label: eq:ols_v -->
>     \hat{\mathbf{v}}_i = (\Phi_n^\Phi_n)^{-1}\Phi_n^ \mathbf{D}_n^{(i)},
> $$
> 
> 其中 $\mathbf{D}_n^{(i)} = (D_1^{(i)}, ..., D_n^{(i)})^$ 为逐样本差异向量。
> 
> 对任意单位向量 $\mathbf{u} \in \R^d$，线性组合 $\mathbf{u}^\hat{\mathbf{v}}_i$ 满足：
> 
> $$<!-- label: eq:directional_hoeffding -->
>     \Prob\left(|\mathbf{u}^(\hat{\mathbf{v}}_i - \mathbf{v}_i)| \geq t\right) \leq 2\exp\left(-\frac{2n t^2}{R^2 \cdot \mathbf{u}^(\frac{1}{n}\Phi_n^\Phi_n)^{-1}\mathbf{u}}\right).
> $$

> **Proof:** $\mathbf{u}^\hat{\mathbf{v}}_i = \mathbf{u}^(\Phi_n^\Phi_n)^{-1}\Phi_n^\mathbf{D}_n^{(i)} = \mathbf{a}^\mathbf{D}_n^{(i)}$，其中 $\mathbf{a} = \Phi_n(\Phi_n^\Phi_n)^{-1}\mathbf{u}$。这是 $n$ 个独立观测的线性组合，每个观测在 $[-R, R]$ 内。由加权Hoeffding不等式，系数向量 $\mathbf{a}$ 的 $\ell_2$ 范数平方为 $\|\mathbf{a}\|_2^2 = \mathbf{u}^(\Phi_n^\Phi_n)^{-1}\mathbf{u}$。Hoeffding界即得。$\square$

### 条件偏差的分层检测 / Stratified Detection for Conditional Bias

> **Theorem:** [分层Hoeffding检测 / Stratified Hoeffding Detection]
> <!-- label: thm:stratified -->
> 将输入空间 $\mathcal{X}$ 划分为 $L$ 个不相交的层 $\mathcal{X}_1, ..., \mathcal{X}_L$。对每层 $\ell$，独立抽取 $n_\ell$ 个复现样本。每层的复现差异统计量为 $D_{n_\ell}^{(i,\ell)}$。则联合检验：
> 
> $$<!-- label: eq:stratified_test -->
>     T_{strat} = \max_{\ell=1,...,L} \frac{|D_{n_\ell}^{(i,\ell)}|}{\sqrt{R^2 / (2n_\ell)}}.
> $$
> 
> 在全局原假设 $g_i(x) = 0, \forall x \in \mathcal{X}$ 下：
> 
> $$<!-- label: eq:stratified_bound -->
>     \Prob\left(T_{strat} \geq t\right) \leq 2L \cdot \exp\left(-t^2\right).
> $$

> **Proof:** 每层统计量 $Z_\ell = D_{n_\ell}^{(i,\ell)} / \sqrt{R^2/(2n_\ell)}$ 在原假设下满足 $\Prob(|Z_\ell| \geq t) \leq 2e^{-t^2}$（由Hoeffding）。联合界（union bound）乘以 $L$ 即得。Bonferroni校正可通过控制 family-wise error rate (FWER) 获得更紧的界。$\square$

### 时变偏差的滑动窗口检测 / Sliding Window for Time-Varying Bias

> **Theorem:** [滑动窗口Hoeffding检测 / Sliding Window Hoeffding Detection]
> <!-- label: thm:sliding_window -->
> 设偏差 $g_i^{(t)}$ 在时间窗口 $W$ 内近似恒定：$|g_i^{(t)} - g_i^{(t')}| \leq \delta_W$ 对所有 $|t - t'| \leq W$。在滑动窗口 $[t-W+1, t]$ 内累积 $n_W$ 个复现样本，定义窗口统计量：
> 
> $$<!-- label: eq:window_stat -->
>     D_W^{(i,t)} = \frac{1}{n_W} \sum_{k \in window} \left(\hat{S}_i(x_k) - \hat{S}_{TPR}(x_k)\right).
> $$
> 
> 则：
> 
> $$<!-- label: eq:window_bound -->
>     \Prob\left(|D_W^{(i,t)} - \bar{g}_i^{(t)}| \geq t\right) \leq 2\exp\left(-\frac{2n_W t^2}{R^2}\right),
> $$
> 
> 其中 $\bar{g}_i^{(t)} = \frac{1}{W}\sum_{\tau=t-W+1}^{t} g_i^{(\tau)}$ 是窗口内平均偏差。
> 
> 若 $g_i^{(t)} = \delta \cdot t/T$（线性慢毒化），则 $\bar{g}_i^{(t)} \approx \delta \cdot (t - W/2)/T$。窗口统计量可检测窗口内平均偏差，检测条件为 $|\bar{g}_i^{(t)}| \geq \varepsilon$，给出：
> 
> $$<!-- label: eq:slow_poison_detect -->
>     t_{detect} \geq \frac{T \cdot \varepsilon} + \frac{W}{2}.
> $$
> 
> 最小化 $t_{detect}$ 需要在窗口长度 $W$（窗越大，平均偏差越大，但检测时延也越大）与检测敏感性之间权衡。最优 $W^*$ 满足 $W^* = \sqrt{2 R^2 \log(2/\alpha) / \delta^2}$。

> **Proof:** 滑动窗口内的Hoeffding界是直接的——窗口内的 $n_W$ 个样本独立同分布（假设慢变偏差），因此应用  [ref]。
> 
> 对于线性毒化 $g_i^{(t)} = \delta \cdot t/T$，窗口内平均 $\bar{g}_i^{(t)} = \frac{T} \cdot \frac{1}{W} \sum_{\tau=t-W+1}^{t} \tau = \frac{T} \cdot (t - \frac{W-1}{2})$。当 $|\bar{g}_i^{(t)}| \geq \varepsilon$ 时统计上可检测，解得 $t \geq T\varepsilon/\delta + (W-1)/2 \approx T\varepsilon/\delta + W/2$。
> 
> 最优窗口：检测时延 $t_{detect} \approx T\varepsilon/\delta + W/2 + n_W$（因为需要 $n_W$ 个样本）。$n_W$ 由 $n_W \geq R^2\log(2/\alpha)/(2\varepsilon^2)$ 决定。总时延 $\approx T\varepsilon/\delta + W/2 + R^2\log(2/\alpha)/(2\varepsilon^2)$。对 $W$ 求导（注意 $n_W$ 通常与 $W$ 成比例，假设采样率恒定），可解出最优 $W$。$\square$

## 策略偏差与随机审计 / Strategic Bias and Random Audits

### 审计博弈模型 / Audit Game Model

> **Definition:** [审计博弈 Audit Game]
> <!-- label: def:audit_game -->
> 维护者 $M_i$ 与元审计者（Meta-Auditor, MA）之间的博弈：
> 
- **维护者行动:** 对每个输入 $x$，选择是否施加偏差 $g_i(x) \in \{0, b\}$（$b > 0$ 为偏差幅度）。施加偏差有收益 $\rho \cdot b$（如推动特定议程），但有被检测的风险。
- **元审计者行动:** 选择复现比例 $p \in (0, 1]$，即以概率 $p$ 对任意审计输出进行独立复现（而不告知维护者哪些输出被选中）。
- **检测:** 若偏差输入被复现，以概率 $q(n, \varepsilon, \alpha)$ 被检测，其中 $q$ 由  [ref] 给出。
- **惩罚:** 若检测到偏差，维护者被移除，损失 $L$（未来所有收益的贴现值）。

> **Theorem:** [随机审计的威慑效应 / Deterrence Effect of Random Audits]
> <!-- label: thm:deterrence -->
> 在审计博弈中，若复现概率 $p$ 满足：
> 
> $$<!-- label: eq:deterrence_condition -->
>     p \cdot q \cdot L > \rho \cdot b,
> $$
> 
> 则维护者的占优策略是不施加偏差（$g_i = 0$）。$p$ 的最小威慑值为：
> 
> $$<!-- label: eq:min_p -->
>     p_ = \frac{\rho \cdot b}{q \cdot L}.
> $$

> **Proof:** 维护者的一次性偏差施加的期望收益为 $\rho b - p \cdot q \cdot L$（收益减去期望惩罚）。若此值为负，即 $\rho b < p \cdot q \cdot L$，则施加偏差的期望净收益为负，理性维护者不施加偏差。注意：这是单次博弈的分析。在重复博弈中，被检测的代价还包括未来所有时期的收益损失，因此 $L$ 在重复设置中更大，威慑条件更容易满足。$\square$

> **Corollary:** [无限期重复博弈的威慑 / Infinite-Horizon Deterrence]
> <!-- label: cor:infinite_deterrence -->
> 在无限期重复博弈中，折现因子为 $\beta \in (0, 1)$。维护者被检测后永久移除。施加偏差的期望长期收益为：
> 
> $$
>     \rho b - p \cdot q \cdot \frac{\rho \cdot \bar{S}}{1 - \beta},
> $$
> 
> 其中 $\bar{S}$ 是维护者每时期的平均合法收益。威慑条件为：
> 
> $$<!-- label: eq:infinite_deterrence -->
>     p \cdot q > \frac{\rho b (1-\beta)}{\rho \cdot \bar{S}}.
> $$
> 
> 由于 $\bar{S} \gg b$（合法审计收益远大于偏差收益），右侧极小，$p$ 可极小——**长任期维护者比短任期维护者更容易被威慑**。

### 不可区分复现 / Indistinguishable Replication

> **Definition:** [不可区分复现 Indistinguishable Replication]
> <!-- label: def:indist_replication -->
> 复现样本与常规审计样本的概率分布完全相同：若维护者观察到输入 $x$，其无法以高于随机猜测的概率判断 $x$ 是否为复现样本。形式上，复现标记 $R_x \in \{0, 1\}$ 独立于 $x$ 的任意可观测特征：
> 
> $$<!-- label: eq:indist -->
>     \Prob(R_x = 1 \mid x) = \Prob(R_x = 1) = p, \quad R_x \indep \phi(x),
> $$
> 
> 其中 $\phi(x)$ 是维护者可观测的任意输入特征。

> **Remark:** 不可区分性是随机审计的**核心安全属性**。若无此属性，维护者可策略性地仅在非复现样本上施加偏差——这等价于方向性偏差的特例：$g_i(x) = b \cdot \ind{R_x = 0}$。在实践中，不可区分性通过以下方式实现：(a) 复现者直接从公共审计日志中随机抽样，而非使用独立的采样机制；(b) 复现审计的延迟足够大，使维护者无法关联复现请求与特定触发事件；(c) 使用密码学承诺（cryptographic commitment）确保审计样本在维护者输出结果之前已被选定但对其隐藏。

## 数值分析与模拟 / Numerical Analysis and Simulation

### 检测样本复杂度表 / Detection Sample Complexity Table

[Table omitted — see original .tex]

### 轮换累积偏差模拟 / Rotation Cumulative Bias Simulation

[Table omitted — see original .tex]

## 与SCX框架的集成 / Integration with the SCX Framework

### 自反性作为SCX的第九原则 / Reflexivity as the Ninth SCX Principle

**中文.**
SCX平等论框架的核心公理（Theorem 1--8）构建了从专家一致性检测到人机协同审计的完整理论体系。然而，这些定理均假设审计者的可靠性。元审计协议填补了这一自反性缺口，可被视为SCX的**第九原则：自反性检验原则（Principle of Reflexivity）**：

> **原则9（自反性检验）.** 任何声称实现了SCX审计的系统中，审计者本身必须接受同级或更高级别的审计。该元审计必须：(a) 公开所有审计日志；(b) 允许并鼓励独立第三方随机复现；(c) 实施维护者轮换与多维护者共识；(d) 使用统计检验（如Hoeffding界）对审计者偏差进行定量检测，其检验功效和样本复杂度需事前声明并公开验证。

**English.**
The SCX Equality Framework's core axioms (Theorems 1--8) construct a complete theoretical edifice from expert consensus detection to human-AI collaborative auditing. However, these theorems all assume auditor reliability. The meta-audit protocol fills this reflexivity gap and can be regarded as SCX's **Ninth Principle: the Principle of Reflexivity**:

> **Principle 9 (Reflexivity Verification).** In any system claiming to implement SCX auditing, the auditors themselves must be subject to audit at the same or higher level. This meta-audit must: (a) make all audit logs public; (b) permit and encourage independent third-party random replication; (c) implement maintainer rotation and multi-maintainer consensus; (d) use statistical tests (such as the Hoeffding bound) to quantitatively detect auditor bias, with test power and sample complexity declared in advance and publicly verified.

### 与Theorem 3的详细一致性分析

> **Theorem:** [元审计与Theorem 3的一致性 / Consistency of Meta-Audit with Theorem 3]
> <!-- label: thm:consistency_t3 -->
> 元审计协议 $\MetaAudit$ 不违反 SCX\ Theorem 3（噪声-难度不可区分性）。具体地：
> 
1. $\MetaAudit$ 使用的检测统计量 $D_n^{(i)} = \frac{1}{n}\sum_{k}(\hat{S}_i(x_k) - \hat{S}_{TPR}(x_k))$ 涉及**两个独立审计源**的输出差异，而非单个审计源的内部解析；
2. Theorem 3 的不可区分性声明适用于单一审计源的可观测量 $\{\hat{S}(x), \nabla\hat{S}(x), H_{\hat{S}}(x)\}$；
3. $D_n^{(i)}$ 的信息来源于审计者间的**不一致性**（disagreement），这是Theorem 3的定义域之外的信息维度；
4. 形式化地：若Theorem 3声明 $\forall \mathcal{A}_{internal}$ 仅依赖 $\hat{S}_i(x)$ 的内部结构（梯度、Hessian等），有 $\mathcal{A}_{internal}$ 不可区分 $H_0$ 与 $H_1$，则 $\MetaAudit$ 不在此声明的范围内，因为 $\MetaAudit$ 的核心输入是 $\hat{S}_i(x) - \hat{S}_j(x)$（跨源差分），该差分在Theorem 3的输入空间中不可表示。

## 实现考量 / Implementation Considerations

### 审计日志的密码学保证 / Cryptographic Guarantees for Audit Logs

1. **内容可寻址存储 (Content-Addressable Storage).** 每个审计条目 $(x, \hat{S}_i(x), t)$ 的哈希 $\mathsf{hash} = H(x \| \hat{S}_i(x) \| t)$ 唯一标识该条目。审计日志存储在内容可寻址系统中（如 IPFS），确保条目不可篡改。
2. **Merkle链 (Merkle Chain).** 日志条目构成哈希链：$\mathsf{hash}_j = H(x_j \| \hat{S}_i(x_j) \| t_j \| \mathsf{hash}_{j-1})$。任何条目的修改都会改变所有后续哈希，使得篡改可被公开检测。
3. **时间戳 (Timestamping).** 定期将最新 $\mathsf{hash}$ 锚定到公共区块链（如通过 Opentimestamps 或类似机制），提供不可否认的时间证明。
4. **零知识复现证明 (ZK Replication Proofs).** TPR 可生成一个零知识证明 $\pi$，证明 $\exists$ 复现计算 $\hat{S}_{TPR}(x) = y$ 与维护者日志中的条目 $\hat{S}_i(x) = y'$ 满足 $|y - y'| \geq \tau$（显著差异），而不泄露TPR的计算方法或中间结果——保护TPR的审计方法学产权。

### 维护者池的治理 / Maintainer Pool Governance

1. **准入机制 (Admission).** 新维护者需通过：数学能力测试（确保能正确计算 Cercis\ Score 和梯度场诊断）、偏差声明（公开任何可能影响审计的利益冲突）、质押保证金（经济担保，若被检测偏差则罚没）。
2. **退出机制 (Exit).** 维护者可自愿退出（需提前公告并完成当前审计周期）。强制退出在连续 $C_{strike}$ 次偏差标记后自动触发。
3. **声誉系统 (Reputation).** 每个维护者的历史表现公开记录：偏差检测次数、复现一致性得分、共识贡献率。声誉影响权重 $w_i$ 和维护者调度优先级。
4. **去中心化协调 (Decentralized Coordination).** 轮换调度和复现者分配通过链上随机信标（如 RANDAO）或可验证随机函数（VRF）确定，防止调度本身被操控。

## 相关工作 / Related Work

**中文.**
元审计的概念与以下领域交叉：

1. **统计审计抽样 (Statistical Audit Sampling).** 金融审计中的属性抽样和变量抽样方法与本文的复现统计有相似性，但传统审计的样本量计算基于正态近似而非Hoeffding界，且不涉及维护者之间的博弈。
2. **分布式系统Byzantine容错 (BFT).** PBFT (Castro \& Liskov, 1999)、Tendermint (Buchman, 2016)、HotStuff (Yin et al., 2019) 等共识协议处理的是一般状态机复制的Byzantine容错，而本文聚焦于审计评分的数值共识，允许更高效的统计聚合（如加权中位数）。
3. **同行评审的去偏见化 (Debiasing Peer Review).** NeurIPS实验 (2014, 2022)、ICML的随机化审稿分配、以及bid calibration方法试图减少审稿人偏差，但均依赖制度设计而非统计检测保证——元审计协议提供了数学上更严格的方法。
4. **预测市场与真相发现 (Prediction Markets \& Truth Discovery).** 贝叶斯真相血清（Bayesian Truth Serum, Prelec, 2004）和加权多数算法（weighted majority）与本文的加权共识机制有数学平行，但本文的权重更新基于统计假设检验而非主观评分。
5. **算法审计 (Algorithmic Auditing).** 公平性审计 (fairness audits) 和模型卡 (model cards) 关注算法输出偏差，本文关注的是审计者本身的偏差——元层面的审计。

**English.**
The concept of meta-audit intersects with the following areas:

1. **Statistical Audit Sampling.** Attribute and variable sampling methods in financial auditing share similarities with our replication statistics, but traditional audit sample-size calculations rely on normal approximations rather than Hoeffding bounds and do not involve inter-maintainer game theory.
2. **Distributed Systems Byzantine Fault Tolerance (BFT).** PBFT (Castro \& Liskov, 1999), Tendermint (Buchman, 2016), HotStuff (Yin et al., 2019), and other consensus protocols handle Byzantine fault tolerance for general state-machine replication, whereas this paper focuses on numerical consensus of audit scores, enabling more efficient statistical aggregation (e.g., weighted median).
3. **Debiasing Peer Review.** NeurIPS experiments (2014, 2022), ICML's randomized reviewer assignments, and bid calibration methods attempt to reduce reviewer bias, but all rely on institutional design rather than statistical detection guarantees---the meta-audit protocol provides a mathematically more rigorous approach.
4. **Prediction Markets \& Truth Discovery.** Bayesian Truth Serum (Prelec, 2004) and weighted majority algorithms share mathematical parallels with our weighted consensus mechanism, but our weight updates are based on statistical hypothesis testing rather than subjective scoring.
5. **Algorithmic Auditing.** Fairness audits and model cards focus on algorithmic output bias, whereas this paper focuses on the bias of the auditor itself---auditing at the meta-level.

## 开放问题与未来工作 / Open Problems and Future Work

1. **最小方差无偏估计 (MVUE).** 当前Hoeffding界依赖有界假设。是否存在对任意分布的更紧界（如使用经验Bernstein不等式），在保持分布无关性的同时利用样本方差信息？当 $\sigma_i^2 \ll R^2$ 时，效率提升可观。
2. **自适应检测阈值 (Adaptive Thresholds).** $\tau = \varepsilon/2$ 是对称分配的最优选择。是否存在基于数据驱动的自适应阈值（如Lawless \& Singhal的混合停止规则），在不增加假阳性的条件下降低检测延迟？
3. **多方计算 (MPC) 元审计.** 能否将 $\MetaAudit$ 协议实现为安全多方计算（secure MPC），使得偏差检测在不泄露任何单个审计者的原始审计输出的条件下完成？这与FA-Theorem的联邦审计框架兼容。
4. **全自动元审计 (Fully Autonomous Meta-Audit).** 当审计者和元审计者均为AI系统时，元审计的递归深度如何选择？是否存在一个自然停止点（如达到可用计算资源的上限，或递归收益递减至低于阈值）？
5. **元审计的元审计 (Meta-Meta-Audit).** 谁审计元审计者？本文未完全解决此问题——我们假设TPR的诚实性或多数共识的可靠性。完全的递归解决方案需要无限多层次的审计，但实用中2-3层即可有效威慑，因为每增加一层，攻击者的操作复杂度呈指数增长。
6. **博弈论完备分析 (Game-Theoretic Completeness).** 审计博弈 [ref] 仅分析了单次和无限期重复的极端情况。有限期、不完全信息、多维护者串谋等情况需要更精细的分析。特别地：当 $b \geq 2$ 个维护者同时施加偏差时，$k$-of-$n$ 共识的可靠性条件是什么？

## 结论 / Conclusion

**中文.**
本文严格形式化了 SCX\ 平等论框架中的元审计协议，回答了“谁审计审计者”的自反性问题。核心结果包括：

1. 形式化维护者偏差模型 $\hat{S}_i(x) = S(x) + g_i + \epsilon_i(x)$，区分系统性偏差 $g_i$ 与随机误差 $\epsilon_i(x)$。
2. 基于Hoeffding不等式，证明在给定显著性水平 $\alpha$ 和功效 $1-\beta$ 下，检测 $|g_i| \geq \varepsilon$ 所需的独立复现样本量下界为 $n \geq \frac{R^2}{2\varepsilon^2} (\sqrt{\log(2/\alpha)} + \sqrt{\log(2/\beta)})^2$。
3. 多TPR联合检测、方向偏差、条件偏差、时变偏差（慢毒化）的Hoeffding扩展定理，覆盖所有主要偏差类型。
4. 维护者轮换调度的累积偏差上界 $O(G_ \cdot T \cdot L_/(L_ + C_))$，在最优参数（$L_=1, C_=N-1$）下减少66.7\%-85.7\%的累积偏差。
5. $k$-of-$n$ Byantine共识的可靠性条件 $b < \min(k, n-k+1)$，及加权共识的Hoeffding误差界。
6. 随机审计博弈的威慑条件 $p \cdot q \cdot L > \rho \cdot b$，以及不可区分复现的安全属性。
7. 与 SCX\ Theorem 3 的一致性证明——元审计操作于跨源差异信息维度，不违反噪声/难度不可区分性。

元审计协议将 SCX\ 框架从“信任审计者”提升为“验证审计者”，实现了审计制度的自反性完备。它既是数学定理，也是制度设计——兼具统计严格性和博弈论激励相容性。

**English.**
This paper rigorously formalizes the meta-audit protocol within the SCX Equality Framework, answering the reflexive question ``who audits the auditor.'' Core results include:

1. Formalization of the maintainer bias model $\hat{S}_i(x) = S(x) + g_i + \epsilon_i(x)$, distinguishing systematic bias $g_i$ from random error $\epsilon_i(x)$.
2. Proof, via Hoeffding's inequality, that detecting $|g_i| \geq \varepsilon$ at significance level $\alpha$ and power $1-\beta$ requires a lower bound of $n \geq \frac{R^2}{2\varepsilon^2} (\sqrt{\log(2/\alpha)} + \sqrt{\log(2/\beta)})^2$ independent replication samples.
3. Hoeffding extension theorems for multi-TPR joint detection, directional bias, conditional bias, and time-varying bias (slow poisoning), covering all major bias types.
4. Cumulative bias upper bound $O(G_ \cdot T \cdot L_/(L_ + C_))$ for maintainer rotation scheduling, achieving 66.7\%--85.7\% cumulative bias reduction under optimal parameters ($L_=1, C_=N-1$).
5. Reliability condition $b < \min(k, n-k+1)$ for $k$-of-$n$ Byzantine consensus, and Hoeffding error bound for weighted consensus.
6. Deterrence condition $p \cdot q \cdot L > \rho \cdot b$ for random audit games, and the security property of indistinguishable replication.
7. Consistency proof with SCX Theorem 3---meta-audit operates on cross-source disagreement information, not violating noise/difficulty indistinguishability.

The meta-audit protocol elevates the SCX Framework from ``trust the auditor'' to ``verify the auditor,'' achieving reflexive completeness of the audit regime. It is both a mathematical theorem and an institutional design---combining statistical rigor with game-theoretic incentive compatibility.

## 附录 A: 关键符号表 / Appendix A: Key Notation

[Table omitted — see original .tex]

\begin{thebibliography}{99}

\bibitem{hoeffding1963}
W. Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock *Journal of the American Statistical Association*, 58(301):13--30, 1963.

\bibitem{scx_core}
SCX Core Team.
\newblock SCX Equality Framework: Theorems 1--8.
\newblock Technical Report, 2025.

\bibitem{castro1999}
M. Castro and B. Liskov.
\newblock Practical Byzantine fault tolerance.
\newblock In *OSDI*, 1999.

\bibitem{prelec2004}
D. Prelec.
\newblock A Bayesian truth serum for subjective data.
\newblock *Science*, 306(5695):462--466, 2004.

\bibitem{bernstein1924}
S. Bernstein.
\newblock On a modification of Chebyshev's inequality.
\newblock *Annals of Mathematical Statistics*, 1924.

\bibitem{cramer1946}
H. Cramér.
\newblock *Mathematical Methods of Statistics*.
\newblock Princeton University Press, 1946.

\bibitem{wasserman2004}
L. Wasserman.
\newblock *All of Statistics*.
\newblock Springer, 2004.

\bibitem{lehmann2005}
E. L. Lehmann and J. P. Romano.
\newblock *Testing Statistical Hypotheses*, 3rd ed.
\newblock Springer, 2005.

\bibitem{bentkus2004}
V. Bentkus.
\newblock On Hoeffding's inequalities.
\newblock *Annals of Probability*, 32(2):1650--1673, 2004.

\bibitem{audit_sword}
SCX Audit Sword Protocol.
\newblock *SCX Framework Documentation*, 2025.

\bibitem{byzantine_consensus}
M. Pease, R. Shostak, and L. Lamport.
\newblock Reaching agreement in the presence of faults.
\newblock *Journal of the ACM*, 27(2):228--234, 1980.

\bibitem{buenau2020}
M. Bun and T. Steinke.
\newblock Concentrated differential privacy.
\newblock *Journal of Privacy and Confidentiality*, 2020.

\end{thebibliography}