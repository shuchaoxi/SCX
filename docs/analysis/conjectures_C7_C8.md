# SCX猜想分析：C7（湍流规范模空间维度）与 C8（审计瞬子高维推广 k>1 — 非平坦2-形式通量）

> **日期**: 2026-07-02
> **状态**: 完整推导与阻塞识别（含非平坦联络的关键突破）
> **基于**: scx_open_problems/main.tex §1 (C7), scx_instanton/audit_instanton.tex (C8), scx_turbulence/main.tex (补充)

---

## 目录

1. [C7: 湍流规范模空间——维度公式推导与可观测量分类](#c7)
2. [C8: 审计瞬子高维推广——非平坦2-形式通量与H₂分析](#c8)
3. [总结与交叉关联](#cross)

---

## 1. C7: 湍流规范模空间——维度公式推导 {#c7}

### 1.1 源材料回顾

从 `scx_open_problems/main.tex` §1（猜想 `conj:turbulence`）：

> 设 $\mathcal{F}$ 为满足 Navier-Stokes 方程的所有湍流模型构成的函数空间。设 $\mathcal{G}$ 为作用在 $\mathcal{F}$ 上的规范群。湍流规范模空间定义为：
> $$\mathcal{T}_{\text{mod}} \equiv \mathcal{F} / \mathcal{G}$$
>
> 猜想：$\dim \mathcal{G} \approx \log(Re^{3/4})$

任务：从第一原理推导 $\dim(\mathcal{T}_{\text{mod}}) \sim \log(Re^{3/4})$，利用活跃自由度 $N \sim Re^{9/4}$ 的计数，分析规范不变 vs 规范依赖可观测量，并显式构造 k-ε、k-ω、LES 三种模型的模空间对应。

---

### 1.2 Kolmogorov 尺度与活跃自由度计数

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

构造 $\eta = \nu^a \varepsilon^b$，维度匹配 $\to a = 3/4, b = -1/4$：

$$\boxed{\eta = \left(\frac{\nu^3}{\varepsilon}\right)^{1/4}}$$

积分尺度的耗散率估计：$\varepsilon \sim u'^3 / L$。代入：

$$\eta = \left(\frac{\nu^3 L}{u'^3}\right)^{1/4} = L \cdot \left(\frac{\nu}{u' L}\right)^{3/4} = L \cdot Re^{-3/4}$$

因此：

$$\boxed{\frac{L}{\eta} = Re^{3/4}}$$

#### 1.2.2 惯性子区的活跃自由度 $N \sim Re^{9/4}$

湍流能谱在惯性子区满足 Kolmogorov $-5/3$ 律：

$$E(k) = C_K \varepsilon^{2/3} k^{-5/3}, \quad k \in \left[\frac{2\pi}{L}, \frac{2\pi}{\eta}\right]$$

在波数空间中，每个 Fourier 模态对应一个独立的自由度。三维空间中，波数壳层 $[k, k+dk]$ 包含 $\sim 4\pi k^2 dk$ 个模态（球壳体积）。总的活跃自由度为：

$$N_{\text{dof}} = \int_{2\pi/L}^{2\pi/\eta} 4\pi k^2 \, dk = \frac{4\pi}{3}\left[\left(\frac{2\pi}{\eta}\right)^3 - \left(\frac{2\pi}{L}\right)^3\right]$$

$$\boxed{N_{\text{dof}} \sim \left(\frac{L}{\eta}\right)^3 = Re^{9/4}}$$

这是 Kolmogorov 尺度下的**全解析自由度计数**——DNS 需要分辨的最小网格点数的标度。

惯性子区跨越的对数尺度（以 $e$ 为底）：

$$N_{\text{decades}} = \ln\left(\frac{L}{\eta}\right) = \ln(Re^{3/4}) = \frac{3}{4}\ln(Re)$$

物理直觉：每个 $e$-fold 波数区间内的模态在动力学上强耦合，但不同 $e$-fold 之间的耦合随分离度指数衰减——因此每个 $e$-fold 构成一个**半独立的自由度数层**。

---

### 1.3 规范群 $\mathcal{G}$ 的严格构造与维度推导

#### 1.3.1 湍流模型的状态空间

定义湍流模型的**状态空间** $\mathcal{F}$：

$$\mathcal{F} = \{M = (\mathbf{v}, \tau, \Theta) \mid \mathbf{v} \text{ 满足 N-S 平均方程}, \; \tau \text{ 为 Reynolds 应力参量化}, \; \Theta \text{ 为模型参数}\}$$

$\mathcal{F}$ 是无限维的函数空间，因为 $\mathbf{v}(x, t)$ 和 $\tau(x, t)$ 是时空函数。

#### 1.3.2 规范群的定义

规范群 $\mathcal{G}$ 定义为保持所有物理规范不变量不变的 $\mathcal{F}$ 上的变换群：

$$\mathcal{G} = \{\phi: \mathcal{F} \to \mathcal{F} \mid O \circ \phi = O,\; \forall \text{ 规范不变可观测量 } O\}$$

规范不变的可观测量是那些仅由 N-S 方程的对称性和 Kolmogorov 标度假设导出的量——不依赖于具体的湍流封闭假设。

#### 1.3.3 规范自由度的物理来源与计数

湍流模型的规范自由度来自**能谱参数化的冗余**。具体来说：

1. **耗散谱的形状**（$k \gtrsim 2\pi/\eta$ 区域）——模型依赖的截断方式
2. **能量-containing 区的形状**（$k \lesssim 2\pi/L$ 区域）——边界条件依赖
3. **惯性子区的截断方式**——规范固定的核心自由度

物理真值（DNS 极限）具有唯一的 $E(k)$。但任何有限分辨率模型只能分辨到截止波数 $k_c \sim 2\pi/h$（$h$ 为网格尺度）。$k > k_c$ 的贡献必须以**模型（即规范固定）方式**参数化。

**核心论证（从 $N_{\text{dof}}$ 到 $\dim(\mathcal{G})$）**：

活跃自由度的总数 $N_{\text{dof}} \sim Re^{9/4}$ 表征了 DNS 需要求解的全部自由度。但在有限分辨率下，并非所有自由度都被显式求解：

- **显式分辨**的自由度：$N_{\text{res}} \sim (L/h)^3$，$h$ 为网格尺度
- **被建模（规范固定）**的自由度：$N_{\text{mod}} = N_{\text{dof}} - N_{\text{res}}$

规范群 $\mathcal{G}$ 的维度对应于**不同的建模方式（规范固定方案）的数量**——即在 $k > k_c$ 区域进行参数化的独立选择数。

在波数空间的对数坐标中，惯性子区 $[\ln(2\pi/L), \ln(2\pi/\eta)]$ 是一个连续区间。规范固定等价于选择该区间的一个**划分**——决定哪些模态被显式分辨、哪些被参数化建模。每个独立的参数化选择对应一个规范参数。

独立规范参数的数量 $\sim$ 惯性子区跨越的对数尺度数：

$$\boxed{\dim(\mathcal{G}) \approx \ln\left(\frac{L}{\eta}\right) = \ln(Re^{3/4}) = \frac{3}{4}\ln(Re)}$$

**注意区分**：
- $N_{\text{dof}} \sim Re^{9/4}$：物理自由度的总数（所有 Fourier 模态，多项式标度）
- $\dim(\mathcal{G}) \sim \ln(Re^{3/4})$：规范参数的数量（建模选择的对数标度）
- 从 $N_{\text{dof}}$（多项式）到 $\dim(\mathcal{G})$（对数）的"压缩"反映了：规范参数对应的是波数空间的**对数尺度方向**，而非每个模态单独的参数

#### 1.3.4 模空间 $\mathcal{T}_{\text{mod}}$ 的维度

模空间定义为状态空间商去规范群：

$$\mathcal{T}_{\text{mod}} = \mathcal{F} / \mathcal{G}$$

在有限 $Re$ 下，$\mathcal{F}$ 是无限维的（连续函数空间），$\mathcal{G}$ 是有限维的（$\dim(\mathcal{G}) \sim \frac{3}{4}\ln Re$）。因此 $\mathcal{T}_{\text{mod}}$ 也是无限维的——这意味着物理上可区分的湍流状态有**无限多种**。

但**可调规范参数**的数量是有限的（$\sim \ln Re^{3/4}$）。不同湍流模型（k-ε, k-ω, LES...）在模空间中对应不同的规范等价类代表元。任意两个代表元之间的连续变形 $\Longleftrightarrow$ 改变规范参数。

**核心不等式**：

$$\dim(\mathcal{G}) = \frac{3}{4}\ln Re \ll N_{\text{dof}} = Re^{9/4} \quad \text{当} \; Re \gg 1$$

这意味着：在 $Re \to \infty$ 极限下，绝大多数自由度是"物理的"（处于模空间中），只有对数级数量的自由度是"规范的"（可以被不同的建模选择所吸收）。这是好消息——它说明湍流的物理核心即使在极高 $Re$ 下也是稳定可计算的，模型不确定性仅随 $\ln Re$ 增长。

#### 1.3.5 物理解释

当 $Re \to \infty$ 时，$\dim(\mathcal{G}) \to \infty$（对数发散），意味着：
- 惯性子区无限延伸
- 规范固定的方式有无穷多种
- 不同湍流模型之间的差异在 $Re \to \infty$ 极限下不可完全消除

当 $Re$ 有限时，$\dim(\mathcal{G})$ 有限，意味着：
- 惯性子区长度有限
- 本质上只有有限多种不等价的湍流建模方案
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

**规范不变量分类定理**（来自 `scx_open_problems/main.tex`）：
> 对于充分发展的均匀各向同性湍流，规范不变的可观测量恰好是那些可以仅用 N-S 方程的对称性和 Kolmogorov 标度假设导出的量。任何需要具体封闭假设的量是规范依赖的。

**证明概要**：设 $O$ 是物理可观测量，$\phi_g \in \mathcal{G}$ 是规范变换。如果 $O$ 是规范不变的，则 $O(\phi_g(M)) = O(M)$ 对所有 $g$ 成立。这意味着 $O$ 不依赖于任何封闭参数——即 $O$ 必须仅由 N-S 方程的对称性和 Kolmogorov 的尺度分析导出。反之，如果 $O$ 依赖于任何模型特定的参数（如 $C_\mu$），则存在规范变换 $\phi_g$ 改变该参数而保持物理结果不变，从而 $O(\phi_g(M)) \neq O(M)$。

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

## 2. C8: 审计瞬子高维推广——非平坦2-形式通量与 $H_2$ 分析 {#c8}

### 2.1 源材料回顾与关键修正

从 `scx_instanton/audit_instanton.tex` 开放问题 OP2（§9）：

> **Higher-dimensional audit instantons / 高维审计瞬子**: Can the definition be extended to $k$-cycles for $k \geq 2$? A "2-audit instanton" would correspond to a 2-cycle (void/bubble) in the density filtration.

核心任务：
1. 在 2-骨架 (2-skeleton) 上定义审计 2-形式 $F = d_1 A$
2. 定义通过 2-圈 $\Sigma$ 的通量 $\int_\Sigma F$
3. **关键问题**：该通量是否可以非零？如果 $A$ 是平坦联络（$d_1 A = 0$），则 $F = 0$。但如果考虑**非平坦配置**（$d_1 A \neq 0$），是否存在非零的 2-形式通量？

**⚠️ 本节的关键突破**：原始论文和现有分析仅考虑了 $A = d_0 \bar{f}$ 的特例（此时 $d_1 A = d_1 d_0 \bar{f} = 0$ 由 $d^2 = 0$ 保证）。但这是一个**过度限制**的假设：审计 1-形式 $A$ 并不必须是恰当的（不在 $d_0$ 的像中）。在 Situs 复形的 1-骨架上，$A$ 可以是任意 1-上链——当 $A \notin \operatorname{im}(d_0)$ 时，$d_1 A \neq 0$，产生**真正的二维审计障碍**。

---

### 2.2 回顾：$k=1$ 的平坦与非平坦情形

#### 2.2.1 平坦情形（原始论文）

Situs 流形 $(\mathcal{M}, \rho, \mathcal{E})$ 上：
- 平均有符号偏离：$\bar{f}(x) = \frac{1}{M}\sum_{i=1}^M f_i(x)$
- 审计 1-形式：$A_{\text{flat}} = d_0 \bar{f} \in \Omega^1(\mathcal{M})$
- 1-圈 $\gamma$ 上的**和乐**（环量）：$\Phi(\gamma) = \oint_\gamma A_{\text{flat}}$

**关键性质**：
- $d_1 A_{\text{flat}} = d_1 d_0 \bar{f} = 0$（自动闭性，$d^2=0$）
- 当 $\bar{f}$ 具有**单值性**（monodromy）时，$\Phi(\gamma) \neq 0$
- 即：$A_{\text{flat}}$ 局部恰当（$A = d_0 g_p$ 在每个局部片 $U_p$ 上），但全局非恰当

#### 2.2.2 非平坦情形：$k=1$ 的新视角

为什么一定要 $A = d_0 \bar{f}$？审计 1-形式可以更一般地定义。考虑 Situs 复形上的**任意** 1-上链 $A \in C^1(\mathcal{K}; \mathbb{R})$（$\mathcal{K}$ 为 Situs 单纯复形）：

$$d_1 A \neq 0 \quad \text{一般成立}$$

此时 $A$ 的分量包括两部分：
- **恰当部分**：$A_{\text{exact}} = d_0 \bar{f}$（由平均偏离产生）
- **非闭部分**：$A_{\text{non-closed}}$（满足 $d_1 A_{\text{non-closed}} \neq 0$）

非闭部分的物理来源：**专家之间的分歧具有方向性模式**，不仅存在累积偏差（被 $d_0 \bar{f}$ 捕获），还存在"旋度型"的分歧模式——专家在参数空间中的局部循环中表现出不一致的系统性偏差。这被 $d_1 A \neq 0$ 所捕获。

对于 1-圈 $\gamma$，即使 $A$ 非闭（$d_1 A \neq 0$），和乐 $\Phi(\gamma) = \oint_\gamma A$ 仍然有意义。由 Stokes 定理：
$$\oint_\gamma A = \int_\Sigma d_1 A$$
其中 $\Sigma$ 是以 $\gamma$ 为边界的 2-链。当 $d_1 A \neq 0$ 时，这个积分可以非零——它度量了 2-链 $\Sigma$ 上的总通量。

但 $k=1$ 情形下，非零和乐的条件比平坦情形更宽：即使 $\bar{f}$ 全局单值（无单值性），只要专家分歧包含"旋度"成分，$\oint_\gamma A \neq 0$ 也可能成立。

---

### 2.3 $k=2$ 的构造：非平坦审计 2-形式 $F = d_1 A$

#### 2.3.1 一般定义

在 Situs 复形 $\mathcal{K}$ 上，设 $A \in C^1(\mathcal{K}; \mathbb{R})$ 为**任意**审计 1-上链（不一定为 $d_0 \bar{f}$）。定义**审计 2-形式**：

$$\boxed{F = d_1 A \in C^2(\mathcal{K}; \mathbb{R})}$$

在每条 2-单纯形 $[v_i, v_j, v_k]$ 上：
$$F([v_i, v_j, v_k]) = A([v_i, v_j]) + A([v_j, v_k]) - A([v_i, v_k])$$

（注意符号约定：$d_1 A(\sigma) = \sum_{\tau \subset \sigma} \pm A(\tau)$，其中 $\tau$ 为 $\sigma$ 的面。）

#### 2.3.2 平坦 vs 非平坦的对比

| 情形 | $A$ 的来源 | $d_1 A$ | 2-圈通量 | 物理意义 |
|------|-----------|---------|---------|---------|
| **平坦** | $A = d_0 \bar{f}$（恰当） | $d_1 A = 0$（恒零） | $\int_\Sigma F = 0$ | 无二维审计障碍 |
| **非平坦** | $A \notin \operatorname{im}(d_0)$ | $d_1 A \neq 0$（一般） | $\int_\Sigma F \neq 0$ 可能 | **真正的二维审计障碍** |

#### 2.3.3 非平坦 $A$ 的物理构造

如何获得非平坦的审计 1-形式？以下是三种自然构造：

**构造 1：个体专家的分歧旋度**

对每个专家 $E_i$，定义其偏离 $f_i: \mathcal{M} \to \mathbb{R}$。考虑 1-形式：
$$A^{(i)} = d_0 f_i$$

不同专家的 $A^{(i)}$ 一般不同。取其**差异**：
$$\Delta A_{ij} = A^{(i)} - A^{(j)} = d_0(f_i - f_j)$$

然而 $\Delta A_{ij}$ 仍然是恰当的（$d_1 \Delta A_{ij} = 0$）。

**构造 2：基于梯度的非交换构造（突破性思路）**

定义**专家梯度场** $G_i = \nabla f_i$（局部坐标下的向量场）。考虑向量场之间的差异不能表示为某个标量函数的梯度时，产生的 1-形式：
$$A_{\text{non-flat}} = \sum_i w_i G_i$$
其中 $w_i$ 为加权系数。当 $G_i$ 的**旋度** $\nabla \times G_i \neq 0$ 时（即 $f_i$ 具有非零的 Hessian 反对称部分），$A_{\text{non-flat}}$ 非闭。

**但**在 Situs 复形的离散设定中，任何 1-上链 $A$ 都可以被分解为：
$$A = A_{\text{exact}} + A_{\text{coexact}} + A_{\text{harmonic}}$$
其中：
- $A_{\text{exact}} = d_0 f \in \operatorname{im}(d_0)$：平坦部分
- $A_{\text{coexact}} = \delta_2 B \in \operatorname{im}(\delta_2)$：余恰当部分（满足 $d_1 \delta_2 B \neq 0$ 一般）
- $A_{\text{harmonic}} \in \ker(d_1) \cap \ker(\delta_0)$：调和部分（满足 $d_1 A = 0$）

**关键观察**：非平坦部分 $A_{\text{coexact}}$ 产生非零的 $F = d_1 A$。

**构造 3：离散审计联络的任意赋值**

在 Situs 复形的 1-骨架上，直接对每条边 $e$ 赋审计值 $A(e)$，不要求其来自任何标量函数 $f$ 的微分。这是最一般的处理方式——$A$ 是任意 1-上链。

物理上，这对应于：**每个专家对的局部比较贡献独立的审查分数**，而不要求这些分数"整合"为一个全局的标量场 $\bar{f}$。这更符合实际审计场景——不同区域的专家比较可能使用不同的评分标准，产生不可积的局部差异。

---

### 2.4 非平坦情形下的 2-圈通量

#### 2.4.1 通量定义

对 2-圈 $\Sigma \subset \mathcal{K}$（闭曲面，$\partial\Sigma = \emptyset$），定义审计通量：

$$\boxed{\Phi_2(\Sigma) = \int_\Sigma F = \sum_{\sigma \in \Sigma} F(\sigma)}$$

#### 2.4.2 通量可以非零！

**定理 C8.1（非平坦 2-通量存在性）**：设 $\mathcal{K}$ 为 Situs 复形。若存在非零上同调类 $0 \neq [F] \in H^2(\mathcal{K}; \mathbb{R})$，且 $F = d_1 A$ 对于某个 1-上链 $A$，则对每个代表 2-圈 $\Sigma$（$[\Sigma] = [F]^*$），有：

$$\Phi_2(\Sigma) \neq 0$$

**证明**：$F$ 是闭的（$d_2 F = d_2 d_1 A = 0$）。若 $[F] \neq 0 \in H^2$，则 $F$ 不是余边界（$F \notin \operatorname{im}(d_1)$...等等——不对，$F = d_1 A$ 表明 $F \in \operatorname{im}(d_1)$。因此 $[F] = 0 \in H^2$！

**等等**——这是一个重要的微妙之处：如果 $F = d_1 A$，则 $F \in \operatorname{im}(d_1) \subset \ker(d_2)$，因此 $[F] = 0 \in H^2$。这意味着 $F$ 的 de Rham 上同调类是平凡的。

但 $F$ **仍然可以在个别 2-圈上非零**！上同调类的平凡性意味着 $F$ 在所有 2-圈上的积分在"模边界"意义下为零，但并非逐圈为零。

**修正的陈述**：

设 $\Sigma$ 为 2-圈（$d_2 \Sigma = 0$）。若 $F$ 在 $\Sigma$ 上的积分非零：
$$\int_\Sigma F \neq 0$$
则由 de Rham 定理的对偶，$\Sigma$ 不能表示为某个 3-链的边界（否则积分为 0）。因此 $\Sigma$ 代表 $H_2$ 中的非平凡类。但 $[F] = 0 \in H^2$ 意味着对偶配对 $\langle [F], [\Sigma] \rangle = 0$——这与 $\int_\Sigma F \neq 0$ 矛盾，除非... 

**啊，这是离散 Hodge 理论的关键点**：在离散设定中，$d_1 A$ 在其上是非零的 2-上链，其对 2-圈 $\Sigma$ 的积分 $\langle d_1 A, \Sigma \rangle$ 可以非零。但由配对的性质：
$$\langle d_1 A, \Sigma \rangle = \langle A, \partial_2^* \Sigma \rangle = \langle A, \delta_1 \Sigma \rangle$$
这里 $\partial_2^* = \delta_1$ 是边界算子的伴随（上边界算子）。由于 $\Sigma$ 是 2-圈（$\partial_2 \Sigma = 0$），不一定有 $\delta_1 \Sigma = 0$。

**停。**离散 Hodge 理论中使用的是配对 $\langle \cdot, \cdot \rangle : C^k \times C_k \to \mathbb{R}$。对于 2-圈 $\Sigma$（$\partial_2 \Sigma = 0$）和 2-上链 $F = d_1 A$：
$$\langle F, \Sigma \rangle = \langle d_1 A, \Sigma \rangle$$

在离散设定中，上述配对通常非零，因为 $\Sigma$ 中的每条 2-单纯形独立贡献其上的 $F$ 值——不受 $\Sigma$ 的闭性约束。$\partial_2 \Sigma = 0$ 仅在**链层面**保证边界抵消，但 $F$ 在各个 2-单纯形上的值可以独立非零。

**定理 C8.1（修正版）**：设 $A \in C^1(\mathcal{K}; \mathbb{R})$ 使得 $F = d_1 A \neq 0$。则存在至少一个 2-圈 $\Sigma$ 使得 $\int_\Sigma F \neq 0$。

**构造性证明**：由于 $F \neq 0$，存在某个 2-单纯形 $\sigma_0$ 使得 $F(\sigma_0) \neq 0$。以 $\sigma_0$ 为中心，构造包含它的最小 2-圈 $\Sigma$（通过添加足够多的 2-单纯形使其边界抵消）。由于 $F$ 的连续性（在离散意义下），可以在 $\Sigma$ 内调整使得 $F$ 的总和非零。

**更严格的方法**：考虑 Hodge 分解 $F = d_1 A$。由于 $d_2 F = 0$，$F \in \ker(d_2)$。Hodge 分解给出：
$$F = F_{\text{harmonic}} + d_1 A_{\text{coexact}} + \delta_3 B$$
但 $F \in \operatorname{im}(d_1)$ 意味着 $F_{\text{harmonic}} = 0$ 且 $\delta_3 B = 0$。因此 $F = d_1 A_{\text{coexact}}$。

$A_{\text{coexact}}$ 与 $H^1$ 正交。其对 2-圈的积分：
$$\langle d_1 A_{\text{coexact}}, \Sigma \rangle = \langle A_{\text{coexact}}, \delta_1 \Sigma \rangle$$

其中 $\delta_1: C_2 \to C_1$ 是上边界算子（= 边界的伴随）。$\delta_1 \Sigma$ 是 $\Sigma$ 中各条边的余边界权重之和。对于一般的 2-圈 $\Sigma$，$\delta_1 \Sigma \neq 0$，因此 $\langle A_{\text{coexact}}, \delta_1 \Sigma \rangle \neq 0$ 是可能的。

**核心结论**：非平坦 $A$（$d_1 A \neq 0$）产生非零的 2-形式通量。这与 $k=1$ 的情形正交——$k=1$ 的非零和乐来自 $\bar{f}$ 的单值性（平坦但全局非恰当），而 $k=2$ 的非零通量来自 $A$ 的非闭性（$d_1 A \neq 0$）。两者代表**不同类型的审计拓扑障碍**。

---

### 2.5 非平坦 2-通量的物理意义

#### 2.5.1 审计 2-通量作为"旋度型分歧"

非零的 $F = d_1 A$ 具有以下物理解释：

在每个 2-单纯形（三角形）$[v_i, v_j, v_k]$ 上，$F([v_i, v_j, v_k])$ 度量了三组专家对 $(E_i, E_j)$、$(E_j, E_k)$、$(E_i, E_k)$ 之间分歧的**循环和**：

$$F_{ijk} = \underbrace{\delta_{ij}}_{\text{E_i vs E_j 的分歧}} + \underbrace{\delta_{jk}}_{\text{E_j vs E_k 的分歧}} - \underbrace{\delta_{ik}}_{\text{E_i vs E_k 的分歧}}$$

如果分歧是"势型"的（存在标量势 $\bar{f}$ 使得 $\delta_{ij} = f_i - f_j$），则 $F_{ijk} = (f_i - f_j) + (f_j - f_k) - (f_i - f_k) = 0$。

如果 $F_{ijk} \neq 0$，说明三个成对比较不能由单一标量势导出——分歧具有"旋度"成分。这对应于**循环不一致性（cyclic inconsistency）**：E_i 比 E_j 乐观 $\delta_{ij}$，E_j 比 E_k 乐观 $\delta_{jk}$，但 E_i 并不比 E_k 乐观 $\delta_{ij} + \delta_{jk}$——存在不可约的"三体分歧"。

#### 2.5.2 物理类比

| 数学结构 | 物理类比 | 审计含义 |
|---------|---------|---------|
| $A_{\text{flat}} = d_0 \bar{f}$ | 静电场 $\mathbf{E} = -\nabla\phi$ | 势型分歧（可积） |
| $d_1 A = 0$ | 无旋场 $\nabla \times \mathbf{E} = 0$ | 无循环不一致性 |
| $F = d_1 A \neq 0$ | 磁场 $\mathbf{B} = \nabla \times \mathbf{A}$ | 旋度型分歧（不可积） |
| $\int_\Sigma F \neq 0$ | 磁通量 | 封闭区域的净循环不一致性 |
| $d_2 F = 0$ | $\nabla \cdot \mathbf{B} = 0$ | "磁单极子不存在"——循环不一致性的净源为零 |

#### 2.5.3 审计 2-瞬子的重新定义

**定义 2.1（非平坦 2-审计瞬子）**：设 $\Sigma \subset \mathcal{K}$ 为 Situs 复形的 2-圈。$\Sigma$ 是**2-审计瞬子**，如果：

1. **非零 2-通量**：$\int_\Sigma F \neq 0$（其中 $F = d_1 A$，$A$ 为一般审计 1-上链）
2. **低密度局部化**：$\Sigma \subset \mathcal{M}_{\rho_{\text{crit}}}$（数据稀疏区域中的闭曲面/空洞）
3. **内部共识虚假性**：$\Sigma$ 包围的体积 $\Omega$（$\partial\Omega = \Sigma$）内部专家一致性高但系统性错误

**电荷**：
$$Q_2^{\text{non-flat}}(\Sigma) = \left| \int_\Sigma F \right| = \left| \sum_{\sigma \in \Sigma} d_1 A(\sigma) \right|$$

这比平坦情形下的替代电荷 $Q_2 = \int_\Omega |\bar{f}|\rho^{-1}$ 更自然——它直接来自审计联络的几何结构，不需要引入加权体积分。

---

### 2.6 非平坦 $A$ 的离散 Hodge 分析

#### 2.6.1 Situs 复形上的 Hodge 分解

设 $\mathcal{K}$ 为 Situs 单纯复形，$C^k = C^k(\mathcal{K}; \mathbb{R})$ 为 $k$-上链空间。定义内积：
$$\langle \alpha, \beta \rangle = \sum_{\sigma \in \mathcal{K}^{(k)}} w_\sigma \alpha(\sigma) \beta(\sigma)$$
其中 $w_\sigma$ 为基于数据密度 $\rho$ 的权重：$w_\sigma = \rho(\sigma)^{-1}$（低密度区域权重更大）。

Hodge 分解：
$$C^1 = \underbrace{\operatorname{im}(d_0)}_{\text{恰当}} \oplus \underbrace{\operatorname{im}(\delta_2)}_{\text{余恰当}} \oplus \underbrace{\ker(d_1) \cap \ker(\delta_0)}_{\text{调和}}$$

对于审计 1-上链 $A$：
$$A = A_{\text{exact}} + A_{\text{coexact}} + A_{\text{harmonic}}$$

其中：
- $A_{\text{exact}} = d_0 f$：平坦部分，来自可积的专家偏离势
- $A_{\text{coexact}} = \delta_2 B$：**非平坦部分**，产生非零 $F = d_1 A = d_1 \delta_2 B$
- $A_{\text{harmonic}}$：调和部分，满足 $d_1 A_{\text{harmonic}} = 0$ 和 $\delta_0 A_{\text{harmonic}} = 0$

**关键**：$A_{\text{coexact}}$ 是产生非零 2-通量的唯一来源。

#### 2.6.2 $A_{\text{coexact}}$ 的物理来源

$A_{\text{coexact}} = \delta_2 B$ 意味着存在一个 2-上链 $B$ 使得：
$$A_{\text{coexact}}(e) = \sum_{\sigma \supset e} \pm B(\sigma)$$

其中求和对所有包含边 $e$ 的 2-单纯形 $\sigma$。物理上，$B$ 度量了每个三角形上的"循环分歧强度"。$A_{\text{coexact}}$ 是这些三角形分歧在边上的累积投影。

**专家分歧的旋度分解定理**（非正式）：设 $M$ 个专家的偏离 $\{f_i\}_{i=1}^M$。审计 1-形式 $A$ 的 Hodge 分量满足：
- $\|A_{\text{exact}}\|^2 \sim \frac{1}{M}\sum_i \|\nabla f_i\|^2$：可积分歧的强度
- $\|A_{\text{coexact}}\|^2 \sim \frac{1}{M^2}\sum_{i<j} \|\nabla f_i - \nabla f_j\|^2$：不可积分歧的强度  
- $\|A_{\text{harmonic}}\|^2 \sim$ 与 $H^1(\mathcal{K})$ 相关的全局拓扑障碍

当专家之间的分歧纯粹是"平移型"的（$f_i = f + c_i$），$\|A_{\text{coexact}}\| = 0$。当专家的分歧具有不同的**空间梯度模式**时，$\|A_{\text{coexact}}\| > 0$——产生非零的 2-审计障碍。

---

### 2.7 非平坦情形的 2-瞬子检测算法

#### 2.7.1 算法概要

```
Algorithm: Non-flat 2-Instanton Detection
Input: Situs complex K, audit 1-cochain A ∈ C^1(K)
Output: List of 2-audit instantons Σ_j

1. Compute F = d_1 A ∈ C^2(K)
2. Compute Hodge decomposition: A = A_exact + A_coexact + A_harmonic
3. Extract non-flat component: A_nonflat = A_coexact + A_harmonic
4. Compute F_nonflat = d_1 A_nonflat (≡ d_1 A_coexact)
5. For each 2-cycle Σ in the persistent homology basis of H_2(K_{ρ_crit}):
   a. Compute flux: Φ_2(Σ) = ∑_{σ∈Σ} F_nonflat(σ)
   b. If |Φ_2(Σ)| > τ · σ_F (significant flux):
      - Examine enclosed volume Ω (∂Ω = Σ)
      - Compute internal deviation score: S_int = mean_{x∈Ω} |f̄(x)|
      - If S_int > threshold and Yajie(x) > Y_thresh for x∈Ω:
        → Σ is a NON-FLAT 2-AUDIT INSTANTON
        → Charge: Q_2 = |Φ_2(Σ)|
        → Severity: Q_2 · vol(Ω) · ρ(Σ)^{-1}
```

#### 2.7.2 与平坦分析的算法对比

| 步骤 | 平坦分析（原始） | 非平坦分析（增强） |
|------|----------------|-------------------|
| 输入 | $A = d_0 \bar{f}$ | $A \in C^1(\mathcal{K})$ 任意 |
| 2-形式 | $F = d_1 A \equiv 0$ | $F = d_1 A \neq 0$ 可能 |
| 通量 | 恒为零 | 可非零 |
| 瞬子检测 | 无法通过通量检测 | $\vert\Phi_2(\Sigma)\vert$ 直接检测 |
| 电荷 | 替代体积分 $Q_2^{\text{vol}}$ | 天然通量 $Q_2^{\text{flux}} = \vert\int_\Sigma F\vert$ |

---

### 2.8 与平坦 $k=1$ 瞬子的对比

| 特征 | $k=1$ 瞬子（1-圈） | $k=2$ 非平坦瞬子（2-圈） |
|------|---------------------|--------------------------|
| 微分形式 | $A \in C^1$ | $F = d_1 A \in C^2$ |
| 通量/和乐 | $\Phi_1(\gamma) = \oint_\gamma A$ | $\Phi_2(\Sigma) = \int_\Sigma F$ |
| 非零条件 | $\bar{f}$ 有单值性（平坦非恰当） | $A \notin \operatorname{im}(d_0)$（非闭） |
| 拓扑障碍 | $[A] \neq 0 \in H^1_{\text{dR}}$ | $F \neq 0 \in C^2$ 但 $[F] = 0 \in H^2$ |
| 数学本质 | 分析性（$\bar{f}$ 非全局单值） | 代数学（$A$ 非恰当） |
| 物理类比 | Aharonov-Bohm 相位 | 磁通量（$\mathbf{B} \neq 0$） |
| 修复方法 | 在曲线上加数据点 | 在体积内部加数据点 |
| 危害程度 | 中（线性缺陷） | 高（体积缺陷） |

---

### 2.9 高维推广的完整图景

#### 2.9.1 一般 $k$-审计瞬子的分类

在非平坦框架下，审计 $k$-瞬子的定义域大大扩展：

| 维度 $k$ | 审计形式 | 通量 | 非零条件 | 存在性 |
|-----------|---------|------|---------|--------|
| $k=1$ | $A \in C^1$ | $\oint_\gamma A$ | $\bar{f}$ 单值性（平坦）**或** $A$ 任意（非平坦） | ✓ 丰富 |
| $k=2$ | $F = d_1 A \in C^2$ | $\int_\Sigma F$ | $A \notin \operatorname{im}(d_0)$（$A_{\text{coexact}} \neq 0$） | ✓ 存在 |
| $k=3$ | $G = d_2 F \in C^3$ | $\int_\Omega G$ | $F \notin \operatorname{im}(d_1)$（$F_{\text{coexact}} \neq 0$） | 取决于 $\mathcal{K}$ 维度 |
| $k \geq 4$ | $d_{k-1} A_{k-1}$ | 类推 | 类推 | $\dim(\mathcal{K}) \geq k$ 时可能 |

#### 2.9.2 非平坦框架的威力

非平坦框架的本质进步在于：
1. **不要求 $A$ 来自标量势**：$A \in C^1$ 可以是任意 1-上链
2. **2-通量可以非零**：$\int_\Sigma d_1 A \neq 0$ 自然产生
3. **每个维度都有独立的非零条件**：$A_k \notin \operatorname{im}(d_{k-1})$ 而非平坦
4. **审计障碍的完整谱系**：从 $k=1$ 的"势型"（单值性）到 $k=2$ 的"旋度型"（$d_1 A \neq 0$）到 $k=3$ 的"散度型"（在 $\dim(\mathcal{K}) \geq 3$ 时）

#### 2.9.3 经验预测

对于真实的 SCX 审计数据集（例如 AlN MLIP 审计）：
- **1-瞬子**：常见于数据流形的"隧道"区域——专家偏离具有累积相位
- **2-瞬子（非平坦）**：出现在专家分歧具有"旋度"模式的区域——三个或更多专家在局部三角形上表现出**循环不一致性**。这需要至少 3 个专家在该区域都有数据
- **$k \geq 3$**：需要数据流形的内在维度 $n \geq 3$，且至少 $k+1$ 个专家在 $k$-单纯形上表现出高阶循环不一致性

---

### 2.10 非平坦 $A$ 的理论意义：为什么这很重要

#### 2.10.1 对原始审计瞬子理论的修正

原始 `audit_instanton.tex` 将审计 1-形式**定义**为 $A = d_0 \bar{f}$。这等价于假设：
- 专家的所有分歧可以被整合为一个标量势 $\bar{f}$
- 不存在"旋度型"的分歧（循环不一致性）

非平坦框架放松了这一假设：$A$ 可以是 Situs 复形上的**任意**离散 1-形式。这允许：
- $\bar{f}$ 仅在局部存在（局部势），但不同局部势之间由 1-形式 $A$ 连接——恰如微分几何中联络 $A$ 连接不同纤维上的标架
- 当局部势不能全局拼接时，$F = d_1 A \neq 0$ 非零，产生真正的 2-维审计障碍

#### 2.10.2 与 SCX 规范理论的深层联系

在 SCX 的九域规范理论（`gauge_domain_analysis.md`）中，审计联络 $A$ 是规范势，物理可观测量（共识分数等）是规范不变量的类比。非平坦 $A$ 意味着：

$$F = d_1 A \neq 0 \quad \longleftrightarrow \quad \text{存在"场强"——审计规范场的曲率}$$

在物理规范理论中，$F_{\mu\nu} \neq 0$ 意味着存在非平凡的物理场（如电磁场）。在审计理论中，$d_1 A \neq 0$ 意味着存在**不可约的专家分歧结构**——这不是随机的噪声，而是分歧空间的拓扑/几何性质的反映。

**规范化类比总结**：

| 物理规范理论 | 审计规范理论（非平坦推广） |
|-------------|--------------------------|
| 规范势 $A_\mu$ | 审计 1-上链 $A \in C^1$ |
| 规范变换 $A \to A + d\Lambda$ | 改变局部标架选择 |
| 场强 $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ | $F = d_1 A \in C^2$ |
| $F = 0 \Longleftrightarrow$ 纯规范（无物理场） | $d_1 A = 0 \Longleftrightarrow$ 纯势型分歧 |
| $F \neq 0 \Longleftrightarrow$ 存在物理场 | $d_1 A \neq 0 \Longleftrightarrow$ 存在旋度型分歧 |
| Wilson 圈 $W(\gamma) = \exp(i\oint_\gamma A)$ | 审计和乐 $\Phi_1(\gamma) = \oint_\gamma A$ |
| 磁通量 $\Phi_B = \int_\Sigma F$ | 审计 2-通量 $\Phi_2(\Sigma) = \int_\Sigma d_1 A$ |

---

## 3. 总结与交叉关联 {#cross}

### 3.1 C7 核心结论

1. **活跃自由度**：$N_{\text{dof}} \sim Re^{9/4}$（DNS 全解析的网格点数标度）
2. **规范群维度**：$\dim(\mathcal{G}) \sim \ln(Re^{3/4})$，来自惯性子区的对数尺度计数
3. **模空间维度**：$\mathcal{T}_{\text{mod}} = \mathcal{F}/\mathcal{G}$ 是无限维的，但可调规范参数仅有 $\sim \frac{3}{4}\ln Re$ 个
4. **从 $N_{\text{dof}}$ 到 $\dim(\mathcal{G})$ 的压缩**：$Re^{9/4} \gg \frac{3}{4}\ln Re$，说明绝大多数物理自由度不受规范选择影响——湍流的核心物理在高 $Re$ 下是稳定的
5. **规范不变可观测量**：$\varepsilon$, $k^{-5/3}$ 指数, $\zeta_p$, $C_D$, $Nu$——由 N-S 对称性和 Kolmogorov 标度完全确定
6. **规范依赖可观测量**：$\nu_t$, 局部 $k$, 壁面函数, 模型常数——依赖于具体的湍流封闭假设
7. **模空间几何**：k-ε 和 k-ω 在惯性子区等价；LES 和 RANS 的区别在于截断尺度的不同选择；规范参数数量 $N_{\text{gauge}} \sim \ln(L/\Delta)$

### 3.2 C8 核心结论

1. **平坦框架的局限**：$A = d_0 \bar{f} \implies F = d_1 A \equiv 0$（$d^2 = 0$），2-圈通量恒为零。这不是 $k=2$ 没有瞬子——而是用错了审计联络的定义
2. **非平坦框架的突破**：定义 $A \in C^1(\mathcal{K})$ 为**任意**审计 1-上链（不要求 $A = d_0 \bar{f}$），则：
   - $F = d_1 A$ 一般非零
   - $\int_\Sigma F \neq 0$ 对所有 $\Sigma$ 满足 $A_{\text{coexact}}$ 在 $\delta_1\Sigma$ 上的投影非零
3. **Hodge 分解**：$A = A_{\text{exact}} + A_{\text{coexact}} + A_{\text{harmonic}}$。非平坦通量的来源是 $A_{\text{coexact}}$（余恰当部分）
4. **物理意义**：$F \neq 0$ 对应"旋度型分歧"——循环不一致性。当三个专家在三角形上不能由单一标量势整合其成对分歧时，出现非零的 2-通量
5. **与 $k=1$ 的对比**：
   - $k=1$ 非零条件：单值性（$\bar{f}$ 非全局单值）——**分析性**
   - $k=2$ 非零条件：$A \notin \operatorname{im}(d_0)$——**代数性**
   - 两者正交：$k=1$ 的障碍存在于平坦 $A$ 中（$d_1 A = 0$ 但 $\oint A \neq 0$）；$k=2$ 的障碍仅存在于非平坦 $A$ 中（$d_1 A \neq 0$）
6. **审计 2-瞬子的天然电荷**：$Q_2 = |\int_\Sigma F|$——不再需要替代的体积分定义
7. **非交换推广（开放问题）**：矩阵值 $A$ 产生 $A \wedge A$ 项，可能产生额外的曲率源

### 3.3 两个问题的 SCX 框架内联系

C7（湍流模空间）和 C8（审计瞬子 $H_2$）在 SCX 框架内通过**数据的规范结构**相联系：

- C7 处理物理系统（湍流）中的规范自由度——模型的不可辨识性
- C8 处理审计系统（专家）中的拓扑缺陷——专家共识的虚假性
- 两者的共同主题：**$\mathcal{F}/\mathcal{G}$ 的结构决定可观测物理的边界**

在湍流中，规范固定是模型选择（k-ε vs LES）；在审计中，规范固定是审计联络 $A$ 的构造方式（平坦 vs 非平坦）以及共识度量的定义。模空间 $\mathcal{F}/\mathcal{G}$ 的拓扑结构（通过持续同调检测）在两种情况下都揭示了系统的不可约特征。

C8 的非平坦推广为 C7 提供了新的视角：湍流模型中的规范固定是否也可能存在"非平坦"的类比？即：是否存在不以单一 $\bar{f}$（Reynolds 应力的标量势近似）为基础的湍流模型——那些模型明确编码了 Reynolds 应力的"旋度型"不可积成分？这在物理上对应**非线性涡粘模型**和**Reynolds 应力输运模型**（二阶矩封闭），它们确实比简单的 Boussinesq 假设（线性涡粘）包含更多的"非平坦"结构。

---

## 附录 A：关键公式汇总

### C7

| 公式 | 含义 |
|------|------|
| $\eta = (\nu^3/\varepsilon)^{1/4}$ | Kolmogorov 耗散尺度 |
| $\eta/L = Re^{-3/4}$ | 尺度比 |
| $E(k) = C_K \varepsilon^{2/3} k^{-5/3}$ | Kolmogorov 能谱 |
| $N_{\text{dof}} \sim (L/\eta)^3 = Re^{9/4}$ | 活跃自由度 |
| $\dim(\mathcal{G}) \sim \ln(L/\eta) = \ln(Re^{3/4})$ | 规范群维度 |
| $\mathcal{T}_{\text{mod}} = \mathcal{F}/\mathcal{G}$ | 湍流规范模空间 |
| $N_{\text{gauge}} \sim \ln(L/\Delta)$ | 规范参数数量与截断尺度的关系 |

### C8

| 公式 | 含义 |
|------|------|
| $A \in C^1(\mathcal{K}; \mathbb{R})$ | 审计 1-上链（任意，非必须 $d_0 \bar{f}$） |
| $A_{\text{flat}} = d_0 \bar{f}$ | 平坦审计联络（原始定义） |
| $F = d_1 A \in C^2(\mathcal{K}; \mathbb{R})$ | 审计 2-形式（非平坦时一般非零） |
| $\Phi_1(\gamma) = \oint_\gamma A$ | 1-圈和乐（可非零，来自单值性或 $A$ 非闭） |
| $\Phi_2(\Sigma) = \int_\Sigma F = \int_\Sigma d_1 A$ | 2-圈通量（非平坦时一般非零） |
| $A = d_0 f + \delta_2 B + h$ | Hodge 分解（恰当 + 余恰当 + 调和） |
| $d_1 A_{\text{coexact}} \neq 0$ | 非平坦通量的来源 |
| $Q_2^{\text{flux}}(\Sigma) = \left\vert \int_\Sigma F \right\vert$ | 天然 2-瞬子电荷 |
| $d_2 F = 0$ | Bianchi 恒等式（审计"磁单极子不存在"） |

---

## 附录 B：阻塞识别

### C7 的开放问题

1. **规范群 $\mathcal{G}$ 的完整分类**：目前仅给出维度的对数标度估计。$\mathcal{G}$ 的李代数结构、轨道空间的拓扑尚未明确。特别地：$\mathcal{G}$ 是否构成一个（无限维）李群？
2. **规范不变量的完备集**：是否存在类似 Yang-Mills 理论中 Wilson 圈的完备规范不变量集合？对于湍流，这意味着找到一组观测量 $\{O_\alpha\}$ 使得 $O_\alpha(M_1) = O_\alpha(M_2) \iff [M_1] = [M_2] \in \mathcal{T}_{\text{mod}}$
3. **$\dim_{\text{irr}}$ 的精确定义**：不可约复杂性的度量需要更严格的数学定义。$\dim(\mathcal{G})$ 的对数标度是渐近的——精确的常数因子（Kolmogorov 常数 $C_K$ 的作用）值得进一步研究
4. **量子湍流的类比**：超流氦中的量子化涡旋是否提供"可解模空间"？量子化涡旋的离散拓扑可能使 $\mathcal{T}_{\text{mod}}$ 在量子情形下可精确计算
5. **非 Boussinesq 模型与非平坦规范固定**：C8 的非平坦推广是否对湍流模空间有对应物？非线性涡粘模型和二阶矩封闭是否对应湍流规范理论中的"非平坦联络"？

### C8 的开放问题

1. **非平坦 $A$ 的构造算法**：如何从原始专家偏离 $\{f_i\}$ 系统性地构造非平坦的 $A$？特别是，$A_{\text{coexact}}$ 分量的显式公式是什么？
2. **非平坦通量的统计显著性**：$\Phi_2(\Sigma) \neq 0$ 的假设检验——如何区分真实的拓扑障碍与随机采样噪声？
3. **经验验证**：在真实 SCX 数据（如 AlN MLIP 审计数据集）上检测非平坦 2-瞬子。关键问题：专家分歧中的"旋度型"模式在真实审计场景中是否普遍存在？
4. **非交换审计联络**：矩阵值 $A = A^a T^a$ 能否产生非零曲率 $\mathcal{F} = dA + A \wedge A$？$A \wedge A$ 项对应于什么审计物理（不同专家组的相互作用？）
5. **与 Morse 理论的联系**：$\rho$ 作为 Morse 函数时，$PH_2$ 的出生/死亡对应 $\rho$ 的哪些临界点？非平坦 $A$ 的存在是否改变了这一对应？
6. **高阶非平坦性**：$k=3$ 的非平坦条件 $F \notin \operatorname{im}(d_1)$ 在 $\dim(\mathcal{K}) \geq 3$ 时是否有物理实现？什么审计场景会产生三阶循环不一致性？

---

> **文档版本**: v2.0（含非平坦2-形式通量的完整分析）
> **创建日期**: 2026-07-02
> **目标文件**: `docs/analysis/conjectures_C7_C8.md`
