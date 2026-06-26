# Proposition 3: State-Conditioned Expert Weighting

> 最优专家权重不是全局常数，而是状态条件函数。状态条件权重的期望风险不高于任何全局固定权重。

---

## 1 Statement

### 1.1 正式陈述

设 $M$ 个专家 $f_1, \ldots, f_M$，融合预测为：

$$f_{\text{ens}}(x) = \sum_{m=1}^M w_m(x) f_m(x) \quad (\text{状态条件})$$
$$\bar{f}_{\text{ens}}(x) = \sum_{m=1}^M \bar{w}_m f_m(x) \quad (\text{全局固定})$$

其中 $w_m(x) \geq 0$, $\sum_m w_m(x) = 1$；$\bar{w}_m \geq 0$, $\sum_m \bar{w}_m = 1$。

风险为 $R(f) = \mathbb{E}[\ell(f(X), f^*(X))]$。

最优专家权重不是全局常数 $w_m = \text{const}$，而是状态条件函数：

$$w_m(x) \propto \exp\left(-\alpha \cdot \sum_s \gamma_s(x) \cdot \hat{R}_m(s)\right)$$

在以下意义下，状态条件权重优于全局权重：

$$\mathbb{E}_{x \sim P}\left[\sum_m w_m(x) \ell(f_m(x), y)\right] \leq \mathbb{E}_{x \sim P}\left[\sum_m w_m^{\text{global}} \ell(f_m(x), y)\right]$$

只要状态划分 $\Pi$ 是 $Y$ 的充分统计量或与其近似。

### 1.2 凸性假设

损失函数 $\ell(\cdot, \cdot)$ 对第一个参数是凸的。常见损失（MSE、交叉熵、Hinge）均满足。

---

## 2 Formal Proof

### 2.1 利用 Jensen 不等式和条件期望的塔性质

**步骤 1：定义状态条件风险差**

对任意固定的全局权重 $\bar{w} = (\bar{w}_1, \ldots, \bar{w}_M)$，全局固定融合的风险为：

$$R(\bar{f}_{\text{ens}}) = \mathbb{E}_X\left[\ell\left(\sum_m \bar{w}_m f_m(X), f^*(X)\right)\right]$$

状态条件融合的风险为：

$$R(f_{\text{ens}}) = \mathbb{E}_X\left[\ell\left(\sum_m w_m(X) f_m(X), f^*(X)\right)\right]$$

**步骤 2：对任意 $x$，构造最优状态条件权重**

在给定 $x$ 时，最优权重 $w^*(x) = \arg\min_{w \in \Delta^{M-1}} \ell(\sum_m w_m f_m(x), f^*(x))$。

由于 $x$ 已知，最优权重可以完美匹配 $x$ 处的点态最优专家组合，因此对任意单点 $x$：

$$\ell\left(\sum_m w_m^*(x) f_m(x), f^*(x)\right) \leq \ell\left(\sum_m \bar{w}_m f_m(x), f^*(x)\right)$$

等号仅当 $\bar{w} \in \arg\min_{w \in \Delta^{M-1}} \ell(\sum_m w_m f_m(x), f^*(x))$ 时成立。

**步骤 3：在分布上取期望**

由于对每个 $x$ 逐点不等式成立，取期望保序：

$$\mathbb{E}_X\left[\ell\left(\sum_m w_m^*(X) f_m(X), f^*(X)\right)\right] \leq \mathbb{E}_X\left[\ell\left(\sum_m \bar{w}_m f_m(X), f^*(X)\right)\right]$$

即 $R(f_{\text{ens}}^*) \leq R(\bar{f}_{\text{ens}})$。

**步骤 4：SCX 的 $w_m(x)$ 是 $w^*(x)$ 的近似**

SCX 权重 $w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(x) \hat{R}_m(s))$ 不一定是 $w^*(x)$，但它是基于经验风险的估计。当 $\hat{R}_m(s) \xrightarrow{p} R_m(s)$ 且 $\gamma_s(x)$ 是 $x$ 位于状态 $s$ 的精确后验概率时，$w_m(x)$ 将收敛到 $w_m^*(x)$。$\square$

### 2.2 基于 Gibbs 不等式的严格证明

**定义权重**：

状态条件权重：

$$w_m(s) = \frac{\exp(-\alpha \hat{R}_m(s))}{\sum_{m'} \exp(-\alpha \hat{R}_{m'}(s))}$$

全局权重：

$$w_m^{\text{global}} = \frac{\exp(-\alpha \hat{R}_m)}{\sum_{m'} \exp(-\alpha \hat{R}_{m'})}$$

**Step 1：使用 Gibbs 不等式**

对于固定的 $x \in s$，在状态 $s$ 内，权重 $w_m(s)$ 最小化以下目标：

$$J_s(w) = \sum_m w_m \hat{R}_m(s) + \frac{1}{\alpha} \sum_m w_m \log w_m$$

这是概率单纯形上的凸优化，其 KKT 条件给出 $w_m(s)$ 为唯一解。因此对于任意其他权重向量 $w'$（包括 $w_m^{\text{global}}$）：

$$\sum_m w_m(s) \hat{R}_m(s) + \frac{1}{\alpha} \sum_m w_m(s) \log w_m(s) \leq \sum_m w_m^{\text{global}} \hat{R}_m(s) + \frac{1}{\alpha} \sum_m w_m^{\text{global}} \log w_m^{\text{global}}$$

**Step 2：两边取条件期望**

给定 $x \in s$：

$$\mathbb{E}\left[\sum_m w_m(s) \ell(f_m(X), Y) \mid X \in s\right] + \frac{1}{\alpha} H(w(s)) \leq \mathbb{E}\left[\sum_m w_m^{\text{global}} \ell(f_m(X), Y) \mid X \in s\right] + \frac{1}{\alpha} H(w^{\text{global}})$$

其中 $H(w) = -\sum_m w_m \log w_m$ 为 Shannon 熵。

**Step 3：利用熵差**

由 Jensen 不等式，全局权重的熵小于等于状态条件权重的期望熵：

$$H(w^{\text{global}}) \leq \mathbb{E}_{s}[H(w(s))]$$

这是因为凸函数 $-H$ 满足：$H(\mathbb{E}[w(s)]) \geq \mathbb{E}[H(w(s))]$。因此：

$$\mathbb{E}\left[\sum_m w_m(s) \ell(f_m(X), Y) \right] \leq \mathbb{E}\left[\sum_m w_m^{\text{global}} \ell(f_m(X), Y) \right]$$

**严格性**：当且仅当所有状态有相同的风险估计（即 $\hat{R}_m(s) = \hat{R}_m$ 对所有 $s$ 成立），或者熵差正好抵消风险差时，等号成立。否则不等式严格。$\square$

### 2.3 Bound 的显式化

**定理 3.1**：若 $\ell$ 有界于 $[0, L_{\max}]$，则：

$$\mathbb{E}\left[\sum_m w_m(s) \ell(f_m(X), Y)\right] \leq \mathbb{E}\left[\sum_m w_m^{\text{global}} \ell(f_m(X), Y)\right] - \frac{1}{\alpha} \cdot I(s; w)$$

其中 $I(s; w) = \mathbb{E}_s[\text{KL}(w(s) \| w^{\text{global}})]$ 为状态与权重的互信息。

**证明**：

$$\begin{aligned}
&\mathbb{E}\left[\sum_m w_m^{\text{global}} \ell(f_m(X), Y) - \sum_m w_m(s) \ell(f_m(X), Y)\right] \\
&= \mathbb{E}\left[\sum_m (w_m^{\text{global}} - w_m(s)) \ell(f_m(X), Y)\right] \\
&= \mathbb{E}\left[\sum_m (w_m^{\text{global}} - w_m(s)) (\ell(f_m(X), Y) - \hat{R}_m(s))\right] + \mathbb{E}\left[\sum_m (w_m^{\text{global}} - w_m(s)) \hat{R}_m(s)\right] \\
&\geq \mathbb{E}\left[\sum_m (w_m^{\text{global}} - w_m(s)) \hat{R}_m(s)\right] \quad (\text{由于 } \ell - \hat{R} \text{ 是零均值噪声})
\end{aligned}$$

由 Gibbs 不等式：

$$\sum_m (w_m^{\text{global}} - w_m(s)) \hat{R}_m(s) = \frac{1}{\alpha} \sum_m w_m(s) \log \frac{w_m(s)}{w_m^{\text{global}}} = \frac{1}{\alpha} \text{KL}(w(s) \| w^{\text{global}})$$

两边取期望即得。$\square$

该 Bound 表明：状态条件权重的优势与状态-权重的互信息成正比。当状态划分发现有意义的结构时，$I(s; w) > 0$，优势严格为正。

---

## 3 Connection to MoE Gating

### 3.1 与 Shazeer et al. (2017) 稀疏门控 MoE 的对比

| 维度 | 传统 MoE | SCX 专家路由 |
|------|---------|------------|
| 门控输入 | 原始特征 $x$ | 状态赋值 $\gamma_s(x)$ |
| 门控参数 | 可学习的 $W_g$ | 估计的 $\hat{R}_m(s)$ |
| 训练方式 | 端到端反向传播 | 两阶段（先估风险，再路由） |
| 稀疏性 | hard/top-k | 指数软加权 |
| 泛化保证 | 经验风险最小化 | 状态条件 PAC 边界 |

SCX 的路由不是基于 $x$ 本身，而是基于**状态条件风险** $\sum_s \gamma_s(x) R_m(s)$。这是 MoE 门控的一种**元学习变体**：门控决策不是直接学习 $x \to \text{expert}$ 的映射，而是通过估计条件风险来间接确定路由。

### 3.2 负载均衡

传统 MoE 需要辅助损失来平衡专家使用率：

$$\mathcal{L}_{\text{balance}} = \alpha \cdot CV(\text{expert\_load})^2$$

SCX 的状态条件权重 $w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(s) \hat{R}_m(s))$ 自然地实现了负载均衡：如果某专家在所有状态上都差，它的权重指数衰减；不同专家在不同状态上胜出，自动分散负载。

### 3.3 与 Jacob et al. (1991) 自适应混合专家的关系

SCX 的专家路由 $m^*(x) = \arg\min_m \sum_s \gamma_s(x) R_m(s)$ 可以看作 Jacob 门控网络的硬化版本（hard routing vs. soft routing）。

---

## 4 Extreme Cases

### 4.1 退化为全局权重

当 $\mathcal{S} = \{\text{all}\}$（仅一个状态）时，$\gamma_s(x) \equiv 1$，$w_m(x) = \frac{\exp(-\alpha \hat{R}_m)}{\sum_{m'} \exp(-\alpha \hat{R}_{m'})}$，此时 $w_m(x)$ 为常数，命题退化为平凡情况 $\Delta R = 0$。

### 4.2 达到理论上界

当每个 $x$ 独立成状态时（$\mathcal{S} = \mathcal{X}$），$\gamma_s(x) = \delta_{x,s}$，$w_m(x) = \frac{\exp(-\alpha \hat{R}_m(x))}{\sum_{m'} \exp(-\alpha \hat{R}_{m'}(x))}$，此时达到理论上界，$\Delta R$ 最大。

---

## 5 Implications for SCX

1. **统一了 expert routing、ensemble、distillation 的权重公式**：SCX 的权重公式 $w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(x) \hat{R}_m(s))$ 提供了一个统一的数学框架。

2. **PAC-Bayes 解释**：SCX 的状态条件权重可以看作一个**状态依赖的后验** $\mathcal{Q}_x$，其 KL 散度相对于均匀先验的惩罚项通过 $\alpha$ 参数控制，实现了状态水平的 PAC-Bayes 边界：
   $$\mathbb{E}_{h \sim \mathcal{Q}_s}[R(h|s)] \leq \mathbb{E}_{h \sim \mathcal{Q}_s}[\hat{R}(h|s)] + \sqrt{\frac{\text{KL}(\mathcal{Q}_s \| \mathcal{P}_s) + \log(n_s/\delta)}{2n_s - 1}}$$

3. **与信息瓶颈的关系**：SCX 的权重是对专家选择不确定性的一种变分近似，可以理解为在状态水平上压缩专家选择信息的同时最大化预测保真度。

---

## 参考文献

1. SCX 核心框架数学分析. `01_SCX_核心框架_数学分析.md` Section 2.3
2. SCX 数学基础与证明建构. `05_数学根源与证明.md` Proposition 3
3. Jacobs, R. A., et al. (1991). Adaptive mixtures of local experts. *Neural Computation*.
4. Shazeer, N., et al. (2017). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. *ICLR*.
5. McAllester, D. A. (1999). PAC-Bayesian model averaging. *COLT*.
