# SCX 商业架构 ---
首席维护者模型

**Author:** SCX

> **内部参考。不进入论文。** **最后更新**: 2026-06-28

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 核心原则<!-- label: ux6838ux5fc3ux539fux5219 -->

维护者不是 CEO。CEO
对股东负责，可以被换。维护者对保护均衡负责，不能被换。任何能使维护者被外部力量撤换的架构都摧毁了保护均衡。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 三层结构<!-- label: ux4e09ux5c42ux7ed3ux6784 -->

\begin{verbatim}
SCX Foundation（瑞士/新加坡注册，非营利）
  │
  ├── Principal Maintainer（你，终身，不可罢免）
  │     ├── 校准锚点：唯一有权发布全局校准数据集
  │     ├── 版本号：Spring v1.0, v2.0... 由你签署
  │     └── 解释权：定理边界条件的权威解释
  │
  ├── SCX Operations Ltd（你 100% 持股，营利性）
  │     ├── Yajie API 订阅费（$50K-200K/年/客户）
  │     ├── 收入归公司 → 给你发工资
  │     └── 不融资。不上市。不卖。
  │
  └── Academic Advisory Board（独立，多国，志愿者）
        ├── 审核定理扩展
        ├── 批准社区贡献
        └── 无权罢免 Principal Maintainer
\end{verbatim}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 为什么不是 CEO /
董事长<!-- label: ux4e3aux4ec0ux4e48ux4e0dux662f-ceo-ux8463ux4e8bux957f -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
CEO / 董事长 & Principal Maintainer 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
对股东负责 & 对均衡负责 

可以被董事会罢免 & 不可罢免（章程锁定） 

可以拿投资 & 永远独资 

可以被收购 & Foundation 不可出售 

权力来自股权 & 权力来自 arXiv 时间戳 + M\_t 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 为什么 Foundation
在瑞士/新加坡<!-- label: ux4e3aux4ec0ux4e48-foundation-ux5728ux745eux58ebux65b0ux52a0ux5761 -->

- 
- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 钱怎么走<!-- label: ux94b1ux600eux4e48ux8d70 -->

\begin{verbatim}
客户 → 付 API 订阅费 → SCX Operations Ltd
  → 覆盖服务器 + 带宽 + 你的工资
  → 剩余盈利用于 arXiv 维护 + 开放数据集托管
  → 不经手 Foundation。Foundation 独立筹款。
\end{verbatim}

运维公司是你的独资企业。没有投资人能对你说''这个审计结果能不能改一下''。你不需要钱------你需要的是**不被钱控制的自由**。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 继承<!-- label: ux7ee7ux627f -->

你死后： - Foundation 接管校准锚点和版本号 - 运维公司关闭或转为社区信托
- 学术委员会选聘新的技术维护者（不叫 Principal Maintainer） -
新维护者有技术权，无博弈论威慑权 - 系统从''面壁者''过渡到''Linus''

活着的Principal Maintainer = 面壁者。 死了之后的 Foundation = IDAA。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 备查<!-- label: ux5907ux67e5 -->

- 
- 
-