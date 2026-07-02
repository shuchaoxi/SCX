## Original Claim (Incorrect) / 原始观点 (有误)

> **Original Viewpoint 1:**
> Experts live in their own coordinate systems — this is not a bug but gauge freedom.

> Each expert output carries an unobservable offset $g_m$.

> Training loss does not sense it — the residual connection absorbs it.

> Routers / auditors / comparators do not know about it.

> They compare things that are incomparable.
> 
> 
> **原始观点1:**
> 专家活在各自坐标系里——不是bug是规范自由度。

> 每个专家输出带不可观测偏移$g_m$。

> 训练损失不感知——残差连接吸收。

> 路由器/审计者/比较者不知道。

> 在比较不可比的东西。

## Verdict / 判决

<div align="center">

\fbox{\parbox{0.9\textwidth}{

**Verdict: LARGELY INCORRECT / 大部分错误**

The core intuition (parameter redundancy exists) has merit.

But every specific mechanism claim is wrong or requires heavy qualification.

LayerNorm eliminates constant offsets — **not** vector offsets.

Routers **can** detect gauge offsets.

Training loss **does** sense gauge offsets directly.
}}

</div>

## Corrected Viewpoint 1 / 修正后的观点1

> \fcolorbox{blue!30}{blue!5}{\parbox{0.95\textwidth}{
> **Corrected Viewpoint 1:**
> Experts in a Mixture of Experts (MoE) operate in different coordinate systems:
> each expert $m$ can carry an additive offset $\gauge_m \in \R^d$ in its output.
> This offset is a **gauge degree of freedom** — a parameter redundancy rather
> than a true observable.
> **However**, the claim that these offsets are invisible to the training
> process, routers, and auditors is **incorrect**.
> 
> 1. **LayerNorm:** In Pre-LN Transformers, LayerNorm eliminates the
> 2. **Training loss:** The loss function directly senses $\gauge_m$.
> 3. **Routers:** In Top-1 routing, $\gauge_m$ is **exactly
> 4. **Auditors:** Given sufficient samples where expert $m$ is
> 
> 
> 
> **The real problem:** It is not that gauge offsets are invisible. It is
> that existing architectures do not *explicitly* model the gauge degrees
> of freedom. Compensation happens **implicitly** — via SGD absorbing offsets
> into bias terms, and LayerNorm partially suppressing them. This implicit
> compensation degrades routing quality, pollutes inter-layer communication,
> and makes expert outputs incomparable without proper gauge fixing.
> 
> 
> \rule{0.5pt}
> 
> 
> **修正后的观点1:**
> 专家在MoE中运行于不同的坐标系：每个专家$m$可以在其输出中携带加性偏移$\gauge_m \in \R^d$。
> 这个偏移是一个**规范自由度**——即参数冗余，而非真正的可观测量。
> **然而**，声称这些偏移对训练过程、路由器和审计者不可见是**错误的**。
> 
> 1. **LayerNorm:** 在Pre-LN Transformer中，LayerNorm通过均值减法消除$\gauge_m$
> 2. **训练损失:** 损失函数直接感知$\gauge_m$。
> 3. **路由器:** 在Top-1路由中，$\gauge_m$可从观测输出中**精确恢复**
> 4. **审计者:** 给定专家$m$被激活的足够样本，审计者可通过普通最小二乘回归
> 
> 
> 
> **真正的问题是:** 并非规范偏移不可见，而是现有架构没有*显式地*建模规范自由度。
> 补偿以*隐式*方式发生——SGD将偏移吸收到偏置项中，LayerNorm部分抑制它们。
> 这种隐式补偿降低了路由质量，污染了层间通信，使专家输出在缺乏适当规范固定的情况下不可比较。
> **}

## Precise Analysis: What LayerNorm Does and Does Not Do
## 精确分析: LayerNorm 做了什么、没做什么

### Mathematics of LayerNorm Gauge Absorption
### LayerNorm 规范吸收的数学

Consider a Pre-LN Transformer block where the output of layer $l$ passes
through LayerNorm before entering layer $l+1$:

$$
    y^{(l)} = x^{(l)} + FFN^{(l)}\bigl(LN(x^{(l)})\bigr)
$$

If expert $m$ adds a gauge offset $\gauge_m$ to its output:

$$
    y^{(l)} = x^{(l)} + FFN^{(l)}\bigl(LN(x^{(l)})\bigr) + \gauge_m
$$

The next layer's input is $LN(y^{(l)})$. For a vector $z \in \R^d$:

$$
    LN(z)_i = \frac{z_i - \mu(z)}{\sigma(z)} \cdot \gamma_i + \beta_i,
    \quad \mu(z) = \frac{1}{d}\sum_{j=1}^d z_j
$$

Now consider two cases:

**Case 1: Constant offset** $\gauge_m = c \cdot \mathbf{1}$ (all dimensions
shifted by the same scalar $c$).

$$
    \mu(y + c\mathbf{1}) &= \mu(y) + c 

    y_i + c - \mu(y + c\mathbf{1}) &= y_i + c - (\mu(y) + c) = y_i - \mu(y) 

    \sigma(y + c\mathbf{1}) &= \sigma(y)
$$

Therefore $LN(y + c\mathbf{1}) = LN(y)$. The constant offset is
**completely eliminated**.

**Case 2: Vector offset** $\gauge_m$ where $\gauge_{m,i}$ varies
across dimensions.

$$
    \mu(y + \gauge_m) &= \mu(y) + \overline{\gauge_m} 

    (y_i + \gauge_{m,i}) - \mu(y + \gauge_m) &= (y_i - \mu(y)) + (\gauge_{m,i} - \overline{\gauge_m}) 

    \sigma(y + \gauge_m) &\neq \sigma(y) \quad (in general)
$$

**Only the mean component** $\overline{\gauge_m}$ is subtracted.
The **differential component** $\gauge_{m,i} - \overline{\gauge_m}$
survives LayerNorm and leaks to the next layer.

\rule{0.5pt}

**情况1: 常数偏移** $\gauge_m = c \cdot \mathbf{1}$（所有维度加相同标量$c$）。

$$
    \mu(y + c\mathbf{1}) &= \mu(y) + c 

    y_i + c - \mu(y + c\mathbf{1}) &= y_i + c - (\mu(y) + c) = y_i - \mu(y) 

    \sigma(y + c\mathbf{1}) &= \sigma(y)
$$

因此$LN(y + c\mathbf{1}) = LN(y)$。常数偏移被**完全消除**。

**情况2: 向量偏移** $\gauge_m$，其中$\gauge_{m,i}$各维度值不同。

$$
    \mu(y + \gauge_m) &= \mu(y) + \overline{\gauge_m} 

    (y_i + \gauge_{m,i}) - \mu(y + \gauge_m) &= (y_i - \mu(y)) + (\gauge_{m,i} - \overline{\gauge_m}) 

    \sigma(y + \gauge_m) &\neq \sigma(y) \quad (一般情况)
$$

**仅均值分量**$\overline{\gauge_m}$被消除。
**差分分量**$\gauge_{m,i} - \overline{\gauge_m}$穿透LayerNorm泄漏到下一层。

### Empirical Evidence / 实验证据

[Table omitted — see original .tex]

[Table omitted — see original .tex]

## Why Routers CAN Detect Gauge / 路由器为何能检测规范

### Top-1 Routing: Direct Observation
### Top-1 路由: 直接观测

In Top-1 routing, exactly one expert is active per token. The MoE output is:

$$
    y = FFN_{m^*}(x) + \gauge_{m^*}
$$

The gauge offset $\gauge_{m^*}$ appears **directly** in the output.
A downstream observer (or Layer $l+1$ router) sees $y$, which contains
$\gauge_{m^*}$ as an additive term. If the observer also knows $FFN_{m^*}(x)$
(or can approximate it), $\gauge_{m^*}$ is trivially recoverable by subtraction.

\rule{0.5pt}
在Top-1路由中，每个token恰好激活一个专家。MoE输出为:

$$
    y = FFN_{m^*}(x) + \gauge_{m^*}
$$

规范偏移$\gauge_{m^*}$**直接**出现在输出中。下游观察者（或第$l+1$层路由器）
看到$y$，其中包含$\gauge_{m^*}$作为加性项。若观察者也知晓$FFN_{m^*}(x)$
（或可近似之），则$\gauge_{m^*}$可通过减法平凡地恢复。

### Multi-Layer Contamination / 多层污染

In a multi-layer MoE, the Layer $l$ output feeds into Layer $l+1$'s router:

$$
    r^{(l+1)} = Router^{(l+1)}\bigl(y^{(l)}\bigr)
              = Router^{(l+1)}\bigl(x^{(l)} + FFN^{(l)}(\cdot) + \gauge_m\bigr)
$$

The router computes $\alpha^{(l+1)}(x) = softmax(r^{(l+1)})$.
Since $\gauge_m$ shifts $r^{(l+1)}$, the softmax weights change:

$$
    \alpha^{(l+1)}_k = \frac{\exp(r^{(l+1)}_k + \Delta_k)}{\sum_j \exp(r^{(l+1)}_j + \Delta_j)},
    \quad \Delta = W_{router} \cdot \gauge_m
$$

**Consequence:** $\gauge_m$ from layer $l$ changes the routing decisions
in layer $l+1$. This is direct evidence that routers **do** sense gauge offsets.

\rule{0.5pt}
在多层MoE中，第$l$层输出馈入第$l+1$层路由器:

$$
    r^{(l+1)} = Router^{(l+1)}\bigl(y^{(l)}\bigr)
              = Router^{(l+1)}\bigl(x^{(l)} + FFN^{(l)}(\cdot) + \gauge_m\bigr)
$$

路由器计算$\alpha^{(l+1)}(x) = softmax(r^{(l+1)})$。
由于$\gauge_m$偏移了$r^{(l+1)}$，softmax权重发生变化:

$$
    \alpha^{(l+1)}_k = \frac{\exp(r^{(l+1)}_k + \Delta_k)}{\sum_j \exp(r^{(l+1)}_j + \Delta_j)},
    \quad \Delta = W_{router} \cdot \gauge_m
$$

**结论:** 第$l$层的$\gauge_m$改变了第$l+1$层的路由决策。
这是路由器**确实**感知规范偏移的直接证据。

## How the Training Process Senses Gauge / 训练过程如何感知规范

The claim ``training loss does not sense $\gauge_m$'' conflates two distinct
phenomena:

1. **Instantaneous loss:** $\mathcal{L}(y + \gauge_m, t) \neq \mathcal{L}(y, t)$
2. **Post-convergence equivalence:** If the expert has a learnable

\rule{0.5pt}

声称``训练损失不感知$\gauge_m$''混淆了两个不同的现象:

1. **瞬时损失:** 对任意固定$\gauge_m \neq 0$，
2. **收敛后等效:** 若专家有可学习偏置$b$，则训练后的有效偏置为$b + \gauge_m$。

## Comparison with SCX Gauge Theory / 与SCX规范理论的对比

[Table omitted — see original .tex]

The MoE situation is **not** a true gauge symmetry in the physical sense.
It is a **parameter redundancy** that the optimization process resolves
implicitly. Unlike SCX where $\sum g_e = 0$ is an active human convention,
MoE ``gauge fixing'' is a passive byproduct of gradient descent and
normalization layers.

\rule{0.5pt}
MoE的情况**不是**物理意义上的真正规范对称性。它是一种**参数冗余**，
优化过程隐式地解决它。与SCX中$\sum g_e = 0$是主动人为约定不同，
MoE的``规范固定''是梯度下降和归一化层的被动副产品。

## Required Qualifications for Any ``Gauge Freedom'' Claim
## 任何"规范自由度"声称所需的限定条件

For the claim ``experts operate in different coordinate systems due to gauge
freedom'' to be accurately stated, the following qualifications are necessary:

对于``专家因规范自由度运行于不同坐标系''的声称要准确表述，需要以下限定:

1. **Learnable parameter condition / 可学习参数条件:**
2. **Offset type condition / 偏移类型条件:**
3. **Convergence condition / 收敛条件:**
4. **Single-layer condition / 单层条件:**
5. **Information-limiting condition / 信息限制条件:**

## Summary: The Correct Picture / 总结: 正确的图景

<div align="center">

\fcolorbox{green!40}{green!5}{\parbox{0.92\textwidth}{
**The Correct Claim / 正确的声称:**
Experts in MoE carry additive offsets $\gauge_m$ that constitute a form of
parameter redundancy. In Pre-LN Transformers, LayerNorm eliminates the
*constant* (per-token mean) component of these offsets, but
*vector* components (dimension-specific differences) leak through
the residual stream. Training senses these offsets directly and compensates
via bias terms — this is active sensing, not ignorance. Routers in multi-layer
MoE are directly affected: gauge offsets from one layer contaminate the input
distribution of the next, causing routing decisions to flip. Auditors with
sufficient samples can statistically recover the offsets with near-perfect
accuracy.
**The real problem is not invisibility — it is that existing architectures
do not explicitly model the gauge degrees of freedom.** Implicit compensation
degrades routing quality and makes cross-expert comparisons unreliable.
Proper gauge fixing (explicitly constraining offsets, as in SCX's
$\sum g_e = 0$ convention) would make expert outputs comparable and improve
routing stability.

\rule{0.5pt}

MoE中的专家携带加性偏移$\gauge_m$，构成一种参数冗余。在Pre-LN Transformer中，
LayerNorm消除这些偏移的*常数*（逐token均值）分量，但*向量*分量
（各维度不同的差值）通过残差流泄漏。训练直接感知这些偏移并通过偏置项进行补偿——
这是主动感知，而非无知。多层MoE中的路由器直接受影响：一层的规范偏移污染下一层的
输入分布，导致路由决策翻转。拥有足够样本的审计者可以统计性地恢复偏移，
精度接近机器精度。
**真正的问题不是不可见性——而是现有架构没有显式地建模规范自由度。**
隐式补偿降低了路由质量，使跨专家比较不可靠。
适当的规范固定（显式约束偏移，如SCX的$\sum g_e = 0$约定）将使专家输出可比较，
并提高路由稳定性。
}}

</div>

## Code Evidence / 代码证据

All experimental claims are validated by `analysis\_viewpoint1.py`
(pure NumPy, no deep learning framework dependency). Key results:

所有实验声称由`analysis\_viewpoint1.py`验证（纯NumPy，无深度学习框架依赖）。关键结果:

- **PART 2:** Top-1 routing enables exact $g_m$ recovery (error $<10^{-15}$)
- **PART 3:** Constant offset eliminated by LN (residual $10^{-16}$);
- **PART 4:** Direct loss sensing: $\Delta\mathcal{L} = 7.79$
- **PART 5:** SGD absorbs $g$ into learnable bias (post-training difference norm 0.153)
- **PART 6:** Multi-layer contamination: 5/8 tokens flip top-1 routing
- **PART 7:** Statistical $g_m$ separation via OLS: error $<10^{-14}$