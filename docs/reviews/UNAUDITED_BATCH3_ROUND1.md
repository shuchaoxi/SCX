# 未审计 Batch 3 首轮审查报告

**日期**: 2026-07-02  
**范围**: spring_framework + matrix_theory + climate  
**轮次**: Round 1 (首轮)

---

## 检查清单总览

| 检查项 | spring_framework | matrix_theory | climate |
|--------|:---:|:---:|:---:|
| 1. 无中文字符 | ❌ | ❌ | ⚠️ |
| 2. `\author{SCX}` | ✅ | ✅ | ✅ |
| 3. `\textsf{SCX}` | ❌ | ❌ | ❌ |
| 4. `\pdfoutput=1` 首行 | ❌ | ❌ | ❌ |
| 5. article 文档类 | ✅ | ❌ | ✅ |
| 6. 无 physics/inputenc | ✅ | ✅ | ✅ |
| 7. pdflatex 编译 | 28页，72错误 | 超时(ctexart)，1错误 | 16页，3错误 |
| 8. Abstract 英文 | ❌ | ❌ | ✅ |

---

## 1. spring_framework (spring_framework.tex, 1608行)

### 逐项检查

1. **中文**: 文件中无中文字符（hex验证），但 Abstract 内容残缺/乱码——不是正常英文，内容不完整。
2. **`\author{SCX}`**: ✅ 第132行
3. **`\textsf{SCX}`**: ❌ 使用 `\textsc{SCX}`（第86行），应为 `\textsf{SCX}`
4. **`\pdfoutput=1` 首行**: ❌ 第1行 `pdfoutput=1` 缺少反斜杠，应为 `\pdfoutput=1`；第2行有正确的 `\pdfoutput=1`
5. **article 类**: ✅ `\documentclass[12pt,a4paper]{article}`
6. **无 physics/inputenc**: ✅
7. **pdflatex**: 28页，**72个错误**、56个警告
   - 首行 `pdfoutput=1`（无反斜杠）导致 `Missing \begin{document}` 等错误
   - 大量 `Missing $ inserted`、`Extra }` 等数学模式错误
   - PGF Math 错误：`Unknown function 'of'`
   - Unicode 字符 ω (U+03C9) 未在 math 模式中使用
8. **Abstract**: ❌ 内容残缺，不是正常英文，看起来像是中文内容被损坏/剥离后的残留

### 其他问题
- `\date{202671}` 格式异常（第133行）
- `\textsc{SCX}` 等5个宏定义全部使用 `\textsc` 而非 `\textsf`

---

## 2. matrix_theory (main.tex, 1566行)

### 逐项检查

1. **中文**: ❌ **大量中文**——Abstract 双语（第130-154行）、标题含中文（第5、120行）、Keywords、全部章节标题均为中英双语
2. **`\author{SCX}`**: ✅ 第121行
3. **`\textsf{SCX}`**: ❌ 使用 `\textsc{SCX}`（第51行），应为 `\textsf{SCX}`
4. **`\pdfoutput=1` 首行**: ❌ 首行为 `% !TEX program = xelatex`，完全没有 `\pdfoutput=1`
5. **article 类**: ❌ 使用 `\documentclass[12pt,a4paper]{ctexart}`，应为 `article`
6. **无 physics/inputenc**: ✅（ctexart 自动加载 UTF8 支持，但无显式 `\usepackage[utf8]{inputenc}`）
7. **pdflatex**: ❌ 编译超时（120秒），因为 ctexart + CJK 字体在 pdflatex 下极慢
   - 1个错误：`Command \I already defined`（第79行 `\newcommand{\I}{\mathbb{I}}` 与 ctexart 内部定义冲突）
   - 11个警告
   - 部分生成 PDF（仅第1页完整）
8. **Abstract**: ❌ 双语（英文 + 中文），不是纯英文

### 其他问题
- 整个文件为中英双语结构，所有章节标题均为双语
- `\textsc{SCX}` 等5个宏定义全部使用 `\textsc` 而非 `\textsf`

---

## 3. climate (main.tex, 979行)

### 逐项检查

1. **中文**: ⚠️ 仅在注释中出现（第5-8行注释含中文），标题行第76行含中文破折号 `——`。正文无中文。
2. **`\author{SCX}`**: ✅ 第77行
3. **`\textsf{SCX}`**: ❌ 所有组件宏使用 `\textsc`（第67-70行），且**未定义 `\SCX` 宏**（只在正文中用裸 `SCX`）
4. **`\pdfoutput=1` 首行**: ❌ 第1行 `pdfoutput=1` 缺少反斜杠，应为 `\pdfoutput=1`；第2行有正确的 `\pdfoutput=1`
5. **article 类**: ✅ `\documentclass[11pt,a4paper]{article}`
6. **无 physics/inputenc**: ✅
7. **pdflatex**: 16页，**3个错误**、13个警告
   - `\begin{abstract} on input line 84 ended by \end{proof}`——**缺少 `\end{abstract}`**
   - 首行 `pdfoutput=1` 导致 `Missing \begin{document}`
8. **Abstract**: ✅ 纯英文

### 严重问题
- **缺少 `\end{abstract}`**：Abstract 环境从未关闭，内容直接流入正文（第84行 `\begin{abstract}` 后，直到第171行 `\end{proof}` 才被系统自动闭合）
- **缺少 `\newcommand{\SCX}`**：正文中使用 `SCX` 但未定义为 LaTeX 宏
- `\textsc{SCX}` 等4个组件宏定义全部使用 `\textsc` 而非 `\textsf`

---

## 总结

三个文件**无一通过全部8项检查**。共性问题：

1. **全部使用 `\textsc` 而非 `\textsf`**（3/3）
2. **首行 `\pdfoutput=1` 问题**（2/3 缺少反斜杠，1/3 完全缺失）
3. **Abstract 问题**：spring_framework 残缺乱码，matrix_theory 含中文，climate 缺少 `\end{abstract}`

优先级排序：
- 🔴 **climate**: 缺少 `\end{abstract}`（结构性错误，阻塞编译）
- 🟠 **matrix_theory**: ctexart + 中文 + 无 `\pdfoutput=1`（需大改）
- 🟡 **spring_framework**: Abstract 残缺、`\textsc` → `\textsf`、`pdfoutput=1` 修复
