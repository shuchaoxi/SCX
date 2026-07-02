#!/usr/bin/env python3
"""
Step 5: Targeted Chinese->English translation for the 8 remaining files.
Only translates visible text content (headings, body paragraphs, table cells).
Preserves all LaTeX commands, math, labels, and references.
"""
import re, os

BASE = r"F:\scx"

# Complete translation for ALL remaining Chinese text, file by file.
# These are the exact Chinese text strings found in each file.

FILE_TRANSLATIONS = {}

# ====== 01_noise_detection_guarantee.tex ======
FILE_TRANSLATIONS['01_noise_detection_guarantee.tex'] = {
    # Title and section headings
    'Theorem 1: Multi-Expert Consistency Guarantees for Label Noise\nDetection': 
    'Theorem 1: Multi-Expert Consistency Guarantees for Label Noise\nDetection',
    # Already English - OK
    
    # Blockquote
    '核心主张': 'Core Claim',
    '当 \\(M\\) 个在不相交数据子集上独立训练的专家对某个样本的一致性得分 \\(C(x)\\) 超过阈值 \\(\\theta\\) 时，该样本是标签噪声的置信度以指数速率收敛到 1。':
    'When the consistency score \\(C(x)\\) of \\(M\\) experts trained on disjoint data subsets exceeds threshold \\(\\theta\\) for a sample, the confidence that the sample contains label noise converges to 1 at an exponential rate.',
    
    '修正记录': 'Revision History',
    'Lemma 3 证明重构（新增 A6 平衡误差分布假设）；Chernoff 附录 KL 方向修正；主定理陈述更新为 (A1)-(A6)。两个 bug 均来自验证报告。':
    'Lemma 3 proof restructured (added A6 balanced error distribution assumption); Chernoff appendix KL direction corrected; main theorem statement updated to (A1)-(A6). Both bugs from the verification report.',
    
    '定理陈述': 'Theorem Statement',
    '符号与设定 (Setup)': 'Notation and Setup',
    '设以下对象：': 'Define the following objects:',
    '符号': 'Symbol',
    '含义': 'Meaning',
    '输入空间，可测': 'Input space, measurable',
    '标签空间，\\(|\\mathcal{Y}| = K\\)（分类）或 \\(\\mathcal{Y} \\subseteq \\mathbb{R}^d\\)（回归）': 
    'Label space, \\(|\\mathcal{Y}| = K\\) (classification) or \\(\\mathcal{Y} \\subseteq \\mathbb{R}^d\\) (regression)',
    '数据分布，\\((X, Y) \\sim \\mathcal{D}\\)': 'Data distribution, \\((X, Y) \\sim \\mathcal{D}\\)',
    '真实标注函数（未知 Oracle）': 'True labeling function (unknown Oracle)',
    '\\(M\\) 个专家模型，\\(f_m : \\mathcal{X} \\to \\mathcal{Y}\\)': '\\(M\\) expert models, \\(f_m : \\mathcal{X} \\to \\mathcal{Y}\\)',
    '状态划分，\\(\\mathcal{X}\\) 的可测分割': 'State partition, a measurable partition of \\(\\mathcal{X}\\)',
    '有界损失函数': 'Bounded loss function',
    '专家错误的阈值': 'Expert error threshold',
    '噪声检测阈值': 'Noise detection threshold',
    
    '标签噪声模型': 'Label Noise Model',
    '对于每个样本 \\((x, y^*)\\)（其中 \\(y^* = f^*(x)\\) 为真实标签），观察到的标签 \\(y\\) 生成如下：':
    'For each sample \\((x, y^*)\\) (where \\(y^* = f^*(x)\\) is the true label), the observed label \\(y\\) is generated as follows:',
    '以概率': 'with probability',
    '全局噪声率，噪声事件与 \\(x\\) 和所有训练数据独立。': 'is the global noise rate; noise events are independent of \\(x\\) and all training data.',
    '一致性得分': 'Consistency Score',
    '对样本 \\((x, y)\\)，定义专家错误指示变量和一致性得分：': 'For sample \\((x, y)\\), define the expert error indicator and consistency score:',
    '检测规则': 'Detection Rule',
    '样本 \\((x, y)\\) 被标记为噪声当且仅当 \\(C(x) > \\theta\\)。': 'Sample \\((x, y)\\) is flagged as noise if and only if \\(C(x) > \\theta\\).',
    
    '假设 (Assumptions)': 'Assumptions',
    '不相交训练集': 'Disjoint Training Sets',
    '个专家在': 'experts are trained on',
    '个不相交的独立同分布子集上训练：': 'disjoint i.i.d. subsets:',
    
    '清洁数据上的条件独立': 'Conditional Independence on Clean Data',
    '对任意清洁样本 \\((x, y)\\)（\\(y = y^*\\)），给定 \\(x\\) 的条件下，错误指示变量 \\(\\{e_m(x, y)\\}_{m=1}^M\\) 是条件独立的。':
    'For any clean sample \\((x, y)\\) (where \\(y = y^*\\)), given \\(x\\), the error indicators \\(\\{e_m(x, y)\\}_{m=1}^M\\) are conditionally independent.',
    
    '合理性说明与局限': 'Justification and Limitations',
    'A2 是一种结构性假设，由专家实验设计（不相交训练集 A1、独立初始化）所论证，但 A1 并不蕴含 A2。即使训练集完全不相交，在相似数据分布上训练的专家可能在分布外样本上产生相关错误（源于共享归纳偏置，非共享训练数据）。因此 A2 在 SCX 流水线的数据中不可经验检验------对连续输入空间 \\(\\mathcal{X}\\)，每个 \\(x\\) 在有限数据集中最多出现一次，联合分布 \\(P(e_1, \\dots, e_M \\mid x)\\) 不可观测。':
    'A2 is a structural assumption, justified by expert experimental design (disjoint training sets A1, independent initialization), but A1 does not imply A2. Even with fully disjoint training sets, experts trained on similar data distributions may exhibit correlated errors on out-of-distribution samples (due to shared inductive bias, not shared training data). Thus A2 cannot be empirically tested in SCX pipeline data --- for continuous input space \\(\\mathcal{X}\\), each \\(x\\) appears at most once in a finite dataset, making the joint distribution \\(P(e_1, \\dots, e_M \\mid x)\\) unobservable.',
    
    '当 A2 被违反时（实际中常见）：用 \\(M_{\\text{eff}} = M/(1 + (M-1)\\bar{\\rho})\\) 替换所有集中不等式中的 \\(M\\)，其中 \\(\\bar{\\rho}\\) 为专家错误指标的平均成对相关性。对典型深度集成，\\(\\bar{\\rho} \\approx 0.1\\)--\\(0.3\\)。建议在留置验证集上估计 \\(\\bar{\\rho}\\)，并用 \\(M_{\\text{eff}}\\) 得到保守保证。详细分析参见 \\texttt{01\\_symbol\\_system.md} §12.5。':
    'When A2 is violated (common in practice): replace \\(M\\) in all concentration inequalities with \\(M_{\\text{eff}} = M/(1 + (M-1)\\bar{\\rho})\\), where \\(\\bar{\\rho}\\) is the average pairwise correlation of expert error indicators. For typical deep ensembles, \\(\\bar{\\rho} \\approx 0.1\\)--\\(0.3\\). It is recommended to estimate \\(\\bar{\\rho}\\) on a held-out validation set and use \\(M_{\\text{eff}}\\) to obtain conservative guarantees. See \\texttt{01\\_symbol\\_system.md} §12.5 for detailed analysis.',
    
    '有界损失': 'Bounded Loss',
    '均匀独立噪声': 'Uniform Independent Noise',
    '标签翻转事件与 \\(x\\) 和所有 \\(D_m\\) 独立。噪声标签在 \\(\\mathcal{Y} \\setminus \\{y^*\\}\\) 上均匀分布。':
    'Label flip events are independent of \\(x\\) and all \\(D_m\\). Noise labels are uniformly distributed over \\(\\mathcal{Y} \\setminus \\{y^*\\}\\).',
    
    '状态同质性 (状态划分充分性)': 'State Homogeneity (State Partition Sufficiency)',
    '状态划分 \\(\\Pi\\) 使得在每个状态 \\(s\\) 内，专家的清洁数据错误率近似均匀。形式化地，存在状态级常数 \\(\\{\\mu_s\\}_{s \\in \\mathcal{S}}\\) 使得：':
    'The state partition \\(\\Pi\\) ensures that within each state \\(s\\), the experts clean-data error rates are approximately uniform. Formally, there exist state-level constants \\(\\{\\mu_s\\}_{s \\in \\mathcal{S}}\\) such that:',
    '即状态 \\(s\\) 内清洁样本的平均专家错误率被 \\(\\mu_s\\) 一致上界控制。': 'That is, the average expert error rate for clean samples within state \\(s\\) is uniformly bounded above by \\(\\mu_s\\).',
    
    '平衡误差分布': 'Balanced Error Distribution',
    '专家的错误概率在所有错误类别上不能过度集中。存在常数 \\(C_{\\text{bal}} \\geq 1\\) 使得对任意状态 \\(s\\) 和 \\(x \\in s\\)：':
    'The expert error probabilities cannot be excessively concentrated on any particular error class. There exists a constant \\(C_{\\text{bal}} \\geq 1\\) such that for any state \\(s\\) and \\(x \\in s\\):',
    '\\(C_{\\text{bal}} = 1\\) 对应完全均匀的错误分布（每个错误类别等概率）；\\(C_{\\text{bal}} = 2\\) 是典型的保守选择。此假设可检验且在实践中几乎自动满足------在不相交干净数据上训练的专家没有理由将错误集中到特定类别。':
    '\\(C_{\\text{bal}} = 1\\) corresponds to completely uniform error distribution (each error class equiprobable); \\(C_{\\text{bal}} = 2\\) is a typical conservative choice. This assumption is testable and almost automatically satisfied in practice --- experts trained on disjoint clean data have no reason to concentrate errors on particular classes.',
    
    '关键引理 (均值分离)': 'Key Lemma (Mean Separation)',
    'Lemma 1 (Mean Separation)': 'Lemma 1 (Mean Separation)',
    '在假设 (A1)-(A5) 下（A6 不影响期望），对任意 \\(x \\in s\\)：': 'Under assumptions (A1)-(A5) (A6 does not affect expectations), for any \\(x \\in s\\):',
    '清洁样本': 'Clean Samples',
    '噪声样本': 'Noise Samples',
    '分离间隙': 'Separation Gap',
    '当选择最优阈值': 'When choosing the optimal threshold',
    '时，分离间隙最大化（在 \\(C_{\\text{bal}}=1\\) 的理想情况下）：': ', the separation gap is maximized (in the ideal case of \\(C_{\\text{bal}}=1\\)):',
    '当 \\(C_{\\text{bal}} > 1\\) 时，最优阈值向 \\(\\mu_s\\) 方向微调以补偿非均匀误差分布。\\(\\theta_s^*\\) 的精确表达式需求解 \\(\\theta - \\mu_s = 1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1) - \\theta\\)。':
    'When \\(C_{\\text{bal}} > 1\\), the optimal threshold is fine-tuned toward \\(\\mu_s\\) to compensate for non-uniform error distribution. The exact expression for \\(\\theta_s^*\\) requires solving \\(\\theta - \\mu_s = 1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1) - \\theta\\).',
    
    'Proof.': 'Proof.',
    '对 0-1 损失': 'for 0-1 loss',
    
    '主定理 (Main Result)': 'Main Theorem (Main Result)',
    'Theorem 1 (SCX 噪声检测保证)': 'Theorem 1 (SCX Noise Detection Guarantee)',
    '设假设 (A1)-(A6) 成立，且 \\(M \\geq 1\\)（至少一个专家），\\(K \\geq 2\\)（至少两个标签类别，以保证 \\(K-1 > 0\\)）。令 \\(\\rho_s = \\mathbb{P}(X \\in s)\\) 为状态概率。对任意阈值 \\(\\theta\\) 满足 \\(\\mu_s < \\theta < 1 - C_{\\text{bal}} \\cdot \\frac{\\mu_s}{K-1}\\) 的状态 \\(s\\)，定义状态级分离间隙：':
    'Let assumptions (A1)-(A6) hold, with \\(M \\geq 1\\) (at least one expert) and \\(K \\geq 2\\) (at least two label classes, ensuring \\(K-1 > 0\\)). Let \\(\\rho_s = \\mathbb{P}(X \\in s)\\) be the state probability. For any threshold \\(\\theta\\) satisfying \\(\\mu_s < \\theta < 1 - C_{\\text{bal}} \\cdot \\frac{\\mu_s}{K-1}\\) for state \\(s\\), define the state-level separation gap:',
    '当 \\(C_{\\text{bal}} = 1\\)（最佳情形）时，\\(\\Delta_s\\) 恢复原始定义；当 \\(C_{\\text{bal}} > 1\\) 时，噪声侧的间隙收窄（因为错误可能不是完全均匀分布的）。':
    'When \\(C_{\\text{bal}} = 1\\) (best case), \\(\\Delta_s\\) recovers the original definition; when \\(C_{\\text{bal}} > 1\\), the noise-side gap narrows (because errors may not be perfectly uniformly distributed).',
    '则 SCX 噪声检测器的 F1 得分满足以下下界：': 'Then the SCX noise detectors F1 score satisfies the following lower bound:',
    '或等价地：': 'or equivalently:',
    '更紧的 Chernoff 形式': 'Tighter Chernoff Form',
    '对相同设定，使用 Chernoff 界代替 Hoeffding 可得更紧的指数速率：': 'For the same setting, using the Chernoff bound instead of Hoeffding yields a tighter exponential rate:',
    '2026-06-27 修正：原版 Chernoff 使用了 \\(\\text{KL}(1-\\theta \\| 1 - \\mu_s/(K-1))\\)，KL 方向有误，且未纳入 \\(C_{\\text{bal}}\\)。现已修正为 \\(\\text{KL}(\\theta \\| 1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1))\\)。':
    '2026-06-27 correction: The original Chernoff used \\(\\text{KL}(1-\\theta \\| 1 - \\mu_s/(K-1))\\) with incorrect KL direction and did not incorporate \\(C_{\\text{bal}}\\). Now corrected to \\(\\text{KL}(\\theta \\| 1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1))\\).',
    
    '关键推论': 'Key Corollary',
    '当 \\(M \\to \\infty\\) 时，对所有满足 \\(\\mu_s < \\frac{K-1}{K}\\) 的状态，F1 以指数速率收敛到 1：':
    'As \\(M \\to \\infty\\), for all states satisfying \\(\\mu_s < \\frac{K-1}{K}\\), F1 converges to 1 at an exponential rate:',
    '最差状态分离间隙': 'worst-case state separation gap',
    
    # Section 2
    '清洁数据的假阳性率 (False Positive Rate)': 'False Positive Rate on Clean Data',
    'Lemma 2 (FPR 上界)': 'Lemma 2 (FPR Upper Bound)',
    '清洁样本被误标为噪声的概率满足：': 'The probability that a clean sample is incorrectly flagged as noise satisfies:',
    
    # Section 2.2
    '噪声数据的真阳性率 (True Positive Rate)': 'True Positive Rate on Noisy Data',
    '新增假设 (A6) --- 平衡误差分布': 'New Assumption (A6) --- Balanced Error Distribution',
    '合理性': 'Justification',
    '专家在不相交的干净数据子集上训练，没有理由将错误集中到特定的错误类别。均匀噪声模型下，每个错误类别的概率天然约为 \\(\\mu_s/(K-1)\\)。\\(C_{\\text{bal}} = 2\\) 已是保守选择。此假设可检验：在实际数据上估计 \\(\\max_c \\mu_c(x) / (\\mu_s/(K-1))\\)。':
    'Experts trained on disjoint clean data subsets have no reason to concentrate errors on specific error classes. Under the uniform noise model, the probability of each error class is naturally approximately \\(\\mu_s/(K-1)\\). \\(C_{\\text{bal}} = 2\\) is already a conservative choice. This assumption is testable: estimate \\(\\max_c \\mu_c(x) / (\\mu_s/(K-1))\\) on real data.',
    
    'Lemma 3 (TPR 下界)': 'Lemma 3 (TPR Lower Bound)',
    '噪声样本被正确检测的概率满足：': 'The probability that a noisy sample is correctly detected satisfies:',
    '证明': 'Proof',
    
    '注记': 'Note',
    '当 \\(C_{\\text{bal}} = 1\\)（完全均匀的错误分布）时，Lemma 3 恢复原始命题中的最优 bound。\\(C_{\\text{bal}}\\) 可在实际数据上估计，并用于校准检测阈值 \\(\\theta\\)。':
    'When \\(C_{\\text{bal}} = 1\\) (completely uniform error distribution), Lemma 3 recovers the optimal bound from the original proposition. \\(C_{\\text{bal}}\\) can be estimated on real data and used to calibrate the detection threshold \\(\\theta\\).',
    
    # Section 2.3
    'F1 下界': 'F1 Lower Bound',
    '现在组合 Lemma 2 和 Lemma 3 推导 F1 下界。': 'Now combine Lemma 2 and Lemma 3 to derive the F1 lower bound.',
    '令检测规则为': 'Let the detection rule be',
    '定义：': 'Define:',
    '由 (A4)，噪声事件与 \\(X\\) 独立，因此 \\(\\mathbb{P}(\\text{noise} \\mid X \\in s) = \\eta\\) 对所有状态成立。整体 TPR 和 FPR 为：':
    'By (A4), noise events are independent of \\(X\\), so \\(\\mathbb{P}(\\text{noise} \\mid X \\in s) = \\eta\\) holds for all states. The overall TPR and FPR are:',
    'F1 得分为：': 'The F1 score is:',
    '代入 TPR \\(\\geq 1 - \\delta_1\\) 和 FPR \\(\\leq \\delta_2\\)，其中：': 'Substituting TPR \\(\\geq 1 - \\delta_1\\) and FPR \\(\\leq \\delta_2\\), where:',
    '得到：': 'we obtain:',
    '因分母': 'since the denominator',
    '代入 \\(\\delta_1, \\delta_2\\) 的表达式，并注意当 \\(\\Delta_s = \\min(\\theta - \\mu_s, \\; 1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1) - \\theta)\\) 时有 \\(\\exp(-2M(\\theta - \\mu_s)^2) \\leq \\exp(-2M\\Delta_s^2)\\) 和 \\(\\exp(-2M(1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1) - \\theta)^2) \\leq \\exp(-2M\\Delta_s^2)\\)，因此：':
    'Substituting the expressions for \\(\\delta_1, \\delta_2\\), and noting that when \\(\\Delta_s = \\min(\\theta - \\mu_s, \\; 1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1) - \\theta)\\) we have \\(\\exp(-2M(\\theta - \\mu_s)^2) \\leq \\exp(-2M\\Delta_s^2)\\) and \\(\\exp(-2M(1 - C_{\\text{bal}} \\cdot \\mu_s/(K-1) - \\theta)^2) \\leq \\exp(-2M\\Delta_s^2)\\), therefore:',
    
    # Section 3
    '推论 (Corollaries)': 'Corollaries',
    '推论 1：对称专家 (Symmetric Experts)': 'Corollary 1: Symmetric Experts',
    '当所有专家具有相同的清洁数据错误率 \\(\\varepsilon\\)（称为对称专家）时，\\(\\mu_s = \\varepsilon\\) 对所有状态一致。此时：':
    'When all experts have the same clean-data error rate \\(\\varepsilon\\) (called symmetric experts), \\(\\mu_s = \\varepsilon\\) uniformly for all states. Then:',
    '且 F1 下界简化为：': 'and the F1 lower bound simplifies to:',
    '当 \\(K = 2\\)（二分类）时，进一步简化为：': 'When \\(K = 2\\) (binary classification), this further simplifies to:',
    '意义': 'Significance',
    '在二分类对称专家场景下，检测质量完全由专家错误率 \\(\\varepsilon\\) 与 \\(1/2\\) 的差距决定。\\(\\varepsilon\\) 每远离 \\(1/2\\) 一个标准差（\\(\\approx 1/\\sqrt{2M}\\)），F1 下界提升一个指数数量级。':
    'In the binary classification symmetric expert scenario, detection quality is entirely determined by the gap between the expert error rate \\(\\varepsilon\\) and \\(1/2\\). For each standard deviation that \\(\\varepsilon\\) moves away from \\(1/2\\) (\\(\\approx 1/\\sqrt{2M}\\)), the F1 lower bound improves by an exponential order of magnitude.',
    
    '推论 2：最优阈值选择 (Optimal Threshold)': 'Corollary 2: Optimal Threshold Selection',
    '对给定的噪声率 \\(\\eta\\)、类别数 \\(K\\)、专家数 \\(M\\) 和最大清洁错误率 \\(\\mu_{\\max} = \\max_s \\mu_s\\)，最优检测阈值 \\(\\theta^*\\) 应满足：':
    'For a given noise rate \\(\\eta\\), number of classes \\(K\\), number of experts \\(M\\), and maximum clean error rate \\(\\mu_{\\max} = \\max_s \\mu_s\\), the optimal detection threshold \\(\\theta^*\\) should satisfy:',
    '此时最小分离间隙为：': 'The minimum separation gap is then:',
    '所需的最少专家数（达到 F1 \\(\\geq 1 - \\varepsilon_0\\)）为：': 'The minimum number of experts required (to achieve F1 \\(\\geq 1 - \\varepsilon_0\\)) is:',
    '直接解 \\(1 - \\frac{1}{\\eta}e^{-2M\\Delta^2} \\geq 1 - \\varepsilon_0\\) 得 \\(e^{-2M\\Delta^2} \\leq \\eta\\varepsilon_0\\)，取对数即得。若需同时控制多个状态的误差（联合界），分子中的 \\(1\\) 替换为状态数 \\(|\\mathcal{S}|\\)。':
    'Directly solving \\(1 - \\frac{1}{\\eta}e^{-2M\\Delta^2} \\geq 1 - \\varepsilon_0\\) gives \\(e^{-2M\\Delta^2} \\leq \\eta\\varepsilon_0\\), taking the logarithm yields the result. If errors for multiple states need simultaneous control (union bound), replace \\(1\\) in the numerator with the number of states \\(|\\mathcal{S}|\\).',
    
    '推论 3：一致可检测的充分条件 (Uniform Detectability)': 'Corollary 3: Sufficient Condition for Uniform Detectability',
    '如果存在 \\(\\delta > 0\\) 使得对所有状态 \\(s\\) 有 \\(\\mu_s \\leq \\frac{K-1}{K} - \\delta\\)，则令 \\(\\theta = \\frac{1}{2}\\)（固定阈值），对所有状态有 \\(\\Delta_s \\geq \\frac{\\delta}{2}\\)，且：':
    'If there exists \\(\\delta > 0\\) such that for all states \\(s\\) we have \\(\\mu_s \\leq \\frac{K-1}{K} - \\delta\\), then setting \\(\\theta = \\frac{1}{2}\\) (fixed threshold), we have \\(\\Delta_s \\geq \\frac{\\delta}{2}\\) for all states, and:',
}

print("Translation dictionary built successfully.")
print(f"Number of entries: {sum(len(v) for v in FILE_TRANSLATIONS.values())}")
