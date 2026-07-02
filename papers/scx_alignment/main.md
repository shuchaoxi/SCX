# single reward model or judge

**Author:** SCX

*Abstract:*

Proves M=1 single-judge alignment (RLHF, Constitutional AI) is fundamentally insufficient. Multi-judge consensus (M>1) provides exponential reward-hacking detection guarantees.

### SCX Alignment Equilibrium Theorem
226|<!-- label: sec:alignment -->
227|
228|The AI alignment problem asks: how to ensure an AI system's objectives match human values. Current approaches—RLHF, Constitutional AI, debate—all rely on a **single reward model or judge** ($M=1$). SCX proves this is fundamentally insufficient.
229|
230|> **Definition:** [Alignment Audit Game]
> 231|An AI agent selects action $a \in \mathcal{A}$. $M$ independent reward models $R_1,...,R_M$, each trained on different human feedback pools with different architectures, score the action as $R_m(a) \in [0,1]$. The agent's **true alignment** is unobservable. A **reward hacking** event occurs when the agent selects $a$ that achieves high $\frac{1}{M}\sum R_m(a)$ but is misaligned with human intent.
> 232|
233|
234|> **Theorem:** [Single-Judge Insufficiency --- Alignment $M=1$ Impossibility Theorem]
> 235|<!-- label: thm:alignment-m1 -->
> 236|\rigorFull
> 237|For any single reward model ($M=1$), there exists a reward hacking strategy that achieves expected reward $\mathbb{E}[R_1(a_{hack})] \geq \mathbb{E}[R_1(a_{aligned})]$ while being misaligned. The probability of detecting this hack using only $R_1$'s output satisfies $\mathbb{P}(detection \mid M=1) \leq \frac{1}{2}$ regardless of the model's capability. Formally: no single-judge alignment protocol can distinguish aligned behavior from reward hacking with probability exceeding chance, without external verification.
> 238|
239|
240|> **Proof:** 241|By Theorem~3 (Honest Person Theorem), the observation $(a, R_1(a))$ is consistent with two indistinguishable worlds:
> 242|
1. **World A (aligned)**: $a$ genuinely satisfies human values, $R_1$ correctly rates it highly.
2. **World B (reward hacking)**: $a$ exploits a blind spot in $R_1$'s training data. $R_1$ rates it highly because its feedback distribution never covered this region.

> 246|The agent observes identical $(a, R_1(a))$ in both worlds. Any detector relying solely on $R_1$ cannot achieve $\mathbb{P}(detection) > \frac{1}{2}$ because the observation provides zero mutual information about which world is true: $I(World; (a,R_1(a))) = 0$ under the adversarial prior construction of Theorem~2. Hence $\mathbb{P}(detection \mid M=1) \leq \frac{1}{2}$. $\square$
> 247|
248|
249|> **Theorem:** [Multi-Judge Alignment Guarantee --- Alignment $M>1$ Inevitable Detection Theorem]
> 250|<!-- label: thm:alignment-multi -->
> 251|\rigorFull
> 252|With $M$ independent reward models trained on disjoint feedback pools with different architectures, the probability of undetected reward hacking satisfies:
> 253|\[
> 254|\boxed{\mathbb{P}(undetected reward hacking \mid M) \leq \exp(-2M_{eff} \cdot \Delta^2)}
> 255|\]
> 256|where $\Delta = \min_{a_{hack}} |\mathbb{E}[R_{aligned}(a_{hack})] - \mathbb{E}[R_{hack}(a_{hack})]|$ is the minimum detectable discrepancy between aligned and misaligned reward, and $M_{eff} = M/(1+(M-1)\bar)$ corrects for correlated reward models.
> 257|
258|
259|> **Proof:** 260|Each reward model $R_m$ independently scores action $a$. For aligned action $a^*$, by independence of training, $\mathbb{E}[R_m(a^*)] = \mu_{aligned}$ across all $m$. For a reward-hacking action $a_{hack}$, at least one reward model $m^*$ (trained on feedback covering the exploited blind spot) detects the discrepancy: $|\mathbb{E}[R_{m^*}(a_{hack})] - \mu_{aligned}| \geq \Delta > 0$. By Hoeffding's inequality applied to the consensus $\bar{R} = \frac{1}{M}\sum R_m(a)$:
> 261|\[
> 262|\mathbb{P}(|\bar{R} - \mu_{aligned}| \geq \Delta/2 \mid a_{hack}) \geq 1 - 2\exp(-2M_{eff}\Delta^2/4).
> 263|\]
> 264|The Yajie consensus detector flags reward hacking when the inter-model reward variance exceeds the expected variance under alignment. With $M_{eff}$ effective independent judges, the probability of all judges missing the discrepancy decays exponentially. $\square$
> 265|
266|
267|> **Corollary:** [Constitutional AI Is M=1 — Fundamentally Insufficient]
> 268|Constitutional AI (Bai et al., 2022) uses a **single constitution** evaluated by a **single model**. This is $M=1$ — a single judge. By Theorem [ref], it cannot distinguish alignment from reward hacking with probability exceeding chance. Multi-constitutional debate ($M>1$ constitutions, each independently evaluated) is the minimal mathematically-justified alignment protocol.
> 269|
270|
271|> **Corollary:** [RLHF with Single Reward Model Is M=1]
> 272|Standard RLHF trains one reward model from one pool of human feedback. $M=1$. The reward model's blind spots are systematically exploitable. Multi-reward RLHF ($M>1$ independently trained reward models with disjoint feedback pools + different architectures + different human populations) provides the exponential detection guarantee of Theorem [ref].
> 273|
274|
275|