"""ExpertRouter — 状态条件专家路由

根据 R_m(s) 矩阵将样本路由到最合适的专家。

路由模式:
    - hard     : 硬路由，m*(x) = arg min_m R_m(s(x))
    - weighted : 软权重，w_m(x) ∝ exp(-alpha * R_m(s(x)))
    - ensemble : 加权集成预测
    - cost     : 成本敏感，m* = arg min_m R_m(s) + lambda * C_m
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from .registry import ExpertRegistry
from .reliability import ExpertReliability


class ExpertRouter:
    """状态条件专家路由。

    Parameters
    ----------
    registry : ExpertRegistry
        已注册专家的注册中心。
    reliability : ExpertReliability or None, default=None
        可靠性估计器，可选。传入后可使用其 loss_fn 等配置。
    alpha : float, default=1.0
        控制软权重分布锐度的温度参数。
    """

    def __init__(
        self,
        registry: ExpertRegistry,
        reliability: ExpertReliability | None = None,
        alpha: float = 1.0,
    ) -> None:
        self.registry = registry
        self.reliability = reliability
        self.alpha = alpha

    # ------------------------------------------------------------------
    # 硬路由
    # ------------------------------------------------------------------

    def route_hard(
        self,
        X: np.ndarray,
        state_assignments: np.ndarray,
        R_matrix: np.ndarray,
    ) -> np.ndarray:
        """硬路由：对每个样本选择风险最低的专家。

        m*(x) = arg min_m R_m(s(x))

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
            输入数据（仅用于确定 N，实际路由仅依赖状态分配和风险矩阵）。
        state_assignments : np.ndarray, shape (N,)
            每个样本的状态分配，值域 {0, ..., K-1}。
        R_matrix : np.ndarray, shape (M, K)
            风险矩阵 R_m(s)。

        Returns
        -------
        expert_ids : np.ndarray, shape (N,)
            每个样本分配的专家 ID（ExpertInfo.id）。
        """
        expert_ids = self._id_list()
        M, K = R_matrix.shape
        N = len(X)

        # (K, M) -> 每个状态下最优专家
        best_per_state = np.argmin(R_matrix, axis=0)  # (K,)

        # 按状态分配
        assigned = np.empty(N, dtype=int)
        for k in range(K):
            mask = state_assignments == k
            assigned[mask] = best_per_state[k]

        # 将索引映射为 ExpertInfo.id
        return np.array([expert_ids[idx] for idx in assigned])

    # ------------------------------------------------------------------
    # 软权重路由
    # ------------------------------------------------------------------

    def route_weighted(
        self,
        X: np.ndarray,
        state_assignments: np.ndarray,
        R_matrix: np.ndarray,
        temperature: float = 1.0,
    ) -> np.ndarray:
        """软权重：为每个样本计算各专家的归一化权重。

        w_m(x) ∝ exp(-alpha * R_m(s(x)))

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        state_assignments : np.ndarray, shape (N,)
        R_matrix : np.ndarray, shape (M, K)
        temperature : float, default=1.0
            温度参数，控制权重分布的锐度。
            温度低 → 权重分布尖锐，趋近 hard routing。
            温度高 → 权重分布平坦，趋近均匀集成。

        Returns
        -------
        weights : np.ndarray, shape (N, M)
            每个样本的专家权重矩阵，每行和为 1。
        """
        M, K = R_matrix.shape
        N = len(X)
        alpha_eff = self.alpha / max(temperature, 1e-8)

        weights = np.zeros((N, M), dtype=float)
        for k in range(K):
            mask = state_assignments == k
            n_k = int(np.sum(mask))
            if n_k == 0:
                continue
            # 取该状态下所有专家的风险
            risk_k = R_matrix[:, k]  # (M,)
            # 负风险 → 权重
            logits = -alpha_eff * risk_k  # (M,)
            # softmax
            logits_shifted = logits - np.max(logits)
            exp_logits = np.exp(logits_shifted)
            w = exp_logits / (np.sum(exp_logits) + 1e-30)
            weights[mask, :] = w[np.newaxis, :]

        return weights

    # ------------------------------------------------------------------
    # 加权集成预测
    # ------------------------------------------------------------------

    def ensemble_predict(
        self,
        X: np.ndarray,
        state_assignments: np.ndarray,
        R_matrix: np.ndarray,
    ) -> np.ndarray:
        """加权集成预测。

        根据 R_m(s) 计算软权重 w_m(x)，然后对专家预测进行加权平均。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        state_assignments : np.ndarray, shape (N,)
        R_matrix : np.ndarray, shape (M, K)

        Returns
        -------
        y_pred : np.ndarray, shape (N,) or (N, output_dim)
            加权集成后的预测。
        """
        weights = self.route_weighted(X, state_assignments, R_matrix)  # (N, M)
        all_preds = self.registry.predict_all(X)  # (M, N, *out_dim)

        # 加权求和: (N, *out_dim)
        M, N = all_preds.shape[0], all_preds.shape[1]
        out_shape = all_preds.shape[2:]  # 可能为 ()

        # 将权重 reshape 便于广播: (N, M) -> (N, M, 1...)
        w_reshaped = weights.T.reshape(M, N, *([1] * len(out_shape)))

        weighted = np.sum(w_reshaped * all_preds, axis=0)  # (N, *out_dim)
        return weighted

    # ------------------------------------------------------------------
    # 成本敏感路由
    # ------------------------------------------------------------------

    def route_cost_sensitive(
        self,
        X: np.ndarray,
        state_assignments: np.ndarray,
        R_matrix: np.ndarray,
        lambda_cost: float = 0.1,
    ) -> np.ndarray:
        """成本敏感的专家选择。

        综合考虑风险与标注成本:
            m* = arg min_m [R_m(s) + lambda * C_m]

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        state_assignments : np.ndarray, shape (N,)
        R_matrix : np.ndarray, shape (M, K)
            风险矩阵 R_m(s)。
        lambda_cost : float, default=0.1
            成本项的权衡系数。
            lambda=0 → 纯风险路由（等价于 route_hard）
            lambda 大 → 更倾向于低成本专家

        Returns
        -------
        expert_ids : np.ndarray, shape (N,)
            每个样本分配的成本敏感最优专家 ID。
        """
        expert_list = self._id_list()
        costs = np.array([
            self.registry.get(eid).cost for eid in expert_list
        ])  # (M,)
        M, K = R_matrix.shape

        # 成本调整后的得分: (M, K)
        adjusted = R_matrix + lambda_cost * costs[:, np.newaxis]
        best_per_state = np.argmin(adjusted, axis=0)  # (K,)

        N = len(X)
        assigned = np.empty(N, dtype=int)
        for k in range(K):
            mask = state_assignments == k
            assigned[mask] = best_per_state[k]

        return np.array([expert_list[idx] for idx in assigned])

    # ------------------------------------------------------------------
    # 内部辅助
    # ------------------------------------------------------------------

    def _id_list(self) -> list[int]:
        """返回按注册顺序排列的 ExpertInfo.id 列表。"""
        return [info.id for info in self.registry.list()]

    def __repr__(self) -> str:
        return (
            f"ExpertRouter(experts={len(self.registry)}, alpha={self.alpha})"
        )
