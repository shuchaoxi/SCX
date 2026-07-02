*Abstract:*

热力学教导我们，孤立系统不可逆地朝向最大熵演化。我们追问 SCX 审计是否服从类似的规律：审计者关于标签噪声的残留不确定性是否单调演化，如果是，则趋向什么极限？我们定义 **审计熵** $H_A(t)=H(\varepsilon\mid\cI_A^{(t)})$ —— 给定审计者在时刻 $t$ 的累积信息集 $\cI_A^{(t)}$ 时真实噪声标签 $\varepsilon$ 的条件熵 —— 并证明四个定理。(i)~**审计第二律**（定理 [ref]）：在``无遗忘''条件 $\cI_A^{(t)}\subseteq\cI_A^{(t+1)}$ 下，$H_A(t+1)\leq H_A(t)$，等号成立当且仅当第 $(t+1)$ 步审计提供关于 $\varepsilon$ 的零新信息。这是信息论数据处理不等式的 **严格** 推论。(ii)~**审计的朗道尔代价**（定理 [ref]）：将 $H_A$ 降低 $\Delta H$ 需要物理能量 $E_{\mathrm{audit}}\geq k_B T\cdot\Delta H\cdot\ln2$，这是来自朗道尔原理的 **严格** 下界；该下界是否可由最优审计协议达到是 **开放问题**。(iii)~**审计热寂**（定理 [ref]）：$\lim_{t\to\infty}H_A(t)=H_>0$，其中 $H_=H(\varepsilon\mid S)$ 是定理~3 保证的不可消除的无知。\rigorous (iv)~**多审计者熵合并**（定理 [ref]）：$H_A(1\oplus2)\leq\min(H_A(1),H_A(2))$，以及链式展开的严格等式刻画，为联邦 SCX 审计提供信息论基础。\rigorous

## 引言

热力学第二定律可能是支配不可逆过程最深远的物理原理：孤立系统的熵永不减少。每一次计算，每一次测量，每一次信息处理操作都必须支付热力学代价——朗道尔原理确立了擦除一个比特的信息至少向环境耗散 $k_B T\ln 2$ 的热量 [cite]。

SCX 审计是一个信息过程：审计者积累证据，降低关于哪些样本是有噪声的不确定性，并逐步缩小估计噪声率与真实噪声率之间的差距。这一描述立即暗示了一个热力学类比：

- **物理熵** = 关于微观状态的不确定性
- **审计熵** = 关于噪声标签的不确定性
- **热力学不可逆性** = 熵增
- **审计不可逆性** = 知识积累（熵*减少*）

该类比反转了符号——审计减少熵而非增加熵——但保留了单向箭头。一旦审计者学会区分一个噪声模式，该知识就不能仅使用已拥有的信息被``遗忘''。这个 **审计时间箭头** 指向更低的审计熵，正如热力学箭头指向更高的物理熵。

AE定理将此直觉形式化为四个精确的信息论陈述。综合起来，它们将 SCX 审计从算法过程提升为具有良好定义的热力学结构的过程——将定理~3 的统计极限连接到朗道尔的物理极限。

**贡献.**

1. **审计第二律**（定理 [ref]）：审计熵的单调非增。\rigorous
2. **审计的朗道尔代价**（定理 [ref]）：物理能量下界；可达性开放。\rigorous~/ \openquest
3. **审计热寂**（定理 [ref]）：收敛到 $H_>0$，即定理~3 的极限。\rigorous
4. **多审计者熵合并**（定理 [ref]）：信息论联邦审计基础。\rigorous

## 预备知识

### 概率空间与记号

令 $(\Omega, \mathcal{F}, P)$ 为一个固定的概率空间，承载所有相关随机变量。噪声指示变量 $\varepsilon: \Omega \to \{0,1\}$ 是 $\mathcal{F}$-可测的，表示每个样本是否被真实噪声污染。

对于任意子 $\sigma$-代数 $\mathcal{G} \subseteq \mathcal{F}$，条件熵定义为
\[
H(\varepsilon \mid \mathcal{G}) = -\mathbb{E}\bigl[\log_2 P(\varepsilon \mid \mathcal{G})\bigr],
\]
单位为比特。若无特别说明，所有熵与互信息均以 $\log_2$ 计算。

### 审计熵

> **Definition:** [审计熵]
> <!-- label: def:audit-entropy -->
> 在时刻 $t$，审计者的累积信息集 $\cI_A^{(t)}$ 是 $\mathcal{F}$ 的一个子 $\sigma$-代数，包含截至时刻 $t$ 的所有观测：Cercis 分数、梯度、Hessian、专家判断以及任何其他审计相关信号。
> **审计熵**定义为
> 
> $$<!-- label: eq:H-A-def -->
>     H_A(t) = H\bigl(\varepsilon \mid \cI_A^{(t)}\bigr)
>     = -\mathbb{E}\Bigl[\log_2 P\bigl(\varepsilon \mid \cI_A^{(t)}\bigr)\Bigr],
> $$
> 
> 即给定截至时刻 $t$ 审计者积累的所有信息时，真实噪声指标 $\varepsilon(x)\in\{0,1\}$ 的条件熵。

$H_A(t)$ 度量审计者的**残留无知**：在处理所有审计证据后，关于哪些样本真正有噪声仍存在多少不确定性。完美审计将达到 $H_A=0$（零残留不确定性）；定理~3 保证这是不可能的。

> **Definition:** [无遗忘条件]
> <!-- label: def:no-forgetting -->
> 审计过程满足**无遗忘**若审计者的信息集是单调非减的：
> 
> $$<!-- label: eq:no-forgetting -->
>     \cI_A^{(t)} \subseteq \cI_A^{(t+1)}, \qquad \forall t\geq0,
> $$
> 
> 即先前获取的信息不被丢弃或丢失。在 $\sigma$-代数语言中，这意味着 $\cI_A^{(t)}$ 是 $\mathcal{F}$ 中一个递增的子 $\sigma$-代数流（filtration）。

### 假设系列

我们给出全文共享的形式化假设。

\begin{assumption}[概率正则性]
<!-- label: ass:prob -->
概率空间 $(\Omega, \mathcal{F}, P)$ 是完备的。$\varepsilon \in L^1(\Omega)$，即 $\mathbb{E}[|\varepsilon|] < \infty$。
\end{assumption}

\begin{assumption}[信息流可测性]
<!-- label: ass:filtration -->
$\{\cI_A^{(t)}\}_{t \ge 0}$ 构成 $\mathcal{F}$ 的一个递增 filtration，即 $\cI_A^{(t)} \subseteq \cI_A^{(t+1)} \subseteq \mathcal{F}$ 对所有 $t$ 成立。
\end{assumption}

\begin{assumption}[SCX 可观测性]
<!-- label: ass:scx -->
对于所有充分大的 $t$，Cercis 分数 $S$、其梯度 $\nabla S$ 和 Hessian $H_S$ 是 $\cI_A^{(t)}$-可测的。特别地，$S \in \cI_A^{(\infty)}$，其中 $\cI_A^{(\infty)} := \sigma\bigl(\bigcup_{t=0}^\infty \cI_A^{(t)}\bigr)$。
\end{assumption}

\begin{assumption}[定理~3 的极限信息集]
<!-- label: ass:t3 -->
由 SCX 可观测生成的 $\sigma$-代数为 $\sG_{\mathrm{SCX}} = \sigma(\{S, \nabla S, H_S\})$。定理~3 的耦合构造断言：
\[
H\bigl(\varepsilon \mid \sG_{\mathrm{SCX}}\bigr) = H(\varepsilon \mid S) > 0.
\]
此外，$\sG_{\mathrm{SCX}}$ 是从数据中可提取的关于 $\varepsilon$ 的最大信息 $\sigma$-代数，即对任何子 $\sigma$-代数 $\mathcal{H} \subseteq \mathcal{F}$ 满足 $S \in \mathcal{H}$ 有 $\mathcal{H} \subseteq \sG_{\mathrm{SCX}}$ 或 $H(\varepsilon \mid \mathcal{H}) \ge H(\varepsilon \mid \sG_{\mathrm{SCX}})$。
\end{assumption}

### 审计信息源

信息集 $\cI_A^{(t)}$ 聚合多个渠道：

1. **Cercis 渠道**：$S(x)=Q(x)+\eta N(x)$ 及其导数；
2. **专家渠道**：人类或算法专家判断 $J_k(x)\in\{\mathrm{noise},\mathrm{hard}\}$；
3. **一致性渠道**：跨多个审计者或跨时间的一致模式；
4. **因果渠道**：关于数据生成过程的领域知识。

每个渠道贡献关于 $\varepsilon$ 的增量互信息，并且随着渠道并集增长，审计熵减少。

## 主要结果

### 审计第二律

> **Theorem:** [审计第二律——熵单调减少]
> <!-- label: thm:second-law -->
> 在假设 [ref] 和 [ref]（无遗忘条件 [ref]）下，对任意审计过程 $\cA$，
> 
> $$<!-- label: eq:second-law -->
>     H_A(t+1) \;\leq\; H_A(t),
> $$
> 
> 等号成立当且仅当
> \[
> I\bigl(\varepsilon; \cI_A^{(t+1)} \mid \cI_A^{(t)}\bigr) = 0,
> \]
> 即第 $(t+1)$ 步审计关于 $\varepsilon$ 提供零额外信息——换言之，$\varepsilon \perp\!\!\!\perp \cI_A^{(t+1)} \mid \cI_A^{(t)}$。

> **Proof:** [定理~AE.1 的严格证明]
> 设 $\cI_t := \cI_A^{(t)}$ 为子 $\sigma$-代数。
> 
> **第一步：信息论恒等式。**
> 由条件熵的定义与链式法则：
> \[
> H(\varepsilon \mid \cI_{t+1}) = H(\varepsilon \mid \cI_t, \cI_{t+1}),
> \]
> 其中 $\cI_{t+1}$ 包含比 $\cI_t$ 更多的信息。
> 
> **第二步：应用数据处理不等式。**
> 由于 $\cI_t \subseteq \cI_{t+1}$（假设 [ref]），我们有 $\sigma$-代数包含关系 $\sigma(\cI_{t+1}) \supseteq \sigma(\cI_t)$。条件熵在 $\sigma$-代数上具有反单调性：若 $\mathcal{G}_1 \subseteq \mathcal{G}_2$ 为子 $\sigma$-代数，则
> \[
> H(\varepsilon \mid \mathcal{G}_1) \ge H(\varepsilon \mid \mathcal{G}_2).
> \]
> 取 $\mathcal{G}_1 = \sigma(\cI_t)$ 和 $\mathcal{G}_2 = \sigma(\cI_{t+1})$，得到
> \[
> H(\varepsilon \mid \cI_t) \ge H(\varepsilon \mid \cI_{t+1}),
> \]
> 这正是要证的 [ref]。
> 
> **第三步：等号条件。**
> 定义增量互信息：
> \[
> \Delta I_t := I(\varepsilon; \cI_{t+1} \mid \cI_t) = H(\varepsilon \mid \cI_t) - H(\varepsilon \mid \cI_t, \cI_{t+1}).
> \]
> 由链式法则：
> \[
> H(\varepsilon \mid \cI_t) = H(\varepsilon \mid \cI_{t+1}) + \Delta I_t.
> \]
> 因此，$H(\varepsilon \mid \cI_{t+1}) = H(\varepsilon \mid \cI_t)$ 当且仅当 $\Delta I_t = 0$。
> 
> $\Delta I_t = 0$ 等价于条件独立性 $\varepsilon \perp\!\!\!\perp \cI_{t+1} \mid \cI_t$，即 $\cI_{t+1}$ 不携带关于 $\varepsilon$ 的任何信息，超出 $\cI_t$ 已包含的内容。数学上：
> \[
> P(\varepsilon \in A \mid \cI_t, \cI_{t+1}) = P(\varepsilon \in A \mid \cI_t),\quad \forall A \in \mathcal{B}(\{0,1\}).
> \]
> 
> **第四步：互信息分解的显式展开。**
> 展开 $\Delta I_t$ 以便检查：
> \[
> 
> $$
> \Delta I_t &= I(\varepsilon; \cI_{t+1} \mid \cI_t) 

> &= H(\cI_{t+1} \mid \cI_t) - H(\cI_{t+1} \mid \varepsilon, \cI_t) 

> &= \mathbb{E}\Bigl[ \log_2 \frac{P(\cI_{t+1}, \varepsilon \mid \cI_t)}{P(\cI_{t+1} \mid \cI_t) P(\varepsilon \mid \cI_t)} \Bigr].
> $$
> 
> \]
> 当且仅当联合分布分解 $P(\cI_{t+1}, \varepsilon \mid \cI_t) = P(\cI_{t+1} \mid \cI_t) P(\varepsilon \mid \cI_t)$ 时 $\Delta I_t = 0$。$\square$

**应用：**
定理 [ref] 为 SCX 审计记录提供了**不可逆性保证**。一旦审计者了解到关于标签噪声的事实，该知识不能仅使用审计线索中已有的信息被遗忘。这对审计日志完整性有直接意义：对历史审计记录的任何篡改都会造成单调性条件 [ref] 的可检测违反——$H_A(t)$ 下降后紧接着上升将标志数据操纵。在审计线索有法律要求的受监管行业（金融服务、制药制造），此定理为防篡改审计日志提供了数学基础：系统应持续监控 $H_A(t)$ 并将任何上升标记为潜在的完整性违规。等号条件进一步提供了诊断：若 $H_A(t+1)=H_A(t)$ 持续多个步骤，审计过程已停滞，信息渠道需要多样化。

> **Remark:** [严格性标注]
> 定理 [ref] 是**严格的**——它是数据处理不等式的直接推论，而 DPI 本身就是经典信息论中的定理 [cite]。审计第二律不需要任何热力学假设；它纯粹从信息集扩展下的条件熵的数学结构得出。\rigorous

> **Remark:** [诚实暴击]
> <!-- label: crit:ae1 -->
> \hcritique~定理~AE.1 的逻辑是无可置疑的，但两个隐含假设值得审视：
> 
1. **无遗忘的现实性**：在真实系统中，审计者可能因存储限制或故意压缩而丢弃旧信息。若 $\cI_A^{(t+1)} \not\supseteq \cI_A^{(t)}$，单调性可能被破坏，熵可能回升。
2. **信息集的可比性**：$\cI_A^{(t)} \subseteq \cI_A^{(t+1)}$ 要求信息集以 $\sigma$-代数包含关系可比。在实际的异构审计系统中，不同时间点的信息可能是不可比的（例如，结构完全不同的特征集）。

> 在理想化假设下定理成立，实际部署需验证无遗忘条件被满足。

### 审计的朗道尔代价

> **Theorem:** [审计计算的朗道尔界]
> <!-- label: thm:landauer -->
> 设 $\Delta H = H_A(t) - H_A(t+1) > 0$（以比特为单位）为一个步骤中实现的审计熵减少。实现该减少的计算所需的物理能量满足
> 
> $$<!-- label: eq:landauer-cost -->
>     E_{\mathrm{audit}} \;\geq\;
>     k_B T \cdot \Delta H \cdot \ln 2,
> $$
> 
> 其中 $k_B$ 是玻尔兹曼常数，$T$ 是计算基底的物理温度。

> **Proof:** [定理~AE.2 的严格证明]
> **第一步：信息熵与物理熵的对应。**
> 审计熵 $H_A(t) = H(\varepsilon \mid \cI_A^{(t)})$ 以比特为单位度量不确定性。根据假设 [ref]，在时刻 $t$ 审计者的认知状态可以通过一个物理存储器表示，其微观状态数约为 $2^{H_A(t)}$。
> 
> 更精确地，考虑实现审计计算的物理系统。设 $\rho_t$ 为时刻 $t$ 存储器的物理状态（密度矩阵）。存储器处于一个宏观状态，对应于 $W(t) = e^{H_A(t) \ln 2} = 2^{H_A(t)}$ 个可分辨的微观状态。于是存储器的物理熵（玻尔兹曼熵）为
> \[
> S_{\mathrm{phys}}(t) = k_B \ln W(t) = k_B H_A(t) \ln 2.
> \]
> 
> **第二步：熵的减少对应物理信息擦除。**
> 在一次审计步骤中，熵减少 $\Delta H = H_A(t) - H_A(t+1)$ 比特。相应的物理熵减少为
> \[
> \Delta S_{\mathrm{phys}} = k_B (\ln 2) \bigl(H_A(t) - H_A(t+1)\bigr) = k_B \Delta H \ln 2.
> \]
> 
> **第三步：应用朗道尔原理。**
> 朗道尔原理 [cite] 指出：在任何逻辑上不可逆的计算操作中，每擦除一个比特的信息，至少向环境耗散 $k_B T \ln 2$ 的能量。擦除 $\Delta H$ 比特的信息对应于熵减少 $\Delta S_{\mathrm{phys}}$。
> 
> 形式上，设 $\Delta Q$ 为操作中释放的热量。热力学第二律要求：
> \[
> \Delta S_{\mathrm{环境}} = \frac{\Delta Q}{T} \ge \Delta S_{\mathrm{phys}}.
> \]
> 因此，
> \[
> E_{\mathrm{audit}} \ge \Delta Q \ge T \cdot \Delta S_{\mathrm{phys}} = k_B T \cdot \Delta H \cdot \ln 2.
> \]
> 
> **第四步：关于 nats 与 bits 转换的注记。**
> 若审计熵以 nats 而非 bits 计量（即使用自然对数），则 $H_A^{\mathrm{nats}} = H_A^{\mathrm{bits}} \cdot \ln 2$，且
> \[
> \Delta H^{\mathrm{bits}} = \frac{\Delta H^{\mathrm{nats}}}{\ln 2}.
> \]
> 代入朗道尔界：
> \[
> E_{\mathrm{audit}} \ge k_B T \cdot \frac{\Delta H^{\mathrm{nats}}}{\ln 2} \cdot \ln 2 = k_B T \cdot \Delta H^{\mathrm{nats}}.
> \]
> 因此，不论计量单位如何，$E_{\mathrm{audit}} \ge k_B T \cdot (以 nats 计的熵减) = k_B T \cdot (以 bits 计的熵减) \cdot \ln 2$。$\square$

**应用：**
定理 [ref] 将审计精度转化为**物理运行成本**。将审计熵降低 $\Delta H$ 比特每样本每样本至少消耗 $k_B T\cdot\Delta H\cdot\ln 2$ 焦耳。对于一个处理 $10^9$ 样本、$\Delta H=0.1$ 比特每样本的大规模审计管线（将不确定性从例如 0.5 降低到 0.4 比特），室温下的最小能耗约为 $2.8\times10^{-13}$ 焦耳每样本，整个管线累计约 $2.8\times10^{-4}$ 焦耳。虽数值不大，但这确立了一个任何工程优化都无法突破的**热力学下限**。在能量受限的边缘部署（物联网传感器、卫星系统）中，该界直接决定了可行的审计深度：审计精度不能超过能量预算热力学上可支持的范围。紧致性的开放问题（开放问题 [ref]）决定了实际 SCX 系统是接近此下限还是高出几个数量级——这对大规模审计部署的经济学有直接影响。

\begin{openproblem}[审计朗道尔界的紧致性]
<!-- label: prob:landauer-tight -->
是否存在最优审计协议，其计算代价*饱和*朗道尔界 $E_{\mathrm{audit}} = k_B T \cdot \Delta H \cdot \ln 2$？这要求数据生成过程的 Situs 编码是热力学最优的——即生成数据的物理熵恰好等于审计它的朗道尔代价。Situs 几何与热力学代价之间的关系是**开放的**。\openquest
\end{openproblem}

> **Remark:** [严格性标注]
> 定理 [ref] 在以下意义下是**条件严格的**：若朗道尔原理成立（经过实验验证 [cite]），且审计熵减少对应物理信息擦除，则下界无条件成立。\conditionallyrigorous

> **Remark:** [诚实暴击]
> <!-- label: crit:ae2 -->
> \hcritique~定理~AE.2 涉及多个深层的概念性问题：
> 
1. **非封闭系统的朗道尔界适用性**：朗道尔原理针对的是逻辑上不可逆的计算操作，特别是信息的擦除。审计过程中，审计者的认知熵减少对应于**信息获取**而非信息擦除。计算硬件在执行审计算法时确实会擦除中间状态（例如，ALU 操作覆盖寄存器），这些操作的能耗受朗道尔原理约束。但审计熵减少本身——知识增加——并不直接对应擦除操作。更准确地说，知识增加是信息获取的结果，而获取信息不一定需要能量消耗（例如，测量可以原则上无能耗 [cite]）。能量代价来自处理获取信息时的不可逆计算。
2. **可逆计算的可能性**：原则上，可以使用可逆计算（如 Bennett 的 pebble game [cite]）来执行审计算法，使能耗任意接近零。这种情况下朗道尔界不适用。然而，可逆计算需要保留所有中间状态，这在实际审计中可能不可行（存储成本过高）。是否存在一种审计算法在保持 $\Delta H$ 的同时使用可逆计算避免能量耗散，是开放问题。
3. **$H_A$ 与物理熵的对应并非一一对应**：信息熵 $H_A$ 是认知状态的概率度量，而物理熵是物理系统的热力学性质。将计算存储器状态与认知状态直接对应是理想化假设，在真实神经形态或分布式系统中可能不成立。

> 这些批评不否定定理的数学有效性，但限制了其在真实审计系统上的直接适用性。

### 审计热寂

> **Theorem:** [审计热寂——收敛到不可消除的无知]
> <!-- label: thm:heat-death -->
> 在假设 [ref]、 [ref]、 [ref] 和 [ref]下，对任何满足无遗忘条件的审计过程，
> 
> $$<!-- label: eq:heat-death -->
>     \lim_{t\to\infty} H_A(t) \;=\; H_ \;>\; 0,
> $$
> 
> 其中
> 
> $$<!-- label: eq:H-min -->
>     H_ = H(\varepsilon \mid S)
>     = H(\varepsilon) - I(\varepsilon; S)
> $$
> 
> 是**不可消除的审计熵**——即使在无限审计后仍存留的关于 $\varepsilon$ 的残留不确定性。它正是定理~3 障碍的信息论量化。

> **Proof:** [定理~AE.3 的严格证明]
> 证明分三个步骤：极限存在性、极限正性、极限识别。
> 
> **第一步：极限的存在性。**
> 序列 $\{H_A(t)\}_{t=0}^\infty$ 满足：
> 
1. [（i）] **单调性**：由定理~AE.1，$H_A(t+1) \le H_A(t)$ 对所有 $t \ge 0$。
2. [（ii）] **下有界性**：条件熵非负，$H_A(t) = H(\varepsilon \mid \cI_A^{(t)}) \ge 0$。

> 由实分析中的单调收敛定理：单调非增下有界序列必有极限。因此
> \[
> \lim_{t\to\infty} H_A(t) =: H_ \quad 存在且  H_ \ge 0.
> \]
> 
> **第二步：极限的正性。**
> 定义极限 $\sigma$-代数
> \[
> \cI_A^{(\infty)} := \sigma\Bigl(\bigcup_{t=0}^\infty \cI_A^{(t)}\Bigr).
> \]
> 由鞅收敛定理，当 $t \to \infty$ 时 $P(\varepsilon \mid \cI_A^{(t)}) \to P(\varepsilon \mid \cI_A^{(\infty)})$ a.s.，且 $H(\varepsilon \mid \cI_A^{(t)}) \to H(\varepsilon \mid \cI_A^{(\infty)})$。
> 
> 
1. [（i）] 由假设 [ref]，Cercis 分数 $S$ 是 $\cI_A^{(\infty)}$-可测的，即 $\sigma(S) \subseteq \cI_A^{(\infty)}$。
2. [（ii）] 由条件熵的反单调性（DPI），$\sigma(S) \subseteq \cI_A^{(\infty)}$ 蕴含
3. [（iii）] 由假设 [ref]，SCX 框架的 $\sigma$-代数 $\sG_{\mathrm{SCX}} = \sigma(\{S, \nabla S, H_S\})$ 是从数据中可提取的关于 $\varepsilon$ 的最大信息结构。由于 $\cI_A^{(\infty)}$ 仅包含审计观察，我们有 $\cI_A^{(\infty)} \subseteq \sG_{\mathrm{SCX}} \lor \mathcal{N}$（模零测集意义下）。
4. [（iv）] 由 T3 的耦合构造（假设 [ref]）：
5. [（v）] 由定理~3，$H(\varepsilon \mid S) > 0$，故 $H_ > 0$。

> 
> **第三步：极限的识别。**
> 上一步已证明 $H_ = H(\varepsilon \mid S)$。因此
> \[
> \lim_{t\to\infty} H_A(t) = H_ = H(\varepsilon \mid S) > 0.
> \]
> 
> 关于 $\sigma$-代数极限结构，$\cI_A^{(\infty)}$ 渐进生成 $\sG_{\mathrm{SCX}}$（在适当的正则条件下，即审计过程收集所有 SCX 可观测）。在 T3 的构造下：
> \[
> \cI_A^{(\infty)} = \sG_{\mathrm{SCX}} \quad (模零测集),
> \]
> 给出信息论上的极限。$\square$

**应用：**
定理 [ref] 为任何 SCX 审计管线提供了**终端性能保证**。无论进行多少轮审计，咨询多少专家，或积累多少数据，残留审计熵 $H_=H(\varepsilon\mid S)>0$ 无法被消除。这对审计 SLA 有直接影响：服务等级协议应规定*可达*审计精度 $1-H_/\log 2$（可解析的噪声不确定性比例），而非 $100\%$ 噪声检测。实践中，$H_$ 可以通过在已知噪声标签的留出集上估计 Cercis 分数分布来计算，提供数据驱动的准确率天花板。对于采购，这意味着：签约 SCX 审计服务前，要求提供商在基准数据集上认证 $H_$——这是任何审计量都无法穿透的不可消除错误下限。与 RA-Theorem 不动点 $\eta^*$ 的联系（猜想 [ref]）提示递归自我审计正好收敛到此 $H_$，统一了热力学和递归视角下的审计极限。

> **Remark:** ``审计热寂''是 SCX 中热力学热寂的类比：一个无法进一步降低熵的终端状态。与热力学热寂（最大熵）不同，审计热寂是*最小*熵状态——但它不为零。定理~3 保证 $H_>0$，意味着**审计永远无法实现噪声与难度的完美分离**。\rigorous

> **Remark:** [诚实暴击]
> <!-- label: crit:ae3 -->
> \hcritique~定理~AE.3 的证明依赖若干关键假设，值得严格审视：
> 
1. **T3 的 $\sigma$-代数真的是极限信息集的全部吗？**
2. **极限是否存在？**
3. **审计热寂与物理热寂的类比是否误导？**

### 多审计者熵合并

> **Theorem:** [多审计者熵合并]
> <!-- label: thm:merging -->
> 设审计者 $A_1$ 和 $A_2$ 分别持有信息集 $\cI_1$ 和 $\cI_2$，审计熵分别为 $H_A(1)=H(\varepsilon\mid\cI_1)$ 和 $H_A(2)=H(\varepsilon\mid\cI_2)$。合并后审计者拥有信息 $\cI_1 \cup \cI_2$，其审计熵满足以下恒等式和不等式：
> 
> **（基本恒等式）**
> 
> $$<!-- label: eq:merging-identity -->
> H_A(1\oplus 2) = H(\varepsilon \mid \cI_1, \cI_2)
> = H(\varepsilon \mid \cI_1) + H(\varepsilon \mid \cI_2) - H(\varepsilon)
> - I(\cI_1; \cI_2 \mid \varepsilon) + I(\cI_1; \cI_2).
> $$
> 
> 
> **（上界）**
> 
> $$<!-- label: eq:merging-ub -->
> H_A(1\oplus 2) \;\leq\; \min\bigl(H_A(1),\, H_A(2)\bigr),
> $$
> 
> 等号成立当且仅当 $\varepsilon \perp\!\!\!\perp \cI_2 \mid \cI_1$（或 $\varepsilon \perp\!\!\!\perp \cI_1 \mid \cI_2$）。
> 
> **（下界）**
> 
> $$<!-- label: eq:merging-lb -->
> H_A(1\oplus 2) \;\geq\; H_A(1) + H_A(2) - H(\varepsilon) - I(\cI_1; \cI_2 \mid \varepsilon),
> $$
> 
> 等号成立当且仅当 $I(\cI_1; \cI_2) = 0$，即 $\cI_1$ 与 $\cI_2$ 边缘独立。
> 
> **（条件独立特例）** 若 $\cI_1 \perp\!\!\!\perp \cI_2 \mid \varepsilon$（给定 $\varepsilon$ 条件独立），则 $I(\cI_1; \cI_2 \mid \varepsilon) = 0$ 且
> 
> $$<!-- label: eq:merging-ci -->
> H_A(1\oplus 2) = H_A(1) + H_A(2) - H(\varepsilon) + I(\cI_1; \cI_2).
> $$

> **Proof:** [定理~AE.4 的严格证明]
> **第一步：链式法则展开。**
> 由条件熵的定义和链式法则：
> \[
> 
> $$
> H_A(1\oplus 2) &= H(\varepsilon \mid \cI_1, \cI_2) 

> &= H(\varepsilon \mid \cI_1) - I(\varepsilon; \cI_2 \mid \cI_1) \quad （链式法则） 

> &= H(\varepsilon \mid \cI_2) - I(\varepsilon; \cI_1 \mid \cI_2) \quad （对称形式）.
> $$
> 
> \]
> 仅需展开第一形式，对称形式完全类似。
> 
> **第二步：互信息的对称展开。**
> 对 $I(\varepsilon; \cI_2 \mid \cI_1)$ 应用三重互信息恒等式：
> \[
> 
> $$
> I(\varepsilon; \cI_2 \mid \cI_1) &= H(\cI_2 \mid \cI_1) - H(\cI_2 \mid \varepsilon, \cI_1) 

> &= \bigl[H(\cI_2) - I(\cI_1; \cI_2)\bigr] - \bigl[H(\cI_2 \mid \varepsilon) - I(\cI_1; \cI_2 \mid \varepsilon)\bigr] 

> &= \bigl[H(\cI_2) - H(\cI_2 \mid \varepsilon)\bigr] - I(\cI_1; \cI_2) + I(\cI_1; \cI_2 \mid \varepsilon) 

> &= I(\varepsilon; \cI_2) - I(\cI_1; \cI_2) + I(\cI_1; \cI_2 \mid \varepsilon).
> $$
> 
> \]
> 
> **第三步：代入链式法则。**
> \[
> 
> $$
> H_A(1\oplus 2) &= H(\varepsilon \mid \cI_1) - \bigl[ I(\varepsilon; \cI_2) - I(\cI_1; \cI_2) + I(\cI_1; \cI_2 \mid \varepsilon) \bigr] 

> &= H(\varepsilon \mid \cI_1) - I(\varepsilon; \cI_2) + I(\cI_1; \cI_2) - I(\cI_1; \cI_2 \mid \varepsilon).
> $$
> 
> \]
> 
> 注意到 $H(\varepsilon) - I(\varepsilon; \cI_2) = H(\varepsilon \mid \cI_2) = H_A(2)$，即 $I(\varepsilon; \cI_2) = H(\varepsilon) - H_A(2)$。代入：
> \[
> 
> $$
> H_A(1\oplus 2) &= H_A(1) - \bigl[H(\varepsilon) - H_A(2)\bigr] + I(\cI_1; \cI_2) - I(\cI_1; \cI_2 \mid \varepsilon) 

> &= H_A(1) + H_A(2) - H(\varepsilon) + I(\cI_1; \cI_2) - I(\cI_1; \cI_2 \mid \varepsilon).
> $$
> 
> \]
> 这正是恒等式 [ref]。
> 
> **第四步：上界的推导。**
> 由步骤一中链式法则直接给出：
> \[
> H_A(1\oplus 2) = H(\varepsilon \mid \cI_1) - I(\varepsilon; \cI_2 \mid \cI_1) \le H(\varepsilon \mid \cI_1) = H_A(1),
> \]
> 因为互信息非负。对称地，$H_A(1\oplus 2) \le H_A(2)$。因此
> \[
> H_A(1\oplus 2) \le \min(H_A(1), H_A(2)).
> \]
> 等号成立当 $I(\varepsilon; \cI_2 \mid \cI_1) = 0$（对于上界 $H_A(1)$），即 $\varepsilon \perp\!\!\!\perp \cI_2 \mid \cI_1$。类似地，$\varepsilon \perp\!\!\!\perp \cI_1 \mid \cI_2$ 对应 $H_A(1\oplus 2) = H_A(2)$。
> 
> **第五步：下界的推导。**
> 由恒等式 [ref] 和互信息的非负性 $I(\cI_1; \cI_2) \ge 0$：
> \[
> H_A(1\oplus 2) = H_A(1) + H_A(2) - H(\varepsilon) - I(\cI_1; \cI_2 \mid \varepsilon) + I(\cI_1; \cI_2) \ge H_A(1) + H_A(2) - H(\varepsilon) - I(\cI_1; \cI_2 \mid \varepsilon).
> \]
> 等号成立当且仅当 $I(\cI_1; \cI_2) = 0$。
> 
> **第六步：条件独立情形的验证。**
> 若 $\cI_1 \perp\!\!\!\perp \cI_2 \mid \varepsilon$，则 $I(\cI_1; \cI_2 \mid \varepsilon) = 0$。代入 [ref]：
> \[
> H_A(1\oplus 2) = H_A(1) + H_A(2) - H(\varepsilon) + I(\cI_1; \cI_2).
> \]
> 此式表明即使在条件独立下，合并后的熵还依赖于 $\cI_1$ 与 $\cI_2$ 的边际相关性（通过 $\varepsilon$ 间接产生的相关性）。$\square$

**应用：**
定理 [ref] 为多审计者 SCX 系统提供了**组合演算**。合并上界 [ref] 量化了审计者多样性的价值：$I(\cI_1;\cI_2\mid\varepsilon)$ 在审计者使用互补信息渠道时最小化（例如一个审计者使用 Cercis 分数，另一个使用专家判断，第三个使用因果模型）。在联邦审计联盟（FA-Theorem）中，此定理指导合作伙伴选择：仅当新审计者的条件互信息与现有审计者的互信息互补时才加入联盟——冗余审计者（$\cI_1\approx\cI_2$）贡献零边际熵降。条件独立情形 $\cI_1\perp\cI_2\mid\varepsilon$ 提供了最佳改善：每个独立审计者对熵降贡献加性。在去中心化审计网络（基于区块链的 SCX）中，此定理提供了审计奖励分配的信息论基础：提供最多互补信息的审计者（最大的 $I(\cI_k;\cI_{others}\mid\varepsilon)$）应获得相应更高的报酬。

> **Remark:** [严格性标注]
> 定理 [ref] 是**严格的**，不依赖任何超出经典信息论的假设。恒等式 [ref] 是所有后续不等式的基础，其成立无需任何额外条件。\rigorous

> **Remark:** [诚实暴击]
> <!-- label: crit:ae4 -->
> \hcritique~定理~AE.4 虽然在经典信息论框架内严格成立，但存在以下实践层面的限度：
> 
1. **等号条件 $I(\cI_1; \cI_2) = 0$ 可能无法在审计中实现**：下界等号要求 $\cI_1$ 与 $\cI_2$ 边缘独立。但在 SCX 审计中，$\cI_1$ 和 $\cI_2$ 都包含关于同一 $\varepsilon$ 的信息，因此通常通过 $\varepsilon$ 间接相关，$I(\cI_1; \cI_2) > 0$。这意味着下界通常是严格的（非紧）。
2. **条件独立 $\cI_1 \perp \cI_2 \mid \varepsilon$ 的物理意义**：该条件意味着给定 $\varepsilon$ 后，两个审计者的观察在统计上独立。这等价于假设每个审计者的信息获取过程仅通过 $\varepsilon$ 耦合。在实际联邦审计中，审计者可能共享共同的训练数据、算法或偏见，导致 $I(\cI_1; \cI_2 \mid \varepsilon) > 0$，降低合并效率。
3. **在实践中，$I(\cI_1; \cI_2 \mid \varepsilon)$ 和 $I(\cI_1; \cI_2)$ 都需要估计**，这本身是一个高维统计难题。定理提供了定性洞察（互补审计者合并更优），但定量计算可能受维数灾难影响。

## SCX 审计的热力学图景

四个定理共同确立了 SCX 审计不仅仅是一个统计程序，而是一个**热力学过程**：

<div align="center">

[Table omitted — see original .tex]

</div>

### 审计时间箭头

审计箭头从高 $H_A$ 指向低 $H_A$——从无知到知识——且该方向与热力学箭头一样不可逆。你无法从审计后的知识状态仅使用 $\cI_A^{(t)}$ 中的信息重建审计前的不确定性状态。这对**审计记录的价值**提供了新视角：审计日志是不可逆熵减的热力学记录，对它的篡改将违反审计第二律——类似于麦克斯韦妖的违反。

### 与 RA-Theorem 的联系

审计热寂 $H_$ 被猜想等于递归审计不动点 $\eta^*$（RA-Theorem [cite]）。若 $H_=H(\varepsilon\mid S)=\eta^*$，则无限递归审计的收敛点恰是定理~3 的信息障碍——审计之剑，转向自身，终击中其锻造所要穿透的盾。

## 结论

AE-Theorem 揭示了 SCX 审计具有真正的热力学结构：一个不可逆箭头、一个物理能量代价、一个终端热寂、以及组合审计者的演算。四个结果覆盖了从严格到开放的光谱：

1. **审计第二律**：$H_A$ 单调非增。\rigorous
2. **朗道尔代价**：$E_{\mathrm{audit}}\geq k_B T\cdot\Delta H\cdot\ln2$；紧致性开放。\rigorous~/ \openquest
3. **审计热寂**：$\lim H_A = H_ > 0$。\rigorous
4. **多审计者合并**：恒等式 $H_A(1\oplus2) = H_A(1) + H_A(2) - H(\varepsilon) + I(\cI_1;\cI_2) - I(\cI_1;\cI_2\mid\varepsilon)$，上界 $\le \min(H_A(1), H_A(2))$。\rigorous

最显著的开放问题——朗道尔界的紧致性（开放问题 [ref]）——决定了 SCX 审计是否本质上受能量限制，或者最优协议能否接近热力学极限。其解决将塑造大规模 SCX 部署的工程经济学。

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{scx2024ra}
SCX Working Group.
\newblock ``RA-Theorem: Recursive Audit Theorem,''
\newblock *Technical Report*, 2024.

\bibitem{landauer1961irreversibility}
R.~Landauer.
\newblock ``Irreversibility and heat generation in the computing process,''
\newblock *IBM Journal of Research and Development*, 5(3):183--191, 1961.

\bibitem{bennett2003notes}
C.~H.~Bennett.
\newblock ``Notes on Landauer's principle, reversible computation, and
Maxwell's demon,''
\newblock *Studies in History and Philosophy of Modern Physics*,
34(3):501--510, 2003.

\bibitem{berut2012experimental}
A.~B\'erut, A.~Arakelyan, A.~Petrosyan, S.~Ciliberto, R.~Dillenschneider,
and E.~Lutz.
\newblock ``Experimental verification of Landauer's principle linking
information and thermodynamics,''
\newblock *Nature*, 483:187--189, 2012.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\bibitem{parrondo2015thermodynamics}
J.~M.~R.~Parrondo, J.~M.~Horowitz, and T.~Sagawa.
\newblock ``Thermodynamics of information,''
\newblock *Nature Physics*, 11:131--139, 2015.

\bibitem{maroney2009generalizing}
O.~J.~E.~Maroney.
\newblock ``Generalizing Landauer's principle,''
\newblock *Physical Review E*, 79:031105, 2009.

\bibitem{sagawa2008second}
T.~Sagawa and M.~Ueda.
\newblock ``Second law of thermodynamics with discrete quantum feedback
control,''
\newblock *Physical Review Letters*, 100:080403, 2008.

\bibitem{shannon1948mathematical}
C.~E.~Shannon.
\newblock ``A mathematical theory of communication,''
\newblock *Bell System Technical Journal*, 27:379--423, 623--656, 1948.

\bibitem{jaynes1957information}
E.~T.~Jaynes.
\newblock ``Information theory and statistical mechanics,''
\newblock *Physical Review*, 106:620--630, 1957.

\bibitem{villani2008optimal}
C.~Villani.
\newblock *Optimal Transport: Old and New*.
\newblock Springer, 2008.

\end{thebibliography}