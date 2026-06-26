# SCX 在 LLM 大模型方向的战略与发展路线图

> 基于 2026-06-26 与 GPT 的深度讨论整理
> 整理日期：2026-06-26

---

## 一、LLM 对 SCX 为什么重要

### 1.1 GPT 的核心论证：LLM 数据筛选是 SCX 的"远期外延"

GPT 多次强调一个核心判断：

> **SCX 在 ACE/MLIP 上已经有了强 prototype，这给了你很强的动机去往 LLM 扩展，但 ACE 成功不等于 LLM 会自动成功。**

ACE/MLIP 成功的原因是：
- 有明确的 DFT oracle（gold label）
- 物理 descriptor 状态空间天然有意义
- 冗余非常明显（AIMD 相邻帧相似）
- 物理有约束（能量守恒、连续性）

而 LLM 场景会遇到四个新难题：
1. **表示空间不等于价值空间**：embedding 相近的两条文本，训练价值可能完全不同
2. **误差难以定义**：LLM 数据没有绝对 gold label，只能用代理量（loss、perplexity、model disagreement 等）
3. **数据价值不是局部可加的**：一条数据的价值依赖已有数据集和当前模型
4. **冗余不能只靠相似度判断**：LLM 中"看起来重复"的数据可能增强鲁棒性

### 1.2 市场大小对比：材料 vs LLM

| 维度 | 材料/MLIP | LLM 数据 |
|------|-----------|----------|
| 市场规模 | 较小（学术+材料公司） | 巨大（所有 AI 公司） |
| 竞争强度 | 低（SCX 是原创方向） | 极高（大厂+学术都在做） |
| SCX 优势 | 强（有 DFT oracle + 物理描述符） | 弱（标签模糊、误差不可定义） |
| 商业化难度 | 中等（需要行业合作） | 极高（大厂内部化） |

GPT 的最终判断：**SCX 不适合正面切入通用 LLM 数据评价，但适合作为远期外延和论文 discussion。**

### 1.3 SCX 在 LLM 数据筛选中的独特优势

SCX 在 LLM 场景的合理定位不是"又一个更准的 judge"，而是：

> **状态条件的 judge 可靠性校准系统 / 评价器编排框架。**

具体来说，SCX 可以补的是：
1. **不同 judge 在不同状态下的可靠性评估**：强 GPT 也不是所有状态都强，数学强不一定医学强
2. **高分数据的真实边际价值判断**：GPT 喜欢"漂亮但重复"的数据，SCX 加入冗余项
3. **低分数据的训练价值识别**：覆盖模型薄弱状态的数据可能更值钱
4. **评价器成本感知调度**：不同状态切换使用不同评价器，控制成本

---

## 二、LLM 实验需求

### 2.1 为什么要做 LLM 实验

要说服审稿人和客户，SCX 在 LLM 数据筛选上有效，必须有一个最小可行实验。

但 GPT 强调：**LLM 实验不能作为 SCX 的核心实验主战场。** LLM 只能作为 discussion/extension，核心实验应该在 ACE/MLIP 和医学图像上。

### 2.2 最小可行 LLM demo

| 项目 | 规格 |
|------|------|
| 模型 | 0.5B-3B 小模型 + LoRA 微调 |
| 数据 | 公开 instruction dataset（几千到几万条） |
| 硬件 | 单张 4090 足够 |

**SCX 表示**：sentence embedding 或模型 hidden states

**误差代理**：初始模型 loss 或多模型 disagreement

### 2.3 实验设计

**冗余判断公式：**
```
Redundancy(s) = [1 - mean_r(s)] * density(s) * similarity(s)
```

**数据压缩策略：**
- 保留高误差高密度状态
- 保留边界状态
- 每个冗余状态保留 medoid
- 设置随机/多样性对照组

**验证对比：**
- full data（100%）
- random 20%
- diversity 20%
- high-loss 20%
- SCX 20%

**目标：** SCX 20% 接近 full data 效果，或优于 random/diversity

### 2.4 具体技术路线

**实验 A：冗余压缩**
1. 训练基础模型，提取 embedding
2. 计算 loss 作为残差
3. 聚类形成状态
4. 对每个状态计算冗余分数
5. 只保留代表样本，加权训练
6. 对比 full data / random / uncertainty / coreset

**实验 B：高误差不等于高价值**
1. 人为加入 label noise
2. 比较 high-loss sampling、uncertainty sampling、SCX state-wise acquisition
3. 证明 SCX 优先选高密度、一致、可学习的高误差状态（而非噪声点）

**实验 C：专家路由**
1. 训练多个不同能力的 judge/expert
2. 估计每个 expert 在不同状态上的可靠性
3. 路由决策：为每个样本选择最可靠且成本最优的 judge

---

## 三、发展路线图（时间线）

### 阶段 1：当前（0-2 月）—— 立住根

**关键里程碑：**
- [ ] 完成 SCX-MLIP 论文（gauge-normalized expert potentials + residual-state map）
- [ ] 新建私人 SCX 仓库，clean-room 重写代码
- [ ] 完成 DEVELOPMENT_LOG.md，建立证据隔离
- [ ] 查 IP 协议，做专利评估
- [ ] 用 MedMNIST 跑通第一个 SCX-Compress demo
- [ ] 用最小 instruction dataset 跑通第一个 LLM 小实验（验证趋势，不追求大规模）

**目标：** 证明 SCX 不是 PPT，在 ACE/MLIP 上有强原型

### 阶段 2：1-2 月 —— 建理论地基

**关键里程碑：**
- [ ] arXiv 发布 SCX-Theory（数学定义 + 可识别性边界 + 合成实验）
- [ ] 抢占命名权：State-Conditioned eXpertise
- [ ] 完成 SCX-Core 开源（轻量版，做到"足以复现论文，不足以替代产品"）
- [ ] 跑通 HAM10000/CheXpert 医学图像实验
- [ ] 完成 LLM 小规模 SFT 验证实验（证明 SCX 选择的 20% 数据趋势有效）
- [ ] 校外资 IP 律师咨询

**目标：** 建立 SCX 的概念占位和理论地基，LLM 作为 discussion/extension

### 阶段 3：3-6 月 —— 攻大论文

**关键里程碑：**
- [ ] 完成 SCX-Sim 大论文（DFT/MLIP + FEM/PDE + 医学图像 + OPC/TCAD toy）
- [ ] 目标期刊：Nature Computational Science / Nature Communications
- [ ] 找 1-2 个甲方做 paid pilot
- [ ] 完成 SCX-Health 开源框架
- [ ] 构建 SCX Potential Compiler 原型（ACE + NEP + MACE + DeepMD 多专家蒸馏）
- [ ] 完善 LLM 实验：在更大 SFT 数据集上验证 SCX routing 的性价比

**目标：** 证明 SCX 是跨领域的科学/工程仿真数据价值评估框架；LLM 数据评价的论文讨论充分展开

### 阶段 4：6-12 月 —— 商业化落地

**关键里程碑：**
- [ ] 成立 SCX Working Group / Consortium（多公司参与）
- [ ] 建立 SCX 认证体系雏形（SCX-certified dataset 等）
- [ ] 找 CEO/COO，自己退到 scientific founder 角色
- [ ] 将 LLM 方向的 SCX-Judge 作为企业版功能模块（本地部署 + 数据审计报告）
- [ ] 正式接触华为（健康/昇腾生态）、小米（可穿戴/IoT）、半导体（国产 TCAD/CMP）
- [ ] 将 "SCX 评价器编排系统" 包装为企业可购买的数据审计服务

**目标：** 从学术论文走向产业标准

### LLM 方向在整个路线图中的位置

```
阶段 1: LLM 小实验（验证趋势）
      ↓
阶段 2: LLM 嵌入 SCX-Theory（作为讨论/extension）
      ↓
阶段 3: LLM 实验完善（作为 SCX-Sim 的一个外延验证）
      ↓
阶段 4: SCX-Judge 模块商业化（企业版功能）
```

**核心原则：LLM 是远期外延，不是主战场。**

---

## 四、资源配置

### 4.1 人力需求

| 角色 | 必要性 | 来源建议 |
|------|--------|----------|
| 你自己（学术/算法核心） | 必须 | SCX 理论+核心代码 |
| 1-2 名学生/合作者 | 需要 | 协助实验和代码 |
| 运营负责人 | 阶段 2-3 需要 | 管合同、客户、项目排期 |
| 工程负责人 | 阶段 3-4 需要 | 管平台、部署、CLI 工具 |
| 法务/IP 顾问 | 优先找 | 管专利、许可、CLA、合作协议 |
| 商务顾问/产业导师 | 阶段 3 需要 | 帮你找甲方，不被甲方牵着走 |

### 4.2 算力需求

| 实验类型 | 最低配置 | 推荐配置 |
|---------|----------|----------|
| MedMNIST / 小型图像实验 | 笔记本 CPU | 4090 |
| ACE/MLIP 势函数 | 单卡 4090 | 单卡 4090 |
| LLM 最小实验（0.5B-3B + LoRA） | 单卡 4090（24GB） | 单卡 4090 |
| 更大规模 LLM SFT | 单卡 4090（可跑 7B 量级） | A100/多卡 |
| SCX-Potential Compiler | 单卡 4090 | 多卡并行 |
| 工业级大规模 pipeline | - | 需要集群 |

**结论：4090 可以跑通全部学术版 demo，包括 LLM 最小实验。短期不需要追加算力投资。**

### 4.3 资金需求估算

| 阶段 | 主要支出 | 预算估算 |
|------|----------|----------|
| 阶段 1（0-2月） | 校外 IP 律师（1次咨询）、论文投稿费 | ~0.5-1 万 |
| 阶段 2（1-2月） | arXiv 费用、开源仓库托管、律师持续咨询 | ~1-2 万 |
| 阶段 3（3-6月） | Nature 系列 OA 版面费（~2-4 万人民币）、vaspkit/软件许可、合作差旅 | ~5-10 万 |
| 阶段 4（6-12月） | 运营/工程人力、AWS/超算、法务、商务、公司注册 | ~20-50 万 |

**资金来源建议：**
1. 阶段 1-2：个人资金 + 课题组经费（如果切割清楚）
2. 阶段 3：paid pilot 收入 + 赞助研究
3. 阶段 4：membership fee + 企业版授权 + 可能的小规模种子轮

---

## 五、优先级决策

### 5.1 现在必须做（高优先级）

1. **SCX-MLIP 论文**：这是你已有的最强资产，优先出
2. **证据隔离**：新建私人仓库、clean-room 写代码、写 DEVELOPMENT_LOG.md
3. **IP 保护**：查协议、问律师、考虑专利/软著/时间戳
4. **SCX-Core 最小实现**：核心数学 + 合成数据 demo
5. **MedMNIST 跑通**：用公开医学数据做第一个外部验证
6. **最小 LLM 实验**：用 0.5B-3B 模型 + LoRA 验证趋势

### 5.2 可以等论文发表后

- 完整开源 SCX-Health
- 找甲方做 paid pilot
- 建立产业联盟
- 正式公司化
- 大规模 LLM 数据评价实验

### 5.3 需要合作者/资金后

- TCAD/OPC/CMP 工业数据实验（需要行业合作）
- 多中心临床医学验证（需要医院合作）
- 华为/小米可穿戴数据试点（需要企业协议）
- 分布式大规模 SCX 计算平台（需要算力投资）

### 5.4 对 LLM 的精力分配建议

GPT 的原始建议值得全文引用：

> **"大模型不适合做你的主战场。大模型是远期外延，不是核心根据地。"**
>
> **"大模型数据评价已经被大厂内部化；你一个博士硬冲很难。"**
>
> **"SCX 在 LLM 上的合理切口：不是造主任医师，而是造医院的分诊、会诊、质控和病历审计系统。"**

具体来说：

| LLM 方向 | 该花多少精力 | 原因 |
|----------|-------------|------|
| SCX-Theory 中讨论 LLM 作为外延 | 5% | 论文需要提及，但不展开 |
| 最小 LLM 实验验证趋势 | 10% | 有比没有好，但不作为核心证据 |
| LLM-as-Judge 可靠性校准论文 | 15% | 如果有余力可以单独发短文 |
| 通用 LLM 数据评价平台 | 不投入 | 大厂内部在做，很难差异化 |
| 垂直领域 LLM 数据审计（法律/医学/科学） | 20% | 大厂不愿意细做的领域，有空间 |

**最终结论：把 70% 精力放在 SCX-MLIP + SCX-Theory + SCX-Sim 三条主线上，20% 放在医学/视觉开源，10% 放在 LLM 外延验证。**

---

## 六、SCX 在 LLM 的竞争分析

### 6.1 现有 9 类主流方法

| 方法 | 核心思想 | SCX 的关系 |
|------|----------|------------|
| 规则清洗（FineWeb） | 启发式过滤垃圾 | SCX 可以补充状态条件质量判断 |
| 质量分类器（FinerWeb） | 强模型标一小批，训练轻量分类器 | SCX 可加"状态条件"：Q(x|s) |
| Perplexity/Loss（Rho-1） | 用 loss 判断 token 价值 | SCX 可上升到 state-level selection |
| 目标分布匹配（DSIR） | 选最像目标分布的数据 | SCX 可扩展为状态条件 DSIR |
| Influence/Gradient（LoGra/LESS） | 看数据对目标 loss 的贡献 | 计算贵，SCX 可在高价值状态上调用 |
| LLM-as-a-Judge | 用强模型评价 | SCX 做 judge 可靠性校准 |
| 多样性/去重 | 避免重复数据 | SCX 集成到价值公式 V(x)=Q*(1-D) |
| 可验证任务（数学/代码） | 用标准答案验证 | SCX 设为高可靠专家 |
| Benchmark-driven（DataComp-LM） | 最终看训练效果 | SCX 的闭环验证 |

### 6.2 SCX 的框架优势

现有方法大多是**单信号或单阶段**，而 SCX 回答的是：

> **在当前状态 (s)、当前模型 (M)、当前数据集 (D)、可用评价器集合 (J) 下，这个样本应该采取什么动作？**

动作不是只有 keep/drop，而是：
```
keep | drop | downweight | deduplicate | relabel
| route to stronger judge | verify with tool
| use for SFT | use for preference data | use for eval
```

核心公式：
```
Q_SCX(x) = sum_j w_j(s(x)) * Q_j(x)

其中 w_j(s) ∝ exp(alpha * A_j(s) - lambda * C_j)

- Q_j(x): 第 j 个评价器的分数
- A_j(s): 该评价器在状态 s 上的可靠性
- C_j: 评价成本
```

### 6.3 不要正面硬刚的 Statement

> ~~我提出一个更准的数据质量算法。~~

应该说：
> **我提出一个状态条件的数据质量评价编排框架。它把 LLM judge、reward model、verifier、influence score、loss dynamics、dedup、target-distribution matching 统一到同一个决策系统里，并学习每个评价器在不同数据状态下的可靠性。**

---

## 七、风险与注意事项

### 7.1 LLM 方向的主要风险

1. **被大厂平替的风险**：通用 LLM 数据评价大厂都在做，差异化很难
2. **证明成本高**：LLM 数据价值需要大规模训练实验验证，小实验说服力有限
3. **标签模糊**：没有 gold label，SCX 只能输出弱判断（noise-risk 而非 noise）
4. **Goodhart 问题**：企业可能优化数据迎合 SCX 评分而非真正提升模型

### 7.2 与其他方向的资源冲突

LLM 方向投入过多会影响主战场（MLIP、FEM、医学）。**必须控制 LLM 方向不超过总精力的 10-15%。**

### 7.3 关键建议

1. **不要为了 LLM 放弃 ACE/MLIP**——那是你最有原创证据链的地方
2. **不要声称"替代大厂 judge"**——要说"补充和校准"
3. **LLM 实验只做趋势验证**——不要追求大规模，小数据集跑通即可
4. **垂直领域优先**——法律、材料科学、医学问答等 SCX-MedJudge/SCX-STEMJudge 比通用 LLM judge 更有空间
5. **先有根据地，再谈外延**——SCX-MLIP 和 SCX-Theory 出不来，LLM 方向没有根基

---

## 八、核心行动清单（Next Actions）

### 本周
- [ ] 新建私人 SCX 仓库（个人邮箱、个人电脑）
- [ ] 写 DEVELOPMENT_LOG.md 第一版
- [ ] 查入学/助研协议和学校 IP 政策
- [ ] 定 SCX-MLIP 论文框架

### 本月
- [ ] clean-room 写 SCX-Core 代码
- [ ] MedMNIST 跑通第一个 SCX-Compress 实验
- [ ] 用 0.5B-3B 模型 + LoRA 跑通最小 LLM 实验
- [ ] 联系校外 IP 律师

### 下月
- [ ] arXiv SCX-Theory 草稿
- [ ] 开源 SCX-Core（轻量版）
- [ ] 完成 HAM10000 实验
- [ ] 论文投出 SCX-MLIP

### 季度目标
- [ ] SCX-Sim 大论文成型
- [ ] 跑通 FEM/PDE toy demo
- [ ] 完成 SCX-Health 开源框架
- [ ] LLM 方向论文讨论/extension 写完
- [ ] 开始接触早期甲方（材料/医学方向优先）

---

> **一句话总结：SCX 在 LLM 方向有框架优势，但不应作为主战场。用 10% 精力做 LLM 外延验证，70% 精力做 MLIP+Theory+Sim 主线，20% 做医学开源。先有根据地，再谈大模型。**
