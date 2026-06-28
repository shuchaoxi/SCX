# SCX 竞争者理论分析：系统性跨域扫描

> **分析框架**: 对 8 个子领域的 28+ 个竞争者进行数学公式级对比
> **核心问题**: SCX 是否严格优于每个竞争者？若是，证明何在？若否，诚实承认。
> **日期**: 2026-06-28 | **版本**: v1.0

---

## 目录

1. [标注者建模 (Annotator Modeling)](#1-标注者建模-annotator-modeling)
2. [标签噪声检测 (Label Noise Detection)](#2-标签噪声检测-label-noise-detection)
3. [数据估值 (Data Valuation)](#3-数据估值-data-valuation)
4. [专家混合 (Mixture of Experts)](#4-专家混合-mixture-of-experts)
5. [主动学习 (Active Learning)](#5-主动学习-active-learning)
6. [贝叶斯优化 (Bayesian Optimization)](#6-贝叶斯优化-bayesian-optimization)
7. [在线学习 (Online Learning)](#7-在线学习-online-learning)
8. [MLIP 势函数 (Machine-Learned Interatomic Potentials)](#8-mlip-势函数-machine-learned-interatomic-potentials)
9. [SCX 相对位置矩阵](#9-scx-相对位置矩阵)
10. [总体评价](#10-总体评价)

---

## 1. 标注者建模 (Annotator Modeling)

### 1.1 竞争者概述

标注者建模的核心问题：给定多个标注者的标注结果，如何估计每个标注者的质量以及真实标签？

#### Dawid-Skene (1979)

**核心公式**:

对每个标注者 $m$ 定义一个混淆矩阵 $\pi^{(m)}$，其中 $\pi^{(m)}_{jk} = \mathbb{P}(f_m(x) = k \mid y^* = j)$。EM 算法交替执行：

**E-step**: 估计真实标签概率

$$\mathbb{P}(y^*_i = j \mid \{f_m(x_i)\}, \pi) \propto \prod_{m=1}^M \prod_{k=1}^K \bigl(\pi^{(m)}_{jk}\bigr)^{\mathbf{1}\{f_m(x_i) = k\}}$$

**M-step**: 更新混淆矩阵

$$\pi^{(m)}_{jk} \propto \sum_{i: f_m(x_i) = k} \mathbb{P}(y^*_i = j \mid \cdot)$$

复杂度：$O(M \cdot N \cdot K^2)$ 每次迭代。

#### Raykar et al. (2010) — "Learning from Crowds"

**核心公式**: 同时学习分类器 $w$ 和标注者质量矩阵 $\pi^{(m)}$。目标函数为边缘似然：

$$\mathcal{L}(w, \pi) = \log \sum_{y^*} \prod_i \prod_m \pi^{(m)}_{f_m(x_i), y^*_i} \cdot \prod_i \mathbb{P}(y^*_i \mid x_i, w)$$

交替优化：对 $w$ 用梯度下降，对 $\pi^{(m)}$ 用封闭解。额外引入了特征 $\phi(x)$ 与标注者质量的耦合。

#### Platanios et al. (2018) — "Estimating Accuracy from Unlabeled Data"

**核心公式**: 利用标注者之间的一致性和混淆程度，在**无真实标签**的情况下估计标注者准确率：

$$\mathbb{E}[\text{Acc}_m] = \frac{\mathbb{E}[f_m(x) = \bar{f}_{-m}(x)] - \mathbb{E}[\text{chance agreement}]}{1 - \mathbb{E}[\text{chance agreement}]}$$

这是一种无监督标注者质量估计器，其核心思想是"若标注者与其他标注者一致性显著高于随机，则更准确"。

### 1.2 与 SCX 的对比表格

| 维度 | Dawid-Skene (1979) | Raykar et al. (2010) | Platanios et al. (2018) | **SCX** |
|------|--------------------|--------------------|------------------------|---------|
| **核心对象** | 标注者混淆矩阵 $\pi^{(m)}$ | 分类器参数 $w$ + 混淆矩阵 $\pi$ | 标注者间一致性 | 共识分数 $C(x)=\frac{1}{M}\sum_m e_m(x)$ |
| **状态条件化** | 无状态；所有样本共享 $\pi^{(m)}$ | 无状态；$w$ 依赖 $x$，但 $\pi^{(m)}$ 全局 | 无状态 | **有**：$C(x)$ 的期望因状态 $s$ 而异 |
| **噪声模型** | 隐式（标注者可能随时出错） | 隐式（同 DS） | 标注者独立准确率 | **显式**：A4 均匀噪声假设 + Theorem 1 分离间隙 |
| **理论保证** | EM 收敛到局部最优（无全局保证） | EM 收敛到局部最优 | 一致性估计，无 F1 保证 | **F1 ≥ 1 - O(e^{-2MΔ²})** (Theorem 1) + **最小最大最优** (Theorem 4') |
| **需要真实标签？** | 否（联合估计） | 否（联合估计） | 否（仅利用一致性） | 是（需要 $y$ 计算 $e_m(x)$） |
| **标注者数量** | $M \geq 2$ | $M \geq 2$ | $M \geq 3$ 更好 | $M \geq 10$（实际推荐） |
| **可扩展性** | $O(MNK^2)$ | $O(MNK^2 + dN)$ | $O(M^2 N)$ | $O(MK_S N + K_S d_\phi)$ |
| **目标** | 估计 $y^*$ + $\pi$ | 估计 $y^*$ + $w$ + $\pi$ | 估计 Acc$_m$ | **检测噪声样本**（不是估计 $y^*$） |

### 1.3 关键问题分析

**问题**: Dawid-Skene 已经能做到标注者特定准确率估计，SCX 的状态条件化真的更优吗？

**回答**: 两者解决的**不是同一个问题**。

1. **Dawid-Skene 估计 $y^*$（真实标签），SCX 检测噪声（Z=1 vs Z=0）**。DS 输出每个样本的真实标签概率 $\mathbb{P}(y^*_i = j)$；SCX 输出每个样本的噪声标志 $\hat{z}(x)$。DS 本身不区分"噪声样本"和"困难样本"——标注者都会犯错，DS 只是合成了更准确的标签。

2. **SCX 的 Theorem 3 不识别性对这个比较至关重要**。DS 也无法区分这两种情况：给定相同的观测分布，DS 的 $\pi^{(m)}$ 和 $y^*$ 的估计在 Theorem 3 的两个世界会完全不同。SCX 诚实承认了这个不识别性（Theorem 3 的反向结果），而 DS 只是简单地输出某个局部最优解，不区分噪声和困难。

3. **SCX 有 F1 保证，DS 没有**。Theorem 1 给出了检测的下界（$\text{F1} \geq 1 - \frac{1}{\eta}\sum_s \rho_s e^{-2M\Delta_s^2}$），Theorem 4' 给出了精确最小最大常数。DS 没有任何等价的检测保证。

4. **但如果任务是从噪声标注中恢复 $y^*$，SCX 不如 DS**。SCX 专门设计用于**检测**噪声样本，而不是估计真实标签。如果目标是 $y^*$ 估计，DS 的 EM 框架更直接。SCX+DS 可以互补：先用 SCX 检测并移除噪声，再用 DS 在剩余数据上估计 $y^*$。

**判定**: SCX 在噪声**检测**任务上严格优于 DS（有 F1 保证 + 状态条件化），但在真实标签**估计**任务上不如 DS（SCX 不估计 $y^*$）。这是设计目标的不同，不是技术不足。

---

## 2. 标签噪声检测 (Label Noise Detection)

### 2.1 竞争者概述

#### Confident Learning (Northcutt et al., 2021)

**核心公式**: 通过估计噪声联合分布 $\hat{Q}_{ij} = \mathbb{P}(\hat{y}=i, y^*=j)$ 来识别错误标签。核心算法：

**Step 1**: 对每个样本，计算置信度 $p_j(x_i) = \mathbb{P}(y=j \mid x_i)$（来自单模型）。
**Step 2**: 对每个类 $j$，构造阈值 $t_j = \frac{1}{n_j} \sum_{i: \hat{y}=j} p_j(x_i)$。
**Step 3**: 对每个样本 $i$，定义自置信：$p_{\hat{y}}(x_i)$。若 $p_{\hat{y}}(x_i) < t_{\hat{y}}$，标记为可能噪声。
**Step 4**: 估计联合分布 $\hat{Q}_{ij} = \frac{|X_{\hat{y}=i, y^*=j}|}{n}$，并对角线修正。
**Step 5**: Prune：按 $\hat{Q}_{ij}$ 选择 $n \cdot \hat{Q}_{ij}$ 个最低置信的 $\hat{y}=i$ 样本进行删除。

**SCX 对应**: SCX 用 $C(x) = \frac{1}{M}\sum_m e_m(x)$ 做检测，靠的是 M 个独立专家的离散度，而非单模型置信度。

#### MentorNet (Jiang et al., 2018)

**核心公式**: 用一个 mentor 网络 $g$ 学习样本权重 $w_i = g(\nabla \mathcal{L}_i)$，student 网络 $f$ 在加权损失上训练：

$$\min_f \sum_i w_i \cdot \ell(f(x_i), y_i), \quad w_i = g(\nabla \ell(f(x_i), y_i) \mid \text{curriculum params})$$

mentor 网络通过预训练（在干净数据上或合成噪声数据上）学习 curriculum 策略。

#### ELR (Liu et al., 2020) — Early-Learning Regularization

**核心公式**: 在标准交叉熵损失中加入正则项，利用模型自身在早期学习的"记忆效应"：

$$\mathcal{L}_{\text{ELR}} = \mathcal{L}_{\text{CE}} + \frac{\lambda}{n} \sum_{i=1}^n \log\left(1 - \langle p_i, t_i\rangle\right)$$

其中 $p_i$ 是模型对样本 $i$ 的预测，$t_i$ 是移动平均目标 $t_i^{(k)} = \beta t_i^{(k-1)} + (1-\beta) p_i^{(k)}$。核心直觉：模型在早期阶段先学到干净样本（记忆效应），ELR 强制预测与移动平均一致，阻止模型适应噪声。

#### DivideMix (Li et al., 2020)

**核心公式**: 将噪声检测与半监督学习联合。用两个网络 $f_1, f_2$ 的**交叉验证**机制：

**Stage 1 (Co-Divide)**: 每个网络为另一个网络划分样本：
$$ \text{对于 } f_2\text{，样本 } i \text{ 被 } f_1 \text{ 分类为干净如果 } \ell(f_1(x_i), y_i) < \tau_{1}^{(t)}$$
其中 $\tau_{1}^{(t)}$ 是动态阈值（按 $\beta$ 分位数），$\tau_{1}^{(t)} = \text{Percentile}(\{\ell(f_1(x_i), y_i)\}, 1 - \frac{\eta}{1-\eta})$。

**Stage 2 (Semi-Supervised)**: 将干净样本用作有标签数据，噪声样本用作无标签数据（用 MixMatch 框架训练）。

### 2.2 对比表格

| 维度 | Confident Learning | MentorNet | ELR | DivideMix | **SCX** |
|------|-------------------|-----------|-----|-----------|---------|
| **核心检测机制** | 单模型自置信 $p_j(x)$ < 类阈值 $t_j$ | 梯度幅值的 curriculum 过滤 | 早期学习正则化抑制噪声适应 | 双模型交叉 + 阈值分位数 | 多专家共识 $C(x)$ vs 阈值 $\theta$ |
| **模型数量** | 1 个 | 2 个（mentor + student） | 1 个 | 2 个 | $M \geq 10$ 个独立训练 |
| **理论保证** | 经验性准确率；有 joint dist 估计的一致性 | 无理论保证 | 无（经验性观察记忆效应） | 无（经验性 SOTA） | **F1 ≥ 1 - O(e^{-2MΔ²})** + **最小最大最优** |
| **需要干净数据？** | 否（噪声联合分布可估计） | 需要预训练 mentor | 否 | 否 | 否（但需要 $y$ 来计算 $e_m$） |
| **计算成本** | 低（单模型训练 1 次） | 中（两个网络） | 低（额外正则项） | 高（两个网络 + MixMatch） | **高**（M 个独立训练 + 聚类） |
| **泛化域** | 图像、文本（任何有置信度的模型） | 图像 | 图像 | 图像（MixMatch 生态） | 任何多专家场景 |
| **噪声类型** | 任意（joint dist 无假设） | 任意 | **对称噪声**（均匀）效果最好 | 任意 | **均匀噪声**（A4 假设） |

### 2.3 关键问题分析

**问题**: SCX 需要 $M \geq 10$ 个独立训练的专家，Confident Learning 只需要 1 个模型 + confident joint — 实验设置不公平？

**诚实分析**: 这里有三层答案：

**第一层：公平性与设计目标不同**

Confident Learning 是为**单模型**场景设计的——你有一个训练好的分类器，想在它的训练数据中找噪声。SCX 是为**多专家**场景设计的——你有多个独立训练的模型（材料领域：不同势函数；医学：不同诊断模型）。它们解决的是不同的资源假设。

**第二层：SCX 的 M 个专家的成本是否总是更高？**

- 在材料 MLIP 场景：ACE 和 NEP 是**已有的**——没有人专门为噪声检测训练它们。M 个专家是现成的。使用 SCX 的**边际成本仅为嵌入和聚类**。
- 在图像场景：训练 M 个 CNN 确实贵。但 SCX 的 Theorem 4' 显示误差以 $e^{-M\kappa}$ 衰减，而 Confident Learning 的误差衰减没有已知的理论保证（虽然经验性不错）。
- **关键不对称**：SCX 的 $e^{-M\kappa}$ 衰减是指数级的——M 个专家带来的不是线性收益，而是指数级更精确的检测。如果用 M=1 甚至 M=2，SCX 理论上失效；但 M=10 时 SCX 的保证就非常强劲了。

**第三层：Confident Learning 的一个隐藏问题**

Confident Learning 的 $p_j(x)$ 来自一个**在噪声数据上训练的模型**。这意味着 $p_j(x)$ 本身是有偏的——模型在噪声上过拟合后会错误地自信（ELR 的研究正好说明了这一点）。SCX 的 M 个专家是在**独立的、不重叠的训练集**上训练的（A1 假设），因此它们的误差不是共同有偏的。这是结构性的区别，不是实验设置的区别。

**诚实判定**:

| 场景 | 更好的选择 | 理由 |
|------|-----------|------|
| 单模型 + 噪声数据 | **Confident Learning** | SCX 无法单模型运行 |
| 多专家 + 噪声标签 | **SCX** | 利用多专家独立性获得指数级保证 |
| 图像分类 + 大量未标注 | **DivideMix** | 半监督范式利用无标签数据 |
| 材料势函数 | **SCX** | 多势函数是标配，SCX 零边际成本 |
| 噪声类型未知 | **Confident Learning** | SCX 的 A4 均匀噪声假设可能被违反 |

**SCX 并不严格优于 Confident Learning**。它们是互补的，适用于不同的资源设定。SCX 的优势区域是多专家场景；Confident Learning 的优势区域是单模型场景。

---

## 3. 数据估值 (Data Valuation)

### 3.1 竞争者概述

#### Data Shapley (Ghorbani & Zou, 2019)

**核心公式**: 基于合作博弈论，数据点 $i$ 的 Shapley 值为：

$$\phi_i = \sum_{S \subseteq \mathcal{D} \setminus \{i\}} \frac{|S|!(|\mathcal{D}| - |S| - 1)!}{|\mathcal{D}|!} \bigl[V(S \cup \{i\}) - V(S)\bigr]$$

其中 $V(S)$ 是在数据集 $S$ 上训练模型的性能（如验证集准确率）。Shapley 值是满足以下公理的**唯一**估值函数：
- **对称性**（Symmetry）：若 $i$ 和 $j$ 对所有子集贡献相同，则 $\phi_i = \phi_j$
- **零元素**（Dummy）：若 $i$ 对任何子集都无贡献，则 $\phi_i = 0$
- **可加性**（Additivity）：两个游戏的 Shapley 值之和等于联合游戏的 Shapley 值
- **有效性**（Efficiency）：$\sum_i \phi_i = V(\mathcal{D})$

计算复杂度：$O(2^n)$ 精确，近似需要蒙特卡洛 $O(Tn)$ 次模型重训练。

#### LOO (Leave-One-Out)

**核心公式**:

$$\phi_i^{\text{LOO}} = V(\mathcal{D}) - V(\mathcal{D} \setminus \{i\})$$

即移除 $i$ 后验证性能的下降。计算复杂度 $O(n)$ 次重训练（实际上不可行，需近似）。

#### Data-OOB (Kwon & Zou, 2022)

**核心公式**: 利用 bagging 的 out-of-bag 样本来近似 Shapley 值。对每个 bagging 模型 $t$，OOB 集 $O_t$ 用于估值：

$$\hat{\phi}_i = \frac{1}{T} \sum_{t: i \notin \mathcal{D}_t} \bigl[V_t(O_t) - V_t(O_t \setminus \{i\})\bigr]$$

其中 $\mathcal{D}_t$ 是第 $t$ 个 bagging 的训练集。复杂度 $O(T \log T)$ 次模型调用。

#### DVRL (Yoon et al., 2020) — Data Valuation using Reinforcement Learning

**核心公式**: 用强化学习学习一个数据选择策略 $g_\theta$：

$$\max_\theta \mathbb{E}_{S \sim g_\theta} [V(S)]$$

其中 $g_\theta(x_i)$ 是选择 $x_i$ 的概率。通过 REINFORCE 或 Gumbel-softmax 训练。输出每个样本的"价值权重"。

#### LAVA (Just et al., 2023) — Label Valuation

**核心公式**: 将"数据估值"分解为 "特征价值" + "标签价值"：

$$\phi_i^{\text{LAVA}} = \phi_i^{\text{feature}} + \phi_i^{\text{label}}$$

其中标签价值通过比较原始标签 $y_i$ 与模型预测 $\hat{y}_i$ 来估计：

$$\phi_i^{\text{label}} = V(\mathcal{D}_{\text{clean}}) - V(\mathcal{D}_{\text{clean}} \setminus \{(x_i, y_i)\} \cup \{(x_i, \hat{y}_i)\})$$

LAVA 的重要发现是：大部分数据价值来源于特征，标签的价值通常很小。

### 3.2 对比表格

| 维度 | Data Shapley | LOO | Data-OOB | DVRL | LAVA | **SCX** |
|------|-------------|-----|---------|------|------|---------|
| **核心公式** | 博弈论 Shapley 值 | $V(\mathcal{D}) - V(\mathcal{D}\setminus\{i\})$ | OOB 近似 Shapley | RL 策略 $g_\theta$ | $\phi^{\text{feature}} + \phi^{\text{label}}$ | $V(s) = \bar{r}(s) \cdot \rho(s) \cdot L(s) \cdot (1-D(s))$ |
| **公理化基础** | **有**（Shapley 四条公理） | 无（不满足对称性等） | 近似满足 Shapley 公理 | 无 | 无 | 无（经验性框架） |
| **计算复杂度** | $O(2^n)$ 精确，$O(Tn)$ 近似 | $O(n)$ 近似 | $O(T \log T)$ | $O(Tn)$ 训练 | $O(n)$ 一次前向 | $O(MK_S N + K_S d_\phi)$ |
| **估值级别** | 样本级 | 样本级 | 样本级 | 样本级 | 样本级 | **状态级**（$V(s)$ 是按状态的） |
| **考虑噪声？** | 隐式（噪声样本价值低） | 隐式 | 隐式 | 隐式 | 显式（标签价值） | **显式**（$L(s)$ 包含 $1-N(s)$） |
| **需要重训练？** | 是（多次） | 是（多次） | 是（bagging 内） | 是（RL 训练） | 是 | **否**（静态计算） |
| **可解释性** | 高（公理化） | 高（直观） | 中 | 低（黑箱策略） | 中（分解） | **高**（每个 state 的 V(s) 有明确含义） |

### 3.3 关键问题分析

**问题**: Data Shapley 有公理化基础（对称性、可加性等），SCX 的 $V(s)$ 有类似的公理化吗？

**诚实回答**: **没有。SCX 的 $V(s)$ 是一个工程性的评分函数，不是公理化的价值函数。**

具体来说：

1. **SCX 的 $V(s)$ 不满足 Shapley 公理**（也不试图满足）。它是在状态级别定义的一个评分 $\bar{r}(s)\rho(s)L(s)(1-D(s))$，用于决定哪些状态值得采集样本。它不是合作博弈中的价值函数。

2. **这既是弱点也是优点**：
   - **弱点**：缺乏公理基础意味着 $V(s)$ 没有"正确性"的理论保证。$V(s)$ 的各个分量（$\bar{r}(s), \rho(s), L(s), D(s)$）之间的权重组合是经验性的，不是从最优性推导出来的。
   - **优点**：Shapley 值的计算需要**每种子集上的模型重训练**，这在实践中几乎不可行（$O(2^n)$）。SCX 的 $V(s)$ 是**完全前向的**——不需要重训练任何模型，只需一次状态发现 + 一次误差计算。

3. **但是 SCX 有一个 Shapley 没有的东西：量化保证**。Shapley 值告诉你哪个样本有价值，但不告诉你这个值在统计上是否可靠。SCX 的 Theorem 2 告诉你：如果特征弱（$I(\phi;S)$ 小），那么状态划分无效，$V(s)$ 不可靠。Proposition 6 给出了具体的诊断阈值（$S(\Phi,K) > 0.7$）。这种"知道自己不知道"的能力其实是 Shapley 方法没有的。

4. **SCX 不出样本级价值**。Shapley 和 LOO 给出每个样本的个体价值，SCX 只给出状态级聚合价值。如果用户需要细粒度到样本级，SCX 需要额外的步骤（在状态内按残差排序）。

**诚实判定**: Data Shapley 的公理化基础是 SCX 无法替代的。如果论文审稿人问"为什么 $V(s)$ 使用乘积而不是其他组合形式？"，目前的回答只能是"这是直观设计的选择"而不是"从公理推导而来"。这是 SCX 的一个理论弱点。

---

## 4. 专家混合 (Mixture of Experts)

### 4.1 竞争者概述

#### HME (Jacobs et al., 1991) — Hierarchical Mixture of Experts

**核心公式**: 将输入空间划分为多个专家领域，用门控网络 $g(x)$ 分配权重：

$$p(y \mid x) = \sum_{m=1}^M g_m(x) \cdot p_m(y \mid x, \theta_m)$$

其中 $g(x) = \text{softmax}(Vx)$ 是线性的门控，$p_m$ 是指数族分布（通常是广义线性模型）。通过 EM 或梯度下降联合训练。

#### Sparsely-Gated MoE (Shazeer et al., 2017)

**核心公式**: 用稀疏门控激活 $TopK$ 个专家：

$$y = \sum_{m=1}^M g_m(x) \cdot f_m(x), \quad g(x) = \text{softmax}(\text{TopK}(x \cdot W_g, k))$$

其中 TopK 保留最大的 $k$ 个值，其余置为 $-\infty$（softmax 后为 0）。增加辅助损失以平衡各专家负载：

$$\mathcal{L}_{\text{balance}} = \alpha \cdot C_V \cdot \sum_{m=1}^M \frac{\sum_i g_m(x_i)}{N} \cdot \frac{\sum_i \mathbf{1}\{g_m(x_i) > 0\}}{N}$$

#### Switch Transformer (Fedus et al., 2022)

**核心公式**: 简化 MoE，每个 token 只路由到一个专家：

$$y = f_{\text{expert}(x)}(x), \quad \text{expert}(x) = \arg\max_m x \cdot W_m$$

Switch Transformer 证明这种极稀疏路由（MoE 的 $k=1$ 特例）在大规模缩放时效果优异，同时计算效率最高。

#### Soft MoE (Puigcerver et al., 2024)

**核心公式**: 用软分配替代离散路由，避免负载不均衡和不平衡损失：

$$y_j = \sum_{i=1}^N \frac{\exp(x_i \cdot \Phi_j)}{\sum_{k} \exp(x_i \cdot \Phi_k)} \cdot f_m(x_i)$$

其中 $\Phi_j$ 是可学习的"slot"参数。每个 slot 接收所有输入的加权组合，消除了硬路由的离散选择问题。

### 4.2 对比表格

| 维度 | HME (1991) | Sparse MoE (2017) | Switch TF (2022) | Soft MoE (2024) | **SCX Router** |
|------|-----------|-----------------|-----------------|----------------|----------------|
| **路由机制** | 软门控 $g_m(x) = \text{softmax}(Vx)$ | 稀疏 TopK 门控 + softmax | 硬 Top-1 路由 | 软插槽分配（全对全加权） | 状态条件路由 $m^*(x) = \arg\min_m \sum_s \gamma_s(x) R_m(s)$ |
| **状态条件化** | **无**（门控是 $x$ 的函数） | **无**（门控是 $x$ 的函数） | **无** | **无** | **有**（先划分状态，再状态内路由） |
| **专家异构？** | 专家结构相同（同质） | 专家结构相同 | 专家结构相同 | 专家结构相同 | **显式处理异构**（不同结构的模型） |
| **训练方式** | 联合训练 (EM/GD) | 联合训练 | 联合训练 | 联合训练 | **独立训练**（不联合更新） |
| **路由学习信号** | 梯度（端到端） | 梯度 + 辅助负载平衡损失 | 梯度 + 辅助损失 | 梯度（软分配自动平衡） | 专家在状态上的历史性能 $R_m(s)$ |
| **路由适应性** | 在线（随训练变化） | 在线 | 在线 | 在线 | **固定**（路由策略基于评估后静态统计量） |
| **计算效率** | 全部专家都计算 | TopK 个专家计算 | 1 个专家计算 | 所有专家（但软组合） | 1 个专家（路由后） |

### 4.3 关键问题分析

**问题**: MoE 的 gate 也是输入条件的（$g(x) = \text{softmax}(x \cdot W_g)$）——SCX 的"状态条件化"真的不同吗？

**诚实回答**: **确实不同，但差异没有 SCX 宣传的那么大。**

**第一层：两者的条件化级别不同**

- MoE 的门控：$g(x) = \text{softmax}(x \cdot W_g)$ 是 **连续、输入级** 的条件化。每个输入 $x$ 可以分配到**多个专家的混合**。
- SCX 的路由：$m^*(x) = \arg\min_m \sum_s \gamma_s(x) R_m(s)$ 是 **状态级** 的条件化。$x$ 先被软分配到状态 $\gamma_s(x)$，然后基于状态聚合的历史误差选择专家。

关键区别：MoE 的门控是**学习一个关于 $x$ 的直接映射**（$W_g$ 直接作用于输入），SCX 是**首先聚类出状态结构，然后在状态层面路由**。这有本质区别吗？有。

**第二层：SCX 的优势**

- **状态可解释**：SCX 的状态 $s$ 有明确的物理解释（例如在 MLIP 中，状态可以对应 sp²/sp³ 杂化、表面等等）。MoE 的门控是高维非线性映射，不可解释。
- **状态聚合降低方差**：SCX 的专家可靠性 $\text{SCX}_m(s)$ 是在整个状态 $s$ 上聚合的统计量，方差 $O(1/n_s)$。MoE 的 $g(x)$ 是逐样本的，没有状态聚合的稳定性。
- **异构专家**：SCX 的路由基于历史误差 $R_m(s)$，不要求专家结构相同。MoE 通常要求专家是相同架构的网络。这是 SCX 的一个实际优势。

**第三层：SCX 的劣势**

- **路由不是联合优化的**。MoE 的门控是端到端训练的，门控 $W_g$ 能通过梯度信号学习到最优分配。SCX 的路由是后验的——先用独立数据训练专家，再评估他们在各状态上的表现，然后根据这个固定统计量路由。这种**非端到端**的方式会错过联合训练带来的协同优化。
- **状态划分固定**。SCX 的状态划分一旦确定就不随路由目标调整。MoE 的门控会持续调整以优化路由。如果 SCX 的状态划分与路由最优状态不一致（例如聚类在特征空间 $\phi(x)$ 上做，但最优路由需要不同的划分），性能会退化。
- **Theorem 2 对此有预示**：如果特征 $\delta$-weak，状态划分无效，SCX 的路由退化为基于全局 $R_m$ 的路由（等同于无状态门控）。

**诚实判定**: SCX 的状态条件路由**不是** MoE 门控的一个简单变体。它是一种不同的范式——可解释、低方差、支持异构专家。但它缺乏 MoE 的联合优化，状态划分的固定性意味着它对特征质量高度敏感。SCX 不严格优于 MoE；两者在路由质量上的比较需要实证验证。

---

## 5. 主动学习 (Active Learning)

### 5.1 竞争者概述

#### Uncertainty Sampling (Lewis & Catlett, 1994)

**核心公式**:

$$x^* = \arg\max_{x \in \mathcal{U}} \mathcal{H}(y \mid x, \theta) = \arg\max_x \left[-\sum_{j=1}^K p_j(x) \log p_j(x)\right]$$

即选择模型最不确定的样本。简单但易受离群点和噪声影响。

#### Query-by-Committee (QBC) (Seung et al., 1992)

**核心公式**: 维护一个模型委员会 $\{h_1, \ldots, h_C\}$，选择委员会分歧最大的样本：

$$x^* = \arg\max_{x \in \mathcal{U}} \frac{1}{C} \sum_{c=1}^C \mathbb{KL}(h_c(y \mid x) \| \bar{h}(y \mid x))$$

其中 $\bar{h}(y \mid x) = \frac{1}{C}\sum_c h_c(y \mid x)$ 是委员会的共识分布。分歧的度量可以是投票熵或 KL 散度。

**与 SCX 最接近的基准**——都用多模型不一致来选择样本。

#### BADGE (Ash et al., 2020)

**核心公式**: 选择梯度嵌入**多样**的样本（不是不确定的样本）：

$$g_i = \nabla \ell(x_i, \hat{y}_i; \theta), \quad \hat{y}_i = \arg\max_y p(y \mid x_i, \theta)$$

然后用 k-means++ 在梯度嵌入空间中挑选代表点。BADGE 的关键创新是将不确定性和多样性统一在梯度嵌入中。

#### BAAL (Atighehchian et al., 2020)

**核心公式**: 用 MC-Dropout 的贝叶斯估计作为不确定性：

$$p(y \mid x, \mathcal{D}) \approx \frac{1}{T} \sum_{t=1}^T p(y \mid x, \theta^{(t)}), \quad \theta^{(t)} \sim q(\theta \mid \mathcal{D})$$

不确定性度量 $U(x) = \mathcal{H}(\bar{p}) - \frac{1}{T}\sum_t \mathcal{H}(p_t)$（互信息），捕获认识论不确定性。

#### TypiClust (Hacohen et al., 2022)

**核心公式**: 选择典型（typical）样本，代表数据分布的密集区域：

$$x^* = \arg\max_{x \in \mathcal{U}} \left[- \min_{z \in \text{labeled}} \| \phi(x) - \phi(z) \|_2\right]$$

即在嵌入空间 $\phi$ 中选择离现有标注集最远的样本，但**优先选择密度高的区域**（通过密度权重调整）。这种 "coverage + typicality" 策略是对不确定性采样的重要补充。

### 5.2 对比表格

| 维度 | Uncertainty | QBC | BADGE | BAAL | TypiClust | **SCX** |
|------|-----------|-----|-------|------|-----------|---------|
| **选择准则** | $\mathcal{H}(y \mid x)$ | $\frac{1}{C}\sum_c \mathbb{KL}(h_c \| \bar{h})$ | k-means++ on $\nabla \ell$ | $\mathcal{H}(\bar{p}) - \frac{1}{T}\sum_t \mathcal{H}(p_t)$ | $-\min_z \|\phi(x) - \phi(z)\|$ + density | $V(s) = \bar{r}(s)\rho(s)L(s)(1-D(s))$ |
| **多模型使用** | 单模型 | **委员会**（$C$ 个模型） | 单模型（梯度空间） | 单模型（MC-Dropout） | 单模型（嵌入空间） | **M 个独立专家** |
| **多样性考虑** | 否 | 否（逐样本独立） | **是**（k-means++ 选择） | 否 | **是**（覆盖+典型性） | **状态级**（选状态，再在状态内选点） |
| **抗噪声？** | **差**（不确定=噪声？） | 中等（分歧可能来源噪声） | 中等 | 中等 | 中等 | **好**（Theorem 1 检测噪声） |
| **理论保证** | 经验性 | **标签复杂度 $O(\theta d \log(1/\varepsilon))$**（Balcan et al.） | 经验性 | 经验性 | 经验性 | **有**（Theorem 1 F1 保证） |
| **状态结构** | 无 | 无 | 无 | 无 | 无（有密度但无状态） | **核心**（状态是一切的基础） |
| **选择级别** | 样本级 | 样本级 | 样本级 | 样本级 | 样本级 | **先状态级，再样本级** |

### 5.3 关键问题分析

**问题**: Query-by-Committee 已经是"用多专家不一致来选择样本"——SCX 相比 QBC 的增量在哪里？

**诚实回答**: 增量是真实的，但需要逐层分析。

**增量 1：QBC 用分歧，SCX 用共识（Theorem 1）**

QBC：选择 $\arg\max_x \frac{1}{C}\sum_c \mathbb{KL}(h_c \| \bar{h})$ —— 分歧最大的样本，假设分歧意味着信息量。

SCX：检测 $C(x) > \theta$ 的样本为噪声——共识（而非分歧）的阈值化。

**这是根本不同的操作**：
- QBC 想找"专家们意见不统一的样本，因为标注它们可能最有信息量"
- SCX 想找"专家们意见统一但都错了的样本——因为这是噪声"

QBC 的前提是：标注是干净的，不一致是由于模型欠拟合，所以标注最好。SCX 的前提是：标签可能是脏的，一致地错误是噪声的信号。

**增量 2：状态结构**

SCX 的所有信号都是在状态层面聚合的：$\text{SCX}_m(s) = \mathbb{P}(\ell(f_m(x), y) < \tau \mid x \in s)$。这意味着专家可靠性是状态条件的。QBC 没有这个。

**增量 3：Theorem 3 不识别性**

SCX 诚实地区分了"噪声"和"困难"两个不可识别世界。QBC 简单地假设分歧等同于信息量，不会质疑"这个专家分歧是因为噪声还是因为样本本身就难？"

**增量 4：Theorem 2 的特征弱点意识**

SCX 在 Theorem 2 中明确量化了特征弱点 $\delta = I(\phi;S)$ 对检测能力的影响，Proposition 6 提供了可操作的诊断工具。QBC 没有等价的"自知之明"。

**但是 QBC 有一个 SCX 没有的优势**：

QBC 的委员会是在**同一个训练集上训练**的（通过不同的初始化、bagging 等），模型数量 $C$ 可以很大（100+）。SCX 的专家必须在**不重叠的子集**上训练（A1 假设），否则独立性被破坏。对于小数据集，SCX 的 $M$ 受限于 $n / n_{\text{per expert}}$ 比率。

**诚实判定**: SCX 在**噪声存在**的主动学习场景下严格优于 QBC（有检测保证、状态聚合、噪声-困难区分）。在**标签干净**的场景下，QBC 可能更有效——因为 SCX 的检测保证在没有噪声时没有意义，状态划分反而增加成本。

---

## 6. 贝叶斯优化 (Bayesian Optimization)

### 6.1 竞争者概述

#### GP-UCB (Srinivas et al., 2010)

**核心公式**: 选择最大化上置信边界的点：

$$x_{t+1} = \arg\max_{x \in \mathcal{X}} \underbrace{\mu_t(x)}_{\text{预测均值}} + \beta_t \underbrace{\sigma_t(x)}_{\text{后验标准差}}$$

其中 $\mu_t(x)$ 和 $\sigma_t(x)$ 来自高斯过程后验，$\beta_t$ 是探索-利用平衡参数。累积遗憾界：

$$R_T = \sum_{t=1}^T (f(x^*) - f(x_t)) \leq \sqrt{T \cdot \gamma_T \cdot C}$$

其中 $\gamma_T$ 是最大信息增益（对于 SE 核：$\gamma_T = O((\log T)^{d+1})$）。

#### Expected Improvement (EI)

**核心公式**:

$$x_{t+1} = \arg\max_{x \in \mathcal{X}} \mathbb{E}[\max(0, f(x) - f_{\text{best}}) \mid \mathcal{D}_t]$$

对于高斯过程后验，闭合形式为：

$$\alpha_{\text{EI}}(x) = (f_{\text{best}} - \mu(x)) \Phi\!\left(\frac{f_{\text{best}} - \mu(x)}{\sigma(x)}\right) + \sigma(x) \phi\!\left(\frac{f_{\text{best}} - \mu(x)}{\sigma(x)}\right)$$

其中 $\Phi, \phi$ 是标准正态的 CDF 和 PDF。

#### qNEHVI (Daulton et al., 2021)

**核心公式**: 多目标贝叶斯优化的**批量高效**采集函数。通过近似超体积改进（NEHVI）并支持批量查询：

$$\alpha_{\text{qNEHVI}}(X_{\text{batch}}) = \mathbb{E}\left[\max\left(0, HV(Pareto_{t} \cup \{f(x)\}_{x \in X_{\text{batch}}}) - HV(Pareto_t)\right)\right]$$

使用准蒙特卡洛采样近似该期望，支持 $\leq 128$ 点的批量查询。

### 6.2 对比表格

| 维度 | GP-UCB | EI | qNEHVI | **SCX Acquisition** |
|------|--------|-----|--------|-------------------|
| **核心采集函数** | $\mu_t(x) + \beta_t \sigma_t(x)$ | $\mathbb{E}[\max(0, f(x)-f_{\text{best}})]$ | 期望超体积改进 | $V(s) = \bar{r}(s)\rho(s)L(s)(1-D(s))$ |
| **代理模型** | 高斯过程 | 高斯过程 | 高斯过程（多目标） | 多专家共识 + 状态统计量 |
| **探索机制** | $\beta_t \sigma_t(x)$（后验方差） | $\sigma(x)\phi(\cdot)$（隐含） | 帕累托前沿不确定性 | 低共识 $1-C(s)$ + 低密度 $1/\rho(s)$ |
| **状态结构** | 无（逐点） | 无（逐点） | 无（逐点） | **有**（状态级聚合） |
| **目标函数** | 单目标 $f(x)$ | 单目标 $f(x)$ | 多目标 $f_1(x), \ldots, f_k(x)$ | **隐式目标**（发现高价值采集状态） |
| **评价成本** | 每次 $O(n^3)$（GP） | 每次 $O(n^3)$ | 每次 $O(n^3 + T_{\text{MC}})$ | 每次 $O(MK_S N + K_S d_\phi)$ |
| **理论保证** | 遗憾界 $O(\sqrt{T\gamma_T})$ | 无（经验性） | 无（经验性） | Theorem 1 + Theorem 4'（检测） |
| **在线更新** | 增量 GP 更新 | 增量 GP 更新 | 增量 GP 更新 | **有**（Online SCX 框架） |

### 6.3 关键问题分析

**问题**: SCX 的 acquisition 函数是否等价于某种 BO acquisition 的特例？

**诚实回答**: **不完全是，但深层联系是存在的。**

**等价性的论证**：

如果我们将状态 $s$ 视为"输入空间的一个区域"，将 $\bar{r}(s)$ 视为"当前模型在该区域的误差"（类比 BO 中的 $f(x)$ 值），$1-C(s)$ 视为"不确定性的度量"（类比 $\sigma^2(s)$），那么：

$$V(s) = \underbrace{\bar{r}(s)}_{\text{目标值}} \cdot \underbrace{\rho(s)}_{\text{区域质量}} \cdot \underbrace{L(s)}_{\text{可学习性}} \cdot \underbrace{(1-D(s))}_{\text{不冗余}}$$

$$\alpha_{\text{EI}}(x) = \underbrace{(f_{\text{best}} - \mu(x))}_{\text{改进量}} \cdot \underbrace{\Phi(\frac{f_{\text{best}}-\mu(x)}{\sigma(x)})}_{\text{改进概率}} + \underbrace{\sigma(x)\phi(\cdot)}_{\text{不确定性}}\]

有结构上的相似性：都包含（价值项）$\times$（不确定性/探索项）。但 SCX 多了 $\rho(s)$（区域大小）和 $1-D(s)$（不冗余）——这两个在 BO 的标准 acquisition 中没有直接对应。

**本质区别**：

1. **BO 优化的是一个固定黑箱函数** $f$。SCX 的 acquisition 目标**在模型改进过程中自身也在变化**——随着专家改进，$\bar{r}(s)$ 下降，$L(s)$ 变化。SCX 的目标分布是演变的，BO 的目标函数是固定的。

2. **BO 是点级操作，SCX 是状态级操作**。BO 选择单个点 $x_{t+1}$，SCX 先选状态 $s^*$ 再在状态内采样。这使得 SCX 在状态内可以批量采集（状态内的所有样本共享特性），而 BO 的批量扩展需要额外的机制（如 qNEHVI）。

3. **SCX 的 $\rho(s)$ 是一个在 BO 中没有对应项的因子**。$\rho(s)$ 反映了状态的大小——大的状态即使平均误差不高也值得采集，因为改进的绝对影响更大。BO 不会因为某个区域"很宽"就优先在其中采样，它完全基于点级的不确定性和改进量。

**诚实判定**: SCX 的 acquisition 不是 BO acquisition 的特例。两者有拓扑相似性但细节根本不同。SCX 在"多批量并行采集"上可能比 BO 更自然（状态就是天然的批量），但在"精细的单点优化"上不如 BO（状态是粗糙的划分）。

---

## 7. 在线学习 (Online Learning)

### 7.1 竞争者概述

#### OGD (Zinkevich, 2003) — Online Gradient Descent

**核心公式**: 在每一轮 $t$ 接收损失函数 $\ell_t$，更新参数：

$$\theta_{t+1} = \Pi_{\Theta}(\theta_t - \eta_t \nabla \ell_t(\theta_t))$$

其中 $\Pi_{\Theta}$ 是向凸集 $\Theta$ 的投影。累积遗憾界（对于凸损失和有界梯度 $\|\nabla \ell\| \leq G$，步长 $\eta_t = \frac{D}{G\sqrt{T}}$）：

$$\text{Regret}_T = \sum_{t=1}^T \ell_t(\theta_t) - \min_{\theta \in \Theta} \sum_{t=1}^T \ell_t(\theta) \leq 2GD\sqrt{T}$$

#### FTRL (McMahan & Streeter, 2010)

**核心公式**: 在每一轮选择最小化累积损失 + 正则项的参数：

$$\theta_{t+1} = \arg\min_{\theta \in \Theta} \left( \sum_{s=1}^t \ell_s(\theta) + \psi(\theta) \right)$$

其中 $\psi$ 是正则函数（如 $\ell_1$ 或 $\ell_2$）。FTRL 可以视为 OGD 的"代理"版本。对于自适应学习率：

$$\text{Regret}_T \leq 2G \sqrt{\sum_{t=1}^T \|\nabla \ell_t(\theta_t)\|_*^2}$$

#### AdaGrad (Duchi et al., 2011)

**核心公式**: 自适应调整每个维度的学习率：

$$\theta_{t+1, i} = \theta_{t, i} - \eta \frac{g_{t, i}}{\sqrt{\sum_{s=1}^t g_{s, i}^2}}$$

其中 $g_{t, i}$ 是 $\nabla \ell_t(\theta_t)$ 的第 $i$ 个分量。AdaGrad 的遗憾界：

$$\text{Regret}_T \leq O\left(\max_i \| \theta_{1:T, i} \|_2 \cdot \sqrt{\sum_{t=1}^T \|\nabla \ell_t(\theta_t)\|_2^2}\right)$$

### 7.2 对比表格

| 维度 | OGD | FTRL | AdaGrad | **SCX Self-Evolution** |
|------|-----|------|---------|----------------------|
| **更新规则** | $\theta_{t+1} = \Pi(\theta_t - \eta_t \nabla \ell_t)$ | $\theta_{t+1} = \arg\min_\theta (\sum_{s=1}^t \ell_s + \psi)$ | $\theta_{t+1,i} = \theta_{t,i} - \eta g_{t,i}/\sqrt{\sum g_{t,i}^2}$ | $S_{t+1} \gets \text{BayesUpdate}(S_t, M_t)$; $\theta_{t+1} \gets \text{GD}(\theta_t, S_t)$ |
| **遗憾界** | $O(GD\sqrt{T})$ | $O(G\sqrt{\sum \|\nabla\|_*^2})$ | $O(\max \|\theta_{1:T}\|_2 \sqrt{\sum \|\nabla\|_2^2})$ | $O(GR\sqrt{T})$（Theorem 7, 延迟反馈） |
| **耦合系统？** | 单变量 $\theta_t$ | 单变量 $\theta_t$ | 单变量 $\theta_t$ | **耦合** $(S_t, \theta_t, M_t)$ |
| **延迟处理** | 无 | 无 | 无 | **有**（Theorem 8: 延迟反馈 Regret $\leq 2GR\sqrt{T} + G^2 D_{\max}\sqrt{T}$） |
| **凸性要求** | 凸损失 + 凸集 | 凸损失 | 凸损失 | **非凸**（NEP 损失非凸） |
| **记忆机制** | 无（一步遗忘） | 隐式（损失累积） | 隐式（梯度平方累积） | **显式**（记忆库 $M_t$） |
| **收敛保证** | $O(1/\sqrt{T})$ 遗憾 | $O(1/\sqrt{T})$ 遗憾 | $O(1/\sqrt{T})$ 遗憾（自适应） | **几乎必然收敛**（Theorem SE-1）到不动点 |

### 7.3 关键问题分析

**问题**: SCX 的 regret bound 与 OGD 的 $\sqrt{T}$ regret 相比是否更紧？

**诚实回答**: **SCX 的 regret bound 不更紧——它在结构上不同，且不完全可比。**

**具体比较**：

1. **SCX 的遗憾界（来自 `03_online_learning_regret.md` Theorem 7）**：
   $$\text{Regret}_T \leq 2GR\sqrt{T}$$
   其中 $G$ 是梯度上界，$R$ 是参数空间半径。这个形式与 OGD 的 $2GD\sqrt{T}$ 完全相同（只是 $D$ 与 $R$ 的符号差异）。**在常数意义上，SCX 的遗憾界与 OGD 等价，没有改进。**

2. **SCX 有延迟反馈版本（Theorem 8）**：
   $$\text{Regret}_T \leq 2GR\sqrt{T} + G^2 D_{\max}\sqrt{T}$$
   额外项 $+ G^2 D_{\max}\sqrt{T}$ 是 OGD 没有的（OGD 假设即时反馈）。这意味着 SCX 的遗憾界实际上比标准 OGD 弱，因为多了一个正项。

3. **但 SCX 的结果形式上更丰富**：
   - OGD 只有一个更新序列 $\theta_t$。
   - SCX 有两个耦合序列：$S_t$（gatekeeper）和 $\theta_t$（NEP 学生），还有记忆库 $M_t$。SCX 的遗憾是在这个耦合系统上定义的，比 OGD 要复杂得多。
   - SCX 还有 Theorem SE-1 的几乎必然收敛（在有限状态空间 + Robbins-Monro 条件下），这在 OGD 中没有等价物（OGD 给出遗憾界但不保证参数收敛）。

4. **SCX 的假设更强**：
   - OGD 只需要凸损失 + 有界梯度。
   - SCX 需要 SE-A1 到 SE-A6（包括 Lyapunov 下降假设、有限结构空间、Lipschitz 条件、Robbins-Monro 条件等）。

**诚实判定**: SCX 的遗憾界 $O(\sqrt{T})$ 与 OGD 同阶，**不更紧**。SCX 在理论上的真正增量是**耦合动力系统的几乎必然收敛**（Theorem SE-1），这与 OGD 的遗憾分析是不同类型的理论结果。一个是收敛性分析（$\theta_t \to \theta^*$ a.s.），另一个是竞争性分析（Regret vs 最优固定参数）。两者不能直接比较。

---

## 8. MLIP 势函数 (Machine-Learned Interatomic Potentials)

### 8.1 竞争者概述

#### ACE (Drautz, 2019) — Atomic Cluster Expansion

**核心公式**: 将原子环境展开为基函数的线性组合：

$$E_i = \sum_{v} c_v \cdot B_{iv}(\{\boldsymbol{r}_{ij}\}_{j})$$

其中 $B_{iv}$ 是原子环境 $\{\boldsymbol{r}_{ij}\}$ 的对称函数（通过体-函数-积分的张量积构造，保持旋转-反射不变性）。ACE 的核心数学工具是**广义克利布施-戈登系数**来构建 $O(3)$ 不变的 $B_{iv}$ 基函数。

$$\phi_i = \bigotimes_{v=1}^\nu \bigotimes_{j \neq i} R_{n_v l_v m_v}(\boldsymbol{r}_{ij}) \quad \Rightarrow \quad B_i = \text{Clebsch-Gordon}(\phi_i)$$

#### MACE (Batatia et al., 2022)

**核心公式**: 将 ACE 的线性展开替换为**消息传递**（message passing）的等变神经网络：

$$\mathbf{m}_i^{(t+1)} = \sum_{j \in \mathcal{N}(i)} \sum_{k} W_{tk}(\boldsymbol{r}_{ij}) \cdot \mathbf{h}_j^{(t)}$$

其中 $\mathbf{h}_j^{(t)}$ 是节点 $j$ 在第 $t$ 层的特征，$W_{tk}(\boldsymbol{r}_{ij})$ 是等变的消息函数。MACE 将 ACE 的效率（使用对称基）与消息传递的表达能力结合。

**预训练模型**: MACE-MP-0（Batatia et al., 2023）是在材料项目（MP）数据集上预训练的通用势，涵盖 89 种元素。

#### CHGNet (Deng et al., 2023)

**核心公式**: 基于图神经网络的预训练势函数，使用晶体图表示：

$$E = \sum_{i} E_i(\{\mathbf{h}_j \mid j \in \mathcal{N}(i)\}), \quad \mathbf{h}_i^{(t+1)} = \text{Update}( \mathbf{h}_i^{(t)}, \sum_{j \in \mathcal{N}(i)} \mathbf{m}_{ij}^{(t)} )$$

CHGNet 的关键创新：使用**轨道场线性化**（orbital field linearization）和**磁矩**作为额外的自由度来捕捉磁性。预训练在 Materials Project 的 16 万结构上。

#### M3GNet (Chen & Ong, 2022)

**核心公式**: 用于材料的三键图神经网络（Multi-Graph），用三种键：键长、键角、二面角：

$$E = \sum_{i} f_{\text{atom}}(\mathbf{h}_i), \quad \mathbf{h}_i = \text{M3G}(\{\boldsymbol{r}_{ij}\}, \{\boldsymbol{r}_{ijk}\}, \{\boldsymbol{r}_{ijkl}\})$$

M3GNet 扩展到包含 $\mathbf{E}(3)$ 等变性（SO(3) × $\mathbb{R}^3$），支持张量属性（应力、力常数）的预测。

#### SevenNet (Peng et al., 2024)

**核心公式**: 基于七元素（H, O, C, N, S, P, Cl）的通用势函数，使用等变图神经网络。核心设计是通过选择覆盖有机化学的主要元素来最大化预训练覆盖度。训练数据来自多个开放数据库的融合。在 MD 模拟的稳定性上优于之前的通用势。

#### ORB (Neumann et al., 2024)

**核心公式**: 基于等变 Transformer（Equiformer）的通用势函数。使用 $e^3\mathrm{nn}$ 框架的等变注意力机制：

$$\mathbf{h}_i' = \sum_{j \in \mathcal{N}(i)} \text{Attention}(\mathbf{h}_i, \mathbf{h}_j, \boldsymbol{r}_{ij}) \cdot \text{Value}(\mathbf{h}_j)$$

ORB 的预训练覆盖 89 种元素，在多种材料性质预测上达到 SOTA。关键差异：使用**等变注意力**（Equiformer）替代简单的消息传递，增加了表达能力和对长程相互作用的捕获。

### 8.2 对比表格

| 维度 | ACE | MACE (MP-0) | CHGNet | M3GNet | SevenNet | ORB | **SCX-Life** |
|------|-----|------------|--------|--------|----------|-----|-------------|
| **核心方法** | 线性原子基展开 | 等变消息传递 + ACE | 图神经网络 + 轨道线性化 | 多键图网络 + E(3) 等变 | 等变 GNN + 有限元素 | 等变 Transformer | **数据估值 + 专家路由 + 噪声检测** |
| **训练数据量** | 小到中等（~1K 结构） | **大**（~160K MP 结构） | **大**（~160K） | **大**（~160K） | **大**（多库融合） | **大**（~160K） | 依赖领域（SCX 不提供预训练势） |
| **理论保证** | 无（线性拟合，无泛化界） | 无 | 无 | 无 | 无 | 无 | **有**（Theorem 1-5 全套） |
| **势函数合并** | 无 | **有**（MP-0 是合并结果） | **有**（预训练多元素） | **有**（预训练多元素） | **有**（7 元素） | **有**（89 元素） | 声称但**未实现**（EGP 合并算法在设计阶段） |
| **元素覆盖** | 单元素/二元 | 89 种 | 89 种 | 89 种 | 7 种 | 89 种 | 不限（框架层面） |
| **输出物理量** | 能量 + 力 | 能量 + 力 | 能量 + 力 + 磁矩 | 能量 + 力 + 应力 | 能量 + 力 | 能量 + 力 | 不直接预测——**管理势函数** |
| **计算效率** | **高**（线性） | 中等（消息传递） | 中等 | 中等 | 中等 | **低**（Transformer） | 低（需要 M 个势函数都预测） |
| **开源实现** | ACE.jl (Julia) | MACE (Python) | CHGNet (Python) | M3GNet (Python) | SevenNet (Python) | ORB (Python) | 内部 |

### 8.3 关键问题分析

**问题**: SCX 声称的"势函数合并"（EGP/SCX-Life）是否已有 MACE-MP-0 等预训练模型做得更好？

**诚实回答**: **是的，在当前（2026年6月）的状态下，MACE-MP-0 和 ORB 等通用势在"势函数合并"方面远超 SCX 的实现进度。**

**逐层分析**：

**第一层：SCX 的 EGP 是什么？**

Expert Governance Protocol (EGP) 是 SCX 框架中声称用于势函数合并的模块。其核心思路：
- 对每个势函数 $f_m$（ACE/NEP/MACE），学习一个"专家级修正" $\delta_m(\theta)$
- 通过 gauge-fixed 系数组合（$c_0 + c_Z$）合并多个势函数
- SCX 的噪声检测用于标记并移除训练数据中的低质量 DFT 标签

EGP 目前处于**设计阶段**（README 中提到 `distill/devirus.py` 是"待实现"状态）。没有实验结果。

**第二层：MACE-MP-0 等通用势的现状**

- MACE-MP-0 已经在 160K 材料项目（MP）结构上训练，涵盖 89 种元素的多域势函数。
- ORB 使用等变 Transformer 在类似数据集上训练。
- 这些模型不是"合并多个势函数"，而是**直接训练一个覆盖多元素的势函数**。这比"先有多个单元素/二元势函数再合并"的方式更直接、更统一、更可扩展。

**第三层：SCX 对比通用势的核心差异**

| 方面 | MACE-MP-0 等通用势 | SCX's 声称的势函数合并 |
|------|-------------------|---------------------|
| **数据来源** | 单一高质量数据集（MP） | 多个异构势函数的知识提取 |
| **训练** | 端到端联合训练 | 后处理合并（EGP） |
| **可扩展性** | 预训练后零微调 | 每次需要重新发现状态和评估 |
| **实现状态** | **成熟、已发表** | **设计阶段、未实现** |
| **理论保证** | 无 | 有（Theorem 1-5 覆盖检测和估值，但不直接支持合并的质量保证） |

**第四层：SCX 相较通用势的潜在优势**

- **数据效率**：如果目标系统对通用势来说是"分布外"（如非常规合金），通用势可能失败。SCX 可以用少量 DFT 数据（通过主动采集）在特定系统上微调。
- **可解释性**：SCX 的状态结构提供了比黑箱 GNN 更好的可解释性。
- **质量问题意识**：SCX 的 Theorem 2（特征弱点诊断）和 Proposition 6（稳定性诊断）提供了通用势完全没有的"自知之明"。

**诚实判定**: 在"势函数合并"这个具体任务上，MACE-MP-0 和 ORB 等通用势确实比 SCX 当前阶段**做得更好、更成熟、更有实证支持**。SCX 的理论保证在合并任务上**没有直接证明**——Theorem 1-5 主要覆盖噪声检测和数据价值评估，没有定理保证合并后的势函数质量比原势函数更好。

SCX 的潜在优势在未来可能实现（当 EGP 实现并验证后），但在当前的基准比较中，SCX 在 MLIP 势函数领域的**实证成熟度显著弱于**现有通用势。

---

## 9. SCX 相对位置矩阵

### 9.1 竞争者 × 10 维度矩阵

维度说明：
- **检测保证**：是否有 F1/检测的正式理论保证
- **公理化**：是否有公理系统支持
- **状态条件化**：是否使用状态/分组结构
- **噪声-困难区分**：是否能区分噪声和困难样本
- **多模型使用**：是否利用多个模型/专家
- **计算效率**：前向计算的复杂度是否现实
- **实证成熟度**：是否有已发表的实证结果
- **聚合 vs 逐点**：操作在聚合级还是逐点级
- **自知之明**：是否有"知道自己不知道"的诊断机制
- **端到端优化**：所有组件是否联合训练

| 竞争者 | 检测保证 | 公理化 | 状态条件化 | 噪声-困难区分 | 多模型使用 | 计算效率 | 实证成熟度 | 聚合 vs 逐点 | 自知之明 | 端到端优化 |
|--------|:-------:|:------:|:---------:|:------------:|:---------:|:--------:|:---------:|:----------:|:--------:|:---------:|
| **Dawid-Skene** | ✗ | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | 聚合 (标签) | ✗ | ✓ |
| **Raykar et al.** | ✗ | ✗ | ✗ | ✗ | ✓ | ~ | ✓ | 聚合 (标签) | ✗ | ✓ |
| **Platanios et al.** | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | 聚合 (标签) | ✗ | ✗ |
| **Confident Learning** | ~ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 聚合 (类) | ✗ | ✓ |
| **MentorNet** | ✗ | ✗ | ✗ | ✗ | ✗(2个) | ~ | ✓ | 逐点 | ✗ | ✓ |
| **ELR** | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 逐点 | ✗ | ✓ |
| **DivideMix** | ✗ | ✗ | ✗ | ~ | ✓(2个) | ~ | ✓ | 逐点 | ✗ | ✓ |
| **Data Shapley** | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 逐点 (采样级) | ✗ | ✗ |
| **Data-OOB** | ✗ | ~ | ✗ | ✗ | ✓(bagging) | ~ | ✓ | 逐点 | ✗ | ~ |
| **DVRL** | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | 逐点 | ✗ | ✓ |
| **LAVA** | ✗ | ✗ | ✗ | ~(标签价值) | ✗ | ~ | ✓ | 逐点 | ✗ | ✗ |
| **HME** | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | 逐点 (门控) | ✗ | ✓ |
| **Sparse MoE** | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | 逐点 (门控) | ✗ | ✓ |
| **Switch TF** | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | 逐点 (门控) | ✗ | ✓ |
| **Soft MoE** | ✗ | ✗ | ✗ | ✗ | ✓ | ~ | ✓ | 逐点 (门控) | ✗ | ✓ |
| **Uncertainty** | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 逐点 | ✗ | ✓ |
| **QBC** | ~ | ✗ | ✗ | ✗ | ✓ | ~ | ✓ | 逐点 | ✗ | ✓ |
| **BADGE** | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | 簇 (梯度) | ✗ | ✓ |
| **BAAL** | ✗ | ✗ | ✗ | ✗ | ✗(MC) | ~ | ✓ | 逐点 | ✗ | ✓ |
| **TypiClust** | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 簇 (密度) | ✗ | ✗ |
| **GP-UCB** | ✓(遗憾) | ✗ | ✗ | ✗ | ✗(GP) | ~ | ✓ | 逐点 | ~(GP后验) | ✓ |
| **EI** | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | 逐点 | ~ | ✓ |
| **qNEHVI** | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | 批量 | ~ | ✓ |
| **OGD** | ✓(遗憾) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 逐点 | ✗ | ✓ |
| **FTRL** | ✓(遗憾) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 逐点 | ✗ | ✓ |
| **AdaGrad** | ✓(遗憾) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 逐点 | ✗ | ✓ |
| **ACE** | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | 原子级 | ✗ | ✓ |
| **MACE** | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | 原子级 | ✗ | ✓ |
| **CHGNet** | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | 原子级 | ✗ | ✓ |
| **ORB** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | 原子级 | ✗ | ✓ |
| **SCX** | **✓** | **~**(部分) | **✓** | **✓**(Thm3) | **✓**(M≥10) | **~** | **~** | **聚合 (状态)** | **✓**(Prop6) | **✗** |

### 9.2 SCX 的相对优势区域（✓ 优势明显）

1. **检测保证**：SCX 是唯一提供 F1 下界（Theorem 1）和精确最小最大常数（Theorem 4'）的框架。
2. **状态条件化**：SCX 是唯一将"状态"作为核心概念的理论框架。
3. **噪声-困难区分**：虽然 Theorem 3 证明无法完全区分，但 SCX 是唯一**正式承认并量化**这一局限的框架。
4. **自知之明**：Proposition 6 的稳定性诊断和 Theorem 2 的特征弱点界是竞争者在同等深度上没有的。
5. **多模型使用**：SCX 利用 M 个独立训练专家，而不是单个模型或 MC-Dropout。

### 9.3 SCX 的相对劣势区域（✗ 需诚实承认）

1. **端点优化**：SCX 的组件（状态发现、噪声检测、路由、采集）不是端到端联合训练的。这是与 MoE、主动学习等方法的核心差距。
2. **公理化**：SCX 的 $V(s)$ 和 $L(s)$ 等评分函数缺乏公理基础。Data Shapley 在这方面更强。
3. **实证成熟度**：SCX 目前只有小规模实验验证（CIFAR-10, AlN v3），远不如 Confident Learning、DivideMix、MACE 等方法的广泛验证。
4. **计算效率**：SCX 需要 M 个独立训练的专家和聚类步骤。在大规模场景下，Confident Learning 或 ELR 的单模型方案更高效。
5. **样本级精度**：SCX 操作在状态级而非样本级。当状态内异构性大时，状态级决策可能错过细粒度模式。
6. **均匀噪声假设（A4）**：SCX 的理论保证依赖于均匀噪声假设。在实际中噪声可能不是均匀的（如标签噪声偏向某些类），此时 Theorem 1 的保证可能不成立。Confident Learning 的联合分布估计没有这种假设。

### 9.4 关键维度的 SCX 定位

```
                    检测保证 (Theorems 1, 4')
                    +
    SCX ─────────────|───────────────────
                    |                    \
     实证成熟度 ----|----                \
                    |   \                 \
     自知之明 ------|----|----             \
                    |   |    \              \
     状态条件化 ----|----|----|----          \
                    |   |    |    \           \
     噪声-困难区分 -|----|----|----|---        \
                    |   |    |    |   \         \
     端到端优化 ----|----|----|----|----|----------(All MoE/AL methods)
                    |   |    |    |    |
                    +---+----+----+----+----> 更具优势的方向
                   Shapley MoE AL  BO
                   (公理) (联 (点 (连续
                         合)  级)  目标)
```

---

## 10. 总体评价

### 10.1 最有力的竞争者对比

| SCX 核心主张 | 最接近的竞争者 | 对比结论 |
|-------------|--------------|---------|
| "多专家共识检测噪声" | Confident Learning | 两者互补。SCX 需多专家，CL 需单模型置信度。SCX 有理论保证，CL 经验性强。 |
| "状态条件化比全局化好" | Dawid-Skene (per-annotator) | DS 是标注者级，SCX 是样本状态级。目标不同（噪声检测 vs 标签估计）。 |
| "状态路由优于门控网络" | Sparse MoE | 两者不同。SCX 可解释、支持异构，MoE 端到端优化。SCX 不严格优于 MoE。 |
| "V(s) 驱动主动采集" | Data Shapley | Data Shapley 有公理基础，SCX 无。但 SCX 的计算成本低一个数量级。 |
| "在线自进化闭环" | OGD / AlphaZero | SCX 的遗憾界与 OGD 同阶（$O(\sqrt{T})$），不更紧。耦合系统收敛是新贡献。 |
| "势函数合并" | MACE-MP-0 / ORB | 通用势在实现和实证上远超 SCX 当前阶段。SCX 的理论保证不直接覆盖合并质量。 |

### 10.2 四个理论层面

1. **最坚实的层面**（噪声检测）：Theorem 1 - 4' 构成一个完整的最小最大检测理论，在领域内是原创的。与 Confident Learning 等互补。

2. **中等坚实的层面**（特征-状态关系）：Theorem 2 + 5 + Proposition 6 提供了从特征质量到检测性能的完整链式保证。No Free Lunch 类比恰当。

3. **形式化但较弱验证的层面**（自进化）：Theorem SE-1 和 SE-2 是标准动力系统 + 随机逼近理论的适配。新颖性在耦合系统，但假设较强（Lyapunov 下降假设是直接假设而非推导结果）。

4. **最弱的层面**（MLIP 势函数合并）：EGP/SCX-Life 目前只有架构设计，没有实证结果。通用势已经在此方向上远更成熟。

### 10.3 诚实结论

SCX 并非在 8 个领域都优于所有竞争者。它的真正贡献在**噪声检测理论**（Theorem 1 + 4' 的最小最大 F1 最优）和**特征-状态-检测的统一链式分析**（Theorem 2 → 5 → Prop 6）。在其他领域（主动学习、在线学习、势函数合并），它提供的是**已有的理论框架的适配或扩展**，而非颠覆性创新。

SCX 对自身局限的诚实（Theorem 3 的不识别性、Theorem 2 的特征弱点界、Proposition 6 的阈值启发式）是其相对于大多数竞争者（它们只报喜不报忧）的一个真正优势。

---

*本分析由 Codex orchestrator agent 3 (竞争者扫描) 生成，2026-06-28*
