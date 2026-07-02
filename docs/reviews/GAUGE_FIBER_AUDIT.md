# GAUGE_FIBER_AUDIT — fiber_bundle 论文第一原理严格审计

**审计文件:**
- `F:\scx\papers\scx_fiber_bundle\fiber_bundle.tex` (1681 行)
- `F:\scx\papers\scx_fiber_bundle\fiber_bundle.md` (1477 行)

**交叉参考:**
- `F:\scx\papers\scx_gauge_formalized\gauge_formalized.tex` (1662 行)

**审计日期:** 2026-07-03
**审计范围:** 拓扑声明（同伦等价、循环基引理、四边形+三角形完备性）、纤维丛结构定义、Cercis 代码-论文差距声明、所有定理/证明的数学正确性
**已核实的关键修复提交:** 27d87a0, c7218ef, 3c20a35, 45ad33d, a715e95

---

## 一、总览

| 审计维度 | 状态 | 说明 |
|----------|------|------|
| 离散 Hodge 理论基础 | ✅ 正确 | 标准离散外微分, 无问题 |
| SCX 图的构造 | ✅ 正确 | 顶点-边-回路定义自洽 |
| 曲率作为回路和乐 | ✅ 正确 | 代数化简无误 |
| 规范变换公式 $A' = A - d_0 g$ | ✅ 正确 | 证明无误 |
| 规范不变性证明 | ✅ 正确 | 基于 $d_1 d_0 = 0$ |
| 零模固定 $\neq$ Coulomb 规范 | ✅ 正确 | 四项论证充分 |
| 最小二乘规范固定 | ✅ 正确 | 法方程+伪逆严格 |
| Cercis 分数定义 | ✅ 正确 | 投影算子公式一致 |
| 拓扑平凡性声明 | ✅ 正确 | 可缩群+可缩底空间 |
| 循环基引理 (Lemma) | ❌ LaTeX 破损 | 参数缺失, 但数学内容正确 |
| 平坦性判据 (Thm 3.5) | ✅ 已修复 | 明确了"四边形+三角形"回路及调和分量假设 |
| Cercis=0 刻画 (Thm 5.3) | ❌ 条件(v)不足 | 仅要求四边形曲率为零, 缺三角形 |
| Cercis vs Yang-Mills 注记 | ❌ 数学错误 | $\|d_1 r\|^2 = \|d_1 r_\text{harm}\|^2$ 错误 |
| 代码-论文差距声明 | ⚠️ LaTeX 破损+缺证明 | 声明诚实但缺极限一致性证明 |
| dim ker($\Delta_1$) 声明 | ⚠️ 跨论文不一致 | 图 vs 2-复形定义不同 |

---

## 二、逐项详细审计

### 2.1 离散 Hodge 理论基础 (Section 2) — ✅ 全部正确

**定义检查:**

- 有向图 $\mathcal{G}=(\mathcal{V},\mathcal{E})$: 标准定义, 无自环允许多重边 ✅
- 关联矩阵 $B$ 及 $d_0$: $B_{e,w} = +1$ (目标), $-1$ (源) — 标准定义 ✅
- 基本恒等式 $d_1 d_0 = 0$: 证明 (telescoping sum) 正确 ✅
- 伴随算子 $d_0^T = W_0^{-1} B^T W_1$: 由伴随条件推导, 公式正确 ✅
- 无权情况 $d_0^T = B^T$: 离散散度 (入减出) — 经典结果 ✅
- 图 Laplacians $\Delta_0 = B^T B$, $\Delta_1 = BB^T + C^T C$: 标准定义 ✅
- 离散 Hodge 分解 $\Omega^1 = \operatorname{im}(d_0) \oplus \ker(\Delta_1) \oplus \operatorname{im}(d_1^T)$: 标准结果 ✅

### 2.2 SCX 图的构造 (Section 3) — ✅ 全部正确

- 顶点: $(k,m)$, $k=1..N$, $m=1..M$, 共 $NM$ 个 ✅
- 参数边: $(k,m)\to(k+1,m)$, 共 $M(N-1)$ 条 ✅
- 专家边: $(k,i)\to(k,j)$, $i\neq j$, 共 $NM(M-1)$ 条 ✅
- 边赋值 $A_e$: 参数边 $=\tilde{x}_m^{k+1}-\tilde{x}_m^k$, 专家边 $=\tilde{x}_i^k-\tilde{x}_j^k$ ✅
- 基本四边形回路: $(k,i)\to(k,j)\to(k+1,j)\to(k+1,i)\to(k,i)$ — 方向需要小心处理逆向边 ✅
- 曲率化简: $\operatorname{curv}(\gamma_{k,i,j}) = (\tilde{x}_i^k-\tilde{x}_i^{k+1})-(\tilde{x}_j^k-\tilde{x}_j^{k+1})$ — 代数验证正确 ✅

**曲率化简的逐行验证:**

```
curv = δ_{ij}^k + (x̃_j^{k+1} - x̃_j^k) + δ_{ji}^{k+1} + (x̃_i^k - x̃_i^{k+1})
     = (x̃_i^k - x̃_j^k) + (x̃_j^{k+1} - x̃_j^k) + (x̃_j^{k+1} - x̃_i^{k+1}) + (x̃_i^k - x̃_i^{k+1})
     = x̃_i^k - x̃_j^k + x̃_j^{k+1} - x̃_j^k + x̃_j^{k+1} - x̃_i^{k+1} + x̃_i^k - x̃_i^{k+1}
     = (x̃_i^k - x̃_i^{k+1}) - (x̃_j^k - x̃_j^{k+1})
```

注意: $\delta_{ji}^{k+1} = \tilde{x}_j^{k+1} - \tilde{x}_i^{k+1}$, 不是 $+$, 但在曲率定义中边 $(k+1,j)\to(k+1,i)$ 是逆向的, 故应取负号. 代入得 $\delta_{ji}^{k+1}$ **带正号** (因为已经在回路中反向). 验证:

四边形回路: $(k,i)\to(k,j)$ (正向专家边, $+\delta_{ij}^k$), $(k,j)\to(k+1,j)$ (正向参数边, $+A_{param}$), $(k+1,j)\to(k+1,i)$ (逆向专家边, 取 $-A_{expert}$, 即 $+\delta_{ji}^{k+1}$), $(k+1,i)\to(k,i)$ (逆向参数边, 取 $-A_{param}$).

该推导正确. ✅

### 2.3 ❌ 循环基引理 (Lemma: Cycle Basis of the SCX Graph) — LaTeX 破损

**位置:** fiber_bundle.tex 行 627-647 (commit c7218ef 新增)

**LaTeX 问题:** 多处参数缺失, 导致渲染后不可读:

```latex
\item {\\bf Quadrilateral loops:}  \\to (k,j) \\to (k+1,j) \\to (k+1,i) \\to (k,i)$
      for all configurations $ and expert pairs <j$;
```

起始顶点 `(k,i)` 缺失, 配置索引 `k` 缺失, 专家对 `i<j` 缺失.

```latex
\item {\\bf Triangle loops:}  \\to (k,j) \\to (k,\\ell) \\to (k,i)$
      for all configurations $ and distinct experts ,j,\\ell$.
```

起始顶点 `(k,i)` 缺失, 配置索引 `k` 缺失, 专家索引 `i` 缺失.

**证明草图的 LaTeX 问题:** 多处数学模式参数缺失:
- `$\verts = \\{(k,m) : 1 \\leq k \\leq K, 1 \\leq m \\leq M\\}$` — 渲染后 `\verts` 缺失
- `$M-1$ star edges` — `M` 缺失
- `$\\binom{M}{2}K + (M-1)(K-1)$` — 多处参数缺失

**数学内容评估:** 尽管 LaTeX 破损, 从上下文可推断数学声明是正确的:
- 生成树: 每个配置 $k$ 内用 $M-1$ 条星形边连接, 配置间用 $(k,1)\to(k+1,1)$ 连接
- 非树参数边 $(k,m)\to(k+1,m)$ ($m\neq 1$) 产生四边形基本回路
- 非树专家边 (两端都不是专家 1) 产生三角形基本回路
- 四边形 + 三角形回路确实生成全循环空间

**结论:** 数学成立, LaTeX 需修复.

### 2.4 ✅ 平坦性判据 (Thm 3.5: SCX Flatness Criterion) — 已修复

**commit a715e95 修复内容:**

1. 标题改为 "(Harmonic-Corrected)" — 明确假设
2. 前提条件明确: "When the harmonic component of the Hodge decomposition vanishes"
3. 条件 (i): 改为 "for all elementary **quadrilateral and triangle** loops" — 完备
4. 证明重写, 使用 Hodge 分解 $ \ker(d_1) = \operatorname{im}(d_0) \oplus \ker(\Delta_1) $, 在调和分量为零的假设下得到等价性
5. 补充特例: $M=1$ 或 $M=2$ 时 $\beta_1=0$, 等价无条件成立

**独立验证:** 正确. 证明链:
- (i)⇒ 四边形+三角形曲率皆零 ⇒ $d_1 A = 0$ ⇒ $A \in \ker(d_1)$
- Hodge: $\ker(d_1) = \operatorname{im}(d_0) \oplus \ker(\Delta_1)$
- 调和分量为零 ⇒ $\ker(\Delta_1) = \{0\}$ ⇒ $A \in \operatorname{im}(d_0)$ ⇒ (ii)
- (ii)⇒(i): $d_1 d_0 = 0$ ✅
- (ii)⇔(iii): 代数推导正确 ✅

**结论:** 该定理经修复后正确.

### 2.5 ❌ Cercis=0 刻画 (Thm 5.3: Characterization of $\mathcal{C}=0$) — 条件(v)不足

**当前文本** (fiber_bundle.tex 行 970-971):
> (v) $\operatorname{curv}(\gamma) = 0$ for all **quadrilateral** elementary loops $\gamma$, *and* the **harmonic** component of $A$ is zero.

**问题:** 条件 (v) 仅要求**四边形**回路的曲率为零, 未包含**三角形**回路.

**反例构造:** 设三角形回路 $\gamma_{\text{tri}} = (k,i)\to(k,j)\to(k,\ell)\to(k,i)$ 上的曲率非零, 但所有四边形回路的曲率为零, 且调和分量为零.
- 三角形曲率非零 ⇒ $d_1 A \neq 0$ ⇒ $A$ 有非零余正合分量
- 余正合分量 $\in \operatorname{im}(d_1^T) \subseteq \operatorname{im}(d_0)^\perp$
- 故 $\mathcal{C} = \|P^\perp A\|^2 > 0$, 但条件 (v) 声称 $\mathcal{C}=0$

**修复方案:** 条件 (v) 应改为:
> $\operatorname{curv}(\gamma) = 0$ for all elementary loops $\gamma$ in a cycle basis (i.e., both quadrilateral **and triangle** loops), *and* the harmonic component of $A$ is zero.

或等价地:
> $d_1 A = 0$ *and* the harmonic component of $A$ is zero.

**注记中的错误** (行 974-975):
> "$d_1 A = 0$ alone only excludes the harmonic component"

此陈述错误. $d_1 A = 0$ 意味着 $A$ 的**余正合分量为零**, 而非调和分量. 调和分量 $r_{\text{harm}} \in \ker(d_1)$ 定义为满足 $d_1 r_{\text{harm}} = 0$ **且** $d_0^T r_{\text{harm}} = 0$. $d_1 A = 0$ 正是调和形式的必要条件之一, 不是排除条件.

**正确陈述应为:**
> $d_1 A = 0$ alone guarantees $A$ has zero coexact component (since $\operatorname{im}(d_1^T) \perp \ker(d_1)$), but does not guarantee $A$ is exact — $A$ could still have a non-zero harmonic component in $\ker(\Delta_1)$.

### 2.6 ❌ Cercis vs Yang-Mills 注记 — 数学错误

**位置:** fiber_bundle.tex 行 927-935

**原文:**
> "whereas a Yang-Mills-type functional would only capture
> $\|d_1 r\|^2 = \|d_1 r_{\text{harm}}\|^2$."

**错误分析:**

由 Hodge 分解: $r = A - d_0 g^* \in \operatorname{im}(d_0)^\perp = \ker(\Delta_1) \oplus \operatorname{im}(d_1^T)$.

分解: $r = r_{\text{harm}} + r_{\text{coexact}}$, 其中 $r_{\text{coexact}} = d_1^T \beta$.

应用 $d_1$:
- $d_1 r_{\text{harm}} = 0$ (调和形式的定义: $r_{\text{harm}} \in \ker(d_1)$)
- $d_1 r_{\text{coexact}} = d_1 d_1^T \beta$

所以: $\|d_1 r\|^2 = \|d_1 d_1^T \beta\|^2 \neq 0$ (一般情况)

**而论文声称** $\|d_1 r\|^2 = \|d_1 r_{\text{harm}}\|^2 = \|0\|^2 = 0$, 与事实矛盾.

**正确的 Yang-Mills 解释:**
- Cercis = $\|r\|^2 = \|r_{\text{harm}}\|^2 + \|d_1^T \beta\|^2$ — 捕获调和+余正合两部分的全范数
- Yang-Mills 型泛函 = $\|d_1 r\|^2 = \|d_1 d_1^T \beta\|^2$ — 捕获余正合分量通过 $d_1$ 作用后的范数
- 调和分量对 Yang-Mills 无贡献 (被 $d_1$ 杀死), 但对 Cercis 有贡献
- 余正合分量对二者都有贡献, 但程度不同 ($\|d_1^T\beta\|^2$ vs $\|d_1 d_1^T\beta\|^2$)

**结论:** 该注记的数学陈述错误. 需完全重写.

### 2.7 ⚠️ 代码-论文差距声明 (Remark 5.5) — LaTeX 破损 + 缺证明

**位置:** fiber_bundle.tex 行 983-997 (commit c7218ef 新增)

**LaTeX 问题:**
```latex
approximation}: (s) = Q(s) + \\eta(t) \\cdot N(s)$, where $ is binary
vote consensus among experts and $ is feature-space novelty.
```
- `\cercis(s)` 的宏 `\cercis` 缺失, 显示为空白
- `$` 号缺失导致数学模式混乱
- `^T B g = B^T A$` — 丢失前导 `B`
- `+\\eta N$` — 丢失 `Q`

**数学声明评估:**
该注记声明 Cercis 分数 $=\|P^\perp A\|^2$ 是"理论理想", 而生产代码计算的是 $Q(s)+\eta(t)\cdot N(s)$ (二值投票一致性+特征空间新颖性), 两者在极限情况 (完美专家、零噪声) 下一致.

**问题:**
1. 未提供极限情况下一致的**证明** (哪怕是证明草图)
2. 未提供**定量边界**: 有限样本下差异多大?
3. 声称 "code's $Q+\eta N$ is a computationally efficient proxy" 预设二者正相关, 但未证明

**结论:** 声明诚实但数学不严格. 应至少提供:
- 极限一致的证明草图
- 或明确标记为 Conjecture

### 2.8 ⚠️ 跨论文不一致: $\dim\ker(\Delta_1)$

**问题:** fiber_bundle.tex 和 gauge_formalized.tex 对 $\dim\ker(\Delta_1)$ 隐含不同的值.

**fiber_bundle.tex** (Remark 4.5, 行 878):
> $\dim\ker(\Delta_1)$ equals the **cyclomatic number** $|\mathcal{L}|$ of the graph

图 (1-骨架) 的圈数:
$$|\mathcal{L}| = |\mathcal{E}| - |\mathcal{V}| + 1 = NM^2 - NM - M + 1$$
(依赖于 $N$ 和 $M$)

**gauge_formalized.tex** (Thm 3.2):
> 2-复形 $\mathcal{K}_{\text{SCX}}$ 的 $\beta_1 = (M-1)(M-2)/2$
(仅依赖于 $M$, 与 $N$ 无关)

**分析:**

- fiber_bundle.tex 的 $\Delta_1 = d_0 d_0^T + d_1^T d_1$ 定义在**图** (1-骨架) 层次, $d_1$ 映射到形式回路空间 (非面空间). $\ker(\Delta_1) \cong H_1(\text{graph})$, 维数确为圈数.

- gauge_formalized.tex 的 $\Delta_1$ 定义在**2-复形**层次 (图+四边形面), $d_1$ 映射到面空间 $C_2$. $\ker(\Delta_1) \cong H_1(\text{2-complex})$, 维数更小, 因为四边形面边界消灭了部分 1-循环.

**验证 (2-复形的 $H_1$):**

对于有向边计数:
- 1-循环空间维数 = $|\mathcal{E}| - |\mathcal{V}| + 1$ (圈数)
- 面边界 $\operatorname{im}(\partial_2)$: 所有四边形面边界线性无关, 秩 = $(N-1)M(M-1)/2$
- $H_1(2\text{-complex}) = \ker(\partial_1)/\operatorname{im}(\partial_2)$

关键观察: 配置 $k$ 处的三角形回路与配置 $k+1$ 处的三角形回路在 2-复形中**同调** (二者之差是三个四边形面边界的线性组合):
$$\partial(f_{k,i,j} + f_{k,j,\ell} - f_{k,i,\ell}) = \text{triangle}_k - \text{triangle}_{k+1}$$

因此所有 $N$ 个配置的三角形回路在同调中等价, 独立三角形回路数 = $(M-1)(M-2)/2$, 与 $N$ 无关.

**计算验证:**
$$H_1 = \text{圈数} - \operatorname{rank}(\partial_2) = [NM(M-1)/2 - M + 1] - [(N-1)M(M-1)/2]$$
$$= \frac{M(M-1)}{2} - M + 1 = \frac{(M-1)(M-2)}{2}$$

对于有向边, 使用正确的 $|\mathcal{E}| = 2M(N-1) + NM(M-1)$ (参数边来回各一), 结果一致. ✅

**结论:**
- fiber_bundle.tex 的声明 (图圈数) **技术上正确** — 在其图层次定义下
- gauge_formalized.tex 的声明 (2-复形 Betti 数) **物理上更相关** — 衡量"不一致模式的本质数量"
- 两篇论文使用**不同的** $\Delta_1$ 算子, 导致核维数不同 — 这是**隐含的定义分歧**, 应显式说明

### 2.9 同伦等价声明 (gauge_formalized.tex Thm 3.2) — 数学正确

**声明:** $\mathcal{K}_{\text{SCX}} \simeq K_M$ (SCX 2-复形同伦等价于 $M$ 个顶点的完全图)

**证明草图的独立验证:**

1. 对每个专家 $m$, 参数边 $(1,m)\to(2,m)\to\cdots\to(N,m)$ 形成一棵路径树 $P_N$
2. 收缩每条参数边: 将 $N$ 个配置的顶点折叠到 $k=1$ 的对应顶点
3. 四边形面 $f_{k,i,j}$ 提供同伦: 边界为 $(k,i)\to(k,j)\to(k+1,j)\to(k+1,i)\to(k,i)$. 收缩参数边 $(k,j)\to(k+1,j)$ 和 $(k+1,i)\to(k,i)$ 后, 该面退化为连接配置 $k$ 和 $k+1$ 的专家边的同伦
4. 收缩后剩余 $M$ 个顶点 (每个专家一个), 及所有专家边 (从所有 $N$ 个配置来的平行边)
5. 这些平行边对应的 1-循环通过四边形面的退化物彼此同调

**同伦等价的严谨性:**
- 收缩一棵生成树的边总是同伦等价 (树可缩)
- 但此处收缩的是参数边 (属于四边形面的边界), 不是孤立的树边. 四边形面提供了必要的同伦使得收缩"参数边+面"成为形变收缩.
- 经严格分析, 该形变收缩确实正确: 可以按顺序从 $k=N$ 到 $k=2$ 逐层将配置切片 $k$ 推入配置切片 $k-1$, 每步由四边形面提供同伦.

**Betti 数验证:** $\beta_1(K_M) = \binom{M}{2} - (M-1) = (M-1)(M-2)/2$ ✅

**结论:** 同伦等价声明数学正确. 证明可进一步形式化, 但直觉和代数验证均成立.

---

## 三、交叉参考: fiber_bundle.tex vs gauge_formalized.tex

### 3.1 gauge_formalized.tex 对 fiber_bundle.tex 的批评

gauge_formalized.tex Section 5.2 指出 fiber_bundle.tex 的四项缺失:

| 批评 | 评估 |
|------|------|
| **E1**: 仅处理平移群 $\mathbb{R}^d$ | ✅ 正确 — fiber_bundle.tex 有意限制于此, Section 9.2 提及非 Abel 推广但未展开 |
| **E2**: 调和分量的模空间未描述 | ✅ 正确 — fiber_bundle.tex 仅说 $\ker(\Delta_1)$ 是"不可消除残差" |
| **E3**: 调和分量维数隐含暗示错误 | ⚠️ 部分正确 — fiber_bundle.tex 的图圈数与 gauge_formalized.tex 的 2-复形 Betti 数是不同层次的对象 (见 §2.8) |
| **E4**: 无概率解释 | ✅ 正确 — fiber_bundle.tex 仅处理欧氏范数 |
| **E5**: 非 Abel 推广为空 | ✅ 正确 — Section 9.2 仅有概念描述, 无定理/证明/算法 |

### 3.2 fiber_bundle.tex 对 gauge_formalized.tex 的隐含批评

fiber_bundle.tex Section 8 详细论证为何连续纤维丛框架对 SCX 不适用 (F1-F4 错误). gauge_formalized.tex 接受此批评并定位为 discrete Hodge 的**扩展** (非 Abel + TQFT + 信息几何).

### 3.3 两篇论文的一致性

| 概念 | fiber_bundle.tex | gauge_formalized.tex | 一致性 |
|------|-----------------|---------------------|--------|
| 离散 Hodge 分解 | $\Omega^1 = \operatorname{im}(d_0) \oplus \ker(\Delta_1) \oplus \operatorname{im}(d_1^T)$ | 同 (在小联络极限) | ✅ |
| 规范变换 | $A' = A - d_0 g$ | $A_e \mapsto g_v A_e g_u^{-1}$ (非 Abel) | ✅ (Abel 特例一致) |
| Cercis 定义 | $\|P^\perp A\|^2$ | $\min_{d_0 h} \operatorname{GeoDist}(P_A, P_{d_0 h})^2$ | ⚠️ 欧氏 vs Fisher 度量 |
| $\dim\ker(\Delta_1)$ | 圈数 $=NM^2-NM-M+1$ | $\beta_1=(M-1)(M-2)/2$ | ❌ 不同层次 |
| 零模固定 | $\sum g_v = 0$ | 全局常数 $O(d)$ 变换固定 | ✅ |
| 曲率定义 | $d_1 A$ (向量和) | $\operatorname{Hol}(\text{face})$ (Wilson loop) | ✅ (Abel 特例一致) |

---

## 四、定理/证明逐一核实

### 4.1 已有证明且正确的定理

| 定理 | 页/行 | 核实结果 |
|------|-------|----------|
| Thm 2.1: $d_1 d_0 = 0$ | §2, ~290 | ✅ Telescoping sum 证明 |
| Thm 2.2: Hodge 分解 | §2, ~362 | ✅ 标准结果, 声明正确 |
| Prop 3.2: 边赋值规范变换 | §3, ~527 | ✅ 直接代数验证 |
| Prop 3.3: 曲率规范不变性 | §3, ~597 | ✅ $d_1 d_0 = 0$ 的应用 |
| Thm 3.5: 平坦性判据 | §3, ~649 | ✅ 经 a715e95 修复后正确 |
| Thm 3.6: PES 不齐刻画 | §3, ~686 | ✅ $d_1 A \neq 0 \Rightarrow$ 不可能全局对齐 |
| Prop 4.1: 法方程 | §4, ~735 | ✅ 标准最小二乘 |
| Thm 4.2: $\sum g_v = 0$ 是零模固定 | §4, ~765 | ✅ 四项论证严密 |
| Prop 4.3: 闭式解 | §4, ~818 | ✅ 伪逆/增广系统 |
| Prop 4.4: 正交投影解释 | §4, ~852 | ✅ $d_0 g^* = \operatorname{proj}_{\operatorname{im}(B)}(A)$ |
| Thm 5.2: Cercis 规范不变性 | §5, ~939 | ✅ $g'^* = g^* - h$ 保持残差 |
| Prop 6.1: 拓扑平凡性 | §6, ~1031 | ✅ 可缩性 $\Rightarrow$ 分类空间平凡 |
| Prop 6.2: 图同调 | §6, ~1089 | ✅ 图 (1-骨架) 同调正确 |

### 4.2 有问题的定理/注记

| 定理 | 问题 | 严重度 |
|------|------|--------|
| **Lemma: 循环基** | LaTeX 破损 (参数缺失) | 🟡 中 — 渲染问题 |
| **Thm 5.3(v)**: Cercis=0 条件 | 仅要求四边形曲率为零, 缺三角形 | 🔴 高 — 数学漏洞 |
| **Thm 5.3 注记** | "$d_1 A=0$ excludes harmonic component" 方向反了 | 🟡 中 — 概念错误 |
| **Remark 5.2**: Yang-Mills 注记 | $\|d_1 r\|^2 = \|d_1 r_{\text{harm}}\|^2$ 错误 | 🔴 高 — 数学错误 |
| **Remark 5.5**: 代码-论文差距 | LaTeX 破损 + 极限一致性缺证明 | 🟡 中 — 声明不严格 |

---

## 五、修复建议

### 5.1 关键修复

1. **Thm 5.3(v):** 将 "quadrilateral" 改为 "quadrilateral and triangle" (或等价地 "$d_1 A = 0$"):
   ```latex
   \\item $\\curv(\\gamma) = 0$ for all elementary {\\it quadrilateral and triangle} 
         loops $\\gamma$, {\\it and} the {\\bf harmonic} component of $A$ is zero.
   ```

2. **Thm 5.3 注记:** 修正为:
   ```latex
   Note: $d_1 A = 0$ alone guarantees $A$ has no coexact component 
   ($\\operatorname{im}(d_1^T)$), but does not guarantee $A$ is exact — 
   $A$ could still have a non-zero harmonic component in $\\ker(\\Delta_1)$.
   ```

3. **Yang-Mills 注记:** 重写为:
   ```latex
   whereas a Yang-Mills-type functional would capture $\\|d_1 r\\|^2 = 
   \\|d_1 d_1^T \\beta\\|^2$ (the coexact part after applying $d_1$), 
   which differs from both the harmonic norm $\\|r_{\\text{harm}}\\|^2$ 
   (not captured by Yang-Mills, since $d_1 r_{\\text{harm}} = 0$) and 
   the full coexact norm $\\|r_{\\text{coexact}}\\|^2 = \\|d_1^T \\beta\\|^2$.
   ```

### 5.2 次要修复

4. **Lemma 循环基:** 修复缺失的 LaTeX 参数:
   ```latex
   \\item {\\bf Quadrilateral loops:} $(k,i) \\to (k,j) \\to (k+1,j) \\to (k+1,i) \\to (k,i)$
         for all configurations $k$ and expert pairs $i<j$;
   \\item {\\bf Triangle loops:} $(k,i) \\to (k,j) \\to (k,\\ell) \\to (k,i)$
         for all configurations $k$ and distinct experts $i,j,\\ell$.
   ```

5. **Remark 5.5 (代码-论文差距):** 修复 LaTeX 并添加证明草图或标记为 Conjecture.

6. **跨论文一致性:** 在 fiber_bundle.tex 中显式区分 "graph cyclomatic number" 和 "2-complex Betti number", 说明 gauge_formalized.tex 使用的是后者且更物理.

### 5.3 .md 文件同步

fiber_bundle.md 存在类似的问题 (Thm 5.3(v) 仅四边形, Yang-Mills 注记等). 建议同步修复, 同时注意 .md 中 "余正合分量为零" 与 .tex 中 "harmonic component zero" 的不一致 (应统一为后者).

---

## 六、总体评估

| 维度 | 评级 | 说明 |
|------|------|------|
| 离散 Hodge 框架 | A+ | 严格、自包含、准确 |
| 曲率/规范变换/不变性 | A | 构造和证明均正确 |
| 零模固定 $\neq$ Coulomb | A+ | 论文的核心概念贡献, 论证严密 |
| Cercis 定义/规范不变性 | A | 定义唯一、证明正确 |
| 拓扑平凡性声明 | A | 诚实、准确 |
| 平坦性判据 (Thm 3.5) | A | 经 a715e95 修复后正确 |
| Cercis=0 刻画 (Thm 5.3) | C | 条件(v)不足, 注记错误 |
| Yang-Mills 注记 | D | 数学陈述错误 |
| 循环基引理 | B | 数学正确, 但 LaTeX 破损 |
| 代码-论文差距 | B | 声明诚实但 LaTeX 破损+缺证明 |
| 跨论文一致性 | B | $\Delta_1$ 的定义层次需显式区分 |

**总体评级: B+** — 框架坚实, 核心定理正确, 但存在两个中等严重度的数学错误 (Thm 5.3 条件和 Yang-Mills 注记) 和若干 LaTeX 破损, 需要针对性修复. 修复后可升至 A.

**修复优先级:** 1→2→3 (见 §五), 预计工作量 ~30 分钟.
