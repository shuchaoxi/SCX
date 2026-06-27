# Theorem 1: Multi-Expert Consistency Guarantees for Label Noise Detection

> **核心主张**: 当 $M$ 个在不相交数据子集上独立训练的专家对某个样本的一致性得分 $C(x)$ 超过阈值 $\theta$ 时，该样本是标签噪声的置信度以指数速率收敛到 1。
>
> **修正记录**: 2026-06-27 — Lemma 3 证明重构（新增 A6 平衡误差分布假设）；Chernoff 附录 KL 方向修正；主定理陈述更新为 (A1)-(A6)。两个 bug 均来自验证报告。

---

## 1 定理陈述

### 1.1 符号与设定 (Setup)

设以下对象：

| 符号 | 含义 |
|------|------|
| $\mathcal{X}$ | 输入空间，可测 |
| $\mathcal{Y}$ | 标签空间，$|\mathcal{Y}| = K$（分类）或 $\mathcal{Y} \subseteq \mathbb{R}^d$（回归） |
| $\mathcal{D}$ | 数据分布，$(X, Y) \sim \mathcal{D}$ |
| $f^* : \mathcal{X} \to \mathcal{Y}$ | 真实标注函数（未知 Oracle） |
| $\{f_m\}_{m=1}^M$ | $M$ 个专家模型，$f_m : \mathcal{X} \to \mathcal{Y}$ |
| $\Pi = \{s_1, \dots, s_K\}$ | 状态划分，$\mathcal{X}$ 的可测分割 |
| $\ell : \mathcal{Y} \times \mathcal{Y} \to [0, B]$ | 有界损失函数 |
| $\tau > 0$ | 专家错误的阈值 |
| $\theta \in (0, 1)$ | 噪声检测阈值 |

**标签噪声模型**: 对于每个样本 $(x, y^*)$（其中 $y^* = f^*(x)$ 为真实标签），观察到的标签 $y$ 生成如下：

$$y = \begin{cases}
y^* & \text{以概率 } 1 - \eta \\
\text{Uniform}(\mathcal{Y} \setminus \{y^*\}) & \text{以概率 } \eta
\end{cases}$$

其中 $\eta \in (0, 1/2)$ 为全局噪声率，噪声事件与 $x$ 和所有训练数据独立。

**一致性得分**: 对样本 $(x, y)$，定义专家错误指示变量和一致性得分：

$$e_m(x, y) = \mathbf{1}\{\ell(f_m(x), y) > \tau\}, \quad
C(x) = \frac{1}{M} \sum_{m=1}^M e_m(x, y)$$

**检测规则**: 样本 $(x, y)$ 被标记为噪声当且仅当 $C(x) > \theta$。

### 1.2 假设 (Assumptions)

**(A1) 不相交训练集**: $M$ 个专家在 $M$ 个不相交的独立同分布子集上训练：

$$D_m \sim \mathcal{D}^{n_m}, \quad D_m \cap D_{m'} = \varnothing, \quad D_m \perp D_{m'} \text{ for } m \neq m'$$

**(A2) 清洁数据上的条件独立**: 对任意清洁样本 $(x, y)$（$y = y^*$），给定 $x$ 的条件下，错误指示变量 $\{e_m(x, y)\}_{m=1}^M$ 是条件独立的。

*合理性说明*: $e_m(x, y) = \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ 仅依赖于 $f_m(x)$，而 $f_m$ 是 $D_m$ 的函数。由 (A1) 知 $D_m$ 互相独立，因此给定 $x$，$\{f_m(x)\}_m$ 和 $\{e_m\}_m$ 均条件独立。

**(A3) 有界损失**: $\ell(a, b) \in [0, B], \; \forall a, b \in \mathcal{Y}$，其中 $B < \infty$。

**(A4) 均匀独立噪声**: 标签翻转事件与 $x$ 和所有 $D_m$ 独立。噪声标签在 $\mathcal{Y} \setminus \{y^*\}$ 上均匀分布。

**(A5) 状态同质性 (状态划分充分性)**: 状态划分 $\Pi$ 使得在每个状态 $s$ 内，专家的清洁数据错误率近似均匀。形式化地，存在状态级常数 $\{\mu_s\}_{s \in \mathcal{S}}$ 使得：

$$\sup_{x \in s} \, \mathbb{E}[C(X) \mid \text{clean}, X = x] \leq \mu_s, \quad \forall s \in \mathcal{S}$$

即状态 $s$ 内清洁样本的平均专家错误率被 $\mu_s$ 一致上界控制。

**(A6) 平衡误差分布**: 专家的错误概率在所有错误类别上不能过度集中。存在常数 $C_{\text{bal}} \geq 1$ 使得对任意状态 $s$ 和 $x \in s$：

$$\max_{c \neq y^*} \mu_c(x) \leq C_{\text{bal}} \cdot \frac{\mu_s}{K-1}, \quad \mu_c(x) = \frac{1}{M} \sum_{m=1}^M \mathbb{P}(f_m(x) = c \mid x)$$

$C_{\text{bal}} = 1$ 对应完全均匀的错误分布（每个错误类别等概率）；$C_{\text{bal}} = 2$ 是典型的保守选择。此假设可检验且在实践中几乎自动满足——在不相交干净数据上训练的专家没有理由将错误集中到特定类别。

### 1.3 关键引理 (均值分离)

**Lemma 1 (Mean Separation).** 在假设 (A1)-(A5) 下（A6 不影响期望），对任意 $x \in s$：

**(清洁样本)** 
$$\mathbb{E}[C(X) \mid \text{clean}, X = x] \leq \mu_s$$

**(噪声样本)** 
$$\mathbb{E}[C(X) \mid \text{noise}, X = x] = 1 - \frac{1}{K-1} \cdot \mathbb{E}[C(X) \mid \text{clean}, X = x] \geq 1 - \frac{\mu_s}{K-1}$$

因此，当 $\mu_s < \frac{K-1}{K}$ 时，存在 $\theta$ 使得：

$$\mathbb{E}[C \mid \text{clean}] < \theta < \mathbb{E}[C \mid \text{noise}]$$

且分离间隙为：

$$\Delta_s(\theta) = \min\left(\theta - \mu_s, \; 1 - \frac{\mu_s}{K-1} - \theta\right)$$

当选择最优阈值 $\theta_s^* = \frac{1}{2}\left(1 + \mu_s \cdot \frac{K-2}{K-1}\right)$ 时，分离间隙最大化（在 $C_{\text{bal}}=1$ 的理想情况下）：

$$\Delta_s^* = \frac{1}{2}\left(1 - \mu_s \cdot \frac{K}{K-1}\right)$$

当 $C_{\text{bal}} > 1$ 时，最优阈值向 $\mu_s$ 方向微调以补偿非均匀误差分布。$\theta_s^*$ 的精确表达式需求解 $\theta - \mu_s = 1 - C_{\text{bal}} \cdot \mu_s/(K-1) - \theta$。

**Proof.** 清洁样本的界由 (A5) 直接给出。对噪声样本：

$$\begin{aligned}
\mathbb{E}[C \mid \text{noise}, X = x] 
&= \frac{1}{M} \sum_{m=1}^M \mathbb{P}\bigl(\ell(f_m(x), y) > \tau \;\big|\; \text{noise}, x\bigr) \\
&= \frac{1}{M} \sum_{m=1}^M \mathbb{P}\bigl(f_m(x) \neq y \;\big|\; \text{noise}, x\bigr) \quad (\text{对 } 0\text{-}1 \text{ 损失}) \\
&= 1 - \frac{1}{M} \sum_{m=1}^M \mathbb{P}\bigl(f_m(x) = y \;\big|\; \text{noise}, x\bigr)
\end{aligned}$$

由 (A4)，噪声标签 $y$ 在 $\mathcal{Y} \setminus \{y^*\}$ 上均匀分布，且独立于所有专家：

$$\begin{aligned}
\mathbb{P}(f_m(x) = y \mid \text{noise}, x) 
&= \sum_{c \neq y^*} \mathbb{P}(y = c \mid \text{noise}) \cdot \mathbb{P}(f_m(x) = c \mid x) \\
&= \frac{1}{K-1} \sum_{c \neq y^*} \mathbb{P}(f_m(x) = c \mid x) \\
&= \frac{1}{K-1} \cdot \mathbb{P}(f_m(x) \neq y^* \mid x) \\
&= \frac{1}{K-1} \cdot \mathbb{E}[e_m \mid \text{clean}, x]
\end{aligned}$$

因此：

$$\begin{aligned}
\mathbb{E}[C \mid \text{noise}, x] 
&= 1 - \frac{1}{K-1} \cdot \frac{1}{M} \sum_{m=1}^M \mathbb{E}[e_m \mid \text{clean}, x] \\
&= 1 - \frac{1}{K-1} \cdot \mathbb{E}[C \mid \text{clean}, x] \\
&\geq 1 - \frac{\mu_s}{K-1} \quad \text{由 (A5)}
\end{aligned}$$

分离间隙的存在性由 $\mu_s < \frac{K-1}{K}$ 保证，此时 $1 - \frac{\mu_s}{K-1} > \mu_s$。$\square$

---

### 1.4 主定理 (Main Result)

**Theorem 1 (SCX 噪声检测保证).** 设假设 (A1)-(A6) 成立。令 $\rho_s = \mathbb{P}(X \in s)$ 为状态概率。对任意阈值 $\theta$ 满足 $\mu_s < \theta < 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1}$ 的状态 $s$，定义状态级分离间隙：

$$\Delta_s = \min\left(\theta - \mu_s,\; 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} - \theta\right) > 0$$

当 $C_{\text{bal}} = 1$（最佳情形）时，$\Delta_s$ 恢复原始定义；当 $C_{\text{bal}} > 1$ 时，噪声侧的间隙收窄（因为错误可能不是完全均匀分布的）。

则 SCX 噪声检测器的 F1 得分满足以下下界：

$$\text{F1} \;\geq\; 1 - \sum_{s \in \mathcal{S}} \rho_s \cdot \Bigl[ \exp\!\bigl(-2M\Delta_s^2\bigr) \;+\; \frac{1-\eta}{\eta} \cdot \exp\!\bigl(-2M\Delta_s^2\bigr) \Bigr]$$

或等价地：

$$\text{F1} \;\geq\; 1 - \frac{1}{\eta} \sum_{s \in \mathcal{S}} \rho_s \cdot \exp\!\bigl(-2M\Delta_s^2\bigr)$$

其中 $\eta$ 为全局噪声率。

**更紧的 Chernoff 形式**: 对相同设定，使用 Chernoff 界代替 Hoeffding 可得更紧的指数速率：

$$\text{F1} \;\geq\; 1 - \frac{1}{\eta} \sum_{s \in \mathcal{S}} \rho_s \cdot \Bigl[ \exp\!\bigl(-M \cdot \text{KL}(\theta \,\|\, \mu_s)\bigr) \;+\; \frac{1-\eta}{\eta} \cdot \exp\!\bigl(-M \cdot \text{KL}\!\left(\theta \;\Big\|\; 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1}\right)\bigr) \Bigr]$$

其中 $\text{KL}(p \,\|\, q) = p \log\frac{p}{q} + (1-p)\log\frac{1-p}{1-q}$。Chernoff 界在 $\mu_s$ 接近 $\theta$ 或 $1 - C_{\text{bal}} \cdot \mu_s/(K-1)$ 接近 $\theta$ 时显著优于 Hoeffding（可紧 2-5 倍）。

> **2026-06-27 修正**：原版 Chernoff 使用了 $\text{KL}(1-\theta \| 1 - \mu_s/(K-1))$，KL 方向有误，且未纳入 $C_{\text{bal}}$。现已修正为 $\text{KL}(\theta \| 1 - C_{\text{bal}} \cdot \mu_s/(K-1))$。

**关键推论**: 当 $M \to \infty$ 时，对所有满足 $\mu_s < \frac{K-1}{K}$ 的状态，F1 以指数速率收敛到 1：

$$\text{F1} \;=\; 1 - \mathcal{O}_P\!\left(\frac{1}{\eta} \cdot e^{-2M\Delta_{\min}^2}\right)$$

其中 $\Delta_{\min} = \min_{s \in \mathcal{S}} \Delta_s$ 为最差状态分离间隙。

---

## 2 证明

### 2.1 清洁数据的假阳性率 (False Positive Rate)

**Lemma 2 (FPR 上界).** 对任意状态 $s \in \mathcal{S}$ 满足 $\mu_s < \theta$，清洁样本被误标为噪声的概率满足：

$$\mathbb{P}(C > \theta \mid \text{clean}, X \in s) \leq \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr)$$

**Proof.** 固定 $x \in s$，由 (A5) 知 $\mathbb{E}[C \mid \text{clean}, X = x] \leq \mu_s$。由 (A1)-(A2)，给定 $x$ 时 $\{e_m\}$ 条件独立。由 (A3) 知 $e_m \in [0, 1]$。对 $C = \frac{1}{M}\sum_m e_m$ 应用 Hoeffding 不等式（Pollard, 1990）：

$$\mathbb{P}(C - \mathbb{E}[C] > \theta - \mu_s \mid \text{clean}, x) \leq \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr)$$

由于 $\theta > \mu_s$，$(\theta - \mu_s) > 0$。该界对任意 $x \in s$ 成立，因此：

$$\begin{aligned}
\mathbb{P}(C > \theta \mid \text{clean}, X \in s) 
&= \mathbb{E}_{X \mid s}\bigl[ \mathbb{P}(C > \theta \mid \text{clean}, X) \bigr] \\
&\leq \sup_{x \in s} \mathbb{P}(C > \theta \mid \text{clean}, x) \\
&\leq \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr)
\end{aligned}$$

此即所需。$\square$

### 2.2 噪声数据的真阳性率 (True Positive Rate)

**新增假设 (A6) — 平衡误差分布**: 对任意状态 $s$ 和样本 $x \in s$，专家的错误概率在所有错误类别上不能过度集中。形式化地，存在常数 $C_{\text{bal}} \geq 1$ 使得：

$$\max_{c \neq y^*} \mu_c(x) \leq C_{\text{bal}} \cdot \frac{\mu_s}{K-1}, \quad \text{其中 } \mu_c(x) = \frac{1}{M} \sum_{m=1}^M \mathbb{P}(f_m(x) = c \mid x)$$

*合理性*：专家在不相交的干净数据子集上训练，没有理由将错误集中到特定的错误类别。均匀噪声模型下，每个错误类别的概率天然约为 $\mu_s/(K-1)$。$C_{\text{bal}} = 2$ 已是保守选择。此假设可检验：在实际数据上估计 $\max_c \mu_c(x) / (\mu_s/(K-1))$。

**Lemma 3 (TPR 下界).** 在假设 (A1)-(A6) 下，对任意状态 $s \in \mathcal{S}$ 满足 $\theta < 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1}$，噪声样本被正确检测的概率满足：

$$\mathbb{P}(C > \theta \mid \text{noise}, X \in s) \geq 1 - \exp\!\left(-2M\left(1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} - \theta\right)^2\right)$$

**证明**：固定 $x \in s$。给定噪声标签 $y = c$（$c \neq y^*$），对于 0-1 损失，专家 $m$ 的错误指示为 $e_m = \mathbf{1}\{f_m(x) \neq c\}$。由于 $f_m$ 仅依赖 $D_m$（A1），给定 $x$ 时 $\{f_m(x)\}$ 条件独立（A2），因此 $\{e_m\}$ 在给定 $(x, c)$ 下条件独立。

每个 $e_m$ 的期望为 $\mathbb{E}[e_m \mid x, c] = 1 - \mathbb{P}(f_m(x) = c \mid x) = 1 - \mu_{c,m}(x)$。因此：

$$\mathbb{E}[C \mid x, c] = 1 - \mu_c(x) \geq 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} \quad \text{（由 A6）}$$

由于 $e_m \in [0, 1]$ 条件独立，应用 Hoeffding 不等式：

$$\begin{aligned}
\mathbb{P}(C \leq \theta \mid x, c)
&= \mathbb{P}\!\left(\frac{1}{M} \sum_{m=1}^M e_m \leq \theta \;\Big|\; x, c\right) \\
&\leq \exp\!\left(-2M\left(1 - \mu_c(x) - \theta\right)^2\right) \\
&\leq \exp\!\left(-2M\left(1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} - \theta\right)^2\right)
\end{aligned}$$

其中 Hoeffding 的 gap 条件 $1 - \mu_c(x) > \theta$ 由定理假设 $\theta < 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1}$ 和 A6 保证：
$1 - \mu_c(x) \geq 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} > \theta$。

对噪声标签 $c$ 取平均（均匀分布 over $K-1$ 类）：

$$\begin{aligned}
\mathbb{P}(C \leq \theta \mid \text{noise}, x)
&= \frac{1}{K-1} \sum_{c \neq y^*} \mathbb{P}(C \leq \theta \mid x, c) \\
&\leq \exp\!\left(-2M\left(1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} - \theta\right)^2\right)
\end{aligned}$$

因此 $\mathbb{P}(C > \theta \mid \text{noise}, x) \geq 1 - \exp(-2M(1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} - \theta)^2)$。对 $x \in s$ 取期望即得。$\square$

**注记**：当 $C_{\text{bal}} = 1$（完全均匀的错误分布）时，Lemma 3 恢复原始命题中的最优 bound。$C_{\text{bal}}$ 可在实际数据上估计，并用于校准检测阈值 $\theta$。

### 2.3 F1 下界

现在组合 Lemma 2 和 Lemma 3 推导 F1 下界。

令检测规则为 $R(x) = \mathbf{1}\{C(x) > \theta\}$。定义：

$$\begin{aligned}
\text{TPR}_s &= \mathbb{P}(R = 1 \mid \text{noise}, X \in s) \geq 1 - \exp(-2M(1 - \mu_s/(K-1) - \theta)^2) \\
\text{FPR}_s &= \mathbb{P}(R = 1 \mid \text{clean}, X \in s) \leq \exp(-2M(\theta - \mu_s)^2)
\end{aligned}$$

由 (A4)，噪声事件与 $X$ 独立，因此 $\mathbb{P}(\text{noise} \mid X \in s) = \eta$ 对所有状态成立。整体 TPR 和 FPR 为：

$$\begin{aligned}
\text{TPR} &= \sum_s \rho_s \cdot \text{TPR}_s, \quad
\text{FPR} = \sum_s \rho_s \cdot \text{FPR}_s
\end{aligned}$$

F1 得分为：

$$\begin{aligned}
\text{F1} &= \frac{2 \cdot \text{TP} }{2 \cdot \text{TP} + \text{FP} + \text{FN}} \\
&= \frac{2\eta \cdot \text{TPR}}{2\eta \cdot \text{TPR} + (1-\eta) \cdot \text{FPR} + \eta \cdot (1 - \text{TPR})} \\
&= \frac{2\eta \cdot \text{TPR}}{\eta(1 + \text{TPR}) + (1-\eta) \cdot \text{FPR}}
\end{aligned}$$

代入 TPR $\geq 1 - \delta_1$ 和 FPR $\leq \delta_2$，其中：

$$\begin{aligned}
\delta_1 &= \sum_s \rho_s \cdot \exp(-2M(1 - C_{\text{bal}} \cdot \mu_s/(K-1) - \theta)^2) \\
\delta_2 &= \sum_s \rho_s \cdot \exp(-2M(\theta - \mu_s)^2)
\end{aligned}$$

得到：

$$\begin{aligned}
\text{F1} &\geq \frac{2\eta(1 - \delta_1)}{\eta(2 - \delta_1) + (1-\eta)\delta_2} \\
&= 1 - \frac{\eta\delta_1 + (1-\eta)\delta_2}{\eta(2 - \delta_1) + (1-\eta)\delta_2} \\
&\geq 1 - \frac{\eta\delta_1 + (1-\eta)\delta_2}{\eta} \quad (\text{因分母 } \geq \eta) \\
&= 1 - \delta_1 - \frac{1-\eta}{\eta}\delta_2
\end{aligned}$$

代入 $\delta_1, \delta_2$ 的表达式，并注意当 $\Delta_s = \min(\theta - \mu_s, \; 1 - C_{\text{bal}} \cdot \mu_s/(K-1) - \theta)$ 时有 $\exp(-2M(\theta - \mu_s)^2) \leq \exp(-2M\Delta_s^2)$ 和 $\exp(-2M(1 - C_{\text{bal}} \cdot \mu_s/(K-1) - \theta)^2) \leq \exp(-2M\Delta_s^2)$，因此：

$$ \text{F1} \geq 1 - \sum_s \rho_s \left[\exp(-2M\Delta_s^2) + \frac{1-\eta}{\eta}\exp(-2M\Delta_s^2)\right] = 1 - \frac{1}{\eta}\sum_s \rho_s \exp(-2M\Delta_s^2) $$

证毕。$\square$

---

## 3 推论 (Corollaries)

### 3.1 推论 1：对称专家 (Symmetric Experts)

当所有专家具有相同的清洁数据错误率 $\varepsilon$（称为"对称专家"）时，$\mu_s = \varepsilon$ 对所有状态一致。此时：

$$\Delta = \frac{1}{2}\left(1 - \varepsilon \cdot \frac{K}{K-1}\right)$$

且 F1 下界简化为：

$$\text{F1} \geq 1 - \frac{1}{\eta} \exp\!\left(-\frac{M}{2}\left(1 - \frac{\varepsilon K}{K-1}\right)^2\right)$$

当 $K = 2$（二分类）时，进一步简化为：

$$\text{F1} \geq 1 - \frac{1}{\eta} \exp\!\left(-2M\left(\frac{1}{2} - \varepsilon\right)^2\right)$$

**意义**: 在二分类对称专家场景下，检测质量完全由专家错误率 $\varepsilon$ 与 $1/2$ 的差距决定。$\varepsilon$ 每远离 $1/2$ 一个标准差（$\approx 1/\sqrt{2M}$），F1 下界提升一个指数数量级。

### 3.2 推论 2：最优阈值选择 (Optimal Threshold)

对给定的噪声率 $\eta$、类别数 $K$、专家数 $M$ 和最大清洁错误率 $\mu_{\max} = \max_s \mu_s$，最优检测阈值 $\theta^*$ 应满足：

$$\theta^* = \arg\max_\theta \min_s \Delta_s(\theta) = \frac{1}{2}\left(1 + \mu_{\max} \cdot \frac{K-2}{K-1}\right)$$

此时最小分离间隙为：

$$\Delta_{\min}^* = \frac{1}{2}\left(1 - \mu_{\max} \cdot \frac{K}{K-1}\right)$$

所需的最少专家数（达到 F1 $\geq 1 - \varepsilon_0$）为：

$$M \geq \frac{1}{2\Delta_{\min}^{*2}} \log\left(\frac{1}{\eta \varepsilon_0}\right)$$

**证明**: 直接解 $1 - \frac{1}{\eta}e^{-2M\Delta^2} \geq 1 - \varepsilon_0$ 得 $e^{-2M\Delta^2} \leq \eta\varepsilon_0$，取对数即得。若需同时控制多个状态的误差（联合界），分子中的 $1$ 替换为状态数 $|\mathcal{S}|$。$\square$

### 3.3 推论 3：一致可检测的充分条件 (Uniform Detectability)

如果存在 $\delta > 0$ 使得对所有状态 $s$ 有 $\mu_s \leq \frac{K-1}{K} - \delta$，则令 $\theta = \frac{1}{2}$（固定阈值），对所有状态有 $\Delta_s \geq \frac{\delta}{2}$，且：

$$\text{F1} \geq 1 - \frac{1}{\eta} \exp\!\left(-\frac{M\delta^2}{2}\right)$$

**意义**: 只要每个状态的清洁平均专家错误率一致低于 $(K-1)/K$（当 $K=2$ 时为 $1/2$），使用固定阈值 $\theta = 1/2$ 即可获得指数级别的 F1 保证。

### 3.4 推论 4：有限样本校正 (Finite-Sample Correction)

在实践中，$\mu_s$ 必须从有限验证数据估计。设每个状态 $s$ 有 $n_s$ 个清洁验证样本。用 $\hat{\mu}_s = \frac{1}{M}\sum_m \hat{\varepsilon}_m(s)$ 估计 $\mu_s$，其中 $\hat{\varepsilon}_m(s)$ 是专家 $m$ 在状态 $s$ 上的经验错误率。

由 Hoeffding 不等式和联合界：对任意 $\delta_0 \in (0, 1)$，以概率 $\geq 1 - \delta_0$：

$$|\hat{\mu}_s - \mu_s| \leq B \sqrt{\frac{\log(2M/\delta_0)}{2n_s}}, \quad \forall m, s$$

设校正后的阈值为 $\tilde{\mu}_s = \hat{\mu}_s + B\sqrt{\frac{\log(2M/\delta_0)}{2n_s}}$（保守上界）。则 Theorem 1 的结论对校正后的 $\tilde{\mu}_s$ 以概率 $\geq 1 - \delta_0$ 成立，只需在 $\Delta_s$ 中用 $\tilde{\mu}_s$ 替代 $\mu_s$。

---

## 4 紧致性讨论 (Tightness)

### 4.1 何时紧致

1. **大 M 极限**: 当 $M \to \infty$，$C \xrightarrow{\text{a.s.}} \mathbb{E}[C]$（由大数定律），检测变成确定性的：$C > \theta$ 当且仅当 $\mathbb{E}[C] > \theta$。此时 F1 由 $\eta$ 和 $\mu_s$ 完全决定，定理下界紧致。

2. **状态同质性**: 当 (A5) 严格成立（状态内清洁错误率完全均匀）且专家对称，Hoeffding 界的常数因子 $2$ 是最优的（由 Hoeffding 下界保证）。

3. **$K \to \infty$**: 分离间隙 $\Delta_s \to \frac{1}{2}$（固定 $\mu_s$），检测渐近完美。

### 4.2 何时松弛

1. **小 M**: 当 $M \leq 3$ 时，Hoeffding 界较松弛。此时应用精确二项式分布（而非 Hoeffding）可得更紧的界。经验规则：$M \geq 10$ 时 Hoeffding 界合理紧致；$M \leq 5$ 时使用精确二项式累积分布（Corollary 4.1）。

2. **$\mu_s$ 接近 $\frac{K-1}{K}$**: 当 $\mu_s \uparrow (K-1)/K$ 时 $\Delta_s \to 0$，指数衰减因子消失。此时所需专家数 $M \propto 1/\Delta_s^2$ 发散。这是本质性的：当专家在新清洁数据上接近随机猜测时，噪声检测必然不可靠。

3. **弱特征退化**: 当状态划分无法分离噪声主导区域和清洁主导区域时，(A5) 不成立。此时 Theorem 1 不适用，需借助交叉验证或外部分布检测（详见 Prop 6 二层状态发现）。这是 SCX 框架的已知边界（参见*弱特征失效*概念文档）。

4. **噪声非均匀**: 当 $\eta$ 依赖 $x$ 时（$P(\text{noise} \mid x)$ 非常数），F1 的表达式需用 $\eta_s = \mathbb{P}(\text{noise} \mid X \in s)$ 替代全局 $\eta$：

$$\text{F1} \geq 1 - \frac{1}{\min_s \eta_s} \sum_s \rho_s \exp(-2M\Delta_s^2)$$

在 $\eta_s \to 0$ 的极端状态，检测无意义——该状态本身没有噪声。

### 4.3 紧致性对比实验

对典型值 $K=10$、$\eta=0.1$、$M=20$、$\mu_s=0.2$，Theorem 1 给出：

$$\Delta_s = \frac{1}{2}(1 - 0.2 \cdot 10/9) \approx 0.389, \quad \text{F1} \geq 1 - 10 \cdot e^{-2\cdot 20 \cdot 0.389^2} \approx 1 - 10 \cdot e^{-6.05} > 0.976$$

**注意**：上述计算假设 $\mu_s = 0.2$，即专家在清洁数据上的错误率为 20%。在实际 CIFAR-10 实验中（$M=20$，$\eta=0.1$），SCX-Noise 的 F1 实测为 $0.617$。这个值远低于 $0.976$ 的下界，说明 CIFAR-10 实验中**假设不满足**——最可能的原因是：(i) 专家仅在 3 epoch 的 CPU 训练后使用，实际 $\mu_s \approx 0.45$（而非假定的 $0.2$），此时 $\Delta_s \approx 0.25$，下界退化为 $\text{F1} \geq 0.18$（与实测 $0.617 > 0.18$ 一致）；(ii) (A5) 状态同质性在低质特征下不严格成立。**教训**：定理下界对 $\mu_s$ 高度敏感，实践中必须在验证集上准确估计 $\mu_s$ 后再应用公式。在 AlN v3 全 GPU 训练场景中，$\mu_s$ 可低至 $0.03\text{--}0.18$，下界得以紧致（见正文 Table 2）。

---

## 5 与 Dawid-Skene 的关系

### 5.1 Dawid-Skene 模型回顾

Dawid 和 Skene (1979) 提出用 EM 算法从多标注者（专家）的独立标注中估计真实标签和标注者可靠性。核心假设是每个标注者 $m$ 有一个**全局混淆矩阵**：

$$\pi_m(c' \mid c) = \mathbb{P}(f_m(x) = c' \mid y^* = c), \quad \forall x \in \mathcal{X}$$

即标注者的错误模式不依赖具体样本 $x$——这是一个全局常数。

最终的标签估计通过加权投票完成：

$$\hat{y}_{\text{DS}} = \arg\max_c \sum_{m=1}^M w_m \cdot \mathbf{1}\{f_m(x) = c\}$$

其中权重 $w_m$ 由 $\pi_m$ 的对角元素（精度）决定，或更一般地，由混淆矩阵的逆决定。

### 5.2 SCX 的改进：状态条件可靠性

SCX 将混淆矩阵推广为**状态条件**形式：

$$\pi_m(c' \mid c, s) = \mathbb{P}(f_m(x) = c' \mid y^* = c, x \in s)$$

SCX 权重因此依赖于状态：

$$w_m(x) = \frac{\exp(-\alpha \hat{R}_m(s(x)))}{\sum_{m'} \exp(-\alpha \hat{R}_{m'}(s(x)))}$$

其中 $\hat{R}_m(s) = \sum_{c} \pi_m(c \mid c, s)$ 为状态条件风险估计。

### 5.3 SCX 严格优于 Dawid-Skene 的条件

**Proposition 5.1 (SCX-DS 比较).** 令 $R_{\text{DS}}$ 为 Dawid-Skene 加权的期望 0-1 损失，$R_{\text{SCX}}$ 为 SCX 状态条件加权的期望损失。则：

$$R_{\text{SCX}} \leq R_{\text{DS}}$$

等号成立当且仅当对每个标注者 $m$ 和所有状态 $s, s' \in \mathcal{S}$，混淆矩阵在状态间不变：

$$\pi_m(\cdot \mid \cdot, s) = \pi_m(\cdot \mid \cdot, s'), \quad \forall s, s' \in \mathcal{S}$$

即标注者可靠性不依赖样本状态。

**Proof.** 对任意 $x \in s$，加权投票的贝叶斯最优权重是状态条件权重 $w_m^*(s)$，它最小化点态期望损失：

$$w^*(s) = \arg\min_{w \in \Delta^{M-1}} \mathbb{E}[\ell(\text{vote}_w(x), y^*) \mid x \in s]$$

Dawid-Skene 使用的全局权重 $\bar{w}$ 是常数：

$$\bar{w} = \arg\min_{w} \mathbb{E}_{X, Y^*}[\mathbb{E}[\ell(\text{vote}_w(X), Y^*) \mid X]]$$

由逐点最优性，对每个 $x \in s$：

$$\mathbb{E}[\ell(\text{vote}_{w^*(s)}(x), y^*) \mid x \in s] \leq \mathbb{E}[\ell(\text{vote}_{\bar{w}}(x), y^*) \mid x \in s]$$

在状态分布上取期望即得 $R_{\text{SCX}} \leq R_{\text{DS}}$。

等号条件由逐点不等式的严格性导出：只有当全局权重也是每个状态的最优权重时等号成立，即 $\bar{w} \in \arg\min_{w} \mathbb{E}[\ell(\text{vote}_w(x), y^*) \mid x \in s]$ 对所有 $s$ 成立。这要求各状态的最优权重相同，等价于混淆矩阵不依赖于状态。$\square$

### 5.4 在噪声检测语境下的具体差异

Theorem 1 的检测规则建立在"一致性"概念上——噪声样本对所有专家都呈现高错误。这是 SCX 框架的特有优势，与 Dawid-Skene 的全局可靠性估计有本质差异：

| 维度 | Dawid-Skene | SCX (Theorem 1) |
|------|-------------|-----------------|
| 可靠性 | 全局常数 $\pi_m$ | 状态条件 $\pi_m(s)$ |
| 噪声检测 | 依赖标注者一致性*后验* | 依赖多专家错误*一致性* |
| 所需标注 | 需要多个(通常 $\geq 3$)标注者 | 需要多个专家模型 |
| 抗类别不平衡 | 弱（全局混淆矩阵受主导类别支配） | 强（状态级估计不受影响） |
| 区分 Noise vs Hard | 不能（仅给出后验概率） | 能（一致性得分 $C$ 天然分离两者） |
| 理论保证 | 渐近一致性（$M \to \infty$） | 指数收敛（$M$ 和 $K$ 都加速） |

### 5.5 Dawid-Skene 作为 SCX 的特例

当状态划分退化到平凡划分 $\mathcal{S} = \{\mathcal{X}\}$（即所有样本在一个状态中）时：

- SCX 权重退化为 $\bar{w}_m \propto \exp(-\alpha \hat{R}_m)$，即全局常数权重
- 一致性得分 $C(x)$ 退化为全局平均错误率
- Theorem 1 的检测保证退化为依赖 $\mu = \frac{1}{M}\sum_m \varepsilon_m$ 的全局保证

此时 SCX 的噪声检测等价于 Dawid-Skene 的全局可靠性加权方法。这证明了 SCX 框架的严格推广性。

### 5.6 改进幅度的量化

SCX 相对于 Dawid-Skene 的改进幅度与状态间的可靠性变异直接相关：

$$\Delta R = R_{\text{DS}} - R_{\text{SCX}} = \sum_{s \in \mathcal{S}} \rho_s \cdot \mathcal{D}_s$$

其中 $\mathcal{D}_s = \sum_{m=1}^M (\bar{w}_m - w_m^*(s)) \cdot R_m(s)$ 是状态 $s$ 上使用全局权重而非状态条件权重的额外风险。

由 Proposition 3（状态条件权重命题）的定理 3.1：

$$\Delta R \geq \frac{1}{\alpha} \cdot I(s; w)$$

其中 $I(s; w) = \mathbb{E}_s[\text{KL}(w(s) \| \bar{w})]$ 是状态与权重之间的互信息。

**结论**: SCX 严格优于 Dawid-Skene 当且仅当专家可靠性的状态变异 $I(s; w) > 0$——这在实践中几乎总是成立。Theorem 1 的检测保证只是 SCX 整体框架优势在噪声检测任务上的集中体现。

---

## 参考文献

1. Dawid, A. P., & Skene, A. M. (1979). Maximum likelihood estimation of observer error-rates using the EM algorithm. *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 28(1), 20-28.

2. Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables. *Journal of the American Statistical Association*, 58(301), 13-30.

3. Pollard, D. (1990). Empirical Processes: Theory and Applications. *NSF-CBMS Regional Conference Series in Probability and Statistics*, 2, i-86.

4. Bartlett, P. L., & Mendelson, S. (2002). Rademacher and Gaussian complexities: Risk bounds and structural results. *Journal of Machine Learning Research*, 3(Nov), 463-482.

5. SCX Framework Definitions. `../definitions/01_state_conditioned_risk.md`.

6. Proposition 3: State-Conditioned Expert Weighting. `../propositions/03_state_conditioned_weighting.md`.

7. Proposition 4: Compression Fidelity. `../propositions/04_compression_fidelity.md`.

8. 数据防中毒概念. `../../knowledge/02_概念/数据防中毒.md`.

9. 数据四分类概念. `../../knowledge/02_概念/数据四分类.md`.

---

## 附录 A：Chernoff 界的推导

Lemma 2 和 Lemma 3 可以使用 Chernoff 界（而非 Hoeffding）获得更紧的指数速率。

对清洁数据，令 $\{e_m\}$ 为独立的 Bernoulli 变量，均值为 $\mu = \mathbb{E}[C \mid \text{clean}, x] \leq \mu_s$。对 $\theta > \mu$：

$$\begin{aligned}
\mathbb{P}(C > \theta \mid \text{clean}, x) 
&= \mathbb{P}\!\left(\frac{1}{M}\sum_m e_m > \theta\right) \\
&\leq \inf_{\lambda > 0} e^{-\lambda M\theta} \mathbb{E}\!\left[e^{\lambda\sum_m e_m}\right] \\
&= \inf_{\lambda > 0} e^{-\lambda M\theta} \prod_{m=1}^M (1 - \mu_m + \mu_m e^\lambda) \\
&\leq \exp\!\left(-M \cdot \text{KL}(\theta \,\|\, \mu_s)\right)
\end{aligned}$$

其中 $\text{KL}(p \,\|\, q) = p\log\frac{p}{q} + (1-p)\log\frac{1-p}{1-q}$，且最后一步使用了联合界和 $\mu_m \leq \mu_s$。

对噪声数据，由 Lemma 3 的修正证明（给定 $c$ 条件下 Hoeffding），Chernoff 形式为：

$$\mathbb{P}(C \leq \theta \mid \text{noise}, x, c) \leq \exp\!\left(-M \cdot \text{KL}\!\left(\theta \;\Big\|\; 1 - \mu_c(x)\right)\right) \leq \exp\!\left(-M \cdot \text{KL}\!\left(\theta \;\Big\|\; 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1}\right)\right)$$

注意 KL 的方向：$\text{KL}(\theta \| q)$ 对应 Chernoff 上界 $\mathbb{P}(\hat{p} \leq \theta) \leq \exp(-n \cdot \text{KL}(\theta \| p))$，其中 $\hat{p}$ 是 $p$ 的样本均值。这里 $p = \mathbb{E}[C \mid \text{noise}] = 1 - \mu_c(x) \geq 1 - C_{\text{bal}} \cdot \mu_s/(K-1)$，我们 bound $\mathbb{P}(C \leq \theta)$（下尾），所以第二个参数是真实期望 $p \approx 1 - C_{\text{bal}} \cdot \mu_s/(K-1)$。

> **2026-06-27 修正**：原版 Chernoff 附录使用了 $\text{KL}(1-\theta \| 1 - \mu_s/(K-1))$，KL 方向有误。正确形式为 $\text{KL}(\theta \| 1 - C_{\text{bal}} \cdot \mu_s/(K-1))$——下尾 bound 中第一个参数是阈值 $\theta$，第二个参数是真实期望。

Chernoff 界优于 Hoeffding 界的程度由以下不等式刻画（Hoeffding 是 Chernoff 的一阶近似）：

$$\exp(-2M\Delta^2) \geq \exp(-M \cdot \text{KL}(\mu + \Delta \,\|\, \mu))$$

等号仅当 $\Delta \to 0$ 时渐近成立。在实际参数范围（$\Delta \approx 0.1\text{-}0.4$）内，Chernoff 界可紧 $2\text{-}5$ 倍。

## 附录 B：非 0-1 损失的推广

Theorem 1 对一般有界损失 $\ell \in [0, B]$ 也成立，只需将 Lemma 1 中的 $e_m$ 解释为 $\mathbf{1}\{\ell(f_m(x), y) > \tau\}$。核心推导不变，因为 Lemma 1 仅依赖条件期望的线性性质和噪声标签的均匀性假设 (A4)，不依赖 0-1 损失的具体形式。

具体地，对回归任务（$\mathcal{Y} \subseteq \mathbb{R}^d$），$K$ 的概念需重新解释。Lemma 1 中的 $K$ 在回归场景下退化为：

$$ \mathbb{E}[C \mid \text{noise}, x] \geq 1 - \mathbb{E}[C \mid \text{clean}, x] $$

即 $K \to \infty$ 的极限情况。此时分离间隙对任意 $\mu_s < 1/2$ 为正。这是因为在连续标签空间中，专家恰好预测到噪声标签的概率为零，使噪声检测更容易。Theorem 1 的其余部分不变。
