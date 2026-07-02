\section{明日推进 TODO ---
2026-06-29}<!-- label: ux660eux65e5ux63a8ux8fdb-todo-2026-06-29 -->

\subsection{🔴 全药物数据库下载 + Yajie
一次性全筛}<!-- label: ux5168ux836fux7269ux6570ux636eux5e93ux4e0bux8f7d-yajie-ux4e00ux6b21ux6027ux5168ux7b5b -->

\subsubsection{数据库清单（全量，不仅限于
HIV）}<!-- label: ux6570ux636eux5e93ux6e05ux5355ux5168ux91cfux4e0dux4ec5ux9650ux4e8e-hiv -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1667}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
数据库
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} & \begin{minipage}[b]
大小
\end{minipage} & \begin{minipage}[b]
优先级
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
1 & **ChEMBL** & 全量生物活性数据（所有靶点、所有化合物） &
~50GB & 🔴 

2 & **DrugBank** & 全部已批准+实验性药物，带靶点 &
~1GB & 🔴 

3 & **PubChem BioAssay** & 全部检测数据 & ~50GB &
🔴 

4 & **BindingDB** & 全量蛋白-配体结合亲和力 & ~2GB &
🔴 

5 & **PDBbind** & 蛋白-配体复合物+结合亲和力（最精确） &
~5GB & 🟡 

6 & **TTD** (Therapeutic Target Database) & 已知治疗靶点+对应药物 &
~500MB & 🔴 

7 & **DrugCentral** & FDA批准药物的靶点+适应症 & ~1GB
& 🟡 

8 & **Open Targets** & 靶点-疾病关联（GWAS+文献） &
~10GB & 🟡 

9 & **PharmGKB** & 药物基因组学（基因×药物×反应） &
~2GB & 🟡 

10 & **Stanford HIVDB** & HIV耐药突变（保留） & \textless100MB &
🔴 

11 & **SIDER** & 药物副作用数据库 & ~1GB & 🟡 

12 & **STITCH** & 化合物-蛋白相互作用网络 & ~20GB &
🟢 

\end{longtable}

#### 硬盘需求<!-- label: ux786cux76d8ux9700ux6c42 -->

\begin{verbatim}
🔴 优先级 (必须): ~105GB
🟡 强推荐:         ~20GB  
🟢 可选:           ~20GB
缓冲+解压:        ~50GB
─────────────────────────
总计:             ~200GB
\end{verbatim}

#### 预处理管道<!-- label: ux9884ux5904ux7406ux7ba1ux9053 -->

- [$\boxtimes$]
- [$\boxtimes$]
- [$\boxtimes$]

#### Yajie 运行<!-- label: yajie-ux8fd0ux884c -->

- [$\boxtimes$]
- [$\boxtimes$]
- [$\boxtimes$]
- 
- 
- 

\end{itemize}

#### 验证<!-- label: ux9a8cux8bc1 -->

- [$\square$]
- [$\square$]
- [$\square$]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 🟡 arXiv 投稿<!-- label: arxiv-ux6295ux7a3f -->

- [$\square$]
- [$\square$]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### ✅ 已完成<!-- label: ux5df2ux5b8cux6210 -->

- [$\boxtimes$]
- [$\boxtimes$]
- [$\boxtimes$]
- 
- 
- 
- 
- 

\item[$\boxtimes$]
  **Yajie全数据库筛查脚本**
  `drug-module/scripts/screen\_all\_databases.py`
  (~930行)

  
- 
- 
- 
- 
- 
- 

\end{itemize}