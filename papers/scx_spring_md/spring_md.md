<div align="center">

**版本：** v1.0 \quad | \quad
**状态：** 预印本 \quad | \quad
**分类：** SCX理论体系 — 分子模拟卷·Spring MD工程实现篇

</div>

*Abstract:*

本文提出\SpringMD{}——第一款端到端的、训练即审计的势函数训练与分子动力学运行软件。
\SpringMD{}将Spring{}自演化多专家训练循环、Yajie{}共识审计、$M_t$共生绑定、\Arbiter{}审计报告
整合为四个子命令的统一工作流：`spring-md train`（训练）、`spring-md run`（运行）、
`spring-md audit`（审计）、`spring-md compare`（对比）。

\SpringMD{}的核心工程主张有三：
**第一，BORN AUDITED势函数。** 通过Spring{}训练循环产生的每一个势函数，在训练完成之时即携
带$M_t$、Cercis{}评分、Yajie{}共识向量——势函数与审计元数据不可分离。
这是第一款在势函数层面实现"born audited"的MD软件。
**第二，审计报告而非裸轨迹。** \SpringMD{}的分子动力学模拟产出不仅是原子轨迹（trajectory），
还包含\Arbiter{}审计报告——逐帧的Cercis{}评分、Yajie{}共识度、势函数适用域诊断。
用户不再需要信任一个裸的轨迹文件；审计报告告诉用户模拟的每一帧是否可靠。
**第三，统一审计工作流。** \SpringMD{}用一个命令替代了NEP/DeepMD/MACE各自独立的训练管道
——训练、验证、审计不再分离。

本文详细描述了\SpringMD{}的软件架构、四个子命令的完整规范、数据格式与API接口、
与LAMMPS/ASE的兼容性设计、\Arbiter{}审计报告的生成逻辑，
以及端到端的使用示例。本文是SCX Spring理论体系的工程实现论文——使所有定理成为可执行的代码。

**关键词：** Spring MD；势函数训练；分子动力学；训练即审计；Arbiter审计报告；
Yajie共识；Cercis评分；LAMMPS接口；ASE接口；软件工程

---

## 引言：分子动力学软件的审计真空

### 从DFT到MD模拟：信任链的断裂

分子动力学（Molecular Dynamics, MD）模拟是现代材料科学、化学、生物物理的基石计算工具。
一个典型的MD工作流包含以下步骤：

1. **第一性原理计算：** 使用密度泛函理论（DFT）对数千个原子构型计算参考能量和力。
2. **势函数训练：** 使用机器学习方法（NEP、DeepMD、ACE、GAP、MTP等）拟合DFT数据，
3. **分子动力学模拟：** 将训练好的势函数加载到MD引擎（LAMMPS、ASE等），
4. **轨迹分析：** 对MD模拟产生的轨迹进行后处理——计算径向分布函数、

在这一工作流中，存在一个\**结构性的信任链断裂**：

- DFT计算的质量取决于交换关联泛函的选择、k点采样、截断能等参数——这些选择的可靠性
- 势函数训练的质量通常以测试集RMSE衡量——但RMSE是聚合统计量，
- MD模拟的质量假设势函数在模拟的所有构型上都可靠——这是一个\*从未被验证的假设*。
- 轨迹分析的质量假设模拟轨迹是物理真实的——但这一假设建立在上述所有未经验证的环节之上。

> **诚实暴击:** 现有MD软件（LAMMPS、GROMACS、ASE、VASP等）在势函数可靠性和模拟轨迹可信度
这两个核心问题上处于"信任我"（trust-me）模式——用户被要求信任软件的输出，而没有任何内建机制
来验证这一信任是否应该被给予。}

### SCX审计理论在MD领域的工程含义

SCX{}理论体系 [cite]已经证明：

1. 单模型（$M=1$）无法自审计——NEP、DeepMD、ACE、GAP、MTP均属于此列（SCX定理2）。
2. $M>1$个独立专家提供指数增长的误差检测能力（SCX定理1）。
3. 审计必须内建于训练过程，不能事后追加（SCX定理3）。
4. Spring{}自演化训练循环实现了"训练即审计"（Spring Trainer论文 [cite]）。

这些理论的\**工程含义**是清晰的：需要一款软件，将训练-审计-运行-验证整合为单一工作流，
使得审计信息从训练阶段无缝传递到运行阶段，最终产出自带审计报告的模拟结果。

\SpringMD{}正是这一工程含义的实现。

### Spring MD的定位与核心主张

\SpringMD{}不是又一
个势函数训练器（与NEP/DeepMD/ACE竞争），也不是又一个MD引擎（与LAMMPS/GROMACS竞争）。
它的定位是\**审计中间件**（Audit Middleware）——位于训练器和引擎之间的审计层，
确保从DFT数据到最终模拟报告的整个链路都是可审计的。

\SpringMD{}的五项核心主张：

1. **BORN AUDITED势函数：**
2. **审计报告而非裸轨迹：**
3. **替代NEP/DeepMD/MACE训练管道：**
4. **LAMMPS/ASE兼容：**
5. **端到端审计闭环：**

### 术语约定

- **PES（Potential Energy Surface）：** 势能面——体系总能量作为原子坐标的函数$E(\mathbf{R})$。
- **势函数（Potential Function）：** PES的参数化近似$V_\theta(\mathbf{R}) \approx E(\mathbf{R})$。
- **轨迹（Trajectory）：** MD模拟产生的时间序列$\{\mathbf{R}(t_1), ..., \mathbf{R}(t_T)\}$。
- **审计报告（Audit Report）：** \Arbiter{}对轨迹的逐帧诊断，包含Cercis{}评分、Yajie{}共识度和OOD标志。
- **Born Audited：** 审计信息在势函数/轨迹诞生之时即已绑定，不可分离。

### 本文结构

1. 第2节：软件架构总览——\SpringMD{}的四命令工作流。
2. 第3节：`spring-md train`——训练即审计的势函数学习管道。
3. 第4节：`spring-md run`——审计注入的分子动力学运行。
4. 第5节：`spring-md audit`——已有轨迹的独立审计。
5. 第6节：`spring-md compare`——多势函数的Cercis{}排名。
6. 第7节：\Arbiter{}审计报告——格式、字段、生成逻辑。
7. 第8节：数据格式与API——势函数格式、轨迹格式、审计报告格式。
8. 第9节：LAMMPS/ASE兼容性设计。
9. 第10节：端到端使用示例。
10. 第11节：与NEP/DeepMD/MACE的工程对比。
11. 第12节：讨论——诚实暴击、适用边界、未来方向。
12. 第13节：结论。

---

## 软件架构总览：Spring MD的四命令工作流

### 顶层架构

\SpringMD{}由一个命令行入口`spring-md`和四个子命令构成：

[Figure omitted — see original .tex]

### 四命令的职责划分

[Table omitted — see original .tex]

### 审计信息流：从训练到运行的贯通

\SpringMD{}区别于所有现有MD软件的核心特征，是审计信息从训练到运行的\**无缝贯通**：

1. **训练阶段（`train`）：**
2. **运行阶段（`run`）：**
3. **独立审计阶段（`audit`）：**
4. **对比排名阶段（`compare`）：**

> **Remark:** [审计不可绕过]
> \SpringMD{}的软件设计遵循一条强制原则：\**审计不可绕过**（Audit Non-Bypassability）。
> `spring-md run`在执行MD模拟时\*必须*同时运行\Arbiter{}审计引擎——
> 不存在"只跑模拟不审计"的模式。这不是一个可选的flag，而是软件的硬编码行为。
> 如果用户确实只需要裸轨迹，他们可以使用原始的LAMMPS或ASE——\SpringMD{}的定位是审计中间件。

---

## `spring-md train：训练即审计的势函数学习管道`

### 命令规范

\begin{lstlisting}[caption={`spring-md train` 命令语法},label=lst:train]
spring-md train [OPTIONS] <INPUT>

INPUT:
  <data.xyz>           DFT训练数据 (extended XYZ格式)
  <data.npz>           或NPZ格式 ({R, E, F, Z})

OPTIONS:
  --config <FILE>       Spring训练配置文件 (YAML)
  --output <DIR>        输出目录 (默认: ./spring_output/)
  --arch <ARCH>         专家架构: nep | deepmd | ace | mace (默认: nep)
  --M-min <INT>         最小专家数 (默认: 3)
  --M-max <INT>         最大专家数 (默认: 32)
  --epochs <INT>        最大训练轮数 (默认: 1000)
  --batch-size <INT>    批次大小 (默认: 32)
  --lr <FLOAT>          学习率 (默认: 1e-3)
  --noise-threshold <FLOAT>  Yajie噪声过滤阈值 (默认: 0.05)
  --device <STR>        计算设备: cuda | cpu (默认: cuda)
  --seed <INT>          随机种子 (默认: 42)

OUTPUT (在 <DIR>/ 下):
  potential.pt          共识势函数 (PyTorch格式)
  potential.yaml        势函数元数据 (YAML格式)
  audit_report.json     Cercis评分 + Yajie向量 + Mt + Lyapunov
  training_log.csv      训练日志 (loss, consensus, lyap per epoch)
  checkpoints/          训练检查点目录
\end{lstlisting}

### 训练管道的五个阶段

`spring-md train`的内部管道由五个顺序阶段构成，对应Spring{}自演化训练循环的五项内生产出。

[Figure omitted — see original .tex]

#### 阶段1：数据喂入（Data Ingestion）

从DFT计算输出加载训练数据。支持的输入格式：

- **extended XYZ：** 标准原子构型格式，包含晶格矢量、原子坐标、物种、能量、力、应力。
- **NPZ：** 紧凑的NumPy字典格式，键为`R`（坐标，$N_{data} \times N_{atoms} \times 3$）、

数据验证步骤：

1. 检查每个构型的原子数一致性（同一体系）；
2. 检查能量/力的数值范围，标记异常值（$|E| > 10^6$ eV或$|F| > 10^4$ eV/Å）；
3. 计算数据复杂度$\Sigma_0(\D)$（式 [ref]），用于后续$M_t$自动生成；
4. 计算数据哈希$\Dhash = SHA-256(\D)$；
5. 按能量分位数进行分层划分：训练集80\%，验证集10\%，校准集10\%。

#### 阶段2：多专家训练（Multi-Expert Training）

Spring{}自演化训练循环的核心。伪代码如算法 [ref]所示。

\begin{algorithm}[H]
*Caption:* Spring自演化多专家训练循环
<!-- label: alg:spring_training -->
\begin{algorithmic}[1]
\Require 训练数据 $\D_{train}$，验证数据 $\D_{val}$，校准数据 $\D_{calib}$
\Require 最大迭代数 $T_{max}$，收敛阈值 $\varepsilon_{conv}$
\Ensure 共识势函数 $V_{consensus}$，审计元数据
\State $\Lyap_0 \gets \infty$; $t \gets 0$
\State $\mathcal{H}_{data} \gets SHA-256(\D_{train})$
\State $\Sigma_0 \gets ComputeComplexity(\D_{train})$ \Comment{数据复杂度}
\State $M_0 \gets \Xi(\mathcal{H}_{data}, \Sigma_0)$ \Comment{初始$M_t$自动生成}
\While{$t < T_{max}$ **and** $\Lyap_t > \varepsilon_{conv}$}
    \State $\{\D_1, ..., \D_{M_t}\} \gets StratifiedBootstrap(\D_{train}, M_t)$
    \State **parallel for** $m = 1$ **to** $M_t$ **do**
        \State $\theta_m^{(t)} \gets TrainExpert(\D_m, \theta_m^{init})$
            \Comment{独立训练，无梯度共享}
    \State **end parallel for**
    \State $\mathbf{s}_{Yajie}^{(t)} \gets YajieConsensus(\{f_{\theta_m}\}_{m=1}^{M_t}, \D_{calib})$
    \State $\Lyap_t \gets \frac{1}{|\D_{train}|}\sum_{i}\Var_m[f_m(\mathbf{R}_i)]$
    \State $\D_{train} \gets RemoveNoise(\D_{train}, \mathbf{s}_{Yajie}^{(t)}, \tau_{noise})$
    \State $M_{t+1} \gets \Xi(\mathcal{H}_{data}, \Lyap_t, \mathbf{s}_{Yajie}^{(t)}, \Sigma_0)$
    \State $t \gets t + 1$
\EndWhile
\State $V_{consensus} \gets \sum_{m} \omega_m f_{\theta_m}$ \Comment{逆方差加权}
\State $S_{Cercis} \gets CercisScore(V_{consensus}, \mathbf{s}_{Yajie}, \Lyap_t, \D_{val})$
\State \Return $(V_{consensus}, \mathbf{s}_{Yajie}, \Lyap_t, M_t, S_{Cercis})$
\end{algorithmic}
\end{algorithm}

#### 阶段3：Yajie{降噪（Yajie Denoising）}

Yajie{}共识机制 [cite]在Spring训练中的应用包括三项操作：

- **逐构型共识评分：** 对每个训练构型$\mathbf{R}_i$，计算$M_t$个专家的预测一致性：
- **低共识构型标记：** 评分低于$\tau_{noise}$分位数的构型被标记为"疑似噪声/异常"。
- **数据净化：** 标记的构型从下一轮训练中移除，净化后的数据返回阶段2。

> **Remark:** [降噪的理性]
> Yajie{}降噪不是武断地删除数据——它是\*多专家集体判断*的结果。
> 一个构型只有在\*所有*独立专家都无法就它的能量达成共识时，才被认为是不可靠的。
> 如果$M_t-1$个专家达成共识而仅1个分歧，该构型的评分虽降低但不会被移除——
> 这防止了单个异常模型污染全体数据。

#### 阶段4：$M_t$绑定（$M_t$ Binding）

$M_t$的自动生成与密码学绑定是\SpringMD{}实现"训练即审计"的关键机制 [cite]。

> **Definition:** [$M_t$共生绑定]<!-- label: def:Mt_binding -->
> 第$t$次迭代的专家数$\Mauto$由数据哈希$\Dhash$、Lyapunov监控量$\Lyap_{t-1}$和
> Yajie共识评分向量$\mathbf{s}_{Yajie}^{(t-1)}$共同确定：
> 
> $$<!-- label: eq:Mt_binding_formula -->
>     \Mauto = \Xi(\Dhash; \Lyap_{t-1}, \mathbf{s}_{Yajie}^{(t-1)}, \Sigma_0(\D))
> $$
> 
> 这一确定性映射确保了：给定相同的数据和相同的训练流程，产生的$M_t$是唯一确定的——
> 这就是"共生绑定"的含义：$M_t$与数据\*共生*（co-emerge），不可篡改。

> **Proposition:** [$M_t$的密码学验证性]<!-- label: prop:Mt_verifiable -->
> 任何持有原始数据$\D$的第三方可以独立重计算$\Dhash$和$\Sigma_0(\D)$，进而验证
> $M_t$是否正确生成。这种可验证性防止了"声明$M_t=8$但实际只用$M=1$训练"的欺诈行为。

#### 阶段5：Cercis{评分（Cercis Scoring）}

Cercis{}评分是\SpringMD{}为每个训练完成的势函数分配的单一质量度量 [cite]：

$$<!-- label: eq:cercis_score -->
    S_{Cercis} = Q + \eta \cdot N
$$

其中：

- $Q \in [0, 1]$：质量保证得分，基于Yajie{}平均共识度和Lyapunov收敛度：
- $N \in [0, 1]$：覆盖度得分，基于训练数据在能量空间和构型空间的覆盖：
- $\eta = 0.2$：认知折扣因子——除非经过实验验证，覆盖率评价的价值打两折。

$S_{Cercis} \in [0, 1.2]$，越接近1.2表示势函数质量越高（经过验证的广泛适用性）。

### 训练配置文件格式

`spring-md train`通过YAML配置文件控制所有训练参数：

\begin{lstlisting}[caption={`spring\_config.yaml` 示例},label=lst:config]
# Spring MD 训练配置
train:
  data:
    path: "./data/train.xyz"
    format: "extxyz"
    train_ratio: 0.8
    val_ratio: 0.1
    calib_ratio: 0.1

  model:
    architecture: "nep"        # nep | deepmd | ace | mace
    num_neurons: [30, 30]      # 隐藏层神经元数
    cutoff: 6.0                # 截断半径 (Å)
    descriptor_dim: 128        # 描述符维度

  spring:
    M_min: 3                   # 最小专家数
    M_max: 32                  # 最大专家数
    noise_fraction: 0.05       # 噪声比例先验
    consensus_threshold: 0.7   # Yajie共识阈值

  optim:
    epochs: 1000
    batch_size: 32
    learning_rate: 1.0e-3
    scheduler: "cosine"
    weight_decay: 1.0e-5

  output:
    dir: "./spring_output"
    save_checkpoints: true
    checkpoint_freq: 50
\end{lstlisting}

### 训练产出的审计元数据

每次`spring-md train`完成后，`audit\_report.json`包含以下审计元数据：

\begin{lstlisting}[caption={`audit\_report.json` 结构},label=lst:audit_json]
{
  "spring_md_version": "1.0.0",
  "timestamp": "2026-07-01T12:00:00Z",
  "data_hash": "a3f8c2...",
  "complexity": {
    "Sigma_0": 1.42,
    "energy_entropy": 3.21,
    "energy_range": [-78.5, -72.3],
    "num_species": 2,
    "num_configurations": 10000
  },
  "training": {
    "M_t": 12,
    "M_t_history": [8, 12, 12, 12],
    "total_epochs": 450,
    "converged": true,
    "Lyapunov_final": 0.0012,
    "Lyapunov_initial": 0.0450
  },
  "yajie": {
    "mean_consensus": 0.92,
    "consensus_histogram": [0, 5, 23, 142, ...],
    "noise_fraction_removed": 0.032,
    "calibration_set_size": 1000
  },
  "cercis": {
    "score": 1.08,
    "quality_Q": 0.92,
    "coverage_N": 0.80,
    "discount_eta": 0.20
  }
}
\end{lstlisting}

---

## `spring-md run：审计注入的分子动力学运行`

### 命令规范

\begin{lstlisting}[caption={`spring-md run` 命令语法},label=lst:run]
spring-md run [OPTIONS] <POTENTIAL> <INPUT_STRUCTURE>

INPUT:
  <POTENTIAL>            训练好的势函数文件 (potential.pt)
  <INPUT_STRUCTURE>      初始构型文件 (XYZ, POSCAR, CIF, LAMMPS data)

OPTIONS:
  --config <FILE>        MD运行配置文件 (YAML)
  --output <DIR>         输出目录 (默认: ./md_output/)
  --engine <ENGINE>      MD引擎: lammps | ase (默认: lammps)
  --ensemble <ENS>       系综: nve | nvt | npt (默认: nvt)
  --temperature <FLOAT>  温度 (K) (默认: 300)
  --timestep <FLOAT>     时间步长 (fs) (默认: 0.5)
  --steps <INT>          总步数 (默认: 100000)
  --audit-every <INT>    每多少步做一次审计 (默认: 100)
  --device <STR>         计算设备 (默认: cuda)

OUTPUT (在 <DIR>/ 下):
  trajectory.xyz         原子轨迹 (extended XYZ)
  trajectory.h5          原子轨迹 (HDF5, 含速度/力)
  arbiter_report.json    Arbiter审计报告
  md_log.txt             MD运行日志
  thermo.dat             热力学量记录 (T, P, E...)
\end{lstlisting}

### 运行管道的架构

`spring-md run`的核心设计原则是：\**\SpringMD{}本身不执行MD积分——它调用LAMMPS或ASE来执行，
但在调用前后注入审计层。**

[Figure omitted — see original .tex]

### 审计钩子（Audit Hook）的触发逻辑

\Arbiter{}审计钩子在MD模拟期间以固定频率（由`--audit-every`指定，默认每100步）触发。
每一次触发执行以下审计流程：

> **Protocol:** [Arbiter审计钩子操作流程]<!-- label: prot:audit_hook -->
> 
1. **提取当前帧构型$\mathbf{R}(t)$：** 从MD引擎获取当前原子坐标。
2. **多专家一致性检查：** 如果势函数携带$M_t>1$个专家的信息，
3. **OOD检测：** 比较$\mathbf{R}(t)$的ACE描述符与训练数据的ACE描述符分布。
4. **Cercis{}逐帧评分：**
5. **写入审计记录：** 将当前步数$t$、$s_{Yajie}$、$\sigma_E$、$\bar_F$、
6. **OOD预警（可选）：** 如果连续$n_{warn}$帧被标记为OOD（默认$n_{warn}=10$），

> **Remark:** [为什么不主动停止MD？]
> 一个合理的疑问是：当\Arbiter{}检测到OOD时，为什么不自动停止模拟？
> 答案是：**审计和执行的职责分离**。\Arbiter{}的职责是\*报告*势函数的可靠性状态，
> 而不是\*控制*MD的执行。用户可能有意探索OOD区域（例如自由能计算中的非平衡过程），
> 此时模拟的继续是有科学价值的。\Arbiter{}忠实地报告"这个区域是OOD"——
> 如何响应这一信息，是用户的决策。

### MD运行配置文件

\begin{lstlisting}[caption={`md\_config.yaml` 示例},label=lst:md_config]
# Spring MD 运行配置
run:
  engine: "lammps"            # lammps | ase
  ensemble: "nvt"             # nve | nvt | npt
  temperature: 300.0          # 温度 (K)
  pressure: 1.0               # 压力 (bar, 仅NPT)
  timestep: 0.5               # 时间步长 (fs)
  total_steps: 100000         # 总步数

  thermostat:
    type: "nose_hoover"       # nose_hoover | berendsen | langevin
    tau: 100.0                # 热浴弛豫时间 (fs)

  barostat:                   # 仅NPT
    type: "nose_hoover"
    tau: 1000.0

  audit:
    frequency: 100            # 审计频率 (步)
    ood_warn_consecutive: 10  # OOD连续预警阈值
    save_full_experts: false  # 是否保存所有专家预测

  output:
    dir: "./md_output"
    format: "xyz"             # xyz | h5 | both
    thermo_freq: 10           # 热力学量输出频率
\end{lstlisting}

### LAMMPS接口设计

当`--engine lammps`时，\SpringMD{}通过以下机制与LAMMPS交互：

1. **势函数转换：** 训练好的PyTorch势函数被序列化为LibTorch C++格式（TorchScript），
2. **LAMMPS库调用：** \SpringMD{}以Python子进程方式调用LAMMPS二进制文件，
3. **审计钩子集成：** \SpringMD{}在LAMMPS运行期间通过读取临时输出的轨迹文件
4. **性能开销：** 每次审计钩子触发的计算开销约为单步MD积分的$10\times \sim 50\times$

### ASE接口设计

当`--engine ase`时，\SpringMD{}直接使用ASE（Atomic Simulation Environment）的Python API：

1. **势函数封装：** 训练好的势函数被封装为ASE兼容的`Calculator`对象，
2. **审计钩子集成：** ASE支持自定义`Observer`回调函数。
3. **优势：** ASE接口比LAMMPS接口更紧密——审计钩子可以直接访问MD引擎的内部状态

---

## `spring-md audit：已有轨迹的独立审计`

### 命令规范

\begin{lstlisting}[caption={`spring-md audit` 命令语法},label=lst:audit]
spring-md audit [OPTIONS] <TRAJECTORY> [POTENTIAL]

INPUT:
  <TRAJECTORY>           轨迹文件 (XYZ, H5, LAMMPS dump)
  [POTENTIAL]            势函数文件 (可选; 不提供则仅做结构分析)

OPTIONS:
  --config <FILE>        审计配置文件 (YAML)
  --output <DIR>         输出目录 (默认: ./audit_output/)
  --M <INT>              审计专家数 (不提供则从势函数读取)
  --ood-method <STR>     OOD检测方法: ace_mahalanobis | knn | isolation_forest
  --per-frame            逐帧审计 (默认: 每10帧)
  --reference <FILE>     参考势函数进行交叉审计

OUTPUT (在 <DIR>/ 下):
  arbiter_report.json    Arbiter审计报告
  per_frame.csv          逐帧审计明细
  ood_analysis.json      OOD帧分析
  summary.txt            审计摘要
\end{lstlisting}

### 审计模式

`spring-md audit`支持三种审计模式，取决于是否提供势函数和参考势函数：

[Table omitted — see original .tex]

### 交叉审计的工程价值

交叉审计是`spring-md audit`最具工程价值的特性之一。其场景为：
用户使用\SpringMD{}训练了一个势函数$V_A$，想要验证$V_A$与另一个独立训练的势函数$V_B$
（可能来自不同框架，如DeepMD或MACE）在相同轨迹上是否给出一致的物理预测。

> **Protocol:** [交叉审计协议]<!-- label: prot:cross_audit -->
> 
1. 对轨迹的每一帧$\mathbf{R}(t)$，使用$V_A$和$V_B$分别计算能量$E_A(t), E_B(t)$和力$\mathbf{F}_A(t), \mathbf{F}_B(t)$。
2. 计算逐帧的能量差$\Delta E(t) = |E_A(t) - E_B(t)|$和力差$\Delta F(t) = \|\mathbf{F}_A(t) - \mathbf{F}_B(t)\|$。
3. 识别"分歧帧"——$\Delta E(t) > \varepsilon_E$或$\Delta F(t) > \varepsilon_F$的帧
4. 对分歧帧进行深入分析：检查其ACE描述符是否处于任一势函数的训练数据分布之外。
5. 计算"交叉Yajie{}共识评分"——将两个势函数视为两个"专家"：
6. 输出交叉审计报告，重点突出分歧帧及其特征。

### 无势函数的轨迹结构审计

即使在没有势函数的情况下（模式1：结构审计），`spring-md audit`也能对轨迹进行有价值的诊断：

- **能量漂移检测：** 如果轨迹包含势能信息，检测能量的系统漂移（线性拟合斜率）。
- **温度控制质量：** 从速度计算温度，检查温度波动是否在合理范围。
- **结构异常检测：** 检测异常的原子间距（过近接触）、异常配位数、
- **周期性破坏检测：** 检测原子是否因热涨落漂移出模拟盒子。
- **保守量检查：** 对于NVE系综，检查总能量守恒；对于NVT，检查温度稳定性。

> **Remark:** [结构审计的价值]
> 仅依赖轨迹文件的结构审计虽然不如完整\Arbiter{}审计（含势函数）强大，
> 但它可以在\*势函数不存在的情况下*发现MD模拟的明显问题——
> 例如能量漂移（表明积分器步长过大或势函数不光滑）、原子碰撞（表明初始构型不合理或
> 势函数排斥壁过软）等。结构审计是MD模拟质量的"第一道防线"。

---

## `spring-md compare：多势函数的Cercis排名`

### 命令规范

\begin{lstlisting}[caption={`spring-md compare` 命令语法},label=lst:compare]
spring-md compare [OPTIONS] <POTENTIALS...> --test-set <FILE>

INPUT:
  <POTENTIALS...>        两个或更多势函数文件 (potential_1.pt potential_2.pt ...)
  --test-set <FILE>      测试构型集 (extended XYZ)

OPTIONS:
  --config <FILE>        对比配置文件 (YAML)
  --output <DIR>         输出目录 (默认: ./compare_output/)
  --metrics <LIST>       对比指标: energy, forces, stress, yajie, cercis
  --per-config           逐构型详细对比 (默认: 聚合对比)
  --reference <FILE>     参考势函数 (可选; 用于"相对误差"计算)
  --plot                 生成对比图 (需要matplotlib)

OUTPUT (在 <DIR>/ 下):
  ranking.json           Cercis排名结果
  ranking.csv            排名表 (CSV)
  per_config.csv         逐构型对比 (如果 --per-config)
  comparison_report.pdf  对比报告 (如果 --plot)
\end{lstlisting}

### 对比指标的层次结构

`spring-md compare`计算的对比指标分为三个层次：

[Figure omitted — see original .tex]

### 对比算法

\begin{algorithm}[H]
*Caption:* 多势函数Cercis排名算法
<!-- label: alg:compare -->
\begin{algorithmic}[1]
\Require $K$个势函数 $\{V_k\}_{k=1}^{K}$，测试构型集 $\D_{test} = \{\mathbf{R}_i, E_i^{ref}, \mathbf{F}_i^{ref}\}_{i=1}^{N}$
\Ensure Cercis排名 $rank_k$ 和综合对比报告
\For{$k = 1$ **to** $K$}
    \State 加载势函数$V_k$及其审计元数据 $\mathcal{A}_k$
    \State **// 第一层：聚合精度**
    \For{$i = 1$ **to** $N$}
        \State $\hat{E}_i^{(k)} \gets V_k(\mathbf{R}_i)$; $\hat{\mathbf{F}}_i^{(k)} \gets -\nabla V_k(\mathbf{R}_i)$
    \EndFor
    \State $RMSE_E^{(k)} \gets \sqrt{\frac{1}{N}\sum_i (\hat{E}_i^{(k)} - E_i^{ref})^2}$
    \State $RMSE_F^{(k)} \gets \sqrt{\frac{1}{3N N_{atoms}}\sum_i \|\hat{\mathbf{F}}_i^{(k)} - \mathbf{F}_i^{ref}\|^2}$

    \State **// 第二层：审计质量**
    \If{$\mathcal{A}_k$ 包含多专家信息}
        \State 对每个测试构型计算Yajie{}共识评分 $\{s_{Yajie}^{(k)}(\mathbf{R}_i)\}$
        \State $\bar{s}_{Yajie}^{(k)} \gets \frac{1}{N}\sum_i s_{Yajie}^{(k)}(\mathbf{R}_i)$
        \State $f_{OOD}^{(k)} \gets$ 被标记为OOD的测试构型比例
    \Else
        \State $\bar{s}_{Yajie}^{(k)} \gets NaN$; $f_{OOD}^{(k)} \gets NaN$
    \EndIf

    \State **// 第三层：Cercis综合评分**
    \State $S_{Cercis}^{(k)} \gets CercisScore(V_k, \bar{s}_{Yajie}^{(k)}, RMSE_E^{(k)})$
\EndFor

\State 按$S_{Cercis}$降序排列势函数 → $rank_k$
\State \Return $\{(rank_k, S_{Cercis}^{(k)}, RMSE_E^{(k)}, \bar{s}_{Yajie}^{(k)})\}_{k=1}^{K}$
\end{algorithmic}
\end{algorithm}

### Cercis排名报告格式

\begin{lstlisting}[caption={`ranking.json` 示例},label=lst:ranking]
{
  "test_set": {
    "path": "./data/test.xyz",
    "num_configurations": 500,
    "energy_range": [-80.2, -71.5],
    "num_species": 2
  },
  "rankings": [
    {
      "rank": 1,
      "potential": "spring_nep_M12",
      "source": "spring-md train",
      "M_t": 12,
      "Cercis_score": 1.08,
      "RMSE_E": 0.85,
      "RMSE_F": 52.3,
      "Yajie_consensus": 0.92,
      "Lyapunov_final": 0.0012,
      "OOD_fraction": 0.01
    },
    {
      "rank": 2,
      "potential": "spring_nep_M8",
      "source": "spring-md train",
      "M_t": 8,
      "Cercis_score": 0.96,
      "RMSE_E": 0.92,
      "RMSE_F": 58.1,
      "Yajie_consensus": 0.87,
      "Lyapunov_final": 0.0024,
      "OOD_fraction": 0.03
    },
    {
      "rank": 3,
      "potential": "deepmd_v2",
      "source": "DeepMD-kit",
      "M_t": null,
      "Cercis_score": null,
      "RMSE_E": 0.88,
      "RMSE_F": 55.0,
      "Yajie_consensus": null,
      "OOD_fraction": null
    }
  ],
  "notes": ["DeepMD势函数缺少多专家审计信息，因此Cercis评分和Yajie共识度不可用"]
}
\end{lstlisting}

> **Remark:** [非Spring势函数的审计缺失]
> > **诚实暴击:** 来自NEP/DeepMD/MACE的势函数在`spring-md compare`中只能参与第一层比较
> （聚合精度），无法参与第二层（审计质量）和第三层（Cercis综合）的排名。
> 这不是\SpringMD{}的偏见——而是这些框架的设计缺陷：它们的训练过程不产生审计信息，
> 因此\SpringMD{}无法事后"捏造"审计元数据。第一层的RMSE排名仍然可用，
> 但它回答的是"平均而言谁拟合得更准"，而非"对于具体的构型谁更可信"。}

---

## Arbiter审计报告：格式、字段与生成逻辑

### 审计报告的设计哲学

\Arbiter{}（仲裁者）审计报告是\SpringMD{}区别于所有现有MD软件的核心产出物。
其设计哲学遵循三条原则：

1. **审计不可分离（Audit Non-Separability）：**
2. **逐帧可追溯（Per-Frame Traceability）：**
3. **人机双读（Human-Machine Dual-Readability）：**

### 审计报告的完整Schema

[Table omitted — see original .tex]

### 审计报告的可视化摘要

\Arbiter{}审计报告的`summary`部分提供了轨迹整体质量的快速诊断：

- **良好轨迹（Healthy Trajectory）：**
- **警告轨迹（Warning Trajectory）：**
- **不可靠轨迹（Unreliable Trajectory）：**

---

## 数据格式与API

### 势函数文件格式

\SpringMD{}的势函数以两种互补格式存储：

1. **PyTorch二进制格式（`potential.pt`）：**
2. **YAML元数据格式（`potential.yaml`）：**

### 势函数加载API

\begin{lstlisting}[caption={Python API：加载势函数},label=lst:api_load]
from spring_md import SpringPotential

# 加载训练好的势函数
potential = SpringPotential.load("spring_output/potential.pt")

# 获取共识预测
energy = potential.predict_energy(positions, cell, atomic_numbers)
forces = potential.predict_forces(positions, cell, atomic_numbers)

# 获取多专家预测（用于审计）
expert_energies = potential.predict_energy_all_experts(positions, cell, atomic_numbers)

# 获取审计元数据
meta = potential.audit_metadata
print(f"M_t = {meta['M_t']}")
print(f"Cercis = {meta['Cercis_score']}")
print(f"Yajie consensus = {meta['Yajie_mean_consensus']}")
\end{lstlisting}

### 轨迹格式

\SpringMD{}支持的轨迹格式：

[Table omitted — see original .tex]

### \Arbiter{审计报告API}

\begin{lstlisting}[caption={Python API：加载和分析审计报告},label=lst:api_arbiter]
from spring_md import ArbiterReport

# 加载审计报告
report = ArbiterReport.load("md_output/arbiter_report.json")

# 获取摘要
print(report.summary())
# => "Healthy: 99.2% consensus, 1.3% OOD, Cercis 0.89"

# 获取OOD帧列表
ood_frames = report.get_ood_frames(threshold=0.5)
for frame in ood_frames:
    print(f"Step {frame.step}: OOD score = {frame.OOD_score:.2f}")

# 获取共识度低于阈值的帧
low_consensus = report.get_frames_by_flag("low_consensus")

# 绘制共识度随时间的变化
report.plot_consensus_over_time(save="consensus_plot.png")

# 导出为CSV
report.export_csv("arbiter_report.csv")
\end{lstlisting}

---

## LAMMPS/ASE兼容性设计

### 设计原则：审计层透明注入

\SpringMD{}与LAMMPS和ASE的兼容遵循一条核心原则：\**审计层透明注入**（Transparent Audit Injection）。
这意味着：

1. \SpringMD{}不修改LAMMPS或ASE的源代码。
2. \SpringMD{}不修改LAMMPS或ASE的输入/输出格式——任何原生LAMMPS/ASE脚本
3. 审计过程的添加对用户是可见的（通过审计报告），但对MD引擎是透明的（引擎不知道审计的存在）。

### LAMMPS集成细节

\begin{lstlisting}[caption={LAMMPS集成：Python端代码},label=lst:lammps_integration]
import subprocess
from spring_md import SpringPotential, ArbiterHook

# 1. 加载势函数并生成LAMMPS势函数文件
potential = SpringPotential.load("potential.pt")
potential.export_lammps("spring_potential.so")  # TorchScript → LAMMPS pair style

# 2. 生成LAMMPS输入脚本
lammps_script = f"""
units          metal
atom_style     atomic
pair_style     spring_md
pair_coeff     * * spring_potential.so {element_list}

read_data      input.data
velocity       all create {temp} {seed}
fix            nvt all nvt temp {temp} {temp} {tau}
thermo         {thermo_freq}
thermo_style   custom step temp pe ke etotal press
dump           traj all xyz {dump_freq} trajectory.xyz
run            {total_steps}
"""

with open("in.spring", "w") as f:
    f.write(lammps_script)

# 3. 启动LAMMPS（后台）
proc = subprocess.Popen(
    ["lmp", "-in", "in.spring"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

# 4. 注册Arbiter审计钩子
hook = ArbiterHook(
    potential=potential,
    trajectory_file="trajectory.xyz",
    audit_every=100,
    output="arbiter_report.json"
)
hook.attach_to_process(proc)  # 监控子进程，在每k步后读取trajectory.xyz并审计

proc.wait()
hook.finalize()  # 写入最终审计报告
\end{lstlisting}

### ASE集成细节

ASE集成更简单，因为ASE的所有组件都是Python对象：

\begin{lstlisting}[caption={ASE集成：Python端代码},label=lst:ase_integration]
from ase.io import read
from ase.md.nvt import NVTBerendsen
from ase import units
from spring_md import SpringPotential, ArbiterObserver

# 1. 加载势函数，封装为ASE Calculator
potential = SpringPotential.load("potential.pt")
atoms = read("input.xyz")
atoms.calc = potential.to_ase_calculator()

# 2. 设置MD
dyn = NVTBerendsen(
    atoms,
    timestep=0.5 * units.fs,
    temperature=300 * units.kB,
    taut=100 * units.fs
)

# 3. 注册Arbiter审计观察者
observer = ArbiterObserver(
    potential=potential,
    audit_every=100,
    output="arbiter_report.json"
)
dyn.attach(observer, interval=100)

# 4. 运行MD
trajectory_writer = Trajectory("trajectory.traj", "w", atoms)
dyn.attach(trajectory_writer.write, interval=10)
dyn.run(100000)

# 5. 生成审计报告
observer.save_report()
\end{lstlisting}

### 支持的功能矩阵

[Table omitted — see original .tex]

---

## 端到端使用示例

### 示例1：从DFT数据到审计轨迹的完整工作流

以下是一个完整的端到端工作流——从原始DFT数据开始，到产生自带审计报告的MD轨迹：

\begin{lstlisting}[caption={端到端工作流},label=lst:workflow]
# ================================================================
# 步骤1：准备DFT训练数据
# ================================================================
# DFT数据已由VASP/CP2K/Quantum ESPRESSO生成，格式为extended XYZ
# 文件名：data/dft_train.xyz (10000个构型)

# ================================================================
# 步骤2：训练势函数
# ================================================================
spring-md train data/dft_train.xyz \
    --config configs/train.yaml \
    --arch nep \
    --output ./outputs/Si_potential \
    --device cuda

# 输出（在 ./outputs/Si_potential/ 下）：
#   potential.pt          ← 共识势函数
#   potential.yaml        ← 人类可读的元数据
#   audit_report.json     ← Cercis评分 + Yajie + Mt
#   training_log.csv      ← 训练日志

# ================================================================
# 步骤3：检查训练产出的审计信息
# ================================================================
cat ./outputs/Si_potential/potential.yaml
# 输出：
#   Cercis_score: 1.08
#   M_t: 12
#   Yajie_mean_consensus: 0.92
#   Lyapunov_final: 0.0012
#   Data_hash: a3f8c2e1...

# ================================================================
# 步骤4：运行MD模拟（带Arbiter审计）
# ================================================================
spring-md run ./outputs/Si_potential/potential.pt data/initial_Si.xyz \
    --config configs/md.yaml \
    --engine lammps \
    --ensemble nvt \
    --temperature 300 \
    --steps 100000 \
    --audit-every 100 \
    --output ./outputs/Si_md_run

# 输出（在 ./outputs/Si_md_run/ 下）：
#   trajectory.xyz        ← 原子轨迹
#   arbiter_report.json   ← Arbiter审计报告
#   thermo.dat            ← 热力学量
#   md_log.txt            ← MD日志

# ================================================================
# 步骤5：审查审计报告
# ================================================================
spring-md audit ./outputs/Si_md_run/trajectory.xyz \
    ./outputs/Si_potential/potential.pt \
    --output ./outputs/Si_md_audit

# 或者，使用Python API进行更详细的分析
python -c "
from spring_md import ArbiterReport
report = ArbiterReport.load('./outputs/Si_md_run/arbiter_report.json')
print(report.summary())
report.plot_consensus_over_time('consensus.png')
ood = report.get_ood_frames()
print(f'OOD frames: {len(ood)}/{report.summary_data[\"total_frames\"]}')
"

# ================================================================
# 步骤6：对比多个势函数（可选）
# ================================================================
spring-md compare \
    ./outputs/Si_potential/potential.pt \
    ./outputs/Si_potential_alt/potential.pt \
    ./external/deepmd_Si.pb \
    --test-set data/test_Si.xyz \
    --output ./outputs/Si_comparison

# 查看排名
cat ./outputs/Si_comparison/ranking.json
\end{lstlisting}

### 示例2：第三方轨迹的独立审计

用户拥有来自传统LAMMPS运行的轨迹（未经\SpringMD{}），想要评估其可靠性：

\begin{lstlisting}[caption={第三方轨迹审计},label=lst:third_party]
# 场景：用户有一个LAMMPS dump轨迹（来自DeepMD势函数的模拟）
# 想要使用Spring MD进行独立审计

# 步骤1：仅结构审计（不需要势函数）
spring-md audit legacy_run/dump.lammpstrj \
    --output ./audit_legacy

# 输出：结构分析——能量漂移、异常键长、温度稳定性等

# 步骤2：如果用户有自己的Spring势函数，使用交叉审计
# （将Spring势函数的预测与原始模拟的预测对比）
spring-md audit legacy_run/dump.lammpstrj \
    ./outputs/Si_potential/potential.pt \
    --output ./audit_legacy_cross

# 输出：交叉审计报告——Spring势函数 vs 原始DeepMD势函数
# 重点：识别两个势函数预测分歧的帧
\end{lstlisting}

### 示例3：高吞吐量材料筛选

对数百种材料成分进行自动化的势函数训练、模拟和审计：

\begin{lstlisting}[caption={高吞吐量材料筛选},label=lst:high_throughput]
#!/bin/bash
# 高吞吐量材料筛选脚本

MATERIALS=("Si" "SiO2" "SiC" "Si3N4" "Al2O3" "MgO" "TiN" "ZrO2")

for mat in "${MATERIALS[@]}"; do
    echo "=== Processing $mat ==="

    # 训练
    spring-md train data/${mat}_dft.xyz \
        --output ./ht_outputs/${mat}_potential \
        --config configs/ht_train.yaml

    # 读取Cercis评分
    CERCIS=$(python -c "
import json
with open('./ht_outputs/${mat}_potential/audit_report.json') as f:
    print(json.load(f)['cercis']['score'])
")

    # 只有Cercis > 0.7的材料才进行昂贵的MD模拟
    if (( $(echo "$CERCIS > 0.7" | bc -l) )); then
        spring-md run ./ht_outputs/${mat}_potential/potential.pt \
            data/${mat}_initial.xyz \
            --output ./ht_outputs/${mat}_md \
            --config configs/ht_md.yaml
    else
        echo "Skipping $mat: Cercis score $CERCIS < 0.7"
    fi
done

# 最终排名
spring-md compare ./ht_outputs/*_potential/potential.pt \
    --test-set data/ht_test.xyz \
    --output ./ht_outputs/final_ranking
\end{lstlisting}

---

## 与NEP/DeepMD/MACE的工程对比

### 功能性对比

[Table omitted — see original .tex]

### 审计维度的根本差距

> **Definition:** [审计完备性的工程判据]<!-- label: def:audit_engineering -->
> 一款MD软件在工程意义上被称为\**审计完备**的，当且仅当：
> 
1. 势函数训练过程产生可验证的审计信息（$M_t$、Cercis{}、Yajie{}）；
2. 势函数与审计信息通过密码学手段绑定，不可分离篡改；
3. 分子动力学模拟的产出包含逐帧的审计诊断；
4. 存在独立审计命令，可对任意轨迹（包括第三方轨迹）进行审计；
5. 审计不可在软件中被绕过（非可选功能）。

根据定义 [ref]，当前所有主流MD软件（NEP、DeepMD、ACE、MACE、GAP、MTP）的
审计完备性评分为**0/5**。\SpringMD{}是第一款在所有五个维度上都满足条件的软件。

> **Remark:** [这不是营销——这是逻辑结论]
> > **诚实暴击:** 声称"Spring MD比NEP/DeepMD/MACE更好"是不准确的——这是一种误导性的比较。
> 
SpringMD{}和NEP/DeepMD/MACE解决的问题不同。NEP/DeepMD/MACE解决的是"拟合精度"问题——
> 如何用更少的参数、更快的速度、更少的数据来达到更低的RMSE。
> \SpringMD{}解决的是"审计"问题——如何确保用户知道模拟的哪些部分可信、哪些部分不可信。
> 两者不是竞争对手，而是不同维度上的工具。真正的诚实陈述是：
> 
现有工具在审计维度上是空白（0/5），\SpringMD{}填补了这一空白（5/5）。}

### 计算成本对比

\SpringMD{}的多专家训练自然比单专家训练（NEP/DeepMD/ACE）更昂贵。
但是，这一成本需要放在正确的上下文中理解：

[Table omitted — see original .tex]

> **Remark:** [成本-审计的权衡]
> $M_t=8$的\SpringMD{}训练成本约为NEP的6-8倍。这一额外的4-7×成本购买的是什么？
> 答案是：\**审计信息**——$M_t$个专家的共识/分歧模式、Yajie{}噪声诊断、逐构型的可靠性评分。
> 如果用户的科学场景是"跑一个粗略的MD然后看结果"——传统NEP/DeepMD可能足够。
> 如果用户的科学场景是"我发表的这个相的稳定性依赖于这个MD轨迹"——
> \SpringMD{}提供的审计信息可能是论文被接受或被拒稿的区别。

---

## 讨论

### 诚实暴击：Spring MD做不到的事情

作为一篇工程论文，我们有责任诚实地列出\SpringMD{}的当前局限：

1. > **诚实暴击:** 审计不等于物理真实性。}
2. > **诚实暴击:** 计算成本是真实的。}
3. > **诚实暴击:** MD模拟中的审计开销不可忽略。}
4. > **诚实暴击:** 非Spring势函数的审计能力有限。}
5. > **诚实暴击:** 生态系统不成熟。}

### 适用边界

\SpringMD{}的设计适用于以下场景：

- **高可靠性需求：** 当MD模拟的结果将用于发表、工业决策或安全评估时，
- **多势函数比较：** 当有多个候选势函数且需要系统性地选择最佳者时，
- **第三方审计：** 当需要独立验证他人的MD模拟结果时，
- **高吞吐量筛选：** 当需要对大量材料进行自动化训练-模拟-分析时，

\SpringMD{}的当前设计\**不**适用于以下场景：

- **快速原型：** 如果用户只需要快速测试一个势函数的可行性，
- **反应力场（ReaxFF）：** \SpringMD{}当前专注于机器学习势函数
- **粗粒化模拟：** \SpringMD{}当前在全原子层面操作，不支持粗粒化映射。

### 与SCX理论体系的关系

\SpringMD{}是SCX理论体系 [cite]
在分子模拟工程领域的具体实现。它在SCX体系的定位如下：

- **SCX理论卷：** 证明审计的数学基础——$M=1$不可能、$M>1$指数增长、
- **Spring框架卷 [cite]：** 提出五层统一多模态架构——
- **Spring Trainer卷 [cite]：** 定义自演化训练循环——
- **Spring MD卷（本文）：** 将上述理论工程化为可执行的软件——

### 未来方向

1. **在线学习模式：** 当前\SpringMD{}在训练和运行之间是分离的。
2. **分布式训练：** 支持多节点、多GPU的Spring多专家并行训练，
3. **审计信息可视化：** 开发基于Web的审计仪表板，
4. **预训练审计势函数库：** 建立经过\SpringMD{}审计的预训练势函数库，
5. **审计标准协议：** 与MD社区合作，将\Arbiter{}审计报告格式

---

## 结论

本文提出了\SpringMD{}——第一款将"训练即审计"理念工程化为可执行命令的分子动力学软件。
\SpringMD{}通过四个子命令（`train`、`run`、`audit`、`compare`）
实现了从DFT数据到审计完备的MD模拟报告的端到端工作流。

\SpringMD{}的核心工程贡献可以概括为三点：

1. **BORN AUDITED势函数：**
2. **审计报告而非裸轨迹：**
3. **统一审计工作流：**

> **诚实暴击:** \SpringMD{}不是"更好的NEP"或"更好的DeepMD"——它是一款在\*不同维度*上
运作的软件。传统MD软件解决的是"速率-精度"问题（更快更准的势函数），
\SpringMD{}解决的是"信任-可验证"问题（更可靠的模拟报告）。两个维度并不相互替代——
但它们也不应永远分离。我们希望未来NEP/DeepMD/MACE能够内建审计机制，
使"auditable by design"成为分子模拟软件的行业标准。}

\SpringMD{}的当前版本（v1.0）是SCX Spring理论体系的工程实现——
它将SCX定理1（多专家检测）、SCX定理2（自审计不可能）、SCX定理3（噪声-信号不可区分）、
Spring{}自演化训练循环和Yajie{}共识协议转化为四个可执行的命令。
它是第一个使"auditable MD"从理论概念变为工程现实的软件。

\begin{thebibliography}{99}

\bibitem{scx_ml_audit}
SCX, ``安全共识专家系统（SCX）：多专家审计的机器学习范式,''
*SCX理论体系 — 机器学习审计卷*, 2026.

\bibitem{scx_hamiltonian}
SCX理论物理工作组, ``神经网络哈密顿量与SCX多专家审计：一个统计力学对应,''
*SCX理论体系 — 统计力学卷*, 2026.

\bibitem{yajie_protocol}
SCX, ``Yajie共识协议：多独立审计模块的结盟、审查与审计数学基础,''
*SCX理论体系 — 审计协议卷*, 2026.

\bibitem{scx_spring_trainer}
SCX, ``Spring自演化势函数训练器：训练即审计的分子动力学势函数学习框架,''
*SCX理论体系 — 分子模拟卷*, 2026.

\bibitem{scx_spring_framework}
SCX, ``Spring统一多模态大模型框架：训练即审计的全模态智能架构,''
*SCX理论体系 — 大模型架构卷*, 2026.

\bibitem{nep}
Z. Fan *et al.*, ``Neuroevolution machine learning potentials:
Combining high accuracy and low cost in atomistic simulations,''
*Phys. Rev. B*, vol. 104, p. 104309, 2021.

\bibitem{deepmd}
L. Zhang, J. Han, H. Wang, R. Car, and W. E, ``Deep Potential Molecular Dynamics:
A Scalable Model with the Accuracy of Quantum Mechanics,''
*Phys. Rev. Lett.*, vol. 120, p. 143001, 2018.

\bibitem{ace}
R. Drautz, ``Atomic cluster expansion for accurate and transferable interatomic potentials,''
*Phys. Rev. B*, vol. 99, p. 014104, 2019.

\bibitem{mace}
I. Batatia, D. P. Kovács, G. N. C. Simm, C. Ortner, and G. Csányi,
``MACE: Higher Order Equivariant Message Passing Neural Networks for
Fast and Accurate Force Fields,''
*Advances in Neural Information Processing Systems*, 2022.

\bibitem{gap}
A. P. Bartók, M. C. Payne, R. Kondor, and G. Csányi,
``Gaussian Approximation Potentials: The Accuracy of Quantum Mechanics,
without the Electrons,''
*Phys. Rev. Lett.*, vol. 104, p. 136403, 2010.

\bibitem{lammps}
S. Plimpton, ``Fast Parallel Algorithms for Short-Range Molecular Dynamics,''
*J. Comp. Phys.*, vol. 117, pp. 1–19, 1995.

\bibitem{ase}
A. H. Larsen *et al.*, ``The Atomic Simulation Environment—a Python library
for working with atoms,''
*J. Phys.: Condens. Matter*, vol. 29, p. 273002, 2017.

\end{thebibliography}

## Appendix

## \Arbiter{审计报告JSON Schema（完整版）}

以下为\Arbiter{}审计报告的完整JSON Schema定义（JSON Schema Draft 2020-12）：

\begin{lstlisting}[caption={Arbiter审计报告JSON Schema},label=lst:schema, basicstyle=\ttfamily]
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Arbiter Audit Report",
  "type": "object",
  "required": ["report_meta", "potential", "simulation", "audit_frames", "summary"],
  "properties": {
    "report_meta": {
      "type": "object",
      "required": ["version", "timestamp", "report_type"],
      "properties": {
        "version": {"type": "string", "pattern": "^
d+
.
d+
.
d+$"},
        "timestamp": {"type": "string", "format": "date-time"},
        "report_type": {"type": "string", "enum": ["train", "run", "audit"]}
      }
    },
    "potential": {
      "type": "object",
      "required": ["path", "architecture", "M_t", "data_hash"],
      "properties": {
        "path": {"type": "string"},
        "architecture": {"type": "string"},
        "M_t": {"type": "integer", "minimum": 2},
        "data_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "Cercis_score": {"type": "number", "minimum": 0, "maximum": 1.2},
        "Yajie_mean_consensus": {"type": "number", "minimum": 0, "maximum": 1},
        "Lyapunov_final": {"type": "number", "minimum": 0}
      }
    },
    "simulation": {
      "type": "object",
      "required": ["ensemble", "temperature", "timestep", "total_steps"],
      "properties": {
        "ensemble": {"type": "string", "enum": ["nve", "nvt", "npt"]},
        "temperature": {"type": "number", "minimum": 0},
        "timestep": {"type": "number", "minimum": 0},
        "total_steps": {"type": "integer", "minimum": 1},
        "engine": {"type": "string", "enum": ["lammps", "ase"]},
        "trajectory_hash": {"type": "string"}
      }
    },
    "audit_frames": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step", "time", "Yajie_consensus", "Cercis_frame"],
        "properties": {
          "step": {"type": "integer", "minimum": 0},
          "time": {"type": "number"},
          "Yajie_consensus": {"type": "number", "minimum": 0, "maximum": 1},
          "energy_std": {"type": "number", "minimum": 0},
          "force_std": {"type": "number", "minimum": 0},
          "is_OOD": {"type": "boolean"},
          "OOD_score": {"type": "number", "minimum": 0},
          "Cercis_frame": {"type": "number", "minimum": 0, "maximum": 1},
          "flags": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "summary": {
      "type": "object",
      "required": ["total_frames", "mean_consensus"],
      "properties": {
        "total_frames": {"type": "integer"},
        "mean_consensus": {"type": "number", "minimum": 0, "maximum": 1},
        "OOD_fraction": {"type": "number", "minimum": 0, "maximum": 1},
        "Cercis_mean": {"type": "number", "minimum": 0, "maximum": 1},
        "flags_summary": {"type": "object"}
      }
    }
  }
}
\end{lstlisting}

## 命令行完整参考

### `spring-md`

\begin{lstlisting}[basicstyle=\ttfamily, frame=single]
spring-md <COMMAND> [OPTIONS]

COMMANDS:
  train     训练势函数 (Training)
  run       运行分子动力学模拟 (MD Simulation)
  audit     审计已有轨迹 (Trajectory Auditing)
  compare   对比多个势函数 (Potential Comparison)
  help      显示帮助信息

GLOBAL OPTIONS:
  --version  显示版本号
  --help     显示帮助信息
\end{lstlisting}

### 退出码

[Table omitted — see original .tex]

## 安装指南

\SpringMD{}的安装依赖：

\begin{lstlisting}[caption={安装命令},label=lst:install]
# 通过pip安装
pip install spring-md

# 系统依赖
# - Python >= 3.9
# - PyTorch >= 2.0 (with CUDA support for GPU)
# - LAMMPS (可选, 用于lammps引擎)
# - ASE >= 3.22 (可选, 用于ase引擎)

# 验证安装
spring-md --version
# Spring MD v1.0.0 (SCX Audit Middleware)
# PyTorch backend: CUDA 12.1
# Engines: lammps (found), ase (v3.23.0)
\end{lstlisting}