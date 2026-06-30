# SCX 论文矩阵 — 三篇 Nature 系列

> 更新：2026-06-28
> 策略：三篇论文直指 Nature 系列期刊，互相引用形成学术壁垒

---

## 论文谱系

| # | 目录 | 标题 | 目标期刊 | 类型 | 核心贡献 |
|:--:|------|------|------|------|------|
| I | `nature_theory/` | A Fundamental Impossibility in Data Quality | **Nature** | 理论发现 | 不可辨识定理 + 精确常数 minimax 最优性 (Thm 1-6) |
| II | `nature_curation/` | The Curation-Exploration Tradeoff | **Nature Computational Science** | 实践原则 | 过早清洗破坏信号 → 先探索后清洗 |
| III | `paper1_nature/` | Data Quality Dominates Model Architecture | **Nature Machine Intelligence** | 方法验证 | SCX 两层状态发现 + 4 域跨域验证 |
| IV | `paper2_mlip/` | Consistency-Constrained Expert Merging | **npj Computational Materials** | 领域应用 | EGP gauge fixing + 多专家势函数合并 |

## 互相引用关系

```
Paper I (Nature): 数学基础
  ├── 被 Paper II 引用: "Thm 3 证明清洗前需要专家多样性"
  ├── 被 Paper III 引用: "Thm 1+4' 提供 SCX 方法的理论保证"
  └── 被 Paper IV 引用: "gauge fixing 是状态条件专家性的一个实例"

Paper II (Nat Comp Sci): 实践原则
  ├── 引用 Paper I: 数学基础
  ├── 引用 Paper III: SCX 作为实现方案
  └── 独立贡献: "Curation-Exploration Tradeoff" 概念

Paper III (Nat Mach Intell): 方法验证
  ├── 引用 Paper I: 理论保证
  ├── 引用 Paper II: 实践框架
  └── 独立贡献: 4 域实验证据（AlN, CIFAR, MedMNIST, DrugBank）

Paper IV (npj): 领域应用
  ├── 引用 Paper I: 状态条件框架
  └── 独立贡献: ACE 专家势函数合并
```

## 投稿顺序

```
1. Paper IV (npj Comp Mat)  ← 最快可投 (1-2 周)，不依赖其他论文
2. Paper I (Nature)          ← 数学全部就绪，SI 写作中
3. Paper III (Nat Mach Intell) ← 等 GPU 完成 P0 实验后投稿
4. Paper II (Nat Comp Sci)   ← 最后投，引用前三篇
```

## 各论文状态

| 论文 | 正文 | SI | 实验 | 投稿 |
|:--:|:--:|:--:|:--:|:--:|
| I (Nature) | ✅ 已起草 | ⬜ 待 LaTeX 转译 | ✅ 数值验证完成 | ⬜ |
| II (Nat Comp Sci) | ⬜ 概念已设计 | ⬜ | ⬜ | ⬜ |
| III (Nat Mach Intell) | ✅ 已有草稿 | ✅ 定理可用 | ⏳ 等 GPU | ⬜ |
| IV (npj) | ✅ 已完成 | ✅ 就绪 | ⏳ 等 GPU/超算 | ⬜ |

## 期刊策略

| 期刊 | 如果被拒 → |
|------|------------|
| Nature | → Nature Computational Science |
| Nature Computational Science | → Nature Machine Intelligence |
| Nature Machine Intelligence | → JMLR / TMLR |
| npj Computational Materials | → Computational Materials Science |

---

*关联：[[../SCX/knowledge/05_决策/论文规划|论文规划]] · [[THEOREMS_UNIFIED]]*
