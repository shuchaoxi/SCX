# SCX: State-Conditioned eXpertise

> **面向数据价值评估与专家引导学习的状态条件专家框架**

## 一句话

专家可靠性不是全局常数，而是状态条件函数。数据价值不是样本固有属性，而是由状态、专家可靠性和当前模型缺陷共同决定的条件量。

## 版本状态 — v0.3.0

| 指标 | 数值 |
|------|------|
| Python 文件 | 35 (`src/scx/` 6 子包, 34 模块) |
| 总源文件 | 108 (含实验、测试、文档、配置) |
| Python 代码行 | ~16,000 |
| 总行数 | ~43,000 |
| 单元测试 | **336 tests** (9 文件, 全部通过) |
| 数学命题/定理 | 5 (定义 + 命题 + 证明, `theory/propositions/`) |
| Agent 分析文档 | 6 份 (`CodexKnowledge/agent_outputs/`) |

### v0.3.0 新增功能

- **StateConditionedInfluence** — `valuation/influence.py`: 状态条件影响力，SCX 粗筛状态 + Influence 细筛样本
- **OnlineSCXFramework** — `core/online.py`: 增量状态更新 + 在线专家可靠性追踪 + 数据流实验
- **CIFAR 实验** — `experiments/cifar/`: 3 组实验（baselines, noise, routing），SCX-Noise F1=0.617 超 loss-based 2.5x
- **MedMNIST 实验** — `scx-health/experiments/`: 3 组实验（compress, noise, routing），30% 压缩 +6.00% 精度
- **Clean-room 认证** — `IP_NOTE.md` + `DEVELOPMENT_LOG.md` + `CLEAN_ROOM_CHECK.md`: 30 源文件零学校引用

## 5 篇论文谱系

SCX 是系列研究的第 2 篇。完整的 5 篇论文序列和依赖关系如下：

```
EGP (concrete, 材料方法) → SCX-Theory (⌘本框架) → SCX-MLIP (MLIP) → SCX-Sim (仿真) → SCX-Health (医学)
```

| 顺序 | 论文 | 工作目录 | 核心问题 | 目标期刊 | 数据状态 |
|------|------|---------|----------|----------|---------|
| **1** | **EGP**: Gauge-normalized expert merging for ACE/PACE | `egp/` | 多个 MLIP expert 在 ACE/PACE 下如何规范化、对齐、合并？ | npj Comput. Mater. / JCTC | AlN v3 已训练 |
| **2** | **SCX-Theory** (State-Conditioned eXpertise) | **`SCX/`** （本项目） | 专家可靠性和数据价值的数学定义；噪声 vs 可学习困难区分 | TMLR / AISTATS / arXiv | 数学框架 + 合成实验 (0 DFT) |
| **3** | **SCX-MLIP** (SCX 应用于 MLIP) | `SCX/` | SCX 理论 → state-conditioned expert reliability → residual maps → certified merge | Nat. Commun. / npj Comput. Mater. | 等待 Paper 1+2 |
| **4** | **SCX-Sim** (多保真仿真) | `SCX/` | 高成本仿真中如何根据状态选粗/细模型？ | Nat. Comput. Sci. | toy demo 可启动 |
| **5** | **SCX-Health** (医学数据估值) | `SCX/scx-health/` | 区分冗余/长尾高价值/错标/专家依赖的医学样本 | npj Digit. Med. | MedMNIST 已下载 |

> **发表策略**: EGP Paper 1 先发（有完整 DFT 数据）→ SCX-Theory arXiv 占坑 → SCX-MLIP 整合两者投稿 → SCX-Sim / SCX-Health 跨领域扩展。

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
├── theory/                  # 数学框架（5 命题/定理 + 证明）
│   ├── README.md
│   └── propositions/
│       ├── 04_compression_fidelity.md
│       └── 05_expert_governance_protocol.md
├── src/scx/                 # SCX 框架 Python 包
│   ├── core/                # 框架核心（SCXFramework, Config, Metrics）
│   ├── state/               # 状态空间（Discovery, Assignment, Robustness）
│   ├── expert/              # 专家管理（Registry, Reliability, Router, Conflict）
│   ├── valuation/           # 数据估值（Learnability, Noise, Redundancy, Classifier, Influence）
│   └── action/              # 行动策略（Acquisition, Compress, Policy）
├── experiments/             # 验证实验
│   ├── synthetic/           # 合成 2D 实验
│   ├── cifar/               # CIFAR-10/100 基准
│   ├── ml_benchmarks/       # 通用 ML 基准
│   └── mlip_case/           # MLIP 科学案例
├── scx-health/              # 医学数据估值子项目
│   ├── data/                # MedMNIST + HAM10000
│   ├── src/scx_health/      # scx-health Python 包
│   └── experiments/         # compress / noise / routing
├── tests/                   # 单元测试（9 文件, 336 tests）
├── paper/                   # 论文草稿 + 参考文献
├── outputs/                 # 实验输出 + 图表
├── images/                  # 概念图
├── pyproject.toml
└── .gitignore
```

## 核心公式

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )

V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s)
```

## 关键文件索引

| 想了解什么 | 读哪个 |
|-----------|--------|
| 项目总览（本文件） | `README.md` |
| AI 恢复 / 新成员入口 | `CodexKnowledge/START_HERE_CODEX.md` |
| 核心数学定义 | `CodexKnowledge/SCX_核心定义.md` |
| 开发 TODO 列表 | `CodexKnowledge/SCX_TODO.md` |
| 综合 TODO（含 IP/商业） | `CodexKnowledge/SCX_终极TODO.md` |
| 发展方向分析 | `CodexKnowledge/SCX_思想扩展_综合方案.md` |
| 关键决策记录 | `CodexKnowledge/决策日志.md` |
| 理论框架总览 | `theory/README.md` |
| 代码 API | `src/scx/`（各子包 `__init__.py`） |
| 测试套件 | `tests/`（9 文件, 336 tests） |
| IP 保护文档 | `IP_NOTE.md`, `DEVELOPMENT_LOG.md`, `CLEAN_ROOM_CHECK.md` |
| 医学子项目 | `scx-health/README.md` |

## 环境

- Python >= 3.9
- 依赖: numpy, scipy, pandas, scikit-learn, matplotlib, plotly
- 推理: `D:/SHEprogram/EGP/.venv/Scripts/python.exe`（可复用 EGP 环境）
- 超算: `ssh -p 24678 cxshu@219.139.78.251`（仅 MLIP 案例可能需要）
