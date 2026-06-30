"""ExpertRegistry — 专家注册与管理中心

管理多专家系统中所有专家的注册、查询与批处理预测。
每个专家由 ExpertInfo 数据类描述，包含唯一标识、标注成本、预测函数和元数据。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np


@dataclass
class ExpertInfo:
    """单个专家的元数据结构

    Attributes
    ----------
    id : int
        自动分配的全局唯一专家编号。
    name : str
        专家唯一标识名。
    cost : float
        标注成本 C_m，表示调用该专家一次的成本开销。
    metadata : dict
        额外元数据（如专家类型、训练数据量、架构名称等）。
    predict_fn : callable
        预测函数 f_m(x) -> y_pred，接受 numpy 数组并返回预测结果。
    """

    id: int
    name: str
    predict_fn: Callable = field(repr=False)
    cost: float = 1.0
    metadata: dict = field(default_factory=dict)


class ExpertRegistry:
    """专家注册中心

    维护所有注册专家的集合，提供增删查改及批量预测接口。

    Examples
    --------
    >>> registry = ExpertRegistry()
    >>> eid = registry.register("linear_svm", lambda X: X @ w + b, cost=0.5)
    >>> info = registry.get(eid)
    >>> print(info.name)
    linear_svm
    """

    def __init__(self) -> None:
        self._experts: dict[int, ExpertInfo] = {}
        self._next_id: int = 0

    def register(
        self,
        name: str,
        predict_fn: Callable,
        cost: float = 1.0,
        **meta: Any,
    ) -> int:
        """注册一个专家。

        Parameters
        ----------
        name : str
            专家名称（不必唯一，但建议保持唯一以便识别）。
        predict_fn : callable
            预测函数 f_m(x) -> y_pred，签名 ``predict_fn(X: np.ndarray) -> np.ndarray``。
        cost : float, default=1.0
            标注成本 C_m，路由时可结合成本做 cost-sensitive 选择。
        **meta : Any
            附加元数据，以关键字参数形式传入（如 type="rf", n_params=1e5）。

        Returns
        -------
        int
            新注册专家的唯一 ID。
        """
        expert_id = self._next_id
        self._next_id += 1
        self._experts[expert_id] = ExpertInfo(
            id=expert_id,
            name=name,
            cost=cost,
            metadata=dict(meta),
            predict_fn=predict_fn,
        )
        return expert_id

    def unregister(self, expert_id: int) -> None:
        """注销一个专家。

        Parameters
        ----------
        expert_id : int
            要移除的专家 ID。

        Raises
        ------
        KeyError
            如果 expert_id 不存在。
        """
        if expert_id not in self._experts:
            raise KeyError(f"Expert with id={expert_id} not found.")
        del self._experts[expert_id]

    def get(self, expert_id: int) -> ExpertInfo:
        """获取指定 ID 的专家信息。

        Parameters
        ----------
        expert_id : int
            专家 ID。

        Returns
        -------
        ExpertInfo
        """
        if expert_id not in self._experts:
            raise KeyError(f"Expert with id={expert_id} not found.")
        return self._experts[expert_id]

    def list(self) -> list[ExpertInfo]:
        """列出所有已注册的专家。

        Returns
        -------
        list[ExpertInfo]
        """
        return list(self._experts.values())

    def predict_all(self, X: np.ndarray) -> np.ndarray:
        """所有专家对输入 X 进行预测。

        对每个专家 m 调用 predict_fn(X)，结果堆叠为形状 (M, N, *output_dim) 的数组。
        如果各专家输出形状不一致，将尝试广播对齐。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
            输入数据。

        Returns
        -------
        predictions : np.ndarray, shape (M, N, *output_dim)
            所有专家的预测结果堆叠，M 为专家数，N 为样本数。
        """
        if not self._experts:
            raise RuntimeError("No experts registered.")
        preds = [
            info.predict_fn(X)[np.newaxis, ...]
            for info in self._experts.values()
        ]
        return np.concatenate(preds, axis=0)

    def __len__(self) -> int:
        """返回已注册的专家数量。"""
        return len(self._experts)

    def __repr__(self) -> str:
        experts_repr = ", ".join(
            f"#{eid}({info.name})" for eid, info in self._experts.items()
        )
        return f"ExpertRegistry({len(self)} experts: [{experts_repr}])"
