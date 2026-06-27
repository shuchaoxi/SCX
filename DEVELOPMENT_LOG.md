# SCX 开发日志

> 最后更新：2026-06-26

---

## 核心思想的产生时间线

### 源头：EGP Paper 1 — ACE/PACE Gauge Fixing

- **2026-05 ~ 2026-06 上旬**：在 EGP（Expert-Guided Potential）项目——即 Paper 1 的 ACE/PACE 多专家势函数拼接工作中——用户注意到一个反复出现的现象：**同一专家（势函数）在不同构型空间区域上的预测可靠性存在显著差异**。这个观察是 SCX 全部思想的萌芽。

### 从 "Gauge" 到 "State Condition"

- **2026-06-15 ~ 2026-06-22**：在撰写 Paper 2（Residual-state error maps）和 Paper 3（Expert compiler + distillation）的过程中，用户开始将"专家可靠性随构型区域变化"这个经验观察形式化，逐步提炼出**状态条件专家性**（State-Conditioned Expertise）的概念雏形。
- 关键认识转变：专家可靠性不是全局常数（一个数字），而是状态 s 上的条件概率 SCX_m(s) = P(loss < tau | s)。

### SCX 概念形成

| 日期                 | 事件                                                                                                                                                                                       | 地点                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| **2026-06-23** | 与 GPT 讨论，首次系统性地将"状态条件专家性"从 EGP 项目中剥离，确认这是一个**独立于 DFT/Material Science 的通用 ML 数学框架**。概念正式成形。                                         | **个人电脑**（居家） |
| **2026-06-24** | 完成数学框架初稿：定义体系（SCX Reliability, Data Four-Classification, State-Wise AL, Expert Routing, Noise vs Hard State）+ 3 个核心命题的证明。                                          | **个人电脑**         |
| **2026-06-25** | SCX v0.1.0 Python 包完成：30 files, 6,269 lines of code, 259 tests 全部通过（3.37s）。同日创建 GitHub 私密仓库。代码全部由 AI (Claude Code+deepseek v4) 根据用户的数学框架和设计方向生成。 | **个人电脑**         |
| **2026-06-26** | SCX v0.2.0 理论扩展：完成 Compress Theorem（状态条件数据压缩的理论下界）和 Governance Protocol（多专家状态路由协议）的形式化证明。                                                         | **个人电脑**         |
| **2026-06-27** | SCX v0.4.0-pre 定理驱动重构：Theorem 1-3 + Proposition 1',3',4 证明完成，StateValue 定理化重构，yajie.py 新模块，427 tests。 | **个人电脑**         |

---

## 开发地点记录

| 组件                             | 开发设备           | 地点               | 说明                                                |
| -------------------------------- | ------------------ | ------------------ | --------------------------------------------------- |
| SCX 数学框架（定义、命题、证明） | 个人电脑           | 居家               | 所有理论工作均在个人时间和个人设备上完成            |
| SCX Python 实现（`src/scx/`）  | 个人电脑           | 居家               | 由 AI (Claude Code+deepseek v4) 在用户指导下生成    |
| SCX 实验（合成数据）             | 个人电脑           | 居家               | 合成数据生成 + 可视化，无需超算                     |
| SCX 测试套件（259 tests）        | 个人电脑           | 居家               | 全部在个人电脑本地运行通过                          |
| GitHub 仓库创建/管理             | 个人电脑           | 居家               | 私密仓库，用户个人 GitHub 账户                      |
| **EGP/AlGaN VASP 计算**    | **孝感超算** | **学校设备** | **仅限 EGP 项目的 DFT 计算，与 SCX 框架无关** |

> **关键声明**：SCX 项目所有理论工作、代码实现、实验验证均在**个人电脑**上完成，未使用学校设备或超算资源。孝感超算仅用于 EGP 项目（Paper 1-3）的 DFT 数据生成。

---

## 当前状态 (2026-06-27)

- **代码**：v0.4.0-pre（定理驱动架构），427 tests 通过
- **理论**：3 个核心定理 (Theorem 1-3) + 3 个命题 (Proposition 1', 3', 4) 全部证明完成
- **实验**：定理验证完成（Agent 独立验证发现 2+3 个 bug，已修复）
- **核心发现**：
  - Theorem 1：多专家一致性可检测噪声（Chernoff bound on false positives）
  - Theorem 2：弱特征状态下 SCX 必然失效（Fano inequality lower bound on AUC）
  - Theorem 3：噪声与困难样本本质不可区分（constructive two-world proof）
- **论文**：5 篇结构（噪声检测与压缩理论拆分为两篇）
- **商业化**：5 层资产模型集成

---

## 当前状态 (2026-06-26)

- **代码**：v4.0 Phase A（通用模块化架构），370 tests 通过
- **实验**：AlN v3 两层分析完成, scx-health v2 完成, SCX vs DFT 对比完成
- **核心发现**：SCX 100% 命中已知噪声帧（数据防中毒），两层 F1 2.3x 提升
- **关键认知**：弱特征 → SCX 失效（AlN 12-dim, SimpleCNN 128-dim, DermaMNIST uniform noise 三条线汇聚）
- **论文**：EGP→SCX-Theory→SCX-MLIP→SCX-Sim→SCX-Health 序列确定

---

## 关键里程碑

### 2026-06-26：SCX v4.0 Phase A + 两层描述符 + 数据防中毒验证

- **通用模块化架构**：抽象基类 (SCXStateEncoder, SCXExpert) + YAML 域配置，新域 3 步接入
- **两层描述符**：ErrorDrivenEncoder + TwoLayerStateDiscovery — Layer 1 人工 + Layer 2 错误驱动聚类
- **AlN v3 两层分析**：max blob 50%→33%，noise F1 0.253→0.585, phonon 100% 隔离
- **SCX vs DFT**：SCX 噪声帧 100% 覆盖 REPORT 最差帧，力 RMSE 预估降 29-48%
- **scx-health v2**：Noise + Routing 完成，Compress 揭示特征依赖性

### 2026-06-27：SCX v0.4.0-pre — 定理证明 + 代码重构

- **Theorem 1 (Multi-Expert Consistency for Noise Detection)** — PROVED：多专家在状态 s 上一致性显著高于随机水平 → 该样本为噪声。假设 A1-A6，核心工具：Chernoff bound + Hoeffding inequality。
  - Bug fix：Lemma 3 重构（新增 A6 假设），Chernoff KL 方向修正
- **Theorem 2 (Weak Feature Failure Lower Bound)** — PROVED：若状态 s 中所有特征与误差的互信息 I(X_j; L) 低于 delta，则任何噪声检测器的 AUC 被 Fano inequality 限制在 0.5 + epsilon。
  - Bug fix：AUC eta-dependence 添加，k-means 最优性声称移除，cluster balance qualifier 添加
- **Theorem 3 (Unidentifiability of Noise vs Difficulty)** — PROVED：给定"噪声"和"困难样本"的经验不可区分性，两个世界构造性证明（数据分布相同，但标签生成机制不同）。
- **Proposition 1' (Global Regret Lower Bound)** — PROVED：全局最优路由策略的 regret 下界（替代原有弱"no global optimal"反例）。
- **Proposition 3' (State-Conditioned Weighting Advantage)** — PROVED：通过 Jensen 不等式证明状态条件加权策略优于全局均匀加权。
- **Proposition 4 (Compression Fidelity)** — FIXED：利用 Theorem 1 一致性修正了循环定义。
- **Arrow's impossibility analogy** — REMOVED & archived 到 `theory/archive/arrow_analogy_removed.md`。
- **代码重构**：
  - `src/scx/valuation/state_value.py` — 添加 theorem-based 方法：noise_consistency_score, optimal_noise_threshold, noise_detection_f1_bound, chernoff_bound, hoeffding_bound, feature_strength_diagnostic；旧 V(s) 方法标记 deprecated
  - `src/scx/yajie.py` — 新模块（雅洁：优雅的数据清理器）
  - `tests/test_yajie.py` — 新测试文件
- **测试**：427 tests 全部通过（新增 ~57 tests）
- **论文规划**：4→5 篇拆分（噪声检测理论和压缩理论各成一篇）；商业化 5 层资产模型集成
- **Obsidian 知识库**：新增 `08_说明书/`（面向非专家的定理解释：7 个文件）
- **数字谱系追溯**：Condorcet (1785), Dawid-Skene (1979), Fano (1961), Le Cam (1973), Tsybakov (2009)

### 2026-06-23：SCX 概念正式形成

与 GPT 深度讨论后，用户将"状态条件专家性"概念从 EGP/MLIP 语境中完全剥离，确立为独立 ML 理论框架：

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )
```

核心洞见：数据价值不是样本固有属性，而是由**状态 s**、**专家可靠性 SCX_m(s)**、和**当前模型缺陷**共同决定的条件量。

### 2026-06-25：SCX v0.1.0 Python 包完成

- **30 个源文件**，6,269 行 Python 代码
- **259 个单元测试**，全部通过（运行时间 3.37s）
- 覆盖 6 个子模块：`core`, `state`, `expert`, `valuation`, `action`, `utils`
- 同日创建 GitHub 私密仓库

### 2026-06-26：SCX v0.2.0 理论扩展

- **Compress Theorem**：状态条件数据压缩的信息论下界，证明基于状态密度的加权压缩在保留 SCX 信息的意义上优于全局均匀压缩
- **Governance Protocol**：多专家场景下的状态路由协议，包括专家冲突检测、可靠性仲裁、负载均衡机制的形式化描述

---

## 代码生成说明

SCX Python 包的**所有代码**均由 AI 工具 **Claude Code (Anthropic)** +deepseek v4pro生成，具体分工如下：

| 角色                  | 工作内容                                                                             |
| --------------------- | ------------------------------------------------------------------------------------ |
| **用户**        | 数学框架设计（定义体系、命题提出、证明推导）、整体架构设计、算法伪代码、设计方向决策 |
| **Claude Code** | Python 代码实现、单元测试编写、API 接口设计、文档字符串、类型注解                    |

用户提供的是**数学框架和设计方向**，具体编码由 AI 完成。这是有意的分工策略——用户作为数学家/理论家专注于理论创新，实现细节交给 AI。

---

## 数据来源声明

| 数据类型                  | 来源                                                 | 与 SCX 框架的关系                        |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------- |
| 合成 2D 数据              | `experiments/synthetic/data_generator.py` 自行生成 | SCX 核心验证实验                         |
| MedMNIST                  | 公开数据集                                           | SCX 通用 ML 基准实验                     |
| CIFAR-10/100              | 公开数据集                                           | SCX 通用 ML 基准实验                     |
| **AlN v3 DFT 数据** | **EGP 项目**（孝感超算生成）                   | **仅作为 MLIP 案例展示（非必须）** |

> SCX 是一个**纯数学/ML 框架**，不依赖任何 DFT 数据。合成数据 + 公开基准数据集已足够验证 SCX 的所有核心主张。AlN v3 DFT 数据是 EGP 项目的成果，仅在 MLIP 案例中作为额外展示。

---

## 论文线上下文

| #                 | 主题                                | 工作目录           | SCX 的关系                                         |
| ----------------- | ----------------------------------- | ------------------ | -------------------------------------------------- |
| Paper 1           | ACE/PACE expert gauge + merge       | `egp/`           | SCX 思想的经验来源（观察到"专家可靠性随区域变化"） |
| Paper 2           | Residual-state error maps           | `egp/`           | 直接前驱，SCX 与之共享"状态"概念                   |
| Paper 3           | Expert compiler + distillation      | `egp/`           | 相关但独立                                         |
| **Paper 4** | **SCX-Theory: 状态条件噪声检测**    | **`SCX/`** | **Theorem 1-2 + 3 个命题，核心理论**       |
| **Paper 5** | **SCX-Compress: 状态条件压缩理论**  | **`SCX/`** | **从原 Paper 4 拆分，压缩+路由理论**       |
