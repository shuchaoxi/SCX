# Spring 自进化算法 — 数学谱系学

> **Spring (春季)** = Spring Self-Evolving Gatekeeper (SSEG)
> **地位**: Paper 2 (Nature Computational Science 目标) 的核心算法
> **文档类型**: 理论根源追溯 — 数学领域归属、关键思想来源、历史发展脉络、与前人工作的对比
> **日期**: 2026-06-28

---

## 目录

1. [数学领域归属](#1-数学领域归属)
2. [关键思想与证明工具](#2-关键思想与证明工具)
3. [历史发展时间线](#3-历史发展时间线)
4. [Spring 与前人的对比表](#4-spring-与前人的对比表)
5. [Spring 独有的贡献](#5-spring-独有的贡献)

---

## 1. 数学领域归属

Spring 自进化算法并非属于单一数学领域，而是跨越七个经典数学领域，在它们的交汇处合成全新结构。

### 1.1 随机逼近 (Stochastic Approximation)

**根源**: Robbins & Monro (1951). "A stochastic approximation method." *Annals of Mathematical Statistics*, 22(3), 400-407.

**Spring 中的角色**: NEP 学生参数 $\theta_t$ 的在线更新遵循 Robbins-Monro 递归：

$$\theta_{t+1} = \theta_t - \alpha_t \nabla_\theta \ell(f_{\theta_t}(x_t), y_t)$$

其中学习率 $\alpha_t$ 满足标准 RM 条件：$\sum \alpha_t = \infty$，$\sum \alpha_t^2 < \infty$。

Spring 将标准 RM 推广到**耦合双时间尺度**设置：
- **快时间尺度**: 学生 $\theta_t$ 在固定 gatekeeper $S_t$ 下以速率 $\alpha_t$ 更新
- **慢时间尺度**: gatekeeper $S_t$ 在学生准稳态下以速率 $\beta_t = o(\alpha_t)$ 更新

这对应于 Borkar (2008) 的双时间尺度随机逼近框架，条件 C6' ($\beta_t = o(\alpha_t)$) 是关键创新——它同时保证学生局部收敛与累积分布偏移有限。

**参考文献**:
- Robbins & Monro (1951)
- Kushner & Yin (2003). *Stochastic Approximation and Recursive Algorithms and Applications*
- Borkar (2008). *Stochastic Approximation: A Dynamical Systems Viewpoint*
- Polyak & Juditsky (1992). "Acceleration of stochastic approximation by averaging"

### 1.2 动力系统 / Lyapunov 稳定性

**根源**: Lyapunov, A. M. (1892). *The General Problem of the Stability of Motion*. Kharkov Mathematical Society.

**Spring 中的角色**: Spring 自进化循环是一个离散动力系统：

$$z_{t+1} = \Phi(z_t), \quad z_t = (S_t, M_t, \theta_t) \in \mathcal{Z}$$

其中 $\Phi = (\Phi_S, \Phi_M, \Phi_\theta)$ 是更新算子，$\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$ 是演化状态空间。

Lyapunov 函数候选为（在固定参考集 $M_0$ 上求值）：

$$\Psi(S_t, \theta_t) = \frac{1}{|M_0|} \sum_{x \in M_0} (S_t(x, y(x)) - \hat{C}(x))^2 + \lambda \cdot \frac{1}{|V_0|} \sum_{(x,y) \in V_0} \ell(f_{\theta_t}(x), y)$$

Lyapunov 下降性质 $\mathbb{E}[\Psi_{t+1} \mid \mathcal{F}_t] \leq \Psi_t$ 经 Theorem 12.5 在参考集重放机制下被完整证明。不动点 $(S^*, \theta^*)$ 满足自洽耦合方程，$\omega$-极限集为单点。

Spring 使用了动力系统的完整工具链：吸引子、盆地、相图（四种收敛机制）、$\omega$-极限集。

**参考文献**:
- Lyapunov (1892). *The General Problem of the Stability of Motion*
- Khalil (2002). *Nonlinear Systems* (3rd ed.)
- Strogatz (2018). *Nonlinear Dynamics and Chaos* (2nd ed.)
- Conley (1978). *Isolated Invariant Sets and the Morse Index*

### 1.3 贝叶斯推断 / 鞅理论

**根源**: Doob, J. L. (1953). *Stochastic Processes*. Wiley.

**Spring 中的角色**: Gatekeeper 评分函数 $S_t$ 的演化被解释为贝叶斯后验均值更新：

$$S_t(x,y) = \mathbb{E}_{S \sim P_t}[S(x,y)], \quad P_{t+1}(S) \propto P_t(S) \cdot \mathcal{L}(\mathcal{D}_{t+1} \mid S)$$

定理 (Doob 鞅收敛): 序列 $\{S_t\}_{t \geq 0}$ 是关于滤子 $\mathcal{F}_t = \sigma(\mathcal{M}_1, \dots, \mathcal{M}_t)$ 的 $[0,1]$-有界鞅。由 Doob 鞅收敛定理：

$$S_t(x,y) \xrightarrow{a.s.} S_\infty(x,y), \quad \forall (x,y)$$

重要限制：鞅性质要求模型正确（$S^*$ 在先验 $P_0$ 的支撑内）。在模型错误设定下，后验收敛到 KL 投影 $S^\dagger$ 而非真值 $S^*$。Spring 诚实标注了此限制。

**参考文献**:
- Doob (1953). *Stochastic Processes*
- Doob (1949). "Application of the theory of martingales"
- Ghosh & Ramamoorthi (2003). *Bayesian Nonparametrics*
- van der Vaart (1998). *Asymptotic Statistics*
- Kleijn & van der Vaart (2012). "The Bernstein-von Mises theorem under misspecification"

### 1.4 在线学习 / 遗憾分析

**根源**: Zinkevich, M. (2003). "Online convex programming and generalized infinitesimal gradient ascent." *ICML 2003*.

**Spring 中的角色**: Gatekeeper 的在线梯度下降 (OGD) 更新产生标准遗憾界：

$$\text{Regret}_T \leq 2GR\sqrt{T} \quad \text{(无延迟)}$$

Spring 将该界推广到**延迟反馈**设置（NEP 学生的反馈延迟 $d_t \leq D_{\max}$）：

$$\text{Regret}_T^{\text{delay}} \leq 2GR\sqrt{T} + G^2 D_{\max} \sqrt{T}$$

进一步推广到**增长记忆库**设置——记忆库 $M_t$ 的单调增长提供有效样本复杂度改进：

$$\text{Regret}_T^{\text{eff}} \leq \text{Regret}_T^{\text{delay}} + O\left(T \sqrt{\frac{\text{VC}(\mathcal{H})}{N_T}}\right)$$

随着 $N_T \to \infty$，系统满足**渐近无遗憾**：$\frac{1}{T}\text{Regret}_T^{\text{eff}} \to 0$。

**参考文献**:
- Zinkevich (2003). "Online convex programming"
- Hazan (2016). "Introduction to online convex optimization"
- Joulani et al. (2016). "Online learning under delayed feedback"
- Shalev-Shwartz (2012). "Online learning and online convex optimization"
- Cesa-Bianchi & Lugosi (2006). *Prediction, Learning, and Games*

### 1.5 集中不等式

**根源**:
- Hoeffding, W. (1963). "Probability inequalities for sums of bounded random variables." *JASA*, 58(301), 13-30.
- Chernoff, H. (1952). "A measure of asymptotic efficiency for tests of a hypothesis." *Annals of Mathematical Statistics*, 23(4), 493-507.

**Spring 中的角色**: 在 Spring 的多个关键位置：

1. **共识得分的集中**: 专家一致性 $\hat{C}(x) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ 的 Hoeffding 尾界：
   $$\mathbb{P}(|C - \mathbb{E}[C]| > t) \leq 2\exp(-2M t^2)$$
   当 A2 因专家相关而被违反时，$M$ 被替换为有效专家数 $M_{\text{eff}} = M/(1 + (M-1)\bar{\rho})$。

2. **Chernoff 信息**: 检测问题的最优指数速率由 Chernoff 信息 $\kappa = \text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1)$ 给出，应用于 Theorem 4'。

3. **Bahadur-Rao 精确渐近**: Bernoulli 格子修正因子 $(1-e^{-\lambda^*})^{-1}$ 替代标准的 Chernoff 前缀，将 Theorem 4' 的精确常数收紧 5-12%。

**参考文献**:
- Hoeffding (1963)
- Chernoff (1952)
- Bahadur & Rao (1960). "On deviations of the sample mean"
- Dembo & Zeitouni (2010). *Large Deviations Techniques and Applications*

### 1.6 信息论

**根源**:
- Fano, R. M. (1961). *Transmission of Information: A Statistical Theory of Communications*. MIT Press.
- Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.

**Spring 中的角色**:

1. **Fano 不等式**: 用于 Theorem 2（弱特征失败）的下界——当特征 $\phi$ 与真实状态 $S$ 的互信息 $I(\phi; S) \leq \delta$ 时，任何状态估计算法有：
   $$P(\hat{S} \neq S) \geq \frac{H(S) - \delta - \log 2}{\log K}$$

2. **数据处理不等式 (DPI)**: 用于 Theorem 2 证明 Step 3——马尔可夫链 $\phi(X) \to \hat{S} \to \hat{z}$ 意味着 TV 不会增加。

3. **Pinsker 不等式**: 将互信息界 $\delta = I(\phi; S)$ 转换为总变差界 $\text{TV} \leq \sqrt{\delta/2}$。

4. **KL 收缩**: 在正确模型下，后验收敛 $D_{\text{KL}}(P^* \| P_t) \xrightarrow{a.s.} 0$。

**参考文献**:
- Fano (1961)
- Cover & Thomas (2006)
- Pinsker (1964). *Information and Information Stability of Random Variables and Processes*

### 1.7 Minimax 理论

**根源**: Le Cam, L. (1973). "Convergence of estimates under dimensionality restrictions." *Annals of Statistics*, 1(1), 38-53.

**Spring 中的角色**:

1. **Le Cam 两点法**: 构造两个难以区分的分布 $P_0 = \text{Bern}(\mu_s)^{\otimes M}$（清洁）和 $P_1 = \text{Bern}(1 - C_{\text{bal}}\mu_s/(K-1))^{\otimes M}$（噪声），利用 Hellinger tensorization 获得 minimax 下界。

2. **Neyman-Pearson 归约**: 通过 Neyman-Pearson 引理将任意算法归约为 Bayes 检验，给出 Theorem 4' 的最优性。

3. **Hellinger 精确张量化**: 在 A2（条件独立）下，$H^2(P_0^{\otimes M}, P_1^{\otimes M}) = 1 - (1 - H^2(P_0, P_1))^M$——精确等式，无不等式松弛。

**参考文献**:
- Le Cam (1973)
- Le Cam (1986). *Asymptotic Methods in Statistical Decision Theory*
- Tsybakov (2009). *Introduction to Nonparametric Estimation*

---

## 2. 关键思想与证明工具

### 2.1 双时间尺度分离 ($\beta_t = o(\alpha_t)$)

Spring 最关键的架构创新。条件 C6' 要求 gatekeeper 更新速率 $\beta_t$ 是学生更新速率 $\alpha_t$ 的低阶无穷小：

$$\beta_t = o(\alpha_t), \quad \text{即} \quad \lim_{t\to\infty} \frac{\beta_t}{\alpha_t} = 0$$

**目的**: 在任意两次 gatekeeper 更新之间，学生执行渐近无限多次梯度步骤，在分布偏移前收敛到当前分布的局部最小值。

**规范调度**: $\alpha_t = t^{-a}$，$\beta_t = t^{-b}$，其中 $\frac{1}{2} < a < 1 < b$。例如 $a = 0.6$，$b = 1.2$：
- $\sum \alpha_t = \infty$（学生探索），$\sum \alpha_t^2 < \infty$（噪声控制）
- $\sum \beta_t < \infty$（有限总分布偏移），$\sum \beta_t^2 < \infty$（方差控制）
- $\beta_t / \alpha_t = t^{-0.6} \to 0$（时间尺度分离）

### 2.2 参考集重放打破选择偏差

Spring 最深刻的证明工具。Theorem 12.2 证明：**没有参考集重放，Lyapunov 下降在渐近意义下是不可能的**——gatekeeper 可以通过只接受"简单"样本来降低表观损失，而不真正改进判别能力。

解决方案 (Theorem 12.5, 完整证明):
1. **学生侧**: 重要性采样权重 $w(x) = P_0(x) / P_{S_t}(x)$，使得有效训练分布为参考分布 $P_0$
2. **Gatekeeper 侧**: 在固定参考集 $M_0$ 上计算 SCXUpdate，消除对齐偏差
3. **代价**: 重要性权重方差膨胀因子 $W \leq 1/\varepsilon_{\text{explore}} < \infty$

### 2.3 Lipschitz-almost-everywhere 引理

解决了一个基本的数学障碍 (Lemma SE-1.0, B9 fix)：

**问题**: 共识得分 $C(x) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ 在阈值 $\tau$ 处不连续（指示函数跳跃）。

**解决**: 在条件 C5（条件 i.i.d. 采样）下，不连续集合具有概率测度零，因为：
$$\mathbb{P}(\exists m: \ell(f_m(X), Y) = \tau) \leq \sum_{m=1}^M \mathbb{P}(\ell(f_m(X), Y) = \tau) = 0$$
对于连续分布上的光滑函数 $\ell(f_m(x), y)$。期望不受零测集修改的影响，Lyapunov 分析保留有效。

### 2.4 贝叶斯后验更新作为 Gatekeeper 进化

Gatekeeper 的进化被解释为序贯贝叶斯更新：

$$P_{t+1}(S) \propto P_t(S) \cdot \prod_{(x,y) \in \mathcal{D}_{t+1}} S(x,y)^{a} (1 - S(x,y))^{1-a}$$

这产生了两个强大的理论性质：
1. **鞅性质**: $\mathbb{E}[S_{t+1} \mid \mathcal{F}_t] = S_t$（塔性质），由 Doob 定理保证 a.s. 收敛
2. **KL 收缩**: 在正确模型下，$D_{\text{KL}}(P^* \| P_t) \to 0$

### 2.5 Lyapunov 下降与重要性采样

Theorem 12.5 的完整证明结构证明了 $\mathbb{E}[\Delta\Psi_t \mid \mathcal{F}_t] \leq 0$：

$$\mathbb{E}[\Delta\Psi_t \mid \mathcal{F}_t] \leq -\alpha_t \|\nabla L_0(\theta_t)\|^2 - \beta_t \cdot 2\rho_{\text{ideal}} \cdot \|\Delta_t^{\text{ideal}}\|_{M_0} \cdot \|S_t - \hat{C}\|_{M_0} + O(\alpha_t^2 W + \beta_t^2)$$

四个项的分解：
- **(A) 学生改进**: $\Delta_{\text{student}}$，通过重要性采样消除 $D_{\text{static}}$ 间隙（**已证明**）
- **(B) Gatekeeper 改进**: $\Delta_{\text{gatekeeper}}$，通过在 $M_0$ 上计算 SCXUpdate 消除对齐偏差（**已证明**）
- **(C) 分布偏移**: $\Delta_{\text{selection}} = O(\beta_t) = o(\alpha_t)$，由双时间尺度控制（**已证明**）
- **(D) 交叉耦合**: $\Delta_{\text{cross}} = 0$，因参考集可分离性（**已证明**）

### 2.6 $O(t^{-a})$ 收敛率与 Polyak 平均

在强凸条件下，学生的收敛率为 $O(t^{-a})$，其中 $a \in (0.5, 1]$ 为学习率指数。

**Polyak-Ruppert 平均** ($\bar{\theta}_t = \frac{1}{t}\sum_{i=1}^t \theta_i$) 将速率提升至 $O(t^{-1})$——与 minimax 下界 $\Omega(t^{-1})$ 匹配的最优速率——适用于任何 $a \in (0.5, 1)$ 且无需精确调谐。

### 2.7 四种失效模式刻画

Spring 系统性地刻画了四种规范失效模式：

| 模式 | 机制 | 严重性 |
|------|------|--------|
| **1. 过早冻结** | $\beta_t$ 在学生提供纠正信号之前衰减过快 | 中等（双精度下罕见） |
| **2. 积压** | 数据进入速率超过 gatekeeper 评分吞吐量 | 高（大数据集下实际存在） |
| **3. 客户端分歧** | 多个不动点 + 不同初始条件/数据流 → 不可调和的分歧 | 中等（仅多客户端部署） |
| **4. 对抗投毒** | 对手注入精心构造的样本；自进化循环放大污染 | 高（有放大效应时严重） |

每种模式配有形式化条件、退化速率和缓解策略。

---

## 3. 历史发展时间线

```
1892 ─ Lyapunov 稳定性理论
      A. M. Lyapunov, The General Problem of the Stability of Motion
      动力系统定性分析的基础——不动点、吸引子、Lyapunov 函数
      ↓ Spring 使用: Ψ(S_t, θ_t) 为 Lyapunov 函数；不动点分析；吸引子盆地
      
1933 ─ Kolmogorov 强大数定律
      A. N. Kolmogorov, Grundbegriffe der Wahrscheinlichkeitsrechnung
      独立同分布序列的几乎必然收敛基础
      ↓ Spring 使用: 共识统计量 C(x) 的大样本行为
      
1951 ─ Robbins-Monro 随机逼近
      H. Robbins & S. Monro, "A stochastic approximation method"
      随机梯度下降的数学基础；∑α_t=∞, ∑α_t²<∞ 条件
      ↓ Spring 使用: θ_t 更新遵循 RM 递归；双时间尺度扩展
      
1952 ─ Chernoff 信息
      H. Chernoff, "A measure of asymptotic efficiency for tests"
      假设检验的最优指数速率
      ↓ Spring 使用: Theorem 4' 检测的精确指数速率

1953 ─ Doob 鞅收敛
      J. L. Doob, Stochastic Processes
      有界鞅的几乎必然收敛
      ↓ Spring 使用: S_t 为 [0,1]-有界鞅 → S_t → S_∞ a.s.

1960 ─ Bahadur-Rao 精确渐近
      R. R. Bahadur & R. R. Rao, "On deviations of the sample mean"
      样本均值尾概率的精确二阶渐近（含格子修正）
      ↓ Spring 使用: Theorem 4' 的精确常数；Bernoulli 格子修正
      
1961 ─ Fano 不等式
      R. M. Fano, Transmission of Information
      信息论下界——互信息与错误概率的关系
      ↓ Spring 使用: Theorem 2 弱特征下界
      
1963 ─ Hoeffding 不等式
      W. Hoeffding, "Probability inequalities for sums of bounded random variables"
      有界独立变量和的指数集中
      ↓ Spring 使用: 共识分数的集中界；Theorem 1 的主工具
      
1964 ─ Pinsker 不等式
      M. S. Pinsker, Information and Information Stability
      TV ≤ √(KL/2) —— 信息散度与统计距离的桥梁
      ↓ Spring 使用: Theorem 2 中 δ → TV 的转换
      
1973 ─ Le Cam Minimax
      L. Le Cam, "Convergence of estimates under dimensionality restrictions"
      两点法下界、凸包论证、minimax 最优性框架
      ↓ Spring 使用: Theorem 4' 下界；Hellinger tensorization
      
1981 ─ Pollard k-means 一致性
      D. Pollard, "Strong consistency of k-means clustering"
      k-means 的几乎必然一致性
      ↓ Spring 使用: Theorem 5 状态发现的理论基础

1985 ─ QWERTY 锁定 (David)
      P. A. David, "Clio and the Economics of QWERTY"
      路径依赖与次优技术锁定的经济学理论
      ↓ 概念类比: Spring 的多不动点结构——gatekeeper 可能锁定于次优自洽配置
      
1989 ─ 递增回报 (Arthur)
      W. B. Arthur, "Competing technologies, increasing returns, and lock-in by historical events"
      正反馈循环中的多重均衡
      ↓ 概念类比: Spring gatekeeper 的选择偏差循环——初始偏差通过自进化被放大

2003 ─ 在线凸规划 (Zinkevich)
      M. Zinkevich, "Online convex programming and generalized infinitesimal gradient ascent"
      在线梯度下降的遗憾界 O(√T)
      ↓ Spring 使用: gatekeeper OGD 更新、延迟反馈扩展、增长记忆库扩展

2010 ─ 领域自适应理论
      Ben-David et al., "A theory of learning from different domains"
      训练与测试分布不匹配的泛化界
      ↓ Spring 使用: D_static 间隙的领域自适应界 (Lemma 12.1)

2017 ─ AlphaZero 自我博弈
      D. Silver et al., "Mastering Chess and Shogi by Self-Play..."
      通过自我博弈实现超人类水平、策略迭代、蒙特卡洛树搜索
      ↓ Spring 类似: 自进化循环结构、单调改进保证、记忆重放
      ↓ Spring 不同: 处理真实物理数据（非合成）、未知环境动态、形式收敛证明

2026 ─ Spring 自进化 Gatekeeper (本工作)
      SCX Research Group, "Spring: A Self-Evolving Gatekeeper with Provable Convergence"
      自进化评估标准（不仅自改进策略）、单调增长记忆、
      复活机制——"冬天不杀，它等待春天"
```

---

## 4. Spring 与前人的对比表

### 4.1 核心对比

| 算法 / 框架 | 年份 | 自进化? | 收敛证明? | 记忆? | 领域 |
|-------------|------|---------|-----------|-------|------|
| **Robbins-Monro** | 1951 | 否 | 是（渐近 a.s.） | 否 | 通用随机逼近 |
| **Hedge / 专家建议** | 1997 | 否 | 是（遗憾 O(√T)） | 否 | 在线决策 |
| **主动学习** | 2009 | 否（固定查询策略） | 是（标签复杂度） | 标注池 | 分类（单模型） |
| **贝叶斯优化** | 2016 | 否（固定先验） | 是（遗憾） | GP 后验 | 黑箱优化 |
| **AlphaZero** | 2017 | 是（自我博弈） | 否（经验性）* | 重放缓冲（有替换） | 游戏（已知环境） |
| **Solomonoff 归纳** | 1964 | N/A（理论极限） | 是（对可计算环境） | 全部历史 | 通用归纳（不可计算） |
| **Spring (Cercis)** | 2026 | **是**（gatekeeper 协同进化） | **是**（Theorem SE-1/2, Theorem 12.5） | **是**（M_t 单调增长，无删除） | **任意**（设计用于物理科学） |

*AlphaZero 在表格情况下有策略迭代的收敛证明；对神经网络情况为经验性。

### 4.2 Spring vs AlphaZero 详细对比

| 维度 | AlphaZero | Spring |
|------|-----------|--------|
| **数据生成** | 合成（自我博弈）——环境完全已知 | 真实（NEP 模拟）——物理规律未知 |
| **反馈** | 即时（游戏结局） | 延迟（NEP 批处理训练） |
| **收敛机制** | 策略迭代 + MCTS | Lyapunov 下降 + 贝叶斯更新 |
| **记忆** | 重放缓冲（有替换） | 单调增长记忆库（不删除） |
| **收敛保证** | 单调改进（表格情况已证明） | 有限时间不动点（Theorem SE-2, 已证明） |
| **最终状态** | 原则上最优策略 | 自洽不动点（可能次优） |
| **探索** | Dirichlet 噪声 + 访问计数 | 随机探索分数 ε + 退火接受阈值 |

### 4.3 Spring vs 贝叶斯优化

| 维度 | 贝叶斯优化 | Spring |
|------|-----------|--------|
| **目标** | 优化静态黑箱函数 | 进化评估标准 + 优化模型 |
| **替代模型** | 高斯过程 | NEP 学生（神经网络） |
| **采集函数** | EI / UCB / Thompson | 状态值函数 V(s) = R̂(s)·ρ(s)·(1-C(s)) |
| **粒度** | 逐点 | 逐状态（聚合多个样本） |
| **目标数量** | 单目标（通常） | 多目标（噪声检测、专家分歧、数据多样性） |
| **成本结构** | 同质 | 异质（DFT 计算成本因状态而异） |
| **收敛速率** | O(√(T·γ_T))（累积遗憾） | O(t^{-a}) + 有限时间终止保证 |

### 4.4 Spring vs 主动学习

| 维度 | 主动学习 | Spring |
|------|---------|--------|
| **查询策略** | 不确定性 / QBC / 期望模型变化 | 状态认证——在状态级聚合后决策 |
| **模型** | 单一判别模型 | 多专家集成 + 学生模型 |
| **查询决策** | 逐点 | 分层——先状态级，再样本级 |
| **噪声处理** | Oracle 假设清洁（多数） | **主要设计目标**——明确检测标签噪声 |
| **标签复杂度** | O(θ·d·log(1/ε)) | O(K_S·(1/Δ_min²)·log(1/ε)) |
| **认证** | 无 | 每个行动由状态级保证认证 |

---

## 5. Spring 独有的贡献

以下是 Spring 完成而**没有任何前人工作同时完成**的事情：

### 5.1 自进化评估标准（不仅自改进策略）

**前人限制**: AlphaZero 自改进其策略（如何下棋），但评估标准（游戏规则）是固定的外部真理。主动学习和贝叶斯优化有固定查询策略/采集函数。

**Spring 的创新**: Gatekeeper $S_t$ **自身**是学习对象——它定义"什么是好的数据"。系统不是在固定评估标准下优化策略，而是**同时进化评估标准本身**。这是一个二阶学习问题：学习如何学习判断数据质量。

### 5.2 单调增长记忆（不替换重放）

**前人限制**: 所有重放缓冲方案（AlphaZero、DQN、经验重放）在某种程度上替换旧记忆——缓冲有界，最旧/最不有用的样本被丢弃。

**Spring 的创新**: $M_t \subseteq M_{t+1}$——记忆仅增长。无删除策略意味着：
1. 无灾难性遗忘——早期学习的结构永不被丢弃
2. 记忆单调性提供自由的结构性质（Lemma SE-1.2 需要）
3. 复活机制成为可能——分数低于阈值的旧结构保留在记忆库中，等待 gatekeeper 成熟时重新评分

### 5.3 复活机制

**前人限制**: 无前人算法包含"复活"的概念。被拒绝的样本要么被丢弃（主动学习），要么不被重访。

**Spring 的创新**: "冬天不杀——它等待春天"。低于阈值 $\tau_{\text{keep}}$ 的结构不被删除——它们进入休眠。当 gatekeeper 在后续迭代中进化（$S_{t+1}$ 可能对相同结构给出更高分数）时，休眠结构被复活并引入训练：

```python
for (x, y, old_score) in M_t where old_score < τ_keep:
    new_score = S_{t+1}(x, y)
    if new_score >= τ_keep:
        RESURRECT(x, y)  # 春天使其复活
```

这在数学上编码为：gatekeeper 更新可以在任何时间将样本的评分推过阈值，变拒绝为接受——这在主动学习（一旦拒绝即永久丢弃）或贝叶斯优化（一旦评估即消耗预算）中是不可能的。

### 5.4 耦合动力系统分析（gatekeeper + 学生协同进化）

**前人限制**: Robbins-Monro 分析单一递归。AlphaZero 的策略迭代交替固定一个组件更新另一个（策略评估与策略改进之间无耦合动力系统分析）。

**Spring 的创新**: 完整的耦合动力系统形式化：
- 状态空间 $\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta$（乘积空间）
- 更新算子 $\Phi = (\Phi_S, \Phi_M, \Phi_\theta)$（因果前馈结构，块三角 Jacobian）
- 双时间尺度 ODE 分析（快慢方程组）
- Lyapunov 函数在乘积空间上的显式下降
- $\omega$-极限集、吸引子盆地、相图

没有前人算法在形式耦合动力系统框架中分析两个学习组件的协同进化。

### 5.5 精确收敛速率与 Polyak 平均

**前人限制**: 贝叶斯优化给出累积遗憾界 $O(\sqrt{T \cdot \gamma_T})$ 但不给出参数收敛速率。主动学习给出标签复杂度但不给出学习速率。

**Spring 的创新**:
- 强凸下学生速率为 $O(t^{-a})$（Theorem 11.1, 已证明）
- 收缩下 gatekeeper 速率为 $O(t^{-b})$（Theorem 11.2, 已证明）
- Polyak-Ruppert 平均将速率提升至 $O(t^{-1})$——匹配 minimax 下界 $\Omega(t^{-1})$
- 耦合速率由学生瓶颈 $O(t^{-a})$ 主导（Theorem 11.3）
- 有限时间（非渐近）界含显式常数（Theorem 11.6, 已证明）

### 5.6 形式化选择偏差循环分析

**前人限制**: 无前人算法形式化分析其自身数据选择程序创建自强化偏差循环的机制。

**Spring 的创新**: Theorem 12.2 证明——**在没有参考集重放的情况下，Lyapunov 下降在渐近意义下是不可能的**——gatekeeper 可以通过只接受"简单"样本来降低其表观损失，而不真正改进。这是对任何自选择学习系统的深刻限制，在 Spring 之前未被形式化证明。

具体来说，选择偏差循环：

$$\text{Gatekeeper } S_t \xrightarrow{\text{选择}} \text{Memory } M_{t+1} \xrightarrow{\text{训练}} \text{NEP } f_{\theta_{t+1}} \xrightarrow{\text{反馈}} \text{Gatekeeper } S_{t+1}$$

被分解、量化并证明为 Lyapunov 下降的必要阻碍——然后通过参考集重放 + 重要性采样的联合机制被解决（Theorem 12.5, 完整证明）。

---

## 总结

Spring 自进化算法在七个经典数学领域的交汇处运作：随机逼近、动力系统、贝叶斯推断、在线学习、集中不等式、信息论和 minimax 理论。其核心架构创新——双时间尺度分离、参考集重放打破选择偏差、单调增长记忆、复活机制、耦合动力系统分析——由这些领域的完整证明链支撑。与所有前人的决定性区别在于：Spring **同时**自进化其评估标准和被评估模型，形式化证明收敛，并保持单调增长的记忆（永不遗忘）。

---

*本谱系学由 SCX 理论组编制, 2026-06-28*
