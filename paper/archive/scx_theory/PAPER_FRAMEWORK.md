# Paper: A Complete Theory of Noise Detection via State-Conditioned eXpertise

> **目标期刊**: Annals of Statistics (冲刺) → IEEE Trans. Information Theory (主投) → JMLR (保底)
> **论文类型**: 纯理论（定理+证明），正文 30-40 页 + 补充材料 60-80 页
> **核心卖点**: 充分条件 + 匹配下界 + 不可能性定理 = 完整理论闭环
> **创建日期**: 2026-06-27

---

## 一句话卖点

**We prove that distinguishing label noise from intrinsic sample difficulty requires state-conditioned expertise, establish the exact exponential rate at which multi-expert consistency detects noise (rate-optimal, matching upper and lower bounds), and prove that without our assumptions the problem is fundamentally unidentifiable.**

---

## 数学贡献矩阵

| 组件 | 定理 | 数学工具 | 贡献层级 |
|------|------|----------|:--:|
| **正命题** | Thm 1: F1 ≥ 1 − (1/η)Σρ_s e^{−2MΔ²} | Hoeffding + Chernoff 浓度 | 充分条件 |
| **反命题** | Thm 2: F1 ≤ F1_base + C_F √(δ/2) | Pinsker + Fano + DP 不等式 | 边界条件 |
| **不可能性** | Thm 3: 噪声与困难观测不可区分 | 构造性反例 + 观测等价 | 必要性支柱 |
| **速率最优** | Thm 4: liminf (−1/M)log(F1 下界) = 2Δ² | Bretagnolle-Huber + Hellinger + Le Cam | **核心深度** |
| **算法收敛** | Thm 5: k-means 状态发现一致性 | Pollard (1981) 框架 + Lloyd | 算法基础 |
| **可计算诊断** | Prop 6: Bootstrap ARI 稳定性 ⇔ 特征强度 | Bootstrap + ARI + 聚类稳定性 | 实践桥梁 |

**理论闭环**：
```
Thm 3 (没有假设 → 不可能)
    ↓
假设 A1-A6 成立
    ↓
Thm 1 (充分条件: F1 → 1, 指数速率 2MΔ²)
    + Thm 4 (匹配下界: 速率 2MΔ² 是最优的)
    = 速率最优性 (rate optimality)
    ↓
Thm 2 (边界: 当特征弱时退化到基线)
    + Thm 5 (特征强时算法收敛)
    = 完整的相变图景
```

---

## 正文结构（Annals of Statistics 格式，~35 页）

### 1. Introduction (4 pp)

**叙事弧线**：
1. 开篇钩子：训练数据中，哪些错误是标签错了，哪些是样本太难？这是 ML 中一个未被正视的基础问题。
2. 现有方法（loss-based, confidence-based, Dawid-Skene）隐式假设两者可分——但从未有人证明过它们**确实**可分。
3. 我们证明：**不加额外假设时，两者本质上不可区分**（Thm 3）。
4. 然后给出最小充分假设集（A1-A6），在此之下：
   - 噪声检测 F1 以指数速率收敛到 1（Thm 1）
   - 指数 2MΔ² 是 minimax 最优的（Thm 4）
   - 当特征信息不足时，方法退化到基线（Thm 2）
5. 一张图：理论闭环示意图

### 2. Problem Formulation (3 pp)

- 数据生成模型（潜在变量：真实状态 S, 真实标签 Y*）
- 噪声模型（均匀翻转, A4）
- 多专家设定（不相交训练, A1）
- 一致性得分 C(x) 的定义
- 状态条件检测规则
- 假设 A1-A6 的动机与合理性讨论

### 3. Main Results (14 pp)

#### 3.1 The Unidentifiability Theorem (Thm 3) — 3 pp
- 形式化陈述：两个观测等价世界
- 构造：世界 A（噪声） vs 世界 B（困难）
- K=2 完整构造 + K>2 推广
- 推论：打破不可识别性的最小充分条件

#### 3.2 Noise Detection Guarantee (Thm 1) — 4 pp
- Lemma 1: 均值分离（噪声 vs 清洁的 E[C|x] 差距）
- Lemma 2: FPR 上界 (Hoeffding)
- Lemma 3: TPR 下界 (Hoeffding + C_bal)
- 主定理：F1 下界
- Chernoff 紧化形式
- 推论：M 的选择, 最优阈值, 有限样本校正

#### 3.3 Minimax Rate Optimality (Thm 4) — 4 pp
- 陈述：liminf_{M→∞} (−1/M) log(min_F1_error) = 2Δ²
- Le Cam 两点法框架
- Bretagnolle-Huber 不等式 + Hellinger 距离
- 构造困难分布对 (P_noise, P_hard)
- 匹配上下界 → 速率最优

#### 3.4 Weak Feature Boundary (Thm 2) — 3 pp
- δ = I(φ(X); S) 定义特征弱度
- Fano 不等式 → 状态估计误差下界
- Pinsker → TV ≤ √(δ/2)
- 退化到损失基线的条件
- 推论：最小信息阈值, 状态数的影响

### 4. Algorithmic Foundation (4 pp)

#### 4.1 Cluster Consistency for State Discovery (Thm 5)
- Pollard (1981) 框架推广
- 固定 K, Lloyd's + random restarts
- 4 引理结构

#### 4.2 Bootstrap Stability Diagnostic (Prop 6)
- Bootstrap ARI 作为特征强度的可计算代理
- 与互信息 δ 的关系
- 实用诊断协议

### 5. Connections to Existing Theory (4 pp)

- Dawid-Skene 作为特例（单状态退化）
- 标签噪声理论（噪声转移矩阵不可识别性）
- PAC-Bayes 泛化界
- 众包/标注者一致性模型
- 因果推断视角（马尔可夫等价类）

### 6. Numerical Validation (3 pp)

- 合成数据：验证指数速率（M 增大时 F1 的收敛）
- AlN v3：真实数据上理论界与经验 F1 的一致性
- CIFAR-10/MNIST：跨领域验证
- Bootstrap ARI 诊断有效性

### 7. Discussion (2 pp)

- 理论局限：常数最优性未证明, K>2 下界待紧化
- 实践意义：特征工程优先于架构调优
- 开放问题：增长-K 渐近, 常数最优性, 非均匀噪声

---

## 补充材料结构（~70 页）

### S1. Full Proof of Theorem 1 (15 pp)
- 详细假设讨论
- Lemma 1-3 完整证明
- F1 下界推导的每一步
- Chernoff 附录
- 非 0-1 损失推广
- 所有推论的证明

### S2. Full Proof of Theorem 2 (15 pp)
- 马尔可夫链与数据处理不等式的详细推导
- Fano 不等式应用
- 辅助分布 P̃ 构造与 KL 计算
- AUC/PR-AUC/F1 的 TV 界转化
- C_F Lipschitz 常数的数值验证
- 各推论的证明

### S3. Full Proof of Theorem 3 (10 pp)
- K=2 构造的完整验证
- K>2 推广（随机专家构造）
- 推论 1-6 的证明
- 与 Dawid-Skene 不可识别性的关系

### S4. Full Proof of Minimax Lower Bound (Thm 4) (15 pp)
- Bretagnolle-Huber 不等式完整推导
- Hellinger 距离在稀疏信号下的紧致性
- F1 分解的完整代数
- 两轮 bug 修复记录
- Slud 不等式为何被弃用

### S5. Full Proof of Cluster Consistency (Thm 5) (10 pp)
- Pollard (1981) 框架回顾
- 4 引理完整证明
- Lloyd's + random restarts 的 ε-近似保证
- 固定-K vs 增长-K 的讨论

### S6. Bootstrap Stability Diagnostic (Prop 6) (5 pp)
- Bootstrap ARI 的分布性质
- 与互信息 δ 的 Monte Carlo 对比
- 诊断阈值校准

### S7. Additional Numerical Experiments (10 pp)
- 合成数据相变图
- AlN v3 完整各状态诊断
- CIFAR-10 各噪声率下 F1 曲线
- DermaMNIST 弱特征详细分析

---

## 写作分工（从现有文件到论文章节）

| 论文章节 | 源文件 | 状态 |
|----------|--------|:--:|
| §3.1 (Thm 3) | `theory/theorems/03_unidentifiability_theorem.md` (540行) | ✅ 已修复 |
| §3.2 (Thm 1) | `theory/theorems/01_noise_detection_guarantee.md` (519行) | ✅ 已修复 |
| §3.3 (Thm 4) | `theory/explorations/minimax_lower_bound_v2.md` (1023行) | ✅ v2 通过 |
| §3.4 (Thm 2) | `theory/theorems/02_weak_feature_failure.md` (633行) | ✅ 已修复 |
| §4.1 (Thm 5) | `theory/explorations/cluster_consistency_v2.md` (748行) | ✅ v2 通过 |
| §4.2 (Prop 6) | `theory/explorations/feature_strength_via_stability.md` (614行) | ✅ 完成 |
| §5 (Connections) | `theory/paper3_upgrades/*.md` + DS 比较 | 🔲 待整合 |
| §6 (Numerical) | 实验报告 | 🔲 待整理 |
| S1-S6 | 上述证明文件 | ✅ 已就绪 |

---

## 与现有 Paper 3 (JMLR) 的关系

本论文是 Paper 3 的**升级版**：
- Paper 3 (JMLR): 3 个核心定理 + PAC-Bayes + DS 比较
- 本论文 (Annals/IT): 6 个定理/命题 + 匹配下界 + 聚类一致性 + 稳定性诊断

如果本论文投 Annals/IT，Paper 3 (JMLR) 可以取消。如果被拒转 JMLR，则合并回 Paper 3 路线。

---

## 写作时间线

| 阶段 | 内容 | 预计时间 |
|------|------|:--:|
| Phase 1 | 正文 §1-3 草稿（定理 1-4） | 2 周 |
| Phase 2 | 正文 §4-7 + 补充 S1-S6 | 2 周 |
| Phase 3 | 内部审查 + 数值实验补充 | 1 周 |
| Phase 4 | 英文润色 + 格式调整 | 1 周 |
| **投稿** | | **6 周后** |

---

## 期刊要求速查

### Annals of Statistics
- 页数：通常 30-50 页
- 补充材料：允许，单独文件
- 风格：Theorem-Proof 结构，强调数学严格性
- 关键词：minimax, concentration inequalities, information theory, identifiability

### IEEE Trans. Information Theory
- 页数：通常 20-40 页（双栏）
- 补充材料：允许
- 风格：信息论框架优先，Fano/Pinsker/KL 是标准语言
- 关键词：mutual information, Fano's inequality, minimax lower bound, hypothesis testing

---

*关联：[[../05_决策/论文规划|论文规划]] · [[NOW_Nature_JMLR]] · [[深水区理论]]*
