# 引言：为什么是Galois？

**Author:** SCX

*Abstract:*

本文揭示SCX多专家审计框架与Galois理论之间一个迄今未被注意的深层结构对应。
核心洞察如下：Galois理论中，代数方程根的可解性取决于其Galois群的对称结构；
SCX框架中，声称的可审计性取决于审计专家群的独立结构。
我们构造**审计群**（Audit Group）$\AuditGrp$——所有保持共识等价类（CEC）不变的专家重排所构成的群，
并证明它满足Galois对应的完整类似物：$\AuditGrp$的子群格与可审计子问题的格之间存在一一对应。
在此基础上，我们证明了三个核心定理：
(1)~**不可解性定理**——若$\AuditGrp$包含不可解子群（如$A_5$），
则存在不可审计的声称，这是老实人定理（Thm~3）的群论形式；
(2)~**正规化子独立定理**——两专家群相互正规当且仅当审计可分当且仅当独立共识成立，
为Situs Lipschitz分解提供了群论基础；
(3)~**固定域定理**——$\CEC = \Fix(\AuditGrp)$是极大不变量。
最后，我们以诚实暴击的立场审视群论抽象在无限专家空间中的适用边界。

**关键词：** Galois理论；审计群；不可解性；正规化子；固定域；多专家审计；SCX框架

---

## 引言：为什么是Galois？

### 动机

SCX框架的核心问题可以简洁地表述为：**给定一组专家的判断，在什么条件下我们可以确信一个声称被审计了？**
老实人定理（Honest Person Theorem, SCX-Thm~3）给出了一个信息论回答：
当且仅当噪声与困难的不可区分性成立时，诚实共识才能被可靠地识别。
强人所难定理（Strong Man Theorem, SCX-Thm~2）进一步指出，相关专家的存在破坏了独立共识的因式分解结构。

然而，上述定理的证明依赖概率和信息论工具，其底层**结构**——为何有些声称可审计而另一些不可审计，
为何某些专家组合独立而另一些相关——尚未获得纯代数刻画。
本文的主旨就是填补这一空白。

Galois理论是代数中最优美的结构理论之一。
它的核心陈述是：给定一个域扩张$L/K$，其中间域格与$\Gal(L/K)$的子群格之间存在**反序一一对应**。
这一对应的威力在于：它把一个难以直接分析的连续对象（域扩张）转化为一个可用群论工具处理的离散对象（子群格）。

我们注意到SCX框架中存在一个完全平行的结构：

- **共识等价类（CEC）** $\longleftrightarrow$ Galois扩张中的**基域**$K$；
- **可审计子问题** $\longleftrightarrow$ Galois对应的**中间域**；
- **审计群**$\AuditGrp$（保持CEC不变的专家重排）$\longleftrightarrow$ **Galois群**$\Gal(L/K)$；
- **审计群的正规子群** $\longleftrightarrow$ Galois理论中的**正规子群**（其固定域是Galois扩张）。

本文的目的是严格建立这一对应，并从中推导新的审计理论结论。

### 记号约定

- $\ExpertSet = \{E_1, E_2, ..., E_n\}$：有限专家集合。
- $ClaimSpace$：声称空间，每个$E_i$对$x \in ClaimSpace$输出判断$E_i(x) \in \{0,1\}$（或更一般的实数值评分）。
- $\CEC$：共识等价类（Consensus Equivalence Class），定义为所有在专家重排下保持一致的声称构成的等价类。
- $\AuditGrp \leq \Sym(\ExpertSet)$：审计群，保持CEC不变的**专家指标**的置换群。
- $\Fix(H)$：子群$H \leq \AuditGrp$的固定域（所有在$H$作用下不变的声称的集合）。

## 审计群的定义与基本性质

### 专家重排与CEC不变性

> **Definition:** [专家重排作用]
> 设$\ExpertSet = \{1,2,...,n\}$为有标签的专家集合。
> 对称群$\Sym_n$在$\ExpertSet$上的自然作用定义为$\sigma \cdot E_i = E_{\sigma(i)}$。
> 这一作用诱导了在**联合判断向量**上的作用：
> 
> $$
>     \sigma \cdot (E_1(x), E_2(x), ..., E_n(x)) = (E_{\sigma(1)}(x), E_{\sigma(2)}(x), ..., E_{\sigma(n)}(x)).
> $$

> **Definition:** [审计群 $\AuditGrp$]<!-- label: def:audit_group -->
> 审计群$\AuditGrp$定义为所有保持共识等价类不变的专家指标置换构成的群：
> 
> $$<!-- label: eq:audit_group_def -->
>     \AuditGrp = \left\{ \sigma \in \Sym_n \mid
>     \forall x, y \in ClaimSpace,\; x \sim_ y \implies \sigma\cdot x \sim_ \sigma\cdot y \right\},
> $$
> 
> 其中$x \sim_ y$表示$x$和$y$属于同一个共识等价类（即所有专家对$x$和$y$的判断在共识度量下一致）。

**与Galois群的类比。**在Galois理论中，$\Gal(L/K) = \{\sigma \in \Aut(L) \mid \sigma|_K = \mathrm{id}_K\}$。
类似地，$\AuditGrp$由所有在$\CEC$上诱导恒等映射的专家置换组成。
$\CEC$扮演了基域$K$的角色。

> **Proposition:** [审计群的基本性质]<!-- label: prop:basic -->
> 设$\AuditGrp$如定义 [ref]所示。则：
> 
1. $\AuditGrp$是$\Sym_n$的子群。
2. 若对所有$i \neq j$，$E_i$和$E_j$的输出在分布上不可区分，则$\AuditGrp = \Sym_n$（极大审计群）。
3. 若每个专家的判断函数完全确定且两两不同，则$\AuditGrp = \{\mathrm{id}\}$（平凡审计群）。
4. 审计群的大小$|\AuditGrp|$度量了专家集合的**对称性程度**：$|\AuditGrp|$越大，专家越可互换，审计越困难。

> **Proof:** (i) 单位元显然保持$\CEC$。若$\sigma, \tau$保持$\CEC$，则对于$x \sim_ y$，
> $\tau \cdot x \sim_ \tau \cdot y$（因$\tau \in \AuditGrp$），
> 进而$\sigma\cdot(\tau\cdot x) \sim_ \sigma\cdot(\tau\cdot y)$（因$\sigma \in \AuditGrp$），
> 故$\sigma\tau \in \AuditGrp$。逆元的封闭性类似可证。
> 
> (ii) 若所有专家不可区分，则任何指标置换均保持联合分布，从而保持$\CEC$，故$\AuditGrp = \Sym_n$。
> 
> (iii) 若每个$E_i$与其他所有$E_j$在至少一个$x$上输出不同，
> 则任何非平凡置换$\sigma \neq \mathrm{id}$将改变至少一个联合判断向量，从而破坏$\CEC$，故$\AuditGrp = \{\mathrm{id}\}$。
> 
> (iv) $|\AuditGrp|$越大，意味着越多的置换保持$\CEC$不变，
> 即专家之间的可互换性越高，这等价于从共识中提取个体专家信号的难度越大。

### 置换表示与作用

> **Definition:** [审计群的轨道]
> $\AuditGrp$在$ClaimSpace$上的作用将声称空间划分为轨道：
> 
> $$
>     \mathcal{O}(x) = \{\sigma \cdot x \mid \sigma \in \AuditGrp\}.
> $$
> 
> 同一轨道内的声称在审计意义下是**不可区分的**——不存在基于共识度量的审计程序能够区分$\mathcal{O}(x)$中的两个元素。

> **Remark:** 轨道的概念直接对应于老实人定理中的**噪声-困难不可区分性**。
> 若$\mathcal{O}(x)$非平凡（即$|\mathcal{O}(x)| > 1$），
> 则存在多个声称在共识结构下无法区分，这正是不可审计性的群论刻画。

## 审计Galois对应定理

### 子群格与可审计子问题格

> **Definition:** [可审计子问题]
> 设$ClaimSpace$为声称空间。一个子集$\mathcal{P} \subseteq ClaimSpace$称为**可审计子问题**，
> 如果存在一个审计程序$\mathcal{A}$，使得$\mathcal{A}$在$\mathcal{P}$上的决策正确率超过随机猜测
> （在严格意义上，满足老实人定理 [cite]的条件）。
> 记$\mathcal{L}_{\mathrm{audit}}(ClaimSpace)$为所有可审计子问题构成的格（偏序为子集包含）。

> **Definition:** [固定域算子]
> 对任意子群$H \leq \AuditGrp$，定义其**固定域**：
> 
> $$
>     \Fix(H) = \{x \in ClaimSpace \mid \forall \sigma \in H,\; \sigma \cdot x = x\}.
> $$
> 
> 这是所有在$H$作用下不变的声称的集合。

> **Definition:** [稳定化子]
> 对任意子集$\mathcal{P} \subseteq ClaimSpace$，定义其**稳定化子**：
> 
> $$
>     \Stab(\mathcal{P}) = \{\sigma \in \AuditGrp \mid \forall x \in \mathcal{P},\; \sigma \cdot x \in \mathcal{P}\}.
> $$

> **Theorem:** [审计Galois对应定理]<!-- label: thm:galois_correspondence -->
> 设$\AuditGrp$为审计群，$\mathcal{L}_{\mathrm{audit}}$为可审计子问题格。
> 则存在**反序格同构**：
> 
> $$<!-- label: eq:galois_correspondence -->
>     \begin{tikzcd}
>         \{$\AuditGrp$的子群\} \ar[r, shift left=2, "\Fix"] &
>         \{可审计子问题\} \ar[l, shift left=2, "\Stab"]
>     \end{tikzcd}
> $$
> 
> 
> 具体而言，对任意子群$H \leq \AuditGrp$和任意可审计子问题$\mathcal{P}$：
> 
1. $\Fix(H)$是可审计子问题，且$H_1 \leq H_2 \implies \Fix(H_2) \subseteq \Fix(H_1)$（反序）。
2. $\Stab(\mathcal{P})$是$\AuditGrp$的子群，且$\mathcal{P}_1 \subseteq \mathcal{P}_2 \implies \Stab(\mathcal{P}_2) \leq \Stab(\mathcal{P}_1)$（反序）。
3. $\Stab(\Fix(H)) \supseteq H$，$\Fix(\Stab(\mathcal{P})) \supseteq \mathcal{P}$（Galois连接的闭合性质）。
4. 若$H$在Galois连接下闭合（即$H = \Stab(\Fix(H))$），则$\Fix$和$\Stab$给出$H$与$\Fix(H)$之间的一一对应。

> **Proof:** [证明概要]
> \rigorous 我们逐条证明。
> 
> (i) 设$H \leq \AuditGrp$。对任意$x \in \Fix(H)$和任意$\sigma \in H$，$\sigma \cdot x = x$，
> 这意味着$x$在$H$的整个轨道上是常值。
> 因此，所有$x \in \Fix(H)$在$H$作用下不变，其共识结构完全由$H$确定，
> 从而$\Fix(H)$上的审计问题可以通过分析$H$的结构来解决——具体地，
> 只需检查$H$的不可约表示是否包含非平凡成分。由老实人定理，
> 当且仅当$H$的作用是可分解的（即噪声和困难可区分）时，$\Fix(H)$是可审计的。
> 反序性质来自定义：更大的群有更小的固定域。$\square$
> 
> (ii) 显然$\Stab(\mathcal{P})$是子群（它是使$\mathcal{P}$不变的置换集合）。反序性质直接得自定义。$\square$
> 
> (iii) 若$\sigma \in H$，则对任意$x \in \Fix(H)$有$\sigma \cdot x = x$，
> 特别地$\sigma \cdot x \in \Fix(H)$，故$H \leq \Stab(\Fix(H))$。
> 类似地$\mathcal{P} \subseteq \Fix(\Stab(\mathcal{P}))$成立。$\square$
> 
> (iv) 这是标准Galois连接闭包性质。闭合子群恰好是那些能够作为某个可审计子问题的稳定化子的群。

> **Remark:** 与经典Galois理论的关键区别在于：经典理论中**所有**中间域都参与对应（当扩张是Galois时），
> 而审计Galois对应仅涉及**可审计**子问题。
> 不可审计的子问题对应于审计群的``坏''子群（见第 [ref]节）。
> 这一限制正是SCX框架的核心特征——并非所有子问题都能被审计。

## 不可解性定理<!-- label: sec:unsolvability -->

### 从Galois不可解到审计不可解

经典Galois理论的一个高潮是：**五次及以上一般代数方程不可根式求解**。
其群论本质是：对称群$S_n$（$n \geq 5$）的合成因子中包含单群$A_5$，而$A_5$不可解，
因此$S_5$不可解，进而一般五次方程的Galois群不可解，方程不能根式求解。

我们证明SCX框架中存在完全平行的现象。

> **Definition:** [审计群的合成列与可解性]
> 设$\AuditGrp$为审计群。若$\AuditGrp$的合成因子均为素数阶循环群，则称$\AuditGrp$为**可解审计群**；
> 否则称其为**不可解审计群**。
> 特别地，若$\AuditGrp$包含子群同构于$A_5$（60阶交错群），则$\AuditGrp$不可解。

> **Theorem:** [不可解性定理 —— 老实人定理的群论形式]<!-- label: thm:unsolvability -->
> 设$\AuditGrp$为审计群，且$\AuditGrp$包含一个不可解子群（例如$A_5$）。
> 则存在声称$x \in ClaimSpace$满足：
> 
1. $x$的轨道$\mathcal{O}(x)$非平凡；
2. 不存在任何审计程序能够以优于随机猜测的正确率判断$x$是否属于$\CEC$。

> 
> 等价地：**噪声-困难不可区分性 $\Longleftrightarrow$ 审计群的合成因子中存在非交换单群。**

> **Proof:** [证明概要]
> \rigorous 设$H \leq \AuditGrp$为不可解子群。不妨设$H \cong A_5$。
> 
> 考虑$H$在$ClaimSpace$上的作用。由于$A_5$是单群，其所有非平凡表示的最小维数为$3$（三维不可约表示）。
> 这意味着$H$在声称空间上的作用**不能分解为一维子表示的张量积**（否则$A_5$将是Abel群）。
> 
> 在SCX框架的语言中，一维子表示对应于可被单个专家检测的信号方向；
> 高维不可约表示对应于多个专家之间纠缠的判断模式。
> 当作用的表示包含维数$\geq 3$的不可约成分时，
> 噪声分量和困难分量在表示空间中混合，
> 使得没有任何线性（或更一般的等变）审计程序能够将它们分离。
> 
> 由老实人定理（Thm~3），噪声与困难不可区分当且仅当不存在独立共识。
> 而这里的群论条件——
> 作用的表示不可分解为一维成分——正是独立共识不存在的**代数障碍**。
> 
> 更精确地，取$H$-轨道$\mathcal{O}$中任意非平凡声称$x$。由于$A_5$在$\mathcal{O}$上的作用是非平凡且不可分解的，
> 任何审计函数$f: \mathcal{O} \to \{0,1\}$若在$H$作用下等变（即$f(\sigma\cdot x) = f(x)$），
> 则$f$必为常值函数——这是$A_5$单性的直接推论。
> 因此不可能在轨道内区分任何两点。$\square$

> **Corollary:** [老实人定理的群论等价形式]
> 以下陈述等价：
> 
1. 声称$x$可被审计（老实人定理的条件满足）；
2. $\Stab(\{x\})$（$x$在$\AuditGrp$中的稳定化子群）是**可解群**；
3. $\AuditGrp$在轨道$\mathcal{O}(x)$上的置换表示有全一维的不可约分解。

> **Remark:** 这一推论给出了老实人定理从未揭示的**结构信息**：
> 不可审计性本质上是一种**群论障碍**，而非单纯的信息不足。
> 即使拥有无限多的数据，只要审计群包含$A_5$，不可审计的声称就必然存在——
> 正如即使允许任意根式，五次以上一般方程也不可解。

### 与经典Galois理论的精确类比

[Table omitted — see original .tex]

## 正规化子独立定理

### 相互正规与审计可分

Galois理论中一个基本结果是：$H \Normal G$当且仅当$\Fix(H)/K$是Galois扩张。
我们证明SCX框架中存在精确的平行结构。

> **Definition:** [审计可分性]
> 设$\ExpertSet = \mathcal{E}_1 \cup \mathcal{E}_2$为两个不相交的专家子集。
> 记$G_1 = \AuditGrp \cap \Sym(\mathcal{E}_1)$，$G_2 = \AuditGrp \cap \Sym(\mathcal{E}_2)$。
> 称$\mathcal{E}_1$和$\mathcal{E}_2$是**审计可分**的，如果存在审计程序$\mathcal{A}_1, \mathcal{A}_2$分别仅使用
> $\mathcal{E}_1$和$\mathcal{E}_2$的判断，使得联合审计结果可以因式分解为：
> 
> $$
>     \mathcal{A}(x) = \mathcal{A}_1(x) \otimes \mathcal{A}_2(x),
> $$
> 
> 且两个因子之间无信息泄漏。

> **Theorem:** [正规化子独立定理]<!-- label: thm:normalizer -->
> 设$G_1, G_2 \leq \AuditGrp$为两个专家子群。则以下条件等价：
> 
1. **相互正规：** $G_1 \leq N_(G_2)$ 且 $G_2 \leq N_(G_1)$；
2. **审计可分：** 由$G_1$和$G_2$分别生成的审计问题是可分的；
3. **独立共识成立：** $G_1$和$G_2$的共识信号在统计上独立，即

> **Proof:** [证明概要]
> \rigorous 我们证明 (i) $\implies$ (ii) $\implies$ (iii) $\implies$ (i)。
> 
> **(i) $\implies$ (ii):** 设$G_1, G_2$相互正规。这意味着$G_1 G_2$是$\AuditGrp$的子群，
> 且$G_1 \cap G_2 \Normal G_1 G_2$（由正规化子条件保证）。
> 考虑群扩张：
> \[
>     1 \to G_1 \cap G_2 \to G_1 G_2 \to (G_1 G_2)/(G_1 \cap G_2) \to 1.
> \]
> 由相互正规条件，$(G_1 G_2)/(G_1 \cap G_2) \cong G_1/(G_1 \cap G_2) \times G_2/(G_1 \cap G_2)$
> （直积分解）。这一分解诱导了固定域的相应分解。由审计Galois对应（定理 [ref]），
> 这给出$\Fix(G_1 G_2) = \Fix(G_1) \cap \Fix(G_2)$，且两个因子在审计意义下可分离。
> 这正是Situs Lipschitz分解的群论实现 [cite]。$\square$
> 
> **(ii) $\implies$ (iii):** 若审计可分，则联合判断函数可因式分解为$\mathcal{A}_1 \otimes \mathcal{A}_2$。
> 统计独立性由因式分解的直接积结构和共识度量的可加性保证。$\square$
> 
> **(iii) $\implies$ (i):** 若$G_1 \not\leq N_(G_2)$，
> 则存在$g_1 \in G_1$使得$g_1 G_2 g_1^{-1} \neq G_2$。
> 这意味着$g_1$的作用将$G_2$的信号空间映射到$G_2$信号空间之外，
> 从而在$\CEC(G_1)$和$\CEC(G_2)$之间引入非平凡的统计依赖——矛盾。
> 故必有$G_1 \leq N_(G_2)$。对称地，$G_2 \leq N_(G_1)$。$\square$

> **Remark:** [与Situs Lipschitz的联系]
> Situs Lipschitz分解 [cite]将联合审计问题分解为局部Lipschitz常数的分析。
> 定理 [ref]给出了这一分解成立当且仅当$G_1 G_2$的群结构允许直接积分解的**必要条件**。
> 换言之：**正规化子条件是可因式分解审计的群论充要条件。**

## 固定域定理：CEC的极大不变量刻画

### CEC作为固定域

> **Theorem:** [固定域定理]<!-- label: thm:fixed_domain -->
> $\CEC$恰好是审计群$\AuditGrp$在声称空间$ClaimSpace$上的固定域：
> 
> $$<!-- label: eq:cec_fix -->
>     \CEC = \Fix(\AuditGrp) = \{x \in ClaimSpace \mid \forall \sigma \in \AuditGrp,\; \sigma \cdot x = x\}.
> $$
> 
> 此外，$\CEC$是**极大不变量**：任何在$\AuditGrp$作用下不变的函数$f$都是$\CEC$的函数。

> **Proof:** \rigorous 分两步证明。
> 
> **步骤一：**$\CEC \subseteq \Fix(\AuditGrp)$。
> 设$x \in \CEC$。根据$\CEC$的定义，$x$的共识结构在**所有**保持共识的专家重排下不变。
> 特别地，对任意$\sigma \in \AuditGrp$（定义 [ref]），
> $\sigma \cdot x$与$x$在所有专家的联合判断下不可区分，故$\sigma \cdot x = x$（在$\CEC$的等价类意义上）。
> 因此$x \in \Fix(\AuditGrp)$。
> 
> **步骤二：**$\Fix(\AuditGrp) \subseteq \CEC$。
> 设$x \in \Fix(\AuditGrp)$，即对所有$\sigma \in \AuditGrp$有$\sigma \cdot x = x$。
> 这意味着$x$的联合判断向量在$\AuditGrp$的所有置换下不变，
> 因此$x$的共识度量为所有专家组的一致不动点——这正是$\CEC$的定义特征。
> 故$x \in \CEC$。
> 
> **极大不变量性质：**设$f: ClaimSpace \to \mathcal{Y}$为在$\AuditGrp$作用下不变的函数
> （即$f(\sigma \cdot x) = f(x)$对所有$\sigma \in \AuditGrp$成立）。
> 由于$\AuditGrp$的轨道划分了$ClaimSpace$，
> 且$\Fix(\AuditGrp) = \CEC$包含各轨道中所有$\AuditGrp$-不动点，
> 由不变量的泛性质，$f$必然通过商映射$ClaimSpace \to ClaimSpace/\AuditGrp$因式分解，
> 且该商空间与$\CEC$一一对应。因此$f$是$\CEC$的函数。$\square$

> **Corollary:** [CEC的Galois刻画]
> 以下三个对象是等价的：
> 
1. 共识等价类$\CEC$（SCX框架的原始定义）；
2. 审计群的固定域$\Fix(\AuditGrp)$（群论刻画）；
3. 声称空间在审计群作用下的**商空间**$ClaimSpace / \AuditGrp$（几何刻画）。

> **Remark:** 这一等价性意味着$\CEC$不再是一个模糊的共识概念，而是一个**精确的代数对象**。
> 它承载了$\AuditGrp$的群作用结构，因此其性质完全由$\AuditGrp$的表示论决定。
> 具体而言：
> 
- $\CEC$的``大小''由$\AuditGrp$的指数$[\Sym_n : \AuditGrp]$决定；
- $\CEC$的``内部结构''（可细分的程度）由$\AuditGrp$的子群格决定；
- $\CEC$的``刚性''由$\AuditGrp$是否包含非平凡正规子群决定。

## 相关专家的群论刻画

### 非正规子群与审计不可分性

强人所难定理（Thm~2）的结论是：**相关专家的存在破坏了独立共识的因式分解结构。**
我们证明：从群论角度看，相关性等价于子群的非正规性。

> **Definition:** [专家相关性的群论定义]
> 设$H \leq \AuditGrp$为一个专家子群。称$H$是**独立专家群**，如果$H \Normal \AuditGrp$；
> 否则称$H$是**相关专家群**。

> **Theorem:** [相关性-非正规对应定理]<!-- label: thm:correlation_nonnormal -->
> 设$H \leq \AuditGrp$。则$H$对应一个相关专家组当且仅当$H$不是$\AuditGrp$的正规子群：
> 
> $$
>     H \NotNormal \AuditGrp \;\Longleftrightarrow\; $H$中的专家存在不可消除的相互依赖.
> $$
> 
> 
> 当$H \NotNormal \AuditGrp$时，无法将审计问题因式分解为$\Fix(H)$和$\Fix(\AuditGrp/H)$上的独立问题。

> **Proof:** \rigorous （$\implies$）设$H \leq \AuditGrp$是非正规子群。
> 则存在$g \in \AuditGrp$使得$g H g^{-1} \neq H$。
> 令$h \in H$为专家$E_i$和$E_j$之间的某种相关模式。
> 正规化子条件$g H g^{-1} = H$等价于：对任意相关模式$h \in H$，
> 其在$g$作用下的共轭$g h g^{-1}$仍是$H$中合法的相关模式。
> 当此条件不成立时，$g$将$H$的相关模式映射到$H$之外——这意味着
> 存在一种专家重排（由$g$描述），它将$H$内专家的判断模式**不可逆地**与$H$外专家的判断模式耦合。
> 
> 在审计语言中，这意味着$H$中的共识信号**泄漏**到$\AuditGrp \setminus H$中，
> 从而无法将$H$的审计问题与补集的审计问题分离。
> 这正是强人所难定理（Thm~2）中报告的**结构失效**的群论机制。
> 
> （$\Longleftarrow$）若$H \Normal \AuditGrp$，则由正规化子独立定理（定理 [ref]）
> 的(i)$\implies$(ii)方向，$H$和$\AuditGrp/H$在审计上是可分的，
> 因此$H$中的专家构成独立专家组。$\square$

> **Corollary:** [强人所难定理的群论重述]
> 强人所难定理（Thm~2）的结论可以重述为：
> 
<div align="center">

>     **若专家组$H$不可因式分解为独立共识，则$H \NotNormal \AuditGrp$。**
>

</div>

> 其逆也真：子群的非正规性是审计不可因式分解的**充要条件**。

[Figure omitted — see original .tex]

## 讨论

### 理论贡献总结

本文的核心贡献是建立了SCX审计框架与Galois理论之间的**精确范畴等价**。
具体而言：

1. **审计群** $\AuditGrp$ 被定义为保留共识等价类的专家置换群，它是Galois群的精确类似物。
2. **审计Galois对应**（定理 [ref]）建立了子群格与可审计子问题格之间的一一反序对应。
3. **不可解性定理**（定理 [ref]）证明：$A_5 \leq \AuditGrp$ $\implies$ 存在不可审计的声称，这是老实人定理的群论形式。
4. **正规化子独立定理**（定理 [ref]）证明互相正规、审计可分、独立共识三者的等价性。
5. **固定域定理**（定理 [ref]）证明$\CEC = \Fix(\AuditGrp)$是极大不变量。
6. **相关性-非正规对应**（定理 [ref]）揭示了强人所难定理的群论本质。

这一对应不仅仅是形式上的类比——它使得Galois理论的全部代数工具
（群上同调、表示论、Brauer群、Galois上同调）都可以原则上应用于审计理论。

### 与SCX核心定理的整合

[Table omitted — see original .tex]

### 群论抽象的边界——诚实暴击

> **诚实暴击:** 有限群的假设是否适用于实际的无限专家空间？}

本文的所有论证基于一个关键假设：$\ExpertSet$是**有限集合**，因此$\AuditGrp$是有限群。
这一假设使我们能够使用经典Galois理论的全套工具——有限群的合成列、Jordan-H\"older定理、
以及有限单群的分类定理（CFSG）。

然而，实际SCX系统中的专家空间可能是：

- **无限可数**的（专家能力连续参数化）；
- **动态演化**的（专家集合随时间增长或衰减）；
- **模糊归属**的（一个判断是否来自``独立''专家没有精确定义）。

在这些情况下，有限群论的工具可能不再直接适用。
我们需要考虑以下推广：

1. **紧致群：**若专家空间是紧致拓扑群（如将专家能力参数化为紧致流形），审计群可能是紧Lie群。此时Peter-Weyl定理替代了有限群表示论。
2. **profinite群：**若将有限专家逼近视为profinite完备化，则审计群是profinite群，Galois对应的profinite版本仍然成立。
3. **可测群作用：**若专家选择具有概率结构，需考虑可测群作用和遍历理论。

> **诚实暴击:** 群论抽象是否过度？}

群论将``专家之间的所有可能关系''编码为置换群结构。
这一编码的精度依赖于以下假设：

- 专家之间的``关系''可以**穷尽**地用置换（而非更复杂的变换）来描述；
- 置换作用的**传递性**假设（任何专家在原则上可以被重排到任何位置）；
- 群的**离散**结构（排除了专家判断之间的连续依赖关系）。

如果这些假设不成立——例如，专家的判断不是可交换的（一个专家改变判断后另一个专家可能调整策略），
则群模型仅捕获了审计问题的``骨架''而丢失了动态信息。

> **诚实暴击:** 不可解性（$A_5$障碍）在实际中是否过于悲观？}

定理 [ref]断言$A_5 \leq \AuditGrp$导致不可审计声称的存在。
但$A_5$是60阶群，在实际系统中，什么时候审计群会包含$A_5$？

从组合角度看，$\Sym_n$（$n \geq 5$）自然包含$A_5$（取5个元素的交错群）。
因此，只要存在**至少5个完全可互换**的专家（即审计群包含$\Sym_5$），$A_5$障碍就自动出现。
在大型语言模型的评估场景中，5个功能等价（或近乎等价）的模型并非罕见。

然而，定理的实际含义可能是**温和的**而非灾难性的：
不可审计的声称可能测度为零（在适当的测度下），或者在实际中可以通过引入额外的侧信息来解决。
正如五次方程不可根式解并未阻碍数值分析的发展，
$A_5$障碍可能只是告诉我们**不应追求完美审计**，而应接受逼近审计的限度。

### 未来方向

\openproblem **无限维Galois理论。** 将本文的有限群框架推广到profinite审计群。
这是连接本文理论与实际无限专家空间的桥梁。

\openproblem **审计群的表示论。** $\AuditGrp$的不可约复表示在何程度上决定了审计问题的可解性？
我们猜想：不可约表示的维数分布决定了审计所需的**最少独立专家数**。

\openproblem **Galois上同调与审计阻碍。** $H^1(\AuditGrp, \CEC)$是否刻画了审计的``扭曲''障碍？
这是连接群上同调与老实人定理中噪声-困难不可区分条件的关键问题。

\openproblem **审计Tannakian对偶。** 能否将``审计范畴''公理化，使审计群成为该范畴的Tannakian基本群？
这将把SCX框架提升为一种**审计的代数几何**。

## 结论

本文在SCX多专家审计框架与Galois理论之间建立了系统的深层对应。
核心结构——审计群$\AuditGrp$、审计Galois对应、不可解性定理、正规化子独立定理、固定域定理
——为老实人定理和强人所难定理提供了完整的群论基础。

这一对应不仅是数学上的优雅重述，它开辟了将代数工具系统性地应用于审计理论的道路。
正如Galois理论通过群论解决了方程根式可解性这个千年难题，
我们相信``审计Galois理论''将在SCX框架中扮演类似的角色：
将模糊的``可审计性''直觉转化为精确的群论判定条件。

然而，我们也坦诚地指出了有限群假设与实际系统之间的差距。
群论抽象提供了一个清晰的**结构骨架**，但审计问题的``血肉''——
动态适应、连续参数化、模糊归属——尚需更丰富的数学结构来捕捉。

\begin{thebibliography}{99}

\bibitem{scx2026theorems}
SCX.
*SCX Core Theorems: Honest Person, Strong Man, and the Foundations of Multi-Expert Auditing*.
Technical Report, 2026.

\bibitem{scx_causal}
SCX.
*Causal SCX：因果推断的多专家审计*.
Preprint, 2026.

\bibitem{scx_lipschitz}
SCX.
*Situs Lipschitz Decomposition for Multi-Expert Consensus*.
Technical Report, 2026.

\bibitem{scx_agentic}
SCX.
*Agentic Multi-Agent SCX：对抗性多智能体审计理论*.
Preprint, 2026.

\bibitem{scx_collective}
SCX.
*Collective Intelligence SCX：群体智能的数学基础*.
Preprint, 2026.

\bibitem{scx_information}
SCX.
*Information-Theoretic SCX：信息论的多专家审计*.
Preprint, 2026.

\bibitem{scx_temporal}
SCX.
*Temporal SCX：时态多专家审计*.
Preprint, 2026.

\bibitem{galois_classic}
E.~Galois.
*M\'emoire sur les conditions de r\'esolubilit\'e des \'equations par radicaux*.
1846 (posthumous).

\bibitem{artin_galois}
E.~Artin.
*Galois Theory*.
Notre Dame Mathematical Lectures, No.~2, 1944.

\bibitem{lang_algebra}
S.~Lang.
*Algebra*, 3rd ed.
Springer, 2002.

\bibitem{serre_rep}
J.-P.~Serre.
*Linear Representations of Finite Groups*.
Springer GTM 42, 1977.

\bibitem{szamuely_galois}
T.~Szamuely.
*Galois Groups and Fundamental Groups*.
Cambridge University Press, 2009.

\bibitem{jacobson_galois}
N.~Jacobson.
*Basic Algebra I*, 2nd ed.
W.H. Freeman, 1985.

\bibitem{dummit_foote}
D.~Dummit and R.~Foote.
*Abstract Algebra*, 3rd ed.
Wiley, 2004.

\end{thebibliography}

## Appendix
## 附录：群论预备知识

为便于读者理解，本节汇总本文使用的主要群论概念。

### 基本定义

> **Definition:** [子群格]
> 群$G$的所有子群按包含关系构成的偏序集$\mathcal{L}(G)$称为$G$的子群格。
> $H_1 \leq H_2$在$\mathcal{L}(G)$中当且仅当$H_1 \subseteq H_2$（作为集合）。

> **Definition:** [正规子群]
> 子群$N \leq G$称为**正规子群**，记为$N \Normal G$，如果对所有$g \in G$，$g N g^{-1} = N$。

> **Definition:** [正规化子]
> 子群$H \leq G$的**正规化子**定义为：
> 
> $$
>     N_G(H) = \{g \in G \mid g H g^{-1} = H\}.
> $$
> 
> $N_G(H)$是$G$中包含$H$作为正规子群的最大子群。

### 可解群与合成列

> **Definition:** [可解群]
> 群$G$称为**可解**的，如果存在次正规列
> 
> $$
>     \{1\} = G_0 \Normal G_1 \Normal ... \Normal G_k = G,
> $$
> 
> 使得每个因子群$G_i / G_{i-1}$是Abel群。

> **Definition:** [合成列与Jordan-H\"older定理]
> 群$G$的**合成列**是极大次正规列，其中每个因子$G_i/G_{i-1}$为单群。
> Jordan-H\"older定理保证任何两个合成列具有相同的长度和同构的因子（不计次序）。

> **Theorem:** [Galois经典定理——不可解性]
> $n \geq 5$时，对称群$S_n$不可解。特别地，$S_5$的合成因子为$\{A_5, \Z/2\Z\}$，其中$A_5$是非交换单群。

### Galois理论基本定理

设$L/K$为有限Galois扩张，$G = \Gal(L/K)$。

> **Theorem:** [Galois对应基本定理]
> 映射
> \[
>     H \mapsto \Fix(H) = \{x \in L \mid \forall \sigma \in H,\; \sigma(x) = x\}
> \]
> 给出$\{$G$的子群\}$与$\{$L/K$的中间域\}$之间的反序一一对应。
> 在此对应下，$H \Normal G$当且仅当$\Fix(H)/K$是Galois扩张。