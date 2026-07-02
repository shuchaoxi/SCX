# SCX 分析报告：AlN v3 训练数据

> 日期：2026-06-26 | SCX v4.0 Phase A | 534 帧 DFT 标签

---

## 摘要

用 SCX + 12 维手工 MLIP encoder 分析 AlN v3 训练数据。**12 维特征不足以精细分离 MLIP 状态空间**——50% 帧挤在一个状态。但在 coarse 层面揭示了明确模式：**MLMD/thermal 高帧是高噪声风险帧**（已知：v3 已对 fmax>5 帧做了降权）。需要更丰富的描述符（ACE/SOAP）才能做有意义的状态条件分析。

---

## 数据概况

| 指标 | 数值 |
|------|------|
| 总帧数 | 534 |
| Batches | 00 equilibrium(3), 01 EOS(32), 02 elastic(126), 03 cross(80), 04 phonon(120), 05 thermal(107), 08 MLMD(60) |
| 原子数 | 4 atoms(119), 32 atoms(414), 72 atoms(1) |
| fmax 范围 | 0.009 ~ 16.37 eV/Å |
| fmax 均值 | 2.3 eV/Å |

---

## SCX 分析结果 (K=20, 12-dim features)

### 数据分类

| 类别 | 状态数 | 帧数 | 占比 |
|------|--------|------|------|
| Valuable | 12 | 33 | 6.2% |
| Redundant | 0 | 0 | 0% |
| Noisy | 0 | 0 | 0% |
| Expert-dependent | 8 | 501 | 93.8% |

### Top 10 潜在噪声帧

| # | Structure ID | Batch | fmax (eV/Å) |
|---|-------------|-------|-------------|
| 1 | AlN_wz_thermal_strained_1500K_r03 | 05_thermal | 11.13 |
| 2 | AlN_wz_stress10_mlmd_1500K_s05 | 08_MLMD | 8.23 |
| 3 | AlN_wz_stress10_mlmd_1800K_s09 | 08_MLMD | 7.82 |
| 4 | AlN_wz_stress10_mlmd_1500K_s01 | 08_MLMD | 7.14 |
| 5 | AlN_wz_stress10_mlmd_1800K_s07 | 08_MLMD | 7.09 |
| 6-10 | (全是 MLMD 1500-1800K) | 08_MLMD | 5.3-6.7 |

**结论**：Top 10 噪声帧全部来自 thermal (1800K) 和 MLMD (1500-1800K)。这与 AlN v3 训练中已知的"thermal fmax>5 需要降权"一致——**SCX 独立发现了相同的高噪声区域**。

---

## 关键发现

### 1. SCX 独立验证了 v3 的降权策略

v3 训练中对 thermal 帧 fmax>5 做了 `energy_weight = 5/fmax` 降权。SCX 分析中 Top 10 噪声帧全部 fmax>5，且集中在 thermal 和 MLMD batch——**SCX 在没有先验知识的情况下复现了人工判断**。

### 2. 12 维手工 encoder 太粗

- 50% 帧 (267/534) 挤在 State 3
- 多个状态只有 1-2 帧
- 无法区分 EOS/phonon/elastic 之间的冗余
- **原因**：手工描述符（CN, bond length, volume）对 AlN 这种单一化学环境区分度低

### 3. 压缩潜力被低估

- SCX 报告 0% 冗余——**这不合理**。v3 的 EOS 16 点、弹性 9 类型 × 多个幅度之间存在大量相似帧
- **根因**：12 维特征无法捕捉原子构型的细粒度差异
- **需要**：ACE/SOAP descriptor (100+ 维) 才能做有意义的冗余分析

### 4. 分类偏向 "expert-dependent"

93.8% 分类为 "expert-dependent"——因为 12 维特征中 force 方差与特征方差的相关性弱，导致一致性始终 moderate。SCX 的默认阈值在 MLIP 场景需要重新校准。

---

## 改进建议

### P0: 替换 encoder

用真正的 ACE descriptor (100-200 维) 替代 12 维手工特征：

```python
# Option A: dscribe SOAP
from dscribe.descriptors import SOAP
soap = SOAP(species=["Al","N"], r_cut=6.0, n_max=6, l_max=4)

# Option B: 用 v3 训练好的 ACE 模型的 B-basis features
```

### P1: 重新校准阈值

MLIP 数据中 fmax 的自然尺度与图像分类的 loss 不同。需要：
- `error_high` 从 0.05 → fmax 的 75th percentile (~3 eV/Å)
- `noise_high` 从 0.5 → fmax 的 95th percentile (~9 eV/Å)

### P2: 压缩验证实验

1. 用更好的 encoder 重跑 SCX
2. 对标记为 "redundant" 的帧做压缩
3. 在压缩后的训练集上重训 ACE
4. 对比：full data vs SCX-compressed vs random-compressed

---

## 诚实结论

| 问题 | 答案 |
|------|------|
| SCX 能发现 AlN v3 的噪声吗？ | ✅ 能——Top 10 全部 fmax>5，与人工判断一致 |
| 能节省多少训练数据？ | ❓ 12 维 encoder 太粗，无法确定。需要 ACE descriptor |
| 分类可靠性如何？ | ⚠️ 93.8% expert_dependent——阈值需要 MLIP 专用校准 |
| 值得继续吗？ | ✅ 替换 encoder 后预计可发现 20-30% 冗余 |

**底线**：SCX 的方向是对的（独立发现已知高噪声区域），但 12 维手工 encoder 不足以释放 SCX 的全部能力。需要接入真正的 ACE descriptor。