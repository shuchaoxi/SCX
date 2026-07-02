\section{敌对审稿报告：Situs
理论的逐行攻击}<!-- label: ux654cux5bf9ux5ba1ux7a3fux62a5ux544asitus-ux7406ux8bbaux7684ux9010ux884cux653bux51fb -->

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

**审稿人身份**: Annals of Statistics 最苛刻的审稿人

**审稿日期**: 2026-06-29

**审稿对象**: `paper/situs\_theory/main.tex` +
`theory/self\_evolution/ppe\_rigorous\_derivation.md`

**审稿标准**: 不礼貌。不妥协。只要有一个漏洞就不放过。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 〇、总体印象<!-- label: ux603bux4f53ux5370ux8c61 -->

这篇论文声称在一个叫SCX的框架上建立了Situs（物理位置编码）的''严格数学基础''。实际读完三份文档后的结论是：**这篇文章在多个核心定理的证明上存在根本性错误或无法修复的逻辑跳跃。Theorem
2.4.1 的证明是错的------不是不完整，是错的。Theorem 1.3.1
的Lipschitz常数差了约3.5倍。Theorem 2.2.1
的步骤4是一个无法用当前工具填补的鸿沟。Theorem 3'
的''构造性示例''实际上证伪了它声称要证明的命题。以下逐条分解。**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{一、符号一致性：主论文 vs
ppe\_rigorous\_derivation.md}<!-- label: ux4e00ux7b26ux53f7ux4e00ux81f4ux6027ux4e3bux8bbaux6587-vs-ppe_rigorous_derivation.md -->

\subsubsection{1.1
定理编号不一致}<!-- label: ux5b9aux7406ux7f16ux53f7ux4e0dux4e00ux81f4 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1071}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2321}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.5536}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1071}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
位置
\end{minipage} & \begin{minipage}[b]
main.tex 编号
\end{minipage} & \begin{minipage}[b]
ppe\_rigorous\_derivation.md 编号
\end{minipage} & \begin{minipage}[b]
差异
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
学习型PE破坏定理 & 定理4.2 (line 1048) & 定理4.1 (§4.2.3, line 851) &
**编号差1** 

编码不完美度上界 & 命题3.1 (line 864) & 命题3.1 (§3.1.3, line 690) &
一致 

Theorem 2' & Theorem 2' (line 881) & Theorem 2' (§3.2, line 702) &
一致 

\end{longtable}

**攻击**: 定理4.1 vs
定理4.2的编号跳跃意味着论文正文中存在一个''消失的定理4.1''。如果定理4.1是命题4.1（固定PE保持Theorem
3），那为什么命题4.1不叫定理4.1？这不是笔误------这是逻辑链条断裂：命题4.1用了一个平凡的确定性函数论证，不配称为定理；但定理4.2的''破坏性''结果才是真正的定理级贡献。编号混乱暴露了作者自己对贡献重要性的认知混乱。

\subsubsection{1.2
符号命名体系的双重人格}<!-- label: ux7b26ux53f7ux547dux540dux4f53ux7cfbux7684ux53ccux91cdux4ebaux683c -->

论文正文使用 `\{}Situs`,
`\{}Sstates`, `\{}Ppos`,
`\{}PE`,
\texttt{d\_\{\{}pe\}}，ppe\_rigorous\_derivation.md 使用
`PPE`, `\{}mathcal\{S\}`,
`\{}mathcal\{P\}`,
`\{}text\{PE\}`,
\texttt{d\_\{\{}text\{pe\}\}}。论文声称这些编号与
ppe\_rigorous\_derivation.md ``保持一致''（line
1343），但在所有符号上都不同。这不是LaTeX vs
Markdown的格式差异------论文用 `\{}Ppos`
表示位置空间，md用
`\{}mathcal\{P\}`。作者在同一个句子里宣称一致性的同时展示了不一致性。

\subsubsection{1.3 Theorem 2.3.1
的两个版本}<!-- label: theorem-2.3.1-ux7684ux4e24ux4e2aux7248ux672c -->

**论文版** (line 697-701):
\[\delta_s^ \leq \min\!\left(1 - p_{clean, s},\, \sqrt{\frac{1}{2} D_(P_{\PE|S,Y} \| P_{\PE|S})}\right) + \delta_s^{variance}\]

**md版** (line 512-513):
\[\delta_s^{PE} \leq \min\left(1, \sqrt{\frac{1}{2} \cdot I(P; PE(P) \mid S, Y)}\right) + Bernstein 修正项\]

这**不是**同一个上界。第一个用 \(1-p_{clean,s}\) 和 KL
散度（逐点条件），第二个用 \(1\)
和互信息（期望形式）。md版用''Bernstein修正''（暗示\(O(1/M)\)收敛），论文用
\(\delta_s^{variance} = O(1/\sqrt{M})\)（暗示CLT收敛）。两者在有限\(M\)下的缩放律完全不同------一个是\(1/M\)，一个是\(1/\sqrt{M}\)。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{二、假设检验：A1-A6 在 Situs
下还成立吗？}<!-- label: ux4e8cux5047ux8bbeux68c0ux9a8ca1-a6-ux5728-situs-ux4e0bux8fd8ux6210ux7acbux5417 -->

CC审计报告隐含了原始SCX定理的6个核心假设。逐条检查加入Situs后的状态：

\subsubsection{\texorpdfstring{A1: 专家独立性
(\(v_m \indep v_{m'} \mid s\))}{A1: 专家独立性 (v\_m \ indep v\_\{m\textquotesingle\} \ mid s)}}<!-- label: a1-ux4e13ux5bb6ux72ecux7acbux6027-v_m-indep-v_m-mid-s -->

**原始状态**: \(M\)个专家对同一状态原子\(s\)的投票是i.i.d.
Bernoulli。

**加入Situs后**: 所有专家接收相同的增强输入
\(h_i = \phi(s_i) + \PE(p_i)\)。PE项是共享的确定性信号------如果PE携带关于标签的信息，那么所有专家的输入都包含同一条''提示''。这使得专家的条件独立性假设**被削弱**：\(\Cov(v_m, v_{m'} \mid s, p) \neq 0\)。严格地说，Chernoff-Hoeffding
bound要求的是给定状态后的条件独立，现在PE注入了一个所有专家共享的公共信号。**这破坏了i.i.d.假设的严格性。**

攻击严重度:
**中**。在\(M\)很大时，这种共享信号引入的相关性可能使Chernoff界变松一个常数因子（类似于\(\beta\)-mixing修正），但论文没有提及这个问题------它装作Chernoff-Hoeffding的结构''不变''。

\subsubsection{\texorpdfstring{A2: 检测边际为正
(\(\Delta_s > 0\))}{A2: 检测边际为正 (\ Delta\_s \textgreater{} 0)}}<!-- label: a2-ux68c0ux6d4bux8fb9ux9645ux4e3aux6b63-delta_s-0 -->

**原始状态**:
\(\Delta_s = p_{noisy,s} - p_{clean,s} > 0\)。

**加入Situs后**: 需要
\(\Delta_s^ = \Delta_s + \delta_s^ > 0\)。但
\(\delta_s^ \in [-\Delta_s, 1-p_{clean,s}]\)。**Situs可以使检测边际减小**！如果\(\delta_s^ < 0\)且\(|\delta_s^| > \Delta_s\)，则\(\Delta_s^ < 0\)------Situs反转了检测方向。Theorem
2.2.1只给出了存在某个\(s\)和某个PE使\(\delta_s^ > 0\)的充分条件，但**没有排除对其他\(s\)有\(\delta_s^ < 0\)的可能性**。

攻击严重度: **高**。论文中的修正Theorem
1将所有状态的\(\Delta_s\)替换为\(\Delta_s + \delta_s^\)，但\(\delta_s^\)可以是负的。对某些\(s\)，\(\exp(-2M(\Delta_s + \delta_s^)^2)\)可能比\(\exp(-2M\Delta_s^2)\)更大，即\(F_1\)下界**变差**。这不是论文声称的''系统性增强''。

\subsubsection{A3:
状态空间离散性}<!-- label: a3-ux72b6ux6001ux7a7aux95f4ux79bbux6563ux6027 -->

**原始状态**: \(\mathcal{S} = \{s_1, ..., s_N\}\)是有限离散集。

**加入Situs后**: 编码空间
\(\R^d\)是连续的，\(h_i = \phi(s_i) + \PE(p_i)\)在\(\R^d\)中连续变化。即使\(s_i\)是离散的，\(h_i\)也不再是。这意味着状态原子之间的''等价类''不再严格------两个原本映射到同一状态\(s\)的原子，如果它们的物理位置不同，会得到不同的\(h_i\)。这使''按状态\(s\)聚合''的概率\(\rho_s\)的定义变得模糊------原本按状态原子类型聚合，现在需要按\((s, p)\)联合聚合。

攻击严重度:
**低-中**。技术上可修复（在联合空间上定义分布），但论文没有讨论这个微妙之处。

\subsubsection{A4: 有界随机变量
(Chernoff-Hoeffding适用性)}<!-- label: a4-ux6709ux754cux968fux673aux53d8ux91cf-chernoff-hoeffdingux9002ux7528ux6027 -->

**原始状态**: \(v_m \in \{0,1\}\)有界。

**加入Situs后**:
投票仍然在\(\{0,1\}\)中，Chernoff-Hoeffding的适用性不变。这个假设**形式上保持**。但如A1所述，独立性条件被削弱。

攻击严重度: **低**（形式保持，实质被A1牵连）。

\subsubsection{A5-A6:
Bayes错误率和Fano条件}<!-- label: a5-a6-bayesux9519ux8befux7387ux548cfanoux6761ux4ef6 -->

这些涉及原始Theorem 2和Theorem
3的内部构造，在CC审计报告中未显式编号。在Situs下： -
Bayes错误率在增强特征空间中的定义需要额外小心（增强空间引入了连续维度）
- Fano不等式中的\(\log|\Y|\)项不变，但条件熵的计算涉及连续-离散混合

攻击严重度:
**低**。这些是标准信息论的技术细节，可以处理，但论文没有处理。

#### 假设检验结论<!-- label: ux5047ux8bbeux68c0ux9a8cux7ed3ux8bba -->

**论文声称的6个假设中，至少A1（独立性）和A2（正边际）在Situs下被显著影响。论文没有逐条验证这些假设仍然成立就声称Chernoff结构''不变''，这是不诚实的。**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 三、证明完整性：逻辑跳跃、未声明假设、错误推理<!-- label: ux4e09ux8bc1ux660eux5b8cux6574ux6027ux903bux8f91ux8df3ux8dc3ux672aux58f0ux660eux5047ux8bbeux9519ux8befux63a8ux7406 -->

\subsubsection{3.1
定理2.2.1步骤4：贝叶斯最优→实际专家的推广（致命）}<!-- label: ux5b9aux74062.2.1ux6b65ux9aa44ux8d1dux53f6ux65afux6700ux4f18ux5b9eux9645ux4e13ux5bb6ux7684ux63a8ux5e7fux81f4ux547d -->

论文正文 line 659-661： \textgreater{}
步骤4（从贝叶斯最优到实际专家）：假设实际专家一致地逼近贝叶斯最优（从增广特征中提取信息的方向与贝叶斯最优相同），则上述不等号的符号在期望意义下保持。

论文自己标注这是
`{[}启发式{]}`。但这不是启发式------**这是一个无桥的鸿沟**。问题如下：

**(a)**
贝叶斯最优分类器在给定\((s, \PE(p))\)下的行为与任意一个实际训练的神经网络专家\(E_m\)的行为之间，没有任何有限样本的收敛保证。

**(b)**
``一致地逼近贝叶斯最优''意味着什么？如果专家是随机梯度下降训练的神经网络，它们的收敛点是损失景观的某个驻点，不一定是贝叶斯最优。即使是，也是在**总体分布**意义下，不保证对每个特定状态\(s\)的\(\delta_s^\)符号正确。

**(c)**
论文声称\(p_{clean,s}^ \leq p_{clean,s}\)（干净样本上分歧不增加）。贝叶斯最优分类器在获得更多信息后确实不会变得更差（数据处理不等式保证）。但实际专家可能因为PE引入了**虚假相关性**而在干净样本上表现更差------特别是当训练数据有限时，PE可能学到一个碰巧在训练集上有效但在测试集上无效的模式。这个情况下\(p_{clean,s}^ > p_{clean,s}\)，且\(\delta_s^\)可能为负。

**(d)**
整个定理2.2.1的结论------``存在PE和维度使得\(\delta_s^ > 0\)''------如果没有步骤4，只对贝叶斯最优分类器成立。对于实际SCX框架中的神经网络专家，这是一个**未经证实的猜想**。

**判决**:
定理2.2.1是本文最重要的信息论结果（连接了\(I(Y;P|S) > 0\)和检测改进）。去掉步骤4后，它只证明了贝叶斯最优分类器可以从位置信息中受益------这是平凡的。将这个结果用于SCX框架中的实际专家是**逻辑跳跃**。

\subsubsection{3.2
定理2.4.1步骤2：Fano不等式的方向性（致命）}<!-- label: ux5b9aux74062.4.1ux6b65ux9aa42fanoux4e0dux7b49ux5f0fux7684ux65b9ux5411ux6027ux81f4ux547d -->

这是我发现的最严重错误。论文声称Fano给出了\(\delta_s^\)的**下界**。但仔细检查推导：

**步骤1**: Fano不等式标准形式（正确）------
\[H(Y \mid S, \PE(P)) \leq H_2(P_e) + P_e \cdot \log(|\Y| - 1)\]

由此可得（论文line 750-752）：
\[P_e \geq \frac{H(Y \mid S, \PE(P)) - 1}{\log |\Y|}\]

这是正确的**下界**。

**步骤3** (论文line 763-766, md line 601-607):
\[P_e - P_e^ = \frac{H(Y|S) - H(Y|S, \PE(P))}{\log |\Y|} \quad (取Fano的等号)\]

**这是根本性错误。** 逻辑链条是： 1.
\(P_e \geq \frac{H(Y|S)-1}{\log|\Y|}\)（Fano） 2.
\(P_e^ \geq \frac{H(Y|S,\PE(P))-1}{\log|\Y|}\)（Fano） 3.
如果两个不等式都取等号 →
\(P_e - P_e^ = \frac{H(Y|S) - H(Y|S,\PE(P))}{\log|\Y|}\)

但从(1)和(2)的**不等式**到(3)的**等式**，需要 (i)
Fano不等式在两个世界都达到等式，且 (ii) ``两个Fano等式的差 =
错误率的差''。

问题在于： -
Fano不等式只在特定分布上达到等号（噪声均匀分布在错误类别上，且\(H_2(P_e)\)是二值熵），这在一般情况下不成立。
-
更重要的是，即使两个Fano界都达到等号，\(a \geq A\)和\(b \geq B\)**不能推出**
\(a-b = A-B\)。例如\(P_e = 0.5\)（Fano界0.3），\(P_e^ = 0.45\)（Fano界0.25），则\(P_e - P_e^ = 0.05\)但\(\frac{I}{\log|\Y|} = 0.05\)碰巧成立。但也可以\(P_e = 0.5\)（界0.3），\(P_e^ = 0.3\)（界0.15），则\(P_e - P_e^ = 0.2\)但\(\frac{I}{\log|\Y|} = 0.15\)------Fano等式形式给出错误的下界。

md明确标注''近似，取Fano的等号''------**这承认了不是严格推导**。但论文正文中Theorem
2.4.1的陈述没有这个''近似''的限定，它被呈现为一个**定理**，带有`{[}严格{]}`/`{[}启发式{]}`混合标注（步骤1严格，步骤2-3启发式）。

**方向性错误的本质**:
论文试图从Fano的**上界**（条件熵）推出错误率改善的**下界**。Fano不等式是\(H(Y|X) \leq f(P_e)\)的形式，给出的是\(P_e\)的下界。但\(P_e - P_e^\)作为一个差值，不能直接从两个\(P_e\)的下界推导出来------差值的方向不受单个下界的控制。

**正确做法**:
需要的是\(P_e - P_e^\)的**上界**才能用Fano给出任何严格的界。或者使用更强的工具如Fano的逆形式（但这通常需要额外的分布假设）。

**判决**: **Theorem 2.4.1的证明是错的。**
不是不完整，不是启发式------是从不等式推出等式的逻辑谬误。定理陈述中的''下界''一词误导读者以为这是严格的信息论界。实际上它最多是一个启发式猜测。

\subsubsection{3.3
定理2.2.1步骤3的''干净样本分歧不增加''论证}<!-- label: ux5b9aux74062.2.1ux6b65ux9aa43ux7684ux5e72ux51c0ux6837ux672cux5206ux6b67ux4e0dux589eux52a0ux8bbaux8bc1 -->

论文line 655: \textgreater{}
对于干净样本，额外位置信息进一步确认正确标签→分歧概率不增加：\(p_{clean, s}^ \leq p_{clean, s}\)。

这依赖于一个隐含假设：PE的信息与正确标签''一致''而非''冲突''。但： -
PE是从物理位置派生的，物理位置可能与标签有**虚假相关**（在训练分布中相关，但在目标分布中不相关）。
-
PE可能放大专家的某个系统性偏差------如果所有专家都有一个共同的盲点，额外的PE信息可能让它们集体在这个盲点上更自信地错。
-
论文自己承认了这种风险：在§6.3的''一票否决条件''中，F5指出''随机或伪随机构型+有限样本''下，训练集上的\(\delta_s^ > 0\)可能在测试集上变为\(\delta_s^ < 0\)。

**攻击**:
步骤3的论证假设PE提供的信息总是''有益的''------它增加噪声样本的分歧但不增加干净样本的分歧。这等于**假设了结论**：PE以某种方式区分噪声和干净样本。如果PE的信息是纯粹的额外特征（相关性但不因果），它可能以相同的幅度增加两类样本的分歧，导致\(\delta_s^ = 0\)。

\subsubsection{3.4
定理2.5.1：Lipschitz连续性假设的非法使用}<!-- label: ux5b9aux74062.5.1lipschitzux8fdeux7eedux6027ux5047ux8bbeux7684ux975eux6cd5ux4f7fux7528 -->

定理2.5.1声称：
\[|\delta_i^ - \delta_j^| \leq 2 \cdot L_E \cdot L_ \cdot d_(p_i, p_j)\]

证明中使用 (md line 640):
\[|p_{clean, i}^{PPE} - p_{clean, j}^{PPE}| \leq L_E \cdot \|h_i - h_j\|\]

但\(p_{clean, i}^{PPE} = \mathbb{E}[\mathbf{1}[E_m(h_i) \neq y]]\)是**指示函数的期望**。即使\(E_m\)的输出是\(L_E\)-Lipschitz的（在某种意义下），指示函数\(\mathbf{1}[\cdot \neq y]\)是**不连续的**------它在决策边界处跳跃。\(L_E\)-Lipschitz假设通常适用于网络的输出logit或softmax概率，而不是0/1决策的期望。

要这个界成立，需要额外的假设： -
专家的决策边界距离\(h_i\)和\(h_j\)都足够远（margin条件），或者 -
专家输出的是软概率且指示函数的期望恰好是Lipschitz的（这要求专家的预测概率关于输入是Lipschitz的，且阈值交叉的概率为零测集）

论文没有提供这些条件。**这不是技术细节------这是界是否非空（non-vacuous）的关键。**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 四、符号错误：不止一处<!-- label: ux56dbux7b26ux53f7ux9519ux8befux4e0dux6b62ux4e00ux5904 -->

\subsubsection{4.1 CC审计报告中的sign
error（已修正，确认）}<!-- label: ccux5ba1ux8ba1ux62a5ux544aux4e2dux7684sign-errorux5df2ux4feeux6b63ux786eux8ba4 -->

CC审计报告命题2.1的符号确实是错的。其
\(\delta_s^ = (p_{clean}^{PPE} - p_{clean}) - (p_{noisy}^{PPE} - p_{noisy})\)
的物理含义是：当干净样本上的一致性增益超过噪声样本上的''混淆增益''时，编码才有帮助。这与''编码应该增大噪声检测边际''的直觉相反。论文的修正（交换两项的顺序）是正确的。

**但是**：CC审计报告内部的符号本身就是不一致的。§0.2定义\(p_{clean}\)为分歧概率（\(<0.5\)），但§2.3的证明中出现了\(|p_{clean} + p_{noisy} - 1|\)这种把\(p_{clean}\)当一致性概率用的公式。所以CC报告的''sign
error''可能不是单纯的符号反了------而是更深的**符号体系内部分裂**：§0.2和§2.3
用的是完全不同的\(p\)的语义。

论文修正了这个sign
error但**没有指出CC报告内部的符号分裂**------它只是反了一下符号就宣称修正了。实际上CC报告的问题更严重。

\subsubsection{4.2
定理1.3.1：Lipschitz常数的巨大高估（新的推导错误）}<!-- label: ux5b9aux74061.3.1lipschitzux5e38ux6570ux7684ux5de8ux5927ux9ad8ux4f30ux65b0ux7684ux63a8ux5bfcux9519ux8bef -->

这不是符号错误------是量级错误。论文声称：
\[L_^{rot} = 2\sqrt{\alpha^2 + \beta^2 + \gamma^2}\]

实际的Lipschitz常数是\(\max(\alpha, \beta, \gamma)\)。差了约\(2\sqrt{3} \approx 3.46\)倍（当\(\alpha=\beta=\gamma\)时）。

**推导**:
对于\(\mathbf{e}_0 = (1,0,0,1,0,0,...)^T\)（每个旋转平面第一维为1），
\[\|\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})\|^2 = 4\sin^2(\alpha\Delta x/2) + 4\sin^2(\beta\Delta y/2) + 4\sin^2(\gamma\Delta z/2)\]

当\(\|\Delta\mathbf{p}\| \to 0\):
\[\|\PE_{rot}(\mathbf{p}) - \PE_{rot}(\mathbf{q})\| \approx \sqrt{\alpha^2\Delta x^2 + \beta^2\Delta y^2 + \gamma^2\Delta z^2}\]

由Cauchy-Schwarz:
\[\sqrt{\alpha^2\Delta x^2 + \beta^2\Delta y^2 + \gamma^2\Delta z^2} \leq \max(\alpha, \beta, \gamma) \cdot \|\Delta\mathbf{p}\|_2\]

**真正的Lipschitz常数是\(\max(\alpha, \beta, \gamma)\)**，并且这个界是紧的（取\(\Delta\mathbf{p}\)沿最大频率参数的方向）。

论文证明中的错误出在步骤2的三角不等式分解（md line
300-317）。作者正确地得到了：
\[\|\mathbf{R}(\mathbf{p}) - \mathbf{R}(\mathbf{q})\|_F \leq 2\alpha|\Delta x| + 2\beta|\Delta y| + 2\gamma|\Delta z|\]

但三个差分矩阵作用于**互不相交的子空间**上（维度对(0,1), (2,3),
(4,5)）。对于互不相交子空间上的矩阵和\(D = D_x + D_y + D_z\)：
\[\|D\|_F^2 = \|D_x\|_F^2 + \|D_y\|_F^2 + \|D_z\|_F^2\]

而三角不等式 \(\|D\|_F \leq \|D_x\|_F + \|D_y\|_F + \|D_z\|_F\)
在最坏情况下可以松\(\sqrt{3}\)倍（三个等范数项）。然后作者又通过Cauchy-Schwarz引入了另一个\(\sqrt{3}\)倍的松弛（\(\ell_1 \to \ell_2\)转换）。

**两个松弛相乘导致最终常数高出约3.46倍**。更糟的是，作者注意到了这个问题（注记1.3.1/md
note
1.3.1承认单方向的有效常数只是\(\alpha\)而非\(2\alpha\)），但仍然把松的界作为''精确常数''写进定理陈述。

**判决**:
定理1.3.1声称的''精确Lipschitz常数''既不精确也不紧。真正的精确Lipschitz常数（取\(\|\cdot\|_2\)向量范数和\(\|\cdot\|_2\)位置范数）是\(\max(\alpha, \beta, \gamma)\)。

\subsubsection{4.3
定理1.2.1中缺失的归一化因子}<!-- label: ux5b9aux74061.2.1ux4e2dux7f3aux5931ux7684ux5f52ux4e00ux5316ux56e0ux5b50 -->

编码核的定义（定义1.2.1）是：
\[\langle \PE_{scalar}(p), \PE_{scalar}(q) \rangle = \sum_{j=0}^{d/2-1} \cos(2\pi(p-q)/\lambda_j) = K_(\Delta)\]

在\(\Delta = 0\)处，\(K_(0) = d/2\)。而目标核\(k(0) = 1\)。

当\(d \to \infty\)，编码核**发散**至无穷而非收敛到目标核。要使编码核逼近目标核，必须归一化：
\[\frac{2}{d} K_(\Delta) \to \int_0^\infty S(\omega)\cos(\omega\Delta)d\omega = k(\Delta)\]

但定理1.2.1的陈述和证明**完全没有**提到这个\(2/d\)因子。定理中''编码核在\(L^2([0,L])\)中最优逼近\(k(\Delta)\)``的陈述在数学上是错误的------\(K_\)和\(k\)的量级不同（\(O(d)\)
vs \(O(1)\)）。

\subsubsection{4.4 定理2.3.1
Pinsker应用的合法性问题}<!-- label: ux5b9aux74062.3.1-pinskerux5e94ux7528ux7684ux5408ux6cd5ux6027ux95eeux9898 -->

定理2.3.1使用Pinsker不等式将\(\delta_s^\)与KL散度联系起来。但Pinsker不等式的使用有一个微妙的问题：

Pinsker
bound是：\(|P(A) - Q(A)| \leq \sqrt{\frac{1}{2}D_(P\|Q)}\)，其中\(P\)和\(Q\)是**同一可测空间上的概率测度**且\(A\)是该空间中的事件。

论文应用时，\(P\)和\(Q\)是\(\PE(P)\)在给定\(S\)下的条件分布（纯净vs混杂），但被bound的量\(p_{clean,s}^ - p_{clean,s}\)涉及的是**专家的输出事件**，该事件不在\(\PE(P)\)的空间中。

严格来说，正确的论证是：
\[p_{clean,s}^ = \int P(E_m(\phi(s)+z) \neq y) \cdot dP_{\PE(P)|S=s,clean}(z)\]
\[p_{clean,s} = P(E_m(\phi(s)) \neq y)\]

第二个量甚至不涉及\(\PE(P)\)的分布。论文比较了\(p_{clean,s}^\)和\(p_{clean,s}\)，但Pinsker只限制\(\PE(P)\)的分布变化，不直接限制输出概率的变化------除非额外假设专家输出对PE的依赖是Lipschitz的（回到定理2.5.1的问题）。

**不过这可能是可修复的**:
如果我们比较\(p_{clean,s}^\)和\(p_{clean,s}^{avg} = \int P(E_m(\phi(s)+z) \neq y) \cdot dP_{\PE(P)|S=s}(z)\)（即对PE取平均的干净分歧率），Pinsker就可以合法应用。但论文没有做这个分解。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{五、紧致性：声称 tight 但 none are
tight}<!-- label: ux4e94ux7d27ux81f4ux6027ux58f0ux79f0-tight-ux4f46-none-are-tight -->

\subsubsection{5.1
定理1.2.3：标量正弦Lipschitz常数}<!-- label: ux5b9aux74061.2.3ux6807ux91cfux6b63ux5f26lipschitzux5e38ux6570 -->

声称是''紧的''（line 414, md line
203）。每个\((\sin,\cos)\)对的导数的确满足\(\cos^2 + \sin^2 = 1\)对于任意\(p\)恒成立，所以对于任意接近的两个点，这个对的局部变化率确实达到\(\omega_j\)。对于整个向量，所有对在正交子空间中独立作用，所以Lipschitz常数确实是\(\sqrt{\sum_j \omega_j^2 \cdot 2}\)
= 声称的值。**这个bound确实是紧的。**✓

\subsubsection{5.2
定理1.3.1：3D旋转Lipschitz常数}<!-- label: ux5b9aux74061.3.13dux65cbux8f6clipschitzux5e38ux6570 -->

声称是''最坏情况''紧的（line 519, md line
337）。如§4.2所示，**不紧**------高出约3.46倍。真正的紧Lipschitz常数是\(\max(\alpha, \beta, \gamma)\)。✗

\subsubsection{5.3
定理1.2.2：逼近误差界}<!-- label: ux5b9aux74061.2.2ux903cux8fd1ux8befux5deeux754c -->

声称\(O(1/d)\)且常数\(\frac{2\pi^2\xi}{d} \cdot \frac{L} = \frac{2\pi^2 L}{d}\)。**无证明。**
而且\(\xi\)出现在分子和分母中相消，表明常数\(\frac{2\pi^2 L}{d}\)与物理相关长度\(\xi\)无关------这极其可疑。一个核的逼近质量怎么可能与核的宽度无关？

实际推导（我做的）：对区间\([0,L]\)上\(\cos(\omega\Delta)\)的Riemann-Stieltjes和近似，使用分位数采样，误差受被截断的高频分量和最粗的低频分辨率共同控制。当\(d\)固定时，误差应该随\(\xi\)变化------小\(\xi\)（短程相关）意味着高频分量更多，更难逼近。论文声称的常数与\(\xi\)无关在物理上是荒谬的。

#### 5.4 Theorem 2'的界<!-- label: theorem-2ux7684ux754c -->

声称\(F_{1,SCX}^ \leq F_{1,base} + C_F \cdot \sqrt{(\delta + 2\varepsilon_/C_F^2)/2}\)。

注意当\(\varepsilon_ \to I(Y;P|X)\)（完全失败的编码）时：
\[\delta_{PPE} = \delta + \frac{2I(Y;P|X)}{C_F^2}\]

上界比原始Theorem
2松了\(\sqrt{\delta + 2I/C_F^2} / \sqrt\)倍。当\(I(Y;P|X)\)很大（位置有很多信息但编码完全丢失）时，上界可以变得任意松。这当然不是一个''紧''的界------它是一个**非空的但可能非常宽松的**上界。论文没有声称它是紧的（这点诚实），但在摘要中说''修正了弱特征失效上界''暗示了某种精确性，实际上只是在一个已经很松的界上再加了一个正项。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{六、Theorem 3'
的构造性示例：自己打自己的脸}<!-- label: ux516dtheorem-3-ux7684ux6784ux9020ux6027ux793aux4f8bux81eaux5df1ux6253ux81eaux5df1ux7684ux8138 -->

\subsubsection{6.1
示例的宣称与实际的矛盾}<!-- label: ux793aux4f8bux7684ux5ba3ux79f0ux4e0eux5b9eux9645ux7684ux77dbux76fe -->

§4.3（论文line
1096-1137）标题为''构造性最小示例''。这篇''构造性最小示例''展示了什么？

1. 
2. 
3. 
4. 

**这是一个''构造性反例''------它构造了一个学习型PE无法区分的例子，正好证明了Theorem
3的鲁棒性而非其脆弱性！**

\subsubsection{6.2
手一挥的''真正能区分的条件''}<!-- label: ux624bux4e00ux6325ux7684ux771fux6b63ux80fdux533aux5206ux7684ux6761ux4ef6 -->

在证明学习型PE不能区分之后，论文（line 1134-1136）手一挥说：
\textgreater{}
``但是，当辅助损失涉及未观测到的物理量\(Z\)------例如在\(W_A\)中噪声标签导致\(|Z_{pred} - Z_{DFT}|\)较大（物理不一致），而在\(W_B\)中该差异较小（困难但物理一致）------则学习型PE的最优参数在两个世界中出现差异，不可区分性被破坏。''

这**不是构造性证明**------这是口头描述了一个设想中的场景。没有给出\(Z\)的具体定义，没有给出\(\mathcal{L}_{aux}\)的具体形式，没有验证两个世界确实给出不同的最优点。整个§4.3承诺了一个''构造性最小示例''但只交付了一个**空的声称**。

\subsubsection{6.3 对Theorem
3'的最终判决}<!-- label: ux5bf9theorem-3ux7684ux6700ux7ec8ux5224ux51b3 -->

Theorem
3'本身是一个合理的条件化定理陈述（加了前提(A)(B)则保持不可区分性），但：
- 前提(A)不成立时的''可区分性''结论**没有构造性证明支撑** -
``构造性最小示例''实际上是定理的**反例的反例**------即它展示了定理的鲁棒性
-
区分噪声和困难样本的实际机制（多任务学习+物理一致性）没有被形式化、没有被证明、没有被构造

**Theorem 3'的''破坏''部分是一个未被证明的猜想。**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 七、致命缺陷汇总<!-- label: ux4e03ux81f4ux547dux7f3aux9677ux6c47ux603b -->

\subsubsection{致命缺陷 \#1: Theorem 2.4.1 的 Fano
推导}<!-- label: ux81f4ux547dux7f3aux9677-1-theorem-2.4.1-ux7684-fano-ux63a8ux5bfc -->

**性质**: 逻辑错误（不等号方向误用）

**位置**: main.tex §3.4 (line 746-776), md §2.4 (line 557-617)

**具体错误**:
从两个Fano下界推出错误率差的下界。\(a \geq A\)和\(b \geq B\)不能推出\(a-b = A-B\)或\(a-b \geq A-B\)。

**可修复性**:
不可修复。需要完全不同的证明策略。可能的方向是使用强Fano或Fano的逆，但这需要关于分布的具体假设。

**后果**: Theorem
2.4.1（Fano下界）不能被称为定理------它最多是一个启发式估计。

\subsubsection{致命缺陷 \#2: Theorem 1.3.1 的 Lipschitz
常数}<!-- label: ux81f4ux547dux7f3aux9677-2-theorem-1.3.1-ux7684-lipschitz-ux5e38ux6570 -->

**性质**: 常数因子高估约3.46倍

**位置**: main.tex §2.3 (line 483-492), md §1.3.4 (line 269-276)

**具体错误**:
三角不等式+Cauchy-Schwarz的双重松弛在子空间正交的情况下应该简化为直接Frobenius范数计算。

**可修复性**:
可修复。正确的Lipschitz常数是\(\max(\alpha, \beta, \gamma)\)。

**后果**:
定理1.4.1（统一Lipschitz）和定理2.5.1（空间光滑性）都使用了这个高估的常数。空间光滑性界实际上比声称的紧约3.5倍------这是好消息，但说明论文的分析不够精确。

\subsubsection{致命缺陷 \#3: Theorem 2.2.1 的
Bayes→实际专家鸿沟}<!-- label: ux81f4ux547dux7f3aux9677-3-theorem-2.2.1-ux7684-bayesux5b9eux9645ux4e13ux5bb6ux9e3fux6c9f -->

**性质**: 不可桥接的逻辑跳跃

**位置**: main.tex line 659-661, md line 484

**具体错误**:
贝叶斯最优分类器的行为不能推广到实际训练的神经网络专家。没有有限样本保证。

**可修复性**:
可能通过假设专家模型类具有某种一致逼近性质来修补，但这将本质性地改变定理的性质（从信息论变成学习理论）。

**后果**: Theorem
2.2.1（全文最重要的连接定理）在去掉步骤4后退化为：\(I(Y;P|S) > 0\)意味着贝叶斯最优分类器在使用\(P\)信息时表现更好。这是平凡的，不是贡献。

\subsubsection{致命缺陷 \#4: Theorem 1.2.1
缺失归一化因子}<!-- label: ux81f4ux547dux7f3aux9677-4-theorem-1.2.1-ux7f3aux5931ux5f52ux4e00ux5316ux56e0ux5b50 -->

**性质**: 推导遗漏

**位置**: main.tex §2.2.2, md §1.2.2

**具体错误**:
\(K_(0) = d/2\)而\(k(0) = 1\)。不归一化不可能有收敛。

**可修复性**:
可修复。在编码定义中加入\(1/\sqrt{d/2}\)因子或在内积中加入\(2/d\)归一化。但所有后续常数（Lipschitz、误差界）都需要相应调整。

**后果**:
定理1.2.1的''最优逼近''陈述和定理1.2.2的逼近误差界在没有归一化的情况下是错的。

\subsubsection{半致命缺陷 \#5: Theorem 3'
的''破坏''方向无构造性证明}<!-- label: ux534aux81f4ux547dux7f3aux9677-5-theorem-3-ux7684ux7834ux574fux65b9ux5411ux65e0ux6784ux9020ux6027ux8bc1ux660e -->

**性质**: 未被支持的声称

**位置**: main.tex §4.3, md §4.3

**具体错误**: ``构造性最小示例''反而证明了Theorem 3的鲁棒性。

**可修复性**:
需要一个真正展示学习型PE能在观测等价数据上产生不同参数的例子。这要求辅助损失涉及未观测变量------这样的例子是可能存在的，但**没有被构造出来**。

**后果**: Theorem
3'的''若前提(A)不成立''部分目前是一个未被证明的猜想。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 八、附加问题：小但真实<!-- label: ux516bux9644ux52a0ux95eeux9898ux5c0fux4f46ux771fux5b9e -->

\subsubsection{\texorpdfstring{8.1 定理2.3.1中
\(\min(1-p_{clean,s}, ...)\)
的来源不明}{8.1 定理2.3.1中 \ min(1-p\_\{\ text\{clean\},s\}, \ ldots) 的来源不明}}<!-- label: ux5b9aux74062.3.1ux4e2d-min1-p_textcleans-ldots-ux7684ux6765ux6e90ux4e0dux660e -->

为什么上界中有一个\(1-p_{clean,s}\)的项？推导（line
708-719）从Pinsker+三角不等式得到：
\[\delta_s^ \leq \sqrt{\frac{1}{2}D_^{(1)}} + \sqrt{\frac{1}{2}D_^{(2)}}\]

然后突然变成\(\min(1-p_{clean,s}, ...)\)。\(1-p_{clean,s}\)是从哪里冒出来的？它看起来像是\(\delta_s^\)的值域上限（来自\(\delta_s^ \in [-\Delta_s, 1-p_{clean,s}]\)），但值域上限和Pinsker上界取\(\min\)的数学依据是什么？如果Pinsker给了0.3，值域上限给了0.7，为什么上界是0.3而非0.7？这需要论证Pinsker界\(\leq\)值域上限总是成立，或者需要解释为什么Pinsker界和值域上限都构成有效上界。目前这个\(\min\)的引入没有逻辑。

\subsubsection{\texorpdfstring{8.2 定理2.4.1中 \(\log 2\)
的单位歧义}{8.2 定理2.4.1中 \ log 2 的单位歧义}}<!-- label: ux5b9aux74062.4.1ux4e2d-log-2-ux7684ux5355ux4f4dux6b67ux4e49 -->

论文的Fano下界中出现了\(\frac{2\rho I - \log 2}{\log|\Y|}\)。\(I(\cdot;\cdot)\)通常以nat为单位（如果使用自然对数），\(\log 2\)是什么单位？如果统一用nat，\(H_2(P_e) \leq \ln 2\)
nats；如果统一用bit，\(H_2(P_e) \leq 1\)
bit，没有\(\log 2\)。\(\log 2\)的出现表明论文在nats和bits之间切换而没有声明。在信息论论文中这是不可接受的草率。

\subsubsection{8.3
定理1.4.1是纯包装}<!-- label: ux5b9aux74061.4.1ux662fux7eafux5305ux88c5 -->

定理1.4.1将两个Lipschitz常数汇总在一个表格里，声称这是''统一Lipschitz连续性定理''。它没有新的数学内容------它只是定义了两个常数的并集。这不是一个定理，这是一个定义或汇总表。

\subsubsection{8.4
命题3.1（维度-信息权衡）的指数衰减声称}<!-- label: ux547dux98983.1ux7ef4ux5ea6-ux4fe1ux606fux6743ux8861ux7684ux6307ux6570ux8870ux51cfux58f0ux79f0 -->

\[\varepsilon_ \leq I(Y; P \mid X) \cdot \exp(-d/d_0)\]

标注为`{[}启发式{]}`。指数衰减对于解析核（Cauchy）的Fourier级数逼近在某些光滑性条件下成立，但这里逼近的是核\(k(\Delta)\)，而信息丢失\(\varepsilon_\)涉及条件分布\(P_{Y|X,P}\)和编码造成的KL散度。从核逼近误差到信息丢失，中间需要至少两次Pinsker应用和关于\(P_{Y|X,P}\)光滑性的假设。这些假设没有被陈述。指数衰减函数形式\(\exp(-d/d_0)\)是猜测级别的精度。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 九、加分题：CC审计报告内部的额外问题<!-- label: ux4e5dux52a0ux5206ux9898ccux5ba1ux8ba1ux62a5ux544aux5185ux90e8ux7684ux989dux5916ux95eeux9898 -->

虽本次审稿以论文正文和ppe\_rigorous\_derivation.md为主，但CC审计报告中有一个论文没有修正的问题值得指出：

\subsubsection{9.1
CC审计报告命题2.1的检测边际定义内部分裂}<!-- label: ccux5ba1ux8ba1ux62a5ux544aux547dux98982.1ux7684ux68c0ux6d4bux8fb9ux9645ux5b9aux4e49ux5185ux90e8ux5206ux88c2 -->

CC报告§0.2定义 \(p_{clean} < 0.5\)
为分歧概率。但§2.3的证明中突然出现：
\[\Delta_s^{PPE} = |p_{clean,s}^{PPE} - (1 - p_{noisy,s}^{PPE})| = |p_{clean,s}^{PPE} + p_{noisy,s}^{PPE} - 1|\]

如果\(p_{noisy}\)是分歧概率（\(>0.5\)），\(1-p_{noisy}\)是一致性概率（\(<0.5\)），那么\(\Delta = |分歧_{clean} - 一致_{noisy}|\)------这不是检测边际的标准定义。标准定义应该是\(|分歧_{noisy} - 分歧_{clean}|\)。这表明CC报告在§2.3切换了\(p_{noisy}\)的语义（分歧→一致）但没有声明。论文的''修正''只是反了一下\(\delta_s^\)的符号，没有触及这个更深的符号分裂问题。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 十、最终评分<!-- label: ux5341ux6700ux7ec8ux8bc4ux5206 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
维度
\end{minipage} & \begin{minipage}[b]
评分
\end{minipage} & \begin{minipage}[b]
评语
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
问题重要性 & 8/10 & 物理PE与统计PE的区分是真实且重要的问题 

理论野心 & 9/10 & 四个层面上建立严格基础是雄心勃勃的 

定理1.2.1-1.4.1 & 5/10 & 核心思想正确，但1.3.1常数错误，1.2.1缺归一化 

定理2.2.1 & 4/10 & 步骤1-3正确但平凡，步骤4不可桥接 

定理2.3.1 & 5/10 & 方向正确但细节有问题（Pinsker应用、min项来历不明） 

定理2.4.1 & **1/10** & **证明是逻辑错误的，不能被称为定理** 

定理2.5.1 & 4/10 & Lipschitz假设在指示函数上不合法 

Theorem 2' & 7/10 & 信息论定义+代数推导正确，是本文最佳部分 

Theorem 3' & 3/10 & 前提成立时的结论正确但平凡；破坏方向的结论无证明 

诚实度 & 6/10 &
标注了启发式vs严格，但2.4.1标注不够诚实（标了部分严格但它整体是错的） 

**总体** & **4/10** &
**存在一个致命逻辑错误（2.4.1）、一个量级错误（1.3.1）、一个不可桥接的推广（2.2.1步4）。在修正这些之前不适合发表。** 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 十一、如果要修改，最少需要做哪些事？<!-- label: ux5341ux4e00ux5982ux679cux8981ux4feeux6539ux6700ux5c11ux9700ux8981ux505aux54eaux4e9bux4e8b -->

1. 
2. 
3. 
4. 
5. 
6. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*审稿人签字: 不用签。这些问题是客观的。*

*P.S.
这篇论文不是没有价值。编码函数理论（§2）和信息论定义（§3.1-3.2）是扎实的。但Theorem
2.4.1的Fano推导是致命伤------你不能把两个不等号当等号用，然后声称给了下界。Theorem
1.3.1的3.5倍高估表明作者没有充分验证自己推导中的每一步。这些问题在投Annals
of Statistics之前需要修正。目前的状态更适合作为一个技术报告。*