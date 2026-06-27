---
tags: [TODO, 论文, 写作]
created: 2026-06-27
status: active
---

# 📝 论文推进 · 任务清单

---

## Paper 2：EGP Gauge Fixing（根据地论文）🔴 最高优先级 — 当前焦点

**当前状态**：`paper/paper1_mlip/paper.tex` 已完成 Abstract + Introduction + Methods。Fig 1-8 就绪。**定理 1+2 已完成**，不再占用 Paper 2 精力，可全速推进。

**目标期刊**：npj Computational Materials

**时间估计**：1-2 周可投稿

> ⚠️ **当前立即工作**：P2.1 止损收窄 + P2.2 Results 写作。Paper 1 理论已独立完成，不干扰 Paper 2。

### P2.1 止损收窄（阶段 0，来自 SCX_TODO_论文框架.md）

- [ ] **P2.1.1** 移除 SCX 噪声检测 Figs (Fig 4-8)
  - 这些图属于 Paper 1
  - 保留：EOS 对比 (Fig 1)、弹性常数 (Fig 2)、Per-batch 误差 (Fig 3)、Gauge violation (Fig 4)
  - 参考：`paper/paper1_mlip/FIGURES_ANALYSIS.md`

- [ ] **P2.1.2** 移除所有 SCX 理论提及
  - 正文中不讨论"状态条件专家可靠性"
  - Discussion 末尾最多一句话埋种子

- [ ] **P2.1.3** 收窄 claims
  - ✅ claim: gauge-fixed shared+correction ACE 参数化
  - ❌ 不 claim: 新的 MoE runtime、element correction 原子能、AlGaN 可转移
  - 保留 fair comparison 结果（改善来自参数量而非架构本身）

### P2.2 写作完成

- [ ] **P2.2.1** 写完 Results section
  - 3.1 EOS ($V_0$, $B_0$ vs DFT ref 10.64/192.6)
  - 3.2 Elastic Constants ($C_{11}$-$C_{66}$ 对比表)
  - 3.3 Phonon Forces (力 RMSE 0.00793→0.00580, -27%)
  - 3.4 Gauge Violation (8.77→4.6×10⁻¹⁶)
  - 3.5 Fair Parameter-Matched Comparison ⭐

- [ ] **P2.2.2** 写完 Discussion + Conclusion
  - gauge fixing 对势函数合并的奠基作用
  - 不泛化到通用框架

- [ ] **P2.2.3** 整合 EGP-V2 agent 讨论的 4 个修订
  - 修订 1：Model B 不是新的运行时势函数架构
  - 修订 2：gauge fixing 必须提升到 coefficient-level
  - 修订 3：第一代实现需要自定义线性拟合
  - 修订 4：论文叙事必须收窄
  - 来源：`CodexKnowledge/SCX_发展史与成就.md`

### P2.3 图表整理

- [ ] **P2.3.1** 生成最终版 Fig 1-4（保留的 EGP 图）
- [ ] **P2.3.2** 补充 fair comparison 对比表
- [ ] **P2.3.3** 准备 SI 数据和表格

### P2.4 投稿

- [ ] **P2.4.1** 选择目标期刊（npj Comput. Mater. 首选）
- [ ] **P2.4.2** 准备 Cover Letter
- [ ] **P2.4.3** 准备 SI
- [ ] **P2.4.4** arXiv 上传
- [ ] **P2.4.5** 正式投稿

---

## Paper 1：Nature Computational Science 旗舰论文 🟡 并行准备

**当前状态**：仅有规划，无草稿。**理论部分已就绪**（定理 1+2 完整证明 + Dawid-Skene 对比分析于 2026-06-27 完成），现在可以开始写论文正文的理论 Section。实验等 GPU。

> ✅ **定理 1+2 可用**：`../../../theory/theorems/01_noise_detection_guarantee.md` 和 `02_weak_feature_failure.md`
> ✅ **方案 D 决策**：Paper 1 正文 2-3 页轻量版，Paper 3 (JMLR) 深度版
> ✅ **V(s) 循环定义**已标记待移除（Paper 3 修复）

### P1.1 理论部分 ✅ 证明已完成，可开始写作

- [x] **P1.1.1** 写定理 1（充分条件）的形式化陈述和证明 ✅ 2026-06-27
  - 产出：`../../../theory/theorems/01_noise_detection_guarantee.md`
  - 论文目标：2 页正文 + 附录证明（方案 D 轻量版）

- [x] **P1.1.2** 写定理 2（失败下界）的形式化陈述和证明 ✅ 2026-06-27
  - 产出：`../../../theory/theorems/02_weak_feature_failure.md`
  - 论文目标：1 页正文 + 附录证明（方案 D 轻量版）

- [x] **P1.1.3** 写与 Dawid-Skene 的对比分析 ✅ 2026-06-27
  - 包含在定理 1 证明中
  - 论文目标：0.5 页

- [ ] **P1.1.4** 将定理 1+2 写为论文正文（即可开始，不等 GPU）

### P1.2 已有实验整理（现在可做）

- [ ] **P1.2.1** 整理 AlN v3 两层分析结果 → 论文 Figures
  - 来源：`experiments/mlip_case/SCX_AlN_v3_两层分析报告.md`
  - 生成：fmax vs test error scatter (r=0.966)、噪声分布、一层 vs 两层 F1

- [ ] **P1.2.2** 整理 CIFAR 噪声检测结果 → 论文 Figures
  - 来源：`experiments/cifar/results/experiment_report_2026-06-26.md`
  - 注意：标注"3 epoch CPU training"作为限制

- [ ] **P1.2.3** 整理 MedMNIST 压缩结果 → 论文 Figures
  - 来源：`scx-health/results/experiment_report_v2.md`

### P1.3 Introduction + Methods 草稿（现在可写）

- [ ] **P1.3.1** 写 Introduction
  - 锚定："ML 社区默认模型架构 > 数据质量，我们挑战这个假设"
  - 引用 AlN v3 的 9.7× per-batch RMSE 差异作为 motivating example

- [ ] **P1.3.2** 写 Methods
  - Two-Layer State Discovery + Multi-Expert Consistency
  - 轻量理论（定理 1+2）

### P1.4 等 GPU 后完成的实验

- [ ] **P1.4.1** AlN v3 去噪重训（最高优先级）
- [ ] **P1.4.2** CIFAR-10/100 完整训练 (50 epoch + ResNet-18)
- [ ] **P1.4.3** MedMNIST 强 backbone (ResNet-18/EfficientNet)
- [ ] **P1.4.4** UCI tabular benchmarks
- [ ] **P1.4.5** 跨材料 MLIP 验证 (Si, Cu, MgO)
- [ ] **P1.4.6** 所有领域的架构对比基线

### P1.5 写作完成（实验后）

- [ ] **P1.5.1** 写 Results (§4 Cross-Domain Validation)
- [ ] **P1.5.2** 写 §5 Why Architecture Didn't Help
- [ ] **P1.5.3** 写 Discussion
- [ ] **P1.5.4** 投稿 Nature Computational Science

---

## Paper 3：压缩保真定理 🟢 低优先级

**当前状态**：命题 4 已有完整证明，需要修复循环定义。

- [ ] **P3.1** 修复 $D(s)$ 的循环定义（依赖 T2.3）
- [ ] **P3.2** 紧化 bound
- [ ] **P3.3** 灵敏度代理的 gap 分析
- [ ] **P3.4** 合成实验验证 bound
- [ ] **P3.5** 写论文 → 投稿 JMLR/TMLR

---

## Paper 4：跨领域深挖 🔵 远期

- [ ] **P4.1** 等 Paper 1 和 3 完成后评估领域选择
- [ ] **P4.2** 建立合作方/数据
- [ ] **P4.3** 深度实验
- [ ] **P4.4** 投稿

---

*关联文件：[[../05_决策/论文规划_终版|论文规划 · 终版]]*
