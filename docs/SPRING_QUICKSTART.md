# Spring 快速上手指南：让你的模型从 M=1 变成可审计的

> **受众**：ML 工程师（懂训练流水线，不需要懂规范场论）
> **语言**：中文
> **风格**：直接、实用、不讲理论废话

---

## 目录

1. [Spring 是什么](#1-spring-是什么)
2. [我有什么好处](#2-我有什么好处)
3. [输入是什么](#3-输入是什么)
4. [中间做了什么](#4-中间做了什么)
5. [输出是什么](#5-输出是什么)
6. [代码在哪里](#6-代码在哪里)
7. [每个定理有什么用](#7-每个定理有什么用)
8. [三步集成](#8-三步集成)
9. [常见问题](#9-常见问题)

---

## 1. Spring 是什么

**Spring 不是一个新的模型架构。** 它是 SCX 框架的自我进化引擎——一个架在你的训练流水线之上的**审计层**。

一句话讲清楚：

> 你有一堆训练数据和一个模型。Spring 用多个独立专家对你的数据做交叉验证，自动识别噪声、去掉脏数据、追踪收敛状态、生成不可伪造的审计证据（M_t 参数）和一个可横向对比的质量分数（Cercis Score）。

对比一下：

| 你现在做的事 | 加了 Spring 之后 |
|---|---|
| 你自己说"我们模型最好" | Cercis 分数横向排名，第三方可验证 |
| 不知道数据集里有多少噪声 | Yajie 共识自动分类 CLEAN/NOISY/AMBIGUOUS |
| 数据质量靠人工抽查 | 多专家投票，概率保证（定理 1） |
| 没有审计痕迹 | M_t 参数从数据哈希派生，一旦改了数据 M 就变 |
| M=1（只有一个模型自评） | M>1（多个独立专家交叉审计） |

**核心洞察**：你自己的模型说自己是好的——这不叫审计（定理 3，老实人定理）。Spring 强制引入多个独立视角，让"好"变成一个可证明的结果。

---

## 2. 我有什么好处

### 2.1 可证明的数据质量

不用再靠"这个人看起来靠谱"来信任数据。Yajie 共识评分给每一条数据贴标签：

- **CLEAN** — 多数专家一致认为这条数据正确
- **NOISY** — 多数专家一致认为这条数据有问题
- **AMBIGUOUS** — 专家分歧大，需要人工核查

概率保证来自定理 1：M 个专家一致同意 → 数据的真实标签大概率就是这个。M 越大，保障越强。

### 2.2 M_t 自动生成，不可伪造

在传统场景下，M（专家数量）是你自己报的——你说用了几个专家就是几个。Spring 的 M 不是声明出来的，是**算出来的**：

```
M = SHA-256(你的训练数据集) 的前 20 位
```

改一条数据 → hash 变 → M 变。这叫**共生绑定（Symbiotic Binding）**，挂羊头卖狗肉在数学上不可行。

### 2.3 Cercis 分数可横向对比

不同公司、不同架构、不同数据集的模型，怎么比？

Cercis Score = **Q（精度）+ η·N（覆盖度）**

一个数字，排名一切。不关心你用什么架构（Transformer / Diffusion / MoE），只关心你的数据质量和模型在数据上的表现。

### 2.4 消除自卖自夸

每个公司都说"我们的模型取得了 SOTA 结果"。Spring 改变了游戏规则：

- **你没法挑选最好的一次 run 来报** — M_t 绑定数据，改了数据就能被检测到
- **你没法只报好的不报差的** — Cercis 分数覆盖全量数据，不是 cherry-pick 的 benchmark
- **你没法自己评自己** — 定理 3（老实人定理）从数学上证明了单模型自评无效

---

## 3. 输入是什么

Spring 需要三样东西，都是你已经有的：

### 3.1 你的训练数据

任何格式。CSV、JSON、Parquet、原始文本、图片目录……都行。Spring 不关心格式，只需要你的数据加载器能吐出 numpy 数组。

```python
# 例子：从你的数据加载器获取
X_train = your_dataloader.load()  # shape: (N, d) 或 (N, ...)
y_train = your_dataloader.labels()  # shape: (N,)
```

### 3.2 你的模型（任何架构）

Spring 对你的模型**零假设**：

- Transformer？没问题
- Diffusion model？没问题
- MoE（Mixture of Experts）？没问题
- 传统 CNN / LSTM？没问题
- 你自己搭的奇怪玩意？也没问题

你的模型只需要实现两个方法之一（Spring 会自动检测）：

```python
class YourModel:
    def predict(self, X):          # 返回预测值
        ...

    def predict_confidence(self, X):  # 返回置信度（更优）
        ...
```

### 3.3 你想验证的声称（可选）

你声称你的模型在某方面特别厉害？把那个场景的数据放进 Spring，它会告诉你这个声称是否经得起多专家审计。

例如：
- "我们在中文理解上超越了 GPT-4" → 用你的中文理解数据集跑一次 Spring
- "我们的模型对噪声极其鲁棒" → 用 Spring 的噪声检测反向验证

---

## 4. 中间做了什么

下面是 Spring 内部的工作流程。每一步都对应代码中的一个模块。

### 4a. 数据喂入 Spring → 多专家训练（M > 1，并行）

你提供 M 个预训练的专家模型（M ≥ 3 效果最好，M ≥ 5 推荐）。

```python
experts = [expert_1, expert_2, expert_3, ..., expert_M]  # 你的 M 个模型
```

Spring 并行运行所有专家对数据进行推理。这 M 个专家需要是**独立训练的**（不同的初始化、不同的数据子集、甚至不同的架构），这样才能保证交叉验证的有效性。

**如果你只有 1 个模型怎么办？** 从不同 checkpoint、不同超参数训练出 M 个变体即可。M=3 就能开始工作，M=5 效果显著。

### 4b. Yajie 共识评分 → CLEAN / NOISY / AMBIGUOUS 分类

这是 Yajie（雅洁）模块做的事：

```python
from scx.yajie import Yajie

yj = Yajie(grace=0.05, purity_threshold=0.9)
yj.fit(X_train, y_train, experts=experts, n_states=5)
```

内部流程：

1. **状态发现** — 用 K-Means 将数据聚类成 K 个状态（相似的数据聚在一起）
2. **多专家评估** — M 个专家在每个状态上打分
3. **共识计算** — 如果 M 个专家在某个样本上一致犯错 → 很可能是标签噪声；如果专家分歧巨大 → 这个样本"难"但可能是合理的
4. **分类阈值** — 用中位数分割法自动划分干净/噪声/模糊边界

你得到的是一个 DataFrame，每一行是一条数据：

| sample_id | state_id | verdict | state_quality | state_noise | state_cercis |
|-----------|----------|---------|---------------|-------------|--------------|
| 0 | 2 | clean | 0.92 | 0.05 | 0.93 |
| 1 | 0 | noisy | 0.45 | 0.78 | 0.48 |
| 2 | 3 | ambiguous | 0.67 | 0.45 | 0.69 |

### 4c. 噪声自动剔除 → 数据越来越干净

标注为 `noisy` 的数据被 Yajie 自动过滤掉。这不是一次性操作——在 Spring 自我进化循环中，每一轮都会重新评估，数据越来越干净：

```
Round 1: 10,000 条数据 → Yajie → 8,500 CLEAN, 1,000 NOISY, 500 AMBIGUOUS
Round 2: 8,500 条 CLEAN → 新模型 → Yajie → 8,200 CLEAN, 150 NOISY, 150 AMBIGUOUS
Round 3: ...
```

噪声率持续下降，干净的训练集持续收敛。

### 4d. Spring 自进化 → Lyapunov 监控收敛

Spring 的核心是一个六步循环（每轮迭代）：

```
while t < T_max:
    1. Explore  — 从候选池抽样（η(t) 控制探索强度）
    2. Evaluate — 质量分 + 新颖度 bonus
    3. Store    — 前 k 名进入记忆库 M_t
    4. Update   — NEP 学生模型在 M_t 上更新
    5. Refine   — 守门人 Bayesian 后验更新
    6. Decay    — η(t) = η_init × exp(-t / τ)
```

Lyapunov 函数 Φ 在每一步被估算，用来判断系统是否在收敛：

```python
lyap = spring.lyapunov_estimate(reference_features)
```

- **Φ 持续下降** → 训练在收敛，系统越来越好 ✓
- **Φ 震荡不降** → 可能卡在局部最优，需要加大 η（探索率）
- **Φ 突然发散** → 数据或模型出了问题，需要排查

工程上，你不需要手动监控。Spring 内置了 `convergence_diagnostic()` 方法自动判断当前状态：

```python
diag = spring.convergence_diagnostic()
print(diag)  # {'converged': True, 'regime': 'classical_convergence', ...}
```

### 4e. M_t 自动生成（数据哈希绑定，不可伪造）

在传统的训练报告里，M=1 意味着"我自己评自己"。Spring 改变了这一点：

**M 不是你声明的——M 是从你的训练数据的 SHA-256 哈希中算出来的。**

```python
from scx.m_registry import MRegistry

registry = MRegistry()
entry = registry.register(
    entity_id="your-company",
    data_hash="a1b2c3d4...（64位SHA-256）",
    domain="language-modeling",
    code_hash="e5f6g7h8...",
)
print(f"M = {entry.M}")  # M 被自动计算，你没法挑
```

M-Registry 是公开的、只追加的账本。一旦注册，不可篡改。

**共生绑定机制**：
- 你提交数据哈希 → M 被自动推算
- 改数据 → 哈希不同 → M 不同 → 不匹配 → 审计失败
- 想挂羊头卖狗肉（声称用了 5 个专家，实际上只用 1 个）→ M 和实际数据对不上 → 立即检测到

### 4f. Cercis 分数产出（精度 + 覆盖度）

Cercis Score 是整个流程的最终输出——一个 0 到 1 之间的数字，越高越好：

```
S(s) = Q(s) + η(t) · N(s)
```

- **Q(s)** = 质量组件：多专家共识精度。专家们越一致、置信度越高，Q 越大。
- **N(s)** = 噪声/新颖度组件：覆盖了多少"冷门"数据。你的模型在罕见样本上也表现好，N 就高。
- **η(t)** = 时间衰减权重：早期鼓励探索（η 大），后期注重精度（η 小）。

五种内置权重衰减策略（在 `cercis.py` 中）：

| 策略 | 公式 | 适用场景 |
|------|------|----------|
| constant | η(t) = η₀ | 快速原型、不在乎探索 |
| exponential | η(t) = η₀ · e^(-λt) | **推荐**：一般用途 |
| inverse | η(t) = η₀ / (1 + λt) | 长期运行、需要缓慢衰减 |
| step | η(t) = η₀ · γ^⌊t/τ⌋ | 阶段性部署 |
| cosine | η(t) = η₀ · ½(1+cos(πt/T)) | 有限轮次、平滑归零 |

---

## 5. 输出是什么

运行完 Spring，你拿到三样东西：

### 5.1 训练好的模型

你的 NEP 学生模型已经在清理后的数据（去掉了噪声样本）上完成了训练。这个模型的性能会比你在原始数据上训练的好，因为脏数据已经被自动剔除了。

### 5.2 M_t 参数（证明审计过）

M-Registry 中的一条不可变记录，包含：

- `entity_id`：你的公司/团队标识
- `M`：从数据哈希自动推算的专家数量
- `data_hash`：你的训练数据的 SHA-256
- `code_hash`：你的训练代码的哈希
- `commitment_hash`：所有字段加密绑定，防篡改
- `verification_status`：`VERIFIED` / `DISCREPANCY` / `PENDING`

这个记录可以附在你的模型卡（Model Card）上，向第三方证明你的训练过程经过了独立审计。

### 5.3 Cercis 分数（证明有多好）

一个 0~1 的标量，可以和其他模型的 Cercis 分数直接比较。

```
Model A: Cercis = 0.87
Model B: Cercis = 0.82
Model C: Cercis = 0.91  ← 最好
```

你可以用这个排序取代"我们在 XX benchmark 上取得了 SOTA"。

**附一个输出示例**：

```python
# 运行完成后
print(f"M_t = {entry.M}")
print(f"Verification = {registry.verify('your-company')}")  # VERIFIED
print(f"Cercis Score = {cercis_score:.4f}")

# 在模型卡上:
# ---
# Audit: Spring SCX v2.1
# M = 1048575 (symbiotic-bound, SHA-256 verified)
# Cercis Score = 0.873
# Verification: PASS
# ---
```

---

## 6. 代码在哪里

Spring 框架的代码组织非常清晰，按模块分文件：

### 核心模块

| 文件路径 | 功能 | 关键类/函数 |
|----------|------|------------|
| `src/scx/spring.py` | Spring 自我进化引擎 | `Spring`, `SpringConfig`, `MemoryBank`, `Gatekeeper`, `evolve()` |
| `src/scx/yajie.py` | Yajie 数据净化器 | `Yajie`, `yajie()`, `clean()` |
| `src/scx/cercis.py` | Cercis 评分 | `CercisScore`, `ConstantSchedule`, `ExponentialSchedule` 等 |
| `src/scx/m_registry.py` | M 参数注册表 | `MRegistry`, `MRegistryEntry` |
| `src/scx/m_parameter.py` | M 参数计算 | `derive_M_from_data_hash()`, `compute_M_min()`, `compute_f1_bound()` |
| `src/scx/situs.py` | 位置编码 | `SitusEncoder`, `SitusEncoder3D` |

### 支撑模块

| 文件路径 | 功能 |
|----------|------|
| `src/scx/theorem3.py` | 定理 3（老实人定理）可执行实现 |
| `src/scx/valuation/noise_score.py` | 噪声评分（定理 1 的基础） |
| `src/scx/valuation/state_value.py` | 状态价值评估（定理 1/2 边界） |
| `src/scx/valuation/redundancy.py` | 冗余度评估 |
| `src/scx/valuation/classifier.py` | 数据分类器 |
| `src/scx/valuation/base.py` | 评分基类 |
| `src/scx/state/discovery.py` | 状态发现（聚类） |
| `src/scx/core/config.py` | 全局配置 |
| `src/scx/expert/reliability.py` | 专家可靠性评估 |
| `src/scx/expert/router.py` | 专家路由器 |
| `src/scx/expert/conflict.py` | 专家冲突检测 |

### 测试文件

| 文件路径 | 测试内容 |
|----------|----------|
| `tests/test_yajie.py` | Yajie 扫描、清理、便捷函数 |
| `tests/test_yajie_fit.py` | Yajie 完整流水线（状态发现 → 评分 → 分类） |
| `tests/test_cercis.py` | Cercis 评分、五种衰减策略、组件分离 |
| `tests/test_m_registry.py` | M-Registry 注册、验证、共生绑定 |
| `tests/test_situs.py` | 位置编码正确性、Lipschitz 常数 |
| `tests/test_theorem3.py` | 定理 3 不可区分性验证 |
| `tests/test_expert.py` / `test_expert_module.py` | 专家路由和可靠性 |

### 入口文件

```
src/scx/__init__.py          # 包入口
src/scx/core/__init__.py     # 核心模块聚合
```

---

## 7. 每个定理有什么用

这里用 ML 工程师的语言解释 SCX 的定理——不讲证明，只讲"这个定理对你有什么用"。

### 定理 1：噪声检测定理

> **"M 个独立专家一致认为某条数据是错的 → 这条数据大概率就是错的。"**

**给你的价值**：
- 这是 Yajie 共识评分的理论基础
- M 越大，检测噪声的能力越强（指数级收敛）
- 工程建议：M ≥ 5 能稳定工作，M ≥ 10 的噪声检测几乎完美
- 你的每一个独立训练的 checkpoint 都可以充当一个专家

**直觉**：如果 5 个人都说这道题做错了，那这道题大概率就是错了——不太可能是 5 个人同时看走眼。

### 定理 3：老实人定理

> **"单模型自评在数学上是无效的。从观测数据中，你无法区分标签噪声和样本本身的固有难度。"**

**给你的价值**：
- 这是"为什么你需要 Spring"的根本原因
- 你自己的模型在自评 benchmark 上跑出高分——这不叫审计
- 噪声和难度在观测上是不可区分的（二元世界构造证明）
- 唯一的出路：引入外部独立视角（即 M > 1）

**直觉**：一道题所有人（包括你自己）都做错了——可能是题出错了（标签噪声），也可能是题太难（固有难度）。只看一个人做这题的结果，你永远分不清是哪种情况。

### Yajie 共识机制

> **"多个独立专家给同一条数据打分。打分越一致 → 数据越可能是干净的。打分越分散 → 数据越可疑。"**

**给你的价值**：
- 这是 Spring 中实际运行的共识算法
- 一致性分数 C_i ∈ [0, 1]：
  - C_i > 0.8：所有专家都失败 → **NOISY**（大概率标签错了）
  - C_i < 0.2：专家一致正确 → **CLEAN**（数据没问题）
  - 中间值：部分专家对部分错 → **AMBIGUOUS**（需要更多信息）
- 你的训练数据会被自动分成这三类
- 不需要人工标注，不需要预先知道哪些数据是脏的

### Spring 收敛定理（Lyapunov）

> **"Lyapunov 函数 Φ(S_t, θ_t) 单调下降 → 系统在收敛。不下降 → 出问题了。"**

**给你的价值**：
- 这是你的训练监控仪表盘
- 不需要盯着 loss 曲线猜——Φ 下降就是好的，Φ 震荡就是需要干预
- `spring.convergence_diagnostic()` 自动判断四种收敛状态：
  - `classical_convergence`：已收敛 ✓
  - `approaching_fixed_point`：接近收敛
  - `limit_cycle_suspected`：可能卡循环了
  - `evolving`：还在训练中

**直觉**：Lyapunov 就像物理系统的能量。能量一直降 → 小球滚到坑底。能量不降了 → 到了稳态或卡住了。

### Cercis 分数

> **"Cercis = Q（精度） + η·N（覆盖度）。一个数字，排名一切。"**

**给你的价值**：
- Q 看的是"在常见数据上你多准"
- N 看的是"在冷门数据上你多全"
- η 控制权重：早期 η 大 → 鼓励覆盖冷门数据；后期 η 小 → 更看重精度
- 你可以和任何模型比 Cercis，不管它用什么架构
- 分数来自全量数据，不是 cherry-pick 的 5 个 benchmark

### 共生绑定（M_t）

> **"M 不是你自己报的——是从你的数据哈希里算出来的。改了数据 M 就变。"**

**给你的价值**：
- 这是审计可信度的根基
- 再也无法"声称用了 10 个专家但实际只用了 1 个"
- 再也无法"报了最好的 run 而隐藏了其他失败的 run"
- 第三方可以直接验证：拿你的数据 → 算 hash → 比对 M → 确认一致性
- M-Registry 公开可查，一次注册永久可审计

---

## 8. 三步集成

最简单的接入方式，三步走。

### Step 1：安装

```bash
# 方式一：pip 安装（如果已发布到 PyPI）
pip install scx

# 方式二：从源码安装（推荐，保证最新）
git clone https://github.com/your-org/SCX.git
cd SCX
pip install -e .
```

安装后验证：

```python
from scx.yajie import Yajie
from scx.spring import Spring
from scx.cercis import CercisScore
print("OK — Spring is ready.")
```

### Step 2：把你的训练数据路径给 Spring

最简用法——一行代码启动 Yajie 数据净化：

```python
import numpy as np
from scx.yajie import Yajie

# 1. 加载你的数据
X_train = np.load("your_training_data.npy")  # 或你自己的加载逻辑
y_train = np.load("your_labels.npy")

# 2. 准备 M 个专家（你的模型的不同 checkpoint）
def make_expert(checkpoint_path):
    """加载你模型的一个 checkpoint 作为专家"""
    model = YourModel()
    model.load_weights(checkpoint_path)
    return lambda x: model.predict(x)

checkpoints = [
    "checkpoints/model_epoch_10.pt",
    "checkpoints/model_epoch_20.pt",
    "checkpoints/model_epoch_30.pt",
    "checkpoints/model_epoch_40.pt",
    "checkpoints/model_epoch_50.pt",
]
experts = [make_expert(ckpt) for ckpt in checkpoints]

# 3. 一键净化
yj = Yajie(grace=0.05, purity_threshold=0.9)
yj.fit(X_train, y_train, experts=experts, n_states=5)

# 4. 查看报告
print(yj.state_report_)

# 5. 提取干净数据，继续训练
clean_mask = yj.report_["verdict"] == "clean"
X_clean = X_train[clean_mask]
y_clean = y_train[clean_mask]
print(f"Retained {len(X_clean)}/{len(X_train)} ({100*len(X_clean)/len(X_train):.1f}%) samples")
```

如果你还想运行完整的 Spring 自我进化：

```python
from scx.spring import Spring, SpringConfig

config = SpringConfig(
    max_iterations=50,
    eta_init=0.3,
    tau_decay=20.0,
    top_k=20,
    n_states=10,
)
spring = Spring(config, nep_student=your_model)
spring.initialize(feature_matrix=X_clean)
history = spring.evolve(candidate_pool=X_clean)

# 监控收敛
diag = spring.convergence_diagnostic()
print(f"Regime: {diag['regime']}, Converged: {diag['converged']}")
```

### Step 3：拿到 M_t + Cercis 分数，附在你的模型卡上

```python
from scx.m_registry import MRegistry
from scx.m_parameter import hash_data_manifest, derive_M_from_data_hash
from scx.cercis import CercisScore
import hashlib

# === 生成 M_t ===
# 计算你的训练数据的哈希
data_hash = hashlib.sha256(X_train.tobytes()).hexdigest()
code_hash = hash_data_manifest(["src/model.py", "src/trainer.py"])

# 注册到 M-Registry
registry = MRegistry()
entry = registry.register(
    entity_id="your-company",
    data_hash=data_hash,
    domain="language-modeling",
    code_hash=code_hash,
)

# === 生成 Cercis 分数 ===
cercis = CercisScore(schedule="exponential", schedule_kwargs={"eta0": 0.5, "lam": 0.05})
cercis_score = cercis.score_batch(
    votes_batch=expert_votes,
    states=X_clean,
    memory=None,
    t=50.0,  # 最终时刻
).mean()

# === 附在你的模型卡上 ===
print(f"""
---
## Audit Trail (Spring SCX)

| Parameter | Value |
|-----------|-------|
| M (symbiotic) | {entry.M} |
| Data Hash | {data_hash[:16]}... |
| Verification | {registry.verify('your-company')} |
| Cercis Score | {cercis_score:.4f} |
| Noise Removed | {100 - 100*len(X_clean)/len(X_train):.1f}% |

*Audited by Spring SCX. M_t is symbiotically bound to training data hash.*
*Cercis Score = Q (precision) + η·N (coverage). Higher is better.*
""")
```

**完工。** 你的模型现在有了可审计的出生证明。

---

## 9. 常见问题

### Q: 我不懂数学（规范场论、Lyapunov、Bayesian……），能用吗？

**能。** Spring 是一个工程工具，不是一篇论文。你不需要理解 Lyapunov 函数的数学推导，只需要知道：

- Lyapunov 下降 = 好
- Lyapunov 不降 = 查问题

就像你不需要理解 TCP 三次握手才能用 `requests.get()` 一样。

所有复杂的数学都被封装到了 `Spring`, `Yajie`, `CercisScore` 这三个类里。你用 `fit()` / `evolve()` / `score()` 这三个方法就够了。

### Q: 我的模型不是 Transformer，能用吗？

**能。** Spring 对你的模型架构零依赖。

Spring 只要求你的模型能输出**预测结果**（或预测置信度）。不管是 Transformer、Diffusion、CNN、LSTM、MoE、还是你自己写的奇怪玩意，只要有一个 `predict(X) -> y` 接口就行。

```python
# 任何模型都可以
spring.set_nep_student(any_model_with_predict_method)
```

### Q: M 设几比较合适？

| M 值 | 效果 | 算力需求 |
|------|------|----------|
| M=1 | 你自己评自己（无效，见定理 3） | 最低 |
| M=3 | 开始有效，但精度有限 | 低 |
| M=5 | **推荐起点**，噪声检测可靠 | 中等 |
| M=10 | 噪声检测近乎完美 | 高 |
| M≥20 | 超额保障，除非对审计要求极高 | 很高 |

**实际建议**：取你训练过程中的 5 个不同 checkpoint（epoch 10, 20, 30, 40, 50）作为 M=5 的专家。不需要额外训练。

### Q: Spring 和现有的 eval benchmark（MMLU, HumanEval, etc.）是什么关系？

**互补关系，不是替代关系。**

| 维度 | Benchmark | Spring |
|------|-----------|--------|
| 测什么 | 最终性能（分类准确率、生成质量） | 数据质量和模型可审计性 |
| 谁来测 | 你自己跑（可能 cherry-pick） | 第三方可验证 |
| 可比性 | 跨模型对比依赖同样的 benchmark 设定 | Cercis 分数一个数字直接比 |
| 审计能力 | 无 | M_t 不可伪造、全量数据覆盖 |

建议：两个都用。Benchmark 证明你的模型能力强，Spring 证明你没有在数据上做手脚。

### Q: 需要多少算力？

Spring 的主要算力开销来自多专家推理。如果你用 M=5 的配置：

- **Yajie 单次扫描**：≈ 5 次模型前向传播（每专家一次）。对于百万级数据集，和一次 validation 差不多。
- **Spring 自我进化**：取决于迭代次数 T。默认 T=50，每次迭代处理 top_k=20 条数据，开销很低。
- **Cercis 打分**：基本上是纯计算，不需要 GPU。

**结论**：Spring 的算力开销远小于一次训练 run。如果你的训练花了 100 GPU-hours，Spring 可能只需要 2-5 GPU-hours。

### Q: 我的数据不是分类问题，是生成式任务（文本生成、图像生成），能用吗？

**能。** 专家一致性不要求你的任务是分类。Yajie 的核心逻辑是：

1. 多个专家对同一输入产生输出
2. 比较这些输出的差异程度
3. 差异大 → 可能是噪声/困难样本；差异小 → 数据干净

对于生成式任务，你可以定义自己的"差异度量"（如 BLEU、ROUGE、CLIP score、FID 等），只要它能衡量两个输出之间的差异即可。

### Q: 我需要把全部训练数据都跑一遍吗？

**不需要。** 建议策略：

1. **抽样**：从你的训练集中随机抽 10%-20% 数据
2. 用 Yajie 检测这部分的噪声率
3. 如果噪声率 < 5%：你的数据质量不错，可以放心
4. 如果噪声率 > 15%：建议对全量数据跑一遍 Yajie，剔除噪声

这比人工抽检高效得多，而且有统计保证（定理 1 给了置信度边界）。

### Q: Spring 和 Data-Centric AI（数据为中心 AI）的趋势有什么关系？

Spring 是 Data-Centric AI 的**工程化落地**：

- Data-Centric AI 说："与其调模型参数，不如清理数据"
- Spring 做到了："自动清理数据，并且能证明你清理了"

一致性：
- 数据质量自动评估 ✓
- 噪声自动剔除 ✓
- 数据迭代闭环 ✓
- 可审计、可复现 ✓ ← Spring 独有的

### Q: 如果我的模型还没训练完，能在训练过程中用 Spring 吗？

**能。** 这正是 Spring 的设计目标之一。

```python
# 在你的训练循环中
for epoch in range(total_epochs):
    # 正常训练一步
    model.train_step(batch)

    # 每 N 个 epoch，用 Spring 审计一次数据质量
    if epoch % 10 == 0:
        yj = Yajie()
        yj.fit(X_val, y_val, experts=[model], phi=model.encode)
        noise_rate = (yj.report_["verdict"] == "noisy").mean()
        print(f"Epoch {epoch}: estimated noise rate = {noise_rate:.2%}")
```

这让你能在训练过程中**实时感知数据质量**，而不是训完了才发现数据有问题。

---

## 附录：快速参考卡片

```python
# ========== 最小可用示例 ==========

# 1. 安装
# pip install scx

# 2. 导入
from scx.yajie import Yajie
from scx.spring import Spring, SpringConfig
from scx.cercis import CercisScore
from scx.m_registry import MRegistry

# 3. 数据净化（5 行）
experts = [model_v1, model_v2, model_v3, model_v4, model_v5]  # M=5
yj = Yajie()
yj.fit(X_train, y_train, experts=experts, n_states=5)
X_clean = X_train[yj.report_["verdict"] == "clean"]

# 4. 自我进化（3 行）
spring = Spring(SpringConfig(max_iterations=50))
spring.initialize(feature_matrix=X_clean)
history = spring.evolve(candidate_pool=X_clean)

# 5. Cercis 评分（2 行）
cercis = CercisScore(schedule="exponential")
score = cercis.score_batch(expert_votes, X_clean).mean()

# 6. M_t 注册（3 行）
registry = MRegistry()
entry = registry.register("your-company", data_hash, "your-domain", code_hash)
print(f"M={entry.M}, Cercis={score:.4f}, Verified={registry.verify('your-company')}")

# 完工。
```

---

## 蒸馏流程

Spring 训练好的大模型作为 Teacher，用 Yajie 共识清洗数据后训练小模型。

```
Step 1: Teacher 前向
  └─ 对每批数据，用不同策略（temperature 0.3/0.7/1.0, top-p 0.9/0.95）
     生成 M_eff 个独立路径的输出

Step 2: Yajie 共识评分
  └─ yajie.score(predictions) → 每个样本的共识分数 s_i
     s_i > 0.8  → CLEAN   → 保留
     s_i < 0.3  → NOISY   → 丢弃
     中间       → AMBIGUOUS → 可选人工审核

Step 3: 清洗后训练
  └─ 用 CLEAN 数据集训练 Student 模型
     Student 不需要 M>1 — 训练数据已经被审计过了

Step 4: 输出
  └─ Student 模型 + Cercis 分数
```

**注意：不需要先用 Yajie 单独洗数据再训练。Spring 的每一轮迭代本身就是训练 + 审计 + 清洗的循环。蒸馏场景是你已经有了一个 Spring 训练好的 Teacher，想产出一个更小的 Student。**

## 评判模型正确性

一个数字：**Cercis Score**。

- Q（质量/精度）：模型在测试集上的主指标
- N（新颖性/覆盖度）：模型覆盖的场景/领域广度
- S = Q + η·N：最终分数，$\eta$ 控制覆盖度的权重（默认 0.1）

横向对比不需要看论文里的 benchmark 表格——Cercis 分数跑完直接出。跨架构可比：Transformer 的 0.85 和 MoE 的 0.82 可以直接排。

## 数据如何判断

**核心原则：不需要你事先判断。Spring 替你判断。**

- 训练前：数据原样喂入
- Spring 内循环：每轮 Yajie 评分 → CLEAN/NOISY/AMBIGUOUS
- NOISY 自动剔除，CLEAN 继续训练
- 循环结束：数据已经是干净的，附带每轮审计日志

**如果你想事先了解数据质量：**
```python
from scx import Yajie
yajie = Yajie()
report = yajie.audit(dataset)  # 返回每个样本的 CLEAN/NOISY/AMBIGUOUS 标签
print(report.summary())        # 多少干净、多少噪声、多少模糊
```

---

> **Spring 快速上手指南** · 版本 1.0
> 适用于 SCX 框架 v2.x
> 面向 ML 工程师 · 不讲废话 · 直接能用
