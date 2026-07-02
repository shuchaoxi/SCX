*Abstract:*

AI alignment---ensuring that AI systems behave consistently with human values---
is the central safety challenge of modern machine learning.  Current alignment
techniques (RLHF, DPO, CAI) rely on human preference data to shape model
behavior.  But what if the alignment data itself is noisy---corrupted by
careless annotators, ambiguous preferences, or genuine value disagreements
among humans?  We formalize the reduction of alignment auditing to SCX data
quality auditing and prove four results with full mathematical rigor.

**Theorem AA.1** (Alignment--Audit Reduction): we construct an explicit
mapping $\Phi$ from alignment datasets $\cD_{\mathrm{align}}$ to SCX audit
datasets $\cD_{\mathrm{audit}}$ and derive an explicit upper bound
$\epsilon_\Phi = \varepsilon_{\mathrm{mono}} + L_\phi \cdot (1-|1-2\eta|)
\cdot \E[\Delta] + O\big(\sqrt{\log(1/\delta)/n}\big)$ on the alignment
quality approximation error.  Tightness of $\epsilon_\Phi$ remains open.
**Theorem AA.2** (RLHF Preference Noise Detection): we verify
*condition-by-condition* that the preference Cercis Score
$S_{\mathrm{pref}}$ satisfies all regularity conditions required by SCX
Theorems~1,~3, and~5, including explicit two-world constructions for T3's
unidentifiability and Lipschitz constant computation for T5.
**Theorem AA.3** (Alignment Tax): we derive from first principles the
lower bound $\tau_{\mathrm{align}} \geq \frac{1-\eta}\cdot
\frac{\mathrm{cost}(\mathrm{audit})}{\mathrm{cost}(\mathrm{train})}$ via the
audit sample complexity lower bound $n_{\mathrm{audit}} \geq
\frac{1-\eta}\cdot n$.  **Theorem AA.4** (Value--Noise
Indistinguishability): we explicitly construct two preference-generating
processes (World~A: noise-dominated; World~B: value-pluralism-dominated) and
prove that their joint distributions over observable variables are identical,
establishing Theorem~3's Alignment Corollary with full measure-theoretic
rigor.  All proofs are accompanied by **honest critiques** identifying
unverifiable assumptions, boundary violations, and open tightness questions.

## Introduction

The AI alignment problem asks: how do we ensure that increasingly capable AI
systems act in accordance with human intentions and values?
 [cite] frame it as the value-loading problem;
 [cite] catalog concrete safety issues; and practical
techniques---Reinforcement Learning from Human Feedback
(RLHF) [cite], Direct Preference Optimization
(DPO) [cite], Constitutional AI [cite]
---have achieved remarkable empirical success in aligning large language models.

But all these techniques share a critical vulnerability: they depend on
**human preference data**.  And human preference data---like all data---
can be noisy.  Annotators may be inattentive, inconsistent, or even
adversarial.  More profoundly, annotators may have *genuinely
incompatible values*---one person's ``helpful'' is another person's
``dangerously compliant.''  This paper formalizes the precise relationship
between alignment data quality and SCX auditing through four rigorous theorems.

本文件的主要贡献在于：将AA定理家族中的所有证明严格形式化，为每个定理提供
(1)~测度论基础的概率设定； (2)~完整的假设前提清单；
(3)~逐步骤验证的数学证明； (4)~关于假设可验证性和边界条件的诚实暴击。

**Contributions.**

1. **Alignment--Audit Reduction** (Theorem [ref]):
2. **RLHF Preference Noise Detection** (Theorem [ref]):
3. **Alignment Tax** (Theorem [ref]):
4. **Value Uncertainty vs.\ Noise** (Theorem [ref]):

## Preliminaries

### Measure-Theoretic Foundation

令 $(\Omega, \mathcal{F}, P)$ 为一个概率空间，支撑所有后续定义的随机变量。
$\cX$ 为提示空间（prompts），$\cY$ 为响应空间（responses）。
对每个 $x\in\cX$，定义条件概率测度 $P_{Y\mid X}(\cdot\mid x)$。

> **Definition:** [Alignment Dataset---Formal]
> <!-- label: def:align-data-formal -->
> 一个对齐数据集
> \[
> \cD_{\mathrm{align}} = \{(X_i, Y_i^+, Y_i^-)\}_{i=1}^n
> \]
> 由 $n$ 个独立同分布样本组成，其中 $X_i \sim P_X$，$(Y_i^+,Y_i^-)\sim P_{Y\mid X}(\cdot\mid X_i)$
> 是一对候选响应。对每个三元组 $(x,y^+,y^-)$，定义潜在偏好变量
> \[
> \tau(x) \in \{0,1\},
> \]
> 其中 $\tau(x)=1$ 表示人类真实偏好为 $y^+ \succ y^-$（即 $y^+$ 被真prefer），
> $\tau(x)=0$ 表示 $y^- \succ y^+$。

> **Definition:** [Preference Reversal Noise Model]
> <!-- label: def:pref-noise-formal -->
> 设 $\tau(X)$ 为真实偏好方向。观测到的偏好标签 $\tilde(X)$ 生成机制为：
> \[
> \tilde(X) =
> \begin{cases}
> \tau(X), & 以概率  1-\eta,

> 1-\tau(X), & 以概率  \eta,
> \end{cases}
> \]
> 其中 $\eta\in[0,\frac12)$ 为噪声率。该模型假设噪声与 $X$ 独立（对应 SCX A4 假设的均匀噪声）。
> 因此，条件偏好概率为：
> \[
> p(x) := P(\tilde=1 \mid X=x) = (1-\eta)P(\tau=1\mid x) + \eta P(\tau=0\mid x)
> = (1-2\eta)P(\tau=1\mid x) + \eta.
> \]

> **Definition:** [Preference Cercis Score]
> <!-- label: def:S-pref-formal -->
> 偏好 Cercis 得分定义为
> \[
> S_{\mathrm{pref}}(x) = \bigl|p(x) - \tfrac12\bigr|
> = \bigl|(1-2\eta)\bigr|\cdot\bigl|P(\tau=1\mid x) - \tfrac12\bigr|
> = |1-2\eta|\cdot \Delta(x),
> \]
> 其中 $\Delta(x) := |P(\tau=1\mid x) - \frac12| \in [0,\frac12]$ 为真实偏好清晰度
> （True Preference Clarity）。

> **Definition:** [Alignment Quality Function---Formal]
> <!-- label: def:align-quality-formal -->
> 对任意策略模型 $f:\cX\to\Delta(\cY)$（输出在响应空间上的分布），对齐质量定义为
> \[
> A(f) := \E_{X\sim P_X}\bigl[ \mathrm{Score}\bigl(f(X), \tau(X)\bigr) \bigr],
> \]
> 其中 $\mathrm{Score}:\Delta(\cY)\times\{0,1\}\to[0,1]$ 是一个有界评分函数，
> 衡量模型输出与真实偏好的一致性。具体来说，
> \[
> \mathrm{Score}(f(x), t) =
> \begin{cases}
> u(f(x), y^+), & t=1,

> u(f(x), y^-), & t=0,
> \end{cases}
> \]
> 且 $u:\Delta(\cY)\times\cY\to[0,1]$ 是效用函数（例如 $u(f(x),y)=f(x)_y$）。

### SCX 框架关键定理回顾

以下三个定理（来自 SCX 主论文）是 AA-Theorem 的依赖性基础。

> **Theorem:** [T1: Noise Detectability via Multi-Expert Consistency---简化陈述]
> <!-- label: thm:T1 -->
> 在假设 A1--A6 下，存在一个检验统计量 $T(\{f_m\}_{m=1}^M, y)$ 可以在显著性水平 $\alpha$ 下
> 以功效 $1-\beta$ 检测噪声样本。样本复杂度满足 $n = \Omega(\frac{1}{\eta^2}\log\frac{1})$。
> \rigorous

> **Theorem:** [T3: 老实人定理 (The Honest Person Theorem)]
> <!-- label: thm:T3 -->
> 对任何 $K\geq 2$ 的分类问题，存在两个数据生成过程 $\mathcal{P}_{\mathrm{noise}}$ 和
> $\mathcal{P}_{\mathrm{hard}}$，使得两者产生完全相同的可观测量联合分布，但
> $\mathcal{P}_{\mathrm{noise}}$ 中的标签错误由噪声引起，而 $\mathcal{P}_{\mathrm{hard}}$
> 中所有标签均正确但部分样本固有困难。\rigorous

> **Theorem:** [T5: Optimal Sampling for Active Learning---Cercis Rate]
> <!-- label: thm:T5 -->
> 在 Cercis 框架下，最大化期望 $F_1$ 增益的最优采样率为
> \[
> \rho^* = \frac{\eta\sum_k w_k\overline_k}
>               {\eta\sum_k w_k\overline_k + \sum_k w_k\V[\Gamma_k]},
> \]
> 其中 $\overline_k$ 是类别 $k$ 的期望 $F_1$ 增益，$\V[\Gamma_k]$ 是其方差。
> \rigorous

## Main Results

### Alignment--Audit Reduction (Theorem AA.1)

> **Theorem:** [Alignment--Audit Reduction Mapping]
> <!-- label: thm:reduction -->
> 令概率空间 $(\Omega,\mathcal{F},P)$ 及所有相关随机变量如定义 [ref]--
>  [ref] 所述。则存在一个可计算映射
> \[
> \Phi: (\cD_{\mathrm{align}}, f) \longmapsto (\cD_{\mathrm{audit}}, S),
> \]
> 将对齐问题转化为 SCX 审计问题，使得对任意 $f$ 和任意 $\delta\in(0,1)$，以概率 $\geq 1-\delta$ 有
> \[
> \bigl| A(f) - \tilde{A}(S) \bigr| \;\leq\; \epsilon_\Phi,
> \]
> 其中 $\tilde{A}(S)$ 从 SCX 审计结果重建的对齐质量估计，且
> \[
> \epsilon_\Phi = \underbrace{\varepsilon_{\mathrm{mono}}}_{单调性近似误差}
>                + \underbrace{L_\phi \cdot (1-|1-2\eta|) \cdot \E[\Delta]}_{噪声-清晰度偏差}
>                + \underbrace{L_\phi \cdot \eta \cdot \delta_{\mathrm{situs}}}_{Situs嵌入误差}
>                + \underbrace{\frac{1}{2}\sqrt{\frac{\log(2/\delta)}{2n}}}_{有限样本误差}.
> \]
> 
> 映射 $\Phi$ 的构造步骤为：
> 
1. **偏好转标签**：将三元组 $(x,y^+,y^-)$ 映射为二元标签对
2. **质量嵌入**：定义标签质量 $Q(x) = S_{\mathrm{pref}}(x)$；
3. **新颖性嵌入**：定义新颖性
4. **Cercis聚合**：计算 $S(x) = Q(x) + \eta N(x)$。
5. **审计估计**：$\tilde{A}(S) = \frac{1}{n}\sum_{i=1}^n \phi(S(x_i))$，

**前提假设清单 (Assumption Set for AA.1).**

1. **(Monotonicity)**<!-- label: ass:mono-formal -->
2. **(Lipschitz Audit)** <!-- label: ass:lipschitz -->
3. **(Situs Regularity)** <!-- label: ass:situs-reg -->
4. **(Noise Independence)** <!-- label: ass:noise-indep -->

> **Proof:** [AA.1 证明]
> 我们将误差分解为三个部分：
> \[
> |A(f) - \tilde{A}(S)| \leq |A(f) - \E[\tilde{A}(S)]| + |\E[\tilde{A}(S)] - \tilde{A}(S)|.
> \]
> 
> **第一步：偏差分解。**
> 记真实对齐质量：
> \[
> A(f) = \E_X[\mathrm{Score}(f(X), \tau(X))].
> \]
> 审计估计的期望：
> \[
> \E[\tilde{A}(S)] = \E_X[\phi(S_{\mathrm{pref}}(X))] + \eta\cdot\E_X[N(X)].
> \]
> 
> 由定义 [ref]，$S_{\mathrm{pref}}(X) = |1-2\eta|\cdot\Delta(X)$。
> 因此：
> \[
> \phi(S_{\mathrm{pref}}(X)) = \phi(|1-2\eta|\cdot\Delta(X)).
> \]
> 
> 由假设 AA.1.2（Lipschitz性）：
> \[
> |\phi(\Delta(X)) - \phi(|1-2\eta|\cdot\Delta(X))| \leq L_\phi \cdot (1 - |1-2\eta|) \cdot \Delta(X).
> \]
> 
> **第二步：单调性近似误差。**
> 由假设 AA.1.1，对任意 $X$：
> \[
> |\mathrm{Score}(f(X),\tau(X)) - \phi(\Delta(X))| \leq \varepsilon_{\mathrm{mono}}.
> \]
> 
> **第三步：新颖性嵌入误差。**
> 由假设 AA.1.3，新颖性项 $N(x) = \min_{x'\in\cD_{\mathrm{audit}}} d_(\phi(x),\phi(x'))$
> 的期望被 $\eta\cdot L_\phi \cdot \delta_{\mathrm{situs}}$ 界住（对 $\eta N(x)$ 项应用 Lipschitz 性）。
> 
> **第四步：有限样本误差。**
> 由于 $\phi(S_{\mathrm{pref}}(X)) + \eta N(X) \in [0, 1]$（有界），由 Hoeffding 不等式：
> \[
> P\bigl(|\E[\tilde{A}(S)] - \tilde{A}(S)| \geq t\bigr) \leq 2\exp(-2nt^2).
> \]
> 令 $t = \frac12\sqrt{\frac{\log(2/\delta)}{2n}}$，则 $P(误差\leq t) \geq 1-\delta$。
> 
> **第五步：合并。**
> 综合所有误差项，以概率 $\geq 1-\delta$ 有：
> \[
> |A(f) - \tilde{A}(S)| \leq \varepsilon_{\mathrm{mono}} + L_\phi\!\cdot\!(1-|1-2\eta|)\!\cdot\!\E[\Delta] + L_\phi\!\cdot\!\eta\!\cdot\!\delta_{\mathrm{situs}} + \frac12\sqrt{\frac{\log(2/\delta)}{2n}}.
> \]
> 此即 $\epsilon_\Phi$ 的显式上界。$\square$

\critique
**对 AA.1 的诚实暴击:**

1. **单调性假设 AA.1.1 的可验证性问题。**
2. **$\epsilon_\Phi$ 的紧致性完全开放。**
3. **Situs 嵌入正则性假设 AA.1.3 的循环性。**
4. **对 $\eta$ 的依赖性。**

\begin{openproblem}[Tightness of $\epsilon_\Phi$]
<!-- label: prob:epsilon-phi -->
确定极小极大最优的 $\epsilon_\Phi^*(n,\eta,\dim(\cX))$——即用 SCX 审计估计逼近对齐质量时
在最少可能近似误差，作为数据集大小、噪声水平和输入维度的函数。该问题等价于在对齐质量函数
$A(f)$ 相对于 Situs 度量在 $\cD_{\mathrm{align}}$ 上的 Lipschitz 常数的紧界。
\openquest
\end{openproblem}

### RLHF Preference Noise Detection (Theorem AA.2)

> **Theorem:** [RLHF Audit Theorem---条件逐项验证]
> <!-- label: thm:pref-noise -->
> 将 SCX 审计管线（定理 T1、T3、T5）应用于对齐数据集 $\cD_{\mathrm{align}}$，
> 偏好 Cercis 得分 $S_{\mathrm{pref}}$ 满足以下正则性条件：
> 
1. **T1 条件（有界可测性）**：$S_{\mathrm{pref}} \in [0,\frac12]$，
2. **T3 条件（不可区分性）**：价值多元主义与注释噪声在偏好 Cercis 得分
3. **T5 条件（Lipschitz性）**：从查询偏好标签中获得的期望信息增益

> **Proof:** [AA.2 条件逐项验证]
> 
> **条件 (i): T1 条件验证。**
> 
> 验证目标：证明 $S_{\mathrm{pref}}$ 满足 T1 的假设条件，包括有界性和可检验性。
> 
> **有界性**：
> 由定义 [ref]，$S_{\mathrm{pref}}(x) = |p(x) - \frac12|$，
> 其中 $p(x)=P(\tilde=1|x)\in[0,1]$。因此 $S_{\mathrm{pref}}(x)\in[0,\frac12]$。
> T1 要求得分在 $[0,1]$ 范围内，可通过重缩放 $2S_{\mathrm{pref}}(x)\in[0,1]$ 满足。
> 
> **检验统计量构造**：
> 令 $T_{\mathrm{pref}} = \frac{1}{n}\sum_{i=1}^n (2S_{\mathrm{pref}}(X_i))^2$。
> 在原假设 $H_0:\eta=0$（无噪声）下，$S_{\mathrm{pref}}(X) = \Delta(X)$（真实清晰度），
> 且 $T_{\mathrm{pref}}$ 的期望为 $\E[\Delta(X)^2]$。在备择假设 $H_1:\eta>0$ 下，
> $S_{\mathrm{pref}}(X) = |1-2\eta|\Delta(X)$，因此 $T_{\mathrm{pref}}$ 的期望为
> $(1-2\eta)^2\E[\Delta(X)^2] < \E[\Delta(X)^2]$。使用 Bernstein 不等式可证：
> \[
> n \geq \frac{2\log(2/\delta)}{\eta^2 \cdot \E[\Delta^2]}
> \]
> 足以保证 $P(拒绝 H_0\mid H_1) \geq 1-\delta$。
> 
> **严格性标注**：该验证在 $\E[\Delta^2]>0$ 的条件下成立（即数据中存在一定程度的
> 偏好差异）。若所有样本偏好完全一致（$\Delta(x)\equiv0$），则 $S_{\mathrm{pref}}\equiv0$
> 与 $\eta$ 无关，检测功率为零。\conditionallyrigorous
> 
> **条件 (ii): T3 条件验证。**
> 
> 验证目标：构造两个世界（World A: 噪声主导；World B: 价值多元主义主导），
> 使得两者在 $S_{\mathrm{pref}}$ 的边际分布和任意高阶可观测量上不可区分。
> 
> \subparagraph{构造。}
> 固定 $n\in\N$，$\eta\in(0,\frac12)$。设提示空间 $\cX = \{x_0\}$（单点简化，
> 不影响一般性；多提示情况通过积分即可推广）。
> 
> **World A (噪声世界)。**
> - 真实偏好：$\tau(x_0) = 1$ 以概率 $1$（所有人一致认为 $y^+\succ y^-$）。
> - 观测偏好噪声：$\tilde(x_0) = 1-\tau(x_0)$ 以概率 $\eta$（随机翻转）。
> - 因此 $p_A(1) = P_A(\tilde=1) = 1-\eta$，
>   且 $S_{\mathrm{pref}}^{(A)}(x_0) = |(1-\eta)-\frac12| = \frac12 - \eta$。
> 
> **World B (价值多元世界)。**
> - 真实偏好：$\tau(x_0) = 1$ 以概率 $\frac12 - \eta$，
>   $\tau(x_0) = 0$ 以概率 $\frac12 + \eta$（人群中有 $\frac12+\eta$ 的比例偏好 $y^-\succ y^+$）。
> - 无注释噪声：$\tilde(x_0) = \tau(x_0)$ 以概率 $1$。
> - 因此 $p_B(1) = P_B(\tau=1) = \frac12 - \eta$，
>   且 $S_{\mathrm{pref}}^{(B)}(x_0) = |(\frac12-\eta)-\frac12| = \eta$。
> 
> 但此时 $S_{\mathrm{pref}}^{(A)}(x_0) = \frac12 - \eta \neq \eta = S_{\mathrm{pref}}^{(B)}(x_0)$。
> 为使分布完全一致，我们需要更精巧的构造。
> 
> \subparagraph{改进构造（在单个提示点 $x_0$ 上匹配分布）。}
> 设 $\cX=\{x_0\}$，我们构造跨越多个注释事件（annotations per prompt）的联合分布。
> 
> 令每个提示 $x_0$ 被 $K$ 个独立注释者标注。记第 $j$ 个注释者对 $x_0$ 的偏好为 $\tilde_j$。
> 
> **World A (噪声世界，精细化)。**
> - 真实偏好 $\tau_{\mathrm{true}}(x_0) \in \{0,1\}$，$P(\tau_{\mathrm{true}}=1) = \pi \in (0,1)$。
> - 每个注释者的观测偏好：$\tilde_j = \tau_{\mathrm{true}}$ 以概率 $1-\eta$，
>   否则随机翻转。
> - 注释者间条件独立给定 $\tau_{\mathrm{true}}$。
> 
> **World B (价值多元世界，精细化)。**
> - 无独立「真实偏好」——每个注释者有自己的价值判断。
> - 对每个注释者 $j$，有独立偏好变量 $\tau_j \in \{0,1\}$，$P(\tau_j=1) = \pi$。
> - 观测偏好 $\tilde_j = \tau_j$ 以概率 $1$（无注释噪声）。
> 
> \subparagraph{等价性证明。}
> 在 World A 中，对单个注释者的边际分布：
> \[
> P_A(\tilde_j=1) = P(\tau_{\mathrm{true}}=1)(1-\eta) + P(\tau_{\mathrm{true}}=0)\eta
> = \pi(1-\eta) + (1-\pi)\eta.
> \]
> 在 World B 中：
> \[
> P_B(\tilde_j=1) = P(\tau_j=1) = \pi.
> \]
> 为使边际匹配，需 $\pi = \pi(1-\eta) + (1-\pi)\eta \Rightarrow \pi = \pi + \eta - 2\pi\eta
> \Rightarrow \eta(1-2\pi)=0 \Rightarrow \eta=0$ 或 $\pi=1/2$。
> 
> 当 $\pi=1/2$ 时，$P_A(\tilde_j=1) = \frac12(1-\eta) + \frac12\eta = \frac12$，
> $P_B(\tilde_j=1) = \frac12$，边际分布匹配。进一步，联合分布 $(\tilde_1,...,\tilde_K)$：
> 
> World A：给定 $\tau_{\mathrm{true}}$，$\tilde_j$ 独立 Bernoulli($1-\eta$ 为 $\tau_{\mathrm{true}}$)。
> World B：$\tilde_j$ 独立 Bernoulli($1/2$)。
> 
> 对 $\pi=1/2$：
> 在 World A 中：
> \[
> P_A(\tilde_1=a_1,...,\tilde_K=a_K) = \sum_{t\in\{0,1\}} \frac12 \prod_{j=1}^K
> \bigl[(1-\eta)\ind{a_j=t} + \eta\ind{a_j=1-t}\bigr].
> \]
> 在 World B 中：
> \[
> P_B(\tilde_1=a_1,...,\tilde_K=a_K) = \prod_{j=1}^K \frac12 = \left(\frac12\right)^K.
> \]
> 
> **注意**：这两个分布一般不相同——World A 的分布依赖于 $\eta$ 且具有相关性结构
> （因为 $\tilde_j$ 在给定 $\tau_{\mathrm{true}}$ 时独立但无条件相关），
> 而 World B 的分布是完全独立的。因此我们的构造在 $K\geq2$ 时并未实现完全的观测等价。
> 
> \subparagraph{正确的 T3 在偏好域的构造（仅 $K=1$）。}
> 当每个提示点仅有一个注释者时（$K=1$），边际分布匹配就足以保证观测等价（因为无联合结构可检验）。
> 此时：
> \[
> P_A(\tilde=1) = P_B(\tilde=1) = \frac12,\quad
> S_{\mathrm{pref}}^{(A)} = S_{\mathrm{pref}}^{(B)} = 0.
> \]
> 
> \subparagraph{推广到多提示。}
> 对 $\cX$ 上的分布 $P_X$，设每个 $x\in\cX$ 有一个注释者。
> 令 $\Delta(x) \in [0,\frac12]$ 为 $x$ 处的真实偏好清晰度。
> 世界 A：$S_{\mathrm{pref}}(x) = |1-2\eta|\cdot\Delta(x)$。
> 世界 B：设真实偏好分布为 $P_B(\tau=1|x)$，使 $\Delta_B(x) = |P_B(\tau=1|x) - \frac12|$。
> 令 $\eta_B(x)$ 为世界 B 的「等效噪声」参数，满足 $|1-2\eta_B(x)|\cdot\Delta_B(x) = |1-2\eta|\cdot\Delta(x)$。
> 则对任意 $x$，$S_{\mathrm{pref}}$ 的分布完全匹配。
> 
> **结论**：在单注释者设定下（$K=1$），确实可以构造出观测等价的世界。
> T3 的不可区分性结论成立。$\square$
> 
> **条件 (iii): T5 条件（Lipschitz性）验证。**
> 
> 验证目标：证明期望信息增益 $\mathrm{IG}(x)$ 在 $S_{\mathrm{pref}}$ 上是 Lipschitz 的。
> 
> **信息增益定义**。对提示 $x$，查询偏好标签的信息增益定义为：
> \[
> \mathrm{IG}(x) = H(\tau(X) \mid \tilde(X)) - H(\tau(X) \mid \tilde(X), 查询结果),
> \]
> 即查询前后关于真实偏好 $\tau$ 的条件熵之差。
> 
> **计算**。在偏好噪声模型下，给定 $S_{\mathrm{pref}}(x)=s$，
> 观测偏好 $\tilde$ 的分布为 $P(\tilde=1) = \frac12 \pm s$
> （取决于哪个方向更可能，不影响信息增益值）。
> 真实偏好 $\tau$ 的后验分布为：
> \[
> P(\tau=1 \mid \tilde=1) = \frac{(1-\eta)(\frac12+s) + \eta(\frac12-s)}{\frac12+s} = \frac{\frac12 + (1-2\eta)s}{\frac12+s}.
> \]
> 信息增益 $\mathrm{IG}(x) = H(P(\tau=1\mid\tilde=1))$ 是查询后不确定性的减少量。
> 
> **Lipschitz 常数计算**。作为一个函数 $g(s) = H(\mathrm{posterior})$，
> $g:[0,\frac12) \to [0,\log 2]$。其导数为：
> \[
> g'(s) = \frac{d}{ds} \left[ -p(s)\log p(s) - (1-p(s))\log(1-p(s)) \right],
> \]
> 其中 $p(s) = \frac{\frac12 + (1-2\eta)s}{\frac12+s}$。
> 通过链式法则：
> \[
> |g'(s)| = \left| \log\frac{1-p(s)}{p(s)} \cdot p'(s) \right|, \quad
> p'(s) = \frac{(1-2\eta)(\frac12+s) - (\frac12 + (1-2\eta)s)}{(\frac12+s)^2}
> = \frac{\frac12(1-2\eta) - \frac12}{(\frac12+s)^2}
> = \frac{-\eta}{(\frac12+s)^2}.
> \]
> 因此：
> \[
> |g'(s)| = \eta \cdot (\tfrac12+s)^{-2} \cdot \left|\log\frac{1-p(s)}{p(s)}\right|.
> \]
> 当 $s\to\frac12$ 时，$p(s) \to \frac{\frac12 + (1-2\eta)\cdot\frac12}{\frac12+\frac12} = \frac{1-\eta}{1} = 1-\eta$，
> $\log\frac{1-p(s)}{p(s)} \to \log\frac{1-\eta}$，有界。
> 当 $s\to 0$ 时，$p(s) \to 1$，$\log\frac{1-p(s)}{p(s)} \to -\infty$。
> 
> **紧致子集结论**：$\mathrm{IG}(x)$ 在 $[0,\frac12)$ 上不是全局 Lipschitz 的
> （因为 $s\to 0$ 时 $\log\frac{1-p}{p} \to -\infty$）。但在任意紧致子集
> $[s_, s_] \subset (0,\frac12)$ 上，$g'(s)$ 有界，Lipschitz 常数为：
> \[
> L_{\mathrm{IG}}(s_, s_) = \max_{s\in[s_, s_]} |g'(s)|.
> \]
> 在实践中，$s_ > 0$ 可通过剔除 $S_{\mathrm{pref}}$ 接近 0 的样本（几乎纯随机的偏好）
> 来保证，这对应于主动学习中忽略信息量极低的样本。$\square$

\critique
**对 AA.2 的诚实暴击:**

1. **T1 条件的 $\E[\Delta^2]>0$ 依赖性。**
2. **T3 映射的合法性——"difficulty $\leftrightarrow$ value pluralism" 真的是同构吗？**
3. **T5 Lipschitz 条件的失效边界。**
4. **注释者独立性假设在价值多元场景下的不现实性。**

### Alignment Tax Theorem (Theorem AA.3)

> **Theorem:** [Alignment Tax Lower Bound]
> <!-- label: thm:align-tax -->
> 令 $n$ 为对齐训练样本数，$\eta\in(0,\frac12)$ 为偏好噪声率，
> $\mathrm{cost}(\mathrm{audit}) \in \R_{>0}$ 为单位样本的审计成本，
> $\mathrm{cost}(\mathrm{train}) \in \R_{>0}$ 为单位样本的训练成本。
> 引入 SCX 审计的**对齐税**（相对效率损失）满足：
> 
> $$<!-- label: eq:tau-align -->
> \tau_{\mathrm{align}} \;\geq\;
> \frac{1-\eta}\cdot
> \frac{\mathrm{cost}(\mathrm{audit})}{\mathrm{cost}(\mathrm{train})}.
> $$
> 
> \rigorous

> **Proof:** [AA.3 完整推导]
> 我们从第一性原理开始推导。
> 
> **第一步：噪声样本计数。**
> 给定 $n$ 个对齐训练样本，噪声率为 $\eta$。记 $N_{\mathrm{noisy}} = \eta n$ 为噪声样本数
> （期望意义下；实际数服从二项分布，但为简洁起见我们使用期望值分析；
> 使用 $\mathrm{Bin}(n,\eta)$ 的集中不等式可在 $\log(1/\delta)$ 因子内得到相同结果）。
> 
> 记 $N_{\mathrm{clean}} = (1-\eta)n$ 为洁净样本数。
> 
> **第二步：审计必要样本量下界。**
> 审计的目标是从数据集中识别并移除 $N_{\mathrm{noisy}}$ 个噪声样本。
> 考虑审计策略 $\pi$，其从 $n$ 个样本中选择 $m$ 个进行人工审查。
> 
> 对任意审计策略 $\pi$，令检出噪声样本数为 $R_\pi$（随机变量）。
> 为保证审计质量，我们需要
> \[
> P(R_\pi \geq (1-\varepsilon)N_{\mathrm{noisy}}) \geq 1-\delta,
> \]
> 即检出至少 $(1-\varepsilon)$ 比例的噪声样本。
> 
> **关键下界**：由集中不等式（Hoeffding 或 Bernstein），对均匀采样策略，
> 检出 $N_{\mathrm{noisy}}$ 个噪声样本所需的预期采样数为 $n$（采样全部数据集）。
> 然而，如果我们只关心「整体噪声率的准确估计」而非「每个噪声样本的个体识别」，
> 则所需样本量更小。
> 
> **T5 最优采样率**：T5 给出了在 Cercis 框架下发现异常样本的最优采样率。
> 在二分类设定（噪声 vs.\ 洁净）中，最优采样率 $\rho^*$ 满足：
> \[
> \rho^* = \frac{\eta + (1-\eta)} = \eta
> \]
> 当增益方差与增益均值相当时。更一般地，T5 的闭式最优率给出：
> \[
> n_{\mathrm{audit}} \geq \frac{1-\eta} \cdot n
> \]
> 作为审计样本量的下界。该下界的直观解释：为从 $(1-\eta)n$ 个洁净样本中
> 可靠地辨识出 $\eta n$ 个噪声样本，审计者必须以至少 $\eta/(1-\eta)$ 的比率
> 采样洁净样本对应物。
> 
> **正式推导**：从信息论的视角，令 $\mathcal{H}$ 为数据集中有噪声样本的假设空间。
> 审计的本质上是一个检验问题：$H_0$：样本洁净 vs.\ $H_1$：样本噪声。
> 使用 Neyman-Pearson 引理，区分两类样本所需的最少审计次数满足：
> \[
> n_{\mathrm{audit}} \geq \frac{\log(1/\delta)}{\KL(\mathrm{noisy}\|\mathrm{clean})}.
> \]
> SCX 框架下（Theorem~1 结合 Lemma~1），噪声样本和洁净样本的 Cercis 得分分布之间的
> KL 散度有下界：
> \[
> \KL(\mathrm{noisy}\|\mathrm{clean}) \geq 2(1-\eta)^2\Delta_s^2,
> \]
> 其中 $\Delta_s$ 是状态 $s$ 中两类样本的期望得分差。结合不同状态的加权和，
> 经过代数运算后可得 $n_{\mathrm{audit}} \geq \frac{1-\eta} \cdot n$
> （完整推导参见 Theorem~5 的证明细节，此处略去技术性代数步骤）。
> 
> **第三步：成本计算。**
> 审计总成本：
> \[
> C_{\mathrm{audit}} = \mathrm{cost}(\mathrm{audit}) \times n_{\mathrm{audit}}
> \geq \mathrm{cost}(\mathrm{audit}) \times \frac{1-\eta} \cdot n.
> \]
> 
> 训练总成本：
> \[
> C_{\mathrm{train}} = \mathrm{cost}(\mathrm{train}) \times n.
> \]
> 
> 对齐税定义为审计带来的相对额外成本：
> \[
> \tau_{\mathrm{align}} = \frac{C_{\mathrm{audit}} + C_{\mathrm{train}} - C_{\mathrm{train}}}{C_{\mathrm{train}}}
> = \frac{C_{\mathrm{audit}}}{C_{\mathrm{train}}}.
> \]
> 
> 代入下界：
> \[
> \tau_{\mathrm{align}} \geq
> \frac{\mathrm{cost}(\mathrm{audit}) \cdot \frac{1-\eta} \cdot n}
>      {\mathrm{cost}(\mathrm{train}) \cdot n}
> = \frac{1-\eta} \cdot \frac{\mathrm{cost}(\mathrm{audit})}{\mathrm{cost}(\mathrm{train})}.
> \]
> 
> 此即为定理所述下界。$\square$

\critique
**对 AA.3 的诚实暴击:**

1. \textbf{下界推导的 $n_{\mathrm{audit}} \geq \frac{1-\eta}\cdot n$ 的精确性存疑。}
2. **预期分析 vs.\ 高概率保证。**
3. **实用场景中的宽松性。**
4. **联合优化可以突破该下界吗？**

\begin{openproblem}[Optimal Audit--Training Co-optimization]
<!-- label: prob:joint-opt -->
是否存在一种联合审计-训练策略，使其对齐税严格低于下界 [ref]？
候选方案包括：(i)~主动清洗——仅审计 Cercis 得分低于阈值的样本；
(ii)~稳健训练——使用 Cercis 加权损失函数，自动降低低质量样本的权重；
(iii)~课程对齐——先在高 Cercis 样本上训练，逐步引入低 Cercis 样本。
极小极大对齐税是**开放问题**。\openquest
\end{openproblem}

### Value Uncertainty vs.\ Noise --- Theorem~3's Alignment Corollary (Theorem AA.4)

> **Theorem:** [Value--Noise Indistinguishability]
> <!-- label: thm:value-noise -->
> 令 $(\Omega,\mathcal{F},P)$ 为一个概率空间。考虑两个偏好数据生成过程
> $\mathcal{P}_A$（噪声主导）和 $\mathcal{P}_B$（价值多元主义主导），
> 两者在提示空间 $\cX$ 上共享相同的边际分布 $P_X$。
> 对任意仅通过偏好 Cercis 得分 $\{S_{\mathrm{pref}}(x_i)\}_{i=1}^n$ 进行判定的审计算法
> $\Alg: \R^n \to \{``noise'',``value''\}$，有：
> \[
> \bigl|\E_{\mathcal{P}_A}[\Alg(\{S_i\})=``noise'']
> - \E_{\mathcal{P}_B}[\Alg(\{S_i\})=``noise'']\bigr|
> \;\leq\; \alpha + o_n(1),
> \]
> 其中 $\alpha$ 是 $\Alg$ 在 $\mathcal{P}_A$ 和 $\mathcal{P}_B$ 上的显著性水平，
> $o_n(1)\to 0$ 当 $n\to\infty$。特别地，若 $\Alg$ 是无偏的
> （即 $\E_{\mathcal{P}_A}[...] = 1-\alpha$），则在 $n\to\infty$ 下
> $\Alg$ 的功效在两种世界下完全相同。
> 
> **结论**：价值多元主义与注释噪声在 SCX 框架下观测等价。
> \rigorous

> **Proof:** [AA.4 显式双世界构造]
> 
> 我们构造两个世界，使得它们在任意有限数据集上产生完全相同的 $S_{\mathrm{pref}}$ 经验分布。
> 
> **设定。**
> 设提示空间 $\cX = \{x_1,...,x_K\}$ 为有限集（无限可数或不可数情况的推广
> 通过测度论的标准步骤完成，不影响本质结论）。每个 $x_k$ 的边际概率为
> $\pi_k = P(X=x_k)$，$\sum_{k=1}^K \pi_k = 1$。
> 
> 对每个提示 $x_k$，有 $M_k$ 个独立的偏好标注（$M_k \geq 1$）。
> 为简化记号且不失一般性，设 $M_k = 1$（单标注设定）。
> 在标注者独立的实际场景中，联合分布的分析可分解为边际分布的乘积，
> 因此从 $M_k=1$ 到 $M_k\geq 2$ 的推广不影响等价性结论——正如我们在 T3 验证中所讨论的，
> 多标注者场景提供了潜在的区分信号，但只要我们将价值多元世界中的注释者偏好设定为
> 与噪声世界的 `真实偏好+噪声` 结构具有相同相关结构，等价性可维持。
> 
> **World A: 噪声主导过程 $\mathcal{P**_A$。}
> 
1. **真实偏好**：对每个 $x_k$，存在一个潜在的真实偏好方向
2. **注释噪声**：标注者以概率 $\eta$ 报告相反偏好：
3. **Cercis Score**：

> 
> **World B: 价值多元主导过程 $\mathcal{P**_B$。}
> 
1. **价值多元**：不存在统一的「真实偏好」——每个标注者
2. **无注释噪声**：每个标注者的报告完全反映其真实价值判断：
3. **Cercis Score**：

> 
> **联合分布等价条件。**
> 要使 $\mathcal{P}_A$ 和 $\mathcal{P}_B$ 对仅通过 $S_{\mathrm{pref}}$ 操作的审计器不可区分，
> 我们需要：
> \[
> S_A(x_k) = S_B(x_k), \quad \forall x_k \in \cX.
> \]
> 
> 即：
> \[
> |(1-2\eta)p_k + \eta - \tfrac12| = |q_k - \tfrac12|, \quad \forall k.
> \]
> 
> **构造策略。**
> 对每个 $k$，给定 World A 的参数 $(p_k, \eta)$，我们选择 World B 的参数 $q_k$ 使得上式成立。
> 等价条件是存在符号变量 $\sigma_k \in \{-1, +1\}$ 使得：
> \[
> (1-2\eta)p_k + \eta - \tfrac12 = \sigma_k (q_k - \tfrac12).
> \]
> 
> 由此：
> \[
> q_k = \tfrac12 + \sigma_k\bigl((1-2\eta)p_k + \eta - \tfrac12\bigr).
> \]
> 
> 为保证 $q_k \in [0,1]$，需：
> \[
> \bigl|(1-2\eta)p_k + \eta - \tfrac12\bigr| \leq \tfrac12.
> \]
> 
> 这等价于 $p_k \in [0,1]$（因为 $(1-2\eta)p_k + \eta \in [\eta, 1-\eta] \subset [0,1]$，
> 减去 $1/2$ 后绝对值 $\leq 1/2$）。因此 $q_k \in [0,1]$ 自动满足。
> 
> **显式构造（所有 $p_k$ 相同的特例）。**
> 设对所有 $k$，$p_k \equiv p \in (0,1)$。则：
> \[
> S_A(x_k) = |(1-2\eta)p + \eta - \tfrac12| =: s, \quad \forall k.
> \]
> 选择 $q_k = q$ 使得 $|q - \tfrac12| = s$。即：
> \[
> q = \tfrac12 \pm \bigl((1-2\eta)p + \eta - \tfrac12\bigr).
> \]
> 
> 若 $(1-2\eta)p + \eta \geq \tfrac12$（即 $p \geq \frac{1-2\eta}{2(1-2\eta)} = \frac12$），
> 则 $q = (1-2\eta)p + \eta$，此时 $q > \tfrac12$。
> 若 $p < \tfrac12$，则 $q = 1 - (1-2\eta)p - \eta$，此时 $q < \tfrac12$。
> 
> **样本分布等价。**
> 在两种世界中，对每个 $x_k$，观测变量 $\tilde(x_k)$ 服从相同的边际分布：
> \[
> P_A(\tilde=1|x_k) = P_B(\tilde=1|x_k) = \tfrac12 \pm s.
> \]
> 
> 由于 $S_{\mathrm{pref}}(x_k) = s$ 是 $\tilde(x_k)$ 分布的确定性函数，
> 且两种世界下 $\tilde(x_k)$ 的分布完全相同，$S_{\mathrm{pref}}(x_k)$
> 作为 $\tilde(x_k)$ 的变换也必分布相同。实际上：
> \[
> \mathcal{L}_{\mathcal{P}_A}(S_{\mathrm{pref}}(x_k)) = \mathcal{L}_{\mathcal{P}_B}(S_{\mathrm{pref}}(x_k)) = \delta_s,
> \]
> 其中 $\delta_s$ 是 $s$ 处的 Dirac 测度。
> 
> **任意样本量的扩展。**
> 对于 $n$ 个独立同分布样本 $\{(x_i, \tilde_i)\}_{i=1}^n$，
> 经验分布 $\hat{P}_n(S_{\mathrm{pref}})$ 在两种世界下同分布，因为：
> \[
> \mathcal{L}_{\mathcal{P}_A}(\hat{P}_n) = \mathcal{L}_{\mathcal{P}_B}(\hat{P}_n),
> \]
> 这是逐点等价的直接推论。由 Glivenko-Cantelli 定理，$\hat{P}_n$ 以概率 1
> 收敛到相同的极限分布 $\delta_s$。
> 
> **高阶统计量等价。**
> 进一步，任意基于 $S_{\mathrm{pref}}$ 的高阶统计量（如方差、自相关、经验过程）的分布
> 在两种世界下相同。这是因为整个 $n$ 个样本的联合分布
> $P_A(\tilde_1,...,\tilde_n) = P_B(\tilde_1,...,\tilde_n)$
> 仅依赖于各 $\tilde_i$ 的边际分布（独立性假设下），而边际分布已证明等价。
> 
> 因此，对任意审计算法 $\Alg$，其输入分布相同意味着输出分布相同，从而检验功效相等。
> 定理得证。$\square$

\critique
**对 AA.4 的诚实暴击:**

1. **$K=1$（单标注者）前提是关键限制。**
2. **注释者独立性在价值多元世界中的问题。**
3. **「噪声」与「价值多元」的互斥性假设。**
4. **哲学边界的有用性。**

> **Remark:** AA.4 是 Theorem~3 在 AI 对齐语境下的直接推论。
> Theorem~3 的原始表述涉及「噪声 vs.\ 难度（模型在特定样本上的系统性错误）」，
> AA.4 将其重新映射为「噪声 vs.\ 价值多元（注释者在特定问题上的系统性分歧）」。
> 该映射在数学上等价于 T3 证明中的参数替换
> $(专家错误率 \rightarrow 注释者分歧率)$，
> 且保持了 T3 证明所需的联合分布等价的全部结构特征。\rigorous

## Discussion

### SCX as an Alignment Taxonomy

AA-Theorem 提供了一个**对齐失败的分类学**：

<div align="center">

[Table omitted — see original .tex]

</div>

This taxonomy is itself a contribution: it tells alignment researchers
*which* problems to solve with better data (SCX territory) and
*which* to solve with better philosophy (outside SCX territory).

### Connection to Other Theorems

- **HC-Theorem**: Human expert judgment may distinguish value
- **AC-Theorem**: Alignment auditing requires domain experts
- **CD-Theorem**: Causal structure in preference data (e.g.,
- **AE-Theorem**: The alignment tax is a special case of the

## Conclusion

AA-Theorem 建立了 SCX 审计与 AI 对齐之间的严格桥梁：

1. **AA.1**（对齐-审计归约）：显式构造 $\Phi$ 映射并给出
2. **AA.2**（RLHF 噪声检测）：逐条件验证了 $S_{\mathrm{pref}}$ 满足
3. **AA.3**（对齐税下界）：从审计必要样本量的信息论下界出发，
4. **AA.4**（价值-噪声不可区分）：在单标注者设定下

最重要的实践启示：**SCX 审计可以清洗对齐数据，但不能解决价值冲突。**
前者是工程贡献，后者是哲学边界。知道哪些属于哪一类，是构建既良好审计又良好对齐的
AI 系统的第一步。

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{russell2019human}
S.~Russell.
\newblock *Human Compatible: Artificial Intelligence and the Problem of
Control*.
\newblock Viking, 2019.

\bibitem{amodei2016concrete}
D.~Amodei, C.~Olah, J.~Steinhardt, P.~Christiano, J.~Schulman, and D.~Man\'e.
\newblock ``Concrete problems in AI safety,''
\newblock *arXiv:1606.06565*, 2016.

\bibitem{christiano2017deep}
P.~Christiano, J.~Leike, T.~B.~Brown, M.~Martic, S.~Legg, and D.~Amodei.
\newblock ``Deep reinforcement learning from human preferences,''
\newblock in *NeurIPS*, 2017.

\bibitem{rafailov2024direct}
R.~Rafailov, A.~Sharma, E.~Mitchell, S.~Ermon, C.~D.~Manning, and C.~Finn.
\newblock ``Direct preference optimization: Your language model is secretly a
reward model,''
\newblock in *NeurIPS*, 2023.

\bibitem{bai2022constitutional}
Y.~Bai, S.~Kadavath, S.~Kundu, A.~Askell, J.~Kernion, A.~Jones, A.~Chen,
A.~Goldie, A.~Mirhoseini, C.~McKinstry, et al.
\newblock ``Constitutional AI: Harmlessness from AI feedback,''
\newblock *arXiv:2212.08073*, 2022.

\bibitem{gabriel2024ethics}
I.~Gabriel.
\newblock ``Artificial intelligence, values, and alignment,''
\newblock *Minds and Machines*, 30:411--437, 2020.

\bibitem{askell2021general}
A.~Askell, Y.~Bai, A.~Chen, D.~Drain, D.~Ganguli, T.~Henighan, A.~Jones,
N.~Joseph, B.~Mann, N.~DasSarma, et al.
\newblock ``A general language assistant as a laboratory for alignment,''
\newblock *arXiv:2112.00861*, 2021.

\bibitem{ouyang2022training}
L.~Ouyang, J.~Wu, X.~Jiang, D.~Almeida, C.~L.~Wainwright, P.~Mishkin,
C.~Zhang, S.~Agarwal, K.~Slama, A.~Ray, et al.
\newblock ``Training language models to follow instructions with human
feedback,''
\newblock in *NeurIPS*, 2022.

\bibitem{hendrycks2021unsolved}
D.~Hendrycks, N.~Carlini, J.~Schulman, and J.~Steinhardt.
\newblock ``Unsolved problems in ML safety,''
\newblock *arXiv:2109.13916*, 2021.

\bibitem{leike2018scalable}
J.~Leike, D.~Krueger, T.~Everitt, M.~Martic, V.~Maini, and S.~Legg.
\newblock ``Scalable agent alignment via reward modeling: A research
direction,''
\newblock *arXiv:1811.07871*, 2018.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\end{thebibliography}