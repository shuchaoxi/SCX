# SCX 开发 TODO

> 最后更新：2026-06-26 | 基于 6 Agent 讨论的综合方案

---

## Phase 1：理论加固（1-2 月）

### 1.1 SCX-Compress 定理 🔴 P0

- [x] **Theorem 1** ✅ — `theory/propositions/04_compression_fidelity.md` (689行)
  - 压缩保真上界: 偏差项 + Rademacher 方差项
  - 核心结论: 50% 压缩且精度损失 <5% 需要 D(s) ≥ 0.90
- [ ] 合成验证: 在 2D 合成数据上数值验证 bound 的 tightness
- [ ] **写入 Paper 4 §4.3**

### 1.2 Expert Governance Protocol 形式化 🔴 P0

- [x] **5 步协议** ✅ — `theory/propositions/05_expert_governance_protocol.md`
  - Gauge Check → Domain Certificate → Conflict Resolution → Anchor Verification → Distillation Authorization
- [x] **Certification Theorem** ✅ — R_student(s) ≤ R_min(s) + ε(N_anchor, δ)
- [ ] 在 AlN v3 数据上 retrospective 验证
- [ ] **写入 Paper 3 §3**

### 1.3 State Discovery 鲁棒性 🟡 P1

- [x] **Mis-specification 分析** ✅ — `src/scx/state/robustness.py` (merge/split/noise impact)
- [x] **跨描述符稳定性** ✅ — `cross_descriptor_stability()` (ARI)
- [x] **Bootstrap 稳健 K** ✅ — `suggest_robust_states()`
- [x] **边界置信度** ✅ — `state_boundary_confidence()`
- [ ] 稳定性定理: state partition 小扰动 → 分类结果变化 bounded
- [ ] **写入 Paper 4 §3.4**

### 1.4 自适应阈值 🟢 P2

- [x] **网格搜索校准** ✅ — `src/scx/valuation/adaptive.py` (`calibrate()`)
- [x] **Sensitivity analysis** ✅ — 阈值 ±20% → 分类变化
- [x] **无监督自适应** ✅ — percentile/gap 方法 (`auto_threshold()`)
- [ ] **写入 Paper 4 §5.1**

---

## Phase 2：实验补强（2-3 月）

### 2.1 SCX + Influence 融合 🟡 P1

- [ ] 实现 `scx/valuation/influence.py` — State-Conditioned Influence
- [ ] CIFAR-100 上对比: SCX vs LESS vs SCX+LESS
- [ ] 证明: SCX 粗选状态 + Influence 细选样本 > 任一单独方法
- [ ] **写入 Paper 4 §6.3**

### 2.2 通用 ML 实验 🟡 P1

- [ ] **CIFAR-100 + 5 ResNet-18**: 每个在不同子集训练 → multi-expert
  - [ ] 注入 label noise (10-30%)
  - [ ] SCX 四分类 vs ground truth noise labels
  - [ ] 对比 Data Shapley (pyDVL), LOO, Random
- [ ] **UCI Tabular × 2**: 10+ 维数据集
  - [ ] 对比 Uncertainty, Diversity, Coreset
- [ ] **产出 3 张 Figure** (acquisition efficiency, classification accuracy, ablation)

### 2.3 自适应阈值 🟢 P2

- [ ] 实现 `DataClassifier.auto_calibrate(X, y_labeled)`
- [ ] Sensitivity analysis: 阈值 ±20% → 分类变化
- [ ] Bayesian 阈值 (可选)
- [ ] **写入 Paper 4 §5.1**

---

## Phase 3：扩展（3-6 月）

### 3.1 Online SCX 🔵 P3

- [ ] 设计 `OnlineSCXFramework` API
- [ ] 增量状态更新 (exponential moving average)
- [ ] 在线专家可靠性追踪
- [ ] 合成数据流实验

### 3.2 Benchmark Suite 🔵 P3

- [ ] 5-10 数据集 (合成 + UCI + 图像 + MLIP)
- [ ] 标准化 API: `benchmark.run(method, dataset) → results`
- [ ] Baseline 集成: Random, Uncertainty, Diversity, Shapley, LESS, Coreset, SCX
- [ ] Leaderboard + 文档

---

## Phase 4：论文写作

### Paper 3 (Expert Compiler) — 等 AlN v4 重训后

- [ ] §3 Expert Compilation Protocol (方向 4)
- [ ] §5 Experiments: retrospective on AlN v3

### Paper 4 (SCX) — 持续更新

- [ ] §3.4 Robustness Analysis (方向 2)
- [ ] §4.3 Compression Theory (方向 1)
- [ ] §5.1 Adaptive Threshold (方向 6)
- [ ] §6.2 General ML Experiments (方向 5)
- [ ] §6.3 Comparison with Influence Methods (方向 3)

---

## 快速索引

| 想做什么 | 看哪个文件 |
|---------|-----------|
| 完整扩展方案 | `SCX_思想扩展_综合方案.md` |
| 核心数学 | `agent_outputs/01_SCX_核心框架_数学分析.md` |
| 子模块设计 | `agent_outputs/02_SCX_子模块_详细设计.md` |
| 竞争分析: 数据估值 | `agent_outputs/03_竞争分析_数据估值与主动学习.md` |
| 竞争分析: MoE/蒸馏 | `agent_outputs/04_竞争分析_MoE与蒸馏.md` |
| 数学根源 | `agent_outputs/05_数学根源与证明.md` |
| 实现架构 | `agent_outputs/06_实现架构与实验设计.md` |
| Python 代码 | `../src/scx/` |
| 测试 | `../tests/` |
