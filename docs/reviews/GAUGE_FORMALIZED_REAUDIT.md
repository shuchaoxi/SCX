# gauge_formalized.tex 修复后再审计报告

**审计时间**: 2026-07-03  
**文件**: `F:\scx\papers\scx_gauge_formalized\gauge_formalized.tex`  
**状态**: 6 项修复已应用，进行再审计  

---

## 一、编译状态

`pdflatex` 编译通过，生成 33 页 PDF。无致命错误（无 `!` 级别错误）。

**LaTeX 警告**:
- `Reference 'thm:hodge_iso' on page 14 undefined on input line 762` — 未定义的交叉引用（详见下文 §3.1）
- `destination with the same identifier (name{Hfootnote.1})` — 重复脚注标识符（第 1234-1249 行，脚注计数器手动操作的已知问题，不影响输出）

**结论**: 文件可编译，但有一个未定义的 `\ref` 标签会导致输出中出现 "??"。

---

## 二、六项修复逐项验证

### Fix 1: 删除重复的 `\newcommand{\face}`（原第 149 行）

| 项目 | 详情 |
|------|------|
| **状态** | ✅ 已正确修复 |
| **验证** | 第 90 行保留唯一定义 `\newcommand{\face}{\ensuremath{\mathit{f}}}`；原第 149 行已变为 `\DeclareMathOperator{\grad}{grad}` |
| **影响** | 全文 48 处 `\face` 使用均正常工作 |

### Fix 2: 添加 `\DeclareMathOperator{\Conj}{Conj}`（第 148 行）

| 项目 | 详情 |
|------|------|
| **状态** | ✅ 已正确添加 |
| **验证** | 第 148 行: `\DeclareMathOperator{\Conj}{Conj}` |
| **注记** | 第 808 行实际使用 `\operatorname{Conj}(\Od)` 而非 `\Conj(\Od)`，`\Conj` 声明存在但未被调用。两者在 LaTeX 中等价，仅风格不一致 |

### Fix 3: 收敛率声明修正（第 550 行）

| 项目 | 详情 |
|------|------|
| **状态** | ✅ 已正确修复 |
| **原文** | `converges quadratically` |
| **修改后** | `converges linearly to the global minimum of $\mathcal{E}_{\Od}$ (with quadratic convergence only in the zero-residual limit)` |
| **与证明一致性** | 证明草图（第 556-559 行）: "linear convergence (quadratic only in the zero-residual limit) follows from standard optimization theory" — 命题声明与证明完全一致 ✅ |
| **注记** | 命题声称收敛到 "global minimum"，证明仅涉及局部收敛性（Gauss-Newton 是局部方法）。在 small-connection 区域能量函数是强凸的，局部极小即全局极小，故数学上成立，但证明草图未显式论证此点 |

### Fix 4: DW 公式补充非交换群说明（第 696 行）

| 项目 | 详情 |
|------|------|
| **状态** | ⚠️ 语义正确，但引入语法断裂 |
| **修改后（第 692-697 行）** | |
| 公式行 | `$Z_{\DW}(\mathcal{K}, G) = \|\Gflatquot(\mathcal{K}, G)\| = \frac{\|\Hom(\pi_1(\mathcal{K}), G)\|}{\|G\|},$` |
| 新增行 696 | `which holds for non-abelian $G$ (the general case). For abelian $G$, see Corollary~\ref{cor:dw_abelian}.` |
| 原有行 697 | `where $\Gflatquot(\mathcal{K}, G) = \Gflat(\mathcal{K}, G) / \mathcal{G}$ is the space of gauge equivalence classes of flat connections.` |
| **问题** | 第 697 行的 "where" 从句被第 696 行的新句子断开，形成悬空从句。原始结构是"公式, where ..."的连续语句，现在变成"公式, which ... . For abelian ..., see Corollary. where ..."——"where" 前是一个句号，且首字母为小写，语法不通 |
| **建议修复** | 将第 697 行的 "where" 改为 "Here" 或以其他方式重新连接；或者将定义移到公式之前 |
| **交叉引用** | `\ref{cor:dw_abelian}` → 第 718 行 `\label{cor:dw_abelian}` 存在 ✅ |

### Fix 5: Stabilizer 假设修改（第 711 行）

| 项目 | 详情 |
|------|------|
| **状态** | ✅ 已正确修复 |
| **原文** | `for all flat A` |
| **修改后** | `for generic flat $A$ (which holds for most $A$; the trivial connection is a measure-zero exception)` |
| **验证** | "generic flat A" 表述精确，与后文第 712 行 "For a generic flat $G$-connection on the SCX 2-complex (connected graph), $\Stab(A) \cong Z(G)$" 一致 |
| **注记** | 第 711-712 行存在轻微冗余——两句话本质上表述同一事实。非错误，仅风格问题 |

### Fix 6: O(d)/O(d)≅{pt} 修正为 Conj(O(d))（第 808 行）

| 项目 | 详情 |
|------|------|
| **状态** | ✅ 已正确修复 |
| **原文** | `O(d)/O(d) \cong \{pt\}` |
| **修改后** | `$\Gflatquot \cong \operatorname{Conj}(\Od)$ (the space of conjugacy classes of $\Od$), which is not a single point` |
| **数学正确性** | 对于 M=3, β₁=1 的情况，$\Hom(\pi_1, \Od)/\Od$ 同构于 $\Od$ 的共轭类空间，确实不是单点。原始断言 O(d)/O(d) 商掉共轭作用后为单点是错误的 ✅ |

---

## 三、修复引入的新问题

### 3.1 关键问题：未定义的 `\ref{thm:hodge_iso}`（第 762 行）

**严重程度**: ⚠️ 中（编译警告，输出中出现 "??"）

```latex
By Theorem~\ref{thm:hodge_iso}, $\ker(\Lone) \cong H^1(\mathcal{K})$.
```

- `\label{thm:hodge_iso}` 在本文中**不存在**。该定理（Hodge 同构定理：$\ker(\Delta_1) \cong H^1$）可能在 `fiber_bundle.tex` 中定义，但本文未定义。
- 编译日志确认: `LaTeX Warning: Reference 'thm:hodge_iso' on page 14 undefined`

**建议**: 
- 方案 A: 在本文中添加一个 Lemma/Theorem 声明 $\ker(\Lone) \cong H^1(\mathcal{K}; \R)$ 并赋予标签 `thm:hodge_iso`
- 方案 B: 将引用改为描述性语句，如 "by the standard Hodge isomorphism $\ker(\Lone) \cong H^1(\mathcal{K})$"

**是否为修复引入**: 否，此为第一轮审计遗漏的预存问题。

### 3.2 语法断裂：第 696-697 行 "where" 从句悬空

**严重程度**: ⚠️ 低（不影响编译，仅影响可读性）

修复 4 在第 696 行插入句子后，原有的 "where" 从句（定义 `\Gflatquot` 符号）被断开。见 §Fix 4 的详细分析。

**建议修复**:
```latex
% 当前（有问题）:
   = \frac{|\Hom(\pi_1(\mathcal{K}), G)|}{|G|},
```
which holds for non-abelian $G$ (the general case). For abelian $G$, see Corollary~\ref{cor:dw_abelian}.
where $\Gflatquot(\mathcal{K}, G) = \Gflat(\mathcal{K}, G) / \mathcal{G}$ is ...

% 建议修改为:
   = \frac{|\Hom(\pi_1(\mathcal{K}), G)|}{|G|},
```
where $\Gflatquot(\mathcal{K}, G) = \Gflat(\mathcal{K}, G) / \mathcal{G}$ is the space of gauge equivalence classes of flat connections.
This formula holds for non-abelian $G$ (the general case). For abelian $G$, see Corollary~\ref{cor:dw_abelian}.
```

### 3.3 `\Conj` 声明未使用

**严重程度**: 极低（不影响功能）

第 148 行声明了 `\DeclareMathOperator{\Conj}{Conj}`，但第 808 行使用的是 `\operatorname{Conj}(\Od)`。两者输出相同，但建议统一为 `\Conj(\Od)` 以利用已声明的运算符。

---

## 四、其他发现（第一轮审计遗漏）

### 4.1 脚注重复标识符（第 1234-1249 行）

**编译警告**: `destination with the same identifier (name{Hfootnote.1}) has been already used`

```latex
% 第 1234 行
\footnotemark \\
% 第 1236 行
\footnotemark[\value{footnote}] \\
% 第 1246-1249 行
\addtocounter{footnote}{-2}
\footnotetext{...}
\addtocounter{footnote}{1}
\footnotetext{...}
```

手动操作 `footnote` 计数器导致两个 footnote mark 使用相同标识符。虽然 `hyperref` 发出警告，但 PDF 输出正常。这是已知的 LaTeX 技巧性问题，如果需彻底消除警告，可使用 `\footnotemark` 的不同值或改用 `\footnote`。

### 4.2 第 711-712 行冗余

第 711 行: `provided $\Stab(A) = Z(G)$ for generic flat $A$ (which holds for most $A$; the trivial connection is a measure-zero exception).`
第 712 行: `For a generic flat $G$-connection on the SCX 2-complex (connected graph), $\Stab(A) \cong Z(G)$.`

两句话表达同一事实，建议合并或删除一处。

### 4.3 命题 prop:od_convergence 的 "global minimum" 断言

命题（第 546-550 行）声称算法收敛到 "global minimum"，但证明草图（第 555-559 行）仅展示局部收敛性论证（Gauss-Newton = Newton 在零残差极限下 → 线性收敛）。虽然在 small-connection 强凸区域局部极小即全局极小，但证明未显式指出这一关联。对数学严谨性要求高的读者可能需要补充一句话。

### 4.4 交叉引用一致性

已验证所有 46 处 `\ref{}` 和 10 处 `\cite{}`:
- **1 处未定义**: `thm:hodge_iso`（见 §3.1）
- **其余全部匹配**: 所有 `\label`, `\ref`, `\cite` — `\bibitem` 对应关系正确 ✅
- `\begin{...}` 85 处 = `\end{...}` 85 处 ✅

---

## 五、总体评估

| 维度 | 评级 | 说明 |
|------|------|------|
| 6 项修复的正确性 | ✅ 全部正确 | 每项修复均达到预期目标 |
| 修复完整性 | ✅ 完整 | 无遗漏 |
| 引入新 LaTeX 错误 | ✅ 无 | 编译通过，无 `!` 级错误 |
| 引入新问题 | ⚠️ 1 项 | Fix 4 引入 where 从句语法断裂（低严重度） |
| 预存问题 | ⚠️ 1 项中等 | `thm:hodge_iso` 未定义（造成输出中 "??"） |
| 交叉引用一致性 | 46/47 通过 | 仅 `thm:hodge_iso` 缺失 |

### 建议优先修复项

1. **【必须】** 修复 `\ref{thm:hodge_iso}` 未定义（第 762 行）—— 这是唯一会在 PDF 中显示 "??" 的问题
2. **【建议】** 修复第 696-697 行 "where" 从句语法断裂
3. **【可选】** 第 808 行统一使用 `\Conj` 替代 `\operatorname{Conj}`
4. **【可选】** 合并第 711-712 行冗余内容
