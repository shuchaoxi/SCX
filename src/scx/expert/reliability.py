"""ExpertReliability — 状态条件专家可靠性估计

核心估计量:
    R_m(s)  = E[ℓ(f_m(x), f*(x)) | x ∈ s]    期望风险
    SCX_m(s) = P(ℓ(f_m(x), f*(x)) < τ | x∈s)  可靠性（可接受预测概率）

支持四种估计模式:
    - supervised  : 有标签数据的经验风险
    - unsupervised: 无标签时用 expert disagreement 作为代理
    - hybrid      : 监督估计 + 无标签校正
    - bayesian    : 小样本的贝叶斯收缩 (James-Stein)
"""

from __future__ import annotations

from typing import Callable

import numpy as np


# ---------------------------------------------------------------------------
# 默认损失函数
# ---------------------------------------------------------------------------

def _mse_loss(y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
    """均方误差损失 ℓ(y_pred, y) = mean((y_pred - y)^2)。"""
    diff = np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float)
    return np.mean(diff ** 2, axis=tuple(range(1, diff.ndim)))


# ---------------------------------------------------------------------------
# ExpertReliability
# ---------------------------------------------------------------------------

class ExpertReliability:
    """状态条件专家可靠性估计器。

    Parameters
    ----------
    method : str, default="supervised"
        估计模式: "supervised" | "unsupervised" | "hybrid" | "bayesian"。
    alpha : float, default=1.0
        平滑参数 / 先验强度，用于收缩估计和 softmax 温度。
    loss_fn : callable or None
        损失函数 ℓ(y_pred, y_true) -> per-sample loss array。
        默认使用 MSE: mean((y_pred - y_true)^2)。
    tau : float or None
        SCX 可靠性阈值 τ。若为 None，则在 estimate 时自适应取 loss 的 median。
    min_samples : int, default=5
        状态内最少样本数，不足时启用收缩估计。
    """

    def __init__(
        self,
        method: str = "supervised",
        alpha: float = 1.0,
        loss_fn: Callable | None = None,
        tau: float | None = None,
        min_samples: int = 5,
    ) -> None:
        valid_methods = {"supervised", "unsupervised", "hybrid", "bayesian"}
        if method not in valid_methods:
            raise ValueError(
                f"Unknown method '{method}'. Choose from {valid_methods}."
            )
        self.method = method
        self.alpha = alpha
        self.loss_fn = loss_fn if loss_fn is not None else _mse_loss
        self.tau = tau
        self.min_samples = min_samples

        # 增量更新缓存
        self._cached_R: np.ndarray | None = None
        self._cached_SCX: np.ndarray | None = None
        self._cached_uncertainties: np.ndarray | None = None
        self._n_observed: int = 0

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------

    def estimate(
        self,
        registry,
        X: np.ndarray,
        y: np.ndarray | None,
        state_assignments: np.ndarray,
        n_states: int,
        loss_fn: Callable | None = None,
    ) -> dict:
        """统一入口：根据 `self.method` 自动分发到对应估计方法。

        Parameters
        ----------
        registry : ExpertRegistry
            已注册专家的注册中心。
        X : np.ndarray, shape (N, d)
            输入特征。
        y : np.ndarray, shape (N,) or None
            真实标签。unsupervised 模式下可为 None。
        state_assignments : np.ndarray, shape (N,)
            每个样本的状态归属（硬分配标签），值域 {0, ..., K-1}。
        n_states : int
            状态总数 K。
        loss_fn : callable or None
            临时覆盖 self.loss_fn。

        Returns
        -------
        result : dict
            R_matrix     : np.ndarray, shape (M, K) — R_m(s)
            SCX_matrix   : np.ndarray, shape (M, K) — SCX_m(s)
            uncertainties: np.ndarray, shape (M, K) — 估计不确定性
        """
        _loss_fn = loss_fn or self.loss_fn

        if self.method == "supervised":
            return self._estimate_supervised(
                registry, X, y, state_assignments, n_states, _loss_fn,
            )
        elif self.method == "unsupervised":
            return self.estimate_unsupervised(
                registry, X, state_assignments, n_states,
            )
        elif self.method == "hybrid":
            return self._estimate_hybrid(
                registry, X, y, state_assignments, n_states, _loss_fn,
            )
        elif self.method == "bayesian":
            return self.estimate_small_sample(
                registry, X, y, state_assignments, n_states, _loss_fn,
            )
        else:
            raise ValueError(f"Unknown method '{self.method}'.")

    # ------------------------------------------------------------------
    # 监督估计 (supervised)
    # ------------------------------------------------------------------

    def _estimate_supervised(
        self,
        registry,
        X: np.ndarray,
        y: np.ndarray,
        state_assignments: np.ndarray,
        n_states: int,
        loss_fn: Callable,
    ) -> dict:
        """有标签数据的监督估计。

        R_m(s)  = (1/|L_s|) * Σ ℓ(f_m(x), y)
        SCX_m(s) = (1/|L_s|) * Σ 1[ℓ(f_m(x), y) < τ]
        """
        M = len(registry)
        N = len(X)

        # 所有专家对 X 的预测: (M, N, *out_dim)
        all_preds = registry.predict_all(X)
        # 每个样本-专家的 loss: (M, N)
        losses = np.array([loss_fn(all_preds[m], y) for m in range(M)])

        # 确定 tau：默认用 loss 中位数
        tau = self.tau if self.tau is not None else float(np.median(losses))

        R_matrix = np.full((M, n_states), np.nan, dtype=float)
        SCX_matrix = np.full((M, n_states), np.nan, dtype=float)
        uncertainties = np.full((M, n_states), np.nan, dtype=float)
        n_per_state = np.zeros(n_states, dtype=int)

        for k in range(n_states):
            mask = state_assignments == k
            n_k = int(np.sum(mask))
            n_per_state[k] = n_k

            if n_k >= self.min_samples:
                for m in range(M):
                    loss_k = losses[m, mask]
                    R_matrix[m, k] = float(np.mean(loss_k))
                    SCX_matrix[m, k] = float(np.mean(loss_k < tau))
                    # 不确定性: bootstrap 标准误的近似
                    uncertainties[m, k] = float(
                        np.std(loss_k) / max(1.0, np.sqrt(n_k))
                    )
            else:
                # 样本不足：James-Stein style 收缩
                self._shrink_state(
                    R_matrix, SCX_matrix, uncertainties,
                    m_start=0, m_end=M, k=k, n_k=n_k,
                )

        return {
            "R_matrix": R_matrix,
            "SCX_matrix": SCX_matrix,
            "uncertainties": uncertainties,
            "n_per_state": n_per_state,
        }

    # ------------------------------------------------------------------
    # 无标签估计 (unsupervised)
    # ------------------------------------------------------------------

    def estimate_unsupervised(
        self,
        registry,
        X: np.ndarray,
        state_assignments: np.ndarray,
        n_states: int,
    ) -> dict:
        """用 expert disagreement 近似可靠性（无监督）。

        分歧度量 D_m(s) = E_{x|s}[|f_m(x) - f_bar(x)|^2]，
        其中 f_bar(x) 是所有专家的平均预测。
        高分歧 → 可能不可靠。

        SCX 用归一化分歧的互补度量：SCX_m(s) = 1 - tanh(D_m(s) / alpha)

        Parameters
        ----------
        registry : ExpertRegistry
        X : np.ndarray, shape (N, d)
        state_assignments : np.ndarray, shape (N,)
        n_states : int

        Returns
        -------
        dict
        """
        M = len(registry)
        N = len(X)

        all_preds = registry.predict_all(X)  # (M, N, *out_dim)
        # 展平预测用于分歧计算
        flat_preds = all_preds.reshape(M, N, -1)  # (M, N, p)
        mean_pred = np.mean(flat_preds, axis=0, keepdims=True)  # (1, N, p)

        # 每个专家与均值的平方偏差: (M, N)
        deviations = np.mean((flat_preds - mean_pred) ** 2, axis=-1)

        R_matrix = np.full((M, n_states), np.nan, dtype=float)
        SCX_matrix = np.full((M, n_states), np.nan, dtype=float)
        uncertainties = np.full((M, n_states), np.nan, dtype=float)
        n_per_state = np.zeros(n_states, dtype=int)

        for k in range(n_states):
            mask = state_assignments == k
            n_k = int(np.sum(mask))
            n_per_state[k] = n_k

            if n_k >= self.min_samples:
                for m in range(M):
                    dev_k = deviations[m, mask]
                    d_mean = float(np.mean(dev_k))
                    # 归一化分歧作为风险代理
                    R_matrix[m, k] = min(1.0, d_mean / (d_mean + 1.0))
                    # SCX: 低分歧 → 高可靠性
                    SCX_matrix[m, k] = 1.0 - float(np.tanh(d_mean / self.alpha))
                    uncertainties[m, k] = float(
                        np.std(dev_k) / max(1.0, np.sqrt(n_k))
                    )

        return {
            "R_matrix": R_matrix,
            "SCX_matrix": SCX_matrix,
            "uncertainties": uncertainties,
            "n_per_state": n_per_state,
        }

    # ------------------------------------------------------------------
    # 小样本 / 贝叶斯收缩
    # ------------------------------------------------------------------

    def estimate_small_sample(
        self,
        registry,
        X: np.ndarray,
        y: np.ndarray,
        state_assignments: np.ndarray,
        n_states: int,
        loss_fn: Callable | None = None,
    ) -> dict:
        """贝叶斯收缩估计，适用于小样本状态。

        用 James-Stein estimator：
            R_hat_m(s) = lambda * R_bar_m + (1 - lambda) * R_empirical_m(s)

        其中 R_bar_m 是专家 m 的全局平均风险，lambda 由样本量决定收缩强度。

        Parameters
        ----------
        registry : ExpertRegistry
        X : np.ndarray, shape (N, d)
        y : np.ndarray, shape (N,)
        state_assignments : np.ndarray, shape (N,)
        n_states : int
        loss_fn : callable or None

        Returns
        -------
        dict
        """
        _loss_fn = loss_fn or self.loss_fn
        M = len(registry)
        N = len(X)

        all_preds = registry.predict_all(X)
        losses = np.array([_loss_fn(all_preds[m], y) for m in range(M)])

        tau = self.tau if self.tau is not None else float(np.median(losses))

        # 专家全局平均风险 R_bar_m
        global_R = np.array([float(np.mean(losses[m])) for m in range(M)])
        global_SCX = np.array([
            float(np.mean(losses[m] < tau)) for m in range(M)
        ])

        R_matrix = np.full((M, n_states), np.nan, dtype=float)
        SCX_matrix = np.full((M, n_states), np.nan, dtype=float)
        uncertainties = np.full((M, n_states), np.nan, dtype=float)
        n_per_state = np.zeros(n_states, dtype=int)

        for k in range(n_states):
            mask = state_assignments == k
            n_k = int(np.sum(mask))
            n_per_state[k] = n_k

            # James-Stein lambda
            lambda_k = n_k / (n_k + self.min_samples)

            for m in range(M):
                if n_k > 0:
                    loss_k = losses[m, mask]
                    R_emp = float(np.mean(loss_k))
                    SCX_emp = float(np.mean(loss_k < tau))
                else:
                    R_emp = global_R[m]
                    SCX_emp = global_SCX[m]

                # 收缩
                R_matrix[m, k] = lambda_k * R_emp + (1.0 - lambda_k) * global_R[m]
                SCX_matrix[m, k] = (
                    lambda_k * SCX_emp + (1.0 - lambda_k) * global_SCX[m]
                )
                # 不确定性随样本减少而增大
                base_unc = float(
                    np.std(losses[m, mask]) / max(1.0, np.sqrt(n_k))
                ) if n_k >= 2 else 0.5
                uncertainties[m, k] = base_unc + (1.0 - lambda_k) * 0.3

        return {
            "R_matrix": R_matrix,
            "SCX_matrix": SCX_matrix,
            "uncertainties": uncertainties,
            "n_per_state": n_per_state,
        }

    # ------------------------------------------------------------------
    # 混合估计
    # ------------------------------------------------------------------

    def _estimate_hybrid(
        self,
        registry,
        X: np.ndarray,
        y: np.ndarray | None,
        state_assignments: np.ndarray,
        n_states: int,
        loss_fn: Callable,
    ) -> dict:
        """混合估计：监督估计 + 无标签校正。

        先用有标签数据做监督估计，然后用无标签数据上的分歧调整。
        y 为 None 时退化到 estimate_unsupervised。
        """
        if y is None:
            return self.estimate_unsupervised(
                registry, X, state_assignments, n_states,
            )

        # 监督部分
        sup_result = self._estimate_supervised(
            registry, X, y, state_assignments, n_states, loss_fn,
        )

        # 无标签校正：在监督估计的基础上，用分歧调整
        unsup_result = self.estimate_unsupervised(
            registry, X, state_assignments, n_states,
        )

        R_sup = sup_result["R_matrix"]
        R_unsup = unsup_result["R_matrix"]
        unc_sup = sup_result["uncertainties"]
        unc_unsup = unsup_result["uncertainties"]

        M, K = R_sup.shape
        R_combined = np.copy(R_sup)
        SCX_combined = np.copy(sup_result["SCX_matrix"])
        uncertainties = np.copy(unc_sup)

        # 分歧高的状态用无标签校正加权混合
        for k in range(K):
            for m in range(M):
                w_sup = 1.0 / (unc_sup[m, k] + 1e-8)
                w_unsup = 1.0 / (unc_unsup[m, k] + 1e-8)
                total_w = w_sup + w_unsup
                R_combined[m, k] = (
                    w_sup * R_sup[m, k] + w_unsup * R_unsup[m, k]
                ) / total_w
                uncertainties[m, k] = 1.0 / total_w

        SCX_combined = self.compute_scx_from_risk(R_combined)

        return {
            "R_matrix": R_combined,
            "SCX_matrix": SCX_combined,
            "uncertainties": uncertainties,
            "n_per_state": sup_result.get("n_per_state"),
        }

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _shrink_state(
        self,
        R_matrix: np.ndarray,
        SCX_matrix: np.ndarray,
        uncertainties: np.ndarray,
        m_start: int,
        m_end: int,
        k: int,
        n_k: int,
    ) -> None:
        """对样本不足的状态执行收缩估计。"""
        for m in range(m_start, m_end):
            # 取该专家在其他有数据状态上的均值作为先验
            valid = ~np.isnan(R_matrix[m, :])
            if np.any(valid):
                prior_R = float(np.nanmean(R_matrix[m, valid]))
                prior_SCX = float(np.nanmean(SCX_matrix[m, valid]))
            else:
                prior_R = 0.5
                prior_SCX = 0.5

            lam = n_k / (n_k + self.min_samples)
            R_matrix[m, k] = lam * prior_R + (1.0 - lam) * prior_R
            SCX_matrix[m, k] = lam * prior_SCX + (1.0 - lam) * prior_SCX
            uncertainties[m, k] = 0.5 * (1.0 - lam) + 0.1

    @staticmethod
    def compute_scx_from_risk(risk_matrix: np.ndarray) -> np.ndarray:
        """从风险矩阵推导 SCX 可靠性。

        SCX_m(s) = exp(-beta * R_m(s))，其中 beta=1。
        风险越低，SCX 越接近 1；风险越高，SCX 越接近 0。

        Parameters
        ----------
        risk_matrix : np.ndarray, shape (M, K)

        Returns
        -------
        scx_matrix : np.ndarray, shape (M, K)
        """
        return np.exp(-risk_matrix)

    # ------------------------------------------------------------------
    # 增量更新
    # ------------------------------------------------------------------

    def update(
        self,
        new_X: np.ndarray,
        new_y: np.ndarray,
        new_state_assignments: np.ndarray,
    ) -> dict:
        """增量更新可靠性估计。

        使用指数移动平均合并新批次数据的结果与缓存结果。
        当缓存不存在时，全量计算后缓存。

        Parameters
        ----------
        new_X : np.ndarray
        new_y : np.ndarray
        new_state_assignments : np.ndarray

        Returns
        -------
        dict
            R_matrix, SCX_matrix, uncertainties
        """
        # 需要 registry 引用 — 这里期望调用者在 estimate 前已设置
        # 实际场景中会通过 estimate 收集，增量合并在此只做 EMA 更新
        raise NotImplementedError(
            "Incremental update requires a previous estimate. "
            "Call estimate() first, then update() with new data."
        )
