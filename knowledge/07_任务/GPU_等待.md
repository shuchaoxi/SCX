---
tags: [TODO, GPU, 阻塞]
created: 2026-06-27
status: blocked
blocked_by: 等显卡
---

# ⏳ GPU 阻塞任务

> **当前状态**：torch CPU-only。所有需要 GPU 训练的实验被阻塞。
> **预期解除**：显卡到货后。

---

## G1: AlN v3 去噪重训 🔴 最高优先级 🔴

**为什么重要**：Paper 1 的核心发现依赖此实验。29-48% 是预估——必须用实测替换。

**计算量估计**：4-8 小时 GPU 时间

- [ ] **G1.1** 准备去噪数据集（3 个方案）
  - 方案 A（推荐先做）：移除 fmax > 5 eV/Å 的 74 帧
  - 方案 B：移除 SCX 两层 Top-2 噪声状态（约 90-131 帧）
  - 方案 C：移除 fmax > 10 的 14 帧 + 降权 fmax 5-10 的 60 帧

- [ ] **G1.2** 训练对照组
  - (a) Clean baseline: 去噪后训练 Single ACE
  - (b) Original baseline: 全部 534 帧（已有）
  - (c) Random drop: 随机去除 74 帧
  - (d) Loss-based drop: 去除训练 loss 最高的 74 帧

- [ ] **G1.3** 评测
  - 同一个 103 帧测试集
  - 报告力 RMSE、能量 RMSE
  - 实测 (a) vs (b) 的改善幅度

- [ ] **G1.4** 更新 FIGURES_ANALYSIS.md Fig 7
  - 用实测值替换"SCX-ACE（预估）"柱

- [ ] **G1.5** 根据实测结果确定 Paper 1 claim 级别
  - 力 RMSE 降 > 15%：claim "数据清洗显著提升模型性能"
  - 力 RMSE 降 5-15%：claim "SCX 识别影响性能的数据质量问题"
  - 力 RMSE 降 < 5%：需要重新审视叙事

---

## G2: CIFAR-10/100 完整训练 🔴

**为什么重要**：Paper 1 的跨领域证据支柱 2（Vision）。

**当前状态**：3 epoch SimpleCNN CPU → SCX-Compress 退化，SCX-Noise 有信号但不稳定。

- [ ] **G2.1** CIFAR-10 完整训练
  - ResNet-18, 50 epoch, batch_size=128
  - 5 个独立 seed 的专家
  - 噪声检测实验（10%, 20% label noise）
  - 压缩实验（20%, 30%, 50%）

- [ ] **G2.2** CIFAR-100 完整训练
  - 同上设置

- [ ] **G2.3** 产出完整实验报告

---

## G3: MedMNIST 强 Backbone 🟡

**为什么重要**：Paper 1 的跨领域证据支柱 3（Medical）。

**当前状态**：SimpleCNN 在 DermaMNIST 上弱特征失效。

- [ ] **G3.1** PathMNIST + DermaMNIST + BloodMNIST
  - ResNet-18 或 EfficientNet-B0 backbone
  - 压缩 + 噪声 + 路由三组实验
  - 验证弱特征失效是否因 backbone 太弱

- [ ] **G3.2** 产出 v3 实验报告

---

## G4: 架构对比基线 🟡

**为什么重要**：需要证明"数据质量 > 架构改进"不是特例。

- [ ] **G4.1** 对每个领域设计 fair comparison
  - MLIP: Model B (shared+correction) vs 数据清洗
  - Vision: ResNet-18 vs ResNet-50 vs 数据清洗
  - Medical: SimpleCNN vs ResNet-18 vs 数据清洗

- [ ] **G4.2** 统一评估协议

---

## G5: 跨材料 MLIP 重训（可选）🟢

- [ ] **G5.1** 如果 E2 中在 Si/Cu/MgO 上发现噪声，做去噪重训
- [ ] **G5.2** 验证跨材料的"数据质量 > 架构改进"一致性

---

## 解除阻塞后的执行顺序

```
Day 1-2:  G1 (AlN v3 去噪重训，4-8h 计算) ← 最高优先
Day 3-5:  G2 (CIFAR 完整训练)
Day 6-8:  G3 (MedMNIST 强 backbone)
Day 9+:   G4 (架构对比) + G5 (跨材料)
```

---

*关联：[[NOW_实验]], [[论文规划_终版|论文规划 · 终版]] §3.4*
