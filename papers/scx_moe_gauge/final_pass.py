# -*- coding: utf-8 -*-
"""
Final comprehensive translation pass for main.md.
Uses exact fragment matching for remaining Chinese text.
"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
cjk = re.compile(r'[一-鿿]+')

# Build translation map: fragment -> English replacement
# Order matters: more specific fragments first
translation_rules = []

def add_rule(fragment, english, start=0, end=None):
    """Add a translation rule: if line contains fragment, replace entire line"""
    translation_rules.append((fragment, english, start, end))

# ===== PROBLEM SETUP & GAUGE FORMALIZATION =====
add_rule('设路由器 $r(x) =', '> Let the router be $r(x) = \\text{softmax}(W_r x)$, where $W_r \\in \\mathbb{R}^{N \\times d}$ is fixed after training. Applying a translation gauge transformation $E_m \\to E_m + \\mathbf{g}_m$ (with $\\mathbf{g}_m \\in \\mathbb{R}^d$) to expert $m$, the routing score does **not** change under the transformation -- that is, $r(x)$ has zero explicit dependence on $E_m(x)$, because $r(x)$ does not receive $E_m(x)$ as input.', 150, 200)

add_rule('若 $\\gamma_m$ 不全部相同', '> If the $\\gamma_m$ are not all identical, there exist $m_1, m_2$ such that $\\gamma_{m_1} \\neq \\gamma_{m_2}$. Consider input $x$ such that $E_{m_1}(x) = E_{m_2}(x)$ (such points exist in the training distribution because $d \\ll$ data dimension). In the original gauge, $r_{m_1}(x) = r_{m_2}(x)$. In the new gauge, the outputs $\\gamma_{m_1}(E_{m_1}(x))$ and $\\gamma_{m_2}(E_{m_2}(x))$ are unequal -- but the router still assigns the same scores, which is suboptimal.', 210, 250)

add_rule('我们将规范固定表述为一个优化问题', 'We formulate gauge fixing as an optimization problem: find gauge parameters $\\{\\mathbf{g}_m\\}$ such that, on the given calibration input set, expert outputs are as comparable as possible in the same "coordinate system".', 240, 260)

add_rule('贪心算法等价于以样本均值估计', '> **Proof:** The greedy algorithm is equivalent to estimating each expert\'s output expectation by the sample mean: $\\hat{\\mu}_m = \\frac{1}{n}\\sum_i E_{im}$. By Hoeffding\'s inequality (under the sub-Gaussian assumption),', 315, 335)

add_rule('期望平方误差为', '> The expected squared error is $\\mathbb{E}[\\|\\hat{\\mu}_m - \\mu_m\\|^2] = \\frac{\\text{Tr}(\\Sigma)}{n}$.', 322, 335)

add_rule('MILP的最优规范参数', '> In the simplest case (without routing interaction), the optimal gauge parameters $\\mathbf{g}_m^*$ of the MILP are equivalent to centering: $\\mathbf{g}_m^* = \\mu_m - \\frac{1}{N}\\sum_j \\mu_j$. The greedy algorithm estimates this quantity as $\\hat{\\mathbf{g}}_m = \\hat{\\mu}_m - \\frac{1}{N}\\sum_j \\hat{\\mu}_j$. The error is', 325, 340)

add_rule('平方范数的期望：', '> Expectation of the squared norm:', 332, 340)

add_rule('加上归一化步骤后', '> After adding the normalization step, the total error is bounded by $2\\text{Tr}(\\Sigma)/n \\cdot (1 + 1/N)$.', 340, 350)

add_rule('其中 $\\sigma_*(\\mathbf{Y})$ 是', '> where $\\sigma_*(\\mathbf{Y})$ is the smallest non-zero singular value of $\\mathbf{Y}$.', 365, 380)

add_rule('定义有效秩为满足', '> Define the effective rank as the smallest $r$ satisfying $\\sum_{i=1}^{r} \\sigma_i^2 \\geq \\rho \\cdot \\|\\mathbf{Y}\\|_F^2$ (taking $\\rho = 0.95$). The additional energy dispersion introduced by the gauge perturbation is $\\|\\mathbf{G}\\|_F^2$, which adds at most $\\|\\mathbf{G}\\|_F^2 / \\sigma_*^2$ effective dimensions.', 370, 385)

add_rule('设规范已通过MILP', '> Suppose the gauge has been fixed by MILP (Section [ref]), and all expert outputs after gauge fixing become $\\tilde{E}_m(x) = E_m(x) - \\hat{\\mathbf{g}}_m$. For input $x$, construct the aligned output matrix $\\tilde{\\mathbf{Y}} = [\\tilde{E}_1(x), ..., \\tilde{E}_N(x)]^T$. If the model\'s confidence on query $x$ exceeds threshold $\\theta$ (i.e., all experts are "consistent" after gauge alignment), then', 390, 410)

add_rule('其中 $\\Delta$ 是确信与不确信之间的最小间隔', '> where $\\Delta$ is the minimum margin between certainty and uncertainty, and $\\gamma$ is the gauge fixing residual energy ratio.', 398, 410)

add_rule('规范固定后，若模型对查询$x$确信', '> After gauge fixing, if the model is certain about query $x$, there exists a "consensus direction" $\\mathbf{v}^* \\in \\mathbb{R}^d$ ($\\|\\mathbf{v}^*\\| = 1$) such that all experts\' outputs are highly aligned along this direction. Formally: $\\langle \\tilde{E}_m(x), \\mathbf{v}^* \\rangle \\geq \\Delta > 0$ holds for all $m$.', 400, 415)

add_rule('在此条件下，$\\tilde{\\mathbf{Y}}$ 在第$\\mathbf{v}^*$方向上的投影的方差由专家的非共识分量决定', '> Under this condition, the variance of the projection of $\\tilde{\\mathbf{Y}}$ along the $\\mathbf{v}^*$ direction is determined by the non-consensus components of the experts. By Hoeffding\'s inequality, the variance of non-consensus components among $M_{eff}$ effectively independent experts converges exponentially. Specifically:', 405, 415)

add_rule('其中 $\\gamma = \\|\\mathbf{G}_{res}\\|_F', '> where $\\gamma = \\|\\mathbf{G}_{res}\\|_F / \\|\\tilde{\\mathbf{Y}}\\|_F$ is the gauge fixing residual energy ratio. Under exact gauge fixing (e.g., the $<10^{-15}$ achieved by the EGP work), $\\gamma \\approx 0$, and the exponential decay rate is $2M_{eff}\\varepsilon^2$.', 410, 420)

# ===== UNIFICATION WITH ACE =====
add_rule('在本节中，我们展示MoE规范固定和ACE规范固定', 'In this section, we show that MoE gauge fixing and ACE gauge fixing [EGP paper] are instances of the same mathematical structure.', 425, 440)

add_rule('一个**模块化规范系统**', '> A **Modular Gauge System (MGS)** consists of a triple $(\\{C_m\\}, \\mathcal{G}, \\Pi)$:', 432, 442)

add_rule('$C_m$：独立训练的模块化组件', '- $C_m$: independently trained modular components (ACE expert coefficients or MoE expert networks)', 434, 445)

add_rule('$\\mathcal{G}$：规范群', '- $\\mathcal{G}$: gauge group -- the transformation group that preserves all observable predictions under each component\'s training loss', 435, 445)

add_rule('$\\Pi$：规范固定投影器', '- $\\Pi$: gauge fixing projector -- a linear projection (or more general contraction mapping) that maps each component into the gauge-fixed subspace', 436, 446)

add_rule('设 $(\\{C_m\\}, \\mathcal{G}, \\Pi)$ 是一个MGS', '> Let $(\\{C_m\\}, \\mathcal{G}, \\Pi)$ be an MGS. If cross-component operations (merging, comparing, routing) are performed directly without applying $\\Pi$, the results are not preserved under gauge transformations -- different gauge choices yield different operation results. If $\\Pi$ is applied before operating, the results are invariant under gauge transformations.', 440, 450)

add_rule('未固定规范时的跨组件操作', '> A cross-component operation $F(C_1, ..., C_N)$ without gauge fixing (e.g., coefficient averaging or routing score computation) transforms under gauge transformations $C_m \\to \\gamma_m \\circ C_m$ into $F(\\gamma_1 \\circ C_1, ..., \\gamma_N \\circ C_N)$. Unless $F$ is invariant under $\\mathcal{G}^{\\times N}$ -- which requires $\\gamma_1 = ... = \\gamma_N$ (a global gauge transformation) -- $F$ is not preserved under gauge transformations.', 442, 452)

add_rule('施加 $\\Pi$ 后', '> After applying $\\Pi$: $F(\\Pi(C_1), ..., \\Pi(C_N))$. Since $\\Pi(C_m) = \\Pi(\\gamma_m \\circ C_m)$ (the projector contracts the gauge orbit to a single representative), $F(\\Pi(C_1), ..., \\Pi(C_N))$ is invariant under gauge transformations.', 444, 455)

add_rule('（ACE情况：$\\Pi$', '> (ACE case: $\\Pi$ = orthogonal projection onto the $\\sum_Z \\pi_Z \\mathbf{c}_Z = 0$ subspace. MoE case: $\\Pi$ = solving MILP to obtain $\\hat{\\mathbf{g}}_m$ and subtracting it from $E_m$.)', 446, 458)

add_rule('两个问题的共同起源是简单的：', 'The common origin of both problems is simple:', 452, 460)

add_rule('**模块化规范原理 (Modular Gauge Principle)**', '**Modular Gauge Principle**', 458, 466)

add_rule('任何由独立训练的组件构成的系统，其中组件的训练损失在某个规范群', 'Any system composed of independently trained components, where the training loss of each component is invariant under some gauge group $\\mathcal{G}$, must explicitly apply gauge fixing before **comparing, merging, routing, or aggregating** the outputs of these components -- otherwise the operation results depend on unobserved training history rather than the intrinsic properties of the components.', 460, 470)

add_rule('这一原理预示了规范问题可能存在于其他模块化系统中', 'This principle suggests that gauge problems may exist in other modular systems: model aggregation in federated learning, multi-model voting in ensemble methods, multimodal fusion, and even policy coordination in multi-agent systems -- each has its own version of "misaligned potential surfaces."', 467, 475)

# ===== EXPERIMENTS =====
add_rule('以下实验方案需要在具有稀疏MoE架构的Transformer模型上执行', 'The following experimental protocol needs to be executed on Transformer models with sparse MoE architectures (e.g., Mixtral 8x7B, DeepSeek-V2, etc.). Calibration sets can be randomly sampled from general text corpora (no labels needed). Core metrics require only forward passes to compute.', 470, 480)

add_rule('**预期**：规范不对齐应显著高于随机基线', '**Expected:** Gauge misalignment should be significantly higher than the random baseline ($p < 0.001$), and accumulate with layer depth (Corollary [ref]).', 483, 493)

add_rule('**目标**：验证规范固定是否改善路由的一致性。', '**Goal:** Verify whether gauge fixing improves routing consistency.', 488, 498)

add_rule('**预期**：路由翻转率在早期层应较高', '**Expected:** The routing flip rate should be high in early layers ($>5\\%$) and low in later layers (subsequent Transformer layers partially adapt to the gauge differences). Gauge fixing should not significantly increase perplexity (change $< 2\\%$), and may slightly decrease perplexity due to more reasonable expert assignments.', 495, 505)

add_rule('**目标**：验证规范对齐后的SVD谱是否能区分幻觉与非幻觉输出。', '**Goal:** Verify whether the SVD spectrum after gauge alignment can distinguish hallucinated from non-hallucinated outputs.', 500, 510)

# Apply rules
applied = 0
for fragment, english, start, end in translation_rules:
    for i in range(start, min(end, len(lines))):
        if fragment in lines[i] and cjk.search(lines[i]):
            lines[i] = english
            applied += 1
            break

print(f"Applied: {applied} translations")

# Check remaining
cn_remaining = [(i+1, l) for i, l in enumerate(lines) if cjk.search(l)]
print(f"Chinese lines remaining: {len(cn_remaining)}")
for num, text in cn_remaining[:15]:
    print(f"  L{num}: {text[:80]}")

content = '\n'.join(lines)
with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
