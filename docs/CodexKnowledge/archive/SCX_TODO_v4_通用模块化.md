# SCX TODO v4 — 通用模块化重构

> 生成时间：2026-06-26
> 替代：`SCX_TODO_2026-06-26.md`（被本文件替代）
> 定位：综合 TODO，覆盖通用模块化重构 + 原等待项
> 详细规划：见 `SCX_规划_v4_通用模块化.md`

---

## 标记说明

| 标记 | 维度 | 说明 |
|------|------|------|
| [A] | Academic / 学术 | 论文、投稿、学术影响力 |
| [C] | Code / 代码 | 软件工程、实现、开源 |
| [B] | Business / 商业 | 商业模式、合作、收入 |
| [IP] | Intellectual Property / 知识产权 | 专利、权属、保护 |
| [LLM] | LLM / 大模型 | 大模型数据评价方向 |

**优先级**: P0=立即做, P1=1-2月内, P2=3-6月内, P3=6-12月

**时间标记**: ⚡=现在就能做, ⏳=需要等待前置条件

---

## Phase A: 核心重构 (2-4 周) 🔴 P0

> 目标：定义抽象接口，现有代码解耦，336 tests 通过

### A.1 抽象基类定义

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| A.1.1 | 定义 `SCXStateEncoder` 抽象基类（`featurize/distance/get_state/state_statistics`） | P0 | 无 | 1d | [C] | ⚡ |
| A.1.2 | 定义 `SCXExpert` 抽象基类（`predict/confidence/cost/metadata`） | P0 | 无 | 0.5d | [C] | ⚡ |
| A.1.3 | 定义 `SCXDataPoint` 抽象基类（`features/label/meta/state`） | P0 | 无 | 0.5d | [C] | ⚡ |
| A.1.4 | 类型标注 + 文档字符串 + 抽象方法检查 | P0 | A.1.1-3 | 1d | [C] | ⚡ |

### A.2 Encoder 提取

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| A.2.1 | 从 `experiments/mlip_case/` 提取 `MLIPEncoder`（ACE descriptor） | P0 | A.1.1 | 1d | [C] | ⚡ |
| A.2.2 | 从 `scx-health/` 提取 `VisionEncoder`（DINO/CLIP/ViT） | P0 | A.1.1 | 1d | [C] | ⚡ |
| A.2.3 | 从 `experiments/cifar/` 提取 `CIFAREncoder` | P0 | A.1.1 | 0.5d | [C] | ⚡ |
| A.2.4 | 每个 encoder 独立模块，可单独 import | P0 | A.2.1-3 | 0.5d | [C] | ⚡ |
| A.2.5 | 创建 `encoders/` 目录结构 | P0 | A.2.1-4 | 0.5d | [C] | ⚡ |

### A.3 核心模块解耦

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| A.3.1 | `scx/state/` 重构为使用 `SCXStateEncoder` 接口 | P0 | A.1.1 | 2d | [C] | ⚡ |
| A.3.2 | `scx/expert/` 重构为使用 `SCXExpert` 接口 | P0 | A.1.2 | 1d | [C] | ⚡ |
| A.3.3 | `scx/valuation/` 重构为使用统一 DataPoint 和 State 类型 | P0 | A.1.3 | 1d | [C] | ⚡ |
| A.3.4 | `scx/action/` 重构为使用抽象接口 | P0 | A.1.1-3 | 1d | [C] | ⚡ |
| A.3.5 | `scx/core/online.py` 使用抽象接口 | P0 | A.1.1-3 | 1d | [C] | ⚡ |
| A.3.6 | 删除重复代码，统一数据流 | P0 | A.3.1-5 | 1d | [C] | ⚡ |

### A.4 声明式配置原型

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| A.4.1 | 定义 YAML schema（encoder/expert/阈值/数据路径） | P0 | A.1.1-3 | 1d | [C] | ⚡ |
| A.4.2 | 实现 `ConfigLoader.from_yaml(path)` → `SCXConfig` | P0 | A.4.1 | 1d | [C] | ⚡ |
| A.4.3 | 创建 `domains/mlip.yaml` 示例配置 | P0 | A.4.1 | 0.5d | [C] | ⚡ |
| A.4.4 | 创建 `domains/health.yaml` 示例配置 | P0 | A.4.1 | 0.5d | [C] | ⚡ |
| A.4.5 | 创建 `domains/cifar.yaml` 示例配置 | P0 | A.4.1 | 0.5d | [C] | ⚡ |

### A.5 验证

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| A.5.1 | 全部 336 tests 通过，无回归 | **P0** | A.2-4 | 1d | [C] | ⚡ |
| A.5.2 | 每个领域 demo notebook 可运行 | P0 | A.2-4 | 1d | [C][A] | ⚡ |
| A.5.3 | 代码覆盖率不低于当前水平 | P0 | A.5.1 | 0.5d | [C] | ⚡ |

---

## Phase B: 声明式配置 (2-3 周) 🟡 P1

> 目标：YAML → SCXFramework 自动构建，CLI 接口

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| B.1 | YAML 配置解析器完善（嵌套定义、路径映射、验证） | P1 | A.4 | 3d | [C] | ⚡ |
| B.2 | `SCXFramework.from_config(config)` 工厂方法 | P1 | A.3, B.1 | 3d | [C] | ⚡ |
| B.3 | CLI 设计：`scx run/config-check/list-encoders/list-experts` | P1 | B.2 | 2d | [C] | ⚡ |
| B.4 | 审计报告自动生成（Markdown/PDF/HTML + 可视化） | P1 | B.2 | 3d | [C][B] | ⚡ |
| B.5 | Encoder 开发指南 + YAML 配置参考 + 端到端 demo | P1 | B.2-4 | 2d | [C][A] | ⚡ |

---

## Phase C: 新领域扩展 (4-8 周) 🟡 P1

> 目标：用新架构快速适配新领域，验证通用性

### C.1 SCX-Robot

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| C.1.1 | 调研 LeRobot 公开数据 / Open X-Embodiment 子集 | P1 | 无 | 2d | [A][C] | ⚡ |
| C.1.2 | 实现 `TrajectoryEncoder`（视觉+关节+力+成功信号融合） | P1 | A.1.1 | 5d | [C] | ⚡ |
| C.1.3 | 创建 `domains/robot.yaml` | P1 | B.1 | 0.5d | [C] | ⚡ |
| C.1.4 | 成功/失败状态分类实验 | P1 | C.1.2 | 3d | [A][C] | ⏳等 GPU |
| C.1.5 | 冗余轨迹压缩实验 | P1 | C.1.2 | 2d | [A][C] | ⏳等 GPU |
| C.1.6 | 失败状态挖掘实验 | P1 | C.1.2 | 2d | [A][C] | ⏳等 GPU |
| C.1.7 | 对比：full-data vs SCX-selected vs random 在 imitation policy 上表现 | P1 | C.1.4-6 | 3d | [A] | ⏳等 GPU |

### C.2 SCX-FEM

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| C.2.1 | 调研 PDEBench / 自生成弹性/热传导数据 | P1 | 无 | 2d | [A][C] | ⚡ |
| C.2.2 | 实现 `SimulationEncoder`（网格/几何/响应 embedding） | P1 | A.1.1 | 5d | [C] | ⚡ |
| C.2.3 | 创建 `domains/fem.yaml` | P1 | B.1 | 0.5d | [C] | ⚡ |
| C.2.4 | 多保真调度实验：粗网格 vs 细网格 | P1 | C.2.2 | 3d | [A][C] | ⚡ |
| C.2.5 | Surrogate 可靠性判断实验 | P1 | C.2.2 | 2d | [A][C] | ⚡ |
| C.2.6 | 对比：SCX 多保真调度 vs 全细网格 vs 全粗网格 | P1 | C.2.4-5 | 2d | [A] | ⏳等 GPU |

### C.3 SCX-LLM (minimal)

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| C.3.1 | 实现 `TextEncoder`（LLM embedding + 任务类型编码） | P1 | A.1.1 | 3d | [C] | ⚡ |
| C.3.2 | 创建 `domains/llm.yaml` (minimal) | P1 | B.1 | 0.5d | [C] | ⚡ |
| C.3.3 | 极小验证：区分有价值/冗余/噪声的 instruction 数据 | P2 | C.3.1 | 3d | [A][LLM] | ⏳等 GPU |
| C.3.4 | 定位文档：SCX-LLM 聚焦可验证任务（数学/代码/逻辑） | P2 | 无 | 2d | [LLM][A] | ⚡ |

---

## Phase D: 插件系统 (长期) 🟢 P2

> 目标：模块插件化，社区贡献指南，Benchmark 标准化

| # | TODO | 优先级 | 依赖 | 预估 | 维度 | 可执行性 |
|---|------|--------|------|------|------|---------|
| D.1 | 插件注册机制（`register()` 装饰器 + 自动发现 + 沙箱） | P2 | A.3 | 1w | [C] | ⚡ |
| D.2 | `SCXCompress` 插件化 | P2 | D.1 | 2d | [C] | ⚡ |
| D.3 | `OnlineSCXFramework` 插件化 | P2 | D.1 | 2d | [C] | ⚡ |
| D.4 | `StateConditionedInfluence` 插件化 | P2 | D.1 | 1d | [C] | ⚡ |
| D.5 | CONTRIBUTING.md + CLA + Issue/PR 模板 | P2 | D.1-4 | 1w | [C][B] | ⚡ |
| D.6 | SCX-Bench 标准化 API + 5-10 数据集 + Baseline 集成 | P2 | D.1 | 2w | [C][A] | ⏳等 GPU |

---

## 原等待项（保留，来自 Phase 1-3）

以下为之前 TODO 中的等待项，与本 TODO 并行推进。

### 等待 GPU (8月中旬，出差回来)

| # | TODO | 优先级 | 阻塞因素 | 维度 | 预计解锁 |
|---|------|--------|---------|------|---------|
| W.1 | CIFAR/MedMNIST GPU 重跑（ResNet-18 + 50 epochs） | P1 | 无 GPU | [A][C] | 8月中旬 |
| W.2 | SCX-Noise 论文 Figure (publication-quality) | P1 | W.1 | [A] | 8月中旬 |
| W.3 | 与 Data Shapley/LESS 对比实验（GPU加速后） | P1 | W.1 | [A][C] | 8月中旬 |
| W.4 | HAM10000/ISIC 实验 | P1 | W.1 | [A][C] | 8月中旬 |
| W.5 | SCX-Health 论文草稿 | P2 | W.4 | [A] | 8月中旬 |
| W.6 | SCX-Robot 实验 (C.1.4-7) | P1 | W.1 | [A][C] | 8月中旬 |
| W.7 | SCX-FEM GPU 实验 (C.2.6) | P1 | W.1 | [A] | 8月中旬 |
| W.8 | SCX-LLM 实验 (C.3.3) | P2 | W.1 | [LLM][A] | 8月中旬 |
| W.9 | SCX-Bench GPU baseline 集成 (D.6) | P2 | W.1 | [C][A] | 8月中旬 |

### 等待 DFT (2-4周，超算运行中)

| # | TODO | 优先级 | 阻塞因素 | 维度 | 预计解锁 |
|---|------|--------|---------|------|---------|
| W.10 | GaN_v1 DFT 结果 → 训练 GaN expert | P1 | 超算运行中 | [A][C] | 2-4周 |
| W.11 | AlN_v4 DFT 结果 → 重训 AlN expert | P1 | 超算运行中 | [A][C] | 2-4周 |
| W.12 | EGP Paper 1 完整实验 (M1-M6) | P1 | W.10-11 | [A] | 2-4周 |
| W.13 | SCX-MLIP 论文完成 | P1 | W.10-11 | [A] | 2-4周 |
| W.14 | SCX-Potential Compiler 实验 (2.11-2.18) | P2 | W.10-11 | [C][A] | 2-4周 |

### 论文与投稿

| # | TODO | 优先级 | 依赖 | 维度 | 可执行性 |
|---|------|--------|------|------|---------|
| W.15 | EGP Paper 1 Introduction + Methods 写作 | **P0** | 无 | [A] | ⚡ |
| W.16 | SCX-Theory arXiv 草稿 | **P0** | 无 | [A] | ⚡ |
| W.17 | 投稿 npj Computational Materials / Nature Communications | P1 | W.13 | [A] | ⏳ |
| W.18 | arXiv 占坑（SCX-Theory） | P1 | W.16 | [A] | ⚡ |
| W.19 | SCX-Sim 大论文 | P2 | W.17 | [A] | ⏳ |
| W.20 | SCX-Health 论文投稿 | P2 | W.5 | [A] | ⏳ |

### 商业

| # | TODO | 优先级 | 依赖 | 维度 | 可执行性 |
|---|------|--------|------|------|---------|
| W.21 | 调研华为健康合作入口 | P1 | 无 | [B] | ⚡ |
| W.22 | 调研国产 EDA/TCAD 公司技术合作 | P2 | 无 | [B] | ⚡ |
| W.23 | 找 1-2 个 paid pilot 甲方 | P2 | 有 demo 后 | [B] | ⏳ |
| W.24 | 设计三层商业产品线 | P2 | 无 | [B][C] | ⚡ |
| W.25 | 找校外 IP 律师评估 | P1 | 无 | [IP] | ⚡ |

### IP 与权属

| # | TODO | 优先级 | 依赖 | 维度 | 可执行性 |
|---|------|--------|------|------|---------|
| W.26 | 关键代码 Sha-256 存证 | P1 | 无 | [IP] | ⚡ |
| W.27 | 专利价值判断 | P1 | W.25 | [IP] | ⏳ |
| W.28 | CLA 模板 | P2 | 无 | [IP] | ⚡ |

---

## 时间线总览

```
现在 (6月)                   7月                        8月                        9月
─────                       ───                        ───                        ───

Phase A ───────────────────→ Phase B ─────────────────→ Phase C ────────────────→ Phase D
核心重构   2-4周             声明式配置  2-3周            新领域扩展  4-8周          插件系统
                                                                                 
  A.1 抽象基类                 B.1 YAML 完善                C.1 SCX-Robot           D.1 插件注册
  A.2 Encoder提取             B.2 Factory 方法             C.2 SCX-FEM              D.2-4 插件化
  A.3 核心解耦                B.3 CLI                     C.3 SCX-LLM (minimal)     D.5 社区指南
  A.4 配置原型                B.4 报告生成                                          D.6 Benchmark
  A.5 验证                    B.5 文档
                                                                                 
等待项 ──────────────────────────────────────────────────────────────────────────
                                                                                 
W.15 EGP Paper 1 写作 ──────→ W.16 SCX-Theory arXiv ────→ W.13 MLIP 论文完成 ────→ W.17 投稿
                              W.18 arXiv 占坑                                    
                              W.10-12 DFT 结果 ↔ W.14 Pot Compiler
                              W.1-9 GPU 实验 (8月中旬) ──→ W.4-5 Health 论文
                                                          W.6-8 Robot/FEM/LLM
```

---

## 依赖关系图

```
Phase A (核心重构)             Phase B (声明式配置)         Phase C (新领域)
─────────────────             ────────────────────        ─────────────────

A.1 抽象基类 ────→ A.2 Encoder提取
                      │
                      ├──→ A.3 核心解耦 ────→ A.5 验证
                      │                        │
                      └──→ A.4 配置原型 ────→ B.1 YAML完善 → B.2 Factory → B.3 CLI
                                                   │            │
                                                   └──→ B.4 报告生成
                                                        B.5 文档
                                                        │
                              C.1 Robot ────────────────┘
                              C.2 FEM  ─────────────────┘
                              C.3 LLM  ─────────────────┘

等待项:

W.15 EGP Paper 1 ───→ W.16 SCX-Theory arXiv ───→ W.18 arXiv 占坑
W.10 DFT结果   ───→ W.12 EGP实验     ───→ W.13 MLIP论文
W.1 GPU       ───→ W.2-9 全部GPU实验
```

---

## 核心风险提示

| 风险 | 严重程度 | 缓解措施 |
|------|---------|---------|
| 重构破坏现有 336 tests | 🔴 高 | 每步重构保持 test 覆盖，CI pipeline |
| 过度抽象导致灵活性下降 | 🟡 中 | 保留 `CustomEncoder` 逃生口 |
| 新领域 encoder 开发成本超预期 | 🟡 中 | 先用简单 embedding 做 MVP |
| 学校主张 SCX IP 权属 | 🔴 高 | Phase 0 证据隔离 + 校外律师评估 |
| GPU 到位后实验时间紧 | 🟡 中 | 提前准备好代码，GPU 一到就开跑 |
| 论文审稿人质疑"框架论文" | 🟡 中 | 论文重心在具体实验，不单独发框架论文 |
| VASP 任务占满超算 | 🟢 低 | 分批提交、监控负载 |

---

## 总结：现在立刻做的 5 件事

1. **定义抽象基类** (A.1.1-A.1.4) — 通用架构的根基
2. **提取现有 encoder** (A.2.1-A.2.5) — 解耦第一步
3. **重构核心模块** (A.3.1-A.3.6) — 让代码只依赖抽象接口
4. **创建 YAML 配置原型** (A.4.1-A.4.5) — 声明式配置的第一步
5. **保持 W.15/W.16 论文写作并行** — 架构重构不影响论文进度

> **一句话战略：先解耦再扩展。Phase A 完成后，新增领域的适配成本将从"2-3 周"降到"2-3 天"。**
