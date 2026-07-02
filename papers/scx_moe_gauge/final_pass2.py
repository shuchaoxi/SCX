# -*- coding: utf-8 -*-
"""
FINAL translation pass for main.md.
Processes each remaining Chinese line and replaces with English.
Uses exact line content matching from the saved JSON file.
"""
import re, json

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
cjk = re.compile(r'[一-鿿]+')

# Dictionary mapping: exact Chinese line -> English replacement
translations = {}

# ============================================================
# Read remaining Chinese lines and build translations
# ============================================================

def add_translation(fragment, english):
    """Add translation for any line containing the fragment"""
    translations[fragment] = english

# ============================================================
# TECHNICAL SECTIONS (easier fragments)
# ============================================================

add_translation('1. 在$n_{cal}=5000$的校准集上，用算法', '1. On a calibration set of size $n_{cal}=5000$, compute gauge parameters $\\{\\hat{\\mathbf{g}}_m\\}$ using Algorithm [ref]')
add_translation('2. 在测试集上：', '2. On the test set:')
add_translation('3. 指标：', '3. Metrics:')
add_translation('1. 构建评估集：', '1. Construct evaluation set:')
add_translation('2. 对每个问题：', '2. For each question:')
add_translation('3. 比较两种模式：', '3. Compare two modes:')
add_translation('4. 指标：AUROC', '4. Metrics: AUROC (ability to distinguish high/low hallucination questions), precision-recall curve')
add_translation('**预期**：模式B的AUROC应显著高于模式A', '**Expected:** Mode B should have significantly higher AUROC than Mode A ($\\Delta AUROC > 0.1$), because gauge fixing eliminates "pseudo-dispersion" -- spectral flatness caused by gauge misalignment being misinterpreted as hallucination.')
add_translation('**目标**：比较精确MILP求解器', '**Goal:** Compare gauge fixing quality between exact MILP solvers (CPLEX/Gurobi) and the greedy algorithm [ref].')
add_translation('1. 在小规模合成MoE', '1. Apply known gauge transformations on a small-scale synthetic MoE ($N=4$, $d=64$)')
add_translation('2. 分别用MILP求解器', '2. Recover gauge parameters using the MILP solver (via SCIP) and the greedy algorithm respectively')
add_translation('3. 指标：恢复误差', '3. Metrics: recovery error $\\frac{1}{N}\\sum_m \\|\\hat{\\mathbf{g}}_m - \\mathbf{g}_m^{true}\\|$, runtime')
add_translation('4. 在$n \\in', '4. Sweep over $n \\in \\{100, 500, 1000, 5000\\}$')
add_translation('**预期**：MILP在$n$较小时有优势', '**Expected:** MILP has an advantage when $n$ is small (more precise use of discrete structure); when $n > 1000$, the greedy algorithm approaches MILP quality (Theorem [ref]) but is $O(n \\log N)$ times faster.')

# Discussion
add_translation('本工作将规范理论(Gauge Theory)', 'This work applies gauge theory -- the core tool in physics for describing redundant representations of degrees of freedom -- to modern deep learning architectures. We identify a previously overlooked gauge degree of freedom in MoE, which causes different experts\' outputs to live in incomparable coordinate systems, thereby undermining the mathematical foundation of routing decisions.')
add_translation('与ACE规范固定的连接表明，这不是一个孤立现象', 'The connection with ACE gauge fixing shows that this is not an isolated phenomenon but a manifestation of a universal principle: the **Modular Gauge Principle**. Any system composed of independently trained components -- regardless of its specific architecture -- must explicitly fix the gauge before comparing component outputs.')
add_translation('1. **非线性规范群。** 我们目前考虑了平移、旋转和缩放。在具有非线性激活函数的深层网络中，规范群可能比阿贝尔群更丰富——包括局部微分同胚不变性。这种更丰富的规范结构是否能被利用以改进路由？',
    '1. **Nonlinear gauge groups.** We have currently considered translation, rotation, and scaling. In deep networks with nonlinear activation functions, the gauge group may be richer than Abelian groups -- including local diffeomorphism invariance. Can this richer gauge structure be exploited to improve routing?')
add_translation('2. **端到端规范感知训练。** 本工作（与EGP工作一致）采用后处理规范固定。是否可能在训练过程中施加软规范约束——尽管EGP中$\\lambda$扫描显示后处理优于软约束——通过改进的正则化方案实现端到端规范感知？',
    '2. **End-to-end gauge-aware training.** This work (consistent with EGP work) adopts post-hoc gauge fixing. Is it possible to impose soft gauge constraints during training -- although EGP\'s $\\lambda$ scan showed post-processing outperforms soft constraints -- to achieve end-to-end gauge awareness through improved regularization schemes?')
add_translation('3. **规范固定与模型压缩。** 规范固定后，对齐的专家输出在低维子空间中的集中度更高。这是否意味着可以通过在规范固定子空间中进行低秩投影来压缩MoE模型？',
    '3. **Gauge fixing and model compression.** After gauge fixing, aligned expert outputs are more concentrated in a low-dimensional subspace. Does this mean MoE models can be compressed via low-rank projection in the gauge-fixed subspace?')
add_translation('4. **跨架构规范。** ACE的规范群（系数空间的平移）和MoE的规范群（表示空间的平移）是否存在一个共同的数学结构——可能是某种纤维丛(fiber bundle)结构——使得不同架构的规范固定方法可以统一？',
    '4. **Cross-architecture gauge.** Is there a common mathematical structure between ACE\'s gauge group (translation in coefficient space) and MoE\'s gauge group (translation in representation space) -- perhaps some fiber bundle structure -- that could unify gauge fixing methods across different architectures?')
add_translation('5. **规范群的结构与模型容量。** 规范群的大小是否与模型的过参数化程度相关？更宽/更深的网络是否具有更大的规范群——这是否可以作为一个正则化信号？',
    '5. **Gauge group structure and model capacity.** Is the size of the gauge group related to the degree of model overparameterization? Do wider/deeper networks have larger gauge groups -- and can this serve as a regularization signal?')
add_translation('> **诚实暴击:** 本工作的三个主要限制：', '> **Honest Critique:** Three main limitations of this work:')
add_translation('1. **实验验证缺失。** 所有实验方案设计在第 [ref]节中，但尚未执行。定理虽已严格证明，但实验证据是科学主张成立的另一半。',
    '1. **Lack of experimental validation.** All experimental protocols are designed in Section [ref], but have not yet been executed. Although the theorems are rigorously proven, experimental evidence is the other half of what makes a scientific claim valid.')
add_translation('2. **规范群的不完全刻画。** 我们识别了平移、旋转和缩放的规范自由，但深度网络中的实际规范群可能更复杂。BatchNorm/LayerNorm与残差连接的交互可能产生非平凡的规范结构——特别是Pre-LN vs Post-LN的不同规范群——我们未完全刻画。',
    '2. **Incomplete characterization of the gauge group.** We have identified translation, rotation, and scaling gauge freedoms, but the actual gauge group in deep networks may be more complex. The interaction between BatchNorm/LayerNorm and residual connections may produce nontrivial gauge structures -- particularly the different gauge groups of Pre-LN vs. Post-LN -- which we have not fully characterized.')
add_translation('3. **校准集选择偏差。** 规范固定依赖于校准集', '3. **Calibration set selection bias.** Gauge fixing depends on the calibration set $\\mathcal{D}_{cal}$. If the inference distribution differs from the calibration distribution (distribution shift), gauge fixing may introduce systematic bias. This is effectively a "meta-gauge degree of freedom" of the gauge fixing problem itself -- the choice of calibration set.')
add_translation('如果本工作的主张成立——MoE路由器在比较不可比的专家输出', 'If the claims of this work hold -- that MoE routers compare incomparable expert outputs -- then all deployed MoE models (Mixtral, DeepSeek-V2/V3, Grok, etc.) may have systematic routing bias. This is not to say these models are broken -- residual connections and subsequent layer adaptation mitigate part of the problem -- but rather that their routing decisions can be improved after gauge alignment.')
add_translation('更深远的是，"模块化规范原理"暗示：任何联邦学习中的模型聚合', 'More profoundly, the "Modular Gauge Principle" implies: any model aggregation in federated learning, any voting in ensemble methods, any coordination in multi-agent systems -- all face their own versions of "misaligned potential surfaces." Identifying and resolving these gauge problems is a fundamental step toward building truly modular and composable AI systems.')

# ============================================================
# ENGINEERING ROADMAP
# ============================================================
add_translation('前文从理论上建立了规范不对齐的诊断和修复框架。本节将理论落地', 'The preceding sections have theoretically established a framework for diagnosing and fixing gauge misalignment. This section brings theory to practice: **Given a trained MoE large model, what can users do with gauge analysis?** We propose three progressive engineering paths -- from lossless router replacement, to distillation denoising without gauge alignment, to precise distillation using intermediate-layer representations.')
add_translation('三条路径在处理深度和是否需要规范对齐上存在根本差异', 'The three paths differ fundamentally in processing depth and whether gauge alignment is required:')
add_translation('**核心思想：** 不对模型权重做任何修改，仅在推理时用规范固定后的路由决策替换原始路由器。',
    '**Core idea:** Do not modify any model weights; only replace the original router with gauge-fixed routing decisions at inference time.')
add_translation('**操作流程：**', '**Procedure:**')

# Add more as needed...

# Now apply translations: for each fragment, find ALL lines containing it and replace
applied = 0
for fragment, english in translations.items():
    for i, line in enumerate(lines):
        if fragment in line and cjk.search(line):
            lines[i] = english
            applied += 1

content = '\n'.join(lines)
with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)

remaining = len([l for l in lines if cjk.search(l)])
print(f"Applied: {applied} translations")
print(f"Remaining Chinese lines: {remaining}")
print("Done")
