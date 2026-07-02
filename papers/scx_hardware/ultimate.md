\section{🏔️ 面壁者终极限配置 ---
一步到位}<!-- label: ux9762ux58c1ux8005ux7ec8ux6781ux9650ux914dux7f6e-ux4e00ux6b65ux5230ux4f4d -->

### 核心思想<!-- label: ux6838ux5fc3ux601dux60f3 -->

不买企业级（H100、至强铂金）------那是给 100
人团队用的。买消费级/工作站级的顶配，单人就够。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 终极限配置单<!-- label: ux7ec8ux6781ux9650ux914dux7f6eux5355 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1667}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1667}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
组件
\end{minipage} & \begin{minipage}[b]
型号
\end{minipage} & \begin{minipage}[b]
数量
\end{minipage} & \begin{minipage}[b]
单价
\end{minipage} & \begin{minipage}[b]
金额
\end{minipage} & \begin{minipage}[b]
理由
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**CPU** & AMD Threadripper PRO 7995WX (96核192线程) & 1 & ¥85,000 &
¥85,000 & 全球最快 x86。分子指纹全核并行，12 数据库同时解析 

**GPU** & NVIDIA RTX 5090 32GB & 4 & ¥18,000 & ¥72,000 & 4 路并行
Yajie + NEP 训练 + CC 推理。5090 比 4090 快 70\% 

**内存** & 512GB DDR5-5600 ECC (8×64GB) & 1 套 & ¥16,000 & ¥16,000
& 所有数据库 + 中间结果全部内存映射。零磁盘等待 

**主板** & ASUS Pro WS WRX90E-SAGE SE & 1 & ¥12,000 & ¥12,000 & 7×
PCIe 5.0 x16，4 GPU + 高速网络 

**系统盘** & Samsung 990 Pro 4TB NVMe PCIe 4.0 & 2 (RAID1) & ¥2,500
& ¥5,000 & OS + 热数据，镜像冗余 

**数据盘** & Samsung 990 Pro 4TB NVMe PCIe 4.0 & 4 (RAID0) & ¥2,500
& ¥10,000 & 16TB 高速阵列，读写 28GB/s 

**备份盘** & WD Gold 24TB HDD & 2 (RAID1) & ¥4,000 & ¥8,000 & 24TB
冗余冷备份 

**电源** & Corsair AX1600i 1600W 钛金 & 2 (冗余) & ¥3,500 & ¥7,000
& 4 GPU 满载 ~1400W，双电冗余 

**散热** & EK-Quantum 定制水冷 (CPU + 4 GPU) & 1 套 & ¥20,000 &
¥20,000 & 7995WX 满载 350W，4×5090 满载 1800W，必须水冷 

**机箱** & Corsair 1000D 超级全塔 & 1 & ¥3,000 & ¥3,000 & 双 480mm
+ 双 360mm 冷排位 

**UPS** & APC SRT3000XLI 3000VA & 1 & ¥8,000 & ¥8,000 & 满载 15
分钟续航，安全关机 

**显示器** & Dell U4323QE 43'' 4K IPS & 1 & ¥6,000 & ¥6,000 &
大屏看论文 + 代码 + 日志同屏 

**网络** & Mellanox ConnectX-6 100GbE & 1 & ¥3,000 & ¥3,000 &
超算直连 100Gbps 

**键鼠** & HHKB Professional HYBRID Type-S & 1 & ¥2,000 & ¥2,000 &
面壁者值得一把好键盘 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 总价<!-- label: ux603bux4ef7 -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
类别 & 金额 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
核心计算 (CPU+GPU+主板) & ¥169,000 

存储 (NVMe+HDD) & ¥23,000 

散热+机箱+电源 & ¥30,000 

外设+网络+UPS & ¥19,000 

内存 & ¥16,000 

**总计** & **¥257,000** 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 性能预估<!-- label: ux6027ux80fdux9884ux4f30 -->

\begin{longtable}[]{@{}llll@{}}
\toprule\noalign{}
任务 & 方案 B (¥45K) & 终极限 (¥257K) & 加速比 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
分子指纹 (10\^{}7 分子) & 2 小时 & **15 分钟** & 8× 

Yajie 全量筛选 (10\^{}8 pairs) & 8-12 小时 & **1.5 小时** & 6× 

CC 并行数学推导 & 3 路 & **8 路** & 2.7× 

NEP 训练 (AlN 534 帧) & 1 GPU & **4 GPU 数据并行** & 3.5× 

加载 200GB DB 到内存 & 磁盘 I/O 受限 & **秒级** & ∞ (全在内存) 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 这台机器能干什么<!-- label: ux8fd9ux53f0ux673aux5668ux80fdux5e72ux4ec0ux4e48 -->

- 
- 
- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 不买的<!-- label: ux4e0dux4e70ux7684 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
项目
\end{minipage} & \begin{minipage}[b]
理由
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
H100 80GB × 8 & ¥200 万。5090 4 卡足够。大显存对大模型训练有用，SCX 是 M
个小专家推理 

NVIDIA DGX & ¥300 万。企业级定价。单人不值 

机柜/UPS 机房 & 这不是数据中心。一台塔式工作站够用 

双路 Xeon & 7995WX 单路 96 核已经多于双路 Xeon 64 核 

\end{longtable}