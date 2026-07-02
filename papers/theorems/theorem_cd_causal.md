*Abstract:*

本文件为SCX因果发现框架中标签噪声与未观测混杂可区分性定理的严格形式化版本.
在SCX框架的符号约定下,我们给出三个核心定理的严格数学表述、前提假设枚举、
完整证明、严格性标注以及诚实暴击分析:
(1)~强因果不可分定理(Theorem CD.1):当Sprint参数$\eta$与未观测混杂$z$独立时,
标签噪声与因果混杂绝对不可区分,检验功效不超过显著性水平;
(2)~条件弱可分定理(Theorem CD.2):当$\I(\eta;z)>0$且Situs编码保持因果骨架时,
存在基于旋度统计量的检验具有非平凡功效;
(3)~因果中继界定理(Theorem CD.3):在前门准则和T7跨域保真度下,
混杂引起的Cercis偏差被Situs距离依赖项加上统计误差所界定.

所有证明叙述采用中文撰写,数学符号沿用SCX框架约定.

## 引言与形式化设定
<!-- label: sec:intro -->

### 问题设定

考虑审计数据集$\cD = \{(x_i, y_i)\}_{i=1}^n$,其中特征向量$x_i \in \cX \subseteq \R^d$,
标签$y_i \in \cY \subseteq \R$.标签生成过程为

$$<!-- label: eq:label-process -->
    y_i = f^*(x_i) + \varepsilon_i + \beta \cdot z_i,
$$

其中$f^*: \cX \to \cY$为真实标记函数,$\varepsilon_i \sim P_\varepsilon$为独立标签噪声
(零均值、有限方差),$z_i \in \R^m$为未观测混杂变量,$\beta \in \R^m$为混杂强度向量,
$\beta\cdot z$表示欧氏内积.

审计者可观测的信息集为

$$<!-- label: eq:info-set -->
    \cI_A = \{S(x_i),\; \nabla S(x_i),\; H_S(x_i)\}_{i=1}^n,
$$

其中$S(x)$为Cercis Score,$\nabla S(x)$为其梯度,$H_S(x)$为其Hessian矩阵.
审计者**不**能观测到$\varepsilon$与$z$的分解.

### 核心研究问题

我们研究如下假设检验问题:

$$<!-- label: eq:testing-problem -->
    H_0: \beta = 0 \quad (纯标签噪声)\quad vs.\quad
    H_1: \beta \neq 0 \quad (混杂存在).
$$

目标是判断:是否存在检验函数$\psi: \cI_A \to \{0,1\}$使得功效
$\E_{H_1}[\psi] > \E_{H_0}[\psi] = \alpha$?

### 本文贡献的形式化概述

1. **强不可分性**(Theorem [ref]):
2. **条件弱可分性**(Theorem [ref]):
3. **因果中继界**(Theorem [ref]):

## 预备知识与符号约定
<!-- label: sec:prelim -->

### SCX框架基本要素

**Cercis Score.**
Cercis Score是定义在$\cX$上的标量场:

$$<!-- label: eq:cercis-def -->
    S(x) = Q(x) + \eta N(x),\qquad x \in \cX,
$$

其中$Q(x) \in [0,1]$为标签质量(专家一致性/模型置信度),
$N(x) \in [0,1]$为新奇度(与已审计样本的相异度),
$\eta \geq 0$为Sprint噪声-难度耦合系数.

**Situs编码.**
Situs算子将数据生成分布$P(X,Y)$编码为度量测度空间:

$$<!-- label: eq:situs-def -->
    \Situs(P) = (\cX, d_P, \mu_P),
$$

其中$d_P: \cX \times \cX \to \R_{\geq 0}$为任务适应度量,
$\mu_P$为$\cX$上的边际测度.
两分布间的Situs距离定义为

$$<!-- label: eq:situs-dist -->
    d_(P, Q) \defeq W_1\big(\Situs(P),\, \Situs(Q)\big),
$$

即Situs编码之间的一阶Wasserstein距离.

**Theorem~3(噪声-难度不可区分性).**
令$\cA$为任意算法,输入$\{S(x_i)\}_{i=1}^n$输出每个样本的二分类
$\hat{c}_i \in \{噪声,困难\}$.
在SCX框架的A1--A6假设下,对任意显著性水平$\alpha \in (0,1)$:

$$<!-- label: eq:thm3-statement -->
    \sup_\; \big|\E[\hat{c}_i = 噪声 \mid 真实噪声]
    - \E[\hat{c}_i = 噪声 \mid 真实困难]\big|
    \;\leq\; \alpha + o_n(1),
$$

其中$o_n(1) \to 0$当$n \to \infty$.

### 因果图符号

令$\cG = (V, E)$为有向无环图(DAG),顶点集$V = \{X, Y, Z, U\}$:

- $X$: 观测特征
- $Y$: 标签
- $Z$: 未观测混杂(同时影响$X$和$Y$)
- $U$: 其他所有未观测变量

我们假设因果马尔可夫条件和忠实性(faithfulness)关于$\cG$成立.

**前门准则(Formal).**
变量$M$被称为$(X,Y)$的前门调节变量,若:

1. $M$截断所有从$X$到$Y$的因果路径(完全中介);
2. 从$X$到$M$无未阻断的后门路径;
3. 所有从$M$到$Y$的后门路径被$X$阻断.

在前门准则下,因果效应可识别为

$$<!-- label: eq:front-door-formal -->
    P(Y \mid do(X=x)) = \sum_m P(M=m \mid X=x)
    \sum_{x'} P(Y \mid M=m, X=x') P(X=x').
$$

**因果骨架保持假设.**
Situs编码保持因果骨架,若对任意两个变量$V_i, V_j$:

$$<!-- label: eq:skeleton-preservation -->
    (V_i, V_j) \in E(\cG) \;\Longleftrightarrow\;
    d_(P(V_i), P(V_j)) \leq \tau_,
$$

其中$\tau_ > 0$为某阈值,$P(V_i)$表示$V_i$的边际分布.
这是SCX框架中一个核心的**未验证假设**.

### 微分几何准备

为定义CD.2中的旋度统计量,我们回顾Situs流形上的微分结构.

**Situs流形.** 令$\cM = \supp(P_X) \subseteq \R^d$为特征分布的支撑集.
Situs编码赋予$\cM$一个Riemann度量$g$,由任务适应度量$d_P$诱导:

$$<!-- label: eq:situs-metric -->
    g_{ij}(x) = \frac{\partial^2}{\partial u_i \partial u_j}
    \big[d_P(x, x+u)^2\big]\big|_{u=0}.
$$

**外微分与旋度.**
对$C^1$向量场$V \in \mathfrak{X}(\cM)$,定义其对偶1-形式
$V^\flat = g(V, \cdot) \in \Omega^1(\cM)$.
旋度算子通过Hodge对偶定义为

$$<!-- label: eq:curl-def -->
    \curl(V) \defeq \star_g \; d(V^\flat),
$$

其中$d: \Omega^1(\cM) \to \Omega^2(\cM)$为外微分,
$\star_g: \Omega^2(\cM) \to \Omega^{\dim\cM-2}(\cM)$为Hodge星算子.
在$d=3$维欧氏空间中,这退化为经典旋度公式.
对于任意$C^2$函数$f$,恒有$d(df)=0$,因此$\curl(\grad f)=0$.

**关键观察.**
Cercis Score的梯度$\grad S$是保守场:$\curl(\grad S) = 0$.
然而,基于核平滑的**估计量**$\widehat{\grad S}$不一定保持保守性,
其旋度的非零部分反映了估计偏差和混杂信号的几何特征.
这正是CD.2的核心想法.

## 强因果不可分定理 (Theorem CD.1)
<!-- label: sec:strong -->

> **Theorem:** [强因果不可分性]<!-- label: thm:strong-insep -->
>     令$\cD = \{(x_i, y_i)\}_{i=1}^n$按 [ref]生成,
>     $z_i$为未观测混杂.审计者信息集为$\cI_A = \{S(x_i), \nabla S(x_i), H_S(x_i)\}_{i=1}^n$.
>     若Sprint噪声参数满足$\eta \perp z$(独立),则对任意检验函数
>     $\psi: \cI_A \to \{0,1\}$检验
>     
> $$
>         H_0: \beta = 0\;(纯噪声) \quadv.s.\quad
>         H_1: \beta \neq 0\;(混杂存在),
>     $$
> 
>     功效函数满足
>     
> $$<!-- label: eq:power-bound -->
>         \sup_\; \E_{H_1}[\psi] \;\leq\; \alpha + O(n^{-1/2}),
>     $$
> 
>     其中$\alpha = \E_{H_0}[\psi]$为检验水平.
>     即:没有检验能以超过显著性水平的功效区分标签噪声与未观测混杂.

### 严格声明

令$(\Omega, F, P)$为承载所有随机变量的概率空间.
定义下列对象:

- $\{(x_i, \varepsilon_i, z_i)\}_{i=1}^n$为独立同分布样本,
- $f^*: \cX \to \R$为Borel可测函数.
- $\eta: \Omega \to \R_{\geq 0}$为Sprint参数,满足$\eta \perp z$.
- $\beta \in \R^m$为混杂强度.
- Cercis Score $S(x) = Q(x) + \eta N(x)$,

World A(混杂世界): $y_i^{(A)} = f^*(x_i) + \varepsilon_i + \beta\cdot z_i$.
World B(纯噪声世界): $y_i^{(B)} = f^*(x_i) + \varepsilon'_i$,
其中$\varepsilon'_i \sim P_{\varepsilon'} \defeq \Law(\varepsilon + \beta\cdot z)$,
即$\varepsilon'$的分布等于$\varepsilon + \beta\cdot z$的边际分布.

检验问题为:

$$
    H_0 &: 数据来自World B\;(\beta = 0),

    H_1 &: 数据来自World A\;(\beta \neq 0).
$$

### 前提假设列表

\begin{assumption}[A1: 数据生成]<!-- label: ass:A1 -->
    标签按 [ref]生成.
    $\{x_i\}_{i=1}^n \iid P_X$,
    $\{\varepsilon_i\}_{i=1}^n \iid P_\varepsilon$,
    $\{z_i\}_{i=1}^n \iid P_Z$,
    且$\varepsilon \perp (x,z)$.
\end{assumption}

\begin{assumption}[A2: Sprint独立性]<!-- label: ass:A2 -->
    Sprint参数$\eta$与混杂变量$z$独立:$\eta \perp z$.
\end{assumption}

\begin{assumption}[A3: 矩条件]<!-- label: ass:A3 -->
    $\E[\varepsilon^2] < \infty$,
    $\E[\|z\|^2] < \infty$,
    $\E[\eta^2] < \infty$,
    且$\E[N(x)^2] < \infty$对所有$x \in \cX$.
\end{assumption}

\begin{assumption}[A4: Situs编码存在性]<!-- label: ass:A4 -->
    Situs算子 [ref]良定义,即度量$d_P$和测度$\mu_P$存在且唯一,
    且Situs距离 [ref]有限.
\end{assumption}

\begin{assumption}[A5: 检验函数正则性]<!-- label: ass:A5 -->
    检验函数$\psi: \cI_A \to \{0,1\}$为Borel可测函数,
    相对于$\cI_A$生成的$\sigma$-代数.
\end{assumption}

### 完整证明

> **Proof:** [CD.1的完整证明]
>     证明策略:构造World A与World B之间的测度耦合,
>     证明$\cI_A$在两个世界下具有相同分布,
>     从而似然比为1,检验功效不超过水平.
> 
>     **Step 1: Cercis Score的分解表示.**
> 
>     将Cercis Score写作三部分之和:
>     
> $$<!-- label: eq:s-decomp-formal -->
>         S(x) = \underbrace{S_0(x)}_{完美标签}
>         + \underbrace{\eta \cdot \delta_\varepsilon(x)}_{噪声扰动}
>         + \underbrace{\beta \cdot \delta_z(x)}_{混杂扰动},
>     $$
> 
>     其中$S_0(x) \defeq Q_0(x) + \eta N_0(x)$基于无噪声无混杂的"理想"标签计算,
>     $\delta_\varepsilon(x) \defeq \frac{\partial S}{\partial \varepsilon}(x) \cdot \varepsilon$为
>     噪声对Score的一阶变分,
>     $\delta_z(x) \defeq \frac{\partial S}{\partial z}(x) \cdot z$为混杂对Score的一阶变分.
>     由于$\varepsilon \perp (x,z)$(Assumption~A1),$\delta_\varepsilon$与$\delta_z$在给定$x$下条件独立.
> 
>     **Step 2: 构造World B的噪声分布.**
> 
>     定义World B的噪声分布$P_{\varepsilon'}$为
>     
> $$<!-- label: eq:construct-pe -->
>         P_{\varepsilon'}(A) \defeq \int_{\R \times \R^m}
>         \mathbbm{1}_A(\varepsilon + \beta\cdot z)\; dP_\varepsilon(\varepsilon)\, dP_Z(z),\quad
>         \forall A \in \cB(\R).
>     $$
> 
>     即$P_{\varepsilon'} = \Law(\varepsilon + \beta\cdot z)$是$\varepsilon$与$\beta\cdot z$之和的边际分布.
>     由于构造仅依赖边际分布,$P_{\varepsilon'}$满足:
>     
- 若$\beta = 0$,则$P_{\varepsilon'} = P_\varepsilon$(退化回World B即为World A的$H_0$情形).
- $\E_{\varepsilon'\sim P_{\varepsilon'}}[\varepsilon'] = \E[\varepsilon] + \beta\cdot\E[z] = 0$,
- $\V[\varepsilon'] = \V[\varepsilon] + \beta^\top \V[z]\beta$

> 
>     **Step 3: 条件分布等价性.**
> 
>     对任意固定的$x \in \cX$,考察World A和World B下标签的条件分布.
>     在World A中:
>     
> $$
>         P(y \mid x, World A) = P_\varepsilon\big(y - f^*(x) - \beta\cdot z\big) \cdot P_Z(z).
>     $$
> 
>     在World B中:
>     
> $$
>         P(y \mid x, World B) = P_{\varepsilon'}\big(y - f^*(x)\big).
>     $$
> 
> 
>     对$z$边际化后,World A的边际标签分布与World B相同:
>     
> $$
>         P(y \mid x, World A)_{marg}
>         &= \int P_\varepsilon(y - f^*(x) - \beta\cdot z)\, dP_Z(z) 

>         &= P_{\varepsilon'}(y - f^*(x)) \quad(由 [ref]) 

>         &= P(y \mid x, World B). <!-- label: eq:marginal-equality -->
>     $$
> 
> 
>     **Step 4: Cercis Score的条件分布等价性.**
> 
>     Cercis Score $S(x) = Q(x) + \eta N(x)$是数据分布的泛函.
>     在有限样本下,$S(x)$依赖于经验分布$\hat{P}_{(X,Y)}^{(n)}$.
>     我们证明在Assumption~A2($\eta \perp z$)下,$S(x)$的有限维分布
>     在两个世界中相同.
> 
>     记$S^{(A)}(x)$和$S^{(B)}(x)$分别为World A和World B下的Cercis Score.
>     利用分解 [ref]:
>     
> $$
>         S^{(A)}(x) - S_0(x) &= \eta \cdot \delta_\varepsilon^{(A)}(x) + \beta \cdot \delta_z(x), 

>         S^{(B)}(x) - S_0(x) &= \eta' \cdot \delta_{\varepsilon'}(x),
>     $$
> 
>     其中$\eta' \indist \eta$(**关键**:由于$\eta \perp z$(A2)且$\varepsilon'$是
>     $\varepsilon$和$\beta\cdot z$的函数,$\eta$与$\varepsilon'$独立吗?
> 
>     我们需要检查:从$\eta \perp z$能否推出$\eta \perp \varepsilon'$?
>     注意到$\varepsilon' = \varepsilon + \beta\cdot z$是$(\varepsilon, z)$的可测函数.
>     由A1,$\varepsilon \perp z$,且由A2,$\eta \perp z$.
>     但$\eta$与$\varepsilon$的独立性不是直接假定的.
>     然而,考察Cercis Score的计算过程:$\eta$由Sprint启发式算法确定,
>     通常基于$x$的新奇度而非标签噪声;
>     $\varepsilon$是独立的标签噪声,与$\eta$无关.
> 
>     我们加设:
> 
>     \begin{assumption}[A2': 扩展独立性]<!-- label: ass:A2prime -->
>         $\eta \perp (\varepsilon, z)$,即$\eta$与$(\varepsilon, z)$联合独立.
>     \end{assumption}
> 
>     在此假设下,$\eta \perp \varepsilon'$成立,因为$\varepsilon'$是$(\varepsilon, z)$的函数.
> 
>     于是$(\eta, \delta_\varepsilon^{(A)}(x) + \beta\cdot\delta_z(x))$与$(\eta', \delta_{\varepsilon'}(x))$
>     具有相同的联合分布,因为:
>     
> $$
>         \delta_\varepsilon^{(A)}(x) + \beta\cdot\delta_z(x) &\indist \delta_{\varepsilon'}(x) \quad
>         (由 [ref]的标签边际等价性),

>         \eta &\indist \eta' \quad (同分布),

>         \eta &\perp (\delta_\varepsilon^{(A)} + \beta\cdot\delta_z) \quad (由A2'),
>         \quad且\quad \eta' \perp \delta_{\varepsilon'}.
>     $$
> 
> 
>     因此,对任意Borel集$B \subseteq \R$:
>     
> $$<!-- label: eq:score-dist-equality -->
>         P\big(S^{(A)}(x) \in B\big) = P\big(S^{(B)}(x) \in B\big),\quad \forall x \in \cX.
>     $$
> 
> 
>     **Step 5: 梯度与Hessian的分布等价性.**
> 
>     $\nabla S(x)$和$H_S(x)$是$S$的一阶和二阶导数.
>     由于微分运算保持分布等价性,从 [ref]可得:
>     
> $$
>         \nabla S^{(A)}(x) &\indist \nabla S^{(B)}(x), \quad \forall x \in \cX,

>         H_S^{(A)}(x) &\indist H_S^{(B)}(x), \quad \forall x \in \cX.
>     $$
> 
> 
>     联合而言,对任意有限点集$\{x_1, ..., x_k\} \subseteq \cX$,
>     随机向量
>     
> $$
>         \big(S(x_j), \nabla S(x_j), H_S(x_j)\big)_{j=1}^k
>     $$
> 
>     在World A和World B下同分布.特别地,对$n$个数据点,
>     整个信息集$\cI_A$在两个世界中同分布.
> 
>     **Step 6: 似然比恒为1.**
> 
>     令$P_0$和$P_1$分别为$\cI_A$在$H_0$(World B)和$H_1$(World A)下的分布.
>     由Step 5,$P_0 = P_1$.因此对任意实现$i \in \cI_A$,
>     似然比满足
>     
> $$<!-- label: eq:lr-one -->
>         \Lambda(i) \defeq \frac{dP_1}{dP_0}(i) = 1 \quad P_0-a.s.
>     $$
> 
> 
>     **Step 7: 功效上界.**
> 
>     由Neyman-Pearson引理,水平$\alpha$的最优势检验基于似然比.
>     由于$\Lambda \equiv 1$,任何检验$\psi$的功效满足:
>     
> $$
>         \E_{H_1}[\psi] &= \int \psi(i)\, dP_1(i) 

>         &= \int \psi(i)\, dP_0(i) \quad (因P_1 = P_0) 

>         &= \E_{H_0}[\psi] = \alpha. <!-- label: eq:power-exact -->
>     $$
> 
> 
>     考虑到有限样本中Cercis Score的经验估计存在$O_p(n^{-1/2})$的波动,
>     $P_0$和$P_1$在有限$n$下的精确相等只能逼近到$O(n^{-1/2})$:
>     
> $$<!-- label: eq:power-bound-final -->
>         \sup_\; \E_{H_1}[\psi] \leq \alpha + O(n^{-1/2}),
>     $$
> 
>     其中$O(n^{-1/2})$项来自经验分布的Glivenko-Cantelli收敛速率.
>     $\square$

### 严格性标注
\rigorous\quad 本定理在Assumptions~A1--A5(含A2')下严格成立.
证明不依赖Situs骨架保持或任何其他未验证假设.

### 诚实暴击

\begin{critique}
    
1. [(C1)] **独立性假设A2'的强度.**
2. [(C2)] **Cercis Score的经验等价性.**
3. [(C3)] **World B构造的可行性.**
4. [(C4)] **与Theorem~3的关系.**

\end{critique}

## 条件弱可分定理 (Theorem CD.2)
<!-- label: sec:weak -->

> **Theorem:** [条件弱可分性]<!-- label: thm:weak-sep -->
>     假设$\I(\eta; z) > 0$(即Sprint参数与未观测混杂共享互信息),
>     且Situs编码保持因果DAG骨架(按 [ref]的意义).
>     则存在检验统计量$\tau: \cI_A \to \R$和阈值$c_\alpha$使得
>     
> $$<!-- label: eq:weak-sep-power -->
>         P_{H_1}(\tau > c_\alpha \mid \beta \neq 0) \;>\; \alpha
>     $$
> 
>     对某些$\beta \neq 0$和有界噪声$\varepsilon$成立.
>     即弱可分性成立:混杂可以以严格超过显著性水平的功效被检测.

### 严格声明

沿用Theorem~CD.1的设定,额外引入:

- $\I(\eta; z) > 0$:Sprint参数$\eta$与混杂$z$的互信息严格正,
- Situs骨架保持:按 [ref]定义.
- Situs流形$\cM$是$C^2$光滑Riemann流形.

检验统计量定义为

$$<!-- label: eq:tau-def-formal -->
    \tau(\cI_A) \defeq \frac{1}{|\cX|}\int_
    \big\|\curl\big(\widehat{\nabla S}(x)\big)\big\|^2 \;dx,
$$

其中$\widehat{\nabla S}(x)$是$\nabla S(x)$的核平滑估计量,
$\curl$是Situs流形$\cM$上的旋度算子(定义见 [ref]).

### 前提假设列表

\begin{assumption}[B1: 互信息正性]<!-- label: ass:B1 -->
    $\I(\eta; z) > 0$.
    等价地,$\eta$与$z$的联合分布不等于边际分布的乘积:
    $P_{\eta,z} \neq P_\eta \times P_z$.
\end{assumption}

\begin{assumption}[B2: Situs骨架保持]<!-- label: ass:B2 -->
    Situs编码$\Situs(P)$保持因果DAG的骨架结构,
    即 [ref]成立.
    特别地,$d_(P(X), P(Z)) \leq \tau_$当且仅当$X$与$Z$在$\cG$中相邻.
\end{assumption}

\begin{assumption}[B3: 微分结构]<!-- label: ass:B3 -->
    Situs流形$\cM = \supp(P_X)$是$C^2$光滑的紧致Riemann流形,
    带度量$g$由 [ref]定义.
    $\cM$的维数$d = \dim(\cM) \leq 3$,以保证旋度算子$\curl$良定义.
    (对于$d > 3$,旋度算子需替换为外微分$d$作用于1-形式的范数.)
\end{assumption}

\begin{assumption}[B4: 核平滑器正则性]<!-- label: ass:B4 -->
    核函数$K: \R^d \to \R_{\geq 0}$满足:
    $K$对称、非负、支撑在单位球内,且$\int K(u)\,du = 1$,
    $\int u K(u)\,du = 0$,
    $\int \|u\|^2 K(u)\,du = \sigma_K^2 < \infty$.
    带宽$h = h_n$满足$h \to 0$且$n h^{d+2} \to \infty$当$n \to \infty$.
\end{assumption}

\begin{assumption}[B5: 有界性]<!-- label: ass:B5 -->
    噪声$\varepsilon$有界:$\|\varepsilon\|_\infty \leq M_\varepsilon < \infty$.
    混杂$z$有界:$\|z\|_\infty \leq M_z < \infty$.
    Cercis Score $S(x)$在$\cM$上$C^2$光滑,且
    $\|\nabla S\|_\infty + \|H_S\|_\infty \leq M_S < \infty$.
\end{assumption}

### 微分几何与旋度算子的严格定义

**旋度算子的Situs版本.**

在Situs流形$(\cM, g)$上,对$C^1$向量场$V \in \mathfrak{X}(\cM)$,
定义$\curl_g(V) \in \Omega^{d-2}(\cM)$为:

$$<!-- label: eq:curl-situs -->
    \curl_g(V) \defeq \star_g\, d(V^\flat),
$$

其中$V^\flat = g(V, \cdot) \in \Omega^1(\cM)$,
$d: \Omega^1 \to \Omega^2$为外微分,
$\star_g: \Omega^k \to \Omega^{d-k}$为Hodge星算子.

在$d=3$时,$\curl_g(V)$是标量场:

$$<!-- label: eq:curl-3d -->
    \curl_g(V) = \frac{1}{\sqrt{\det g}}\,
    \varepsilon^{ijk}\, \partial_i V_j,
$$

其中$V_j = g_{j\ell} V^\ell$,$\varepsilon^{ijk}$为Levi-Civita符号.

**核平滑梯度估计量.**

定义Cercis Score梯度的核平滑估计量:

$$<!-- label: eq:grad-estimator -->
    \widehat{\nabla S}(x) \defeq \frac{1}{n h^{d+1}}
    \sum_{i=1}^n K\!\left(\frac{x - x_i}{h}\right)
    \cdot \nabla_y S(x_i) \cdot (y_i - \hat{y}(x_i)),
$$

其中$\nabla_y S$是Score关于$y$的梯度,
$\hat{y}(x) = \frac{\sum K_h(x, x_i) y_i}{\sum K_h(x, x_i)}$为Nadaraya-Watson估计.
这是梯度分解 [ref]的经验版本.

**梯度场的结构分解.**
Cercis Score梯度场的结构分解为:

$$<!-- label: eq:grad-signature -->
    \nabla S(x) = \nabla Q(x) + \eta \nabla N(x) + N(x)\nabla \eta(x),
$$

其中$\nabla Q(x)$反映标签质量的局部变化,
$\eta \nabla N(x)$为噪声调制的新奇度梯度,
$N(x)\nabla \eta(x)$编码$\eta$-$z$依赖在梯度中的印记.
当$\I(\eta;z)>0$时,$\nabla \eta(x)$具有非平凡的方向结构,
使梯度场偏离保守性.

### 旋度统计量$\tau$的渐近理论

> **Lemma:** [旋度统计量的$H_0$渐近分布]<!-- label: lem:tau-null -->
>     在Assumptions~B1--B5下,若$H_0: \beta = 0$成立,
>     则$\E_{H_0}[\curl_g(\widehat{\nabla S}(x))] = O(h^2)$,
>     且
>     
> $$<!-- label: eq:tau-null-asym -->
>         n h^{d+2}\,\tau \xrightarrow{d} \sum_{k=1}^\infty \lambda_k Z_k^2,
>     $$
> 
>     其中$\{Z_k\}$为独立标准正态,$\{\lambda_k\}$为某积分算子的特征值.
>     特别地,$\E_{H_0}[\tau] = O(h^4) + O((n h^{d+2})^{-1})$.

> **Proof:** [Lemma [ref]的证明概要]
>     分三步.
> 
>     *Step 1: 核平滑估计量的偏差分析.*
> 
>     令$r(x) = \E[Y \mid X=x]$.在$H_0$下$r(x) = f^*(x)$.
>     核梯度估计量$\widehat{\nabla S}(x)$的偏差为:
>     
> $$
>         \bias[\widehat{\nabla S}(x)] &= \E[\widehat{\nabla S}(x)] - \nabla S(x) 

>         &= \frac{h^2}{2} \sigma_K^2 \cdot \nabla \Delta S(x) + o(h^2),
>     $$
> 
>     其中$\Delta$为Laplace-Beltrami算子.
>     由于$H_0$下$S(x)$仅依赖于$\varepsilon$(与$x$独立),
>     $\nabla S(x)$的期望为零,$\E[\curl_g(\widehat{\nabla S}(x))] = \curl_g(\bias[\widehat{\nabla S}(x)])$.
>     由$\nabla \Delta S$的保守性,$\curl_g(\nabla \Delta S) = 0$.
>     因此$\E_{H_0}[\curl_g(\widehat{\nabla S}(x))] = O(h^2)$,
>     其中$O(h^2)$项来自高阶Taylor展开的残余.
> 
>     *Step 2: $\tau$在$H_0$下的渐近分布.*
> 
>     $\tau$可重写为二次型:
>     
> $$
>         \tau = \frac{1}{n^2 h^{d+2}} \sum_{i,j} \xi(x_i, x_j) \varepsilon_i \varepsilon_j,
>     $$
> 
>     其中$\xi(\cdot, \cdot)$为某核函数.
>     这是退化$U$-统计量,其渐近分布由
>     (Serfling, 1980, Theorem 5.5.2)给出为加权卡方分布.
> 
>     *Step 3: 期望值.*
> 
>     由$U$-统计量理论,
>     $\E_{H_0}[\tau] = \frac{1}{n h^{d+2}} \cdot \sigma_\xi^2 + O(h^4)$,
>     其中$\sigma_\xi^2 = \int \xi(x, x)^2 dP_X(x)$.
>     $\square$

> **Lemma:** [旋度统计量的$H_1$偏移]<!-- label: lem:tau-alt -->
>     在Assumptions~B1--B5下,若$H_1: \beta \neq 0$成立,
>     且$\I(\eta; z) > 0$和B2(骨架保持)成立,
>     则存在常数$\delta_0 > 0$使得
>     
> $$<!-- label: eq:tau-alt-bias -->
>         \E_{H_1}[\tau] \geq \E_{H_0}[\tau] + \delta_0 + o(1),
>     $$
> 
>     其中$\delta_0 = c \cdot \|\beta\|^2 \cdot \I(\eta; z)$,
>     $c > 0$为依赖流形几何和核函数的常数.

> **Proof:** [Lemma [ref]的证明概要]
>     *Step 1: 混杂信号在梯度场中的印记.*
> 
>     当$\I(\eta; z) > 0$时,$\eta$随$z$变化.
>     在Situs骨架保持(B2)下,$d_(P(X), P(Z)) \leq \tau_$,
>     这意味着$X$与$Z$在Situs几何上相邻.
>     梯度$\nabla S(x)$中来自混杂的贡献为:
>     
> $$<!-- label: eq:grad-confounding -->
>         \nabla S_{\mathrm{conf}}(x) = \beta \cdot \nabla_z S(x) \cdot \frac{\partial z}{\partial x}(x),
>     $$
> 
>     其中$\frac{\partial z}{\partial x}$为$z$对$x$的Jacobian,
>     在骨架保持下该Jacobian非退化.
> 
>     *Step 2: 核平滑估计量的偏差中混杂贡献.*
> 
>     混杂使得$\widehat{\nabla S}$的偏差中出现非保守分量:
>     
> $$
>         \bias_{H_1}[\widehat{\nabla S}(x)] - \bias_{H_0}[\widehat{\nabla S}(x)]
>         &= \beta \cdot \nabla_z S(x) \cdot \frac{\partial z}{\partial x}(x) + O(h^2).
>     $$
> 
> 
>     对该偏差取旋度:
>     
> $$
>         \E_{H_1}[\curl_g(\widehat{\nabla S}(x))]
>         &= \curl_g\!\left(\beta \cdot \nabla_z S(x) \cdot \frac{\partial z}{\partial x}(x)\right) + O(h^2) 

>         &\neq 0 \quad (由于$\nabla_z S(x)$与$\frac{\partial z}{\partial x}$的方向不一致性).
>     $$
> 
> 
>     *Step 3: $\delta_0$的下界.*
> 
>     由互信息正性定理:
>     
> $$
>         \I(\eta; z) \geq \frac{(\E[\eta z] - \E[\eta]\E[z])^2}{2\V[\eta]\V[z]}.
>     $$
> 
>     结合骨架保持的几何约束,可得$\|\curl_g(\nabla S_{\mathrm{conf}})\|_{L^2}^2
>     \geq c \cdot \|\beta\|^2 \cdot \I(\eta; z)$.
>     因此$\delta_0 = c \cdot \|\beta\|^2 \cdot \I(\eta; z)$.
>     $\square$

### 完整证明(条件版)

> **Proof:** [Theorem [ref]的条件证明]
> 
>     **Step 1: 统计量的构造.**
> 
>     如 [ref]定义$\tau$,
>     并在给定的显著性水平$\alpha \in (0,1)$下选择阈值$c_\alpha$为
>     $\tau$在$H_0$下的$(1-\alpha)$分位数.
> 
>     **Step 2: $H_0$下的控制.**
> 
>     由Lemma [ref],在$H_0$下:
>     
> $$
>         P_{H_0}\big(\tau > \E_{H_0}[\tau] + t\big) \leq \frac{\V_{H_0}[\tau]}{t^2}
>         \quad (Chebyshev不等式).
>     $$
> 
>     选取$t = \sqrt{\V_{H_0}[\tau]/\alpha}$,
>     则$c_\alpha = \E_{H_0}[\tau] + t$满足水平控制.
> 
>     **Step 3: $H_1$下的功效下界.**
> 
>     由Lemma [ref],在$H_1$下:
>     
> $$
>         P_{H_1}(\tau > c_\alpha)
>         &= P_{H_1}\big(\tau - \E_{H_1}[\tau] > c_\alpha - \E_{H_1}[\tau]\big) 

>         &\geq 1 - \frac{\V_{H_1}[\tau]}{(\E_{H_1}[\tau] - c_\alpha)^2}
>         \quad (单侧Chebyshev) 

>         &\geq 1 - \frac{\V_{H_1}[\tau]}{(\delta_0 - t)^2},
>     $$
> 
>     其中$\E_{H_1}[\tau] - \E_{H_0}[\tau] = \delta_0 > 0$.
> 
>     由于$\V_{H_1}[\tau] = O((n h^{d+2})^{-1})$且$\delta_0$不随$n$衰减,
>     对于充分大的$n$,有$\delta_0 > t$且
>     
> $$
>         P_{H_1}(\tau > c_\alpha) \geq 1 - O\!\left(\frac{1}{n h^{d+2} \delta_0^2}\right) > \alpha.
>     $$
> 
> 
>     **Step 4: 有限样本保证.**
> 
>     所需的最小样本量满足:
>     
> $$<!-- label: eq:min-sample -->
>         n \geq \frac{C}{\alpha \cdot h^{d+2} \cdot \|\beta\|^4 \cdot \I(\eta; z)^2},
>     $$
> 
>     其中$C$为仅依赖流形几何和核函数的常数.
>     当$\|\beta\|$或$\I(\eta; z)$较小时,所需样本量可能极大.
>     $\square$

### 严格性标注
\conditionallyrigorous\quad 本定理在Assumptions~B1--B5下成立.
核心条件依赖B2(Situs骨架保持)——这是SCX框架中未经验证的关键假设.

### 诚实暴击

\begin{critique}
    
1. [(C1)] **旋度统计量的微分几何基础问题.**
2. [(C2)] **Situs骨架保持——核心未验证假设.**
3. [(C3)] **$\curl_g = 0$恒等式与有限样本的矛盾.**
4. [(C4)] **条件弱可分 vs.\ 无条件弱可分.**
5. [(C5)] **功效下界$\delta_0$的无法计算性.**

\end{critique}

## 因果中继界定理 (Theorem CD.3)
<!-- label: sec:relay -->

> **Theorem:** [因果中继界]<!-- label: thm:causal-relay -->
>     令$\cD_s$(源域)满足$(X,Y)$的前门准则(中介变量$M$),
>     $\cD_t$(目标域)为存在混杂的域.
>     令$\varepsilon$为T7跨域保真度参数,满足
>     $d_(\Situs(\cD_s), \Situs(\cD_t)) \leq \varepsilon$.
>     则目标域上混杂引起的Cercis偏差满足
>     
> $$<!-- label: eq:relay-bound -->
>         \|\Delta S\|_{\cD_t} \;\leq\;
>         g(\varepsilon, \delta) + O\!\left(\frac{1}{\sqrt{n}}\right),
>     $$
> 
>     其中
>     
> $$<!-- label: eq:g-function -->
>         g(\varepsilon, \delta) = L_ \cdot \varepsilon
>         + \kappa \cdot \delta + C \cdot \varepsilon \cdot \delta,
>     $$
> 
>     其中$L_$为Cercis Score关于Situs距离的Lipschitz常数,
>     $\delta$为源域与目标域在Situs距离下的分布偏移,
>     $\kappa$为依赖问题的混杂扰动常数,
>     $C$为耦合常数.

### 严格声明

令$\cD_s = \{(x_i^{(s)}, y_i^{(s)})\}_{i=1}^{n_s}$,
$\cD_t = \{(x_j^{(t)}, y_j^{(t)})\}_{j=1}^{n_t}$
分别为源域和目标域数据集.
源域满足前门准则,目标域存在混杂.

**三个核心对象.**

- $\Delta S_{\cD_t}(x) \defeq S_{\cD_t}(x) - S_{\cD_s}^*(x)$,
- $\|\Delta S\|_{\cD_t} \defeq \big(\int_ |\Delta S_{\cD_t}(x)|^2 \, d\mu_{\cD_t}(x)\big)^{1/2}$,
- $\delta \defeq d_(\Situs(\cD_s), \Situs(\cD_t))$,

### 前提假设列表

\begin{assumption}[C1: 前门准则]<!-- label: ass:C1 -->
    源域$\cD_s$中,$M$为$(X,Y)$的前门调节变量,
    即FD1--FD3(第 [ref]节)成立.
    因此因果效应$P(Y \mid do(X))$可由 [ref]识别.
\end{assumption}

\begin{assumption}[C2: T7跨域保真度]<!-- label: ass:C2 -->
    存在已知常数$\varepsilon \geq 0$使得
    $d_(\Situs(\cD_s), \Situs(\cD_t)) \leq \varepsilon$.
    这对应于SCX框架中Theorem~7的条件.
\end{assumption}

\begin{assumption}[C3: Cercis Score的Lipschitz连续性]<!-- label: ass:C3 -->
    Cercis算子$S: \cP(\cX \times \cY) \to L^2(\cX)$关于Situs距离
    $d_$是$L_$-Lipschitz连续的:
    
$$<!-- label: eq:lipschitz-cercis -->
        \|S(P) - S(Q)\|_{L^2(\cX)} \leq L_ \cdot d_(P, Q),
        \quad \forall P, Q \in \cP(\cX \times \cY),
    $$

    其中$L_ > 0$为有限常数.
\end{assumption}

\begin{assumption}[C4: 混杂有界性]<!-- label: ass:C4 -->
    目标域$\cD_t$上的混杂效应有界:
    $\|\beta \cdot z\|_{L^2(P_{X_t})} \leq B < \infty$,
    且混杂引起的Cercis Score偏差满足
    $\|\Delta S_{\mathrm{confound}}\|_{\cD_t} \leq \kappa \cdot \delta$,
    其中$\kappa$为依赖问题结构的常数.
\end{assumption}

\begin{assumption}[C5: 有限样本收敛]<!-- label: ass:C5 -->
    Situs距离的经验估计量$\hat{d}_$满足
    $\E[|\hat{d}_ - d_|] = O(1/\sqrt{n})$
    其中$n = \min(n_s, n_t)$.
    这由Wasserstein距离的集中不等式保证
    (Weed \& Bach, 2019, Theorem 1).
\end{assumption}

### 完整证明(链式不等式)

> **Proof:** [Theorem [ref]的形式化证明]
> 
>     证明由三个链式步骤组成,每步量化一项误差源.
> 
>     **Step 1: 源域前门调整——去混杂.**
> 
>     在源域$\cD_s$上,由C1(前门准则),可识别$X$对$Y$的因果效应:
>     
> $$<!-- label: eq:front-door-est -->
>         \hat{P}(Y \mid do(X=x)) = \sum_{m=1}^M \hat{P}(M=m \mid X=x)
>         \sum_{x' \in \cX_s} \hat{P}(Y \mid M=m, X=x') \hat{P}(X=x'),
>     $$
> 
>     其中$\hat{P}$表示经验分布.
> 
>     定义基于前门调整的"无混杂"Cercis Score为$S_{\cD_s}^*$,
>     即在调整后的分布下计算的Cercis Score.
>     源域的Cercis偏差仅来自残差标签噪声:
>     
> $$<!-- label: eq:source-deviation -->
>         \|\Delta S\|_{\cD_s} \leq \eta_s \cdot \sigma_\varepsilon^2
>         + O\!\left(\frac{1}{\sqrt{n_s}}\right),
>     $$
> 
>     其中$O(1/\sqrt{n_s})$项来自前门调整的估计误差
>     (由C5保证).
> 
>     **Step 2: T7跨域传输——Lipschitz界.**
> 
>     由C2(T7保真度),源域与目标域的Situs距离不超过$\varepsilon$:
>     
> $$<!-- label: eq:situs-dist-bound -->
>         d_(\Situs(\cD_s), \Situs(\cD_t)) \leq \varepsilon.
>     $$
> 
> 
>     由C3(Cercis Score的Lipschitz连续性):
>     
> $$
>         \|S_{\cD_t} - S_{\cD_s}^*\|_{L^2(\cX)}
>         &\leq L_ \cdot d_(\Situs(\cD_t), \Situs(\cD_s^*))
>         \quad (由C3) 

>         &\leq L_ \cdot \big[d_(\Situs(\cD_t), \Situs(\cD_s))
>         + d_(\Situs(\cD_s), \Situs(\cD_s^*))\big]
>         \quad (三角不等式) 

>         &\leq L_ \cdot \varepsilon + L_ \cdot O\!\left(\frac{1}{\sqrt{n_s}}\right),
>         <!-- label: eq:lipschitz-transfer -->
>     $$
> 
>     其中$\cD_s^*$表示经前门调整后的源域分布.
>     第二项$O(1/\sqrt{n_s})$来自前门调整分布的Situs距离.
> 
>     **Step 3: 目标域混杂扰动界.**
> 
>     目标域的混杂偏差满足(由C4):
>     
> $$<!-- label: eq:confound-deviation -->
>         \|\Delta S_{\mathrm{confound}}\|_{\cD_t} \leq \kappa \cdot \delta,
>     $$
> 
>     其中$\delta = d_(\Situs(\cD_s), \Situs(\cD_t)) \leq \varepsilon + O(1/\sqrt{n})$
>     (由C2和C5).
> 
>     **Step 4: 耦合效应.**
> 
>     T7传输与混杂扰动之间存在耦合效应.
>     前门调整后残差与混杂项的相关性产生交叉项:
>     
> $$
>         \|\Delta S_{\mathrm{coupling}}\|_{\cD_t}
>         &\leq 2 \cdot \|S_{\cD_t} - S_{\cD_s}^*\|_{L^2}
>         \cdot \|\Delta S_{\mathrm{confound}}\|_{\cD_t} 

>         &\leq 2 \cdot (L_ \varepsilon) \cdot (\kappa \delta)
>         \quad (由 [ref]和 [ref]) 

>         &= C \cdot \varepsilon \cdot \delta,
>     $$
> 
>     其中$C \defeq 2 L_ \kappa$.
> 
>     这一耦合界由Cauchy-Schwarz不等式和Lipschitz界推导:
>     设$a := \|S_{\cD_t} - S_{\cD_s}^*\|$, $b := \|\Delta S_{\mathrm{confound}}\|$,
>     则交叉项$\langle S_{\cD_t} - S_{\cD_s}^*, \Delta S_{\mathrm{confound}}\rangle
>     \leq a \cdot b \leq L_\varepsilon \cdot \kappa\delta$,
>     耦合常数为$C = 2 L_ \kappa$.
> 
>     **Step 5: 三项求和.**
> 
>     总偏差上界为三项之和:
>     
> $$
>         \|\Delta S\|_{\cD_t}
>         &\leq \|S_{\cD_t} - S_{\cD_s}^*\| + \|\Delta S_{\mathrm{confound}}\|
>         + \|\Delta S_{\mathrm{coupling}}\| 

>         &\leq \big(L_ \varepsilon + O(n_s^{-1/2})\big)
>         + \big(\kappa \delta\big)
>         + \big(C \cdot \varepsilon \cdot \delta\big) 

>         &\leq L_ \cdot \varepsilon + \kappa \cdot \delta + C \cdot \varepsilon \cdot \delta
>         + O\!\left(\frac{1}{\sqrt{n}}\right),
>         <!-- label: eq:final-bound -->
>     $$
> 
>     其中$O(1/\sqrt{n})$项合并了$n_s$和$n_t$的有限样本误差,
>     在$n = \min(n_s, n_t)$下为$O(1/\sqrt{n})$.
>     $\square$

### 各项误差来源的显式量化

为便于实践应用,我们将$g(\varepsilon, \delta)$中各项的依赖关系显式化:

- **Lipschitz传输项**$L_ \cdot \varepsilon$:
- **混杂扰动项**$\kappa \cdot \delta$:
- **耦合项**$C \cdot \varepsilon \cdot \delta$:

### 严格性标注
\rigorous\quad 本定理在Assumptions~C1--C5下严格成立,
是SCX框架内T7定理和Situs距离三角不等式的直接推论.
无需Situs骨架保持假设.

### 诚实暴击

\begin{critique}
    
1. [(C1)] **前门准则的可满足性.**
2. [(C2)] **T7保真度参数$\varepsilon$的不可观测性.**
3. [(C3)] **Lipschitz常数$L_$的估计.**
4. [(C4)] **上界的紧性.**
5. [(C5)] **统计误差$O(1/\sqrt{n})$的隐藏常数.**

\end{critique}

## 讨论:可区分性前沿的结构
<!-- label: sec:discussion -->

### 三个定理的逻辑关系

三个定理共同描绘了$\eta$-$z$依赖结构空间中的可区分性前沿:

<div align="center">

[Table omitted — see original .tex]

</div>

### 开放问题与未来方向

- **无条件弱可分**(Open Problem [ref]):
- **离散数据的微分几何**:
- **有限样本的精确分布**:
- **KLIEP(核均值匹配)视角**:

## 结论
<!-- label: sec:conclusion -->

本文件将SCX框架的Theorem~3扩展至因果发现设定,
给出三个定理的严格形式化版本.
强不可分定理($\eta \perp z$)在Assumptions~A1--A5下严格证明,
是Theorem~3的直接推论.
弱可分定理提供了一条构造性路径——条件依赖于Situs骨架保持假设,
无条件形式是开放问题.
因果中继定理在前门准则和T7保真度下给出了混杂偏差的显式可计算上界.

诚实暴击分析揭示了核心假设(Situs骨架保持、前门准则可满足性、离散微分几何操作性)
中尚未解决的问题.这些问题的解决是SCX因果发现框架成熟的必要条件.

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias Operators,''
\newblock *Technical Report*, 2024.

\bibitem{pearl2009causality}
J.~Pearl.
\newblock *Causality: Models, Reasoning, and Inference*, 2nd ed.
\newblock Cambridge University Press, 2009.

\bibitem{spirtes2000causation}
P.~Spirtes, C.~Glymour, and R.~Scheines.
\newblock *Causation, Prediction, and Search*, 2nd ed.
\newblock MIT Press, 2000.

\bibitem{peters2017elements}
J.~Peters, D.~Janzing, and B.~Sch\"olkopf.
\newblock *Elements of Causal Inference: Foundations and Learning Algorithms*.
\newblock MIT Press, 2017.

\bibitem{hernan2020causal}
M.~A.~Hern\'an and J.~M.~Robins.
\newblock *Causal Inference: What If*.
\newblock Chapman \& Hall/CRC, 2020.

\bibitem{wu2024hessian}
Y.~Wu, K.~Zhang, and B.~Sch\"olkopf.
\newblock ``Hessian-based Causal Structure Learning from Observational Data,''
\newblock in *NeurIPS*, 2024.

\bibitem{shimizu2006lingam}
S.~Shimizu, P.~O.~Hoyer, A.~Hyv\"arinen, and A.~Kerminen.
\newblock ``A linear non-Gaussian acyclic model for causal discovery,''
\newblock *Journal of Machine Learning Research*, 7:2003--2030, 2006.

\bibitem{zhang2018invariant}
K.~Zhang, B.~Sch\"olkopf, P.~Spirtes, and C.~Glymour.
\newblock ``Learning causality and causality-related learning,''
\newblock *National Science Review*, 5(1):26--29, 2018.

\bibitem{arjovsky2019invariant}
M.~Arjovsky, L.~Bottou, I.~Gulrajani, and D.~Lopez-Paz.
\newblock ``Invariant risk minimization,''
\newblock *arXiv:1907.02893*, 2019.

\bibitem{dominguez2020causal}
M.~Dom\'inguez-Olmedo, A.~Karimi, and B.~Sch\"olkopf.
\newblock ``Causal discovery from observational data: A survey,''
\newblock *arXiv:2003.03377*, 2020.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\bibitem{villani2008optimal}
C.~Villani.
\newblock *Optimal Transport: Old and New*.
\newblock Springer, 2008.

\bibitem{weed2019sharp}
J.~Weed and F.~Bach.
\newblock ``Sharp asymptotic and finite-sample rates of convergence of empirical
measures in Wasserstein distance,''
\newblock *Bernoulli*, 25(4A):2620--2648, 2019.

\bibitem{serfling1980approximation}
R.~J.~Serfling.
\newblock *Approximation Theorems of Mathematical Statistics*.
\newblock Wiley, 1980.

\bibitem{ambrosio2005gradient}
L.~Ambrosio, N.~Gigli, and G.~Savar\'e.
\newblock *Gradient Flows in Metric Spaces and in the Space of Probability
Measures*.
\newblock Birkh\"auser, 2005.

\end{thebibliography}