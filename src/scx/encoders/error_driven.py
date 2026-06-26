"""
ErrorDrivenEncoder — 两层描述符的 Layer 2：算法从误差分布中自动发现状态。

核心思想：
  不是由人预设状态（"这是 bulk，那是 surface"），
  而是由模型在哪里失败来定义状态。

工作流：
  1. Layer 1 encoder 编码所有样本
  2. 计算每个样本的 residual（error）
  3. 特征选择：找出与误差最相关的特征维度
  4. 只在误差相关子空间中聚类 → 自动发现 error states
  5. 为每个 error state 生成物理解释

Example
-------
>>> import numpy as np
>>> from scx.encoders.mlip import MLIPEncoder
>>> from scx.encoders.error_driven import ErrorDrivenEncoder
>>> layer1 = MLIPEncoder(species=["Al", "N"], rcut=4.0)
>>> layer2 = ErrorDrivenEncoder(layer1, n_error_states=3)
>>> # 假设有 20 个 Atoms 结构
>>> atoms_list = ...  # list[ase.Atoms]
>>> # 人造 residuals
>>> residuals = np.random.rand(len(atoms_list))
>>> states = layer2.fit_error_states(atoms_list, residuals)
>>> print(states[0]['description'])
"""
from __future__ import annotations

from typing import Any

import numpy as np

from scx.encoders.base import SCXStateEncoder


class ErrorDrivenEncoder(SCXStateEncoder):
    """两层描述符的 Layer 2：算法自动发现状态。

    不是由人预设状态，而是：
    1. 用 Layer 1 encoder 编码所有样本
    2. 计算每个样本的 residual (error)
    3. 在与误差最相关的特征子空间中聚类
    4. 自动发现"模型在哪里失败"

    这就是 SCX 与众不同的地方：
    不是"人类说这5个状态重要"，而是"算法发现模型在这3个区域误差大"

    Parameters
    ----------
    layer1_encoder : SCXStateEncoder
        第一层编码器（人手选，如 MLIPEncoder）
    n_error_states : int
        第二层状态数（算法自动确定范围，默认 10）
    feature_selection : str
        特征选择方法:
        - 'mutual_info' : 互信息回归（默认）
        - 'correlation' : Pearson 相关系数
        - 'shap'        : SHAP 值（需 shap 库）
        - 'none'        : 不做选择，使用全部维度
    selected_dims_ratio : float
        选择与误差最相关的维度比例（默认 1/3），仅在 feature_selection != 'none' 时生效
    """

    def __init__(
        self,
        layer1_encoder: SCXStateEncoder,
        n_error_states: int = 10,
        feature_selection: str = "mutual_info",
        selected_dims_ratio: float = 1.0 / 3.0,
    ) -> None:
        valid_methods = {"mutual_info", "correlation", "shap", "none"}
        if feature_selection not in valid_methods:
            raise ValueError(
                f"Unknown feature_selection '{feature_selection}'. "
                f"Choose from {valid_methods}."
            )

        self.layer1 = layer1_encoder
        self.n_error_states = max(1, n_error_states)
        self.feature_selection = feature_selection
        self.selected_dims_ratio = selected_dims_ratio
        self._feature_dim = layer1_encoder.get_feature_dim() or 0

        # Fitted state
        self.error_states_: dict[int, dict[str, Any]] = {}
        self.error_labels_: np.ndarray | None = None
        self._error_centroids_: np.ndarray | None = None
        self._top_dims_: np.ndarray | None = None
        self._feature_importance_: np.ndarray | None = None
        self._layer1_phi_: np.ndarray | None = None

    # ------------------------------------------------------------------
    # SCXStateEncoder interface
    # ------------------------------------------------------------------

    def encode(self, x: Any) -> np.ndarray:
        """Layer 1 编码：委托给 layer1_encoder。

        Parameters
        ----------
        x : Any
            原始输入样本

        Returns
        -------
        np.ndarray, shape (d,)
        """
        return self.layer1.encode(x)

    def batch_encode(self, X: list[Any]) -> np.ndarray:
        """批量编码，委托给 layer1_encoder。"""
        return self.layer1.batch_encode(X)

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """特征空间中两点的距离，委托给 layer1_encoder。"""
        return self.layer1.distance(a, b)

    def cluster(
        self, X: np.ndarray, n_clusters: int, **kwargs
    ) -> tuple[np.ndarray, np.ndarray]:
        """在 error-driven 空间中聚类。

        如果已经过 fit_error_states，返回已发现的 error states 标签和质心；
        否则委托给 layer1_encoder。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        n_clusters : int
        **kwargs
            额外参数传递给 layer1.cluster

        Returns
        -------
        labels : np.ndarray, shape (N,)
        centroids : np.ndarray, shape (K, d)
        """
        if self.error_labels_ is not None and self._error_centroids_ is not None:
            # Return the already-discovered error-driven states
            return self.error_labels_, self._error_centroids_
        return self.layer1.cluster(X, n_clusters, **kwargs)

    # ------------------------------------------------------------------
    # Core: error-driven state discovery
    # ------------------------------------------------------------------

    def fit_error_states(
        self,
        X_raw: list[Any],
        residuals: np.ndarray,
        layer1_labels: np.ndarray | None = None,
    ) -> dict[int, dict[str, Any]]:
        """核心方法：从误差分布中发现状态。

        Args:
            X_raw: 原始输入样本列表 (ASE Atoms, images, etc.)
            residuals: 每个样本的误差 (force error, energy loss, etc.),
                       shape (N,) 或 (N, M) 每样本多误差分量
            layer1_labels: 可选的第一层聚类标签，shape (N,)

        Returns:
            error_states: dict mapping state_id -> {
                'feature_profile': 该状态的特征模式 (d,)
                'top_error_dims': 与误差最相关的维度索引
                'mean_error': 平均误差
                'n_samples': 样本数
                'description': 自动生成的描述
            }
        """
        n_samples = len(X_raw)
        residuals = self._ensure_residuals_1d(residuals, n_samples)

        # 1. Layer 1 编码
        self._layer1_phi_ = self.batch_encode(X_raw)  # (N, d)
        phi = self._layer1_phi_

        # 2. 特征选择：哪些维度与误差最相关？
        feature_importance = self._compute_feature_importance(phi, residuals)

        # 3. 只在与误差最相关的维度上聚类
        top_dims = self._select_top_dims(feature_importance, phi.shape[1])
        self._top_dims_ = top_dims

        phi_error = phi[:, top_dims] if len(top_dims) > 0 else phi

        # 4. 在误差相关子空间中聚类 → 自动发现 error states
        n_clusters = min(self.n_error_states, max(1, n_samples - 1))
        labels, centroids = self.layer1.cluster(phi_error, n_clusters)

        # If there are layer1_labels, attempt to refine each layer-1 cluster
        # into error-driven substates
        if layer1_labels is not None:
            labels = self._refine_with_layer1(
                phi_error, labels, layer1_labels, n_clusters
            )

        self.error_labels_ = labels
        self._error_centroids_ = centroids

        # 5. 为每个 error state 生成物理解释
        error_states: dict[int, dict[str, Any]] = {}
        for s in range(n_clusters):
            mask = labels == s
            if mask.sum() == 0:
                continue
            error_states[int(s)] = {
                "feature_profile": phi[mask].mean(axis=0),
                "top_error_dims": top_dims,
                "feature_importance": feature_importance,
                "mean_error": float(residuals[mask].mean()),
                "n_samples": int(mask.sum()),
                "description": self._describe_state(
                    phi[mask], residuals[mask], top_dims
                ),
            }

        self.error_states_ = error_states
        self._feature_importance_ = feature_importance
        return error_states

    # ------------------------------------------------------------------
    # Feature importance computation
    # ------------------------------------------------------------------

    def _compute_feature_importance(
        self, phi: np.ndarray, residuals: np.ndarray
    ) -> np.ndarray:
        """计算每个特征维度与误差的相关性。

        Returns
        -------
        importance : np.ndarray, shape (d,)
        """
        d = phi.shape[1]
        if d <= 1 or self.feature_selection == "none":
            return np.ones(d)

        if self.feature_selection == "mutual_info":
            return self._mutual_info_regression(phi, residuals)
        elif self.feature_selection == "correlation":
            return self._correlation_importance(phi, residuals)
        elif self.feature_selection == "shap":
            return self._shap_importance(phi, residuals)
        return np.ones(d)

    def _mutual_info_regression(
        self, phi: np.ndarray, residuals: np.ndarray
    ) -> np.ndarray:
        """互信息回归：每个特征维度和残差之间的互信息。"""
        from sklearn.feature_selection import mutual_info_regression

        n_samples = phi.shape[0]
        # mutual_info_regression requires n_neighbors < n_samples_fit.
        # For very small datasets, fall back to uniform importance.
        if n_samples < 3:
            return np.ones(phi.shape[1])

        try:
            mi = mutual_info_regression(phi, residuals, random_state=42)
            mi = np.nan_to_num(mi, nan=0.0, posinf=0.0, neginf=0.0)
            # Normalize to [0, 1]
            max_mi = mi.max()
            if max_mi > 1e-12:
                mi = mi / max_mi
            return mi
        except ValueError:
            # Fallback for any other sklearn edge case
            return np.ones(phi.shape[1])

    def _correlation_importance(
        self, phi: np.ndarray, residuals: np.ndarray
    ) -> np.ndarray:
        """Pearson 相关系数的绝对值作为特征重要性。"""
        corrs = np.array(
            [
                np.abs(np.corrcoef(phi[:, i], residuals)[0, 1])
                if np.std(phi[:, i]) > 1e-12 and np.std(residuals) > 1e-12
                else 0.0
                for i in range(phi.shape[1])
            ],
            dtype=np.float64,
        )
        corrs = np.nan_to_num(corrs, nan=0.0)
        max_c = corrs.max()
        if max_c > 1e-12:
            corrs = corrs / max_c
        return corrs

    def _shap_importance(
        self, phi: np.ndarray, residuals: np.ndarray
    ) -> np.ndarray:
        """SHAP 值作为特征重要性（需 shap 库）。"""
        try:
            import shap
            from sklearn.ensemble import RandomForestRegressor

            model = RandomForestRegressor(
                n_estimators=50, max_depth=5, random_state=42
            )
            model.fit(phi, residuals)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(phi)
            importance = np.abs(shap_values).mean(axis=0)
            return np.nan_to_num(importance, nan=0.0)
        except ImportError:
            import warnings

            warnings.warn(
                "shap not installed, falling back to mutual_info"
            )
            return self._mutual_info_regression(phi, residuals)

    def _select_top_dims(
        self, importance: np.ndarray, d: int
    ) -> np.ndarray:
        """选择与误差最相关的维度。"""
        if self.feature_selection == "none" or d <= 3:
            return np.arange(d)

        n_select = max(3, int(d * self.selected_dims_ratio))
        n_select = min(n_select, d)
        # Sort by importance (descending) and take top-k
        top_dims = np.argsort(importance)[-n_select:]
        return top_dims

    # ------------------------------------------------------------------
    # Refinement helpers
    # ------------------------------------------------------------------

    def _refine_with_layer1(
        self,
        phi_error: np.ndarray,
        labels: np.ndarray,
        layer1_labels: np.ndarray,
        n_clusters: int,
    ) -> np.ndarray:
        """在 layer1 聚类结果内部分解 error-driven substates。

        策略：对每个 layer1 簇，检查其中的 error 方差；
        如果某个 layer1 簇内的误差方差大，则将其拆分为多个 error states。
        """
        refined = labels.copy()
        next_label = int(labels.max()) + 1 if len(labels) > 0 else 0

        for l1_label in np.unique(layer1_labels):
            mask = layer1_labels == l1_label
            if mask.sum() <= 3:
                continue  # too few samples to subdivide

            # Get error labels within this layer-1 cluster
            sub_labels = labels[mask]
            unique_subs = np.unique(sub_labels)

            # If the layer1 cluster contains multiple error-driven states,
            # keep them all; otherwise leave as-is
            if len(unique_subs) >= 2:
                continue  # already split by error

            # If this layer1 cluster maps to a single error state,
            # and it's large enough, try sub-clustering
            if mask.sum() > 10 and next_label < n_clusters * 2:
                try:
                    sub_phi = phi_error[mask]
                    _, sub_centroids = self.layer1.cluster(
                        sub_phi, min(2, mask.sum() - 1)
                    )
                    sub_k = sub_centroids.shape[0]
                    # Assign to nearest sub-centroid
                    for i in np.where(mask)[0]:
                        dists = np.linalg.norm(
                            sub_centroids - phi_error[i], axis=1
                        )
                        sub_idx = int(np.argmin(dists))
                        if sub_idx > 0:
                            # Split to a new label
                            if next_label >= n_clusters * 2:
                                break
                            refined[i] = next_label
                    next_label += sub_k - 1
                except Exception:
                    pass

        return refined

    # ------------------------------------------------------------------
    # Description generation
    # ------------------------------------------------------------------

    @staticmethod
    def _describe_state(
        phi_s: np.ndarray,
        residuals_s: np.ndarray,
        top_dims: np.ndarray,
    ) -> str:
        """自动生成状态描述。

        格式：'dim_3=0.75, dim_7=1.23, dim_1=0.42, err=0.15'
        """
        if phi_s.shape[0] == 0:
            return "empty"
        feature_means = phi_s.mean(axis=0)
        feature_stds = phi_s.std(axis=0)
        mean_err = float(residuals_s.mean())

        # Select top-3 most distinctive features (highest std within state)
        distinctive = np.argsort(-feature_stds)[:3]
        parts = [
            f"dim_{d}={feature_means[d]:.4f}" for d in distinctive
        ]
        parts.append(f"err={mean_err:.4f}")
        return ", ".join(parts)

    # ------------------------------------------------------------------
    # Analysis utilities
    # ------------------------------------------------------------------

    def get_high_error_states(
        self, threshold: float | None = None
    ) -> list[int]:
        """返回平均误差超过阈值（默认全局 mean + 1 std）的状态 ID 列表。

        Parameters
        ----------
        threshold : float, optional
            误差阈值，默认使用所有 error state 的 mean + 1 std

        Returns
        -------
        list[int]
            高误差状态 ID 列表
        """
        if not self.error_states_:
            return []

        errors = np.array(
            [s["mean_error"] for s in self.error_states_.values()]
        )
        if threshold is None:
            threshold = errors.mean() + errors.std()

        return [
            sid for sid, s in self.error_states_.items()
            if s["mean_error"] > threshold
        ]

    def summary(self) -> dict[str, Any]:
        """返回 error state 分析的摘要报告。"""
        if not self.error_states_:
            return {"status": "not_fitted", "n_states": 0}

        n_states = len(self.error_states_)
        total_samples = sum(s["n_samples"] for s in self.error_states_.values())
        errors = [s["mean_error"] for s in self.error_states_.values()]
        high_error = self.get_high_error_states()

        return {
            "status": "fitted",
            "n_states": n_states,
            "total_samples": total_samples,
            "mean_error_mean": float(np.mean(errors)),
            "mean_error_std": float(np.std(errors)),
            "top_error_dims": (
                self._top_dims_.tolist() if self._top_dims_ is not None else []
            ),
            "n_high_error_states": len(high_error),
            "high_error_state_ids": high_error,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _ensure_residuals_1d(
        residuals: np.ndarray, n_samples: int
    ) -> np.ndarray:
        """确保 residuals 为 1D 数组。如果是 2D（每样本多分量），取 norm。"""
        residuals = np.asarray(residuals, dtype=np.float64).ravel()
        if residuals.shape[0] != n_samples:
            # Try to interpret as (N, M) multi-component
            try:
                residuals_2d = residuals.reshape(n_samples, -1)
                residuals = np.linalg.norm(residuals_2d, axis=1)
            except Exception:
                pass
        if residuals.shape[0] != n_samples:
            raise ValueError(
                f"residuals length {residuals.shape[0]} != n_samples {n_samples}"
            )
        return residuals
