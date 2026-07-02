# -*- coding: utf-8 -*-
"""
Apply translations from Agent 1 (lines 1-400) and Agent 2 (lines 400-800).
Reads file line by line and replaces Chinese lines with English.
"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Build translation map: keyed by line index (0-based)
# We'll use fuzzy matching - find lines containing key Chinese phrases
# and replace their text

translations = {}

# Scan for Chinese lines and build translations
# This is based on the agent outputs for lines 1-800

# Helper: find a line containing specific Chinese text and replace it
def find_and_replace(chinese_fragment, english_text, start=0, end=None):
    """Find line containing chinese_fragment and replace with english_text"""
    if end is None:
        end = len(lines)
    for i in range(start, end):
        if chinese_fragment in lines[i]:
            lines[i] = english_text + '\n'
            return i
    return -1

# ====== LINES 1-400: Agent 1 translations ======
# Line 31: ruler metaphor
ruler_key = '尺子 = MoE'  # 尺子 = MoE
ruler_idx = find_and_replace(ruler_key,
    '- **Ruler = MoE expert network** $E_m$. Each expert is trained independently and is \\"accurate\\" in its own domain (low loss).',
    0, 100)
if ruler_idx < 0:
    print('MISS: ruler line')

# Line 33: piecing rulers
piecing_key = '拼尺子'  # 拼尺子
piecing_idx = find_and_replace(piecing_key,
    '- **Assembling rulers = router comparing experts**. The router uses a linear function to compare the \\"markings\\" of 8 experts, but it does not know where each expert\\'s zero mark is.',
    0, 100)
if piecing_idx < 0:
    print('MISS: piecing rulers line')

# Line 48: three sentence problem
find_and_replace('发现问题：',  # 发现问题：
    '1. **The problem:** Different MoE experts live in their own \\"coordinate systems\\". The router is comparing incomparable things. This is not an engineering oversight -- it is a mathematical structure: gauge degrees of freedom.',
    0, 100)

# Line 50: unexpected discovery
find_and_replace('意外收获：',  # 意外收获：
    '3. **Unexpected discovery:** The SVD spectrum after gauge alignment can detect \\"shared hallucinations\\" that Yajie misses -- errors that all experts agree on. True knowledge is low-dimensional in representation space; shared hallucinations are high-dimensional. SVD can see this difference.',
    0, 100)

# Line 79: core intuition
find_and_replace('核心直觉',  # 核心直觉
    '**Core intuition:** Expert $E_1$ and expert $E_2$ each learn different output \\"baselines\\" during training -- $E_1$\\'s output is naturally \\"higher\\", $E_2$\\'s output is naturally \\"lower\\", even for similar inputs. This difference is adaptively absorbed by the downstream layers of the residual connection during each one\\'s training, so it is not detected by the training loss. However --',
    60, 100)

# Line 89: surfaces naturally differ
find_and_replace('这些曲面在输出',  # 这些曲面在输出
    'These surfaces naturally differ in height, scale, and even direction in output space -- not because any expert is \\"wrong\\", but because the training dynamics permit a gauge degree of freedom.',
    80, 100)

# Line 155+: Let the router be
idx = find_and_replace('设路由器',  # 设路由器
    '> Let the router be $r(x) = \\text{softmax}(W_r x)$, where $W_r \\in \\mathbb{R}^{N \\times d}$ is fixed after training. Applying a translation gauge transformation $E_m \\to E_m + \\mathbf{g}_m$ (with $\\mathbf{g}_m \\in \\mathbb{R}^d$) to expert $m$, the routing score does **not** change under the transformation -- that is, $r(x)$ has zero explicit dependence on the output $E_m(x)$, because $r(x)$ does not receive $E_m(x)$ as input.',
    150, 200)
if idx < 0:
    print('MISS: Let the router line')

# Line 224: If gamma_m not all identical
find_and_replace('若 $\\gamma_m$ 不全',  # 若 $\gamma_m$ 不全
    '> If the $\\gamma_m$ are not all identical, there exist $m_1, m_2$ such that $\\gamma_{m_1} \\neq \\gamma_{m_2}$. Consider input $x$ such that $E_{m_1}(x) = E_{m_2}(x)$ (such points exist in the training distribution because $d \\ll$ data dimension). In the original gauge, $r_{m_1}(x) = r_{m_2}(x)$. In the new gauge, the outputs $\\gamma_{m_1}(E_{m_1}(x))$ and $\\gamma_{m_2}(E_{m_2}(x))$ are unequal -- but the router still assigns the same scores, which is suboptimal.',
    210, 250)

# Line 248: We formulate gauge fixing
find_and_replace('我们将规范固定表述',  # 我们将规范固定表述
    'We formulate gauge fixing as an optimization problem: find gauge parameters $\\{\\mathbf{g}_m\\}$ such that, on the given calibration input set, expert outputs are as comparable as possible in the same \\"coordinate system\\".',
    240, 260)

# Line 321: Greedy algorithm proof
idx = find_and_replace('贪心算法等价于',  # 贪心算法等价于
    '> **Proof:** The greedy algorithm is equivalent to estimating each expert\\'s output expectation by the sample mean: $\\hat{\\mu}_m = \\frac{1}{n}\\sum_i E_{im}$. By Hoeffding\\'s inequality (under the sub-Gaussian assumption),',
    310, 340)

# Line 327: Expected squared error
find_and_replace('期望平方误差',  # 期望平方误差
    '> The expected squared error is $\\mathbb{E}[\\|\\hat{\\mu}_m - \\mu_m\\|^2] = \\frac{\\text{Tr}(\\Sigma)}{n}$.',
    320, 340)

# Line 329: MILP optimal gauge
find_and_replace('MILP的最优规范',  # MILP的最优规范
    '> In the simplest case (without routing interaction), the optimal gauge parameters $\\mathbf{g}_m^*$ of the MILP are equivalent to centering: $\\mathbf{g}_m^* = \\mu_m - \\frac{1}{N}\\sum_j \\mu_j$. The greedy algorithm estimates this quantity as $\\hat{\\mathbf{g}}_m = \\hat{\\mu}_m - \\frac{1}{N}\\sum_j \\hat{\\mu}_j$. The error is',
    325, 340)

# Line 335: Expectation of squared norm
find_and_replace('平方范数的期望',  # 平方范数的期望
    '> Expectation of the squared norm:',
    330, 345)

# Line 345: After adding normalization
find_and_replace('加上归一化步骤',  # 加上归一化步骤
    '> After adding the normalization step, the total error is bounded by $2\\text{Tr}(\\Sigma)/n \\cdot (1 + 1/N)$.',
    340, 350)

# Line 352: SVD in prior work
find_and_replace('哈密顿量审计',  # 哈密顿量审计
    'In prior work [Hamiltonian Audit Paper], we proposed using the SVD spectrum as a hallucination detection metric: query the model $M$ times on the same question, take the hidden state matrix $\\mathbf{H} \\in \\mathbb{R}^{M \\times d}$ of the last layer, compute the SVD $\\mathbf{H} = \\mathbf{U} \\boldsymbol{\\Sigma} \\mathbf{V}^T$, and define',
    345, 365)

# Line 373: effective rank
find_and_replace('有效秩为满足',  # 有效秩为满足
    '> Define the effective rank as the smallest $r$ satisfying $\\sum_{i=1}^{r} \\sigma_i^2 \\geq \\rho \\cdot \\|\\mathbf{Y}\\|_F^2$ (taking $\\rho = 0.95$). The additional energy dispersion introduced by the gauge perturbation is $\\|\\mathbf{G}\\|_F^2$, which adds at most $\\|\\mathbf{G}\\|_F^2 / \\sigma_*^2$ effective dimensions.',
    368, 385)

# Line 391: Honest Strike SVD
find_and_replace('不固定规范就做SVD',  # 不固定规范就做SVD
    '> **Honest Strike:** This means: if you perform SVD detection without fixing the gauge, you cannot tell whether the flatness of the spectrum is due to the model hallucinating, or due to the \\"pseudo-dispersion\\" caused by gauge misalignment of the experts. Gauge alignment is a prerequisite for SVD detection.}',
    385, 400)

# ====== LINES 400-800: Agent 2 translations ======
# These are the major sections that need translation
# Experiment headers, discussion, etc.

# Fix Chinese section headers in the 400-800 range
section_fixes = {
    '## SVD幻觉检测的规范对齐版本': '## Gauge-Aligned SVD Hallucination Detection',
    '### 规范不对齐如何破坏SVD检测': '### How Gauge Misalignment Destroys SVD Detection',
    '### 规范对齐后的一致性检测': '### Consistency Detection After Gauge Alignment',
    '## 与ACE规范固定的统一': '## Unification with ACE Gauge Fixing',
    '### 共同结构：模块化组件 + 隐式规范群 + 后处理投影': '### Common Structure: Modular Components + Implicit Gauge Group + Post-hoc Projection',
    '### 深层原理': '### Deep Principle',
    '## 实验方案设计': '## Experimental Design',
    '## 讨论': '## Discussion',
    '## 工程路线图：从理论到实践的三条路径': '## Engineering Roadmap: Three Paths from Theory to Practice',
    '### 路一：路由修复（零训练、后处理）': '### Path 1: Router Repair (Zero Training, Post-hoc)',
    '### 路二：蒸馏 + Yajie 共识降噪（无需规范对齐）': '### Path 2: Distillation + Yajie Consensus Denoising (No Gauge Alignment Needed)',
    '### 路三：Gauge 对齐 + 表示级蒸馏': '### Path 3: Gauge Alignment + Representation-Level Distillation',
    '### 路径选择：决策树': '### Path Selection: Decision Tree',
    '### 实践者速查表 (Practitioner\'s Quick Reference)': '### Practitioner Quick Reference',
    '## 常见误解与澄清': '## Common Misconceptions and Clarifications',
    '### 诚实暴击：当前限制': '### Honest Critique: Current Limitations',
    '### 理论贡献总结': '### Summary of Theoretical Contributions',
    '### 开放问题': '### Open Questions',
    '### 更广泛的影响': '### Broader Implications',
}

# Apply section header fixes (these should work as they don't have backslash issues)
content = ''.join(lines)
for old, new in section_fixes.items():
    if old in content:
        content = content.replace(old, new)

# Write back
with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! Applied translations for lines 1-400 and section headers.')
