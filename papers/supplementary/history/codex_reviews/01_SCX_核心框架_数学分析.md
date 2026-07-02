\section{SCX (State-Conditioned eXpertise)
核心数学框架深度分析}<!-- label: scx-state-conditioned-expertise-ux6838ux5fc3ux6570ux5b66ux6846ux67b6ux6df1ux5ea6ux5206ux6790 -->

> 本文档对 SCX
> 状态条件专家可靠性框架进行逐层解构，追溯每个数学对象的统计/信息论/博弈论源头，证伪/证成三条核心命题，并给出理论边界。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 目录<!-- label: ux76eeux5f55 -->

1. 
2. 
3. 
4. 
5. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. 数学根源追溯<!-- label: ux6570ux5b66ux6839ux6e90ux8ffdux6eaf -->

\subsubsection{1.1 条件风险与 Kolmogorov
公理体系}<!-- label: ux6761ux4ef6ux98ceux9669ux4e0e-kolmogorov-ux516cux7406ux4f53ux7cfb -->

\paragraph{1.1.1
核心对象再定义}<!-- label: ux6838ux5fc3ux5bf9ux8c61ux518dux5b9aux4e49 -->

SCX 分析的基础是状态条件专家风险：

\[R_m(s) = \mathbb{E}_{x \sim P(\cdot|s)}[\ell(f_m(x), f^*(x))]\]

这一定义看似平凡，实则嵌套了 Kolmogorov
概率公理体系中三个最深刻的概念：**条件期望**、**正则条件概率**
和 **Radon-Nikodym 导数**。

\paragraph{1.1.2 Kolmogorov
条件期望的正式定义}<!-- label: kolmogorov-ux6761ux4ef6ux671fux671bux7684ux6b63ux5f0fux5b9aux4e49 -->

设 \((\Omega, \mathcal{F}, P)\) 为概率空间，\(X\) 为随机变量满足
\(\mathbb{E}[|X|] < \infty\)，\(\mathcal{G} \subseteq \mathcal{F}\) 为子
\(\sigma\)-代数。则存在 \(P\)-几乎必然唯一的 \(\mathcal{G}\)-可测函数
\(\mathbb{E}[X|\mathcal{G}]\)，满足：

\[\forall G \in \mathcal{G}: \int_G \mathbb{E}[X|\mathcal{G}] dP = \int_G X dP\]

**存在性**由 Radon-Nikodym 定理保证：定义有限符号测度
\(\nu(G) = \int_G X dP\)，则 \(\nu \ll P|_{\mathcal{G}}\)，其 RN
导数即为 \(\mathbb{E}[X|\mathcal{G}]\)。

SCX 中的 \(R_m(s)\) 本质上是
\(\mathbb{E}[\ell(f_m(X), f^*(X)) | X \in s]\)。设 \(s\) 为
\(\mathcal{X}\) 中的一个可测子集，则状态 \(s\)
对应条件事件，\(R_m(s) = \mathbb{E}[L_m | \mathbf{1}_s(X)=1]\)，其中
\(L_m = \ell(f_m(X), f^*(X))\)。

\paragraph{1.1.3
正则条件概率}<!-- label: ux6b63ux5219ux6761ux4ef6ux6982ux7387 -->

严格处理 \(P(\cdot|s)\) 需要正则条件概率（Regular Conditional
Probability）。给定随机元 \(X: \Omega \to \mathcal{X}\) 和子
\(\sigma\)-代数 \(\mathcal{G} \subset \mathcal{F}\)，若存在映射
\(P(\cdot|\mathcal{G})(\cdot): \mathcal{F} \times \Omega \to [0,1]\)
满足：

1. 
2. 

则称 \(P(\cdot|\mathcal{G})(\cdot)\) 为正则条件概率。

在 SCX 中，状态 \(s\) 诱导出条件分布 \(P_{X|s}\)。当
\(\mathcal{X} = \mathbb{R}^d\) 为 Polish 空间时，正则条件概率存在（这由
Blackwell 定理保证）。因此 \(P(x|s)\) 在测度论意义下是良定义的。

\paragraph{\texorpdfstring{1.1.4 损失函数 \(\ell\)
的可积性条件}{1.1.4 损失函数 \ ell 的可积性条件}}<!-- label: ux635fux5931ux51fdux6570-ell-ux7684ux53efux79efux6027ux6761ux4ef6 -->

\(R_m(s)\) 的良定义需要 \(\ell(f_m(x), f^*(x))\) 对 \(P(\cdot|s)\)
可积。对于回归问题 (\(\ell_2\) 损失) 或分类问题 (0-1 损失)，只要 \(f_m\)
和 \(f^*\) 是平方可积函数，条件期望存在。更一般地，若 \(\ell\) 是凸的且
\(f^*(x) = \arg\min_y \mathbb{E}[\ell(Y, y)|X=x]\)
(贝叶斯最优)，则相关测度论条件自动满足。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.2
统计决策理论与贝叶斯风险}<!-- label: ux7edfux8ba1ux51b3ux7b56ux7406ux8bbaux4e0eux8d1dux53f6ux65afux98ceux9669 -->

**1.2.1 从 Wald 到 SCX**<!-- label: ux4ece-wald-ux5230-scx -->

Abraham Wald 在 1950 年代建立的统计决策理论框架为 SCX
的条件风险提供了上层结构：

- 
- 
- 

SCX 的创新在于将这一框架**局部化**到每个状态 \(s\)：

\[R_m(s) = \int_{\mathcal{X}} \ell(f_m(x), f^*(x)) dP_{X|s}(x)\]

这正是**状态条件**的贝叶斯风险，其先验由状态 \(s\) 的指示函数给出。

\paragraph{1.2.2 Berger
的广义贝叶斯分析}<!-- label: berger-ux7684ux5e7fux4e49ux8d1dux53f6ux65afux5206ux6790 -->

Berger (1985) 指出，任意合理的决策规则都是某个（可能为
impropriate）先验下的广义贝叶斯规则。SCX 状态条件路由
\(m^*(x) = \arg\min_m \sum_s \gamma_s(x) R_m(s)\) 可理解为：将输入 \(x\)
的不确定性通过状态的软赋值 \(\gamma_s(x)\)
分散到多个''局部先验''上，然后取后验期望损失最小的专家。

\paragraph{1.2.3 与 PAC-Bayes
的联系}<!-- label: ux4e0e-pac-bayes-ux7684ux8054ux7cfb -->

状态条件风险 \(R_m(s)\) 与 PAC-Bayes 边界也有深层联系。令
\(\mathcal{Q}\) 为专家假设空间上的后验分布，标准 PAC-Bayes 边界为：

\[\mathbb{E}_{h \sim \mathcal{Q}}[R(h)] \leq \mathbb{E}_{h \sim \mathcal{Q}}[\hat{R}(h)] + \sqrt{\frac{KL(\mathcal{Q}||\mathcal{P}) + \log(n/\delta)}{2n}}\]

SCX 中，状态条件权重
\(w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(x) \hat{R}_m(s))\)
可以看作一个**状态依赖的后验** \(\mathcal{Q}_x\)，其 KL
散度相对于均匀先验的惩罚项通过 \(\alpha\) 参数控制，实现了状态水平的
PAC-Bayes 边界。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.3
状态划分：充分统计量与信息瓶颈}<!-- label: ux72b6ux6001ux5212ux5206ux5145ux5206ux7edfux8ba1ux91cfux4e0eux4fe1ux606fux74f6ux9888 -->

**1.3.1 状态的定义**<!-- label: ux72b6ux6001ux7684ux5b9aux4e49 -->

SCX 中的''状态'' \(s\) 是输入空间 \(\mathcal{X}\)
的一个子集或一个区域。状态划分的数学本质是找到一个映射
\(\phi: \mathcal{X} \to \mathcal{S}\)，使得：

\[P(Y|X) \approx P(Y|\phi(X))\]

即 \(\phi(X)\) 是 \(Y\) 关于 \(X\) 的**近似充分统计量**。

\paragraph{1.3.2
充分统计量理论}<!-- label: ux5145ux5206ux7edfux8ba1ux91cfux7406ux8bba -->

Fisher (1922) 提出：统计量 \(T(X)\) 对参数 \(\theta\)
是充分的，当且仅当：

\[P(X|T(X), \theta) = P(X|T(X))\]

等价地，由 Neyman-Fisher 因子分解定理：

\[p(x|\theta) = g(T(x), \theta) \cdot h(x)\]

在 SCX 中，状态 \(s\) 的角色类似于一个离散的充分统计量：给定
\(x \in s\)，专家的条件风险 \(R_m(s)\)
应能充分反映专家在该区域的性能，而不需要更细粒度的 \(x\) 信息。

更精确地说，SCX 的最优状态划分 \(\mathcal{S}^*\) 应满足：

\[R_m(s) = \mathbb{E}[\ell(f_m(X), f^*(X)) | X \in s] \approx \mathbb{E}[\ell(f_m(X), f^*(X)) | X = x], \quad \forall x \in s\]

即状态内部的条件风险方差最小化。

\paragraph{1.3.3
信息瓶颈原理}<!-- label: ux4fe1ux606fux74f6ux9888ux539fux7406 -->

Tishby, Pereira 与 Bialek (1999) 提出的信息瓶颈 (IB)
原理为状态划分提供了变分框架：

\[\min_{p(\tilde{X}|X)} I(X; \tilde{X}) - \beta I(\tilde{X}; Y)\]

其中 \(\tilde{X}\) 是 \(X\) 的压缩表示。在 SCX 中，状态变量
\(S = \phi(X)\) 扮演了 \(\tilde{X}\) 的角色。IB 拉格朗日量：

\[\mathcal{L}_{IB} = I(X; S) - \beta I(S; Y)\]

- 
- 
- 

SCX 的状态划分隐式地解决了 IB 目标：它寻找一个状态空间
\(\mathcal{S}\)，使得： 1. 同一状态内的样本有相似的专家表现（高
\(I(S; R_m)\)） 2. 状态数量可控（低 \(I(X; S)\)）

当 \(\beta \to \infty\) 时，IB 退化为每个 \(x\)
对应唯一状态（完全不压缩），\(M^* = 专家数量\)；当
\(\beta \to 0\) 时，\(|S| = 1\)（全局池化），退化为全局专家排序。

\paragraph{1.3.4
率失真理论视角}<!-- label: ux7387ux5931ux771fux7406ux8bbaux89c6ux89d2 -->

状态划分也是率失真理论 (Rate-Distortion Theory)
的一个实例。定义失真度量：

\[d(x, x') = |R_m(x) - R_m(x')|\]

其中 \(R_m(x) = \mathbb{E}[\ell(f_m(X), f^*(X)) | X = x]\)
为点态条件风险。状态划分等价于对 \((\mathcal{X}, d)\)
进行量化（quantization），率失真函数为：

\[R(D) = \min_{P(S|X): \mathbb{E}[d(X, S)] \leq D} I(X; S)\]

SCX 的聚类过程（如 K-means on 嵌入空间）正是 \(R(D)\) 的一个经验近似。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.4 数据价值：Shapley
公理与合作博弈论}<!-- label: ux6570ux636eux4ef7ux503cshapley-ux516cux7406ux4e0eux5408ux4f5cux535aux5f08ux8bba -->

\paragraph{1.4.1
数据价值函数的形式}<!-- label: ux6570ux636eux4ef7ux503cux51fdux6570ux7684ux5f62ux5f0f -->

SCX 定义状态 \(s\) 的**数据价值**为：

\[V(s) = \bar{r}(s) \cdot \rho(s) \cdot L(s) \cdot [1 - D(s)] \cdot \max_m SCX_m(s)\]

这是五个因子的乘积。其根源可追溯到合作博弈论中的**Shapley
公理体系**和**数据 Shapley** (Ghorbani \& Zou, 2019)。

\paragraph{1.4.2 Shapley
值的公理}<!-- label: shapley-ux503cux7684ux516cux7406 -->

Shapley (1953) 定义了合作博弈 \(v: 2^N \to \mathbb{R}\) 中单个玩家 \(i\)
的价值：

\[\phi_i(v) = \frac{1}{|N|!} \sum_{\pi \in \Pi(N)} [v(S_\pi^i \cup \{i\}) - v(S_\pi^i)]\]

其中 \(S_\pi^i\) 是排列 \(\pi\) 中 \(i\) 之前玩家的集合。Shapley
值是唯一满足以下公理的分配方案：

1. 
2. 
3. 
4. 

\paragraph{1.4.3 SCX 价值函数与 Shapley
的偏离}<!-- label: scx-ux4ef7ux503cux51fdux6570ux4e0e-shapley-ux7684ux504fux79bb -->

SCX 的 \(V(s)\) 不是精确的 Shapley
值，而是其**可分解代理**。真正计算数据点级别的 Shapley 值是
\(O(2^N)\) 的。SCX 做了关键简化：

- 
- 

将 \(V(s)\) 的因子逐个与博弈论概念对应：

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
因子 & 博弈论对应 & 解释 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\bar{r}(s)\) & 边际收益 & 该状态当前的残差越高，改善的潜在收益越大 

\(\rho(s)\) & 概率权重 & 罕见状态的预期收益需打折扣 

\(L(s)\) & 可达收益 & 噪声大或无结构的状态无法通过学习改善 

\(1-D(s)\) & 多样性惩罚 & 冗余高的点贡献为负（已有类似信息） 

\(\max_m SCX_m(s)\) & 可实现性 & 必须有可靠的专家来获取收益 

\end{longtable}

这种分解是**启发式但可解释的**，其代价是放弃 Shapley 的加法公理。

\paragraph{1.4.4 与 Data Shapley
的精确关系}<!-- label: ux4e0e-data-shapley-ux7684ux7cbeux786eux5173ux7cfb -->

Ghorbani \& Zou (2019) 的数据 Shapley 将每个训练点 \(z_i\)
的价值定义为：

\[\phi_i = \frac{1}{N} \sum_{k=1}^N \frac{1}{\binom{N-1}{k-1}} \sum_{S \subseteq N \setminus \{i\}, |S| = k-1} [v(S \cup \{i\}) - v(S)]\]

其中 \(v(S)\) 是在数据集 \(S\) 上训练的模型的验证性能。

SCX 的 \(V(s)\) 可以看作一个**代理函数** \(\tilde{V}(s)\)，它满足：

\[V(s) \approx \mathbb{E}_{i \in s}[\phi_i] \cdot |s|\]

但 \(V(s)\) 的乘法分解意味着 SCX 假设价值函数具有**因子可分离性**：

\[v(S) \approx \prod_{s \in \mathcal{S}} g_s(|S \cap s|, stats(s))\]

这在 \(v\) 为次模函数时是合理的近似（Shapley 值在次模博弈中具有凹性）。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.5 专家可靠性：Dawid-Skene 与
IRT}<!-- label: ux4e13ux5bb6ux53efux9760ux6027dawid-skene-ux4e0e-irt -->

\paragraph{1.5.1 Dawid-Skene
标注者模型}<!-- label: dawid-skene-ux6807ux6ce8ux8005ux6a21ux578b -->

Dawid \& Skene (1979) 提出了著名的标注者（专家）可靠性模型。设 \(J\)
个标注者对 \(N\) 个样本进行分类，每个样本的真实类别为
\(y_i \in \{1,...,K\}\)。标注者 \(j\) 的混淆矩阵为：

\[\pi^{(j)}_{kl} = P(标注者 j 将类别 k 标为 l)\]

观测似然为：

\[P(数据 | \pi, y) = \prod_{i=1}^N \prod_{j=1}^J \pi^{(j)}_{y_i, z_{ij}}\]

EM 算法交替估计 \(\pi^{(j)}\) 和 \(y_i\) 的后验分布。

SCX 的 \(SCX_m(s) = P(\ell(f_m(x), y) < \tau | x \in s)\) 是 Dawid-Skene
框架的推广：

- 
- 

这一推广的关键数学结果：当存在状态 \(s_1, s_2\) 使得 Dawid-Skene
全局混淆矩阵 \(\pi^{(j)}\) 无法同时预测 \(s_1\) 和 \(s_2\)
上的表现时，状态条件建模是必要的。这正是命题一的本质。

\paragraph{1.5.2 项目反应理论
(IRT)}<!-- label: ux9879ux76eeux53cdux5e94ux7406ux8bba-irt -->

Rasch 模型 (1960) 是 IRT 的基础模型：

\[P(Y_{ij} = 1 | \theta_i, b_j) = \frac{\exp(\theta_i - b_j)}{1 + \exp(\theta_i - b_j)}\]

其中 \(\theta_i\) 是样本 \(i\) 的''能力''，\(b_j\) 是标注者 \(j\)
的''难度阈值''。

SCX 的 \(SCX_m(s)\) 可以映射到 Rasch 模型：

\[\log\left(\frac{SCX_m(s)}{1 - SCX_m(s)}\right) = \theta_s - b_m\]

其中 \(\theta_s\) 是状态 \(s\) 的''可处理性''参数（容易与否），\(b_m\)
是专家 \(m\) 的能力阈值。

**更丰富的 IRT 模型**如 2-PL (两参数逻辑模型)：

\[P(Y_{ij}=1|\theta_i, a_j, b_j) = \frac{\exp(a_j(\theta_i - b_j))}{1 + \exp(a_j(\theta_i - b_j))}\]

对应 SCX 中引入专家确度斜率
\(a_j\)，允许不同专家对状态变化的敏感度不同------这正是 SCX 中
\(max_m SCX_m(s)\) 的核心假设。

\paragraph{1.5.3
与贝叶斯众包的联系}<!-- label: ux4e0eux8d1dux53f6ux65afux4f17ux5305ux7684ux8054ux7cfb -->

Raykar et al.~(2010)
的贝叶斯众包模型进一步考虑了标注者的敏感度和特异度。SCX 在状态水平上的
\(SCX_m(s)\) 可以看作在状态 \(s\)
上的标注者性能矩阵的奇异值分解的第一个分量------即最能区分''可靠/不可靠''维度的投影。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.6 噪声与可学习性：Tsybakov 与
Huber}<!-- label: ux566aux58f0ux4e0eux53efux5b66ux4e60ux6027tsybakov-ux4e0e-huber -->

\paragraph{1.6.1 Tsybakov
噪声条件}<!-- label: tsybakov-ux566aux58f0ux6761ux4ef6 -->

Tsybakov (2004) 提出了分类问题中噪声条件的关键定义。对于二分类问题，设
\(\eta(x) = P(Y=1|X=x)\)，则 Tsybakov 噪声条件为：存在常数 \(C > 0\) 和
\(\alpha \geq 0\)，使得：

\[P_X\left(|\eta(X) - 1/2| \leq t\right) \leq C t^\alpha, \quad \forall t > 0\]

\(\alpha\) 控制决策边界附近的噪声程度： -
\(\alpha = 0\)：无结构噪声（最坏情况） -
\(\alpha \to \infty\)：无噪声（马吉尼-差距条件，Massart 条件）

在 Tsybakov 条件下，分类器的收敛速率为
\(n^{-\frac{1+\alpha}{2+\alpha}}\)。

SCX 的 **噪声分数**：

\[NoiseScore(x_i) = r_i \cdot \frac{1}{\rho(s_i) + \varepsilon} \cdot [1 - C(s_i)]\]

中的 \(C(s)\)（状态内部一致性）与 Tsybakov 参数 \(\alpha\) 有深层联系：

\[C(s) \approx 1 - 2 \cdot \mathbb{E}_{x \in s}[|\eta(x) - 1/2|]\]

当 \(C(s) \to 1\)
时，状态内部近似为贝叶斯最优决策（\(\alpha \to \infty\)）；当
\(C(s) \to 0\) 时，状态内标签接近随机（\(\alpha \to 0\)）。

具体地，若在状态 \(s\) 内有
\(P_X(|\eta(x)-1/2| \leq t | x \in s) \leq C_s t^{\alpha_s}\)，则
\(C(s) = \Phi(\alpha_s)\)，其中 \(\Phi\) 是单调增函数（如
\(\Phi(\alpha) = 1 - e^{-\alpha}\) 或
\(\Phi(\alpha) = \alpha/(1+\alpha)\)）。

**1.6.2 Huber 污染模型**<!-- label: huber-ux6c61ux67d3ux6a21ux578b -->

Huber (1964) 的 \(\varepsilon\)-污染模型：

\[F = (1 - \varepsilon) F_0 + \varepsilon G\]

其中 \(F_0\) 是真实分布，\(G\) 是污染分布，\(\varepsilon \in [0, 1]\)
是污染比例。

SCX 的噪声分数 \(N(s)\) 对应状态 \(s\) 的污染比例 \(\varepsilon_s\)：

\[P_{X|s} = (1 - N(s)) \cdot P_{X|s}^0 + N(s) \cdot P_{X|s}^{noise}\]

其中 \(P_{X|s}^0\) 是干净数据的条件分布，\(P_{X|s}^{noise}\)
是噪声分布。

**可学习性** \(L(s) = C(s) \cdot [1 - N(s)]\) 可以严谨定义为：

\[L(s) = \inf_{f \in \mathcal{F}} \left[ \frac{R(f|s) - R^*(s)}{R^*(s)} \right]^{-1}\]

其中
\(R(f|s) = \mathbb{E}[\ell(f(X), Y) | X \in s]\)，\(R^*(s) = \inf_f R(f|s)\)
是贝叶斯风险。\(L(s) \to 0\) 表示状态在现有函数类 \(\mathcal{F}\)
下不可学习。

\paragraph{1.6.3 Natarajan
维度与噪声}<!-- label: natarajan-ux7ef4ux5ea6ux4e0eux566aux58f0 -->

在噪声条件下学习的样本复杂度由 Natarajan
维度刻画。对于多分类问题，Natarajan (1989) 给出了噪声存在的泛化边界：

\[R(f) \leq \hat{R}_\gamma(f) + \tilde{O}\left(\sqrt{\frac{d}{n\gamma^2}}\right)\]

其中 \(d\) 是 Natarajan 维度。SCX 的 \(L(s)\) 隐式编码了
\(\frac{d_s}{n_s}\) 的比值------状态 \(s\) 的''有效复杂度''。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.7 主动采样：OED、信息论与
Bandit}<!-- label: ux4e3bux52a8ux91c7ux6837oedux4fe1ux606fux8bbaux4e0e-bandit -->

\paragraph{1.7.1 MacKay
信息论主动学习}<!-- label: mackay-ux4fe1ux606fux8bbaux4e3bux52a8ux5b66ux4e60 -->

MacKay (1992) 的主动学习框架基于信息增益：

\[x^* = \arg\max_x H[\theta | \mathcal{D}] - H[\theta | \mathcal{D} \cup \{x, y\}]\]

其中 \(H[\cdot]\) 是 Shannon 熵。在 SCX
的数据四分类中，**valuable** 数据点正是具有高信息增益的点。

SCX 的采样策略等价于优化期望信息增益：

\[\Delta H(s) = H[R_m | \mathcal{D}] - \mathbb{E}_{y \sim P(\cdot|s)}[H[R_m | \mathcal{D} \cup (s, y)]]\]

\(V(s)\) 正比于 \(\Delta H(s)\) 的代理。

\paragraph{1.7.2 最优实验设计
(OED)}<!-- label: ux6700ux4f18ux5b9eux9a8cux8bbeux8ba1-oed -->

在经典 OED 中，目标是选择实验 \(x\) 使得 Fisher
信息矩阵的某个标量函数最优：

- 
- 
- 

SCX 的 \(V(s)\) 中的 \(\bar{r}(s) \cdot L(s)\)
因子对应**与参数估计的不确定性成比例**的采样准则。当 \(\bar{r}(s)\)
大且 \(L(s)\) 高时，标注 \((s, y)\) 对 Fisher 信息矩阵的更新贡献大。

\paragraph{1.7.3 Bandit
视角：探索-利用权衡}<!-- label: bandit-ux89c6ux89d2ux63a2ux7d22-ux5229ux7528ux6743ux8861 -->

SCX 的 acquire 动作本质上是**多臂 Bandit 的变体**：

- 
- 
- 

SCX 的 \(V(s)\) 是 Upper Confidence Bound (UCB) 启发式的推广：

\[V_{UCB}(s) = \underbrace{\bar{r}(s) \cdot L(s)}_{利用项} + \underbrace{\rho(s) \cdot [1 - D(s)]}_{探索项} \cdot \max_m SCX_m(s)\]

其中 \(\rho(s)\) 类比于 UCB 中的
\(\sqrt{\frac{\log t}{n_s}}\)，当状态样本少时 \(\rho(s)\)
被低估，需手动校准 \(\frac{1}{\rho(s) + \varepsilon}\) 因子。

\paragraph{1.7.4 Thompson Sampling
联系}<!-- label: thompson-sampling-ux8054ux7cfb -->

V(s) 中出现的 \(\max_m SCX_m(s)\) 也可以理解为 Thompson Sampling
式的后验概率：对状态 \(s\)，最佳专家 \(m^*(s) = \arg\max_m SCX_m(s)\)
是后验下最可能的''最佳动作''。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.8 SCX-Compress：Coreset
与蒸馏}<!-- label: scx-compresscoreset-ux4e0eux84b8ux998f -->

\paragraph{1.8.1 Coreset
理论基础}<!-- label: coreset-ux7406ux8bbaux57faux7840 -->

Coreset 理论的目标是找到一个加权子集
\(C \subseteq \mathcal{D}\)，使得对任意 \(f \in \mathcal{F}\)：

\[|\sum_{i \in \mathcal{D}} \ell(f(x_i), y_i) - \sum_{j \in C} w_j \ell(f(x_j), y_j)| \leq \varepsilon \sum_{i \in \mathcal{D}} \ell(f(x_i), y_i)\]

SCX-Compress 的四个输出类别构成了一个结构化 coreset：

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
类别 & Coreset 角色 & 权重 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Valuable & 核心集 (必须保留) & \(w_i = 1\) 

Redundant & 可压缩 (冗余合并) & \(w_i < 1/密度\) 

Noisy & 异常值 (排除或降权) & \(w_i = 0\) 或 \(\ll 1\) 

Expert-dependent & 需要路由缓存 & \(w_i\) 取决于选中的专家 

\end{longtable}

**1.8.2 敏感度采样**<!-- label: ux654fux611fux5ea6ux91c7ux6837 -->

Chen et al.~(2018) 的 Coreset 构造通过敏感度采样实现。每个点 \(x_i\)
的敏感度为：

\[\sigma_i = \sup_{f \in \mathcal{F}} \frac{w_i |\ell(f(x_i), y_i)|}{\sum_{j} w_j |\ell(f(x_j), y_j)| - \varepsilon}\]

SCX 的 \(V(s)\) 提供了敏感度的经验代理：

\[\sigma(s) \propto \frac{V(s)}{\sum_{s'} V(s')}\]

当 \(V(s)\) 高时，该状态在 coreset 中被过采样（保留更多点）。

**1.8.3 数据集蒸馏**<!-- label: ux6570ux636eux96c6ux84b8ux998f -->

数据集蒸馏 (Wang et al.~2018) 寻求合成样本 \((x^*, y^*)\)
使得在其上训练的模型近似等价于在全数据集上训练的模型：

\[(x^*, y^*) = \arg\min_{(\tilde{x}, \tilde{y})} \mathcal{L}(\theta(\tilde{x}, \tilde{y}), \mathcal{D}_{val})\]

SCX-Compress 的 Redundant
类别就是蒸馏目标：同一状态内的冗余样本可以用少量代表性样本替代。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{1.9 专家路由：MoE
谱系}<!-- label: ux4e13ux5bb6ux8defux7531moe-ux8c31ux7cfb -->

\paragraph{1.9.1 Jacob et al.~(1991)
自适应混合专家}<!-- label: jacob-et-al.-1991-ux81eaux9002ux5e94ux6df7ux5408ux4e13ux5bb6 -->

这是 MoE 的开山之作。模型使用门控网络 \(g(x)\) 来加权各个专家 \(f_m(x)\)
的输出：

\[f(x) = \sum_{m=1}^M g_m(x) \cdot f_m(x), \quad g_m(x) = softmax(W_g x)_m\]

训练通过 EM 算法最大化对数似然（回归时为加权最小二乘）。

SCX 的专家路由 \(m^*(x) = \arg\min_m \sum_s \gamma_s(x) R_m(s)\)
可以看作 Jacob 门控网络的硬化版本（hard routing vs.~soft routing）。

\paragraph{1.9.2 Shazeer et al.~(2017) 稀疏门控
MoE}<!-- label: shazeer-et-al.-2017-ux7a00ux758fux95e8ux63a7-moe -->

Shazeer 引入 top-\(k\) 门控实现稀疏性：

\[g(x) = softmax(KeepTopK(x \cdot W_g, k))\]

其中 \(KeepTopK(v, k)_i = v_i\) 若 \(v_i\) 在前 \(k\) 大，否则
\(-\infty\)。

SCX 的路由不是基于 \(x\) 本身，而是基于**状态条件风险**
\(\sum_s \gamma_s(x) R_m(s)\)。这是 MoE
门控的一种**元学习变体**：门控决策不是直接学习
\(x \to expert\) 的映射，而是通过估计条件风险来间接确定路由。

\paragraph{1.9.3
负载均衡与辅助损失}<!-- label: ux8d1fux8f7dux5747ux8861ux4e0eux8f85ux52a9ux635fux5931 -->

传统 MoE 需要辅助损失来平衡专家使用率：

\[\mathcal{L}_{balance} = \alpha \cdot CV(expert\_load)^2\]

SCX 的状态条件权重
\(w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(s) \hat{R}_m(s))\)
自然地实现了负载均衡：如果某专家在所有状态上都差，它的权重指数衰减；不同专家在不同状态上胜出，自动分散负载。

\paragraph{1.9.4 从 MoE 到 SCX
的差异}<!-- label: ux4ece-moe-ux5230-scx-ux7684ux5deeux5f02 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
维度 & 传统 MoE & SCX 专家路由 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
门控输入 & 原始特征 \(x\) & 状态赋值 \(\gamma_s(x)\) 

门控参数 & 可学习的 \(W_g\) & 估计的 \(\hat{R}_m(s)\) 

训练方式 & 端到端反向传播 & 两阶段（先估风险，再路由） 

稀疏性 & hard/top-k & 指数软加权 

泛化保证 & 经验风险最小化 & 状态条件 PAC 边界 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2.
三个命题的完整证明框架}<!-- label: ux4e09ux4e2aux547dux9898ux7684ux5b8cux6574ux8bc1ux660eux6846ux67b6 -->

\subsubsection{2.1
命题一：全局专家排序不足}<!-- label: ux547dux9898ux4e00ux5168ux5c40ux4e13ux5bb6ux6392ux5e8fux4e0dux8db3 -->

> **命题陈述**：若存在状态 \(s_1, s_2 \in \mathcal{S}\) 和专家
> \(a, b \in \{1,...,M\}\)，使得 \(R_a(s_1) < R_b(s_1)\) 但
> \(R_a(s_2) > R_b(s_2)\)，则不存在全局最优专家。

**2.1.1 形式化定义**<!-- label: ux5f62ux5f0fux5316ux5b9aux4e49 -->

**定义 1（全局专家排序）**：全局专家排序是一个全序关系 \(\preceq\)
在专家集合 \(\{1,...,M\}\) 上，满足：若 \(a \preceq b\)，则认为专家
\(a\) 整体上不劣于专家 \(b\)。

**定义 2（全局最优专家）**：专家 \(m^*\)
称为全局最优，若对任意其他专家 \(m \neq m^*\) 和任意状态
\(s \in \mathcal{S}\)，有 \(R_{m^*}(s) \leq R_m(s)\)。

**2.1.2 证明**<!-- label: ux8bc1ux660e -->

**证法 1（反证法）**： 假设存在全局最优专家 \(m^*\)。

由全局最优的定义，对所有 \(s \in \mathcal{S}\)：
\[R_{m^*}(s) \leq R_a(s) \quad 且 \quad R_{m^*}(s) \leq R_b(s)\]

但在状态 \(s_1\) 处：\(R_{m^*}(s_1) \leq R_a(s_1) < R_b(s_1)\)，故
\(m^*\) 在 \(s_1\) 上优于 \(b\)。记
\(\Delta_1 = R_b(s_1) - R_{m^*}(s_1) > 0\)。

在状态 \(s_2\) 处：\(R_{m^*}(s_2) \leq R_b(s_2) < R_a(s_2)\)，故 \(m^*\)
在 \(s_2\) 上也优于 \(a\)。记
\(\Delta_2 = R_a(s_2) - R_{m^*}(s_2) > 0\)。

但交叉条件 \(R_a(s_1) < R_b(s_1)\) 且 \(R_a(s_2) > R_b(s_2)\) 意味着：

\[R_a(s_1) - R_b(s_1) < 0 < R_a(s_2) - R_b(s_2)\]

由于 \(R_{m^*}(s_1) \leq R_a(s_1)\) 且
\(R_{m^*}(s_2) \leq R_b(s_2) < R_a(s_2)\)，我们有：

\[R_{m^*}(s_1) \leq R_a(s_1) < R_b(s_1)\]
\[R_{m^*}(s_2) \leq R_b(s_2) < R_a(s_2)\]

但这不产生矛盾。矛盾需要额外的条件。

**修正的证明**：我们需要证明不存在单一的 \(m^*\)
能在两个状态上**同时**最优，而非逐状态最优。

设 \(\mathcal{M} = \{1,...,M\}\)。定义状态条件最优集：

\[\mathcal{M}^*(s) = \arg\min_{m \in \mathcal{M}} R_m(s)\]

若 \(a \in \mathcal{M}^*(s_1)\) 且 \(b \in \mathcal{M}^*(s_2)\)，且
\(a \neq b\)，则
\(|\bigcap_{s \in \mathcal{S}} \mathcal{M}^*(s)| \leq 1\)。若
\(|\mathcal{S}| \geq 2\)
且存在至少两个不同的最优专家，则不存在单个专家在所有状态上都是最优的。

由条件 \(R_a(s_1) < R_b(s_1)\) 得 \(a \in \mathcal{M}^*(s_1)\) 或
\(b \notin \mathcal{M}^*(s_1)\)；由 \(R_a(s_2) > R_b(s_2)\) 得
\(b \in \mathcal{M}^*(s_2)\) 或
\(a \notin \mathcal{M}^*(s_2)\)。若同时有 \(a \in \mathcal{M}^*(s_1)\)
和 \(b \in \mathcal{M}^*(s_2)\)，则当 \(a \neq b\) 时得证。

若 \(a = b\)，则 \(R_a(s_1) < R_a(s_1)\)（矛盾），故 \(a \neq b\)
必然成立。

因此，\(\mathcal{M}^*(s_1) \neq \mathcal{M}^*(s_2)\)，即全局最优专家不存在。\(\square\)

\paragraph{2.1.3
推广：连续状态下的退化形式}<!-- label: ux63a8ux5e7fux8fdeux7eedux72b6ux6001ux4e0bux7684ux9000ux5316ux5f62ux5f0f -->

当 \(\mathcal{S}\) 连续时（如 \(\mathcal{S} = [0,1]\)），命题退化为：若
\(\exists s_1, s_2\) 使得 \(R_a(s_i)\) 与 \(R_b(s_i)\) 交叉，则不存在
Lebesgue-几乎必然的全局最优专家。这用测度论语言表述为：

\[\mu\left(\left\{s \in \mathcal{S} : m^*(s) = \arg\min_m R_m(s)\right\}\right) < 1\]

其中 \(\mu\) 是 \(\mathcal{S}\) 上的某参考测度（如输入分布 \(P_X\) 的
push-forward）。

**2.1.4 实证含义**<!-- label: ux5b9eux8bc1ux542bux4e49 -->

这一命题直接论证了 SCX 框架的**必要性**而非充分性。它说明： -
任何全局聚合指标（平均精度、平均 AUC、F1 宏观平均）都会丢失信息 -
在交叉发生的数据区域，必须引入状态条件建模 -
交叉的频次决定了状态粒度的需求：交叉越多，需要的状态越多

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{2.2
命题二：高误差采样在噪声下非最优}<!-- label: ux547dux9898ux4e8cux9ad8ux8befux5deeux91c7ux6837ux5728ux566aux58f0ux4e0bux975eux6700ux4f18 -->

> **命题陈述**：在噪声存在时，单纯基于残差（max-residual
> sampling）的主动采样策略不是最优的。

**2.2.1 问题形式化**<!-- label: ux95eeux9898ux5f62ux5f0fux5316 -->

设 \(\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N\) 为当前标注数据集，未标注池为
\(\mathcal{U}\)。对于 \(x \in \mathcal{U}\)，定义残差：

\[r(x) = \ell(f_{current}(x), \hat{y}(x))\]

其中 \(\hat{y}(x)\) 是当前最佳预测。

**max-residual 采样**：\(x^* = \arg\max_{x \in \mathcal{U}} r(x)\)

**噪声条件下**，观测到的残差 \(\tilde{r}(x)\) 可分解为：

\[\tilde{r}(x) = r_{true}(x) + \varepsilon(x)\]

其中 \(\varepsilon(x) \sim P_{noise}(x)\) 是状态依赖的噪声过程。

**2.2.2 假设**<!-- label: ux5047ux8bbe -->

1. 
2. 
3. 

**2.2.3 证明**<!-- label: ux8bc1ux660e-1 -->

**证法 1（期望风险最小化）**：

定义采样策略 \(\pi\) 的收益为：

\[J(\pi) = \mathbb{E}_{(x_1^*, ..., x_B^*) \sim \pi}[\sum_{t=1}^B \Delta R(f_t | x_t^*)]\]

其中 \(\Delta R(f_t | x) = R(f_{t-1}) - R(f_t)\) 是标注 \(x\)
后模型的期望风险降低。

记 \(r_i = r(x_i)\)，\(\hat{r}_i = \tilde{r}(x_i) - \varepsilon_i\)
为真实残差（不可观测）。

**引理 1**：max-residual 策略 \(\pi_{MR}\) 在 \(B=1\)
时选择：

\[x_{MR}^* = \arg\max_{i \in \mathcal{U}} \hat{r}_i + \varepsilon_i\]

**引理 2**：最优策略 \(\pi^*\) 在 \(B=1\) 时选择：

\[x_{\pi^*}^* = \arg\max_{i \in \mathcal{U}} \mathbb{E}[\Delta R(f | x_i)] = \arg\max_{i \in \mathcal{U}} \int \Delta R(f | x_i) dP_{\varepsilon_i}(\varepsilon_i)\]

**定理**（命题二的正式陈述）：若存在至少一个pair \((i,j)\) 使得
\(\hat{r}_i > \hat{r}_j\) 但
\(\mathbb{E}[\Delta R(f|x_i)] < \mathbb{E}[\Delta R(f|x_j)]\)，则
\(\pi_{MR} \neq \pi^*\)。

**证明**：

步骤 1：建立 \(\Delta R\) 与 \(r\) 的关系。

对平滑损失 \(L(f(x), y)\) 在 \(f_{current}\) 处做 Taylor 展开：

\[\Delta R(f|x) \approx r(x)^2 \cdot \frac{\partial^2 \mathbb{E}[L]}{\partial f^2}\bigg|_{f_{current}} + \sigma_y^2(x)\]

其中 \(\sigma_y^2(x)\) 是标签噪声方差。

步骤 2：噪声 \(\varepsilon\) 引入偏差。

观察到的残差平方
\([\tilde{r}(x)]^2 = [r_{true}(x) + \varepsilon]^2\) 满足：

\[\mathbb{E}[[\tilde{r}(x)]^2 | x] = r_{true}(x)^2 + \sigma_\varepsilon^2(x)\]

当 \(\sigma_\varepsilon^2(x)\) 大时，max-residual
倾向于选择**噪声大的样本而非信息量大的样本**。

步骤 3：构造反例。

假设 \(\mathcal{U} = \{x_1, x_2\}\)： - \(x_1\):
\(r_{true}(x_1) = 0.1\), \(\sigma_\varepsilon^2(x_1) = 0.5\),
\(\tilde{r}(x_1) \approx 0.71\) - \(x_2\):
\(r_{true}(x_2) = 0.5\), \(\sigma_\varepsilon^2(x_2) = 0.01\),
\(\tilde{r}(x_2) \approx 0.50\)

则 max-residual 选择 \(x_1\)，但
\(\mathbb{E}[\Delta R(f|x_1)] \approx 0.01 + \sigma_y^2(x_1) \ll \mathbb{E}[\Delta R(f|x_2)] \approx 0.25 + \sigma_y^2(x_2)\)。

因此 max-residual 是**次优**的。\(\square\)

\paragraph{2.2.4
信息论视角的补充证明}<!-- label: ux4fe1ux606fux8bbaux89c6ux89d2ux7684ux8865ux5145ux8bc1ux660e -->

令 \(I(X; Y | f)\) 为在给定当前模型时，未标注样本 \(X\) 和真实标签 \(Y\)
之间的条件互信息。max-residual 采样最大化的是
\(H[\hat{Y} | f, X] = \mathbb{E}[\ell(\hat{Y}, Y)]\)，而非
\(I(X; Y|f)\)。

由数据处理不等式：

\[I(X; Y | f) \leq H[\hat{Y}|f] - H[\hat{Y}|f, X, Y] + H[Y|f] - H[Y|f, X]\]

高噪声下，\(H[Y|f, X]\) 增大，而 \(I(X; Y|f)\) 减小。max-residual
无法区分''高不确定性源于信息缺失''与''高不确定性源于固有噪声''。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{2.3
命题三：状态条件专家权重优于全局固定权重}<!-- label: ux547dux9898ux4e09ux72b6ux6001ux6761ux4ef6ux4e13ux5bb6ux6743ux91cdux4f18ux4e8eux5168ux5c40ux56faux5b9aux6743ux91cd -->

> **命题陈述**：对于专家融合（ensemble）问题，状态条件权重 \(w_m(x)\)
> 的期望风险不高于任何全局固定权重 \(w_m\)。

**2.3.1 形式化设定**<!-- label: ux5f62ux5f0fux5316ux8bbeux5b9a -->

设 \(M\) 个专家 \(f_1, ..., f_M\)，融合预测为：

\[f_{ens}(x) = \sum_{m=1}^M w_m(x) f_m(x) \quad (状态条件)\]
\[\bar{f}_{ens}(x) = \sum_{m=1}^M \bar{w}_m f_m(x) \quad (全局固定)\]

其中 \(w_m(x) \geq 0\), \(\sum_m w_m(x) = 1\)；\(\bar{w}_m \geq 0\),
\(\sum_m \bar{w}_m = 1\)。

风险为 \(R(f) = \mathbb{E}[\ell(f(X), f^*(X))]\)。

**2.3.2 凸性假设**<!-- label: ux51f8ux6027ux5047ux8bbe -->

损失函数 \(\ell(\cdot, \cdot)\) 对第一个参数是凸的。常见损失（MSE,
交叉熵, Hinge）均满足。

**2.3.3 证明**<!-- label: ux8bc1ux660e-2 -->

**证法 1（利用 Jensen 不等式和条件期望的塔性质）**：

步骤 1：定义状态条件风险差。

对任意固定的全局权重
\(\bar{w} = (\bar{w}_1, ..., \bar{w}_M)\)，全局固定融合的风险为：

\[R(\bar{f}_{ens}) = \mathbb{E}_X\left[\ell\left(\sum_m \bar{w}_m f_m(X), f^*(X)\right)\right]\]

状态条件融合的风险为：

\[R(f_{ens}) = \mathbb{E}_X\left[\ell\left(\sum_m w_m(X) f_m(X), f^*(X)\right)\right]\]

步骤 2：对任意 \(x\)，构造最优状态条件权重。

在给定 \(x\) 时，最优权重
\(w^*(x) = \arg\min_{w \in \Delta^{M-1}} \ell(\sum_m w_m f_m(x), f^*(x))\)。

由于 \(x\) 已知，最优权重可以完美匹配 \(x\)
处的点态最优专家组合，因此对任意单点 \(x\)：

\[\ell\left(\sum_m w_m^*(x) f_m(x), f^*(x)\right) \leq \ell\left(\sum_m \bar{w}_m f_m(x), f^*(x)\right)\]

等号仅当
\(\bar{w} \in \arg\min_{w \in \Delta^{M-1}} \ell(\sum_m w_m f_m(x), f^*(x))\)
时成立。

步骤 3：在分布上取期望。

由于对每个 \(x\) 逐点不等式成立，取期望保序：

\[\mathbb{E}_X\left[\ell\left(\sum_m w_m^*(X) f_m(X), f^*(X)\right)\right] \leq \mathbb{E}_X\left[\ell\left(\sum_m \bar{w}_m f_m(X), f^*(X)\right)\right]\]

即 \(R(f_{ens}^*) \leq R(\bar{f}_{ens})\)。

步骤 4：SCX 的 \(w_m(x)\) 是 \(w^*(x)\) 的近似。

SCX 权重
\(w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(x) \hat{R}_m(s))\)
不一定是 \(w^*(x)\)，但它是基于经验风险的估计。当
\(\hat{R}_m(s) \xrightarrow{p} R_m(s)\) 且 \(\gamma_s(x)\) 是 \(x\)
位于状态 \(s\) 的精确后验概率时，\(w_m(x)\) 将收敛到
\(w_m^*(x)\)。\(\square\)

\paragraph{2.3.4
一个更精细的证明（通过冗余分析）}<!-- label: ux4e00ux4e2aux66f4ux7cbeux7ec6ux7684ux8bc1ux660eux901aux8fc7ux5197ux4f59ux5206ux6790 -->

重新表述风险差：

\[\Delta R = R(\bar{f}_{ens}) - R(f_{ens})\]

利用凸性和 Taylor 展开：

\[\Delta R \geq \mathbb{E}\left[\left\langle \nabla \ell(\bar{f}_{ens}), \sum_m (\bar{w}_m - w_m(X)) f_m(X) \right\rangle\right]\]

记 \(\delta_m(X) = \bar{w}_m - w_m(X)\)，则：

\[\Delta R \geq \sum_m \mathbb{E}[\delta_m(X) \cdot \nabla \ell(\bar{f}_{ens}) \cdot f_m(X)]\]

对全局固定权重，\(\mathbb{E}[\delta_m(X)] = \bar{w}_m - \mathbb{E}[w_m(X)]\)。利用条件期望的塔性质：

\[\Delta R \geq \sum_m \mathbb{E}\left[\delta_m(X) \cdot \mathbb{E}[\nabla \ell(\bar{f}_{ens}) \cdot f_m(X) | X]\right]\]

若状态条件权重 \(w_m(X)\) 与
\(\nabla \ell(\bar{f}_{ens}) \cdot f_m(X)\) 负相关（这正是 SCX
设计目标------降低高损失区域的权重），则 \(\Delta R > 0\)。

\paragraph{2.3.5
极端情况：当状态条件权重退化为全局权重}<!-- label: ux6781ux7aefux60c5ux51b5ux5f53ux72b6ux6001ux6761ux4ef6ux6743ux91cdux9000ux5316ux4e3aux5168ux5c40ux6743ux91cd -->

当
\(\mathcal{S} = \{all\}\)（仅一个状态）时，\(\gamma_s(x) \equiv 1\)，\(w_m(x) = \frac{\exp(-\alpha \hat{R}_m)}{\sum_{m'} \exp(-\alpha \hat{R}_{m'})}\)，此时
\(w_m(x)\) 为常数，命题退化为平凡情况 \(\Delta R = 0\)。

当每个 \(x\)
独立成状态时（\(\mathcal{S} = \mathcal{X}\)），\(\gamma_s(x) = \delta_{x,s}\)，\(w_m(x) = \frac{\exp(-\alpha \hat{R}_m(x))}{\sum_{m'} \exp(-\alpha \hat{R}_{m'}(x))}\)，此时达到理论上界，\(\Delta R\)
最大。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3.
状态空间构造方法}<!-- label: ux72b6ux6001ux7a7aux95f4ux6784ux9020ux65b9ux6cd5 -->

\subsubsection{\texorpdfstring{3.1 嵌入映射
\(\phi: \mathcal{X} \to \mathbb{R}^d\)}{3.1 嵌入映射 \ phi: \ mathcal\{X\} \ to \ mathbb\{R\}\^{}d}}<!-- label: ux5d4cux5165ux6620ux5c04-phi-mathcalx-to-mathbbrd -->

\paragraph{3.1.1
嵌入选择的原则}<!-- label: ux5d4cux5165ux9009ux62e9ux7684ux539fux5219 -->

状态构造的第一步是将原始输入 \(x\) 映射到低维连续空间
\(\mathbb{R}^d\)。选择准则：

1. 
2. 
3. 

\paragraph{3.1.2
候选嵌入方法}<!-- label: ux5019ux9009ux5d4cux5165ux65b9ux6cd5 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
方法
\end{minipage} & \begin{minipage}[b]
维度 \(d\)
\end{minipage} & \begin{minipage}[b]
特性
\end{minipage} & \begin{minipage}[b]
适用场景
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
原始特征 & \(\dim(\mathcal{X})\) & 无信息损失 & \(\mathcal{X}\) 维度低
(\(<100\)) 

PCA & 可调 (\(k\)) & 线性降维，最大方差 & 线性结构数据 

t-SNE & 2-3 & 局部结构保持，全局失真 & 可视化为主 

UMAP & 可调 & 保持局部和全局结构 & 通用 

PaCMAP & 可调 & 平衡局部/全局/频谱 & 高维聚类前处理 

自编码器 & 可调 & 非线性压缩 & 复杂高维输入 

对比学习嵌入 & 可调 & 语义距离保持 & 图像/文本 

专家特征 \([f_1(x),...,f_M(x)]\) & \(M\) & 专家性能的直接表征 &
当专家数量少时 

\end{longtable}

\paragraph{3.1.3
推荐方案：双视图嵌入}<!-- label: ux63a8ux8350ux65b9ux6848ux53ccux89c6ux56feux5d4cux5165 -->

结合原始特征和专家输出：

\[\phi(x) = [\phi_{feat}(x), \phi_{exp}(x)] \in \mathbb{R}^{d_f + d_e}\]

其中 \(\phi_{feat}(x)\)
是原始特征的降维版本，\(\phi_{exp}(x) = [f_1(x), ..., f_M(x)]\)
是专家输出向量。

\subsubsection{3.2
降维方法对比分析}<!-- label: ux964dux7ef4ux65b9ux6cd5ux5bf9ux6bd4ux5206ux6790 -->

\paragraph{3.2.1
PCA（主成分分析）}<!-- label: pcaux4e3bux6210ux5206ux5206ux6790 -->

**目标**：最大化投影后方差
\(\max_{V} tr(V^\top \Sigma V)\)，其中
\(\Sigma = Cov(X)\)。

**代价**：\(O(n d^2 + d^3)\) 或 \(O(n d \log k)\) (随机化 SVD)。

**SCX 适配性**：PCA 保持全局方差，但不保证局部风险同质性。在
\(R_m(x)\) 变化剧烈的区域，PCA 可能将不同风险的区域投影到相邻位置。

**线性限制**：\(R_m(x)\) 对 \(x\) 的函数可能高度非线性，PCA
的线性投影会破坏保真性。

\paragraph{3.2.2 t-SNE (t-distributed Stochastic Neighbor
Embedding)}<!-- label: t-sne-t-distributed-stochastic-neighbor-embedding -->

**目标**：最小化 \(KL(P||Q)\)，其中 \(p_{ij}\)
是高维高斯相似度，\(q_{ij}\) 是低维 t-分布相似度。

\[p_{j|i} = \frac{\exp(-\|x_i - x_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|x_i - x_k\|^2 / 2\sigma_i^2)}, \quad q_{ij} = \frac{(1 + \|y_i - y_j\|^2)^{-1}}{\sum_{k \neq l} (1 + \|y_k - y_l\|^2)^{-1}}\]

**代价**：\(O(n^2)\)，对大 \(n\) 不适用。

**SCX 适配性**： -
优点：局部结构保持极好，适合发现精细的风险模式变化 -
缺点：全局结构失真严重，\(d\) 通常限于 2-3 不利于聚类

\paragraph{3.2.3 UMAP (Uniform Manifold Approximation and
Projection)}<!-- label: umap-uniform-manifold-approximation-and-projection -->

**目标**：最小化模糊集交叉熵 \(CE(F, G)\)，其中 \(F\)
是高维模糊拓扑表示，\(G\) 是低维表示。

**代价**：\(O(n \log n)\)（近似最近邻加速后）。

**SCX 适配性**： - 保持局部和部分全局结构 -
聚类边界清晰，利于后续聚类 - \(d\) 可调至 10-50，提高聚类质量

**推荐**: UMAP 是 SCX 中 \(\phi\) 构建的首选方法。

\paragraph{3.2.4 PaCMAP (Pairwise Controlled Manifold
Approximation)}<!-- label: pacmap-pairwise-controlled-manifold-approximation -->

**目标**：平衡三类力------近邻吸引、中程排斥、远距排斥。

\[Loss = w_{near} \cdot Loss_{near} + w_{mid} \cdot Loss_{mid} + w_{far} \cdot Loss_{far}\]

**SCX 适配性**：PaCMAP 对参数不敏感，聚类鲁棒性优于 UMAP。当 SCX
需要自动化管线时，PaCMAP 减少了调参需求。

\subsubsection{3.3
聚类方法对比分析}<!-- label: ux805aux7c7bux65b9ux6cd5ux5bf9ux6bd4ux5206ux6790 -->

\paragraph{3.3.1
GMM（高斯混合模型）}<!-- label: gmmux9ad8ux65afux6df7ux5408ux6a21ux578b -->

**模型**：

\[P(x) = \sum_{k=1}^K \pi_k \mathcal{N}(x | \mu_k, \Sigma_k)\]

**估计**：EM 算法最大化对数似然。E-step 计算后验责任：

\[\gamma_{ik} = P(z_i = k | x_i) = \frac{\pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k)}{\sum_{j=1}^K \pi_j \mathcal{N}(x_i | \mu_j, \Sigma_j)}\]

**SCX 适配性**： - 天然支持软状态赋值
\(\gamma_s(x) = \gamma_{ik}\)！这是 SCX 中 \(\gamma_s(x)\) 的精确实现 -
协方差矩阵 \(\Sigma_k\) 捕捉状态内部方差 - 适用于凸形状的簇

**局限性**： - 需要指定 \(K\) - 假设高斯分布（不适用于高度非凸簇）
- 高维数据时协方差矩阵估计困难（可通过 \(\Sigma_k = \sigma_k^2 I\)
或对角矩阵简化）

\paragraph{3.3.2 DBSCAN（Density-Based Spatial Clustering of
Applications with
Noise）}<!-- label: dbscandensity-based-spatial-clustering-of-applications-with-noise -->

**核心概念**： -
\(\varepsilon\)-邻域：\(N_\varepsilon(p) = \{q \in D | dist(p,q) \leq \varepsilon\}\)
- 核心点：\(|N_\varepsilon(p)| \geq MinPts\) -
边界点：处于核心点邻域内但自身不是核心点 -
噪声点：既不是核心点也不是边界点

**SCX 适配性**： - 自动识别噪声状态（Noise 分类） - 不需要预指定
\(K\) - 可发现任意形状的簇

**局限性**： - \(\varepsilon\) 和 MinPts 敏感 -
密度变化剧烈的数据效果差 - 边界点 \(\gamma_s(x)\) 是硬赋值（0 或
1），不支持软状态

\paragraph{3.3.3 HDBSCAN (Hierarchical
DBSCAN)}<!-- label: hdbscan-hierarchical-dbscan -->

**改进**：基于层次聚类，消除 \(\varepsilon\) 参数。

1. 
2. 
3. 
4. 

**SCX 适配性**： - 优于 DBSCAN：可处理变密度数据 -
提供样本水平的状态归属概率（通过 \(\lambda\)-稳定性导出） -
获取开箱即用的噪声点检测

**推荐**：对 \(\mathcal{X}\) 空间复杂时，HDBSCAN 是比 GMM
更好的选择。

**3.3.4 Spectral Clustering**<!-- label: spectral-clustering -->

**步骤**： 1. 构建相似度图
\(W_{ij} = \exp(-\|x_i - x_j\|^2 / 2\sigma^2)\) 2. 计算图拉普拉斯
\(L = D - W\) 或归一化拉普拉斯
\(L_{sym} = I - D^{-1/2} W D^{-1/2}\) 3. 取 \(L\) 的 \(K\)
个最小特征向量构成 \(U \in \mathbb{R}^{n \times K}\) 4. 对 \(U\)
的行进行 \(K\)-means

**SCX 适配性**： - 擅长发现非凸簇（环状、螺旋状） -
对专家性能局部分布复杂的场景有效 - 可导出类似软赋值的谱嵌入空间

**局限性**： - \(O(n^3)\) 复杂度（可近似为 \(O(n^2)\)） - \(K\)
需预设 - 对新样本无法直接预测（需要 Nystroem 逼近）

\subsubsection{\texorpdfstring{3.4 软状态赋值
\(\gamma_s(x)\)}{3.4 软状态赋值 \ gamma\_s(x)}}<!-- label: ux8f6fux72b6ux6001ux8d4bux503c-gamma_sx -->

**3.4.1 定义**<!-- label: ux5b9aux4e49 -->

软状态赋值函数 \(\gamma: \mathcal{X} \times \mathcal{S} \to [0,1]\)
满足：

\[\sum_{s \in \mathcal{S}} \gamma_s(x) = 1, \quad \forall x \in \mathcal{X}\]

**3.4.2 实现方式**<!-- label: ux5b9eux73b0ux65b9ux5f0f -->

**方法 1：GMM 后验概率**

\[\gamma_s(x) = \frac{\pi_s \mathcal{N}(\phi(x) | \mu_s, \Sigma_s)}{\sum_{t \in \mathcal{S}} \pi_t \mathcal{N}(\phi(x) | \mu_t, \Sigma_t)}\]

**方法 2：Kernel 加权**

\[\gamma_s(x) = \frac{\kappa(\phi(x), \mu_s)}{\sum_{t \in \mathcal{S}} \kappa(\phi(x), \mu_t)}\]

其中 \(\kappa(x,y) = \exp(-\|x - y\|^2 / 2\sigma^2)\)，\(\mu_s\)
是簇中心。

**方法 3：t-SNE/UMAP 嵌入上的 Softmax**

\[\gamma_s(x) = softmax(-\beta \cdot d(\phi(x), \mu_s))_s\]

其中 \(d\) 是欧氏距离，\(\beta\) 控制软度温度。

**方法 4：KNN 概率**

\[\gamma_s(x) = \frac{|KNN(x) \cap s|}{k}\]

基于 \(\phi(x)\) 的 \(k\) 近邻中属于 \(s\) 的比例。

\paragraph{3.4.3 软 vs
硬赋值的权衡}<!-- label: ux8f6f-vs-ux786cux8d4bux503cux7684ux6743ux8861 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
维度 & 硬赋值 (Hard) & 软赋值 (Soft) 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
风险估计 & 样本量少时方差大 & 借用邻域信息，方差小 

计算 & 快 & 稍慢 

边界处 & 不连续 & 光滑过渡 

理论分析 & 简单 & 需要处理混合分布 

\end{longtable}

SCX 主框架使用软赋值，因为 \(\gamma_s(x)\) 在专家路由
\[w_m(x) \propto \exp(-\alpha \sum_s \gamma_s(x) \hat{R}_m(s))\]
中的使用需要微分连续性。

\subsubsection{3.5
状态粒度选择}<!-- label: ux72b6ux6001ux7c92ux5ea6ux9009ux62e9 -->

**3.5.1 Silhouette Score**<!-- label: silhouette-score -->

对点 \(i\)，其轮廓值为：

\[s_i = \frac{b_i - a_i}{\max(a_i, b_i)}\]

其中 \(a_i\) 是 \(i\) 与同一簇内点的平均距离，\(b_i\)
是与最近的其他簇的平均距离。

整体 silhouette 得分：\(S(K) = \frac{1}{n} \sum_i s_i\)。

**SCX 选择准则**：\(K^* = \arg\max_K S(K)\)。但 silhouette
仅基于几何距离，不考虑风险 \(R_m(s)\) 的内部方差。

\paragraph{3.5.2 Gap Statistic (Tibshirani et al.,
2001)}<!-- label: gap-statistic-tibshirani-et-al.-2001 -->

比较实际数据的聚类紧凑度 \(W_K\) 与零参考分布下的期望值 \(E_n^*[W_K]\)：

\[Gap_n(K) = E_n^*[\log W_K] - \log W_K\]

最优 \(K\) 是使得 \(Gap(K) \geq Gap(K+1) - s_{K+1}\)
的最小值。

**SCX 适配性**：可替换 \(W_K\) 为聚类内风险方差之和
\(\sum_{s \in \mathcal{S}} Var_{x \in s}[R_m(x)]\)。

\paragraph{3.5.3 BIC
(贝叶斯信息准则)}<!-- label: bic-ux8d1dux53f6ux65afux4fe1ux606fux51c6ux5219 -->

\[BIC(K) = -2 \log L + K \cdot \log n\]

SCX 上下文中，\(L\) 是给定状态划分的似然：

\[L = \prod_{i=1}^n \sum_{k=1}^K \pi_k \mathcal{N}(\phi(x_i) | \mu_k, \Sigma_k)\]

\paragraph{3.5.4 特定于 SCX
的粒度选择：状态风险同质性}<!-- label: ux7279ux5b9aux4e8e-scx-ux7684ux7c92ux5ea6ux9009ux62e9ux72b6ux6001ux98ceux9669ux540cux8d28ux6027 -->

定义状态内风险方差：

\[Var_m(s) = \frac{1}{|s|} \sum_{x \in s} (R_m(x) - R_m(s))^2\]

其中 \(R_m(x) = \ell(f_m(x), f^*(x))\) 为点态风险。

总同质性度量：

\[H(K) = \sum_{m=1}^M \sum_{s \in \mathcal{S}} Var_m(s)\]

选择满足 \(H(K+1) - H(K) < \varepsilon\) 的最小 \(K\)（肘部法则）。

\paragraph{3.5.5 推荐的 SCX
粒度选择管线}<!-- label: ux63a8ux8350ux7684-scx-ux7c92ux5ea6ux9009ux62e9ux7ba1ux7ebf -->

\begin{verbatim}
For K in [2, K_max]:
    1. 降维: φ(X) → UMAP(X, d=min(50, n/10))
    2. 聚类: GMM(K) 或 HDBSCAN
    3. 计算:
       - 几何紧致度: Silhouette(K)
       - 风险同质性: H(K)
       - 模型复杂度: BIC(K)
    4. 综合得分: Score(K) = w_s · S(K) + w_h · (1-H_norm(K)) - w_b · BIC_norm(K)
选择 K* = argmax Score(K)
\end{verbatim}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4.
子模块数据流与协调}<!-- label: ux5b50ux6a21ux5757ux6570ux636eux6d41ux4e0eux534fux8c03 -->

#### 4.1 整体架构<!-- label: ux6574ux4f53ux67b6ux6784 -->

SCX 框架由以下子模块构成，形成闭环数据流：

\begin{verbatim}
输入数据 D
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  1. 状态构造引擎 (State Constructor)                 │
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐        │
│  │ 嵌入 φ  │→│ 降维     │→│ 聚类 + γ_s(x) │        │
│  └─────────┘  └─────────┘  └──────────────┘        │
└─────────────────────┬───────────────────────────────┘
                      │ 状态索引 {s, γ_s(x)}
                      ▼
┌─────────────────────────────────────────────────────┐
│  2. 风险评估模块 (Risk Estimator)                    │
│  R̂_m(s) = average loss of expert m on state s      │
│  SCX_m(s) = empirical reliability                   │
│  噪声检测: NoiseScore(x_i)                          │
└─────────────────────┬───────────────────────────────┘
                      │ {R̂_m(s), SCX_m(s), NoiseScore}
                      ▼
┌─────────────────────────────────────────────────────┐
│  3. 数据价值评估器 (Value Assessor)                  │
│  V(s) = r̄(s)·ρ(s)·L(s)·[1-D(s)]·max_m SCX_m(s)    │
│  四分类: Valuable / Redundant / Noisy / Expert-Dep  │
└─────────────────────┬───────────────────────────────┘
                      │ 数据分类标签
                      ▼
┌─────────────────────────────────────────────────────┐
│  4. 动作决策引擎 (Action Engine)                     │
│  A = {acquire, relabel, downweight, discard,        │
│       route, split}                                  │
│  对每个状态 s，选择动作 a ∈ A                        │
└──────────┬──────────┬──────────┬────────────────────┘
           │          │          │
    acquire/relabel  downweight/discard  route/split
           │          │          │
           ▼          ▼          ▼
    标注预算分配    数据清理    专家路由/状态细分
           │          │          │
           └──────────┴──────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  5. 模型更新模块 (Model Updater)                     │
│  重训练 / 微调专家模型                               │
│  更新风险估计 / 状态哈希                              │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
                ┌───────────┐
                │ SCX-压缩  │
                │ (Coreset) │
                └───────────┘
                      │
                      ▼ (返回步骤 1, 闭环迭代)
\end{verbatim}

\subsubsection{4.2
模块间接口契约}<!-- label: ux6a21ux5757ux95f4ux63a5ux53e3ux5951ux7ea6 -->

\paragraph{4.2.1 状态构造引擎 →
风险评估模块}<!-- label: ux72b6ux6001ux6784ux9020ux5f15ux64ce-ux98ceux9669ux8bc4ux4f30ux6a21ux5757 -->

\begin{verbatim}
输入: 原始数据 D = {x_i, y_i, f_m(x_i)}
输出: 
  - 状态映射: state_idx[i] ∈ {1,...,K} (硬) 或 γ_s(x_i) (软)
  - 状态统计: count[s], centroid[s], density[s]
  - 嵌入: φ(x_i) ∈ R^d (可选缓存)
\end{verbatim}

**数据流方向**：单向，状态构造仅在数据新增或状态分裂时触发。

\paragraph{4.2.2 风险评估模块 →
数据价值评估器}<!-- label: ux98ceux9669ux8bc4ux4f30ux6a21ux5757-ux6570ux636eux4ef7ux503cux8bc4ux4f30ux5668 -->

\begin{verbatim}
输入: D, {state_idx}, {f_m(x_i), y_i}
输出:
  - R̂_m(s): K × M 矩阵
  - SCX_m(s): K × M 矩阵
  - NoiseScore[i]: N 维向量
  - C(s): K 维一致性分数
  - N(s): K 维噪声分数
\end{verbatim}

**关键算法**：

\[R_m(s) = \frac{\sum_{x_i \in s} \ell(f_m(x_i), y_i)}{|s|}\]

\[SCX_m(s) = \frac{|\{x_i \in s : \ell(f_m(x_i), y_i) < \tau\}|}{|s|}\]

\[C(s) = 1 - \frac{1}{|s|} \sum_{x_i \in s} \frac{|\ell(f_m(x_i), y_i) - \bar(s)|}{\max \ell - \min \ell}\]

\paragraph{4.2.3 数据价值评估器 →
动作决策引擎}<!-- label: ux6570ux636eux4ef7ux503cux8bc4ux4f30ux5668-ux52a8ux4f5cux51b3ux7b56ux5f15ux64ce -->

\begin{verbatim}
输入: {R̂_m(s)}, {SCX_m(s)}, {NoiseScore}, {C(s)}, {N(s)}
输出:
  - Value[s]: K 维
  - Class[s]: {'V','R','N','E'} 四分类标签
  - confidence[s]: 分类置信度
\end{verbatim}

**四分类规则**：

\begin{verbatim}
if V(s) > τ_v && max_m SCX_m(s) < τ_r:
    → Expert-dependent (E)
elif V(s) > τ_v && D(s) < τ_d:
    → Valuable (V)
elif D(s) > τ_d && N(s) < τ_n:
    → Redundant (R)
elif N(s) > τ_n:
    → Noisy (N)
else:
    → Expert-dependent (E) [catch-all]
\end{verbatim}

阈值 \(\tau_v, \tau_r, \tau_d, \tau_n\) 可由交叉验证或启发式规则确定。

\paragraph{4.2.4 动作决策引擎 →
模型更新模块}<!-- label: ux52a8ux4f5cux51b3ux7b56ux5f15ux64ce-ux6a21ux578bux66f4ux65b0ux6a21ux5757 -->

\begin{verbatim}
动作规范:
  - acquire(s): 请求标注 batch_size 个来自状态 s 的未标注样本
  - relabel(s): 请求对状态 s 的样本重新标注（高噪声状态）
  - downweight(s): 将状态 s 的样本权重设为 w_s < 1
  - discard(s): 清洗状态 s（标记为离群）
  - route(s, m*): 将状态 s 路由到专家 m*
  - split(s): 将状态 s 分裂为两个子状态
\end{verbatim}

每个动作触发模型更新模块的不同子流程。

\paragraph{4.2.5 模型更新模块 → 状态构造引擎
(反馈闭环)}<!-- label: ux6a21ux578bux66f4ux65b0ux6a21ux5757-ux72b6ux6001ux6784ux9020ux5f15ux64ce-ux53cdux9988ux95edux73af -->

\begin{verbatim}
输出:
  - 更新后的 {f_m(x)}, {f_m(x_i)}
  - 状态分裂后的新 centroid 映射
  - SCX-Compress 后的浓缩数据集 D'
\end{verbatim}

\subsubsection{4.3
闭环更新逻辑}<!-- label: ux95edux73afux66f4ux65b0ux903bux8f91 -->

**当新数据到达时**：

1. 
2. 
3. 
4. 
5. 

**当动作触发时**：

- 
- 
- 
- 

\subsubsection{4.4
计算复杂度分析}<!-- label: ux8ba1ux7b97ux590dux6742ux5ea6ux5206ux6790 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
模块 & 初始构建 & 增量更新 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
UMAP 嵌入 & \(O(n \log n)\) & \(O(n_{new} \log n)\) 

GMM 聚类 & \(O(n K d)\) & \(O(K d)\) (E-step only) 

风险估计 & \(O(n M)\) & \(O(n_{new} M)\) 

价值评估 & \(O(K M)\) & \(O(K M)\) 

四分类 & \(O(K)\) & \(O(1)\) 

SCX-Compress & \(O(n \log n)\) & \(O(n_{new} \log K)\) 

\end{longtable}

**总复杂度**：初始构建 \(O(n \log n + n M)\)，增量更新
\(O(n_{new} M)\)，适合流式场景。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. SCX 理论边界<!-- label: scx-ux7406ux8bbaux8fb9ux754c -->

\subsubsection{5.1
收敛边界：风险估计的一致性}<!-- label: ux6536ux655bux8fb9ux754cux98ceux9669ux4f30ux8ba1ux7684ux4e00ux81f4ux6027 -->

给定 \(n_s\) 个来自状态 \(s\) 的独立同分布样本，经验风险
\(\hat{R}_m(s)\) 的收敛速度由 Hoeffding 不等式和 Bernstein 不等式控制。

**5.1.1 有界损失**<!-- label: ux6709ux754cux635fux5931 -->

设 \(\ell \in [0, L]\)，对任意 \(\delta > 0\)，以概率 \(1 - \delta\)：

\[|\hat{R}_m(s) - R_m(s)| \leq L \sqrt{\frac{\log(2/\delta)}{2 n_s}}\]

**5.1.2 亚高斯损失**<!-- label: ux4e9aux9ad8ux65afux635fux5931 -->

若 \(\ell\) 是 \(\sigma\)-亚高斯的（如 MSE 损失在正态误差下），则：

\[P\left(|\hat{R}_m(s) - R_m(s)| \geq t\right) \leq 2 \exp\left(-\frac{n_s t^2}{2\sigma^2}\right)\]

\paragraph{5.1.3
多状态联合边界}<!-- label: ux591aux72b6ux6001ux8054ux5408ux8fb9ux754c -->

对所有 \(K\) 个状态和 \(M\) 个专家应用 Bonferroni 校正，以概率
\(1 - \delta\)：

\[\max_{m,s} |\hat{R}_m(s) - R_m(s)| \leq L \sqrt{\frac{\log(2MK/\delta)}{2 \min_s n_s}}\]

**警告**：当某个状态 \(s\) 的 \(n_s\)
很小时（如样本稀疏状态），该边界失去意义。这是 SCX
的固有局限------**状态划分越细，每个状态内的样本越少，风险估计的方差越大**。

\subsubsection{5.2
泛化边界：状态条件专家路由}<!-- label: ux6cdbux5316ux8fb9ux754cux72b6ux6001ux6761ux4ef6ux4e13ux5bb6ux8defux7531 -->

对状态条件路由
\(m^*(x) = \arg\min_m \sum_s \gamma_s(x) \hat{R}_m(s)\)，其期望风险为：

\[R(m^*) = \mathbb{E}[\ell(f_{m^*(X)}(X), f^*(X))]\]

\paragraph{5.2.1 基于 VC
维的边界}<!-- label: ux57faux4e8e-vc-ux7ef4ux7684ux8fb9ux754c -->

设专家函数类 \(\mathcal{F}_m\) 的 VC 维为 \(d_m\)（二分类）或伪维数为
\(P_(\mathcal{F}_m)\)（回归）。则对任意 \(\delta > 0\)，以概率
\(1 - \delta\)：

\[R(m^*) \leq \hat{R}(m^*) + \tilde{O}\left(\sqrt{\frac{\max_m d_m}{n}} + \sqrt{\frac{K \log M}{n}}\right)\]

其中第二项来自状态选择器的复杂度（\(K\) 个状态中选择最优专家）。

\paragraph{5.2.2
若状态划分也是数据驱动的}<!-- label: ux82e5ux72b6ux6001ux5212ux5206ux4e5fux662fux6570ux636eux9a71ux52a8ux7684 -->

如果状态 \(\mathcal{S}\) 和嵌入 \(\phi\)
是通过数据学习的（通常如此），则需要额外惩罚：

\[R(m^*) \leq \hat{R}(m^*) + \tilde{O}\left(\sqrt{\frac{\max_m d_m + d_ + K \log M}{n}}\right)\]

其中 \(d_\) 是嵌入函数的 Rademacher 复杂度或 VC 维（如 UMAP
的参数自由度）。

#### 5.3 信息论下界<!-- label: ux4fe1ux606fux8bbaux4e0bux754c -->

\paragraph{5.3.1
状态级最坏情况错误率}<!-- label: ux72b6ux6001ux7ea7ux6700ux574fux60c5ux51b5ux9519ux8befux7387 -->

考虑最坏情况分布族 \(\mathcal{P}\)（专家性能随机），任何算法都需要：

\[\inf_{Alg} \sup_{P \in \mathcal{P}} \mathbb{E}[R(Alg) - R^*] \geq \Omega\left(\sqrt{\frac{K M}{n}}\right)\]

当 \(n/K < \log M\) 时，不可能以高概率识别每个状态的最优专家。这为 SCX
设定了一个**必要条件的样本复杂度**------每个状态至少需要
\(O(\log M)\) 个样本来判断最优专家。

\paragraph{5.3.2
最小-最大风险比率}<!-- label: ux6700ux5c0f-ux6700ux5927ux98ceux9669ux6bd4ux7387 -->

定义状态条件路由相对于最优固定专家权重的改进率：

\[\eta(\mathcal{S}) = \frac{R(\bar{f}_{ens}^*) - R(f_{ens}^*)}{R(\bar{f}_{ens}^*)}\]

则 \(\eta(\mathcal{S})\) 的上界受限于状态间的风险异质性：

\[\eta(\mathcal{S}) \leq 1 - \frac{\min_m \sum_s P(s) R_m(s)}{\sum_s P(s) \min_m R_m(s)}\]

当所有状态的最优专家相同时，\(\eta(\mathcal{S}) = 0\)（状态条件路由无改进）。

\subsubsection{5.4
噪声条件下的边界}<!-- label: ux566aux58f0ux6761ux4ef6ux4e0bux7684ux8fb9ux754c -->

\paragraph{5.4.1
噪声分数的统计一致性}<!-- label: ux566aux58f0ux5206ux6570ux7684ux7edfux8ba1ux4e00ux81f4ux6027 -->

噪声分数
\(NoiseScore(x_i) = r_i \cdot \frac{1}{\rho(s_i)+\varepsilon} \cdot [1 - C(s_i)]\)
作为噪声检测器，其 Type-I/II 错误率由以下边界控制：

在 Tsybakov 噪声条件下，存在常数 \(\alpha \geq 0\) 使得：

\[P(false positive) \leq C n_s^{-\frac{1+\alpha}{2+\alpha}}, \quad P(false negative) \leq C' n_s^{-\frac{1+\alpha'}{2+\alpha'}}\]

其中 \(C, C'\) 是取决于 \(\rho(s)\) 和 \(C(s)\) 的常数。

\paragraph{5.4.2
冗余检测的精度}<!-- label: ux5197ux4f59ux68c0ux6d4bux7684ux7cbeux5ea6 -->

D(s) 的估计精度由状态内 pairwise 相似度的 U-statistic 收敛速度控制：

\[|\hat{D}(s) - D(s)| = O_p\left(\frac{1}{\sqrt{n_s}}\right)\]

更精确的 Berry-Esseen 型边界：

\[P\left(\sqrt{n_s} |\hat{D}(s) - D(s)| \geq t\right) \leq 2 \exp\left(-\frac{t^2}{2\sigma_D^2}\right) + O\left(\frac{1}{\sqrt{n_s}}\right)\]

\subsubsection{5.5 状态分裂 vs
合并的互信息权衡}<!-- label: ux72b6ux6001ux5206ux88c2-vs-ux5408ux5e76ux7684ux4e92ux4fe1ux606fux6743ux8861 -->

\paragraph{5.5.1
分裂的信息增益}<!-- label: ux5206ux88c2ux7684ux4fe1ux606fux589eux76ca -->

将状态 \(s\) 分裂为 \(s_1\) 和 \(s_2\) 的信息增益为：

\[\Delta I_{split} = I(S'; R_m) - I(S; R_m)\]

其中 \(S\) 是分裂前的状态变量，\(S'\) 是分裂后的。

若 \(\Delta I_{split} < \log(2)/n\)（每个子状态的样本少于 2
个的等效信息量），则分裂不应执行。

\paragraph{5.5.2
最优状态数的信息论界}<!-- label: ux6700ux4f18ux72b6ux6001ux6570ux7684ux4fe1ux606fux8bbaux754c -->

记 \(R_{gen}(\mathcal{S})\) 为状态划分 \(\mathcal{S}\)
下的期望泛化风险。由率失真理论：

\[R_{gen}(\mathcal{S}) \geq R^* + \exp(-I(S; R_m))\]

其中 \(R^* = \min_{m^*(x)} \mathbb{E}[\ell(f_{m^*(X)}(X), f^*(X))]\)
是已知点态最优专家的极限风险。

因此，状态粒度选择是在两个目标间的权衡： - 减小
\(R_{gen}(\mathcal{S})\)：需要更多状态（高 \(I(S; R_m)\)） -
控制估计方差：需要更大的 \(n_s\)（减少状态）

\subsubsection{5.6
对抗鲁棒性边界}<!-- label: ux5bf9ux6297ux9c81ux68d2ux6027ux8fb9ux754c -->

\paragraph{5.6.1
对抗状态扰动}<!-- label: ux5bf9ux6297ux72b6ux6001ux6270ux52a8 -->

若攻击者可以操纵
\(\gamma_s(x)\)（如通过中毒攻击），则状态条件路由可能被劫持。

在 \(\ell_\infty\)
攻击下，\(\tilde_s(x) = \gamma_s(x) + \delta_s(x)\)，\(\|\delta\|_\infty \leq \varepsilon\)。路由决策的变化上界为：

\[P(m^*(x) \neq \tilde{m}^*(x)) \leq \frac{2\varepsilon}{\min_{s} \gamma_s(x) + \varepsilon}\]

当某个状态的 \(\gamma_s(x)\) 接近 0 时，微扰即可翻转路由。

\paragraph{\texorpdfstring{5.6.2
防御：\(\gamma\)-平滑}{5.6.2 防御：\ gamma-平滑}}<!-- label: ux9632ux5fa1gamma-ux5e73ux6ed1 -->

对 \(\gamma_s(x)\) 施加 \(\ell_1\) 正则化或标签平滑可提高鲁棒性：

\[\tilde_s(x) = \frac{\gamma_s(x) + \lambda/K}{1 + \lambda}\]

对应的路由决策变化概率降至 \(O(\varepsilon/\lambda)\)。

\subsubsection{5.7
计算-统计折衷}<!-- label: ux8ba1ux7b97-ux7edfux8ba1ux6298ux8877 -->

\begin{longtable}[]{@{}lllll@{}}
\toprule\noalign{}
状态数 \(K\) & 统计效率 & 计算代价 & 路由精度 & 适用场景 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(K=1\) & 高（\(n_s=n\)） & 最低 & 低 & 全局专家差异大 

\(K=\sqrt{n}\) & 中等 & 中等 & 中-高 & 通用 

\(K=n/\log n\) & 低（\(n_s=\log n\)） & 最高 & 极高 &
专家性能高度异质 

\end{longtable}

**经验法则**：对 \(n=10^5\) 样本，\(K \in [10, 100]\)
是合理范围，对应 \(n_s \in [10^3, 10^4]\)。

#### 5.8 边界汇总表<!-- label: ux8fb9ux754cux6c47ux603bux8868 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4091}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3182}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
边界类型
\end{minipage} & \begin{minipage}[b]
表达式
\end{minipage} & \begin{minipage}[b]
条件
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
风险估计误差 & \(O(L\sqrt{\log(MK/\delta)/n_})\) & 有界损失,
\(\ell \leq L\) 

路由泛化 & \(\tilde{O}(\sqrt{(d_ + K\log M)/n})\) & VC 维
\(d_\), 状态数 \(K\) 

信息论下界 & \(\Omega(\sqrt{KM/n})\) & 最坏情况分布 

噪声检测 & \(O(n_s^{-(1+\alpha)/(2+\alpha)})\) & Tsybakov 条件
\(\alpha \geq 0\) 

对抗鲁棒性 & \(O(\varepsilon / (\gamma_ + \varepsilon))\) &
\(\ell_\infty\) 攻击 \(\varepsilon\) 

分裂增益 & \(\Delta I_{split} \geq \log(2)/n\) &
最小可检测增益 

率失真极限 & \(R_{gen} \geq R^* + \exp(-I(S;R_m))\) &
任意状态划分 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 附录：符号对照表<!-- label: ux9644ux5f55ux7b26ux53f7ux5bf9ux7167ux8868 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
符号 & 含义 & 定义位置 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(R_m(s)\) & 专家 \(m\) 在状态 \(s\) 上的条件风险 & 1.1 

\(SCX_m(s)\) & SCX 可靠性指标 & 1.5 

\(V(s)\) & 状态 \(s\) 的数据价值 & 1.4 

\(\gamma_s(x)\) & \(x\) 属于状态 \(s\) 的软概率 & 3.4 

\(\bar{r}(s)\) & 状态 \(s\) 的平均残差 & 1.4 

\(\rho(s)\) & 状态 \(s\) 的出现概率 & 1.4 

\(L(s)\) & 状态 \(s\) 的可学习性 & 1.6 

\(C(s)\) & 状态 \(s\) 的内部一致性 & 1.6 

\(N(s)\) & 状态 \(s\) 的噪声分数 & 1.6 

\(D(s)\) & 状态 \(s\) 的冗余度 & 5.4 

\(\phi(x)\) & 输入嵌入映射 & 3.1 

\(\mathcal{S}\) & 状态空间 & 1.3 

\(M\) & 专家数量 & --- 

\(K = |\mathcal{S}|\) & 状态数量 & 3.3 

\(\ell\) & 损失函数 & 1.1 

\(f_m\) & 第 \(m\) 个专家模型 & --- 

\(f^*\) & 真实函数/最优函数 & 1.1 

\end{longtable}