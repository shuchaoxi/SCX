# SCX 论文框架 TODO

> 创建日期：2026-06-26
> 基于：五审查员综合报告
> 关联文件：[[论文框架审查报告_五审查员综合]]

---

## 阶段 0：立即止损（本周）

### 0.1 EGP Paper 1 内容收窄

- [ ] **移除 EGP Paper 1 中的 SCX 噪声检测 Figs (Fig 4-8)**
  - 这些图（SCX 噪声分布、一层 vs 两层 F1、fmax vs error、综合力 RMSE、雷达图）属于 SCX-MLIP
  - EGP P1 只保留：EOS 对比、弹性常数对比、Per-batch 误差对比、Gauge violation 对比
  - 参考：`G:\Xiaogan_Supercomputing_data\SCX\paper\paper1_mlip\FIGURES_ANALYSIS.md`
- [ ] **移除 EGP P1 中所有 SCX 理论提及**
  - 不在正文中讨论"状态条件专家可靠性"
  - Discussion 末尾最多一句话："Whether expert reliability is inherently state-conditioned remains an open question for future work"
- [ ] **确认 EGP P1 的独立贡献叙事**
  - 只 claim：gauge-fixed shared+correction ACE 参数化
  - 不 claim：新的 MoE runtime、element correction 原子能、AlGaN 可转移

### 0.2 SCX 理论加固

- [ ] **删除 Arrow 不可能定理类比**（`theory/propositions/01_global_ranking_insufficiency.md` Section 4）
- [ ] **重构 Proposition 1**
  - 从"不存在全局最优专家"改为"全局排序的遗憾下界为 Ω(p·δ_min)"
  - 给出可检验的共单调性条件（已有推论草稿，需正式化）
- [ ] **添加不可识别性定理草稿**
  - 显式陈述：无额外假设时，噪声与可学习困难不能仅从 (x,y) 识别
  - 放在 Prop 2 旁边，作为理论边界

---

## 阶段 1：EGP Paper 1 收尾（1-2 周）

### 1.1 写作

- [ ] **写完 Introduction**
  - 锚定问题：多元素 ACE 势函数合并时 gauge 不一致导致势能面不连续
  - 文献回顾：ACE 框架 (Drautz 2019, Lysogorskiy 2021)，PACE，已有 merging 尝试
  - 贡献陈述：shared+correction 参数化 + coefficient-level post-hoc gauge fixing
- [ ] **写完 Methods**
  - 2.1: Shared+Correction ACE Architecture (E = Σ[c₀ᵀB + c_ZᵀB + b_Z])
  - 2.2: Gauge Freedom (c₀→c₀+d, c_Z→c_Z-d 不变性)
  - 2.3: Post-hoc Projection (g = Σπ_Z c_Z; c_Z' = c_Z - g; c₀' = c₀ + g)
  - 2.4: Why Soft Constraint Fails (梯度竞争分析：loss 范比 79%→5.6%，精度崩溃)
  - 2.5: Training Protocol (AlN v3: Pacemaker baseline → Model A ablation → Model B design matrix → constrained ridge → export PACE)
- [ ] **写完 Results: AlN v3**
  - 3.1: EOS (V₀, B₀ vs DFT ref 10.64/192.6)
  - 3.2: Elastic Constants (C₁₁-C₆₆ 对比表)
  - 3.3: Phonon Forces (声子力 RMSE 0.00793→0.00580, -27%)
  - 3.4: Gauge Violation (8.77→4.6×10⁻¹⁶, soft constraint 失败 vs post-hoc 成功)
  - 3.5: Surface/Defect Transferability
- [ ] **写完 Discussion + Conclusion**
- [ ] **制作最终 Figures**（EOS curve, elastic bar chart, gauge violation comparison）

### 1.2 实验补充（可选，取决于 GaN/AlN v4 进度）

- [ ] **检查 GaN/AlN v4 超算任务状态**
  - `python .hpc/hpcmgr.py list`
  - `python .hpc/hpcmgr.py logs <job_id>`
- [ ] **如果 v4 已完成**：补充 GaN/AlN v4 的 Model B 训练 + gauge fix + 对比
- [ ] **如果 v4 未完成**：EGP P1 先以 AlN v3 单系统投出，v4 结果作为 revision 补充

### 1.3 投稿准备

- [ ] **选择目标期刊**：npj Computational Materials（首选）/ PRM（备选）/ JCTC（备选）
- [ ] **准备 SI（Supporting Information）**
- [ ] **准备 Cover Letter**
- [ ] **arXiv 上传**

---

## 阶段 2：P0 实验 — 重训验证（本周，不可跳过）⭐

### 2.1 AlN v3 去噪重训

- [ ] **准备去噪数据集**
  - 方案 A：移除 fmax > 5 eV/Å 的 74 帧（保守）
  - 方案 B：移除 SCX 两层 Top-2 噪声状态（约 90-131 帧）
  - 方案 C：移除 fmax > 10 eV/Å 的 14 帧 + 降权 fmax 5-10 eV/Å 的 60 帧
  - 推荐先做方案 A（最简单，审稿人最容易理解）
- [ ] **训练对照组**
  - (a) Clean baseline: 去噪后数据训练 Single ACE
  - (b) Original baseline: 全部 534 帧训练 Single ACE（已有）
  - (c) Random drop: 随机去除 74 帧，训练 Single ACE
  - (d) Loss-based drop: 去除训练 loss 最高的 74 帧，训练 Single ACE
- [ ] **评测**
  - 在同一个 103 帧测试集上测力 RMSE、能量 RMSE
  - 报告 (a) vs (b) 的改善幅度（实测值，不是预估值！）
  - 展示 SCX 指导的 drop (a) 显著优于 random drop (c) 和 loss-based drop (d)
- [ ] **更新 FIGURES_ANALYSIS.md 的 Fig 7**
  - 用实测值替换"SCX-ACE（预估）"柱

### 2.2 重训后叙事更新

- [ ] **根据实测结果确定 claim 级别**
  - 如果力 RMSE 降 >15%：可以 claim "SCX improves model performance" (L2)
  - 如果力 RMSE 降 5-15%：claim "SCX identifies data quality issues that affect model performance" (L1+)
  - 如果力 RMSE 降 <5%：claim "SCX is a diagnostic tool for data quality auditing" (L1)
  - 如果力 RMSE 没降甚至升了：需要重新审视 SCX 的噪声检测逻辑

---

## 阶段 3：SCX-MLIP 论文准备（2-4 周）

### 3.1 理论部分（精简到 ~3 页正文）

- [ ] **写 Core Definitions 节**
  - R_m(s) = E[ℓ(f_m(x), f*(x)) | x∈s]
  - SCX_m(s) = P(ℓ < τ | x∈s)
  - 数据四分类：Valuable / Noisy / Redundant / Expert-dependent
  - 不包含 V(s) 乘法分解（用四分类规则替代）
- [ ] **写 Three Propositions 节（重构版）**
  - Prop 1：全局排序的遗憾下界（含共单调性可检验条件）
  - Prop 2：噪声下 error-driven sampling 次优性 + 不可识别性定理
  - Prop 3：状态条件权重优势（Jensen + 塔性质证明）
- [ ] **写 State Discovery 节**
  - 两层架构：L1 域知识 + L2 ErrorDrivenEncoder
  - 最优粒度：Silhouette + 风险同质性联合优化
  - 状态发现作为 oracle（ErrorDrivenEncoder 是实例化，细节放附录）
- [ ] **写冷启动协议**（可放附录）
  - 第一阶段：无标签代理（expert disagreement, model uncertainty, self-consistency）
  - 第二阶段：acquisition
  - 收敛条件

### 3.2 实验部分

- [ ] **AlN v3 两层状态发现**（已有，整理成论文格式）
  - Table: 一层 vs 两层 F1 (th=2.0/3.0/4.0/5.0)
  - Table: Top-K 噪声捕获率
  - Figure: 50% megastate 被分解为 6 个误差特征不同的子状态
  - Figure: Phonon 100% 落入同一低误差状态
- [ ] **AlN v3 去噪重训**（P0 完成后纳入）
  - Figure: 力 RMSE 实测对比（Clean vs Original vs Random vs Loss-based）
  - Figure: fmax vs test error scatter (r=0.966)
- [ ] **跨材料验证**（P1）
  - 下载 Si、Cu、MgO 公开 ACE 训练数据
  - 运行 SCX 两层分析
  - 报告每个系统的噪声/冗余发现
  - 目标：展示 SCX 不只在 AlN 上有效
- [ ] **合成实验**（P1）
  - 已知噪声结构 → SCX 恢复状态结构的能力
  - 不可识别性定理的数值演示

### 3.3 竞争对比

- [ ] **与 loss-based sampling 对比**（包含在重训实验中）
- [ ] **与 random sampling 对比**（包含在重训实验中）
- [ ] **（可选）与 active learning 方法对比**（如 BADGE, uncertainty sampling）
  - 仅当重训结果非常好且想冲高影响力期刊时做

### 3.4 写作与投稿

- [ ] **写 Introduction**
  - 锚定：MLIP 数据贵但价值不均 → EGP P1 的 9.7× per-batch 差异 → 需要一个状态条件框架
  - 不泛化到"通用框架"——收窄到 "methodology for MLIP data quality"
- [ ] **写 Methods: SCX Pipeline for MLIP**
- [ ] **写 Discussion**
  - SCX 是数据诊断工具，与模型架构改进互补
  - 拓展潜力（一句话提 Sim/Health，不展开）
  - 局限：冷启动需要初始标签; 状态粒度敏感
- [ ] **内部审查 → 修改 → arXiv → 投稿**

---

## 阶段 4：跨领域扩展（SCX-MLIP 投稿后）

### 4.1 选择主攻领域

- [ ] **评估 SCX-Sim 可行性**
  - 是否有产业合作方数据？
  - 是否能用公开仿真 benchmark？
  - 如果 YES → 优先 SCX-Sim（Nature Computational Science 目标）
- [ ] **评估 SCX-Health 可行性**
  - MedMNIST 实验 GPU 升级后是否有效？
  - 是否有临床合作方？
  - 如果 Sim 不可行 → 做 Health

### 4.2 领域深挖

- [ ] **选定的领域内，做出与 AlN v3 可比证据强度的实验结果**
- [ ] **写第三篇论文**

---

## 阶段 5：长期（论文系列完成后）

### 5.1 理论完善

- [ ] 将 SCX 形式化为完整的统计学习理论论文（如果 SCX-MLIP 反响好）
- [ ] V(s) 从信息增益第一性原理推导（如果找到合适的数学框架）

### 5.2 开源

- [ ] 开源 `scx-research/` 代码（"足以复现论文"级别）
- [ ] 发布 2-3 个 SCX-cleaned 公开数据集（MPTraj 子集、ColabFit 的 AlN/GaN 等）

### 5.3 商业

- [ ] 基于 SCX-Pro 的商业授权/合作谈判
- [ ] SCX Consortium 产业联盟（远期）

---

## 优先级总览

```
本周必做 ████████████████████ P0
████ 阶段 0: 止损（EGP P1 收窄 + 理论加固）
████ 阶段 2: AlN v3 去噪重训（4-8h 计算）

两周内 ████████████████████ P1
████ 阶段 1: EGP P1 写完 + 投稿
████ 阶段 2: 公开 MLIP 数据集分析

一月内 ████████████████████ P2
████ 阶段 3: SCX-MLIP 论文完成

投稿后 ████████████████████ P3
████ 阶段 4: 跨领域扩展（Sim 或 Health 二选一）
```

---

## 关键决策记录

| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-06-26 | SCX-Theory 不与 SCX-MLIP 分开投稿 | 五审查员全票：独立理论论文被攻击风险极高，且 EGP P1 的保护不传导到不同审稿人 |
| 2026-06-26 | 理论部分收窄到 1/3 篇幅 | 核心期刊审稿人更看重实验验证，长理论会稀释实验贡献的冲击力 |
| 2026-06-26 | EGP P1 不包含 SCX 噪声检测 | 避免审稿人混淆两篇论文的贡献边界 |
| 2026-06-26 | 七领域收窄到 MLIP + 最多一个 | 当前 MedMNIST/CIFAR 实验质量不足以支撑通用性 claim |

---

*关联文件：[[论文框架审查报告_五审查员综合]]*
