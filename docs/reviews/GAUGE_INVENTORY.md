# SCX 规范理论完整清查 / Gauge Theory Complete Inventory

> **日期**: 2026-07-03  
> **清查范围**: 5 个核心文件  
> **语言**: 中文  

---

## 文件总览 / File Overview

| # | 文件 | 类型 | 版本 | 行数 | 核心贡献 |
|---|------|------|------|------|----------|
| 1 | `papers/scx_gauge_formalized/gauge_formalized.tex` | 形式化论文 | v2.0 | 1662 | O(d)格点规范 + DW TQFT + 信息几何体-边界对应 |
| 2 | `papers/scx_gauge_physics/gauge_physics.tex` | 物理映射综述 | v1.0 | 1809 | 六大规范理论到SCX的结构类比，诚实声明 |
| 3 | `papers/scx_fiber_bundle/fiber_bundle.tex` | 基础论文 | — | 1681 | 离散Hodge理论，修正连续框架错误 |
| 4 | `papers/supplementary/analysis/gauge_domain_analysis.md` | 域分析裁决 | 正式裁决 | 553 | 九个规范方向的严格三标准评估 |
| 5 | `papers/supplementary/analysis/gauge_domain_formalization.md` | 形式化文档 | — | 708 | 三个复活域的严格定理陈述与证明框架 |

---

## 文件 1: gauge_formalized.tex — 规范理论形式化完成版

### 基本信息
- **副标题**: O(d) Lattice Gauge · Dijkgraaf-Witten Discrete TQFT · Information-Geometric Bulk-Boundary Correspondence
- **定位**: 超越先前 fiber_bundle.tex 的阿贝尔平移规范框架，完成三个互连域的严格数学形式化

### 出发点：先前的三个局限性 (L1-L3)
| 局限 | 描述 |
|------|------|
| L1 | 仅有平移群 R^d，忽略旋转对称性（SO(3)协变的ACE势需要非阿贝尔规范群） |
| L2 | 调和分量的模空间结构未被揭示——"专家系统有多少种本质上不同的不一致方式？" |
| L3 | 无概率解释——Cercis用欧几里得范数定义，但专家输出是概率分布 |

### 三个形式化域 (D1-D3)

#### D1: O(d) 格点规范理论 (Section 2)

**定义和结构:**
- 顶点 O(d) 标架空间: Ω^0(G; O(d))
- 边 O(d) 联络空间 (ACE 势): Ω^1(G; O(d))
- 规范变换群: G ≅ O(d)^|V|，非阿贝尔作用: A_e ↦ g_v ∘ A_e ∘ g_u^{-1}
- 面 Wilson 环路曲率: Hol_A(f) = ∏ A_e^{σ_e} ∈ O(d)

**定理清单:**

| # | 定理 | 内容 | 假设 | 状态 |
|---|------|------|------|------|
| Thm 2.1 | O(d) 平坦性刻画 | 平坦 ⇔ 正合 ⇔ 存在全局O(d)规范对齐 | 面生成所有环路 | 已证明 ✓ |
| Thm 2.2 | O(d) 规范固定定理 — 非阿贝尔离散Hodge分解 | (a) 小联络极限下存在唯一解(模常值规范); (b) 全局存在性由O(d)^|V|紧性保证; (c) 李代数上Hodge分解 | 小联络: max dist(A_e,I) < r_0 | 已证明框架 ✓ |
| Thm 2.3 | O(d) Cercis 规范不变性 | Cercis_Od 在O(d)规范变换下不变 | 双不变距离 | 已证明 ✓ |
| Thm 2.4 | SE(d) 半直积规范群 | 平移和旋转规范固定解耦; 总Cercis = Cercis_Od + Cercis_R^d | SE(d) = R^d ⋊ O(d) | 已证明 ✓ |

**关键引理:**
- Lemma 2.1 (Cartan 分解与局部线性化): 小联络极限下 log(g_v^{-1} A_e g_u) = a_e - (h_v - h_u) + O(||a||²)

**算法:** Riemannian Gauss-Newton 在 O(d)^|V| 上迭代:
1. 李代数线性化 → 2. 图 Hodge 求解 → 3. 指数更新 → 4. 收敛检查
- 每迭代复杂度: O(|E|·d²)
- 收敛性: Cartan半径内线性收敛

**未解决问题:**
- Open Problem: 大畸变下O(d)规范固定的全局极小值分类（与Gribov歧义相关）

#### D2: Dijkgraaf-Witten 离散 TQFT (Section 3)

**SCX 2-复形构造:**
- 顶点: (k,m), |V| = NM
- 边: 参数边 M(N-1) + 专家边 NM(M-1), 总计 |E| = NM² - M
- 面: 四边形 (k,i)→(k,j)→(k+1,j)→(k+1,i), |F| = (N-1)M(M-1)/2

**定理清单:**

| # | 定理 | 内容 | 假设 | 状态 |
|---|------|------|------|------|
| Thm 3.1 | SCX 2-复形的同伦型 | K_SCX ≃ K_M (同伦等价于M个顶点的完全图) | — | 已证明 ✓ |
| Cor 3.1 | Betti数 | β_1 = (M-1)(M-2)/2，仅依赖专家数M，与配置数N无关 | — | 推导 ✓ |
| Thm 3.2 | DW配分函数 | Z_DW(K, G) = |Hom(π_1(K), G)/G| = 平坦联络规范等价类数 | G有限群 | 已证明 ✓ |
| Cor 3.2 | 阿贝尔群DW | Z_DW = |G|^{β_1} | G阿贝尔 | 推导 ✓ |
| Thm 3.3 | DW-Cercis调和分量对应 | T_{[triv]} M_flat ≅ ker(Δ_1) ⊗ g，即Cercis调和分量是平坦联络模空间在平凡联络处的切空间 | 小联络极限 | 已证明 ✓ |
| Thm 3.4 | 调和模空间的几何 | (a) 平移规范: R^{d·β_1}; (b) 旋转规范: so(d)^{β_1}; (c) 离散群: |G|^{β_1}个离散状态 | — | 已证明 ✓ |

**具体算例:**
- M=3: β_1=1, Z_DW = |G| (如 Z_2 → 2个不等价平坦联络)
- M=4: β_1=3, Z_DW(Z_2) = 8 个状态（超立方 {0,1}³）
- M=10, d=3: dim M_flat = 3×36 = 108维"不一致空间"

#### D3: 信息几何体-边界对应 (Section 4)

**关键结构:**
- Situs 流形: (Θ, g), Fisher 信息度量
- 指数族假设: p(x|θ) = h(x)exp(⟨θ,T(x)⟩ - ψ(θ))

**定理清单:**

| # | 定理 | 内容 | 假设 | 状态 |
|---|------|------|------|------|
| Thm 4.1 | Fisher测地-KL条件等价 | d_geo(p,q)² = 2·KL(p||q) + O(||Δθ||³) | 指数族 + 局部逼近 | 已证明（有条件）✓ |
| Thm 4.2 | Cercis的体-边界Fisher测地解释 | Cercis = min_{d_0h ∈ im(d_0)} d_geo(P_A, P_{d_0h})² ≈ 2·min KL(P_A || P_{pure gauge}) | 指数族 + 小联络 | 已证明框架 ✓ |
| Cor 4.1 | Cercis的KL解释 | Cercis_norm ≈ min 2KL / ||A||² | 指数族 | 推导 ✓ |
| Thm 4.3 | KL正则化Cercis | 引入信息瓶颈解释：KL(边) + λ·KL(规范参数先验) | — | 已陈述 ✓ |

**关键引理:**
- Lemma 4.1: KL散度 = Bregman散度（指数族）

**重要警告 (corrigendum):**
- Fisher-KL等价**有条件地**成立：需要指数族假设(H1)和局部逼近假设(H2)
- 在非指数族下，差异由Amari-Chentsov三阶张量控制
- "自然涌现"的说法被降级为"条件等价"

#### 统一结构定理 (Theorem 5.1)

三个域共享单一拓扑不变量: **β_1 = (M-1)(M-2)/2**
- O(d)规范中: 调和1-形式数（每个 so(d) 基元一个）
- DW TQFT中: 平坦联络模空间维数
- 信息几何中: 纯规范体子流形 im(d_0) 的余维数

#### 与 fiber_bundle.tex 的详细比较 (Section 5)

**保留的优点 (S1-S4):**
- S1: 图Hodge理论的正确基础
- S2: 零模固定 ≠ Coulomb规范 的严格区分
- S3: 拓扑平凡性的诚实承认
- S4: Cercis = 残差范数（非Yang-Mills泛函）

**修正的错误/遗漏 (E1-E5):**
- E1: 仅有平移群 R^d → 扩展到O(d)
- E2: 调和分量缺乏模空间解释 → 用DW TQFT填补
- E3: 调和分量维数不精确 → β_1 = (M-1)(M-2)/2
- E4: 无概率解释 → Fisher度量 + KL散度
- E5: 非阿贝尔"推广"空洞 → 完整O(d)理论

#### 开放问题 (5个)
| # | 问题 | 所需工具 |
|---|------|----------|
| 1 | O(d)大畸变下规范固定分支分类 | Morse理论 + O(d)同伦群 |
| 2 | 非指数族下Fisher-KL关系 | Amari-Chentsov张量界 |
| 3 | 有限 (M,N) 的DW配分函数精确值 | Mednykh公式 |
| 4 | 调和模空间的全局几何（奇点） | GIT商分析 |
| 5 | 体-边界对应的全息对偶性 | 离散全息原理（推测性） |

#### 数学断言统计
- 定义: 12个
- 定理(含证明): 9个
- 引理(含证明): 2个
- 命题(含证明): 3个
- 推论: 3个
- 开放问题: 5个
- **无类比或启发式断言**

---

## 文件 2: gauge_physics.tex — 物理映射综述

### 基本信息
- **副标题**: From Electromagnetic Gauge to Spring Lattice: A Survey of Sixty Years of Gauge Theory Physics Transplanted to SCX
- **定位**: 系统性调查六大规范理论核心组件，逐项映射到SCX结构
- **诚实声明**: "本文绝大多数对应是**结构类比**，非严格的数学同构"

### 六大规范理论组件

#### 1. 电磁规范不变性 (§1)
- **物理**: A_μ → A_μ + ∂_μΛ, F_μν规范不变量, Coulomb/Lorenz规范
- **SCX对应**: g_m → g_m + c, Cercis Score规范不变量, Σg_m = 0
- **诚实修正**: Σg_m = 0 是零模固定（Ω⁰空间），非Coulomb规范（Ω¹空间）
- **可采纳工具**: 协变导数形式化、场强张量、规范固定条件分类、Noether定理

#### 2. Yang-Mills 非阿贝尔规范理论 (§2)
- **物理**: F_μν = ∂_μA_ν - ∂_νA_μ + ig[A_μ,A_ν], 纤维丛几何
- **SCX对应**: G = ∏G_m（含O(d)非阿贝尔子群）, Situs流形=底流形, MILP=截面选择
- **诚实修正**: 离散Hodge理论应为正确框架（非连续纤维丛）; 图Betti数替代Chern类
- **可采纳工具**: 瞬子=规范跳跃, 渐近自由=高通量规范解耦, 禁闭=单专家输出无绝对意义

#### 3. Higgs机制：自发对称破缺 (§3)
- **物理**: V(φ) = -μ²|φ|² + λ|φ|⁴, 动力学破缺
- **SCX对应**: 显式破缺（分析者选择约束），非自发
- **诚实区分** (6项差异表): 破缺模式、驱动力、真空简并、Goldstone模、相变、质量产生——全部不同
- **更好的类比**: 广义相对论中的坐标选择
- **可采纳工具**: 有效势能形式化、零模=Goldstone模、幺正规范选择

#### 4. BRST 量子化 (§4)
- **物理**: Q²=0幂零算子, 物理态=BRST上同调类, 鬼场
- **SCX对应**: 审计算子Q（形式构造：Q(g_m)=c_m, Q(c_m)=0）
- **诚实修正**: 这是平凡2-步链复形，不是真正的BRST（缺少[A_μ,c]对易子项）
- **核心价值**: ker(Q)/im(Q) → Yajie共识的形式化数学定义
- **可采纳工具**: 幂零审计算子、上同调完备性判据、规范固定拉氏量、Slavnov-Taylor恒等式

#### 5. 规范反常与反常抵消 (§5)
- **物理**: Tr[T^a{T^b,T^c}] = 0, 费米子三角图
- **SCX对应**: Σg_m = 0（零模固定）
- **诚实修正**: 量子反常 ≠ 经典零模固定。机制完全不同。
- **"诚实人定理"**: 信息论反常——单个观察者无法区分真相和噪声
- **可采纳工具**: 反常系数系统计算、Wess-Zumino有效作用量、反常流入机制

#### 6. 格点规范理论 (§6)
- **物理**: Wilson作用量、链接变量、plaquette、面积律/周长律
- **SCX对应**: Spring框架状态离散化 = 格点离散化
- **可采纳工具**: Wilson作用量Spring版、面积/周长律分类、Monte Carlo算法、改进作用量(Symanzik)

#### 总体对应表 (Section 7)
包含约60+项详细对应，成熟度分四个等级:
- ★★★ 已验证
- ★★☆ 部分验证  
- ★☆☆ 推测
- — 待探索

#### 高优先级采纳清单 (Section 8)
1. 采纳离散Hodge框架（替代纤维丛）
2. BRST上同调作为审计完备性判据
3. Wilson作用量 + 面积/周长律
4. 诚实承认拓扑平凡性
5. Slavnov-Taylor恒等式验证
6. 全局反常检测
7. Monte Carlo算法移植
8. 改进作用量和标度分析

#### 中等优先级理论方向
- 瞬子和规范跳跃
- 渐近自由和规范解耦
- θ-真空和规范固定简并
- **AdS/CFT对偶 SCX版**（后被 gauge_domain_analysis.md 判定为 DEAD END）
- 格点规范相变

#### 文件核心论点 (Section 9)
> "规范场论和SCX共享同一个数学结构并非巧合——它们处理的是同一个根本问题：**从冗余表示中提取不变量**。"

---

## 文件 3: fiber_bundle.tex — 离散Hodge理论基础

### 基本信息
- **副标题**: Discrete Geometry of PES Misalignment: A Graph Hodge Formalization of SCX Gauge Theory
- **定位**: 放弃连续纤维丛前导，直接在离散图Hodge理论上建立SCX规范理论
- **文件功能**: 严格基础 + 错误修正

### 核心贡献

#### 1. 离散Hodge理论基础工具箱 (Section 2)

| 结构 | 定义 | 关键属性 |
|------|------|----------|
| 有向图 G=(V,E) | |V|=n, |E|=m |
| 0-形式空间 Ω⁰ | 顶点函数 f: V→R | dim=n |
| 1-形式空间 Ω¹ | 边赋值 α: E→R | dim=m |
| 关联矩阵 B | B_{e,w} = ±1 | d₀ = B |
| 循环矩阵 C | C_{γ,e} = ±1 | d₁ = C |
| 基本恒等式 | d₁∘d₀ = C·B = 0 | 离散 de Rham |
| 伴随算子 d₀† | = W₀^{-1} B^T W₁ | 离散散度 |
| 0-Laplacian Δ₀ | = d₀† d₀ = B^T B (无权) | |
| 1-Laplacian Δ₁ | = d₀ d₀† + d₁† d₁ | |

**Theorem 2.1 (离散Hodge分解):**
Ω¹(G) = im(d₀) ⊕ ker(Δ₁) ⊕ im(d₁†)
- im(d₀): 正合1-形式（梯度部分）
- ker(Δ₁): 调和1-形式（既无散度又无旋度）
- im(d₁†): 余正合1-形式

**重要注释**: SCX计算只用"下部" B^T B，但调和分解需要完整 Δ₁。

#### 2. SCX图的构造 (Section 3)

- 顶点: (k,m) ——每个(配置,专家)对
- 参数边: (k,m)→(k+1,m) ——同一专家沿参数轴的变化
- 专家边: (k,i)→(k,j) ——同一配置下不同专家的位移
- 边赋值: **直接数据**（非连续联络的离散化）
- 初等环路: 四边形(k,i)→(k,j)→(k+1,j)→(k+1,i)

**曲率 = 环路和乐:**
curv(γ_{k,i,j}) = (x̃_i^k - x̃_i^{k+1}) - (x̃_j^k - x̃_j^{k+1})
几何解释: 度量专家i和j的预测在参数变化下的**差异**

**Proposition 3.1 (曲率规范不变性):** curv'(γ) = curv(γ)，因为 d₁d₀ = 0。

**Theorem 3.1 (平坦性判据——调和修正版):**
当调和分量为零时，以下等价:
- 所有初等环路的曲率为零
- A是正合的 (A = d₀g)
- 存在全局规范对齐

关键修正: d₁A = 0 **不蕴含** A ∈ im(d₀)（当调和分量非零时）

#### 3. 规范固定 (§4)

**最小二乘问题:** min_g ||A - d₀g||²

**正规方程:** B^T B · g = B^T A （即 Δ₀ g = d₀† A）

**Theorem 4.1 (Σg_v = 0 是零模固定，非Coulomb规范):**
四个理由:
1. 约束对象不同（规范参数 vs 规范势）
2. 数学类型不同（代数 vs 微分）
3. 连续类比不同（∫Λdx=0 vs ∂_μA^μ=0）
4. 计算角色不同（伪逆选择 vs 散度条件）

**Proposition 4.1 (解):** g* = (B^T B)^+ B^T A ——Moore-Penrose伪逆

**几何解释:** 规范固定 = 正交投影到 im(B)

#### 4. Cercis Score (§5)

**唯一定义:** Cercis = ||A - d₀g*||² = ||P^⊥ A||²

**Theorem 5.1 (规范不变性):** Cercis在规范变换下不变

**Theorem 5.2 (Cercis=0的刻画):**
Cercis=0 ⇔ A正合 ⇔ A ∈ im(d₀) ⇔ 完美全局对齐 ⇔ (d₁A=0 且 调和分量为零)

关键: 调和分量非零时，即使曲率为零，Cercis也可能>0。

**重要注释 (Remark 5.1):**
Cercis **不是** Yang-Mills泛函 ∫||F||²。
Cercis = ||r_ham||² + ||r_coexact||²（包含调和+余正合部分）
Yang-Mills型泛函只捕获 ||d₁ r_coexact||²（仅余正合部分）

**Remark 5.2 (代码-论文差距):**
- 理论理想: Cercis = ||P^⊥ A||²（离散Hodge残差）
- 生产代码: Cercis(s) = Q(s) + η(t)·N(s)（投票+新颖性）
- 差距是开放工程问题

#### 5. 拓扑平凡性的诚实承认 (§6)

**Proposition 6.1 (SCX丛拓扑平凡):**
1. 结构群 G ≅ R^{Md} 可缩
2. 底空间 X ⊂ R^K 可缩
3. 分类空间平凡: [X, BG] = {*}
4. 所有示性类为零: c_k(P)=0, H^k(X;R)=0

**结论**: 内容是几何的（平坦 vs 非平坦），非拓扑的。

**图视角下的"拓扑"内容:**
- H₀(G) ≅ R（连通分量）
- H₁(G) ≅ R^{|L|}（独立环路数）
- 图Betti数 = 调和1-形式空间的维数

#### 6. 数值算法 (§7)
完整的7步管线和复杂度分析: O(NM²)边构造 → O(sparse)求解 → O(NM²d) Cercis计算

#### 7. 与先前连续框架的系统对比 (§8-9)

**连续框架的4个根本缺陷 (F1-F4):**
- F1: Σg_m=0误称为Coulomb规范
- F2: 联络ω从未被构造
- F3: Cercis定义不一致（在∫||F||²和Q+ηN之间摇摆）
- F4: 拓扑被误表述

**连续框架需要完成才能成为有效替代的5个条件 (C1-C5):**
- C1: 从离散数据显式构造联络
- C2: 证明离散化一致性
- C3: 识别实际存在的非平凡拓扑
- C4: 精确关联Cercis与Yang-Mills泛函
- C5: 正确定义Coulomb规范的离散类比

**核心结论**: 离散图Hodge理论是SCX规范理论的**权威形式化**。

---

## 文件 4: gauge_domain_analysis.md — 九域严格裁决

### 基本信息
- **方法论**: 每个域按三个标准评估: (1)可移植性 (2)新颖性 (3)审计提升
- **裁决等级**: MUST FORMALIZE / USEFUL ANALOGY / DEAD END / ALREADY DONE

### 裁决汇总表

| # | 域 | 裁决 | 核心理由 |
|---|-----|------|----------|
| 1 | **U(1) 电磁规范** | **ALREADY DONE** | SCX基础设施已完成。离散Hodge框架已覆盖。无新数学。 |
| 2 | **Yang-Mills 非阿贝尔** | **DEAD END** | ∏的非阿贝尔性 ≠ SU(N)的非阿贝尔规范场。范畴错误。 |
| 3 | **格点规范 (Wilson环路+面积/周长律)** | **MUST FORMALIZE** ⭐ | 三类全过。区分系统性偏差 vs 局部噪声。严格可移植+新颖+实质性审计提升。 |
| 4 | **纤维丛+Chern类** | **DEAD END** | 底空间和结构群可缩→所有示性类为零。ker(Δ₁)已做同样工作。 |
| 5 | **BRST上同调** | **MUST FORMALIZE** ⭐ | Q²=0+上同调→Yajie共识严格数学定义。区分真知识 vs 规范伪影。 |
| 6 | **反常抵消** | **USEFUL ANALOGY** | 量子反常≠经典零模固定。"自洽性约束"概念有价值但不能数学移植。 |
| 7 | **自发对称破缺/Higgs** | **DEAD END** | 显式固定=特征非缺陷。"自发涌现"不可操作+审计上不可取。 |
| 8 | **TQFT/Chern-Simons** | **DEAD END** | 维度不兼容（要求3维）。组合拓扑（Betti数）已足够。审计不需纽结不变量。 |
| 9 | **AdS/CFT对偶** | **DEAD END** | 最不可辩护的方向。弦论奇迹≠审计工具。应使用信息几何替代。 |

### 两个 MUST FORMALIZE 方向的路线图

#### 方向A: 格点规范 — Wilson环路 + 面积/周长律分类
1. **修正Theorem 3**: d₁A=0 + A⟂ker(Δ₁) ⇔ A∈im(d₀)
2. **定义SCX Wilson环路族** W_k(C)
3. **证明分类定理**: 存在阈值k_c，k<k_c周长律（局部噪声），k>k_c面积律（系统性偏差）
4. **算法规约**: 可计算的分类算法

#### 方向B: BRST上同调 — 审计算子 + Yajie共识形式化
1. **定义审计算子Q**: Q作用于边空间，Q=d₁或其变体，证明Q²=0
2. **计算上同调群**: H¹(Q) = ker(d₁)/im(d₀) ≅ ker(Δ₁)
3. **Yajie共识定理**: K∈ker(Q)且K∉im(Q) ⇒ K是Yajie共识元素
4. **审计完备性定理**: 若H¹(Q)=0（图是树），所有Cercis非零必来自专家噪声

### 方法论附注
- 严格区分**数学移植**和**概念类比**
- 诚实命名规则: 若数学类型不同，不用同一个名字
  - Σg_m=0 → "零模固定"，不是"反常抵消"
  - Q(g_m)=c_m → "离散de Rham上同调"，不是"BRST"

### 最终结论
> 九个方向中，七个是DEAD END或已完成。两个真正值得形式化：格点规范（面积/周长律）和BRST上同调（共识形式化）。

---

## 文件 5: gauge_domain_formalization.md — 复活域的严格形式化

### 基本信息
- **前置文档**: gauge_domain_analysis.md, gauge_domain_reexam.md, GAUGE_REVIEW_3.md
- **方法论**: 对每个复活域：(1)精确陈述定理 (2)列出所有假设 (3)提供证明框架或诚实声明"被X阻塞" (4)若被阻塞，精确说明缺少什么数学结果
- **原则**: 不写类比。不写"启发"。只写定理。

### 域1: O(d) 格点规范理论

**定义:**
- SCX专家图上的O(d)标架: R_v ∈ O(d)（顶点v处ACE基函数的局部定向）
- 离散O(d)联络: U_{vw} = R_v^T R_w ∈ O(d)
- Plaquette和乐: W_f = U_{ij}U_{jk}U_{ki} ∈ O(d)

**定理1.1 (O(d)平坦联络分类):**
- (a) 平坦O(d)联络的规范等价类 ≅ Hom(π₁(G), O(d))/O(d)
- (b) 当b₁=0（树），所有平坦联络是纯规范的
- (c) 当b₁≥1，平坦联络模空间维数 = d(d-1)/2 · max(b₁-1, 0)

假设: G连通、边定向一致、π₁自由（自动满足）、O(d)连通李群

**定理1.2 (非阿贝尔离散Hodge问题):**
- (a) S({R_v}) = Σ||R_v^T R_w - U_{vw}||²_F 的一阶必要条件
- (b) d=1时（O(1)={±1}）简化为Z₂-值Ising型问题，多项式时间可解
- (c) d≥2时是O(d)^{|V|}上的非凸优化，无闭式解

阻塞:
- B1.2.1 (中等): d≥2时S的局部极小值完整分类
- B1.2.2 (中等): Riemannian优化收敛速率

**定理1.3 (O(d)和乐作为不可消除偏差诊断):**
- (a) 消失判据: W_f=I ∀f ⇔ 联络平坦
- (b) 不可消除性: ∃W_f≠I ⇒ 无局部规范变换可同时消除所有和乐
- (c) 偏差分解: W_f = R(θ_f)·S_f（旋转角θ_f度量标架扭曲程度）
- (d) 面积律预判: ||W_large - I|| ~ exp(σk²)面积律（系统性O(d)偏差）vs ~ exp(αk)周长律（局部噪声）

严重阻塞 B1.3.1: (d)的严格证明在离散O(d)格点规范中**未被证明**——其严格证明是Yang-Mills质量间隙问题级别。**修正方案**: 将(d)从定理降级为"猜想1.3"。

### 域4: Dijkgraaf-Witten 离散 TQFT

**定义:**
- SCX专家图为2-复形 M=(V,E,F)
- 离散G-规范场: g: E→G
- DW配分函数: Z_ω(M) = |G|^{-|V|} Σ_{g:E→G} ∏_{f∈F} ω(g_{ij}, g_{jk})
- 非平凡2-cocycle ω ∈ Z²(G, U(1))

**定理2.1 (平坦G-联络的计数):**
- (a) |F(M,G)/G| = |Hom(π₁(M), G)|/|G|（拓扑不变量）
- (b) 当π₁(M)≅Z^{*b₁}且G有限: |F/G| = |G|^{b₁-1}
- (c) 阿贝尔群修正: |F/G| = |G|^{b₁}（共轭作用平凡）

阻塞:
- B2.1.1 (低): 非自由π₁时的精确计数
- B2.1.2 (中等): 连续群极限过渡

**定理2.2 (DW不变量作为SCX审计诊断):**
- (a) 拓扑不变性: 同伦等价的M₁,M₂有相同Z_ω
- (b) 超越Betti数的区分能力: 存在同调相同但Z_ω不同的例子（lens空间）
- (c) 平坦与扭曲的区别: 平凡ω→仅依赖|E|-|V|; 非平凡ω→捕获调和分量无法区分的全局结构
- (d) SCX审计翻译: Z_ω(M)≠Z_ω(M_ref)表示包含拓扑上不可约简的全局不一致性

严重阻塞:
- B2.2.1: SCX专家图的2-复形结构需精确定义（面的粘合映射）
- B2.2.2: ω的审计物理解释缺失——"ω代表审计中的什么？"

**定理2.3 (离散BF理论与调和分量维数):**
Z_BF(M; G) = |G|^{b₁(M)}（阿贝尔群G）
- 建立了从"离散TQFT"到"SCX已有结构"的严格桥梁
- **fiber_bundle.tex Theorem 3的错误根源**: 遗漏了|G|^{b₁}因子

**与fiber_bundle.tex Theorem 3的关系:**
Theorem 3声称"曲率=0对所有plaquette ⇔ A正合 ⇔ Cercis=0"——这**不成立**。
修正: 曲率条件需加入 ⟨A, h_i⟩ = 0（h_i为ker(Δ₁)的基），即调和分量为零。

### 域5: 信息几何体-边界对应

**定义:**
- Situs流形: (Θ, g), Fisher信息度量
- KL散度 = Bregman散度（指数族）
- Spring训练 = "体"梯度流; Cercis = "边界"观测

**定理3.1 (Cercis-Fisher测地等价):**
- (a) D_KL(p_θ̄ || p_θ̂_m) = ½||Δθ_m||²_g + O(||Δθ||³)
- (b) Cercis² ∝ (1/M)Σ D_KL(p_θ̄ || p_θ̂_m)（比例常数由g(θ̄)特征值决定）
- (c) d_FR(θ̄, θ̂_m) = ||Δθ_m||_g + O(||Δθ||²)
- (d) 体-边界解释: Spring轨迹长度 ≈ √Cercis（推测性）

阻塞:
- B3.1.1 (中等): Spring是否使用自然梯度流？
- B3.1.2 (中等): Euclidean→Fisher范数转换常数依赖g(θ̄)条件数
- B3.1.3 (低): ACE输出到概率分布的嵌入映射

**定理3.2 (Cercis的Bregman散度刻画):**
- (a) 广义Cercis: Cercis_IG = (1/M)√(Σ D_ψ(θ̂_m || θ̄))
- (b) Bregman三角形等式: 将专家对差异分解为"各自到共识+交叉项"

### 跨域结构关系

**定理X.1 (调和分量=BF配分函数):**
统一了域1和域4: 两者都是SCX图上平坦规范场规范等价类的计数。差异来自规范群是否为阿贝尔（平移 vs O(d)旋转）。

**定理X.2 (信息几何度量曲率与和乐):**
Fisher度量曲率R_{ijkℓ}对离散联络的plaquette和乐产生贡献。当Fisher度量弯曲时，Cercis包含信息几何曲率贡献。
- **严重阻塞 B_G8**: 要求dim Θ = d(d-1)/2且非平凡曲率耦合——通用SCX不满足。

### 未解决的形式化缺口汇总 (G1-G8)

| # | 域 | 缺口 | 严重性 |
|---|-----|------|--------|
| G1 | 1 | 面积律/周长律严格证明 | **严重** |
| G2 | 1 | O(d)规范固定优化收敛速率 | 中等 |
| G3 | 4 | 2-复形精确定义 | **严重** |
| G4 | 4 | DW cocycle ω的审计物理解释 | **严重** |
| G5 | 4 | 李群连续极限计数→维数过渡 | 中等 |
| G6 | 5 | Spring动力学是否为自然梯度流 | 中等 |
| G7 | 5 | Cercis Euclidean→Fisher范数转换 | 低 |
| G8 | 跨域 | Fisher曲率对O(d)和乐的贡献 | **严重** |

### 诚实性声明
1. 每个定理或被证明，或被诚实声明为"阻塞"——无"好像可以证明"
2. 不做概念类比
3. 命名精确: O(d)格点规范≠Yang-Mills; DW≠Chern-Simons; 信息几何≠AdS/CFT
4. 区分定理、猜想和推测

### 最终结论
> 三个复活域构成统一数学图景：**SCX审计的"调和分量缺失"（fiber_bundle.tex Theorem 3的错误）是离散平坦联络的规范等价类——它是拓扑的，可通过TQFT计数，且可在信息几何中赋予度量解释。**

---

## 跨文件连接图 / Cross-File Connections

### 核心概念流 / Core Concept Flow

```
fiber_bundle.tex          gauge_formalized.tex        gauge_domain_formalization.md
(离散Hodge基础)    ←→    (三域形式化完成)      ←→    (复活域定理严格化)
     ↓                          ↓                            ↓
  图Hodge分解              O(d)+DW+信息几何              阻塞声明+证明框架
     ↓                          ↓                            ↓
  Cercis定义               统一结构定理                  形式化缺口G1-G8
     ↓                          ↓                            ↓
  拓扑平凡性               与fiber_bundle比较             定理/猜想/推测分类
     
gauge_physics.tex  ←→  gauge_domain_analysis.md
(物理类比映射)          (九域严格裁决)
     ↓                       ↓
  六大规范理论             MUST FORMALIZE ×2
  诚实类比声明             DEAD END ×5
  采纳建议                 USEFUL ANALOGY ×1
                           ALREADY DONE ×1
```

### 关键定理的跨文件引用

| 定理 | gauge_formalized | fiber_bundle | gauge_domain_formalization |
|------|:---:|:---:|:---:|
| 离散Hodge分解 | Thm 2.4(c)依赖 | Thm 2.1 (完整陈述) | 基础前提 |
| 零模固定 ≠ Coulomb | Remark引用 | Thm 4.1 (核心修正) | 诚实命名原则 |
| 拓扑平凡性 | §5.2 进一步注释 | §6 (完整承认) | 域4裁决依据 |
| Cercis = 残差范数 | Thm 4.2 (Fisher推广) | Def 5.1 (唯一定义) | — |
| β_1 = (M-1)(M-2)/2 | Thm 3.1 | 3.5节暗示 | Thm 1.1 隐含 |
| DW配分函数 | Thm 3.2 | — | Thm 2.1-2.3 |
| Fisher-KL等价 | Thm 4.1 (有条件) | — | Thm 3.1 |
| 调和分量=模空间切空间 | Thm 3.3 | — | Theorem 2.3 |
| 面积律/周长律 | — | — | Thm 1.3(d) → Conjecture |

### 文件间的修正关系

1. **fiber_bundle.tex 修正 gauge_physics.tex**:
   - Σg_m=0 从 "Coulomb规范" 修正为 "零模固定"
   - Cercis 从 "Yang-Mills泛函/Q+ηN" 统一为 "残差范数"
   - 拓扑从 "非平凡" 修正为 "平凡"

2. **gauge_formalized.tex 扩展 fiber_bundle.tex**:
   - 从 R^d (阿贝尔平移) → O(d) (非阿贝尔旋转)
   - 补充调和分量的模空间几何意义
   - 补充信息几何的概率解释
   - 修正调和分量维数的不精确表述

3. **gauge_domain_analysis.md 裁决 gauge_physics.tex 的九个方向**:
   - 5个 DEAD END（含AdS/CFT、Chern-Simons等）
   - 2个 MUST FORMALIZE（格点规范、BRST上同调）
   - 1个 USEFUL ANALOGY（反常抵消）
   - 1个 ALREADY DONE（U(1)电磁规范）

4. **gauge_domain_formalization.md 严格化三个复活域**:
   - 将 gauge_domain_analysis.md 的 MUST FORMALIZE 方向 + 一个复活域（O(d)格点规范）转化为精确定理
   - 识别8个形式化缺口（G1-G8），其中4个为严重

---

## 全局假设清单 / Global Assumptions Inventory

### 所有文件共有的核心假设

| # | 假设 | 影响范围 | 后果若违反 |
|---|------|----------|------------|
| H1 | SCX图是连通的 | 所有文件 | 不连通可分解为各分量独立分析 |
| H2 | 底空间（Situs流形）可缩 | fiber_bundle, gauge_formalized | 所有Chern类为零；若不可缩（如有孔洞），拓扑内容非平凡 |
| H3 | 平移规范群 R^d 是阿贝尔的 | 所有文件 | 若非阿贝尔，离散Hodge分解的简单形式不成立 |
| H4 | 边赋值A_e是直接数据（非连续联络的离散化） | fiber_bundle | 这是离散框架的本体论基础 |

### gauge_formalized.tex 特有假设

| # | 假设 | 定理 | 后果若违反 |
|---|------|------|------------|
| H5 | 小联络: max dist(A_e, I_d) < r_0 | Thm 2.2(a,c) | 李代数线性化失效，需完整非凸优化 |
| H6 | 面集F生成π₁ | Thm 2.1, 3.3 | 平坦性条件不完整 |
| H7 | 指数族 | Thm 4.1, 4.2 | Fisher-KL等价退化，由Amari-Chentsov张量控制 |
| H8 | 局部逼近: ||Δθ||小 | Thm 4.1, 4.2 | Fisher-KL的二阶展开失效 |

### gauge_domain_formalization.md 特有假设

| # | 假设 | 定理 | 阻塞 |
|---|------|------|------|
| H9 | G是有限群 | Thm 2.1 | 连续群需维数替代计数 |
| H10 | π₁(M) ≅ Z^{*b₁} (自由群) | Thm 1.1, 2.1 | 非自由π₁需完整表示论 |
| H11 | 2-复形结构完整定义 | Thm 2.2 | **G3: 面的粘合映射未定义** |

---

## 全局局限清单 / Global Limitations Inventory

### 数学层面的局限

| # | 局限 | 来源文件 | 严重性 |
|---|------|----------|--------|
| L1 | O(d)规范固定在大畸变下无闭式解 | gauge_formalized §2.5 | 中等 |
| L2 | O(d)大畸变极小值分类未解决（Gribov歧义） | gauge_formalized Open Problem 1 | 中等 |
| L3 | 面积律/周长律分类定理未经严格证明 | gauge_domain_formalization B1.3.1 | **严重** |
| L4 | 非指数族下Fisher-KL等价失效 | gauge_formalized Open Problem 2 | 中等 |
| L5 | Fisher曲率→O(d)和乐的贡献仅在极特殊设定下非平凡 | gauge_domain_formalization B_G8 | **严重** |
| L6 | 2-复形面的粘合映射未精确定义 | gauge_domain_formalization B2.2.1 | **严重** |
| L7 | DW cocycle ω缺少审计物理解释 | gauge_domain_formalization B2.2.2 | **严重** |
| L8 | 连续群极限中计数→维数过渡未建立 | gauge_domain_formalization B2.1.2 | 中等 |

### 物理-审计对应层面的局限

| # | 局限 | 来源文件 | 说明 |
|---|------|----------|------|
| L9 | Yang-Mills非阿贝尔结构与SCX的∏-非阿贝尔性是范畴错误 | gauge_domain_analysis §2 | SCX的规范群是独立因子的直积，非SU(N)型 |
| L10 | Chern类恒为零——纤维丛框架在此不产生非平凡输出 | fiber_bundle §6, gauge_domain_analysis §4 | 调和分量ker(Δ₁)已提供等价信息 |
| L11 | Σg_m=0 不是反常抵消——是经典零模固定 | gauge_physics §5, gauge_domain_analysis §6 | 数学形式相似但机制完全不同 |
| L12 | 显式规范固定不是自发对称破缺 | gauge_physics §3, gauge_domain_analysis §7 | 这是特征，非缺陷 |
| L13 | SCX的BRST是平凡2-步链复形（缺[A_μ,c]对易子项） | gauge_domain_analysis §5 | Q(g_m)=c_m不是真正的BRST |
| L14 | 理论Cercis（||P^⊥A||²）与生产代码Cercis（Q+ηN）存在差距 | fiber_bundle Remark 5.2 | 开放工程问题 |

### 设定层面的局限

| # | 局限 | 说明 |
|---|------|------|
| L15 | 所有结论依赖图连通性假设 | 不连通时需分量分解 |
| L16 | 所有结论依赖底空间/结构群可缩假设 | 若未来SCX设定改变（如有孔洞的参数空间），某些"DEAD END"方向可能复活 |
| L17 | 平移规范仅覆盖R^d（阿贝尔）——旋转规范O(d)仅在gauge_formalized中完整处理 | fiber_bundle仅处理平移 |

---

## SCX其他方向的连接 / Connections to Other SCX Directions

| SCX概念 | 规范理论连接 | 涉及文件 |
|---------|-------------|----------|
| **Cercis Score** | 规范不变可观测（类比F_μν），Fisher测地距离 | 全部5个文件 |
| **Situs流形** | 底空间/Fisher信息流形 | gauge_formalized §4, gauge_physics §2 |
| **Spring框架** | 格点离散化（类比格点QCD） | gauge_physics §6 |
| **ACE势** | O(d)联络的物理来源（原子环境旋转响应） | gauge_formalized §2 |
| **Yajie共识** | BRST上同调类 ker(Q)/im(Q) | gauge_physics §4, gauge_domain_analysis §5 |
| **MILP规范固定** | 纤维丛截面选择 | gauge_physics §2 |
| **M_t参数** | Wilson环路类比 | gauge_physics §2, §6 |
| **PES失配** | 离散曲率 = 专家预测变化的差异 | fiber_bundle §3 |
| **持久同调** | H₁持久条形码区分"真调和模"与"有限尺寸效应" | gauge_formalized §7 |

---

## 版本状态 / Version Status

| 文件 | 版本 | 状态 | 与清查的关系 |
|------|------|------|-------------|
| gauge_formalized.tex | v2.0 | Preprint | **最新最完整的形式化** |
| gauge_physics.tex | v1.0 | Preprint | 物理映射综述，多处类比被后续文件修正 |
| fiber_bundle.tex | — | — | 离散Hodge基础，**权威形式化** |
| gauge_domain_analysis.md | 正式裁决 | Final | 严格的优先级判断 |
| gauge_domain_formalization.md | — | — | 复活域定理级严格化 |

### 已知矛盾与待协调项

1. **gauge_physics.tex §9.5 将 AdS/CFT 列为"中等优先级"** vs **gauge_domain_analysis.md §9 判定为 DEAD END**——后者认为应删除此方向。

2. **gauge_physics.tex 多处使用"BRST"名称** vs **gauge_domain_analysis.md 指出这是"平凡2-步链复形"**——后者要求诚实命名为"离散de Rham上同调"。

3. **gauge_physics.tex 将 Σg_m=0 称为"反常抵消"** vs **三个后续文件均修正为"零模固定"**。

4. **gauge_domain_analysis.md 将BRST列为 MUST FORMALIZE (#2)** vs **gauge_domain_formalization.md 中BRST未出现在三个复活域中**（复活的是O(d)格点规范、DW TQFT、信息几何）——BRST的形式化路线图已给出但尚未执行。

5. **fiber_bundle.tex Theorem 3（平坦性判据）** vs **gauge_formalized.tex Thm 3.1 / gauge_domain_formalization.tex Thm 2.3**——前者缺少调和分量条件，已被后者修正。

---

> **清查完成日期**: 2026-07-03  
> **清查原则**: 每项结果标注假设、局限、证明状态和跨文件连接。无类比表述。  
> **下一步建议**: 
> 1. 解决形式化缺口 G1（面积律）、G3（2-复形定义）、G4（ω审计解释）
> 2. 执行 BRST 上同调形式化路线图
> 3. 协调 gauge_physics.tex 中的类比表述与后续严格文件
> 4. 关闭 Cercis 理论定义与生产代码之间的差距
