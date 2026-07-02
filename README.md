# SCX — State-Conditioned eXpertise

**A mathematical framework for certifying data quality through multi-expert consensus.**  
**多专家共识驱动的数据质量认证数学框架。**

```math
∑g = 0  —  the only condition.  唯一条件。
```

---

## 📊 Status · 状态

| | |
|:--|:--|
| Papers 论文 | 195+ |
| Review rounds 审查轮次 | 105+ |
| Tests 测试 | 676 passed |
| Converged items 已收敛 | 24/24 |
| P0 critical fixes | ✅ 全部清零 |
| Formalization 形式化 | ✅ 全部完成 |

→ [Full audit status 完整审计状态](AUDIT_STATUS.md)

---

## 🌳 How to Critique SCX · 如何批评SCX

SCX welcomes critique. Here is the dependency tree — the shortest path to falsifying the framework.  
SCX欢迎批评。以下是依赖树——证伪此框架的最短路径。

### Dependency Hierarchy · 依赖层次

```
L0 数学地基 Mathematical Foundation
├── Thm1 (Hoeffding noise bound 噪声检测界)
│   └── Depends on 被依赖: all audit guarantees 所有审计保证
├── Thm3 (Honest Person 老实人定理)
│   └── Depends on: M>1 necessity 多专家必要性
└── Discrete Hodge gauge theory 离散Hodge规范理论
    └── Depends on: ∑g=0 formalism 规范固定形式化

L1 博弈论与经济 Game Theory & Economics
├── NPE Equilibrium (Theorem 1 algebra error found ❗)
│   └── Depends on: Yajie adoption, protocol value
├── Audit Economics 审计经济学
└── SCX Prize mechanism

L2 工程实现 Engineering
├── Spring → Yajie → Arbiter → Cercis
└── Verification scripts 验证脚本

L3 物理方向 Physics
├── Gauge theory (discrete Hodge) — L0
├── Quantum audit — independent
├── Singularity theory — POETRY, noted
├── Audit instanton — killed (holonomy=0)
├── String theory — CARGO-CULT, closed
└── Entanglement/wormhole/relativity — 5 rounds

L4 社会推论 Social Inference
├── 7 directions (edu/med/social/parent/peer/env/art)
├── Legal inference (false accusation + delayed justice)
└── Literary analysis (Three-Body Problem)

L5 协议与治理 Protocol & Governance
├── Protocol governance 协议治理
├── Grand unification 大统一
├── World audit 世界审计
├── Industry analysis 行业分析
├── Geopolitical analysis 地缘政治
├── Maintainer analysis 维护者分析
├── Resistance paradox 反抗悖论
└── Auditability principle 可审计性原理
```

### Attack Paths · 攻击路径

| Path 路径 | Target 目标 | Impact 影响 |
|:--|------|:--:|
| **最短致命 Shortest kill** | Thm1 Hoeffding constant wrong | All audit guarantees collapse 全塌 |
| **经济蒸发 Economic** | NPE equilibrium invalid | Protocol layer evaporates 协议层消失 |
| **绕过 Bypass** | Social inference domain errors | Public trust lost 公众信任丧失 |

### Fix Priority · 修复优先级

| P | Item |
|:--:|------|
| P0 | ✅ NPE Theorem 1 — 从第一原理重建 |
| P0 | ✅ Thm1 constant — 代码正确 |
| P1 | ✅ Thm3 preference domain — 构造闭合 |
| P2 | ⏳ Engineering code review — 进行中 |
| P2 | 大统一 LaTeX — 待重做 |
| P3 | 地缘政治 — 新国家章节 |

→ [Full attack surface 完整攻击面](ATTACK_SURFACE.md)

---

## 📂 Structure · 结构

```
papers/      92+ papers 论文
src/scx/     55 Python files (Spring, Yajie, Arbiter, Cercis, Situs, M-Registry)
tests/       678 tests passed 测试全绿
docs/
├── reviews/     30+ review reports 审查报告
├── analysis/    10+ analysis documents 分析文档
└── supplementary/  193+ historical files 历史文件
```

## Author · 作者

SCX. 2026. All theorems open. All code open. Audit me.  
所有定理公开。所有代码公开。审计我。
