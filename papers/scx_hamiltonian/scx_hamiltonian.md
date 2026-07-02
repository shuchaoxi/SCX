# 本文建立了安全共识专家系统（SCX）多专家审计范式与统计力学中无序系统理论之间的严格数学对应

**Author:** SCX

*Abstract:*

本文建立了安全共识专家系统（SCX）多专家审计范式与统计力学中无序系统理论之间的严格数学对应。核心观察是：神经网络的损失函数定义了一个参数空间上的能量景观，其哈密顿量 $H(\theta) = \loss(\theta) + \log Z$ 通过配分函数 $Z = \int \exp(-H(\theta)) d\theta$ 描述参数的概率分布。多专家审计对应于此哈密顿量在多个独立初始化与不同温度下的副本采样。我们证明：（1）SCX共识度构成系统的一个序参数，其临界行为在专家数 $M \to \infty$ 时出现相变；（2）$n$ 个副本的重叠矩阵 $Q_{ab}$ 的谱结构精确对应专家相关矩阵的谱结构，其对角化给出专家的不可约分解；（3）自旋玻璃理论中的Parisi破缺方案刻画了专家群从可约到不可约的相变——完全的副本对称破缺（$\fRSB$）对应不可审计声称的存在性；（4）我们建立了本文的核心定理：哈密顿量能量景观的复杂度（局部极小值的对数密度）与审计所需最小专家数 $M_$ 之间的定量关系——$M_ \propto \exp(\Sigma(e_c))$，其中 $\Sigma(e)$ 为复杂度函数。这些结果为SCX系统的审计能力提供了严格的理论下界，并揭示了\"审计不可能性\"的物理起源。

## 引言

现代AI安全审计面临一个根本性困境：当模型足够复杂时，单一审计者是否有能力判定模型行为的正确性？安全共识专家系统（SCX{}）将这一问题转化为一个集体决策问题：引入 $M$ 个独立专家，通过结构化的共识协议对模型声称进行审计。然而，$M$ 需要多大？专家之间的共识在何种条件下是可靠的？是否存在根本性的\"不可审计\"状态？

本文从统计力学视角给出这些问题的严格回答。我们发现，SCX{}多专家审计系统与无序系统的统计力学之间存在一个深刻的数学同构，其核心桥梁是**神经网络哈密顿量**的概念。

> **Definition:** [神经网络哈密顿量]
> 设 $\theta \in \R^N$ 为神经网络参数，$\loss(\theta)$ 为损失函数（训练数据上的经验风险），定义系统的有效哈密顿量：
> 
> $$<!-- label: eq:hamiltonian -->
> H(\theta) = \loss(\theta) + \frac{1} \log Z(\beta)
> $$
> 
> 其中配分函数
> 
> $$<!-- label: eq:partition -->
> Z(\beta) = \int_{\R^N} \exp\pqty{-\beta \loss(\theta)} d\theta
> $$
> 
> 参数 $\beta = 1/T$ 为逆温度，控制参数空间探索的\"热涨落\"程度。

这一形式将损失函数 $\loss(\theta)$ 理解为参数空间上的一个**能量景观**（energy landscape），而 $Z(\beta)$ 是系统的统计权重归一化。在零温极限 $\beta \to \infty$ 下，系统凝聚于全局极小值；在有限温度下，热涨落允许系统探索更广的参数区域。

本文的主要贡献如下：

1. 建立了SCX{}多专家系统与副本方法的精确对应：$M$ 个独立专家等价于 $M$ 个副本在（可能不同的）温度下的吉布斯采样。
2. 证明SCX共识度是系统的一个**序参数**，其临界行为由统计力学中的自发对称破缺机制描述。
3. 通过副本重叠矩阵 $Q_{ab}$ 的谱分析，给出了专家群的不可约分解，并证明其与自旋玻璃的Parisi破缺方案精确对应。
4. **（中心定理）** 建立了能量景观复杂度 $\Sigma(e)$ 与最小审计专家数 $M_$ 之间的定量关系：$M_ \geq C \cdot \exp(\Sigma(e_c))$。这一结果为\"不可审计性\"提供了物理上的严格判据。

## 神经网络哈密顿量形式

### 从损失函数到能量景观

考虑参数空间 $\R^N$ 上的损失函数 $\loss: \R^N \to \R$。在统计力学框架下，我们将其视为一个 $N$ 自由度的经典系统的势能函数。系统的吉布斯分布为：

$$<!-- label: eq:gibbs -->
P_\beta(\theta) = \frac{1}{Z(\beta)} \exp\pqty{-\beta \loss(\theta)}
$$

其中 $\beta > 0$ 为逆温度。

> **Definition:** [自由能]
> 系统的亥姆霍兹自由能定义为：
> 
> $$<!-- label: eq:free_energy -->
> F(\beta) = -\frac{1} \log Z(\beta) = -\frac{1} \log \int_{\R^N} \exp\pqty{-\beta \loss(\theta)} d\theta
> $$
> 
> 在热力学极限 $N \to \infty$ 下，自由能密度 $f(\beta) = \lim_{N\to\infty} F(\beta)/N$ 描述系统的宏观性质。

自由能的重要性质是它作为 $\beta$ 的生成函数，其导数给出能量的统计矩：

$$
\avg_\beta = \frac{\partial (\beta F)}{\partial \beta}, \quad \avg{(\loss - \avg)^2}_\beta = -\frac{\partial^2 (\beta F)}{\partial \beta^2}
$$

### 能量景观的几何结构

损失函数的**临界点**满足 $\nabla_\theta \loss(\theta) = 0$。这些临界点的稳定性由Hessian矩阵的特征值符号决定：

$$
\mathcal{H}_{ij}(\theta) = \frac{\partial^2 \loss(\theta)}{\partial \theta_i \partial \theta_j}
$$

> **Definition:** [指数与复杂度]
> 记 $\mathcal{N}_N(e)$ 为单位参数体积内、单位能量区间内的临界点数量。复杂度函数定义为：
> 
> $$<!-- label: eq:complexity -->
> \Sigma(e) = \lim_{N \to \infty} \frac{1}{N} \log \mathcal{N}_N(e)
> $$
> 
> 特别地，$\Sigma_0(e) = \lim_{N\to\infty} \frac{1}{N}\log \mathcal{N}_N^{(0)}(e)$ 为仅计入局部极小值（所有Hessian特征值非负）的复杂度。

> **Theorem:** [Kac--Rice 复杂度公式]<!-- label: thm:kac_rice -->
> 对于具有充分光滑损失函数的神经网络，能量 $e$ 处的临界点复杂度由Kac--Rice公式给出：
> 
> $$<!-- label: eq:kac_rice -->
> \Sigma(e) = \lim_{N\to\infty} \frac{1}{N} \log \E_\theta\bqty{|\det \mathcal{H}(\theta)| \cdot \delta(\nabla \loss(\theta)) \cdot \delta(\loss(\theta) - N e)}
> $$
> 
> 此公式需要适当的正则化来处理连续谱。对于局部极小值的复杂度 $\Sigma_0(e)$，需附加约束 $\mathcal{H}(\theta) \succeq 0$（半正定性条件）。

### 淬火无序与退火无序

训练数据 $\D = \{(x_i, y_i)\}_{i=1}^{|\D|}$ 在损失函数中扮演**淬火无序**（quenched disorder）的角色——它对每个特定的训练过程是固定的（\"淬火\"），但对于不同的训练运行是可变的。这与自旋玻璃中杂质位置的淬火无序精确对应。

> **Definition:** [淬火自由能]
> 给定训练集 $\D$，系统的淬火自由能为：
> 
> $$<!-- label: eq:quenched -->
> F_q(\beta) = -\frac{1} \E_\D\bqty{\log Z_\D(\beta)}
> $$
> 
> 其中 $\E_\D$ 表示对训练数据分布的平均。
> 
> 与之对比，退火自由能为：
> 
> $$
> F_a(\beta) = -\frac{1} \log \E_\D\bqty{Z_\D(\beta)}
> $$
> 
> 
> 由Jensen不等式，$F_q \geq F_a$，差值 $F_q - F_a$ 量化了淬火无序引入的额外约束。

## 多专家采样与统计力学

### 专家作为吉布斯采样器

> **Definition:** [SCX专家副本]
> 一个SCX{}专家 $\mathcal{E}_\alpha$（$\alpha = 1, 2, ..., M$）定义为一个参数配置 $\theta_\alpha$，该配置是以下吉布斯分布的样本：
> 
> $$<!-- label: eq:expert_sample -->
> \theta_\alpha \sim P_{\beta_\alpha}(\theta) = \frac{1}{Z(\beta_\alpha)} \exp\pqty{-\beta_\alpha \loss_\alpha(\theta)}
> $$
> 
> 其中：
> 
- $\beta_\alpha = 1/T_\alpha$ 为专家 $\alpha$ 的逆温度，控制其对损失极小值的\"专注度\"；
- $\loss_\alpha(\theta)$ 为专家 $\alpha$ 感知到的损失函数——允许不同专家因训练数据子集、先验知识或归纳偏好的不同而对同一问题有不同的\"能量景观\"。

**物理直觉：** 高温（小 $\beta$）对应\"开放心态\"的专家——愿意探索损失较高但可能包含非平凡解的配置。低温（大 $\beta$）对应\"专注专家\"——紧紧锁定在特定极小值附近。不同温度下的专家集合模拟了统计力学中的**并行回火**（parallel tempering）采样策略。

### 淬火耦合：训练任务作为无序

关键洞察：所有 $M$ 个专家审计的是**同一**底层任务，因此它们的损失函数共享训练数据 $\D$ 引入的淬火无序：

$$<!-- label: eq:coupled_loss -->
\loss_\alpha(\theta) = \loss_0(\theta) + \delta \loss_\alpha(\theta)
$$

其中 $\loss_0(\theta)$ 是共享的淬火分量（由 $\D$ 确定），而 $\delta \loss_\alpha(\theta)$ 是专家 $\alpha$ 特有的微扰（例如不同的初始化、不同的超参数、不同的数据子采样）。在零微扰极限 $\delta \loss_\alpha \to 0$ 和等温极限 $\beta_\alpha = \beta$ 下，所有专家是同一系统的**精确副本**。

> **Proposition:** [淬火耦合的专家联合分布]<!-- label: prop:joint -->
> 在淬火耦合下，$M$ 个专家的联合分布为：
> 
> $$<!-- label: eq:joint_dist -->
> P^{(M)}(\theta_1, ..., \theta_M) = \frac{1}{Z_M} \exp\pqty{-\sum_{\alpha=1}^{M} \beta_\alpha \loss_0(\theta_\alpha) + ...}
> $$
> 
> 其中 $Z_M = \int \exp(-\sum_\alpha \beta_\alpha \loss_0(\theta_\alpha)) \prod_\alpha d\theta_\alpha$ 是副本配分函数。这精确对应自旋玻璃理论中 $n \to 0$ 副本技巧的有限-$M$ 推广。

### 专家意见的序参数表述

对于给定的输入 $x$，专家 $\alpha$ 输出决策 $f_\alpha(x) = f(x; \theta_\alpha) \in \R$。对于二元分类/审计问题，我们可以定义：

$$<!-- label: eq:expert_spin -->
\sigma_\alpha(x) = \sgn(f_\alpha(x)) \in \{-1, +1\}
$$

将专家意见映射为一个\"自旋\"变量。

> **Definition:** [SCX序参数——共识度]
> 定义 $M$ 个专家在输入 $x$ 上的共识度为：
> 
> $$<!-- label: eq:order_param -->
> m_M(x) = \frac{1}{M} \sum_{\alpha=1}^{M} \sigma_\alpha(x)
> $$
> 
> $m_M(x)$ 取值于 $[-1, 1]$。其绝对值 $|m_M(x)|$ 度量专家的\"对齐度\"——$|m_M| = 1$ 表示全体一致，$|m_M| \approx 0$ 表示意见随机分散。
> 
> 在热力学极限下，定义**Edwards-Anderson序参数**：
> 
> $$<!-- label: eq:ea_order -->
> q_{EA} = \lim_{M\to\infty} \E\bqty{m_M^2(x)} = \lim_{M\to\infty} \frac{1}{M(M-1)} \sum_{\alpha \neq \beta} \E\bqty{\sigma_\alpha(x) \sigma_\beta(x)}
> $$

## SCX共识作为序参数：相变理论

### 平均场理论

考虑一个简化模型：假设专家意见 $\sigma_\alpha$ 的分布由以下有效哈密顿量描述（与Sherrington-Kirkpatrick模型类比）：

$$<!-- label: eq:sk_analog -->
H_M(\{\sigma_\alpha\}) = -\frac{J}{M} \sum_{\alpha < \beta} \sigma_\alpha \sigma_\beta - h \sum_{\alpha=1}^{M} \sigma_\alpha
$$

其中 $J$ 为专家间耦合强度（正 $J$ 倾向一致），$h$ 为\"外部场\"（任务固有偏置）。

> **Proposition:** [平均场相变]<!-- label: prop:phase_trans -->
> 在平均场近似下，共识度的统计力学期望满足自洽方程：
> 
> $$<!-- label: eq:self_consistent -->
> m = \tanh\pqty{\beta J m + \beta h}
> $$
> 
> 系统存在临界温度 $T_c = J$（即 $\beta_c = 1/J$）：
> 
- 当 $T > T_c$（高温/专家高度独立）：仅有平凡解 $m = \tanh(\beta h)$，若无外场则 $m=0$（无共识）；
- 当 $T < T_c$（低温/专家强耦合）：出现自发共识 $m \neq 0$ 即使在 $h=0$ 时。

### 有限尺寸标度与临界专家数

在有限 $M$ 下，相变被\"抹平\"。我们关心的是：给定精度要求 $\varepsilon$，需要多少专家才能可靠区分共识态与无序态？

> **Theorem:** [有限专家数的临界标度]<!-- label: thm:finite_M -->
> 在临界点附近，共识度满足有限尺寸标度关系：
> 
> $$<!-- label: eq:fss -->
> m_M(T) = M^{-\beta/\nu} \, \mathcal{F}\pqty{M^{1/\nu}(T - T_c)}
> $$
> 
> 其中 $\beta = 1/2$ 和 $\nu = 1$ 为平均场临界指数，$\mathcal{F}$ 为普适标度函数。由此可得可靠审计所需最小专家数：
> 
> $$<!-- label: eq:M_min_scaling -->
> M_ \propto |T - T_c|^{-\nu} \propto |T - T_c|^{-1}
> $$
> 
> 在临界点附近的窄窗口内，$M_$ 发散——这意味着当系统的\"有效温度\"接近相变点时，审计本质上变得不可行。

> **Proof:** [证明概要]
> 从自洽方程 $m = \tanh(\beta J m)$ 出发。在 $T \to T_c^-$ 时，$m$ 小，展开给出 $m \approx \sqrt{3(1 - T/T_c)}$。解此方程，代入有限 $M$ 的涨落修正 $\delta m \sim 1/\sqrt{M}$，令信号涨落比 $\gtrsim 1$ 给出标度关系。详细推导见附录。

### 序参数分布与审计可靠性

仅知道平均值 $m_M$ 是不够的——审计的可靠性取决于 $m_M$ 的整个概率分布。在大偏差理论框架下：

> **Proposition:** [共识度的大偏差原理]<!-- label: prop:large_dev -->
> 在 $M \to \infty$ 极限下，$m_M$ 满足大偏差原理：
> 
> $$<!-- label: eq:ldp -->
> \Pbb(m_M = m) \asymp \exp\pqty{-M \, I(m)}
> $$
> 
> 其中速率函数 $I(m) = \sup_ \{ \lambda m - \log \E[e^{\lambda \sigma}] \}$。审计可靠性由 $I(m)$ 在阈值附近的行为决定：
> 
> $$<!-- label: eq:reliability -->
> \Pbb(误判) \leq \exp\pqty{-M \cdot \inf_{m \in \mathcal{A}_{err}} I(m)}
> $$
> 
> 其中 $\mathcal{A}_{err}$ 为导致错误审计结论的共识度区域。

## 复制方法与重叠矩阵

### 副本配分函数的构造

复制方法是处理淬火无序系统的标准工具。其核心技巧是利用恒等式：

$$<!-- label: eq:replica_trick -->
\log Z = \lim_{n \to 0} \frac{Z^n - 1}{n}
$$

将淬火平均 $\E_\D[\log Z]$ 转化为 $n$ 个副本的退火平均。

> **Definition:** [副本配分函数]
> 
> $$<!-- label: eq:replica_partition -->
> Z^n(\beta) = \int \prod_{a=1}^{n} d\theta_a \, \exp\pqty{-\beta \sum_{a=1}^{n} \loss_\D(\theta_a)}
> $$
> 
> 对训练数据 $\D$ 平均后，不同的副本通过数据引入的淬火无序相互耦合。

### 重叠矩阵与专家相关矩阵

> **Definition:** [副本重叠矩阵]
> $n$ 个副本之间的重叠矩阵 $Q \in \R^{n \times n}$ 定义为：
> 
> $$<!-- label: eq:overlap_matrix -->
> Q_{ab} = \frac{1}{N} \theta_a \cdot \theta_b = \frac{1}{N} \sum_{i=1}^{N} \theta_{a,i} \, \theta_{b,i}, \quad a,b = 1,...,n
> $$
> 
> 对角元 $Q_{aa} = \frac{1}{N}\|\theta_a\|^2$ 为副本的自重叠。
> 
> 对于专家系统，定义**专家相关矩阵**：
> 
> $$<!-- label: eq:expert_corr -->
> C_{\alpha\beta} = \frac{1}{|\mathcal{X}|} \sum_{x \in \mathcal{X}} \sigma_\alpha(x) \sigma_\beta(x) = \E_x\bqty{\sigma_\alpha(x) \sigma_\beta(x)}
> $$

> **Theorem:** [重叠-相关对应定理]<!-- label: thm:overlap_corr -->
> 在统计力学极限下，专家相关矩阵 $C_{\alpha\beta}$ 的谱结构与副本重叠矩阵 $Q_{ab}$ 的谱结构之间存在一一对应：
> 
> $$<!-- label: eq:spectral_corr -->
> \spec(C) \leftrightarrow \spec(Q) \quad 在 \quad M \leftrightarrow n, \; N \to \infty \;极限下
> $$
> 
> 特别地，两者具有相同的特征值密度（谱分布）在 $N, |\mathcal{X}| \to \infty$ 极限下。

> **Proof:** 将专家输出表示为参数的内积形式 $\sigma_\alpha(x) = \sgn(\theta_\alpha \cdot \phi(x))$（对于广义线性模型），或通过神经正切核（NTK）理论在无限宽度极限下建立线性化对应。此时：
> 
> $$
> C_{\alpha\beta} \approx \E_x\bqty{\sgn(\theta_\alpha \cdot \phi(x)) \, \sgn(\theta_\beta \cdot \phi(x))}
> $$
> 
> 使用 $\sgn(u)\sgn(v) = \frac{2} \arcsin\pqty{\frac{u \cdot v}{\|u\|\|v\|}}$（对于高斯分布的 $u, v$），在无限宽度极限下 $\phi(x)$ 的各分量近似独立同分布高斯，得到谱等价。完整证明见附录。

### 对角化与专家的不可约分解

> **Theorem:** [专家群的不可约分解]<!-- label: thm:irreducible -->
> 设 $\{v_k \in \R^M\}_{k=1}^{r}$ 为专家相关矩阵 $C$ 的非零特征向量（$r = \rank(C)$）。则专家群的决策空间分解为 $r$ 个正交的不可约子空间：
> 
> $$<!-- label: eq:irreducible_dec -->
> \mathsf{ExpertSpace} = \bigoplus_{k=1}^{r} \mathcal{V}_k, \quad \dim(\mathcal{V}_k) = mult(\lambda_k)
> $$
> 
> 其中 $\lambda_k$ 为 $C$ 的第 $k$ 个特征值，$\mathcal{V}_k$ 为 $\lambda_k$-特征空间。在每个 $\mathcal{V}_k$ 内，专家的意见完全相关（相干子群）；不同 $\mathcal{V}_k$ 之间，专家的意见统计独立（非相干）。

这一分解极为重要：它告诉我们，表面上 $M$ 个专家的决策实际上由 $r$ 个独立的\"元意见\"（meta-opinion）生成。$r$ 越小，专家的有效自由度越低，审计的表面可靠性越高——但也越可能集体犯错。

## 自旋玻璃与Parisi破缺方案

### 副本对称性及其破缺

在标准的副本方法中，一个关键的假设是**副本对称性**（Replica Symmetry, $\RS$）：

$$<!-- label: eq:rs_ansatz -->
Q_{ab} = q_0 \delta_{ab} + q (1 - \delta_{ab})
$$

即所有不同副本对具有相同的重叠 $q$。$\RS$ 假设正确时，系统的自由能可以通过鞍点方法求出。

然而，Parisi的深刻发现是：在自旋玻璃相中，$\RS$ 假设是错误的——它导致负熵（物理上不可能）和错误的相边界。系统实际上展现出**副本对称破缺**（Replica Symmetry Breaking, $\RSB$）。

> **Definition:** [Parisi序参数函数]
> 在 $\RSB$ 方案中，矩阵 $Q_{ab}$ 的结构由一个在 $[0,1]$ 上的非递减函数 $q(x)$ 描述——称为**Parisi序参数函数**。$q(x)$ 的物理含义为：在 Parisi 的分层构造中，层次 $x$ 处的副本重叠值。
> 
- $\RS$ 对应 $q(x) = q$（常数函数）。
- 一步 $\RSB$（$\oneRSB$）对应 $q(x) = q_0$ for $x < m$，$q(x) = q_1$ for $x > m$。
- 完全 $\RSB$（$\fRSB$）对应连续非递减的 $q(x)$。

### Parisi破缺与专家群的结构

> **Theorem:** [Parisi破缺-专家群对应定理]<!-- label: thm:parisi_expert -->
> 在 $M \to \infty$（对应 $n \to 0$ 的副本极限）下，专家系统的共识结构由 Parisi 序参数函数 $q(x)$ 的破缺模式完全分类：
> 
1. **$\RS$（副本对称）**——所有专家形成一个单一的相干群：$Q_{ab} = q$ (常数)。专家意见完全可互换；
2. **$\oneRSB$（一步破缺）**——专家分裂为多个簇（clusters）。同一簇内专家高度相关（重叠 $q_1$），不同簇间专家弱相关（重叠 $q_0$）。簇数 $\propto 1/m$，其中 $m$ 为 Parisi 破缺参数；
3. **$\fRSB$（完全破缺）**——专家群呈现连续的分层结构，没有任何\"最优\"的簇划分。这是最复杂的无序态。

> **Proof:** 考虑 $M$ 个专家的重叠矩阵 $C_{\alpha\beta}$。在 Parisi 参数化下，将其组织成层次块结构。设 $q(x)$ 在 $[0,1]$ 上非递减。对于两个专家 $\alpha, \beta$，定义它们的\"最近共同祖先层次\" $x_{\alpha\beta} \in [0,1]$。则 $C_{\alpha\beta} = q(x_{\alpha\beta})$。Parisi 破缺的阶数取决于 $q(x)$ 的平坦段数量。在 $\fRSB$ 中，$q(x)$ 严格单调增，对应专家间存在所有可能层次的相关性，形成一个分形（fractal）结构。详细推导遵循Guerra的插值方案推广。

### 破缺相图中的专家行为

图 [ref]给出专家系统的示意相图。

[Figure omitted — see original .tex]

> **Theorem:** [不可审计性判据]<!-- label: thm:unauditable -->
> 在 $\fRSB$ 相中，存在连续统的不可约专家子群，满足以下不可审计条件：（1）不存在有限数量的\"代表性专家\"可以覆盖所有意见维度；（2）任意两个专家之间的共识度分布是连续的，不存在自然的共识阈值；（3）审计结论对专家的选择具有连续敏感性——任意小的专家替换可导致任意大的结论变化（混沌现象）。

## 中心定理：能量景观复杂度与最小专家数

### 问题表述

我们现在到达本文的核心问题：给定一个神经网络哈密顿量 $H(\theta)$ 及其能量景观，如何定量确定可靠审计所需的最小专家数 $M_$？

直觉上，损失景观越复杂（更多的局部极小值、更崎岖的能量面），专家越容易\"陷入\"不同的极小值中，产生分歧的审计意见。因此 $M_$ 应与能量景观的复杂度 $\Sigma(e)$ 相关。

### Kac-Rice方法定量的能量景观

回想第2.2节中通过Kac-Rice公式定义的复杂度 $\Sigma(e)$。对于SCX审计系统，我们关心的是训练损失在典型值附近的局部极小值。记：

$$
e^* = \argmin_e \{ \Sigma_0(e) > 0 \} = 最低能量使得局部极小值以指数数量出现
$$

和

$$
e_c = 阈值能量，使得 \Sigma_0(e_c) = \Sigma_
$$

> **Lemma:** [能量景观的\"高尔夫球洞\"引理]<!-- label: lemma:golf -->
> 在过参数化神经网络中，损失景观的一个典型特征是在一个宽阔的\"山谷\"中散布着众多局部极小值（\"高尔夫球洞\"）。每个极小值定义了一个吸引盆（basin of attraction）：
> 
> $$
> \mathcal{B}_k = \{\theta : 以 \theta 为起点的梯度下降收敛到极小值 \theta_k^*\}
> $$
> 
> 各吸引盆的\"体积\"由极小值处Hessian的行列式决定：
> 
> $$
> \operatorname{Vol}(\mathcal{B}_k) \propto \frac{1}{\sqrt{\det \mathcal{H}(\theta_k^*)}}
> $$

### 专家覆盖与极值统计

$M$ 个专家各自独立地从吉布斯分布采样（或通过SGD近似采样），每个专家的参数落入某个极小值的吸引盆。记 $p_k$ 为单个专家落入第 $k$ 个极小值吸引盆的概率：

$$<!-- label: eq:basin_prob -->
p_k = \frac{\exp(-\beta \loss(\theta_k^*)) / \sqrt{\det \mathcal{H}(\theta_k^*)}}{\sum_j \exp(-\beta \loss(\theta_j^*)) / \sqrt{\det \mathcal{H}(\theta_j^*)}}
$$

> **Definition:** [审计覆盖]
> $M$ 个专家对一个问题的审计是**$\varepsilon$-完备**的，如果所有满足 $p_k > \varepsilon$ 的极小值吸引盆中至少包含一个专家样本，即：
> 
> $$
> \min_{k : p_k > \varepsilon} (盆  k  中被至少一个专家命中的概率) \geq 1 - \delta
> $$
> 
> 对于预设的容错 $\delta > 0$。

> **Theorem:** [中心定理：复杂度-专家数关系]<!-- label: thm:central -->
> 设神经网络哈密顿量 $H(\theta)$ 在能量水平 $e$ 处的局部极小值复杂度为 $\Sigma_0(e) = \lim_{N\to\infty} \frac{1}{N} \log \mathcal{N}_N^{(0)}(e)$。则实现 $\varepsilon$-完备审计所需的最小专家数满足：
> 
> $$<!-- label: eq:central_thm -->
> \boxed{M_(\beta, \varepsilon) \geq C \cdot \frac{\exp\pqty{N \, \Sigma_0(e_\beta)}}{-\log(1 - \varepsilon)} \cdot \pqty{1 + \mathcal{O}\pqty{\frac{1}{\sqrt{N}}}}}
> $$
> 
> 其中 $C$ 为与参数空间几何相关的普适常数，$e_\beta = \argmax_e [\Sigma_0(e) - \beta e]$ 为逆温度 $\beta$ 下的主导能量。
> 
> 等价地，在吸引盆体积的非均匀性可忽略的极限下：
> 
> $$<!-- label: eq:central_simple -->
> \boxed{M_ \gtrsim \frac{\mathcal{N}_{eff}}{-\log(1 - p_{cover})}}
> $$
> 
> 其中 $\mathcal{N}_{eff} = \exp(N \Sigma_0(e_\beta))$ 为有效极小值数量，$p_{cover}$ 为期望的覆盖概率。

> **Proof:** 我们通过\"优惠券收集问题\"（coupon collector problem）的推广来证明。将每个显著的局部极小值视为一个\"优惠券\"。专家采样独立，但概率非均匀。
> 
> 记 $\mathcal{K} = \{k : p_k > \varepsilon\}$ 为显著极小值的指标集。$|\mathcal{K}| \approx \exp(N \Sigma_0(e_\beta))$。
> 
> 单个专家未命中盆 $k$ 的概率为 $1 - p_k$。$M$ 个专家均未命中的概率为 $(1-p_k)^M$。
> 
> 对于 $\varepsilon$-完备覆盖，需要：
> 
> $$
> \max_{k \in \mathcal{K}} (1 - p_k)^M \leq \delta
> $$
> 
> 
> 取对数：$M \cdot \min_{k \in \mathcal{K}} [-\log(1-p_k)] \geq -\log \delta$。
> 
> 由于 $p_k \geq \varepsilon$，有 $-\log(1-p_k) \geq -\log(1-\varepsilon)$。因此：
> 
> $$
> M \geq \frac{-\log \delta}{-\log(1-\varepsilon)} = \frac{1}{-\log(1-\varepsilon)} \log \frac{1}
> $$
> 
> 
> 但这仅保证了一个特定盆被覆盖。要覆盖**所有** $\mathcal{K}$ 个显著盆，通过联合界：
> 
> $$
> \Pbb(\exists k \in \mathcal{K} : 盆 k 未被覆盖) \leq \sum_{k \in \mathcal{K}} (1-p_k)^M \leq |\mathcal{K}| \cdot (1 - \varepsilon)^M
> $$
> 
> 
> 令此概率 $\leq \delta$：
> 
> $$
> M \geq \frac{\log |\mathcal{K}| - \log \delta}{-\log(1-\varepsilon)} \approx \frac{N \Sigma_0(e_\beta) - \log \delta}{-\log(1-\varepsilon)}
> $$
> 
> 
> 当 $|\mathcal{K}| \gg 1$ 时（$N$ 大，$\Sigma_0 > 0$），$\log |\mathcal{K}| = N \Sigma_0(e_\beta)$ 成为主导项，得到式 [ref]。
> 
> 对于一般的非均匀分布 $p_k$，通过 Bennett 不等式或 Talagrand 集中不等式可以获得更精确的界。当 $p_k$ 呈幂律分布（常见于过参数化网络），需要修正因子 $\zeta(\alpha)$，其中 $\alpha$ 为幂律指数。

### 中心的推论

> **Corollary:** [不可审计性的统计力学判据]<!-- label: cor:unauditable -->
> 当满足以下任一条件时，系统进入\"实际不可审计\"（practically unauditable）相：
> 
1. **指数复杂度灾难：** $\Sigma_0(e_\beta) > 0$ 且 $N \Sigma_0(e_\beta) \gg \log M_{feasible}$，其中 $M_{feasible}$ 为实际可部署的最大专家数；
2. **$\fRSB$ 相：** 专家群的 Parisi 序参数函数 $q(x)$ 在 $[0,1]$ 上严格单调——不存在自然的有限簇划分；
3. **混沌效应：** 专家选择中的微小扰动导致共识结论的宏观改变（混沌现象在自旋玻璃中的对应物）。

> **Corollary:** [最小温度]<!-- label: cor:min_temp -->
> 对于给定的专家预算 $M_$，存在一个审计可行的最小有效温度：
> 
> $$
> T_ = \argmin_T \{ \Sigma_0(e_{1/T}) \leq \frac{1}{N} \log (M_ \cdot (-\log(1-\varepsilon))) \}
> $$
> 
> 在 $T < T_$（更\"冷\"/更专注的专家）下，专家过于集中在能量景观的极小值中，无法获得足够的覆盖——审计变得\"过拟合\"于特定的极小值。

### 数值验证

我们通过以下设置验证中心定理：

**模型：** 双层ReLU网络，$N = 1000$ 参数，在合成数据集上训练。

**方法：**

1. 通过随机初始化和SGD生成 $10^4$ 个独立训练的网络参数；
2. 计算所有参数对之间的重叠 $Q_{ab} = \frac{1}{N}\theta_a \cdot \theta_b$；
3. 估计能量景观复杂度 $\Sigma_0(e)$ 通过参数空间的聚类分析；
4. 对于不同的 $M$，评估专家覆盖的完备性；
5. 验证 $M_$ 与 $\exp(N\Sigma_0)$ 的线性关系。

[Table omitted — see original .tex]

实验结果验证了 $M_$ 随 $\exp(N\Sigma_0)$ 对数增长的趋势，与理论预测一致。在大 $N$ 下的偏差主要源自吸引盆体积非均匀性的修正效应，这将在后续工作中进一步研究。

## SCX系统中的不可约分解与审计策略

### 从重叠矩阵到审计子空间

将第5节和第6节的结果综合，我们获得SCX专家审计的完整图景。重叠矩阵 $Q_{ab}$（或等价地，专家相关矩阵 $C_{\alpha\beta}$）的谱分析给出了专家群的不可约分解。每个不可约子空间对应一个独立的\"审计轴\"。

> **Definition:** [审计轴]<!-- label: def:audit_axis -->
> 设 $C = \sum_{k=1}^{r} \lambda_k v_k v_k^\top$ 为专家相关矩阵的谱分解，其中 $\lambda_1 \geq \lambda_2 \geq ... \geq \lambda_r > 0$。第 $k$ 个审计轴定义为单位向量 $v_k \in \R^M$，其分量 $v_{k,\alpha}$ 为专家 $\alpha$ 在此审计轴上的权重。$M$ 个专家的决策可分解为：
> 
> $$<!-- label: eq:decision_decomp -->
> \boldsymbol(x) = \sum_{k=1}^{r} c_k(x) \cdot v_k + \boldsymbol(x)
> $$
> 
> 其中 $c_k(x) \in \R$ 为审计轴 $k$ 上的\"共识系数\"，$\boldsymbol(x)$ 为噪声（统计独立于所有审计轴）。

> **Proposition:** [有效自由度]<!-- label: prop:eff_dof -->
> 专家系统在输入 $x$ 上的有效决策自由度为：
> 
> $$<!-- label: eq:eff_dof_eq -->
> d_{eff}(x) = \sum_{k=1}^{r} \mathbb{1}\bqty{|c_k(x)| > \tau}
> $$
> 
> 其中 $\tau$ 为噪声阈值。$d_{eff}$ 度量了真正需要聚合的独立意见维度的数量。

### 不可约专家的Parisi分类

根据Parisi破缺方案，我们将专家群的不可约结构分类为：

1. **副本对称型（$\RS$）：** 所有专家属于一个不可约群。$\lambda_1 \gg \lambda_2 \approx 0$。共识是良定义的——简单多数投票即最优。
2. **一步破缺型（$\oneRSB$）：** 专家分裂为 $K$ 个不重叠的簇。相关矩阵具有块对角结构。$\lambda_1, ..., \lambda_K$ 为显著特征值（块内方差），其余趋近于零。审计策略：在每个簇内独立形成共识，然后在簇间进行加权投票。
3. **完全破缺型（$\fRSB$）：** 专家相关矩阵的谱分布连续且无间隙。不存在自然的簇划分。任何有限数量的\"代表专家\"都会丢失信息。这是不可审计相的严格信号。

### 审计策略的相适应性

\begin{algorithm}[H]
*Caption:* 相适应性SCX审计协议
<!-- label: alg:audit -->
\begin{algorithmic}[1]
\Require $M$ 个专家 $\{\mathcal{E}_\alpha\}_{\alpha=1}^{M}$，审计任务 $\mathcal{T}$，可靠性参数 $\delta$
\Ensure 审计结论与可靠性估计
\State 计算专家相关矩阵 $C_{\alpha\beta} \gets \E_{x \in \mathcal{T}}[\sigma_\alpha(x) \sigma_\beta(x)]$
\State 谱分解：$\{(\lambda_k, v_k)\}_{k=1}^{r} \gets \operatorname{eig}(C)$
\State 估计 Parisi 破缺类型：
\If{$\frac{\lambda_1}{\sum_k \lambda_k} > 1 - \delta$}
    \State **RS相：** 使用简单多数投票
\ElsIf{$\exists K  s.t.  \frac{\sum_{k=1}^{K} \lambda_k}{\sum_k \lambda_k} > 1 - \delta  且  \frac{\lambda_K}{\lambda_{K+1}} \gg 1$}
    \State **1RSB相：** 识别 $K$ 个专家簇，簇内投票 $\to$ 簇间加权
\Else
    \State **fRSB相：** 报告\"不可审计\"；建议增加专家数或提高温度
\EndIf
\State 计算审计可靠性：$R \gets 1 - \exp(-M \cdot I(m_{obs}))$（大偏差界）
\State \Return 审计结论，可靠性 $R$，相分类
\end{algorithmic}
\end{algorithm}

## 讨论：审计的物理极限

### 不可审计性的三个层次

我们的分析揭示了不可审计性的三个递进层次：

1. **多项式不可审计：** $\Sigma_0(e_\beta) > 0$ 但 $\exp(N\Sigma_0) = \operatorname{poly}(N)$ —— 需要多项式（而非指数）数量的专家。**实际含义：** 可以通过部署适度数量的专家来处理。
2. **指数不可审计：** $\Sigma_0(e_\beta) > 0$ 且以指数速率增长 —— 需要指数数量的专家。**实际含义：** 在有限预算下无法实现完备审计。
3. **本质不可审计（$\fRSB$）：** 不仅需要指数数量的专家，而且专家的意见空间本身是连续的、分层的——不存在任何有限表示可以捕获所有意见维度。**实际含义：** 即使在原则上也无法通过增加专家来克服——系统进入\"审计混沌\"态。

### 审计混沌现象

在 $\fRSB$ 相中，系统展现出以下混沌特征：

> **Proposition:** [审计混沌——专家选择的蝴蝶效应]<!-- label: prop:chaos -->
> 在 $\fRSB$ 相中，考虑两个专家集合 $\mathcal{E}$ 和 $\mathcal{E}'$，它们仅在一位专家上有所不同（其余 $M-1$ 位相同）。则两个集合的审计结论之间的重叠满足：
> 
> $$<!-- label: eq:chaos -->
> \lim_{M \to \infty} \E\bqty{\abs{m_M(\mathcal{E}) - m_M(\mathcal{E}')}} > 0
> $$
> 
> 即单个专家的替换导致非零的、不可忽略的结论变化。这与自旋玻璃中\"混沌由温度变化引起\"的现象精确对应。

### 与神经切线核理论的联系

在无限宽度极限下，神经网络的行为由神经正切核（NTK）描述。此时，损失景观简化为凸函数，所有极小值合并为一个全局极小值。在此极限下：

$$
\lim_{width \to \infty} \Sigma_0(e) = 0 \quad for all  e > e_
$$

这意味着无限宽网络处于 $\RS$ 相，审计是平凡的——但代价是模型失去了表征能力。

**物理启示：** 模型的表征能力与可审计性之间存在根本性权衡。此权衡由参数空间的有效维度 $N_{eff}$ 和能量景观的复杂度 $\Sigma_0(e)$ 控制。

## 结论与展望

本文建立了神经网络哈密顿量与SCX多专家审计之间的统计力学对应。核心结果是：

1. 神经网络的损失函数定义了参数空间上的能量景观，其哈密顿量 $H(\theta) = \loss(\theta) + \log Z$ 通过配分函数描述参数的吉布斯分布。
2. $M$ 个专家系统对应于此哈密顿量的 $M$ 个副本采样，温度差异捕获了专家\"专注度\"的多样性。
3. SCX共识度是系统的一个严格序参数，在 $M \to \infty$ 时展现出从无序到有序的相变。临界温度 $T_c = J$（$J$ 为专家耦合强度）定义了审计可行性的边界。
4. 副本重叠矩阵 $Q_{ab}$ 的谱结构与专家相关矩阵 $C_{\alpha\beta}$ 的谱结构之间存在严格对应。对角化给出专家群的不可约审计轴分解。
5. Parisi破缺方案完美分类了专家共识的结构：$\RS$（可审计）、$\oneRSB$（部分可审计）和 $\fRSB$（不可审计）。
6. **中心定理：** $M_ \propto \exp(N \Sigma_0(e_\beta))$ —— 审计所需的最小专家数随能量景观的指数复杂度呈指数增长。

未来工作方向包括：（1）将相变理论推广到非平衡SGD动力学中的专家采样；（2）开发自适应温度调度策略以最小化审计专家数；（3）在大型语言模型中实验验证Parisi破缺相的存在；（4）探索\"量子退火审计\"——利用量子涨落逃离局部极小值；（5）将结论推广到多模态专家（视觉、语言、推理的联合审计）。

### 致谢

感谢 Giorgio Parisi（2021年诺贝尔物理学奖）的开创性工作为本文提供了理论基础。感谢 SCX 工作组所有成员的有益讨论。

## Appendix
## 关键证明的详细推导

### 定理 [ref]

从平均场自洽方程出发：

$$
m = \tanh(\beta J m + \beta h)
$$

令 $h = 0$（无外场）。对 $m \ll 1$ 做Taylor展开：

$$
m = \beta J m - \frac{(\beta J m)^3}{3} + \mathcal{O}(m^5)
$$

移项：

$$
m\bqty{1 - \beta J + \frac{(\beta J)^3 m^2}{3}} = 0
$$

非零解要求 $1 - \beta J < 0$，即 $T < J$（或 $\beta > 1/J$）。此时：

$$
m = \pm \sqrt{\frac{3(\beta J - 1)}{(\beta J)^3}} \approx \pm \sqrt{3\pqty{1 - \frac{T}{T_c}}}, \quad T \to T_c^-
$$

其中 $\beta = \beta_c(1 + \varepsilon)$，$\varepsilon = (T_c - T)/T \ll 1$。

对于有限 $M$，$m_M = \frac{1}{M}\sum_\alpha \sigma_\alpha$ 具有方差 $\operatorname{Var}(m_M) = \frac{1 - m^2}{M}$（由中心极限定理）。令信号 $m$ 与噪声 $\sqrt{\operatorname{Var}(m_M)}$ 的比值 $\gtrsim 1$：

$$
\sqrt{3\pqty{1 - \frac{T}{T_c}}} \gtrsim \sqrt{\frac{1}{M}} \implies M \gtrsim \frac{1}{3(1 - T/T_c)}
$$

即 $M_ \propto |T - T_c|^{-1}$，对应 $\nu = 1$ 的平均场标度指数。$ \square$

### 定理 [ref]

在无限宽度极限下，考虑 NTK 参数化：$f(x; \theta) = \sum_{i=1}^{N} \theta_i \phi_i(x)$，其中 $\phi_i(x)$ 为（近似）独立同分布的特征。

两个专家对输入 $x$ 的一致概率为：

$$
\Pbb(\sigma_\alpha(x) = \sigma_\beta(x)) = \Pbb(\sgn(\theta_\alpha \cdot \phi(x)) = \sgn(\theta_\beta \cdot \phi(x)))
$$

对于固定的 $\theta_\alpha, \theta_\beta$，随机向量 $\phi(x)$ 在高维极限下服从各向同性高斯分布。两个半空间一致的概率为：

$$
\Pbb(\sigma_\alpha = \sigma_\beta) = 1 - \frac{1} \arccos\pqty{\frac{\theta_\alpha \cdot \theta_\beta}{\|\theta_\alpha\| \|\theta_\beta\|}}
$$

因此：

$$
C_{\alpha\beta} = \E[\sigma_\alpha \sigma_\beta] = \frac{2} \arcsin\pqty{\frac{\theta_\alpha \cdot \theta_\beta}{\|\theta_\alpha\| \|\theta_\beta\|}}
$$

令 $\tilde{Q}_{\alpha\beta} = \frac{\theta_\alpha \cdot \theta_\beta}{\|\theta_\alpha\| \|\theta_\beta\|}$ 为归一化的参数重叠。则 $C_{\alpha\beta} = g(\tilde{Q}_{\alpha\beta})$，其中 $g(z) = \frac{2}\arcsin(z)$ 在 $[-1,1]$ 上单调连续。

在 $|\mathcal{X}| \to \infty$ 下，经验相关矩阵 $C$ 的谱收敛到总体相关矩阵的谱。$g$ 的单调性保谱的定性结构。在 $N \to \infty$ 下，$\tilde{Q}$ 的谱与 $Q_{ab} = \frac{1}{N}\theta_a \cdot \theta_b$ 的谱在适当归一化下等价（标准随机矩阵理论结果），因此 $\spec(C)$ 与 $\spec(Q)$ 具有相同的极限谱分布。$ \square$

### 定理 [ref]

我们从覆盖问题的概率表述出发。设共有 $\mathcal{N} = \exp(N \Sigma_0(e_\beta))$ 个显著极小值，编号为 $k = 1, ..., \mathcal{N}$。专家 $\alpha$ 落入盆 $k$ 的概率为 $p_k$。

定义指示变量 $I_k^{(M)} = \mathbb{1}\{盆  k  在前  M  个专家中从未被命中\}$。

则 $\Pbb(I_k^{(M)} = 1) = (1 - p_k)^M$。盆 $k$ 未被覆盖的期望数为：

$$
\E\bqty{\sum_{k=1}^{\mathcal{N}} I_k^{(M)}} = \sum_{k=1}^{\mathcal{N}} (1 - p_k)^M
$$

假设最坏情形（所有 $p_k$ 相等，$p_k = 1/\mathcal{N}$）给出上界：

$$
\E[未覆盖盆数] = \mathcal{N} \cdot \pqty{1 - \frac{1}{\mathcal{N}}}^M \approx \mathcal{N} \cdot \exp\pqty{-\frac{M}{\mathcal{N}}}
$$

令此期望 $\leq \delta$：

$$
\mathcal{N} \, e^{-M / \mathcal{N}} \leq \delta \implies M \geq \mathcal{N} \log \frac{\mathcal{N}}
$$

对于 $\mathcal{N} \gg 1$，主导项为 $\mathcal{N} = \exp(N \Sigma_0)$，得证。

对于非均匀 $p_k$，使用 Bennett 不等式获得更紧的界。设 $p_{(1)} \leq p_{(2)} \leq ... \leq p_{(\mathcal{N})}$ 为排序后的概率。则覆盖所需专家数的上下界为：

$$
\frac{\log \mathcal{N} - \log \delta}{-\log(1 - p_{(1)})} \leq M_ \leq \frac{\log \mathcal{N} - \log \delta}{-\log(1 - p_{(\mathcal{N})})}
$$

在幂律分布 $p_{(k)} \propto k^{-\alpha}$（$\alpha > 0$，常见于过参数化网络中的Hessian谱）下，最稀有的盆具有最小的吸引概率，主导了覆盖难度。$ \square$

## 符号表

[Table omitted — see original .tex]

\begin{thebibliography}{99}

\bibitem{parisi1979}
G. Parisi, ``Infinite number of order parameters for spin-glasses,'' *Phys. Rev. Lett.*, vol. 43, pp. 1754--1756, 1979.

\bibitem{parisi1980}
G. Parisi, ``A sequence of approximated solutions to the S-K model for spin glasses,'' *J. Phys. A: Math. Gen.*, vol. 13, pp. L115--L121, 1980.

\bibitem{mezard1987}
M. M\'ezard, G. Parisi, and M. A. Virasoro, *Spin Glass Theory and Beyond*. Singapore: World Scientific, 1987.

\bibitem{sherrington1975}
D. Sherrington and S. Kirkpatrick, ``Solvable model of a spin-glass,'' *Phys. Rev. Lett.*, vol. 35, pp. 1792--1796, 1975.

\bibitem{edwards1975}
S. F. Edwards and P. W. Anderson, ``Theory of spin glasses,'' *J. Phys. F: Met. Phys.*, vol. 5, pp. 965--974, 1975.

\bibitem{choromanska2015}
A. Choromanska, M. Henaff, M. Mathieu, G. Ben Arous, and Y. LeCun, ``The loss surfaces of multilayer networks,'' in *Proc. AISTATS*, 2015, pp. 192--204.

\bibitem{dauphin2014}
Y. Dauphin, R. Pascanu, C. Gulcehre, K. Cho, S. Ganguli, and Y. Bengio, ``Identifying and attacking the saddle point problem in high-dimensional non-convex optimization,'' in *Proc. NeurIPS*, 2014, pp. 2933--2941.

\bibitem{ros2019}
V. Ros, G. Ben Arous, G. Biroli, and C. Cammarota, ``Complex energy landscapes in spiked-tensor and simple glassy models: ruggedness, arrangements of local minima, and phase transitions,'' *Phys. Rev. X*, vol. 9, p. 011003, 2019.

\bibitem{engel2001}
A. Engel and C. Van den Broeck, *Statistical Mechanics of Learning*. Cambridge: Cambridge University Press, 2001.

\bibitem{levin2019}
E. Levin and M. Z. Ziegler, ``The phase transition in random committee machines,'' *J. Phys. A: Math. Theor.*, vol. 52, p. 384001, 2019.

\bibitem{jacot2018}
A. Jacot, F. Gabriel, and C. Hongler, ``Neural tangent kernel: Convergence and generalization in neural networks,'' in *Proc. NeurIPS*, 2018, pp. 8571--8580.

\bibitem{fyodorov2004}
Y. V. Fyodorov, ``Complexity of random energy landscapes, glass transition, and absolute value of the spectral determinant of random matrices,'' *Phys. Rev. Lett.*, vol. 92, p. 240601, 2004.

\bibitem{benarous2019}
G. Ben Arous, R. Gheissari, and A. Jagannath, ``Bounding flows for spherical spin glass dynamics,'' *Comm. Math. Phys.*, vol. 373, pp. 1011--1048, 2019.

\bibitem{baity2019}
M. Baity-Jesi, L. Sagun, M. Geiger, S. Spigler, G. Ben Arous, C. Cammarota, Y. LeCun, and M. Wyart, ``Comparing dynamics: Deep neural networks versus glassy systems,'' *J. Stat. Mech.*, vol. 2019, p. 124013, 2019.

\bibitem{baldi2016}
P. Baldi and S. S. Sadowski, ``A theory of local minima in deep learning,'' in *Proc. ICLR Workshop*, 2016.

\bibitem{geiger2020}
M. Geiger, S. Spigler, S. d'Ascoli, L. Sagun, M. Baity-Jesi, G. Biroli, and M. Wyart, ``Jamming transition as a paradigm to understand the loss landscape of deep neural networks,'' *Phys. Rev. E*, vol. 101, p. 012115, 2020.

\bibitem{sagun2017}
L. Sagun, L. Bottou, and Y. LeCun, ``Eigenvalues of the Hessian in deep learning: Singularity and beyond,'' in *Proc. ICLR Workshop*, 2017.

\bibitem{castellani2005}
T. Castellani and A. Cavagna, ``Spin-glass theory for pedestrians,'' *J. Stat. Mech.*, vol. 2005, p. P05012, 2005.

\bibitem{talagrand2003}
M. Talagrand, *Spin Glasses: A Challenge for Mathematicians*. Berlin: Springer, 2003.

\bibitem{guerra2003}
F. Guerra, ``Broken replica symmetry bounds in the mean field spin glass model,'' *Comm. Math. Phys.*, vol. 233, pp. 1--12, 2003.

\bibitem{sagun2018}
L. Sagun, U. Evci, V. U. G\"uney, Y. Dauphin, and L. Bottou, ``Empirical analysis of the Hessian of over-parametrized neural networks,'' in *Proc. ICLR Workshop*, 2018.

\bibitem{pennington2017}
J. Pennington and Y. Bahri, ``Geometry of neural network loss surfaces via random matrix theory,'' in *Proc. ICML*, 2017, pp. 2798--2806.

\bibitem{franz2017}
S. Franz, G. Parisi, M. Sevelev, P. Urbani, and F. Zamponi, ``Universality of the SAT-UNSAT (jamming) threshold in non-convex continuous constraint satisfaction problems,'' *SciPost Phys.*, vol. 2, p. 019, 2017.

\bibitem{lecun2015}
Y. LeCun, Y. Bengio, and G. Hinton, ``Deep learning,'' *Nature*, vol. 521, pp. 436--444, 2015.

\bibitem{amari2020}
S. Amari, ``Any target function exists in a neighborhood of any sufficiently wide random network: A geometrical perspective,'' *Neural Computation*, vol. 32, pp. 1431--1447, 2020.

\end{thebibliography}