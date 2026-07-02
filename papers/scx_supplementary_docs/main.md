\section{SCX
附加材料清单}<!-- label: scx-ux9644ux52a0ux6750ux6599ux6e05ux5355 -->

> 配合 paper/arxiv/README.md 论文索引使用

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 核心代码<!-- label: ux6838ux5fc3ux4ee3ux7801 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
文件
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} & \begin{minipage}[b]
行数
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`src/scx/yajie.py` & Yajie 审计核心 & --- 

`src/scx/spring.py` & Spring 自演化门控 & --- 

`src/scx/state/` & State Crystallization + 双层状态发现 & 10
文件 

`src/scx/expert/` & 专家注册、路由、冲突检测、可靠性估计 & 4
文件 

`src/scx/valuation/` & 噪声评分、自适应阈值、冗余检测、状态价值 &
8 文件 

`tests/` & 完整测试套件 & 12 文件 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 实验<!-- label: ux5b9eux9a8c -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
目录 & 实验 & 状态 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`experiments/mlip\_case/` & AlN MLIP SCX 双层审计 & ✅ 已运行 

`experiments/cifar/` & CIFAR-10/100 噪声检测 + 路由 & ✅
已运行 

`experiments/synthetic/` & 合成数据验证 & ✅ 

`scx-health/` & 医学影像 (HAM10000, MedMNIST) & ✅ 

`scx-life/drug/` & 药物靶点筛选 & ⬜ 等硬件 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 证明与推导<!-- label: ux8bc1ux660eux4e0eux63a8ux5bfc -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
目录
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`theory/self\_evolution/` & Spring 12 篇理论文件 + hostile review
+ 验证报告 

`theory/theorems/` & Theorem 1-4 的独立证明文件 

`theory/explorations/` & minimax 下界、聚类一致性、Bahadur-Rao
推导等 

`theory/self\_evolution/ppe\_rigorous\_derivation.md` & Situs
1110 行严格推导 

`theory/self\_evolution/situs\_final\_verification.md` & Situs
8/8 最终验证 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 审查记录<!-- label: ux5ba1ux67e5ux8bb0ux5f55 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
文件
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`theory/self\_evolution/final\_review\_jmlr.md` & JMLR
三理论论文审查 

`theory/self\_evolution/final\_review\_nature.md` & Nature Comp
Sci 应用论文审查 

`theory/self\_evolution/hostile\_review.md` & Situs hostile
review 

`theory/self\_evolution/spring\_hostile\_review.md` & Spring
hostile review 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 关键声明<!-- label: ux5173ux952eux58f0ux660e -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
文件
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`AUDIT\_SWORD.md` & 审计之剑------不限军用，但可独立审计 

`BUSINESS\_ARCHITECTURE.md` & 商业模式------Principal Maintainer
+ API 订阅 

`IP\_NOTE.md` & 知识产权策略 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 开发记录<!-- label: ux5f00ux53d1ux8bb0ux5f55 -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
文件 & 内容 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`DEVELOPMENT\_LOG.md` & 864 行开发日志（2026-05 到 2026-06） 

`SCX\_HISTORY.md` & 1027 行 SCX 思想进化史 

`paper/arxiv/ARCHITECTURE.md` & 四论文关系图 + SCX 分层架构 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 硬件规划<!-- label: ux786cux4ef6ux89c4ux5212 -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
文件 & 内容 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`HARDWARE\_SPEC.md` & 三档配置（¥800 / ¥45K / ¥100K） 

`HARDWARE\_ULTIMATE.md` & 终极限 ¥257K------7995WX + 4×5090 

`HARDWARE\_CHECKLIST.md` & 全栈清单（网络、软件、安全） 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 药物模块<!-- label: ux836fux7269ux6a21ux5757 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
文件
\end{minipage} & \begin{minipage}[b]
内容
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`drug-module/scripts/download\_databases.py` & 1906 行，12
数据库下载管线 

`drug-module/scripts/screen\_all\_databases.py` & 全量 drug ×
target Yajie 审计 

`drug-module/RUN\_GUIDE.md` & 一页纸运行指南 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 未包含（待补充）<!-- label: ux672aux5305ux542bux5f85ux8865ux5145 -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
项目 & 状态 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
AlN v3 DFT 数据 (534 帧) & 未上传（大文件） 

State Crystallization vs BPE 形式化对比 & 未完成 

推测解码 (DSpark) 交叉验证 & 未完成 

12 药物数据库原始数据 & 未下载 

\end{longtable}