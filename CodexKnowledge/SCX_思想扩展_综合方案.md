# SCX 思想扩展 — 基于 6 Agent 讨论的综合方案

> 生成：2026-06-26 | 基于 356KB agent 输出的交叉分析

---

## 0. 现有基础

### 已完成的（v0.1.0）

| 维度 | 状态 |
|------|------|
| 核心数学框架 (R_m(s), SCX_m(s), V(s)) | ✅ 完整定义 + 3 命题证明 |
| 数据四分类 (Valuable/Redundant/Noisy/Expert-dep) | ✅ 规则引擎 |
| Python 包 (30 files, 6269 lines, 259 tests) | ✅ 全模块实现 |
| 合成实验框架 | ✅ data_generator + run_experiment |
| 数学根源追溯 | ✅ Kolmogorov → PAC-Bayes |
| 竞争格局分析 | ✅ 6 维度覆盖，Expert Governance 是独有创新区 |
| SCX-Compress (加权 coreset) | ✅ 算法框架，缺理论证明 |

### 竞争格局中的独特位置

```
SCX 是唯一覆盖 6 个维度的方法：
  数据估值 + 数据选择 + 多专家 + 状态条件 + 噪声检测 + 可学习性

Expert Governance（蒸馏前专家规范化）是 SCX 的独有创新区
——没有已有工作在 MLIP 领域讨论跨专家冲突仲裁和域认证
```

---

## 1. 可发展的 8 个方向

### 方向 1：SCX-Compress 理论加固 🔴 P0

**现状**：算法已实现（weighted_random/kcenter/herding），缺理论保证。

**发展内容**：
- **Coreset 保真定理**：证明 SCX-Compress 的冗余分数 D(s) 与经验风险近似误差之间的 bound
  $$\sup_{f \in \mathcal{F}} \left|\frac{1}{N}\sum_i \ell(f(x_i),y_i) - \frac{1}{N}\sum_j w_j \ell(f(x_j^*),y_j^*)\right| \leq \epsilon(D)$$
- **样本复杂度**：压缩到多少比例还能保持 95% 精度？
- **与 Dataset Distillation 的等价性**：SCX-Compress 在什么条件下等价于梯度匹配蒸馏？

**实现**：
- 在合成数据上验证 bound
- CIFAR-100 上对比 coreset baseline (K-Center, Herding, Random)

---

### 方向 2：State Discovery 鲁棒性分析 🟡 P1

**现状**：SCX 假设 state discovery 已完成，但真实场景中 state 是 latent 的。

**发展内容**：
- **误指定分析**：如果状态划分有误差（merge 了两个不同状态、split 了一个同质状态），SCX 分类的结果会偏离多少？
- **稳定性定理**：证明在什么条件下，状态划分的小扰动不会改变数据分类结果
- **自适应状态数**：不预设 K，根据 SCX 性能自动调整
- **跨描述符稳定性**：用不同 φ（ACE/SOAP/MBTR）重复分析，量化 cluster 一致性

**实现**：
- 合成实验中引入 controlled mis-specification
- 添加 `StateDiscovery.stability_analysis()` 方法

---

### 方向 3：SCX 与 Influence Function 的融合 🟡 P1

**现状**：竞争分析显示 Data Shapley 和 Influence Function 是主要对手，但 SCX 的 state-level 视角可以与它们互补。

**发展内容**：
- **State-Conditioned Influence**：传统 influence 是 $\mathcal{I}(x_i, x_j)$，SCX 版本是 $\mathcal{I}_s(x_i, x_j) = \mathcal{I}(x_i, x_j | x_i, x_j \in s)$
- **两阶段估值**：SCX 粗选状态 → Influence/Shapley 细选样本
- **与 LESS 的对比**：LESS 用梯度相似性选数据，SCX 用状态价值选数据——两者结合可以同时考虑"对模型影响大"和"状态覆盖不足"

**实现**：
- 在 CIFAR-100 实验中加入 LESS baseline
- 实现 `scx/valuation/influence.py`

---

### 方向 4：Expert Governance Protocol 形式化 🔴 P0

**现状**：竞争分析确认这是 SCX 的独有创新区——没有已有工作。但当前只是概念框架。

**发展内容**：
- **Governance 协议**：形式化定义 expert 进入蒸馏前的必要步骤
  1. Gauge Check → 2. Domain Certificate → 3. Conflict Resolution → 4. Anchor Verification → 5. Distillation Authorization
- **Certification Bound**：给定 N 个 DFT anchor，专家在状态 s 的可靠性估计误差不超过 ε 的概率 ≥ 1-δ
- **协议状态机**：每个 (expert, state) pair 经过协议后得到一个状态：`certified` / `conditionally_certified` / `uncertified` / `rejected`

**实现**：
- 在 AlN v3 数据上做 retrospective 验证（已有 DFT 标签可以作为 anchor）
- 论文级输出：Protocol specification + Certification theorem

---

### 方向 5：SCX 通用 ML 实验 🟡 P1

**现状**：合成实验框架就绪，但缺真实数据实验。竞争分析中审稿人攻击点 4b 指出"合成实验不能证明在高维数据上有效"。

**发展内容**：
- **CIFAR-100 + 5 ResNet-18**：每个 ResNet 在不同类别子集上训练，模拟 multi-expert 场景
- **UCI Tabular Benchmark**：10+ 维真实数据，展示 SCX 不限于图像
- **对比**：Data Shapley (via pyDVL), LOO, Random, Uncertainty, Diversity + SCX
- **关键指标**：相同标注预算下模型精度提升、数据分类准确率

**实现**：
- 扩展现有 `experiments/ml_benchmarks/`
- 产出 2-3 张 Figure 级图表

---

### 方向 6：SCX 自适应阈值 🟢 P2

**现状**：四分类的阈值（error_high=0.05, density_high=0.05, consistency_high=0.7）是人为预设的。审稿人攻击点 4c 指出这是"参数化的数据描述"。

**发展内容**：
- **数据驱动的阈值选择**：在合成数据上扫描参数空间，找到使分类准确率最大的阈值
- **自适应阈值**：根据数据分布自动调整——高维稀疏数据用更宽松的阈值
- **Bayesian 阈值**：将阈值建模为随机变量，用少量标注数据推断后验

**实现**：
- 添加 `DataClassifier.auto_calibrate(X, y_labeled)` 方法
- Sensitivity analysis: 阈值变化 ±20% 对分类结果的影响

---

### 方向 7：Online SCX 🔵 P3

**现状**：SCX 是批处理模式——收集一批数据后统一分析。

**发展内容**：
- **增量状态更新**：新数据到来时，不重新聚类，而是更新现有状态的质心和半径
- **在线专家可靠性追踪**：用 exponential moving average 更新 R_m(s)
- **数据流版本的四分类**：实时判断 incoming sample 是 valuable/redundant/noisy/expert-dependent

**实现**：
- `scx/core/online.py` — OnlineSCXFramework
- 合成数据流实验

---

### 方向 8：SCX Benchmark Suite 🔵 P3

**现状**：没有标准化的评估框架来比较 state-conditioned data valuation 方法。

**发展内容**：
- **Benchmark 设计**：5-10 个数据集（合成 + UCI + 图像 + MLIP），每个有预定义的 ground-truth state
- **评估指标**：state discovery accuracy, expert routing precision, data classification F1, acquisition efficiency
- **Baseline 集成**：Random, Uncertainty, Diversity, Data Shapley, LESS, Coreset

**实现**：
- `experiments/benchmark/` 目录
- 标准化 API：`benchmark.run(method, dataset) → results`

---

## 2. 优先级矩阵

| 方向 | 优先级 | 理论深度 | 实验难度 | 论文贡献 | 时间估计 |
|------|--------|---------|---------|---------|---------|
| 1. SCX-Compress 理论 | 🔴 P0 | 高 | 低 | **Paper 4 核心定理** | 2-4 周 |
| 4. Expert Governance Protocol | 🔴 P0 | 高 | 中 | **Paper 3 核心框架** | 4-6 周 |
| 2. State Discovery 鲁棒性 | 🟡 P1 | 高 | 低 | Paper 4 鲁棒性章节 | 2-3 周 |
| 3. SCX + Influence 融合 | 🟡 P1 | 中 | 中 | Paper 4 实验亮点 | 3-4 周 |
| 5. 通用 ML 实验 | 🟡 P1 | 低 | 中 | **审稿人必需** | 3-5 周 |
| 6. 自适应阈值 | 🟢 P2 | 低 | 低 | Paper 4 消融实验 | 1-2 周 |
| 7. Online SCX | 🔵 P3 | 中 | 中 | 未来 Paper 5 | 4-8 周 |
| 8. Benchmark Suite | 🔵 P3 | 低 | 高 | 社区影响力 | 6-10 周 |

---

## 3. Roadmap

```
Phase 1 (1-2 月): 理论加固
  ├── SCX-Compress 定理 + 证明
  ├── State Discovery 鲁棒性定理
  └── Expert Governance Protocol 形式化

Phase 2 (2-3 月): 实验补强
  ├── CIFAR-100 + UCI 实验
  ├── SCX + Influence 对比实验
  └── 自适应阈值 sensitivity analysis

Phase 3 (3-6 月): 扩展
  ├── Online SCX 原型
  └── Benchmark Suite 设计
```

---

## 4. 与论文谱系的对应关系

`EGP Paper 1 (egp/)` → `SCX-Theory` → `SCX-MLIP` → `SCX-Sim` → `SCX-Health`

| 方向 | 贡献给 | 具体位置 |
|------|--------|---------|
| 1. SCX-Compress 理论 | **SCX-Theory (Paper 2)** | §4 Data Value → §4.3 Compression Theory |
| 2. State Discovery 鲁棒性 | **SCX-Theory (Paper 2)** | §3 State Discovery → §3.4 Robustness Analysis |
| 3. SCX + Influence 融合 | **SCX-MLIP (Paper 3)** | §6 Experiments → §6.3 Comparison with Influence |
| 4. Expert Governance | **SCX-MLIP (Paper 3)** | §3 Expert Compilation Protocol |
| 5. 通用 ML 实验 | **SCX-MLIP (Paper 3)** | §6.2 General ML Experiments |
| 6. 自适应阈值 | **SCX-MLIP (Paper 3)** | §5.1 Adaptive Threshold Calibration |
| 7. Online SCX | **SCX-Sim (Paper 4)** | 未来方向 |
| 8. Benchmark Suite | 社区贡献 | 独立 release |

---

*本方案综合了 6 份 agent 输出（01-06，共 356KB），交叉分析竞争格局、数学基础、实现现状后提炼。*
