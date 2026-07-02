#!/usr/bin/env python3
"""Second-pass Chinese→English translation for remaining fragments."""
import re, os, sys

# Additional translations for remaining Chinese chars
# These target the specific remaining fragments identified in pass 1
TRANSLATIONS_V2 = [
    # === Compounds involving the remaining chars ===
    # 定 family
    ("判定", "judge"),
    ("确定", "determine"),
    ("限定", "qualify"),
    ("给定", "given"),
    ("固定", "fixed"),
    ("决定", "decide"),
    ("假定", "assume"),
    ("否定", "negate"),
    ("肯定", "affirm"),
    ("稳定", "stable"),
    ("特定", "specific"),
    ("定义", "define"),
    ("约定", "convention"),
    ("规定", "stipulate"),
    ("设定", "set"),
    ("鉴定", "identify"),
    ("标定", "calibrate"),
    ("测定", "measure"),
    ("裁定", "rule"),
    ("判定", "adjudicate"),
    
    # 家 family
    ("专家", "expert"),
    ("行家", "specialist"),
    ("学家", "scientist"),
    
    # 方 family
    ("方向", "direction"),
    ("方法", "method"),
    ("方案", "scheme"),
    ("方式", "manner"),
    ("方面", "aspect"),
    ("方差", "variance"),
    ("对方", "opponent"),
    ("双方", "both sides"),
    
    # 化 family - suffix meaning -ize/-ization
    ("形式化", "formalize"),
    ("量化", "quantify"),
    ("优化", "optimize"),
    ("最大化", "maximize"),
    ("最小化", "minimize"),
    ("正则化", "regularize"),
    ("标准化", "standardize"),
    ("归一化", "normalize"),
    ("离散化", "discretize"),
    ("数字化", "digitize"),
    ("自动化", "automate"),
    ("可视化", "visualize"),
    ("模块化", "modularize"),
    ("结构化", "structuralize"),
    ("抽象化", "abstract"),
    ("具体化", "concretize"),
    ("简化", "simplify"),
    ("复杂化", "complicate"),
    ("强化", "strengthen"),
    ("弱化", "weaken"),
    ("深化", "deepen"),
    ("浅化", "shallow"),
    ("进化", "evolve"),
    ("退化", "degenerate"),
    ("变化", "change"),
    ("转化", "transform"),
    ("异化", "differentiate"),
    ("同化", "assimilate"),
    ("分化", "differentiate"),
    ("合并化", "merge"),
    
    # 份 family
    ("部分", "part"),
    ("成分", "component"),
    ("身份", "identity"),
    ("份额", "share"),
    ("备份", "backup"),
    ("两份", "two copies"),
    ("几份", "several copies"),
    
    # 残 family
    ("残差", "residual"),
    ("残余", "residual"),
    ("残留", "remaining"),
    ("残存", "surviving"),
    
    # 版 family
    ("版本", "version"),
    ("原版", "original"),
    ("初版", "first edition"),
    ("修订版", "revised edition"),
    ("最终版", "final version"),
    
    # 编 family
    ("编码", "encode"),
    ("编辑", "edit"),
    ("编写", "write"),
    ("编译", "compile"),
    ("编解码", "codec"),
    
    # 贝 — part of 贝叶斯
    ("贝叶斯", "Bayes"),
    ("贝塞尔", "Bessel"),
    ("贝尔", "Bell"),
    ("贝努利", "Bernoulli"),
    
    # 丢 family
    ("丢弃", "drop"),
    ("丢失", "lose"),
    ("丢掉", "discard"),
    ("丢包", "packet loss"),
    
    # 息 family
    ("信息", "information"),
    ("消息", "message"),
    ("信号", "signal"),
    ("噪声", "noise"),
    ("休息", "rest"),
    ("利息", "interest"),
    ("出息", "promise"),
    ("信息量", "information content"),
    
    # 毁 family
    ("破坏", "break"),
    ("摧毁", "destroy"),
    ("毁灭", "annihilate"),
    ("毁坏", "damage"),
    ("损坏", "damage"),
    
    # 必 family
    ("必须", "must"),
    ("必要", "necessary"),
    ("必然", "inevitable"),
    ("必定", "certainly"),
    ("必需", "required"),
    ("务必", "be sure to"),
    ("未必", "not necessarily"),
    
    # 帮 family
    ("帮助", "help"),
    ("帮派", "faction"),
    ("帮忙", "assist"),
    
    # 奖 family
    ("奖励", "reward"),
    ("奖金", "bonus"),
    ("奖惩", "reward and punishment"),
    ("夸奖", "praise"),
    
    # 害 family
    ("损害", "harm"),
    ("伤害", "damage"),
    ("危害", "endanger"),
    ("有害", "harmful"),
    ("无害", "harmless"),
    ("厉害", "powerful"),
    
    # 擦 family
    ("摩擦", "friction"),
    ("擦除", "erase"),
    ("擦肩", "brush past"),
    
    # 晰 family
    ("清晰", "clear"),
    ("明晰", "lucid"),
    
    # 概 family
    ("概念", "concept"),
    ("概率", "probability"),
    ("概括", "summarize"),
    ("概况", "overview"),
    ("大概念", "rough concept"),
    
    # 水 family
    ("水平", "level"),
    ("水准", "standard"),
    ("水平面", "horizontal"),
    ("水平线", "horizon"),
    ("水分", "moisture"),
    
    # 洁 family
    ("清洁", "clean"),
    ("整洁", "tidy"),
    ("纯洁", "pure"),
    ("洁净", "clean"),
    
    # 结 family
    ("结果", "result"),
    ("结论", "conclusion"),
    ("结构", "structure"),
    ("结合", "combine"),
    ("结束", "end"),
    ("总结", "summary"),
    ("结晶", "crystallize"),
    
    # 线 family
    ("线性", "linear"),
    ("曲线", "curve"),
    ("直线", "straight line"),
    ("线路", "circuit"),
    ("在线", "online"),
    ("离线", "offline"),
    ("路线", "route"),
    
    # 般 family
    ("一般", "general"),
    ("普遍", "general"),
    ("通常", "usually"),
    
    # 访 family
    ("访问", "access"),
    ("采访", "interview"),
    ("拜访", "visit"),
    
    # 话 family
    ("对话", "dialogue"),
    ("说话", "speak"),
    ("话语", "discourse"),
    
    # 象 family
    ("现象", "phenomenon"),
    ("抽象", "abstract"),
    ("对象", "object"),
    ("象征", "symbolize"),
    ("想象", "imagine"),
    ("印象", "impression"),
    ("迹象", "sign"),
    ("气象", "meteorology"),
    
    # 赌 family
    ("赌博", "gamble"),
    ("赌注", "bet"),
    
    # 鞅 family
    ("鞅", "martingale"),
    ("半鞅", "semimartingale"),
    ("上鞅", "supermartingale"),
    ("下鞅", "submartingale"),
    
    # 务 family
    ("任务", "task"),
    ("服务", "service"),
    ("业务", "business"),
    ("事务", "affair"),
    ("务必", "must"),
    ("任务型", "task-oriented"),
    
    # 专 family
    ("专业", "specialized"),
    ("专门", "specialized"),
    ("专家", "expert"),
    ("专注", "focus"),
    ("专利", "patent"),
    ("专项", "special"),
    
    # 叶 family
    ("叶片", "blade"),
    ("树叶", "leaf"),
    ("中叶", "mid-"),
    ("末叶", "late"),
    ("初叶", "early"),
    ("中叶层", "middle layer"),
    
    # 坍 family
    ("坍塌", "collapse"),
    ("坍缩", "collapse"),
    
    # 备 family
    ("准备", "prepare"),
    ("完备", "complete"),
    ("具备", "possess"),
    ("装备", "equip"),
    ("备份", "backup"),
    ("预备", "preparatory"),
    ("防备", "guard against"),
    
    # 害 family (duplicate, already above)
    ("损害", "harm"),
    
    # 帮 (duplicate)
    ("帮助", "help"),
    
    # 吸 family
    ("吸收", "absorb"),
    ("吸引", "attract"),
    ("吸附", "adsorb"),
    ("吸取", "absorb"),
    ("吸引盆", "basin of attraction"),
    
    # 奖 (duplicate)
    ("奖励", "reward"),
    
    # 布 family
    ("分布", "distribute"),
    ("布置", "arrange"),
    ("布局", "layout"),
    ("散布", "scatter"),
    ("发布", "publish"),
    ("宣布", "announce"),
    
    # 弛 family
    ("弛豫", "relaxation"),
    ("松弛", "relax"),
    ("弛缓", "relax"),
    
    # 待 family
    ("等待", "wait"),
    ("对待", "treat"),
    ("期待", "expect"),
    ("待遇", "treatment"),
    ("接待", "receive"),
    ("虐待", "abuse"),
    
    # 憾 family
    ("遗憾", "regret"),
    ("缺憾", "shortcoming"),
    ("遗憾的", "unfortunately"),
    
    # 扯 family
    ("拉扯", "pull"),
    ("牵扯", "involve"),
    ("扯平", "even out"),
    ("胡扯", "nonsense"),
    
    # 拟 family
    ("模拟", "simulate"),
    ("拟合", "fit"),
    ("虚拟", "virtual"),
    ("比拟", "compare"),
    ("拟态", "mimicry"),
    
    # 控 family
    ("控制", "control"),
    ("监控", "monitor"),
    ("遥控", "remote control"),
    ("调控", "regulate"),
    
    # 摆 family
    ("摆脱", "escape"),
    ("摆放", "place"),
    ("摇摆", "swing"),
    ("摆动", "oscillate"),
    
    # 族 family
    ("族", "family"),
    ("家族", "family"),
    ("族类", "class"),
    ("族谱", "family tree"),
    ("函数族", "function family"),
    
    # 机 family
    ("机制", "mechanism"),
    ("机器", "machine"),
    ("机会", "opportunity"),
    ("随机", "random"),
    ("机动", "flexible"),
    ("机理", "mechanism"),
    ("机关", "organ"),
    
    # 染 family
    ("污染", "pollution"),
    ("感染", "infection"),
    ("传染", "contagion"),
    ("染色", "stain"),
    ("渲染", "render"),
    
    # 桥 family
    ("桥梁", "bridge"),
    ("桥接", "bridge"),
    ("桥段", "bridge segment"),
    
    # 测 family
    ("测量", "measure"),
    ("测试", "test"),
    ("检测", "detect"),
    ("预测", "predict"),
    ("推测", "infer"),
    ("监测", "monitor"),
    ("观测", "observe"),
    ("估算", "estimate"),
    ("猜测", "guess"),
    
    # 滑 family
    ("光滑", "smooth"),
    ("滑动", "slide"),
    ("滑移", "slip"),
    
    # 监 family
    ("监督", "supervise"),
    ("监控", "monitor"),
    ("监管", "regulate"),
    ("监视", "surveil"),
    ("监测", "monitor"),
    
    # 般 (duplicate)
    ("一般", "general"),
    
    # 节 family
    ("章节", "chapter"),
    ("节点", "node"),
    ("细节", "detail"),
    ("调节", "adjust"),
    ("节约", "save"),
    ("节目", "program"),
    ("节拍", "beat"),
    ("环节", "link"),
    ("季节", "season"),
    
    # 著 family
    ("显著", "significant"),
    ("著名", "famous"),
    ("著作", "work"),
    ("著称", "known as"),
    ("卓著", "outstanding"),
    ("显", "obvious"),
    
    # 虎 family
    ("老虎", "tiger"),
    ("马虎", "careless"),
    
    # 逃 family
    ("逃避", "escape"),
    ("逃逸", "escape"),
    ("逃跑", "flee"),
    ("逃出", "escape from"),
    ("选逃", "choose to escape"),
    
    # 逼 family
    ("逼迫", "force"),
    ("逼近", "approximate"),
    ("逼真", "realistic"),
    
    # 避 family
    ("避免", "avoid"),
    ("逃避", "escape"),
    ("回避", "evade"),
    ("躲避", "dodge"),
    ("避让", "yield"),
    
    # 乱 family
    ("混乱", "chaos"),
    ("杂乱", "disorder"),
    ("扰乱", "disturb"),
    ("混乱的", "chaotic"),
    
    # 伤 family
    ("损伤", "damage"),
    ("伤害", "harm"),
    ("受伤", "injured"),
    ("伤心", "sad"),
    ("创伤", "trauma"),
    
    # 估 family
    ("估计", "estimate"),
    ("评估", "evaluate"),
    ("估算", "estimate"),
    ("低估", "underestimate"),
    ("高估", "overestimate"),
    ("估值", "valuation"),
    ("估量", "estimate"),
    
    # 剖 family
    ("剖析", "dissect"),
    ("解剖", "anatomy"),
    ("剖面", "profile"),
    ("剖分", "partition"),
    
    # 劣 family
    ("劣势", "disadvantage"),
    ("恶劣", "severe"),
    ("低劣", "inferior"),
    ("退化", "degrade"),
    ("劣化", "degrade"),
    
    # 勃 family
    ("蓬勃", "vigorous"),
    ("勃发", "burgeon"),
    ("兴致勃勃", "enthusiastic"),
    
    # 吹 family
    ("吹牛", "boast"),
    ("吹嘘", "brag"),
    ("吹风", "blow"),
    
    # 呈 family
    ("呈现", "present"),
    ("呈交", "submit"),
    ("呈献", "offer"),
    ("呈报", "report"),
    ("呈递", "submit"),
    
    # 响 family
    ("影响", "affect"),
    ("响应", "respond"),
    ("反响", "reaction"),
    ("音响", "sound"),
    ("响亮", "loud"),
    ("响声", "noise"),
    
    # 幻 family
    ("幻想", "fantasy"),
    ("幻觉", "illusion"),
    ("虚幻", "illusory"),
    ("科幻", "science fiction"),
    
    # 播 family
    ("传播", "propagate"),
    ("播放", "play"),
    ("广播", "broadcast"),
    ("直播", "live stream"),
    ("散播", "spread"),
    
    # 改 family
    ("改变", "change"),
    ("改进", "improve"),
    ("修改", "modify"),
    ("改正", "correct"),
    ("改革", "reform"),
    ("改编", "adapt"),
    ("改写", "rewrite"),
    
    # 族 (duplicate)
    ("族", "family"),
    
    # 术 family
    ("技术", "technique"),
    ("艺术", "art"),
    ("学术", "academic"),
    ("算术", "arithmetic"),
    ("战术", "tactics"),
    ("手术", "surgery"),
    ("术语", "terminology"),
    
    # 汇 family
    ("词汇", "vocabulary"),
    ("汇总", "aggregate"),
    ("汇率", "exchange rate"),
    ("汇报", "report"),
    ("汇合", "converge"),
    ("汇集", "gather"),
    
    # 沟 family
    ("沟通", "communicate"),
    ("沟壑", "ravine"),
    ("鸿沟", "chasm"),
    ("沟道", "channel"),
    
    # 痕 family
    ("痕迹", "trace"),
    ("伤痕", "scar"),
    ("裂痕", "crack"),
    
    # 脊 family
    ("脊线", "ridge"),
    ("脊柱", "spine"),
    ("山脊", "ridge"),
    ("屋脊", "rooftop ridge"),
    
    # 藏 family
    ("隐藏", "hide"),
    ("包含", "contain"),
    ("收藏", "collect"),
    ("储藏", "store"),
    ("蕴藏", "contain"),
    ("暗藏", "conceal"),
    
    # 觉 family
    ("感觉", "feel"),
    ("视觉", "visual"),
    ("听觉", "auditory"),
    ("知觉", "perception"),
    ("察觉", "detect"),
    ("发觉", "discover"),
    ("自觉", "conscious"),
    ("直觉", "intuition"),
    ("错觉", "illusion"),
    
    # 野 family
    ("领域", "domain"),
    ("视野", "field of view"),
    ("野生", "wild"),
    ("野外", "outdoor"),
    ("分", "part"),
    
    # 偿 family
    ("补偿", "compensate"),
    ("赔偿", "compensate"),
    ("偿还", "repay"),
    ("偿付", "pay"),
    ("代偿", "substitute"),
    
    # 割 family
    ("分割", "segment"),
    ("切割", "cut"),
    ("划分", "divide"),
    ("割裂", "split"),
    ("分割线", "separator"),
    
    # 呈 (duplicate)
    ("呈现", "present"),
    
    # 天 family
    ("天然", "natural"),
    ("今天", "today"),
    ("明天", "tomorrow"),
    ("天空", "sky"),
    ("天气", "weather"),
    ("先天", "innate"),
    ("天然而然", "naturally"),
    ("天", "day"),
    
    # 毒 family
    ("病毒", "virus"),
    ("中毒", "poison"),
    ("毒性", "toxicity"),
    ("消毒", "disinfect"),
    ("无毒", "non-toxic"),
    ("毒品", "drug"),
    
    # 教 family
    ("教育", "education"),
    ("教学", "teaching"),
    ("教师", "teacher"),
    ("教训", "lesson"),
    ("教堂", "church"),
    ("教材", "textbook"),
    
    # 校 family
    ("校正", "correct"),
    ("校准", "calibrate"),
    ("学校", "school"),
    ("校对", "proofread"),
    ("校园", "campus"),
    
    # 审 family
    ("审查", "review"),
    ("审核", "audit"),
    ("审计", "audit"),
    ("审美", "aesthetic"),
    ("审批", "approve"),
    ("审稿", "review"),
    
    # 详 family
    ("详细", "detailed"),
    ("详尽", "exhaustive"),
    ("详情", "details"),
    ("详述", "elaborate"),
    
    # 亦 family
    ("亦即", "i.e."),
    ("亦然", "also"),
    ("亦可", "also can"),
    ("亦或", "or alternatively"),
    ("不亦", "isn't it"),
    
    # 兰 family
    ("兰", "Lan"),  # often part of a name
    ("格兰", "grant"),  # could be part of Ghadimi-Lan
    ("爱尔兰", "Ireland"),
    ("波兰", "Poland"),
    ("荷兰", "Netherlands"),
    ("芬兰", "Finland"),
    ("新西兰", "New Zealand"),
    
    # 德 family
    ("道德", "moral"),
    ("德国", "Germany"),
    ("品德", "character"),
    ("道德经", "Tao Te Ching"),
    
    # 救 family
    ("拯救", "save"),
    ("补救", "remedy"),
    ("救援", "rescue"),
    ("急救", "first aid"),
    
    # 簇 family
    ("簇", "cluster"),
    ("一簇", "a cluster"),
    ("簇状", "cluster-like"),
    ("簇群", "cluster group"),
    
    # 缘 family
    ("边缘", "edge"),
    ("边界", "boundary"),
    ("因缘", "cause"),
    ("缘由", "reason"),
    ("边缘化", "marginalize"),
    
    # 叠 family
    ("重叠", "overlap"),
    ("叠加", "superpose"),
    ("折叠", "fold"),
    ("叠代", "iterate"),
    
    # 启 family
    ("启动", "start"),
    ("启发", "inspire"),
    ("开启", "open"),
    ("启示", "reveal"),
    ("启动器", "starter"),
    
    # 斥 family
    ("排斥", "repel"),
    ("斥力", "repulsive force"),
    ("驳斥", "refute"),
    ("训斥", "reprimand"),
    
    # 普 family
    ("普遍", "universal"),
    ("普通", "ordinary"),
    ("普及", "popularize"),
    ("普通话", "Mandarin"),
    ("普适", "universal"),
    
    # 究 family
    ("研究", "research"),
    ("终究", "after all"),
    ("探究", "explore"),
    ("考究", "examine"),
    ("究竟", "exactly"),
    
    # 识 family
    ("知识", "knowledge"),
    ("认识", "recognize"),
    ("识别", "recognize"),
    ("标识", "mark"),
    ("共识", "consensus"),
    ("意识", "consciousness"),
    ("常识", "common sense"),
    
    # 锚 family
    ("锚定", "anchor"),
    ("锚点", "anchor point"),
    ("抛锚", "anchor"),
    
    # === More multi-char compounds ===
    ("世界", "world"),
    ("两个世界", "two worlds"),
    ("现实世界", "real world"),
    ("理想世界", "ideal world"),
    
    # Action-related
    ("操作", "operation"),
    ("动作", "action"),
    ("移动", "move"),
    ("移除", "remove"),
    ("删除", "delete"),
    ("添加", "add"),
    ("插入", "insert"),
    
    # Measurement
    ("测量", "measure"),
    ("计算", "compute"),
    ("统计", "statistics"),
    ("分析", "analyze"),
    ("综合", "synthesize"),
    
    # Comparison
    ("比较", "compare"),
    ("相对", "relative"),
    ("绝对", "absolute"),
    ("相似", "similar"),
    ("相同", "identical"),
    ("不同", "different"),
    
    # Logic
    ("如果", "if"),
    ("那么", "then"),
    ("否则", "otherwise"),
    ("因为", "because"),
    ("所以", "therefore"),
    ("虽然", "although"),
    ("但是", "but"),
    ("然而", "however"),
    ("并且", "and"),
    ("或者", "or"),
    ("否则话", "otherwise"),
    
    # Quantity
    ("所有", "all"),
    ("每个", "each"),
    ("任何", "any"),
    ("一些", "some"),
    ("许多", "many"),
    ("少量", "few"),
    ("大量", "large amount"),
    ("足够", "sufficient"),
    
    # Time
    ("现在", "now"),
    ("过去", "past"),
    ("未来", "future"),
    ("之前", "before"),
    ("之后", "after"),
    ("之间", "between"),
    ("期间", "during"),
    ("同时", "simultaneously"),
    
    # Quality
    ("正确", "correct"),
    ("错误", "incorrect"),
    ("精确", "precise"),
    ("准确", "accurate"),
    ("近似", "approximate"),
    ("严格", "rigorous"),
    
    # Common phrases
    ("例如", "for example"),
    ("包括", "including"),
    ("特别是", "especially"),
    ("尤其是", "particularly"),
    ("根据", "according to"),
    ("关于", "regarding"),
    ("对于", "for"),
    ("由于", "due to"),
    ("通过", "through"),
    ("按照", "according to"),
    ("除了", "except"),
    ("除非", "unless"),
    ("尽管", "despite"),
    ("无论", "regardless"),
    ("只要", "as long as"),
    ("只有", "only if"),
    ("直到", "until"),
    ("自从", "since"),
    
    # Verbal
    ("使用", "use"),
    ("利用", "utilize"),
    ("采用", "adopt"),
    ("应用", "apply"),
    ("提供", "provide"),
    ("产生", "produce"),
    ("导致", "lead to"),
    ("引起", "cause"),
    ("造成", "cause"),
    ("形成", "form"),
    ("组成", "compose"),
    ("构成", "constitute"),
    
    # Research
    ("实验", "experiment"),
    ("试验", "trial"),
    ("实证", "empirical"),
    ("理论", "theory"),
    ("实践", "practice"),
    ("实现", "implement"),
    ("执行", "execute"),
    
    # Data
    ("数据", "data"),
    ("样本", "sample"),
    ("特征", "feature"),
    ("属性", "attribute"),
    ("实例", "instance"),
    ("案例", "case"),
    
    # More specific
    ("边界条件", "boundary condition"),
    ("初始条件", "initial condition"),
    ("充分条件", "sufficient condition"),
    ("必要条件", "necessary condition"),
    ("充要条件", "necessary and sufficient condition"),
    ("能观性", "observability"),
    ("能控性", "controllability"),
    
    # === Single remaining char fallbacks ===
    # These catch any remaining single chars my compound list missed
    # Format: char that might survive alone
    
    # Additional common 2-char compounds
    ("展开式", "expansion"),
    ("表达式", "expression"),
    ("显示式", "explicit form"),
    ("隐式", "implicit form"),
    ("闭式", "closed form"),
    
    # Domain terms
    ("定义域", "domain"),
    ("值域", "range"),
    ("像集", "image set"),
    ("原像", "preimage"),
    
    # More from earlier leftover
    ("说明", "explain"),
    ("叙述", "describe"),
    ("刻画", "characterize"),
    ("描绘", "depict"),
    
    # Geometry
    ("几何", "geometry"),
    ("拓扑", "topology"),
    ("代数", "algebra"),
    ("微分", "differential"),
    ("积分", "integral"),
    ("偏微分", "partial differential"),
    
    # Additional
    ("近似式", "approximate expression"),
    ("准确度", "accuracy"),
    ("错误率", "error rate"),
    ("对抗", "adversarial"),
    ("鲁棒", "robust"),
    ("泛化", "generalize"),
    ("过拟合", "overfit"),
    ("欠拟合", "underfit"),
    
    # Physics/chemistry/materials
    ("位错", "dislocation"),
    ("掺杂", "doping"),
    ("取代", "substitute"),
    ("各向异性", "anisotropy"),
    ("各向同性", "isotropy"),
    ("压电", "piezoelectric"),
    ("铁电", "ferroelectric"),
    ("铁磁", "ferromagnetic"),
    ("反铁磁", "antiferromagnetic"),
    ("超导", "superconducting"),
    ("拓扑绝缘体", "topological insulator"),
    ("半金属", "semimetal"),
    ("半导体", "semiconductor"),
    ("绝缘体", "insulator"),
    ("导体", "conductor"),
    
    # Fluid
    ("流体", "fluid"),
    ("湍流", "turbulence"),
    ("层流", "laminar flow"),
    
    # Dynamics
    ("动力学", "dynamics"),
    ("运动学", "kinematics"),
    ("静力学", "statics"),
    ("热力学", "thermodynamics"),
    ("统计力学", "statistical mechanics"),
    ("量子力学", "quantum mechanics"),
    ("经典力学", "classical mechanics"),
    ("连续介质力学", "continuum mechanics"),
    
    # More organisms
    ("细体", "fine"),
    ("粗体", "coarse"),
    ("微观", "microscopic"),
    ("宏观", "macroscopic"),
    ("介观", "mesoscopic"),
    
    # Common compounds that may have been missed
    ("不对称", "asymmetric"),
    ("非线性", "nonlinear"),
    ("非平稳", "non-stationary"),
    ("非参数", "non-parametric"),
    ("非监督", "unsupervised"),
    ("非负", "non-negative"),
    ("非零", "non-zero"),
    ("非空", "non-empty"),
    ("非平凡", "non-trivial"),
    ("非光滑", "non-smooth"),
    ("非凸", "non-convex"),
    ("非凹", "non-concave"),
    ("非可微", "non-differentiable"),
    ("非连续", "discontinuous"),
    
    # Extra
    ("等价", "equivalent"),
    ("均匀", "uniform"),
    ("非均匀", "non-uniform"),
    ("平稳", "stationary"),
    ("遍历", "ergodic"),
    ("混合", "mixing"),
    ("可逆", "reversible"),
    ("不可逆", "irreversible"),
    
    # Verbs
    ("实现", "realize"),
    ("实施", "implement"),
    ("实行", "carry out"),
    ("运行", "run"),
    ("操作", "operate"),
    ("工作", "work"),
    ("处理", "process"),
    ("管理", "manage"),
    
    # More
    ("组织", "organize"),
    ("安排", "arrange"),
    ("设计", "design"),
    ("开发", "develop"),
    ("部署", "deploy"),
    ("维护", "maintain"),
    ("升级", "upgrade"),
    ("降级", "downgrade"),
    ("回滚", "rollback"),
    ("提交", "commit"),
    ("合并", "merge"),
    ("冲突", "conflict"),
    ("解决", "resolve"),
    ("修复", "fix"),
    ("调试", "debug"),
    ("追踪", "trace"),
    ("记录", "record"),
    ("日志", "log"),
    ("监控", "monitor"),
    ("报警", "alert"),
    ("通知", "notify"),
    ("报告", "report"),
    ("总结", "summarize"),
    ("回顾", "review"),
    ("计划", "plan"),
    ("预测", "predict"),
    ("优化", "optimize"),
    ("调整", "adjust"),
    ("配置", "configure"),
    ("安装", "install"),
    ("卸载", "uninstall"),
    ("启动", "start"),
    ("停止", "stop"),
    ("重启", "restart"),
    ("暂停", "pause"),
    ("继续", "continue"),
    ("完成", "complete"),
    ("结束", "end"),
    ("退出", "exit"),
    ("取消", "cancel"),
    ("确认", "confirm"),
    ("接受", "accept"),
    ("拒绝", "reject"),
    ("批准", "approve"),
    ("驳回", "reject"),
    ("请求", "request"),
    ("回复", "reply"),
    ("转发", "forward"),
    ("分享", "share"),
    ("收藏", "bookmark"),
    ("点赞", "like"),
    ("关注", "follow"),
    ("订阅", "subscribe"),
    ("注册", "register"),
    ("登录", "login"),
    ("注销", "logout"),
    ("认证", "authenticate"),
    ("授权", "authorize"),
    ("加密", "encrypt"),
    ("解密", "decrypt"),
    ("签名", "sign"),
    ("验证", "verify"),
    ("备份", "backup"),
    ("恢复", "restore"),
    ("导入", "import"),
    ("导出", "export"),
    ("上传", "upload"),
    ("下载", "download"),
    ("同步", "sync"),
    ("复制", "copy"),
    ("粘贴", "paste"),
    ("剪切", "cut"),
    ("撤销", "undo"),
    ("重做", "redo"),
    ("查找", "find"),
    ("替换", "replace"),
    ("排序", "sort"),
    ("过滤", "filter"),
    ("搜索", "search"),
    ("浏览", "browse"),
    ("导航", "navigate"),
    ("返回", "back"),
    ("前进", "forward"),
    ("刷新", "refresh"),
    ("加载", "load"),
    ("保存", "save"),
    ("打印", "print"),
    ("预览", "preview"),
    ("缩放", "zoom"),
    ("全屏", "fullscreen"),
    ("最小化", "minimize"),
    ("最大化", "maximize"),
    ("关闭", "close"),
    ("打开", "open"),
    ("新建", "new"),
    ("编辑", "edit"),
    ("删除", "delete"),
    ("重命名", "rename"),
    ("移动", "move"),
    ("复制", "copy"),
    ("链接", "link"),
    ("属性", "properties"),
    ("设置", "settings"),
    ("选项", "options"),
    ("偏好", "preferences"),
    ("帮助", "help"),
    ("关于", "about"),
    ("版本", "version"),
    ("更新", "update"),
]

# Sort: longer patterns first
TRANSLATIONS_V2.sort(key=lambda x: -len(x[0]))

def find_chinese_ranges(text):
    ranges = []
    i = 0
    while i < len(text):
        if '\u4e00' <= text[i] <= '\u9fff' or '\u3400' <= text[i] <= '\u4dbf':
            start = i
            while i < len(text) and ('\u4e00' <= text[i] <= '\u9fff' or '\u3400' <= text[i] <= '\u4dbf'):
                i += 1
            ranges.append((start, i))
        else:
            i += 1
    return ranges

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    before_count = len(find_chinese_ranges(content))
    
    result = content
    for chinese, english in TRANSLATIONS_V2:
        result = result.replace(chinese, english)
    
    after_count = len(find_chinese_ranges(result))
    
    if after_count > 0:
        ranges = find_chinese_ranges(result)
        # Show surviving fragments with context
        for start, end in ranges[:20]:  # Show first 20
            ctx_start = max(0, start-20)
            ctx_end = min(len(result), end+20)
            fragment = result[start:end]
            context = result[ctx_start:ctx_end].replace('\n', '\\n')
            print(f"  [{fragment}] in: ...{context}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    
    return before_count, after_count

def main():
    files = [
        "theory/self_evolution/final_review_jmlr.tex",
        "theory/self_evolution/final_review_nature.tex",
        "theory/self_evolution/README.tex",
        "theory/self_evolution/situs_final_verification.tex",
        "theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex",
        "theory/self_evolution/ppe_rigorous_derivation.tex",
        "theory/self_evolution/situs_physical_validation.tex",
        "theory/self_evolution/spring_convergence_analysis.tex",
        "theory/self_evolution/spring_hostile_review.tex",
        "theory/theorems/01_noise_detection_guarantee.tex",
        "theory/theorems/02_weak_feature_failure.tex",
        "theory/theorems/03_unidentifiability_theorem.tex",
    ]
    
    base = "F:/scx"
    total_before = 0
    total_after = 0
    
    for f in files:
        path = os.path.join(base, f)
        if not os.path.exists(path):
            print(f"MISSING: {path}")
            continue
        print(f"\n=== {f} ===")
        before, after = translate_file(path)
        total_before += before
        total_after += after
        print(f"  {before} → {after} fragments")
    
    print(f"\n=== TOTAL: {total_before} → {total_after} ===")

if __name__ == "__main__":
    main()
