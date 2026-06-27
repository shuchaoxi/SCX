# Theory Paper — 正文 + 附加材料

> 目标期刊: Annals of Statistics → IEEE Trans. Information Theory → JMLR
> 论文类型: 纯数学理论（6 定理 + 1 命题）
> 状态: 框架已就绪，正文写作待启动

## 文件结构

```
paper_theory/
├── PAPER_FRAMEWORK.md          # 本框架文档（论文蓝图）
├── README.md                   # 本文件
├── main/                       # 正文 (30-40 页)
│   ├── main.tex                # 主 LaTeX 文件
│   ├── sec1_intro.tex          # Introduction
│   ├── sec2_formulation.tex    # Problem Formulation
│   ├── sec3_main_results.tex   # Main Results (§3.1-3.4)
│   ├── sec4_algorithms.tex     # Algorithmic Foundation (§4.1-4.2)
│   ├── sec5_connections.tex    # Connections to Existing Theory
│   ├── sec6_numerical.tex      # Numerical Validation
│   └── sec7_discussion.tex     # Discussion
└── supplementary/              # 补充材料 (60-80 页)
    ├── supp.tex                # 主 SI 文件
    ├── S1_thm1_full_proof.tex  # Theorem 1 完整证明
    ├── S2_thm2_full_proof.tex  # Theorem 2 完整证明
    ├── S3_thm3_full_proof.tex  # Theorem 3 完整证明
    ├── S4_minimax_proof.tex    # Theorem 4 Minimax 下界
    ├── S5_cluster_proof.tex    # Theorem 5 聚类一致性
    ├── S6_stability.tex        # Proposition 6 Bootstrap 稳定性
    └── S7_extra_experiments.tex # 额外数值实验
```

## 现有材料映射

所有证明已经写好（Markdown），需要转换为 LaTeX：

| SI 章节 | 源 Markdown 文件 | 行数 | 状态 |
|---------|-----------------|:--:|:--:|
| S1 | `../../theory/theorems/01_noise_detection_guarantee.md` | 519 | ✅ |
| S2 | `../../theory/theorems/02_weak_feature_failure.md` | 633 | ✅ |
| S3 | `../../theory/theorems/03_unidentifiability_theorem.md` | 540 | ✅ |
| S4 | `../../theory/explorations/minimax_lower_bound_v2.md` | 1023 | ✅ |
| S5 | `../../theory/explorations/cluster_consistency_v2.md` | 748 | ✅ |
| S6 | `../../theory/explorations/feature_strength_via_stability.md` | 614 | ✅ |

## 定理编号与论文标签

| 论文标签 | 内容 | 内部名称 |
|:--:|------|----------|
| Theorem 1 | 噪声检测保证 (F1 下界, 指数收敛) | Noise Detection Guarantee |
| Theorem 2 | 弱特征失效边界 (F1 上界, δ→0 退化) | Weak Feature Boundary |
| Theorem 3 | 噪声-困难不可辨识性 (无假设→不可能) | Unidentifiability |
| Theorem 4 | Minimax 速率最优性 (匹配下界) | Rate Optimality |
| Theorem 5 | 聚类一致性 (k-means 状态发现) | Cluster Consistency |
| Proposition 6 | Bootstrap ARI 稳定性诊断 | Stability Diagnostic |
