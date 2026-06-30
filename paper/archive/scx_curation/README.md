# The Curation-Exploration Tradeoff
# Don't Clean Your Data — Teach a Gatekeeper to Evolve,
# and Never Delete What You Don't Yet Understand

> **目标期刊**: Nature / Nature Computational Science  
> **硬件**: 单机 1× RTX 4090 (24GB)，零外存依赖  
> **时间线**: 6-12 个月  
> **最后更新**: 2026-06-28

---

## 🔴 P0 — 阻塞项

- [ ] pip install mace-torch chgnet sevenn calorine deepmd-kit nequip
- [ ] 下载 8 个 Materials teacher 模型权重 (~8 GB)
- [ ] MP API 流式下载 + 边下边提特征 → 原始删除
- [ ] **特征矩阵 ~100 MB 永久缓存到本地**
- [ ] 实现 Sprint 评分核心代码 (含原因标签)
- [ ] 实现路径索引 (SQLite: score, reason_tag, material_id, timestamp)

## 🟡 P1 — Teacher 蒸馏 + NEP Baseline

- [ ] 8 个 teacher 加载 + 验证推理
- [ ] 生成结构集 (50 元素 × 200 环境 = 10K)
- [ ] Teacher pairwise disagreement 分析
- [ ] 三层对齐 (参考态→仿射→贝叶斯)
- [ ] 共识标签数据集
- [ ] **格式转换层**: VASP/teacher output → NEP train.in 格式
- [ ] NEP_sprint baseline 训练 (50% 化学空间, ~2万结构)
- [ ] 与文献对比: MACE 18, CHGNet 22, SevenNet 20 meV

## 🟡 P2 — Sprint 在线成长

- [ ] 剩余 50% 化学空间逐步喂入
- [ ] Sprint 评分 → 原因标签 (QUALITY_MAGMOM, REDUNDANT_DENSITY...)
- [ ] **在线学习曲线**: static vs online Sprint
- [ ] Curation-exploration η(t) 衰减曲线

## 🟡 P3 — 搁置复活

- [ ] 低分结构 → 记 API 路径，不召回
- [ ] 模型更新 → 重评分 → 复活率测量
- [ ] 复活数据对精度的贡献 (ΔMAE)

## 🟢 P4 — 消融 (不烧全量，一周跑完)

- [ ] NEP_sprint (精选 2万) — 2天
- [ ] NEP_random (随机等量 2万) — 2天
- [ ] NEP_nosprint (去重不评分 3万) — 3天
- [ ] **对比**: sprint < random → Sprint 有效
- [ ] 对比文献: MACE 18 / CHGNet 22 / SevenNet 20 meV

## 🟢 P5 — 分析

- [ ] 丢弃原因分布统计 (REDUNDANT_DENSITY: 40%, QUALITY_SCF: 15%...)
- [ ] 幂律冗余 KS 检验
- [ ] Teacher 覆盖盲区分析

## 🔵 P6 — 论文

- [ ] 6 张 Figure (含 Fig 6 三方向延伸图)
- [ ] Abstract + Introduction + Results + Methods + Discussion
- [ ] SI (~40页)
- [ ] 投稿 Nature

---

## 📊 消融实验设计 (核心)

```
不训全量 benchmark — 用已发表的 teacher 数据作为 baseline:

  MACE-MP-0 论文: MAE = 18 meV/atom  ✅ 已发表
  CHGNet 论文:   MAE = 22 meV/atom  ✅ 已发表
  SevenNet 论文: MAE = 20 meV/atom  ✅ 已发表

Mini ablation (一周):

  NEP_sprint    (2万, Sprint精选) → MAE = ?
  NEP_random    (2万, 随机采样)   → MAE = ?
  NEP_nosprint  (3万, 去重不评分) → MAE = ?

  若 sprint < random 且接近 MACE → 赢
```

## 📋 Sprint 原因标签

| 标签 | 原因 | 触发条件 |
|------|------|----------|
| QUALITY_MAGMOM | 磁矩不合理 | 原子磁矩 = 0 |
| QUALITY_SCF | SCF 不收敛 | convergence = False |
| QUALITY_EFORM | 形成能异常 | abs(E_form) > 5 eV/atom |
| REDUNDANT_DENSITY | 化学空间饱和 | 同类样本 > 阈值 |
| REDUNDANT_TEMP | 温度区间饱和 | 该温度 bin 已满 |
| OUTLIER_UNEXPLAINED | 统计异常 | 3σ 外，原因不明 |
| NOVELTY_LOW | 结构已覆盖 | Tanimoto > 0.95 |

---

*SCX Devirus-Distill Project — v4.0*
