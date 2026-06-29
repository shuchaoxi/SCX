# SCX — State-Conditioned eXpertise

> 一个暑假。178 commits。36 theorems。29 papers。从 EGP 规范固定到 SCX 不确定性原理。

---

## 这是什么

SCX 是一个数学框架，用多专家共识检测数据中的标签噪声。核心发现：**噪声和困难在观测上不可区分**（Theorem 3——SCX 的"不确定性原理"）。

---

## 快速导航

| 你想看什么 | 去这里 |
|-----------|--------|
| **所有论文列表** | `paper/arxiv/README.md` — 12+ 篇论文，每篇一句话 |
| **核心定理（2 页）** | `paper/arxiv/taxonomic_nn/theorem3_short.tex` — 自包含 |
| **框架宣言** | `paper/arxiv/SCX_MANIFESTO.tex` |
| **定理全景** | `theory/SCX_Undiscovered_Theorems.md` — 17 个定理方向 |
| **完整故事** | `SCX_HISTORY.md` — 从 EGP 到量子审计 |
| **开发日志** | `DEVELOPMENT_LOG.md` |
| **审计之剑** | `AUDIT_SWORD.md` — 不限军用，但可审计 |

---

## 论文结构

```
paper/arxiv/
├── scx_theory/          Theorem 1-4（静态审计）
├── situs_theory/        物理位置编码
├── spring_config/       自演化门控收敛
├── situs_applications/  12 科学场景
├── taxonomic_nn/        ML 现象推导 + Theorem 3
├── scx_llm/             SCX 与 LLM
├── scx_curation/        数据策展方法
├── scx_method/          实证锚定
├── scx_review/          跨域综述
├── egp_merging/         ACE 势函数合并
├── yajie_protocol/      博弈论 + 经济地理学
├── theorem5-7 + cd/fa/ar/ts/hc + q/ae/ac/ra/aa  定理论文
├── SCX_MANIFESTO.tex    统一宣言
├── SCX_HISTORY.tex      思想进化史
└── human_future.tex     人类未来
```

---

## 代码

```
src/scx/        核心实现（yajie.py, spring.py, state/, expert/）
experiments/    CIFAR + MLIP 实验
tests/          测试套件
drug-module/    药物数据库筛选管线
```

---

## 怎么读

1. 先读 `SCX_MANIFESTO.tex`（10 分钟）——知道我们在做什么
2. 再读 `theorem3_short.tex`（15 分钟）——理解核心定理
3. 想深入看 `scx_theory/` 和 `scx_review/`
4. 想用代码看 `src/scx/`

---

## 作者

SCX Research Group. 2026.

所有论文署名 SCX Research Group，不包含学校或个人信息。详见 `AUDIT_SWORD.md`。
