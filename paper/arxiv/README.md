# SCX 论文索引

> 12 篇论文。一个理论。269 页。2026 年 6 月。

---

## 理论核心

| # | 论文 | 文件夹 | 做了什么 | 讲了一个什么故事 |
|---|------|--------|----------|------------------|
| 1 | **SCX 核心理论** | `scx_theory/` | Theorem 1-4：多专家共识噪声检测的 F1 指数下界、弱特征失效上界、噪声-难度不可区分（SCX 不确定性原理）、精确常数 minimax 最优 | M 个专家独立投票，错误率指数衰减。但噪声和困难在观测上不可区分——这是信息论硬边界，不是工程局限 |
| 2 | **Situs 理论** | `situs_theory/` | 物理位置编码的形式化——从 Laplace 核推导最优频率谱、3D 旋转编码、精确 Lipschitz 常数、信息论修正 | 给状态原子加上物理位置。不是 RoPE 那种统计旋转——是物理锚定的。当位置携带额外标签信息时，审计更准 |
| 3 | **Spring 收敛** | `spring_config/` | 自演化门控的 Lyapunov 收敛：参考集重放打破选择偏差循环、有限时间终止、四收敛路径 | 门控器不是一次性的——它在时间轴上自进化。先前丢弃的数据可以被复活。数学保证它收敛到自洽不动点 |
| 4 | **分类学理论** | `taxonomic_nn/` | 从 SCX 公理推导 ML 现象：集成、深度、表示学习、LLM 幻觉、自监督学习、深度是噪声时代的产物 | 机器学习可以用 5 个公式解释。Theorem 3 是旗舰——SCX 的"不确定性原理"。其余都是从它展开的推论 |

---

## 应用与扩展

| # | 论文 | 文件夹 | 做了什么 | 讲了一个什么故事 |
|---|------|--------|----------|------------------|
| 5 | **SCX in Space** | `situs_applications/` | 12 个科学场景的 Situs 适用性分析：基因组学、天文、遥感、气候、地震、半导体、医学影像等 | Situs 不是万能的。12 个场景中有些是天堂（基因组碱基对精度）、有些是陷阱（医学影像配准误差会反转信号）。诚实标注每一个 |
| 6 | **Theorem 3 单发** | `taxonomic_nn/theorem3.tex` | Theorem 3 的独立版本：噪声-难度不可区分 + M-seed LLM 幻觉应用。不依赖 SCX 公理体系 | 一颗子弹。不需要读任何其他论文。Theorem 3 自己就是 SCX 的"不确定性原理"——海森堡有测不准，SCX 有不可区分 |
| 7 | **SCX-LLM** | `scx_llm/` | SCX 与 LLM 的全组件映射：State Crystallization vs BPE、Situs vs RoPE、Yajie 审计层 vs Softmax | LLM 是缺审计层的 Yajie。BPE 是 State Crystallization 的退化特例。深度是噪声时代的产物——干净数据不需要那么多层 |

---

## 方法与工程

| # | 论文 | 文件夹 | 做了什么 | 讲了一个什么故事 |
|---|------|--------|----------|------------------|
| 8 | **EGP 合并** | `egp_merging/` | ACE 专家势函数的规范固定与合并：四种不一致性、后验正交投影、机器精度约束 | 独立训练的势函数不能直接合并。物理上存在规范自由度——我们找到了消除它的方法。SCX 蒸馏路径有望突破全周期表 |
| 9 | **SCX Curation** | `scx_curation/` | 数据策展必须先探索后清洗——这是数学必然性，不是工程选择 | Theorem 3 告诉你：你无法区分噪声和困难。所以别先清洗——先探索，让 Spring 帮你区分 |
| 10 | **SCX Method** | `scx_method/` | SCX 方法的完整描述：State Crystallization + Yajie + Spring 的算法流程 | 数据清洗效果是换架构的 12-19 倍。这不是工程 trick——是数学保证 |

---

## 综述与元论文

| # | 论文 | 文件夹 | 做了什么 | 讲了一个什么故事 |
|---|------|--------|----------|------------------|
| 11 | **SCX Review** | `scx_review/` | 六领域综述：SCX 在材料、生物、地球科学、天文、工程、LLM | SCX 不是为一个领域设计的——它是数据质量的统一语言 |
| 12 | **SCX 历史** | `meta/SCX_HISTORY.tex` | SCX 思想进化路线：从 EGP 规范固定到 Theorem 3 不确定性原理。8 章。附录含完整时间线 | "How a Gauge-Fixing Problem Became an Uncertainty Principle." 一个真实的科研故事——包括六条死路和修正的代数错误 |

---

## 独立定理

| 文件夹 | 定理 | 论文文件 |
|--------|------|----------|
| `theorems/` | 13 篇独立定理 | `theorem_aa_alignment.tex` · `theorem_ac_complexity.tex` · `theorem_ae_entropy.tex` · `theorem_ar_adversarial.tex` · `theorem_cd_causal.tex` · `theorem_fa_federated.tex` · `theorem_hc_human.tex` · `theorem_q_quantum.tex` · `theorem_ra_recursive.tex` · `theorem_ts_temporal.tex` · `theorem5_active_learning.tex` · `theorem6_protocol_game.tex` · `theorem7_cross_domain.tex` |
| `meta/` | 元文档 | `SCX_HISTORY.tex` · `SCX_MANIFESTO.tex` |

---

## 附属文件

| 文件 | 内容 |
|------|------|
| `AUDIT_SWORD.md` | 审计之剑声明——不禁止军事用途，但任何 SCX 使用可被独立审计 |
| `HARDWARE_ULTIMATE.md` | 面壁者终极限配置——¥257K |
| `ARCHITECTURE.md` | 四篇理论论文的关系图 + SCX 分层架构 |

---

## 故事线

**起点：** 一个实际问题——ACE 势函数怎么合并？（EGP）

**展开：** 四个定理——多专家共识、弱特征边界、不可区分性、minimax 最优（SCX 核心）

**细化：** 空间编码（Situs）、时间进化（Spring）、状态本体（State Crystallization）

**应用：** 12 个科学场景（SCX in Space）、LLM 全组件审计（SCX-LLM）

**独立：** Theorem 3 拆弹——SCX 的"不确定性原理"可独立发表

**哲学：** 审计之剑声明 + 电报公共品 + 面壁者准则

**记录：** SCX 历史——包括六条死路和修正的代数错误
