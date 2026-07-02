#!/usr/bin/env python3
"""
Translate remaining Chinese / [ZH] placeholders in yajie_protocol/main.tex to English.
Handles lines 320-2124.
"""
import re

TRANSLATIONS = [
    # === Theorem 2: Asymptotic Uniqueness (lines 320-352) ===
    (r'\\begin\{theorem\}\[\[ZH\]CEC\[ZH\]\]',
     r'\\begin{theorem}[Asymptotic Uniqueness of the Non-Proliferation Equilibrium and the CEC Critical Threshold]'),
    (r'\[ZH\]A1--A7\[ZH\]：',
     r'Under Assumptions A1--A7:'),
    (r'\[ZH\]\\textbf\{CEC\[ZH\]\} \$\\|\mathcal\{E\}\\|\\^\*\$，\[ZH\]：',
     r'There exists a unique \textbf{CEC critical size} $|\mathcal{E}|^*$, defined as:'),
    (r'\[ZH\] \$\\Delta\(0\) \\geq \\lambda - \\kappa\$，\[ZH\] \$\\|\mathcal\{E\}\\|\\^\* = 0\$（\[ZH\]）。\[ZH\]，\[ZH\] \$\\theta\(\\cdot\)\$ \[ZH\] \$V\(\\cdot\)\$ \[ZH\]，\$\\|\mathcal\{E\}\\|\\^\*\$ \[ZH\]。',
     r'If $\Delta(0) \geq \lambda - \kappa$, then $|\mathcal{E}|^* = 0$ (the protocol locks in the market from its initial release). Otherwise, by the continuity and strict monotonicity of $\theta(\cdot)$ and $V(\cdot)$, $|\mathcal{E}|^*$ is a well-defined positive real number.'),
    (r'\[ZH\] \$\\|\mathcal\{E\}\\| > \\|\mathcal\{E\}\\|\\^\*\$，\$s\\^\* = \(A, \\ldots, A\)\$ \[ZH\] \$\\Gamma\^\{NP\}\$ \[ZH\]\\textbf\{\[ZH\]\}\[ZH\]——\[ZH\]，\[ZH\]。',
     r'For all $|\mathcal{E}| > |\mathcal{E}|^*$, $s^* = (A, \ldots, A)$ is the \textbf{unique} Nash equilibrium of the game $\Gamma^{\text{NP}}$—no other pure-strategy equilibrium and no mixed-strategy equilibrium exists.'),
    (r'CEC\[ZH\]：',
     r'The explicit solution for the CEC critical threshold is:'),
    (r'\[ZH\] \$\\theta\\^\* = V\^\{-1\}\\left\(V\[\\theta\(0\)\] \+ c\^\{adopt\} \- c\^\{develop\} \- \\kappa \+ \\lambda \- \\kappa\\right\)\$，\$V\^\{-1\}\$ \[ZH\] \$V\$ \[ZH\]（\[ZH\]A1\[ZH\]）。',
     r'where $\theta^* = V^{-1}\left(V[\theta(0)] + c^{\text{adopt}} - c^{\text{develop}} - \kappa + \lambda - \kappa\right)$, and $V^{-1}$ is the inverse function of $V$ (whose existence is guaranteed by the strict monotonicity in A1).'),
    
    # Proof of Theorem 2
    (r'\\textbf\{\(i\)\} \[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\] \$\[0, \\infty\)\$ \[ZH\]（A1--A2\[ZH\] \$V \\circ \\theta\$ \[ZH\]）\[ZH\]：',
     r'\textbf{(i)} The function $\Delta(|\mathcal{E}|)$ is continuous on $[0, \infty)$ (A1--A2 guarantee that $V \circ \theta$ is continuous) and strictly increasing:'),
    (r'\[ZH\] \$V\' > 0\$（A1）\[ZH\] \$\\theta\' > 0\$（A2）。\[ZH\]\$\\inf\$\[ZH\]。',
     r'where $V' > 0$ (A1) and $\theta' > 0$ (A2). The infimum definition yields a unique critical value.'),
    (r'\\textbf\{\(ii\)\} \[ZH\] \$\\|\mathcal\{E\}\\| > \\|\mathcal\{E\}\\|\\^\*\$，\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\) > \\lambda - \\kappa\$（\[ZH\]）。\[ZH\]\\ref\{thm:npe-complete\}\[ZH\]\(ii\)\[ZH\] \$\(A, \\ldots, A\)\$ \[ZH\]。\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\) \\leq -\(n-1\)\\kappa\$ \[ZH\]（\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\) > \\lambda - \\kappa > 0 > -\(n-1\)\\kappa\$，\[ZH\]A4 \$\\lambda > \\kappa > 0\$）。\[ZH\]，\[ZH\]，\[ZH\]。\[ZH\] \$\(A, \\ldots, A\)\$ \[ZH\]。',
     r'\textbf{(ii)} When $|\mathcal{E}| > |\mathcal{E}|^*$, by definition $\Delta(|\mathcal{E}|) > \lambda - \kappa$ (strict inequality). Theorem~\ref{thm:npe-complete}(ii) guarantees that $(A, \ldots, A)$ is a strict Nash equilibrium. The universal-development equilibrium condition $\Delta(|\mathcal{E}|) \leq -(n-1)\kappa$ does not hold (since $\Delta(|\mathcal{E}|) > \lambda - \kappa > 0 > -(n-1)\kappa$, by A4 $\lambda > \kappa > 0$). A mixed-strategy equilibrium requires the indifference condition to hold, but under a strict Nash equilibrium the expected payoff from deviation is strictly less than the equilibrium payoff, so the indifference condition cannot be satisfied. Hence $(A, \ldots, A)$ is the unique equilibrium.'),
    (r'\\textbf\{\(iii\)\} \[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\) = \\lambda - \\kappa\$ \[ZH\] \$\\theta\\^\*\$，\[ZH\]A2\[ZH\]。',
     r'\textbf{(iii)} Solving $\Delta(|\mathcal{E}|) = \lambda - \kappa$ for $\theta^*$ and substituting the functional form from A2 yields the explicit solution.'),
    
    # Corollary 1: self-reinforcing
    (r'\\begin\{corollary\}\[\[ZH\]\]',
     r'\\begin{corollary}[Monotonic Self-Reinforcing Property of the Non-Proliferation Equilibrium]'),
    (r'\[ZH\]A1--A7\[ZH\]，\[ZH\]\\textbf\{\[ZH\]\}：',
     r'Under Assumptions A1--A7, define the \textbf{stability margin} of the non-proliferation equilibrium:'),
    (r'\[ZH\]：',
     r'Then:'),
    (r'\$M\(\\|\mathcal\{E\}\\|\)\$ \[ZH\] \$\[0, \\infty\)\$ \[ZH\]：\$M\'\(\\|\mathcal\{E\}\\|\) = V\'\[\\theta\(\\|\mathcal\{E\}\\|\)\] \\cdot \\theta\'\(\\|\mathcal\{E\}\\|\) > 0\$；',
     r'$M(|\mathcal{E}|)$ is strictly increasing on $[0, \infty)$: $M'(|\mathcal{E}|) = V'[\theta(|\mathcal{E}|)] \cdot \theta'(|\mathcal{E}|) > 0$;'),
    (r'\[ZH\] \$\\Delta \\|\mathcal\{E\}\\| > 0\$ \[ZH\]CEC，\[ZH\]：\(a\) \[ZH\]（\$\\partial u_i\(A, \\cdot\) / \\partial \\|\mathcal\{E\}\\| > 0\$），\(b\) \[ZH\]（\$M\(\\|\mathcal\{E\}\\|\)\$ \[ZH\]），\(c\) \[ZH\] \$p\\^\*\$ \[ZH\]（\[ZH\]）。',
     r'Each audit cycle expands the CEC by $\Delta |\mathcal{E}| > 0$, simultaneously: (a) increasing the attractiveness of adoption ($\partial u_i(A, \cdot) / \partial |\mathcal{E}| > 0$), (b) increasing the relative loss from deviation ($M(|\mathcal{E}|)$ grows), and (c) reducing the uncertainty of the adoption probability $p^*$ in mixed-strategy equilibria (when the equilibrium is pure-strategy, the uncertainty goes to zero).'),
    (r'\[ZH\]——\[ZH\]——\[ZH\]\\textit\{\[ZH\]\}\[ZH\]。',
     r'This property—that the stability of the equilibrium is self-reinforcing as it is achieved—is the precise game-theoretic expression of the \textit{time-accumulated advantage} mechanism.'),
    
    # Proof of Corollary 1
    (r'\[ZH\]\\ref\{thm:npe-complete\}\[ZH\]\\ref\{thm:asymptotic-uniqueness\}\[ZH\]A1--A2\[ZH\]。',
     r'Direct verification from Theorems~\ref{thm:npe-complete} and~\ref{thm:asymptotic-uniqueness} combined with the monotonicity properties of A1--A2.'),
    
    # Corollary 2: first-mover decay
    (r'\\begin\{corollary\}\[\[ZH\] \(Temporal Decay of First-Mover Advantage\)\]',
     r'\\begin{corollary}[Temporal Decay of First-Mover Advantage]'),
    (r'\[ZH\]A1--A7\[ZH\]。\[ZH\]：',
     r'Under Assumptions A1--A7. Define the following quantities:'),
    (r'\\begin\{definition\}\[\[ZH\]\]',
     r'\\begin{definition}[Normalized First-Mover Advantage Intensity]'),
    (r'\[ZH\]（CEC\[ZH\] \$\\|\mathcal\{E\}\\|\$）\[ZH\]CEC\[ZH\]\\textbf\{\[ZH\]\}\[ZH\]：',
     r'The \textbf{absolute accuracy advantage} of the first mover (with CEC size $|\mathcal{E}|$) relative to a zero-CEC late mover is:'),
    (r'\\textbf\{\[ZH\]\}——\[ZH\]——\[ZH\]：',
     r'The \textbf{normalized first-mover advantage intensity}—i.e., the ratio of the first-mover advantage to the maximum possible advantage—is:'),
    (r'\[ZH\]：',
     r'The following propositions hold:'),
    (r'\\textbf\{\[ZH\]：\} \[ZH\] \$\\delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\]（\$\\delta\'\(\\|\mathcal\{E\}\\|\) = \\gamma\(\\theta_\{\\max\} - \\theta_0\)e\^\{-\\gamma \\|\mathcal\{E\}\\|\} > 0\$），\[ZH\]\\textit\{\[ZH\]\}\[ZH\]：',
     r'\textbf{Diminishing marginal returns and asymptotic saturation of the absolute advantage:} The first mover\'s absolute accuracy advantage $\delta(|\mathcal{E}|)$ is monotonically increasing ($\delta'(|\mathcal{E}|) = \gamma(\theta_{\max} - \theta_0)e^{-\gamma |\mathcal{E}|} > 0$), but its \textit{marginal increment} strictly decreases to zero:'),
    (r'\[ZH\]：',
     r'and the absolute advantage converges to a finite upper bound:'),
    (r'\\textbf\{\[ZH\]：\[ZH\]——CEC\[ZH\]（\[ZH\]）。\[ZH\]，\[ZH\]，\[ZH\] \$\\theta_\{\\max\} - \\theta_0\$。\}',
     r'\textbf{Economic meaning: first-mover advantage does not grow without bound—the accuracy contribution of the CEC has a hard upper limit (determined by the theoretical detection capability of the audit modules). Below this ceiling, no matter how much audit history the first mover accumulates, its accuracy advantage cannot exceed $\theta_{\max} - \theta_0$.}'),
    (r'\\textbf\{\[ZH\]：\} \[ZH\] \$\\delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\]（\[ZH\]\\ref\{eq:adoption-advantage-def\}）：',
     r'\textbf{Marginal decay of the adoption advantage:} Substituting $\delta(|\mathcal{E}|)$ into the definition of $\Delta(|\mathcal{E}|)$ (equation~\ref{eq:adoption-advantage-def}):'),
    (r'\[ZH\]A1（\$V\$ \[ZH\]），\$\\Delta\'\(\\|\mathcal\{E\}\\|\) = V\'\[\\theta\(\\|\mathcal\{E\}\\|\)\] \\cdot \\delta\'\(\\|\mathcal\{E\}\\|\) > 0\$ \[ZH\] \$\\Delta\'\'\(\\|\mathcal\{E\}\\|\) < 0\$。\[ZH\]（\$\\delta\' \\to 0\$）\[ZH\]（\$V\' \\to 0\$ \[ZH\] \$\\theta \\to \\theta_\{\\max\}\$）。\[ZH\]：',
     r'By Assumption A1 ($V$ is strictly concave), $\Delta'(|\mathcal{E}|) = V'[\theta(|\mathcal{E}|)] \cdot \delta'(|\mathcal{E}|) > 0$ and $\Delta''(|\mathcal{E}|) < 0$. The marginal growth of the adoption advantage is simultaneously constrained by diminishing marginal returns to accuracy ($\delta' \to 0$) and diminishing marginal returns to value ($V' \to 0$ as $\theta \to \theta_{\max}$). Hence:'),
    (r'\\textbf\{\[ZH\]：\[ZH\]CEC\[ZH\]——\[ZH\]。\}',
     r'\textbf{Economic meaning: the first mover\'s ability to expand its adoption advantage by continuing to accumulate CEC diminishes over time—the marginal contribution of additional audit cycles to equilibrium stability converges to zero.}'),
    (r'\\textbf\{CEC\[ZH\]（\[ZH\]）：\} CEC\[ZH\]\\textit\{\[ZH\]\}（additive public good）：\(a\) \\textbf\{\[ZH\]\}——\[ZH\]CEC\[ZH\]（\$\\Delta \\|\mathcal\{E\}\\| > 0\$），CEC\[ZH\]（\[ZH\]M4）；\(b\) \\textbf\{\[ZH\]\}——CEC\[ZH\]、\[ZH\]\\textit\{\[ZH\]\}\[ZH\]：\[ZH\] \$i\$ \[ZH\] \$j\$ \[ZH\]。',
     r'\textbf{CEC as an additive public good (the core mechanism of temporal decay):} The essence of the CEC is that of an \textit{additive public good}: (a) \textbf{Additivity}—each audit cycle appends new entries to the CEC ($\Delta |\mathcal{E}| > 0$), and the CEC size is non-decreasing (Assumption M4); (b) \textbf{Publicness}—the anomaly registers, calibration parameters, and quality fingerprints stored in the CEC are \textit{non-rivalrous} knowledge: jurisdiction $i$\'s use of a particular calibration datum does not diminish jurisdiction $j$\'s ability to use the same datum.'),
    (r'\[ZH\]CEC\[ZH\] \$T\\^\*\$ \[ZH\]——\[ZH\]（\[ZH\]6\[ZH\]1\[ZH\]IDAA）。\[ZH\] \$t > T\\^\*\$，\[ZH\] \$\\|\mathcal\{E\}_t\^\{public\}\\|\$ \[ZH\]CEC\[ZH\]。\[ZH\] \$\\theta\(\\|\mathcal\{E\}_t\\|\) - \\theta\(0\)\$ \[ZH\] \$\\theta\(\\|\mathcal\{E\}_t\\|\) - \\theta\(\\|\mathcal\{E\}_t\^\{public\}\\|\)\$。\[ZH\]\\textbf\{\[ZH\]\}：',
     r'Suppose the CEC is internationalized at time $T^*$—i.e., transformed through a multilateral governance mechanism into a global public infrastructure equally accessible to all jurisdictions (see Section~6, Recommendation~1 on the IDAA). For any $t > T^*$, let $|\mathcal{E}_t^{\text{public}}|$ be the CEC size that any late-moving jurisdiction can immediately access. The cold-start penalty of a late mover shrinks from $\theta(|\mathcal{E}_t|) - \theta(0)$ to $\theta(|\mathcal{E}_t|) - \theta(|\mathcal{E}_t^{\text{public}}|)$. Define the \textbf{late-mover penalty ratio}:'),
    (r'\$\\Psi\(T\\^\*; T\\^\*\) = 1\$（\[ZH\]，\[ZH\]CEC\[ZH\]，\[ZH\]）。\[ZH\] \$\\|\mathcal\{E\}_t\^\{public\}\\| \\to \\|\mathcal\{E\}_t\\|\$（\[ZH\]CEC\[ZH\]CEC），\$\\Psi \\to 0\$。\[ZH\]（\$\\|\mathcal\{E\}_t\^\{public\}\\| = \\|\mathcal\{E\}_t\\|\$），\$\\Psi \\equiv 0\$——\[ZH\]。',
     r'$\Psi(T^*; T^*) = 1$ (at the moment of internationalization, the late mover has not yet accessed the public portion of the CEC, so the penalty is complete). But as $|\mathcal{E}_t^{\text{public}}| \to |\mathcal{E}_t|$ (the public CEC catches up to the first mover\'s private CEC), $\Psi \to 0$. Under ideal internationalization ($|\mathcal{E}_t^{\text{public}}| = |\mathcal{E}_t|$), $\Psi \equiv 0$—the first-mover advantage is completely eliminated at the adoption level.'),
    (r'\[ZH\]，\[ZH\]。\[ZH\]\\textit\{\[ZH\]\}\[ZH\]：\(a\) \\textbf\{\[ZH\]\}——\[ZH\]、\[ZH\]（\[ZH\]\\ref\{thm:absorption\}\[ZH\]）；\(b\) \\textbf\{\[ZH\]\}——CEC\[ZH\]，\[ZH\]。',
     r'However, complete elimination applies only to the accuracy dimension of a single audit. The first mover retains two \textit{non-internationalizable} residual advantages: (a) \textbf{the temporal depth of ecosystem inertia}—the first mover\'s adopter network, regulatory recognition, and institutional embedding possess incompressible historical depth (the stage lock-in of Theorem~\ref{thm:absorption}); (b) \textbf{the path-dependence of operational standard-setting authority}—the anomaly adjudication thresholds and calibration parameter configurations in the CEC reflect the first mover\'s initial data characteristics, and these features remain as historical anchors of the operational standard even after internationalization.'),
    (r'\\textbf\{\[ZH\]：\} \[ZH\]\\textbf\{\[ZH\]\} \$T_\{1/2\}\^\{Delta\}\$ \[ZH\]：',
     r'\textbf{Half-life of first-mover advantage:} Define the \textbf{adoption half-life} $T_{1/2}^{\Delta}$ as the time satisfying:'),
    (r'\[ZH\]NPE\[ZH\]（\[ZH\]\\ref\{cor:self-reinforcing\}）\[ZH\]。\[ZH\]A2\[ZH\]，\$T_\{1/2\}\^\{Delta\}\$ \[ZH\]：',
     r'i.e., the NPE stability margin (Corollary~\ref{cor:self-reinforcing}) drops to one-half of its value at the moment of internationalization. Under the functional form of A2, $T_{1/2}^{\Delta}$ satisfies the implicit equation:'),
    (r'\[ZH\] \$V \\circ \\theta\$ \[ZH\] \$\\Delta\(\\cdot\)\$ \[ZH\]。\[ZH\]：\\textbf\{\[ZH\]，\[ZH\]。\}',
     r'The existence of the half-life is guaranteed by the continuity of $V \circ \theta$ and the monotone boundedness of $\Delta(\cdot)$. Its finiteness implies: \textbf{first-mover advantage is not a permanent structure but a phased phenomenon with a clearly defined temporal boundary.}'),
    (r'\\textbf\{\[ZH\]——NPE\[ZH\]：\} \[ZH\]\\ref\{thm:npe-complete\}\[ZH\]\\ref\{cor:self-reinforcing\}\[ZH\]\"\[ZH\]CEC\[ZH\]\"\[ZH\]，\[ZH\]CEC\[ZH\]，\[ZH\]：NPE\[ZH\]CEC\[ZH\]\\textit\{\[ZH\]\}\[ZH\]。\[ZH\]CEC\[ZH\]（\[ZH\]IDAA\[ZH\]），\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\]——\[ZH\] \$\\theta\(\\|\mathcal\{E\}_t\^\{private\}\\|\) - \\theta\(\\|\mathcal\{E\}_t\^\{public\}\\|\)\$ \[ZH\]——\[ZH\]。\[ZH\]，\[ZH\]\"\[ZH\]\"\[ZH\]\"\[ZH\]\"——\[ZH\]CEC\[ZH\]，\[ZH\] \$\\lambda\$ \[ZH\]，\[ZH\]CEC\[ZH\]CEC\[ZH\]。',
     r'\textbf{Honest strike—normative correction of the NPE:} The conclusion established by Theorem~\ref{thm:npe-complete} and Corollary~\ref{cor:self-reinforcing}—that ``the equilibrium self-reinforces as the CEC grows''—must be qualified as follows once the CEC is analyzed as an additive public good: the self-reinforcement of the NPE occurs only under the condition that the CEC is \textit{exclusively held}. Once the CEC is internationalized (through the IDAA or an equivalent multilateral mechanism), the component of the adoption advantage $\Delta(|\mathcal{E}|)$ that is specific to the first mover—namely, the $\theta(|\mathcal{E}_t^{\text{private}}|) - \theta(|\mathcal{E}_t^{\text{public}}|)$ term—tends to zero. At this point, the motivation for adoption shifts from ``developing an alternative protocol is not worth it'' to ``developing an alternative protocol is unnecessary''—all jurisdictions benefit equally from the global CEC infrastructure, the public-bads effect of fragmentation $\lambda$ continues to deter proliferation, but the basis of deterrence shifts from the first mover\'s private CEC monopoly to the universal availability of the CEC as a global public good.'),
    (r'\[ZH\]，NPE\[ZH\]\\textit\{\[ZH\]\}\[ZH\]\\textit\{\[ZH\]\}\[ZH\]。\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\^\{private\}\\|\) \\geq \\lambda - \\kappa\$ \[ZH\]（\[ZH\]NPE）；\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\^\{public\}\\|\) \\geq \\lambda - \\kappa\$ \[ZH\]（\[ZH\]NPE），\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\^\{public\}\\|\)\$ \[ZH\]——\[ZH\]，\[ZH\]CEC\[ZH\]（\[ZH\]）。',
     r'In other words, the NPE undergoes an institutional transformation from a \textit{first-mover monopoly deterrence} regime to a \textit{public-good coordination equilibrium}. Before the transformation, the equilibrium is sustained by $\Delta(|\mathcal{E}^{\text{private}}|) \geq \lambda - \kappa$ (first-mover monopoly NPE); after the transformation, it is sustained by $\Delta(|\mathcal{E}^{\text{public}}|) \geq \lambda - \kappa$ (public-good NPE), where $\Delta(|\mathcal{E}^{\text{public}}|)$ is identical for all jurisdictions—the first mover\'s identity-based advantage disappears; only the CEC\'s scale advantage remains (which is a public good shared by all jurisdictions).'),
    (r'\\textbf\{\[ZH\]\"\[ZH\]\"\[ZH\]——\[ZH\]5.2.2\[ZH\]。\}',
     r'\textbf{This is the game-theoretic foundation of ``Universal Harmony''—see Section~5.2.2 for the full formalization.}'),
    
    # Proof of Corollary 2 
    (r'\\textbf\{\(i\)--\(ii\)\} \[ZH\]。\[ZH\]A2，\$\\theta\'\(\\|\mathcal\{E\}\\|\) = \\gamma\(\\theta_\{\\max\} - \\theta_0\)e\^\{-\\gamma \\|\mathcal\{E\}\\|\} > 0\$，\$\\theta\'\'\(\\|\mathcal\{E\}\\|\) = -\\gamma\^2\(\\theta_\{\\max\} - \\theta_0\)e\^\{-\\gamma \\|\mathcal\{E\}\\|\} < 0\$。\[ZH\] \$\\delta\'\(\\|\mathcal\{E\}\\|\) > 0\$，\$\\delta\'\'\(\\|\mathcal\{E\}\\|\) < 0\$，\[ZH\] \$\\delta\'\(\\|\mathcal\{E\}\\|\) \\to 0\$ \[ZH\] \$\\|\mathcal\{E\}\\| \\to \\infty\$。\$\\lim_\{\\|\mathcal\{E\}\\| \\to \\infty\} \\delta\(\\|\mathcal\{E\}\\|\) = \\theta_\{\\max\} - \\theta_0\$ \[ZH\]。\$\\Delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\] \$V\$ \[ZH\]（A1）\[ZH\] \$\\delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\]。',
     r'\textbf{(i)--(ii)} Direct differentiation. By A2, $\theta\'(|\mathcal{E}|) = \gamma(\theta_{\max} - \theta_0)e^{-\gamma |\mathcal{E}|} > 0$, $\theta\'\'(|\mathcal{E}|) = -\gamma^2(\theta_{\max} - \theta_0)e^{-\gamma |\mathcal{E}|} < 0$. Hence $\delta\'(|\mathcal{E}|) > 0$, $\delta\'\'(|\mathcal{E}|) < 0$, and $\delta\'(|\mathcal{E}|) \to 0$ as $|\mathcal{E}| \to \infty$. $\lim_{|\mathcal{E}| \to \infty} \delta(|\mathcal{E}|) = \theta_{\max} - \theta_0$ follows from the exponential decay term going to zero. The monotonicity and concavity of $\Delta(|\mathcal{E}|)$ follow from the composite of the monotone concavity of $V$ (A1) with the monotone concavity of $\delta(|\mathcal{E}|)$, which preserves strict concavity.'),
    (r'\\textbf\{\(iii\)\} CEC\[ZH\]：\[ZH\]——\[ZH\]，\[ZH\]。\[ZH\]CEC\[ZH\]（\[ZH\]\(2\)）\[ZH\]——\$\\mathcal\{E\}_t = \\bigcup_\{\\tau=0\}\^\{t\} \\{\\cdots\\\}\$，\[ZH\]。\[ZH\] \$\\Psi\(t; T\\^\*\)\$ \[ZH\]：\[ZH\] \$\\|\mathcal\{E\}_t\^\{public\}\\| \\to \\|\mathcal\{E\}_t\\|\$，\[ZH\] \$\\theta\$ \[ZH\]，\$\\theta\(\\|\mathcal\{E\}_t\^\{public\}\\|\) \\to \\theta\(\\|\mathcal\{E\}_t\\|\)\$，\[ZH\] \$\\Psi \\to 0\$。\[ZH\]\\ref\{thm:absorption\}（\[ZH\]，\[ZH\]M3）\[ZH\]（CEC\[ZH\]）\[ZH\]。',
     r'\textbf{(iii)} The public-good character of the CEC: non-rivalry is guaranteed by the nature of knowledge—calibration parameters and anomaly patterns are information, and information consumption is non-rivalrous. Additivity is guaranteed by the CEC definition (equation (2))—$\mathcal{E}_t = \bigcup_{\tau=0}^{t} \{\cdots\}$, and the union operation is monotonically non-decreasing. Limit behavior of the late-mover penalty ratio $\Psi(t; T^*)$: as $|\mathcal{E}_t^{\text{public}}| \to |\mathcal{E}_t|$, by continuity of $\theta$, $\theta(|\mathcal{E}_t^{\text{public}}|) \to \theta(|\mathcal{E}_t|)$, so $\Psi \to 0$. The non-internationalizable residual advantages are guaranteed by Theorem~\ref{thm:absorption} (irreversibility of stage lock-in, Assumption M3) and the path-dependent standard-setting authority (the CEC\'s initial configuration reflects the first mover\'s calibration choices).'),
    (r'\\textbf\{\(iv\)\} \[ZH\]：\[ZH\] \$f\(t\) = \\Delta\(\\|\mathcal\{E\}_t\\|\) - \(\\lambda - \\kappa\)\$ \[ZH\] \$\[T\\^\*, \\infty\)\$ \[ZH\]（A1--A2\[ZH\]）、\[ZH\]（\[ZH\] \$\\lim_\{\\|\mathcal\{E\}\\| \\to \\infty\} \\Delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\] \$\\lambda - \\kappa\$ \[ZH\]）。\[ZH\] \$\\frac\{1\}\{2\}\[\\Delta\(\\|\mathcal\{E\}_\{T\\^\*\}\\|\) - \(\\lambda - \\kappa\)\]\$，\[ZH\]（\[ZH\]）。\[ZH\]，\[ZH\]——\$f\(t\)\$ \[ZH\]。\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\) \\equiv \\text\{const\}\$（\[ZH\] \$V\$ \[ZH\] \$\\theta\$ \[ZH\]，\[ZH\]A1--A2\[ZH\]），\[ZH\]。',
     r'\textbf{(iv)} Existence of the half-life: the function $f(t) = \Delta(|\mathcal{E}_t|) - (\lambda - \kappa)$ is continuous on $[T^*, \infty)$ (guaranteed by A1--A2), strictly decreasing, and converges to zero or to a positive lower bound (depending on the relationship between $\lim_{|\mathcal{E}| \to \infty} \Delta(|\mathcal{E}|)$ and $\lambda - \kappa$). If the lower bound exceeds $\frac{1}{2}[\Delta(|\mathcal{E}_{T^*}|) - (\lambda - \kappa)]$, then the half-life is finite (by the intermediate value theorem). If the lower bound is smaller, the half-life is still finite—$f(t)$ eventually crosses the half-value line. The only exception would be $\Delta(|\mathcal{E}|) \equiv \text{const}$ (requiring $V$ linear and $\theta$ constant, contradicting A1--A2), in which case the half-life is undefined, but this scenario does not arise.'),
    (r'\\textbf\{\(v\)\} NPE\[ZH\]：\[ZH\]\(\\ref\{eq:all-adopt-condition\}\)\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\\|\)\$ \[ZH\]CEC\[ZH\]。\[ZH\]，\$\\Delta\(\\|\mathcal\{E\}\\|\) = \\Delta\(\\|\mathcal\{E\}\^\{private\}\\|\)\$；\[ZH\]，\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\^\{public\}\\|\)\$。\[ZH\] \$\\Delta\(\\|\mathcal\{E\}\^\{public\}\\|\) \\geq \\lambda - \\kappa\$ \[ZH\]——\[ZH\]。',
     r'\textbf{(v)} Institutional transformation of the NPE: decompose $\Delta(|\mathcal{E}|)$ in equation (\ref{eq:all-adopt-condition}) into the first mover\'s private contribution and the public CEC contribution. Before internationalization, $\Delta(|\mathcal{E}|) = \Delta(|\mathcal{E}^{\text{private}}|)$; after internationalization, the adoption advantage of all jurisdictions converges to $\Delta(|\mathcal{E}^{\text{public}}|)$. The condition $\Delta(|\mathcal{E}^{\text{public}}|) \geq \lambda - \kappa$ involves no jurisdiction\'s identity—the first-mover advantage disappears at the level of the adoption game.'),
    
    # Remark: first-mover decay and NPT
    (r'\\begin\{remark\}\[\[ZH\]\]',
     r'\\begin{remark}[First-Mover Advantage Decay and the Structural Analogy to the NPT]'),
    (r'\[ZH\]\\ref\{cor:first-mover-decay\}\[ZH\]NPT\[ZH\]（\[ZH\]3.5\[ZH\]）\[ZH\]。NPT\[ZH\]VI\[ZH\]\"\[ZH\]\"\[ZH\]——\[ZH\]。\[ZH\]，CEC\[ZH\]\"\[ZH\]VI\[ZH\]\"：\[ZH\]CEC\[ZH\]，\[ZH\]。\[ZH\]NPT\[ZH\]（Joyner, 2011），CEC\[ZH\]——\[ZH\] \$S_3\$（\[ZH\]）\[ZH\]（\[ZH\]\\ref\{prop:intervention-window\}\[ZH\]）。',
     r'Corollary~\ref{cor:first-mover-decay} completes a key institutional corollary of the NPT analogy (Section~3.5). Article VI of the NPT requires nuclear-weapon states to ``pursue negotiations in good faith'' toward nuclear disarmament—i.e., a commitment to the decay of nuclear first-mover advantage. Similarly, the internationalization of the CEC constitutes the ``Article VI'' of audit first-mover advantage: the first mover commits to transforming the CEC into a global public good, thereby allowing its first-mover advantage to decay over time. But just as the disarmament commitment of the NPT faces a credibility crisis (Joyner, 2011), the credibility of CEC internationalization equally depends on institutional design—whether the first mover has the incentive to continue promoting internationalization after reaching $S_3$ (moat formation) (see Proposition~\ref{prop:intervention-window} on the monotonic closure of the intervention window).'),
    
    # Section title
    (r'\\subsection\{\[ZH\]：\[ZH\]\}',
     r'\\subsection{Payoff Matrix and Equilibrium Regions: Parameter-Space Decomposition}'),
]

def main():
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in TRANSLATIONS:
        if old in content:
            content = content.replace(old, new)
            print(f'Replaced: {old[:60]}...')
        else:
            print(f'NOT FOUND: {old[:60]}...')
    
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    remaining = content.count('[ZH]')
    print(f'\nRemaining [ZH] instances: {remaining}')

if __name__ == '__main__':
    main()
