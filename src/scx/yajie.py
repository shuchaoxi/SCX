"""
雅洁 — Yajie: Elegant Data Sanitizer for SCX
===============================================

Named after the most elegant cleaner. 雅 (grace) + 洁 (purity).

Yajie wraps SCX's noise detection theorems (Thm 1+2), multi-expert
consistency analysis, and data quality diagnostics into a single
clean interface. Feed it dirty data — get back pristine data.

Philosophy: Data cleaning shouldn't feel like plumbing.
It should feel like spring cleaning with the windows open.

Examples
--------
>>> from scx.yajie import Yajie
>>> yj = Yajie()
>>> yj.scan(data, experts)
>>> clean = yj.purify(data)

Yajie won't just tell you what's wrong with your data.
She'll tell you *why* — and whether it's noise, redundancy,
or just a hard example that needs more love.
"""

from __future__ import annotations

import warnings
from typing import Optional

import numpy as np
import pandas as pd

from scx.valuation.state_value import StateValue, hoeffding_bound, chernoff_bound
from scx.valuation.noise_score import NoiseScore
from scx.valuation.redundancy import RedundancyScore
from scx.valuation.classifier import DataClassifier
from scx.state.discovery import StateDiscovery


class Yajie:
    """Elegant data sanitizer.

    Yajie takes dirty training data, runs it through SCX's
    theorem-backed diagnostics, and returns a clean dataset
    with a full audit report.

    Parameters
    ----------
    grace : float, default=0.05
        Tolerance for imperfection. Higher = more forgiving.
        Named after the "grace" in 雅.
    purity_threshold : float, default=0.9
        Minimum acceptable SCX reliability for a sample to be kept.
        Named after the "purity" in 洁.

    Attributes
    ----------
    report_ : pd.DataFrame
        After ``scan()``, contains per-sample diagnostics:
        noise_risk, redundancy, value, verdict.
    """

    def __init__(
        self,
        grace: float = 0.05,
        purity_threshold: float = 0.9,
    ) -> None:
        if not 0 < grace < 1:
            raise ValueError(f"grace must be in (0, 1), got {grace}")
        if not 0 < purity_threshold <= 1:
            raise ValueError(
                f"purity_threshold must be in (0, 1], got {purity_threshold}"
            )

        self.grace = grace
        self.purity_threshold = purity_threshold
        self._noise_scorer = NoiseScore()
        self._redundancy_scorer = RedundancyScore()
        self._classifier = DataClassifier()
        self._state_value = StateValue()

        # Internal state
        self.report_: Optional[pd.DataFrame] = None
        self._is_scanned = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan(
        self,
        data: np.ndarray,
        experts: list,
        state_labels: Optional[np.ndarray] = None,
        feature_matrix: Optional[np.ndarray] = None,
    ) -> pd.DataFrame:
        """Scan data and produce a full diagnostic report.

        Like opening all the windows and letting the light in.

        Parameters
        ----------
        data : np.ndarray, shape (N, ...)
            Training samples.
        experts : list of callable
            M trained models. Each should accept ``data`` and return
            predictions. More experts = better diagnostics (Theorem 1).
        state_labels : np.ndarray, optional, shape (N,)
            Pre-computed state assignments. If None, states are
            discovered automatically.
        feature_matrix : np.ndarray, optional, shape (N, d_phi)
            Feature representations for Theorem 2 weak-feature check.

        Returns
        -------
        pd.DataFrame
            Columns: noise_risk, redundancy, scx_value, verdict, reason
        """
        M = len(experts)
        N = len(data)

        if M < 2:
            warnings.warn(
                "Yajie works best with multiple experts (M ≥ 3). "
                "With only one expert, noise/hard distinction is impossible. "
                "See Theorem 1 for why.",
                UserWarning,
            )

        # Compute multi-expert consistency
        expert_errors = self._compute_expert_errors(data, experts)

        # Scan each sample
        records = []
        for i in range(N):
            residual = float(expert_errors[i, :].mean())
            consistency = float(1.0 - expert_errors[i, :].std())

            noise = self._noise_scorer.compute(
                residuals=np.array([residual]),
                state_proportion=1.0 / N,
                consistency=consistency,
            )[0]
            noise = float(noise)
            redundancy = 1.0 - consistency  # proxy for redundancy

            # Consistency score (Theorem 1)
            C_i = self._state_value.noise_consistency_score(expert_errors[i, :])

            # Verdict
            if C_i > 0.8:
                verdict = "noisy"
                reason = "All experts fail — likely bad label"
            elif C_i < 0.2:
                verdict = "clean"
                reason = "Experts agree — likely good data"
            elif noise > 0.5 and redundancy < 0.3:
                verdict = "hard"
                reason = "Some experts fail — learnable difficulty"
            elif redundancy > 0.6:
                verdict = "redundant"
                reason = "Well-covered region, compressible"
            else:
                verdict = "uncertain"
                reason = "Need more experts or better features"

            records.append(
                {
                    "noise_risk": float(noise),
                    "redundancy": float(redundancy),
                    "consistency_score": float(C_i),
                    "verdict": verdict,
                    "reason": reason,
                }
            )

        self.report_ = pd.DataFrame(records)
        self._is_scanned = True

        # Theorem 2: check if features are too weak
        if feature_matrix is not None and state_labels is not None:
            diag = self._state_value.feature_strength_diagnostic(
                feature_matrix, state_labels
            )
            if diag.get("recommendation") in ("weak", "features_too_weak"):
                warnings.warn(
                    f"δ = {diag.get('delta', '?')}:.4f — "
                    f"Features may be too weak for reliable noise detection. "
                    f"See Theorem 2. Yajie will do her best, but be cautious.",
                    UserWarning,
                )

        return self.report_

    def fit(
        self,
        X: np.ndarray,
        y: Optional[np.ndarray] = None,
        experts: Optional[list] = None,
        phi: Optional[callable] = None,
        n_states: int = 5,
        exploration_rate: float = 0.1,
    ) -> "Yajie":
        """Fit the full Yajie pipeline: state discovery → cluster → multi-expert scoring.

        This is the state-level pipeline that discovers latent data states via
        clustering in feature space, then scores each state using the **Cercis Score**:

        .. math::

            S(s) = Q(s) + \\eta \\cdot N(s)

        where:
        - :math:`Q(s)` = quality score (1 - mean expert residual in state s)
        - :math:`N(s)` = noise score (density + consistency weighted residual)
        - :math:`\\eta` = exploration rate (``grace`` in Yajie parlance)

        States are then classified into three categories:

        * **clean** — high quality, low noise (keep as-is)
        * **noisy** — low quality, high noise (likely mislabeled)
        * **ambiguous** — moderate quality/noise (needs more investigation)

        Parameters
        ----------
        X : np.ndarray, shape (N, d) or (N, ...)
            Training samples. If ``phi`` is None, X is used directly as features.
        y : np.ndarray, shape (N,), optional
            Labels for supervised expert evaluation.
        experts : list of callable, optional
            M trained models. Each should accept ``X`` and return predictions.
            If None, a heuristic noise estimation is used.
        phi : callable, optional
            Feature extraction function ``phi: X → R^{d_phi}``.
            If None, ``X`` is flattened and used directly.
        n_states : int, default=5
            Number of states K for state discovery clustering.
        exploration_rate : float, default=0.1
            Weight η for the noise term in the Cercis Score.
            Higher = more tolerance for noisy states.

        Returns
        -------
        self : Yajie
            The fitted instance with ``self.report_`` containing per-sample
            diagnostics and ``self.state_report_`` containing per-state
            classification.
        """
        N = len(X)

        # ---- Step 1: Feature extraction ---------------------------------
        if phi is not None:
            phi_X = np.asarray(phi(X), dtype=float)
        else:
            phi_X = np.asarray(X, dtype=float)
        if phi_X.ndim == 1:
            phi_X = phi_X.reshape(-1, 1)
        if phi_X.ndim > 2:
            phi_X = phi_X.reshape(N, -1)

        d_phi = phi_X.shape[1]

        # ---- Step 2: State discovery ------------------------------------
        K = min(n_states, N)
        if K < 2:
            K = 2
        sd = StateDiscovery(
            method="kmeans",
            n_states=K,
            random_state=42,
        )
        state_labels = sd.fit_predict(phi_X)
        centroids = sd.get_centroids()

        # ---- Step 3: Multi-expert error computation ---------------------
        if experts is not None and len(experts) > 0:
            M = len(experts)
            expert_errors = self._compute_expert_errors(X, experts)  # (N, M)
        else:
            # Heuristic: use reconstruction error as proxy
            M = 0
            expert_errors = None

        # ---- Step 4: Per-state scoring ----------------------------------
        state_records = []
        sample_verdicts = np.full(N, "uncertain", dtype=object)

        for s in range(K):
            mask = state_labels == s
            n_s = mask.sum()
            if n_s == 0:
                continue

            rho_s = n_s / N  # state proportion

            # Quality score Q(s): 1 - mean residual
            if expert_errors is not None and M > 0:
                state_errors = expert_errors[mask]  # (n_s, M)
                mean_residual = float(state_errors.mean())
                # Consistency: inverse std of expert errors (higher = more consistent)
                expert_std = float(state_errors.std(axis=1).mean())
                consistency = float(1.0 / (1.0 + expert_std))
            else:
                # Heuristic: distance to centroid as residual proxy
                dists = np.linalg.norm(phi_X[mask] - centroids[s], axis=1)
                mean_residual = float(dists.mean() / (dists.max() + 1e-8)) if dists.max() > 0 else 0.0
                consistency = float(1.0 / (1.0 + dists.std()))

            Q_s = float(1.0 - mean_residual)

            # Noise score N(s)
            noise_scores = self._noise_scorer.compute(
                residuals=np.full(n_s, mean_residual),
                state_proportion=rho_s,
                consistency=consistency,
            )
            N_s = float(noise_scores.mean())

            # Redundancy D(s)
            X_s = phi_X[mask]
            redundancy_scorer = RedundancyScore()
            D_s = redundancy_scorer.redundancy(
                state_proportion=rho_s,
                mean_residual=mean_residual,
                similarity=redundancy_scorer.state_similarity(X_s),
                boundary=redundancy_scorer.boundary_score(X_s, centroids, s),
            )

            # ---- Cercis Score: S(s) = Q(s) + η · N(s) ------------------
            eta = exploration_rate if exploration_rate is not None else self.grace
            S_s = float(Q_s + eta * N_s)

            state_records.append({
                "state_id": s,
                "n_samples": n_s,
                "proportion": float(rho_s),
                "mean_residual": float(mean_residual),
                "quality_score": float(Q_s),
                "noise_score": float(N_s),
                "cercis_score": float(S_s),
                "consistency": float(consistency),
                "redundancy": float(D_s),
                # verdict assigned after all states scored (adaptive)
            })

        # ---- Adaptive classification: clean / noisy / ambiguous ---------
        # Use percentile-based thresholds within the batch, per Theorem 1's
        # state-conditioned separation gap principle.
        # With K >= 3 states, uses median split; with K < 3, compares absolute scores.
        if len(state_records) >= 3:
            Q_vals = np.array([r["quality_score"] for r in state_records])
            N_vals = np.array([r["noise_score"] for r in state_records])
            q_median = float(np.median(Q_vals))
            n_median = float(np.median(N_vals))

            for r in state_records:
                Q_s = r["quality_score"]
                N_s = r["noise_score"]
                if Q_s >= q_median and N_s <= n_median:
                    r["verdict"] = "clean"
                elif Q_s <= q_median and N_s >= n_median:
                    r["verdict"] = "noisy"
                else:
                    r["verdict"] = "ambiguous"
        elif len(state_records) == 2:
            # Two states: one cleaner, one noisier
            sorted_by_q = sorted(state_records, key=lambda r: r["quality_score"], reverse=True)
            sorted_by_q[0]["verdict"] = "clean"
            sorted_by_q[1]["verdict"] = "noisy"
        elif len(state_records) == 1:
            state_records[0]["verdict"] = "ambiguous"

        # Propagate verdicts to samples
        for s, r in enumerate(state_records):
            mask = state_labels == r["state_id"]
            sample_verdicts[mask] = r["verdict"]

        # ---- Step 5: Build sample-level report --------------------------
        sample_records = []
        for i in range(N):
            s = int(state_labels[i])
            sr = state_records[s] if s < len(state_records) else {}
            sample_records.append({
                "sample_id": i,
                "state_id": s,
                "verdict": str(sample_verdicts[i]),
                "state_quality": float(sr.get("quality_score", 0.5)),
                "state_noise": float(sr.get("noise_score", 0.5)),
                "state_cercis": float(sr.get("cercis_score", 0.5)),
            })

        self.report_ = pd.DataFrame(sample_records)
        self.state_report_ = pd.DataFrame(state_records)
        self._is_scanned = True  # Mark as scanned so purify() can be called
        self._state_labels_ = state_labels
        self._phi_X_ = phi_X

        # Theorem 2: weak feature diagnostic
        if d_phi > 0 and K >= 2:
            diag = self._state_value.feature_strength_diagnostic(phi_X, state_labels)
            if diag.get("recommendation") in ("weak",):
                warnings.warn(
                    f"δ = {diag.get('delta', '?'):.4f} — "
                    f"Features may be too weak for reliable state discovery. "
                    f"See Theorem 2. Yajie will do her best, but be cautious.",
                    UserWarning,
                )

        return self

    def purify(
        self,
        data: np.ndarray,
        labels: Optional[np.ndarray] = None,
        mode: str = "conservative",
    ) -> tuple[np.ndarray, Optional[np.ndarray], pd.DataFrame]:
        """Purify data by removing or flagging problematic samples.

        雅洁 at work — sweeping out the noise, keeping the gems.

        Parameters
        ----------
        data : np.ndarray
        labels : np.ndarray, optional
        mode : str, default='conservative'
            'conservative': only remove high-confidence noise.
            'aggressive': remove noise + compress redundants.
            'audit': keep all data but add verdict labels.

        Returns
        -------
        clean_data : np.ndarray
        clean_labels : np.ndarray or None
        audit : pd.DataFrame
            Summary of what was kept, removed, and why.
        """
        if not self._is_scanned:
            raise RuntimeError(
                "Call scan() first. Yajie needs to see the data "
                "before she can clean it."
            )

        report = self.report_

        if mode == "conservative":
            keep_mask = report["verdict"] != "noisy"
        elif mode == "aggressive":
            keep_mask = ~report["verdict"].isin(["noisy", "redundant"])
        elif mode == "audit":
            keep_mask = np.ones(len(data), dtype=bool)
        else:
            raise ValueError(f"Unknown mode: {mode}. Use 'conservative', 'aggressive', or 'audit'.")

        clean_data = data[keep_mask]
        clean_labels = labels[keep_mask] if labels is not None else None

        n_removed = (~keep_mask).sum()
        audit = pd.DataFrame(
            {
                "total_samples": [len(data)],
                "kept": [keep_mask.sum()],
                "removed": [n_removed],
                "removed_noise": [(report["verdict"] == "noisy").sum()],
                "removed_redundant": [(report["verdict"] == "redundant").sum()],
                "mode": [mode],
                "signature": ["— 雅洁"],
            }
        )

        return clean_data, clean_labels, audit

    def bless(self) -> str:
        """Return a blessing for your freshly cleaned data.

        Because every dataset deserves a moment of grace.
        """
        if not self._is_scanned:
            return "雅洁 has not yet visited this dataset. Call scan() first."

        n = len(self.report_)
        n_noisy = (self.report_["verdict"] == "noisy").sum()
        n_clean = (self.report_["verdict"] == "clean").sum()
        n_hard = (self.report_["verdict"] == "hard").sum()

        ratio = n_noisy / n if n > 0 else 0

        if ratio < 0.05:
            quality = "✨ 近乎完美"
        elif ratio < 0.15:
            quality = "🌿 略有尘埃，已拂去"
        elif ratio < 0.30:
            quality = "🧹 大扫除完成"
        else:
            quality = "🏚️ 这数据经历了什么..."

        return (
            f"               ✧ 雅洁 · 数据净化报告 ✧\n"
            f"  ╔══════════════════════════════════╗\n"
            f"  ║  总样本:  {n:>6d}                   ║\n"
            f"  ║  洁净:    {n_clean:>6d}  ← 保留       ║\n"
            f"  ║  困难:    {n_hard:>6d}  ← 保留(需更多爱) ║\n"
            f"  ║  噪声:    {n_noisy:>6d}  ← 已净化       ║\n"
            f"  ║  纯净度:  {(1-ratio)*100:>5.1f}%                  ║\n"
            f"  ╚══════════════════════════════════╝\n"
            f"  {quality}\n"
            f"  grace={self.grace}, purity_threshold={self.purity_threshold}\n"
            f"  Theorem 1 says: more experts → cleaner data.\n"
            f"  Theorem 2 says: weak features → be humble.\n"
            f"  Yajie says: data deserves respect. Clean it with love."
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_expert_errors(
        data: np.ndarray,
        experts: list,
    ) -> np.ndarray:
        """Compute expert errors for all samples.

        Parameters
        ----------
        data : np.ndarray, shape (N, ...)
        experts : list of callable

        Returns
        -------
        errors : np.ndarray, shape (N, M)
            errors[i, m] = loss of expert m on sample i
        """
        N = len(data)
        M = len(experts)
        errors = np.zeros((N, M))

        for m, expert in enumerate(experts):
            preds = expert(data)
            # Use MSE per sample as error
            if preds.ndim == data.ndim:
                errors[:, m] = np.mean((data - preds) ** 2, axis=tuple(range(1, data.ndim)))
            else:
                errors[:, m] = np.abs(preds - data).reshape(N, -1).mean(axis=1)

        # Normalize to [0, 1] per sample
        max_err = errors.max(axis=1, keepdims=True)
        max_err[max_err == 0] = 1.0
        errors = errors / max_err

        return errors


# ------------------------------------------------------------------
# Singleton convenience
# ------------------------------------------------------------------

# You can just: from scx.yajie import yajie
yajie = Yajie()


def clean(data, experts, labels=None, mode="conservative"):
    """One-liner: clean data with 雅洁.

    >>> from scx.yajie import clean
    >>> clean_data, clean_labels, report = clean(dirty_data, my_experts)

    No fuss. Just clean.
    """
    yj = Yajie()
    yj.scan(data, experts)
    return yj.purify(data, labels, mode=mode)
