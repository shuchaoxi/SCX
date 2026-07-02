# SCX 论文-验证脚本完整索引

**Total count: 197 papers (94 directories), 30 verification scripts | 总计数：197篇论文（94个目录），30个验证脚本**

---

## 目录

1. [核心理论 (Core Theory)](#核心理论-core-theory) (22 篇)
2. [物理方向 (Physics)](#物理方向-physics) (12 篇)
3. [博弈论与经济 (Game Theory & Economics)](#博弈论与经济-game-theory-&-economics) (8 篇)
4. [协议与治理 (Protocol & Governance)](#协议与治理-protocol-&-governance) (8 篇)
5. [社会推论 (Social Inference)](#社会推论-social-inference) (18 篇)
6. [工程实现 (Engineering)](#工程实现-engineering) (21 篇)
7. [其他 (Other)](#其他-other) (7 篇)

---

## 核心理论 (Core Theory)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_theory/` | SCX核心理论：基于状态条件专家的标签噪声检测 / SCX Core Theory: Detecting Label Noise by State-Conditioned eXpertise | SCX框架的核心理论论文，证明噪声-难度不可区分性定理，建立多专家一致性审计的数学基础 | Core theory establishing SCX framework: proves noise-difficulty unidentifiability theorem and multi-expert consensus audit foundations | ⬜ |
| 2 | `scx_information_theory/` | 信息论SCX：多专家信息融合的率失真理论 / Information-Theoretic SCX: Rate-Distortion Theory of Multi-Expert Information Fusion | 从率失真理论、Slepian-Wolf编码和Shannon分离定理为SCX建立完整信息论基础 | Complete information-theoretic foundation for SCX via rate-distortion, Slepian-Wolf coding, and Shannon separation | ⬜ |
| 3 | `scx_compactness/` | 紧致性定理与SCX的深层连接 / Compactness Theorem and Deep Connections to SCX | 揭示模型论紧致性定理与SCX多专家审计框架之间的深层结构对应，证明有限到无限的审计传递性 | Deep structural correspondence between compactness theorem and SCX audit: finite-to-infinite audit transfer | ⬜ |
| 4 | `scx_galois/` | Galois-SCX：群论与多专家审计的深层对应 / Galois-SCX: Deep Correspondence Between Group Theory and Multi-Expert Audit | 构造审计群并证明Galois对应的完整类似物：子群格与可审计子问题格的一一对应 | Audit group construction with full Galois correspondence: subgroup lattice ↔ auditable subproblem lattice | ⬜ |
| 5 | `scx_galois_falsifiability/` | Galois反证：SCX的可证伪边界 / Galois Falsification: Falsifiable Boundaries of SCX | 从Galois-SCX的逆否命题导出SCX框架第一个严格的波普尔式可证伪预测 | First rigorous Popperian falsifiable predictions for SCX via contrapositive of Galois-SCX | ⬜ |
| 6 | `scx_fiber_bundle/` | 势能面不齐的离散几何：SCX规范理论的图霍奇形式化 / Discrete Geometry of Potential Misalignment: Graph Hodge Formalization of SCX Gauge Theory | 将SCX规范理论建立在图上的离散霍奇理论之上，完全放弃连续微分几何的纤维丛框架 | SCX gauge theory reformulated on discrete graph Hodge theory, abandoning continuous fiber bundle framework | ⬜ |
| 7 | `scx_gauge_formalized/` | SCX规范理论形式化：多专家系统的规范固定与曲率 / Formalized SCX Gauge Theory: Gauge Fixing and Curvature in Multi-Expert Systems | SCX规范理论的形式化阐述，包含规范固定、曲率定义和多视角校正（viewpoint4_correction） | Formal exposition of SCX gauge theory: gauge fixing, curvature, and viewpoint corrections | ✅ |
| 8 | `scx_gauge_physics/` | 规范场论与SCX多专家系统的数学结构类比 / Gauge Field Theory and Mathematical Structure Analogy with SCX Multi-Expert Systems | 系统阐述规范场论（Yang-Mills、纤维丛、联络、曲率）与SCX多专家系统的数学结构类比 | Systematic analogy between gauge field theory (Yang-Mills, fiber bundles) and SCX multi-expert structure | ⬜ |
| 9 | `scx_matrix_theory/` | 矩阵形式的SCX / SCX in Matrix Form | SCX多专家审计框架的矩阵理论形式化，以线性代数语言重述核心定理 | Matrix-theoretic formalization of SCX multi-expert audit framework using linear algebra | ⬜ |
| 10 | `scx_S_operator/` | SCX社会推论中势能算子S的操作定义 / Operational Definition of the Potential Operator S in SCX Social Inference | SCX社会推论中势能算子S的严格操作定义及其数学性质 | Rigorous operational definition and mathematical properties of the S operator in SCX social inference | ✅ |
| 11 | `scx_causal/` | SCX因果不可辨识性定理 / SCX Causal Unidentifiability Theorem | 证明因果方向声称在无声明识别假设时从观测数据不可辨识，三个互不相容的SCM产生相同观测分布 | Causal direction claims unidentifiable without declared assumptions; three incompatible SCMs yield identical distributions | ⬜ |
| 12 | `scx_causal_consensus/` | 因果SCX：因果推断的多专家审计 / Causal SCX: Multi-Expert Audit of Causal Inference | 将3-SCM不可辨识性定理推广至M>2个因果估计器的一般情形，建立因果共识界 | Generalizes 3-SCM unidentifiability to M>2 causal estimators, establishing causal consensus bounds | ⬜ |
| 13 | `scx_complexity/` | SCX谕示分离：通过多专家审计审视P vs NP / The SCX Oracle Separation: P vs NP Through Multi-Expert Audit | 证明SCX多专家审计机制构成一个Baker-Gill-Solovay谕示，相对其P≠NP | SCX multi-expert audit mechanism constitutes a BGS oracle relative to which P≠NP | ⬜ |
| 14 | `scx_temporal/` | 时间SCX：记忆-遗忘的形式理论 / Temporal SCX: A Formal Theory of Memory and Forgetting | 将Spring SE-1推广到时变目标，推导遗忘必要性定理、最优遗忘率及记忆-泛化权衡 | Extends Spring SE-1 to time-varying targets: necessity of forgetting, optimal forgetting rate, memory-generalization tradeoff | ⬜ |
| 15 | `scx_alignment/` | SCX对齐均衡定理 / SCX Alignment Equilibrium Theorem | 证明M=1单裁判对齐（RLHF/ Constitutional AI）根本不足，多裁判共识提供指数级奖励篡改检测保证 | Single-judge alignment (RLHF) fundamentally insufficient; multi-judge consensus provides exponential detection guarantees | ⬜ |
| 16 | `scx_hallucination/` | SCX幻觉必然性定理 / SCX Hallucination Inevitability Theorem | 证明高置信度幻觉对任何单模型LLM不可避免，仅多模型审计提供指数级检测保证 | High-confidence hallucinations inevitable for single-model LLMs; only multi-model auditing provides exponential guarantees | ⬜ |
| 17 | `scx_ood/` | SCX分布外检测下界 / SCX OOD Detection Lower Bound | 证明有限专家OOD检测下界：最小可检测偏移δ_min=σ/√M，虚警和检测功效均由Hoeffding界控制 | Finite-expert OOD lower bound: minimum detectable shift δ_min=σ/√M with Hoeffding-bounded false alarms | ⬜ |
| 18 | `scx_distillation_hallucination/` | 幻觉的必然性：蒸馏模型幻觉的结构性证明 / The Inevitability of Hallucination: Structural Proof for Distilled Models | 从紧致性断裂、信息论退化和自旋玻璃相变三重角度证明蒸馏幻觉是结构性必然 | Triple proof (compactness breakdown, information degradation, spin-glass transition) that distillation hallucination is structural | ⬜ |
| 19 | `scx_goodhart/` | Goodhart规范：Cercis评分框架中度量操纵的形式化检测与缓解 / The Goodhart Gauge: Formal Detection and Mitigation of Metric Manipulation | 形式化Goodhart定律在SCX/Cercis评分框架中的表现，提出度量操纵的检测与缓解方法 | Formalizes Goodhart's Law in SCX/Cercis framework with detection and mitigation of metric manipulation | ✅ |
| 20 | `scx_hamiltonian/` | 神经网络哈密顿量与SCX多专家审计：统计力学对应 / Neural Network Hamiltonian and SCX Multi-Expert Audit: A Statistical Mechanics Correspondence | 建立SCX多专家审计与统计力学无序系统理论的严格对应，副本对称破缺刻画专家群结构 | Rigorous correspondence between SCX audit and disordered systems: replica symmetry breaking characterizes expert structure | ⬜ |
| 21 | `scx_hamiltonian_audit/` | 哈密顿量作为审计条件：从能量景观判断可审计性 / Hamiltonian as Audit Condition: Judging Auditability from Energy Landscape | 将SCX哈密顿量理论推进为预审计诊断工具，仅通过能量景观判断可审计性 | Advances SCX Hamiltonian theory to pre-audit diagnostics: judge auditability from energy landscape alone | ⬜ |
| 22 | `theorems/` | SCX定理集合：审计复杂性、对齐、熵、对抗、因果、联邦、人类、量子、递归、时间等 / SCX Theorem Collection: Audit Complexity, Alignment, Entropy, Adversarial, Causal, Federated, Human, Quantum, Recursive, Temporal | 14篇独立定理论文：涵盖主动学习采样、协议博弈、跨域保持、弱特征界、对齐审计、审计复杂度、审计熵、对抗分类、因果发现、联邦审计、人机协作、量子SCX、递归审计和时间SCX | 14 standalone theorem papers covering active learning, protocol games, cross-domain, weak features, alignment, complexity, entropy, adversarial, causal, federated, human-AI, quantum, recursive, and temporal SCX | ⬜ |

## 物理方向 (Physics)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_quantum/` | 量子测量作为多观察者共识：波函数坍缩的SCX审计 / Quantum Measurement as Multi-Observer Consensus: An SCX Audit of Wavefunction Collapse | 将量子测量问题重构为多专家审计问题，用Born规则和SCX定理重新诠释波函数坍缩 | Reframes quantum measurement as multi-expert audit, reinterpreting wavefunction collapse via Born rule and SCX | ⬜ |
| 2 | `scx_quantum_audit/` | 量子安全SCX审计 / Quantum-Secured SCX Audit | 将SCX审计协议扩展到量子安全领域，利用量子密码学保护审计完整性 | Extends SCX audit to quantum-secured domain using quantum cryptography for audit integrity | ✅ |
| 3 | `scx_instanton/` | 审计瞬子：SCX规范理论中的瞬子解 / Audit Instantons: Instanton Solutions in SCX Gauge Theory | 发现SCX规范场论中的瞬子解——审计空间中的隧道效应和拓扑非平凡配置 | Instanton solutions in SCX gauge theory: tunneling effects and topologically non-trivial audit configurations | ✅ |
| 4 | `scx_singularity/` | SCX奇点理论深化：从黑洞物理学到审计奇点 / Deepening SCX Singularity Theory: From Black Hole Physics to Audit Singularities | 将黑洞物理学（事件视界、奇点定理、霍金辐射）映射到SCX审计框架中的审计奇点 | Maps black hole physics (event horizons, singularity theorems, Hawking radiation) to audit singularities in SCX | ✅ |
| 5 | `scx_unified_field/` | SCX统一场论 / SCX Unified Field Theory | 探索SCX多专家审计框架与物理学统一场论的深层对应关系 | Explores deep correspondence between SCX multi-expert audit and unified field theory in physics | ⬜ |
| 6 | `scx_turbulence/` | 湍流作为不可辨识性定理：有限分辨率下N体截断误差与真实湍流的不可区分性 / Turbulence as an Unidentifiability Theorem: Indistinguishability of N-Body Truncation and True Turbulence | 将湍流重构为认知论问题：N体截断误差与真实湍流在有限分辨率下数学上不可区分 | Reconstructs turbulence as epistemological problem: N-body truncation error and true turbulence are mathematically indistinguishable | ⬜ |
| 7 | `scx_cfd/` | SCX审计下的神经计算流体力学 / Neural Computational Fluid Dynamics Under SCX Audit | 将SCX质量审计框架应用于神经CFD，多物理模型作为独立专家检测模拟噪声 | Applies SCX quality audit to neural CFD with multiple physics models as independent experts | ⬜ |
| 8 | `scx_multiphysics/` | SCX审计多物理场模拟：跨耦合物理域的质量保证 / SCX-Audited Multi-Physics Simulation: Quality Across Coupled Physical Domains | SCX多专家审计在多物理场耦合模拟中的质量保证框架 | SCX multi-expert quality assurance framework for coupled multi-physics simulations | ⬜ |
| 9 | `scx_climate/` | SCX审计气候建模：耦合地球系统预测中的认证不确定性量化 / SCX-Audited Climate Modeling: Certified Uncertainty Quantification in Earth System Prediction | 应用SCX多模型共识机制对气候模型进行认证不确定性量化 | Certified uncertainty quantification for climate models via SCX multi-model consensus | ⬜ |
| 10 | `scx_astronomy/` | SCX审计多信使天文学 / SCX-Audited Multi-Messenger Astronomy | SCX多专家审计框架在多信使天文学（引力波+电磁+中微子）中的应用 | SCX multi-expert audit applied to multi-messenger astronomy (gravitational + EM + neutrino) | ⬜ |
| 11 | `scx_nv_center/` | SCX审计NV色心 / SCX-Audited NV Centers | SCX审计框架在NV色心量子传感实验中的应用 | SCX audit framework applied to NV center quantum sensing experiments | ⬜ |
| 12 | `scx_pseudopotential/` | 神经赝势：SCX审计蒸馏的理论框架 / Neural Pseudopotentials via SCX-Audited Distillation: A Theoretical Framework | 在SCX审计范式下将VASP PAW赝势蒸馏为神经网络表示的理论框架 | Theoretical framework for distilling VASP PAW pseudopotentials into neural networks under SCX audit | ⬜ |

## 博弈论与经济 (Game Theory & Economics)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_economics/` | SCX审计宏观经济预测：结构断裂下的多模型共识 / SCX-Audited Macroeconomic Forecasting: Multi-Model Consensus under Structural Breaks | 将SCX共识机制应用于DSGE、VAR和ML模型的宏观经济预测审计 | SCX consensus applied to macroeconomic forecasting with DSGE, VAR, and ML models | ⬜ |
| 2 | `scx_business/` | SCX商业格局分析：全球AI基础设施的三层重构 / SCX Business Landscape Analysis: Three-Layer Restructuring of Global AI Infrastructure | 以SCX规范理论分析全球AI基础设施的商业格局重构 | SCX gauge-theoretic analysis of global AI infrastructure business restructuring | ✅ |
| 3 | `scx_company_valuation/` | SCX商业格局分析：全球AI基础设施的三层重构（公司估值版） / SCX Business Analysis: Global AI Infrastructure Restructuring (Company Valuation) | SCX框架下的公司估值分析，聚焦全球AI基础设施三层重构 | Company valuation under SCX framework, focused on three-layer AI infrastructure restructuring | ✅ |
| 4 | `scx_audit_economics/` | SCX审计经济学：后Yajie时代的审计阶级与新经济秩序 / SCX Audit Economics: Audit Class and New Economic Order in the Post-Yajie Era | 分析审计能力如何成为新的经济阶级划分标准，预测后Yajie时代的经济秩序重构 | How audit capability becomes new class divider; predicts economic order restructuring in post-Yajie era | ✅ |
| 5 | `scx_quant_finance/` | SCX审计量化金融 / SCX-Audited Quantitative Finance | SCX多专家审计框架在量化金融模型验证和风险管理中的应用 | SCX multi-expert audit applied to quantitative finance model validation and risk management | ⬜ |
| 6 | `scx_supply_chain/` | SCX审计供应链可追溯性 / SCX-Audited Supply Chain Traceability | SCX审计框架在供应链追溯和验证中的应用，多专家确认货物流转 | SCX audit for supply chain traceability: multi-expert verification of goods flow | ⬜ |
| 7 | `scx_elections/` | SCX审计选举诚信 / SCX-Audited Electoral Integrity | SCX多专家审计在选举诚信验证中的应用，多独立观察者检测异常 | SCX multi-expert audit for electoral integrity: independent observers detect anomalies | ⬜ |
| 8 | `scx_blockchain/` | SCX审计区块链共识 / SCX-Audited Blockchain Consensus | 将SCX多专家审计原则应用于区块链共识机制设计 | Applies SCX multi-expert audit principles to blockchain consensus mechanism design | ⬜ |

## 协议与治理 (Protocol & Governance)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_governance/` | 治理的SCX审计 / SCX Audit of Governance | SCX审计框架在治理结构和决策过程中的应用 | SCX audit framework applied to governance structures and decision-making processes | ⬜ |
| 2 | `scx_world_government/` | 世界审计治理 / World Audit Governance | SCX审计治理在全球尺度上的应用：审计作为世界政府的核心机制 | SCX audit governance at global scale: audit as core mechanism for world government | ✅ |
| 3 | `scx_protocol_governance/` | SCX协议治理：维护者轮换博弈论与免信任架构 / SCX Protocol Governance: Maintainer Rotation Game Theory and Trustless Architecture | SCX协议的维护者轮换博弈论分析，设计免信任的治理架构 | Game-theoretic analysis of maintainer rotation for SCX protocol with trustless governance architecture | ✅ |
| 4 | `scx_maintainer_analysis/` | SCX协议维护者候选人分析 / SCX Protocol Maintainer Candidate Analysis | 对SCX协议维护者候选人的系统性偏差分析，g=0条件下的候选人评估 | Systematic bias analysis of SCX protocol maintainer candidates under g=0 condition | ✅ |
| 5 | `scx_meta_audit/` | 元审计协议形式化：谁审计审计者 / Formalizing the Meta-Audit Protocol: Who Audits the Auditor | 严格形式化元审计协议，回答审计的自反性问题，维护者偏差g的形式化定义与检测 | Rigorous formalization of meta-audit protocol: self-referential audit, maintainer bias g detection | ✅ |
| 6 | `scx_law/` | SCX审计法律证据 / SCX-Audited Legal Evidence | SCX多专家审计框架在法律证据验证和司法决策中的应用 | SCX multi-expert audit applied to legal evidence verification and judicial decision-making | ⬜ |
| 7 | `scx_security/` | SCX审计网络安全 / SCX-Audited Cybersecurity | SCX审计框架在网络安全威胁检测和防御中的应用 | SCX audit framework applied to cybersecurity threat detection and defense | ⬜ |
| 8 | `yajie_protocol/` | Yajie协议：技术锁定、审计主权与数据质量评估的防扩散逻辑 / The Yajie Protocol: Technology Lock-in, Audit Sovereignty, and Non-Proliferation Logic | Yajie协议——基于多专家一致性的数据审计算法及其作为技术锁定和审计主权工具的地缘政治分析 | Yajie Protocol: multi-expert consistency-based data auditing as tech lock-in and audit sovereignty tool | ⬜ |

## 社会推论 (Social Inference)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_social_media/` | SCX与社会媒体信息势能面：推荐算法作为信息势能隔离器 / SCX and Social Media Information Potential: Recommendation as Information Potential Isolator | 分析推荐算法如何创建信息势能隔离器，跨坐标系暴露的收敛条件 | How recommendation algorithms create information potential isolators; convergence conditions for cross-frame exposure | ✅ |
| 2 | `scx_community/` | 内河：SCX社区审计 / Inner River: SCX Community Audit | SCX审计框架在社区治理和共识形成中的应用 | SCX audit framework applied to community governance and consensus formation | ✅ |
| 3 | `scx_civilization/` | 文明不平等计：λ压制与解压制 / Civilization Inequality Gauge: λ Suppression and De-suppression | 分析文明寿命与不平等测度λ²的反比关系，λ压制机制（信息隔离、武力垄断、信仰合法性） | Civilization lifespan inverse to inequality λ²; λ suppression via information isolation, force monopoly, belief legitimacy | ✅ |
| 4 | `scx_environment/` | SCX与环境代际势能：气候变化作为跨代势能跳跃 / SCX and Environmental Intergenerational Potential: Climate Change as Cross-Generation Potential Jump | 气候变化作为跨代势能跳跃的SCX分析，定理10（边界锁定）在文明尺度的必然引爆 | Climate change as cross-generational potential jump; Thm10 boundary lock's inevitable detonation at civilizational scale | ✅ |
| 5 | `scx_education/` | 势能面几何与教育公正：评分的规范固定与势能阶梯管理 / Potential Surface Geometry and Educational Justice: Gauge Fixing of Grading and Potential Ladder Management | 以SCX势能面几何分析教育评分制度的公正性，悬崖效应与马太效应的形式化 | SCX potential geometry analysis of grading justice: formalization of cliff effects and Matthew effect | ⬜ |
| 6 | `scx_medicine/` | 势能面不齐与医学诊断：医生坐标系与患者坐标系的规范不对齐 / Potential Misalignment in Medical Diagnosis: Gauge Misalignment of Doctor and Patient Coordinates | 证明医生和患者坐标系之间的规范自由度是误诊的深层数学根因 | Proves gauge freedom between doctor and patient coordinate systems is the deep mathematical root of misdiagnosis | ⬜ |
| 7 | `scx_parenting/` | 亲子关系中的势能面几何与规范固定：青春期叛逆作为家庭尺度的定理11 / Potential Geometry in Parenting: Adolescent Rebellion as Family-Scale Theorem 11 | 分析青春期叛逆作为家庭尺度势能跳跃的SCX表现形式 | Adolescent rebellion analyzed as family-scale potential jump manifestation of SCX dynamics | ⬜ |
| 8 | `scx_peer_review/` | SCX与科学同行评审势能审计：评审者数量M与坐标系对齐 / SCX and Scientific Peer Review Potential Audit: Reviewer Count M and Coordinate Alignment | 同行评审作为SCX势能审计的实例化：评审者数量M与坐标系对齐作为科学知识生产的规范条件 | Peer review as SCX potential audit instance: reviewer count M and coordinate alignment as science production norm | ⬜ |
| 9 | `scx_art/` | SCX与艺术创造的势能规范：制造受控的势能跳跃 / SCX and the Potential Norm of Artistic Creation: Manufacturing Controlled Potential Jumps | 艺术创造作为制造受控势能跳跃的过程，平等论框架下的审美经验几何 | Artistic creation as manufacturing controlled potential jumps; aesthetic geometry under egalitarian framework | ⬜ |
| 10 | `scx_journalism/` | SCX审计新闻验证 / SCX-Audited News Verification | SCX多专家审计在新闻真实性和信息来源验证中的应用 | SCX multi-expert audit for news authenticity and source verification | ⬜ |
| 11 | `scx_personal_ethics/` | SCX个人伦理：面对数据造假要求的数学最优策略 / SCX Personal Ethics: Mathematical Optimal Strategy Against Data Falsification Demands | 在SCX审计框架下，面对上级造假要求时个人的数学最优策略——诚实是严格占优策略 | Under SCX audit, honesty is the strictly dominant strategy when superiors demand data falsification | ⬜ |
| 12 | `scx_philosophy_education/` | SCX与教育哲学：省定理的教育含义 / SCX and Philosophy of Education: Educational Implications of the Conservation Theorem | 从SCX公理推导省定理、梯度悬崖、平等收敛和多样性必要性四个教育哲学定理 | Derives four educational philosophy theorems from SCX axioms: conservation, gradient cliffs, equality convergence, diversity necessity | ⬜ |
| 13 | `scx_philosophy_law/` | SCX与证据法：法哲学的形式化 / SCX and Evidence Law: Formalization of Legal Philosophy | 以SCX信息论公理严格形式化法哲学核心问题：证据效力、举证责任、交叉验证、法律平等 | Rigorous formalization of legal philosophy via SCX: evidentiary weight, burden of proof, cross-examination, equality before law | ⬜ |
| 14 | `scx_philosophy_science/` | SCX与科学共识：科学哲学的形式化 / SCX and Scientific Consensus: Formalization of Philosophy of Science | 从SCX公理严格推导科学共识、范式转移、可证伪性和复现危机的数学条件 | Rigorous derivation of scientific consensus, paradigm shift, falsifiability, and replication crisis conditions from SCX axioms | ⬜ |
| 15 | `scx_geopolitics/` | SCX审计地缘政治 / SCX-Audited Geopolitics | SCX多专家审计框架在地缘政治分析和冲突预测中的应用 | SCX multi-expert audit applied to geopolitical analysis and conflict prediction | ✅ |
| 16 | `scx_prize/` | SCX奖宣言：审计替代诺贝尔——在可审计标准下重新定义科学卓越 / SCX Prize Manifesto: Audit Replaces Nobel — Redefining Scientific Excellence Under Auditable Standards | 提出以SCX审计标准替代传统科学奖励体系，在可审计标准下重新定义科学卓越 | Proposes replacing traditional science prizes with SCX audit standards for redefining scientific excellence | ⬜ |
| 17 | `scx_collective_intelligence/` | 集体智能：Condorcet陪审团定理的现代形式化 / Collective Intelligence: Modern Formalization of Condorcet Jury Theorem | 从SCX定理1出发，形式化异质专家加权、多样性-规模权衡、相关性结构和策略性投票检测 | From SCX Thm1: formalizes heterogeneous weighting, diversity-scale tradeoff, correlation structure, and strategic voting detection | ⬜ |
| 18 | `scx_genomics/` | SCX审计基因组学 / SCX-Audited Genomics | SCX审计框架在基因组数据分析和变异检测中的应用 | SCX audit framework applied to genomic data analysis and variant detection | ⬜ |

## 工程实现 (Engineering)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_method/` | 数据质量与模型架构：状态条件专家SCX / Data Quality and Model Architecture: State-Conditioned eXpertise | 证明数据清洗优于架构创新12-19倍，SCX方法论文（含methods.tex和supp.tex） | Data cleaning outperforms architecture innovation by 12-19x; SCX methods paper with methods and supplement | ⬜ |
| 2 | `scx_llm/` | 大语言模型数据策展的状态条件专家方法 / State-Conditioned Expertise for Language Model Data Curation | 将SCX多专家一致性检测应用于万亿token级LLM训练数据的质量策展 | SCX multi-expert consistency applied to trillion-token LLM training data quality curation | ⬜ |
| 3 | `scx_curation/` | 状态条件专家与策展-探索权衡 / State-Conditioned Expertise and the Curation-Exploration Tradeoff | 证明传统预处理式数据清洗在数学上自我挫败——无训练模型时标签噪声与样本难度不可区分 | Traditional preprocessing data cleaning is mathematically self-defeating: noise vs difficulty indistinguishable without trained models | ⬜ |
| 4 | `scx_ml_audit/` | SCX审讯：机器学习模型的审计 / The SCX Inquisition: Auditing Machine Learning Models | SCX审计协议在机器学习模型审查中的应用框架 | SCX audit protocol framework for machine learning model examination | ⬜ |
| 5 | `scx_ml_history/` | SCX透镜：机器学习历史的审计视角 / The SCX Lens: Auditing Machine Learning History | 通过SCX审计框架重新审视机器学习历史发展中的关键节点和误区 | Re-examining key milestones and pitfalls in ML history through the SCX audit lens | ⬜ |
| 6 | `scx_ml_verdict/` | SCX裁决：对机器学习领域的审计判决 / The SCX Verdict: An Audit Judgment on the ML Field | 以SCX审计标准对当前机器学习领域实践的系统性裁决和评估 | Systematic judgment and evaluation of current ML practices under SCX audit standards | ⬜ |
| 7 | `scx_science_audit/` | SCX审计授权：科学研究的强制审计框架 / The SCX Audit Mandate: Mandatory Audit Framework for Scientific Research | 提出科学研究的强制SCX审计授权，所有科学声称必须经过多专家审计验证 | Mandatory SCX audit for all scientific claims: multi-expert verification required | ⬜ |
| 8 | `scx_review/` | 状态条件专家：跨领域数据质量——从不确定性原理到全球基础设施 / State-Conditioned Expertise: Data Quality Across Domains — From Uncertainty Principle to Global Infrastructure | SCX框架的综述论文，涵盖从核心原理到全球基础设施应用的完整图景 | SCX review paper covering the complete picture from core principles to global infrastructure applications | ⬜ |
| 9 | `scx_spring_framework/` | Spring统一多模态大模型框架：训练即审计的全模态智能架构 / Spring Unified Multimodal LLM Framework: Train-as-Audit Omnmodal Intelligence Architecture | Spring框架——训练即审计的全模态大模型统一架构设计 | Spring framework: unified multimodal LLM architecture where training is audit | ⬜ |
| 10 | `scx_spring_limits/` | Spring的边界：可审计性与不可审计性的数学极限 / Spring's Boundaries: Mathematical Limits of Auditability and Unauditability | 严格分析Spring框架的可审计性边界和不可审计性的数学极限 | Rigorous analysis of Spring framework's auditability boundaries and mathematical limits of unauditability | ⬜ |
| 11 | `scx_spring_md/` | Spring分子动力学：审计驱动的势函数 / Spring Molecular Dynamics: Audit-Driven Potential Functions | Spring框架在分子动力学模拟中的应用，审计驱动的势函数学习 | Spring framework applied to MD simulation: audit-driven potential function learning | ⬜ |
| 12 | `scx_spring_trainer/` | Spring自演化势函数训练器：训练即审计的MD势函数学习框架 / Spring Self-Evolving Potential Trainer: Train-as-Audit MD Potential Learning Framework | 第一个将训练过程本身作为审计过程的分子动力学势函数学习框架 | First MD potential learning framework where training itself is the audit process | ⬜ |
| 13 | `scx_moe_gauge/` | 势能面不齐：多专家路由中的规范自由度与MILP规范固定 / Potential Misalignment: Gauge Freedom and MILP Gauge Fixing in Multi-Expert Routing | MoE路由中专家势能面不齐的规范理论分析及混合整数线性规划规范固定方法 | Gauge-theoretic analysis of expert potential misalignment in MoE routing with MILP gauge fixing | ⬜ |
| 14 | `scx_agentic_audit/` | Agentic多智能体SCX：对抗性多智能体审计理论 / Agentic Multi-Agent SCX: Adversarial Multi-Agent Audit Theory | 将单智能体审计推广到多智能体对抗场景，含合谋检测、纳什均衡和审计下界定理 | Extends single-agent audit to multi-agent adversarial setting: collusion detection, Nash equilibrium, audit lower bounds | ⬜ |
| 15 | `scx_world_model/` | SCX审计世界模型 / SCX-Audited World Models | SCX审计框架在世界模型（world model）质量评估中的应用 | SCX audit framework for world model quality assessment | ⬜ |
| 16 | `egp_merging/` | 一致性约束专家合并：可迁移ACE机器学习原子间势 / Consistency-Constrained Expert Merging for Transferable ACE ML Interatomic Potentials | 解决不同化学域MLIP的安全合并问题，识别四类不一致源 | Safe merging of MLIPs across chemical domains by identifying four inconsistency sources | ⬜ |
| 17 | `situs_theory/` | Situs：物理锚定的位置编码与状态条件专家 / Situs: Physics-Anchored Positional Encoding for State-Conditioned Expertise | 基于可观测物理量的位置编码框架，增强多专家标签噪声检测的统计功效 | Physics-anchored positional encoding framework enhancing multi-expert noise detection statistical power | ⬜ |
| 18 | `situs_applications/` | SCX在空间中：跨科学领域的状态条件专家 / SCX in Space: State-Conditioned eXpertise Across Scientific Domains | SCX + Situs双层描述符框架在多个科学领域的跨域应用 | SCX + Situs two-layer descriptor framework applied across multiple scientific domains | ⬜ |
| 19 | `spring_config/` | Spring：具有可证收敛性的自进化守门人 / Spring: A Self-Evolving Gatekeeper with Provable Convergence | Spring自进化守门人算法的严格形式化，含Lyapunov收敛证明和记忆库复活机制 | Rigorous formalization of Spring self-evolving gatekeeper: Lyapunov convergence proof and memory revival | ⬜ |
| 20 | `taxonomic_nn/` | 神经网络分类学理论：从SCX公理系统推导ML已知现象 / Neural Network Taxonomy: Deriving Known ML Phenomena from SCX Axioms | 从SCX公理系统统一推导集成方法、深度效应、表示学习、LLM幻觉等六大ML现象的严格形式化 | Unified rigorous derivation of six ML phenomena (ensembles, depth, representation, hallucination, etc.) from SCX axioms | ⬜ |
| 21 | `scx_acad_mdta_ilh/` | 学术MDTA-ILH：SCX审计学术研究 / Academic MDTA-ILH: SCX-Audited Academic Research | SCX审计框架在学术研究（MDTA/ILH方法论）质量评估中的应用 | SCX audit applied to academic research quality assessment (MDTA/ILH methodology) | ✅ |

## 其他 (Other)

| # | 目录 (Directory) | 论文标题 (Paper Title) | 中文描述 (CN) | 英文描述 (EN) | 脚本状态 |
|---|-------------------|------------------------|---------------|---------------|----------|
| 1 | `scx_capstone/` | 一切皆可审计：不可审计的即是幻觉或紧致性不可分 / Everything is Auditable: What Cannot Be Audited Is Illusion or Compactness-Inseparable | SCX的顶点论文——提出可审计性作为实在性的判据，不可审计的即是幻觉或紧致性不可分 | SCX capstone: auditability as criterion of reality — the unauditable is illusion or compactness-inseparable | ✅ |
| 2 | `scx_resistance/` | 审计反抗悖论：被描述对象的反击及其自我暴露 / The Audit Resistance Paradox: Counterattack of the Described and Its Self-Exposure | 分析被审计对象对审计框架的反抗行为如何反而暴露其不可审计性 | How resistance to audit paradoxically exposes the unauditability of the resisting entity | ✅ |
| 3 | `scx_open_problems/` | SCX开放问题 / SCX Open Problems | SCX框架中尚未解决的开放数学问题和研究方向汇总 | Compendium of unsolved open mathematical problems and research directions in SCX | ✅ |
| 4 | `scx_grand_unification/` | SCX大统一理论 / SCX Grand Unification Theory | SCX框架中核心理论、物理方向和社会推论的大统一理论尝试 | Grand unification attempt connecting SCX core theory, physics, and social inference | ✅ |
| 5 | `scx_lambda/` | SCX λ方向性与λ<0发散情形 / SCX λ Directionality and λ<0 Divergence Cases | 分析SCX中λ参数的方向性和负值发散情形的数学性质 | Analysis of λ parameter directionality and negative divergence cases in SCX | ✅ |
| 6 | `scx_industry/` | SCX产业审计：六大行业多验证者收敛性分析 / SCX Industry Audit: Multi-Verifier Convergence Analysis Across Six Sectors | SCX审计在六大行业中的多验证者收敛性实证分析 | Empirical multi-verifier convergence analysis of SCX audit across six industry sectors | ✅ |
| 7 | `meta/` | SCX故事：规范固定问题如何成为不确定性原理 / SCX宣言 / The SCX Story: How a Gauge-Fixing Problem Became an Uncertainty Principle / The SCX Manifesto | SCX的起源叙事（从EGP规范固定到不确定性原理的演化史）和SCX宣言 | SCX origin narrative (evolution from EGP gauge fixing to uncertainty principle) and the SCX Manifesto | ⬜ |

---

## 验证脚本状态汇总

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 已有验证脚本 | 25 | 目录中存在 verify_*.py |
| ⬜ 待生成 | 71 | 暂无验证脚本 |

**总计：96 个论文目录，30 个验证脚本文件**

### 已有验证脚本的目录

- `scx_gauge_formalized/`: `verify_gauge.py`
- `scx_S_operator/`: `verify_S_operator.py`
- `scx_goodhart/`: `verify_goodhart.py`
- `scx_quantum_audit/`: `verify_quantum.py`
- `scx_instanton/`: `verify_tda.py`
- `scx_singularity/`: `verify_singularity.py`
- `scx_business/`: `verify_business.py`
- `scx_company_valuation/`: `verify_company_valuation.py`
- `scx_audit_economics/`: `verify_audit_economics.py`
- `scx_world_government/`: `verify_world_government.py`
- `scx_protocol_governance/`: `verify_protocol_governance.py`
- `scx_maintainer_analysis/`: `verify_maintainer_analysis.py`
- `scx_meta_audit/`: `verify_meta_audit.py`
- `scx_social_media/`: `verify_social_media.py`
- `scx_community/`: `verify_community.py`
- `scx_civilization/`: `verify_civilization.py`
- `scx_environment/`: `verify_environment.py`
- `scx_geopolitics/`: `verify_geopolitics.py`
- `scx_acad_mdta_ilh/`: `verify_acad_mdta_ilh.py`
- `scx_capstone/`: `verify_capstone.py`
- `scx_resistance/`: `verify_resistance.py`
- `scx_open_problems/`: `verify_open_problems.py`
- `scx_grand_unification/`: `verify_grand_unification.py`
- `scx_lambda/`: `verify_lambda.py`
- `scx_industry/`: `verify_industry.py`

---

*自动生成日期：2026-07-02*
*论文总数：197 篇 .tex 文件（含 theorems/ 14篇独立定理、supplementary/ 补充材料）*
*验证脚本：30 个文件（含 verify_common.py 共用模块）*
