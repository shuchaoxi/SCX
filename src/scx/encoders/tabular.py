"""
Tabular Encoder — 表格数据领域的状态编码器。

将表格行 (numpy 数组、pandas Series/DataFrame 等) 编码为归一化的特征向量。

Example
-------
>>> import numpy as np
>>> from scx.encoders.tabular import TabularEncoder
>>> encoder = TabularEncoder(normalize=True)
>>> row = np.array([1.0, 2.0, 3.0, 0.5])
>>> vec = encoder.encode(row)
>>> vec.shape
(4,)
"""

from __future__ import annotations

from typing import Any

import numpy as np

from scx.encoders.base import SCXStateEncoder


class TabularEncoder(SCXStateEncoder):
    """表格数据编码器: 将表格行编码为 (可选归一化的) 特征向量。

    Parameters
    ----------
    normalize : bool
        是否对特征进行 min-max 归一化 (到 [0, 1])
    feature_min : np.ndarray | None
        每个特征的最小值 (用于归一化, fit 后可获得)
    feature_max : np.ndarray | None
        每个特征的最大值 (用于归一化, fit 后可获得)
    categorical_indices : list[int] | None
        类别特征的列索引列表 (对这些列进行 one-hot 编码)
    categorical_cards : dict[int, int] | None
        类别特征的基数 {col_index: n_categories}
    """

    def __init__(
        self,
        normalize: bool = True,
        feature_min: np.ndarray | None = None,
        feature_max: np.ndarray | None = None,
        categorical_indices: list[int] | None = None,
        categorical_cards: dict[int, int] | None = None,
    ) -> None:
        self.normalize = normalize
        self.feature_min = feature_min
        self.feature_max = feature_max
        self.categorical_indices = categorical_indices or []
        self.categorical_cards = categorical_cards or {}
        self._feature_dim = 0  # determined after first encode or fit

    def encode(self, row: Any) -> np.ndarray:
        """将单行表格数据编码为特征向量。

        Parameters
        ----------
        row : np.ndarray, list, pd.Series, or pd.DataFrame
            单个样本。若为 DataFrame, 取第一行。

        Returns
        -------
        np.ndarray, shape (d,)
        """
        vec = self._to_array(row)

        # Split categorical and numerical features
        if self.categorical_indices:
            numerical = np.array(
                [v for i, v in enumerate(vec) if i not in self.categorical_indices],
                dtype=np.float64,
            )
            cat_parts = []
            for idx in self.categorical_indices:
                val = int(vec[idx])
                n_cat = self.categorical_cards.get(idx, val + 1)
                one_hot = np.zeros(max(n_cat, val + 1), dtype=np.float64)
                if 0 <= val < len(one_hot):
                    one_hot[val] = 1.0
                cat_parts.append(one_hot)
            numerical = np.atleast_1d(numerical)
            result = np.concatenate([numerical] + cat_parts) if cat_parts else numerical
        else:
            result = vec.astype(np.float64)

        # Normalize if requested and stats are available
        if self.normalize and self.feature_min is not None and self.feature_max is not None:
            n = len(result)
            # Only normalize the numerical part (first len(feature_min) dims)
            n_num = len(self.feature_min)
            num_part = result[:n_num]
            denom = self.feature_max - self.feature_min
            denom[denom < 1e-10] = 1.0  # avoid div-by-zero
            result[:n_num] = (num_part - self.feature_min) / denom
            # Clamp to [0, 1]
            result[:n_num] = np.clip(result[:n_num], 0.0, 1.0)

        self._feature_dim = len(result)
        return result

    def batch_encode(self, rows: list[Any] | np.ndarray) -> np.ndarray:
        """批量编码表格数据。

        Parameters
        ----------
        rows : list[np.ndarray] or np.ndarray, shape (N, d)

        Returns
        -------
        np.ndarray, shape (N, d)
        """
        if isinstance(rows, np.ndarray) and rows.ndim == 2:
            # Fast path: stack directly
            return np.stack([self.encode(rows[i]) for i in range(len(rows))])
        return np.stack([self.encode(r) for r in rows])

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Euclidean 距离。"""
        return float(np.linalg.norm(a - b))

    def cluster(
        self, X: np.ndarray, n_clusters: int, **kwargs
    ) -> tuple[np.ndarray, np.ndarray]:
        """KMeans 聚类。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        n_clusters : int
        **kwargs
            random_state : int

        Returns
        -------
        labels : np.ndarray, shape (N,)
        centroids : np.ndarray, shape (K, d)
        """
        from sklearn.cluster import KMeans

        n = max(min(n_clusters, len(X) - 1), 1)
        rs = kwargs.get("random_state", 42)
        km = KMeans(n_clusters=n, random_state=rs, n_init="auto")
        labels = km.fit_predict(X)
        return labels, km.cluster_centers_

    def fit_normalization(
        self, X: np.ndarray | list[np.ndarray]
    ) -> "TabularEncoder":
        """从数据中学习归一化参数 (min, max)。

        Parameters
        ----------
        X : np.ndarray, shape (N, d) or list[np.ndarray]
        """
        if isinstance(X, list):
            X = np.array(X)
        self.feature_min = X.min(axis=0)
        self.feature_max = X.max(axis=0)
        return self

    def get_default_config(self) -> dict:
        return {"n_states": 10, "cluster_method": "kmeans"}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_array(row: Any) -> np.ndarray:
        """将各种表格输入统一转换为 1D numpy 数组。"""
        if isinstance(row, np.ndarray):
            return row.flatten()
        if isinstance(row, list):
            return np.array(row, dtype=np.float64)
        # Try pandas
        try:
            import pandas as pd
            if isinstance(row, pd.Series):
                return row.values.astype(np.float64)
            if isinstance(row, pd.DataFrame):
                return row.iloc[0].values.astype(np.float64)
        except ImportError:
            pass
        # Fallback
        return np.array(row, dtype=np.float64, copy=False).flatten()
