# SCX 理论架构说明

> 最后更新：2026-06-30

---

## 四篇论文的关系

```
                    ┌─────────────────────────┐
                    │   Paper 1: SCX 核心理论   │
                    │   Yajie 审计的数学基础     │
                    │   Theorem 1-4             │
                    └───────────┬───────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ Paper 2: Situs 理论  │ │ Paper 3: Spring 理论 │ │ Paper B: SCX in     │
│ 物理位置编码         │ │ 自进化 Gatekeeper    │ │ Space 应用展望       │
│ 可选的空间感知层     │ │ 数据质量自我改进     │ │ 12 场景适用性分析    │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

---

## Paper 1：SCX 核心理论（Yajie）

**文件：** `paper/arxiv/scx_theory/main.tex`

**做什么：** 用 M 个独立专家的一致性检测标签噪声。

**核心定理：**
- **Theorem 1（噪声检测）：** F1 ≥ 1 − (1/η)·Σρ_s·exp(−2MΔ_s²)。M 个专家 → 检测精度指数增长。
- **Theorem 2（弱特征界）：** 特征不够好时，SCX 不比简单基线强。Fano 不等式给出上界。
- **Theorem 3（不可区分性）：** 噪声样本和困难样本在观测上不可区分。这是定理级别的"数据清洗有硬边界"。
- **Theorem 4（Minimax 最优）：** SCX 的自适应阈值达到精确常数最优。Bahadur-Rao + Chernoff-Stein。

**依赖：** 无。这是地基。

**状态：** ✅ 已编译 PDF，理论完整。

---

## Paper 2：Situs 理论

**文件：** `paper/arxiv/situs_theory/main.tex`

**做什么：** 在状态原子上叠加物理位置编码 h_i = φ(s_i) + PE(p_i)。让框架感知空间。

**核心贡献：**
- 最优频率谱（Laplace 核 + Bochner 定理）
- 3D 旋转编码（SO(d) 嵌入）
- 精确 Lipschitz 常数
- 修正 Theorem 1-3 以适应 Situs 增强
- 诚实标注所有理论局限（Fano 降级、贝叶斯最优鸿沟、旋转等变性缺失）

**与 Paper 1 的关系：** Situs 是 Yajie 的上游。Yajie 不依赖 Situs——没有空间信息时直接跑 Core。有空间信息时 Situs 改善 Δ_s。

**Situs 不破坏 Yajie 的任何定理。** 唯一的"破坏"是学习型 Situs 可能打破 Theorem 3 的不可区分性——但这是审计能力增强，不是缺陷。

**状态：** ✅ 8/8 最终验证通过。

---

## Paper 3：Spring 理论

**文件：** `paper/arxiv/spring_config/main.tex`

**做什么：** 让门控器 S_t 和 NEP 学生 f_θ_t 在记忆库 M_t 上共同进化。数据质量自我改进。

**核心定理：**
- **Theorem Spring-1：** 在 C1-C7 条件下，(S_t, θ_t) 收敛到联合不动点 (S*, θ*)。Lyapunov 下降 + 参考集重放 (C10) + 重要性采样 (C11)。
- **Theorem Spring-2：** 物理约束下有限时间终止。
- **关键创新：** 先证"没有 C10/C11 则 Lyapunov 下降不可能"，再证"有则严格成立"。

**与 Paper 1 的关系：** Spring 是 Yajie 的下游。Yajie 初始化 S_0（初始门控器 = 多专家共识分数），Spring 让它进化。

**状态：** ✅ 已编译 PDF，Lyapunov 证明完整。

---

## Paper B：SCX in Space 应用展望

**文件：** `paper/arxiv/situs_applications/main.tex`

**做什么：** 12 个科学场景的 Situs 适用性分析。告诉别人"在哪用"。

**核心判据：** I(Y;P|S) > 0 —— 物理位置在给定状态原子后仍携带标签信息。

**场景：** AlN 缺陷、CNT 手性（教学）、Drug-Target 对接、基因组学（旗舰）、遥感、气候、地震、半导体制造、网格审计、医学影像、天文、辐照物理（展望）。酶活性位点和海洋学为条件性/排除场景。

**状态：** ✅ 3 轮审查修正。

---

## 分层架构

```
Tier 1 (Core)：       无空间数据
  State Crystallization → Spring → Yajie → Cercis Score

Tier 2 (Spatial)：    有空间数据
  State Crystallization → Situs → Spring → Yajie → Cercis Score

Tier 3 (Extended)：   大规模空间数据 + Multi-Head
  State Crystallization → Situs → Multi-Head Spring → Yajie → Cercis Score
```

---

## 独立性与交集

| | Paper 1 (Yajie) | Paper 2 (Situs) | Paper 3 (Spring) |
|---|---|---|---|
| 依赖 Yajie？ | — | ❌ 不依赖。Situs 是 Yajie 的上游增强 | ✅ Spring 的 S_0 = Yajie 的共识分数 |
| 被 Yajie 依赖？ | — | ❌ Yajie 不依赖 Situs | ❌ Yajie 不依赖 Spring |
| 独立可投？ | ✅ | ✅ | ✅ |

**三篇理论论文两两独立，可以分开投稿。** Yajie 是地基，Situs 和 Spring 是两个独立方向的扩展——一个加空间感知，一个加时间进化。

---

## 证明文件索引

| 理论 | 主论文 | 底层推导 | 验证报告 |
|------|--------|---------|---------|
| Yajie | `paper/arxiv/scx_theory/main.tex` | `theory/theorems/` (S1-S8) | — |
| Situs | `paper/arxiv/situs_theory/main.tex` | `theory/self_evolution/ppe_rigorous_derivation.md` | `situs_final_verification.md` |
| Spring | `paper/arxiv/spring_config/main.tex` | `theory/self_evolution/01-12_*.md` | `09_verification_report.md` |
