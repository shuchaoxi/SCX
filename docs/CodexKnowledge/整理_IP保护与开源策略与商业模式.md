# SCX 知识产权保护、开源策略与商业模式

> 整理自 GPT 讨论 (2026-06-26)，综合 IP 保护、开源发布、商业化和组织架构设计。

---

## 一、五层资产模型

将 SCX 资产分为五层，每层采用不同的发表/开源/保留策略：

| 层级 | 内容 | 策略 |
|------|------|------|
| **数学理论** | SCX 定义、状态条件风险、数据价值函数、命题证明 | **发表，完全公开** |
| **算法框架** | pseudocode、核心流程、基本公式 | **发表，完全公开** |
| **最小代码** | toy demo、基础 SCX score、简单 coreset | **开源** |
| **工程实现** | 高性能 pipeline、自动诊断、可视化、工业接口、模型适配器 | **暂不全开源** |
| **数据/模型/专家库** | 高质量 benchmarks、专家势函数库、私有筛选规则、校准参数 | **重点商业资产，严格保留** |

### 做什么
- 论文里把数学定义、命题、伪代码、synthetic 实验全部公开。
- 开源一个轻量 `scx-core`，让别人能复现论文结论。
- 工程实现可以开源部分通用模块，但核心策略、阈值、校准参数保留。

### 不做什么
- 不把所有生产级代码、数据、模型和调参细节一次性放出去。
- 不把工业级 pipeline、商业 GUI、专家库、训练好的高价值模型开源。
- 不把私有校准参数和阈值策略公开。

---

## 二、三层开源策略

### 第一层：论文完全公开

**做什么：**
- 公开 SCX 核心数学定义、状态条件专家风险、数据价值函数、冗余压缩目标、专家路由公式。
- 公开命题与证明、合成实验、小规模真实案例、算法伪代码。
- 目标期刊/会议：Nature Computational Science / npj Digital Medicine / TMLR / JMLR 等。

**目的：** 抢概念、拿引用、建立信誉、获得学术优先权。

**不做什么：**
- 论文里不要公开全部工程细节、自动阈值选择、高性能状态划分策略。
- 不要把大规模工业 pipeline 写进论文补充材料。

---

### 第二层：reference code 开源

**做什么：**
- 开源轻量仓库 `scx-core`，包含：state partition、expert reliability estimation、redundancy compression、noise score、data value score、toy examples。
- 许可证偏宽松（如 MIT / Apache 2.0），方便学术传播。
- 开源 `SCX-Health` 仓库，用 MedMNIST / HAM10000 / CheXpert 做公开 demo。

**目的：** 让别人能复现论文、建立开源社区、吸引合作者、获得公信力。

**不做什么：**
- 不开源工业级数据处理 pipeline。
- 不开源企业级 API、商业 dashboard、自动报告系统。
- 不开源完整 AlGaN/NEP/MACE 专家库和大规模 benchmark 原始数据。

### 第三层：商业版闭源

**SCX-Pro / SCX-Compiler 保留内容：**
- 大规模数据管线
- MLIP expert compiler（能量零点对齐、gauge normalization、domain certificate、conflict arbitration、distilled student）
- LLM data curation 模块
- 企业可视化 dashboard
- 自动报告生成
- 大模型数据筛选模块
- 云 API 和企业私有部署
- 私有 benchmark

**目的：** 服务商业用户，形成付费壁垒。

**不做什么：**
- 不把商业版放在公开仓库。
- 不把企业部署代码在开源协议下发布。

### 核心原则
> **开源到"足以复现论文"，不要开源到"足以替代你的商业产品"。**

---

## 三、IP 保护流程

### 论文发表前必须做的事

正确顺序：

```
内部 invention disclosure → 专利评估 → 问学校/专利代理人
→ 值得就提交申请 → arXiv/投稿 → 选择性开源 → 商业版
```

**做什么：**
1. **写 invention disclosure（内部 2-5 页材料）**：记录 SCX 核心流程、数据压缩、专家路由、状态价值函数、应用场景。这是确权第一步。
2. **找学校知识产权办公室或校外专利代理人评估**：确认哪些有专利价值。
3. **有专利价值就先申请**：至少把关键权利要求占住，再 arXiv/投稿。
4. **论文发表后再开源最小代码**：确保公开披露不破坏新颖性。
5. **最后做商业版**。

**不做什么：**
- 不要先公开完整论文和代码后再想专利——许多司法辖区的宽限期有限，不值得赌。
- 不要在论文/arXiv/代码公开前在朋友圈、报告、PPT 中披露关键技术方案。

### 哪些可以专利？

这些具体技术方案可以申请专利或软著：
- 状态条件数据价值评估系统
- SCX-Compress 冗余压缩流程（具体技术流程）
- 专家可靠性矩阵与数据路由策略
- 高误差状态 acquire/relabel/downweight 策略
- 用于 MLIP/LLM 数据审计的自动报告系统

### 哪些靠论文确权？

这些靠论文建立学术优先权（专利不适合保护纯数学）：
- 数学公式本身
- 抽象思想、框架概念
- 定义、命题、证明

### "防御性公开"策略

不是把全部资产藏起来，而是：
```
论文（确立学术优先权）
+ 选择性开源（建立生态）
+ 闭源增强版（保护商业核心）
```
三者并行，形成 "公开理论，保留产品化能力" 的防御体系。

---

## 四、学校 IP 风险切割

### 主要风险

如果使用学校资源（超算、导师项目、实验室数据），成果可能被认定为职务发明/职务作品。

**高风险：** DFT 数据、AlGaN/MLIP 应用软件、用学校超算产出的结果。
**可切割：** SCX 通用数学框架与一般代码（如果独立开发、使用非学校资源）。

### 做什么

1. **新建私人仓库**：用个人邮箱、个人 GitHub、个人电脑，建立 `scx-core-private`。
2. **开启可验证时间线**：Git commit 全部保留，关键文档生成 SHA-256 哈希，定期做时间戳存证，保留电脑购买记录。
3. **Clean-room 重写**：SCX 通用版重新写一遍，不从旧项目复制粘贴。
4. **写 DEVELOPMENT_LOG.md**：记录开发日期、地点、设备、是否使用学校资源。
5. **把 DFT/AlGaN 和 SCX 分离**：SCX 论文不使用学校 DFT 数据作为核心证据。
6. **查清签过的协议**：入学协议、奖学金协议、课题组管理规定、学校 IP 政策、超算使用协议。

### 不做什么

- 不把 SCX 核心代码上传学校服务器。
- 不在学校超算跑 SCX。
- 不用导师项目数据做 SCX 核心实验。
- 不用课题组网盘备份核心代码。
- 不在课题组群里发完整设计。
- 不把 repo 权限给课题组任何人。
- 不要轻易把导师列为 SCX 数学论文的共同作者（如果导师没有实质参与）。

---

## 五、商业模式

### 四种产品化方向

#### 1. 数据压缩 / 数据去冗余工具（SCX-Compress）
- 用户输入训练数据，输出：保留多少数据、训练误差保持多少、高误差区域不删、边界 anchor 保留、噪声点降权。
- 最直接的商业价值。

#### 2. 专家标注路由工具
- 适用于大模型、科学数据、人类专家、DFT 标注等场景。
- 判断：哪类数据交给哪个 expert、哪类数据必须高精度 oracle、哪类数据不用标（冗余）。
- 服务于 AI 数据公司、材料计算团队、自动驾驶/医疗影像/遥感等领域。

#### 3. MLIP expert compiler
- 最自然的垂直商业入口。
- 输入：多个 ACE/NEP/MACE expert → 能量零点对齐 → gauge normalization → domain certificate → conflict arbitration → distilled student / merged potential。

#### 4. 数据价值审计报告（SCX Data Value Audit Report）
- 交付物包括：数据冗余地图、噪声风险地图、高价值状态地图、专家可靠性矩阵、建议保留/删除/重标注/补数据清单、预计压缩比例、压缩前后模型性能对比、可复现实验脚本。
- 是最容易商业化的形式——企业愿意为"审计能力"买单。

### 五种收费模式

#### 模式 A：赞助研究（Sponsored Research）
- 公司给课题组一笔钱，支持 SCX 在其场景上验证。
- 交付：技术报告、论文合作、内部 demo、数据审计结果。
- 适合博士身份，缺点是学校可能参与管理经费和 IP。

#### 模式 B：产业联盟会员（SCX Consortium）
- 会员公司每年交会费，共同支持 SCX 标准。
- 每家公司私有数据不共享，共同获得工具更新、benchmark、报告模板。
- 最符合"他们任何一个人都不希望我被对方收购"的中立性要求。

#### 模式 C：第三方审计服务
- 公司给数据，你出审计报告。
- 报告包括：Dataset redundancy score、Noise risk score、Valuable state map、Expert reliability matrix、Recommended compression ratio、Recommended relabeling set。
- 最容易商业化的形式。

#### 模式 D：非独占授权
- 把 SCX-Pro 授权给多家公司使用。
- **关键：非独占授权，不卖断，不给某一家独占。**

#### 模式 E：开源核心 + 企业版（Open Core）
- 开源 SCX-Core。
- 收费 SCX-Pro：大规模数据处理、自动报告、多专家模型接口、企业隐私部署、高性能压缩、可视化 dashboard。

### "中立第三方数据价值审计方"的定位

核心定位：
> **SCX 是面向 AI 训练流程的第三方数据价值审计框架。**

不卖"一个公式"，而是卖：
- Data Value Audit / Expert Reliability Audit / Dataset Compression Report
- "帮我减少训练数据量或标注成本，精度基本不掉"

### 与公司谈话术

正确说法：
> 我不做独占外包，也不做单家公司内部工具。我做的是中立的 SCX 数据价值评估标准。贵公司可以作为早期产业合作方，提供资金、场景、工程师参与共建；你们获得优先试用、内部部署和非独占授权，但核心标准和 IP 保持中立，以确保其他公司也能信任这个体系。

更商业的版本：
> SCX 不出售给单一公司。我们提供非独占授权、数据审计、联合 benchmark 和企业部署。所有成员公司都可以使用，但没有一家可以控制标准。

---

## 六、组织架构

### 三层结构

#### 第一层：SCX Research（学术层）

- 负责：论文、数学定义、benchmark、reference implementation、开源核心、学术影响力。
- 挂靠形式：学校、实验室、个人开源项目、非营利式研究组织。
- 控制人：你（scientific founder / chief scientist）。

#### 第二层：SCX Consortium（产业联盟层）

- 成员公司交钱，获得：标准制定参与权、内部试用权、benchmark 访问权、定期技术报告、优先试点机会、非独占企业授权折扣。
- 成员不能获得的：SCX 核心 IP 所有权、独占授权、单方面修改标准的权力、收购后封锁其他成员的权力。

#### 第三层：SCX Operator / SCX-Pro（商业执行层）

- 负责：企业项目交付、数据审计、工程部署、可视化平台、API、客户支持、合同和收费。
- 可由 CEO/COO/项目经理/工程负责人管理，你不需要天天打商业仗。
- 你保留：scientific founder、chief scientist、standards chair、architecture veto、IP owner/licensor。

### 你应控制的四项核心权力

1. **IP 控制权**：SCX 名字、核心框架、代码主仓库、商标、专利/软著。
2. **标准控制权**：什么叫 SCX-compatible、什么叫 SCX-certified，由你定义。
3. **认证控制权**：企业想说"我通过 SCX 数据价值审计"，需要你的体系认证。
4. **方向控制权**：哪些模块进入 core、哪些只是企业插件，你有最终路线权。

### 你不需要控制的

- 每个客户怎么谈
- 每个工程需求怎么排
- 每个 dashboard 怎么做
- 每个部署细节

这些交给运营团队。

---

## 七、与公司合作的注意事项

### 做什么

1. **合同写成 sponsored research / membership / paid pilot**，而不是 equity acquisition / exclusive buyout。
2. **坚持非独占授权，不卖断。**
3. **甲方出人可以，但代码贡献必须受控：**
   - 签 Contributor License Agreement (CLA)。
   - 贡献进入 SCX core 前必须签 CLA。
   - SCX 维护方有最终 merge 权。
   - 贡献不得附带独占限制。
   - 贡献后的 core 仍由 SCX 标准方统一维护。
4. **技术路线你有最终权**：
   - 标准命名权、版本发布权、reference implementation 合并权、benchmark 认证口径、SCX 商标使用权、论文署名与发布权。
   - 公司可以投票建议，但不能控制核心标准。
5. **找可靠的小班子**：运营负责人、工程负责人、学术/算法核心（你+1-2学生）、法务/IP 顾问、商务顾问。

### 不做什么

1. **不签独占**：比如"公司 A 出钱，你把 SCX 在 AI 数据领域独占授权给 A"——这直接毁掉中立性。
2. **不接受"买断式合作开发"**：比如"你帮我们做，成果归我们"。
3. **不让甲方控制论文发表**：合作协议里可以有保密审查期，但不要给甲方无限否决发表的权力。
4. **不让甲方工程师绕过主仓库**：所有核心贡献必须进统一代码库、统一协议、统一 review。
5. **不要私下收大额商业款**：你是博士，学校 IP 和经费合规要处理好。
6. **不要过早卖给一家大公司**：如果早早被收购，其他公司不会再用你的标准。
7. **不要全开源生产级代码**：研究版开源，工业版闭源。

### 如何让甲方出钱出人但不失控

关键设计：
```
公司 A 出钱 + 工程师
公司 B 出钱 + 数据案例
公司 C 出钱 + 应用场景
         ↓
    SCX 中立实验室/标准方
         ↓
统一标准、开源核心、认证报告、商业审计、企业部署
```

你不是给某一家打工，而是让多方围绕你的标准参与。

---

## 八、商业路线图

### 阶段 1：论文确权 + 最小工具（现在）
- SCX 数学论文（arXiv 或投稿）。
- SCX-Core 最小代码开源。
- 一个漂亮 demo（MedMNIST 数据压缩）。
- 一个数据压缩/冗余案例。

### 阶段 2：找 1-2 个甲方做 paid pilot
- 每个 pilot 只做一件事：帮它减少训练数据量或标注成本。
- 交付报告，不承诺全平台。

### 阶段 3：成立 SCX Working Group / Consortium
- 让多个单位加入：公司、高校、材料计算团队、AI 数据团队。
- 收 membership fee 或项目费。

### 阶段 4：找职业经理人
- 你做 scientific founder，别人做 CEO/COO。
- 你保留标准控制权和技术 veto。

### 阶段 5：建立认证体系
- SCX-certified dataset
- SCX-compressed dataset
- SCX expert reliability report
- SCX-compatible data pipeline

### 明确不能做的事

> - 不要一上来找大厂签"所有成果归甲方"的合作。
> - 不要把 SCX 讲成万能 AI，要讲成"状态条件质量判断层"。
> - 不要喊"取代 TCAD/OPC/Calibre"，要说"SCX complements physical solvers by deciding when their outputs are trustworthy"。
> - LLM 可以放 discussion，主战场是高精度标签/仿真数据。
> - 不要一开始写成商业帝国 PPT——先做出第一个"能省 50% 仿真/标注成本且性能不掉"的样板。

---

## 九、论文谱系与发表策略

### 推荐发表顺序

| 顺序 | 论文 | 定位 | 目标期刊 |
|------|------|------|---------|
| 1 | **EGP Paper 1**: ACE gauge-normalized expert merging | 材料势函数方法，根据地（有完整 DFT 数据） | npj Computational Materials / PRM / JCTC |
| 2 | **SCX-Theory**: 数学定义、命题、可识别性边界 | 理论地基，arXiv 占坑 | TMLR / SIMODS / JMLR |
| 3 | **SCX-MLIP**: SCX 理论应用于 MLIP | 理论→应用闭环 | Nature Communications / npj Computational Materials |
| 4 | **SCX-Sim**: 科学与工程仿真多保真调度 | 跨领域大文章，主冲 Nature 系列 | Nature Computational Science |
| 5 | **SCX-Health**: 医学/视觉数据审计 | 开源影响力 + 商业入口 | npj Digital Medicine |

### 每篇的独立性要求

- **EGP Paper 1** 解决 ACE expert 的 gauge/energy 规范化与合并方法。
- **SCX-Theory** 提出状态条件专家性与数据价值的数学定义和可识别性边界。
- **SCX-MLIP** 将 SCX 理论应用回 MLIP 领域，完成理论→应用闭环。
- **SCX-Sim** 把 SCX 发展成高保真科学/工程仿真的多保真调度系统。
- **SCX-Health** 解决医学数据中的标签噪声、长尾、专家复核和冗余压缩。

不要把 SCX 当成一个方法拆成很多应用论文；要把 SCX 当成一个理论母体，每篇论文解决一个不同层级的问题。
