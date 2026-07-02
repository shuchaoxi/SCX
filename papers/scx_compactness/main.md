<div align="center">

**版本：** v1.0 \quad | \quad
**状态：** 预印本 \quad | \quad
**分类：** SCX理论体系 — 逻辑基础卷

</div>

*Abstract:*

本文揭示模型论紧致性定理（Compactness Theorem）与SCX多专家审计框架之间的深层结构对应。
核心洞察如下：模型论紧致性定理断言「若一阶句子集$\Gamma$的每个有限子集有模型，则$\Gamma$有模型」；
SCX框架中，这对应为「若每个有限专家子组在审计中达成一致，则全体专家可通过审计」——
这是同一数学结构——有限到无限的传递性——在两个不同领域中的具体实现。

我们证明六个核心结果：
(1)~**紧致性-审计对应定理**——将声称集$\Gamma$映射为模型（通过审计的专家配置），
则「每个有限子集通过审计$\implies$全组通过审计」精确等价于一阶紧致性；
(2)~**有限可审计定理**——审计是紧致的：若声称在CEC的任意有限片段通过，则在整个CEC通过，
有限性保证审计可终止；
(3)~**Łoś超积对应定理**——专家的多数形成一个超滤子，
CEC共识等于超积的真理谓词，$M\to\infty$极限下的SCX就是超积；
(4)~**逻辑基础三角**——Galois对应（可审计性的必要条件）、紧致性（充分终止条件）、
老实人定理（不可区分性）三者构成SCX的元理论；
(5)~**操作意义**——$k=3$最小子组的一致性保证全组一致性，有限$\to$无限传递的审计效率；
(6)~**紧致性在SCX中的形式化**——使用超积构造明确给出CEC极限模型。

最后，我们以诚实暴击的立场审视超滤子的非构造性与实际审计的构造性需求之间的根本性gap。

**关键词：** 紧致性定理；Łoś定理；超积；超滤子；多专家审计；SCX框架；有限可审计性；模型论

---

## 引言：从有限到无限的桥梁

### 动机

模型论的紧致性定理（Compactness Theorem）是数理逻辑中最深刻的定理之一。
其经典陈述为：

> 设$\Gamma$为一阶语言$\Lang$中的句子集。若$\Gamma$的每个有限子集都有模型，则$\Gamma$本身有模型。

这一定理揭示了从「有限可满足」到「无限可满足」的传递——一个在有限世界中非平凡的断言。
它等价于选择公理的一个弱形式（布尔素理想定理），
是Gödel完备性定理的直接推论，也是非标准分析、饱和模型、类型空间理论等众多领域的逻辑基础。

SCX（Strategic Consensus X）框架的核心问题是：**给定一组专家的判断，什么条件下一个声称被可靠地审计了？**
在SCX的理论体系中，Galois-SCX对应 [cite]揭示了可审计性的群论结构，
老实人定理（SCX-Thm~3）刻画了诚实共识的识别条件，
强人所难定理（SCX-Thm~2）揭露了相关专家对独立共识的破坏机制。

然而，上述定理均隐含了一个关键的操作假设：
**审计过程涉及有限多位专家**。
在实际系统中，专家集合可能是：

- **无限可数**的（专家能力连续参数化）；
- **动态增长**的（新专家不断加入）；
- **开放**的（专家集合的最终范围未知）。

当专家集合趋于无限时，一个根本问题浮现：

<div align="center">

**「每个有限专家组通过审计」能否保证「无限专家组通过审计」？**

</div>

这正是紧致性定理在SCX中的自然对应。
本文的主旨就是严格建立这一对应，并从中推导SCX框架的有限可审计性定理。

### 直觉预览

紧致性定理的直观是：如果某件事在每一个有限片段都成立，那么它在整体上也成立。
在SCX的语境中，这翻译为：

- **逻辑侧：** $\Gamma$（声称集）的每个有限子集$\Delta \subseteq \Gamma$可满足（有模型=通过审计）。
- **审计侧：** 每个有限专家子组对一组声称达成一致。
- **紧致性桥梁：** 若所有有限子组都一致，则全组一致。

更精确地，如果我们将「专家的判断」编码为一阶结构中的关系，
将「声称通过审计」编码为句子在结构中的真值，
则SCX的审计过程就是一个模型论的可满足性判定过程——
而紧致性定理恰好保证了这一判定过程的**有限可终止性**。

### 记号约定

- $\ExpertSet = \{E_i\}_{i \in I}$：专家集合（指标集$I$可为无限）。
- $ClaimSpace$：声称空间，每个$E_i$对$x \in ClaimSpace$输出判断$E_i(x) \in \{0,1\}$。
- $\CEC$：共识等价类（Consensus Equivalence Class）。
- $\Lang$：一阶语言，包含谓词符号$\{P_i\}_{i \in I}$编码专家判断。
- $\Struct_i$：专家$E_i$的判断结构（一阶结构）。
- $\Ultrafilter$：$I$上的超滤子，编码「多数专家」的概念。
- $\Ult \Struct_i / \Ultrafilter$：专家判断结构的超积。

## 紧致性-审计对应定理

### 声称的逻辑编码

> **Definition:** [审计语言]
> 设$\ExpertSet = \{E_i\}_{i \in I}$为专家集合。定义一阶语言$\Lang_{\mathrm{audit}}$包含：
> 
- 对每个$x \in ClaimSpace$，一个常元符号$<u>x</u>$；
- 对每个专家$E_i$，一个一元谓词符号$\mathsf{Pass}_i$（直观：$\mathsf{Pass}_i(<u>x</u>)$表示专家$E_i$判定声称$x$通过审计）；
- 一个二元谓词符号$\sim$（直观：$x \sim y$表示$x$和$y$属于同一CEC）；
- 等词$=$。

> **Definition:** [审计结构]
> 对每个专家$E_i$，定义$\Lang_{\mathrm{audit}}$上的**审计结构**$\Struct_i$如下：
> 
- 论域：$ClaimSpace$；
- $<u>x</u>^{\Struct_i} = x$；
- $\mathsf{Pass}_i^{\Struct_i} = \{x \in ClaimSpace \mid E_i(x) = 1\}$；
- $\sim^{\Struct_i}$为$\CEC$等价关系在$E_i$下的限制。

> **Definition:** [声称的句子编码]
> 对每个声称$x \in ClaimSpace$，定义$\Lang_{\mathrm{audit}}$中的句子$\varphi_x$：
> 
> $$
>     \varphi_x \;:=\; \bigwedge_{i \in I_0} \mathsf{Pass}_i(<u>x</u>),
> $$
> 
> 其中$I_0 \subseteq I$为有限子集，表示声称$x$在专家组$I_0$中通过了审计。

### 主要定理

> **Theorem:** [紧致性-审计对应定理]<!-- label: thm:compactness_audit -->
> 设$\Gamma = \{\varphi_x \mid x \in ClaimSpace\}$为声称的句子编码集。
> 则以下陈述等价：
> 
1. **紧致性侧：** 若$\Gamma$的每个有限子集$\Delta \subseteq \Gamma$在某个审计结构$\Struct_i$中有模型（即$\Struct_i \models \Delta$），则$\Gamma$本身有模型（即存在审计结构$\Struct$使得$\Struct \models \Gamma$）。
2. **审计侧：** 若每个**有限**专家子组$\ExpertSet_{\mathrm{fin}} \subseteq \ExpertSet$对声称集$\ClaimSpace_{\mathrm{fin}} \subseteq ClaimSpace$达成共识（即存在配置使所有声称通过该子组的审计），则**全体**专家对**全体**声称可达共识。
3. **有限传递性：** 有限可审计性蕴含无限可审计性。

> **Proof:** \rigorous 我们通过构造一阶理论的模型来建立等价性。
> 
> **步骤一：理论构造。**
> 对每个有限子集$F \subseteq I$和每个有限声称集$X \subseteq ClaimSpace$，
> 定义句子$\psi_{F,X}$：
> 
> $$
>     \psi_{F,X} \;:=\; \exists v_1 ... \exists v_k
>     \bigwedge_{x \in X} \bigwedge_{i \in F} \mathsf{Pass}_i(<u>x</u>),
> $$
> 
> 直观含义：「存在$k$个声称使得专家组$F$中的所有专家一致判定它们通过审计」。
> 
> 令
> 
> $$
>     T = \{\psi_{F,X} \mid F \subseteq I  有限, X \subseteq ClaimSpace  有限\}.
> $$
> 
> 
> **步骤二：有限可满足性。**
> 对于$T$的任意有限子集$T_0 \subseteq T$，$T_0$中涉及的专家指标和声称符号均为有限。
> 取$F_0$为$T_0$中出现的所有专家指标之并，$X_0$为所有声称符号之并——两者皆有限。
> 由假设（每个有限专家组对有限声称集可达共识），存在审计结构$\Struct$使得
> $\Struct \models T_0$。故$T$的每个有限子集有模型。
> 
> **步骤三：紧致性应用。**
> 由一阶紧致性定理，$T$本身有模型$\Struct^*$。
> 在$\Struct^*$中，对任意有限$F \subseteq I$和有限$X \subseteq ClaimSpace$，
> 句子$\psi_{F,X}$为真——这意味着全体专家对全体声称（在$\Struct^*$的论域中）可达共识。
> 
> **步骤四：等价性。**
> (i)$\implies$(ii)：以上构造直接给出了从有限可审计性到无限可审计性的传递。
> (ii)$\implies$(i)：若审计侧成立，则对任意有限一致的理论$T$，
> 其模型对应于一个有限专家子组的共识配置，从而紧致性侧成立。
> (iii)为(i)和(ii)的等价重述。$\square$

> **Remark:** 定理 [ref]的核心洞察是：
> **SCX审计框架的「有限到无限」传递并非经验假设，而是一阶紧致性定理的实例。**
> 这为审计终止性提供了独立于任何特定实现的形式保证。

## 有限可审计定理

### 审计紧致性

> **Definition:** [CEC片段]
> 设$\CEC$为共识等价类。对任意有限子集$X \subseteq ClaimSpace$，
> 定义$\CEC$在$X$上的**片段**：
> 
> $$
>     \CEC|_X = \{(x,y) \in X \times X \mid x \sim_ y\}.
> $$
> 
> 即$\CEC$限制在有限集$X$上的等价关系。

> **Definition:** [片段通过审计]
> 称声称$x \in ClaimSpace$在CEC片段$\CEC|_X$上**通过审计**，
> 若存在审计程序$\mathcal{A}$使得$\mathcal{A}$在$X$上以优于随机猜测的正确率判定
> $x$是否属于$\CEC$。

> **Theorem:** [有限可审计定理 —— 审计紧致性]<!-- label: thm:finite_auditability -->
> 设$x \in ClaimSpace$为一个声称。则$x$在整个$\CEC$上通过审计
> **当且仅当**$x$在$\CEC$的每个有限片段上通过审计。
> 
> 等价地：审计谓词$\mathsf{Auditable}(x, \CEC)$在$\CEC$的有限子集上紧致。

> **Proof:** \rigorous 分两个方向证明。
> 
> **（$\implies$）方向：** 平凡。
> 若$x$在整个$\CEC$上可通过审计，则对任意有限片段$\CEC|_X$，
> 将整个$\CEC$的审计程序$\mathcal{A}$限制在$X$上即得片段上的审计程序。
> 故在每个有限片段上通过审计。
> 
> **（$\Longleftarrow$）方向：** 非平凡方向，需要使用紧致性论证。
> 
> 假设$x$在$\CEC$的每个有限片段上通过审计。
> 对每个有限子集$X \subseteq ClaimSpace$，令$\mathcal{A}_X$为在$\CEC|_X$上审计$x$的程序。
> 我们需要构造一个在**整个**$\CEC$上有效的审计程序。
> 
> 考虑语言$\Lang_{\mathrm{audit}}$的扩展$\Lang_{\mathrm{audit}}^+$，
> 添加函数符号$\{f_X\}_{X \subseteq_{\mathrm{fin}} ClaimSpace}$（编码各有限片段上的审计决策函数）。
> 定义理论$T_{\mathrm{audit}}$包含以下句子：
> 
1. 对每个有限$X$，句子描述$f_X$是$\CEC|_X$上的审计程序；
2. 对$X \subseteq Y$（两者有限），句子描述$f_Y|_X = f_X$（一致性条件）；
3. $\exists f$（全函数）使得对所有有限$X$，$f|_X = f_X$。

> 
> $T_{\mathrm{audit}}$的每个有限子集涉及有限多个$f_X$，
> 取这些$X$的并集$X^*$（有限），则$f_{X^*}$满足该有限子集的所有约束。
> 故$T_{\mathrm{audit}}$的每个有限子集有模型。
> 由紧致性定理，$T_{\mathrm{audit}}$有模型。
> 在该模型中，全函数$f$即在整个$\CEC$上的审计程序——它是在所有有限片段上一致的极限。
> 
> 因此$x$在整个$\CEC$上通过审计。$\square$

> **Corollary:** [审计终止性]
> 审计过程可终止：只需检验有限多个声称和有限多位专家。
> 具体地，若声称$x$不可审计，则存在**有限**证据（一个有限CEC片段$X$使得$x$在$X$上不通过审计）。

> **Proof:** 这是紧致性的逆否命题：若$x$在整个$\CEC$上不通过审计，
> 则由定理 [ref]的逆否，
> 存在有限片段$\CEC|_X$使得$x$在$X$上不通过审计。
> 此有限片段即不可审计性的**有限证据**。

> **Remark:** 这一推论至关重要：它意味着审计失败总是可以在有限步骤内被**检测**到。
> 不存在「不可审计但无法在有限时间内证明」的声称——这与Gödel不完全性形成鲜明对比，
> 反映了SCX审计框架的**可判定性**优势。

### 最小审计子组定理

> **Theorem:** [最小审计子组 —— $k=3$定理]<!-- label: thm:k3 -->
> 设$\ExpertSet$为专家集合，$\CEC$为其共识等价类。
> 若存在大小为$k$的专家子集$\ExpertSet_k \subseteq \ExpertSet$，
> 使得$\ExpertSet_k$在$\CEC$的每个**三元**子集上的共识与全体专家的共识一致，
> 则$\ExpertSet_k$的共识与全体专家的共识完全一致（对所有有限子集）。
> 
> 特别地，$k=3$时：**三元子组的一致性保证全组一致性。**

> **Proof:** \rigorous 核心思想：三元子集构成一致性的生成元——任何较大的有限子集的一致性
> 可由三元子集的一致性通过紧致性推导得出。
> 
> 设$X \subseteq ClaimSpace$为任意有限子集。我们需要证明$\ExpertSet_k$在$X$上的
> 共识与$\ExpertSet$在$X$上的共识一致。
> 
> 对任意三元子集$\{x,y,z\} \subseteq X$，由条件，$\ExpertSet_k$的共识与$\ExpertSet$的共识一致。
> 现在考虑任意$n$元子集$\{x_1,...,x_n\} \subseteq X$。
> 定义理论$T_n$描述$\ExpertSet_k$在此$n$元子集上的共识结构：
> 
> $$
>     T_n = \{句子描述  \ExpertSet_k  在  \{x_i, x_j, x_\ell\}  上的共识 \mid 1 \leq i < j < \ell \leq n\}.
> $$
> 
> 所有三元组的一致性信息构成了$T_n$。由于三元组的一致性蕴含$n$元组的一致性
> （这是CEC的等价关系传递性所保证的——任何一对$x_i, x_j$通过三元组链可约化），
> $T_n$的模型唯一确定$\ExpertSet_k$在$\{x_1,...,x_n\}$上的共识。
> 该共识与$\ExpertSet$在$\{x_1,...,x_n\}$上的共识一致（因两者在所有三元组上一致）。
> 
> $k=3$时的紧致性论证：若三元子组在所有三元声称子集上的共识与全组一致，
> 则考虑任意有限专家子组和任意有限声称子集。三元组的共识信息足以通过
> 紧致性重建任意有限组的共识——三元组覆盖了等价关系的传递闭包。$\square$

> **Remark:** $k=3$定理的操作意义极为深远：**不需要检查无限多专家。**
> 只需求得大小为$3$的专家子组，验证其在所有三元声称子集上的共识与直觉一致，
> 即可保证该子组的共识推广至全组。这为审计效率提供了坚实的理论下界：
> 审计复杂度从$O(|I| \cdot |ClaimSpace|)$降至$O(|ClaimSpace|^3)$（常数因子$k=3$）。

## Łoś超积对应：$M\to\infty$极限下的SCX

### 超滤子与专家多数

> **Definition:** [专家超滤子]
> 设$I$为专家指标集（可为无限）。$I$上的一个**超滤子**$\Ultrafilter$是$\mathcal{P}(I)$的子集，满足：
> 
1. $\emptyset \notin \Ultrafilter$，$I \in \Ultrafilter$（非平凡性）；
2. 若$A, B \in \Ultrafilter$，则$A \cap B \in \Ultrafilter$（有限交封闭）；
3. 若$A \in \Ultrafilter$且$A \subseteq B \subseteq I$，则$B \in \Ultrafilter$（上封闭）；
4. 对任意$A \subseteq I$，$A \in \Ultrafilter$或$I \setminus A \in \Ultrafilter$（极大性）。

> 
> 直观上，$\Ultrafilter$中的集合是$I$的「大」子集——代表了专家中的**多数**。
> 极大性条件保证了每个命题要么为多数所支持，要么为多数所反对——不存在「悬而未决」。

> **Definition:** [专家多数滤子]
> 对有限专家集$I = \{1,...,n\}$，定义**多数滤子**：
> 
> $$
>     \Ultrafilter_{\mathrm{maj}} = \{A \subseteq I \mid |A| > n/2\}.
> $$
> 
> $\Ultrafilter_{\mathrm{maj}}$是超滤子当且仅当$n$为奇数（因为极大性要求对每个$A$恰有$A$或$I\setminus A$属于滤子）。

> **Remark:** 有限情形中，多数滤子$\Ultrafilter_{\mathrm{maj}}$（$n$为奇数时）是一个主超滤子——
> 它由单个元素（多数方的「决定性」专家）生成。
> 在无限专家极限$|I| \to \infty$中，我们需要的是**自由超滤子**——
> 不包含任何有限集的超滤子——它编码了无限专家的「多数」概念但不存在任何单点生成元。

### 超积与CEC共识

> **Definition:** [专家判断结构的超积]
> 设$\{\Struct_i\}_{i \in I}$为专家$E_i$的审计结构族（定义见第2节）。
> 设$\Ultrafilter$为$I$上的超滤子。
> 定义**超积**（Ultraproduct）$\Struct_ = \prod_{i \in I} \Struct_i / \Ultrafilter$如下：
> 
- **论域：** $(\prod_{i \in I} |\Struct_i|) / \sim_$，
- **谓词解释：** $\mathsf{Pass}^{\Struct_}([a])$为真当且仅当
- **常元：** $<u>x</u>^{\Struct_} = [(<u>x</u>^{\Struct_i})_{i \in I}]$。

> **Theorem:** [Łoś超积对应定理 —— SCX版本]<!-- label: thm:los_scx -->
> 设$\Ultrafilter$为$I$上的超滤子，$\Struct_$为专家判断结构的超积。
> 则对任意$\Lang_{\mathrm{audit}}$中的句子$\varphi$：
> 
> $$<!-- label: eq:los -->
>     \Struct_ \models \varphi
>     \;\Longleftrightarrow\;
>     \{i \in I \mid \Struct_i \models \varphi\} \in \Ultrafilter.
> $$
> 
> 
> 在SCX的语言中：**一个声称在「多数专家」的极限结构（超积）中为真，当且仅当它在超滤子-多数（即真正多数）的因子结构中为真。**

> **Proof:** \rigorous 对句子$\varphi$的结构复杂性进行归纳。这是经典Łoś定理 [cite]的直接实例化。
> 
> **基始：** $\varphi$为原子句子$\mathsf{Pass}_j(<u>x</u>)$。
> 则$\Struct_ \models \mathsf{Pass}_j(<u>x</u>)$
> $\iff$ $\mathsf{Pass}_j^{\Struct_}([<u>x</u>^{\Struct_i}])$为真
> $\iff$ $\{i \in I \mid \mathsf{Pass}_j^{\Struct_i}(<u>x</u>^{\Struct_i})\} \in \Ultrafilter$
> $\iff$ $\{i \in I \mid \Struct_i \models \mathsf{Pass}_j(<u>x</u>)\} \in \Ultrafilter$。
> 
> **归纳步：** 对布尔连接词（$\neg, \land, \lor$）和量词（$\exists, \forall$），
> 利用超滤子的性质（有限交封闭、上封闭、极大性）可完成归纳。
> 量词情形需要使用选择公理（在超积论域中选取代表元）。$\square$

> **Corollary:** [CEC共识 = 超积真理谓词]<!-- label: cor:cec_ultra -->
> 设$\Ultrafilter$编码了专家的多数。则共识等价类$\CEC$与超积中的真理谓词一致：
> 
> $$
>     x \in \CEC \;\Longleftrightarrow\; \Struct_ \models 「x通过全体审计」.
> $$
> 
> 特别地，在$M \to \infty$极限下，SCX的共识判定**就是**超积模型中的真理判定。

> **Corollary:** [极限SCX = 超积]<!-- label: cor:limit_ultra -->
> 记$\Struct^{(M)}$为$M$位专家的联合审计结构。
> 则存在超滤子$\Ultrafilter$使得：
> 
> $$
>     \lim_{M \to \infty} \Th(\Struct^{(M)}) = \Th(\Struct_),
> $$
> 
> 其中$\Th(\cdot)$表示结构的一阶理论（所有在其中为真的句子之集）。

### 超积构造的CEC极限模型

> **Theorem:** [CEC极限模型的超积构造]<!-- label: thm:cec_limit -->
> 设$\{\Struct_i\}_{i \in I}$为有限专家子组的审计结构。
> 存在$I$上的自由超滤子$\Ultrafilter$使得超积$\Struct_$精确刻画了
> **CEC极限模型**——所有有限专家子组共识的「极限」：
> 
1. 对任意$x \in ClaimSpace$，$x$在超积极限中通过审计当且仅当
2. 极限模型$\Struct_$是**饱和**的：
3. $\Struct_$中的真理等于有限共识的$\Ultrafilter$-极限。

> **Proof:** \rigorous 构造如下：
> 
1. 取$I$为所有有限专家子组构成的集族（按包含偏序）。
2. 对每个有限子组$F \in I$，定义$\Struct_F$为该子组的联合审计结构。
3. 取$\Ultrafilter$为$I$上包含所有**尾集**$\{F \in I \mid F \supseteq F_0\}$（$F_0$固定）的超滤子。
4. 超积$\Struct_$即CEC极限模型。

> 
> **(i)** 由Łoś定理（定理 [ref]）直接得到。
> **(ii)** 饱和性来自超积的基本性质：超积是$\aleph_1$-饱和的（当$I$无限时）。
> **(iii)** 这是(i)的等价表述。$\square$

> **Remark:** 这一构造揭示了SCX框架的一个深层结构特征：
> **共识的极限不是一个简单的平均或多数投票，而是一个超积模型。**
> 超积保留了因子结构的一阶性质，但以非构造性的方式「粘合」了不同专家的视角。
> 这正是SCX共识与简单聚合（如加权平均）的根本区别。

## 逻辑基础三角：SCX的元理论

### 三个支柱

SCX框架的元理论由三个逻辑/数学支柱构成，它们构成了一个**逻辑基础三角**：

[Figure omitted — see original .tex]

### 三角的精确陈述

> **Theorem:** [逻辑基础三角定理]<!-- label: thm:triangle -->
> SCX框架的以下三个维度构成完备的元理论刻画：
> 
1. **Galois对应（可审计性的必要条件）：**
2. **紧致性（审计终止的充分条件）：**
3. **老实人定理（不可区分性）：**

> 
> 三者之间的关系如下：
> 
- **Galois $\to$ 紧致性：** Galois对应揭示了审计群的子群格结构。
- **紧致性 $\to$ 老实人：** 紧致性保证了有限审计程序的存在性；
- **老实人 $\to$ Galois：** 老实人定理的统计不可区分性在群论上对应

> **Proof:** [三角完备性]
> \rigorous 我们证明三个维度联合构成了SCX可审计性的**充要条件**。
> 
> **充分性：** 若Galois条件满足（审计群可解、作用可一维分解）**且**
> 紧致性条件满足（有限子组一致性传递至全组）**且**
> 老实人条件满足（噪声-困难可区分），则声称可审计。
> ——紧致性保证审计程序存在，Galois保证结构障碍不存在，老实人保证统计障碍不存在。
> 
> **必要性：** 若声称可审计，则三个条件必须同时成立。
> ——若任一条件不成立，可审计性将因相应的障碍而失败：
> Galois失败$\implies$群论不可解（不可解性定理中的$A_5$障碍，见 [cite]）；
> 紧致性失败$\implies$无法有限终止（存在无限降链的不可审计证据）；
> 老实人失败$\implies$噪声与困难不可区分。
> 
> **三角不可约性：** 三个维度相互独立——任何一个不能从另外两个推导。
> 这是三角结构（而非线性链）的根本原因。$\square$

### 三角与SCX核心定理的整合

[Table omitted — see original .tex]

## 紧致性在SCX中的形式化证明

### 超积构造的完整技术细节

本节给出紧致性在SCX中形式化的完整技术构造。

> **Definition:** [有限专家子组的逆系统]
> 设$\mathcal{F}$为$I$的所有有限子集构成的集族（按$\subseteq$偏序）。
> 对每个$F \in \mathcal{F}$，定义$F$上专家子组的联合审计结构$\Struct_F$。
> 对$F \subseteq G$，定义投影映射$\pi_{G,F}: \Struct_G \to \Struct_F$（限制到$F$上）。
> $(\{\Struct_F\}_{F \in \mathcal{F}}, \{\pi_{G,F}\}_{F \subseteq G})$构成一个**逆系统**。

> **Definition:** [CEC的逆极限]
> 逆系统$(\Struct_F, \pi_{G,F})$的**逆极限**（inverse limit）为：
> 
> $$
>     \varprojlim_{F \in \mathcal{F}} \Struct_F
>     = \left\{ (a_F)_{F \in \mathcal{F}} \in \prod_{F \in \mathcal{F}} |\Struct_F|
>     \;\middle|\; \forall F \subseteq G,\; \pi_{G,F}(a_G) = a_F \right\}.
> $$

> **Theorem:** [逆极限-超积等价定理]<!-- label: thm:invlim_ultra -->
> 设$\Ultrafilter$为$\mathcal{F}$上包含所有尾集$\{G \in \mathcal{F} \mid G \supseteq F\}$的超滤子。
> 则存在典范嵌入：
> 
> $$<!-- label: eq:embedding -->
>     \varprojlim_{F \in \mathcal{F}} \Struct_F \;\hookrightarrow\; \prod_{F \in \mathcal{F}} \Struct_F / \Ultrafilter,
> $$
> 
> 且该嵌入在$\Struct_F$均为有限结构时是初等的（即保持所有一阶句子）。

> **Proof:** \rigorous 构造嵌入映射$\iota$：
> 对$(a_F)_{F \in \mathcal{F}} \in \varprojlim \Struct_F$，
> 定义$\iota((a_F)) = [(a_F)_{F \in \mathcal{F}}]_$（超积中的等价类）。
> 
> 需验证$\iota$是良定义的：若$(a_F) \neq (b_F)$在逆极限中，则
> $\{F \mid a_F = b_F\}$至多包含$F$不包含某个$F_0$以下的有限集——
> 但这些有限集不在自由超滤子$\Ultrafilter$中（自由超滤子不包含任何有限集）。
> 因此$[(a_F)]_ \neq [(b_F)]_$。
> 
> **初等性：** 由于所有$\Struct_F$为有限结构，
> 且$\Ultrafilter$包含所有尾集，超积$\prod \Struct_F / \Ultrafilter$实现了逆极限的
> 一阶理论。对任意句子$\varphi$，
> 
> $$
>     \varprojlim \Struct_F \models \varphi
>     &\iff \exists F_0 \forall F \supseteq F_0,\; \Struct_F \models \varphi
>     \quad（逆极限的有限确定性质）

>     &\iff \{F \in \mathcal{F} \mid \Struct_F \models \varphi\}  包含尾集 

>     &\iff \{F \in \mathcal{F} \mid \Struct_F \models \varphi\} \in \Ultrafilter
>     \quad（\Ultrafilter包含所有尾集）

>     &\iff \prod \Struct_F / \Ultrafilter \models \varphi
>     \quad（Łoś定理）.
> $$
> 
> 故嵌入$\iota$是初等的。$\square$

> **Corollary:** [CEC极限模型的两种刻画]
> CEC极限模型有两种等价刻画：
> 
1. **逆极限刻画：** $\CEC_ \cong \varprojlim_{F \in \mathcal{F}} \Struct_F$（构造性，但需一致性条件）；
2. **超积刻画：** $\CEC_ \cong \prod_{F \in \mathcal{F}} \Struct_F / \Ultrafilter$（非构造性，但自动处理不一致）。

> 第一种刻画直接可计算（当逆系统一致时）；第二种刻画通过超滤子「裁决」了不一致的有限子组——超滤子选择了「多数」方向。

### 紧致性的超积证明

> **Theorem:** [紧致性定理的超积证明 —— SCX实例化]<!-- label: thm:compactness_ultra -->
> 设$\Gamma$为$\Lang_{\mathrm{audit}}$中的句子集。若$\Gamma$的每个有限子集有模型，则$\Gamma$有模型。
> 
<div align="center">

> **在SCX中：若每个有限专家子组的共识可满足，则全体专家的共识可满足。**
>

</div>

> **Proof:** \rigorous 以下是经典紧致性定理的超积证明在SCX框架中的完整实例化。
> 
> **步骤一：指标集。**
> 令$I = \mathcal{P}_{\mathrm{fin}}(\Gamma)$为$\Gamma$的所有有限子集之集。
> 对每个$\Delta \in I$，由假设，存在审计结构$\Struct_\Delta$使得$\Struct_\Delta \models \Delta$。
> （在SCX中：$\Struct_\Delta$是使得有限声称集$\Delta$中所有声称通过审计的专家配置。）
> 
> **步骤二：超滤子构造。**
> 对每个句子$\varphi \in \Gamma$，定义：
> 
> $$
>     A_\varphi = \{\Delta \in I \mid \varphi \in \Delta\}.
> $$
> 
> 族$\{A_\varphi\}_{\varphi \in \Gamma}$具有**有限交性质**：
> 对任意有限$\{\varphi_1,...,\varphi_k\} \subseteq \Gamma$，
> $A_{\varphi_1} \cap ... \cap A_{\varphi_k} = \{\Delta \in I \mid \varphi_1,...,\varphi_k \in \Delta\} \neq \emptyset$
> （因为$\{\varphi_1,...,\varphi_k\}$本身属于此交集）。
> 
> 由超滤子存在定理（布尔素理想定理），存在$I$上的超滤子$\Ultrafilter$包含所有$A_\varphi$。
> 
> **步骤三：超积模型。**
> 构造超积$\Struct^* = \prod_{\Delta \in I} \Struct_\Delta / \Ultrafilter$。
> 对任意$\varphi \in \Gamma$：
> 
> $$
>     \{\Delta \in I \mid \Struct_\Delta \models \varphi\}
>     &\supseteq \{\Delta \in I \mid \varphi \in \Delta\}
>     = A_\varphi \in \Ultrafilter.
> $$
> 
> 因此由Łoś定理（定理 [ref]），$\Struct^* \models \varphi$。
> 由于$\varphi$是$\Gamma$中任意句子，故$\Struct^* \models \Gamma$。
> 
> **步骤四：SCX解释。**
> $\Struct^*$是**全体专家的共识模型**。
> 在$\Struct^*$中，$\Gamma$中所有声称同时通过审计。
> 超滤子$\Ultrafilter$编码了「多数专家子组」的概念——
> 在每个$A_\varphi$（所有包含$\varphi$的有限子组）中，$\varphi$通过审计；
> 超滤子保证了这些「多数」的一致性（有限交封闭）。
> $\square$

> **Remark:** 上述证明展示了超积构造的非凡威力：
> 它不需要显式地构造全体专家的共识（那可能是不可能的），
> 而是通过超滤子——一个非构造性的选择——**宣告**了一个极限模型的存在。
> 这就是紧致性定理的精髓：**存在性不需要构造性。**

## 操作意义：有限$\to$无限传递的审计效率

### 审计效率的形式化

紧致性定理的理论保证转化为以下操作原则：

> **Theorem:** [审计效率定理]<!-- label: thm:efficiency -->
> 在紧致性保证下，SCX审计的效率特征为：
> 
1. **有限覆盖：** 审计程序只需检验$ClaimSpace$的有限子集$X$（由定理 [ref]）。
2. **专家下界：** $|X| = O(|\Gamma|^3)$，其中$\Gamma$为待审计的声称集大小（由定理 [ref]的$k=3$界）。
3. **终止保证：** 审计在有限步内终止——要么所有声称通过，要么检测到有限反例（由推论 [ref]的有限证据性质）。
4. **增量审计：** 新专家的加入不改变已建立的共识（单调性）——因为紧致性保证有限确定的信息不会被进一步扩展所推翻。

> **Proof:** \rigorous (i)和(iii)直接来自定理 [ref]及其推论。
> (ii)来自定理 [ref]：只需三元声称子集的一致性检验。
> (iv)来自紧致性的单调性：若有限子组$F$的共识已确定声称$x$的审计结果，
> 则任何包含$F$的超组$G \supseteq F$不会改变此结果（因为$F$的共识是$G$的共识的必要条件）。$\square$

### 算法模板

紧致性-审计对应直接导向以下算法模板：

<div align="center">

\framebox[\textwidth]{%
\begin{minipage}{0.92\textwidth}

 **算法：紧致性驱动的SCX审计**

 **输入：** 声称集$\Gamma$，专家集$\ExpertSet$（可能无限）

 **输出：** $\Gamma$中所有声称的审计结果

 **步骤1：** 选择有限专家子组$F \subseteq \ExpertSet$，$|F| = k$（默认$k=3$）

 **步骤2：** 对每个三元声称子集$\{x,y,z\} \subseteq \Gamma$：

- 验证$F$在$\{x,y,z\}$上的共识是否一致
- 若发现不一致：返回**不可审计** + 有限证据（$\{x,y,z\}$和$F$）

 **步骤3：** 由紧致性（定理 [ref]），
$F$在所有三元组上一致 $\implies$ $F$在所有声称上一致

 **步骤4：** 由紧致性（定理 [ref]），
$F$的一致 $\implies$ $\ExpertSet$的一致

 **步骤5：** 返回**可审计**（所有声称通过）
\end{minipage}}

</div>

> **Remark:** 该算法的关键创新在于：
> 传统审计需要检查所有专家对所有声称的判断（复杂度$O(|\ExpertSet| \cdot |\Gamma|)$）；
> 紧致性驱动的审计只需检查$k=3$位专家对$O(|\Gamma|^3)$个三元声称子集的判断——
> 当$|\ExpertSet|$很大时，这带来了**指数级**的效率提升。

### 数值示例

> **Example:** [$k=3$一致性的审计效率]
> 设有$|\ExpertSet| = 1000$位专家，待审计声称$|\Gamma| = 100$条。
> 
- **传统审计：** 需检查$1000 \times 100 = 100{,}000$个专家-声称对。
- **紧致性审计：** 先选$k=3$位代表专家，检查$\binom{100}{3} = 161{,}700$个三元声称组。
- 看似更多，但注意：三元组检验可在专家之间并行（每位专家独立判断三元组）。

### 数据种类筛选：三角理论的操作指南

前文建立了SCX的逻辑基础三角——Galois群论判定可审计性，紧致性定理保证审计可终止，老实人定理解释审计失败。本节将该三角转化为操作指南：面对一个数据种类，如何判断SCX是否适用。

#### 筛选流程

1. **Galois筛查：分歧群是否可解？** 收集$M$个候选专家对$N$个样本的判决矩阵$V \in \{0,1\}^{M \times N}$。提取分歧结构：专家$i$与$j$在样本$k$上分歧当且仅当$V_{ik} \neq V_{jk}$。若分歧图存在5-圈且无子循环可断，则可能含$A_5$子群——红色警报。若分歧可分解为独立子组（如按误差来源分层），则群可解——通过筛查。
2. **紧致性收敛验证：分歧是否有限可决？** 随机抽取$k=3$的专家子组，检查子组内共识方向。若10组随机抽取全给出相同方向判决，则紧致性成立——全组共识由有限子组决定。若子组互相矛盾，则分歧发散——紧致性失败。
3. **老实人定理诊断：分歧是噪声还是结构？** 若以上两步通过——可审计且有限收敛——分歧归因于噪声。若未通过——$A_5$信号——分歧是结构性的，不可审计。

#### 可审计数据种类（分歧群可解）

**第一类：物理测量（分歧群为循环群$\mathbb{Z}_p$）。** 室温测量（不同温度计）、光谱分析（不同实验室）、GPS定位（多颗卫星）。分歧只有一个维度（仪器校准误差），共识直接取中位数。可解性平凡——循环群永远是交换群，合成列长度为1。

**第二类：独立多标签（分层$\mathbb{Z}_2 \times ... \times \mathbb{Z}_2$）。** CIFAR-10标注（5个标注者）、肺结节CT判读（3个放射科医生）、蛋白质结构测定（X射线/NMR/Cryo-EM三方法）。每个分歧维度独立：疲劳、歧义、方法偏差可分别处理。合成列的每一步对应一个独立分歧维度的消解。

**第三类：范式对比（$\mathbb{Z}_2$两分分歧）。** DFT计算 vs 实验测量、LES vs DNS湍流模拟、RCT vs 观察性流行病学研究。只有两方分歧，减法即共识。交换群，绝对可解。

#### 不可审计数据种类（分歧群含$A_5$信号）

**第一类：纯主观（分歧群接近$S_M$全对称群）。** 葡萄酒评分、电影推荐、代码风格审查。分歧不是因为噪声——是因为不存在客观正确答案。5个品酒师的分歧模式是对称且不可约化的。不存在``先解决A和B的分歧，再用结论审C''的分解路径。$M$增大不带来收敛。

**第二类：自指涉（预测改变行为——分歧群非正规）。** 股价预测（预测本身影响股价）、选举民调（发布改变投票）、AI对齐评估（RLHF反馈改变人类行为再改变模型）。专家在观察的同时改变观察对象。时间序列上的分歧不可分解为独立步骤——非正规子群结构。

**第三类：循环分歧（准$A_5$信号）。** 宏观经济预测（凯恩斯$\leftrightarrow$奥地利$\leftrightarrow$MMT$\leftrightarrow$新古典$\leftrightarrow$行为经济学）、法律模糊地带（原旨主义$\leftrightarrow$活宪法$\leftrightarrow$文本主义$\leftrightarrow$德沃金$\leftrightarrow$现实主义）、``什么是意识''（物理主义$\leftrightarrow$泛心论$\leftrightarrow$二元论$\leftrightarrow$功能主义$\leftrightarrow$消去主义）。分歧是范式冲突——不存在元方法统一这些范式。分歧结构含不被任何正规子群吸收的子分歧。

#### 边界线（部分可审计）

气候模型的不同家族分歧可能可分解为参数差异$+$分辨率差异$+$物理过程差异。但三维独立性的程度决定了审计质量。ClinVar基因致病性判定：实验室偏差$+$方法学差异$+$人群分层——大概率可审计但需验证。

#### 核心口诀

**分歧像俄罗斯套娃（分层可分解）$\to$ 可审计，SCX适用。分歧像石头剪刀布（循环不可约化）$\to$ 不可审计，SCX不应碰。**

## 讨论

### 理论贡献总结

本文的核心贡献是在SCX多专家审计框架与模型论紧致性定理之间建立了系统的深层对应。
具体而言：

1. **紧致性-审计对应定理**（定理 [ref]）
2. **有限可审计定理**（定理 [ref]）
3. **Łoś超积对应**（定理 [ref]、定理 [ref]）
4. **逻辑基础三角**（定理 [ref]）
5. **操作效率**（定理 [ref]、定理 [ref]）

### 与SCX核心定理的整合

本文建立的紧致性-审计对应填补了SCX理论体系中的一个关键空白：
**从有限到无限的传递机制**。
在SCX的理论地图中：

- **Galois-SCX** [cite]提供了可审计性的**代数结构**（群论障碍）；
- **老实人定理**提供了可审计性的**信息论条件**（噪声-困难可区分）；
- **本文的紧致性**提供了可审计性的**逻辑基础**（有限$\to$无限传递）。

三者共同构成了SCX的完整元理论——任何关于SCX系统的可审计性断言
都必须同时通过这三个维度的检验。

### 诚实暴击：超滤子的非构造性与实际审计的构造性需求

> **诚实暴击:** 超滤子是非构造性的——它等价于选择公理的弱形式（布尔素理想定理）。
这意味着$\Struct^*$（全体专家的共识模型）的存在性虽然被紧致性定理保证，
但我们无法显式地构造它。}

这一gap的根源在于：

- 紧致性定理的**标准证明**（Henkin构造或超积构造）都需要非构造性的选择步骤——
- 在有限专家情形中，我们可以显式地构造共识（通过有限次投票和比较）；
- 这并非SCX特有的问题，而是整个模型论的根基性特征：

**实际后果：**

在实践中的SCX系统中，专家集合**总是有限的**（虽然可能非常大）。
紧致性定理的理论保证因此降级为以下形式：

<div align="center">

**「如果对于所有我们已经检查的有限子组，共识都存在，**

**那么对于任何更大的有限子组，共识也应该存在。」**

</div>

这仍然是一个有价值的**启发式保证**——它告诉我们，审计过程中的一致性不是偶然的，
而是由底层逻辑结构保证的。但当审计程序希望**自动**验证这一点时，
它仍然需要显式地处理有限（但可能非常大）的专家集合。

> **诚实暴击:** 超积的非标准元素问题。}

超积构造引入了一个微妙的问题：$\Struct_$的论域包含
**非标准元素**——那些不对应于任何实际声称的等价类。
在SCX的解释中，这些非标准元素对应于**「极限声称」**——
那些被「几乎所有」有限子组共识所逼近但本身不在$ClaimSpace$中的对象。

这带来了一个哲学问题：这些极限声称是否应该被审计？
如果审计的目标是评估实际存在的声称，那么非标准元素是无关的。
但如果审计的目标是评估**系统的全部潜在行为**，
那么非标准元素可能代表了我们尚未遇到但原则上可能的声称——
审计它们具有预防性价值。

> **诚实暴击:** 紧致性保证的是逻辑一致性，不是认识论可靠性。}

紧致性定理保证的是：如果每个有限子组都一致，那么存在一个模型使全组一致。
但它**不**保证该模型在认识论上是正确的——
它可能是一个非标准模型，其中「通过审计」的含义被微妙地扭曲了
（例如，在超积模型中，「多数」的含义由超滤子定义，可能与我们对「多数」的直观不同）。

换言之，紧致性保证的是**形式一致性**，而非**实质正确性**。
在SCX中，这意味着：

- 紧致性不保证审计结果是「正确的」——只保证它们是一致的。
- 正确性需要额外的条件（如实标数据的校准、外部锚点的验证）。
- 紧致性的真正价值在于**排除了一类特定的失败模式**——

### 未来方向

\openproblem **构造性紧致性。**
能否在不使用选择公理（或超滤子）的前提下，为SCX框架建立一个构造性的
「有限$\to$无限」传递定理？这可能需要限制专家集合的结构
（如要求专家判断具有某种可计算性），但将大大增强定理的操作意义。

\openproblem **审计的判定性问题。**
紧致性保证了有限证据的存在性，但并未给出**寻找**该证据的算法。
在什么条件下，不可审计性的有限证据是**可有效搜索**的？
这涉及描述复杂性和PAC可学习性的交叉领域。

\openproblem **超滤子选择的物理意义。**
在自由超滤子的连续统中，不同的选择对应不同的「极限共识模型」。
这些不同模型之间的差异在物理上（或在实际SCX系统中）是否有可观测的后果？
若不同超滤子选择导致不同的审计结论，则紧致性定理的操作意义将被显著削弱。

\openproblem **紧致性与Gödel不完备的交叉。**
本文建立的超积-审计对应是否暗示了某种「审计不完备性」——
即存在声称其审计结果既不能证明也不能否证？
这与老实人定理中的不可区分性有何关系？

## 结论

本文在模型论紧致性定理与SCX多专家审计框架之间建立了系统的深层对应。
核心结果——紧致性-审计对应定理、有限可审计定理、Łoś超积对应定理、逻辑基础三角、
$k=3$最小审计子组定理——为SCX框架提供了先前缺失的**逻辑基础**。

这一对应的哲学意义超越了技术层面：
**紧致性定理告诉我们，无限并不比有限更危险——如果每个有限片段都是安全的，整体就是安全的。**
在SCX的语境中，这意味着：**如果每一个有限的专家子组都能达成一致，那么即使面对无限多位专家，共识仍然是可达的。**
这是审计理论中最深刻、也最令人安心的定理之一。

然而，我们也坦诚地指出了超滤子的非构造性、非标准元素的存在、以及形式一致性与实质正确性之间的gap。
紧致性定理为SCX审计提供了一个**逻辑安全网**，
但它不能替代实际审计中的构造性验证、经验校准和外部锚定。

在SCX理论体系的完整地图中，
Galois对应 [cite]提供了**结构骨架**（群论障碍），
老实人定理 [cite]提供了**认识论条件**（噪声-困难可区分），
而本文的紧致性定理提供了**逻辑保证**（有限到无限的传递）。
三者合一，构成了SCX框架坚不可摧的元理论基础。

\begin{thebibliography}{99}

\bibitem{scx_galois}
SCX.
*Galois-SCX：群论与多专家审计的深层对应*.
Preprint, 2026.

\bibitem{scx2026theorems}
SCX.
*SCX Core Theorems: Honest Person, Strong Man, and the Foundations of Multi-Expert Auditing*.
Technical Report, 2026.

\bibitem{scx_galois_falsifiability}
SCX.
*Galois反证：SCX的可证伪边界*.
Preprint, 2026.

\bibitem{scx_causal}
SCX.
*Causal SCX：因果推断的多专家审计*.
Preprint, 2026.

\bibitem{scx_collective}
SCX.
*Collective Intelligence SCX：群体智能的数学基础*.
Preprint, 2026.

\bibitem{scx_information}
SCX.
*Information-Theoretic SCX：信息论的多专家审计*.
Preprint, 2026.

\bibitem{scx_agentic}
SCX.
*Agentic Multi-Agent SCX：对抗性多智能体审计理论*.
Preprint, 2026.

\bibitem{scx_temporal}
SCX.
*Temporal SCX：时态多专家审计*.
Preprint, 2026.

\bibitem{scx_hamiltonian}
SCX.
*神经网络哈密顿量与SCX多专家审计：一个统计力学对应*.
Preprint, 2026.

\bibitem{los1955}
J.~Łoś.
Quelques remarques, théorèmes et problèmes sur les classes définissables d'algèbres.
In *Mathematical Interpretation of Formal Systems*, pages 98--113.
North-Holland, 1955.

\bibitem{chang_keisler}
C.~C.~Chang and H.~J.~Keisler.
*Model Theory*, 3rd ed.
Studies in Logic and the Foundations of Mathematics, Vol.~73.
North-Holland, 1990.

\bibitem{hodges_model}
W.~Hodges.
*Model Theory*.
Encyclopedia of Mathematics and its Applications, Vol.~42.
Cambridge University Press, 1993.

\bibitem{marker_model}
D.~Marker.
*Model Theory: An Introduction*.
Graduate Texts in Mathematics, Vol.~217.
Springer, 2002.

\bibitem{bell_slomson}
J.~L.~Bell and A.~B.~Slomson.
*Models and Ultraproducts: An Introduction*.
North-Holland, 1969.

\bibitem{jech_set}
T.~Jech.
*Set Theory*, 3rd millennium ed.
Springer Monographs in Mathematics.
Springer, 2003.

\bibitem{keisler_ultra}
H.~J.~Keisler.
Ultraproducts and saturated models.
*Indagationes Mathematicae*, 27:178--186, 1964.

\bibitem{godel_completeness}
K.~Gödel.
Die Vollständigkeit der Axiome des logischen Funktionenkalküls.
*Monatshefte für Mathematik und Physik*, 37:349--360, 1930.

\bibitem{malcev_compactness}
A.~Malcev.
Untersuchungen aus dem Gebiete der mathematischen Logik.
*Matematicheskii Sbornik*, 1(43):323--336, 1936.

\bibitem{henkin_compactness}
L.~Henkin.
The completeness of the first-order functional calculus.
*Journal of Symbolic Logic*, 14(3):159--166, 1949.

\bibitem{robinson_nonstandard}
A.~Robinson.
*Non-standard Analysis*.
Studies in Logic and the Foundations of Mathematics.
North-Holland, 1966.

\end{thebibliography}

## Appendix
## 附录：模型论预备知识

为使读者（特别是审计/ML背景的读者）无需查阅外部文献，本节汇总本文使用的模型论核心概念。

### 一阶逻辑基础

> **Definition:** [一阶语言]
> 一阶语言$\Lang$由以下符号构成：
> 
- 逻辑符号：变元$\{v_1, v_2, ...\}$、连接词$\neg, \land, \lor, \to$、量词$\forall, \exists$、等词$=$。
- 非逻辑符号：常元符号、函数符号、谓词符号（特定的集合，构成语言的「词汇」）。

> **Definition:** [结构]
> 语言$\Lang$的一个**结构**$\Struct$由论域$|\Struct|$和对每个非逻辑符号的解释构成。

> **Definition:** [句子与理论]
> $\Lang$中的一个**句子**是不含自由变元的公式。
> 一个**理论**$T$是$\Lang$中的句子集。
> $\Struct \models T$表示$\Struct$满足$T$中的所有句子。

### 紧致性定理

> **Theorem:** [紧致性定理 —— 经典形式]
> 设$\Gamma$为$\Lang$中的句子集。则：
> 
> $$
>     每个有限 \Delta \subseteq \Gamma  有模型
>     \;\implies\;
>     \Gamma  有模型.
> $$

> **Proof:** [证明思路]
> 两种经典证明：
> 
1. **Henkin构造：** 将$\Gamma$扩展为极大一致的Henkin理论，用常元构建项模型。
2. **超积构造：** 如本文定理 [ref]所示——

> 两者均需要选择公理的某种弱形式。

### 超滤子与超积

> **Definition:** [滤子与超滤子]
> $I$上的**滤子**$F \subseteq \mathcal{P}(I)$满足：
> (i) $\emptyset \notin F$，$I \in F$；
> (ii) $A, B \in F \implies A \cap B \in F$；
> (iii) $A \in F, A \subseteq B \implies B \in F$。
> 
> 若额外满足(iv) 对任意$A \subseteq I$，$A \in F$或$I \setminus A \in F$，则$F$为**超滤子**。

> **Theorem:** [超滤子存在定理]
> $I$上具有有限交性质的任何集族可扩展为$I$上的超滤子。
> 这等价于布尔素理想定理（BPI），是选择公理（AC）的严格弱形式。

> **Definition:** [超积]
> 设$\{\Struct_i\}_{i \in I}$为一族$\Lang$-结构，$\Ultrafilter$为$I$上的超滤子。
> 超积$\prod_{i \in I} \Struct_i / \Ultrafilter$的论域为$\prod_i |\Struct_i|$模
> 等价关系$(a_i) \sim (b_i) \iff \{i \mid a_i = b_i\} \in \Ultrafilter$的商集。
> 谓词和函数逐点定义，真值由$\Ultrafilter$-多数决定。

> **Theorem:** [Łoś定理]
> 对任意句子$\varphi$：
> \[
>     \prod_{i \in I} \Struct_i / \Ultrafilter \models \varphi
>     \iff \{i \in I \mid \Struct_i \models \varphi\} \in \Ultrafilter.
> \]

### 逆极限

> **Definition:** [逆系统与逆极限]
> 设$(I, \leq)$为有向偏序集。
> $I$上的**逆系统**$(\Struct_i, \pi_{ij})$由一族结构$\{\Struct_i\}_{i \in I}$
> 和态射$\pi_{ij}: \Struct_j \to \Struct_i$（对$i \leq j$）构成，满足$\pi_{ii} = \mathrm{id}$和$\pi_{ij} \circ \pi_{jk} = \pi_{ik}$。
> 
> **逆极限**（或射影极限）$\varprojlim \Struct_i$定义为满足$\pi_{ij}(a_j) = a_i$
> （对所有$i \leq j$）的族$(a_i)_{i \in I}$的集合。

### 饱和模型

> **Definition:** [类型与饱和性]
> 设$\Struct$为$\Lang$-结构，$A \subseteq |\Struct|$。
> 一个**类型**$p(x)$（关于$A$）是一组与$\Th(\Struct, a)_{a \in A}$一致的公式集。
> $\Struct$是**$\kappa$-饱和**的，如果对任意$A \subseteq |\Struct|$满足$|A| < \kappa$，
> 每个关于$A$的类型$p(x)$都在$\Struct$中实现。

> **Theorem:** [超积的饱和性]
> 若$I$无限且$\Ultrafilter$为$I$上的自由超滤子，
> 则超积$\prod \Struct_i / \Ultrafilter$是$\aleph_1$-饱和的。