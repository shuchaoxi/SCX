## CLAUDE.md --- SCX 项目<!-- label: claude.md-scx-ux9879ux76ee -->

> 最后更新：2026-06-28

### 项目概述<!-- label: ux9879ux76eeux6982ux8ff0 -->

SCX (State-Conditioned eXpertise) 是一个数学理论 +
工程框架，核心发现是：**区分标签噪声和样本内在困难------这个问题在不加假设时已被数学证明不可解。**
在最小充分假设下，多专家一致性可以提供精确常数 minimax 最优的噪声检测。

\subsection{论文矩阵（全部直指 Nature
系列）}<!-- label: ux8bbaux6587ux77e9ux9635ux5168ux90e8ux76f4ux6307-nature-ux7cfbux5217 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
目录
\end{minipage} & \begin{minipage}[b]
期刊
\end{minipage} & \begin{minipage}[b]
状态
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
I & `paper/nature\_theory/` & **Nature** & 正文已起草, SI
待转译 

II & `paper/nature\_curation/` & **Nat Comp Sci** &
概念已设计 

III & `paper/paper1\_nature/` & **Nat Mach Intell** &
已有草稿, 等 GPU 

IV & `paper/paper2\_mlip/` & **npj Comp Mat** & 已完成,
等超算 

\end{longtable}

参见 `paper/PAPER\_MATRIX.md`。

### 核心定理<!-- label: ux6838ux5fc3ux5b9aux7406 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} & \begin{minipage}[b]
文件
\end{minipage} & \begin{minipage}[b]
验证状态
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
1 & 噪声检测保证 (F1 指数收敛) &
`theory/theorems/01\_noise\_detection\_guarantee.md` & ✅ 

2 & 弱特征失效边界 (δ→0 退化) &
`theory/theorems/02\_weak\_feature\_failure.md` & ✅ 

3 & 噪声-困难不可辨识性 &
`theory/theorems/03\_unidentifiability\_theorem.md` & ✅ 

4' & 精确常数 minimax 最优性 &
`theory/explorations/exact\_constant\_minimax.md` + 4 lemma 文件
& ✅ 

5 & 聚类一致性 (k-means 状态发现) &
`theory/explorations/cluster\_consistency\_v3.md` & ✅ 

6 & Bootstrap 稳定性诊断 &
`theory/explorations/feature\_strength\_via\_stability.md` &
✅ 

\end{longtable}

权威参考：`theory/THEOREMS\_UNIFIED.md`。

### 关键路径<!-- label: ux5173ux952eux8defux5f84 -->

\begin{verbatim}
paper/nature_theory/           ← 主攻：数学理论 Nature 投稿
paper/nature_curation/         ← 次攻：实践原则 Nat Comp Sci
paper/paper1_nature/           ← 第三：方法验证 Nat Mach Intell
scx-life/                      ← 应用模块 (health/ + drug/)
\end{verbatim}

### 当前阻塞<!-- label: ux5f53ux524dux963bux585e -->

- 
- 

### 关联<!-- label: ux5173ux8054 -->

- 
- 
-