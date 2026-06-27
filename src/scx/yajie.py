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
