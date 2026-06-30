# SCX 框架数学工具理论根源追溯

> **分析类型**: 完整数学谱系学追溯
> **分析日期**: 2026-06-28
> **覆盖范围**: Theorem 1-5, Proposition 6, Lemma A-F, 自我进化理论
> **严格性**: 每项工具均追溯至原始论文引用, 评估应用忠实度, 识别增量贡献

---

## 目录

1. [Hoeffding 不等式](#1-hoeffding-不等式)
2. [Chernoff 界 / Chernoff 信息](#2-chernoff-界--chernoff-信息)
3. [Fano 不等式](#3-fano-不等式)
4. [Le Cam 方法](#4-le-cam-方法)
5. [Bahadur-Rao 精确渐近](#5-bahadur-rao-精确渐近)
6. [Robbins-Monro 随机逼近](#6-robbins-monro-随机逼近)
7. [Bayesian martingale / Doob 鞅收敛](#7-bayesian-martingale--doob-鞅收敛)
8. [聚类理论 (Pollard 1981, k-means 一致性)](#8-聚类理论-pollard-1981-k-means-一致性)
9. [其他深层连接](#9-其他深层连接)
10. [理论根源树状图](#10-理论根源树状图)

---

## 1. Hoeffding 不等式

### 1.1 原始论文引用

Hoeffding, W. (1963). "Probability inequalities for sums of bounded random variables." *Journal of the American Statistical Association*, 58(301), 13-30.

### 1.2 原始核心定理陈述

**Hoeffding (1963, Theorem 2)**:
设 \(X_1, \dots, X_n\) 为独立随机变量, 满足 \(a_i \leq X_i \leq b_i\) 几乎必然. 记 \(\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i\). 则对任意 \(t > 0\):

\[
\mathbb{P}(\bar{X} - \mathbb{E}[\bar{X}] \geq t) \leq \exp\left(-\frac{2n^2 t^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)
\]

当所有 \(X_i \in [0,1]\) 时, 上界简化为 \(\exp(-2n t^2)\). 不等式对上下尾均成立, 且不需要同分布假设——仅需要独立性.

### 1.3 SCX 中的应用

**位置**:
- Theorem 1, Lemma 2 (FPR 上界): 文件 `01_noise_detection_guarantee.md` 第 2.1 节
- Theorem 1, Lemma 3 (TPR 下界): 同上第 2.2 节
- Theorem 1 主定理: 以 Hoeffding 形式给出 F1 \(\geq 1 - \frac{1}{\eta}\sum_s \rho_s \exp(-2M\Delta_s^2)\)

**Lemma 2 具体应用**:
\[
\mathbb{P}(C > \theta \mid \text{clean}, X \in s) \leq \exp(-2M(\theta - \mu_s)^2)
\]
其中 \(C = \frac{1}{M}\sum_{m=1}^M e_m\), \(e_m \in [0,1]\), 条件独立给定 \(x\), \(\mathbb{E}[C] \leq \mu_s\).

**Lemma 3 具体应用**:
\[
\mathbb{P}(C > \theta \mid \text{noise}, X \in s) \geq 1 - \exp\left(-2M\left(1 - C_{\text{bal}}\cdot\frac{\mu_s}{K-1} - \theta\right)^2\right)
\]

### 1.4 应用忠实度评估

**合法使用**: \(\checkmark\)

1. **独立性条件**: 假设 A2 (清洁条件独立) 保证给定 \(x\) 下 \(\{e_m\}\) 条件独立. 原始 Hoeffding 定理仅要求独立性而非同分布, 因此条件独立足够. A1 (不相交训练集) 提供了 A2 的合理性基础.

2. **有界性条件**: \(e_m \in [0,1]\) 由定义直接满足 (专家错误指示变量). 假设 A3 (有界损失) 是技术性保证.

3. **上尾 vs 下尾**: Lemma 2 使用上尾 (\(\theta > \mu_s\) 时 \(C > \theta\)), 方向正确. Lemma 3 使用下尾 (\(\theta < p_1\) 时 \(C \leq \theta\) 的补事件), 方向也正确.

4. **条件期望的替代**: Lemma 2 中 \(\mathbb{E}[C \mid \text{clean}, x] \leq \mu_s\) 而非等于——Hoeffding 对 \(\mathbb{E}[C]\) 的上界成立, 因为不等式对 \(\mathbb{E}[C]\) 的任意值单调: 若 \(\mathbb{E}[C] \leq \mu_s\), 则 \(\mathbb{P}(C - \mathbb{E}[C] > \theta - \mu_s) \leq \mathbb{P}(C - \mathbb{E}[C] > \theta - \mathbb{E}[C]) \leq \exp(-2M(\theta - \mathbb{E}[C])^2) \leq \exp(-2M(\theta - \mu_s)^2)\). 方向正确.

5. **状态级平均**: 证明中使用了 \(\mathbb{P}(C > \theta \mid \text{clean}, X \in s) \leq \sup_{x \in s} \mathbb{P}(C > \theta \mid \text{clean}, x)\). 这是合法的上界 (但可能不是紧的).

### 1.5 隐式依赖检查

**潜在风险**: 条件独立性假设 A2 在逻辑上来自 A1 (专家在不相交数据上独立训练). 对 Theorem 1, 给定 \(x\) 的条件独立性是 Hoeffding 应用的基础. 但在 Lemma 2 中, Hoeffding 用于条件分布 \(\mathbb{P}(\cdot \mid x)\), 而最终 bound 取 \(\sup_x\)——这一步骤隐含地要求对**每个** \(x\) 条件独立性成立. A5 (状态同质性) 保证 \(\mu_s\) 对所有 \(x \in s\) 是统一上界, 从而使 \(\sup_x\) 操作合理.

**一个重要但隐式的假设**: Lemma 3 对每个噪声标签 \(c\) 应用 Hoeffding, 然后在 \(c\) 上平均. 这要求对每个 \(c\), 在给定 \((x, c)\) 下 \(\{e_m\}\) 条件独立. A6 (平衡误差分布) 在此处用于下界 \(\mathbb{E}[C \mid x, c]\)——没有 A6, 最坏类别可能使 TPR 下界显著放松. SCX 文档正确标识了 A6 的角色, 无隐式依赖.

**结论**: SCX 的 Hoeffding 应用在数学上是合法的. 所有关键条件 (独立、有界、期望上界) 均有显式假设支撑.

### 1.6 SCX 的增量

1. **将 Hoeffding 嵌入多状态框架**: 不仅对单个 Bernoulli 样本应用 Hoeffding, 还通过状态划分 \(S\) 和 union bound 聚合多个状态的指数界. 状态级分离间隙 \(\Delta_s = \min(\theta - \mu_s, 1 - C_{\text{bal}}\mu_s/(K-1) - \theta)\) 是 SCX 的创新概念, 将 Hoeffding 的通用上界转化为依赖状态的指数衰减.

2. **F1 复合**: 将 FPR 和 FNR 的 Hoeffding 界通过 F1 公式组合, 得到一个非平凡的 F1 下界. 这涉及除法和代数操作, 不是直接应用 Hoeffding.

3. **与 Chernoff 形式共存**: Theorem 1 同时给出 Hoeffding 形式和 Chernoff (KL) 形式, 后者更紧. 这种双形式表述在标准教科书之外.

4. **\(C_{\text{bal}}\) 修正**: 在 Hoeffding 界中引入平衡参数 \(C_{\text{bal}}\), 使界适用于非均匀错误分布.\
   这是对原始 Hoeffding 不等式的**参数化扩展**, 而非不等式本身的修改.

---

## 2. Chernoff 界 / Chernoff 信息

### 2.1 原始论文引用

Chernoff, H. (1952). "A measure of asymptotic efficiency for tests of a hypothesis based on the sum of observations." *Annals of Mathematical Statistics*, 23(4), 493-507.

### 2.2 原始核心定义

**Chernoff 信息 (Chernoff, 1952, Definition)**:
对两个概率分布 \(P_0\) 和 \(P_1\), Chernoff 信息定义为:

\[
C(P_0, P_1) = -\min_{\lambda \in [0,1]} \log \left( \int p_0(x)^\lambda p_1(x)^{1-\lambda} d\mu(x) \right)
\]

对 Bernoulli 分布 \(\text{Bern}(p_0), \text{Bern}(p_1)\):

\[
C(\text{Bern}(p_0), \text{Bern}(p_1)) = \text{KL}(\theta^* \| p_0) = \text{KL}(\theta^* \| p_1)
\]

其中 \(\theta^*\) 是满足 \(\text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1)\) 的唯一值.

Chernoff (1952) 的原始定理指出: 在最小化总错误概率的渐近意义下, 最优检验的误差指数由 Chernoff 信息给出.

### 2.3 SCX 中的应用

**位置**:
- Theorem 1, 附录 A (Chernoff 形式): 文件 `01_noise_detection_guarantee.md`
- Theorem 4' (精确常数最小最大最优性): 文件 `exact_constant_minimax.md`
- Lemma C (Chernoff 信息闭式): 文件 `lemma_CD_chernoff_adaptive.md`
- Lemma D (自适应阈值): 同上
- Lemma E (下界): 文件 `lemma_EF_lowerbound_aggregation.md`

**Theorem 4' 核心应用**:
Chernoff 信息 \(\kappa = C(\text{Bern}(p_0), \text{Bern}(p_1))\) 作为 SCX 检测的精确指数速率:

\[
\lim_{M\to\infty} e^{M\kappa}\sqrt{2\pi M}(1 - \text{F1}_{\text{SCX}}(\theta^\dagger)) = \frac{C_{\min}}{\eta}
\]

其中 \(p_0 = \mu_s\), \(p_1 = 1 - C_{\text{bal}}\cdot\mu_s/(K-1)\).

### 2.4 应用忠实度评估

**合法使用**: \(\checkmark\)

1. **Chernoff 信息的定义**: SCX 正确使用 \(\kappa = \text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1)\) 作为 Chernoff 信息. Lemma C 提供了 \(\theta^*\) 的闭式解:
   \[
   \theta^* = \frac{\log\frac{1-p_0}{1-p_1}}{\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}
   \]
   推导正确.

2. **指数最优性**: Chernoff-Stein Lemma 的应用是标准的——它说明 KL 散度是假阳性率固定下假阴性率的最优指数. SCX 正确引用了这一点.

3. **KL 与 Hoeffding 的关系**: SCX 文档正确指出 \(\text{KL}(\theta\|p) \geq 2(\theta-p)^2\) (Pinsker 型不等式), 确认 Chernoff 界总是至少和 Hoeffding 界一样紧.

4. **2026-06-27 KL 方向修正**: 早期版本使用了错误的 KL 方向 \(\text{KL}(1-\theta \| 1 - \mu_s/(K-1))\), 被修正为正确的 \(\text{KL}(\theta \| 1 - C_{\text{bal}}\mu_s/(K-1))\). 修正后的版本正确.

### 2.5 KL 散度与 Chernoff 信息的桥梁

SCX 展示了从简单的 Hoeffding 界到 Chernoff 信息的自然升级路径:

1. **Theorem 1** (Hoeffding 阶段): 使用 \(2\Delta^2\) 作为指数速率.
2. **Theorem 1 Chernoff 附录**: 用 \(\text{KL}(\theta\|p)\) 替代 \(2(\theta-p)^2\).
3. **Theorem 4'**: 在 Chernoff 点 \(\theta^*\) 处, \(\text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1) = \kappa\) 成为精确速率.

这个桥梁是标准的——大偏差理论中的 Cramer 变换建立从 Hoeffding 到 KL 的升级——但 SCX 将其嵌入到 F1 风险的语境中.

### 2.6 SCX 的增量

1. **自适应阈值**: Lemma D 证明最优阈值 \(\theta^\dagger = \theta^* + O(1/M)\) 对 \(\eta\) 敏感. 这个 \(O(1/M)\) 偏移通过指数产生 \(O(1)\) 乘性因子 \(((1-\eta)/\eta)^s\). 这是 SCX 的关键创新——标准 Chernoff 理论通常假设等先验 (\(\eta = 1/2\)), 而 SCX 的阈值自适应地补偿非对称噪声率.

2. **F1 语境下的第二阶渐近**: Chernoff 信息通常用于**总错误概率**的最优性分析. SCX 将其推广到 F1 风险——一个非线性的性能度量. F1 与总错误概率不同 (涉及精度和召回率的调和平均), 因此需要 Lemma B 中的渐近展开.

3. **\(C_{\text{bal}}\) 扩参数化**: Chernoff 信息的参数 \(p_1 = 1 - C_{\text{bal}}\mu_s/(K-1)\) 引入了一个非标准参数结构, 将状态同质性 (A5) 和平衡误差 (A6) 编码到测试问题的信息几何中.

---

## 3. Fano 不等式

### 3.1 原始论文引用

Fano, R. M. (1961). *Transmission of Information: A Statistical Theory of Communications*. MIT Press.

标准教科书表述见 Cover & Thomas (2006). *Elements of Information Theory* (2nd ed.), Section 2.10.

### 3.2 原始核心定理陈述

**Fano 不等式**:
设 \(\hat{X}\) 是对随机变量 \(X\) (取值于集合 \(\mathcal{X}\)) 的估计, 基于观测 \(Y\). 则:

\[
P(\hat{X} \neq X) \geq \frac{H(X \mid Y) - \log 2}{\log |\mathcal{X}|}
\]

等价形式: \(P(\hat{X} \neq X) \geq \frac{H(X) - I(X;Y) - \log 2}{\log |\mathcal{X}|}\).

### 3.3 SCX 中的应用

**位置**:
- Theorem 2 (弱特征失败), Lemma 1: 文件 `02_weak_feature_failure.md` 第 3 节

**应用陈述**:
设 \(\hat{S}\) 是基于 \(\phi(X)\) 的状态估计. 若 \(\phi\) 是 \(\delta\)-弱的 (\(I(\phi; S) \leq \delta\)):

\[
P(\hat{S} \neq S) \geq \frac{H(S) - \delta - \log 2}{\log K}
\]

**推论 (均匀状态)**: 当 \(H(S) \approx \log K\):
\[
P(\hat{S} \neq S) \geq 1 - \frac{\delta + \log 2}{\log K}
\]

### 3.4 应用忠实度评估

**合法使用**: \(\checkmark\)

1. **Fano 不等式标准应用**: 将 \(X = S\), \(Y = \phi(X)\) 代入标准 Fano 不等式. \(I(\phi;S) = \delta\) 由弱特征定义给出. \(|\mathcal{X}| = |\mathcal{S}| = K\).

2. **\(\log 2\) 项**: 标准 Fano 不等式包含 \(\log 2\) 项, 来自二进制熵 \(H_b(1/2) = \log 2\). SCX 正确包含此项.

3. **熵单位**: 所有熵和互信息以 nat 为单位, 一致.

4. **方向**: Fano 不等式给出**下界**——这是正确的方向以建立"不可能性"结果.

### 3.5 多专家设置的合法性

**检查**: Theorem 2 的 Fano 应用未涉及多专家结构——Fano 仅适用于特征 \(\phi\) 和真实状态 \(S\) 之间的关系, 而非直接涉及专家. 这是合理的, 因为 Theorem 2 是关于状态发现 (而非噪声检测) 的信息论下界. 多专家通过 SCX 流水线进入后续步骤 (引理 2 的退化分析), 而非通过 Fano.

### 3.6 SCX 的增量

1. **状态估计误差 → SCX 性能退化**: Fano 下界被链接到 SCX 一致性估计的退化 (引理 2). 这是通过将 \(P(\hat{S} \neq S)\) 转化为 \(\mathbb{E}[|C(\hat{S}) - C(S)|]\) 的界——一个非标准的桥梁, 将信息论下界与具体算法性能定量连接.

2. **与 Pinsker 链的协同**: Fano 提供下界, Pinsker 提供上界 (TV 的传播). 两者共同完成 Theorem 2 的证明: Fano 说明状态估计必然有误差; Pinsker 说明该误差的传播效应. 这种协同是 SCX 的创新, 非任意单一工具的标准应用.

---

## 4. Le Cam 方法

### 4.1 原始论文引用

Le Cam, L. (1973). "Convergence of estimates under dimensionality restrictions." *The Annals of Statistics*, 1(1), 38-53.

更易获取的教科书表述: Tsybakov, A. B. (2009). *Introduction to Nonparametric Estimation*. Springer, Section 2.1-2.4.

### 4.2 原始核心定理陈述

**Le Cam 引理 (两点法)**:
设 \(P_0\) 和 \(P_1\) 为同一可测空间上的概率分布. 对任意检验 \(\psi \in \{0,1\}\):

\[
\mathbb{P}_0(\psi = 1) + \mathbb{P}_1(\psi = 0) \geq 1 - \text{TV}(P_0, P_1)
\]

等价地:

\[
\max\{\mathbb{P}_0(\psi = 1), \mathbb{P}_1(\psi = 0)\} \geq \frac{1 - \text{TV}(P_0, P_1)}{2}
\]

**Le Cam 凸包方法**: 对参数空间 \(\Theta\) 上的 minimax 风险, 可在先验分布上的 Bayes 风险和构造的"最不利"两点之间建立联系.

### 4.3 SCX 中的应用

**位置**:
- Theorem 4 (rate optimality version): 文件 `minimax_lower_bound_v2.md`
- Theorem 4' (exact constant version): 文件 `exact_constant_minimax.md` 第 4 节

**具体应用** (Hellinger 版本, `minimax_lower_bound_v2.md`):

1. 构造两个分布: \(P_0 = \text{Bern}(\mu_s)^{\otimes M}\) (清洁), \(P_1 = \text{Bern}(1-\mu_s)^{\otimes M}\) (噪声, K=2).
2. 计算 Hellinger affinity: \(\rho = 2\sqrt{\mu_s(1-\mu_s)}\).
3. Tensorize: \(\rho_M = \rho^M\).
4. TV-Hellinger: \(\text{TV} \leq H = \sqrt{1-\rho^M}\).
5. Le Cam: \(R(\psi) \geq (1 - \sqrt{1-\rho^M})/2 \geq \rho^M/4\).
6. 在 K=2 下, 得到下界 \(R(\psi) \geq \frac14 (2\sqrt{\mu_s(1-\mu_s)})^M\).

**在 Theorem 4' 中的应用** (由 Lemma E 的 Neyman-Pearson 归约):
- 通过 Neyman-Pearson 引理将任意算法的风险下界归约为 Bayes 检验
- 用 Le Cam 第三引理 + LAN 框架获得第二阶渐近常数

### 4.4 应用忠实度评估

**合法使用**: \(\checkmark\)

1. **Le Cam 两点法标准应用**: 正确构造了两个难以区分的分布 \(P_0\) (清洁) 和 \(P_1\) (噪声). 原始 Le Cam 方法的本质是在两个分布之间建立"最小距离"的下界.

2. **TV → 下界的方向**: Le Cam 引理的正确方向是 \(\max(\alpha, \beta) \geq (1 - \text{TV})/2\). 由于 TV 可能小于 1, 这个下界可能很小, 但方向是**正确的**: 它确实给出了无法被突破的下限.

3. **Hellinger 替代 χ²**: 在 v2 中, 原始的 Slud 不等式 (给出无效上界而非下界) 被替换为 Hellinger 方法. Hellinger 方法的关键优势是其精确 tensorization 性质: \(H^2(P^{\otimes M}, Q^{\otimes M}) = 1 - (1 - H^2(P,Q))^M\). 这是精确等式, 不需要任何不等式近似. 此替换修复了 v1 的致命缺陷.

4. **\(1 - \sqrt{1-x} \geq x/2\)**: 用此不等式将 Le Cam 下界从 \(\frac{1-\sqrt{1-\rho^M}}{2}\) 简化为 \(\rho^M/4\). 方向是**正确的**: 下界被进一步降低 (更保守), 但仍然保持有效.

5. **\(K > 2\) 推广**: v2 正确注意到在 \(C_{\text{bal}} = 1\) 下, \(P_1\) 是所有噪声标签类下的公共分布, 因此 tensorization 对任意 \(K\) 依然精确. 这避免了 v1 中错误的 χ² 方向论证.

### 4.5 Le Cam convex hull 论证的正确性

**检查**: SCX 在 Theorem 4' 中使用了 Neyman-Pearson 归约 (Lemma E), 而非直接 Le Cam convex hull. 这是一条不同的路径:

1. 通过 Neyman-Pearson 引理, 任意检验的加权误差 (\(w_0\alpha + w_1\beta\)) 不低于 Bayes 检验的误差.
2. Bayes 检验的阈值为 \(\tau = (1-\eta)/\eta\).
3. 对该具体检验应用 Bahadur-Rao 精确渐近.

这种归约是标准的, 且避免了 Le Cam convex hull 论证中可能出现的 slack. 它等价于将 minimax 下界问题转化为 Bayes 下界问题, 因为这里的参数空间仅两个点 (清洁 vs 噪声).

**结论**: SCX 的 Le Cam 方法应用是合法的. 从 v1 的 Slud 错误到 v2 的 Hellinger 修正严格正确.

### 4.6 SCX 的增量

1. **Hellinger tensorization 在专家设置中的应用**: 利用 A2 (条件独立) 提供的乘积分布结构, SCX 展示了如何从单专家 Hellinger affinity \(\rho = 2\sqrt{\mu_s(1-\mu_s)}\) 精确推广到多专家 \(\rho^M\). 这在标准 Hellinger 教材之外, 因为其参数 \(p_1 = 1 - C_{\text{bal}}\mu_s/(K-1)\) 不是标准设定.

2. **F1 风险下 Le Cam 的应用**: 标准 Le Cam 应用于简单 0-1 损失或总错误概率. SCX 将 Le Cam 下界转换为 F1 下界需要 Lemma B 中的 F1 渐近展开——这是非平凡的一步.

3. **第二阶渐近的 Neyman-Pearson 路径**: Theorem 4' 不满足于指数层最优性 (Chernoff-Stein), 而是通过 Neyman-Pearson + Bahadur-Rao 达到精确常数. 这超越了标准 Le Cam 方法的能力.

---

## 5. Bahadur-Rao 精确渐近

### 5.1 原始论文引用

Bahadur, R. R., & Rao, R. R. (1960). "On deviations of the sample mean." *Annals of Mathematical Statistics*, 31(4), 1015-1027.

### 5.2 原始核心定理陈述

**Bahadur-Rao 定理 (1960)**:
设 \(X_1, \dots, X_n\) 为 i.i.d. 随机变量, 具有有限矩母函数. 记 \(\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i\), \(\theta > \mathbb{E}[X_1]\). 则当 \(n \to \infty\):

\[
\mathbb{P}(\bar{X}_n \geq \theta) \sim \frac{\exp(-n I(\theta))}{\lambda^*(\theta) \sqrt{2\pi n \cdot \sigma^2(\theta)}}
\]

其中:
- \(I(\theta) = \sup_\lambda \{\lambda\theta - \psi(\lambda)\}\) 为 Cramer 变换 (率函数)
- \(\lambda^*(\theta)\) 为达到上确界的鞍点
- \(\sigma^2(\theta) = \psi''(\lambda^*)\) 为倾斜分布的方差

对 Bernoulli\((p)\), 鞍点 \(\lambda^*(\theta) = \log\frac{\theta(1-p)}{p(1-\theta)}\), 倾斜方差 \(\sigma^2(\theta) = \theta(1-\theta)\).

### 5.3 SCX 中的应用

**位置**:
- Theorem 4' 的核心: 文件 `exact_constant_minimax.md` 第 2.4 节
- Lemma A: 文件 `lemma_AB_bahadur_rao_f1.md`
- Lemma B: 同上
- Lemma D (自适应阈值): 文件 `lemma_CD_chernoff_adaptive.md`

**具体应用**:
Bahadur-Rao 用于给出 FPR 和 FNR 的精确渐近:

\[
\text{FPR}_M \sim \frac{\exp(-M \cdot \text{KL}(\theta \| p_0))}{\lambda_0^* \sqrt{2\pi M \theta(1-\theta)}}
\]
\[
\text{FNR}_M \sim \frac{\exp(-M \cdot \text{KL}(\theta \| p_1))}{|\lambda_1^*| \sqrt{2\pi M \theta(1-\theta)}}
\]

然后代入 F1 展开获得精确常数.

### 5.4 应用忠实度评估

**合法使用**: \(\checkmark\)

1. **i.i.d. 条件**: Bahadur-Rao 要求 i.i.d. 或至少满足 Gartner-Ellis 条件的独立变量. SCX 的 Lemma 2 和 3 使用 i.i.d. Bernoulli(\(p_0\)) 和 Bernoulli(\(p_1\))——精确满足条件.

2. **鞍点计算**: Lemma A 提供了完整的鞍点推导链: CGF \(\psi(\lambda) = \log(1-p+pe^\lambda)\) → 鞍点方程 \(\psi'(\lambda^*) = \theta\) → 闭式解 \(\lambda^* = \log\frac{\theta(1-p)}{p(1-\theta)}\) → 倾斜方差 \(\psi''(\lambda^*) = \theta(1-\theta)\). 所有推导正确.

3. **格子分布修正**: Lemma A 正确识别了伯努利分布是格子分布 (lattice distribution), 需要格子修正因子 \(\lambda^*/(1-e^{-\lambda^*})\). 这对精确常数至关重要.

4. **下半公式**: Lemma A.6 正确使用对称性 \(Y_i = 1-X_i\) 将下半情况归约到上半.

### 5.5 有限样本修正的处理

**评估: 充分处理**

1. Lemma A 使用 Robbins-Stirling 公式给出了显式的 \(O(1/M)\) 误差界 (Proposition A.5):
   \[
   |\varepsilon_M| \leq \frac{C(p,\theta)}{M}
   \]
   其中 \(C(p,\theta)\) 被分解为 Stirling 余项、阈值离散化误差和几何级数截断误差.

2. **Berry-Esseen 型修正**: Lemma A 引用了 Berry-Esseen 常数 \(C_{\text{BE}} \leq 0.4748\) (Shevtsova, 2011) 用于有限样本校正.

3. **非 i.i.d. 扩展**: Lemma A.6 提供了独立非同分布伯努利的 Bahadur-Rao 类比, 使用 Gartner-Ellis 定理, 适用于专家异质的情况.

**问题**: \(O(1/M)\) 界的显式常数依赖于复杂的中间常数, 其数值紧度未经验证. 若实际 M 较小 (如 M < 20), 标称的 \(O(1/M)\) 项可能不可忽略.

### 5.6 SCX 的增量

1. **将 Bahadur-Rao 嵌入 F1 风险**: Bahadur-Rao 原本用于单个均值的偏差概率. SCX 将其代入 F1 的渐近展开 (Lemma B), 得到三参数 (\(p_0, p_1, \eta\)) 的复合表达. 这不是标准应用.

2. **自适应阈值的二阶效应**: Lemma D 利用 Bahadur-Rao 展开捕捉 \(O(1/M)\) 阈值偏移通过指数产生的 \(O(1)\) 乘性效应. 这是精妙的分析——标准 Bahadur-Rao 不涉及阈值依赖于 M 的情况.

3. **格子修正 + F1 组合**: 格子修正因子 \(\lambda^*/(1-e^{-\lambda^*})\) 在 F1 表达式中出现于分子和分母中, 其相互抵消效果被正确跟踪. SCX 文档指出"可以将此效应显式追踪".

4. **与下界的精确匹配**: Theorem 4' 的关键优雅之处在于, FPR 和 FNR 贡献在自适应阈值下共享相同的因子 \(((1-\eta)/\eta)^s\), 使得 SCX 的渐近常数与理论下界精确相等. 这是 Bahadur-Rao 工具链的巧妙应用.

---

## 6. Robbins-Monro 随机逼近

### 6.1 原始论文引用

Robbins, H., & Monro, S. (1951). "A stochastic approximation method." *Annals of Mathematical Statistics*, 22(3), 400-407.

### 6.2 原始核心定理陈述

**Robbins-Monro 算法**:
设 \(M(x)\) 为未知函数, 观测 \(Y(x) = M(x) + \varepsilon\) 为含噪观测. 欲求 \(\theta\) 满足 \(M(\theta) = \alpha\). Robbins-Monro 迭代:

\[
\theta_{n+1} = \theta_n - a_n (Y_n - \alpha)
\]

其中 \(\{a_n\}\) 为满足 \(\sum a_n = \infty\), \(\sum a_n^2 < \infty\) 的正数列 (标准条件). 则 \(\theta_n \to \theta^*\) 几乎必然.

### 6.3 SCX 中的应用

**位置**:
- 自我进化理论 (self_evolution): 文件 `self_evolution/05_stochastic_approximation.md`
- 假设 SE-A5 (Robbins-Monro 学习率条件)
- Theorem SE-1 (收敛定理)

**应用陈述**:
NEP 学生参数的在线更新:
\[
\theta_{t+1} = \theta_t - \alpha_t \nabla \ell(\theta_t; x_t, y_t) + \xi_t
\]
其中 \(\xi_t\) 为噪声项, \(\alpha_t\) 满足 Robbins-Monro 条件 \(\sum \alpha_t = \infty\), \(\sum \alpha_t^2 < \infty\).

双时间尺度分析: gatekeeper \(S_t\) 在慢时间尺度更新, NEP 学生在快时间尺度更新——标准双时间尺度 SA 设置.

### 6.4 应用忠实度评估

**部分合法, 部分假设性**: \(\sim\)

1. **学习率条件**: 假设 SE-A5 正确列出了 Robbins-Monro 标准条件. \(\checkmark\)

2. **梯度有偏性**: 标准 Robbins-Monro 要求 \(M(\theta)\) 是回归函数 (即噪声的条件期望为零). SCX 中的梯度 \(\nabla \ell\) 是否满足 \(\mathbb{E}[\xi_t \mid \mathcal{F}_t] = 0\) 取决于记忆库采样是否无偏. 若 gatekeeper 引入选择偏差, 则梯度估计可能有偏. 自我进化理论假设 SE-A4 (条件 i.i.d. 采样) 旨在控制此偏差, 但此假设的成立条件未完全验证.

3. **双时间尺度**: 标准双时间尺度 SA (Borkar, 2008) 要求快慢时间尺度的学习率比率 \(\alpha_t^{(fast)} / \alpha_t^{(slow)} \to 0\). SCX 文档假设此条件但未提供具体调度策略.

4. **收敛目标**: Robbins-Monro 标准收敛到不动点, 但不保证是全局最优. Theorem SE-1 承认 SCX 收敛到"自洽不动点"而非全局最优——这与 SA 理论一致.

**结论**: Robbins-Monro 的框架性应用是合理的, 但精确验证需要更多关于采样偏差和学习率调度的细节. 当前表述处于"形式化猜想"水平.

### 6.5 SCX 的增量

1. **耦合动力系统**: 标准 SA 分析单一递归. SCX 将 SA 扩展到耦合系统 \((S_t, \theta_t)\), 其中 \(S_t\) 通过选择训练数据影响 \(\theta_t\), \(\theta_t\) 通过影响专家预测反馈到 \(S_t\). 双时间尺度分析是对标准 SA 的扩展, 而非照搬.

2. **Lyapunov 超鞅**: Theorem SE-1 使用 Lyapunov 超鞅论证而非标准 SA ODE 方法. 这是一条替代收敛路径, 在有限状态空间中特别有效.

3. **有限时间终止**: Theorem SE-2 将 SA 的渐近收敛转化为有限时间保证, 利用物理约束 (有限数据、有限精度). 这在标准 SA 中不常见.

---

## 7. Bayesian martingale / Doob 鞅收敛

### 7.1 原始论文引用

Doob, J. L. (1953). *Stochastic Processes*. Wiley.

鞅收敛定理: 若 \(\{M_n\}\) 是一致可积鞅 (或有界 \(L^1\) 鞅), 则 \(M_n\) 几乎必然收敛到某极限 \(M_\infty\).

### 7.2 SCX 中的应用

**位置**:
- 自我进化理论: 文件 `self_evolution/04_bayesian_update.md`

**应用陈述**:
Gatekeeper 评分 \(S_t\) 被解释为贝叶斯后验均值:
\[
S_t(x) = \mathbb{P}(\text{correct} \mid x, \mathcal{M}_t)
\]
其中 \(\mathcal{M}_t\) 是累积记忆库.

**鞅性质** (Claim): \(\mathbb{E}[S_{t+1} \mid \mathcal{F}_t] = S_t\), 即 \(\{S_t\}\) 是测度空间 \(\{\mathcal{F}_t\}\) 上的鞅.

**Doob 收敛**: 若 \(S_t\) 有界 (\([0,1]\) 内), 由 Doob 鞅收敛定理, \(S_t \to S_\infty\) a.s.

### 7.3 应用忠实度评估

**部分合法, 依赖条件未完全验证**: \(\sim\)

1. **鞅条件**: 要使 \(\mathbb{E}[S_{t+1} \mid \mathcal{F}_t] = S_t\) 成立, gatekeeper 更新必须是无偏的——即新数据不能系统性地使评分偏向更高或更低. 如果 gatekeeper 更新是贝叶斯后验更新, 那么在正确模型下后验均值确实是鞅. 但 SCX 的 gatekeeper 更新是否精确对应贝叶斯更新?

2. **模型正确性**: 贝叶斯鞅性质要求模型正确指定. 若 SCX 的先验或似然设定与真实数据生成过程不符, 则后验均值不具有鞅性质. SCX 文档承认这一点:"严格贝叶斯鞅要求模型正确".

3. **分布偏移**: 更新过程中, 记忆库 \(\mathcal{M}_t\) 的增长可能改变采样分布. 标准鞅停止理论假设观测是固定分布下的 i.i.d. 或至少满足特定依赖结构. SCX 中, gatekeeper 选择何方数据进入记忆库, 引入了非平凡的选择偏差.

4. **Doob 收敛**: 有界鞅的 a.s. 收敛成立, 但极限 \(S_\infty\) 可能不是真实后验——而是被模型错误指定的扭曲后验.

**结论**: 鞅框架提供启发性和结构性的视角, 但作为严格收敛证明的基础需要更强的模型假设. SCX 文档将贝叶斯更新标记为"贝叶斯解释"而非"贝叶斯证明", 这是诚实的.

### 7.4 SCX 的增量

1. **Gatekeeper 评分作为鞅**: 将 gatekeeper 评分函数 \(S_t\) 解释为鞅序列是新颖的. 在主动学习或贝叶斯优化中, 采集函数通常不是鞅.

2. **非平稳环境下的鞅收敛**: SCX 的自我进化是目标分布演化的过程. 标准鞅理论假设静态分布. SCX 通过条件 i.i.d. 假设 (SE-A4) 将更新步骤解耦, 使得鞅论证仍然适用.

3. **有限时间界**: 将 Doob 的渐近 a.s. 收敛转化为 Theorem SE-2 的有限时间保证是一个实际的增量, 尽管依赖于物理约束而非纯概率论证.

---

## 8. 聚类理论 (Pollard 1981, k-means 一致性)

### 8.1 原始论文引用

Pollard, D. (1981). "Strong consistency of k-means clustering." *The Annals of Statistics*, 9(1), 135-140.

Pollard 证明了当 \(n \to \infty\) 时, k-means 的经验最小化器几乎必然收敛到总体最小化器. 前提是总体分布有有限二阶矩, 且最小化器在排列意义下唯一.

### 8.2 SCX 中的应用

**位置**:
- Theorem 5 (Fixed-K Cluster Consistency): 文件 `cluster_consistency_v3.md`
- Proposition 6 (Bootstrap Stability): 文件 `feature_strength_via_stability.md`

**Theorem 5 核心结果**:
在强分离条件下 (\(\Delta_{\min}^2 / (\sigma^2 d_\phi) \geq C_0\)), Lloyd 算法以概率 \(1 - K\exp(-c n_{\min} \Delta_{\min}^2 / (\sigma^2 d_\phi)) - o(1)\) 恢复真实状态划分.

**证明工具**:
- Pollard (1981) 一致性 → 引理 1 (总体最小化器接近真中心)
- 经验过程理论 + 局部化论证 → 引理 2 (经验最小化器指数收敛)
- 三角形不等式 → 引理 3 (中心接近 → 划分正确)
- Lloyd 景观分析 → 引理 4 (Lloyd 在强分离下找到全局最小化器)

### 8.3 应用忠实度评估

**合法使用, 但扩展显著**: \(\checkmark\)

1. **Pollard 一致性**: SCX 引理 1 的总体最小化器接近真中心证明是对 Pollard (1981) 的继承性扩展. Pollard 证明了 k-means 的经验中心收敛到总体中心, 但没有给出在生成模型下的显式收敛速率. SCX 使用自洽性论证和子高斯尾界给出了指数速率.

2. **强分离条件**: Pollard 不需要分离条件 (一致性在弱条件下成立). SCX 的强分离条件 \(\Delta_{\min}^2 / (\sigma^2 d_\phi) \geq C_0\) 是获得指数速率的代价——无此条件时一致性仍然成立但速率更慢.

3. **固定 K**: Pollard (1981) 考虑固定 K 的情况. SCX Theorem 5 同样要求 K 固定 (Section 9.1 诚实讨论了 K 增长时的退化). 一致.

4. **总体 vs 经验**: Pollard 结果用于引理 1 的总体最小化器分析. 引理 2 的经验过程论证 (局部化、剥离技术、Talagrand 不等式) 不是 Pollard 的, 而是现代经验过程理论的工具.

### 8.4 聚类数与真实状态数的关系

**核心问题**: Theorem 5 假设聚类数 \(K\) 等于真实状态数 \(K_{\mathcal{S}}\). 在实践中, K 可能未知或误指定.

**SCX 的处理**:
1. Theorem 5 显式假设 K 固定且已知.
2. Section 9.4 讨论 K 的选择方法 (肘部法则、gap 统计量、BIC), 但未将这些选择的不确定性纳入概率界.
3. Proposition 6 的稳定性诊断可用于选择 K (选择最大化稳定性的 K), 但此选择的影响未正式纳入 Theorem 5 的保证.

**评估**: 这是诚实的——Theorem 5 的假设部分清楚说明了已知 K 的要求. 其他论文通常也做此假设. 但直接将定理应用于 K 未知的场景时需要谨慎.

### 8.5 NP-hard 间隙的处理

**评估: 充分**. Lemma 4 直接应对 k-means 的 NP-hard 问题. 在强分离条件下, k-means 景观具有唯一局部最小化器 (也是全局最小化器), Lloyd 算法以 \(R = \Omega(\log n)\) 次随机初始化成功. 当强分离条件不成立时, SCX 明确承认间隙保留, 并引用 Kumar & Kannan (2010) 和 Ostrovsky et al. (2013) 的近似算法. 这种处理比大多数 k-means 论文更诚实.

### 8.6 SCX 的增量

1. **指数速率的有限样本保证**: Pollard (1981) 给出 a.s. 一致性但无速率. SCX 给出显式指数速率 \(K\exp(-c n_{\min}\Delta_{\min}^2/(\sigma^2 d_\phi))\). 这在高维统计中常见但不平凡.

2. **子高斯噪声的显式处理**: Pollard 假设有限二阶矩. SCX 使用子高斯尾界 (Vershynin 2018) 得到指数集中. 这是将经典一致性结果升级到现代高维框架.

3. **Lloyd 成功概率**: 随机初始化 Lloyd 算法的成功概率分析是对 Pollard 的补充——Pollard 假设全局最小化器已被访问, 而 SCX 显式证明 Lloyd 在强分离下能够找到它.

4. **v1 → v3 的修订**: 从 v1 到 v3 的修改 (修复反向不等式、指数符号、NP-hard 间隙) 表明 SCX 团队实施了严格的自审. 特别是, 将错误的直接 \(W(\mu) - W(\mu^*)\) 计算替换为自洽性 + 收缩论证是实质性的改进.

---

## 9. 其他深层连接

### 9.1 BBP 跃迁 (Baik-Ben Arous-Peche 2005)

**原始论文**: Baik, J., Ben Arous, G., & Peche, S. (2005). "Phase transition of the largest eigenvalue for nonnull complex sample covariance matrices." *Annals of Probability*, 33(5), 1643-1697.

**在 SCX 中的角色**: 最初在 `feature_strength_via_stability.md` 的早期版本中被尝试作为特征强度诊断工具. BBP 跃迁描述在尖峰协方差矩阵模型中, 当信号强度超过某阈值时最大特征值偏离 Marchenko-Pastur 分布.

**评估: 失败连接, 已被弃用**.

1. **弃用原因**: SCX 文档诚实列出了 BBP 桥梁的五条致命缺陷:
   - 特征值的最大方差方向 ≠ 互信息的状态信息 (反例: 高方差独立特征产生大 \(\lambda_1\) 但 \(\delta=0\))
   - 高斯-各向同性假设被 SCX 的真实特征违反 (ACE、CNN、表格数据)
   - 校准常数 C 是循环的
   - Tracy-Widom 检验要求 i.i.d. 元素, 被违反
   - 多弱信号机制不可检测

2. **替代**: 稳定度诊断 (Proposition 6) 取代了 BBP 代理. 这是一个正确的选择——稳定度直接测试 k-means 的可重复性而非 Gram 特征值.

**教训**: BBP 跃迁是随机矩阵理论的一个优雅结果, 但不适用于 SCX 的特征. 这一失败的诚实文档是 SCX 理论文化的一个亮点.

### 9.2 随机矩阵理论的连接

**存在性**: 弱, 且主要是通过弃用的 BBP 桥梁. 在 Theorem 5 中, 谱聚类连接 (Ding & He, 2004: k-means ≈ PCA on Gram 矩阵) 被提及, 但未作为正式论证使用.

**评价**: "连接"更多是概念层面的 (如将 k-means 与谱聚类关联, 或在深层数学连接文档中提及 C*-代数), 而非定理证明中的实质性工具. 虽然 `deep_math_connections.md` 探索了丰富的类比 (纤维丛、Galois 类比、函子), 但这些被诚实标记为"推测性"或"审美类比", 未声称是严格的数学连接.

### 9.3 数据处理不等式 (DPI)

**原始引用**: Cover & Thomas (2006). *Elements of Information Theory* (2nd ed.), Section 2.8.

**SCX 中的应用**: Theorem 2 证明中的关键步骤.

**DPI 陈述**: 若 \(X \to Y \to Z\) 形成马尔可夫链, 则 \(I(X; Z) \leq I(X; Y)\).

**SCX 使用**: 在 Theorem 2 证明 Step 3 中:
\[
\text{TV}(P_{\text{pred}}, \tilde{P}_{\text{pred}}) \leq \text{TV}(P, \tilde{P})
\]
通过数据处理不等式: 预测分布 \((\hat{z}(X), Z)\) 是原始数据 \((X, Z)\) 的函数, 因此 TV 不会增加.

**合法使用**: \(\checkmark\). 这是 DPI 在总变差距离下的标准使用. 马尔可夫链结构 \(P \to P_{\text{pred}}\) 是 SCX 流水线 (\(\phi\) → 聚类 → 状态分配 → 噪声分数 → 决策) 的直接结果.

**SCX 的增量**: 将 DPI 与 Pinsker 不等式结合, 创建一条从互信息 \(\delta = I(\phi; S)\) 到 TV 界再引入性能指标 (AUC, PR-AUC, F1) 的完整链. 这种信息论到统计决策的翻译虽非全新, 但 SCX 将其用于一个新颖的多专家设置.

### 9.4 Pinsker 不等式

**原始引用**: Pinsker, M. S. (1964). *Information and Information Stability of Random Variables and Processes*. Holden-Day.

**陈述**: \(\text{TV}(P, Q) \leq \sqrt{\text{KL}(P \| Q) / 2}\).

**SCX 应用**: Theorem 2, 将 \(\delta = I(\phi; S)\) 转化为 TV 界.

**合法使用**: \(\checkmark\). 标准应用.

**方向正确性检查**: Pinsker 给 TV 上界. SCX 使用它来限制 AUC/F1 的变化 (\(|\text{AUC}_P - \text{AUC}_{\tilde{P}}| \leq \text{TV}\)). 这是正确的: TV 小意味着性能变化小.

### 9.5 Hellinger distance tensorization

**原始引用**: 在各种教科书中 (如 Polyanskiy & Wu, Tsybakov). 基本性质: \(H^2(P^{\otimes n}, Q^{\otimes n}) = 1 - (1 - H^2(P,Q))^n\).

**SCX 应用**: `minimax_lower_bound_v2.md` 中替代 Slud 不等式.

**创新应用**: 在专家独立性 (A2) 下, 精确 tensorization 导出指数衰减下界, 避免了对二项式尾界的复杂处理.

---

## 10. 理论根源树状图

以下 ASCII 树图展示 SCX 定理与原始数学工具之间的依赖关系.

```
                                          ┌─────────────────────────┐
                                          │      SCX Framework      │
                                          │  (A1-A6 Assumptions)    │
                                          └─────────────────────────┘
                                                    │
          ┌─────────────────┬──────────────────┬────┴─────┬──────────────────┬──────────────────┐
          ▼                 ▼                  ▼          ▼                  ▼                  ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────────┐
   │  Theorem 1   │ │  Theorem 2   │ │  Theorem 3   │ │Theorem 4'│ │  Theorem 5   │ │ Proposition 6   │
   │    噪声检测    │ │    弱特征     │ │    不可识别性   │ │ 精确常数    │ │  聚类一致性    │ │  稳定度诊断      │
   └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └─────┬────┘ └──────┬───────┘ └────────┬─────────┘
          │                │                │              │            │                   │
     ┌────┴────┐      ┌────┴────┐     ┌────┴────┐    ┌────┴────┐     ┌──┴───┐          ┌───┴────┐
     ▼         ▼      ▼         ▼     ▼         ▼    ▼         ▼     ▼      ▼          ▼        ▼
 ┌────────┐┌────────┐┌─────┐┌─────┐┌────┐┌──────┐┌──────┐┌────────┐┌────┐┌──────┐┌────────┐┌────────┐
 │Hoeffding││Chernoff││Fano ││Pinsker││混合 ││最小最大││Chernoff││Bahadur││k-means││子高斯 ││聚类    ││Bootstrap│
 │(1963)  ││(1952)  ││(1961)││(1964) ││模型 ││论证   ││信息    ││-Rao   ││一致  ││集中   ││稳定度  ││重采样  │
 │        ││        ││     ││       ││等价 ││(Le    ││(1952)  ││(1960) ││Pollard││(Versh ││(von    ││        │
 │        ││        ││     ││       ││     ││Cam    ││        ││       ││1981)  ││2018)  ││Luxburg││        │
 └────────┘└────────┘└─────┘└─────┘└────┘└──────┘└──────┘└────────┘└────┘└──────┘└────────┘└────────┘
                                                               │
                                                          ┌────┴────┐
                                                          ▼         ▼
                                                    ┌──────────┐┌──────────┐
                                                    │Neyman-   ││Cramer    │
                                                    │Pearson   ││定理      │
                                                    │(1933)    ││(1938)    │
                                                    └──────────┘└──────────┘

  ──────────── 自我进化理论 (Self-Evolution) ────────────

    Theorem SE-1 (收敛)           Theorem SE-2 (完备性)
         │                             │
    ┌────┴────┐                   ┌────┴────┐
    ▼         ▼                   ▼         ▼
┌────────┐┌────────┐        ┌────────┐┌────────────┐
│Robbins ││Doob    │        │Lyapunov││物理约束    │
│-Monro  ││鞅收敛  │        │函数    ││(有限数据、  │
│(1951)  ││(1953)  │        │        ││ 有限精度)   │
└────────┘└────────┘        └────────┘└────────────┘

  ──────────── 弃用连接 ────────────

    BBP 跃迁 (Baik-Ben Arous-Peche, 2005)
    ── 在 BBP 光谱代理中被尝试, 但失败 (详见第 9.1 节)
    ── 被 Proposition 6 的稳定度诊断替代

  ──────────── 概念类比 (非严格) ────────────
    统计物理 (Ising/Curie-Weiss)       ─ 共识得分为磁化强度
    信息几何 (Fisher 度量)             ─ Δ_s 为测地距
    纤维丛                            ─ Theorem 3 不可识别性为纤维
    Galois 对应                       ─ 状态粗粒化 ↔ 专家对称性子群
    函子/自然变换                     ─ 两层级架构为自然变换
```

---

## 附录: Conjecture 和不确定性标注

| 编号 | 内容 | 类型 | 文件位置 |
|------|------|------|----------|
| C1 | O(1/M) 有限样本修正的紧度 | 不确定性 | Lemma A, Proposition A.5 |
| C2 | 非 i.i.d. Bahadur-Rao 的 Lyapunov 条件 | 假设性 | Lemma A.6 |
| C3 | 双时间尺度 SA 的精确收敛率 | 形式化猜想 | self_evolution/05 |
| C4 | Gatekeeper 的贝叶斯鞅性质 | 假设性 (依赖模型正确) | self_evolution/04 |
| C5 | Lyapunov 函数的精确形式 | 开放问题 (\(P0\)) | self_evolution/06, 09 |
| C6 | 四种收敛路径的精确定界 | 开放问题 (\(P1\)) | self_evolution/06, 09 |
| C7 | Proposition 6 阈值 \(\tau=0.7\) | 启发式 (Landis & Koch) | feature_strength_via_stability.md |
| C8 | BBP 桥接 (已弃用) | 失败连接 | feature_strength_via_stability.md §1 |
| C9 | Theorem 2 PR-AUC 界 | 部分证明 | THEOREMS_UNIFIED.md §8.1 |
| C10 | C*-代数/Galois/函子类比 | 推测性 | deep_math_connections.md |

---

## 参考文献汇总

1. Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables. *JASA*, 58(301), 13-30.
2. Chernoff, H. (1952). A measure of asymptotic efficiency for tests of a hypothesis. *Annals of Mathematical Statistics*, 23(4), 493-507.
3. Fano, R. M. (1961). *Transmission of Information: A Statistical Theory of Communications*. MIT Press.
4. Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
5. Le Cam, L. (1973). Convergence of estimates under dimensionality restrictions. *Annals of Statistics*, 1(1), 38-53.
6. Le Cam, L. (1986). *Asymptotic Methods in Statistical Decision Theory*. Springer.
7. Bahadur, R. R. & Rao, R. R. (1960). On deviations of the sample mean. *Annals of Mathematical Statistics*, 31(4), 1015-1027.
8. Cramer, H. (1938). Sur un nouveau theoreme-limite de la theorie des probabilites. *Actualites Scientifiques et Industrielles*, 736, 5-23.
9. Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*, 22(3), 400-407.
10. Doob, J. L. (1953). *Stochastic Processes*. Wiley.
11. Pollard, D. (1981). Strong consistency of k-means clustering. *Annals of Statistics*, 9(1), 135-140.
12. Pinsker, M. S. (1964). *Information and Information Stability of Random Variables and Processes*. Holden-Day.
13. Baik, J., Ben Arous, G. & Peche, S. (2005). Phase transition of the largest eigenvalue. *Annals of Probability*, 33(5), 1643-1697.
14. Neyman, J. & Pearson, E. S. (1933). On the problem of the most efficient tests of statistical hypotheses. *Phil. Trans. R. Soc. A*, 231, 289-337.
15. Vershynin, R. (2018). *High-Dimensional Probability*. Cambridge University Press.
16. Tsybakov, A. B. (2009). *Introduction to Nonparametric Estimation*. Springer.
17. van der Vaart, A. W. (1998). *Asymptotic Statistics*. Cambridge University Press.
18. Borkar, V. S. (2008). *Stochastic Approximation: A Dynamical Systems Viewpoint*. Cambridge University Press.
19. Shamir, O. & Tishby, N. (2009). On the reliability of clustering stability in the large sample regime. *NIPS 2008*.
20. von Luxburg, U. (2010). Clustering stability: An overview. *Foundations and Trends in ML*, 2(3), 235-274.
21. Landis, J. R. & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159-174.
22. Shevtsova, I. G. (2011). On the absolute constants in the Berry-Esseen-type inequalities. *Doklady Mathematics*, 83(3), 320-323.
23. Dembo, A. & Zeitouni, O. (2010). *Large Deviations Techniques and Applications* (2nd ed.). Springer.
24. Ingster, Y. I. & Suslina, I. A. (2003). *Nonparametric Goodness-of-Fit Testing Under Gaussian Models*. Springer.

---

*本分析由 Codex orchestrator agent 1 (数学根源挖掘) 生成, 2026-06-28*
