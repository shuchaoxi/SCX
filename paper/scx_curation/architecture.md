# Devirus-Distill: Sprint Gatekeeper Architecture

> **论文**: "The Curation-Exploration Tradeoff: Don't Clean Your Data — Teach a Gatekeeper to Evolve, and Never Delete What You Don't Yet Understand"
> **硬件**: 单机 1× RTX 4090 (24GB)，零外存依赖
> **核心卖点**: 任何课题组可复现

---

## 架构总图

```
╔══════════════════════════════════════════════════════════════╗
║                    单机 RTX 4090                              ║
║                                                              ║
║  数据摄入 (流式，不存原始数据)                                  ║
║  ├── MP API / OQMD API → 边下边提特征 → 原始数据删除           ║
║  └── Teacher 模型推理 → 边算边存共识标签                       ║
║                                                              ║
║  特征矩阵 (永久缓存, ~100 MB)                                  ║
║  ├── SOAP / ACSF descriptors                                 ║
║  └── 10万结构 × 1 KB = ~100 MB                               ║
║                                                              ║
║  Sprint 评分引擎                                              ║
║  ├── S(s) = quality_score(s) + η(t) × novelty_bonus(s)      ║
║  ├── 遍历 100 MB 特征矩阵 → 毫秒级                             ║
║  ├── S > τ_keep   → 从 API 召回原始结构 → GPU 训练            ║
║  └── S ≤ τ_keep   → 只记 API 路径，不召回                     ║
║                                                              ║
║  NEP Student 训练                                             ║
║  ├── 混合训练集: Sprint 精选 DFT + Teacher 蒸馏共识            ║
║  └── ~10K 参数                                               ║
║                                                              ║
║  路径索引 (SQLite, ~几 MB)                                    ║
║  ├── 每个结构: score, timestamp, API source, material_id      ║
║  └── 模型更新 → 重评分 → 从 API 按需召回                        ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 数据流

```
初始化 (一次性):

  MP API 流式下载 → 边下边提特征 → 原始数据删除
      ↓
  特征矩阵 ~100 MB (永久缓存)
  Teacher 模型推理 → 共识标签
      ↓
  NEP baseline 训练 (50% 化学空间)

────────────────────────────────────────────

运行时循环:

  Sprint 遍历 100 MB 特征矩阵 → 评分 (毫秒级)
      ↓
  S > τ_keep → MP API 召回单个结构 → 训练
      ↓
  模型更新 → Sprint 重跑特征矩阵 → 评分进化
      ↓
  之前搁置的结构 → 评分跨过 τ_keep → API 召回 → 复活
```

### 为什么不需要存原始数据

| 阶段 | 操作 | 存储 |
|------|------|:---:|
| 下载 | MP API 流式 | 0 |
| 特征提取 | 边下边算 | 100 MB |
| 原始数据 | 提取完即删 | 0 |
| 需要时 | API 按 material_id 召回单个结构 | 用完即删 |

---

## 核心创新点

| 概念 | 说明 |
|------|------|
| **Sprint Gatekeeper** | 实时评分，只有模型知道标准 |
| **Curation-Exploration Tradeoff** | η(t) 衰减，初期探索后期收敛 |
| **Data Quarantine** | 不删除，记 API 路径，搁置待复活 |
| **Stream-Then-Forget** | 流式下载+特征提取，不存原始数据 |
| **Resurrection** | 模型进化 → 重评分 → API 召回 → 复活 |
| **教师蒸馏** | 8个MLIP teacher → 共识标签 → NEP student |

---

## 为什么单机 4090 够用

| 资源 | 用量 |
|------|------|
| 特征矩阵 | ~100 MB (常驻内存) |
| 路径索引 | ~几 MB (SQLite) |
| Teacher 模型 | ~8 GB (GPU 显存) |
| NEP 训练 | ~2 GB (GPU 显存) |
| 训练集 | ~50 GB (磁盘，按需加载) |
| 原始 DFT 数据 | **0 (不存)** |

---

## 论文结构 (Nature 格式)

```
Main (4 pages):
  Fig 1: Sprint-Distill 架构总图 (单机 4090)
  Fig 2: Curation-Exploration Tradeoff (η 衰减)
  Fig 3: 在线学习曲线 (static vs online Sprint)
  Fig 4: 搁置复活实验 (复活率 vs 精度提升)
  Fig 5: NEP student vs teacher comparison
  Fig 6: Extensions — Drug Discovery, Semiconductor, Embodied

SI (~40 pages):
  完整 Methods + Ablation + 额外实验

一句话卖点:
  "Single RTX 4090. Zero external storage. Fully reproducible."
```

---

*Architecture v3.0 — Single Machine, Zero Bloat*
