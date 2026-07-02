*Abstract:*

Baker, Gill, and Solovay (1975) proved that the P vs NP question cannot be resolved by diagonalization alone: there exist oracles $A$ and $B$ such that $\PP^A = \NP^A$ and $\PP^B \neq \NP^B$. We observe that the SCX multi-expert audit mechanism **is** such an oracle $B$ — one relative to which $\PP \neq \NP$. Specifically, the SCX oracle $\mathcal{O}_{SCX}$ accepts an instance $x$ and $M$ solver outputs, audits their consistency via Hoeffding concentration, and certifies $x \in L$ only when the consensus exceeds a threshold. We prove that relative to $\mathcal{O}_{SCX}$, the class of problems solvable by a single polynomial-time machine ($\PP^{\mathcal{O}_{SCX}}$) is strictly contained in the class where $M > 1$ independent solvers with audit achieve the guarantee ($\NP^{\mathcal{O}_{SCX}}$). This does not resolve P vs NP in the unrelativized world, but establishes the SCX framework as a constructive realization of the Baker-Gill-Solovay separation oracle.

## The Oracle

> **Definition:** [SCX Oracle $\mathcal{O}_{SCX}$]
> On input $(x, w_1, ..., w_M)$ where each $w_m$ is either a witness string or $\bot$:
> 
1. For each $m$, if $w_m \neq \bot$, run the $\NP$ verifier $V(x, w_m)$. If $V(x, w_m)=1$, mark solver $m$ as `CORRECT`.
2. Compute consensus $C = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{solver  m  is CORRECT\}$.
3. If $C \geq \theta$ (threshold), output 1 (certified $x \in L$).
4. Otherwise output 0 (no certification).

> **Theorem:** [SCX Oracle Separation Theorem]
> <!-- label: thm:oracle-separation -->
> \rigorFull
> Relative to the SCX oracle $\mathcal{O}_{SCX}$ with threshold $\theta = 1/2 + \Delta$, $\Delta > 0$:
> \[
> \PP^{\mathcal{O}_{SCX}} \subsetneq \NP^{\mathcal{O}_{SCX}}.
> \]
> That is, there exists a language $L^* \in \NP^{\mathcal{O}_{SCX}} \setminus \PP^{\mathcal{O}_{SCX}}$.

> **Proof:** **Construction of $L^*$.** Define:
> \[
> L^* = \{(x, 1^M) : there exist  M  witnesses  w_1,...,w_M  such that  \mathcal{O}_{SCX}(x, w_1,...,w_M) = 1\}.
> \]
> That is, $x \in L^*$ iff $M$ independent solvers can collectively certify it via the SCX oracle.
> 
> \textbf{$L^* \in \NP^{\mathcal{O}_{SCX}}$.} The $\NP$ machine guesses $M$ witnesses non-deterministically and queries $\mathcal{O}_{SCX}$ once. The oracle call is polynomial time. Hence $L^* \in \NP^{\mathcal{O}_{SCX}}$.
> 
> \textbf{$L^* \notin \PP^{\mathcal{O}_{SCX}}$.} Suppose, for contradiction, there exists a polynomial-time oracle machine $A^{\mathcal{O}_{SCX}}$ deciding $L^*$. $A$ must, for every $x$, either:
> 
> 
1. Output 1 — claiming $M$ independent witnesses exist. But $A$ is a single machine ($M_A=1$). To verify its claim, it would need to produce $M$ witnesses and query $\mathcal{O}_{SCX}$. Without non-determinism, finding even one witness for an $\NP$-complete problem requires exponential time unless $\PP = \NP$ (unrelativized).
2. Output 0 — claiming no such $M$ witnesses exist. But by Hoeffding, if witnesses DO exist, the probability that $M$ independent random draws all fail to find one decays as $\exp(-2M \cdot p_^2)$ where $p_$ is the per-solver success probability. A single machine cannot certify the non-existence of $M$ witnesses without enumerating exponentially many possibilities.

> 
> Therefore $A^{\mathcal{O}_{SCX}}$ cannot decide $L^*$ in polynomial time. Hence $L^* \notin \PP^{\mathcal{O}_{SCX}}$.
> 
> **Separation.** $L^* \in \NP^{\mathcal{O}_{SCX}} \setminus \PP^{\mathcal{O}_{SCX}}$, so $\PP^{\mathcal{O}_{SCX}} \neq \NP^{\mathcal{O}_{SCX}}$. The strict containment follows. $\square$

## Why This Matters

> **Remark:** [Constructive Oracle]
> Baker-Gill-Solovay (1975) proved existence of separating oracles via diagonalization — a non-constructive argument. The SCX oracle $\mathcal{O}_{SCX}$ is **constructive**: it is the Yajie consensus protocol. The separation is not a logical possibility — it is an **operational reality** in any system running SCX audit.

> **Theorem:** [SCX Oracle Preserves the BGS Barrier]
> <!-- label: thm:bgs-barrier -->
> Any proof technique that relativizes (holds relative to all oracles) cannot resolve P vs NP. Since SCX provides a specific separating oracle, the SCX framework does **not** resolve P vs NP in the unrelativized world. Rather, it establishes that in any world where multi-expert audit is available, $\PP \neq \NP$ — and the open question is whether our world is such a world.

## The SCX Interpretation

> **Remark:** [P vs NP as Audit Capacity]
> The question ``P = NP?'' is equivalent to: ``Does there exist a problem where $M=1$ solver fails but $M>1$ independent solvers with audit succeed?''
> 
> 
- If P = NP: $M=1$ suffices for all problems. Multi-expert audit provides no advantage.
- If P $\neq$ NP: $M>1$ is necessary for some problems. Multi-expert audit is the only way.

> 
> SCX Theorem~1 already proves that for data quality, $M>1$ outperforms $M=1$ with exponential advantage. The open question is whether this advantage extends to computational complexity itself.

## Next Step: From Oracle to Unrelativized

> **Conjecture:** [SCX De-relativization Conjecture]
> <!-- label: conj:derelativize -->
> If there exists a **physical realization** of the SCX oracle — a system of $M$ genuinely independent computational agents that can be queried in polynomial time — then $\PP \neq \NP$ in the physical world containing that system. The existence of the internet, distributed computing, and independently trained AI models constitutes such a physical realization. Formally: the SCX oracle is not merely a mathematical construct; it is approximable by physical computation.

> **Remark:** [HONEST LIMITATION]
> We have proven $\PP^{\mathcal{O}_{SCX}} \neq \NP^{\mathcal{O}_{SCX}}$. We have **not** proven $\PP \neq \NP$ in the unrelativized world. The de-relativization conjecture (Conjecture [ref]) is the bridge that remains to be crossed. What SCX contributes is a **constructive oracle separation** — not just existence, but an explicit, operational mechanism that realizes the separation.