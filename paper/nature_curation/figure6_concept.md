# 论文 Figure 6: Extensions — Sprint Beyond MD

> 放在论文最后，标题 "Outlook" 或 "Broader Implications"

---

## Figure 6 概念设计

```
╔══════════════════════════════════════════════════════════════════╗
║                  SPRINT GATEKEEPER                               ║
║         "Curate, Don't Clean. Evolve, Don't Discard."           ║
║                                                                  ║
║   ✅ Proven in this work: MD 非平衡模拟 + DFT 蒸馏 + 在线成长      ║
╚══════════════════════╤═══════════════════════════════════════════╝
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌─────────┐  ┌─────────────┐
    │  🧬     │  │  🏭     │  │  🤖          │
    │ 药物发现 │  │ 半导体   │  │ 具身智能     │
    │         │  │ 工艺     │  │             │
    │ DTI筛选 │  │ CMP/Etch │  │ 机器人实验   │
    │ 蛋白降解 │  │ 设备寿命 │  │ 自驱动实验室 │
    │ 货架期   │  │ 预测维护 │  │ 主动学习     │
    │         │  │         │  │             │
    │ "同样    │  │ "同构的  │  │ "Sprint     │
    │  的幂律  │  │  Gamma   │  │  告诉机器人 │
    │  冗余"   │  │  退化"   │  │  下一个该测 │
    │         │  │         │  │  什么"       │
    └────┬────┘  └────┬────┘  └──────┬──────┘
         │            │              │
         └────────────┼──────────────┘
                      │
                      ▼
         ┌─────────────────────────┐
         │  Future Directions       │
         │  (not in this work)      │
         └─────────────────────────┘
```

---

## 图的文字说明

**Figure 6 | Sprint as a universal data-quality paradigm.**

The Sprint gatekeeper proven here for MD non-equilibrium simulations
extends naturally to three domains:

**Drug Discovery.** Protein-ligand interaction databases exhibit the same
power-law redundancy and systematic assay noise as DFT datasets. Sprint's
quality scoring directly transfers — replacing SCF convergence checks with
assay reproducibility filters, and magnetic moment corrections with pKd
calibration across measurement platforms.

**Semiconductor Manufacturing.** CMP pad wear, etch chamber drift, and
deposition sensor degradation all follow gamma-process decay curves —
structurally isomorphic to the MD trajectory quality metrics Sprint already
handles. The online learning loop proven here for molecular dynamics applies
unchanged to equipment lifecycle monitoring.

**Embodied Intelligence.** In self-driving laboratories, Sprint serves as
the experimental design critic — evaluating not just data quality, but
experimental value. The curation-exploration tradeoff becomes an
acquisition function: Sprint tells the robot which experiment to run next,
and which past results to revisit as the model evolves.

---

## 排版建议

- 上半部分：Sprint 核心框架 (Fig 1 的简化版)
- 下半部分：三个延伸方向，用箭头连接，虚线边框（表示"未在本文验证"）
- 配色：已证明的用实色，延伸的用半透明/虚线
- 底部标注：*"Extensions. Validation in these domains is left for future work."*

---

## 为什么要放这张图

| 作用 | 效果 |
|------|------|
| 显示 vision | reviewer 看到你不是"只会做 MD" |
| 预判质疑 | "为什么只做一个领域？"→ 图上已经回答了 |
| 吸引引用 | 做药物/半导体/具身智能的人会 cite 你 |
| Nature 风格 | Nature 论文标配：最后一张图放 broader impact |
