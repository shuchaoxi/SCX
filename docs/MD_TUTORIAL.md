# Spring MD：给你的势函数加一个质检报告

> **受众**：计算材料科学研究者 — 训练过 NEP/DeepMD/MACE 势函数，使用 GPUMD/LAMMPS 做分子动力学模拟。
> **前置知识**：DFT 计算、势函数训练、MD 基础。不需要了解 SCX 理论或规范场论。
> **代码位置**：`github.com/shuchaoxi/SCX` — 源码在 `src/scx/`，测试在 `tests/`，673 项测试全部通过。
> **原则**：开源，

---

## 当前困境

计算材料领域面临三个结构性问题，非个人能力所能解决：

**第一，势函数质量无法横向对比。** 每个课题组训练 NEP 或 DeepMD 后，报告各自的 RMSE。测试集不同、split 方式不同、checkpoint 选择策略不同。甲的 45 meV/Å 和乙的 50 meV/Å 无法直接比较——测试集不是同一批数据。更无法排除 cherry-picking 的可能性。

**第二，训练数据的质量无法自证。** DFT 计算中混入的未收敛构型、标注错误的力、不同赝势/泛函混用导致的不一致——这些噪声在单模型训练中几乎不可见。训练者本人可能也不清楚训练集里有多少脏数据。

**第三，势函数发布时缺乏可信的质检凭证。** 当前业界没有统一的势函数质量认证标准。审稿人和使用者只能依赖作者的自述。

Spring MD 提供了这三个问题的工程解决方案。

---

## 1. 一句话讲清楚

**Spring 不是一个新的势函数框架。**

NEP 是势函数。DeepMD 是势函数。MACE 是势函数。GPUMD 是跑 MD 的引擎。LAMMPS 是跑 MD 的引擎。

Spring 不是这些。**Spring 是一个审计层。** 它架在你的训练流程之上，不替代任何东西。

训练完势函数之后，跑一遍 Spring。它会：

1. 把你的训练数据放进多个独立专家模型做交叉验证
2. 自动标出训练集里的脏数据（Yajie 共识评分）
3. 生成一个不可伪造的审计参数 **M_t**（数据哈希绑定的）
4. 产出一个可横向对比的质量分数 **Cercis Score**

从此你的势函数不只是"我训了一个 NEP 模型"——它带着一份独立的质检报告。

```
你的 NEP/DeepMD/MACE 训练流程
         │
         ▼
    ┌─────────┐
    │ Spring  │  ← 审计层，不改你的势函数
    │  Audit  │
    └────┬────┘
         │
         ▼
    nep.scxp + 审计报告（M_t + Cercis + 数据质量标签）
```

---

## 2. 为什么你需要这个

### 2.1 你现在怎么证明你的势函数比别人的好？

RMSE。对不对？训完 NEP，算一个 force RMSE —— "我们的模型在测试集上 forces RMSE = 45 meV/Å"。

问题在哪？

**每个组都挑自己最好的 RMSE 报。** 不同的测试集、不同的 split、不同的训练条件。你没法直接比一个组的 45 meV/Å 和另一个组的 50 meV/Å —— 测试集不一样，什么都说明不了。

更糟的是：你没法证明你的 RMSE 是真的。你也可能 cherry-pick 了最好的那个 checkpoint。你也可能"不小心"选了噪声最少的那段测试集。这不一定是故意的——但没有外部约束，你凭什么让别人相信？

### 2.2 Spring 解决了什么

Spring 提供两样你现在没有的东西：

**第一，统一标准。** Cercis 分数不关心你用什么架构（NEP / DeepMD / MACE / ACE / GAP），不关心你的测试集怎么分的。它是一套跨架构可比的评分机制。NEP 的 0.78 和 DeepMD 的 0.82 可以直接排——因为它看的是数据质量和多专家一致性，不是你自己报的 RMSE。

**第二，不可伪造。** M_t 参数不是你自己填的——它是从你的训练数据的 SHA-256 哈希中算出来的。改一条数据，M_t 就变。想声称"我用了最好的那组数据"而不提其他失败的 run？M_t 和你的数据绑定，挂羊头卖狗肉在数学上不可行。

### 2.3 从 M=1 到 M>1

在 Spring 的框架里，你现在做的事情叫 **M=1**：

> 一个模型自己评价自己。

这有没有问题？有，而且不是你操作的问题——是数学上的问题。

定理 3（老实人定理）证明了：**从单模型的预测结果中，你无法区分标签噪声和样本本身的固有困难。** 一条数据你的模型算出来和 DFT 差很多——是 DFT 标错了（这条数据是噪声）还是这条构型本身就很难算（你的模型能力不够）？只看一个模型的结果，你永远分不清。

唯一的出路：引入多个独立视角（M > 1）。Spring 强制引入多个独立专家，让"好"变成一个可验证的结果，而不是一个声称。

---

## 3. 核心概念：三个你只需要知道的名词

全篇只涉及三个新名词。每个一句话。

### 3.1 M_t 参数

**M_t 是你势函数的审计指纹。** 它不是你自己报的数字——是从你的训练数据的 SHA-256 哈希算出来的。改数据 → 哈希变 → M_t 变。你的势函数和你的训练数据被数学绑定在一起，不可拆分、不可伪造。

你可以把 M_t 理解成"这份势函数的出生证明"。它证明：这份势函数被审计过，且审计用的就是这批数据。

### 3.2 Cercis 分数

**Cercis 是一个 0 到 1 之间的数字，衡量你的势函数在训练数据上的综合表现。** 越高越好。它由两部分组成：

- **Q（质量）**：你的势函数在训练数据上的精度。多专家共识越高，Q 越大。
- **N（覆盖）**：你的训练数据覆盖了多少物理空间。你的训练集里各种构型越全，N 越大。

Cercis = Q + η·N。早期训练 η 大，鼓励覆盖更多构型；后期 η 小，更看重精度。最终分数是一个统一的标量，不同架构的势函数可以直接比。

### 3.3 Yajie（雅洁）

**Yajie 是 Spring 内部的噪声检测模块。** 你把训练数据和 M 个独立专家喂给它，它会：

- 把每条训练数据标为 **CLEAN**（干净）、**NOISY**（噪声）或 **AMBIGUOUS**（存疑）
- 告诉你训练集里有多少脏数据
- 自动过滤掉噪声数据，让后续训练更干净

你不需要预先知道哪些数据是坏的。Yajie 自己发现。

---

## 4. 怎么用（以 NEP 为例）

假设你是一个典型的 NEP 用户：用 GPUMD 的 `nep` 模块训练了一个 III-nitride（比如 GaN）的势函数。你有一个 `train.xyz`，里面有 DFT 算的能量、力、应力。你跑了 `nep` 训练，得到了 `nep.txt`。

你的工作流现在是这样的：

```
train.xyz → nep 训练 → nep.txt → GPUMD 跑 MD
```

加上 Spring 之后：

```
train.xyz → nep 训练 → nep.txt
                            │
                            ▼
                      spring-md audit ──→ nep.scxp + audit_report.json
                            │
                            ▼
                      GPUMD 跑 MD（用 nep.scxp 或转回 nep.txt）
```

### 4.1 你已经有一个训练好的 NEP 势函数

你的 `nep.txt` 大概长这样：

```
nep 3 1
Ga N
...
```

这是 GPUMD 的 NEP 势函数文件。训练数据在 `training_data/` 目录下，里面是 XYZ 格式的 DFT 计算结果。

### 4.2 跑 Spring 审计

一行命令：

```bash
spring-md audit \
  --format nep \
  --input nep.txt \
  --data training_data/ \
  --experts 5 \
  --output nep_audited
```

参数说明：


| 参数                    | 含义                                                  |
| ----------------------- | ----------------------------------------------------- |
| `--format nep`          | 你的势函数格式。支持`nep`、`deepmd`、`mace`、`lammps` |
| `--input nep.txt`       | 你的势函数文件                                        |
| `--data training_data/` | 训练数据目录。XYZ 格式直接读                          |
| `--experts 5`           | 用几个独立专家做交叉验证。推荐 ≥ 3，5 效果显著       |
| `--output nep_audited`  | 输出文件前缀                                          |

### 4.3 输出什么

运行完成后，你得到：

```
nep_audited.scxp          # 带审计元数据的势函数包
nep_audited_report.json   # 详细审计报告
nep_audited_quality.csv   # 每条训练数据的质量标签
```

**`nep_audited.scxp`** 是一个容器文件。它里面包含：

- 原始的 NEP 参数（`nep.txt` 的所有内容）
- M_t 审计参数
- 数据哈希
- 审计时间戳
- 版本信息

你打开 `.scxp` 文件就能看到——它是结构化文本，不是二进制。NEP 参数部分和原来的 `nep.txt` 一模一样，只是头尾加了审计元数据。

**`nep_audited_report.json`** 是审计报告，包含：

```json
{
  "model_format": "nep",
  "audit_timestamp": "2026-07-01T10:23:45Z",
  "M_t": 1048673,
  "M_experts": 5,
  "experts_passed": 4,
  "cercis_score": 0.783,
  "data_hash": "a1b2c3d4e5f6...",
  "verification": "VERIFIED",
  "data_quality": {
    "total_samples": 12500,
    "clean": 11240,
    "noisy": 860,
    "ambiguous": 400
  },
  "state_summary": [
    {"state_id": 0, "label": "bulk_equilibrium", "cercis": 0.94, "verdict": "clean"},
    {"state_id": 1, "label": "defect_N_vacancy", "cercis": 0.71, "verdict": "ambiguous"},
    {"state_id": 2, "label": "thermal_1200K", "cercis": 0.62, "verdict": "ambiguous"}
  ]
}
```

**`nep_audited_quality.csv`** 给每一条训练数据贴上标签：


| sample_id | state_id | verdict   | consensus_score | cercis_component |
| --------- | -------- | --------- | --------------- | ---------------- |
| 0         | 2        | clean     | 0.94            | 0.91             |
| 1         | 5        | clean     | 0.88            | 0.85             |
| 2         | 0        | noisy     | 0.12            | 0.22             |
| 3         | 3        | ambiguous | 0.55            | 0.61             |
| ...       | ...      | ...       | ...             | ...              |

### 4.4 现在你的势函数带着质检报告

把 `.scxp` 文件和 `_report.json` 一起发布。别人拿到你的势函数，可以直接验证：

```bash
# 验证审计完整性
spring-md verify --input nep_audited.scxp

# 输出：
# ✅ Verification: PASS
#    M_t matches data hash
#    Cercis Score: 0.783
#    Audit date: 2026-07-01
```

---

## 5. 怎么和 GPUMD 对接

核心原则：**Spring 不改你的计算。审计报告是独立的 JSON 文件，不影响 GPUMD 运行。**

### 5.1 方案 A：GPUMD 直接读 .scxp（推荐）

如果你用的是支持 `.scxp` 的 GPUMD 版本（或你加了 SCX 插件），直接把 `.scxp` 当成势函数文件喂给 GPUMD：

```bash
gpumd -p nep_audited.scxp
```

`.scxp` 文件里的 NEP 参数部分和原来的 `nep.txt` 完全一样。GPUMD 读它就和读 `nep.txt` 一样跑。SCX 元数据在文件头尾，GPUMD 忽略它们。

### 5.2 方案 B：从 .scxp 转回 nep.txt

如果 GPUMD 不支持 `.scxp`，一行命令转回去：

```bash
spring-md convert \
  --input nep_audited.scxp \
  --to nep \
  --output nep_recovered.txt
```

`nep_recovered.txt` 就是干净的 NEP 参数文件——和原来的 `nep.txt` 数学上等价（NEP 参数完全一致）。审计元数据被剥离。GPUMD 照常运行：

```bash
gpumd -p nep_recovered.txt
```

### 5.3 审计报告独立存在

不管用方案 A 还是方案 B，`nep_audited_report.json` 是独立文件。它不参与 MD 计算。它只是你的势函数的质检报告——就像你买一块 CPU 附带的技术规格书。

**对计算性能零影响。** GPUMD 跑的物理和你不加 Spring 时一模一样。

---

## 6. 和 LAMMPS / DeepMD / MACE 对接

### 6.1 DeepMD (DeePMD-kit)

你已经训好了 DeepMD 模型（`frozen_model.pb` 或 `model.pt`）。训练数据在 `deepmd_data/` 目录下（`set.000`、`type.raw` 等）。

```bash
spring-md audit \
  --format deepmd \
  --input frozen_model.pb \
  --data deepmd_data/ \
  --experts 5 \
  --output deepmd_audited
```

输出：

- `deepmd_audited.scxp`
- `deepmd_audited_report.json`

转回 DeepMD 格式：

```bash
spring-md convert --input deepmd_audited.scxp --to deepmd --output model_recovered.pb
```

然后在 LAMMPS 里照常用：

```
pair_style deepmd model_recovered.pb
```

### 6.2 MACE

```bash
spring-md audit \
  --format mace \
  --input MACE_model.model \
  --data mace_training.xyz \
  --experts 5 \
  --output mace_audited
```

### 6.3 通用 XYZ 格式

如果你有一个自己训练的势函数（不限于上述框架），只要有 XYZ 格式的训练数据，就可以跑审计：

```bash
spring-md audit \
  --format generic \
  --model your_model.py \      # 你的模型推理脚本
  --data training_set.xyz \
  --experts 5 \
  --output audited
```

`your_model.py` 只需要实现一个接口：

```python
def predict(positions, species, cell):
    """返回 (energy, forces, stress)"""
    ...
```

---

## 7. 训练数据用什么

### 7.1 不挑格式

Spring 不关心你的训练数据来源。你现在用什么，直接喂进去就行：

- NEP 的 `train.xyz`（GPUMD 格式，含 energy/forces/virial）
- DeepMD 的 `set.000/` 目录
- 扩展 XYZ（extxyz）
- VASP 的 OUTCAR / vasprun.xml（通过内置解析器）
- 纯 numpy 数组（如果你自己写加载器）

### 7.2 推荐的数据构成

Spring 在多专家交叉验证时，数据的多样性直接影响审计质量。推荐：

- **DFT 静态计算**：弹性常数、空位形成能、表面能 —— 覆盖物理性质
- **AIMD 轨迹**：不同温度（300K, 600K, 1200K）的 NVT/NPT 轨迹 —— 覆盖相空间
- **缺陷结构**：空位、间隙、反位、位错 —— 覆盖非平衡构型
- **扰动结构**：rattled 结构、phonon 位移 —— 覆盖力空间

混合得越丰富，Yajie 的状态发现越准确，Cercis 分数越有区分度。

### 7.3 数据量建议


| 场景                | 最少数据量 | 推荐数据量 |
| ------------------- | ---------- | ---------- |
| 单一元素（Si）      | 500 条     | 2000+ 条   |
| 二元化合物（GaN）   | 1000 条    | 5000+ 条   |
| 三元及以上（AlGaN） | 3000 条    | 10000+ 条  |

数据太少 → 状态发现不稳定 → 审计结果参考价值下降。但 Spring 会诚实地告诉你"数据量不足，审计置信度低"——不会强行给一个虚假的高分。

### 7.4 Spring 自动降噪

你不需要手动清洗训练集。Yajie 会自动发现并标注噪声数据：

```
训练集 12,500 条
    │
    ▼
Yajie 共识评分
    │
    ├── CLEAN:     11,240 条 (89.9%)
    ├── NOISY:        860 条 ( 6.9%)  ← 自动标记，可以剔除
    └── AMBIGUOUS:    400 条 ( 3.2%)  ← 需要人工核查
```

NOISY 数据通常是：

- DFT 计算未收敛的构型
- 力标注错误的帧
- 两个不同赝势/泛函混用导致的不一致数据

你可以选择自动剔除 NOISY 数据后重新训练——你的势函数在新训练集上的 RMSE 通常会下降。但注意：Yajie 标为 NOISY 的数据不一定是"错的"——它只是"M 个专家一致认为这条数据和主流模式不一致"。建议人工抽查 NOISY 数据确认。

---

## 8. 审计报告长什么样

完整的审计报告包含以下部分。你不必全部看懂——日常使用只需要关注 Cercis 分数和 M_t。

### 8.1 报告头

```json
{
  "audit_id": "audit-20260701-gaN-nep-v2",
  "audit_timestamp": "2026-07-01T10:23:45.123456Z",
  "spring_version": "2.1.0",
  "model_format": "nep",
  "model_architecture": "NEP (Neuroevolution Potential)",
  "model_hash": "sha256:e7f3a9b1..."
}
```

### 8.2 M_t 参数

```json
{
  "M_t": 1048673,
  "M_experts": 5,
  "experts_passed": 4,
  "symbiotic_binding": {
    "data_hash": "sha256:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6...",
    "code_hash": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7...",
    "binding_verified": true
  }
}
```

- **M_t**：从数据哈希派生的审计指纹（不是你自己填的）
- **M_experts**：实际参与审计的专家数量
- **experts_passed**：通过一致性检查的专家数（4/5 意味着 4 个专家结果一致，1 个偏离）
- **symbiotic_binding**：数据-模型-代码的绑定验证。`binding_verified: true` 表示没有篡改

### 8.3 Cercis 分数

```json
{
  "cercis_score": 0.783,
  "cercis_components": {
    "quality_Q": 0.712,
    "coverage_N": 0.601,
    "eta_at_audit_time": 0.118,
    "schedule": "exponential"
  },
  "cercis_percentile": "top 23% among audited GaN models"
}
```

- **quality_Q**：精度组件。你的势函数在常见构型上的表现。
- **coverage_N**：覆盖组件。你的训练数据覆盖了多少物理空间。
- **eta_at_audit_time**：审计时的探索-利用权重。早期审计 η 大（鼓励覆盖），后期 η 小（注重精度）。
- **cercis_percentile**：在同材料体系的被审计模型中的排名。

### 8.4 数据质量摘要

```json
{
  "data_quality": {
    "total_samples": 12500,
    "clean": 11240,
    "noisy": 860,
    "ambiguous": 400,
    "clean_ratio": 0.899
  }
}
```

### 8.5 逐状态分析

```json
{
  "state_analysis": [
    {
      "state_id": 0,
      "state_label": "bulk_wurtzite_equilibrium",
      "sample_count": 2500,
      "verdict": "clean",
      "consensus_score": 0.94,
      "cercis_component": 0.91,
      "expert_agreement": "5/5"
    },
    {
      "state_id": 1,
      "state_label": "N_vacancy_3c",
      "sample_count": 420,
      "verdict": "ambiguous",
      "consensus_score": 0.61,
      "cercis_component": 0.58,
      "expert_agreement": "3/5"
    },
    {
      "state_id": 2,
      "state_label": "surface_10-10",
      "sample_count": 800,
      "verdict": "clean",
      "consensus_score": 0.87,
      "cercis_component": 0.84,
      "expert_agreement": "5/5"
    }
  ]
}
```

这里你能看到你的势函数在每种物理状态（平衡体相、空位缺陷、表面等）上的表现差异。状态是 Spring 自动发现的——你不必预先定义。

### 8.6 审计可验证声明

```json
{
  "verification": {
    "status": "VERIFIED",
    "reproducible_by": "any third party with access to the same training data and M=5 independent NEP models",
    "theorem_basis": "Yajie Theorem 1: multi-expert consensus with exponentially decaying false-positive probability"
  }
}
```

---

## 9. 对比：自报 RMSE vs Spring 审计

### 9.1 场景

两个组各自训练了 GaN 的 NEP 势函数。都声称自己的模型"在测试集上达到 state-of-the-art"。

**组 A（不加 Spring）：**

```
训练方式：GPUMD nep 模块
训练数据：~5000 条 DFT 构型（含 AIMD 轨迹）
测试集 RMSE：energy = 0.48 meV/atom, force = 42 meV/Å
发布：arXiv 上说 "our NEP achieves SOTA accuracy on GaN"
```

**组 B（加 Spring）：**

```
训练方式：GPUMD nep 模块（相同的 nep 版本）
训练数据：~5000 条 DFT 构型（含 AIMD 轨迹）
Spring 审计结果：
  - M_t = 1048673 (数据绑定验证通过)
  - Cercis Score = 0.783
  - M_experts = 5, experts_passed = 4/5
  - 数据质量：CLEAN 4520 / NOISY 320 / AMBIGUOUS 160
  - 逐态分析：bulk_equilibrium Cercis 0.94, defect Cercis 0.61
发布：附带 .scxp 文件和审计报告
```

### 9.2 区别在哪


| 维度             | 组 A（自报 RMSE）             | 组 B（Spring 审计）                |
| ---------------- | ----------------------------- | ---------------------------------- |
| **可信度**       | 自己说自己好                  | 第三方独立验证（多专家交叉）       |
| **可复现性**     | 测试集不公开 → 无法复现      | 数据哈希绑定 → 可验证             |
| **可比较性**     | RMSE 依赖测试集 → 跨组不可比 | Cercis 统一标准 → 跨组可比        |
| **数据质量可见** | 不知道训练集里有多少脏数据    | NOISY/AMBIGUOUS 明确标出           |
| **势函数弱点**   | 不知道——只能靠试            | 逐态分析告诉你哪些构型表现差       |
| **作弊难度**     | 低（挑好的 checkpoint 报）    | 高（M_t 绑定数据，改了就能检测到） |

### 9.3 组 B 的审计报告更有说服力

不是因为"Spring 说它好"——而是因为：

1. **Cercis 0.783 是独立验证的结果**，不是你自己的 NEP 模型在自评
2. **M_t = 1048673 证明你没有换数据**——如果组 B 后来偷偷替换了训练集，M_t 会变
3. **experts_passed = 4/5** 说明 5 个独立专家中有 4 个一致同意——有一个偏离，但多数通过
4. **defect Cercis 0.61 < bulk Cercis 0.94** 诚实地告诉你这个势函数在缺陷构型上还有提升空间

这比"我们 force RMSE = 42 meV/Å"有诚意的多。

---

## 10. 三步开始

### Step 1：克隆仓库

```bash
git clone https://github.com/shuchaoxi/SCX.git
cd SCX
```

### Step 2：安装

```bash
pip install -e .
```

验证安装：

```bash
spring-md --version
# Spring MD v2.1.0
```

### Step 3：跑第一次审计

```bash
# 假设你已经有一个 NEP 势函数
spring-md audit \
  --format nep \
  --input /path/to/your/nep.txt \
  --data /path/to/your/training_data/ \
  --experts 5 \
  --output my_first_audit
```

跑完之后，看一下审计报告：

```bash
cat my_first_audit_report.json | python -m json.tool | head -30
```

或者用 Spring 自带的报告查看器：

```bash
spring-md report --input my_first_audit_report.json
```

---

## 11. 高级用法

### 11.1 调整专家数量 M

```bash
# M=3：快速审计，适合开发阶段
spring-md audit --experts 3 ...

# M=5：推荐，平衡速度和审计质量
spring-md audit --experts 5 ...

# M=10：最严格的审计，适合正式发布
spring-md audit --experts 10 ...
```

M 越大，噪声检测越准确（指数级收敛），但运行时间成比例增加。日常开发用 M=3，正式发布用 M=5 或以上。

### 11.2 指定 Cercis 衰减策略

```bash
# 默认：指数衰减（推荐）
spring-md audit --cercis-schedule exponential ...

# 逆衰减：长期运行，缓慢降低探索权重
spring-md audit --cercis-schedule inverse ...

# 余弦衰减：有限轮次，平滑归零
spring-md audit --cercis-schedule cosine ...
```

大多数情况下默认的 `exponential` 就够用。如果你的训练数据特别大、覆盖特别广，用 `inverse` 可以让探索期更长。

### 11.3 只跑数据质量检查（不生成完整审计）

如果你只想看一下训练集里有多少脏数据，不需要完整审计：

```bash
spring-md yajie \
  --data training_data/ \
  --experts 5 \
  --output data_quality_check
```

输出：`data_quality_check.csv`（每行一条数据的 CLEAN/NOISY/AMBIGUOUS 标签）。

### 11.4 审计多个势函数并横向对比

```bash
spring-md audit --input model_A.txt --data data_A/ --output audit_A
spring-md audit --input model_B.txt --data data_B/ --output audit_B

spring-md compare audit_A_report.json audit_B_report.json
```

输出：

```
Model        Cercis    M_t        Data Quality    Verdict
──────────────────────────────────────────────────────────
model_A      0.783     1048673    89.9% clean     ✅ VERIFIED
model_B      0.812     998244     92.1% clean     ✅ VERIFIED

Winner: model_B (+0.029 Cercis)
```

### 11.5 自定义专家模型

默认情况下，Spring 用不同的随机种子训练 N 个 NEP 变体作为专家。你也可以提供自己的专家模型：

```bash
spring-md audit \
  --format nep \
  --input nep.txt \
  --data training_data/ \
  --expert-models expert1.txt expert2.txt expert3.txt expert4.txt expert5.txt
```

这在以下场景有用：

- 你用不同的超参数训练了多个变体
- 你想用不同架构的模型做交叉验证（比如一个 NEP + 一个 DeepMD + 一个 MACE 做专家）
- 你从不同 checkpoint 取了多个模型

### 11.6 审计流水线自动化

如果你想在每个训练 epoch 之后自动跑审计：

```bash
# 在你的训练脚本最后加上
spring-md audit \
  --format nep \
  --input ${LATEST_CHECKPOINT} \
  --data ${TRAINING_DATA_DIR} \
  --experts 5 \
  --output audit_epoch_${EPOCH} \
  --quiet   # 不打印详细日志

# 收集所有 epoch 的 Cercis 分数
spring-md track --pattern "audit_epoch_*_report.json" --output cercis_trajectory.csv
```

你会得到一条 Cercis 收敛曲线，告诉你审计质量随训练的演变。

---

## 12. 常见问题

### Q1：我的训练数据要重新算吗？

**不需要。** 你现在用什么训练数据，直接喂给 Spring。XYZ 文件、DeepMD 的 set.000 目录、VASP 的 OUTCAR——Spring 都支持。

唯一的前提：你的训练数据里有能量/力/应力的 DFT 参考值。Spring 需要这些做多专家交叉验证。

### Q2：对 GPUMD 性能有影响吗？

**没有。** Spring 是审计工具，不是运行时组件。审计跑完之后，GPUMD 用 `.scxp` 或转回 `.nep.txt` 跑 MD——计算速度和你不加 Spring 时完全一样。

审计报告是独立的 JSON 文件，不参与 MD 计算，不影响任何物理量。

### Q3：可以用在 LAMMPS 上吗？

**可以。** Spring 支持 LAMMPS 的势函数格式（EAM、MEAM、ReaxFF 等）。步骤一样：

```bash
spring-md audit \
  --format lammps \
  --input potential.eam \
  --data training_data/ \
  --experts 5 \
  --output lammps_audited
```

对于 LAMMPS 的 pair_style 势函数，审计完转回原格式：

```bash
spring-md convert --input lammps_audited.scxp --to lammps --output potential_recovered.eam
```

然后在 LAMMPS 输入文件里照用：

```
pair_style eam/alloy
pair_coeff * * potential_recovered.eam Ga N
```

### Q4：M 设几比较好？

- **M=3**：开发阶段、快速迭代。审计速度快（~3x 训练时间），噪声检测够用。
- **M=5**：发布前审计。推荐。审计质量和速度的平衡点。
- **M=7 或以上**：正式论文、和别的组对比。噪声检测趋于完美。

M 越大，噪声检测的假阳性概率指数级下降（定理 1 保证），但运行时间线性增长。M=5 对绝大多数场景足够。

### Q5：Spring 需要 GPU 吗？

审计过程需要跑多次模型推理（M 个专家在训练集上推理）。如果你用的是 NEP——NEP 推理本身需要 GPU。Spring 本身不额外消耗 GPU 显存——它只是调用你的模型。

如果你的训练集是 5000 条 DFT 构型、M=5、每条构型 ~100 原子，整个审计在单张 GPU 上跑 10-30 分钟。

### Q6：我的老板/审稿人不了解 Spring 怎么办？

两种策略：

**策略一（推荐）：附 Cercis 分数 + 简短说明。** 在你的论文方法部分加一段：

> 我们使用 Spring MD（v2.1）对训练好的 NEP 势函数进行了独立审计。审计基于 M=5 个独立专家模型对训练集（5,000 条 DFT 构型）的交叉验证。审计结果：Cercis Score = 0.783，数据质量 CLEAN 比率 = 89.9%，M_t 验证通过审计完整性检查。审计报告随补充材料提供。

引用 Spring 的 arXiv 论文或 GitHub 链接即可。

**策略二：Cercis 分数和 RMSE 并报。** 在论文的表格里同时列出：


| 模型          | RMSE (meV/atom) | Cercis Score | M_t       |
| ------------- | --------------- | ------------ | --------- |
| NEP (ours)    | 0.48            | 0.783        | 1,048,673 |
| DeepMD (ours) | 0.52            | 0.791        | 987,654   |

这样即使审稿人不了解 Spring，也能看到第二个数字比第一个更有信息量。

### Q7：多组共用同一个训练集怎么比？

如果两个组用了同一套公开 DFT 数据集（比如 Materials Project 的 GaN 计算），Spring 的审计可以直接横向对比——因为训练集一样，数据哈希一样，M_t 一样。Cercis 分数的差异只来自势函数本身的质量。

这是 Spring 的杀手级场景：**统一训练集 + 不同势函数 + 统一审计 = 真正的公平对比。**

### Q8：Spring 是开源的吗？需要付费吗？

**完全开源。** MIT 协议。GitHub：`github.com/shuchaoxi/SCX`。不需要付费，不需要注册，不需要联网。

### Q9：Spring 支持哪些势函数格式？

当前支持：


| 格式                |    状态    | 备注                          |
| ------------------- | :---------: | ----------------------------- |
| NEP (GPUMD)         | ✅ 原生支持 | `nep.txt` → `.scxp` 双向转换 |
| DeepMD (DeePMD-kit) | ✅ 原生支持 | `frozen_model.pb` / `.pt`     |
| MACE                | ✅ 原生支持 | `.model` 格式                 |
| LAMMPS EAM/MEAM     |   ✅ 支持   | `potential.eam` / `.meam`     |
| LAMMPS ReaxFF       |   ✅ 支持   | `ffield.reax`                 |
| ACE (pace)          |  🔄 适配中  | `.yace` 格式                  |
| GAP (QUIP)          |  🔄 适配中  | `.xml` 格式                   |
| 通用格式            |   ✅ 支持   | 提供推理接口即可              |

### Q10：Yajie 标为 NOISY 的数据一定是错的吗？

**不一定。** Yajie 的 NOISY 标签意思是：M 个独立专家一致认为这条数据与训练集的主流模式不一致。

可能原因：

- DFT 计算确实有问题（最常见）
- 这条数据代表的是一个极稀有的物理状态，没有足够的训练样本支撑
- 这条数据恰好落在两个专家的分歧区域

建议：**抽查 NOISY 数据。** 如果是 DFT 问题，重新算。如果是稀有构型，增加该类型的数据。如果确实是正确的但被误标，手动改回 CLEAN。

---

## 总结

Spring MD 做了一件事：**把"我的势函数比别人好"从一句空话变成一个可验证的结果。** 不改变现有训练流程。NEP 照训，GPUMD 照跑。Spring 只加一步审计。

**文件位置：**


| 内容                | 路径                                               |
| ------------------- | -------------------------------------------------- |
| 源码                | `github.com/shuchaoxi/SCX` — `src/scx/`           |
| 测试                | `tests/` — 673 项全部通过                         |
| Spring MD 论文      | `papers/scx_spring_md/spring_md.tex`               |
| Spring 训练器论文   | `papers/scx_spring_trainer/spring_trainer.tex`     |
| Spring 统一框架论文 | `papers/scx_spring_framework/spring_framework.tex` |

**不解释。有代码。自己跑。**

```bash
git clone https://github.com/shuchaoxi/SCX.git
cd SCX
pip install -r requirements.txt
python -m pytest tests/ -q          # 673 passed
python -m scx.spring_md audit \     # 审计你的势函数
  --format nep --input your_nep.txt --data training_data/ --experts 5
```

---

## 附录：命令速查

```bash
# 审计 NEP 势函数
spring-md audit --format nep --input nep.txt --data ./data/ --experts 5 --output audited

# 审计 DeepMD 势函数
spring-md audit --format deepmd --input frozen_model.pb --data ./deepmd_data/ --experts 5 --output audited

# 审计 MACE 势函数
spring-md audit --format mace --input model.model --data ./training.xyz --experts 5 --output audited

# 只看数据质量
spring-md yajie --data ./training_data/ --experts 5 --output quality

# .scxp 转回原格式
spring-md convert --input audited.scxp --to nep --output recovered.txt

# 查看审计报告
spring-md report --input audited_report.json

# 验证审计完整性
spring-md verify --input audited.scxp

# 对比多个审计结果
spring-md compare audit_A_report.json audit_B_report.json

# 追踪审计收敛
spring-md track --pattern "audit_epoch_*_report.json" --output trajectory.csv
```

---

> **Spring MD — 审计层，不是新势函数。给 GPUMD/NEP/DeepMD 用户的一个诚实的工具。**
>
> GitHub: [github.com/shuchaoxi/SCX](https://github.com/shuchaoxi/SCX)
>
> 有问题提 Issue。或者跑一遍审计，看看你的 Cercis 分数是多少。
