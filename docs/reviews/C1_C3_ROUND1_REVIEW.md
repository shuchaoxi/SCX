# C1–C3 首轮审查报告 (Round 1 Audit)

**审查日期**: 2026-07-02  
**审查范围**: SCX 猜想系列 C1, C2, C3  
**审查类型**: 格式合规 + 编译验证 + 内容抽查  

---

## 总体摘要

| 项目 | C1 | C2 | C3 |
|------|:--:|:--:|:--:|
| 中文字符 | 0 ✅ | 0 ✅ | 0 ✅ |
| `\author{SCX}` | ❌ | ❌ | ❌ |
| `\textsf{SCX}` 宏 | ❌ | ✅ | ✅ |
| `\pdfoutput=1` 首行 | ❌ | ❌ | ❌ |
| article 文档类 | ✅ | ✅ | ✅ |
| 无 physics 包 | ✅ | ✅ | ✅ |
| 无 inputenc 包 | ❌ | ❌ | ❌ |
| 编译通过 | ✅ (82W) | ✅ (18W) | ⚠️ (9E+23W) |
| 英文摘要 | ✅ | ✅ | ✅ |
| 空章节 | 无 | 无 | 无 |
| 定理/定义总数 | 37 | 7 | 14 |

---

## 详细报告

### C1: P≠NP 去相对化 (`papers/scx_pnp/main.tex`)

| Check | Result |
|-------|--------|
| Chinese | 0 (通过) |
| `\author{SCX}` | ❌ 实际为 `\textsc{SCX Consortium}` |
| `\textsf` macro | ❌ 未定义 `\newcommand{\SCX}{\textsf{SCX}}` |
| `\pdfoutput=1` | ❌ 首行为注释 `% ====` |
| article class | ✅ `\documentclass[11pt,a4paper]{article}` |
| No physics/inputenc | ❌ 含 `\usepackage[utf8]{inputenc}` (L10) |
| Compile | ✅ 24 页, 82 warnings, 0 errors |
| Abstract EN | ✅ 英文摘要, 含 Keywords 和 MSC 分类 |
| Issues found | 见下方 |

**数学结构**: 16 theorems + 5 lemmas + 13 definitions + 3 conjectures = 37 个数学环境。10 个主要章节 + 4 个附录。

**发现的问题**:
1. `\author` 字段不符合规范（应为 `\author{SCX}`，实际是 `\textsc{SCX Consortium}`）
2. 缺少 `\textsf{SCX}` 宏定义（C2/C3 均有，C1 缺失）
3. 首行不是 `\pdfoutput=1`（而是注释块）
4. 使用了 `\usepackage[utf8]{inputenc}` — 现代 LaTeX 中已内置 UTF-8 支持，应移除
5. 82 个编译警告（主要是 hyperref PDF 字符串中 token 问题，属于良性）

---

### C2: κ 压制悖论 (`papers/scx_kappa_suppression/main.tex`)

| Check | Result |
|-------|--------|
| Chinese | 0 (通过) |
| `\author{SCX}` | ❌ 实际为 `\SCX\ Theory Group` |
| `\textsf` macro | ✅ `\newcommand{\SCX}{\textsf{SCX}}` (L50) |
| `\pdfoutput=1` | ❌ 首行为注释 |
| article class | ✅ `\documentclass[12pt,a4paper]{article}` |
| No physics/inputenc | ❌ 含 `\usepackage[utf8]{inputenc}` (L9) |
| Compile | ✅ 14 页, 18 warnings, 0 errors |
| Abstract EN | ✅ 英文摘要 |
| Issues found | 见下方 |

**数学结构**: 4 theorems + 1 corollary + 2 definitions = 7 个数学环境。10 个章节。

**发现的问题**:
1. `\author` 不符合规范（`\SCX\ Theory Group` 而非 `SCX`）
2. 首行缺少 `\pdfoutput=1`
3. 使用了 `\usepackage[utf8]{inputenc}` — 应移除
4. 18 个 hyperref 警告（与 C1 类似，PDF 书签中 Unicode token 问题）

---

### C3: 非指数族 Cercis 界 (`papers/scx_cercis_bound/main.tex`)

| Check | Result |
|-------|--------|
| Chinese | 0 (通过) |
| `\author{SCX}` | ❌ 实际为 `SCX Theory Architect` |
| `\textsf` macro | ✅ `\newcommand{\SCX}{\textsf{SCX}}` (L48) |
| `\pdfoutput=1` | ❌ 首行为注释 |
| article class | ✅ `\documentclass[12pt,a4paper]{article}` |
| No physics/inputenc | ❌ 含 `\usepackage[utf8]{inputenc}` (L8) |
| Compile | ⚠️ 18 页, 23 warnings, **9 errors** |
| Abstract EN | ✅ 英文摘要 |
| Issues found | 见下方 |

**数学结构**: 5 theorems + 2 lemmas + 1 proposition + 6 definitions = 14 个数学环境。11 个章节（含附录）。

**发现的问题**:
1. `\author` 不符合规范（`SCX Theory Architect` 而非 `SCX`）
2. 首行缺少 `\pdfoutput=1`
3. 使用了 `\usepackage[utf8]{inputenc}` — 应移除
4. **关键**: 9 个编译错误 — 直接在 LaTeX 文本中使用 Unicode 希腊字母 `α` 和 `θ`（应用 `\alpha`, `\theta` 替代）。位置在 L737, L752–755, L763–766（数值验证结果表格）
5. 未定义引用警告（`eq:cercis_kl_exp`, `eq:taylor_loglik` 等），可能是交叉引用标签问题

---

## 通用问题（三篇共有）

1. **`\author` 规范**: 三篇均不符合。规范要求 `\author{SCX}`，但实际分别为 `\textsc{SCX Consortium}`, `\SCX\ Theory Group`, `SCX Theory Architect`。

2. **`\pdfoutput=1`**: 三篇首行均为注释块而非 `\pdfoutput=1`。需在 `\documentclass` 之前添加。

3. **`\usepackage[utf8]{inputenc}`**: 三篇均有。2018 年后的 LaTeX 内核默认使用 UTF-8，此包不需要且可能产生警告，建议移除。

4. **C1 缺少 `\textsf{SCX}` 宏**: C2/C3 通过 `\newcommand{\SCX}{\textsf{SCX}}` 定义了该宏，C1 需补充。

---

## 建议修复优先级

| 优先级 | 问题 | 影响文件 |
|--------|------|----------|
| P0 | 修复 C3 Unicode 希腊字母编译错误 | C3 |
| P1 | 统一 `\author{SCX}` | C1, C2, C3 |
| P1 | 添加 `\pdfoutput=1` 首行 | C1, C2, C3 |
| P1 | C1 添加 `\textsf{SCX}` 宏定义 | C1 |
| P2 | 移除 `\usepackage[utf8]{inputenc}` | C1, C2, C3 |

---

*审查由 Hermes Agent 自动执行*
