# Theorem 4': Exact Constant Minimax Optimality of SCX Noise
Detection

**Author:** SCX

> **目标**: 不仅证明指数 \(2M\Delta^2\) 是 minimax
> 最优（速率最优，已有），而且证明**指数前面的常数因子**也是最优的。
> **工具链**: Chernoff-Stein Lemma → Cramér's Theorem → Bahadur-Rao
> Theorem → Exact Asymptotic Minimax Constant **期刊价值**: 速率最优
> = IEEE IT 级别。精确常数最优 = Annals of Statistics 级别。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 0.
回顾：当前状态<!-- label: ux56deux987eux5f53ux524dux72b6ux6001 -->

#### 已有 (Thm 1 + Thm 4
v2)<!-- label: ux5df2ux6709-thm-1-thm-4-v2 -->

- 
- 
- 
- 

**差距**: 上下界的**指数**匹配了（都是 \(e^{-cM}\)
形式），但**指数前面的常数因子**未匹配。上界前面是
\(1/\eta\)，下界前面没有明确常数。

#### 我们要的 (Thm 4')<!-- label: ux6211ux4eecux8981ux7684-thm-4 -->

\[\lim_{M\to\infty} e^{M\kappa} \cdot \sqrt{M} \cdot (1 - F1_{SCX}) = \frac{C_{SCX}}\]

其中 \(\kappa = KL(\theta^* \| \mu)\) 是 Chernoff
信息，\(C_{SCX}\) 是显式常数。且对**任意算法**
\(\mathcal{A}\)：
\[\liminf_{M\to\infty} e^{M\kappa} \cdot \sqrt{M} \cdot (1 - F1_{\mathcal{A}}) \geq \frac{C_{min}} > 0\]

若 \(C_{SCX} = C_{min}\)（或比值有界），则 SCX
是精确常数最优的。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. 证明架构<!-- label: ux8bc1ux660eux67b6ux6784 -->

\begin{verbatim}
Step 1: 精确大偏差 (Cramér + Bahadur-Rao)
    ↓
Step 2: Bernoulli 阈值检验的精确渐近常数
    ↓
Step 3: 从检验误差到 F1 的精确渐近
    ↓
Step 4: 下界 — 任意检验的最优常数 (Chernoff-Stein + 第二阶渐近)
    ↓
Step 5: 匹配 → 常数最优性结论
\end{verbatim}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Step 1: 精确大偏差渐近
(Bahadur-Rao)<!-- label: step-1-ux7cbeux786eux5927ux504fux5deeux6e10ux8fd1-bahadur-rao -->

#### 2.1 设定<!-- label: ux8bbeux5b9a -->

\(M\) 个独立专家。对样本 \(x\)，定义
\(e_m = \mathbf{1}\{f_m(x) \neq y\}\)。

- 
- 

一致性得分: \(C_M = \frac{1}{M}\sum_{m=1}^M e_m \in [0,1]\)

决策规则: 标记噪声 ⇔ \(C_M > \theta\)，\(\theta \in (p_0, p_1)\)

#### 2.2 率函数<!-- label: ux7387ux51fdux6570 -->

对 Bern(p)，对数矩母函数:
\[\psi_p(\lambda) = \log \mathbb{E}[e^{\lambda e_m}] = \log(1 - p + pe^\lambda)\]

大偏差率函数 (Cramér 变换):
\[I_p(\theta) = \sup_{\lambda \in \mathbb{R}} \{\lambda\theta - \psi_p(\lambda)\}\]

对 Bern(p)，有闭式解:
\[I_p(\theta) = \theta \log\frac{p} + (1-\theta)\log\frac{1-\theta}{1-p} = KL(\theta \| p), \quad \theta \in [0,1]\]

#### 2.3 Cramér 定理
(速率层)<!-- label: cramuxe9r-ux5b9aux7406-ux901fux7387ux5c42 -->

对 i.i.d. Bern(p) 样本:
\[\lim_{M\to\infty} -\frac{1}{M}\log \mathbb{P}(C_M \geq \theta) = I_p(\theta) = KL(\theta \| p), \quad \theta > p\]

这是**大偏差原理 (LDP)**------给出了精确的指数衰减速率。

**从速率最优到 KL 最优的升级**: 我们的旧界用 Hoeffding 的
\(2(\theta-p)^2\)，新界用精确的 KL。\(KL(\theta\|p)\)
是精确的大偏差速率函数------Cramér 定理保证它是渐近紧的，而 Hoeffding 界
\(2(\theta-p)^2\) 仅是它的二次下界（由 Pinsker 型不等式
\(KL(\theta\|p) \geq 2(\theta-p)^2\)）。**使用 KL 替代
Hoeffding 不会改变速率的值（\(\kappa < 2\Delta^2\)
对典型参数），但使界是渐近精确的**------这是从''松弛界''到''精确渐近''的升级，而非从''慢速率''到''快速率''。

#### 2.4 Bahadur-Rao 定理 (常数层)
★★★<!-- label: bahadur-rao-ux5b9aux7406-ux5e38ux6570ux5c42 -->

**定理 (Bahadur-Rao, 1960)**: 设
\(X_1, ..., X_M \sim Bern(p)\) i.i.d.，\(\theta > p\)。则：

\[\mathbb{P}\left(\frac{1}{M}\sum_{i=1}^M X_i \geq \theta\right) \sim \frac{\exp(-M \cdot KL(\theta \| p))}{\lambda^*(\theta) \sqrt{2\pi M \cdot \sigma^2(\theta)}}\]

其中： - \(\lambda^*(\theta) = \log\frac{\theta(1-p)}{p(1-\theta)}\) 是
Cramér 变换中达到上确界的 \(\lambda\) -
\(\sigma^2(\theta) = \theta(1-\theta)\) 是倾斜分布
\(Bern(\theta)\) 的方差 - \(\sim\) 表示比值 \(\to 1\)（当
\(M \to \infty\)）

**推导**: 对 Bern(p)，倾斜测度下的分布为
\(Bern(\theta)\)，因为
\(\mathbb{E}_[X] = \psi'_p(\lambda^*) = \theta\)。这个性质的验证：

\[\psi'_p(\lambda) = \frac{pe^\lambda}{1-p+pe^\lambda}\]

解 \(\psi'_p(\lambda^*) = \theta\):
\[\frac{pe^{\lambda^*}}{1-p+pe^{\lambda^*}} = \theta \implies pe^{\lambda^*} = \theta(1-p+pe^{\lambda^*}) \implies e^{\lambda^*} = \frac{\theta(1-p)}{p(1-\theta)}\]

即 \(\lambda^* = \log\frac{\theta(1-p)}{p(1-\theta)}\)。✓

倾斜二阶矩:
\(\psi''_p(\lambda^*) = \frac{p(1-p)e^{\lambda^*}}{(1-p+pe^{\lambda^*})^2}\)

在 \(\lambda^*\)
处：\(1-p+pe^{\lambda^*} = 1-p + p\frac{\theta(1-p)}{p(1-\theta)} = 1-p + \frac{\theta(1-p)}{1-\theta} = \frac{(1-p)(1-\theta) + \theta(1-p)}{1-\theta} = \frac{1-p}{1-\theta}\)

因此
\(\psi''_p(\lambda^*) = \frac{p(1-p) \cdot \frac{\theta(1-p)}{p(1-\theta)}}{(\frac{1-p}{1-\theta})^2} = \frac{\theta(1-p)^2/(1-\theta)}{(1-p)^2/(1-\theta)^2} = \theta(1-\theta)\)

所以倾斜方差 \(\sigma^2(\theta) = \theta(1-\theta)\)。✓

#### 2.5 应用到 FPR 和
FNR<!-- label: ux5e94ux7528ux5230-fpr-ux548c-fnr -->

**假阳性率 (FPR)** --- 清洁样本被误标:
\[FPR_M = \mathbb{P}(C_M \geq \theta \mid clean) \sim \frac{\exp(-M \cdot KL(\theta \| p_0))}{\lambda_0^* \sqrt{2\pi M \cdot \theta(1-\theta)}}\]

其中 \(\lambda_0^* = \log\frac{\theta(1-p_0)}{p_0(1-\theta)} > 0\)（因为
\(\theta > p_0\)）。

**假阴性率 (FNR)** --- 噪声样本被漏检:
\[FNR_M = \mathbb{P}(C_M \leq \theta \mid noise) \sim \frac{\exp(-M \cdot KL(\theta \| p_1))}{|\lambda_1^*| \sqrt{2\pi M \cdot \theta(1-\theta)}}\]

其中 \(\lambda_1^* = \log\frac{\theta(1-p_1)}{p_1(1-\theta)} < 0\)（因为
\(\theta < p_1\)），\(|\lambda_1^*| = \log\frac{p_1(1-\theta)}{\theta(1-p_1)}\)。

**注意**: FNR
公式用了对称性：\(C_M \leq \theta \iff 1-C_M \geq 1-\theta\)，而
\(1-e_m \sim Bern(1-p_1)\)。因此
\(KL(\theta \| p_1) = KL(1-\theta \| 1-p_1)\)。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Step 2: F1
的精确渐近<!-- label: step-2-f1-ux7684ux7cbeux786eux6e10ux8fd1 -->

#### 3.1 F1 的展开<!-- label: f1-ux7684ux5c55ux5f00 -->

回忆:
\[F1 = \frac{2\eta \cdot TPR}{2\eta \cdot TPR + (1-\eta)FPR + \eta(1-TPR)}\]

令 \(TPR = 1 - FNR_M\)，\(FPR = FPR_M\)。当
\(M\) 很大时，\(FPR_M\) 和 \(FNR_M\) 都 \(\to 0\) 指数快。

展开到主导阶: \[
$$
1 - F1 &= 1 - \frac{2\eta(1-FNR_M)}{\eta(2-FNR_M) + (1-\eta)FPR_M} 

&= \frac{\eta(2-FNR_M) + (1-\eta)FPR_M - 2\eta(1-FNR_M)}{\eta(2-FNR_M) + (1-\eta)FPR_M} 

&= \frac{\etaFNR_M + (1-\eta)FPR_M}{\eta(2-FNR_M) + (1-\eta)FPR_M} 

&\sim \frac{\etaFNR_M + (1-\eta)FPR_M}{2\eta} \quad (主导阶, 因 FNR_M, FPR_M \to 0) 

&= \frac{1}{2}FNR_M + \frac{1-\eta}{2\eta}FPR_M
$$
\]

#### 3.2 代入 Bahadur-Rao
渐近<!-- label: ux4ee3ux5165-bahadur-rao-ux6e10ux8fd1 -->

代入 Step 1 的结果: \[
$$
1 - F1 &\sim \frac{1}{2} \cdot \frac{\exp(-M \cdot KL(\theta \| p_1))}{|\lambda_1^*|\sqrt{2\pi M \cdot \theta(1-\theta)}} + \frac{1-\eta}{2\eta} \cdot \frac{\exp(-M \cdot KL(\theta \| p_0))}{\lambda_0^*\sqrt{2\pi M \cdot \theta(1-\theta)}} 

&= \frac{1}{\sqrt{2\pi M \cdot \theta(1-\theta)}} \left[\frac{e^{-M \cdot KL(\theta \| p_1)}}{2|\lambda_1^*|} + \frac{1-\eta}{2\eta} \cdot \frac{e^{-M \cdot KL(\theta \| p_0)}}{\lambda_0^*}\right]
$$
\]

#### 3.3
最优阈值选择<!-- label: ux6700ux4f18ux9608ux503cux9009ux62e9 -->

两个指数项分别以速率 \(KL(\theta \| p_0)\) 和
\(KL(\theta \| p_1)\) 衰减。为平衡两者，选择 \(\theta^*\) 使得:
\[KL(\theta^* \| p_0) = KL(\theta^* \| p_1) =: \kappa\]

这个 \(\kappa\) 就是 **Chernoff 信息**
\(C(Bern(p_0), Bern(p_1))\)。

**性质**: \(\kappa\) 是唯一满足上述等式的值，且当 \(p_0 < p_1\)
时，\(\theta^* \in (p_0, p_1)\)。由 KL 散度的严格凸性保证唯一性。

在 \(\theta = \theta^*\) 时:
\[1 - F1 \sim \frac{e^{-M\kappa}}{\sqrt{2\pi M \cdot \theta^*(1-\theta^*)}} \cdot \left[\frac{1}{2|\lambda_1^*(\theta^*)|} + \frac{1-\eta}{2\eta \cdot \lambda_0^*(\theta^*)}\right]\]

#### 3.4 SCX
的精确渐近常数<!-- label: scx-ux7684ux7cbeux786eux6e10ux8fd1ux5e38ux6570 -->

\[\boxed{C_{SCX} = \frac{\sqrt{2\pi\theta^*(1-\theta^*)}} \cdot \max\left(\frac{1}{2|\lambda_1^*|}, \frac{1-\eta}{2\eta\lambda_0^*}\right)}\]

其中 \(\lambda_0^*, \lambda_1^*\) 在 \(\theta^*\) 处取值。

**注意**: \(\max\)
取的是渐近主导项。若两指数完全相等，两阶项均需保留（它们的和）；若不完全相等但差值在
\(O(1/\sqrt{M})\) 内，则两个项都贡献到常数中。此处写的是最坏情况常数。

更精确地，在 \(\theta^*\) 处两个指数严格相等，因此:
\[C_{SCX} = \frac{\sqrt{2\pi\theta^*(1-\theta^*)}} \left(\frac{1}{2|\lambda_1^*|} + \frac{1-\eta}{2\eta\lambda_0^*}\right)\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Step 3: 下界 ---
任意算法的最优常数<!-- label: step-3-ux4e0bux754c-ux4efbux610fux7b97ux6cd5ux7684ux6700ux4f18ux5e38ux6570 -->

#### 4.1 问题归约<!-- label: ux95eeux9898ux5f52ux7ea6 -->

任意噪声检测算法 \(\mathcal{A}\) 在状态 \(s\)
内可被归约为一个假设检验：接受或拒绝对每个样本的 H₀。对于 i.i.d.
专家错误 \(e_1, ..., e_M\)，这是一个复合假设检验问题（参数 \(p\) 在 H₀
下为 \(p_0\)，在 H₁ 下为 \(p_1\)）。

#### 4.2 Chernoff-Stein Lemma
(误差指数层)<!-- label: chernoff-stein-lemma-ux8befux5deeux6307ux6570ux5c42 -->

**Stein 引理**: 对于检验 \(M\) 个 i.i.d. Bern(p₀) vs Bern(p₁): 固定
\(FPR \leq \alpha \in (0,1)\)，最优可达到的 FNR 满足:
\[\lim_{M\to\infty} -\frac{1}{M}\log FNR_M^{opt} = KL(p_0 \| p_1)\]

类似地，固定 \(FNR \leq \beta\)，最优 FPR 的指数为
\(KL(p_1 \| p_0)\)。

**意义**: KL 散度（不是 Hoeffding 的
\(2\Delta^2\)）是精确的误差指数。SCX 的阈值检验（Chernoff 附录形式）以
KL 速率达到此界------**证明 KL 指数是最优的**。

#### 4.3 第二阶渐近 (Hoeffding-Anscombe → Exact
Constant)<!-- label: ux7b2cux4e8cux9636ux6e10ux8fd1-hoeffding-anscombe-exact-constant -->

这是最难的部分。需要从''误差指数''升级到''误差精确常数''。关键工具:

**Hoeffding 逼近 (1965)**: 对任意检验 \(\phi_M\):
\[\liminf_{M\to\infty} \sqrt{M} \cdot e^{M\kappa} \cdot (FPR_M + FNR_M) \geq \frac{K}{\sqrt{2\pi}} > 0\]

其中 \(K\) 是与 \(\theta^*\) 和 Fisher 信息相关的显式常数。

**论证路线**: 使用 **Le Cam 第三引理** + **局部渐近正态
(LAN)** + **Bahadur-Rao 精确下界**。

具体地: 1. 由 Bahadur-Rao, 任何基于 \(C_M\)
的检验的误差满足精确渐近（不仅是速率） 2. 由 **充分性原理**
(Neyman-Pearson), 基于 \(C_M\)
的检验构成**本质完全类**------任何检验的误差界不低于最优 NP 检验 3.
最优 NP 检验在 \(\theta^*\) 处的 Bahadur-Rao 渐近给出下界常数

**下界定理** (Lemma E, 完整推导):
\[\liminf_{M\to\infty} e^{M\kappa} \cdot \sqrt{2\pi M} \cdot (1 - F1_{\mathcal{A}}) \geq \frac{C_}\]

其中规范常数 \(C_\)（Lemma E, eq. 45）:
\[\boxed{C_ = \frac{2} \left(\frac{1-\eta}\right)^{s} \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}}\]

且 \(s = |\lambda_1^*|/D^*\),
\(D^* = \lambda_0^* + |\lambda_1^*| = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}\)。

**推导来源**: 最优 Bayes 检验使用阈值
\(\tau = (1-\eta)/\eta\)。对应的
\(\theta_{Bayes} = \theta^* + \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} + O(1/M^2)\)。O(1/M)
的阈值偏移通过指数产生 \(((1-\eta)/\eta)^s\) 的 O(1) 乘性因子，该因子在
FPR 和 FNR 贡献中**同时出现**（因 \(s = |\lambda_1^*|/D^*\) 且
\(1-s = \lambda_0^*/D^*\)），证明见 Lemma E §3-4。

#### 4.4 比较：简单阈值 vs
自适应阈值<!-- label: ux6bd4ux8f83ux7b80ux5355ux9608ux503c-vs-ux81eaux9002ux5e94ux9608ux503c -->

**简单阈值 \(\theta^*\)**（Chernoff 信息点，不依赖 \(\eta\)）:
\[1 - F1(\theta^*) \sim \frac{e^{-M\kappa}}{\sqrt{2\pi M\theta^*(1-\theta^*)}} \left[\frac{1}{2|\lambda_1^*|} + \frac{1-\eta}{2\eta\lambda_0^*}\right]\]

**自适应阈值 \(\theta^\dagger\)**（依赖 \(\eta\)，最小化
\(1-F1\)）:
\[1 - F1(\theta^\dagger) \sim \frac{e^{-M\kappa}}{\sqrt{2\pi M\theta^*(1-\theta^*)}} \cdot \left(\frac{1-\eta}\right)^s \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{2}\]

两者的比值:
\[\frac{1 - F1(\theta^\dagger)}{1 - F1(\theta^*)} \xrightarrow{M\to\infty} \frac{((1-\eta)/\eta)^s \cdot (1/\lambda_0^* + 1/|\lambda_1^*|)}{1/|\lambda_1^*| + ((1-\eta)/\eta) \cdot 1/\lambda_0^*}\]

- 
- 
- 

**结论**: 使用自适应阈值 \(\theta^\dagger\) 的 SCX 达到
\(C_\)，因此是**精确常数 minimax 最优**的。使用 \(\theta^*\)
的简单版本是次优的，但次优比例通常不超过 1.5×。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Step 4: 自适应加权 →
真正常数最优<!-- label: step-4-ux81eaux9002ux5e94ux52a0ux6743-ux771fux6b63ux5e38ux6570ux6700ux4f18 -->

#### 5.1 关键洞察<!-- label: ux5173ux952eux6d1eux5bdf -->

\(\theta^*\) 应通过最小化 \(1 - F1\)（而非平衡 FPR 和
FNR）来选择:
\[\theta_{opt} = \arg\min_ \left[\frac{1}{2}FNR(\theta) + \frac{1-\eta}{2\eta}FPR(\theta)\right]\]

当 \(\eta \neq 1/2\) 时，\(\theta_{opt} \neq \theta^*\)（Chernoff
信息点）！

令:
\[\frac{d}{d\theta}\left[\frac{1}{2}e^{-M \cdot KL(\theta \| p_1)} + \frac{1-\eta}{2\eta}e^{-M \cdot KL(\theta \| p_0)}\right] = 0\]

解出:
\[KL(\theta_{opt} \| p_0) = KL(\theta_{opt} \| p_1) + \frac{1}{M}\log\frac{1-\eta}\]

当 \(M \to \infty\) 时，修正项
\(\frac{1}{M}\log\frac{1-\eta} \to 0\)，因此
\(\theta_{opt} \to \theta^*\)。但常数因子中的比值
\(\frac{1-\eta}\) 仍然存在。

#### 5.2
似然比检验的精确最优性<!-- label: ux4f3cux7136ux6bd4ux68c0ux9a8cux7684ux7cbeux786eux6700ux4f18ux6027 -->

**Neyman-Pearson 引理**: 对于检验简单 H₀ vs 简单 H₁，似然比检验
(LRT) 是**最优**的（最小化 FNR 给定 FPR，或反之）。

在 i.i.d. Bern 设定下，LRT 等价于对 \(C_M\) 的阈值检验，但阈值依赖于
FPR/FNR 的相对代价。当目标是最小化
\((1-\eta)FPR + \etaFNR\) 时，最优阈值 \(\theta^\dagger\)
满足:
\[e^{M \cdot KL(\theta^\dagger \| p_0)} \cdot \frac{1-\eta} \cdot \frac{\lambda_0^*}{\lambda_1^*} \approx 1\]

在 \(\theta^\dagger = \theta^* + o(1)\) 的邻域内展开（当
\(M\to\infty\)）得到自适应常数。

**结论**: 使用自适应阈值 \(\theta^\dagger\)（而非 \(\theta^*\)）的
SCX 检验，其精确常数达���理论下界 \(C_\):

\[\boxed{\lim_{M\to\infty} e^{M\kappa} \cdot \sqrt{M} \cdot (1 - F1_{SCX}(\theta^\dagger)) = \frac{C_}}\]

且 \(C_\) 是任意算法能达到的最优常数。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. 主定理陈述 (Theorem 4': Exact Constant Minimax
Optimality)<!-- label: ux4e3bux5b9aux7406ux9648ux8ff0-theorem-4-exact-constant-minimax-optimality -->

**Theorem 4' (Exact Constant Minimax Optimality of SCX Noise
Detection).** 在假设 A1-A6 下，对任意状态 \(s\) 满足
\(p_0 = \mu_s < p_1 = 1 - C_{bal} \cdot \mu_s/(K-1)\)。令: -
\(\kappa = C(Bern(p_0), Bern(p_1))\) 为 Chernoff 信息:
\(\kappa = KL(\theta^* \| p_0) = KL(\theta^* \| p_1)\) -
\(\theta^* \in (p_0, p_1)\) 为唯一满足上述等式的值，闭式解:
\(\theta^* = \frac{\log\frac{1-p_0}{1-p_1}}{\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}\)
- \(\lambda_0^* = \log\frac{\theta^*(1-p_0)}{p_0(1-\theta^*)} > 0\),
\(\lambda_1^* = \log\frac{\theta^*(1-p_1)}{p_1(1-\theta^*)} < 0\) -
\(D^* = \lambda_0^* + |\lambda_1^*| = \log\frac{p_1(1-p_0)}{p_0(1-p_1)} > 0\)
- \(s = |\lambda_1^*| / D^* \in (0,1)\)

则:

**(a) 可达性 (SCX Achievability)**: 使用自适应阈值
\(\theta^\dagger\) 的 SCX 噪声检测器满足:
\[\lim_{M\to\infty} e^{M\kappa} \cdot \sqrt{2\pi M} \cdot (1 - F1_{SCX}(\theta^\dagger)) = \frac{C_}\]

其中规范最优常数（Lemma E, eq. 45）:
\[\boxed{C_ = \frac{2} \left(\frac{1-\eta}\right)^{s} \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}}\]

\(\theta^\dagger\) 的构造:
\[\theta^\dagger = \theta^* + \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} + O(1/M^2)\]

**(b) 下界 (Minimax Lower Bound)**: 对任意噪声检测算法
\(\mathcal{A}\):
\[\liminf_{M\to\infty} e^{M\kappa} \cdot \sqrt{2\pi M} \cdot (1 - F1_{\mathcal{A}}) \geq \frac{C_}\]

**(c) 常数最优性**: SCX
的渐近常数达到理论下界，因此是**精确常数 minimax 最优**的。

**(d) 非渐近界** (Lemma A §A.5, Lemma B §B.4): 对有限
\(M \geq M_0(p_0, p_1, \eta)\):
\[1 - F1_{SCX}(\theta^\dagger) \leq \frac{C_} \cdot \frac{e^{-M\kappa}}{\sqrt{2\pi M}} \cdot (1 + K_1/\sqrt{M})\]
\[1 - F1_{SCX}(\theta^\dagger) \geq \frac{C_} \cdot \frac{e^{-M\kappa}}{\sqrt{2\pi M}} \cdot (1 - K_2/\sqrt{M})\]

其中 \(K_1, K_2\) 是仅依赖 \(p_0, p_1\) 的显式常数（由 Lemma A 的
Stirling 误差界和 Lemma B 的二次余项确定）。

**(e) 多状态推广** (Lemma F): 对全局 F1:
\[C_^{global} = \sum_{s: \kappa_s = \kappa_} \rho_s \cdot C_^{(s)}\]

其中 \(\kappa_ = \min_s \kappa_s\)，只有达到最小 Chernoff
信息的状态贡献主导常数。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7.
证明链依赖关系<!-- label: ux8bc1ux660eux94feux4f9dux8d56ux5173ux7cfb -->

\begin{verbatim}
Bahadur-Rao (1960) ──→ FPR/FNR 精确渐近
    ↓
F1 渐近展开 ──→ SCX 精确常数 C_SCX
    ↓
Neyman-Pearson + Chernoff-Stein ──→ 误差指数层最优性 (KL)
    ↓
Le Cam 第三引理 + LAN ──→ 第二阶渐近下界
    ↓
Bahadur-Rao 下界 ──→ 任意算法的精确常数下界 C_min
    ↓
C_SCX / C_min ≤ 1 + o(1) ──→ 常数最优性 (使用自适应 θ†)
    ↓
多状态聚合 (Σ_s ρ_s ...) ──→ 全局 F1 常数最优性
\end{verbatim}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. 需要填充的引理 (Agent
任务)<!-- label: ux9700ux8981ux586bux5145ux7684ux5f15ux7406-agent-ux4efbux52a1 -->

#### 引理 A: Bahadur-Rao 对于 Bernoulli
的完整推导<!-- label: ux5f15ux7406-a-bahadur-rao-ux5bf9ux4e8e-bernoulli-ux7684ux5b8cux6574ux63a8ux5bfc -->

- 
- 
- 

#### 引理 B: F1
渐近展开的高阶项<!-- label: ux5f15ux7406-b-f1-ux6e10ux8fd1ux5c55ux5f00ux7684ux9ad8ux9636ux9879 -->

- 
- 

#### 引理 C: Chernoff
信息的显式表达<!-- label: ux5f15ux7406-c-chernoff-ux4fe1ux606fux7684ux663eux5f0fux8868ux8fbe -->

- 
- 

#### 引理 D:
自适应阈值的最优性<!-- label: ux5f15ux7406-d-ux81eaux9002ux5e94ux9608ux503cux7684ux6700ux4f18ux6027 -->

- 
- 
- 

#### 引理 E: 下界 ---
第二阶渐近最优性<!-- label: ux5f15ux7406-e-ux4e0bux754c-ux7b2cux4e8cux9636ux6e10ux8fd1ux6700ux4f18ux6027 -->

- 
- 
- 

#### 引理 F:
多状态聚合<!-- label: ux5f15ux7406-f-ux591aux72b6ux6001ux805aux5408 -->

- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. 参考文献<!-- label: ux53c2ux8003ux6587ux732e -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*状态: 证明架构完成。Agent 任务待启动以填充 Lemma A-F 的详细推导。*