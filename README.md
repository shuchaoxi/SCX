# SCX — State-Conditioned eXpertise

> 一个暑假。178 commits。75 theorems。27 papers。从 EGP 规范固定到博弈论非扩散均衡。

---

## 这是什么

SCX 是一个数学框架，用多专家共识检测数据中的标签噪声。核心发现：**老实人定理 (The Honest Person Theorem)**——噪声和困难在观测上不可区分。

---

## 📚 论文目录（27 篇）

### 核心理论（5 篇，严格形式化）

| # | 论文 | 目录 | 核心内容 | 定理 | 证明 |
|---|------|------|----------|------|------|
| 1 | **scx_theory** | `paper/arxiv/scx_theory/` | Thm 1-4：噪声检测→极小极大最优 | 5 | ✅ |
| 2 | **taxonomic_nn** | `paper/arxiv/taxonomic_nn/` | ML推导 + **老实人定理**（旗舰） | 15 | 22 |
| 3 | **spring_config** | `paper/arxiv/spring_config/` | 自演化守门人 + Lyapunov 收敛 | 13 | 29 |
| 4 | **situs_theory** | `paper/arxiv/situs_theory/` | 物理位置编码（Situs） | 4 | ✅ |
| 5 | **yajie_protocol** | `paper/arxiv/yajie_protocol/` | 博弈论：NPE + AAE + 审计之剑 | 9 | 14 |

### 应用与方法（6 篇）

| # | 论文 | 目录 | 核心内容 |
|---|------|------|----------|
| 6 | **scx_curation** | `paper/arxiv/scx_curation/` | 数据策展方法 |
| 7 | **scx_method** | `paper/arxiv/scx_method/` | 实证锚定 + Cercis Score |
| 8 | **scx_review** | `paper/arxiv/scx_review/` | 跨域综述 |
| 9 | **scx_llm** | `paper/arxiv/scx_llm/` | SCX 与 LLM |
| 10 | **egp_merging** | `paper/arxiv/egp_merging/` | ACE 势函数合并 |
| 11 | **situs_applications** | `paper/arxiv/situs_applications/` | 12 科学场景 |

### 独立定理（13 篇，全部形式化）

| # | 缩写 | 文件 | 内容 | 定理 |
|---|------|------|------|------|
| 12 | thm5 | `theorems/theorem5_active_learning.tex` | 主动学习 | 3 |
| 13 | thm6 | `theorems/theorem6_protocol_game.tex` | 协议博弈 | 3 |
| 14 | thm7 | `theorems/theorem7_cross_domain.tex` | 跨域迁移 | 2 |
| 15 | cd | `theorems/theorem_cd_causal.tex` | 因果发现 | 3 |
| 16 | fa | `theorems/theorem_fa_federated.tex` | 联邦审计 | 2 |
| 17 | ar | `theorems/theorem_ar_adversarial.tex` | 对抗鲁棒 | 2 |
| 18 | ts | `theorems/theorem_ts_temporal.tex` | 时序状态 | 3 |
| 19 | hc | `theorems/theorem_hc_human.tex` | 人类协作 | 3 |
| 20 | q | `theorems/theorem_q_quantum.tex` | 量子扩展 | 2 |
| 21 | ae | `theorems/theorem_ae_entropy.tex` | 熵界 | 4 |
| 22 | ac | `theorems/theorem_ac_complexity.tex` | 复杂度 | 3 |
| 23 | ra | `theorems/theorem_ra_recursive.tex` | 递归自指 | 3 |
| 24 | aa | `theorems/theorem_aa_alignment.tex` | 对齐 | 7 |

### 元论文（3 篇）

| # | 论文 | 文件 |
|---|------|------|
| 25 | **SCX_MANIFESTO** | `paper/arxiv/meta/SCX_MANIFESTO.tex` |
| 26 | **SCX_HISTORY** | `paper/arxiv/meta/SCX_HISTORY.tex` |
| 27 | **human_future** | `paper/arxiv/yajie_protocol/human_future.tex` |

---

## 🧭 快速导航

| 想看什么 | 去这里 |
|----------|--------|
| 所有论文 PDF | `paper/arxiv/` 各子目录 `main.pdf` |
| 旗舰定理（2页自包含） | `paper/arxiv/taxonomic_nn/theorem3_short.tex` |
| 定理全景（17方向） | `theory/SCX_Undiscovered_Theorems.md` |
| 框架宣言 | `paper/arxiv/meta/SCX_MANIFESTO.tex` |
| 完整故事 | `docs/SCX_HISTORY.md` |
| 开发日志 | `docs/DEVELOPMENT_LOG.md` |
| 审计之剑 | `docs/AUDIT_SWORD.md` |
| 旧版草稿 | `paper/archive/` |

---

## 💻 代码

```
src/scx/       核心实现（yajie.py, spring.py, state/, expert/, valuation/）
experiments/   CIFAR + MLIP 实验
tests/         测试套件
drug-module/   药物数据库筛选管线
```

---

## 📂 项目结构

```
paper/arxiv/    ← 27篇论文（arXiv 投递版）
paper/archive/  ← 旧版草稿
theory/         ← 定理 + 证明 + hostile review
docs/           ← 项目文档 + 开发日志
src/scx/        ← 核心代码
experiments/    ← 实验数据
knowledge/      ← Obsidian 知识库
```

---

## 怎么读

1. 先读 `paper/arxiv/meta/SCX_MANIFESTO.tex`（10分钟）—— 知道我们在做什么
2. 再读 `paper/arxiv/taxonomic_nn/theorem3_short.tex`（15分钟）—— 理解核心定理
3. 深入：`paper/arxiv/scx_theory/` → `spring_config/` → `yajie_protocol/`
4. 想用代码：`src/scx/`

---

## 作者

SCX Research Group. 2026.

所有论文署名 SCX Research Group，不包含学校或个人信息。详见 `docs/AUDIT_SWORD.md`。
