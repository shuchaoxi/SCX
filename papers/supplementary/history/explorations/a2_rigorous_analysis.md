\section{A2
的严格数学分析}<!-- label: a2-ux7684ux4e25ux683cux6570ux5b66ux5206ux6790 -->

> 触发: hostile review 指出 \(\exp(-2M\Delta^2/(1+(M-1)\rho))\)
> 不是严格定理 结论: 正确。方差膨胀代入 Hoeffding
> 是指启发式，不是严格界。但 A2 本身有更强的论证。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{1. \(\exp(-2M t^2/(1+(M-1)\rho))\)
是不是严格定理？}{1. \ exp(-2M t\^{}2/(1+(M-1)\ rho)) 是不是严格定理？}}<!-- label: exp-2m-t21m-1rho-ux662fux4e0dux662fux4e25ux683cux5b9aux7406 -->

**不是。**

Hoeffding 不等式的证明依赖:
\[\mathbb{E}\left[\exp\left(\lambda\sum_{i=1}^M (X_i - \mu_i)\right)\right] = \prod_{i=1}^M \mathbb{E}[\exp(\lambda(X_i - \mu_i))]\]

这个**因式分解**要求 \(\{X_i\}\) 独立。如果 \(X_i\) 相关，MGF
不能因式分解，你不能简单地把 \(M\) 替换成 \(M/(1+(M-1)\rho)\)
就得到严格指数界。

方差膨胀 \((1+(M-1)\rho)\) 对 **\(Var(\sum X_i)\)**
是正确的，但对 **指数集中** 不正确。方差只给 Chebyshev
界（多项式速率 \(1/t^2\)），不是指数界。

**结论**: 方差膨胀 Hoeffding
是启发式（heuristic），在调查抽样和群组随机试验中广泛使用，但不是数学定理。把它写进
SI 会被审稿人抓。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. 那 A2
本身到底站不站得住？}<!-- label: ux90a3-a2-ux672cux8eabux5230ux5e95ux7ad9ux4e0dux7ad9ux5f97ux4f4f -->

\subsubsection{2.1 更强的论证: A1 蕴含
A2}<!-- label: ux66f4ux5f3aux7684ux8bbaux8bc1-a1-ux8574ux542b-a2 -->

A1 说: \(M\) 个专家在**不相交的独立同分布子集**上训练。
\[D_1, ..., D_M \sim_{i.i.d.} P^n \quad 且 \quad D_i \cap D_j = \varnothing\]

每个 \(f_m = \mathcal{A}(D_m)\) 是训练算法 \(\mathcal{A}\)
作用于数据子集 \(D_m\) 的**确定函数**。

因为 \(D_1, ..., D_M\) 是独立随机变量，\(f_1, ..., f_M\)
也是独立的随机函数。

对任意固定的测试点 \(x\):
\[e_m(x, y) = \mathbf{1}\{\ell(f_m(x), y) > \tau\}\]

因为 \(f_m\) 只依赖 \(D_m\)，且
\(D_1 \perp D_2 \perp ... \perp D_M\):
\[e_1 \perp e_2 \perp ... \perp e_M \quad \mid \quad x\]

**A2 不是假设------它是 A1 的推论。**

\subsubsection{2.2
概率空间是什么？}<!-- label: ux6982ux7387ux7a7aux95f4ux662fux4ec0ux4e48 -->

Hoeffding
界的概率空间是**训练数据的随机性**，不是测试数据的随机性。

\[\mathbb{P}_{D_1,...,D_M}\left(C(x) > \theta \mid clean, x\right) \leq \exp(-2M(\theta-\mu_s)^2)\]

意思是: 如果你随机划分训练数据 \(M\) 次、独立训练 \(M\)
个专家，得到的专家集以高概率具有好的噪声检测性质。

**训练完成后**，你有一组固定的专家。对于给定的测试样本
\(x\)，\(C(x)\) 是一个确定性的数。Hoeffding 不适用。

但这不削弱定理------所有的泛化界都有这个性质。定理告诉你''这个**方法**是好的''，不是''这组**特定专家**是好的''。

\subsubsection{2.3 Hostile reviewer
的反驳为什么不对}<!-- label: hostile-reviewer-ux7684ux53cdux9a73ux4e3aux4ec0ux4e48ux4e0dux5bf9 -->

> ``所有 CNN 在模糊图像上都一起错''

这是在说: **给定已经训练好的
CNN**，它们在模糊图像上的确定行为是一致的。

但 Hoeffding 问的是:
**在训练之前**，随机划分数据并独立训练后，你有多大把握得到一组能检测噪声的专家？

两者不在同一个概率空间里。Hostile reviewer
混淆了**训练后确定性行为**和**训练前概率保证**。

\subsubsection{2.4
但仍有一个残留问题}<!-- label: ux4f46ux4ecdux6709ux4e00ux4e2aux6b8bux7559ux95eeux9898 -->

即使 A2 严格成立（作为 A1 的推论），**估计** \(\mu_s\)
仍然需要清洁标签。在有限样本下，\(\hat_s\) 的误差会转化为
\(\hat_s\)
的误差。这是**有限样本估计问题**，不是**独立性假设问题**。推论
4（有限样本校正）已经用保守上界处理了这个问题。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3.
诚实的修改建议}<!-- label: ux8bdaux5b9eux7684ux4feeux6539ux5efaux8bae -->

#### 3.1 不要引入 A2'<!-- label: ux4e0dux8981ux5f15ux5165-a2 -->

方差膨胀 Hoeffding 是启发式，不够格写进定理陈述。保持原有的
A2，但**在正文和 SI 中诚实讨论**。

\subsubsection{3.2 在 SI 中加一节 ``On the Role of Assumption
A2''}<!-- label: ux5728-si-ux4e2dux52a0ux4e00ux8282-on-the-role-of-assumption-a2 -->

内容: 1. A2 实际上是 A1 的推论（不相交训练集 → 独立专家 → 独立错误） 2.
概率空间是训练随机性，不是测试行为 3. 有限样本下 \(\mu_s\)
的估计误差有独立处理（推论 4） 4.
在实践中，专家错误可能表现出表面相关（同一张模糊图），但这反映的是特征相似性导致相似的
\(\mu_s\)，而非统计相关性 5. 对 A2 的经验诊断:
在验证集上估计专家错误的条件相关系数；如果显著偏离零，检查训练集是否真的不相交

\subsubsection{3.3
在正文中诚实措辞}<!-- label: ux5728ux6b63ux6587ux4e2dux8bdaux5b9eux63aaux8f9e -->

把 ``conditional independence'' 改为: \textgreater{} ``conditional
independence of expert errors, which follows from training on disjoint
data subsets (Assumption A1)''

这样把 A2 从''假设''降级为''A1 的逻辑结果''，同时指出它依赖于 A1
的正确执行。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. 最终判断<!-- label: ux6700ux7ec8ux5224ux65ad -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.6000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.4000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
问题
\end{minipage} & \begin{minipage}[b]
状态
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
A2 是否站得住？ & **是** --- A1 蕴含 A2（训练集不相交 →
专家独立） 

在实践中是否违反？ & **取决于 A1 的执行** ---
如果训练集真的不相交，A2 成立 

\(\exp(-2M\Delta^2/(1+(M-1)\rho))\) 是否严格？ & **否** ---
这是启发式，不应写进定理 

应该如何修改？ & 澄清 A2 是 A1 的推论；在 SI
中加入诚实讨论；不要引入虚假的 A2' 

对论文的影响程度 & **低** ---
不需要改定理陈述，只需要加一段诚实讨论 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. 对 hostile review
其他批评的回应}<!-- label: ux5bf9-hostile-review-ux5176ux4ed6ux6279ux8bc4ux7684ux56deux5e94 -->

\subsubsection{``CIFAR F1=0.617, 理论下界
F1≥0.976''}<!-- label: cifar-f10.617-ux7406ux8bbaux4e0bux754c-f10.976 -->

这已经在 §4.3（紧致性讨论）中诚实处理了: \(\mu_s\) 在 CIFAR 实验中约为
0.45（3-epoch CPU 训练后），而非假定的 0.20。代入正确的 \(\mu_s\)
后下界为 F1≥0.18，与经验值 0.617 一致。

\subsubsection{\texorpdfstring{``\(\mu_s\) 需要清洁标签 →
鸡生蛋''}{``\ mu\_s 需要清洁标签 → 鸡生蛋''}}<!-- label: mu_s-ux9700ux8981ux6e05ux6d01ux6807ux7b7e-ux9e21ux751fux86cb -->

冷启动协议需要少量锚点样本（推论 1），这是理论上的必要成本（Thm 3
证明了没有锚点时不可识别）。这不是循环定义------是对不可识别性定理的工程回应。

\subsubsection{``Bootstrap 诊断的 τ=0.7
是拍脑袋''}<!-- label: bootstrap-ux8bcaux65adux7684-ux3c40.7-ux662fux62cdux8111ux888b -->

承认。\(\tau=0.7\) 是初始校准值，应在具体领域中根据已知噪声标签校准。SI
中应明确标注为''建议初始值，需领域校准''。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*关联: {[}{[}01\_noise\_detection\_guarantee{]}{]} ·
{[}{[}03\_unidentifiability{]}{]} ·
{[}{[}a2\_correlation\_analysis{]}{]}*