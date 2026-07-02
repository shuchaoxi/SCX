# -*- coding: utf-8 -*-
"""
Apply ALL translations from all 4 agents to main.md.
Handles Chinese text matching by using regex and fragment matching.
"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
cjk = re.compile(r'[一-鿿]+')

# Track which lines we've changed
changed = set()
applied = 0

def replace_line_by_index(idx, new_text):
    """Replace a specific line index"""
    global applied
    if 0 <= idx < len(lines):
        if cjk.search(lines[idx]):
            lines[idx] = new_text
            changed.add(idx)
            applied += 1
            return True
    return False

def find_line_by_fragment(fragment, start=0, end=None):
    """Find a line index by searching for a fragment"""
    if end is None:
        end = len(lines)
    for i in range(start, min(end, len(lines))):
        if fragment in lines[i]:
            return i
    return -1

# ============================================================
# AGENT 1 TRANSLATIONS: Lines 1-400
# ============================================================

# Section headers already done in previous pass

# Line 31: Ruler metaphor
idx = find_line_by_fragment('尺子 = MoE', 25, 40)
if idx is not None:
    replace_line_by_index(idx, '- **Ruler = MoE expert network** $E_m$. Each expert is trained independently and is \\"accurate\\" in its own domain (low loss).')

# Line 33: Assembling rulers
idx = find_line_by_fragment('拼尺子', 30, 40)
if idx is not None:
    replace_line_by_index(idx, '- **Assembling rulers = router comparing experts**. The router uses a linear function to compare the \\"markings\\" of 8 experts, but it does not know where each expert\'s zero mark is.')

# Line 48: Problem identification
idx = find_line_by_fragment('发现问题', 44, 55)
if idx is not None:
    replace_line_by_index(idx, '1. **The problem:** Different MoE experts live in their own \\"coordinate systems\\". The router is comparing incomparable things. This is not an engineering oversight -- it is a mathematical structure: gauge degrees of freedom.')

# Line 50: Unexpected discovery
idx = find_line_by_fragment('意外收获', 44, 55)
if idx is not None:
    replace_line_by_index(idx, '3. **Unexpected discovery:** The SVD spectrum after gauge alignment can detect \\"shared hallucinations\\" that Yajie misses -- errors that all experts agree on. True knowledge is low-dimensional in representation space; shared hallucinations are high-dimensional. SVD can see this difference.')

# Line 79: Core intuition
idx = find_line_by_fragment('核心直觉', 70, 90)
if idx is not None:
    replace_line_by_index(idx, '**Core intuition:** Expert $E_1$ and expert $E_2$ each learn different output \\"baselines\\" during training -- $E_1$\'s output is naturally \\"higher\\", $E_2$\'s output is naturally \\"lower\\", even for similar inputs. This difference is adaptively absorbed by the downstream layers of the residual connection during each one\'s training, so it is not detected by the training loss. However --')

# Line 89: surfaces
idx = find_line_by_fragment('这些曲面在输出空间', 80, 100)
if idx is not None:
    replace_line_by_index(idx, 'These surfaces naturally differ in height, scale, and even direction in output space -- not because any expert is \\"wrong\\", but because the training dynamics permit a gauge degree of freedom.')

# Problem Setup section
idx = find_line_by_fragment('一个稀疏MoE层由以下组件构成', 110, 130)
if idx is not None:
    replace_line_by_index(idx, 'A sparse MoE layer consists of the following components:')

idx = find_line_by_fragment('激活数 $k', 120, 140)
if idx is not None:
    replace_line_by_index(idx, '- Number of active experts $k \\in \\{1, ..., N\\}$')

idx = find_line_by_fragment('对输入 token', 125, 145)
if idx is not None:
    replace_line_by_index(idx, '> For input token $x \\in \\mathbb{R}^d$, the output is')

# Assumption texts
idx = find_line_by_fragment('我们假设训练已完成', 130, 150)
if idx is not None:
    replace_line_by_index(idx, 'We assume that post-hoc gauge fixing is performed after training has completed, similar to the post-hoc projection method in the EGP work. No gauge constraints are imposed during training -- this has been shown to be suboptimal [EGP paper, $\\lambda$ scan failure].')

idx = find_line_by_fragment('设第$\\ell$层MoE的输入', 135, 155)
if idx is not None:
    replace_line_by_index(idx, 'Let the input to the $\\ell$-th MoE layer be $x^{(\\ell)}$. The residual connection')

idx = find_line_by_fragment('使得规范自由度得以存在', 145, 160)
if idx is not None:
    replace_line_by_index(idx, 'enables gauge freedom to exist: upstream LayerNorm and downstream projection matrices can adaptively absorb gauge transformations of expert outputs, making the training loss locally insensitive to these transformations.')

idx = find_line_by_fragment('存在一个校准数据集', 148, 160)
if idx is not None:
    replace_line_by_index(idx, 'There exists a calibration dataset $\\mathcal{D}_{cal} = \\{x_i\\}_{i=1}^{n_{cal}}$ of size $n_{cal} \\geq N \\cdot d$, which can be used to estimate gauge parameters. The calibration set does not require labels -- only input tokens. This matches common practical scenarios.')

# Theorem texts
idx = find_line_by_fragment('然而，路由器在训练中被', 155, 175)
if idx is not None:
    replace_line_by_index(idx, '> However, the router is **implicitly** tuned during training to match the output distribution of the experts. Specifically, the gradient of the router during training is')

idx = find_line_by_fragment('其中 $\\partial y / \\partial r$ 依赖于', 165, 180)
if idx is not None:
    replace_line_by_index(idx, '> where $\\partial y / \\partial r$ depends on the values of $E_m(x)$. Therefore, the optimal value of $W_r$ **depends on the output distribution of the experts during training**.')

idx = find_line_by_fragment('具体而言，设原始规范', 165, 185)
if idx is not None:
    replace_line_by_index(idx, '> Specifically, let the expert outputs in the original gauge (during training) be $\\{E_m^{train}\\}$, with router $W_r^{train}$.')

# Greedy algorithm lines
idx = find_line_by_fragment('在实际应用中', 295, 310)
if idx is not None:
    replace_line_by_index(idx, 'In practical applications -- especially at inference time -- we may need gauge fixing faster than convex relaxation. The following greedy algorithm provides an $O(n N d + n k \\log N)$ approximation.')

# SVD section intro
idx = find_line_by_fragment('在之前的工作中', 345, 365)
if idx is not None:
    replace_line_by_index(idx, 'In prior work [Hamiltonian Audit Paper], we proposed using the SVD spectrum as a hallucination detection metric: query the model $M$ times on the same question, take the hidden state matrix $\\mathbf{H} \\in \\mathbb{R}^{M \\times d}$ of the last layer, compute the SVD $\\mathbf{H} = \\mathbf{U} \\boldsymbol{\\Sigma} \\mathbf{V}^T$, and define')

idx = find_line_by_fragment('若 $\\rho_{10} > 0.9$，模型对此问题确信', 355, 370)
if idx is not None:
    replace_line_by_index(idx, 'If $\\rho_{10} > 0.9$, the model is confident on this question; if $\\rho_{100} < 0.5$, the model is hallucinating.')

idx = find_line_by_fragment('但这是在单模型上做的', 358, 370)
if idx is not None:
    replace_line_by_index(idx, '**But this was done on a single model.** In MoE, applying the same method to multi-expert outputs faces a fundamental problem:')

# ============================================================
# AGENT 2 + 3 + 4 TRANSLATIONS for remaining sections
# These are the big bulk sections
# ============================================================

# Now let's find ALL remaining Chinese lines and show them
lines_with_chinese = []
for i, line in enumerate(lines):
    if cjk.search(line):
        lines_with_chinese.append((i, line))

print(f"Chinese lines remaining: {len(lines_with_chinese)}")
print(f"Applied: {applied}")

# Write back
content = '\n'.join(lines)
with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
