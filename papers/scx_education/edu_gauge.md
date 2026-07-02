# Introduction: Education as a Potential Surface

**Author:** SCX

*Abstract:*

**中文摘要.**
评分制度创造了一个教育势能面 $\cS_{edu}(x)$：每个学生通过分数获得一个势能位置。势能梯度 $\gradS$ 是学习动机的数学表达——学生沿梯度上行、追求更高分数。然而，当评分产生的势能台阶过大时，梯度退化为**悬崖**（cliff）：底部的学生永远无法看到攀登路径，顶部的学生被锁定为**势能奇点**（Thm~10--11）。马太效应（Thm~12）使高势能学生获得更高的势能增长率，将平滑梯度变为不可逆的阶梯函数——每一级台阶都是一个延迟引爆的不稳定界面。本文在平等论框架（$\sumgd$）下构建教育势能面的形式化几何，提出三个核心定理：(1)~梯度必要性定理——$|\gradS|>0$ 是学习动机存在的必要条件；(2)~悬崖定理——当相邻势能台阶 $\Delta_k$ 超过临界值 $\Delta_{crit}$ 时，跨台阶的学习迁移在数学上不可行；(3)~态度对齐定理——教师与学生的规范姿态 $\mathbf{g}_T, \mathbf{g}_S$ 必须满足 $\mathbf{g}_T + \sum_{i} \mathbf{g}_{S_i}/N = \mathbf{0}$，否则评分比较失去合法性。我们分析排名系统、标准化考试、分轨/分流制作为教育势能面管理的不同策略，并给出保留动机梯度同时避免悬崖的操作准则。

**English Abstract.**
Grading systems construct an educational potential surface $\cS_{edu}(x)$: each student receives a potential position via scores. The potential gradient $\gradS$ is the mathematical expression of learning motivation — students climb the gradient toward higher scores. However, when grade-induced potential steps become too large, the gradient degenerates into **cliffs**: students at the bottom can never see a climbing path, and students at the top become locked as **potential singularities** (Thm~10--11). The Matthew Effect (Thm~12) grants higher-potential students higher growth rates, transforming smooth gradients into irreversible staircase functions — each step a time-delayed detonation interface. We formalize the geometry of educational potential surfaces within the Equality Principle framework ($\sumgd$), establishing three core theorems: (1)~Gradient Necessity — $|\gradS|>0$ is necessary for learning motivation; (2)~Cliff Theorem — when adjacent potential steps $\Delta_k$ exceed a critical threshold $\Delta_{crit}$, cross-step learning transfer becomes mathematically infeasible; (3)~Attitude Alignment — the gauge postures of teacher and students must satisfy $\mathbf{g}_T + \sum_i \mathbf{g}_{S_i}/N = \mathbf{0}$ for grading comparisons to possess legitimacy. We analyze ranking systems, standardized testing, and tracking/streaming as strategies for managing the educational potential surface, deriving operational principles for preserving motivational gradients while avoiding cliffs.

## Introduction: Education as a Potential Surface

### The Central Tension

Education systems face a paradox embedded in their very structure. Consider any classroom at the start of a term:

- The teacher enters with a **gauge** — a set of reference points, expectations, and implicit norms that define what counts as ``good work,'' ``correct thinking,'' or ``progress.''
- Each student enters with their own **gauge** — shaped by prior schooling, family background, cognitive style, and accumulated confidence or its absence.
- The grading system superimposes a single coordinate system over this plurality, assigning each student a scalar position: a grade.

This superimposition is not neutral. It creates a **potential surface** $\cS_{edu}(x)$ on which every student occupies a point. The gradient $\gradS(x)$ at a student's position drives their behavior: they move toward higher potential. This is the **motivational function** of grading — arguably the reason grading exists at all.

But the same mechanism that creates motivation also creates **cliffs**. When the gap between a high-scoring student and a low-scoring student exceeds a critical threshold, the student at the bottom cannot perceive a continuous path upward. The gradient, from their perspective, is not a gentle slope — it is a vertical wall. At this point, motivation inverts: the student stops climbing and starts defending. Or drops out. Or attacks.

This paper formalizes this tension within the SCX Equality Principle (*平等论*) framework [cite]. We model education as a potential surface geometry problem, where the core question is:

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**How to preserve $\gradS$ — the motivational gradient — without creating cliffs (悬崖) where students can never catch up?**
\end{minipage}%
}

</div>

### The SCX Equality Principle in Brief

The SCX framework establishes a chain of epistemic conditions for legitimate knowledge production [cite]. At its foundation lies the Equality Principle:

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**The Equality Principle (平等论)**

Different observers within the same system, even when trained on identical objectives to identical loss, develop incommensurable internal representations.

Consistency is not natural — it must be explicitly constructed. The mathematical legitimacy of comparison is not a default — it must be conferred by gauge fixing.

$\boxed{\sum_m \mathbf{g}_m = \mathbf{0}}$
\end{minipage}%
}

</div>

The gauge condition $\sumgd$ states that no subsystem's coordinate system is the privileged origin. When applied to education, this yields a precise mathematical constraint: the teacher's grading framework and the students' self-assessment frameworks must jointly satisfy gauge invariance. A teacher who unilaterally declares their rubric as the ``standard'' coordinate system — i.e., sets $\mathbf{g}_T = \mathbf{0}$ implicitly — violates the gauge condition and renders all subsequent grade comparisons mathematically ill-posed.

### Why Education Needs This Framework

Existing educational theories speak of ``growth mindset'' [cite], ``zone of proximal development'' [cite], and ``achievement gap'' [cite] — all grasping at the same underlying geometry but lacking a unified mathematical language. The growth mindset is a strategy for gradient perception. The zone of proximal development is a constraint on admissible step sizes. The achievement gap is a potential step that has hardened into a cliff.

The SCX potential surface geometry provides this unified language. It does not replace these theories — it subsumes them, revealing their common mathematical structure and, crucially, their common failure modes.

### Key Theorems from SCX Referenced in This Work

We rely on four theorems from the SCX corpus, adapted to the education domain:

1. **Cross-Domain Preservation (Thm~7).** When a partition (classification, rubric) optimized on one distribution is applied to another, information loss is bounded by the Wasserstein distance between distributions [cite]. In education: a grading rubric optimized on one cohort loses predictive power when applied to a demographically different cohort — unless gauge-fixed at the interface.
2. **Confinement Instability (Thm~10).** Blocking movement across a potential jump creates pressure accumulation proportional to the jump magnitude; the system inevitably destabilizes on time scale $O(1/\Delta)$ [cite]. In education: tracking/streaming that locks students into low tracks creates cumulative motivational pressure that manifests as dropout, disengagement, or behavioral crisis.
3. **Singularity Attack (Thm~11).** A potential singularity — a subregion with potential exceeding its surroundings by $>\delta_{crit}$ — attracts attention and attack with probability approaching 1 as group size or $\delta$ increases [cite]. In education: consistently top-ranked students constitute potential singularities; the social dynamics of ``nerd-bashing,'' ``tall poppy syndrome,'' and gifted-student isolation are structural inevitabilities, not moral failures.
4. **Matthew Effect / Staircase Mines (Thm~12).** When potential growth rate is proportional to current potential ($\partial\mathcal{S}/\partial t \propto \mathcal{S}$), the surface evolves into a staircase function; each step is a delayed-detonation interface with characteristic explosion time $T_k \propto 1/\Delta_k^2$ [cite]. In education: cumulative advantage in grading systems creates irreversible stratification; each cohort-level gap is a future crisis.

### Structure of This Paper

Section~2 defines the educational potential surface and its gradient. Section~3 proves the Gradient Necessity Theorem and the Cliff Theorem. Section~4 analyzes ranking, standardized testing, and tracking through the potential surface lens. Section~5 treats the role of attitude ($\mathbf{g}$) in teacher-student gauge alignment. Section~6 derives operational principles for gradient preservation without cliff creation. Section~7 provides concluding remarks.

## The Educational Potential Surface: Formal Definitions
<!-- label: sec:framework -->

### Student State Space

Let $\mathcal{X}$ be the **student state space** — a measurable space whose points $x \in \mathcal{X}$ represent complete descriptions of a student's cognitive, affective, and behavioral state. In practice, $\mathcal{X}$ is unobservable in full dimensionality; we observe projections through assessments, observations, and student work.

> **Definition:** [Educational Potential Surface, **教育势能面**]
> <!-- label: def:edu_potential -->
> The **educational potential surface** is a function
> 
> $$
>     \cS_{edu}: \mathcal{X} \to \R,
> $$
> 
> mapping each student state to a scalar potential. The value $\cS_{edu}(x)$ aggregates:
> 
1. **Assessed achievement** (分数, grades, test scores) — the direct observable;
2. **Teacher perceived competence** (教师感知能力) — transmitted through feedback valence, attention allocation, and implicit expectations;
3. **Peer-relative standing** (同伴相对位置) — rank within reference group;
4. **Institutional labels** (制度标签) — track placement, honors status, remedial classification.

\edunote{Unlike physical potential defined by energy, $\cS_{edu}$ is a *socially constructed* potential — it exists because the system's participants agree (or are compelled to agree) that certain positions are ``higher'' than others. This is precisely what makes it a **gauge-dependent** quantity.}

> **Definition:** [Educational Potential Gradient, **教育势能梯度**]
> <!-- label: def:edu_gradient -->
> At a student state $x$, the **educational potential gradient** is
> 
> $$
>     \gradS(x) = \left(\frac{\partial \cS_{edu}}{\partial x_1}, ..., \frac{\partial \cS_{edu}}{\partial x_d}\right)(x),
> $$
> 
> where $d = \dim(\mathcal{X})$. The gradient direction indicates which changes in student state produce the largest increase in assessed potential. The magnitude $|\gradS(x)|$ measures **motivational intensity**: how strongly the system rewards movement in the ``right'' direction.

> **Definition:** [Potential Step, **势能台阶**]
> <!-- label: def:potential_step -->
> Let $\Omega_k$ and $\Omega_{k+1}$ be two adjacent regions in the educational potential surface, corresponding to adjacent grade bands (e.g., C to B, B to A) or adjacent tracks (e.g., remedial to standard). The **potential step** between them is
> 
> $$
>     \Delta_k = \min_{x \in \Omega_{k+1}} \cS_{edu}(x) - \max_{x \in \Omega_k} \cS_{edu}(x).
> $$
> 
> If $\Delta_k \leq 0$, the regions overlap — students can move continuously between them. If $\Delta_k > 0$, there exists a gap: no student state bridges the two bands.

> **Definition:** [Cliff, **悬崖**]
> <!-- label: def:cliff -->
> A potential step $\Delta_k$ is called a **cliff** if
> 
> $$
>     \Delta_k > \Delta_{crit} = \frac{\eta \cdot \tau},
> $$
> 
> where $\gamma$ is the minimum perceptible potential increment (the ``just noticeable difference'' in educational progress), $\eta$ is the student's learning rate (mobility), and $\tau$ is the available time window (e.g., one academic year). When $\Delta_k > \Delta_{crit}$, a student at the bottom of $\Omega_k$ cannot, within time $\tau$, accumulate enough increments to cross into $\Omega_{k+1}$ — even at maximum learning rate.

\edunote{A cliff is not the same as a challenge. A challenge ($0 < \Delta_k \leq \Delta_{crit}$) is surmountable within the time window — it is the ``desirable difficulty'' that learning science praises [cite]. A cliff ($\Delta_k > \Delta_{crit}$) is insurmountable within the given temporal constraint — it is a structural wall disguised as a standard.}

### The Gauge Structure of Grading

> **Definition:** [Grading Gauge, **评分规范**]
> <!-- label: def:grading_gauge -->
> A **grading gauge** is a triple $\cG = (\mathbf{b}, \sigma, \mathbf{w})$ where:
> 
- $\mathbf{b} \in \R$ is the **baseline shift** (零刻度偏移) — what score counts as ``zero'' or ``passing'';
- $\sigma > 0$ is the **scale factor** (尺度因子) — how wide a score difference counts as ``one grade step'';
- $\mathbf{w} \in \R^d$ is the **weight vector** (权重向量) — which dimensions of student state matter for the grade.

> Two grading systems $\cG_A$ and $\cG_B$ are **gauge-equivalent** if there exists an affine transformation mapping one to the other that preserves rank order. They are **gauge-inequivalent** if no such transformation exists — i.e., they measure incommensurable things.

The crucial insight from the SCX framework is that the choice of $\cG$ is a **gauge freedom**: many different $\cG$ produce identical rank orderings on a fixed dataset, yet they differ in their baseline shift $\mathbf{b}$ and scale $\sigma$. A teacher who grades ``on a curve'' is performing one gauge transformation; a teacher who grades against ``absolute standards'' is performing another. Neither is objectively correct — but the latter, by treating their own $\mathbf{b}$ as the natural zero, violates the gauge condition $\sumgd$.

> **Definition:** [Teacher and Student Gauge Postures, **师生规范姿态**]
> <!-- label: def:gauge_posture -->
> Let the teacher $T$ have **gauge posture** $\mathbf{g}_T \in \R^d$ representing the implicit coordinate origin of their grading framework. Let each student $S_i$ have gauge posture $\mathbf{g}_{S_i} \in \R^d$ representing their self-assessment coordinate origin. The **teacher-student gauge system** satisfies **attitude alignment** if
> 
> $$
>     \mathbf{g}_T + \frac{1}{N}\sum_{i=1}^{N} \mathbf{g}_{S_i} = \mathbf{0}.
>     <!-- label: eq:teacher_student_gauge -->
> $$
> 
> This is the education-specific instance of the SCX gauge condition $\sumgd$.

\edunote{Eq. [ref] means that the teacher's coordinate system is not the default origin. It requires that the teacher's framing is offset by the average of students' framings — precisely $\mathbf{g}_T = -\bar{\mathbf{g}}_S$. A teacher who says ``my rubric is the objective standard'' is setting $\mathbf{g}_T = \mathbf{0}$ while $\bar{\mathbf{g}}_S \neq \mathbf{0}$, violating the condition.}

## Core Theorems: Gradient, Cliff, and Alignment
<!-- label: sec:theorems -->

### Theorem 1: Gradient Necessity (梯度必要性定理)

> **Theorem:** [Gradient Necessity for Learning Motivation]
> <!-- label: thm:gradient_necessity -->
> Let $\cS_{edu}(x)$ be the educational potential surface over student state space $\mathcal{X}$. For a student with learning dynamics
> 
> $$
>     \frac{dx}{dt} = \eta(x) \cdot \gradS(x) + \xi(t),
> $$
> 
> where $\eta(x) > 0$ is the state-dependent learning rate and $\xi(t)$ is zero-mean stochastic exploration noise, the following hold:
> 
> 
1. **Motivation existence.** If $|\gradS(x)| = 0$ for all $x$ in a connected region $\Omega$, then within $\Omega$, the student's expected state drift is zero: $\E[dx/dt] = 0$. The student has no directional signal — motivation is absent.
2. **Gradient lower bound.** For motivated learning to be possible, there must exist at least one path $\gamma \subset \mathcal{X}$ along which $|\gradS| \geq \varepsilon_{min} > 0$, where $\varepsilon_{min}$ is the minimum perceptible gradient.
3. **Rate bound.** The expected time for a student to traverse from state $x_0$ to a target region $\Omega_{target}$ is bounded below by

> **Proof:** (i) The learning dynamics are a gradient-ascent stochastic differential equation. The expected drift is $\E[dx/dt] = \eta(x) \gradS(x)$ since $\E[\xi(t)] = 0$. If $\gradS \equiv 0$ on $\Omega$, then $\E[dx/dt] = 0$ everywhere in $\Omega$. By the martingale property of driftless diffusion, the student's expected position is constant — no systematic progress occurs.
> 
> (ii) If $|\gradS| < \varepsilon_{min}$ along all paths, then the signal-to-noise ratio $SNR = |\gradS|^2 / \E[|\xi|^2] < \varepsilon_{min}^2 / \sigma_\xi^2$. Below a critical SNR threshold (established by standard detection theory [cite]), the student cannot distinguish signal from noise — gradient-following behavior degenerates into random walk.
> 
> (iii) Along any path $\gamma$ from $x_0$ to $\Omega_{target}$, the student's speed is bounded by $\eta \cdot |\gradS| \leq \eta_ \cdot \max |\gradS|$. The time to traverse path length $L(\gamma)$ is at least $L(\gamma) / (\eta_ \cdot \max |\gradS|)$. Taking the infimum over all paths and the supremum of the denominator yields the bound. In the worst case — minimum gradient along the best path — we obtain the stated inequality.\qed

> **诚实暴击:** Theorem [ref] is nearly tautological: it says students need to see that effort leads to progress. Its value is not in novelty but in precision — it quantifies *how much* gradient is needed ($\varepsilon_{min}$) and how long it takes to climb given a gradient. Most educational systems fail to compute either number.}

**教育含义 (Educational Implication).**
Grading is not optional. A classroom without differential feedback — where all work receives identical evaluation — produces $|\gradS| \approx 0$ and extinguishes directional motivation. This is why ``everyone gets a trophy'' pedagogies fail: they flatten the potential surface, removing the gradient that drives learning. The question is never *whether* to grade, but *how steep* to make the gradient.

### Theorem 2: The Cliff Theorem (悬崖定理)

> **Theorem:** [Cliff Impassability]
> <!-- label: thm:cliff -->
> Consider two adjacent grade bands $\Omega_k$ and $\Omega_{k+1}$ with potential step $\Delta_k > 0$ as defined in Def. [ref]. Let student $i$ have maximum sustainable learning rate $\eta_i^$ and available time window $\tau$ (e.g., one semester). If
> 
> $$
>     \Delta_k > \eta_i^ \cdot \tau,
>     <!-- label: eq:cliff_condition -->
> $$
> 
> then:
> 
> 
1. **Ascent impossibility.** The probability that student $i$ crosses from $\Omega_k$ to $\Omega_{k+1}$ within time $\tau$ is zero under deterministic dynamics, and exponentially small under stochastic dynamics:
2. **Motivation inversion.** When condition [ref] holds and the student recognizes it (i.e., estimates $\hat_k$ and $\hat_i^$), the effective motivational force inverts:
3. **Cliff-propagation.** Students clustered below a cliff form a **confinement basin** (受限盆地). By Thm~10 (Confinement Instability), pressure accumulates at rate proportional to $\Delta_k$, and the basin inevitably destabilizes on time scale $O(1/\Delta_k^2)$.

> **Proof:** (i) Under deterministic gradient ascent ($\xi = 0$), the student's state evolves as $x(t) = x(0) + \int_0^t \eta \gradS(x(s)) ds$. The maximum potential increase in time $\tau$ is $\Delta S_ = \eta_i^ \cdot \max_{s \in [0,\tau]} |\gradS| \cdot \tau \leq \eta_i^ \tau$ (since $|\gradS| \leq 1$ after normalization). If $\Delta_k > \eta_i^ \tau$, the student simply cannot accumulate enough potential to reach $\Omega_{k+1}$.
> 
> Under stochastic dynamics, the probability of reaching a target $\Delta_k$ away under gradient drift $\mu = \eta |\gradS|$ and diffusion $\sigma_\xi^2$ is bounded by the standard Gaussian tail bound for Brownian motion with drift: $\Pbb(reach) \leq \exp(-(\Delta_k - \mu\tau)^2 / (2\sigma_\xi^2 \tau))$, valid when $\Delta_k > \mu\tau$.
> 
> (ii) Motivation inversion follows from **learned helplessness** dynamics [cite] reformulated in potential surface terms. When a student repeatedly fails to cross $\Delta_k$ despite maximum effort, their internal model updates: the estimated gradient $\widehat$ develops a negative projection onto the actual gradient direction. The expected drift becomes $\E[dx/dt] = \eta \cdot \widehat \approx -\alpha \cdot \gradS$ — the student learns to move away from what they've learned they cannot reach.
> 
> (iii) The confinement basin argument follows directly from Thm~10 [cite]. Students in $\Omega_k$ experience a persistent gradient toward $\Omega_{k+1}$ but are structurally prevented from crossing. The boundary $\partial\Omega_k$ becomes a pressure accumulation interface. By the confinement instability theorem, the basin destabilizes with characteristic time $T_{crit} \propto 1/\Delta_k^2$.\qed

**教育含义.**
The cliff theorem formalizes why ``raising standards'' without infrastructure can be destructive. If the step from current performance to the new standard exceeds $\eta_i^ \tau$ for a significant fraction of students, the policy does not motivate — it creates a cliff. Students at the cliff base invert their motivational vector: they stop trying to climb and start trying to exit the system.

> **诚实暴击:** The cliff theorem is pessimistic: it identifies a structural condition under which no amount of ``grit'' or ``growth mindset'' intervention can help — the step is simply too large for the available time and learning rate. This does not mean students at the bottom cannot learn. It means the *institutional step size* must be reduced, or the time window extended, or the learning rate amplified through instructional intervention.}

### Theorem 3: Attitude Alignment and Grading Legitimacy (态度对齐与评分合法性)

> **Theorem:** [Teacher-Student Gauge Alignment]
> <!-- label: thm:attitude_alignment -->
> Let teacher $T$ impose grading gauge $\cG_T = (\mathbf{b}_T, \sigma_T, \mathbf{w}_T)$ and let students $\{S_i\}_{i=1}^N$ have self-assessment gauges $\cG_{S_i} = (\mathbf{b}_{S_i}, \sigma_{S_i}, \mathbf{w}_{S_i})$. Define the **gauge mismatch** between teacher and student $i$ as
> 
> $$
>     \delta_i = \norm{\mathbf{g}_T - \mathbf{g}_{S_i}},
> $$
> 
> where $\mathbf{g} = (\mathbf{b}, \log\sigma, \mathbf{w})$ is the vectorized gauge parameter. Then:
> 
> 
1. **Comparison legitimacy.** The operation of comparing two students' grades, $\cS_{edu}(x_i) > \cS_{edu}(x_j)$, is **gauge-legitimate** only if the gauge mismatch between teacher and both students satisfies
2. **Feedback effectiveness.** The information $I(improvement; feedback)$ conveyed by teacher feedback to student $i$ decays with gauge mismatch:
3. **Alignment condition.** Maximum feedback effectiveness and comparison legitimacy are achieved when

> **Proof:** (i) The grade $\cS_{edu}(x_i)$ is a function of both the student's true state $x_i$ and the gauge $\cG_T$ through which it is observed: $\cS_{edu}(x_i) = f_{\cG_T}(x_i)$. If $\delta_i > \delta_{crit}$, the mapping $f_{\cG_T}$ differs from the student's self-mapping $f_{\cG_{S_i}}$ by more than a gauge transformation — they are genuinely incommensurable. Comparing $f_{\cG_T}(x_i)$ with $f_{\cG_T}(x_j)$ is valid only when both $x_i$ and $x_j$ are measured in the same gauge. But the student's internal state $x_i$ is accessible to the teacher only through observations mediated by the student's own gauge $\cG_{S_i}$. When $\delta_i$ is large, the teacher *does not know* what the student's grade means to the student — the comparison lacks a shared referent.
> 
> (ii) The mutual information bound follows from the data processing inequality applied to the gauge-mismatched channel. Teacher feedback $F$ is a function of observed student work $W$, which is a function of true state $x$: $F = \phi_T(W(x))$. The student's interpretation $\hat{F} = \phi_{S_i}^{-1}(F)$ passes through the inverse of their own gauge. The effective channel $x \to \hat{F}$ has capacity degraded by the gauge mismatch. Under Gaussian assumptions on gauge parameters, the exponential decay follows from the Shannon-Hartley theorem with SNR inversely proportional to $\delta_i^2$.
> 
> (iii) The condition $\mathbf{g}_T + \bar{\mathbf{g}}_S = \mathbf{0}$ is the unique gauge-fixing that minimizes the sum of squared mismatches $\sum_i \delta_i^2$ subject to the constraint that no participant is privileged as the origin. It is precisely the education-domain instance of the SCX gauge condition $\sumgd$.\qed

\edunote{This theorem explains a familiar classroom phenomenon: why some students ``just don't get'' a particular teacher's feedback, even when the teacher is objectively skilled. The feedback is transmitted in the teacher's gauge but interpreted in the student's gauge. If $\delta_i$ is large, the information is garbled — not by noise, but by a coordinate transformation the teacher never acknowledged.}

**教育含义.**
The attitude alignment theorem shifts the burden of communication from the student (``pay attention'') to the system (``align your coordinate systems''). A teacher who says ``my feedback is clear — the student just isn't trying'' may be correct about the clarity of their signal in their own gauge, while being mathematically wrong about its decodability in the student's gauge.

### Theorem 4: Matthew Effect in Education (教育马太效应阶梯)

> **Theorem:** [Educational Matthew Effect Staircasing]
> <!-- label: thm:edu_matthew -->
> Let the educational potential surface evolve over cohort time $t$ (measured in academic years) under the dynamics
> 
> $$
>     \frac{\partial \cS_{edu}(x,t)}{\partial t} = \beta \cdot \cS_{edu}(x,t) + \nu(x,t),
>     <!-- label: eq:matthew_dynamics -->
> $$
> 
> where $\beta > 0$ is the **cumulative advantage coefficient** and $\nu(x,t)$ is a mean-zero perturbation (new learning, random variation). This dynamics captures that higher-graded students receive more teacher attention, more challenging assignments, higher peer expectations, and greater self-efficacy — all of which accelerate further potential gain. Then:
> 
> 
1. **Staircase convergence.** In the long-time limit, for any initial condition with non-zero variance:
2. **Step amplification.** The gap between adjacent strata amplifies exponentially:
3. **Critical time to cliff.** For an initial step $\Delta_k(0)$, the time until it exceeds the cliff threshold $\Delta_{crit}$ is
4. **System survival.** By Thm~12, each stratum boundary becomes a delayed-detonation interface. The system's survival probability over time horizon $T$ decays as

> **Proof:** (i) Eq. [ref] is a multiplicative growth process with additive noise. By the law of large numbers for multiplicative random walks, the distribution of $\cS_{edu}$ across the student population converges to a log-normal distribution whose variance grows exponentially in time. Discretization into strata occurs when between-stratum variance exceeds within-stratum variance by a factor that grows with $\beta t$.
> 
> (ii) From the dynamics, $\E[h_k(t)] = h_k(0) e^{\beta t}$. The gap $\Delta_k(t) = \E[h_{k+1}(t)] - \E[h_k(t)] = (h_{k+1}(0) - h_k(0)) e^{\beta t} = \Delta_k(0) e^{\beta t}$.
> 
> (iii) Setting $\Delta_k(t_{cliff}) = \Delta_{crit}$ and solving yields $t_{cliff} = (1/\beta) \ln(\Delta_{crit} / \Delta_k(0))$.
> 
> (iv) This follows directly from Theorem 12 of the SCX framework [cite] (台阶的埋雷性质), applied to the education domain. Each stratum boundary $\partial\Omega_k$ constitutes a potential jump interface. Under Thm~12, the probability that interface $k$ has not destabilized by time $T$ is at most $\exp(-T/T_k)$ with $T_k \propto 1/\Delta_k^2$.\qed

**教育含义.**
The Matthew Effect in education is not a moral failing — it is a **structural inevitability** of any grading system that allocates future learning opportunities based on past performance. The exponential amplification of initial differences means that even small early advantages (slightly better kindergarten preparation, slightly more parental involvement) compound into large later gaps. After $t_{cliff}$ years, the gap exceeds the cliff threshold, and cross-stratum mobility becomes mathematically impossible under the existing institutional structure.

> **诚实暴击:** The Matthew Effect theorem is the most uncomfortable result in this paper. It says that if you grade students and then give the higher-graded students more resources, you are not ``rewarding merit'' — you are manufacturing cliffs on an industrial scale. The system's own dynamics will produce irreversible stratification. This is not a criticism of teachers — it is a property of the feedback loop itself.}

## Educational Practices as Potential Surface Strategies
<!-- label: sec:practices -->

### Ranking Systems: The Flat Gradient with Fixed Cliffs

**排名系统 (Ranking Systems).** Consider a system that assigns each student an integer rank $r_i \in \{1, ..., N\}$ based on a scalar exam score. The potential surface is

$$
    \cS_{edu}(x_i) = N - r_i + 1,
$$

so the top-ranked student has $\cS = N$ and the bottom-ranked has $\cS = 1$.

> **Proposition:** [Ranking Gradient Properties]
> <!-- label: prop:ranking -->
> In a pure ranking system with $N$ students:
> 
1. The average gradient magnitude across the cohort is $|\overline| = 1$ — each rank step is one potential unit.
2. The step between any two adjacent ranks is exactly $\Delta = 1$, regardless of the underlying score differences.
3. **Artifact:** If student A and student B are separated by one rank but their underlying competence difference is negligible (e.g., scores of 89.4 vs. 89.2), the ranking still assigns $\Delta = 1$ — a **false cliff**. Conversely, if student C and student D are also one rank apart but their underlying difference is vast (95 vs. 65), the ranking still assigns $\Delta = 1$ — a **false bridge**.
4. The gauge condition $\sumgd$ is violated because the ranking origin ($\mathbf{b} = 0$ at rank $N$) is arbitrary — it privileges the bottom-ranked student as the zero-reference without their consent.

**教育含义.**
Ranking creates a **uniform gradient** that ignores the actual difficulty landscape. A student who improves from 60\% to 65\% expends far more learning effort than one who improves from 94\% to 95\%, yet ranking rewards both with the same $\Delta = 1$. This uniform gradient **manufactures cliffs** for struggling students (who need larger potential gain for their effort) while **manufacturing bridges** for high-performing students (who receive disproportionate rank movement for marginal improvement).

> **诚实暴击:** Ranking is the ``fairness'' that isn't. It treats all rank steps as equal when the underlying learning distances are radically unequal. It is geometrically equivalent to projecting a rugged mountain landscape onto a flat staircase — all the actual topography is erased, and students are told the staircase is the mountain.}

### Standardized Testing: Cross-Cohort Gauge Fixing

**标准化考试 (Standardized Testing).** Standardized tests attempt to fix a common gauge $\cG_{std}$ across all classrooms, schools, and regions. The test score provides a potential value:

$$
    \cS_{std}(x_i) = percentile(x_i \mid national cohort).
$$

> **Proposition:** [Standardized Testing as Gauge Fixing]
> <!-- label: prop:standardized -->
> Standardized testing performs a partial gauge-fixing operation:
> 
1. **Benefit:** It eliminates inter-teacher gauge drift. Without standardization, Teacher A's ``A'' and Teacher B's ``A'' may be incommensurable — exactly the problem identified by the SCX MoE gauge paper [cite].
2. **Cost:** It imposes a **single gauge origin** — the national norming sample — as the privileged coordinate system. This violates $\sumgd$ because the gauge is not symmetrically fixed: it is imposed top-down. The local classroom gauge ($\mathbf{g}_{class}$) and the standardized gauge ($\mathbf{g}_{std}$) may differ substantially, creating a gauge mismatch $\delta_{class} = \norm{\mathbf{g}_{class} - \mathbf{g}_{std}}$ that renders within-classroom comparisons under the standardized gauge ill-posed.
3. **Hidden cliff:** The percentile transformation maps the continuous score distribution onto a uniform distribution over $[0,100]$. This **flattens the gradient** in the dense middle of the distribution while **steepening cliffs** at the tails, where small score differences map to large percentile jumps.

**教育含义.**
Standardized testing solves one gauge problem (teacher-to-teacher incommensurability) while creating another (test-to-student incommensurability). A test normed on a national population may measure something fundamentally different from what a rural classroom values as ``learning.'' The gauge mismatch $\delta_{class}$ is largest precisely for the students the test is meant to help — those in non-dominant cultural, linguistic, or pedagogical contexts.

### Tracking / Streaming: Institutionalized Cliffs

**分轨/分流制 (Tracking / Streaming).** Tracking assigns students to different instructional tracks (e.g., remedial, standard, honors, gifted) based on prior performance. Formally, it partitions the student state space:

$$
    \mathcal{X} = \bigcup_{k=1}^{K} \Omega_k, \quad \Omega_k \cap \Omega_j = \emptyset \;\; (k \neq j),
$$

and assigns a distinct curriculum $\mathcal{C}_k$ to each track. Students in $\Omega_k$ are taught to a standard that prepares them for $\mathcal{C}_k$ — not for $\mathcal{C}_{k+1}$.

> **Theorem:** [Tracking as Cliff Institutionalization]
> <!-- label: thm:tracking -->
> Under tracking with $K$ tracks and non-overlapping curricula $\{\mathcal{C}_k\}$:
> 
1. **Cliff creation.** The potential step between track $k$ and track $k+1$ is at least
2. **Confinement.** Students in $\Omega_k$ are **confined**: the curriculum $\mathcal{C}_k$ does not teach the prerequisites for $\mathcal{C}_{k+1}$, so even if a student achieves mastery of $\mathcal{C}_k$, they cannot enter $\Omega_{k+1}$ without external intervention. By Thm~10 (confinement instability), this creates cumulative pressure with characteristic destabilization time $T_k \propto 1/(\Delta_k^{track})^2$.
3. **Irreversibility.** The probability that a student initially placed in $\Omega_k$ reaches $\Omega_{k+m}$ decays super-exponentially with $m$:

> **Proof:** (i) The curriculum distance $d_{\mathcal{C}}(x,y)$ measures the minimum learning steps needed to bridge the gap between the highest-achieving student in $\Omega_k$ and the lowest-achieving student in $\Omega_{k+1}$. Since $\mathcal{C}_k$ does not cover material prerequisite for $\mathcal{C}_{k+1}$, this distance is strictly positive and grows with tracking rigidity.
> 
> (ii) Confinement follows from the structural property that $\mathcal{C}_k$ does not provide the keys to $\Omega_{k+1}$. Students are locked in by curriculum design, not by ability. The pressure accumulation argument follows Thm~10 directly.
> 
> (iii) To ascend $m$ tracks, a student must cross $m$ independent potential steps. Each crossing event has probability bounded by the Gaussian tail $\exp(-\Delta_{k+j}^2 / 2\sigma^2)$. The product bound follows from the worst-case assumption of independence (in practice, correlations make it even harder, as failure at one step erodes the motivation to attempt the next).\qed

**教育含义.**
Tracking is cliff institutionalization. It takes the naturally occurring potential steps created by differential prior learning and **codifies them into the curriculum architecture**. Once codified, crossing tracks requires not just catching up on missed content, but learning an entirely *different* content sequence — a vastly larger $\Delta$ than the original grade gap.

> **诚实暴击:** Proponents of tracking argue it allows ``appropriate pacing'' for each ability level. In potential surface terms, this argument says: ``We've created an unclimbable wall between tracks, but within each track, the gradient is well-calibrated.'' The question is whether the within-track gradient optimization justifies the between-track cliff. Theorem [ref] says the answer depends entirely on $\Delta_k^{track}$: if it exceeds $\Delta_{crit}$, the tracking system is mathematically guaranteed to produce irreversible stratification — regardless of within-track quality.}

### Gauge Misalignment in Cross-Track Comparison

A subtler problem arises when the same test is administered across tracks. Suppose students in $\Omega_k$ (remedial) and $\Omega_{k+1}$ (standard) take the same standardized exam. The test is designed with gauge $\cG_{test}$. But:

- Students in $\Omega_k$ have been taught in gauge $\cG_k$ (remedial framing: ``basic skills, step-by-step'')
- Students in $\Omega_{k+1}$ have been taught in gauge $\cG_{k+1}$ (standard framing: ``conceptual understanding, independent problem-solving'')
- The test gauge $\cG_{test}$ is closer to $\cG_{k+1}$ (tests are typically written by standard-track teachers)

Thus, the gauge mismatch for remedial students is $\delta_{remedial} = \norm{\mathbf{g}_{test} - \mathbf{g}_k}$, which is systematically larger than $\delta_{standard} = \norm{\mathbf{g}_{test} - \mathbf{g}_{k+1}}$. The test does not measure ability difference alone — it measures **ability difference convolved with gauge mismatch**.

By Theorem [ref], the information conveyed by the test score about the student's true state is degraded by $\exp(-\delta^2 / 2\sigma_{\mathbf{g}}^2)$. The systematic gauge mismatch means that cross-track score comparisons are **not gauge-legitimate**: the scores belong to different coordinate systems, and comparing them is mathematically ill-posed.

## The Role of Attitude ($\mathbf{g$) in Teacher-Student Coordinate Alignment}
<!-- label: sec:attitude -->

### Attitude as Gauge Posture

In the SCX framework, $\mathbf{g}_m$ — the **gauge posture** or **attitude** — is not a personality trait. It is a **geometric parameter**: the offset of subsystem $m$'s coordinate origin from the symmetric gauge-fixed origin. When $\mathbf{g}_m = \mathbf{0}$ is assumed implicitly, subsystem $m$ has declared itself the standard — the reference frame against which all others are measured.

> **Definition:** [Teacher Attitude, **教师态度**]
> <!-- label: def:teacher_attitude -->
> A teacher's **attitude** $\mathbf{g}_T$ is the implicit coordinate origin of their pedagogical framework. It manifests in:
> 
- **Reference examples:** Which cultural references, analogies, and ``common sense'' the teacher assumes students share;
- **Error interpretation:** Whether a wrong answer is framed as ``careless mistake'' (high-expectation gauge) or ``lack of ability'' (low-expectation gauge);
- **Praise distribution:** Which achievements are celebrated as ``exceptional'' vs. which are treated as ``expected baseline'';
- **Question framing:** Whether questions are posed in abstract, decontextualized form (privileging students whose home culture practices decontextualized reasoning) or in situated, practical form.

> **Definition:** [Student Attitude, **学生态度**]
> <!-- label: def:student_attitude -->
> A student's **attitude** $\mathbf{g}_S$ is the implicit coordinate origin of their learning framework:
> 
- **Self-assessment anchor:** Where the student places ``adequate'' vs. ``excellent'' on their internal scale;
- **Attribution style:** Whether success is attributed to stable internal factors (``I'm good at this subject'') or unstable external factors (``the test was easy''), and whether failure is attributed to stable internal factors (``I'm bad at this subject'') or unstable controllable factors (``I didn't study enough'');
- **Goal orientation:** Whether the student's coordinate system is oriented toward mastery ($\mathbf{g}_S$ aligned with $\gradS$) or performance-avoidance ($\mathbf{g}_S$ orthogonal to $\gradS$).

### The Alignment Spectrum

Teacher-student gauge alignment is not binary — it exists on a spectrum:

1. **Complete alignment** ($\delta \approx 0$). Teacher and student share a coordinate system. The student understands what the teacher wants, why it matters, and how to get there. Feedback is received as intended. This is the ideal — but it is rare and cannot be assumed.
2. **Translatable misalignment** ($0 < \delta \leq \delta_{trans}$). The gauges differ, but the difference is systematic and can be corrected by an affine transformation. The teacher can ``translate'' their feedback into the student's gauge (``What I mean by *needs more analysis* is what you would call *explain why you think that*'') — but this requires the teacher to know the student's gauge.
3. **Incommensurable misalignment** ($\delta_{trans} < \delta < \delta_{crit}$). The gauges differ substantially. Translation is possible in principle but requires significant effort. Most cross-cultural, cross-class, and cross-linguistic teaching falls here.
4. **Cliff-level misalignment** ($\delta \geq \delta_{crit}$). The gauges are incommensurable. Communication is mathematically ill-posed. The teacher's feedback and the student's interpretation belong to different coordinate systems with no shared reference points.

\edunote{Alignment level 4 is more common than educational systems admit. A teacher from a high-SES, native-language, university-educated background teaching low-SES, second-language, first-generation students faces $\delta \gg \delta_{crit}$ — not because of malice or incompetence, but because their coordinate systems were constructed in non-overlapping worlds. The teacher is not ``failing to communicate'' — they are attempting an operation (comparison) that is not defined in the shared gauge space.}

### Attitude High as Structural Hazard

In the SCX framework, ``态度高'' (attitudinal elevation) refers to a subsystem's unilateral declaration of its own coordinate system as the standard origin:

$$
    \mathbf{g}_m = \mathbf{0} \quad (self-declared), \quad while \quad \sum_{k} \mathbf{g}_k \neq \mathbf{0}.
$$

In education, a teacher with attitude high:

- Assumes their cultural references are ``neutral'' rather than culturally specific;
- Frames students' failure to understand as a student deficit rather than a gauge mismatch;
- Treats their grading rubric as ``objective'' without acknowledging its gauge dependence;
- Believes students who succeed are ``naturally talented'' and students who fail are ``not trying hard enough'' — both attributions that ignore $\delta_i$.

> **Proposition:** [Attitude High Amplifies the Matthew Effect]
> <!-- label: prop:attitude_matthew -->
> When a teacher has attitude high ($\mathbf{g}_T \neq -\bar{\mathbf{g}}_S$), the effective cumulative advantage coefficient $\beta$ in Eq. [ref] is amplified:
> 
> $$
>     \beta_{eff} = \beta_0 \cdot (1 + \gamma \cdot \norm{\mathbf{g}_T + \bar{\mathbf{g}}_S}),
> $$
> 
> where $\beta_0$ is the baseline advantage rate and $\gamma > 0$ is the attitude amplification factor. A teacher whose gauge is systematically closer to high-performing students' gauges (because both share cultural and linguistic backgrounds) will, through no malicious intent, accelerate the Matthew Effect — shortening $t_{cliff}$ and deepening the resulting cliffs.

> **Proof:** The teacher allocates attention, encouragement, and challenging assignments based on their perception of student potential. When $\delta_i$ is small (teacher and student share a gauge), the teacher perceives the student's work as ``promising'' or ``insightful'' — the signal passes cleanly through the matched gauge. When $\delta_i$ is large, the same quality of work is perceived as ``confused'' or ``off-topic'' — the signal is garbled by the gauge mismatch. The differential allocation of learning opportunities based on perceived (not actual) quality creates a feedback loop: students whose gauge matches the teacher's receive more opportunities $\to$ learn more $\to$ appear even more promising $\to$ receive even more opportunities. The amplification factor $\gamma$ quantifies this loop's strength.\qed

**教育含义.**
The platitude ``teachers should have high expectations for all students'' is, in potential surface terms, a call for $\mathbf{g}_T$ to be configured such that all students are equidistant from the teacher's origin — i.e., the teacher's gauge is exactly the negative average of all student gauges: $\mathbf{g}_T = -\bar{\mathbf{g}}_S$. This is not a feel-good aspiration — it is the unique gauge configuration that minimizes the Matthew Effect amplification.

> **诚实暴击:** The practical difficulty is that $\bar{\mathbf{g}}_S$ is not directly observable. A teacher cannot survey their students' coordinate systems the way they can survey their prior test scores. The gauge posture $\mathbf{g}_S$ is implicit — students themselves may not know their own coordinate origin. This means attitude alignment cannot be achieved through measurement alone; it requires **interaction density** — enough time, enough contact, and enough varied scenarios that the teacher's gauge is empirically calibrated to the classroom's average gauge.}

### Attitude Convergence Through Interaction

The SCX framework provides a convergence result adapted from Theorem~3 (老实人定理): under repeated, honest, bidirectional interaction, gauge estimates converge.

> **Proposition:** [Attitude Convergence Through Classroom Interaction]
> <!-- label: prop:attitude_convergence -->
> Let teacher and students engage in $M$ distinct interaction episodes (lessons, assessments, conferences, informal conversations). In each episode $j$, both parties emit signals in their own gauges and attempt to decode the other's signals. Under the assumption of honest signaling (both parties genuinely attempt to communicate, not deceive), the teacher's estimate of the classroom average gauge $\hat{\bar{\mathbf{g}}}_S$ converges:
> 
> $$
>     \norm{\hat{\bar{\mathbf{g}}}_S^{(M)} - \bar{\mathbf{g}}_S} \leq \frac{\sigma_{\mathbf{g}}}{\sqrt{M}} \cdot \sqrt{2\log(2/\alpha)},
> $$
> 
> with probability at least $1 - \alpha$, where $\sigma_{\mathbf{g}}$ is the within-classroom gauge variance.
> 
> The required number of interaction episodes for the teacher's estimate to fall below a tolerance $\varepsilon$ is
> 
> $$
>     M^* \geq \frac{2\sigma_{\mathbf{g}}^2 \log(2/\alpha)}{\varepsilon^2}.
> $$

\edunote{This proposition is both encouraging and sobering. It says gauge alignment is achievable — but it takes time and density. A teacher who meets a class for 45 minutes, 3 times a week, for one semester has at most $M \approx 50-60$ formal interaction episodes. If $\sigma_{\mathbf{g}}$ is large (highly diverse classroom), $M^*$ may exceed this — meaning alignment cannot be achieved within the semester without changing the interaction structure (more episodes, or episodes designed to reduce $\sigma_{\mathbf{g}}$).}

## Preserving $\gradS$ Without Creating Cliffs: Operational Principles
<!-- label: sec:preserving -->

The central question of this paper — **how to preserve the motivational gradient while avoiding cliffs** — translates into the following mathematical program:

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}
**The Education Gauge-Fixing Program:**

$$
    Maximize \quad & \int_{\mathcal{X}} |\gradS(x)| \cdot \rho(x) \, dx \quad (total motivational gradient) 

    Subject to \quad & \max_{k} \Delta_k \leq \Delta_{crit} \quad (no cliffs) 

    & \sum_{m \in \{T, S_1, ..., S_N\}} \mathbf{g}_m = \mathbf{0} \quad (gauge condition) 

    & \mathbf{g}_T = -\frac{1}{N}\sum_{i=1}^N \mathbf{g}_{S_i} \quad (attitude alignment)
$$

\end{minipage}%
}

</div>

This section derives operational principles from the geometry of this optimization.

### Principle 1: Continuous Gradient with Bounded Steps (连续梯度，有界步长)

The potential surface $\cS_{edu}$ should be **Lipschitz continuous** with Lipschitz constant $L \leq \eta^ / \tau$, where $\eta^$ is the minimum learning rate in the student population and $\tau$ is the available time window:

$$
    |\cS_{edu}(x) - \cS_{edu}(y)| \leq \frac{\eta^} \cdot d_{\mathcal{X}}(x,y) \quad \forall x,y \in \mathcal{X}.
$$

**Operational translation:** Grade steps must be small enough that a student at any position can, within one grading period, accumulate enough improvement to reach the next level. This means:

- Grading rubrics with too few levels (e.g., pass/fail) create a single monolithic step that is a cliff for all but the students nearest the boundary.
- Grading rubrics with too many levels (e.g., 100-point scale with 1-point increments) may create *perceived* continuous gradients but *actual* cliffs if the real grade boundaries (A/B, B/C, etc.) are the only psychologically salient steps.
- The **optimal granularity** is one where $\Delta_k \approx \eta^{median} \cdot \tau$ for the median student — small enough to be surmountable, large enough to be perceptible.

### Principle 2: Gauge-Fixed Rubrics (规范固定的评分标准)

A rubric is a coordinate system. When unilaterally declared, it sets $\mathbf{g}_T = \mathbf{0}$ and violates the gauge condition. A gauge-fixed rubric requires:

1. **Explicit origin declaration.** The teacher states: ``This rubric is one possible coordinate system for evaluating this work. It is not the only one, and it is not the *correct* one. Here is why I chose it, and here is what it privileges.''
2. **Student gauges solicited.** Before grading, students articulate their own evaluation criteria. What would *they* count as excellent work? The teacher integrates these into the rubric — moving $\mathbf{g}_T$ toward $-\bar{\mathbf{g}}_S$.
3. **Post-hoc translation.** After grading, for each student whose $\delta_i$ is large (where the grade and the student's self-assessment diverge substantially), the teacher provides a ``gauge translation'': ``In my rubric, the score of X means [specific meaning in teacher's gauge]. In your self-assessment, this may correspond to [estimated meaning in student's gauge]. The gap between these is not a judgment of your ability — it is information about where our coordinate systems differ.''

> **诚实暴击:** This principle demands a level of metacognitive transparency that most educational systems are not structured to support. It requires teachers to admit that their rubrics are not ``objective'' — a concession that institutional evaluation systems (which evaluate teachers by their students' standardized scores) actively punish. The gauge condition cannot be satisfied by individual teachers acting alone; it requires institutional support.}

### Principle 3: Dynamic Regrouping with Controlled Step Size (动态重组的受控步长)

Tracking/streaming is the worst-case scenario — it creates institutionalized cliffs. The alternative is **dynamic regrouping**: students are regrouped frequently (every unit, every month) based on current performance, with the regrouping step size $\Delta_{regroup}$ deliberately kept below $\Delta_{crit}$.

> **Proposition:** [Dynamic Regrouping Stability]
> <!-- label: prop:dynamic_regrouping -->
> Under dynamic regrouping with regrouping period $\tau_{regroup}$ and maximum potential step $\Delta_{regroup}$:
> 
1. The probability that a student is permanently stuck in a low group decays exponentially with the number of regrouping cycles:
2. As $\tau_{regroup} \to 0$ (continuous regrouping), the system approximates a smooth potential surface with gradient $\gradS$ but no discrete steps — the ideal configuration.

**Operational translation:** ``Flexible grouping'' in elementary reading and mathematics — where groups change every 2-4 weeks based on current skill — is an empirical approximation of this principle. It works better than fixed-year tracking because $\tau_{regroup}$ is small enough to prevent any single $\Delta_k$ from exceeding $\Delta_{crit}$.

\edunote{The limit $\tau_{regroup} \to 0$ is approximated by **individualized instruction**: each student works at their own pace on their own sequence. In this limit, there are no groups, no tracks, no discrete steps — only a continuous gradient defined by the curriculum sequence. This is why Montessori, mastery-based, and competency-based systems outperform traditional age-cohort systems for heterogeneous populations: they eliminate the discrete step structure entirely.}

### Principle 4: Achievement Measured in Gain, Not Level (增量衡量，非水平衡量)

If the Matthew Effect arises from $\partial\cS/\partial t \propto \cS$, then the antidote is to define educational potential in terms of **gain** rather than **level**:

$$
    \cS_{gain}(x_i, t) = \cS_{edu}(x_i, t) - \cS_{edu}(x_i, t - \tau_{period}).
$$

Under gain-based potential, the dynamics become:

$$
    \frac{\partial \cS_{gain}}{\partial t} \propto \frac{\partial^2 \cS_{edu}}{\partial t^2},
$$

which does not exhibit the multiplicative instability of Eq. [ref]. A student starting at a low level who makes large gains outranks a student starting at a high level who makes small gains.

> **Proposition:** [Gain-Based Grading Eliminates Matthew Amplification]
> <!-- label: prop:gain_based -->
> Under gain-based potential $\cS_{gain}$, the cumulative advantage coefficient $\beta$ in the Matthew dynamics satisfies $\beta_{gain} = 0$. The potential surface does not spontaneously staircase — differences in level do not compound into differences in growth rate.

> **Proof:** In level-based potential, $\partial\cS/\partial t = \beta \cS + \nu$ implies $\cS(t) = \cS(0) e^{\beta t} + \int_0^t e^{\beta(t-s)} \nu(s) ds$. The exponential factor $e^{\beta t}$ amplifies initial differences $\cS(0)$. Under gain-based potential, $\cS_{gain}(t) = \cS(t) - \cS(t-\tau)$, and the dynamics $\partial\cS_{gain}/\partial t = \beta \cS_{gain} + \Delta\nu$ has no dependence on the absolute level $\cS(0)$ — only on recent gains. If $\cS_{gain}(0) = 0$ (by definition, gain starts at zero each period), the feedback loop is broken.\qed

**Operational translation:** Value-added models (VAM) in teacher evaluation are an application of this principle at the teacher level — measuring how much students grew, not where they ended. Applying VAM at the student level — grading students on their growth, not their absolute achievement — eliminates the Matthew Effect from the grading structure itself.

> **诚实暴击:** Gain-based grading has a known equity problem: students at the ceiling cannot demonstrate gain because there is no room above them. A student at 98\% cannot gain as much as a student at 50\%. This creates an **inverse cliff** at the top — ceiling effects that penalize high achievers. The solution is not to abandon gain-based grading but to extend the ceiling: unbounded assessment (e.g., open-ended projects, research extensions, enrichment beyond grade level) so that all students have room to grow.}

### Principle 5: Interface Smoothing Through Peer Teaching (同伴教学的界面平滑)

The most effective mechanism for smoothing potential interfaces is **peer interaction across step boundaries**. When students at adjacent levels interact — through peer tutoring, collaborative projects, or mixed-ability discussion groups — the interface $\partial\Omega_k$ becomes a zone of exchange rather than a wall.

> **Proposition:** [Peer Interaction Gradient Smoothing]
> <!-- label: prop:peer_smoothing -->
> Let students from adjacent strata $\Omega_k$ and $\Omega_{k+1}$ interact with frequency $f_{peer}$ and interaction depth $d_{peer}$. The effective potential step at the interface is reduced:
> 
> $$
>     \Delta_k^{eff} = \Delta_k \cdot \exp\left(-f_{peer} \cdot d_{peer} \cdot \tau\right),
> $$
> 
> where $\tau$ is the interaction time window. For sufficiently high $f_{peer} \cdot d_{peer}$, $\Delta_k^{eff}$ falls below $\Delta_{crit}$ even when the institutional step $\Delta_k$ exceeds it.

> **Proof:** Peer interaction creates **information channels** across the interface. Higher-stratum students transmit curricular knowledge, study strategies, and — crucially — **gauge information**: ``Here's how the teacher thinks. Here's what they actually want.'' Lower-stratum students update their internal models of $\cS_{edu}$ and the effective gradient $\gradS$. The exponential form follows from the information-theoretic model of gauge convergence (Prop. [ref]), where each peer interaction serves as one ``measurement'' of the higher stratum's gauge.\qed

**Operational translation:** Mixed-ability grouping is not a compromise between equity and excellence — it is a **stability operation**. By smoothing the potential interface, it reduces the pressure accumulation that leads to destabilization (Thm~10). Well-implemented peer tutoring programs produce learning gains for *both* tutor and tutee not despite their level difference, but *because* the level difference creates an information gradient that, when channeled through structured interaction, accelerates gauge alignment.

## System-Level Implications: Educational Policy as Gauge Engineering
<!-- label: sec:implications -->

### The National Potential Surface

At the national level, an education system's potential surface $\cS_{national}(x)$ aggregates all the sub-surfaces of classrooms, schools, districts, and states. The interfaces between these subsystems — school district boundaries, state lines, urban-rural divides — are potential interfaces where gauge misalignment accumulates.

> **Proposition:** [National Stratification Bound]
> <!-- label: prop:national_stratification -->
> For a national education system composed of $M$ subsystems (e.g., school districts), the total potential variance can be decomposed:
> 
> $$
>     \V[\cS_{national}] = \underbrace{\sum_{m=1}^{M} w_m \V[\cS_m]}_{within-subsystem variance} + \underbrace{\sum_{m=1}^{M} w_m (\bar_m - \bar_{national})^2}_{between-subsystem variance},
> $$
> 
> where $w_m$ is the proportion of students in subsystem $m$, and $\bar_m, \bar_{national}$ are subsystem and national means. The between-subsystem term measures **systemic cliffs**: the gaps between average outcomes in different subsystems that students cannot cross by individual effort alone.

When the between-subsystem variance dominates the within-subsystem variance — i.e., the system's inequality is primarily *between* schools/districts rather than *within* them — the potential surface is a staircase at the institutional level. Students in lower-strata districts face a cliff measured not in grade points but in life trajectories.

> **诚实暴击:** This decomposition reveals the mathematical structure of educational inequality: it is not about ``bad schools'' or ``bad teachers'' but about the **step function** between district A and district B. A student in district B who achieves the maximum possible within-district potential still cannot reach the average potential of district A — the step $\Delta_{AB}$ exceeds their $\eta^ \cdot \tau_{schooling}$. No amount of within-district improvement can fix this. The step itself must be reduced.}

### Policy Instruments as Gauge Operations

Different policy instruments correspond to different gauge operations:

[Table omitted — see original .tex]

### The Survival Constraint

The SCX Smooth Potential Surface Theorem [cite] provides a system-level survival constraint adapted to education:

> **Theorem:** [Education System Survival Bound]
> <!-- label: thm:edu_survival -->
> An education system with $K$ distinct potential strata (tracks, tiers, districts with non-overlapping outcome distributions) has survival probability bounded by:
> 
> $$
>     \Pbb(system stability \mid T) \leq \exp\left(-T \cdot \sum_{k=1}^{K-1} \kappa_k \cdot \Delta_k^2\right),
> $$
> 
> where $\Delta_k$ is the potential step at interface $k$, and $\kappa_k$ is the **interface permeability** — the rate at which students attempt to cross the interface. Higher steps and more permeable interfaces (more students aware of and desiring to cross) both accelerate destabilization.

**教育含义.**
This theorem says that educational inequality is not just normatively bad — it is **existentially unstable**. A system with large, visible gaps between its strata will experience cumulative pressure at every interface. ``Visible'' is key: $\kappa_k$ captures the **awareness factor**. When students in a low-strata school know exactly what resources, opportunities, and outcomes students in a high-strata school receive, $\kappa_k$ is large and $T_k = 1/(\kappa_k \Delta_k^2)$ is short — destabilization comes quickly. When the gaps are hidden — by geographical isolation, information segregation, or ideological narratives that justify the gaps — $\kappa_k$ is small, and the system can persist in metastable inequality for longer.

> **诚实暴击:** This implies a dark corollary: **information suppression is a stability strategy**. Systems that hide inequality survive longer than systems that expose it — not because they are more just, but because lower $\kappa$ extends $T_k$. The corollary is empirically testable: the introduction of school performance dashboards, publicized rankings, or transparency initiatives should *increase* short-term instability (by increasing $\kappa$) while *decreasing* long-term inequality (by forcing $\Delta$ reduction in response to instability). This is the ``transparency destabilizes, then equalizes'' hypothesis.}

## Discussion and Limitations
<!-- label: sec:discussion -->

### What This Framework Explains

The potential surface geometry framework provides unified explanations for several persistent educational puzzles:

1. **Why ``growth mindset'' interventions have heterogeneous effects.** Growth mindset is a strategy for improving gradient perception — it tells students that $\gradS$ exists and is climbable. But it cannot help when the actual institutional step $\Delta_k$ genuinely exceeds $\eta_i^ \cdot \tau$. Telling a student ``you can grow'' when the system has placed a cliff between them and the next level is not empowerment — it is gaslighting. The framework predicts that growth mindset interventions will be effective only when $\Delta_k \leq \Delta_{crit}$, and ineffective or counterproductive (motivation inversion) when $\Delta_k > \Delta_{crit}$.
2. **Why some excellent teachers fail in new contexts.** A teacher whose $\mathbf{g}_T$ is well-calibrated to one student population ($\mathbf{g}_T \approx -\bar{\mathbf{g}}_S^{(1)}$) may find their methods inexplicably failing with a different population ($\mathbf{g}_T \not\approx -\bar{\mathbf{g}}_S^{(2)}$). The teaching is not ``worse'' — the gauge alignment is broken. This explains the ``culture shock'' experienced by teachers moving between demographic contexts.
3. **Why tracking produces both excellence and despair.** Tracking optimizes within-track gradients (homogeneous groups allow well-calibrated pacing) while creating between-track cliffs (irreversible stratification). The framework quantifies this trade-off and predicts that the net welfare effect depends on whether within-track gradient gains outweigh between-track cliff costs.
4. **Why desegregation is both necessary and insufficient.** Desegregation increases interface contact ($f_{peer}$ in Prop. [ref]), which enables peer smoothing. But if the institutional step $\Delta_{AB}$ remains large — if within-school tracking recreates the segregation that between-school desegregation eliminated — the contact produces pressure without smoothing. Desegregation without detracking is geometrically incomplete: it brings students to the same interface without reducing the step.

### Limitations

This framework has significant limitations that must be acknowledged:

1. **The education potential operator is not yet formally defined.** As with the ``national potential operator'' $\cS_{nation}$ in the SCX framework, $\cS_{edu}$ is currently a **formalized conjecture** — its mathematical structure is specified, but its operational measurement awaits definition. How to aggregate grades, teacher perceptions, peer standing, and institutional labels into a scalar potential is a non-trivial measurement problem.
2. **The learning rate $\eta$ is heterogeneous and endogenous.** Students' learning rates depend on prior knowledge, motivation, instructional quality, and a host of unobservable factors. The assumption of a fixed $\eta_i^$ is a simplification.
3. **Gauge postures are unobservable.** $\mathbf{g}_T$ and $\mathbf{g}_{S_i}$ are theoretical constructs. Their empirical measurement would require metacognitive instruments that do not currently exist at scale. The attitude convergence bound (Prop. [ref]) assumes honest signaling — an assumption that may fail when students strategically present themselves or when teachers have incentives to appear aligned.
4. **The cliff threshold $\Delta_{crit}$ is contextual.** It depends on $\eta, \tau$, and the perceptibility parameter $\gamma$, all of which vary across students, subjects, and institutional contexts. The framework provides the structure for computing $\Delta_{crit}$ but not the parameter values.
5. **The framework is descriptive, not prescriptive at the operational level.** It says ``keep $\Delta_k \leq \Delta_{crit}$'' but does not provide a turnkey method for measuring $\Delta_k$ in a specific classroom on a Tuesday afternoon. The translation from geometric principle to classroom practice remains largely untheorized.

### Relation to Existing Theories

[Table omitted — see original .tex]

## Conclusion: The Geometry of Educational Justice
<!-- label: sec:conclusion -->

We have formalized education as a potential surface $\cS_{edu}$ generated by grading, ranking, tracking, and teacher-student interaction. Within the SCX Equality Principle framework ($\sumgd$), we have established:

1. **Gradient necessity.** A non-zero potential gradient $\gradS$ is mathematically necessary for directional motivation. Systems that eliminate grading eliminate the signal that drives learning.
2. **Cliff danger.** When institutional steps $\Delta_k$ exceed the student's maximum achievable gain $\eta_i^ \cdot \tau$, the system creates cliffs — insurmountable walls that invert motivation and trigger confinement instability (Thm~10).
3. **Matthew inevitability.** Under level-based grading with cumulative advantage ($\partial\cS/\partial t \propto \cS$), the potential surface inevitably staircases — creating increasingly steep interfaces that function as delayed-detonation bombs (Thm~12).
4. **Attitude alignment.** Teacher-student gauge alignment ($\mathbf{g}_T = -\bar{\mathbf{g}}_S$) is not a pedagogical nicety — it is the mathematical condition for legitimate comparison and effective feedback (Thm~3). Attitude high amplifies the Matthew Effect and accelerates cliff formation.
5. **Operational principles.** We derived five principles for preserving $\gradS$ without creating cliffs: (i) continuous gradient with bounded steps, (ii) gauge-fixed rubrics, (iii) dynamic regrouping, (iv) gain-based measurement, and (v) peer-mediated interface smoothing.

**The unifying intuition** is geometric: educational inequality is not fundamentally about resources, culture, or individual differences — it is about the **shape of the potential surface**. A system with large, discretized steps between its levels is a system with cliffs. A system with cliffs is a system with confined basins. A system with confined basins is a system accumulating pressure at every interface. A system accumulating pressure at every interface is a system whose survival time is bounded by $\exp(-T \sum \kappa_k \Delta_k^2)$.

**The conclusion is not moral but structural:** Smooth your potential surface — not because it is ``fair,'' but because staircase systems do not survive. The systems we see persisting in history are the ones that, by luck or design, maintained sufficiently smooth gradients that their internal pressures never exceeded their structural tolerances. ``Equality'' in this framework is not a value — it is a survival condition.

<div align="center">

\fbox{%
\begin{minipage}{0.88\textwidth}

**最后一句话 / Final Word**

**教育的公正不是道德律令，是几何约束。**

Educational justice is not a moral imperative — it is a geometric constraint.

不平滑的势能面活不长。

A non-smooth potential surface does not survive.

$\boxed{\sum_m \mathbf{g}_m = \mathbf{0}}$

不是应该平等——是不平等的教育系统在数学上注定分层，分层在数学上注定引爆。

Not ``should be equal'' — unequal educational systems are mathematically destined to stratify, and stratified systems are mathematically destined to destabilize.
\end{minipage}%
}

</div>

## Acknowledgments

This work builds on the SCX Equality Principle (平等论) framework developed in [cite]. We acknowledge the intellectual debt to the勢能面几何 formulation and the Theorem 7--12 chain. The application to education is novel to this paper; any errors in domain translation are ours alone.

\begin{thebibliography}{99}

\bibitem{scx_moe_gauge}
Anonymous. *势能面不齐——多专家路由中的规范自由度与MILP规范固定* (Potential Surface Misalignment: Gauge Freedom in Multi-Expert Routing and MILP Gauge Fixing). SCX Technical Report, 2026.

\bibitem{scx_equality_principle}
Anonymous. *平等论：势能面不齐的认识论含义* (The Equality Principle: Epistemological Implications of Potential Surface Misalignment). In [cite], Section~E, 2026.

\bibitem{scx_thm7}
Anonymous. *Theorem 7 — Cross-Domain Preservation of State Partitions: An Information-Theoretic Bound via the Situs Conditional Mutual Information*. SCX Theorem Series, 2026.

\bibitem{dweck2006mindset}
C.~S.~Dweck. *Mindset: The New Psychology of Success*. Random House, 2006.

\bibitem{vygotsky1978mind}
L.~S.~Vygotsky. *Mind in Society: The Development of Higher Psychological Processes*. Harvard University Press, 1978.

\bibitem{ladson2006achievement}
G.~Ladson-Billings. ``From the Achievement Gap to the Education Debt.'' *Educational Researcher*, 35(7):3--12, 2006.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas. *Elements of Information Theory*, 2nd ed. Wiley, 2006.

\bibitem{bjork1994memory}
R.~A.~Bjork. ``Memory and Metamemory Considerations in the Training of Human Beings.'' In *Metacognition: Knowing About Knowing*, MIT Press, 1994.

\bibitem{seligman1972learned}
M.~E.~P.~Seligman. ``Learned Helplessness.'' *Annual Review of Medicine*, 23(1):407--412, 1972.

\bibitem{oakes2005keeping}
J.~Oakes. *Keeping Track: How Schools Structure Inequality*, 2nd ed. Yale University Press, 2005.

\bibitem{rosenthal1968pygmalion}
R.~Rosenthal and L.~Jacobson. *Pygmalion in the Classroom*. Holt, Rinehart and Winston, 1968.

\bibitem{steele1997stereotype}
C.~M.~Steele. ``A Threat in the Air: How Stereotypes Shape Intellectual Identity and Performance.'' *American Psychologist*, 52(6):613--629, 1997.

\end{thebibliography}

## Appendix
## Notation Glossary / 符号表

[Table omitted — see original .tex]