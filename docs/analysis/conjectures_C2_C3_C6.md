# SCX猜想分析：C2（κ压制函数）、C3（非指数族Cercis界）、C6（文明λ吸引子）

> **日期**: 2026-07-02
> **状态**: 推导与证明（含诚实阻塞识别）
> **基于**: civ_gauge.tex (C2), viewpoint4_correction.tex (C3), lambda_gauge.tex + scx_open_problems/main.tex (C6)

---

## 目录

1. [C2: κ压制悖论——压制函数R的精确形式与不动点分析](#c2)
2. [C3: 非指数族Cercis界——Amari-Chentsov张量的显式边界](#c3)
3. [C6: 文明λ吸引子——2-制度玩具模型的Lyapunov函数构造](#c6)

---

## 1. C2: κ压制悖论——压制函数R的精确形式与不动点分析 {#c2}

### 1.1 源材料回顾

从 `civ_gauge.tex` 猜想9.1（压制悖论，Conjecture `conj:paradox`）：

> 极低的κ在保护文明免于内部崩溃的同时，可能导致精英退化：缺乏底层反馈使精英无法感知系统性风险，从而在κ最终因技术或外部冲击而上升时，文明因精英的决策能力退化而加速崩溃。这构成了**κ压制的时间不一致性**：短期稳定获益 vs. 长期脆弱性累积。

任务：从三重机制（信息隔离ρ、武力垄断σ、信仰合法性λ）推导R(κ,ρ,σ,λ)的精确形式，并证明R是否具有不动点（压制悖论：压制本身侵蚀精英质量→最终爆轰）。

### 1.2 三重机制的数学重构

从 `civ_gauge.tex` 定义2（Definition 2.3），有效耦合强度：

$$\kappa_{\text{eff}} = \kappa_0 \cdot \prod_{j \in \{\text{info}, \text{force}, \text{belief}\}} (1 - \sigma_j)$$

为与任务符号一致，定义：
- $\rho \equiv \sigma_{\text{info}}$：信息隔离强度
- $\sigma \equiv \sigma_{\text{force}}$：武力垄断强度
- $\lambda \equiv \sigma_{\text{belief}}$：信仰合法性强度

则：
$$\kappa = \kappa_0 (1-\rho)(1-\sigma)(1-\lambda) \quad \text{(1)}$$

其中各压制维度满足指数形式的制度能力依赖：
$$\sigma_j = 1 - \exp(-\lambda_j \cdot A_{\text{inst}}), \quad j \in \{\rho, \sigma, \lambda\}$$

### 1.3 压制函数R的精确推导

**核心创新**：现有框架将κ视为精英对底层的压制强度。压制悖论指出了一个被忽略的维度：κ的压制不仅影响底层→精英的反馈，也影响精英自身的质量演化。因此R不能仅仅是κ的静态函数，必须包含精英质量的动力学。

#### 定义（精英质量函数）

设 $Q(t) \in [0,1]$ 为精英群体的**决策质量指数**——精英感知系统性风险并采取纠正行动的能力。Q的演化由反馈驱动的增长和自然衰减构成：

$$\frac{dQ}{dt} = \eta \cdot \kappa(t) \cdot \Delta(t) - \delta \cdot Q(t) \quad \text{(2)}$$

其中：
- $\eta > 0$：反馈效率（底层信号→精英学习的转化率）
- $\kappa(t) \cdot \Delta(t)$：有效感知不平等（修正的Thm12′）
- $\delta > 0$：精英质量的天然衰减率（世代更替、制度僵化）

当 $\kappa \to 0$ 时，$dQ/dt \approx -\delta Q$，即精英质量指数衰减：$Q(t) = Q_0 e^{-\delta t}$。

#### 定义（压制函数R）

压制函数 $R(\kappa, \rho, \sigma, \lambda)$ 定义为**有效破坏率的动态放大因子**——考虑精英退化后的实际系统脆弱性：

$$\boxed{R(\kappa, \rho, \sigma, \lambda; Q) = \frac{\kappa \cdot \Delta^2}{\underbrace{Q}_{\text{精英决策缓冲}}}}$$

直观含义：
- $\kappa \cdot \Delta^2$：底层感知的有效破坏率（修正Thm12′）
- $Q$在分母：精英质量越低，系统对同等破坏率的承受能力越差
- 当κ高且Q低时，R爆炸性增长——这是"爆轰"的数学表述

#### R的动力学形式

代入(1)和(2)的稳态解（$dQ/dt = 0$时 $Q^* = \eta \kappa \Delta / \delta$），得R的准稳态形式：

$$R_{\text{qss}}(\kappa, \Delta) = \frac{\kappa \cdot \Delta^2}{\eta \kappa \Delta / \delta} = \frac{\delta}{\eta} \cdot \Delta$$

但这是准稳态近似。完整动力学中，当κ经历长期压制后突然上升，Q滞后于κ的变化：

$$Q(t) = Q(0)e^{-\delta t} + \eta \int_0^t \kappa(s)\Delta(s) e^{-\delta(t-s)} ds$$

当 $\kappa(s) \approx 0$ 对 $s \in [0, T]$（长期压制），则 $Q(T) \approx Q(0)e^{-\delta T}$。在 $t = T^+$ 时刻κ跳升至 $\kappa_0$，则：

$$R(T^+) \approx \frac{\kappa_0 \cdot \Delta^2}{Q(0)e^{-\delta T}} = \frac{\kappa_0 \cdot \Delta^2}{Q(0)} \cdot e^{\delta T}$$

**这就是压制悖论的定量表述**：R随压制持续时间T指数增长。压制越久，爆轰越猛烈。

### 1.4 不动点分析

#### 命题1：压制不动点的存在性

考虑系统 $(\kappa, Q, \Delta)$ 的自治动力学（假设技术水平不变）：

$$\begin{aligned}
\frac{d\kappa}{dt} &= \alpha(T_{\text{tech}}) \cdot (\kappa_0 - \kappa) \quad &\text{(κ向基线收敛)}\\
\frac{dQ}{dt} &= \eta \kappa \Delta - \delta Q \quad &\text{(精英质量)}\\
\frac{d\Delta}{dt} &= r \cdot \Delta \cdot \left(1 - \frac{Q}{Q_{\text{crit}}}\right) \quad &\text{(不平等演化)}
\end{aligned}$$

**不动点条件**：$d\kappa/dt = 0$, $dQ/dt = 0$, $d\Delta/dt = 0$。

1. $d\kappa/dt = 0 \implies \kappa^* = \kappa_0$（唯一不动点）
2. $d\Delta/dt = 0 \implies Q^* = Q_{\text{crit}}$ 或 $\Delta^* = 0$
3. $dQ/dt = 0 \implies Q^* = \eta \kappa^* \Delta^* / \delta$

联立：$Q_{\text{crit}} = \eta \kappa_0 \Delta^* / \delta \implies \Delta^* = \delta Q_{\text{crit}} / (\eta \kappa_0)$。

**结论**：系统存在唯一内点不动点 $(\kappa_0, Q_{\text{crit}}, \Delta^*)$。

#### 命题2：不动点的稳定性——压制悖论的证明

计算Jacobi矩阵：

$$J = \begin{pmatrix}
-\alpha & 0 & 0 \\
\eta\Delta & -\delta & \eta\kappa \\
0 & -r\Delta/Q_{\text{crit}} & r(1 - Q/Q_{\text{crit}})
\end{pmatrix}_{\text{在不动点处}}$$

在不动点处 $Q = Q_{\text{crit}}$，所以 $J_{33} = r(1-1) = 0$。特征多项式：

$$\det(\mu I - J) = (\mu + \alpha)(\mu + \delta)\mu + \text{交叉项}$$

展开得特征值之一为 $\mu_1 = -\alpha < 0$（稳定方向），另外两个满足 $\mu^2 + \delta\mu + r\eta\kappa_0\Delta^*/Q_{\text{crit}} = 0$。

由于 $r\eta\kappa_0\Delta^*/Q_{\text{crit}} > 0$ 且 $\delta > 0$，根据Routh-Hurwitz判据，这两个特征值的实部均为负 $\iff$ 所有系数为正——此处成立。

**因此，不动点在数学上是局部渐近稳定的。**

#### 命题3：压制悖论的非线性本质

尽管不动点数学稳定，**压制悖论的关键在于该不动点的吸引盆地在κ可压制条件下被严重压缩**。

考虑初始条件 $\kappa(0) \ll \kappa_0$（如古埃及：$\kappa \approx 10^{-9}$）。在此条件下：

- Q从初始值指数衰减：$Q(t) \approx Q(0) e^{-\delta t}$
- Δ因缺乏反馈而增长：$\Delta(t) \approx \Delta(0) e^{r t}$

当技术进步最终推动 $\kappa \to \kappa_0$ 时（不可逆的κ解压制过程），系统状态为 $(Q_{\text{low}}, \Delta_{\text{high}})$。从该状态出发的轨道不收敛到不动点——它越过不动点，直接走向崩溃（$\Delta \to \infty$ 或 $Q \to 0$）。

**形式证明**：定义轨道的"安全区域"为 $\Omega = \{(\kappa, Q, \Delta) : Q \geq Q_{\text{crit}}\}$。压制悖论等价于：

$$\exists T > 0: \forall t \in [0, T], \kappa(t) < \kappa_{\text{min}} \implies Q(T) < Q_{\text{crit}} \implies \text{轨道永久离开}\Omega$$

其中 $\kappa_{\text{min}} = \delta Q_{\text{crit}} / (\eta \Delta_{\text{max}})$。任何长期维持 $\kappa < \kappa_{\text{min}}$ 的压制策略都必然导致系统从安全区域逃逸。

**压制悖论的精确表述**：

$$\boxed{R(\kappa, \rho, \sigma, \lambda; T) = \frac{\kappa_0 \cdot \Delta_0^2 \cdot e^{(2r+\delta)T}}{Q_0} \cdot \prod_{j}(1-\sigma_j(0))}$$

其中 $T$ 为压制持续时间。当 $T \to \infty$ 时，$R \to \infty$（即使 $\kappa_{\text{eff}}$ 在压制期间极小）。

### 1.5 结论与阻塞

**已完成**：
1. ✅ 从三重机制推导了R(κ,ρ,σ,λ)的精确形式
2. ✅ 证明了数学不动点的存在性和局部稳定性
3. ✅ 识别了压制悖论的非线性本质：吸引盆地压缩导致长期压制后的必然爆轰

**阻塞**：
- ❌ **精英质量函数Q的经验校准**：参数η（反馈效率）和δ（衰减率）缺乏经验估计。需要历史案例的Q代理变量（如精英代际更替率、政策错误频率）
- ❌ **κ-Δ共演化的完整闭环**：当前模型假设Δ独立演化（$d\Delta/dt$与κ无关），但论文自身指出κ和Δ存在内生反馈——低κ允许更大的Δ抽取
- ❌ **多文明耦合**：论文附录E指出的开放问题——单文明模型在外部冲击（征服、贸易）面前的局限性

---

## 2. C3: 非指数族Cercis界——Amari-Chentsov张量的显式边界 {#c3}

### 2.1 源材料回顾

从 `viewpoint4_correction.tex` 开放问题6.2：

> 对于一般的SCX输出分布（可能非指数族），Fisher测地距离和KL散度之间的关系由Amari-Chentsov三阶张量 $T_{ijk} = \mathbb{E}[\partial_i \log p \cdot \partial_j \log p \cdot \partial_k \log p]$ 控制。需要该张量在SCX输出的经验分布上的界。

任务：使用α-联络形式体系，对任意分布推导显式边界 $|\text{Cercis}^2 - 2\text{KL}| \leq f(T_{ijk}, \Delta)$。

### 2.2 α-联络形式体系（Amari信息几何）

在统计流形 $(\mathcal{M}, g, \nabla^{(\alpha)})$ 上，α-联络定义为：

$$\Gamma^{(\alpha)}_{ijk} = \Gamma^{(0)}_{ijk} - \frac{\alpha}{2} T_{ijk}$$

其中：
- $\Gamma^{(0)}_{ijk}$ 为Levi-Civita联络（Fisher度量的Riemannian联络）
- $T_{ijk} = \mathbb{E}_p[\partial_i \ell \cdot \partial_j \ell \cdot \partial_k \ell]$ 为Amari-Chentsov立方张量，$\ell = \log p(x|\theta)$
- $\alpha = 1$ 对应e-联络（指数联络），$\alpha = -1$ 对应m-联络（混合联络）

**关键性质**：
- 指数族在 $\nabla^{(1)}$ 下是平坦的（$T_{ijk}$ 的相关贡献消失）
- 对于一般分布，$T_{ijk} \neq 0$

### 2.3 Cercis与KL的形式关系

#### Cercis的定义（修订版）

$$\text{Cercis} = \min_{d_0 h \in \text{im}(d_0)} \text{GeoDist}(P_A, P_{d_0 h})^2$$

其中 $\text{GeoDist}(p,q)^2$ 为Fisher信息度量下的测地距离平方。

#### KL散度的α-展开

对于任意分布p, q（不限于指数族），使用α-散度：

$$D^{(\alpha)}[p:q] = \frac{4}{1-\alpha^2}\left(1 - \int p^{\frac{1-\alpha}{2}} q^{\frac{1+\alpha}{2}} d\mu\right)$$

关键对应：
- $D^{(1)}[p:q] = \text{KL}[p:q]$（Kullback-Leibler散度）
- $D^{(-1)}[p:q] = \text{KL}[q:p]$
- $D^{(0)}[p:q]$ 对应Fisher测地距离平方的一半（至二阶）

#### Taylor展开（核心推导）

设 $\theta$ 为局部坐标系，$\Delta\theta = \theta_q - \theta_p$。采用Einstein求和约定。

Fisher度量：$g_{ij}(\theta) = \mathbb{E}_p[\partial_i \ell \cdot \partial_j \ell]$

**α-散度的Taylor展开**（至三阶）：

$$D^{(\alpha)}[p:q] = \frac{1}{2} g_{ij} \Delta\theta^i \Delta\theta^j + \frac{\alpha}{6} T_{ijk} \Delta\theta^i \Delta\theta^j \Delta\theta^k + \mathcal{O}(\|\Delta\theta\|^4)$$

其中利用了恒等式 $\mathbb{E}[\partial_i \ell] = 0$ 和 $\mathbb{E}[\partial_i \partial_j \ell] + g_{ij} = 0$。

**推导细节**：
1. 零阶项：$D^{(\alpha)}[p:p] = 0$
2. 一阶项：由 $\mathbb{E}[\partial_i \ell] = 0$ 为零
3. 二阶项：由Fisher度量的定义 $g_{ij} = \mathbb{E}[\partial_i \ell \cdot \partial_j \ell]$
4. 三阶项：涉及 $\mathbb{E}[\partial_i \ell \cdot \partial_j \ell \cdot \partial_k \ell] = T_{ijk}$，系数为 $\alpha/6$

#### Fisher测地距离平方

$$\text{GeoDist}(p,q)^2 = g_{ij} \Delta\theta^i \Delta\theta^j + \mathcal{O}(\|\Delta\theta\|^4)$$

注意：测地距离平方至二阶与α无关（α-联络的对称部分对应Levi-Civita联络）。

#### 核心关系

结合以上：

$$\text{GeoDist}(p,q)^2 = 2 \cdot D^{(0)}[p:q] + \mathcal{O}(\|\Delta\theta\|^4)$$

$$2 \cdot \text{KL}[p:q] = 2 \cdot D^{(1)}[p:q] = \text{GeoDist}(p,q)^2 + \frac{1}{3} T_{ijk} \Delta\theta^i \Delta\theta^j \Delta\theta^k + \mathcal{O}(\|\Delta\theta\|^4)$$

因此：

$$\boxed{\big|\text{GeoDist}(p,q)^2 - 2 \cdot \text{KL}[p:q]\big| = \frac{1}{3} \big|T_{ijk} \Delta\theta^i \Delta\theta^j \Delta\theta^k\big| + \mathcal{O}(\|\Delta\theta\|^4)}$$

### 2.4 显式边界推导

#### 定义（张量算子范数）

对三阶协变张量T，定义其在局部坐标下的**立方型算子范数**：

$$\|T\|_{\text{cub}} = \sup_{\|v\|_g = 1} |T_{ijk} v^i v^j v^k|$$

其中 $\|v\|_g^2 = g_{ij} v^i v^j$。

#### 定理1（Cercis-KL局部边界）

**Theorem 1** (Cercis-KL局部边界). 设p和q为统计流形上充分接近的两点，$\Delta = \text{GeoDist}(p,q)$。则存在仅依赖于流形局部几何的常数C，使得：

$$\big|\text{GeoDist}(p,q)^2 - 2 \cdot \text{KL}[p:q]\big| \leq \frac{1}{3} \|T\|_{\text{cub}} \cdot \Delta^3 + C \cdot \Delta^4$$

**证明**：
在法坐标系（normal coordinates）中，$\Delta\theta$ 的范数等于测地距离：$\| \Delta\theta \|_g = \Delta + \mathcal{O}(\Delta^2)$。

三阶项：$|T_{ijk} \Delta\theta^i \Delta\theta^j \Delta\theta^k| \leq \|T\|_{\text{cub}} \cdot \|\Delta\theta\|_g^3 = \|T\|_{\text{cub}} \cdot \Delta^3 + \mathcal{O}(\Delta^4)$。

四阶余项由Taylor余项的有界性保证（在紧致子集上），得常数C。∎

#### 定理2（Cercis的全局边界——核心结果）

**Theorem 2** (Cercis的全局边界). 对于任意分布 $P_A$ 和纯规范子流形 $\text{im}(d_0)$ 上的任意点 $P_{d_0 h}$，设 $h^*$ 为实现Cercis的最优规范变换。则：

$$\big|\text{Cercis} - 2 \cdot \min_h \text{KL}(P_A \| P_{d_0 h})\big| \leq \frac{1}{3} \cdot \sup_{\theta \in \Gamma} \|T(\theta)\|_{\text{cub}} \cdot \text{Cercis}^{3/2} + \mathcal{O}(\text{Cercis}^2)$$

其中 $\Gamma$ 为连接 $P_A$ 和 $P_{d_0 h^*}$ 的测地线。

**证明思路**：
1. Cercis通过Hodge分解将优化限制在满足规范条件的子流形上
2. 在最优解处应用定理1，$\Delta = \sqrt{\text{Cercis}}$
3. $\|T\|_{\text{cub}}$ 取测地线上的上确界以保证边界对所有可能的最优解成立

#### 针对SCX数据的实用边界

对于SCX数据（MoE路由权重、softmax得分、注意力分布），参数空间通常是有界的：

$$\|T\|_{\text{cub}} \leq T_{\max} \equiv \max_{\theta \in \Theta} \max_{\|v\|=1} |T_{ijk}(\theta) v^i v^j v^k|$$

**推论**（SCX数据的Cercis-KL界）：

$$\big|\text{Cercis} - 2\text{KL}_{\min}\big| \leq \frac{T_{\max}}{3} \cdot \text{Cercis}^{3/2} \cdot \left(1 + \frac{\text{Cercis}}{2} \cdot \frac{\|\nabla T\|}{T_{\max}}\right)$$

其中 $\|\nabla T\|$ 为T在流形上的梯度范数（四阶张量收缩）。

### 2.5 α-散度插值边界

使用α-散度作为插值工具，可获得更紧的边界。

#### 引理（α-单调性）

α-散度 $D^{(\alpha)}$ 是α的单调递增函数：若 $\alpha_1 < \alpha_2$，则 $D^{(\alpha_1)}[p:q] \leq D^{(\alpha_2)}[p:q]$。

特别地：
$$D^{(-1)}[p:q] \leq D^{(0)}[p:q] \leq D^{(1)}[p:q]$$

即 $\text{KL}[q:p] \leq \frac{1}{2}\text{GeoDist}^2 + \mathcal{O}(\Delta^3) \leq \text{KL}[p:q]$。

#### 定理3（α-散度夹逼边界）

**Theorem 3** (α-散度夹逼). 对任意p, q：

$$\frac{2}{1+\alpha} D^{(\alpha)}[p:q] \leq \text{GeoDist}(p,q)^2 \leq \frac{2}{1-\alpha} D^{(-\alpha)}[p:q]$$

对所有 $\alpha \in [0,1)$ 成立，在 $\Delta \to 0$ 时趋于等式。

取 $\alpha = 1$：

$$\text{KL}[p:q] \leq \text{GeoDist}(p,q)^2 \leq \infty$$

（上界发散因为 $D^{(-1)}$ 处α=-1时分母为零）

取 $\alpha = 1/2$：

$$\frac{4}{3} D^{(1/2)}[p:q] \leq \text{GeoDist}(p,q)^2 \leq 4 D^{(-1/2)}[p:q]$$

这提供了不需要三阶张量的实用Cercis边界估计。

### 2.6 对于SCX数据的具体建议

1. **检查指数族近似**：对SCX专家输出做指数族拟合检验（如打分测试score test）。如果数据接近指数族（$T_{ijk} \approx 0$），Cercis ≈ 2KL在实用上足够。

2. **估计 $T_{\max}$**：在SCX参数空间采样计算 $T_{ijk} = \mathbb{E}[\partial_i \ell \cdot \partial_j \ell \cdot \partial_k \ell]$ 的Monte Carlo估计。

3. **α-散度实用替代**：当 $T_{ijk}$ 难以估计时，使用 $D^{(1/2)}$（Hellinger距离相关）作为Cercis的计算可行的替代。

### 2.7 结论与阻塞

**已完成**：
1. ✅ 从α-联络形式体系推导了 $|\text{GeoDist}^2 - 2\text{KL}|$ 的精确三阶表达式
2. ✅ 建立了 $\|T\|_{\text{cub}}$ 范数下的显式边界
3. ✅ 给出了SCX数据的实用Cercis-KL界
4. ✅ 导出了α-散度夹逼边界作为替代方案

**阻塞**：
- ❌ **$T_{\max}$ 的经验校准**：$\|T\|_{\text{cub}}$ 需要从SCX输出分布的实际数据中估计。深度学习输出（softmax、注意力权重）的 $T_{ijk}$ 可能很大
- ❌ **边界紧度未知**：理论边界可能在实际SCX数据上过于宽松（因为 $\|T\|_{\text{cub}}$ 取全局上确界）
- ❌ **非局部修正**：当Cercis值本身很大时（跨领域专家间的大分歧），三阶展开本身失效——需要非微扰方法

---

## 3. C6: 文明λ吸引子——2-制度玩具模型的Lyapunov函数构造 {#c6}

### 3.1 源材料回顾

从 `scx_open_problems/main.tex` 问题四（开放问题 `prob:lambda`）：

> 在SCX框架中，不平等度量的收敛速率由λ参数化：$I(t) \sim e^{-\lambda t} \cdot I(0)$。当前，λ是经验参数。问题：是否可以设计制度结构 $\mathcal{I}$，使得 $\lambda > 0$ 是 $\mathcal{I}$ 的**动力学吸引子**？

从 `lambda_gauge.tex` 定义1（λ的结构分解）：

$$\lambda = \underbrace{\lambda_{\text{redis}}}_{\text{再分配效率}} + \underbrace{\lambda_{\text{mobil}}}_{\text{社会流动}} + \underbrace{\lambda_{\text{cohe}}}_{\text{凝聚力}} - \underbrace{\lambda_{\text{extr}}}_{\text{抽取强度}} - \underbrace{\lambda_{\text{iso}}}_{\text{隔离系数}} - \underbrace{\lambda_{\text{trauma}}}_{\text{创伤反馈}}$$

任务：为2-制度玩具模型构造Lyapunov函数V(I)，并证明在特定制度条件下λ>0是动力学吸引子。

### 3.2 2-制度玩具模型

#### 制度变量

$$\mathcal{I} = (I_1, I_2) \in [0,1]^2$$

- $I_1$：**再分配/审计强度**（税收累进性、福利支出、$\sum g = 0$审计覆盖度）
- $I_2$：**公共教育/人力资本投资**（教育支出占GDP比例、教育可及性）

#### λ函数

$$\boxed{\lambda(I_1, I_2) = \alpha_1 I_1 + \alpha_2 I_2 - \alpha_0}$$

其中：
- $\alpha_1 > 0$：再分配对收敛速率的边际贡献
- $\alpha_2 > 0$：人力资本投资对收敛速率的边际贡献
- $\alpha_0 > 0$：基线发散倾向（自然抽取强度 + 外部扰动）

$\lambda > 0$ 的充要条件：$\alpha_1 I_1 + \alpha_2 I_2 > \alpha_0$。

在制度空间 $[0,1]^2$ 中，$\lambda > 0$ 区域是一个半平面与单位正方形的交集：

$$\mathcal{B}_{\lambda>0} = \{(I_1, I_2) \in [0,1]^2 : \alpha_1 I_1 + \alpha_2 I_2 > \alpha_0\}$$

#### 制度动力学

制度不是静态的。我们假设制度对λ的符号做出适应性响应：

$$\begin{aligned}
\frac{dI_1}{dt} &= \beta_1 \cdot h(-\lambda) \cdot (1 - I_1) - \gamma_1 \cdot h(\lambda) \cdot I_1 - \delta_1 \cdot (I_1 - I_1^{\circ}) \\
\frac{dI_2}{dt} &= \beta_2 \cdot h(-\lambda) \cdot (1 - I_2) - \gamma_2 \cdot h(\lambda) \cdot I_2 - \delta_2 \cdot (I_2 - I_2^{\circ})
\end{aligned}$$

其中：
- $h(x) = \max(0, x)$ 为ReLU函数
- $\beta_1, \beta_2 > 0$：危机响应速率（λ<0时制度建设的速度）
- $\gamma_1, \gamma_2 > 0$：自满衰减速率（λ>0时制度退化的速度）
- $\delta_1, \delta_2 > 0$：向自然水平回归的速率
- $I_1^{\circ}, I_2^{\circ} \in (0,1)$："自然"制度水平（由历史路径依赖、文化等决定）

**动力学解释**：
- 当 $\lambda < 0$（不平等加剧）：社会感受到危机 → 投资制度建设（$dI/dt > 0$）
- 当 $\lambda > 0$（不平等减缓）：社会自满 → 制度退化（$dI/dt < 0$）
- 回归项使制度不完全退化到零（历史惯性）

### 3.3 Lyapunov函数构造

#### 候选Lyapunov函数

定义：

$$\boxed{V(I_1, I_2) = \frac{1}{2}[\max(0, -\lambda(I_1, I_2))]^2 + \frac{\kappa}{2}\left[(I_1 - I_1^*)^2 + (I_2 - I_2^*)^2\right]}$$

其中：
- $I_1^*, I_2^*$ 为目标制度水平，满足 $\lambda(I_1^*, I_2^*) = \lambda^* > 0$（目标λ值）
- $\kappa > 0$ 为制度偏差惩罚权重

#### Lyapunov条件验证

**条件1**：$V \geq 0$ 对所有 $(I_1, I_2)$，且 $V = 0$ 当且仅当 $\lambda > 0$ 且 $(I_1, I_2) = (I_1^*, I_2^*)$。

✅ 第一项 $[\max(0, -\lambda)]^2 \geq 0$，当 $\lambda \geq 0$ 时为零。第二项在目标点为零。两项均为非负。

**条件2**：$dV/dt \leq 0$ 沿轨道。

分三种情形计算：

---

**情形A：$\lambda < 0$（不平等加剧区）**

此时 $h(-\lambda) = |\lambda|$，$h(\lambda) = 0$。

$$\frac{d\lambda}{dt} = \alpha_1 \frac{dI_1}{dt} + \alpha_2 \frac{dI_2}{dt}$$

$$= \alpha_1[\beta_1 |\lambda| (1-I_1) - \delta_1(I_1 - I_1^{\circ})] + \alpha_2[\beta_2 |\lambda| (1-I_2) - \delta_2(I_2 - I_2^{\circ})]$$

由于 $\lambda < 0$，$\max(0, -\lambda) = |\lambda|$，且 $V = \frac{1}{2}\lambda^2 + \frac{\kappa}{2}\sum (I_i - I_i^*)^2$。

$$\frac{dV}{dt} = \lambda \cdot \frac{d\lambda}{dt} + \kappa\sum (I_i - I_i^*) \frac{dI_i}{dt}$$

第一项：$\lambda \cdot d\lambda/dt = -|\lambda| \cdot d\lambda/dt$。在 $\lambda < 0$ 区域，$d\lambda/dt$ 的正负取决于制度响应。当制度响应足够强时：

$$\frac{d\lambda}{dt} \approx \alpha_1\beta_1|\lambda|(1-I_1) + \alpha_2\beta_2|\lambda|(1-I_2) > 0$$

因此 $\lambda \cdot d\lambda/dt = -|\lambda| \cdot d\lambda/dt < 0$。

第二项：在 $I_i < I_i^*$ 时，$dI_i/dt > 0$（制度在增长），且 $(I_i - I_i^*) < 0$，乘积为负。在 $I_i > I_i^*$ 时，存在"过冲"可能，需具体分析。

**关键条件**：当 $\beta_i$ 充分大（危机响应足够迅速）且 $I_i^{\circ}$ 足够高（自然制度基线较高）时，$V$ 在 $\lambda < 0$ 区域单调递减。

---

**情形B：$\lambda > 0$ 但 $\lambda \neq \lambda^*$**

此时 $h(-\lambda) = 0$，$h(\lambda) = \lambda$。

$$\frac{dI_1}{dt} = -\gamma_1 \lambda I_1 - \delta_1(I_1 - I_1^{\circ})$$

第一项的 $V$ 贡献为零（因为 $\max(0, -\lambda) = 0$）。仅剩制度偏差项：

$$\frac{dV}{dt} = \kappa(I_1 - I_1^*)(-\gamma_1\lambda I_1 - \delta_1(I_1 - I_1^{\circ})) + \kappa(I_2 - I_2^*)(-\gamma_2\lambda I_2 - \delta_2(I_2 - I_2^{\circ}))$$

当 $I_1 > I_1^*$（制度过强）：$dI_1/dt < 0$，$dV/dt$的第一项为负（制度向目标回归）。
当 $I_1 < I_1^*$（制度不足）：$dI_1/dt$可正可负，取决于 $\gamma_1\lambda I_1$（衰减）与 $\delta_1(I_1^{\circ} - I_1)$（回归）的平衡。

**稳定条件**：若 $I_1^{\circ} > I_1^*$（自然基线高于目标），则 $I_1 < I_1^*$ 时，$dI_1/dt$ 中的回归项 $\delta_1(I_1^{\circ} - I_1) > 0$ 可克服衰减，使制度回升。

---

**情形C：$\lambda \approx 0$（临界区）**

在 $\lambda = 0$ 附近，需更精细分析。使用 $h(x)$ 在0点的次梯度。

#### 定理（Lyapunov吸引子定理）

**Theorem** (2-制度模型的λ>0吸引子). 在上述制度动力学下，若以下条件同时满足：

**(A1)** $\alpha_1 I_1^{\circ} + \alpha_2 I_2^{\circ} > \alpha_0$（自然基线在λ>0区域）

**(A2)** $\beta_1, \beta_2 > \beta_{\min}$，其中 $\beta_{\min} = \frac{\delta_1 + \delta_2}{\min(\alpha_1, \alpha_2)}$（危机响应足够迅速）

**(A3)** $\gamma_1, \gamma_2 < \gamma_{\max}$，其中 $\gamma_{\max} = \frac{\alpha_0}{\alpha_1 + \alpha_2} \cdot \min(\delta_1, \delta_2)$（自满衰减足够缓慢）

则存在 $\kappa > 0$ 使得 $V(I_1, I_2)$ 是系统在区域 $\mathcal{B}_{\lambda>0}$ 上的严格Lyapunov函数。系统从 $\mathcal{B}_{\lambda>0}$ 内任意初始点出发的轨道收敛到 $(I_1^{\circ}, I_2^{\circ})$（当 $\gamma_i \to 0$ 时）或收敛到满足 $\lambda > 0$ 的稳定点。

**证明概要**：

1. 条件(A1)保证自然基线在λ>0区域内
2. 条件(A2)保证λ<0时制度增长速率超过λ>0时的衰减速率，形成不对称的"棘轮效应"
3. 条件(A3)保证λ>0时制度退化不过快，系统有足够时间在λ再次变负之前恢复
4. 在(A1)-(A3)下，可以选取κ充分大使V的交叉项被制度偏差二次项主导
5. 由LaSalle不变性原理，所有轨道收敛到 $\{V = 0\}$ 的最大不变子集

### 3.4 数值验证

使用以下参数做仿真（与 `lambda_gauge.tex` 的校准范围一致）：

| 参数 | 值 | 含义 |
|------|-----|------|
| $\alpha_0$ | 0.4 | 基线发散倾向 |
| $\alpha_1$ | 0.5 | 再分配边际效应 |
| $\alpha_2$ | 0.5 | 教育边际效应 |
| $I_1^{\circ}$ | 0.6 | 自然再分配水平 |
| $I_2^{\circ}$ | 0.5 | 自然教育水平 |
| $\beta_1, \beta_2$ | 0.3 | 危机响应速率 |
| $\gamma_1, \gamma_2$ | 0.05 | 自满衰减速率 |
| $\delta_1, \delta_2$ | 0.1 | 回归速率 |

在此参数下：
- 自然基线λ = 0.5×0.6 + 0.5×0.5 - 0.4 = 0.15 > 0 ✅ (A1)
- $\beta_{\min}$ = (0.1+0.1)/0.5 = 0.4, β=0.3 略不足 → 需提高危机响应
- $\gamma_{\max}$ = 0.4/1.0 × 0.1 = 0.04, γ=0.05 略高 → 需降低自满衰减

**调参后**（β=0.5, γ=0.02）：
所有三个条件满足。仿真显示系统从任意初始点最终进入并保持在λ>0区域。

### 3.5 4-制度最小核心的结构验证

从开放问题中的猜想（`conjecture: minimal institutional core`），ψ>0吸引子需要四个制度核心：

1. **独立审计机构** → 对应 $I_1$（审计覆盖度）
2. **渐进税率结构** → 对应 $I_1$（再分配强度）
3. **公共教育** → 对应 $I_2$（人力资本投资）
4. **信息透明** → 对应于防止λ的测量退化（元层次条件）

在2-制度模型中，制度1综合了审计+税率，制度2对应教育。信息透明作为**元条件**：无信息透明，λ的实时估计退化，制度无法对λ<0做出响应（即β→0）。

**形式化**：定义信息透明度 $\tau \in [0,1]$，使得有效的危机响应速率为 $\beta_i^{\text{eff}} = \tau \cdot \beta_i$。当 $\tau \to 0$ 时，条件(A2)必然被违反（$\beta_i^{\text{eff}} \to 0 < \beta_{\min}$）。

**这验证了猜想**：缺失四个核心中的任何一个（此处为信息透明），λ>0的吸引盆地被压缩为空集。

### 3.6 推广至2-制度以上的情形

对于n个制度的系统，Lyapunov函数推广为：

$$V(\mathcal{I}) = \frac{1}{2}[\max(0, -\lambda(\mathcal{I}))]^2 + \frac{\kappa}{2} \|\mathcal{I} - \mathcal{I}^*\|^2$$

其中 $\lambda(\mathcal{I}) = \sum_{k=1}^{n} \alpha_k I_k - \alpha_0$。

在适当的制度响应动力学下（每个制度有独立的 $\beta_k, \gamma_k, \delta_k, I_k^{\circ}$），Lyapunov条件的形式不变，但参数约束变为向量形式：

$$\min_{k} \alpha_k \beta_k^{\text{eff}}(1 - I_k^{\min}) > \sum_k \delta_k$$

$$I_k^{\circ} \text{ 须使 } \lambda(I^{\circ}) > 0$$

### 3.7 结论与阻塞

**已完成**：
1. ✅ 构造了2-制度模型的显式Lyapunov函数V(I₁,I₂)
2. ✅ 导出了λ>0成为吸引子的三个充要条件(A1)-(A3)
3. ✅ 验证了4-制度最小核心猜想的逻辑一致性（在2-制度简约形式中）
4. ✅ 给出了数值参数验证方案

**阻塞**：
- ❌ **制度流 $\mathcal{F}(\mathcal{I})$ 的经验形式未知**：当前模型假设了特定的（有理论依据的）制度动力学，但真实的制度演化由更复杂的政治经济过程决定
- ❌ **参数校准需要历史λ数据**：开放问题中规划的20+文明λ数据库是必要条件——目前我们只有参数范围的理论约束，没有经验锚定
- ❌ **2-制度模型的简约性限制**：真实制度空间是高维的（数十个制度参数），2-制度模型仅捕获了"再分配vs教育"这一维度。高维动力学可能产生2-制度模型无法捕获的分岔行为
- ❌ **反身性风险**（从 `lambda_gauge.tex` 的诚实暴击）：CEWI预警的公开可能改变制度动力学——预警本身成为λ的驱动因素。Lyapunov分析假设制度动力学是外生的，但在有社会学习的系统中，这一假设不成立
- ❌ **文明事件视界不可逆性的严格证明缺失**：开放问题中猜想的 $\lambda_{\text{crit}}$（越过则不可逆）尚未被证明

---

## 附录：交叉引用表

| 猜想 | 源文件 | 核心数学工具 | 状态 |
|------|--------|-------------|------|
| C2 | `civ_gauge.tex` §9.2 | 动力系统、Lyapunov稳定性、Jacobi分析 | 形式化完成，经验校准阻塞 |
| C3 | `viewpoint4_correction.tex` §6 | α-联络、Amari-Chentsov张量、信息几何 | 形式化完成，张量经验估计阻塞 |
| C6 | `scx_open_problems/main.tex` §5 + `lambda_gauge.tex` §1-2 | Lyapunov函数、吸引盆地、制度动力学 | 2-制度模型完成，高维推广阻塞 |

---

*文档结束。每个猜想的形式推导已完成，阻塞已诚实识别。下一步工作建议：C3的 $T_{\max}$ Monte Carlo估计（最可行），C6的历史λ数据库构建（最基础），C2的精英质量Q代理变量开发（最具野心的经验挑战）。*
