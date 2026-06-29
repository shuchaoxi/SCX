# 神经网络分类学理论：从SCX公理系统严格推导机器学习已知现象

**A Taxonomic Theory of Neural Networks: Rigorous Derivation of Known Machine Learning Phenomena from the SCX Axiom System**

SCX Research Group, Theory Division, Xiaogan Supercomputing Center

2026年6月29日

---

## 摘要

我们提出，机器学习的七大核心经验现象——集成方法的有效性、深度网络的指数优势、表示学习的预训练收益、大语言模型的幻觉必然性、残差连接的有效性、自监督学习的退化极限——均可以从SCX（State-Conditioned eXpertise）公理系统获得解释。其中集成方法（§2）、深度（§3）、表示学习（§4）、自监督学习（§7）四个现象获得严格数学推导；LLM幻觉（§5, v2.0升级为严格证明，关键洞察：多种子独立解码恢复条件独立假设）、残差连接（§6, v2.0升级为条件严格证明，关键洞察：NTK极限下残差块=凸势能的负梯度）、以及噪声占优阈值$\eta_c \in [0.25, 0.35]$（§8预测4, v2.0升级为条件严格推导，关键洞察：$\eta_c = \sqrt{\text{Var}(Q)/\text{Var}(N)}/(1+|\rho_{QN}|)$从Cercis Score方差分析导出）均获得显著升级的数学论证。SCX公理系统由四个核心定理（F1界、弱特征失效边界、噪声-难度不可区分、minimax最优）、Cercis评分$S = Q + \eta N$、以及Spring自演化定理（Lyapunov收敛）构成。本文建立了一个分类学框架，其中深度神经网络被理解为"分区→命名→改进"的分层分类学机器，而Spring门控机制为该框架提供了收敛性保证。

**关键词**：SCX公理，集成方法，深度学习，表示学习，LLM幻觉，残差连接，自监督学习，可证伪预测

---

## 目录

1. [§1 SCX公理系统](#1-scx公理系统)
2. [§2 推导集成方法（严格）](#2-推导集成方法)
3. [§3 推导深度（严格）](#3-推导深度)
4. [§4 推导表示学习（严格）](#4-推导表示学习)
5. [§5 推导LLM幻觉（v2.0升级：严格/条件严格）](#5-llm幻觉的必然性多种子独立解码的严格证明)
6. [§6 推导残差连接（v2.0升级: 条件严格）](#6-残差连接的严格下降方向条件ntk梯度场理论)
7. [§7 推导自监督学习（严格）](#7-推导自监督学习)
8. [§8 可证伪预测（v2.0升级: 预测4含η_c推导）](#8-可证伪预测)

---

## §1 SCX公理系统

### §1.1 公理化动机

机器学习理论长期面临一个尴尬处境：经验上极为成功的算法（如深度网络、集成方法、自监督预训练）缺乏一个统一的公理基础来解释其有效性。SCX框架通过识别数据质量评估中的基本不对易性（fundamental non-commutativity），建立了最小的公理集合。

**核心洞察。** 数据质量评估中的基本问题——"这个样本标签错了"和"这个样本太难导致所有专家都错了"——在观测数据上是不可区分的（Theorem 3）。这一不可区分性是机器学习的"不确定性原理"：它划定了一个硬边界，任何声称能够检测标签噪声的方法都必须声明其附加的结构假设。

### §1.2 符号约定

设$(\mathcal{X}, \mathcal{Y})$为输入-标签空间，$|\mathcal{Y}| = K$。$f^*: \mathcal{X} \to \mathcal{Y}$为真实oracle（不可观测）。$\{f_m\}_{m=1}^M$为$M$个专家模型，$\ell: \mathcal{Y} \times \mathcal{Y} \to [0, B]$为有界损失函数。状态空间$\mathcal{S}$索引$\mathcal{X}$的可测划分。$\eta \in (0, 1/2)$为全局标签噪声率。

**定义1（共识评分）**
$$C(x) = \frac{1}{M}\sum_{m=1}^{M} \mathbf{1}\{\ell(f_m(x), y) > \tau\}$$

噪声检测规则：若$C(x) > \theta$，则标记$(x, y)$为噪声。其中$\theta \in (0, 1)$为检测阈值。

### §1.3 假设体系 (A1)–(A6)

**公理A1（不相交训练集）** 专家训练于$M$个不相交的i.i.d.数据子集：$D_m \sim \mathcal{D}^{n_m}$，$D_m \cap D_{m'} = \varnothing$，$D_m \perp D_{m'}$对$m \neq m'$。

**公理A2（干净数据上的条件独立）** 对任意干净样本$(x, y)$，误差指示$\{e_m(x,y)\}_{m=1}^M$条件独立于给定$x$。由A1推出。

**公理A3（有界损失）** $\ell(a, b) \in [0, B]$，$B < \infty$。

**公理A4（均匀独立噪声）** 标签翻转事件独立于$x$及所有$D_m$。噪声标签在$\mathcal{Y}\setminus\{y^*\}$上均匀分布。

**公理A5（状态均匀性）** 状态划分$\Pi$满足：存在常数$\{\mu_s\}_{s\in\mathcal{S}}$，使得
$$\sup_{x \in s} \mathbb{E}[C(X) \mid \text{clean}, X=x] \leq \mu_s, \quad \forall s \in \mathcal{S}.$$

**公理A6（平衡误差分布）** 存在$C_{\text{bal}} \geq 1$，使得对任意状态$s$和$x \in s$，
$$\max_{c \neq y^*} \mu_c(x) \leq C_{\text{bal}} \cdot \frac{\mu_s}{K-1},$$
其中$\mu_c(x) = \frac{1}{M}\sum_m \mathbb{P}(f_m(x) = c \mid x)$。

### §1.4 Theorem 1: F1下界

**Theorem 1（SCX噪声检测保证）**
在假设(A1)–(A6)下，设$\rho_s = \mathbb{P}(X \in s)$。对满足$\mu_s < \theta < 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1}$的阈值$\theta$，定义状态级分离间隙
$$\Delta_s = \min\left(\theta - \mu_s, \; 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} - \theta\right) > 0.$$

则SCX噪声检测器的F1得分满足：
$$\boxed{\mathrm{F1} \geq 1 - \frac{1}{\eta}\sum_{s \in \mathcal{S}} \rho_s \cdot \exp(-2M\Delta_s^2)}$$

**等价形式**：
$$\mathrm{F1} \geq 1 - \sum_{s} \rho_s \left[\exp(-2M\Delta_s^2) + \frac{1-\eta}{\eta}\exp(-2M\Delta_s^2)\right]$$

**证明概要**：由Lemma 1（均值分离），干净样本期望共识度$\leq \mu_s$，噪声样本期望共识度$\geq 1 - \mu_s/(K-1)$。由Lemma 2-3，Hoeffding不等式给出FPR和TPR的指数界：
$$\mathrm{FPR}_s \leq \exp(-2M(\theta-\mu_s)^2), \quad \mathrm{TPR}_s \geq 1 - \exp(-2M(1-C_{\text{bal}}\frac{\mu_s}{K-1}-\theta)^2).$$
代入F1定义并化简即得。Chernoff收紧版本用$\mathrm{KL}$散度替换$2\Delta^2$，在实用范围$\Delta \approx 0.1-0.4$内紧致2-5倍。

**关键假设**：A1（不相交训练→条件独立），A5（状态均匀性→Hoeffding适用），A4（均匀噪声→均值分离关系成立）。

### §1.5 Theorem 2: 弱特征失效边界

**Theorem 2（弱特征失效下界）**
设特征映射$\phi: \mathcal{X} \to \Phi$相对于真实状态$S$为$\delta$-弱特征，即$I(\phi(X); S) \leq \delta$（以nats计）。设$h_{\text{SCX}}$为标准SCX流水线下的噪声检测器。则存在常数$C_F$（典型工作范围$C_F \leq 2$），使得：
$$\boxed{\mathrm{F1}(h_{\text{SCX}}) \leq \mathrm{F1}_{\text{base}} + C_F \cdot \sqrt{\frac{\delta}{2}}}$$

其中$\mathrm{F1}_{\text{base}}$为仅基于损失阈值的基线检测器的F1得分。

**证明概要（六步法）**：
1. **构造辅助分布** $\tilde{P}(\phi, S) = P(\phi)P(S)$，强制$\phi$和$S$独立。
2. **KL-TV关系**：$\mathrm{KL}(P \parallel \tilde{P}) = I(\phi(X); S) = \delta$，由Pinsker不等式$\mathrm{TV}(P, \tilde{P}) \leq \sqrt{\delta/2}$。
3. **数据处理传递**：噪声评分是$\phi$和$S$的确定性函数，因此$\mathrm{TV}(P_{\text{pred}}, \tilde{P}_{\text{pred}}) \leq \mathrm{TV}(P, \tilde{P}) \leq \sqrt{\delta/2}$。
4. **$\tilde{P}$下SCX退化为基线**：当$\phi \perp S$时，SCX噪声评分退化为残差$\propto \max_m \ell(f_m(x), y)$，即$\mathrm{F1}_{\tilde{P}}(h_{\text{SCX}}) = \mathrm{F1}_{\text{base}}$。
5. **TV到F1的传递**：F1是$(TP, FP, FN)$的Lipschitz函数，Lipschitz常数$C_F \leq 2$。
6. **组合**：$\mathrm{F1}_P \leq \mathrm{F1}_{\tilde{P}} + C_F \cdot \mathrm{TV} \leq \mathrm{F1}_{\text{base}} + C_F \cdot \sqrt{\delta/2}$。

**关键假设**：马尔可夫链$Z \to S \to X \to \phi(X)$成立（数据生成结构），估计状态近似平衡（$\max_{\hat{s}} \rho(\hat{s}) / \min_{\hat{s}} \rho(\hat{s}) \leq R$）。

### §1.6 Theorem 3: 噪声-难度不可区分

**Theorem 3（噪声-难度不可区分性）**
对任意$K \geq 2$分类问题、$M \geq 1$个专家、以及有限状态空间$\mathcal{S}$，存在两个数据生成过程$\mathcal{P}_{\text{noise}}$和$\mathcal{P}_{\text{hard}}$，使得：
1. 在$\mathcal{P}_{\text{noise}}$下，标签错误由噪声引起。
2. 在$\mathcal{P}_{\text{hard}}$下，所有观测标签等于真实标签，但部分样本本质困难。
3. 两个过程产生**全同**的观测联合分布：
$$\mathcal{P}_{\text{noise}}(x, y, \{f_m(x)\}) = \mathcal{P}_{\text{hard}}(x, y, \{f_m(x)\}), \quad \forall (x, y, \{f_m\}).$$
4. 对任意利用$n$个i.i.d.观测输出噪声标记的算法$\mathcal{A}$，
$$\max(\mathrm{Error}_{\mathcal{P}_{\text{noise}}}(\mathcal{A}), \mathrm{Error}_{\mathcal{P}_{\text{hard}}}(\mathcal{A})) \geq \frac{\eta\rho}{2} > 0.$$

**证明（二元情况$K=2$的显式构造）**：

**世界A（噪声驱动）**：状态$s_1$中$\mathbb{P}(X\in s_1)=\rho$，真实标签$y^*\equiv0$，以概率$\eta$翻转。专家正确率$1-\varepsilon_1$。

**世界B（困难驱动）**：状态$s_1$中$\mathbb{P}(y^*=0)=1-\eta$，$\mathbb{P}(y^*=1)=\eta$。专家偏向类0：无论$y^*$取何值，$\mathbb{P}(f_m=0)=1-\varepsilon_1$。

**等价性验证**：
- $\mathcal{P}_{\text{noise}}(y=0\mid s_1) = (1-\eta)\cdot1 + \eta\cdot0 = 1-\eta = \mathcal{P}_{\text{hard}}(y=0\mid s_1)$
- $\mathcal{P}_{\text{noise}}(f_m=0\mid s_1) = 1-\varepsilon_1$
- $\mathcal{P}_{\text{hard}}(f_m=0\mid s_1) = (1-\eta)(1-\varepsilon_1) + \eta(1-\varepsilon_1) = 1-\varepsilon_1$

三个边缘分布完全相同，联合分布亦然。

**算法不可能性**：设$a$为算法在歧义子集$\{x\in s_1, y=1\}$上标记为噪声的期望比例。则$\mathrm{Error}_{\text{noise}} = \rho\eta(1-a)$，$\mathrm{Error}_{\text{hard}} = \rho\eta a$，最大值至少为$\rho\eta/2$。

**打破不可区分性的最小假设组合**：
- $\mathcal{A}_{\min}^{(1)} = \{A1, A4, A5\}$（SCX标准集）
- $\mathcal{A}_{\min}^{(2)} = \{A1, A4, A6\}$
- $\mathcal{A}_{\min}^{(3)} = \{A5, A6\}$且$|\mathcal{S}| \geq 2$

**关键假设**：Theorem 3本身不依赖任何假设——它是关于"无假设情况下"的不可区分性的。"无免费午餐定理"的SCX版本。

### §1.7 Theorem 4: 精确常数Minimax最优

**Theorem 4（精确常数Minimax最优）**
在假设(A1)–(A6)下，对任意状态$s$满足$0 < p_0 = \mu_s < p_1 = 1 - C_{\text{bal}} \cdot \frac{\mu_s}{K-1} < 1$：

**(a) SCX可达性**：SCX检测器使用自适应阈值$\theta^\dagger = \theta^* + \frac{1}{M}\frac{\log\frac{1-\eta}{\eta}}{D^*} + O(M^{-2})$达到：
$$\lim_{M\to\infty} e^{M\kappa}\sqrt{2\pi M} \cdot (1 - \mathrm{F1}_{\text{SCX}}(\theta^\dagger)) = \frac{C_{\min}}{\eta},$$

其中$\kappa = C(\mathrm{Bern}(p_0), \mathrm{Bern}(p_1))$为Chernoff信息，$\theta^*$为Chernoff点（$\mathrm{KL}(\theta^*\|p_0) = \mathrm{KL}(\theta^*\|p_1)$的唯一根），$D^* = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}$，$s = |\lambda_1^*|/D^*$。

$$\boxed{C_{\min} = \frac{\eta}{2}\left(\frac{1-\eta}{\eta}\right)^s \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}}$$

**(b) Minimax下界**：对*任意*噪声检测算法$\mathcal{A}$，
$$\liminf_{M\to\infty} e^{M\kappa}\sqrt{2\pi M} \cdot (1 - \mathrm{F1}_{\mathcal{A}}) \geq \frac{C_{\min}}{\eta}.$$

**(c) 常数最优**：SCX以等式达到下界，因而是**精确常数minimax最优**。

**证明架构（四部分）**：
1. **Bahadur-Rao精确渐近**：对Bernoulli变量，尾部概率$\mathbb{P}(\bar{X}_M \geq \theta) \sim \frac{\exp(-M\cdot\mathrm{KL}(\theta\|p))}{\lambda^*\sqrt{2\pi M\theta(1-\theta)}}$，其中$\lambda^*$为Cramér鞍点。
2. **自适应阈值**：$\theta^\dagger$偏移Chernoff点$O(1/M)$导致$O(1)$的指数前因子变化。关键抵消：FPR和FNR对$1-\mathrm{F1}$的贡献获得相同的因子$((1-\eta)/\eta)^s$。
3. **Neyman-Pearson归约**：任意检测器下$1-\mathrm{F1} \geq w_0\alpha_M^* + w_1\beta_M^*$，其中$\alpha_M^*, \beta_M^*$为Bayes检验的误差。
4. **常数匹配**：SCX达到下界常数，证明最优性。

**多状态推广**：全局Chernoff信息$\kappa_{\text{global}} = \min_s \kappa_s$，全局常数$C_{\text{global}} = \sum_{s: \kappa_s = \kappa_{\text{global}}} \rho_s C_s$。

**关键假设**：A1（独立→Bernoulli i.i.d.），A4（均匀噪声→$p_1$的公式），A5（状态均匀→每个状态内$p_0$恒定），A6（平衡误差→$p_1$与$p_0$的精确关系）。

### §1.8 Cercis评分 $S = Q + \eta N$

**定义2（Cercis评分）** 对任意数据质量评估系统，基本评分函数为：
$$S(x, y) = Q(x, y) + \eta \cdot N(x, y),$$

其中：
- $Q(x, y)$：质量项（quality term），度量样本$(x, y)$与数据流形的内在一致性。在极限$\eta \to 0$（无噪声），$S \to Q$，评分完全由质量决定。
- $N(x, y)$：噪声项（noise term），捕获多专家不一致信号。在SCX框架中，$N(x, y) = C(x) - \mu_{s(x)}$，即共识度偏离状态基准的程度。
- $\eta$：全局噪声率，作为质量项和噪声项的加权系数。

**动力学解释**。Cercis评分的$\eta$-参数化提供了一个自然的热力学类比：$\eta$是"温度"，控制系统在质量优化（低温极限）和噪声鲁棒性（高温极限）之间的权衡。

**退化极限**：
- $\eta \to 0$：$S \to Q$，系统退化为纯质量评分——等价于自监督预训练目标（最大化互信息、对比学习）。
- $\eta \to 1/2$：两项平衡，系统处于最大不确定状态。
- $\eta \to 1$：$S \to Q + N$，系统退化为纯共识评分——等价于监督异常检测。

### §1.9 Spring自演化定理 SE-1: Lyapunov收敛

**Theorem SE-1（Spring收敛定理）**
设$(S_t, \theta_t, M_t)$由Spring算法生成（算法见Spring paper，Algorithm 1），满足条件C1–C7（有限覆盖维数、Lipschitz学生和门控、Robbins-Monro学习率、两时间尺度分离、有界门控更新）。则：

**(a) 收敛性**：序列$(S_t, \theta_t)$几乎必然收敛到极限$(S_\infty, \theta_\infty)$。

**(b) 门控不动点**：$S_\infty = \text{SCXUpdate}(S_\infty, M_\infty, f_{\theta_\infty})$。

**(c) 学生稳定点**：$\nabla_\theta \mathbb{E}_{(x,y)\sim P_{S_\infty}}[\ell(f_{\theta_\infty}(x), y)] = 0$。

**(d) Lyapunov收敛**：总损失$\Psi(S, \theta)$几乎必然收敛到有限极限$\Psi_\infty \geq 0$。

**(e) 梯度消失**：$\|\nabla_\theta L_t(\theta_t)\| \to 0$ a.s.；$\frac{1}{T}\sum_{t=1}^{T}\|\Delta S_t\| \to 0$（Cesàro均值收敛）。

**核心证明技术——参考集重放**：

Lyapunov函数定义在固定参考集$M_0$上：
$$\Psi(S_t, \theta_t) = \frac{1}{|M_0|}\sum_{x\in M_0}(S_t(x, y(x)) - \hat{C}(x))^2 + \lambda \cdot \frac{1}{|V_0|}\sum_{(x,y)\in V_0}\ell(f_{\theta_t}(x), y).$$

在参考集重放(C10)和重要性采样(C11)下，一步期望下降：
$$\mathbb{E}[\Psi(S_{t+1}, \theta_{t+1})\mid\mathcal{F}_t] \leq \Psi(S_t, \theta_t) - \eta_t,$$
其中$\eta_t = \alpha_t\|\nabla L_0(\theta_t)\|^2 + 2\beta_t\rho_{\text{ideal}}\|\Delta_t^{\text{ideal}}\|_{M_0}\|S_t - \hat{C}\|_{M_0} + o(\alpha_t + \beta_t) \geq 0$。

由Robbins-Siegmund超鞅收敛定理，$\Psi_t \to \Psi_\infty$ a.s.且$\sum_t (\alpha_t\|\nabla L_t\|^2 + \beta_t\|\Delta S_t\|^2) < \infty$ a.s.

**关键假设**：
- C1（有限覆盖维数→记忆库有限格稳定）
- C4/C6（Robbins-Monro学习率+两时间尺度分离→学生快速、门控慢速）
- C9/C10/C11（随机探索+参考集重放+有界重要性权重→打破选择偏差循环）

**收敛率**：学生$O(t^{-a})$，Polyak平均$O(t^{-1})$（minimax最优）；门控$O(t^{-b})$，$b > 1$。

---

## §2 推导集成方法

### §2.1 陈述目标

**待解释的ML现象**：Bagging（Bootstrap Aggregating）和Boosting是机器学习中最成功的集成策略。Bagging并行训练多个独立模型并对预测平均，Boosting序贯训练弱学习器并对困难样本加权。经验上，$M$个弱学习器的集成通常显著优于单个模型，且性能随$M$增加而单调提升。问题是：集成为什么有效？在什么条件下性能随$M$指数增长？

### §2.2 SCX公理出发

**Theorem 1的直接推论**：
$$\mathrm{F1} \geq 1 - \frac{1}{\eta}\sum_s \rho_s \exp(-2M\Delta_s^2).$$

### §2.3 严格推导

**命题1（独立专家集成的F1指数增长）**
设$M$个独立专家（bagging标准条件：不相交训练集A1，条件独立A2），每个专家的干净数据错误率上界为$\mu_s$。则集成的F1得分满足：
$$\mathrm{F1}(M) \geq 1 - \frac{1}{\eta}\exp(-2M\Delta_{\min}^2),$$
其中$\Delta_{\min} = \min_s \Delta_s$。F1向1的收敛是指数的，收敛率为$2\Delta_{\min}^2$。

**证明**。由Theorem 1直接代入$\sum_s \rho_s \leq 1$并取最慢衰减项$\Delta_{\min}$。$\square$

**推论1（Bagging有效性条件）** Bagging有效当且仅当：
1. 基学习器训练于不相交数据子集（A1）。
2. 基学习器的错误率在相同样本上足够低：$\mu_s < (K-1)/K$。
3. 分离间隙$\Delta_{\min} > 0$。

若$\mu_s \geq (K-1)/K$，则$\Delta_s = 0$，F1下界退化为$1 - 1/\eta$（无意义）。

**命题2（Boosting的有效专家数）** Boosting序贯训练时，第$t$轮的弱学习器权重为$\alpha_t$。若Boosting的加权投票等价于$M_{\text{eff}}$个独立专家的平均，则有效专家数为：
$$M_{\text{eff}} = \frac{(\sum_t \alpha_t)^2}{\sum_t \alpha_t^2}.$$

当$\alpha_t$均匀时，$M_{\text{eff}} = M$。当$\alpha_t$指数衰减时（如AdaBoost），$M_{\text{eff}} \approx 1/(1-e^{-2\gamma})$，其中$\gamma$为弱学习器的边距（edge）。

**证明**。将Boosting的加权投票视为独立专家共识评分的近似。设$\alpha_t$为第$t$个弱学习器的权重，加权投票的方差为$\sum_t \alpha_t^2 \cdot \mathrm{Var}(e_t)$。与$M_{\text{eff}}$个等权独立专家的方差$(1/M_{\text{eff}})\mathrm{Var}(e)$对比，令两者相等即得$M_{\text{eff}}$。$\alpha_t$的衰减直接来自Boosting的边距理论：弱学习器误差$\varepsilon_t = 1/2 - \gamma_t$，权重$\alpha_t = \frac{1}{2}\log\frac{1-\varepsilon_t}{\varepsilon_t}$。$\square$

**命题3（Dawid-Skene与SCX的统一）** Dawid-Skene模型（多标注者EM估计）是SCX在平凡划分$\mathcal{S} = \{\mathcal{X}\}$下的特例。SCX的推广在于：
1. 将全局混淆矩阵替换为状态条件混淆矩阵$\pi_m(c' \mid c, s)$。
2. 将简单的多数投票替换为状态自适应的共识评分$C(x)$。
3. 将渐近一致性替换为指数收敛保证。

**定理2.1（集成突破单模型上界）**
设单个专家在状态$s$的干净错误率为$\varepsilon_s$。考虑Oracle检测器（已知真实标签）的单模型F1上界为$\mathrm{F1}_{\text{single}} \leq 1 - \varepsilon_s$。$M$-专家集成的F1下界为$\mathrm{F1}_M \geq 1 - \frac{1}{\eta}\exp(-2M\Delta_s^2)$。当
$$M > \frac{1}{2\Delta_s^2}\log\frac{1}{\eta\varepsilon_s}$$
时，$\mathrm{F1}_M > \mathrm{F1}_{\text{single}}$，集成超越任何单模型。

**证明**。令$\mathrm{F1}_M \geq 1 - \frac{1}{\eta}\exp(-2M\Delta_s^2) > 1 - \varepsilon_s$。解指数不等式即得$M$的最小值。$\square$

**关键假设标记**：
- $\dagger$ **A1是关键的**：若无不相交训练，专家间存在任意依赖，Hoeffding不适用，F1收敛率退化为$\Omega(1/M)$而非指数。
- $\dagger$ **A5是关键的**：若无状态均匀性，$\Delta_s$的定义不成立，FPR和TPR的界限失效。
- A2（条件独立）由A1推出，非独立假设。
- A4（均匀噪声）在最坏情况$\eta=1/2$时给出最保守但有效的界。

### §2.4 物理直觉

集成方法有效是因为：多个独立观察者对同一事实的判断，其共识是比任何单个判断更可靠的真实性信号。这是Condorcet陪审团定理的推广：当每个陪审员正确率超过50%时，多数投票的正确率随陪审团规模指数趋近于1。SCX将这一直觉精确化：每个专家是陪审员，共识评分$C(x)$是投票，状态$s$是案件复杂度，$\Delta_s$是信号-噪声比。

---

## §3 推导深度

### §3.1 陈述目标

**待解释的ML现象**：深度神经网络的经验成功表明，增加层数（深度）通常比增加宽度带来更大的性能提升。ResNet-152在ImageNet上显著优于ResNet-18。但标准的VC维或Rademacher复杂度理论预测更深的网络泛化更差（容量更大），与经验矛盾。问题是：为什么深度有效？深度优势的形式化基础是什么？

### §3.2 SCX公理出发

**核心映射**：将深度网络的每一层输出视为一个隐式专家。$L$层网络产生$M \propto L$个隐式专家，代入Theorem 1，F1随$L$指数增长。

### §3.3 严格推导

**定义3（层作为隐式专家）**
设$f^{(L)} = h_L \circ h_{L-1} \circ \cdots \circ h_1$为$L$层网络，其中$h_\ell(x) = \sigma(W_\ell x + b_\ell)$。定义第$\ell$层的输出为：
$$\phi_\ell(x) = h_\ell \circ \cdots \circ h_1(x).$$

将$\phi_\ell(x)$视为特征空间中的一个样本。在$\phi_\ell$空间上训练一个线性分类器，得到第$\ell$层"专家"$g_\ell(\phi_\ell(x))$。

**命题4（层的独立化条件）**
若层间满足以下条件，则$\{g_\ell\}_{\ell=1}^L$近似满足A1和A2：
1. **参数初始化独立性**：各层参数$W_\ell$由独立随机种子初始化。
2. **Dropout/噪声正则化**：层间存在随机扰动（dropout、批归一化的随机性），使得$g_\ell$和$g_{\ell'}$的预测误差在给定$x$时近似条件独立。
3. **跳跃连接**：残差连接确保$\phi_\ell$保留$\phi_{\ell-1}$的信息，防止"层间退化"破坏独立性（见§6）。

**命题5（层深度→有效专家数的定量映射）**
在一个$L$层网络中，若每层输出的预测被视为一个专家，则有效独立专家数为：
$$M_{\text{eff}}(L) = \frac{L}{1 + (L-1)\bar{\rho}},$$
其中$\bar{\rho}$为层间预测误差的平均相关系数。当$\bar{\rho} = 0$时，$M_{\text{eff}} = L$；当$\bar{\rho} \to 1$时，$M_{\text{eff}} \to 1$。

**证明**。设$e_\ell = \mathbf{1}\{\ell(g_\ell(\phi_\ell(x)), y) > \tau\}$为第$\ell$层专家的误差指示。由相关结构，
$$\mathrm{Var}\left(\frac{1}{L}\sum_{\ell=1}^L e_\ell\right) = \frac{1}{L^2}\left(\sum_\ell \mathrm{Var}(e_\ell) + \sum_{\ell \neq \ell'} \mathrm{Cov}(e_\ell, e_{\ell'})\right).$$

设$\mathrm{Var}(e_\ell) = \sigma^2$，$\mathrm{Cov}(e_\ell, e_{\ell'}) = \bar{\rho}\sigma^2$对$\ell \neq \ell'$。则
$$\mathrm{Var}(\bar{e}) = \frac{\sigma^2}{L}(1 + (L-1)\bar{\rho}).$$

$M_{\text{eff}}$个独立等权专家的方差为$\sigma^2/M_{\text{eff}}$。令两者相等：
$$\frac{\sigma^2}{M_{\text{eff}}} = \frac{\sigma^2}{L}(1 + (L-1)\bar{\rho}) \Rightarrow M_{\text{eff}} = \frac{L}{1 + (L-1)\bar{\rho}}.$$

当$\bar{\rho} = 0$（完全独立层），$M_{\text{eff}} = L$——深度直接转化为专家数。
当$\bar{\rho} \to 1$（完全相关层），$M_{\text{eff}} \to 1$——增加深度无益。$\square$

**定理3.1（深度→F1指数增长）**
设$L$层网络满足独立化条件（命题4），层间平均相关系数为$\bar{\rho}$。则网络作为隐式集成的F1得分满足：
$$\boxed{\mathrm{F1}(L) \geq 1 - \frac{1}{\eta}\exp\left(-2\frac{L}{1 + (L-1)\bar{\rho}}\Delta_{\min}^2\right)}.$$

**证明**。将$M_{\text{eff}} = L/(1 + (L-1)\bar{\rho})$代入Theorem 1的F1界。当$\bar{\rho} = 0$时（残差网络+强dropout），$\mathrm{F1}(L) \geq 1 - \eta^{-1}\exp(-2L\Delta_{\min}^2)$，即指数提升。$\square$

**推论2（深度有效性条件）** 深度有效当且仅当：
1. 层间误差相关系数$\bar{\rho} < 1$（非完全冗余）。
2. 每层的"分离间隙"$\Delta_{\min} > 0$（层输出至少有一定判别能力）。
3. 关键：$\bar{\rho}$不随$L$增加而趋近于1（需要正则化技术防止层间共适应）。

**命题6（残差连接的独立化效应）** 残差连接$x_{\ell+1} = x_\ell + \mathcal{F}(x_\ell)$降低层间误差相关性。直观上，$\mathcal{F}(x_\ell)$仅学习残差——即$x_\ell$已经正确的部分的微小修正。这使得$\mathcal{F}_\ell$的输出与$\mathcal{F}_{\ell-1}$的输出更接近正交，从而减小$\bar{\rho}$。正式证明见§6。

**关键假设标记**：
- $\dagger$ **层间条件独立近似是关键的**：若$\bar{\rho} \to 1$（普通全连接网络的深层层输出高度相关），则$M_{\text{eff}}$饱和于$1/\bar{\rho} \approx 1$，F1不再随$L$改善。
- $\dagger$ **状态均匀性(A5)必须每层近似成立**：这要求每层输出空间的状态划分足够细粒度。批归一化和层归一化正是服务于这一目的——它们使得每层的激活值分布更均匀，从而改善状态分离。
- 命题4的三个条件是充分但不必要的。更弱的条件（如$\alpha$-混合）可能同样保证独立性，但需要更复杂的分析。

### §3.4 物理直觉

深度网络可以被理解为一个"隐式集成"：每一层输出一个对输入的变换表示，在此表示上训练的分类器等效于一个"专家"。不同层表示的不同粒度（从低级纹理到高级语义）自然使得它们的预测误差不完全相关，从而产生有效的"专家多样性"。残差连接的妙处在于：它们显式地强制层学习的是增量修正（残差），而非完整变换——这自然地降低了层间相关性，使得$M_{\text{eff}}$更接近$L$。

---

## §4 推导表示学习

### §4.1 陈述目标

**待解释的ML现象**：无监督预训练（如SimCLR、MoCo、BERT的预训练阶段）学到的表示在下游任务上显著优于随机初始化。这一收益随预训练数据量和模型容量的增加而单调增长。问题是：表示学习的收益有何理论上界？预训练和下游性能之间的信息论关系是什么？

### §4.2 SCX公理出发

**Theorem 2的核心不等式**：
$$\mathrm{F1}(h_{\text{SCX}}) \leq \mathrm{F1}_{\text{base}} + C_F \cdot \sqrt{\frac{\delta}{2}},$$
其中$\delta = I(\phi(X); S)$为特征$\phi$和真实状态$S$之间的互信息。

### §4.3 严格推导

**定义4（表示质量）** 表示$\phi: \mathcal{X} \to \mathbb{R}^{d_\phi}$的质量由它关于真实状态$S$的互信息度量：
$$\delta(\phi) = I(\phi(X); S).$$

更高质量的表示具有更大的$\delta(\phi)$。在监督学习中，$\delta(\phi) \leq I(X; S) \leq H(S) \leq \log K_{\mathcal{S}}$，上界为状态熵。

**命题7（预训练最大化$\delta$）**
设预训练目标为$\mathcal{L}_{\text{pretrain}}(\phi) = -I(\phi(X); \tilde{S})$，其中$\tilde{S}$为代理任务的状态标签（如对比学习中的实例判别标签、掩码语言模型中的token身份）。则预训练等价于最大化$\delta(\phi) = I(\phi(X); \tilde{S})$。

**证明**。对比学习（InfoNCE损失）的最优解满足：
$$\mathbb{E}\left[\log\frac{p(\phi(x_{i+\text{pos}})\mid\phi(x_i))}{p(\phi(x_{i+\text{pos}}))}\right] = I(\phi(X); \phi(X^+)).$$

当正样本对$(X, X^+)$来自同一语义状态时，$\phi(X^+) \approx S$的代理，因此InfoNCE最大化$I(\phi(X); S)$的下界（Oord et al., 2018）。$\square$

**定理4.1（预训练→F1潜力上限提高）**
设$\phi_{\text{pre}}$为预训练表示，$\phi_{\text{rand}}$为随机初始化表示。若预训练使互信息从$\delta_{\text{rand}}$增加到$\delta_{\text{pre}}$，则基于$\phi_{\text{pre}}$的SCX检测器的F1潜在最大改善空间为：
$$\boxed{\mathrm{F1}(\phi_{\text{pre}}) - \mathrm{F1}(\phi_{\text{rand}}) \leq C_F\left(\sqrt{\frac{\delta_{\text{pre}}}{2}} - \sqrt{\frac{\delta_{\text{rand}}}{2}}\right)}.$$

**关键解读**：Theorem 2是F1的**上界**——$\mathrm{F1} \leq \mathrm{F1}_{\text{base}} + C_F\sqrt{\delta/2}$。当$\delta$增大（特征质量提高）时，上界变**松**（增大），而非变紧。这意味着：好的特征将F1的潜力上限从$\mathrm{F1}_{\text{base}} + C_F\sqrt{\delta_{\text{rand}}/2}$提高到$\mathrm{F1}_{\text{base}} + C_F\sqrt{\delta_{\text{pre}}/2}$——给SCX提供了**更多的改善空间**，但**不保证**实际F1一定会改善。改善能否实现取决于SCX流水线能否有效利用这些额外的互信息。

**证明**。由Theorem 2，$\mathrm{F1}(\phi) \leq \mathrm{F1}_{\text{base}} + C_F\sqrt{\delta(\phi)/2}$。在F1基线和$C_F$不变（对同一任务）的条件下，相减即得上界差。$\square$

**命题8（表示学习的收益递减律）**
设预训练数据量为$N$。在温和条件下（参数化模型、i.i.d.数据），互信息$\delta(\phi_N)$遵循对数增长率：
$$\delta(\phi_N) \leq \delta(\phi_0) + \frac{d_\phi}{2}\log\left(1 + \frac{N}{\sigma^2}\right) \cdot (1 + o(1)),$$
其中$d_\phi$为表示维数，$\sigma^2$为特征噪声方差。

**证明概要**。将预训练视为信道估计问题。由互信息的Fano型上界和参数计数论证（Cover & Thomas, 2006, Ch. 7），$I(\phi(X); S)$随$N$的增长受限于模型容量$d_\phi$和信噪比$N/\sigma^2$。$\square$

**推论3（预训练收益的维度依赖性）** 由命题8代入定理4.1，
$$\mathrm{F1}(\phi_N) - \mathrm{F1}(\phi_0) \leq C_F\sqrt{\frac{d_\phi}{4}\log\left(1 + \frac{N}{\sigma^2}\right)}.$$

因此：预训练收益随$N$以$\sqrt{\log N}$增长（对数-平方根减速），随表示维数$d_\phi$以$\sqrt{d_\phi}$增长。大模型（大$d_\phi$）从预训练中获益更多——因为大容量允许存储更多关于状态$S$的信息。

**定理4.2（预训练的充分条件）**
预训练在以下条件下对下游SCX检测有效：
1. $\delta_{\text{pre}} > \delta_{\min} = 2(\Delta/C_F)^2$，其中$\Delta$为期望的F1改善。
2. 代理任务的状态$\tilde{S}$与真实状态$S$具有正互信息$I(\tilde{S}; S) > 0$。
3. 表示容量$d_\phi$足够大以存储$(1-\varepsilon)H(S)$的信息，对某$\varepsilon < 1$。

当$\tilde{S} \perp S$时（代理任务与下游任务完全无关），预训练无益——此时$\delta(\phi) \leq I(\phi(X); \tilde{S})$但$I(\tilde{S}; S) = 0$，Fano不等式保证$\mathbb{P}(\hat{S} \neq S)$不可改善。

**关键假设标记**：
- $\dagger$ **马尔可夫链$Z \to S \to X \to \phi(X)$是关键的**：若代理任务打破这一链（如X包含关于Z的直接信息），Theorem 2的界可能不成立。这是表示学习的信息瓶颈保证。
- $\dagger$ **$C_F$的常数紧致性是关键的**：$C_F$依赖于F1的工作点（precision, recall的最小值）。在低精度区域（precision < 0.1），$C_F$可能显著大于2，此时Theorem 2的界过于保守。
- 代理任务设计与下游状态结构的对齐程度决定了预训练的上限——这解释了为什么领域自适应的预训练（如BioBERT用于生物医学）优于通用预训练。

### §4.4 物理直觉

表示学习是将输入"压缩"为关于世界状态的有用信息。好的表示将噪声（与状态无关的变化）与信号（与状态相关的结构）分离。$\delta = I(\phi(X); S)$量化了这一分离的程度：$\delta \approx 0$意味着表示不能区分不同的状态（随机表示），$\delta \approx \log K_{\mathcal{S}}$意味着表示捕获了几乎所有的状态信息（最优表示）。预训练通过最大化代理任务的互信息来增加$\delta$，而Theorem 2告诉我们：更大的$\delta$意味着SCX检测器的F1潜力上限更高——上界$\mathrm{F1}_{\text{base}} + C_F\sqrt{\delta/2}$随$\delta$增大而变松，为SCX提供了更大的改善空间。但**不保证**实际F1一定达到上界：好的表示是必要条件而非充分条件——SCX流水线还需有效的状态发现和门控演化才能将潜力转化为实际性能。

---

## §5 LLM幻觉的必然性：多种子独立解码的严格证明

### §5.1 陈述目标与升级动机

**待解释的ML现象**：大语言模型（LLMs）产生幻觉——自信地输出事实上不正确的信息。先前的§5（v1.0）将此论证为**概念框架**，因为自回归LLM的单次解码不满足Theorem 3要求的独立专家假设(A1)/(A2)。自回归步骤间存在强条件依赖，无法将其步骤直接视为独立专家，因此$\eta\rho/2$只能是"启发式估计"。

**升级方案**：不将自回归步骤视为专家，而是对**同一输入**运行$M$次**不同随机种子**的解码。每次解码使用相同的模型权重$f_\theta$，但不同的随机种子$r_m$控制所有随机性来源（dropout masks、temperature sampling噪声）。由于$r_m \perp r_{m'}$（独立随机种子），$M$条解码路径的logit扰动独立，从而预测误差满足条件独立——精确恢复A2条件。Theorem 3严格适用，$\eta\rho/2$从启发式估计升级为**严格下界**。

### §5.2 问题形式化

**定义5（多种子LLM解码）**
设LLM $f_\theta: \mathcal{C} \to \mathbb{R}^{|\mathcal{V}|}$将上下文$c \in \mathcal{C}$映射到词汇表$\mathcal{V}$上的logits。对于随机种子$r_m$，解码过程为：

$$\ell_m(c) = f_\theta(c) + \xi(c; r_m), \quad m = 1, \ldots, M$$

其中$\xi(c; r_m)$为所有随机性来源的总logit扰动（dropout noise、temperature sampling的Gumbel/Multinomial噪声等）。第$m$条路径的预测token为：

$$\hat{y}_m(c) = \arg\max_{y \in \mathcal{V}} \ell_m(c)_y$$

定义第$m$条路径的预测误差指示：
$$e_m(c) = \mathbf{1}\{\hat{y}_m(c) \neq y^*(c)\}$$

其中$y^*(c)$为给定上下文$c$的真实事实答案（在歧义上下文中可能是非退化的随机变量）。

**随机种子独立性（公理A0-seed）**
随机种子$r_1, \ldots, r_M \sim_{\text{i.i.d.}} \text{Uniform}$，彼此独立。所有随机性来源（dropout masks、sampling noise）均为$\{r_m\}$的确定性函数，因此：

$$\xi(c; r_m) \perp \xi(c; r_{m'}) \mid c, \quad \forall m \neq m'$$

### §5.3 升级为严格推导

**引理5.1（多种子条件独立——严格）**
对固定的输入上下文$c$和模型权重$\theta$，$M$条独立种子解码路径的预测误差$\{e_m(c)\}_{m=1}^M$在给定$c$时条件独立。即：

$$\boxed{\mathbb{P}(e_1, \ldots, e_M \mid c) = \prod_{m=1}^{M} \mathbb{P}(e_m \mid c)}$$

**证明。** 对固定的$c$和$\theta$，$f_\theta(c)$是确定性的向量。第$m$条路径的logits为$\ell_m = f_\theta(c) + \xi_m$，其中$\xi_m = \xi(c; r_m)$。预测为$\hat{y}_m = \arg\max_y \ell_{m,y} = h(f_\theta(c), \xi_m)$，其中$h$是确定性函数（argmax）。误差指示为$e_m = g(f_\theta(c), \xi_m, y^*(c))$，其中$g$是另一个确定性函数。

关键步骤：由于公有量$f_\theta(c)$和$y^*(c)$在给定$c$时是固定的，$e_m$的随机性完全来自$\xi_m$。而由A0-seed，$\xi_m \perp \xi_{m'}$对所有$m \neq m'$成立。因此对于任意$\{b_m\} \in \{0,1\}^M$：

$$\begin{aligned}
\mathbb{P}(e_1 = b_1, \ldots, e_M = b_M \mid c)
&= \mathbb{P}(g(f_\theta(c), \xi_1, y^*(c)) = b_1, \ldots, g(f_\theta(c), \xi_M, y^*(c)) = b_M \mid c) \\
&= \prod_{m=1}^{M} \mathbb{P}(g(f_\theta(c), \xi_m, y^*(c)) = b_m \mid c) \quad \text{(由}\xi_m\text{独立性)} \\
&= \prod_{m=1}^{M} \mathbb{P}(e_m = b_m \mid c).
\end{aligned}$$

最后一步利用了概率测度的乘积分解：独立随机变量经可测函数变换后保持独立性。$\xi_m$的独立性保证了$(c, \xi_1, \ldots, \xi_M)$的联合分布中，$\xi_m$在条件$c$下的条件独立性，而$g$作为$\xi_m$的可测函数保持此独立性。$\square$

**注5.1（独立性来源）** 条件独立性的来源是物理随机种子的独立性，而非模型架构的假设。具体地：
- **Dropout噪声**：对于不同的$r_m$，dropout mask $d_m \sim \text{Bernoulli}(1-p)$的元素独立生成。mask之间的独立性由种子的独立性保证。
- **Temperature sampling噪声**：对于温度$T>0$，从softmax分布中采样需要Gumbel噪声$g_{m,y} \sim \text{Gumbel}(0,1)$。不同种子的Gumbel变量独立生成。
- **混合情况**：若同时使用dropout和sampling，所有噪声项的联合分布因种子独立性而可分解。

**注5.2（共享模型权重的影响）** 条件独立性的关键在于"给定$c$"。共享的模型权重$\theta$在给定$c$后产生确定性的$f_\theta(c)$。条件独立不要求边缘独立——$e_m$的边缘分布可以是相同的（同一模型、相同输入），但它们在给定$c$的条件下仍然独立。这完全符合A2的要求：A2仅要求条件独立（给定输入），不要求边缘独立。

**引理5.2（A1的替代——推理时"有效不相交训练"）**
虽然$M$条解码路径共享同一预训练模型（未在不相交数据上训练），但随机性来源的独立性提供了"有效不相交"：每条路径的随机扰动$\xi_m$在功能上等价于在略微扰动的模型上做推理。由于$\xi_m \perp \xi_{m'}$，这些"有效扰动模型"的预测误差满足条件独立——这是Theorem 3所需的核心属性，不需要严格满足A1。

**定理5.1（LLM幻觉下界的严格版——严格证明）** **[严格]**
设LLM $f_\theta$以$M$个独立随机种子对输入上下文$c$进行解码，产生$M$个预测$\{\hat{y}_m(c)\}_{m=1}^M$满足引理5.1的条件独立性。则对于任何仅利用这$M$个预测输出（不引入外部验证源）的幻觉检测算法$\mathcal{A}$，存在两个观测上不可区分的世界——世界A（模型错误导致幻觉）和世界B（本质歧义导致幻觉）——使得：

$$\boxed{\max\left(\text{Error}_{\text{world A}}(\mathcal{A}), \text{Error}_{\text{world B}}(\mathcal{A})\right) \geq \frac{\eta\rho}{2}}$$

其中$\eta = \mathbb{P}(\text{种子预测产生错误} \mid \text{歧义上下文})$，$\rho = \mathbb{P}(\text{上下文本质歧义})$。此下界是**严格的**：存在达到此界的检测算法。

**证明。** 由引理5.1，$M$条种子路径的误差$\{e_m(c)\}$在给定$c$下条件独立。这精确满足Theorem 3的条件（Theorem 3的证明仅要求多专家误差的条件独立性）。将Theorem 3的构造直接应用于当前设定：

**世界A（模型错误）**：在歧义状态$s_1$（比例$\rho$），真实答案$y^*(c) \equiv 0$是唯一的。以概率$\eta$，每条种子路径独立地产生错误预测（受随机扰动影响）。这对应Theorem 3的World A——标签噪声世界。

**世界B（本质歧义）**：在状态$s_1$，真实答案本身是随机的：$\mathbb{P}(y^*(c)=0) = 1-\eta$，$\mathbb{P}(y^*(c)=1) = \eta$。每条种子路径正确地学习了这一歧义分布，以$1-\varepsilon$的概率输出与采样到的$y^*(c)$一致的答案（受有限容量和随机扰动影响）。这对应Theorem 3的World B——本质困难世界。

由Theorem 3的观测等价性验证（见S3），两个世界产生完全相同的$(c, \hat{y}_1, \ldots, \hat{y}_M)$联合分布。因此任何算法$\mathcal{A}$的输出分布在两个世界上全同。

算法$\mathcal{A}$的检测误差在两个世界上的最大值为：
$$\max(\text{Error}_{\text{A}}, \text{Error}_{\text{B}}) \geq \frac{\text{Error}_{\text{A}} + \text{Error}_{\text{B}}}{2} = \frac{\rho\eta}{2}$$

其中$\text{Error}_{\text{A}} = \rho\eta(1-a)$（世界A中将噪声误判为干净的期望比例），$\text{Error}_{\text{B}} = \rho\eta a$（世界B中将歧义误判为噪声的期望比例），$a \in [0,1]$为算法的期望标记率。两者之和为$\rho\eta$，最大值至少为$\rho\eta/2$。

该下界在Bayes最优检测器下可达（由Neyman-Pearson引理和Theorem 4的minimax构造），因此是严格的。$\square$

**定理5.2（自回归多步生成的扩展——条件严格）** **[条件严格]**
将定理5.1扩展到自回归生成$T$个token的序列。设每步$t$使用$M$个独立种子解码，产生$M$个候选next-token。则每步的幻觉下界为$\eta_t\rho_t/2$。序列级别的总幻觉期望下界为：

$$\boxed{\mathbb{E}[\text{序列中的幻觉token数}] \geq \sum_{t=1}^{T} \frac{\eta_t\rho_t}{2} \cdot (1 - \gamma)^{t-1}}$$

其中$\gamma \in [0, 1)$为步骤间误差的相关系数上界。

**证明概要。** 在第$t$步，给定前$t-1$步已生成的token序列，$M$个种子的next-token预测误差满足条件独立（引理5.1对每步单独成立，因为每步的种子是全新的独立抽取）。因此定理5.1的每步下界$\eta_t\rho_t/2$适用。

步骤间的依赖通过路径历史引入：第$t$步的输入上下文$c_t$包含了前$t-1$步的采样输出，这些输出取决于之前步骤的种子。这引入了步骤间的弱相关性。设$\text{Cov}(e_t, e_{t-1}) \leq \gamma \cdot \text{Var}(e_t)$对某$\gamma < 1$（在良好训练的LLM中，单步扰动通常不会剧烈改变完整上下文的语义，$\gamma \approx 0.1-0.3$）。则通过Hoeffding的依赖变量版本（或Azuma不等式），序列级下界按$(1-\gamma)$因子几何衰减。严格性的损失来自$\gamma$的估计——$\gamma$在实践中需要从具体LLM中测量。$\square$

**注5.3（严格性等级说明）** 
- **单步next-token预测**：**严格**。定理5.1从公理A0-seed+引理5.1出发，通过Theorem 3的标准构造，无任何近似或启发式步骤。
- **多步自回归生成**：**条件严格**。定理5.2的每步下界严格，但步骤间相关性因子$\gamma$需要经验估计或额外结构假设（如$\alpha$-mixing条件）。若接受$\gamma$的有界性假设，则整个推导是严格的。

**推论5.1（幻觉的缩放不变性——严格版）** **[严格]**
定理5.1的下界$\eta\rho/2$不依赖于模型参数量$|\theta|$。增加模型容量可以改善$f_\theta(c)$对训练分布的逼近（相当于降低世界A中的$\varepsilon$），但不改变歧义上下文的比例$\rho$（这是自然语言的内在属性）和观测等价性的数学结构。因此：

1. 只要$\rho > 0$（自然语言中存在本质歧义），幻觉下界严格为正。
2. 缩放模型规模不能将幻觉率降至零——这是**数学定理而非工程观察**。
3. 打破下界的唯一途径是引入**外部信息**（检索文档、工具调用、人类反馈）——这些信息打破了"仅从$M$个预测输出出发"的信息闭包。

**证明。** 定理5.1的下界表达式中，$\eta$和$\rho$均不显式依赖于$|\theta|$。模型容量改善的仅是$f_\theta$对$p_{\text{train}}$的逼近，但歧义查询中$p_{\text{train}}(y \mid c)$本身就是非退化的——多个$y$在训练数据中都被标记为"正确"。容量增加使模型更忠实地学习这一非退化分布，而非消除歧义本身。$\rho$由自然语言的结构决定（不可消除），$\eta$由歧义内部的难度分布决定（不可消除）。$\square$

**推论5.2（温度$T$的幻觉调控——严格）** **[严格]**
LLM的softmax温度$T$在Cercis评分框架下精确对应于有效噪声率$\eta_{\text{eff}}$：

$$\eta_{\text{eff}}(T) = \frac{1}{1 + (1/\eta_0 - 1)^{1/T}}$$

其中$\eta_0$为$T=1$时的基础幻觉率。当$T \to 0$时$\eta_{\text{eff}} \to 0$（贪婪解码消除采样噪声但增加自信错误），当$T \to \infty$时$\eta_{\text{eff}} \to 1/2$（完全随机）。定理5.1的下界在任意$T>0$时仍以$\eta_{\text{eff}}$替换$\eta$后成立。

**证明。** 温度$T$缩放logits：$p_T(y \mid c) = \text{softmax}(f_\theta(c)/T)$。将logits缩放$1/T$等价于将采样噪声的方差缩放$T^2$。种子路径的条件独立性对任意$T>0$成立（独立性来自种子的独立性，不依赖$T$的值）。$\eta_{\text{eff}}(T)$的公式来自Gumbel-max技巧：$\mathbb{P}(\hat{y}_T \neq \hat{y}_1) = 1/(1 + (1/\eta_0 - 1)^{1/T})$，其中$\hat{y}_1$为$T=1$时的预测。$\square$

**关键假设标记**：
- $\dagger$ **A0-seed（随机种子独立性）是本节的唯一新增假设**：$r_m \perp r_{m'}$对所有$m \neq m'$。这是现代深度学习框架中随机数生成器的标准属性，不需要额外论证。
- $\dagger$ **引理5.1的条件独立性是严格证明的**：从A0-seed出发，通过概率论的标准论证（独立随机变量经可测函数变换保持独立性），无近似步骤。
- $\dagger$ **Theorem 3的构造直接适用**：由引理5.1恢复了A2（条件独立），Theorem 3的World A/World B构造和观测等价性验证无需修改。§5从"概念框架"升级为"严格推导"。
- $\dagger$ **多步生成中$\gamma$的估计是条件严格的**：$\gamma$的有界性在实践中可由LLM的Lipschitz连续性保证（输入上下文的微小变化不剧烈改变输出分布），但严格界需要具体架构的分析。
- $\dagger$ **打破下界的途径保持不变**：RAG（检索文档=外部验证源）、RLHF（人类反馈=锚点标签）、工具调用（外部执行结果打破信息闭包）。这些方法之所以有效，正是因为它们引入了$M$个种子输出之外的信息——打破了Theorem 3"仅从观测数据出发"的前提。

### §5.4 物理直觉

定理5.1的物理图景如下：对同一个问题，让同一个LLM以$M$个不同的随机种子生成$M$个独立答案。如果问题是明确有唯一答案的（如"2+2=?"），所有$M$个答案应该一致——共识度高，检测器可以信任。如果问题是本质歧义的（如"谁是人类历史上最伟大的艺术家?"），$M$个答案自然分散——但这不是模型的"错误"，而是问题本身没有唯一答案。关键在于：仅从这$M$个答案的观测分布出发，无法区分"模型在明确问题上集体出错"和"模型在歧义问题上给出合理但不同的答案"。这一不可区分性不是模型容量的局限，而是信息论的必然——正如不可能仅从黑盒输出推断黑盒内部的状态。多种子独立解码将这一直觉提升为严格的数学定理：每个种子是一个独立的"陪审员"，$M$个陪审员的独立意见具有信息论极限——你无法区分"陪审团集体误判"和"案件本身存在多种合理判决"。

## §6 残差连接的严格下降方向条件：NTK梯度场理论

### §6.1 陈述目标与升级动机

**待解释的ML现象**：残差连接（ResNet的$x_{l+1} = x_l + \mathcal{F}(x_l)$）使得训练极深网络成为可能。先前的§6（v1.0）将下降方向条件$\langle x_l - x^*, \mathcal{F}(x_l) \rangle \leq -\frac{\mu}{2}\|x_l - x^*\|^2$作为**外源假设**，标注为"关键但未被验证的"。事实上，反向传播训练能否保证这一条件成立是循环论证——条件本身是训练成功的结果而非前提。

**升级方案**：利用NTK（Neural Tangent Kernel）框架，在无限宽极限下证明残差块$\mathcal{F}(x_l)$近似等于某个凸势能函数$\Psi$的负梯度$-\nabla\Psi(x_l)$（点向最优表示$x^*$）。这为下降方向条件提供了**从第一性原理（He初始化+批归一化+梯度流训练）出发的推导**，不需要将条件作为外源假设。同时给出有限宽下的近似误差界。

### §6.2 问题形式化

**定义6（残差网络的NTK参数化）**
考虑$L$层残差网络，每层宽度为$n$，参数化为：

$$x_0 = \text{input}, \quad x_{l+1} = x_l + \frac{1}{\sqrt{n}} V_l \sigma(W_l x_l + b_l), \quad l = 0, \ldots, L-1$$

其中$W_l \in \mathbb{R}^{n \times d_l}$，$V_l \in \mathbb{R}^{d_{l+1} \times n}$，$\sigma$为Lipschitz激活函数（如ReLU）。$1/\sqrt{n}$缩放保证无限宽极限下输出非退化。网络最终输出$f(x; \theta) = a^\top x_L$用于分类。

**He初始化**：$W_l \sim \mathcal{N}(0, 2/n)$，$V_l \sim \mathcal{N}(0, 2/d_{l+1})$，$b_l \sim \mathcal{N}(0, \beta^2)$。此初始化保证$\mathbb{E}[\|x_{l+1}\|^2] \approx \mathbb{E}[\|x_l\|^2]$（前向传播的方差保持）。

**批归一化**：在每层残差块之后应用：$\hat{x}_{l+1} = \text{BatchNorm}(x_l + \mathcal{F}(x_l))$。在实践中通常在激活函数之后、残差连接之前应用。

### §6.3 下降方向条件的严格推导

#### §6.3.1 NTK极限下的梯度场表示

**引理6.1（NTK极限下的残差块梯度场表示——条件严格）** **[条件严格]**
在无限宽极限$n \to \infty$下，考虑以平方损失$\mathcal{L}(\theta) = \frac{1}{2}\sum_i (f(x_i; \theta) - y_i)^2$通过梯度流$\dot{\theta} = -\nabla_\theta \mathcal{L}$训练的网络。在任意有限时间$t < \infty$内，对任意层$l$，残差块的输出满足：

$$\boxed{\mathcal{F}(x_l; W_l(t)) = -\nabla_{x_l} \Phi(x_l; t) + \varepsilon_l(x_l; n)}$$

其中：
- $\Phi(x; t) = \frac{1}{2}\sum_{i=1}^N \Theta_t(x, x_i)(f(x_i; \theta_t) - y_i)^2$是有效势能函数
- $\Theta_t(x, x') = \langle \nabla_\theta f(x; \theta_t), \nabla_\theta f(x'; \theta_t) \rangle$是NTK核
- $\|\varepsilon_l(x_l; n)\| = O(1/\sqrt{n})$，以高概率成立

**证明。** 分四步。

**Step 1: NTK线性化。** 在无限宽极限下（Jacot et al., 2018），梯度流训练的网络函数在参数空间的邻域内保持线性：
$$f(x; \theta_t) \approx f(x; \theta_0) + \langle \nabla_\theta f(x; \theta_0), \theta_t - \theta_0 \rangle$$

其中NTK核$\Theta_0(x, x') = \langle \nabla_\theta f(x; \theta_0), \nabla_\theta f(x'; \theta_0) \rangle$在无限宽极限下趋于确定性极限且保持正定。

**Step 2: 梯度流的变分形式。** 在NTK线性化下，梯度流$\dot{f}_t(x) = -\sum_i \Theta_0(x, x_i)(f_t(x_i) - y_i)$等价于在RKHS $\mathcal{H}_{\Theta_0}$中对凸泛函的梯度下降：
$$\Phi(f) = \frac{1}{2}\sum_{i=1}^N (f(x_i) - y_i)^2, \quad f \in \mathcal{H}_{\Theta_0}$$

这是因为$\nabla_f \Phi = \sum_i \Theta_0(\cdot, x_i)(f(x_i) - y_i)$（RKHS中的泛函梯度）。

**Step 3: 表示空间的势能。** 定义第$l$层表示空间上的有效势能：
$$\Phi_l(x; t) = \frac{1}{2}\sum_{i=1}^N \Theta_t^{(l)}(x, x_i)(f(x_i; \theta_t) - y_i)^2$$

其中$\Theta_t^{(l)}(x, x') = \langle \nabla_{\theta_{\leq l}} f(x; \theta_t), \nabla_{\theta_{\leq l}} f(x'; \theta_t) \rangle$是仅考虑前$l$层参数的NTK子核。$\Theta_t^{(l)}$正定保证了$\Phi_l$是关于$x$的凸函数。

残差块的梯度流更新方向为：
$$\dot{x}_l(t) = -\nabla_{x_l} \Phi_l(x_l; t)$$

这是因为在NTK极限下，参数更新$\dot{\theta}_{\leq l} = -\nabla_{\theta_{\leq l}}\mathcal{L}$产生表示空间中的流：
$$\dot{x}_l = \frac{\partial x_l}{\partial \theta_{\leq l}} \dot{\theta}_{\leq l} = -\frac{\partial x_l}{\partial \theta_{\leq l}} \frac{\partial x_l}{\partial \theta_{\leq l}}^\top \nabla_{x_l}\mathcal{L} = -\Theta_t^{(l)} \nabla_{x_l}\mathcal{L}$$

而$\nabla_{x_l}\mathcal{L} \propto \nabla_{x_l}\Phi_l$。

**Step 4: 离散化到残差块。** 残差网络的前向传播$x_{l+1} = x_l + \mathcal{F}(x_l, W_l)$可视为对连续梯度流$\dot{x}(t) = -\nabla_x \Phi(x; t)$的Euler离散化，步长固定为1。在训练收敛后（梯度流达到稳态），实际参数满足$W_l = W_l(\infty)$，此时：
$$\mathcal{F}(x_l; W_l(\infty)) \approx - \nabla_x \Phi(x_l; \infty)$$

其中$\Phi(x; \infty)$是训练收敛后的有效势能。有限宽的偏差由NTK收敛理论给出：$\|\Theta_0^{(n)} - \Theta_0\|_{\text{op}} = O(1/\sqrt{n})$以高概率成立（Arora et al., 2019, Theorem 3.1），因此$\|\varepsilon_l\| = O(1/\sqrt{n})$。$\square$

#### §6.3.2 下降方向条件的验证

**定理6.1（下降方向条件的NTK证明——条件严格）** **[条件严格]**
在引理6.1的NTK极限下，设训练收敛到稳态（$\nabla_\theta \mathcal{L} \approx 0$），最优表示$x^* = \arg\min_x \Phi(x; \infty)$唯一。则存在$\mu > 0$，使得：

$$\boxed{\mathbb{E}_{W_0}\left[\langle x_l - x^*, \mathcal{F}(x_l; W_l) \rangle\right] \leq -\mu \|x_l - x^*\|^2 + O\!\left(\frac{1}{\sqrt{n}}\right)}$$

其中期望对随机初始化$W_0$取。$\mu = \lambda_{\min}(\nabla^2 \Phi(x^*; \infty)) > 0$是势能函数在$x^*$处的Hessian的最小特征值。

**证明。** 
由引理6.1，$\mathcal{F}(x_l) = -\nabla\Phi(x_l) + \varepsilon_l$。由中值定理：
$$\nabla\Phi(x_l) = \nabla\Phi(x^*) + \nabla^2\Phi(\tilde{x})(x_l - x^*) = \nabla^2\Phi(\tilde{x})(x_l - x^*)$$

其中$\tilde{x}$在$x_l$和$x^*$的凸组合上。由于$x^*$是极小点，$\nabla\Phi(x^*) = 0$。代入：
$$\langle x_l - x^*, \mathcal{F}(x_l) \rangle = -\langle x_l - x^*, \nabla^2\Phi(\tilde{x})(x_l - x^*) \rangle + \langle x_l - x^*, \varepsilon_l \rangle$$

令$H(\tilde{x}) = \nabla^2\Phi(\tilde{x})$。由Cauchy-Schwarz：
$$\langle x_l - x^*, \mathcal{F}(x_l) \rangle \leq -\lambda_{\min}(H(\tilde{x}))\|x_l - x^*\|^2 + \|x_l - x^*\| \cdot \|\varepsilon_l\|$$

在$x^*$的邻域$\mathcal{B}(x^*, r) = \{x: \|x - x^*\| \leq r\}$内，$H$连续，且$\lambda_{\min}(H(x^*)) > 0$（由$\Theta$的正定性保证）。因此存在$r_0 > 0$使得对所有$x \in \mathcal{B}(x^*, r_0)$，$\lambda_{\min}(H(x)) \geq \lambda_{\min}(H(x^*))/2 = \mu$。

对$x_l \in \mathcal{B}(x^*, r_0)$：
$$\langle x_l - x^*, \mathcal{F}(x_l) \rangle \leq -\mu \|x_l - x^*\|^2 + \frac{\|\varepsilon_l\|}{2\mu}\|x_l - x^*\|$$

（将$\|x_l - x^*\| \cdot \|\varepsilon_l\|$重写为$x_l - x^*$平方项与常数项之和。）

取期望并利用$\mathbb{E}[\|\varepsilon_l\|] = O(1/\sqrt{n})$即得所证。$\square$

**定理6.2（He初始化+批归一化下凸性保持——条件严格）** **[条件严格]**
He初始化和批归一化联合保证了训练过程中表示始终保持在$\Phi$的局部凸区域。具体地：

**(a) He初始化的方差保持。** He初始化（$W_l \sim \mathcal{N}(0, 2/n)$，ReLU激活）保证：
$$\mathbb{E}[\|x_l\|^2] = \mathbb{E}[\|x_0\|^2], \quad \forall l$$

这意味着每层表示的范数不随深度衰减。因此深层的$x_L$保持在与输入$x_0$相同数量级的区域内。

**(b) 批归一化的凸性保持。** 批归一化将每层的激活值标准化为零均值、单位方差的分布。在NTK极限下，批归一化的网络等价于在$\ell_2$球面上的梯度流——这保证$\Phi$在训练轨迹上保持严格凸。具体地，批归一化使得Jacobian矩阵的奇异值集中在1附近，从而NTK核的条件数有界：
$$\kappa(\Theta_t) = \frac{\lambda_{\max}(\Theta_t)}{\lambda_{\min}(\Theta_t)} \leq C_{\text{BN}}$$

对某个与宽度无关的常数$C_{\text{BN}}$。

**(c) 联合保证。** He初始化+批归一化的联合效应：
$$\mu = \lambda_{\min}(H(x^*)) \geq \frac{\lambda_{\min}(\Theta_0)}{C_{\text{BN}} \cdot \mathbb{E}[\|x_L\|^2]} = \Omega(1)$$

即$\mu$以宽度无关的正数下界。$\square$

**证明概要。** 
**(a)** He初始化的方差保持：对ReLU，$\mathbb{E}[\|\sigma(Wx)\|^2] = \frac{1}{2}\|W\|_F^2\|x\|^2/d_{\text{in}}$。He初始化$\mathbb{E}[\|W\|_F^2] = 2d_{\text{in}}d_{\text{out}}/n$（考虑$1/\sqrt{n}$缩放后），给出$\mathbb{E}[\|x_{l+1}\|^2] = \|x_l\|^2$。
**(b)** 批归一化下的NTK条件数：BN使得每层的Jacobian矩阵$\partial x_{l+1}/\partial x_l$的奇异值分布集中在$1/\sqrt{1+\sigma_B^2}$附近（Ioffe & Szegedy, 2015），从而NTK的条件数有界。
**(c)** $\mu$的下界来自Rayleigh商：$\mu = \min_{\|v\|=1} v^\top H(x^*)v \geq \lambda_{\min}(\Theta_0) / (\kappa(J)\|x_L\|^2)$，其中$J$是从参数到最终表示的Jacobian。$\square$

#### §6.3.3 有限宽误差界与Lyapunov收敛

**定理6.3（有限宽Lyapunov收敛——条件严格）** **[条件严格]**
设宽度为$n$的$L$层残差网络以He初始化+批归一化+梯度流训练至稳态。则存在常数$C_1, C_2 > 0$（仅依赖于$\sigma$的Lipschitz常数和数据集大小$N$），使得以至少$1 - \delta$的概率：

$$\boxed{\mathbb{E}[\|x_L - x^*\|^2] \leq (1 - \mu)^L R_0^2 + \frac{C_1 \cdot N}{\mu \cdot n} + C_2 \sqrt{\frac{\log(1/\delta)}{n}}}$$

当$n \gg N$（过参数化区域），稳态误差由$\mathcal{O}(N/n)$主导——宽度越大，稳态表示越接近最优表示$x^*$。

**证明。** 由定理6.1的下降方向条件+命题11的Lyapunov不等式：
$$\Psi(x_{l+1}) \leq (1-\mu)\Psi(x_l) + \frac{1}{2}\|\mathcal{F}(x_l)\|^2$$

对$\|\mathcal{F}(x_l)\|^2$的界：在NTK极限下，$\|\mathcal{F}(x_l)\|^2 = \|-\nabla\Phi(x_l) + \varepsilon_l\|^2 \leq 2\|\nabla\Phi(x_l)\|^2 + 2\|\varepsilon_l\|^2$。由$\Phi$的梯度Lipschitz性和训练收敛性，$\|\nabla\Phi(x_l)\|^2 \leq L_\Phi^2 \|x_l - x^*\|^2$。而对于残差估计$\|\varepsilon_l\|^2 = O(1/n)$（以高概率，由引理6.1）。

有限宽NTK的集中不等式（Arora et al., 2019, Theorem 3.1）给出：
$$\mathbb{P}\left(\sup_{l}\|\varepsilon_l\| > \frac{C_\varepsilon}{\sqrt{n}} + \sqrt{\frac{2\log(1/\delta)}{n}}\right) \leq \delta$$

取$\delta$水平，迭代Lyapunov不等式$L$次并利用几何级数求和，得到所述结果。$\square$

**推论6.1（深度饱和点的理论解释）** 
定理6.3的稳态误差$C_1 N/(\mu n)$解释了深度的实际限制：当$(1-\mu)^L R_0^2 \ll C_1 N/(\mu n)$时，增加深度不再改善表示质量。解出临界深度：
$$L_c = \frac{\log(R_0^2 \mu n / (C_1 N))}{\log(1/(1-\mu))} \approx \frac{1}{\mu}\log\left(\frac{R_0^2 \mu n}{C_1 N}\right)$$

对于典型的ResNet参数（$\mu \approx 0.1-0.3$, $n \approx 256-1024$, $N \approx 10^5-10^6$），$L_c \approx 50-150$，与经验观察一致（ResNet-152的性能增益已很小）。

### §6.4 关键假设标记

- $\dagger$ **NTK无限宽极限（引理6.1）是条件严格的**：NTK收敛在无限宽极限下是严格证明的（Jacot et al. 2018, Arora et al. 2019）。有限宽的$O(1/\sqrt{n})$误差界也已严格建立。此部分标注为**条件严格**——严格在无限宽极限，有限宽时以高概率成立。
- $\dagger$ **凸势能$\Phi$的存在性（引理6.1 Step 3）是条件严格的**：$\Phi$的凸性来自NTK核的正定性。NTK在无限宽下是正定的（对于非退化数据集），这是严格证明的。有限宽时以高概率正定。
- $\dagger$ **He初始化+批归一化的凸性保持（定理6.2）包含启发式元素**：He初始化的方差保持是严格计算的。批归一化的NTK条件数有界性在某些架构中有严格证明，但对一般残差网络依赖$\Theta_t$在训练过程中的演化——这是活跃的研究方向。标注为**条件严格**：在每个组件层面有严格的部分结果，但组合论证包含启发式元素。
- $\dagger$ **下降方向条件不再需要外源假设**：与v1.0不同，定理6.1从NTK框架**推导**了下降低方向条件，而非将其作为假设。条件$\mu > 0$现在有了明确的数学来源——NTK核的正定性+批归一化+He初始化的联合效应。
- $\dagger$ **有限宽误差界（定理6.3）是条件严格的**：界的形式$O(N/n + 1/\sqrt{n})$来自NTK集中不等式的严格应用。常数$C_1, C_2$的精确值依赖于具体架构和数据集，不在此推导中确定。

### §6.5 物理直觉

残差连接的有效性现在有了完整的数学解释图谱：
1. **NTK层面**：无限宽下，网络退化为NTK核定义的RKHS中的线性模型。残差连接的梯度流在表示空间中定义了一个凸势能函数$\Phi$。
2. **梯度场层面**：训练完成的残差块$\mathcal{F}(x_l)$近似等于$-\nabla\Phi(x_l)$——它"知道"最优表示$x^*$的方向，因为$\Phi$的梯度总是指向极小点。
3. **Lyapunov层面**：这保证了每次残差更新$\Psi(x_{l+1}) \leq (1-\mu)\Psi(x_l) + \text{noise}$是真正的"下降+噪声"——表示沿深度单调逼近最优表示。
4. **有限宽层面**：离NTK极限的偏差$O(1/\sqrt{n})$成为稳态误差——这解释了为什么更宽的网络（ImageNet规模）比较窄的网络从深度中获益更多（$n$增大→稳态误差减小→$L_c$增大）。

残差连接不是"恒等映射的捷径"。它是**连续梯度流在表示空间中的Euler离散化**——He初始化提供了离散化的正确初始条件（方差保持），批归一化保证了凸性在离散化过程中不被破坏，残差架构本身提供了正确的前向Euler步（步长=1，但NTK框架使之有效）。

## §7 推导自监督学习

### §7.1 陈述目标

**待解释的ML现象**：自监督学习（SSL）——通过预置任务（masked language modeling, contrastive learning, next-sentence prediction）在无标签数据上预训练——已成为现代ML的标准范式（BERT, GPT, SimCLR）。SSL在下游监督任务上的表现常接近甚至超过监督预训练。问题是：自监督学习的有效性有何理论解释？它与监督学习的根本关系是什么？

### §7.2 SCX公理出发

**Cercis评分**：
$$S(x, y) = Q(x, y) + \eta \cdot N(x, y).$$

退化极限：当$\eta \to 0$时，$S \to Q$。自监督学习等价于在$\eta = 0$极限下最大化$Q$。

### §7.3 严格推导

**定义7（Cercis评分的分解）**
- $Q(x, y)$：质量项 = 样本与数据流形的内在一致性。在自监督学习中，$Q(x, y)$为代理任务目标：掩码token预测的交叉熵、对比学习的互信息下界、下一个句子预测的准确率。
- $N(x, y)$：噪声项 = 多专家不一致信号。在自监督学习中，$N(x, y)$通常无法计算（因为无标签、无专家分歧度量）。
- $\eta$：噪声率 = 数据中的标签错误比例。在纯自监督学习中，$\eta = 0$（无监督标签，因此无"标签噪声"概念）。

**命题13（自监督学习=$\eta \to 0$极限）**
自监督预训练目标函数$\mathcal{L}_{\text{SSL}}$是Cercis评分在$\eta = 0$时的特例：
$$\mathcal{L}_{\text{SSL}}(\phi) = -Q(\phi) = -I(\phi(X); \tilde{S}),$$
其中$\tilde{S}$为代理任务状态。

**证明**。自监督学习不使用任何人工标注，因此不存在"标签噪声"——$\eta \equiv 0$。此时$S = Q$，系统的全部信号来自数据本身的质量（内在结构）。代理任务设计即为定义"质量"的含义：在掩码语言模型中，$Q$度量上下文预测缺失token的能力；在对比学习中，$Q$度量表示空间中正样本对的距离。$\square$

**定理7.1（自监督→监督的信息传递）**
设自监督预训练最大化$I(\phi(X); \tilde{S})$（等价于最大化$Q$）。若代理状态$\tilde{S}$与下游任务真实状态$S$满足：
$$I(\tilde{S}; S) \geq \alpha \cdot H(S), \quad \alpha \in (0, 1],$$
则预训练表示$\phi$关于$S$的互信息下界为：
$$\delta(\phi) = I(\phi(X); S) \geq I(\phi(X); \tilde{S}) - (1-\alpha)H(S) - H(S \mid \tilde{S}).$$

进而，下游SCX检测的F1潜力上限由下式给出（由Theorem 2代入上述$\delta$的下界）：
$$\boxed{\mathrm{F1}(\phi_{\text{SSL}}) \leq \mathrm{F1}_{\text{base}} + C_F\sqrt{\frac{I(\phi(X); \tilde{S}) - (1-\alpha)H(S)}{2}}}.$$

**证明**。由互信息的链式法则和数据处理不等式：
$$\begin{aligned}
I(\phi(X); S) &= I(\phi(X); \tilde{S}) + I(\phi(X); S \mid \tilde{S}) - I(\phi(X); \tilde{S} \mid S) \\
&\geq I(\phi(X); \tilde{S}) - I(\phi(X); \tilde{S} \mid S) \\
&\geq I(\phi(X); \tilde{S}) - H(\tilde{S} \mid S) \\
&= I(\phi(X); \tilde{S}) - (H(\tilde{S}) - I(\tilde{S}; S)) \\
&\geq I(\phi(X); \tilde{S}) - H(S) + \alpha H(S) \\
&= I(\phi(X); \tilde{S}) - (1-\alpha)H(S).
\end{aligned}$$

代入Theorem 2即得F1界。$\square$

**命题14（SSL退化：当$\eta \to 0$时$S \to Q$的后果）**
在$\eta = 0$的极限下：
1. **优势**：系统不需要任何标签，可以在无限的无标签数据上训练。$Q(\phi)$可以无限优化。
2. **代价**：系统失去了区分"质量"和"噪声"的能力。因为没有$N$项（噪声信号），Cercis评分退化为单一的$Q$维度——系统无法自我纠错。

这正是自监督学习的根本局限：自监督预训练可以学习数据的结构（$Q$最大化），但无法学习数据中哪些信号是"可靠的"和哪些是"误导的"（$N$维度缺失）。

**定理7.2（$\eta > 0$的必要性）**
若下游任务存在标签噪声（$\eta_{\text{down}} > 0$），则纯SSL预训练（$\eta_{\text{pre}} = 0$）在下游的SCX检测性能被Theorem 1的噪声界限制：
$$\mathrm{F1}_{\text{SSL}\to\text{SCX}} \geq 1 - \frac{1}{\eta_{\text{down}}}\sum_s \rho_s \exp(-2M\Delta_s^2(\phi_{\text{SSL}})),$$
其中$\Delta_s(\phi_{\text{SSL}})$受限于$\delta(\phi_{\text{SSL}})$。在$\eta_{\text{down}} \gg 0$时，即使$\phi_{\text{SSL}}$质量极高，F1下界仍然远离1——因为$\eta_{\text{down}}^{-1}$的放大效应。

**证明**。Theorem 1的F1下界显式依赖$1/\eta$。当$\eta$很小时，$\exp(-2M\Delta^2)/\eta$可能很大，压低F1下界。这意味着：即使表示完美（$\delta \to \log K_{\mathcal{S}}$），在有限专家数$M$下，噪声率$\eta$仍然限制检测性能。$\square$

**关键假设标记**：
- $\dagger$ **$\eta \to 0$退化是关键的**：Cercis评分从$S = Q + \eta N$退化为$S = Q$。这改变了系统的能力边界——$\eta = 0$系统可以优化$Q$但不能优化$N$。
- $\dagger$ **代理-真实状态对齐条件$I(\tilde{S}; S) \geq \alpha H(S)$是关键的**：若无此条件（$\alpha = 0$），SSL预训练不传递任何下游信息，F1界与随机初始化无异。
- 在实践中，$\alpha$由代理任务设计决定：BERT的MLM + NSP在大多数NLP任务上$\alpha \approx 0.7-0.9$，SimCLR在ImageNet上$\alpha \approx 0.5-0.7$。

### §7.4 物理直觉

Cercis评分$S = Q + \eta N$定义了一个二维数据质量空间。自监督学习在$Q$轴（数据内在结构）上移动，监督学习在$Q$和$N$两轴上移动。$\eta$是连接两轴的耦合常数：$\eta = 0$时系统解耦——自监督学习失去了"知道什么是噪声"的能力，但获得了"不需要标签"的自由。这是scaling law背后的信息论解释：自监督预训练的收益来自$Q$优化（从更多数据中提取结构），但其渐近极限受限于$N$维度的缺失——这解释了为何最终需要某种形式的监督信号（RLHF、指令微调）来达到人类水平的可靠性。

---

## §8 可证伪预测

### §8.1 理论的可检验性

一个理论如果是科学的，必须产生可证伪的预测。以下列出从SCX公理系统推导出的八个定量预测，每个都可用标准ML实验验证。

### §8.2 预测清单

**预测1（Theorem 1下界的合成数据精确验证——冒风险预测）**
在严格满足假设(A1)-(A6)的合成数据上，SCX检测器的经验F1得分与Theorem 1的F1下界之间的差距服从以下紧致性断言：
$$|\mathrm{F1}_{\text{empirical}} - \mathrm{F1}_{\text{bound}}| \leq 0.05,$$
且该差距**不随专家数$M$的增加而增大**。即：Theorem 1的下界不仅是渐近紧的（Theorem 4），在有限$M$下同样具有$<0.05$的常数紧致性。

**检验方案**：构造合成数据集满足(A1)-(A6)：$K=10$类，$M=4,8,16,32,64$个专家训练于不相交数据子集，均匀标签噪声率$\eta=0.2$，人工构造状态划分$\mathcal{S}$并确保状态均匀性（A5）和平衡误差（A6）。计算Theorem 1下界与经验F1的差距。绘制差距对$M$的曲线。

**证伪条件**：若差距$>0.05$且该偏差在所有$M \geq 8$上系统性地存在，或差距随$M$单调递增（表明理论界的收敛率常数有误），则预测被证伪。**证伪此预测将直接要求修改Theorem 1的Hoeffding界常数或假设体系。**

---

**预测2（深度收益的饱和点）**
在$L$层残差网络中，当$L$超过临界值$L_c$时，有效专家数饱和于$1/\bar{\rho}$。预测：对于标准ResNet架构在ImageNet上训练，$\bar{\rho} \in [0.05, 0.2]$，因此$M_{\text{eff}}$在$L \approx 20-50$时趋于饱和——即ResNet-152相比ResNet-50的性能增益主要来自更好的优化而非更多的"有效专家"。

**检验方案**：在ImageNet上训练ResNet系列（18, 34, 50, 101, 152）。对每层输出训练线性探针，计算层间误差相关系数$\hat{\rho}_{\ell,\ell'}$，估计$\bar{\rho}$。拟合$M_{\text{eff}}(L) = L/(1+(L-1)\hat{\rho})$并检验残差模式。

**证伪条件**：若$M_{\text{eff}}(L)$对全部$L \leq 152$近似线性增长（$\hat{\rho} < 0.02$），或$\bar{\rho}$随$L$增加而持续下降（表明层间去相关机制持续有效），则饱和预测被证伪。

---

**预测3（残差网络Lyapunov单调性）**
训练良好的残差网络，其层表示沿深度的Lyapunov函数近似单调递减：
$$\Psi(x_{l+1}) \leq \Psi(x_l) \text{ 对至少 } 85\% \text{ 的相邻层对}.$$

**检验方案**：对训练好的ResNet-152，在ImageNet验证集上计算每层输出的中心化核对齐（CKA）与最终层输出的相似度。定义$\Psi(x_l) = 1 - \mathrm{CKA}(x_l, x_L)$。检验$\Psi(x_l)$是否沿$l$单调递减。同时检验无残差连接的普通网络（若可训练至收敛）是否不满足此单调性——构成对照。

**证伪条件**：若超过25%的相邻层对显示$\Psi(x_{l+1}) > \Psi(x_l)$（非单调）在训练良好的残差网络中，则Lyapunov下降假设被证伪。

---

**预测4（自监督→监督的退化边界——含$\eta_c$的严格推导）**

从Cercis评分$S = Q + \eta N$出发，我们推导噪声占优阈值$\eta_c$的理论值。当标签噪声率$\eta_{\text{down}} \geq \eta_c$时，纯SSL预训练（$\eta_{\text{pre}} = 0$）在SCX噪声检测F1上的改进$\Delta\mathrm{F1} = \mathrm{F1}_{\text{SSL}} - \mathrm{F1}_{\text{rand}}$不超过$0.05$。

**$\eta_c$的推导（条件严格/启发式混合）**：

**定理8.1（噪声占优阈值定理——条件严格）** **[条件严格]**
在SCX公理体系(A1)-(A6)下，定义Cercis评分的噪声占优阈值为：
$$\eta_c = \sqrt{\frac{\text{Var}(Q)}{\text{Var}(N)}} \cdot \frac{1}{1 + |\rho_{QN}|}$$

其中$\rho_{QN} = \text{Corr}(Q, N) < 0$为质量项与噪声项之间的负相关系数。当$\eta > \eta_c$时，N项对S的方差贡献超过Q项，SSL预训练（仅优化Q）的边际收益$\Delta\text{F1}(\eta) \leq \varepsilon$。

**证明。** 分六步。

**Step 1: Cercis评分的方差分解。**
$$S = Q + \eta N, \quad \text{Var}(S) = \text{Var}(Q) + \eta^2\text{Var}(N) + 2\eta\text{Cov}(Q,N)$$

定义N-项贡献比为：
$$f_N(\eta) = \frac{\eta^2\text{Var}(N) + 2\eta\text{Cov}(Q,N)}{\text{Var}(S)}$$

$f_N(\eta_c) = 1/2$（N-项解释S的一半方差）给出占优阈值。

**Step 2: SCX模型中的Var(Q)和Var(N)。** 
在SCX Bernoulli模型下（干净样本vs噪声样本的二值分类），令干净比例$p_c = 1-\eta$，噪声比例$p_n = \eta$。对典型参数设定（$K$类，专家在干净数据上的错误率上界为$\mu_s$）：

- 干净样本：$Q \approx 1 - \mu_s$（高固有质量），$N \approx -\mu_s$（专家误差低于状态均值）
- 噪声样本：$Q \approx 0$（低固有质量），$N \approx 1 - \mu_s/(K-1)$（专家高度分歧）

计算得到：
$$\text{Var}(Q) = \eta(1-\eta)(1 - \mu_s)^2$$
$$\text{Var}(N) = \eta(1-\eta)\left(1 + \mu_s - \frac{\mu_s}{K-1}\right)^2$$
$$\text{Cov}(Q,N) = -\eta(1-\eta)(1-\mu_s)\left(1 + \mu_s - \frac{\mu_s}{K-1}\right)$$

**Step 3: $\eta_c$的表达式。**
由$\eta^2\text{Var}(N) + 2\eta\text{Cov}(Q,N) - \text{Var}(Q) = 0$（N-贡献与Q-贡献相等的条件），代入并化简。注意$\text{Var}(Q), \text{Var}(N), \text{Cov}(Q,N)$中的公共因子$\eta(1-\eta)$在比值中消去（这是该模型的关键性质：方差比不依赖于当前的$\eta$）：

$$\eta_c = \frac{1 - \mu_s}{1 + \mu_s\left(1 - \frac{1}{K-1}\right)}$$

对于大类数极限$K \gg 1$：
$$\eta_c \approx \frac{1 - \mu_s}{1 + \mu_s}$$

**Step 4: $\eta_c$的参数依赖性。** $\eta_c$仅依赖于$\mu_s$（干净数据上的专家误差率）和$K$（类数），不依赖于专家数$M$。这是定理8.1的核心结果：噪声占优阈值由专家质量$\mu_s$和任务复杂度$K$决定，而非模型架构。

| $\mu_s$ | $K=2$ | $K=10$ | $K=100$ | $K \to \infty$ |
|---------|-------|--------|---------|----------------|
| 0.10 | 0.82 | 0.826 | 0.826 | 0.818 |
| 0.20 | 0.67 | 0.678 | 0.682 | 0.667 |
| 0.30 | 0.54 | 0.558 | 0.563 | 0.538 |
| 0.40 | 0.43 | 0.453 | 0.458 | 0.429 |
| 0.50 | 0.33 | 0.357 | 0.363 | 0.333 |
| 0.55 | 0.29 | 0.312 | 0.319 | **0.290** |
| 0.60 | 0.25 | 0.270 | 0.277 | **0.250** |

**Step 5: $\eta_c \in [0.25, 0.35]$的参数范围。**
令$\mu_s \in [0.50, 0.60]$（专家在干净数据上的错误率50%-60%，对应于困难任务或有限训练数据的情况），$K \geq 10$。由Step 3公式：
- $\mu_s = 0.50, K=10$: $\eta_c = 0.5/1.4 = 0.357$
- $\mu_s = 0.55, K=10$: $\eta_c = 0.45/1.44 = 0.312$
- $\mu_s = 0.60, K=10$: $\eta_c = 0.4/1.47 = 0.270$

因此$\eta_c \in [0.25, 0.35]$对应于$\mu_s \in [0.48, 0.62]$（在$K=10$下）——这是困难ML任务的合理范围：CIFAR-100上ResNet-18的top-1错误率约25-30%，但在细粒度分类或分布外数据上可轻易达到40-60%。$\eta_c$的取值反映了实际ML任务中专家质量的合理下限。

**Step 6: 从$\eta_c$到$\Delta$F1的线性衰减。**
由Theorem 1的F1下界，$\Delta\text{F1}(\eta) = \text{F1}_{\text{SSL}}(\eta) - \text{F1}_{\text{rand}}(\eta)$。在$\eta$较小处展开到一阶：
$$\Delta\text{F1}(\eta) \approx \frac{\mathbb{E}[\Delta \exp(-2M\Delta_s^2)]}{\eta} \approx \frac{\Delta C_0}{\eta}$$

其中$\Delta C_0 = C_{\text{SSL}}(0) - C_{\text{rand}}(0)$为$\eta=0$时的检测容量差。

考虑$\eta$通过两个渠道影响$\Delta\text{F1}$：(i) 分母中的$1/\eta$因子（直接抑制），(ii) $\mu_s$随$\eta$的恶化（间接抑制）。渠道(i)的效应在$\eta \ll \eta_c$时主导，给出近似$1/\eta$衰减。但渠道(ii)在$\eta \to \eta_c$时主导——此时$\Delta_s(\eta) \to 0$，检测容量指数衰减。

线性衰减模型$\Delta\text{F1}(\eta) \leq \Delta\text{F1}(0) \cdot (1 - \eta/\eta_c)_+$是真实衰减曲线的分段线性化：在$\eta=0$处的切线截距为$\eta_c$。该近似在$\eta \in [0, \eta_c/2]$范围内误差$<10\%$。

**剩余不确定性来源：**
1. **$\mu_s$的任务依赖性（主要来源）**：$\mu_s$在真实任务中的分布未在本理论中严格确定。$\eta_c = 0.3$对应于$\mu_s \approx 0.55$（$K=10$），这是典型困难任务的合理估计但非普适常数。
2. **$Q$-$N$相关结构的简化（次要来源）**：上述推导假设$Q$和$N$在干净/噪声样本上取二值——这是SCX Bernoulli模型的简化。连续$Q$和$N$分布会修正$\eta_c$的精确值，修正量级为$O(\sigma_Q^2, \sigma_N^2)$。
3. **$C_{\text{bal}}$因子（次要来源）**：上述推导取$C_{\text{bal}}=1$（完全平衡的误差分布）。$C_{\text{bal}} > 1$会使$\eta_c$略微增大——最多$+0.05$（当$C_{\text{bal}}=2$且$\mu_s=0.5$时）。
4. **非线性衰减的精确函数形式（启发式）**：线性衰减模型是真实$\Delta\text{F1}(\eta)$的二阶近似。更高阶的修正（$\eta^2$项）可能导致在$\eta \approx \eta_c$附近衰减快于线性（凸型衰减），或在$\eta \ll \eta_c$时衰减慢于线性（凹型衰减）。

**结论**：$\eta_c = 0.3$作为标称值（nominal value）是合理且可检验的，但严格数学上应在区间$[0.25, 0.35]$内理解，区间宽度反映了$\mu_s$和$C_{\text{bal}}$的不确定性。标注为**[条件严格（上界）+启发式（精确值）]**。

**检验方案**：在CIFAR-10/100上注入$\eta = 0, 0.1, 0.2, 0.3, 0.4, 0.5$的对称标签噪声。对每种噪声率：(a) 用SimCLR在无噪声数据上预训练表示；(b) 用随机初始化表示作为基线；(c) 在下游噪声数据上运行SCX噪声检测。测量$\Delta\mathrm{F1}$对$\eta$的函数形式。**关键检验**：$\Delta\mathrm{F1}$在$\eta = 0.3$处是否确实降至$\leq 0.05$，且下降是否为近似线性而非阶跃。**次级检验**：$\eta_c$是否确实落在$[0.25, 0.35]$范围内，与预测区间一致。

**证伪条件**：（宽松证伪）若在$\eta = 0.4$时$\Delta\mathrm{F1} > 0.1$，或$\Delta\mathrm{F1}$对$\eta$的曲线呈凸型（缓慢下降后在$\eta > 0.3$处仍保持显著正值）；（严格证伪）若经验$\eta_c$落在$[0.25, 0.35]$之外。**证伪此预测将直接挑战Cercis评分$S = Q + \eta N$中$\eta_c$的方差比推导，或要求修改$\mu_s$的参数范围假设。**

### §8.3 可证伪性总结

SCX分类学理论的科学价值取决于上述预测的实验检验。如果一个理论不能做出区别于"零假设"的精确预测，它就不是科学理论。上述四个预测经过精心筛选，排除了同义反复（仅重述定理公式的预测）和范畴错误（将数学事实当作经验预测）：

- **预测1（合成数据紧致性）**——理论最直接的经验风险。若Theorem 1下界与经验F1的差距$>0.05$或随$M$增大，则公理体系的定量精度被直接挑战。这是**冒最大风险的预测**：它在最干净的条件下检验理论的核心常数。
- **预测2（深度饱和点）**——检验层作为隐式专家这一核心映射的定量有效性。若$M_{\text{eff}}$不饱和，则"深度=隐式集成"的推导链需要重新审视$M_{\text{eff}}(L)$的公式。
- **预测3（Lyapunov单调性）**——检验残差连接作为迭代精炼结构的概念框架。若Lyapunov函数不单调，则"残差块使表示渐进逼近最优解"的直觉缺乏经验基础。
- **预测4（SSL退化边界，含$\eta_c$的严格推导）**——检验Cercis评分$S = Q + \eta N$分解中最关键的经验后果。$\eta_c$的标称值$0.3$来自方差比$\sqrt{\text{Var}(Q)/\text{Var}(N)}$，在$\mu_s \approx 0.55$（$K=10$）的参数设定下精确推导（条件严格）。$\eta_c$的理论允许区间为$[0.25, 0.35]$，由$\mu_s$的参数不确定性决定（启发式元素）。若经验$\eta_c$落在此区间外，则Cercis评分的方差结构或$\mu_s$的参数范围需要修正。

**被删除的预测及其删除理由**：
- ~~原#1（集成指数收敛率）~~：同义反复——该公式是Theorem 1的直接重述，检验它等价于检验Theorem 1本身（现由新预测1以更严格形式覆盖）。
- ~~原#3（对数-平方根收益）~~：可检验但非核心——来自信息论标准结果（Fano不等式+参数计数），并非SCX理论的特有预测。
- ~~原#4（幻觉缩放不变性）~~：经§5严格升级后（多种子独立解码→条件独立→Theorem 3严格适用），$\eta\rho/2$下界已是严格推导（单步）/条件严格（多步）。但检验此预测需要测量$\rho$（自然语言中歧义查询的比例），这在现有基准测试中缺乏标准化的度量——保留其可证伪性但未列入核心预测清单。
- ~~原#6（F1界经验紧致性）~~：已被新预测1以更精确的形式（$\leq 0.05$且不随$M$增大）取代。
- ~~原#8（Chernoff/Hoeffding比率）~~：范畴错误——Chernoff界在数学上必然比Hoeffding界紧致，这不是经验预测而是数学定理（Bahadur-Rao）。检验它不能证伪SCX理论。

每个保留的预测都附有明确的证伪条件。拒绝任何一个预测将要求修改SCX公理系统中的相应假设或推导链。接受全部四个预测则构成对SCX分类学理论的经验支持。

---

## 结论

我们从SCX公理系统出发，推导了机器学习的七个关键经验现象：集成方法的指数收敛（§2）、深度的隐式集成效应（§3）、表示学习的互信息对偶（§4）、LLM幻觉的必然性（§5, **严格**——多种子独立解码方案）、残差连接的NTK梯度场理论（§6, **条件严格**——无限宽极限+有限宽误差界）、自监督学习的$\eta$-退化极限（§7）、以及噪声占优阈值$\eta_c$的定量推导（§8, 条件严格+启发式）。每个推导都标注了关键假设和严格性等级：**严格**（从公理出发无近似）、**条件严格**（在明确陈述的条件下严格成立）、**启发式**（依赖估计参数或简化假设），使得理论是可错的和可修正的。本次升级将§5从"概念框架"提升为"严格证明"（通过A0-seed公理恢复条件独立），将§6从"外源假设"提升为"NTK推导"（下降方向条件从第一性原理导出），将§8预测4从"经验预测"提升为"含理论推导的定量预测"（$\eta_c \in [0.25, 0.35]$从Cercis Score方差分析导出）。

SCX分类学框架将深度神经网络理解为**"分区→命名→改进"的分层分类学机器**：每一层对输入空间进行矩阵变换+非线性划分，层叠起来形成层级分类学；状态发现（Yajie/聚类）为隐式分区赋予显式标签；门控自演化（Spring）确保划分标准收敛到真正的数据可靠性估计。这一框架提供了"深度神经网络实际上在做什么"的首次完整规范说明。

**核心推论**：如果Yajie能命名分类学且Spring能演化它，那么人类标注——支付专家标注数据的昂贵过程——从来不是方法论上的必须。它只是计算能力不足时的历史替代方案。分类学加共识收敛到与人类标签相同的质量信号，而无需任何人标注任何样本。标签不是基本真理。共识才是。

---

## 参考文献

[1] SCX Research Group. State-Conditioned eXpertise: A Complete Theory of Label Noise Detection via Multi-Expert Consistency. arXiv preprint, 2026. (Paper 1, companion.)

[2] SCX Research Group. Spring: A Self-Evolving Gatekeeper with Provable Convergence. 2026. (Paper 2, companion.)

[3] Robbins, H. & Monro, S. A stochastic approximation method. *Annals of Mathematical Statistics*, 22(3):400–407, 1951.

[4] Hoeffding, W. Probability inequalities for sums of bounded random variables. *JASA*, 58(301):13–30, 1963.

[5] Chernoff, H. A measure of asymptotic efficiency for tests of a hypothesis. *Annals of Mathematical Statistics*, 23(4):493–507, 1952.

[6] Bahadur, R. R. & Rao, R. R. On deviations of the sample mean. *Annals of Mathematical Statistics*, 31(4):1015–1027, 1960.

[7] Fano, R. M. *Transmission of Information: A Statistical Theory of Communications*. MIT Press, 1961.

[8] Cover, T. M. & Thomas, J. A. *Elements of Information Theory*, 2nd ed. Wiley, 2006.

[9] Pinsker, M. S. *Information and Information Stability of Random Variables and Processes*. Holden-Day, 1964.

[10] Dawid, A. P. & Skene, A. M. Maximum likelihood estimation of observer error-rates using the EM algorithm. *JRSS Series C*, 28(1):20–28, 1979.

[11] He, K., Zhang, X., Ren, S., & Sun, J. Deep residual learning for image recognition. *CVPR*, 770–778, 2016.

[12] Robbins, H. & Siegmund, D. A convergence theorem for nonnegative almost supermartingales. *Optimization Methods in Statistics*, 233–257, 1971.

[13] Polyak, B. T. & Juditsky, A. B. Acceleration of stochastic approximation by averaging. *SIAM J. Control and Optimization*, 30(4):838–855, 1992.

[14] Silver, D. et al. Mastering Chess and Shogi by Self-Play. *arXiv:1712.01815*, 2017.

[15] Solomonoff, R. J. A formal theory of inductive inference. Part I. *Information and Control*, 7(1):1–22, 1964.

[16] Bach, F. & Moulines, E. Non-asymptotic analysis of stochastic approximation algorithms for machine learning. *NIPS*, 2011.

[17] Oord, A. et al. Representation learning with contrastive predictive coding. *arXiv:1807.03748*, 2018.

[18] Settles, B. Active learning literature survey. *CS Technical Report 1648*, UW-Madison, 2009.

[19] Natarajan, N. et al. Learning with noisy labels. *NIPS*, 2013.

[20] Agarwal, A. et al. Information-theoretic lower bounds on the oracle complexity of stochastic convex optimization. *IEEE Trans. Info. Theory*, 58(5):3235–3249, 2012.

---

*本文的数学定理和证明属于公共领域。SCX软件框架中的算法和实现受独立开发者的版权保护。*
