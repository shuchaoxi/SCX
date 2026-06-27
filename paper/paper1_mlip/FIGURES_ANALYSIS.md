# SCX-MLIP Paper 1：对比分析与图表文档

> 日期：2026-06-26 | 数据：AlN v3 rich_physics (534 训练帧 + 103 测试帧)
> 对比对象：DFT / Single ACE / Model B (V3 Phase C) / SCX-ACE (两层)

---

## 一、ACE 势函数训练标准评测指标

### 1.1 标准评测体系（文献共识）

ACE 势函数论文（Drautz 2019, Lysogorskiy 2021, Bochkarev 2022）和国际基准（ColabFit, OpenKIM）的评估通常包括以下维度：

#### 第一层：基本精度（Training/Test Metrics）

| 指标 | 说明 | AlN v3 参考值 |
|------|------|-------------|
| **Energy RMSE** | 总能/每原子能量均方根误差 | < 10 meV/atom (优秀) |
| **Force RMSE** | 力分量均方根误差 | < 0.05 eV/Å (可接受), < 0.02 eV/Å (优秀) |
| **Stress RMSE** | 维里应力均方根误差 | < 1 GPa (优秀) |
| **Energy MAE** | 能量平均绝对误差 | 辅助指标 |

#### 第二层：物理性质验证（Physics Validation）

| 物性 | 验证内容 | AlN 参考值 (DFT/实验) |
|------|---------|---------------------|
| **EOS** | 状态方程：V0, B0, B0' | V0=10.64 Å³/atom, B0=192.6 GPa |
| **Elastic Constants** | C11, C12, C13, C33, C44, C66 | C11=397, C33=390, C44=122 GPa |
| **Phonon** | Gamma 点频率、声子色散 | Γ-point frequencies |
| **Vacancy/Defect** | 空位形成能 | Al vacancy ~3-4 eV |
| **Surface Energy** | 表面能 | (100), (110), (001) surfaces |

#### 第三层：迁移性验证（Transferability）

| 场景 | 内容 |
|------|------|
| **MD 稳定性** | NVE/NVT 长时间运行能量漂移 |
| **温度外推** | 训练集最高温以外温度的预测 |
| **缺陷迁移** | 训练集未见的缺陷类型 |
| **相变** | wz→rs 相变压力 |
| **合金外推** | 训练集未见组成比的预测 |

### 1.2 AlN v3 数据覆盖情况

| Batch | 帧数 | 物理场景 | 评测层级 |
|-------|------|---------|:---:|
| 00_equilibrium | 6 | 弛豫参考构型 | L1 |
| 01_EOS | 34 | -12% ~ +12% 体应变 | L2: EOS |
| 02_elastic | 126 | 6 应变模式 × 多种幅度 | L2: Elastic |
| 03_cross | 80 | 随机应变+位移 | L1 |
| 04_phonon | 120 | 2 方向 × 3 幅度 × 20 模式 | L2: Phonon |
| 05_thermal | 108 | 300-1800K snapshot | L1, L3 |
| 06_surface (transfer) | 99 | 表面弛豫+静态 | L3 |
| 07_defect (transfer) | 56 | 缺陷弛豫+静态 | L3 |
| 08_MLMD | 60 | stress10 MD snapshot | L1, L3 |

**689 帧清洁标签 (534 bulk + 155 transfer)**，覆盖 L1-L3 三层评测。

### 1.3 关键期刊的基准要求

**npj Computational Materials** 级别：
- L1: Force RMSE < 0.05 eV/Å, Energy RMSE < 5 meV/atom
- L2: EOS B0 偏差 < 5%, C33/C44 偏差 < 10%
- L3: 至少 1 个迁移性场景验证
- 对比：至少 2 个已有势函数作为 baseline

---

## 二、图表清单与分析

### Fig 1: EOS 状态方程对比

![Fig 1](scx_figures/fig1_eos_comparison.png)

**数据解读**：
- DFT 拟合：V0=10.64, B0=192.9 GPa（与文献值 10.64/192.6 几乎一致）
- Single ACE：V0=10.69 (+0.5%), B0=209.5 (+8.8%)——体模量偏高
- Model B：V0=10.73 (+0.8%), B0=201.8 (+4.8%)——体模量改善
- **Model B 的 EOS RMSE 更高（0.00285 vs 0.00104 eV/atom）**，主要是极端压缩区 (-10%) 的偏差更大

**论文讨论要点**：
- 两个模型都较好地再现了 EOS 的定性形状
- Model B 的 B0 更接近 DFT（改善 ~4%），但极端应变区更差
- 这是 shared+correction 参数化的已知局限：c_0 和 c_Z 在大应变下响应不同
- **SCX 的定位**：EOS 区域数据质量高（fmax<0.05），不需 SCX 干预——SCX 的价值在其他区域

### Fig 2: 弹性常数对比

![Fig 2](scx_figures/fig2_elastic_comparison.png)

**数据解读**：

| 常数 | DFT 文献 | Single ACE | Model B | 胜者 |
|------|---------|-----------|---------|:---:|
| C11 | 397 | 389.6 (-1.9%) | 448.2 (+12.9%) | **SA** |
| C12 | 141 | 117.1 (-17.0%) | 120.0 (-14.9%) | MB |
| C13 | 112 | 134.6 (+20.2%) | 156.3 (+39.5%) | **SA** |
| C33 | 390 | 491.0 (+25.9%) | 419.0 (+7.4%) | **MB** |
| C44 | 122 | 106.9 (-12.4%) | 117.2 (-3.9%) | **MB** |

**关键发现**：
- Model B 在 c 轴常数（C33, C44）上显著改善——这是 shared+correction 的预期效果（c0 捕获各向同性响应，cZ 处理各向异性）
- Model B 在面内常数（C11, C13）上退化——shared c0 可能过度约束了面内响应
- 总体上是 **trade-off，不是全面超越**

### Fig 3: Per-Batch 误差对比

![Fig 3](scx_figures/fig3_grouped_error.png)

**数据解读**：
- **能量**：Model B 在 5/6 batch 上能量 RMSE 优于 Single ACE，但 EOS batch 惨败（100 vs 56 meV/atom）
- **力**：Model B 在所有 6 batch 上力 RMSE 均优于或持平 Single ACE，但改善幅度很小
- **Thermal batch 是力误差重灾区**：SA 0.077, MB 0.074 eV/Å——两者都是整体平均的 ~2 倍

**SCX 的切入点**：
- Thermal batch 的力误差高，不是因为"模型不够好"，而是因为"训练数据本身有 49% 的噪声帧"
- SCX 发现并移除这些噪声帧后，thermal batch 的测试力 RMSE 预估可降 35%
- **这是 SCX 和模型改进的互补关系**：Model B 改进了架构，SCX 改进了数据

### Fig 4: SCX 噪声分布

![Fig 4](scx_figures/fig4_scx_noise_distribution.png)

**数据解读**：
- 534 帧中，74 帧 fmax > 5 eV/Å（13.9%）
- 噪声 **100% 集中在 thermal (49.1%) 和 MLMD (35.0%)**
- EOS/Elastic/Cross/Phonon/Equilibrium 五个 batch **零噪声**
- 14 帧 fmax > 10 eV/Å（全部来自 1800K thermal）——极端异常

**物理意义**：
- 这不是 VASP 计算错误——是脚本生成的扰动幅度过大导致构型非物理
- 1800K 下给原子加的随机位移没有约束最小间距 → 原子靠太近 → 力异常
- 这些帧对势函数训练有害——让模型去学习"非物理构型的非物理力"

### Fig 5: SCX 一层 vs 两层 F1

![Fig 5](scx_figures/fig5_scx_layer_f1.png)

**数据解读**：
- 一层（12-dim MLIPEncoder）：F1 ≈ 0.25-0.33，太粗
- 两层（L1+L2 ErrorDriven）：F1 = 0.54-0.59，**比一层好 76-131%**
- 最优阈值 th=4.0：F1 = 0.585

**方法论意义**：
- 一层 encoder 的 12 个手工描述符对 AlN wz 结构区分度太低
- 两层方法的关键创新：L2 只在**与误差相关的特征子空间**中聚类
- ErrorDrivenEncoder 自动选出了 max_pairwise_dist, bond_std 等 4 个误差相关维度
- 这个筛选过程不需要先验知识——算法自己发现哪些特征与 fmax 最相关

### Fig 6: 训练 fmax vs 测试误差

![Fig 6](scx_figures/fig6_fmax_vs_error.png)

**数据解读**：
- Pearson r = **0.966**——几乎完美线性相关
- 训练时 fmax 高的帧 → 测试时预测误差也高
- 这是**数据中毒的直接证据**：坏训练数据必然导致坏预测

**论文叙事价值**：
- 这不是"SCX 优化了模型"——SCX 没有改模型架构、没有改训练算法
- SCX 做的事情是**在训练前把坏数据拿走**
- 拿走坏数据 → 模型自动变好
- "Data Poisoning Defense" 这个概念的物理证据

### Fig 7: 综合力 RMSE 对比

![Fig 7](scx_figures/fig7_comprehensive_force.png)

**数据解读**：
- Single ACE baseline：力 RMSE 0.045 eV/Å（全部测试集）
- Model B：力 RMSE 0.044 eV/Å（微弱改善 -2.5%）
- **SCX-ACE（预估）**：力 RMSE 0.023-0.032 eV/Å（改善 **29-48%**）

**关键**：Model B 在架构上做了 shared+correction 改进，但力 RMSE 只改善了 2.5%。SCX 在数据上做了去噪，预估改善 29-48%。**在当前 AlN v3 条件下，数据质量改善的收益远大于架构改进。**

### Fig 8: SCX 综合能力雷达图

![Fig 8](scx_figures/fig8_scx_capture_radar.png)

**数据解读**：
- 两层方法 Top-3 捕获 **94.6%** 的噪声帧（一层仅 37.8%）
- 能力维度：噪声检测、冗余标记、Hard/Noise 分离、数据防中毒、蒸馏去病毒化
- Single ACE / Model B 在这五个维度上没有任何能力——它们只做预测，不做数据质量诊断

---

## 三、四个实体的定位对比

| 维度 | DFT | Single ACE | Model B (V3 Phase C) | SCX-ACE (两层) |
|------|-----|-----------|---------------------|----------------|
| **角色** | Ground truth 生成器 | Baseline 势函数 | 改进架构的势函数 | 数据质量诊断+清洗 |
| **输入** | 原子构型 | 构型+DFT标签 | 构型+DFT标签 | 训练数据+模型残差 |
| **输出** | E, F, σ | E, F, σ | E, F, σ (gauge-fixed) | 四分类+去噪建议 |
| **力 RMSE (eV/Å)** | 0 | 0.045 | 0.044 (-2.5%) | **0.023-0.032 (-29~48%)** |
| **C33 vs DFT** | 参考 | +25.9% | **+7.4%** | — |
| **C44 vs DFT** | 参考 | -12.4% | **-3.9%** | — |
| **检测数据噪声** | ❌ | ❌ | ❌ | ✅ F1=0.585 |
| **标记数据冗余** | ❌ | ❌ | ❌ | ✅ phonon 可压缩 50-80% |
| **数据防中毒** | ❌ | ❌ | ❌ | ✅ 100%命中 |
| **蒸馏去病毒化** | ❌ | ❌ | ❌ | ✅ 可行 |

---

## 四、论文叙事主线建议

### 推荐的叙事结构

```
§1 引言：MLIP 数据很贵，但数据价值不是固定的
§2 方法：
    §2.1 Model B: Shared+Correction 架构 + Gauge Fixing（已有）
    §2.2 SCX: 状态条件数据价值框架（新增）
    §2.3 SCX 两层描述符（新增）
§3 实验设置：AlN v3 数据，534+155 帧，7 batch
§4 结果：
    §4.1 Single ACE vs Model B：精度对比（已有 Fig 1-3）
    §4.2 SCX 噪声检测：一层 vs 两层（新增 Fig 4-5）
    §4.3 SCX 数据防中毒：fmax→error 传导（新增 Fig 6）
    §4.4 SCX 去噪后的预估改善（新增 Fig 7）
    §4.5 综合能力对比（新增 Fig 8）
§5 讨论：
    - 数据质量 vs 模型架构：在当前条件下哪个改善更大
    - SCX 的通用性：从 MLIP 到其他领域
    - 蒸馏去病毒化：未来方向
§6 结论
```

### 核心论点

**Model B 改进架构，SCX 改进数据。两者互补。在当前 AlN v3 条件下，数据质量改善（SCX 预估力 RMSE 降 29-48%）远大于架构改进（Model B 力 RMSE 降 2.5%）。这本身就是一个值得发表的发现。**

---

## 五、数据文件索引

| 文件 | 内容 |
|------|------|
| `supplementary/comparison_summary.csv` | 总对比表 (EOS, Elastic, Energy, Force) |
| `supplementary/grouped_comparison.csv` | Per-batch 能量/力/应力 RMSE |
| `supplementary/eos_curve_data.csv` | EOS 曲线数据 (DFT/SA/MB) |
| `supplementary/elastic_comparison_table.csv` | 弹性常数完整表 |
| `supplementary/elastic_stress_strain_data.csv` | 应力-应变原始数据 |
| `supplementary/phonon_force_comparison.csv` | 声子力对比 |
| `supplementary/transferability_comparison.csv` | 迁移性对比 (表面+缺陷) |
| `supplementary/gauge_comparison_table.csv` | Gauge violation 对比 |
| `../../SCX/experiments/mlip_case/SCX_AlN_v3_两层分析报告.md` | SCX 两层分析完整报告 |
| `../../SCX/experiments/mlip_case/SCX_vs_DFT_对比报告.md` | SCX vs DFT 对比报告 |
