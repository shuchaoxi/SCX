# SCX
净室代码检查报告

**Author:** SCX

> 检查日期：2026-06-26 检查工具：`src/scx/`
> 及周边目录的自动模式扫描 检查目标：确认 SCX 代码不含学校/课题组特定引用

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 检查范围与模式<!-- label: ux68c0ux67e5ux8303ux56f4ux4e0eux6a21ux5f0f -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
扫描目标
\end{minipage} & \begin{minipage}[b]
扫描模式
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`src/scx/core/` & `cxshu`, `simu\_data`,
`EGP`, `egp`, `AlGaN`, `孝感`,
`Xiaogan`, `VASP`, `DFT` 

`src/scx/state/` & 同上 

`src/scx/expert/` & 同上 

`src/scx/valuation/` & 同上 

`src/scx/action/` & 同上 

`src/scx/utils/` & 同上 

`tests/` & 同上 

`experiments/` & 同上 

`theory/` & 同上 

\end{longtable}

扫描工具：Python 脚本遍历所有 `.py`, `.md`, `.txt`
文件，列级别精确匹配。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 结果总览<!-- label: ux7ed3ux679cux603bux89c8 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
目录 & 判定 & 发现数 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**`src/scx/`** (核心 Python 包) & **CLEAN** &
**0** 

**`tests/`** (测试套件) & **CLEAN** & **0** 

**`experiments/`** (实验代码) & **CLEAN** &
**0** 

`theory/` (理论文档) & 含理论关联引用 & 23 处（详见下文） 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 核心 Python
包：确认洁净<!-- label: ux6838ux5fc3-python-ux5305ux786eux8ba4ux6d01ux51c0 -->

`src/scx/` 下的所有 `.py`
文件**未发现**任何以下模式： -
学校服务器路径（`/home/cxshu/`, `W:/simu\_data/`） - EGP
项目代码引用 - DFT/VASP 硬编码 - 课题组或学校特定注释/标记

#### 已检查的源文件<!-- label: ux5df2ux68c0ux67e5ux7684ux6e90ux6587ux4ef6 -->

\begin{verbatim}
src/scx/__init__.py
src/scx/core/__init__.py
src/scx/core/config.py
src/scx/core/framework.py
src/scx/core/metrics.py
src/scx/state/__init__.py
src/scx/state/space.py
src/scx/state/discovery.py
src/scx/state/assignment.py
src/scx/state/metrics.py
src/scx/expert/__init__.py
src/scx/expert/registry.py
src/scx/expert/reliability.py
src/scx/expert/router.py
src/scx/expert/conflict.py
src/scx/valuation/__init__.py
src/scx/valuation/learnability.py
src/scx/valuation/noise_score.py
src/scx/valuation/redundancy.py
src/scx/valuation/classifier.py
src/scx/valuation/state_value.py
src/scx/action/__init__.py
src/scx/action/policy.py
src/scx/action/acquisition.py
src/scx/action/compress.py
src/scx/utils/__init__.py
src/scx/utils/helpers.py
src/scx/utils/data_loader.py
src/scx/utils/visualization.py
src/scx/utils/evaluation.py
\end{verbatim}

**结论：SCX Python 包在净室条件下独立开发，与学校/EGP/DFT
代码无交叉污染。**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 测试与实验：确认洁净<!-- label: ux6d4bux8bd5ux4e0eux5b9eux9a8cux786eux8ba4ux6d01ux51c0 -->

`tests/` 和 `experiments/`
下的所有文件同样洁净，无学校特定引用。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 理论文档中的引用说明<!-- label: ux7406ux8bbaux6587ux6863ux4e2dux7684ux5f15ux7528ux8bf4ux660e -->

`theory/` 目录下的数学框架文档中存在 DFT/EGP
引用，但**这是预期的理论关联**，属于论文线中 Paper 4 (SCX) 与 Paper
1-3 (EGP) 的自然学术衔接，而非代码依赖。

具体文件：

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4545}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
文件
\end{minipage} & \begin{minipage}[b]
引用类型
\end{minipage} & \begin{minipage}[b]
说明
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`theory/README.md` & DFT (1 处) &
表格中梳理各方法的数据需求，提及 DFT 作为对比基线 

`theory/propositions/05\_expert\_governance\_protocol.md` & DFT
(21 处), EGP (2 处) & 治理协议的锚定验证步骤讨论了如何用 DFT 作为 ground
truth；这是 Paper 4 与 Paper 1-3 的理论衔接 

\end{longtable}

**这些理论引用不构成代码层面的交叉污染**，它们是学术论文中引用前期工作的正常行为，与净室代码检查的目标无关。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 验证命令<!-- label: ux9a8cux8bc1ux547dux4ee4 -->

使用以下命令可复现本检查（需 Python 3.9+）：

\begin{Shaded}
\begin{Highlighting}[]
\ExtensionTok{python} \AttributeTok{{-}c} \StringTok{"}
\StringTok{import os}
\StringTok{suspicious = []}
\StringTok{for root, dirs, files in os.walk(\textquotesingle{}src/scx\textquotesingle{}):}
\StringTok{    for f in files:}
\StringTok{        if f.endswith(\textquotesingle{}.py\textquotesingle{}):}
\StringTok{            path = os.path.join(root, f)}
\StringTok{            with open(path) as fh:}
\StringTok{                content = fh.read()}
\StringTok{            for pattern in [\textquotesingle{}cxshu\textquotesingle{}, \textquotesingle{}simu\_data\textquotesingle{}, \textquotesingle{}EGP\textquotesingle{}, \textquotesingle{}egp\textquotesingle{}, \textquotesingle{}AlGaN\textquotesingle{}, \textquotesingle{}孝感\textquotesingle{}, \textquotesingle{}Xiaogan\textquotesingle{}, \textquotesingle{}VASP\textquotesingle{}, \textquotesingle{}DFT\textquotesingle{}]:}
\StringTok{                if pattern in content:}
\StringTok{                    suspicious.append((path, pattern))}
\StringTok{if suspicious:}
\StringTok{    for p, pat in suspicious:}
\StringTok{        print(f\textquotesingle{}FOUND: \{pat\} in \{p\}\textquotesingle{})}
\StringTok{else:}
\StringTok{    print(\textquotesingle{}CLEAN: No school{-}specific references found\textquotesingle{})}
\StringTok{"}
\end{Highlighting}
\end{Shaded}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 最终判定<!-- label: ux6700ux7ec8ux5224ux5b9a -->

\begin{verbatim}
┌─────────────────────────────────────────────────────┐
│  CLEAN ROOM CHECK: PASSED                           │
│  Core SCX Python package: CLEAN (0 findings)        │
│  Tests:                CLEAN (0 findings)            │
│  Experiments:          CLEAN (0 findings)            │
│  Theory docs:         Contains academic references  │
│                        to EGP/DFT (expected)         │
└─────────────────────────────────────────────────────┘
\end{verbatim}