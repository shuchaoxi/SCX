#!/usr/bin/env python3
"""
Complete cleanup: mechanical fixes + Chinese to English translation
for scx_moe_gauge/main.md
"""
import re, json, os

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    text = f.read()

# ============== STEP 1: MECHANICAL CLEANUPS ==============

# Fix remaining LaTeX artifacts
text = text.replace(r'\begin{assumption_env}', '')
text = text.replace(r'\end{assumption_env}', '')
text = text.replace(r'\begin{algorithm}[H]', '')
text = text.replace(r'\end{algorithm}', '')
text = text.replace(r'\begin{algorithmic}[1]', '')
text = text.replace(r'\end{algorithmic}', '')
text = text.replace(r'\begin{keyeq}', '')
text = text.replace(r'\end{keyeq}', '')
text = text.replace(r'\begin{flushright}', '')
text = text.replace(r'\end{flushright}', '')
text = text.replace(r'\begin{compactenum}', '')
text = text.replace(r'\end{compactenum}', '')
text = text.replace(r'\begin{thebibliography}', '')
text = text.replace(r'\end{thebibliography}', '')
text = text.replace(r'\rigorFull', '')
text = re.sub(r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}', '', text)
text = re.sub(r'\\newcommand\{[^}]*\}\{[^}]*\}', '', text)
text = re.sub(r'\\resizebox\{[^}]*\}\{[^}]*\}\{', '', text)
text = re.sub(r'\\rule\{[^}]*\}\{[^}]*\}', '', text)
text = re.sub(r'\\Caption\{([^}]*)\}', r'**\1**', text)

# Fix \sim_g (was \sim_)
text = text.replace(r'\sim_', r'\sim_g')

# Fix \bar where it should be \bar{y}
text = text.replace(r'\bar =', r'\bar{y} =')
text = text.replace(r'(\gamma_m \circ E_m - \bar)', r'(\gamma_m \circ E_m - \bar{y})')

# Fix \mathcal{D}elta
text = text.replace(r'\mathcal{D}elta', r'\Delta')

# Fix g_ to g_*
text = re.sub(r'g_([^a-zA-Z])', r'g_*\1', text)
text = text.replace(r'g_*^{(\ell)}', r'g_*^{(\ell)}')  # already correct

# Fix stray \fbox and minipage
text = re.sub(r'\\fbox\s*[{%]?', '', text)
text = re.sub(r'\\begin\{minipage\}\{[^}]*\}', '', text)
text = text.replace(r'\end{minipage}', '')
text = re.sub(r'^\s*\}\s*$', '', text, flags=re.MULTILINE)

# Fix \textbf and \textit
text = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', text)
text = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', text)

# Fix math: \E[ -> \mathbb{E}[  (some may have been missed)
text = re.sub(r'(?<!\w)\\[A-Z](?=[^a-zA-Z])', lambda m: {
    '\\R': '\\mathbb{R}', '\\N': '\\mathbb{N}', '\\E': '\\mathbb{E}',
    '\\D': '\\mathcal{D}', '\\G': '\\mathcal{G}', '\\X': '\\mathcal{X}',
    '\\F': '\\mathcal{F}', '\\T': '\\mathcal{T}', '\\A': '\\mathcal{A}',
}.get(m.group(0), m.group(0)), text)

# Remove ghost braces from fbox removal
text = text.replace('\\fbox', '')
text = re.sub(r'^\{\s*$', '', text, flags=re.MULTILINE)

# Clean up HTML comments
text = re.sub(r'<!--\s*label:\s*([^>]+)\s*-->', r'<!-- \1 -->', text)

# ============== STEP 2: CHINESE TO ENGLISH TRANSLATIONS ==============

# Comprehensive translation map -- ordered by first occurrence in the file
translations = [
    # HEADER
    ("**版本：** v1.0 \\quad | \\quad\n**状态：** 预印本 \\quad | \\quad\n**分类：** SCX理论体系 — 信息论卷·多专家规范篇",
     "**Version:** v1.0 \\quad | \\quad\n**Status:** Preprint \\quad | \\quad\n**Category:** SCX Theory System -- Information Theory Volume: Multi-Expert Gauge Chapter"),

    # CORE INTUITION section
    ("## 核心直觉：一页读懂势能面不齐", "## Core Intuition: Understanding Potential Surface Misalignment in One Page"),

    ("### 尺子比喻 (The Ruler Metaphor)", "### The Ruler Metaphor"),
    ("想象你请了 8 个工程师每人造一把尺子，然后你把这些尺子拼成一根长尺。",
     "Imagine you ask 8 engineers to each build a ruler, and then you piece these rulers together into one long ruler."),
    ("每个工程师造的尺子上**刻度是准的**——1厘米就是1厘米——但每个人把**零刻度放在了不同的位置**。张三的零刻度在尺子最左端。李四的零刻度在尺子中间。王五的零刻度偏右了2毫米。",
     "Each engineer's ruler has **accurate markings** -- 1 cm is 1 cm -- but each person placed **the zero mark at a different position**. Zhang San's zero is at the far left. Li Si's zero is in the middle. Wang Wu's zero is shifted 2 mm to the right."),
    ("把 8 把尺子直接拼起来：刻度线对不齐，接缝处出现跳变。但每把尺子单独用来量东西，都是准的——因为量的是**相对长度**，不是绝对位置。",
     "Put the 8 rulers together directly: the markings do not align, and there is a jump at the seam. But each ruler is accurate when used alone to measure something -- because what is measured is **relative length**, not absolute position."),
    ("**这，就是势能面不齐。**", "**This is potential surface misalignment.**"),
    ("- **尺子 = MoE 专家网络** $E_m$。每个专家单独训练，在自己的领域里是\"准的\"（loss 低）",
     "- **Ruler = MoE expert network** $E_m$. Each expert is trained independently and is \"accurate\" in its own domain (low loss)."),
    ("- **零刻度位置 = 规范自由度** $\\mathbf{g}_m$。训练损失对零刻度位置不敏感——因为残差连接 + LayerNorm 会自动吸收偏移",
     "- **Zero mark position = gauge freedom** $\\mathbf{g}_m$. The training loss is insensitive to the zero mark position -- because residual connections + LayerNorm automatically absorb the offset."),
    ("- **拼尺子 = 路由器比较专家**。路由器用一个线性函数比较 8 个专家的\"刻度\"，但它不知道每个专家的零刻度在哪",
     "- **Piecing rulers = router comparing experts**. The router uses a linear function to compare the \"markings\" of 8 experts, but it does not know where each expert's zero mark is."),
    ("- **接缝跳变 = 路由偏差**。选错了专家，或者给了不该给的权重",
     "- **Seam jump = routing bias**. The wrong expert is selected, or an inappropriate weight is assigned."),
    ("**解决方法也很简单：** 先让所有尺子对齐零刻度（规范固定），再拼（路由）。或者——更聪明地——不拼尺子，而是让每把尺子量完之后只报告**最终结果**（蒸馏 + Yajie），因为最终结果不依赖零刻度位置（规范不变）。",
     "**The solution is also simple:** First align all rulers to zero (gauge fixing), then assemble (route). Or -- more cleverly -- instead of piecing rulers together, let each ruler report only the **final result** after measurement (distillation + Yajie), because the final result does not depend on the zero mark position (gauge invariance)."),

    # THREE SENTENCE SUMMARY
    ("### 三句话总结本文", "### Three-Sentence Summary"),
    ("1. **发现问题：** MoE 的不同专家活在各自的\"坐标系\"里。路由器在比较不可比的东西。这不是工程疏忽——这是数学结构：规范自由度。",
     "1. **Problem identification:** Different MoE experts live in their own \"coordinate systems.\" The router is comparing incomparable things. This is not an engineering oversight -- it is a mathematical structure: gauge freedom."),
    ("2. **解决问题：** 三种方法。(a) 修路由器——零训练，校准集上算个偏置就行。(b) 蒸馏+Yajie——绕开规范问题，在输出空间做共识降噪。(c) 先对齐再蒸馏——最优雅，信息量最大。",
     "2. **Solution:** Three methods. (a) Repair the router -- zero training, just compute a bias on a calibration set. (b) Distillation + Yajie -- bypass the gauge problem, perform consensus denoising in output space. (c) Align first then distill -- most elegant, highest information content."),
    ("3. **意外收获：** 规范对齐后的 SVD 谱能检测 Yajie 漏掉的\"共享幻觉\"——所有专家一致同意的错误。真知识在表示空间里是低维的，共享幻觉是高维的。SVD 看得见这个区别。",
     "3. **Unexpected finding:** The SVD spectrum after gauge alignment can detect \"shared hallucinations\" missed by Yajie -- errors that all experts agree on. True knowledge is low-dimensional in representation space; shared hallucinations are high-dimensional. SVD can see this difference."),

    # INTRODUCTION
    ("## 引言：从ACE规范到MoE规范", "## Introduction: From ACE Gauge to MoE Gauge"),
    ("在先前的工作中~[EGP论文, SCX体系文献]，我们识别并解决了原子团簇展开(ACE)势函数合并中的一个核心问题：**系数级规范自由度**(coefficient-level gauge freedom)。具体而言，shared-correction ACE参数化",
     "In prior work [EGP paper, SCX system literature], we identified and solved a core problem in merging atomic cluster expansion (ACE) potentials: **coefficient-level gauge freedom**. Specifically, the shared-correction ACE parameterization"),
    ("在变换", "under the transformation"),
    ("下保持所有物理预测不变，但不同的独立训练会利用这一自由度走向不同的参数点。我们通过**后处理正交投影**解决了这一问题，将规范违反降至机器精度($<10^{-15}$)。",
     "leaves all physical predictions invariant, but different independent training runs exploit this freedom to reach different parameter points. We solved this via **post-hoc orthogonal projection**, reducing gauge violation to machine precision ($<10^{-15}$)."),
    ("> **诚实暴击:** 但那只是特例。规范自由度远不限于ACE参数空间——它在所有模块化多组件系统中普遍存在。MoE是下一个靶子。}",
     "> **Honest Strike:** But that was only a special case. Gauge freedom is far from limited to ACE parameter space -- it is universal in all modular multi-component systems. MoE is the next target."),

    # PSM subsection
    ("### 势能面不齐：问题的直观表述", "### Potential Surface Misalignment: An Intuitive Statement of the Problem"),
    ("考虑一个标准的稀疏MoE层。设 $N$ 个专家 $\\{E_m\\}_{m=1}^{N}$，每个专家是一个前馈网络 $E_m: \\mathbb{R}^d \\to \\mathbb{R}^d$。路由器给出分数 $g(x) = \\text{softmax}(W_r x) \\in \\mathbb{R}^N$，选取 $\\text{top-}k(g(x), k)$ 激活的专家。",
     "Consider a standard sparse MoE layer. Let there be $N$ experts $\\{E_m\\}_{m=1}^{N}$, each a feedforward network $E_m: \\mathbb{R}^d \\to \\mathbb{R}^d$. The router produces scores $g(x) = \\text{softmax}(W_r x) \\in \\mathbb{R}^N$, selecting the $\\text{top-}k(g(x), k)$ activated experts."),
    ("**核心直觉**：专家 $E_1$ 和专家 $E_2$ 在训练中各自学会了不同的输出\"基准\"——$E_1$ 的输出天然偏\"高\"，$E_2$ 的输出天然偏\"低\"，即使对相似的输入也是如此。这个差异在各自训练时被残差连接的后续层自适应地吸收掉了，因此不被训练损失所感知。但是——",
     "**Core intuition:** Experts $E_1$ and $E_2$ each learn different output \"baselines\" during training -- $E_1$'s output is naturally \"higher,\" $E_2$'s output is naturally \"lower,\" even for similar inputs. This difference is adaptively absorbed by subsequent residual connection layers during training and is thus not perceived by the training loss. However --"),
    ("**路由器不知道这件事。** 路由器 $W_r x$ 是一个线性映射，它比较的是原始专家输出的某种隐式代理。当 $E_1$ 和 $E_2$ 活在不同的坐标系中时，路由器的比较在数学上是**定义不清的**。",
     "**The router does not know this.** The router $W_r x$ is a linear map; it compares some implicit proxy of the raw expert outputs. When $E_1$ and $E_2$ live in different coordinate systems, the router's comparison is **ill-defined** mathematically."),
    ("我们称这种现象为**势能面不齐**(Potential Surface Misalignment, PSM)：每个专家定义了一个函数曲面",
     "We call this phenomenon **Potential Surface Misalignment (PSM)**: each expert defines a function surface"),
    ("这些曲面在输出空间的高度、尺度、甚至方向上天然不同——不是因为任何专家\"错了\"，而是因为训练动力学允许一个规范自由度。",
     "These surfaces naturally differ in height, scale, and even direction in output space -- not because any expert is \"wrong,\" but because the training dynamics permit a gauge freedom."),

    # GAUGE GROUP IDENTIFICATION
    ("### 规范群的识别", "### Identification of the Gauge Group"),
    ("我们识别出MoE表示空间中存在以下规范自由度：", "We identify the following gauge freedoms in MoE representation space:"),
    ("> **Definition:** [MoE表示空间的规范群]<!-- def:gauge_group  -->", "> **Definition:** [Gauge Group of MoE Representation Space]<!-- def:gauge_group -->"),
    ("> 设专家 $E_m$ 的输出空间为 $\\mathbb{R}^d$。专家$m$的**局部规范群** $\\mathcal{G}_m$ 是一个变换集合，满足：对任意 $\\gamma \\in \\mathcal{G}_m$，存在残差连接的下游自适应 $\\delta_\\gamma$ 使得",
     "> Let the output space of expert $E_m$ be $\\mathbb{R}^d$. The **local gauge group** $\\mathcal{G}_m$ of expert $m$ is a set of transformations such that: for any $\\gamma \\in \\mathcal{G}_m$, there exists a downstream adaptation $\\delta_\\gamma$ of the residual connection such that"),
    ("> 在训练损失下不可区分。具体而言：", "> is indistinguishable under the training loss. Specifically:"),
    ("1. **平移规范** $\\mathcal{G}_m^{trans} = \\{T_{\\mathbf{b}} : \\mathbf{y} \\mapsto \\mathbf{y} + \\mathbf{b}, \\mathbf{b} \\in \\mathbb{R}^d\\}$",
     "1. **Translation gauge** $\\mathcal{G}_m^{trans} = \\{T_{\\mathbf{b}} : \\mathbf{y} \\mapsto \\mathbf{y} + \\mathbf{b}, \\mathbf{b} \\in \\mathbb{R}^d\\}$"),
    ("2. **缩放规范** $\\mathcal{G}_m^{scale} = \\{S_ : \\mathbf{y} \\mapsto \\alpha \\mathbf{y}, \\alpha > 0\\}$",
     "2. **Scale gauge** $\\mathcal{G}_m^{scale} = \\{S_\\alpha : \\mathbf{y} \\mapsto \\alpha \\mathbf{y}, \\alpha > 0\\}$"),
    ("3. **旋转规范** $\\mathcal{G}_m^{rot} = \\{R_{\\mathbf{Q}} : \\mathbf{y} \\mapsto \\mathbf{Q}\\mathbf{y}, \\mathbf{Q} \\in O(d)\\}$",
     "3. **Rotation gauge** $\\mathcal{G}_m^{rot} = \\{R_{\\mathbf{Q}} : \\mathbf{y} \\mapsto \\mathbf{Q}\\mathbf{y}, \\mathbf{Q} \\in O(d)\\}$"),
    ("> 全规范群为这些子群的半直积：$\\mathcal{G} = \\mathcal{G}^{trans} \\rtimes (\\mathcal{G}^{scale} \\times \\mathcal{G}^{rot})$。",
     "> The full gauge group is the semidirect product of these subgroups: $\\mathcal{G} = \\mathcal{G}^{trans} \\rtimes (\\mathcal{G}^{scale} \\times \\mathcal{G}^{rot})$."),
    ("> **诚实暴击:** 平移规范是主要的——Post-LN或Pre-LN的LayerNorm会吸收平移。旋转规范次之——下游投影矩阵可以学习去旋转。缩放规范最微妙——它部分被LayerNorm掩盖，但在残差求和前仍然存在。}",
     "> **Honest Strike:** Translation gauge is the dominant one -- Post-LN or Pre-LN LayerNorm absorbs translations. Rotation gauge is secondary -- downstream projection matrices can learn to de-rotate. Scale gauge is the most subtle -- it is partially masked by LayerNorm but still exists before residual summation."),

    # CONTRIBUTIONS
    ("### 本工作的贡献", "### Contributions of This Work"),
    ("1. **识别MoE路由的规范不变量缺乏。** 我们证明标准路由器 $\\text{softmax}(W_r x)$ 在 $\\mathcal{G}$ 下不是不变的——路由分数随规范变换而改变，使得不同规范下的专家输出不可比较。",
     "1. **Identifying the lack of gauge invariance in MoE routing.** We prove that the standard router $\\text{softmax}(W_r x)$ is not invariant under $\\mathcal{G}$ -- routing scores change under gauge transformations, making expert outputs in different gauges incomparable."),
    ("2. **MILP规范固定公式化。** 我们将最优规范固定表述为混合整数线性规划(MILP)：整数变量编码路由决策，连续变量编码规范参数。我们给出了该MILP的紧致松弛和多项式时间近似。",
     "2. **MILP gauge fixing formulation.** We formulate optimal gauge fixing as a Mixed Integer Linear Program (MILP): integer variables encode routing decisions, continuous variables encode gauge parameters. We provide a tight relaxation and polynomial-time approximation for this MILP."),
    ("3. **规范对齐的SVD幻觉检测。** 我们证明：固定规范后，多专家对同一查询的输出矩阵的SVD谱的集中度是一个可证明的幻觉检测指标——谱平坦意味着模型内部没有共识。",
     "3. **Gauge-aligned SVD hallucination detection.** We prove that after gauge fixing, the concentration of the SVD spectrum of the multi-expert output matrix for the same query is a provable hallucination detection metric -- spectral flatness indicates no internal consensus in the model."),
    ("4. **连接ACE规范与MoE规范。** 我们展示两者是同一深层原理的实例：任何独立训练的模块化组件在交互前都需要显式的规范对齐。",
     "4. **Connecting ACE gauge and MoE gauge.** We show that both are instances of the same deep principle: any independently trained modular component requires explicit gauge alignment before interaction."),

    # PROBLEM SETUP
    ("## 问题设定：MoE的形式化", "## Problem Setup: Formalization of MoE"),
    ("> **Definition:** [稀疏MoE层]<!-- def:moe  -->", "> **Definition:** [Sparse MoE Layer]<!-- def:moe -->"),
    ("> 一个稀疏MoE层由以下组件构成：", "> A sparse MoE layer consists of the following components:"),
    ("- $N$ 个专家函数 $E_m: \\mathbb{R}^d \\to \\mathbb{R}^d$，$m = 1, ..., N$，每个专家是一个前馈网络",
     "- $N$ expert functions $E_m: \\mathbb{R}^d \\to \\mathbb{R}^d$, $m = 1, ..., N$, each a feedforward network"),
    ("- 路由器 $r: \\mathbb{R}^d \\to \\mathcal{D}elta^{N-1}$，$r(x) = \\text{softmax}(W_r x)$，其中 $W_r \\in \\mathbb{R}^{N \\times d}$",
     "- A router $r: \\mathbb{R}^d \\to \\Delta^{N-1}$, $r(x) = \\text{softmax}(W_r x)$, where $W_r \\in \\mathbb{R}^{N \\times d}$"),
    ("- 激活数 $k \\in \\{1, ..., N\\}$", "- Number of active experts $k \\in \\{1, ..., N\\}$"),
    ("> 对输入 token $x \\in \\mathbb{R}^d$，输出为", "> For input token $x \\in \\mathbb{R}^d$, the output is"),
    ("> 其中 $\\mathcal{A}(x) = \\arg\\max_k r(x)$ 是得分最高的$k$个专家的索引集合。", "> where $\\mathcal{A}(x) = \\arg\\max_k r(x)$ is the set of indices of the $k$ highest-scoring experts."),
    ("我们假设训练已完成后进行后处理规范固定(post-hoc gauge fixing)，类似于EGP工作中的后处理投影方法。训练阶段不施加规范约束——这已被证明是次优的~[EGP论文，$\\lambda$扫描失败]。",
     "We assume that post-hoc gauge fixing is performed after training has completed, similar to the post-hoc projection method in the EGP work. No gauge constraints are imposed during training -- this has been shown to be suboptimal [EGP paper, $\\lambda$ scan failure]."),
    ("设第$\\ell$层MoE的输入为$x^{(\\ell)}$。残差连接", "Let the input to the $\\ell$-th MoE layer be $x^{(\\ell)}$. The residual connection"),
    ("使得规范自由度得以存在：上游LayerNorm和下游投影矩阵可以自适应地吸收专家输出的规范变换，使得训练损失在局域上对这些变换不敏感。",
     "enables gauge freedom to exist: upstream LayerNorm and downstream projection matrices can adaptively absorb gauge transformations of expert outputs, making the training loss locally insensitive to these transformations."),
    ("存在一个校准数据集 $\\mathcal{D}_{cal} = \\{x_i\\}_{i=1}^{n_{cal}}$，大小为 $n_{cal} \\geq N \\cdot d$，可用于估计规范参数。校准集不需要标签——仅需要输入token。这满足实际中常见的情况。",
     "There exists a calibration dataset $\\mathcal{D}_{cal} = \\{x_i\\}_{i=1}^{n_{cal}}$ of size $n_{cal} \\geq N \\cdot d$, which can be used to estimate gauge parameters. The calibration set does not require labels -- only input tokens. This matches common practical scenarios."),

    # GAUGE FORMALIZATION
    ("## 规范自由度的形式化", "## Formalization of Gauge Freedom"),
    ("### 路由器的规范非不变性", "### Gauge Non-Invariance of the Router"),
    ("> **Theorem:** [路由器的规范非不变性]<!-- thm:noninvariance  -->", "> **Theorem:** [Gauge Non-Invariance of the Router]<!-- thm:noninvariance -->"),
    ("> 设路由器 $r(x) = \\text{softmax}(W_r x)$，其中 $W_r \\in \\mathbb{R}^{N \\times d}$ 在训练后固定。对专家$m$施加平移规范变换 $E_m \\to E_m + \\mathbf{g}_m$（其中 $\\mathbf{g}_m \\in \\mathbb{R}^d$），路由分数在变换**不**改变——即 $r(x)$ 对 $E_m$ 输出的显式依赖为零，因为 $r(x)$ 不接收$E_m(x)$作为输入。",
     "> Let the router be $r(x) = \\text{softmax}(W_r x)$, where $W_r \\in \\mathbb{R}^{N \\times d}$ is fixed after training. Applying a translation gauge transformation $E_m \\to E_m + \\mathbf{g}_m$ (where $\\mathbf{g}_m \\in \\mathbb{R}^d$) to expert $m$, the routing score does **not** change under the transformation -- i.e., $r(x)$ has zero explicit dependence on $E_m$ output, because $r(x)$ does not receive $E_m(x)$ as input."),
    ("> 然而，路由器在训练中被**隐式地**调谐以匹配专家的输出分布。具体而言，训练期间路由器的梯度为",
     "> However, the router is **implicitly** tuned during training to match the output distribution of the experts. Specifically, the gradient of the router during training is"),
    ("> 其中 $\\partial y / \\partial r$ 依赖于 $E_m(x)$ 的值。因此，$W_r$ 的最优值**依赖于训练时专家的输出分布**。当训练后施加规范变换 $E_m \\to E_m + \\mathbf{g}_m$，训练时的 $W_r^*$ 不再是新规范下的最优路由器。",
     "> where $\\partial y / \\partial r$ depends on the values of $E_m(x)$. Therefore, the optimal value of $W_r$ **depends on the output distribution of the experts during training**. When a gauge transformation $E_m \\to E_m + \\mathbf{g}_m$ is applied after training, the $W_r^*$ from training is no longer optimal under the new gauge."),
    ("> 具体而言，设原始规范(训练时)的专家输出为 $\\{E_m^{train}\\}$，路由器为 $W_r^{train}$。在规范变换后，专家输出变为 $\\{E_m^{train} + \\mathbf{g}_m\\}$。路由损失的最优值在两种规范下的差异由以下不等式控制：",
     "> Specifically, let the expert outputs in the original gauge (during training) be $\\{E_m^{train}\\}$, with router $W_r^{train}$. After the gauge transformation, expert outputs become $\\{E_m^{train} + \\mathbf{g}_m\\}$. The difference in optimal routing loss between the two gauges is bounded by the following inequality:"),
    ("> 其中 $L_r$ 是 $\\mathcal{L}$ 关于 $W_r$ 的Lipschitz常数。",
     "> where $L_r$ is the Lipschitz constant of $\\mathcal{L}$ with respect to $W_r$."),

    # Proof section
    ("> **Proof:** 考虑路由器在训练结束时的最优性条件。训练期间的损失函数为",
     "> **Proof:** Consider the optimality condition of the router at the end of training. The loss function during training is"),
    ("> 设训练收敛后 $W_r^{train} \\approx \\arg\\min_{W_r} \\mathcal{L}(W_r; \\{E_m^{train}\\})$。规范变换后，新的损失面为",
     "> Suppose after training convergence, $W_r^{train} \\approx \\arg\\min_{W_r} \\mathcal{L}(W_r; \\{E_m^{train}\\})$. After the gauge transformation, the new loss landscape is"),
    ("> 关键点：$\\mathcal{L}(W_r^{train}; \\{E_m^{train}\\})$ 在 $W_r^{train}$ 处达到(近似)极小值。但 $\\mathcal{L}'(W_r^{train})$ 在 $W_r^{train}$ 处**不一定**是极小值——规范变换改变了损失面本身，因为",
     "> Key point: $\\mathcal{L}(W_r^{train}; \\{E_m^{train}\\})$ reaches a (near) minimum at $W_r^{train}$. But $\\mathcal{L}'(W_r^{train})$ is **not necessarily** a minimum at $W_r^{train}$ -- the gauge transformation changes the loss landscape itself, because"),
    ("> 中的 $(E_m^{train}(x) + \\mathbf{g}_m)$ 项不同于训练时。",
     "> the $(E_m^{train}(x) + \\mathbf{g}_m)$ term differs from the training time."),
    ("> 对子优性的边界：由于 $\\mathcal{L}$ 关于 $W_r$ 是 $L_r$-Lipschitz的（在合理的正则化条件下），且有界专家输出变化 $\\|\\delta E_m\\| = \\|\\mathbf{g}_m\\|$：",
     "> Bounding the suboptimality: Since $\\mathcal{L}$ is $L_r$-Lipschitz with respect to $W_r$ (under reasonable regularization conditions), with bounded expert output change $\\|\\delta E_m\\| = \\|\\mathbf{g}_m\\|$:"),

    ("因此 $|\\mathcal{L}'(W_r^{train}) - \\min_{W_r} \\mathcal{L}'(W_r)| \\leq 2 L_\\ell \\cdot \\max_m \\|\\mathbf{g}_m\\|$。令 $L_r = 2L_\\ell$ 即得结论。",
     "Therefore $|\\mathcal{L}'(W_r^{train}) - \\min_{W_r} \\mathcal{L}'(W_r)| \\leq 2 L_\\ell \\cdot \\max_m \\|\\mathbf{g}_m\\|$. Setting $L_r = 2L_\\ell$ yields the result."),
    ("> **Corollary:** [路由偏差的积累]<!-- cor:cumulative  -->", "> **Corollary:** [Accumulation of Routing Bias]<!-- cor:cumulative -->"),
    ("> 考虑一个$L$层的Transformer，每层有一个MoE子层。若每层存在大小为 $\\|\\mathbf{g}_m^{(\\ell)}\\| \\leq g_*$ 的规范偏差，则累计路由偏差在深度$L$下最多放大 $O(L \\cdot g_*)$，在最坏情况下导致末端层的专家选择与最优选择偏离 $O(L \\cdot g_*)$ 的Hellinger距离。",
     "> Consider an $L$-layer Transformer with an MoE sublayer in each layer. If each layer has gauge bias of size $\\|\\mathbf{g}_m^{(\\ell)}\\| \\leq g_*$, then the cumulative routing bias grows at most as $O(L \\cdot g_*)$ in depth $L$, causing the expert selection in the final layer to deviate from optimal by a Hellinger distance of $O(L \\cdot g_*)$ in the worst case."),

    # GAUGE EQUIVALENCE
    ("### 规范等价类", "### Gauge Equivalence Classes"),
    ("> **Definition:** [规范等价]<!-- def:gauge_equiv  -->", "> **Definition:** [Gauge Equivalence]<!-- def:gauge_equiv -->"),
    ("> 两个专家配置 $\\{E_m\\}$ 和 $\\{E_m'\\}$ 称为**规范等价的**，记作 $\\{E_m\\} \\sim_g \\{E_m'\\}$，如果存在规范变换 $\\gamma_m \\in \\mathcal{G}_m$ 使得 $E_m' = \\gamma_m \\circ E_m$ 对所有 $m$ 成立，且存在下游自适应使得训练损失不变。",
     "> Two expert configurations $\\{E_m\\}$ and $\\{E_m'\\}$ are called **gauge-equivalent**, denoted $\\{E_m\\} \\sim_g \\{E_m'\\}$, if there exist gauge transformations $\\gamma_m \\in \\mathcal{G}_m$ such that $E_m' = \\gamma_m \\circ E_m$ for all $m$, and there exist downstream adaptations that keep the training loss invariant."),
    ("> **Theorem:** [规范等价类中的路由器不唯一性]<!-- thm:nonuniq  -->", "> **Theorem:** [Non-Uniqueness of Router in Gauge Equivalence Classes]<!-- thm:nonuniq -->"),
    ("> 设 $\\{E_m\\}$ 和 $\\{E_m'\\}$ 是规范等价的配置，满足 $\\{E_m\\} \\sim_g \\{E_m'\\}$。设 $W_r^*$ 是 $\\{E_m\\}$ 下训练出的最优路由器。则存在规范变换使得 $W_r^*$ 在 $\\{E_m'\\}$ 下不是最优路由器，除非所有专家的规范变换相同（即 $\\gamma_1 = \\gamma_2 = ... = \\gamma_N$）。",
     "> Let $\\{E_m\\}$ and $\\{E_m'\\}$ be gauge-equivalent configurations satisfying $\\{E_m\\} \\sim_g \\{E_m'\\}$. Let $W_r^*$ be the optimal router trained under $\\{E_m\\}$. Then there exist gauge transformations such that $W_r^*$ is not optimal under $\\{E_m'\\}$, unless all expert gauge transformations are the same (i.e., $\\gamma_1 = \\gamma_2 = ... = \\gamma_N$)."),
    ("> **Proof:** 假设所有 $\\gamma_m$ 相同（全局规范变换）。则 $\\sum_m r_m \\cdot \\gamma(E_m(x)) = \\gamma(\\sum_m r_m \\cdot E_m(x))$ 当 $\\gamma$ 线性时成立（平移和缩放满足线性性）。此时路由器的最优性被保持。",
     "> **Proof:** Assume all $\\gamma_m$ are the same (global gauge transformation). Then $\\sum_m r_m \\cdot \\gamma(E_m(x)) = \\gamma(\\sum_m r_m \\cdot E_m(x))$ holds when $\\gamma$ is linear (translation and scaling satisfy linearity). In this case, the optimality of the router is preserved."),
    ("> 若 $\\gamma_m$ 不全部相同，则存在 $m_1, m_2$ 使得 $\\gamma_{m_1} \\neq \\gamma_{m_2}$。考虑输入 $x$ 使得 $E_{m_1}(x) = E_{m_2}(x)$（在训练分布中存在这样的点，因为 $d \\ll$ 数据维度）。在原始规范中，$r_{m_1}(x) = r_{m_2}(x)$。在新规范中，输出为 $\\gamma_{m_1}(E_{m_1}(x))$ 和 $\\gamma_{m_2}(E_{m_2}(x))$ 不等——但路由器仍给相同分数，这是次优的。",
     "> If the $\\gamma_m$ are not all identical, then there exist $m_1, m_2$ such that $\\gamma_{m_1} \\neq \\gamma_{m_2}$. Consider an input $x$ such that $E_{m_1}(x) = E_{m_2}(x)$ (such points exist in the training distribution because $d \\ll$ data dimension). In the original gauge, $r_{m_1}(x) = r_{m_2}(x)$. In the new gauge, the outputs $\\gamma_{m_1}(E_{m_1}(x))$ and $\\gamma_{m_2}(E_{m_2}(x))$ are unequal -- but the router still gives the same score, which is suboptimal."),
    ("> 更严格地：令 $W_r^*$ 是 $\\{E_m\\}$ 下的最优路由器，其一阶最优条件为",
     "> More rigorously: Let $W_r^*$ be the optimal router under $\\{E_m\\}$, with first-order optimality condition"),
    ("> 在 $\\{E_m'\\}$ 下，梯度为", "> Under $\\{E_m'\\}$, the gradient is"),
    ("> 其中 $\\bar{y} = \\sum_m r_m \\cdot \\gamma_m \\circ E_m$。此梯度一般非零——除非所有 $\\gamma_m$ 相同。因此 $W_r^*$ 不再满足最优条件。",
     "> where $\\bar{y} = \\sum_m r_m \\cdot \\gamma_m \\circ E_m$. This gradient is generally non-zero -- unless all $\\gamma_m$ are the same. Therefore $W_r^*$ no longer satisfies the optimality condition."),
    ("> **Corollary:** [规范固定是必要的]<!-- cor:necessity  -->", "> **Corollary:** [Gauge Fixing is Necessary]<!-- cor:necessity -->"),
    ("> 在MoE中进行任何有意义的跨专家比较之前，规范固定(gauge fixing)是**数学上必要的**——路由器训练在一个隐含的规范选择下进行，而这个选择在推理时可能不成立。",
     "> Before any meaningful cross-expert comparison in MoE, gauge fixing is **mathematically necessary** -- the router is trained under an implicit gauge choice, and this choice may not hold at inference time."),

    # MILP GAUGE FIXING
    ("## MILP规范固定", "## MILP Gauge Fixing"),
    ("### MILP公式化", "### MILP Formulation"),
    ("我们将规范固定表述为一个优化问题：寻找规范参数 $\\{\\mathbf{g}_m\\}$ 使得在给定的校准输入集上，专家输出在同一个\"坐标系\"中尽可能可比。",
     "We formulate gauge fixing as an optimization problem: find gauge parameters $\\{\\mathbf{g}_m\\}$ such that expert outputs are as comparable as possible in the same \"coordinate system\" over the given calibration input set."),
    ("> **Definition:** [MILP规范固定问题]<!-- def:milp_gf  -->", "> **Definition:** [MILP Gauge Fixing Problem]<!-- def:milp_gf -->"),
    ("> 给定校准集 $\\mathcal{D}_{cal} = \\{(x_i, y_i^*)\\}_{i=1}^{n}$（其中 $y_i^*$ 可以缺失——无监督版本仅用$x_i$），寻找规范参数 $\\{\\mathbf{g}_m \\in \\mathbb{R}^d\\}_{m=1}^N$ 和路由指示 $\\{z_{im} \\in \\{0,1\\}\\}$ 使得",
     "> Given a calibration set $\\mathcal{D}_{cal} = \\{(x_i, y_i^*)\\}_{i=1}^{n}$ (where $y_i^*$ can be missing -- the unsupervised version uses only $x_i$), find gauge parameters $\\{\\mathbf{g}_m \\in \\mathbb{R}^d\\}_{m=1}^N$ and routing indicators $\\{z_{im} \\in \\{0,1\\}\\}$ such that"),
    ("> 其中 $\\bar{E}(x_i)$ 是规范固定后的平均专家输出（它本身依赖 $\\{\\mathbf{g}_m\\}$），$N_{avg} = nk/N$ 是理想的平均负载，$\\alpha, \\beta \\in (0, 2)$ 是负载均衡松弛参数。",
     "> where $\\bar{E}(x_i)$ is the mean expert output after gauge fixing (which itself depends on $\\{\\mathbf{g}_m\\}$), $N_{avg} = nk/N$ is the ideal average load, and $\\alpha, \\beta \\in (0, 2)$ are load-balancing slack parameters."),
    ("> **Remark:** 等式 [ref]消除全局规范自由度——没有这个约束，所有$\\mathbf{g}_m$可以整体平移。选择零和条件是最自然的规范固定条件，与EGP工作中 $\\sum_Z \\pi_Z \\mathbf{c}_Z = 0$ 的条件完全平行。",
     "> **Remark:** Equation [ref] eliminates the global gauge freedom -- without this constraint, all $\\mathbf{g}_m$ can be translated as a whole. Choosing the zero-sum condition is the most natural gauge fixing condition, completely parallel to the condition $\\sum_Z \\pi_Z \\mathbf{c}_Z = 0$ in the EGP work."),

    # CONVEX RELAXATION
    ("### 凸松弛", "### Convex Relaxation"),
    ("MILP [ref]-- [ref]在整数约束 $z_{im} \\in \\{0,1\\}$ 下是NP-难的。我们提供紧致凸松弛。",
     "MILP [ref]--[ref] is NP-hard under the integer constraint $z_{im} \\in \\{0,1\\}$. We provide a tight convex relaxation."),
    ("> **Theorem:** [凸松弛]<!-- thm:convex_relax  -->", "> **Theorem:** [Convex Relaxation]<!-- thm:convex_relax -->"),
    ("> 将 $z_{im} \\in \\{0,1\\}$ 松弛为 $z_{im} \\in [0,1]$，并将目标函数中的 $z_{im} \\cdot \\|E_m(x_i) - \\mathbf{g}_m - \\bar{E}(x_i)\\|^2$ 替换为以下上界：",
     "> Relax $z_{im} \\in \\{0,1\\}$ to $z_{im} \\in [0,1]$, and replace $z_{im} \\cdot \\|E_m(x_i) - \\mathbf{g}_m - \\bar{E}(x_i)\\|^2$ in the objective with the following upper bound:"),
    ("> 则松弛后的问题是关于 $(\\{z_{im}\\}, \\{\\mathbf{g}_m\\})$ 的**联合凸优化问题**，可在 $O(n N d^2)$ 时间内通过投影梯度下降求解。",
     "> Then the relaxed problem is a **jointly convex optimization problem** in $(\\{z_{im}\\}, \\{\\mathbf{g}_m\\})$, solvable via projected gradient descent in $O(n N d^2)$ time."),
    ("> **Proof:** 令 $\\Phi(z, g) = \\sum_{i,m} z_{im} \\|E_{im} - \\mathbf{g}_m - \\bar{E}_i\\|^2$，其中 $E_{im} = E_m(x_i)$ 且 $\\bar{E}_i = \\frac{1}{k}\\sum_{m} z_{im} E_{im}$。",
     "> **Proof:** Let $\\Phi(z, g) = \\sum_{i,m} z_{im} \\|E_{im} - \\mathbf{g}_m - \\bar{E}_i\\|^2$, where $E_{im} = E_m(x_i)$ and $\\bar{E}_i = \\frac{1}{k}\\sum_{m} z_{im} E_{im}$."),
    ("> 目标函数展开为：", "> Expanding the objective:"),
    ("> 固定 $z$ 时，$\\Phi$ 是关于 $\\mathbf{g}_m$ 的二次型，系数矩阵为 $\\text{diag}(\\sum_i z_{i1}, ..., \\sum_i z_{iN}) \\otimes I_d$，是正半定的。固定 $\\mathbf{g}$ 时，$\\Phi$ 是关于 $z_{im}$ 的线性函数加上 $z_{im}$ 的二次项（来自 $\\bar{E}_i$ 中的依赖），后者通过构造可被线性化。",
     "> When $z$ is fixed, $\\Phi$ is a quadratic form in $\\mathbf{g}_m$, with coefficient matrix $\\text{diag}(\\sum_i z_{i1}, ..., \\sum_i z_{iN}) \\otimes I_d$, which is positive semidefinite. When $\\mathbf{g}$ is fixed, $\\Phi$ is a linear function of $z_{im}$ plus quadratic terms in $z_{im}$ (from the dependence in $\\bar{E}_i$), which can be linearized by construction."),
    ("> 联合凸性来自 $z$ 和 $\\mathbf{g}$ 各自凸、且耦合项为双线性的结构。约束集(松弛后)是凸多面体。复杂度 $O(n N d^2)$ 来自每步梯度计算中 $N$ 个专家的 $d \\times d$ 矩阵乘法。",
     "> Joint convexity follows from the structure where $z$ and $\\mathbf{g}$ are each convex and the coupling term is bilinear. The constraint set (after relaxation) is a convex polytope. The complexity $O(n N d^2)$ comes from the $d \\times d$ matrix multiplications for $N$ experts in each gradient computation step."),

    # GREEDY APPROXIMATION
    ("### 贪心近似", "### Greedy Approximation"),
    ("在实际应用中——特别是在推理时——我们可能需要比凸松弛更快的规范固定。以下贪心算法提供一个 $O(n N d + n k \\log N)$ 时间的近似。",
     "In practical applications -- especially at inference time -- we may need gauge fixing faster than convex relaxation. The following greedy algorithm provides an $O(n N d + n k \\log N)$ approximation."),
    ("*Caption:* 贪心规范固定(Greedy Gauge Fixing)", ""),
    ("> **Theorem:** [贪心近似的保障]<!-- thm:greedy_bound  -->", "> **Theorem:** [Guarantee for Greedy Approximation]<!-- thm:greedy_bound -->"),
    ("> 假设专家的输出分布具有相同的协方差结构，即 $\\text{Cov}[E_m(x)] = \\Sigma$ 对所有 $m$。则算法 [ref]找到的 $\\{\\hat{\\mathbf{g}}_m\\}$ 与MILP最优解 $\\{\\mathbf{g}_m^*\\}$ 满足",
     "> Assume that the expert output distributions share the same covariance structure, i.e., $\\text{Cov}[E_m(x)] = \\Sigma$ for all $m$. Then the $\\{\\hat{\\mathbf{g}}_m\\}$ found by Algorithm [ref] and the MILP optimal solution $\\{\\mathbf{g}_m^*\\}$ satisfy"),
    ("> **Proof:** 贪心算法等价于以样本均值估计每个专家的输出期望：$\\hat{\\mu}_m = \\frac{1}{n}\\sum_i E_{im}$。由Hoeffding不等式（在次高斯假设下），",
     "> **Proof:** The greedy algorithm is equivalent to estimating each expert's output expectation by the sample mean: $\\hat{\\mu}_m = \\frac{1}{n}\\sum_i E_{im}$. By Hoeffding's inequality (under sub-Gaussian assumption),"),
    ("> 期望平方误差为 $\\mathbb{E}[\\|\\hat{\\mu}_m - \\mu_m\\|^2] = \\frac{\\text{Tr}(\\Sigma)}{n}$。",
     "> The expected squared error is $\\mathbb{E}[\\|\\hat{\\mu}_m - \\mu_m\\|^2] = \\frac{\\text{Tr}(\\Sigma)}{n}$."),
    ("> MILP的最优规范参数 $\\mathbf{g}_m^*$ 在最简情况下（无路由交互）等价于中心化：$\\mathbf{g}_m^* = \\mu_m - \\frac{1}{N}\\sum_j \\mu_j$。贪心算法估计此量为 $\\hat{\\mathbf{g}}_m = \\hat{\\mu}_m - \\frac{1}{N}\\sum_j \\hat{\\mu}_j$。误差为",
     "> The MILP optimal gauge parameters $\\mathbf{g}_m^*$ in the simplest case (no routing interaction) are equivalent to centering: $\\mathbf{g}_m^* = \\mu_m - \\frac{1}{N}\\sum_j \\mu_j$. The greedy algorithm estimates this as $\\hat{\\mathbf{g}}_m = \\hat{\\mu}_m - \\frac{1}{N}\\sum_j \\hat{\\mu}_j$. The error is"),
    ("> 加上归一化步骤后，整体误差以 $2\\text{Tr}(\\Sigma)/n \\cdot (1 + 1/N)$ 为界。",
     "> After adding the normalization step, the total error is bounded by $2\\text{Tr}(\\Sigma)/n \\cdot (1 + 1/N)$."),
]

# Apply translations
applied = 0
for old, new in translations:
    if old in text:
        text = text.replace(old, new)
        applied += 1
    else:
        print(f"MISS: {old[:80]}...")

print(f"Applied {applied}/{len(translations)} translations")

# ============== STEP 3: FINAL CLEANUP ==============
# Remove excessive blank lines
text = re.sub(r'\n{4,}', '\n\n\n', text)
# Remove trailing whitespace
lines = [line.rstrip() for line in text.split('\n')]
text = '\n'.join(lines)

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(text)

print("Done! File written.")
