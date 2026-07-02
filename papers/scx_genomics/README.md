# SCX-Audited Genomics

## Certified Variant Pathogenicity Prediction via Multi-Algorithm Consensus

**SCX Genomics Working Group** — Xiaogan Supercomputing Center & Nous Research  
*June 2026*

---

## Overview

This repository contains the LaTeX source for the SCX-Audited Genomics theoretical paper, which formalizes variant pathogenicity prediction (变异致病性预测) within the SCX (Supercomputing Certification eXchange) audit framework.

The paper addresses a fundamental challenge in clinical genomics: when multiple computational variant effect predictors (SIFT, PolyPhen-2, CADD, REVEL, PrimateAI, AlphaMissense, ESM-1v) disagree, is the disagreement due to algorithmic bias (标注偏差) or genuinely novel biology (新生物学)?

## Paper Structure

| Section | Content |
|---------|---------|
| 1. Introduction | Motivation, related work, contributions |
| 2. Formalization | Genomic context state, expert predictor model, SCX mapping |
| 3. Theorem 1 | Multi-Predictor Error Detection with effective multiplicity $`M_{\text{eff}}`$ |
| 4. Theorem 3 | Annotation Error vs. True Novel Variant Unidentifiability |
| 5. Cercis Score | Dual-component metric: reliability ($`Q`$) + evolutionary novelty ($`N`$) |
| 6. Situs Encoding | Protein 3D structural context as physical coordinate system |
| 7. Yajie Consensus | Multi-algorithm consensus protocol (多算法共识) with 3-tier certification |
| 8. Experimental Protocol | Validation plan across ClinVar, gnomAD, and MAVE datasets |
| 9. Discussion | Clinical/regulatory implications, limitations, future work |

## Key Theorems

### Theorem 1: Multi-Predictor Systematic Error Detection

With $`M`$ correlated predictors of effective multiplicity $`M_{\text{eff}} = M / (1 + (M-1)\bar)`$, systematic annotation errors exceeding a consensus-margin threshold are detectable with probability at least $`1 - \exp(-2M_{\text{eff}}\varepsilon^2)`$.

**Minimum detectable bias:** $`\tau_ \approx 1.36 / \sqrt{M_{\text{eff}}}`$ at 95% confidence.

### Theorem 3: Unidentifiability

Without an explicit declaration of distributional assumptions connecting training and novel variant distributions, algorithmic bias and novel biology are **observationally indistinguishable** from predictor outputs alone. Resolution requires orthogonal experimental evidence (e.g., MAVE functional assays).

### Key Insight

> The effective multiplicity $`M_{\text{eff}}`$ has a finite upper bound of $`1/\bar`$ as $`M \to \infty`$ — adding more correlated predictors yields diminishing returns.

## Cercis Score

The **Cercis Score** $`\mathcal{C}(f) = (Q_f, N_f)`$ jointly quantifies:

- **$`Q_f`$ (Reliability Quotient):** $`Q_f = \alpha \cdot Q_f^{\text{ClinVar}} + (1-\alpha) \cdot Q_f^{\text{func}}`$
  - ClinVar concordance (star-weighted accuracy)
  - Functional assay correlation (Spearman-$`\rho`$ with MAVE data)
- **$`N_f`$ (Novelty Sensitivity):** responsiveness to evolutionarily unexpected variants

## Situs Encoding

The **Situs encoding** $`\mathcal{S}(k)`$ captures a variant's physical position within protein 3D structure:

- $`C_\alpha`$ coordinate
- Spatial neighborhood (8 Å radius)
- Local geometric context (Gaussian-weighted neighbor vectors)
- Packing density
- Domain embedding

A situs-aware distance metric enables structural nearest-neighbor label transfer with Lipschitz guarantees.

## Yajie Consensus Protocol

The **Yajie consensus** (雅洁共识 — "elegant purity") implements multi-algorithm consensus in four stages:

1. **Calibration:** Isotonic regression per predictor
2. **Weighting:** Cercis-derived weights $`w_i = Q_i \cdot \exp(-\gamma N_i)`$
3. **Aggregation:** Weighted average of calibrated scores
4. **Certification:** Three-tier output
   - 🟢 **Certified** — high margin, sufficient effective multiplicity
   - 🟡 **Provisional** — moderate margin or structural support
   - 🔴 **Uncertain** — recommend orthogonal assay

## Experimental Datasets

| Dataset | Size | Use |
|---------|------|-----|
| ClinVar | ~195K missense variants (2+ stars) | Calibration, testing, Cercis $`Q`$ |
| gnomAD v4.1 | 807K+ individuals | Population frequencies, novelty detection |
| MAVE (MaveDB) | BRCA1, PTEN, TP53 + more | Functional ground truth, unidentifiability resolution |

## Building

```bash
cd papers/scx_genomics
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Requires a standard LaTeX distribution (TeX Live 2023+ or MiKTeX) with packages:
`amsmath`, `amssymb`, `amsthm`, `mathtools`, `bm`, `algorithm`, `algpseudocode`, `booktabs`, `cleveref`, `hyperref`, `geometry`, `CJKutf8`.

## SCX Framework Mapping

| SCX Component | Genomics Instantiation |
|---------------|----------------------|
| State ($`\mathcal{S}`$) | Genomic context (variant + sequence + structure + population + evolutionary features) |
| Expert ($`f_i`$) | Variant effect predictor |
| Claim ($`\gamma_i(s)`$) | Pathogenicity score + uncertainty |
| Audit Layer | Yajie consensus protocol |
| Reliability Score | Cercis $`Q`$ |
| Certification | 3-tier (Certified / Provisional / Uncertain) |
| Structural Context | Situs encoding |

## Key Chinese Terminology

| English | 中文 |
|---------|------|
| Genome / Genomics | 基因组 |
| Variant pathogenicity | 变异致病性 |
| Multi-algorithm consensus | 多算法共识 |
| Annotation bias / error | 标注偏差 |
| Novel biology | 新生物学 |
| Prediction error | 预测误差 |
| Assumption declaration | 假设声明 |
| Orthogonal evidence | 正交证据 |
| Indications for use | 适应症 |
| Genomic equity | 基因组公平性 |

## Regulatory Relevance

The paper's unidentifiability theorem has direct implications for:
- **FDA** AI/ML-based Software as a Medical Device (SaMD) framework
- **EU IVDR** In Vitro Diagnostic Regulation
- **NMPA** (中国NMPA) medical device registration

We recommend that regulatory submissions include:
1. A **Cercis Score report** for all algorithmic components
2. An **Assumption Declaration Document (ADD)** specifying domain of applicability
3. **Uncertainty quantification** for out-of-domain predictions

## License

This work is part of the SCX research program. See repository root for license information.

## Citation

```bibtex
@techreport{scx-genomics-2026,
  title     = {{SCX-Audited Genomics: Certified Variant Pathogenicity Prediction via Multi-Algorithm Consensus}},
  author    = {{SCX Genomics Working Group}},
  institution = {Xiaogan Supercomputing Center \& Nous Research},
  year      = {2026},
  month     = jun
}
```