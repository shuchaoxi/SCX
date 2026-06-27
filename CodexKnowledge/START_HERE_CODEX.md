# START_HERE_CODEX — SCX 项目 AI 恢复入口

> 最后更新：2026-06-27
> 
> **如果你是 AI（Claude Code / GPT / 其他）被用户拉入这个项目，这是你的第一份阅读材料。**
> 读完这份文件再行动。不要跳过。

---

## 项目根目录

`G:\Xiaogan_Supercomputing_data\SCX`

## 一句话定位

**SCX: State-Conditioned eXpertise** — 状态条件专家性框架。核心主张：专家可靠性不是全局常数，而是状态条件函数。数据价值不由样本固有属性决定，而由状态、专家可靠性和当前模型缺陷共同决定。

---

## 版本状态

**v0.4.0-pre** (2026-06-27)

| 指标 | 数值 |
|------|------|
| Python 文件 | 35 (`src/scx/` 6 子包, 34 模块) |
| 单元测试 | **370 tests**（全部通过） |
| 核心定理 | **2**：定理 1（噪声检测保证）+ 定理 2（弱特征失效下界） |
| 旧命题 | 6 → 重构中（V(s) 已标记 deprecated） |
| GPU | ❌ 无（torch CPU-only，等显卡） |
| 超算 | ✅ cxshu（仅 EGP DFT 计算用） |

---

## 用户习惯与偏好

### 沟通风格
- **中文为主**，技术术语可中英混用
- 偏好**独立思考**：不要盲从 GPT 的建议，要从理论和审稿人视角出发独立判断
- 重视**严密性**：理论证明 > 实验 > 叙事。反对"空中楼阁"
- 喜欢用 `[[wikilink]]` 和 Obsidian 图谱组织知识

### 工作方式
- **多 Agent 并行**：能用 agent 并发的事不要串行
- **先规划后执行**：复杂任务先写 plan → 用户审批 → 再动手
- **文件合并癖**：多个文件讨论同一主题 → 合并为单一权威来源
- **TODO 狂热**：喜欢细粒度、可追踪、分优先级的任务清单
- **里程碑驱动**：喜欢看到进度（M1→M2→M3...）

### 价值观
- **学术优先权 > 商业**：先发论文占坑，再考虑商业
- **但商业不是不重要**：论文公开 L1-L2（数学+算法），工程 L4-L5 闭源保留
- **诚实面对失败**：弱特征失效不是 bug 是定理。审稿人喜欢看到作者知道方法的边界
- **Nature 是目标不是梦**：冲击正刊需要"惊人发现 + 理论保证 + 多领域证据"

### 当前心态
- 等显卡焦虑但不想浪费时间 → 把能做的理论/写作/CPU实验先做了
- 项目从 EGP 到 SCX 迭代太快，需要 Obsidian 库来追溯思想演化
- Paper 2（EGP gauge fixing）是最接近投稿的，想赶紧投出去建立根据地

---

## 5 篇论文谱系

> 唯一权威来源：`knowledge/05_决策/论文规划.md`

```
Paper 2 (先发, npj)    Paper 1 (旗舰, Nature)       Paper 3 (TMLR)    Paper 4 (JMLR)   Paper 5 (远期)
Gauge Fixing           Data Quality > Architecture   噪声检测理论        压缩保真理论       跨领域深挖
    ↓                        ↓                          ↓                  ↓               ↓
 纯应用                   Thm 1+2 轻量版              Thm 1+2 放松版     Thm 3 完善版      合作方驱动
 已有草稿+8图             跨领域 4 domain             5→3 假设           coreset 对话       Sim/Health
 1-2周可投稿              方法完整框架                 Bernstein/Talagrand Feldman-Langberg  /Robot
```

| # | 论文 | 核心问题 | 目标期刊 | 状态 |
|---|------|---------|----------|------|
| **2** | Gauge-Normalized ACE for AlN | shared+correction ACE 的 gauge freedom 识别与 post-hoc 修复 | npj Comput. Mater. | ✅ 已有草稿+8图，1-2周可投 |
| **1** | Data Quality > Model Architecture | 训练数据清洗 vs 架构改进：SCX 多专家一致性跨领域验证 | Nature Comput. Sci. | 🔴 等 GPU 补齐实验 |
| **3** | Noise Detection Theory | Thm 1+2 放松假设版 + Dawid-Skene + PAC-Bayes | TMLR / AISTATS | 📐 定理已证明 |
| **4** | Compression Fidelity Theory | Thm 3 (Prop 4 完善版) + coreset theory | JMLR | 📐 需完善 bound |
| **5** | Cross-Domain Deep Dive | 选一个领域做 10× 深度验证 | 待定 | ❌ 远期 |

**定理放置（方案 D）**：Paper 1 正文轻量陈述 + SI 完整证明。Paper 3+4 放松假设完整理论版。

---

## 商业化策略

**5 层资产模型**（来自与 GPT 的深度讨论）：

| 层级 | 内容 | 公开？ | 策略 |
|------|------|:----:|------|
| L1 数学理论 | Thm 1+2+3, 命题证明 | ✅ 全部发表 | 学术优先权 |
| L2 算法框架 | pseudocode, 核心流程 | ✅ 全部发表 | 学术优先权 |
| L3 最小代码 | reference implementation | ✅ 开源 | 复现论文用 |
| **L4 工程实现** | pipeline, dashboard, 云API | ❌ 闭源 | **商业壁垒** |
| **L5 数据/专家库** | 校准参数, 训练好的势函数 | ❌ 闭源 | **核心资产** |

**操作顺序**：invention disclosure → 专利评估 → 提交专利申请 → arXiv → 期刊投稿 → 开源最小代码 → 商业版

**关键认知**：公式定理全公开建立"SCX 是你发明的"学术事实。竞争对手可以读论文但不能复制工程调优和数据积累。Google 发表了 PageRank 公式，搜索引擎壁垒在爬虫和索引——不在公式。

---

## 快速导航：Obsidian 知识库

> Obsidian vault 根目录：`knowledge/`
> 
> 在 Obsidian 中打开 `knowledge/` 作为 vault，`Ctrl+G` 查看图谱。

| 我想了解... | 去这里 |
|------------|--------|
| 📘 **论文规划（唯一权威）** | `knowledge/05_决策/论文规划.md` |
| 🧮 定理 1+2 完整证明 | `theory/theorems/01_noise_detection_guarantee.md`, `02_weak_feature_failure.md` |
| 📋 **任务清单（全面推进）** | `knowledge/07_任务/README.md` |
| 🎯 里程碑追踪 | `knowledge/07_任务/里程碑.md` |
| 🔬 CPU 可做的实验 | `knowledge/07_任务/NOW_实验.md` |
| 🧮 待证的理论 | `knowledge/07_任务/NOW_理论.md` |
| 📝 论文推进任务 | `knowledge/07_任务/NOW_论文.md` |
| 💻 代码工程任务 | `knowledge/07_任务/NOW_代码.md` |
| ⏳ GPU 阻塞任务 | `knowledge/07_任务/GPU_等待.md` |
| 🔍 代码审查报告 | `knowledge/07_任务/代码审查_定理同步.md` |
| 📅 时间线 | `knowledge/01_时间线/README.md` |
| 🗺️ 思想演化地图 | `knowledge/00_入口/思想演化地图.md` |
| 📖 论文谱系 | `knowledge/00_入口/论文谱系.md` |
| 📊 项目状态 | `knowledge/03_项目/SCX-框架.md` |
| 💼 IP 策略 | `knowledge/05_决策/IP策略.md` |
| 🏠 知识库首页 | `knowledge/00_入口/🏠_Home.md` |

---

## 项目结构

```
SCX/
├── knowledge/                # 📓 Obsidian 知识库（AI 的主要导航界面）
│   ├── .obsidian/            # Obsidian 配置
│   ├── 00_入口/              # MOC：首页、思想演化地图、论文谱系
│   ├── 01_时间线/            # 每日开发日志（6/14 → 6/27）
│   ├── 02_概念/              # 原子概念笔记（互相 [[链接]]）
│   ├── 03_项目/              # 项目状态面板
│   ├── 04_对话/              # GPT + Agent 讨论摘要
│   ├── 05_决策/              # 决策日志、IP策略、论文规划
│   ├── 06_收件箱/            # 临时笔记
│   └── 07_任务/              # 任务清单 + 里程碑
│
├── CodexKnowledge/           # AI 恢复入口 + 原文档案（本文件在此）
│   ├── START_HERE_CODEX.md  # ← 你正在读的文件
│   ├── SCX_核心定义.md       # 核心数学定义速查
│   ├── SCX_发展史与成就.md   # 发展历程（含 EGP-V2 agent 修订）
│   ├── SCX_思想扩展_综合方案.md
│   ├── SCX_架构清单.md       # 全项目文件清单
│   ├── SCX_TODO_论文框架.md  # 五阶段论文计划（五审查员产出）
│   ├── 决策日志.md           # 关键决策记录
│   ├── 工具状态.md           # 工具链状态
│   ├── 论文框架审查报告_五审查员综合.md
│   ├── 整理_IP保护与开源策略与商业模式.md
│   ├── 整理_LLM战略与发展路线图.md
│   ├── 整理_框架与模块与论文分布.md
│   ├── 与GPT的讨论2026-06-26-07-49.md  # 244KB GPT 对话（IP/商业/开源）
│   ├── 与gpt的对话202606261332.md      # 158KB GPT 对话（架构/多领域）
│   ├── agent_outputs/        # 8 份 Agent 分析文档
│   ├── archive/              # 过期文档
│   └── images/               # 讨论配图
│
├── theory/                   # 数学框架
│   ├── README.md             # 框架总览
│   ├── definitions/          # 6 个核心定义
│   ├── propositions/         # 6 个旧命题（重构中）
│   └── theorems/             # ✅ 2 个新定理（完整证明）
│       ├── 01_noise_detection_guarantee.md  # Thm 1: F1 ≥ 1 - exp(-2MΔ²)/η
│       └── 02_weak_feature_failure.md       # Thm 2: F1 ≤ baseline + √(2δ)
│
├── paper/                    # 论文相关
│   └── paper1_mlip/          # Paper 2 (EGP) LaTeX 草稿 + 8 张图 + supplementary
│
├── src/scx/                  # SCX Python 包（6 子包, 34 模块, ~16,000 行）
│   ├── core/                 # SCXFramework, Config, Metrics
│   ├── state/                # StateDiscovery, StateAssignment
│   ├── expert/               # ExpertRegistry, ExpertReliability, ExpertRouter, ExpertConflict
│   ├── valuation/            # DataClassifier, Learnability, Noise, Redundancy, StateValue, Influence
│   └── action/               # Acquisition, Compress, Policy
│
├── tests/                    # 370 tests (9 文件)
├── experiments/              # 验证实验
│   ├── synthetic/            # 合成 2D 实验
│   ├── cifar/                # CIFAR-10/100（SCX-Noise F1=0.617）
│   ├── mlip_case/            # AlN v3 两层分析（F1=0.585）
│   └── ml_benchmarks/        # 通用 ML 基准
├── scx-health/               # 医学数据估值子项目（MedMNIST, Routing 93.22%）
├── outputs/                  # 实验输出/图表
├── images/                   # 概念图
├── 势函数合并/               # 6 份早期研究想法文档
└── pyproject.toml
```

---

## 核心定理速查

### Theorem 1: 多专家一致性噪声检测保证

**核心结果**：F1 ≥ 1 - (1/η) · Σ ρ_s · exp(-2M · Δ_s²)

**5 个假设**：(A1) 不相交训练集, (A2) 清洁数据条件独立, (A3) 有界损失, (A4) 均匀独立噪声, (A5) 状态同质性

**证明方法**：Hoeffding 不等式 + Chernoff 界 + 条件期望分解

**实践推论**：M ≥ 20 且平均专家错误率 ≤ 20% → F1 ≥ 0.95

**代码位置**：`src/scx/valuation/state_value.py` → `noise_detection_f1_bound()`, `noise_consistency_score()`, `optimal_noise_threshold()`

### Theorem 2: 弱特征失效下界

**核心结果**：F1 ≤ F1_base + C_F · √(2δ)，其中 δ = I(φ(X); s(X))

**证明方法**：Fano 不等式 + 耦合论证 + Pinsker 不等式 + 数据处理不等式

**实践推论**：特征互信息 δ → 0 时 SCX 退化到随机基线。解释了 DermaMNIST 上的失效

**代码位置**：`src/scx/valuation/state_value.py` → `feature_strength_diagnostic()`

### V(s) 状态

旧 V(s) = r̄(s)·ρ(s)·L(s)·[1-D(s)]·maxSCX(s) 已标记 **deprecated**（循环定义不可修复）。Thm 1+2 替代了其理论功能。代码中 `acquisition_value()` 和 `compression_value()` 仍可用但 emit DeprecationWarning。

---

## 环境

| 资源 | 值 |
|------|-----|
| Python | `C:\Users\admin\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe` (3.11.9) |
| EGP venv (含 torch CPU) | `D:/SHEprogram/EGP/.venv/Scripts/python.exe` |
| GPU | ❌ 无（torch CPU-only） |
| CPU ML | ✅ numpy, scipy, sklearn, pandas |
| SCX 安装 | `pip install -e .` (370 tests pass) |
| 超算 | `ssh -p 24678 cxshu@219.139.78.251` (AlN v3 DFT 已生成) |
| Obsidian vault | `knowledge/` |
| LaTeX | 无本地编译器，论文用 Overleaf |

---

## AI 操作协议

### 每次会话启动
1. 读本文件（你正在做）
2. 扫一眼 `knowledge/07_任务/里程碑.md` 了解当前进度
3. 扫一眼 `knowledge/07_任务/README.md` 了解当前优先级

### 执行任务前
1. 先判断是否复杂到需要 plan mode
2. 能用 agent 并行的事不要串行
3. 改代码前先跑 `python -m pytest tests/ -v --tb=short` 确认基线
4. 改完后再次跑测试确认不破坏

### 理论工作
- 证明优先于实验
- 假设必须显式陈述
- 审稿人视角前置：每提出一个 claim，先问"审稿人会用什么理由 reject"

### 论文工作
- Paper 2 是当前焦点（最接近投稿）
- 不要混淆论文的贡献边界（EGP gauge fixing ≠ SCX noise detection）
- 公式浓度：Paper 1 低（Nature 风格），Paper 3+4 高（JMLR 风格）

### 商业化意识
- 区分"论文里写什么"和"代码里开源什么"
- L1-L2 全公开，L4-L5 闭源保留
- 期刊投稿前确认专利状态

---

## 当前阻塞与下一步

**阻塞**：GPU 未到 → AlN v3 去噪重训、CIFAR 完整训练、MedMNIST 强 backbone 无法进行

**当前可推进**（无 GPU 依赖）：
1. 🔴 Paper 2 收尾投稿（1-2 周）
2. 🟡 Paper 1 理论部分草稿（定理已就绪）
3. 🟡 UCI tabular 实验（CPU 可做）
4. 🟢 公开 MLIP 数据下载分析（CPU 可做）

**参考**：`knowledge/07_任务/` 下的所有任务文件

---

*本文件是 AI 恢复入口。用户每次与新的 AI 会话时，指示 AI 先读这个文件。*
