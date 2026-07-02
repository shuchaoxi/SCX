#!/usr/bin/env python3
"""Third pass: aggressive remaining Chinese→English translation."""
import re, os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    patches = [
        # === File 1: 05_expert_governance_protocol.tex ===
        ('SCX 代码ofimplementationmapping', 'SCX Code Implementation Mapping'),
        ('沿use SCX frameworkDefinition(参见', 'Following SCX framework definitions (see'),
        ('match号', 'Notation'),
        ('original子构type', 'atomic configuration'),
        ('标签space', 'label space'),
        ('true实Annotationsfunction', 'true labeling function'),
        ('个 MLIP expert', ' MLIP expert'),
        ('expert总number', 'expert count'),
        ('Statusspace(have限划分)', 'state space (finite partition)'),
        ('Statusmappingfunction', 'state mapping function'),
        ('can测function', 'measurable function'),
        ('构type', 'configuration'),
        ('归属ofStatus', 'belongs to state'),
        ('Statusconditionsexpert风险', 'State-conditional expert risk'),
        ('SCX 可relyproperty', 'SCX Reliability'),
        ('expert配对冲突', 'Expert Pairwise Conflict'),
        ('Protocol 整body结构', 'Protocol Overall Structure'),
        
        # === File 2: SCX_Undiscovered_Theorems.tex ===
        ('任务:atalreadyhaveT1-T7basis础Theorem', 'Task: Based on existing T1-T7 fundamental theorems'),
        ('五methodtoward草案之上,深究iswhether还havenot yet覆盖oftheory盲区', 'the five draft directions, investigate whether there are uncovered theoretical blind spots'),
        ('with下五个methodtoward按''最具finding潜force''排order', 'the following five directions are ordered by "highest discovery potential"'),
        ('eachgiveCompleteTheorem陈述draft并honest标Note推property', 'each given complete theorem statement draft with honest provability annotations'),
        ('Q-Theorem', 'Q-Theorem'),
        ('Audit Entropy Theorem', 'Audit Entropy Theorem'),
        ('AE-Theorem', 'AE-Theorem'),
        ('Audit Complexity Theorem', 'Audit Complexity Theorem'),
        ('AC-Theorem', 'AC-Theorem'),
        ('Recursive Audit Theorem', 'Recursive Audit Theorem'),
        ('RA-Theorem', 'RA-Theorem'),
        ('Alignment Audit Theorem', 'Alignment Audit Theorem'),
        ('AA-Theorem', 'AA-Theorem'),
        ('新Theorem群ofreasoning编Structure', 'Logical Structure of the New Theorem Group'),
        ('成熟度总table', 'Maturity Summary Table'),
        ('核心claim张', 'Core Claim'),
        ('严格可推部share比', 'Rigorously Provable Portion'),
        ('关键开发challenge', 'Key Open Challenge'),
        ('quantumNoclonereinforcementTheorem', 'quantum no-cloning reinforces Theorem'),
        ('审计熵单调解少', 'audit entropy monotonically decreases'),
        ('Audit热寂对shouldTheorem', 'Audit heat death corresponds to Theorem'),
        ('Nocan约无知', 'irreducible ignorance'),
        ('检测噪声ofminimumexpert数下界as', 'minimum expert count lower bound for detecting noise'),
        ('Modelcomplexityand审计代pricedual', 'model complexity and audit cost duality'),
        ('递归审计收convergent当and仅当', 'recursive audit converges if and only if'),
        ('Nocan动point恰asTheorem', 'the fixed point is exactly Theorem'),
        ('information壁barrier', 'information barrier'),
        ('对齐problemcan归约asdata审计', 'alignment problem reducible to data audit'),
        ('already有五Theorem', 'Existing Five Theorems'),
        ('新五Theorem', 'New Five Theorems'),
        ('关system', 'Relationship'),
        ('causalseparation', 'causal separation'),
        ('quantum共share', 'quantum share'),
        ('Federated审计', 'Federated Audit'),
        ('AuditEntropy', 'Audit Entropy'),
        ('AEasFAgiveuniformalizedinformation论skeleton', 'AE provides FA with a unified information-theoretic skeleton'),
        ('对抗鲁棒', 'Adversarial Robustness'),
        ('AuditComplexity量化', 'Audit Complexity quantifies'),
        ('时序漂移', 'Temporal Shift'),
        ('Recursive Audit是TSof元level推广', 'RA is a meta-level generalization of TS'),
        ('人机collaborative', 'Human-Computer Collaboration'),
        ('对齐Audit是HCat对齐场sceneof特化', 'AA is a specialization of HC for alignment scenarios'),
        ('草案版', 'Draft version'),
        ('SCX理论架构师', 'SCX Theory Architect'),
        ('待collaborativeauthor审阅', 'Pending collaborator review'),
        ('五Theorem均处Concept阶segment', 'All five theorems are at the conceptual stage'),
        
        # === File 3: MATHEMATICAL_GENEALOGY.tex ===
        ("construct with 区'sDistribution", 'construct with distinguishable distributions'),
        ('Neyman-Pearson 归bound', 'Neyman-Pearson reduction'),
        ('ArbitraryAlgorithm归boundas Bayes checktest', 'arbitrary algorithm reduces to Bayes test'),
        ('Nonon-etc.formula 松弛', 'Not an inequality relaxation'),
        ('Spring 最深刻Proof具', "Spring's most profound proof tool"),
        ('渐near义under Yescannot be can', 'asymptotically cannot be'),
        ('non-true正improvement判别can', 'not truly improving discrimination ability'),
        ('指showFunction跳跃', 'indicator function jump'),
        ('零测set 修improvement', 'zero-measure set modification'),
        
        # === File 4: multi_head_spring_and_positional_encoding_analysis.tex ===
        ('弱featurenecessarilylosseffect', 'Weak Feature Inevitable Failure'),
        ('刻画featurespace', 'characterizes the feature space'),
        ('informationnon-足程', 'information insufficiency'),
        ('Proof technique', 'Proof Technique'),
        ('贝叶斯Optimal间', 'Bayes optimal'),
        ('comparison(feature弱)', 'is large (features weak)'),
        ('决', 'determined'),
        ('construct property 双世bound Proof', 'Constructive Two-World Bound Proof'),
        ('has 观测etc.价', 'has observationally equivalent'),
        ('Errortitle 记', 'error label'),
        ('title Noise', 'label noise'),
        ('Correcttitle but on Difficulty(贝叶斯non-determine property)', 'correct label but on Difficulty (Bayesian non-deterministic)'),
        ('has Algorithmcan only through 观测Data', 'no algorithm can distinguish these worlds through observed data alone'),
        ('形formula ization', 'Formalization'),
        ('决策规then', 'decision rule'),
        
        # === File 5: ppe_rigorous_derivation.tex ===
        ('修订: Correction of CC audit report', 'Revision: Correction of CC audit report'),
        ('audit报告', 'audit report'),
        ('decision阈value', 'decision threshold'),
        ('basis础', 'Foundations'),
        ('随变quantity', 'random variables'),
        ('audit报告make using', 'audit report uses'),
        ('table明', 'indicates'),
        ('遵循 CC report', 'following the CC report'),
        ('original始报告', 'original report'),
        ('严密number learning formula ization', 'Rigorous Mathematical Formalization'),
        ('蛋白qualityorder sequence', 'Protein Sequence'),
        ('Situstheory最终验证报告', 'Situs Theory Final Verification Report'),
        
        # General remaining single chars and short fragments
        ('修improvement', 'modification'),
        ('包contain', 'contain'),
        ('归normalization', 'normalization'),
        ('Warning框', 'Warning box'),
        ('clearly声明', 'Explicit statement'),
        ('table达formula', 'expression'),
        ('逻辑Errortitle', 'Logical error description'),
        ('cannot 逻辑推', 'cannot logically deduce'),
        ('赖氨酸残basis', 'lysine residue'),
        ('蛋白qualitynon-Location', 'protein at different positions'),
        ('type ization 残basis', 'typical residue'),
        ('侧chain', 'side chain'),
        ('bias离溶液value', 'deviates from solution value'),
        ('单位', 'units'),
        ('酸碱催ization', 'acid-base catalysis'),
        ('共价催ization', 'covalent catalysis'),
        ('Q-Theorem(量subSCXTheorem)', 'Q-Theorem (Quantum SCX Theorem)'),
        ('AE-Theorem(审计熵Theorem)', 'AE-Theorem (Audit Entropy Theorem)'),
        ('AC-Theorem(审计complexityTheorem)', 'AC-Theorem (Audit Complexity Theorem)'),
        ('RA-Theorem(递recursive审计Theorem)', 'RA-Theorem (Recursive Audit Theorem)'),
        ('AA-Theorem(对alignment审计Theorem)', 'AA-Theorem (Alignment Audit Theorem)'),
        
        # More single chars that survived
        ('数 照', 'account'),
        ('符号约', 'Notation Conventions'),
        ('注形', 'attention'),
        ('符预', 'match expected'),
        ('修improvement', 'modification'),
        ('已修correct', 'corrected'),
        ('统one', 'unified'),
        ('已降level', 'downgraded'),
        ('已限determine', 'restricted'),
        ('已改', 'changed'),
        ('放开problem', 'open problem'),
        ('余non-one', 'residual inconsistencies'),
        ('需关note', 'require attention'),
        ('充must', 'necessary and sufficient'),
        ('必must', 'necessary'),
        ('充conditions', 'sufficient condition'),
        ('摘must', 'abstract'),
        ('粗rough形formula', 'approximate formula'),
        ('验all', 'posterior'),
        ('贝叶斯', 'Bayesian'),
    ]
    
    for old, new in patches:
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

files = [
    'theory/propositions/05_expert_governance_protocol.tex',
    'theory/SCX_Undiscovered_Theorems.tex',
    'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
    'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
    'theory/self_evolution/ppe_rigorous_derivation.tex',
    'theory/self_evolution/situs_final_verification.tex',
    'theory/self_evolution/situs_physical_validation.tex',
]

for f in files:
    path = os.path.join('F:/scx', f)
    if os.path.exists(path):
        changed = fix_file(path)
        print(f'{f}: {"CHANGED" if changed else "UNCHANGED"}')
    else:
        print(f'{f}: NOT FOUND')
