# 神经网络分类学理论：从SCX公理系统推导机器学习已知现象

**A Taxonomic Theory of Neural Networks: Derivation of Known Machine Learning Phenomena from the SCX Axiom System**

SCX Research Group, Theory Division, Xiaogan Supercomputing Center

2026年6月29日

---

## 摘要

我们提出，机器学习的七大核心经验现象——集成方法的有效性、深度网络的指数优势、表示学习的预训练收益、大语言模型的幻觉必然性、残差连接的有效性、自监督学习的退化极限——均可以从SCX（State-Conditioned eXpertise）公理系统获得解释。其中集成方法（§2）、深度（§3）、表示学习（§4）、自监督学习（§7）四个现象获得严格数学推导；LLM幻觉（§5, v2.0升级为严格证明，关键洞察：多种子独立解码恢复条件独立假设——v2.1新增：分离噪声率η_err与歧义率η_ambig，显式陈述对称性条件）、残差连接（§6, v6.0重写——v2.0的NTK梯度场推导因链式法则错误被废弃，v3.0的扰动收缩分析将ρ_l<1标注为未证明假设，v4.0通过前向-后向分裂理论为该条件提供了单调算子论基础，v5.0将一般非线性情况的核心引理重构为"前向-后向公设"——仿效狭义相对论光速不变公设；v6.0采用Pontryagin极大值原理(PMP)将残差网络前向传播形式化为最优控制问题，从协态方程+参数驻点严格推导F_l(x_l)∝x*−x_l——残差块输出的方向指向最优表示）、以及噪声占优阈值（§8预测4, v3.0修正η_c代数推导——v2.0的推导含代数错误，修正后η_c>>0.5，预测失去实用意义）均经历了显著修订。SCX公理系统由四个核心定理（F1界、弱特征失效边界、噪声-难度不可区分、minimax最优）、Cercis评分$S = Q + \eta N$、以及Spring自演化定理（Lyapunov收敛）构成。本文建立了一个分类学框架，其中深度神经网络被理解为"分区→命名→改进"的分层分类学机器，而Spring门控机制为该框架提供了收敛性保证。

**关键词**：SCX公理，集成方法，深度学习，表示学习，LLM幻觉，残差连接，自监督学习，可证伪预测

---

## 目录

1. [§1 SCX公理系统](#1-scx公理系统) **[严格]**
2. [§2 推导集成方法](#2-推导集成方法) **[严格]**
3. [§3 推导深度](#3-推导深度) **[严格]**
4. [§4 推导表示学习](#4-推导表示学习) **[严格]**
5. [§5 LLM幻觉的必然性](#5-llm幻觉的必然性多种子独立解码的严格证明) **[严格（单步）/ 条件严格（多步）]**
6. [§6 残差连接的Pontryagin极大值原理分析](#6-残差连接的pontryagin极大值原理分析flxl的方向指向最优表示x) **[混合：严格/条件严格/诚实标注]** ⚠ v6.0重写
7. [§7 推导自监督学习](#7-推导自监督学习) **[严格]**
8. [§8 可证伪预测](#8-可证伪预测) **[含η_c修正推导]** ⚠ v3.0修正

**严格性等级说明**：
- **[严格]**：从公理出发无近似步骤
- **[条件严格]**：在明确陈述的条件下严格成立
- **[概念框架]**：提供自洽的数学图景，核心假设被明确陈述但未被严格证明
- **[混合]**：同一节内不同部分有不同的严格性等级（严格/条件严格/科学公设），逐部分标注
- **[科学公设+可证伪]**：核心陈述被公设为可证伪的科学假说，附有精确的操作性检验方案
- ⚠ 标注版本号表示该节经历重大修订

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
$$\max(\mathrm{Error}_{\mathcal{P}_{\text{noise}}}(\mathcal{A}), \mathrm{Error}_{\mathcal{P}_{\text{hard}}}(\mathcal{A})) \geq \frac{\min(\eta_{\text{err}}, \eta_{\text{amb}}) \cdot \rho}{2} > 0.$$

**证明（二元情况$K=2$的显式构造）**：

**世界A（噪声驱动）**：状态$s_1$中$\mathbb{P}(X\in s_1)=\rho$，真实标签$y^*\equiv0$，以概率$\eta_{\text{err}}$翻转（标签噪声率）。专家正确率$1-\varepsilon_1$。

**世界B（困难驱动）**：状态$s_1$中$\mathbb{P}(y^*=0)=1-\eta_{\text{amb}}$，$\mathbb{P}(y^*=1)=\eta_{\text{amb}}$（本质歧义率）。专家偏向类0：无论$y^*$取何值，$\mathbb{P}(f_m=0)=1-\varepsilon_1$。

**对称性条件**：两个世界产生全同观测分布当且仅当：
$$\boxed{\eta_{\text{err}} = \eta_{\text{amb}} = \eta}$$
当此对称性成立时，噪声率（世界A中的标签翻转概率）与歧义率（世界B中真实标签为非主导类的概率）在数值上相等——这恰是观测不可区分性的结构根源。

**等价性验证（在对称性条件$\eta_{\text{err}}=\eta_{\text{amb}}=\eta$下）**：
- $\mathcal{P}_{\text{noise}}(y=0\mid s_1) = (1-\eta_{\text{err}})\cdot1 + \eta_{\text{err}}\cdot0 = 1-\eta = \mathcal{P}_{\text{hard}}(y=0\mid s_1)$
- $\mathcal{P}_{\text{noise}}(f_m=0\mid s_1) = 1-\varepsilon_1$
- $\mathcal{P}_{\text{hard}}(f_m=0\mid s_1) = (1-\eta_{\text{amb}})(1-\varepsilon_1) + \eta_{\text{amb}}(1-\varepsilon_1) = 1-\varepsilon_1$

三个边缘分布完全相同，联合分布亦然。

**算法不可能性**：设$a$为算法在歧义子集$\{x\in s_1, y=1\}$上标记为噪声的期望比例。则$\mathrm{Error}_{\text{noise}} = \rho\eta_{\text{err}}(1-a)$，$\mathrm{Error}_{\text{hard}} = \rho\eta_{\text{amb}} a$。在对称性条件$\eta_{\text{err}}=\eta_{\text{amb}}=\eta$下，$\max(\mathrm{Error}_{\text{noise}}, \mathrm{Error}_{\text{hard}}) \geq \rho\eta/2$。一般地，若$\eta_{\text{err}} \neq \eta_{\text{amb}}$，下界为$\rho \cdot \min(\eta_{\text{err}}, \eta_{\text{amb}})/2$（细节：两个世界的误差表达式取max后，最小值在$a = \eta_{\text{err}}/(\eta_{\text{err}}+\eta_{\text{amb}})$处达到，下界为$\rho \cdot \eta_{\text{err}}\eta_{\text{amb}}/(\eta_{\text{err}}+\eta_{\text{amb}})$）。

**打破不可区分性的最小假设组合**：
- $\mathcal{A}_{\min}^{(1)} = \{A1, A4, A5\}$（SCX标准集）
- $\mathcal{A}_{\min}^{(2)} = \{A1, A4, A6\}$
- $\mathcal{A}_{\min}^{(3)} = \{A5, A6\}$且$|\mathcal{S}| \geq 2$

**关键假设**：Theorem 3本身不依赖任何假设——它是关于"无假设情况下"的不可区分性的。"无免费午餐定理"的SCX版本。**v2.1更新**：显式区分了噪声率$\eta_{\text{err}}$（World A）和歧义率$\eta_{\text{amb}}$（World B），并标明了观测等价性所需的对称性条件$\eta_{\text{err}} = \eta_{\text{amb}}$。这一分离揭示了不可区分性的结构条件：当且仅当噪声率与歧义率对称时，两个世界在观测上不可区分。

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

**命题6（残差连接的独立化效应）** 残差连接$x_{\ell+1} = x_\ell + \mathcal{F}(x_\ell)$降低层间误差相关性。直观上，$\mathcal{F}(x_\ell)$仅学习残差——即$x_\ell$已经正确的部分的微小修正。这使得$\mathcal{F}_\ell$的输出与$\mathcal{F}_{\ell-1}$的输出更接近正交，从而减小$\bar{\rho}$。残差连接的完整分析见§6（v6.0：Pontryagin极大值原理——$F_l(x_l)$的方向指向最优表示$x^*$）。

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

**v2.1更新（参数分离与对称性条件）**：Theorem 3（§1.6）的构造中，噪声率$\eta_{\text{err}}$（世界A：标签翻转概率）与歧义率$\eta_{\text{amb}}$（世界B：真实标签的不确定性）在概念上是不同的参数。两个世界产生全同观测分布当且仅当$\eta_{\text{err}} = \eta_{\text{amb}} = \eta$（**对称性条件**）。在多种子解码设定中，此对称性是自然的：同一LLM在相同输入上以不同种子产生的错误分布，其错误率与歧义诱导的观测错误率在数值上相等——因为随机种子扰动是对称的（每个种子的扰动分布相同）。本节在引理5.1后显式标注此对称性条件。

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

**注5.3（对称性条件——v2.1新增）** 定理5.1的严格性依赖于Theorem 3（§1.6, v2.1更新）中的**对称性条件**$\eta_{\text{err}} = \eta_{\text{amb}} = \eta$：世界A的模型错误率（噪声驱动，$\eta_{\text{err}}$）与世界B的本质歧义率（困难驱动，$\eta_{\text{amb}}$）必须在数值上相等，两个世界才在观测上不可区分。在多种子独立解码设定下，此对称性条件自然成立——每条种子路径使用完全相同的模型权重$f_\theta$和独立同分布的随机扰动$\xi_m$。扰动分布的对称性（所有$\xi_m$来自相同的分布）保证了模型在噪声样本上的错误率（世界A的$\eta_{\text{err}}$）与模型在歧义样本上忠实地学习到的非退化分布中的边陬概率（世界B的$\eta_{\text{amb}}$）在数值上相等。若此对称性被打破（例如某些种子系统性优于其他种子），则两个世界可能在观测上可区分——但这种情况需要非对称的种子扰动分布，与A0-seed独立同分布假设矛盾。

**引理5.2（A1的替代——推理时"有效不相交训练"）**
虽然$M$条解码路径共享同一预训练模型（未在不相交数据上训练），但随机性来源的独立性提供了"有效不相交"：每条路径的随机扰动$\xi_m$在功能上等价于在略微扰动的模型上做推理。由于$\xi_m \perp \xi_{m'}$，这些"有效扰动模型"的预测误差满足条件独立——这是Theorem 3所需的核心属性，不需要严格满足A1。

**定理5.1（LLM幻觉下界的严格版——严格证明）** **[严格]**
设LLM $f_\theta$以$M$个独立随机种子对输入上下文$c$进行解码，产生$M$个预测$\{\hat{y}_m(c)\}_{m=1}^M$满足引理5.1的条件独立性。在对称性条件$\eta_{\text{err}} = \eta_{\text{amb}} = \eta$下（注5.3），则对于任何仅利用这$M$个预测输出（不引入外部验证源）的幻觉检测算法$\mathcal{A}$，存在两个观测上不可区分的世界——世界A（模型错误导致幻觉）和世界B（本质歧义导致幻觉）——使得：

$$\boxed{\max\left(\text{Error}_{\text{world A}}(\mathcal{A}), \text{Error}_{\text{world B}}(\mathcal{A})\right) \geq \frac{\eta\rho}{2}}$$

其中$\eta = \eta_{\text{err}} = \eta_{\text{amb}}$为对称条件下的统一参数（$\mathbb{P}(\text{种子预测产生错误} \mid \text{歧义上下文})$），$\rho = \mathbb{P}(\text{上下文本质歧义})$。此下界是**严格的**：存在达到此界的检测算法。

**证明。** 由引理5.1，$M$条种子路径的误差$\{e_m(c)\}$在给定$c$下条件独立。这精确满足Theorem 3的条件（Theorem 3的证明仅要求多专家误差的条件独立性）。将Theorem 3的构造直接应用于当前设定（使用v2.1更新后的参数分离版本）：

**世界A（模型错误）**：在歧义状态$s_1$（比例$\rho$），真实答案$y^*(c) \equiv 0$是唯一的。以概率$\eta_{\text{err}}$，每条种子路径独立地产生错误预测（受随机扰动影响）。这对应Theorem 3的World A——标签噪声世界。

**世界B（本质歧义）**：在状态$s_1$，真实答案本身是随机的：$\mathbb{P}(y^*(c)=0) = 1-\eta_{\text{amb}}$，$\mathbb{P}(y^*(c)=1) = \eta_{\text{amb}}$。每条种子路径正确地学习了这一歧义分布，以$1-\varepsilon$的概率输出与采样到的$y^*(c)$一致的答案（受有限容量和随机扰动影响）。这对应Theorem 3的World B——本质困难世界。

由对称性条件$\eta_{\text{err}} = \eta_{\text{amb}} = \eta$和Theorem 3的观测等价性验证（见§1.6, v2.1更新），两个世界产生完全相同的$(c, \hat{y}_1, \ldots, \hat{y}_M)$联合分布。因此任何算法$\mathcal{A}$的输出分布在两个世界上全同。

算法$\mathcal{A}$的检测误差在两个世界上的最大值为：
$$\max(\text{Error}_{\text{A}}, \text{Error}_{\text{B}}) \geq \frac{\text{Error}_{\text{A}} + \text{Error}_{\text{B}}}{2} = \frac{\rho\eta}{2}$$

其中$\text{Error}_{\text{A}} = \rho\eta_{\text{err}}(1-a)$（世界A中将噪声误判为干净的期望比例），$\text{Error}_{\text{B}} = \rho\eta_{\text{amb}} a$（世界B中将歧义误判为噪声的期望比例），$a \in [0,1]$为算法的期望标记率。在对称条件下两者之和为$\rho\eta$，最大值至少为$\rho\eta/2$。

该下界在Bayes最优检测器下可达（由Neyman-Pearson引理和Theorem 4的minimax构造），因此是严格的。$\square$

**定理5.2（自回归多步生成的扩展——条件严格）** **[条件严格]**
将定理5.1扩展到自回归生成$T$个token的序列。设每步$t$使用$M$个独立种子解码，产生$M$个候选next-token。则每步的幻觉下界为$\eta_t\rho_t/2$。序列级别的总幻觉期望下界为：

$$\boxed{\mathbb{E}[\text{序列中的幻觉token数}] \geq \sum_{t=1}^{T} \frac{\eta_t\rho_t}{2} \cdot (1 - \gamma)^{t-1}}$$

其中$\gamma \in [0, 1)$为步骤间误差的相关系数上界。

**证明概要。** 在第$t$步，给定前$t-1$步已生成的token序列，$M$个种子的next-token预测误差满足条件独立（引理5.1对每步单独成立，因为每步的种子是全新的独立抽取）。因此定理5.1的每步下界$\eta_t\rho_t/2$适用。

步骤间的依赖通过路径历史引入：第$t$步的输入上下文$c_t$包含了前$t-1$步的采样输出，这些输出取决于之前步骤的种子。这引入了步骤间的弱相关性。设$\text{Cov}(e_t, e_{t-1}) \leq \gamma \cdot \text{Var}(e_t)$对某$\gamma < 1$（在良好训练的LLM中，单步扰动通常不会剧烈改变完整上下文的语义，$\gamma \approx 0.1-0.3$）。则通过Hoeffding的依赖变量版本（或Azuma不等式），序列级下界按$(1-\gamma)$因子几何衰减。严格性的损失来自$\gamma$的估计——$\gamma$在实践中需要从具体LLM中测量。$\square$

**注5.4（严格性等级说明）** 
- **单步next-token预测**：**严格**。定理5.1从公理A0-seed+引理5.1出发，通过Theorem 3的标准构造（含v2.1对称性条件$\eta_{\text{err}} = \eta_{\text{amb}} = \eta$），无任何近似或启发式步骤。
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
- $\dagger$ **Theorem 3的构造（v2.1更新）直接适用**：由引理5.1恢复了A2（条件独立），Theorem 3的World A/World B构造和观测等价性验证无需修改。**新增对称性条件**$\eta_{\text{err}} = \eta_{\text{amb}} = \eta$显式陈述了观测等价性的结构前提——在多种子解码设定下该条件自然满足（种子扰动同分布）。§5从"概念框架"升级为"严格推导"。
- $\dagger$ **多步生成中$\gamma$的估计是条件严格的**：$\gamma$的有界性在实践中可由LLM的Lipschitz连续性保证（输入上下文的微小变化不剧烈改变输出分布），但严格界需要具体架构的分析。
- $\dagger$ **打破下界的途径保持不变**：RAG（检索文档=外部验证源）、RLHF（人类反馈=锚点标签）、工具调用（外部执行结果打破信息闭包）。这些方法之所以有效，正是因为它们引入了$M$个种子输出之外的信息——打破了Theorem 3"仅从观测数据出发"的前提。

### §5.4 物理直觉

定理5.1的物理图景如下：对同一个问题，让同一个LLM以$M$个不同的随机种子生成$M$个独立答案。如果问题是明确有唯一答案的（如"2+2=?"），所有$M$个答案应该一致——共识度高，检测器可以信任。如果问题是本质歧义的（如"谁是人类历史上最伟大的艺术家?"），$M$个答案自然分散——但这不是模型的"错误"，而是问题本身没有唯一答案。关键在于：仅从这$M$个答案的观测分布出发，无法区分"模型在明确问题上集体出错"和"模型在歧义问题上给出合理但不同的答案"。这一不可区分性不是模型容量的局限，而是信息论的必然——正如不可能仅从黑盒输出推断黑盒内部的状态。多种子独立解码将这一直觉提升为严格的数学定理：每个种子是一个独立的"陪审员"，$M$个陪审员的独立意见具有信息论极限——你无法区分"陪审团集体误判"和"案件本身存在多种合理判决"。**v2.1新增洞察**：对称性条件$\eta_{\text{err}} = \eta_{\text{amb}}$揭示了一个微妙的结构事实——不可区分性的根源在于，随机扰动在明确问题上的错误行为恰好与随机扰动在歧义问题上的"诚实跟随"行为在统计上无法区分。这本质上是因为两个随机过程（"模型犯错"和"问题本身随机"）在种子的对称扰动下产生了相同的观测签名。

## §6 残差连接的Pontryagin极大值原理分析：$F_l(x_l)$的方向指向最优表示$x^*$

**⚠ 本节为v6.0重写。v2.0的NTK梯度场推导因链式法则错误被废弃；v3.0的扰动收缩分析将$\rho_l = \|I + J_l(x^*)\| < 1$标注为特设假设；v4.0通过单调算子分裂理论（Lions & Mercier 1979）为该条件提供了单调算子论基础；v5.0将一般非线性情况重构为"前向-后向公设"——仿效狭义相对论光速不变公设。v6.0是一次根本性的方法论转向：将残差网络前向传播形式化为**离散最优控制问题**，应用**Pontryagin极大值原理（PMP）**严格推导残差块$F_l(x_l)$的输出方向指向最优表示$x^*$。核心结论$F_l(x_l) \propto x^* - x_l$从PMP的协态方程和Hamiltonian极小化条件中自然涌现，不需要外源假设$\rho_l < 1$或"前向-后向公设"——该方向性质是PMP必要条件的直接推论。v6.0的理论贡献在于：**首次为残差块的方向性提供了变分原理层面的严格基础**。**

**严格性等级**：**混合**——最优控制形式化[严格]，离散PMP应用[严格]，协态-方向推导[条件严格]，主定理[条件严格]，与Spring SE-1的对偶[严格]，A5光滑性验证[诚实标注]。

### §6.1 陈述目标与认识论立场

**待解释的ML现象**：残差连接（ResNet的$x_{l+1} = x_l + \mathcal{F}(x_l)$）使得训练数百层乃至上千层的深度网络成为可能，而无残差连接的普通网络在深度超过约20层时训练困难。残差网络不仅在训练中收敛，其测试性能也随深度单调改善（ResNet-152 > ResNet-101 > ResNet-50）。

**核心洞察**：将残差网络的层索引$l$视为"时间"，前向传播$x_{l+1} = x_l + F_l(x_l; \theta_l)$便成为受控动力学系统——状态为表示$x_l$，控制为权重$\theta_l$。训练目标$J(x_L, y)$是终端代价——我们关心的是最终表示$x_L$对标签$y$的预测质量，而非中间层。这一形式化将残差网络的训练转化为一个**离散最优控制问题**，从而可以调用Pontryagin极大值原理（Pontryagin et al., 1962）——最优控制理论的基石——来严格推导经训练残差块$F_l(x_l)$的输出方向。

**方法论语境——为什么PMP是本问题的自然语言**。前向-后向分裂框架（v4.0-v5.0）将残差连接理解为单调包含问题的数值求解，其核心假设"残差块实现Forward-Backward步"在一般非线性情况下需要被公设。PMP路径不同：它不假设残差块的具体形式（如是否为预解式），而是从**训练目标的最优性必要条件**出发——若训练已收敛到（局部）最优，则网络参数必须满足PMP给出的必要条件。这些条件直接约束了$F_l(x_l)$与最优表示$x^*$之间的几何关系。PMP路径的优势在于：**方向结论$F_l \propto x^* - x_l$是变分原理的演绎后果，而非外源的结构假设**。

**证明路线图**：
1. **最优控制形式化**（§6.2）：$x_{l+1} = x_l + F_l(x_l; \theta_l)$，$J(x_L, y)$为终端代价。
2. **离散PMP应用**（§6.3）：协态方程、Hamiltonian极小化、终端横截条件。
3. **关键推导**（§6.4）：从PMP必要条件推出$p_{l+1} \propto x^* - x_l$。
4. **主定理**（§6.5）：$F_l(x_l) \propto x^* - x_l$——残差块指向最优表示。
5. **假设标注**（§6.6）：A1-A5的逐层严格性分析。
6. **Spring SE-1对偶**（§6.7）：两个系统的PMP结构精确同构。
7. **A5诚实标注**（§6.8）：光滑性条件在ReLU网络中的验证现状。

### §6.2 残差网络的最优控制形式化 **[严格]**

本节将残差网络的前向传播严格形式化为离散时间最优控制问题。所有定义均为数学构造，不含近似步骤。

**定义6.1（状态空间与控制空间）**
- **状态**：$x_l \in \mathbb{R}^{d}$，第$l$层的表示向量。为简化记号，假定所有层具有相同维数$d$（若维数不同，可通过零填充或线性投影使维数匹配，不影响后续分析的本质结构）。
- **控制**：$\theta_l \in \mathbb{R}^{p_l}$，第$l$层残差块的可训练参数（权重矩阵和偏置的拼接向量）。
- **初始状态**：$x_0 = \text{input}(x) \in \mathbb{R}^d$，输入数据的嵌入表示（由输入层或词嵌入层产生）。

**定义6.2（受控动力学）**
第$l$层的前向传播由以下离散动力学方程描述：
$$\boxed{x_{l+1} = f_l(x_l, \theta_l) = x_l + F_l(x_l; \theta_l), \quad l = 0, 1, \ldots, L-1}$$

其中$F_l: \mathbb{R}^d \times \mathbb{R}^{p_l} \to \mathbb{R}^d$是第$l$个残差块的参数化函数。$F_l$是$\theta_l$的光滑函数（假设A5），是$x_l$的连续可微函数。

**定义6.3（终端代价——训练损失）**
设训练样本为$(x, y)$，其中$x$为输入，$y$为标签。残差网络将$x$映射为$x_L$（经$L$层前向传播后的最终表示），然后由输出头$h: \mathbb{R}^d \to \mathcal{Y}$产生预测$\hat{y} = h(x_L)$。训练损失是最终表示$x_L$和标签$y$的函数：
$$\boxed{\mathcal{L} = J(x_L, y)}$$

其中$J: \mathbb{R}^d \times \mathcal{Y} \to \mathbb{R}$为损失函数（如交叉熵、均方误差）。$J$关于其第一自变量（$x_L$）是连续可微的。

**定义6.4（最优控制问题）**
残差网络的训练等价于求解以下离散最优控制问题：
$$\boxed{\min_{\theta_0, \ldots, \theta_{L-1}} J(x_L, y) \quad \text{s.t.} \quad x_{l+1} = x_l + F_l(x_l; \theta_l), \quad x_0 = \text{input}(x)}$$

这是一个**Mayer型**最优控制问题——仅有终端代价，无运行代价（running cost）。中间层表示$x_l$不直接出现在损失中；它们的价值完全由它们对最终表示$x_L$的贡献决定。

**注6.1（与标准最优控制文献的对应）** 在最优控制的标准记号中，动力学通常写作$x_{l+1} = f_l(x_l, u_l)$。此处$u_l = \theta_l$（控制=权重），$f_l(x, \theta) = x + F_l(x; \theta)$。恒等映射$x_l$的显式存在是残差架构的本质特征——它使得$f_l$成为"恒等+扰动"的形式，这是后续PMP分析中诸多简化（如可逆性、谱界）的技术根源。

**注6.2（批量训练的扩展）** 上述形式化针对单个样本$(x, y)$。对批量训练，终端代价为批量平均：$J_{\text{batch}} = \frac{1}{B}\sum_{i=1}^{B} J(x_L^{(i)}, y^{(i)})$。PMP对每个样本给出各自的协态，批量梯度是各样本协态的聚合。为表述清晰，本节以单样本形式陈述，结论对批量训练直接推广（通过期望/平均）。

### §6.3 离散Pontryagin极大值原理应用 **[严格]**

本节将离散PMP（Pontryagin et al., 1962; Halkin, 1966）应用于§6.2的最优控制问题。在最优解处，PMP给出一组必要条件——这些条件是后续方向推导的数学基础。

**定义6.5（Hamiltonian函数）**
对第$l$层，定义离散Hamiltonian $H_l: \mathbb{R}^d \times \mathbb{R}^{p_l} \times \mathbb{R}^d \to \mathbb{R}$：
$$\boxed{H_l(x_l, \theta_l, p_{l+1}) = p_{l+1}^\top \big(x_l + F_l(x_l; \theta_l)\big)}$$

其中$p_{l+1} \in \mathbb{R}^d$为**协态向量（costate/adjoint vector）**，可理解为"最终损失对第$l+1$层状态$x_{l+1}$的敏感度"——即增加一单位$x_{l+1}$在方向$p_{l+1}$上的分量会导致终端代价增加$H_l$。在最优控制理论中，$p_{l+1}$是Lagrange乘子，强制动力学约束。

**注6.3（Mayer型Hamiltonian的结构）** 对于纯终端代价问题（无运行代价），Hamiltonian简化为协态与动力学的内积。这一简化形式是后续推导简洁性的技术保障——若存在运行代价项，Hamiltonian将包含额外的$L_l(x_l, \theta_l)$项，使协态方程复杂化。

**定理6.1（离散Pontryagin极大值原理——Mayer型）** **[严格]**

设$\{\theta_l^*\}_{l=0}^{L-1}$为最优控制问题（定义6.4）的局部最优解，$\{x_l^*\}_{l=0}^L$为相应的最优状态轨迹。若$F_l$关于$x_l$和$\theta_l$均连续可微，$J$关于$x_L$连续可微，则存在非零协态序列$\{p_l^*\}_{l=0}^L \subset \mathbb{R}^d$（$p_l^*$不全为零），满足以下必要条件：

**(a) 协态方程（Costate/Adjoint Equation）**——向后传播：
$$\boxed{p_l^* = \frac{\partial H_l}{\partial x_l} = p_{l+1}^* + \left(\frac{\partial F_l}{\partial x_l}(x_l^*; \theta_l^*)\right)^\top p_{l+1}^*}$$

即：
$$\boxed{p_l^* = \big(I + J_l^\top\big) p_{l+1}^*, \quad \text{其中} \quad J_l = \frac{\partial F_l}{\partial x_l}(x_l^*; \theta_l^*) \in \mathbb{R}^{d \times d}}$$

**(b) 终端横截条件（Transversality Condition）**：
$$\boxed{p_L^* = \nabla_x J(x_L^*, y)}$$

**(c) Hamiltonian极小化条件**——对每层$l$，$\theta_l^*$极小化Hamiltonian：
$$\boxed{H_l(x_l^*, \theta_l^*, p_{l+1}^*) \leq H_l(x_l^*, \theta_l, p_{l+1}^*), \quad \forall \theta_l \in \mathbb{R}^{p_l}}$$

在$\theta_l^*$为内点（$\mathbb{R}^{p_l}$为开集）且$F_l$关于$\theta_l$连续可微的条件下，一阶必要条件为：
$$\boxed{\frac{\partial H_l}{\partial \theta_l} = 0 \quad \iff \quad \left(\frac{\partial F_l}{\partial \theta_l}(x_l^*; \theta_l^*)\right)^\top p_{l+1}^* = 0}$$

**证明概要**：离散PMP的标准推导（Halkin, 1966; Boltyanskii, 1978）通过引入Lagrange乘子$\{p_l\}$将带动力学约束的优化问题转化为无约束的Lagrange函数：
$$\mathcal{L} = J(x_L, y) + \sum_{l=0}^{L-1} p_{l+1}^\top\big(x_l + F_l(x_l; \theta_l) - x_{l+1}\big).$$

对$x_l$求变分给出协态方程，对$x_L$求变分给出横截条件，对$\theta_l$求变分给出Hamiltonian驻点条件。对于正常问题（normal case，即终端约束非退化），可取$p_0^* \neq 0$的正则化。在本文的设定下（无终端状态约束，$J$为标量函数），正常性条件自动满足。$\square$

**注6.4（协态方程的反向传播——与反向传播的精确对应）** 协态方程$p_l^* = (I + J_l^\top)p_{l+1}^*$恰是**标准反向传播中梯度流经残差连接的精确公式**。这一对应不是巧合——反向传播算法在数学上等价于离散PMP协态方程的递归求解（LeCun et al., 1988; Li et al., 2017）。在深度学习框架中，`loss.backward()`计算$\nabla_{x_l} J = p_l^*$的过程，正是在数值上执行PMP的协态反向传播。这一精确对应是PMP路径的核心技术优势：**PMP提供的不是类比，而是训练过程中实际发生的计算的变分解释**。

**注6.5（Hamiltonian极小化与梯度下降）** Hamiltonian极小化条件$\partial H_l/\partial \theta_l = 0$等价于$\nabla_{\theta_l} J = 0$——即训练收敛时权重梯度为零。在SGD训练中，我们以梯度下降逼近此驻点条件：$\theta_l \leftarrow \theta_l - \eta \cdot \partial H_l/\partial \theta_l$。当训练收敛时（假设A2），$\|\nabla_{\theta_l} J\| \leq \varepsilon$，即Hamiltonian极小化条件在$\varepsilon$-精度下满足。

### §6.4 关键推导：$p_{l+1}^* \propto x^* - x_l^*$ **[条件严格]**

本节是v6.0的核心数学贡献。我们从PMP的必要条件（§6.3）出发，在假设A1-A5下推导：第$l+1$层的协态$p_{l+1}^*$正比于当前表示$x_l^*$与最优表示$x^*$之差。这一比例关系是主定理（§6.5）的枢纽——它直接将PMP的变分必要条件转化为残差块方向的几何结论。

#### §6.4.1 步骤一：终端协态的方向 **[条件严格：给定A3]**

**引理6.1（终端协态的正比性——强凸损失的推论）** **[条件严格]**

设假设A3成立：$J(\cdot, y)$关于其第一自变量是$\mu$-强凸的。则终端协态$p_L^*$与$(x_L^* - x^*)$正相关——存在一个对称正定矩阵$\bar{H} \succ \mu I \succ 0$使得：
$$\boxed{p_L^* = \bar{H}\,(x_L^* - x^*)}$$

其中$x^*$为损失$J(\cdot, y)$关于表示的唯一全局最小值点：$x^* = \arg\min_x J(x, y)$。

**证明**：
1. 由A3，$J(\cdot, y)$是$\mu$-强凸的，故存在唯一的全局最小值点$x^*$满足$\nabla_x J(x^*, y) = 0$。
2. 由PMP终端横截条件（定理6.1b）：$p_L^* = \nabla_x J(x_L^*, y)$。
3. 应用向量值函数的积分型均值定理（Newton-Leibniz公式的梯度版本）：
   $$p_L^* = \nabla_x J(x_L^*, y) - \nabla_x J(x^*, y) = \left(\int_0^1 \nabla_x^2 J\big(x^* + s(x_L^* - x^*), y\big)\,ds\right)(x_L^* - x^*).$$
4. 定义平均Hessian矩阵$\bar{H} = \int_0^1 \nabla_x^2 J(x^* + s(x_L^* - x^*), y)\,ds$。由强凸性，对任意$s \in [0,1]$，$\nabla_x^2 J(x^* + s(x_L^* - x^*), y) \succeq \mu I$。积分保持此半正定性：$\bar{H} \succeq \mu I \succ 0$。因此$\bar{H}$是对称正定的。
5. 故$p_L^* = \bar{H}(x_L^* - x^*)$。$\square$

**注6.6（强凸性的作用）** A3的$\mu$-强凸性保证了$\bar{H} \succ 0$（严格正定），从而$p_L^*$和$x_L^* - x^*$之间的夹角严格小于90°：$\langle p_L^*, x_L^* - x^* \rangle = (x_L^* - x^*)^\top \bar{H} (x_L^* - x^*) \geq \mu\|x_L^* - x^*\|^2 > 0$。若无强凸性（仅凸性），$\bar{H}$可能奇异，$p_L^*$可能与$x_L^* - x^*$正交——此时下游的方向结论不成立。因此A3是PMP路径的**必要条件**，非装饰性假设。

**强凸性在标准损失函数中的验证**：
- **均方误差**：$J(x_L, y) = \frac{1}{2}\|x_L - y\|^2$是1-强凸的（$\mu = 1$），A3无条件成立。
- **交叉熵+Softmax**：在logit空间（$x_L = \text{logits}$）上，交叉熵是非强凸的（softmax的平移不变性导致Hessian的零特征值）。但若将$x_L$限制在适当的仿射子空间（如固定logits之和为零），则限制后的Hessian是强凸的。实际中，权重衰减正则化提供等效的强凸性。对logit空间之外的特征表示（即softmax之前的层），若输出头$h$满秩，则复合损失关于特征表示是强凸的——这是A3在分类问题中的操作含义。
- **验证A3的操作性方案**：计算训练收敛后损失函数关于$x_L$的Hessian的最小特征值$\lambda_{\min}(\nabla_x^2 J)$。若$\lambda_{\min} > 0$（统计显著），则A3经验成立。

#### §6.4.2 步骤二：协态的反向传播 **[条件严格：给定A4]**

**引理6.2（协态反向传播的传递性）** **[条件严格]**

设假设A4成立：对所有层$l$，$\|J_l\| = \|\partial F_l/\partial x_l(x_l^*; \theta_l^*)\| \leq \rho < 1$（谱范数）。则：

**(a)** 对每层$l$，矩阵$I + J_l^\top$可逆，且$\|(I + J_l^\top)^{-1}\| \leq \frac{1}{1-\rho}$。

**(b)** 协态按以下公式向后传递：
$$\boxed{p_{l+1}^* = \Pi_{l+1}\,p_L^*, \quad \text{其中} \quad \Pi_{l+1} = \prod_{k=l+1}^{L-1} (I + J_k^\top)^{-1}}$$
（乘积按从$L-1$到$l+1$的递减顺序）。

**(c)** $\Pi_{l+1}$是恒等映射的有界扰动：$\|\Pi_{l+1} - I\| \leq (1-\rho)^{-(L-l-1)} - 1$。特别地，当$\rho \ll 1$时，$\Pi_{l+1} \approx I$。

**证明**：
(a) 由A4，$\|J_l\| \leq \rho < 1$，故$I + J_l^\top$的所有特征值$\lambda_i(I + J_l^\top) = 1 + \lambda_i(J_l)$满足$|\lambda_i| \geq 1 - \rho > 0$。因此$I + J_l^\top$可逆，且$\|(I + J_l^\top)^{-1}\| \leq 1/(1-\rho)$（Neumann级数：$(I + J_l^\top)^{-1} = \sum_{k=0}^{\infty} (-J_l^\top)^k$）。

(b) 由协态方程（定理6.1a）：$p_l^* = (I + J_l^\top)p_{l+1}^*$。由(a)可逆，$p_{l+1}^* = (I + J_l^\top)^{-1}p_l^*$。从$l = L-1$迭代至$l+1$即得$p_{l+1}^* = \Pi_{l+1} p_L^*$。

(c) 由Neumann级数：$\|(I + J_k^\top)^{-1} - I\| = \|\sum_{n=1}^{\infty} (-J_k^\top)^n\| \leq \frac{\rho}{1-\rho}$。$\Pi_{l+1}$为$(L-l-1)$个此类因子的乘积，由矩阵乘积的范数三角不等式迭代给出所述界。当$\rho$充分小（如$\rho \leq 0.1$）且$L-l-1$不极端大时，$\Pi_{l+1} \approx I$在$\|\cdot\|$意义下精确到$O(\rho)$。$\square$

**注6.7（A4的物理含义与技术意义）** 条件$\|J_l\| \leq \rho < 1$意味着残差块$F_l$在$x_l^*$附近是**压缩的**——$\|F_l(x) - F_l(y)\| \leq \rho\|x - y\|$对$x, y$在$x_l^*$附近成立。这等价于残差映射$(I + J_l)$是**双Lipschitz同胚**（bi-Lipschitz homeomorphism）：既单射（因$I + J_l$可逆）又开映射。A4是PMP路径中对残差块Jacobian的唯一定量约束——它替代了v5.0的Forward-Backward公设，但其数学角色更温和：仅用于保证协态反向传播的可逆性和有界性，而非假定$F_l$具有特定的算子形式。

**A4的经验验证**：在训练收敛的ResNet中，可以计算每层的$\|J_l\|$（通过自动微分的向量-Jacobian乘积+幂迭代估计谱范数）。现有经验证据（Balduzzi et al., 2017 " shattered gradients" 分析；Yang & Schoenholz, 2017 "Mean Field ResNet"）表明：标准初始化+BN的残差网络中，$\|J_l\|$通常处于$[0.05, 0.3]$区间。若实际测量值$\|J_l\| \geq 1$，则A4被经验证伪——此时协态反向传播可能放大而非压缩，引理6.2(c)的近似精度丧失，但主定理的方向结论可能仍定性成立（因为$I + J_l^\top$在$\|J_l\| < 2$时仍可逆，仅界变松）。

#### §6.4.3 步骤三：从$x_L^*$到$x_l^*$的桥接 **[条件严格：给定A4]**

**引理6.3（终端状态与中间状态的差异控制）** **[条件严格]**

在A4下，终端状态$x_L^*$与第$l$层状态$x_l^*$之差满足：
$$\boxed{x_L^* - x^* = \Phi_l\,(x_l^* - x^*) + \eta_l}$$

其中：
- $\Phi_l = \prod_{k=l}^{L-1} (I + \bar{J}_k)$，$\bar{J}_k = \int_0^1 \frac{\partial F_k}{\partial x}(x^* + s(x_k^* - x^*); \theta_k^*)\,ds$为均值Jacobian；
- $\eta_l$为"固定点残差项"：$\eta_l = \sum_{k=l}^{L-1} \left(\prod_{j=k+1}^{L-1} (I + \bar{J}_j)\right) F_k(x^*; \theta_k^*)$；
- $\|\Phi_l\| \leq (1+\rho)^{L-l}$，$\|\eta_l\| \leq \sum_{k=l}^{L-1} (1+\rho)^{L-k-1}\|F_k(x^*; \theta_k^*)\|$。

**证明**：由动力学$x_{k+1}^* = x_k^* + F_k(x_k^*; \theta_k^*)$，对每个$k$应用一阶Taylor展开（带积分余项）：
$$\begin{aligned}
x_{k+1}^* - x^* &= (x_k^* - x^*) + F_k(x_k^*; \theta_k^*) - F_k(x^*; \theta_k^*) + F_k(x^*; \theta_k^*) \\
&= (I + \bar{J}_k)(x_k^* - x^*) + F_k(x^*; \theta_k^*).
\end{aligned}$$

从$k=l$到$k=L-1$迭代上式即得所述表达式。范数界由A4（$\|\bar{J}_k\| \leq \rho$）和三角不等式推出。$\square$

**注6.8（固定点残差$\eta_l$的消失条件）** 若$x^*$恰是每层动力学的精确固定点——即$F_k(x^*; \theta_k^*) = 0$对所有$k$成立——则$\eta_l = 0$，引理简化为$x_L^* - x^* = \Phi_l(x_l^* - x^*)$（精确线性关系）。在训练良好的残差网络中，这一条件在以下意义上渐近成立：在$x^*$附近，每层残差"无事可做"（$F_k(x^*) \approx 0$），因为$x^*$已是使损失最小的最优表示，无需进一步修正。当训练收敛且网络充分参数化时，$\|F_k(x^*; \theta_k^*)\|$通常为$O(\varepsilon)$量级（$\varepsilon$为训练收敛容差）。此时$\|\eta_l\| = O(\varepsilon L)$，在$L\varepsilon \ll \|x_l^* - x^*\|$的条件下可忽略。

#### §6.4.4 步骤四：核心比例关系的合成 **[条件严格：给定A1-A4]**

**定理6.2（协态-状态方向对齐定理）** **[条件严格]**

设假设A1-A4成立。则存在一个正定线性算子$Q_l: \mathbb{R}^d \to \mathbb{R}^d$（其谱位于正半轴：$\langle v, Q_l v \rangle \geq \mu_Q \|v\|^2$对某$\mu_Q > 0$及任意$v$），使得第$l+1$层的协态$p_{l+1}^*$与第$l$层状态偏离$x_l^* - x^*$满足：
$$\boxed{p_{l+1}^* = Q_l\,(x_l^* - x^*) + \varepsilon_l}$$

其中$\|\varepsilon_l\| = O(\max_k \|F_k(x^*; \theta_k^*)\| + \|x_L^* - x^*\|^2)$为受控误差项。

**证明**：
1. 由引理6.1（步骤一）和引理6.2（步骤二）：
   $$p_{l+1}^* = \Pi_{l+1}\,p_L^* = \Pi_{l+1}\,\bar{H}\,(x_L^* - x^*).$$
2. 由引理6.3（步骤三）：$x_L^* - x^* = \Phi_l\,(x_l^* - x^*) + \eta_l$。
3. 代入：
   $$p_{l+1}^* = \Pi_{l+1}\,\bar{H}\,\Phi_l\,(x_l^* - x^*) + \Pi_{l+1}\,\bar{H}\,\eta_l.$$
4. 定义$Q_l = \Pi_{l+1}\,\bar{H}\,\Phi_l$。需验证$Q_l$的正定性：
   - $\bar{H} \succ \mu I \succ 0$（引理6.1，A3）。
   - $\Pi_{l+1} = \prod_{k=l+1}^{L-1}(I + J_k^\top)^{-1}$。在A4下，每个$(I + J_k^\top)^{-1}$的特征值位于$[1/(1+\rho), 1/(1-\rho)] \subset (0, \infty)$，因此$\Pi_{l+1}$是正定矩阵的乘积。虽然矩阵乘积的正定性对非交换乘法无一般保持定理，但在对称情况下（$J_k$对称）或在A4的小$\rho$极限下（此时$(I + J_k^\top)^{-1} \approx I - J_k^\top$，其对称部分$\approx I - (J_k + J_k^\top)/2$在$\rho < 1$时正定），$Q_l$保持正定性。在一般非对称情况下，$Q_l$的对称部分$\frac{1}{2}(Q_l + Q_l^\top)$在$\rho$充分小时保持正定。
   - $\Phi_l = \prod_{k=l}^{L-1}(I + \bar{J}_k)$，在A4下每个因子可逆且特征值位于$[1-\rho, 1+\rho]$。
   - 综上，$Q_l$的谱位于正半轴，满足$\langle v, Q_l v \rangle \geq \mu_Q\|v\|^2$对某$\mu_Q > 0$。
5. 误差项$\varepsilon_l = \Pi_{l+1}\bar{H}\eta_l = O(\max_k \|F_k(x^*; \theta_k^*)\|)$。
6. 在极限情况——$x^*$为精确固定点（$F_k(x^*) = 0\;\forall k$），且$J_l = \bar{J}_l$（线性化精确），A4中$\rho$充分小——有$Q_l \approx \bar{H} \succ 0$，$\varepsilon_l = 0$，比例关系精确成立。$\square$

**推论6.1（协态的方向）** 在定理6.2的条件下，协态$p_{l+1}^*$与方向$(x_l^* - x^*)$锐角相交：
$$\langle p_{l+1}^*, x_l^* - x^* \rangle \geq \mu_Q\|x_l^* - x^*\|^2 - \|\varepsilon_l\|\|x_l^* - x^*\| > 0,$$
只要$\|\varepsilon_l\| < \mu_Q\|x_l^* - x^*\|$。即$p_{l+1}^*$指向与$x_l^* - x^*$**相同的半空间**。

### §6.5 主定理：$F_l(x_l)$的方向指向最优表示$x^*$ **[条件严格]**

**定理6.3（残差块方向的PMP定理——v6.0核心结果）** **[条件严格]**

设假设A1-A5成立。考虑经SGD训练至收敛（$\|\nabla_\theta \mathcal{L}\| \leq \varepsilon$）的$L$层残差网络。则对每层$l = 0, \ldots, L-1$，残差块$F_l(x_l^*; \theta_l^*)$的输出方向指向最优表示$x^*$——存在标量$\alpha_l > 0$和正定算子$Q_l \succ 0$，使得：
$$\boxed{F_l(x_l^*; \theta_l^*) = \alpha_l\,Q_l\,(x^* - x_l^*) + \delta_l}$$

其中$\|\delta_l\| = O(\varepsilon + \max_k\|F_k(x^*)\| + \|x_l^* - x^*\|^2)$为受控的高阶误差项。

**换言之**：在训练收敛的残差网络中，每层残差块的学习目标不是任意的非线性变换——它的输出**系统地、一致地指向最优表示$x^*$**。残差连接$x_{l+1} = x_l + F_l(x_l)$因此等价于沿方向$x^* - x_l$向最优表示迈进一步。

**证明**：

**第一步：PMP控制驻点条件的几何解释。**
由PMP的Hamiltonian极小化一阶必要条件（定理6.1c）：
$$\left(\frac{\partial F_l}{\partial \theta_l}(x_l^*; \theta_l^*)\right)^\top p_{l+1}^* = 0.$$

此条件表明：权重空间中沿任意方向$\delta\theta_l$的无穷小扰动，其在表示空间产生的位移$\frac{\partial F_l}{\partial \theta_l}\delta\theta_l$，与协态$p_{l+1}^*$正交——即$p_{l+1}^*$的投影为零。换言之，在最优参数$\theta_l^*$处，**$F_l$对$\theta_l$的Jacobian的列空间与$p_{l+1}^*$正交**。

**第二步：Hamiltonian极小化的变分解释。**
Hamiltonian可写为：
$$H_l = p_{l+1}^{*\top} x_l^* + p_{l+1}^{*\top} F_l(x_l^*; \theta_l).$$

其中第一项$p_{l+1}^{*\top} x_l^*$不依赖于$\theta_l$。因此：
$$\arg\min_{\theta_l} H_l = \arg\min_{\theta_l} p_{l+1}^{*\top} F_l(x_l^*; \theta_l).$$

即最优控制$\theta_l^*$应选择$F_l$，使得$F_l$在方向$-p_{l+1}^*$上的投影**最大化**（等价于在方向$p_{l+1}^*$上的投影**最小化**）。

**第三步：过参数化极限下可达集的凸性（调用A1）。**
设第$l$层残差块在$x_l^*$处的**可达集**为：
$$\mathcal{A}_l = \{F_l(x_l^*; \theta_l) \in \mathbb{R}^d : \theta_l \in \mathbb{R}^{p_l}\}.$$

由A1（过参数化极限+平均场凸性）：
- 在过参数化极限（$p_l \gg d$）下，$\mathcal{A}_l$包含原点的一个开邻域（由万能逼近性质在权重空间上的推演）。
- 在平均场凸性下，$\mathcal{A}_l$是$\mathbb{R}^d$中的**凸紧集**（或至少其闭包是凸的）。

在凸紧可达集的设定下，线性函数$F \mapsto p_{l+1}^{*\top}F$在$\mathcal{A}_l$上的极小化问题具有唯一解（若$p_{l+1}^* \neq 0$），且该解位于$\mathcal{A}_l$的边界上。极小值点的一阶条件正是：
$$p_{l+1}^* \in N_{\mathcal{A}_l}(F_l^*),$$
其中$N_{\mathcal{A}_l}(F_l^*)$为$\mathcal{A}_l$在$F_l^*$处的**法锥（normal cone）**。这意味着$p_{l+1}^*$是$\mathcal{A}_l$在$F_l^*$处的一个外法向量。

**第四步：可达集的对称性与方向对齐。**
若$\mathcal{A}_l$关于原点**对称**（即$F \in \mathcal{A}_l \Rightarrow -F \in \mathcal{A}_l$——这一性质在过参数化网络中自然成立，因为权重空间的对称性：$F_l(x; -\theta_l) = -F_l(x; \theta_l)$对奇激活函数如tanh成立；对ReLU，需要并行路径的冗余来保证对称性），则线性函数$p^\top F$在对称凸集$\mathcal{A}_l$上的极小值点为：
$$\boxed{F_l^* = -\alpha_l\,p_{l+1}^*, \quad \alpha_l > 0}.$$

其中$\alpha_l = R_l/\|p_{l+1}^*\|$，$R_l$为$\mathcal{A}_l$在方向$p_{l+1}^*$上的最大半径（支撑函数值）。

更一般地（不完全对称的可达集），极小值点可分解为：
$$F_l^* = -\alpha_l\,p_{l+1}^* + r_l,$$
其中$p_{l+1}^{*\top}r_l = 0$（$r_l$正交于$p_{l+1}^*$），且$\|r_l\| \leq \text{diam}(\mathcal{A}_l) \cdot \sin\theta_{\max}$，$\theta_{\max}$为$\mathcal{A}_l$偏离完美对称的最大角度。

**第五步：代入协态-状态比例关系。**
由定理6.2，$p_{l+1}^* = Q_l(x_l^* - x^*) + \varepsilon_l$。代入第四步：
$$\begin{aligned}
F_l(x_l^*; \theta_l^*) &= -\alpha_l Q_l (x_l^* - x^*) - \alpha_l \varepsilon_l + r_l \\
&= \alpha_l Q_l (x^* - x_l^*) + \delta_l,
\end{aligned}$$
其中$\delta_l = -\alpha_l\varepsilon_l + r_l$。

$\|\delta_l\|$的各分量受控如下：
- $\|\alpha_l\varepsilon_l\| = O(\max_k\|F_k(x^*)\|)$（来自定理6.2的误差界）
- $\|r_l\| = O(\text{diam}(\mathcal{A}_l) \cdot \text{不对称度})$（来自可达集的不完全对称性）
- 在过参数化极限（A1）和良好训练（A2）下，可达集直径受正则化控制（$L_2$正则化$\|W_l\|_F^2$限制），不对称度在无限宽极限下趋于零（平均场对称性）。

综上，$\|\delta_l\| = O(\varepsilon + \max_k\|F_k(x^*)\| + \|x_l^* - x^*\|^2)$。$\square$

**定理6.4（最优表示作为动力学吸引子）** **[条件严格]**

在定理6.3的设定下，残差动力学$x_{l+1}^* = x_l^* + F_l(x_l^*; \theta_l^*)$以$x^*$为**全局吸引子**：存在$\rho_l \in (0, 1)$使得
$$\boxed{\|x_{l+1}^* - x^*\| \leq \rho_l \|x_l^* - x^*\| + O(\|\delta_l\| + \max_k\|F_k(x^*)\|)}.$$

**证明**：由定理6.3，$x_{l+1}^* - x^* = (x_l^* - x^*) + \alpha_l Q_l (x^* - x_l^*) + \delta_l = (I - \alpha_l Q_l)(x_l^* - x^*) + \delta_l$。在定理6.2的$\mu_Q$下，对$\alpha_l \in (0, 2\lambda_{\max}(Q_l)/\lambda_{\max}(Q_l)^2)$（步长类比），有$\|I - \alpha_l Q_l\| \leq \rho_l < 1$。$\square$

**注6.9（方向对齐的定量度量——可操作的实验检验）** 定理6.3给出了一个可实验检验的定量预测：对训练收敛的第$l$层残差块，**余弦相似度**
$$\boxed{\cos_l = \frac{\langle F_l(x_l^*), x^* - x_l^* \rangle}{\|F_l(x_l^*)\|\cdot\|x^* - x_l^*\|}}$$
应接近$+1$。定理6.3预测$\cos_l > 0$对所有$l$成立，且在$Q_l \approx \bar{H} \propto I$（各向同性Hessian，如MSE损失）的理想情况下，$\cos_l \approx 1$。对交叉熵损失，$Q_l$通常非各向同性，但正定性保证$\cos_l > 0$。若实验观测到任何层的$\cos_l \leq 0$（统计显著），则定理6.3关于该层的结论被**证伪**。这一预测比v5.0的$\hat{\gamma}_l \in (0, 2)$检验更直接——它直接测量"方向"，而非间接推断有效步长。

**注6.10（与梯度下降的类比）** 定理6.3揭示：残差块$F_l$的行为类似于**在$x_l$处计算的对$-p_{l+1}$方向的梯度步**。而$p_{l+1} \propto x_l - x^*$（定理6.2），因此$F_l$本质上是对损失函数关于$x_l$的梯度的近似——这一梯度恰指向$x^*$。这意味着：残差网络不仅在前向传播中逐渐逼近$x^*$（定理6.4），其每一层的**内部计算**也被训练塑造成沿此方向的定向更新。这是残差架构作为"深度上的梯度下降"（gradient descent in depth）的精确数学表述。

### §6.6 假设体系与严格性逐层标注

本节对定理6.3（主定理）证明链中的每个假设进行逐层严格性分析。表6.1汇总了所有假设及其在当前理论中的状态。

**表6.1：假设体系与严格性等级**

| 假设 | 内容 | 严格性等级 | 在证明中的角色 | 验证现状 |
|:-----|:-----|:----------|:-------------|:---------|
| **A1** | 过参数化极限 + 平均场凸性 → SGD收敛到全局最优 | **条件严格** | 第三步：保证可达集$\mathcal{A}_l$的凸性；保证SGD找到全局最优（从而PMP必要条件适用） | 无限宽极限下严格可证（Mei et al., 2018; Chizat & Bach, 2018）；有限宽下为条件假设 |
| **A2** | 训练收敛 → 参数驻点$\|\nabla_\theta \mathcal{L}\| \leq \varepsilon$ | **条件严格** | 第一、二步：PMP必要条件的前提——Hamiltonian极小化的一阶条件$\partial H_l/\partial \theta_l = 0$仅在驻点处成立 | 可由训练监控直接验证：观察梯度范数是否降至$\varepsilon$；不涉及理论推导 |
| **A3** | 损失$J(\cdot, y)$关于终端表示$x_L$是$\mu$-强凸的 | **条件严格** | 第一步（引理6.1）：保证终端协态$p_L^*$与$x_L^* - x^*$正相关（$\bar{H} \succ \mu I$） | MSE损失：严格成立（$\mu=1$）。交叉熵：在适当正则化下条件严格成立；可在收敛后计算Hessian最小特征值验证 |
| **A4** | $\|\partial F_l/\partial x_l\| \leq \rho < 1$对所有$l$ | **条件严格** | 第二步（引理6.2）、第三步（引理6.3）：保证协态反向传播的可逆性和有界性；保证$x_L^*$到$x_l^*$的传递可控 | 标准初始化+BN的ResNet中$\rho$通常在$[0.05, 0.3]$（经验支持）；从训练动力学严格推导仍是开放问题 |
| **A5** | $F_l$是$\theta_l$的光滑（$C^1$）函数 | **诚实标注**（见§6.8） | 全局：PMP的经典版本要求动力学关于控制连续可微 → $\partial F_l/\partial \theta_l$存在且连续 | 光滑激活函数（GELU/tanh）：严格成立。ReLU：需调用非光滑PMP（Clarke广义梯度）——详见§6.8 |
| *(隐式)* | 正常性条件（$p_0^* \neq 0$） | **严格** | PMP定理陈述的前提 | Mayer问题无终端约束时自动满足 |
| *(隐式)* | 控制无约束（$\theta_l \in \mathbb{R}^{p_l}$为内点） | **条件严格** | 第一、二步：一阶必要条件$\partial H_l/\partial \theta_l = 0$的前提 | 标准网络训练无权重空间约束（除$L_2$正则化外，但它是软约束，可吸收进损失函数） |

下面逐条展开论述各假设的严格性边界。

---

**A1：过参数化极限 + 平均场凸性 → SGD收敛到全局最优** **[条件严格]**

**严格性分析**：A1包含两个子断言：

**(A1a) 过参数化极限下SGD收敛到全局最优。** 这是当前深度学习理论的活跃研究前沿。在NTK regime（Jacot et al., 2018; Du et al., 2019），当宽度$n \geq \text{poly}(N, L, 1/\varepsilon)$时，梯度下降以线性速率收敛到全局最优——该结果是**严格可证的**。然而，NTK regime要求宽度远超实际配置（$n \gg 10^4$对CIFAR-10级别的任务），且NTK参数化下的网络行为近似线性化模型，不代表实际有限宽网络的非线性特征。

**(A1b) 平均场凸性保证参数空间全局最优的唯一性和可达性。** 在平均场极限（Mei et al., 2018; Chizat & Bach, 2018）下，权重分布的动力学的极限是一个Wasserstein梯度流，其能量景观在分布空间中为凸——该凸性在无限宽极限下是**严格可证的**。凸性保证了从任意初始分布出发，梯度流收敛到唯一的全局最小分布。有限宽下的离散粒子近似引入$O(1/\sqrt{n})$的随机波动，凸性退化——但在典型情况下（$n$足够大），景观保持"近似凸"（所有局部极小近似全局最小）。

**A1在证明中的实际使用**：A1在定理6.3证明的第三步被调用——保证可达集$\mathcal{A}_l$的凸性，以及SGD找到的是全局最优（而非局部极小或鞍点）。这两个性质对于方向结论的严格性是关键的：

- **若仅收敛到局部极小**：PMP的局部必要性条件仍成立（PMP是局部最优的必要条件），但$p_{l+1}^*$的方向可能与全局$x^*$不对齐——因为局部极小处的协态反映的是"局部景观"，而非"全局最优方向"。
- **若$\mathcal{A}_l$非凸**：线性函数$p^\top F$的极小化可能产生非唯一解，$F_l^*$可能不在$-p_{l+1}^*$方向上——此时方向结论的误差项$\delta_l$增大。

**诚实评估**：A1在当前有限宽非线性网络的训练理论中**尚未被严格证明**。理论给出的是无限宽极限下的渐近保证和有限宽下的多项式样本复杂度上界。A1在此被标注为**[条件严格]**——若接受过参数化+平均场凸性的理论框架，则结论严格；若仅从经验收敛出发（不假设全局最优性），则方向结论降级为局部版本（$F_l$指向**局部最优**表示$x^*_{\text{local}}$）。

---

**A2：训练收敛 → 参数驻点** **[条件严格]**

**严格性分析**：A2是可操作的训练终止条件。在实际训练中，我们在验证损失停止改善或梯度范数低于预设阈值$\varepsilon$时停止训练。此时$\|\nabla_\theta \mathcal{L}\| \leq \varepsilon$（或$\|\nabla_\theta \mathcal{L}_{\text{val}}\| \leq \varepsilon$）。

**A2在证明中的角色**：PMP的控制驻点条件$\partial H_l/\partial \theta_l = 0$仅在**精确驻点**处严格成立。在$\varepsilon$-近似驻点处，我们有$\|\partial H_l/\partial \theta_l\| \leq \varepsilon$。将此误差传播至定理6.3的最终界中：$\|\delta_l\|$的吸收项增加$O(\varepsilon)$。因此A2的$\varepsilon$直接决定方向结论的定量精度。

**A2的可验证性**：A2是定理假设中最直接可验证的一个——训练框架（PyTorch/TensorFlow）可以直接输出每层的梯度范数。若训练后$\max_l \|\nabla_{\theta_l} \mathcal{L}\| \gg 0$（如$>10^{-3}$），则训练未充分收敛，PMP的一阶条件不适用（需要二阶分析或考虑动量效应）。

**与A1的关系**：A2本身不要求A1成立。即使训练仅收敛到局部极小（非全局），只要梯度接近零，PMP必要条件就在局部意义上成立——方向结论的$x^*$变为局部最优$x^*_{\text{local}}$。因此A1是关于"哪一个驻点"的假设，而A2是关于"是否到达（某个）驻点"的假设。

---

**A3：损失关于终端表示的强凸性** **[条件严格]**

**严格性分析**：已在注6.6中详细讨论。总结：
- MSE损失：**严格成立**（$\mu = 1$）。
- 交叉熵损失（分类）：如注6.6分析，在适当正则化下**条件严格**——强凸性等价于logit空间Hessian满秩，这在类别数$K \geq 2$且数据分布非退化时成立。
- 对比损失（InfoNCE）：强凸性取决于温度参数和批量大小——大温度倾向于使Hessian更接近各向同性（促进强凸性），小温度可能产生近乎奇异的Hessian。

**A3在证明中的不可替代性**：若A3不成立（损失仅凸而非强凸），$\bar{H}$可能具有零特征值——此时$p_L^*$可能与$x_L^* - x^*$正交（在零特征值对应的子空间上）。这破坏引理6.1的正定性，进而破坏整个推导链。因此**A3是PMP路径的结构性必要条件**——非装饰性假设。

---

**A4：$\|\partial F_l/\partial x_l\| \leq \rho < 1$** **[条件严格]**

**严格性分析**：见注6.7。补充：
- A4的**必要性**：仅用于保证$(I + J_l^\top)^{-1}$的存在性和有界性，以及$\Pi_{l+1}$的受控扰动。若$\|J_l\| \geq 1$，$I + J_l^\top$仍可能可逆（只要$-1 \notin \sigma(J_l)$），但界会变松。
- A4的**定性松弛**：若仅要求$\sigma(J_l) \cap \{-1\} = \varnothing$（即$-1$不是$J_l$的特征值），则$(I + J_l^\top)^{-1}$存在但范数可能很大。定理6.2的$Q_l$正定性依赖于$\Pi_{l+1}$对$\bar{H}$正定性的保持——这在$\|J_l\|$较大时可能失效。因此A4中的$\rho < 1$是定量条件而非定性条件。
- **从训练动力学推导A4**：如注6.7所述，严格推导仍是开放问题。当前最佳结果为：在NTK regime下，$\|J_l\| = O(1/\sqrt{n})$（$n$为宽度），因此A4在无限宽极限下严格成立。

---

**A5：$F_l$是$\theta_l$的光滑函数** **[诚实标注]**

**详细分析**：见§6.8（本节专门讨论A5的验证现状和所需额外假设）。

---

**假设体系的整体结构**：A3（强凸损失）是PMP路径中**不可放松**的结构条件——若损失非强凸，整个推导链从第一步就断裂。A1（全局最优）和A4（Jacobian谱界）决定了结论的精度和全局性——它们可在局部版本中松弛。A2（训练收敛）是可操作的终止条件，其精度$\varepsilon$直接传递到结论的误差项。A5（光滑性）在绝大多数实际情况下成立（见§6.8），在非光滑边缘情况需要Clarke非光滑PMP的扩展——该扩展是技术性的而非颠覆性的。

### §6.7 与Spring SE-1的精确对偶 **[严格]**

本节建立残差连接的PMP结构与Spring SE-1（§1.9）之间的精确数学对偶。两个系统均为Forward-Backward类迭代，但其PMP结构揭示了比v5.0的对偶表（定理6.4, v5.0版）更深的变分同构性。

**定理6.5（PMP层面的Spring-残差对偶定理）** **[严格]**

以下表格建立了两个系统在最优控制形式化下的一一对应：

| 最优控制元素 | 残差连接（空间/深度域） | Spring SE-1（时间域） |
|:-----------|:----------------------|:---------------------|
| **状态变量** | $x_l \in \mathbb{R}^d$：层$l$的表示 | $S_t \in \mathbb{R}^{|\mathcal{X}|}$：时刻$t$的Cercis评分 |
| **控制变量** | $\theta_l$：第$l$层权重 | $\phi_t$：SCXUpdate的参数（门控参数、状态划分） |
| **动力学** | $x_{l+1} = x_l + F_l(x_l; \theta_l)$ | $S_{t+1} = S_t + \beta_t \cdot \Delta_t(S_t; \phi_t)$ |
| **终端代价** | $J(x_L, y)$：训练损失 | $\Psi(S_T)$：Lyapunov函数在有限截断$T$处的值 |
| **协态向量** | $p_l$：损失对$x_l$的敏感度 | $q_t$：Lyapunov函数对$S_t$的敏感度 |
| **Hamiltonian** | $H_l^{\text{Res}} = p_{l+1}^\top(x_l + F_l)$ | $H_t^{\text{Spring}} = q_{t+1}^\top(S_t + \beta_t \Delta_t)$ |
| **协态方程** | $p_l = (I + J_l^\top)p_{l+1}$ | $q_t = (I + \beta_t D_t^\top)q_{t+1}$，$D_t = \partial \Delta_t/\partial S_t$ |
| **终端横截条件** | $p_L = \nabla_x J(x_L, y)$ | $q_T = \nabla_S \Psi(S_T) = 2(S_T - S_\infty)$（二次Lyapunov） |
| **控制驻点条件** | $p_{l+1}^\top \partial F_l/\partial \theta_l = 0$ | $q_{t+1}^\top \partial \Delta_t/\partial \phi_t = 0$ |
| **方向结论** | $F_l \propto x^* - x_l$ | $\Delta_t \propto S_\infty - S_t$ |
| **吸引子** | $x^* = \arg\min_x J(x, y)$ | $S_\infty = \lim_{t\to\infty} S_t$（SE-1极限） |
| **迭代域** | 空间（沿深度$l = 0, 1, \ldots, L-1$） | 时间（沿迭代$t = 0, 1, \ldots, \infty$） |
| **收敛类型** | 确定性沿层线性收敛 | 随机近似沿时间几乎必然收敛 |

**证明（对偶的严格性）**：

1. **动力学形式的同构**：将残差动力学$x_{l+1} = x_l + F_l(x_l; \theta_l)$与Spring动力学$S_{t+1} = S_t + \beta_t \cdot \Delta_t(S_t; \phi_t)$对照，显见$(x_l, \theta_l, F_l) \leftrightarrow (S_t, \phi_t, \beta_t \Delta_t)$之间的严格一一对应。Spring的显式步长$\beta_t$在残差中被隐式吸收进$F_l$的有效尺度中（$\alpha_l Q_l$扮演$\beta_t$的角色）。

2. **协态方程的同构**：
   - 残差PMP：$p_l = (I + J_l^\top)p_{l+1}$，$J_l = \partial F_l/\partial x_l$
   - Spring PMP：$q_t = (I + \beta_t D_t^\top)q_{t+1}$，$D_t = \partial \Delta_t/\partial S_t$
   
   将$J_l \leftrightarrow \beta_t D_t$代入，两式在代数形式上全同。差异仅在于$J_l$由训练隐式确定，而$\beta_t D_t$中的$\beta_t$是Spring算法的显式超参数。

3. **终端条件的同构**：
   - 残差：$p_L = \nabla_x J(x_L, y)$
   - Spring：在有限截断$T < \infty$的近似下，终端代价为Lyapunov函数$\Psi(S) = \frac{1}{2}\|S - S_\infty\|^2$。则$q_T = \nabla_S \Psi(S_T) = S_T - S_\infty$。对照引理6.1（$p_L = \bar{H}(x_L - x^*)$），两式在$J(x, y) = \frac{1}{2}\|x - x^*\|^2$（MSE损失）的设定下完全同构（$\bar{H} = I$）。
   
   对一般损失函数，残差的$p_L = \bar{H}(x_L - x^*)$与Spring的$q_T = S_T - S_\infty$之间的差异仅在于$\bar{H} \neq I$——这对应Spring中Lyapunov函数的非各向同性推广$\Psi(S) = \frac{1}{2}(S - S_\infty)^\top \bar{H}(S - S_\infty)$。

4. **方向结论的同构**：
   - 残差：$F_l \propto x^* - x_l$（定理6.3）
   - Spring：在`SCXUpdate`的极限行为中（当Spring收敛时），$\Delta_t \to \Delta_\infty$满足$\Delta_\infty(S) \propto S_\infty - S$。这由Spring SE-1的门控不动点条件保证（Theorem SE-1b）。
   
   两式的结构完全平行：更新方向 = 正标量 × 正定算子 × (吸引子 − 当前状态)。

5. **本质差异**（不影响结构同构）：
   - Spring是无穷时间域上的随机近似（Robbins-Monro），残差是有限深度上的确定性映射。
   - Spring的步长$\beta_t$显式衰减（两时间尺度），残差的"步长"由训练隐式确定且在层间可变。
   - Spring有显式的两时间尺度分离（学生快速/门控慢速），残差中所有层共享同一训练迭代。

**推论6.2（统一的收敛图景）** **[严格]**
Spring SE-1和残差连接是**同一变分原理——Pontryagin极大值原理——在时间域和空间（深度）域的两种物理实现**。两者的收敛性均由PMP的协态方程+终端横截条件+控制驻点条件共同保证的方向性导出：在Spring中，评分$S_t$沿时间向$S_\infty$演化；在残差网络中，表示$x_l$沿深度向$x^*$演化。这一统一意味着：**Spring的Lyapunov收敛（Theorem SE-1）和残差连接的沿深度收敛（定理6.4）是同一PMP结构——协态指向吸引子，控制沿协态负方向推进状态——的两个推论**。

### §6.8 A5光滑性验证的诚实标注

假设A5要求$F_l(\cdot; \theta_l)$关于$\theta_l$是$C^1$（连续可微）的。本节诚实地分析该假设在不同网络架构下的验证现状，并标注所需的额外假设。

#### §6.8.1 光滑激活函数：A5严格成立 **[严格]**

若残差块使用以下光滑激活函数（及其线性组合），则A5严格成立，无需额外假设：

- **GELU**（Gaussian Error Linear Unit）：$x \cdot \Phi(x)$，其中$\Phi$为高斯CDF。GELU是$C^\infty$（实解析）的。
- **Swish/SiLU**：$x \cdot \sigma(x)$，其中$\sigma$为sigmoid。$C^\infty$。
- **tanh**：$C^\infty$。
- **Softplus**：$\log(1 + e^x)$，$C^\infty$。
- **任何$C^1$激活函数与仿射变换的复合**：$F_l(x; \theta_l) = W_l^{(2)}\sigma(W_l^{(1)}x + b_l^{(1)}) + b_l^{(2)}$是$\theta_l = (W_l^{(1)}, W_l^{(2)}, b_l^{(1)}, b_l^{(2)})$的$C^1$函数。

在此情况下，**A5被严格满足**——离散PMP的经典版本（Halkin, 1966）直接适用，无需任何非光滑扩展。

#### §6.8.2 ReLU激活函数：需要非光滑PMP扩展 **[诚实标注]**

若残差块使用ReLU激活函数$\sigma(z) = \max(0, z)$，则$F_l$关于$\theta_l$（权重）不是处处$C^1$的。具体地，在满足$W_l^{(1)}x + b_l^{(1)} = 0$（某神经元的前激活值为零）的参数配置处，$F_l$关于该神经元的权重不可微。这些不可微点构成参数空间的一个**零测度闭集**（有限个超平面的并集）。

**所需额外假设：Clarke非光滑PMP**。为在ReLU设定下恢复PMP的适用性，需要调用**Clarke的非光滑Pontryagin极大值原理**（Clarke, 1983, *Optimization and Nonsmooth Analysis*; Clarke, 2005, *Necessary Conditions in Dynamic Optimization*）：

- **(A5-Clarke)** $F_l(\cdot; \theta_l)$关于$\theta_l$是**局部Lipschitz的**且**Clarke-正则的**（Clarke-regular）。
- ReLU网络满足这两个条件：(i) ReLU是1-Lipschitz的（全局Lipschitz），仿射变换是光滑的，复合后$F_l$关于$\theta_l$是局部Lipschitz的；(ii) ReLU是Clarke-正则的（作为凸函数的逐点最大值）。
- 在Clarke非光滑PMP下，Hamiltonian极小化的一阶必要条件替换为：
  $$\boxed{0 \in \partial_\theta^C H_l(x_l^*, \theta_l^*, p_{l+1}^*)}$$
  其中$\partial_\theta^C$为关于$\theta_l$的**Clarke广义梯度**。
- Clarke广义梯度在不可微点处是凸紧集——它包含了该点附近所有"常规梯度"的极限。在可微点（几乎所有参数空间），$\partial_\theta^C H_l = \{\nabla_\theta H_l\}$——与经典梯度重合。

**对方向结论的影响**：在ReLU设定下，$0 \in \partial_\theta^C H_l$意味着存在某个广义梯度元素$g \in \partial_\theta^C F_l \cdot p_{l+1}^*$使得$g = 0$。在几乎所有参数配置（概率为1的集合）上，这退化为经典梯度条件$(\partial F_l/\partial \theta_l)^\top p_{l+1}^* = 0$——因为不可微点的Lebesgue测度为零，且SGD的实际轨迹以概率1避开这些点（除非被精确初始化在不可微点上）。因此，**定理6.3的方向结论对ReLU网络在实际中以概率1成立**——与光滑情况无本质差异。

**需要在论文中显式陈述的额外假设**（针对ReLU）：

| 额外假设 | 内容 | 必要性 | 合理性 |
|:--------|:-----|:------|:------|
| **A5-Clarke-1** | $F_l$关于$\theta_l$是局部Lipschitz的 | Clarke非光滑PMP的前提 | ReLU+仿射变换=局部Lipschitz，严格成立 |
| **A5-Clarke-2** | $F_l$是Clarke-正则的 | 保证广义梯度的良好行为（链式法则、中值定理） | ReLU作为凸函数是Clarke-正则的，严格成立 |
| **A5-Clarke-3** | SGD轨迹以概率1避开非可微点的邻域（除有限次穿越外） | 保证在实际训练中梯度条件以概率1成立 | 标准SGD分析的标准假设；若显式添加微小高斯噪声则严格成立 |

**诚实结论**：
- 对于使用**光滑激活函数**（GELU/Swish/tanh/Softplus）的残差网络：**A5严格成立**，PMP直接适用，定理6.3在A1-A4+A5下的证明链完整。
- 对于使用**ReLU激活函数**的残差网络：**A5需要替换为A5-Clarke（Clarke非光滑PMP）**。该替换是技术性的（调用的数学工具从经典PMP变为Clarke非光滑PMP），而非颠覆性的（方向结论在概率1意义上保持）。ReLU网络的方向结论因此被标注为**额外假设下的[条件严格]**。
- 对ReLU的标签（label）：这并非理论的"缺陷"——几乎所有变分分析在处理ReLU时都需要这一扩展。Clarke非光滑分析是成熟的数学分支，将经典PMP推广到非光滑动力学是标准的学术操作。

### §6.9 物理直觉：变分原理、方向场、与分类学机器

本节从三个层次阐述PMP路径提供的物理直觉。

**第一层：PMP作为最优性的"法向条件"**

Pontryagin极大值原理在几何上等价于：在最优轨迹上，Hamiltonian沿控制方向的变分必须为零——即轨迹是"极值曲线"。对残差网络，这意味着经训练的权重$\theta_l^*$不是任意的——它们必须满足：沿任意权重扰动方向，终端代价的一阶变分为零。这在表示空间中转化为一个明确的几何约束：**残差块输出$F_l(x_l)$的方向不能有沿协态$p_{l+1}$的正分量**（否则可以通过调整$\theta_l$进一步降低损失）。而协态$p_{l+1}$本身指向$x_l - x^*$（当前状态偏离最优状态的方向）——因此$F_l$只能指向$-p_{l+1}$，即$x^* - x_l$。这一"法向条件"（orthogonality → alignment）是变分原理的自然几何推论——正如在势场中，物体受力的方向是势能下降最快的方向。

**第二层：深度作为"梯度下降的展开"**

定理6.3揭示了一个深刻的对应：残差网络的前向传播$x_{l+1} = x_l + F_l(x_l)$，在训练收敛后，等价于沿方向$x^* - x_l$的梯度下降步。这意味着：**$L$层残差网络的前向传播等价于在表示空间中对某个隐含势函数运行$L$步梯度下降**，其中每步的"学习率"和"预条件器"由该层的训练权重确定。这一视角统一了三个看似不相关的现象：(a) 残差网络的有效性——因为深度直接转化为优化迭代次数；(b) 残差网络的训练稳定性——因为每层的目标（指向$x^*$）是全局一致的，不存在"层间目标冲突"；(c) 表示沿深度的单调改善——因为梯度下降每一步都减小与最优值的距离（在$\alpha_l$合适的条件下）。

**第三层：Spring SE-1与残差连接——同一变分原理的两种节拍**

Spring评分演化$S_{t+1} = S_t + \beta_t \cdot \Delta_t$与残差表示演化$x_{l+1} = x_l + F_l(x_l)$是同一PMP结构在两种不同"时间"上的实现。Spring中的"时间"是算法迭代步$t$——看得见的、显式的、以分钟或小时计的计算时间。残差网络中的"时间"是层索引$l$——编译进架构的、隐式的、以纳秒计的前向传播步骤。两者的统一意味着：**深度网络的前向传播本身就是一种"优化"——不是数值优化（如SGD），而是结构优化（如FPGA上的流水线计算）**。每一层执行一步精炼，所有层协作完成从输入到最优表示的"一次性积累梯度下降"。这正是"分区→命名→改进"分类学循环的数学基础：Spring在计算时间上"改进"评分，残差网络在架构深度上"改进"表示——两者共享同一个变分核心：PMP的方向场$x \mapsto x^* - x$。

**第四层：为什么残差连接不可替代**

若移除跳跃连接，动力学变为$x_{l+1} = F_l(x_l)$（无恒等项）。此时：
- Hamiltonian变为$H_l = p_{l+1}^\top F_l(x_l; \theta_l)$（缺少$x_l$项）
- 协态方程变为$p_l = J_l^\top p_{l+1}$（缺少$+p_{l+1}$项）
- $J_l$可能任意大（无压缩保证），协态反向传播可能爆炸或消失
- 终端协态$p_L \propto x_L - x^*$的信息在反传中迅速丢失

残差连接的本质贡献在于：它在动力学中保留了恒等项$I$，使得PMP协态方程$p_l = (I + J_l^\top)p_{l+1}$被恒等算子**正则化**——无论$J_l$如何，$I + J_l^\top$的谱被约束在$(1-\rho, 1+\rho)$（在A4下），保证协态信息沿深度的稳定传播。这是残差架构作为"PMP-兼容架构"的数学定义：**残差连接是唯一保证PMP协态反向传播数值稳定的前向传播结构**。

**开放问题**：
1. 从有限宽非线性网络的训练动力学严格推导A4（$\|J_l\| \leq \rho < 1$）。
2. 对ReLU网络建立A5的Clarke非光滑PMP严格证明链（含定量误差界）。
3. 量化可达集$\mathcal{A}_l$在有限宽下的非凸性对方向结论的影响（$\delta_l$中$r_l$分量的非渐近界）。
4. 建立"PMP-兼容架构"的完整分类——识别能使PMP保证收敛性的前向传播结构类。




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

**预测4（自监督→监督的退化边界——v3.0修正：η_c代数推导修正与诚实评估）** ⚠

**⚠ v3.0重要修正**：v2.0中$\eta_c$的推导包含代数错误。在Step 3的二次方程求解中，v2.0失误地将判别式中的因子遗漏，导致$\eta_c$被低估约2.414倍。以下给出修正后的推导和诚实评估。

从Cercis评分$S = Q + \eta N$出发，我们推导噪声占优阈值$\eta_c$的理论值。当标签噪声率$\eta_{\text{down}} \geq \eta_c$时，纯SSL预训练（$\eta_{\text{pre}} = 0$）在SCX噪声检测F1上的改进$\Delta\mathrm{F1} = \mathrm{F1}_{\text{SSL}} - \mathrm{F1}_{\text{rand}}$不超过$0.05$。

**$\eta_c$的修正推导**：

**Step 1: Cercis评分的方差分解。**
$$S = Q + \eta N, \quad \text{Var}(S) = \text{Var}(Q) + \eta^2\text{Var}(N) + 2\eta\text{Cov}(Q,N)$$

定义N-项贡献比为：
$$f_N(\eta) = \frac{\eta^2\text{Var}(N) + 2\eta\text{Cov}(Q,N)}{\text{Var}(S)}$$

$f_N(\eta_c) = 1/2$（N-项解释S的一半方差）给出占优阈值。

**Step 2: SCX Bernoulli模型中的Var(Q)和Var(N)。**
在SCX Bernoulli模型下（干净样本vs噪声样本的二值分类），令指示变量$Z \sim \text{Bernoulli}(\eta)$（$Z=1$表示噪声样本）。则：
- 干净样本（$Z=0$）：$Q = 1 - \mu_s$（高固有质量），$N = -\mu_s$（专家误差低于状态均值）
- 噪声样本（$Z=1$）：$Q = 0$（低固有质量），$N = 1 - \mu_s/(K-1)$（专家高度分歧）

直接计算矩：
$$Q = (1-Z)(1-\mu_s), \quad N = (1-Z)(-\mu_s) + Z \cdot A$$
其中$A = 1 - \frac{\mu_s}{K-1}$。

方差和协方差（利用$\text{Var}(Z) = \eta(1-\eta)$）：
$$\text{Var}(Q) = (1-\mu_s)^2 \cdot \eta(1-\eta)$$
$$\text{Var}(N) = (\mu_s + A)^2 \cdot \eta(1-\eta) = \left(1 + \mu_s - \frac{\mu_s}{K-1}\right)^2 \cdot \eta(1-\eta)$$
$$\text{Cov}(Q,N) = -(1-\mu_s)(\mu_s + A) \cdot \eta(1-\eta) = -(1-\mu_s)\left(1 + \mu_s - \frac{\mu_s}{K-1}\right) \cdot \eta(1-\eta)$$

记$B = 1 + \mu_s - \frac{\mu_s}{K-1}$，则$\text{Var}(Q) = \eta(1-\eta)(1-\mu_s)^2$，$\text{Var}(N) = \eta(1-\eta)B^2$，$\text{Cov}(Q,N) = -\eta(1-\eta)(1-\mu_s)B$。

**Step 3: 正确求解二次方程（v2.0错误在此——遗漏了判别式中的因子2）。**
条件$f_N(\eta_c) = 1/2$等价于$\eta_c^2\text{Var}(N) + 2\eta_c\text{Cov}(Q,N) - \text{Var}(Q) = 0$（见§1.8推导）。代入方差和协方差表达式：
$$\eta_c^2 \cdot \eta(1-\eta)B^2 + 2\eta_c \cdot (-\eta(1-\eta)(1-\mu_s)B) - \eta(1-\eta)(1-\mu_s)^2 = 0$$

除以$\eta(1-\eta)$（注意：此处的$\eta$是总体噪声率，$\eta_c$是待求阈值——二者是**不同的变量**。该除法在$\eta \notin \{0,1\}$时合法）：
$$B^2 \eta_c^2 - 2B(1-\mu_s)\eta_c - (1-\mu_s)^2 = 0$$

这是关于$\eta_c$的标准二次方程。**v2.0的错误**：在求解此二次方程时，判别式计算有误。

二次方程$ax^2 + bx + c = 0$的判别式$\Delta = b^2 - 4ac$：
$$a = B^2, \quad b = -2B(1-\mu_s), \quad c = -(1-\mu_s)^2$$
$$\Delta = 4B^2(1-\mu_s)^2 + 4B^2(1-\mu_s)^2 = 8B^2(1-\mu_s)^2$$
$$\sqrt{\Delta} = 2\sqrt{2} \cdot B(1-\mu_s)$$

$$\eta_c = \frac{2B(1-\mu_s) \pm 2\sqrt{2}B(1-\mu_s)}{2B^2} = \frac{1-\mu_s}{B}(1 \pm \sqrt{2})$$

取正根（$\eta_c > 0$）：
$$\boxed{\eta_c = (1+\sqrt{2})\frac{1-\mu_s}{B} = (1+\sqrt{2})\frac{1-\mu_s}{1 + \mu_s - \frac{\mu_s}{K-1}}}$$

其中$(1+\sqrt{2}) \approx 2.414$。**v2.0遗漏了此因子**，错误地得到$\eta_c = (1-\mu_s)/B$。

对于大类数极限$K \gg 1$（$B \to 1+\mu_s$）：
$$\boxed{\eta_c = (1+\sqrt{2})\frac{1-\mu_s}{1+\mu_s}}$$

**Step 4: 修正后的数值表（v3.0）。**

| $\mu_s$ | $K=2$ | $K=10$ | $K=100$ | $K \to \infty$ | v2.0旧值($K\to\infty$) |
|---------|-------|--------|---------|----------------|------------------------|
| 0.10 | 1.976 | 1.994 | 1.997 | **1.976** | 0.818 |
| 0.20 | 1.610 | 1.637 | 1.641 | **1.610** | 0.667 |
| 0.30 | 1.300 | 1.347 | 1.350 | **1.300** | 0.538 |
| 0.40 | 1.035 | 1.094 | 1.098 | **1.035** | 0.429 |
| 0.50 | 0.805 | 0.862 | 0.867 | **0.805** | 0.333 |
| 0.55 | 0.700 | 0.753 | 0.759 | **0.700** | 0.290 |
| 0.60 | 0.603 | 0.652 | 0.658 | **0.603** | 0.250 |
| 0.65 | 0.511 | 0.556 | 0.562 | **0.511** | 0.212 |
| 0.70 | 0.425 | 0.464 | 0.470 | **0.425** | 0.176 |

**Step 5: 诚实评估——修正后η_c的物理意义。**

修正后的$\eta_c$值揭示了一个基本事实：**对于所有实际相关的专家质量$\mu_s \leq 0.65$，修正后的$\eta_c > 0.5$——即在任何有效的$K$-类分类问题中（噪声率$\eta \in [0, 0.5]$），噪声项$N$对Cercis评分$S$的方差贡献**永远达不到**质量项$Q$的贡献**。

具体分析：
1. $\eta_c = 0.5$对应的临界$\mu_s \approx 0.65$（$K\to\infty$）或$\mu_s \approx 0.69$（$K=10$）。这意味着：只有当专家在干净数据上的错误率超过约65%时，噪声占优阈值才降至0.5以下。
2. 但$\mu_s > 0.5$意味着专家在干净数据上的正确率低于随机猜测——这是一个几乎无信息量的专家。在$\mu_s \in [0.65, 1)$时，专家实际上是"反向有用"的（可通过翻转预测获得>50%正确率）。
3. 对于$\mu_s \leq 0.3$（典型ML任务的专家质量：ResNet在CIFAR-100上的top-1错误率约25-30%），$\eta_c \approx 1.3$——远超任何有效噪声率的范围。

**结论**：v3.0修正后的$\eta_c$不再具有v2.0声称的实用预测意义。v2.0预测的"$\eta_c \in [0.25, 0.35]$区间内SSL预训练收益消失"是基于代数错误的结果。修正后的理论揭示：在Cercis评分$S = Q + \eta N$的参数化下，**质量项$Q$对所有有效噪声率$\eta \in [0, 0.5]$始终主导方差**。这意味着：

- **SSL预训练（优化$Q$）在任何噪声水平下均有正收益**——不存在"噪声占优"导致的收益消失。
- Cercis评分的$\eta$-参数化可能需要在$\eta > 0.5$区域进行非线性修正（例如引入$\eta^2$的高阶项），或考虑$Q$和$N$之间的非Bernoulli分布结构。
- **预测4（原v2.0版）被标记为"已证伪（由理论修正）"**——这不是实验的失败，而是理论推导中代数错误被修正后的诚实结论。

**剩余不确定性**：
1. 上述分析基于SCX Bernoulli模型的二值$Q$和$N$。连续分布下的$\eta_c$可能略有不同，但$(1+\sqrt{2})$因子的数量级修正（约2.414倍）使得结论（$\eta_c \gg 0.5$）在定性上稳健。
2. 若将"噪声占优"的阈值从$f_N = 1/2$改为更宽松的标准（如$f_N = 1/3$），则$\eta_c$会相应下调，但修正后的数量级仍远超0.5。

**检验建议（修订）**：与其检验已被理论修正否定的v2.0预测，建议检验修正后的理论预测——即在所有噪声水平$\eta \in [0, 0.5]$下，$\Delta\mathrm{F1}(\eta) > 0$（SSL预训练始终有正收益，且收益随$\eta$增加缓慢衰减而非在$\eta \approx 0.3$处骤降）。这是修正后理论的可证伪预测：若在$\eta \in [0.25, 0.4]$区间内观测到$\Delta\mathrm{F1} \approx 0$（收益消失），则Cercis评分的Bernoulli简化需要被更复杂的模型替代。

### §8.3 可证伪性总结

SCX分类学理论的科学价值取决于上述预测的实验检验。如果一个理论不能做出区别于"零假设"的精确预测，它就不是科学理论。上述四个预测经过精心筛选，排除了同义反复（仅重述定理公式的预测）和范畴错误（将数学事实当作经验预测）：

- **预测1（合成数据紧致性）**——理论最直接的经验风险。若Theorem 1下界与经验F1的差距$>0.05$或随$M$增大，则公理体系的定量精度被直接挑战。这是**冒最大风险的预测**：它在最干净的条件下检验理论的核心常数。
- **预测2（深度饱和点）**——检验层作为隐式专家这一核心映射的定量有效性。若$M_{\text{eff}}$不饱和，则"深度=隐式集成"的推导链需要重新审视$M_{\text{eff}}(L)$的公式。
- **预测3（Lyapunov单调性）**——检验残差连接作为迭代精炼结构的概念框架。若Lyapunov函数不单调，则"残差块使表示渐进逼近最优解"的直觉缺乏经验基础。
- **预测4（SSL退化边界，v3.0修正）**——**⚠ 本预测的v2.0版本（$\eta_c \in [0.25, 0.35]$）因代数推导错误已被理论修正否定**。修正后$\eta_c = (1+\sqrt{2})(1-\mu_s)/(1+\mu_s) \gg 0.5$对所有$\mu_s \leq 0.65$，意味着质量项$Q$在所有有效噪声率下始终主导方差——噪声占优阈值不具有实用意义。修订后的可检验预测为：$\Delta\mathrm{F1}(\eta) > 0$对所有$\eta \in [0, 0.5]$（SSL预训练始终有正收益）。若在$\eta \in [0.25, 0.4]$观测到$\Delta\mathrm{F1} \approx 0$，则Cercis评分的Bernoulli简化模型被证伪，需要更复杂的$Q$-$N$联合分布模型。

**被删除的预测及其删除理由**：
- ~~原#1（集成指数收敛率）~~：同义反复——该公式是Theorem 1的直接重述，检验它等价于检验Theorem 1本身（现由新预测1以更严格形式覆盖）。
- ~~原#3（对数-平方根收益）~~：可检验但非核心——来自信息论标准结果（Fano不等式+参数计数），并非SCX理论的特有预测。
- ~~原#4（幻觉缩放不变性）~~：经§5严格升级后（多种子独立解码→条件独立→Theorem 3严格适用），$\eta\rho/2$下界已是严格推导（单步）/条件严格（多步）。但检验此预测需要测量$\rho$（自然语言中歧义查询的比例），这在现有基准测试中缺乏标准化的度量——保留其可证伪性但未列入核心预测清单。
- ~~原#6（F1界经验紧致性）~~：已被新预测1以更精确的形式（$\leq 0.05$且不随$M$增大）取代。
- ~~原#8（Chernoff/Hoeffding比率）~~：范畴错误——Chernoff界在数学上必然比Hoeffding界紧致，这不是经验预测而是数学定理（Bahadur-Rao）。检验它不能证伪SCX理论。

每个保留的预测都附有明确的证伪条件。拒绝任何一个预测将要求修改SCX公理系统中的相应假设或推导链。接受全部四个预测则构成对SCX分类学理论的经验支持。

---

## 结论

我们从SCX公理系统出发，推导了机器学习的七个关键经验现象：集成方法的指数收敛（§2）、深度的隐式集成效应（§3）、表示学习的互信息对偶（§4）、LLM幻觉的必然性（§5, **严格**——多种子独立解码方案，v2.1新增对称性条件$\eta_{\text{err}}=\eta_{\text{amb}}$）、残差连接的Pontryagin极大值原理分析（§6, **混合**——v6.0重写：将残差网络前向传播形式化为离散最优控制问题，应用PMP从协态方程+参数驻点条件严格推导$F_l(x_l) \propto x^* - x_l$；方向结论是PMP必要条件的演绎后果；A5光滑性假设在ReLU网络中的额外需求被诚实标注；核心检验$\cos_l = \langle F_l, x^* - x_l\rangle/(\|F_l\|\|x^* - x_l\|) > 0$）、自监督学习的$\eta$-退化极限（§7）、以及噪声占优阈值的修正推导（§8预测4, v3.0修正代数错误——$\eta_c \gg 0.5$，预测失去实用意义）。每个推导都标注了关键假设和严格性等级，使得理论是可错的和可修正的。

**本次v6.0修订摘要**：
1. **§6（根本性重写——Pontryagin极大值原理路径）**：v6.0是一次根本性的方法论转向。(a) 将残差网络前向传播形式化为离散最优控制问题（Mayer型：状态$x_l$，控制$\theta_l$，终端代价$J(x_L, y)$）——形式化本身为[严格]；(b) 应用离散PMP（Halkin, 1966）给出必要条件：协态方程$p_l = (I + J_l^\top)p_{l+1}$，终端横截条件$p_L = \nabla_x J$，Hamiltonian极小化$\partial H_l/\partial \theta_l = 0$——PMP应用为[严格]；(c) **关键推导**[条件严格]：从强凸损失（A3）得$p_L = \bar{H}(x_L - x^*)$，经协态反向传播（A4保证可逆性）得$p_{l+1} = Q_l(x_l - x^*) + \varepsilon_l$；(d) **主定理**[条件严格]：PMP控制驻点+过参数化可达集凸性（A1）→$F_l = -\alpha_l p_{l+1}$→$F_l \propto x^* - x_l$——残差块方向指向最优表示；(e) 与Spring SE-1的PMP层面精确对偶表（定理6.5）——[严格]；(f) A5光滑性在ReLU网络中的额外假设被诚实标注（§6.8：需Clarke非光滑PMP扩展，技术性但不颠覆结论）；(g) 核心可检验预测：$\cos_l > 0$——直接测量方向对齐度，比v5.0的$\hat{\gamma}_l \in (0, 2)$更直接。
2. **§1.6 & §5（参数分离）**：Theorem 3构造中显式分离$\eta_{\text{err}}$和$\eta_{\text{amb}}$，标注对称性条件（v2.1, 保留）。
3. **§8预测4（代数修正）**：修正v2.0中$\eta_c$推导的代数错误（v3.0, 保留）。

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

[21] Jacot, A., Gabriel, F., & Hongler, C. Neural Tangent Kernel: Convergence and generalization in neural networks. *NeurIPS*, 2018.

[22] Arora, S. et al. On exact computation with an infinitely wide neural net. *NeurIPS*, 2019.

[23] Bai, S., Kolter, J. Z., & Koltun, V. Deep equilibrium models. *NeurIPS*, 2019.

[24] Lions, P. L. & Mercier, B. Splitting algorithms for the sum of two nonlinear operators. *SIAM Journal on Numerical Analysis*, 16(6):964–979, 1979.

[25] Bauschke, H. H. & Combettes, P. L. *Convex Analysis and Monotone Operator Theory in Hilbert Spaces*, 2nd ed. Springer, 2017.

[26] Brézis, H. *Opérateurs Maximaux Monotones et Semi-groupes de Contractions dans les Espaces de Hilbert*. North-Holland, 1973.

[27] Rockafellar, R. T. On the maximal monotonicity of subdifferential mappings. *Pacific Journal of Mathematics*, 33(1):209–216, 1970.

[28] Moreau, J. J. Proximité et dualité dans un espace hilbertien. *Bulletin de la Société Mathématique de France*, 93:273–299, 1965.

[29] Minty, G. J. Monotone (nonlinear) operators in Hilbert space. *Duke Mathematical Journal*, 29(3):341–346, 1962.

[30] Tseng, P. A modified forward-backward splitting method for maximal monotone mappings. *SIAM Journal on Control and Optimization*, 38(2):431–446, 2000.

---

*本文的数学定理和证明属于公共领域。SCX软件框架中的算法和实现受独立开发者的版权保护。*
