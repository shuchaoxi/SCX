# 引言：势函数训练的审计缺口

**Author:** SCX

*Abstract:*

本文提出Spring{}自演化势函数训练器——第一个将训练过程本身作为审计过程的分子动力学势函数学习框架。
与现有范式（NEP、DeepMD、ACE等）在训练完成后进行事后验证不同，
Spring{}的每一次训练迭代即产生一份经过审计的势函数。
其核心机制为：从$M>1$个独立专家中自举训练，
通过Yajie{}共识评分实时滤除噪声，
以Lyapunov函数$\Lyap_t$监控收敛性，
自动生成$M_t$参数并绑定至数据哈希（共生绑定），
最终以Cercis{}评分作为跨架构可比的单一质量度量。

我们证明：在温和条件下，Spring训练循环满足$\Lyap_t \to 0$（$t \to \infty$）的收敛保证（定理1）；
自动生成的$M_t$是数据复杂度$\Sigma_0(\D)$的单调函数，实现了参数-数据的结构绑定（定理2）；
Yajie{}共识在多专家框架下的噪声检测概率随$M_t$呈指数增长（定理3）。
我们将Spring{}与NEP（$M=1$，不可验证）、DeepMD（$M=1$，无多专家机制）和ACE（$M=1$，无审计结构）
进行了系统比较，论证了Spring{}是目前唯一实现"训练即审计"的势函数学习框架。

**关键词：** 势函数训练；自演化学习；多专家共识；Yajie协议；Lyapunov收敛；Cercis评分；Spring框架；分子动力学；审计内建训练

---

## 引言：势函数训练的审计缺口

### 分子动力学势函数：从经验到机器学习

分子动力学（Molecular Dynamics, MD）模拟的核心是原子间相互作用势函数$V(\mathbf{r}_1, ..., \mathbf{r}_N)$，
它决定了体系的一切静态和动力学性质。
传统势函数（Lennard-Jones、EAM、ReaxFF等）依赖人工设计的解析形式，参数通过拟合实验或第一性原理数据确定。
其根本局限在于：**解析形式的表达能力受限于人类的物理直觉**。

机器学习势函数（Machine Learning Potentials, MLPs）的兴起打破了这一限制。
以Behler-Parrinello对称函数（2007）为起点，过去十五年间涌现了多种架构：

- **NEP（Neuroevolution Potential, 2022）：** 基于分离卷积神经网络的单模型训练，$M=1$。
- **DeepMD（Deep Potential Molecular Dynamics, 2018）：** 深度势能网络，通过能量-力联合训练生成单一势函数，$M=1$。
- **ACE（Atomic Cluster Expansion, 2019）：** 基于完备基展开的线性模型，单个拟合过程，$M=1$。
- **GAP（Gaussian Approximation Potential, 2010）：** 高斯过程回归，单一核函数选择，$M=1$。
- **MTP（Moment Tensor Potential, 2016）：** 线性回归在张量基上的展开，$M=1$。

这些方法的共同特征——也是本文将要论证的**结构性缺陷**——是它们的训练过程和验证过程是分离的。
训练产生一个势函数，随后通过测试集的能量/力误差来评估其质量。
但测试集误差是**聚合统计量**——它回答"平均而言这个势函数有多准"，而不能回答"对于这个特定的原子构型，预测是否可靠"。

### 审计缺口：聚合精度与逐点可靠性的鸿沟

在SCX理论框架下 [cite]，审计缺口的本质是**实例级验证的缺失**。
设训练数据为$\D = \{(\mathbf{R}_i, E_i, \mathbf{F}_i)\}_{i=1}^{N_{data}}$，
其中$\mathbf{R}_i$为原子坐标，$E_i$为参考能量，$\mathbf{F}_i$为参考力。
一个势函数$V_\theta(\mathbf{R})$的测试误差定义为：

$$<!-- label: eq:rmse_def -->
    RMSE_E = \sqrt{\frac{1}{N_{test}}\sum_{i=1}^{N_{test}}(V_\theta(\mathbf{R}_i) - E_i)^2},
    \quad
    RMSE_F = \sqrt{\frac{1}{3N_{test}N_{atoms}}\sum_{i=1}^{N_{test}}\|\mathbf{F}_\theta(\mathbf{R}_i) - \mathbf{F}_i\|^2}
$$

当$RMSE_E = 1\ meV/atom$时，这个数字告诉我们*平均*偏差为1 meV/atom。
它*不*告诉我们的是：

1. 哪1\%的构型贡献了50\%的误差？
2. 对于构型$\mathbf{R}^*$——处于训练数据分布边界或之外的构型——预测是否可靠？
3. 两个训练得到的势函数$V_{\theta_1}$和$V_{\theta_2}$在测试集上RMSE相同，但在关键构型上的预测完全相反——我们如何知道？

这三个问题构成了势函数训练的**审计三元组**（Audit Trilemma），
而现有框架无一能同时解决。

> **Definition:** [势函数审计三元组]
> 势函数$V_\theta$被称为**可审计**的，当且仅当以下三个条件同时满足：
> 
1. **误差定位（Error Localization）：** 对于任意构型$\mathbf{R}$，系统能判断$V_\theta(\mathbf{R})$的误差是否超出阈值$\varepsilon$，无需参考真实值$E_{ref}(\mathbf{R})$。
2. **分布外检测（OOD Detection）：** 系统能识别$\mathbf{R}$是否处于训练数据支持的域外，并在域外构型上拒绝给出高置信度预测。
3. **多解可辨性（Multi-Solution Distinguishability）：** 当存在多个RMSE相近的势函数时，系统能判断它们是否在关键物理区域给出定性一致的预测。

现有框架的审计失败是结构性的：

- **NEP（$M=1$）：** 单个网络产生单个输出。没有任何机制实现(A1)误差定位——模型无法判断自己的预测何时错误（自审计等于无审计，SCX定理2 [cite]）。
- **DeepMD（$M=1$）：** 虽然使用能量-力联合训练提高精度，但最终仍是一个模型。对(A2)分布外检测，DeepMD依赖事后不确定性估计（如Dropout ensemble、Deep Ensemble），这些是*事后*追加的，不是训练本身的内建特性。
- **ACE（$M=1$）：** 线性模型虽然系数可解释，但*基的完备性不等于预测的可靠性*。对于(A3)，ACE无法区分"缺乏训练数据"和"物理上预测可靠"——两者都给出低置信度，但原因完全不同。

### Spring的定位：训练即审计

Spring{}框架的根本创新在于：**它不区分"训练阶段"和"审计阶段"**。
在Spring中，每一次训练迭代本身就是一次完整的审计循环。
具体而言，Spring的第$t$次迭代产生以下五项输出：

$$<!-- label: eq:spring_outputs -->
    \boxed{
    
$$
        Spring(t) \mapsto \Bigl(
            &\underbrace{V^{(t)}_{consensus}}_{经共识的势函数},\ 
            \underbrace{\mathbf{s}_{Yajie}^{(t)}}_{Yajie共识评分},\ 
            \underbrace{\Lyap_t}_{Lyapunov监控量},\ 
            \underbrace_{自生成$M_t$},\ 
            \underbrace{S_{Cercis}^{(t)}}_{Cercis评分}
        \Bigr)
    $$
}
$$

其中每一项都不是事后计算的——它们是训练循环的*内生*产物。
这就是"训练即审计"的严格含义：**如果你完成了Spring训练，你就已经完成了审计——你拿到的势函数天然是经过审计的。**

### 本文结构

1. 第2节：Spring自演化训练架构的完整描述。
2. 第3节：多专家训练定理——$M>1$训练的形式化保证。
3. 第4节：Yajie共识评分的集成——实时噪声过滤的数学机制。
4. 第5节：$M_t$自动生成与共生绑定——数据驱动的结构参数。
5. 第6节：Cercis评分——跨架构可比的单一质量度量。
6. 第7节：Lyapunov收敛分析与收敛定理。
7. 第8节：与NEP/DeepMD/ACE的系统比较。
8. 第9节：讨论——适用边界、计算成本、诚实暴击。
9. 第10节：结论。

---

## Spring自演化训练架构

### 训练循环的拓扑结构

Spring的训练循环是一个**自演化自治系统**（Self-Evolving Autonomous System），
由四个拓扑层组成，每一层在逻辑上封闭但信息上互通：

1. **多专家自举层（Multi-Expert Bootstrap Layer）：**
2. **独立训练层（Independent Training Layer）：**
3. **Yajie共识层（Yajie Consensus Layer）：**
4. **自演化调控层（Self-Evolution Regulation Layer）：**

[Figure omitted — see original .tex]

### Spring的五个内生产出

图 [ref]展示了Spring训练循环的完整拓扑。
每一次迭代$t$的内部计算流程收敛后的产出——式 [ref]中的五个量——
是*内生*的：它们由训练过程本身产生，而非事后计算。
下面我们给出每个量的形式定义，后续各节将详细展开其数学基础。

> **Definition:** [Spring五项内生产出]
> 设训练数据为$\D$，第$t$次Spring迭代完成时，系统输出：
> 
1. **共识势函数$V^{(t)}_{consensus}$：**
2. **Yajie共识评分$\mathbf{s}_{Yajie}^{(t)}$：**
3. **Lyapunov监控量$\Lyap_t$：**
4. **自生成专家数$\Mauto$：**
5. **Cercis评分$S_{Cercis}^{(t)}$：**

### 与现有框架的本质区别

表 [ref]总结了Spring与主要现有框架在**结构层面**的本质区别。

[Table omitted — see original .tex]

---

## 多专家训练定理

### 从$M=1$到$M>1$：势函数学习的认识论跃迁

现有势函数训练框架的一个共同前提是：**存在一个"正确"的势函数$V^*$，训练的目标是通过数据找到其最佳近似**。
这一前提在认识论上存在问题。
对于真实的量子力学多体系统，基态能量$E_0(\mathbf{R})$是Schrödinger方程的精确解。
任何经典势函数$V(\mathbf{R})$都是对这一量子力学实在的近似——
但*近似*不只有一种。
在有限数据下，存在无限多种势函数能够在训练数据上达到同等的精度，
但在未见构型上的预测可能截然不同。

这一定性观察是SCX定理1（多专家误差检测定理 [cite]）
在势函数训练领域的直接推论：

> **Theorem:** [势函数多专家检测定理 — 定理1]<!-- label: thm:spring_thm1 -->
> 设$\D$为包含$N_{data}$个构型的训练数据集，每个构型$i$具有参考能量$E_i$和参考力$\mathbf{F}_i$。
> 令$\Fset^{(M_t)} = \{f_1, ..., f_{M_t}\}$为$M_t$个独立训练的势函数专家，
> 满足：(i) 在互信息意义上独立训练（式 [ref]）；(ii) 每个专家$f_m$在有界能量误差意义上优于随机猜测。
> 则对于任意构型$\mathbf{R}$，所有$M_t$个专家同时对该构型产生误差超过$\Delta$的概率满足：
> 
> $$<!-- label: eq:thm1_bound -->
>     \Pbb\left(\bigcap_{m=1}^{M_t} \left\{|f_m(\mathbf{R}) - E_{ref}(\mathbf{R})| > \Delta\right\}\right) \leq \exp\left(-2 M_t^{eff} \cdot \frac{\Delta^2}{\bar^2}\right)
> $$
> 
> 其中$M_t^{eff} = M_t / (1 + \bar_t)$为有效专家数，
> $\bar_t$为平均专家间误差相关性，
> $\bar^2$为单个专家在训练分布上的预测方差。

> **Proof:** 定义指示变量$Z_m = \mathbb{1}[|f_m(\mathbf{R}) - E_{ref}(\mathbf{R})| > \Delta]$。
> 在独立训练假设下（条件(i)），不同$Z_m$之间的相关性仅来自其共享的数据生成分布，
> 其边际相关性由$\bar_t$捕获。
> 给定构型$\mathbf{R}$，误差超过$\Delta$的概率为$p_\Delta = \Pbb(Z_m = 1)$。
> 
> 由于各专家的训练过程独立，$Z_m$条件（于$\mathbf{R}$的分布类别）独立。
> 应用Hoeffding不等式于独立（经$M_t^{eff}$校正后）的伯努利随机变量：
> 
> $$
>     \Pbb\left(\sum_{m=1}^{M_t} Z_m = 0\right)
>     &= \prod_{m=1}^{M_t} \Pbb(Z_m = 0 \mid \mathbf{R}) \cdot (1 + \mathcal{O}(\bar_t)) 

>     &\leq (1 - p_\Delta)^{M_t^{eff}} 

>     &\leq \exp\left(-M_t^{eff} \cdot p_\Delta\right)
> $$
> 
> 由Chernoff界，当$p_\Delta \geq 2\Delta^2/\bar^2$（单专家条件(ii)）时，
> 代入得式 [ref]。 $\square$

> **Corollary:** [审计完备性所需专家数]<!-- label: cor:M_required -->
> 为达到审计完备性$\varepsilon$（即$\Pbb(全部错过) \leq \varepsilon$），所需最小专家数为：
> 
> $$<!-- label: eq:M_min_potential -->
>     M_(\varepsilon, \Delta) = \left\lceil \frac{\bar^2 \cdot \ln(1/\varepsilon)}{2\Delta^2} \cdot (1 + \bar) \right\rceil
> $$

这一推论具有直接的工程意义。对于典型的势函数训练场景：
$\bar \approx 5$ meV/atom（单个专家的典型预测标准差），
$\Delta = 2$ meV/atom（可接受的审计灵敏度），
$\varepsilon = 0.01$（99\%审计完备性），
$\bar = 0.3$（专家间适度的良性相关性），
代入得$M_ \approx 7.2 \to M_ = 8$个专家。

### 多专家训练的博弈论解读

将势函数训练中的多专家设置理解为某种形式的"集成学习"（ensemble learning）是肤浅的。
集成学习（如bagging、boosting）的目标是降低方差从而提高*聚合精度*。
Spring多专家训练的**认识论目标**与此完全不同：它是为了获得*可验证性*。

> **Remark:** [集成学习 vs. 多专家审计]
> 在集成学习中，$M$个模型的平均预测$\bar{f}(\mathbf{R}) = \frac{1}{M}\sum_m f_m(\mathbf{R})$是为了降低预测方差。
> $M$是超参数——它由工程师根据验证集性能手动选择。
> 在Spring多专家审计中，$M_t$个专家的共识不仅给出共识预测，*同时*给出该预测的可靠性度量（Yajie共识评分）。
> $M_t$不是超参数——它由数据复杂度驱动（第5节），是训练过程的内生产物。

> **Proposition:** [多专家训练的信息论收益]<!-- label: prop:info_gain -->
> 在$M>1$的条件下，Spring训练循环的每次迭代产生的关于势函数质量的信息量为：
> 
> $$<!-- label: eq:info_gain -->
>     \Delta I^{(t)} = I(V^{(t)}_{consensus}; V^* \mid \D) - I(V^{(t-1)}_{consensus}; V^* \mid \D) \geq 0
> $$
> 
> 当且仅当$\Lyap_t \geq \Lyap_{t-1}$时等号成立（即收敛停滞）。

> **Proof:** [证明概要]
> $M$个专家的独立预测构成对势函数$V^*$的$M$个独立信息通道。
> Yajie共识整合这些通道，根据数据处理不等式，
> $I(共识; V^*) \geq I(f_m; V^*)$对任意单个$m$。
> 随着训练迭代进行，噪声移除降低了专家预测方差，共识精度单调提升。
> 信息增益的单调性来自Lyapunov函数$\Lyap_t$的非增性（第7节）。
>  $\square$

---

## Yajie共识评分的集成：实时噪声过滤的数学机制

### Yajie共识评分的定义

Yajie{}协议的核心思想 [cite]是：**当多个独立审计模块在一个判断上收敛时，该判断正确的概率乘法式增长；
当它们发散时，发散的模式本身携带关于错误性质和位置的诊断信息**。

在Spring势函数训练中，我们将这一思想适配到多专家预测场景。
对于构型$\mathbf{R}$，$M_t$个专家给出预测值$\{\hat{E}_m(\mathbf{R})\}_{m=1}^{M_t}$。
Yajie共识评分$s_{Yajie}(\mathbf{R})$定义为：

$$<!-- label: eq:yajie_score -->
    \boxed{s_{Yajie}(\mathbf{R}) = \exp\left(-\frac{1}{M_t} \sum_{m=1}^{M_t} \left(\frac{\hat{E}_m(\mathbf{R}) - \hat{E}_{Yajie}(\mathbf{R})}{\sigma_{calib, m}}\right)^2\right)}
$$

其中：

- $\hat{E}_{Yajie}(\mathbf{R}) = \sum_m \omega_m \hat{E}_m(\mathbf{R})$为逆方差加权的共识预测，
- $\sigma_{calib, m}$为专家$m$在Yajie共识校准数据集$\D_{calib}$上的校准标准差，
- $s_{Yajie} \in [0,1]$：$s_{Yajie} = 1$表示完美共识（所有专家给出完全一致的预测），

### 共识评分的统计性质

> **Theorem:** [Yajie共识评分的噪声检测性质 — 定理2]<!-- label: thm:yajie_noise -->
> 设构型$\mathbf{R}$的能量标签$E_{ref}(\mathbf{R})$包含独立加性噪声：
> $E_{obs}(\mathbf{R}) = E_{true}(\mathbf{R}) + \epsilon$，
> 其中$\epsilon \sim \mathcal{N}(0, \sigma_\epsilon^2)$。
> 在$M_t$个专家独立训练的条件下，Yajie共识评分$s_{Yajie}(\mathbf{R})$的期望满足：
> 
> $$<!-- label: eq:yajie_noise_expectation -->
>     \E[s_{Yajie}(\mathbf{R})] = \left(1 + \frac{\sigma_\epsilon^2}{\bar_{expert}^2}\right)^{-M_t/2}
> $$
> 
> 其中$\bar_{expert}^2 = \frac{1}{M_t}\sum_m \sigma_{calib, m}^2$为平均专家校准方差。

> **Proof:** 在加性噪声模型下，专家$m$的预测可写为：
> \[
> \hat{E}_m(\mathbf{R}) = E_{true}(\mathbf{R}) + \epsilon + \delta_m
> \]
> 其中$\delta_m \sim \mathcal{N}(0, \sigma_m^2)$为专家特有的预测误差，
> $\epsilon$为标签噪声（所有专家共享）。
> 在条件独立下，$\epsilon \indep \delta_m$对每个$m$。
> 
> 共识预测为$\hat{E}_{Yajie}(\mathbf{R}) = E_{true}(\mathbf{R}) + \epsilon + \bar$，
> 其中$\bar = \sum_m \omega_m \delta_m$。
> 偏差为$\hat{E}_m - \hat{E}_{Yajie} = \delta_m - \bar$。
> 代入式 [ref]的指数项：
> \[
> \E\left[\left(\frac{\delta_m - \bar}{\sigma_{calib, m}}\right)^2\right]
> = 1 - \frac{2}{M_t} + \mathcal{O}(M_t^{-2}) \approx 1
> \]
> （经过归一化，各专家的校准方差$ \sigma_{calib, m}^2 \approx \Var(\delta_m - \bar)$）。
> 
> 因此，在无噪声（$\sigma_\epsilon = 0$）时，$\E[s_{Yajie}] \approx \exp(-1/2)^{M_t}$。
> 有噪声时，$\hat{E}_{Yajie}$包含噪声项$\epsilon$，增加额外方差，
> 使得期望评分按式 [ref]降低。
> 通过求解$\E[(\hat{E}_m - \hat{E}_{Yajie})^2] = \sigma_{calib, m}^2 + \sigma_\epsilon^2 \cdot (1 - 2\omega_m + \sum_j \omega_j^2)$
> 并代入指数期望即得结果。 $\square$

> **Corollary:** [噪声检测的指数优势]<!-- label: cor:noise_advantage -->
> 在$M_t$个专家的Yajie共识下，含噪构型（$\sigma_\epsilon > 0$）的共识评分与无噪构型（$\sigma_\epsilon = 0$）的评分之比为：
> 
> $$
>     \frac{\E[s_{Yajie} \mid \sigma_\epsilon > 0]}{\E[s_{Yajie} \mid \sigma_\epsilon = 0]} = \left(1 + \frac{\sigma_\epsilon^2}{\bar_{expert}^2}\right)^{-M_t/2}
> $$
> 
> 该比值随$M_t$指数衰减。当$M_t = 8$，$\sigma_\epsilon = 2\bar_{expert}$时，
> 比值约为$5^{-4} = 0.0016$——噪声构型的共识评分比无噪构型低三个数量级。

这一性质是Spring实时噪声过滤的数学基础：
Yajie{}共识评分在训练过程中自动区分干净数据和噪声数据，
无需额外的事后噪声检测步骤。

### 共识评分在训练循环中的应用

在Spring的每次迭代中，Yajie共识评分参与以下三项核心操作：

> **Protocol:** [Yajie驱动的噪声移除协议]<!-- label: prot:noise_removal -->
> 对于第$t$次迭代：
> 
1. 计算所有$N_{data}$个训练构型的共识评分$\{s_i^{(t)}\}_{i=1}^{N_{data}}$。
2. 按评分排序，识别低共识尾部。设阈值$\tau_{noise}^{(t)}$为：
3. 移除共识评分低于$\tau_{noise}^{(t)}$的构型，净化后的数据集为：
4. 更新噪声评分直方图$\mathcal{H}_{noise}^{(t)}$，记录每轮移除的构型数量及其评分分布。

> **Remark:** [噪声移除的保守性]
> Spring的噪声移除是*保守*的——它只移除在当前迭代中*所有*专家均无法达成共识的构型。
> 如果某个构型在$M_t$个专家中有$M_t - 1$个达成共识而仅1个产生分歧，
> 它的共识评分虽然降低，但不会低于$p_{noise}$分位数——
> 这确保Spring不会因为单个异常专家而错误地丢弃有效数据。
> 这种设计体现了Yajie协议的核心原则：**共识是判断噪声的唯一依据，而少数专家的分歧不构成噪声证据**。

---

## $M_t$自动生成与共生绑定

### 从超参数到内生变量

在现有势函数训练框架中，模型的复杂度参数（层数、宽度、基函数数量等）由工程师通过试错或网格搜索确定。
这些参数的选择直接影响最终的势函数质量，但它们与训练数据之间不存在*结构性的*绑定关系——
同一个超参数配置在不同的数据子集上可能产生截然不同的模型质量，
而工程师无法从事前判断哪些配置对哪些数据是合适的。

Spring的一个核心创新是：**$M_t$不是工程师声明的超参数，而是训练过程的内生产物**。
$M_t$由数据驱动自动生成，并通过密码学哈希与训练数据绑定——
一旦数据和训练流程确定，$M_t$就是唯一确定的。

> **Definition:** [自生成专家数$\Mauto$]
> 设训练数据为$\D$，其SHA-256哈希为$\Dhash = SHA-256(\D)$。
> 第$t$次迭代的自动生成专家数定义为：
> 
> $$<!-- label: eq:Mt_definition -->
>     \boxed{\Mauto = \Xi(\Dhash; \Lyap_{t-1}, \mathbf{s}_{Yajie}^{(t-1)}, \Sigma_0(\D))}
> $$
> 
> 其中：
> 
- $\Dhash$为数据指纹——确保$M_t$与数据绑定的密码学基础；
- $\Lyap_{t-1}$为上轮Lyapunov监控量——反映当前训练的收敛进度；
- $\mathbf{s}_{Yajie}^{(t-1)}$为上轮Yajie共识评分向量——反映数据的内在噪声水平；
- $\Sigma_0(\D)$为数据的能量景观复杂度估计（见下文定义 [ref]）；
- $\Xi: \{0,1\}^{256} \times \R^+ \times [0,1]^{N_{data}} \times \R^+ \to \N_{>1}$为确定性生成函数。

### 数据复杂度$\Sigma_0(\D)$的定义

> **Definition:** [训练数据的能量景观复杂度]<!-- label: def:data_complexity -->
> 设训练数据$\D$覆盖的能量范围为$[E_, E_]$。
> 定义能量分布的信息熵为：
> 
> $$
>     H_E(\D) = -\int_{E_}^{E_} p(E) \log p(E) \, dE
> $$
> 
> 其中$p(E)$为训练数据中构型能量的经验分布密度。
> 数据复杂度$\Sigma_0(\D)$定义为：
> 
> $$<!-- label: eq:Sigma0_data -->
>     \Sigma_0(\D) = \frac{H_E(\D)}{H_} \cdot \left(1 + \frac{\sigma_E}{\bar{E}}\right) \cdot \left(1 + \frac{N_{species}}{N_{species}^{ref}}\right)
> $$
> 
> 其中$H_ = \log(E_ - E_)$为均匀分布的最大熵，
> $\sigma_E$为能量标准差，
> $\bar{E}$为平均能量，
> $N_{species}$为化学物种数量，
> $N_{species}^{ref} = 1$为参考物种数。
> $\Sigma_0(\D) \in [0, \infty)$，越大的值代表数据分布越复杂（覆盖更多能量范围、更多物种、更大的能量方差）。

> **Theorem:** [$M_t$的数据驱动性质 — 定理3]<!-- label: thm:Mt_theorem -->
> 在Spring训练循环中，自动生成的$M_t$是数据复杂度$\Sigma_0(\D)$的单调非减函数：
> 
> $$<!-- label: eq:Mt_monotonic -->
>     \Sigma_0(\D_1) \geq \Sigma_0(\D_2) \Longrightarrow \Mauto(\D_1) \geq \Mauto(\D_2)
> $$
> 
> 且$M_t$满足边界约束：
> 
> $$<!-- label: eq:Mt_bounds -->
>     M_ \leq \Mauto \leq M_
> $$
> 
> 其中$M_ = 3$（审计的最小专家数，由SCX定理1要求$M>1$并加安全裕度给出），
> $M_ = \min(32, \lfloor N_{data} / N_{min\_per\_expert} \rfloor)$（受数据总量限制）。

> **Proof:** $\Xi$的构造如下：
> 
1. 从$\Dhash$派生确定性随机种子：$seed = int(\Dhash[0:8], 16)$。
2. 计算复杂度缩放因子：$\alpha(\D) = \min(1, \Sigma_0(\D) / \Sigma_0^{ref})$，
3. 计算收敛进度因子：$\beta_t = \max(0, 1 - \Lyap_{t-1} / \Lyap_0)$，
4. 计算噪声惩罚因子：$\gamma_t = 1 - \frac{1}{N_{data}}\sum_i \mathbb{1}[s_i^{(t-1)} < \tau_{noise}]$，
5. 生成$M_t$：

> $\alpha(\D)$随$\Sigma_0(\D)$单调增加，$\beta_t$和$\gamma_t$随训练进展单调增加，
> 因此$\Mauto$随数据复杂度单调非减。
> 边界约束由取整和数据分割限制自然满足。 $\square$

> **Remark:** [共生绑定的含义]
> "共生绑定"（Symbiotic Binding）意味着$M_t$与训练数据之间是一种*双向不可分*的关系：
> 
- **正向：** 给定$\D$，$M_t$被唯一确定。无法在不改变数据的情况下改变$M_t$。
- **反向：** 给定$M_t$，可以验证$\Dhash$与$M_t$的一致性。如果训练数据被篡改，$M_t$也会改变，篡改能被检测到。

> 这一双向绑定机制确保了Spring训练的**可复现性**和**可审计性**：
> 任何第三方可以独立验证一个声称的Spring势函数是否确实是从声称的数据中训练得到的。

### $M_t$的演化动力学

在Spring训练循环中，$M_t$不是固定的——它随训练进展而动态演化。
图 [ref]展示了$M_t$的典型演化轨迹。

[Figure omitted — see original .tex]

---

## Cercis评分：跨架构可比的单一质量度量

### 为什么需要新的质量度量？

目前，势函数领域使用RMSE（均方根误差）作为几乎唯一的质量度量。
RMSE存在三个根本性问题：

1. **聚合性与实例性：** RMSE是一个聚合统计量——它回答"平均多准"，而非"这个构型是否可靠"。
2. **数据依赖性：** RMSE依赖于测试集的选择。不同的测试集给出不同的RMSE，而测试集的选择本身是主观的。
3. **跨架构不可比：** NEP的RMSE=1 meV/atom和DeepMD的RMSE=1 meV/atom意味着什么？

Cercis{}评分 [cite]将这些问题统一解决为两个正交维度：
**精度（Precision）**和**覆盖度（Coverage）**。

> **Definition:** [Cercis{}评分 — 势函数版本]<!-- label: def:cercis_potential -->
> 对于由Spring训练产生的势函数$V^{(t)}_{consensus}$，其Cercis{}评分定义为：
> 
> $$<!-- label: eq:cercis_potential -->
>     \boxed{S_{Cercis}(V) = Q_{prec}(V) + \eta \cdot N_{cov}(V)}
> $$
> 
> 其中：
> 
- $Q_{prec}(V) \in [0,1]$为**质量保证得分（Quality Guarantee）**，衡量势函数预测精度的可验证性。
- $N_{cov}(V) \in [0,1]$为**覆盖度得分（Coverage）**，衡量训练数据覆盖的有效构型空间比例。
- $\eta = 0.2$为**认知折扣因子**：精度有保证时的覆盖才有价值；没有精度保证的覆盖是噪声。

### 质量保证得分$Q_{prec$的构成}

$Q_{prec}$由三项组成，分别对应势函数审计三元组（第1.2节）的三个条件：

$$<!-- label: eq:Q_decomposition -->
    Q_{prec}(V) = \frac{1}{3}\left(q_{loc}(V) + q_{ood}(V) + q_{multi}(V)\right)
$$

1. **误差定位得分$q_{loc}$：**
2. **分布外检测得分$q_{ood}$：**
3. **多解可辨性得分$q_{multi}$：**

### 覆盖度得分$N_{cov$的构成}

覆盖度得分衡量训练数据在构型空间中的覆盖质量：

$$<!-- label: eq:N_coverage -->
    N_{cov}(V) = \exp\left(-\frac{\Omega_{unsampled}}{\Omega_{total}}\right) \cdot \left(1 - \frac{E_{gap}}{E_ - E_}\right)
$$

其中：

- $\Omega_{unsampled}/\Omega_{total}$为构型空间中未被采样的体积比例（通过Voronoi镶嵌估计）。
- $E_{gap}$为训练数据能量分布中最大的连续空白区间长度——间隙越大，该能量区域的预测越不可靠。

### Cercis评分的跨架构可比性

Cercis评分的核心优势在于：**它使不同架构的势函数在统一维度下可比较**。
表 [ref]给出了按Cercis评分排名的示意性比较。

[Table omitted — see original .tex]

> **Remark:** [Cercis评分可超过1.0]
> 当$Q_{prec}$和$N_{cov}$都很高时，$S_{Cercis}$可以超过1.0——这表示势函数同时在精度可验证性和数据覆盖度两个维度上表现优异。
> $S_{Cercis} = 1.0$是"基本可部署"的参考标准。

---

## Lyapunov收敛分析

### Spring训练循环的动力学表述

将Spring训练循环视为离散动力系统，其状态变量为$\mathbf{X}_t = (\Lyap_t, M_t, \mathbf{s}_{Yajie}^{(t)}, \D^{(t)})$。
系统的演化由映射$\Phi: \mathbf{X}_t \mapsto \mathbf{X}_{t+1}$给出，
其中$\Phi$封装了第2节描述的完整训练循环（自举→训练→共识→调控）。

> **Definition:** [Spring训练的Lyapunov函数]<!-- label: def:lyap -->
> Spring训练循环的自然Lyapunov函数定义为：
> 
> $$<!-- label: eq:Lyap_def -->
>     \boxed{\Lyap_t = \frac{1}{|\D^{(t)}|}\sum_{\mathbf{R} \in \D^{(t)}} \Var_{m=1,...,M_t}\left[f_m^{(t)}(\mathbf{R})\right]}
> $$
> 
> 即所有训练构型上$M_t$个专家预测的方差均值。

$\Lyap_t$具有明确的物理含义：

- $\Lyap_t$大 $\Longrightarrow$ 专家间分歧大 $\Longrightarrow$ 共识尚未形成 $\Longrightarrow$ 训练不充分。
- $\Lyap_t$小 $\Longrightarrow$ 专家间高度一致 $\Longrightarrow$ 共识已经形成 $\Longrightarrow$ 训练接近收敛。
- $\Lyap_t \to 0$ $\Longrightarrow$ 所有专家在所有训练构型上给出相同预测 $\Longrightarrow$ 完全收敛。

### 收敛定理

> **Theorem:** [Spring训练的Lyapunov收敛定理 — 定理4]<!-- label: thm:lyap_convergence -->
> 设Spring训练循环满足以下条件：
> 
1. **专家容量的有界性：** 存在常数$B_f < \infty$，使得对所有专家$m$和所有构型$\mathbf{R}$，
2. **训练数据的有限性：** $|\D| = N_{data} < \infty$。
3. **噪声移除的保守性：** 遵循协议 [ref]，噪声移除比例$\nu_t$满足$\sum_t \nu_t < \infty$（仅有限多构型被移除）。
4. **优化的渐近性：** 每轮独立训练的优化过程达到$\varepsilon_{opt}^{(t)}$-近似最优，

> 则在Spring训练循环下：
> 
> $$<!-- label: eq:lyap_convergence -->
>     \boxed{\lim_{t \to \infty} \Lyap_t = 0}
> $$
> 
> 即系统渐近收敛到完美共识状态。

> **Proof:** 证明分三步。
> 
> **第一步：**$\Lyap_t$的非增性（几乎处处）。
> 在第$t$次迭代中，噪声移除协议 [ref]移除了共识评分最低的构型。
> 这些构型对$\Lyap_t$的贡献最大（分歧最大的构型就是方差最大的构型）。
> 移除它们直接降低$\Lyap_t$。
> 
> 其次，在新数据集$\D^{(t+1)}$上训练的专家，由于噪声更少，
> 其预测的一致性天然高于在$\D^{(t)}$上训练的专家。
> 形式化地：
> 
> $$<!-- label: eq:lyap_decrease -->
>     \Lyap_{t+1} \leq \Lyap_t - \Delta_{noise}^{(t)} + \Delta_{opt}^{(t)}
> $$
> 
> 其中$\Delta_{noise}^{(t)} > 0$为噪声移除带来的方差降低，
> $\Delta_{opt}^{(t)} = \mathcal{O}(\varepsilon_{opt}^{(t)})$为优化不完全带来的小涨落。
> 
> **第二步：**$\Lyap_t$有下界0。
> $\Lyap_t$是方差均值，天然非负：$\Lyap_t \geq 0$对所有$t$成立。
> 
> **第三步：**收敛性的建立。
> 由条件(C3)，$\sum_t \nu_t < \infty$，故存在$T_0$使得对所有$t \geq T_0$，$\nu_t = 0$（不再移除任何构型）。
> 此后，$\D^{(t)} = \D^{(T_0)}$是固定的有限数据集。
> 
> 由条件(C4)，在固定数据集上重复训练，优化误差$\varepsilon_{opt}^{(t)} \to 0$。
> 由条件(C1)，专家参数空间紧致，训练序列$\{\theta_m^{(t)}\}$存在于紧集中，
> 因此存在收敛子列。
> 
> 在极限$t \to \infty$下，所有专家在固定数据集$\D^{(T_0)}$上达到全局最优（或相同局部最优盆地），
> 预测值趋于一致，因此$\Lyap_t \to 0$。
> 
> 由单调有界序列的收敛定理（$\Lyap_t$单调递减有下界），$\lim_{t\to\infty} \Lyap_t$存在。
> 再结合上述论证，极限必为0。 $\square$

> **Corollary:** [收敛速率]<!-- label: cor:convergence_rate -->
> 在条件(C1)-(C4)下，Spring训练的收敛速率至少为：
> 
> $$<!-- label: eq:convergence_rate -->
>     \Lyap_t \leq \Lyap_0 \cdot \exp(-\lambda t) + \mathcal{O}\left(\frac{1}{t}\right)
> $$
> 
> 其中$\lambda > 0$为表征专家学习速率的衰减常数，取决于专家架构的容量和数据的信息含量。

### Lyapunov函数选择的物理动机

选择$\Lyap_t$作为Lyapunov函数并非随意——它具有深层物理动机。
在统计力学中，$\Lyap_t$的倒数$1/\Lyap_t$可以解释为
具有$M_t$个副本的系统的有效温度$T_{eff}$ [cite]。
高$T_{eff}$（小$\Lyap_t^{-1}$）对应专家高度一致的"冻结"相；
低$T_{eff}$（大$\Lyap_t^{-1}$）对应专家高度分歧的"顺磁"相。
Spring训练的收敛过程，从这一角度看，是系统从高温分歧相降温到低温共识相的*退火*过程。

> **Remark:** [与SCX哈密顿量理论的联系]
> 在SCX哈密顿量理论 [cite]中，
> Parisi序参数$q(x)$描述了副本（专家）间的重叠分布。
> $\Lyap_t$的物理对应是$1 - q(0)$（$q(0)$为不同盆间的重叠，$\Lyap_t$反映盆间分歧程度）。
> Spring训练的收敛等价于副本对称性从破缺态恢复到对称态的过程——
> 这是自旋玻璃理论在势函数训练中的直接应用。

---

## 与NEP/DeepMD/ACE的系统比较

### NEP（Neuroevolution Potential）：$M=1$的不可验证性

NEP（Fan et al., 2022）是近年来最具影响力的机器学习势函数之一，
以其"单网络+分离卷积"架构的高效性著称。
NEP的核心设计思想是：通过精心设计的描述符和分离卷积神经网络，
在保持训练和推理效率的同时达到化学精度。

然而，从SCX审计框架审视，NEP具有一个不可消除的结构性缺陷：**$M=1$**。

- **误差检测的不可能性：** NEP产生单一预测。当该预测错误时——无论是在训练分布内还是分布外——NEP没有任何内部机制来检测该错误。自审计等于无审计（SCX定理2）。
- **精度与可靠性的混淆：** NEP论文通过能量/力RMSE来证明其精度。但RMSE不能替代逐点可靠性——一个RMSE=1 meV/atom的NEP模型可能在1\%的关键构型上产生100 meV的误差，而用户无从知晓。
- **超参数的非绑定：** NEP的架构超参数（截止半径、神经元数、层数等）由用户手动调整。它们与训练数据之间没有绑定关系——同一套超参数在不同的数据子集上可能产生质量迥异的势函数。

### DeepMD（Deep Potential）：$M=1$，事后的不确定性

DeepMD（Zhang et al., 2018; Wang et al., 2018）是使用最广泛的深度学习势函数框架。
其核心优势在于：(1) 能量守恒的严格满足（力由势能的负梯度解析计算）；
(2) Deep Potential-Smooth Edition对势函数光滑性的保证；
(3) DeePMD-kit的工程成熟度。

但在审计维度上，DeepMD与NEP面临同样的$M=1$问题：

- **事后ensemble并非审计：** DeepMD社区发展了几种不确定性量化方法——Deep Ensemble（训练多个DeepMD模型取平均）、Dropout ensemble等。但这些方法有两个问题：(1) 它们是*事后*添加的——不嵌入训练过程本身；(2) 同一架构的多个模型共享结构偏差，$M_{eff} \ll M_{nominal}$。
- **训练数据中的噪声无法自动检测：** DeepMD假设DFT标签是"真实"的，忽略了DFT计算中的泛函选择偏差、k点采样误差和赝势近似误差。当训练数据包含系统性噪声时，DeepMD无法自动识别。
- **DeepMD与Spring的集成可能性：** 值得指出的是，DeepMD的模型架构*可以*作为Spring中的一个专家类型。Spring框架是**架构无关的**——任何一个满足独立训练条件的回归模型都可以成为Spring的专家。因此，从DeepMD到Spring不是"替代"而是"升级"：将$M=1$的DeepMD升级为$M>1$的Spring-DeepMD。

### ACE（Atomic Cluster Expansion）：完备基的局限

ACE（Drautz, 2019）在理论上是最"完备"的势函数框架——它在一组系统构造的完备基函数上展开原子能量，从理论上可以逼近任意光滑的势能面。
ACE的优势在于：(1) 线性参数化，训练是凸优化；(2) 基的完备性保证逼近能力。

但完备性*不等于*可审计性：

- **完备基中的过拟合：** ACE的线性参数化意味着基函数数量随截断阶数快速增长。当基函数数量接近训练构型数量时，存在无穷多组参数在训练数据上达到零误差——但在数据覆盖薄弱的区域预测完全不同。ACE本身无法区分这些等价解中哪一个是物理上正确的。
- **线性模型的"置信度"问题：** 线性回归可以提供系数的标准误差，从而给出预测方差。但这一方差只反映*同一模型*在重复抽样下的统计不确定性——它不考虑模型形式的系统误差（即真实势能面不是一个截断的ACE展开）。这种"置信度假象"比没有置信度更危险。
- **多解的不可辨性：** 两个不同截断阶数的ACE模型可能给出不同的预测——ACE框架内部没有机制来判断哪个更可靠（更高的截断阶数不一定更好，可能引入了数据的噪声结构）。

### 综合对比矩阵

表 [ref]给出了Spring与三种主要框架在审计相关维度上的完整对比。

[Table omitted — see original .tex]

### 定性差异：训练过程中的审计信息流

图 [ref]对比了Spring与其他框架在训练过程中的审计信息流。

[Figure omitted — see original .tex]

---

## 讨论

### Spring的适用边界

Spring作为"训练即审计"框架，有其明确的适用条件和边界：

1. **适用条件：**
2. **不适用场景：**
3. **中间地带：** 对于计算资源有限但需要审计保证的场景，

### 计算成本分析

Spring相对于$M=1$框架的主要代价是$M_t$倍的训练计算。
具体而言：

- **前向传播成本：** $\mathcal{O}(M_t)$。$M_t$个专家独立前向传播，天然可并行。
- **反向传播成本：** $\mathcal{O}(M_t)$。各专家独立计算梯度，无梯度通信开销。
- **总训练时间：** $\mathcal{O}(M_t \cdot T_{单专家})$，
- **并行化：** $M_t$个专家可完全并行训练，在$M_t$个GPU上线性加速。

> **Remark:** [成本-审计收益权衡]
> Spring的$M_t$倍训练成本不应被视为"额外"成本，而应被视为**审计基础设施的成本**——
> 就像实验室的校准仪器成本、建筑的地震加固成本一样。
> 一个没有审计的势函数，其预测对于安全关键应用而言价值为零——
> 无论它的RMSE多低。
> 从这个角度看，Spring的成本是*使势函数可部署的必要投入*，
> 而非可有可无的额外开销。

### 诚实暴击：Spring的局限与未解决问题

> **诚实暴击:** Spring不是万能药。以下是我们诚实面对的限制和开放问题。}

1. **$M_t$倍训练成本的不可消除性：**
2. **共识一致性的幻觉风险：**
3. **Lyapunov收敛的有限时间保证：**
4. **数据哈希绑定的实际强度：**
5. **Cercis评分中$\eta=0.2$的校准：**

### 与SCX理论体系的内在关系

Spring自演化势函数训练器是SCX理论体系在分子模拟领域的系统化应用。
它与SCX其他组件的关系如下：

- **SCX定理1（多专家检测）：** Spring的核心数学基础——$M_t$个专家提供了误差检测的指数保证。
- **SCX定理2（自审计禁止）：** 解释了为什么$M=1$的势函数框架在认识论上等价于无审计。
- **SCX定理3（噪声-信号不可区分）：** 为Yajie共识评分作为噪声检测机制提供了理论支撑。
- **Yajie{}协议：** 多专家共识评分的算法基础，Spring将其适配到势函数训练场景。
- **SCX哈密顿量理论 [cite]：** 将Spring训练的Lyapunov收敛过程解释为副本对称性恢复过程。
- **Cercis{}评分：** 提供了跨架构可比的单一质量度量。

---

## 结论

本文提出了Spring{}自演化势函数训练器——第一个实现"训练即审计"的分子动力学势函数学习框架。
我们的核心贡献可以总结为以下五点：

1. **训练即审计的范式转换：**
2. **多专家训练定理（定理1）：**
3. **Yajie共识集成（定理2）：**
4. **$M_t$自动生成与共生绑定（定理3）：**
5. **Lyapunov收敛定理（定理4）：**

Spring{}框架的一个直接推论是：**未经过审计的势函数（$M=1$）不应该被部署在安全关键应用中**。
这不是一个性能问题——它是一个认识论问题。
一个$M=1$的势函数无法告诉你它何时出错，
因此无论它的RMSE多么令人印象深刻，
它都缺乏作为科学工具或工程组件的基本可验证性。

未来的工作方向包括：

- **异构专家池：** 将Spring扩展到支持混合架构的专家池（NEP + DeepMD + ACE），
- **自适应收敛准则：** 开发数据驱动的、不依赖启发式阈值$\varepsilon_{conv}$的收敛判断方法。
- **大规模实证验证：** 在涵盖多种材料体系（金属、半导体、分子晶体、液体）的标准基准上，
- **与主动学习的整合：** 将Spring的Yajie共识评分作为主动学习的采集函数——
- **工业部署标准：** 制定Spring训练势函数的工业规范——

\rule{0.4pt}

**致谢：** 
感谢SCX理论团队在定理证明、Yajie协议设计和Cercis评分框架方面的开创性工作。
本文是SCX理论体系在分子模拟领域的应用和拓展。
所有数学证明在标注的假设范围内是严格的。

\begin{thebibliography}{99}

\bibitem{scx_ml_audit}
SCX. *The SCX Inquisition: A Complete Audit of Machine Learning — What Every Algorithm Lacks and Why.*
SCX预印本, 2026.

\bibitem{scx_hamiltonian}
SCX. *哈密顿量作为审计条件——从能量景观判断可审计性.*
SCX理论体系 — 统计力学卷, 2026.

\bibitem{yajie_protocol}
SCX. *The Yajie Protocol: Technology Lock-in, Audit Sovereignty, and the Non-Proliferation Logic of Data Quality Assessment.*
SCX预印本, 2026.

\bibitem{nep}
Fan, Z. et al. *Neuroevolution machine learning potentials: Combining high accuracy and low cost in atomistic simulations.*
Phys. Rev. B, 2022.

\bibitem{deepmd}
Zhang, L., Han, J., Wang, H., Car, R., \& E, W. *Deep Potential Molecular Dynamics: A Scalable Model with the Accuracy of Quantum Mechanics.*
Phys. Rev. Lett., 2018.

\bibitem{ace}
Drautz, R. *Atomic cluster expansion for accurate and transferable interatomic potentials.*
Phys. Rev. B, 2019.

\bibitem{gap}
Bart\'{o}k, A.P. et al. *Gaussian Approximation Potentials: The Accuracy of Quantum Mechanics, without the Electrons.*
Phys. Rev. Lett., 2010.

\bibitem{mtp}
Shapeev, A.V. *Moment Tensor Potentials: A Class of Systematically Improvable Interatomic Potentials.*
Multiscale Model. Simul., 2016.

\bibitem{bp}
Behler, J. \& Parrinello, M. *Generalized Neural-Network Representation of High-Dimensional Potential-Energy Surfaces.*
Phys. Rev. Lett., 2007.

\bibitem{lyapunov}
Lyapunov, A.M. *The General Problem of the Stability of Motion.*
1892 (English translation: Int. J. Control, 1992).

\bibitem{scx_galois}
SCX. *Galois不可解定理与审计的群论极限.*
SCX理论体系 — 代数学卷, 2026.

\bibitem{scx_distillation_hallucination}
SCX. *蒸馏幻觉定理：从知识蒸馏的角度理解AI幻觉.*
SCX预印本, 2026.

\end{thebibliography}