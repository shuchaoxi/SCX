#!/usr/bin/env python3
"""Complete Chinese->English translation script for theory/ Batch 1 (14 files)."""
import os, re

BASE = r'F:\scx\theory'
cn_re = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

FILES = [
    'definitions/01_state_conditioned_risk.tex',
    'explorations/a2_correlation_analysis.tex',
    'explorations/a2_rigorous_analysis.tex',
    'explorations/exact_constant_minimax.tex',
    'explorations/scx_complexity.tex',
    'explorations/scx_galois_deep.tex',
    'explorations/turbulence_unidentifiability.tex',
    'explorations/verification_exact_constant.tex',
    'information_theory/fano_scx.tex',
    'information_theory/information_limits.tex',
    'information_theory/landauer_scx.tex',
    'propositions/01_global_ranking_insufficiency.tex',
    'propositions/01_regret_lower_bound.tex',
    'propositions/02_higherror_suboptimality.tex',
]

def global_fixes(content):
    content = content.replace('\\mathsf', '\\textsf')
    return content

def get_translations(rel):
    b = os.path.basename(rel)
    t = []
    
    # Generic terms
    gen = [
        ('参考文献', 'References'), ('符号表', 'Notation Table'),
        ('证明', 'Proof'), ('证明概要', 'Proof Sketch'),
        ('推导', 'Derivation'), ('总结', 'Summary'),
        ('附录', 'Appendix'), ('关联', 'Related'),
        ('状态', 'Status'), ('注', 'Note'),
        ('推导概要', 'Derivation Sketch'),
        ('直觉证明', 'Intuitive Proof'),
        ('正式陈述', 'Formal Statement'),
        ('正式证明', 'Formal Proof'),
        ('构造法', 'Constructive Method'),
        ('反例', 'Counterexample'),
        ('修正证明', 'Corrected Proof'),
        ('反证法', 'Proof by Contradiction'),
    ]
    
    # ═══════════════════════════════════════════════════════════
    # FILE 1: 01_state_conditioned_risk.tex (remaining cleanup)
    # ═══════════════════════════════════════════════════════════
    if b == '01_state_conditioned_risk.tex':
        t = [
            ('第 \\(m\\) 个专家模型', 'The \\(m\\)-th expert model'),
            ('\\(\\mathcal{X}\\) 的可测子集', 'measurable subset of \\(\\mathcal{X}\\)'),
            ('回归函数 \\(\\mathbb{E}[Y \\mid X=x]\\)', 'Regression function \\(\\mathbb{E}[Y \\mid X=x]\\)'),
            ('近似误差', 'Approximation error'),
            ('目标噪声', 'Target noise'),
            ('偏差-方差分解', 'Bias-Variance Decomposition'),
            ('噪声与可学习性', 'Noise and Learnability'),
            ('专家路由', 'Expert Routing'),
            ('加权', 'Weighted'),
            ('硬路由', 'Hard Routing'),
            ('清洁', 'clean'),
            ('噪声', 'noise'),
            ('事实', 'fact'),
            ('世界', 'world'),
            ('全局', 'Global'),
            ('高', 'High'),
            ('无', 'None'),
            ('低', 'Low'),
            ('中', 'Medium'),
            ('问题确诊', 'Problem Diagnosis'),
            ('修复方案', 'Repair Strategy'),
            ('诚实化', 'Honestifying'),
            ('弱相关集中不等式', 'Weakly-Correlated Concentration Inequality'),
            ('修正后的', 'Corrected'),
            ('诚实结论', 'Honest Conclusions'),
            ('数值验证', 'Numerical Verification'),
            ('需要填充的引理', 'Lemmas to Fill In'),
            ('Agent 任务', 'Agent Tasks'),
            ('引理 A:', 'Lemma A:'),
            ('引理 B:', 'Lemma B:'),
            ('引理 C:', 'Lemma C:'),
            ('引理 D:', 'Lemma D:'),
            ('引理 E:', 'Lemma E:'),
            ('引理 F:', 'Lemma F:'),
            ('验证倾斜测度的所有计算', 'Verify all computations of the tilted measure'),
            ('给出 \\(o(1)\\) 项的显式界 (Berry-Esseen 型修正)', 'Provide explicit bounds for the \\(o(1)\\) term (Berry-Esseen-type correction)'),
            ('推广到非 i.i.d. 但仍独立的 Bernoulli（不同 \\(p_m\\)）', 'Generalize to non-i.i.d. but still independent Bernoulli (different \\(p_m\\))'),
            ('从\n\\(1-\\text{F1} \\approx \\frac{1}{2}\\text{FNR} + \\frac{1-\\eta}{2\\eta}\\text{FPR}\\)\n到包括 \\(O(e^{-2M\\kappa})\\) 项', 'From \\(1-\\text{F1} \\approx \\frac{1}{2}\\text{FNR} + \\frac{1-\\eta}{2\\eta}\\text{FPR}\\) to including \\(O(e^{-2M\\kappa})\\) terms'),
            ('验证展开在 \\(\\eta \\to 0\\) 或 \\(\\eta \\to 1\\) 时的有效性', 'Verify validity of the expansion as \\(\\eta \\to 0\\) or \\(\\eta \\to 1\\)'),
            ('\\(C(\\text{Bern}(p_0), \\text{Bern}(p_1))\\) 的闭式解 (不是数值解)', 'Closed-form solution for \\(C(\\text{Bern}(p_0), \\text{Bern}(p_1))\\) (not numerical)'),
            ('与 \\(2(p_1-p_0)^2\\) (Hoeffding) 和\n\\(\\frac{1}{2}(\\sqrt{p_0} - \\sqrt{p_1})^2\\) (Hellinger) 的比较', 'Comparison with \\(2(p_1-p_0)^2\\) (Hoeffding) and \\(\\frac{1}{2}(\\sqrt{p_0} - \\sqrt{p_1})^2\\) (Hellinger)'),
            ('证明 \\(\\theta^\\dagger\\) 最小化 \\(1-\\text{F1}\\) 的渐近表达式', 'Prove that \\(\\theta^\\dagger\\) minimizes the asymptotic expression for \\(1-\\text{F1}\\)'),
            ('验证 \\(\\theta^\\dagger = \\theta^* + O(1/M)\\)', 'Verify \\(\\theta^\\dagger = \\theta^* + O(1/M)\\)'),
            ('导出使用 \\(\\theta^\\dagger\\) 的精确常数', 'Derive the exact constant when using \\(\\theta^\\dagger\\)'),
            ('形式化状态 ``任何算法不优于 LRT\'\'', 'Formalize the statement ``no algorithm outperforms LRT\'\''),
            ('Le Cam 第三引理 + LAN 框架下的精确常数', 'Exact constant under Le Cam\'s Third Lemma + LAN framework'),
            ('或者：使用 Ingster-Suslina 的非参数检验下界框架', 'Alternatively: use Ingster-Suslina\'s nonparametric testing lower-bound framework'),
            ('从单状态常数最优推广到 \\(\\sum_s \\rho_s\\) 加权', 'Generalize from single-state constant optimality to \\(\\sum_s \\rho_s\\) weighting'),
            ('证明全局常数\n\\(C_{\\text{global}} = \\sum_s \\rho_s C_s\\)（受最坏状态支配）', 'Prove that the global constant is \\(C_{\\text{global}} = \\sum_s \\rho_s C_s\\) (dominated by the worst state)'),
            ('状态: 证明架构完成。Agent 任务待启动以填充 Lemma A-F 的详细推导。', 'Status: Proof architecture complete. Agent tasks pending to fill in detailed derivations for Lemmas A-F.'),
        ]
    
    # ═══════════════════════════════════════════════════════════
    # FILE 2: a2_correlation_analysis.tex (remaining cleanup)
    # ═══════════════════════════════════════════════════════════
    elif b == 'a2_correlation_analysis.tex':
        t = [
            ('A2 依赖程度', 'A2 Dependence'),
            ('关联影响', 'Correlation Impact'),
            ('修正难度', 'Repair Difficulty'),
            ('无需修正', 'No correction needed'),
        ]
    
    # ═══════════════════════════════════════════════════════════
    # FILE 3: a2_rigorous_analysis.tex  (227 CN segments)
    # ═══════════════════════════════════════════════════════════
    elif b == 'a2_rigorous_analysis.tex':
        t = [
            ('的严格数学分析', '--- Rigorous Mathematical Analysis'),
            ('触发: hostile review 指出 \\(\\exp(-2M\\Delta^2/(1+(M-1)\\rho))\\)\n不是严格定理 结论: 正确。方差膨胀代入 Hoeffding\n是指启发式，不是严格界。但 A2 本身有更强的论证。',
             'Trigger: hostile review points out that \\(\\exp(-2M\\Delta^2/(1+(M-1)\\rho))\\)\nis not a rigorous theorem. Conclusion: correct. Plugging variance inflation into Hoeffding\nis a heuristic, not a rigorous bound. But A2 itself has stronger justification.'),
            ('是不是严格定理？', '--- Is It a Rigorous Theorem?'),
            ('\\textbf{不是。}', '\\textbf{No.}'),
            ('Hoeffding 不等式的证明依赖:', 'The proof of Hoeffding\'s inequality depends on:'),
            ('这个\\textbf{因式分解}要求 \\(\\{X_i\\}\\) 独立。如果 \\(X_i\\) 相关，MGF\n不能因式分解，你不能简单地把 \\(M\\) 替换成 \\(M/(1+(M-1)\\rho)\\)\n就得到严格指数界。',
             'This \\textbf{factorization} requires \\(\\{X_i\\}\\) to be independent. If \\(X_i\\) are correlated, the MGF\ncannot be factorized, and you cannot simply substitute \\(M/(1+(M-1)\\rho)\\) for \\(M\\)\nto obtain a rigorous exponential bound.'),
            ('方差膨胀 \\((1+(M-1)\\rho)\\) 对 \\textbf{\\(\\text{Var}(\\sum X_i)\\)}\n是正确的，但对 \\textbf{指数集中} 不正确。方差只给 Chebyshev\n界（多项式速率 \\(1/t^2\\)），不是指数界。',
             'Variance inflation \\((1+(M-1)\\rho)\\) is correct for \\textbf{\\(\\text{Var}(\\sum X_i)\\)}\nbut not for \\textbf{exponential concentration}. Variance only gives a Chebyshev\nbound (polynomial rate \\(1/t^2\\)), not an exponential bound.'),
            ('\\textbf{结论}: 方差膨胀 Hoeffding\n是启发式（heuristic），在调查抽样和群组随机试验中广泛使用，但不是数学定理。把它写进\nSI 会被审稿人抓。',
             '\\textbf{Conclusion}: The variance-inflated Hoeffding\nis a heuristic, widely used in survey sampling and cluster randomized trials, but it is not a mathematical theorem. Writing it into the\nSI will get caught by reviewers.'),
            ('那 A2 本身到底站不站得住？', 'So Does A2 Itself Hold Up or Not?'),
            ('更强的论证: A1 蕴含 A2', 'A Stronger Argument: A1 Implies A2'),
            ('A1 说: \\(M\\) 个专家在\\textbf{不相交的独立同分布子集}上训练。',
             'A1 states: \\(M\\) experts are trained on \\textbf{disjoint i.i.d. subsets}.'),
            ('每个 \\(f_m = \\mathcal{A}(D_m)\\) 是训练算法 \\(\\mathcal{A}\\)\n作用于数据子集 \\(D_m\\) 的\\textbf{确定函数}。',
             'Each \\(f_m = \\mathcal{A}(D_m)\\) is a \\textbf{deterministic function} of training algorithm \\(\\mathcal{A}\\)\napplied to data subset \\(D_m\\).'),
            ('因为 \\(D_1, \\dots, D_M\\) 是独立随机变量，\\(f_1, \\dots, f_M\\)\n也是独立的随机函数。',
             'Since \\(D_1, \\dots, D_M\\) are independent random variables, \\(f_1, \\dots, f_M\\)\nare also independent random functions.'),
            ('\\textbf{A2 不是假设------它是 A1 的推论。}', '\\textbf{A2 is not an assumption --- it is a corollary of A1.}'),
            ('概率空间是什么？', 'What Is the Probability Space?'),
            ('Hoeffding\n界的概率空间是\\textbf{训练数据的随机性}，不是测试数据的随机性。',
             'The probability space of the Hoeffding\nbound is the \\textbf{randomness of training data}, not the randomness of test data.'),
            ('意思是: 如果你随机划分训练数据 \\(M\\) 次、独立训练 \\(M\\)\n个专家，得到的专家集以高概率具有好的噪声检测性质。',
             'Meaning: if you randomly partition training data \\(M\\) times and independently train \\(M\\)\nexperts, the resulting expert ensemble has good noise-detection properties with high probability.'),
            ('\\textbf{训练完成后}，你有一组固定的专家。对于给定的测试样本\n\\(x\\)，\\(C(x)\\) 是一个确定性的数。Hoeffding 不适用。',
             '\\textbf{After training}, you have a fixed set of experts. For a given test sample\n\\(x\\), \\(C(x)\\) is a deterministic number. Hoeffding does not apply.'),
            ('但这不削弱定理------所有的泛化界都有这个性质。定理告诉你\'\'这个\\textbf{方法}是好的\'\'，不是\'\'这组\\textbf{特定专家}是好的\'\'。',
             'But this does not weaken the theorem --- all generalization bounds have this property. The theorem tells you ``this \\textbf{method} is good,\'\' not ``this \\textbf{specific ensemble} is good.\'\''),
            ('Hostile reviewer 的反驳为什么不对', 'Why the Hostile Reviewer\'s Objection Is Wrong'),
            ('这是在说: \\textbf{给定已经训练好的\nCNN}，它们在模糊图像上的确定行为是一致的。',
             'This is saying: \\textbf{given already-trained\nCNNs}, their deterministic behavior on blurry images is consistent.'),
            ('但 Hoeffding 问的是:\n\\textbf{在训练之前}，随机划分数据并独立训练后，你有多大把握得到一组能检测噪声的专家？',
             'But what Hoeffding asks is:\n\\textbf{before training}, after randomly partitioning data and independently training, how confident are you of obtaining an ensemble that can detect noise?'),
            ('两者不在同一个概率空间里。Hostile reviewer\n混淆了\\textbf{训练后确定性行为}和\\textbf{训练前概率保证}。',
             'These two are not in the same probability space. The hostile reviewer\nconfuses \\textbf{post-training deterministic behavior} with \\textbf{pre-training probabilistic guarantee}.'),
            ('但仍有一个残留问题', 'But There Remains a Residual Issue'),
            ('即使 A2 严格成立（作为 A1 的推论），\\textbf{估计} \\(\\mu_s\\)\n仍然需要清洁标签。在有限样本下，\\(\\hat{\\mu}_s\\) 的误差会转化为\n\\(\\hat{\\Delta}_s\\)\n的误差。这是\\textbf{有限样本估计问题}，不是\\textbf{独立性假设问题}。推论\n4（有限样本校正）已经用保守上界处理了这个问题。',
             'Even if A2 holds rigorously (as a corollary of A1), \\textbf{estimating} \\(\\mu_s\\)\nstill requires clean labels. In finite samples, errors in \\(\\hat{\\mu}_s\\) translate into\nerrors in \\(\\hat{\\Delta}_s\\).\nThis is a \\textbf{finite-sample estimation problem}, not an \\textbf{independence assumption problem}. Corollary\n4 (finite-sample correction) already handles this with a conservative upper bound.'),
            ('诚实的修改建议', 'Honest Revision Suggestions'),
            ('不要引入 A2\'', 'Do Not Introduce A2\''),
            ('方差膨胀 Hoeffding 是启发式，不够格写进定理陈述。保持原有的\nA2，但\\textbf{在正文和 SI 中诚实讨论}。',
             'The variance-inflated Hoeffding is a heuristic and is not qualified for theorem statements. Keep the original\nA2, but \\textbf{discuss it honestly in the main text and SI}.'),
            ('在 SI 中加一节 ``On the Role of Assumption A2\'\'', 'Add a Section ``On the Role of Assumption A2\'\' in the SI,'),
            ('内容: 1. A2 实际上是 A1 的推论（不相交训练集 → 独立专家 → 独立错误） 2.\n概率空间是训练随机性，不是测试行为 3. 有限样本下 \\(\\mu_s\\)\n的估计误差有独立处理（推论 4） 4.\n在实践中，专家错误可能表现出表面相关（同一张模糊图），但这反映的是特征相似性导致相似的\n\\(\\mu_s\\)，而非统计相关性 5. 对 A2 的经验诊断:\n在验证集上估计专家错误的条件相关系数；如果显著偏离零，检查训练集是否真的不相交',
             'Contents: 1. A2 is actually a corollary of A1 (disjoint training sets → independent experts → independent errors) 2.\nThe probability space is training randomness, not test behavior 3. The estimation error of \\(\\mu_s\\)\nin finite samples is handled separately (Corollary 4) 4.\nIn practice, expert errors may exhibit superficial correlation (same blurry image), but this reflects similar \\(\\mu_s\\) values due to feature similarity, not statistical dependence 5. Empirical diagnosis of A2:\nEstimate conditional correlation coefficients of expert errors on a validation set; if they deviate significantly from zero, check whether training sets were truly disjoint'),
            ('在正文中诚实措辞', 'Honest Wording in the Main Text'),
            ('把 ``conditional independence\'\' 改为: \\textgreater{} ``conditional\nindependence of expert errors, which follows from training on disjoint\ndata subsets (Assumption A1)\'\'',
             'Change ``conditional independence\'\' to: \\textgreater{} ``conditional\nindependence of expert errors, which follows from training on disjoint\ndata subsets (Assumption A1)\'\''),
            ('这样把 A2 从\'\'假设\'\'降级为\'\'A1 的逻辑结果\'\'，同时指出它依赖于 A1\n的正确执行。',
             'This downgrades A2 from ``assumption\'\' to ``logical consequence of A1,\'\' while noting that it depends on the correct execution of A1.'),
            ('最终判断', 'Final Judgment'),
            ('A2 是否站得住？', 'Does A2 hold up?'),
            ('\\textbf{是} --- A1 蕴含 A2（训练集不相交 → 专家独立）', '\\textbf{Yes} --- A1 implies A2 (disjoint training sets → independent experts)'),
            ('在实践中是否违反？', 'Is it violated in practice?'),
            ('\\textbf{取决于 A1 的执行} --- 如果训练集真的不相交，A2 成立', '\\textbf{Depends on A1 execution} --- if training sets are truly disjoint, A2 holds'),
            ('\\(\\exp(-2M\\Delta^2/(1+(M-1)\\rho))\\) 是否严格？', 'Is \\(\\exp(-2M\\Delta^2/(1+(M-1)\\rho))\\) rigorous?'),
            ('\\textbf{否} --- 这是启发式，不应写进定理', '\\textbf{No} --- this is a heuristic and should not appear in theorems'),
            ('应该如何修改？', 'How should it be revised?'),
            ('澄清 A2 是 A1 的推论；在 SI 中加入诚实讨论；不要引入虚假的 A2\'', 'Clarify that A2 is a corollary of A1; add honest discussion in SI; do not introduce a fake A2\''),
            ('对论文的影响程度', 'Impact on the paper'),
            ('\\textbf{低} --- 不需要改定理陈述，只需要加一段诚实讨论', '\\textbf{Low} --- no need to change theorem statements, just add a paragraph of honest discussion'),
            ('对 hostile review 其他批评的回应', 'Response to Other Criticisms from the Hostile Review'),
            ('``CIFAR F1=0.617, 理论下界 F1≥0.976\'\'', '``CIFAR F1=0.617, theoretical lower bound F1≥0.976\'\''),
            ('这已经在 §4.3（紧致性讨论）中诚实处理了: \\(\\mu_s\\) 在 CIFAR 实验中约为\n0.45（3-epoch CPU 训练后），而非假定的 0.20。代入正确的 \\(\\mu_s\\)\n后下界为 F1≥0.18，与经验值 0.617 一致。',
             'This has already been honestly addressed in §4.3 (tightness discussion): \\(\\mu_s\\) in the CIFAR experiment is approximately\n0.45 (after 3-epoch CPU training), not the assumed 0.20. Plugging in the correct \\(\\mu_s\\)\ngives a lower bound of F1≥0.18, consistent with the empirical value 0.617.'),
            ('``\\(\\mu_s\\) 需要清洁标签 → 鸡生蛋\'\'', '``\\(\\mu_s\\) requires clean labels → chicken-and-egg\'\''),
            ('冷启动协议需要少量锚点样本（推论 1），这是理论上的必要成本（Thm 3\n证明了没有锚点时不可识别）。这不是循环定义------是对不可识别性定理的工程回应。',
             'The cold-start protocol requires a small number of anchor samples (Corollary 1), which is a theoretically necessary cost (Thm 3\nproves unidentifiability without anchors). This is not a circular definition --- it is an engineering response to the unidentifiability theorem.'),
            ('``Bootstrap 诊断的 τ=0.7 是拍脑袋\'\'', '``Bootstrap diagnostic τ=0.7 is arbitrary\'\''),
            ('承认。\\(\\tau=0.7\\) 是初始校准值，应在具体领域中根据已知噪声标签校准。SI\n中应明确标注为\'\'建议初始值，需领域校准\'\'。',
             'Acknowledged. \\(\\tau=0.7\\) is an initial calibration value that should be calibrated against known noisy labels in specific domains. The SI\nshould explicitly label it as ``suggested initial value, requires domain calibration.\'\''),
        ]
    
    return t


# ── Main ──
for rel_path in FILES:
    fp = os.path.join(BASE, rel_path)
    if not os.path.exists(fp):
        print(f'MISSING: {fp}')
        continue
    
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    before = len(cn_re.findall(content))
    content = global_fixes(content)
    
    trans = get_translations(rel_path)
    if trans:
        trans.sort(key=lambda x: -len(x[0]))
        for old, new in trans:
            if old in content:
                content = content.replace(old, new)
    
    after = len(cn_re.findall(content))
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'{os.path.basename(rel_path)}: {before} -> {after} CN ({before-after} removed)')

print('\nDone.')
