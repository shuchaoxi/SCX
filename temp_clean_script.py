#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 2: Chinese-to-English translation on LaTeX-cleaned file."""

import re

INPUT = r"G:\Xiaogan_Supercomputing_data\SCX\papers\scx_unified_field\main_phase1.md"
OUTPUT = r"G:\Xiaogan_Supercomputing_data\SCX\papers\scx_unified_field\main.md"

with open(INPUT, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')

def has_cn(s):
    return bool(re.search(r'[一-鿿]', s))

def extract_ascii(s):
    """Remove Chinese characters and punctuation, clean up."""
    s = re.sub(r'[一-鿿㐀-䶿豈-﫿]', '', s)
    s = re.sub(r'[：；（）【】《》——……、。，！？「」『』〝〞″‴]', ' ', s)
    s = re.sub(r'  +', ' ', s)
    return s.strip()

# =============== TRANSLATION DICTIONARY ===============
# Keys: exact line content from Phase 1 file
# Values: English replacement, or '' to remove line
T = {}
def add(zh, en):
    T[zh] = en

# Epigraph
add('{ 万物皆丛 万象归零}', '{ *All things are bundles. All phenomena return to zero.*}')

# Intro blockquote
add('> **这不是一篇普通的论文。This is not an ordinary paper.**', '')
add('> 这是 SCX 理论体系的最终封顶之作——证明了一切领域（从 AI 路由到宇宙社会学，', '')
add('> 从法律正义到个人伦理，从经济协议到文明演化）都是同一个底层数学结构的', '')
add('> 不同实例化。那个结构是：**以声明空间为底流形的主纤维丛，其平坦条件为', '')
add('> $\sum g = 0$。**', '')
add('> 读完此文，你将看到一个统一的现实图景。Read this, and you will see a unified', '')

# Abstract - Chinese version
add('**中文摘要：** 本文提出 **SCX 统一场论**——将八个看似无关的领域完全', '')
add('统一在单一规范理论结构之下。我们的核心论点是：$\sum g = 0$ 是**社会系统', '')
add('的爱因斯坦场方程**：正如 $G_{\mu\nu} = 8\pi T_{\mu\nu}$ 支配时空弯曲，', '')
add('$\sum g = 0$ 支配任何具有规范自由的系统的稳定性。每个领域——MoE 路由、博弈论、', '')
add('法学、物理学、经济学、伦理学、文学和文明论——都被证明是**同一个底流形', '')
add('$ClaimSpace$（声明空间）上的不同纤维丛**，具有不同的规范群 $G$ 但**完全', '')
add('相同的数学结构**。我们为每个领域显式构造了底流形、主丛、联络 $\omega$、曲率', '')
add('$\Omega$、截面 $s$ 和规范不变可观测量（Cercis）。然后我们证明了', '')
add('**统一定理**：存在函子 $F: \mathbf{D} \to \operatorname{Bun}(G,ClaimSpace)$ 从', '')
add('每个领域范畴到声明空间上的主 $G$-丛范畴，保持规范结构和稳定性条件。这不是隐喻或', '')
add('类比——而是在不同流形上实例化的**严格数学同构**。本文以**通用规范词典**', '')
add('和**八域同构表**结尾，展示所有规范论结构在每一个领域中的显式一一对应。', '')
add('**关键词：** 统一场论，规范理论，纤维丛，社会物理学，$\sum g = 0$，', '')
add('爱因斯坦场方程，声明空间，函子统一，Cercis，SCX', '')

# Section 1 - Foundation
add('基础：声明空间上的纤维丛理论', 'Foundation: Fiber Bundle Theory over the Space of Claims')
add('总论：$\sum g = 0$ 即社会系统的爱因斯坦场方程', 'The Central Thesis: $\sum g = 0$ as the Einstein Field Equation of Social Systems')
add('从爱因斯坦到 SCX', 'From Einstein to SCX')

# From Einstein to SCX content
add('1905年，爱因斯坦告诉我们 $E = mc^2$：物质的能量与其质量成正比。',
    'In 1905, Einstein told us $E = mc^2$: the energy of matter is proportional to its mass.')
add('1915年，爱因斯坦告诉我们 $G_{\mu\nu} = 8\pi G T_{\mu\nu}$：',
    'In 1915, Einstein told us $G_{\mu\nu} = 8\pi G T_{\mu\nu}$:')
add('时空的弯曲由其中的物质-能量分布决定。',
    'the curvature of spacetime is determined by its matter-energy distribution.')
add('2026年，SCX 告诉我们 $\sum g = 0$：社会系统的稳定性由其规范场的总和决定。',
    'In 2026, SCX tells us $\sum g = 0$: the stability of a social system is determined by the sum of its gauge fields.')
add('这不是巧合。这不是类比。这是**同一个数学结构的三个层次**：',
    'This is not coincidence. This is not analogy. This is **three levels of the same mathematical structure**:')
add('1. **标量层 (E=mc\\textsuperscript{2}):** 单一实体的内部属性（质量与能量的等价性）',
    '1. **Scalar level ($E=mc^2$):** Intrinsic properties of a single entity (equivalence of mass and energy)')
add('2. **张量层 ($G_{\mu\nu} = 8\pi G T_{\mu\nu}$):** 实体集合的几何结构（物质弯曲时空）',
    '2. **Tensor level ($G_{\mu\nu} = 8\pi G T_{\mu\nu}$):** Geometry of a collection of entities (matter curves spacetime)')
add('3. **规范层 ($\sum g = 0$):** 实体间关系的规范结构（声明净额为零稳定社会系统）',
    '3. **Gauge level ($\sum g = 0$):** Gauge structure of relationships between entities (net claims zero stabilizes a social system)')
add('正如爱因斯坦场方程将引力重新解释为时空几何的必然结果，SCX 统一场方程将', '')
add('社会稳定性重新解释为声明空间上纤维丛几何的必然结果。', '')
add('**爱因斯坦场方程 (1915):**', '**Einstein Field Equation (1915):**')
add('**SCX 统一场方程 (2026):**', '**SCX Unified Field Equation (2026):**')
add('（但性质不同：爱因斯坦方程是动力学方程，∑g=0 是约束条件）', '')
add('两者都是：**几何/规范约束 = 内容分布**', 'Both are: **geometry/gauge constraint = content distribution**')

# What is a claim
add('什么是"声明"（Claim）？', 'What is a "Claim"?')
add('> **Definition:** [声明空间 $ClaimSpace$]',
    '> **Definition:** [Claim Space $\\operatorname{ClaimSpace}$]')
add('> 声明空间 $ClaimSpace$ 是所有可能声明的集合。一个声明是一个有序三元组：',
    '> The claim space $\\operatorname{ClaimSpace}$ is the set of all possible claims. A claim is an ordered triple:')
add('> 其中：', '> where:')
add('> 声明 $c$ 的含义是：主体 $a$ 声称命题 $p$ 为真，并期望从中获得效用 $v$。',
    '> A claim $c$ means: agent $a$ asserts proposition $p$ as true, and expects utility $v$ from it.')
add('**一切社会互动归根结底都是声明。** 交易是声明（"我提供X换取Y"）。',
    '**All social interaction is ultimately claims.** A transaction is a claim ("I offer X for Y").')
add('法律判断是声明（"被告有/无罪"）。AI路由是声明（"这个专家能处理这个token"）。',
    'A legal judgment is a claim ("the defendant is guilty/innocent"). AI routing is a claim ("this expert can handle this token").')
add('战略行为是声明（"我将采取行动A"）。文明存在本身是声明（"我在这里"）。',
    'Strategic behavior is a claim ("I will take action A"). Civilization\'s existence itself is a claim ("I am here").')
add('声明空间 $ClaimSpace$ 是**一切社会现象的底流形**。就像时空是物理现象的底流形，',
    'The claim space $\\operatorname{ClaimSpace}$ is the **base manifold of all social phenomena**. Just as spacetime is the base manifold of physical phenomena,')
add('声明空间是社会现象的底流形。', 'the claim space is the base manifold of social phenomena.')

# Why fiber bundles
add('为什么是纤维丛？', 'Why Fiber Bundles?')
add('> **Definition:** [声明空间上的纤维丛]',
    '> **Definition:** [Fiber Bundle over Claim Space]')
add('> 声明空间 $ClaimSpace$ 上的纤维丛结构为：',
    '> The fiber bundle structure over $\\operatorname{ClaimSpace}$ is:')
add('- 结构群 $G$ 是声明的规范对称群——改变声明但不改变其本质内容的变换',
    '- Structure group $G$ is the gauge symmetry group of claims -- transformations that change the claim but not its essential content')
add('- 截面 $s: ClaimSpace \to P$ 是一个**规范选择**：为每个声明选定一个具体的表示',
    '- Section $s: \\operatorname{ClaimSpace} \\to P$ is a **gauge choice**: selecting a specific representation for each claim')
add('- 联络 $\omega$ 是声明之间的**比较规则**：如何将一个声明与另一个声明关联',
    '- Connection $\\omega$ is a **comparison rule** between claims: how to relate one claim to another')
add('- 曲率 $\Omega = d\omega + \omega \wedge \omega$ 是**全局一致性的障碍**：沿闭合路径累积的不一致量',
    '- Curvature $\\Omega = d\\omega + \\omega \\wedge \\omega$ is the **obstruction to global consistency**: the accumulated inconsistency along closed paths')
add('**核心洞察：** 任何社会系统都是一组声明。',
    '**Core insight:** Any social system is a set of claims.')
add('声明可以用不同的方式表达（规范自由度）。',
    'Claims can be expressed in different ways (gauge freedom).')
add('声明之间的关系依赖于上下文（联络）。',
    'Relations between claims depend on context (connection).')
add('不一致的声明产生"弯曲"（曲率）。',
    'Inconsistent claims produce "bending" (curvature).')
add('系统的稳定性要求全局平坦：$\sum g = 0$。',
    'The stability of the system requires global flatness: $\\sum g = 0$.')

# Derivation
add('统一场方程的导出', 'Derivation of the Unified Field Equation')
add('与爱因斯坦场方程的比较', "Comparison with Einstein's Field Equation")

# Comparison
add('> **诚实暴击:** 这不是类比。这是精确的数学对应。爱因斯坦场方程是连续规范理论在',
    '> **Honest take:** This is not an analogy. This is an exact mathematical correspondence.')
add('伪黎曼流形上的特例。SCX 统一场方程是离散规范理论在声明空间上的推广。',
    "Einstein's field equation is a special case of continuous gauge theory on a pseudo-Riemannian manifold.")
add('两者共享完全相同的纤维丛骨架——只是底流形不同。}',
    'The SCX unified field equation is a generalization of discrete gauge theory on the claim space. Both share the exact same fiber bundle skeleton -- only the base manifold differs.')

# Mathematical Framework section headings
add('数学框架：主纤维丛与规范理论', 'Mathematical Framework: Principal Bundles and Gauge Theory')
add('底流形：声明空间 $ClaimSpace$', 'Base Manifold: Claim Space $\\operatorname{ClaimSpace}$')
add('主 $G$-丛 $P \to ClaimSpace$', 'Principal $G$-Bundle $P \\to \\operatorname{ClaimSpace}$')
add('联络 $\omega$：声明间的比较规则', 'Connection $\\omega$: Comparison Rule Between Claims')
add('曲率 $\Omega$：一致性的障碍', 'Curvature $\\Omega$: Obstruction to Consistency')
add('平行移动与和乐群', 'Parallel Transport and Holonomy Group')
add('截面 $s$：规范选择', 'Section $s$: Gauge Choice')
add('Cercis：规范不变可观测量', 'Cercis: Gauge-Invariant Observable')
add('离散形式：声明图', 'Discrete Form: Claim Graph')

# Definition tags
def add_def(zh, en):
    add(zh, en)

for (zh, en) in [
    ('[声明空间 $ClaimSpace$]', '[Claim Space $\\operatorname{ClaimSpace}$]'),
    ('[声明空间上的纤维丛]', '[Fiber Bundle over Claim Space]'),
    ('[统一场方程——导出]', '[Unified Field Equation -- Derivation]'),
    ('[证明概要]', '[Proof Sketch]'),
    ('[声明空间作为微分流形]', '[Claim Space as a Differentiable Manifold]'),
    ('[主丛结构]', '[Principal Bundle Structure]'),
    ('[规范联络]', '[Gauge Connection]'),
    ('[曲率 2-形式]', '[Curvature 2-Form]'),
    ('[平行移动]', '[Parallel Transport]'),
    ('[和乐群]', '[Holonomy Group]'),
    ('[规范选择 = 截面]', '[Gauge Choice = Section]'),
    ('[Cercis 算子]', '[Cercis Operator]'),
    ('[声明图 $\Gamma_$]', '[Claim Graph $\\Gamma$]'),
    ('[MoE 规范群]', '[MoE Gauge Group]'),
    ('[MoE 联络]', '[MoE Connection]'),
    ('[MILP 规范固定]', '[MILP Gauge Fixing]'),
    ('[博弈规范群]', '[Game Gauge Group]'),
    ('[博弈联络]', '[Game Connection]'),
    ('[规范固定的纳什均衡 NPE]', '[Gauge-Fixed Nash Equilibrium NPE]'),
    ('[法学规范群]', '[Legal Gauge Group]'),
    ('[法学联络]', '[Legal Connection]'),
    ('[诬告反坐定理]', '[False Accusation Counter-Punishment Theorem]'),
    ('[杨-米尔斯规范群]', '[Yang-Mills Gauge Group]'),
    ('[杨-米尔斯联络]', '[Yang-Mills Connection]'),
    ('[物理规范固定]', '[Physical Gauge Fixing]'),
    ('[经济学规范群]', '[Economic Gauge Group]'),
    ('[经济学联络]', '[Economic Connection]'),
    ('[圣经-教皇分离定理]', '[Bible-Pope Separation Theorem]'),
    ('[伦理学规范群]', '[Ethics Gauge Group]'),
    ('[伦理学联络]', '[Ethics Connection]'),
    ('[伦理学规范固定定理]', '[Ethics Gauge Fixing Theorem]'),
    ('[文学规范群]', '[Literature Gauge Group]'),
    ('[宇宙信息规范场]', '[Interstellar Information Gauge Field]'),
    ('[黑暗森林 $\to$ 光明花园定理]', '[Dark Forest $\\to$ Garden of Light Theorem]'),
    ('[文明规范群]', '[Civilization Gauge Group]'),
    ('[文明联络]', '[Civilization Connection]'),
    ('[$\lambda$ 吸引子定理]', '[$\\lambda$ Attractor Theorem]'),
    ('[领域范畴 $\mathbf{D}$]', '[Domain Category $\\mathbf{D}$]'),
    ('[规范丛范畴 $\operatorname{Bun}(G, ClaimSpace)$]', '[Gauge Bundle Category $\\operatorname{Bun}(G, \\operatorname{ClaimSpace})$]'),
    ('[统一定理 — Unification Theorem]', '[Unification Theorem]'),
    ('[统一场方程]', '[Unified Field Equation]'),
    ('[普适性原理]', '[Principle of Universality]'),
    ('[物理学中的 $\sum g = 0$]', '[$\\sum g = 0$ in Physics]'),
]:
    add(zh, en)

# Eight domains section headings
domain_headings = [
    ('八域统一：显式数学同构', 'The Eight-Domain Unification: Explicit Mathematical Isomorphisms'),
    ('领域一：MoE 路由 —— 平移群 $\mathbb{R}^d$ 与 MILP 规范固定',
     'Domain I: MoE Routing -- Translation Group $\\mathbb{R}^d$ and MILP Gauge Fixing'),
    ('领域定义', 'Domain Definition'),
    ('规范群：平移群 $\mathbb{R}^d$', 'Gauge Group: Translation Group $\\mathbb{R}^d$'),
    ('底流形与丛结构', 'Base Manifold and Bundle Structure'),
    ('联络与曲率', 'Connection and Curvature'),
    ('规范固定：MILP', 'Gauge Fixing: MILP'),
    ('同构映射', 'Isomorphism Map'),
    ('稳定性方程', 'Stability Equation'),
    ('领域二：博弈论 —— 策略偏离群与 NPE 均衡',
     'Domain II: Game Theory -- Strategy Deviation Group and NPE Equilibrium'),
    ('规范群：策略重参数化群', 'Gauge Group: Strategy Reparameterization Group'),
    ('规范固定：NPE 均衡', 'Gauge Fixing: NPE Equilibrium'),
    ('领域三：法学 —— 声明偏置群与诬告反坐',
     'Domain III: Law -- Claim Bias Group and False Accusation Counter-Punishment'),
    ('规范群：声明偏置群', 'Gauge Group: Claim Bias Group'),
    ('规范固定：诬告反坐', 'Gauge Fixing: False Accusation Counter-Punishment'),
    ('领域四：物理学 —— 杨-米尔斯 $SU(N)$ 与库仑/洛伦兹规范',
     'Domain IV: Physics -- Yang-Mills $SU(N)$ and Coulomb/Lorenz Gauge'),
    ('规范群：$SU(N)$', 'Gauge Group: $SU(N)$'),
    ('规范固定：库仑/洛伦兹规范', 'Gauge Fixing: Coulomb/Lorenz Gauge'),
    ('$\sum g = 0$ 的连续形式', 'Continuous Form of $\\sum g = 0$'),
    ('领域五：经济学 —— 协议中性群与圣经-教皇分离',
     'Domain V: Economics -- Protocol Neutrality Group and Bible-Pope Separation'),
    ('规范群：协议中性群', 'Gauge Group: Protocol Neutrality Group'),
    ('规范固定：圣经-教皇分离', 'Gauge Fixing: Bible-Pope Separation'),
    ('领域六：伦理学 —— 态度姿态群与"势能可高，态度如空气"',
     'Domain VI: Ethics -- Posture Group and "Potential High, Attitude Like Air"'),
    ('规范群：态度姿态群', 'Gauge Group: Posture Group'),
    ('规范固定：势能可高，态度如空气', 'Gauge Fixing: Potential High, Attitude Like Air'),
    ('领域七：文学 —— 叙事框架群与黑暗森林 $\to$ $\sum g = 0$ 宇宙',
     'Domain VII: Literature -- Narrative Frame Group and Dark Forest $\\to$ $\\sum g = 0$ Universe'),
    ('规范群：叙事框架群', 'Gauge Group: Narrative Frame Group'),
    ('黑暗森林作为弯曲规范场', 'Dark Forest as Curved Gauge Field'),
    ('规范固定：$\sum g = 0$ 宇宙', 'Gauge Fixing: $\\sum g = 0$ Universe'),
    ('领域八：文明论 —— 制度偏置群与 $\lambda$ 吸引子设计',
     'Domain VIII: Civilization -- Institutional Bias Group and $\\lambda$ Attractor Design'),
    ('规范群：制度偏置群', 'Gauge Group: Institutional Bias Group'),
    ('规范固定：$\lambda$ 吸引子设计', 'Gauge Fixing: $\\lambda$ Attractor Design'),
    # Part III
    ('统一：大定理与通用词典', 'Unification: The Great Theorem and Universal Dictionary'),
    ('统一定理：从领域范畴到规范丛范畴的函子',
     'The Unification Theorem: Functors from Domain Categories to the Category of Gauge Bundles'),
    ('范畴的构造', 'Construction of Categories'),
    ('统一函子的构造', 'Construction of the Unification Functor'),
    ('推论：统一场方程', 'Corollaries: Unified Field Equation'),
    ('函子图', 'Functor Diagram'),
    ('通用规范词典：八域一一对应',
     'The Universal Gauge Dictionary: One-to-One Correspondence Across All Eight Domains'),
    ('完整同构表', 'Complete Isomorphism Table'),
    ('结构的层次对应', 'Hierarchical Correspondence of Structures'),
    ('统一场方程的比较表', 'Comparison Table of Unified Field Equations'),
    ('意义与应用：万物归零之后', 'Implications and Applications: After Everything Returns to Zero'),
    ('理论意义', 'Theoretical Implications'),
    ('实践意义', 'Practical Implications'),
    ('哲学意义', 'Philosophical Implications'),
    ('结论：万物皆丛，万象归零', 'Conclusion: All Things Are Bundles, All Phenomena Return to Zero'),
    ('我们已经证明了什么', 'What We Have Proven'),
    ('统一场方程：最后的陈述', 'The Unified Field Equation: Final Statement'),
    ('最后的思考', 'Final Thoughts'),
    # Appendices
    ('附录 Appendices', 'Appendices'),
    ('附录A：数学符号表', 'Appendix A: Mathematical Notation'),
    ('附录B：八域声明类型对照表', 'Appendix B: Claim Types Across Eight Domains'),
    ('附录C：Cercis 计算协议', 'Appendix C: Cercis Computation Protocol'),
    ('附录D：八个域间的交叉推论', 'Appendix D: Cross-Domain Corollaries'),
]
for zh, en in domain_headings:
    add(zh, en)

print(f"Translation dict: {len(T)} entries")

# =============== PROCESS LINES ===============
out = []
i = 0
n = len(lines)

while i < n:
    line = lines[i]
    s = line.rstrip('\n')

    # Skip decorative Chinese-only lines
    if re.match(r'^\{?\s*[一-鿿]+\s*\}?\s*$', s):
        i += 1
        continue
    if re.match(r'^\{?\s*\*{0,2}[一-鿿]+\*{0,2}\s*\}?\s*$', s):
        i += 1
        continue

    # Bilingual heading: Chinese heading then English heading
    if (re.match(r'^#{1,6}\s', s) and has_cn(s) and
        i + 1 < n and
        re.match(r'^#{1,6}\s', lines[i+1]) and
        not has_cn(lines[i+1])):
        out.append(lines[i+1].rstrip())
        i += 2
        continue

    # Exact match in dictionary
    if s in T:
        val = T[s]
        if val:
            out.append(val)
        i += 1
        continue

    # Has Chinese - try extraction
    if has_cn(s):
        extracted = extract_ascii(s)
        if extracted and len(extracted) > 3:
            # Check if extracted content is meaningful
            # Count significant ASCII characters
            alpha = len(re.findall(r'[A-Za-z0-9]', extracted))
            if alpha >= 2:
                out.append(extracted)
        i += 1
        continue

    # No Chinese - keep
    out.append(s)
    i += 1

text = '\n'.join(out)

# Clean up
text = re.sub(r'\n{4,}', '\n\n\n', text)
text = re.sub(r'[ \t]+\n', '\n', text)
text = text.strip() + '\n'

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Phase 2 done: {len(text)} chars to {OUTPUT}')
