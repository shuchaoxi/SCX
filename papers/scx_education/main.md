*Abstract:*

Educational assessment---from classroom grading to high-stakes standardized testing---relies on the fundamental act of assigning scores to student work. Yet the scoring enterprise lacks formal certification: a single grader (teacher, examiner, or automated system) produces a single score, and that score is treated as truth. We apply the SCX{} (Structured Causal eXamination) auditing framework to educational assessment, treating each grader as an **expert** and each score as a **claim** about student competence. The core thesis: unless $M \ge M_$ independent graders certify a score through Yajie{} consensus, that score is unverifiable. We prove five theorems:
(1)~**Multi-Grader Detection Bound 多评卷人检测界**: Under blind grading conditions (A1 independence), the probability that all $M$ graders miss a scoring error of magnitude $\Delta$ is bounded by $\exp(-2M_{eff}\Delta^2 / B^2)$, where $B$ is the scoring range.
(2)~**Rubric Consensus = Yajie Consensus 评分标准共识即Yajie共识**: When $M$ graders apply a common rubric $\rubric$ to student $s$'s work, the Yajie{} consensus score $\hat_{Yajie}$ converges to the true latent score $\trueScore_s$ at rate $O(1/\sqrt{M_{eff}})$ as grader expertise is bounded below $1/2 + \gamma$.
(3)~**Grade Inflation Detection 分数膨胀检测**: Systematic upward drift $\inflationRate > 0$ in cohort-averaged scores is detectable with probability $\ge 1 - \exp(-2M_{eff}\inflationRate^2)$ when $M$ graders are drawn from temporally-independent pools, establishing inflation as a detectable structural bias.
(4)~**Blind Grading = A1 Enforcement 盲审即A1强制**: Removing student identity and inter-grader communication reduces inter-grader error correlation $\bar$ by factor $1 - \beta$, where $\beta \in [0,1]$ is the blindness index, increasing effective multiplicity $M_{eff} = M/(1 + \bar(1-\beta))$.
(5)~**AI-Human Grading = Multi-Modal Audit AI与人类评分即多模态审计**: AI graders and human graders constitute heterogeneous expert modalities with distinct error profiles. Their disagreement pattern decomposes into $\Var(\hat_{AI} - \hat_{human}) = \sigma_{AI}^2 + \sigma_{human}^2 - 2\Cov(\hat_{AI}, \hat_{human})$, enabling modality-specific calibration.

We operationalize these theorems through the Cercis{} Score for assessment systems: $S = Q + \eta N$, where $Q$ measures the fraction of SCX{} theorems the scoring system satisfies and $N$ measures empirical scoring reliability. A single-grader system receives $Q = 0$ and $S \le 0.20$ regardless of grader expertise — the grader cannot certify their own accuracy (Theorem~2). A $K$-grader rubric system with blind review receives $Q = 0.60$–$0.80$. A fully SCX{}-compliant assessment ($M \ge M_$ blind graders, Spring{} permanent scoring records, Yajie{} consensus) achieves $Q = 1.0$ and certified scoring. We provide experimental protocols for the Gaokao (高考), SAT, and essay-grading contexts, and close with an honest discussion of limitations: the cost of $M$ graders, the impossibility of zero correlation, and the incommensurability of certain rubric dimensions.

**摘要.**
教育评估——从课堂评分到高风险标准化考试——都依赖于对学生作业赋分这一基本行为。然而，评分事业缺乏正式认证：单个评分者（教师、考官或自动系统）产生单一分数，该分数即被视为真理。我们将SCX{}审计框架应用于教育评估，将每位评分者视为**专家**，将每个分数视为关于学生能力的**声明**。核心论点：除非$M \ge M_$位独立评分者通过Yajie{}共识认证一个分数，否则该分数不可验证。我们证明了五条定理：(1)多评卷人检测界；(2)评分标准共识即Yajie共识；(3)分数膨胀检测；(4)盲审即A1强制；(5)AI与人类评分即多模态审计。我们通过评估系统的Cercis{}评分来操作化这些定理，并为高考、SAT和作文评分提供实验方案。

**Keywords:** educational assessment 教育评估, multi-grader consensus 多评卷人共识, grade inflation 分数膨胀, blind grading 盲审, standardized testing 标准化考试, AI grading AI评分, SCX{} auditing SCX{}审计, Yajie{} consensus Yajie{}共识, Cercis{} score Cercis{}评分, rubric certification 评分标准认证, Gaokao 高考, scoring bias 评分偏差

## Introduction 引言：评分即声明，评卷人即专家

Educational assessment is the world's most consequential measurement enterprise. Every year, hundreds of millions of students receive scores — on classroom assignments, end-of-term examinations, university entrance exams (高考, SAT, A-Levels, Abitur), professional licensing tests, and language proficiency certifications. These scores determine university admissions, scholarship awards, job qualifications, and immigration eligibility. The total stakes, measured in human life trajectories, are incalculable.

Yet the scoring enterprise operates under a structural assumption so fundamental that it is rarely examined: **one grader produces one score, and that score is treated as the truth.**

Consider three canonical scenarios:

- **Classroom grading 课堂评分.** A teacher grades 30 essays. Each essay receives one score from one grader. If the teacher is tired, biased, or inconsistent — the score stands. There is no second opinion, no audit mechanism, no formal guarantee that the score reflects the student's true competence.
- **Standardized testing 标准化考试.** The Gaokao (高考) processes approximately 12 million scripts annually. Essays are typically double-graded (two human raters), with third-grade arbitration when scores diverge by more than a threshold — an implicit $M=2$ (or $M=3$ on disagreement) system. But the graders are trained on the same rubric, calibrated on the same anchor scripts, and subject to the same institutional pressures. Their effective multiplicity $M_{eff}$ may be far lower than the nominal $M$.
- **AI grading AI评分.** Automated essay scoring (AES) systems — from e-rater [cite] to GPT-4-based graders — produce instantaneous scores at near-zero marginal cost. But an AI grader is $M=1$: one model, one training corpus, one scoring function. The model cannot certify its own accuracy (Theorem~2 of SCX{}). When the AI and a human disagree, who is right? Without a formal audit framework, the question is undecidable.

The common thread: **scores are claims about latent student competence, and graders are experts making those claims.** This mapping — graders $\leftrightarrow$ experts, scores $\leftrightarrow$ claims — is the foundational insight that enables SCX{} auditing of educational assessment. Every theorem in the SCX{} framework translates directly to a constraint on scoring validity.

### The Educational Assessment Landscape 教育评估格局

Educational assessment spans a spectrum from low-stakes formative assessment to high-stakes summative certification. We focus on the subset where formal certification matters:

1. **High-stakes examinations 高风险考试.** Gaokao (高考, China, $\sim$12M/year), SAT/ACT (USA, $\sim$4M/year), GCSE/A-Levels (UK, $\sim$5M/year), Abitur (Germany), Baccalauréat (France). These examinations determine access to higher education and, by extension, lifetime earnings trajectories.
2. **Professional licensing 职业资格考试.** Bar examinations, medical board exams (USMLE, PLAB), accounting certifications (CPA, ACCA), engineering licensure (PE, CEng). Scoring errors in these contexts have direct professional consequences.
3. **Language proficiency 语言能力测试.** IELTS, TOEFL, HSK, DELF/DALF. These determine immigration eligibility and university admission for international students.
4. **Large-scale assessments 大规模教育评估.** PISA (OECD, $\sim$80 countries), TIMSS, PIRLS, NAEP (USA). These inform national education policy and international comparisons.

In each context, the assessment system produces scores. The question SCX{} asks is not ``are the scores accurate on average?'' — many are. The question is: ``**can the assessment system certify the accuracy of each individual score?**''

### The Audit Gap in Education 教育审计缺口

The audit gap in educational assessment is the distance between *aggregate scoring reliability* (inter-rater reliability coefficients, Cronbach's $\alpha$, Cohen's $\kappa$) and *individual score certification* (knowing whether *this* score for *this* student on *this* question is correct). The assessment literature has developed sophisticated tools for measuring aggregate reliability [cite], but these tools do not certify individual scores.

> **Definition:** [Educational Audit Gap 教育审计缺口]
> <!-- label: def:audit_gap -->
> For an assessment system $\cA$ that produces score $v_s$ for student $s$, the audit gap is:
> 
> $$
>     Gap(\cA) = \Pbb(v_s = \trueScore_s \mid system reports  v_s) - \Pbb(v_s = \trueScore_s \mid external auditor certifies  v_s),
> $$
> 
> where $\trueScore_s$ is the latent true score. A system with $Gap(\cA) > 0$ has unverifiable scores: the system's self-reported confidence exceeds the confidence warranted by independent audit.

The audit gap manifests in several well-documented phenomena:

1. **Grade inflation 分数膨胀.** Over decades, mean grades in secondary and tertiary education have drifted upward without corresponding increases in measured competence [cite]. In the UK, the proportion of A-level entries awarded A or A* rose from 8.8\% (1982) to 44.8\% (2021). In US higher education, the modal grade shifted from C (1960s) to A (2010s). A single grader (or institution) cannot detect its own inflation — the drift is visible only through external comparison (Theorem~2: self-audit = no audit).
2. **Scoring inconsistency 评分不一致.** The same essay graded by different raters can receive substantially different scores. In a meta-analysis of essay scoring reliability, inter-rater correlations ranged from $r = 0.55$ to $r = 0.85$ [cite]. The difference between a passing and failing score can be a matter of which grader was assigned.
3. **AI-human disagreement AI与人类评分分歧.** AI grading systems produce scores that correlate with human scores but systematically differ in distribution (lower variance, regression to the mean). Without a multi-expert framework, determining whether the AI or the human is ``correct'' is logically underdetermined.
4. **Rubric ambiguity 评分标准模糊性.** Scoring rubrics (\rubric) define the mapping from student work to scores. But rubrics are themselves claims about what constitutes quality. A rubric is a consensus among its designers — a Yajie{} consensus at the design level. When rubrics are applied by a single grader, the consensus is lost.

### Mapping Education to SCX 教育到SCX的映射

The conceptual mapping that structures this paper:

[Table omitted — see original .tex]

### Our Contribution

We provide:

1. **Formalization** (Section [ref]): The assessment scoring game with $M$ graders, $K$ rubric dimensions, and explicit grader expertise and bias parameters. Seven assumptions \assumptionTag{1}--\assumptionTag{7} declared.
2. **Five Theorems with Proofs** (Sections [ref]-- [ref]):
3. **Cercis{} Score for Assessment Systems** (Section [ref]): $S(\cA) = Q(\cA) + \eta \cdot N(\cA)$ quantifying the certification quality of any scoring system.
4. **Experimental Protocols** (Section [ref]): Concrete protocols for Gaokao essay scoring, SAT scoring, and AI-assisted grading with Spring{} permanent records.
5. **Discussion** (Section [ref]): Honest limitations — the cost of $M$ graders, irreducible inter-grader correlation, rubric incommensurability, and the political economy of grade inflation.

## Formalization: The Assessment Scoring Game 形式化：评估评分博弈
<!-- label: sec:formalization -->

### The Assessment State Space 评估状态空间

> **Definition:** [Student Competence 学生能力]
> <!-- label: def:competence -->
> For a student $s \in \studentSet$, the true latent competence on assessment dimension $k \in [K]$ is $\trueScore_s^{(k)} \in [0, B_k] \subset \R$, where $B_k$ is the maximum score on dimension $k$. The full competence vector is:
> 
> $$
>     \boldsymbol_s = (\trueScore_s^{(1)}, ..., \trueScore_s^{(K)}) \in \cT = \prod_{k=1}^K [0, B_k].
> $$
> 
> For holistic scoring ($K=1$), $\trueScore_s \in [0, B]$.

The competence $\boldsymbol_s$ is latent — it cannot be directly observed. Assessment is the process of estimating $\boldsymbol_s$ from observable student work $w_s$ (essay, exam answers, project, oral examination).

> **Definition:** [Student Work 学生作业]
> <!-- label: def:work -->
> Student $s$ produces work $w_s \in \cW$, where $\cW$ is the space of all possible responses to the assessment task. The mapping from competence to work is stochastic:
> 
> $$
>     w_s \sim p(w \mid \boldsymbol_s, \xi_s),
> $$
> 
> where $\xi_s$ captures idiosyncratic factors (test anxiety, time pressure, luck in question selection) independent of $\boldsymbol_s$.

### The Grader as Expert 评卷人作为专家

> **Definition:** [Grader 评卷人]
> <!-- label: def:grader -->
> A grader $g \in \graderSet = \{g_1, ..., g_M\}$ is a function:
> 
> $$
>     g_m: \cW \times \rubric \to [0, B],
> $$
> 
> that maps student work $w_s$ and a rubric $\rubric$ to a score $v_{s,m} = g_m(w_s, \rubric)$. Each grader has:
> 
- **Expertise 专业水平** $\expertiseVec_m \in [0,1]$: the probability that the grader correctly identifies the quality level of work, $\Pbb(|g_m(w_s, \rubric) - \trueScore_s| \le \delta \mid \trueScore_s) \ge \expertiseVec_m$ for $\delta > 0$.
- **Bias 偏差** $\biasVec_m \in [-B, B]$: systematic over- or under-scoring tendency, $\E[g_m(w_s, \rubric) - \trueScore_s] = \biasVec_m$.
- **Variance 方差** $\sigma_m^2$: random scoring noise around the biased estimate.

The grader's score production function is:

$$
    v_{s,m} = \trueScore_s + \biasVec_m + \varepsilon_{s,m}, \quad \varepsilon_{s,m} \sim \cD_m(0, \sigma_m^2),
$$

where $\cD_m$ is grader $m$'s error distribution (not necessarily Gaussian).

### The Rubric as \Situs{ Encoding 评分标准作为Situs编码}

> **Definition:** [Rubric 评分标准]
> <!-- label: def:rubric -->
> A rubric $\rubric$ is a \Situs{} encoding that partitions the work space $\cW$ into quality regions and maps each region to a score. Formally:
> 
> $$
>     \rubric = \{\phi_k: \cW \to [0, B_k]\}_{k=1}^K \cup \{\psi: [0, B_1] \times ... \times [0, B_K] \to \cW\},
> $$
> 
> where $\phi_k$ is the scoring function for dimension $k$ and $\psi$ is the (partial) decoder — the exemplar work that ``represents'' a given score combination. The rubric's quality is:
> 
> $$
>     Q_(\rubric) = (1 - \varepsilon_\rubric) \cdot \exp(-L_\rubric \cdot \sigma_w^2),
> $$
> 
> where $\varepsilon_\rubric$ is the reconstruction error (how well exemplars represent score levels) and $L_\rubric$ is the rubric's Lipschitz constant (sensitivity of scores to small work variations).

A well-designed rubric has low $L_\rubric$ (similar work receives similar scores) and low $\varepsilon_\rubric$ (exemplars accurately represent score levels). A poorly-designed rubric has high $L_\rubric$ (score changes dramatically for minor work differences) or high $\varepsilon_\rubric$ (exemplars are unrepresentative).

### Core Assumptions 核心假设

\begin{assumption}[Independent Grader Training — A1 独立评卷人训练]
<!-- label: asm:A1_edu -->
Each grader $g_m$ is trained independently: they receive disjoint calibration sets $\cD_m \subset \cD_{cal}$, do not communicate during training, and do not observe other graders' scores before producing their own. Formally, for $m \neq m'$: $I(\cD_m; \cD_{m'}) = 0$, and grader $m$'s scoring function $g_m(\cdot, \rubric)$ is conditionally independent of $g_{m'}(\cdot, \rubric)$ given $\rubric$.
\end{assumption}

\begin{assumption}[Conditional Grader Independence — A2 条件评卷人独立]
<!-- label: asm:A2_edu -->
Given the true score $\trueScore_s$, grader errors are conditionally independent:

$$
    \Pbb(\varepsilon_{s,m} = a, \varepsilon_{s,m'} = b \mid \trueScore_s) = \Pbb(\varepsilon_{s,m} = a \mid \trueScore_s) \cdot \Pbb(\varepsilon_{s,m'} = b \mid \trueScore_s), \quad \forall m \neq m'.
$$

In practice, graders share rubric $\rubric$, creating correlation. We define the **effective multiplicity**:

$$
    M_{eff} = \frac{M}{1 + \bar_{grader}},
$$

where $\bar_{grader} = \frac{2}{M(M-1)}\sum_{m<m'}\Corr(\varepsilon_{s,m}, \varepsilon_{s,m'})$ is the average inter-grader error correlation.
\end{assumption}

\begin{assumption}[Bounded Grader Competence — A3 有界评卷人能力]
<!-- label: asm:A3_edu -->
Each grader achieves accuracy strictly better than random scoring within the score band $\delta$. For $B$ score levels:

$$
    \Pbb(|v_{s,m} - \trueScore_s| \le \delta \mid \trueScore_s) > \frac{2\delta}{B}, \quad \forall m \in [M].
$$

Equivalently, each grader's scoring function is informative: $\expertiseVec_m > 2\delta/B$.
\end{assumption}

\begin{assumption}[Detectable Scoring Error Margin — A4 可检测评分误差边界]
<!-- label: asm:A4_edu -->
When a scoring error of magnitude $\Delta > 0$ occurs, at least one grader detects it with probability $p_d \ge 1/2 + \gamma$ for some $\gamma > 0$:

$$
    \E[\ind{|v_{s,m} - \trueScore_s| > \Delta} \mid scoring error  \Delta  exists] \ge \frac{1}{2} + \gamma.
$$

\end{assumption}

\begin{assumption}[Stationary Student Distribution — A5 平稳学生分布]
<!-- label: asm:A5_edu -->
The distribution of student competence $\boldsymbol_s$ across cohorts is stationary within regime: $\boldsymbol_s \sim \cP_t$ where $\cP_t = \cP_{t-1}$ unless a structural break (curriculum reform, demographic shift, assessment redesign) has occurred. Distribution shift $\cP_t \to \cP_{t+1}$ is detectable via Spring{} gating.
\end{assumption}

\begin{assumption}[Blindness Feasibility — A6 盲审可行性]
<!-- label: asm:A6_edu -->
Student identity markers can be removed from work $w_s$ with high probability: $P(identity revealed after redaction) \le \varepsilon_{redact} \ll 1$. For written work, this is achievable through anonymization protocols. For oral examinations or performance assessments, blindness is partial: $\varepsilon_{redact} > 0$.
\end{assumption}

\begin{assumption}[Rubric Stability — A7 评分标准稳定性]
<!-- label: asm:A7_edu -->
The rubric $\rubric$ is stable across the assessment period: $\rubric_t = \rubric_{t-1}$ for all $t$ in the assessment window. Changes to $\rubric$ constitute a structural break and require re-audit.
\end{assumption}

## Theorem 1: Multi-Grader Detection Bound 定理1：多评卷人检测界
<!-- label: sec:theorem1 -->

> **Theorem:** [Multi-Grader Scoring Error Detection 多评卷人评分误差检测]
> <!-- label: thm:detection -->
> Let $\cG = \{g_1, ..., g_M\}$ be $M$ graders satisfying A1--A4, scoring student work on the range $[0, B]$ with effective multiplicity $M_{eff} = M/(1 + \bar_{grader})$. For any scoring error of magnitude $\Delta > 0$, the probability that all $M$ graders fail to detect the error satisfies:
> 
> $$
>     \Pbb\left(\bigcap_{m=1}^M \{|v_{s,m} - \trueScore_s| \le \Delta\}\right) \le \exp\left(-\frac{2 M_{eff} \Delta^2}{B^2}\right).
>     <!-- label: eq:detection_bound -->
> $$

> **Proof:** Define the error detection indicator for grader $m$:
> 
> $$
>     Z_m = \ind{|v_{s,m} - \trueScore_s| > \Delta}.
> $$
> 
> Under A4, $\E[Z_m \mid error exists] = p_m \ge 1/2 + \gamma$. Under A2, $Z_m \perp Z_{m'}$ given $\trueScore_s$ (with residual correlation $\bar_{grader}$ captured by $M_{eff}$).
> 
> The event ``all $M$ graders miss the error'' is $\bigcap_{m=1}^M \{Z_m = 0\}$. By Hoeffding's inequality for the sample mean $\bar{Z} = \frac{1}{M}\sum_{m=1}^M Z_m$:
> 
> $$
>     \Pbb(\bar{Z} - \E[\bar{Z}] \le -t) \le \exp(-2 M_{eff} t^2),
> $$
> 
> where the range of $Z_m$ is $[0,1]$. Setting $t = \E[\bar{Z}] = \bar{p} \ge 1/2 + \gamma$ and noting that $t \ge \Delta/B$ (since the minimum detectable error as a fraction of the scoring range determines detection probability):
> 
> $$
>     \Pbb(\bar{Z} = 0) = \Pbb(\bar{Z} - \bar{p} \le -\bar{p}) \le \exp(-2 M_{eff} \bar{p}^2) \le \exp\left(-\frac{2 M_{eff} \Delta^2}{B^2}\right),
> $$
> 
> where the last inequality uses $\bar{p} \ge \Delta/B$ (a grader detecting error $\Delta$ on range $B$ must have accuracy deviating from random by at least $\Delta/B$).  $\square$

> **Corollary:** [Single-Grader Insufficiency 单评卷人不足性]
> <!-- label: cor:single_grader -->
> For $M=1$, the detection probability is at most $1 - \exp(-2\Delta^2/B^2)$. For a typical scoring range $B=100$ (percentage scale) and minimum meaningful error $\Delta=10$ (one letter grade), $\Pbb(detect) \le 1 - e^{-0.02} \approx 0.0198$. A single grader has less than 2\% probability of detecting a 10-point scoring error — the grader is epistemically blind to their own mistakes.

> **Corollary:** [Required Number of Graders 所需评卷人数量]
> <!-- label: cor:required_M -->
> To achieve error detection probability $\ge 1 - \varepsilon$, the required number of independent graders is:
> 
> $$
>     M \ge \frac{B^2 \ln(1/\varepsilon)}{2 \Delta^2} \cdot (1 + \bar_{grader}).
>     <!-- label: eq:M_required_edu -->
> $$
> 
> For $B=100$, $\Delta=5$, $\varepsilon=0.05$, $\bar_{grader}=0.3$: $M \ge \frac{10000 \cdot 2.996}{2 \cdot 25} \cdot 1.3 = 77.9 \Rightarrow M \ge 78$. This explains why high-stakes essay scoring with two raters ($M=2$) provides negligible formal error detection. For $\Delta=15$ (three letter grades on a 100-point scale), $M \ge 8.7 \Rightarrow M \ge 9$.

> **Remark:** [The Gaokao Double-Grading Gap 高考双评缺口]
> The Gaokao essay scoring protocol uses $M=2$ graders with third-grade arbitration when scores diverge by $\tau$ (typically $\tau=6$ on a 60-point essay scale). Under our framework, $M=2$ with $\bar_{grader} \approx 0.5$ (same training, same rubric, shared institutional context) gives $M_{eff} = 2/1.5 \approx 1.33$. The detection probability for a $\Delta=10\%$ error on a 60-point scale ($\Delta=6$) is:
> 
> $$
>     \Pbb(detect) \le 1 - \exp\left(-\frac{2 \cdot 1.33 \cdot 6^2}{60^2}\right) = 1 - e^{-0.0266} \approx 0.026.
> $$
> 
> The system detects at most 2.6\% of significant scoring errors — effectively no detection. The third-grade arbitration improves this slightly: $M_{eff} \approx (3)/(1+0.5) = 2.0$ when triggered, yielding $\Pbb(detect) \le 1 - e^{-0.04} \approx 0.039$.

## Theorem 2: Rubric Consensus = Yajie Consensus 定理2：评分标准共识即Yajie共识
<!-- label: sec:theorem2 -->

> **Theorem:** [Rubric-Guided Yajie Consensus 评分标准引导的Yajie共识]
> <!-- label: thm:rubric_yajie -->
> Let $M$ graders produce scores $\{v_{s,m}\}_{m=1}^M$ for student $s$ under rubric $\rubric$ with A1--A4. Define the Yajie{} consensus score:
> 
> $$
>     \hat_{Yajie}(s) = \sum_{m=1}^M \omega_m \cdot v_{s,m}, \quad \omega_m = \frac{1/\sigma_m^2}{\sum_{j=1}^M 1/\sigma_j^2},
> $$
> 
> where $\sigma_m^2 = \Var(v_{s,m} \mid \trueScore_s)$ is grader $m$'s scoring variance. Then:
> 
> $$
>     \E\left[(\hat_{Yajie}(s) - \trueScore_s)^2\right] \le \frac{1}{\sum_{m=1}^M 1/\sigma_m^2} + \left(\sum_{m=1}^M \omega_m \biasVec_m\right)^2,
>     <!-- label: eq:yajie_mse -->
> $$
> 
> and the consensus converges to the unbiased true score at rate $O(1/\sqrt{M_{eff}})$ when $\biasVec_m = 0$ for all $m$.

> **Proof:** Decompose the Yajie{} consensus error:
> 
> $$
>     \hat_{Yajie}(s) - \trueScore_s &= \sum_{m=1}^M \omega_m (v_{s,m} - \trueScore_s) 

>     &= \sum_{m=1}^M \omega_m (\biasVec_m + \varepsilon_{s,m}) 

>     &= \underbrace{\sum_{m=1}^M \omega_m \biasVec_m}_{systematic bias} + \underbrace{\sum_{m=1}^M \omega_m \varepsilon_{s,m}}_{random error}.
> $$
> 
> 
> By A2 (conditional independence of errors), the variance of the random error term is:
> 
> $$
>     \Var\left(\sum_{m=1}^M \omega_m \varepsilon_{s,m}\right) = \sum_{m=1}^M \omega_m^2 \sigma_m^2.
> $$
> 
> 
> Minimizing this variance subject to $\sum_m \omega_m = 1$ via Lagrange multipliers yields $\omega_m \propto 1/\sigma_m^2$, giving:
> 
> $$
>     \Var_{random} = \frac{1}{\sum_{m=1}^M 1/\sigma_m^2}.
> $$
> 
> 
> The total MSE decomposes as variance plus squared bias:
> 
> $$
>     \MSE(\hat_{Yajie}) = \frac{1}{\sum_{m=1}^M 1/\sigma_m^2} + \left(\sum_{m=1}^M \omega_m \biasVec_m\right)^2.
> $$
> 
> 
> When $\biasVec_m = 0$ for all $m$ and $\sigma_m^2 = \sigma^2$ for all $m$ (homogeneous graders), $\MSE = \sigma^2/M$, yielding $O(1/\sqrt{M})$ convergence. With inter-grader correlation $\bar$, the effective sample size is $M_{eff} = M/(1 + \bar)$, giving $O(1/\sqrt{M_{eff}})$ convergence.  $\square$

> **Corollary:** [Rubric Design as Variance Reduction 评分标准设计即方差缩减]
> <!-- label: cor:rubric_variance -->
> A rubric $\rubric$ reduces inter-grader variance $\sigma_m^2$ by providing explicit scoring anchors. The rubric's effectiveness is:
> 
> $$
>     \eta_ = 1 - \frac{\sigma^2_{with rubric}}{\sigma^2_{without rubric}}.
> $$
> 
> A rubric with $\eta_ = 0.5$ halves inter-grader variance, equivalent to doubling the effective number of graders without increasing $M$.

> **Corollary:** [Score Confidence Interval 分数置信区间]
> <!-- label: cor:score_ci -->
> Under normally-distributed grader errors, the $(1-\alpha)$ confidence interval for $\trueScore_s$ is:
> 
> $$
>     \hat_{Yajie}(s) \pm z_{\alpha/2} \cdot \sqrt{\frac{1}{\sum_{m=1}^M 1/\hat_m^2} + \widehat^2},
> $$
> 
> where $\widehat = \sum_m \omega_m \biasVec_m$ is estimated from historical grading data in Spring{} memory. A score report should display this interval, not a point estimate.

## Theorem 3: Grade Inflation Detection 定理3：分数膨胀检测
<!-- label: sec:theorem3 -->

Grade inflation is the systematic upward drift of scores over time without corresponding improvement in measured competence. It is a canonical example of SCX{} systematic bias — a structural error that no single grader can detect (Theorem~2) but that multi-grader temporal audit makes visible.

> **Definition:** [Grade Inflation Rate 分数膨胀率]
> <!-- label: def:inflation -->
> For cohorts $t = 1, 2, ..., T$, let $\bar{v}_t = \frac{1}{|\studentSet_t|}\sum_{s \in \studentSet_t} v_s$ be the cohort-averaged score. The grade inflation rate from cohort $t-1$ to $t$ is:
> 
> $$
>     \inflationRate_t = \frac{\bar{v}_t - \bar{v}_{t-1}}{\bar{v}_{t-1}}.
> $$
> 
> Inflation is present when $\inflationRate_t > 0$ but the latent competence distribution is stationary: $\cP_t = \cP_{t-1}$.

> **Theorem:** [Grade Inflation Detection 分数膨胀检测]
> <!-- label: thm:inflation -->
> Let cohorts $t-1$ and $t$ be scored by disjoint grader pools $\cG_{t-1}$ and $\cG_t$, each of size $M$, with A1--A5. Define the inter-cohort score drift:
> 
> $$
>     D_t = \bar{v}_t - \bar{v}_{t-1} = \frac{1}{|\studentSet_t|}\sum_{s \in \studentSet_t} v_s - \frac{1}{|\studentSet_{t-1}|}\sum_{s' \in \studentSet_{t-1}} v_{s'}.
> $$
> 
> Under the null hypothesis of no inflation ($\cP_t = \cP_{t-1}$ and no grader bias shift), $D_t$ has mean zero. The probability of failing to detect genuine inflation of magnitude $\inflationRate > 0$ is:
> 
> $$
>     \Pbb(miss inflation \mid \inflationRate) \le \exp\left(-\frac{2 M_{eff} \inflationRate^2 \cdot \bar{v}^2}{B^2}\right).
>     <!-- label: eq:inflation_detection -->
> $$

> **Proof:** Under A5 (stationary student distribution), the expected score for any student under unbiased grading is $\E[v_s] = \E_{\trueScore \sim \cP}[\trueScore] = \mu_\trueScore$. The observed cohort mean $\bar{v}_t$ estimates $\mu_\trueScore$ with two sources of variation: sampling variation across students and grader variation.
> 
> Decompose $\bar{v}_t$:
> 
> $$
>     \bar{v}_t = \underbrace{\frac{1}{|\studentSet_t|}\sum_{s} \trueScore_s}_{true mean  \hat_t} + \underbrace{\frac{1}{|\studentSet_t|}\sum_{s} \frac{1}{M}\sum_{m} (\biasVec_m^{(t)} + \varepsilon_{s,m}^{(t)})}_{grader contribution  \bar_t}.
> $$
> 
> 
> With $M$ graders per cohort, by Hoeffding, the grader contribution has variance $\le B^2/(4 M_{eff})$. For large $|\studentSet_t|$, student sampling variance $\to 0$, and $D_t$ is dominated by grader effects. The inflation signal $\inflationRate \cdot \bar{v}$ is detectable when it exceeds the grader noise floor $B/\sqrt{2 M_{eff}}$:
> 
> $$
>     \Pbb(miss) = \Pbb(|D_t| < \tau \mid \inflationRate) \le \exp\left(-\frac{2 M_{eff} (\inflationRate \cdot \bar{v} - \tau)^2}{B^2}\right) \le \exp\left(-\frac{2 M_{eff} \inflationRate^2 \bar{v}^2}{B^2}\right),
> $$
> 
> setting the detection threshold $\tau = 0$ for maximum sensitivity.  $\square$

> **Corollary:** [Inflation Requires External Audit 分数膨胀需要外部审计]
> <!-- label: cor:inflation_external -->
> If the same grader pool $\cG$ scores both cohorts $t-1$ and $t$, the inflation detection bound collapses: grader bias shifts $\Delta \biasVec_m = \biasVec_m^{(t)} - \biasVec_m^{(t-1)}$ are confounded with genuine competence shifts. This is the grade-inflation analog of Theorem~2 (self-audit = no audit): the institution that produced the scores cannot certify that scores haven't inflated. External, temporally-independent grader pools are required.

> **Remark:** [UK A-Level and US GPA Inflation 英国A-Level和美国GPA膨胀]
> The UK A-Level A/A* rate rose from 8.8\% (1982) to 44.8\% (2021), a compound annual inflation rate of approximately 4.0\%. The US college GPA rose from approximately 2.6 (1960s) to 3.15 (2010s), a compound annual inflation rate of approximately 0.4\%. Under Theorem [ref] with $B=100$, $\bar{v}=50$, $\inflationRate=0.04$, and $M_{eff}=5$ (typical for institution-level audit): $\Pbb(miss) \le \exp(-2 \cdot 5 \cdot 0.04^2 \cdot 2500 / 10000) = \exp(-0.04) \approx 0.96$. This means even $M=5$ independent graders would miss a single year's inflation with 96\% probability — but over 39 years (UK) or 50 years (US), the cumulative detection probability approaches 1. The data are clear in hindsight; the framework shows why they were invisible year-by-year.

## Theorem 4: Blind Grading = A1 Enforcement 定理4：盲审即A1强制
<!-- label: sec:theorem4 -->

Blind grading — the practice of concealing student identity from graders and preventing inter-grader communication — is standard in high-stakes assessment. Our framework reveals *why* it matters mathematically: blindness enforces Assumption A1 (independent expert training) by reducing inter-grader correlation.

> **Definition:** [Blindness Index 盲审指数]
> <!-- label: def:blindness -->
> The blindness index $\beta \in [0,1]$ measures the degree to which student identity and inter-grader influence are suppressed:
> 
- $\beta = 0$: fully non-blind. Graders know student identity and can communicate.
- $\beta = 1$: fully blind. Student identity is perfectly concealed; graders are isolated.

> In practice, $\beta$ is estimated as the reduction in inter-grader correlation attributable to blinding procedures.

> **Theorem:** [Blindness Increases Effective Multiplicity 盲审提高有效多重性]
> <!-- label: thm:blind -->
> Under blindness level $\beta$, the effective multiplicity of $M$ graders is:
> 
> $$
>     M_{eff}(\beta) = \frac{M}{1 + \bar_{grader} \cdot (1 - \beta)},
>     <!-- label: eq:Meff_beta -->
> $$
> 
> where $\bar_{grader}$ is the inter-grader error correlation under $\beta = 0$. Blindness increases detection probability by factor:
> 
> $$
>     \frac{\Pbb_(detect)}{\Pbb_{0}(detect)} \approx \exp\left(2 M \Delta^2 \cdot \frac{\bar_{grader} \cdot \beta}{(1 + \bar_{grader})(1 + \bar_{grader}(1-\beta))}\right) > 1.
>     <!-- label: eq:blindness_gain -->
> $$

> **Proof:** Under non-blind conditions ($\beta=0$), graders may be influenced by:
> 
1. **Student identity effects 学生身份效应**: Knowing a student's past performance, demographic characteristics, or perceived ability biases scoring. This creates correlation because multiple graders observe the same identity signal.
2. **Inter-grader influence 评卷人间影响**: Graders who discuss scores or observe each other's ratings converge — reducing effective independence.
3. **Institutional pressure 制度压力**: Graders in the same institution share norms about ``appropriate'' score distributions.

> These effects contribute to $\bar_{grader}$. Blinding reduces each: identity effects are eliminated (up to redaction quality $\varepsilon_{redact}$), inter-grader influence is blocked by isolation protocols, and institutional pressure is weakened when graders don't know whose work they're scoring.
> 
> Let $\bar_{grader}(\beta) = \bar_{grader}(0) \cdot (1 - \beta)$ be the residual correlation under blindness $\beta$. Then:
> 
> $$
>     M_{eff}(\beta) = \frac{M}{1 + \bar_{grader}(0) \cdot (1 - \beta)}.
> $$
> 
> 
> The detection probability ratio follows from substituting $M_{eff}(\beta)$ into Theorem [ref]:
> 
> $$
>     \frac{\Pbb_(detect)}{\Pbb_{0}(detect)}
>     &= \frac{1 - \exp(-2 M_{eff}(\beta) \Delta^2 / B^2)}{1 - \exp(-2 M_{eff}(0) \Delta^2 / B^2)} 

>     &\approx \exp\left(2 M \Delta^2 \left[\frac{1}{1 + \bar(1-\beta)} - \frac{1}{1 + \bar}\right] / B^2\right) 

>     &= \exp\left(2 M \Delta^2 \cdot \frac{\bar\beta}{(1+\bar)(1+\bar(1-\beta))} / B^2\right).
> $$
> 
> Since $\bar, \beta \ge 0$, the exponent is non-negative, so the ratio $\ge 1$.  $\square$

> **Corollary:** [Blindness Multiplier 盲审乘数]
> <!-- label: cor:blindness_multiplier -->
> For $M=3$, $\bar=0.5$, complete blindness ($\beta=1$) transforms effective multiplicity from $M_{eff}(0) = 3/1.5 = 2.0$ to $M_{eff}(1) = 3/1.0 = 3.0$ — a 50\% increase. The detection probability for $\Delta/B = 0.1$ (10\% of scoring range) improves from $1 - e^{-0.04} \approx 3.9\%$ to $1 - e^{-0.06} \approx 5.8\%$ — a 49\% relative improvement. For $M=10$: from $M_{eff}=6.67$ to $M_{eff}=10$ (50\% increase), detection probability from $1 - e^{-0.133} \approx 12.5\%$ to $1 - e^{-0.20} \approx 18.1\%$.

> **Remark:** [Blindness in Oral Examinations 口试中的盲审]
> For oral examinations (PhD defenses, language proficiency interviews, medical OSCEs), perfect blindness ($\beta=1$) is impossible — the student's identity is visible. However, partial blindness is achievable: multiple examiners can be drawn from different institutions, with no prior knowledge of the student. In this case, $\beta$ reflects the fraction of identity-correlated information unavailable to graders, and $M_{eff}$ is correspondingly reduced. This explains why doctoral defenses typically use external examiners: to maximize $\beta$ given the inherent limitations of the format.

## Theorem 5: AI-Human Grading = Multi-Modal Audit 定理5：AI与人类评分即多模态审计
<!-- label: sec:theorem5 -->

AI grading systems — from classical AES (e-rater, Intellimetric) to LLM-based graders (GPT-4, Claude) — introduce a new grader modality with distinct error characteristics. The interaction between AI and human graders creates a multi-modal audit structure: two expert types with different training, different biases, and different failure modes.

> **Definition:** [Multi-Modal Grader Set 多模态评卷人集合]
> <!-- label: def:multimodal -->
> A multi-modal grader set consists of $M_H$ human graders $\cG_H = \{g_1^H, ..., g_{M_H}^H\}$ and $M_A$ AI graders $\cG_A = \{g_1^A, ..., g_{M_A}^A\}$. Human graders have error distribution $\cD_H(0, \sigma_H^2)$ with bias $\biasVec_H$; AI graders have error distribution $\cD_A(0, \sigma_A^2)$ with bias $\biasVec_A$. The two modalities are conditionally independent given $\trueScore_s$: $\Cov(\varepsilon_H, \varepsilon_A \mid \trueScore_s) = 0$.

> **Theorem:** [AI-Human Disagreement Decomposition AI与人类分歧分解]
> <!-- label: thm:multimodal -->
> The disagreement between AI and human consensus scores decomposes as:
> 
> $$
>     \E[(\hat_{AI} - \hat_{human})^2] = \underbrace{(\biasVec_A - \biasVec_H)^2}_{bias difference} + \underbrace{\frac{\sigma_A^2}{M_A} + \frac{\sigma_H^2}{M_H}}_{variance terms}.
>     <!-- label: eq:ai_human_decomp -->
> $$
> 
> The probability that AI and human graders disagree by more than $\tau$ while the true score lies between their estimates is bounded by:
> 
> $$
>     \Pbb(|\hat_{AI} - \hat_{human}| > \tau \mid \trueScore_s \in [\hat_{AI}, \hat_{human}]) \le \exp\left(-\frac{\tau^2}{2(\sigma_A^2/M_A + \sigma_H^2/M_H)}\right).
>     <!-- label: eq:disagreement_bound -->
> $$

> **Proof:** The AI and human consensus scores are:
> 
> $$
>     \hat_{AI} = \frac{1}{M_A}\sum_{m=1}^{M_A} v_{s,m}^A, \quad \hat_{human} = \frac{1}{M_H}\sum_{m=1}^{M_H} v_{s,m}^H.
> $$
> 
> 
> By the scoring production function (equation for $v_{s,m}$):
> 
> $$
>     \hat_{AI} - \hat_{human} &= (\trueScore_s + \biasVec_A + \bar_A) - (\trueScore_s + \biasVec_H + \bar_H) 

>     &= (\biasVec_A - \biasVec_H) + (\bar_A - \bar_H),
> $$
> 
> where $\bar_A = \frac{1}{M_A}\sum_m \varepsilon_{s,m}^A$ with variance $\sigma_A^2/M_A$, and similarly for humans.
> 
> Taking expectation of the squared difference:
> 
> $$
>     \E[(\hat_{AI} - \hat_{human})^2] = (\biasVec_A - \biasVec_H)^2 + \frac{\sigma_A^2}{M_A} + \frac{\sigma_H^2}{M_H},
> $$
> 
> since $\E[\bar_A] = \E[\bar_H] = 0$ and $\Cov(\bar_A, \bar_H) = 0$ by conditional independence.
> 
> For the tail bound: when $\biasVec_A = \biasVec_H$ (unbiased graders), the disagreement is $\bar_A - \bar_H \sim N(0, \sigma_A^2/M_A + \sigma_H^2/M_H)$ (asymptotically normal by CLT). By the Gaussian tail bound:
> 
> $$
>     \Pbb(|\bar_A - \bar_H| > \tau) \le 2\exp\left(-\frac{\tau^2}{2(\sigma_A^2/M_A + \sigma_H^2/M_H)}\right).
> $$
> 
> Conditioning on $\trueScore_s$ lying between the estimates removes the factor of 2 (one tail is impossible), yielding the bound.  $\square$

> **Corollary:** [AI Bias Detection AI偏差检测]
> <!-- label: cor:ai_bias -->
> AI grading bias $\biasVec_A$ is detectable through systematic deviation from human consensus:
> 
> $$
>     \hat_A = \frac{1}{|\studentSet|}\sum_{s \in \studentSet} (\hat_{AI}(s) - \hat_{human}(s)).
> $$
> 
> By the Central Limit Theorem, $\hat_A \sim N(\biasVec_A - \biasVec_H, (\sigma_A^2/M_A + \sigma_H^2/M_H)/|\studentSet|)$. Testing $H_0: \biasVec_A = \biasVec_H$ requires $|\studentSet| \ge z_{\alpha/2}^2 (\sigma_A^2/M_A + \sigma_H^2/M_H) / \delta^2$ for power $1-\beta$ at effect size $\delta$.

> **Corollary:** [Optimal AI-Human Grader Allocation 最优AI与人类评卷人分配]
> <!-- label: cor:optimal_allocation -->
> Given a budget $C$ with human grader cost $c_H$ and AI grader cost $c_A \ll c_H$, the variance-minimizing allocation solves:
> 
> $$
>     \min_{M_H, M_A} \frac{\sigma_H^2}{M_H} + \frac{\sigma_A^2}{M_A} \quad s.t. \quad c_H M_H + c_A M_A \le C.
> $$
> 
> The optimal ratio is:
> 
> $$
>     \frac{M_A^*}{M_H^*} = \frac{\sigma_A}{\sigma_H} \sqrt{\frac{c_H}{c_A}}.
> $$
> 
> When AI is 100$\times$ cheaper ($c_H/c_A = 100$) but 2$\times$ noisier ($\sigma_A/\sigma_H = 2$), the optimal ratio is $M_A^*/M_H^* = 2 \cdot 10 = 20$: deploy 20 AI graders per human grader.

> **Remark:** [The AI Auditor Paradox AI审计员悖论]
> AI grading is simultaneously (a) the cheapest way to achieve high $M$ (reducing $\sigma^2/M$ through multiplicity) and (b) the modality most vulnerable to undetected systematic bias (because all AI instances share the same training distribution, creating hidden correlation $\bar_{AI}$). The solution is not to avoid AI grading but to treat AI as one modality in a multi-modal panel that includes human graders. Theorem [ref] provides the mathematical basis: human graders detect AI bias, while AI graders provide the multiplicity needed for Theorem [ref]'s error detection bound.

## The Cercis Score for Assessment Systems 评估系统的Cercis评分
<!-- label: sec:cercis -->

> **Definition:** [Cercis Score for Assessment 评估系统的Cercis评分]
> <!-- label: def:cercis_edu -->
> For an assessment system $\cA$, the Cercis{} Score is:
> 
> $$
>     Cercis(\cA) = Q(\cA) + \eta \cdot N(\cA),
> $$
> 
> where:
> 
- $Q(\cA) \in [0,1]$ is the **Quality Guarantee 质量保证**: the fraction of SCX{} theorems the system structurally satisfies:
- $q_1 \in [0,1]$: degree to which Theorem~1 (multi-grader detection) is satisfied. $q_1 = 1$ when $M \ge M_$ as defined in equation~( [ref]).
- $q_2 \in [0,1]$: degree to which Theorem~2 (self-audit prohibition) is satisfied. $q_2 = 1$ when no grader evaluates their own prior scores; $q_2 = 0$ when the system self-certifies.
- $q_3 \in [0,1]$: degree to which Theorem~3 (noise-signal unidentifiability) is addressed. $q_3 = 1$ when rubric dimension contributions are independently auditable.
- $q_4 \in [0,1]$: degree to which \Situs{}-1 (encoding quality) is satisfied. $q_4 = 1$ when the rubric has bounded Lipschitz constant and measurable reconstruction error.
- $q_5 \in [0,1]$: degree to which Spring{}-1 (permanent memory) is satisfied. $q_5 = 1$ when all scores, grader identities, and rubrics are permanently stored.

>     \item $N(\cA) \in [0,1]$ is the **Empirical Novelty 经验评分可靠性**: normalized scoring reliability metrics (inter-rater reliability, test-retest stability, predictive validity).
>     \item $\eta = 0.2$ is the **epistemic discount factor 认知折扣因子**: empirical reliability without formal certification is worth at most 20\%.
> \end{itemize}
> *Critical:* If $Q(\cA) = 0$, then $Cercis(\cA) \le 0.20$ regardless of empirical reliability. A system with 0.95 inter-rater reliability and zero quality guarantee is epistemically equivalent to random grading with a lucky rubric.

[Table omitted — see original .tex]

The Cercis{} Score exposes a systematic pattern: current assessment systems cluster in the $0.08$--$0.56$ range, far below the certification threshold of $0.70$. Even the Gaokao's double-grading with arbitration — among the most sophisticated operational systems — achieves only $Cercis = 0.56$. The gap between current practice and SCX{}-compliant assessment ($Cercis = 1.00$) is the education audit gap quantified.

## Experimental Protocols 实验方案
<!-- label: sec:protocols -->

### Protocol 1: Gaokao Essay Scoring Audit 高考作文评分审计

**Setting.** Gaokao Chinese essay (作文, 60 points). $N = 10,000$ essays sampled from a provincial examination cohort. Standard protocol: $M=2$ human raters, third rater if $|v_1 - v_2| > 6$.

**SCX Enhancement.**

1. **Grader pool expansion 评卷人池扩展.** Recruit $M = 20$ independent graders from different provinces, trained on disjoint calibration sets (A1 enforcement).
2. **Full blindness 完全盲审.** Redact all student identifiers (name, school, region) and randomize essay order per grader (A1 enforcement, $\beta \to 1$).
3. **AI grader addition AI评卷人加入.** Deploy $M_A = 5$ AI graders (GPT-4, Claude, Qwen, ERNIE, Gemini) with distinct prompts and temperature settings.
4. **Yajie{} consensus computation Yajie{}共识计算.** Compute $\hat_{Yajie}(s)$ with inverse-variance weights estimated from calibration essays.
5. **Spring{} permanent record Spring{}永久记录.** Store: essay text hash, all $M_H + M_A$ scores, grader identities, rubric version, timestamp, and $\hat_{Yajie}(s)$ with 95\% CI.
6. **Inflation monitoring 膨胀监控.** Compare $\hat_{Yajie}$ across years; flag when $\inflationRate_t > 0$ with $p < 0.05$.

**Expected Outcomes.**

- Detection probability for $\Delta = 6$ (10\% of 60): $\Pbb(detect) \ge 1 - \exp(-2 \cdot 20 \cdot 0.01 / (1+0.3)) \approx 1 - e^{-0.308} \approx 26.5\%$, versus $\approx 3.9\%$ for $M=2$.
- AI-human bias estimate $\hat_A$ with 95\% CI width $\le 3$ points for $N=10,000$.
- Cercis{} Score improvement from $0.56$ (current) to $\approx 0.85$.

### Protocol 2: SAT Essay Scoring Audit SAT作文评分审计

**Setting.** SAT Essay (discontinued 2021, but illustrative). Scoring: Reading, Analysis, Writing dimensions, each 2--8 points. Two human raters per dimension.

**SCX Enhancement.**

1. **Multi-modal panel 多模态评卷组.** $M_H = 5$ human raters + $M_A = 10$ AI raters across 3 rubric dimensions $\times$ 2 modalities = 30 scores per essay.
2. **Dimension-specific Yajie{} consensus 分维度Yajie共识.** Compute $\hat_{Yajie}^{(k)}(s)$ per dimension $k$, then aggregate via rubric-weighted sum.
3. **Bias decomposition 偏差分解.** Decompose total grader bias into dimension-specific components: $\biasVec_m = (\biasVec_m^{(1)}, \biasVec_m^{(2)}, \biasVec_m^{(3)})$.
4. **Spring{} gating for rubric drift Spring{}评分标准漂移门控.** Detect when grader score distributions shift, indicating rubric interpretation drift or inflation.

### Protocol 3: AI-Assisted Classroom Grading AI辅助课堂评分

**Setting.** University course with $N=200$ students, 4 essay assignments. Instructor grades all essays (traditional $M=1$).

**SCX Enhancement.**

1. **AI pre-grading AI预评分.** Deploy $M_A = 5$ AI graders on all essays ($5 \times 200 \times 4 = 4000$ scores at near-zero marginal cost).
2. **Human spot-check 人工抽查.** Instructor grades a random sample of $n = 40$ essays (10\%). This provides calibration for $\biasVec_A$ estimation.
3. **Disagreement flagging 分歧标记.** Essays where $|\hat_{AI} - \hat_{human}| > 2\sigma_{disagree}$ are flagged for additional human review.
4. **Cercis{} Score reporting Cercis{}评分报告.** Each student receives $\hat_{Yajie}$ with 95\% CI, grader composition, and overall $Cercis(\cA)$ for the course.

**Cost-Benefit.** Human grading cost: $200 \times 4 \times 15min = 200$ hours. SCX cost: $40 \times 4 \times 15min = 40$ hours + AI API costs ($\sim$\$50). Net savings: 160 hours (80\%), with formal certification.

## Discussion 讨论
<!-- label: sec:discussion -->

### The Cost of Certification 认证的成本

The primary objection to multi-grader SCX audit is cost: $M$ graders cost $M$ times as much as one. We address this at three levels:

1. **AI reduces marginal cost AI降低边际成本.** AI graders cost $\sim$\$0.01--\$0.10 per essay versus $\sim$\$5--\$20 for human graders (at $\sim$\$20--\$80/hour, 4 essays/hour). The optimal AI:human ratio from Corollary [ref] shows that even modest AI deployment ($M_A = 10$--$50$) dramatically increases $M_{eff}$ at minimal cost.
2. **Not all assessments need full certification 并非所有评估都需要完全认证.** Formative classroom assessment may accept $Cercis \approx 0.3$--$0.5$; high-stakes examinations require $Cercis \ge 0.8$. The Cercis{} Score enables cost-graded certification: higher stakes $\to$ higher required $Cercis$ $\to$ higher $M$.
3. **The cost of *not* certifying 不认证的成本.** A single erroneous Gaokao score can alter a student's university trajectory, with estimated lifetime earnings impact of \$50,000--\$200,000. At 12M essays/year with $M=2$ and $\Pbb(miss  \Delta=10\%) \approx 97.4\%$, the expected number of undetected significant errors is large. The certification cost ($M=10$ graders $\times$ \$50/essay = \$500/essay incremental) must be weighed against the cost of errors.

### Irreducible Inter-Grader Correlation 不可消除的评卷人相关性

A2 (conditional independence) is an idealization. In practice, graders share:

- **The same rubric $\rubric$**: even with independent training, the rubric constrains all graders toward the same score regions. This is desirable (it reduces variance) but creates irreducible correlation.
- **The same cultural context 相同文化背景**: graders from similar educational backgrounds share implicit scoring norms not captured by the rubric.
- **The same language 相同语言**: for essay scoring, linguistic patterns that one grader finds sophisticated, another also finds sophisticated.

The framework accommodates this through $M_{eff} = M/(1 + \bar)$. The irreducible correlation $\bar_$ is an empirical quantity that must be estimated for each assessment context. The Cercis{} Score should report $\bar_$ alongside $M_{eff}$.

### Rubric Incommensurability 评分标准不可通约性

Theorem [ref] assumes a common rubric $\rubric$ shared by all graders. But what if graders use *different* rubrics? Consider:

- **Holistic vs. analytic 整体评分 vs. 分析评分.** Grader A uses a holistic 1--6 scale; Grader B uses analytic scoring across 5 dimensions. Their scores are incommensurable — they cannot be averaged.
- **Criterion disagreement 标准分歧.** Grader A values ``creativity''; Grader B values ``grammatical accuracy.'' Their scores reflect different latent constructs.

SCX{} addresses this through \Situs{} encoding: each grader's rubric $\rubric_m$ defines a distinct encoding $\phi_m: \cW \to [0, B_m]$. The Yajie{} consensus operates not on raw scores but on the *rankings* induced by each rubric: $\hat_{Yajie} = median_m(rank_m(w_s))$. This preserves the consensus property while accommodating rubric heterogeneity. The cost is reduced interpretability — a consensus rank is less informative than a consensus score.

### The Political Economy of Grade Inflation 分数膨胀的政治经济学

Theorem [ref] proves that grade inflation is detectable with temporally-independent grader pools. But detection is not correction. Grade inflation persists because institutions benefit from it:

- **Student satisfaction 学生满意度.** Higher grades increase student satisfaction and reduce complaints.
- **Competitive positioning 竞争定位.** Institutions with higher average grades appear more successful.
- **Graduate outcomes 毕业生出路.** Higher grades improve graduate school and employment prospects, creating alumni goodwill.

SCX{} does not solve the political economy problem — it solves the detection problem. Once inflation is detected and publicly certified (via Spring{} permanent records), the political choice to tolerate or correct it becomes explicit rather than hidden. This is the governance analog: audit creates transparency; transparency enables accountability; accountability is a political choice.

### Limitations 局限性

We declare the following honest limitations:

1. **Latent score unobservability 潜分数不可观测性.** The true score $\trueScore_s$ is a latent construct. All theorems are stated in terms of $\trueScore_s$, but $\trueScore_s$ is never directly observed. The framework certifies *consensus* — agreement among graders — not *truth*. Consensus is a necessary condition for truth (disagreement implies at least one grader is wrong) but not sufficient (all graders could share the same bias).
2. **AI grader correlation AI评卷人相关性.** AI graders from different providers (GPT-4, Claude, Gemini) may have correlated errors because they are trained on overlapping internet text corpora. The independence assumption A2 for AI graders requires empirical validation. If $\bar_{AI} \approx 0.3$--$0.5$, then deploying $M_A=50$ AI graders is equivalent to $M_{eff} \approx 33$--$38$, not 50.
3. **Rubric quality is exogenous 评分标准质量是外生的.** The framework certifies scoring *given* a rubric, not the rubric itself. A poor rubric ($\varepsilon_\rubric$ large, $L_\rubric$ large) can produce perfectly certified worthless scores. Rubric validation — demonstrating that rubric scores predict external outcomes — is outside the scope of SCX{} audit.
4. **Cost remains a barrier 成本仍是障碍.** While AI reduces marginal cost, human graders are still required for bias calibration (Theorem [ref]). The minimum viable $M_H$ is likely 3--5, which may be prohibitive for resource-constrained settings.
5. **Temporal grader drift 评卷人时间漂移.** Individual graders' biases $\biasVec_m(t)$ may drift over time (fatigue, experience, rubric re-interpretation). Spring{} memory enables detection of this drift, but correction requires re-calibration, which may lag behind the drift.
6. **Cultural specificity 文化特殊性.** The rubric consensus in Theorem [ref] assumes graders share a common understanding of quality. In cross-cultural assessment (e.g., PISA, TOEFL), graders from different cultures may apply incompatible quality standards. SCX{} detects the resulting disagreement but cannot resolve it — resolution requires substantive consensus on what quality means, which is a normative question.

## Conclusion 结论
<!-- label: sec:conclusion -->

Educational assessment is the world's largest measurement enterprise, and it operates without formal certification. Scores are claims about student competence; graders are experts making those claims. The SCX{} auditing framework, applied to this domain, reveals that:

\begin{enumerate}[label=(\roman*)]
    \item **Single-grader scoring is epistemically equivalent to no scoring** ($M=1 \Rightarrow Q=0$). A teacher, examiner, or AI that scores alone cannot certify the score's accuracy. This is not a criticism of grader competence — it is a mathematical consequence of Theorem~2 (self-audit = no audit).
    \item **Current ``best practices'' (Gaokao double-grading, SAT two-rater) provide negligible error detection** ($\Pbb(detect  \Delta=10\%) \le 3\%$--$5\%$). Two correlated graders are not meaningfully better than one.
    \item **AI grading is not a threat — it is the enabling technology for affordable multi-grader audit.** AI graders can provide $M_A = 50$--$100$ at near-zero marginal cost, while $M_H = 3$--$5$ human graders provide bias calibration. The hybrid model achieves $Cercis > 0.85$ at lower total cost than current $M=2$ human-only systems.
    \item **Grade inflation is mathematically detectable** but requires temporally-independent grader pools and Spring{} permanent records. The framework transforms inflation from an anecdotal concern into a testable hypothesis with explicit detection bounds.
    \item **The Cercis{} Score provides a single-number summary** of assessment system certification quality, enabling comparison across systems, institutions, and countries. Any assessment system can compute and publish its Cercis{} Score — and should be asked to.

The bottom line: **every score is a claim. Every claim needs an auditor. In education, the auditors are other graders. The more independent graders agree, the more the score can be trusted.** This is not a pedagogical opinion — it is a mathematical theorem.

**结论.**
教育评估是世界上最大的测量事业，但它没有正式认证。分数是关于学生能力的声明；评卷人是做出这些声明的专家。SCX{}审计框架应用于此领域，揭示出：(1)单评卷人评分在认识论上等同于没有评分；(2)当前“最佳实践”（高考双评、SAT两评）提供的误差检测几乎为零；(3)AI评分不是威胁——它是实现可负担多评卷人审计的使能技术；(4)分数膨胀在数学上是可检测的，但需要时间上独立的评卷人池和Spring{}永久记录；(5)Cercis{}评分提供了评估系统认证质量的单一数字总结。归根结底：每个分数都是一个声明。每个声明都需要审计员。在教育中，审计员就是其他评卷人。独立评卷人同意得越多，分数就越可信。这不是教学观点——这是数学定理。

\begin{thebibliography}{99}

\bibitem{AttaliBurstein2006}
Y.~Attali and J.~Burstein.
\newblock Automated essay scoring with e-rater v.2.
\newblock {\em Journal of Technology, Learning, and Assessment}, 4(3), 2006.

\bibitem{Brennan2001}
R.~L.~Brennan.
\newblock {\em Generalizability Theory}.
\newblock Springer, 2001.

\bibitem{Haertel2006}
E.~H.~Haertel.
\newblock Reliability.
\newblock In {\em Educational Measurement} (4th ed.), pages 65--110. ACE/Praeger, 2006.

\bibitem{Johnson2003}
V.~E.~Johnson.
\newblock {\em Grade Inflation: A Crisis in College Education}.
\newblock Springer, 2003.

\bibitem{MeadowsBillington2005}
M.~Meadows and L.~Billington.
\newblock A review of the literature on marking reliability.
\newblock {\em AQA Research Report}, 2005.

\bibitem{RojstaczerHealy2012}
S.~Rojstaczer and C.~Healy.
\newblock Where A is ordinary: The evolution of American college and university grading, 1940--2009.
\newblock {\em Teachers College Record}, 114(7):1--23, 2012.

\bibitem{ShermisBurstein2013}
M.~D.~Shermis and J.~Burstein (eds.).
\newblock {\em Handbook of Automated Essay Evaluation}.
\newblock Routledge, 2013.

\bibitem{William2011}
D.~William.
\newblock {\em Embedded Formative Assessment}.
\newblock Solution Tree Press, 2011.

\bibitem{Sadler2009}
D.~R.~Sadler.
\newblock Indeterminacy in the use of preset criteria for assessment and grading.
\newblock {\em Assessment \& Evaluation in Higher Education}, 34(2):159--179, 2009.

\bibitem{Bloxham2009}
S.~Bloxham.
\newblock Marking and moderation in the UK: false assumptions and wasted resources.
\newblock {\em Assessment \& Evaluation in Higher Education}, 34(2):209--220, 2009.

\bibitem{Page2003}
E.~B.~Page.
\newblock Project Essay Grade: PEG.
\newblock In {\em Automated Essay Scoring: A Cross-Disciplinary Perspective}, pages 43--54. Lawrence Erlbaum, 2003.

\bibitem{Dikli2006}
S.~Dikli.
\newblock An overview of automated scoring of essays.
\newblock {\em Journal of Technology, Learning, and Assessment}, 5(1), 2006.

\bibitem{Perelman2014}
L.~Perelman.
\newblock When the state of the art is counting words.
\newblock {\em Assessing Writing}, 21:104--111, 2014.

\bibitem{Bridgeman2012}
B.~Bridgeman, C.~Trapani, and Y.~Attali.
\newblock Comparison of human and machine scoring of essays.
\newblock {\em ETS Research Report}, RR-12-06, 2012.

\bibitem{Davey2015}
T.~Davey, S.~Ferrara, P.~Holland, E.~Shavelson, N.~Webb, and L.~Wise.
\newblock Psychometric considerations for the next generation of performance assessment.
\newblock {\em ETS Research Report}, 2015.

\bibitem{SCX2025}
SCX.
\newblock The SCX framework: A complete audit of machine learning.
\newblock Technical report, 2025.

\bibitem{Kane2006}
M.~T.~Kane.
\newblock Validation.
\newblock In {\em Educational Measurement} (4th ed.), pages 17--64. ACE/Praeger, 2006.

\bibitem{Messick1989}
S.~Messick.
\newblock Validity.
\newblock In {\em Educational Measurement} (3rd ed.), pages 13--103. Macmillan, 1989.

\bibitem{NewtonShaw2014}
P.~E.~Newton and S.~D.~Shaw.
\newblock {\em Validity in Educational and Psychological Assessment}.
\newblock SAGE, 2014.

\bibitem{Wiliam2010}
D.~Wiliam.
\newblock What counts as evidence of educational achievement?
\newblock {\em Educational Assessment}, 15(3-4):143--162, 2010.

\bibitem{BlackWiliam1998}
P.~Black and D.~Wiliam.
\newblock Assessment and classroom learning.
\newblock {\em Assessment in Education}, 5(1):7--74, 1998.

\bibitem{Brookhart2013}
S.~M.~Brookhart.
\newblock {\em How to Create and Use Rubrics for Formative Assessment and Grading}.
\newblock ASCD, 2013.

\bibitem{Andrade2005}
H.~G.~Andrade.
\newblock Teaching with rubrics: The good, the bad, and the ugly.
\newblock {\em College Teaching}, 53(1):27--31, 2005.

\bibitem{JonssonSvingby2007}
A.~Jonsson and G.~Svingby.
\newblock The use of scoring rubrics: Reliability, validity and educational consequences.
\newblock {\em Educational Research Review}, 2(2):130--144, 2007.

\bibitem{SutoNadas2009}
I.~Suto and R.~Nadas.
\newblock The cognitive demands of examination syllabuses and associated assessment arrangements.
\newblock {\em Cambridge Assessment Research Report}, 2009.

\end{thebibliography}