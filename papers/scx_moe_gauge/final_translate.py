# -*- coding: utf-8 -*-
"""Final translations for remaining Chinese lines in main.md"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

cjk = re.compile(r'[一-鿿]+')

translations = {}

# Read exact lines containing Chinese and build translation map
lines = content.split('\n')
cn_indices = [i for i, l in enumerate(lines) if cjk.search(l) and i != 10]  # skip abstract

for idx in cn_indices:
    line = lines[idx]

    # Build translations based on content patterns
    if '你分不清谱的平坦是因为模型在幻觉' in line:
        translations[line] = '> **Honest Strike:** This means: if you perform SVD detection without gauge fixing, you cannot tell whether the spectral flatness is due to the model hallucinating, or due to the "pseudo-dispersion" caused by expert gauge misalignment. Gauge alignment is a prerequisite for SVD detection.}'
    elif '更深远的是' in line:
        translations[line] = 'More profoundly, the "Modular Gauge Principle" implies that any model aggregation in federated learning, any voting in ensemble methods, any coordination in multi-agent systems -- all face their own versions of "potential surface misalignment." Identifying and resolving these gauge problems is a fundamental step toward building truly modular, composable AI systems.'
    elif '路由修复等价于在路由器的logits空间加一个专家特定的偏置' in line:
        translations[line] = '> **Remark:** Router repair is equivalent to adding an expert-specific bias in the router\'s logits space. This does not require modifying expert weights -- only adding a bias vector before the top-k selection. Implementation cost is zero.'
    elif '路一的局限性：它只修复路由' in line:
        translations[line] = '> **Honest Strike:** Limitation of Path 1: it only repairs the router -- it does not change the experts themselves. If the potential surface misalignment has already caused experts to learn suboptimal specialization patterns during training, repairing the router can only stop further losses, not recover already lost information.}'
    elif '模型的最终输出是规范不变的' in line:
        translations[line] = 'Key insight: **The model\'s final output is gauge-invariant.** Regardless of how much gauge offset exists inside each expert $E_m$, residual connections and subsequent Transformer layers absorb them layer by layer, so that the final softmax token probability distribution remains invariant under gauge transformations. Formally:'
    elif '[证明概要]' in line:
        translations[line] = '> **Proof:** [Proof Sketch]'
    elif '考虑第 ' in line and 'MoE子层后的残差流' in line:
        translations[line] = '> Consider the residual stream after the $\\ell$-th MoE sublayer:'
    elif 'LayerNorm 的归一化操作' in line:
        translations[line] = '> The response of LayerNorm\'s normalization operation $LN(x) = \\gamma \\odot (x - \\mu)/\\sigma + \\beta$ to translation $\\mathbf{g}_m$ is:'

# Apply
applied = 0
for old, new in translations.items():
    if old in content:
        content = content.replace(old, new)
        applied += 1

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)

remaining = len([l for l in content.split('\n') if cjk.search(l) and l[:20] != 'Mixture-of-Experts'])
print(f'Applied: {applied}')
print(f'Remaining: {remaining}')

cjk2 = re.compile(r'[一-鿿]+')
for i, l in enumerate(content.split('\n')):
    if cjk2.search(l) and i != 10 and i != 20:
        print(f'L{i+1}: {l[:100]}')
        if i > 30:
            break
