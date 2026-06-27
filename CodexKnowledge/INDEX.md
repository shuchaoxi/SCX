# SCX CodexKnowledge 索引

> 更新：2026-06-26 | SCX v4.0 Phase A

## 当前状态

- **代码**：v4.0 Phase A 完成（通用模块化架构，抽象基类 + YAML 域配置）
- **测试**：370 tests 通过
- **实验**：CIFAR (v1+noise), MedMNIST (v1+v2), AlN v3 (一层+两层)
- **论文**：5 篇序列（EGP→SCX-Theory→SCX-MLIP→SCX-Sim→SCX-Health）
- **GitHub**：`git@github.com:shuchaoxi/State-Conditioned-eXpertise.git`（私有）

---

## 文件导航

### 核心定义与规划
| 文件 | 用途 |
|------|------|
| `SCX_核心定义.md` | 核心数学定义、符号表、命题索引 |
| `SCX_思想扩展_综合方案.md` | Agent 讨论产出的完整扩展方案 |
| `SCX_通用模块化架构设计.md` | v4.0 通用模块化架构设计 |
| `START_HERE_CODEX.md` | 新会话入口（AI 恢复 prompt） |

### TODO（当前唯一有效）
| 文件 | 用途 |
|------|------|
| `SCX_TODO_2026-06-26.md` | **当前 TODO** — Phase 1-4 任务跟踪 |

已归档（`archive/`）：`SCX_TODO.md`, `SCX_终极TODO.md`, `SCX_TODO_v4_通用模块化.md`, `SCX_规划_v4_通用模块化.md`

### GPT 讨论整理
| 文件 | 内容 |
|------|------|
| `整理_框架与模块与论文分布.md` | SCX 框架结构 + 5 篇论文分工 |
| `整理_IP保护与开源策略与商业模式.md` | IP 保护、开源策略、商业模式 |
| `整理_LLM战略与发展路线图.md` | LLM 集成战略 |

### Agent 输出
| 文件 | 内容 |
|------|------|
| `agent_outputs/01_SCX_核心框架_数学分析.md` | 核心数学框架 |
| `agent_outputs/02_SCX_子模块_详细设计.md` | 子模块设计 |
| `agent_outputs/03_竞争分析_数据估值与主动学习.md` | 竞争分析：数据估值 |
| `agent_outputs/04_竞争分析_MoE与蒸馏.md` | 竞争分析：MoE/蒸馏 |
| `agent_outputs/05_数学根源与证明.md` | 数学根源 |
| `agent_outputs/06_实现架构与实验设计.md` | 实现架构 |
| `agent_outputs/07_两层描述符_错误驱动状态发现.md` | 两层描述符方案 |

### 原始对话
| 文件 | 说明 |
|------|------|
| `与gpt的对话202606261332.md` | 2026-06-26 GPT 对话（9011行） |
| `与GPT的讨论2026-06-26-07-49.md` | 2026-06-26 早期讨论 |

### 其他
| 文件 | 用途 |
|------|------|
| `决策日志.md` | 关键决策记录 |
| `工具状态.md` | 工具配置状态 |

---

## 仓库结构速查

```
SCX/
├── src/scx/                  ← Python 库
│   ├── core/                 在线跟踪、SCX 核心
│   ├── encoders/             ErrorDrivenEncoder, MLIPEncoder, 抽象基类
│   ├── state/                两层状态发现、鲁棒性
│   ├── valuation/            数据分类、自适应阈值、影响力
│   └── action/               压缩、路由
├── tests/                    370 tests
├── theory/
│   ├── definitions/          核心数学定义 + 符号表
│   └── propositions/         Prop 01-06（含两层描述符）
├── experiments/
│   ├── cifar/                CIFAR-10/100 实验
│   ├── mlip_case/            AlN v3 SCX 分析
│   ├── ml_benchmarks/        通用 ML 基准
│   └── synthetic/            合成数据
├── scx-health/               MedMNIST 实验
│   ├── experiments/          compress/noise/routing 脚本
│   └── results/              v1 + v2 报告
├── paper/                    论文草稿
└── CodexKnowledge/           ← 本目录（知识管理）
```

## 当前优先级

1. **P0**：Compress 实验修复（GPU + ResNet-18，恢复 v1 的 clean win）
2. **P1**：Noise 实验用状态相关噪声（非均匀）
3. **P2**：Benchmark suite + Online SCX
4. **论文**：Paper 4 (SCX) §4.3 压缩定理 + §6.2 通用实验
