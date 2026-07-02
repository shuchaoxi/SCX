#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';

my $dir = "F:/scx/papers";
my @files = (
    "scx_environment/env_gauge.tex", "scx_industry/main.tex",
    "scx_medicine/med_gauge.tex", "scx_art/art_gauge.tex",
    "scx_distillation_hallucination/main.tex", "scx_audit_economics/audit_economics.tex",
    "scx_hamiltonian_audit/main.tex", "scx_compactness/main.tex",
    "scx_company_valuation/company_valuation.tex", "scx_capstone/auditability_principle.tex",
    "scx_business/business_gauge.tex", "scx_galois_falsifiability/main.tex",
    "scx_information_theory/main.tex", "scx_dev_log/main.tex",
    "scx_acad_mdta_ilh/main.tex", "scx_lambda/lambda_gauge.tex",
    "scx_meta_audit/meta_audit.tex", "scx_civilization/civ_gauge.tex",
    "scx_agentic_audit/main.tex", "scx_hamiltonian/scx_hamiltonian.tex",
    "scx_galois/main.tex", "scx_maintainer_analysis/maintainer_analysis.tex",
    "scx_causal_consensus/main.tex", "scx_instanton/audit_instanton.tex",
    "scx_collective_intelligence/main.tex", "scx_goodhart/goodhart_gauge.tex",
    "scx_geopolitics/main.tex", "scx_education/main.tex",
    "scx_grand_unification/grand_unification.tex", "scx_matrix_theory/main.tex",
    "scx_ip_note/main.tex", "scx_medicine/main.tex", "scx_ml_audit/main.tex",
    "scx_education/edu_gauge.tex", "scx_community/main.tex",
    "scx_astronomy/main.tex", "scx_blockchain/main.tex",
    "scx_governance/main.tex", "scx_elections/main.tex",
    "scx_llm/llm_todo.tex", "scx_business_architecture/main.tex",
    "scx_hardware/checklist.tex", "scx_hardware/ultimate.tex",
    "scx_clean_room/main.tex", "scx_hardware/spec.tex",
    "scx_law/main.tex", "scx_journalism/main.tex",
    "scx_climate/main.tex", "scx_ml_history/main.tex",
    "scx_claude_meta/main.tex", "scx_audit_sword/main.tex",
    "scx_cfd/main.tex", "scx_genomics/main.tex",
    "meta/SCX_MANIFESTO.tex", "meta/SCX_HISTORY.tex",
    "meta/SCX_HISTORY_v2.tex", "egp_merging/main.tex",
);

# Comprehensive Chinese→English mapping
my %map = (
    # ── Theorem environments (remaining) ──
    '命题' => 'Proposition',
    '示例' => 'Example',
    '诚实暴击' => 'Honest Strike',
    '暴击' => 'Strike',
    '严格证明' => 'Rigorous Proof',
    '启发式' => 'Heuristic',
    '开放问题' => 'Open Problem',
    '部分证明' => 'Partial Proof',
    '证明概要' => 'Proof Sketch',
    
    # ── Section headings ──
    '偏差可检测性' => 'Bias Detectability',
    '证明' => 'Proof',
    '附录' => 'Appendix',
    '参考文献' => 'References',
    '致谢' => 'Acknowledgments',
    '结论' => 'Conclusion',
    '摘要' => 'Abstract',
    '关键词' => 'Keywords',
    '作者贡献' => 'Author Contributions',
    '数据可用性' => 'Data Availability',
    '代码可用性' => 'Code Availability',
    '利益冲突' => 'Conflict of Interest',
    
    # ── Environment/Climate ──
    '环境代际势能' => 'Environmental Intergenerational Potential',
    '气候变化作为跨代势能跳跃' => 'Climate Change as Intergenerational Potential Jump',
    '跨代势能跳跃' => 'Intergenerational Potential Jump',
    '边界锁定' => 'Boundary Locking',
    '文明尺度' => 'Civilization Scale',
    '必然引爆' => 'Inevitable Detonation',
    '代际规范' => 'Intergenerational Gauge',
    '环境卷' => 'Environment Volume',
    '代际正义' => 'Intergenerational Justice',
    '环境工作组' => 'Environment Working Group',
    '预印本' => 'Preprint',
    
    # ── Industry/Service ──
    '服务业质量审计' => 'Service Industry Quality Audit',
    '质量保证' => 'Quality Assurance',
    '内部检验' => 'Internal Inspection',
    '制造业' => 'Manufacturing',
    '半导体' => 'Semiconductor',
    '银行业' => 'Banking',
    '金融监管' => 'Financial Regulation',
    '咨询服务' => 'Consulting Services',
    '广告行业' => 'Advertising Industry',
    '法律行业' => 'Legal Industry',
    '高等教育' => 'Higher Education',
    '医疗行业' => 'Healthcare Industry',
    '政府服务' => 'Government Services',
    '先发者' => 'First Movers',
    '后来者' => 'Late Movers',
    '审计维度' => 'Audit Dimensions',
    '可证明的诚信' => 'Provable Integrity',
    '可证明事实' => 'Provable Facts',
    '行业共识' => 'Industry Consensus',
    '赢家类别' => 'Winner Categories',
    '晶圆厂' => 'Wafer Fab',
    '台积电' => 'TSMC',
    '零知识证明' => 'Zero-Knowledge Proof',
    '零知识审计' => 'Zero-Knowledge Audit',
    '质量证明' => 'Quality Proof',
    '客户续约率' => 'Client Renewal Rate',
    '切换成本' => 'Switching Costs',
    '企业惯性' => 'Corporate Inertia',
    '不良' => 'Non-Performing',
    '高质量流动性资产' => 'High-Quality Liquid Assets',
    '公务员' => 'Civil Servants',
    '腐败' => 'Corruption',
    '寻租' => 'Rent-Seeking',
    '可证明的能力' => 'Provable Competence',
    '可感知的忠诚' => 'Perceived Loyalty',
    
    # ── Medicine ──  
    '医学诊断' => 'Medical Diagnosis',
    '医生坐标系' => 'Doctor Coordinate System',
    '患者坐标系' => 'Patient Coordinate System',
    '规范不对齐' => 'Gauge Misalignment',
    '势能面不齐' => 'Potential Surface Misalignment',
    '临床诊断' => 'Clinical Diagnosis',
    '诊断准确性' => 'Diagnostic Accuracy',
    '假阳性' => 'False Positive',
    '假阴性' => 'False Negative',
    '医疗资源' => 'Medical Resources',
    '过度医疗' => 'Over-Treatment',
    '漏诊' => 'Missed Diagnosis',
    
    # ── Art ──
    '艺术势能' => 'Artistic Potential',
    '艺术创作' => 'Artistic Creation',
    '创作自由' => 'Creative Freedom',
    '艺术市场' => 'Art Market',
    '艺术价值' => 'Artistic Value',
    '艺术品' => 'Artwork',
    
    # ── Distillation/Hallucination ──
    '蒸馏' => 'Distillation',
    '幻觉' => 'Hallucination',
    '知识蒸馏' => 'Knowledge Distillation',
    '模型压缩' => 'Model Compression',
    '学生模型' => 'Student Model',
    '教师模型' => 'Teacher Model',
    
    # ── Economics ──
    '审计经济学' => 'Audit Economics',
    '市场效率' => 'Market Efficiency',
    '信息不对称' => 'Information Asymmetry',
    '逆向选择' => 'Adverse Selection',
    '道德风险' => 'Moral Hazard',
    
    # ── Compactness ──
    '紧致性' => 'Compactness',
    '模型复杂度' => 'Model Complexity',
    '过拟合' => 'Overfitting',
    '泛化能力' => 'Generalization Ability',
    
    # ── Company Valuation ──
    '公司估值' => 'Company Valuation',
    '内在价值' => 'Intrinsic Value',
    '市场价值' => 'Market Value',
    '审计溢价' => 'Audit Premium',
    
    # ── Capstone ──
    '可审计性原理' => 'Auditability Principle',
    '审计不可区分性' => 'Audit Unidentifiability',
    
    # ── Business ──
    '商业规范' => 'Business Gauge',
    '商业模式' => 'Business Model',
    '竞争优势' => 'Competitive Advantage',
    
    # ── Galois ──
    '伽罗瓦' => 'Galois',
    '域扩张' => 'Field Extension',
    '可解群' => 'Solvable Group',
    '代数结构' => 'Algebraic Structure',
    
    # ── Information Theory ──
    '信息论审计' => 'Information-Theoretic Audit',
    '信道容量' => 'Channel Capacity',
    '互信息' => 'Mutual Information',
    '熵' => 'Entropy',
    
    # ── Dev Log ──
    '开发日志' => 'Development Log',
    '迭代记录' => 'Iteration Record',
    
    # ── Academic MDTA ILH ──
    '学术' => 'Academic',
    '超越隐喻' => 'Beyond Metaphor',
    '量子纠缠' => 'Quantum Entanglement',
    '数据虫洞' => 'Data Wormholes',
    '相对论不变性' => 'Relativistic Invariance',
    
    # ── Agentic Audit ──
    '智能体审计' => 'Agentic Audit',
    '自主审计' => 'Autonomous Audit',
    
    # ── Hamiltonian ──
    '哈密顿量' => 'Hamiltonian',
    '相空间' => 'Phase Space',
    '辛结构' => 'Symplectic Structure',
    
    # ── Meta Audit ──
    '元审计' => 'Meta-Audit',
    '自审计' => 'Self-Audit',
    
    # ── Civilization ──
    '文明规范' => 'Civilization Gauge',
    '文明尺度' => 'Civilization Scale',
    '文明演化' => 'Civilization Evolution',
    
    # ── Collective Intelligence ──
    '集体智慧' => 'Collective Intelligence',
    '群体决策' => 'Group Decision-Making',
    
    # ── ML Audit ──
    '机器学习审计' => 'Machine Learning Audit',
    '模型审计' => 'Model Audit',
    
    # ── Causal Consensus ──
    '因果共识' => 'Causal Consensus',
    '因果推断' => 'Causal Inference',
    
    # ── Instanton ──
    '瞬子' => 'Instanton',
    '隧穿' => 'Tunneling',
    
    # ── Lambda Gauge ──
    '拉姆达规范' => 'Lambda Gauge',
    '宇宙学常数' => 'Cosmological Constant',
    
    # ── Education ──
    '教育评估' => 'Educational Assessment',
    '评卷人' => 'Grader',
    '评分标准' => 'Rubric',
    '分数' => 'Score',
    '膨胀' => 'Inflation',
    '教育公正' => 'Educational Equity',
    '平等论' => 'Equality Principle',
    
    # ── Geopolitics ──
    '地缘政治学' => 'Geopolitics',
    '战略分析司' => 'Strategic Analysis Division',
    '相互审计均衡' => 'Mutual Audit Equilibrium',
    'GPU霸权' => 'GPU Hegemony',
    '审计至上' => 'Audit Supremacy',
    '绝密' => 'TOP SECRET',
    '内部战略文件' => 'Internal Strategic Document',
    
    # ── Grand Unification ──
    '大统一' => 'Grand Unification',
    '统一场论' => 'Unified Field Theory',
    
    # ── Matrix Theory ──
    '矩阵理论' => 'Matrix Theory',
    '随机矩阵' => 'Random Matrix',
    
    # ── IP Note ──
    '知识产权说明' => 'Intellectual Property Note',
    
    # ── Goodhart ──
    '古德哈特定律' => "Goodhart's Law",
    '指标失效' => 'Metric Failure',
    
    # ── Hardware ──
    '超级配置' => 'Supercomputing Configuration',
    '研发工作站' => 'R&D Workstation',
    '一、算力层' => 'I. Compute Layer',
    '二、存储层' => 'II. Storage Layer',
    '三、网络层' => 'III. Network Layer',
    '四、软件层' => 'IV. Software Layer',
    '五、安全层' => 'V. Security Layer',
    '组件' => 'Component',
    '配置' => 'Configuration',
    '任务' => 'Task',
    '瓶颈' => 'Bottleneck',
    '量级' => 'Scale',
    '不买企业级' => 'Do not buy enterprise-grade',
    '买消费级/工作站级的顶配，单人就够' => 'Buy top consumer/workstation-grade hardware; sufficient for a single person',
    '数据库下载' => 'Database Download',
    '全量筛选' => 'Full Screening',
    
    # ── Clean Room ──
    '净室' => 'Clean Room',
    '代码检查' => 'Code Audit',
    '检查日期' => 'Audit Date',
    '检查工具' => 'Audit Tool',
    '自动模式扫描' => 'Automated Pattern Scanning',
    '检查目标' => 'Audit Objective',
    '不含学校/课题组特定引用' => 'No institution/lab-specific references',
    '检查范围与模式' => 'Audit Scope and Patterns',
    '扫描目标' => 'Scan Target',
    '扫描模式' => 'Scan Pattern',
    '扫描工具' => 'Scanning Tool',
    '遍历所有' => 'traverses all',
    '文件' => 'files',
    '列级别精确匹配' => 'line-level exact matching',
    '结果总览' => 'Results Overview',
    '目录' => 'Directory',
    '判定' => 'Verdict',
    '发现数' => 'Findings',
    '孝感' => 'Xiaogan',
    '核心' => 'Core',
    
    # ── Community ──
    '内河' => 'Neihe (Inner River)',
    '协议社区' => 'Protocol Community',
    '形式化框架' => 'Formal Framework',
    '定理守护者集体' => 'Theorem Guardian Collective',
    '维护者轮换' => 'Maintainer Rotation',
    '紧急审计' => 'Emergency Audit',
    '内核' => 'Kernel',
    '贡献者' => 'Contributors',
    '观察者' => 'Observers',
    
    # ── Claude Meta ──
    '项目' => 'Project',
    '论文矩阵' => 'Paper Matrix',
    '全部直指' => 'All Targeting',
    '系列' => 'Series',
    '期刊' => 'Journal',
    '状态' => 'Status',
    '正文已起草' => 'Main text drafted',
    '待转译' => 'Awaiting translation',
    '概念已设计' => 'Concept designed',
    '已有草稿' => 'Draft available',
    '等' => 'awaiting',
    '已完成' => 'Completed',
    '参见' => 'See',
    
    # ── ML History ──
    '视角' => 'Perspective',
    '逐定理再审计' => 'Theorem-by-Theorem Re-Audit',
    '公理体系' => 'Axiom System',
    '机器学习相关子集' => 'Machine Learning Relevant Subset',
    '集成方法作为' => 'Ensemble Methods as',
    '显式多专家共识' => 'Explicit Multi-Expert Consensus',
    '纯形式' => 'Purest Form',
    '方差缩减作为有效' => 'Variance Reduction as Effective',
    '增长' => 'Growth',
    '学习权重' => 'Learned Weighting',
    '为何不同（且危险）' => 'Why Different (and Dangerous)',
    '隐式多专家' => 'Implicit Multi-Expert',
    '子网络投票' => 'Sub-Network Voting',
    '深度作为噪声补偿' => 'Depth as Noise Compensation',
    '注意力机制作为' => 'Attention Mechanism as',
    '式记忆' => '-Style Memory',
    '批归一化作为状态空间正则化' => 'Batch Normalization as State-Space Regularization',
    '生成对抗网络作为对抗审计' => 'GANs as Adversarial Audit',
    '为何' => 'Why',
    '失败' => 'Fails',
    '自监督学习作为自我审计' => 'Self-Supervised Learning as Self-Audit',
    '适用领域' => 'Domain of Applicability',
    
    # ── LLM TODO ──
    '明日推进' => 'Tomorrow\'s TODOs',
    '全药物数据库' => 'Full Drug Database',
    '一次性全筛' => 'One-Shot Full Screening',
    '数据库清单（全量，不仅限于' => 'Database List (Full, not limited to',
    
    # ── Audit Sword ──
    '面壁者不发禁令。面壁者留剑。' => 'The Wall-Facer issues no prohibitions. The Wall-Facer leaves a sword.',
    '任何人都可以阅读、复现、部署' => 'Anyone may read, reproduce, and deploy',
    '我们不禁止任何特定用途' => 'We prohibit no specific use',
    '但我们保留一项不可剥夺的权利' => 'But we reserve one inalienable right',
    '任何组织使用' => 'Any organization using the',
    '框架进行数据质量评估，其评估结果可以通过相同的数学方法被独立第三方进行验证和审计。军事用途不例外。' => 'framework for data quality assessment shall have its assessment results verifiable and auditable by independent third parties using the same mathematical methods. Military use is no exception.',
    '这不是限制。这是威慑。审计之剑不区分军民。' => 'This is not a restriction. It is deterrence. The Audit Sword makes no distinction between military and civilian use.',
    '定理保证。外部可复现。不需要许可。' => 'Guaranteed by theorems. Externally reproducible. No permission required.',
    
    # ── Climate ──
    '地球系统模式' => 'Earth System Models',
    '未来气候' => 'Future Climate',
    '人为强迫' => 'Anthropogenic Forcing',
    '不确定性估计' => 'Uncertainty Estimation',
    '非正式约定' => 'Informal Conventions',
    '数学保证' => 'Mathematical Guarantees',
    '耦合气候系统' => 'Coupled Climate System',
    '多专家预测问题' => 'Multi-Expert Prediction Problem',
    '系统偏差检测' => 'Systematic Bias Detection',
    '结构独立' => 'Structurally Independent',
    '遗漏' => 'Missing',
    '间隙' => 'Gap',
    '衰减' => 'Decays',
    '归因不可区分性' => 'Attribution Unidentifiability',
    '区域气候响应' => 'Regional Climate Response',
    '北极放大效应' => 'Arctic Amplification',
    '分歧' => 'Disagreement',
    '数学上不可能' => 'Mathematically Impossible',
    '声明显式结构假设' => 'Declare Explicit Structural Assumptions',
    '次网格参数化误差' => 'Sub-Grid Parameterization Error',
    '复合质量指标' => 'Composite Quality Metric',
    '多模式后报技巧' => 'Multi-Model Hindcast Skill',
    '新意加权探索奖励' => 'Novelty-Weighted Exploration Reward',
    '有原则的气候预测排名方法' => 'Principled Climate Prediction Ranking Method',
    '对观测的忠实性' => 'Fidelity to Observations',
    '前所未有状态的认识价值' => 'Recognition Value of Unprecedented States',
    '气候归因' => 'Climate Attribution',
    '人人平等' => 'Universal Equality',
    '一致性' => 'Consistency',
    
    # ── CFD ──
    '传统计算流体力学通过多专家冗余提供了隐含的质量保证（不同湍流模型、网格分辨率、数值格式）。神经CFD方法缺少这种保证。SCX审计框架通过显式化假设、检测系统误差、标准化基准测试，为神经CFD提供了缺失的质量证明层。' => 'Traditional CFD provides implicit quality assurance through multi-expert redundancy (different turbulence models, grid resolutions, numerical schemes). Neural CFD methods lack such guarantees. The SCX audit framework provides the missing quality certification layer for neural CFD by explicitizing assumptions, detecting systematic errors, and standardizing benchmarks.',
    
    # ── Generic document metadata ──
    '版本' => 'Version',
    '状态：' => 'Status:',
    '分类：' => 'Classification:',
    '理论体系' => 'Theoretical System',
    '最后更新：' => 'Last Updated:',
    '内部参考' => 'Internal Reference',
    '不进入论文' => 'Not for publication',
    '审核人：' => 'Reviewer:',
    '保密级别：' => 'Classification Level:',
    '答辩日期：' => 'Defense Date:',
    '指导老师：' => 'Advisor:',
    '所属单位：' => 'Affiliation:',
    
    # ── Misc remaining phrases ──
    '没有办法知道' => 'There is no way to know',
    '这个假设是错的' => 'This assumption is wrong',
    '这个假设的两个部分都有严重瑕疵' => 'Both parts of this assumption have serious flaws',
    '将变得可以被证明——这在当前体制下是不可能的' => 'will become provable — which is impossible under the current system',
    '它不改变行业做什么，而是改变行业' => 'It does not change what industries do, but changes how industries',
    '如何证明它们做了所说的事' => 'prove they did what they claimed',
    '术语' => 'Term',
    
    # ── Confidence markers ──
    '【诚实暴击】' => '[Honest Strike]',
    '【严格证明】' => '[Rigorous Proof]',
    '【启发式】' => '[Heuristic]',
    '【开放问题】' => '[Open Problem]',
    '【部分证明】' => '[Partial Proof]',
    '【证明概要】' => '[Proof Sketch]',
);

# Apply replacements
foreach my $relpath (@files) {
    my $fpath = "$dir/$relpath";
    next unless -f $fpath;
    
    open my $fh, '<:encoding(UTF-8)', $fpath or next;
    my $c = do { local $/; <$fh> };
    close $fh;
    
    my $orig = $c;
    
    foreach my $cn (sort { length($b) <=> length($a) } keys %map) {
        my $en = $map{$cn};
        $c =~ s/\Q$cn\E/$en/g;
    }
    
    if ($c ne $orig) {
        open my $out, '>:encoding(UTF-8)', $fpath or die "Cannot write $fpath: $!";
        print $out $c;
        close $out;
        my $before = () = $orig =~ /[\x{4e00}-\x{9fff}]/g;
        my $after = () = $c =~ /[\x{4e00}-\x{9fff}]/g;
        print "TRANSLATED: $relpath ($before -> $after Chinese chars)\n";
    }
}

print "DONE.\n";
