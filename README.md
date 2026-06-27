# SCX: State-Conditioned eXpertise

> **面向数据价值评估与专家引导学习的状态条件专家框架**

## 一句话

专家可靠性不是全局常数，而是状态条件函数。数据价值不是样本固有属性，而是由状态、专家可靠性和当前模型缺陷共同决定的条件量。

## 版本状态 — v0.4.0-pre

| 指标 | 数值 |
|------|------|
| Python 文件 | 37 (`src/scx/` 6 子包, 35 模块 + yajie.py) |
| 总源文件 | 125+ (含实验、测试、文档、配置) |
| Python 代码行 | ~18,000 |
| 总行数 | ~47,000 |
| 单元测试 | **427 tests** (11 文件, 全部通过) |
| 核心定理 | **3** (Theorem 1-3, `theory/theorems/`) |
| 命题/命题证明 | **6** (定义 + 命题 + 证明, `theory/propositions/`, `theory/definitions/`) |
| Agent 分析文档 | 6 份 (`CodexKnowledge/agent_outputs/`) |

### v0.4.0-pre 新增功能 (2026-06-27)

- **Theorem 1 (Multi-Expert Consistency for Noise Detection)** — 多专家一致性噪声检测定理，Chernoff bound 保证假阳性率
- **Theorem 2 (Weak Feature Failure Lower Bound)** — 弱特征状态下 SCX 必然失效的 Fano inequality 下界
- **Theorem 3 (Unidentifiability of Noise vs Difficulty)** — 噪声与困难样本本质不可区分的构造性证明
- **Proposition 1' (Global Regret Lower Bound)** — 全局最优路由策略的 regret 下界
- **Proposition 3' (State-Conditioned Weighting Advantage)** — Jensen 不等式证明状态条件加权优于全局加权
- **Proposition 4 (Compression Fidelity)** — 循环定义修复 (利用 Theorem 1)
- **StateValue 定理化重构** — `valuation/state_value.py`: 新增 theorem-based 方法 (noise_consistency_score, chernoff_bound, hoeffding_bound, feature_strength_diagnostic等)，旧 V(s) 方法标记 deprecated
- **yajie.py** — 雅洁数据清理器模块
- **Obsidian 知识库** — 新增 `knowledge/08_说明书/` (7 个定理解释文件)
- **Arrow analogy** — 已移除并归档到 `theory/archive/`

## 5 篇论文谱系

SCX 是系列研究的核心理论部分。完整的 5 篇论文序列和依赖关系如下：

```
EGP (concrete, 材料方法) → SCX-Theory (噪声检测) → SCX-Compress (压缩理论) → SCX-MLIP (MLIP) → SCX-Sim (仿真) / SCX-Health (医学)
```

| 顺序 | 论文 | 工作目录 | 核心问题 | 目标期刊 | 数据状态 |
|------|------|---------|----------|----------|---------|
| **1** | **EGP**: Gauge-normalized expert merging for ACE/PACE | `egp/` | 多个 MLIP expert 在 ACE/PACE 下如何规范化、对齐、合并？ | npj Comput. Mater. / JCTC | AlN v3 已训练 |
| **2** | **SCX-Theory**: State-Conditioned Noise Detection | **`SCX/`** | 多专家一致性如何保证噪声检测？噪声与困难不可区分性？ | TMLR / AISTATS / arXiv | 数学框架 + 合成实验 (0 DFT) |
| **3** | **SCX-Compress**: State-Conditioned Compression Theory | **`SCX/`** | 状态条件数据压缩的理论下界；弱特征失效边界 | TMLR / AISTATS / arXiv | 压缩定理 + low-rank 条件 |
| **4** | **SCX-MLIP** (SCX 应用于 MLIP) | `SCX/` | SCX 理论 → state-conditioned expert reliability → residual maps → certified merge | Nat. Commun. / npj Comput. Mater. | 等待 Paper 1+2 |
| **5** | **SCX-Sim / SCX-Health** (多保真仿真 / 医学) | `SCX/` | 高成本仿真中状态条件选模型；医学数据估值 | Nat. Comput. Sci. / npj Digit. Med. | toy demo 可启动 |

> **发表策略**: EGP Paper 1 先发（有完整 DFT 数据）→ SCX-Theory arXiv 占坑 → SCX-Compress 同步 → SCX-MLIP 整合两者投稿 → SCX-Sim / SCX-Health 跨领域扩展。

## 子项目: scx-health

`scx-health/` 是 SCX 框架在医学数据估值上的独立实验子项目。

- **数据**: MedMNIST (PathMNIST, DermaMNIST, BloodMNIST) + HAM10000
- **实验**: compress (coreset), noise (噪声检测), routing (专家路由)
- **状态**: 实验骨架已建，结果待分析
- 独立 README: `scx-health/README.md`

## 快速开始

```bash
# 环境
cd G:\Xiaogan_Supercomputing_data\SCX
python -m venv .venv                     # 或复用 EGP .venv
pip install -e .                         # 安装 scx 包
pip install -r experiments/cifar/requirements.txt

# 运行合成实验
python experiments/synthetic/run_experiment.py

# 运行 CIFAR 实验
python experiments/cifar/run_baselines.py

# 运行测试
python -m pytest tests/ -v --tb=short

# 启动 codegraph（可选）
D:\SHEprogram\claude-code\npm-global\codegraph.cmd init
D:\SHEprogram\claude-code\npm-global\codegraph.cmd index
```

## 项目结构

```
SCX/
├── CodexKnowledge/          # 项目知识库（入口: START_HERE_CODEX.md）
│   ├── START_HERE_CODEX.md  # AI 恢复/新成员入口
│   ├── SCX_核心定义.md      # 核心数学定义
│   ├── SCX_TODO.md          # 开发待办（Phase 1-3）
│   ├── SCX_终极TODO.md      # 综合 TODO（学术/代码/商业/IP）
│   ├── SCX_思想扩展_综合方案.md  # 8 个可发展方向
│   ├── 整理_*.md            # 策略分析（IP/LLM/框架分布）
│   ├── 与GPT的讨论*.md      # 完整对话记录
│   ├── 决策日志.md           # 关键决策记录
│   ├── 工具状态.md           # 工具链配置
│   ├── agent_outputs/       # 6 Agent 分析文档
│   ├── images/              # 讨论配图
│   └── archive/             # 过期文档归档
├── theory/                  # 数学框架（3 定理 + 6 命题 + 定义）
│   ├── README.md
│   ├── definitions/         # 核心数学定义
│   │   └── 01_state_conditioned_risk.md
│   ├── theorems/            # 核心定理
│   │   ├── README.md
│   │   ├── 01_noise_detection_guarantee.md
│   │   ├── 02_weak_feature_failure.md
│   │   └── 03_unidentifiability_theorem.md
│   ├── propositions/        # 命题 + 证明
│   │   ├── 01_global_ranking_insufficiency.md
│   │   ├── 01_regret_lower_bound.md
│   │   ├── 02_higherror_suboptimality.md
│   │   ├── 03_state_conditioned_weighting.md
│   │   ├── 03_state_conditioned_weighting_proof.md
│   │   ├── 04_compression_fidelity.md
│   │   ├── 05_expert_governance_protocol.md
│   │   └── 06_two_layer_state_discovery.md
│   └── archive/             # 过期理论文档
│       └── arrow_analogy_removed.md
├── knowledge/               # Obsidian 知识库
│   ├── 00_入口/             # 导航入口
│   ├── 01_时间线/           # 每日记录
│   ├── 02_概念/             # 核心概念解释
│   ├── 03_项目/             # 项目说明
│   ├── 04_对话/             # GPT + Agent 对话
│   ├── 05_决策/             # 决策记录
│   ├── 06_收件箱/           # 待整理
│   ├── 07_任务/             # 任务看板
│   └── 08_说明书/           # 定理非专家解释（7 files）
├── src/scx/                 # SCX 框架 Python 包
│   ├── core/                # 框架核心（SCXFramework, Config, Metrics）
│   ├── state/               # 状态空间（Discovery, Assignment, Robustness）
│   ├── expert/              # 专家管理（Registry, Reliability, Router, Conflict）
│   ├── valuation/           # 数据估值（Learnability, Noise, Redundancy, Classifier, Influence, StateValue）
│   ├── action/              # 行动策略（Acquisition, Compress, Policy）
│   └── yajie.py             # 雅洁数据清理器
├── experiments/             # 验证实验
│   ├── synthetic/           # 合成 2D 实验
│   ├── cifar/               # CIFAR-10/100 基准
│   ├── ml_benchmarks/       # 通用 ML 基准
│   └── mlip_case/           # MLIP 科学案例
├── scx-health/              # 医学数据估值子项目
│   ├── data/                # MedMNIST + HAM10000
│   ├── src/scx_health/      # scx-health Python 包
│   └── experiments/         # compress / noise / routing
├── tests/                   # 单元测试（11 文件, 427 tests）
├── paper/                   # 论文草稿 + 参考文献
├── outputs/                 # 实验输出 + 图表
├── images/                  # 概念图
├── pyproject.toml
└── .gitignore
```

## 核心公式

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )

V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s)    [DEPRECATED — 参见 Theorem 1-3]
```

> **v0.4.0-pre 重要变更**: 旧 V(s) 公式已标记 deprecated。数据估值请使用 Theorem 1 (noise_consistency_score), Theorem 2 (feature_strength_diagnostic), Theorem 3 (unidentifiability) 中的定理指导方法。见 `src/scx/valuation/state_value.py` 中的 theorem-based 方法。

## 关键文件索引

| 想了解什么 | 读哪个 |
|-----------|--------|
| 项目总览（本文件） | `README.md` |
| AI 恢复 / 新成员入口 | `CodexKnowledge/START_HERE_CODEX.md` |
| 核心数学定义 | `CodexKnowledge/SCX_核心定义.md`, `theory/definitions/` |
| 核心定理 (Theorem 1-3) | `theory/theorems/README.md` |
| 噪声检测定理 | `theory/theorems/01_noise_detection_guarantee.md` |
| 弱特征失效定理 | `theory/theorems/02_weak_feature_failure.md` |
| 不可区分定理 | `theory/theorems/03_unidentifiability_theorem.md` |
| 开发 TODO 列表 | `CodexKnowledge/SCX_TODO.md` |
| 综合 TODO（含 IP/商业） | `CodexKnowledge/SCX_终极TODO.md` |
| 发展方向分析 | `CodexKnowledge/SCX_思想扩展_综合方案.md` |
| 关键决策记录 | `CodexKnowledge/决策日志.md` |
| 理论框架总览 | `theory/README.md` |
| 代码 API | `src/scx/`（各子包 `__init__.py`） |
| 测试套件 | `tests/`（11 文件, 427 tests） |
| IP 保护文档 | `IP_NOTE.md`, `DEVELOPMENT_LOG.md`, `CLEAN_ROOM_CHECK.md` |
| 医学子项目 | `scx-health/README.md` |
| 定理非专家解释 | `knowledge/08_说明书/README.md` |

## 环境

- Python >= 3.9
- 依赖: numpy, scipy, pandas, scikit-learn, matplotlib, plotly
- 推理: `D:/SHEprogram/EGP/.venv/Scripts/python.exe`（可复用 EGP 环境）
- 超算: `ssh -p 24678 cxshu@219.139.78.251`（仅 MLIP 案例可能需要）
