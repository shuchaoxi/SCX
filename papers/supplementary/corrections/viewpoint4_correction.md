# 审查裁决 / Review Verdict

**Author:** SCX

## 审查裁决 / Review Verdict

<div align="center">

[Table omitted — see original .tex]

</div>

### 具体问题 / Specific Issues

1. **不是``平均KL''而是``最小KL''。**
2. **不是``自然涌现''而是条件等价。**
3. **非指数族下完全失效。**

## 八大假设清单 / The Eight Assumptions
<!-- label: sec:assumptions -->

要使得 $\GeoDist(p,q)^2 = 2\KL(p\|q) + O(\|p-q\|^3)$ 严格成立，
以下八个假设必须同时满足。任何一个的失效都会导致等式退化。

For $\GeoDist(p,q)^2 = 2\KL(p\|q) + O(\|p-q\|^3)$ to hold rigorously,
the following eight assumptions must be simultaneously satisfied.
Failure of any single one degrades the equality.

1. **指数族假设 (Exponential Family Assumption).** 

2. **小距离／局部近似假设 (Small-Distance / Local Approximation Assumption).** 

3. **$C^2$ 可微性假设 ($C^2$ Differentiability Assumption).** 

4. **积分-微分可交换假设 (Integration-Differentiation Interchangeability Assumption).** 

5. **Fisher满秩假设 (Fisher Full-Rank Assumption).** 

6. **小联络近似假设 (Small-Connection Approximation Assumption).** 

7. **欧氏近似假设 (Euclidean Approximation / Degenerate Fisher Assumption).** 

8. **分布紧致假设 (Distribution Compactness / Bounded Support Assumption).** 

## 修正后的主张 / Corrected Claim

### 中文修正 (Chinese Correction)

{\bf 原主张（夸大，需删除）：}

> ``Cercis分数是Fisher信息度量下的测地线距离。指数族假设下Cercis${}^2 \propto$ 平均KL散度
> $=$ Fisher测地线长度平方。审计分数不是人为定义——从数据流形信息几何自然涌现。''

{\bf 修正后的主张（条件等价）：}

> {\bf 在指数族假设和局部近似下，}Cercis分数等于观测边分布到纯规范子流形的{\bf 最小}KL散度的两倍，
> 而后者又等于（至二阶）Fisher测地线距离的平方。
> 这提供了一种信息几何{\bf 解释}——但并非``自然涌现''，而是{\bf 条件等价}：
> 当且仅当Situs流形承认指数族结构时成立。
> {\bf 对于非指数族数据，该关系由Amari-Chentsov三阶张量退化（开放问题6.2）。}

具体表述为：

\fbox{%
\begin{minipage}{0.94\textwidth}

 {\bf 定理（Cercis的信息几何条件等价性，修订版）}
<!-- label: thm:cercis_conditional_equivalence -->

{\bf 假设：} 上述8个假设(H1--H8)同时成立。

{\bf 结论：}
\[
\cercis = \min_{d_0 h \in \im(d_0)} \GeoDist(P_A,\; P_{d_0 h})^2
       = 2 \min_{d_0 h \in \im(d_0)} \KL(P_A \| P_{d_0 h}) + O(\|\mathfrak{a}\|^3).
\]

Cercis度量了从观测专家边缘分布到``纯规范体态''（可完美对齐的假想世界）
的最小Fisher信息距离。

{\bf 限制：}

1. 该等价性在指数族(H1)内严格成立；非指数族下，$\GeoDist^2$与$2\KL$的差
2. 该等价性在局部(H2)近似下成立；大分歧下三阶项主导。
3. ``自然涌现''是错误的描述——这是在一组强假设下的构造性等价，

\end{minipage}%
}

### English Correction

{\bf Original claim (overstated, to be removed):}

> ``The Cercis Score is the geodesic distance under the Fisher information metric.
> Under the exponential family assumption, Cercis${}^2 \propto$ mean KL divergence
> $=$ squared Fisher geodesic length. The audit score is not artificially defined —
> it naturally emerges from the information geometry of the data manifold.''

{\bf Corrected claim (conditional equivalence):}

> {\bf Under the exponential family assumption and local approximation,} the Cercis Score
> equals twice the {\bf minimum} KL divergence from the observed edge distribution to the
> pure-gauge submanifold, which in turn equals (to second order) the squared Fisher geodesic
> distance. This provides an information-geometric {\bf interpretation} — not a ``natural emergence''
> but a {\bf conditional equivalence} that holds when and only when the Situs manifold
> admits an exponential family structure.
> {\bf For non-exponential-family data, the relationship degrades by the Amari-Chentsov
> tensor (Open Problem~6.2).}

Explicit formulation:

\fbox{%
\begin{minipage}{0.94\textwidth}

 {\bf Theorem (Information-Geometric Conditional Equivalence of Cercis, Revised)}
<!-- label: thm:cercis_conditional_equivalence_en -->

{\bf Assumptions:} All 8 assumptions (H1--H8) hold simultaneously.

{\bf Conclusion:}
\[
\cercis = \min_{d_0 h \in \im(d_0)} \GeoDist(P_A,\; P_{d_0 h})^2
       = 2 \min_{d_0 h \in \im(d_0)} \KL(P_A \| P_{d_0 h}) + O(\|\mathfrak{a}\|^3).
\]

Cercis measures the minimal Fisher information distance from the observed expert edge
distributions to the ``pure-gauge bulk states'' — the hypothetical world where all
experts can be perfectly aligned.

{\bf Limitations:}

1. The equivalence is rigorous within exponential families (H1); outside them,
2. The equivalence holds under local approximation (H2); for large discrepancies,
3. ``Natural emergence'' is an incorrect characterization — this is a

\end{minipage}%
}

## 五大断裂点 / Five Breakdown Points

以下总结了等价性在实际SCX数据上的五个主要断裂途径：

Below, we summarize five principal ways the equivalence can break on real SCX data:

1. **非指数族失效（最严重） / Non-Exponential-Family Failure (Most Severe).** 

2. **混淆``最小KL''与``平均KL'' / Confusing ``min KL'' with ``average KL''.** 

3. **欧氏近似的隐性要求 / Hidden Euclidean Approximation Requirement.** 

4. **定理4.2证明中的内在修正 / Intrinsic Correction in Theorem~4.2 Proof.** 

5. **局部性限制 / Locality Constraint.** 

## 修订建议 / Recommended Revisions

### 在主文件中需要的修改 / Changes Needed in gauge\_formalized.tex

1. **摘要（第234--238行）：**
2. **第 [ref]节标题：**
3. **定理 [ref]：**
4. **定理 [ref]（统一结构定理）：**
5. **比较表（第1529--1532行）：**
6. **第 [ref]节``信息几何的严格性''段落（第1560--1564行）：**
7. **结论第3点（第1678--1684行）：**

## 开放问题6.2的交叉引用 / Cross-Reference to Open Problem 6.2

本更正与开放问题 [ref]（``非指数族下的Fisher-KL等价性''）直接关联。
该问题指出：

> 对于一般的SCX输出分布（可能非指数族），Fisher测地距离和KL散度之间的关系由
> Amari-Chentsov三阶张量 $T_{ijk} = \E[\partial_i \log p \cdot \partial_j \log p \cdot \partial_k \log p]$
> 控制。需要该张量在SCX输出的经验分布上的界。

This corrigendum is directly linked to Open Problem [ref]
(``Fisher-KL Equivalence Outside Exponential Families''), which states:

> For general SCX output distributions (potentially non-exponential-family),
> the relationship between Fisher geodesic distance and KL divergence is controlled
> by the Amari-Chentsov third-order tensor $T_{ijk} = \E[\partial_i \log p \cdot \partial_j \log p \cdot \partial_k \log p]$.
> Bounds on this tensor for empirical SCX output distributions are needed.

\rule{0.5pt}

 { **审查依据：** 本更正基于以下审查文件：
`docs/reviews/GAUGE\_5VIEWPOINTS\_FINAL.md`（裁决：``夸大''）及
`docs/reviews/GAUGE\_VIEWPOINTS\_REVIEW.md`（详细分析）。
对观点4的裁决为$\checkmark$数学关系正确但``自然涌现''严重夸大，需降级为``条件等价''。}

 { **Review basis:** This corrigendum is based on:
`docs/reviews/GAUGE\_5VIEWPOINTS\_FINAL.md` (verdict: ``overstated'') and
`docs/reviews/GAUGE\_VIEWPOINTS\_REVIEW.md` (detailed analysis).
The verdict on Viewpoint~4 is: $\checkmark$ mathematically correct relationship but
``natural emergence'' is severely overstated — downgrade to ``conditional equivalence''.}