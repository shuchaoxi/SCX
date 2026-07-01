# SCX 附加材料清单

> 配合 paper/arxiv/README.md 论文索引使用

---

## 核心代码

| 文件 | 内容 | 行数 |
|------|------|------|
| `src/scx/yajie.py` | Yajie 审计核心 | — |
| `src/scx/spring.py` | Spring 自演化门控 | — |
| `src/scx/state/` | State Crystallization + 双层状态发现 | 10 文件 |
| `src/scx/expert/` | 专家注册、路由、冲突检测、可靠性估计 | 4 文件 |
| `src/scx/valuation/` | 噪声评分、自适应阈值、冗余检测、状态价值 | 8 文件 |
| `tests/` | 完整测试套件 | 12 文件 |

---

## 实验

| 目录 | 实验 | 状态 |
|------|------|------|
| `experiments/mlip_case/` | AlN MLIP SCX 双层审计 | ✅ 已运行 |
| `experiments/cifar/` | CIFAR-10/100 噪声检测 + 路由 | ✅ 已运行 |
| `experiments/synthetic/` | 合成数据验证 | ✅ |
| `scx-health/` | 医学影像 (HAM10000, MedMNIST) | ✅ |
| `scx-life/drug/` | 药物靶点筛选 | ⬜ 等硬件 |

---

## 证明与推导

| 目录 | 内容 |
|------|------|
| `theory/self_evolution/` | Spring 12 篇理论文件 + hostile review + 验证报告 |
| `theory/theorems/` | Theorem 1-4 的独立证明文件 |
| `theory/explorations/` | minimax 下界、聚类一致性、Bahadur-Rao 推导等 |
| `theory/self_evolution/ppe_rigorous_derivation.md` | Situs 1110 行严格推导 |
| `theory/self_evolution/situs_final_verification.md` | Situs 8/8 最终验证 |

---

## 审查记录

| 文件 | 内容 |
|------|------|
| `theory/self_evolution/final_review_jmlr.md` | JMLR 三理论论文审查 |
| `theory/self_evolution/final_review_nature.md` | Nature Comp Sci 应用论文审查 |
| `theory/self_evolution/hostile_review.md` | Situs hostile review |
| `theory/self_evolution/spring_hostile_review.md` | Spring hostile review |

---

## 关键声明

| 文件 | 内容 |
|------|------|
| `AUDIT_SWORD.md` | 审计之剑——不限军用，但可独立审计 |
| `BUSINESS_ARCHITECTURE.md` | 商业模式——Principal Maintainer + API 订阅 |
| `IP_NOTE.md` | 知识产权策略 |

---

## 开发记录

| 文件 | 内容 |
|------|------|
| `DEVELOPMENT_LOG.md` | 864 行开发日志（2026-05 到 2026-06） |
| `SCX_HISTORY.md` | 1027 行 SCX 思想进化史 |
| `paper/arxiv/ARCHITECTURE.md` | 四论文关系图 + SCX 分层架构 |

---

## 硬件规划

| 文件 | 内容 |
|------|------|
| `HARDWARE_SPEC.md` | 三档配置（¥800 / ¥45K / ¥100K） |
| `HARDWARE_ULTIMATE.md` | 终极限 ¥257K——7995WX + 4×5090 |
| `HARDWARE_CHECKLIST.md` | 全栈清单（网络、软件、安全） |

---

## 药物模块

| 文件 | 内容 |
|------|------|
| `drug-module/scripts/download_databases.py` | 1906 行，12 数据库下载管线 |
| `drug-module/scripts/screen_all_databases.py` | 全量 drug × target Yajie 审计 |
| `drug-module/RUN_GUIDE.md` | 一页纸运行指南 |

---

## 未包含（待补充）

| 项目 | 状态 |
|------|------|
| AlN v3 DFT 数据 (534 帧) | 未上传（大文件） |
| State Crystallization vs BPE 形式化对比 | 未完成 |
| 推测解码 (DSpark) 交叉验证 | 未完成 |
| 12 药物数据库原始数据 | 未下载 |
