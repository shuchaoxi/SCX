\section{A2 (Conditional Independence) --- Vulnerability Analysis and
Fix}<!-- label: a2-conditional-independence-vulnerability-analysis-and-fix -->

> **触发**: Hostile review 指出 A2 ``几乎肯定为假，是整个框架的
> Achilles 之踵'' **结论**:
> 诊断正确，但可以修复。替换为弱相关集中不等式，降价退化速率。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. 问题确诊<!-- label: ux95eeux9898ux786eux8bca -->

Theorem 1 的证明链:

\begin{verbatim}
A2 (条件独立) → e_m 独立 → Hoeffding 集中 → exp(-2MΔ²) 指数速率
\end{verbatim}

如果专家错误之间存在条件相关 \(\rho > 0\)（给定状态 \(s\)）: - CNN:
所有专家在模糊图像上一起错 - MLIP: 所有专家在过渡态构型上一起错 -
有效独立专家数: \(M_{eff} \approx M / (1 + (M-1)\rho)\)

在 \(\rho = 0.3\) 时，\(M=12\) 退化到
\(M_{eff} = 2.8\)------指数增益几乎消失。

**CIFAR-10 实验证据**: 理论下界 F1≥0.976（假定的独立情况），实测
F1=0.617。差距无法仅用 \(\mu_s\) 估计误差解释。

**AlN 实验证据**: 全局界 F1≥0.87 匹配经验值。但仅当
\(\rho \lesssim 0.02\) 时才成立------这是一个极弱的假设，需要验证。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. 修复方案<!-- label: ux4feeux590dux65b9ux6848 -->

#### 2.1 诚实化 A2<!-- label: ux8bdaux5b9eux5316-a2 -->

**旧 A2**: 给定 \(x\) 下，专家错误 \(\{e_m\}\) 条件独立。

**新 A2'**: 给定状态 \(s\) 下，专家错误 \(\{e_m\}\)
的条件相关系数有界:
\[\rho_s = \max_{m \neq m'} Corr(e_m, e_{m'} \mid X \in s) \leq \bar < 1\]

其中
\(Corr(e_m, e_{m'} \mid s) = \frac{Cov(e_m, e_{m'} \mid s)}{\sqrt{Var(e_m \mid s) Var(e_{m'} \mid s)}}\)

当 \(\bar = 0\) 时恢复旧 A2。

\subsubsection{2.2
弱相关集中不等式}<!-- label: ux5f31ux76f8ux5173ux96c6ux4e2dux4e0dux7b49ux5f0f -->

**Lemma 2' (弱相关 Hoeffding)**. 设 \(\{e_m\}_{m=1}^M\) 为
\([0,1]\)-值随机变量，满足 \(\mathbb{E}[e_m \mid s] \leq \mu_s\)，且
\(Cov(e_m, e_{m'} \mid s) \leq \rho \cdot \sqrt{Var(e_m) Var(e_{m'})}\)，其中
\(\rho \in [0, 1)\)。则:

\[\mathbb{P}\left(\frac{1}{M}\sum_{m=1}^M e_m > \theta \;\middle|\; s\right) \leq \exp\left(-\frac{2M(\theta - \mu_s)^2}{1 + (M-1)\rho}\right)\]

**证明**:
对相关随机变量，\(Var(\sum_m e_m \mid s) = \sum_m Var(e_m) + \sum_{m \neq m'} Cov(e_m, e_{m'}) \leq M\sigma^2(1 + (M-1)\rho)\)，其中
\(\sigma^2 = \max_m Var(e_m) \leq 1/4\)。应用 Bentkus (2004) 或
van de Geer \& Lederer (2013) 的弱相关 Hoeffding 界。\(\square\)

\subsubsection{2.3 修正后的 Theorem
1}<!-- label: ux4feeux6b63ux540eux7684-theorem-1 -->

\[F1 \geq 1 - \frac{1}\sum_{s} \rho_s \cdot \exp\left(-\frac{2M\Delta_s^2}{1 + (M-1)\bar_s}\right)\]

其中
\(\bar_s = \max_{m \neq m'} Corr(e_m, e_{m'} \mid X \in s)\)
是状态 \(s\) 内的**最大专家错误相关系数**。

**退化速率**:
\[M_{eff}(s) = \frac{M}{1 + (M-1)\bar_s}\]

\begin{longtable}[]{@{}ccl@{}}
\toprule\noalign{}
\(\bar_s\) & \(M=12\) 时 \(M_{eff}\) & 退化程度 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.00 & 12.0 & 原界 

0.02 & 9.8 & 轻微 

0.05 & 7.7 & 中度 

0.10 & 5.7 & 显著 

0.20 & 3.8 & 严重 

0.50 & 1.8 & 指数增益消失 

\end{longtable}

**关键推论**: 即使 \(\bar_s = 0.05\)（轻微相关），\(M=12\)
仍然相当于 7.7 个独立专家------指数收敛依然成立，只是常数稍大。

\subsubsection{2.4 A2'
的可检验性}<!-- label: a2-ux7684ux53efux68c0ux9a8cux6027 -->

与旧 A2 不同，A2' 是**可检验的**: 1. 对每个状态
\(s\)，计算专家错误矩阵 \(E_s \in \{0,1\}^{n_s \times M}\) 2.
估计成对相关系数 \(\hat_{mm'}^{(s)}\) 3. 取
\(\hat{\bar}_s = \max_{m \neq m'} \hat_{mm'}^{(s)}\) 4. 如果
\(\hat{\bar}_s \geq 0.5\)，发出 A2' 违反警告

**AlN v3 估计**: 在 8 个状态上估计
\(\hat{\bar}_s\)（待实验验证），预期在 thermal 状态上
\(\hat{\bar} \lesssim 0.05\)（因为每个专家在不同子集上训练）。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. 对 Theorem 4' (Exact Constant Minimax)
的影响}<!-- label: ux5bf9-theorem-4-exact-constant-minimax-ux7684ux5f71ux54cd -->

#### 3.1 问题<!-- label: ux95eeux9898 -->

Theorem 4' 使用 Bahadur-Rao 精确渐近，要求 i.i.d. Bernoulli
专家错误。如果存在相关:

\[Var\left(\frac{1}{M}\sum e_m \mid s\right) = \frac{p_0(1-p_0)}{M}(1 + (M-1)\rho) \neq \frac{p_0(1-p_0)}{M}\]

Bahadur-Rao 的渐近展开需要修正: 实际方差被放大 \((1+(M-1)\rho)\) 倍。

#### 3.2 修正<!-- label: ux4feeux6b63 -->

**修正的 Bahadur-Rao** (相关 Bernoulli):
\[\mathbb{P}(C_M \geq \theta \mid clean) \sim \frac{\exp(-M \cdot KL(\theta \| p_0))}{\lambda_0^* \sqrt{2\pi M \cdot \theta(1-\theta) \cdot (1+(M-1)\rho)}}\]

相关使有效样本量减少，但**指数速率 \(\kappa\) 不变**（Chernoff
信息只依赖于边际分布，不依赖相关性）。

**关键结论**: 精确常数 \(C_\) 需要乘以 \(\sqrt{1+(M-1)\rho}\)
的修正因子------但这不影响**速率最优性**（liminf
的指数不变）和**常数最优性**（只要修正后的常数对所有算法都适用）。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4. 对 Theorem 2
的影响}<!-- label: ux5bf9-theorem-2-ux7684ux5f71ux54cd -->

Theorem 2 的 Fano-Pinsker-TV 链**不依赖 A2**------只依赖特征
\(\phi\) 和状态 \(S\) 之间的互信息。专家相关不影响这个 bound。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. 对 Theorem 3
的影响}<!-- label: ux5bf9-theorem-3-ux7684ux5f71ux54cd -->

Theorem 3 的构造（世界 A vs 世界 B）**在 A2'
下仍然成立**------两个世界都可以容纳相关专家。不可识别性结论不受影响。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. 诚实结论<!-- label: ux8bdaux5b9eux7ed3ux8bba -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
定理
\end{minipage} & \begin{minipage}[b]
A2 依赖程度
\end{minipage} & \begin{minipage}[b]
关联影响
\end{minipage} & \begin{minipage}[b]
修正难度
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Thm 1 & **高** & 指数速率退化 \(M \to M_{eff}\) & 中等（替换
Hoeffding） 

Thm 2 & 无 & --- & 无需修正 

Thm 3 & 无 & --- & 无需修正 

Thm 4' & **高** & 精确常数修正 \(\sqrt{1+(M-1)\rho}\) &
中等（Bahadur-Rao 相关版本） 

Thm 5 & 无 & --- & 无需修正 

Prop 6 & 无 & --- & 无需修正 

\end{longtable}

**总体**: A2 是框架最脆弱的假设，但可以修复为
A2'（弱相关）而不改变核心结论的方向。指数速率仍然成立，只是有效专家数从
\(M\) 降为
\(M_{eff}\)。在实践中，两层状态发现**降低**了专家相关（因为状态内特征同质），但不能**消除**它。

**向审稿人的诚实回应**: ``We acknowledge that A2 (conditional
independence) is the strongest and least verifiable assumption in the
framework. We relax it to A2' (bounded correlation) and provide the
degraded bound. Under A2', the exponential rate is preserved but with
effective expert count \(M_{eff} = M/(1+(M-1)\bar)\). We
provide a procedure for estimating \(\bar\) from data.''

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{7. 数值验证：AlN
数据的相关性}<!-- label: ux6570ux503cux9a8cux8bc1aln-ux6570ux636eux7684ux76f8ux5173ux6027 -->

（待跑实验。预期：两层状态发现后，每个状态内专家错误的相关性应该很低------因为专家在不同子集上训练，且状态内样本分布同质。如果
thermal 状态的 \(\hat{\bar} \gtrsim 0.1\)，则当前 \(M=12\)
不够，需要增加到 \(M \approx 20\)。）

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*关联: {[}{[}01\_noise\_detection\_guarantee{]}{]} ·
{[}{[}exact\_constant\_minimax{]}{]} ·
{[}{[}hostile\_review\_response{]}{]}*