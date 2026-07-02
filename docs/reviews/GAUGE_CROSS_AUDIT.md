# SCX 规范应用论文交叉审计报告

> **日期**: 2026-07-03  
> **审计范围**: fiber_bundle.md, fiber_bundle.tex, gauge_physics.tex, gauge_domain_analysis.md, gauge_domain_formalization.md, gauge_formalized.tex  
> **审计目标**: 验证修复后各论文之间的一致性，检查交叉引用是否正确

---

## 一、审计总结 / Executive Summary

| 检查项 | 结果 | 严重性 |
|--------|------|--------|
| fiber_bundle.md 是否包含 fiber_bundle.tex 中已修复的错误 | ✅ 已同步修复 | — |
| gauge_physics.tex 是否引用修复后的定理 | ⚠️ 部分引用，但仍有残留混淆 | 中 |
| dim(ker(Δ₁)) 值跨论文是否一致 | ✅ 一致（不同图结构下预期不同） | — |
| supplementary 文件与 gauge_formalized.tex 一致性 | ✅ 完全一致 | — |
| 整体跨论文一致性评级 | **良好，有 2 项轻微问题** | — |

---

## 二、逐项详细分析 / Detailed Analysis

### 2.1 fiber_bundle.md 与 fiber_bundle.tex 的一致性

#### 检查点 CP-1：平坦性定理（原 Theorem 3 的修复）

**fiber_bundle.tex 修复状态（✅ 已修复）**:
- 定理 `thm:flatness`（第 650 行）明确加入了前提条件："When the harmonic component of the Hodge decomposition vanishes"
- 证明中指出：$\ker(d_1) = \operatorname{im}(d_0) \oplus \ker(\Delta_1)$，需调和分量为零才能推出 $A$ 是正合的
- 显式引用 `thm:cercis_zero` 提供包含调和分量的完整刻画
- 对 $M=1$ 或 $M=2$（$\beta_1=0$）的情况，等价性无条件成立

**fiber_bundle.md 修复状态（✅ 已同步修复）**:
- Markdown 版本第 639–658 行同样包含了调和分量的注释：
  > "需注意图有回路时 $\ker(d_1) = \operatorname{im}(d_0) \oplus \ker(\Lone)$。…若调和分量非零，$A$ 仍可满足 $d_1 A = 0$ 但不是正合的。"
- 定理 `thm:cercis_zero`（第 998–1018 行）的条件 (v) 正确包含"且余正合分量为零"

**结论**: ✅ 两个版本在核心修复上一致。

#### 检查点 CP-2：Yang-Mills 相关声明

**fiber_bundle.tex**:
- 第 919–935 行 Remark 明确声明："Cercis Is Not the Yang-Mills Functional"——Cercis 是残差范数，不是 $\int \|F\|^2$
- 正确区分 Cercis = $\|r_{\text{harm}}\|^2 + \|r_{\text{coexact}}\|^2$，而 Yang-Mills 型泛函仅捕获 $\|d_1 r\|^2$

**fiber_bundle.md**:
- 第 942–969 行 Remark 同样声明："本文中的 Cercis 分数**不是** Yang-Mills 泛函"
- 内容与 .tex 版本一致

**结论**: ✅ Yang-Mills 与 Cercis 的区分在两个版本中一致。

#### 检查点 CP-3：回路基 (Cycle Basis) 定义

**两个版本**:
- 都使用"基本回路 (elementary loops)"由生成树的补边确定的标准定义
- `d_1 := C`（回路矩阵）的定义一致
- **注意**: 论文中没有"Theorem 5.3"这样的编号——定理按节编号（如 `thm:flatness`, `thm:cercis_zero`），在编译后的 PDF 中才显示为"Theorem 5.x"。两个源文件中使用 `\label` 和 `[ref]` 占位符而非硬编码编号，这是**正确的做法**。

**结论**: ✅ 回路基定义一致。不存在 "Thm 5.3" 的硬编码引用问题。

---

### 2.2 gauge_physics.tex 对已修复定理的引用

#### 检查点 CP-4：对 Coulomb 规范 / 零模固定区分的引用

**gauge_physics.tex 第 330–334 行**:
```latex
The correct continuous analog is fixing the integration constant
∫Λ dx = 0 (eliminating the zero-mode of gauge transformations),
not imposing a divergence condition. For a rigorous discussion
of this distinction, see~\cite{scx_fiber_bundle}.
```
- ✅ **正确引用了修复后的 fiber_bundle.tex**，后者确实严格区分了零模固定和 Coulomb 规范

**gauge_physics.tex 第 513–514 行**:
```latex
See~\cite{scx_fiber_bundle} for details.
```
- ✅ 在 Yang-Mills 章节中正确引用离散 Hodge 理论作为正确框架

#### 检查点 CP-5：残留的 Coulomb 规范混淆

**gauge_physics.tex 第 219 行（表格）**:
```
Gauge-fixing condition | Σ g_m = 0 | Coulomb gauge ∂_i A^i = 0
```
**gauge_physics.tex 第 365–366 行（"What SCX Can Adopt"）**:
```latex
\item \textbf{Coulomb-type:} Σ g_m = 0 (already implemented)
```

**问题分析**: 
- gauge_physics.tex 在多处**同时**做了两件事：(a) 在第 330–334 行诚实地指出 $\sum g_m = 0$ **不是** Coulomb 规范，是零模固定；(b) 在第 219 行和第 366 行仍将其**归类**为 "Coulomb-type" 或与 Coulomb gauge 对照
- 这种双重表述虽然附带了诚实声明，但仍可能造成读者的混淆

**评级**: ⚠️ 轻微不一致。建议将 "Coulomb-type" 在第 366 行改为 "Zero-mode-fixing type (functionally analogous to Coulomb gauge)"，与 fiber_bundle.tex 的术语保持一致。

#### 检查点 CP-6：Cercis 定义的一致性

**gauge_physics.tex 第 338–343 行**:
```
The Cercis Score S(x) = Q(x) + η N(x) is designed as a
gauge-invariant observable
```
**fiber_bundle.tex 第 895–917 行**:
```
Cercis := R[g*] = Σ_e ‖A_e - (d_0 g*)_e‖²
```
**fiber_bundle.tex 第 983–997 行**（Remark `rem:code_paper_gap`）:
- 明确区分了理论 Cercis（残差范数）与代码 Cercis（$Q + \eta N$）

**问题**: gauge_physics.tex 使用的是代码版本的 Cercis 定义（$Q + \eta N$），而 fiber_bundle.tex 使用的是理论版本（残差范数）。两篇论文各自声明了不同的 Cercis 定义，但 gauge_physics.tex **未引用** fiber_bundle.tex 的 `rem:code_paper_gap` 来解释两者之间的关系。

**评级**: ⚠️ 轻微不一致。gauge_physics.tex §1.2.3 应增加对 fiber_bundle.tex 中理论 Cercis 定义的交叉引用。

---

### 2.3 dim(ker(Δ₁)) 跨论文一致性

| 来源文件 | dim(ker(Δ₁)) 或等价表述 | 使用的图结构 |
|----------|------------------------|-------------|
| fiber_bundle.tex (line 878) | $\dim\ker(\Delta_1) = \|\mathcal{L}\|$（圈数/cyclomatic number） | SCX 专家比较图 $\mathcal{G}_{SCX}$ |
| gauge_formalized.tex (line 199–201) | $\beta_1 = (M-1)(M-2)/2$ | SCX 2-复形（同伦等价于 $K_M$） |
| gauge_domain_formalization.md (§2.2) | $b_1$ = 第一 Betti 数；阿贝尔群下 $\dim = d \cdot b_1$；O(d) 下 $\dim = d(d-1)/2 \cdot \max(b_1-1, 0)$ | 一般图 G |
| gauge_domain_analysis.md (§3) | $b_1 = \dim H_1$ = 独立回路数 | SCX 图 |

**一致性分析**:
- fiber_bundle.tex 使用圈数 $\|\mathcal{L}\|$ 作为 $\dim\ker(\Delta_1)$，但未给出针对 SCX 图的具体公式
- gauge_formalized.tex 给出 $\beta_1 = (M-1)(M-2)/2$——这是针对**2-复形**（其 1-骨架同伦等价于 $K_M$）的 Betti 数
- 两者**不矛盾**：fiber_bundle.tex 的图结构（含 $NM$ 个顶点）与 gauge_formalized.tex 的 2-复形（缩并到 $M$ 个顶点）具有**不同的圈数**，分别计算了各自结构下的 $\dim\ker(\Delta_1)$
- gauge_domain_formalization.md 的 $d \cdot b_1$（阿贝尔）与 $d(d-1)/2 \cdot \max(b_1-1,0)$（非阿贝尔）提供了更一般的公式框架

**结论**: ✅ 跨论文的 $\dim\ker(\Delta_1)$ 表述在各自图结构设定下一致。但建议 fiber_bundle.tex 和 gauge_formalized.tex 在交叉引用时显式解释图结构差异导致的 Betti 数不同。

---

### 2.4 Supplementary 文件与 gauge_formalized.tex 的一致性

#### 检查点 CP-7：三个复活域的一致性

| 域 | gauge_domain_analysis.md | gauge_domain_formalization.md | gauge_formalized.tex |
|----|------------------------|------------------------------|---------------------|
| O(d) 格点规范 | MUST FORMALIZE ⭐ | Theorem 1.1–1.3 完整证明框架 | Section 2: 完整形式化 |
| Dijkgraaf-Witten TQFT | MUST FORMALIZE ⭐ | Theorem 2.1–2.3 完整证明框架 | Section 3: 完整形式化 |
| 信息几何体-边界 | —（域 5 在 analysis 中标记为外部） | Theorem 3.1–3.2 完整证明框架 | Section 4: 完整形式化 |

**补充一致性细节**:
- gauge_domain_analysis.md 将"格点规范"列为域 3、将"BRST 上同调"列为域 5（两者均为 MUST FORMALIZE）
- gauge_domain_formalization.md 形式化了"O(d) 格点规范"（域 1）、"DW TQFT"（域 4）、"信息几何"（域 5）
- gauge_formalized.tex 的三个 Section 与 gauge_domain_formalization.md 的三个域**完全对应**
- BRST 上同调虽然在 gauge_domain_analysis.md 中标记为 MUST FORMALIZE，但不是 gauge_formalized.tex 和 gauge_domain_formalization.md 的形式化对象——这是**有意为之**的优先级选择

**结论**: ✅ Supplementary 文件与 gauge_formalized.tex 在三个复活域上完全一致。

#### 检查点 CP-8：对 fiber_bundle.tex Theorem 3 错误的识别

**gauge_domain_analysis.md 第 128–136 行**:
> "fiber_bundle.tex 的定理 3（曲率处处为零 ⇔ 规范场正合 ⇔ Cercis=0）在有环路的图上**不成立**。"

**gauge_domain_formalization.md 第 431 行**:
> "fiber_bundle.tex 的 Theorem 3 声称 'curvature = 0 对所有 plaquette ⇔ A 是恰当的 ⇔ Cercis = 0'。Theorem 2.3 证明了这**不成立**。"

**gauge_formalized.tex**:
- Section 5 的 comparison table 未直接提及 Theorem 3 错误
- 但在 "Why This Paper's Mathematics is Correct" (第 1251 行) 中，通过指出 fiber_bundle.tex 的调和模空间仅为向量空间 $\ker(\Delta_1) \cong \mathbb{R}^{\beta_1}$ 而本论文扩展为平坦联络模空间，**隐含地**修正了此错误

**结论**: ✅ Supplementary 文件正确识别了错误。gauge_formalized.tex 通过扩展（而非直接否定）来处理此错误，这种方法在学术上是得体的。

---

### 2.5 附加检查：gauge_physics.tex 的诚实性声明

#### 检查点 CP-9：诚实性声明的自洽性

gauge_physics.tex 包含多处 `\honestcrit` 诚实标注和明确的 "Honesty Statement"（第 150–160 行）：

| 声明位置 | 内容 | 是否自洽 |
|---------|------|---------|
| Abstract (line 151–160) | "绝大多数对应是**结构性类比**，非严格数学同构" | ✅ |
| §1.2.2 (line 329–334) | Σg_m=0 是零模固定，非 Coulomb 规范 | ✅ |
| §3.2.1 (line 621–652) | SCX 规范固定是**显式对称破缺**，非自发破缺 | ✅ |
| §4.2.1 (line 782–790) | M_t 参数**不是**鬼场，BRST 构造是**形式的** | ✅ |
| §5.2.1 (line 952–973) | Σg_m=0 是**经典零模固定**，非量子反常抵消 | ✅ |

**但存在以下不一致**:
- §1.2.2 的诚实声明之后，§1.3 (line 366) 仍将 $\sum g_m = 0$ 称为 "Coulomb-type"
- §5.2.1 正确区分后，§5.3 (line 1026) 仍将 $\|\sum g_m\|$ 称为 "anomaly coefficient"

**评级**: ⚠️ 诚实声明本身自洽且准确，但后续分类标签与诚实声明之间存在术语张力。建议排查所有将 $\sum g_m = 0$ 称为 "Coulomb-type" 或 "anomaly" 的标签并统一替换。

---

## 三、发现的问题汇总 / Issues Found

### 问题 1: gauge_physics.tex 的 Coulomb/Coulomb-type 术语混淆
- **位置**: §1.2.2 (line 366), Table 1 (line 219)
- **描述**: 诚实声明称 $\sum g_m = 0$ 非 Coulomb 规范，但后续将其归类为 "Coulomb-type"
- **建议**: 统一为 "Zero-mode-fixing type" 或引注区分

### 问题 2: gauge_physics.tex 的 Cercis 定义未交叉引用
- **位置**: §1.2.3 (line 338–343)
- **描述**: 使用代码 Cercis（$Q+\eta N$）而非理论 Cercis（$\|P^\perp A\|^2$），未引用 fiber_bundle.tex 的 `rem:code_paper_gap`
- **建议**: 增加对理论 Cercis 定义的交叉引用

### 问题 3: Betti 数公式的图结构差异未显式解释
- **涉及文件**: fiber_bundle.tex, gauge_formalized.tex
- **描述**: fiber_bundle.tex 的圈数 $\|\mathcal{L}\|$ 与 gauge_formalized.tex 的 $\beta_1 = (M-1)(M-2)/2$ 针对不同图结构，但两者均未在交叉引用时解释此差异
- **建议**: 在 gauge_formalized.tex §5 的 comparison table 中增加注释，说明 $\beta_1$ 公式的图结构假设

### 问题 4: fiber_bundle.md 中的 `[ref]` 占位符
- **位置**: fiber_bundle.md 全文
- **描述**: Markdown 版本使用 `[ref]` 替代 LaTeX 的 `\ref{label}`，但某些引用无法追溯到具体定理（例如 "Theorem [ref]"）
- **建议**: 如果 .md 版本用于独立阅读，应替换为可追溯的引用编号

---

## 四、总体评估 / Overall Assessment

### 修复有效性：✅ 有效
fiber_bundle.tex 的核心修复（平坦性定理加入调和分量条件、Cercis ≠ Yang-Mills 的明确区分、零模固定 ≠ Coulomb 规范的严格论证）已正确同步到 fiber_bundle.md，并被 supplementary 文件和 gauge_formalized.tex 正确引用和扩展。

### 跨论文一致性：✅ 良好
- 数学定义（离散外导数、关联矩阵、回路矩阵、Hodge 分解）在所有文件中一致
- $\dim\ker(\Delta_1)$ 的值在各自图结构设定下自洽
- Supplementary 文件正确诊断了被修复文件中的错误

### 待改进项：⚠️ 轻微
- gauge_physics.tex 的术语标签（"Coulomb-type", "anomaly coefficient"）与自身的诚实声明存在张力
- 部分交叉引用可以更完整

---

## 五、建议行动 / Recommended Actions

| 优先级 | 行动 | 目标文件 |
|--------|------|---------|
| 高 | 将 "Coulomb-type" 改为 "Zero-mode-fixing type" | gauge_physics.tex §1.3 |
| 中 | 增加对 fiber_bundle.tex `rem:code_paper_gap` 的交叉引用 | gauge_physics.tex §1.2.3 |
| 中 | 在 gauge_formalized.tex comparison table 中注释 β₁ 公式的图结构差异 | gauge_formalized.tex §5 |
| 低 | 将 .md 版本的 `[ref]` 替换为可追溯编号 | fiber_bundle.md |

---

> **审计结论**: 修复后的 SCX 规范应用论文体系在核心数学内容上具有良好的一致性。主要问题集中在 gauge_physics.tex 的术语标签与其自身诚实声明之间的轻微张力——这不会导致数学错误，但可能造成读者的概念混淆。建议执行上述行动以进一步提升跨论文的术语一致性。
