"""
TwoLayerStateDiscovery — 两层状态发现。

核心原则：
> 研究人员说"我要做 AlGaN, bulk/surface/defect, 300-1800K"
> 算法说"在 CN<3.5 + local_strain>3% 的区域，误差是平均的 8 倍，
>   这个区域应该成为一个独立状态"

架构：
  Layer 1: 人提供的粗粒度领域知识（通过 SCXStateEncoder）
  Layer 2: 算法从误差分布中自动发现的细粒度状态（通过 ErrorDrivenEncoder）

工作流：
  1. Layer 1 粗聚类（人定义的领域知识）
  2. 训练模型（或使用 pretrained predictions）
  3. 计算 residuals
  4. Layer 2 在每个 Layer 1 状态内发现 error-driven substates
  5. 输出两层级联的状态划分 + 定向补样本建议

Example
-------
>>> import numpy as np
>>> from scx.encoders.mlip import MLIPEncoder
>>> from scx.encoders.error_driven import ErrorDrivenEncoder
>>> from scx.state.two_layer import TwoLayerStateDiscovery
>>> layer1 = MLIPEncoder(species=["Al", "N"])
>>> discovery = TwoLayerStateDiscovery(layer1)
>>> # 假设 100 个 Atoms 结构
>>> atoms_list = ...
>>> residuals = np.random.rand(len(atoms_list))
>>> result = discovery.discover(atoms_list, residuals, layer1_k=3, layer2_k=5)
>>> print(result['recommendations'][:3])
"""
from __future__ import annotations

from typing import Any

import numpy as np

from scx.encoders.base import SCXStateEncoder
from scx.encoders.error_driven import ErrorDrivenEncoder
from scx.state.discovery import StateDiscovery


class TwoLayerStateDiscovery:
    """两层状态发现。

    Layer 1: 人提供的粗粒度领域知识
    Layer 2: 算法从误差分布中自动发现的细粒度状态

    Parameters
    ----------
    layer1_encoder : SCXStateEncoder
        第一层编码器（人手选，如 MLIPEncoder）
    error_encoder : ErrorDrivenEncoder | None
        第二层误差驱动编码器；若为 None 则自动创建
    """

    def __init__(
        self,
        layer1_encoder: SCXStateEncoder,
        error_encoder: ErrorDrivenEncoder | None = None,
    ) -> None:
        self.layer1 = layer1_encoder
        self.layer2 = error_encoder or ErrorDrivenEncoder(layer1_encoder)

        # Cached results
        self._X_phi: np.ndarray | None = None
        self._layer1_labels: np.ndarray | None = None
        self._layer2_labels: np.ndarray | None = None
        self._layer1_discovery: StateDiscovery | None = None

    # ------------------------------------------------------------------
    # Main discovery pipeline
    # ------------------------------------------------------------------

    def discover(
        self,
        X_raw: list[Any],
        residuals: np.ndarray,
        layer1_k: int = 5,
        layer2_k: int = 10,
        use_layer1_clusters: bool = True,
        **discovery_kwargs,
    ) -> dict[str, Any]:
        """完整的两层发现流程。

        Parameters
        ----------
        X_raw : list[Any]
            原始输入样本列表
        residuals : np.ndarray, shape (N,)
            每个样本的误差值
        layer1_k : int
            Layer 1 聚类数（默认 5）
        layer2_k : int
            Layer 2 每个 error state 的最多子状态数（默认 10）
        use_layer1_clusters : bool
            是否将 layer1 聚类标签传给 layer2 做细化（默认 True）
        **discovery_kwargs
            额外参数传递给 StateDiscovery（如 method, random_state）

        Returns
        -------
        result : dict
            {
                'layer1_labels': np.ndarray (N,),
                'layer2_labels': np.ndarray (N,),
                'error_states': dict,      # 算法发现的高误差状态
                'layer1_states': dict,     # 人定义的状态摘要
                'recommendations': list,   # 定向补样本建议
                'layer1_metrics': dict,    # Layer 1 聚类质量
                'layer2_summary': dict,    # Layer 2 摘要
            }
        """
        n_samples = len(X_raw)
        residuals = np.asarray(residuals, dtype=np.float64).ravel()

        # --- Layer 1: 编码 + 粗聚类 ---
        X_phi = self.layer1.batch_encode(X_raw)  # (N, d)
        self._X_phi = X_phi

        # Use StateDiscovery for layer 1
        method = discovery_kwargs.pop("method", "kmeans")
        rs = discovery_kwargs.pop("random_state", 42)
        sd = StateDiscovery(
            method=method,
            n_states=layer1_k,
            random_state=rs,
            **discovery_kwargs,
        )
        layer1_labels = sd.fit_predict(X_phi)
        self._layer1_labels = layer1_labels
        self._layer1_discovery = sd

        # Build layer1 state descriptions
        layer1_states: dict[int, dict[str, Any]] = {}
        for s in range(layer1_k):
            mask = layer1_labels == s
            if mask.sum() == 0:
                continue
            layer1_states[int(s)] = {
                "n_samples": int(mask.sum()),
                "proportion": float(mask.sum() / max(n_samples, 1)),
                "mean_residual": float(residuals[mask].mean()),
                "centroid": X_phi[mask].mean(axis=0),
            }

        # --- Layer 2: 误差驱动的精细化 ---
        layer2_labels = None
        if use_layer1_clusters and layer1_k > 1:
            error_states = self.layer2.fit_error_states(
                X_raw, residuals, layer1_labels=layer1_labels
            )
        else:
            error_states = self.layer2.fit_error_states(
                X_raw, residuals, layer1_labels=None
            )

        # Build layer2 labels: map each sample to its error state
        if hasattr(self.layer2, "error_labels_") and self.layer2.error_labels_ is not None:
            layer2_labels = self.layer2.error_labels_.copy()
        else:
            layer2_labels = np.zeros(n_samples, dtype=int)

        self._layer2_labels = layer2_labels

        # --- Generate recommendations ---
        recommendations = self.recommend_sampling(
            error_states, budget=min(100, max(10, n_samples // 5))
        )

        # --- Layer 1 metrics ---
        layer1_metrics = self._compute_layer1_metrics(X_phi, layer1_labels)

        # --- Layer 2 summary ---
        layer2_summary = self.layer2.summary()

        return {
            "layer1_labels": layer1_labels,
            "layer2_labels": layer2_labels,
            "error_states": error_states,
            "layer1_states": layer1_states,
            "recommendations": recommendations,
            "layer1_metrics": layer1_metrics,
            "layer2_summary": layer2_summary,
        }

    # ------------------------------------------------------------------
    # Sampling recommendations
    # ------------------------------------------------------------------

    def recommend_sampling(
        self,
        error_states: dict[int, dict[str, Any]],
        budget: int = 100,
        min_samples_per_state: int = 3,
    ) -> list[dict[str, Any]]:
        """基于 error state 的定向补样本建议。

        策略：
        - 高误差 + 高密度 = 高优先级（补样本可以快速改善模型）
        - 高误差 + 低密度 = 中优先级（可能是稀疏区域，需验证）
        - 低误差 = 低优先级
        - 极高误差 + 极少样本 = 检查是否为噪声

        Parameters
        ----------
        error_states : dict
            fit_error_states 的输出
        budget : int
            建议的总补样本数
        min_samples_per_state : int
            每个状态最少建议数（防止忽略小簇）

        Returns
        -------
        list[dict]
            按优先级从高到低排列的建议列表：
            [
                {
                    'state_id': 0,
                    'priority': 'high',
                    'mean_error': 0.15,
                    'n_samples': 30,
                    'suggested_samples': 20,
                    'description': 'dim_3=0.75, err=0.15',
                    'rationale': 'high error (0.15) + high density (30 samples)',
                },
                ...
            ]
        """
        if not error_states:
            return []

        errors = np.array([s["mean_error"] for s in error_states.values()])
        n_samps = np.array(
            [s["n_samples"] for s in error_states.values()]
        )
        err_mean, err_std = float(errors.mean()), float(errors.std())

        recommendations = []
        total_priority = 0.0
        priorities: dict[int, float] = {}

        for sid, state in error_states.items():
            n_s = state["n_samples"]
            e_s = state["mean_error"]

            # Priority score: error * sqrt(density)
            density_factor = np.sqrt(n_s / max(n_samps.sum(), 1))
            priority = e_s * (1.0 + density_factor)

            if e_s > err_mean + 1.5 * err_std and n_s >= min_samples_per_state:
                priority *= 2.0  # high-error, non-noise
            elif e_s < err_mean - 0.5 * err_std:
                priority *= 0.3  # low-error, low priority

            priorities[sid] = priority
            total_priority += priority

        # Allocate budget proportionally
        if total_priority > 0:
            raw_budget = {
                sid: int(budget * p / total_priority)
                for sid, p in priorities.items()
            }
        else:
            equal_share = budget // max(len(error_states), 1)
            raw_budget = {sid: equal_share for sid in error_states}

        for sid, state in error_states.items():
            e_s = state["mean_error"]
            n_s = state["n_samples"]
            suggested = max(raw_budget.get(sid, 0), min_samples_per_state)

            if e_s > err_mean + err_std and n_s >= min_samples_per_state:
                priority_label = "high"
            elif e_s > err_mean + 0.5 * err_std:
                priority_label = "medium"
            elif e_s < err_mean - err_std and n_s < 5:
                priority_label = "check_noise"
            else:
                priority_label = "low"

            recommendations.append(
                {
                    "state_id": sid,
                    "priority": priority_label,
                    "mean_error": e_s,
                    "n_samples": n_s,
                    "suggested_samples": suggested,
                    "description": state.get("description", ""),
                    "rationale": (
                        f"{priority_label} error ({e_s:.4f}) + "
                        f"{'high' if n_s > n_samps.mean() else 'low'} density "
                        f"({n_s} samples)"
                    ),
                }
            )

        recommendations.sort(
            key=lambda r: (
                {"high": 0, "medium": 1, "low": 2, "check_noise": 3}[r["priority"]],
                -r["mean_error"],
            )
        )
        return recommendations

    # ------------------------------------------------------------------
    # Comparisons helpers
    # ------------------------------------------------------------------

    def compare_with_pure_layer1(
        self,
        X_raw: list[Any],
        residuals: np.ndarray,
        layer1_k: int = 5,
        layer2_k: int = 10,
    ) -> dict[str, Any]:
        """对比纯 Layer 1 聚类 vs 两层聚类的状态划分质量。

        Returns
        -------
        comparison : dict
            {
                'layer1': {
                    'n_states': K1,
                    'state_error_spread': float,  # 各状态平均误差的方差
                    'max_min_error_ratio': float, # 最大/最小状态误差比
                },
                'two_layer': {
                    'n_states': K2,
                    'state_error_spread': float,
                    'max_min_error_ratio': float,
                },
                'improvement': {
                    'error_spread_ratio': float,  # 两层/一层, <1 表示更集中
                    'high_error_states_resolved': int,
                }
            }
        """
        # Pure layer1 clustering
        from scx.state.metrics import StateMetrics

        X_phi = self.layer1.batch_encode(X_raw)
        sd = StateDiscovery(method="kmeans", n_states=layer1_k, random_state=42)
        l1_labels = sd.fit_predict(X_phi)

        l1_states = {}
        for s in range(layer1_k):
            mask = l1_labels == s
            if mask.sum() == 0:
                continue
            l1_states[int(s)] = {
                "n_samples": int(mask.sum()),
                "mean_residual": float(residuals[mask].mean()),
            }

        l1_errors = [s["mean_residual"] for s in l1_states.values()]
        l1_spread = float(np.std(l1_errors)) if len(l1_errors) > 1 else 0.0
        l1_maxmin = (
            float(max(l1_errors) / max(min(l1_errors), 1e-12))
            if len(l1_errors) > 1
            else 1.0
        )

        # Two-layer discovery
        two_layer_result = self.discover(
            X_raw, residuals, layer1_k=layer1_k, layer2_k=layer2_k
        )
        l2_labels = two_layer_result["layer2_labels"]
        unique_l2 = np.unique(l2_labels)
        l2_states = {}
        for s in unique_l2:
            mask = l2_labels == s
            if mask.sum() == 0:
                continue
            l2_states[int(s)] = {
                "n_samples": int(mask.sum()),
                "mean_residual": float(residuals[mask].mean()),
            }

        l2_errors = [s["mean_residual"] for s in l2_states.values()]
        l2_spread = float(np.std(l2_errors)) if len(l2_errors) > 1 else 0.0
        l2_maxmin = (
            float(max(l2_errors) / max(min(l2_errors), 1e-12))
            if len(l2_errors) > 1
            else 1.0
        )

        # Improvement metrics
        error_spread_ratio = l2_spread / max(l1_spread, 1e-12)
        n_high_l2 = sum(
            1 for e in l2_errors if e > np.mean(l2_errors) + np.std(l2_errors)
        )
        n_high_l1 = sum(
            1 for e in l1_errors if e > np.mean(l1_errors) + np.std(l1_errors)
        )

        return {
            "layer1": {
                "n_states": len(l1_states),
                "state_error_spread": l1_spread,
                "max_min_error_ratio": l1_maxmin,
            },
            "two_layer": {
                "n_states": len(l2_states),
                "state_error_spread": l2_spread,
                "max_min_error_ratio": l2_maxmin,
            },
            "improvement": {
                "error_spread_ratio": error_spread_ratio,
                "high_error_states_resolved": n_high_l2 - n_high_l1,
            },
        }

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_layer1_labels(self) -> np.ndarray | None:
        """返回 Layer 1 聚类标签（需先运行 discover）。"""
        return self._layer1_labels

    def get_layer2_labels(self) -> np.ndarray | None:
        """返回 Layer 2 误差驱动标签（需先运行 discover）。"""
        return self._layer2_labels

    def get_error_states(self) -> dict[int, dict[str, Any]]:
        """返回发现的 error states。"""
        return self.layer2.error_states_

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_layer1_metrics(
        X_phi: np.ndarray, labels: np.ndarray
    ) -> dict[str, Any]:
        """计算 Layer 1 聚类质量指标。"""
        from scx.state.metrics import StateMetrics

        sil = StateMetrics.silhouette(X_phi, labels)
        db = StateMetrics.davies_bouldin(X_phi, labels)
        return {
            "silhouette": sil,
            "davies_bouldin": db,
            "n_states": int(len(np.unique(labels))),
        }
