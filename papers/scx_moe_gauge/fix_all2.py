#!/usr/bin/env python3
"""
Comprehensive fix: handle ALL remaining Chinese text and LaTeX artifacts
in scx_moe_gauge/main.md after mechanical cleanup.
"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    text = f.read()

# ============== STANDARDIZE QUOTES AND SPECIAL CHARS ==============
# Replace curly quotes with straight quotes for matching reliability
text = text.replace('“', '"')
text = text.replace('”', '"')
text = text.replace('‘', "'")
text = text.replace('’', "'")

# ============== COMPREHENSIVE TRANSLATIONS ==============
# (organized by section)

translations = {

    # === RULER METAPHOR ===
    '- **尺子 = MoE 专家网络** $E_m$.每个专家单独训练，在自己的领域里是“准的”（loss 低）':
        '- **Ruler = MoE expert network** $E_m$. Each expert is trained independently and is "accurate" in its own domain (low loss).',

    '- **拼尺子 = 路由器比较专家**。路由器用一个线性函数比较 8 个专家的“刻度”，但它不知道每个专家的零刻度在哪':
        '- **Piecing rulers = router comparing experts**. The router uses a linear function to compare the "markings" of 8 experts, but it does not know where each expert\'s zero mark is.',

    '1. **发现问题：** MoE 的不同专家活在各自的“坐标系”里。路由器在比较不可比的东西。这不是工程疏忽——这是数学结构：规范自由度。':
        '1. **Problem identification:** Different MoE experts live in their own "coordinate systems." The router is comparing incomparable things. This is not an engineering oversight -- it is a mathematical structure: gauge freedom.',

    '3. **意外收获：** 规范对齐后的 SVD 谱能检测 Yajie 漏掉的“共享幻觉”——所有专家一致同意的错误。真知识在表示空间里是低维的，共享幻觉是高维的。SVD 看得见这个区别。':
        '3. **Unexpected finding:** The SVD spectrum after gauge alignment can detect "shared hallucinations" missed by Yajie -- errors that all experts agree on. True knowledge is low-dimensional in representation space; shared hallucinations are high-dimensional. SVD can see this difference.',

    # === INTRODUCTION ===
    '**核心直觉**：专家 $E_1$ 和专家 $E_2$ 在训练中各自学会了不同的输出“基准”——$E_1$ 的输出天然偏“高”，$E_2$ 的输出天然偏“低”，即使对相似的输入也是如此。这个差异在各自训练时被残差连接的后续层自适应地吸收掉了，因此不被训练损失所感知。但是——':
        '**Core intuition:** Experts $E_1$ and $E_2$ each learn different output "baselines" during training -- $E_1$\'s output is naturally "higher," $E_2$\'s output is naturally "lower," even for similar inputs. This difference is adaptively absorbed by subsequent residual connection layers during training and is thus not perceived by the training loss. However --',

    '这些曲面在输出空间的高度、尺度、甚至方向上天然不同——不是因为任何专家“错了”，而是因为训练动力学允许一个规范自由度。':
        'These surfaces naturally differ in height, scale, and even direction in output space -- not because any expert is "wrong," but because the training dynamics permit a gauge freedom.',

    # === PROBLEM SETUP ===
    '- 路由器 $r: \\mathbb{R}^d \\to \\Delta^{N-1}$，$r(x) = \\text{softmax}(W_r x)$，其中 $W_r \\in \\mathbb{R}^{N \\times d}$':
        '- A router $r: \\mathbb{R}^d \\to \\Delta^{N-1}$, $r(x) = \\text{softmax}(W_r x)$, where $W_r \\in \\mathbb{R}^{N \\times d}$',

    # === GAUGE NON-INVARIANCE ===
    '> 设路由器 $r(x) = \\text{softmax}(W_r x)$，其中 $W_r \\in \\mathbb{R}^{N \\times d}$ 在训练后固定。对专家$m$施加平移规范变换 $E_m \\to E_m + \\mathbf{g}_m$（其中 $\\mathbf{g}_m \\in \\mathbb{R}^d$），路由分数在变换**不**改变——即 $r(x)$ 对 $E_m$ 输出的显式依赖为零，因为 $r(x)$ 不接收$E_m(x)$作为输入。':
        '> Let the router be $r(x) = \\text{softmax}(W_r x)$, where $W_r \\in \\mathbb{R}^{N \\times d}$ is fixed after training. Applying a translation gauge transformation $E_m \\to E_m + \\mathbf{g}_m$ (where $\\mathbf{g}_m \\in \\mathbb{R}^d$) to expert $m$, the routing score does **not** change under the transformation -- i.e., $r(x)$ has zero explicit dependence on $E_m$ output, because $r(x)$ does not receive $E_m(x)$ as input.',

    '> 若 $\\gamma_m$ 不全部相同，则存在 $m_1, m_2$ 使得 $\\gamma_{m_1} \\neq \\gamma_{m_2}$。考虑输入 $x$ 使得 $E_{m_1}(x) = E_{m_2}(x)$（在训练分布中存在这样的点，因为 $d \\ll$ 数据维度）。在原始规范中，$r_{m_1}(x) = r_{m_2}(x)$。在新规范中，输出为 $\\gamma_{m_1}(E_{m_1}(x))$ 和 $\\gamma_{m_2}(E_{m_2}(x))$ 不等——但路由器仍给相同分数，这是次优的。':
        '> If the $\\gamma_m$ are not all identical, then there exist $m_1, m_2$ such that $\\gamma_{m_1} \\neq \\gamma_{m_2}$. Consider an input $x$ such that $E_{m_1}(x) = E_{m_2}(x)$ (such points exist in the training distribution because $d \\ll$ data dimension). In the original gauge, $r_{m_1}(x) = r_{m_2}(x)$. In the new gauge, the outputs $\\gamma_{m_1}(E_{m_1}(x))$ and $\\gamma_{m_2}(E_{m_2}(x))$ are unequal -- but the router still gives the same score, which is suboptimal.',

    # === MILP ===
    '我们将规范固定表述为一个优化问题：寻找规范参数 $\\{\\mathbf{g}_m\\}$ 使得在给定的校准输入集上，专家输出在同一个“坐标系”中尽可能可比。':
        'We formulate gauge fixing as an optimization problem: find gauge parameters $\\{\mathbf{g}_m\\}$ such that expert outputs are as comparable as possible in the same "coordinate system" over the given calibration input set.',

    # === GREEDY ALGORITHM TEXT ===
    # Fix the \mathbb{R}equire and \mathbb{E}nsure artifacts
    '\\mathbb{R}equire': '**Require:',
    '\\mathbb{E}nsure': '**Ensure:',

    '规范参数 $\\{\\hat{\\mathbf{g}}_m\\}_{m=1}^{N}$':
        'Gauge parameters $\\{\\hat{\\mathbf{g}}_m\\}_{m=1}^{N}$',

    '校准集 $\\mathcal{D}_{cal} = \\{x_i\\}_{i=1}^{n}$，专家 $\\{E_m\\}$，激活数 $k$':
        'Calibration set $\\mathcal{D}_{cal} = \\{x_i\\}_{i=1}^{n}$, experts $\\{E_m\\}$, number of active experts $k$',

    '- 对所有 $i, m$ 计算 $E_{im} = E_m(x_i)$':
        '1. Compute $E_{im} = E_m(x_i)$ for all $i, m$',

    '- 初始化 $\\hat{\\mathbf{g}}_m \\leftarrow \\mathbf{0}$ 对所有 $m$':
        '2. Initialize $\\hat{\\mathbf{g}}_m \\leftarrow \\mathbf{0}$ for all $m$',

    '- 计算全局均值 $\\bar{E} = \\frac{1}{Nn} \\sum_{i,m} E_{im}$ ($O(Nnd)$':
        '3. Compute global mean $\\bar{E} = \\frac{1}{Nn} \\sum_{i,m} E_{im}$  ($O(Nnd)$)',

    '- \\quad $\\hat{\\mathbf{g}}_m \\leftarrow \\hat{\\mathbf{g}}_m + \\frac{1}{n}\\sum_{i=1}^{n} E_{im} - \\bar{E}$ (平移规范固定':
        '4. $\\hat{\\mathbf{g}}_m \\leftarrow \\hat{\\mathbf{g}}_m + \\frac{1}{n}\\sum_{i=1}^{n} E_{im} - \\bar{E}$  (translation gauge fixing)',

    '- \\quad $\\hat{\\mathbf{g}}_m \\leftarrow \\hat{\\mathbf{g}}_m / \\|\\hat{\\mathbf{g}}_m\\|$ (归一化':
        '5. $\\hat{\\mathbf{g}}_m \\leftarrow \\hat{\\mathbf{g}}_m / \\|\\hat{\\mathbf{g}}_m\\|$  (normalization)',

    '- 投影至零和：$\\hat{\\mathbf{g}}_m \\leftarrow \\hat{\\mathbf{g}}_m - \\frac{1}{N}\\sum_{j=1}^{N} \\hat{\\mathbf{g}}_j$':
        '6. Project to zero-sum: $\\hat{\\mathbf{g}}_m \\leftarrow \\hat{\\mathbf{g}}_m - \\frac{1}{N}\\sum_{j=1}^{N} \\hat{\\mathbf{g}}_j$',

    # GREEDY PROOF
    '> **Proof:** 贪心算法等价于以样本均值估计每个专家的输出期望：$\\hat{\\mu}_m = \\frac{1}{n}\\sum_i E_{im}$。由Hoeffding不等式（在次高斯假设下），':
        '> **Proof:** The greedy algorithm is equivalent to estimating each expert\'s output expectation by the sample mean: $\\hat{\\mu}_m = \\frac{1}{n}\\sum_i E_{im}$. By Hoeffding\'s inequality (under sub-Gaussian assumption),',

    '> 期望平方误差为 $\\mathbb{E}[\\|\\hat{\\mu}_m - \\mu_m\\|^2] = \\frac{{\\cal T}r(\\Sigma)}{n}$。':
        '> The expected squared error is $\\mathbb{E}[\\|\\hat{\\mu}_m - \\mu_m\\|^2] = \\frac{\\text{Tr}(\\Sigma)}{n}$.',

    '> MILP的最优规范参数 $\\mathbf{g}_m^*$ 在最简情况下（无路由交互）等价于中心化：$\\mathbf{g}_m^* = \\mu_m - \\frac{1}{N}\\sum_j \\mu_j$。贪心算法估计此量为 $\\hat{\\mathbf{g}}_m = \\hat{\\mu}_m - \\frac{1}{N}\\sum_j \\hat{\\mu}_j$。误差为':
        '> The MILP optimal gauge parameters $\\mathbf{g}_m^*$ in the simplest case (no routing interaction) are equivalent to centering: $\\mathbf{g}_m^* = \\mu_m - \\frac{1}{N}\\sum_j \\mu_j$. The greedy algorithm estimates this as $\\hat{\\mathbf{g}}_m = \\hat{\\mu}_m - \\frac{1}{N}\\sum_j \\hat{\\mu}_j$. The error is',

    '> 加上归一化步骤后，整体误差以 $2{\\cal T}r(\\Sigma)/n \\cdot (1 + 1/N)$ 为界。':
        '> After adding the normalization step, the total error is bounded by $2\\text{Tr}(\\Sigma)/n \\cdot (1 + 1/N)$.',

    # Fix \mathcal{T}r -> \text{Tr}
    '{\\cal T}r': '\\text{Tr}',
}

# Apply translations
for old, new in translations.items():
    if old in text:
        text = text.replace(old, new)
    else:
        # Try matching with escaped or unescaped versions
        print(f"  MISS: {old[:80]}...")

# Fix remaining \mathcal{T}r patterns
text = text.replace('\\mathcal{T}r', '\\text{Tr}')

# Fix \sigma_(\mathbf{Y}) -> \sigma_*(\mathbf{Y})
text = text.replace('\\sigma_(\\mathbf{Y})', '\\sigma_*(\\mathbf{Y})')
text = text.replace('\\sigma_^2(\\mathbf{Y})', '\\sigma_*^2(\\mathbf{Y})')
text = text.replace('/\\sigma_^2', '/\\sigma_*^2')

# Fix the abstract \mathcal{G)_m issue
text = text.replace('$\\mathcal{G)_m$', '$\\mathcal{G}_m$')

# ============== SECTION HEADERS REMAINING ==============
remaining_sections = {
    '## SVD幻觉检测的规范对齐版本': '## Gauge-Aligned SVD Hallucination Detection',
    '### 规范不对齐如何破坏SVD检测': '### How Gauge Misalignment Destroys SVD Detection',
    '在之前的工作中~〔哈密顿量审计论文〕，我们提出了使用SVD谱作为幻觉检测指标：对同一查询询问模型$M$次，取最后一层的hidden state矩阵 $\\mathbf{H} \\in \\mathbb{R}^{M \\times d}$，计算SVD $\\mathbf{H} = \\mathbf{U} \\boldsymbol{\\Sigma} \\mathbf{V}^T$，定义':
        'In prior work [Hamiltonian Audit paper], we proposed using the SVD spectrum as a hallucination detection metric: query the model $M$ times on the same query, take the last-layer hidden state matrix $\\mathbf{H} \\in \\mathbb{R}^{M \\times d}$, compute the SVD $\\mathbf{H} = \\mathbf{U} \\boldsymbol{\\Sigma} \\mathbf{V}^T$, and define',

    '若 $\\rho_{10} > 0.9$，模型对此问题确信；若 $\\rho_{100} < 0.5$，模型在胡说八道。':
        'If $\\rho_{10} > 0.9$, the model is confident on this question; if $\\rho_{100} < 0.5$, the model is hallucinating.',

    '**但这是在单模型上做的。** 在MoE中，同样的方法应用于多专家输出时面临一个根本问题：':
        '**But this was done on a single model.** In MoE, applying the same method to multi-expert outputs faces a fundamental problem:',

    '> **Theorem:** [规范不对齐破坏SVD集中性]<!-- thm:svd_gauge  -->':
        '> **Theorem:** [Gauge Misalignment Destroys SVD Concentration]<!-- thm:svd_gauge -->',

    '> 设 $N$ 个专家对同一输入 $x$ 的输出矩阵为 $\\mathbf{Y} = [E_1(x), ..., E_N(x)]^T \\in \\mathbb{R}^{N \\times d}$。在规范变换 $\\mathbf{Y} \\to \\mathbf{Y} + \\mathbf{G}$ 下（其中 $\\mathbf{G} = [\\mathbf{g}_1, ..., \\mathbf{g}_N]^T$），有效秩 $r_{eff}(\\mathbf{Y})$ 满足':
        '> Let the output matrix of $N$ experts on the same input $x$ be $\\mathbf{Y} = [E_1(x), ..., E_N(x)]^T \\in \\mathbb{R}^{N \\times d}$. Under the gauge transformation $\\mathbf{Y} \\to \\mathbf{Y} + \\mathbf{G}$ (where $\\mathbf{G} = [\\mathbf{g}_1, ..., \\mathbf{g}_N]^T$), the effective rank $r_{eff}(\\mathbf{Y})$ satisfies',

    # SVD proof
    '> **Proof:** 由Weyl不等式，对每个奇异值 $\\sigma_i(\\mathbf{Y} + \\mathbf{G}) \\geq \\sigma_i(\\mathbf{Y}) - \\|\\mathbf{G}\\|_2$。同时 $\\|\\mathbf{G}\\|_2 \\leq \\|\\mathbf{G}\\|_F$。':
        '> **Proof:** By Weyl\'s inequality, for each singular value $\\sigma_i(\\mathbf{Y} + \\mathbf{G}) \\geq \\sigma_i(\\mathbf{Y}) - \\|\\mathbf{G}\\|_2$. Also $\\|\\mathbf{G}\\|_2 \\leq \\|\\mathbf{G}\\|_F$.',

    '> 定义有效秩为满足 $\\sum_{i=1}^{r} \\sigma_i^2 \\geq \\rho \\cdot \\|\\mathbf{Y}\\|_F^2$ 的最小 $r$（取 $\\rho = 0.95$）。规范扰动引入的额外能量散布为 $\\|\\mathbf{G}\\|_F^2$，这增加最多 $\\|\\mathbf{G}\\|_F^2 / \\sigma_*^2$ 个有效维度。':
        '> Define effective rank as the smallest $r$ satisfying $\\sum_{i=1}^{r} \\sigma_i^2 \\geq \\rho \\cdot \\|\\mathbf{Y}\\|_F^2$ (take $\\rho = 0.95$). The additional energy spread introduced by the gauge perturbation is $\\|\\mathbf{G}\\|_F^2$, which adds at most $\\|\\mathbf{G}\\|_F^2 / \\sigma_*^2$ effective dimensions.',

    '> 具体而言，设原始矩阵的平方Frobenius范数为 $S = \\|\\mathbf{Y}\\|_F^2$，前$r$个奇异值捕获比例 $\\rho$：即 $\\sum_{i=1}^{r} \\sigma_i^2 = \\rho S$。扰动后，总能量变为':
        '> Specifically, let the squared Frobenius norm of the original matrix be $S = \\|\\mathbf{Y}\\|_F^2$, with the first $r$ singular values capturing proportion $\\rho$: i.e., $\\sum_{i=1}^{r} \\sigma_i^2 = \\rho S$. After perturbation, the total energy becomes',

    '> 最坏情况下，$\\langle \\mathbf{Y}, \\mathbf{G} \\rangle_F = -\\|\\mathbf{Y}\\|_F \\|\\mathbf{G}\\|_F$（反相关），总能量变为 $S + \\|\\mathbf{G}\\|_F^2 - 2\\sqrt{S}\\|\\mathbf{G}\\|_F$。':
        '> In the worst case, $\\langle \\mathbf{Y}, \\mathbf{G} \\rangle_F = -\\|\\mathbf{Y}\\|_F \\|\\mathbf{G}\\|_F$ (anti-correlated), the total energy becomes $S + \\|\\mathbf{G}\\|_F^2 - 2\\sqrt{S}\\|\\mathbf{G}\\|_F$.',

    '> 为保持相同的捕获比例 $\\rho$，需要的奇异值数量最多增加':
        '> To maintain the same capture ratio $\\rho$, the number of singular values needed increases by at most',

    '> 这给出声明中的下界。':
        '> This gives the lower bound in the statement.',

    '> **诚实暴击:** 这意味着：不固定规范就做SVD检测，你分不清谱的平坦是因为模型在幻觉，还是因为专家的规范不对齐导致的“假性弥散”。规范对齐是SVD检测的前提条件。}':
        '> **Honest Strike:** This means: if you perform SVD detection without gauge fixing, you cannot tell whether the spectral flatness is due to the model hallucinating, or due to the "pseudo-dispersion" caused by expert gauge misalignment. Gauge alignment is a prerequisite for SVD detection.',

    '### 规范对齐后的一致性检测':
        '### Consistency Detection After Gauge Alignment',

    '> **Theorem:** [规范对齐后的一致性保证]<!-- thm:aligned_svd  -->':
        '> **Theorem:** [Consistency Guarantee After Gauge Alignment]<!-- thm:aligned_svd -->',

    '> **Corollary:** [实用判据]<!-- cor:practical  -->':
        '> **Corollary:** [Practical Criterion]<!-- cor:practical -->',

    '> 在实际部署中，对每个查询：':
        '> In practical deployment, for each query:',

    '1. 在规范固定后的输出矩阵 $\\tilde{\\mathbf{Y}}$ 上执行SVD':
        '1. Compute SVD on the gauge-fixed output matrix $\\tilde{\\mathbf{Y}}$',

    '2. 计算 $\\rho_{10} = \\sum_{i=1}^{10} \\sigma_i^2 / \\sum_i \\sigma_i^2$':
        '2. Compute $\\rho_{10} = \\sum_{i=1}^{10} \\sigma_i^2 / \\sum_i \\sigma_i^2$',

    '3. 若 $\\rho_{10} > 0.9$：模型内部共识 → 输出可信':
        '3. If $\\rho_{10} > 0.9$: internal consensus $\rightarrow$ output is trustworthy',

    '4. 若 $\\rho_{10} < 0.5$：模型内部无共识 → **必为幻觉**（以概率 $\\geq 1 - N e^{-2M_{eff}\\Delta^2}$ 的保证）':
        '4. If $\\rho_{10} < 0.5$: no internal consensus $\rightarrow$ **definitely hallucination** (with guarantee $\\geq 1 - N e^{-2M_{eff}\\Delta^2}$)',

    '5. 若 $0.5 \\leq \\rho_{10} \\leq 0.9$：灰色区域 → 需要额外验证':
        '5. If $0.5 \\leq \\rho_{10} \\leq 0.9$: gray area $\rightarrow$ additional verification needed',

    # UNIFICATION
    '## 与ACE规范固定的统一':
        '## Unification with ACE Gauge Fixing',

    '在本节中，我们展示MoE规范固定和ACE规范固定~〔EGP论文〕是同一数学结构的实例。':
        'In this section, we show that MoE gauge fixing and ACE gauge fixing [EGP paper] are instances of the same mathematical structure.',

    '### 共同结构：模块化组件 + 隐式规范群 + 后处理投影':
        '### Common Structure: Modular Components + Implicit Gauge Group + Post-hoc Projection',

    '> **Definition:** [模块化规范系统]<!-- def:modular_gauge  -->':
        '> **Definition:** [Modular Gauge System]<!-- def:modular_gauge -->',

    '> **Theorem:** [MGS中的规范固定必要性定理]<!-- thm:mgs_necessity  -->':
        '> **Theorem:** [Necessity of Gauge Fixing in MGS]<!-- thm:mgs_necessity -->',

    '### 深层原理':
        '### Deep Principle',

    # EXPERIMENTS
    '## 实验方案设计':
        '## Experimental Design',

    # And many more...
}

for old, new in remaining_sections.items():
    if old in text:
        text = text.replace(old, new)

# Replace unicode right/left arrows
text = text.replace('→', '$\rightarrow$')

# Clean up
text = re.sub(r'\n{4,}', '\n\n\n', text)
lines = [line.rstrip() for line in text.split('\n')]
text = '\n'.join(lines)

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(text)

print("Comprehensive cleanup done!")
