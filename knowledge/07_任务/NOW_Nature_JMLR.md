---
tags: [TODO, 论文, Nature, JMLR]
created: 2026-06-27
---

# Nature + JMLR 双线推进 · TODO

> Paper 2 (npj) 根据地 → Paper 1 (Nature) 旗舰 → Paper 3 (JMLR) 理论深挖
> 
> **框架设计**: Paper 1 → `paper/paper1_nature/PAPER_FRAMEWORK.md` | Paper 3 → `paper/paper3_jmlr/PAPER_FRAMEWORK.md`

---

## 投稿顺序

```
Paper 2 (npj)           Paper 1 (Nature)               Paper 3 (JMLR)
Gauge Fixing            Data Quality > Architecture     Noise Detection Theory
    ↓                        ↓                              ↓
  先发                    GPU到后补齐实验                  Paper1 arXiv后投
  1-2周可投               预计8周                          +6月
```

**关键约束**: Paper 3 必须在 Paper 1 arXiv 之后投稿（建立学术优先权）。Paper 1 必须在 GPU 到位后跑完 P0 实验。

---

## Paper 1 (Nature) — GPU 前可做

### 写作（无阻塞）

- [ ] **P1.W1** Introduction 草稿（800 words）
  - "We found data quality matters 12-19× more than architecture"
  - 锚定故事：AlN v3, r=0.966

- [ ] **P1.W2** Methods 精简（从 theory_methods.tex 压缩到 1500 words）
  - 已有草稿 156 行，需要向 Nature 风格靠拢

- [ ] **P1.W3** Discussion + Conclusion 草稿（500 words）

- [ ] **P1.W4** Supplementary Information (S1-S5)
  - S1-S3: 定理完整证明（已就绪）
  - S4: 实验细节
  - S5: 补充图表

### 非 GPU 实验（CPU 可做）

- [ ] **P1.E1** UCI tabular benchmarks
  - 3-5 个数据集（Adult, Wine, Breast Cancer, Diabetes, Bank）
  - SCX-Noise vs Loss-based vs Confidence-based
  - 产出：Table 1 的 Tabular 行

- [ ] **P1.E2** 公开 MLIP 数据下载 + SCX 分析
  - Si, Cu, MgO (ColabFit/OpenKIM)
  - 跨材料噪声分布分析

### Figures（部分可做）

- [ ] **P1.F1** fmax vs test error scatter (r=0.966) — 数据已有 ✅
- [ ] **P1.F3** Two-layer state discovery t-SNE — 数据已有 ✅
- [ ] **P1.F2** SCX cleaning vs Model B bar chart — ⏳ 等 GPU
- [ ] **P1.F4** 4-panel cross-domain comparison — ⏳ 等 GPU

---

## Paper 1 (Nature) — GPU 后必做 🔴

| # | 实验 | GPU 时 | 优先级 |
|---|------|--------|:----:|
| **G1** | AlN v3 去噪重训（方案 A: fmax>5 移除 74 帧） | 4-8h | 🔴 P0 |
| **G2** | CIFAR-10 完整训练（ResNet-18, 50 epoch, M=20 experts） | ~16h | 🔴 P0 |
| **G3** | MedMNIST 强 backbone（ResNet-18, δ 测量） | ~8h | 🟡 P1 |
| **G4** | 架构对比基线（所有领域 fair comparison） | ~12h | 🟡 P1 |

**P0 总计**: ~20-24 GPU-hours。**G1 最高优先**——把 29-48% 从预估变实测。

---

## Paper 3 (JMLR) — 全部现在可做 🔓

> 纯理论论文，零 GPU 依赖。30-40 页。Paper 1 arXiv 后投稿。

### 定理升级（核心新贡献）

- [ ] **P3.T1** Thm 1 放松版：Hoeffding → Bernstein 界（2-10× 更紧）
- [ ] **P3.T2** Thm 1 放松版：A1 不相交训练集 → 依赖专家浓度不等式
- [ ] **P3.T3** Thm 2 升级：Pinsker → Le Cam + Assouad minimax 下界
- [ ] **P3.T4** Rate optimality 证明：√δ 是最优速率
- [ ] **P3.T5** 自适应 bound：不依赖 A5（用 empirical Bernstein）
- [ ] **P3.T6** PAC-Bayes 泛化 bound for noise detector
- [ ] **P3.T7** Dawid-Skene 正式比较定理

### 写作（全部可启动）

- [ ] **P3.W1** Introduction + Problem Formulation（~7pp）
- [ ] **P3.W2** Main Results (3.1-3.4, ~14pp) — 主体
- [ ] **P3.W3** Connections to Existing Theory（~7pp）：Dawid-Skene, PAC-Bayes, Coreset, IB
- [ ] **P3.W4** Simulations + Case Studies（~6pp）
- [ ] **P3.W5** Discussion + Appendices（~13pp）

### 时间线

| 阶段 | 内容 | 时间 |
|------|------|------|
| Phase 1 | P3.T1-T7 证明 + P3.W1-W2 写作 | 4 周 |
| Phase 2 | P3.W3-W5 写作完成 | 4 周 |
| Phase 3 | 内部审查 + 修改 | 2 周 |
| **投稿** | Paper 1 arXiv 后 → submit | +6 月 |

---

## 可立即推进（本周）

```
🔴 Paper 2: M1+M2 实测（如果有 GPU/超算可用）
🟡 Paper 1: P1.W1 Intro + P1.W3 Discussion + P1.E1 UCI tabular
🟢 Paper 3: P3.T1 证明（Bernstein 升级是最直接的）
```

---

*关联：[[NOW_论文]] · [[论文规划|论文规划]]*
