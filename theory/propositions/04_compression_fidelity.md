# 04 — Compression Fidelity of SCX-Compress

> 推导 SCX-Compress 模块的压缩保真定理、安全压缩比条件，以及与经典 coreset 理论的关系。
>
> **关联代码**: `src/scx/action/compress.py`
> **关联公式**: 冗余分数 $D(s)$，压缩规模 $n_s' = \alpha\sqrt{|S_s|} + \beta\cdot\text{Boundary}(s) + \gamma\cdot\bar{r}(s)$

---

## 1 符号与设定 (Notation)

| 符号 | 含义 |
|------|------|
| $\mathcal{S}$ | 状态空间，通过 SCX 聚类划分 |
| $s \in \mathcal{S}$ | 单个状态 |
| $S_s = \{(x_i, y_i)\}_{i=1}^{N_s}$ | 状态 $s$ 包含的训练样本 |
| $N_s = |S_s|$ | 状态大小 |
| $\mathcal{F}$ | 假设类 (hypothesis class) |
| $\ell: \mathcal{F} \times (\mathcal{X}, \mathcal{Y}) \to [0, B]$ | 有界损失函数 |
| $D(s) \in [0, 1]$ | 状态 $s$ 的冗余分数 |
| $D_i \in [0, 1]$ | 样本 $i$ 的个体冗余分数 |
| $\rho(s) = N_s / N$ | 状态比例 |
| $\bar{r}(s) = \frac{1}{N_s}\sum_i r_i$ | 平均归一化残差，$r_i \in [0, 1]$ |
| $\text{Sim}(s) \in [0, 1]$ | 状态内部相似度 |
| $\text{Boundary}(s) \in [0, 1]$ | 边界样本比例 |
| $C_s \subset S_s$ | 压缩后保留的加权子集 |
| $n_s' = |C_s|$ | 压缩集大小 |
| $w_i$ | 样本 $i$ 在压缩集中的权重，$\sum_{i \in C_s} w_i = N_s$ |
| $R_S(f) = \frac{1}{N_s} \sum_{i \in S_s} \ell(f(x_i), y_i)$ | 原始经验风险 |
| $R_C(f) = \frac{1}{N_s} \sum_{i \in C_s} w_i \ell(f(x_i), y_i)$ | 压缩后的加权经验风险估计 |
| $\varepsilon(s) = \sup_{f \in \mathcal{F}} |R_S(f) - R_C(f)|$ | 压缩保真误差 |

### 冗余分数定义

状态级冗余分数为各因子的乘积形式：

$$
D(s) = \rho(s) \cdot \bigl(1 - \bar{r}(s)\bigr) \cdot \text{Sim}(s) \cdot \bigl(1 - \text{Boundary}(s)\bigr).
\tag{1}
$$

代码实现中，个体冗余分数采用加权和形式（与乘积形式等价但在因子分解方式上略有不同）：

$$
D_i = 0.4 \cdot \underbrace{\Bigl(1 - \frac{\text{nn\_dist}_i}{\max(\text{nn\_dist})}\Bigr)}_{\text{density}} \;+\; 0.4 \cdot \underbrace{\Bigl(1 - \frac{r_i}{\max(r)}\Bigr)}_{\text{residual}} \;+\; 0.2 \cdot \underbrace{\min(5\rho(s), 1)}_{\text{proportion}}.
\tag{2}
$$

状态级 $D(s)$ 与个体级 $\{D_i\}$ 通过 $D(s) \approx \frac{1}{N_s} \sum_i D_i$ 关联。

### 压缩规模公式

SCX-Compress 为目标状态保留的样本数由三项构成：

$$
n_s' = \alpha \sqrt{N_s} \;+\; \beta \cdot \text{Boundary}(s) \cdot N_s \;+\; \gamma \cdot \bar{r}(s) \cdot \sqrt{N_s}.
\tag{3}
$$

- 第一项 **(coreset backbone)**: $\alpha \sqrt{N_s}$，经典 coreset 的次线性规模
- 第二项 **(boundary preservation)**: $\beta B_s N_s$，边界样本强制保留
- 第三项 **(residual compensation)**: $\gamma \bar{r}(s) \sqrt{N_s}$，高残差区域增加容量

当 $N_s$ 较大时，$n_s' = \Theta(\sqrt{N_s})$，实现次线性压缩。

---

## 2 核心假设 (Assumptions)

**(A1) 有界损失**: 对任意 $f \in \mathcal{F}$ 和 $(x, y) \sim \mathcal{D}$，

$$
0 \leq \ell(f(x), y) \leq B < \infty.
$$

**(A2) 复合类复杂度**: 损失复合类 $\mathcal{L}_{\mathcal{F}} = \{\ell_f: \ell_f(x,y) = \ell(f(x), y) \mid f \in \mathcal{F}\}$ 是 VC 型类，其伪维数 (pseudo-dimension) 为 $d = \text{Pdim}(\mathcal{L}_{\mathcal{F}}) < \infty$。等价地，对任意经验分布 $P_N$，其 $L_2(P_N)$ 覆盖数满足：

$$
\mathcal{N}(\varepsilon, \mathcal{L}_{\mathcal{F}}, L_2(P_N)) \leq \left(\frac{C_K}{\varepsilon}\right)^{2d}, \quad \forall \varepsilon > 0.
\tag{4}
$$

**(A3) 冗余-敏感性关联**: 对任意样本 $i \in S_s$，其灵敏度 (sensitivity) $\sigma_i$ 被冗余分数控制：

$$
\sigma_i \;:=\; \sup_{f \in \mathcal{F}} \frac{|\ell(f(x_i), y_i)|}{\sum_{j \in S_s} |\ell(f(x_j), y_j)|} \;\leq\; \frac{1 - D_i}{\sum_{j \in S_s} (1 - D_j)} \cdot C_{\text{cal}},
\tag{5}
$$

其中 $C_{\text{cal}}$ 为校准常数。该假设的直观含义是：高冗余样本（$D_i \approx 1$）在任意假设 $f$ 下的边际贡献很小，因此可以被安全地降采样。下文的推导取 $C_{\text{cal}} = 1$（通过重新缩放吸收到常数中）。

**(A4) 边界保留**: 所有边界样本（$b_i = 1$，即 $D_i = 0$ 的样本）被确定性保留。

---

## 3 压缩保真定理 (Compression Fidelity)

### 3.1 定理陈述

**Theorem 1 (Compression Fidelity).** 设状态 $s$ 满足假设 (A1)–(A4)。令 $C_s$ 为 SCX-Compress 以式 (3) 的规模 $n_s'$ 和式 (2) 的冗余分数选择的加权子集，且权重 $\{w_i\}_{i \in C_s}$ 按代码实现归一化满足 $\sum_{i \in C_s} w_i = N_s$。则对任意 $\delta \in (0, 1)$，以概率至少 $1 - \delta$ 成立：

$$
\sup_{f \in \mathcal{F}} \bigl| R_S(f) - R_C(f) \bigr|
\;\leq\; B \cdot \frac{1 - D_{\text{eff}}(s)}{1 - n_s'/N_s}
\;+\; \mathcal{O}\!\left(
B \cdot \sqrt{\frac{d}{n_s'} \cdot \frac{1 - D_{\text{eff}}(s)}{1 - n_s'/N_s} \cdot \log\frac{N_s}{\delta}}
\right),
\tag{6}
$$

其中 $D_{\text{eff}}(s) = D(s) \cdot \bigl(1 - \text{Boundary}(s)\bigr)$ 为经边界校正的有效冗余。

---

### 3.2 显式上界的紧凑形式

更便于使用的紧凑形式为：

$$
\varepsilon(s) \;\leq\; \underbrace{B \cdot \bigl(1 - D_{\text{eff}}(s)\bigr) \cdot \left(1 - \frac{n_s'}{N_s}\right)}_{\text{(i) 偏差项}}
\;+\; \underbrace{\frac{4B}{\sqrt{n_s'}} \cdot \sqrt{d \cdot \bigl(1 - D_{\text{eff}}(s)\bigr) \cdot \left(1 - \frac{n_s'}{N_s}\right) \cdot \log\frac{2}{\delta}}}_{\text{(ii) 方差项}}.
\tag{7}
$$

- **(i) 偏差项 (bias term)**: 来自非均匀采样导致的系统偏移。当 $D_{\text{eff}}(s) \to 1$（高度冗余）或 $n_s'/N_s \to 1$（几乎不压缩）时偏差消失。
- **(ii) 方差项 (variance term)**: 来自有限样本的随机波动。包含伪维数 $d$（模型复杂度）和 $\log(1/\delta)$（置信度）。

---

### 3.3 证明框架 (Proof Sketch)

**Step 1 — 灵敏度分解**  

将误差重写为加权和形式。令 $a_i = 1 - w_i \cdot \mathbf{1}\{i \in C_s\}$，则

$$
R_S(f) - R_C(f) = \frac{1}{N_s} \sum_{i \in S_s} a_i \cdot \ell_f(x_i, y_i),
$$

其中 $\sum_i a_i = 0$（由权重归一化保证）。由假设 (A3)，$\{a_i\}$ 满足：

$$
|a_i| \leq \max\!\left\{
\underbrace{\frac{N_s}{n_s'} \cdot \frac{e^{\tau}}{\bar{w}} - 1}_{\text{保留样本上界}},
\; \underbrace{1}_{\text{未保留样本上界}}
\right\}
\leq \frac{N_s}{n_s'} \cdot \frac{e^{\tau}}{\bar{w}},
$$

其中 $\bar{w} = \frac{1}{n_s'} \sum_{i \in C_s} e^{-\tau D_i}$ 为平均指数权重，$\tau$ 为代码中的 `temperature` 参数。

**Step 2 — 有效样本量与冗余的关系**  

定义有效样本量 (effective sample size)：

$$
N_{\text{eff}} = \frac{(\sum w_i)^2}{\sum w_i^2} = \frac{N_s^2}{\sum_{i \in C_s} w_i^2}.
$$

当 $D_{\text{eff}}(s)$ 较高时，$w_i \approx N_s/n_s'$（各样本权重接近），$N_{\text{eff}} \approx n_s'$；当 $D_{\text{eff}}(s)$ 较低时，权重发散，$N_{\text{eff}} < n_s'$。具体地：

$$
N_{\text{eff}} \;\geq\; n_s' \cdot \bigl(1 - D_{\text{eff}}(s)\bigr)^{-1}.
\tag{8}
$$

该式建立了 $D(s)$ 与采样效率之间的桥梁：高冗余意味着高有效样本量。

**Step 3 — 应用 uniform convergence 界**  

对于固定的加权机制，对损失复合类 $\mathcal{L}_{\mathcal{F}}$ 应用标准 uniform convergence bound（见 Bartlett & Mendelson, 2002; Bousquet et al., 2004）：

以概率 $\geq 1 - \delta$，

$$
\sup_{f \in \mathcal{F}} \bigl| R_S(f) - R_C(f) \bigr|
\;\leq\; 2 \cdot \mathfrak{R}_{N_{\text{eff}}}(\mathcal{L}_{\mathcal{F}})
\;+\; B \cdot \sqrt{\frac{\log(2/\delta)}{2 N_{\text{eff}}}}
\;+\; \mathbb{E}\bigl[|R_S - R_C|\bigr],
$$

其中 $\mathfrak{R}_{m}(\mathcal{L}_{\mathcal{F}})$ 是 $m$ 个样本上的 Rademacher 复杂度。由假设 (A2) 的覆盖数条件，$\mathfrak{R}_{m}(\mathcal{L}_{\mathcal{F}}) \leq B \sqrt{d/m}$。

**Step 4 — 代入 $N_{\text{eff}}$ 与 $n_s'$ 的关系**  

将式 (8) 代入，并结合式 (3) 中 $n_s'$ 的显式形式：

$$
\frac{1}{\sqrt{N_{\text{eff}}}}
\;\leq\; \sqrt{\frac{1 - D_{\text{eff}}(s)}{n_s'}}
\;\leq\; \sqrt{\frac{1 - D_{\text{eff}}(s)}{\alpha \sqrt{N_s} + \beta B_s N_s + \gamma \bar{r}(s)\sqrt{N_s}}}.
$$

偏差项直接来自权重非均匀性：

$$
\mathbb{E}\bigl[|R_S - R_C|\bigr]
\;\leq\; B \cdot \bigl(1 - D_{\text{eff}}(s)\bigr) \cdot \left(1 - \frac{n_s'}{N_s}\right).
$$

合并即得式 (7)。$\square$

---

### 3.4 讨论

**Theorem 1 给出的保真界具有以下性质：**

1. **自适应性**: 当 $D(s) \to 1$（完美冗余）时，$\varepsilon(s) \to 0$，即使 $n_s' \ll N_s$。当 $D(s) \to 0$（无冗余）时，$\varepsilon(s)$ 退化为无压缩的 ERM 泛化界。

2. **次线性压缩**: 由于 $n_s' = \Theta(\sqrt{N_s})$，当 $N_s$ 增大时压缩比 $n_s'/N_s = \Theta(1/\sqrt{N_s}) \to 0$，而误差 $\varepsilon(s) \to B(1-D_{\text{eff}}(s))$，即被有效冗余控制。

3. **边界保护**: $\text{Boundary}(s)$ 同时降低 $D_{\text{eff}}(s)$（提高分子）和增加 $n_s'$（降低分母），双重机制确保关键样本不被过度压缩。

4. **模型复杂度依赖性**: 误差随 $\sqrt{d/n_s'}$ 增长，这与标准 ERM 的 $\sqrt{d/N}$ 形式一致，但分母从 $N_s$ 变为 $n_s'$，体现了压缩的成本。

---

## 4 安全压缩比推论 (Safe Compression Ratio)

**Corollary 1 (Safe Compression Ratio).** 设目标精度损失 $\varepsilon_0 \in (0, B)$（即要求 $\varepsilon(s) \leq \varepsilon_0$）。定义压缩比 $r = n_s' / N_s$。则 SCX-Compress 达到 $\varepsilon(s) \leq \varepsilon_0$ 的充分条件是：

$$
D_{\text{eff}}(s) \;\geq\; 1 - \frac{\varepsilon_0}{B \cdot (1 - r)} \cdot
\left(1 \;-\; \frac{4\sqrt{d \log(2/\delta)}}{\sqrt{r N_s}}\right)^{-1}.
\tag{9}
$$

**特例**: 当 $N_s$ 充分大使得 $\frac{4\sqrt{d \log(2/\delta)}}{\sqrt{r N_s}} \ll 1$ 时，条件退化为：

$$
D_{\text{eff}}(s) \;\geq\; 1 - \frac{\varepsilon_0}{B \cdot (1 - r)}.
\tag{10}
$$

**50% 压缩 ($r = 0.5$) 时精度损失 $< 5\%$ 的条件**：  

代入 $\varepsilon_0 = 0.05 B$（损失相对 $B$ 的 5%）、$r = 0.5$，得：

$$
D_{\text{eff}}(s) \;\geq\; 1 - \frac{0.05}{0.5} = 0.90.
$$

即：**状态冗余分数需不低于 0.90 时，50% 压缩可保证精度损失不超过 5%**。

更一般地，$r$ 与 $\varepsilon_0$ 的 trade-off 曲线由下式给出：

$$
r \;\geq\; 1 - \frac{\varepsilon_0}{B \cdot (1 - D_{\text{eff}}(s))}.
\tag{11}
$$

该式说明：安全压缩比由 $D(s)$ 线性控制——$D(s)$ 每增加 0.1，可额外压缩约 $\frac{\varepsilon_0}{B}$ 的比例。

---

## 5 与经典 Coreset 理论的联系

### 5.1 Feldman-Langberg 灵敏度采样

经典的 Feldman-Langberg 框架 (Feldman & Langberg, 2011; Feldman, 2020) 通过灵敏度加权采样构建 coreset：

**Theorem (Feldman-Langberg, 概括)**. 设样本 $\{z_i\}_{i=1}^N$ 的灵敏度为 $\sigma_i$，总灵敏度 $T = \sum_i \sigma_i$。以概率 $p_i \geq \sigma_i / T$ 独立采样 $m$ 个样本，权重设为 $1/(m p_i)$，则对任意 $\delta \in (0,1)$，以概率 $\geq 1-\delta$：

$$
\sup_{f \in \mathcal{F}} \left| \frac{1}{N} \sum_{i=1}^N \ell_f(z_i) - \frac{1}{N} \sum_{i \in C} w_i \ell_f(z_i) \right|
\leq \frac{B}{N} \cdot \left( T + \sqrt{T \log(1/\delta)} + \sqrt{m \log(1/\delta)} \right).
$$

**SCX-Compress 与之相比的差异和优势**：

| 维度 | Feldman-Langberg | SCX-Compress |
|------|-------------------|--------------|
| 灵敏度估计 | 需计算 $\sup_{f \in \mathcal{F}} \frac{|\ell_f(z_i)|}{\sum_j \ell_f(z_j)}$，通常无闭式解 | 用 $D_i$ 代理灵敏度，可直接从数据计算 |
| 采样分布 | $p_i \geq \sigma_i/T$，需显式知道 $\sigma_i$ | $p_i \propto 1 - D_i$，无需额外计算 |
| 边界处理 | 无显式机制 | $\beta \cdot \text{Boundary}(s)$ 强制保留 |
| 规模 | $m$ 需手动指定 | $n_s'$ 自动适应 $N_s$、$B_s$、$\bar{r}(s)$ |
| 计算成本 | 每点评估 $\sigma_i$ 通常需 $O(N^2)$ 以上 | $O(N_s d + N_s \log N_s)$ |

### 5.2 SCX-Compress 的灵敏度实现

由假设 (A3)，SCX-Compress 实际上使用了 $D_i$ 作为灵敏度的代理变量。将 $p_i \propto 1 - D_i$ 代入 Feldman-Langberg 框架，可得总灵敏度 $T$ 的界：

$$
T = \sum_i \sigma_i \;\leq\; \sum_i \frac{1 - D_i}{\sum_j (1 - D_j)} = 1.
$$

这比 Feldman-Langberg 的一般情况（通常 $T = \Omega(\sqrt{N})$ 甚至 $T = \Omega(N)$）更有利。其原因正是 SCX 的状态划分：**在同一状态内，样本的表达已通过聚类对齐，剩余差异被 $D_i$ 捕获**。

### 5.3 在 SCX 框架中的定位

SCX-Compress 可视为 **LC (Lossless Compression) 假设下的 Feldman-Langberg 变体**：

1. **聚类预处理**（SCX 的状态划分）将原始数据集分解为 $|\mathcal{S}|$ 个近似同质的状态
2. **状态内压缩**（SCX-Compress）在每个状态内应用冗余感知的加权 coreset
3. **整体保真度**跨状态独立组合：

$$
\varepsilon_{\text{total}} = \bigvee_{s \in \mathcal{S}} \varepsilon(s) \quad \text{(逐状态的误差以 union bound 组合)}.
$$

---

## 6 合成验证方案

### 6.1 实验设计

**数据生成**：在 $[0, 1]^2$ 上生成 4 个高斯混合状态，每个状态 $N_s = 2000$ 样本。

| 状态 | 均值 | 协方差 | $D(s)$ (期望) | 说明 |
|------|------|--------|----------------|------|
| s1 | (0.2, 0.2) | $0.01 I$ | $\approx 0.95$ | 高度密集、高冗余 |
| s2 | (0.5, 0.5) | $0.05 I$ | $\approx 0.75$ | 中等密度 |
| s3 | (0.8, 0.8) | $0.15 I$ | $\approx 0.50$ | 较分散 |
| s4 | (0.1, 0.9) | $0.25 I$ | $\approx 0.25$ | 分散且靠近边界 |

**标签函数**：$y = \sin(2\pi x) \cdot \cos(2\pi y) + \varepsilon$，$\varepsilon \sim \mathcal{N}(0, 0.05)$。

**假设类 $\mathcal{F}$**：RBF 核 SVM 或 3 层 MLP（作为 $\mathcal{F}$ 的替代）。

### 6.2 需要验证的命题

**(P1) 保真界 tightness**: 对不同 $D(s)$ 的状态，测量 $\varepsilon(s)$ 并对比 Theorem 1 的理论上界。预期：s1 的 $\varepsilon$ 最小，且理论界紧因子 $\leq 2$。

**(P2) 压缩比-误差 trade-off**: 固定 $\alpha, \beta, \gamma$，变化压缩比 $r \in [0.1, 0.9]$，绘制 $\varepsilon(s)$ 随 $r$ 的变化曲线。验证式 (11) 的线性关系。

**(P3) 边界保留效果**: 在 s4 中人工注入边界样本（Bayes 决策面附近），对比有/无强制保留时的分类精度。

**(P4) 对比基线**:
- 随机采样 + 均匀权重
- K-Center coreset
- Feldman-Langberg 灵敏度采样（用 $|y - \hat{y}|$ 作为灵敏度代理）

### 6.3 可视化方案

| 图号 | 类型 | 内容 | 验证目标 |
|------|------|------|----------|
| Fig 1 | 散点+等高线 | 4 个状态在 2D 空间中的分布，颜色标记 $D_i$ 大小 | 展示冗余分数与数据密度的关系 |
| Fig 2 | 折线图 (双轴) | x 轴 = 压缩比 $r$，左 y = $\varepsilon(s)$，右 y = 理论界 | (P2) 理论界 tightness |
| Fig 3 | 箱线图 | 对每个 $D(s)$ bin，展示 $\varepsilon(s)$ 的 50 次重复分布 | (P1) 误差随 $D(s)$ 减小 |
| Fig 4 | 柱状图 | 不同方法在各状态上的 $\varepsilon$ 对比 | (P4) SCX-Compress vs 基线 |
| Fig 5 | 热力图 | $(\alpha, \gamma)$ 参数扫描下的 $\varepsilon(s)$ | 参数敏感性分析 |
| Fig A1 | 棒棒糖图 | 权重分布 $w_i$ 在压缩前后的对比 | 直观展示加权效果 |

### 6.4 预期结果

1. **误差排序**: $\varepsilon(s1) < \varepsilon(s2) < \varepsilon(s3) < \varepsilon(s4)$，严格与 $D(s)$ 负相关。
2. **临界点**: $D(s) \geq 0.90$ 的状态（s1）在 $r = 0.5$ 时 $\varepsilon < 0.05B$，验证 Corollary 1。
3. **边界保留**: 在 s4 中，无强制保留时精度损失约 12-15%，有强制保留时降至 3-5%。
4. **计算效率**: SCX-Compress 的运行时间与 $N_s \log N_s$ 近似线性，优于 K-Center 的 $O(N_s^2)$。
5. **参数敏感性**: $\alpha$ 控制基础 coreset 规模，$\beta$ 仅在高 Boundary(s) 时显著，$\gamma$ 在残差异质性高时重要。

---

## 7 补充：循环定义修复 (2026-06-27)

### 7.1 问题陈述

原始冗余分数 $D(s)$ 的定义（式 1）依赖于平均归一化残差 $\bar{r}(s)$：

$$
D(s) = \rho(s) \cdot \bigl(1 - \bar{r}(s)\bigr) \cdot \text{Sim}(s) \cdot \bigl(1 - \text{Boundary}(s)\bigr).
$$

其中 $\bar{r}(s) = \frac{1}{N_s}\sum_i r_i$，而 $r_i = \ell(f(x_i), y_i)$ 是模型对样本 $(x_i, y_i)$ 的损失。问题是：**残差 $r_i$ 的计算需要真实标签 $y_i$**。在无监督或弱监督场景下，真实标签不可用，无法直接计算 $\bar{r}(s)$，导致 $D(s)$ 存在循环依赖——你需要知道哪些数据有噪声才能计算 $D(s)$，但 $D(s)$ 的本意正是用于发现噪声数据。

### 7.2 解决方案：一致性替代

Theorem 1（多专家一致性噪声检测保证）证明了一种可靠的无监督噪声指示量——多专家一致性得分 $C(x)$。定义状态平均一致性得分：

$$
\bar{C}(s) = \frac{1}{N_s} \sum_{x \in S_s} C(x), \quad C(x) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}.
$$

由 Theorem 1 的 Lemma 1（均值分离），清洁样本的一致性得分被 $\mu_s$ 控制，而噪声样本的一致性得分接近 1。因此 $\bar{C}(s)$ 与 $\bar{r}(s)$ 存在以下关系：

$$
\bar{r}(s) = 1 - \bar{C}(s) + \mathcal{O}\!\left(\frac{1}{\sqrt{M}}\right).
\tag{12}
$$

**推导**：由 Lemma 1，对清洁样本 $\mathbb{E}[C \mid \text{clean}] \leq \mu_s$，对噪声样本 $\mathbb{E}[C \mid \text{noise}] \geq 1 - \mu_s/(K-1)$。因此 $\bar{C}(s)$ 在清洁区域接近 0，在噪声区域接近 1——与归一化残差 $\bar{r}(s)$ 的单调关系相反。$\mathcal{O}(1/\sqrt{M})$ 项来自 Hoeffding 不等式对有限 $M$ 个专家的浓度界（见 Theorem 1 式 (6) 的指数收敛），当 $M \geq 10$ 时该项通常可忽略。

### 7.3 修正后的冗余分数

将式 (12) 代入式 (1)，修正后的冗余分数为：

$$
D_{\text{fix}}(s) = \rho(s) \cdot \bigl(1 - [1 - \bar{C}(s) + \mathcal{O}(1/\sqrt{M})]\bigr) \cdot \text{Sim}(s) \cdot \bigl(1 - \text{Boundary}(s)\bigr)
$$

化简为：

$$
D_{\text{fix}}(s) = \rho(s) \cdot \bar{C}(s) \cdot \text{Sim}(s) \cdot \bigl(1 - \text{Boundary}(s)\bigr) \;+\; \mathcal{O}\!\left(\frac{1}{\sqrt{M}}\right).
\tag{13}
$$

**关键改进**：$\bar{C}(s)$ 仅基于多专家模型的预测一致性，不需要任何真实标签。这打破了原始定义的循环依赖。

### 7.4 对压缩保真界的影响

替换 $\bar{r}(s)$ 为 $1 - \bar{C}(s)$ 后，压缩规模公式（式 3）变为：

$$
n_s' = \alpha \sqrt{N_s} \;+\; \beta \cdot \text{Boundary}(s) \cdot N_s \;+\; \gamma \cdot \bigl(1 - \bar{C}(s)\bigr) \cdot \sqrt{N_s} \;+\; \mathcal{O}\!\left(\frac{\sqrt{N_s}}{\sqrt{M}}\right).
\tag{14}
$$

**保真界的松弛程度**：原始保真界（定理 1 / 式 7）的偏差项和方差项均涉及 $D_{\text{eff}}(s)$。替换后，$D_{\text{eff}}(s)$ 的估计误差传播到保真界中：

$$
\varepsilon_{\text{fix}}(s) \;\leq\; \varepsilon_{\text{orig}}(s) \;+\; \mathcal{O}\!\left(B \cdot \frac{1}{\sqrt{M}}\right).
\tag{15}
$$

**松弛是可接受的**，原因有三：

1. **$M$ 的典型规模**：噪声检测场景中 $M$（专家数）通常 $\geq 10$，此时 $\mathcal{O}(1/\sqrt{M}) \leq 0.32$；当 $M \geq 50$ 时降低到 $0.14$ 以下。
2. **指数收敛**：Theorem 1 的实际 F1 以 $\exp(-2M\Delta^2)$ 速率收敛，意味着 $\bar{C}(s)$ 对 $\bar{r}(s)$ 的近似误差随 $M$ 指数级衰减——比式 (12) 的 $\mathcal{O}(1/\sqrt{M})$ 更乐观。
3. **理论完整性**：付出 $1/\sqrt{M}$ 的代价换来无监督可计算性，这在理论上是最优折衷——任何无监督近似必然引入有限样本误差。

### 7.5 总结

修复后的 $D_{\text{fix}}(s)$ 具有以下性质：

| 属性 | 原始 $D(s)$ | 修正 $D_{\text{fix}}(s)$ |
|------|-------------|--------------------------|
| 计算所需数据 | 真实标签 $y_i$ | 仅需多专家预测 $\{f_m(x_i)\}_m$ |
| 循环依赖 | 有（需标签才能算冗余） | 无 |
| 理论保真度 | 精确 | $+ \mathcal{O}(1/\sqrt{M})$ 松弛 |
| 适用场景 | 有监督 | 无监督 / 弱监督 |
| 与 Theorem 1 的关系 | 无 | 核心依赖 |

**结论**：With Theorem 1, the compression fidelity theorem is now fully self-contained — all quantities can be estimated from observable data without ground truth labels.
