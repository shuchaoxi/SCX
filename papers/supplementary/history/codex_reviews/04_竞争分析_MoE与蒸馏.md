\section{SCX/EGP 竞争分析报告：MoE
架构、蒸馏与专家治理}<!-- label: scxegp-ux7adeux4e89ux5206ux6790ux62a5ux544amoe-ux67b6ux6784ux84b8ux998fux4e0eux4e13ux5bb6ux6cbbux7406 -->

> 生成时间：2026-06-25
> 
> 覆盖范围：2023-2026 年最新文献，涵盖 Mixture-of-Experts (MoE)、Knowledge
> Distillation (KD)、模型合并、MLIP gauge 对齐，以及专家治理（Expert
> Governance）四大方向。
> 
> 目标：评估每一项工作与 SCX/EGP 框架的关系，定位 SCX/EGP
> 的差异化优势及未被占领的技术空白。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 目录<!-- label: ux76eeux5f55 -->

1. 
2. 
3. 
4. 
5. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{A. Mixture of Experts (MoE) in
MLIP}<!-- label: a.-mixture-of-experts-moe-in-mlip -->

\subsubsection{A1. DeepMD MoE/MoLE --- ``Scaling MLIP with Mixtures of
Experts''}<!-- label: a1.-deepmd-moemole-scaling-mlip-with-mixtures-of-experts -->

**论文：** Liu, Zhang, Peng, E, Zhang, Wang. ``Scaling Machine
Learning Interatomic Potentials with Mixtures of Experts.''
arXiv:2603.07977 (2026).

**他们解决了什么？** 将 MoE 架构系统性地引入 MLIP 领域。此前 MoE 在
NLP 和 CV 中已取得巨大成功，但面向原子间势函数的 MoE
架构设计（路由策略、专家结构、稀疏激活）缺乏系统研究。

**核心方法：** -
提出了两种架构变体：**MoLE（Mixture-of-Linear-Experts）** 和
**MoE（非线性 MLP 专家）**。 -
设计三种路由策略对比：**逐元素路由**（element-wise routing）
vs.~构型级路由（configuration-level routing） vs.~全局 MoE 路由。 -
引入**共享专家（shared expert）** 机制增强泛化。 - 经由 DeepMD-kit
框架实现，基于 DP 模型架构扩展。

**关键发现：** - **逐元素路由（E(3) equivariant
routing）显著优于构型级路由**，全局 MoE 路由常导致数值不稳定。 - 非线性
MoE + 共享专家组合效果最优，超越 MoLE。 -
路由模式呈现**化学可解释的专家分工**：不同专家倾向于处理特定元素族（与周期表趋势一致）。
- 在 OMol25、OMat24、OC20M 基准上达到 SOTA。

**与 SCX/EGP 的关系：** - **强相关。** DeepMD MoE 是目前与
SCX/EGP 最直接的竞争方法。 - 二者都使用 MoE
思想来提升势函数精度。区别在于：DeepMD MoE 在**训练时**构建 MoE
架构（端到端训练一个模型），而 SCX/EGP
是**后训练**方式------将多个独立训练的专家模型编译为联合系统。 -
DeepMD MoE 的专家是在训练中自动形成的（emergent expertise），而 SCX/EGP
的专家是独立训练的（pre-defined expertise）。

**SCX 相对优势：** - **灵活性：** SCX/EGP
可以组合任意来源的独立训练模型（不同架构、不同训练集、不同超参数），而
DeepMD MoE 所有专家必须在同一框架下端到端训练。 - **可扩展性：**
EGP 的专家可以是异构的（MACE + NEP + SevenNet），DeepMD MoE
的所有专家必须是同构的 DP 架构。 - **增量更新：** EGP
可以随时加入新模型而无需重训，DeepMD MoE 需要整体重训。

**空白填补机会：** - DeepMD MoE
未讨论**专家选择的可解释性**------SCX/EGP
的输入条件路由可以明确解释''对给定结构，为何选择某专家''。 - DeepMD MoE
没有蒸馏流程------SCX/EGP 的蒸馏环节可与 MoE 结合形成''MoE 预编译 +
蒸馏''流水线。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{A2. Allegro/NequIP MoE --- Spatial Partition +
Co-training
Agreement}<!-- label: a2.-allegronequip-moe-spatial-partition-co-training-agreement -->

**论文：** Nascimento et al.~``Mixture of Experts Framework in
Machine Learning Interatomic Potentials for Atomistic Simulations.''
arXiv:2604.26143 (2026).

**他们解决了什么？** 解决了**空间分区 MoE**
中的关键问题：不同复杂度模型在界面处的力学失配（artificial stress
fields），以及高频模型在局部区域带来的计算瓶颈。

**核心方法：** - 基于 E(3)-equivariant **Allegro**
架构构建多保真 MoE 框架。 - **空间分区（Spatial Partitioning）：**
将模拟域分为化学复杂区域（如催化反应界面）和简单区域（如体相晶格），分配不同保真度的模型。
- **协同训练（Co-training）：**
损失函数包含**一致性约束（agreement
constraints）**------对共享体相环境的逐原子能量和力差异施加惩罚，迫使不同专家学习一致的体相物理描述。
- 验证体系：Pt+CO 催化系统。

**结果：** - 精确能量守恒（exact energy conservation maintained） -
体相力学响应（EOS、体模量）在专家间对齐 - 预测精度与全高保真模拟相当 -
**计算速度提升超过 2 倍**

**与 SCX/EGP 的关系：** - **互补关系。**
该工作解决的是**空间分区**问题（不同区域用不同模型），SCX/EGP
解决的是**输入条件路由**问题（不同条件用不同模型）。 -
二者的共识在于：**单一模型不足以覆盖所有场景**，需要多个专家协作。
- 该工作的''一致性约束''思想与 SCX/EGP 的''Gauge
对称化''有关联------都试图使多个模型在重叠区域保持一致预测。

**SCX 相对优势：** - SCX/EGP
不依赖空间分区假设，因此适用于**非局域问题**（如长程相互作用、全局结构变化），而空间分区
MoE 仅适用于可划分的体系。 - SCX/EGP
的专家数量不受空间维度限制，可扩展到任意多专家。

**空白填补机会：** -
该工作的''一致性约束''需要通过额外训练来实现；SCX/EGP
可以在**不重训**的情况下实现专家间一致性（通过校准层的后处理）。 -
空间分区与输入条件路由可以结合------例如在界面上同时使用两种策略。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{A3. 通用 MoE --- Shazeer et al.~2017, Switch
Transformer}<!-- label: a3.-ux901aux7528-moe-shazeer-et-al.-2017-switch-transformer -->

**论文：** - Shazeer et al.~``Outrageously Large Neural Networks:
The Sparsely-Gated Mixture-of-Experts Layer.'' ICLR 2017. - Fedus, Zoph
\& Shazeer. ``Switch Transformers: Scaling to Trillion Parameter Models
with Simple and Efficient Sparsity.'' JMLR 2022.

**他们解决了什么？** Shazeer 2017 提出了**稀疏门控 MoE
层**的核心架构：通过一个可学习的门控网络将每个输入路由到 top-k
个专家（子网络），实现''总参数量巨大但计算量恒定''的效果。Switch
Transformer 将其简化为 top-1 路由，显著降低了通信和计算开销。

**核心方法：** - **Noisy Top-K Gating：** 在门控 logits
上加噪声后取 top-k，实现稀疏激活。 - **辅助负载均衡损失（Switch
Transformer）：**
通过不同化的负载均衡损失避免''富者愈富''（少数专家支配大部分输入）问题。
- **容量因子（Capacity Factor）：** 控制每个专家处理的 token
数上限。 - **训练稳定技巧：** 选择性精度（router 用
float32）、更小的初始化、专家 dropout。

**影响：** 直接催生了 Mixtral 8x7B、DeepSeek-V2/V3、Llama 4 等现代
MoE LLM。

**与 SCX/EGP 的关系：** - **理论基础关系。** 这些工作奠定了
MoE 路由、负载均衡的理论基础。SCX/EGP
的''输入条件路由''本质上是同一问题在势函数领域的应用，但面临不同挑战： -
NLP MoE 的输入是离散 token，路由空间相对有限 - SCX/EGP
的输入是连续原子构型，路由空间是高维连续流形 - NLP MoE 的专家是同构 FFN
层；SCX/EGP 的专家可以是异构的完整势函数

**SCX 相对优势：** - SCX/EGP
的核心理念------**``训练时不耦合，推理时再融合''**------避免了通用
MoE 的两个致命问题： 1. **训练不稳定：** 通用 MoE
的路由器与专家耦合训练，常导致专家坍塌（collapse）或不稳定。 2.
**负载均衡的开销：** 需要复杂的辅助损失函数。 - SCX/EGP
中每个专家可独立训练和验证，质量可控。

**空白填补机会：** - 通用 MoE
文献中丰富的理论成果（负载均衡、容量规划、路由策略）可以迁移到 SCX/EGP
框架中。 - 思考：能否借鉴 NLP MoE 的''共享专家''（shared expert）思想到
SCX/EGP 中？

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{B. Knowledge Distillation for
MLIP}<!-- label: b.-knowledge-distillation-for-mlip -->

#### B1. MACE → NEP 蒸馏<!-- label: b1.-mace-nep-ux84b8ux998f -->

**论文：** ``Constructing machine learning interatomic potentials
with minimum amount of ab initio data.'' npj Computational Materials,
s41524-026-02023-y (2026).

**他们解决了什么？** 用最少量的 DFT 数据（~200
个构型）构建高精度 MLIP，无需昂贵的主动学习循环（通常需要数千个 DFT
计算）。

**核心方法：** - **两阶段教师-学生蒸馏：** - Stage
1（教师）：从预训练通用模型 **MACE-MP-0** 开始，在
~200 个 DFT 构型上微调。 - Stage 2（学生）：将微调后的
MACE 教师蒸馏到轻量 **NEP** 模型。 -
验证体系：固态电解质（LGPS、LATP、LYC）。

**优势：** 单次（single-shot）工作流，无需主动学习循环。NEP
的推理速度远快于 MACE，适合大规模 MD 模拟。

**与 SCX/EGP 的关系：** - **强相关。** 该工作展示了''昂贵教师
→ 廉价学生''的标准蒸馏流水线。SCX/EGP 的蒸馏环节本质上也是''复杂专家 →
统一学生''，但 SCX/EGP 的关键差异在于： 1. **蒸馏前需规范化（Gauge
对齐）：** SCX/EGP 的 Gauge
对称化确保专家间能量零点一致，而该工作假设单一教师没有问题。 2.
**多专家蒸馏：** SCX/EGP
面临的不是单教师→单学生，而是多教师→单学生。

**SCX 相对优势：** - SCX/EGP
处理多专家情况下的''冲突预测''问题，该工作未涉及。 - SCX/EGP
可以蒸馏来自不同架构类型（MACE、NequIP、SevenNet
等）的教师，而该工作只有单一架构。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{B2. Ensemble Knowledge Distillation (EKD) for
MLIP}<!-- label: b2.-ensemble-knowledge-distillation-ekd-for-mlip -->

**论文：** Matin et al.~``Ensemble Knowledge Distillation for
Machine Learning Interatomic Potentials.'' arXiv:2503.14293 (2025).

**他们解决了什么？** 解决能量数据集缺少力标签的问题。在只有 QC
能量的数据集上，通过集成多个教师模型生成伪力，提高学生模型的精度。

**核心方法：** 1. 在 QC 能量上训练 **多个教师
MLIP**（多种初始化/架构）。 2.
用集成教师生成**平均伪力**（ensemble-averaged forces）作为软标签。
3. 学生模型同时学习 **QC 能量 + 集成平均力**。 4. 验证于 ANI-1ccx
数据集（耦合簇级别能量），在 COMP6 基准上达到 SOTA。

**与 SCX/EGP 的关系：** - **弱相关但有启发性。**
该工作关注的是''如何生成更好的软标签''，SCX/EGP
关注的是''如何组合多个独立训练的专家''。EKD
自然地使用了集成思路，但目的是蒸馏而非专家协作。

**SCX 相对优势：** - EKD 的所有教师需要共享同一训练数据；SCX/EGP
的专家可以在不同数据上独立训练。 - EKD
的学生架构不能是教师集的一部分；SCX/EGP
的''学生''本质上是编译器化的专家系统，保留了专家多样性。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{B3. Foundation Model
Distillation}<!-- label: b3.-foundation-model-distillation -->

**论文：** Gardner et al.~``Distillation of atomistic foundation
models across architectures and chemical domains.'' arXiv:2506.10956
(2025).

**他们解决了什么？** 证明合成数据蒸馏（distillation via synthetic
data）可以便宜地将原子级基础模型的知识迁移到不同架构。

**核心方法：** - 教师：基础模型（large universal MLIP） -
生成合成数据，标记后训练轻量学生 - 演示 \textgreater10x（GNN→GNN）和
\textgreater100x（GNN→ACE）加速 -
验证体系：液态水、极端条件下的氢、多孔二氧化硅、杂化钙钛矿、有机反应

**与 SCX/EGP 的关系：** - **中等相关。**
这是''基础模型→专门模型''的知识迁移，SCX/EGP
是''多个专门模型→编译器化系统''的专家协作。二者互补------基础模型可以作为
SCX/EGP 的专家候选池之一。

**空白填补机会：** - 该工作的''跨架构蒸馏''可以借鉴到 SCX/EGP
的蒸馏环节（如何从异构专家蒸馏到统一学生）。 -
目前没有工作探讨''如何从多个基础模型中蒸馏''------这正是 SCX/EGP
的用武之地。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{B4. Teacher-Student Training for MLIPs (RSC
2025)}<!-- label: b4.-teacher-student-training-for-mlips-rsc-2025 -->

**论文：** Matin et al.~``Teacher-student training improves the
accuracy and efficiency of machine learning interatomic potentials.''
RSC Digital Discovery, 2025.

**他们解决了什么？**
证明教师-学生训练不仅能加速推理，还能**提高学生模型的准确率**（甚至超过教师）。

**核心方法：** - 架构：**HIPNN**（Hierarchically Interacting
Particle Neural Network） -
损失函数增加一项：匹配学生与教师的逐原子能量预测 -
辅助标签：教师网络隐藏层的原子能量输出 - 实验：学生模型实现
**\textgreater2 倍速度**、**\textless50\%
内存**，且精度**超越**教师 - **帕累托主导**（Pareto
dominance）：在每个成本点上都优于对照模型

**与 SCX/EGP 的关系：** - **中等相关。**
关键启示：**蒸馏可以同时提高精度和效率**。SCX/EGP
的蒸馏环节应追求类似效果，而不仅仅是为了压缩。

**空白填补机会：** - 该工作仅使用单一教师。SCX/EGP
有机会展示''多教师蒸馏''不仅可以压缩模型，还可以通过集成效应超越任何单个专家------即
**EGP 的协同效应（synergy）**。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{B5.
其他重要蒸馏工作}<!-- label: b5.-ux5176ux4ed6ux91cdux8981ux84b8ux998fux5de5ux4f5c -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1765}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1765}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1765}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.4706}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
工作
\end{minipage} & \begin{minipage}[b]
年份
\end{minipage} & \begin{minipage}[b]
贡献
\end{minipage} & \begin{minipage}[b]
与 SCX/EGP 关系
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**SevenNet-Nano** (arXiv:2604.10887) & 2026 & 从 SevenNet-Omni
蒸馏到 Nano，\textgreater10 倍加速，极端条件验证 &
补偿性：单一模型蒸馏 

**PFD 框架** (Phys. Rev.~Materials, 2025) & 2025 &
Pre-train→Fine-tune→Distill 流水线，~100 DFT
帧训练~100x加速学生 & 流程互补：PFD 是蒸馏前的准备流程 

**ARK Distillation** (npj Comput. Mater., 2026) & 2026 &
角度关系知识蒸馏 + 对比学习，11.9x 催化剂筛选加速 &
方法创新：蒸馏中的结构保持 

\end{longtable}

**ARK Distillation 特别值得关注：** - 论文：Lim et al.~``Angular
relational knowledge distillation of machine learning interatomic
potentials for scalable catalyst exploration.'' npj Computational
Materials, 2026. - 核心创新：用**角度关系向量（angular relational
vectors）** 和**对比学习**保持教师 PES 的几何结构。 - 高通量筛选：58
万结构筛选仅用 11.6 GPU-hours（对照：59.4 CPU-years）。 - 启示：SCX/EGP
的蒸馏环节可以借鉴这种''结构保持''的思想，确保编译后的学生模型不丢失专家对
PES 几何的精细刻画。

**PFD 框架特别值得关注：** - 论文：Wang, Gao et al.~``Pre-training,
fine-tuning, and distillation (PFD): Automatically generating machine
learning force fields from universal models.'' Phys. Rev.~Materials,
2025. - 核心：DPA-2 → 微调 → DeePMD 学生，仅 ~100 帧 DFT
数据。 - SCX/EGP 可以与 PFD 结合：PFD 作为''专家生成''环节，SCX/EGP
作为''专家编译''环节。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{C. Expert Merging / Gauge / Energy
Alignment}<!-- label: c.-expert-merging-gauge-energy-alignment -->

\subsubsection{C1. Model Merging (Model Soup, Git Re-Basin,
线性模式连接)}<!-- label: c1.-model-merging-model-soup-git-re-basin-ux7ebfux6027ux6a21ux5f0fux8fdeux63a5 -->

**核心思想：**
将多个独立训练的模型权重直接平均（或经过排列对齐后平均）获得合并模型，无需再训练。核心假设：不同模型的解在权重空间中通过线性路径连接且损失面平坦。

**关键工作：**

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
工作
\end{minipage} & \begin{minipage}[b]
年份
\end{minipage} & \begin{minipage}[b]
贡献
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Model Soups** (Wortsman et al., ICML 2022) & 2022 &
均匀/贪心平均微调模型权重，提升精度且不增推理时间 

**Git Re-Basin** (Ainsworth et al., ICLR 2023) & 2023 &
通过排列对齐（permutation alignment）使不同模型处于同一
basin，再平均权重 

**ZipIt!** (ICLR 2024) & 2024 &
可以合并来自不同任务、不同架构的模型（以特征融合代替简单平均） 

**AME** (Lee \& Ngo, NeurIPS 2025) & 2025 & 将模型 soup
重新解释为''摊销模型集成（Amortized Model
Ensembling）``，使用伪梯度进行无数据元优化 

**Soup-of-Experts** (ICML 2025) & 2025 &
参数级专家线性组合，测试时可即时实例化任意域权重组合的模型 

**LLM Souping** (Meta, 2025) & 2025 & 加权平均多个微调
LLM，引入类别感知专家选择 SoCE 

\end{longtable}

**与 SCX/EGP 的关系：** - **概念近但方法不同。** 模型合并和
SCX/EGP 都追求''结合多个模型的知识''。但： -
模型合并在**权重空间**操作（weight-space
averaging），要求模型架构相同。 - SCX/EGP
在**预测空间**操作（prediction-space ensembling），可处理异构架构。
- 模型合并是一个**融合**过程（多个模型融合为一个）；SCX/EGP
是一个**编译**过程（多个模型保持独立但通过路由系统协调）。

**SCX 相对优势：** - **架构无关性：**
模型合并要求同构架构，SCX/EGP 可处理 MACE + NEP + SevenNet 异构组合。 -
**可竞争性：** 模型合并建立于''模型在权重空间中相容''的假设上，这在
MLIP 中是否成立尚待验证。SCX/EGP 不需要这种假设。 - **可解释性：**
SCX/EGP 保留了每个专家的身份，可以追溯哪些专家对哪些输入负责。

**空白填补机会：** - 目前**没有工作**将模型合并方法系统应用于
MLIP 领域。 - 可以尝试''MLIP
在权重空间中的线性模式连通性''研究------这是一个开放问题。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{C2. MLIP Gauge Freedom 与 Species Energy
Shift}<!-- label: c2.-mlip-gauge-freedom-ux4e0e-species-energy-shift -->

**论文：** ``Gauge dependence of total energies and
cross-functional transfer learning.'' arXiv:2504.05565 (2025).

**他们解决了什么？** 明确指出了 MLIP 中的 **Gauge 自由（gauge
freedom）** 问题：DFT
总能依赖于真空能级的标度选择，不同泛函的总能量基准不同。这个''Gauge''的选择影响
MLIP 的迁移学习效果。

**核心方法：** - 分析多种迁移学习策略，对比''是否调整
AtomRef（species energy shift）``的影响。 - **关键发现：**
跨功能迁移学习时，**先 refit AtomRef 再训练 GNN**
是最优策略。仅重训练 AtomRef 就将 Pearson 相关系数从 0.09 提升到 0.93。
- 具体结果：Method 4（refit AtomRef + train GNN）能量 MAE = 17
meV/atom，而直接在源功能基上训练 GNN 是 26 meV/atom。

**与 SCX/EGP 的关系：** - **核心相关。** Gauge freedom 正是
SCX/EGP 中 **Gauge 对称化**环节要解决的问题。不同 MLIP
在相同结构上的总能量预测存在系统性能量偏移（例如，OUTCAR 中的''energy
without entropy''和 MACE 的预测相差数 eV）。 - SCX/EGP 的 Gauge
层（GAU）作用就是消除这种偏移，使不同专家的能量预测在联合前可比较。

**SCX 相对优势：** - 该工作需要每个专家都有自己的 AtomRef
且需要在数据集上显式计算。SCX/EGP 的 Gauge
层可以在不接触原始训练数据的情况下**在线校准**------只需在重叠构型上比较预测值。
- SCX/EGP 的 Gauge
对称化不仅处理能量偏移，还处理**力和应力的对齐**（通过 DOF 变换）。

**空白填补机会：** - 该工作中指出''formation energy''方法是
Gauge-invariant 的替代方案。SCX/EGP 可以探索：是否在 formation energy
空间而非 total energy 空间进行专家编译？ -
目前没有工作系统地探讨**多专家之间的 Gauge 不一致性**------SCX/EGP
是第一个系统解决该问题的框架。 - 该工作只跨功能基（GGA/GGA+U →
r²SCAN）迁移。SCX/EGP 可以扩展到跨势函数的 Gauge 对齐（SPME → MACE →
NEP）。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{C3. Species Energy Shift
标准做法}<!-- label: c3.-species-energy-shift-ux6807ux51c6ux505aux6cd5 -->

当前主流通用 MLIP 中的能量偏移处理：

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
模型 & 方法 & 说明 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
CHGNet & AtomRef + GNN & 元素级线性偏移 + 图神经网络残差 

M3GNet & AtomRef + GNN & 同上 

NequIP & AtomRef (subtract per-atom energy) & 训练前减去参考能量 

CACE & AtomRef + GNN & Composible Atomic Cluster Expansion 

MACE-MP-0 & 平均原子能偏移 & 基于 MP 数据集计算平均偏移 

SevenNet & 隐式 offset & 模型自动学习偏移 

\end{longtable}

所有这些方法都是**单模型校准**------将单个模型的能量预测对齐到某个参考。SCX/EGP
的 Gauge 对称化是第一个处理**跨模型能量对齐**的方法。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{D. Expert Compilation / Governance（SCX
核心创新区）}<!-- label: d.-expert-compilation-governancescx-ux6838ux5fc3ux521bux65b0ux533a -->

这是 SCX/EGP
最核心的差异化领域。搜索结果显示，该方向目前**基本没有竞争工作**。以下是搜索覆盖的几个子方向：

\subsubsection{D1. ``蒸馏前的专家规范化''（Expert Normalization Before
Distillation）}<!-- label: d1.-ux84b8ux998fux524dux7684ux4e13ux5bb6ux89c4ux8303ux5316expert-normalization-before-distillation -->

**搜索结论：没有专门的工作。**

- 
- 
- 
- 

**SCX 的机会：** - 这是 SCX/EGP
最明确的技术壁垒。如果有其他工作开始研究''多教师蒸馏前的能量对齐''，SCX
需要及时跟进和引用。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{D2. Expert Domain
Certification}<!-- label: d2.-expert-domain-certification -->

**搜索结论：没有适用于 MLIP 的专家域认证工作。**

- 
- 
- 
- 

**SCX 的机会：** - 可以考虑发表专门的方法论文定义''MLIP Expert
Domain Certification''的形式化框架。 - 可以借鉴 conformal prediction
的思想，为每个专家在认证域内提供保证。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{D3. Multi-Expert Conflict
Arbitration（多专家冲突仲裁）}<!-- label: d3.-multi-expert-conflict-arbitrationux591aux4e13ux5bb6ux51b2ux7a81ux4ef2ux88c1 -->

**搜索结论：在通用 ML 领域有探索，但在 MLIP 领域为空白。**

通用 ML 领域的相关工作：

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
工作
\end{minipage} & \begin{minipage}[b]
类型
\end{minipage} & \begin{minipage}[b]
方法
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**King Solomon Protocol** (2026) & 人类监督仲裁 &
正式的仲裁框架，双助手架构，结构化人类仲裁层 

**HCDF** (2026) & 层次化认知 &
知识获取→显式风险表示→结构仲裁三层架构 

**Cognitive Hives** (2026) & 分布式认知 &
专门的冲突解决层，识别/仲裁/协调争议 

**LLMediator / Mediator** (2025) & LLM 调解 &
基于不确定性路由，低冲突层平均 + 高冲突层 MoE 

**AEGIS-Nexus** (2026) & 伦理仲裁 &
元司法仲裁代理，平衡影响力、可靠性和严重性 

**Multi-Expert Fusion Networks** survey & 综述 &
软门控、稀疏路由、top-k 仲裁等分类 

\end{longtable}

**MLIP 领域：没有工作探讨多势函数之间的预测冲突与仲裁。**

- 
- 

**SCX 的机会：** - 可以将通用 ML 仲裁的成果（如 HCDF
的层次化解耦、LLMediator 的不确定性路由）引入 MLIP 领域。 -
可以发表案例研究，展示 EGP 仲裁策略对预测质量的影响。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{D4.
多专家性能的输入条件依赖}<!-- label: d4.-ux591aux4e13ux5bb6ux6027ux80fdux7684ux8f93ux5165ux6761ux4ef6ux4f9dux8d56 -->

**搜索结论：没有系统性的工作。**

- 
- 
- 
- 

**SCX 的机会：** - ECR
层本质上就是一个专家性能配置文件的实时评估器。 -
可以发布一个专家性能配置文件的自动构建工具。

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{E.
竞争格局总结与战略建议}<!-- label: e.-ux7adeux4e89ux683cux5c40ux603bux7ed3ux4e0eux6218ux7565ux5efaux8bae -->

\subsubsection{E1.
创新维度对比矩阵}<!-- label: e1.-ux521bux65b0ux7ef4ux5ea6ux5bf9ux6bd4ux77e9ux9635 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.2857}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 10\tabcolsep) * \real{0.1429}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
竞争维度
\end{minipage} & \begin{minipage}[b]
DeepMD MoE (2603)
\end{minipage} & \begin{minipage}[b]
Allegro MoE (2604)
\end{minipage} & \begin{minipage}[b]
模型合并
\end{minipage} & \begin{minipage}[b]
MLIP 蒸馏
\end{minipage} & \begin{minipage}[b]
SCX/EGP
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
训练时 MoE & Y & Y & N & N & N 

后训练/编译 & N & N & Y & Y & **Y** 

异构专家 & N & N & N & N & **Y** 

Gauge 对齐 & N & Y(隐式) & N & N & **Y** 

输入条件路由 & Y(元素级) & Y(空间) & N & N & **Y** 

专家域认证 & N & N & N & N & **Y** 

蒸馏前规范化 & N & N & N & N & **Y** 

冲突仲裁 & N & N & N & N & **Y** 

训练不可知 & N & N & Y & N & **Y** 

\end{longtable}

**核心结论：SCX/EGP 在''后训练编译''这个细分领域没有直接竞争。**
每个现有工作都只在某些维度上与 SCX/EGP 有交集，但没有任何工作覆盖
SCX/EGP 的全部创新维度。

\subsubsection{E2.
竞争风险等级评估}<!-- label: e2.-ux7adeux4e89ux98ceux9669ux7b49ux7ea7ux8bc4ux4f30 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2381}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4762}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2857}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
风险等级
\end{minipage} & \begin{minipage}[b]
竞争方向
\end{minipage} & \begin{minipage}[b]
原因
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**高** & DeepMD MoE (2603.07977) & DeepMD
社区大、影响力强，如果他们将路由策略扩展到后训练场景，将是直接竞争 

**高** & Allegro MoE (2604.26143) &
如果他们将''空间分区''扩展到''输入条件分区''，会与 EGP 的路由层重叠 

**中** & ARK 蒸馏 (npj 2026) & 如果 ARK
扩展到多教师蒸馏并引入对齐步骤，将进入''蒸馏前规范化''领域 

**中** & PFD 流程 (PRM 2025) & 如果 PFD
扩展到''多模型联合蒸馏''，将接近 EGP 的 Compile 层 

**低** & 模型合并 (通用 ML) &
架构不可知方向不同，且合并需要同构架构 

**低** & Foundation 蒸馏 (2506.10956) &
目前聚焦单教师→单学生，进入多教师领域还需较大跨度 

\end{longtable}

\subsubsection{E3. SCX/EGP
必须主动占领的空白}<!-- label: e3.-scxegp-ux5fc5ux987bux4e3bux52a8ux5360ux9886ux7684ux7a7aux767d -->

按优先级排序：

1. 
2. 
3. 
4. 
5. 

#### E4. 建议行动项<!-- label: e4.-ux5efaux8baeux884cux52a8ux9879 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2941}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3529}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3529}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
优先级
\end{minipage} & \begin{minipage}[b]
行动
\end{minipage} & \begin{minipage}[b]
说明
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
P0 & SCX 系统论文 & 在 arXiv 上发表 SCX/EGP 的方法论文，建立''Expert
Compilation''这一新方向的官方名称 

P0 & 开源 EGP 演示 & 基于现有的 VASP + MACE + NEP 等模型展示完整的
Gauge→Route→Compile 流水线 

P1 & Gauge 对称化论文 & 单独发表对 MLIP Gauge freedom
的量化分析和校准方法 

P1 & 输入条件路由 vs.~DeepMD MoE 对比基准 & 在 OMat24 等标准基准上与
DeepMD MoE 对比 

P2 & 专家域认证白皮书 & 定义 Expert Domain Certification 的形式化框架 

P2 & 冲突仲裁方法论论文 & 展示 EGP 的 Route 层如何处理多专家分歧 

\end{longtable}

\subsubsection{E5.
竞争方法背后的团队/组织}<!-- label: e5.-ux7adeux4e89ux65b9ux6cd5ux80ccux540eux7684ux56e2ux961fux7ec4ux7ec7 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2857}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4762}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2381}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
团队
\end{minipage} & \begin{minipage}[b]
相关论文
\end{minipage} & \begin{minipage}[b]
对 SCX 的竞争风险
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**DP Technology / AIS** (张林峰, 王涵等) & DeepMD MoE (2603.07977)
& 高------他们在 MLIP 领域影响力最大 

**Boris Kozinsky 组** (Harvard) & Allegro/NequIP, MoE (2604.26143)
& 高------势函数架构原创者 

**InstaDeep** & mlip JAX 库 (2605.22698) &
中------工程能力强，但研究侧重不同 

**LANL** (Sakib Matin 等) & EKD, Teacher-student RSC &
中------蒸馏方向强，但短期内不会进入多专家编译 

**Volker Deringer 组** (Oxford) & Foundation distillation
(2506.10956) & 中低------学术风格偏基础模型，而非工程编译 

**Seoul National Univ.** (Jeong Woo Han 组) & ARK Distillation &
中低------集中在催化筛选应用，而非方法论 

**USTC** (高玉祥等) & PFD 框架 (2502.20809) & 中------PFD
的''自动生成''方向与 EGP 互补 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 参考文献<!-- label: ux53c2ux8003ux6587ux732e -->

#### A. MoE in MLIP<!-- label: a.-moe-in-mlip -->

1. 
2. 
3. 
4. 
5. 
6. 

\subsubsection{B. Knowledge Distillation for
MLIP}<!-- label: b.-knowledge-distillation-for-mlip-1 -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 

\subsubsection{C. Expert Merging / Gauge
Alignment}<!-- label: c.-expert-merging-gauge-alignment -->

1. 
2. 
3. 
4. 
5. 
6. 

\subsubsection{D. Governance / Arbitration (General
ML)}<!-- label: d.-governance-arbitration-general-ml -->

1. 
2. 
3. 
4. 
5. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

> 报告结束。本分析基于公开文献检索（截至 2026-06-25），覆盖 arXiv、Nature
> Portfolio、RSC、APS、Springer 等来源。SCX/EGP
> 在''后训练多专家编译''这一细分领域无直接竞争，但需警惕 DeepMD 和
> Kozinsky 组等团队可能的后续扩展工作。