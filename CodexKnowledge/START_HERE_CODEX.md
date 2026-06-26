# Codex Project Knowledge Start — SCX

Date: 2026-06-25

Project root:

`G:\Xiaogan_Supercomputing_data\SCX`

## 项目定位

**SCX: State-Conditioned eXpertise** — 面向数据价值评估与专家引导学习的状态条件专家性框架。

这是第 4 篇论文的工作目录，主题是**数学理论 + 合成实验 + 轻量 ML 验证**，不涉及大规模 DFT 计算。

与 EGP 的关系：
- **EGP** (`G:\Xiaogan_Supercomputing_data\egp`)：第 1-3 篇（ACE/PACE 专家合并、残差态误差地图、专家编译蒸馏）
- **SCX**（本项目）：第 4 篇（状态条件专家可靠性 → 数据价值理论）

## Operating Mode

Before substantial work:

1. Run `codegraph status`.
2. Read `CodexKnowledge\START_HERE_CODEX.md` (this file).
3. Read `CodexKnowledge\SCX_TODO.md` for current work items.
4. Read `CodexKnowledge\SCX_终极TODO.md` for comprehensive TODO list.
5. Read `CodexKnowledge\决策日志.md` when relevant.
6. Read `CodexKnowledge\工具状态.md` for tool configuration.
7. Read `CodexKnowledge\archive\项目状态_2026-06-25.md` for prior state (archived).
8. Read `CodexKnowledge\archive\后续任务.md` for prior task list (archived).

## Source Priority

1. Actual command output and current files.
2. `START_HERE_CODEX.md` and tool/project status files.
3. `theory/` — mathematical definitions and propositions.
4. `CodexKnowledge/` — all knowledge docs.
5. Previous discussion memory only as weak context.

## Tool Policy

- Use codegraph first for function/class/script lookup, call graph, and impact precheck.
- Use `rg` to verify codegraph results before interface changes, deletions, or renames.
- Use `markitdown` before reading PDF/Word/PPT/Excel files.

## Project Structure

```
SCX/
├── CodexKnowledge/          # 项目知识库
│   ├── START_HERE_CODEX.md # ← 本文件
│   ├── SCX_终极TODO.md     # 综合 TODO（含 IP/商业）
│   ├── SCX_TODO.md         # 开发待办
│   ├── SCX_核心定义.md     # 核心数学定义速查
│   ├── 决策日志.md         # 关键决策记录
│   ├── 工具状态.md         # 工具链状态
│   ├── agent_outputs/      # 6 Agent 分析文档
│   ├── archive/            # 过期文档归档
│   └── images/             # 讨论/会议配图
├── theory/                  # 数学框架（5 命题 + 证明）
│   ├── README.md           # 框架总览
│   └── propositions/       # 定理与命题
├── paper/                   # 论文相关
│   ├── paper_text/         # 论文草稿
│   ├── paper_sources/      # 参考文献
│   └── papers/             # 收集的论文 PDF
├── experiments/             # 验证实验
│   ├── synthetic/          # 合成 2D 实验
│   ├── cifar/              # CIFAR-10/100
│   ├── ml_benchmarks/      # 通用 ML 基准
│   └── mlip_case/          # MLIP 科学案例
├── scx-health/              # 医学数据估值子项目
├── src/scx/                 # SCX 框架代码（6 子包, 34 模块）
├── tests/                   # 单元测试（9 文件, 336 tests）
├── outputs/                 # 实验输出/图表
└── images/                  # 概念图/示意图
```

## 核心概念速查

### SCX (State-Conditioned eXpertise)

专家可靠性不是全局标量，而是状态条件函数：

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )
```

### 四大数据分类

| 类别 | 条件 | 动作 |
|------|------|------|
| **Valuable** | 高误差 + 高密度 + 高一致性 + 低冗余 | acquire (补样本) |
| **Redundant** | 低误差 + 高密度 + 已充分覆盖 | skip (跳过) |
| **Noisy** | 高误差 + 低密度 + 低一致性 | downweight/discard (降权/丢弃) |
| **Expert-dependent** | 仅有特定专家可靠 | route to expert (路由到专家) |

### 状态数据价值

```
V(s) = r̄(s) · ρ(s) · L(s) · [1-D(s)] · max_m SCX_m(s)
```

- `r̄(s)`: 状态平均误差
- `ρ(s)`: 状态出现概率
- `L(s)`: 可学习性
- `D(s)`: 冗余度

## Quick Reference

| 想了解什么 | 读哪个 |
|---|---|
| 完整对话记录 | `CodexKnowledge/与GPT的讨论2026-06-26-07-49.md` |
| AI 恢复入口 | `CodexKnowledge/START_HERE_CODEX.md` (本文件) |
| 核心数学定义 | `CodexKnowledge/SCX_核心定义.md` |
| 开发 TODO | `CodexKnowledge/SCX_TODO.md` |
| 综合 TODO | `CodexKnowledge/SCX_终极TODO.md` |
| 理论框架总览 | `theory/README.md` |
| 项目当前状态 | `CodexKnowledge/SCX_思想扩展_综合方案.md` (v0.2.0 概览) |
| 过期文档 | `CodexKnowledge/archive/` (历史状态/旧计划) |

## 环境

- Python: `D:/SHEprogram/EGP/.venv/Scripts/python.exe` (可复用 EGP 环境)
- CodeGraph CLI: `D:\SHEprogram\claude-code\npm-global\codegraph.cmd`
- 超算: `ssh -p 24678 cxshu@219.139.78.251` (仅 MLIP 案例可能需要)
- 无 LaTeX 编译器，论文需 Overleaf
