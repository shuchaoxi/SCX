---
tags: [TODO, 论文, 写作]
created: 2026-06-27
status: active
---

# 📝 论文推进 · 任务清单

---

## Paper 2：Consistency-Constrained Expert Merging for ACE（根据地论文）🔴

> **已采纳 V3 方案**（`egp/CodexKnowledge/实验重设计_综合方案_v3.md`）。
> 旧版 659 行 gauge-fixing-only → 归档；新版 785 行 merging framework → 当前。
> 故事：**独立训练的专家势函数能不能安全合并？能，但必须经过 gauge fixing + energy alignment + residual construction。**

**文件**：`paper/paper1_mlip/paper_v3.tex`（785 行，全部章节）
**目标期刊**：npj Computational Materials
**核心叙事**：四种不一致（energy reference, species shift, gauge ambiguity, residual meaning）→ 三步解决 → naive merge 惨败 → gauge-fixed merge 成功

### M1-M6 实验矩阵（V3 方案）

#### M1: Naive merge 产生物理错误 ⭐ 最关键的实验
| 项目 | 内容 |
|------|------|
| **命题** | P1a: 不 fix gauge/energy zero 的 naive merge 产生物理错误 |
| **对比** | Naive merge vs Gauge-fixed merge vs Full retrain baseline |
| **测试** | EOS (V0,B0), Elastic (Cij), 形成能, 声子 |
| **预期** | C33 偏差 >50%, 形成能符号可能错误 |
| **新增 DFT** | **0** |
| **致命风险** | 如果 naive merge 没崩 → P1a 不成立 → 转 "negative result" |
| **状态** | ⬜ 待 GPU/超算 |

#### M2: 域精度保留
| 项目 | 内容 |
|------|------|
| **命题** | P1b: Gauge-fixed merge 保持各 expert 域内精度 |
| **对比** | Merged vs Single ACE_AlN (on AlN) + vs Single ACE_GaN (on GaN) |
| **判据** | Force RMSE 增 <5%, Energy RMSE 增 <2 meV/atom |
| **新增 DFT** | **0** |
| **状态** | ⬜ 待 GPU/超算 |

#### M3: Species shift 对齐必要性
| 项目 | 内容 |
|------|------|
| **命题** | P1c: Species shift 歧义导致形成能偏差 |
| **对比** | Shift-aligned vs unaligned merge → 形成能 |
| **预期** | 未对齐 >0.5 eV; 对齐后 <0.05 eV |
| **新增 DFT** | ~50 帧 AlGaN mixed |
| **状态** | ⬜ 需 DFT |

#### M4: Residual expert 防遗忘
| 项目 | 内容 |
|------|------|
| **命题** | P1d: Residual construction 增量添加不遗忘 |
| **对比** | Residual sequential (AlN→GaN→AlGaN) vs Full joint retrain |
| **判据** | <20% 数据量达到 Full retrain >85% 精度 |
| **新增 DFT** | ~150 帧 AlGaN mixed |
| **状态** | ⬜ 需 DFT |

#### M5: 跨域优势
| 项目 | 内容 |
|------|------|
| **命题** | P1e: Merged model 在跨域优于单域 expert |
| **对比** | Merged vs SA_AlN vs SA_GaN on 5 properties |
| **新增 DFT** | ~100 帧 surface/defect |
| **状态** | ⬜ 需 DFT |

#### M6: 统计可重复性
| 项目 | 内容 |
|------|------|
| **命题** | 5 seeds × mean±std, p-value, Cohen's d |
| **新增 DFT** | **0** |
| **状态** | ⬜ |

### 新增 DFT 汇总
| 实验 | 新增 DFT | 用途 |
|------|---------|------|
| M1+M2 | 0 | 已有数据 |
| M3 | ~50 | AlGaN formation energies |
| M4 | ~150 | AlGaN mixed training |
| M5 | ~100 | Surface/defect reference |
| **总计** | **~300** | 对比原计划 9000+ 帧减少 97% |

### 投稿准备
- [ ] M1+M2 GPU 实测（最高优先，零新增 DFT）
- [ ] Overleaf 编译 paper_v3.tex
- [ ] Cover Letter
- [ ] arXiv → npj Comput. Mater.

### P2.1 止损收窄 ✅ 已完成

- [x] **P2.1.1** SCX Figs (Fig 5-8) 不在正文中引用 ✅
- [x] **P2.1.2** 零 SCX 理论提及 ✅
- [x] **P2.1.3** Claims 已收窄 ✅

### P2.2 写作完成 ✅ 已完成

- [x] **P2.2.1** Results: EOS + Elastic + Phonon + Gauge Violation + Fair Comparison ✅
- [x] **P2.2.2** Discussion + Conclusion ✅
- [x] **P2.2.3** EGP-V2 修订已整合 ✅

### P2.3 图表整理 ✅

- [x] Fig 1-4 已就绪（EOS、弹性、分批误差、gauge tradeoff）
- [x] supplementary CSV 就绪

### P2.4 投稿准备 🔴 当前焦点

- [ ] **P2.4.1** 在 Overleaf 打开 `paper.tex`，编译验证
- [ ] **P2.4.2** 准备 Cover Letter（可协助起草）
- [ ] **P2.4.3** arXiv 上传
- [ ] **P2.4.4** 投稿 npj Computational Materials

---

## Paper 1：Data Quality > Model Architecture（Nature 旗舰）🟡

> ⚠️ **标题策略**：Nature 卖的是发现，不是方法名。标题用 "Training Data Quality Dominates Model Architecture in Scientific Machine Learning"，不用 "State-Conditioned eXpertise"。SCX 在 Methods 里解释，在 Discussion 里命名。品牌在论文里建立，不在标题里。

**文件**：`paper/paper1_nature/theory_methods.tex`（156 行，~2000 words，Nature 风格）
**目标期刊**：Nature Computational Science（首选）/ Nature Machine Intelligence
**核心发现**：数据清洗 → 29-48% 提升 vs 架构改进 → 2.5%。12-19 倍差距。

### 理论部分 ✅ 已起草
- [x] 两层状态发现 + 多专家一致性 + 弱特征检测 ✅
- [x] Thm 1+2+3 Nature 风格陈述（无 Lemma/Proof） ✅
- [x] 实践实现指南 + 计算成本 ✅

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

*关联文件：[[论文规划_终版|论文规划 · 终版]]*
