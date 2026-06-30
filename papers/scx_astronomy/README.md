# SCX-Audited Multi-Messenger Astrophysics

## Certified Joint Detection from Heterogeneous Observational Experts

### Paper Overview

This paper establishes the SCX auditing framework for multi-messenger astrophysics, treating each instrument (LIGO/Virgo/KAGRA, JWST, IceCube, Fermi, LSST, FAST) as a heterogeneous expert with distinct systematics, signal-to-noise characteristics, and false-alarm profiles. The framework provides rigorous statistical guarantees for joint detection across GW, EM, neutrino, and cosmic-ray channels.

### Key Results

| Theorem | Name | Statement |
|---------|------|-----------|
| **Theorem 1** | Joint Detection Confidence 联合探测置信度 | SCX consensus FAR ≤ exp(−2·K_eff·Δ²) — exponential decay with K_eff = K/(1+(K−1)ρ̄) accounting for correlated systematics |
| **Theorem 2** | Instrumental Artifact vs. New Physics Unidentifiability 仪器假象与新物理不可区分性 | GW-detected but EM-dark events: artifact, selection effect, and dark event interpretations are observationally indistinguishable without declared assumptions |
| **Theorem 3** | Situs Celestial Lipschitz Bound Situs天球Lipschitz定位界 | ‖Δx̂‖ ≤ L_situs · (SNR)⁻¹ · θ_res — bilateral Lipschitz bound for S²×R encoding |

### Theorems Detail

**Theorem 1 (Joint Detection Confidence):** For K instruments with individual false-alarm probabilities α_k, the SCX consensus false-alarm rate is bounded by exp(−2·K_eff·Δ²). Full proof adapting Hoeffding's inequality to Poisson-limited photon/neutrino counting statistics through a de-Poissonization argument. K_eff = K/(1+(K−1)ρ̄) accounts for correlated systematics. When instruments are perfectly correlated (ρ̄ → 1), K_eff → 1.

**Theorem 2 (Instrumental Artifact vs. New Physics):** For a GW-detected event with no EM counterpart, three hypotheses (instrumental artifact H_art, selection effect H_sel, genuinely dark event H_dark) are constructed to be observationally equivalent up to total variation distance ε_TV = O(∏_j p_{det,j}^{max}). No hypothesis test can distinguish them with power exceeding chance level without declared systematic error budgets.

**Theorem 3 (Situs Celestial Lipschitz):** Celestial coordinates (RA, Dec, redshift) are encoded via Situs mapping on S²×R. Lipschitz bound: ‖Δx̂‖ ≤ L_situs · (SNR)⁻¹ · θ_res. L_situs derives from spherical harmonic truncation (angular), log-redshift Fourier modes (radial), and distance-sensitive attenuation (scale).

### SCX Components Applied

- **Yajie**: Multi-instrument weighted consensus with heterogeneous detection thresholds and χ² tension down-weighting
- **Situs**: Spherical harmonic + log-redshift Fourier encoding for (S²×R) celestial coordinates with Lipschitz bound
- **Cercis**: Discovery score S = Q + η·N where Q = Q_loc + Q_spec + Q_time, N = discovery novelty
- **Spring**: Self-evolving gatekeeper for anomalous transients (FRBs, new source classes)

### Benchmarks

1. **GW170817/GRB 170817A** — NS-NS merger with full EM+GW coverage, Cercis score S ≈ 15.0
2. **IceCube-170922A** — neutrino+γ-ray coincidence with TXS 0506+056, analyzed under Theorem 2 unidentifiability
3. **FRB localization** — ASKAP/CHIME/FAST precision comparison via Theorem 3 Lipschitz bounds
4. **LIGO O4/O5** — Projected multi-messenger detection rates and FAR control

### Assumptions

- **A1_mm**: Independent background realizations (physically separated instruments)
- **A2_mm**: Calibrated per-instrument FAR (verified by time-slide/off-source analyses)
- **A3_mm**: Bounded pairwise correlation (ρ̄ ≤ 0.5)
- **A4_mm**: Poisson-to-Gaussian regime (λ·T ≥ 10 expected background counts)
- **B1_mm**: Finite instrumental sensitivity (flux limits)
- **B2_mm**: Non-informative non-detection (valid likelihood for upper limits)
- **B3_mm**: GW glitch morphology (non-zero glitch mimic probability)
- **C1_mm**: Smooth instrumental PSF (Lipschitz-continuous)
- **C2_mm**: Band-limited signal (spherical harmonic cutoff)

### Chinese Keywords

多信使天文 (multi-messenger astronomy), 引力波 (gravitational waves), 中微子 (neutrinos), 联合探测 (joint detection), 仪器假象 (instrumental artifact), 新物理 (new physics), 不可区分性 (unidentifiability), 天球编码 (celestial encoding), 定位界 (localization bound), 虚警率 (false-alarm rate)

### Build

```bash
cd papers/scx_astronomy
xelatex main.tex
xelatex main.tex   # second pass for TOC
```

### Dependencies

- `ctex` package (Chinese support, requires xelatex)
- `amsmath`, `amssymb`, `amsthm`, `mathtools`
- `cleveref`, `hyperref`, `booktabs`

### Conventions

- Chinese+English bilingual throughout
- Rigor labels: 已证明/Proven (provenFull), 部分证明/Partial Proof, 证明概要/Proof Sketch
- All theorems have explicit numbered assumptions (A1_mm–A4_mm, B1_mm–B3_mm, C1_mm–C2_mm)
- Full proofs with de-Poissonization, cluster decomposition, and bilateral Lipschitz derivation
- NO hype — honest Limitations section acknowledging Poisson approximation accuracy, correlation estimation uncertainty, and Situs dimensionality scaling
- Theorems are in the public domain (mathematical results)
