---
tags: [TODO, 实验, CPU可做]
created: 2026-06-27
status: active
---

# 🔬 实验任务

---

## 一、CPU 立即可做的实验

### E1: UCI Tabular Benchmarks 🔴

**目标**：在 tabular 数据上验证 SCX 噪声检测和压缩，为 Paper 1 增加一个领域。

**环境**：CPU 可做（numpy, scipy, sklearn 就绪）

- [ ] **E1.1** 选择 3-5 个 UCI 数据集
  - 候选：Adult, Wine Quality, Breast Cancer, Diabetes, Bank Marketing
  - 标准：≥ 1000 samples, ≥ 10 features, binary or multi-class

- [ ] **E1.2** 实现 SCX tabular pipeline
  - TabularEncoder（直接用原始特征 + StandardScaler）
  - 训练 5 个异构专家（不同 ML 模型：RF, XGBoost, Logistic, MLP, KNN）

- [ ] **E1.3** 噪声检测实验
  - 注入 10%, 20% 标签噪声
  - SCX-Noise vs Loss-based vs Confidence-based
  - 报告 Precision, Recall, F1

- [ ] **E1.4** 压缩实验
  - SCX-Compress vs Random vs K-Center
  - 压缩比 20%, 30%, 50%
  - 报告精度保持

- [ ] **E1.5** 产出实验报告 → `experiments/tabular/results/`

### E2: 公开 MLIP 数据下载与分析 🟡

**目标**：在非 AlN 体系上运行 SCX 分析，展示跨材料泛化。

- [ ] **E2.1** 下载公开 ACE 训练数据
  - Si (ColabFit 或 OpenKIM)
  - Cu (ColabFit)
  - MgO (ColabFit)
  - 目标 ≥ 3 个体系

- [ ] **E2.2** 对每个体系运行 SCX 单层分析
  - MLIPEncoder (12-dim ACE descriptor)
  - 报告噪声检测结果

- [ ] **E2.3** 对发现噪声的体系运行两层分析

- [ ] **E2.4** 产出跨材料对比报告 → `experiments/mlip_case/cross_material/`

### E3: 合成实验 2D 增强 🟢

**目标**：在已知 ground truth 的合成数据上，系统性验证定理 1 和定理 2。

- [ ] **E3.1** 设计 4 个 controlled 合成场景
  - 场景 A: 高特征信息量 + 低噪声（SCX 应完美工作）
  - 场景 B: 高特征信息量 + 高噪声（SCX 应工作良好）
  - 场景 C: 低特征信息量 + 低噪声（SCX 应退化）
  - 场景 D: 低特征信息量 + 高噪声（SCX 应退化到 random）

- [ ] **E3.2** 每个场景变化专家数量 M ∈ {3, 5, 10}

- [ ] **E3.3** 每个场景变化状态划分粒度 K ∈ {3, 5, 10, 20}

- [ ] **E3.4** 验证定理 1：画出 F1 vs M, F1 vs K 的曲线

- [ ] **E3.5** 验证定理 2：画出 F1 vs I(φ(x); y) 的曲线

- [ ] **E3.6** 产出合成验证报告 → `experiments/synthetic/theorem_validation/`

---

## 二、CPU 可做的数据分析（不等 GPU）

### E4: AlN v3 数据深度分析

- [ ] **E4.1** 分析 fmax 与结构参数的关联
  - 哪些结构性特征（键长、配位、应变）与高 fmax 相关？
  - 验证 ErrorDrivenEncoder 选出的 4 个维度是否在不同 random seed 下稳定

- [ ] **E4.2** 分析 phonon batch 的冗余结构
  - 120 帧全部落入同一低误差状态
  - 计算 phonon 内部的结构多样性（pairwise distance distribution）
  - 估算安全压缩比

- [ ] **E4.3** 分析 thermal batch 噪声的物理起源
  - 53 帧噪声是否来自特定温度？
  - 是否与原子间距过近直接相关？

### E5: 竞争方法对比分析

- [ ] **E5.1** 在 AlN v3 上实现并对比
  - Confident Learning (Northcutt et al.)
  - Ensemble disagreement (标准方法)
  - Loss-based detection
  - SCX-Noise
  - 统一 F1 对比表

---

## 三、等 GPU 的实验

> 详细列表见 [[GPU_等待]]

---

*关联：[[NOW_理论]], [[GPU_等待]]*
