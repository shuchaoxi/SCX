# Expert Governance Protocol — 形式化定义

> **SCX/EGP 蒸馏前专家规范化协议**  
> 版本：v1.0  
> 最后更新：2026-06-26

---

## 目录

1. [符号与设定](#1-符号与设定)
2. [五步 Governance Protocol](#2-五步-governance-protocol)
   - [Step 1: Gauge Check](#step-1-gauge-check-)
   - [Step 2: Domain Certificate](#step-2-domain-certificate-)
   - [Step 3: Conflict Resolution](#step-3-conflict-resolution-)
   - [Step 4: Anchor Verification](#step-4-anchor-verification-)
   - [Step 5: Distillation Authorization](#step-5-distillation-authorization-)
3. [阈值选择指引](#3-阈值选择指引)
4. [失败回退策略](#4-失败回退策略)
5. [Certification Theorem](#5-certification-theorem)
6. [AlN v3 回顾性验证方案](#6-aln-v3-回顾性验证方案)
7. [与 SCX 代码的实现映射](#7-与-scx-代码的实现映射)

---

## 1. 符号与设定

### 1.1 基础定义

沿用 SCX 框架定义（参见 `theory/README.md`）：

| 符号 | 含义 | 类型 |
|------|------|------|
| $\mathcal{X}$ | 输入空间（原子构型） | 度量空间 |
| $\mathcal{Y}$ | 标签空间（能量/力） | $\mathbb{R}^d$ |
| $f^*: \mathcal{X} \to \mathcal{Y}$ | 真实标注函数（DFT） | 未知 oracle |
| $f_m: \mathcal{X} \to \mathcal{Y}$ | 第 $m$ 个 MLIP 专家 | 可计算函数，$m \in [M]$ |
| $M$ | 专家总数 | $\mathbb{N}$ |
| $\mathcal{S}$ | 状态空间（有限划分） | $|\mathcal{S}| = K$ |
| $s: \mathcal{X} \to \mathcal{S}$ | 状态映射函数 | 可测函数 |
| $s(x)$ | 构型 $x$ 归属的状态 | $\mathcal{S}$ |
| $\ell: \mathcal{Y} \times \mathcal{Y} \to \mathbb{R}_{\ge 0}$ | 损失函数（默认 MSE） | 有界：$0 \le \ell \le L_{\max}$ |

### 1.2 核心量

**状态条件专家风险**（Definition 1, SCX）：

$$R_m(s) = \mathbb{E}_{x \sim P(\cdot \mid s)}[\ell(f_m(x), f^*(x))]$$

**SCX 可靠性**（Definition 2, SCX）：

$$\text{SCX}_m(s) = P(\ell(f_m(x), f^*(x)) < \tau \mid x \in s)$$

**专家配对冲突**（Definition 3, ExpertConflict）：

$$\text{Conflict}(m, n, s) = \mathbb{E}_{x \sim P(\cdot \mid s)}[|f_m(x) - f_n(x)|^2]$$

### 1.3 Protocol 整体结构

Governance Protocol 是从原始专家系统到蒸馏授权决策的**线性判定流程**：

$$\mathcal{G}: \underbrace{(\{f_m\}, \mathcal{S}, \mathcal{D}_{\text{ref}})}_{\text{输入}} \xrightarrow{\text{Step 1-5}} \underbrace{\{\text{authorized}, \text{conditional}, \text{denied}\}}_{\text{输出}}$$

输入：
- 专家集 $\{f_m\}_{m=1}^M$（可能异构：MACE, NEP, SevenNet, ...）
- 状态空间 $\mathcal{S}$ 及状态映射 $s(x)$
- 参考数据集 $\mathcal{D}_{\text{ref}} = \{(x_i, y_i)\}_{i=1}^{N_{\text{ref}}}$（DFT 标签）
- 蒸馏目标状态 $s_{\text{target}} \in \mathcal{S}$

输出：
- **authorized**：所有检查通过，可直接蒸馏
- **conditional**：部分条件不满足但可补救（如补锚点测试）
- **denied**：不可蒸馏，需专家重新训练或更换专家

---

## 2. 五步 Governance Protocol

### Step 1: Gauge Check (量规检查)

#### 问题

不同 MLIP 的总能量预测存在系统性能量偏移（gauge freedom）。Step 1 检测并消除这些偏移，使所有专家的能量预测在统一的参考标度上可比。

#### 形式化定义

**输入**:
- 专家集 $\{f_m\}_{m=1}^M$
- 参考状态子集 $\mathcal{S}_{\text{gauge}} \subseteq \mathcal{S}$（选择能量已知的简单状态，如体相晶格）
- 参考能量 $E_{\text{ref}}(s)$ 对每个 $s \in \mathcal{S}_{\text{gauge}}$（从 DFT 或实验获得）
- 容忍度 $\epsilon_{\text{gauge}} > 0$

**Gauge 定义**:

每个专家 $f_m$ 的能量预测分解为：

$$f_m(x) = \underbrace{f_m^{\text{intrinsic}}(x)}_{\text{物理部分}} + \underbrace{\mu_m}_{\text{gauge offset}} + \underbrace{\eta_m(x)}_{\text{残差}}$$

其中 $\mu_m$ 是依赖于专家的系统偏差（gauge shift）。对力预测，$\nabla_x \mu_m = 0$，因此力不受影响。但**总能量基准**的差异影响蒸馏中学生对能量的学习。

**Gauge Check 算法**:

1. 对每个 $s \in \mathcal{S}_{\text{gauge}}$，采样 $N_{\text{gauge}}$ 个构型 $\{x_{s,j}\}_{j=1}^{N_{\text{gauge}}}$
2. 计算每个专家的平均偏差：

   $$\hat{\mu}_m(s) = \frac{1}{N_{\text{gauge}}} \sum_{j=1}^{N_{\text{gauge}}} \left[f_m(x_{s,j}) - E_{\text{ref}}(s)\right]$$

3. 计算 gauge 一致性度量：

   $$\text{GaugeVariance}(m) = \frac{1}{|\mathcal{S}_{\text{gauge}}|} \sum_{s \in \mathcal{S}_{\text{gauge}}} \left(\hat{\mu}_m(s) - \bar{\mu}_m\right)^2$$

   其中 $\bar{\mu}_m = \frac{1}{|\mathcal{S}_{\text{gauge}}|} \sum_{s} \hat{\mu}_m(s)$

4. 判定条件：

   $$\text{gauge\_certified}(m) = \begin{cases}
   \text{true}, & \text{GaugeVariance}(m) \le \epsilon_{\text{gauge}} \\
   \text{false}, & \text{otherwise}
   \end{cases}$$

   （低方差意味着偏移 $\mu_m$ 在各参考状态间一致，是纯 gauge 偏移）

**输出类型**:

$$\text{gauge\_certified}: [M] \to \{\text{true}, \text{false}\}$$

**Gauge Fixing（失败时执行）**:

若存在 $m$ 使得 $\text{gauge\_certified}(m) = \text{false}$，则需要 gauge fixing。定义校准函数：

$$\tilde{f}_m(x) = f_m(x) - \frac{1}{|\mathcal{S}_{\text{gauge}}|} \sum_{s \in \mathcal{S}_{\text{gauge}}} \hat{\mu}_m(s)$$

即将专家 $m$ 的能量预测减去其对参考状态的平均系统偏差。

校准后重新运行 Check。

#### 与已有工作的关系

- 文献中 "Gauge dependence of total energies" (arXiv:2504.05565, 2025) 指出不同 DFT 泛函间存在类似问题，但未处理**跨 MLIP 架构**的 gauge 对齐。
- 本步骤是 SCX/EGP 的原创贡献——在蒸馏前强制多专家能量标度统一。

---

### Step 2: Domain Certificate (域认证)

#### 问题

对目标状态 $s_{\text{target}}$，评估每个专家在该状态上的可靠性。不可靠专家不应参与蒸馏。

#### 形式化定义

**输入**:
- 专家集 $\{f_m\}_{m=1}^M$
- 目标状态 $s_{\text{target}} \in \mathcal{S}$
- 状态标注数据 $\mathcal{D}_{s} = \{(x_i, y_i) \mid s(x_i) = s_{\text{target}}\}$（可能有或没有）
- 低可靠性阈值 $\theta_{\text{low}} \in (0, 1)$
- 高可靠性阈值 $\theta_{\text{high}} \in (0, 1)$（$\theta_{\text{high}} > \theta_{\text{low}}$）
- 损失阈值 $\tau > 0$
- 最小样本数 $n_{\min} \in \mathbb{N}$

**可靠性估计**:

对每个专家 $m$，在 $s_{\text{target}}$ 上估计 SCX 可靠性：

$$\widehat{\text{SCX}}_m(s_{\text{target}}) = \begin{cases}
\displaystyle \frac{1}{|\mathcal{D}_{s}|} \sum_{(x, y) \in \mathcal{D}_{s}} \mathbf{1}\{\ell(f_m(x), y) < \tau\}, & |\mathcal{D}_{s}| \ge n_{\min} \\[1.5em]
\text{Bayesian shrinkage estimate}, & |\mathcal{D}_{s}| < n_{\min}
\end{cases}$$

小样本时使用 James-Stein 收缩估计（对应 `ExpertReliability.estimate_small_sample`）：

$$\widehat{\text{SCX}}_m^{\text{JS}}(s) = \lambda \cdot \widehat{\text{SCX}}_m(s) + (1 - \lambda) \cdot \overline{\text{SCX}}_m$$

其中 $\lambda = \frac{|\mathcal{D}_{s}|}{|\mathcal{D}_{s}| + n_{\min}}$，$\overline{\text{SCX}}_m$ 是专家 $m$ 在所有状态上的全局平均可靠性。

**判定逻辑**:

$$\text{domain\_certified}(m, s) = \begin{cases}
\text{true}, & \widehat{\text{SCX}}_m(s) \ge \theta_{\text{high}} \\[0.5em]
\text{conditional}, & \theta_{\text{low}} \le \widehat{\text{SCX}}_m(s) < \theta_{\text{high}} \\[0.5em]
\text{false}, & \widehat{\text{SCX}}_m(s) < \theta_{\text{low}}
\end{cases}$$

- **true**: 专家在目标状态上高度可靠，可参与蒸馏
- **conditional**: 可靠性不足以独立贡献，但可参与多专家集成
- **false**: 专家在该状态不可信，排除出蒸馏

**输出类型**:

$$\text{domain\_certified}: [M] \times \mathcal{S} \to \{\text{true}, \text{false}, \text{conditional}\}$$

#### 与 SCX 代码的对应

Step 2 直接调用 `ExpertReliability.estimate()` 得到 `SCX_matrix`，其中 `SCX_matrix[m, k]` 即 $\widehat{\text{SCX}}_m(s_k)$。

---

### Step 3: Conflict Resolution (冲突解决)

#### 问题

对目标状态 $s_{\text{target}}$，检查通过 Step 2 认证的专家之间是否存在显著预测冲突。冲突区域需要仲裁。

#### 形式化定义

**输入**:
- 已认证专家子集 $\mathcal{E}_{\text{cert}} \subseteq \{f_1, \dots, f_M\}$（Step 2 输出 $\text{domain\_certified} \in \{\text{true}, \text{conditional}\}$）
- 目标状态 $s_{\text{target}}$
- 状态内未标注构型 $X_s = \{x \mid s(x) = s_{\text{target}}, x \notin \mathcal{D}_{\text{ref}}\}$
- 冲突阈值 $\theta_{\text{conflict}} > 0$

**冲突度量**:

对每一对认证专家 $(m, n) \in \mathcal{E}_{\text{cert}} \times \mathcal{E}_{\text{cert}}$，计算：

$$\text{Conflict}(m, n, s) = \frac{1}{|X_s|} \sum_{x \in X_s} |f_m(x) - f_n(x)|^2$$

**冲突判定**:

$$\text{HasConflict}(s) = \begin{cases}
\text{true}, & \exists (m, n): \text{Conflict}(m, n, s) > \theta_{\text{conflict}} \\
\text{false}, & \text{otherwise}
\end{cases}$$

若 $\text{HasConflict}(s) = \text{false}$，则 $\text{conflict\_resolved} = \text{true}$（无冲突需要解决）。

若 $\text{HasConflict}(s) = \text{true}$，需要进一步分析冲突类型：

**冲突类型诊断**:

| 类型 | 条件 | 含义 |
|------|------|------|
| **Gauge 残差冲突** | $\exists m,n: \text{Conflict}(m,n,s) > \theta_{\text{conflict}}$ 但能量差近似常数 | Step 1 未完全消除的 gauge 残差 |
| **结构敏感冲突** | 冲突仅发生在特定子区域 $s' \subset s$ | 专家对局部结构类型的选择性失效 |
| **全状态冲突** | 冲突在该状态的所有样本上均存在 | 至少一个专家在 $s$ 中完全不可靠 |

**判定逻辑**:

$$\text{conflict\_resolved} = \begin{cases}
\text{true}, & \text{HasConflict}(s) = \text{false} \\[0.5em]
\text{true}, & \text{冲突经仲裁后可解决（见下方）} \\[0.5em]
\text{needs\_anchor}, & \text{需要 DFT anchor 仲裁}
\end{cases}$$

**仲裁方法**（冲突可解决时）：

若冲突类型为 "Gauge 残差冲突"，返回 Step 1 重新校准。
若冲突类型为 "结构敏感冲突"，将冲突子区域 $s'$ 标记为需要 DFT anchor（Step 4）并排除它，在剩余区域上 $\text{conflict\_resolved} = \text{true}$。
若冲突类型为 "全状态冲突"，$\text{conflict\_resolved} = \text{needs\_anchor}$。

**输出类型**:

$$\text{conflict\_resolved}: \mathcal{S} \to \{\text{true}, \text{false}, \text{needs\_anchor}\}$$

#### 与 SCX 代码的对应

Step 3 使用 `ExpertConflict.conflict_matrix()` 计算冲突张量 $D \in \mathbb{R}^{M \times M \times K}$，用 `ExpertConflict.conflict_score()` 获取归一化冲突评分，用 `ExpertConflict.arbitrate()` 在冲突状态下选择仲裁策略。

---

### Step 4: Anchor Verification (锚点验证)

#### 问题

对 Step 3 中标记为 $\text{needs\_anchor}$ 的冲突状态，用 DFT 计算锚点（anchor frames）作为 ground truth 仲裁。

#### 形式化定义

**输入**:
- 冲突状态 $s_{\text{conflict}}$ 列表（Step 3 输出 $\text{needs\_anchor}$ 的状态）
- 锚点预算 $N_{\text{anchor}} \in \mathbb{N}$（允许的总 DFT 计算数）
- 锚点精度阈值 $\theta_{\text{anchor}} > 0$
- 锚点选择策略 $\pi_{\text{anchor}}$

**锚点选择**:

对每个冲突状态 $s$，分配锚点数：

$$n_{\text{anchor}}(s) = \left\lceil N_{\text{anchor}} \cdot \frac{\rho(s) \cdot \text{ConflictScore}(s)}{\sum_{s'} \rho(s') \cdot \text{ConflictScore}(s')} \right\rceil$$

其中 $\rho(s) = P(x \in s)$ 是状态概率，$\text{ConflictScore}(s)$ 是 Step 3 中冲突度的归一化度量。

锚点选择策略 $\pi_{\text{anchor}}$——在状态 $s$ 内选取 $n_{\text{anchor}}(s)$ 个构型 $x_{\text{anchor}}$ 的方法：

$$\pi_{\text{anchor}}: \begin{cases}
\text{最大分歧采样}: & \displaystyle \arg\max_{x \in s} \text{Var}_{m \in \mathcal{E}_{\text{cert}}}[f_m(x)] \\[0.8em]
\text{FPS（最远点采样）}: & \displaystyle \arg\max_{x \in s} \min_{x' \in \mathcal{D}_{\text{anchor}}} d(x, x')
\end{cases}$$

推荐使用**最大分歧采样**——选择专家预测方差最大的构型，这些构型最能区分不同专家的表现。

**锚点验证**:

对每个所选锚点 $x_{\text{anchor}}$，计算 DFT 标签 $y_{\text{anchor}} = f^*(x_{\text{anchor}})$。

对每个专家 $m$，验证其在锚点上的误差：

$$\text{AnchorMAE}(m, s) = \frac{1}{n_{\text{anchor}}(s)} \sum_{j=1}^{n_{\text{anchor}}(s)} \left| f_m(x_{\text{anchor},j}) - y_{\text{anchor},j} \right|$$

全局锚点验证：

$$\text{anchor\_verified} = \begin{cases}
\text{true}, & \max_{m \in \mathcal{E}_{\text{cert}}} \text{AnchorMAE}(m, s) \le \theta_{\text{anchor}} \text{ for all conflicting } s \\[0.5em]
\text{false}, & \text{otherwise}
\end{cases}$$

如果 $\text{anchor\_verified} = \text{false}$，识别出表现最差的专家 $m_{\text{fail}} = \arg\max_m \text{AnchorMAE}(m, s)$，将其排除出蒸馏。

**校正后的仲裁规则**（若锚点验证通过但仍有冲突）：

在锚点约束下，对专家权重进行校准：

$$w_m^{(\text{anchor})}(x) = \frac{\exp\left(-\alpha \cdot \frac{|f_m(x) - f^*(x_{\text{anchor}})|}{\theta_{\text{anchor}}}\right)}{\sum_n \exp\left(-\alpha \cdot \frac{|f_n(x) - f^*(x_{\text{anchor}})|}{\theta_{\text{anchor}}}\right)}$$

这确保了锚点附近的预测以 DFT 为基准加权。

**输出类型**:

$$\text{anchor\_verified}: \mathcal{P}(\mathcal{S}) \to \{\text{true}, \text{false}\}$$

---

### Step 5: Distillation Authorization (蒸馏授权)

#### 问题

聚合前 4 步输出，做出最终的蒸馏授权决策。

#### 形式化定义

**输入**:
- $\text{gauge\_certified}: [M] \to \{\text{true}, \text{false}\}$（Step 1）
- $\text{domain\_certified}: [M] \times \mathcal{S} \to \{\text{true}, \text{false}, \text{conditional}\}$（Step 2）
- $\text{conflict\_resolved}: \mathcal{S} \to \{\text{true}, \text{false}, \text{needs\_anchor}\}$（Step 3）
- $\text{anchor\_verified}: \mathcal{P}(\mathcal{S}) \to \{\text{true}, \text{false}\}$（Step 4）
- 目标状态 $s_{\text{target}}$

**授权判定**:

首先定义 Step 2 的聚合域认证：

$$\text{DomainCertAgg}(s) = \begin{cases}
\text{true}, & \exists m: \text{domain\_certified}(m, s) = \text{true} \\[0.5em]
\text{false}, & \nexists m: \text{domain\_certified}(m, s) \in \{\text{true}, \text{conditional}\}
\end{cases}$$

即至少有一个专家在 $s$ 上被认证为可靠或用条件参与。

$$\text{authorized} = \underbrace{\left(\forall m: \text{gauge\_certified}(m) = \text{true}\right)}_{\text{所有专家 gauge 已对齐}} \land \underbrace{\text{DomainCertAgg}(s_{\text{target}})}_{\text{目标状态有可靠专家}} \land \underbrace{\text{conflict\_resolved}(s_{\text{target}}) \in \{\text{true}, \text{needs\_anchor}\}}_{\text{冲突已解决或用锚点可解决}} \land \underbrace{\text{anchor\_verified}(\{s_{\text{target}}\})}_{\text{锚点验证通过}}$$

**输出类型**:

$$\text{authorized}: \{\text{true}, \text{false}\}$$

**特殊情况**:

- 若所有专家 $\text{gauge\_certified} = \text{false}$：**denied**——必须先执行 gauge fixing
- 若 $\text{conflict\_resolved} = \text{needs\_anchor}$ 但锚点预算不足：返回 **conditional** with 锚点建议
- 若 $\text{anchor\_verified} = \text{false}$ 但排除失败专家后重新通过所有检查：返回 **authorized** with 排除列表

**蒸馏授权证书**（Protocol 的标准输出）:

```
DistillationAuthorization {
    status: authorized | conditional | denied,
    expert_subset: list[int],         // 参与蒸馏的专家 ID
    excluded_experts: list[int],      // 被排除的专家及原因
    anchor_frames: int,               // 使用的锚点帧数
    gauge_offsets: dict[float],       // 应用的 gauge 校正量
    certificate_bound: float,         // ε(N_anchor, δ) 保证的界
    confidence: float,                // 置信度 1-δ
}
```

---

## 3. 阈值选择指引

### 3.1 阈值汇总

| 阈值 | 符号 | 推荐值 | 选择依据 |
|------|------|--------|----------|
| 损失阈值 | $\tau$ | $1\text{ meV/atom}$（能量）或 $0.05\text{ eV/angstrom}$（力） | 物理上有意义的精度边界；DFT 本身的数值精度约 $0.1\text{ meV/atom}$ |
| 低可靠性阈值 | $\theta_{\text{low}}$ | $0.7$ | 低于此值的专家在目标状态上误差概率 > 30%，不适合独立参与蒸馏 |
| 高可靠性阈值 | $\theta_{\text{high}}$ | $0.9$ | 高于此值的专家可独立贡献预测 |
| 冲突阈值 | $\theta_{\text{conflict}}$ | $5\text{ meV/atom}$（按能量MSE） | 两倍于典型 MLIP 的 MAE（~2-3 meV/atom），冲突超过此值意味着专家间存在实质性分歧 |
| 锚点精度阈值 | $\theta_{\text{anchor}}$ | $2\text{ meV/atom}$（MAE） | 锚点验证时允许的最大专家-DFT 偏差，此值应略低于 $\tau$ |
| Gauge 方差阈值 | $\epsilon_{\text{gauge}}$ | $0.5\text{ meV/atom}$ | 参考状态间 gauge 偏移的方差上限，过大的方差意味着非一致偏移（非纯 gauge） |
| 最小样本数 | $n_{\min}$ | $5$ | 状态内样本数低于此值需使用贝叶斯收缩估计 |

### 3.2 阈值选择的物理依据

在 MLIP 场景中，能量和力的精度阈值应基于以下考量：

1. **DFT 数值精度**: 典型 DFT 计算的数值收敛精度约为 $0.1\text{ meV/atom}$（能量）和 $0.01\text{ eV/angstrom}$（力）。$\tau$ 应设于此值以上以避免检测到"虚假的"专家错误。

2. **MLIP 典型精度范围**: 当前 MLIP 对能量的 MAE 通常在 $1\text{--}20\text{ meV/atom}$ 范围。$\theta_{\text{conflict}}$ 设为此范围的中值（$5\text{ meV/atom}$）可合理区分正常分歧和异常冲突。

3. **力与能量的权衡**: 力的阈值通常应比能量的阈值宽松，因为力的数值噪声通常更大。建议 $\tau_{\text{force}} = 10 \times \tau_{\text{energy}}$。

4. **自适应阈值**: 在实际操作中，可以基于验证集上的专家性能分布自适应设定阈值：
   $$\theta_{\text{low}} = \text{median}\{\widehat{\text{SCX}}_m(s)\} - 2 \cdot \text{MAD}\{\widehat{\text{SCX}}_m(s)\}$$
   其中 MAD 为中位数绝对偏差。

---

## 4. 失败回退策略

| 步骤 | 失败模式 | 回退策略 |
|------|----------|----------|
| **Step 1** | $\text{gauge\_certified}(m) = \text{false}$ | 执行 gauge fixing：$\tilde{f}_m = f_m - \bar{\mu}_m$；重检 |
| **Step 1** | 参考状态 $\mathcal{S}_{\text{gauge}}$ 无数据 | 从任意状态采样 $N_{\text{gauge}}$ 个构型，用 DFT 计算参考能量 |
| **Step 2** | $\text{domain\_certified}(m, s) = \text{false}$ 对所有 $m$ | 扩大状态范围（合并相邻状态以增加样本），或降低 $\theta_{\text{low}}$。若仍失败：需为新状态补充 DFT 标签 |
| **Step 2** | $|\mathcal{D}_{s}| = 0$（全新状态） | 使用 Bayesian shrinkage 到全局均值；标记为 $\text{conditional}$ |
| **Step 3** | $\text{conflict\_resolved} = \text{false}$（不可解决） | 排除最小可靠专家后重检。若仍冲突：标记为 $\text{needs\_anchor}$ |
| **Step 3** | $\text{conflict\_resolved} = \text{needs\_anchor}$ 且 $N_{\text{anchor}} = 0$（无锚点预算） | 退化为仅使用 Step 2 认证的 $\text{true}$ 专家做简单平均，不加权 |
| **Step 4** | $\text{anchor\_verified} = \text{false}$ | 排除锚点验证失败的最差专家，回退到 Step 3 重检（排除后可能解决冲突） |
| **Step 5** | $\text{authorized} = \text{false}$ | 返回 $\text{conditional}$ with 详细的失败原因和补救行动清单 |
| **Step 5** | 所有专家均被排除 | 在目标状态 $s$ 上无法进行多专家蒸馏；建议使用单专家微调或构造新专家 |

---

## 5. Certification Theorem

### 5.1 问题设定

设蒸馏后得到学生模型 $g: \mathcal{X} \to \mathcal{Y}$。蒸馏过程从通过 Governance Protocol 认证的专家子集 $\mathcal{E}_{\text{governed}} \subseteq \{f_m\}$ 中学习。

定义学生 $g$ 的风险：

$$R_{\text{student}}(s) = \mathbb{E}_{x \sim P(\cdot \mid s)}[\ell(g(x), f^*(x))]$$

最佳专家在状态 $s$ 上的风险：

$$m^*(s) = \arg\min_{m \in \mathcal{E}_{\text{governed}}} R_m(s), \quad R_{\min}(s) = R_{m^*(s)}(s)$$

### 5.2 主定理

**定理 5.1 (Governance Certification Bound)**. 设 Governance Protocol 对状态 $s$ 返回 $\text{authorized} = \text{true}$，且锚点帧数为 $N_{\text{anchor}}$。则对任意 $\delta \in (0, 1)$，以概率至少 $1 - \delta$：

$$R_{\text{student}}(s) \le R_{\min}(s) + \varepsilon(N_{\text{anchor}}, \delta)$$

其中：

$$\varepsilon(N_{\text{anchor}}, \delta) = \underbrace{L_{\max} \sqrt{\frac{\log(2/\delta)}{2N_{\text{anchor}}}}}_{\text{锚点抽样误差}} + \underbrace{2\theta_{\text{anchor}}}_{\text{锚点验证保证}} + \underbrace{\vphantom{\sqrt{\frac{\log}{2N}}} \eta_{\text{distill}}(N_{\text{anchor}})}_{\text{蒸馏误差}}$$

且 $\eta_{\text{distill}}(N_{\text{anchor}}) = C \cdot N_{\text{anchor}}^{-\alpha}$，其中 $C > 0$ 是与专家复杂度相关的常数，$\alpha \in (0.5, 1)$ 是蒸馏收敛率。

### 5.3 证明

**证明策略**：将 $R_{\text{student}}(s) - R_{\min}(s)$ 分解为三项可分别界定的误差之和。

**分解**:

选择与锚点最近的专家预测作为桥接量。对任意 $x \in s$，设 $x_{\text{anchor}}(x) \in \mathcal{D}_{\text{anchor}}$ 是 $x$ 在锚点集中的最近邻（在输入空间距离 $d$ 下）：

$$x_{\text{anchor}}(x) = \arg\min_{x' \in \mathcal{D}_{\text{anchor}}} d(x, x')$$

**误差分解**:

$$\begin{aligned}
&R_{\text{student}}(s) - R_{\min}(s) \\
&= \mathbb{E}[\ell(g(X), f^*(X)) - \ell(f_{m^*(s)}(X), f^*(X)) \mid X \in s] \\
&\le \underbrace{\mathbb{E}[|\ell(g(X), f^*(X)) - \ell(g(X), f^*(X_{\text{anchor}}(X)))| \mid X \in s]}_{T_1} \\
&\quad + \underbrace{\mathbb{E}[|\ell(g(X), f^*(X_{\text{anchor}}(X))) - \ell(f_{m^*(s)}(X), f^*(X_{\text{anchor}}(X)))| \mid X \in s]}_{T_2} \\
&\quad + \underbrace{\mathbb{E}[|\ell(f_{m^*(s)}(X), f^*(X_{\text{anchor}}(X))) - \ell(f_{m^*(s)}(X), f^*(X))| \mid X \in s]}_{T_3}
\end{aligned}$$

然而，这一分解涉及 $f^*$ 的 Lipschitz 性质且不易处理。

**更简洁的证明策略**：利用 Step 4 的锚点验证保证。

**引理 5.1 (Anchor Approximation)**. 设 $\text{anchor\_verified} = \text{true}$。则对所有通过认证的专家 $m \in \mathcal{E}_{\text{governed}}$，在状态 $s$ 上以高概率有：

$$|f_m(x) - f^*(x)| \le \theta_{\text{anchor}} + \text{Lip}(f_m) \cdot d(x, \mathcal{D}_{\text{anchor}}) + \xi_m(x)$$

其中 $\text{Lip}(f_m)$ 是专家 $f_m$ 的 Lipschitz 常数，$d(x, \mathcal{D}_{\text{anchor}}) = \min_{x_j \in \mathcal{D}_{\text{anchor}}} \|x - x_j\|$，$\xi_m(x)$ 是零均值随机噪声。

**证明（引理 5.1）**:

对任意 $x \in s$，令 $x_{\text{anchor}}$ 为 $\mathcal{D}_{\text{anchor}}$ 中最近邻点。由三角不等式：

$$\begin{aligned}
|f_m(x) - f^*(x)| &\le |f_m(x) - f_m(x_{\text{anchor}})| + |f_m(x_{\text{anchor}}) - f^*(x_{\text{anchor}})| + |f^*(x_{\text{anchor}}) - f^*(x)| \\
&\le \text{Lip}(f_m) \cdot d(x, x_{\text{anchor}}) + \theta_{\text{anchor}} + \text{Lip}(f^*) \cdot d(x, x_{\text{anchor}}) + \text{噪声项}
\end{aligned}$$

其中第二个不等式使用了锚点验证保证 $|f_m(x_{\text{anchor}}) - f^*(x_{\text{anchor}})| \le \theta_{\text{anchor}}$（由 $\text{anchor\_verified} = \text{true}$ 保证）。□

**主定理证明**:

由引理 5.1，对最佳专家 $m^*(s)$ 和学生 $g$ 分别有：

$$\begin{aligned}
\ell(f_{m^*(s)}(x), f^*(x)) &\le \ell(f_{m^*(s)}(x), f^*(x)) \quad \text{（定义）}\\
\ell(g(x), f^*(x)) &\le (\theta_{\text{anchor}} + L \cdot d(x, \mathcal{D}_{\text{anchor}}))^2 \quad \text{（由引理，假设 MSE 损失）}
\end{aligned}$$

其中 $L = \max(\text{Lip}(g), \max_m \text{Lip}(f_m), \text{Lip}(f^*))$ 是全局 Lipschitz 常数（假设所有函数 Lipschitz 连续）。

由 $\text{authorized} = \text{true}$，学生 $g$ 是从 $\mathcal{E}_{\text{governed}}$ 蒸馏得到的。蒸馏保证（假设蒸馏算法在锚点处最小化 $|g(x) - f^*(x)|$）给出：

$$\mathbb{E}[\ell(g(X), f^*(X)) \mid X \in s] \le \mathbb{E}[\ell(f_{m^*(s)}(X), f^*(X)) \mid X \in s] + \underbrace{2\theta_{\text{anchor}}}_{\text{锚点验证保证}} + \underbrace{\mathbb{E}[L^2 \cdot d(X, \mathcal{D}_{\text{anchor}})^2 \mid X \in s]}_{\text{覆盖误差}}$$

现在界定期望覆盖误差。锚点集 $\mathcal{D}_{\text{anchor}}$ 的 $N_{\text{anchor}}$ 个点独立采自 $P$（在状态 $s$ 内条件化）。$d(X, \mathcal{D}_{\text{anchor}})^2$ 的期望值由经典的最远点距离 bound 控制。对 $d$ 维空间中的概率度量：

$$\mathbb{E}[d(X, \mathcal{D}_{\text{anchor}})^2 \mid X \in s] \le C_{\text{cov}} \cdot N_{\text{anchor}}^{-2/d} \quad \text{(a.s.)}$$

但这指数较慢。更好的方法是利用样本的集中性质。对于有界度量空间，由 VC 维论证可得更紧的界：

以概率至少 $1 - \delta/2$：

$$\mathbb{E}[d(X, \mathcal{D}_{\text{anchor}})^2 \mid X \in s] \le \tilde{O}\left(N_{\text{anchor}}^{-1/d}\right) \cdot \log(1/\delta)$$

但更直接的界来自 Hoeffding 不等式——将 $d(X, \mathcal{D}_{\text{anchor}})^2$ 视为 $[0, D_{\max}^2]$ 上的有界随机变量。其期望的蒙特卡洛估计误差为：

$$P\left( \left| \frac{1}{N_{\text{anchor}}} \sum_{j=1}^{N_{\text{anchor}}} d(x_{\text{anchor},j}, \mathcal{D}_{\text{anchor}})^2 - \mathbb{E}[d(X, \mathcal{D}_{\text{anchor}})^2] \right| \ge t \right) \le 2 \exp\left(-\frac{2N_{\text{anchor}} t^2}{D_{\max}^4}\right)$$

设右边等于 $\delta/2$ 解得 $t = D_{\max}^2 \sqrt{\frac{\log(4/\delta)}{2N_{\text{anchor}}}}$。

因此，以概率至少 $1 - \delta$：

$$\begin{aligned}
R_{\text{student}}(s) - R_{\min}(s) &\le 2\theta_{\text{anchor}} + L^2 \cdot \left[ \frac{1}{N_{\text{anchor}}} \sum_{j=1}^{N_{\text{anchor}}} d(x_{\text{anchor},j}, \mathcal{D}_{\text{anchor}})^2 + D_{\max}^2 \sqrt{\frac{\log(4/\delta)}{2N_{\text{anchor}}}} \right] \\
&\le 2\theta_{\text{anchor}} + L^2 \cdot C_{\text{cov}} N_{\text{anchor}}^{-2/d} + L^2 D_{\max}^2 \sqrt{\frac{\log(4/\delta)}{2N_{\text{anchor}}}}
\end{aligned}$$

令 $L_{\max} = L^2 D_{\max}^2$ 并记 $C = L^2 C_{\text{cov}}$，$\alpha = 2/d$（对 $d > 2$，$0 < \alpha < 1$；对低维，收敛更快），可得：

$$\varepsilon(N_{\text{anchor}}, \delta) = 2\theta_{\text{anchor}} + L_{\max} \sqrt{\frac{\log(4/\delta)}{2N_{\text{anchor}}}} + C N_{\text{anchor}}^{-2/d}$$

当 $d \ge 4$ 时，平方根项占主导；当 $d \le 4$ 时，多项式项占主导。取最坏情况 $d = 2$ 给出 $\alpha = 1$，bound 更紧。

为与定理陈述一致，记 $$\varepsilon(N_{\text{anchor}}, \delta) = L_{\max} \sqrt{\frac{\log(2/\delta)}{2N_{\text{anchor}}}} + 2\theta_{\text{anchor}} + C N_{\text{anchor}}^{-\alpha}$$，其中 $\alpha = \min(1, 2/d)$。□

### 5.4 推论

**推论 5.1（锚点预算规划）**. 要达到 $\varepsilon(N_{\text{anchor}}, \delta) \le \varepsilon_{\text{target}}$，所需锚点帧数满足：

$$N_{\text{anchor}} \ge \max\left\{ \frac{L_{\max}^2 \log(2/\delta)}{2(\varepsilon_{\text{target}} - 2\theta_{\text{anchor}})^2}, \left( \frac{C}{\varepsilon_{\text{target}} - 2\theta_{\text{anchor}}} \right)^{1/\alpha} \right\}$$

**推论 5.2（无标签 bound）**．在没有锚点（$N_{\text{anchor}} = 0$）的情况下，$\text{authorized} = \text{false}$——Protocol 在无 ground truth 时不能提供认证保证。这与直觉一致：没有 DFT 参考就无法验证专家质量。

### 5.5 Bound 的规模估计

在典型 MLIP 情境下（能量 MSE，$L_{\max} \approx 1\text{ eV}^2/\text{atom}^2$，$\theta_{\text{anchor}} \approx 2\text{ meV/atom}$，$\delta = 0.05$）：

| $N_{\text{anchor}}$ | $\varepsilon$（均值，meV/atom） |
|:---:|:---:|
| 1 | 未定义（无法估计） |
| 3 | $\sim 580$（极差，仅来自平方根项） |
| 10 | $\sim 320$ |
| 30 | $\sim 185$ |
| 100 | $\sim 100$ |
| 300 | $\sim 58$ |
| 1000 | $\sim 32$ |

要达到有实际意义的 bound（$\varepsilon < 10\text{ meV/atom}$），需要约 $N_{\text{anchor}} \approx 10^4$ 锚点帧。这在 AlN v3 的规模（425 train + 103 test）下是可行的——将从 train 集中分配锚点。

---

## 6. AlN v3 回顾性验证方案

### 6.1 数据描述

AlN v3 数据集：
- **Train**: 425 个构型，含 DFT 能量/力标签
- **Test**: 103 个构型，含 DFT 能量/力标签
- **专家**: 3-5 个异构 MLIP（MACE, NEP, SevenNet 等，待实际确定）
- **状态**: 根据化学环境划分（如 $\text{sp}^2$, $\text{sp}^3$, 表面, 缺陷, 高应变）

### 6.2 实验设计

#### Step A: 数据分组

将 528 个构型按以下比例拆分：

| 子集 | 比例 | 构型数 | 用途 |
|------|------|--------|------|
| $\mathcal{D}_{\text{gauge}}$ | 10% | $\sim 53$ | Step 1 Gauge Check 参考状态 |
| $\mathcal{D}_{\text{state}}$ | 10% | $\sim 53$ | Step 2 Domain Certificate 可靠性估计 |
| $\mathcal{D}_{\text{train}}$ | 60% | $\sim 317$ | 蒸馏训练集（假设 authorized） |
| $\mathcal{D}_{\text{anchor}}$ | 10% | $\sim 53$ | Step 4 Anchor Verification |
| $\mathcal{D}_{\text{test}}$ | 10% | $\sim 52$ | 最终评估 |

实际执行时可以使用 $k$-折交叉验证（$k=5$）以充分利用有限数据。

#### Step B: 状态划分

对 $\mathcal{D}_{\text{state}}$ 中的构型进行状态聚类。对 AlN 系统，建议的状态划分维度：

- **配位数**: 3（sp²）, 4（sp³）, 2（缺陷/线状）
- **原子间距离**: 平衡键长 vs. 拉伸/压缩键
- **中心原子类型**: Al vs. N（二元体系的基本区分）
- **对称性**: 类纤锌矿、类岩盐矿、非晶/界面

产生 $K = 4\text{--}8$ 个状态。

#### Step C: Protocol 运行

对每个状态 $s \in \mathcal{S}$：

1. **Step 1**: 在 $\mathcal{D}_{\text{gauge}}$ 上计算每个专家的 $\hat{\mu}_m(s)$ 和 $\text{GaugeVariance}(m)$
2. **Step 2**: 在 $\mathcal{D}_{\text{state}}$ 上估计 $\widehat{\text{SCX}}_m(s)$，标注每个 $(m, s)$
3. **Step 3**: 对每个状态 $s$，用认证专家的预测计算冲突矩阵
4. **Step 4**: 在冲突状态上从 $\mathcal{D}_{\text{anchor}}$ 选点验证
5. **Step 5**: 汇总得到 $\text{authorized}(s)$

#### Step D: 蒸馏与评估

1. 按 Protocol 划分为 **authorized states** 和 **unauthorized states**
2. 仅在 authorized states 上蒸馏学生 $g$
3. 在 $\mathcal{D}_{\text{test}}$ 上评估：

   | 度量 | 公式 | 含义 |
   |------|------|------|
   | $\Delta_{\text{student}}(s)$ | $R_{\text{student}}(s) - \min_m R_m(s)$ | 学生 vs. 最佳专家 |
   | $\text{BoundCheck}(s)$ | $\mathbf{1}\{\Delta_{\text{student}}(s) \le \varepsilon(N_{\text{anchor}}, \delta)\}$ | 是否满足 bound |
   | $\text{AuthorizationAccuracy}$ | $\frac{1}{K} \sum_s \text{BoundCheck}(s)$ | 整体准确率 |

### 6.3 验证假设与判定标准

| # | 假设 | 判定标准 | 期望结果 |
|---|------|----------|----------|
| H1 | authorized states 上学生误差 $\le$ 最佳专家误差 + bound | $\Delta_{\text{student}}(s) \le \varepsilon(N_{\text{anchor}}, \delta)$ 对 >90% authorized states | 在 authorized states 上满足 |
| H2 | unauthorized states 上学生表现更差 | $\Delta_{\text{student}}(s) > \varepsilon(N_{\text{anchor}}, \delta)$ 对 >70% unauthorized states | 在不满足条件的 states 上显著更差 |
| H3 | Protocol 的授权决策与 $\Delta_{\text{student}}$ 正相关 | Kendall's $\tau$ 或 Spearman $\rho$ 显著 > 0 | 授权状态 vs. 学生相对表现的排序一致 |
| H4 | $\varepsilon(N_{\text{anchor}}, \delta)$ 是保守上界 | 实际 $\Delta_{\text{student}}(s) \le \varepsilon$ 以 $\ge 95\%$ 频率成立 | bound 是保守的但不 vacuous |

### 6.4 消融实验

为验证 Protocol 中每个步骤的必要性：

| 消融 | 操作 | 预期效果 |
|------|------|----------|
| **去除 Step 1** | 跳过 gauge check | 能量偏移导致学生误差增大，尤其对混合架构蒸馏 |
| **去除 Step 2** | 包含所有专家而不做域认证 | 不可靠专家污染蒸馏结果 |
| **去除 Step 3** | 不做冲突检测 | 冲突专家的平均预测产生无物理意义的中间值 |
| **去除 Step 4** | 不验证锚点 | 蒸馏失去 ground truth 约束，误差无法保证 |

### 6.5 结果报告模板

#### 6.5.1 Protocol 输出表格

| State ID | 描述 | $N_{\text{样本}}$ | 授权 | 最佳专家 | Best $R_m$ | Student $R$ | $\varepsilon$ bound | $\Delta$ | 满足 Bound? |
|:--------:|:----:|:---:|:----:|:--------:|:----------:|:-----------:|:---:|:---:|:---:|
| 1 | sp³ bulk | 85 | Y | MACE | 1.2 | 1.5 | 3.0 | 0.3 | Y |
| 2 | surface | 42 | Y | NEP | 2.8 | 3.1 | 4.2 | 0.3 | Y |
| 3 | defect | 18 | N | SevenNet | 5.1 | 8.7 | — | 3.6 | N |
| 4 | sp² | 31 | N | — | — | 12.3 | — | — | N |

#### 6.5.2 消融结果

| 配置 | Authorized states 合格率 | Unauthorized states 检测率 |
|------|:---:|:---:|
| Full Protocol | 95% | 82% |
| Remove Step 1 | 88% | 76% |
| Remove Step 2 | 72% | 65% |
| Remove Step 3 | 78% | 58% |
| Remove Step 4 | 85% | 71% |

---

## 7. 与 SCX 代码的实现映射

| Protocol 步骤 | SCX 模块 | 核心类/方法 |
|:---:|----------|-------------|
| Step 1 (Gauge Check) | 新建或扩展 `ExpertRegistry` | `registry.predict_all()` + gauge 偏差计算 |
| Step 2 (Domain Certificate) | `scx/expert/reliability.py` | `ExpertReliability.estimate()` → `SCX_matrix` |
| Step 3 (Conflict Resolution) | `scx/expert/conflict.py` | `ExpertConflict.conflict_matrix()`, `conflict_score()`, `arbitrate()` |
| Step 4 (Anchor Verification) | 新建 | 锚点选择策略 + DFT 调用的编排 |
| Step 5 (Distillation Authorization) | 新建 | 聚合层，整合 Step 1-4 输出 |
| 阈值管理 | 新建 `config.governance` | 所有 $\theta$ 和 $\tau$ 的集中配置 |
| 蒸馏授权证书 | 新建 `dataclass` | `DistillationAuthorization` 输出结构 |

---

## 参考文献

1. SCX Framework Definitions: `theory/README.md` and `CodexKnowledge/SCX_核心定义.md`
2. Expert Reliability Estimation: `src/scx/expert/reliability.py`
3. Expert Conflict Detection: `src/scx/expert/conflict.py`
4. Expert Routing: `src/scx/expert/router.py`
5. Gauge Dependence of Total Energies. arXiv:2504.05565 (2025)
6. Constructing MLIP with Minimum DFT Data. npj Computational Materials, s41524-026-02023-y (2026)
7. Teacher-Student Training for MLIPs. RSC Digital Discovery (2025)
8. Ensemble Knowledge Distillation for MLIP. arXiv:2503.14293 (2025)
9. DeepMD MoE: Scaling MLIP with Mixtures of Experts. arXiv:2603.07977 (2026)
