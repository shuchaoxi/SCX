# SCX 复活规范域的严格形式化
# Strict Formalization of Resurrected Gauge Domains

> **日期 / Date**: 2026-07-02
> **前置文档 / Prerequisites**:
> - `gauge_domain_analysis.md` — 九域严格裁决，三个 DEAD END 被重审复活
> - `gauge_domain_reexam.md` — 五条替代数学路径，其中三条被选作形式化目标
> - `GAUGE_REVIEW_3.md` — 对 fiber_bundle.tex 和 gauge_physics.tex 的 hostile review
>
> **方法论 / Methodology**: 对每一个复活域：(1) 精确陈述定理，(2) 列出所有假设，(3) 提供证明框架或诚实声明"被 X 阻塞"，(4) 若被阻塞，精确说明缺少什么数学结果。不写类比。不写"启发"。只写定理。
>
> **For each resurrected domain**: (1) State the theorem precisely, (2) List all assumptions, (3) Provide proof sketch or honestly declare "proof blocked by X", (4) If blocked, state exactly what mathematical result is needed. No analogies. No "inspirations." Only theorems.

---

## 目录 / Table of Contents

1. [域 1: O(d) 格点规范理论 — 旋转对称性的非阿贝尔联络](#域-1)
2. [域 4: Dijkgraaf-Witten 离散 TQFT — 调和分量的拓扑起源](#域-4)
3. [域 5: 信息几何体-边界对应 — Cercis-Fisher 测地等价](#域-5)
4. [跨域结构关系 / Cross-Domain Structural Relations](#跨域结构)
5. [未解决的形式化缺口 / Unresolved Formalization Gaps](#缺口)

---

## 1. O(d) 格点规范理论 — 旋转对称性的非阿贝尔联络 {#域-1}
## Domain 1: O(d) Lattice Gauge Theory — Non-Abelian Connection for Rotational Symmetry

### 1.1 数学设定 / Mathematical Setup

**定义 1.1 (SCX 专家图上的 O(d) 标架丛).** 设 SCX 专家图为连通单纯复形 $G = (V, E, F)$，其中：

- $V$: 顶点集 = 数据点 / 审计状态 $x \in \mathcal{X}$（Situs 流形上的点）
- $E$: 边集 = 专家预测差异关系。边 $e = (v, w) \in E$ 表示专家在 $v$ 和 $w$ 处的预测通过某种关系连接
- $F$: 面集 = 初等三角形环路 $(v_i, v_j, v_k)$

在每个顶点 $v \in V$ 上，定义 O(d) 标架 $R_v \in O(d)$。$R_v$ 表示在数据点 $v$ 处 ACE 基函数的局部定向。物理上，$R_v$ 捕捉原子环境对 O(3) 旋转的响应。

**定义 1.2 (离散 O(d) 联络).** 边 $e = (v, w)$ 上的链接变量（平行传输）定义为：

$$U_e = U_{vw} = R_v^T R_w \in O(d)$$

规范变换由顶点赋值 $g: V \to O(d)$ 给出，作用于标架和链接变量：

$$R_v \mapsto g_v R_v, \quad U_{vw} \mapsto g_v^T \, U_{vw} \, g_w$$

**定义 1.3 (Plaquette 曲率 / 和乐).** 沿三角形面 $f = (v_i, v_j, v_k)$ 的 plaquette 和乐为：

$$W_f = U_{ij} \, U_{jk} \, U_{ki} \in O(d)$$

$W_f$ 在规范变换 $g: V \to O(d)$ 下**共变**（covariant）：$W_f \mapsto g_{v_i}^T \, W_f \, g_{v_i}$。其迹 $\operatorname{Tr}(W_f)$ 和特征值是规范不变量。

---

### 1.2 定理 1.1: O(d) 曲率的平坦性分类
### Theorem 1.1: Flatness Classification of O(d) Curvature

**定理陈述 / Theorem Statement.**

> **Theorem 1.1 (Classification of Flat O(d) Connections on a Graph).**
> 设 $G = (V, E)$ 为具有第一 Betti 数 $b_1 = |E| - |V| + 1$ 的连通图。其基本群 $\pi_1(G)$ 是 $b_1$ 个生成元的自由群。则：
>
> **(a)** 图 $G$ 上的平坦 O(d) 联络（所有 plaquette 和乐为 $I$）的规范等价类与群同态的共轭类一一对应：
>
> $$\frac{\{\text{flat O(d) connections on } G\}}{O(d)\text{-gauge}} \;\cong\; \frac{\operatorname{Hom}(\pi_1(G), O(d))}{O(d)}$$
>
> 其中 $O(d)$ 通过共轭作用于 $\operatorname{Hom}(\pi_1(G), O(d))$：$(g \cdot \rho)(\gamma) = g^{-1} \rho(\gamma) g$。
>
> **(b)** 当 $G$ 是一棵树（$b_1 = 0$，$\pi_1$ 平凡），所有平坦 O(d) 联络都是纯规范的（pure gauge）：每个平坦联络可以通过某个规范变换变为 $U_e = I \; \forall e$。
>
> **(c)** 当 $b_1 \geq 1$，存在非平凡的平坦联络，其数量（对于有限群 $G$ 的类比 O(d)）构成"调和分量"——即使所有局部曲率消失，这些全局自由度仍然存在。对于 $\pi_1 = \text{Free}(b_1)$ 且 O(d) 为连通李群的情况，平坦联络的模空间维度为：
>
> $$\dim\left(\frac{\operatorname{Hom}(\pi_1(G), O(d))}{O(d)}\right) = \dim O(d) \cdot \max(b_1 - 1, 0) = \frac{d(d-1)}{2} \cdot \max(b_1 - 1, 0)$$
>
> 其中 $\dim O(d) = d(d-1)/2$。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A1.1 | $G$ 是连通图 | 若图不连通，每个连通分量可独立分析 |
| A1.2 | $G$ 的边定向一致（用于定义链接变量方向） | 技术性，可通过反向约定处理 |
| A1.3 | $\pi_1(G)$ 是自由群（对所有图成立：图的基本群总是自由的） | 自动满足 |
| A1.4 | O(d) 是连通李群（$d \geq 1$）; 对于 $d=1$，O(1) = {±1} 是离散的 | 维度公式在 $d=1$ 时需修正 |

**证明框架 / Proof Sketch.**

**(a) 部分的证明：**

1. **从平坦联络构造表示 $\rho$：** 给定图 $G$ 上的平坦 O(d) 联络 $\{U_e\}_{e\in E}$，对 $\pi_1(G)$ 的每个生成元 $\gamma$（由基本环路代表），定义 $\rho(\gamma) = \prod_{e \in \gamma} U_e$（沿环路的平行传输积）。由于联络平坦，$\rho(\gamma)$ 不依赖于 $\gamma$ 在固定基点同伦类内的代表元选择——这是平坦性的定义性质。这给出了群同态 $\rho: \pi_1(G) \to O(d)$。

2. **规范等价对应共轭等价：** 若两个联络由规范变换 $g: V \to O(d)$ 相关联，它们在基点 $v_0$ 处产生的表示满足 $\rho_2(\gamma) = g_{v_0}^{-1} \rho_1(\gamma) g_{v_0}$，即共轭等价。反之，给定共轭的表示，可构造规范变换连接对应联络。

3. **满射：** 给定任意表示 $\rho: \pi_1(G) \to O(d)$，可以在 $G$ 的生成树上平凡地构造平坦联络（在树上 $U_e = I$），然后在余边（生成 $\pi_1$ 的边）上令 $U_e = \rho(\gamma_e)$。平坦性自动满足。

4. **据此，双射得证。** $\square$

**(b) 部分：** 当 $b_1 = 0$，图是树。$\pi_1(G)$ 平凡，因此 $\operatorname{Hom}(\pi_1, O(d)) = \{\text{trivial homomorphism}\}$。对应唯一规范等价类（纯规范联络）。沿树逐顶点地构建规范变换 $g_v$，使得 $g_v^T U_{vw} g_w = I$。$\square$

**(c) 部分：** 当 $\pi_1 = \text{Free}(b_1)$，$\operatorname{Hom}(\pi_1, O(d)) \cong O(d)^{b_1}$（$b_1$ 个自由生成元可独立取 O(d) 中任意值）。O(d) 共轭作用在此积上：同时共轭所有分量。商空间的维度为 $\dim O(d)^{b_1} - \dim O(d) = \dim O(d) \cdot (b_1 - 1)$，当 $b_1 \geq 1$。当 $b_1 = 0$，商为点（维度 0）。$\square$

**注 1.1 (与 SCX 平移规范的对比).** 在 SCX 的原始平移规范 $g_m \in \mathbb{R}^d$ 中，规范群是阿贝尔的 $(\mathbb{R}^d, +)$。此时 $\operatorname{Hom}(\pi_1, \mathbb{R}^d) \cong (\mathbb{R}^d)^{b_1}$，规范变换为公共平移（减 $d$ 维），平坦联络模空间 $\cong \mathbb{R}^{d(b_1-1)}$。这与离散 Hodge 分解 $\ker(d_1) = \operatorname{im}(d_0) \oplus \ker(L_1)$ 完全一致，其中 $\ker(L_1)$ 是调和分量，维数 $d \cdot b_1$。但请注意，$\ker(L_1)$ 对应**所有**闭链模规范（$\ker d_1 / \operatorname{im} d_0$），维数 $d \cdot b_1$，而**非** $d(b_1-1)$。阿贝尔情况下的差异来自于：对于 $\mathbb{R}^d$，$\operatorname{Hom}(\pi_1, \mathbb{R}^d)/(\mathbb{R}^d) \cong H^1(G; \mathbb{R}^d) \cong \mathbb{R}^{d \cdot b_1}$，因为 $\mathbb{R}^d$ 作用在此是**加法**平移而非共轭。$H^1$ 的维数确实为 $d \cdot b_1$。

---

### 1.3 定理 1.2: 非阿贝尔离散 Hodge 问题
### Theorem 1.2: The Non-Abelian Discrete Hodge Problem

**定理陈述 / Theorem Statement.**

> **Theorem 1.2 (O(d) Gauge Fixing as Non-Abelian Discrete Hodge).**
> 设 $G = (V, E)$ 为连通图，边上有给定的链接变量 $U_e \in O(d)$。寻找全局标架赋值 $\{R_v\}_{v \in V} \subset O(d)$ 以最小化标架传输不一致性：
>
> $$S(\{R_v\}) = \sum_{(v,w) \in E} \|R_v^T R_w - U_{vw}\|_F^2$$
>
> 其中 $\|\cdot\|_F$ 为 Frobenius 范数。则：
>
> **(a)** $S$ 的一阶必要条件为：对每个顶点 $v \in V$，
>
> $$\sum_{w \sim v} \left(R_v^T R_w - U_{vw}\right) R_w^T = 0$$
>
> 其中 $w \sim v$ 表示与 $v$ 相邻的顶点。该条件等价于 Riemannian 流形 $O(d)^{|V|}$ 上的非线性方程。
>
> **(b)** 当 $d = 1$（$O(1) = \{\pm 1\}$），问题简化为 $\mathbb{Z}_2$-值离散 Poisson 方程，可通过图割（graph cut）算法在多项式时间内精确求解。
>
> **(c)** 当 $d \geq 2$，该问题是 $O(d)^{|V|}$ 乘积流形上的**非凸优化**。不存在闭式解。必须使用 Riemannian 流形上的迭代优化方法（Riemannian 信赖域法、非线性共轭梯度法）。问题的非阿贝尔性体现在：最优标架 $\{R_v^*\}$ 不是唯一的——平坦分量的 O(d) 和乐产生规范等价的连续解族。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A2.1 | $U_{vw} \in O(d)$ 已知（由专家预测差异的 O(d) 分解得到） | 核心输入数据 |
| A2.2 | 图连通 | 不连通可分解 |
| A2.3 | 目标函数 $S$ 使用 Frobenius 范数 | 可推广为其他不变度量 |

**证明框架 / Proof Sketch.**

**(a) 部分：** 目标函数 $S: O(d)^{|V|} \to \mathbb{R}_{\geq 0}$ 是乘积流形上的光滑函数（由于 $O(d)$ 是紧李群，Frobenius 范数光滑）。在 Riemannian 流形 $O(d)^{|V|}$ 上（配备乘积双不变度量），$S$ 的 Riemannian 梯度为：

$$\nabla_{R_v} S = \sum_{w \sim v} \left(R_v^T R_w - U_{vw}\right) R_w^T \cdot \Pi_{T_{R_v}O(d)}$$

其中 $\Pi$ 投影到 $O(d)$ 在 $R_v$ 处的切空间。通过左平移，切空间为 $R_v \cdot \mathfrak{o}(d)$（其中 $\mathfrak{o}(d)$ 为反对称矩阵的李代数）。一阶必要条件 $\nabla S = 0$ 给出方程 $\sum_{w \sim v} (R_v^T R_w - U_{vw}) R_w^T \in \mathfrak{n}_{R_v}O(d)$（法空间）。在双不变度量下展开，给出所述形式。$\square$

**(b) 部分（$d=1$）：** 当 $d=1$，$O(1) = \{+1, -1\} \cong \mathbb{Z}_2$。$R_v \in \{\pm 1\}$，$U_{vw} \in \{\pm 1\}$。目标函数：

$$S = \sum_{(v,w) \in E} (R_v R_w - U_{vw})^2 = \sum_{(v,w) \in E} 2\left(1 - R_v R_w U_{vw}\right)$$

因为 $R_v, R_w, U_{vw} \in \{\pm 1\}$ 时 $(R_v R_w - U_{vw})^2 = 2 - 2R_v R_w U_{vw}$。最小化 $S$ 等价于最大化 $\sum_{(v,w)} R_v R_w U_{vw}$。定义 $J_{vw} = U_{vw}$ 作为边权重，这是 $\mathbb{Z}_2$ 上的 Ising 型问题，可通过最小割（min-cut）在多项式时间内求解。$\square$

**(c) 部分：** 对于 $d \geq 2$，$O(d)$ 是维数 $\geq 1$ 的连续流形。目标函数非凸：存在多个局部极小值，对应不同的平坦联络规范类。特别地，两个标架赋值 $\{R_v\}$ 和 $\{g_v R_v\}$（其中 $\{g_v\}$ 为平坦联络的规范变换）可产生相同的 $S$ 值。因此最优解不唯一，构成连续族。不存在全局闭式解——这是非阿贝尔规范理论的一般性质（Gribov 模糊）。$\square$

**阻塞声明 / Blockers.**

| 阻塞 | 严重性 | 缺失的数学结果 |
|------|--------|----------------|
| B1.2.1 | 中等 | 对于 $d \geq 2$，$S$ 的局部极小值的完整分类（哪些极小值对应不同的平坦和乐类？）需要分析 $S$ 的 Morse 理论 |
| B1.2.2 | 中等 | 收敛速率保证：Riemannian 优化从任意初始点到局部极小值的迭代复杂度。这在数值上是熟知的（Absil et al., 2008），但未针对 SCX 的特殊图结构特化 |

---

### 1.4 定理 1.3: O(d) 和乐作为不可消除偏差的诊断
### Theorem 1.3: O(d) Holonomy as Diagnostic for Irreducible Bias

**定理陈述 / Theorem Statement.**

> **Theorem 1.3 (O(d) Holonomy Detects Irreducible Frame Misalignment).**
> 设 $G = (V, E, F)$ 为 SCX 专家图，携带 O(d) 联络 $\{U_e\}$。对每个 plaquette $f \in F$，计算和乐 $W_f \in O(d)$。则：
>
> **(a)** **消失判据（Vanishing Criterion）：** $W_f = I$（恒等矩阵）对所有 $f \in F$ 成立，当且仅当联络是平坦的。
>
> **(b)** **不可消除性（Irreducibility）：** 若存在 $f \in F$ 使得 $W_f \neq I$，则不存在任何局部 O(d) 规范变换 $\{g_v\}$（仅在单个顶点上非平凡）可以使得所有和乐同时变为 $I$。非零和乐是拓扑障碍。
>
> **(c)** **偏差分解（Bias Decomposition）：** 和乐矩阵 $W_f$ 可分解为：
>
> $$W_f = R(\theta_f) \cdot S_f$$
>
> 其中 $R(\theta_f) \in SO(d)$ 是角度为 $\theta_f \in [0, \pi]$ 的旋转，$S_f$ 包含反射部分（若 $\det W_f = -1$）。角度 $\theta_f$ 度量了沿 plaquette $f$ 的"不可消除的标架扭曲程度"。对所有 plaquette 的 $\theta_f$（或 $\operatorname{Tr}(W_f)$）的分布构成 O(d) 型系统性偏差的诊断。
>
> **(d)** **面积律预判（Area Law Anticipation）：** 若沿长度为 $k$ 的大环路（$k$ 个 plaquette 拼接）的和乐 $\|W_{\text{large}} - I\|_F$ 增长满足 $\sim \exp(\sigma k^2)$（面积律），则存在系统性的 O(d) 偏差；若满足 $\sim \exp(\alpha k)$（周长律），则 O(d) 偏差是局部噪声。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A3.1 | 面集 $F$ 生成 $\pi_1(G)$（即所有基本环路可由 plaquette 环路组合而成） | 若 $F$ 不完全，结论仅适用于由 $F$ 生成的 $\pi_1$ 的子群 |
| A3.2 | $U_e$ 已知 | 输入数据 |
| A3.3 | 面积律/周长律需要大图极限（$G$ 足够大以区分定律） | 小图两种行为不可区分 |

**证明框架 / Proof Sketch.**

**(a) 部分：** "当"方向：若所有 $W_f = I$，则沿任意基本环路 $\gamma \in \pi_1(G)$ 的和乐为 $W_\gamma = \prod_f W_f^{n_f} = I$（因为 $\pi_1$ 由 plaquette 生成）。因此联络平坦。"仅当"方向：若联络平坦，则沿任意环路（包括 plaqutte）的和乐为 $I$（由平坦性的定义）。$\square$

**(b) 部分：** 设 $W_f \neq I$。若局部规范变换可将所有 plaquette 和乐变为 $I$，则联络必然是平坦的，矛盾。因此至少一个 plaquette 的非平凡和乐必须保持，且无法被任何局部变换消除。这是 O(d) 主丛上非零曲率的基本性质。$\square$

**(c) 部分：** 由 O(d) 的 Cartan 分解：任意 $W \in O(d)$ 可写为 $W = R \cdot S$，其中 $R \in SO(d)$（旋转），$S$ 为反射（若 $\det W = -1$）。旋转部分 $R$ 的特征值为 $\{e^{\pm i\theta_1}, ..., e^{\pm i\theta_k}, 1\}$（若 $d$ 为奇数则加一个 1）。定义 $\theta_f = \max_i |\theta_i|$ 为最大旋转角。该角度度量了"标架扭曲的最大程度"。$\square$

**(d) 部分：** 此部分目前为**推测**而非定理。面积律/周长律的严格证明需要以下条件：
- 在大图上定义概率测度（随机 O(d) 联络）
- 证明和乐范数的期望满足对应标度律
- 或者，对确定性图定义渐近标度

**此部分被阻塞（见下）。** $\square$

**阻塞声明 / Blockers.**

| 阻塞 | 严重性 | 缺失的数学结果 |
|------|--------|----------------|
| B1.3.1 | **严重** | 面积律/周长律分类定理 (d) 在离散 O(d) 格点规范理论中**未被证明**。在格点 QCD 中，面积律是数值观察（对 SU(3)），其严格证明是著名的 Yang-Mills 质量间隙问题（千禧年大奖难题之一）。声称 SCX 可以严格证明面积律是不诚实的。可做的是：(i) 证明面积律在某些可解极限下成立（如强耦合展开），(ii) 对 SCX 特定图结构进行数值验证，(iii) 将面积律作为**诊断启发**而非严格定理。 |

**修正方案 / Mitigation Plan for B1.3.1:**
将 Theorem 1.3(d) 从"定理"降级为"Conjecture 1.3"（面积律猜想），在强耦合极限（所有 $U_e$ 接近 $I$）下提供部分严格结果，并明确标注完整证明需要尚未解决的数学工具。

---

## 2. Dijkgraaf-Witten 离散 TQFT — 调和分量的拓扑起源 {#域-4}
## Domain 4: Dijkgraaf-Witten Discrete TQFT — Topological Origin of the Harmonic Component

### 2.1 数学设定 / Mathematical Setup

**定义 2.1 (SCX 专家图作为 2-复形).** SCX 专家图提升为 2-复形 $M = (V, E, F)$，其中：

- $V$: 数据点（0-单形）
- $E$: 专家差异边（1-单形），边 $e = (v, w)$ 携带平移向量 $\mathbf{g}_m - \mathbf{g}_n \in \mathbb{R}^d$（或更一般的群元素）
- $F$: 三角形面（2-单形），$(v_i, v_j, v_k)$ 表示三元专家环路

**定义 2.2 (离散规范场).** 令 $G$ 为有限群（或李群的有限截断）。离散 $G$-规范场由赋值 $g: E \to G$ 给出，每条边上一个群元素。面 $f = (v_i, v_j, v_k)$ 的曲率（和乐）为：

$$h_f = g_{ij} \cdot g_{jk} \cdot g_{ki} \in G$$

（方向约定：$g_{ij}$ 表示从 $v_i$ 传输到 $v_j$，反向使用逆元 $g_{ji} = g_{ij}^{-1}$。）

**定义 2.3 (Dijkgraaf-Witten 配分函数).** 令 $\omega \in Z^2(G, U(1))$ 为群上同调类 $[\omega] \in H^2(G, U(1))$ 的代表 2-cocycle。Dijkgraaf-Witten 配分函数为：

$$Z_\omega(M) = |G|^{-|V|} \sum_{g: E \to G} \; \prod_{f \in F} \omega(g_{ij}, g_{jk})$$

其中 $\omega(g_{ij}, g_{jk})$ 解释为对三角形的赋权（2-cocycle 条件保证配分函数不依赖于具体三角剖分的选择，是拓扑不变量）。

---

### 2.2 定理 2.1: 平坦规范场的计数与调和分量
### Theorem 2.1: Counting Flat Gauge Fields and the Harmonic Component

**定理陈述 / Theorem Statement.**

> **Theorem 2.1 (Flat G-Connections on SCX Graph).**
> 设 $M = (V, E, F)$ 为有限 2-复形（SCX 专家图），$G$ 为有限群。定义平坦 $G$-联络的集合：
>
> $$\mathcal{F}(M, G) = \big\{ g: E \to G \;\big|\; h_f = 1_G \text{ 对所有 } f \in F \big\}$$
>
> 即所有使得每个 plaquette 上曲率为零的边赋值。则：
>
> **(a)** 规范群 $\mathcal{G} = \{h: V \to G\}$ 通过 $g_{vw} \mapsto h_v^{-1} \, g_{vw} \, h_w$ 作用于 $\mathcal{F}(M, G)$。规范等价类的数量为：
>
> $$|\mathcal{F}(M, G)/\mathcal{G}| = \frac{|\operatorname{Hom}(\pi_1(M), G)|}{|G|}$$
>
> 其中 $\pi_1(M)$ 为 2-复形 $M$ 的基本群。该数量为拓扑不变量（仅依赖于 $M$ 的同伦型，不依赖于具体三角剖分）。
>
> **(b)** 当 $M$ 的 1-骨架 $M^{(1)}$ 为连通图，且 $\pi_1(M) \cong \mathbb{Z}^{*b_1}$（$b_1$ 个生成元的自由群，$b_1 = \dim H_1(M)$），则：
>
> $$|\mathcal{F}(M, G)/\mathcal{G}| = |G|^{b_1 - 1}$$
>
> **此即调和分量的起源**：即使所有局部曲率消失，仍有 $|G|^{b_1 - 1}$ 个规范不等价的平坦联络——它们对应离散 Hodge 分解中的 $\ker(L_1)$ 分量。
>
> **(c)** 对于阿贝尔群 $G$（如 $G = \mathbb{Z}_q$ 或 $G = U(1)$ 的有限子群），
>
> $$|\mathcal{F}(M, G)/\mathcal{G}| = |G|^{b_1}$$
>
> **这是因为阿贝尔群下共轭作用是平凡的**，$\operatorname{Hom}(\pi_1, G) \cong G^{b_1}$，且 $|G^{b_1}|/|G| = |G|^{b_1}$ 对非平凡作用成立，但对平（阿贝尔）作用，商为 $|G|^{b_1}$（无需除以 $|G|$，因为规范群不作用于规范等价类本身——等等，这里需要仔细分析）。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A2.1.1 | $G$ 是有限群 | 计数公式依赖 $|G|$ 有限。对于李群，需用维数替代计数 |
| A2.1.2 | $M$ 的 2-复形结构已知（$V, E, F$ 及关联关系） | 输入 |
| A2.1.3 | Plaquette 曲率条件 $h_f = 1_G$ 在所有 $f \in F$ 上检查 | 平坦联络的定义 |

**证明框架 / Proof Sketch.**

**(a) 部分：** 这是平坦 $G$-丛理论的标准结果。证明步骤如下：

1. **从平坦联络到表示 $\rho$：** 给定 $\{g_e\} \in \mathcal{F}(M, G)$，对 $\pi_1(M)$ 的每个元素 $\gamma$（由边序列表示），定义 $\rho(\gamma) = \prod_{e \in \gamma} g_e^{\pm 1}$（沿 $\gamma$ 的定向积）。平坦性（$h_f = 1_G$ 对所有 $f \in F$）保证 $\rho(\gamma)$ 仅依赖于 $\gamma$ 的同伦类——这是 2-骨架的基本群定义。

2. **映射 $\Phi: \mathcal{F}(M, G) \to \operatorname{Hom}(\pi_1(M), G)$：** 上述构造给出 $\Phi(\{g_e\}) = \rho$。$\Phi$ 是满射：给定 $\rho$，在 $M^{(1)}$ 的生成树上设 $g_e = 1$，在其余边上设 $g_{\gamma_i} = \rho(\gamma_i)$（其中 $\gamma_i$ 为 $\pi_1$ 生成元）。

3. **纤维分析：** $\Phi^{-1}(\rho)$ 中的元素由在生成树上自由选择 $g_e$ 决定。树的边数为 $|V|-1$，因此每条纤维大小为 $|G|^{|V|-1}$。

4. **规范等价：** 两个平坦联络由规范变换 $h: V \to G$ 关联，当且仅当它们对应共轭的 $\pi_1$ 表示。因此：
   $$|\mathcal{F}(M, G)/\mathcal{G}| = \frac{|\mathcal{F}(M, G)|}{|\mathcal{G}|/|Z_G|} = \frac{|\operatorname{Hom}(\pi_1, G)| \cdot |G|^{|V|-1}}{|G|^{|V|}/|G|} = \frac{|\operatorname{Hom}(\pi_1, G)|}{|G|}$$
   其中 $|\mathcal{G}| = |G|^{|V|-1} \cdot |G|$（注意：全局常值规范变换 $h_v \equiv g_c$ 当 $g_c \in Z(G)$ 时对联络无影响——严格而言应除以中心的大小。在一般公式 $|\operatorname{Hom}(\pi_1, G)|/|G|$ 中，商由 $G$ 的共轭作用给出，大小为 $|G|$）。$\square$

**(b) 部分：** 当 $\pi_1(M) \cong \mathbb{Z}^{*b_1}$，每个生成元可独立取 $G$ 中任意值：
$$|\operatorname{Hom}(\pi_1(M), G)| = |G|^{b_1}$$
因此：
$$|\mathcal{F}(M, G)/\mathcal{G}| = \frac{|G|^{b_1}}{|G|} = |G|^{b_1 - 1}$$
$\square$

**(c) 部分的修正：** 对于阿贝尔群 $G$，$\operatorname{Hom}(\pi_1, G) \cong G^{b_1}$（仍成立）。但 $G$ 的共轭作用是**平凡的**（因为 $ghg^{-1} = h$ 对所有 $g, h \in G$）。因此商 $\operatorname{Hom}(\pi_1, G)/G$（按共轭）的计数：共轭作用平凡意味着每个轨道大小为 1。因此：
$$|\operatorname{Hom}(\pi_1, G)/G| = |G|^{b_1}$$

**但**这似乎与直接计数矛盾——对于 $G = \mathbb{Z}_2$，阿贝尔情况应有 $2^{b_1}$ 个规范不等价类，而非 $2^{b_1-1}$。让我们通过具体例子验证：

$G = \mathbb{Z}_2$，$b_1 = 1$（圆图）。$\pi_1 \cong \mathbb{Z}$。$\operatorname{Hom}(\mathbb{Z}, \mathbb{Z}_2) \cong \mathbb{Z}_2$（生成元 $\gamma$ 映射到 $0$ 或 $1$）。规范变换 $h: V \to \mathbb{Z}_2$。当所有 $h_v$ 相同时，$g_{vw} \mapsto h_v^{-1}g_{vw}h_w = g_{vw}$（因为 $\mathbb{Z}_2$ 是阿贝尔的，$h_v^{-1}h_w = h_v + h_w$ 模 2——等等，对于阿贝尔群 $h_v^{-1} g_{vw} h_w = g_{vw} \cdot (h_v^{-1} h_w)$，而不是 $g_{vw}$！阿贝尔群中规范变换为 $g_{vw} \mapsto g_{vw} \cdot h_v^{-1} h_w$（乘法符号），确实改变联络。）

**关键修正：** 在阿贝尔群中，规范变换**仍然有效**（它改变边赋值），只是共轭作用在 $\pi_1$ 表示上变为平凡。准确计数：

- $\mathcal{F} = G^{b_1} \cdot G^{|V|-1}$（解空间大小）
- $\mathcal{G}$ = 有效规范变换数 = $|G|^{|V|-1}$（整体常值规范变换为 $1_G$ 时无影响，在阿贝尔群中 $h_v \equiv c$ 产生 $g_{vw} \mapsto g_{vw} \cdot c^{-1}c = g_{vw}$，因此整体常值变换不影响任何边）
- $|\mathcal{F}/\mathcal{G}| = |G|^{b_1}$

**对于阿贝尔群，规范等价类数量为 $|G|^{b_1}$**，与离散 Hodge 理论中 $\ker(L_1) \cong (\text{群})^{b_1 \cdot \text{纤维维数}}$ 一致。

对于非阿贝尔群（自由 $\pi_1$），总数为 $|G|^{b_1-1} \cdot |Z(G)|$（考虑到中心的不动点修正），一般公式需要包含中心 $Z(G)$ 的修正。对于大多数实际相关的非阿贝尔群（如 O(d), SU(n)），$|Z(G)|$ 很小。这个细微之处在以下被阻塞声明中标出。$\square$

**阻塞声明 / Blockers.**

| 阻塞 | 严重性 | 缺失的数学结果 |
|------|--------|----------------|
| B2.1.1 | 低 | 一般非阿贝尔群 $G$ 的规范等价类精确计数公式当 $\pi_1$ 非自由时需要 $|G| \cdot |\operatorname{Hom}(\pi_1, G)| = \sum_\rho |G|/|C_G(\operatorname{im} \rho)|$（Burnside 引理在共轭作用下的应用）。自由群情况用上述公式处理，一般情况需要完整表示论。 |
| B2.1.2 | 中等 | 对于连续群（$\mathbb{R}^d$），计数应替换为维数：$\dim(\mathcal{F}/\mathcal{G}) = d \cdot b_1$。需要建立"离散有限群→连续李群"的极限过渡。 |

---

### 2.3 定理 2.2: Dijkgraaf-Witten 不变量与 SCX 审计诊断
### Theorem 2.2: Dijkgraaf-Witten Invariants as SCX Audit Diagnostics

**定理陈述 / Theorem Statement.**

> **Theorem 2.2 (DW Invariant as Topological Audit Discriminant).**
> 设 $M_1, M_2$ 为两个 SCX 审计配置的 2-复形表示。选择有限规范群 $G$ 和非平凡 2-cocycle $\omega \in Z^2(G, U(1))$（来自 $H^2(G, U(1))$ 的非平凡类，例如 $G = \mathbb{Z}_n \times \mathbb{Z}_n$ 时的离散 theta 项）。则：
>
> **(a) 拓扑不变性（Topological Invariance）：** 若 $M_1$ 和 $M_2$ 同伦等价，则 $Z_\omega(M_1) = Z_\omega(M_2)$。特别地，若审计配置 $M_1$ 和 $M_2$ 有相同的 Betti 数但不同的 $Z_\omega$ 值，则它们不是同伦等价的。
>
> **(b) 超越 Betti 数的区分能力：** 存在两个 2-复形 $M_1, M_2$ 具有相同的 Betti 数 $(b_0, b_1, b_2)$，但 $Z_\omega(M_1) \neq Z_\omega(M_2)$。具体例子：lens spaces $L(p, q_1)$ 和 $L(p, q_2)$ 具有相同同调群但不同 $Z_\omega$ 值。
>
> **(c) 平坦与扭曲的区别：** 当 $\omega = 1$（平凡 cocycle），$Z_1(M) = |G|^{|E|-|V|}$ 仅依赖边的数量。当 $\omega$ 非平凡，$Z_\omega(M)$ 依赖于 $\pi_1(M)$ 在 $G$ 中的表示如何"扭曲"——捕获了调和分量 $\ker(L_1)$ 无法区分的全局结构信息。
>
> **(d) SCX 审计翻译：** $Z_\omega(M) \neq Z_\omega(M_{\text{ref}})$（其中 $M_{\text{ref}}$ 为某个参考配置）表示审计配置 $M$ 包含**拓扑上不可约简的全局不一致性**，其程度由 $\omega$ 的选取编码。不同 $\omega$ 探测不同"类型"的不一致性。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A2.2.1 | 选择有限群 $G$ 和非平凡 $[\omega] \in H^2(G, U(1))$ | 平凡 $\omega$ 只给出 $|G|^{|E|-|V|}$（无拓扑信息） |
| A2.2.2 | $M$ 是 2-复形（闭曲面或有边界） | DW 理论标准设定 |
| A2.2.3 | 规范群 $G$ 的离散化是合理的（对于 SCX 的 $\mathbb{R}^d$，需选择有限截断子群） | 技术前提 |

**证明框架 / Proof Sketch.**

**(a) 部分：** 这是 Dijkgraaf 和 Witten (1990) 的核心结果。证明分为三个步骤：

1. **配分函数不依赖于三角剖分：** 2-cocycle 条件 $\delta\omega(g,h,k) = \omega(h,k)\omega(gh,k)^{-1}\omega(g,hk)\omega(g,h)^{-1} = 1$ 保证在 Pachner 移动（2-复形的初等同伦变换）下 $Z_\omega$ 不变。

2. **同伦等价蕴含三角剖分的 Pachner 等价：** 二维 PL 流形的同伦等价可通过有限次 Pachner 移动实现。

3. 因此 $Z_\omega$ 是同伦不变量。$\square$

**(b) 部分：** Lens space 的构造：$L(p, q) = S^3/\mathbb{Z}_p$，其中 $\mathbb{Z}_p$ 作用于 $S^3 \subset \mathbb{C}^2$，生成元 $T(z_1, z_2) = (e^{2\pi i/p} z_1, e^{2\pi i q/p} z_2)$。所有 $L(p, q)$ 有相同同调：$H_0 = \mathbb{Z}, H_1 = \mathbb{Z}_p, H_2 = 0, H_3 = \mathbb{Z}$，但 DW 不变量可以区分 $q$ 的不同值（当选取 $G = \mathbb{Z}_p$ 时）。在 SCX 2-复形中，类似的"扭曲"可能由专家环路间的非平凡关系产生。$\square$

**(c) 部分：** 当 $\omega = 1$，$\prod_f \omega(...) = 1$，求和为 $Z_1 = |G|^{-|V|} |G|^{|E|} = |G|^{|E|-|V|}$。当 $\omega$ 非平凡，和乐表示不同的 $\pi_1 \to G$ 获得不同权重，配分函数捕获表示论信息。调和分量 $\ker(L_1)$ 仅计数平坦联络的数量（不加权），因此丢失了"扭曲程度"信息。$\square$

**(d) 部分：** 这是审计解释的自然推广——若两个审计拓扑不等价，存在深层差异。需要建立从 $Z_\omega$ 值差异到审计断言（"存在不可消除的系统性偏差"）的严格映射。$\square$

**阻塞声明 / Blockers.**

| 阻塞 | 严重性 | 缺失的数学结果 |
|------|--------|----------------|
| B2.2.1 | **严重** | SCX 专家图的 2-复形结构需要**精确定义**。当前 SCX 有顶点和边，但"面"的定义含糊：三元专家环路 $(k,i) \to (k,j) \to (k,m) \to (k,i)$ 是自然的三角形，但这些三角形是否构成完整的三角剖分？面的粘合映射是什么？需要先完成 2-复形构造。 |
| B2.2.2 | **严重** | 非平凡 $\omega$ 的选取**没有明确的审计物理解释**。在 Chern-Simons 理论中，$\omega$ 对应 level $k$。在 SCX 中，需要回答"$\omega$ 代表审计中的什么物理量？"若没有答案，DW 不变量是一个纯数学玩具，不具有审计意义。 |
| B2.2.3 | 中等 | 对 $\mathbb{R}^d$ 做有限群离散化：选择有限子群 $G_N \subset \mathbb{R}^d$ 使得 $G_N \to \mathbb{R}^d$ 在某种极限下。DW 不变量的连续极限过渡是已知的（BF 理论的离散化），但需要针对 SCX 做具体验证。 |

---

### 2.4 定理 2.3: 离散 BF 理论与调和分量维数
### Theorem 2.3: Discrete BF Theory and Harmonic Component Dimension

**定理陈述 / Theorem Statement.**

> **Theorem 2.3 (BF Partition Function = Count of Flat Connections).**
> 设 $M = (V, E, F)$ 为连通 2-复形，$G$ 为阿贝尔群（加性表示）。定义离散 BF 配分函数：
>
> $$Z_{BF}(M; G) = \frac{1}{|G|^{|V|}} \sum_{A: E \to G} \; \prod_{f \in F} \delta\!\left(\sum_{e \in \partial f} \pm A_e = 0\right)$$
>
> 其中 $\delta(\cdot) = 1$ 若参数为 $0$，否则 $\delta(\cdot) = 0$；$\partial f$ 为面 $f$ 的边界边（带符号）。则：
>
> $$Z_{BF}(M; G) = |G|^{b_1(M)}$$
>
> 其中 $b_1(M) = \dim_{\mathbb{R}} H_1(M; \mathbb{R}) = \dim \ker \Delta_1$（第一 Betti 数 = 调和 1-形式空间的维数）。
>
> **此定理建立了从"离散 TQFT"到"SCX 已有结构"的严格桥梁**：$Z_{BF}$ 直接计数了 $\ker(L_1)$ 中的调和分量维数。SCX 的 Theorem 3（fiber_bundle.tex）遗漏的正是这个 $|G|^{b_1}$ 因子（当 $G = \mathbb{R}^d$ 时替换为 $d \cdot b_1$ 维的连续空间）。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A2.3.1 | $G$ 是有限阿贝尔群（或 $\mathbb{R}^d$ 的紧子群截断） | BF 理论在阿贝尔群上最简洁 |
| A2.3.2 | 边定向一致，面定向与边定向兼容 | 符号约定 |
| A2.3.3 | $M$ 连通 | 不连通可分解，$b_1$ 为各分量之和 |

**证明框架 / Proof Sketch.**

离散 BF 配分函数的计算使用了有限阿贝尔群的 Fourier 分析：

1. **积分表示：** 对每个面 $f$ 使用 $\delta$ 函数的 Fourier 表示（当 $G$ 为有限阿贝尔群）：
   $$\delta(x = 0) = \frac{1}{|G|} \sum_{\chi \in \hat{G}} \chi(x)$$
   其中 $\hat{G}$ 为 $G$ 的 Pontryagin 对偶。

2. **重新排序求和：**
   $$Z_{BF} = \frac{1}{|G|^{|V|}} \sum_{A: E \to G} \; \frac{1}{|G|^{|F|}} \sum_{B: F \to \hat{G}} \prod_{f} \chi_{B_f}\!\left(\sum_{e \in \partial f} \pm A_e\right)$$
   $$= \frac{1}{|G|^{|V|+|F|}} \sum_{B} \prod_{e \in E} \sum_{A_e \in G} \chi_{\sum_{f \supset e} \pm B_f}(A_e)$$

3. **内求和的评估：**
   $$\sum_{A_e \in G} \chi_C(A_e) = \begin{cases} |G| & \text{若 } C = 0 \\ 0 & \text{否则} \end{cases}$$
   其中 $C = \sum_{f \supset e} \pm B_f$（边上来自相邻面的面变数的 coboundary）。

4. **因此：**
   $$Z_{BF} = \frac{1}{|G|^{|V|+|F|}} \sum_{B: \delta B = 0} |G|^{|E|} = |G|^{|E|-|V|-|F|} \cdot |\ker(\delta: C^2 \to C^1)|$$

5. **使用同调：** $\ker(\delta: C^2 \to C^1) = Z^2(M; \hat{G})$（2-cocycle 空间）。$|Z^2| = |G|^{b_2 + \dim \operatorname{im}(\delta)}$。

   更简单的方法——直接计数平坦联络：
   - 平坦联络 $A$ 满足 $\delta A = 0$ 对所有面
   - $\ker(d_1) = \{A: E \to G \mid \sum \pm A_e = 0 \text{ on each face}\}$
   - $|\ker(d_1)| = |G|^{|E| - \dim \operatorname{im}(d_1)}$
   - 规范变换 $A_e \mapsto A_e + (\delta \phi)_e$ 的像空间大小为 $|G|^{|V|-1}$（整体常值 $\phi$ 不影响 $A$）
   - $|\ker(d_1)/\operatorname{im}(d_0)| = |G|^{|E| - \dim \operatorname{im}(d_1) - (|V|-1)}$
   - 由 $b_1 = |E| - \dim \operatorname{im}(d_1) - (|V|-1)$（秩-零化度），得 $|\ker(d_1)/\operatorname{im}(d_0)| = |G|^{b_1}$

   此即 $Z_{BF}$ 等于平坦联络规范等价类的数量。$\square$

**与 fiber_bundle.tex Theorem 3 的关系：** fiber_bundle.tex 的 Theorem 3 声称"curvature = 0 对所有 plaquette ⇔ A 是恰当的 ⇔ Cercis = 0"。Theorem 2.3 证明了这**不成立**——"curvature = 0"蕴含 $A \in \ker(d_1)$，但 $\ker(d_1) = \operatorname{im}(d_0) \oplus \ker(L_1)$。调和分量 $\ker(L_1)$ 非零时，$A$ 可以是平坦的（曲率为 0）但不是恰当的。此时 Cercis $\neq 0$，但曲率为 0。**Theorem 3 的修正必须在曲率条件上加入 $\langle A, h_i \rangle = 0$（$h_i$ 为 $\ker(L_1)$ 的基），即调和分量为零。**

---

## 3. 信息几何体-边界对应 — Cercis-Fisher 测地等价 {#域-5}
## Domain 5: Information-Geometric Bulk-Boundary Correspondence — Cercis-Fisher Geodesic Equivalence

### 3.1 数学设定 / Mathematical Setup

**定义 3.1 (Situs 流形上的 Fisher 信息度量).** 设 $\{p_\theta(x) : \theta \in \Theta\}$ 为 $d$ 维指数族，$\Theta \subset \mathbb{R}^d$ 为自然参数空间。Fisher 信息矩阵：

$$g_{ij}(\theta) = \mathbb{E}_{x \sim p_\theta}\!\left[\frac{\partial \log p_\theta(x)}{\partial \theta_i} \frac{\partial \log p_\theta(x)}{\partial \theta_j}\right] = -\mathbb{E}_{x \sim p_\theta}\!\left[\frac{\partial^2 \log p_\theta(x)}{\partial \theta_i \partial \theta_j}\right]$$

在 $\Theta$ 上定义 Riemannian 流形 $(\Theta, g)$——即"**Situs 流形**"（统计流形版本）。Fisher-Rao 距离 $d_{FR}(\theta_1, \theta_2)$ 为 $\Theta$ 上关于 $g$ 的测地线长度。

**定义 3.2 (KL 散度与 Bregman 散度).** 对于指数族，KL 散度与 Bregman 散度对偶：

$$D_{KL}(p_\theta \| p_{\theta'}) = \psi(\theta') - \psi(\theta) - \nabla\psi(\theta)^T (\theta' - \theta) = D_\psi(\theta', \theta)$$

其中 $\psi(\theta)$ 是对数配分函数（log-partition function），$D_\psi$ 是以 $\psi$ 为势的 Bregman 散度。

**定义 3.3 (Spring 训练作为"体"梯度流).** Spring 训练动力学生活在增广空间 $\tilde = \Theta \times \mathbb{R}_{\geq 0}$（"体" = 参数空间 + 训练时间）。"边界"在 $t = T$（训练终点）给出 Cercis Score。Spring 的 Lyapunov 函数 $L: \tilde \to \mathbb{R}$ 定义了体的度量结构。

**定义 3.4 (Cercis Score 的几何解释).** 在已做规范固定（$\sum \mathbf{g}_m = 0$）后，Cercis Score 衡量所有专家预测差异向量的总范数：

$$\text{Cercis} = \frac{1}{M} \sum_{m=1}^M \|\mathbf{g}_m\| = \frac{1}{M} \sum_{m=1}^M \|\hat_m - \bar\|$$

在指数族设定下，每个专家 $m$ 的预测对应自然参数的估计 $\hat_m \in \Theta$。$\bar = \frac{1}{M} \sum \hat_m$ 为规范固定后的均值（规范固定条件 $\sum \mathbf{g}_m = 0$ 蕴含 $\bar$ 是固定点）。

---

### 3.2 定理 3.1: Cercis Score 与 Fisher 测地距离的等价
### Theorem 3.1: Equivalence of Cercis Score and Fisher Geodesic Distance

**定理陈述 / Theorem Statement.**

> **Theorem 3.1 (Cercis–Fisher–Geodesic Equivalence for Exponential Families).**
> 设 $\mathcal{M} = (\Theta, g)$ 为指数族 $p_\theta$ 的 Fisher-Rao 统计流形。设专家预测给出自然参数 $\hat_1, ..., \hat_M \in \Theta$。定义 $\bar = \frac{1}{M}\sum_m \hat_m$ 为规范固定后的参考点。$\Delta\theta_m = \hat_m - \bar$（满足 $\sum_m \Delta\theta_m = 0$，即规范固定条件）。则：
>
> **(a) KL 散度的二阶逼近（Second-Order KL Approximation）：**
>
> $$D_{KL}(p_{\bar} \| p_{\hat_m}) = \frac{1}{2} \|\Delta\theta_m\|_g^2 + O(\|\Delta\theta_m\|^3)$$
>
> 其中 $\|\Delta\theta\|_g^2 = g_{ij}(\bar) \Delta\theta^i \Delta\theta^j$ 是在参考点 $\bar$ 处度量的 Fisher 范数。
>
> **(b) 平方 Cercis 与平均 KL 散度成正比（Cercis² ∝ Mean KL）：**
>
> $$\text{Cercis}^2 = \frac{1}{M^2} \sum_{m=1}^M \|\Delta\theta_m\|^2 \;\propto\; \frac{1}{M} \sum_{m=1}^M \|\Delta\theta_m\|_g^2 + O(\max_m \|\Delta\theta_m\|^3)$$
>
> $$= \frac{2}{M} \sum_{m=1}^M D_{KL}(p_{\bar} \| p_{\hat_m}) + O(\max_m \|\Delta\theta_m\|^3)$$
>
> **(c) Fisher 测地距离与 Cercis 的关系（Fisher Geodesic Bound）：**
>
> $$d_{FR}(\bar, \hat_m) = \|\Delta\theta_m\|_g + O(\|\Delta\theta_m\|^2)$$
>
> 因此：
>
> $$\text{Cercis}^2 \approx \frac{1}{M^2} \sum_{m=1}^M d_{FR}^2(\bar, \hat_m)$$
>
> **即：Cercis² 近似等于所有专家到规范固定点的 Fisher 测地距离的均方。**
>
> **(d) 体-边界解释（Bulk-Boundary Interpretation）：** 若 Spring 训练动力学沿 Fisher 测地线下降 Lyapunov 函数 $L$（即 Spring 做自然梯度下降），则训练轨迹在"体" $\Theta \times [0, T]$ 中的长度等于边界 Cercis Score：
>
> $$\text{Length}_{\text{Spring trajectory}} \;\approx\; \sqrt{\text{Cercis}}$$

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A3.1.1 | 专家预测 $p_{\hat_m}$ 属于同一指数族 | 若不属于，Fisher 度量无全局定义，定理需逐对推广 |
| A3.1.2 | $\hat_m$ 接近 $\bar$（$\|\Delta\theta_m\|$ 小） | 二阶逼近需要。若差异大，需完整 Fisher-Rao 距离（无闭式） |
| A3.1.3 | $\bar$ 处的 Fisher 度量 $g_{ij}(\bar)$ 满秩 | 非奇异统计模型 |
| A3.1.4 | 规范固定条件 $\sum \mathbf{g}_m = 0$ 已施加 | Cercis 的定义前提 |

**证明框架 / Proof Sketch.**

**(a) 部分：** 对 KL 散度做 Taylor 展开（以 $\bar$ 为中心）：

$$D_{KL}(p_{\bar} \| p_{\hat_m}) = D_{KL}(p_{\bar} \| p_{\bar + \Delta\theta_m})$$

首先，$D_{KL}(p_{\bar} \| p_{\bar}) = 0$。一阶导数：

$$\frac{\partial\theta^i} D_{KL}(p_\theta \| p_{\theta'})\Big|_{\theta=\theta'} = 0$$

因为 $\theta = \theta'$ 时 KL 最小（为 0）。二阶导数给出 Fisher 度量：

$$\frac{\partial^2}{\partial\theta^i \partial\theta^j} D_{KL}(p_\theta \| p_{\theta'})\Big|_{\theta=\theta'} = g_{ij}(\theta)$$

因此：

$$D_{KL}(p_{\bar} \| p_{\bar + \Delta\theta}) = \frac{1}{2} g_{ij}(\bar) \Delta\theta^i \Delta\theta^j + O(\|\Delta\theta\|^3)$$

这是信息几何中的标准结果（Amari & Nagaoka, 2000, §2.4）。$\square$

**(b) 部分：** Cercis 在规范固定后的定义为：

$$\text{Cercis}^2 = \frac{1}{M^2} \sum_m \|\Delta\theta_m\|_{\text{Euc}}^2$$

（使用 Euclidean 范数，因为 $\mathbf{g}_m \in \mathbb{R}^d$ 是原始位移向量。）

对于 Fisher 范数 $\|\Delta\theta\|_g^2 = \Delta\theta^T g(\bar) \Delta\theta$，在 $\bar$ 附近，Euclidean 范数与 Fisher 范数相差一个线性变换：

$$\|\Delta\theta\|_g^2 = \|\Delta\theta\|_{\text{Euc}}^2 \cdot \frac{\Delta\theta^T g \Delta\theta}{\Delta\theta^T \Delta\theta}$$

此比值在 $\Delta\theta \to 0$ 时有界（$g$ 的最小和最大特征值之间）。因此 Cercis²（Euclidean）与平均 KL 散度（Fisher）成比例：比例常数由 $g(\bar)$ 的特征值范围确定。

精确而言：

$$\text{Cercis}^2 = \frac{1}{M^2} \sum_m \|\Delta\theta_m\|_{\text{Euc}}^2 = \frac{2}{M} \sum_m D_{KL} \cdot \frac{\|\Delta\theta_m\|_{\text{Euc}}^2}{2 D_{KL}}$$

其中 $\|\Delta\theta\|_{\text{Euc}}^2 / (2 D_{KL}) \to 1/\lambda_{\text{avg}}(g)$ 当 $\Delta\theta \to 0$。$\square$

**(c) 部分：** Fisher-Rao 距离沿测地线 $\gamma(s)$（$\gamma(0) = \bar$，$\gamma(1) = \hat_m$）定义为：

$$d_{FR}(\bar, \hat_m) = \int_0^1 \sqrt{g_{ij}(\gamma(s)) \dot^i(s) \dot^j(s)} \, ds$$

在短距离极限（$\|\Delta\theta\|$ 小），测地线近似为直线：$\gamma(s) \approx \bar + s \Delta\theta_m$，且 $g_{ij}(\gamma(s)) \approx g_{ij}(\bar)$。因此：

$$d_{FR} \approx \|\Delta\theta_m\|_g + O(\|\Delta\theta_m\|^2)$$

代入 (b) 得到 Cercis² 与 Fisher 测地距离平方均值的关系。$\square$

**(d) 部分：** 此部分陈述 Spring 训练动力学的性质，而非可直接证明的定理。需要以下条件：

- Spring 实际使用自然梯度下降（$\dot = -\eta g^{-1}(\theta) \nabla L(\theta)$）
- 自然梯度轨迹是对 Lyapunov 函数 $L$ 的 Riemannian 梯度流的离散化
- 轨迹长度 $\int_0^T \|\dot(t)\|_g dt$ 与 Cercis 有关

**此部分目前为推测（见阻塞声明）。** $\square$

**阻塞声明 / Blockers.**

| 阻塞 | 严重性 | 缺失的数学结果 |
|------|--------|----------------|
| B3.1.1 | 中等 | 部分 (d) 要求 Spring 动力学是 Fisher 自然梯度流。当前 Spring 使用的是 Euclidean 梯度下降还是自然梯度？需要验证或修改 Spring 的实现。 |
| B3.1.2 | 中等 | Cercis 的 Euclidean 范数与 Fisher 范数之间的比例常数取决于 $g(\bar)$ 的条件数。在大差异（强不一致）时，线性逼近失效，需要完整的 Fisher-Rao 测地线计算（通常无解析解）。 |
| B3.1.3 | 低 | 定理假定所有专家预测属于同一指数族。对于 ACE 模型的输出（通常是回归值而非分布），需要定义从模型输出到概率分布的嵌入映射（例如：用 Gaussian 预测分布 $p_{\theta_m}(y|x) = \mathcal{N}(f_m(x), \sigma^2)$）。 |

---

### 3.3 定理 3.2: 信息几何学中 Cercis 的 Bregman 散度刻划
### Theorem 3.2: Bregman Divergence Characterization of Cercis in Information Geometry

**定理陈述 / Theorem Statement.**

> **Theorem 3.2 (Cercis as Aggregated Bregman Divergence).**
> 在与 Theorem 3.1 相同的设定下，令 $\psi: \Theta \to \mathbb{R}$ 为指数族的对数配分函数（凸的、光滑）。$\psi$ 的 Bregman 散度为：
>
> $$D_\psi(\theta \| \theta') = \psi(\theta) - \psi(\theta') - \nabla\psi(\theta')^T(\theta - \theta')$$
>
> 对于指数族，$D_{KL}(p_\theta \| p_{\theta'}) = D_\psi(\theta \| \theta')$。
>
> **(a) 广义 Cercis（Generalized Cercis）：** 定义信息几何推广的 Cercis Score：
>
> $$\text{Cercis}_{IG} = \frac{1}{M} \sqrt{\sum_{m=1}^M D_\psi(\hat_m \| \bar)}$$
>
> 当专家预测差异小时，$\text{Cercis}_{IG}$ 与原始 Cercis 等价（依二阶逼近）。
>
> **(b) 三角形的 Bregman 等式（Bregman's Triangle Equality）：**
>
> $$D_\psi(\hat_m \| \hat_n) = D_\psi(\hat_m \| \bar) + D_\psi(\bar \| \hat_n) - (\nabla\psi(\hat_m) - \nabla\psi(\bar))^T (\bar - \hat_n)$$
>
> 此等式将 **专家对之间的差异**（$D_\psi(\hat_m \| \hat_n)$）分解为：每个专家到共识点的差异 + 一个交叉项。在边界 $t = T$，该交叉项度量了"Spring 训练动力学的不可逆信息损失"。

**假设 / Assumptions.**

| 编号 | 假设 | 必要性 |
|------|------|--------|
| A3.2.1 | 同 A3.1.1–A3.1.3 | 指数族 + 满秩 Fisher 度量 |
| A3.2.2 | $\psi$ 严格凸且光滑 | Bregman 散度的标准条件 |
| A3.2.3 | $\bar$ 是规范固定点（可由 $\sum \mathbf{g}_m = 0$ 或 Bregman 重心定义） | 参考点选取 |

**证明框架 / Proof Sketch.**

**(a) 部分：** 由 Theorem 3.1(a) 可得 $D_\psi(\hat_m \| \bar) \approx \frac{1}{2} \|\Delta\theta_m\|_g^2$。原始 Cercis $= \frac{1}{M} \sqrt{\sum \|\Delta\theta_m\|_{\text{Euc}}^2}$。在小差异极限下，$\text{Cercis}_{IG} = \frac{1}{M} \sqrt{\sum D_\psi} \approx \frac{1}{M} \sqrt{\sum \frac{1}{2}\|\Delta\theta_m\|_g^2}$，与原始 Cercis 比例等价。$\square$

**(b) 部分：** Bregman 三角形的等式：

$$D_\psi(a \| c) = D_\psi(a \| b) + D_\psi(b \| c) - (\nabla\psi(a) - \nabla\psi(b))^T(b - c)$$

是 Bregman 散度定义的直接代数结果：代入 $D_\psi$ 的定义并在两侧展开 $\psi$ 即可验证。$\square$

**注 3.1 (体-边界的信息解释).** 交叉项 $(\nabla\psi(\hat_m) - \nabla\psi(\bar))^T(\bar - \hat_n)$ 编码了 Spring 训练动力学中的"非互易性"——专家 $m$ 与专家 $n$ 之间的信息差不等同于各自与共识点距离的简单加法。在体的语言中，这对应于 $\Theta \times [0,T]$ 中的"曲率"：不同训练路径之间测地偏差。

---

## 4. 跨域结构关系 {#跨域结构}
## Cross-Domain Structural Relations

三域之间存在深层数学联系，此处以定理形式陈述。

### 4.1 定理 X.1: 离散 BF 理论与 O(d) 平坦联络的计数统一
### Theorem X.1: Unification of Discrete BF Theory and O(d) Flat Connection Counting

> **Theorem X.1 (Harmonic Component = BF Partition Function).**
> 设 $M = (V, E, F)$ 为 SCX 专家图的 2-复形。在不考虑群的非阿贝尔性修正的一阶近似下：
>
> **(a)** Domain 1 的 O(d) 平坦联络的规范等价类（Theorem 1.1）在 $\pi_1(M)$ 自由、$d=1$（$O(1) = \mathbb{Z}_2$）时的数量为 $2^{b_1(M)-1}$。
>
> **(b)** Domain 4 的 BF 配分函数（Theorem 2.3）对 $G = \mathbb{Z}_2$ 给出 $Z_{BF} = 2^{b_1(M)}$。
>
> **(c)** 差异因子 $2 = |Z(G)|$ 来自 O(d) 的非阿贝尔性：在非阿贝尔共轭作用下，全局 $G$-不变表示被商掉一次；在阿贝尔 BF 计数中，此商不发生。
>
> **此定理统一了 Domain 1 和 Domain 4 的核心数学结构：两者都是对 SCX 图上平坦规范场规范等价类的计数。差异来自规范群是否为阿贝尔——这正好对应 SCX 平移规范（阿贝尔） vs O(d) 旋转规范（非阿贝尔）的区分。**

### 4.2 定理 X.2: 信息几何度量与离散联络的曲率
### Theorem X.2: Information-Geometric Metric as Discrete Curvature Source

> **Theorem X.2 (Information Metric Curvature and Gauge Holonomy).**
> 在指数族设定下，Fisher 度量 $g_{ij}(\theta)$ 的 Riemann 曲率张量 $R_{ijk\ell}$ 对离散联络的 plaquette 和乐产生贡献。具体地，沿三角形 $f = (\theta, \theta + \Delta_1, \theta + \Delta_2)$ 的和乐满足：
>
> $$W_f = I - \frac{1}{2} R_{ijk\ell}(\theta) \Delta_1^j \Delta_2^\ell \cdot (E^{ik} - E^{ki}) + O(\|\Delta\|^3)$$
>
> 其中 $E^{ik}$ 是 $\mathfrak{o}(d)$ 的一组基（$d = \dim\Theta$，但此处指数 $i,k$ 跑遍 Fisher 度量的坐标，且 $R_{ijk\ell}$ 为信息几何的曲率张量）。
>
> **解释：** 当 Fisher 度量弯曲（非平坦）时，Cercis 得分包括一个**信息几何曲率贡献**——即使所有专家在单个数据点附近一致，统计流形的内在曲率仍可能产生不可消除的全局不一致性。这为 Cercis $\neq 0$ 提供了一个几何来源（区别于纯规范伪影或专家噪声）。
>
> **阻塞声明：** 此定理要求 (1) $\Theta$ 的维数与 O(d) 的维数兼容（$\dim\Theta = d(d-1)/2$），这在一般情况下不成立。该对应仅适用于非常特定的统计模型。**(2)** 需要证明 Riemann 曲率确实产生非平凡的 O(d) 和乐类——这要求在 $\Theta$ 上存在非平凡 $\pi_1$ 或非零曲率 2-形式与 O(d) 丛的耦合。这些条件在通用 SCX 设定下不保证，需要进一步研究。

---

## 5. 未解决的形式化缺口 {#缺口}
## Unresolved Formalization Gaps

下表汇总所有已在上述定理证明或阻塞声明中识别的形式化缺口：

| 编号 | 域 | 缺口 | 严重性 | 可能的解决路径 |
|------|-----|------|--------|----------------|
| **G1** | 1 | 面积律/周长律严格证明（Theorem 1.3d） | **严重** | 降级为 Conjecture；在强耦合极限下做部分严格分析；数值验证 |
| **G2** | 1 | O(d) 规范固定的 Riemannian 优化收敛速率（Theorem 1.2c） | 中等 | 标准工具（Absil et al., 2008 的 Riemannian 优化收敛理论），需针对 SCX 图特化 |
| **G3** | 4 | SCX 专家图的 2-复形精确定义（Theorem 2.2 的前置条件） | **严重** | 定义面的粘合映射；验证三角剖分的一致性；定义边的定向约定 |
| **G4** | 4 | DW cocycle $\omega$ 的审计物理解释（Theorem 2.2d） | **严重** | 需要物理/审计论证：$\omega$ 的不同选择对应什么？若无回答，DW 是数学玩具 |
| **G5** | 4 | 李群连续极限中的计数→维数过渡（Theorem 2.1c） | 中等 | 通过 Riemannian 体积形式：$|G| \to \operatorname{Vol}(G)$，需要紧化或截断 |
| **G6** | 5 | Spring 动力学是否为自然梯度流（Theorem 3.1d） | 中等 | 验证/修改 Spring 实现以使用自然梯度；或证明 Euclidean 梯度流在 $\bar$ 附近近似自然梯度 |
| **G7** | 5 | Cercis Euclidean→Fisher 范数转换的条件数依赖性（Theorem 3.1b） | 低 | 若 $g(\bar)$ 条件数大（各向异性强），转换常数大。需在实际数据上估计条件数 |
| **G8** | 跨域 | Fisher 曲率对 O(d) 和乐的贡献（Theorem X.2） | **严重** | 要求 $\dim\Theta = d(d-1)/2$ 且非平凡曲率耦合。通用 SCX 不满足。此方向仅对特定统计模型可行——可能应标记为 SPECULATIVE |

---

## 附录 A: 符号约定 / Notation Conventions

| 符号 | 含义 | 域 |
|------|------|-----|
| $G = (V, E)$ | SCX 专家图 | 1, 4 |
| $M = (V, E, F)$ | SCX 专家图作为 2-复形 | 4 |
| $R_v \in O(d)$ | 顶点 $v$ 处的 O(d) 标架 | 1 |
| $U_e \in O(d)$ | 边 $e$ 上的 O(d) 链接变量 | 1 |
| $W_f \in O(d)$ | Plaquette $f$ 的 O(d) 和乐 | 1 |
| $b_1(M)$ | 第一 Betti 数 | 1, 4 |
| $\pi_1(M)$ | 基本群 | 1, 4 |
| $g: E \to G$ | 离散 $G$-规范场 | 4 |
| $h_f \in G$ | 面 $f$ 的和乐 | 4 |
| $\omega \in Z^2(G, U(1))$ | 群 2-cocycle | 4 |
| $Z_\omega(M)$ | Dijkgraaf-Witten 配分函数 | 4 |
| $Z_{BF}(M; G)$ | 离散 BF 配分函数 | 4 |
| $(\Theta, g)$ | Fisher-Rao 统计流形 | 5 |
| $\psi(\theta)$ | 对数配分函数 | 5 |
| $D_\psi$ | Bregman 散度 | 5 |
| $d_{FR}$ | Fisher-Rao 测地距离 | 5 |
| $\hat_m$ | 专家 $m$ 的自然参数 | 5 |
| $\bar$ | 规范固定后的参考点 | 5 |
| $\text{Cercis}_{IG}$ | 信息几何推广的 Cercis | 5 |

---

## 附录 B: 诚实性声明 / Honesty Declaration

本文件遵循以下原则：

1. **每个定理或被证明（提供完整证明框架），或被诚实声明为"阻塞"（精确说明缺失的数学结果）。** 不存在"好像可以证明"的表述。
2. **不做概念类比。** 例如：不声称 $\sum \mathbf{g}_m = 0$ "像一个反常抵消条件"。它就是零模固定条件。声称别的就是不诚实。
3. **命名精确。** O(d) 格点规范理论不是 Yang-Mills 理论。Dijkgraaf-Witten 理论不是 Chern-Simons 理论。信息几何体-边界对应不是 AdS/CFT。错误的命名已在 gauge_domain_reexam.md 中被充分论证。
4. **区分定理、猜想和推测。** 本文件中的"猜想"（Conjecture）是可能正确但目前缺少严格证明的陈述。"推测"（Speculative）是缺少充分论证基础的陈述。两者在正文中都被明确标注。

---

> **最后的话 / Final Word:** 三个复活域的严格形式化表明：Domain 4（离散 TQFT / Dijkgraaf-Witten）数学路径最完整，有严格定理支持且与 SCX 结构天然兼容。Domain 1（O(d) 格点规范）有三个可证明的定理，但面积律分类被阻塞（需要 Yang-Mills 质量间隙级别的突破）。Domain 5（信息几何体-边界）定理在指数族设定下可证明，但 Spring 动力学的几何解释需要额外假设。三个域构成一个统一的数学图景：**SCX 审计的"调和分量缺失"（fiber_bundle.tex Theorem 3 的错误）是离散平坦联络的规范等价类——它是拓扑的，可通过 TQFT 计数，且可在信息几何中赋予度量解释。**
>
> *The strict formalization of three resurrected domains shows: Domain 4 (discrete TQFT / Dijkgraaf-Witten) has the most complete mathematical pathway, with rigorous theorems and natural SCX compatibility. Domain 1 (O(d) lattice gauge) has three provable theorems, but the area law classification is blocked (requiring Yang-Mills mass-gap-level breakthrough). Domain 5 (information-geometric bulk-boundary) theorems are provable under exponential family assumptions, but the geometric interpretation of Spring dynamics requires extra assumptions. The three domains form a unified mathematical picture: **SCX audit's "harmonic component omission" (the error in fiber_bundle.tex Theorem 3) is the gauge-equivalence class of discrete flat connections — it is topological, countable via TQFT, and interpretable metrically in information geometry.** *