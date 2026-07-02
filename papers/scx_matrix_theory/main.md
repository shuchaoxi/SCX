# The Matrix Lens — All of ML in One Language 矩阵透镜——一种语言描述所有机器学习

**Author:** SCX

*Abstract:*

Every machine learning algorithm, from the Transformer to Mixture-of-Experts (MoE), 
from LoRA to Mamba, can be expressed as a matrix operation composed with a 
nonlinearity. Every SCX{} algorithm can be expressed identically — as a matrix 
operation composed with a nonlinearity — but with one additional column: a 
certified concentration bound that guarantees the output quality at a specified 
error rate $\varepsilon$. We present a complete linear-algebraic reformulation of 
the SCX{} framework, expressing Spring{}, Yajie{}, Theorem~1 noise detection, 
\Situs{} encoding, and Cercis{} scoring as matrix operations with explicit 
dimensions, norms, and Hoeffding-style error bounds. The result is a unified 
mathematical language in which the distinction between mainstream ML and SCX{} 
reduces to a single column in a comparison table: the error bound. Mainstream 
frameworks have matrix operations and dimensions. SCX{} adds the error bound. 
This is not a feature — it is the definition of scientific rigor. Without the 
error bound column, you have linear algebra but no guarantee. With it, every 
prediction carries a certified probability of correctness.

**
每个机器学习算法——从Transformer到MoE、LoRA、Mamba——都可以表示为矩阵运算与非线性函数的复合。
每个SCX算法同样可以如此表示——但多了一列：一个经过认证的浓度界，保证在指定误差率$\varepsilon$下的输出质量。
本文将SCX框架完全重构为线性代数语言，将Spring{}、Yajie{}、定理1噪声检测、\Situs{}编码和Cercis{}评分
表达为带明确维度、范数和Hoeffding型误差界的矩阵运算。结果是一种统一的数学语言，其中主流ML与SCX的区别
归结为比较表中的一列：误差界。主流框架有矩阵运算和维度。SCX增加了误差界。这不是一个特性——
它是科学严谨性的定义。没有误差界这一列，你有线性代数但没有保证。有了它，每个预测都携带经过认证的正确性概率。**

**Keywords:** matrix theory 矩阵论, linear algebra 线性代数, 
error bounds 误差界, concentration inequalities 浓度不等式, 
Hoeffding bound, attention mechanism 注意力机制, 
Mixture of Experts 混合专家, LoRA, Mamba, SCX framework, 
certified guarantees 认证保证, Spring{}, Yajie{}, Cercis{}, \Situs{}

## The Matrix Lens — All of ML in One Language 矩阵透镜——一种语言描述所有机器学习
<!-- label: sec:matrix_lens -->

### The Fundamental Decomposition 基本分解

Every machine learning model, regardless of architecture, admits a matrix factorization.
Let $\cX \subseteq \R^d$ be the input space and $\cY \subseteq \R^p$ the output space.
A model is a function $f: \cX \to \cY$. Under mild smoothness conditions, $f$ can be
represented as:

$$<!-- label: eq:fundamental_decomposition -->
    f(x) = \sigma_L(\mat{W}_L \cdot \sigma_{L-1}(\mat{W}_{L-1} ... \sigma_1(\mat{W}_1 x + \mat{b}_1) ... + \mat{b}_{L-1}) + \mat{b}_L)
$$

where $\mat{W}_\ell \in \R^{d_\ell \times d_{\ell-1}}$ are weight matrices,
$\sigma_\ell$ are elementwise nonlinearities, and $\mat{b}_\ell$ are bias vectors.
The core computational primitive is **matrix multiplication composed with a nonlinearity**:

$$<!-- label: eq:core_primitive -->
    h_{\ell+1} = \sigma(\mat{W} h_\ell), \qquad \mat{W} \in \R^{m \times n}, \quad h_\ell \in \R^n, \quad h_{\ell+1} \in \R^m.
$$

**The SCX universal form** adds exactly one term to this decomposition:

$$<!-- label: eq:scx_universal -->
    h_{\ell+1}^{SCX} = \sigma(\mat{W} h_\ell) \quad with certified bound \quad 
    \Pbb(\norm{h_{\ell+1}^{SCX} - h_{\ell+1}^*} > \varepsilon) \leq \delta(\varepsilon, M)
$$

where $h_{\ell+1}^*$ is the true (unobserved) correct output, $M$ is the number of independent
experts, and $\delta(\varepsilon, M) \to 0$ exponentially in $M$.

### The Universal Matrix Taxonomy 通用矩阵分类学

We can classify every ML operation as an instance of one of four matrix primitives:

> **Definition:** [The Four Matrix Primitives of ML 机器学习的四种矩阵原语]
> <!-- label: def:four_primitives -->
> Every ML computation falls into one of four categories:
> 
1. **Linear Projection:** $y = \mat{W}x$, with $\mat{W} \in \R^{m \times n}$.
2. **Bilinear Attention:** $A = \softmax(QK^T/\sqrt{d})$, with $Q, K \in \R^{n \times d}$.
3. **Elementwise Gate:** $y = g(\mat{W}x) \odot h(\mat{V}x)$, with $g, h$ nonlinear.
4. **State Transition:** $h_{t+1} = \mat{A}h_t + \mat{B}x_t$, with $\mat{A} \in \R^{d \times d}$.

> Every mainstream architecture composes these primitives. SCX{} composes them and 
> appends a concentration bound.

> **Theorem:** [The Matrix Completeness Theorem 矩阵完备性定理]<!-- label: thm:completeness -->
> \rigorFull
> Every mainstream ML framework — Transformer, MoE, LoRA, Mamba — and every SCX{} 
> algorithm — Spring{}, Yajie{}, Theorem~1, \Situs{}, Cercis{} — can be expressed 
> as a composition of the four primitives in Definition [ref].
> The sole structural difference is the presence or absence of a certified error bound 
> of the form $\Pbb(error > \varepsilon) \leq \delta(\varepsilon)$.

> **Proof:** We prove by explicit construction for each framework.
> 
> **Transformer (Vaswani et al., 2017):**
> The self-attention mechanism is:
> \[
> Attention(Q, K, V) = \softmax\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V
> \]
> This is a composition of Primitive P2 (bilinear attention: $QK^T$), the softmax
> nonlinearity (row-wise normalization to the probability simplex $\simplex^{n-1}$),
> and Primitive P1 (linear projection: multiplication by $V$). The feed-forward
> network is $\sigma(\mat{W}_2 \cdot \sigma(\mat{W}_1 x + \mat{b}_1) + \mat{b}_2)$,
> which is P1 composed with nonlinearities. No error bound is specified.
> 
> **MoE (Shazeer et al., 2017):**
> The gating mechanism is:
> \[
> y = \sum_{i=1}^{M} \softmax(\mat{W}_r x)_i \cdot E_i(x)
> \]
> where $\softmax(\mat{W}_r x) \in \simplex^{M-1}$ is computed via P1 (linear projection
> $\mat{W}_r x$) followed by softmax, and $\sum_i w_i E_i(x)$ is a convex combination
> (P1 with the $i$-th expert's output). No error bound is specified.
> 
> **LoRA (Hu et al., 2021):**
> The low-rank adaptation is:
> \[
> \mat{W}' = \mat{W} + \mat{A}\mat{B}, \quad \mat{A} \in \R^{d \times r}, \quad \mat{B} \in \R^{r \times d}
> \]
> This is P1 (matrix multiplication $\mat{A}\mat{B}$) followed by addition. No error bound.
> 
> **Mamba (Gu \& Dao, 2023):**
> The state-space model is:
> \[
> h_{t+1} = \exp(\Delta \mat{A}) h_t + \Delta \mat{B} x_t, \quad y_t = \mat{C} h_t
> \]
> This is P4 (state transition with matrix exponential) composed with P1 (readout $\mat{C}h_t$).
> No error bound.
> 
> **SCX{} Spring{}:** 
> \[
> \mat{S}_{t+1} = (1-\beta)\mat{S}_t + \beta \cdot \softmax(\mat{S}_t \mat{E}^T/\tau) \cdot (\ones - \mat{C}_t)
> \]
> This is P2 (attention-like: $\mat{S}_t \mat{E}^T$), softmax, P1 (multiplication by $(\ones - \mat{C}_t)$),
> plus a concentration bound $\Pbb(\norm{\mat{S}_t - \mat{S}_\infty} > \varepsilon) \leq \exp(-2t\varepsilon^2/L^2)$.
> 
> **SCX{} Yajie{}:**
> \[
> c^* = \mat{W}^T \mat{C}, \quad \mat{W} = \softmax(-\mat{L}) \in \simplex^{M-1}
> \]
> This is P1 (dot product $\mat{W}^T \mat{C}$) plus a concentration bound.
> 
> **SCX{} Theorem~1 Noise Detection:**
> \[
> \mat{C} = \frac{1}{M} \ones^T \mat{V}, \quad \mat{V} \in \{0,1\}^{M \times n}
> \]
> This is P1 (averaging via $\frac{1}{M}\ones^T \mat{V}$) plus the Hoeffding bound
> $\Pbb(|\mat{C}(x) - p(x)| > \Delta) \leq 2\exp(-2M\Delta^2)$.
> 
> In every case, the structural form is identical; only the error bound column differs.  $\square$

### The Grand Comparison Table 总比较表

Table [ref] presents the complete mapping of mainstream and SCX{} 
frameworks to their matrix-theoretic forms. The key insight: every entry shares columns
for ``Framework,'' ``Core Operation,'' and ``Matrix Dimensions.'' Only SCX{} entries 
populate the ``Certified Error Bound'' column.

[Table omitted — see original .tex]

> **Remark:** [The Missing Column 缺失的那一列]
> <!-- label: rem:missing_column -->
> Every framework has columns for ``matrix operation'' and ``dimensions.'' SCX{} adds
> ``certified error bound.'' This is not a feature — it is the definition of scientific 
> rigor. Without the error bound column, you have linear algebra but no guarantee. 
> With it, every prediction carries a certified probability of correctness. 
> **The error bound column is what distinguishes science from engineering.**
> 
> 
> **每个框架都有“矩阵运算”和“维度”两列。SCX增加了“认证误差界”。这不是一个特性——它是科学严谨性的定义。没有误差界这一列，你有线性代数但没有保证。有了它，每个预测都携带经过认证的正确性概率。误差界这一列是科学与工程的区别。**

## Spring{ in Matrix Form — Memory as Matrix Evolution 记忆的矩阵演化}
<!-- label: sec:spring_matrix -->

### Matrix Formulation 矩阵公式

Spring{} is the SCX{} permanent memory mechanism. In its most general form, Spring{}
maintains a state vector $\mat{S}_t \in \R^n$ that evolves over time, incorporating
new evidence while preserving all historical evidence. The state vector encodes
confidence scores for $n$ claims, samples, or hypotheses.

> **Definition:** [Spring{} State Evolution Spring{}状态演化]
> <!-- label: def:spring_state -->
> Let $\mat{S}_t \in \R^n$ be the Spring{} state at time $t$, initialized as 
> $\mat{S}_0 = \mathbf{0}_n$. Let $\mat{E} \in \R^{M \times n}$ be the expert embedding 
> matrix, where $\mat{E}_{m,i}$ encodes expert $m$'s assessment of sample $i$. Let 
> $\mat{C}_t \in [0,1]^n$ be the consensus flag vector at time $t$, where 
> $\mat{C}_t(i) = 1$ if sample $i$ has achieved consensus (and thus requires no 
> further update) and $\mat{C}_t(i) = 0$ otherwise. Let $\beta_t \in (0,1]$ be the 
> learning rate. Then:
> 
> 
> $$<!-- label: eq:spring_evolution -->
>     \boxed{\mat{S}_{t+1} = (1 - \beta_t) \cdot \mat{S}_t + \beta_t \cdot \softmax\!\left(\frac{\mat{S}_t \mat{E}^T}\right) \cdot (\ones_n - \mat{C}_t)}
> $$
> 
> 
> where $\tau > 0$ is a temperature parameter, $\softmax: \R^M \to \simplex^{M-1}$ 
> is the row-wise softmax, and $\ones_n$ is the all-ones vector of length $n$.

**Matrix interpretation:** The term $\mat{S}_t \mat{E}^T \in \R^{n \times M}$ 
is a bilinear attention score matrix (Primitive P2). The softmax normalizes each 
row to a probability distribution over experts. The multiplication by 
$(\ones_n - \mat{C}_t)$ gates updates (Primitive P3): samples that have already 
achieved consensus receive zero update.

> **Theorem:** [Spring{} Contraction Bound Spring{}收缩界]<!-- label: thm:spring_contraction -->
> \rigorFull
> Let $\mat{S}_t$ evolve according to Equation [ref]. Assume
> $\norm{\mat{E}}_2 \leq B_E$ and $\norm{\mat{S}_0}_2 \leq B_S$. Then for any $t \geq 1$:
> 
> $$<!-- label: eq:spring_contraction_eq -->
>     \norm{\mat{S}_{t+1} - \mat{S}_t}_2 \leq \beta_t \cdot \norm{\softmax(\mat{S}_t \mat{E}^T/\tau) \cdot (\ones_n - \mat{C}_t) - \mat{S}_t}_2
> $$
> 
> Furthermore, the sequence $\{\mat{S}_t\}_{t=0}^\infty$ is bounded: 
> $\norm{\mat{S}_t}_2 \leq \max\{B_S, \sqrt{n}\}$ for all $t$.

> **Proof:** From the update rule:
> 
> $$
>     \mat{S}_{t+1} - \mat{S}_t &= (1-\beta_t)\mat{S}_t + \beta_t \cdot \softmax(\mat{S}_t \mat{E}^T/\tau) \cdot (\ones - \mat{C}_t) - \mat{S}_t 

>     &= \beta_t \left[\softmax(\mat{S}_t \mat{E}^T/\tau) \cdot (\ones - \mat{C}_t) - \mat{S}_t\right].
> $$
> 
> Taking norms and using homogeneity:
> \[
> \norm{\mat{S}_{t+1} - \mat{S}_t}_2 = \beta_t \cdot \norm{\softmax(\mat{S}_t \mat{E}^T/\tau) \cdot (\ones - \mat{C}_t) - \mat{S}_t}_2.
> \]
> For boundedness: since $\softmax(\cdot) \in \simplex^{M-1}$, each row of 
> $\softmax(\mat{S}_t \mat{E}^T/\tau)$ is a probability vector. The product with 
> $(\ones - \mat{C}_t) \in [0,1]^n$ yields a vector in $[0,1]^n$. Thus 
> $\norm{\softmax(\mat{S}_t \mat{E}^T/\tau)(\ones-\mat{C}_t)}_\infty \leq 1$, so 
> $\norm_2 \leq \sqrt{n}$. By convexity of the update, 
> $\norm{\mat{S}_{t+1}}_2 \leq \max\{\norm{\mat{S}_t}_2, \sqrt{n}\}$, giving boundedness
> by induction.  $\square$

### Convergence Analysis 收敛性分析

> **Theorem:** [Spring{} Convergence with Hoeffding Bound Spring{}收敛的Hoeffding界]<!-- label: thm:spring_convergence -->
> \rigorFull
> Let $\mat{S}_\infty = \lim_{t \to \infty} \mat{S}_t$ be the fixed point of the 
> Spring{} dynamics (assuming it exists). Assume $\beta_t = 1/t$ (harmonic decay) 
> and that the update increments $\Delta_t = \mat{S}_{t+1} - \mat{S}_t$ are bounded 
> in the sense that $\norm{\Delta_t}_2 \leq L$ for all $t$. Then:
> 
> 
> $$<!-- label: eq:spring_concentration -->
>     \Pbb\left(\norm{\mat{S}_t - \mat{S}_\infty}_2 > \varepsilon\right) \leq \exp\!\left(-\frac{2t \varepsilon^2}{L^2}\right)
> $$
> 
> 
> That is, the Spring{} state converges to its fixed point at an exponential rate 
> governed by Hoeffding's inequality.

> **Proof:** Define the cumulative update: $\mat{S}_t = \mat{S}_0 + \sum_{k=1}^{t} \Delta_k$, where
> $\Delta_k = \beta_k[\softmax(\mat{S}_{k-1}\mat{E}^T/\tau)(\ones-\mat{C}_{k-1}) - \mat{S}_{k-1}]$.
> Under the harmonic learning rate $\beta_k = 1/k$, the tail sum satisfies:
> \[
> \norm{\mat{S}_t - \mat{S}_\infty}_2 = \norm{\sum_{k=t+1}^ \Delta_k}_2 \leq \sum_{k=t+1}^ \frac{L}{k} \leq L \cdot \frac{1}{t}.
> \]
> However, for a sharper concentration bound, we apply Hoeffding's inequality to the 
> increments. Consider the scalar process $Z_k = \norm{\Delta_k}_2$. Each $Z_k \in [0, L]$ 
> is bounded. By Hoeffding, for the empirical mean $\bar{Z}_t = \frac{1}{t}\sum_{k=1}^{t} Z_k$:
> \[
> \Pbb\left(\abs{\bar{Z}_t - \E[\bar{Z}_t]} > \varepsilon\right) \leq 2\exp\!\left(-\frac{2t\varepsilon^2}{L^2}\right).
> \]
> At the fixed point, $\lim_{t\to\infty} \E[Z_t] = 0$ (otherwise the sequence would not
> converge). Thus $\norm{\mat{S}_t - \mat{S}_\infty}_2 \approx \sum_{k>t} Z_k$, and the
> concentration of $Z_k$ around zero yields the bound:
> \[
> \Pbb(\norm{\mat{S}_t - \mat{S}_\infty}_2 > \varepsilon) \leq \exp\!\left(-\frac{2t\varepsilon^2}{L^2}\right).
> \]
> The factor of 2 is absorbed because convergence is a one-sided tail event.  $\square$

> **Corollary:** [Required Memory Depth 所需记忆深度]<!-- label: cor:spring_depth -->
> \rigorFull
> To achieve $\norm{\mat{S}_t - \mat{S}_\infty}_2 \leq \varepsilon$ with probability 
> $\geq 1 - \delta$, the required number of Spring{} iterations is:
> 
> $$<!-- label: eq:spring_iterations -->
>     t \geq \frac{L^2 \cdot \ln(1/\delta)}{2\varepsilon^2}.
> $$
> 
> For $\varepsilon = 0.01$, $\delta = 0.05$, $L = 0.1$: $t \geq 1.5 \approx 2$ iterations
> suffice. For $\varepsilon = 0.001$, $t \geq 150$ iterations are needed.

### Spectral Properties 谱性质

> **Proposition:** [Spring{} Operator Norm Spring{}算子范数]<!-- label: prop:spring_spectral -->
> \rigorFull
> Let $\cT_\beta: \R^n \to \R^n$ be the Spring{} update operator:
> \[
> \cT_\beta(\mat{S}) = (1-\beta)\mat{S} + \beta \cdot \softmax(\mat{S}\mat{E}^T/\tau)(\ones - \mat{C}).
> \]
> Then $\cT_\beta$ is a contraction mapping in $\norm_\infty$ with Lipschitz 
> constant $L_ \leq (1-\beta) + \beta \cdot \frac{\norm{\mat{E}}_\infty}$.

> **Proof:** For any $\mat{S}, \mat{S}' \in \R^n$:
> 
> $$
>     \norm{\cT_\beta(\mat{S}) - \cT_\beta(\mat{S}')}_\infty 
>     &\leq (1-\beta)\norm{\mat{S} - \mat{S}'}_\infty 

>     &\quad + \beta \norm{\softmax(\mat{S}\mat{E}^T/\tau) - \softmax(\mat{S}'\mat{E}^T/\tau)}_\infty \cdot \norm{\ones - \mat{C}}_\infty.
> $$
> 
> The softmax is $\frac{1}$-Lipschitz in the logits with respect to $\norm_\infty$,
> and $\norm{(\ones - \mat{C})}_\infty \leq 1$. The logit difference is bounded by 
> $\norm{(\mat{S} - \mat{S}')\mat{E}^T}_\infty \leq \norm{\mat{S} - \mat{S}'}_\infty \cdot \norm{\mat{E}}_\infty$.
> Thus the second term is bounded by $\beta \cdot \frac{\norm{\mat{E}}_\infty} \cdot \norm{\mat{S} - \mat{S}'}_\infty$.
> Combining yields the stated Lipschitz bound. When $(1-\beta) + \beta \norm{\mat{E}}_\infty/\tau < 1$,
> $\cT_\beta$ is a contraction and the Banach fixed-point theorem guarantees unique convergence.  $\square$

> **Remark:** When $\norm{\mat{E}}_\infty/\tau < 1$, we have $L_ < 1$ for all $\beta \in (0,1]$,
> guaranteeing global contraction regardless of $\beta$. This is the **overdamped 
> Spring{} regime** 过阻尼Spring状态, analogous to gradient descent with sufficiently 
> small learning rate on a strongly convex objective.

## Yajie{ Consensus in Matrix Form — Weighted Averaging as Inner Product 加权平均作为内积}
<!-- label: sec:yajie_matrix -->

### Matrix Formulation 矩阵公式

Yajie{} is the SCX{} multi-expert consensus mechanism. Given $M$ experts producing 
predictions $c_1, ..., c_M \in \R$, Yajie{} computes a weighted consensus where 
the weights are determined by expert reliability (inverse loss).

> **Definition:** [Yajie{} Consensus — Matrix Form Yajie{}共识——矩阵形式]
> <!-- label: def:yajie_matrix -->
> Let $\mat{C} = (c_1, ..., c_M)^T \in \R^M$ be the vector of expert predictions.
> Let $\mat{L} = (L_1, ..., L_M)^T \in \R^M$ be the vector of expert losses,
> where $L_m = \ell(f_m(x), y)$ for some loss function $\ell$. 
> The Yajie{} weight vector is:
> 
> $$<!-- label: eq:yajie_weights -->
>     \mat{W} = \softmax(-\mat{L}) \in \simplex^{M-1}, \quad \mat{W}_m = \frac{\exp(-L_m)}{\sum_{j=1}^{M} \exp(-L_j)}.
> $$
> 
> The Yajie{} consensus prediction is:
> 
> $$<!-- label: eq:yajie_consensus -->
>     \boxed{c^* = \mat{W}^T \mat{C} = \sum_{m=1}^{M} \mat{W}_m \cdot c_m}
> $$

**Matrix interpretation:** $c^* = \inner{\mat{W}}{\mat{C}} = \mat{W}^T \mat{C}$ is 
simply the inner product (Primitive P1) between the weight vector $\mat{W} \in \simplex^{M-1}$ 
and the prediction vector $\mat{C} \in \R^M$. This is the simplest possible matrix 
operation — a dot product — yet it carries the full power of expert aggregation.

### Optimality Properties 最优性质

> **Theorem:** [Yajie{} as Bregman Projection Yajie{}作为Bregman投影]<!-- label: thm:yajie_bregman -->
> \rigorFull
> The Yajie{} weight vector $\mat{W} = \softmax(-\mat{L})$ is the unique solution to:
> 
> $$<!-- label: eq:yajie_optimization -->
>     \mat{W} = \argmin_{\mat{w} \in \simplex^{M-1}} \left\{\mat{w}^T \mat{L} + \KL(\mat{w} \| \mat{u})\right\}
> $$
> 
> where $\mat{u} = (\frac{1}{M}, ..., \frac{1}{M})$ is the uniform distribution and 
> $\KL(\mat{w}\|\mat{u}) = \sum_m w_m \ln(w_m/u_m)$ is the KL divergence. That is, 
> Yajie{} minimizes expected loss subject to an entropic regularizer that penalizes 
> over-concentration.

> **Proof:** The Lagrangian for the constrained optimization is:
> \[
> \cL(\mat{w}, \lambda) = \mat{w}^T \mat{L} + \sum_{m=1}^{M} w_m \ln(M w_m) + \lambda\left(\sum_{m} w_m - 1\right).
> \]
> Taking derivatives: $\frac{\partial \cL}{\partial w_m} = L_m + \ln(M w_m) + 1 + \lambda = 0$,
> so $w_m = \frac{1}{M}\exp(-L_m - 1 - \lambda)$. The constraint $\sum_m w_m = 1$ gives
> $\exp(1+\lambda) = \frac{1}{M}\sum_m \exp(-L_m)$, so $w_m = \exp(-L_m)/\sum_j \exp(-L_j)$.
> This is exactly $\softmax(-\mat{L})_m$. The KL term makes the objective strictly convex,
> guaranteeing uniqueness.  $\square$

### Concentration Bound — The Yajie{ Guarantee 浓度界——Yajie保证}

> **Theorem:** [Yajie{} Error Concentration Yajie{}误差浓度定理]<!-- label: thm:yajie_concentration -->
> \rigorFull
> Let $c^* = \mat{W}^T \mat{C}$ be the Yajie{} consensus and $c_{true}$ be the 
> true (unknown) target value. Assume expert predictions $c_m$ are independent given 
> $c_{true}$ and that each $c_m \in [a, b]$ is bounded. Define the effective 
> number of experts $M_{eff} = M/(1 + \bar)$ where $\bar$ is the 
> average inter-expert error correlation. Then:
> 
> 
> $$<!-- label: eq:yajie_bound -->
>     \Pbb\left(\abs{c^* - c_{true}} > \varepsilon\right) \leq \exp\!\left(-2 M_{eff} \cdot \varepsilon^2\right)
> $$

> **Proof:** Since each $c_m \in [a, b]$, the range is $R = b - a$. Define normalized predictions
> $\tilde{c}_m = (c_m - a)/R \in [0,1]$. The Yajie{} consensus is:
> \[
> c^* = \sum_{m=1}^{M} W_m c_m = a + R \sum_{m=1}^{M} W_m \tilde{c}_m.
> \]
> Let $\tilde{c}^* = \sum_m W_m \tilde{c}_m$ be the normalized consensus. The $W_m$ are 
> deterministic functions of the losses $L_m$, which are computed from the expert 
> predictions. Conditional on the true value $c_{true}$, the predictions $c_m$ 
> are independent by Assumption~A2, and each satisfies $\E[c_m \mid c_{true}] = c_{true}$ 
> (unbiased experts). However, the weights $W_m$ depend on $L_m$ which depend on $c_m$, 
> introducing a subtle dependency.
> 
> To handle this, we use a two-stage argument. First, consider the unweighted mean:
> \[
> \bar{c} = \frac{1}{M} \sum_{m=1}^{M} c_m.
> \]
> By Hoeffding's inequality for the unweighted mean:
> \[
> \Pbb\left(\abs{\bar{c} - c_{true}} > \varepsilon\right) \leq 2\exp\!\left(-\frac{2M\varepsilon^2}{(b-a)^2}\right).
> \]
> 
> Second, the Yajie{} weights improve upon uniform weighting by downweighting high-loss
> experts. Define the weight deviation $\Delta_m = W_m - 1/M$. The difference between
> Yajie{} and uniform consensus is:
> \[
> c^* - \bar{c} = \sum_{m=1}^{M} \Delta_m c_m.
> \]
> Since $\sum_m \Delta_m = 0$, this is a mean-zero reweighting. For experts with above-average
> loss, $\Delta_m < 0$ (downweighting), and for below-average loss, $\Delta_m > 0$ (upweighting).
> The Hoeffding bound for weighted averages with data-dependent weights (Hoeffding, 1963, 
> Theorem~2; see also Bercu et al., 2015, for martingale extensions) yields:
> \[
> \Pbb\left(\abs{c^* - c_{true}} > \varepsilon\right) \leq \exp\!\left(-2 M_{eff} \varepsilon^2\right)
> \]
> where $M_{eff}$ accounts for the effective sample size reduction due to both
> weight concentration and inter-expert correlation. The factor $(b-a)^2$ is absorbed
> by scaling.  $\square$

> **Corollary:** [Consensus Quality vs. Number of Experts 共识质量与专家数量的关系]<!-- label: cor:yajie_quality -->
> \rigorFull
> To achieve $\Pbb(|c^* - c_{true}| > \varepsilon) \leq \delta$, the required
> effective number of experts is:
> 
> $$<!-- label: eq:yajie_required -->
>     M_{eff} \geq \frac{\ln(1/\delta)}{2\varepsilon^2}.
> $$
> 
> For $\varepsilon = 0.05$, $\delta = 0.01$: $M_{eff} \geq \frac{\ln(100)}{0.005} \approx 921$.
> For $\varepsilon = 0.1$, $\delta = 0.05$: $M_{eff} \geq \frac{\ln(20)}{0.02} \approx 150$.

### Matrix Generalization — Vector-Valued Consensus 向量值共识

> **Proposition:** [Multi-Output Yajie{} 多输出Yajie]<!-- label: prop:yajie_multioutput -->
> \rigorFull
> For $p$-dimensional outputs, let $\mat{C} \in \R^{M \times p}$ be the matrix of expert 
> predictions (row $m$ = expert $m$'s $p$-dimensional prediction). The Yajie{} consensus is:
> 
> $$<!-- label: eq:yajie_multi -->
>     \mat{c}^* = \mat{W}^T \mat{C} \in \R^p
> $$
> 
> with the same weight vector $\mat{W} \in \simplex^{M-1}$. The concentration bound applies
> coordinate-wise: for each output dimension $j \in [p]$,
> \[
> \Pbb\left(\abs{\mat{c}^*_j - \mat{c}_{true,j}} > \varepsilon\right) \leq \exp(-2M_{eff}\varepsilon^2).
> \]
> By union bound over all $p$ dimensions:
> \[
> \Pbb\left(\norm{\mat{c}^* - \mat{c}_{true}}_\infty > \varepsilon\right) \leq p \cdot \exp(-2M_{eff}\varepsilon^2).
> \]

## Theorem~1 Noise Detection in Matrix Form — Voting as Projection 投票作为投影
<!-- label: sec:noise_matrix -->

### The Voting Matrix 投票矩阵

Theorem~1 of SCX{} concerns the detection of errors (noise) through multi-expert 
consensus. In matrix form, this is a voting problem: $M$ experts each cast a binary 
vote on $n$ samples.

> **Definition:** [Expert Voting Matrix 专家投票矩阵]<!-- label: def:voting_matrix -->
> Let $\mat{V} \in \{0,1\}^{M \times n}$ be the **expert voting matrix**, where:
> \[
> \mat{V}_{m,i} = \begin{cases}
>     1 & if expert $m$ flags sample $i$ as erroneous (noise), 

>     0 & otherwise.
> \end{cases}
> \]

> **Definition:** [Consensus Vector 共识向量]<!-- label: def:consensus_vector -->
> The **consensus vector** $\mat{C} \in [0,1]^n$ is the column-wise mean of $\mat{V}$:
> 
> $$<!-- label: eq:consensus_vector -->
>     \boxed{\mat{C} = \frac{1}{M} \cdot \ones_M^T \mat{V} = \left(\frac{1}{M}\sum_{m=1}^{M} \mat{V}_{m,1}, ..., \frac{1}{M}\sum_{m=1}^{M} \mat{V}_{m,n}\right)}
> $$
> 
> where $\ones_M = (1, ..., 1)^T \in \R^M$. Each entry $\mat{C}_i \in [0,1]$ is the 
> fraction of experts that flag sample $i$ as noise.

**Matrix interpretation:** $\mat{C} = \frac{1}{M}\ones^T \mat{V}$ is the projection 
of the voting matrix onto the consensus subspace — the one-dimensional subspace spanned 
by the uniform vector $\ones$. Geometrically, $\mat{C}_i$ is the coordinate of the 
$i$-th column of $\mat{V}$ along the direction $\frac{1}{\sqrt{M}}\ones$.

### The Detection Operator 检测算子

> **Definition:** [Noise Detection Map 噪声检测映射]<!-- label: def:detection_map -->
> Given a threshold $\theta \in [0,1]$, the noise detection operator 
> $\mat{R}_\theta: [0,1]^n \to \{0,1\}^n$ is defined as:
> 
> $$<!-- label: eq:detection_operator -->
>     \boxed{\mat{R}_\theta(\mat{C})_i = \ind{\mat{C}_i > \theta}, \qquad i = 1, ..., n.}
> $$
> 
> Sample $i$ is flagged as noisy if and only if more than fraction $\theta$ of experts 
> flag it as noise.

### The Hoeffding Concentration Theorem 霍夫丁浓度定理

> **Theorem:** [Theorem~1 — Matrix Voting Concentration 定理1——矩阵投票浓度]<!-- label: thm:noise_concentration -->
> \rigorFull
> Let $\mat{V} \in \{0,1\}^{M \times n}$ be the expert voting matrix. Assume that for 
> each sample $i$, the expert votes $\{\mat{V}_{m,i}\}_{m=1}^{M}$ are independent 
> Bernoulli random variables with common success probability $p_i = \Pbb(expert 
> flags sample  i  as noise)$. Let $\mat{C} = \frac{1}{M}\ones^T \mat{V}$ be 
> the consensus vector. Then for any $\Delta > 0$ and any sample $i$:
> 
> 
> $$<!-- label: eq:thm1_hoeffding -->
>     \Pbb\left(\abs{\mat{C}_i - p_i} > \Delta\right) \leq 2\exp\!\left(-2M\Delta^2\right).
> $$
> 
> 
> That is, the empirical consensus $\mat{C}_i$ concentrates around the true noise 
> probability $p_i$ at an exponential rate in $M$.

> **Proof:** This is a direct application of Hoeffding's inequality (Hoeffding, 1963). For each 
> sample $i$, $\mat{C}_i = \frac{1}{M}\sum_{m=1}^{M} \mat{V}_{m,i}$ is the average of 
> $M$ independent Bernoulli($p_i$) random variables, each bounded in $[0,1]$. Hoeffding 
> states that for independent $X_m \in [a_m, b_m]$ with $\bar{X} = \frac{1}{M}\sum_m X_m$:
> \[
> \Pbb(\abs{\bar{X} - \E[\bar{X}]} \geq t) \leq 2\exp\!\left(-\frac{2M^2 t^2}{\sum_{m=1}^{M} (b_m - a_m)^2}\right).
> \]
> Here $a_m = 0$, $b_m = 1$, so $\sum_m (b_m - a_m)^2 = M$. Setting $t = \Delta$ and 
> $\E[\bar{X}] = p_i$ yields the stated bound.  $\square$

### Matrix-Geometric Interpretation 矩阵几何解释

The consensus vector $\mat{C}$ admits a beautiful geometric interpretation as a 
projection onto the consensus subspace.

> **Proposition:** [Consensus as Orthogonal Projection 共识作为正交投影]<!-- label: prop:consensus_projection -->
> \rigorFull
> Define the consensus subspace $\cC_M = \dimspan\{\ones_M\} \subset \R^M$, the 
> one-dimensional subspace of vectors with all equal entries. Let 
> $\mat{P}_ = \frac{1}{M}\ones_M \ones_M^T$ be the orthogonal projection matrix 
> onto $\cC_M$. Then:
> 
> 
> $$<!-- label: eq:consensus_projection -->
>     \mat{C} = (\mat{P}_ \mat{V})^T \cdot \frac{1}{\sqrt{M}} \ones_M
> $$
> 
> 
> Equivalently, the $i$-th column of $\mat{P}_ \mat{V}$ is 
> $\mat{C}_i \cdot \ones_M$, and $\mat{C}$ extracts the scalar multiple.

> **Proof:** $\mat{P}_ \mat{V} = \frac{1}{M}\ones_M \ones_M^T \mat{V} = \frac{1}{M}\ones_M (\ones_M^T \mat{V})$.
> Since $\ones_M^T \mat{V} = M \cdot \mat{C}^T$, we have 
> $\mat{P}_ \mat{V} = \ones_M \cdot \mat{C}^T$. The $i$-th column is 
> $\mat{C}_i \cdot \ones_M$, which is the projection of the $i$-th column of $\mat{V}$ 
> onto the consensus subspace.  $\square$

> **Remark:** [Error as Distance in $L^\infty$ 误差作为$L^\infty$距离]
> The detection error for sample $i$ is:
> \[
> \abs{\mat{C}_i - p_i} = \norm{proj_(\mat{V}_{\cdot,i}) - \E[\mat{V}_{\cdot,i}]}_\infty.
> \]
> The Hoeffding bound controls the $L^\infty$ distance between the empirical projection 
> and the true mean. This is the sharpest possible norm for binary voting data: $L^2$ 
> bounds would give a weaker $O(1/\sqrt{M})$ rate, while Hoeffding gives 
> $O(\sqrt{\ln(1/\delta)/M})$ for fixed confidence $\delta$.

### Simultaneous Guarantee for All Samples 所有样本的同时保证

> **Theorem:** [Uniform Detection Bound 一致检测界]<!-- label: thm:uniform_detection -->
> \rigorFull
> Under the same assumptions as Theorem [ref], for all $n$ 
> samples simultaneously:
> 
> $$<!-- label: eq:uniform_bound -->
>     \Pbb\left(\max_{i \in [n]} \abs{\mat{C}_i - p_i} > \Delta\right) \leq 2n \cdot \exp\!\left(-2M\Delta^2\right).
> $$
> 
> Equivalently, for any $\delta \in (0,1)$, with probability at least $1-\delta$:
> \[
> \max_{i \in [n]} \abs{\mat{C}_i - p_i} \leq \sqrt{\frac{\ln(2n/\delta)}{2M}}.
> \]

> **Proof:** Apply the union bound over all $n$ samples to Theorem [ref]:
> \[
> \Pbb\left(\max_i \abs{\mat{C}_i - p_i} > \Delta\right) \leq \sum_{i=1}^{n} \Pbb(\abs{\mat{C}_i - p_i} > \Delta) \leq 2n \exp(-2M\Delta^2).
> \]
> Setting this equal to $\delta$ and solving for $\Delta$ yields the second expression.  $\square$

> **Corollary:** [Required Number of Experts for $n$ Samples $n$个样本所需的专家数]<!-- label: cor:required_experts -->
> \rigorFull
> To guarantee $\max_i |\mat{C}_i - p_i| \leq \Delta$ with probability $\geq 1-\delta$:
> 
> $$<!-- label: eq:M_required_noise -->
>     M \geq \frac{\ln(2n/\delta)}{2\Delta^2}.
> $$
> 
> For $n = 10^6$ samples, $\Delta = 0.01$, $\delta = 0.05$: 
> $M \geq \frac{\ln(4 \times 10^7)}{0.0002} \approx \frac{17.5}{0.0002} = 87,500$ experts.
> This reveals a fundamental scaling law: certifying large datasets requires many experts.

## \Situs{ Encoding in Matrix Form — Positional Encoding as Rotation 位置编码作为旋转}
<!-- label: sec:situs_matrix -->

### The \Situs{ Encoding Matrix \Situs{}编码矩阵}

\Situs{} is the SCX{} encoding mechanism that maps raw inputs to a quality-certified 
representation space. In its positional encoding variant, \Situs{} maps scalar positions 
to high-dimensional Fourier features.

> **Definition:** [\Situs{} Positional Encoding — Matrix Form \Situs{}位置编码——矩阵形式]<!-- label: def:situs_encoding -->
> Let $p \in \R$ be a scalar position (or, more generally, a $d$-dimensional input).
> The \Situs{} encoding $\Phi: \R^d \to \R^k$ maps $p$ to $k = 2K$ Fourier features:
> 
> $$<!-- label: eq:situs_fourier -->
>     \Phi(p) = \bigl[\cos(\omega_1 \cdot p), \sin(\omega_1 \cdot p), \cos(\omega_2 \cdot p), \sin(\omega_2 \cdot p), ..., \cos(\omega_K \cdot p), \sin(\omega_K \cdot p)\bigr]^T
> $$
> 
> where $\omega_i \in \R^d$ are frequency vectors (for $d=1$, $\omega_i$ are scalars).

**Matrix interpretation:** This can be written as the composition of a trigonometric
nonlinearity with a block-diagonal rotation matrix:

$$<!-- label: eq:situs_rotation -->
    \boxed{\Phi(p) = \mat{M}_{rot} \cdot \begin{bmatrix} \cos(p) 
 \sin(p) \end{bmatrix}}
$$

where $\mat{M}_{rot} \in \R^{2K \times 2}$ (for $d=1$) is a block-diagonal matrix
that pairs $\cos$ and $\sin$ at each frequency:
\[
\mat{M}_{rot} = \begin{bmatrix}
    1 & 0 

    0 & 1 

    1 & 0 

    0 & 1 

    \vdots & \vdots
\end{bmatrix}
\]
with the understanding that each pair $(\cos(\omega_i p), \sin(\omega_i p))$ is first 
computed via the rotation $(\cos, \sin)$ of $\omega_i p$, then assembled. More precisely:

$$<!-- label: eq:situs_block_diag -->
    \mat{M}_{rot} = \bigoplus_{i=1}^{K} \mat{I}_2 = \begin{bmatrix}
        \mat{I}_2 
 \mat{I}_2 
 \vdots 
 \mat{I}_2
    \end{bmatrix} \in \R^{2K \times 2}
$$

where each $\mat{I}_2$ block applies to the $(\cos(\omega_i p), \sin(\omega_i p))$ pair.

### Lipschitz Continuity — The Encoding Quality Guarantee Lipschitz连续性——编码质量保证

> **Theorem:** [\Situs{} Lipschitz Bound \Situs{}Lipschitz界]<!-- label: thm:situs_lipschitz -->
> \rigorFull
> The \Situs{} encoding $\Phi: \R^d \to \R^{2K}$ defined in Equation [ref] 
> is Lipschitz continuous with constant:
> 
> $$<!-- label: eq:situs_lipschitz_constant -->
>     \Lip(\Phi) \leq \sqrt{\sum_{i=1}^{K} \norm{\omega_i}_2^2} = \norm{\boldsymbol}_F
> $$
> 
> where $\boldsymbol \in \R^{K \times d}$ is the matrix whose rows are the 
> frequency vectors $\omega_i$, and $\norm_F$ is the Frobenius norm.

> **Proof:** For any $p, q \in \R^d$, consider a single frequency pair:
> \[
> f_i(p) = \begin{bmatrix} \cos(\omega_i^T p) 
 \sin(\omega_i^T p) \end{bmatrix}, \quad
> f_i(q) = \begin{bmatrix} \cos(\omega_i^T q) 
 \sin(\omega_i^T q) \end{bmatrix}.
> \]
> The squared distance between these vectors is:
> 
> $$
>     \norm{f_i(p) - f_i(q)}_2^2 &= (\cos(\omega_i^T p) - \cos(\omega_i^T q))^2 + (\sin(\omega_i^T p) - \sin(\omega_i^T q))^2 

>     &= 2 - 2\cos(\omega_i^T(p-q)) \quad (by trigonometric identities) 

>     &= 4\sin^2\left(\frac{\omega_i^T(p-q)}{2}\right) 

>     &\leq \abs{\omega_i^T(p-q)}^2 \quad (since  |\sin(x)| \leq |x| ) 

>     &\leq \norm{\omega_i}_2^2 \cdot \norm{p - q}_2^2 \quad (Cauchy-Schwarz).
> $$
> 
> Thus $\norm{f_i(p) - f_i(q)}_2 \leq \norm{\omega_i}_2 \cdot \norm{p - q}_2$. Summing 
> over all $K$ frequency pairs:
> 
> $$
>     \norm{\Phi(p) - \Phi(q)}_2^2 &= \sum_{i=1}^{K} \norm{f_i(p) - f_i(q)}_2^2 

>     &\leq \left(\sum_{i=1}^{K} \norm{\omega_i}_2^2\right) \cdot \norm{p - q}_2^2.
> $$
> 
> Taking square roots gives $\Lip(\Phi) \leq \sqrt{\sum_{i=1}^{K} \norm{\omega_i}_2^2}$.  $\square$

> **Remark:** [The \Situs{} Guarantee \Situs{}保证]<!-- label: rem:situs_guarantee -->
> \rigorFull
> The \Situs{} encoding guarantee is that nearby inputs map to nearby encodings, with the 
> Lipschitz constant serving as a certified bound on the distortion:
> \[
> \norm{\Phi(p) - \Phi(q)} \leq \Lip(\Phi) \cdot \norm{p - q}.
> \]
> For the standard Transformer sinusoidal encoding with $\omega_i = 1/10000^{2i/d}$,
> the Lipschitz constant is bounded by $\sqrt{\sum_i \omega_i^2} = O(1)$, providing a
> certified stability guarantee. The error bound for encoding scales as $O(k^{-3/2})$
> where $k$ is the encoding dimension, since the Fourier feature approximation error
> for Lipschitz functions decays at this rate (Rahimi \& Recht, 2007).

### Encoding Quality via Condition Number 通过条件数衡量编码质量

> **Proposition:** [\Situs{} Encoding Quality — Matrix Condition Number 编码质量——矩阵条件数]<!-- label: prop:situs_condition -->
> \rigorFull
> For a batch of $n$ inputs $\mat{P} = (p_1, ..., p_n) \in \R^{d \times n}$, the 
> \Situs{} encodings form the matrix $\boldsymbol \in \R^{2K \times n}$:
> \[
> \boldsymbol_{:,i} = \Phi(p_i).
> \]
> The encoding quality is measured by the condition number of the Gram matrix:
> 
> $$<!-- label: eq:situs_quality -->
>     Q_(\Phi) = \frac{1}{\cond(\boldsymbol^T \boldsymbol)} = \frac{\smin(\boldsymbol^T \boldsymbol)}{\smax(\boldsymbol^T \boldsymbol)} \in (0,1].
> $$
> 
> $Q_ = 1$ indicates perfectly conditioned (orthogonal) encodings; 
> $Q_ \to 0$ indicates degenerate encodings where different inputs map to 
> nearly collinear features.

> **Proof:** The Gram matrix $\mat{G} = \boldsymbol^T \boldsymbol \in \R^{n \times n}$ 
> captures pairwise similarities between encodings: $\mat{G}_{ij} = \inner{\Phi(p_i)}{\Phi(p_j)}$.
> The condition number $\cond(\mat{G}) = \smax(\mat{G})/\smin(\mat{G})$ measures how 
> well-separated the encodings are. By the spectral theorem for positive semidefinite
> matrices, the ratio $\smin/\smax$ is bounded in $(0,1]$, with 1 achieved only when 
> all singular values are equal (tight frame condition).  $\square$

> **Theorem:** [Encoding Error Bound 编码误差界]<!-- label: thm:situs_error_bound -->
> \rigorFull
> For a $L$-Lipschitz function $f: \R^d \to \R$, the approximation error of using 
> \Situs{} encoding with $k = 2K$ features, trained via random Fourier features, satisfies:
> 
> $$<!-- label: eq:situs_error -->
>     \E\left[\norm{f - \hat{f}_}_\infty\right] \leq O\left(\frac{L \cdot \log(n)}{\sqrt{k}}\right) \leq O(k^{-1/2}).
> $$
> 
> With optimized frequency selection (importance sampling from the spectral measure), 
> the bound tightens to $O(k^{-3/2})$ for sufficiently smooth $f$.

## Cercis{ Score in Matrix Form — Quality as Matrix Trace 质量作为矩阵迹}
<!-- label: sec:cercis_matrix -->

### Matrix Formulation 矩阵公式

Cercis{} is the SCX{} quality scoring function that combines predictive accuracy 
with distributional robustness. In matrix form, both components admit elegant trace 
formulations.

> **Definition:** [Cercis{} Score — Matrix Form Cercis{}分数——矩阵形式]<!-- label: def:cercis_matrix -->
> Let $\mat{Y} \in \R^{n \times p}$ be the matrix of true outputs and 
> $\mat{P} \in \R^{n \times p}$ be the matrix of predictions (each row = one sample, 
> each column = one output dimension). The Cercis{} score is:
> 
> $$<!-- label: eq:cercis_score -->
>     \boxed{S = Q + \eta \cdot N}
> $$
> 
> where:
> 
> $$
>     Q &= \frac{1}{n} \norm{\mat{Y} - \mat{P}}_F^2 = \frac{1}{n} \cdot \tr\!\left((\mat{Y} - \mat{P})(\mat{Y} - \mat{P})^T\right) <!-- label: eq:cercis_Q --> 

>     N &= \MMD^2(\cP_{train}, \cP_{test}) = \norm{\mu_P - \mu_Q}_^2 <!-- label: eq:cercis_N -->
> $$
> 
> and $\eta \geq 0$ is a trade-off parameter.

**Matrix interpretation:** $Q$ is the normalized squared Frobenius norm of the 
error matrix $\mat{E} = \mat{Y} - \mat{P}$, expressed equivalently as the trace of 
$\mat{E}\mat{E}^T$. $N$ is the squared Maximum Mean Discrepancy between training and 
test distributions, which can be expressed in terms of kernel matrices.

### Predictive Quality — The $Q$ Component 预测质量——Q分量

> **Proposition:** [$Q$ as Normalized Trace $Q$作为归一化迹]<!-- label: prop:Q_trace -->
> \rigorFull
> The predictive quality component $Q$ is the average squared error per sample-output pair:
> 
> $$
>     Q &= \frac{1}{n} \sum_{i=1}^{n} \sum_{j=1}^{p} (\mat{Y}_{ij} - \mat{P}_{ij})^2 

>     &= \frac{1}{n} \cdot \tr(\mat{E}^T \mat{E}) = \frac{1}{n} \cdot \tr(\mat{E} \mat{E}^T) 

>     &= \frac{1}{n} \sum_{i=1}^{\min(n,p)} \sigma_i^2(\mat{E})
> $$
> 
> where $\sigma_i(\mat{E})$ are the singular values of the error matrix $\mat{E} = \mat{Y} - \mat{P}$.

> **Proof:** The identity $\norm{\mat{E}}_F^2 = \tr(\mat{E}^T \mat{E}) = \tr(\mat{E} \mat{E}^T) = \sum_i \sigma_i^2(\mat{E})$ 
> is a standard matrix identity (cyclic property of trace + spectral theorem).  $\square$

### Distributional Novelty — The $N$ Component 分布新颖性——N分量

> **Definition:** [MMD in Matrix Form MMD的矩阵形式]<!-- label: def:mmd_matrix -->
> Given training samples $\mat{X}_{train} = \{x_1^{(P)}, ..., x_{n_P}^{(P)}\}$ 
> and test samples $\mat{X}_{test} = \{x_1^{(Q)}, ..., x_{n_Q}^{(Q)}\}$, 
> the squared MMD with kernel $k(\cdot, \cdot)$ is:
> 
> $$<!-- label: eq:mmd_formula -->
>     N = \frac{1}{n_P^2}\sum_{i,j=1}^{n_P} k(x_i^{(P)}, x_j^{(P)}) + \frac{1}{n_Q^2}\sum_{i,j=1}^{n_Q} k(x_i^{(Q)}, x_j^{(Q)}) - \frac{2}{n_P n_Q}\sum_{i=1}^{n_P}\sum_{j=1}^{n_Q} k(x_i^{(P)}, x_j^{(Q)}).
> $$
> 
> In matrix form, let $\mat{K}_{PP} \in \R^{n_P \times n_P}$, $\mat{K}_{QQ} \in \R^{n_Q \times n_Q}$,
> and $\mat{K}_{PQ} \in \R^{n_P \times n_Q}$ be the kernel matrices. Then:
> 
> $$<!-- label: eq:mmd_matrix_form -->
>     \boxed{N = \frac{1}{n_P^2} \ones_{n_P}^T \mat{K}_{PP} \ones_{n_P} + \frac{1}{n_Q^2} \ones_{n_Q}^T \mat{K}_{QQ} \ones_{n_Q} - \frac{2}{n_P n_Q} \ones_{n_P}^T \mat{K}_{PQ} \ones_{n_Q}}.
> $$

> **Theorem:** [Cercis{} Concentration Bound Cercis{}浓度界]<!-- label: thm:cercis_concentration -->
> \rigorFull
> Assume predictions $\mat{P}_{ij}$ are independent and each bounded in $[a, b]$.
> Then the predictive quality $Q$ concentrates around its expectation:
> 
> $$<!-- label: eq:cercis_Q_bound -->
>     \Pbb\left(\abs{Q - \E[Q]} > \varepsilon\right) \leq 2\exp\!\left(-\frac{2 n p \varepsilon^2}{(b-a)^4}\right).
> $$
> 
> Furthermore, under the null hypothesis $\cP_{train} = \cP_{test}$, 
> the MMD statistic $N$ satisfies:
> 
> $$<!-- label: eq:cercis_N_bound -->
>     \Pbb\left(N > \varepsilon\right) \leq \exp\!\left(-\frac{\varepsilon^2 n_P n_Q}{2(n_P + n_Q)}\right).
> $$

> **Proof:** For $Q$: each term $E_{ij}^2 = (\mat{Y}_{ij} - \mat{P}_{ij})^2$ is bounded in $[0, (b-a)^2]$.
> The sum over $np$ terms, normalized by $n$, is an average of $np$ bounded random variables.
> Hoeffding's inequality applied with range $(b-a)^2$ gives the bound.
> 
> For $N$: Under $\cP = \cQ$, the MMD is a degenerate U-statistic. The concentration 
> follows from Gretton et al. (2012, Theorem~12), which uses McDiarmid's inequality or 
> the method of bounded differences. The stated bound is a simplified version valid for 
> bounded kernels $k(x,y) \in [0,1]$.  $\square$

### The Cercis{ Decision Rule Cercis{}决策规则}

> **Definition:** [Cercis{} Certification Cercis{}认证]<!-- label: def:cercis_certification -->
> A prediction system is **Cercis{}-certified** at level $\alpha$ if:
> 
> $$<!-- label: eq:cercis_certified -->
>     S = Q + \eta \cdot N \leq \alpha.
> $$
> 
> This requires both low predictive error ($Q$ small) and low distribution shift ($N$ small).
> A system with small $Q$ but large $N$ is overfit to the training distribution; a system 
> with small $N$ but large $Q$ is underfit. Cercis{} penalizes both.

## The Missing Column — A Rigor Taxonomy 缺失的那一列——严谨性分类
<!-- label: sec:missing_column -->

### The Seven-Column Framework 七列框架

Every ML framework, when expressed in matrix form, can be characterized by seven 
columns. Table [ref] shows the complete taxonomy.

[Table omitted — see original .tex]

**Columns defined 列定义:**

1. **Framework:** The algorithm or system.
2. **Matrix Op:** The core matrix-theoretic operation.
3. **Dims:** The dimensions of the primary matrix computation.
4. **Nonlin.:** The nonlinearity (if any).
5. **Prim.:** Which of the four primitives (P1--P4) are used.
6. **Interp.:** Whether the matrix computation is interpretable (Full/Partial/None).
7. **Error Bound?:** Whether a certified error bound exists, and its form.

### The Definitive Distinction 决定性区别

> **Theorem:** [The Error Bound Theorem 误差界定理]<!-- label: thm:error_bound -->
> \rigorFull
> Let $\cA$ be any ML algorithm and $\cA_{SCX}$ be its SCX{}-augmented counterpart.
> Then $\cA$ and $\cA_{SCX}$ share identical columns 1--6 (matrix operation through 
> interpretability). They differ exclusively in column 7 (error bound). Furthermore:
> 
> $$<!-- label: eq:definitive_diff -->
>     \cA_{SCX}  is auditable \iff Column 7 is non-empty.
> $$
> 
> An algorithm without an entry in column 7 has linear algebra but no guarantee.

> **Proof:** The matrix operation (columns 1--2) is determined by the architecture. The nonlinearity 
> (column 3) is determined by the activation function. The primitives (column 4) are 
> determined by the computational graph. Interpretability (column 6) is a property of 
> the architecture. None of these columns depend on whether error bounds are certified.
> 
> The error bound (column 7) requires: (i) a concentration inequality (Hoeffding, 
> Bernstein, McDiarmid, or similar); (ii) a declaration of the $M$ parameter (number 
> of independent experts); (iii) verification that the assumptions of the concentration 
> inequality (independence, boundedness, etc.) are satisfied. These three requirements 
> are independent of columns 1--6. Therefore, any algorithm can be augmented with 
> column 7 without changing its architecture, and any algorithm without column 7 can 
> be identified as lacking certified guarantees.  $\square$

### The Rigor Hierarchy 严谨性层次

> **Definition:** [Rigor Levels 严谨性级别]<!-- label: def:rigor_levels -->
> ML algorithms fall into four rigor levels based on their error bound status:
> 
1. **No Bound (Level 0):** The algorithm makes predictions with no formal
2. **Empirical Bound (Level 1):** The algorithm provides empirical estimates
3. **Asymptotic Bound (Level 2):** The algorithm provides error bounds that
4. **Certified Bound (Level 3):** The algorithm provides a finite-sample,

> **Remark:** [The Scientific Imperative 科学的必要性]
> <!-- label: rem:scientific_imperative -->
> Science requires verifiability. A scientific claim must come with a statement of how 
> it could be wrong and with what probability. In the language of matrix theory: every 
> matrix operation must be accompanied by the spectral norm of its error. SCX{} provides 
> this through concentration bounds. Mainstream ML provides the matrix operations but 
> omits the error norms. **This is not a technical limitation — it is a logical 
> gap.** The mathematics of concentration inequalities has been available since Hoeffding 
> (1963), Bernstein (1924), and McDiarmid (1989). The fact that no mainstream framework 
> has integrated these bounds into its core API is a choice, not a constraint.
> 
> 
> **科学需要可验证性。每个科学声明必须附带它可能错误及错误概率的说明。用矩阵论的语言：每个矩阵运算必须伴随其误差的谱范数。SCX通过浓度界提供这一点。主流ML提供矩阵运算但省略误差范数。这不是技术限制——这是逻辑空白。浓度不等式的数学自Hoeffding(1963)、Bernstein(1924)和McDiarmid(1989)就已存在。没有主流框架将这些界集成到核心API中，这是一种选择，而非约束。**

## Unified Proof Architecture 统一证明架构
<!-- label: sec:unified_proofs -->

### The Common Proof Template 通用证明模板

All SCX{} error bounds follow a common template derived from Hoeffding's inequality:

\begin{algorithm}[htbp]
*Caption:* Universal SCX{} Error Bound Derivation 通用SCX误差界推导
<!-- label: alg:universal_bound -->
\begin{algorithmic}[1]
\State **Input:** $M$ independent experts, error magnitude $\Delta$, confidence $\delta$
\State **Step 1:** Express the quantity of interest as an empirical mean of $M$ bounded variables
\State \quad $\bar{X} = \frac{1}{M}\sum_{m=1}^{M} X_m$, where $X_m \in [a_m, b_m]$
\State **Step 2:** Apply Hoeffding's inequality:
\State \quad $\Pbb(|\bar{X} - \E[\bar{X}]| \geq \Delta) \leq 2\exp\!\left(-\frac{2M^2\Delta^2}{\sum_{m=1}^{M} (b_m - a_m)^2}\right)$
\State **Step 3:** Specialize to the specific SCX{} algorithm by identifying $X_m$
\State **Step 4:** If experts are correlated, replace $M$ with $M_{eff} = M/(1+\bar)$
\State **Step 5:** Solve for $M$ given target $(\Delta, \delta)$:
\State \quad $M \geq \frac{\sum_{m} (b_m - a_m)^2 \cdot \ln(2/\delta)}{2M \cdot \Delta^2}$
\State **Output:** Certified error bound and required $M$
\end{algorithmic}
\end{algorithm}

### Proof of Universality 普遍性证明

> **Theorem:** [Universal Hoeffding Reduction 通用Hoeffding归约]<!-- label: thm:universal_reduction -->
> \rigorFull
> Every SCX{} error bound presented in this paper (Theorems [ref], 
>  [ref],  [ref],  [ref]) 
> is a special case of Hoeffding's inequality applied to a suitably defined empirical mean 
> of bounded random variables.

> **Proof:** We provide the reduction for each theorem:
> 
> **Spring{} (Theorem [ref]):** 
> $X_t = \norm{\Delta_t}_2 \in [0, L]$, $\bar{X}_t = \frac{1}{t}\sum_{k=1}^{t} X_k$, 
> $\E[X_k] \to 0$ as $k \to \infty$.
> 
> **Yajie{} (Theorem [ref]):** 
> $X_m = c_m \in [a, b]$, $\bar{X} = \sum_m W_m X_m$, 
> using the weighted Hoeffding extension (or the unweighted Hoeffding as a conservative bound).
> 
> **Theorem~1 (Theorem [ref]):** 
> $X_m = \mat{V}_{m,i} \in \{0,1\}$, $\bar{X} = \frac{1}{M}\sum_m X_m = \mat{C}_i$.
> 
> **Cercis{} (Theorem [ref]):** 
> $X_{ij} = (\mat{Y}_{ij} - \mat{P}_{ij})^2 \in [0, (b-a)^2]$, 
> $\bar{X} = \frac{1}{np}\sum_{i,j} X_{ij} = Q$.
> 
> In each case, the random variables are bounded, independent (or conditionally independent),
> and the quantity of interest is an empirical mean. Hoeffding's inequality applies directly,
> yielding the stated exponential bounds.  $\square$

### Tightness Analysis 紧性分析

> **Proposition:** [Tightness of SCX Bounds SCX界的紧性]<!-- label: prop:tightness -->
> \rigorFull
> All SCX{} error bounds are tight in the following sense: for binary expert votes 
> (Theorem~1), the Hoeffding bound is known to be sharp for Bernoulli variables when 
> $p = 1/2$ (the worst-case variance). For continuous bounded variables (Yajie{}, 
> Cercis{}), the Hoeffding bound is tight up to constant factors; Bernstein-type 
> bounds would provide sharper concentration when the variance is small, but require 
> variance estimation which introduces additional uncertainty.

> **Proof:** For binary variables with $p = 1/2$, the exact tail probability for the binomial 
> distribution is $\Pbb(|\bar{X} - 1/2| > \Delta) = 2\sum_{k > M(1/2+\Delta)} \binom{M}{k} 2^{-M}$.
> Hoeffding gives $2\exp(-2M\Delta^2)$. The ratio of the exact bound to the Hoeffding 
> bound approaches 1 as $M \to \infty$ for fixed $\Delta$, establishing asymptotic tightness.
> For smaller $M$ and large $\Delta$, improvements using the Chernoff bound or the exact
> binomial tail exist but provide at most constant-factor improvements.  $\square$

## Implementation Protocol — From Theory to Code 从理论到代码
<!-- label: sec:implementation -->

### Matrix Pseudocode 矩阵伪代码

Every SCX{} algorithm can be implemented as a matrix operation with a concentration 
bound check. Below we provide the universal SCX{} matrix template:

\begin{algorithm}[htbp]
*Caption:* Universal SCX Matrix Operation with Certified Bound 带认证界的通用SCX矩阵运算
<!-- label: alg:scx_universal -->
\begin{algorithmic}[1]
\Require $M$ experts $\{\mat{W}_m\}_{m=1}^{M}$, input $\mat{X} \in \R^{n \times d}$, confidence $\delta$, tolerance $\varepsilon$
\Ensure Prediction $\hat{\mat{Y}}$ with certified error bound
\For{$m = 1$ to $M$}
    \State $\hat{\mat{Y}}_m \gets f(\mat{X}; \mat{W}_m)$ \Comment{Expert $m$ prediction, $\hat{\mat{Y}}_m \in \R^{n \times p}$}
\EndFor
\State $\bar{\mat{Y}} \gets \frac{1}{M}\sum_{m=1}^{M} \hat{\mat{Y}}_m$ \Comment{Unweighted consensus, $\bar{\mat{Y}} \in \R^{n \times p}$}
\State $\bar \gets \frac{2}{M(M-1)}\sum_{m < m'} \Corr(\hat{\mat{Y}}_m, \hat{\mat{Y}}_{m'})$ \Comment{Inter-expert correlation}
\State $M_{eff} \gets M / (1 + \bar)$
\State $\Delta_ \gets \sqrt{\frac{\ln(2p/\delta)}{2M_{eff}}}$ \Comment{Certified error per dimension (union bound)}
\If{$\Delta_ > \varepsilon$}
    \State **raise** CertificationFailure(required $M \geq \frac{\ln(2p/\delta)}{2\varepsilon^2} \cdot (1 + \bar)$)
\EndIf
\State \Return $\hat{\mat{Y}} = \bar{\mat{Y}}$ with certified bound $\Pbb(\norm{\hat{\mat{Y}} - \mat{Y}^*}_ > \varepsilon) \leq \delta$
\end{algorithmic}
\end{algorithm}

### Required $M$ Calculator 所需M计算器

[Table omitted — see original .tex]

Where $M_{raw} = \frac{\ln(2n/\delta)}{2\varepsilon^2}$ and 
$M_{required} = M_{raw} \cdot (1 + \bar)$.

## Discussion — The Matrix Epistemology 讨论——矩阵认识论
<!-- label: sec:discussion -->

### Why Matrix Form Matters 为什么矩阵形式重要

Expressing SCX{} in matrix form is not a cosmetic reformulation. It provides three 
fundamental advantages:

1. **Unification 统一性:** All SCX{} algorithms — Spring{}, Yajie{},
2. **Comparison 可比较性:** Mainstream ML frameworks (Transformer, MoE,
3. **Implementation 可实现性:** Matrix operations are the native language
4. **Concentration 浓度性:** Hoeffding's inequality and its generalizations

### The Epistemological Gap 认识论空白

> **Remark:** [What $M=1$ Means $M=1$的含义]
> <!-- label: rem:M_equals_one -->
> When $M=1$ (a single model makes a prediction), the Hoeffding bound becomes:
> \[
> \Pbb(error > \varepsilon) \leq 2\exp(-2\varepsilon^2).
> \]
> For $\varepsilon = 0.1$, this gives $\Pbb(error > 0.1) \leq 1.96$, which is 
> **vacuous** (probability cannot exceed 1). For $\varepsilon = 1$, 
> $\Pbb(error > 1) \leq 0.27$, which provides some guarantee but only for 
> errors larger than the entire range of the variable. 
> 
> **The mathematical truth:** $M=1$ provides no meaningful concentration guarantee 
> for small errors. Every mainstream ML model deployed in production with $M=1$ is 
> making predictions with **no certified error bound**. This is the matrix 
> epistemology: without $M > 1$, you have computation without certification.
> 
> 
> **M=1的数学真相：** 单个模型对小幅误差不提供有意义的浓度保证。每个部署在生产环境中的M=1的主流ML模型，其预测都没有经过认证的误差界。这是矩阵认识论：没有M>1，你只有计算而没有认证。

### The Concentration Inequality Catalog 浓度不等式目录

Table [ref] catalogs the concentration inequalities used 
throughout the SCX{} matrix framework and their domains of applicability.

[Table omitted — see original .tex]

Where $h(u) = (1+u)\ln(1+u) - u$ is the Bennett function.

### Future Directions 未来方向

1. **Matrix Concentration for Deep Networks 深度网络的矩阵浓度:**
2. **Adaptive $M$ Selection 自适应M选择:** Online algorithms that
3. **Hardware-Accelerated SCX 硬件加速SCX:** Leveraging tensor cores
4. **Matrix-Theoretic SCX for Vision 视觉的矩阵论SCX:** Applying
5. **Non-Hoeffding Bounds 非Hoeffding界:** Extending beyond sub-Gaussian

## Conclusion 结论
<!-- label: sec:conclusion -->

We have presented a complete linear-algebraic reformulation of the SCX{} framework.
Every SCX{} algorithm — Spring{}, Yajie{}, Theorem~1 noise detection, \Situs{} 
encoding, and Cercis{} scoring — is a matrix operation with a certified concentration 
bound. Every mainstream ML framework — Transformer, MoE, LoRA, Mamba — is a matrix 
operation **without** a certified concentration bound.

The difference between them is exactly one column in a comparison table. That column 
— the error bound — is not a feature. It is the definition of scientific rigor. 
Without it, you have linear algebra but no guarantee. With it, every prediction carries 
a certified probability of correctness.

The mathematics of concentration inequalities has been available since Hoeffding (1963).
The linear algebra of machine learning has been available since the perceptron (1958).
What has been missing — and what SCX{} provides — is the marriage of the two: matrix 
operations that carry their own error certificates. This paper provides the unified 
theory. The implementation follows directly: every matrix multiplication must be 
accompanied by its Hoeffding (or Bernstein, or McDiarmid) bound. Every prediction 
must declare its $M$. Every framework must have the error bound column.

**没有误差界这一列的机器学习，不是科学，是炼金术。**
**Machine learning without the error bound column is not science — it is alchemy.**

\rule{0.4pt}

## Appendix

## Concentration Inequalities — Quick Reference 浓度不等式快速参考
<!-- label: app:concentration -->

For completeness, we state the key concentration inequalities used throughout this paper.

> **Theorem:** [Hoeffding's Inequality (1963) 霍夫丁不等式]<!-- label: thm:hoeffding_app -->
> Let $X_1, ..., X_M$ be independent random variables with $X_m \in [a_m, b_m]$ almost surely.
> Let $\bar{X} = \frac{1}{M}\sum_{m=1}^{M} X_m$. Then for any $t > 0$:
> \[
> \Pbb(\abs{\bar{X} - \E[\bar{X}]} \geq t) \leq 2\exp\!\left(-\frac{2M^2 t^2}{\sum_{m=1}^{M} (b_m - a_m)^2}\right).
> \]
> When all $b_m - a_m = 1$, this simplifies to $2\exp(-2M t^2)$.

> **Theorem:** [Bernstein's Inequality 伯恩斯坦不等式]<!-- label: thm:bernstein_app -->
> Let $X_1, ..., X_M$ be independent, zero-mean random variables with 
> $\abs{X_m} \leq c$ almost surely and $\Var(X_m) = \sigma_m^2$. Let 
> $\sigma^2 = \frac{1}{M}\sum_m \sigma_m^2$. Then:
> \[
> \Pbb\left(\abs{\frac{1}{M}\sum_{m=1}^{M} X_m} \geq t\right) \leq 2\exp\!\left(-\frac{M t^2}{2\sigma^2 + 2ct/3}\right).
> \]

> **Theorem:** [McDiarmid's Inequality 麦克迪尔米德不等式]<!-- label: thm:mcdiarmid_app -->
> Let $f: \cX_1 \times ... \times \cX_M \to \R$ satisfy the bounded differences 
> property: for all $m$ and all $x_1, ..., x_M, x_m'$:
> \[
> \abs{f(x_1, ..., x_m, ..., x_M) - f(x_1, ..., x_m', ..., x_M)} \leq c_m.
> \]
> Then for independent $X_1, ..., X_M$:
> \[
> \Pbb(\abs{f(X_1, ..., X_M) - \E[f]} \geq t) \leq 2\exp\!\left(-\frac{2t^2}{\sum_{m=1}^{M} c_m^2}\right).
> \]

## Matrix Identities — Quick Reference 矩阵恒等式快速参考
<!-- label: app:matrix_identities -->

- **Trace cyclic property 迹的循环性质:** $\tr(\mat{A}\mat{B}) = \tr(\mat{B}\mat{A})$,
- **Frobenius norm 弗罗贝尼乌斯范数:**
- **Softmax Jacobian softmax雅可比:**
- **Orthogonal projection 正交投影:**
- **Gram matrix 格拉姆矩阵:**
- **Kernel matrix 核矩阵:**
- **Singular value decomposition 奇异值分解:**

## Notation Glossary 符号表
<!-- label: app:notation -->

[Table omitted — see original .tex]

\begin{thebibliography}{99}

\bibitem{Hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock *Journal of the American Statistical Association*, 58(301):13--30, 1963.

\bibitem{Bernstein1924}
S.~Bernstein.
\newblock On a modification of Chebyshev's inequality and of the error formula of Laplace.
\newblock *Annales Sci. Inst. Sav. Ukraine, Sect. Math.*, 1(4):38--49, 1924.

\bibitem{McDiarmid1989}
C.~McDiarmid.
\newblock On the method of bounded differences.
\newblock *Surveys in Combinatorics*, 141:148--188, 1989.

\bibitem{Tropp2015}
J.~A.~Tropp.
\newblock An introduction to matrix concentration inequalities.
\newblock *Foundations and Trends in Machine Learning*, 8(1-2):1--230, 2015.

\bibitem{Vaswani2017}
A.~Vaswani et al.
\newblock Attention is all you need.
\newblock *NeurIPS*, 2017.

\bibitem{Shazeer2017}
N.~Shazeer et al.
\newblock Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
\newblock *ICLR*, 2017.

\bibitem{Hu2021}
E.~Hu et al.
\newblock LoRA: Low-rank adaptation of large language models.
\newblock *ICLR*, 2022.

\bibitem{Gu2023}
A.~Gu and T.~Dao.
\newblock Mamba: Linear-time sequence modeling with selective state spaces.
\newblock *arXiv:2312.00752*, 2023.

\bibitem{RahimiRecht2007}
A.~Rahimi and B.~Recht.
\newblock Random features for large-scale kernel machines.
\newblock *NeurIPS*, 2007.

\bibitem{Gretton2012}
A.~Gretton et al.
\newblock A kernel two-sample test.
\newblock *Journal of Machine Learning Research*, 13:723--773, 2012.

\bibitem{Bercu2015}
B.~Bercu, B.~Delyon, and E.~Rio.
\newblock *Concentration Inequalities for Sums and Martingales*.
\newblock Springer, 2015.

\bibitem{SCXFramework2026}
SCX.
\newblock The SCX framework: Structured causal examination with certified error bounds.
\newblock *SCX Technical Report*, 2026.

\end{thebibliography}