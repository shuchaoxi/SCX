#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';

my $dir = "F:/scx/papers";
my @files = (
    "egp_merging/main.tex",
    "meta/SCX_HISTORY.tex", "meta/SCX_HISTORY_v2.tex", "meta/SCX_MANIFESTO.tex",
    "scx_acad_mdta_ilh/main.tex", "scx_agentic_audit/main.tex",
    "scx_art/art_gauge.tex", "scx_astronomy/main.tex",
    "scx_audit_economics/audit_economics.tex", "scx_audit_sword/main.tex",
    "scx_blockchain/main.tex", "scx_business/business_gauge.tex",
    "scx_business_architecture/main.tex", "scx_capstone/auditability_principle.tex",
    "scx_causal_consensus/main.tex", "scx_cfd/main.tex",
    "scx_civilization/civ_gauge.tex", "scx_claude_meta/main.tex",
    "scx_clean_room/main.tex", "scx_climate/main.tex",
    "scx_collective_intelligence/main.tex", "scx_community/main.tex",
    "scx_compactness/main.tex", "scx_company_valuation/company_valuation.tex",
    "scx_dev_log/main.tex", "scx_distillation_hallucination/main.tex",
    "scx_education/edu_gauge.tex", "scx_education/main.tex",
    "scx_elections/main.tex", "scx_environment/env_gauge.tex",
    "scx_galois/main.tex", "scx_galois_falsifiability/main.tex",
    "scx_genomics/main.tex", "scx_geopolitics/main.tex",
    "scx_goodhart/goodhart_gauge.tex", "scx_governance/main.tex",
    "scx_grand_unification/grand_unification.tex",
    "scx_hamiltonian/scx_hamiltonian.tex", "scx_hamiltonian_audit/main.tex",
    "scx_hardware/checklist.tex", "scx_hardware/spec.tex", "scx_hardware/ultimate.tex",
    "scx_industry/main.tex", "scx_information_theory/main.tex",
    "scx_instanton/audit_instanton.tex", "scx_ip_note/main.tex",
    "scx_journalism/main.tex", "scx_lambda/lambda_gauge.tex",
    "scx_law/main.tex", "scx_llm/llm_todo.tex",
    "scx_maintainer_analysis/maintainer_analysis.tex",
    "scx_matrix_theory/main.tex", "scx_medicine/main.tex",
    "scx_medicine/med_gauge.tex", "scx_meta_audit/meta_audit.tex",
    "scx_ml_audit/main.tex", "scx_ml_history/main.tex",
);

my %replacements = (
    # Names / Parenthetical explanations
    '(老实人定理)' => '(the Honest Person Theorem)',
    '(老实人)' => '(the Honest Person)',
    '(面壁者)' => '(the Wall-Facer)',
    '(紫荆)' => '(the Chinese redbud)',
    '(雅洁)' => '(elegant purification)',
    '(春季)' => '(spring season)',
    '(春)' => '(Spring)',
    
    # Section headings
    '全化学周期表势函数的SCX蒸馏路径' => 'SCX Distillation Pathway for Full Periodic Table Potential Functions',
    
    # Genomics
    '基因组' => 'Genomic',
    '变异致病性' => 'Variant Pathogenicity',
    '多算法共识' => 'Multi-Algorithm Consensus',
    '预测误差' => 'Prediction Error',
    '新生物学' => 'Novel Biology',
    '标注偏差' => 'Annotation Bias',
    '变异' => 'Variant',
    '预测' => 'Prediction',
    '预测工具' => 'Prediction Tools',
    '类似于药物说明书的适应症声明' => 'analogous to drug indication statements',
    '适应症' => 'Indications',
    '假设声明' => 'Assumption Declaration',
    '正交证据' => 'Orthogonal Evidence',
    '不确定性量化' => 'Uncertainty Quantification',
    '公平性' => 'Equity',
    
    # CFD
    '空气动力学' => 'Aerodynamics',
    '湍流模型' => 'Turbulence Modeling',
    '核心命题' => 'Core Proposition',
    
    # Climate
    '气候建模' => 'Climate Modeling',
    
    # Hardware
    '药物数据库全量筛选' => 'Full Drug Database Screening',
    '硬件配置单' => 'Hardware Specification',
    '计算需求分析' => 'Computational Requirements Analysis',
    '面壁者终极限配置' => 'Wall-Facer Ultimate Configuration',
    '一步到位' => 'One-Shot Complete Setup',
    '核心思想' => 'Core Philosophy',
    '研究超级配置清单' => 'Research Supercomputing Configuration Checklist',
    '算力层' => 'Compute Layer',
    
    # Keywords patterns (keep English + Chinese → English only)
    '多信使天文学' => 'multi-messenger astronomy',
    '引力波' => 'gravitational waves',
    '中微子天文' => 'neutrino astronomy',
    '机器学习理论' => 'machine learning theory',
    '多专家共识' => 'multi-expert consensus',
    
    # Legal
    '法律证据' => 'legal evidence',
    '证人认证' => 'witness certification',
    '交叉质询' => 'cross-examination',
    '证据链' => 'evidence chain',
    '传闻证据规则' => 'hearsay rule',
    '伪证检测' => 'perjury detection',
    '多专家验证' => 'multi-expert verification',
    '加密哈希链' => 'cryptographic hash chain',
    '对抗审计' => 'adversarial audit',
    '多证人佐证' => 'Multi-Witness Corroboration',
    '传闻证据的自审计不可辨识性' => 'Hearsay as Self-Audit: Unidentifiability',
    '伪证检测与对抗性质询' => 'Perjury Detection via Adversarial Cross-Examination',
    
    # Journalism
    '新闻核查' => 'news verification',
    '事实核查' => 'fact-checking',
    '多源验证' => 'multi-source corroboration',
    '假新闻检测' => 'fake news detection',
    '来源匿名' => 'source anonymity',
    '认证式事实核查' => 'certified fact-checking',
    '多源印证界' => 'Multi-Source Corroboration Bound',
    '单源不可验证性' => 'Single-Source Unverifiability',
    '匿名性保护共识' => 'Anonymity-Preserving Consensus',
    '事实核查网络韧性' => 'Fact-Checker Network Resilience',
    
    # Elections
    '选举诚信' => 'electoral integrity',
    '多方法计票' => 'multi-method vote tabulation',
    '共识认证' => 'consensus certification',
    '选举舞弊检测' => 'electoral fraud detection',
    '多方法共识检测' => 'Multi-Method Consensus Detection',
    '差异来源不可辨识性' => 'Discrepancy Source Unidentifiability',
    '观察者社区检测' => 'Observer Community Detection',
    
    # Governance
    '治理透明性' => 'governance transparency',
    '多专家验证' => 'multi-expert verification',
    '政策评估' => 'policy evaluation',
    '透明度优势' => 'Transparency Dominance',
    '不透明性检测界' => 'Opacity Detection Bound',
    '政策不可辨识性' => 'Policy Unidentifiability',
    
    # Blockchain
    '区块链共识' => 'blockchain consensus',
    '多验证者认证' => 'multi-validator certification',
    '分叉预防' => 'fork prevention',
    '中本聪共识' => 'Nakamoto consensus',
    '拜占庭容错' => 'Byzantine fault tolerance',
    '分叉不可能性' => 'Fork Impossibility',
    
    # Education
    '多评卷人检测界' => 'Multi-Grader Detection Bound',
    '评分标准共识即Yajie共识' => 'Rubric Consensus = Yajie Consensus',
    '分数膨胀检测' => 'Grade Inflation Detection',
    
    # Labels
    '绿色' => 'Green',
    '黄色' => 'Yellow',
    '红色' => 'Red',
    
    # Common words
    '引言' => 'Introduction',
    '项目概述' => 'Project Overview',
    '核心定理' => 'Core Theorems',
    '核心原则' => 'Core Principles',
    '民主协商' => 'democratic deliberation',
    
    # ML History
    '芽接' => 'Yajie (grafting)',
    '定位' => 'Positioning',
    '随机森林' => 'Random Forest',
    '装袋法' => 'Bagging',
    '堆叠泛化' => 'Stacking',
    '梯度提升' => 'Boosting',
    
    # Clean room
    '净室代码检查报告' => 'Clean Room Code Audit Report',
    '检查范围与模式' => 'Audit Scope and Patterns',
    '扫描目标' => 'Scan Target',
    '扫描模式' => 'Scan Pattern',
    '结果总览' => 'Results Overview',
    
    # Misc
    '中文摘要' => 'Abstract (Chinese)',
    '中文' => 'Chinese',
    '数学依据' => 'Mathematical Basis',
    '谁来监督监督者？' => 'who watches the watchers?',
    '内部参考。不进入论文。' => 'Internal reference. Not for publication.',
    '文件状态' => 'Document Status',
    '最后更新' => 'Last Updated',
    '审核人' => 'Reviewer',
    '保密级别' => 'Classification',
    '答辩日期' => 'Defense Date',
    '指导老师' => 'Advisor',
    '所属单位' => 'Affiliation',
    '密钥' => 'Key',
    '加密' => 'Encryption',
    '审计之剑声明' => 'The Audit Sword Declaration',
    '审计之剑' => 'The Audit Sword',
    '不区分军民' => 'makes no distinction between military and civilian use',
);

foreach my $relpath (@files) {
    my $fpath = "$dir/$relpath";
    next unless -f $fpath;
    
    open my $fh, '<:encoding(UTF-8)', $fpath or do {
        warn "Cannot open $fpath: $!";
        next;
    };
    my $content = do { local $/; <$fh> };
    close $fh;
    
    my $changed = 0;
    foreach my $cn (keys %replacements) {
        my $en = $replacements{$cn};
        if (index($content, $cn) >= 0) {
            $content =~ s/\Q$cn\E/$en/g;
            $changed = 1;
        }
    }
    
    if ($changed) {
        open my $out, '>:encoding(UTF-8)', $fpath or die "Cannot write $fpath: $!";
        print $out $content;
        close $out;
        print "TRANSLATED: $relpath\n";
    } else {
        print "SKIP: $relpath\n";
    }
}

print "\nDONE: Batch translation complete.\n";
