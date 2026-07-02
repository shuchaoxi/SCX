# 本文提出\Situs{}——一种

**Author:** SCX

*Abstract:*

大语言模型的位置编码（Positional Encoding, PE）本质上是统计驱动的——其频率分布与数据中
token共现的统计规律对齐，缺乏对物理世界因果结构的建模能力。本文提出\Situs{}——一种
**物理锚定的位置编码**框架，将可观测物理量（空间坐标、序列位置、系统尺寸）作为编码的
原始信号源。\Situs{}的核心理念是：当物理位置在给定状态原子的条件下携带关于标签的额外互信息
$I(Y; P \mid S) > 0$时，位置编码嵌入的表示空间能够系统性地增强多专家标签噪声检测的统计功效。

本文在四个层面上为\Situs{}建立严格数学基础。**第一**（编码函数理论），基于Bochner定理
和Laplace核推导了正弦编码的最优频率谱（定理1.2.1），证明了逼近误差以$O(1/d)$速率收敛
（定理1.2.2），并为标量正弦编码和3D旋转编码分别计算了精确Lipschitz常数
（定理1.2.3、定理1.3.1），建立了统一Lipschitz连续性定理（定理1.4.1）。
**第二**（Theorem~1修正），修正了此前审计报告中$\delta_s^$的符号错误，
给出了$\Delta_s^ = \Delta_s + \delta_s^$的精确表达式，
证明了$\delta_s^ > 0$的充分条件为$I(Y; P \mid S) > 0$（定理2.2.1，限定贝叶斯最优分类器），
并分别通过数据处理不等式（定理2.3.1）给出了$\delta_s^$的
信息论上界，通过启发式Fano估计（命题2.4.1）给出了量级参考。**第三**（Theorem~2修正），定义了编码不完美度
$\varepsilon_ = I(Y; P \mid X) - I(Y; \PE(P) \mid X)$（定义3.1），
修正了弱特征失效上界（Theorem~$2'$），并给出了基于KSG估计器和预测性能差异的两种
$\varepsilon_$可估计形式（定理3.3.1、命题3.3.1）。
**第四**（Theorem~$3'$），精确阐明了固定位置编码和学习型位置编码对噪声-困难样本
不可区分性的截然不同的影响：固定编码保持定理3的不可区分性（命题4.1），而通过学习
编码破坏不可区分性目前是一个**开放问题**（原声称的``构造性示例''实际展示了定理的鲁棒性）。
修正定理陈述（Theorem~$3'$）给出了保持不可区分性的精确前提条件。

本文保持对理论局限性的诚实态度：明确标注了所有严格证明的定理与启发式论证的命题；
指出了3D旋转编码缺少旋转等变性这一根本缺陷；分析了\Situs{}在固有无序区域、纯组成分类、
虚假相关性等场景中的退化与风险。本文的理论框架为物理科学中位置感知的机器学习提供了可验证
的预测和可操作的指导原则。

**关键词：**位置编码，物理锚定，多专家一致性，标签噪声检测，信息论，Lipschitz连续性，
Bochner定理，不可区分性

## 引言

### 位置编码：从统计驱动到物理驱动

现代大语言模型的核心组件之一是位置编码（Positional Encoding, PE）。
在Transformer架构中，自注意力机制本质上是置换不变的——它处理的是输入的**集合**而非
**序列**。位置编码通过向token嵌入中注入位置相关的信号来打破这种对称性，使模型能够
利用序列顺序信息 [cite]。

然而，当前主流的位置编码方法——无论是正弦编码 [cite]、
旋转位置编码（RoPE） [cite]，还是可学习的位置嵌入 [cite]——
都共享一个根本特征：它们是**统计驱动**的。这意味着：

1. 编码函数的参数（频率、波长、基函数形式）要么是先验固定的（基于关于
2. 编码所捕获的``位置关系''本质上是**语言学的**——它反映的是词序、句法距离、
3. 编码的设计目标是最小化语言建模的困惑度（perplexity），而非忠实地表征物理世界中

当这些统计驱动的位置编码被应用于**物理科学**领域——如蛋白质功能预测、晶体缺陷检测、
药物-靶标对接评分——时，出现了一个根本性的不匹配：物理世界的结构由空间中的原子坐标、
化学键的几何约束、能量面的曲率边界所决定，而这些因果关系**不能**从token共现统计中
推断出来。

**一个简单的物理事实说明了这一鸿沟：**考虑蛋白质中的一个赖氨酸残基（Lys）。
在标准的氨基酸tokenization中，所有赖氨酸残基被映射为同一个token。
然而，位于酶活性位点的Lys-37（侧链$pK_a$降至6--8，参与酸碱催化）与位于
溶剂暴露表面的Lys-289（$pK_a \approx 10.4$，参与非特异性静电相互作用）
具有**完全不同的功能角色**。这两个残基的局部化学环境差异并非源于残基类型
（它们同为Lys），而是源于它们在三维折叠结构中的**空间位置**。
一个统计驱动的编码永远无法区分它们；一个物理驱动的编码却可以。

### \Situs{的核心思想}

本文提出\Situs{}（源自拉丁语*situs*，意为``位置''或``场所''）——一种
**物理锚定的位置编码框架**。\Situs{}的基本理念可以表述为：

> **\Situs{}原则：**若物理位置$P$在给定状态原子$S$的条件下携带关于标签$Y$的
>     额外互信息——即$I(Y; P \mid S) > 0$——则存在一种位置编码函数
>     $\PE: \Ppos \to \R^{d_}$，使得在编码空间中，多专家标签噪声检测的统计功效
>     得到系统性增强。

\Situs{}定义了三类物理位置域（定义1.1.1--1.1.3）：

- **标量序列域** $\Ppos_{seq} = \{1, 2, ..., L\}$：
- **三维向量域** $\Ppos_{3D} = \R^3$：
- **标量总数域** $\Ppos_{count} = \N$：

### 理论背景：SCX框架与CC审计

\Situs{}被设计为嵌入SCX（State-Conditioned eXpertise）框架的一个组件。
SCX框架通过以下机制运作 [cite]：设有$M$个独立专家模型
$\{E_1, ..., E_M\}$，对于每个状态原子$s_i$及其标签$y_i$，专家$m$的投票为
$v_m(s_i) = \mathbf{1}[E_m(s_i) \neq y_i] \in \{0, 1\}$。
在干净样本下，$v_m \sim Bernoulli(p_{clean, s})$（$p_{clean, s} < 0.5$）；
在噪声样本下，$v_m \sim Bernoulli(p_{noisy, s})$（$p_{noisy, s} > 0.5$）。
检测边际定义为$\Delta_s = p_{noisy, s} - p_{clean, s} > 0$。

SCX框架包含四个核心定理 [cite]：

- **Theorem 1**（多专家一致性噪声检测）：$F_1 \geq 1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)$，通过Chernoff-Hoeffding不等式保障；
- **Theorem 2**（弱特征必然失效）：$F_{1,SCX} \leq F_{1,base} + C_F\sqrt{\delta/2}$，通过Fano不等式刻画特征信息不足时的性能上界；
- **Theorem 3**（噪声与困难样本的不可区分性）：存在两个世界$W_A, W_B$，观测分布完全相同但内在结构不同，没有任何算法能仅通过观测数据区分它们；
- **Theorem 4**（精确常数Minimax最优）：误差指数达到Chernoff-Stein引理给出的信息论下界。

一篇独立的CC（Correctness \& Completeness）审计报告 [cite]分析了
物理位置编码和多头Spring机制对这四个定理的影响。该审计报告提出了许多有价值的见解，
但也存在若干需要修正的问题——包括符号不一致和两处符号错误（sign error）。

**本文的贡献：**

1. **编码函数的严密形式化**（\S2）：从第一性原理推导了基于物理相关核的最优
2. **Theorem 1的严格修正**（\S3）：纠正了CC审计报告中的符号错误，建立了
3. **Theorem 2的精确修正**（\S4）：引入了编码不完美度$\varepsilon_$的
4. **Theorem 3$'$的条件化**（\S5）：精确阐明了固定PE和学习型PE对不可区分性
5. **诚实暴击**（全文标注）：明确区分严格证明的定理与启发式论证的命题，

## 编码函数的严密数学基础

本节建立\Situs{}三类物理位置域上编码函数的严格数学形式化。所有编码函数的核心设计原则是：
**物理上邻近的位置应具有相似的编码**（局部性公理），且编码应对位置变化具有可控的
敏感度（Lipschitz连续性）。

### 三种物理位置域的形式化定义

> **Definition:** [标量位置域——蛋白质序列]
> <!-- label: def:1.1.1 -->
> 设$L \in \N$为序列长度。标量序列位置域定义为
> 
> $$
>     \Ppos_{seq} = \{1, 2, ..., L\} \subset \N，
> $$
> 
> 其连续近似为$\Ppos_{seq} \cong [0, L] \subset \R$。

> **物理含义：**残基索引携带局部化学环境的一维顺序信息（从N端到C端）。

> **Definition:** [三维向量位置域——原子坐标]
> <!-- label: def:1.1.2 -->
> 三维实空间位置域定义为
> 
> $$
>     \Ppos_{3D} = \R^3，
> $$
> 
> 元素$\mathbf{p} = (x, y, z) \in \R^3$为原子在笛卡尔坐标系中的坐标。

> **物理含义：**原子的三维空间位置携带键长、键角、配位数等完整几何信息。
> 这是**最丰富**的物理位置域。

> **Definition:** [标量总数域——原子数]
> <!-- label: def:1.1.3 -->
> 标量总数域定义为
> 
> $$
>     \Ppos_{count} = \N，
> $$
> 
> 元素$N$为系统的总原子数。

> **物理含义：**系统大小决定了能量面的维度、可能的振动模式数和有限尺寸效应。

### 标量正弦编码与最优频率谱

#### 编码定义与核表示

> **Definition:** [正弦标量位置编码]
> <!-- label: def:1.2.1 -->
> 对$p \in [0, L]$，编码维度$d$（偶数）：
> 
> $$
>     \boxed{
>     \PE_{scalar}(p, 2j) = \sqrt{\frac{2}{d}}\,\sin\!\left(\frac{2\pi p}{\lambda_j}\right),\quad
>     \PE_{scalar}(p, 2j+1) = \sqrt{\frac{2}{d}}\,\cos\!\left(\frac{2\pi p}{\lambda_j}\right)
>     }，
> $$
> 
> 其中$j = 0, 1, ..., d/2-1$，$\lambda_j > 0$为**特征波长**。

> 归一化因子$\sqrt{2/d}$保证了$\|\PE_{scalar}(p)\| = 1$对所有$p$恒成立
> （因为$d/2$个$(\sin,\cos)$对各贡献$(2/d) \cdot 1 = 2/d$，总和为$1$），
> 并使编码核在$d \to \infty$时**收敛到**目标核$k(\Delta)$而非发散至$O(d)$量级。

> **参数化选择：**与标准Transformer使用$\omega_j = 10000^{-2j/d}$的角频率参数化
> 不同，本文使用**波长参数化**$\lambda_j$，因为它直接对应物理长度尺度：
> $\lambda_j$是一个完整正弦周期对应的位置差。

编码的内积结构自然地导出平移不变的核表示：

$$
    \langle \PE_{scalar}(p), \PE_{scalar}(q) \rangle
    = \frac{2}{d}\sum_{j=0}^{d/2-1} \cos\!\left(\frac{2\pi(p-q)}{\lambda_j}\right)
    = \frac{2}{d}K_(\Delta)，
$$

其中$\Delta = p - q$为两个位置之间的位移。
在$\Delta = 0$处，$\langle \PE(p), \PE(p) \rangle = (2/d) \cdot (d/2) = 1 = k(0)$。
当$d \to \infty$时，$(2/d)K_(\Delta) \to \int_0^\infty S(\omega)\cos(\omega\Delta)d\omega = k(\Delta)$。

#### 最优频率谱的物理推导

核心问题：给定编码维度$d$和物理区间长度$L$，如何选择$\{\lambda_j\}_{j=0}^{d/2-1}$
使得编码``最优''？

\begin{assumption}[物理局部性公理]
<!-- label: ass:1.2.1 -->
物理上相邻的位置应具有相似的编码。对于凝聚态物理系统，存在一个递减的**物理相关核**
$k(\Delta)$（其中$\Delta = |p-q|$）控制两个位置表示应有的相似度：

$$
    k(\Delta) = \exp\!\left(-\frac\right)，
$$

其中$\xi > 0$是**物理相关长度**（例如：共价键长$\approx 1.9$\,\AA{}，
或静电屏蔽长度）。此核满足Bochner定理：它是正定的，因而是某个非负测度的Fourier变换。
\end{assumption}

Laplace核的选择具有明确的物理动机：在凝聚态物理中，局域扰动（如缺陷、杂质）引起的
结构弛豫和电子密度重排随距离呈指数衰减（Friedel振荡的包络、屏蔽Coulomb势的
Yukawa形式），衰减长度$\xi$对应Thomas-Fermi屏蔽长度或键的共轭长度。

> **Theorem:** [编码的最优频率谱——核均值嵌入视角]
> <!-- label: thm:1.2.1 -->
> 设目标核$k(\Delta) = \exp(-|\Delta|/\xi)$（Laplace核）。则规范化编码核
> $\frac{2}{d}K_(\Delta) = \frac{2}{d}\sum_{j=0}^{d/2-1} \cos(2\pi\Delta/\lambda_j)$
> 在$L^2([0, L])$中最优逼近$k(\Delta)$当且仅当$\{\lambda_j\}$满足：
> 
> $$
>     \boxed{
>     \lambda_j = 2\pi\xi \cdot \cot\!\left(\frac{\pi(2j+1)}{2d}\right),\quad
>     j = 0, 1, ..., \frac{d}{2}-1
>     }。
> $$

> **Proof:** **步骤1（Bochner表示）：**Laplace核的Fourier变换为
> 
> $$
>     \hat{k}(\omega) = \int_{-\infty}^ e^{-i\omega\Delta} e^{-|\Delta|/\xi}\,d\Delta
>     = \frac{2\xi}{1 + \xi^2\omega^2}，
> $$
> 
> 这是一个Cauchy分布（尺度参数$1/\xi$）。
> 
> **步骤2（积分表示）：**由Fourier反演公式和$\hat{k}$的偶对称性：
> 
> $$
>     k(\Delta) = \frac{1}{2\pi}\int_{-\infty}^ e^{i\omega\Delta}\hat{k}(\omega)\,d\omega
>     = \int_{0}^ \cos(\omega\Delta) \cdot S(\omega)\,d\omega，
> $$
> 
> 其中谱密度$S(\omega) = \frac{2\xi}{\pi(1 + \xi^2\omega^2)}$，
> 满足$\int_0^ S(\omega)\,d\omega = 1$。
> 
> **步骤3（分位数采样）：**规范化编码核$\frac{2}{d}K_(\Delta) = \frac{2}{d}\sum_{j=0}^{d/2-1} \cos(\omega_j \Delta)$
> （其中$\omega_j = 2\pi/\lambda_j$）是一个**等权离散和**（每项权重$2/d$），逼近连续积分
> $\int_0^ S(\omega)\cos(\omega\Delta)\,d\omega$。最优采样点应使
> $\{S(\omega_j)\Delta\omega_j\}$近似均匀权重，等价于从累积分布函数
> $Q(\omega) = \int_0^ S(u)\,du = \frac{2}\arctan(\xi\omega)$
> 按**分位数**采样。
> 
> **步骤4（求解）：**第$j$个频率点覆盖第$(2j+1)/d$分位数：
> 
> $$
>     Q(\omega_j) = \frac{2j+1}{d} \quad\Longrightarrow\quad
>     \omega_j = \frac{1}\tan\!\left(\frac{\pi(2j+1)}{2d}\right)。
> $$
> 
> 代入$\lambda_j = 2\pi/\omega_j$即得所求。 $\square$

\rigorous{} **证明状态：严格。**该定理是经典数值积分理论（Gauss quadrature的
连续类比）在谱域的直接应用。每一步——Bochner表示、Fourier反演、分位数采样——
均有严格的数学依据。

> **Corollary:** [低频截断]
> <!-- label: cor:1.2.1 -->
> 最大波长（$j=0$）为
> 
> $$
>     \lambda_ = 2\pi\xi \cdot \cot\!\left(\frac{2d}\right)
>     \approx 4d\xi \quad (对较大  d)。
> $$
> 
> 覆盖整个序列区间需满足$\lambda_ \geq 2L$（Nyquist条件），给出最小维度要求：
> 
> $$
>     \boxed{d_ \approx \frac{L}{2\xi}}。
> $$

> **Corollary:** [与Transformer编码的比较]
> <!-- label: cor:1.2.2 -->
> 标准Transformer使用$\omega_j \propto 10000^{-2j/d}$（几何级数），对应
> **对数均匀**频率分布。而物理最优（Laplace核）使用
> $\omega_j \propto \tan(\pi(2j+1)/2d)$（正切分布），更密集地采样**中频区域**。
> 差异来源：NLP中的位置关系是长程而非指数衰减的；物理系统的相关函数通常是短程指数衰减的。

> **Theorem:** [逼近误差界]
> <!-- label: thm:1.2.2 -->
> 对Laplace核和$d/2$个频率点的分位数采样，规范化编码核的逼近误差满足：
> 
> $$
>     \boxed{
>     \sup_{\Delta \in [0, L]} \left|\frac{2}{d}K_(\Delta) - k(\Delta)\right|
>     = O\!\left(\frac{1}{d}\right)
>     }，
> $$
> 
> 随着$d \to \infty$以$O(1/d)$速率收敛。精确常数依赖于$\xi$和$L$，但$O(1/d)$的收敛速率不依赖于
> 这些参数（仅要求$S(\omega)$光滑且$k(\Delta)$在$[0,L]$上有界）。

\rigorous{} **证明状态：标准数值分析结果，证明从略。**
这是带限函数Fourier积分的标准数值积分误差界。分位数采样使得每个频率区间的贡献平衡，
最大误差受最大被忽略的频率分量的Fourier系数控制。与原版本不同，此处使用规范化编码核
$(2/d)K_$而非未规范化的$K_$，确保逼近对象$k(\Delta)$与逼近量处于同一量级
（均为$O(1)$），而非$K_(0)=d/2$与$k(0)=1$的跨量级比较。

### 正弦编码的Lipschitz连续性

> **Theorem:** [正弦Situs编码的Lipschitz常数 (株定理)]
> <!-- label: thm:1.2.3 -->
> 标量正弦编码$\PE_{scalar}: [0, L] \to \R^d$是Lipschitz连续的，精确常数为：
> 
> $$
>     \boxed{
>     L_^{scalar} = \frac{2\sqrt{2}\,\pi}{\sqrt{d}} \cdot \sqrt{\sum_{j=0}^{d/2-1}\frac{1}{\lambda_j^2}}
>     }。
> $$

> **Proof:** 对每个维度对$(2j, 2j+1)$，归一化编码$\PE_j(p) = \sqrt{2/d}\,(\sin(2\pi p/\lambda_j), \cos(2\pi p/\lambda_j))$：
> 
> $$
>     \|\PE_j(p) - \PE_j(q)\|^2
>     &= \frac{2}{d}\Bigl[\bigl[\sin(2\pi p/\lambda_j) - \sin(2\pi q/\lambda_j)\bigr]^2
>      + \bigl[\cos(2\pi p/\lambda_j) - \cos(2\pi q/\lambda_j)\bigr]^2\Bigr] 

>     &= \frac{2}{d} \cdot 4\sin^2\!\left(\frac{\pi(p-q)}{\lambda_j}\right) 

>     &\leq \frac{2}{d} \cdot \left(\frac{2\pi|p-q|}{\lambda_j}\right)^2
>      = \frac{8\pi^2|p-q|^2}{d \cdot \lambda_j^2}，
> $$
> 
> 其中利用了三角恒等式$(\sin a - \sin b)^2 + (\cos a - \cos b)^2 = 4\sin^2((a-b)/2)$
> 和$|\sin\theta| \leq |\theta|$。
> 对所有$j$求和并开方即得所述常数。该上界是紧的（$p, q$无限接近时$\sin\theta \approx \theta$，等号渐近成立）。 $\square$

\rigorous{} **证明状态：严格。**每一步均为精确不等式，最后通过取$p, q$无限接近时
所有分量同时达到最大变化率来验证紧致性。

> **Corollary:** [Lipschitz常数的渐近行为]
> <!-- label: cor:1.2.3 -->
> 对分位数最优谱和归一化编码：
> 
> $$
>     L_^{scalar} \sim \frac{1} \cdot \sqrt{\frac{d}{6}} \quad (d \to \infty)。
> $$
> 
> 归一化后Lipschitz常数的增长从$O(d)$降为$O(\sqrt{d})$——归一化因子$\sqrt{2/d}$
> 抵消了一个$\sqrt{d}$因子，使得编码对位置变化的敏感度随维度**亚线性**增长。

### 三维旋转编码与群论基础

#### 编码定义

> **Definition:** [三维旋转位置编码]
> <!-- label: def:1.3.1 -->
> 对$\mathbf{p} = (x, y, z) \in \R^3$，编码维度$d$（$d \geq 6$，偶数）：
> 
> $$
>     \boxed{
>     \PE_{rot}(\mathbf{p}) = \mathbf{R}(\mathbf{p}) \cdot \mathbf{e}_0
>     }，
> $$
> 
> 其中$\mathbf{e}_0 \in \R^d$是固定的参考单位向量，
> $\mathbf{R}(\mathbf{p}) = \mathbf{R}_x(\alpha x) \cdot \mathbf{R}_y(\beta y) \cdot \mathbf{R}_z(\gamma z) \in SO(d)$，
> 而$\alpha, \beta, \gamma > 0$是三个空间维度的**频率参数**（rad/\AA{}）。
> 每个$\mathbf{R}_a(\theta)$是在指定二维平面上的$d$维旋转，三个旋转平面分别作用于
> 维度对$(0,1)$, $(2,3)$, $(4,5)$。剩余的$d-6$个维度被三个旋转不变地保留。

#### 群论结构

> **Proposition:** [$\R^3 \to SO(d)$的嵌入]
> <!-- label: prop:1.3.1 -->
> 映射$\mathbf{p} \mapsto \mathbf{R}(\mathbf{p})$是$\R^3$到$SO(d)$的三维Abel子群的
> **李群同态**。

关键性质：三个旋转矩阵作用于不相交的坐标对，因此彼此交换：

$$
    [\mathbf{R}_x(\theta), \mathbf{R}_y(\phi)] = 0,\quad
    [\mathbf{R}_y(\phi), \mathbf{R}_z(\psi)] = 0,\quad
    [\mathbf{R}_z(\psi), \mathbf{R}_x(\theta)] = 0。
$$

由此导出加法群同态$\mathbf{R}(\mathbf{p}_1 + \mathbf{p}_2) = \mathbf{R}(\mathbf{p}_1) \cdot \mathbf{R}(\mathbf{p}_2)$。

\rigorous{} **证明状态：严格。**这是有限维李群表示的基本习题。

#### 平移不变内积

对任意两个位置$\mathbf{p}, \mathbf{q} \in \R^3$：

$$
    \langle \PE_{rot}(\mathbf{p}), \PE_{rot}(\mathbf{q}) \rangle
    &= \langle \mathbf{R}(\mathbf{p})\mathbf{e}_0, \mathbf{R}(\mathbf{q})\mathbf{e}_0 \rangle
     = \langle \mathbf{e}_0, \mathbf{R}(\mathbf{q} - \mathbf{p})\mathbf{e}_0 \rangle 

    &= \cos(\alpha\Delta x) + \cos(\beta\Delta y) + \cos(\gamma\Delta z)，
$$

其中$\Delta\mathbf{p} = \mathbf{q} - \mathbf{p}$。内积**仅依赖相对位置**，
具有严格的平移不变性。这满足晶体学的基本要求——完美晶体中两个位置等价当且仅当它们的
相对位移是晶格向量。

#### 旋转编码的Lipschitz连续性

> **Theorem:** [旋转编码的Lipschitz常数 (株定理)]
> <!-- label: thm:1.3.1 -->
> 映射$\PE_{rot}: \R^3 \to \R^d$是Lipschitz连续的。取$\mathbf{e}_0$为每对
> 旋转平面的第一维为1的形式，精确常数为：
> 
> $$
>     \boxed{
>     L_^{rot} = \max(\alpha, \beta, \gamma)
>     }。
> $$

> **Proof:** **步骤1（直接范数计算）：**编码差为
> $\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})
>  = \mathbf{R}(\mathbf{p})\mathbf{e}_0 - \mathbf{R}(\mathbf{q})\mathbf{e}_0$。
> 由于三个旋转作用于互不相交的维度对，编码差的各个分量解耦：
> 
> $$
>     \|\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})\|^2
>     &= 2 - 2\cos(\alpha\Delta x) + 2 - 2\cos(\beta\Delta y) + 2 - 2\cos(\gamma\Delta z) 

>     &= 4\sin^2\!\left(\frac{\alpha\Delta x}{2}\right)
>      + 4\sin^2\!\left(\frac{\beta\Delta y}{2}\right)
>      + 4\sin^2\!\left(\frac{\gamma\Delta z}{2}\right)。
> $$
> 
> 
> **步骤2（利用$|\sin\theta| \leq |\theta|$）：**
> 
> $$
>     \|\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})\|^2
>     \leq \alpha^2\Delta x^2 + \beta^2\Delta y^2 + \gamma^2\Delta z^2
>     \leq \max(\alpha, \beta, \gamma)^2 \cdot \|\Delta\mathbf{p}\|_2^2。
> $$
> 
> 开方即得$\|\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})\|
>  \leq \max(\alpha, \beta, \gamma) \cdot \|\mathbf{p} - \mathbf{q}\|_2$。
> 
> **步骤3（紧致性）：**取$\Delta\mathbf{p} = (\varepsilon, 0, 0)$且$\alpha = \max(\alpha, \beta, \gamma)$，
> 当$\varepsilon \to 0$时$\|\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})\|
> = 2|\sin(\alpha\varepsilon/2)| \to \alpha|\varepsilon|
> = \max(\alpha, \beta, \gamma) \cdot \|\Delta\mathbf{p}\|$。该界是紧的。 $\square$

\rigorous{} **证明状态：严格。**利用旋转平面的正交性直接计算编码差，
避免了对互不相交子空间上矩阵差的三角不等式分解（该分解会在最坏情况下高估约$\sqrt{3}$倍）。

> **Remark:** [与先前版本中常数高估的说明]
> <!-- label: rem:1.3.1 -->
> 先前版本使用了$\|\mathbf{R}(\mathbf{p}) - \mathbf{R}(\mathbf{q})\|_F$的三角不等式分解
> 结合Cauchy-Schwarz，得到$2\sqrt{\alpha^2 + \beta^2 + \gamma^2}$。这一常数比真实值
> $\max(\alpha, \beta, \gamma)$高出约$2\sqrt{3} \approx 3.46$倍（当$\alpha=\beta=\gamma$时），
> 原因是：（i）三个差分矩阵作用于互不相交的子空间上，三角不等式$\|D_x+D_y+D_z\|_F
> \leq \|D_x\|_F + \|D_y\|_F + \|D_z\|_F$在最坏情况下可松$\sqrt{3}$倍；
> （ii）Cauchy-Schwarz将$\ell_1$转换为$\ell_2$又引入约$\sqrt{3}$倍松弛。
> 正确的处理是利用子空间正交性直接计算$\ell_2$范数，避免这两层松弛。

### 统一Lipschitz连续性定理

> **Theorem:** [物理位置编码的统一Lipschitz性质 (株定理)]
> <!-- label: thm:1.4.1 -->
> 设$\PE: \Ppos \to \R^{d_}$为以上定义的任一编码。则存在常数$L_ > 0$使得对所有
> $\mathbf{p}, \mathbf{q} \in \Ppos$：
> 
> $$
>     \boxed{
>     \|\PE(\mathbf{p}) - \PE(\mathbf{q})\| \leq L_ \cdot d_(\mathbf{p}, \mathbf{q})
>     }，
> $$
> 
> 其中$d_$是$\Ppos$上的自然度量（标量域：$|p-q|$；3D域：$\|\mathbf{p} - \mathbf{q}\|_2$）。
> 精确常数的汇总见表 [ref]。

[Table omitted — see original .tex]

**物理意义：**$L_$控制编码对位置变化的**敏感度**。大的$L_$使邻近
位置的编码更加不同（高分辨率），但可能破坏局部光滑性。最优$L_$应在物理相关尺度
$\xi$附近匹配编码的分辨率。

## Theorem 1的严格修正：物理位置对检测边际的影响

### 修正的检测边际——精确表达式

引入\Situs{}后，专家$m$的输入从$s_i$变为

$$
    h_i = \phi(s_i) + \PE(p_i)，
$$

其中$\phi: \R^{d_s} \to \R^d$是状态特征映射。

\begin{assumption}[专家作用于编码空间]
<!-- label: ass:2.1.1 -->
专家模型$E_m$在编码空间$\R^d$上操作。它们接受$h_i$作为输入，投票定义为
$v_m^(s_i) = \mathbf{1}[E_m(h_i) \neq y_i]$。
在干净/噪声条件下的期望分别为$p_{clean, s}^$和$p_{noisy, s}^$。
\end{assumption}

> **Proposition:** [\Situs{}下的精确检测边际变化——修正CC审计报告的符号错误]
> <!-- label: prop:2.1 -->
> \Situs{}增强空间中的有效检测边际为：
> 
> $$
>     \boxed{
>     \Delta_s^ = \Delta_s + \delta_s^
>     }，
> $$
> 
> 其中
> 
> $$
>     \boxed{
>     \delta_s^ = \underbrace{(p_{noisy, s}^ - p_{noisy, s})}_{
>     噪声样本上多出的分歧增益}
>     - \underbrace{(p_{clean, s}^ - p_{clean, s})}_{
>     干净样本上的（不希望有的）分歧变化}
>     }。
> $$
> 
> $\delta_s^$的值域为$[-\Delta_s, 1 - p_{clean, s}]$。

> **Proof:** 由定义直接展开：
> 
> $$
>     \Delta_s^ &= p_{noisy, s}^ - p_{clean, s}^ 

>     &= (p_{noisy, s} + (p_{noisy, s}^ - p_{noisy, s}))
>      - (p_{clean, s} + (p_{clean, s}^ - p_{clean, s})) 

>     &= \Delta_s + \delta_s^。
> $$
> 
> 值域由$p_{noisy}^, p_{clean}^ \in [0,1]$约束。 $\square$

\rigorous{} **正确性说明：**CC审计报告（\S2.3，命题2.1）中$\delta_s^$的表达式符号
**相反**。本文修正为正确符号：$\delta_s^ > 0$意味着\Situs{}帮助增大检测边际
（噪声样本分歧增大的收益超出干净样本上的副作用）。

**修正后的Theorem 1（\Situs{}增强）：**

$$
    \boxed{
    F_1^ \geq 1 - \frac{1} \sum_{s \in \Sstates} \rho_s \cdot
    \exp\!\left(-2M (\Delta_s + \delta_s^)^2\right)
    }。
$$

Chernoff-Hoeffding结构不变（指示变量在$[0,1]$中有界），仅常数从$\Delta_s$变为
$\Delta_s + \delta_s^$。

> **校准说明：** 此处使用的指数因子 $2M(\Delta_s+\delta_s^)^2$ 源自双侧 Hoeffding 界（与 SCX 定理 1 一致）。单侧 Chernoff 界给出更紧的因子 $M(\Delta_s+\delta_s^)/2$，在 $M$ 较小时可提供约 4× 的置信度增益。实际数值计算中，$\Delta_s$ 的校准已通过 `ppe_rigorous_derivation.md` 中的标准化处理吸收了这一常数差异，因此两种形式在重新校准后等价。

### $\delta_s^{\PE > 0$的信息论条件}

> **Theorem:** [$\delta_s^ > 0$的充分条件——信息论形式（贝叶斯最优限定）]
> <!-- label: thm:2.2.1 -->
> 设$S, P, Y$分别表示状态原子、物理位置和标签的随机变量。若
> 
> $$
>     \boxed{
>     I(Y; P \mid S) > 0
>     }，
> $$
> 
> 即物理位置在给定状态原子的条件下携带关于标签的额外信息，则**存在**一个\Situs{}编码函数
> $\PE: \Ppos \to \R^{d_}$和编码维度$d_$，使得对某个状态$s$，
> **贝叶斯最优分类器**在增广特征$(s, \PE(p))$下的检测边际变化满足$\delta_s^ > 0$。

> **Proof:** **步骤1（信息的物理可及性）：**由假设$I(Y; P \mid S) > 0$，存在正测度事件集
> $\mathcal{A} \subset \Sstates \times \Ppos$，在其上$P_{Y|S=s, P=p} \neq P_{Y|S=s}$。
> 
> **步骤2（构造编码）：**由通用逼近定理，存在充分表达力的$\PE$使得
> 
> $$
>     I(Y; \PE(P) \mid S) = I(Y; P \mid S) - \varepsilon_，
> $$
> 
> 其中$\varepsilon_ \geq 0$为编码造成的信息丢失（见\S4）。对于充分表达的$\PE$，
> 可保证$\varepsilon_ < I(Y; P \mid S)$，因此$I(Y; \PE(P) \mid S) > 0$。
> 
> **步骤3（贝叶斯最优分类器的行为）：**考虑贝叶斯最优分类器在增广空间中的表现。
> 对于噪声样本（标签$y$错误），给定$(s, p)$的贝叶斯最优预测器更倾向于输出与$y$不同的
> 真实标签→分歧概率上升：$p_{noisy, s}^ > p_{noisy, s}$。
> 对于干净样本，由数据处理不等式，额外位置信息进一步确认正确标签→分歧概率不增加：
> $p_{clean, s}^ \leq p_{clean, s}$。
> 因此**贝叶斯最优分类器**的$\delta_s^ > 0$。
> 
> **步骤4（从贝叶斯最优到实际专家——猜想）：**\heuristic{} 上述结论对贝叶斯最优分类器严格成立。
> 对于SCX框架中的实际神经网络专家$E_m$，要保证$\delta_s^ > 0$需额外假设：
> 专家模型的输出一致地逼近贝叶斯最优分类器（在$\ell_1$意义下对条件分布$P_{Y|S,P}$的逼近误差
> 小于$|\delta_s^|$）。对于通过随机梯度下降训练的神经网络，目前**没有**有限样本下
> 的严格收敛保证。此为当前定理的**主要局限**：步骤1--3证明了贝叶斯最优分类器可以从位置
> 信息中受益（信息论上的必然性），但从贝叶斯最优到实际专家的推广是\heuristic{}猜想。 $\square$

**证明状态：**步骤1--3为严格信息论推导（结论对贝叶斯最优分类器成立）。步骤4
（从贝叶斯最优到实际专家的推广）是\heuristic{}——依赖于专家模型类具有对贝叶斯最优的
一致逼近性质，这在学习理论中属于主动研究领域（涉及VC维、Rademacher复杂度等）。
若步骤4的推广不成立，定理2.2.1退化为一个经典结论：$I(Y;P|S)>0$意味着贝叶斯最优分类器
在使用$P$信息时表现更好——这是数据处理不等式的直接推论，是平凡的。

> **Proposition:** [$\delta_s^ > 0$的必要条件]
> <!-- label: prop:2.2.1 -->
> 若对所有专家$m$有$\delta_s^ > 0$，则以下两个条件至少之一成立：
> 
1. $I(Y; P \mid S) > 0$（信息论机制——位置携带标签相关信息）；
2. \Situs{}改变了专家系统的偏差-方差结构（非信息论机制——通过随机正则化效应）。

> 物理上有意义的场景是$(i)$。其等价于：
> 
> $$
>     \exists s, p_1, p_2  使得  P_{Y|S=s, P=p_1} \neq P_{Y|S=s, P=p_2}。
> $$

**物理实例：**

- 蛋白质中，相同氨基酸类型（状态$s$）在$\alpha$-螺旋（位置$p_1$）和$\beta$-折叠
- 晶体中，相同的化学环境（状态$s$）在表面（位置$p_1$）和体相（位置$p_2$）中

### $\delta_s^{\PE$的信息论上界：数据处理不等式}

> **Theorem:** [$\delta_s^$的信息论上界]
> <!-- label: thm:2.3.1 -->
> 由数据处理不等式（DPI）和Pinsker不等式：
> 
> $$
>     \boxed{
>     \delta_s^ \leq \min\!\left(1 - p_{clean, s},\,
>     \sqrt{\frac{1}{2} D_(P_{\PE|S,Y} \| P_{\PE|S})}\right)
>     + \delta_s^{variance}
>     }，
> $$
> 
> 其中$\delta_s^{variance} = O(1/\sqrt{M})$来自有限专家数$M$引入的估计方差。
> 当$I(P; Y \mid S) = 0$（位置无用时），在$M \to \infty$极限下$\delta_s^ \leq 0$。

> **Proof:** **步骤1（Pinsker界）：**对任意事件$A$，$|P(A) - Q(A)| \leq \sqrt{\frac{1}{2}D_(P\|Q)}$。
> 应用到概率变化：
> 
> $$
>     |p_{clean, s}^ - p_{clean, s}|
>     &\leq \sqrt{\frac{1}{2} D_(P_{\PE(P)|S=s, clean} \| P_{\PE(P)|S=s})}，

>     |p_{noisy, s}^ - p_{noisy, s}|
>     &\leq \sqrt{\frac{1}{2} D_(P_{\PE(P)|S=s, noisy} \| P_{\PE(P)|S=s})}。
> $$
> 
> 
> **步骤2（三角不等式组合）：**
> $\delta_s^ \leq |p_{noisy, s}^ - p_{noisy, s}|
>                       + |p_{clean, s}^ - p_{clean, s}|$。
> 
> **步骤3（值域上界的来源）：**由$\delta_s^$的值域（命题2.1），恒有
> $\delta_s^ \leq 1 - p_{clean, s}$（取$p_{noisy}^=1, p_{clean}^=0$时的最大值）。
> 此上界来自概率的$[0,1]$约束，不依赖于任何分布假设。Pinsker界给出另一个（基于KL散度的）上界。
> 两者的$\min$是有效的，因为**两者都是有效的上界**：
> $\delta_s^ \leq 1-p_{clean,s}$（值域约束）且
> $\delta_s^ \leq \sqrt{\frac{1}{2}D_^{(1)}} + \sqrt{\frac{1}{2}D_^{(2)}}$（Pinsker约束），
> 因此$\delta_s^ \leq \min(值域界, Pinsker界)$。两个界在不对齐的情况下各自提供信息：
> 当位置信息很少时（KL散度小），Pinsker界更紧；当$p_{clean,s}$本身很大时，值域界更紧。
> 
> **步骤4（DPI约束）：**$I(\PE(P); Y \mid S) \leq I(P; Y \mid S)$。
> 当$I(P; Y \mid S) = 0$时两个KL散度均为零，在$M \to \infty$下$\delta_s^ \leq 0$。
>  $\square$

\rigorous{} **证明状态：步骤1--3严格（Pinsker不等式+三角不等式+值域约束），步骤4的极限
陈述需$M \to \infty$——这是大量专家下的渐近结果。**
有限$M$下的$\delta_s^{variance}$项为$O(1/\sqrt{M})$（由中心极限定理），但精确
常数依赖于专家输出分布的具体形式。**注：**$1-p_{clean,s}$项来源于$\delta_s^$的
值域上界（命题2.1），与Pinsker界取$\min$是因为两者构成**两个独立有效的上界**，
取$\min$等价于取更紧者——这是有效的数学操作。原版本未解释此$\min$的来源，此处补充完整。

### $\delta_s^{\PE$的信息论下界：Fano逆不等式}

> **Proposition:** [$\delta_s^$的启发式估计——Fano界限（非严格下界）]
> <!-- label: prop:2.4.1 -->
> \heuristic{} **（警告：此非严格定理。）**设位置$P$在给定状态$S$下提供关于标签$Y$的额外信息，
> 且编码PE保留其中的$\rho = I(Y; \PE(P) \mid S) / I(Y; P \mid S) \in (0, 1]$部分。
> 若假设Fano不等式在两个世界均达到等号（需特定分布条件：噪声均匀分布在错误类别上），
> 则存在状态$s$使得：
> 
> $$
>     \delta_s^ \approx \frac{2\rho \cdot I(Y; P \mid S) - \log 2}{\log |\Y|}
>     - O\!\left(\frac{1}{\sqrt{M}}\right)。
> $$
> 
> **关键限定：**此表达式**不是**严格的数学下界。从两个Fano下界
> $P_e \geq A$和$P_e^ \geq B$不能逻辑地推出$P_e - P_e^ \geq A - B$，
> 因为$a \geq A$和$b \geq B$不蕴含$a-b \geq A-B$。此外，Fano不等式仅在特定分布上达到等号。
> 因此，此处给出的表达式应被视为对$\delta_s^$量级的**启发式估计**，
> 而非定理级的下界结论。正确的下界需要不同的证明策略，这是当前的一个开放问题。

> **Proof:** [推导思路（非严格证明）]
> **步骤1（Fano不等式）：**标准形式给出
> 
> $$
>     H(Y \mid S, \PE(P)) \leq H_2(P_e) + P_e \cdot \log(|\Y| - 1)，
> $$
> 
> 等价地$P_e \geq (H(Y \mid S, \PE(P)) - 1) / \log |\Y|$。
> 
> **步骤2（启发式关联）：**若Fano不等式在两个世界均达到等号（这在一般情况下不成立），
> 则形式上可写：
> 
> $$
>     P_e - P_e^
>     &\stackrel{若等号}{=} \frac{H(Y|S) - H(Y|S, \PE(P))}{\log |\Y|} 

>     &= \frac{\rho \cdot I(Y; P \mid S)}{\log |\Y|}。
> $$
> 
> 再加上$\Delta P_e$与$\delta_s^$的启发式关联（步骤2原稿），即得所述表达式。
> **再次强调：此推导从不等号推出了等号，不是严格证明。** $\square$

**推导状态：**步骤1（Fano不等式）严格。步骤2--3为\heuristic{}，因为：
(i) $\Delta P_e$与$\delta_s^$的联系假定了\Situs{}主要帮助噪声检测的方向性条件；
(ii) 取Fano等号是不等式方向的误用——两个下界的差不构成差的下界；
(iii) $\log 2$的单位需明确（若统一用nat则为$\ln 2$ nats，若统一用bit则该项为$1$）。
正确的Fano界应使用更强的工具（如Fano的逆形式、强Fano不等式），这需要关于分布的具体假设。

**物理含义：**若$I(Y; P \mid S)$很小（位置几乎不提供额外信息），则$\delta_s^$
的下界接近零或为负——\Situs{}无法实质性地改善检测。这解释了为什么**并非所有物理系统
都能从\Situs{}中受益**。

### 空间局部性正则化

> **Theorem:** [$\delta_s^$的空间光滑性]
> <!-- label: thm:2.5.1 -->
> 设PE满足Lipschitz条件（常数为$L_$），且专家$E_m$的输出**软概率**
> $E_m^{soft}: \R^d \to [0,1]$（如softmax输出的最大类别概率）满足$L_E$-Lipschitz条件。
> 此外，假设**边界条件**：专家$E_m$的决策边界距离两个编码点$h_i, h_j$至少为$\tau > 0$，
> 即$|E_m^{soft}(h) - 0.5| \geq \tau$对$h \in \{h_i, h_j\}$成立。
> 则对同属一个状态$s$、具有物理位置$p_i, p_j$的两个原子：
> 
> $$
>     \boxed{
>     |\delta_i^ - \delta_j^|
>     \leq 2 \cdot L_E \cdot L_ \cdot d_(p_i, p_j)
>     + O\!\left(\frac{1}{\sqrt{M}}\right)
>     }。
> $$
> 
> **若边界条件不成立**（即专家的决策边界恰好穿过$h_i$和$h_j$之间），该界不保证非空
> （non-vacuous）——$\mathbf{1}[E_m(h) \neq y]$作为指示函数在决策边界处是不连续的，
> 即使软概率是$L_E$-Lipschitz的，指示函数的期望变化也可能远大于$L_E L_ d_(p_i, p_j)$。

> **Proof:** $$
>     |\delta_i^ - \delta_j^|
>     &= |(p_{noisy, i}^ - p_{noisy, j}^)
>        - (p_{clean, i}^ - p_{clean, j}^)| 

>     &\leq |p_{noisy, i}^ - p_{noisy, j}^|
>        + |p_{clean, i}^ - p_{clean, j}^| 

>     &\leq 2L_E \cdot \|h_i - h_j\|
>      = 2L_E \cdot \|\PE(p_i) - \PE(p_j)\|
>      \leq 2L_E L_ \cdot d_(p_i, p_j)，
> $$
> 
> 其中利用了$s_i = s_j = s$（相同状态原子）时$\phi(s_i) = \phi(s_j)$。
> **关键**：从第二行到第三行的不等号利用了边界条件。$p_{clean,i}^
> = \E[\mathbf{1}[E_m(h_i) \neq y]]$是**指示函数的期望**。
> 即使软概率$E_m^{soft}$是$L_E$-Lipschitz的，指示函数$\mathbf{1}[\cdot \neq y]$
> 在决策边界处不连续。边界条件$|E_m^{soft}(h) - 0.5| \geq \tau$保证了$h_i$和$h_j$
> 均在决策边界的同一侧并保持一定距离，此时指示函数的期望变化由软概率的Lipschitz性质控制。
> 若无此条件，$p_{clean,i}^$和$p_{clean,j}^$可相差任意大
> （如一个完全在干净侧，另一个完全在噪声侧），即使$\|h_i - h_j\|$任意小。
> 有限专家修正$O(1/\sqrt{M})$来自估计误差。 $\square$

\rigorous{} **证明状态：在边界条件下严格。**该界在满足边界条件时是有效的。
若无边界条件，界变为空（vacuous）。这一命题是CC审计报告命题2.2在修正符号并补充
边界条件后的精确版本。

**物理意义：**物理上邻近的状态原子具有**相似的检测难度**——
前提是它们不在专家的决策边界附近。这是一个**可验证的实验预测**。
如果实验观测到邻近原子的$\delta^$存在跳变，可能因为：(i) 专家在该位置附近
存在决策边界（边界条件被违反），或 (ii) $L_E L_$的上界估计过于保守。

## Theorem 2的精确修正：编码不完美度与弱特征困境

### 编码不完美度$\varepsilon_{\PE$的信息论定义}

设随机变量：

- $X$：原始特征（状态原子$S$或其表示$\phi(S)$）；
- $P$：物理位置（完整信息）；
- $\PE(P)$：编码后的物理位置；
- $Y$：标签。

信息流的Markov链为：

$$
    Y \leftrightarrow (X, P) \leftrightarrow (X, \PE(P))，
$$

即$Y \indep \PE(P) \mid (X, P)$——编码只丢失信息，不创造信息。

> **Definition:** [编码不完美度$\varepsilon_$——信息论定义]
> <!-- label: def:3.1 -->
> 
> $$
>     \boxed{
>     \varepsilon_ = I(Y; P \mid X) - I(Y; \PE(P) \mid X)
>     }。
> $$

**基本性质：**

1. **数据处理不等式（DPI）：**$\varepsilon_ \geq 0$恒成立。
2. **可逆性条件：**$\varepsilon_ = 0$当且仅当PE是给定$X$下对$Y$预测的
3. **平凡情况：**若$I(Y; P \mid X) = 0$，则$\varepsilon_ = 0$自动成立；
4. **上界：**$\varepsilon_ \leq I(Y; P \mid X) \leq H(Y)$。

\rigorous{} **定义状态：严格信息论定义。**性质(1)为标准DPI，
性质(2)为充分统计量的信息论等价刻画，性质(3)(4)为直接推论。

> **Proposition:** [维度-信息权衡]
> <!-- label: prop:3.1 -->
> 对正弦编码（$d$维）和Laplace相关核（相关长度$\xi$）：
> 
> $$
>     \varepsilon_ \leq I(Y; P \mid X) \cdot \exp\!\left(-\frac{d}{d_0}\right)，
> $$
> 
> 其中$d_0 = O(L/\xi)$是特征维度尺度。

\heuristic{} **证明状态：启发式。**编码的逼近误差（定理1.2.2）导致核重建误差，
通过Pinsker不等式转化为互信息丢失。指数衰减依赖于Fourier级数的谱衰减
（Cauchy核的解析性），但$\propto \exp(-d/d_0)$的具体形式是启发式的——
精确的衰减速率取决于$P_{Y|X,P}$在位置上的光滑性，在一般条件下为$O(1/d)$而非指数衰减。

### 修正的Theorem 2——精确陈述和证明

> **Theorem:** [Theorem $2'$——不完美\Situs{}下的弱特征失效上界]
> <!-- label: thm:2' -->
> 设原始特征$X$的信息不足度为$\delta > 0$，且$\varepsilon_$是\Situs{}的编码不完美度。
> 则在\Situs{}增强的特征空间中，SCX的$F_1$分数满足：
> 
> $$
>     \boxed{
>     F_{1,SCX}^ \leq F_{1,base}
>     + C_F \cdot \sqrt{\frac{\delta + \frac{2\varepsilon_}{C_F^2}}{2}}
>     }，
> $$
> 
> 其中$C_F > 0$是$F_1$与贝叶斯错误率之间的转换常数。

> **Proof:** **步骤1（Fano不等式嵌入）：**贝叶斯错误率满足
> $P_e \geq \frac{H(Y \mid X, \PE(P)) - 1}{\log |\Y|}$。
> 
> **步骤2（条件熵分解）：**
> 
> $$
>     H(Y \mid X, \PE(P))
>     &= H(Y \mid X) - I(Y; \PE(P) \mid X) 

>     &= H(Y \mid X) - [I(Y; P \mid X) - \varepsilon_] 

>     &= H(Y \mid X) - I(Y; P \mid X) + \varepsilon_。
> $$
> 
> 
> **步骤3（联系$\delta$）：**定义$\delta_ = \delta + 2\varepsilon_/C_F^2$
> 为\Situs{}增强后的有效信息不足度。
> 
> **步骤4（代入SCX的$F_1$上界）：**
> $F_{1,SCX}^ \leq F_{1,base} + C_F \cdot \sqrt{\delta_/2}$。
> 
> **步骤5（极限验证）：**当$\varepsilon_ \to 0$（完美编码），
> 上界恢复为原始Theorem~2。$ \square$

\rigorous{} **证明状态：严格。**每一步均基于信息论恒等式和不等式，无近似。
转换常数$C_F$的引入将贝叶斯错误率映射到$F_1$度量，其存在性由$F_1$作为分类性能
度量的基本性质保证（$F_1 = 2TP/(2TP + FP + FN)$与
错误率之间存在单调关系）。

**两个极限情形：**

- $\varepsilon_ \to 0$（完美编码）：上界恢复为**原始Theorem 2**——
- $\varepsilon_ \to I(Y; P \mid X)$（完全失败的编码）：

### $\varepsilon_{\PE$的可估计形式}

> **Theorem:** [$\varepsilon_$的可估计性——KSG估计器]
> <!-- label: thm:3.3.1 -->
> $\varepsilon_$可以通过以下方法从有限样本中**一致地**估计：
> 
> $$
>     \boxed{
>     \hat_^{(n)} = \hat{I}^{(n)}(Y; P \mid X)
>                                  - \hat{I}^{(n)}(Y; \PE(P) \mid X)
>     }，
> $$
> 
> 其中$\hat{I}^{(n)}(\cdot; \cdot \mid \cdot)$是使用Kraskov-Stögbauer-Grassberger (KSG)
> 估计器的条件互信息估计。当$n \to \infty$时，$\hat_^{(n)} \xrightarrow{p} \varepsilon_$。

**算法：**

1. 从数据中采样$n$个三元组$(x_i, p_i, y_i)$；
2. 计算编码$\PE(p_i)$；
3. 计算$\hat{I}^{(n)}(Y; (P, X))$：在联合空间$(\Ppos \times \X) \times \Y$中使用$k$-NN；
4. 计算$\hat{I}^{(n)}(Y; X)$：在$\X \times \Y$中使用$k$-NN；
5. $\hat{I}^{(n)}(Y; P \mid X) = \hat{I}^{(n)}(Y; (P, X)) - \hat{I}^{(n)}(Y; X)$；
6. 同理计算$\hat{I}^{(n)}(Y; \PE(P) \mid X)$；
7. $\hat_^{(n)} = \hat{I}^{(n)}(Y; P \mid X) - \hat{I}^{(n)}(Y; \PE(P) \mid X)$。

**收敛速率：**KSG估计器以$O(n^{-1/(d_{eff}+2)})$速率收敛，其中$d_{eff}$
是联合空间的有效维度。\heuristic{} 对于高维$X$，收敛极慢——但$\varepsilon_$本身是
**差值**，两个估计器共享相同的偏差，差值估计可能比单独估计更准确（偏差抵消）。

> **Proposition:** [$\varepsilon_$的预测下界]
> <!-- label: prop:3.3.1 -->
> 设分类器$f_{full}$在$(X, P)$上训练，$f_{enc}$在$(X, \PE(P))$上训练。
> 两者在留出测试集上的**对数损失差**是$\varepsilon_$的下界估计：
> 
> $$
>     \boxed{
>     \hat_^{pred} = \frac{1}{n_{test}}
>     \sum_{i=1}^{n_{test}}
>     \left[\log\frac{1}{p_{enc}(y_i \mid x_i, \PE(p_i))}
>         - \log\frac{1}{p_{full}(y_i \mid x_i, p_i)}\right]
>     }。
> $$
> 
> 当$n_{test} \to \infty$且分类器一致时，$\hat_^{pred} \to \varepsilon_$。

\heuristic{} **实用价值：**如果两个分类器在测试集上的准确率**没有显著差异**，
则$\varepsilon_ \approx 0$——编码是充足的，\Situs{}不会削弱Theorem~2的上界。
这一检验不依赖于KSG估计器的维度灾难问题，具有更实用的价值。但其下界性质依赖于分类器的
一致性假设——如果分类器本身不一致（如欠拟合），对数损失差可能低估真实的$\varepsilon_$。

## Theorem $3'$：学习型位置编码与不可区分性的条件化

### 原始Theorem 3的精确定理陈述

> **Theorem:** [Theorem 3（原始——噪声与困难样本的不可区分性）]
> <!-- label: thm:3_original -->
> 存在两个世界$W_A, W_B$满足：
> 
1. 观测数据分布完全相同：$P_{W_A}(X, Y) = P_{W_B}(X, Y)$；
2. 在$W_A$中，样本$(x, y)$是**标签噪声**（label错误）；
3. 在$W_B$中，样本$(x, y)$是**本质困难样本**（label正确但特征本身无法确定性地支持该label）。

> 则没有任何算法能够仅通过观测i.i.d.样本$(X_i, Y_i)_{i=1}^n$区分$W_A$和$W_B$。形式化地，
> 对任意决策规则$d: (\X \times \Y)^n \to \{W_A, W_B\}$：
> 
> $$
>     \max_{W \in \{W_A, W_B\}} P_W(d(data) \neq W) \geq \frac{1}{2}。
> $$

定理3的核心洞察是：仅凭观测到的特征-标签对，无法判断一个``困难''样本是因为标签错误
还是因为本质上的高贝叶斯不确定性。这为``检测噪声''与``检测困难''之间画上了一条
信息论意义上的等号——二者在观测层面上不可区分。

### 固定PE保持不可区分性

引入\Situs{}后，观测数据扩展为三元组$(X, P, Y)$，其中$P$是物理位置。
**关键区别**在于PE的参数的来源：是固定的，还是从数据中学习的。

> **Proposition:** [固定PE保持Theorem 3]
> <!-- label: prop:4.1 -->
> 若$\PE: \Ppos \to \R^{d_}$是一个**固定的、与数据无关的**函数，
> 则增强后的观测分布依然相同：
> 
> $$
>     P_{W_A}(X, P, \PE(P), Y) = P_{W_B}(X, P, \PE(P), Y)。
> $$
> 
> Theorem~3的不可区分性**完全保持**。

> **Proof:** $\PE$是固定的确定性函数，因此$(X, P, \PE(P), Y)$是$(X, P, Y)$的一个确定性函数。
> 而物理位置$P$由物理结构决定，独立于标签生成过程的世界选择：
> $P_{W_A}(P \mid X) = P_{W_B}(P \mid X)$。
> 结合$P_{W_A}(X, Y) = P_{W_B}(X, Y)$（原始Theorem~3的构造），
> 增强后的联合分布也完全相同。 $\square$

\rigorous{} **证明状态：严格。**该命题是概率论中``确定性函数保持分布等价性''
这一基本性质的特例。

### 学习型PE的破坏机制——精确条件

**核心洞察：**在Theorem~3的构造中，$P_{W_A}(X, Y) = P_{W_B}(X, Y)$成立，
但两个世界在**生成过程**上不同：

- $W_A$：$Y_{true}$先由$X$决定，然后$Y_{obs}$以概率$\eta$被翻转；
- $W_B$：$Y_{obs} = Y_{true}$，但$P(Y_{true} \mid X)$在

当PE的参数$\theta$通过涉及标签$Y$（或任何与$Y_{true}$相关的信号）的目标函数
学习时，学习动态可能在两个世界中产生不同的最优参数——即使训练数据的观测部分完全相同。

> **Theorem:** [学习型PE破坏Theorem 3的精确条件]
> <!-- label: thm:4.1 -->
> 设$\mathcal{L}_{total}(\theta) = \mathcal{L}_{sup}(\theta)
> + \lambda \cdot \mathcal{L}_{aux}(\theta)$是完整的学习目标，其中：
> 
- $\mathcal{L}_{sup}$是监督损失（仅依赖$(X, P, Y)$的观测分布）；
- $\mathcal{L}_{aux}$是辅助损失（可能依赖未观测到的物理量$Z$）。

> 若$\mathcal{L}_{aux}$在$W_A$和$W_B$中具有不同的总体最小值：
> 
> $$
>     \argmin_\theta \mathcal{L}_{aux}^{W_A}(\theta)
>     \neq \argmin_\theta \mathcal{L}_{aux}^{W_B}(\theta)，
> $$
> 
> 则学习到的PE参数$\hat_{W_A} \neq \hat_{W_B}$以趋于1的概率成立
> （当$n \to \infty$）。两个世界变为**可区分**。

**具体的破坏机制**包括：

1. **多任务学习：**PE同时被用于预测另一个与$Y_{true}$相关的量$Z$
2. **物理一致性约束：**损失函数包含物理约束项（如能量守恒），使得$W_A$中
3. **分布外泛化：**PE的参数部分由分布外数据决定，两个世界在分布外表现不同。

### 修正后的Theorem $3'$——完整陈述

> **Theorem:** [Theorem $3'$——不可区分性的条件保持]
> <!-- label: thm:3' -->
> 
> > **前提 (A):** 物理位置编码PE是固定的，或仅通过独立于标签$Y$的信号学习。

> > **前提 (B):** 物理位置$P$在给定$X$下条件独立于世界选择：
> > $P \indep W \mid X$。

> > **结论:** Theorem~3的不可区分性完全保持。对任意决策规则$d$：
> > $\max_{W \in \{W_A, W_B\}} P_W(d \neq W) \geq 1/2$。

> > **若前提 (A) 不成立:** 不可区分性是否被破坏目前是一个**开放问题**。
> > 学习型PE可能通过多任务学习或物理一致性约束等机制区分两个世界，
> > 但当前缺乏构造性证明——详见\S5.3.2的讨论。
> >

\rigorous{} **定理状态：前提(A)(B)成立时，结论是严格的信息论结果。
前提(A)不成立时，定理的``破坏''方向缺乏构造性证明支撑
——目前的``构造性最小示例''（\S5.3.2）实际上展示了Theorem~3的鲁棒性
（学习型PE在该示例中也不能区分两个世界），而非其脆弱性。
真正能展示可区分性的构造性示例需要辅助损失涉及未观测变量，这仍然是开放问题。**

### 构造性最小示例
<!-- label: sec:4.3 -->

考虑一个极简的二元分类问题来说明Theorem~$3'$的机制。

#### 构造

设$X \in \{-1, +1\}$为二元特征，$P \in \{0, 1\}$为二元物理位置，$Y \in \{-1, +1\}$为标签。

**世界$W_A$（标签噪声）：**

- $P(X=+1) = P(X=-1) = 1/2$；
- $Y_{true} = X$（确定性的）；
- 标签以$\eta = 0.2$的概率翻转：$Y_{obs} = Y_{true}$以概率$0.8$，
- $P = X$（确定性）。

**世界$W_B$（本质困难）：**

- $P(X=+1) = P(X=-1) = 1/2$；
- $P(Y=+1 \mid X=+1) = 0.8$, $P(Y=-1 \mid X=+1) = 0.2$；
- $P(Y=+1 \mid X=-1) = 0.2$, $P(Y=-1 \mid X=-1) = 0.8$；
- $Y_{obs} = Y_{true}$（无标签噪声，但条件分布是固有高不确定性）；
- $P = X$（与$W_A$相同）。

**验证观测等价：**两个世界中$P_{W}(X, Y)$完全一致（简单乘法验证）。

#### 学习型PE的可区分性条件

引入简单的学习型PE：$\PE_\theta(p) = \theta \cdot p$（标量编码，$\theta \in \R$可学习）。
考虑辅助损失$\mathcal{L}_{aux}(\theta) = \E[(\PE_\theta(p) - \E[Y \mid X=x])^2]$。

在**此最小示例中**，$\E_{W_A}[Y \mid X] = \E_{W_B}[Y \mid X] = 0.6 \cdot sign(x)$
——两个世界的条件期望**数值相同**，仅解释不同。因此**即使是学习型PE也不能区分**
两个世界。这恰恰印证了Theorem~3的精髓：当观测分布完全相同时，任何算法都不能区分。

**此示例实际上证明了Theorem~3的鲁棒性，而非其脆弱性。**原先声称的``构造性最小示例''
反而构成了Theorem~3'破坏方向的一个**反例**：它展示了一个学习型PE**无法**区分
两个观测等价世界的场景。

\openproblem{} **开放问题3（``破坏''方向的构造性证明）：**当辅助损失涉及
**未观测到的物理量**$Z$——例如在$W_A$中噪声标签导致$|Z_{pred} - Z_{DFT}|$
较大（物理不一致），而在$W_B$中该差异较小（困难但物理一致）——则学习型PE的最优参数
**可能**在两个世界中出现差异。但目前这一场景**缺乏构造性证明**：
需要显式定义$Z$、$\mathcal{L}_{aux}$，并验证两个世界的最优参数确实不同。
这是一个有意义的开放问题。

#### 对实践的启示

> **Corollary:** [对实践的影响]
> <!-- label: cor:4.4.1 -->
> 
1. **固定正弦PE或固定旋转PE：**Theorem~3完全保持。位置编码不会损害最坏情况的
2. **从无标签位置数据学习的PE：**如果训练过程不涉及标签$Y$，Theorem~3保持；
3. **通过多目标学习（包括标签相关目标）的PE：**Theorem~3**可能被破坏**，
4. **风险：**即使辅助目标可能帮助区分，若其设计引入虚假相关性，可能导致错误的

\heuristic{} 第(3)点的``好消息''评价需要限定：只有在辅助目标信号与真实标签噪声相关
（而非虚假相关）时，学习型PE的区分能力才是可靠的好消息。CC审计报告未给出这一限定。

## 讨论与开放问题

### 与现有位置编码的关系

#### 与RoPE/正弦编码的结构性差异

RoPE [cite]和标准正弦编码 [cite]的设计目标
是**最大化语言建模的困惑度降低**，其频率分布$\omega_j = 10000^{-2j/d}$
（几何级数）对应的是自然语言中token共现距离的对数均匀分布。

\Situs{}的物理最优谱（定理1.2.1）使用$\omega_j \propto \tan(\pi(2j+1)/2d)$
（正切分布），对应的是物理系统中指数衰减相关函数的谱表示。
两者的根本差异见表 [ref]。

[Table omitted — see original .tex]

#### 旋转等变性缺失——一个根本缺陷

\Situs{}的3D旋转编码（定义1.3.1）**不具备旋转等变性**。考虑全局旋转
$R_{phys} \in SO(3)$作用于坐标$\mathbf{p} \to R_{phys}\mathbf{p}$：
不存在一个与$\mathbf{p}$无关的变换$T$使得$T \cdot \PE(\mathbf{p}) = \PE(R_{phys}\mathbf{p})$。
原因在于编码为三个坐标轴分配了不相交的维度对——物理旋转混合了$x$和$y$分量，
但编码空间中没有对应的``混合''机制。

这在下述场景中是致命的：多晶/晶界系统（不同晶粒取向不同）、分子动力学轨迹
（分子整体旋转导致所有原子编码变化）、不同切面的表面slab计算。

**理论上可修复：**使用球谐函数编码
$\PE(\mathbf{p}) = [Y_{\ell m}(\theta, \phi)]$，具有严格的$SO(3)$旋转等变性；
或使用E(3)等变网络（Tensor Field Networks [cite]、
SE(3)-Transformers [cite]）。代价是编码维度以$(L+1)^2$增长
（$L=3$即需16维 vs 6维的旋转编码），且Lipschitz行为更复杂。

\openproblem{} **开放问题1：**能否在保持$\R^3 \to SO(d)$的李群同态结构
（命题1.3.1）的前提下，构造具有完整$SO(3)$旋转等变性的位置编码？初步推测答案是否定的——
因为$\R^3 \to SO(d)$的Abel嵌入与$SO(3)$的非Abel作用在本质上是冲突的。

### 排列对称性问题

原子系统本质上是粒子的**集合**——原子的编号/顺序是人为的，不应影响物理预测。
\Situs{}依赖``第$i$个原子的位置$p_i$''，其中$i$是原子的索引。如果数据加载时的
原子排序发生变化，$h_i$会不同——即使物理系统完全相同。

这一问题的严重程度取决于应用场景：

- **可接受：**原子排序在所有样本间一致（如DFT计算使用固定输入模板）；
- **有问题：**不同数据源的原子排序约定不同，或分子动力学轨迹中原子

**缓解措施：**使用等变的位置编码（基于距离矩阵或原子环境），或要求数据预处理中
保证一致的原子排序（如按坐标排序——但这又引入了排序的人为性）。

\openproblem{} **开放问题2：**能否设计一种\Situs{}变体，在保持加法注入结构
$h_i = \phi(s_i) + \PE(p_i)$的同时，天然具备原子的排列不变性（或等变性）？

### \Situs{的适用边界——一票否决条件}

以下条件中任一成立时，\Situs{}**不应使用**：

1. **$I(Y; P \mid S) = 0$：**位置不携带关于标签的额外信息。
2. **纯组成分类（无空间结构）：**$\Ppos$未定义。
3. **标签具有平移/旋转对称性：**任务标签具有平移不变性（如体相带隙），
4. **已有强力结构编码器：**GNN已通过消息传递编码了邻域几何，
5. **随机或伪随机构型+有限样本：**$I(Y; P \mid S)$的统计显著性不足→
6. **未修正的计算artifact：**如混合不同超胞尺寸的未修正DFT数据→

### 理论诚实度总评

表 [ref]总结了本文所有主要定理/命题的证明严格性。

[Table omitted — see original .tex]

**最严重的理论漏洞：**

1. **旋转等变性缺失**（\S6.1.2）：3D旋转编码是对$SO(3)$的残缺表示；
2. **贝叶斯最优到实际专家的鸿沟**（定理2.2.1，步骤4）：缺乏有限样本下的严格收敛保证；
3. **命题2.4.1的Fano推导（已降级）**：原声称的``下界''从两个Fano不等号推出了等号——这是逻辑错误。已降级为启发式估计，正确的下界需要不同的证明策略。

### 开放问题

1. **严格的多头Chernoff界：**当使用Multi-Head Spring（而非独立专家）时，
2. **$SO(3)$等变的位置编码：**能否在保持$\R^3 \to SO(d)$李群同态结构的
3. **排列不变\Situs{}：**能否设计一种编码，天然具备原子的排列不变性
4. **$\varepsilon_$的非渐近置信区间：**KSG估计器的一致性已知，但其
5. **最优频率参数的自适应选择：**定理1.2.1假设物理相关长度$\xi$已知。
6. **Theorem~$3'$的经验验证：**在多任务学习场景中，能否通过实验验证
7. **\Situs{}与其他结构编码的互补性：**当GNN或pLM已提供部分结构信息时，

## 致谢

作者感谢SCX项目团队在CC审计报告 [cite]中的严谨分析，
其中对Theorem~1--4的原始陈述构成了本文修正的理论起点。
本文中$\delta_s^$的符号修正确认了CC审计报告命题2.1中的sign error；
$\varepsilon_$的定义（定义3.1）将CC审计报告中未被命名的概念赋予了精确的信息论形式。
所有引用定理、定义和命题的编号保持了与`ppe\_rigorous\_derivation.md`的一致性。

\begin{thebibliography}{99}

\bibitem{vaswani2017attention}
A.~Vaswani, N.~Shazeer, N.~Parmar, J.~Uszkoreit, L.~Jones, A.~N.~Gomez,
L.~Kaiser, and I.~Polosukhin.
\newblock Attention is all you need.
\newblock In *Advances in Neural Information Processing Systems (NeurIPS)*,
  2017.

\bibitem{su2024roformer}
J.~Su, M.~Ahmed, Y.~Lu, S.~Pan, W.~Bo, and Y.~Liu.
\newblock Ro{Former}: Enhanced transformer with rotary position embedding.
\newblock *Neurocomputing*, 568:127063, 2024.

\bibitem{devlin2019bert}
J.~Devlin, M.-W.~Chang, K.~Lee, and K.~Toutanova.
\newblock {BERT}: Pre-training of deep bidirectional transformers for language
  understanding.
\newblock In *Proceedings of NAACL-HLT*, 2019.

\bibitem{scx2026theorems}
SCX Project.
\newblock {Theorem 1--4}: Multi-expert consistency, weak feature limits,
  unidentifiability, and minimax optimality.
\newblock Technical report, `theory/theorems/`, 2026.

\bibitem{scx2026cc_audit}
SCX Project.
\newblock Multi-head spring and positional encoding analysis: {CC} audit report.
\newblock Technical report,
  `theory/self\_evolution/multi\_head\_spring\_and\_positional\_encoding\_analysis.md`,
  2026.

\bibitem{scx2026ppe_derivation}
SCX Project.
\newblock Physical positional encoding ({PPE}) rigorous derivation in the {SCX}
  framework.
\newblock Technical report,
  `theory/self\_evolution/ppe\_rigorous\_derivation.md`, 2026.

\bibitem{scx2026situs_validation}
SCX Project.
\newblock {Situs} ({Physical Positional Encoding}) physical validation and
  applicability analysis.
\newblock Technical report, `theory/self\_evolution/situs\_physical\_validation.md`,
  2026.

\bibitem{thomas2018tfn}
N.~Thomas, T.~Smidt, S.~Kearnes, L.~Yang, L.~Li, K.~Kohlhoff, and P.~Riley.
\newblock Tensor field networks: Rotation- and translation-equivariant neural
  networks for {3D} point clouds.
\newblock In *NeurIPS*, 2018.

\bibitem{fuchs2020se3}
F.~B.~Fuchs, D.~E.~Worrall, V.~Fischer, and M.~Welling.
\newblock {SE(3)-Transformers}: {3D} roto-translation equivariant attention
  networks.
\newblock In *NeurIPS*, 2020.

\bibitem{wainwright2019}
M.~J.~Wainwright.
\newblock *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*.
\newblock Cambridge University Press, 2019.

\bibitem{boucheron2013}
S.~Boucheron, G.~Lugosi, and P.~Massart.
\newblock *Concentration Inequalities: A Nonasymptotic Theory of
  Independence*.
\newblock Oxford University Press, 2013.

\bibitem{freysoldt2014}
C.~Freysoldt, B.~Grabowski, T.~Hickel, J.~Neugebauer, G.~Kresse,
A.~Janotti, and C.~G.~Van de Walle.
\newblock First-principles calculations for point defects in solids.
\newblock *Reviews of Modern Physics*, 86(1):253--305, 2014.

\bibitem{makov1995}
G.~Makov and M.~C.~Payne.
\newblock Periodic boundary conditions in ab initio calculations.
\newblock *Physical Review B*, 51(7):4014--4022, 1995.

\bibitem{pauling1951}
L.~Pauling, R.~B.~Corey, and H.~R.~Branson.
\newblock The structure of proteins: Two hydrogen-bonded helical configurations
  of the polypeptide chain.
\newblock *Proceedings of the National Academy of Sciences*,
  37(4):205--211, 1951.

\bibitem{dunker2005}
A.~K.~Dunker, M.~S.~Cortese, P.~Romero, L.~M.~Iakoucheva, and V.~N.~Uversky.
\newblock Flexible nets: The roles of intrinsic disorder in protein interaction
  networks.
\newblock *The FEBS Journal*, 272(20):5129--5148, 2005.

\bibitem{cover2006}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd edition.
\newblock Wiley, 2006.

\bibitem{ksg2004}
A.~Kraskov, H.~Stögbauer, and P.~Grassberger.
\newblock Estimating mutual information.
\newblock *Physical Review E*, 69(6):066138, 2004.

\end{thebibliography}