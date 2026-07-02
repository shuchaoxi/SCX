<div align="center">

\fbox{\parbox{0.92\textwidth}{

**摘要 Abstract**

本文为SCX平等论框架中的社会推论模块定义势能算子 $\Sop$ 的操作形式。
$\Sop$ 将社会实体映射为标量势能值，涵盖三个维度：
**国家势能**（人均GDP / 基尼系数 / 预期寿命）、
**财富势能**（净资产分位数 / 收入分位数）、
**认知势能**（教育年限 / 论文引用 / 抽象思维测试）。
每个算子满足四个条件：可量化、可审计、满足规范固定条件 $\sum_m g_m = 0$、
以及跨域可比性。本文在SCX框架内严格形式化这些定义，并提供审计协议与实证校准路径。

*We define the operational form of the potential operator $\Sop$ for the social-inference module of the SCX egalitarian framework. $\Sop$ maps social entities to scalar potential values across three dimensions: **national potential** (per-capita GDP / Gini coefficient / life expectancy), **wealth potential** (net-asset quantile / income quantile), and **cognitive potential** (years of education / citation count / abstract-thinking test). Each operator satisfies four conditions: quantifiability, auditability, the gauge-fixing condition $\sum_m g_m = 0$, and cross-domain comparability. We formalize these definitions rigorously within the SCX framework and provide audit protocols and empirical calibration paths.*
}}

</div>

---

## 引言与框架背景 Introduction and Framework Background

### SCX平等论中的社会推论 Social Inference in SCX Egalitarianism

SCX框架的核心洞见之一是：社会系统中的不平等不仅仅是一个统计现象，
而是一个**场论问题**。社会实体（个人、家庭、区域、国家）之间的差异可以
被建模为一个社会标量场 $\socialfield: \universe \to \R$ 的局部梯度效应，
其中 $\universe$ 是社会实体的宇宙。

*One of the core insights of the SCX framework is that inequality in social systems is not merely a statistical phenomenon, but a **field-theoretic problem**. Differences among social entities (individuals, households, regions, nations) can be modeled as local gradient effects of a social scalar field $\socialfield: \universe \to \R$, where $\universe$ is the universe of social entities.*

在SCX形式体系中，我们区分两个核心算子：

1. **Cercis得分算子 $S$**：衡量数据质量的审计工具，定义在Situs编码空间上，
2. **势能算子 $\Sop$**（本文主题）：衡量社会实体在某个维度上的

*In the SCX formal apparatus, we distinguish two core operators:*

1. **Cercis Score operator $S$**: the audit tool measuring data quality, defined over Situs encoding space, satisfying $S = Q + \eta N$, where $Q$ is the quality component, $N$ the noise component, and $\eta$ the noise--hardness coupling parameter.
2. **Potential operator $\Sop$** (the subject of this paper): the operational definition measuring a social entity's *relative position* or *potential* in a given dimension, constituting the foundational input for social inference.

### 势能算子的四个设计约束 Four Design Constraints

任何有效的势能算子 $\Sop$ 必须满足四个公理条件：

*Any valid potential operator $\Sop$ must satisfy four axiomatic conditions:*

\begin{axiom}[可量化 Quantifiability] <!-- label: ax:quant -->
对任意社会实体 $e \in \universe$，$\Sop(e)$ 是一个定义良好的实数，且存在一个
有限算法在输入 $e$ 的观测数据后，在有限时间内输出 $\Sop(e)$ 的估计值。

*For any social entity $e \in \universe$, $\Sop(e)$ is a well-defined real number, and there exists a finite algorithm that outputs an estimate of $\Sop(e)$ in finite time given observational data about $e$.*
\end{axiom}

\begin{axiom}[可审计 Auditability] <!-- label: ax:audit -->
$\Sop$ 的任意具体计算实例必须附带一个**审计轨迹**（audit trail）$T(e) = \{d_1, ..., d_k\}$，
使得任意独立审计者 $A$ 使用 $T(e)$ 可以验证 $\Sop(e)$ 的计算正确性，且验证过程
的样本复杂度满足SCX T5主动学习界限。

*Every concrete computation instance of $\Sop$ must carry an **audit trail** $T(e) = \{d_1, ..., d_k\}$ such that any independent auditor $A$ can verify the correctness of $\Sop(e)$ using $T(e)$, and the sample complexity of the verification process satisfies the SCX T5 active-learning bounds.*
\end{axiom}

\begin{axiom}[规范固定 Gauge Fixing] <!-- label: ax:gauge -->
对于域 $\universe$ 内的所有实体，$\Sop$ 的值满足规范固定条件：

$$
    \sum_{e \in \universe} g_e(\Sop) = 0
    <!-- label: eq:gauge-fix -->
$$

其中 $g_e(\Sop)$ 为实体 $e$ 的规范权重函数。在最简单的均匀规范下，$g_e = \Sop(e) - \bar$，
其中 $\bar = |\universe|^{-1} \sum_{e} \Sop(e)$，即 $\sum_{e} \Sop(e) = 0$。

*For all entities in domain $\universe$, the value of $\Sop$ satisfies the gauge-fixing condition as in Eq.~( [ref]), where $g_e(\Sop)$ is the gauge-weight function for entity $e$. Under the simplest uniform gauge, $g_e = \Sop(e) - \bar$, where $\bar = |\universe|^{-1} \sum_{e} \Sop(e)$, i.e., $\sum_{e} \Sop(e) = 0$.*
\end{axiom}

\begin{axiom}[跨域可比性 Cross-Domain Comparability] <!-- label: ax:compare -->
若两个实体 $e_1, e_2$ 分属不同社会域 $\universe_1, \universe_2$，
则存在一个规范变换 $\tau_{12}: \R \to \R$ 使得 $\Sop(e_1)$ 与 $\tau_{12}(\Sop(e_2))$
可比，且 $\tau_{12}$ 满足传递性：$\tau_{12} \circ \tau_{23} = \tau_{13}$。

*If two entities $e_1, e_2$ belong to distinct social domains $\universe_1, \universe_2$, there exists a gauge transformation $\tau_{12}: \R \to \R$ such that $\Sop(e_1)$ and $\tau_{12}(\Sop(e_2))$ are comparable, and $\tau_{12}$ satisfies transitivity: $\tau_{12} \circ \tau_{23} = \tau_{13}$.*
\end{axiom}

### 规范固定条件的物理与社会意涵 Physical and Social Meaning of Gauge Fixing

规范固定条件 $\sum_m g_m = 0$ 源自规范场论中的标准技术。在社会场论语境中，
其意涵如下：

*The gauge-fixing condition $\sum_m g_m = 0$ originates from standard techniques in gauge field theory. In the social-field-theoretic context, its meaning is:*

1. **相对性原理 Principle of Relativity**：社会势能是*相对*量，而非*绝对*量。
2. **零和校准 Zero-Sum Calibration**：规范固定确保社会势能的全球平均为零。
3. **消除冗余自由度 Elimination of Redundant Degrees of Freedom**：社会势能的绝对值
4. **群结构 Group Structure**：规范变换构成一个加法群 $\gaugegroup \cong (\R, +)$。

## S 算子的一般形式 General Form of $\Sop$

### 形式定义 Formal Definition

> **Definition:** [势能算子 $\Sop$]
> 设 $\universe$ 为社会实体宇宙，$m$ 为测量维度指标。势能算子 $\Sop$ 定义为一个泛函：
> 
> $$
>     \Sop: \universe \times \mathcal{M} \to \R
> $$
> 
> 其中 $\mathcal{M} = \{nat, wealth, cog, ...\}$ 为度量维度集合。
> 对于实体 $e \in \universe$ 和维度 $m \in \mathcal{M}$：
> 
> $$
>     \Sop(e; m) = \Phi_m\big(x_1^{(m)}(e), x_2^{(m)}(e), ..., x_{k_m}^{(m)}(e)\big)
>     <!-- label: eq:S-general -->
> $$
> 
> 其中 $\{x_i^{(m)}(e)\}_{i=1}^{k_m}$ 为维度 $m$ 下实体的 $k_m$ 个可观测特征，
> $\Phi_m: \R^{k_m} \to \R$ 为维度特定的聚合函数。
> 
> 
> \textit{Let $\universe$ be the universe of social entities and $m$ a measurement-dimension index. The potential operator $\Sop$ is defined as a functional as in Eq.~( [ref]), where $\mathcal{M} = \{nat, wealth, cog, ...\}$ is the set of measurement dimensions. For entity $e \in \universe$ and dimension $m \in \mathcal{M}$, $\{x_i^{(m)}(e)\}_{i=1}^{k_m}$ are the $k_m$ observable features of the entity under dimension $m$, and $\Phi_m: \R^{k_m} \to \R$ is the dimension-specific aggregation function.}

### 聚合函数的设计原则 Design Principles for $\Phi_m$

每个 $\Phi_m$ 必须满足以下设计原则：

*Each $\Phi_m$ must satisfy the following design principles:*

1. **单调性 Monotonicity**：对于每个正向特征 $x_i$（值越大越优），
2. **齐次性 Homogeneity**：$\Phi_m$ 满足度-1正齐次性：
3. **可加可分性 Additive Separability**：$\Phi_m(x_1, ..., x_{k_m}) = \sum_{i=1}^{k_m} w_i \cdot f_i(x_i)$，
4. **鲁棒性 Robustness**：$\Phi_m$ 对异常值不敏感，满足影响函数有界性：

### 标准化协议与规范固定 Normalization Protocol and Gauge Fixing

给定维度 $m$ 下的原始聚合值 $\tilde{S}_m(e) = \Phi_m(x_1^{(m)}(e), ..., x_{k_m}^{(m)}(e))$，
规范固定的势能算子定义为：

*Given raw aggregated values $\tilde{S}_m(e)$, the gauge-fixed potential operator is:*

$$
    \Sop(e; m) = \frac{\tilde{S}_m(e) - \mu_m}{\sigma_m}
    <!-- label: eq:z-normalize -->
$$

其中 $\mu_m = |\universe|^{-1} \sum_{e \in \universe} \tilde{S}_m(e)$ 为全局均值，
$\sigma_m = \sqrt{|\universe|^{-1} \sum_{e} (\tilde{S}_m(e) - \mu_m)^2}$ 为全局标准差。

*where $\mu_m$ is the global mean and $\sigma_m$ the global standard deviation.*

 此标准化自动满足：

$$
    \sum_{e \in \universe} \Sop(e; m) = 0, \quad
    \frac{1}{|\universe|} \sum_{e \in \universe} [\Sop(e; m)]^2 = 1
    <!-- label: eq:gauge-verified -->
$$

 即 $\Sop(e; m) \sim N(0,1)$ 当底层 $\tilde{S}_m$ 服从正态分布时。
更一般地，式( [ref])中的第一式正是公理 [ref]中
均匀规范的特殊情形：$g_e(\Sop) = \Sop(e; m)$。

*This normalization automatically satisfies Eq.~( [ref]), which is precisely the uniform-gauge special case of Axiom [ref].*

## 国家势能算子 $\Sopnat$ National Potential Operator

### 概念定义 Conceptual Definition

国家势能 $\Sopnat$ 衡量一个主权国家（或等效政治实体）在为公民提供基础福祉条件方面
的结构性潜力。它整合三个基本维度：

*National potential $\Sopnat$ measures the structural potential of a sovereign state (or equivalent political entity) to provide basic welfare conditions for its citizens. It integrates three fundamental dimensions:*

1. **经济产出 Economic Output**：人均GDP（购买力平价，PPP），反映物质资源可得性。
2. **分配公平 Distributional Fairness**：基尼系数，反映资源分配的均等程度（负向指标）。
3. **生命质量 Life Quality**：出生预期寿命，反映健康基础设施与营养安全的综合结果。

> **Remark:** 这三个维度在概念上覆盖了Sen的能力方法（capability approach）的核心要素：
> 物质资源（GDP）、资源分配（Gini）、基本功能性活动（预期寿命）。
> 它们共同度量一个国家的*潜力*——即公民能够实现有价值的生活功能的*能力空间*，
> 而非实际成就本身。
> *These three dimensions conceptually cover the core elements of Sen's capability approach: material resources (GDP), resource distribution (Gini), and basic functionings (life expectancy). Together they measure a nation's *potential* — the *capability space* in which citizens can achieve valuable functionings, rather than the achievements themselves.*

### 可观测变量与数据源 Observable Variables and Data Sources

[Table omitted — see original .tex]

 所有数据源均来自公开可获取的国际数据库，满足公理 [ref]的审计要求。
*All data sources are from publicly accessible international databases, satisfying the audit requirement of Axiom [ref].*

### 聚合函数构造 Aggregation Function Construction

国家势能的原始聚合值定义为三个标准化特征的对数加权平均：

*The raw national potential aggregation is defined as a log-weighted average of three normalized features:*

$$
    \tilde{S}_{nat}(e) = w_1 \cdot \log(x_1(e)) + w_2 \cdot \log(1 - x_2(e)) + w_3 \cdot \log(x_3(e))
    <!-- label: eq:nat-raw -->
$$

其中权重满足 $w_1, w_2, w_3 \geq 0$ 且 $\sum w_i = 1$。

*where weights satisfy $w_1, w_2, w_3 \geq 0$ and $\sum w_i = 1$.*

**对数变换的理由 Rationale for the log transform:**

1. GDP和预期寿命呈现对数正态分布特征，对数变换使分布接近正态，
2. 对数变换将乘性差异转为加性差异，使得势能差具有比例解释：
3. $(1 - x_2(e))$ 的补数变换确保高基尼系数（更不平等）→ 低势能，且当 $x_2 \to 1$（极端不平等）时，

### 规范固定与最终形式 Gauge Fixing and Final Form

令全局均值与标准差为：

$$
    \mu_{nat} &= \frac{1}{N} \sum_{e=1}^{N} \tilde{S}_{nat}(e) 

    \sigma_{nat} &= \sqrt{\frac{1}{N} \sum_{e=1}^{N} \big(\tilde{S}_{nat}(e) - \mu_{nat}\big)^2}
$$

则规范固定的国家势能算子为：

$$
    \boxed{\Sopnat(e) = \frac{\tilde{S}_{nat}(e) - \mu_{nat}}{\sigma_{nat}}}
    <!-- label: eq:nat-final -->
$$

 自动满足 $\sum_e \Sopnat(e) = 0$——全球国家势能的平均水平被校准为零。
正值表示高于全球平均的国家潜力，负值表示低于全球平均。
*Automatically satisfies $\sum_e \Sopnat(e) = 0$ — the global mean of national potential is calibrated to zero. Positive values indicate above-average national potential; negative values indicate below-average.*

### 权重的实证校准 Empirical Calibration of Weights

权重向量 $\mathbf{w} = (w_1, w_2, w_3)$ 可以通过以下两种互补方法确定：

*The weight vector $\mathbf{w} = (w_1, w_2, w_3)$ can be determined through two complementary methods:*

1. **主成分分析 PCA**：
2. **德尔菲专家共识 Delphi Expert Consensus**：
3. **融合 Fusion**：$\mathbf{w} = \alpha \mathbf{w}_{PCA} + (1-\alpha) \mathbf{w}_{Delphi}$，

> **Remark:** 默认推荐权重为等权重 $\mathbf{w} = (1/3, 1/3, 1/3)$，作为无信息先验，
> 除非有强有力的实证证据支持偏离等权重。这最小化了对特定价值判断的依赖。
> *Default recommended weights are equal weights $\mathbf{w} = (1/3, 1/3, 1/3)$ as an uninformative prior, unless strong empirical evidence supports deviation from equality. This minimizes dependence on specific value judgments.*

### 审计协议 Audit Protocol

国家势能算子的审计协议包括以下步骤（算法 [ref]）：

\begin{algorithm}[htbp]
\caption{国家势能审计协议 $\mathcal{A}_{nat}$}
<!-- label: alg:audit-nat -->
\begin{algorithmic}[1]
\State **输入 Input**：国家列表 $\mathcal{L} = \{e_1, ..., e_N\}$，审计预算 $B$
\State **输出 Output**：势能向量 $\mathbf{S} = (\Sopnat(e_1), ..., \Sopnat(e_N))$ 及验证报告
\State **步骤 1 数据溯源 Data Provenance**：
    \For{$e \in \mathcal{L}$}
        \State 从WDI/WEO获取 $x_1(e)$（记录API调用时间戳与版本号）
        \State 从SWIID获取 $x_2(e)$（记录估算方法类型：直接调查/间接估算）
        \State 从WHO获取 $x_3(e)$（记录生命表方法版本）
    \EndFor
\State **步骤 2 一致性检查 Consistency Check**：
    \State 对每对国家 $(e_i, e_j)$，验证数据年份差异 $\leq 3$ 年
    \State 若年份差异 $> 3$，标记为"时间可比性警告"（Temporal Comparability Warning）
\State **步骤 3 聚合 Aggregation**：
    \State 计算 $\tilde{S}_{nat}(e) \leftarrow \sum_{i=1}^3 w_i \cdot f_i(x_i(e))$（式 [ref]）
\State **步骤 4 规范固定 Gauge Fixing**：
    \State $\mu \leftarrow N^{-1}\sum_e \tilde{S}(e)$，$\sigma \leftarrow \sqrt{N^{-1}\sum_e (\tilde{S}(e) - \mu)^2}$
    \State 验证 $\left|\sum_e \Sopnat(e)\right| < \epsilon_{machine}$（即满足规范固定条件）
\State **步骤 5 异常检测 Anomaly Detection**：
    \State 对 $|\Sopnat(e)| > 3$ 的实体标记为审计异常（可能的测量误差或数据篡改）
\State **步骤 6 发布审计轨迹 Publish Audit Trail**：
    \State 输出：$\{(e, x_1, x_2, x_3, \tilde{S}, \Sopnat, timestamp, source\_version)\}_{e \in \mathcal{L}}$
    \State 对每个记录计算SHA-256哈希并写入不可变日志
\end{algorithmic}
\end{algorithm}

 此协议保证：任意独立审计者可以仅使用公开数据和算法 [ref]完全复现
$\Sopnat(e)$ 的值，满足公理 [ref]。
*This protocol guarantees that any independent auditor can fully reproduce the values of $\Sopnat(e)$ using only public data and Algorithm [ref], satisfying Axiom [ref].*

### 量化示例 Illustrative Quantification

设三个虚构国家（基于2023年典型数据）：

[Table omitted — see original .tex]

 $\Sopnat(A) = +1.42$ 表示A国的国家潜力比全球平均高1.42个标准差。
$\Sopnat(C) = -1.24$ 表示C国的国家潜力比全球平均低1.24个标准差。
两者之差 $2.66$ 标准差度量了全球国家潜力的极端跨度。

*$\Sopnat(A) = +1.42$ indicates Country A's national potential is 1.42 standard deviations above the global mean. $\Sopnat(C) = -1.24$ indicates Country C's is 1.24 below. The difference of 2.66 standard deviations measures the extreme span of global national potential.*

## 财富势能算子 $\Sopwealth$ Wealth Potential Operator

### 概念定义 Conceptual Definition

财富势能 $\Sopwealth$ 衡量个人或家庭在资产-收入空间中的相对经济位置。
与绝对财富量不同，财富势能强调的是个体在分布中的*位置*和*潜力*——
即个体利用经济资源实现目标的能力的空间映射。

*Wealth potential $\Sopwealth$ measures the relative economic position of an individual or household in asset--income space. Unlike absolute wealth, wealth potential emphasizes the *position* and *potential* in the distribution — the spatial mapping of an individual's ability to use economic resources to achieve goals.*

财富势能整合两个维度：

1. **净资产存量 Net Asset Stock**：总资产减去总负债，反映累积的经济安全垫。
2. **收入流 Income Flow**：年可支配收入（税后+转移支付），反映当前的经济活力。

> **Remark:** 区分存量和流量是财富势能设计的核心。一个退休人员可能有高净资产（存量）但低收入（流量）；
> 一个年轻专业人士可能有高收入但低净资产。仅使用其中任意一个都会系统性地低估或高估
> 特定人群的经济潜力。整合两者可以得到更完整的画像。
> *Distinguishing stock and flow is central to wealth-potential design. A retiree may have high net assets (stock) but low income (flow); a young professional may have high income but low net assets. Using either alone systematically under- or over-estimates economic potential for specific populations. Integrating both yields a more complete picture.*

### 分位数基础的定义 Quantile-Based Definition

财富势能的核心创新在于使用**分位数**而非原始值。原因如下：

*The core innovation of wealth potential is the use of **quantiles** rather than raw values. The reasons are:*

1. **分布鲁棒性 Distributional Robustness**：财富和收入呈现极端的Pareto尾部行为。
2. **跨域可比性 Cross-Domain Comparability**：分位数天然归一化到 $[0, 1]$，
3. **隐私友好 Privacy-Friendly**：发布分位数而非原始值减少了个人识别风险，

### 聚合函数构造 Aggregation Function Construction

设 $Q_{net}(e)$ 为实体 $e$ 在参考总体中的净资产分位数（取值于 $[0, 1]$），
$Q_{inc}(e)$ 为可支配收入分位数。财富势能的原始聚合值定义为：

*Let $Q_{net}(e)$ be the net-asset quantile of entity $e$ in the reference population (range $[0, 1]$), and $Q_{inc}(e)$ the disposable-income quantile. The raw wealth potential is:*

$$
    \tilde{S}_{wealth}(e) = v_1 \cdot \Phi^{-1}(Q_{net}(e)) + v_2 \cdot \Phi^{-1}(Q_{inc}(e))
    <!-- label: eq:wealth-raw -->
$$

其中 $\Phi^{-1}$ 为标准正态分布的分位数函数（probit变换），将 $[0, 1]$ 映射到 $\R$。
权重 $v_1, v_2 \geq 0$ 且 $v_1 + v_2 = 1$。

*where $\Phi^{-1}$ is the quantile function (probit transform) of the standard normal distribution, mapping $[0,1]$ to $\R$. Weights $v_1, v_2 \geq 0$, $v_1+v_2=1$.*

**Probit变换的理由 Rationale for the probit transform:**

1. 分位数 $Q \sim U(0,1)$ → $\Phi^{-1}(Q) \sim N(0,1)$，即变换后的变量服从标准正态分布。
2. 正态分布的双尾特性自然反映了极端富裕（上尾）和极端贫困（下尾）。

### 规范固定与最终形式 Gauge Fixing and Final Form

在全体实体上标准化：

$$
    \boxed{\Sopwealth(e) = \frac{\tilde{S}_{wealth}(e) - \mu_{wealth}}{\sigma_{wealth}}}
    <!-- label: eq:wealth-final -->
$$

其中 $\mu_{wealth} = N^{-1} \sum_e \tilde{S}_{wealth}(e)$，
$\sigma_{wealth} = \sqrt{N^{-1} \sum_e (\tilde{S}_{wealth}(e) - \mu_{wealth})^2}$。

 规范固定条件 $\sum_e \Sopwealth(e) = 0$ 在此自动满足。
*The gauge-fixing condition $\sum_e \Sopwealth(e) = 0$ is automatically satisfied.*

### 审计协议 Audit Protocol

财富势能的数据来源取决于域：

*Wealth potential data sources depend on the domain:*

[Table omitted — see original .tex]

 审计轨迹包括：$\{e, Q_{net}, Q_{inc}, \tilde{S}, \Sopwealth, survey\_wave, imputation\_flag\}$。
审计者可通过独立调查或公开微数据抽样验证分位数值。
*The audit trail includes entity ID, quantiles, raw and gauge-fixed potentials, survey wave, and imputation flags. Auditors can verify quantile values through independent surveys or public microdata sampling.*

### 量化示例 Illustrative Quantification

以典型中国家庭为例（基于2022年CHFS数据分布）：

[Table omitted — see original .tex]

 $\Sopwealth$ 的中位零值恰好是规范固定条件的直接结果：
参考总体的平均财富势能恒为零。$\Sopwealth = +2.85$ 意味着该家庭的经济潜力比总体中位数
高2.85个标准差。这提供了一个对极端值具有鲁棒性的经济位置度量。

*The median-zero value of $\Sopwealth$ is a direct consequence of gauge fixing: the mean wealth potential of the reference population is identically zero. $\Sopwealth = +2.85$ means the household's economic potential is 2.85 standard deviations above the population median. This provides an economic-position metric robust to extreme values.*

## 认知势能算子 $\Sopcog$ Cognitive Potential Operator

### 概念定义 Conceptual Definition

认知势能 $\Sopcog$ 衡量个体在处理抽象信息、生成知识和解决复杂问题方面的潜力。
这是三个势能维度中最具挑战性的，因为认知能力是*潜变量*（latent variable），
无法直接观测，必须通过代理变量间接度量。

*Cognitive potential $\Sopcog$ measures an individual's potential for processing abstract information, generating knowledge, and solving complex problems. This is the most challenging of the three potential dimensions, as cognitive ability is a *latent variable* that cannot be directly observed and must be measured indirectly through proxy variables.*

认知势能整合三个代理变量：

1. **教育年限 Education Years**：正规教育的总年限（包括高等教育），反映制度化知识获取。
2. **研究产出 Research Output**：经学科规范化的论文引用次数（领域-年份标准化），
3. **抽象思维能力 Abstract Reasoning**：标准化抽象推理测试得分（如Raven渐进矩阵），

> **Remark:** 这三个代理变量分别对应Cattell-Horn-Carroll理论中的三个层次：
> 教育年限 → 晶体智力（$G_c$），抽象推理 → 流体智力（$G_f$），
> 论文引用 → 领域特定的专业知识（$G_{kn}$）。
> 它们共同构成认知潜力的多维代理，但不能声称完全穷尽了认知能力的所有方面。
> *These three proxies correspond to three strata in the Cattell-Horn-Carroll theory: education → crystallized intelligence ($G_c$), abstract reasoning → fluid intelligence ($G_f$), citations → domain-specific knowledge ($G_{kn}$). Together they form a multidimensional proxy for cognitive potential, but cannot claim to exhaust all aspects of cognitive ability.*

### 聚合函数构造 Aggregation Function Construction

由于论文引用仅适用于学术研究人群（$\approx$ 总人口的 $<1\%$），
认知势能需要处理**缺失变量**问题。我们定义两个版本：

*Since citation data applies only to the academic research population ($\approx <1\%$ of total population), cognitive potential must handle **missing-variable** issues. We define two versions:*

**版本 A — 学术人群 Academic Population**（$x_3$ 可用）：

$$
    \tilde{S}_{cog}^{(A)}(e) = u_1 \cdot z_{edu}(e) + u_2 \cdot z_{cite}(e) + u_3 \cdot z_{reason}(e)
    <!-- label: eq:cog-A -->
$$

**版本 B — 一般人群 General Population**（$x_3$ 不可用）：

$$
    \tilde{S}_{cog}^{(B)}(e) = u_1' \cdot z_{edu}(e) + u_3' \cdot z_{reason}(e)
    <!-- label: eq:cog-B -->
$$

其中 $z_{var}(e) = (x_{var}(e) - \bar{x}_{var}) / s_{var}$ 为各变量的z-score标准化，
$u_i, u_i'$ 为重新归一化后的权重。

*where $z_{var}(e)$ are the z-score normalized values of each variable, and $u_i, u_i'$ are renormalized weights.*

### 论文引用的领域-年份标准化 Field-Year Normalization of Citations

论文引用具有强领域依赖性和时间依赖性。数学论文的平均引用远低于生物医学论文；
新论文的引用积累需要时间。直接使用原始引用计数会产生严重的系统性偏差。

*Paper citations have strong field dependence and time dependence. Raw citation counts would produce severe systematic bias.*

我们采用**相对引用率**（Relative Citation Rate, RCR）：

$$
    z_{cite}(e) = \frac{1}{|P(e)|} \sum_{p \in P(e)} \frac{c(p) - \mu(field(p), year(p))}{\sigma(field(p), year(p))}
    <!-- label: eq:rcr -->
$$

其中 $P(e)$ 为实体 $e$ 的论文集合，$c(p)$ 为论文 $p$ 的引用总数，
$\mu(f, y)$ 和 $\sigma(f, y)$ 分别为领域 $f$、出版年 $y$ 中论文的平均引用数和标准差。
此标准化使不同领域的引用影响力可比。

*where $P(e)$ is the set of papers by entity $e$, $c(p)$ is the total citation count, and $\mu(f,y), \sigma(f,y)$ are the mean and standard deviation of citations in field $f$, publication year $y$. This normalization makes citation impact comparable across fields.*

> **Remark:** RCR的一个关键优势是：在领域 $f$、年份 $y$ 的参考集内，RCR的均值恰为0，标准差为1。
> 这使得RCR天然满足该参考集内的规范固定条件。*A key advantage of RCR: within the reference set of field $f$, year $y$, the mean of RCR is exactly 0 and its standard deviation is 1. This makes RCR naturally satisfy gauge-fixing within that reference set.*

### 规范固定与最终形式 Gauge Fixing and Final Form

$$
    \boxed{\Sopcog(e) = \frac{\tilde{S}_{cog}(e) - \mu_{cog}}{\sigma_{cog}}}
    <!-- label: eq:cog-final -->
$$

$\mu_{cog}, \sigma_{cog}$ 基于适当的参考总体计算（学术人群版本A的参考总体为
全球学术研究者；一般人群版本B的参考总体为国家/区域的成年人口）。

*$\mu_{cog}, \sigma_{cog}$ are computed based on the appropriate reference population (version A: global academic researchers; version B: national/regional adult population).*

### 审计协议 Audit Protocol

认知势能的审计面临独特的挑战：论文引用数据存在游戏化风险（引用圈、自引），
抽象推理测试存在练习效应和测试条件差异。

*Auditing cognitive potential faces unique challenges: citation data is subject to gaming risks (citation rings, self-citation), and abstract-reasoning tests are subject to practice effects and test-condition variance.*

审计协议包含以下反游戏化措施：

*The audit protocol includes the following anti-gaming measures:*

1. **自引去除 Self-Citation Removal**：在计算 $c(p)$ 时排除所有自引（作者或合著者的引用），
2. **引用圈检测 Citation-Cartel Detection**：计算作者间的引用Jaccard相似度矩阵；
3. **测试条件校准 Test-Condition Calibration**：抽象推理测试得分需附带测试条件元数据
4. **重复测量校正 Repeated-Measures Correction**：若同一个体多次参加测试，

### 量化示例 Illustrative Quantification

[Table omitted — see original .tex]

 $\Sopcog = +2.45$ 表示该研究者的认知潜力在全球学术人群中处于前 $0.7\%$ 的水平。
注意：此度量反映的是*潜力*（基于教育和认知测试的*能力空间*），
而非*成就*本身（虽然RCR已经部分捕捉了成就维度）。

*$\Sopcog = +2.45$ indicates this researcher's cognitive potential is in the top $0.7\%$ of the global academic population. Note: this metric reflects *potential* (the *capability space* based on education and cognitive tests), not *achievement* per se (though RCR already partially captures the achievement dimension).*

## 统一理论与算子间关系 Unified Theory and Inter-Operator Relations

### 三算子的统一形式 Unified Form of the Three Operators

三个势能算子 $\Sopnat$, $\Sopwealth$, $\Sopcog$ 共享一个统一的结构：

*The three potential operators $\Sopnat$, $\Sopwealth$, $\Sopcog$ share a unified structure:*

$$
    \boxed{\Sop_m(e) = \frac{1}{\sigma_m} \left( \sum_{i=1}^{k_m} w_i^{(m)} \cdot \psi_i^{(m)}\big(x_i^{(m)}(e)\big) - \mu_m \right)}
    <!-- label: eq:unified -->
$$

其中：

- $m \in \{nat, wealth, cog\}$ 为维度指标
- $k_m$ 为维度 $m$ 的特征数量
- $w_i^{(m)} \in [0,1]$ 为权重，$\sum_i w_i^{(m)} = 1$
- $\psi_i^{(m)}: \R \to \R$ 为特征变换函数（log, probit, z-score等）
- $\mu_m, \sigma_m$ 为全局均值和标准差（规范固定）

*where the parameters follow the specifications above.*

三个维度的特征变换函数汇总：

[Table omitted — see original .tex]

### 算子间的相关结构 Correlation Structure Among Operators

三个势能算子之间存在非零但非完全的相关性，其相关结构具有重要的社会科学意涵：

*The three potential operators exhibit nonzero but imperfect correlations, with important social-scientific implications:*

$$
    \mathbf{R} = \begin{pmatrix}
        1 & \rho_{nw} & \rho_{nc} 

        \rho_{nw} & 1 & \rho_{wc} 

        \rho_{nc} & \rho_{wc} & 1
    \end{pmatrix}
    <!-- label: eq:corr-matrix -->
$$

典型实证估计（基于跨国面板数据）：

- $\rho_{nw} \approx 0.45$—0.65（国家潜力与财富潜力中度正相关）
- $\rho_{nc} \approx 0.55$—0.75（国家潜力与认知潜力中高度正相关）
- $\rho_{wc} \approx 0.30$—0.50（财富潜力与认知潜力低中度正相关）

 这些相关性*不*是定义的一部分，而是社会系统的实证特征。
它们为SCX框架中的不平等交互效应分析提供输入。

*These correlations are *not* part of the definition but empirical features of the social system. They provide input for inequality interaction analysis in the SCX framework.*

### 与SCX审计框架的对接 Connection to SCX Audit Framework

社会势能算子 $\Sop$ 与SCX核心审计框架的关系如下：

*The relationship between the social potential operator $\Sop$ and the core SCX audit framework is as follows:*

1. **输入角色 Input Role**：$\Sop(e)$ 作为社会推论模块的*输入特征*，
2. **Cercis得分的分解 Decomposition into Cercis Score**：
3. **势能让渡与社会流动性 Potential Transfer and Social Mobility**：

## 规范理论的深层结构 Deep Structure of Gauge Theory

### 社会势能场作为一种规范理论 Social Potential Field as a Gauge Theory

社会势能 $\Sop$ 可以形式化为一个**规范场**。设 $\universe$ 为社会实体构成的底流形
（base manifold），$\socialfield(e) = \Sop(e)$ 为定义在 $\universe$ 上的标量场。
社会势能的规范群为加法群 $\gaugegroup = (\R, +)$，作用于 $\socialfield$ 上：

*Social potential $\Sop$ can be formalized as a **gauge field**. Let $\universe$ be the base manifold of social entities, and $\socialfield(e) = \Sop(e)$ a scalar field over $\universe$. The gauge group is the additive group $\gaugegroup = (\R, +)$, acting on $\socialfield$:*

$$
    \socialfield(e) \mapsto \socialfield(e) + c, \quad c \in \R
    <!-- label: eq:gauge-action -->
$$

 此变换不改变任何物理（社会）可观测量，因为只有势能*差*具有操作意义。
*This transformation does not change any physical (social) observable, since only potential *differences* have operational meaning.*

规范固定条件 $\sum_e g_e(\Sop) = 0$ 的群论解释：

*Group-theoretic interpretation of the gauge-fixing condition:*

1. 未规范固定的势能取值构成一个仿射空间（affine space），
2. 规范固定相当于选择一个截面（section）$\sigma: \universe \to \R$，
3. 不同截面之间的变换是一个全局平移，属于 $\gaugegroup$ 的作用。
4. 所有截面构成一个商空间 $\mathcal{S} = \{\socialfield: \universe \to \R\} / \gaugegroup$，

### 规范不变可观测量 Gauge-Invariant Observables

在规范理论中，只有规范不变量才有物理意义。以下量是规范不变的：

*In gauge theory, only gauge-invariant quantities have physical meaning. The following are gauge-invariant:*

1. **势能差 Potential Difference**：
2. **势能方差 Variance of Potential**：
3. **势能秩相关系数 Rank Correlation of Potentials**：
4. **势能梯度 Potential Gradient**：

### 规范固定的替代方案 Alternative Gauge-Fixing Schemes

虽然本文采用全局z-score标准化作为默认规范固定方案，但也可以考虑其他方案：

*While this paper adopts global z-score normalization as the default gauge-fixing scheme, alternative schemes can be considered:*

1. **中位数规范 Median Gauge**：
2. **极小值规范 Min-Gauge**：
3. **加权规范 Weighted Gauge**：
4. **参考锚点规范 Anchor-Point Gauge**：

> **Remark:** 规范固定方案的选择本身是一个*元层次的社会选择问题*。不同的规范固定方案不会改变
> 任何规范不变的量（如势能差、秩相关），但会影响可视化解释和政策叙事的框架。
> 因此，在应用中应明确标注所使用的规范固定方案，并提供至少两种方案的敏感性分析。
> *The choice of gauge-fixing scheme is itself a *meta-level social-choice problem*. Different schemes do not change any gauge-invariant quantities (potential differences, rank correlations), but they affect visualization interpretation and policy-narrative framing. Therefore, applications should explicitly state the scheme used and provide sensitivity analysis with at least two schemes.*

## 扩展与未来工作 Extensions and Future Work

### 多分辨率规范固定 Multi-Resolution Gauge Fixing

当前的定义采用全局规范固定。但在大型异构总体中，全局规范可能掩盖局部结构。
多分辨率规范固定将总体按层级（地理、行政、文化）划分为子群，在每个子群中单独固定规范：

*Current definitions use global gauge fixing. But in large heterogeneous populations, global gauges may mask local structure. Multi-resolution gauge fixing partitions the population by hierarchy (geographic, administrative, cultural) and fixes gauges within each subgroup:*

$$
    \Sop^{(L)}(e) = \frac{\tilde{S}(e) - \mu_h(e)}{\sigma_h(e)}, \quad h(e)  为  e  在第  L  层的子群
$$

 这允许在同一框架内进行*组内*不平等和*组间*不平等的分离分析。

### 动态势能与Spring更新 Dynamic Potential and Spring Updates

在SCX的Spring框架中，社会势能随数据更新而动态演化。定义势能的时间导数：

*In SCX's Spring framework, social potential evolves dynamically with data updates. Define the time derivative of potential:*

$$
    \dot_m(e, t) = \frac{\partial \Sop_m(e, t)}{\partial t} \approx \frac{\Sop_m(e, t+\Delta t) - \Sop_m(e, t)}{\Delta t}
$$

 $\dot > 0$ 表示势能在上升（社会流动性向上），$\dot < 0$ 表示势能在下降。
势能变化率本身就构成一个新的社会指标——**势能流**（Potential Flux），
其分布特征反映了社会流动性的速度和方向。

*$\dot > 0$ indicates rising potential (upward social mobility), $\dot < 0$ indicates declining potential. The rate of potential change constitutes a new social indicator — **potential flux** — whose distributional characteristics reflect the speed and direction of social mobility.*

### 势能算子的对抗鲁棒审计 Adversarially Robust Audit of Potential Operators

社会势能的量化必然会面临来自不同利益相关方的*势能博弈*：
国家可能低报基尼系数，个人可能夸大收入，研究者可能操纵引用指标。
这与SCX的AR-Theorem（对抗鲁棒性定理）直接相关。

*Quantification of social potential inevitably faces *potential gaming* from various stakeholders: nations may underreport Gini coefficients, individuals may inflate income, researchers may manipulate citation metrics. This directly connects to SCX's AR-Theorem.*

AR增强的势能算子定义为：

$$
    \Sop^{AR}(e) = \inf_{\delta \in \mathcal{B}(e)} \Sop(e; x_1 + \delta_1, ..., x_k + \delta_k)
$$

其中 $\mathcal{B}(e)$ 为实体 $e$ 的可行操纵球（feasible manipulation ball），
由数据审计的成本和检测概率决定。这个定义确保了势能值的对抗鲁棒下界。

*The AR-augmented potential operator takes the infimum over feasible manipulation balls, ensuring an adversarially robust lower bound on potential values.*

## 结论 Conclusion

本文为SCX平等论框架中的社会推论模块定义了势能算子 $\Sop$ 的完整操作形式。
三个维度——国家势能、财富势能、认知势能——覆盖了社会不平等的关键方面，
且全部满足四个公理条件：可量化、可审计、规范固定、跨域可比。

*This paper defines the complete operational form of the potential operator $\Sop$ for the social-inference module of the SCX egalitarian framework. Three dimensions — national potential, wealth potential, and cognitive potential — cover key aspects of social inequality, and all satisfy four axiomatic conditions: quantifiability, auditability, gauge fixing, and cross-domain comparability.*

核心贡献总结 Summary of Core Contributions:

1. **统一形式**：三个算子共享一个统一的聚合-标准化架构（式 [ref]），
2. **规范固定**：通过z-score标准化自动满足 $\sum_e \Sop(e) = 0$ 的规范固定条件，
3. **审计协议**：每个算子都附带了详细的审计协议（算法 [ref]），
4. **特征工程**：为每个维度提供了心理学/经济学上合理的特征变换函数
5. **规范理论对接**：将社会势能形式化为规范场论，建立了社会不平等的场论语言

**下一步 Next Steps:**

1. 使用真实世界数据（WDI, SWIID, CHFS, CFPS, OpenAlex）对三个算子进行实证校准。
2. 开发开源参考实现（Python/R包），包含完整的审计轨迹生成功能。
3. 进行规范固定方案的敏感性分析，评估不同方案对势能排序的影响。
4. 将势能算子集成到SCX的Sprint主动学习循环中，作为社会推论的特征输入。
5. 探索势能算子的量子推广（Q-Theorem），特别是在隐私保护数据聚合场景中的应用。

*Empirical calibration with real-world data; open-source reference implementation; sensitivity analysis of gauge-fixing schemes; integration into SCX Sprint active-learning loop; quantum generalization for privacy-preserving aggregation.*

## Appendix
## 附录：符号表 Appendix: Notation Table

[Table omitted — see original .tex]

## 附录：审计轨迹的JSON模式 Appendix: JSON Schema for Audit Trail

\begin{verbatim}
{
  "entity_id": "CHN",
  "dimension": "national",
  "timestamp": "2026-07-01T00:00:00Z",
  "raw_features": {
    "gdp_per_capita_ppp": 21500.0,
    "gini_coefficient": 0.382,
    "life_expectancy": 78.2
  },
  "feature_sources": {
    "gdp_per_capita_ppp": {
      "source": "World Bank WDI",
      "indicator": "NY.GDP.PCAP.PP.KD",
      "year": 2023,
      "api_version": "v2"
    },
    "gini_coefficient": {
      "source": "SWIID",
      "version": "9.4",
      "estimation_type": "direct_survey",
      "year": 2022
    },
    "life_expectancy": {
      "source": "WHO GHO",
      "indicator": "WHOSIS_000001",
      "year": 2023
    }
  },
  "transformed_features": {
    "log_gdp": 9.9758,
    "log_complement_gini": -0.4780,
    "log_life_expectancy": 4.3593
  },
  "weights": {"gdp": 0.333, "gini": 0.333, "life_exp": 0.333},
  "raw_potential": 3.2857,
  "gauge_parameters": {
    "mu": 3.1192,
    "sigma": 0.5438,
    "reference_population_size": 195,
    "gauge_scheme": "z-score"
  },
  "gauge_fixed_potential": 0.306,
  "audit_hashes": {
    "sha256_input": "abc123...",
    "sha256_output": "def456..."
  },
  "warnings": []
}
\end{verbatim}

## 附录：Python参考实现骨架 Appendix: Python Reference Implementation Skeleton

\begin{verbatim}
import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple

class PotentialOperator:
    """SCX Social Potential Operator S-hat.
    
    Implements the gauge-fixed potential operator for SCX social inference.
    Supports national, wealth, and cognitive dimensions.
    """
    
    def __init__(self, dimension: str, weights: Optional[Dict[str, float]] = None):
        self.dimension = dimension
        self.weights = weights or self._default_weights()
        self.mu: float = 0.0
        self.sigma: float = 1.0
    
    def _default_weights(self) -> Dict[str, float]:
        defaults = {
            "national": {"gdp": 1/3, "gini": 1/3, "life_exp": 1/3},
            "wealth": {"net_asset": 0.5, "income": 0.5},
            "cognitive": {"education": 1/3, "citation": 1/3, "reasoning": 1/3},
        }
        return defaults.get(self.dimension, {})
    
    def transform_features(self, raw: Dict[str, float]) -> Dict[str, float]:
        """Apply dimension-specific feature transforms."""
        ...
    
    def aggregate(self, transformed: Dict[str, float]) -> float:
        """Weighted sum of transformed features."""
        return sum(
            self.weights[k] * transformed[k]
            for k in self.weights if k in transformed
        )
    
    def fit_gauge(self, raw_potentials: np.ndarray) -> None:
        """Compute global mu and sigma for gauge fixing."""
        self.mu = np.mean(raw_potentials)
        self.sigma = np.std(raw_potentials, ddof=0)
    
    def gauge_fix(self, raw_potential: float) -> float:
        """Apply z-score gauge fixing."""
        return (raw_potential - self.mu) / self.sigma
    
    def compute(self, entity_features: Dict[str, float]) -> float:
        """Full pipeline: transform -> aggregate -> gauge-fix."""
        transformed = self.transform_features(entity_features)
        raw = self.aggregate(transformed)
        return self.gauge_fix(raw)
    
    def verify_gauge(self, potentials: np.ndarray, tol: float = 1e-10) -> bool:
        """Verify sum of gauge-fixed potentials is zero."""
        return abs(np.sum(potentials)) < tol

# Example usage:
op_national = PotentialOperator("national")
features = {"gdp": 65000, "gini": 0.30, "life_exp": 83.5}
S_nat = op_national.compute(features)
print(f"National potential: {S_nat:.3f}")
\end{verbatim}

<div align="center">

\rule{0.5\textwidth}{0.4pt}
{
**文档元信息 Document Metadata**

版本 Version: 1.0 

日期 Date: 2026-07-01 

作者 Author: SCX 理论架构师 SCX Theory Architect 

框架 Framework: SCX 平等论 SCX Egalitarianism 

依赖 Dependencies: T1--T7, AE-Theorem, AR-Theorem, FA-Theorem 

状态 Status: 草案 / Draft — 待同行审阅 Pending Peer Review

*本文件是SCX社会推论算子定义的正式技术文档。*
*所有算子定义均附带审计协议，满足SCX审计之剑的可验证性要求。*
*This document is the formal technical specification of SCX social-inference operator definitions.*
*All operator definitions carry audit protocols, satisfying the verifiability requirements of SCX's Audit Sword.*
}

</div>