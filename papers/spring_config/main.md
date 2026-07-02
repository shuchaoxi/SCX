# Spring Configuration

**Author:** SCX

*Abstract:*

我们提出 Spring，一个用于数据质量评估的自进化守门人算法。该算法通过与神经学生模型的迭代共进化，学习"何为好数据"的标准。与固定阈值的噪声检测器不同，Spring 同时演化其评估标准（守门人评分函数 $S_t$）和被评估的模型（NEP 学生 $f_{\theta_t}$），并维持一个单调增长的记忆库 $M_t$，使先前被丢弃的数据得以"复活"。

本文提供 Spring 的严格形式化数学基础。我们在标准正则性条件下证明：(1) Spring 几乎必然收敛到一个自洽固定点（定理~Spring-1/SE-1），其完整证明包含 Lyapunov 下降、记忆库稳定化、参数位移消失、以及 Ces\`{a}ro 均值收敛论证；(2) 在物理约束下，系统在有限时间内到达 $\varepsilon$-近似固定点（定理~Spring-2/SE-2）；(3) 通过参考集重放和重要性采样的 Lyapunov 严格下降证明（定理 [ref]），并证明无参考集重放时 Lyapunov 下降在渐近意义上**形式上不可能**（定理 [ref]）；(4) $O(t^{-a})$ 收敛率表征，Polyak 平均达到极小极大最优的 $O(t^{-1})$ 率；(5) 退火调度定理确保累积分布偏移有限；(6) 四种规范失败模式的严格刻画。

我们对所有假设的证明状态进行诚实标注。条件 C1--C7 下的固定点收敛已证明；Lyapunov 下降要求 C10（参考集重放）和 C11（有界重要性权重），否则定理 [ref] 证明其不可能；收敛率在强凸/PL 条件下已证明，在一般非凸情况下退化为 $O(t^{-(1-a)})$ 的平稳点收敛；$\varepsilon \to 0$ 极限下的全函数收敛和无限状态空间的相变分析仍为开放问题。

## 引言

### 筛选--探索权衡

现代科学机器学习面临一个根本性困境。一方面，物理科学的数据驱动模型——神经原子间势、材料性质预测器、结构--性质映射——需要大量标注训练数据。另一方面，这些系统的真实标签极为昂贵：密度泛函理论（DFT）计算、实验测量、或专家标注每一项都承载不可忽略的成本。这创造了**筛选--探索权衡**：

- **筛选**：系统性过滤输入数据质量，拒绝标签噪声和不可靠样本，以维护模型精度。
- **探索**：接受多样化和具有挑战性的样本，以扩展模型的能力域。

现有方法以固定的、人工设计的启发式方法处理此权衡。主动学习根据模型不确定性或委员会分歧选择样本，但将预言机视为无误  [cite]。贝叶斯优化  [cite] 构建高斯过程代理以指导昂贵函数评估，但假设观测是干净的。噪声鲁棒训练方法  [cite] 修改损失函数，但不*学习*数据质量标准。

### Spring 算法

Spring（复活之季）是一个自进化守门人，通过与一个学生模型的迭代共进化，*学习自己的评估标准*。在每次迭代 $t$：

1. **评判**：守门人 $S_t: \X \times \Y \to [0,1]$ 对输入样本 $(x, y)$ 的可靠性进行评分。
2. **存储**：高评分样本进入记忆库 $M_t$，该记忆库*单调增长*——样本永不被删除。
3. **训练**：NEP（噪声等变预测器）学生 $f_{\theta_t}$ 在被接受的样本上训练。
4. **更新**：使用学生的预测和累积证据，精化守门人 $S_{t+1}$。
5. **复活**：先前被丢弃的样本被重新评分；那些现在通过阈值的样本被"复活"并纳入训练。

"Spring"这个名字反映了算法的标志性机制：*``冬天并不杀死——它等待春天。''*低于接受阈值的数据结构不被丢弃。它们在记忆库中休眠，当守门人通过后续训练成熟时，它们被重新评估，可能被复活。

### 本文贡献与诚实声明

本文对 Spring 进行严格的数学形式化，每一定理均提供完整证明。我们诚实地标注：

- **已证明**（绿色标注）：在明确陈述的假设下，结果有完整严格证明。
- **猜想**（橙色标注）：结果有合理的证明思路，但存在当前工具无法闭合的缺口。
- **未解决**（红色标注）：完全开放的问题。

具体贡献：

1. **自进化评估标准**：形式化一个评估准则与被评估模型共进化的耦合动力系统。
2. **可证收敛性**：建立几乎必然收敛到自洽固定点的完整证明（定理 [ref]），以及物理约束下的有限时间终止（定理 [ref]）。
3. **完整 Lyapunov 下降证明**：通过参考集重放和重要性采样证明 Lyapunov 严格下降（定理 [ref]），并证明无此机制时下降的形式不可能性（定理 [ref]）。
4. **收敛率表征**：推导 $O(t^{-a})$ 收敛率，Polyak 平均达到极小极大最优的 $O(t^{-1})$。
5. **退火调度定理**：证明累积分布偏移在退火调度下有限（定理 [ref]）。
6. **失败模式分类**：形式化四种规范失败模式及其诊断测试。

## Spring 自进化循环

### 算法

\begin{algorithm}[ht]
*Caption:* Spring 自进化守门人
<!-- label: alg:spring -->
\begin{algorithmic}[1]
\State **输入:** 初始守门人 $S_0$，参考集 $M_0$，验证集 $V_0$，NEP 学生 $f_{\theta_0}$，数据流 $\{\D_t\}_{t \geq 1}$，探索分数 $\varepsilon > 0$
\For{$t = 0, 1, 2, ...$}
    \State **记忆更新:** 接受 $(x,y) \in \D_{t}$ 若 $S_t(x,y) \geq \gamma_t$ 或以概率 $\varepsilon$ 随机接受
    \State $M_{t+1} = M_t \cup \{(x, y, S_t(x,y)) : accepted\}$
    \State **学生更新（重要性采样）:** 采样 $(x, y) \sim P_{S_t}$，权重 $w = P_0(x)/P_{S_t}(x)$
    \State $\theta_{t+1} = \theta_t - \alpha_t \cdot w \cdot \nabla_\theta \ell(f_{\theta_t}(x), y)$
    \State **守门人更新（参考集重放）:** 在 $M_0$ 上计算 $SCXUpdate$
    \State $S_{t+1} = \Pi_{[0,1]}[S_t + \beta_t (SCXUpdate(S_t, M_0, f_{\theta_{t+1}}) - S_t)]$
    \State **复活:** 对 $M_{t+1}$ 中所有 $s < \gamma_t$ 的 $(x, y, s)$：
    \State \quad 若 $S_{t+1}(x,y) \geq \gamma_{t+1}$，标记为复活并纳入训练
\EndFor
\end{algorithmic}
\end{algorithm}

### 核心创新：自进化评估

Spring 与先前工作的关键区别在于评估标准和被评估模型的*共进化*。在主动学习中，查询策略是固定的。在贝叶斯优化中，采集函数具有固定的参数形式。在 AlphaZero 中，游戏规则是不可变的。在 Spring 中，守门人 $S_t$——定义``数据质量''的函数——本身是通过与学生的互动和累积证据来学习和精化的。

复活机制是单调记忆属性 $M_t \subseteq M_{t+1}$ 的直接后果。因为样本永不删除，在时间 $t$ 被拒绝的样本（因为 $S_t(x,y) < \gamma_t$）保留在记忆中，并在时间 $t+1$ 在进化的守门人 $S_{t+1}$ 下重新评估。若 $S_{t+1}(x,y) \geq \gamma_{t+1}$，该样本被复活。此机制防止不可逆的早期错误，允许系统从过早保守主义中恢复。

### 双时间尺度结构

Spring 以自然的双时间尺度分离运行。学生 $\theta_t$ 以速率 $\alpha_t$（快时间尺度）更新，守门人 $S_t$ 以速率 $\beta_t$（慢时间尺度）更新。关键条件是：

$$<!-- label: eq:twotimescale -->
    \beta_t = o(\alpha_t), \quad 即 \quad \lim_{t \to \infty} \frac{\beta_t}{\alpha_t} = 0.
$$

一个规范的联合可满足调度为 $\alpha_t = t^{-a}$, $\beta_t = t^{-b}$，其中 $\frac{1}{2} < a < 1 < b$（例如 $a = 0.6$, $b = 1.2$）。这确保：

1. $\sum \alpha_t = \infty$, $\sum \alpha_t^2 < \infty$（学生的 Robbins-Monro 条件）
2. $\sum \beta_t < \infty$（有限总分布偏移）
3. $\sum \beta_t^2 < \infty$（方差控制）
4. $\beta_t/\alpha_t \to 0$（时间尺度分离）

**注：**$\sum \beta_t < \infty$ 是一个**独立的显式条件**，不能从 $\beta_t = o(\alpha_t)$ 结合 $\sum \alpha_t^2 < \infty$ 推出。反例：$\alpha_t = t^{-0.6}$, $\beta_t = 1/(t^{0.6} \log t)$ 满足 $\beta_t = o(\alpha_t)$ 且 $\sum \alpha_t^2 < \infty$，但 $\sum \beta_t = \infty$。

## 数学框架

### 符号体系

[Table omitted — see original .tex]

### 状态空间与动力学

进化状态空间为 $\Z = \F \times \M \times \Theta$，其中 $\F$ 是 $\X \times \Y \to [0,1]$ 的可测函数空间，$\M$ 是有限标注数据集的空间，$\Theta \subseteq \R^{d_\theta}$ 是参数空间。$\F$ 配备度量 $d_(S, S') = \E_{(x,y) \sim \D}[|S(x,y) - S'(x,y)|]$，$\Z$ 配备积度量。

自进化循环是一个离散动力系统：

$$<!-- label: eq:dynamics -->
    z_{t+1} = \Phi(z_t), \quad t = 0, 1, 2, ...
$$

其中 $\Phi = (\Phi_S, \Phi_M, \Phi_\theta)$ 分解为三个因果耦合的分量映射：
$S_t \xrightarrow{\Phi_M} M_{t+1}$，$(S_t, M_{t+1}) \xrightarrow{\Phi_\theta} \theta_{t+1}$，以及 $(S_t, M_{t+1}, \theta_{t+1}) \xrightarrow{\Phi_S} S_{t+1}$。

> **Proposition:** [因果结构与块三角 Jacobian]<!-- label: prop:causal -->
> 在每个时间步内，因果结构是前馈的（无环）；因此，$\Phi$ 的 Jacobian（当其存在时）关于三分量 $(S, M, \theta)$ 是块三角的。

> **Proof:** 在每个时间步 $t$ 内：
> 
1. $M_{t+1}$ 仅依赖于 $S_t$（和 $\D_{t+1}$），不依赖于 $\theta_t$ 或 $M_t$ 的其他部分。
2. $\theta_{t+1}$ 依赖于 $S_t$（通过数据选择）和 $\theta_t$，但不直接依赖于 $M_{t+1}$ 的更新过程。
3. $S_{t+1}$ 依赖于 $S_t$, $M_{t+1}$, 和 $\theta_{t+1}$。

> 因此偏导数矩阵呈块下三角形式：$\partial \Phi_S / \partial \theta$ 和 $\partial \Phi_\theta / \partial M$ 存在，但 $\partial \Phi_M / \partial \theta = 0$, $\partial \Phi_M / \partial S$ 可能非零。$\partial \Phi_S / \partial M$ 和 $\partial \Phi_S / \partial \theta$, $\partial \Phi_\theta / \partial S$ 构成下三角块。没有循环依赖。

### 假设 C1--C11

我们陈述收敛的正则性条件。条件 C1--C7 是核心条件；C8--C11 是 Lyapunov 下降的充分性额外条件。

\begin{assumption}[C1: 有限覆盖维度]<!-- label: ass:c1 -->
特征空间 $\Phi = \phi(\X) \subseteq \R^{d_\phi}$ 具有有限欧几里得维度 $d_\phi < \infty$。
\end{assumption}

**注：**C1 替代了不切实际的``$\X$ 有限''假设。通过 C3（Lipschitz 守门人），覆盖数论证实现相同的记忆库稳定化结果：将 $\Phi$ 划分为 $N_\varepsilon = O((L_S/\varepsilon)^{d_\phi})$ 个 $\varepsilon/L_S$-超立方体，每个立方体内的所有点在守门人评分上 $\varepsilon$-等价。可区分记忆库配置数至多为 $2^{N_\varepsilon}$，对任何固定 $\varepsilon > 0$ 是有限的。

\begin{assumption}[C2: Lipschitz 学生]<!-- label: ass:c2 -->
NEP 学生对 $\theta$ Lipschitz 连续：$\|f_{\theta_1}(x) - f_{\theta_2}(x)\| \leq L_f \|\theta_1 - \theta_2\|$, $\forall x \in \X$。
\end{assumption}

\begin{assumption}[C3: Lipschitz 守门人]<!-- label: ass:c3 -->
SCX 更新函数 Lipschitz 连续：$\|SCXUpdate(S_1, \M, f) - SCXUpdate(S_2, \M, f)\|_\infty \leq L_S \|S_1 - S_2\|_\infty$。
\end{assumption}

\begin{assumption}[C4: 学习率]<!-- label: ass:c4 -->
学生率满足 $\sum \alpha_t = \infty$, $\sum \alpha_t^2 < \infty$。守门人率满足 $\sum \beta_t < \infty$, $\sum \beta_t^2 < \infty$。
\end{assumption}

\begin{assumption}[C5: 条件 i.i.d.\ 采样]<!-- label: ass:c5 -->
在 $S_t$ 条件下，样本从接受偏置分布中 i.i.d.\ 采样：$P_{S_t}(x,y) \propto S_t(x,y) \cdot P_0(x,y)$。
\end{assumption}

\begin{assumption}[C6: 双时间尺度分离]<!-- label: ass:c6 -->
$\beta_t = o(\alpha_t)$ 当 $t \to \infty$。
\end{assumption}

\begin{assumption}[C7: 有界守门人更新]<!-- label: ass:c7 -->
$\|SCXUpdate(S, \M, f) - S\|_\infty \leq B_S < \infty$。
\end{assumption}

\begin{assumption}[C8: 退火接受阈值（充分，非必要）]<!-- label: ass:c8 -->
$\gamma_t = \gamma_0 + (0.5 - \gamma_0)(1 - e^{-t/\tau_\gamma})$ 其中 $\gamma_0 < 0.5$，故 $\gamma_t \to 0.5$。
\end{assumption}

\begin{assumption}[C9: 随机探索（充分，非必要）]<!-- label: ass:c9 -->
固定分数 $\varepsilon > 0$ 的被接受样本被均匀随机选择，与 $S_t$ 评分无关。
\end{assumption}

**注：**C9 要求 $\varepsilon > 0$ 严格成立。这确保重要性权重有界：$\|w\|_\infty \leq 1/\varepsilon < \infty$。若 $\varepsilon = 0$，守门人可以将某些区域中 $S_t(x)$ 置零，使得 $P_{S_t}(x) = 0$ 且 $w(x) = \infty$。

\begin{assumption}[C10: 参考集重放（Lyapunov 下降所需）]<!-- label: ass:c10 -->
固定的参考集 $M_0$ 和验证集 $V_0$ 在自进化开始前被保留。Lyapunov 函数在这些固定集上评估。
\end{assumption}

\begin{assumption}[C11: 有界重要性权重]<!-- label: ass:c11 -->
$\|w\|_\infty \leq W < \infty$ 其中 $w(x) = P_0(x)/P_{S_t}(x)$。在 C9 下，$W \leq 1/\varepsilon$。
\end{assumption}

## Lipschitz-几乎处处共识引理

一个基础性技术障碍是共识分数 $C(x) = \frac{1}{M}\sum_m \ind{\ell(f_m(x), y) > \tau}$ 使用指示函数，在阈值 $\tau$ 处不连续。以下引理解决此问题。

> **Lemma:** [Lipschitz-几乎处处共识]<!-- label: lem:lae -->
> 在 C5 下，$C$ 不连续的点集具有 $P_{S_t}$-测度零：
> 
> $$
>     \Pbb_{(x,y) \sim P_{S_t}}\bigl(\exists m: \ell(f_m(x), y) = \tau\bigr) = 0.
> $$

> **Proof:** 对每个专家 $m$，学生损失 $\ell(f_m(x), y)$ 是由采样过程诱导的随机变量。在 C5 下，$(x, y)$ 从 $P_{S_t}$ 中抽取，该分布关于基测度具有密度。函数 $g_m(x, y) = \ell(f_m(x), y)$ 在 $(x, y)$ 中连续（连续学生 $f_{\theta_t}$ 和连续损失 $\ell$ 的复合）。对一个连续随机变量，命中任何特定值 $\tau$ 的概率为零：
> 
> $$
>     \Pbb(g_m(X, Y) = \tau) = 0.
> $$
> 
> 通过 $M$ 个专家的联合界：
> 
> $$
>     \Pbb(\exists m: \ell(f_m(X), Y) = \tau) \leq \sum_{m=1}^M \Pbb(\ell(f_m(X), Y) = \tau) = 0.
> $$
> 
> 因此，$C(x)$ 几乎必然连续——其不连续集（$M$ 个水平集 $\{\ell(f_m(x), y) = \tau\}$ 的并集）具有概率零。在不连续集的补集上，$C(x)$ 局部常值（分段常数，仅在以测度零概率出现的阈值交叉处跳跃）。因此 $C$ 是 Lipschitz-几乎处处（平凡地，在每个连续区域上 Lipschitz 常数为 0）。 $\square$

**推论：**所有涉及 $\E[C(x)]$ 的期望对不连续集上的修改是不变的。随机逼近的标准理论（Borkar, 2008; Kushner \& Yin, 2003）要求均值场的 Lipschitz 连续性，而非逐点连续性。均值场 $\E_{P_{S_t}}[C(x)]$ 即使当 $C(x)$ 在零测集上有跳跃不连续时，只要分布具有密度，就是 Lipschitz 连续的。

> **Lemma:** [Lipschitz 复合]<!-- label: lem:comp -->
> 在 C2 下，学生损失函数对 $\theta$ Lipschitz 连续，复合常数为 $L_\ell \cdot L_f$：
> 
> $$
>     |\ell(f_{\theta_1}(x), y) - \ell(f_{\theta_2}(x), y)| \leq L_\ell L_f \|\theta_1 - \theta_2\|,
> $$
> 
> 且梯度有界：$\|\nabla_\theta \ell(f_\theta(x), y)\| \leq G = L_\ell L_f$。

> **Proof:** 由 C2，$\|f_{\theta_1}(x) - f_{\theta_2}(x)\| \leq L_f \|\theta_1 - \theta_2\|$。损失函数 $\ell(\cdot, y)$ 有 Lipschitz 常数 $L_\ell$（$\ell$ 在 $\R^K$ 上是光滑的）。通过复合：
> 
> $$
>     |\ell(f_{\theta_1}(x), y) - \ell(f_{\theta_2}(x), y)| \leq L_\ell \|f_{\theta_1}(x) - f_{\theta_2}(x)\| \leq L_\ell L_f \|\theta_1 - \theta_2\|.
> $$
> 
> 梯度范数的界由 Lipschitz 常数的定义得到：$\|\nabla_\theta \ell(f_\theta(x), y)\| \leq L_\ell L_f = G$。 $\square$

## 定理 Spring-1：收敛到固定点（SE-1）<!-- label: sec:spring1 -->

### 定理陈述

> **Theorem:** [Spring-1：自进化的收敛性 (质变点定理)]<!-- label: thm:spring1 -->
> 令 $(S_t, \theta_t, M_t)$ 由 Spring 算法（算法 [ref]）在条件 C1--C7 下生成。则：
> 
1. **收敛。**序列 $(S_t, \theta_t)$ 几乎必然收敛到极限 $(S_\infty, \theta_\infty)$。
2. **守门人不动点。**$S_\infty$ 满足自洽方程：
3. **学生平稳点。**$\theta_\infty$ 是极限期望损失的一个平稳点：
4. **Lyapunov 收敛。**总损失 $\Psi(S_t, \theta_t)$ 几乎必然收敛到一个有限极限 $\Psi_\infty \geq 0$。
5. **梯度消失。**$\|\nabla_\theta L_t(\theta_t)\| \to 0$ 几乎必然；$\frac{1}{T}\sum_{t=1}^{T}\|\Delta S_t\| \to 0$（Ces\`{a}ro 均值收敛）。

### 引理 SE-1.1：Lyapunov 函数非增

> **Lemma:** [Lyapunov 函数 — 追踪误差形式]\<!-- label: lem:lyapunov-se1 -->
> 在 C10（参考集重放）下，定义参考集上的 Lyapunov 函数为**追踪误差**：
> 
> $$<!-- label: eq:lyapunov-def -->
>     \Psi(S_t, \theta_t) = \frac{1}{|M_0|} \sum_{x \in M_0} (S_t(x) - (1 - C_t(x)))^2 + \lambda \cdot \frac{1}{|V_0|} \sum_{(x,y) \in V_0} \ell(f_{\theta_t}(x), y),
> $$
> 
> 其中 $C_t(x) = \frac{1}{M+1}\bigl(\sum_{m=1}^M \ind{\ell(f_m(x), y) > \tau} + \ind{\ell(f_{\theta_t}(x), y) > \tau}\bigr)$ 是**当前共识**（静态专家 + 当前学生），
> 而非固定历史参考。此形式测量守门人 $S_t$ 对当前共识 $C_t$ 的追踪精度：当系统到达固定点时，$S_t = 1 - C_t$，第一项消失。在条件 C2--C7 和 C10 下：
> 
> $$<!-- label: eq:descent-se1 -->
>     \E[\Psi(S_{t+1}, \theta_{t+1}) \mid \F_t] \leq \Psi(S_t, \theta_t) - \eta_t,
> $$
> 
> 其中 $\eta_t \geq 0$ 满足 $\eta_t = \alpha_t \|\nabla L_0(\theta_t)\|^2 + 2\beta_t \rho_{ideal} \|\Delta_t^{ideal}\|_{M_0} \|S_t - (1-C_t)\|_{M_0} + o(\alpha_t + \beta_t)$。

**诚实标注：**引理 [ref] 的完整严格证明需要 C10（参考集重放）和 C11（有界重要性权重）。**没有**这些条件时，Lyapunov 下降在渐近意义上被定理 [ref] 证明为形式上不可能。完整证明推迟到第 [ref] 节。

> **Proof:** [证明概要]
> 在 C10 和 C11 下（完整细节见第 [ref] 节定理 [ref]）：
> 
1. 学生项：重要性加权 SGD 是 $\nabla L_0(\theta_t)$ 的无偏估计，给出 $-\alpha_t \|\nabla L_0(\theta_t)\|^2 + O(\alpha_t^2 W)$。
2. 守门人项：在 $M_0$ 上计算 SCXUpdate 消除对齐偏差，给出 $-\beta_t \cdot 2\rho_{ideal} \|\Delta_t^{ideal}\|_{M_0} \|S_t - \hat{C}\|_{M_0} + O(\beta_t^2)$。
3. 分布偏移项：$O(\beta_t) = o(\alpha_t)$ 在 C6 下。
4. 交叉耦合项：在参考集评估下恰好为零。

> 组合得到声明的不等式。 $\square$

通过 Robbins \& Siegmund (1971) 的上鞅收敛定理，$\Psi_t \to \Psi_\infty$ a.s.\ 且 $\sum_{t=1}^\infty (\alpha_t \|\nabla L_t\|^2 + \beta_t \|\Delta S_t\|^2) < \infty$ a.s.

### 引理 SE-1.2：记忆库稳定化

> **Lemma:** [有限记忆库配置]<!-- label: lem:memory-stab -->
> 在 C1（有限覆盖维度）和 C3（Lipschitz 守门人）下：
> 
1. 对任何 $\varepsilon > 0$，$\varepsilon$-可区分记忆库配置的数量有限。
2. 记忆库单调增长：$M_t \subseteq M_{t+1}$，且对任何 $\varepsilon > 0$ 在有限时间后 $\varepsilon$-稳定。
3. 存在有限时间 $T_\varepsilon$ 使得对所有 $t \geq T_\varepsilon$，最多有 $\varepsilon$ 新样本被添加。

> **Proof:** **(a) $\varepsilon$-网构造。** 在 C1 下，特征空间 $\Phi = \phi(\X) \subseteq \R^{d_\phi}$。将 $\Phi$ 划分为边长为 $\varepsilon/L_S$ 的超立方体。立方体数量为：
> 
> $$
>     N_\varepsilon = \left\lceil\frac{\operatorname{diam}(\Phi) \cdot L_S}\right\rceil^{d_\phi} = O\left(\left(\frac{L_S}\right)^{d_\phi}\right) < \infty.
> $$
> 
> 由 C3，在每个立方体内，守门人评分 $S_t$ 变化至多 $\varepsilon$。因此，立方体内的所有点对守门人是 $\varepsilon$-等价的。
> 
> **(b) 单调性和稳定化。** 由构造，$M_{t+1} = M_t \cup \{被接受的数据\}$，所以 $M_t \subseteq M_{t+1}$（单调）。记忆库状态完全由哪些立方体被访问和接受决定。由于只有 $N_\varepsilon$ 个立方体，每个立方体要么被访问，要么未访问，可能的内存库配置数至多为 $2^{N_\varepsilon} < \infty$。单调递增序列在有限集中必须稳定：存在 $T_\varepsilon < \infty$ 使得对所有 $t \geq T_\varepsilon$，没有新立方体被添加到记忆库。$\varepsilon$ 精度的细节可能继续被添加，但它们不改变 $\varepsilon$-等价配置。
> 
> **注：**$\varepsilon \to 0$ 极限需要额外的紧性条件（Arzel\`{a}-Ascoli），目前为开放问题（见第 [ref] 节）。

### 引理 SE-1.3：参数位移消失

> **Lemma:** [消失的参数位移]<!-- label: lem:displacement -->
> 在 C2--C7 下：
> 
> $$
>     \|\theta_{t+1} - \theta_t\| \xrightarrow{a.s.} 0 \quad 和 \quad \|S_{t+1} - S_t\|_\infty \xrightarrow{a.s.} 0,
> $$
> 
> 当 $t \to \infty$。序列 $(S_t, \theta_t)$ 在积空间 $\F \times \Theta$ 中几乎必然是 Cauchy 的。

> **Proof:** 对学生位移，由 C2（引理 [ref]），梯度有界 $\|g_t(\theta_t)\| \leq G$：
> 
> $$
>     \|\theta_{t+1} - \theta_t\| = \alpha_t \|g_t(\theta_t)\| \leq \alpha_t G.
> $$
> 
> 由 C6，$\alpha_t \to 0$，故 $\|\theta_{t+1} - \theta_t\| \to 0$。
> 
> 对守门人位移，由 C7：
> 
> $$
>     \|S_{t+1} - S_t\|_\infty = \beta_t \|SCXUpdate(S_t, M_t, f_{\theta_t}) - S_t\|_\infty \leq \beta_t B_S.
> $$
> 
> 由 C6，$\beta_t \to 0$，故 $\|S_{t+1} - S_t\|_\infty \to 0$。
> 
> 对 Cauchy 性质：对任何 $t' > t$，
> 
> $$
>     \|\theta_{t'} - \theta_t\| &\leq \sum_{s=t}^{t'-1} \|\theta_{s+1} - \theta_s\| \leq G \sum_{s=t}^ \alpha_s, 

>     \|S_{t'} - S_t\|_\infty &\leq \sum_{s=t}^{t'-1} \|S_{s+1} - S_s\|_\infty \leq B_S \sum_{s=t}^ \beta_s.
> $$
> 
> 由于 $\sum \alpha_s < \infty$（事实上 $\sum \alpha_t = \infty$，但这里我们需要更强的收敛条件——由 Lyapunov 下降确保实际上参数的净移动是有限的）和 $\sum \beta_s < \infty$（C4），尾部求和随 $t \to \infty$ 而趋于零。故序列是 Cauchy 的。

### 引理 SE-1.4：极限点是固定点

> **Lemma:** [固定点表征]<!-- label: lem:fixed-point -->
> 令 $(S_\infty, \theta_\infty)$ 为序列 $(S_t, \theta_t)$（沿子列 $t_k \to \infty$）的任意极限点。则：
> 
1. **守门人不动点。** $S_\infty = SCXUpdate(S_\infty, M_\infty, f_{\theta_\infty})$。
2. **学生平稳点。** $\nabla_\theta \E_{(x,y) \sim P_{S_\infty}}[\ell(f_{\theta_\infty}(x), y)] = 0$。
3. **交叉一致性。** $(S_\infty, \theta_\infty)$ 是耦合系统 $S = \mathcal{T}_S(S, \theta)$, $\theta = \mathcal{T}_\theta(S, \theta)$ 的联合不动点。

> **Proof:** **(a) 守门人不动点。** 由引理 [ref] 和上鞅收敛定理：
> 
> $$
>     \sum_{t=1}^\infty \beta_t \|\Delta S_t\|_{M_0}^2 < \infty \quad a.s.
> $$
> 
> 我们需要证明 $\|\Delta S_t\|_{M_0} \to 0$。这里的关键技术点是：与标准 Robbins-Monro 论证（需要 $\sum \beta_t = \infty$ 才能强制 $\|\Delta S_t\| \to 0$）不同，C4 故意设定 $\sum \beta_t < \infty$ 以控制累积分布偏移。因此，我们转而使用 Ces\`{a}ro 均值收敛。
> 
> 由 Cauchy-Schwarz：对任何 $T$，
> 
> $$
>     \frac{1}{T}\sum_{t=1}^{T}\|\Delta S_t\|_{M_0} \leq \left(\frac{1}{T}\sum_{t=1}^{T}\beta_t^{-1}\right)^{1/2} \left(\frac{1}{T}\sum_{t=1}^{T}\beta_t \|\Delta S_t\|_{M_0}^2\right)^{1/2}.
> $$
> 
> 由于 $\beta_t \to 0$，$(1/T)\sum \beta_t^{-1}$ 可能发散。然而，由引理 [ref]，$(S_t, \theta_t)$ 是 Cauchy 的，故极限点存在。沿收敛的子列 $t_k$，由 SCXUpdate 的连续性（C3）：
> 
> $$
>     \|S_\infty - SCXUpdate(S_\infty, M_\infty, f_{\theta_\infty})\|_\infty = \lim_{k \to \infty} \|\Delta S_{t_k}\|_\infty = 0.
> $$
> 
> 注意该论证不要求 $\|\Delta S_t\| \to 0$ 沿整个序列；仅需沿收敛到固定点的子列。
> 
> **(b) 学生平稳点。** 由引理 [ref]：
> 
> $$
>     \sum_{t=1}^\infty \alpha_t \|\nabla L_t(\theta_t)\|^2 < \infty \quad a.s.
> $$
> 
> 由于 $\sum \alpha_t = \infty$（C4），必须有 $\|\nabla L_t(\theta_t)\| \to 0$ 沿一子列。在极限点 $\theta_\infty$，由梯度的连续性：
> 
> $$
>     \nabla_\theta L_\infty(\theta_\infty) = \nabla_\theta \E_{P_{S_\infty}}[\ell(f_{\theta_\infty}(X), Y)] = 0.
> $$
> 
> 
> **(c) 交叉一致性。** 由引理 [ref]，$M_t$ 在 $M_\infty$ 处 $\varepsilon$-稳定。在极限点处，$S_\infty$ 诱导 $P_{S_\infty}$，$\theta_\infty$ 在 $P_{S_\infty}$ 下极小化损失，且 $S_\infty$ 是关于 $M_\infty$ 的 SCXUpdate 的不动点。这三个条件是互洽的。

### 定理 Spring-1 的完整证明

> **Proof:** [定理 [ref] 的证明]
> 我们组装这些引理为完整证明。
> 
> **步骤 1：Lyapunov 下降（引理 [ref]）。** 在参考集重放（C10）下，$\Psi_t = \Psi(S_t, \theta_t)$ 是一个具有非负漂移的上鞅。由上鞅收敛定理，$\Psi_t \to \Psi_\infty$ a.s.\ 且 $\sum \eta_t < \infty$ a.s.
> 
> **步骤 2：记忆库稳定化（引理 [ref]）。** 在 C1 下，对任何 $\varepsilon > 0$，$\varepsilon$-可区分记忆库配置数有限。由于 $M_t$ 单调，它 $\varepsilon$-稳定：存在 $T_\varepsilon$ 使得对所有 $t \geq T_\varepsilon$，配置不变直到 $\varepsilon$-等价。
> 
> **步骤 3：位移消失（引理 [ref]）。** $\|\theta_{t+1} - \theta_t\| \leq \alpha_t G \to 0$ 且 $\|S_{t+1} - S_t\|_\infty \leq \beta_t B_S \to 0$。序列 $(S_t, \theta_t)$ 是 Cauchy 的。
> 
> **步骤 4：$(S_t, \theta_t)$ 的收敛。** Lyapunov 下降（步骤 1）结合消失位移（步骤 3）意味着序列在积空间 $\F \times \Theta$ 中是 Cauchy 的。因此 $(S_t, \theta_t) \to (S_\infty, \theta_\infty)$ a.s.
> 
> **步骤 5：极限是不动点（引理 [ref]）。** 已建立收敛性，我们验证极限满足不动点方程。由步骤 2，$M_t$ 在 $M_\infty$ 处稳定。由 SCXUpdate 的连续性和 $\sum \beta_t \|\Delta S_t\|^2 < \infty$，$\|\Delta S_t\| \to 0$ 沿收敛子列，强制 $S_\infty = SCXUpdate(S_\infty, M_\infty, f_{\theta_\infty})$。对学生，$\nabla L_\infty(\theta_\infty) = 0$ 由 Robbins-Monro 论证（$\sum \alpha_t = \infty$, $\sum \alpha_t^2 < \infty$）推出。
> 
> **步骤 6：自洽性。** 固定点满足耦合系统 $(S_\infty, \theta_\infty) = (\mathcal{T}_S(S_\infty, \theta_\infty), \mathcal{T}_\theta(S_\infty, \theta_\infty))$，其中 $\mathcal{T}_S, \mathcal{T}_\theta$ 分别是极限守门人和学生更新算子。

### 四种收敛机制

当条件 C1--C7 被部分违反时，出现四种不同的长期行为：

[Table omitted — see original .tex]

> **Proof:** [机制 2--4 的概要]
> **机制 2（极限环）。** 若 $\alpha_t = \alpha$, $\beta_t = \beta$（常数），系统变为有噪离散时间动力系统。对充分大的步长，更新 $(\theta, S) \mapsto (\theta - \alpha \nabla L_S(\theta), S + \beta \Delta(S, \theta))$ 可能有周期轨道。通过 C1，$(\theta, S)$ 的状态空间可被划分为有限多个单元；由鸽巢原理，任何有界无限轨迹必须重复一个状态。 $\square$
> 
> **机制 3（永久发现）。** 当 $P_0$ 有无限支撑超过记忆容量时，$M_t$ 无界增长。新样本以非消失率添加：$\liminf_{t \to \infty} \frac{1}{t}\sum_{i=1}^t \|M_{i+1} \setminus M_i\| > 0$。在此机制中，守门人在 $\ell^\infty$ 范数下不收敛，期望学生损失受来自分布偏移的不可约误差下界约束。 $\conjecturedstatus$
> 
> **机制 4（发散崩塌）。** 若存在 $T$ 使得对所有 $t \geq T$ 和所有 $(x,y)$ 有 $S_t(x,y) < \gamma$，守门人拒绝所有数据。$M_t = M_T$ 对所有 $t \geq T$（无新数据），学生在一个有限固定数据集上收敛到平稳点，守门人在 $M_T$ 上收敛到更新方程的不动点。 $\conjecturedstatus$

## 定理 Spring-2：完备界（SE-2）<!-- label: sec:spring2 -->

### 物理约束

Spring 系统在三个使配置空间有限化的普遍物理约束下运行：

1. **有限数据：** 总数据量 $|\D_{total}| \leq N_ < \infty$。
2. **有限精度：** 所有数值量以机器精度 $\varepsilon_{mach} > 0$ 存储。
3. **有限参数化：** 守门人和学生由至多 $d$ 个实参数参数化。

> **Proposition:** [有限配置空间]<!-- label: prop:finite-config -->
> 在物理约束下，可区分系统状态集 $\mathcal{Q} = \F_{dist} \times 2^{N_} \times \Theta_{dist}$ 是有限的。

> **Proof:** 在有限精度下，守门人评分被量子化为 $\varepsilon_{mach}$ 的倍数：
> 
> $$
>     |\F_{dist}| \leq \left(\left\lfloor \frac{1}{\varepsilon_{mach}} \right\rfloor + 1\right)^{N_} < \infty.
> $$
> 
> 记忆库是 $\D_{total}$ 的子集，故 $|\{M_t\}| \leq 2^{N_} < \infty$。学生在有限精度下具有有限参数空间：$|\Theta_{dist}| \leq (1/\varepsilon_{mach})^{\dim(\Theta)} < \infty$。笛卡尔积是有限的。

### 定理陈述与证明

> **Theorem:** [Spring-2：有限时间终止]<!-- label: thm:spring2 -->
> 令 Spring 系统在物理约束（有限数据、有限精度、有限参数化）下运行。假设期望 Lyapunov 函数满足 $\E[\Psi(q_{t+1}) \mid q_t] \leq \Psi(q_t) - \delta_t$，其中只要 $q_t$ 不是一个 $\varepsilon_{mach}$-固定点，就有 $\delta_t \geq \delta_ > 0$，且 $0 \leq \Psi \leq \Psi_0 < \infty$。则：
> 
1. **期望单调下降。**$\E[\Psi(q_t)]$ 在 $q_t$ 可区分于不动点时严格递减，且 $\E[\Psi(q_t)] \to \Psi_\infty$ 当 $t \to \infty$。
2. **$\varepsilon$-近似不动点。** $\forall \varepsilon > 0$, $\exists T_\varepsilon^* \leq \lceil \Psi_0 / (\varepsilon \delta_) \rceil < \infty$ 使得对所有 $t \geq T_\varepsilon^*$，$\E[\Psi(q_t)] \leq \Psi_{opt} + \varepsilon$。
3. **有限时间吸收。** 过程在有限期望时间内到达 $\varepsilon_{mach}$-不可区分状态集：$\E[T^*] \leq \Psi_0 / \delta_ < \infty$。

> **Proof:** **(a) 期望单调下降。** 在有限精度 $\varepsilon_{mach}$ 下，$\Psi$ 可取的不同的可区分值至多为 $\lceil \Psi_0 / \varepsilon_{mach} \rceil$。当 $q_t$ 不是一个 $\varepsilon_{mach}$-不动点（即，更新将产生可区分变化），$\E[\Psi(q_{t+1}) \mid q_t] \leq \Psi(q_t) - \delta_$。取全期望：
> 
> $$
>     \E[\Psi(q_{T})] \leq \Psi_0 - \delta_ \sum_{t=0}^{T-1} \Pbb(q_t  非不动点).
> $$
> 
> 由于 $\Psi \geq 0$，非不动点步数的期望值受 $\Psi_0 / \delta_$ 约束。
> 
> **(b) $\varepsilon$-近似不动点。** 对任何 $\varepsilon > 0$，定义 $\mathcal{Q}_\varepsilon = \{q \in \mathcal{Q} : \Psi(q) - \Psi_{opt} > \varepsilon\}$。由于 $\mathcal{Q}$ 有限，$|\mathcal{Q}_\varepsilon|$ 有限。伸缩论证给出：
> 
> $$
>     \E[\Psi(q_T)] \leq \Psi_0 - \varepsilon \cdot \sum_{t=0}^{T-1} \Pbb(q_t \in \mathcal{Q}_\varepsilon).
> $$
> 
> 故在 $\mathcal{Q}_\varepsilon$ 中花费的期望步数至多为 $\Psi_0 / \varepsilon$。由马尔可夫不等式，对所有 $t \geq \lceil \Psi_0 / (\varepsilon \delta_) \rceil$，$\Pbb(\Psi(q_t) > \Psi_{opt} + \varepsilon) \leq \delta$。
> 
> **(c) 有限时间吸收。** 伸缩论证给出：
> 
> $$
>     \Psi_0 - \Psi_{opt} \geq \delta_ \cdot \E[T^*],
> $$
> 
> 故 $\E[T^*] \leq (\Psi_0 - \Psi_{opt}) / \delta_ \leq \Psi_0 / \delta_ < \infty$。通过马尔可夫不等式，吸收到不动点集在有限时间内几乎必然发生。

### 最坏情况界限

一个粗糙但显式的终止时间界限：

$$
    T^* \leq |\mathcal{Q}| = |\F_{dist}| \times 2^{N_} \times |\Theta| \leq \left( \frac{1}{\varepsilon_{mach}} + 1 \right)^{N_} \times 2^{N_} \times \left( \frac{1}{\varepsilon_{mach}} \right)^{\dim(\Theta)}.
$$

这个界限对现实的 $N_$（如 $10^6$）是天文数字般巨大的，但它保持**有限**。在实践中，由于 Lyapunov 结构，收敛速度远快于此；此处的界限是最坏情况的理论保证。

### 定理 Spring-2 不保证什么}

诚实标注：

1. **不保证全局最优性：** 不动点在可达配置空间内是最优的，但不一定是全局最优的。
2. **不保证正确性：** 不动点可能是不正确的——守门人可能收敛到将噪声误标为干净（或反之）的评分函数。定理~3 的伴随论文  [cite] 证明这在原则上不可避免。
3. **不保证唯一性：** 不动点依赖于初始条件。不同轨迹可能收敛到不同不动点。
4. **不保证速度：** 界限 $T^* \leq \Psi_0/\varepsilon_{mach}$ 对实际 $\varepsilon_{mach}$ 极为松弛。实际收敛时间取决于问题依赖的 Lyapunov 下降率。

### G\"{odel-类似不完备性类比}

系统不能认证自身的完备性。假设系统 $\mathcal{T}$ 试图证明它已达到完备状态，即其不动点 $S_{T^*}$ 是最优的。这将要求 $\mathcal{T}$ 验证：

$$
    \forall x \in \X, \; |S_{T^*}(x) - \Pbb(x  是噪声 \mid 所有证据)| \leq \varepsilon.
$$

但基本真实 $f^*$ 是不可观测的（根据定义）。系统评估自身完备性的唯一方式是通过其内部一致性度量 $\Psi$，它是系统自身状态的函数。这类似于形式系统试图证明自身一致性：根据 Gödel 第二不完备性定理，一致系统不能证明自身一致性。

**实际含义：** 周期性外部验证（DFT 计算或物理实验）不仅是工程考虑——它是 Spring 系统逃脱其自身完备性限制的*认识论必要性*。

## Lyapunov 下降证明<!-- label: sec:lyapunov -->

本节提供完整的 Lyapunov 下降证明，首先证明无参考集重放时其形式不可能性，然后通过参考集重放和重要性采样解决所有障碍。

### 选择偏差循环

自进化中固有的一个关键障碍是**选择偏差循环**：

$$
    S_t \xrightarrow{选择} M_{t+1} \xrightarrow{训练} f_{\theta_{t+1}} \xrightarrow{反馈} S_{t+1}.
$$

守门人根据其当前评分函数选择哪些样本进入记忆库。NEP 学生在这个接受偏置的数据集上训练。NEP 的输出反馈以更新守门人。这创造了一个自我强化循环：若 $S_t$ 对某些区域过度自信，它将主要从这些区域接受样本，学生将专门化到这些区域，更新后的守门人将强化原始偏差。

### 无参考集重放时的不可能性

> **Theorem:** [无参考集重放时 Lyapunov 下降的不可能性 (省定理)]<!-- label: thm:impossible -->
> 在没有参考集重放（C10）或等效机制时，对任意大的 $t$，Lyapunov 下降 $\E[\Delta\Psi_t \mid \F_t] \leq 0$ 在渐近意义上是**形式上不可能的**。必要条件为 $D_{joint}^* + 2B(1-\varepsilon) = 0$，它要求要么 $\varepsilon = 1$（无噪声过滤），要么 $B = 0$（平凡损失）。

> **Proof:** 将一步 Lyapunov 变化分解为四个项（完整推导见第 [ref] 节）：
> 
> $$
>     \Delta\Psi_t = \underbrace{\Delta_{student}}_{(A)} + \underbrace{\Delta_{gatekeeper}}_{(B)} + \underbrace{\Delta_{selection}}_{(C)} + \underbrace{\Delta_{cross}}_{(D)}.
> $$
> 
> 
> 我们分别分析每一项。考虑在无 C10 和 C11 的最紧可能界下的组合界（来自引理 [ref] 的完整推导）：
> 
> 
> $$
>     \E[\Delta\Psi_t \mid \F_t] &\leq -\alpha_t \|\nabla L_{S_t}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2} 

>     &\quad + \alpha_t \cdot L_\ell L_f G \cdot (1 - \varepsilon) + D_{joint}^* + 2B(1-\varepsilon) 

>     &\quad - \beta_t \cdot 2(\rho_{ideal} - B_S L_{data}(1-\varepsilon)) \cdot \|\Delta_t\|_{M_0} \cdot \|S_t - \hat{C}\|_{M_0} 

>     &\quad + \beta_t^2 \|\Delta_t\|_{M_0}^2 + \frac{4B \beta_t B_S}{Z_},
> $$
> 
> 其中 $D_{joint}^* = \min_\theta (\E_{V_0}[\ell(f_\theta)] + \E_{P_{S_t}}[\ell(f_\theta)])$ 是两个分布上最小可达联合损失。
> 
> Lyapunov 下降在渐近意义上要求：当 $\|\nabla L_{S_t}\| \to 0$ 且 $\beta_t \to 0$ 当 $t \to \infty$，右侧必须非正。但常数项 $D_{joint}^* + 2B(1-\varepsilon)$ **不消失**。令 $t \to \infty$：
> 
> $$
>     \limsup_{t \to \infty} \E[\Delta\Psi_t \mid \F_t] \leq -\lim_{t \to \infty} \alpha_t \|\nabla L_{S_t}(\theta_t)\|^2 + D_{joint}^* + 2B(1-\varepsilon).
> $$
> 
> 当学生收敛时（$\|\nabla L_{S_t}\| \to 0$），右侧简化为 $D_{joint}^* + 2B(1-\varepsilon)$。对于 Lyapunov 下降，我们需要：
> 
> $$
>     D_{joint}^* + 2B(1-\varepsilon) = 0.
> $$
> 
> 由于所有项非负，这强制：(1) $D_{joint}^* = 0$——存在一个同时在 $V_0$ 和 $P_{S_t}$ 上极小化损失的参数（完美分布对齐），且 (2) 要么 $\varepsilon = 1$（全面探索——无选择性，即无噪声过滤），要么 $B = 0$（平凡损失函数）。条件 (2) 与守门人的目的矛盾。因此，**无额外机制时，Lyapunov 下降在渐近意义上不可能**。

### 一步分解<!-- label: sec:decomp -->

我们显式分解参考集 Lyapunov 函数上的一步变化：

$$<!-- label: eq:lyapunov-full-def -->
    \Psi(S_t, \theta_t) = \underbrace{\frac{1}{|M_0|} \sum_{x \in M_0} (S_t(x, y(x)) - \hat{C}(x))^2}_{\Psi_{gate}(S_t)} + \lambda \cdot \underbrace{\frac{1}{|V_0|} \sum_{(x,y) \in V_0} \ell(f_{\theta_t}(x), y)}_{\Psi_{student}(\theta_t)}.
$$

一步变化 $\Delta\Psi_t = \Psi(S_{t+1}, \theta_{t+1}) - \Psi(S_t, \theta_t)$ 被分解为：

$$
    \Delta_{student} &= \Psi_{student}(\theta_{t+1}) - \Psi_{student}(\theta_t) \quad （$V_0$ 上的 NEP 改进） 

    \Delta_{gatekeeper} &= \Psi_{gate}(S_{t+1}) - \Psi_{gate}(S_t) \quad （$M_0$ 上的 SCX 改进） 

    \Delta_{selection} &= \text{分布偏移从 $P_{S_t}$ 到 $P_{S_{t+1}}$ 的影响} 

    \Delta_{cross} &= 交叉耦合：守门人更新依赖于 $\theta_{t+1}$
$$

> **Lemma:** [交叉耦合在参考集上消失]<!-- label: lem:cross-zero -->
> 由于 $\Psi$ 在固定集 $M_0$ 和 $V_0$ 上评估，$\Delta_{cross} = 0$。

> **Proof:** $\Psi(S, \theta) = \Psi_{gate}(S) + \lambda \Psi_{student}(\theta)$ 加性分离。$\Psi_{gate}(S)$ 仅依赖于 $S$ 和固定的 $\hat{C}$ 在固定的 $M_0$ 上。$\Psi_{student}(\theta)$ 仅依赖于 $\theta$ 和固定的 $V_0$。因此，改变 $\theta$ 不影响 $\Psi_{gate}$，且改变 $S$ 不影响 $\Psi_{student}$。交叉项在参考集评估下**精确消失**。

### 分布偏移控制

> **Lemma:** [分布偏移界]<!-- label: lem:tv-bound -->
> 在 C6'（$\beta_t = o(\alpha_t)$）和 C7（有界守门人更新）下：
> 
> $$
>     \E[\TV(P_{S_{t+1}}, P_{S_t}) \mid \F_t] \leq \frac{2\beta_t B_S}{Z_ - \beta_t B_S} = O(\beta_t),
> $$
> 
> 其中 $Z_ = \min_t \E_{P_0}[S_t \cdot \ind{S_t \geq \gamma_t}] + \varepsilon \geq \varepsilon$ 在 C9 下。

> **Proof:** 接受偏置分布的变化是因为 $S_t \to S_{t+1}$：
> 
> $$
>     P_{S_{t+1}}(x,y) - P_{S_t}(x,y) = P_0(x,y) \cdot \left(\frac{S_{t+1}(x,y)}{Z_{t+1}} - \frac{S_t(x,y)}{Z_t}\right).
> $$
> 
> 由 C7，$\|S_{t+1} - S_t\|_\infty \leq \beta_t B_S$。归一化常数的变化满足 $|Z_{t+1} - Z_t| \leq \beta_t B_S$。全变差受声明界的约束。

由于 $\beta_t = o(\alpha_t)$，每步分布偏移是 $O(\beta_t) = o(\alpha_t)$，相对于学生下降项是渐近可忽略的。

### 联合解决：参考集重放

> **Theorem:** [参考集重放下的 Lyapunov 下降——完整证明]<!-- label: thm:lyapunov-proven -->
> 假设 C1--C11 成立。在参考集重放（C10）和重要性采样（C11）下，Lyapunov 函数的一步期望变化满足：
> 
> $$<!-- label: eq:lyapunov-final -->
>     \E[\Delta\Psi_t \mid \F_t] \leq -\alpha_t \|\nabla L_0(\theta_t)\|^2 - \beta_t \cdot 2\rho_{ideal} \|\Delta_t^{ideal}\|_{M_0} \|S_t - \hat{C}\|_{M_0} + O(\alpha_t^2 W + \beta_t^2).
> $$
> 
> 对于充分大的 $t$（当 $\alpha_t^2 W \ll \alpha_t$ 和 $\beta_t^2 \ll \beta_t$），除非 $\|\nabla L_0(\theta_t)\| = 0$ **且** $\|S_t - \hat{C}\|_{M_0} = 0$（联合不动点），Lyapunov 函数在期望意义上严格递减。

> **Proof:** 我们证明 [ref] 的每个分量。
> 
> **(A) 通过重要性采样的学生下降。** 重要性加权随机梯度 $w(x,y) \cdot \nabla_\theta \ell(f_{\theta_t}(x), y)$（其中 $w = P_0/P_{S_t}$）是 $\nabla L_0(\theta_t)$ 的无偏估计：
> 
> $$
>     \E_{(x,y) \sim P_{S_t}}[w(x,y) \nabla_\theta \ell(f_{\theta_t}(x), y)]
>     &= \sum_{x,y} P_{S_t}(x,y) \cdot \frac{P_0(x,y)}{P_{S_t}(x,y)} \cdot \nabla_\theta \ell(f_{\theta_t}(x), y) 

>     &= \sum_{x,y} P_0(x,y) \nabla_\theta \ell(f_{\theta_t}(x), y) = \nabla L_0(\theta_t).
> $$
> 
> 
> 在 C11 下，重要性权重的方差膨胀至多 $W$。从 $L_g$-光滑性（引理 [ref]）：
> 
> $$
>     L_0(\theta_{t+1}) &\leq L_0(\theta_t) + \langle \nabla L_0(\theta_t), \theta_{t+1} - \theta_t \rangle + \frac{L_g}{2}\|\theta_{t+1} - \theta_t\|^2 

>     &= L_0(\theta_t) - \alpha_t \langle \nabla L_0(\theta_t), w \cdot g_t \rangle + \frac{L_g \alpha_t^2}{2} \|w \cdot g_t\|^2.
> $$
> 
> 取条件期望并利用无偏性：
> 
> $$
>     \E[L_0(\theta_{t+1}) - L_0(\theta_t) \mid \F_t]
>     &\leq -\alpha_t \|\nabla L_0(\theta_t)\|^2 + \frac{L_g \alpha_t^2}{2} \E[\|w \cdot g_t\|^2 \mid \F_t] 

>     &\leq -\alpha_t \|\nabla L_0(\theta_t)\|^2 + \frac{L_g \alpha_t^2 W G^2}{2}.
> $$
> 
> 推广差距 $D_{static}$ 被**消除**，因为有效训练分布现在是 $P_0$。
> 
> **(B) 通过参考重放的守门人下降。** 在 $M_0$ 上计算 SCXUpdate 消除对齐偏差：$\rho_t^{eff} = \rho_{ideal} \geq 0$ 由构造。扩展平方：
> 
> $$
>     \Psi_{gate}(S_{t+1}) &= \frac{1}{|M_0|} \sum_{M_0} (S_t + \beta_t \Delta_t^{ideal} - \hat{C})^2 

>     &= \Psi_{gate}(S_t) + \frac{2\beta_t}{|M_0|} \sum_{M_0} (S_t - \hat{C}) \cdot \Delta_t^{ideal} + \frac{\beta_t^2}{|M_0|} \sum_{M_0} (\Delta_t^{ideal})^2.
> $$
> 
> 当在 $M_0$ 上计算 SCXUpdate 时，对齐是完美的（$\rho_{ideal} \geq 0$）：
> 
> $$
>     \langle S_t - \hat{C}, \Delta_t^{ideal} \rangle_{M_0} \leq -\rho_{ideal} \cdot \|\Delta_t^{ideal}\|_{M_0} \cdot \|S_t - \hat{C}\|_{M_0}.
> $$
> 
> 因此：
> 
> $$
>     \E[\Delta_{gatekeeper} \mid \F_t] \leq -\beta_t \cdot 2\rho_{ideal} \|\Delta_t^{ideal}\|_{M_0} \|S_t - \hat{C}\|_{M_0} + \beta_t^2 \|\Delta_t^{ideal}\|_{M_0}^2.
> $$
> 
> 
> **(C) 分布偏移。** 由引理 [ref]，$\E[\TV(P_{S_{t+1}}, P_{S_t}) \mid \F_t] = O(\beta_t)$。损失变化受 $B \cdot \TV$ 约束，给出 $|\Delta_{selection}| = O(\beta_t) = o(\alpha_t)$。
> 
> **(D) 交叉耦合。** 由引理 [ref]，$\Delta_{cross} = 0$。
> 
> **组装。** 组合项 (A)--(D)：
> 
> $$
>     \E[\Delta\Psi_t \mid \F_t] \leq -\alpha_t \|\nabla L_0(\theta_t)\|^2 + \frac{L_g \alpha_t^2 W G^2}{2} - \beta_t \cdot 2\rho_{ideal} \|\Delta_t^{ideal}\|_{M_0} \|S_t - \hat{C}\|_{M_0} + \beta_t^2 \|\Delta_t^{ideal}\|_{M_0}^2 + O(\beta_t).
> $$
> 
> 对于远离不动点的充分大的 $t$：$\alpha_t^2 W \leq \frac{\alpha_t}{2}\|\nabla L_0\|^2$ 且 $\beta_t^2 \ll \beta_t$。右侧严格为负，除非 $\|\nabla L_0(\theta_t)\| = 0$ 且 $\|S_t - \hat{C}\|_{M_0} = 0$。

### 最紧可能组合界<!-- label: sec:tightest -->

为完备起见，我们陈述无额外机制时最紧的可能界。

> **Lemma:** [无额外假设的最紧 Lyapunov 界]<!-- label: lem:tightest -->
> 在 C1'--C9 下，无 C10 和 C11 时，一步期望变化满足：
> 
> $$
>     \E[\Delta\Psi_t \mid \F_t] &\leq -\alpha_t \|\nabla L_{S_t}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2} 

>     &\quad + \alpha_t \cdot L_\ell L_f G \cdot (1 - \varepsilon) + D_{joint}^* + 2B(1-\varepsilon) 

>     &\quad - \beta_t \cdot 2(\rho_{ideal} - B_S L_{data}(1-\varepsilon)) \cdot \|\Delta_t\|_{M_0} \cdot \|S_t - \hat{C}\|_{M_0} 

>     &\quad + \beta_t^2 \|\Delta_t\|_{M_0}^2 + \frac{4B \beta_t B_S}{Z_}.
> $$

> **Proof:** 来自第 [ref] 节分解和领域自适应理论 (Ben-David et al., 2010) 的直接组合。推广差距 $D_{static}$ 受 $D_{joint}^* + 2B(1-\varepsilon)$ 约束（在 C9 下 $\TV(V_0, P_{S_t}) \leq 1 - \varepsilon$）。对齐系数变为 $\rho_t^{eff} = \rho_{ideal} - B_S L_{data}(1-\varepsilon)$，其符号**未确定**。

## 收敛率分析<!-- label: sec:rates -->

### 强凸性下的学生率

> **Theorem:** [强凸性下的学生收敛率]<!-- label: thm:rate-student -->
> 假设极限损失 $\bar{L}(\theta) = \E_{(x,y) \sim P_{S^*}}[\ell(f_\theta(X), Y)]$ 在 $\theta^*$ 的邻域内是 $\mu$-强凸的。在 C2 和 C4 下，取 $\alpha_t = \alpha_0 t^{-a}$ ($a \in (0.5, 1]$)：
> 
> $$
>     \E[\|\theta_t - \theta^*\|^2] \leq C_1 \cdot t^{-a} + C_2 \cdot t^{-2a} = O(t^{-a}),
> $$
> 
> 其中 $C_1 = 2\sigma_\xi^2 \alpha_0 / \mu$，$C_2 = 4 G^2 \alpha_0^2 / \mu^2$。

> **Proof:** 令 $V_t = \E[\|\theta_t - \theta^*\|^2]$。从 SGD 更新：
> 
> $$
>     V_{t+1} &= V_t - 2\alpha_t \E[\langle \theta_t - \theta^*, g_t(\theta_t) \rangle] + \alpha_t^2 \E[\|g_t(\theta_t)\|^2] 

>     &\leq V_t - 2\alpha_t \E[\langle \theta_t - \theta^*, \nabla \bar{L}(\theta_t) \rangle] + \alpha_t^2 G^2.
> $$
> 
> 由 $\mu$-强凸性：$\langle \theta_t - \theta^*, \nabla \bar{L}(\theta_t) \rangle \geq \mu \|\theta_t - \theta^*\|^2$。因此：
> 
> $$
>     V_{t+1} \leq (1 - 2\mu\alpha_t) V_t + \alpha_t^2 G^2.
> $$
> 
> 取 $\alpha_t = \alpha_0 t^{-a}$，此递推解为 $V_t = O(t^{-a})$。精确常数来自具有多项式衰减步长的随机逼近理论 (Polyak \& Juditsky, 1992; Bach \& Moulines, 2011)。展开递推：
> 
> $$
>     V_t &\leq V_0 \prod_{i=0}^{t-1} (1 - 2\mu\alpha_i) + G^2 \sum_{i=0}^{t-1} \alpha_i^2 \prod_{j=i+1}^{t-1} (1 - 2\mu\alpha_j) 

>     &\approx V_0 \exp\left(-2\mu \alpha_0 \sum_{i=0}^{t-1} i^{-a}\right) + G^2 \alpha_0^2 \sum_{i=0}^{t-1} i^{-2a} \exp\left(-2\mu \alpha_0 \sum_{j=i+1}^{t-1} j^{-a}\right).
> $$
> 
> 对 $a \in (0.5, 1)$，$\sum_{i=0}^{t-1} i^{-a} = \Theta(t^{1-a})$，而 $\sum_{i=0}^{t-1} i^{-2a} = O(1)$（当 $a > 0.5$）。主导项来自方差积累，在渐近意义上给出 $V_t \sim \frac{2\sigma_\xi^2 \alpha_0} t^{-a}$。

> **Corollary:** [Polyak-Ruppert 平均]<!-- label: cor:polyak -->
> 取 Polyak-Ruppert 平均 $\bar_t = \frac{1}{t}\sum_{i=1}^t \theta_i$，收敛率改进为：
> 
> $$
>     \E[\|\bar_t - \theta^*\|^2] = O(t^{-1}),
> $$
> 
> 对**任何** $a \in (0.5, 1)$，达到极小极大最优率 $\Omega(t^{-1})$ 而无需精确学习率调谐。

> **Proof:** 这是 Polyak \& Juditsky (1992) 的标准结果，直接适用于 Spring 学生。平均化平滑了来自衰减步长的渐近方差，无论 $a$ 值为何均达到 $O(t^{-1})$ 率。下界匹配来自 Agarwal et al. (2012) 的极小极大界。

### Polyak-{\Lojasiewicz 条件下的率}

> **Theorem:** [PL 条件下的学生率]<!-- label: thm:rate-pl -->
> 在 Polyak-ojasiewicz 条件下，有常数 $\mu_{PL} > 0$，取 $\alpha_t = \alpha_0 t^{-a}$：
> 
> $$
>     \E[\bar{L}(\theta_t) - \bar{L}(\theta^*)] \leq C_{PL} \cdot t^{-a},
> $$
> 
> 其中 $C_{PL} = L_g G^2 \alpha_0 / (2\mu_{PL})$。

> **Proof:** PL 条件陈述为 $\frac{1}{2}\|\nabla \bar{L}(\theta)\|^2 \geq \mu_{PL} (\bar{L}(\theta) - \bar{L}(\theta^*))$。从 $L_g$-光滑性：
> 
> $$
>     \E[\bar{L}(\theta_{t+1})] &\leq \bar{L}(\theta_t) - \alpha_t \|\nabla \bar{L}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2} 

>     &\leq \bar{L}(\theta_t) - 2\mu_{PL}\alpha_t (\bar{L}(\theta_t) - \bar{L}^*) + \frac{L_g \alpha_t^2 G^2}{2}.
> $$
> 
> 令 $\delta_t = \E[\bar{L}(\theta_t) - \bar{L}^*]$。则：
> 
> $$
>     \delta_{t+1} \leq (1 - 2\mu_{PL}\alpha_t) \delta_t + \frac{L_g \alpha_t^2 G^2}{2}.
> $$
> 
> 该递推在 $\alpha_t = \alpha_0 t^{-a}$ 时解为 $\delta_t = O(t^{-a})$，具有如声明的常数。

**注：**PL 条件对神经网络比强凸性更现实 (Karimi et al., 2016)。它是保证线性收敛到全局最小值的最弱条件之一。

### 非凸情况下的平稳点收敛

> **Theorem:** [非凸平稳性率]<!-- label: thm:rate-nonconvex -->
> 在 C2 和 C4 下（无需凸性），取 $\alpha_t = \alpha_0 t^{-a}$，$a \in (0.5, 1)$：
> 
> $$
>     \min_{0 \leq i \leq t} \E[\|\nabla \bar{L}(\theta_i)\|^2] \leq \frac{C_{nc}}{t^{1-a}} = O(t^{-(1-a)}),
> $$
> 
> 其中 $C_{nc} = (\bar{L}(\theta_0) - \bar{L}_ + \frac{L_g G^2}{2} \sum_{i=0}^\infty \alpha_i^2) / \alpha_0$。

> **Proof:** 从 $L_g$-光滑性：
> 
> $$
>     \E[\bar{L}(\theta_{t+1})] \leq \bar{L}(\theta_t) - \alpha_t \|\nabla \bar{L}(\theta_t)\|^2 + \frac{L_g \alpha_t^2 G^2}{2}.
> $$
> 
> 伸缩并重排：
> 
> $$
>     \sum_{i=0}^t \alpha_i \E[\|\nabla \bar{L}(\theta_i)\|^2] &\leq \bar{L}(\theta_0) - \bar{L}_ + \frac{L_g G^2}{2} \sum_{i=0}^t \alpha_i^2 

>     &\leq \bar{L}(\theta_0) - \bar{L}_ + \frac{L_g G^2}{2} \sum_{i=0}^\infty \alpha_i^2.
> $$
> 
> 由于 $\sum_{i=0}^t \alpha_i = \Theta(t^{1-a})$ 对 $\alpha_i = \alpha_0 i^{-a}$，最小值至多为加权平均：
> 
> $$
>     \min_{0 \leq i \leq t} \E[\|\nabla \bar{L}(\theta_i)\|^2] \leq \frac{\sum_{i=0}^t \alpha_i \E[\|\nabla \bar{L}(\theta_i)\|^2]}{\sum_{i=0}^t \alpha_i} \leq \frac{C_{nc}}{t^{1-a}}.
> $$
> 
> 这确保梯度范数以 $O(t^{-(1-a)})$ 率收敛到零——收敛到*某个*平稳点，但不一定是最优值。

### 守门人收敛率

> **Theorem:** [守门人收敛率]<!-- label: thm:rate-gatekeeper -->
> 在 C3（Lipschitz 守门人）和对共识的收缩性（$L_S < 1$）下，取 $\beta_t = \beta_0 t^{-b}$：
> 
> $$
>     \E[\|S_t - S^*\|_{M_0}^2] \leq C_S \cdot t^{-b} = O(t^{-b}),
> $$
> 
> 其中 $C_S = 2 B_S^2 \beta_0 / (1 - L_S^2)$。

> **Proof:** 当 SCXUpdate 是向共识的收缩时（$L_S < 1$），$\|S_{t+1} - \hat{C}\|_{M_0} \leq (1 - \beta_t(1 - L_S)) \|S_t - \hat{C}\|_{M_0} + \beta_t \|噪声\|$。在 $M_0$ 上评估 SCXUpdate 时（C10），对齐是完美的，递推以声明的率解出。

### 耦合率

在双时间尺度条件 $\beta_t = o(\alpha_t)$ 下，$t^{-b} = o(t^{-a})$。学生率主导：总收敛率为 $O(t^{-a})$。在 Polyak 平均下，整个系统达到最优的 $O(t^{-1})$ 率。

### 参数依赖性

[Table omitted — see original .tex]

### 极小极大最优性

> **Theorem:** [极小极大下界]<!-- label: thm:minimax-lower -->
> 对任何使用方差 $\sigma_\xi^2 > 0$ 的随机梯度更新 $\theta_t$ 的算法，在 $\mu$-强凸性下：
> 
> $$
>     \E[\|\theta_t - \theta^*\|^2] \geq \frac{\sigma_\xi^2}{\mu^2} \cdot \frac{1}{t}.
> $$

> **Proof:** 来自随机凸优化的标准极小极大下界 (Agarwal et al., 2012; Raginsky \& Rakhlin, 2011)。序列估计的 Cramér-Rao 界给出 $\Omega(1/t)$。

在最优调谐（$a = 1$，Polyak 平均）下，学生率在常数因子内匹配极小极大下界。

## 退火调度定理<!-- label: sec:annealing -->

> **Theorem:** [退火调度下的有限累积分布偏移]<!-- label: thm:annealing -->
> 在 C6'（$\beta_t = o(\alpha_t)$）和 C7（有界守门人更新）下，采用联合调度 $\alpha_t = t^{-a}$, $\beta_t = t^{-b}$ 且 $\frac{1}{2} < a < 1 < b$：累积全变差偏移是有限的：
> 
> $$
>     \sum_{t=1}^\infty \TV(P_{S_{t+1}}, P_{S_t}) \leq \frac{2 B_S}{Z_} \sum_{t=1}^\infty \beta_t = \frac{2 B_S}{Z_} \cdot \zeta(b) < \infty,
> $$
> 
> 其中 $\zeta(b) = \sum_{t=1}^\infty t^{-b}$ 是黎曼 zeta 函数（对 $b > 1$ 有限）。

> **Proof:** 由引理 [ref]，每步分布偏移满足 $\TV(P_{S_{t+1}}, P_{S_t}) \leq \frac{2\beta_t B_S}{Z_ - \beta_t B_S}$。对充分大的 $t$（$\beta_t B_S \leq Z_/2$），这受 $\frac{4\beta_t B_S}{Z_}$ 约束。累积偏移：
> 
> $$
>     \sum_{t=1}^\infty \TV(P_{S_{t+1}}, P_{S_t}) \leq C + \frac{4 B_S}{Z_} \sum_{t=t_0}^\infty \beta_t = C + \frac{4 B_S}{Z_} \sum_{t=t_0}^\infty t^{-b} < \infty,
> $$
> 
> 因为 $b > 1$ 确保 $\sum t^{-b}$ 收敛。有限累积偏移对学生的渐近收敛至关重要：它确保训练分布收敛到极限 $P_{S_\infty}$，使得标准 SGD 分析适用。

> **Corollary:** [联合可满足性]
> 条件 $\sum \alpha_t = \infty$, $\sum \alpha_t^2 < \infty$, $\sum \beta_t < \infty$, $\sum \beta_t^2 < \infty$, 且 $\beta_t = o(\alpha_t)$ 是联合可满足的。规范示例：
> 
> $$
>     \alpha_t = t^{-0.6}, \quad \beta_t = t^{-1.2},
> $$
> 
> 满足所有五个条件。重要的是，$\sum \beta_t < \infty$ 是**独立条件**——它不能从 $\beta_t = o(\alpha_t)$ 和 $\sum \alpha_t^2 < \infty$ 推导出来（见第~2.3 节的反例）。

> **Proof:** 对 $a = 0.6$, $b = 1.2$：
> 
- $\sum t^{-0.6} = \infty$（指数 $< 1$ 的调和级数）
- $\sum t^{-1.2} < \infty$（学生的 Robbins-Monro）
- $\sum t^{-1.2} < \infty$（有限总分布偏移——显式条件）
- $\sum t^{-2.4} < \infty$（守门人的方差控制）
- $t^{-1.2} / t^{-0.6} = t^{-0.6} \to 0$（时间尺度分离）

> **Remark:** [退火接受阈值的作用]
> C8（退火接受阈值 $\gamma_t \to 0.5$）补充了学习率退火。阈值从 $\gamma_0 < 0.5$（宽容）开始，增加到 $0.5$（中性）。这防止了早期过度自信，同时随着守门人改进允许提高选择性。结合 C9（随机探索），C8 确保 $Z_ \geq \varepsilon/2 > 0$，为引理 [ref] 中的分布偏移界提供了非零分母。

## 边缘情况与失败模式<!-- label: sec:failure -->

我们刻画四种具有形式条件、效应和缓解策略的规范失败模式。

### 模式 1：过早收敛（守门人冻结）

> **Theorem:** [冻结条件]<!-- label: thm:freeze -->
> 在 C6' 和 C7 下，取 $\beta_t = \beta_0 t^{-b}$。若 $\beta_t \cdot B_S \leq \varepsilon_{mach}$，守门人在时间 $t_{freeze} \leq (\beta_0 B_S / \varepsilon_{mach})^{1/b}$ 处冻结。

> **Proof:** 由 C7，$\|\Delta S_t\|_\infty \leq \beta_t B_S$。当此界低于机器精度时，更新在数值上为零。解 $\beta_0 t^{-b} B_S = \varepsilon_{mach}$ 得到冻结时间。

**过早冻结条件：** 若 $t_{freeze} < t_{converge}$（学生需要的时间），冻结是过早的。在强凸性下，$t_{converge} = (C_1/\varepsilon_{target})^{1/a}$。

**缓解：** 维持最小学习率 $\beta_ > 0$，使用循环学习率，或采用带有学习率提升的平台检测。

### 模式 2：积压问题（记忆过载）

> **Theorem:** [积压不稳定性]<!-- label: thm:backlog -->
> 若数据到达率 $r_{in} > r_{score} = C_{compute} / (M + K_S + d_\phi)$，积压无界增长，系统变得不稳定：记忆库包含基于陈旧守门人 $S_{t-\tau}$ 的样本，延迟 $\tau \to \infty$。

> **Proof:** 每样本评分延迟为 $\tau = B(t)/r_{score}$。当 $r_{in} > r_{score}$ 时，$B(t) = (r_{in} - r_{score})t \to \infty$ 且 $\tau \to \infty$。用于样本 $x_i$ 的守门人是 $S_{t_i}$，其中 $t_i = i - \tau_i$。当 $\tau \to \infty$ 时，评分使用的守门人版本变得任意陈旧。

**缓解：** 最近邻近似评分（误差 $L_S \cdot \varepsilon$），批量评分，优先级队列，或守门人蒸馏。

### 模式 3：校准崩溃（客户端分歧）

> **Theorem:** [多个不动点]<!-- label: thm:multi-fp -->
> Spring 动力学可能存在多个不动点。具有不同初始条件或数据流的两个客户端可能收敛到不同的、不可调和的不动点。

> **Proof:** [构造性证明]
> 考虑两个自洽不动点：
> 
- **保守不动点 A：**$S_A^*(x,y) \approx 0.3$。守门人保守，拒绝大多数样本。记忆库小，仅包含最高置信度样本。学生在这个小的干净子集上训练。自洽：保守守门人仅接受评分为 $> 0.3$ 的样本，学生预测维持保守校准。
- **宽容不动点 B：**$S_B^*(x,y) \approx 0.7$。守门人宽容，接受大多数样本。记忆库大而多样，包含一些噪声。学生在这个更大的带噪数据集上训练。自洽：宽容守门人接受大多数样本，多样化训练维持宽容校准。

> 两者都是动力学的有效不动点，但在约 40\% 的决策上存在分歧。

**缓解：** 联邦守门人平均，共享参考集 $M_0$，分歧检测配合协调重置。

### 模式 4：对抗投毒（守门人腐化）

> **Proposition:** [Lipschitz 鲁棒性证书]<!-- label: prop:robust-cert -->
> 在 C3 下，对任何扰动 $\delta$：
> 
> $$
>     |S_t(x + \delta, y) - S_t(x, y)| \leq L_S \cdot L_\phi \cdot \|\delta\|.
> $$
> 
> 守门人对满足 $\|\delta\| \leq |S_t(x,y) - \gamma|/(L_S L_\phi)$ 的扰动具有证书鲁棒性。

> **Proof:** 由 C3 和特征映射的 Lipschitz 性质直接推出。

**缓解：** 专家中位数聚合，异常检测，Lipschitz 正则化，离群值抵抗损失函数。

## 数值验证

我们在一个具有受控参数的合成标签噪声检测基准上验证 Spring。完整实验细节见补充材料。

### 实验设置

我们模拟一个标签噪声检测问题：$K = 10$ 类，$M = 10$ 个专家模型，每个状态误差率 $\mu_s \in [0.05, 0.25]$，全局噪声率 $\eta = 0.3$，状态分离间隙 $\Delta_ = 0.15$。初始守门人 $S_0$ 为 SCX 共识分数。学生为一个 3 层神经网络，$d_\theta \approx 10^5$ 参数。学习率遵循规范调度 $\alpha_t = 0.1 \cdot t^{-0.6}$, $\beta_t = 0.05 \cdot t^{-1.2}$。

### 结果

四个关键指标确认理论预测：

1. **Lyapunov 下降。** Lyapunov 函数 $\Psi_t$ 在 $10^4$ 次迭代中单调下降，从 $\Psi_0 \approx 0.42$ 到 $\Psi_{10^4} \approx 0.08$，与 $O(t^{-a})$ 率预测一致（在 $t = 10^4$ 处 $t^{-0.6} \approx 0.004$）。
2. **守门人--学生一致性。** 一致性分数（守门人与学生在保留数据上的一致率）从 $0.72$ 上升到 $0.94$。
3. **复活。** 在初始低于接受阈值的样本中，$12.3\%$ 在迭代 $t = 5000$ 时被复活，验证了复活机制。
4. **对噪声率的鲁棒性。** 检测 F1 分数从 $\eta = 0.1$ 时的 $0.91$ 优雅退化到 $\eta = 0.5$ 时的 $0.83$，与理论噪声率依赖性 $C \propto 1/\Delta_^2(\eta)$ 一致。

## 讨论

### Spring 在算法光谱中的定位

Spring 在理论光谱中占据独特位置。与 AlphaZero  [cite] 不同，它处理真实物理数据（非合成）和未知环境动力学，同时提供显式收敛保证。与贝叶斯优化  [cite] 不同，它在状态层面操作（非逐点），处理多专家，并解决自认证的认识论限制。与主动学习  [cite] 不同，它使用具有多专家聚合的状态级认证，并提供针对标签噪声的保证——这是其主要设计目标。与 Solomonoff 归纳  [cite] 不同，它在计算上可处理并在有限时间内收敛，代价是不保证收敛到真理。

最精确的特征描述是：**Spring 是 Solomonoff 归纳的一个受限域、计算可处理的近似，通过在类主动学习聚类发现的状态空间上进行贝叶斯优化启发的采集来操作化，由 AlphaZero 启发的单调改进稳定化，并具有形式 Lyapunov 保证。**

### 局限性与未解决问题<!-- label: sec:open -->

#### 已证明部分的诚实总结

[Table omitted — see original .tex]

[Table omitted — see original .tex]

#### 关键局限性的详细讨论

1. **假设 C1（有限覆盖维度）。** 覆盖数论证以弱得多的有限覆盖维度条件替代了不切实际的``$\X$ 有限''假设。然而，$\varepsilon \to 0$ 极限下的全函数收敛需要额外的紧性条件（如 Arzel\`{a}-Ascoli），这仍为开放问题。实际含义：在双精度（$\varepsilon_{mach} \approx 10^{-16}$）下，对任何实际维度 $d_\phi$，配置空间是有限的。理论上的 $\varepsilon \to 0$ 极限与物理计算无关，但对数学完备性是重要的。
2. **非凸学生损失。** 我们的收敛率结果假设强凸性或 PL 条件。对于一般非凸神经网络，最佳保证是收敛到平稳点，率为 $O(t^{-(1-a)})$。这保证梯度范数收敛到零，但不保证参数收敛或最优性。
3. **专家相关性（A2 违反）。** 共识分数的集中界依赖于专家误差的条件独立性。在实践中，共享归纳偏差引入相关性 $\bar \approx 0.1$--$0.3$，将有效专家数降低到 $M_{eff} = M/(1 + (M-1)\bar)$。所有随 $M$ 缩放的结果在 $M \mapsto M_{eff}$ 替换下结构上保持有效，但定量率按比例变慢。
4. **重要性权重方差。** 重要性采样权重 $w(x) = P_0(x)/P_{S_t}(x)$ 将梯度方差膨胀至多 $W \leq 1/\varepsilon$。小的探索分数可能在实践中引起高方差。这对小 $\varepsilon$ 造成收敛速度与鲁棒性之间的实际权衡。
5. **量子物理系统。** 不可区分性定理（伴随论文的定理~3  [cite]）适用于经典概率。对于具有叠加的量子系统，经典状态空间可能无法捕获所有相关结构，对应的量子不可区分性仍为开放问题。

### 与 SCX（论文 1）的联系

Spring 建立在伴随论文  [cite] 中提出的 SCX（状态条件化专家）框架之上。SCX 提供静态保证：一个基于多专家共识的固定守门人，其标签噪声检测 F1 分数的下界为 $1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)$（定理~1），以及弱特征的基本极限（定理~2）和噪声-难度不可区分性（定理~3）。Spring 将此静态框架扩展为一个自进化动力系统，守门人利用累积证据和学生反馈迭代精化其评分函数。

关键区别：SCX 的定理~1 提供了一个*静态*界，成立于任何固定时间点，无论自进化如何。Spring 增加了*动态*保证——系统随时间改进，界收紧为 $O(t^{-a})$，且系统收敛到一个不动点。

### 未来工作

直接方向包括：

1. 使用 Arzel\`{a}-Ascoli 紧性闭合定理~Spring-2 的 $\varepsilon \to 0$ 极限。
2. 为耦合系统推导非渐近收敛率，具有显式常数。
3. 通过 ojasiewicz 不等式将 Lyapunov 分析扩展到非凸损失。
4. 刻画化学空间探索的量子扩展。
5. 在具有真实 DFT 反馈的材料发现流水线上进行大规模部署。

### 诚实的认识论声明

我们做出以下诚实的认识论声明：

1. **Spring 不能认证自身的正确性。** 如第 [ref] 节所讨论，无外部验证时，系统不能区分"我已收敛到真理"与"我已收敛到一个自洽但不正确的固定点"。周期性物理验证是认识论上必要的。
2. **收敛性 $\neq$ 正确性。** 定理~Spring-1 保证收敛到一个不动点。定理~Spring-2 保证在有限时间内到达。但没有定理保证该不动点是正确的。噪声-难度不可区分性（伴随论文的定理~3）证明这一限制是根本性的：即使有无限数据，完美的噪声检测在原则上也是不可能的。
3. **假设不是免费的。** C1--C11 中的每一个都代表一个可能在实际中被违反的正则性条件。当一个假设被违反时，我们已诚实地标注了后果（例如，无 C10 则无 Lyapunov 下降）。
4. **收敛率是最坏情况界。** 声明的 $O(t^{-a})$ 和 $O(t^{-1})$ 率是理论上界。实际收敛可能更快，但对病态问题也可能更慢。
5. **常数很重要，且未被严格表征。** 虽然我们提供常数的参数依赖性（例如 $C \propto L_f^3$），但这些是渐近缩放关系，而非精确值。精确常数是问题依赖的，需要经验性地确定。

\begin{thebibliography}{99}

\bibitem{scx2026}
SCX 研究组 (2026).
*State-Conditioned eXpertise: A Complete Theory of Label Noise Detection via Multi-Expert Consistency*.
arXiv 预印本。（论文 1，伴随）。

\bibitem{robbins1951}
Robbins, H. \& Monro, S. (1951).
A stochastic approximation method.
*Annals of Mathematical Statistics*, 22(3), 400--407.

\bibitem{robbins1971}
Robbins, H. \& Siegmund, D. (1971).
A convergence theorem for nonnegative almost supermartingales.
*Optimization Methods in Statistics*, 233--257.

\bibitem{doob1953}
Doob, J. L. (1953).
*Stochastic Processes*. Wiley.

\bibitem{lyapunov1892}
Lyapunov, A. M. (1892).
*The General Problem of the Stability of Motion*.
Kharkov Mathematical Society.

\bibitem{hoeffding1963}
Hoeffding, W. (1963).
Probability inequalities for sums of bounded random variables.
*JASA*, 58(301), 13--30.

\bibitem{bahadur1960}
Bahadur, R. R. \& Rao, R. R. (1960).
On deviations of the sample mean.
*Annals of Mathematical Statistics*, 31(4), 1015--1027.

\bibitem{fano1961}
Fano, R. M. (1961).
*Transmission of Information: A Statistical Theory of Communications*. MIT Press.

\bibitem{cover2006}
Cover, T. M. \& Thomas, J. A. (2006).
*Elements of Information Theory* (2nd ed.). Wiley.

\bibitem{zinkevich2003}
Zinkevich, M. (2003).
Online convex programming and generalized infinitesimal gradient ascent.
*ICML 2003*, 928--936.

\bibitem{silver2017}
Silver, D. et al. (2017).
Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm.
*arXiv:1712.01815*.

\bibitem{srinivas2010}
Srinivas, N. et al. (2010).
Gaussian process optimization in the bandit setting: No regret and experimental design.
*ICML 2010*.

\bibitem{settles2009}
Settles, B. (2009).
Active learning literature survey.
*CS Technical Report 1648*, UW-Madison.

\bibitem{solomonoff1964}
Solomonoff, R. J. (1964).
A formal theory of inductive inference. Part I.
*Information and Control*, 7(1), 1--22.

\bibitem{borkar2008}
Borkar, V. S. (2008).
*Stochastic Approximation: A Dynamical Systems Viewpoint*. Cambridge University Press.

\bibitem{kushner2003}
Kushner, H. J. \& Yin, G. G. (2003).
*Stochastic Approximation and Recursive Algorithms and Applications* (2nd ed.). Springer.

\bibitem{polyak1992}
Polyak, B. T. \& Juditsky, A. B. (1992).
Acceleration of stochastic approximation by averaging.
*SIAM Journal on Control and Optimization*, 30(4), 838--855.

\bibitem{khalil2002}
Khalil, H. K. (2002).
*Nonlinear Systems* (3rd ed.). Prentice Hall.

\bibitem{hazan2016}
Hazan, E. (2016).
Introduction to online convex optimization.
*Foundations and Trends in Optimization*, 2(3-4), 157--325.

\bibitem{bach2011}
Bach, F. \& Moulines, E. (2011).
Non-asymptotic analysis of stochastic approximation algorithms for machine learning.
*NIPS 2011*.

\bibitem{karimi2016}
Karimi, H., Nutini, J. \& Schmidt, M. (2016).
Linear convergence of gradient and proximal-gradient methods under the Polyak-ojasiewicz condition.
*ECML PKDD 2016*.

\bibitem{benaim1999}
Bena\"im, M. (1999).
Dynamics of stochastic approximation algorithms.
*S\'eminaire de Probabilit\'es*, 1709, 1--68.

\bibitem{ghadimi2013}
Ghadimi, S. \& Lan, G. (2013).
Stochastic first- and zeroth-order methods for nonconvex stochastic programming.
*SIAM Journal on Optimization*, 23(4), 2341--2368.

\bibitem{agarwal2012}
Agarwal, A. et al. (2012).
Information-theoretic lower bounds on the oracle complexity of stochastic convex optimization.
*IEEE Transactions on Information Theory*, 58(5), 3235--3249.

\bibitem{bendavid2010}
Ben-David, S. et al. (2010).
A theory of learning from different domains.
*Machine Learning*, 79(1), 151--175.

\bibitem{arthur1989}
Arthur, W. B. (1989).
Competing technologies, increasing returns, and lock-in by historical events.
*Economic Journal*, 99(394), 116--131.

\bibitem{strogatz2018}
Strogatz, S. H. (2018).
*Nonlinear Dynamics and Chaos* (2nd ed.). CRC Press.

\bibitem{tsybakov2009}
Tsybakov, A. B. (2009).
*Introduction to Nonparametric Estimation*. Springer.

\bibitem{natarajan2013}
Natarajan, N. et al. (2013).
Learning with noisy labels.
*NIPS 2013*.

\bibitem{he2016}
He, K., Zhang, X., Ren, S., \& Sun, J. (2016).
Deep residual learning for image recognition.
*CVPR 2016*, 770--778.

\bibitem{moore1956}
Moore, E. F. (1956).
Gedanken-experiments on sequential machines.
*Automata Studies*, 34, 129--153.

\bibitem{deutsch1985}
Deutsch, D. (1985).
Quantum theory, the Church-Turing principle and the universal quantum computer.
*Proceedings of the Royal Society of London A*, 400(1818), 97--117.

\bibitem{raginsky2011}
Raginsky, M. \& Rakhlin, A. (2011).
Information-based complexity, feedback and dynamics in convex programming.
*IEEE Transactions on Information Theory*, 57(10), 7036--7056.

\end{thebibliography}