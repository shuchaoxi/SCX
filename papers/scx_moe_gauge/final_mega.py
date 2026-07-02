# -*- coding: utf-8 -*-
"""
FINAL comprehensive translation: reads main.md, translates ALL remaining Chinese.
"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
cjk = re.compile(r'[一-鿿]+')

# Build translation map by reading each Chinese line and providing English
# Key: EXACT line content from the file
# Value: English replacement

def make_translation_map():
    """Read Chinese lines and build translation map"""
    trans = {}
    cn_lines = [(i, l) for i, l in enumerate(lines) if cjk.search(l) and 'Mixture-of-Experts' not in l[:30]]

    for idx, line in cn_lines:
        english = None

        # === SVD section (line ~781) ===
        if '你分不清谱的平坦是因为模型在幻觉' in line:
            english = '> **Honest Strike:** This means: if you perform SVD detection without gauge fixing, you cannot tell whether the spectral flatness is due to the model hallucinating, or due to the "pseudo-dispersion" caused by expert gauge misalignment. Gauge alignment is a prerequisite for SVD detection.}'

        # === Discussion section (line ~1091-1113) ===
        elif line.strip() == '> **诚实暴击:**':
            english = '> **Honest Critique:**'
        elif '本工作的三个主要限制' in line:
            english = 'Three main limitations of this work:'
        elif '更深远的是' in line and '模块化规范原理' in line:
            english = 'More profoundly, the "Modular Gauge Principle" implies that any model aggregation in federated learning, any voting in ensemble methods, any coordination in multi-agent systems -- all face their own versions of "potential surface misalignment." Identifying and resolving these gauge problems is a fundamental step toward building truly modular, composable AI systems.'

        # === Engineering Roadmap (lines ~1159-1220) ===
        elif '**校准。**' in line and '无标签校准集' in line:
            english = '1. **Calibration.** Run the MoE model on an unlabeled calibration set $\\mathcal{D}_{cal}$, collecting expert outputs $\\{E_m^{(\\ell)}(x_i)\\}$ for each MoE sublayer'
        elif '**Gauge 固定。**' in line:
            english = '2. **Gauge fixing.** Compute gauge parameters $\\{\\hat{\\mathbf{g}}_m^{(\\ell)}\\}$ using the greedy algorithm (Algorithm [ref])'
        elif '**路由替换。**' in line:
            english = '3. **Router replacement.** At inference time, for each MoE layer:'
        elif '**验证。**' in line:
            english = '4. **Validation.** Compare the downstream task performance of the original and repaired routers on the test set'
        elif 'Remark:' in line and '路由修复等价于' in line:
            english = '> **Remark:** Router repair is equivalent to adding an expert-specific bias in the router\'s logits space. This does not require modifying expert weights -- only adding a bias vector before the top-k selection. Implementation cost is zero.'
        elif '数学保证：' in line:
            english = '**Mathematical guarantee:** By Theorem [ref], the original router has a suboptimality bound $L_r \\cdot \\max_m \\|\\mathbf{g}_m\\|$ under gauge transformations. The gauge-fixed router eliminates this suboptimality down to a residual $O(\\text{Tr}(\\Sigma)/n)$ (Theorem [ref]).'
        elif '路一的局限性' in line:
            english = '> **Honest Strike:** Limitation of Path 1: it only repairs the router -- it does not change the experts themselves. If the potential surface misalignment has already caused experts to learn suboptimal specialization patterns during training, repairing the router can only stop further losses, not recover already lost information.}'
        elif '不碰专家内部表示' in line:
            english = '**Core idea:** Do not touch the internal representations of experts; operate in the gauge-invariant final output space. Use MoE as a teacher and Yajie multi-expert consensus as a data quality filter to train a smaller, cleaner student model.'
        elif '为什么不需要规范对齐' in line:
            english = '**Why is gauge alignment unnecessary?**'
        elif '模型的最终输出是规范不变的' in line:
            english = 'Key insight: **The model\'s final output is gauge-invariant.** Regardless of how much gauge offset exists inside each expert $E_m$, residual connections and subsequent Transformer layers absorb them layer by layer, so that the final softmax token probability distribution remains invariant under gauge transformations. Formally:'
        elif '对任意规范变换' in line and 'LayerNorm' in line:
            english = '> For any gauge transformation $\\{E_m \\to E_m + \\mathbf{g}_m\\}$, there exists an adaptive adjustment of LayerNorm parameters such that the Transformer\'s final output logits $\\mathbf{z}^{(L)}$ and softmax probabilities $\\text{softmax}(\\mathbf{z}^{(L)})$ are invariant under gauge transformations -- up to a small perturbation of $O(\\|\\mathbf{g}\\|_\\infty / \\sqrt{d})$, which is suppressed by the contractive property of residual connections for model depth $L \\geq 2$.'
        elif '证明概要' in line:
            english = '> **Proof:** [Proof Sketch]'
        elif 'MoE子层后的残差流' in line:
            english = '> Consider the residual stream after the $\\ell$-th MoE sublayer:'
        elif 'LayerNorm 的归一化操作' in line:
            english = '> The response of LayerNorm\'s normalization operation $LN(x) = \\gamma \\odot (x - \\mu)/\\sigma + \\beta$ to translation $\\mathbf{g}_m$ is:'

        # === FAQ section (lines ~1640-1660) ===
        elif '两者可以结合：先用 Git Re-Basin' in line:
            english = 'The two can be combined: first use Git Re-Basin to resolve permutation symmetry in weight space, then use this work\'s method to fix the gauge in representation space, then use Path 1 or Path 3 methods to improve routing or distillation. This is a sub-direction of open problem O4 (cross-architecture gauge).'
        elif '这是作者最不关心的问题' in line:
            english = '**Short answer:** This is the question the author cares about least. Theorems do not need reviewers to "understand" them -- they need to be **checked**. The definition of the gauge group (Definition [ref]) is precise. The proofs of the theorems are self-contained. If a reviewer finds a mathematical error, that is something the author needs to fix. If a reviewer is merely "unaccustomed" to the language of gauge theory -- that is the inevitable cost of interdisciplinary work. ACE gauge fixing has already been verified for physical correctness on real material systems; MoE gauge fixing is a generalization of the same principle. Time will judge whether it is correct.'

        # === Equality Principle section (lines ~1669-1770) ===
        elif '以上定理构成了一个完整的工程框架' in line:
            english = 'The above theorems constitute a complete engineering framework. But the significance of potential surface misalignment goes beyond engineering. This section elaborates its **epistemological implications** -- why this mathematical fact changes our understanding of "knowledge," "consensus," and "comparison."'
        elif '本工作的 11 条定理中，任何单条都可以被未来的工作改进' in line:
            english = 'Among the 11 theorems of this work, any single one can be improved, superseded, or discarded by future work. MILP can be replaced by better optimization algorithms. The error bounds of greedy approximation can be tightened. The thresholds for SVD detection can be calibrated by experiments.'
        elif '但有一个东西不会过时' in line:
            english = 'But there is one thing that will not become outdated:'
        elif '平等论 (The Equality Principle)' in line:
            english = '**The Equality Principle**'
        elif '同一个系统内的不同观察者' in line:
            english = '**Different observers within the same system, even when receiving the same training objective and achieving the same training loss, will develop incomparable internal representations.**'
        elif '一致性不是天然的' in line:
            english = '**Consistency is not natural -- it must be explicitly constructed. The mathematical legitimacy of comparison is not granted by default -- it must be conferred by gauge fixing.**'
        elif '这不是一条定理' in line:
            english = 'This is not a theorem. It is a **principle** distilled from Theorems 1-11. The theorems are its corollaries, the algorithms are its implementations, and the experiments are its verification.'
        elif '我们称这个原理为**平等论**' in line:
            english = 'We call this principle **The Equality Principle**. "Equality" has three layers of meaning here:'
        elif '坐标系的平等' in line:
            english = '1. **Equality of coordinate systems.** No expert\'s coordinate system is a privileged coordinate system. All gauge choices are equivalent under the training loss -- there is no "correct" zero-point, no "natural" output scale. Equality means no expert is inherently more "standard."'
        elif '知识生产的平等' in line:
            english = '2. **Equality of knowledge production.** Knowledge (a proposition being judged as "true") cannot be produced by a single observer -- the Honest Person Theorem (SCX Theorem 3) has proved that a single observer cannot distinguish noise, bias, learnability difficulty, and honest error. But multiple observers also **do not automatically** solve the problem -- The Equality Principle supplies the missing half: the measurement tools of multiple observers are not in the same coordinate system, and comparison is mathematically undefined. Knowledge requires **joint verification by multiple independent observers whose gauges have been aligned.**'
        elif '对齐作为先决条件' in line:
            english = '3. **Alignment as a prerequisite.** Equality is not the endpoint -- it is the starting point. Only after acknowledging that all observers are in equal (and incomparable) coordinate systems will we begin to **construct** alignment. Gauge fixing does not break equality -- it **constructs comparability under the premise of equality.**'
        elif 'SCX 理论体系已建立了一条完整的认识论链' in line:
            english = 'The SCX theoretical system has established a complete epistemological chain. The Equality Principle is the newest link in it:'
        elif '知识生产的五阶段条件' in line:
            english = '**Five-Stage Conditions for Knowledge Production**'

        if english:
            trans[line] = english

    return trans

trans_map = make_translation_map()

# Apply
applied = 0
for old, new in trans_map.items():
    if old in content:
        content = content.replace(old, new)
        applied += 1

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)

remaining_lines = [l for l in content.split('\n') if cjk.search(l) and 'Mixture-of-Experts' not in l[:30]]
print(f'Applied: {applied}')
print(f'Remaining: {len(remaining_lines)}')
if remaining_lines:
    for l in remaining_lines[:10]:
        print(f'  {l[:100]}')
