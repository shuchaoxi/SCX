# Nature Submission — Supplementary Information

> 论文: "A Fundamental Impossibility in Data Quality"
> 目标: Nature Article (正文 ~2000 words) + SI (~60 pages)
> 策略: 正文 = 发现陈述（无 Lemma/Proof），SI = 全部数学

---

## SI 结构

| 章节 | 内容 | 来源 | 页数 |
|------|------|------|:--:|
| S1 | Theorem 1 完整证明 (噪声检测保证) | `theory/theorems/01_noise_detection_guarantee.md` | ~12 |
| S2 | Theorem 2 完整证明 (弱特征失效边界) | `theory/theorems/02_weak_feature_failure.md` | ~14 |
| S3 | Theorem 3 完整证明 (不可辨识性) | `theory/theorems/03_unidentifiability_theorem.md` | ~12 |
| S4 | Theorem 4' 精确常数 minimax 最优性 | `theory/explorations/exact_constant_minimax.md` + 4 lemma 文件 | ~20 |
| S5 | Theorem 5 聚类一致性证明 | `theory/explorations/cluster_consistency_v2.md` | ~10 |
| S6 | Proposition 6 Bootstrap 稳定性诊断 | `theory/explorations/feature_strength_via_stability.md` | ~8 |
| S7 | 实验细节 | AlN v3, CIFAR-10, DermaMNIST 配置 | ~6 |
| S8 | 数值验证 | `theory/explorations/numerical_verify.py` | ~4 |
| **总计** | | | **~86 页** |

## 与 paper1_nature 的关系

| | paper1_nature (已有) | paper_theory (新建) |
|---|---|---|
| 叙事 | "SCX 是一个好方法" | "数据质量有不可逾越的数学边界" |
| 核心 | 两层状态发现 + 多专家一致性 | 不可辨识定理 + 匹配上下界 |
| 定理 | 3 个 (支撑方法) | 6 个 (独立贡献) |
| 数学深度 | 中等 | **最深 (Bahadur-Rao + Chernoff-Stein)** |
| Nature 适配度 | 中 (方法论文) | **高 (基础发现)** |

**建议**: paper1_nature 转为 Nature Computational Science 投稿 (方法+实验)。
         paper_theory 投稿 Nature (理论发现)。
         两篇独立，互相引用。

## SI 写作优先级

1. **S4 (Thm 4')** — 最值钱，Nature 审稿人会先看这个
2. **S3 (Thm 3)** — 正文的核心 claim，证明必须无懈可击
3. **S1 (Thm 1)** — 方法的理论基础
4. **S2 (Thm 2)** — 边界条件
5. **S5-S6** — 算法基础
6. **S7-S8** — 实验 + 数值

## 投稿前检查清单

- [ ] 正文 <2500 words (Nature 硬限制)
- [ ] 正文无 Lemma/Proof 环境
- [ ] 所有数学在 SI 中有完整证明
- [ ] SI 交叉引用一致
- [ ] Cover Letter 写好（解释为什么这是基础发现而非方法改进）
- [ ] 正文 Figure 1: 不可辨识定理示意图（两个世界）
- [ ] 正文 Figure 2: 理论界 vs 经验界 (AlN v3)
- [ ] 正文 Figure 3: 特征强度相变图
- [ ] 补充 Figure: 数值验证 (M 增大时 F1 收敛)
- [ ] 数据/代码可用性声明
