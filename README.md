# SCX: State-Conditioned eXpertise

> **面向数据价值评估与专家引导学习的状态条件专家性框架**

## 一句话

专家可靠性不是全局常数，而是状态条件函数。数据价值不是样本固有属性，而是由状态、专家可靠性和当前模型缺陷共同决定的条件量。

## 核心公式

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )

V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s)
```

## 项目结构

```
SCX/
├── CodexKnowledge/          # 项目知识库（入口：START_HERE_CODEX.md）
├── theory/                  # 数学框架（定义 + 命题 + 证明）
│   ├── README.md
│   ├── definitions/
│   └── propositions/
├── paper/                   # 论文草稿 + 参考文献
│   ├── paper_text/
│   ├── paper_sources/
│   └── papers/
├── experiments/             # 验证实验
│   ├── synthetic/           # 合成 2D 实验
│   ├── ml_benchmarks/       # 通用 ML 基准
│   └── mlip_case/           # MLIP 科学案例（连接 EGP）
├── src/scx/                 # SCX 框架 Python 包
├── tests/                   # 单元测试
├── outputs/                 # 实验输出 + 图表
└── images/                  # 概念图
```

## 快速开始

```bash
# 初始化 codegraph
cd G:\Xiaogan_Supercomputing_data\SCX
D:\SHEprogram\claude-code\npm-global\codegraph.cmd init
D:\SHEprogram\claude-code\npm-global\codegraph.cmd index

# 让 AI 开工
# 复制 CodexKnowledge/新建会话_AI恢复prompt_2026-06-25.md 到新对话
```

## 论文线

| # | 主题 | 目录 |
|---|------|------|
| Paper 1 | ACE/PACE expert gauge + merge | `egp/` |
| Paper 2 | Residual-state error maps | `egp/` |
| Paper 3 | Expert compiler + distillation | `egp/` |
| **Paper 4** | **SCX: 状态条件数据价值理论** | **`SCX/` ← 本项目** |

## 核心贡献

1. **SCX Reliability**: 定义专家在状态 s 上的条件可靠性
2. **Data Valuation**: 区分 valuable / redundant / noisy / expert-dependent 四类数据
3. **State-Wise AL**: 从 point-wise 升级到 state-wise active learning
4. **Expert Routing**: 状态条件专家选择与标注路由
5. **Noise vs Hard State**: 区分可学习困难状态和不可约噪声

## 投稿目标

arXiv → Workshop (NeurIPS/ICML) → TMLR / AISTATS / UAI / Machine Learning
