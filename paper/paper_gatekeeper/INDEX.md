# Paper: The Curation-Exploration Tradeoff

> **完整标题**: Don't Clean Your Data — Teach a Gatekeeper to Evolve, and Never Delete What You Don't Yet Understand
> **目标期刊**: Nature / Nature Computational Science
> **硬件**: 单机 1× RTX 4090 (24GB)，零外存依赖
> **状态**: 📋 规划中

---

## 一句话

传统的"清洗数据"范式错了。应该训练一个 Gatekeeper 来动态评分数据——模型进化时标准自动进化，暂不需要的数据不删除只搁置，等模型成长后复活。

## 与 SCX 理论的关系

| Gatekeeper 概念 | SCX 理论支撑 |
|----------------|-------------|
| Sprint 质量评分 | **Theorem 1**: 多专家一致性噪声检测保证 (F1 ≥ 1 - exp(-2MΔ²)/η) |
| Curation-Exploration η(t) 衰减 | **Theorem 2**: 弱特征失效下界 (F1 ≤ baseline + √(2δ)) |
| "不删除, 只搁置"哲学 | **Theorem 3**: 噪声与困难不可区分定理 |
| Teacher 分歧分析 | `src/scx/expert/` ExpertConflict, ExpertReliability |
| 在线复活机制 | State-conditioned re-valuation (SCX 核心框架) |
| 原因标签 (QUALITY_MAGMOM, REDUNDANT_DENSITY...) | StateDiscovery + StateAssignment |

## 核心创新

1. **Sprint Gatekeeper**: 实时评分引擎，遍历 ~100 MB 特征矩阵，毫秒级决策
2. **Curation-Exploration Tradeoff**: η(t) 衰减函数，初期探索后期收敛
3. **Data Quarantine**: 低分数据不删除，记 API 路径，模型进化后重评分复活
4. **Stream-Then-Forget**: 流式下载+特征提取，不存原始 DFT 数据
5. **Teacher Distillation**: 8 个 MLIP teacher → 共识标签 → NEP student (~10K 参数)
6. **单机可复现**: RTX 4090 + 零外存依赖

## 实验设计

### 消融 (核心, 一周)
- NEP_sprint (2万, Sprint 精选)
- NEP_random (2万, 随机采样)
- NEP_nosprint (3万, 去重不评分)
- 对比文献: MACE 18 / CHGNet 22 / SevenNet 20 meV/atom

### 关键假设
> 若 sprint < random 且接近 MACE → 赢

## 目录文件

| 文件 | 内容 |
|------|------|
| `README.md` | 论文 TODO / Sprint 计划 (P0-P6) |
| `architecture.md` | 系统架构设计 (数据流、组件、创新点) |
| `experiment_plan.md` | Devirus-Distill 实验计划 (Phase 0-6, 里程碑) |
| `figure6_concept.md` | Figure 6 延伸方向设计 (药物/半导体/具身智能) |

## 相关模块

- `drug-module/` — SCX 药物发现计算管线 (DTI, 分子特征, 靶点筛选)
- `drug-module/docs/药物靶点全景图_SCX计算筛选TOP10.md` — TOP 10 计算筛选靶点

---

*Gatekeeper Paper — SCX 应用验证线*
