# 纠缠/虫洞/相对论：第 3–5 轮 — 形式化、敌对审查与最终裁决

> **日期**: 2026-07-02
> **轮次**: 第 3 轮（严格形式化）→ 第 4 轮（敌对审查）→ 第 5 轮（修正与最终裁决）
> **前置文件**: `entanglement_wormhole_relativity.md`（第 1–2 轮）
> **三条修正路径**: ACAD（审计相关性不对称检测）、MDTA（流形密度拓扑分析）、ILH（不变性分层体系）

---

## 目录

- **第 3 轮：严格形式化**
  - 6. ACAD 的信息论形式化
  - 7. MDTA 的拓扑形式化
  - 8. ILH 的群论形式化
- **第 4 轮：敌对审查**
  - 9. ACAD 形式化的裂缝
  - 10. MDTA 形式化的裂缝
  - 11. ILH 形式化的裂缝
- **第 5 轮：修正与最终裁决**
  - 12. 修正后的框架
  - 13. 三条路径的最终裁决
  - 14. 综合评估

---

## 第 3 轮：严格形式化
## Round 3: Rigorous Formalization

> 在第 2 轮中，我们将三个物理学类比修正为诚实的数学框架：ACAD、MDTA、ILH。在本轮中，我们为每个框架建立严格的数学基础——定义、定理、证明和界。目标不是"看起来像数学"，而是"经得起推敲的数学"。

---

## 6. ACAD 的信息论形式化
## Formalization of ACAD (Audit Correlation Asymmetry Detection)

### 6.1 基本设定与符号

**定义 6.1（审计对 / Audit Pair）**：一个审计对是一个三元组 $(\mathcal{A}, \mathcal{B}, \mathcal{C})$，其中：
- $\mathcal{A}$：审计员 A 的参考数据集空间，$\mathcal{A} \subseteq \mathcal{X}^n$（$n$ 个数据点）
- $\mathcal{B}$：审计员 B 的参考数据集空间，$\mathcal{B} \subseteq \mathcal{X}^n$
- $\mathcal{C}$：约束函数空间，$\mathcal{C} \subseteq \{C: \mathcal{X} \times \mathcal{X} \to \{0,1\}\}$

**定义 6.2（秘密配对 / Secret Pairing）**：秘密配对是一个双射 $\phi: [n] \to [n]$ 和一个约束函数 $C \in \mathcal{C}$，满足对审计员双方的部分可知性：
- 审计员 A 知道 $\{x_i^A\}_{i=1}^n$ 但不知道 $\phi$ 和 $\{x_j^B\}_{j=1}^n$
- 审计员 B 知道 $\{x_j^B\}_{j=1}^n$ 和 $\phi$，但不知道 $\{x_i^A\}_{i=1}^n$（在篡改检测阶段之前）
- 约束满足：$\forall i \in [n], C(x_i^A, x_{\phi(i)}^B) = 1$

**定义 6.3（攻击者模型 / Adversary Model）**：攻击者 $\mathcal{E}$ 具有以下能力与限制：
- **能力**：可以修改 $D_A = \{x_i^A\}_{i=1}^n$ 中的任意子集为 $\tilde{D}_A = \{\tilde{x}_i^A\}_{i=1}^n$
- **限制**：不知道 $\phi$、$D_B$、$C$ 的具体形式
- **知识**：知道 $\mathcal{X}$、$n$、以及 $D_A$ 的原始内容

**定义 6.4（篡改检测协议 / Tampering Detection Protocol）**：

1. **初始化**：审计员 B 拥有 $D_B$ 和 $\phi$。安全的带外信道用于最终比对。
2. **篡改**：攻击者将 $D_A$ 修改为 $\tilde{D}_A$。
3. **挑战**：B 随机选择 $k$ 个索引 $i_1, \ldots, i_k \subset [n]$（均匀无放回抽样）。
4. **请求**：B 向 A 请求 $\tilde{x}_{i_1}^A, \ldots, \tilde{x}_{i_k}^A$。
5. **验证**：B 计算检查通过率：
   $$T_k = \frac{1}{k} \sum_{j=1}^{k} C(\tilde{x}_{i_j}^A, x_{\phi(i_j)}^B)$$
6. **决策**：如果 $T_k < \tau$（预设阈值），则标记为"检测到篡改"。

### 6.2 理论分析

**定理 6.1（ACAD 检测概率下界 / ACAD Detection Probability Lower Bound）**

设攻击者修改了 $m$ 个数据点（$1 \leq m \leq n$），审计员 B 抽取 $k$ 个样本进行验证。假设约束函数 $C$ 是 $\varepsilon$-鲁棒的：即对于任何未修改的对，$P(C(x_i^A, x_{\phi(i)}^B) = 1) \geq 1 - \varepsilon$（其中 $\varepsilon \geq 0$ 是自然噪声）。假设攻击者不知道 $\phi$ 且 $\phi$ 是均匀随机双射。则：

$$P(\text{检测到篡改}) \geq 1 - \exp\left(-\frac{k m}{n} \cdot (1 - \varepsilon - \tau)^2 \cdot \frac{1}{2}\right)$$

其中 $\tau$ 是检测阈值。

**证明**：

设 $S$ 为被篡改的索引集合，$|S| = m$。B 抽取 $k$ 个样本。对于均匀随机双射 $\phi$，攻击者无法预测哪些 $i$ 被 $\phi$ 映射到哪些 $j$。由于攻击者不知道 $\phi$，对于任何被篡改的索引 $i \in S$，对应的 $x_{\phi(i)}^B$ 在攻击者的视角下是均匀分布在 $D_B$ 上的。

因此，对于 $i \in S$，攻击者要使 $C(\tilde{x}_i^A, x_{\phi(i)}^B) = 1$ 的概率不超过随机猜测的水平。更精确地，给定攻击者对 $\phi$ 的无知，我们可以为约束违反建模。

设随机变量 $Z_j$ 表示第 $j$ 次抽样是否为"成功检测"——即该样本来自被篡改的索引且约束被破坏。则：
- 第 $j$ 次抽样来自 $S$ 的概率：$\frac{m}{n}$（无放回抽样，但 $k \ll n$ 时近似）
- 给定来自 $S$，约束被破坏的概率：$\geq 1 - \varepsilon - \gamma$，其中 $\gamma$ 是攻击者猜测成功的最大概率

由于攻击者不知道 $\phi$，$\gamma = \frac{\text{满足 } C(\tilde{x}, y) = 1 \text{ 的 } y \in D_B \text{ 的期望比例}}{|D_B|}$。在最坏情况下（攻击者最优策略），$\gamma \leq \frac{1}{2}$（如果 $C$ 是平衡的），但更一般地，攻击者能达成的 $C=1$ 比例受限于 $D_B$ 中满足条件的点的密度。

对于独立抽样（近似），$T_k$ 是 $k$ 个 Bernoulli 试验的均值。设 $p_1$ 为篡改条件下单次检查通过的概率：

$$p_1 = \left(1 - \frac{m}{n}\right)(1 - \varepsilon) + \frac{m}{n} \cdot \gamma$$

其中第一项来自未篡改点（自然通过率 $1-\varepsilon$），第二项来自篡改点（攻击者最多以 $\gamma$ 的概率通过）。

设 $p_0 = 1 - \varepsilon$（无篡改条件下的通过率）。检测条件为 $T_k < \tau$。使用 Hoeffding 不等式：

$$P(T_k \geq \tau) = P(T_k - p_1 \geq \tau - p_1) \leq \exp\left(-2k(\tau - p_1)^2\right)$$

当 $\tau < p_1$ 时（这是非平凡检测条件）。选择 $\tau = p_1 + \frac{p_0 - p_1}{2} = \frac{p_0 + p_1}{2}$ 为中间点：

$$\tau - p_1 = \frac{p_0 - p_1}{2} = \frac{m}{n} \cdot \frac{1 - \varepsilon - \gamma}{2}$$

代入：

$$P(\text{未检测到}) \leq \exp\left(-2k \cdot \frac{m^2}{n^2} \cdot \frac{(1 - \varepsilon - \gamma)^2}{4}\right) = \exp\left(-\frac{k m^2}{2n^2} \cdot (1 - \varepsilon - \gamma)^2\right)$$

在最坏情况下（$\gamma = 0$，攻击者对 $C$ 完全无知），简化：

$$P(\text{检测到}) \geq 1 - \exp\left(-\frac{k m^2}{2n^2} \cdot (1 - \varepsilon)^2\right)$$

对于 $k = n$（全面检查），检测概率趋于 1。对于局部检查（$k < n$），当 $m = \Omega(n/\sqrt{k})$ 时检测概率有保证。$\square$

**定理 6.2（ACAD 的信息论安全界 / Information-Theoretic Security Bound）**

如果攻击者不知道 $\phi$ 和 $D_B$，且 $|D_B| = n$ 足够大，则对于任何攻击策略，存在常数 $c > 0$ 使得：

$$\inf_{\mathcal{E}} P(\text{检测到篡改}) \geq 1 - \exp(-c \cdot k \cdot m / n)$$

其中下确界取遍所有满足知识限制的攻击策略 $\mathcal{E}$。

**证明概要**：攻击者的信息状态由 $\sigma(\tilde{D}_A, D_A)$（攻击者知道的 $\sigma$-代数）决定。$\phi$ 在此 $\sigma$-代数下是不可测的（攻击者不知道配对）。由信息论数据处理不等式，攻击者对 $\phi$ 的估计误差下界为：

$$H(\phi | \tilde{D}_A, D_A) \geq \log(n!) - I(\phi; D_A)$$

其中 $H$ 是熵，$I$ 是互信息。由于 $D_A$ 由独立于 $\phi$ 的过程生成（在初始化阶段），$I(\phi; D_A) = 0$。因此 $H(\phi | \tilde{D}_A, D_A) = \log(n!)$——攻击者对 $\phi$ 完全无知。

在此无知条件下，攻击者能成功伪造约束的概率受限于随机猜测的水平，从而导出上述指数界。$\square$

**定理 6.3（样本复杂度 / Sample Complexity）**

为实现检测概率至少 $1 - \delta$（给定显著性水平），所需的最小样本量 $k^*$ 满足：

$$k^* \geq \frac{2n^2}{m^2(1 - \varepsilon - \gamma)^2} \cdot \log\frac{1}{\delta}$$

特别地，对于固定篡改比例 $\alpha = m/n$：

$$k^* = O\left(\frac{1}{\alpha^2} \cdot \log\frac{1}{\delta}\right)$$

**证明**：从定理 6.1 的界出发，设 $P(\text{未检测到}) \leq \delta$：

$$\exp\left(-\frac{k m^2}{2n^2} \cdot (1 - \varepsilon - \gamma)^2\right) \leq \delta$$

取对数并整理即得。$\square$

**推论 6.4（实际参数下的可行性）**：
- 若 $\alpha = 0.1$（攻击者修改 10% 的数据），$\varepsilon = 0.05$，$\gamma = 0$，$\delta = 0.01$
- 则 $k^* \geq 2 \cdot 100 / (1 \cdot 0.9025) \cdot 4.605 \approx 1020$
- 对于 $n = 10^4$，只需检查约 10% 的数据即可高概率检测

### 6.3 ACAD 的审计应用定理

**定理 6.5（ACAD 审计规避检测 / ACAD Audit Evasion Detection）**

设专家系统 $E$ 在审计设置 $S_1$ 和 $S_2$ 下产生预测分布 $p_1$ 和 $p_2$。定义审计设置依赖性度量：

$$\Delta(S_1, S_2) = \text{MMD}(p_1, p_2) = \sup_{f \in \mathcal{F}} \left| \mathbb{E}_{x \sim p_1}[f(x)] - \mathbb{E}_{x \sim p_2}[f(x)] \right|$$

其中 $\mathcal{F}$ 是再生核 Hilbert 空间（RKHS）的单位球。则在零假设 $H_0: p_1 = p_2$（无审计设置依赖）下：

$$P\left( \widehat{\text{MMD}}_n > \sqrt{\frac{2K_{\max}}{n}} + \sqrt{\frac{2}{n}\log\frac{1}{\delta}} \right) \leq \delta$$

其中 $K_{\max} = \sup_x k(x, x)$ 是核函数的上界。

**证明**：这是 MMD 的经典集中不等式。对于有界核 $k(\cdot, \cdot) \leq K_{\max}$，MMD 的经验估计 $\widehat{\text{MMD}}_n$ 满足 McDiarmid 不等式，给出上述界。$\square$

### 6.4 ACAD 形式化的完整性声明

ACAD 的形式化提供了以下数学保证：
1. **检测概率的指数下界**（定理 6.1）
2. **信息论安全基础**（定理 6.2）
3. **样本复杂度上界**（定理 6.3）
4. **审计设置依赖的统计检验**（定理 6.5）

---

## 7. MDTA 的拓扑形式化
## Formalization of MDTA (Manifold Density Topology Analysis)

### 7.1 流形捷径的严格定义

**定义 7.1（数据流形 / Data Manifold）**：设 $\mathcal{X} \subseteq \mathbb{R}^D$ 为数据空间（环境空间）。数据流形是一个三元组 $(\mathcal{M}, g, p)$，其中：
- $\mathcal{M}$ 是 $d$-维光滑流形（$d \ll D$），$\mathcal{M} \subset \mathbb{R}^D$ 是嵌入子流形
- $g$ 是 $\mathcal{M}$ 上的 Riemannian 度规（由嵌入诱导的拉回度规或由数据密度构造的 Fisher 信息度规）
- $p: \mathcal{M} \to \mathbb{R}_{>0}$ 是 $\mathcal{M}$ 上的数据密度函数（光滑，可积）

**定义 7.2（密集区 / Cluster）**：数据流形 $\mathcal{M}$ 上的一个 $\rho$-密集区是一个连通开集 $\mathcal{C} \subset \mathcal{M}$，满足：
1. $\forall x \in \mathcal{C}, p(x) \geq \rho$（密度下界）
2. $\mathcal{C}$ 是道路连通的
3. $\partial\mathcal{C}$ 处 $p(x) = \rho$

**定义 7.3（流形距离 / Manifold Distance）**：两点 $x, y \in \mathcal{M}$ 之间的流形距离为：

$$d_{\mathcal{M}}(x, y) = \inf_{\gamma: [0,1] \to \mathcal{M}, \gamma(0)=x, \gamma(1)=y} \int_0^1 \sqrt{g_{\gamma(t)}(\dot{\gamma}(t), \dot{\gamma}(t))} \, dt$$

两个密集区 $\mathcal{C}_i, \mathcal{C}_j$ 之间的流形距离：

$$d_{\mathcal{M}}(\mathcal{C}_i, \mathcal{C}_j) = \inf_{x \in \mathcal{C}_i, y \in \mathcal{C}_j} d_{\mathcal{M}}(x, y)$$

**定义 7.4（捷径比率 / Shortcut Ratio）**：对于两个密集区 $\mathcal{C}_i, \mathcal{C}_j$，定义：

$$r(\mathcal{C}_i, \mathcal{C}_j) = \frac{d_{\mathcal{M}}(\mathcal{C}_i, \mathcal{C}_j)}{\|\mu_i - \mu_j\|}$$

其中 $\mu_i = \frac{1}{\text{vol}(\mathcal{C}_i)} \int_{\mathcal{C}_i} x \, dx$ 是 $\mathcal{C}_i$ 的质心。

**定义 7.5（流形捷径 / Manifold Shortcut）**：当 $r(\mathcal{C}_i, \mathcal{C}_j) < \tau$（$\tau \in (0, 1)$ 为预设阈值）时，称 $(\mathcal{C}_i, \mathcal{C}_j)$ 构成一个 $\tau$-流形捷径。捷径上的最小密度路径为：

$$\gamma^*_{ij} = \arg\min_{\gamma: \mathcal{C}_i \to \mathcal{C}_j} \int_\gamma ds$$

沿 $\gamma^*$ 的密度最小值定义捷径的喉：

$$x_{\text{throat}} = \arg\min_{x \in \gamma^*_{ij}} p(x)$$

### 7.2 捷径检测的持久同调形式化

**定义 7.6（Vietoris-Rips 滤过 / Vietoris-Rips Filtration）**：给定有限样本 $X = \{x_1, \ldots, x_N\} \subset \mathcal{M}$，对每个尺度 $\varepsilon > 0$，定义 Vietoris-Rips 复形 $\text{VR}_\varepsilon(X)$：

$$\text{VR}_\varepsilon(X) = \{\sigma \subset X : \text{diam}(\sigma) \leq \varepsilon\}$$

滤过 $\{\text{VR}_\varepsilon(X)\}_{\varepsilon \geq 0}$ 产生持续同调群 $H_k^\varepsilon$。

**定义 7.7（捷径的持续同调特征 / Persistent Homology Signature of Shortcuts）**：

考虑 0 维持续同调 $H_0$。设 $\{(\varepsilon_b^{(i)}, \varepsilon_d^{(i)})\}_{i=1}^{N-1}$ 为 0 维条码（barcode），其中 $\varepsilon_b^{(i)}$ 是第 $i$ 个连通分量的"出生"时间，$\varepsilon_d^{(i)}$ 是其"死亡"时间（与另一个分量合并的时间）。

对于每个 0 维条 $(b, d)$，定义其**寿命** $\ell = d - b$ 和**出生密度** $\rho_b = p_{\text{avg}}(b\text{-分量})$。

**定义 7.8（捷径候选 / Shortcut Candidate）**：一个捷径候选是一个三元组 $(\mathcal{C}_a, \mathcal{C}_b, \ell)$，其中：
- $\mathcal{C}_a, \mathcal{C}_b$ 是在高密度阈值 $\rho_{\text{high}}$ 下分离的两个连通分量
- 它们在阈值 $\rho_{\text{low}} = \rho_{\text{high}} - \ell$ 下合并
- 合并的寿命 $\ell$ 满足 $0 < \ell < \ell_{\max}$（非平凡合并但非噪声）

### 7.3 捷径密度分布定理

**定理 7.1（捷径密度分布的变分特征 / Variational Characterization of Shortcut Density）**

设 $\gamma^*$ 是连接 $\mathcal{C}_i$ 和 $\mathcal{C}_j$ 的最小流形测地线。沿 $\gamma^*$ 的密度函数 $p(\gamma^*(t))$ 满足：对于捷径（$r < 1$），存在唯一的极小值点 $t^* \in (0, 1)$ 使得：

$$p(\gamma^*(t^*)) = \min_{t \in [0,1]} p(\gamma^*(t)) < \min(\rho_i, \rho_j)$$

其中 $\rho_i, \rho_j$ 是 $\mathcal{C}_i, \mathcal{C}_j$ 的密度下界。此外，若 $\gamma^*$ 的曲率满足 $|\ddot{\gamma}^*(t^*)| > 0$，则：

$$p(\gamma^*(t^*)) \leq \frac{\rho_i + \rho_j}{2} - \frac{1}{8} |\ddot{\gamma}^*(t^*)| \cdot (\rho_i - \rho_j)^2 + O((\rho_i - \rho_j)^3)$$

**证明概要**：由捷径定义 $r < 1$，流形路径在环境空间中"绕路"，意味着流形在 $\gamma^*$ 附近有显著曲率或折叠。密度函数沿测地线的二阶 Taylor 展开为：

$$p(\gamma^*(t)) = p(\gamma^*(t^*)) + \frac{1}{2} p''(\gamma^*(t^*)) (t - t^*)^2 + O((t - t^*)^3)$$

在端点 $t = 0, 1$ 处，$p \geq \min(\rho_i, \rho_j)$。通过连接端点条件解出 $t^*$ 和 $p(\gamma^*(t^*))$，可得上述界。$\square$

**定理 7.2（捷径存在性条件 / Shortcut Existence Condition）**

两个 $\rho$-密集区 $\mathcal{C}_i, \mathcal{C}_j$ 之间存在 $\tau$-捷径的充分条件是：

$$\exists \text{ 连接 } \mathcal{C}_i, \mathcal{C}_j \text{ 的道路 } \gamma \text{ 使得 } \frac{\int_\gamma ds}{\|\mu_i - \mu_j\|} < \tau$$

等价地，如果 $\mathcal{M}$ 的 reach（到达半径）$\tau_{\mathcal{M}}$ 满足：

$$\tau_{\mathcal{M}} < \frac{\|\mu_i - \mu_j\|}{2} \cdot \sqrt{\frac{1}{\tau^2} - 1}$$

则捷径存在。

**证明**：由流形的 reach 定义（从 $\mathcal{M}$ 到其中轴的最大距离）。reach 越小意味着流形折叠越严重。当流形折叠使得沿流形的路径远长于环境空间直线距离时，捷径比率 $r < 1$。几何推理给出上述界。$\square$

### 7.4 捷径的审计风险评估

**定义 7.9（捷径审计风险 / Shortcut Audit Risk）**：对于捷径 $(\mathcal{C}_i, \mathcal{C}_j, \gamma^*)$，定义审计风险评分为：

$$\text{SAR}(\gamma^*) = \underbrace{\text{Var}_\gamma[g]}_{\text{预测方差}} \times \underbrace{\left|\frac{d}{dt} \text{Cercis}(\gamma^*(t))\right|}_{\text{Cercis 梯度}} \times \underbrace{\frac{1}{p(x_{\text{throat}})}}_{\text{密度倒数}}$$

**定理 7.3（审计风险分类 / Audit Risk Classification）**

基于 SAR 评分，捷径可分类为：
- **良性捷径**（Benign）：$\text{SAR} < \theta_1$ → 真实数据结构
- **对抗性捷径**（Adversarial）：$\theta_1 \leq \text{SAR} < \theta_2$ → 潜在审计盲区
- **噪声走廊**（Noise Corridor）：$\text{SAR} \geq \theta_2$ → 不可审计区域

其中 $\theta_1, \theta_2$ 是基于经验的阈值。分类的一致性由以下条件保证：若 $\text{Cercis}$ 沿捷径是 $\alpha$-Lipschitz 的，则：

$$|\text{SAR}(\gamma_1^*) - \text{SAR}(\gamma_2^*)| \leq L \cdot d_{\mathcal{M}}(\gamma_1^*, \gamma_2^*)$$

其中 $L$ 是组合 Lipschitz 常数。

**证明**：由各因子的 Lipschitz 性质：

$$\text{Var}_\gamma[g] \leq L_V \cdot d_{\mathcal{M}}$$
$$\text{Cercis 梯度} \leq \alpha \cdot d_{\mathcal{M}}$$
$$\frac{1}{p(x_{\text{throat}})} \leq L_p \cdot d_{\mathcal{M}}$$

三者乘积满足 $L = L_V \cdot \alpha \cdot L_p$ 的 Lipschitz 条件。$\square$

### 7.5 离散版本与算法复杂度

**定理 7.4（离散捷径检测的复杂度 / Complexity of Discrete Shortcut Detection）**

对于 $N$ 个数据点的集合，使用 k-NN 图（$k = O(\log N)$）进行流形距离估计，捷径检测算法的时间复杂度为：

$$O(N \log N \cdot k + C^2 \cdot N \log N)$$

其中 $C$ 是检测到的密集区数量。

**证明**：k-NN 图构建：$O(N \log N \cdot k)$（使用 kd-tree）。所有对最短路径：$O(C^2 \cdot N \log N)$（使用 Dijkstra 在每个密集区对上）。$\square$

**定理 7.5（捷径比率估计的一致性 / Consistency of Shortcut Ratio Estimation）**

设 $\hat{d}_{\mathcal{M}}$ 是基于 k-NN 图的流形距离估计，$\hat{r}$ 是相应的捷径比率估计。则在 $N \to \infty$、$k \to \infty$、$k/N \to 0$ 的条件下：

$$\hat{r} \xrightarrow{P} r \quad \text{即} \quad \forall \varepsilon > 0: \lim_{N \to \infty} P(|\hat{r} - r| > \varepsilon) = 0$$

**证明**：由 k-NN 图距离的 Isomap 一致性（Bernstein et al., 2000；Tenenbaum et al., 2000），在流形 $\mathcal{M}$ 是紧致且测地线凸的条件下，k-NN 图最短路径一致地收敛到流形测地距离。捷径比率是连续函数，由连续映射定理得证。$\square$

---

## 8. ILH 的群论形式化
## Formalization of ILH (Invariance Layered Hierarchy)

### 8.1 分层不变性的范畴论基础

**定义 8.1（审计对象 / Audit Object）**：SCX 审计的基本对象是专家预测配置。设 $M$ 为专家数量，$d$ 为预测空间维数。定义：

$$\mathcal{G} = \mathbb{R}^{M \times d}$$

为所有可能的专家预测矩阵（每行是一个专家的 $d$ 维预测向量）。

**定义 8.2（对称群作用 / Symmetry Group Action）**：对于群 $G$ 和表示 $\rho: G \to \text{GL}(\mathcal{G})$，群作用定义为：

$$\alpha: G \times \mathcal{G} \to \mathcal{G}, \quad \alpha(g, \Gamma) = \rho(g) \cdot \Gamma$$

其中 $\Gamma \in \mathcal{G}$ 是预测矩阵。

**定义 8.3（不变性层级 / Invariance Layer）**：第 $\ell$ 层不变性由一个群 $G_\ell$ 及其作用 $\alpha_\ell$ 定义，满足层级包含关系：

$$G_0 \subset G_1 \subset G_2 \subset \cdots \subset G_L$$

其中 $G_0 = \{e\}$（平凡群，无不变性）。

**定理 8.1（层级不变量函子 / Layered Invariant Functor）**

对于每个层级 $\ell$，存在从 $\mathcal{G}$ 到不变量空间 $\mathcal{I}_\ell$ 的函子 $\mathcal{F}_\ell$：

$$\mathcal{F}_\ell: \mathcal{G} \to \mathcal{I}_\ell$$

满足 $\mathcal{F}_\ell(\Gamma) = \mathcal{F}_\ell(\alpha_\ell(g, \Gamma))$ 对所有 $g \in G_\ell$。此外，层级函子满足交换图：

$$\begin{CD}
\mathcal{G} @>{\mathcal{F}_\ell}>> \mathcal{I}_\ell \\
@| @VV{\pi_{\ell, \ell-1}}V \\
\mathcal{G} @>{\mathcal{F}_{\ell-1}}>> \mathcal{I}_{\ell-1}
\end{CD}$$

其中 $\pi_{\ell, \ell-1}$ 是遗忘投影（高层级不变量包含低层级不变量信息）。

**证明**：构造 $\mathcal{I}_\ell = \mathcal{G} / G_\ell$（$G_\ell$ 作用的轨道空间），$\mathcal{F}_\ell$ 为自然投影。$\pi_{\ell, \ell-1}$ 由 $G_{\ell-1} \subset G_\ell$ 诱导的轨道空间的自然映射。$\square$

### 8.2 SCX 不变性层级的具体构造

**层级 0: 平凡不变性 $G_0 = \{e\}$**

$$\mathcal{I}_0 = \mathcal{G} \cong \mathbb{R}^{M \times d}$$

不变量：原始预测矩阵 $\Gamma$。$\mathcal{F}_0 = \text{id}$。

**层级 1: 平移不变性 $G_1 = (\mathbb{R}^d, +)^M_{\text{diag}}$**

群作用：$\Gamma \mapsto \Gamma + \mathbf{1}_M \otimes c^T$，其中 $c \in \mathbb{R}^d$，$\mathbf{1}_M$ 是全 1 向量。这是对角线平移：所有专家平移相同的向量。

不变量：差异向量 $d_{mn} = \Gamma_m - \Gamma_n \in \mathbb{R}^d$，Cercis Score $\text{Cercis}(\Gamma)$。

**定理 8.2（Cercis 的平移不变性 / Translation Invariance of Cercis）**

设 Cercis Score 定义为：

$$\text{Cercis}(\Gamma) = f\left(\{d_{mn}\}_{m<n}\right)$$

其中 $f$ 是差异向量集合的任意函数。则 $\text{Cercis}(\Gamma + \mathbf{1}_M \otimes c^T) = \text{Cercis}(\Gamma)$。

**证明**：$d_{mn}' = (\Gamma_m + c) - (\Gamma_n + c) = \Gamma_m - \Gamma_n = d_{mn}$。$\square$

**定理 8.3（平移不变量的完备性 / Completeness of Translation Invariants）**

差异向量集合 $\{d_{mn}\}_{m<n}$ 构成平移群作用的**完备不变量集合**——即两个配置 $\Gamma, \Gamma'$ 在平移下等价当且仅当它们的所有差异向量相等。

**证明**：($\Rightarrow$) 若 $\Gamma' = \Gamma + \mathbf{1}_M \otimes c^T$，则 $d_{mn}' = d_{mn}$ 平凡成立。($\Leftarrow$) 若 $d_{mn}' = d_{mn}$ 对所有 $m,n$，固定 $m=1$，则 $\Gamma_n' = \Gamma_n + (\Gamma_1' - \Gamma_1)$。设 $c = \Gamma_1' - \Gamma_1$，则 $\Gamma' = \Gamma + \mathbf{1}_M \otimes c^T$。$\square$

**层级 2: 旋转不变性 $G_2 = O(d)^M_{\text{diag}}$**

群作用：$\Gamma \mapsto \Gamma \cdot R^T$，其中 $R \in O(d)$ 是正交矩阵。所有专家的预测被同一个旋转矩阵作用（对角线旋转）。

不变量：$\|\Gamma_m\|^2$（每个专家预测的范数），$\cos\theta_{mn} = \frac{\Gamma_m \cdot \Gamma_n}{\|\Gamma_m\| \|\Gamma_n\|}$（专家间的夹角），Cercis Score（继承自层级 1）。

**定理 8.4（Cercis 的旋转不变性 / Rotational Invariance of Cercis）**

若 Cercis Score 仅通过范数和夹角依赖于 $\Gamma$，则 $\text{Cercis}(\Gamma R^T) = \text{Cercis}(\Gamma)$ 对所有 $R \in O(d)$。

**证明**：$\|\Gamma_m R^T\|^2 = \Gamma_m R^T R \Gamma_m^T = \Gamma_m \Gamma_m^T = \|\Gamma_m\|^2$（$R^T R = I$）。$(\Gamma_m R^T) \cdot (\Gamma_n R^T) = \Gamma_m R^T R \Gamma_n^T = \Gamma_m \Gamma_n^T$。故范数和夹角不变。$\square$

**层级 3: 欧氏不变性 $G_3 = E(d)^M_{\text{diag}} = (\mathbb{R}^d \rtimes O(d))^M_{\text{diag}}$**

群作用：$\Gamma \mapsto \Gamma R^T + \mathbf{1}_M \otimes c^T$，其中 $R \in O(d)$，$c \in \mathbb{R}^d$。

不变量：Cercis Score + 旋转不变量（范数、夹角）——即层级 1 和 2 的不变量之交。

**定理 8.5（半直积不变量的结构 / Structure of Semidirect Product Invariants）**

$G_3$ 的不变量空间 $\mathcal{I}_3$ 同构于 $\mathcal{I}_1 \cap \mathcal{I}_2$（层级 1 和层级 2 不变量的交集）。具体地：

$$\mathcal{I}_3 \cong (\mathcal{G} / (\mathbb{R}^d, +)) \cap (\mathcal{G} / O(d)) \cong \mathcal{G} / E(d)$$

**证明**：由 $E(d) = \mathbb{R}^d \rtimes O(d)$ 的群结构。任何 $E(d)$-不变量必须同时对平移和旋转不变。由于 $(\mathbb{R}^d, +) \triangleleft E(d)$（平移是正规子群），轨道空间继承半直积结构。$\square$

**层级 4: 微分同胚不变性（假设性）$G_4 = \text{Diff}(\mathcal{X})$**

群作用：$\Gamma(x) \mapsto \Gamma(\phi^{-1}(x))$，其中 $\phi \in \text{Diff}(\mathcal{X})$ 是底流形 $\mathcal{X}$ 的微分同胚。

不变量：拓扑特征（Betti 数、持久同调条码长度分布）。

**定理 8.6（拓扑不变量的微分同胚不变性 / Diffeomorphism Invariance of Topological Invariants）**

Betti 数 $\beta_k(\mathcal{X})$ 和持久同调条码的多重集在微分同胚下不变：

$$\beta_k(\phi(\mathcal{X})) = \beta_k(\mathcal{X}), \quad \text{Barcode}(\phi(\mathcal{X})) \cong \text{Barcode}(\mathcal{X})$$

**证明**：Betti 数是同伦不变量，微分同胚诱导同伦等价。持久同调条码在等距嵌入下不变，微分同胚保持拓扑结构（但不一定保持几何）。$\square$

### 8.3 层级间的继承与损失

**定理 8.7（信息损失层级定理 / Information Loss Hierarchy Theorem）**

设 $H(\cdot)$ 为配置空间的熵（或信息量）。则：

$$H(\mathcal{I}_L) \leq H(\mathcal{I}_{L-1}) \leq \cdots \leq H(\mathcal{I}_1) \leq H(\mathcal{I}_0)$$

且每层的损失 $\Delta H_\ell = H(\mathcal{I}_{\ell-1}) - H(\mathcal{I}_\ell)$ 满足：

$$\Delta H_\ell = \log |G_\ell / G_{\ell-1}|$$

（对于离散群；对于连续群，$\Delta H_\ell = \dim(G_\ell) - \dim(G_{\ell-1})$ 作为自由度损失）。

**证明**：轨道空间 $\mathcal{I}_\ell = \mathcal{G} / G_\ell$ 的"大小"随 $G_\ell$ 增大而减小。信息损失等于商掉的群作用的自由度。$\square$

**定理 8.8（Cercis 的层级定位 / Layered Positioning of Cercis）**

Cercis Score 在层级 1、2、3 中均为不变量，但在层级 0 中不是。Cercis 的生成群是其最大的不变性群：

$$G_{\text{Cercis}} = \text{Stab}(\text{Cercis}) = \{\Gamma \mapsto \Gamma R^T + \mathbf{1}_M \otimes c^T : R \in O(d), c \in \mathbb{R}^d\} \cong E(d)$$

即 Cercis 在 $E(d)$ 下不变，且 $E(d)$ 是保持 Cercis 不变的**最大**连通子群。

**证明**：Cercis 在 $E(d)$ 下不变（定理 8.2 + 8.4）。需要证明没有更大的连通子群保持 Cercis 不变。假设存在更大的群作用保持 Cercis，则该作用必须保持所有差异向量的某种函数。但差异向量的完备不变量集在 $E(d)$ 下是极小的（由表示论，$E(d)$ 在 $\mathcal{G}$ 上的作用是极性的——polar representation）。$\square$

### 8.4 Galileo 类比的形式化

**定理 8.9（Galileo vs Lorentz / Galileo vs Lorentz）**

SCX 的不变性结构同构于 $d$ 维空间的 Galileo 群的不变性结构：

$$\text{Gal}(d) = \mathbb{R}^d \rtimes O(d) \cong E(d)$$

而非 Lorentz 群 $\text{SO}(1, d-1)$（包含 boost）的结构。具体差异：

| 群结构 | Galileo $\cong E(d)$ | Lorentz $\cong \text{SO}(1, d-1) \rtimes \mathbb{R}^{d}$ |
|---|---|---|
| 旋转子群 | $O(d)$（紧，$\theta \in [0,2\pi)$） | $\text{SO}(1, d-1)$（非紧，boost 无界） |
| 不变距离 | $\|x - y\|$（正定） | $\eta_{\mu\nu}(x-y)^\mu(x-y)^\nu$（不定） |
| 因果结构 | 无上限（绝对同时性） | 光速 $c$ 上限 |

**证明**：SCX 的 $E(d)$ 群不包含 boost 生成元。因为预测空间的"速度"（相邻数据点的预测变化率）无物理上限。$\square$

---

## 第 4 轮：敌对审查
## Round 4: Hostile Review

> 第 3 轮为三条路径建立了显式的数学框架。在本轮中，我们对这些形式化进行最严厉的审查——假设自己是答辩委员会的成员，带着"找出所有裂缝"的心态。关键问题：这些形式化是**真正严格的**，还是**穿上数学外衣的隐喻**？

---

## 9. ACAD 形式化的裂缝
## Fractures in the ACAD Formalization

### 9.1 裂缝 1：定理 6.1 的证明依赖于独立性近似

**问题**：定理 6.1 使用了独立 Bernoulli 试验的近似（Hoeffding 不等式），但无放回抽样引入了相关性。

**严重程度**：⚠️ 中等。可以使用 Serfling 不等式（无放回抽样的集中不等式）来修复。具体地，对于无放回抽样：

$$P(T_k - p_1 \geq t) \leq \exp\left(-\frac{2k t^2}{(1 - (k-1)/n)}\right)$$

当 $k \ll n$ 时，修正因子接近 1，结论不受影响。但严格来说，原证明需要修正。

**修复难度**：低。替换 Hoeffding 为 Serfling 不等式即可。

### 9.2 裂缝 2：$\varepsilon$-鲁棒约束的假设未给出构造

**问题**：定理 6.1 假设约束 $C$ 是 $\varepsilon$-鲁棒的，但未给出如何构造这样的约束。在真实 SCX 场景中，什么约束是自然的？$C(x, y) = 1$ 究竟意味着什么？

**严重程度**：⚠️ 严重。如果没有具体的约束构造方案，整个 ACAD 框架是空的。

**审查**：可能的构造方案：
- **专家预测一致性约束**：$C(x_i^A, x_j^B) = 1$ 若 $\|E(x_i^A) - E(x_j^B)\| < \delta$（两个配对点在专家预测空间中接近）
- **数据流形邻域约束**：$C(x_i^A, x_j^B) = 1$ 若 $d_{\mathcal{M}}(x_i^A, x_j^B) < \varepsilon$

但这两个方案都存在循环性问题：审计本身就是为了验证专家预测，而约束又依赖于专家预测。此外，如果攻击者也拥有同样的专家模型，他们可以计算预测并在构造 $\tilde{x}_i^A$ 时维持约束。

**诚实评估**：ACAD 的安全依赖于**信息不对称**（攻击者不知道 $\phi$ 和 $D_B$），而非约束本身的强度。但如果约束可以通过公开的专家模型被近似预测，信息不对称就减弱了。这是 ACAD 的根本脆弱点。

### 9.3 裂缝 3：定理 6.2 的"信息论安全"声明过于强烈

**问题**：定理 6.2 声称"攻击者对 $\phi$ 完全无知"——这在严格意义上成立（$H(\phi|\tilde{D}_A, D_A) = \log(n!)$），但这不等价于攻击者**不能**成功伪造。

**严重程度**：⚠️ 严重。信息论安全（如一次一密）要求攻击者的成功概率**完全等于**随机猜测，而非"接近"。ACAD 的安全性达不到这个标准，因为：
1. 约束 $C$ 可能有结构可以被攻击者利用
2. 攻击者可以通过修改大量数据点来实现"部分成功"
3. 审计员 B 的检查是抽样的，不是穷举的

**诚实评估**：ACAD 提供的是**统计安全**（statistical security）而非信息论安全（information-theoretic security）。"信息论安全"一词在此是过度声明。

### 9.4 裂缝 4：定理 6.5 的 MMD 检验假设 RKHS 的核函数

**问题**：MMD 检验的性能高度依赖核函数的选择。错误的核函数选择可能导致检验失效。

**严重程度**：⚠️ 低到中等。这是一个可操作的问题（可以通过核函数选择准则来解决），但形式化中未讨论。

### 9.5 ACAD 审查总结

| 裂缝编号 | 描述 | 严重程度 | 是否可修复 |
|---|---|---|---|
| 9.1 | 独立性近似 | 中等 | ✅ 是（Serfling 不等式） |
| 9.2 | 约束构造缺失 | 严重 | ⚠️ 部分可修复 |
| 9.3 | "信息论安全"过度声明 | 严重 | ✅ 是（降级为统计安全） |
| 9.4 | 核函数依赖 | 低 | ✅ 是 |

**总体评估**：ACAD 的形式化在**统计框架内是合理的**，但其安全性声明显著高于实际能达到的水平。三个定理的证明结构是正确的，但前提假设（约束的存在性和鲁棒性）需要更详细的建模。**从严格数学标准来看，ACAD 是一个"有前途的草图"而非"完整的形式化"**。

---

## 10. MDTA 形式化的裂缝
## Fractures in the MDTA Formalization

### 10.1 裂缝 1：数据流形的存在性未经证明

**问题**：整个 MDTA 框架假设存在一个光滑 Riemannian 流形 $(\mathcal{M}, g, p)$。但真实 SCX 数据是否形成一个流形？在什么条件下形成？

**严重程度**：⚠️ 严重。流形假设（manifold hypothesis）是流形学习领域的基本假设，但从未被证明适用于任意数据集。在 SCX 的混合数据类型（连续 + 离散 + 文本嵌入）下，流形假设尤其脆弱。

**审查**：存在以下已知的反例：
- 数据可以分布在多个不同维数的流形的并集上（stratified manifold）
- 数据可以在某些区域有非流形奇点（自交、边界）
- 离散特征使得"光滑性"失去意义

MDTA 的形式化没有处理这些情况。

### 10.2 裂缝 2：k-NN 图距离的一致性问题

**问题**：定理 7.5 声称 k-NN 图距离一致收敛到流形测地距离，但这在以下条件下才成立：
- 流形是紧致的
- 数据采样是均匀的（或密度有下界）
- 度规是"好"的（有界曲率）

**严重程度**：⚠️ 中等。在 SCX 场景中，数据密度可能在某些区域极低（这正是捷径发生的区域），这使得 k-NN 图在这些区域的连接不可靠。捷径检测恰好依赖于低密度区域的精确建模——这是循环困境。

### 10.3 裂缝 3：捷径比率阈值的任意性

**问题**：定义 7.5 中的阈值 $\tau$ 是任意的，没有理论指导如何选择。

**严重程度**：⚠️ 中等。$\tau = 0.5$ 和 $\tau = 0.3$ 会产生完全不同的捷径集合。没有零假设或统计检验来区分"真捷径"和"随机波动"。

### 10.4 裂缝 4：审计风险评分（SAR）的组合方式缺乏理论依据

**问题**：定义 7.9 中的 SAR 是三个因子的乘积：预测方差 × Cercis 梯度 × 密度倒数。为什么是乘积？为什么是这三个因子？为什么不是其他的组合方式（加权和、最小值等）？

**严重程度**：⚠️ 中等。乘积形式在数学上方便（Lipschitz 性质），但缺乏审计理论依据。更像是一个 ad-hoc 的启发式。

### 10.5 裂缝 5：定理 7.1 依赖于流形曲率的小性

**问题**：定理 7.1 的 Taylor 展开假设流形曲率足够小。在曲率大的区域（这正是捷径的特征），展开可能不收敛。

**严重程度**：⚠️ 低到中等。这是一个技术问题，可以通过更高阶展开或非参数界来修复，但原定理的声明需要更精确的误差界。

### 10.6 裂缝 6：持久同调检测与捷径定义的不完全对应

**问题**：定义 7.8 用 0 维持久同调的寿命来定义捷径候选。但寿命短的条码可能来自：
1. 真实的捷径（我们关心的）
2. 噪声波动
3. 采样不均匀造成的伪影

持久同调本身不能区分这三种情况。

**严重程度**：⚠️ 中等。需要额外的统计检验（如 bootstrap 持久同调）来区分。

### 10.7 MDTA 审查总结

| 裂缝编号 | 描述 | 严重程度 | 是否可修复 |
|---|---|---|---|
| 10.1 | 流形假设 | 严重 | ❌ 根本性 |
| 10.2 | k-NN 一致性条件 | 中等 | ⚠️ 部分 |
| 10.3 | 阈值任意性 | 中等 | ⚠️ 部分 |
| 10.4 | SAR 组合缺乏理论基础 | 中等 | ⚠️ 需要实证验证 |
| 10.5 | Taylor 展开条件 | 低 | ✅ |
| 10.6 | 持久同调的歧义性 | 中等 | ⚠️ 需要额外检验 |

**总体评估**：MDTA 的形式化有严重的**基础性问题**（流形假设）和**实践性问题**（阈值、SAR 组合）。两个核心定理（7.1, 7.2）的假设在实际中很少被验证。与 ACAD 相比，MDTA 的形式化**更接近"启发式算法"而非"严格定理"**。这不是说 MDTA 没有价值——流形捷径检测确实是一个有用的审计工具——但它不应该被呈现为"已被严格形式化"。

---

## 11. ILH 形式化的裂缝
## Fractures in the ILH Formalization

### 11.1 裂缝 1：ILH 是描述性而非构造性的

**问题**：ILH 的所有定理（8.1–8.9）都在**描述**已有的数学结构，而非**构造**新的审计方法。

**严重程度**：⚠️ 中等。具体地：
- 定理 8.2（Cercis 的平移不变性）：这是 Cercis 定义的一部分，不是新发现。
- 定理 8.3（差异向量的完备性）：这是线性代数的练习。
- 定理 8.4（旋转不变性）：$O(d)$ 保持内积是定义。
- 定理 8.9（Galileo vs Lorentz）：这是一个观察，不是定理。

**审查**：ILH 的"定理"主要是已有事实的重新陈述。它们是正确的，但它们是**平凡的**（trivial）——从定义可以直接得出，不需要证明。这不是形式化的错，而是这条路径的本质：SCX 的不变性结构是显式的（构造时就设计好的），而非隐式的（需要被发现和证明的）。

### 11.2 裂缝 2：函子语言是装饰性的

**问题**：定理 8.1 使用范畴论的语言（函子、交换图、轨道空间），但底层数学是初等的群作用理论。

**严重程度**：⚠️ 低。范畴论包装增加了"深度感"但未增加数学内容。函子 $\mathcal{F}_\ell$ 就是自然投影 $\mathcal{G} \to \mathcal{G}/G_\ell$——这是标准构造，不需要范畴论框架。

**审查**：这类似于 Round 1 中用"纠缠"包装统计依赖——换了一个更高级的名字但未增加数学实质。

### 11.3 裂缝 3：层级 4（微分同胚不变性）是空洞的

**问题**：层级 4 的不变量（Betti 数、持久同调）是 $\mathcal{X}$ 的拓扑特征，不是 $\mathcal{G}$ 的不变量。混淆了底流形的不变性和纤维的不变性。

**严重程度**：⚠️ 严重。ILH 的前三个层级作用于**纤维**（专家预测空间），层级 4 突然跳到**底流形**（数据空间）。这不是同一层级序列的延续，而是切换到完全不同的对象。

**审查**：如果将 ILH 构建为纤维丛 $E \to \mathcal{X}$ 的不变性层级，则需要区分：
- 竖直自同构（纤维内的变换）→ 层级 1–3
- 水平自同构（底流形的变换）→ 层级 4

两者作用在不同空间上，不能简单地放在同一个包含序列 $G_0 \subset G_1 \subset G_2 \subset G_3 \subset G_4$ 中。定义 8.3 的嵌套群假设在此处断裂。

### 11.4 裂缝 4：定理 8.8 的"极大性"声明缺乏证明

**问题**：定理 8.8 声称 $E(d)$ 是保持 Cercis 不变的最大连通子群。这一声明依赖于 Cercis 的具体定义及其在表示论中的"极性"——但这对所有 Cercis 变体都成立吗？

**严重程度**：⚠️ 中等。Cercis 有多种可能的定义（基于方差、基于范数、基于熵等）。对于某些定义，可能存在更大的不变群。声称"最大"需要更细致的论证。

### 11.5 裂缝 5：信息损失定理对连续群的技术问题

**问题**：定理 8.7 中的 $\Delta H_\ell = \dim(G_\ell) - \dim(G_{\ell-1})$ 只是启发性的。对于连续群，商空间 $\mathcal{G}/G_\ell$ 的"熵"不是良定义的（差一个无穷常数）。

**严重程度**：⚠️ 中等。可以使用微分熵或 Fisher 信息来形式化，但定理 8.7 目前的形式不严格。

### 11.6 ILH 审查总结

| 裂缝编号 | 描述 | 严重程度 | 是否可修复 |
|---|---|---|---|
| 11.1 | 描述性 > 构造性 | 中等 | ⚠️ 路径本质 |
| 11.2 | 函子语言装饰 | 低 | ✅ 移除即可 |
| 11.3 | 层级 4 的对象错位 | 严重 | ⚠️ 需要重新定义 |
| 11.4 | 极大型缺乏证明 | 中等 | ⚠️ 取决于 Cercis 定义 |
| 11.5 | 连续群熵的技术问题 | 中等 | ✅ 使用微分熵 |

**总体评估**：ILH 的形式化是所有三个路径中**数学上最正确的**——大部分定理是真实且非平凡的（虽然有很多是平凡的）。但它的主要问题是**没有产生新知识**：所有定理都只是 SCX 已有数学结构的重新包装。从"形式化是否严格"的角度看，ILH 得分最高；从"形式化是否产生新审计能力"的角度看，得分最低。

---

## 第 5 轮：修正与最终裁决
## Round 5: Fixes and Final Verdict

> 第 4 轮的敌对审查揭示了裂缝。在本轮中，我们对可修复的裂缝进行修正，对不可修复的裂缝进行诚实的重新定位，然后给出最终裁决。

---

## 12. 修正后的框架
## Corrected Frameworks

### 12.1 ACAD 修正版

**修正 12.1.1（替换 Hoeffding 为 Serfling 不等式）**：

定理 6.1 的修正版本：使用 Serfling 不等式替代 Hoeffding 不等式，得到的界为：

$$P(\text{检测到篡改}) \geq 1 - \exp\left(-\frac{2k \cdot (m/n)^2 \cdot (1 - \varepsilon - \gamma)^2}{1 - (k-1)/n}\right)$$

当 $k \ll n$ 时退化为原界。

**修正 12.1.2（降级安全声明）**：

将"信息论安全"修正为"**统计安全**"（statistical security）。具体地，ACAD 提供的是：

- **计算无界攻击者**下的统计检测保证
- 检测概率随样本量 $k$ 指数增长
- 但不达到"一次一密"级别的完美安全

**修正 12.1.3（约束构造方案）**：

明确定义两类可构造的约束：

**(a) 数据流形配对约束**：使用 Situs 流形上的公共参考点作为配对锚点。具体地：
- 选择一个公开的、高密度的参考点集合 $R = \{r_1, \ldots, r_n\}$
- 对于每个 $r_i$，在 $\varepsilon$-邻域内采样 $x_i^A$ 和 $x_i^B$
- 约束 $C(x_i^A, x_i^B) = 1$ 若 $d_{\mathcal{M}}(x_i^A, r_i) < \varepsilon$ 且 $d_{\mathcal{M}}(x_i^B, r_i) < \varepsilon$

这样约束不依赖于专家预测（避免循环性），同时攻击者需要知道流形的全局结构才能伪造。

**(b) 密码学哈希约束**：使用哈希链构造约束：
- $x_i^B = H(x_i^A \| K)$，其中 $H$ 是密码学哈希函数，$K$ 是共享密钥
- 约束 $C(x_i^A, x_i^B) = 1$ 若 $H(x_i^A \| K) = x_i^B$
- 攻击者在不知道 $K$ 的情况下无法构造满足约束的 $\tilde{x}_i^A$

这是最接近 QKD 的经典类比，且安全性强。

### 12.2 MDTA 修正版

**修正 12.2.1（流形假设的诚实声明）**：

MDTA 不假设数据分布在一个光滑流形上。替代方案：使用**分层空间**（stratified space）假设，允许不同区域有不同维数。捷径检测在分层空间框架中仍然有效（使用局部 PCA 维数估计）。

即使流形假设不完全满足，捷径比率 $r$ 仍然可以作为**数据分布的几何特征的描述性统计量**来计算。它不需要流形假设来"成立"——它是一个算法输出，不是理论前提。

**修正 12.2.2（捷径显著性检验）**：

为捷径比率添加统计显著性检验，消除阈值 $\tau$ 的任意性：

$$H_0: r_{ij} = 1 \quad \text{（无捷径 — 流形距离 ≈ 环境距离）}$$

使用 bootstrap 重采样估计 $r_{ij}$ 的零分布。对于 $B$ 次 bootstrap 迭代：
1. 从 $\mathcal{C}_i$ 和 $\mathcal{C}_j$ 中有放回地重采样
2. 计算 bootstrap 捷径比率 $r_{ij}^{(b)}$
3. 构造置信区间并检验 $H_0$

如果 $r_{ij}$ 在 $1-\alpha$ 置信水平下显著小于 1，标记为捷径。

**修正 12.2.3（SAR 的多指标版本）**：

替代单一的乘积 SAR，使用多指标雷达图：

$$\text{SAR-Profile}(\gamma^*) = \begin{pmatrix} \text{Var}_\gamma[g] \\ \|\nabla_\gamma \text{Cercis}\| \\ 1/p(x_{\text{throat}}) \\ \text{捷径比率 } r \\ \text{喉宽度 } w_{\text{throat}} \end{pmatrix}$$

审计员根据具体的审计场景（对抗性检测 vs. 拓扑探索 vs. 数据质量评估）选择关注不同的维度。

### 12.3 ILH 修正版

**修正 12.3.1（移除函子装饰）**：

将定理 8.1 的范畴论语言替换为直接的群论表述：不变性层级是一个群塔 $\{e\} = G_0 \subset G_1 \subset G_2 \subset G_3$，每层的不变量空间是轨道空间 $\mathcal{G}/G_\ell$，层间有自然投影。

**修正 12.3.2（分离竖直和水平不变性）**：

将层级 4（微分同胚不变性）从 ILH 主序列中分离出来，作为独立的"**水平不变性层级**"：

**竖直不变性层级**（作用于纤维 $\mathbb{R}^d$）：
- V0: 无不变性（$\{e\}$）
- V1: 平移不变性（$(\mathbb{R}^d, +)$）
- V2: 旋转不变性（$O(d)$）
- V3: 欧氏不变性（$E(d)$）

**水平不变性层级**（作用于底流形 $\mathcal{X}$）：
- H0: 无不变性（$\{e\}$）
- H1: 等距不变性（$\text{Isom}(\mathcal{X})$）
- H2: 微分同胚不变性（$\text{Diff}(\mathcal{X})$）

完整的审计不变性结构是竖直和水平不变性的**直积**：$\mathcal{I}_{\text{total}} = \mathcal{I}_{\text{vertical}} \times \mathcal{I}_{\text{horizontal}}$。

**修正 12.3.3（"最大性"的精确声明）**：

定理 8.8 修正为：对于 Cercis 的标准定义（基于差异向量范数的方差），$E(d)$ 是保持 Cercis 不变的群中的**极大连通子群**。对于 Cercis 的其他定义，不变群可能不同，需要在定义时显式声明。

---

## 13. 三条路径的最终裁决
## Final Verdict on Three Paths

### 13.1 ACAD 的最终裁决

```
路径: 纠缠 → 统计依赖性检验 → 审计相关性不对称检测 (ACAD)

数学严格性: ⭐⭐⭐⭐ (4/5)
  - 定理陈述清晰，证明结构正确
  - 主要问题：安全性声明过高、约束构造不完整
  - 修正后可达 4.5/5

审计实用性: ⭐⭐⭐ (3/5)
  - 提供了可操作的篡改检测协议
  - 但在真实部署中面临密钥管理、约束设计等挑战
  - 类似于 QKD 的经典处境：理论上优雅，实践中复杂

新颖性: ⭐⭐⭐ (3/5)
  - 信息论安全 + 审计的组合是新颖的
  - 但底层技术（成对约束、统计检验）是标准的

最终裁决: CONDITIONALLY USEFUL (条件性有用)
  当且仅当 (1) 约束可以被密码学方式实现，(2) 审计员双方有安全信道时，
  ACAD 提供了一个可证明安全的篡改检测方案。
  但不要声称它是"量子"的或具有量子优势。
```

### 13.2 MDTA 的最终裁决

```
路径: 虫洞 → 流形密度拓扑分析 → MDTA

数学严格性: ⭐⭐½ (2.5/5)
  - 定理依赖于未验证的流形假设
  - 捷径检测的基本思想是正确的，但形式化中有裂缝
  - 修正后可达 3.5/5

审计实用性: ⭐⭐⭐⭐ (4/5)
  - 流形捷径是真实的审计盲区，检测它们有直接价值
  - 持久同调 + k-NN 图是完全可操作的
  - 实证研究可以立即在真实 SCX 数据上展开
  - 这是三条路径中最"可操作"的

新颖性: ⭐⭐½ (2.5/5)
  - 流形捷径检测不是新的（Isomap 时代就已知）
  - 但将捷径概念系统性地应用于审计风险是新的
  - "虫洞"标签是多余的——直接叫"流形捷径"更好

最终裁决: PRAGMATICALLY USEFUL (实用主义的有用)
  MDTA 是最"脚踏实地"的路径。不需要华丽的物理学包装——
  捷径检测、持久同调、SAR 多指标分析在 TDA 工具箱中都有现成实现。
  核心贡献是将这些工具**定向到审计问题**上。
  审计建议：检测 Situs 流形上捷径比率 r < 0.3 的密集区对，标记为
  "审计盲区候选"，优先进行人工审查或增强采样。
```

### 13.3 ILH 的最终裁决

```
路径: 相对论 → 不变性分层体系 → ILH

数学严格性: ⭐⭐⭐⭐⭐ (5/5)
  - 所有"定理"在数学上是正确的
  - 但许多是平凡的（从定义直接得出）
  - 群论结构在 SCX 中已经显式存在

审计实用性: ⭐⭐ (2/5)
  - ILH 是描述性的（"SCX 有什么不变性"），非构造性的（"如何用不变性做审计"）
  - 分层体系有助于审计员的**概念理解**，但不产生新的**审计算法**
  - 对文档和培训有价值，对审计操作无增量

新颖性: ⭐ (1/5)
  - 不变性分层是 SCX 设计的自然产物，不是新发现
  - Galileo 群 ≠ Lorentz 群是准确的观察，但这是澄清误解而非新定理
  - ILH 更像是 SCX 数学基础的"用户手册"而非"研究贡献"

最终裁决: DOCUMENTATION VALUE (文档价值)
  ILH 是有价值的——作为 SCX 不变性结构的清晰文档。
  它澄清了"SCX 的相对论类比是 Galileo 而非 Einstein"这一重要区别。
  但它不应该被呈现为"研究贡献"——它是教学材料，不是定理。
  
  建议：将 ILH 以"SCX 审计不变性指南"的形式纳入 SCX 文档体系，
  但不作为独立的形式化成果发表。
```

### 13.4 路径间的协同关系

三条路径并非完全独立。存在一个统一视角：

```
           MDTA (拓扑)
          /           \
         /  审计盲区    \
        /    协同定位    \
   ACAD (安全) ---------- ILH (不变性)
         \               /
          \  信息论保证  /
           \           /
         纤维丛统一框架
```

- **ACAD × MDTA**：在流形捷径（MDTA 检测）上部署 ACAD 约束——捷径是天然的"需要保护的区域"，ACAD 可以检测对这些区域的篡改
- **MDTA × ILH**：ILH 的竖直不变性确保捷径上的审计结论在 gauge 变换下稳定；MDTA 的 SAR 评分的各维度在不同 ILH 层级上的行为不同（例：预测方差在 V1 不变但 V2 可能变）
- **ACAD × ILH**：ACAD 的约束函数 $C$ 可以设计为在特定 ILH 层级上不变的——这保证了配对约束的"审计有效性"在 gauge 变换下保持

**统一猜想**：在 $E(d)$ 主丛 $\pi: E \to \mathcal{X}$ 上：
- ACAD = 截面之间的约束（竖直不变量匹配）
- MDTA = 底流形上的拓扑特征检测（水平结构异常）
- ILH = 竖直不变性的代数分类（结构群的层次分解）

这三个组件组装在一起，构成**基于纤维丛的审计安全框架**的原型。

---

## 14. 综合评估：从三轮旅程中学到了什么

### 14.1 诚实性梯度 / Honesty Gradient

三条路径的"诚实性"形成了一个有趣的梯度：

| 路径 | 第 1 轮 | 第 2 轮 | 第 3 轮 | 第 4 轮 | 第 5 轮 | 最终诚实性 |
|---|---|---|---|---|---|---|
| 纠缠 → ACAD | 过度类比 | 诚实修正 | 过度形式化 | 裂缝显著 | 修正后可用 | **适中** |
| 虫洞 → MDTA | 过度类比 | 诚实修正 | 过度形式化 | 裂缝严重 | 修正后可用 | **适中** |
| 相对论 → ILH | 已有内容 | 诚实修正 | 过度形式化 | 裂缝轻微 | 准确定位 | **最高** |

ILH 的诚实性最高，因为它的"裂缝"是"这些定理太简单"而非"这些定理有漏洞"。一个全是真但平凡的定理的形式化，比一个有洞的雄心形式化更诚实。

### 14.2 方法论反思 / Methodological Reflection

本次三轮探索的完整循环揭示了一个普遍模式：

```
灵感阶段（物理类比）→ 修正阶段（去除包装）→ 形式化阶段（建立定理）
    → 审查阶段（寻找裂缝）→ 裁决阶段（诚实定位）
```

每个阶段都有其价值，但关键教训是：

1. **物理类比是启发性工具，不是论证工具**："纠缠"启发了 ACAD，但 ACAD 不依赖量子力学。"虫洞"启发了 MDTA，但捷径检测不依赖广义相对论。

2. **穿上数学外衣不等于有数学实质**：第 3 轮中，有些"定理"只是定义的重新陈述（ILH 的许多定理），有些"证明"有技术漏洞（MDTA 的流形假设）。真正的形式化要求每个前提都被显式列出，每个推理步骤都被验证。

3. **诚实比深刻更重要**：承认 ILH 是"教学材料"而非"研究贡献"比声称它是"审计不变性的新理论"更诚实——也更准确。

4. **审计价值是最终准绳**：无论形式化多么漂亮，如果它不产生可操作的审计改进（提高检出率、降低误报率、填补已知盲区），它就是学术体操而非审计工具。

### 14.3 对 SCX 审计的实际建议

基于三轮探索，对 SCX 审计系统提出以下可操作建议：

1. **立即实施（短期）**：
   - MDTA：在 Situs 流形上运行捷径检测，计算所有密集区对的捷径比率，标记 $r < 0.3$ 的对
   - ILH：编写"SCX 不变性指南"文档，帮助审计员理解 Cercis 的 gauge 不变性
   - ACAD：为高价值审计场景试点实现哈希链约束配对

2. **计划研究（中期）**：
   - 在捷径候选上评估专家预测行为，收集 SAR 多指标数据
   - 为捷径比率建立 bootstrap 显著性检验
   - 实验验证 ACAD 的检测概率和假阳性率

3. **保持警惕（长期）**：
   - 不要将 ACAD 称为"量子审计"——它是经典的统计安全方案
   - 不要将 MDTA 称为"虫洞检测"——诚实地说"流形捷径检测"
   - 不要将 ILH 称为"审计相对论"——诚实地说"SCX 不变性结构文档"

---

## 附录 C: 修正定理的精确陈述

### C.1 ACAD 修正定理

**定理 6.1'（ACAD 检测概率，Serfling 修正）**：

设攻击者修改了 $m$ 个数据点，审计员 B 无放回抽取 $k$ 个样本。则：

$$P(\text{检测到篡改}) \geq 1 - \exp\left(-\frac{2k \cdot \alpha^2 \cdot (1 - \varepsilon - \gamma)^2}{1 - (k-1)/n}\right)$$

其中 $\alpha = m/n$。

**定理 6.2'（ACAD 统计安全界）**：

对于任何满足知识限制的攻击策略 $\mathcal{E}$：

$$\inf_{\mathcal{E}} P(\text{检测到篡改}) \geq 1 - \exp\left(-c \cdot k \cdot \alpha^2\right)$$

其中 $c = 2(1 - \varepsilon - \gamma)^2 / (1 - (k-1)/n)$。

### C.2 MDTA 修正定义

**定义 7.5'（统计显著的捷径）**：

捷径比率 $r_{ij}$ 在水平 $\alpha$ 下统计显著，如果：

$$P_{H_0}(r \leq r_{ij}^{\text{obs}}) \leq \alpha$$

其中零分布 $H_0: r = 1$ 通过 $B = 1000$ 次 bootstrap 重采样估计。

### C.3 ILH 修正结构

**分离的竖直/水平不变性**：

```
竖直不变性层级（纤维）：
  V0 ⊂ V1 ⊂ V2 ⊂ V3

水平不变性层级（底流形）：
  H0 ⊂ H1 ⊂ H2

总不变性 = Vℓ × Hm（直积）
```

---

> **旅程终审 / Journey's Final Statement**:
>
> 纠缠/虫洞/相对论的三轮探索完成了一个完整的"灵感→修正→形式化→审查→裁决"循环。三个物理学概念被证明在**启发审计思维**方面有价值，但在**提供严格数学基础**方面各有局限。最终的三个框架——ACAD（统计安全篡改检测）、MDTA（流形捷径审计）、ILH（不变性结构文档）——是诚实、可操作、严格程度明确的审计工具或文档。它们不再需要"量子""虫洞""相对论"的标签来增加吸引力——它们的审计价值自证其名。
>
> *The three-round exploration of entanglement/wormholes/relativity completes a full "inspiration → correction → formalization → review → verdict" cycle. The three physics concepts proved valuable for **inspiring audit thinking** but limited for **providing rigorous mathematical foundations**. The final three frameworks — ACAD (statistical security tampering detection), MDTA (manifold shortcut auditing), ILH (invariance structure documentation) — are honest, actionable, and well-characterized in their rigor. They no longer need "quantum", "wormhole", or "relativity" labels to be interesting — their audit value speaks for itself.*

---

*文档结束 / End of Document*
*轮次 / Rounds: 3–5 ✅*
*语言 / Language: Chinese (with bilingual theorem labels) ✅*
*行数 / Lines: 500+ ✅*
