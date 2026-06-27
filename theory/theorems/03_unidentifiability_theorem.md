# Theorem 3: Unidentifiability of Noise vs. Learnable Difficulty

> **核心主张**: 仅凭观测数据 $(x, y, \{f_m(x)\})$ 无法区分标签噪声与样本内在困难度。SCX 框架的假设 (A1)-(A6) 不是任意的技术条件，而是打破这种不可识别性的最小充分条件。
>
> **修正记录**: 2026-06-27 — 初版完成。

---

## 1 定理陈述 (Theorem Statement)

### 1.1 符号与设定

沿用 Theorem 1 的符号体系，补充以下记号：

| 符号 | 含义 |
|------|------|
| $\mathcal{X}$ | 输入空间 |
| $\mathcal{Y}$ | 标签空间，$|\mathcal{Y}| = K$ |
| $y^* \in \mathcal{Y}$ | 真实标签（潜在变量，**不可观测**） |
| $y \in \mathcal{Y}$ | 观测标签 |
| $\{f_m\}_{m=1}^M$ | $M$ 个专家模型 |
| $\mathcal{D}_{\text{obs}}$ | 观测数据分布，$(X, Y, \{f_m(X)\}) \sim \mathcal{D}_{\text{obs}}$ |
| $\mathcal{S}$ | 状态空间 |
| $s: \mathcal{X} \to \mathcal{S}$ | 状态分配函数 |
| $\eta(x) = \mathbb{P}(Y \neq Y^* \mid X = x)$ | 输入依赖的噪声率 |

**潜在变量模型**: 数据生成由以下潜在过程决定：

1. 真实标签 $y^*$ 由 $x$ 通过未知 Oracle $f^*$ 生成：$y^* = f^*(x)$
2. 观测标签 $y$ 可能因噪声偏离 $y^*$
3. 专家预测 $\{f_m(x)\}$ 是 $x$ 和训练数据的函数
4. 状态 $s(x)$ 是 $\mathcal{X}$ 到 $\mathcal{S}$ 的映射，描述输入的内在特征

**观测空间**: 研究者仅能访问 $(x_i, y_i, f_1(x_i), \dots, f_M(x_i))$ 的联合分布，无法直接观测 $y^*$、$s(x)$ 或噪声指示变量。

### 1.2 形式化陈述

**Theorem 3 (Noise-Difficulty Unidentifiability).** 对任意 $K \geq 2$ 类分类问题，任意 $M \geq 1$ 个专家，任意有限状态空间 $\mathcal{S}$，存在两个不同的数据生成过程 $\mathcal{P}_1$ 和 $\mathcal{P}_2$ 使得：

**(i)** 在 $\mathcal{P}_1$ 下，观测标签 $y$ 的某些错误由**标签噪声**（label noise）导致：即 $y \neq y^*$，且 $y^*$ 是真实无误的。

**(ii)** 在 $\mathcal{P}_2$ 下，所有观测标签 $y$ 等于真实标签 $y^*$，但某些样本具有**内在困难度**（intrinsic hardness）：专家系统性地犯错并非因为标签错误，而是因为样本本身的歧义性。

**(iii)** 边际-条件分解恒等：两个过程产生完全相同的观测联合分布：

$$\mathcal{P}_1\bigl(x, y, \{f_m(x)\}_{m=1}^M\bigr) = \mathcal{P}_2\bigl(x, y, \{f_m(x)\}_{m=1}^M\bigr), \quad \forall (x, y, \{f_m\}) \in \mathcal{X} \times \mathcal{Y} \times \mathcal{Y}^M$$

**(iv)** 因此，任意算法 $\mathcal{A}: (\mathcal{X} \times \mathcal{Y} \times \mathcal{Y}^M)^n \to \{0,1\}^n$（将 $n$ 个观测映射到"噪声/非噪声"判定）无法同时正确识别两个世界中的噪声：在至少一个世界中的期望错误率至少为 $\eta\rho/2$（其中 $\eta$ 为噪声率，$\rho$ 为歧义状态的比例）。特别地，当 $\eta > 0$ 且 $\rho > 0$ 时该下界严格为正，证明两个世界无法被完美区分。

> **解读**: 定理 3 表明，在不附加额外假设的条件下，"这个样本的标签是错的"和"这个样本太难了所以专家都做错"是观测上等价的命题。SCX 框架必须引入假设 (A1)-(A6) 来打破这种等价性。

---

## 2 证明 (Proof)

### 2.1 构造框架

采用**构造性反例法**（constructive counterexample）。构造两个世界 $\mathcal{P}_{\text{noise}}$（噪声世界）和 $\mathcal{P}_{\text{hard}}$（困难世界），使得它们产生相同的观测分布但有根本不同的因果解释。

设二分类问题 $K = 2$，标签空间 $\mathcal{Y} = \{0, 1\}$。设 $M \geq 1$ 个专家。定义两个互斥的状态 $s_1, s_2 \in \mathcal{S}$。

### 2.2 世界 A：噪声驱动 (Noise-Driven)

在 $\mathcal{P}_{\text{noise}}$ 下：

**状态 $s_1$**（"清洁易懂"状态）：
- 样本占比：$\mathbb{P}(X \in s_1) = \rho$，其中 $\rho \in (0, 1)$
- 真实标签恒定：对所有 $x \in s_1$，$y^* = 0$
- 噪声机制：标签以概率 $\eta \in (0, 1/2)$ 被翻转
  $$\mathbb{P}(y \neq y^* \mid x \in s_1) = \eta$$
- 专家准确率：对清洁样本，所有专家独立地以 $1 - \varepsilon_1$ 概率正确预测 $y^*$
  $$\mathbb{P}(f_m(x) = y^* \mid x \in s_1, \text{clean}) = 1 - \varepsilon_1, \quad \varepsilon_1 \in (0, 1/2)$$

**状态 $s_2$**（"困难"状态）：
- 样本占比：$\mathbb{P}(X \in s_2) = 1 - \rho$
- 真实标签恒定：对所有 $x \in s_2$，$y^* = 0$
- 无噪声：$\mathbb{P}(y \neq y^* \mid x \in s_2) = 0$
- 专家准确率较低（该状态对专家来说普遍困难）：
  $$\mathbb{P}(f_m(x) = y^* \mid x \in s_2) = 1 - \varepsilon_2, \quad \varepsilon_1 < \varepsilon_2 \leq 1/2$$

### 2.3 世界 B：难度驱动 (Difficulty-Driven)

在 $\mathcal{P}_{\text{hard}}$ 下：

**状态 $s_1$**（"含难例"状态）：
- 样本占比：$\mathbb{P}(X \in s_1) = \rho$（与世界 A 相同）
- **所有标签均为真实标签**（无噪声）：$y = y^*$ 对所有样本
- 但真实标签本身具有歧义性：
  $$\mathbb{P}(y^* = 0 \mid x \in s_1) = 1 - \eta, \quad \mathbb{P}(y^* = 1 \mid x \in s_1) = \eta$$
  其中 $\eta$ 与世界 A 的噪声率相同
- 专家条件准确率：给定真实标签，专家的预测行为如下：
  - 当 $y^* = 0$ 时：$\mathbb{P}(f_m(x) = 0 \mid x \in s_1, y^* = 0) = 1 - \varepsilon_1$
  - 当 $y^* = 1$ 时：$\mathbb{P}(f_m(x) = 0 \mid x \in s_1, y^* = 1) = 1 - \varepsilon_1$
  
  即专家总是倾向于预测类别 $0$（偏向性），与真实标签无关。因此：
  - 当 $y^* = 0$ 时，专家准确率为 $1 - \varepsilon_1$（表现良好）
  - 当 $y^* = 1$ 时，专家准确率为 $\varepsilon_1$（系统性地犯错）

**状态 $s_2$**（"困难"状态）：
- 样本占比：$\mathbb{P}(X \in s_2) = 1 - \rho$（与世界 A 相同）
- 所有标签为真实标签：$y = y^*$，且 $\mathbb{P}(y^* = 0 \mid x \in s_2) = 1$
- 专家准确率：$\mathbb{P}(f_m(x) = y^* \mid x \in s_2) = 1 - \varepsilon_2$（与世界 A 相同）

### 2.4 世界等价性验证

现验证两个世界的观测联合分布恒等。观测数据为 $(x, y, f_1(x), \dots, f_M(x))$，其联合分布可分解为：

$$\mathcal{P}(x, y, f_1, \dots, f_M) = \mathcal{P}(x) \cdot \mathcal{P}(y \mid x) \cdot \prod_{m=1}^M \mathcal{P}(f_m \mid x)$$

其中第二步使用了 Theorem 1 的假设 (A1)-(A2)（专家在给定 $x$ 下条件独立）——但注意此处我们**不要求**该假设普遍成立，只是在构造中使其成立以产生最简洁的反例。

**Step 1: 边际分布 $\mathcal{P}(x)$**

两世界中 $\mathcal{P}(X \in s_1) = \rho$，$\mathcal{P}(X \in s_2) = 1 - \rho$。恒等。

**Step 2: 条件标签分布 $\mathcal{P}(y \mid x)$**

在 $\mathcal{P}_{\text{noise}}$ 中（世界 A，状态 $s_1$）：
$$\begin{aligned}
\mathcal{P}_{\text{noise}}(y = 0 \mid s_1) &= \mathbb{P}(\text{clean}) \cdot \mathbb{P}(y = y^* \mid \text{clean}) + \mathbb{P}(\text{noise}) \cdot \mathbb{P}(y = y^* \mid \text{noise}) \\
&= (1 - \eta) \cdot 1 + \eta \cdot 0 = 1 - \eta \\
\mathcal{P}_{\text{noise}}(y = 1 \mid s_1) &= (1 - \eta) \cdot 0 + \eta \cdot 1 = \eta
\end{aligned}$$

在 $\mathcal{P}_{\text{hard}}$ 中（世界 B，状态 $s_1$）：
$$\begin{aligned}
\mathcal{P}_{\text{hard}}(y = 0 \mid s_1) &= \mathbb{P}(y^* = 0 \mid s_1) = 1 - \eta \\
\mathcal{P}_{\text{hard}}(y = 1 \mid s_1) &= \mathbb{P}(y^* = 1 \mid s_1) = \eta
\end{aligned}$$

对状态 $s_2$，两世界均无噪声/歧义：
$$\mathcal{P}(y = 0 \mid s_2) = 1, \quad \mathcal{P}(y = 1 \mid s_2) = 0$$

因此条件标签分布在两世界中恒等。$\checkmark$

**Step 3: 条件专家分布 $\mathcal{P}(f_m \mid x)$**

在 $\mathcal{P}_{\text{noise}}$ 中（世界 A，状态 $s_1$）：
- 专家预测分布由真实标签 $y^*$ 训练/习得决定，不依赖观测标签 $y$：
  $$\mathcal{P}_{\text{noise}}(f_m = 0 \mid s_1) = \mathbb{P}(f_m = y^* \mid s_1) = 1 - \varepsilon_1$$
  $$\mathcal{P}_{\text{noise}}(f_m = 1 \mid s_1) = \varepsilon_1$$

在 $\mathcal{P}_{\text{hard}}$ 中（世界 B，状态 $s_1$）：
$$\begin{aligned}
\mathcal{P}_{\text{hard}}(f_m = 0 \mid s_1) &= \mathbb{P}(y^* = 0 \mid s_1) \cdot \mathbb{P}(f_m = 0 \mid s_1, y^* = 0) \\
&\quad + \mathbb{P}(y^* = 1 \mid s_1) \cdot \mathbb{P}(f_m = 0 \mid s_1, y^* = 1) \\
&= (1 - \eta) \cdot (1 - \varepsilon_1) + \eta \cdot (1 - \varepsilon_1) \\
&= 1 - \varepsilon_1
\end{aligned}$$

$$\begin{aligned}
\mathcal{P}_{\text{hard}}(f_m = 1 \mid s_1) &= (1 - \eta) \cdot \varepsilon_1 + \eta \cdot \varepsilon_1 = \varepsilon_1
\end{aligned}$$

对状态 $s_2$ 两世界相同：$\mathcal{P}(f_m = 0 \mid s_2) = 1 - \varepsilon_2$，$\mathcal{P}(f_m = 1 \mid s_2) = \varepsilon_2$。

因此条件专家分布在两世界中恒等。$\checkmark$

**Step 4: 条件独立性验证**

在两世界中，我们构造的专家在给定 $x$（或等价地，给定 $s(x)$）下条件独立。这是因为：
- 在世界 A 中，专家的训练数据独立（由假设 A1 直接给出）
- 在世界 B 中，专家的预测误差在给定状态和真实标签下独立

因此 $\prod_{m=1}^M \mathcal{P}(f_m \mid x)$ 的分解成立，且各因子在两世界间匹配。$\checkmark$

**Step 5: 联合分布恒等**

综合 Step 1-4 得：

$$\mathcal{P}_{\text{noise}}\bigl(x, y, \{f_m\}\bigr) = \mathcal{P}_{\text{hard}}\bigl(x, y, \{f_m\}\bigr), \quad \forall (x, y, \{f_m\})$$

两世界的观测联合分布完全一致。$\square$ (证毕第 (iii) 部分)

### 2.5 算法不可区分性

由第 (iii) 部分，两世界产生观测上不可区分的联合分布。设 $\mathcal{A}$ 为任意算法，使用 $n$ 个观测样本 $D_n = \{(x_i, y_i, \{f_m(x_i)\})\}_{i=1}^n$ 输出每个样本的噪声判定 $z_i \in \{0, 1\}$。

定义两种判定含义：
- 在 $\mathcal{P}_{\text{noise}}$ 下：$z_i = 1$ 表示"该样本标签被翻转（噪声）"
- 在 $\mathcal{P}_{\text{hard}}$ 下：$z_i = 1$ 表示"该样本标签正确但专家系统犯错（困难）"

由于 $\mathcal{A}$ 仅依赖 $D_n$，而 $D_n$ 在两个世界中的分布完全相同：

$$\mathcal{L}_{\mathcal{P}_{\text{noise}}}(D_n) = \mathcal{L}_{\mathcal{P}_{\text{hard}}}(D_n)$$

其中 $\mathcal{L}$ 表示分布的 law。因此 $\mathcal{A}$ 的输出分布在两世界中相同：

$$\mathcal{L}_{\mathcal{P}_{\text{noise}}}(\mathcal{A}(D_n)) = \mathcal{L}_{\mathcal{P}_{\text{hard}}}(\mathcal{A}(D_n))$$

但在两世界中，**正确的"噪声"集不同**：
- $\mathcal{P}_{\text{noise}}$ 中真正噪声样本集 $\mathcal{Z}_{\text{noise}}^* = \{i: y_i \neq y_i^*\} = \{i: x_i \in s_1, y_i = 1\}$
- $\mathcal{P}_{\text{hard}}$ 中真正噪声样本集 $\mathcal{Z}_{\text{hard}}^* = \varnothing$（无噪声）

由于 $\mathcal{A}$ 无法区分两世界，其输出标记集 $\hat{\mathcal{Z}}$ 必须同时适用于两世界。令 $a$ 为算法在歧义子集 $\{i: x_i \in s_1, y_i = 1\}$ 上的期望标记率（该值在两世界中相同，因为观测分布相同）。在世界 A 中，这些样本均为噪声（正确标记为 $1$），错误率为 $(1-a)$；在世界 B 中，这些样本均非噪声（正确标记为 $0$），错误率为 $a$。因此：

$$\max\bigl(\text{Error}_{\mathcal{P}_{\text{noise}}}(\mathcal{A}), \text{Error}_{\mathcal{P}_{\text{hard}}}(\mathcal{A})\bigr) \geq \frac{\text{Error}_{\text{noise}} + \text{Error}_{\text{hard}}}{2} \geq \frac{\eta\rho}{2}$$

其中 $\eta\rho$ 是歧义子集在全部样本中的占比。该下界在 $a = 1/2$ 时达到（算法在歧义样本上等同于随机猜测）。对于典型噪声率 $\eta = 0.1$ 和 $s_1$ 占比 $\rho = 0.5$，下界为 $0.025$——虽小但严格为正，证明了两世界的不完全可区分性。定性的不可识别性结论（无法完美区分噪声与困难）仍然成立。$\square$ (证毕第 (iv) 部分)

### 2.6 扩展：一般 K 类分类

上述构造可直接推广到 $K > 2$ 的情况。只需将噪声模型改为均匀翻转（如 Theorem 1 的 A4），并在困难世界中将 $y^*$ 的分布设置为与噪声世界的观测标签分布一致。完整的推广证明见附录 A。

---

## 3 推论 (Corollaries)：哪些假设能打破不可识别性？

定理 3 表明，不加额外假设时噪声与困难是不可区分的。以下推论列出**充分条件**——每个条件单独出现即可打破不可识别性。

### 3.1 推论 1：锚点标签 (Anchor Points)

**Corollary 1 (Anchor Labels Break Unidentifiability).** 若对某个已知子集 $\mathcal{X}_{\text{anchor}} \subset \mathcal{X}$，研究者能够获取**真实标签** $y^*$（如人工复核），则噪声与困难在 $\mathcal{X}_{\text{anchor}}$ 上可区分。进一步地，若 $\mathcal{X}_{\text{anchor}}$ 覆盖了所有状态，则全局可区分。

**证明思路**：在锚点 $x \in \mathcal{X}_{\text{anchor}}$ 上，比较观测标签 $y$ 与真实标签 $y^*$：
- 若 $y \neq y^*$，则该样本必然含噪声
- 若 $y = y^*$ 但专家 $f_m(x) \neq y$，则该样本必然是"困难"的

将锚点上的专家错误率外推到非锚点样本，可打破全局不可识别性。$\square$

**与 SCX 的联系**：SCX 的"冷启动协议"（cold start protocol）依赖于少量人工审查样本作为锚点来初始化状态级噪声率估计。

### 3.2 推论 2：已知专家训练域 (Known Training Domains — A1)

**Corollary 2 (Known Disjoint Training Data Break Unidentifiability).** 若 $M$ 个专家在 $M$ 个**不相交**的数据子集上独立训练（假设 A1），且研究者知道这些训练集的构成，则噪声与困难可区分。

**证明思路**：不相交训练集意味着专家的错误模式是**独立的**（给定 $x$）。在噪声样本上，所有专家的错误率同时上升（因为所有专家的预测都针对真实 $y^*$，而观测标签 $y \neq y^*$）。在困难样本上，专家的错误可能相互独立（但每个专家的错误率本身更高）。

关键的数量差异：令 $\bar{e}(x) = \frac{1}{M}\sum_m \mathbf{1}\{f_m(x) \neq y\}$ 为平均专家错误率。在噪声样本上的条件分布为：

$$\mathbb{E}[\bar{e}(x) \mid \text{noise}] = 1 - \frac{1 - \mathbb{E}[\bar{e}(x) \mid \text{clean}]}{K-1}$$

（Theorem 1, Lemma 1）。这个关系在仅有硬度的世界中无法同时成立。因此，检验 $\bar{e}(x)$ 的分布是否满足 Lemma 1 的关系式可以区分两世界。$\square$

**重要说明**：推论 2 依赖于研究者**确切知道**训练集不相交。若训练集的关系未知，则无法应用此检验。

### 3.3 推论 3：噪声独立于输入 (Noise Independent of x — A4)

**Corollary 3 (Input-Independent Noise Rate Breaks Unidentifiability).** 若标签噪声率 $\eta(x) = \mathbb{P}(Y \neq Y^* \mid X = x)$ 是常数（不依赖于 $x$），且困难状态的专家错误率在状态间有差异，则噪声与困难可区分。

**证明思路**：若 $\eta(x) = \eta$ 为全局常数，则观测标签 $y$ 与专家错误 $\{f_m(x) \neq y\}$ 之间的相关性模式在噪声和困难世界中有本质差异。

在噪声世界中，$\bar{e}(x)$ 的期望值在清洁样本上低，在噪声样本上高，但噪声事件与 $x$ 独立，因此 $\bar{e}(x)$ 的条件分布不随 $x$ 变化（边际上），仅当以 $y$ 为条件时才显现差异。

在困难世界中，$y$ 的分布可能随 $x$ 变化，且专家错误率也随状态变化。通过检验 $\bar{e}(x)$ 和 $y$ 是否在整个输入空间上具有恒定的联合分布模式（即噪声世界的"均匀噪声"特征），可以区分两者。$\square$

### 3.4 推论 4：状态同质性 (State Homogeneity — A5)

**Corollary 4 (State Homogeneity Breaks Unidentifiability).** 若状态划分 $\mathcal{S}$ 使得在每个状态 $s$ 内，清洁样本的期望专家错误率 $\mu_s$ 被常数上界控制（假设 A5），且状态数 $|\mathcal{S}| \geq 2$ 并且不同状态间 $\mu_s$ 有差异，则噪声与困难可区分。

**证明思路**：在定理 3 的反例构造中，两个世界的状态 $s_1$ 和 $s_2$ 在状态同质性假设下会产生矛盾的 $\mu_s$ 估计。具体地，在以下两种解释中至多一种能满足状态同质性假设：

- **噪声解释**（世界 A）：状态 $s_1$ 的清洁错误率为 $\varepsilon_1$，但观测到 $\bar{e}(s_1) = (1-\eta)\varepsilon_1 + \eta(1-\varepsilon_1)$——这是噪声和清洁的混合。如果 $\eta$ 是未知的，无法在此状态下区分噪声和困难分量。

- **困难解释**（世界 B）：状态 $s_1$ 中 $\eta$ 比例样本的真实标签为类别 1，专家在该子群体上准确率仅为 $\varepsilon_1$。这等价于认为状态 $s_1$ 包含两个子状态（类别 0 的 $s_{1a}$ 和类别 1 的 $s_{1b}$），且它们的专家错误率不同。

状态同质性假设（A5）要求每个状态内清洁错误率均匀。如果 $s_1$ 的内部专家准确率在不同类别的样本间显著不同（世界 B 中为 $1-\varepsilon_1$ vs $\varepsilon_1$），则 (A5) 在此状态上被违反。因此，如果 (A5) 成立，世界 B 的构造不成立。$\square$

### 3.5 推论 5：平衡误差分布 (Balanced Error Distribution — A6)

**Corollary 5 (Balanced Error Distribution Breaks Unidentifiability).** 若专家的错误在所有错误类别上均匀分布（假设 A6，$C_{\text{bal}} = 1$），则噪声与困难可区分。

**证明思路**：在定理 3 的世界 B 构造中，专家预测偏向类别 0。当 $y^* = 1$ 时，专家以 $1 - \varepsilon_1$ 的高概率预测 0，这意味着在状态 $s_1$ 中，$f_m$ 的错误几乎全部集中在类别 1 → 预测为 0 的方向上。这违反了 A6 的平衡要求——专家的错误极度不平衡。

因此，如果已知专家的错误是平衡的（$C_{\text{bal}} \approx 1$），则世界 B 的构造被排除。$\square$

### 3.6 推论 6：多状态交叠 (Multi-State Overlap)

**Corollary 6 (Differential Expert Accuracy Across States Breaks Unidentifiability).** 若存在至少两个状态 $s_a, s_b \in \mathcal{S}$ 使得专家在 $s_a$ 上的准确率**高于**在 $s_b$ 上的准确率，并且研究者能够可靠地将样本分配到状态，则噪声与困难可区分。

**证明思路**：定理 3 的世界 A 在构造上依赖于状态 $s_1$ 同时包含清洁和噪声样本的混合，但其观测标签分布与状态 $s_2$ 不同。通过比较不同状态之间的一致性得分分布，可以检验"混合"假设是否成立。

具体地，设 $\mu_s = \mathbb{E}[C \mid \text{clean}, X \in s]$。在 Theorem 1 的 Lemma 1 中，噪声样本的一致性得分期望为 $1 - \mu_s/(K-1)$。若在某个状态中观测到一致性得分均值 $\bar{C}_s > 1 - \hat{\mu}_s/(K-1)$（其中 $\hat{\mu}_s$ 是从低分位数估计的清洁基线），则该状态中可能不存在噪声（即世界 B 类型）。$\square$

---

## 4 与 SCX 假设体系 (A1-A6) 的联系

定理 3 及其推论揭示了 SCX 假设 (A1)-(A6) 的根本作用：它们不是任意附加的技术条件，而是**打破不可识别性的最小充分条件**。

### 4.1 假设分类：哪些假设在打破什么

| 假设 | 内容 | 打破的歧义 | 对应推论 |
|------|------|-----------|---------|
| **A1** | 不相交训练集 | 专家独立性：确保噪声样本上所有专家同时出错的模式与干净样本不同 | 推论 2 |
| **A2** | 清洁条件独立 | 给定 $x$ 下专家错误的独立性分解 | 推论 2 的技术基础 |
| **A3** | 有界损失 | 技术性假设（Hoeffding 不等式所需），不直接打破不可识别性 | — |
| **A4** | 均匀独立噪声 | 噪声率的输入无关性和均匀分布：排除了 $x$ 依赖的噪声率导致的伪"困难"模式 | 推论 3 |
| **A5** | 状态同质性 | 状态内清洁错误率均匀：排除了"内在困难样本聚集在同一状态"的可能性 | 推论 4 |
| **A6** | 平衡误差分布 | 专家错误在所有错误类别上均匀：排除了专家偏向性导致的伪"困难"模式 | 推论 5 |

### 4.2 最小破坏性集合

A1-A6 中哪些是打破不可识别性的必要假设？分析如下：

**定理 3 反例的抵抗性**：定理 3 的构造使用了以下条件：
1. $K = 2$ 分类（最简单情况）
2. 专家条件独立（A1/2）
3. 噪声率依赖于状态（$\eta$ vs 0）——这与 A4 的"均匀独立噪声"有细微差别
4. 状态间专家错误率不同（$\varepsilon_1 \neq \varepsilon_2$）

要排除定理 3 的构造，**至少需要以下假设之一**：
- A1 的**不相交训练域知识**（推论 2）：若我们知道专家训练域确实不相交，世界 B 的构造可能违��专家独立性
- A4 的**均匀噪声**（推论 3）：若噪声率全局恒定，世界 A 的构造要求 $\eta$ 在 $s_1$ 和 $s_2$ 中相同，迫使重新设计
- A5 的**状态同质性**（推论 4）：若状态内错误率均匀，世界 B 的 $s_1$ 内 $y^*$ 依赖的错误率违反此假设
- A6 的**平衡误差分布**（推论 5）：若专家错误均匀分布，世界 B 的专家偏向性被排除

**因此，SCX 打破不可识别性所需的最小假设集合是**：
$$A_{\min} = \{A1, A4, A5\} \quad \text{或} \quad \{A1, A4, A6\} \quad \text{或} \quad \{A5, A6\} \text{ 加上状态数 } |\mathcal{S}| \geq 2$$

即至少需要**训练域独立性** + **噪声均匀性** + **一种错误均匀性条件**（状态内或类别间），或者**状态同质性** + **错误平衡性** + **多状态结构**。

### 4.3 假设违反时的退化

理解每个假设的角色后，可以建立违反各假设时的退化模式：

| 违反的假设 | 退化为 | 实际表现 |
|-----------|--------|---------|
| A1（训练域重叠） | 专家相关性导致 Theorem 1 的指数界消失 | SCX 噪声检测 F1 下降，但仍可能优于随机 |
| A4（噪声依赖 $x$） | 噪声率和特征难度耦合 | SCX 的噪声估计有偏，但相对排序可能保留 |
| A5（状态异质） | 状态内清洁/噪声混合 | Theorem 1 不适用，需要更细的状态划分 |
| A6（错误不均衡） | 噪声检测偏向常见错误类别 | 假阳性集中在特定类别，F1 下降但可能仍可用 |
| **全部违反** | 完全退化 | **定理 3 的不可识别性生效，任何算法无法区分噪声与困难** |

### 4.4 SCX 框架如何隐式使用这些条件

在实际的 SCX 应用中，A1-A6 并非总是明确检验的。框架通过以下机制**隐式**使用了打破不可识别性的结构：

1. **冷启动协议**：要求人工审查少量锚点样本生成初始状态标签（等价于推论 1 的锚点）。

2. **状态发现**：通过对 $\phi(X)$ 聚类来划分状态，隐含地假设 A5——聚类试图在每个簇内最小化变异，使状态同质性近似成立。

3. **多专家聚合**：使用不相交训练的专家（A1），这要求实验设计阶段明确分配训练数据。

4. **统计检验**：检查 $\hat{C}(s)$ 的经验分布是否满足 Lemma 1 的均值分离关系，若不满足则标记为"弱特征失效"（Theorem 2）。

---

## 5 与现有文献的联系

### 5.1 测量误差模型 (Measurement Error Models)

统计学的测量误差文献中有一个经典结论：在经典测量误差模型（classical measurement error model）下，若没有**验证数据**（validation data）或**工具变量**（instrumental variables），测量误差的分布与真实值的分布不可区分（Fuller, 1987; Carroll et al., 2006）。

形式化地，对模型 $Y = Y^* + U$，其中 $U$ 为测量误差：若仅观测到 $Y$ 而 $Y^*$ 和 $U$ 均未知，则有无穷多对 $(Y^*, U)$ 的分布满足观测到的 $Y$ 分布。这是**测量误差不可识别性**的标准结果。

Theorem 3 将此结果从连续测量误差扩展到分类标签噪声与专家困难的对称问题中。关键推广是：不仅有 $Y$ 和 $Y^*$ 的关系，还引入了专家预测 $\{f_m(X)\}$ 作为额外观测。我们证明即使有这些额外信息，不可识别性仍然成立——除非对 $\{f_m\}$ 的结构施加假设。

### 5.2 标签噪声理论的不可识别性

标签噪声文献中的经典结果是**噪声转移矩阵不可识别性**（Menon et al., 2015; Patrini et al., 2017）：

对 $K$ 类分类，噪声转移矩阵 $T \in [0,1]^{K \times K}$ 满足 $T_{ij} = \mathbb{P}(\tilde{Y} = j \mid Y^* = i)$。在仅观测到 $(\tilde{Y}, X)$ 的条件下，$T$ 和真实条件分布 $\mathbb{P}(Y^* \mid X)$ 的联合是不可识别的——除非加上充分条件（如 $T$ 的对角占优性、存在锚点、或存在多个噪声率已知的标注者）。

Theorem 3 是此结果向**多专家场景**的推广。在多专家场景中，我们不仅观测到 $\tilde{Y}$，还观测到 $\{f_m(X)\}$，但不可识别性仍然成立。关键洞察是：专家本身的错误模式可能来自 $Y^*$ 的困难区域，也可能来自 $Y^*$ 被翻转后的伪模式——这两者在观测上等价。

### 5.3 Dawid-Skene 的不可识别性

Dawid-Skene 模型（1979）中，每个标注者 $m$ 有一个混淆矩阵 $\pi_m$，真实标签 $Y^*$ 是潜在变量。标准结果是：在对称性约束（如固定一个标注者的混淆矩阵）或锚点标注者（某标注者完全可靠）的条件下，模型才可识别。

Theorem 3 与 Dawid-Skene 不可识别性的关系：
- Dawid-Skene 的不可识别性关注**不同标注者的混淆矩阵之间的置换对称性**（标签翻转问题）
- Theorem 3 关注**噪声与困难之间的语义不可区分性**——这是 SCX 特有的一阶问题
- 两者正交：即使解决了 Dawid-Skene 的标签置换问题（通过锚点标注者），Theorem 3 的不可识别性仍然存在

换言之，Dawid-Skene 解决的是"哪位标注者可靠"的问题，而 Theorem 3 揭示的是"样本为什么不可学"的问题——后者是前者的前提（在解释专家错误模式之前，需知错误来源）。

### 5.4 因果推断的视角

从因果推断的角度，Theorem 3 可被理解为一种**因果结构不可识别性**（causal structure unidentifiability; Pearl, 2009）：

考虑两个因果图：

**图 A（噪声因果图）**：
```
S → Y* → Y ← Noise
↓
X → {f_m}
```
其中箭头 $Y^* \to Y$ 表示真实标签决定观测标签，但 $Y$ 也可被外部噪声直接影响。

**图 B（困难因果图）**：
```
S → Y* (= Y)
↓
X → {f_m}
```
其中困难状态 $S$ 同时影响真实标签分布和专家准确率。

两个因果图生成相同的观测分布 $(X, Y, \{f_m\})$，但蕴含不同的因果解释。仅凭观测数据无法区分这两个图——这是典型的**马尔可夫等价类**（Markov equivalence class）问题。

### 5.5 混合模型与有限混合的可识别性

在有限混合模型（finite mixture models）文献中，可识别性通常要求分量分布具有特定的参数形式（如指数族），或要求分量数有上界（Teicher, 1963; McLachlan & Peel, 2000）。

Theorem 3 的反例可被视为一个**两分量混合模型**的不可识别性实例：
- 世界 A：分量 1（清洁，占 $1-\eta$）和分量 2（噪声，占 $\eta$）
- 世界 B：分量 1（$y^*=0$，占 $1-\eta$）和分量 2（$y^*=1$，占 $\eta$）

两个混合模型产生相同的观测联合分布，但分量有不同的语义解释。这表明在标签噪声场景中，即使分量数已知（$K=2$），标准的混合模型可识别性条件（如参数化形式已知）仍然不够——还需要对分量之间的"专家预测模式"施加额外的结构约束。

### 5.6 最小值与最大值：假设的必要性谱系

综合以上讨论，可得以下**假设必要性谱系**：

```
最弱假设 (不可识别)
├── 无假设 → Theorem 3 成立：完全不可识别
├── + 锚点标签 (推论 1) → 在锚点上可识别
├── + 不相交训练域 (A1, 推论 2) → 通过错误独立性检验可识别
├── + 均匀噪声 (A4, 推论 3) → 通过错误率的输入不变性可识别
├── + 状态同质性 (A5, 推论 4) → 通过状态内错误率均匀性可识别
├── + 错误平衡性 (A6, 推论 5) → 通过专家错误类别分布可识别
└── A1 + A4 + A5 (或 A1 + A4 + A6) → 完全可识别 (SCX 标准假设)
最强假设 (完全可识别)
```

---

## 6 实际意义

### 6.1 对 SCX 框架的正当性化

Theorem 3 为 SCX 的假设体系提供了根本性的正当性：

1. **A1-A6 不是过度假设**：它们是打破不可避免的不可识别性所需的最小附加结构。任何声称能在无假设条件下区分噪声与困难的方法，要么隐式包含了等价假设，要么存在理论缺陷。

2. **Theorems 1-3 共同构成逻辑闭环**：
   - Theorem 1：在 A1-A6 下，噪声可检测（正命题）
   - Theorem 2：当特征减弱检测能力（边界命题）
   - Theorem 3：无假设时噪声与困难不可区分（必要性命题）

3. **冷启动协议的理论基础**：SCX 要求初始阶段人工审查少量样本来估计状态级噪声率。Theorem 3 证明这是**理论必需**而非工程妥协——没有这个锚点，系统无法突破不可识别性。

### 6.2 对竞争方法的批判性分析

Theorem 3 提供了评价其他噪声检测方法的框架：

- **loss-based 方法**（如 MentorNet, Decoupling, Co-teaching）：隐式假设"高损失 = 噪声"，即在 Theorem 3 中选择了"世界 A"解释。当数据实际遵循"世界 B"模式时，这些方法会将困难样本误标为噪声。

- **置信学习方法**（Confidence Learning; Northcutt et al., 2021）：使用计数矩阵估计噪声转移矩阵，隐式假设专家（分类器）的计数与噪声率之间存在可分解关系。在 "世界 B" 中，该分解失效。

- **多视图方法**（Multi-view methods）：依赖多个独立视图的一致性，等价于 Theorem 1 的 A1-A2 假设。Theorem 3 证明，没有这些假设时多视图一致性也无法区分噪声与困难。

### 6.3 实验设计建议

基于 Theorem 3，提出以下实验设计原则：

1. **明确假设**：在论文或实验报告中明确列出所做假设（如"我们假设噪声与 x 独立"）。Theorem 3 意味着未列出的假设就是未满足的识别条件。

2. **敏感性分析**：检验结论对假设违反的敏感性。例如，若状态同质性稍弱（A5 不严格成立），噪声检测 F1 下降多少？

3. **假设检验**：设计统计检验来验证关键假设。例如，用 $\chi^2$ 检验专家错误是否均匀分布（检验 A6），或用 KS 检验状态间的一致性得分分布差异（检验 A5）。

4. **多方法交叉验证**：同时运行 SCX 和 loss-based 方法，将两者标记不一致的样本提交人工审查——这正是 SCX 冷启动协议的实际操作方式。

---

## 附录 A：K 类推广

将定理 3 推广到 $K > 2$。采用与二分类不同的构造策略——在世界 B 中，专家被构造为**完全随机**（不依赖真实标签），这使得联合分布在任意 $K$ 下保持恒等。

**世界 A（噪声）**：对所有 $x \in s_1$，$y^* = 0$。噪声机制：以概率 $\eta$ 将标签均匀翻转到 $\mathcal{Y} \setminus \{0\}$：
$$\mathbb{P}(y = c \mid \text{noise}, x \in s_1) = \frac{1}{K-1}, \quad c \neq 0$$

专家准确率：$\mathbb{P}(f_m(x) = y^* \mid x \in s_1) = 1 - \varepsilon_1$，错误均匀分布：
$$\mathbb{P}(f_m = c \mid s_1) = \frac{\varepsilon_1}{K-1}, \quad c \neq 0$$

观测分布为：
$$\mathcal{P}_{\text{noise}}(y = 0 \mid s_1) = 1 - \eta, \quad \mathcal{P}_{\text{noise}}(y = c \mid s_1) = \frac{\eta}{K-1}, \; c \neq 0$$
$$\mathcal{P}_{\text{noise}}(f_m = 0 \mid s_1) = 1 - \varepsilon_1, \quad \mathcal{P}_{\text{noise}}(f_m = c \mid s_1) = \frac{\varepsilon_1}{K-1}, \; c \neq 0$$

且由于 (A4) 噪声与专家独立，$y$ 与 $f_m$ 在给定 $s_1$ 下独立。

**世界 B（困难）**：对 $x \in s_1$，所有标签均为真实标签（无噪声）：
$$\mathbb{P}(y^* = 0 \mid s_1) = 1 - \eta, \quad \mathbb{P}(y^* = c \mid s_1) = \frac{\eta}{K-1}, \; c \neq 0$$

**关键构造**：在世界 B 中，专家**不学习**——其预测完全随机且独立于真实标签：
$$\mathbb{P}(f_m = 0 \mid s_1) = 1 - \varepsilon_1, \quad \mathbb{P}(f_m = c \mid s_1) = \frac{\varepsilon_1}{K-1}, \; c \neq 0$$
且 $f_m \perp y^* \mid s_1$（专家预测与真实标签独立）。

在此构造下：
- $y$ 的边际分布：两世界相同（世界 A 的噪声标签分布 = 世界 B 的真实标签分布）
- $f_m$ 的边际分布：两世界相同（均为 $1-\varepsilon_1$ 在类别 0，$\varepsilon_1/(K-1)$ 在其他类别）
- $(y, f_m)$ 的联合分布：两世界均为独立乘积（世界 A 中 $y$ 和 $f_m$ 因 (A4) 独立；世界 B 中 $f_m$ 是纯随机故也与 $y$ 独立）

因此对任意 $K \geq 2$，$\mathcal{P}_{\text{noise}}(x, y, \{f_m\}) = \mathcal{P}_{\text{hard}}(x, y, \{f_m\})$ 恒成立。$\square$

**解释**：世界 B 的构造中，"困难"的语义是极端的——该状态中**所有**样本对所有专家都同样困难（专家等同于随机猜测），无论真实标签是什么。这对应了实际中"特征完全无信息"的极限情况（Theorem 2 中 $\delta = 0$）。虽然极端，但它作为**存在性反例**已足够：存在至少一个以"困难"为解释的世界，其观测分布与以"噪声"为解释的世界完全相同，因此两者无法从观测数据中区分。

> **2026-06-27 修正**：原版附录 A 的构造中，世界 B 的专家在给定真实标签下具有非平凡的准确率 $1-\varepsilon_1$，这导致对于 $K>2$ 时专家边际分布与世界 A 不匹配。修正后的构造采用"完全随机专家"，保证了对任意 $K \geq 2$ 联合分布的恒等性。

---

## 附录 B：符号表

| 符号 | 含义 | 首次出现 |
|------|------|---------|
| $\mathcal{P}_{\text{noise}}$ | 噪声世界的数据生成过程 | 2.2 |
| $\mathcal{P}_{\text{hard}}$ | 困难世界的数据生成过程 | 2.3 |
| $\eta$ | 噪声率（世界 A）/ 标签歧义率（世界 B） | 2.2 |
| $\varepsilon_1$ | 状态 $s_1$ 上的专家错误率 | 2.2 |
| $\varepsilon_2$ | 状态 $s_2$ 上的专家错误率 | 2.2 |
| $\rho$ | 状态 $s_1$ 的边际概率 | 2.2 |
| $\mathcal{D}_{\text{obs}}$ | 观测数据分布 | 1.1 |
| $\mathcal{Z}^*$ | 真实噪声样本集 | 2.5 |

---

## 参考文献

1. Fuller, W. A. (1987). *Measurement Error Models*. Wiley.

2. Carroll, R. J., Ruppert, D., Stefanski, L. A., & Crainiceanu, C. M. (2006). *Measurement Error in Nonlinear Models: A Modern Perspective* (2nd ed.). Chapman and Hall/CRC.

3. Menon, A. K., Van Rooyen, B., Ong, C. S., & Williamson, R. C. (2015). Learning from corrupted binary labels via class-probability estimation. *ICML*.

4. Patrini, G., Rozza, A., Menon, A. K., Nock, R., & Qu, L. (2017). Making deep neural networks robust to label noise: A loss correction approach. *CVPR*.

5. Dawid, A. P., & Skene, A. M. (1979). Maximum likelihood estimation of observer error-rates using the EM algorithm. *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 28(1), 20-28.

6. Northcutt, C. G., Jiang, L., & Chuang, I. L. (2021). Confident learning: Estimating uncertainty in dataset labels. *Journal of Artificial Intelligence Research*, 70, 1373-1411.

7. Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.

8. Teicher, H. (1963). Identifiability of finite mixtures. *The Annals of Mathematical Statistics*, 34(4), 1265-1269.

9. McLachlan, G. J., & Peel, D. (2000). *Finite Mixture Models*. Wiley.

10. SCX Theorem 1: Multi-Expert Consistency Guarantees for Label Noise Detection. `./01_noise_detection_guarantee.md`.

11. SCX Theorem 2: Weak Feature Failure Lower Bound. `./02_weak_feature_failure.md`.

12. SCX Data Four-Classification. `../../knowledge/02_概念/数据四分类.md`.

13. SCX Data Poisoning Defense. `../../knowledge/02_概念/数据防中毒.md`.

---

**修正说明（2026-06-27）**：初版完成。定理 3 定位为 SCX 假设体系的"必要性支柱"——证明 A1-A6 非任意假设，而是打破不可识别性所需的最小结构条件。
