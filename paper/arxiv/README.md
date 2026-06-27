# SCX Paper Series — arXiv Submission Packages

All six papers, ready for arXiv upload. Author: SCX.

| # | Paper | Main .tex | Extras | Total Lines |
|---|-------|-----------|--------|-------------|
| I | A Fundamental Impossibility in Data Quality | main.tex | 8 SI sections | 4,782 |
| II | The Curation-Exploration Tradeoff | main.tex | methods.tex + supp.tex | 563 |
| III | Data Quality Dominates Model Architecture | main.tex | methods.tex + supp.tex | 708 |
| IV | Consistency-Constrained Expert Merging | main.tex | — | 786 |
| V | SCX for LLM Data Curation | main.tex | supp.tex | 967 |
| VI | SCX: A Unified Framework for Data Quality | main.tex | supp.tex | 1,084 |

## How to upload to arXiv

1. Go to https://arxiv.org/submit
2. Upload main.tex + all .tex extras as a single .zip
3. Set author as: SCX
4. Primary subject: cs.LG (Machine Learning) or stat.ML (Machine Learning Statistics)
5. Cross-list as needed

## Cover Letter Template (for Nature submissions — Papers I, II, III)

```
Dear Editor,

We submit "TITLE" for consideration as an Article in JOURNAL.

This paper makes the following contributions:

1. [One-sentence core discovery]
2. [Why it matters to the broad scientific community]
3. [What makes it different from prior work]

Our work does not fit cleanly into any single disciplinary category
but addresses a challenge — data quality assessment — that affects
every field that uses machine learning. We believe it aligns with
JOURNAL's mission to publish research of broad significance.

Thank you for your consideration.

Sincerely,
SCX
```

## Compilation

All papers compile with standard LaTeX (pdflatex, twice). Build scripts at ../build/.
