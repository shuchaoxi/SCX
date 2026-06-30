# NEP 路线是否适合这个课题

## 结论

适合。尤其适合作为第一阶段 proof-of-concept。

建议路线：

```text
NEP4 / GPUMD
```

但需要注意：这里的 NEP 不是用来证明“完全不需要 DFT”，而是用来快速跑通：

```text
多 teacher soft-label 蒸馏 -> 多元素 student -> 少量 DFT 校准 -> MD/物性验证
```

## 为什么 NEP 适合

### 1. 工程链条短

GPUMD 不仅可以用 `gpumd` 做 MD，也可以用 `nep` 可执行程序训练 NEP 模型。

这对探索性课题很重要，因为你不需要在多个框架之间来回转换。

### 2. 多组分体系有 NEP4

GPUMD 官方文档说明：

- 当前支持 NEP3 和 NEP4。
- NEP1 和 NEP2 已弃用。
- 对单组分体系，NEP3 和 NEP4 等价。
- 对多组分体系，在其他超参数相同的情况下，NEP4 通常更准确。

这正好适合你的多元素 student 目标。

### 3. 速度优势明显

NEP 适合后续做：

- 大规模 MD。
- 热输运。
- 缺陷扩散。
- 界面。
- 合金采样。

你的研究如果后面想接 `Si/金刚石/半导体热管理`，NEP/GPUMD 生态非常合适。

### 4. 你能和开发者交流

这是很大的优势。

新方法探索中最容易卡在：

- 训练文件格式。
- 多组分超参数。
- loss 权重。
- fine-tune。
- virial/stress 标签。
- type_weight。
- 数据异常排查。

能和开发者交流会显著降低试错成本。

## NEP 路线的局限

### 1. NEP 本身不是“蒸馏框架”

NEP 训练吃的是结构数据和标签：

```text
structure + energy + forces + virial/stress
```

所以你的“蒸馏”主要体现在数据构造，而不是 NEP 程序本身内置 teacher-student loss。

第一阶段可以把 teacher 生成的 `E/F/virial` 当作训练标签。

### 2. 不容易直接蒸馏 teacher 的隐藏表示

如果 teacher 是 ACE、MACE、NequIP 等，想蒸馏 descriptor/latent feature 比较麻烦。

NEP 第一阶段建议先蒸馏：

```text
E, F, virial
```

以后再考虑更复杂的 relational/descriptor distillation。

### 3. 能量零点必须处理

多个 teacher 的能量基准可能不同。

建议第一阶段：

- 更重视 force 蒸馏。
- 对每个二元体系单独拟合元素参考能。
- 使用 DFT 小集合统一能量基准。
- 训练时可降低 `lambda_e`，提高 `lambda_f`，等基准统一后再提高能量权重。

### 4. 交叉区域不能只靠 teacher

例如：

```text
AlAs + GaAs + InAs
```

teacher 没有直接见过三元局部环境。

所以 student 在 `Al_xGa_yIn_1-x-yAs` 中间区域可能不可靠。

必须补少量 DFT：

- SQS 随机合金。
- 局部应变结构。
- 高温 MD snapshot。
- vacancy/antisite。

## 推荐实施路线

### Step 1：先做二元 teacher 数据池

对每个二元体系生成结构：

- 平衡晶体。
- 体积应变：`-8%` 到 `+8%`。
- 剪切/拉伸畸变。
- 300 K、600 K、900 K、1200 K MD snapshot。
- vacancy。
- 少量表面或界面先不做，避免第一阶段太复杂。

标签来源：

```text
teacher potential -> E/F/virial
```

### Step 2：统一数据格式

转成 NEP 所需的 `train.xyz` / `test.xyz`。

建议记录 metadata：

```text
system = AlAs / GaAs / InAs
source = teacher / DFT
temperature = ...
strain = ...
label_type = soft / hard
```

### Step 3：训练 NEP4 student

第一版目标：

```text
type 4 Al Ga In As
version 4
```

训练集：

```text
AlAs soft labels
GaAs soft labels
InAs soft labels
少量 Al-Ga-In-As DFT hard labels
```

### Step 4：做三种对照

必须有对照，否则论文味道不够。

```text
A. 只用 teacher soft labels
B. teacher soft labels + 少量 DFT hard labels
C. 只用同等数量 DFT hard labels
```

比较：

- RMSE。
- 晶格常数。
- 弹性常数。
- 混合焓。
- 声子谱。
- NPT MD 稳定性。
- 缺陷形成能。

### Step 5：画失效地图

最终最有价值的图不是 RMSE，而是：

```text
composition space: Al-Ga-In-As

颜色 = student 与 DFT 偏差
标记 = teacher disagreement / extrapolation / DFT补点
```

这张图能说明：

- 二元 teacher 何处有效。
- 三元/四元空间何处失败。
- DFT 补点如何修复。

## 推荐题目版本

英文：

**Binary-to-multicomponent distillation of semiconductor interatomic potentials using NEP4: feasibility and failure boundaries in Al-Ga-In-As alloys**

中文：

**基于 NEP4 的半导体势函数并集蒸馏：Al-Ga-In-As 合金中的可行性与失效边界**

## 官方资料

- GPUMD NEP 文档：https://gpumd.org/dev/potentials/nep.html
- GPUMD `nep` 可执行程序文档：https://www.gpumd.org/dev/nep/index.html
- GPUMD potential 输入文档：https://www.gpumd.org/gpumd/input_parameters/potential.html

