# SCX猜想分析：C7（湍流模空间维度）与 C8（审计瞬子高维推广 k>1）

> **日期**: 2026-07-02
> **状态**: 推导与形式化证明（含关键阻塞识别）
> **基于**: scx_open_problems/main.tex §1 (C7), scx_instanton/audit_instanton.tex (C8), scx_turbulence/main.tex (补充)

---

## 目录

1. [C7: 湍流规范模空间——维度公式推导与可观测量分类](#c7)
2. [C8: 审计瞬子高维推广——2-形式通量与H₂分析](#c8)
3. [总结与交叉关联](#cross)

---

## 1. C7: 湍流规范模空间——维度公式推导 {#c7}

### 1.1 源材料回顾

从 `scx_open_problems/main.tex` §1（猜想 `conj:turbulence`）：

> 设 $\mathcal{F}$ 为满足 Navier-Stokes 方程的所有湍流模型构成的函数空间。设 $\mathcal{G}$ 为作用在 $\mathcal{F}$ 上的规范群。湍流规范模空间定义为：
> $$\mathcal{T}_{\text{mod}} \equiv \mathcal{F} / \mathcal{G}$$
>
> 猜想：$\dim \mathcal{G} \approx \log(Re^{3/4})$

任务：从第一原理推导 $\dim(\mathcal{T}_{\text{mod}}) \sim \log(Re^{3/4})$，分析规范不变 vs 规范依赖可观测量，并显式构造 k-ε、k-ω、LES 三种模型的模空间对应。

---

### 1.2 Kolmogorov 尺度与惯性子区自由度

#### 1.2.1 Kolmogorov 标度的第一原理推导

不可压缩 Navier-Stokes 方程：

$$\partial_t \mathbf{v} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\nabla p + \nu \nabla^2 \mathbf{v} + \mathbf{f}, \quad \nabla \cdot \mathbf{v} = 0$$

定义三个基本尺度：

| 符号 | 名称 | 物理意义 |
|------|------|----------|
| $L$ | 积分尺度 (Integral scale) | 能量注入的最大尺度，$\sim$ 几何尺寸 |
| $\eta$ | Kolmogorov 尺度 | 耗散截止尺度，黏性主导 |
| $u'$ | 脉动速度 RMS | $\langle |\mathbf{v}'|^2 \rangle^{1/2}$ |

Reynolds 数：$Re = \dfrac{u' L}{\nu}$

Kolmogorov (1941) 的维度分析：耗散尺度 $\eta$ 仅依赖于 $\varepsilon$（能量耗散率）和 $\nu$（运动黏度）。量纲分析：

$$[\varepsilon] = \text{m}^2/\text{s}^3, \quad [\nu] = \text{m}^2/\text{s}$$

构造 $\eta = \nu^a \varepsilon^b$，维度匹配 → $a = 3/4, b = -1/4$：

$$\boxed{\eta = \left(\frac{\nu^3}{\varepsilon}\right)^{1/4}}$$

积分尺度的耗散率估计：$\varepsilon \sim u'^3 / L$。代入：

$$\eta = \left(\frac{\nu^3 L}{u'^3}\right)^{1/4} = L \cdot \left(\frac{\nu}{u' L}\right)^{3/4} = L \cdot Re^{-3/4}$$

因此：

$$\boxed{\frac{L}{\eta} = Re^{3/4}}$$

#### 1.2.2 惯性子区的自由度计数

湍流能谱在惯性子区满足 Kolmogorov $-5/3$ 律：

$$E(k) = C_K \varepsilon^{2/3} k^{-5/3}, \quad k \in \left[\frac{2\pi}{L}, \frac{2\pi}{\eta}\right]$$

惯性子区跨越的波数范围（以 $e$ 为底的对数尺度）：

$$N_{\text{decades}} = \ln\left(\frac{2\pi/\eta}{2\pi/L}\right) = \ln\left(\frac{L}{\eta}\right) = \ln(Re^{3/4}) = \frac{3}{4}\ln(Re)$$

在物理上，每个 $e$-fold 的波数区间构成一个独立的自由度——因为该区间内的 Fourier 模态在动力学上是耦合的，但不同 $e$-fold 之间的耦合随分离度指数衰减。

三维空间中，每个波数壳层 $[k, k+dk]$ 包含 $\sim k^2 dk$ 个模态。总的活跃自由度为：

$$N_{\text{dof}} \sim \int_{2\pi/L}^{2\pi/\eta} k^2 dk \sim \left(\frac{L}{\eta}\right)^3 = Re^{9/4}$$

但模空间维度不是 $N_{\text{dof}}$——我们关心的是**独立规范参数**的数量。

---

### 1.3 模空间维度 $\dim(\mathcal{T}_{\text{mod}})$ 的推导

#### 1.3.1 规范群的构造

湍流模型的**状态空间**：

$$\mathcal{U} = \{(\mathbf{v}, \tau) \mid \mathbf{v} \text{ 满足 N-S}, \; \tau \text{ 为 Reynolds 应力张量}\}$$

规范群 $\mathcal{G}$ 定义为保持所有物理可观测量不变的 $\mathcal{U}$ 上的变换群：

$$\mathcal{G} = \{\phi: \mathcal{U} \to \mathcal{U} \mid O \circ \phi = O,\; \forall \text{ 规范不变可观测量 } O\}$$

#### 1.3.2 规范自由度的物理来源

湍流模型的规范自由度来自于：能谱 $E(k)$ 的**参数化冗余**。具体来说，任何湍流模型需要指定：

1. **耗散谱的形状**（$k \gtrsim 2\pi/\eta$ 区域）——模型依赖
2. **能量-containing 区的形状**（$k \lesssim 2\pi/L$ 区域）——边界条件依赖
3. **惯性子区的截断方式**——规范固定的核心自由度

物理真值（DNS 极限）具有唯一的 $E(k)$。但任何有限分辨率模型只能分辨到某个截止波数 $k_c \sim 2\pi/h$（$h$ 为网格尺度），$k > k_c$ 的贡献必须以模型（即规范固定）方式参数化。

**核心论证**：在波数空间的对数坐标中，惯性子区 $[\ln(2\pi/L), \ln(2\pi/\eta)]$ 是一个区间。规范固定等价于选择该区间的一个**划分**——决定哪些模态被显式分辨、哪些被建模。

划分的选择自由度 = 区间被划分的段数 = 惯性子区中独立的参数化选择数。

每个独立的参数化选择对应一个规范参数。在惯性子区中，$E(k)$ 的形式为 $C_K \varepsilon^{2/3} k^{-5/3}$，其中 $C_K \approx 1.5$ 是 Kolmogorov 常数（近似普适的）。但：
- 当从一个 $k$ 区域过渡到另一个时，$C_K$ 的有效值可能有微小变化（间歇性修正）
- 每个这样的变化对应一个独立可调的规范参数

独立规范参数的数量 $\sim$ 惯性子区跨越的对数尺度数：

$$\boxed{\dim(\mathcal{G}) \approx \ln\left(\frac{L}{\eta}\right) = \ln(Re^{3/4})}$$

模空间的维度（去掉规范自由度后剩余的物理自由度）为：

$$\dim(\mathcal{T}_{\text{mod}}) = \dim(\mathcal{F}) - \dim(\mathcal{G})$$

其中 $\dim(\mathcal{F})$ 是所有可能湍流模型的函数空间维度（无限维）。模空间 $\mathcal{T}_{\text{mod}}$ 本身是无限维的（因为物理可观测量的空间是无限维的——能谱 $E(k)$ 是 $k$ 的连续函数），但**可调规范参数是有限维的**：

$$\dim(\mathcal{G}) \sim \frac{3}{4}\ln(Re)$$

#### 1.3.3 物理解释

当 $Re \to \infty$ 时，$\dim(\mathcal{G}) \to \infty$，意味着：
- 惯性子区无限延伸
- 规范固定的方式有无穷多种
- 不同湍流模型之间的差异在 $Re \to \infty$ 极限下不可消除

当 $Re$ 有限时，$\dim(\mathcal{G})$ 有限，意味着：
- 惯性子区长度有限
- 本质上只有有限多种不等价的湍流模型
- DNS 在 $Re$ 足够低（层流/过渡流）时是可达的（$\dim(\mathcal{G}) \to 0$）

---

### 1.4 规范不变 vs. 规范依赖可观测量

#### 1.4.1 规范不变可观测量（物理的）

这些量直接由 N-S 方程的对称性和 Kolmogorov 标度假设导出，**不依赖**具体的封闭假设：

| 可观测量 | 符号 | 不变性来源 |
|----------|------|-----------|
| 平均能量耗散率 | $\varepsilon = 2\nu \langle S_{ij}S_{ij} \rangle$ | N-S 方程直接蕴含 |
| 能谱幂律指数 | $\beta$ in $E(k) \sim k^{-\beta}$ | Kolmogorov 标度普适性 |
| 间歇性指数 | $\zeta_p$ in $\langle (\delta v)^p \rangle \sim r^{\zeta_p}$ | 反常标度的普适性 |
| 整体阻力系数 | $C_D$ | 集总参数对细节不敏感 |
| 整体传热系数 | $Nu$ | 集总参数对细节不敏感 |
| 各向异性张量不变量 | $II_b, III_b$ (Lumley 三角形) | 湍流状态的拓扑分类 |

**证明概要**（规范不变量分类定理，来自 `scx_open_problems/main.tex`）：
> 对于充分发展的均匀各向同性湍流，规范不变的可观测量恰好是那些可以仅用 N-S 方程的对称性和 Kolmogorov 标度假设导出的量。任何需要具体封闭假设的量是规范依赖的。

#### 1.4.2 规范依赖可观测量（模型特定的）

这些量的值依赖于选择哪个湍流模型（即哪种规范固定）：

| 可观测量 | 符号 | 依赖的规范参数 |
|----------|------|---------------|
| 涡粘系数 | $\nu_t(x, t)$ | $C_\mu$, 模型选择 |
| 局部湍动能 | $k(x, t)$ | 封闭假设 |
| 壁面函数形状 | $u^+(y^+)$ | 壁面模型的规范固定 |
| 湍流普朗特数 | $\sigma_t$ | 模型特定常数 |
| 模型常数 | $C_\mu, C_{\varepsilon 1}, C_{\varepsilon 2}, \sigma_k, \sigma_\varepsilon$ | 校准数据依赖 |

---

### 1.5 三种湍流模型的模空间显式构造

#### 1.5.1 k-ε 模型

**规范固定条件**（Boussinesq 涡粘假设）：

$$\tau_{ij} = 2\nu_t S_{ij} - \frac{2}{3}k\delta_{ij}, \quad \nu_t = C_\mu \frac{k^2}{\varepsilon}$$

规范参数：$\{C_\mu, C_{\varepsilon 1}, C_{\varepsilon 2}, \sigma_k, \sigma_\varepsilon\}$

标准值（Launder & Spalding, 1974）：
$$C_\mu = 0.09,\; C_{\varepsilon 1} = 1.44,\; C_{\varepsilon 2} = 1.92,\; \sigma_k = 1.0,\; \sigma_\varepsilon = 1.3$$

这些参数是**规范固定的残余**——它们不是物理常数，而是特定规范选择下的校准结果。改变 $C_\mu \to C_\mu + \delta C_\mu$ 对应模空间中的不同点，只要所有规范不变可观测量保持不变。

**模空间坐标**：k-ε 在 $\mathcal{T}_{\text{mod}}$ 中对应一个 $5$ 维的子流形（由 5 个规范参数参数化），但所有这些点都属于同一个规范等价类——即"使用 k-ε 模型类"这一选择本身是规范轨道的一个截断。

#### 1.5.2 k-ω SST 模型

**规范固定条件**：

$$\nu_t = \frac{a_1 k}{\max(a_1 \omega, SF_2)}$$

其中 $\omega = \varepsilon/(C_\mu k)$ 是比耗散率。与 k-ε 的关键区别：
- k-ε 通过 $\varepsilon$ 输运方程封闭
- k-ω 通过 $\omega$ 输运方程封闭

在模空间中，k-ε 与 k-ω 通过变量变换 $\omega = \varepsilon/(C_\mu k)$ 相联系。在惯性子区（均匀湍流），两种模型等价映射——它们属于模空间的**同一点**。但在壁面附近，k-ω 的混合函数 $F_1, F_2$ 引入了不同的规范固定，使得两者在近壁区是**不同的规范等价类代表元**。

**规范参数**：$\{\beta^*, \beta, \sigma_k, \sigma_\omega, a_1\}$ 以及混合函数的切换参数。

#### 1.5.3 LES (Smagorinsky) 模型

**规范固定条件**：

$$\tau_{ij} = -2(C_s \Delta)^2 |\bar{S}| \bar{S}_{ij}$$

规范参数：$C_s$（Smagorinsky 常数，通常 $C_s \approx 0.1-0.2$）和过滤器宽度 $\Delta$。

**与 RANS 的本质区别**：LES 的规范固定发生在**不同的截断尺度**上。RANS 在 $\Delta \gg \eta$（系综平均）处截断，而 LES 在 $\Delta \sim O(10\eta)$ 处截断。

在模空间中：
- DNS：$\Delta \sim \eta$，规范参数个数 $\to 0$（无模型）
- LES：$\Delta \sim \lambda$（Taylor 微尺度），少量规范参数
- RANS：$\Delta \sim L$，最多规范参数

**规范参数数量与截断尺度的关系**：

$$N_{\text{gauge}} \sim \ln\left(\frac{L}{\Delta}\right)$$

当 $\Delta = \eta$（DNS），$N_{\text{gauge}} = 0$（无规范固定）。
当 $\Delta = L$（RANS），$N_{\text{gauge}} \sim \ln(Re^{3/4})$（最多规范固定）。

#### 1.5.4 模空间的几何结构

$$\mathcal{T}_{\text{mod}} = \mathcal{F} / \mathcal{G}$$

可以赋予 Riemann 度量：

$$d([M_1], [M_2]) = \inf_{\phi_1, \phi_2 \in \mathcal{G}} \| \phi_1(M_1) - \phi_2(M_2) \|_{\mathcal{F}}$$

其中 $\|\cdot\|_{\mathcal{F}}$ 可取为观测空间上的 $L^2$ 范数。

在该度量下：
- 同一规范轨道内的模型距离为 0
- DNS 和 LES 之间的距离 $\sim$ 亚格子尺度建模的误差
- k-ε 和 k-ω 在均匀湍流区域的距离为 0，在壁面区域距离 $> 0$

模空间的拓扑依赖于 $\mathcal{M}$（Situs 流形）和 $Re$。对于简单几何（平板边界层）和固定 $Re$，$\mathcal{T}_{\text{mod}}$ 是连通的（所有模型之间可以连续变形）。对于复杂几何，可能存在**不同的连通分支**，对应拓扑上不等价的规范选择。

---

### 1.6 从 scx_turbulence 的补充视角

`scx_turbulence/main.tex` 提出了湍流的**不可辨识性定理**：在有限分辨率 $h$ 下，真实湍流 $\mathbf{u}_{\text{NS}}$ 和截断误差伪影 $\mathbf{u}_N$ 是不可区分的：

$$\text{TV}(P_h^{\mathcal{W}_A}, P_h^{\mathcal{W}_B}) \leq C \cdot h^{\alpha}$$

其中对 Kolmogorov 湍流 $\alpha = 1/3$。

这为模空间提供了新解释：**规范固定的本质是对不可辨识性的明确声明**——选择一个模型等价于声明"在分辨率 $h$ 以下，我选择这种特定方式处理不可辨识的自由度"。模空间 $\mathcal{T}_{\text{mod}}$ 是所有可能不可辨识性处理方式的等价类空间。

---

## 2. C8: 审计瞬子高维推广——2-形式通量与 $H_2$ 分析 {#c8}

### 2.1 源材料回顾

从 `scx_instanton/audit_instanton.tex` 开放问题 OP2（§9）：

> **Higher-dimensional audit instantons / 高维审计瞬子**: Can the definition be extended to $k$-cycles for $k \geq 2$? A "2-audit instanton" would correspond to a 2-cycle (void/bubble) in the density filtration, representing a region where expert consensus *encloses* a systematically wrong prediction volume.

核心任务：
1. 在 2-骨架 (2-skeleton) 上定义审计 2-形式 $F = d_1 A$
2. 定义通过 2-圈 $\Sigma$ 的通量 $\int_\Sigma F$
3. 证明该通量是否可以非零（与 $k=1$ 的情形对比）

---

### 2.2 回顾：$k=1$ 的情形（审计瞬子 1-圈）

#### 2.2.1 已知的构造

Situs 流形 $(\mathcal{M}, \rho, \mathcal{E})$ 上：
- 平均有符号偏离：$\bar{f}(x) = \frac{1}{M}\sum_{i=1}^M f_i(x)$
- 审计 1-形式：$A = d_0 \bar{f} \in \Omega^1(\mathcal{M})$
- 1-圈 $\gamma$ 上的**和乐**（环量）：$\Phi(\gamma) = \oint_\gamma A$

**关键性质**：
- $d_1 A = d_1 d_0 \bar{f} = 0$（自动闭性，命题 3.1）
- 当 $\bar{f}$ 具有**单值性**（monodromy）时，$\Phi(\gamma) \neq 0$
- 即：$A$ 局部恰当（$A = d_0 g_p$ 在每个局部片 $U_p$ 上），但全局非恰当（$\oint_\gamma A \neq 0$ 意味着 $\bar{f}$ 不是全局单值函数）

#### 2.2.2 和乐非零的拓扑本质

$\Phi(\gamma) \neq 0$ 意味着 $\bar{f}$ 绕 $\gamma$ 一周后有净增量。这类似：
- 复分析中对数函数的单值性：$\oint_{|z|=1} \frac{dz}{z} = 2\pi i$
- 规范理论中的 Wilson 圈：$\oint_\gamma A_\mu dx^\mu$
- Berry 相位

---

### 2.3 $k=2$ 的构造：审计 2-形式 $F = d_1 A$

#### 2.3.1 定义

根据外微分运算的自然推广，定义**审计 2-形式**：

$$\boxed{F = d_1 A \in \Omega^2(\mathcal{M})}$$

在局部坐标 $\{x^\mu\}$ 中：
$$F = d_1\left(\sum_\mu \frac{\partial \bar{f}}{\partial x^\mu} dx^\mu\right) = \sum_{\mu < \nu} \left(\frac{\partial^2 \bar{f}}{\partial x^\mu \partial x^\nu} - \frac{\partial^2 \bar{f}}{\partial x^\nu \partial x^\mu}\right) dx^\mu \wedge dx^\nu$$

#### 2.3.2 核心结果：$F$ 恒为零

**定理 1（审计 2-形式的平凡性）**：审计 2-形式 $F = d_1 A$ 在 $\mathcal{M}$ 上恒为零：

$$\boxed{F = d_1 A = d_1(d_0 \bar{f}) = 0}$$

**证明**：由 de Rham 复形的核心恒等式 $d_{k+1} \circ d_k = 0$（即 $d^2 = 0$），取 $k=0$ 得 $d_1 \circ d_0 = 0$。

$$F = d_1 A = d_1(d_0 \bar{f}) = (d_1 \circ d_0)(\bar{f}) = 0$$

由于 $\bar{f}$ 是 $C^\infty$ 函数（至少在局部），混合偏导数可交换（$\partial_\mu \partial_\nu \bar{f} = \partial_\nu \partial_\mu \bar{f}$），因此所有 $F_{\mu\nu} \equiv 0$。$\square$

#### 2.3.3 通量恒为零

**推论 1（2-圈通量的平凡性）**：对任何 2-圈 $\Sigma \subset \mathcal{M}$（闭曲面，$\partial\Sigma = \emptyset$），审计通量恒为零：

$$\boxed{\int_\Sigma F = \int_\Sigma d_1 A = 0}$$

**证明**：直接由 $F = 0$ 得出。另外也可通过 Stokes 定理验证：即使 $F \neq 0$，对闭曲面也有 $\int_\Sigma d_1 A = \oint_{\partial\Sigma} A$，而 $\partial\Sigma = \emptyset$ 意味着积分为 0。但在我们的情形中 $F = 0$ 更强。$\square$

对于有边界的 2-链 $\Sigma$（$\partial\Sigma = \gamma$），由 Stokes 定理：
$$\int_\Sigma F = \int_\Sigma d_1 A = \oint_{\partial\Sigma} A = \oint_\gamma A$$

这恰好回归到 $k=1$ 的和乐。所以 $F$ 在 2-链上的积分不提供新信息——它只是 1-圈和乐的不同表达。

---

### 2.4 为什么 $k=2$ 通量恒为零？（与 $k=1$ 的根本对比）

#### 2.4.1 $k=1$ 非零的本质

$k=1$ 的和乐 $\Phi(\gamma) = \oint_\gamma A \neq 0$ 是可能的，因为：

$$\oint_\gamma A = \oint_\gamma d_0 \bar{f}$$

虽然 $A = d_0 \bar{f}$ 形式上是一个恰当 1-形式，但 $\bar{f}$ 可以是**多值函数**（具有单值性）。此时 $A$ 局部上看是 $d_0$ of something，但全局上没有单值的原函数。因此：

$$A \in \ker(d_1) \setminus \im(d_0) \quad \text{（闭但不恰当）}$$

即 $[A] \neq 0 \in H^1_{\text{dR}}(\mathcal{M})$。

#### 2.4.2 $k=2$ 恒为零的本质

对于 $k=2$，$F = d_1 A = d_1 d_0 \bar{f}$。由于 $d_1 \circ d_0 = 0$ 是**代数的**而非依赖于 $\bar{f}$ 的单值性：

$$d_1(d_0 \bar{f})(x) = 0 \quad \text{逐点成立}$$

无论 $\bar{f}$ 是否全局单值，逐点的偏导数交换性保证了 $F_{\mu\nu} \equiv 0$。这是在**微分形式层面**的恒等式，不依赖于积分路径/曲面的拓扑。

#### 2.4.3 结构对比表

| 特征 | $k=1$（1-圈 $\gamma$） | $k=2$（2-圈 $\Sigma$） |
|------|------------------------|------------------------|
| 微分形式 | $A \in \Omega^1$ | $F = d_1 A \in \Omega^2$ |
| 通量/和乐 | $\Phi(\gamma) = \oint_\gamma A$ | $\Phi(\Sigma) = \int_\Sigma F$ |
| 闭性 | $d_1 A = 0$（总是成立） | $d_2 F = d_2 d_1 A = 0$（总是成立） |
| 非零可能性 | **可以非零**（$\bar{f}$ 有单值性） | **恒为零**（$d_1 d_0 \equiv 0$ 代数恒等式） |
| 非零条件 | $\bar{f}$ 非全局单值 | 不存在（$F = 0$） |
| 拓扑障碍 | $[A] \neq 0 \in H^1_{\text{dR}}$ | $[F] = 0 \in H^2_{\text{dR}}$（平凡） |

---

### 2.5 $H_2$ 的物理意义：即使通量为零，2-圈依然重要

#### 2.5.1 审计 2-瞬子的重新定义

虽然 $F = d_1 A = 0$，但这并不意味着高维审计瞬子没有意义。我们需要重新定义 2-审计瞬子的"电荷"。

**定义 1（审计 2-瞬子）**：设 $\Sigma \subset \mathcal{M}_{\rho_{\text{crit}}}$ 为密度滤流的非平凡 2-圈（$0 \neq [\Sigma] \in H_2(\mathcal{M}_{\rho_{\text{crit}}}; \mathbb{Z})$）。$\Sigma$ 是**审计 2-瞬子**，如果：

1. **低密度局部化**：$\Sigma \subset \mathcal{M}_{\rho_{\text{crit}}}$（数据稀疏区域中的闭曲面/空洞）
2. **内部共识虚假性**：$\Sigma$ 包围的体积 $\Omega$（$\partial\Omega = \Sigma$）满足：
   $$\inf_{x \in \Omega} \text{Yajie}(x) \geq \text{Yajie}_{\text{threshold}} \quad \text{而} \quad \frac{1}{\text{vol}(\Omega)}\int_\Omega |\bar{f}(x)| dx \gg \varepsilon_{\text{tol}}$$
   即：$\Sigma$ 内部所有专家"一致"，但一致于**错误的**预测
3. **拓扑非平凡性**：$[\Sigma] \neq 0 \in H_2(\mathcal{M}_{\rho_{\text{crit}}}; \mathbb{Z})$

#### 2.5.2 2-瞬子的"电荷"：体积分而非通量

虽然曲面通量 $\int_\Sigma F = 0$，但可以定义体积分作为"2-瞬子电荷"：

$$Q_2(\Sigma) = \int_\Omega |\bar{f}(x)| \cdot \rho(x)^{-1} \, d\text{vol}$$

其中 $\Omega$ 是以 $\Sigma$ 为边界的 3-链（$\partial\Omega = \Sigma$）。

直观含义：$Q_2$ 度量了 2-圈包围的体积内，按数据密度加权的总专家偏差。低数据密度（$\rho$ 小）区域中的偏差被放大——因为这些区域正是审计瞬子最危险的地方。

#### 2.5.3 为什么 2-瞬子比 1-瞬子更危险？

1-审计瞬子：1-圈上的闭曲线——需要专家输出沿曲线有一致的偏差。只要在曲线上任意一点有诚实的专家打破一致性，瞬子就被"杀死"。

2-审计瞬子：2-圈包围的**体积**——只要整个体积内没有诚实的数据点/专家，瞬子就存活。破坏 2-瞬子需要在体积**内部**放置数据——比在曲线上放置数据难得多。

类比：
- 1-瞬子 = 围墙上的洞（在边界上检测到即可修复）
- 2-瞬子 = 空心球（需要深入内部才能发现和修复）

---

### 2.6 持续同调的 $H_2$ 分析

#### 2.6.1 密度滤流的 2-维持续同调

对密度子水平滤流 $\{\mathcal{M}_\varepsilon\}_{\varepsilon \geq 0}$，计算 $H_2(\mathcal{M}_\varepsilon; \mathbb{Z}_2)$ 的持续模。持续图 $\mathcal{D}_2 = \{(b_j, d_j)\}$ 中的每个点对应：

- **出生** $b_j$：该 2-维空洞（void/cavity）首次在 $\mathcal{M}_{b_j}$ 中形成
- **死亡** $d_j$：空洞在 $\mathcal{M}_{d_j}$ 中被"填充"（成为边界）

长寿的 $H_2$ 类（$\text{pers} = d_j - b_j$ 大）对应**鲁棒的 2-瞬子候选**。

#### 2.6.2 2-维同调的检测算法概要

1. 构建密度滤流 $\{\mathcal{M}_\varepsilon\}$
2. 计算 $PH_2$（2-维持续同调）
3. 提取长寿类 $[\Sigma_j] \in H_2(\mathcal{M}_{\rho_{\text{crit}}})$
4. 对每个 $\Sigma_j$，计算包围体积 $\Omega_j$ 内的平均偏差 $\int_{\Omega_j} |\bar{f}|$
5. 分类：若 $\int_{\Omega_j} |\bar{f}| > \tau \cdot \text{vol}(\Omega_j)$（偏差显著），且内部 Yajie 分数高，则 $\Sigma_j$ 是**2-审计瞬子**

#### 2.6.3 与 1-瞬子检测的关键差异

| 方面 | 1-瞬子 ($H_1$) | 2-瞬子 ($H_2$) |
|------|---------------|---------------|
| 检测对象 | 低密度"隧道" | 低密度"空洞/气泡" |
| 持续同调维度 | $PH_1$ | $PH_2$ |
| 和乐/电荷 | $\oint_\gamma A$（可能非零） | $F = 0$（恒零） |
| 替代电荷 | 不需要替代 | 体积分 $Q_2$ |
| 修复方法 | 在曲线上加数据点 | 在体积内部加数据点 |
| 危害程度 | 中（线性缺陷） | 高（体积缺陷） |

---

### 2.7 尝试超越 $F = d_1 A$：替代的 2-形式构造

考虑到 $F = d_1 A \equiv 0$，是否存在其他有意义的审计 2-形式？本节探索三个候选。

#### 2.7.1 候选 1：个体专家的 2-形式

不同于用平均偏离，考虑每个专家 $E_i$ 的偏离 $f_i$ 分别构造：

$$F^{(i)} = d_1(d_0 f_i) = 0 \quad \text{（同样恒为零）}$$

个体专家的 2-形式也恒为零。这不是平均化的问题，而是 $d^2 = 0$ 的结构性问题。

#### 2.7.2 候选 2：外积构造

定义外积形式的 2-形式：

$$G = A \wedge A \in \Omega^2(\mathcal{M})$$

但 $A \wedge A$ 作为微分形式，当 $A$ 是 1-形式时，$A \wedge A = 0$（外积的反对称性）。

#### 2.7.3 候选 3：曲率形式（非交换推广）

如果审计联络 $A$ 推广为**非交换的**（矩阵值 1-形式 $A = A^a T^a$，$T^a$ 为李代数生成元），则可以定义曲率 2-形式：

$$\mathcal{F} = d_1 A + A \wedge A$$

此时：
- $d_1 A$ 仍为零（通过 $d_1 d_0 \bar{f} = 0$）
- 但 $A \wedge A = \frac{1}{2}[A_\mu, A_\nu] dx^\mu \wedge dx^\nu$ 可能非零（如果李代数非交换）

这需要将审计推广到非交换的专家规范理论——每个专家 $E_i$ 的偏离对应不同的李代数方向。这是未来工作的一个有趣方向，但超出了当前 $A = d_0 \bar{f}$ 的标量联络框架。

#### 2.7.4 结论

在当前的标量联络框架（$A = d_0 \bar{f}$）中，不存在非零的审计 2-形式。$k=2$ 的审计通量恒为零这一事实是**结构性的**——它源自 $d^2 = 0$ 的代数学。但这并不意味着 $H_2$ 无意义：2-瞬子的"电荷"应从体积分而非曲面通量来定义。

---

### 2.8 高维推广的完整图景

#### 2.8.1 对任意 $k$ 的审计 $k$-形式

递推定义：$A_1 \equiv A = d_0 \bar{f}$，$A_k = d_{k-1} A_{k-1}$。

由 $d^2 = 0$：$A_k = 0$ 对所有 $k \geq 2$。

**推论**：在标量联络框架中，只有 $k=1$ 的审计瞬子具有非零的微分-拓扑电荷（和乐）。

#### 2.8.2 所有维度的审计瞬子分类

审计瞬子的物理意义不依赖于微分通量非零，而是基于**拓扑非平凡性 + 包围区域的系统偏差**：

| 维度 $k$ | 拓扑障碍 | 微分电荷 | 物理电荷 | 存在性 |
|-----------|---------|---------|---------|--------|
| $k=1$ | $H_1(\mathcal{M}_{\rho_{\text{crit}}})$ | $\oint_\gamma A \neq 0$ | 环路累积偏差 | ✓ 存在且丰富 |
| $k=2$ | $H_2(\mathcal{M}_{\rho_{\text{crit}}})$ | $F = 0$（恒零） | $\int_\Omega |\bar{f}|\rho^{-1}$ | ✓ 存在（需替代电荷） |
| $k \geq 3$ | $H_k(\mathcal{M}_{\rho_{\text{crit}}})$ | $A_k = 0$（恒零） | 体积分的推广 | 可能（取决于数据流形维度） |

#### 2.8.3 经验预测

对于真实的 SCX 审计数据集（例如 AlN MLIP 审计），预期：
- 1-瞬子：常见于数据流形的"隧道"区域（例如，两个数据簇之间的稀疏连接）
- 2-瞬子：可能出现在数据流形中的"气泡"区域（例如，三维参数空间中完全没有训练数据的封闭子区域）
- 如果数据流形的内在维度 $n \geq 4$，可能出现 $k=3$ 及以上的瞬子

---

## 3. 总结与交叉关联 {#cross}

### 3.1 C7 核心结论

1. **模空间维度**：$\dim(\mathcal{G}) \sim \ln(Re^{3/4})$，从 Kolmogorov 标度 $\eta/L = Re^{-3/4}$ 和惯性子区自由度的对数标度导出
2. **规范不变可观测量**：$\varepsilon$, $k^{-5/3}$ 指数, $\zeta_p$, $C_D$, $Nu$
3. **规范依赖可观测量**：$\nu_t$, 局部 $k$, 壁面函数, 模型常数
4. **模空间几何**：k-ε 和 k-ω 在惯性子区等价；LES 和 RANS 的区别在于截断尺度的不同选择

### 3.2 C8 核心结论

1. **审计 2-形式 $F = d_1 A \equiv 0$**：由 $d^2 = 0$ 的代数恒等式保证，无论 $\bar{f}$ 是否全局单值
2. **2-圈通量恒为零**：$\int_\Sigma F = 0$ 对所有 2-圈 $\Sigma$
3. **与 $k=1$ 的根本对比**：$k=1$ 的和乐非零依赖于 $\bar{f}$ 的单值性（分析性质）；$k=2$ 的零通量是代数的（$d^2=0$）
4. **2-瞬子依然存在**：使用替代电荷 $Q_2 = \int_\Omega |\bar{f}|\rho^{-1}$ 而非曲面通量
5. **非交换推广**：若将 $A$ 推广为矩阵值联络，$A \wedge A$ 项可能产生非零曲率——这是一个开放问题

### 3.3 两个问题的 SCX 框架内联系

C7（湍流模空间）和 C8（审计瞬子 $H_2$）在 SCX 框架内通过**数据的规范结构**相联系：

- C7 处理物理系统（湍流）中的规范自由度——模型的不可辨识性
- C8 处理审计系统（专家）中的拓扑缺陷——专家共识的虚假性
- 两者的共同主题：**$\mathcal{F}/\mathcal{G}$ 的结构决定可观测物理的边界**

在湍流中，规范固定是模型选择（k-ε vs LES）；在审计中，规范固定是专家池的选择和共识度量的定义。模空间 $\mathcal{F}/\mathcal{G}$ 的拓扑结构（通过持续同调检测）在两种情况下都揭示了系统的不可约特征。

---

## 附录 A：关键公式汇总

### C7

| 公式 | 含义 |
|------|------|
| $\eta = (\nu^3/\varepsilon)^{1/4}$ | Kolmogorov 耗散尺度 |
| $\eta/L = Re^{-3/4}$ | 尺度比 |
| $E(k) = C_K \varepsilon^{2/3} k^{-5/3}$ | Kolmogorov 能谱 |
| $\dim(\mathcal{G}) \sim \ln(Re^{3/4})$ | 规范群维度 |
| $\mathcal{T}_{\text{mod}} = \mathcal{F}/\mathcal{G}$ | 湍流规范模空间 |

### C8

| 公式 | 含义 |
|------|------|
| $A = d_0 \bar{f}$ | 审计 1-形式 |
| $\Phi(\gamma) = \oint_\gamma A$ | 1-圈和乐（可非零） |
| $F = d_1 A = 0$ | 审计 2-形式（恒为零） |
| $\int_\Sigma F = 0$ | 2-圈通量（恒为零） |
| $Q_2(\Sigma) = \int_\Omega \vert\bar{f}\vert\rho^{-1}$ | 替代 2-瞬子电荷 |

---

## 附录 B：阻塞识别

### C7 的开放问题

1. **规范群 $\mathcal{G}$ 的完整分类**：目前仅给出维度的对数标度估计，$\mathcal{G}$ 的李代数结构、轨道空间的拓扑尚未明确
2. **规范不变量的完备集**：是否存在类似 Yang-Mills 理论中 Wilson 圈的完备规范不变量集合？
3. **$\dim_{\text{irr}}$ 的精确定义**：不可约复杂性的度量需要更严格的数学定义
4. **量子湍流的类比**：超流氦中的量子化涡旋是否提供"可解模空间"？

### C8 的开放问题

1. **非交换审计联络**：矩阵值 $A = A^a T^a$ 能否产生非零曲率 $\mathcal{F} = dA + A \wedge A$？
2. **替代电荷的统计显著性**：$Q_2$ 的假设检验需要发展
3. **经验验证**：在真实 SCX 数据上检测 2-瞬子
4. **与 Morse 理论的联系**：$\rho$ 作为 Morse 函数时，$PH_2$ 的出生/死亡对应 $\rho$ 的哪些临界点？

---

> **文档版本**: v1.0
> **创建日期**: 2026-07-02
> **目标文件**: `docs/analysis/conjectures_C7_C8.md`
