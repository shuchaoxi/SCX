#!/usr/bin/env python3
"""Second-pass: more aggressive Chinese-to-English translation for Batch B tex files."""

import re
import os

# More aggressive replacements for remaining Chinese patterns
MORE_REPLACEMENTS = [
    # Fix partial matches from first pass
    ('设 \\(M\\) 个专家', 'Given \\(M\\) experts'),
    ('融合预测provides', 'the ensemble prediction is'),
    ('(\\\\text{全局固定})', '(\\\\text{globally fixed})'),
    ('风险provides', 'The risk is'),
    ('不is全局constant', 'are not global constants'),
    ('whileisStatus条件函数', 'but state-conditioned functions'),
    ('with respect to the Wasserstein metric充分统计量或and其近似', 'is a sufficient statistic or approximates it'),
    ('（原Arrow类比已归档）', '(original Arrow analogy has been archived)'),
    ('\\{符号\\}', 'Symbol'),
    ('\\{含义\\}', 'Meaning'),
    ('\\{类型\\}', 'Type'),
    ('\\{文件\\}', 'File'),
    ('\\{内容\\}', 'Content'),
    ('\\{状态\\}', 'Status'),
    ('\\{定理\\}', 'Theorem'),
    ('\\{命题\\}', 'Proposition'),
    ('\\{数量\\}', 'Quantity'),
    ('\\{领域\\}', 'Domain'),
    ('\\{动作\\}', 'Action'),
    
    # Remaining Chinese characters
    ('个专家', ' experts'),
    ('个状态', ' states'),
    ('个样本', ' samples'),
    ('个构型', ' configurations'),
    ('个描述符', ' descriptors'),
    ('个维度', ' dimensions'),
    ('个方向', ' directions'),
    ('个假设', ' assumptions'),
    ('个定理', ' theorems'),
    ('个命题', ' propositions'),
    ('个专家', ' experts'),
    ('个场景', ' scenarios'),
    ('个透镜', ' lenses'),
    ('个信息集', ' information sets'),
    ('个审计者', ' auditors'),
    ('个配置', ' configurations'),
    ('个边界', ' boundaries'),
    
    # Fix "with respect to the Wasserstein metric" that got inserted incorrectly
    ('with respect to the Wasserstein metric', ''),
    ('  ', ' '),  # clean double spaces
    ('  ', ' '),
    
    # Remaining section titles
    ('数学框架总览', 'Mathematical Framework Overview'),
    ('最后Update', 'Last Updated'),
    ('Question题', 'Problem'),
    ('Given M 个专家', 'Given M experts'),
    ('Input空间', 'Input space'),
    ('标签空间', 'Label space'),
    ('多专家系统with的可靠性', 'the reliability of multi-expert systems'),
    ('到Data价值定义', 'to the definition of data value'),
    ('SCX mathematical foundations', 'SCX Mathematical Foundations'),
    ('数学Analysis', 'Mathematical Analysis'),
    ('核心framework', 'Core Framework'),
    ('数学根源and证明', 'Mathematical Roots and Proofs'),
    ('Derivation SCX-Compress 模块', 'Derivation of the SCX-Compress module'),
    ('compression保真Theorem', 'compression fidelity theorem'),
    ('安全compression比condition', 'safe compression ratio conditions'),
    ('andand经典 coreset 理论', 'and classical coreset theory'),
    ('Status空间', 'State space'),
    ('via SCX 聚类划分', 'via SCX clustering partition'),
    ('单个Status', 'a single state'),
    ('形式化定义', 'Formal Definition'),
    ('SCX/EGP 蒸馏前专家规范化协议', 'SCX/EGP Pre-Distillation Expert Governance Protocol'),
    ('版本:v1.0', 'Version: v1.0'),
    ('最后Update:2026-06-26', 'Last updated: 2026-06-26'),
    ('目录', 'Table of Contents'),
    ('不isguaranteed by人类预设', 'is not pre-specified by humans'),
    ('whileisUnder误差特征子空间自动发现', 'but is automatically discovered in the error-relevant feature subspace'),
    ('Status应guaranteed by', 'States should be defined by'),
    ('ModelUnder哪里失败', 'where the model fails'),
    ('来定义,while非', 'not by'),
    ('人类觉we get什么重要', 'what humans think is important'),
    ('Status应该Underand', 'States should be clustered in the subset of'),
    ('最with的', 'most relevant to'),
    ('Dimension子集聚类', 'dimensions'),
    
    # 8theorems review
    ('8篇Theorem论文数学Complete性审查报告', 'SCX 8-Theorem Paper Mathematical Completeness Audit Report'),
    ('Multi-expert consensus noise detection --- UnderA1-A6Assume下', 'Multi-expert consensus noise detection --- Under assumptions A1-A6'),
    ('指数convergent', 'exponentially convergent'),
    ('From观测DataNone法区分标签噪声and内Under难度', 'No algorithm operating on observed data can distinguish label noise from intrinsic difficulty'),
    ('ThisisSCX', 'This is SCX\'s'),
    ('Uncertainty Principle', 'Uncertainty Principle'),
    ('Bahadur-Rao大bias精确constant', 'Bahadur-Rao large deviation exact constant'),
    
    # SCX_Next_Theorems
    ('2026年6月29日', 'June 29, 2026'),
    ('SE-1(dynamic evolution), Situs(spatial encoding)构成Complete', 'SE-1 (dynamic evolution) and Situs (spatial encoding) form a complete'),
    ('基础理论体系', 'foundational theoretical system'),
    ('一, 因果发现Theorem:标签噪声 vs.', '1. Causal Discovery Theorem: Label Noise vs.'),
    ('因果混淆with的可分离性', 'Causal Confounding Separability'),
    ('3(Uncertainty Principle)asserts:UnderSCX审计framework内', 'Theorem 3 (Uncertainty Principle) asserts: within the SCX audit framework'),
    ('噪声and固we have困难不可区分', 'noise and intrinsic difficulty are indistinguishable'),
    ('Formally,GivenCercis', 'Formally, given the Cercis'),
    
    # SCX_Undiscovered_Theorems
    ('Task:Under已we haveT1-T7基础Theorem + CD/FA/AR/TS/HC五方向Draft之上,深究is否还we have未覆盖', 'Task: Building on the existing T1-T7 fundamental theorems + CD/FA/AR/TS/HC five draft directions, deeply investigate whether there are still uncovered'),
    ('理论盲区', 'theoretical blind spots'),
    ('以下五个方向按', 'The following five directions are ranked by'),
    ('最具发现潜力', 'discovery potential'),
    ('排序,每个givesCompleteTheorem陈述草稿并诚实Annotation可推性', 'each with a complete theorem statement draft and honest annotation of derivability'),
    ('一, 量子SCXTheorem:量子传感下with的远程审计andTheorem 3with的量子Corrected', '1. Quantum SCX Theorem: Remote Audit under Quantum Sensing and Quantum Correction of Theorem 3'),
    
    # CERCIS_NAMING
    ('紫荆花算法', 'Cercis Algorithm'),
    ('正式名称', 'Formal name'),
    ('目标期刊', 'Target journal'),
    ('两篇论文策略中的第二篇', 'Paper 2 of two-paper strategy'),
    ('紫荆', 'Cercis chinensis'),
    ('茎花植物', 'cauliflorous tree'),
    
    # Final reviews
    ('保存日期:2026-06-29', 'Date saved: 2026-06-29'),
    ('个Independent专家', ' independent experts'),
    ('有效IndependentDimension ≈', ' effective independent dimension ≈'),
    ('Medical imaging δ', 'Medical imaging δ'),
    ('自相', 'is self-contradictory'),
    ('registration error dominant failure vs', 'registration error dominant failure vs'),
    ('忽略区域Differenceand卫星Data', 'ignores regional differences and satellite data'),
    ('TCAD/OPC:M', 'TCAD/OPC: M'),
    ('仍宣称we have意义', 'still claims significance'),
    
    # Hostile review
    ('理论with的逐行Attack', 'Line-by-Line Attack on Situs Theory'),
    ('最苛刻with的审稿人', 'the most demanding reviewer'),
    ('审稿auditing象', 'Review target'),
    ('不礼貌.不妥协.只要we have一个漏洞就不放过.', 'Impolite. Uncompromising. Not a single gap goes unpunished.'),
    ('This篇The paper claimsUnder一个叫SCXwith的framework上建立了Situs(物理Locationencoding)', 'This paper claims to have established rigorous mathematical foundations for Situs (physical position encoding) on a framework called SCX'),
    ('with的严格数学基础', ''),
    ('实际读完三份文档后with的Conclusionis', 'After actually reading the three documents, the conclusion is'),
    ('This篇文章Under多个核心Theoremwith的证明上存Under根本性Error或None法修复with的Logical Gaps', 'This paper has fundamental errors or irreparable logical gaps in the proofs of multiple core theorems'),
    ('Theorem', 'Theorem'),
    
    # Mathematical Genealogy
    ('Spring (春季)', 'Spring'),
    ('地位', 'Status'),
    ('目标', 'target'),
    ('核心算法', 'core algorithm'),
    ('文档Type', 'Document type'),
    ('理论根源追溯 --- Mathematical Domain Attribution, 关键思想来源, 历史发展脉络, and前人工作with的auditing比', 'Tracing theoretical roots --- mathematical domain attribution, key idea sources, historical development, and comparison with prior work'),
    ('日期', 'Date'),
    ('2026-06-28', '2026-06-28'),
    
    # Clean up broken patterns
    ('with的', ''),
    ('with的', ''),
    ('andand', 'and'),
    ('is否', 'whether'),
    ('已we have', 'existing'),
    ('未覆盖', 'uncovered'),
    ('None法', 'cannot be'),
    ('存Under', 'exist in'),
    ('an called', 'a framework called'),
    ('and其', 'and its'),
    ('or为', 'or is'),
    
    # More fixes
    ('可检验', 'testable'),
    ('审计framework', 'audit framework'),
    ('内Under', 'intrinsic'),
    ('固we have', ''),
]

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for pattern, replacement in MORE_REPLACEMENTS:
        content = content.replace(pattern, replacement)
    
    # Clean up multiple spaces
    content = re.sub(r' {3,}', '  ', content)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # Fix broken LaTeX patterns
    content = content.replace('andand', 'and')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

files = [
    'theory/propositions/03_state_conditioned_weighting.tex',
    'theory/propositions/03_state_conditioned_weighting_proof.tex',
    'theory/propositions/04_compression_fidelity.tex',
    'theory/propositions/05_expert_governance_protocol.tex',
    'theory/propositions/06_two_layer_state_discovery.tex',
    'theory/README.tex',
    'theory/scx_8theorems_review.tex',
    'theory/SCX_Next_Theorems.tex',
    'theory/SCX_Undiscovered_Theorems.tex',
    'theory/self_evolution/01_symbol_system.tex',
    'theory/self_evolution/CERCIS_NAMING.tex',
    'theory/self_evolution/final_review_jmlr.tex',
    'theory/self_evolution/final_review_nature.tex',
    'theory/self_evolution/hostile_review.tex',
    'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
]

changed = 0
for f in files:
    if os.path.exists(f):
        if fix_file(f):
            print(f"Fixed: {f}")
            changed += 1
        else:
            print(f"No changes: {f}")

print(f"\nFiles changed: {changed}/{len(files)}")
