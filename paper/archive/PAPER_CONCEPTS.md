# SCX 论文构想 — 最终版

> 2026-06-28 | 全部直指 Nature 系列

---

## Paper I: 数学基础 → Nature

**标题**: A Fundamental Impossibility in Data Quality: Distinguishing Label Noise from Sample Difficulty is Provably Unsolvable Without Explicit Assumptions

**一句话**: 我们证明了一个关于数据质量的基础性限制定理——区分标签错误和样本困难在数学上不可解，除非你明确陈述你的假设。在这个假设下，多专家一致性检测达到了精确常数 minimax 最优。

**正文**: 已起草 (`nature_theory/main/nature_main.tex`, ~2000 words)
**SI**: 86 页待转译 LaTeX（S1-S8, 全部证明已就绪）
**阻塞**: SI LaTeX 写作（纯体力活）
**投稿**: 今天可上传 arXiv，SI 完成后投 Nature

---

## Paper II: 实践原则 → Nature Computational Science

**标题**: The Curation-Exploration Tradeoff: Why Premature Data Cleaning Harms Machine Learning

**一句话**: 过早清洗数据会毁掉区分噪声和困难所需的信号。你必须先训练多样化专家（探索），让"状态条件专家性"自然发育，然后用一致性信号识别哪些真正需要清洗（策展）。

**正文**: 概念已设计 (`nature_curation/PAPER_CONCEPT.md`)，正文待写
**实验**: 4 域验证 (AlN, CIFAR, MedMNIST, DrugBank)
**阻塞**: 正文写作 + GPU 实验
**投稿**: Paper I arXiv 后投

---

## Paper III: 方法验证 → Nature Machine Intelligence

**标题**: Training Data Quality Dominates Model Architecture in Scientific Machine Learning

**一句话**: 在材料科学、医学影像、药物发现、计算机视觉四个领域，数据清洗带来的性能提升是架构改进的 12-19 倍。SCX 两层状态发现 + 多专家一致性是实现这一提升的关键。

**正文**: Methods 草稿已有 (`paper1_nature/theory_methods.tex`)
**阻塞**: GPU（AlN v3 重训, CIFAR/MedMNIST 完整训练）
**投稿**: GPU 到位后 4 周

---

## Paper IV: 领域应用 → npj Computational Materials

**标题**: Consistency-Constrained Expert Merging for Atomic Cluster Expansion Potentials

**一句话**: 独立训练的 ACE 专家势函数可以通过 gauge fixing + energy alignment + residual construction 安全合并，naive merge 产生物理错误。

**正文**: 已完成 (`paper2_mlip/paper_v3.tex`, 785 行)
**阻塞**: 超算（M1+M2 实测）
**投稿**: 1-2 周内可投（需超算跑完 M1）

---

## 当前行动

| 优先级 | 行动 | 阻塞 |
|:--:|------|:--:|
| **P0** | Paper I SI 转 LaTeX | 纯体力，无阻塞 |
| **P0** | arXiv 上传 Paper I | 正文已有，SI 可以后续更新 |
| P1 | Paper IV 跑 M1+M2 实验 | 超算 GPU |
| P2 | Paper II 正文写作 | 无阻塞 |
| P3 | Paper III 等 GPU 实验 | GPU |
