# SCX Theory -- Theorems

本目录存放 SCX 框架的核心定理：

| 文件 | 内容 | 状态 |
|------|------|------|
| `01_noise_detection_guarantee.md` | Theorem 1: 多专家一致性噪声检测保证 | 完整 |
| `02_weak_feature_failure.md` | Theorem 2: 弱特征失效下界 | 完整 |
| `03_unidentifiability_theorem.md` | Theorem 3: 噪声与可学习困难的不可识别性 | 完整 (2026-06-27) |

**三个定理的逻辑闭环**:
- **Theorem 1 (正命题)**: 在 A1-A6 下, SCX 能检测噪声
- **Theorem 2 (边界命题)**: 当特征弱时, SCX 退化为损失基线
- **Theorem 3 (必要性命题)**: 无 A1-A6 时, 噪声与困难根本不可区分 -> A1-A6 非任意假设, 而是打破不可识别性的最小条件
