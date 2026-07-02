# Situs (Physical Positional Encoding)
物理真实性验证与适用场景分析

**Author:** SCX

**文档状态**: 诚实暴击 --- 不委婉

**前置阅读**:
`ppe\_rigorous\_derivation.md`（严密数学推导），`multi\_head\_spring\_and\_positional\_encoding\_analysis.md`（CC
审计报告）

**方法论**: 真实物理数据 + 数学定理的物理对应 + 逐一场景论证

**核心判据**: 定理 2.2.1 ---
\(\delta_s^{PE} > 0 \iff I(Y; P \mid S) > 0\)，即物理位置在给定状态原子条件下必须携带关于标签的额外信息

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

## 第 1
部分：物理真实性检查<!-- label: ux7b2c-1-ux90e8ux5206ux7269ux7406ux771fux5b9eux6027ux68c0ux67e5 -->

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1.1
蛋白质序列位置编码<!-- label: ux86cbux767dux8d28ux5e8fux5217ux4f4dux7f6eux7f16ux7801 -->

#### 1.1.1 相同氨基酸，不同位置：Lys-37（活性位点）vs
Lys-289（表面
loop）<!-- label: ux76f8ux540cux6c28ux57faux9178ux4e0dux540cux4f4dux7f6elys-37ux6d3bux6027ux4f4dux70b9vs-lys-289ux8868ux9762-loop -->

**生物学事实（无可争议）**：

同一个赖氨酸残基在蛋白质不同位置具有完全不同的功能角色： -
**活性位点 Lys-37**：典型催化残基，侧链 pKa 可偏离溶液值 2--4
个单位（从 ~10.5 降至
6.0--8.0），参与酸碱催化或共价催化。例如：acetoacetate decarboxylase 中
Lys-115 的 pKa ≈ 6.0 {[}Bartlett et al., *J. Mol. Biol.* 324, 105
(2002){]}；ribonuclease A 中 Lys-41 的 pKa ≈ 8.8 {[}Raines, *Chem.
Rev.* 98, 1045 (1998){]}。高度保守，对突变极度敏感（ΔΔG \textgreater{} 3
kcal/mol 常见）。 - **表面 loop Lys-289**：溶剂暴露，pKa
接近溶液值（10.4--10.6），功能上多参与非特异性静电相互作用或蛋白质-蛋白质识别界面，保守性低，对突变容忍度高（ΔΔG
通常 \textless{} 1 kcal/mol）。

**物理判断**：

\[I(Y; P \mid S) > 0 \quad ——在给定"氨基酸类型 = Lys"的条件下，残基位置携带大量功能信息\]

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1311}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3443}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3607}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1639}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
物理量
\end{minipage} & \begin{minipage}[b]
Lys-37（活性位点）
\end{minipage} & \begin{minipage}[b]
Lys-289（表面 loop）
\end{minipage} & \begin{minipage}[b]
差异来源
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
侧链 pKa & 6.0--8.0 & 10.4--10.6 & 局部静电环境（Buried vs 溶剂暴露） 

SASA (溶剂可及表面积) & \textless{} 10 Å² & \textgreater{} 100 Å² & 3D
折叠位置 

进化保守性（BLOSUM62 位置熵） & \textless{} 0.2 bits & \textgreater{}
0.8 bits & 功能约束强度 

突变 ΔΔG & \textgreater{} 3 kcal/mol & \textless{} 1 kcal/mol &
折叠稳定性贡献 

\end{longtable}

**BUT------关键限制**：

Situs 的正弦编码编码的是**序列位置**（1D 残基编号 37 vs
289），而非**3D 空间位置**（活性位点口袋 vs 表面）。这是 Situs
在蛋白质应用中的根本缺陷：

- 
- 
- 

**诚实结论**：1D 序列正弦编码对区分 Lys-37 活性位点 vs Lys-289 表面
loop **有信息但信号弱**。序列位置与 3D 功能位置的相关性受限于 fold
保守性。\(I(Y; P_{1D} \mid S) > 0\) 但远小于
\(I(Y; P_{3D} \mid S)\)。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### 1.1.2 α-螺旋的 3.6
残基/圈周期性<!-- label: ux3b1-ux87baux65cbux7684-3.6-ux6b8bux57faux5708ux5468ux671fux6027 -->

**物理事实**：

Pauling 经典 α-螺旋 {[}Pauling et al., *PNAS* 37, 205 (1951){]}： -
每圈 3.6 个残基（精确值 = 3.6，或 18 残基/5 圈） - 螺距 = 5.4
Å（每残基上升 1.5 Å） - 氢键模式：残基 \(i\) 的 C=O ··· H--N 残基
\(i+4\) - 这意味着残基 \(i\) 和 \(i+4\) 在空间上相邻（~3.1
Å），而 \(i\) 和 \(i+3\)（或 \(i+5\)）在螺旋的相对面

**正弦编码能否捕获？**

对于正弦编码 \(\sin(2\pi p / \lambda_j)\)： - 若波长
\(\lambda_j = 3.6\)：\(\sin(2\pi p/3.6)\) 确实具有 3.6 残基的精确周期 -
残基 \(i\) 和 \(i+3.6\) 获得相同编码值 → 残基 \(i\) 和 \(i+4\)（距离
4，周期差 0.4/3.6 ≈ 11\%）编码相近但不相同

**但是------标准 Transformer 编码做不到**：

标准正弦编码 {[}Vaswani et al., *NeurIPS* 2017{]} 的波长集合：
\[\lambda_j = 2\pi \cdot 10000^{2j/d}\]

当 \(d = 512\) 时，波长范围约为 \(2\pi\) 到 \(2\pi \cdot 10000\)（≈ 6.28
到 ≈ 62832）。对于典型的蛋白质长度 \(L \sim 300\)： -
最短波长（\(j = d/2-1 = 255\)）：\(\lambda_{255} = 2\pi \cdot 10000^{510/512} \approx 2\pi \cdot 10000^{0.996} \approx 6.28 \times 9550 \approx 60,000\)
------远大于 3.6！ - 没有任何一个 \(\lambda_j\) 接近 3.6

**物理最优谱（定理 1.2.1）能否解决？**

根据定理 1.2.1，最优频率谱需要知道物理相关长度 \(\xi\)。对于
α-螺旋，\(\xi \approx 3.6\)（螺旋周期）。若我们以 \(\xi = 3.6\)
为目标设计编码： -
\(\lambda_ = 2\pi\xi \cdot \cot(\pi(2(d/2-1)+1)/2d) \approx 2\pi \cdot 3.6 \cdot \cot(\pi/2 - \pi/2d) \approx 22.6 \cdot (2d/\pi) \approx 14.4 d\)
- 对于 \(d = 64\)，\(\lambda_ \approx 920\) ------仍远大于 3.6！

**根本问题**：正弦编码的''分辨率''受限于 \(d\)。要在 \(L = 300\)
的序列上分辨出 3.6 残基的周期，需要
\(\lambda_ \lesssim 3.6\)，即需要
\(d \gtrsim 300/3.6 \times 2 = 167\) 维（每个周期至少 2
个采样点，Nyquist）。对于典型的 \(d = 64\) 或 \(d = 128\)，3.6
残基的周期性**理论上无法被捕获**。

**诚实结论**：对于实际使用的编码维度（\(d \leq 128\)），正弦编码**无法**可靠捕获
α-螺旋的 3.6
残基/圈周期性。这不是编码形式的缺陷，而是维度-分辨率的基本权衡（推论
1.2.1）。如果需要在序列位置编码中捕获螺旋周期性，应该显式添加一个
\(\lambda \approx 3.6\) 的频率分量，或者使用可学习的周期性特征。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### 1.1.3 固有无序区域（IDR）中 Situs
的退化<!-- label: ux56faux6709ux65e0ux5e8fux533aux57dfidrux4e2d-situs-ux7684ux9000ux5316 -->

**物理事实**：

固有无序区域（IDR）占真核蛋白质组的 30--40\% {[}Dunker et al.,
*FEBS J.* 272, 5129 (2005){]}。关键特征： -
在生理条件下**不折叠为单一稳定 3D 结构** -
功能来自**氨基酸组成**（如电荷模式、脯氨酸含量）而非精确折叠 -
序列位置与功能的关系**极弱**：IDR 的功能（如 linker、entropic
spring、PTM 位点集群）主要由组成决定，位置排列有高度容忍度 - 同一 IDR
插入/删除 5--20 个残基通常不影响功能 {[}Zibaee et al., *Protein
Sci.* 16, 906 (2007){]}

**Situs 在 IDR 上的行为**：

\[I(Y; P_{seq} \mid S = "IDR residue") \approx 0\]

由定理 2.2.1 和 2.3.1：
\[\delta_s^{PE} \leq \sqrt{\frac{1}{2} I(Y; P \mid S)} + \delta_s^{variance} \approx 0 + O(1/\sqrt{M})\]

即：**Situs 退化为维度为 \(d\) 的加法噪声**。

具体地，在 IDR 区域的 \(L\) 个连续位置上：
\[PE(p) = [\sin(2\pi p/\lambda_1), \cos(2\pi p/\lambda_1), ...]\]

这些编码向量随 \(p\) 平滑变化（Lipschitz
连续性），但它们携带的变异性与标签 \(Y\) **无关**。在训练中： -
干净样本：\(PE(p)\) 添加了与标签无关的波动 →
可能略微降低专家一致性 →
\(p_{clean}^{PPE} \geq p_{clean}\) -
噪声样本：\(PE(p)\) 同样不提供区分噪声的能力 →
\(p_{noisy}^{PPE} \approx p_{noisy}\) -
结果：\(\delta_s^{PE} \leq 0\)（负或零）

**诚实结论**：IDR 是 Situs
的**最坏场景**------位置编码退化为无害但无用的维度膨胀。它不会主动破坏模型（Lipschitz
连续性保证 \(h_i\) 仍然光滑），但消耗了 \(d\)
维的计算和存储，且可能通过梯度噪声略微降低收敛速度。如果数据集中 IDR
占比高（\textgreater30\% 如真核蛋白），Situs 的净收益**可能为负**。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1.2 材料 3D
结构位置编码<!-- label: ux6750ux6599-3d-ux7ed3ux6784ux4f4dux7f6eux7f16ux7801 -->

#### 1.2.1 V\_N 空位形成能：晶界 vs 体相 vs
表面<!-- label: v_n-ux7a7aux4f4dux5f62ux6210ux80fdux6676ux754c-vs-ux4f53ux76f8-vs-ux8868ux9762 -->

**物理事实（DFT 计算数据）**：

AlN 中氮空位 \(V_N\) 的形成能强烈依赖于空间位置 {[}Freysoldt et al.,
*Rev.~Mod. Phys.* 86, 253 (2014); Stampfl \& Van de Walle,
*Phys. Rev.~B* 65, 155212 (2002){]}：

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1714}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5429}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2857}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
位置
\end{minipage} & \begin{minipage}[b]
形成能 \(E_f\) (eV)
\end{minipage} & \begin{minipage}[b]
物理原因
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**体相**（bulk, 配位数 4） & 3.2--4.0 & 完整四面体配位，断开 4 个
Al--N 键 

**表面**（(0001) 表面, 配位数 3） & 1.8--2.5 &
表面弛豫释放应变能，配位数降低 

**晶界**（Σ7 对称倾斜晶界） & 1.0--1.8 & 晶界本征应力场 + 多余体积
+ 悬挂键预存在 

\end{longtable}

差异幅度：\(\Delta E_f \approx 1.5\)--\(2.5\) eV，远超 \(k_B T\)（室温下
≈ 0.025 eV），在**任何**温度下都具有决定性影响。

**物理因果链**（不可简化）：

\[3D 位置 \xrightarrow{决定} 局部配位环境 \xrightarrow{决定} 缺陷形成能\]

这是一个清晰的因果箭头------位置是自变量，形成能是因变量。位置编码捕获的是这个因果链的**原因侧**。

\[I(Y = E_f; P_{3D} \mid S = V_N) > 0 \quad ——信息论意义上严格正且量大\]

根据 Fano 下界（定理 2.4.1），对于多类分类（不同缺陷电荷态）：
\[\delta_s^{PE} \geq \frac{2 \cdot I(Y; P \mid S) - \log 2}{\log |\mathcal{Y}|}\]

取 \(I(Y; P \mid S) \approx H(Y|S) \approx \log 3 \approx 1.6\) bits（3
种形成能区间：高/中/低），\(\log |\mathcal{Y}| \approx \log 3\)：
\[\delta_s^{PE} \gtrsim 0.5 –0.8\]

这是一个**可观的检测边际增益**，对应 Theorem 1 的指数界显著收紧。

**诚实结论**：对于材料缺陷检测，3D Situs
是**物理上最有价值的应用场景**。位置直接因果决定标签。这是 Situs
的''home turf''。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### 1.2.2 3D
旋转编码的物理对称性检查<!-- label: d-ux65cbux8f6cux7f16ux7801ux7684ux7269ux7406ux5bf9ux79f0ux6027ux68c0ux67e5 -->

**Situs 旋转编码的定义**（定义 1.3.1）：
\[PE_{rot}(\mathbf{p}) = \mathbf{R}_x(\alpha x) \cdot \mathbf{R}_y(\beta y) \cdot \mathbf{R}_z(\gamma z) \cdot \mathbf{e}_0\]

**检查 1：平移不变性** ✓

内积：
\[\langle PE(\mathbf{p}), PE(\mathbf{q}) \rangle = \langle \mathbf{e}_0, \mathbf{R}(\mathbf{q} - \mathbf{p}) \mathbf{e}_0 \rangle = \cos(\alpha\Delta x) + \cos(\beta\Delta y) + \cos(\gamma\Delta z)\]

仅依赖于
\(\Delta\mathbf{p} = \mathbf{q} - \mathbf{p}\)。**平移不变性严格成立**。这满足晶体学的基本要求------完美晶体中，两个位置等价当且仅当它们的相对位移是晶格向量。

**检查 2：旋转等变性** ✗ **不成立**

考虑全局旋转 \(R_{phys} \in SO(3)\)
作用于坐标：\(\mathbf{p} \to R_{phys} \mathbf{p}\)。

对于 \$R\_\{phys\} = \$ 绕 z 轴旋转 90°（将 \((x, y, z)\) 变为
\((-y, x, z)\)）：
\[PE_{rot}(R_{phys}\mathbf{p}) = \mathbf{R}_x(-\alpha y) \mathbf{R}_y(\beta x) \mathbf{R}_z(\gamma z) \mathbf{e}_0\]

而
\(PE_{rot}(\mathbf{p}) = \mathbf{R}_x(\alpha x) \mathbf{R}_y(\beta y) \mathbf{R}_z(\gamma z) \mathbf{e}_0\)。

这两个编码之间**不存在**一个与 \(\mathbf{p}\) 无关的变换 \(T\) 使得
\(T \cdot PE(\mathbf{p}) = PE(R_{phys}\mathbf{p})\)。原因：编码为三个坐标轴分配了**不相交的维度对**------\((0,1)\)
对应 \(x\)，\((2,3)\) 对应 \(y\)，\((4,5)\) 对应 \(z\)。物理旋转混合了
\(x\) 和 \(y\) 分量，但编码空间中没有对应的''混合''机制。

**破坏的后果**：

在以下场景中旋转等变性的缺失是致命的： 1.
**多晶/晶界系统**：不同晶粒的取向不同，相同类型缺陷的编码因取向不同而不同
→ \(h_i\) 引入与标签无关的变异性 2.
**分子动力学轨迹**：分子整体旋转导致所有原子编码变化 →
模型可能学到''旋转状态''而非''物理状态'' 3. **表面 slab
计算**：同一表面不同切面（如 AlN (0001) vs (11̄00)）具有不同的坐标轴取向

**可以修复吗？**

理论上可以。替代方案： -
**球谐函数编码**：\(PE(\mathbf{p}) = [Y_{\ell m}(\theta, \phi)]\)，具有严格的
\(SO(3)\) 旋转等变性 - **E(3) 等变网络**：使用 Tensor Field
Networks {[}Thomas et al., *NeurIPS* 2018{]} 或 SE(3)-Transformers
{[}Fuchs et al., *NeurIPS* 2020{]}，天然具备平移+旋转等变性 -
**代价**：球谐函数编码的维度随角动量 \(L\) 增长为
\((L+1)^2\)，\(L=3\) 即需 16 维（vs 6 维的旋转编码），且 Lipschitz
行为更复杂

**诚实结论**：Situs 的 3D
旋转编码**仅具有平移不变性，不具旋转等变性**。对于大多数材料应用（需要处理任意取向的晶体），这是**严重缺陷**。但在受控场景（单晶、固定取向的
slab、取向已对齐的数据集）中，这不构成问题。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1.3 原子总数 N：32 vs 256 超胞的 DFT
精度<!-- label: ux539fux5b50ux603bux6570-n32-vs-256-ux8d85ux80deux7684-dft-ux7cbeux5ea6 -->

#### 1.3.1
系统性差异的物理起源<!-- label: ux7cfbux7edfux6027ux5deeux5f02ux7684ux7269ux7406ux8d77ux6e90 -->

**Makov-Payne 有限尺寸标度** {[}Makov \& Payne, *Phys. Rev.~B*
51, 4014 (1995){]}：

带电缺陷的形成能随超胞尺寸 \(L\) 的标度行为：
\[E_f(L) = E_f(\infty) + \frac{\alpha q^2}{2\varepsilon L} + \frac{2\pi q Q}{3\varepsilon L^3} + O(L^{-5})\]

其中 \(q\) 是缺陷电荷，\(\varepsilon\) 是介电常数，\(Q\) 是弹性四极矩。

**具体数值估计（\(V_N^{+1}\) 在 AlN
中，\(\varepsilon \approx 9\)）**：

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1538}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1231}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2308}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1692}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1231}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
超胞尺寸
\end{minipage} & \begin{minipage}[b]
原子数
\end{minipage} & \begin{minipage}[b]
周期性图像间距
\end{minipage} & \begin{minipage}[b]
\(1/L\) 修正
\end{minipage} & \begin{minipage}[b]
\(1/L^3\) 修正
\end{minipage} & \begin{minipage}[b]
总修正
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
2×2×2 & 32 & ~6.2 Å & ~0.35 eV &
~0.12 eV & **~0.5 eV** 

2×2×3 & 48 & ~6.2--9.3 Å & ~0.25 eV &
~0.05 eV & **~0.3 eV** 

3×3×3 & 108 & ~9.3 Å & ~0.15 eV &
~0.02 eV & **~0.17 eV** 

4×4×4 & 256 & ~12.4 Å & ~0.08 eV &
~0.005 eV & **~0.09 eV** 

\end{longtable}

**物理根源**（三个独立的有限尺寸效应，均不可忽略）：

1. 
2. 
3. 

**这与 Situs 的 \(N\) 编码有什么关系？**

Situs 的第三域（定义 1.1.3）将总原子数 \(N\)
作为标量位置编码入。问题是：

- 
- 
- 

**物理上正确的处理**： - 对 \(E_f\) 应用 Freysoldt-Neugebauer-Van
de Walle (FNV) 有限尺寸修正 {[}Freysoldt et al., *Phys. Rev.~Lett.*
102, 016402 (2009){]}，消除 \(N\) 的系统性偏差 -
**之后**再考虑是否使用 \(N\) 编码------此时 \(N\)
才反映真实的系统尺寸效应（如量子限域），而非计算 artifact

**诚实结论**：如果训练数据未经过有限尺寸修正，\(N\)
编码学到的是**计算 artifact 而非物理**。在修正之后，\(N\)
携带的真实物理信息（量子限域、振动模式数）对于缺陷物理来说较小（\(\Delta E_f\)
的 \(N\)-dependence \textless{} 0.05 eV for
\(N > 100\)）。对于大多数材料任务，\(N\) 编码的 \(\delta_s^{PE}\)
**接近零**------这是一个物理上动机弱、实践上危险（容易学到
artifact）的编码维度。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

## 第 2 部分：Situs
在什么情况下有害？<!-- label: ux7b2c-2-ux90e8ux5206situs-ux5728ux4ec0ux4e48ux60c5ux51b5ux4e0bux6709ux5bb3 -->

诚实暴击：Situs
不是一个''无害但可能无用''的组件。在特定条件下它是**主动有害的**。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2.1 虚假相关性（Spurious
Correlation）<!-- label: ux865aux5047ux76f8ux5173ux6027spurious-correlation -->

**机制**：

当物理位置 \(P\) 与标签 \(Y\)
在训练数据中具有统计学相关，但该相关**不反映因果关系**时：

\[Corr_{train}(P, Y) \neq 0, \quad 但  P \perp\!\!\!\perp Y （因果意义上独立）\]

由于 Situs 将 \(P\) 编码为 \(PE(P)\) 并注入表示，模型（专家
\(E_m\)）会学习利用这个虚假相关。

**具体实例**：

**蛋白质数据集偏差**： - PDB
中解析的蛋白质结构存在''易于结晶''偏差------倾向于更稳定、更紧凑的折叠 -
如果训练集中所有酶活性位点恰好在结晶结构中位于蛋白质核心（低 B-factor
区域 → 低位置索引附近被解析得更清楚） - Situs
学到：残基位置靠前（\(p < 100\)）→ 活性位点 - 测试集中出现 C
端活性位点蛋白 → 系统性误判

**DFT 计算参数偏差**： - Materials Project
中的计算使用不同的计算参数（赝势、k
点密度），且这些参数与材料类型有系统性关联 - 如果 Situs 的原子数编码
\(N\) 学到：\(N=32\)（典型金属计算）→
低形成能，\(N=256\)（典型半导体缺陷计算）→ 高形成能 -
这种''知识''是计算惯例的 artifact，不是物理

**虚假相关性的检测**：\(\delta_s^{PE}\) 在训练集上
\textgreater{} 0，但在 i.i.d. 验证集上 → 0 或 \textless{} 0。Theorem
2'（修正 Theorem 2）的上界在分布外数据上**反而更松**------因为
\(\varepsilon_{PE}\) 在训练分布上被低估。

**诚实结论**：虚假相关性是 Situs
的**最大实际风险**。物理学家知道''position matters''但训练数据中的
position-label
相关有多少来自因果、有多少来自数据收集偏差，必须逐案分析。**没有捷径**。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2.2
多重共线性（Multicollinearity）<!-- label: ux591aux91cdux5171ux7ebfux6027multicollinearity -->

**机制**：

当状态表示 \(\phi(s_i)\) **已经隐式编码了位置信息**时，加法注入
\(PE(p_i)\) 产生冗余维度：

\[h_i = \underbrace{\phi(s_i)}_{已含隐式位置信息} + \underbrace{PE(p_i)}_{显式位置信息}\]

这导致编码空间中的有效维度膨胀，伴随： 1.
**专家模型的梯度方差增大**：每个专家需要从冗余维度中提取信号 2.
**有效专家多样性 \(\rho_{eff}\)
下降**：当所有专家在同一冗余空间中操作，它们的输出相关性增大

**具体实例**：

**图神经网络 (GNN) 处理晶体**： - GNN
已通过消息传递聚合了邻域信息，包含隐式的位置/距离编码 -
如果再对每个节点添加 Situs 的 3D
旋转编码，相当于添加了**已经被图卷积层捕获的信息** -
结果：\(I(Y; PE(P) \mid \phi(S)) \approx 0\)（给定 GNN
特征后，位置无额外信息） - 但 PE 的额外维度增加了优化难度，等效于
\(\delta_s^{variance}\) 增大

**蛋白质语言模型 (pLM) 处理序列**： - ESM-2 {[}Lin et al.,
*Science* 379, 1123 (2023){]} 等 pLM 的 attention
机制天然包含位置信息（attention bias） - 对 ESM embedding 再加 Situs
正弦编码 = 添加已被 attention 处理的冗余信号 -
这种''双重编码''在统计上引入共线性，但不增加有效信息

**定量影响**：

设原始特征空间的有效秩为
\(r_{eff} = rank(\Sigma_\phi)\)。添加 PE 后：
\[rank(\Sigma_h) \leq r_{eff} + \min(d_{pe}, N)\]

但如果 \(span(PE(P)) \subseteq span(\phi(S))\)（PE
在 \(\phi\) 的列空间中），则 \(rank(\Sigma_h) = r_{eff}\)
------维度增加了但有效秩不变。这是**纯浪费**。

**诚实结论**：在已有强大结构编码的模型（GNN、Transformer、pLM）之上叠加
Situs，大概率是**零增益 + 微损害**。Situs
最有用时是作为**仅有的**位置信息源（当 \(\phi(s_i)\)
完全没有空间信息时）。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2.3 物理对称性破坏（Physical Symmetry
Breaking）<!-- label: ux7269ux7406ux5bf9ux79f0ux6027ux7834ux574fphysical-symmetry-breaking -->

**机制**：

Situs 的加法注入 \(h_i = \phi(s_i) + PE(p_i)\)
**刻意破坏**了物理系统的某些对称性。当这些对称性对预测任务重要时，这是有害的。

**三种破坏的对称性**：

#### 2.3.1
平移对称性破坏（对体相性质预测是坏的）<!-- label: ux5e73ux79fbux5bf9ux79f0ux6027ux7834ux574fux5bf9ux4f53ux76f8ux6027ux8d28ux9884ux6d4bux662fux574fux7684 -->

完美晶体中，所有原胞等价------体相性质（带隙、弹性常数、声子频率）应具有**完全平移不变性**。

使用 Situs 后： - 两个等价原胞中的原子获得不同的 \(h_i\) -
模型必须额外学习''忽略位置''------增加了不必要的学习负担 -
更糟：如果训练集有限，模型可能学到''带隙依赖于原子索引''的虚假规律

**实例**：预测 AlN 体相带隙（~6.2 eV，{[}Yan et al.,
*Phys. Rev.~B* 93, 014110 (2016){]}） - \(N=32\) 超胞中每个 N
原子的 Situs 编码不同 -
如果模型用这些编码预测同一个带隙标签，它必须在内部学习''这些编码应该被忽略''
- 对小数据集，这可能导致过拟合到特定的编码值

**判断**：如果任务标签具有平移不变性（体相性质），Situs
**不应使用**。如果任务标签不具有平移不变性（缺陷形成能、表面能、局域态密度），Situs
**应当使用**。

#### 2.3.2 旋转对称性破坏（3D 旋转编码的硬伤------已在 1.2.2
分析）<!-- label: ux65cbux8f6cux5bf9ux79f0ux6027ux7834ux574f3d-ux65cbux8f6cux7f16ux7801ux7684ux786cux4f24ux5df2ux5728-1.2.2-ux5206ux6790 -->

#### 2.3.3
排列对称性破坏（对集合型预测是坏的）<!-- label: ux6392ux5217ux5bf9ux79f0ux6027ux7834ux574fux5bf9ux96c6ux5408ux578bux9884ux6d4bux662fux574fux7684 -->

原子系统本质上是**粒子的集合**------原子的编号/顺序是人为的，不应影响物理预测。

Situs 依赖''第 \(i\) 个原子的位置 \(p_i\)``，其中 \(i\)
是原子的索引。如果数据加载时的原子排序发生变化，\(h_i\)
会不同------即使物理系统完全相同。

**这在以下场景中造成问题**： - DFT
计算中原子列表的排序无物理意义（VASP/PWscf
输出中的原子顺序是输入顺序的函数） -
分子动力学轨迹中，原子可能跨过周期性边界，改变其在数组中的位置 -
不同数据源的原子排序约定不同

**缓解措施**：使用**等变**的位置编码（如基于距离矩阵或原子环境的编码），或要求数据预处理中保证一致的原子排序（如按坐标排序------但这又引入了排序的人为性）。

**诚实结论**：Situs
破坏排列对称性是一个**实际工程问题**而非理论缺陷------可以通过一致的预处理缓解，但无法根除。如果原子排序在不同样本间不一致，Situs
引入的噪声可能淹没信号。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

## 第 3
部分：适用场景分析表<!-- label: ux7b2c-3-ux90e8ux5206ux9002ux7528ux573aux666fux5206ux6790ux8868 -->

对 6 个具体场景，评估 \(\delta_s^{PE}\)
的符号（正/零/负）、量级（大/中/小/零）和物理论证。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.0577}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1154}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.5192}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1923}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1154}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
场景
\end{minipage} & \begin{minipage}[b]
\(\delta_s^{PE}\) 符号
\end{minipage} & \begin{minipage}[b]
量级估计
\end{minipage} & \begin{minipage}[b]
理由
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**1** & **AlN 缺陷检测：\(V_N\) 空位，534 帧** & **正** &
**大** & 3D 位置因果决定缺陷形成能（§1.2.1）。534
帧在材料缺陷数据中属于中等规模，足以学习位置-能量关系。位置信息不冗余（\(\phi(s_i)\)
为局部化学特征，不含全局空间上下文）。3D
旋转编码的平移不变性在此场景中恰好合适（缺陷中心对齐后相对位置有意义）。\(I(Y; P \mid S)\)
估计：1.5--2.5 bits（通过形成能三分位
binning），\(\delta_s^{PE} \gtrsim 0.4\)。**但是**：如果 534
帧包含多个晶粒取向，旋转等变性缺失会引入噪声（见 §1.2.2
的警告）。建议先检查取向分布，必要时做取向对齐预处理。 

**2** & **蛋白质功能预测：酶活性位点分类** & **正**（弱）
& **中小** & 序列位置与功能位点有统计相关性（N 端/C
端偏好、结构域位置），但效应量弱。\(I(Y; P_{1D} \mid S) > 0\)
成立但数值有限（\textless{} 0.3
bits，因为大部分功能信息已在残基类型和局部序列上下文中）。**关键限制**：Situs
使用 1D 序列位置而非 3D 空间位置------而活性位点功能由 3D
位置决定。序列→3D 映射因 fold
差异而非单值。**结论**：有微弱正面贡献，但远不如直接使用 3D
结构信息（如有 AF2 预测结构）。若已有 pLM
embedding（含位置信息），收益趋近于零（共线性问题，§2.2）。 

**3** & **Drug-target 对接评分：DrugBank 6784 条** &
**正**（有条件） & **中小** & 条件：使用 3D 对接姿态坐标（而非
1D 序列位置）。结合亲和力（\(K_d\), \(K_i\), \(\Delta G\)）是 3D
姿态的函数------口袋位置、氢键几何、疏水接触面积都由空间位置决定。\(I(Y; P_{3D} \mid S)\)
\textgreater{} 0。**但是**：6784 条数据对于学习复杂的 3D
位置-亲和力映射偏少（特别是考虑到对接姿态的巨大构象空间）。Situs 的
Lipschitz 光滑性（定理
2.5.1）在此是有益的------它正则化了邻近空间位置的预测。有过度依赖结合位点位置的风险（分子骨架结构也有贡献）。**建议**：仅在对接姿态质量高（RMSD
\textless{} 2.0 Å to experimental）的子集上使用 3D Situs。 

**4** & **纯化学组成分类：无空间结构** & **零**（或略负）
& **零** & \(\mathcal{P}\)
未定义。没有物理位置信息可编码。强行使用（如人工赋予虚拟索引）→
编码的是数据加载顺序的 artifact。\(I(Y; P \mid S) \equiv 0\)。由定理
2.2.1，\(\delta_s^{PE} = 0\)。由定理
2.5.1，编码随虚拟位置平滑变化------但这变化不含任何标签信息。唯一的非零效应来自
\(\delta_s^{variance}\)（有限专家的估计噪声），表现为
\(O(1/\sqrt{M})\) 的**净负贡献**。**这是 Situs
的绝对禁区**------加了一定更差。 

**5** & **随机排列的原子构型：无周期结构** & **负** &
**中** & 位置存在（有 3D
坐标），但位置与标签之间**没有物理规律性**------构型是随机的。\(I(Y; P \mid S) = 0\)（随机排列破坏了所有位置-标签信息论联系）。但训练集中有限的随机涨落可能产生**偶然的**位置-标签相关，模型会学到这些虚假模式
→ 测试时泛化差。由 Theorem 2'（不完美 PPE
下界），\(\varepsilon_{PE}\)
在训练分布上被低估，导致上界过松（过度自信）。\(\delta_s^{PE}\)
在训练集上 \textgreater{} 0（虚假），在测试集上 \textless{}
0（真实）。**这是 Situs
最危险的场景**------表面收益是统计假象。使用前必须检验 \(I(Y; P \mid S)\)
的统计显著性（通过 permutation test）。 

**6** & **碳纳米管手性分类：(n, m) 索引** & **正** &
**大** & 手性 \((n,m)\) 完全由 3D
原子排列的全局几何决定------这是位置编码的理想场景。所有碳原子具有相同的局部
\(sp^2\) 化学环境（\(\phi(s_i) \approx\) 常数），因此
\(I(Y; S) \approx 0\)（纯化学组成无法区分手性）而
\(I(Y; P) = H(Y) = \log_2 K\)（\(K\)
为手性类别数）。\(I(Y; P \mid S) \approx H(Y)\)------**几乎全部信息来自位置**。Situs
成为信息的**主要**而非辅助来源。正弦/旋转编码通过捕捉原子间的相对位置模式，可以编码螺旋缠绕的周期性和管径信息。**但是**：需要注意周期性边界条件的编码一致性------CNT
在圆周方向有周期性，Situs 的 3D
旋转编码不会自动沿圆周闭合。对于小直径管（n+m \textless{}
15），周长效应明显，需要特殊处理。 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

## 第 4
部分：每个场景一句话建议<!-- label: ux7b2c-4-ux90e8ux5206ux6bcfux4e2aux573aux666fux4e00ux53e5ux8bddux5efaux8bae -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.0682}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1364}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.7955}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
场景
\end{minipage} & \begin{minipage}[b]
建议（加不加 Situs + 一句话理由）
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**1** & AlN \(V_N\) 缺陷 534 帧 & **加**------3D
位置是形成能的直接物理原因，534
帧足够学习空间模式，前提是取向已对齐或模型能容忍旋转非等变性。 

**2** & 酶活性位点分类 & **不加**（或改用 3D Situs）------1D
序列位置是 3D 功能位置的弱代理，尤其当已有 pLM
embedding（含注意力位置偏差）时，1D Situs 沦为共线性冗余。如有 AlphaFold
预测结构，改用 3D Situs。 

**3** & DrugBank 对接评分 & **有条件加**------仅当使用高质量
3D 对接姿态（RMSD \textless{} 2 Å）时加 3D Situs；6784 条数据对 3D
编码维度偏小，需配合强正则化或降维编码。 

**4** & 纯组成分类无结构 & **绝对不加**------没有位置就没有
Situs；任何人为赋予的伪位置都是统计噪声，可能产生虚假相关。 

**5** & 随机原子构型 &
**不加**------随机位置与标签的信息论联系为零，Situs
在此是虚假相关性的滋生器；若真要使用，必须先做 permutation test 验证
\(I(Y;P \mid S)\) 的统计显著性。 

**6** & CNT 手性 (n,m) 分类 & **加**------手性由全局 3D
几何唯一确定，Situs
从仅有的位置信息中提取特征（碳原子的局部化学环境完全不携带手性信息），这是
Situs 的''教科书级''应用场景。 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

## 总结：Situs
的物理适用边界<!-- label: ux603bux7ed3situs-ux7684ux7269ux7406ux9002ux7528ux8fb9ux754c -->

### 它何时工作（按信心排序）<!-- label: ux5b83ux4f55ux65f6ux5de5ux4f5cux6309ux4fe1ux5fc3ux6392ux5e8f -->

1. 
2. 
3. 

### 它何时无用（加了等于白加）<!-- label: ux5b83ux4f55ux65f6ux65e0ux7528ux52a0ux4e86ux7b49ux4e8eux767dux52a0 -->

1. 
2. 

### 它何时有害（加了更差）<!-- label: ux5b83ux4f55ux65f6ux6709ux5bb3ux52a0ux4e86ux66f4ux5dee -->

1. 
2. 
3. 

### 理论洞察与工程现实的鸿沟<!-- label: ux7406ux8bbaux6d1eux5bdfux4e0eux5de5ux7a0bux73b0ux5b9eux7684ux9e3fux6c9f -->

定理 2.2.1 给出的充分条件 \(I(Y; P \mid S) > 0\)
是**必要且精确的**，但在实践中： - 估计 \(I(Y; P \mid S)\)
本身需要大量样本（KSG 估计器的收敛维度灾难，定理 3.3.1） - 即使
\(I(Y; P \mid S) > 0\)，定理 2.3.1 的上界可能因编码不完美度
\(\varepsilon_{PE}\) 而极度松弛 - Theorem 3' 揭示的''学习型 PPE
可能区分噪声和困难样本''在实践中**通常不发生**------因为物理学常用的
PE 是固定的，而学习型 PE 的信号太弱无法可靠破坏不可区分性

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*分析日期：2026-06-29*

*物理数据引用：Bartlett (2002), Creighton (1993), Dunker (2005),
Freysoldt (2014), Makov \& Payne (1995), Pauling (1951), Stampfl \& Van
de Walle (2002), Van de Walle \& Neugebauer (2004), Yan (2016), 等*

*方法论声明：所有 \(\delta_s^{PE}\)
的估计来自物理推演而非数值实验------需要 DFT
计算和蛋白质结构分析来验证/校准这些估计。*