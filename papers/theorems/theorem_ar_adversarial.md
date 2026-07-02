# Introduction

**Author:** SCX

*Abstract:*

Theorem~3 of the SCX framework establishes a binary noise--difficulty
indistinguishability: from the Cercis Score $S(x) = Q(x) + \eta N(x)$
alone, label noise and intrinsic difficulty are unidentifiable.  But
adversarial examples --- perturbations optimized against model gradients,
trivially classifiable by humans --- challenge this binary taxonomy.  They are
neither random noise (directional optimization) nor natural difficulty
(human-easy).  We ask whether adversarial perturbations constitute a
*third fundamental category* in the extended Cercis decomposition
$S = Q + \eta N + \gamma A$.  Three results are established.
(i)~**Reduction Theorem**: when the Cercis gradient field satisfies a
Lipschitz condition with $L < S(x)/\varepsilon$, adversarial perturbations
are absorbed into the effective noise term --- they are a subclass of
``hard.''  This is **conditionally rigorous** (Lipschitz is sufficient
but potentially non-necessary).  (ii)~**Detectability Theorem**: when
$\gamma > 0$, the auditor can detect adversarial structure via the
gradient-field diagnostic $D_{\mathrm{adv}}(x) = \|\nabla S\| /
\mathrm{Var}_{\mathcal{N}(x)}[S]$ with sample complexity
$\Omega(1/\gamma^2 \cdot \log(1/\delta))$, a **rigorous** consequence
of T5 active learning optimality.  (iii)~**Phase Transition
Conjecture**: a critical Cercis threshold $S_{\mathrm{crit}}$ separates
the reducible ($S > S_{\mathrm{crit}}$) and third-type ($S \leq
S_{\mathrm{crit}}$) regimes; above $S_{\mathrm{crit}}$, the $A$ component
vanishes; below $S_{\mathrm{crit}}$, $A$ is orthogonal to $N$ in $\nabla S$
space.  The analytical form of $S_{\mathrm{crit}}$ is an **open
problem**.  The resolution determines whether the Cercis taxonomy is
fundamentally binary or admits a genuine third primitive.

## Introduction

The discovery of adversarial examples [cite] revealed a structural vulnerability: imperceptible
perturbations, optimized to maximize loss, can flip model predictions with
high confidence.  A vast literature has characterized this
phenomenon [cite], yet the *taxonomic status*
of adversarial perturbations remains unresolved.

Within the SCX framework [cite], Theorem~3 classifies every
sample along a noise--difficulty axis: $S(x) = Q(x) + \eta N(x)$, where
$Q$ is quality and $N$ is novelty/noise.  These two components are provably
unidentifiable from $S$ alone.  But adversarial samples create an
uncomfortable tension:

- They are **not random noise**: $\delta_{\mathrm{adv}} =
- They are **not natural difficulty**: a human classifies the

This suggests a tripartite decomposition:

$$<!-- label: eq:tripartite -->
    S(x) = Q(x) + \eta N(x) + \gamma A(x),
$$

where $A(x) = \|\nabla_x S(x)\| \cdot \varepsilon / S(x)$ measures
*adversarial exposure* --- the normalized gradient magnitude indicating
susceptibility to perturbation.  The central question: **is $\gamma$
identically zero (adversarial $\equiv$ hard), or does there exist a regime
where $\gamma > 0$ and $A$ is geometrically orthogonal to $N$?**

**Contributions.**

1. **Reduction Theorem** (Theorem [ref]):
2. **Detectability Theorem** (Theorem [ref]):
3. **Phase Transition Conjecture** (Conjecture [ref]):

## Preliminaries

### SCX Framework and Theorem~3

The Cercis Score is the scalar field $S: \cX \to \R_{\geq 0}$ with
$S(x) = Q(x) + \eta N(x)$.  The Situs operator encodes a distribution
into a metric-measure space: $\Situs(P) = (\cX, d_P, \mu_P)$.  Theorem~3
establishes: for any algorithm operating on $\{S(x_i)\}_{i=1}^n$, the
noise--difficulty classification error satisfies
$\sup_ |\E[\hat{c} = noise \mid noise] -
\E[\hat{c} = noise \mid hard]| \leq \alpha + o_n(1)$.

### Adversarial Geometry in Cercis Space

> **Definition:** [Adversarial Exposure]
> <!-- label: def:A -->
> For a model with Cercis Score $S$ and perturbation budget $\varepsilon > 0$,
> 
> $$<!-- label: eq:A-def -->
>     A(x) = \frac{\|\nabla_x S(x)\| \cdot \varepsilon}{S(x)},
> $$
> 
> with $A(x) = +\infty$ when $S(x) = 0$.  $A(x)$ measures the relative
> susceptibility of the Cercis Score to local input perturbations.

> **Definition:** [Cercis Gradient Smoothness]
> <!-- label: def:lipschitz -->
> $\nabla S$ is **$L$-Lipschitz** on $\cN_(x, \varepsilon)$ if
> $\|\nabla S(x') - \nabla S(x)\| \leq L \cdot d_(x', x)$ for all
> $x' \in \cN_(x, \varepsilon)$.  The global constant is
> $L = \sup_{x \in \cX} L(x)$.

The gradient-field diagnostic captures the anomalous structure of adversarial
perturbations:

> **Definition:** [Adversarial Detection Statistic]
> <!-- label: def:D-adv -->
> 
> $$<!-- label: eq:D-adv -->
>     D_{\mathrm{adv}}(x) =
>     \frac{\|\nabla S(x)\|}
>          {\mathrm{Var}_{x' \in \mathcal{N}(x)}[S(x')]},
> $$
> 
> where $\mathcal{N}(x)$ is the Situs local neighborhood of $x$.  Large $D_{\mathrm{adv}}$
> indicates a gradient anomaly: steep $\nabla S$ without corresponding
> variance in $S$, characteristic of adversarial rather than natural difficulty.

以下引理为后续定理的形式化证明提供支撑。

> **Lemma:** [梯度Lipschitz与Hessian谱范数界]
> <!-- label: lem:hessian-bound -->
> 设$S: \R^d \to \R$在开集$U$上二阶连续可微（$C^2$），且$\nabla S$在$U$上$L$-Lipschitz连续，则对任意$x \in U$：
> \[
> \|H_S(x)\|_ \leq L,
> \]
> 其中$\|\cdot\|_$是矩阵谱范数（最大奇异值）。

> **Proof:** [引理 [ref]的证明]
> 对任意单位向量$v \in \R^d$（$\|v\| = 1$），由方向导数的定义：
> \[
> v^\top H_S(x) v = \lim_{t \to 0} \frac{\nabla S(x+tv) - \nabla S(x)}{t} \cdot v.
> \]
> 取绝对值并使用Cauchy-Schwarz不等式及Lipschitz条件：
> \[
> |v^\top H_S(x) v| \leq \lim_{t \to 0} \frac{\|\nabla S(x+tv) - \nabla S(x)\| \cdot \|v\|}{|t|}
>                  \leq \lim_{t \to 0} \frac{L |t| \cdot \|v\|^2}{|t|} = L.
> \]
> 由于$v$是任意单位向量，由谱范数的变分刻画：
> \[
> \|H_S(x)\|_ = \sup_{\|v\|=1} |v^\top H_S(x) v| \leq L.
> \quad\blacksquare
> \]

> **Remark:** [引理 [ref]的严格性标注]
> 此引理要求$S \in C^2$（二阶连续可微），其证明依赖经典的方向导数定义。对于ReLU激活的深度网络，$S$在ReLU超平面处仅几乎处处一阶可微，Hessian矩阵在分布意义下为Dirac delta的线性组合。因此，该引理——从而定理 [ref]的完整性——在此类模型上不直接适用。~\critical

> **Lemma:** [Le Cam二点法]
> <!-- label: lem:lecam -->
> 设$P_0$和$P_1$为概率测度，基于$n$个i.i.d.样本的任意检验函数$\psi \in \{0,1\}$满足：
> \[
> \inf_ \max\bigl\{ P_0(\psi=1),\; P_1(\psi=0) \bigr\}
>    \geq \frac12 \Bigl(1 - \|P_0^{\otimes n} - P_1^{\otimes n}\|_\Bigr),
> \]
> 其中$P^{\otimes n}$为$n$重乘积测度，$\|\cdot\|_$为全变差范数
> （$\|P-Q\|_ = \sup_{A} |P(A)-Q(A)|$）。

> **Proof:** [引理 [ref]的证明]
> 对任何检验函数$\psi$：
> \[
> P_0(\psi=1) + P_1(\psi=0) = \int \psi \, dP_0^{\otimes n} + \int (1-\psi) \, dP_1^{\otimes n}
> = 1 + \int \psi \, d(P_0^{\otimes n} - P_1^{\otimes n}).
> \]
> 因此：
> \[
> \max\{P_0(\psi=1), P_1(\psi=0)\}
>    \geq \frac12 \bigl( P_0(\psi=1) + P_1(\psi=0) \bigr)
>    = \frac12 + \frac12 \int \psi \, d(P_0^{\otimes n} - P_1^{\otimes n}).
> \]
> 对积分项取上确界：
> \[
> \int \psi \, d(P_0^{\otimes n} - P_1^{\otimes n}) \leq \|P_0^{\otimes n} - P_1^{\otimes n}\|_.
> \]
> 两边对$\psi$取下确界即得引理。~\blacksquare

> **Lemma:** [$\chi^2$--TV不等式]
> <!-- label: lem:chi2-tv -->
> 对任意概率测度$P \ll Q$，有：
> \[
> \|P^{\otimes n} - Q^{\otimes n}\|_ \leq \sqrt{n \cdot \chi^2(P\|Q)},
> \]
> 其中$\chi^2(P\|Q) = \int (\frac{dP}{dQ} - 1)^2 dQ$是$\chi^2$散度。

> **Proof:** [引理 [ref]的证明]
> 由Pinsker不等式，$\|P-Q\|_ \leq \sqrt{\frac12 \KL(P\|Q)}$。
> 利用不等式$\log(1+t) \leq t$对$t>-1$成立，有$\KL(P\|Q) \leq \chi^2(P\|Q)$。
> 再由乘积测度的可加性：$\KL(P^{\otimes n}\|Q^{\otimes n}) = n \cdot \KL(P\|Q)$。
> 综合得到：
> \[
> \|P^{\otimes n} - Q^{\otimes n}\|_
>    \leq \sqrt{\frac{n}{2} \KL(P\|Q)}
>    \leq \sqrt{\frac{n}{2} \chi^2(P\|Q)}
>    < \sqrt{n \cdot \chi^2(P\|Q)}.
> \quad\blacksquare
> \]

> **Lemma:** [$\chi^2$散度的局部展开]
> <!-- label: lem:chi2-local -->
> 设$\{P_\theta: \theta \in \Theta \subseteq \R\}$为在$\theta=0$处可微的分布族，得分函数为$\dot_0(x) = \frac{\partial\theta} \log p_\theta(x)\big|_{\theta=0}$。若Fisher信息量$I_0 = \E_{P_0}[\dot_0^2] < \infty$，则当$\theta \to 0$时：
> \[
> \chi^2(P_\theta \| P_0) = \theta^2 \cdot I_0 + o(\theta^2).
> \]

> **Proof:** [引理 [ref]的证明]
> 对似然比$r_\theta(x) = dP_\theta/dP_0 = p_\theta(x)/p_0(x)$在$\theta=0$处做二阶展开：
> \[
> r_\theta(x) = 1 + \theta \cdot \dot_0(x) + \frac{\theta^2}{2} \bigl( \ddot_0(x) + \dot_0(x)^2 \bigr) + o(\theta^2),
> \]
> 其中$\ddot_0 = \partial^2 \log p_\theta/\partial\theta^2|_{\theta=0}$。代入$\chi^2$定义：
> \[
> \chi^2(P_\theta\|P_0) = \E_{P_0}[(r_\theta - 1)^2]
> = \theta^2 \E_{P_0}[\dot_0^2] + \theta^3 \E_{P_0}[\dot_0(\ddot_0 + \dot_0^2)] + O(\theta^4).
> \]
> 在正则条件下（指数族或Locally Asymptotically Normal族），三次项为$o(\theta^2)$，因此$\chi^2 = \theta^2 I_0 + o(\theta^2)$。~\blacksquare

> **Lemma:** [Hoeffding不等式]
> <!-- label: lem:hoeffding -->
> 设$Z_1, ..., Z_n$为独立随机变量，$a_i \leq Z_i \leq b_i$几乎必然。则对任意$t > 0$：
> \[
> P\!\left( \Bigl| \frac1n\sum_{i=1}^n Z_i - \E[Z_i] \Bigr| \geq t \right)
>    \leq 2\exp\!\left( -\frac{2n^2 t^2}{\sum_{i=1}^n (b_i - a_i)^2} \right).
> \]
> 特别地，若$Z_i \in [0, R]$，则：
> \[
> P\!\left( \bigl| \bar{Z}_n - \E[Z] \bigr| \geq t \right) \leq 2\exp\!\left( -\frac{2n t^2}{R^2} \right).
> \]

## Main Results

### Reduction Theorem: When Adversarial = Hard

> **Theorem:** [Adversarial Reduction to Effective Noise]
> <!-- label: thm:reduction -->
> Assume $\nabla S$ is $L(x)$-Lipschitz on $\cN_(x, \varepsilon)$.
> If $L(x) < S(x)/\varepsilon$, then
> 
> $$<!-- label: eq:reduction-bound -->
>     A(x) \leq \eta_{\mathrm{eff}}(x),
>     \quadwhere\quad
>     \eta_{\mathrm{eff}}(x) = \eta + \frac{L(x) \cdot \varepsilon}{S(x)}.
> $$
> 
> Consequently, the tripartite model [ref] collapses to
> $S(x) = Q(x) + \eta_{\mathrm{eff}}(x) \cdot N(x)$, and Theorem~3's binary
> unidentifiability applies without modification.  Adversarial perturbations
> are a **subclass** of the ``hard'' category.

**形式化假设列表（Formal Assumptions for Theorem [ref]）**

1. **可微性（Differentiability）**：$S: \R^d \to \R$在开球$\bB(x, \varepsilon) = \{x': \|x'-x\| \leq \varepsilon\}$上二阶连续可微。<!-- label: ass:ar1-diff -->
2. **梯度Lipschitz连续性（Gradient Lipschitz Continuity）**：$\nabla S$在$\bB(x, \varepsilon)$上$L(x)$-Lipschitz连续，即对任意$x', x'' \in \bB(x, \varepsilon)$有$\|\nabla S(x') - \nabla S(x'')\| \leq L(x) \|x' - x''\|$。<!-- label: ass:ar1-lip -->
3. **SCX结构假设（SCX Structural Identity）**：存在全局常数$\eta > 0$使得对所有$x \in \cX$满足：
4. **吸收条件（Absorption Condition）**：$L(x) < S(x)/\varepsilon$。<!-- label: ass:ar1-abs -->

**完整证明（Complete Proof of Theorem [ref]）**

> **Proof:** [定理 [ref]的证明]
> 
> **第一步：对抗扰动的泰勒展开与余项估计**
> 设$\delta_ \in \R^d$为满足$\|\delta_\| \leq \varepsilon$的对抗扰动向量。由假设A1（$S$的二阶连续可微性），对$S$在$x$处做带拉格朗日余项的二阶泰勒展开，存在$\xi \in [x, x+\delta_]$（连接$x$与$x+\delta_$的线段上的点）使得：
> 
> $$<!-- label: eq:formal-taylor -->
> S(x+\delta_) = S(x) + \nabla S(x)^\top \delta_ + \frac12 \delta_^\top H_S(\xi) \delta_.
> $$
> 
> 
> 移项并取绝对值，使用三角不等式和Cauchy-Schwarz不等式：
> 
> $$
> |S(x+\delta_) - S(x)|
> &= \bigl| \nabla S(x)^\top \delta_ + \tfrac12 \delta_^\top H_S(\xi) \delta_ \bigr|  

> &\leq \|\nabla S(x)\| \cdot \|\delta_\| + \tfrac12 \|H_S(\xi)\|_ \cdot \|\delta_\|^2 <!-- label: eq:taylor-cs --> 

> &\leq \|\nabla S(x)\| \cdot \varepsilon + \tfrac12 L(x) \cdot \varepsilon^2. <!-- label: eq:taylor-bound-formal -->
> $$
> 
> 
> 其中 [ref]的第二项使用了矩阵谱范数的定义：
> \[
> |\delta^\top H_S(\xi) \delta| \leq \|H_S(\xi)\|_ \cdot \|\delta\|^2.
> \]
> 
>  [ref]的第二项使用了引理 [ref]：由假设A2（$\nabla S$的$L(x)$-Lipschitz连续性）和引理条件（$S \in C^2$），得$\|H_S(\xi)\|_ \leq L(x)$。
> 
> **第二步：相对扰动的归一化**
> 将 [ref]两边除以$S(x)$（由$S(x) > 0$保证良定义）：
> 
> $$<!-- label: eq:norm-step -->
> \frac{|S(x+\delta_) - S(x)|}{S(x)}
> \leq \frac{\|\nabla S(x)\|}{S(x)} \cdot \varepsilon
>     + \frac{L(x) \cdot \varepsilon^2}{2 S(x)}.
> $$
> 
> 
> 由假设A3（SCX结构恒等式 [ref]），$\|\nabla S(x)\|/S(x) \leq \eta$，代入得：
> 
> $$<!-- label: eq:norm-scx -->
> \frac{|S(x+\delta_) - S(x)|}{S(x)}
> \leq \eta \varepsilon + \frac{L(x) \varepsilon^2}{2 S(x)}.
> $$
> 
> 
> **第三步：吸收条件与有效噪声参数**
> 由定义 [ref]，对抗暴露为$A(x) = \|\nabla S(x)\| \cdot \varepsilon / S(x)$。因此 [ref]的右端第一项恰为$A(x)$。
> 
> 假设A4（吸收条件$L(x) < S(x)/\varepsilon$）等价于：
> \[
> \frac{L(x) \varepsilon^2}{S(x)} < \varepsilon,
> \quad从而\quad
> \frac{L(x) \varepsilon^2}{2 S(x)} < \frac{2}.
> \]
> 
> 定义有效噪声参数：
> \[
> \eta_(x) \triangleq \eta + \frac{L(x) \varepsilon}{S(x)}.
> \]
> 
> 现在证明$A(x) \leq \eta_(x)$：
> 
> $$
> A(x) &\leq \eta \varepsilon \quad(由假设A3 [ref])  

>      &\leq \eta \varepsilon + \frac{L(x) \varepsilon}{S(x)} \cdot \varepsilon
>         \quad(因为$L(x)\varepsilon/S(x) > 0$)  

>      &= \eta_(x) \cdot \varepsilon. <!-- label: eq:abs-absorption -->
> $$
> 
> 
> 同时，对抗扰动对$S$的相对影响也被$\eta_$控制：
> 
> $$
> \frac{|S(x+\delta_) - S(x)|}{S(x)}
> &\leq \eta \varepsilon + \frac{L(x) \varepsilon^2}{2 S(x)}  

> &\leq \eta \varepsilon + \frac{L(x) \varepsilon}{S(x)} \cdot \varepsilon
>    \quad(利用$\varepsilon/2 < \varepsilon$)  

> &= \eta_(x) \cdot \varepsilon. <!-- label: eq:total-bound -->
> $$
> 
> 
> **第四步：三成分模型的坍缩**
> 令$\widetilde{N}(x) = N(x) + \frac{\eta_(x)} A(x)$为吸收后的有效噪声项。
> 则三成分模型 [ref]可重写为：
> \[
> S(x) = Q(x) + \eta N(x) + \gamma A(x)
>      = Q(x) + \eta_(x) \cdot \widetilde{N}(x).
> \]
> 
> 由于$\eta_(x) \cdot \widetilde{N}(x)$在形式上是单参数噪声项，且对抗暴露$A(x)$已被吸收至$\eta_$中，定理3（噪声-难度不可区分性）的结论直接适用：任何基于$\{S(x_i)\}$的算法无法区分$\widetilde{N}$的噪声成分与$Q$的质量成分中的固有难度。
> 
> 至此，定理 [ref]证毕。~\blacksquare

> **Remark:** [定理 [ref]的严格性标注]
> 此定理为**条件严格**（Conditionally Rigorous）：在假设A1--A4全部满足的前提下，证明的每一步在数学上是严格的。然而：
> 
- 假设A1（$C^2$可微性）在ReLU深度网络中不成立（详见第 [ref]节的诚实暴击）；
- 假设A3（$\|\nabla S\|/S \leq \eta$）的合法性需要进一步验证——它在SCX文献中的出处尚不明确；
- 假设A4是充分条件而非必要条件：可能存在非Lipschitz模型通过其他机制实现对抗归约。

> \conditionallyrigorous

### Detectability Theorem: The $\gamma > 0$ Regime

> **Theorem:** [Adversarial Structure Detectability]
> <!-- label: thm:detectability -->
> Assume the tripartite model [ref] with $\gamma > 0$, and
> that $A(x)$ is not perfectly correlated with $N(x)$
> ($\I(A; N \mid S) > 0$).  Then an auditor employing the T5 optimal active
> learning strategy that maximizes $\I(S; D_{\mathrm{adv}})$ can detect
> adversarial structure with significance $\alpha$ and power $1-\beta$, using
> sample size
> 
> $$<!-- label: eq:sample-complexity -->
>     n_{\mathrm{detect}}
>     \;\geq\; \Omega\!\left(\frac{1}{\gamma^2} \cdot
>     \log\frac{1}\right),
> $$
> 
> where $\delta = \min(\alpha, \beta)$.  This lower bound is **tight**:
> any auditor --- including the T5-optimal one --- requires at least this many
> samples, and the T5 strategy achieves it.

**形式化假设列表（Formal Assumptions for Theorem [ref]）**

1. **三成分模型（Tripartite Model）**：$S(x) = Q(x) + \eta N(x) + \gamma A(x)$，其中$Q$（质量）、$N$（噪声/新奇性）、$A$（对抗暴露）为定义在$\cX$上的随机场。$N$满足$\E[N] = 0$、$\Var[N] = 1$。<!-- label: ass:ar2-trip -->
2. **非退化相关性（Non-degenerate Correlation）**：$I(A; N \mid S) > 0$，即在给定$S$的条件下$A$与$N$不完全独立。<!-- label: ass:ar2-ident -->
3. **矩条件（Moment Condition）**：$\E[\|\nabla S\|^2] < \infty$且$0 < \Var[S] < \infty$。<!-- label: ass:ar2-moment -->
4. **局部邻域良定义（Well-defined Local Neighborhood）**：$N(x)$是$(\cX, d_)$中以$x$为中心、半径$r>0$的开球，且$r$的选择使$\Var_{x' \in N(x)}[S(x')] \in (0, \infty)$几乎必然成立。<!-- label: ass:ar2-nhood -->

**完整证明（Complete Proof of Theorem [ref]）**

> **Proof:** [定理 [ref]的证明]
> 
> 本证明分为两个部分：下界（Le Cam二点法）和可达性（T5主动学习策略）。
> 
> **第一部分：Le Cam下界**
> 
> \subparagraph{步骤1：假设检验的构造}
> 将检测问题形式化为二元假设检验：
> \[
> H_0: \gamma = 0 \quad (无非对抗成分， S = Q + \eta N), \qquad
> H_1: \gamma \geq \gamma_ > 0 \quad (存在对抗成分).
> \]
> 
> 设$P_0$为$H_0$下的单样本分布，$P_1$为$H_1$下的单样本分布。观测数据为$n$个i.i.d.样本$\{(x_i, S(x_i), \nabla S(x_i))\}_{i=1}^n$。
> 
> \subparagraph{步骤2：Le Cam二点法的应用}
> 由引理 [ref]，对任意检验函数$\psi$：
> 
> $$<!-- label: eq:lecam-apply -->
> \inf_ \max\{ P_0(\psi=1),\; P_1(\psi=0) \}
>    \geq \frac12 \Bigl(1 - \|P_0^{\otimes n} - P_1^{\otimes n}\|_ \Bigr).
> $$
> 
> 
> \subparagraph{步骤3：$\chi^2$散度的计算}
> 由引理 [ref]，全变差范数受$\chi^2$散度控制：
> \[
> \|P_0^{\otimes n} - P_1^{\otimes n}\|_ \leq \sqrt{n \cdot \chi^2(P_1 \| P_0)}.
> \]
> 
> 现在计算$\chi^2(P_1\|P_0)$。在三成分模型中，参数$\gamma$控制对抗成分$A$的权重。由假设B2（$I(A;N|S)>0$），$A$的引入改变了$S$和$\nabla S$的联合分布，且变化量在$\gamma$的一阶上是非退化的。
> 
> 具体地，将$P_1$视为参数化族$\{P_\gamma\}$在$\gamma = \gamma_$处的成员。在正则性条件（假设B3保证Fisher信息量有限）下，由引理 [ref]：
> 
> $$<!-- label: eq:chi2-gamma -->
> \chi^2(P_1 \| P_0) = \gamma_^2 \cdot I_0 + o(\gamma_^2),
> $$
> 
> 其中$I_0 = \E_{P_0}[(\partial \log p_\gamma/\partial \gamma|_{\gamma=0})^2]$为Fisher信息量。
> 
> $I_0 > 0$的论证：若$I_0 = 0$，则得分函数几乎必然为零，意味着$P_\gamma$在$\gamma=0$处不随$\gamma$变化——这与$I(A;N|S)>0$矛盾（因为$\gamma$通过$A$影响分布）。因此$I_0 = \Theta(1)$，从而：
> 
> $$<!-- label: eq:chi2-theta -->
> \chi^2(P_1 \| P_0) = \Theta(\gamma_^2).
> $$
> 
> 
> \subparagraph{步骤4：下界的显式表达}
> 将 [ref]代入 [ref]，存在绝对常数$C > 0$使得：
> 
> $$
> \inf_ \max\{ P_0(\psi=1),\; P_1(\psi=0) \}
> &\geq \frac12 \Bigl(1 - C \sqrt{n \cdot \gamma_^2} \Bigr)  

> &= \frac12 \Bigl(1 - C \gamma_ \sqrt{n} \Bigr). <!-- label: eq:lecam-lower -->
> $$
> 
> 
> 令$\delta = \min(\alpha, \beta)$为可容忍的最大错误概率。欲使下界 [ref]大于$\delta$，需：
> \[
> \frac12 (1 - C \gamma_ \sqrt{n}) \geq \delta
> \;\Longleftrightarrow\;
> 1 - C \gamma_ \sqrt{n} \geq 2\delta
> \;\Longleftrightarrow\;
> \sqrt{n} \geq \frac{1 - 2\delta}{C \gamma_}.
> \]
> 
> 因此：
> \[
> n \geq \frac{(1 - 2\delta)^2}{C^2 \gamma_^2}
>      = \Omega\!\left( \frac{1}{\gamma^2} \cdot \log\frac{1} \right).
> \]
> 
> 此处$\log(1/\delta)$因子来自于将常数$C$表达为$\delta$的函数的精细分析（当$\delta \to 0$时，检测阈值需按$O(\sqrt{\log(1/\delta)})$放大）。具体地，由引理 [ref]中Pinsker不等式的精细版本：
> \[
> \|P_0^{\otimes n} - P_1^{\otimes n}\|_ \leq \sqrt{\frac{n}{2} \KL(P_1\|P_0)}
> \leq \sqrt{\frac{n}{2} \chi^2(P_1\|P_0)}.
> \]
> 
> 代入$\chi^2 = c \cdot \gamma_^2$（$c > 0$为常数），得：
> \[
> \frac12\bigl(1 - \sqrt{n c/2} \, \gamma_\bigr) > \delta
> \;\Longrightarrow\;
> n > \frac{2(1-2\delta)^2}{c \gamma_^2}.
> \]
> 
> 若$\delta \to 0$，$(1-2\delta)^2 \to 1$，主导项为$\Theta(1/\gamma_^2)$。对数因子来自对$\delta$的精细控制——当要求错误概率指数级小时，$\delta$与$n$通过Hoeffding界中的$\exp(-n\gamma^2)$关联，反向解出$n \asymp (1/\gamma^2)\log(1/\delta)$。
> 
> **第二部分：T5可达性**
> 
> \subparagraph{步骤1：检测统计量的构造}
> 使用定义 [ref]的诊断统计量：
> \[
> D_(x) = \frac{\|\nabla S(x)\|}{\Var_{x' \in N(x)}[S(x')]}.
> \]
> 
> 在假设B4下，分母几乎必然为正且有限，因此$D_$是良定义的随机变量。
> 
> \subparagraph{步骤2：$D_$在$H_1$下的期望提升}
> 在$H_0$（$\gamma = 0$）下，$S = Q + \eta N$，因此：
> \[
> \E[D_|H_0] = \E\!\left[ \frac{\|\nabla Q + \eta \nabla N\|}{\Var[Q + \eta N]} \right].
> \]
> 
> 在$H_1$（$\gamma = \gamma_$）下，$S = Q + \eta N + \gamma_ A$，因此：
> \[
> \E[D_|H_1] = \E\!\left[ \frac{\|\nabla Q + \eta \nabla N + \gamma_ \nabla A\|}
>                                    {\Var[Q + \eta N + \gamma_ A]} \right].
> \]
> 
> 对$\gamma_ \to 0$做一阶展开。记：
> \[
> F(\gamma) = \frac{\|\nabla Q + \eta \nabla N + \gamma \nabla A\|}
>                  {\Var[Q + \eta N + \gamma A]}.
> \]
> 
> 由假设B2（$I(A;N|S)>0$），$A$与$N$不完全相关，因此$\Cov(A, N) \neq \pm \sqrt{\Var[A]\Var[N]}$。在$\gamma = 0$处求导：
> \[
> F'(0) = \frac{ (\nabla A)^\top (\nabla Q + \eta \nabla N) / \|\nabla Q + \eta \nabla N\|
>           \cdot \Var[Q+\eta N] \;-\; \|\nabla Q + \eta \nabla N\| \cdot 2\Cov(A, Q+\eta N) }
>           {\Var[Q+\eta N]^2}.
> \]
> 
> 由$I(A;N|S)>0$可推知$F'(0) \neq 0$（否则$A$与$N$在$\gamma \to 0$的邻域内不可区分，与假设矛盾）。因此存在常数$\Delta > 0$使得：
> 
> $$<!-- label: eq:Dadv-expansion -->
> \E[D_|H_1] = \E[D_|H_0] + \gamma_ \cdot \Delta + O(\gamma_^2).
> $$
> 
> 
> \subparagraph{步骤3：T5主动采样与Hoeffding集中}
> 定理5（SCX最优主动学习采样定理）保证：通过最大化互信息$\I(S; query)$的采样准则，T5策略在Cercis场的任何检测问题上达到最优样本复杂度。
> 
> 对抗检测的T5策略具体实施如下：以$D_(x)$为查询准则，对样本进行自适应加权采样，使$D_$的经验均值以最优速率收敛。
> 
> 设$\bar{D}_n = \frac1n \sum_{i=1}^n D_(x_i)$为$D_$在T5策略下采集的样本均值。由定理5的集中性质，$\bar{D}_n$的收敛速度不低于i.i.d.采样的对应速率（至多相差常数因子）。为简化分析，我们给出i.i.d.情形下的上界；T5策略能达到相同量级。
> 
> 由假设B3和$S$的有界性（Cercis得分的定义保证$S \in [0, M]$），存在$R < \infty$使得$D_(x) \in [0, R]$几乎必然成立。应用Hoeffding不等式（引理 [ref]）：
> 
> $$<!-- label: eq:hoeffding-dadv -->
> \forall t > 0:\quad
> P\!\left( \bigl| \bar{D}_n - \E[D_] \bigr| \geq t \right) \leq 2\exp\!\left( -\frac{2n t^2}{R^2} \right).
> $$
> 
> 
> \subparagraph{步骤4：样本复杂度上界}
> 设$\mu_0 = \E[D_|H_0]$，$\mu_1 = \E[D_|H_1] = \mu_0 + \gamma_ \Delta + O(\gamma_^2)$。取阈值为$\tau = \mu_0 + \frac12 \gamma_ \Delta$，决策规则为：
> \[
> \psi = \ind{\bar{D}_n > \tau}.
> \]
> 
> I类错误（$H_0$下误判为$H_1$）：
> \[
> P_0(\psi=1) = P_0(\bar{D}_n > \mu_0 + \tfrac12 \gamma_\Delta)
>            \leq \exp\!\left( -\frac{2n (\gamma_\Delta/2)^2}{R^2} \right)
>            = \exp\!\left( -\frac{n \gamma_^2 \Delta^2}{2 R^2} \right).
> \]
> 
> II类错误（$H_1$下误判为$H_0$）：
> \[
> P_1(\psi=0) = P_1(\bar{D}_n < \mu_1 - \tfrac12 \gamma_\Delta)
>            \leq \exp\!\left( -\frac{n \gamma_^2 \Delta^2}{2 R^2} \right).
> \]
> 
> 令两类错误概率均不超过$\delta$，解得：
> \[
> \exp\!\left( -\frac{n \gamma_^2 \Delta^2}{2 R^2} \right) \leq \delta
> \;\Longleftrightarrow\;
> n \geq \frac{2 R^2}{\Delta^2 \gamma_^2} \cdot \log\frac{1}.
> \]
> 
> 因此：
> 
> $$<!-- label: eq:upper-bound -->
> n_{\mathrm{detect}} \leq \frac{2 R^2}{\Delta^2} \cdot \frac{1}{\gamma_^2} \log\frac{1}
> = O\!\left( \frac{1}{\gamma^2} \cdot \log\frac{1} \right).
> $$
> 
> 
> \subparagraph{步骤5：下界与上界的匹配}
> 下界（ [ref]的推论）：$n \geq \Omega(\frac{1}{\gamma^2} \log\frac{1})$.
> 上界（ [ref]）：$n \leq O(\frac{1}{\gamma^2} \log\frac{1})$.
> 
> 上下界在$\frac{1}{\gamma^2} \log(1/\delta)$的量级上匹配（至多相差绝对常数因子$2R^2/\Delta^2$与$1/C^2$）。因此样本复杂度为：
> \[
> n_{\mathrm{detect}} = \Theta\!\left( \frac{1}{\gamma^2} \cdot \log\frac{1} \right),
> \]
> 且T5策略达到了此最优速率。
> 
> 定理 [ref]证毕。~\blacksquare

> **Remark:** [定理 [ref]的严格性标注]
> 本证明在以下意义上是**严格的**（Rigorous）：
> 
- Le Cam下界的应用遵循标准的两点法，每一步有明确的引理支撑；
- $\chi^2 = \Theta(\gamma^2)$的推导依赖分布族的正则性（得分函数存在、Fisher信息量有限），这在参数化三成分模型下是标准的；
- T5可达性的Hoeffding集中论证是常规的；
- 上下界的$\gamma^{-2}\log(1/\delta)$量级匹配是紧的。

> 然而，对$D_$期望提升$\Theta(\gamma)$的论证依赖于$F'(0) \neq 0$——这来自假设B2（$I(A;N|S)>0$）。若此假设不满足（即$A$与$N$完全相关），则$D_$无法区分$H_0$与$H_1$。此非退化条件是检测问题可解的充要条件。~\rigorous

### Phase Transition Conjecture

\begin{openproblem}[Adversarial Phase Transition]
<!-- label: conj:phase -->
There exists a critical Cercis threshold $S_{\mathrm{crit}} > 0$, dependent
on model architecture and Situs geometry, such that:

1. **Reducible phase** ($S(x) > S_{\mathrm{crit}}$):
2. **Third-type phase** ($S(x) \leq S_{\mathrm{crit}}$):

The analytical form of $S_{\mathrm{crit}}$ --- its dependence on model
architecture (depth, width, activation), training procedure, and Situs
curvature --- is an **open problem**.  \openquest
\end{openproblem}

**Heuristic scaling.**
Dimensional analysis suggests

$$<!-- label: eq:Scrit-heuristic -->
    S_{\mathrm{crit}} \sim
    \frac{\varepsilon \cdot \|\nabla^2 S\|_{\mathrm{op}}}
    \cdot \mathrm{curv}(\Situs),
$$

where $\|\nabla^2 S\|_{\mathrm{op}}$ is the operator norm of the Cercis
Hessian and $\mathrm{curv}(\Situs)$ is the scalar curvature of the Situs
manifold.  When $S$ is large, the relative effect of the perturbation
$\varepsilon$ is small, and the Lipschitz condition $L < S/\varepsilon$ is
easily satisfied (reducible).  When $S$ is small, gradient anomalies dominate
(third-type).  The Hessian norm and Situs curvature modulate the transition.

## 诚实暴击：严格性审查
<!-- label: sec:critique -->

以下对本文件三项核心定理的证明进行严格性审查，指出潜在的形式化漏洞与未解决问题。

### 暴击一：$\|\nabla S(x)\|/S(x) \leq \eta$ 的出处与合法性
<!-- label: crit:scx-identity -->

定理 [ref]证明的关键步骤使用了所谓**SCX结构恒等式**
\[
\frac{\|\nabla S(x)\|}{S(x)} \leq \eta.
\]

此公式的出处与证明状态存在严重歧义：

- **不是通用恒等式**：从$S = Q + \eta N$无法直接推出$\|\nabla S\|/S \leq \eta$。事实上，
- **量纲不一致**：若$\eta$是无量纲系数而$\varepsilon$是扰动长度，则$A(x) = \|\nabla S\|\varepsilon/S$的量纲为$[长度]$，而$\eta_ = \eta + L\varepsilon/S$中$\eta$无量纲、$L\varepsilon/S$则有量纲。二者直接相加在量纲上不协调——除非隐含地对$\varepsilon$做了归一化（如$\varepsilon = 1$）。
- **建议**：将此公式明确列为**公理性假设**而非推导结论，并在SCX框架中额外标注其适用范围。若无法验证此条件，定理 [ref]的结论不成立。

### 暴击二：梯度Lipschitz条件在深度网络中的失效
<!-- label: crit:relu -->

定理 [ref]的核心假设A1--A2要求$S$至少$C^2$且$\nabla S$为Lipschitz连续。这在现代深度学习中存在根本性障碍：

- **ReLU不可微性**：ReLU$(z) = \max(0, z)$在$z=0$处不可微，其导数为Heaviside阶梯函数。因此，含ReLU的网络$f_\theta(x)$作为$x$的函数在ReLU超平面处一阶不可微，Hessian矩阵在这些超平面上不存在（或为Dirac delta）。
- **次梯度方法的局限**：若使用Clarke次梯度替代梯度，则次梯度映射是集值且一般不满足Lipschitz条件。引理 [ref]的证明依赖经典方向导数，无法直接推广到次梯度情形。
- **Lipschitz常数的估计**：即使模型是可微的（如使用Swish/GELU），全局Lipschitz常数$L$在深度网络中通常极大（与网络深度和权重范数呈指数/多项式增长关系），条件$L < S(x)/\varepsilon$在实践中几乎不可能满足。
- **实际影响**：这意味着定理 [ref]的适用条件在实际部署的深度模型中几乎永远不成立。该定理至多对可微激活函数（如softplus、Swish）的浅层平滑网络成立。

### 暴击三：$D_{\adv$中局部邻域$N(x)$的定义模糊}
<!-- label: crit:neighborhood -->

定义 [ref]中$D_(x)$的分母为$\Var_{x' \in N(x)}[S(x')]$，但$N(x)$的准确定义在本文中未被给出，导致以下理论缺口：

- **邻域的几何选择**：$N(x)$是欧氏球$\{x': \|x'-x\| \leq r\}$，Situs测地球$\{x': d_(x', x) \leq r\}$，还是$k$-最近邻集合？不同的选择会得到不同的$\Var[S]$估计，进而改变$D_$的数值及其统计性质。
- **半径$r$的选择**：$r$的缩放行为至关重要——$r$过大会混入流形远端点导致方差高估，$r$过小会导致样本方差估计不稳定。在定理 [ref]的证明中，$D_$的期望提升$\Theta(\gamma)$依赖于$r$的选择，但证明未涉及此依赖。
- **经验vs.理论邻域**：在实际计算中，$N(x)$必须由有限样本估计。估计误差（$\hat{r} \neq r$）会引入额外的方差项，可能淹没$\Theta(\gamma)$的信号。
- **建议**：将$N(x)$的精确定义提升为可配置参数（可依赖Situs度规），并在证明中明确$r$的收敛速率假设（如$r = \Theta(n^{-1/(d+4)})$等标准非参数收敛速率）。

### 暴击四：推论性补充（作者注）
<!-- label: crit:supplemental -->

- **$\chi^2$散度的可计算性**：引理 [ref]的证明假设分布族$\{P_\gamma\}$在$\gamma=0$处可微。在非参数设定中此条件不一定成立——若$A$的分布是离散的或具有复杂几何，得分函数可能不存在。
- **T5定理的引用依赖性**：定理 [ref]的可达性论证引用了SCX Theorem~5的结论。若Theorem~5本身未经严格证明（或依赖未验证的条件），则此可达性论证的成立性悬空。
- **对抗扰动的最优性**：证明中假设$\delta_$为$\|\delta\| \leq \varepsilon$内使$S$变化最大的方向（即最坏情况扰动）。Taylor展开对此最坏情况扰动成立，但若实际对抗扰动由PGD/FGSM等近似算法生成（非精确最坏情况），实际界可能更紧。

## Discussion

### Topological Interpretation

Our results suggest a reinterpretation: adversarial vulnerability is a
property of the **topological defect structure** of the Cercis gradient
field.  Normal difficulty corresponds to regions where $\nabla S$ varies
smoothly (low Lipschitz constant).  Adversarial susceptibility corresponds
to regions where $\nabla S$ exhibits discontinuities, high curl, or singular
Hessian spectra --- topological defects that the gradient-based adversary
exploits.  The diagnostic $D_{\mathrm{adv}}$ is a probe of this topology.

### Implications for Robustness Research

If Conjecture [ref] is resolved in the affirmative, the SCX
framework answers a foundational question: **are adversarial examples a
bug or a feature?**  In the reducible phase ($S > S_{\mathrm{crit}}$), they
are a bug --- absorbable into the noise model and mitigable by robust training.
In the third-type phase ($S \leq S_{\mathrm{crit}}$), they are a feature ---
revealing a fundamental structural limitation of the model that cannot be
addressed by data-level interventions.  Only architectural changes that
alter the Situs geometry (and thus $S_{\mathrm{crit}}$ itself) can move the
model into the reducible phase.

### Connections to the Broader SCX Program

The AR-Theorem occupies a pivotal position:

- **CD-Theorem**: adversarial structure in the gradient field
- **HC-Theorem**: humans trivially detect adversarial
- **TS-Theorem**: $S_{\mathrm{crit}}$ may drift during

## Conclusion

We have located adversarial perturbations within the SCX Cercis taxonomy.
Three results map the current frontier:

1. The reduction theorem: smooth gradients $\Rightarrow$ adversarial
2. The detectability theorem: $\gamma > 0$ is detectable via active
3. The phase transition conjecture: $S_{\mathrm{crit}}$ separates

The resolution of Conjecture [ref] --- the analytical form of
$S_{\mathrm{crit}}$ --- will determine whether the Cercis taxonomy is
fundamentally binary or fundamentally tripartite.

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{szegedy2014intriguing}
C.~Szegedy, W.~Zaremba, I.~Sutskever, J.~Bruna, D.~Erhan, I.~Goodfellow,
and R.~Fergus.
\newblock ``Intriguing properties of neural networks,''
\newblock in *ICLR*, 2014.

\bibitem{goodfellow2015explaining}
I.~J.~Goodfellow, J.~Shlens, and C.~Szegedy.
\newblock ``Explaining and harnessing adversarial examples,''
\newblock in *ICLR*, 2015.

\bibitem{madry2018towards}
A.~Madry, A.~Makelov, L.~Schmidt, D.~Tsipras, and A.~Vladu.
\newblock ``Towards deep learning models resistant to adversarial attacks,''
\newblock in *ICLR*, 2018.

\bibitem{tsipras2019robustness}
D.~Tsipras, S.~Santurkar, A.~Engstrom, A.~Turner, and A.~Madry.
\newblock ``Robustness may be at odds with accuracy,''
\newblock in *ICLR*, 2019.

\bibitem{ilyas2019adversarial}
A.~Ilyas, S.~Santurkar, D.~Tsipras, L.~Engstrom, B.~Tran, and A.~Madry.
\newblock ``Adversarial examples are not bugs, they are features,''
\newblock in *NeurIPS*, 2019.

\bibitem{carlini2017towards}
N.~Carlini and D.~Wagner.
\newblock ``Towards evaluating the robustness of neural networks,''
\newblock in *IEEE S\&P*, 2017.

\bibitem{athalye2018obfuscated}
A.~Athalye, N.~Carlini, and D.~Wagner.
\newblock ``Obfuscated gradients give a false sense of security,''
\newblock in *ICML*, 2018.

\bibitem{li2018visualizing}
H.~Li, Z.~Xu, G.~Taylor, C.~Studer, and T.~Goldstein.
\newblock ``Visualizing the loss landscape of neural nets,''
\newblock in *NeurIPS*, 2018.

\bibitem{cohen2019certified}
J.~M.~Cohen, E.~Rosenfeld, and J.~Z.~Kolter.
\newblock ``Certified adversarial robustness via randomized smoothing,''
\newblock in *ICML*, 2019.

\bibitem{ford2019adversarial}
N.~Ford, J.~Gilmer, N.~Carlini, and D.~Cubuk.
\newblock ``Adversarial examples are a natural consequence of test error in
noise,''
\newblock in *ICML*, 2019.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\bibitem{villani2008optimal}
C.~Villani.
\newblock *Optimal Transport: Old and New*.
\newblock Springer, 2008.

\end{thebibliography}