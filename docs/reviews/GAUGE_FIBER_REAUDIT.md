# fiber_bundle.tex 重新审计报告

**审计日期**: 2026-07-03
**文件**: `F:\scx\papers\scx_fiber_bundle\fiber_bundle.tex`
**审计类型**: 5项修复后的重新审计
**行数**: 1681 行

---

## 一、五项修复验证

### 修复1: Lemma 循环基 (Lines 631-634) — ✅ 正确

**修复内容**: 补全了 LaTeX 参数，四边形循环和三角形循环路径完整。

| 行号 | 内容 | 状态 |
|------|------|------|
| 631 | `$(k,i) \to (k,j) \to (k+1,j) \to (k+1,i) \to (k,i)$` | ✅ 完整正确 |
| 632 | `for all configurations $k$ and expert pairs $i<j$;` | ✅ |
| 633 | `$(k,i) \to (k,j) \to (k,\ell) \to (k,i)$` | ✅ 完整正确 |
| 634 | `for all configurations $k$ and distinct experts $i,j,\ell$.` | ✅ |

### 修复2: Thm 5.3(v) — ✅ 正确

**Line 970**: `for all elementary quadrilateral and triangle loops $\gamma$ (equivalently, $d_1 A = 0$), {\it and}`

- 从仅"quadrilateral"扩展为"quadrilateral and triangle" — 匹配 Lemma 的循环基
- 增加了 `$d_1 A = 0$` 等价性声明 — 数学上正确，因为四边形+三角形循环构成完整循环空间
- `{\it and}` 连接后面的谐波分量为零条件 — 正确

### 修复3: Note (Lines 975-976) — ✅ 正确

**内容**: `$d_1 A = 0$ alone guarantees $A$ has no coexact component (since $\im(d_1^T) \perp \ker(d_1)$)`

- 数学验证: $d_1 A = 0$ 意味着 $A \in \ker(d_1)$。由 Hodge 分解，$\Omega^1 = \im(d_0) \oplus \ker(\Delta_1) \oplus \im(d_1^T)$。由于 $\im(d_1^T) \subseteq \ker(d_1)^\perp$（因为 $d_1 d_1^T \neq 0$ 一般情况），$A \in \ker(d_1)$ 确实保证 $A$ 没有 coexact 分量。✅
- 然后 Note 正确指出仅有 $\ker(d_1)$ 不足以保证 exactness，还需要谐波分量为零。

### 修复4: Yang-Mills 注记 (Line 933) — ✅ 正确

**修复前**: `$\|d_1 r_{\text{harm}}\|^2$`（错误：$d_1 r_{\text{harm}} = 0$）

**修复后**: `$\|d_1 r\|^2 = \|d_1 r_{\text{coexact}}\|^2$`

- 数学验证: 残差 $r = A - d_0 g^* \in \im(d_0)^\perp = \ker(\Delta_1) \oplus \im(d_1^T)$。$r = r_{\text{harm}} + r_{\text{coexact}}$。$d_1 r_{\text{harm}} = 0$（谐波形式在 $\ker(d_1)$ 中），所以 $d_1 r = d_1 r_{\text{coexact}}$。Yang-Mills 泛函 $\|d_1 r\|^2$ 只捕获 coexact 部分的导数范数。✅
- 完整解释正确区分了 Cercis（捕获 $\|r\|^2 = \|r_{\text{harm}}\|^2 + \|r_{\text{coexact}}\|^2$）与 Yang-Mills（捕获 $\|d_1 r\|^2 = \|d_1 d_1^T \beta\|^2$）。

### 修复5: Code-Paper Gap 注记 (Lines 990-994) — ✅ 正确

| 行号 | LaTeX 内容 | 状态 |
|------|-----------|------|
| 990 | `$\cercis(s) = Q(s) + \eta(t) \cdot N(s)$` | ✅ `\cercis` 宏正常展开为 $\mathcal{C}(s)$ |
| 991 | `$Q(s)$`, `$N(s)$` | ✅ |
| 994 | `$B^T B g = B^T A$` | ✅ |
| 994 | `$Q + \eta N$` | ✅ |
| 994 | `\S\ref{sec:algorithm}` | ⚠️ 见下文问题 |

---

## 二、新发现的问题

### 🔴 严重问题1: Proof Sketch 中数学模式内容损坏 (Lines 638-642)

通过十六进制分析确认，Lemma 的 proof sketch 中有多处 `$...$` 内部内容被剥离：

| 行号 | 当前内容（损坏） | 应为 |
|------|-----------------|------|
| 638 | `has  = \{(k,m) : ...M\}$` | `has $V = \{(k,m) : ...M\}$` |
| 639 | `parameter edges \to(k+1,m)$` | `parameter edges $(k,m)\to(k+1,m)$` |
| 639 | `expert edges \to(k,j)$` | `expert edges $(k,i)\to(k,j)$` |
| 640 | `within each configuration $, connect all $ vertices` | `within each configuration $k$, connect all $M$ vertices` |
| 641 | `-1$ star edges centered at $;` | `$M-1$ star edges centered at $(k,1)$;` |
| 641 | `via \to(k+1,1)$` | `via $(k,1)\to(k+1,1)$` |
| 642 | `This tree has -1$ edges` | `This tree has $KM-1$ edges` |

**影响**: 
- `\to` 命令在数学模式外，LaTeX 编译会报错
- 孤立的关闭 `$` 符号没有对应的打开 `$`，导致数学模式不匹配
- 缺失的符号 `V`, `k`, `M`, `(k,m)`, `(k,1)`, `KM` 使证明不可读

### 🔴 严重问题2: 损坏的交叉引用 (Line 994)

`\S\ref{sec:algorithm}` 引用了不存在的标签 `sec:algorithm`。

- Section 7 "Numerical Algorithm"（Line 1107）**没有** `\label{sec:algorithm}`
- 文件中只存在标签 `sec:comparison`（Line 1267），`alg:scx`（Line 1117）
- LaTeX 编译后会产生 `§??` 的未定义引用

### 🟡 警告: 数学表述不精确 (Line 926)

**当前文本**: "But Cercis is the total norm of the residual, not just its harmonic component (i.e., curvature)."

**问题**: 括号中的 "(i.e., curvature)" 将谐波分量等同于曲率，这在数学上不准确：
- 曲率 $\kappa = d_1 A = d_1 r = d_1(r_{\text{harm}} + r_{\text{coexact}}) = d_1 r_{\text{coexact}}$
- 谐波分量 $r_{\text{harm}} \in \ker(d_1)$，$d_1 r_{\text{harm}} = 0$，对曲率无贡献
- 曲率完全来自 coexact 部分，而非谐波部分

**建议修改**: 将 "(i.e., curvature)" 改为更准确的表述，例如：
- "...not just its coexact component that generates curvature"
- 或直接删除 "(i.e., curvature)" 并让后续段落（Lines 928-933）自行解释

### 🟢 观察: 语法问题 (Lines 933-934)

句子 "These are different: the harmonic norm...and the coexact norm..." 是一个语法片段（没有主谓结构），但数学内容正确。不影响编译，仅影响可读性。

---

## 三、CRLF 检查

- ✅ 文件使用 Unix 换行符（LF），无 CRLF 问题
- ✅ 文件编码为 UTF-8
- ✅ 最长行 324 字符，在 LaTeX 可接受范围内

---

## 四、交叉引用完整性检查

| 引用 | 标签 | 状态 |
|------|------|------|
| `\ref{thm:hodge_decomp}` | Line 363 | ✅ |
| `\ref{thm:d1d0}` | Line 291 | ✅ |
| `\ref{thm:cercis_zero}` | Line 962 | ✅ |
| `\ref{prop:solution}` | Line 819 | ✅ |
| `\ref{thm:flatness}` | Line 650 | ✅ |
| `\ref{sec:algorithm}` | **不存在** | ❌ |

未引用但已定义的标签（不影响编译）: `prop:trivial`, `alg:scx`, `sec:comparison`, `prop:curv_gauge_inv`, `lem:cycle_basis`, `thm:pes_misalignment`, `prop:normal_eq`, `thm:zero_mode`, `prop:projection`, `def:cercis`, `thm:cercis_inv`, `rem:code_paper_gap`

---

## 五、Thm 5.3 自洽性验证

Theorem 5.3 (Characterization of $\mathcal{C} = 0$, Lines 961-978) 现在自洽：

- (i)-(iv): 标准等价条件 ✅
- (v): 零曲率（四边形+三角形循环）+ 谐波分量为零 ✅
- Note: 正确解释 $d_1 A = 0$ 消除 coexact 但不消除谐波 ✅
- Remark 引用 `\ref{thm:flatness}` 正确 ✅

---

## 六、Yang-Mills 注记数学正确性

Lines 919-935 的数学验证：

1. $r = A - d_0 g^*$，由正规方程 $B^T r = 0$，有 $r \perp \im(d_0)$ ✅
2. Hodge 分解: $r = r_{\text{harm}} + r_{\text{coexact}}$ ✅
3. $\|r\|^2 = \|r_{\text{harm}}\|^2 + \|r_{\text{coexact}}\|^2$（正交分解）✅
4. $d_1 r = d_1 r_{\text{coexact}}$（因为 $d_1 r_{\text{harm}} = 0$）✅
5. Cercis 捕获 $\|r\|^2$，Yang-Mills 捕获 $\|d_1 r\|^2 = \|d_1 r_{\text{coexact}}\|^2$ ✅
6. $\|r_{\text{coexact}}\|^2 = \|d_1^T \beta\|^2$ vs $\|d_1 d_1^T \beta\|^2$ — 不同范数 ✅

**结论**: 除 Line 926 的 "(i.e., curvature)" 表述不精确外，数学全部正确。

---

## 七、总结

| 类别 | 数量 | 详情 |
|------|------|------|
| ✅ 已验证修复 | 5/5 | 五项修复全部正确 |
| 🔴 严重问题 | 2 | Lines 638-642 数学模式损坏; Line 994 断裂交叉引用 |
| 🟡 警告 | 1 | Line 926 将谐波分量误等于曲率 |
| 🟢 观察 | 1 | Lines 933-934 语法片段 |

**优先级建议**:
1. **立即修复**: Lines 638-642 的数学模式损坏和 Line 1107 缺少标签，否则 LaTeX 无法正常编译
2. **建议修复**: Line 926 的 "(i.e., curvature)" 表述
3. **可选**: Lines 933-934 的语法改进
