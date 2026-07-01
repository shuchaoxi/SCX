# arXiv Compatibility Checklist for `papers/scx_climate/main.tex`

Analysis date: 2026-07-01

Source inspected: `papers/scx_climate/main.tex` (1504 lines)

Reference target: the requested arXiv-compatible `article` source. Official arXiv help pages checked:

- https://arxiv.org/help/submit
- https://info.arxiv.org/help/submit_tex.html
- https://info.arxiv.org/help/faq/texlive.html
- https://info.arxiv.org/help/faq/multilang.html

## BLOCKERS

- [ ] **BLOCKER - `ctexart` document class is not the requested arXiv target.**
  - Lines: 9
  - Current source: `\documentclass[11pt,a4paper]{ctexart}`
  - Required action: convert to `\documentclass[11pt]{article}` or another arXiv-accepted standard article class explicitly allowed by the target venue. Remove the `a4paper` option unless there is a specific arXiv-compatible reason to keep it.
  - Why it matters: the requested target says `ctexart` must be replaced by `article`. It also couples the source to a CJK class and nonstandard article behavior.

- [ ] **BLOCKER - Chinese text appears outside the abstract.**
  - Lines: 83, 438, 610, 764, 831
  - Required action: translate/remove these non-abstract Chinese fragments for the arXiv version. If a bilingual submission is intended, prepare a complete English version first and then a complete non-English version according to arXiv multilingual guidance, instead of mixing Chinese snippets into theorem titles and headings.
  - Why it matters: the requested compatibility target flags Chinese characters in non-abstract sections. These lines are in the title and theorem/corollary headings, not only in the abstract.

- [ ] **BLOCKER - `\indep` is used but never defined.**
  - Lines: 324
  - Required action: define it in the preamble, for example `\newcommand{\indep}{\perp\!\!\!\perp}`, or replace the use with an already-defined symbol.
  - Why it matters: this is a real LaTeX compile failure independent of arXiv policy.

## WARNINGS

- [ ] **WARNING - Chinese abstract depends on the current CJK setup.**
  - Lines: 127-137
  - Required action: for a plain `article` arXiv source, either keep only the English abstract or add a deliberate arXiv-compatible Unicode/CJK compilation strategy. If the target is English-only, remove the Chinese abstract.
  - Why it matters: this text is inside `abstract`, so it is not part of the non-abstract blocker above, but it will not survive a simple `ctexart` to `article` conversion without further decisions.

- [ ] **WARNING - Custom page size, margins, and line spacing deviate from plain arXiv article formatting.**
  - Lines: 9, 17, 21-22
  - Current source: `a4paper`, `geometry`, `setspace`, `\onehalfspacing`
  - Required action: remove custom page geometry and line spacing unless there is a specific reason to keep them. Use the default `article` layout for the arXiv source.
  - Why it matters: these are journal/referee-style formatting controls, not content requirements.

- [ ] **WARNING - Title uses manual visual formatting and bilingual subtitle.**
  - Lines: 81-83
  - Required action: use a simple English title without manual `\textbf`, forced line breaks, explicit vertical spacing, `\large`, or the Chinese subtitle.
  - Why it matters: the Chinese subtitle is a blocker; the manual title styling is also unnecessary formatting for an arXiv source.

- [ ] **WARNING - Table of contents is included in the article body.**
  - Lines: 143
  - Required action: remove `\tableofcontents` unless the arXiv version intentionally needs it.
  - Why it matters: a table of contents is unusual for a standard arXiv article and changes the presentation without adding source compatibility value.

- [ ] **WARNING - Colored rigor labels are nonstandard formatting.**
  - Definition lines: 42-47
  - Use lines: 104, 108, 113, 132, 134, 137, 281, 313, 434, 584, 736, 780, 861, 936, 996, 1030, 1076, 1194, 1348, 1358, 1368
  - Required action: either remove these labels for the arXiv version or convert them to plain text annotations that do not rely on color/symbol encoding.
  - Why it matters: `xcolor`, `\blacksquare`, and star badges are technically supportable, but the formatting is atypical and color-dependent.

- [ ] **WARNING - `\textdegree` may require a compatibility decision.**
  - Lines: 1137
  - Required action: either replace `\textdegree` with `$^\circ$` or explicitly load a package/LaTeX format that provides it.
  - Why it matters: current LaTeX formats usually provide this command, but it is a portability risk in a minimal `article` conversion.

- [ ] **WARNING - Non-ASCII source characters appear in comments and headings.**
  - Comment/source hygiene lines: 4, 11, 24, 41, 49, 60, 429, 579, 775
  - Content lines also affected: 83, 127-137, 438, 610, 764, 831
  - Required action: for the plain `article` arXiv source, replace decorative Unicode comment separators and em dashes with ASCII comments, and address the content lines listed above.
  - Why it matters: comments normally do not affect compilation, but keeping the source ASCII-clean reduces encoding surprises after class conversion.

- [ ] **WARNING - `enumitem` is used only for compact/custom list formatting.**
  - Package line: 18
  - Use lines: 243, 594, 621, 746, 841, 944, 1012, 1052, 1101, 1130, 1142, 1155, 1169, 1178, 1201, 1304
  - Required action: keep only if these custom list labels are important. Otherwise use standard `itemize`/`enumerate`.
  - Why it matters: this is not a blocker, but it is another presentation customization beyond a plain arXiv article source.

## Checks With No Blocking Issue Found

- No external source dependencies were detected: no `\input`, `\include`, `\includegraphics`, `\bibliography`, `\addbibresource`, or external `.bib` file use.
- Citation keys used by `\cite{...}` all have matching inline `\bibitem{...}` entries.
- Referenced labels all have matching `\label{...}` entries.
- Standard math/theorem packages in the source are broadly arXiv-compatible: `amsmath`, `amssymb`, `amsthm`, `mathtools`, `bm`, `booktabs`, `graphicx`, `hyperref`, `cleveref`, and `xcolor`.
- Three inline bibliography entries are currently unused: `bahadur1960`, `cover2006`, and `hoeffding1963`. This is cleanup-only, not an arXiv compatibility blocker.

## Minimal Action Plan

1. Replace line 9 with `\documentclass[11pt]{article}`.
2. Remove or translate non-abstract Chinese lines 83, 438, 610, 764, and 831.
3. Define or replace `\indep` at line 324.
4. Decide whether to keep the Chinese abstract; if keeping it, choose an arXiv-compatible Unicode/CJK strategy instead of relying on `ctexart`.
5. Remove layout/referee styling: `a4paper`, `geometry`, `setspace`, `\onehalfspacing`, and likely `\tableofcontents`.
6. Simplify color-dependent rigor labels and other presentation-only customizations.
