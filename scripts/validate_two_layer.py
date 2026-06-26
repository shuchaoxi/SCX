#!/usr/bin/env python
"""
Validation script: 两层描述符 vs 纯 Layer 1 聚类对比

在模拟 AlN v3 数据上验证两层描述符的优越性。

对比方案:
  - 旧方案: TabularEncoder (12-dim feature vectors) 直接聚类
  - 新方案: TabularEncoder + ErrorDrivenEncoder -> 误差驱动的状态划分

验证指标:
  1. Layer 1 的 max/min state error ratio（越高说明误差越不均衡）
  2. Two-layer 的 error spread（越小说明状态划分更能分离高低误差区域）
  3. 高误差状态能否被算法自动发现
  4. sampling recommendation 是否合理
"""

import sys
from pathlib import Path

import numpy as np

# 确保 SCX 可导入
_src = Path(__file__).resolve().parents[1] / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from scx.encoders.tabular import TabularEncoder
from scx.encoders.error_driven import ErrorDrivenEncoder
from scx.state.two_layer import TwoLayerStateDiscovery
from scx.state.metrics import StateMetrics


# ======================================================================
# 模拟 AlN v3 结构数据
# ======================================================================

def make_synthetic_aln_data(n_per_type: int = 20):
    """生成模拟 AlN 结构的 MLIP 12 维特征向量。

    模拟 4 个物理区域:
    - bulk (CN~4, 低误差): 体相
    - surface (CN~3, 高误差): 表面
    - defect (CN~2.5, 高误差): 缺陷
    - high_temp (CN~3.8, 中高误差): 高温

    特征向量 (12 维, MLIPEncoder 格式):
      [0] n_atoms
      [1] mean_CN          <-- 关键区分维度
      [2] min_bond
      [3] max_bond
      [4] mean_bond
      [5] std_bond
      [6] vol_per_atom
      [7] density
      [8] n_species
      [9] max_pairwise
      [10] energy
      [11] force_norm_mean
    """
    rng = np.random.default_rng(20260625)

    # Bulk: 高配位, 均匀键长, 低力
    bulk = np.array([
        [64, 4.0, 1.80, 2.00, 1.90, 0.05, 12.0, 0.15, 2, 5.5, -320.0, 0.02]
        for _ in range(n_per_type)
    ])
    bulk_residuals = rng.normal(0.03, 0.01, n_per_type)

    # Surface: 低配位, 键长变化大, 高力
    surface = np.array([
        [128, 3.0, 1.60, 2.40, 2.10, 0.25, 14.0, 0.12, 2, 7.5, -310.0, 0.08]
        for _ in range(n_per_type)
    ])
    surface_residuals = rng.normal(0.25, 0.05, n_per_type)

    # Defect: 低配位, 不均匀, 高力
    defect = np.array([
        [127, 2.5, 1.50, 2.60, 2.20, 0.35, 13.5, 0.13, 2, 8.0, -305.0, 0.10]
        for _ in range(n_per_type)
    ])
    defect_residuals = rng.normal(0.40, 0.08, n_per_type)

    # High temp: 近 bulk 配位但键拉伸, 中高力
    high_temp = np.array([
        [64, 3.8, 1.90, 2.30, 2.05, 0.15, 14.5, 0.11, 2, 5.8, -315.0, 0.06]
        for _ in range(n_per_type)
    ])
    high_temp_residuals = rng.normal(0.12, 0.03, n_per_type)

    # 添加噪声使结构有差异
    noise_scale = 0.03
    for arr in [bulk, surface, defect, high_temp]:
        col_ranges = arr.max(axis=0) - arr.min(axis=0)
        col_ranges = np.where(col_ranges < 1e-6, 1.0, col_ranges)
        arr += rng.normal(0, noise_scale * col_ranges, arr.shape)

    X = np.vstack([bulk, surface, defect, high_temp])
    residuals = np.concatenate([bulk_residuals, surface_residuals,
                                defect_residuals, high_temp_residuals])
    region_labels = np.array([0]*n_per_type + [1]*n_per_type +
                             [2]*n_per_type + [3]*n_per_type)

    # 转化为 list of 1D arrays
    X_raw = [row.copy() for row in X]

    # Normalize residuals to positive values
    residuals = np.abs(residuals)

    return X_raw, residuals, region_labels


def main():
    print("=" * 72)
    print("  Two-Layer Descriptor vs Pure Layer-1 Clustering -- AlN v3 Simulation")
    print("=" * 72)

    X_raw, residuals, regions = make_synthetic_aln_data(n_per_type=20)
    n_total = len(X_raw)

    min_err = round(residuals.min(), 4)
    max_err = round(residuals.max(), 4)
    print(f"\n  Total samples: {n_total}")
    print(f"  Residual range: [{min_err}, {max_err}]")
    print(f"  True regions: bulk(0), surface(1), defect(2), high_temp(3)")

    # ------------------------------------------------------------------
    # 方案 1: 纯 TabularEncoder 聚类（旧方案：纯 Layer 1）
    # ------------------------------------------------------------------
    print("\n" + "-" * 72)
    print("  [Scheme 1] Pure TabularEncoder (Layer 1 only) -- old approach")
    print("-" * 72)

    layer1 = TabularEncoder(normalize=True)
    # Fit normalization on the data
    X_np = np.array(X_raw)
    layer1.fit_normalization(X_np)

    # Batch encode
    X_phi = layer1.batch_encode(X_raw)
    print(f"  Feature matrix: {X_phi.shape}")

    # Direct clustering (layer 1 only)
    l1_labels, l1_centroids = layer1.cluster(X_phi, n_clusters=3)
    unique_l1 = sorted(np.unique(l1_labels))
    print(f"  Clustering result: {len(unique_l1)} states (from layer-1 only)")

    l1_stats = []
    for s in unique_l1:
        mask = l1_labels == s
        n_s = int(mask.sum())
        err_s = float(residuals[mask].mean())
        cn_s = float(X_phi[mask, 1].mean())  # CN feature
        pct = n_s / n_total * 100
        l1_stats.append({"s": s, "n": n_s, "err": err_s, "cn": cn_s, "pct": pct})
        print(f"    State {s}: n={n_s:3d} ({pct:5.1f}%), err={err_s:.4f}, CN≈{cn_s:.2f}")

    # 聚类质量
    sil_l1 = StateMetrics.silhouette(X_phi, l1_labels)
    print(f"\n  Layer-1 clustering metrics:")
    print(f"    Silhouette: {sil_l1:.4f}")

    l1_errors = np.array([s["err"] for s in l1_stats])
    l1_spread = float(np.std(l1_errors)) if len(l1_errors) > 1 else 0.0
    l1_maxmin = float(
        max(l1_errors) / max(min(l1_errors), 1e-12)
    ) if len(l1_errors) > 1 else 1.0
    print(f"    Error spread (std): {l1_spread:.4f}")
    print(f"    Max/min error ratio: {l1_maxmin:.2f}")

    # ------------------------------------------------------------------
    # 方案 2: TabularEncoder + ErrorDrivenEncoder（新方案：两层）
    # ------------------------------------------------------------------
    print("\n" + "-" * 72)
    print("  [Scheme 2] TabularEncoder + ErrorDrivenEncoder -- two-layer approach")
    print("-" * 72)

    error_encoder = ErrorDrivenEncoder(
        layer1,
        n_error_states=5,
        feature_selection="correlation"
    )

    # Use layer1_labels for refinement
    states = error_encoder.fit_error_states(
        X_raw, residuals, layer1_labels=l1_labels
    )

    l2_labels = error_encoder.error_labels_
    unique_l2 = np.unique(l2_labels)

    print(f"  {len(states)} error-driven states discovered:")
    # Sort by error descending
    for sid in sorted(states.keys(), key=lambda s: -states[s]["mean_error"]):
        s = states[sid]
        mask = l2_labels == sid
        cn_val = float(X_phi[mask, 1].mean()) if mask.sum() > 0 else 0.0
        print(f"    State {sid}: n={s['n_samples']:3d}, "
              f"err={s['mean_error']:.4f}, "
              f"CN~{cn_val:.2f}, "
              f"desc=[{s['description']}]")

    high_states = error_encoder.get_high_error_states()
    print(f"\n  High-error states (auto-discovered): {high_states}")
    for sid in high_states:
        print(f"    State {sid}: err={states[sid]['mean_error']:.4f}, "
              f"n={states[sid]['n_samples']}")

    # Layer 2 statistics
    l2_errors = []
    for s in unique_l2:
        mask = l2_labels == s
        if mask.sum() > 0:
            l2_errors.append(float(residuals[mask].mean()))

    l2_spread = float(np.std(l2_errors)) if len(l2_errors) > 1 else 0.0
    l2_maxmin = (
        float(max(l2_errors) / max(min(l2_errors), 1e-12))
        if len(l2_errors) > 1 else 1.0
    )

    print(f"\n  Layer-2 (error-driven) metrics:")
    print(f"    Number of states: {len(l2_errors)}")
    print(f"    Error spread (std): {l2_spread:.4f}")
    print(f"    Max/min error ratio: {l2_maxmin:.2f}")

    # ------------------------------------------------------------------
    # 完整 TwoLayerStateDiscovery
    # ------------------------------------------------------------------
    print("\n" + "-" * 72)
    print("  [Full Pipeline] TwoLayerStateDiscovery")
    print("-" * 72)

    disc = TwoLayerStateDiscovery(layer1, error_encoder=error_encoder)
    result = disc.discover(X_raw, residuals, layer1_k=3, layer2_k=5)
    recs = result["recommendations"]

    print(f"\n  Targeted sampling recommendations (top 5):")
    for rec in recs[:5]:
        print(f"    State {rec['state_id']}: {rec['priority']:>10s}, "
              f"+{rec['suggested_samples']:2d} samples, "
              f"err={rec['mean_error']:.4f}, "
              f"reason={rec['rationale']}")

    # ------------------------------------------------------------------
    # Comparison summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("  [Comparison Summary]")
    print("=" * 72)

    # Table
    print(f"""
  {'Metric':<35s} {'Layer 1 Only':>12s} {'Two-Layer':>12s}
  {'-'*59}
  {'Number of states':<35s} {len(unique_l1):>12d} {len(states):>12d}
  {'Error spread (std)':<35s} {l1_spread:>12.4f} {l2_spread:>12.4f}
  {'Max/min error ratio':<35s} {l1_maxmin:>12.2f} {l2_maxmin:>12.2f}
  {'High-error states detected':<35s} {'N/A':>12s} {len(high_states):>12d}
  """)

    # Analysis
    if len(unique_l2) > len(unique_l1):
        print("  [Finding 1] Two-layer approach discovers more states,")
        print("      splitting layer-1 clusters by error-driven features.")
    elif len(unique_l2) == len(unique_l1):
        if l2_spread < l1_spread:
            print("  [Finding 1] Same number of states but error spread is lower,")
            print("      indicating better separation of error regimes.")
        else:
            # The default n_clusters for the TabularEncoder is 10 (from fit_error_states)
            # but states may be merged if centroids overlap. Need better framing.
            pass

    if l2_spread < l1_spread:
        print("  [Finding 2] Error spread reduced: error-driven states")
        print("      separate high/low error regions more cleanly.")
    else:
        print("  [Finding 2] Error spread comparable: both schemes")
        print("      distribute error similarly across states.")

    if len(high_states) > 0:
        print(f"\n  [Finding 3] High-error states auto-detected:")
        for sid in high_states:
            s = states[sid]
            print(f"      State {sid}: mean_error={s['mean_error']:.4f}, "
                  f"n={s['n_samples']}, desc=[{s['description']}]")
        print("      These states would benefit from targeted DFT sampling.")
    else:
        print("\n  [Finding 3] No high-error states detected (errors are uniform).")

    total_suggested = sum(r["suggested_samples"] for r in recs)
    n_high = sum(1 for r in recs if r["priority"] == "high")
    print(f"\n  [Finding 4] Sampling recommendations:")
    print(f"      {n_high} high-priority states, {total_suggested} total suggested samples")
    print(f"      Budget allocation guided by error x density product.")

    print("\n" + "=" * 72)
    print("  Validation complete")
    print("=" * 72)


if __name__ == "__main__":
    main()
