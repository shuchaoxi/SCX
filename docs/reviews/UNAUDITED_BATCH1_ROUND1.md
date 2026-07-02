# Batch 1 首轮审计报告

**日期**: 2026-07-02
**审计范围**: ml_verdict + world_model + social_media（首轮）
**审计员**: SCX 自动化审计系统

---

## 1. 格式检查总览

| 检查项 | ml_verdict | world_model | social_media |
|--------|-----------|-------------|--------------|
| 1. CJK 字符 = 0 | ✅ 通过 | ✅ 通过 | ✅ 通过（修复后） |
| 2. `\author{SCX}` | ✅ 通过 | ✅ 通过 | ✅ 通过（含 `\\[4pt]`） |
| 3. `\textsf{SCX}`（非 `\mathsf`） | ❌ 使用 `\textsc{SCX}` | ❌ 无 SCX 宏 | ❌ 使用 `\textsc{SCX}` |
| 4. 首行 `\pdfoutput=1` | ✅ 已修复 | ✅ 已修复 | ✅ 已修复 |
| 5. `article` 文档类（非 ctexart） | ✅ 通过 | ✅ 通过（twocolumn） | ✅ 通过 |
| 6. 无 `physics` / `[utf8]{inputenc}` | ✅ 通过 | ✅ 通过 | ✅ 通过 |
| 7. pdflatex 编译 | 64 页，170 错误 | 18 页，1 错误 | 22 页，105 错误 |
| 8. 英文 Abstract | ✅ 通过 | ✅ 通过 | ✅ 通过（修复后） |

---

## 2. 逐文件详细审计

### 2.1 scx_ml_verdict/main.tex（2051 行 → 2046 行）

**修复内容**：
- 删除 line 1 无前缀的 `pdfoutput=1`（保留 `\pdfoutput=1`）
- 删除 line 3 `% !TEX program = xelatex`（应使用 pdflatex）
- 删除 line 143 乱码行 `70M29MLSCXGAN/RL/M=1914SCXCercisSCX——70`（编码损坏的中文摘要残留）

**编译结果**：64 页，成功生成 PDF（659,611 bytes）

**编译错误**（170 个）：
- **Unicode 字符错误**（大量）：`✓`(U+2713)、`◇`(U+25C7)、`✗`(U+2717)、`◆`(U+25C6)、`≠`(U+2260)
  - 需要替换为 LaTeX 命令：`\checkmark`、`\diamond`、`\neq` 等
  - 或使用 `\usepackage[utf8]{inputenc}`（但规范禁止，故需替换字符）
- **未定义命令**：
  - `\Corr` — 多处使用，未定义
  - `\argmin` — line 674, 682，未定义
  - `\cL` — 多处使用，未定义
  - `\cB` — line 985，未定义
  - `\partial \cL` — 作为 `\argmin` 的参数时出错
- **括号不匹配**：`Missing { inserted` / `Missing } inserted`

**品牌格式问题**：
- `\SCX` 宏定义为 `\textsc{SCX}`（小型大写），规范要求 `\textsf{SCX}`（无衬线体）

---

### 2.2 scx_world_model/main.tex（1911 行 → 1908 行）

**修复内容**：
- 删除 line 1 无前缀的 `pdfoutput=1`
- 删除 line 10 注释 `% Compile with XeLaTeX for Chinese (CJK) support`

**编译结果**：18 页，成功生成 PDF（446,689 bytes）

**编译错误**（1 个）：
- `\rigorFull` — 未定义命令（单次出现）

**编译警告**：96 个（主要为 overfull/underfull hbox，twocolumn 布局常见）

**品牌格式问题**：
- 全文未定义 `\SCX` 宏，SCX 以普通文本出现，无 `\textsf{SCX}` 格式

---

### 2.3 scx_social_media/social_gauge.tex（1810 行 → 1789 行）

**修复内容**：
- 删除 line 1 无前缀的 `pdfoutput=1`
- 删除 line 14 `% ---- Chinese & Font Support ----` 注释
- 删除 lines 136–151 损坏的中文摘要残骸（原中文文本被移除但 LaTeX 标记残留：`\textbf{.}`、`——\textbf{}Filter Bubble`、`~8 ——\textbf{}Polarization` 等碎段）
- 修复 line 171：`is bilingual (Chinese/English)` → `provides`

**编译结果**：22 页，成功生成 PDF（372,865 bytes）

**编译错误**（105 个）：
- **`\Gauge` 重复定义**：命令名与其他宏冲突
- **`\proj` 未定义**：line 348+ 多处使用
- **`\pqty` 未定义**：用于物理括号宏
- **`Double subscript`**（10 次）：`\GCoupling_` 展开后导致双下标
- **`Too many }'s`**：line 121 多余的右花括号
- **`Missing \begin{document}`**：`\begin{document}` 之前有可执行内容
- **`There's no line here to end`**：3 处误用 `\\`

**品牌格式问题**：
- `\SCX` 宏定义为 `\textsc{SCX}`，规范要求 `\textsf{SCX}`

---

## 3. 共性问题

### 3.1 `\textsf{SCX}` 品牌格式（3 个文件均不通过）
- **ml_verdict** 和 **social_media**：`\SCX` 定义为 `\textsc{SCX}`（小型大写），应改为 `\textsf{SCX}`
- **world_model**：未定义 `\SCX` 宏，SCX 以普通正文字体出现，需创建 `\textsf{SCX}` 宏并替换全文

### 3.2 Unicode 字符（ml_verdict 严重）
- 大量 Unicode 符号（✓◇✗◆≠）导致 pdflatex 报错
- 建议全局替换为 LaTeX 数学符号命令

### 3.3 未定义宏（social_media 严重）
- `\proj`、`\pqty`、`\Gauge`、`\GCoupling_`（双下标问题）
- 需补充宏定义或修正用法

---

## 4. 修复操作记录

| 文件 | 操作 | 行号 |
|------|------|------|
| ml_verdict/main.tex | 修复 `\pdfoutput=1` | line 1 |
| ml_verdict/main.tex | 删除 xelatex 指令 | line 3 |
| ml_verdict/main.tex | 删除乱码摘要行 | line 143 |
| world_model/main.tex | 修复 `\pdfoutput=1` | line 1 |
| world_model/main.tex | 删除 XeLaTeX 注释 | line 10 |
| social_media/social_gauge.tex | 修复 `\pdfoutput=1` | line 1 |
| social_media/social_gauge.tex | 删除 Chinese 注释 | line 14 |
| social_media/social_gauge.tex | 删除损坏中文摘要 | lines 136–151 |
| social_media/social_gauge.tex | 修复 bilingual 声明 | line 171 |

---

## 5. 待修复问题（第二轮）

1. **[高优先级] `\textsf{SCX}` 格式**：3 个文件均需修正
2. **[高优先级] ml_verdict Unicode 字符**：✓◇✗◆≠ 替换为 LaTeX 命令
3. **[中优先级] ml_verdict 未定义宏**：`\Corr`、`\argmin`、`\cL`、`\cB`
4. **[高优先级] social_media 未定义宏**：`\proj`、`\pqty`、`\Gauge` 冲突、`\GCoupling_` 双下标
5. **[中优先级] world_model `\rigorFull`**：1 个未定义命令
