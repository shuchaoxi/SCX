"""
SCX 通用模块化架构 — 抽象基类定义。

包含两个核心抽象:
- SCXStateEncoder: 状态编码器, 领域适配的统一接口
- SCXExpert: 轻量专家抽象

使用方式:
    from scx.encoders.base import SCXStateEncoder, SCXExpert
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class SCXStateEncoder(ABC):
    """将任意领域输入编码为状态空间向量。

    这是 SCX 框架唯一的领域接口。新增领域只需实现 encode/distance/cluster 三个方法。

    Example
    -------
    >>> class MyEncoder(SCXStateEncoder):
    ...     def encode(self, x): return np.array([float(x)])
    ...     def distance(self, a, b): return float(np.linalg.norm(a - b))
    ...     def cluster(self, X, n_clusters=3, **kw):
    ...         from sklearn.cluster import KMeans
    ...         km = KMeans(n_clusters=n_clusters, random_state=42)
    ...         labels = km.fit_predict(X)
    ...         return labels, km.cluster_centers_
    """

    @abstractmethod
    def encode(self, x: Any) -> np.ndarray:
        """将原始输入 x 编码为 d 维特征向量 φ(x) ∈ R^d

        Parameters
        ----------
        x : Any
            单个原始输入样本 (ASE Atoms, 图像, 表格行, ...)

        Returns
        -------
        np.ndarray, shape (d,)
            编码后的稠密特征向量
        """
        ...

    def batch_encode(self, X: list[Any]) -> np.ndarray:
        """批量编码, 默认逐个调用 encode(), 子类可重写做并行加速。

        Parameters
        ----------
        X : list[Any]
            一组原始输入样本

        Returns
        -------
        np.ndarray, shape (N, d)
            编码后的特征矩阵
        """
        return np.stack([self.encode(x) for x in X])

    @abstractmethod
    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """特征空间中两点的距离度量。

        Parameters
        ----------
        a : np.ndarray, shape (d,)
        b : np.ndarray, shape (d,)

        Returns
        -------
        float
            距离值 (越小越近)
        """
        ...

    @abstractmethod
    def cluster(
        self, X: np.ndarray, n_clusters: int, **kwargs
    ) -> tuple[np.ndarray, np.ndarray]:
        """对编码后的向量集进行聚类, 划分状态。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
            编码向量矩阵
        n_clusters : int
            目标状态数
        **kwargs
            额外的聚类参数

        Returns
        -------
        labels : np.ndarray, shape (N,)
            每个样本的状态分配 {0, ..., K-1}
        centroids : np.ndarray, shape (K, d)
            每个状态的质心
        """
        ...

    def get_default_config(self) -> dict:
        """默认状态发现配置"""
        return {"n_states": 10, "cluster_method": "kmeans"}

    def get_feature_dim(self) -> int:
        """返回编码向量的维度 d。"""
        if hasattr(self, "_feature_dim") and self._feature_dim is not None:
            return self._feature_dim
        return 0


class SCXExpert(ABC):
    """轻量专家抽象——模型、人、仿真器皆可。

    核心思想: SCX 不关心专家内部实现, 只关心:
    - predict(x) -> y: 预测输出
    - cost() -> float: 使用成本 (用于成本约束决策)
    """

    @abstractmethod
    def predict(self, x: Any) -> Any:
        """专家对输入 x 的预测/决策。

        Parameters
        ----------
        x : Any
            输入样本

        Returns
        -------
        Any
            专家输出 (标量、向量、类别等)
        """
        ...

    def predict_batch(self, X: list[Any]) -> list[Any]:
        """批量预测, 默认逐个调用。"""
        return [self.predict(x) for x in X]

    def cost(self) -> float:
        """调用专家的成本 (默认 1.0)。"""
        return 1.0

    @property
    def name(self) -> str:
        """专家名称, 用于日志和报告。"""
        return self.__class__.__name__

    @property
    def metadata(self) -> dict:
        """专家元数据 (可选的扩展信息)。"""
        return {}
