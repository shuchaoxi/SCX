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
| Papers 论文 | 212 .tex + 250 .md |
| Scripts 验证 | 33 ALL PASS |
| Tests 测试 | 676 passed |
| Reviews 审查 | 155+ 轮次 |
| P0 fixes | ✅ 清零 |
| Review standard | **10 轮收敛** |

→ [Audit status 审计状态](AUDIT_STATUS.md) · [Attack surface 攻击面](ATTACK_SURFACE.md) · [Paper index 论文索引](PAPER_SCRIPT_INDEX.md)

---

## 🔟 10-Round Review Standard · 十轮审查标准

Major scientific questions require 10 rounds of hostile review before convergence.  
重大科学问题需经 10 轮敌对审查方可收敛。

| 阶段 | 轮次 | 目标 |
|:--|:--:|------|
| 初始审查 | 1-3 | 发现致命错误 |
| 深度修复 | 4-6 | 修正+验证+边界条件 |
| 跨域一致性 | 7-9 | 与其他定理交叉验证 |
| 终审 | 10 | 无可发现错误 |

### Convergence Status · 收敛状态

| 项目 | 轮次 | 目标 |
|------|:--:|:--:|
| 规范理论 | 10 | ✅ |
| 核心定理1-4 | 9 | ✅ |
| 博弈论 NPE | 8 | ✅ |
| 统一场论 | 9 | ✅ |
| 量子审计 | 9 | ✅ |
| 黑洞奇点 | 9 | ✅ |
| 社会推论7篇 | 9 | ✅ |
| Monte Carlo | 8 | ✅ |
| 相场论 | 8 | ✅ |
| 弦统一 | 8 | ✅ |
| 反抗悖论 | 9 | ✅ |
| 可审计性原理 | 9 | ✅ |

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
| P0 | ✅ Thm2 δ倒置 — sqrt(2/δ)→sqrt(δ/2) |
| P0 | ✅ 相场论双阱势 — 诚信态局部极大→极小 |
| P0 | ✅ Monte Carlo Cercis符号 — -λ→+λ |
| P1 | ✅ Thm3 preference domain — 构造闭合 |
| P2 | ⏳ 大统一 LaTeX 重做 | 进行中 |
| P2 | ✅ 工程代码审查 | 3轮完成 |
| P3 | ⏳ 地缘政治 新国家章节 | 进行中 |
| P1 | ⏳ 博弈论 治理↔SCX检测率桥接引理 | 本轮识别 |
| P2 | ⏳ 博弈论 M*推导+存在性条件 | 本轮识别 |
| P2 | ⏳ 弦统一 Cercis跨论文协调 | 本轮识别 |
| P3 | ⏳ 地缘政治 新国家章节 | 进行中 |
| P3 | ⏳ 验证脚本生成 (30套中5套排队) | 进行中 |

→ [Full attack surface 完整攻击面](ATTACK_SURFACE.md)

---

## 📂 Structure · 结构

```
papers/      197 papers 论文
src/scx/     55 Python files
tests/       676 passed 测试全绿
docs/
├── reviews/     37+ review reports 审查报告
├── analysis/    15 analysis documents 分析文档
└── supplementary/  193+ historical files 历史文件
```

## 🙏 Acknowledgments · 致谢

This work was audited by multiple independent AI systems through rigorous hostile review.  
本工作经过多个独立 AI 系统的严格敌对审查。

| 致谢 | Why |
|------|-----|
| **Claude Code** (Anthropic) | Powered multi-round hostile review, parallel paper-writing, and 105+ review rounds converging 24/24 items. |
| **Hermes Agent** (Nous Research) | Orchestrated the audit pipeline, sub-agent delegation, theorem review and paper generation. |
| **DeepSeek API** | Compute backbone at 1/20th the cost of alternatives — made 105+ rounds of hostile review economically feasible. |
| **All AI Reviewers** | Claude, DeepSeek, Codex — M>1 independent models, different architectures, genuine multi-expert audit. |

> 不解释。有代码。自己跑。审计我。  
> No explanations. Code is here. Run it yourself. Audit me.

## Author · 作者

SCX. 2026. All theorems open. All code open. Audit me.  
所有定理公开。所有代码公开。审计我。
