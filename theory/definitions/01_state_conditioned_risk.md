# Definition 1: State-Conditioned Expert Risk

> SCX 框架的核心数学对象定义文档。定义状态、状态条件专家风险、SCX 可靠性、数据价值等基本概念。

---

## 1. 状态空间 (State Space)

### 定义 1.1：状态 (State)

状态 $s$ 是输入空间 $\mathcal{X}$ 的一个可测子集。状态划分 $\Pi = \{s_1, s_2, \dots, s_K\}$ 满足：

1. $\bigcup_{k=1}^K s_k = \mathcal{X}$
2. $s_k \cap s_{k'} = \emptyset$ 当 $k \neq k'$
3. 每个 $s_k$ 是 $\mathcal{X}$ 的 Borel $\sigma$-代数中的可测集

状态划分的数学本质是找到一个映射 $\phi: \mathcal{X} \to \mathcal{S}$，使得：

$$P(Y|X) \approx P(Y|\phi(X))$$

即 $\phi(X)$ 是 $Y$ 关于 $X$ 的**近似充分统计量**。

### 定义 1.2：软状态赋值 (Soft State Assignment)

软状态赋值函数 $\gamma: \mathcal{X} \times \mathcal{S} \to [0,1]$ 满足：

$$\sum_{s \in \mathcal{S}} \gamma_s(x) = 1, \quad \forall x \in \mathcal{X}$$

常见实现方式：

- **GMM 后验概率**：$\gamma_s(x) = \frac{\pi_s \mathcal{N}(\phi(x) \mid \mu_s, \Sigma_s)}{\sum_{t \in \mathcal{S}} \pi_t \mathcal{N}(\phi(x) \mid \mu_t, \Sigma_t)}$
- **Kernel 加权**：$\gamma_s(x) = \frac{\kappa(\phi(x), \mu_s)}{\sum_{t \in \mathcal{S}} \kappa(\phi(x), \mu_t)}$
- **KNN 概率**：$\gamma_s(x) = \frac{|\text{KNN}(x) \cap s|}{k}$

---

## 2. 条件风险 (Conditional Risk)

### 定义 2.1：点态风险 (Pointwise Risk)

专家 $f_m$ 在输入 $x$ 处的点态风险：

$$R_m(x) = \mathbb{E}[\ell(f_m(x), f^*(x)) \mid X = x]$$

其中 $\ell: \mathcal{Y} \times \mathcal{Y} \to \mathbb{R}_{\ge 0}$ 为损失函数，$f^*: \mathcal{X} \to \mathcal{Y}$ 为真实标注函数。

### 定义 2.2：状态条件专家风险 (State-Conditioned Expert Risk)

$$R_m(s) = \mathbb{E}_{x \sim P(\cdot|s)}[\ell(f_m(x), f^*(x))]$$

这是 Kolmogorov 意义下的条件期望。由 Radon-Nikodym 定理保证存在性：

$$R_m(s) = \frac{1}{P(X \in s)} \int_{X \in s} \ell(f_m(x), f^*(x)) \, dP_X(x)$$

当 $P(X \in s) = 0$ 时，$R_m(s)$ 可定义为 $\lim_{\epsilon \to 0^+} R_m(s_\epsilon)$，其中 $s_\epsilon$ 是 $s$ 的 $\epsilon$-邻域。

### 定义 2.3：条件贝叶斯风险 (Conditional Bayes Risk)

$$R^*(s) = \inf_{f \text{ 可测}} \mathbb{E}[\ell(f(X), Y) \mid X \in s]$$

专家风险 $R_m(s)$ 衡量专家 $f_m$ 相对于**不可知最优** $f^*$ 的表现，而非相对于 $R^*(s)$。

### 偏差-方差分解

对于平方损失 $\ell(\hat{y}, y) = (\hat{y} - y)^2$，令回归函数 $r(x) = \mathbb{E}[Y \mid X = x]$：

$$R_m(s) = \underbrace{\mathbb{E}[(f_m(X) - r(X))^2 \mid X \in s]}_{\text{近似误差}} + \underbrace{\mathbb{E}[(r(X) - f^*(X))^2 \mid X \in s]}_{\text{目标噪声}}$$

在 $f^* = r$ 的特殊情况下得到**条件偏差-方差分解**：

$$R_m(s) = \mathbb{E}[(f_m(X) - r(X))^2 \mid X \in s] + \mathbb{E}[\text{Var}(Y \mid X) \mid X \in s]$$

---

## 3. SCX 可靠性 (SCX Reliability)

### 定义 3.1：SCX 可靠性

$$SCX_m(s) = P(\ell(f_m(x), f^*(x)) < \tau \mid x \in s)$$

其中 $\tau > 0$ 为可靠性阈值。经验估计为：

$$\widehat{SCX}_m(s) = \frac{|\{x_i \in s : \ell(f_m(x_i), y_i) < \tau\}|}{|s|}$$

### 与 IRT 的关系

SCX 的 $SCX_m(s)$ 可以映射到 Rasch 模型：

$$\log\left(\frac{SCX_m(s)}{1 - SCX_m(s)}\right) = \theta_s - b_m$$

其中 $\theta_s$ 是状态 $s$ 的"可处理性"参数，$b_m$ 是专家 $m$ 的能力阈值。

---

## 4. 状态数据价值 (State Data Value)

### 定义 4.1：状态数据价值

$$V(s) = \bar{r}(s) \cdot \rho(s) \cdot L(s) \cdot [1 - D(s)] \cdot \max_m SCX_m(s)$$

各因子含义：

| 因子 | 符号 | 含义 | 范围 |
|------|------|------|------|
| 平均残差 | $\bar{r}(s)$ | 状态 $s$ 的当前平均预测误差 | $[0, L_{\max}]$ |
| 状态概率 | $\rho(s)$ | 状态 $s$ 的出现概率 $P(x \in s)$ | $[0, 1]$ |
| 可学习性 | $L(s)$ | 状态 $s$ 的性能可改善程度 | $[0, 1]$ |
| 多样性惩罚 | $1-D(s)$ | 状态 $s$ 的未饱和程度（$D$=冗余度） | $[0, 1]$ |
| 专家覆盖 | $\max_m SCX_m(s)$ | 最佳专家在状态 $s$ 上的可靠性 | $[0, 1]$ |

### 与 Shapley 值的关系

SCX 的 $V(s)$ 是一个**代理 Shapley 值**，它将数据点级别的 Shapley 值计算分解为：
- 先聚合成状态 $s$（复杂度 $O(2^{|S|)}$，其中 $|S| \ll N$）
- 再使用乘法分解（五个可解释因子的乘积）

---

## 5. 噪声与可学习性 (Noise & Learnability)

### 定义 5.1：噪声分数

$$\text{NoiseScore}(x_i) = r_i \cdot \frac{1}{\rho(s_i) + \varepsilon} \cdot [1 - C(s_i)]$$

其中 $C(s)$ 为状态 $s$ 的内部一致性：

$$C(s) = 1 - \frac{1}{|s|} \sum_{x_i \in s} \frac{|\ell(f_m(x_i), y_i) - \bar{\ell}(s)|}{\max \ell - \min \ell}$$

### 定义 5.2：可学习性

$$L(s) = \inf_{f \in \mathcal{F}} \left[ \frac{R(f|s) - R^*(s)}{R^*(s)} \right]^{-1}$$

其中 $R(f|s) = \mathbb{E}[\ell(f(X), Y) | X \in s]$，$R^*(s) = \inf_f R(f|s)$ 是贝叶斯风险。$L(s) \to 0$ 表示状态在现有函数类 $\mathcal{F}$ 下不可学习。

### 定义 5.3：冗余度

状态冗余度估计：

$$D(s) = \rho(s) \cdot \bigl(1 - \bar{r}(s)\bigr) \cdot \text{Sim}(s) \cdot \bigl(1 - \text{Boundary}(s)\bigr)$$

其中 $\text{Sim}(s)$ 为状态内部相似度，$\text{Boundary}(s)$ 为边界样本比例。

---

## 6. 专家路由 (Expert Routing)

### 定义 6.1：状态条件专家权重

$$w_m(x) \propto \exp\left(-\alpha \cdot \sum_{s \in \mathcal{S}} \gamma_s(x) \cdot \hat{R}_m(s)\right)$$

归一化保证 $\sum_{m=1}^M w_m(x) = 1$，$\alpha > 0$ 为逆温度参数。

### 定义 6.2：硬路由

$$m^*(x) = \arg\min_{m \in [M]} \sum_{s \in \mathcal{S}} \gamma_s(x) \cdot R_m(s)$$

---

## 7. 收敛性质

### 定理 7.1：经验风险估计的集中性

设 $\ell \in [0, L_{\max}]$，状态 $s$ 有 $n_s$ 个样本。对任意 $\delta > 0$，以概率至少 $1 - \delta$：

$$|\hat{R}_m(s) - R_m(s)| \leq L_{\max} \sqrt{\frac{\log(2/\delta)}{2n_s}}$$

### 定理 7.2：最小最大下界

存在分布使得任意估计器 $\hat{R}_m(s)$ 满足：

$$\mathbb{E}[|\hat{R}_m(s) - R_m(s)|] \geq \frac{\sigma(s)}{2\sqrt{n_s}}$$

其中 $\sigma^2(s) = \text{Var}(\ell(f_m(X), f^*(X)) \mid X \in s)$。

---

## 符号表

| 符号 | 含义 | 类型 |
|------|------|------|
| $\mathcal{X}$ | 输入空间 | 度量空间 |
| $\mathcal{Y}$ | 标签空间 | $\mathbb{R}^d$ |
| $f^*: \mathcal{X} \to \mathcal{Y}$ | 真实标注函数 | 未知 oracle |
| $f_m: \mathcal{X} \to \mathcal{Y}$ | 第 $m$ 个专家模型 | 可计算函数 |
| $M$ | 专家总数 | $\mathbb{N}$ |
| $\mathcal{S}$ | 状态空间 | $|\mathcal{S}| = K$ |
| $s$ | 单个状态 | $\mathcal{X}$ 的可测子集 |
| $\gamma_s(x)$ | 状态软赋值 | $[0,1]$ |
| $\ell$ | 损失函数 | $\mathbb{R}_{\ge 0}$ |
| $\tau$ | 可靠性阈值 | $\mathbb{R}_{>0}$ |
| $R_m(s)$ | 状态条件专家风险 | $\mathbb{R}_{\ge 0}$ |
| $SCX_m(s)$ | SCX 可靠性指标 | $[0, 1]$ |
| $V(s)$ | 状态数据价值 | $\mathbb{R}_{\ge 0}$ |
| $\bar{r}(s)$ | 状态平均残差 | $[0, L_{\max}]$ |
| $\rho(s)$ | 状态概率 | $[0, 1]$ |
| $L(s)$ | 可学习性 | $[0, 1]$ |
| $C(s)$ | 内部一致性 | $[0, 1]$ |
| $N(s)$ | 噪声比例 | $[0, 1]$ |
| $D(s)$ | 冗余度 | $[0, 1]$ |
| $\phi(x)$ | 嵌入映射 | $\mathbb{R}^d$ |
| $\alpha$ | 逆温度参数 | $\mathbb{R}_{>0}$ |
| $\eta(x)$ | 回归函数 $\mathbb{E}[Y \mid X=x]$ | $\mathbb{R}$ |
| $R^*(s)$ | 条件贝叶斯风险 | $\mathbb{R}_{\ge 0}$ |

---

## 参考文献

1. Kolmogorov, A. N. (1933). *Grundbegriffe der Wahrscheinlichkeitsrechnung*.
2. Wald, A. (1950). *Statistical Decision Functions*.
3. Shapley, L. S. (1953). A value for n-person games. *Contributions to the Theory of Games*.
4. Tishby, N., Pereira, F. C., & Bialek, W. (1999). The information bottleneck method. *Allerton Conference*.
5. SCX 核心框架数学分析. `01_SCX_核心框架_数学分析.md`
6. SCX 数学基础与证明建构. `05_数学根源与证明.md`
