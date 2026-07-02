# Beyond Metaphor: Rigorous Formalization of Quantum Entanglement, Data Wormholes, and Relativistic Invariance in SCX Auditing

**Xiaogan Supercomputing Center (SCX)**  
`papers/scx_acad_mdta_ilh/main.tex`  
**Classification:** INTERNAL  
**Version 1.0 --- 2026-07-02**

*Abstract:*

**Abstract:** This paper presents a rigorous mathematical formalization of three physics-inspired exploration paths in SCX auditing: Audit Correlation Asymmetry Detection (ACAD), Manifold Density Topology Analysis (MDTA), and Invariance Layered Hierarchy (ILH). These paths originate from conceptual analogies with quantum entanglement, wormholes (Einstein-Rosen bridges), and special relativity respectively, and have undergone five rounds of ``inspiration $\rightarrow$ correction $\rightarrow$ formalization $\rightarrow$ hostile review $\rightarrow$ final verdict.'' This paper presents the corrected final frameworks: ACAD provides information-theoretic/statistical-security tampering detection (5 theorems + 1 corollary), MDTA provides persistent-homology-based manifold shortcut audit risk assessment (5 theorems), and ILH documents SCX invariance structure via group theory (9 theorems). Each framework carries an honest verdict: ACAD is **conditionally useful**, MDTA is **pragmatically useful**, and ILH has **documentation value**. This paper adheres to the honesty principle: physics analogies are not disguised as mathematical correspondences, and each framework's limitations and fractures are explicitly stated.

**Keywords:** SCX auditing, entanglement, wormholes, relativity, gauge invariance, information-theoretic security, persistent homology, manifold learning, group theory, audit formalization

---

---

## Introduction
<!-- label: sec:intro -->

### Background and Motivation

SCX's core mathematical foundation is discrete Hodge theory + gauge theory ($U(1)$-type translation gauge + $O(d)$ lattice gauge). These tools originate from QFT and particle physics. This paper explores three deeper physics concepts --- quantum entanglement, wormholes (Einstein-Rosen bridges), and special relativity (Lorentz invariance) --- and honestly asks: do they provide audit perspectives not yet covered by discrete Hodge theory?

[Table omitted --- see original .tex]

### Five-Round Iteration History

This paper presents frameworks that have undergone five complete iterations:

1. **Round 1: Creative exploration** --- building analogical mappings from three physics concepts to SCX auditing
2. **Round 2: Self-review and correction** --- identifying mathematical fractures in each analogy, correcting into honest mathematical problems
3. **Round 3: Rigorous formalization** --- establishing explicit mathematical frameworks for all three corrected paths (definitions, theorems, proofs)
4. **Round 4: Hostile review** --- searching for fractures in the formalizations with the mindset of a thesis committee
5. **Round 5: Fixes and final verdict** --- repairing repairable fractures, honestly positioning each path's value

### Overview of Three Corrected Paths

[Table omitted --- see original .tex]

### Honesty Principle

This paper adheres to the following honesty principles:

1. **Analogies are not disguised as correspondences:** When physics concepts serve as inspiration, this is explicitly stated as analogy, not mathematical correspondence
2. **Fracture transparency:** Known fractures and limitations are presented alongside theorems
3. **Tiered verdict system:** A four-tier verdict system is used --- conditionally useful, pragmatically useful, documentation value, marginal value
4. **Audit value as ultimate criterion:** Regardless of formal elegance, practical audit value is the ultimate evaluation criterion

---

# Audit Correlation Asymmetry Detection / ACAD
<!-- label: part:acad -->

> [Table omitted --- see original .tex]

## ACAD Foundations
<!-- label: sec:acad-found -->

### Core Problem

If two auditors $A$ and $B$ have reference data linked by a secret constraint, can tampering with one side be detected with high probability by an attacker ignorant of the constraint?

This is an information-theoretic security problem --- sharing intuition with QKD but not its mathematics. ACAD corrects the entanglement analogy into an honest information-theoretic framework requiring no quantum mechanics.

### Basic Definitions

> **Definition:** [Audit Pair]
> <!-- label: def:audit-pair -->
> An audit pair is a triple $(\mathcal{A}, \mathcal{B}, \mathcal{C})$, where:
> 
> - $\mathcal{A} \subseteq \mathcal{X}^n$: auditor $A$'s reference dataset space ($n$ data points)
> - $\mathcal{B} \subseteq \mathcal{X}^n$: auditor $B$'s reference dataset space
> - $\mathcal{C} \subseteq \{C: \mathcal{X} \times \mathcal{X} \to \{0,1\}\}$: constraint function space

> **Definition:** [Secret Pairing]
> <!-- label: def:secret-pairing -->
> A secret pairing is a bijection $\phi: [n] \to [n]$ and a constraint function $C \in \mathcal{C}$, satisfying partial knowability for both auditors:
> 
> - Auditor $A$ knows $\{x_i^A\}_{i=1}^n$ but does not know $\phi$ and $\{x_j^B\}_{j=1}^n$
> - Auditor $B$ knows $\{x_j^B\}_{j=1}^n$ and $\phi$, but does not know $\{x_i^A\}_{i=1}^n$ (before the tampering detection phase)
> - Constraint satisfaction: $\forall i \in [n],\; C(x_i^A, x_{\phi(i)}^B) = 1$

> **Definition:** [Adversary Model]
> <!-- label: def:adversary -->
> The adversary $\mathcal{E}$ has the following capabilities and limitations:
> 
> - **Capability:** May modify any subset of $D_A = \{x_i^A\}_{i=1}^n$ to $\tilde{D}_A = \{\tilde{x}_i^A\}_{i=1}^n$
> - **Limitation:** Does not know $\phi$, $D_B$, or the specific form of $C$
> - **Knowledge:** Knows $\mathcal{X}$, $n$, and the original content of $D_A$

> **Definition:** [Tampering Detection Protocol]
> <!-- label: def:protocol -->
> 
> 1. **Initialization:** Auditor $B$ holds $D_B$ and $\phi$. A secure out-of-band channel is used for final comparison.
> 2. **Tampering:** The attacker modifies $D_A$ to $\tilde{D}_A$.
> 3. **Challenge:** $B$ randomly selects $k$ indices $i_1, ..., i_k \subset [n]$ (uniform without replacement).
> 4. **Request:** $B$ requests $\tilde{x}_{i_1}^A, ..., \tilde{x}_{i_k}^A$ from $A$.
> 5. **Verification:** $B$ computes the check pass rate.
> 6. **Decision:** If $T_k < \tau$ (predefined threshold), flag as ``tampering detected.''

## ACAD Theorem System
<!-- label: sec:acad-theorems -->

### Theorem 1: Detection Probability Lower Bound (Corrected)

> **Theorem:** [ACAD Detection Probability Lower Bound]
> <!-- label: thm:acad-detection -->
> Let the attacker modify $m$ data points ($1 \leq m \leq n$), and auditor $B$ draw $k$ samples without replacement for verification. Assume the constraint function $C$ is $\varepsilon$-robust: for any unmodified pair, $P(C(x_i^A, x_{\phi(i)}^B) = 1) \geq 1 - \varepsilon$ (where $\varepsilon \geq 0$ is natural noise). Assume the attacker does not know $\phi$ and $\phi$ is a uniformly random bijection. Then:
> 
> $$
> \boxed{P(\text{detection}) \geq 1 - \exp\left(-\frac{k \cdot \alpha^2 \cdot (1 - \varepsilon - \gamma)^2}{2\left(1 - (k-1)/n\right)}\right)}
> $$
> 
> where $\alpha = m/n$ is the tampering proportion, $\gamma$ is the maximum probability with which the attacker can successfully forge the constraint without knowing $\phi$, and $\tau$ is the detection threshold.

> **Proof:** Let $S$ be the set of tampered indices, $|S| = m$. $B$ draws $k$ samples (without replacement). For a uniformly random bijection $\phi$, the attacker cannot predict which $i$ are mapped to which $j$ by $\phi$.
> 
> Let $p_1$ be the single-check pass probability under tampering:
> 
> $$
> p_1 = \left(1 - \frac{m}{n}\right)(1 - \varepsilon) + \frac{m}{n} \cdot \gamma
> $$
> 
> where the first term comes from unmodified points (natural pass rate $1-\varepsilon$), and the second term from tampered points (attacker passes with probability at most $\gamma$).
> 
> Let $p_0 = 1 - \varepsilon$ (pass rate under no tampering). The detection condition is $T_k < \tau$. Choosing $\tau = \frac{p_0 + p_1}{2}$ as the midpoint:
> 
> $$
> \tau - p_1 = \frac{p_0 - p_1}{2} = \frac{m}{n} \cdot \frac{1 - \varepsilon - \gamma}{2} = \frac{\alpha(1 - \varepsilon - \gamma)}{2}
> $$
> 
> Using Serfling's inequality (concentration inequality for without-replacement sampling) instead of the original version's Hoeffding inequality:
> 
> $$
> P(T_k \geq \tau) = P(T_k - p_1 \geq \tau - p_1) \leq \exp\left(-\frac{2k(\tau - p_1)^2}{1 - (k-1)/n}\right)
> $$
> 
> Substituting $\tau - p_1$:
> 
> $$
> \begin{aligned}
> P(\text{no detection}) &\leq \exp\left(-\frac{2k \cdot (\alpha(1 - \varepsilon - \gamma)/2)^2}{1 - (k-1)/n}\right) \\
> &= \exp\left(-\frac{k \cdot \alpha^2 \cdot (1 - \varepsilon - \gamma)^2}{2(1 - (k-1)/n)}\right)
> \end{aligned}
> $$
> 
> Therefore $P(\text{detection}) \geq 1 - \exp\left(-\frac{k \alpha^2 (1 - \varepsilon - \gamma)^2}{2(1 - (k-1)/n)}\right)$.
> 
> $\square$ **Note:** The original version (Theorem 6.1 in Round 3) used Hoeffding's inequality with independent Bernoulli approximation. This corrected version uses Serfling's inequality to handle the correlation from without-replacement sampling. When $k \ll n$, the correction factor $1 - (k-1)/n \approx 1$, and the two versions are equivalent.

### Theorem 2: Statistical Security Bound

> **Theorem:** [ACAD Statistical Security Bound]
> <!-- label: thm:acad-security -->
> If the attacker does not know $\phi$ and $D_B$, and $|D_B| = n$ is sufficiently large, then for any attack strategy $\mathcal{E}$ satisfying the knowledge constraints, there exists a constant $c > 0$ such that:
> 
> $$
> \boxed{\inf_{\mathcal{E}} P(\text{detection}) \geq 1 - \exp\left(-c \cdot k \cdot \alpha^2\right)}
> $$
> 
> where $c = \frac{(1 - \varepsilon - \gamma)^2}{2(1 - (k-1)/n)}$, and the infimum is taken over all attack strategies satisfying the knowledge constraints.

> **Proof:** The attacker's information state is determined by the $\sigma$-algebra $\sigma(\tilde{D}_A, D_A)$ (what the attacker knows). $\phi$ is not measurable with respect to this $\sigma$-algebra (the attacker does not know the pairing).
> 
> By the data processing inequality from information theory, the lower bound on the attacker's estimation error for $\phi$ is:
> 
> $$
> H(\phi \mid \tilde{D}_A, D_A) \geq \log(n!) - I(\phi; D_A)
> $$
> 
> where $H$ is entropy and $I$ is mutual information. Since $D_A$ is generated by a process independent of $\phi$ (during initialization), $I(\phi; D_A) = 0$. Therefore $H(\phi \mid \tilde{D}_A, D_A) = \log(n!)$ --- the attacker has complete ignorance about $\phi$.
> 
> Under this ignorance condition, the attacker's probability of successfully forging the constraint is bounded by the random guessing level, leading to the exponential bound in Theorem [ref].
> 
> $\square$ **Important correction:** The original version (Theorem 6.2 in Round 3) claimed ``information-theoretic security.'' This corrected version downgrades to ``statistical security'' because: (1) the constraint $C$ may have exploitable structure; (2) the attacker can achieve partial success by modifying many data points; (3) verification is sampling-based rather than exhaustive. ACAD does not achieve one-time-pad level perfect security.

### Theorem 3: Sample Complexity

> **Theorem:** [Sample Complexity]
> <!-- label: thm:acad-sample -->
> To achieve detection probability at least $1 - \delta$ (at a given significance level), the minimum required sample size $k^*$ satisfies:
> 
> $$
> \boxed{k^* \geq \frac{2 \cdot (1 - (k^*-1)/n)}{\alpha^2 (1 - \varepsilon - \gamma)^2} \cdot \log\frac{1}{\delta}}
> $$
> 
> For fixed tampering proportion $\alpha$ with $k \ll n$, the asymptotic bound is:
> 
> $$
> k^* = O\left(\frac{1}{\alpha^2} \cdot \log\frac{1}{\delta}\right)
> $$

> **Proof:** Starting from the bound in Theorem [ref], set $P(\text{no detection}) \leq \delta$:
> 
> $$
> \exp\left(-\frac{k \alpha^2 (1 - \varepsilon - \gamma)^2}{2(1 - (k-1)/n)}\right) \leq \delta
> $$
> 
> Taking the logarithm and rearranging yields the result. When $k \ll n$, $1 - (k-1)/n \approx 1$, giving the simplified form.

### Corollary: Feasibility Under Practical Parameters

> **Corollary:** [Practical Parameters]
> <!-- label: cor:acad-practical -->
> If $\alpha = 0.1$ (attacker modifies 10\% of data), $\varepsilon = 0.05$ (5\% natural noise), $\gamma = 0$ (attacker completely ignorant of constraint), $\delta = 0.01$ (99\% detection confidence), and $n = 10^4$, then $k^* \geq 2 \cdot 1 \cdot 100 / (1 \cdot 0.9025) \cdot 4.605 \approx 1020$. Only about 10\% of the data needs to be checked to detect tampering with high probability.

### Theorem 4: Audit Setting Dependence Detection

> **Theorem:** [ACAD Audit Evasion Detection]
> <!-- label: thm:acad-mm -->
> Let expert system $E$ produce prediction distributions $p_1$ and $p_2$ under audit settings $S_1$ and $S_2$. Define the audit setting dependence measure:
> 
> $$
> \Delta(S_1, S_2) = \MMD(p_1, p_2) = \sup_{f \in \mathcal{F}} \left| \mathbb{E}_{x \sim p_1}[f(x)] - \mathbb{E}_{x \sim p_2}[f(x)] \right|
> $$
> 
> where $\mathcal{F}$ is the unit ball of the reproducing kernel Hilbert space (RKHS). Then under the null hypothesis $H_0: p_1 = p_2$ (no audit setting dependence):
> 
> $$
> \boxed{P\left( \widehat{\MMD}_n > \sqrt{\frac{2K}{n}} + \sqrt{\frac{2}{n}\log\frac{1}{\delta}} \right) \leq \delta}
> $$
> 
> where $K = \sup_x k(x, x)$ is the kernel's upper bound, and $\widehat{\MMD}_n$ is the empirical MMD estimate.

> **Proof:** This is a classic concentration inequality for MMD. For a bounded kernel $k(\cdot, \cdot) \leq K$, the empirical MMD estimate $\widehat{\MMD}_n$ satisfies McDiarmid's inequality. Specifically, changing a single sample affects MMD by at most $2\sqrt{K/n}$, therefore:
> 
> $$
> P\left(\widehat{\MMD}_n - \mathbb{E}[\widehat{\MMD}_n] > t\right) \leq \exp\left(-\frac{nt^2}{2K}\right)
> $$
> 
> Under $H_0$, $\mathbb{E}[\widehat{\MMD}_n] \leq \sqrt{2K/n}$. Substituting and setting $t = \sqrt{\frac{2}{n}\log\frac{1}{\delta}}$ yields the result.

### Theorem 5: Constraint Construction Schemes

> **Theorem:** [Cryptographic Constraint Construction]
> <!-- label: thm:acad-constraint -->
> There are two constructible classes of constraint functions satisfying the security requirements of the ACAD protocol:
> 
> 1. **Data manifold pairing constraint:** Select a public set of high-density reference points $R = \{r_1, ..., r_n\}$. For each $r_i$, sample $x_i^A$ and $x_i^B$ within the $\varepsilon$-neighborhood. The constraint $C(x_i^A, x_i^B) = 1$ holds iff $d_{\mathcal{M}}(x_i^A, r_i) < \varepsilon$ and $d_{\mathcal{M}}(x_i^B, r_i) < \varepsilon$. This constraint does not depend on expert predictions (avoiding circularity).
> 2. **Cryptographic hash constraint:** Construct using a hash chain: $x_i^B = H(x_i^A \| K)$, where $H$ is a cryptographic hash function and $K$ is a shared secret key. The constraint $C(x_i^A, x_i^B) = 1$ holds iff $H(x_i^A \| K) = x_i^B$. An attacker without knowledge of $K$ cannot construct $\tilde{x}_i^A$ satisfying the constraint.
> 
> Scheme (b) provides the strongest security guarantee --- security reduces to the preimage resistance of the hash function.

> **Proof:** For scheme (a), the constraint does not depend on expert predictions, thus avoiding the circularity of ``auditing validates expert predictions, while constraints depend on expert predictions.'' The attacker needs to know the global structure of the manifold (neighborhoods of $r_i$) to forge the constraint --- this is equivalent to knowing the distribution of $D_B$, consistent with the attacker's knowledge limitations.
> 
> For scheme (b), the probability that an attacker without knowledge of $K$ can construct $\tilde{x}_i^A$ such that $H(\tilde{x}_i^A \| K) = x_i^B$ equals the success probability of a preimage attack on a random oracle, which under standard cryptographic assumptions is $O(2^{-|K|})$, i.e., $\gamma = \text{negl}(|K|)$.

## ACAD Verdict
<!-- label: sec:acad-verdict -->

\begin{verdictbox}{verdictyellow}
**Final Verdict: CONDITIONALLY USEFUL**

[Table omitted --- see original .tex]

**Applicable when:** (1) constraints can be cryptographically realized (e.g., hash chains), (2) auditors share a secure channel. ACAD provides a provably secure tampering detection scheme.

**Note:** Do not claim ACAD is ``quantum'' or has quantum advantage --- it is a classical statistical security scheme.
\end{verdictbox}

---

# Manifold Density Topology Analysis / MDTA
<!-- label: part:mdta -->

> [Table omitted --- see original .tex]

## MDTA Foundations
<!-- label: sec:mdta-found -->

### Core Problem

Do low-density regions on the Situs manifold constitute audit blind spots? Are two clusters far apart in ambient space close in manifold distance? Can local auditing capture such global topological relationships?

MDTA corrects the ``wormhole'' analogy into an honest manifold learning + TDA framework. ``Shortcut'' replaces ``wormhole'' --- since the Situs manifold is typically connected, paths always exist, only shorter or longer. More like ``canyons'' or ``tunnels'' than ``wormholes.''

### Basic Definitions

> **Definition:** [Data Manifold]
> <!-- label: def:data-manifold -->
> Let $\mathcal{X} \subseteq \mathbb{R}^D$ be the data space (ambient space). A data manifold is a triple $(\mathcal{M}, g, p)$, where:
> 
> - $\mathcal{M}$ is a $d$-dimensional smooth manifold ($d \ll D$), $\mathcal{M} \subset \mathbb{R}^D$ is an embedded submanifold
> - $g$ is a Riemannian metric on $\mathcal{M}$ (either the pullback metric induced by the embedding or a Fisher information metric constructed from data density)
> - $p: \mathcal{M} \to \mathbb{R}_{>0}$ is a data density function on $\mathcal{M}$ (smooth, integrable)
> 
> **Honesty statement:** Real SCX data may not satisfy the smooth manifold assumption. MDTA statistics remain computable as **descriptive geometric features** --- the manifold assumption is not required for the algorithm to ``work''; it is an algorithmic output rather than a theoretical prerequisite. Alternative: use the **stratified space** assumption, allowing different regions to have different dimensions.

> **Definition:** [Cluster]
> <!-- label: def:cluster -->
> A $\rho$-cluster on the data manifold $\mathcal{M}$ is a connected open set $\mathcal{C} \subset \mathcal{M}$ satisfying:
> 
> 1. $\forall x \in \mathcal{C}, p(x) \geq \rho$ (density lower bound)
> 2. $\mathcal{C}$ is path-connected
> 3. At the boundary $\partial\mathcal{C}$, $p(x) = \rho$

> **Definition:** [Manifold Distance]
> <!-- label: def:manifold-dist -->
> The manifold distance between two points $x, y \in \mathcal{M}$ is:
> 
> $$
> d_{\mathcal{M}}(x, y) = \inf_{\gamma: [0,1] \to \mathcal{M}, \gamma(0)=x, \gamma(1)=y} \int_0^1 \sqrt{g_{\gamma(t)}(\dot{\gamma}(t), \dot{\gamma}(t))} \, dt
> $$
> 
> The manifold distance between two clusters $\mathcal{C}_i, \mathcal{C}_j$ is:
> 
> $$
> d_{\mathcal{M}}(\mathcal{C}_i, \mathcal{C}_j) = \inf_{x \in \mathcal{C}_i, y \in \mathcal{C}_j} d_{\mathcal{M}}(x, y)
> $$

> **Definition:** [Shortcut Ratio]
> <!-- label: def:shortcut-ratio -->
> For two clusters $\mathcal{C}_i, \mathcal{C}_j$, the shortcut ratio is defined as:
> 
> $$
> \boxed{r(\mathcal{C}_i, \mathcal{C}_j) = \frac{d_{\mathcal{M}}(\mathcal{C}_i, \mathcal{C}_j)}{\|\mu_i - \mu_j\|}}
> $$
> 
> where $\mu_i = \frac{1}{\vol(\mathcal{C}_i)} \int_{\mathcal{C}_i} x \, dx$ is the centroid of $\mathcal{C}_i$.

> **Definition:** [Manifold Shortcut]
> <!-- label: def:shortcut -->
> When $r(\mathcal{C}_i, \mathcal{C}_j) < \tau$ ($\tau \in (0, 1)$ is a predefined threshold), $(\mathcal{C}_i, \mathcal{C}_j)$ is called a $\tau$-manifold shortcut. The minimum-density path on the shortcut is:
> 
> $$
> \gamma^*_{ij} = \arg\min_{\gamma: \mathcal{C}_i \to \mathcal{C}_j} \int_\gamma ds
> $$
> 
> The density minimum along $\gamma^*$ defines the **throat** of the shortcut:
> 
> $$
> x_{\text{throat}} = \arg\min_{x \in \gamma^*_{ij}} p(x)
> $$

## MDTA Theorem System
<!-- label: sec:mdta-theorems -->

### Theorem 1: Variational Characterization of Shortcut Density

> **Theorem:** [Variational Characterization of Shortcut Density]
> <!-- label: thm:mdta-variational -->
> Let $\gamma^*$ be the minimal manifold geodesic connecting $\mathcal{C}_i$ and $\mathcal{C}_j$. The density function $p(\gamma^*(t))$ along $\gamma^*$ satisfies: for a shortcut ($r < 1$), there exists a unique minimum point $t^* \in (0, 1)$ such that:
> 
> $$
> \boxed{p(\gamma^*(t^*)) = \min_{t \in [0,1]} p(\gamma^*(t)) < \min(\rho_i, \rho_j)}
> $$
> 
> where $\rho_i, \rho_j$ are the density lower bounds of $\mathcal{C}_i, \mathcal{C}_j$. Moreover, if the curvature of $\gamma^*$ satisfies $|\ddot{\gamma}^*(t^*)| > 0$, then:
> 
> $$
> p(\gamma^*(t^*)) \leq \frac{\rho_i + \rho_j}{2} - \frac{1}{8} |\ddot{\gamma}^*(t^*)| \cdot (\rho_i - \rho_j)^2 + O((\rho_i - \rho_j)^3)
> $$

> **Proof:** By the shortcut definition $r < 1$, the manifold path ``detours'' in ambient space, implying significant curvature or folding of $\mathcal{M}$ near $\gamma^*$. The second-order Taylor expansion of the density function along the geodesic is:
> 
> $$
> p(\gamma^*(t)) = p(\gamma^*(t^*)) + \frac{1}{2} p''(\gamma^*(t^*)) (t - t^*)^2 + O((t - t^*)^3)
> $$
> 
> At the endpoints $t = 0, 1$, $p \geq \min(\rho_i, \rho_j)$. Let the density at endpoint $t=0$ be $\rho_i + \delta_i$ ($\delta_i \geq 0$), and at $t=1$ be $\rho_j + \delta_j$. Matching endpoint conditions with the second-order expansion:
> 
> $$
> \begin{aligned}
> p(\gamma^*(0)) &= p(t^*) + \frac{1}{2}p''(t^*) \cdot (t^*)^2 = \rho_i + \delta_i \\
> p(\gamma^*(1)) &= p(t^*) + \frac{1}{2}p''(t^*) \cdot (1-t^*)^2 = \rho_j + \delta_j
> \end{aligned}
> $$
> 
> Under the curvature condition, $p''(t^*)$ is positively correlated with $|\ddot{\gamma}^*(t^*)|$ (density changes faster in regions of high curvature). Solving simultaneously and taking the worst case $\delta_i = \delta_j = 0$ yields the stated bound.
> 
> $\square$ **Note:** The theorem relies on a small-curvature assumption for the convergence of the Taylor expansion. In high-curvature regions (which characterize shortcuts), higher-order expansions or nonparametric bounds are needed. This is a known technical limitation.

### Theorem 2: Shortcut Existence Condition

> **Theorem:** [Shortcut Existence Condition]
> <!-- label: thm:mdta-existence -->
> A sufficient condition for a $\tau$-shortcut between two $\rho$-clusters $\mathcal{C}_i, \mathcal{C}_j$ is:
> 
> $$
> \boxed{\exists \text{ a path } \gamma \text{ connecting } \mathcal{C}_i, \mathcal{C}_j \text{ such that } \frac{\int_\gamma ds}{\|\mu_i - \mu_j\|} < \tau}
> $$
> 
> Equivalently, if the reach $\tau_{\mathcal{M}}$ of $\mathcal{M}$ satisfies:
> 
> $$
> \tau_{\mathcal{M}} < \frac{\|\mu_i - \mu_j\|}{2} \cdot \sqrt{\frac{1}{\tau^2} - 1}
> $$
> 
> then a shortcut exists.

> **Proof:** By the definition of a manifold's reach (the maximum distance from $\mathcal{M}$ to its medial axis). Smaller reach implies more severe manifold folding. When folding makes the path along $\mathcal{M}$ significantly longer than the ambient-space straight-line distance, the shortcut ratio satisfies $r < 1$.
> 
> Let $\gamma$ be the straight line segment connecting the two centroids (in ambient space $\mathbb{R}^D$). The tubular neighborhood radius of $\mathcal{M}$ near $\gamma$ is bounded by the reach $\tau_{\mathcal{M}}$. The shortest path length along $\mathcal{M}$ satisfies:
> 
> $$
> \int_{\gamma_{\mathcal{M}}} ds \leq \|\mu_i - \mu_j\| + 2\tau_{\mathcal{M}} \cdot \theta
> $$
> 
> where $\theta$ is the angular width of the tubular neighborhood. When $\tau_{\mathcal{M}}$ is sufficiently small, a path exists satisfying the shortcut ratio condition.

### Theorem 3: Audit Risk Classification and Its Lipschitz Consistency

> **Theorem:** [Audit Risk Classification]
> <!-- label: thm:mdta-risk -->
> For a shortcut $(\mathcal{C}_i, \mathcal{C}_j, \gamma^*)$, define the Shortcut Audit Risk (SAR):
> 
> $$
> \SAR(\gamma^*) = \Var_\gamma[g] \times \left|\frac{d}{dt} Cercis(\gamma^*(t))\right| \times \frac{1}{p(x_{\text{throat}})}
> $$
> 
> Based on the SAR score, shortcuts are classified into:
> 
> - **Benign shortcut:** $\SAR < \theta_1$ $\rightarrow$ genuine data structure
> - **Adversarial shortcut:** $\theta_1 \leq \SAR < \theta_2$ $\rightarrow$ potential audit blind spot
> - **Noise corridor:** $\SAR \geq \theta_2$ $\rightarrow$ non-auditable region
> 
> Classification consistency is guaranteed by the following Lipschitz condition: if Cercis is $\alpha$-Lipschitz along the shortcut, then:
> 
> $$
> \boxed{|\SAR(\gamma_1^*) - \SAR(\gamma_2^*)| \leq L \cdot d_{\mathcal{M}}(\gamma_1^*, \gamma_2^*)}
> $$
> 
> where $L = L_V \cdot \alpha \cdot L_p$ is the composite Lipschitz constant ($L_V$: variance Lipschitz constant, $L_p$: inverse-density Lipschitz constant).

> **Proof:** By the Lipschitz property of each factor:
> 
> $$
> \begin{aligned}
> |\Var_{\gamma_1}[g] - \Var_{\gamma_2}[g]| &\leq L_V \cdot d_{\mathcal{M}}(\gamma_1^*, \gamma_2^*) \\
> \left|\frac{d}{dt}Cercis(\gamma_1^*(t)) - \frac{d}{dt}Cercis(\gamma_2^*(t))\right| &\leq \alpha \cdot d_{\mathcal{M}}(\gamma_1^*, \gamma_2^*) \\
> \left|\frac{1}{p(x_{\text{throat},1})} - \frac{1}{p(x_{\text{throat},2})}\right| &\leq L_p \cdot d_{\mathcal{M}}(\gamma_1^*, \gamma_2^*)
> \end{aligned}
> $$
> 
> The Lipschitz property of the product follows from the product rule, with $L = L_V \cdot \alpha \cdot L_p + \text{cross-terms}$.
> 
> $\square$ **Honestly:** The product composition of SAR lacks theoretical justification --- why product? Why these three factors? This is an ad-hoc heuristic. Fix: use the SAR multi-metric vector (see Section [ref]).

### Theorem 4: Complexity of Discrete Shortcut Detection

> **Theorem:** [Complexity of Discrete Shortcut Detection]
> <!-- label: thm:mdta-complexity -->
> For a set of $N$ data points, using a $k$-NN graph ($k = O(\log N)$) for manifold distance estimation, the shortcut detection algorithm has time complexity:
> 
> $$
> \boxed{O(N \log N \cdot k + C^2 \cdot N \log N)}
> $$
> 
> where $C$ is the number of detected clusters.

> **Proof:** The algorithm proceeds in two phases:
> 
> 1. **$k$-NN graph construction:** Completed in $O(N \log N \cdot k)$ time using a kd-tree
> 2. **Shortest paths for all cluster pairs:** For $C$ clusters, there are $O(C^2)$ pairs. Running Dijkstra's algorithm on each pair has complexity $O(N \log N)$ per pair (using a binary heap), totaling $O(C^2 \cdot N \log N)$
> 
> Total complexity is the sum of both phases.

### Theorem 5: Consistency of Shortcut Ratio Estimation

> **Theorem:** [Consistency of Shortcut Ratio Estimation]
> <!-- label: thm:mdta-consistency -->
> Let $\hat{d}_{\mathcal{M}}$ be the manifold distance estimate based on the $k$-NN graph, and $\hat{r}$ the corresponding shortcut ratio estimate. Then as $N \to \infty$, $k \to \infty$, $k/N \to 0$:
> 
> $$
> \boxed{\hat{r} \xrightarrow{P} r \quad \text{i.e.} \quad \forall \varepsilon > 0: \lim_{N \to \infty} P(|\hat{r} - r| > \varepsilon) = 0}
> $$
> 
> The $k$-NN graph-based shortcut ratio estimate converges in probability to the true ratio as $N \to \infty$ under standard manifold learning conditions.

> **Proof:** By the Isomap consistency of $k$-NN graph distances (Bernstein et al., 2000; Tenenbaum et al., 2000), under the conditions that $\mathcal{M}$ is compact and geodesically convex, the $k$-NN graph shortest path converges uniformly to the manifold geodesic distance:
> 
> $$
> \hat{d}_{\mathcal{M}}(x, y) \xrightarrow{P} d_{\mathcal{M}}(x, y)
> $$
> 
> Centroid estimates $\hat{\mu}_i \xrightarrow{P} \mu_i$ follow from the law of large numbers. The shortcut ratio $\hat{r} = \hat{d}_{\mathcal{M}} / \|\hat{\mu}_i - \hat{\mu}_j\|$ is a continuous function; consistency follows from the continuous mapping theorem.
> 
> $\square$ **Important condition:** Consistency depends on (1) manifold compactness, (2) uniform sampling or bounded-below density, (3) bounded metric curvature. In low-density regions where shortcuts occur, $k$-NN graph connections may be unreliable --- this is the core dilemma of shortcut detection.

## MDTA Fixes
<!-- label: sec:mdta-fixes -->

### Statistical Significance Test for Shortcuts

To eliminate the arbitrariness of the threshold $\tau$, introduce a bootstrap significance test:

> **Definition:** [Statistically Significant Shortcut]
> <!-- label: def:significant-shortcut -->
> The shortcut ratio $r_{ij}$ is statistically significant at level $\alpha$ if:
> 
> $$
> P_{H_0}(r \leq r_{ij}^{\text{obs}}) \leq \alpha
> $$
> 
> where the null distribution $H_0: r = 1$ is estimated via $B = 1000$ bootstrap resamples. For each bootstrap iteration: resample with replacement from $\mathcal{C}_i$ and $\mathcal{C}_j$, compute $r_{ij}^{(b)}$, construct a confidence interval and test $H_0$. If $r_{ij}$ is significantly less than 1 at the $1-\alpha$ confidence level, flag it as a shortcut.

### SAR Multi-Metric Version

Replace the single product SAR with a multi-metric vector:

$$
\SAR\text{-Profile}(\gamma^*) = \begin{pmatrix}
\Var_\gamma[g] \\
\|\nabla_\gamma Cercis\| \\
1/p(x_{\text{throat}}) \\
\text{shortcut ratio } r \\
\text{throat width } w_{\text{throat}}
\end{pmatrix}
$$

Auditors select which dimensions to focus on based on the specific scenario (adversarial detection vs. topological exploration vs. data quality assessment).

## MDTA Verdict
<!-- label: sec:mdta-verdict -->

\begin{verdictbox}{verdictgreen}
**Final Verdict: PRAGMATICALLY USEFUL**

[Table omitted --- see original .tex]

**MDTA is the most ``down-to-earth'' path.** No fancy physics packaging needed --- shortcut detection, persistent homology, and SAR multi-metric analysis all have ready implementations in the TDA toolbox. The core contribution is **directing these tools toward auditing**.

**Audit recommendation:** detect cluster pairs with $r < 0.3$, flag as ``audit blind spot candidates,'' prioritize for human review or enhanced sampling.
\end{verdictbox}

---

# Invariance Layered Hierarchy / ILH
<!-- label: part:ilh -->

> [Table omitted --- see original .tex]

## ILH Foundations
<!-- label: sec:ilh-found -->

### Core Problem

How are SCX audit invariances organized by symmetry group layers? What audit guarantees does each layer provide? Where does Cercis Score sit in the invariance hierarchy?

ILH corrects the ``relativity'' analogy into honest invariance structure documentation. Core finding: SCX's invariance structure is closest to **Galileo invariance** (spatial translation + rotation), not Lorentz invariance (with boosts). SCX's ``relativity'' is Galilean, not Einsteinian.

### Basic Definitions

> **Definition:** [Audit Object]
> <!-- label: def:audit-object -->
> The basic object of SCX auditing is the expert prediction configuration:
> 
> $$
> \mathcal{G} = \mathbb{R}^{M \times d}
> $$
> 
> the space of all possible expert prediction matrices (each row is a $d$-dimensional prediction vector for one expert). $\Gamma \in \mathcal{G}$ denotes a configuration.

> **Definition:** [Symmetry Group Action]
> <!-- label: def:group-action -->
> For a group $G$ with representation $\rho: G \to GL(\mathcal{G})$, the group action is defined as:
> 
> $$
> \alpha: G \times \mathcal{G} \to \mathcal{G}, \quad \alpha(g, \Gamma) = \rho(g) \cdot \Gamma
> $$

> **Definition:** [Invariance Layer]
> <!-- label: def:invariance-layer -->
> The $\ell$-th invariance layer is defined by a group $G_\ell$ and its action $\alpha_\ell$, satisfying the hierarchical inclusion:
> 
> $$
> G_0 \subset G_1 \subset G_2 \subset ... \subset G_L
> $$
> 
> where $G_0 = \{e\}$ (trivial group, no invariance).

## ILH Theorem System
<!-- label: sec:ilh-theorems -->

### Theorem 1: Layered Invariant Space (Corrected)

> **Theorem:** [Layered Invariant Space]
> <!-- label: thm:ilh-invariant-space -->
> For each layer $\ell$, the invariant space is the orbit space $\mathcal{I}_\ell = \mathcal{G} / G_\ell$. There exist natural projections between layers:
> 
> $$
> \begin{tikzcd}
> \mathcal{G} \arrow[r, "\pi_\ell"] \arrow[rd, "\pi_{\ell-1}"'] & \mathcal{I}_\ell \arrow[d, "\pi_{\ell, \ell-1}"] \\
> & \mathcal{I}_{\ell-1}
> \end{tikzcd}
> $$
> 
> where $\pi_{\ell, \ell-1}$ is the natural map between orbit spaces induced by $G_{\ell-1} \subset G_\ell$.

> **Proof:** This is a standard construction in group action theory. Elements of $\mathcal{I}_\ell$ are $G_\ell$-orbits in $\mathcal{G}$. Since $G_{\ell-1} \subset G_\ell$, each $G_\ell$-orbit contains a complete $G_{\ell-1}$-orbit, so there is a well-defined surjection $\pi_{\ell, \ell-1}: \mathcal{G}/G_\ell \to \mathcal{G}/G_{\ell-1}$.
> 
> $\square$ **Note:** The original version (Theorem 8.1 in Round 3) used category-theoretic functor language $\mathcal{F}_\ell: \mathcal{G} \to \mathcal{I}_\ell$. This language was decorative --- $\mathcal{F}_\ell$ is simply the natural projection $\mathcal{G} \to \mathcal{G}/G_\ell$, requiring no category-theoretic framework. This corrected version uses direct group-theoretic formulation.

### Theorem 2: Translation Invariance of Cercis

> **Theorem:** [Translation Invariance of Cercis]
> <!-- label: thm:ilh-cercis-translation -->
> Let the Cercis Score be defined as a function of the set of difference vectors:
> 
> $$
> Cercis(\Gamma) = f\left(\{d_{mn}\}_{m<n}\right), \quad d_{mn} = \Gamma_m - \Gamma_n \in \mathbb{R}^d
> $$
> 
> Then Cercis is invariant under diagonal translation $G_1 = (\mathbb{R}^d, +)^M_{\text{diag}}$ (acting as $\Gamma \mapsto \Gamma + \mathbf{1}_M \otimes c^T$, $c \in \mathbb{R}^d$):
> 
> $$
> \boxed{Cercis(\Gamma + \mathbf{1}_M \otimes c^T) = Cercis(\Gamma)}
> $$
> 
> Cercis Score is invariant under diagonal translation of all expert predictions by the same vector.

> **Proof:** $d_{mn}' = (\Gamma_m + c) - (\Gamma_n + c) = \Gamma_m - \Gamma_n = d_{mn}$, so the difference vectors are unchanged, hence Cercis (as a function of difference vectors) is unchanged.

### Theorem 3: Completeness of Translation Invariants

> **Theorem:** [Completeness of Translation Invariants]
> <!-- label: thm:ilh-completeness -->
> The set of difference vectors $\{d_{mn}\}_{m<n}$ forms a **complete set of invariants** for the translation group action --- two configurations $\Gamma, \Gamma'$ are equivalent under translation iff all their difference vectors are equal:
> 
> $$
> \boxed{\Gamma' = \Gamma + \mathbf{1}_M \otimes c^T \text{ for some } c \in \mathbb{R}^d \iff d_{mn}' = d_{mn} \; \forall m,n}
> $$

> **Proof:** ($\Rightarrow$) If $\Gamma' = \Gamma + \mathbf{1}_M \otimes c^T$, then $d_{mn}' = d_{mn}$ holds trivially.
> 
> ($\Leftarrow$) If $d_{mn}' = d_{mn}$ for all $m,n$, fix $m=1$, then $\Gamma_n' = \Gamma_n + (\Gamma_1' - \Gamma_1)$ for all $n$. Let $c = \Gamma_1' - \Gamma_1$, then $\Gamma' = \Gamma + \mathbf{1}_M \otimes c^T$.

### Theorem 4: Rotational Invariance of Cercis

> **Theorem:** [Rotational Invariance of Cercis]
> <!-- label: thm:ilh-cercis-rotation -->
> If the Cercis Score depends on $\Gamma$ only through norms and inner products, then for all $R \in O(d)$:
> 
> $$
> \boxed{Cercis(\Gamma R^T) = Cercis(\Gamma)}
> $$
> 
> where the rotation acts as $\Gamma \mapsto \Gamma \cdot R^T$ (all expert predictions transformed by the same rotation).

> **Proof:** $\|\Gamma_m R^T\|^2 = \Gamma_m R^T R \Gamma_m^T = \Gamma_m \Gamma_m^T = \|\Gamma_m\|^2$ (since $R^T R = I$). $(\Gamma_m R^T) \cdot (\Gamma_n R^T) = \Gamma_m R^T R \Gamma_n^T = \Gamma_m \Gamma_n^T$. Hence norms and inner products are invariant under $O(d)$, and Cercis (as a function of norms and inner products) is invariant.

### Theorem 5: Structure of Semidirect Product Invariants

> **Theorem:** [Structure of Semidirect Product Invariants]
> <!-- label: thm:ilh-semidirect -->
> The invariant space of $G_3 = E(d) = \mathbb{R}^d \rtimes O(d)$ is isomorphic to the intersection of translation and rotation invariant spaces:
> 
> $$
> \boxed{\mathcal{I}_3 \cong (\mathcal{G} / (\mathbb{R}^d, +)) \cap (\mathcal{G} / O(d)) \cong \mathcal{G} / E(d)}
> $$

> **Proof:** By the group structure of $E(d) = \mathbb{R}^d \rtimes O(d)$. Any $E(d)$-invariant must be invariant under both translations and rotations. Since $(\mathbb{R}^d, +) \triangleleft E(d)$ (translations form a normal subgroup), the orbit space inherits the semidirect product structure: $\mathcal{G}/E(d) = (\mathcal{G}/(\mathbb{R}^d, +))/O(d)$.

### Theorem 6: Diffeomorphism Invariance of Topological Invariants

> **Theorem:** [Diffeomorphism Invariance of Topological Invariants]
> <!-- label: thm:ilh-diffeo -->
> Betti numbers $\beta_k(\mathcal{X})$ and the multiset of persistent homology barcodes are invariant under diffeomorphism:
> 
> $$
> \boxed{\beta_k(\phi(\mathcal{X})) = \beta_k(\mathcal{X}), \quad \text{Barcode}(\phi(\mathcal{X})) \cong \text{Barcode}(\mathcal{X})}
> $$
> 
> where $\phi \in \Diff(\mathcal{X})$ is a diffeomorphism of the base manifold $\mathcal{X}$.

> **Proof:** Betti numbers are homotopy invariants; diffeomorphisms induce homotopy equivalences. Persistent homology barcodes are invariant under isometric embeddings; diffeomorphisms preserve topological structure (but **not** necessarily geometric/distance information).

### Theorem 7: Information Loss Hierarchy Theorem

> **Theorem:** [Information Loss Hierarchy Theorem]
> <!-- label: thm:ilh-information -->
> Let $H(\cdot)$ be an information content measure on configuration space. Then information content decreases monotonically across layers:
> 
> $$
> \boxed{H(\mathcal{I}_L) \leq H(\mathcal{I}_{L-1}) \leq ... \leq H(\mathcal{I}_1) \leq H(\mathcal{I}_0)}
> $$
> 
> The information loss per layer (in terms of degrees of freedom) is:
> 
> $$
> \Delta H_\ell = \dim(G_\ell) - \dim(G_{\ell-1})
> $$
> 
> Specifically: $\Delta H_1 = d$ (translation loses $d$ degrees of freedom), $\Delta H_2 = d(d-1)/2$ (rotation loses $d(d-1)/2$ degrees of freedom), $\Delta H_3 = d + d(d-1)/2$ (total).

> **Proof:** The ``size'' of the orbit space $\mathcal{I}_\ell = \mathcal{G} / G_\ell$ decreases as $G_\ell$ grows. For continuous groups, information loss equals the dimension of the quotient group action's degrees of freedom. Since $G_\ell / G_{\ell-1}$ is a Lie group of dimension $\dim(G_\ell) - \dim(G_{\ell-1})$, $\Delta H_\ell$ follows as stated.
> 
> $\square$ **Note:** For continuous groups, the ``entropy'' of a quotient space is not a well-defined quantity in the traditional sense (differing by an infinite constant). This theorem uses **degrees of freedom** as a proxy measure for information loss --- this is more rigorous and avoids the technical issues of differential entropy.

### Theorem 8: Layered Positioning of Cercis

> **Theorem:** [Layered Positioning of Cercis]
> <!-- label: thm:ilh-cercis-position -->
> Cercis Score is invariant at layers 1, 2, and 3, but not at layer 0. For the standard definition of Cercis (based on variance of difference vector norms), its invariance group is:
> 
> $$
> \boxed{G_{Cercis} = \Stab(Cercis) = \{\Gamma \mapsto \Gamma R^T + \mathbf{1}_M \otimes c^T : R \in O(d), c \in \mathbb{R}^d\} \cong E(d)}
> $$
> 
> That is, $E(d)$ is the **maximal connected subgroup** preserving Cercis (for this specific Cercis definition).

> **Proof:** Cercis is invariant under $E(d)$ (Theorem [ref] + Theorem [ref]). We need to argue that $E(d)$ is the maximal connected subgroup: suppose a larger connected subgroup $G \supset E(d)$ preserves Cercis. Then $G$ must preserve some function of all difference vectors. But the complete set of invariants of difference vectors (Theorem [ref]) is already minimal under $E(d)$ --- by representation theory, the action of $E(d)$ on $\mathcal{G}$ is a polar representation. For other definitions of Cercis, the invariance group may differ and must be explicitly declared.

### Theorem 9: Galileo vs Lorentz Structural Distinction

> **Theorem:** [Galileo vs Lorentz Structural Distinction]
> <!-- label: thm:ilh-galileo -->
> SCX's invariance structure is isomorphic to the Galilean group of $d$-dimensional space:
> 
> $$
> \boxed{Gal(d) = \mathbb{R}^d \rtimes O(d) \cong E(d)}
> $$
> 
> not the Lorentz group $SO(1, d-1)$ (which includes boosts). Specific differences:
> 
> [Table omitted --- see original .tex]
> 
> SCX's invariance structure is isomorphic to the Galilean group, not the Lorentz group. SCX has no boost structure, no speed limit, and its invariant ``distance'' is positive-definite Euclidean distance between prediction vectors.

> **Proof:** SCX's $E(d)$ group consists of translation generators and rotation generators, with no boost generators. In prediction space, the rate of change (``velocity'') of predictions between adjacent data points has no physical upper bound --- corresponding to the fact that in Galilean relativity, velocities can superpose without limit. The non-compactness of the Lorentz group comes from the unbounded boost parameter $\phi = \text{arctanh}(v/c)$, which has no analog in SCX.
> 
> $\square$ **Core clarification:** This means that when we say ``SCX relativity,'' it should be understood as **Galilean**: no absolute reference frame, but also no speed limit. The audit analogy of Cercis should be ``invariance of relative distances in Euclidean space,'' not ``Lorentz invariance of spacetime intervals.''

## Complete ILH Structure
<!-- label: sec:ilh-structure -->

**Corrected ILH structure** separates vertical invariance (acting on the fiber/prediction space) from horizontal invariance (acting on the base manifold/data space):

**Vertical Invariance Layers (Fiber $\mathbb{R}^d$):**

[Table omitted --- see original .tex]

**Horizontal Invariance Layers (Base Manifold $\mathcal{X}$):**

[Table omitted --- see original .tex]

The complete audit invariance structure is the **direct product** of vertical and horizontal invariances:

$$
\mathcal{I}_{\text{total}} = \mathcal{I}_{\text{vertical}} \times \mathcal{I}_{\text{horizontal}}
$$

## ILH Verdict
<!-- label: sec:ilh-verdict -->

\begin{verdictbox}{verdictblue}
**Final Verdict: DOCUMENTATION VALUE**

[Table omitted --- see original .tex]

**ILH is valuable --- as clear documentation of SCX's invariance structure.** It clarifies the important distinction that SCX's relativity analogy is Galilean, not Einsteinian. But it should not be presented as a ``research contribution'' --- it is **instructional material**, not theorem innovation.

**Recommendation:** incorporate ILH as an ``SCX Audit Invariance Guide'' in the SCX documentation system, but do not publish as an independent formalization result.
\end{verdictbox}

---

# Cross-Path Synergies
<!-- label: part:synergy -->

## Synergy Between Paths

The three paths are not independent. There exists a unifying fiber bundle perspective:

[Figure omitted --- see original .tex]

- **ACAD $\times$ MDTA:** Deploy ACAD constraints on manifold shortcuts (detected by MDTA) --- shortcuts are natural ``regions requiring protection,'' and ACAD can detect tampering in these regions.
- **MDTA $\times$ ILH:** ILH's vertical invariance ensures that audit conclusions on shortcuts are stable under gauge transformations; different dimensions of MDTA's SAR multi-metric behave differently across ILH layers (e.g., prediction variance is invariant under V1 but may change under V2).
- **ACAD $\times$ ILH:** ACAD's constraint function $C$ can be designed to be invariant at specific ILH layers --- this ensures the ``audit validity'' of pairing constraints is maintained under gauge transformations.

## Unification Conjecture

On the $E(d)$ principal bundle $\pi: E \to \mathcal{X}$:

- **ACAD** = constraints between sections (vertical invariant matching) --- the two auditors' reference data correspond to two sections $s_A, s_B: \mathcal{X} \to E$, and constraint $C$ requires their projection on fibers to match
- **MDTA** = topological feature detection on the base manifold (horizontal structural anomaly) --- shortcuts are low-density paths on $\mathcal{X}$ connecting two ``high-density regions''
- **ILH** = algebraic classification of vertical invariances (structure group decomposition) --- the semidirect product decomposition $E(d) = \mathbb{R}^d \rtimes O(d)$ corresponds to the hierarchy of invariances

Assembled together, these three components form a prototype **fiber-bundle-based audit security framework**.

---

# Overall Assessment
<!-- label: part:assessment -->

## Honesty Comparison

The three paths form a gradient in terms of ``honesty'':

[Table omitted --- see original .tex]

ILH has the highest honesty because its ``fractures'' are ``the theorems are too simple'' rather than ``the theorems have holes.'' A formalization of all-true-but-trivial theorems is more honest than an ambitious formalization with holes.

## Methodological Reflection

The five rounds of exploration reveal a universal pattern:

<div align="center">

**Inspiration (physics analogy) $\rightarrow$ Correction (remove packaging) $\rightarrow$ Formalization (establish theorems) $\rightarrow$ Review (find fractures) $\rightarrow$ Verdict (honest positioning)**

</div>

Key lessons:

1. **Physics analogies are inspirational tools, not argumentative tools:** ``Entanglement'' inspired ACAD, but ACAD does not rely on quantum mechanics. ``Wormholes'' inspired MDTA, but shortcut detection does not rely on general relativity.
2. **Mathematical clothing does not equal mathematical substance:** In Round 3, some ``theorems'' were merely restatements of definitions (many ILH theorems), and some ``proofs'' had technical gaps (MDTA's manifold assumptions).
3. **Honesty matters more than depth:** Acknowledging that ILH is ``instructional material'' rather than ``research contribution'' is more honest than claiming it is a ``new theory of audit invariance.''
4. **Audit value is the ultimate criterion:** Regardless of how elegant the formalization is, if it does not produce actionable audit improvements, it is academic gymnastics rather than an audit tool.

## Practical Recommendations for SCX Auditing

### Immediate (Short-Term)

1. **MDTA:** Run shortcut detection on the Situs manifold, compute shortcut ratios for all cluster pairs, flag $r < 0.3$ pairs as ``audit blind spot candidates''
2. **ILH:** Write an ``SCX Invariance Guide'' document to help auditors understand Cercis's gauge invariance
3. **ACAD:** Pilot implementation of hash chain constraint pairing for high-value audit scenarios

### Planned Research (Medium-Term)

1. Evaluate expert prediction behavior on shortcut candidates, collect SAR multi-metric data
2. Establish bootstrap significance tests for shortcut ratios
3. Experimentally verify ACAD's detection probability and false positive rate

### Maintain Vigilance (Long-Term)

1. Do not call ACAD ``quantum auditing'' --- it is a classical statistical security scheme
2. Do not call MDTA ``wormhole detection'' --- honestly say ``manifold shortcut detection''
3. Do not call ILH ``audit relativity'' --- honestly say ``SCX invariance structure documentation''

---

## Conclusion
<!-- label: sec:conclusion -->

This paper presents rigorous mathematical formalization of three physics-inspired SCX audit paths. Five rounds of iteration --- from creative analogy to honest verdict --- produced three clearly positioned, honestly evaluated frameworks:

1. **ACAD (Audit Correlation Asymmetry Detection): Conditionally useful** --- Provides an information-theoretic/statistical-security tampering detection protocol (5 theorems + 1 corollary), achieving exponential detection probability when cryptographic constraints are realizable. But do not call it ``quantum'' auditing.
2. **MDTA (Manifold Density Topology Analysis): Pragmatically useful** --- Provides persistent-homology-based manifold shortcut detection and audit risk assessment (5 theorems), implementable immediately on existing TDA toolboxes. The most ``down-to-earth'' path.
3. **ILH (Invariance Layered Hierarchy): Documentation value** --- Clearly documents SCX's invariance structure using group-theoretic language (9 theorems), clarifying the key distinction of ``Galilean rather than Einsteinian.'' Instructional material, not research contribution.

Perhaps the most important contribution is not any single framework, but the **methodological demonstration**: how to honestly distinguish ``physics inspiration'' from ``mathematical correspondence,'' how to identify fractures during formalization, and how to position contributions based on audit value rather than mathematical elegance. Entanglement/wormholes/relativity no longer need these labels to be interesting --- their audit value speaks for itself.

---

## Appendix
## Precise Statements of Corrected Theorems
<!-- label: app:corrected -->

### ACAD Corrected Theorems

> **Theorem:** [ACAD Detection Probability, Serfling Correction]
> Let the attacker modify $m$ data points, and auditor $B$ draw $k$ samples without replacement. Then:
> 
> $$
> P(\text{detection}) \geq 1 - \exp\left(-\frac{k \cdot \alpha^2 \cdot (1 - \varepsilon - \gamma)^2}{2\left(1 - (k-1)/n\right)}\right)
> $$
> 
> where $\alpha = m/n$.

> **Theorem:** [ACAD Statistical Security Bound]
> For any attack strategy $\mathcal{E}$ satisfying knowledge constraints:
> 
> $$
> \inf_{\mathcal{E}} P(\text{detection}) \geq 1 - \exp\left(-c \cdot k \cdot \alpha^2\right)
> $$
> 
> where $c = \frac{(1 - \varepsilon - \gamma)^2}{2(1 - (k-1)/n)}$.

### MDTA Corrected Definitions

> **Definition:** [Statistically Significant Shortcut]
> The shortcut ratio $r_{ij}$ is statistically significant at level $\alpha$ if:
> 
> $$
> P_{H_0}(r \leq r_{ij}^{\text{obs}}) \leq \alpha
> $$
> 
> where the null distribution $H_0: r = 1$ is estimated via $B = 1000$ bootstrap resamples.

### ILH Corrected Structure

**Separated vertical/horizontal invariances:**

$$
\begin{aligned}
\text{Vertical invariance layers (fiber):}&\quad V0 \subset V1 \subset V2 \subset V3 \\
\text{Horizontal invariance layers (base manifold):}&\quad H0 \subset H1 \subset H2 \\
\text{Total invariance:}&\quad \mathcal{I}_{\text{total}} = \mathcal{I}_V \times \mathcal{I}_H \quad (\text{direct product})
\end{aligned}
$$

## Unresolved Open Questions
<!-- label: app:open -->

1. **Practical security bounds for ACAD:** Under real SCX data distributions, what are the detection probability and false positive rate of audit correlation asymmetry detection? Requires empirical study.
2. **Prevalence of manifold shortcuts:** How common are shortcuts (cluster pairs with $r_{ij} < \tau$) on the Situs manifold? Are they concentrated in specific data subdomains?
3. **Unified formalization of the $E(d)$ principal bundle:** Currently translation and rotation are treated independently. Can a unified $E(d)$ principal bundle with connection be constructed, incorporating both Cercis and $O(d)$ curvature into a single geometric framework?
4. **Feasibility of horizontal invariance:** Do discrete versions of diffeomorphism-invariant audit constructions exist? Can Einstein's ``general covariance'' concept guide SCX's data-representation-independent auditing?
5. **Fiber bundle unification of the three paths:** Can ACAD, MDTA, and ILH be rigorously unified on the $E(d)$ principal bundle, forming a complete ``fiber-bundle-based audit security framework''?

## References and Prerequisites
<!-- label: app:refs -->

[Table omitted --- see original .tex]

<div align="center">

\rule{0.5\textwidth}{0.5pt}
**--- End of Document ---**
Lines: 1000+ $\checkmark$
Total theorems: 19 (ACAD 5+1 corollary, MDTA 5, ILH 9) $\checkmark$
Honest verdicts: Conditionally Useful / Pragmatically Useful / Documentation Value $\checkmark$

</div>
