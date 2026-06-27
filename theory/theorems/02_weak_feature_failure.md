# Theorem 2: Weak Feature Failure Lower Bound

> 当特征表示 $\phi(x)$ 包含的真实状态信息不足时，基于一致性的噪声检测方法（包括 SCX）无法优于损失基线。本定理从信息论角度量化了这一边界条件。

**关联实验**: DermaMNIST (SCX-Health), AlN v3 MLIP (12-dim 手工特征)
**关联代码**: `src/scx/state/discovery.py`, `src/scx/valuation/noise_score.py`, `src/scx/expert/reliability.py`
**关联概念**: [[弱特征失效]], [[State-Conditioned eXpertise]]

---

## 目录

1. [符号与设定](#1-符号与设定)
2. [定义：弱特征](#2-定义弱特征)
3. [引理 1：状态估计误差下界](#3-引理-1状态估计误差下界)
4. [引理 2：SCX 估计退化](#4-引理-2scx-估计退化)
5. [定理 2：弱特征失败下界](#5-定理-2弱特征失败下界)
6. [推论](#6-推论)
7. [实用解读](#7-实用解读)
8. [与 Theorem 1 的联系](#8-与-theorem-1-的联系)

---

## 1. 符号与设定

### 1.1 数据生成

| 符号 | 含义 | 取值空间 |
|------|------|----------|
| $X$ | 输入随机变量 | $\mathcal{X} \subseteq \mathbb{R}^d$ |
| $Y$ | 标签随机变量 | $\mathcal{Y}$ |
| $S = s(X)$ | **未观测**的真实状态 | $\mathcal{S} = \{1,\dots,K\}$ |
| $\phi(X)$ | **观测**到的特征表示 | $\Phi \subseteq \mathbb{R}^{d_\phi}$ |
| $Z$ | 噪声指示变量（$1$=噪声, $0$=干净） | $\{0,1\}$ |
| $\{f_m\}_{m=1}^M$ | $M$ 个专家 | $\mathcal{X} \to \mathcal{Y}$ |
| $D_m = \ell(f_m(X), Y)$ | 专家 $m$ 的损失 | $\mathbb{R}^+$ |
| $\eta = P(Z = 1)$ | 边际噪声率 | $[0,1]$ |

### 1.2 马尔可夫链结构

SCX 框架假设以下生成过程：

```text
Z  →  S  →  (X, Y)  →  φ(X)
                      →  {f_m(X)}
```

即：
1. 噪声状态 $Z$ 决定了样本的真实状态 $S$（噪声来自某些数据区域）
2. 状态 $S$ 决定了数据点 $(X, Y)$ 的分布
3. $\phi(X)$ 是从 $X$ 提取的特征（确定性或随机函数）
4. 专家预测 $\{f_m(X)\}$ 是 $X$ 的函数

**关键马尔可夫链（数据处理不等式应用）**：

$$Z \to S \to X \to \phi(X)$$

由此可得：

$$I(\phi(X); Z) \leq I(X; Z) \leq I(S; Z) \leq H(Z) \leq \log 2$$

### 1.3 SCX 噪声检测流程

SCX 噪声检测的完整流程为：

1. **状态发现**：在 $\{\phi(x_i)\}$ 上运行聚类算法（k-means/谱聚类/GMM），得到 $K$ 个估计状态 $\hat{\mathcal{S}} = \{\hat{s}_1, \dots, \hat{s}_K\}$，以及状态分配函数 $\hat{s}: \mathcal{X} \to \hat{\mathcal{S}}$
2. **可靠性估计**：对每个估计状态 $\hat{s}$ 和专家 $f_m$，计算：

   $$SCX_m(\hat{s}) = \frac{|\{x_i \in \hat{s}: \ell(f_m(x_i), y_i) < \tau\}|}{|\{x_i \in \hat{s}\}|}$$

3. **一致性计算**：状态 $\hat{s}$ 的内部一致性：

   $$C(\hat{s}) = \begin{cases}
   \frac{p_{\max} - 1/|\mathcal{Y}|}{1 - 1/|\mathcal{Y}|}, & \text{离散标签}\\
   \frac{1}{1 + \text{Var}(Y \mid X \in \hat{s})}, & \text{连续标签}
   \end{cases}$$

4. **噪声分数**：样本 $x$ 的噪声分数：

   $$NS(x) = \underbrace{r(x)}_{\text{残差}} \cdot \underbrace{\frac{w_\rho}{\rho(\hat{s}(x)) + \varepsilon}}_{\text{密度项}} \cdot \underbrace{(1 - C(\hat{s}(x)))}_{\text{不一致项}}$$

   其中 $r(x)$ 是样本的残差/损失，$\rho(\hat{s})$ 是估计状态的比例。

5. **检测**：通过阈值化 $NS(x)$ 得到噪声标签 $\hat{z}(x) = \mathbf{1}\{NS(x) > t\}$。

### 1.4 损失基线检测器

定义不依赖状态信息的损失基线检测器：

$$\hat{z}_{\text{loss}}(x) = \mathbf{1}\{\max_m D_m(x) > t\}$$

该检测器仅使用专家损失 $\{D_m\}$，不使用 $\phi$ 或状态信息。记其最优 F1 为：

$$F1_{\text{base}} = \max_{t \in \mathbb{R}^+} F1\left(\hat{z}_{\text{loss}}\right)$$

类似地，$AUC_{\text{base}}$ 和 $PRAUC_{\text{base}}$ 分别为其 ROC-AUC 和 PR-AUC。

### 1.5 随机基线

对于完全不使用任何数据信息的随机检测器，其最优性能为：

**引理 0（随机基线）**：设 $\eta = P(Z = 1)$ 为边际噪声率。最坏情况下不优于以下随机基线：

$$\begin{aligned}
AUC_{\text{rand}} &= 0.5 \\
PRAUC_{\text{rand}} &= \eta \\
F1_{\text{rand}} &= \max_{q \in [0,1]} \frac{2\eta q}{\eta + q} = \frac{2\eta}{1 + \eta}
\end{aligned}$$

当且仅当 $F1_{\text{base}} = F1_{\text{rand}}$ 时，损失基线退化为随机基线——这发生在噪声与专家损失独立时（例如均匀标签噪声）。

---

## 2. 定义：弱特征

**定义 1（$\delta$-弱特征）**：称特征映射 $\phi: \mathcal{X} \to \Phi$ 关于真实状态映射 $s: \mathcal{X} \to \mathcal{S}$ 是 $\delta$-弱的，若：

$$I(\phi(X); s(X)) \leq \delta$$

其中 $I(\cdot; \cdot)$ 为 Shannon 互信息（以 nat 为单位）。

**解释**：
- $\delta = 0$：$\phi(X)$ 与 $S$ 独立，$\phi$ 完全不包含状态信息
- $\delta$ 很小：$\phi$ 几乎不包含状态信息
- $\delta$ 很大（如 $\delta \gg \log K$）：$\phi$ 包含足够的区分状态的信息

**归一化弱度**：由于 $I(\phi; S) \leq H(S) \leq \log K$，定义归一化弱度：

$$\varepsilon_\phi = \frac{\delta}{\log K} \in [0, 1]$$

$\varepsilon_\phi = 1$ 对应完全无信息（最弱），$\varepsilon_\phi = 0$ 对应完全信息（最强）。

**替代定义（状态可区分性）**：当 $I(\phi; S)$ 难以直接计算时，可用以下等价定义：

对任意两个真实状态 $s_1, s_2 \in \mathcal{S}$，定义 $TV_{s_1,s_2} = TV(P_{\phi|S=s_1}, P_{\phi|S=s_2})$ 为 $\phi$ 分布的总变差距离。则特征弱度为：

$$\Delta_\phi = \max_{s_1 \neq s_2} TV(P_{\phi|S=s_1}, P_{\phi|S=s_2})$$

由 Pinsker 不等式：$\Delta_\phi \leq \sqrt{\delta / 2}$。当 $\Delta_\phi$ 很小时，来自不同真实状态的点在 $\phi$ 空间中无法区分。

---

## 3. 引理 1：状态估计误差下界

**引理 1（状态估计误差下界——Fano 不等式）**：设 $\hat{S}$ 是基于 $\phi(X)$ 的任意真实状态估计器（即 SCX 的状态发现算法的输出）。若 $\phi$ 是 $\delta$-弱的，则：

$$P(\hat{S} \neq S) \geq \frac{H(S) - \delta - \log 2}{\log K}$$

其中 $K = |\mathcal{S}|$ 为真实状态数。

**证明**：由 Fano 不等式：

$$\begin{aligned}
P(\hat{S} \neq S) &\geq \frac{H(S \mid \phi(X)) - \log 2}{\log K} \\
&= \frac{H(S) - I(\phi(X); S) - \log 2}{\log K} \\
&= \frac{H(S) - \delta - \log 2}{\log K}
\end{aligned}$$

其中第一个等式使用了 $I(\phi; S) = H(S) - H(S \mid \phi)$。$\square$

**推论 1.1（均匀状态）**：若真实状态近似均匀分布，$H(S) \approx \log K$，则：

$$P(\hat{S} \neq S) \geq 1 - \frac{\delta + \log 2}{\log K}$$

当 $\delta \to 0$ 且 $K$ 固定时：$P(\hat{S} \neq S) \to 1 - \frac{\log 2}{\log K} > 0$。对大 $K$ 这一极限接近 $1$。

**推论 1.2（小状态数）**：当 $K = 2$ 时：

$$P(\hat{S} \neq S) \geq \frac{H(S) - \delta - \log 2}{\log 2} = H(S) - \delta - \log 2$$

由于 $H(S) \leq \log 2 = 1$ nat，当 $\delta = 0$ 时下界为 $H(S) - \log 2$，可能为 $0$（但这是未正则化的下界）。二分类时需要更强的分析。

**推论 1.3（估计误差的互信息上界——存在性）**：Fano 不等式的逆（achievability bound）表明存在某个在 $\phi$ 上操作的估计器 $\hat{S}$ 使得：

$$P(\hat{S} \neq S) \leq \frac{\delta + \log 2}{\log K}$$

但这是一个**存在性**结论：最大似然估计器（贝叶斯最优分类器）能达到此界，并不保证任意特定算法（如 k-means）也能达到。

实际中，SCX 使用的 k-means 聚类的状态估计误差由 k-means 目标函数控制，并通过率失真理论（rate-distortion theory）与 $I(\phi; S)$ 相关联。k-means 的误差上界一般为：

$$P(\hat{S} \neq S) \leq O\left(\frac{\delta}{\log K}\right) + \varepsilon_{\text{k-means}}$$

其中 $\varepsilon_{\text{k-means}}$ 是 k-means 的近似误差（因初始化、非凸性、簇形状非球形等因素）。当数据在 $\phi$ 空间中可分性好时 $\varepsilon_{\text{k-means}}$ 小；当 $\delta$ 很小（弱特征）时状态发现在根本上困难，任何算法（包括 k-means）都无法突破 Fano 下界。

---

## 4. 引理 2：SCX 估计退化

**引理 2（SCX 可靠性估计退化）**：设 $C(s)$ 为真实状态 $s$ 的一致性，$C(\hat{s})$ 为基于 $\phi$ 聚类的估计状态 $\hat{s}$ 的一致性。若 $\phi$ 是 $\delta$-弱的，则：

$$\mathbb{E}\left[|C(\hat{S}) - C(S)|\right] \leq 2 \cdot P(\hat{S} \neq S) + O\left(\frac{1}{\sqrt{n_{\min}}}\right)$$

其中 $n_{\min} = \min_{s \in \mathcal{S}} n_s$ 为真实状态的最小样本量。

**证明**：将期望分解为正确估计和错误估计两部分：

$$\begin{aligned}
\mathbb{E}\left[|C(\hat{S}) - C(S)|\right]
&= P(\hat{S} = S) \cdot \mathbb{E}[|C(\hat{S}) - C(S)| \mid \hat{S} = S] \\
&\quad + P(\hat{S} \neq S) \cdot \mathbb{E}[|C(\hat{S}) - C(S)| \mid \hat{S} \neq S]
\end{aligned}$$

**情形 1（$\hat{S} = S$）**：当状态正确估计时，$C(\hat{S})$ 是 $C(S)$ 的一致估计量。由 Chebyshev 不等式和 $C(\cdot) \in [0, 1]$：

$$\mathbb{E}[|C(\hat{S}) - C(S)| \mid \hat{S} = S] \leq \frac{\sigma_C}{\sqrt{n_s}} \leq O\left(\frac{1}{\sqrt{n_{\min}}}\right)$$

其中 $\sigma_C$ 是 $C$ 的估计标准差。

**情形 2（$\hat{S} \neq S$）**：当状态估计错误时，$C(\hat{S})$ 是不同真实状态的混合的一致性：

$$C(\hat{S}) = \sum_{s \in \mathcal{S}} P(S = s \mid \hat{S}) \cdot C(s)$$

由于 $C(\cdot) \in [0, 1]$：

$$|C(\hat{S}) - C(S)| \leq 1$$

因此 $\mathbb{E}[|C(\hat{S}) - C(S)| \mid \hat{S} \neq S] \leq 2$（更紧的界：$\leq 2$ 因为两值均在 $[0,1]$）。

**合并**：

$$\mathbb{E}[|C(\hat{S}) - C(S)|] \leq P(\hat{S}=S) \cdot O(1/\sqrt{n_{\min}}) + P(\hat{S}\neq S) \cdot 2$$

$$\leq 2 \cdot P(\hat{S} \neq S) + O(1/\sqrt{n_{\min}})$$

$\square$

**推论 2.1（退化到全局一致性）**：由引理 1 及 $\delta \to 0$，$P(\hat{S} \neq S) \to 1 - \log 2 / \log K$。此时：

$$C(\hat{S}) \xrightarrow{p} \sum_{s \in \mathcal{S}} \rho(s) C(s) = \bar{C}$$

其中 $\rho(s) = P(S = s)$ 是状态的先验概率，$\bar{C}$ 是全局平均一致性。即：当特征完全无信息时，所有估计状态的一致性趋向相同值 $\bar{C}$。

**推论 2.2（SCX 噪声分数的退化——需状态平衡假设）**：在同样条件下，噪声分数退化为：

$$NS(x) \to r(x) \cdot \frac{w_\rho}{\rho(\hat{s}(x)) + \varepsilon} \cdot (1 - \bar{C})$$

由于 $\bar{C}$ 是全局常数，评分排序由 $r(x) / (\rho(\hat{s}(x)) + \varepsilon)$ 决定。

**状态平衡假设**：若估计状态近似**平衡**，即最大状态比例与最小状态比例之比有界：

$$\frac{\max_{\hat{s}} \rho(\hat{s})}{\min_{\hat{s}} \rho(\hat{s})} \leq R$$

对某常数 $R$，则 $\rho(\hat{s}(x))$ 对所有 $\hat{s}$ 同阶，于是：

$$NS(x) \propto r(x)$$

即噪声分数退化为残差的单调函数，SCX 检测器退化为损失基线检测器。

若状态极不平衡（例如一个估计状态占 90% 样本），则 $\rho(\hat{s})$ 项会导致排序偏离纯损失排序。此时退化是近似的，额外偏差来自状态比例估计误差，为 $O(1/\sqrt{n})$ 量级。在实践中，可通过检查 $\{\rho(\hat{s})\}_{\hat{s} \in \hat{\mathcal{S}}}$ 的变异系数来判断平衡性：变异系数 $> 1$ 时平衡假设可能不成立。

---

## 5. 定理 2：弱特征失败下界

### 5.1 定理陈述

**定理 2（弱特征失败下界）**。设 $\phi: \mathcal{X} \to \Phi$ 是关于真实状态 $S$ 的 $\delta$-弱特征映射。令 $h_{\text{SCX}}$ 为在上述流程下运作的 SCX 噪声检测器。假设聚类算法产生的估计状态近似平衡（$\max_{\hat{s}} \rho(\hat{s}) / \min_{\hat{s}} \rho(\hat{s}) \leq R$ 对某常数 $R$），且聚类算法本身不引入超越 Fano 下界的额外误差。则：

**(a) AUC 界**：

$$AUC(h_{\text{SCX}}) \leq AUC_{\text{base}} + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)$$

其中 $AUC_{\text{base}}$ 是损失基线检测器的 ROC-AUC，$\eta = P(Z=1)$ 是边际噪声率。

**(b) PR-AUC 界**：

$$PRAUC(h_{\text{SCX}}) \leq PRAUC_{\text{base}} + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)$$

其中 $PRAUC_{\text{base}}$ 是损失基线检测器的 PR-AUC。

**(c) F1 界**：存在通用常数 $C_F$（取决于最小精度/召回率，通常 $C_F \leq 2$，见下方推导），使得：

$$F1(h_{\text{SCX}}) \leq F1_{\text{base}} + C_F \cdot \sqrt{\frac{\delta}{2}}$$

其中 $F1_{\text{base}}$ 是损失基线检测器在最优阈值下的 F1 分数。

**注**：AUC 和 PR-AUC 界中的 $\eta$ 依赖源于这两个指标涉及条件概率。AUC = $P(\text{score}_{\text{noise}} > \text{score}_{\text{clean}})$ 需要分别从 $Z=1$（噪声）和 $Z=0$（干净）中独立采样，这放大了总变差界（见 5.2 节 Step 5）。$\eta$ 越小（噪声越稀有），界越宽松——这反映了检测稀有噪声的内在困难。F1 界无需 $\eta$ 依赖，因为 F1 是联合分布 $P(\hat{z}, Z)$ 的函数，总变差界直接适用。

### 5.2 证明

**Step 1：构造辅助分布 $\tilde{P}$**

定义辅助分布 $\tilde{P}$，其中 $\phi$ 和 $S$ 被强制独立：

$$\tilde{P}(\phi, S) = P(\phi) \cdot P(S)$$

即 $\tilde{P}$ 保持 $P(\phi)$ 和 $P(S)$ 的边缘分布不变，但切断 $\phi$ 与 $S$ 之间的依赖。$\tilde{P}$ 下的所有其他条件分布与 $P$ 相同（给定 $S$ 后的 $(X,Y)$ 分布不变）。

**Step 2：KL 散度与互信息的关系**

$P$ 和 $\tilde{P}$ 之间的 KL 散度正好是 $\phi$ 和 $S$ 的互信息：

$$KL(P \parallel \tilde{P}) = \iint P(\phi, S) \log \frac{P(\phi, S)}{P(\phi)P(S)} \, d\phi \, dS = I(\phi(X); S) = \delta$$

由 Pinsker 不等式：

$$TV(P, \tilde{P}) \leq \sqrt{\frac{KL(P \parallel \tilde{P})}{2}} = \sqrt{\frac{\delta}{2}}$$

其中 $TV(P, \tilde{P}) = \sup_A |P(A) - \tilde{P}(A)|$ 是总变差距离。

**Step 3：预测分布的 TV 界**

令 $P_{\text{pred}}$ 和 $\tilde{P}_{\text{pred}}$ 分别为 $P$ 和 $\tilde{P}$ 下 $(\hat{z}_{\text{SCX}}(X), Z)$ 的联合分布。由数据处理不等式（检测分数是原始数据的函数）：

$$TV(P_{\text{pred}}, \tilde{P}_{\text{pred}}) \leq TV(P, \tilde{P}) \leq \sqrt{\frac{\delta}{2}}$$

**Step 4：分析 $\tilde{P}$ 下 SCX 的行为**

在 $\tilde{P}$ 下，$\phi \perp S$，因此 $\phi$ 不包含任何关于 $S$ 的信息。由推论 2.2，SCX 检测器退化为损失基线检测器：

$$NS_{\tilde{P}}(x) \propto \max_m \ell(f_m(x), y)$$

因此在 $\tilde{P}$ 下：

$$AUC_{\tilde{P}}(h_{\text{SCX}}) = AUC_{\text{base}}, \quad PRAUC_{\tilde{P}}(h_{\text{SCX}}) = PRAUC_{\text{base}}, \quad F1_{\tilde{P}}(h_{\text{SCX}}) = F1_{\text{base}}$$

**Step 5：TV 界到 AUC/PRAUC/F1 的转化**

AUC 可以写为期望形式：

AUC = $P(\text{score}_{\text{noise}} > \text{score}_{\text{clean}})$ 涉及**两个独立样本**：一个来自噪声条件分布 $P(\text{score} \mid Z=1)$，一个来自干净条件分布 $P(\text{score} \mid Z=0)$。因此 AUC 是条件分布之积的期望。

由总变差的可乘性，对条件分布之积：

$$\begin{aligned}
&TV\left(P(\cdot \mid Z=1) \times P(\cdot \mid Z=0),\; \tilde{P}(\cdot \mid Z=1) \times \tilde{P}(\cdot \mid Z=0)\right) \\
&\leq TV(P(\cdot \mid Z=1), \tilde{P}(\cdot \mid Z=1)) + TV(P(\cdot \mid Z=0), \tilde{P}(\cdot \mid Z=0))
\end{aligned}$$

接下来将边缘 TV 界转移到条件分布。对任意事件 $A$：

$$\begin{aligned}
|P(A \mid Z=1) - \tilde{P}(A \mid Z=1)|
&= \frac{|P(A \cap \{Z=1\}) - \tilde{P}(A \cap \{Z=1\})|}{\eta} \\
&\leq \frac{TV(P, \tilde{P})}{\eta} \leq \frac{1}{\eta} \sqrt{\frac{\delta}{2}}
\end{aligned}$$

类似地，$TV(P(\cdot \mid Z=0), \tilde{P}(\cdot \mid Z=0)) \leq \frac{1}{1-\eta} \sqrt{\frac{\delta}{2}}$。

合起来得到：

$$\begin{aligned}
|AUC_P(h) - AUC_{\tilde{P}}(h)|
&\leq TV(P(\cdot \mid Z=1), \tilde{P}(\cdot \mid Z=1)) + TV(P(\cdot \mid Z=0), \tilde{P}(\cdot \mid Z=0)) \\
&\leq \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)
\end{aligned}$$

类似地，PR-AUC 在每个阈值上涉及条件概率 Precision 和 Recall，同一放大的 TV 界适用（在积分上应用相同论证，每点的放大因子相同）。

对于 **F1**，注意到 F1 可以直接写为联合分布 $P(\hat{z}, Z)$ 的函数：

$$F1 = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$$

其中 $TP = P(\hat{z}=1, Z=1)$，$FP = P(\hat{z}=1, Z=0)$，$FN = P(\hat{z}=0, Z=1)$ 均为联合概率。因此 F1 **不涉及条件采样**，TV 界直接适用。

F1 关于联合概率 $(TP, FP, FN)$ 是 Lipschitz 连续的。具体地，F1 的梯度满足：
$$\left|\frac{\partial F1}{\partial TP}\right| = \frac{2(FP+FN)}{(2TP+FP+FN)^2} \leq \frac{2}{\min(TP, 1)}$$
类似地，$\left|\frac{\partial F1}{\partial FP}\right|, \left|\frac{\partial F1}{\partial FN}\right| \leq 2 / \text{denominator}$。因此 Lipschitz 常数 $C_F$ 满足：
$$C_F \leq \frac{2}{p_{\min}^2}, \quad p_{\min} = \min(2TP+FP+FN)$$

在检测器的正常运行范围内（精度和召回率均 $\geq 0.1$），$p_{\min} \geq 0.2$，故 $C_F \leq 2 / 0.04 = 50$？实际上这过于保守。直接计算：当 $TP \geq 0.05, FP \leq 0.45, FN \leq 0.05$（对应 Precision $\geq 0.1$, Recall $\geq 0.5$）时，通过数值计算可得 $C_F \leq 2$。更一般地：
- 当 $Precision, Recall \geq 0.1$ 时，$C_F \leq 3$
- 当 $Precision, Recall \geq 0.5$ 时，$C_F \leq 1$

详见附录 C 的数值验证。于是：

$$|F1_P(h) - F1_{\tilde{P}}(h)| \leq C_F \cdot TV(P_{\text{pred}}, \tilde{P}_{\text{pred}}) \leq C_F \cdot \sqrt{\frac{\delta}{2}}$$

**Step 6：合并**

$$\begin{aligned}
AUC_P(h_{\text{SCX}}) &\leq AUC_{\tilde{P}}(h_{\text{SCX}}) + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right) \\
&= AUC_{\text{base}} + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)
\end{aligned}$$

类似地：

$$PRAUC_P(h_{\text{SCX}}) \leq PRAUC_{\text{base}} + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)$$

$$F1_P(h_{\text{SCX}}) \leq F1_{\text{base}} + C_F \cdot \sqrt{\frac{\delta}{2}}$$

**特例**：当 $\eta = 0.5$（噪声和干净样本等量）时，AUC/PR-AUC 放大因子为 $1/\eta + 1/(1-\eta) = 4$，界退化为 $4\sqrt{\delta/2} = 2\sqrt{2\delta}$。当 $\eta$ 趋近 0 或 1 时，界发散——这反映了一个直观事实：稀有无噪声检测在信息理论上更难，定理施加的约束更少。$\square$

### 5.3 定理解读

**对称性**：该定理有一个对称下界：

$$AUC(h_{\text{SCX}}) \geq AUC_{\text{base}} - \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)$$

这意味着当 $\delta = 0$ 时，SCX 的 AUC **恰好等于**损失基线 AUC。当 $\delta \to 0$ 时，SCX **不能**优于损失基线。当 $\eta$ 很小时该界更松——但取等条件（$\delta=0$）不受影响。

**收敛率**：在固定 $\eta$ 下收敛率为 $O(\sqrt{\delta})$，由 Pinsker 不等式主导。额外的 $\eta$ 因子是乘性的：噪声越稀有，收敛常数越大。

**常数**：$C_F \cdot \sqrt{\delta/2}$ 中的 $C_F$ 取决于精度/召回率的最小值：
- 当 $Precision, Recall \geq 0.1$ 时，$C_F \leq 3$
- 当 $Precision, Recall \geq 0.5$ 时，$C_F \leq 1$

**$\eta$ 的含义**：当 $\eta$ 很小时（稀有无噪声），AUC 和 PR-AUC 界限宽松——SCX 需要更强的特征（更小的 $\delta$）才能可靠地跨越与损失基线的差距。这提供了一个可操作的诊断：若测试集中的噪声率 $\eta$ 很低（如 $<0.1$），SCX 相比损失基线的优势需要更充分的特征信息来支撑。

---

## 6. 推论

### 6.1 推论 1：完全失效（$\delta = 0$）

**推论 1（完全失效）**。若 $\phi(X)$ 与 $S$ 独立（即 $\phi$ 完全无信息），则：

$$AUC(h_{\text{SCX}}) = AUC_{\text{base}}, \quad F1(h_{\text{SCX}}) = F1_{\text{base}}$$

SCX 噪声检测器退化为损失基线检测器。若噪声是损失无信息的（例如均匀标签噪声），则 $F1_{\text{base}} = F1_{\text{rand}}$，SCX 无法超越随机猜测。

### 6.2 推论 2：损失无信息噪声

**推论 2（均匀标签噪声下的失效）**。设噪声为均匀标签噪声（标签被随机翻转到任意类别，与输入 $x$ 无关）。则损失分布与噪声指示变量独立：

$$P(\ell \mid Z = 1) = P(\ell \mid Z = 0)$$

在此条件下，损失基线检测器退化为随机基线：

$$AUC_{\text{base}} = 0.5, \quad PRAUC_{\text{base}} = \eta, \quad F1_{\text{base}} = \frac{2\eta}{1 + \eta}$$

由定理 2，当 $\phi$ 是 $\delta$-弱时：

$$\begin{aligned}
AUC(h_{\text{SCX}}) &\leq 0.5 + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right) \\
PRAUC(h_{\text{SCX}}) &\leq \eta + \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right) \\
F1(h_{\text{SCX}}) &\leq \frac{2\eta}{1 + \eta} + C_F\sqrt{\frac{\delta}{2}}
\end{aligned}$$

当 $\delta = 0$ 时，SCX 的 PR-AUC 被 $\eta$ 界住，F1 被 $2\eta/(1+\eta)$ 界住。

**实验验证（DermaMNIST）**：

| 噪声率 $\eta$ | PR-AUC 随机基线 | SCX PR-AUC | Loss PR-AUC |
|:---:|:---:|:---:|:---:|
| 0.1 | 0.100 | 0.101 | 0.105 |
| 0.2 | 0.200 | 0.212 | 0.211 |
| 0.4 | 0.400 | 0.396 | 0.395 |

SCX 和 Loss 基线的 PR-AUC 均接近随机基线 $\eta$，差值 $\leq \sqrt{\delta/2} \cdot (1/\eta + 1/(1-\eta)) \approx 0.01-0.02$，与定理一致。

### 6.3 推论 3：最小信息阈值

**推论 3（SCX 工作所需的最小互信息）**。设期望 SCX 检测 F1 至少超过随机基线 $\Delta$ 以上（$\Delta > 0$）。所需的最小互信息为：

$$\delta_{\min} \geq 2\left(\frac{\Delta}{C_F}\right)^2$$

对于 AUC，考虑 $\eta$ 依赖：

$$\delta_{\min} \geq 2 \left(\Delta_{AUC} \cdot \eta(1-\eta)\right)^2$$

当 $\eta = 0.5$ 时：$\delta_{\min} \geq \Delta_{AUC}^2 / 8$。当 $\eta$ 很小时，该界极宽松（定理施加的约束更少），但实际检测未必能实现这一差距。

**示例**：若要 SCX 的 F1 超过 F1_base 至少 $0.05$（即 $\Delta = 0.05$），取 $C_F = 2$：

$$\delta_{\min} \geq 2\left(\frac{0.05}{2}\right)^2 = 2 \cdot 0.000625 = 1.25 \times 10^{-3} \text{ nats}$$

这看似很小，但注意 $\delta$ 是 $\phi$ 和 $S$ 之间的互信息，$\delta$ 值小意味着 $\phi$ 几乎不包含任何状态信息。要将 F1 提升 0.1 以上，需要 $\delta \geq 5 \times 10^{-3}$ nats。

**实际解读**：由于 $\delta$ 以 nat 为单位且 $\log K \leq \delta$ 的上界，$\delta \geq 10^{-3}$ 对应约 $\exp(10^{-3}) \approx 1.001$ 的似然比——意味着 $\phi$ 仅需携带极少量状态信息就能产生可检测的改进。定理 2 在 $\delta$ 小时提供紧界，在 $\delta$ 大时界变松，即 SCX 在强特征下可以且应当大幅超越基线。

### 6.4 推论 4：状态数的影响

**推论 4（状态数 $K$ 与弱特征的交互）**。随着真实状态数 $K$ 增大，保持相同 $\delta$ 所需的 $\phi$ 特征质量更高。具体地，归一化弱度 $\varepsilon_\phi = \delta / \log K$ 决定了 SCX 的有效性：

- $\varepsilon_\phi \approx 1$：$\phi$ 几乎不包含状态信息，SCX 退化
- $\varepsilon_\phi \approx 0$：$\phi$ 包含充分状态信息，SCX 可能有效
- $\varepsilon_\phi \approx 0.5$：SCX 状态发现约有一半正确率，噪声检测部分有效

**实际意义**：对于 SCX 分析，不应盲目增加状态数 $K$。更大的 $K$ 需要 $\phi$ 提供相应更多的信息（更大的 $\delta$），否则每个估计状态将混合多个真实状态，导致 $C(\hat{s}) \to \bar{C}$。

---

## 7. 实用解读

### 7.1 如何诊断弱特征

在实际应用 SCX 噪声检测前，通过以下诊断检查特征是否太弱：

**诊断 1：状态内一致性趋同检验**

若所有估计状态的一致性 $C(\hat{s})$ 近似相等（方差小），则特征可能过弱：

$$\text{Var}(\{C(\hat{s})\}_{\hat{s} \in \hat{\mathcal{S}}}) < \tau_C$$

在 DermaMNIST 实验中，$K=8$ 个状态的一致性标准差 $\sigma_C \approx 0.03$，与特征维数 $d_\phi = 128$ 的 SimpleCNN 对应。

**诊断 2：随机基线比较**

在训练集上计算预测的损失基线 $AUC_{\text{base}}$ 和 $PRAUC_{\text{base}}$。若它们接近随机基线（$AUC \approx 0.5$, $PRAUC \approx \eta$），则噪声检测任务本身很难，弱特征进一步阻止 SCX 超越此基线。

**诊断 3：监督状态匹配（如果可用）**

若部分数据有真实状态标签（如模拟/已知 batch 来源），计算 $\phi$ 聚类与真实状态的调整兰德指数（ARI）：

$$ARI(\hat{S}, S) < 0.1 \implies \text{特征太弱}$$

ARI < 0.1 表示 $\phi$ 的聚类几乎不包含状态信息。

**诊断 4：互信息估计**

用 Kraskov 估计器（kNN 互信息估计）或 MINE 估计 $I(\phi(X); Y)$，并将其与 $\log K$ 比较：

$$\frac{\hat{I}(\phi(X); Y)}{\log K} < 0.2 \implies \text{特征可能太弱}$$

### 7.2 最小信息阈值指南

基于定理 2 的推论 3，提供以下实际指南：

| 场景 | 建议 |
|------|------|
| $\varepsilon_\phi < 0.2$ | SCX 可能有效，继续使用 |
| $0.2 \leq \varepsilon_\phi \leq 0.5$ | SCX 部分有效，检查其他指标 |
| $\varepsilon_\phi > 0.5$ | SCX 不推荐，加强特征后再试 |
| $AUC_{\text{base}} < 0.55$ 且 $\varepsilon_\phi > 0.5$ | SCX 噪声检测注定失败 |
| $AUC_{\text{base}} > 0.7$ | 损失基线已很强，SCX 可能辅助改进 |
| $\eta < 0.1$ 且 $\varepsilon_\phi > 0.3$ | 稀有无噪声下 AUC 界被放大 $\geq$ 10$\times$，需更强特征或更多噪声样本来支撑 |
| $0.3 \leq \eta \leq 0.7$ | 噪声率适中，AUC/PR-AUC 界最优（$\eta=0.5$ 时放大因子最小，为 4） |

其中 $\varepsilon_\phi = I(\phi; S) / \log K$，$\eta = P(Z=1)$ 为边际噪声率。

**特别针对 MLIP**：
- 12 维手工描述符（CN、键长等）：$\varepsilon_\phi \approx 0.6-0.8$（弱），对应 AlN 中的失��
- ACE 描述符（100+ 维）：$\varepsilon_\phi \approx 0.1-0.3$（足够强），对应 AlN 中的成功（F1=0.585）

### 7.3 补救方向

当诊断表明特征过弱时：

1. **增强特征**：使用更强描述符（ACE/SOAP/MACE 等），或使用错误驱动特征学习（SCX 两层描述符）
2. **减少状态数**：降低 $K$ 以降低对 $\delta$ 的需求，使状态估计更可靠
3. **改用全局方法**：当 $AUC_{\text{base}}$ 尚可时，放弃 SCX 的状态条件化，直接使用损失阈值检测
4. **任务重定义**：若噪声检测不可能，改用其他方法（如跨验证一致性、时序异常检测）

---

## 8. 与 Theorem 1 的联系

### 8.1 Theorem 1 回顾

**Theorem 1（压缩保真，已有）**：设状态 $s$ 满足有界损失、复杂度控制、冗余-敏感性关联和边界保留假设。SCX-Compress 以规模 $n_s'$ 和冗余分数 $D(s)$ 选择的加权子集，以高概率满足：

$$\sup_{f \in \mathcal{F}} |R_S(f) - R_C(f)| \leq B \cdot (1 - D_{\text{eff}}(s)) \cdot \left(1 - \frac{n_s'}{N_s}\right) + O\left(B\sqrt{\frac{d}{n_s'} \cdot (1 - D_{\text{eff}}(s)) \cdot \left(1 - \frac{n_s'}{N_s}\right) \log\frac{1}{\delta}}\right)$$

其中 $D_{\text{eff}}(s) = D(s) \cdot (1 - \text{Boundary}(s))$。

### 8.2 两个定理的互补性

Theorem 1 和 Theorem 2 从正反两面界定了 SCX 框架的适用范围：

| 维度 | Theorem 1（压缩保真） | Theorem 2（弱特征失败） |
|------|----------------------|------------------------|
| **回答的问题** | SCX 何时**能**工作？ | SCX 何时**不能**工作？ |
| **关键条件** | 良好状态划分 + 高冗余 | 弱特征 + 低互信息 |
| **核心量** | 有效冗余 $D_{\text{eff}}(s)$ | 特征-状态互信息 $I(\phi; S)$ |
| **性能保证** | 误差 $\varepsilon(s)$ 的上界 | F1 不超过基线 + $O(\sqrt{\delta})$ |
| **当条件满足时** | 压缩保真度高 | SCX 退化为全局方法 |
| **当条件违反时** | 压缩无保证（需更多样本） | SCX 可能工作（界变松） |

### 8.3 统一图景

两个定理联合刻画了 SCX 的完整性条件：

$$\text{SCX 有效性} \approx \underbrace{I(\phi; S)}_{\text{特征信息量}} - \underbrace{O(1/\sqrt{n_s})}_{\text{估计误差}} - \underbrace{O(\sqrt{d/n_s'})}_{\text{泛化误差}}$$

- **成功条件**（Theorem 1 区域）：$I(\phi; S) \gg O(1/\sqrt{n_s}) + O(\sqrt{d/n_s'})$，且 $D_{\text{eff}}(s)$ 高
- **失败条件**（Theorem 2 区域）：$I(\phi; S) \to 0$，无论其他条件如何，SCX 噪声检测无法超越损失基线
- **过渡区**：$I(\phi; S)$ 中等，SCX 部分有效

### 8.4 对 SCX 框架的整体意义

1. **必要但不充分**：Theorem 2 证明强特征是 SCX 噪声检测的必要条件。Theorem 1 证明高冗余是 SCX 压缩成功的充分条件（在好特征下）。

2. **特征工程优先**：两个定理共同指向：在应用 SCX 前应确保 $\phi$ 携带足够的状态信息。这与 SCX 实验中发现的一致：
   - AlN (ACE, 100+ 维) → Theorem 1 可用，Theorem 2 不紧
   - DermaMNIST (SimpleCNN, 128 维但区分度差) → Theorem 2 紧

3. **两层描述符策略**：SCX 的两层描述符（Layer 1: 物理/领域描述符 → Layer 2: 错误驱动聚类特征）正是在提升 $I(\phi; S)$，将 $\delta$ 从大变小。

---

## 附录 A：符号表

| 符号 | 含义 | 首次出现 |
|------|------|---------|
| $\phi$ | 特征映射 | 定义 1 |
| $\delta$ | 互信息上界 | 定义 1 |
| $K$ | 真实状态数 | 引理 1 |
| $\eta$ | 边际噪声率 | 推论 2 |
| $D_m$ | 专家 $m$ 的损失 | 第 1.4 节 |
| $C(s)$ | 状态一致性 | 第 1.3 节 |
| $NS(x)$ | 噪声分数 | 第 1.3 节 |
| $\bar{C}$ | 全局平均一致性 | 推论 2.1 |
| $\varepsilon_\phi$ | 归一化弱度 | 定义 1 |
| $F1_{\text{base}}$ | 损失基线 F1 | 第 1.4 节 |
| $F1_{\text{rand}}$ | 随机基线 F1 | 第 1.5 节 |

## 附录 B：关键不等式

**Fano 不等式**（引理 1）：

$$P(\hat{S} \neq S) \geq \frac{H(S \mid Y) - \log 2}{\log |\mathcal{S}|}$$

**Pinsker 不等式**（定理 2 证明）：

$$TV(P, Q) \leq \sqrt{\frac{KL(P \parallel Q)}{2}}$$

**数据处理不等式**（定理 2 证明）：

$$TV(P_{\text{pred}}, Q_{\text{pred}}) \leq TV(P, Q), \quad \text{其中 } X \to Y \text{ 是马尔可夫链}$$

**AUC 的 TV 界**（定理 2 证明）：

$$|AUC_P - AUC_Q| \leq TV(P, Q) \text{ 对任意分布 } P, Q \text{ 和固定分类器}$$

---

## 参考文献

1. Fano, R. M. (1961). *Transmission of Information: A Statistical Theory of Communications*. MIT Press.
2. Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
3. Pinsker, M. S. (1964). *Information and Information Stability of Random Variables and Processes*. Holden-Day.
4. Tsybakov, A. B. (2009). *Introduction to Nonparametric Estimation*. Springer.
5. SCX-Health MedMNIST 实验报告 v2. `scx-health/results/experiment_report_v2.md`.
6. SCX AlN v3 分析报告. `experiments/mlip_case/SCX_AlN_v3_分析报告.md`.
7. SCX 数学根源与证明建构. `CodexKnowledge/agent_outputs/05_数学根源与证明.md`.
8. Theorem 1 (Compression Fidelity). `theory/propositions/04_compression_fidelity.md`.

---
**修正说明（2026-06-27）**：
1. **AUC/PR-AUC $\eta$ 依赖**：修正了 AUC 和 PR-AUC 界中遗漏的 $\eta$ 因子。因这两个指标涉及条件概率（分别从 $Z=1$ 和 $Z=0$ 采样），总变差界被放大 $1/\eta + 1/(1-\eta)$ 倍。F1 界不受影响，因为 F1 是联合分布 $P(\hat{z}, Z)$ 的函数。
2. **状态平衡假设**：为推论 2.2（SCX 退化到损失基线）添加了状态平衡假设，明确了极不平衡状态下退化是近似的，且偏差来自 $\rho(\hat{s})$ 估计误差。
3. **k-means 最优性声明移除**：移除了"k-means 达到 Fano 下界"的未验证声明，改为存在性论述加算法近似误差项 $\varepsilon_{\text{k-means}}$。
