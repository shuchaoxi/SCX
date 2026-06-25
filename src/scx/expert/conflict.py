"""ExpertConflict — 专家间冲突检测与仲裁

当多个专家在同一状态上产生显著分歧时，冲突检测模块负责:
    1. 检测状态内是否存在专家冲突
    2. 计算冲突度评分
    3. 仲裁选择最可靠的预测结果
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from .registry import ExpertRegistry


class ExpertConflict:
    """专家冲突检测与仲裁。

    所有方法均为静态方法，可直接调用无需实例化。
    """

    # ------------------------------------------------------------------
    # 冲突检测
    # ------------------------------------------------------------------

    @staticmethod
    def detect(
        state_id: int,
        registry: ExpertRegistry,
        X_s: np.ndarray,
        threshold: float = 0.1,
    ) -> bool:
        """检测指定状态内是否存在专家冲突。

        冲突判定：计算专家预测的 pairwise 平均差异，
        若该差异超过 threshold，则认为存在冲突。

        Parameters
        ----------
        state_id : int
            要检测的状态编号（仅用于日志/元信息）。
        registry : ExpertRegistry
            已注册的专家中心。
        X_s : np.ndarray, shape (N_s, d)
            属于该状态的样本。
        threshold : float, default=0.1
            冲突判定阈值。预测差异（MSE）超过此值视为冲突。

        Returns
        -------
        has_conflict : bool
            True 表示检测到冲突。
        """
        predictions = registry.predict_all(X_s)  # (M, N_s, *out_dim)
        score = ExpertConflict.conflict_score(X_s, registry)
        return score > threshold

    @staticmethod
    def conflict_matrix(
        X: np.ndarray,
        registry: ExpertRegistry,
        state_assignments: np.ndarray,
        n_states: int,
    ) -> np.ndarray:
        """计算 (M, M, K) 冲突张量。

        每个切片 D[:, :, k] 是状态 k 内专家两两之间的冲突矩阵，
        其中 D[i, j, k] = mean((f_i(x) - f_j(x))^2) over x in state k。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        registry : ExpertRegistry
        state_assignments : np.ndarray, shape (N,)
        n_states : int

        Returns
        -------
        conflict_tensor : np.ndarray, shape (M, M, K)
            冲突张量。对称且对角为 0。
        """
        M = len(registry)
        all_preds = registry.predict_all(X)  # (M, N, *out_dim)
        flat_preds = all_preds.reshape(M, -1)  # (M, N * p)

        tensor = np.zeros((M, M, n_states), dtype=float)

        for k in range(n_states):
            mask = state_assignments == k
            n_k = int(np.sum(mask))
            if n_k == 0:
                continue

            # 展平该状态的预测: (M, n_k * p)
            state_preds = flat_preds[:, mask].reshape(M, -1)

            for i in range(M):
                for j in range(i + 1, M):
                    diff = np.mean((state_preds[i] - state_preds[j]) ** 2)
                    tensor[i, j, k] = diff
                    tensor[j, i, k] = diff

        return tensor

    # ------------------------------------------------------------------
    # 仲裁
    # ------------------------------------------------------------------

    @staticmethod
    def arbitrate(
        X_s: np.ndarray,
        registry: ExpertRegistry,
        R_matrix: np.ndarray,
        state_id: int,
        method: str = "lowest_risk",
    ) -> int:
        """仲裁：选择状态内最可靠的专家预测。

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            属于该状态的样本。
        registry : ExpertRegistry
        R_matrix : np.ndarray, shape (M, K)
            风险矩阵 R_m(s)。
        state_id : int
            当前状态编号。
        method : str, default="lowest_risk"
            仲裁方法:
                "lowest_risk"  — 选 R_m(s) 最小的专家
                "weighted_vote" — 按 exp(-beta * R_m(s)) 加权投票
                "average"       — 所有专家预测简单平均

        Returns
        -------
        chosen_expert_id : int
            胜出专家的 ExpertInfo.id。
            对 "weighted_vote" 和 "average" 返回 -1 表示无单一胜出者。
        """
        M = len(registry)
        expert_ids = [info.id for info in registry.list()]

        if method == "lowest_risk":
            best_idx = int(np.argmin(R_matrix[:, state_id]))
            return expert_ids[best_idx]

        elif method == "weighted_vote":
            # 返回 -1 表示仲裁结果为加权集成，无单一专家
            return -1

        elif method == "average":
            # 返回 -1 表示仲裁结果为简单平均
            return -1

        else:
            raise ValueError(
                f"Unknown arbitrate method '{method}'. "
                f"Choose from: 'lowest_risk', 'weighted_vote', 'average'."
            )

    # ------------------------------------------------------------------
    # 冲突度评分
    # ------------------------------------------------------------------

    @staticmethod
    def conflict_score(
        X_s: np.ndarray,
        registry: ExpertRegistry,
    ) -> float:
        """计算状态内专家冲突度评分，范围 [0, 1]。

        基于 pairwise disagreement 的归一化度量。
        0 = 完全一致，1 = 最大分歧。

        计算方法:
            1. 所有专家对 X_s 预测
            2. 展平后计算 pairwise MSE 矩阵
            3. 取上三角均值并归一化到 [0, 1]

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            属于同一状态的样本。
        registry : ExpertRegistry

        Returns
        -------
        score : float
            0-1 之间的冲突度评分。
        """
        M = len(registry)
        if M < 2:
            return 0.0

        N_s = len(X_s)
        if N_s == 0:
            return 0.0

        predictions = registry.predict_all(X_s)  # (M, N_s, *out_dim)
        # 展平到 (M, N_s * p)
        flat = predictions.reshape(M, -1)

        # 计算 pairwise MSE
        total_diff = 0.0
        count = 0
        for i in range(M):
            for j in range(i + 1, M):
                diff = float(np.mean((flat[i] - flat[j]) ** 2))
                total_diff += diff
                count += 1

        avg_diff = total_diff / max(count, 1)

        # 归一化到 [0, 1]: 用 tanh 将任意正数映射到 [0, 1)
        score = float(np.tanh(avg_diff))
        return score

    @staticmethod
    def pairwise_disagreement(
        predictions: np.ndarray,
    ) -> np.ndarray:
        """计算专家两两之间的分歧矩阵 D in R^{M x M}。

        D[i, j] = mean(|f_i(x) - f_j(x)|^2)

        Parameters
        ----------
        predictions : np.ndarray, shape (M, N, *out_dim)
            专家预测矩阵。

        Returns
        -------
        D : np.ndarray, shape (M, M)
            对称分歧矩阵，对角为 0。
        """
        M = predictions.shape[0]
        flat = predictions.reshape(M, -1)
        D = np.zeros((M, M), dtype=float)

        for i in range(M):
            for j in range(i + 1, M):
                d = float(np.mean((flat[i] - flat[j]) ** 2))
                D[i, j] = d
                D[j, i] = d

        return D
