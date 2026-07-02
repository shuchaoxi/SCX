import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
cjk = re.compile(r'[一-鿿]+')

trans = {}

for idx, line in enumerate(lines):
    if not cjk.search(line):
        continue
    if 'Mixture-of-Experts' in line[:30]:
        continue

    # Translate based on first unique fragment
    l = line

    # FAQ and Discussion section
    if '你说' in l and '势能面不齐' in l and '联邦学习' in l:
        trans[l] = '### Q3: You say "potential surface misalignment" is a universal principle, but federated learning and model ensembles work well enough, so why care?'
    elif '这论文跟' in l and '模型合并' in l:
        trans[l] = '### Q6: How does this paper relate to the "model merging" line of work?'
    elif '两者可以结合：先用' in l:
        trans[l] = 'The two can be combined: first use Git Re-Basin to resolve permutation symmetry in weight space, then use this work\'s method to fix the gauge in representation space, then use Path 1 or Path 3 methods to improve routing or distillation.'
    elif '这是作者最不关心的问题' in l:
        trans[l] = '**Short answer:** This is the question the author cares about least. Theorems do not need reviewers to "understand" them -- they need to be **checked**. If a reviewer finds a mathematical error, that is something the author needs to fix.'

    # Path 2 blind spot
    elif '路二的盲区' in l:
        trans[l] = '### Path 2\'s Blind Spot: Shared Hallucination and Yajie+SVD Dual Filtering'
    elif '路二存在一个根本性盲区' in l:
        trans[l] = 'Path 2 has a fundamental blind spot: **Yajie cannot detect errors that all experts agree on.** This is an inherent limitation of consensus methods.'
    elif '三年的大模型军备竞赛' in l:
        trans[l] = '> **Honest Strike:** Three years of the large-model arms race has produced a large number of "shared hallucinations" -- all mainstream models trained on the same Internet corpus have learned the same erroneous facts and reasoning shortcuts. These errors appear as "high consensus" in Yajie\'s view -- and are therefore labeled CLEAN.}'
    elif '共享幻觉 (Shared Hallucination)' in l:
        trans[l] = '> **Definition:** [Shared Hallucination]'
    elif '设 $\\mathcal{D}_{train}$ 为所有专家的共同训练数据分布' in l:
        trans[l] = '> Let $\\mathcal{D}_{train}$ be the common training data distribution for all experts. An erroneous output $\\hat{y} \\neq y^*$ is called a **shared hallucination** if there exists a systematic bias $b(x)$ such that for all experts $m$,'
    elif '即所有专家在相同输入上犯同样的错误' in l:
        trans[l] = '> i.e., all experts make the same error on the same input.'
    elif '共享幻觉是 Yajie 的检测边界' in l:
        trans[l] = 'Shared hallucination is Yajie\'s detection boundary: when all $M_{eff}$ experts contain the same systematic bias, the Yajie consensus score $s_i$ approaches 1 -- **misclassified as clean data.**'
    elif 'Yajie对共享幻觉的盲区' in l:
        trans[l] = '> **Theorem:** [Yajie\'s Blind Spot for Shared Hallucination]'
    elif '即 Yajie 以指数接近 1 的概率将共享幻觉标记为 CLEAN' in l:
        trans[l] = '> i.e., Yajie labels shared hallucination as CLEAN with probability exponentially close to 1 -- **this is a miss, not a false positive**: all experts do indeed "agree," but they agree on an error.'
    elif '在共享幻觉条件下，每个专家的输出' in l and 'Proof' not in l:
        trans[l] = '> **Proof:** Under the shared hallucination condition, each expert\'s output $\\hat{y}_{hall}$ is identical with probability $\\geq 1 - \\delta$. By the Chernoff bound, when $\\delta < 1/2$, $p_{agree} \\geq 1 - M_{eff} \\delta$.'
    elif 'Yajie + SVD 互补定理' in l:
        trans[l] = '**Yajie + SVD Complementarity Theorem (Informal)**'
    elif '两者互补覆盖了幻觉空间' in l:
        trans[l] = '**Together they cover the hallucination space.** Yajie catches divergence, SVD catches "surface agreement but internal dispersion."'
    elif '共享幻觉的SVD检测' in l:
        trans[l] = '> **Theorem:** [SVD Detection of Shared Hallucination]'
    elif '共享幻觉与真知识的本质差异' in l:
        trans[l] = '> **Proof:** The essential difference between shared hallucination and true knowledge lies in the **geometric structure of representation space:**'
    elif '专家在处理已知事实时' in l:
        trans[l] = '> **True knowledge:** When experts process known facts, their internal representations concentrate along a low-dimensional "fact manifold" -- different experts\' outputs are highly collinear after gauge alignment.'
    elif '专家虽然输出了相同的 token 序列' in l:
        trans[l] = '> **Shared hallucination:** Although experts output the same token sequence, this output is produced through **statistical correlation** rather than **causal understanding** -- surface-level token consistency masks internal representational dispersion.'
    elif '双重过滤协议' in l:
        trans[l] = '> **Corollary:** [Dual Filtering Protocol]'
    elif '在实际蒸馏 pipeline 中' in l:
        trans[l] = '> In an actual distillation pipeline, apply to each training sample $(x_i, y_i)$:'
    elif 'Yajie 过滤：' in l:
        trans[l] = '1. **Yajie filter:** $s_i < \\theta_{noisy} \\Rightarrow$ discard (divergent hallucination)'
    elif 'SVD 过滤：' in l:
        trans[l] = '2. **SVD filter:** $\\rho_{10}(\\tilde{\\mathbf{Y}}_i) < \\tau_\\rho \\Rightarrow$ discard (shared hallucination -- the type missed by Yajie)'
    elif '双重通过' in l:
        trans[l] = '3. Double pass $\\Rightarrow$ CLEAN $\\Rightarrow$ enter training set'
    elif '双重过滤的代价' in l:
        trans[l] = '> **Honest Strike:** The cost of dual filtering: SVD filtering requires access to intermediate-layer representations (gauge-aligned expert outputs). This strips Path 2 of its low-cost advantage.'
    elif '数学题的天然优势' in l:
        trans[l] = '**Natural advantage of mathematical problems.** Mathematics is the ideal testing ground for dual filtering -- math has absolute answers, and correct vs. incorrect solutions are naturally separable in the SVD spectrum.'
    elif '路三：Gauge 对齐 + 表示级蒸馏' in l:
        trans[l] = '### Path 3: Gauge Alignment + Representation-Level Distillation'
    elif '先用规范固定（路一的 MILP/贪心）' in l:
        trans[l] = '**Core idea:** First use gauge fixing (Path 1\'s MILP/greedy) to align expert outputs to the same coordinate system, then perform distillation on intermediate-layer representations.'
    elif '为什么比路二更强' in l:
        trans[l] = '**Why is this stronger than Path 2?**'
    elif '路二只在最终输出上蒸馏' in l:
        trans[l] = 'Path 2 distills only on the final output -- information bottleneck: $V$ logits. Path 3 distills on intermediate-layer representations -- information bottleneck: $N \\times d$ dimensions.'
    elif '规范对齐的表示蒸馏' in l:
        trans[l] = '> **Protocol:** [Gauge-Aligned Representation Distillation]'
    elif '校准 + Gauge 固定' in l:
        trans[l] = '1. **Calibration + Gauge fixing.** Run Path 1\'s gauge fixing on $\\mathcal{D}_{cal}$ to obtain $\\{\\hat{\\mathbf{g}}_m^{(\\ell)}\\}$'
    elif '对齐表示提取' in l:
        trans[l] = '2. **Aligned representation extraction.** For each training sample $(x_i, y_i^*)$:'
    elif '多目标学生训练' in l:
        trans[l] = '3. **Multi-objective student training.** The loss function of the student model $S_\\phi$:'
    elif '可选：SVD 拒绝' in l:
        trans[l] = '4. **Optional: SVD rejection.** Directly reject samples with $\\rho_{10} < 0.3$ -- these are "true hallucinations."'
    elif '共识向量的信息论优势' in l:
        trans[l] = '**Information-theoretic advantage of the consensus vector.** Path 3\'s consensus vector $\\mathbf{c}_i^{(\\ell)}$ is the centroid of $N$ aligned experts -- it captures the direction that all experts jointly believe.'
    elif '共识向量比标量得分信息量大' in l:
        trans[l] = '> **Proposition:** [Consensus Vector Carries More Information Than Scalar Score]'
    elif '设路二的 Yajie 标量得分为' in l:
        trans[l] = '> Let Path 2\'s Yajie scalar score be $s_i \\in [0,1]$ and Path 3\'s consensus vector be $\\mathbf{c}_i \\in \\mathbb{R}^d$. Under mild assumptions, $\\mathbf{c}_i$ carries at least as much information as $s_i$.'
    elif 'Yajie 共识分数 $s_i$ 本质上' in l:
        trans[l] = '> **Proof:** The Yajie consensus score $s_i$ is essentially a measure of consistency among expert outputs in token probability space. After gauge alignment, $\\|\\mathbf{c}_i^{(\\ell)}\\|$ is strongly correlated with the consistency of expert outputs.'
    elif '路三是学术洁癖的最优解' in l:
        trans[l] = '> **Honest Strike:** Path 3 is the optimal solution for academic rigor -- it does not bypass the gauge problem, but solves it first. But Path 2 may be good enough in production environments.'
    elif '一分钟判断走哪条路' in l:
        trans[l] = '**One-Minute Decision: Which Path to Take**'

    # Equality Principle - short entries
    elif '以上定理构成了一个完整的工程框架。但势能面不齐的意义不止于工程。本节阐述它的' in l:
        trans[l] = 'The above theorems constitute a complete engineering framework. But the significance of potential surface misalignment goes beyond engineering. This section elaborates its **epistemological implications** -- why this mathematical fact changes our understanding of "knowledge," "consensus," and "comparison."'
    elif '本工作的 11 条定理中，任何单条都可以被未来的工作改进' in l:
        trans[l] = 'Among the 11 theorems of this work, any single one can be improved, superseded, or discarded by future work. MILP can be replaced by better optimization algorithms.'
    elif '但有一个东西不会过时' in l:
        trans[l] = 'But there is one thing that will not become outdated:'
    elif '平等论 (The Equality Principle)' in l:
        trans[l] = '**The Equality Principle**'
    elif '同一个系统内的不同观察者' in l:
        trans[l] = '**Different observers within the same system, even when receiving the same training objective and achieving the same training loss, will develop incomparable internal representations.**'
    elif '一致性不是天然的' in l:
        trans[l] = '**Consistency is not natural -- it must be explicitly constructed. The mathematical legitimacy of comparison is not granted by default -- it must be conferred by gauge fixing.**'
    elif '这不是一条定理。这是从定理 1-11 中提炼出的' in l:
        trans[l] = 'This is not a theorem. It is a **principle** distilled from Theorems 1-11. The theorems are its corollaries, the algorithms are its implementations, and the experiments are its verification.'
    elif '我们称这个原理为**平等论**' in l:
        trans[l] = 'We call this principle **The Equality Principle**. "Equality" has three layers of meaning here:'
    elif '坐标系的平等' in l and '没有任何专家的坐标系' in l:
        trans[l] = '1. **Equality of coordinate systems.** No expert\'s coordinate system is a privileged coordinate system. All gauge choices are equivalent under the training loss.'
    elif '知识生产的平等' in l and '不能由单一观察者产生' in l:
        trans[l] = '2. **Equality of knowledge production.** Knowledge cannot be produced by a single observer -- the Honest Person Theorem has proved that a single observer cannot distinguish noise, bias, learnability difficulty, and honest error.'
    elif '对齐作为先决条件' in l and '平等不是终点' in l:
        trans[l] = '3. **Alignment as a prerequisite.** Equality is not the endpoint -- it is the starting point. Gauge fixing **constructs comparability under the premise of equality.**'
    elif 'SCX 理论体系已建立了一条完整的认识论链' in l:
        trans[l] = 'The SCX theoretical system has established a complete epistemological chain. The Equality Principle is the newest link in it:'
    elif '知识生产的五阶段条件' in l:
        trans[l] = '**Five-Stage Conditions for Knowledge Production**'
    elif '柏拉图' in l and 'Gettier' in l and '闭合' in l:
        trans[l] = '**Plato to Gettier closure:** Plato required knowledge to be "justified true belief." Gettier demonstrated that justification can be accidentally true.'
    elif 'SCX 的回答是：知识不是个体认知状态' in l:
        trans[l] = 'SCX\'s answer is: knowledge is not an individual cognitive state, but a **verifiable output of a multi-observer consensus process**.'

    # More Equality Principle
    elif '爱因斯坦最伟大的贡献不是' in l:
        trans[l] = 'Einstein\'s greatest contribution was not the formula $E=mc^2$ -- it was the concept of the **principle of relativity**. The Equality Principle does something similar.'
    elif '在比较之前先对齐' in l:
        trans[l] = '**Align before comparing -- not because doing so is better, but because without doing so, comparison itself is mathematically undefined.**'
    elif '势能面可以高低不平' in l:
        trans[l] = '**The potential surface can be uneven.** Imagine three successively descending potential steps: a high region, a middle region, and a low region.'
    elif '但在交汇处必须齐平' in l:
        trans[l] = '**But at the interface, they must be level.** When two steps make contact, they must be at the same height at the contact point.'
    elif '这个几何事实给出了' in l:
        trans[l] = 'This geometric fact provides a precise mathematical formulation of "all people are equal" -- **not that everyone is the same height, but that every contact point must be level.**'
    elif '这解释了为什么' in l and '不是道德主张' in l:
        trans[l] = '> **Honest Strike:** This explains why "all people are equal" is not a moral claim -- it is a **communication condition.** Inequality leads to communication failure.'
    elif '与国家边界的类比' in l:
        trans[l] = '**Analogy with national borders.** Country A has internal wealth disparity. Country B does too. But when two countries sign a trade agreement, the negotiation table must be at the same height.'
    elif '规范固定条件 $\\sum_m \\mathbf{g}_m' in l and '哲学含义' in l:
        trans[l] = '**Philosophical meaning of the gauge fixing condition $\\sum_m \\mathbf{g}_m = \\mathbf{0}$.** In MILP gauge fixing, the zero-sum constraint appears to be a technical detail. But its philosophical meaning is profound:'
    elif '所有专家的规范偏移之和为零' in l:
        trans[l] = '**The sum of all experts\' gauge offsets is zero = no expert is a privileged origin.**'
    elif '这不是随意选的规范固定条件' in l:
        trans[l] = 'This is not an arbitrary choice of gauge fixing condition. It is the only condition that does not grant any expert a privileged position.'
    elif '人人平等定理' in l and '汇合' in l:
        trans[l] = '**Convergence of the Equality Principle and the "All Men Are Equal" Theorem.** In the SCX theorem system, this theorem states: $P(W_A) = P(W_B)$ holds for all observers $A, B$.'
    elif '平等论补充了另一半' in l:
        trans[l] = 'The Equality Principle supplies the other half: **equality of representational frameworks.** Not only is no one\'s cognitive ability privileged -- no one\'s coordinate system is naturally "standard."'
    elif '人人平等定理（认知平等）' in l:
        trans[l] = '- **All Men Are Equal Theorem (cognitive equality):** No one has a privileged observational position -- $P(W_A) = P(W_B)$.'
    elif '平等论（表示平等）' in l:
        trans[l] = '- **The Equality Principle (representational equality):** No one\'s coordinate system is naturally standard -- $\\sum_m \\mathbf{g}_m = \\mathbf{0}$.'
    elif '完整的平等' in l:
        trans[l] = '**Complete equality**'
    elif '认知平等 + 表示平等' in l:
        trans[l] = 'Cognitive equality + representational equality $\\rightarrow$ communication requires prior alignment $\\rightarrow$ aligned consensus is the only legitimate source of knowledge.'
    elif '这个汇合暗示了一个令人不安的推论' in l:
        trans[l] = '> **Honest Strike:** This convergence implies a disturbing corollary: most "communication" in current human society may be comparing incomparable things. Not because we are unwilling to understand each other, but because we never explicitly fixed our gauges.'
    elif '自由流动' in l and '动力学推论' in l:
        trans[l] = '### Free Flow: Dynamical Consequences of Potential Surface Continuity'
    elif '前节讨论了静态的势能面几何。本节讨论它的' in l:
        trans[l] = 'The previous section discussed static potential surface geometry. This section discusses its **dynamics**: when there is a jump on the potential surface, what does the system do?'
    elif '这是最小作用量原理在势能面上的直接表达' in l:
        trans[l] = 'This is a direct expression of the principle of least action on the potential surface -- not a moral choice, but a physical tendency.'
    elif '推论：自由流动不是人权——是结构稳定条件' in l:
        trans[l] = '**Corollary: Free flow is not a human right -- it is a structural stability condition.**'
    elif '这不意味着边界应该消失' in l:
        trans[l] = '> **Honest Strike:** This does not mean borders should disappear. Borders define the identity of a system. But the potential jump at the border must be actively managed.'
    elif '鹤立鸡群' in l and '内部势能奇点的必然命运' in l:
        trans[l] = '### Towering Above the Flock: The Inevitable Fate of Internal Potential Singularities'

    # Conclusion section
    elif '我们识别并形式化了多专家路由中的一个根本性但此前未被注意的问题' in l:
        trans[l] = 'We identify and formalize a fundamental but previously unnoticed problem in multi-expert routing: **Potential Surface Misalignment** -- different experts define their outputs in gauge-inequivalent coordinate systems. We prove this is an instance of **gauge freedom**, parallel to but more general than the gauge problem in ACE potentials.'
    elif '我们提出了MILP规范固定框架' in l:
        trans[l] = 'We propose an MILP gauge-fixing framework, establish convex relaxations and greedy approximations, and provide error guarantees. We establish the SVD spectral concentration after gauge fixing as a provable hallucination detection indicator.'
    elif '**核心信息**' in l:
        trans[l] = '**Core message:** Align before comparing. This is not just an engineering practice -- it is a mathematical necessity.'
    elif '**致谢：**' in l:
        trans[l] = '**Acknowledgments:** This work was completed independently under the "SCX Framework." Thanks to all honest administrators for their pioneering example.'

    # Reference entries with Chinese titles
    elif '哈密顿量作为审计条件' in l:
        trans[l] = ' ``Hamiltonian as Audit Condition: Judging Auditability from the Energy Landscape,'''
    elif '老实人定理 (Honest Person Theorem)' in l and '无额外假设' in l:
        trans[l] = ' ``Honest Person Theorem: Without Additional Assumptions, a Single Observer Cannot Distinguish Noise, Bias, Learnability Difficulty, and Honest Error,'''
    elif 'Yajie协议：多专家共识中的诚实纳什均衡' in l:
        trans[l] = ' ``Yajie Protocol: Honest Nash Equilibrium in Multi-Expert Consensus,'''


applied = 0
for old_line, new_line in trans.items():
    if old_line in content and 'Mixture-of-Experts' not in old_line[:30]:
        content = content.replace(old_line, new_line)
        applied += 1

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)

remaining = [l for l in content.split('\n') if cjk.search(l) and 'Mixture-of-Experts' not in l[:30]]
print(f'Applied: {applied}')
print(f'Remaining: {len(remaining)}')
