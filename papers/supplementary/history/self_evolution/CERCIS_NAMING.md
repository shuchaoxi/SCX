# Cercis Algorithm
(紫荆花算法)

**Author:** SCX

> **Formal name**: Cercis Self-Evolving Gatekeeper (CESG)
> **Location**:
> /g/Xiaogan\_Supercomputing\_data/SCX/theory/self\_evolution/
> **Paper target**: Nature Computational Science (Paper 2 of
> two-paper strategy)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Why ``Cercis''<!-- label: why-cercis -->

*Cercis chinensis* (紫荆) is a **cauliflorous** tree --- its
flowers bloom directly from old branches and trunks, not from new
shoots.

\begin{verbatim}
Cercis biological metaphor → SCX mathematical reality:

  Old branches & trunk    →  Memory bank M_t (accumulated structures, never deleted)
  Flowers                 →  Gatekeeper evaluations (new scores on old structures)
  Each spring bloom       →  Each iteration: S_t re-scores M_t
  Cauliflory              →  Resurrection: discarded structures "bloom" when S_t matures
  New shoots              →  Novelty bonus η(t) · N_t(s) — exploration
  Deep roots              →  DFT/experimental ground truth (physical anchor)
\end{verbatim}

**Tagline for paper**: *``Knowledge does not grow from new
data alone --- it flowers from the old wood of accumulated
experience.''*

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Paper 2: Cercis Flowers<!-- label: paper-2-cercis-flowers -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.4286}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5714}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Item
\end{minipage} & \begin{minipage}[b]
Detail
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Title** & *Cercis Flowers: A Self-Evolving Gatekeeper with
Provable Convergence* 

**Core Theorems** & Theorem SE-1 (Convergence), Theorem SE-2
(Completeness Bound) 

**Target** & Nature Computational Science / Nature Machine
Intelligence 

**Depends on** & SCX framework (Paper 1, JMLR/TMLR) 

**Location** & `theory/self\_evolution/` (theorems),
`paper/paper\_gatekeeper/` (manuscript) 

\end{longtable}