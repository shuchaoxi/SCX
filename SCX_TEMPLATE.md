# SCX Paper Template · LaTeX & Markdown

## 📐 LaTeX Template (Academic Publishing)

Reference: `papers/scx_moe_gauge/main.tex` (10-round converged)

```latex
\documentclass[UTF8]{ctexart}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx,booktabs,hyperref}
\usepackage{tikz}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{proposition}[theorem]{Proposition}

% SCX-specific environments
\newcommand{\SCX}{\textsf{SCX}}
\newcommand{\Yajie}{\textsf{Yajie}}
\newcommand{\Spring}{\textsf{Spring}}
\newcommand{\Cercis}{\textsf{Cercis}}
\newcommand{\Situs}{\textsf{Situs}}
\newcommand{\Mt}{M_t}
\newcommand{\ClaimSpace}{\mathfrak{C}}

% Honest critique boxes
\newenvironment{honestcrit}
  {\par\noindent\textbf{[Honest Critique / 诚实暴击]}\itshape}
  {\par}

\title{Paper Title · 论文标题}
\author{SCX}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
    Abstract in English and Chinese.
\end{abstract}

\section{Introduction}
\section{Main Results}
\section{Proofs}
\section{Discussion}
\section{Conclusion}

\bibliographystyle{plain}
\bibliography{references}
\end{document}
```

## 📝 Markdown Template (Web Distribution)

```markdown
# Paper Title · 论文标题

**Author:** SCX
**Date:** YYYY-MM-DD
**Status:** ⬜ Draft / ⚠️ In Review / ✅ Converged (N rounds)

---

## Abstract

English abstract here.

*中文摘要。*

---

## 1. Introduction

Content with MathJax: $\sum g = 0$ and $$F = d\omega + \omega \wedge \omega$$

> **Theorem 1 (Name).** Statement of theorem.

> **Proof.** Proof of theorem.

### 1.1 Subsection

| Header | Description |
|--------|-------------|
| Item | Description |

> **Honest Critique:** Limitation noted here.

---

## 2. Main Results

## 3. Discussion

## 4. Conclusion

## Appendices

### A. Mathematical Details

### B. Verification

See `verify_*.py` for numerical validation.

## References
```

## 🔧 Key Commands

| LaTeX | Markdown Equivalent |
|-------|-------------------|
| `\section{Title}` | `## Title` |
| `\subsection{Title}` | `### Title` |
| `\begin{theorem}[Name]` | `> **Theorem (Name).**` |
| `\begin{proof}` | `> **Proof.**` |
| `$$...$$` | `$$...$$` (MathJax) |
| `$...$` | `$...$` (MathJax inline) |
| `\textbf{...}` | `**...**` |
| `\textit{...}` | `*...*` |
| `\SCX` | SCX |
| `\Yajie` | Yajie |
| `\cite{key}` | `[key]` |
| `\ref{label}` | cross-reference text |
