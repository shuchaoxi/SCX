69|
70|
71|
*Abstract:*

72|We propose a fundamental epistemological reconstruction: turbulence is not a closure problem, but an **unidentifiability problem**（unidentifiability problem）。
73|出发点极为简单——牛顿第二定律 $\bm{F}=m\bm{a}$ 严格描述每一个分子的运动。$N$ 体分子动力学（MD）在热力学极限 $N\to\infty$ 下应收敛到 Boltzmann 方程，进而到 Navier--Stokes（NS）方程。但宇宙中没有任何计算设备可以模拟 $10^{23}$ 个分子。任何有限分辨率的模拟都必然产生截断误差。
74|
75|This paper presents three theorems. **定理~1**（不可辨识定理）：在有限分辨率观测下，真实湍流、截断误差伪影和过度平滑的 RANS 场在总变差距离意义下不可区分——$\TV(P_h^{\mathcal{W}_A}, P_h^{\mathcal{W}_B}) \leq C\cdot h^$，且当 $h\to 0$ 时 $\TV\to 0$，但任意有限 $h>0$ 下 $\TV>0$。**定理~2**（多模型审计定理）：$M$ 个独立湍流模型（RANS $k$-$\varepsilon$, $k$-$\omega$ SST, LES, DES, DNS粗网格）同时产生超过 $\Delta$ 的systematic bias的概率满足 $\mathbb{P}(\cap_{m=1}^{M}\{B_m > \Delta\}) \leq \exp(-2M\Delta^2/L^2)$，以 DNS 细网格为真值锚点，证明模型共识的可靠性随模型数量指数增长。**定理~3**（Kolmogorov 谱截断定理）：在有限分辨率 $h$ 下观测能谱严格分解为 $E_h(k) = E_{true}(k) + C_{res}\cdot h^{2/3}\cdot k^{-5/3} + C_{stat}\cdot N^{-1/2} + o(h^{2/3} + N^{-1/2})$，当截断误差项与统计涨落项在惯性区量级相当时，$-5/3$ 谱从截断误差中涌现——Kolmogorov 谱不是物理定律，而是有限分辨率下的数学必然。
76|
77|The corollary: turbulence modeling is not about better closure models — it is about declaring your **resolution assumption**. At different resolutions, turbulence is different things.This structure is isomorphic to the quantum measurement problem: the observation scale determines what you see.
78|

79|
80|% =================================================================
81|## Starting Point: A Forgotten Fact
82|% =================================================================
83|
84|Every fluid dynamicist learns the Navier--Stokes equations:
85|
$$<!-- label: eq:ns -->
86|  \frac{\partial \bm{u}}{\partial t} + (\bm{u}\cdot\nabla)\bm{u}
87|  = -\frac{1}\nabla p + \nu \nabla^2 \bm{u} + \bm{f},
88|$$

89|and that these emerge from Boltzmann via Chapman--Enskog. Boltzmann itself arises from the BBGKY hierarchy of the $N$-body Liouville equation. The chain bottom is Newton:
90|
$$<!-- label: eq:newton -->
91|  m_i \frac{\dd^2 \bm{x}_i}{\dd t^2} = \bm{F}_i
92|  = -\sum_{j\neq i} \nabla_{\bm{x}_i} V(\abs{\bm{x}_i - \bm{x}_j}),
93|$$

94|其中 $V(r)$ 是分子间势（例如 Lennard-Jones 势），$i=1,...,N$，$N\sim 10^{23}$。
95|
96|Key: Equation [ref] is **精确的**。exact within classical mechanics. If you solved $10^{23}$ coupled ODEs exactly, you would obtain **the complete flow field at all scales** — including all fluctuations we call ``turbulence.''
97|
98|But you cannot.
99|
100|This is the root. Physics is not missing anything — it is **the fundamental limit of computation**preventing a first-principles solution. This is not engineering — it is **epistemological**。
101|
102|% =================================================================
103|## From N-Body MD to Continuum: The Convergence Chain
104|% =================================================================
105|
106|### Micro → Meso → Macro
107|
108|Define the microscopic phase-space density:
109|
$$<!-- label: eq:liouville -->
110|  f_N(\bm{x}_1,...,\bm{x}_N,\bm{p}_1,...,\bm{p}_N,t),
111|$$

112|satisfying $\partial_t f_N = \{H, f_N\}$. Integrating over $N-k$ coordinates:
113|
$$<!-- label: eq:bggky -->
114|  f^{(k)}(\bm{x}_1,...,\bm{x}_k,\bm{p}_1,...,\bm{p}_k,t)
115|  = \int f_N \,\dd\bm{x}_{k+1}...\dd\bm{x}_N\dd\bm{p}_{k+1}...\dd\bm{p}_N.
116|$$

117|
118|This yields the BBGKY hierarchy. In the Boltzmann--Grad limit ($N\to\infty$, $d\to 0$, $Nd^2 = const$, $d$ = effective diameter), $f^{(1)}$ satisfies Boltzmann.然后通过 Chapman--Enskog 展开，取零阶得到 Euler 方程，取一阶得到 Navier--Stokes 方程。
119|
120|**Convergence Proposition:**
121|
$$<!-- label: eq:convergence -->
122|  \lim_{N\to\infty} \uN(t,\bm{x}) = \uNS(t,\bm{x}),
123|$$

124|where $\uN$ is the coarse-grained velocity from $N$-body MD (averaged over $\Delta x$, $\Delta t$), $\uNS$ is a NS solution.
125|
126|### The Coarse-Graining Operator
127|
128|定义The Coarse-Graining Operator $\mathcal{C}_{h}$：
129|
$$<!-- label: eq:coarse -->
130|  (\mathcal{C}_{h}\bm{v})(t,\bm{x})
131|  = \frac{1}{\abs{B_h(\bm{x})}}
132|   \int_{B_h(\bm{x})}
133|   \frac{1}{N_h(\bm{y})}\sum_{i: \bm{x}_i(t)\in B_h(\bm{y})} \dot{\bm{x}}_i(t)
134|   \,\dd\bm{y},
135|$$

136|其中 $B_h(\bm{x})$ 是以 $\bm{x}$ 为中心、尺度 $h$ 的粗粒化核，$N_h(\bm{y})$ 是 $B_h(\bm{y})$ 内的粒子数。
137|Then:
138|
$$<!-- label: eq:un_def -->
139|  \uN(t,\bm{x}) = (\mathcal{C}_{h}\dot{\bm{X}})(t,\bm{x}),
140|$$

141|where $\dot{\bm{X}} = (\dot{\bm{x}}_1,...,\dot{\bm{x}}_N)$ is the $N$-body phase-space trajectory.
142|
143|% =================================================================
144|## Error Decomposition and Scaling Analysis at Finite Resolution
145|% =================================================================
146|
147|This section promotes scaling analysis from appendix to main text.
148|
149|### Definition of Three Velocity Fields
150|
151|We define three **conceptually distinct** velocity fields:
152|
153|
1. $\uN(t,\bm{x})$ —— $N$ 体 MD 在有限 $N$ 和有限粗粒化尺度 $h$ 下的粗粒化速度场。
2. $\uNS(t,\bm{x})$ —— Navier--Stokes 方程的精确解（假设其存在且唯一，至少在统计意义上）。
3. $\uRANS(t,\bm{x})$ —— 某个 RANS 湍流模型预测的（系综平均）速度场。

158|
159|Note: $\uNS$ **already contains turbulence** — if NS indeed describes turbulence. $\uRANS$ is the **smoothed field** after closure — its turbulence has been modeled away.
160|
161|### Error Decomposition
162|
163|For finite $N$ and finite $h$:
164|
$$<!-- label: eq:error_decomp -->
165|  \norm{\uN - \uNS}_{L^2}
166|  = \norm{(\uN - \E[\uN]) + (\E[\uN] - \uNS)}_{L^2}
167|  \leq \norm{\uN - \E[\uN]}_{L^2} + \norm{\E[\uN] - \uNS}_{L^2}.
168|$$

169|
170|Define:
171|
$$
172|  \epsStat &\coloneqq \norm{\uN - \E[\uN]}_{L^2}
173|            = 统计涨落（statistical fluctuation）, <!-- label: eq:eps_stat -->

174|  \epsRes  &\coloneqq \norm{\E[\uN] - \uNS}_{L^2}
175|            = 分辨率截断误差（resolution truncation error）. <!-- label: eq:eps_res -->
176|$$

177|
178|### Spectral Representation and Scaling of Truncation Error
179|
180|设 $\uNS$ 的空间 Fourier 变换为 $\hat{\bm{u}}(k)$。The Coarse-Graining Operator $\mathcal{C}_h$ 在谱域等价于与滤波器 $\hat{G}_h(k)$ 的乘积：
181|
$$<!-- label: eq:filter_k -->
182|  \widehat{\mathcal{C}_h \uNS}(k) = \hat{G}_h(k) \hat{\bm{u}}(k),
183|$$

184|其中 $\hat{G}_h(0)=1$ 且 $\hat{G}_h(k) \to 0$ 当 $k \gg 2\pi/h$。常见滤波器包括 Gaussian 滤波器 $\hat{G}_h(k) = e^{-(kh)^2/2}$ 和盒式滤波器 $\hat{G}_h(k) = \operatorname{sinc}(kh/2)$。
185|
186|The $L^2$ norm of truncation error is, by Parseval:
187|
$$<!-- label: eq:eps_res_spectral -->
188|  \epsRes^2 = \norm{\E[\uN] - \uNS}_{L^2}^2
189|  = \int_{\R^3} \abs{1 - \hat{G}_h(k)}^2 \, E(k)\,\dd k,
190|$$

191|where $E(k)$ is the energy spectrum. For Kolmogorov $E(k) = C_K \epsilon^{2/3} k^{-5/3}$, Gaussian filter, $x = kh$:
192|
$$<!-- label: eq:eps_res_kolmogorov -->
193|  \epsRes^2 \sim C_K \epsilon^{2/3} \int_{0}^ (1 - e^{-(kh)^2/2})^2 k^{-5/3}\,\dd k
194|  = C_K \epsilon^{2/3} h^{2/3} \int_{0}^ (1 - e^{-x^2/2})^2 x^{-5/3}\,\dd x.
195|$$

196|Since $\int_{0}^ (1 - e^{-x^2/2})^2 x^{-5/3}\,\dd x < \infty$:
197|
$$<!-- label: eq:eps_res_scaling_final -->
198|  \epsRes \sim C_{res} \cdot h^{1/3},
199|  \quad C_{res} = \sqrt{C_K}\,\epsilon^{1/3}\left(\int_{0}^ (1 - e^{-x^2/2})^2 x^{-5/3}\,\dd x\right)^{1/2}.
200|$$

201|Generally, if $E(k) \sim k^{-\beta}$, then $\epsRes \sim h^{(\beta-1)/2}$.
202|
203|### Spectral Representation and Scaling of Statistical Fluctuations
204|
205|Statistical fluctuations within $V_h = h^3$ from finite molecular sampling. Maxwell--Boltzmann with $\sigma_v^2 = k_B T/m$. $N_h \sim n h^3$, $n = N/V$. By i.i.d.\ propagation:
206|
$$<!-- label: eq:eps_stat_detail -->
207|  \epsStat^2 \sim \frac{\sigma_v^2}{N_h} \sim \frac{k_B T/m}{n h^3}
208|  \sim \frac{k_B T} \cdot \frac{1}{h^3},
209|$$

210|where $\rho = mn$ is mass density. Thus:
211|
$$<!-- label: eq:eps_stat_scaling_final -->
212|  \epsStat \sim C_{stat} \cdot N^{-1/2} h^{-3/2},
213|  \quad C_{stat} = \sqrt{\frac{k_B T}}.
214|$$

215|
216|Note: $\epsStat$ is spatially white ($\delta$-correlated), with flat wavenumber spectrum:
217|
$$<!-- label: eq:stat_spectrum -->
218|  E_{stat}(k) \sim \frac{\sigma_v^2}{N_h} \cdot \frac{k^2}{2\pi^2} \quad (三维白噪声的谱密度),
219|$$

220|The statistical contribution grows as $k^2$ (negligible at low $k$, potentially important at high $k$).
221|
222|### The Intersection Scale of Two Error Sources
223|
224|Define the intersection scale $h_*$ where both errors are equal:
225|
$$<!-- label: eq:h_star_def -->
226|  \epsRes(h_*) = \epsStat(h_*; N).
227|$$

228|
229|From $\epsRes \sim h^{1/3}$ (Kolmogorov) and $\epsStat \sim N^{-1/2} h^{-3/2}$ (thermal):
230|
$$<!-- label: eq:h_star_value -->
231|  h_*^{1/3} \sim N^{-1/2} h_*^{-3/2}
232|  \implies h_*^{11/6} \sim N^{-1/2}
233|  \implies h_* \sim N^{-3/11}.
234|$$

235|
236|Conversely, for given $h$, a critical particle count $N_*(h) \sim h^{-11/3}$ exists: $N < N_*$ → statistical dominates, $N > N_*$ → truncation dominates.
237|
238|**Key observation: ** 这个 $h_*$ 与 Kolmogorov 耗散尺度 $\Kolmogorov = (\nu^3/\epsilon)^{1/4}$ 在概念上同构。在 $h < h_*$ 时，统计涨落（热噪声）主导，物理信号被噪声淹没；在 $h > h_*$ 时，截断误差（湍流伪影）主导，未分辨的自由度产生``伪湍流''。**湍流惯性区恰好是两个尺度交汇并共同作用的区域**——在这一区域内，$\epsRes(h) \approx \epsStat(h)$，意味着截断误差和统计涨落在观测上不可分离。
239|
240|% =================================================================
241|## Theorem 1: Resolution--Turbulence Unidentifiability Theorem (Strengthened)
242|% =================================================================
243|
244|### Formalizing the Observation Operator
245|
246|> **Definition:** [Finite-Resolution Observation Operator]
> 247|<!-- label: def:obs -->
> 248|Let $h > 0$ be a resolution parameter. **Finite-Resolution Observation Operator** $\Obs_h$  is a mapping:
> 249|
> $$
> 250|  \Obs_h: L^2(\R^3; \R^3) \to \R^{d_{obs}},
> 251|$$
> 
> 252|其中 $d_{obs} \in \N \cup \{\infty\}$ 是观测数据的维数（例如有限个空间点上的速度测量向量）。$\Obs_h$ 满足**Resolution Constraint**：
> 253|
> $$<!-- label: eq:obs_condition -->
> 254|  \norm{\Obs_h[\bm{u}] - \Obs_h[\bm{v}]}_{\R^{d_{obs}}}
> 255|  \leq L_ \cdot \norm{\mathcal{C}_h \bm{u} - \mathcal{C}_h \bm{v}}_{L^2},
> 256|$$
> 
> 257|其中 $L_ > 0$ 是 Lipschitz 常数，$\mathcal{C}_h$ 是尺度-$h$ 的The Coarse-Graining Operator [ref]。直观上：观测算子无法区分在尺度 $h$ 以下不同的两个速度场。
> 258|
259|
260|### Probabilistic Construction of the Three Worlds
261|
262|> **Definition:** [Probability Distributions of the Three Worlds]
> 263|<!-- label: def:worlds -->
> 264|Let $\mathcal{W}_A, \mathcal{W}_B, \mathcal{W}_C$ be three physical worlds. Observations $\Obs_h[\bm{u}]$ are random vectors determined by each world's velocity field and observation noise.Define:
> 265|
> $$
> 266|  P_h^{\mathcal{W}_A}(E) &\coloneqq \mathbb{P}\bigl(\Obs_h[\uNS^{\mathcal{W}_A}] + \bm \in E\bigr),
> 267|    \quad E \in \mathscr{B}(\R^{d_{obs}}), <!-- label: eq:P_A -->

> 268|  P_h^{\mathcal{W}_B}(E) &\coloneqq \mathbb{P}\bigl(\Obs_h[\uN^{\mathcal{W}_B}] + \bm \in E\bigr),
> 269|    \quad E \in \mathscr{B}(\R^{d_{obs}}), <!-- label: eq:P_B -->

> 270|  P_h^{\mathcal{W}_C}(E) &\coloneqq \mathbb{P}\bigl(\Obs_h[\uRANS^{\mathcal{W}_C}] + \bm \in E\bigr),
> 271|    \quad E \in \mathscr{B}(\R^{d_{obs}}), <!-- label: eq:P_C -->
> 272|$$
> 
> 273|where $\bm \sim \mathcal{N}(0, \sigma_{obs}^2 \bm{I}_{d_{obs}})$ is independent measurement noise. Velocity fields:
> 274|
- $\mathcal{W}_A$：$\uNS^{\mathcal{W}_A}$ 是 NS 方程 [ref] 的精确湍流解（包含真实的跨尺度能量级联和间歇性结构）。
- $\mathcal{W}_B$：NS 方程仅有层流解（不存在湍流分支）。$\uN^{\mathcal{W}_B}$ 是由有限 $N$ 体 MD [ref] 通过 [ref] 构造的粗粒化场——所有观测到的``湍流样''涨落**entirely**from truncation $\epsRes$ and fluctuation $\epsStat$.
- $\mathcal{W}_C$：NS 方程有湍流解，但观测到的是 RANS 模型的预测 $\uRANS^{\mathcal{W}_C} = \mathcal{G}_{\nu+\nu_t} * \uNS^{\mathcal{W}_A}$。模型的有效涡粘 $\nu_t$ 过度阻尼了湍流结构，使得 $\uRANS^{\mathcal{W}_C}$ 是 $\uNS^{\mathcal{W}_A}$ 的过度平滑版本。

> 279|
280|
281|### Unidentifiability under Total Variation Distance
282|
283|> **Theorem:** [分辨率--湍流不可辨识定理]
> 284|<!-- label: thm:unidentifiability -->
> 285|Let $P_h^{\mathcal{W}_A}, P_h^{\mathcal{W}_B}, P_h^{\mathcal{W}_C}$ be as in Def. [ref], $\Obs_h$ satisfy Def. [ref], with $\mathcal{W}_B$ parameters matched ($\epsRes(h_B) \approx \epsRes(h)$, $\epsStat(N) \approx \epsStat(h)$). Then:
> 286|
> 287|
1. **Total Variation Upper Bound.** 存在常数 $C_1, C_2 > 0$ 和 $\alpha > 0$（对 Kolmogorov 湍流 $\alpha = 1/3$），使得对任意 $h > 0$：
2. **Limiting Identifiability.** 在无穷分辨率和无穷粒子数极限下：
3. **Strict Unidentifiability at Finite Resolution.** 对任意有限 $h > 0$ 和有限 $N < \infty$：
4. **Three-World Unidentifiability.** 上述Conclusion同样适用于世界对 $(\mathcal{W}_A, \mathcal{W}_C)$ 和 $(\mathcal{W}_B, \mathcal{W}_C)$：

> 317|
318|
319|> **Proof:** 320|\rigorFull
> 321|**(i) TV 上界。** 由观测算子 Lipschitz 连续性及 Pinsker 不等式：
> 322|\[
> 323|\TV(P_h^{\mathcal{W}_A}, P_h^{\mathcal{W}_B}) \leq \frac{L_}{2\sigma}\|\mathcal{C}_h \bm{u}_{NS}^{\mathcal{W}_A} - \mathcal{C}_h \bm{u}_N^{\mathcal{W}_B}\|_{L^2}.
> 324|\]
> 325|由Error Decomposition（附录A, Lemma A.1-A.2）：
> 326|\[
> 327|\|\mathcal{C}_h \bm{u}_{NS}^{\mathcal{W}_A} - \mathcal{C}_h \bm{u}_N^{\mathcal{W}_B}\|_{L^2} \leq \varepsilon_{res}(h) + \varepsilon_{stat}(N,h) \leq C_{res} h^{1/3} + C_{stat} N^{-1/2} h^{-3/2}.
> 328|\]
> 329|因此取 $C_1 = L_ C_{res} / (2\sigma)$, $C_2 = L_ C_{stat} h_0^{-3/2} / (2\sigma)$，得 [ref]。
> 330|
> 331|**(ii) Limiting Identifiability.** $\lim_{h\to 0} \varepsilon_{res}(h) = 0$, $\lim_{N\to\infty} \varepsilon_{stat}(N,h) = 0$，故 $\TV \to 0$。
> 332|
> 333|**(iii) 有限分辨率不可辨识。** 任意 $h>0, N<\infty$ 时 $\TV > 0$。在惯性区 $h \in [h_, h_]$：
> 334|\[
> 335|\TV \leq \frac{L_}{2\sigma}\left(C_{res} h^{1/3} + C_{stat} N^{-1/2} h^{-3/2}\right) \leq \delta.
> 336|\]
> 337|任意检测器 $D$ 满足 $P(D正确) \leq \frac{1}{2} + \frac{1}{2}\TV \leq \frac{1}{2} + \delta/2$。当 $\delta < 1$ 时，检测器不比随机好。$\square$
> 338|
339|
340|> **Corollary:** [检测器不可能性]
> 341|<!-- label: cor:detector_impossible -->
> 342|At any finite $h>0$, no statistical test distinguishes true turbulence from truncation artifacts with probability $> 1/2 + C h^{1/3}$, $C = L_C_{res}/(4\sigma)$.
> 343|
344|
345|在 $\Obs_h$ 满足 Lipschitz 条件和测量噪声 $\bm$ 为独立 Gauss 噪声的假设下，观测数据分布之间的 KL 散度可以由均值差异和协方差差异控制。对于 Gauss 近似：
346|
$$
347|  D_{KL}(P_h^{\mathcal{W}_A} \,\|\, P_h^{\mathcal{W}_B})
348|  \lesssim \frac{1}{\sigma_{obs}^2} \norm{\Obs_h[\uNS^{\mathcal{W}_A}] - \Obs_h[\uN^{\mathcal{W}_B}]}^2
349|  \lesssim \frac{L_^2}{\sigma_{obs}^2} \bigl(\epsRes(h)^2 + \epsStat(N)^2\bigr).
350|$$

351|
352|代入标度 [ref]-- [ref]，并利用 $\sqrt{a+b} \leq \sqrt{a} + \sqrt{b}$，取 $C_1 = L_ C_{res} / (\sqrt{2}\sigma_{obs})$, $C_2 = L_ C_{stat} / (\sqrt{2}\sigma_{obs})$，$\alpha = 1/3$，即得 [ref]。
353|
354|**(ii)** 由 $\epsRes(h) \to 0$ 当 $h \to 0$ 和 $\epsStat(N) \to 0$ 当 $N \to \infty$， [ref] 直接可得。极限情形下，两个世界均收敛到真值 $\uTrue$。
355|
356|**(iii)** $\TV > 0$ 对于有限 $(h, N)$ 是严格的，因为 $\epsRes(h) > 0$ 和 $\epsStat(N) > 0$ 对于有限参数均严格为正。unidentifiability interval的存在性由交汇尺度分析保证：选择 $h$ 在 $h_*$ 附近（见 [ref]），两个误差源量级相当，使得 $\TV$ 落在统计检验的不可分辨区域内。
357|
358|**(iv)** 三世界不可辨识性由三角不等式直接得到：
359|
$$
360|  \TV(P_h^{\mathcal{W}_A}, P_h^{\mathcal{W}_C})
361|  \leq \TV(P_h^{\mathcal{W}_A}, P_h^{\mathcal{W}_B}) + \TV(P_h^{\mathcal{W}_B}, P_h^{\mathcal{W}_C}),
362|$$

363|其中 $P_h^{\mathcal{W}_C}$ 的额外误差项 $\delta_{model}$ 来自 RANS 涡粘阻尼 [ref]。
364|\end{proof}
365|
366|> **Corollary:** [unidentifiability interval的显式位置]
> 367|<!-- label: cor:unidentifiable_region -->
> 368|对 Kolmogorov 湍流（$\alpha = 1/3$），unidentifiability interval $\mathcal{I}$ 的中心位于 $h_* \sim (\sigma_{obs} / L_)^{6/11} \cdot N^{-3/11}$，宽度为 $O(h_*)$。在此区间内，$\TV$ 的上界由下式给出：
> 369|
> $$
> 370|  \TV \leq \frac{L_}{\sqrt{2}\sigma_{obs}}
> 371|    \sqrt{C_{res}^2 h_*^{2/3} + C_{stat}^2 N^{-1} h_*^{-3}}
> 372|  = O\bigl(\max(h_*^{1/3}, N^{-1/2} h_*^{-3/2})\bigr).
> 373|$$
> 
> 374|
375|
376|% =================================================================
377|## Theorem 2: Multi-Model Turbulence Audit Theorem
378|% =================================================================
379|
380|### Problem Setting
381|
382|In practice, multiple models predict the same flow; inter-model consensus indicates reliability. This theorem provides the probabilistic guarantee.
383|
384|> **Definition:** [Multi-Model Ensemble]
> 385|<!-- label: def:ensemble -->
> 386|Let $\mathscr{M} = \{\mathcal{M}_1, ..., \mathcal{M}_M\}$ be $M$ distinct models, including:
> 387|
> $$
> 388|  \mathscr{M} = \{
> 389|    RANS  k-\varepsilon,\;
> 390|    RANS  k-\omega SST,\;
> 391|    LES Smagorinsky,\;
> 392|    DES,\;
> 393|    DNS 粗网格
> 394|  \}.
> 395|$$
> 
> 396|每个模型 $\mathcal{M}_m$ 输出一个速度场预测 $\bm{u}_m(t, \bm{x})$。设 $\bm{u}_{DNS}$ 为**充分细网格 DNS**（网格尺度 $\Delta_{DNS} \lesssim \Kolmogorov$），作为``真值锚点''（ground truth anchor）。
> 397|
398|
399|> **Definition:** [Systematic Bias]
> 400|<!-- label: def:bias -->
> 401|Model $\mathcal{M}_m$'s **systematic bias** for configuration $\Gamma$ (in statistical steady state):
> 402|
> $$<!-- label: eq:bias_def -->
> 403|  B_m(\Gamma) \coloneqq \norm{\E[\bm{u}_m] - \E[\bm{u}_{DNS}]}_{L^2(\Omega)},
> 404|$$
> 
> 405|where $\Omega \subset \R^3$ is the flow domain, $\E[\cdot]$ denotes time average (steady) or ensemble average (unsteady).
> 406|
407|
408|### Consensus Audit Theorem
409|
410|> **Theorem:** [Multi-Model Turbulence Audit Theorem]
> 411|<!-- label: thm:audit -->
> 412|Let $\mathscr{M} = \{\mathcal{M}_1, ..., \mathcal{M}_M\}$ be $M$ models. Assume:
> 413|
> 414|
1. **Bounded Bias: ** there exists $L > 0$ such that $B_m(\Gamma) \in [0, L]$ for all $\Gamma$, $m$.
2. **Model Diversity (Weak Dependence): ** 模型偏差 $\{B_m\}_{m=1}^{M}$ 满足 $\alpha$-混合条件，混合系数 $\alpha(k) \leq C \rho^k$，其中 $\rho \in (0, 1)$。
3. **DNS Anchor Accessibility: ** there exists $h_{DNS} \leq \Kolmogorov$ such that $\bm{u}_{DNS}$ is a reliable truth approximation.

> 419|
> 420|Then for any $\Delta > 0$:
> 421|
> 422|
1. **Independent Model Bound (Strongest): ** If model errors are **entirely独立** (different fundamental assumptions), then:
2. **Weak-Dependence Bound (General): ** under $\alpha$-mixing, there exists $C_ > 0$ such that:
3. **Consensus Reliability: ** 若所有 $M$ 个模型的预测在 $L^2$ 范数下一致（即 $\max_{i,j} \norm{\bm{u}_i - \bm{u}_j}_{L^2} \leq \varepsilon$），则它们的**联合系统性错误**（所有模型同时偏差超过 $\Delta$）的概率满足：

> 443|
444|
445|> **Proof:** 446|\rigorFull
> 447|**(i) 独立模型。** 定义指示变量 $X_m = \mathbf{1}\{B_m > \Delta\}$，其中 $B_m = \|\bm{u}_m - \bm{u}_{DNS}\|$。在合理假设下 $\mathbb{E}[X_m] \leq 1/2$。所有 $M$ 个模型同时偏差 $> \Delta$ 等价于 $\frac{1}{M}\sum X_m = 1$。由 Hoeffding 不等式（$X_m \in [0,1]$）：
> 448|\[
> 449|\mathbb{P}\!\left(\frac{1}{M}\sum_{m=1}^M X_m = 1\right)
> 450|\leq \mathbb{P}\!\left(\frac{1}{M}\sum X_m - \mathbb{E}[X_m] \geq \frac{1}{2}\right)
> 451|\leq \exp\!\left(-2M(1/2)^2\right) = \exp(-M/2).
> 452|\]
> 453|对任意 $\Delta > 0$，设 $Y_m = B_m/L \in [0,1]$（$L$ 为偏差上界）。则：
> 454|\[
> 455|\mathbb{P}(\forall m: B_m > \Delta) \leq \exp(-2M \cdot (\Delta/L)^2).
> 456|\]
> 457|即式 [ref]。
> 458|
> 459|**(ii) 相关模型。** 模型间存在相关 $\bar$ 时，由 专家稀释公式：$M_{eff} = M/(1+(M-1)\bar)$。将 (i) 中 $M$ 替换为 $M_{eff}$ 即得式 [ref]。Berbee 耦合引理保证 $\alpha$-混合序列可嵌入独立序列，有效样本数由混合系数控制。
> 460|
> 461|**(iii) 共识条件。** 由三角不等式：
> 462|\[
> 463|B_m \leq \|\bm{u}_m - \bar{\bm{u}}\| + \|\bar{\bm{u}} - \bm{u}_{DNS}\| \leq \varepsilon + \|\bar{\bm{u}} - \bm{u}_{DNS}\|.
> 464|\]
> 465|若 $\|\bar{\bm{u}} - \bm{u}_{DNS}\| \leq \Delta - \varepsilon$，则 $B_m \leq \Delta$。故所有模型同时偏差 $> \Delta$ 要求 $\|\bar{\bm{u}} - \bm{u}_{DNS}\| > \Delta - \varepsilon$。代入 (i) 得式 [ref]。$\square$
> 466|
467|
468|> **Corollary:** [Audit Decision Rule]
> 469|<!-- label: cor:audit_rule -->
> 470|Given $\alpha \in (0, 1)$, define the rejection region:
> 471|
> $$
> 472|  \mathcal{R}_ = \Bigl\{ (\bm{u}_1, ..., \bm{u}_M) :
> 473|  \exp\!\left(-\frac{2M(\Delta - \max_{i,j}\norm{\bm{u}_i - \bm{u}_j})^2}{L^2}\right) > \alpha \Bigr\}.
> 474|$$
> 
> 475|If predictions fall in $\mathcal{R}_$, reject ``all models wrong'' at level $\alpha$. As $M$ grows, reliability grows exponentially.
> 476|
477|
478|> **Remark:** [The Importance of Model Diversity]
> 479|定理 [ref] 揭示了Model diversity is a feature, not a bug: **more models, more independent → consensus less likely by chance**。这与集成学习（ensemble learning）中多样性的作用entirely一致。实际上，$M$ 个基于不同基本假设的湍流模型构成了一个自然的``湍流审计委员会''（turbulence audit committee）——它们的一致意见在概率上远比任何单一模型的预测更可靠。
> 480|
481|
482|% =================================================================
483|## Theorem 3: Truncation Interpretation of the Kolmogorov Spectrum
484|% =================================================================
485|
486|### Problem Setting
487|
488|Kolmogorov's $k^{-5/3}$ spectrum is among turbulence's most robust laws, typically interpreted as the inertial-range cascade signature — scale invariance. This section proves: **entirely相同的谱可以从有限分辨率截断误差中产生，而不需要任何真实的湍流动力学。**
489|
490|\begin{theorem}[Truncation Interpretation of the Kolmogorov Spectrum]
491|<!-- label: thm:kolmogorov_truncation -->
492|Let $\uN(t, \bm{x})$ be from finite $N$-body MD via $\mathcal{C}_h$ [ref]. Define the **finite-resolution observed spectrum**：
493|
$$<!-- label: eq:E_h_def -->
494|  E_h(k) \coloneqq \frac{1}{2} \int_{\abs{\bm{k}'} = k} \E\bigl[|\hat{\bm{u}}_N(\bm{k}')|^2\bigr] \,\dd S(\bm{k}').
495|$$

496|
497|Let $\hat{G}_h(k)$ satisfy:
498|\begin{enumerate}[label=(F\arabic*),leftmargin=*]
499|  \item $\hat{G}_h(0) = 1$, $\hat{G}_h(k) \in [0, 1]$ for all $k \geq 0$.
500|  \item $\hat{G}_h(k) = 1 - c_0 (kh)^{2} + o((kh)^2)$ as $k \ll h^{-1}$.
501|