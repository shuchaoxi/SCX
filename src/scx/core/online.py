"""Online SCX: Incremental state update and expert reliability tracking.

Enables SCX to operate on data streams without full re-clustering.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np


class OnlineStateTracker:
    """Incremental state tracking without full re-clustering.

    Maintains running centroids, counts, and radii for each state.
    New samples are hard-assigned to the nearest centroid, which is then
    updated via exponential moving average (EMA).

    Parameters
    ----------
    centroids : np.ndarray, shape (K, d)
        Initial state centroids.
    decay : float, default=0.9
        EMA decay factor for centroid updates (higher = slower adaptation).
    """

    def __init__(self, centroids: np.ndarray, decay: float = 0.9) -> None:
        if centroids.ndim != 2:
            raise ValueError(f"centroids must be 2D, got shape {centroids.shape}")
        if not 0.0 < decay < 1.0:
            raise ValueError(f"decay must be in (0, 1), got {decay}")

        self.centroids = centroids.astype(float)
        self.K = centroids.shape[0]
        self.dim = centroids.shape[1]
        self.decay = decay
        self.counts = np.ones(self.K, dtype=float)
        self.radii = np.zeros(self.K, dtype=float)
        self._initialized = True

    def update(self, x: np.ndarray) -> int:
        """Assign a new sample to the nearest state and update statistics.

        Steps:
        1. Compute distances to all centroids.
        2. Hard-assign to nearest centroid.
        3. EMA update: ``c_k <- decay * c_k + (1 - decay) * x``
        4. Update count and radius (max distance seen from centroid).

        Parameters
        ----------
        x : np.ndarray, shape (d,)
            Incoming sample.

        Returns
        -------
        int
            Assigned state ID.
        """
        x = x.ravel().astype(float)
        dists = np.linalg.norm(self.centroids - x, axis=1)
        s = int(np.argmin(dists))

        # EMA centroid update
        self.centroids[s] = self.decay * self.centroids[s] + (1.0 - self.decay) * x

        # Update count (running count, capped to avoid overflow)
        self.counts[s] = min(self.counts[s] + 1.0, 1e12)

        # Update radius (max observed distance)
        d = float(dists[s])
        if d > self.radii[s]:
            self.radii[s] = d

        return s

    def get_state_proportions(self) -> np.ndarray:
        """Return the empirical proportion of samples in each state.

        Returns
        -------
        np.ndarray, shape (K,)
            Normalised proportions (sum to 1).
        """
        total = float(self.counts.sum())
        if total == 0.0:
            return np.ones(self.K) / self.K
        return self.counts / total

    def should_resplit(self, threshold: float = 2.0) -> bool:
        """Check whether the state radii suggest re-clustering is needed.

        If the ratio of the largest radius to the smallest radius exceeds
        *threshold*, the state space may have drifted and re-clustering is
        recommended.

        Parameters
        ----------
        threshold : float, default=2.0
            Max-to-min radius ratio threshold.

        Returns
        -------
        bool
            ``True`` if re-clustering is advised.
        """
        min_radius = float(self.radii[self.radii > 0].min()) if np.any(self.radii > 0) else 0.0
        max_radius = float(self.radii.max())
        if min_radius <= 0.0 or max_radius <= 0.0:
            return False  # not enough data yet
        return (max_radius / min_radius) > threshold


class OnlineExpertTracker:
    """Online expert reliability tracking.

    Maintains exponentially-weighted moving averages of per-expert,
    per-state residual and SCX scores.

    Parameters
    ----------
    M : int
        Number of experts.
    K : int
        Number of states.
    decay : float, default=0.95
        EMA decay factor for reliability updates.
    """

    def __init__(self, M: int, K: int, decay: float = 0.95) -> None:
        if M <= 0:
            raise ValueError(f"M must be positive, got {M}")
        if K <= 0:
            raise ValueError(f"K must be positive, got {K}")
        if not 0.0 < decay < 1.0:
            raise ValueError(f"decay must be in (0, 1), got {decay}")

        self.M = M
        self.K = K
        self.decay = decay
        self.R_ema = np.zeros((M, K), dtype=float)
        self.SCX_ema = np.ones((M, K), dtype=float)
        self.N_ms = np.zeros((M, K), dtype=float)

    def update(self, m: int, s: int, loss: float, tau: float) -> None:
        """Update reliability statistics for a single (expert, state) observation.

        Parameters
        ----------
        m : int
            Expert index.
        s : int
            State index.
        loss : float
            Observed loss for this sample under expert *m*.
        tau : float
            Threshold for SCX: SCX = P(loss < tau).  A larger *tau* makes
            the SCX criterion more lenient.
        """
        if not 0 <= m < self.M:
            raise ValueError(f"m={m} out of range [0, {self.M})")
        if not 0 <= s < self.K:
            raise ValueError(f"s={s} out of range [0, {self.K})")
        if loss < 0.0:
            loss = 0.0

        # Increment count
        self.N_ms[m, s] = min(self.N_ms[m, s] + 1.0, 1e12)

        # EMA update of R_m(s)
        self.R_ema[m, s] = self.decay * self.R_ema[m, s] + (1.0 - self.decay) * loss

        # SCX_m(s) = P(loss < tau) via EMA of indicator
        scx_indicator = 1.0 if loss < tau else 0.0
        if self.N_ms[m, s] == 1.0:
            self.SCX_ema[m, s] = scx_indicator  # first observation
        else:
            self.SCX_ema[m, s] = (
                self.decay * self.SCX_ema[m, s] + (1.0 - self.decay) * scx_indicator
            )

    def get_reliability(self) -> tuple[np.ndarray, np.ndarray]:
        """Return the current reliability matrices.

        Returns
        -------
        R_matrix : np.ndarray, shape (M, K)
            Mean residual (lower = better).
        SCX_matrix : np.ndarray, shape (M, K)
            SCX reliability (higher = better, in [0, 1]).
        """
        return self.R_ema.copy(), self.SCX_ema.copy()


class OnlineSCXFramework:
    """Online SCX: streaming data valuation with expert routing.

    Combines :class:`OnlineStateTracker` and :class:`OnlineExpertTracker`
    to operate on data streams without full re-clustering.

    Parameters
    ----------
    initial_centroids : np.ndarray, shape (K, d)
        Initial state centroids.
    M : int
        Number of experts.
    state_decay : float, default=0.9
        Decay factor for state centroid updates.
    expert_decay : float, default=0.95
        Decay factor for expert reliability updates.
    tau : float, default=0.5
        SCX threshold ``P(loss < tau)``.
    """

    def __init__(
        self,
        initial_centroids: np.ndarray,
        M: int,
        state_decay: float = 0.9,
        expert_decay: float = 0.95,
        tau: float = 0.5,
    ) -> None:
        self.state_tracker = OnlineStateTracker(initial_centroids, decay=state_decay)
        self.expert_tracker = OnlineExpertTracker(
            M, self.state_tracker.K, decay=expert_decay
        )
        self.tau = tau
        self.history: list[dict] = []

        # Running classification state
        self._state_sample_counts: dict[int, int] = defaultdict(int)
        self._state_loss_sums: dict[int, float] = defaultdict(float)
        self._state_best_expert_changes: dict[int, int] = defaultdict(int)

    @property
    def K(self) -> int:
        """Number of states."""
        return self.state_tracker.K

    @property
    def M(self) -> int:
        """Number of experts."""
        return self.expert_tracker.M

    def process_sample(
        self,
        x: np.ndarray,
        expert_id: int,
        loss: float,
        y_true: float | None = None,
    ) -> dict:
        """Process a single incoming sample.

        Steps:
        1. Assign *x* to a state via :meth:`OnlineStateTracker.update`.
        2. Update expert reliability via :meth:`OnlineExpertTracker.update`.
        3. Classify the sample type.
        4. Record in history.

        Parameters
        ----------
        x : np.ndarray, shape (d,)
            Incoming sample.
        expert_id : int
            Index of the expert that processed this sample.
        loss : float
            Observed loss for this sample.
        y_true : float, optional
            Ground-truth label (if available), stored for reference.

        Returns
        -------
        dict
            Decision record with keys: ``state``, ``expert``, ``loss``,
            ``classification``, ``state_proportion``.
        """
        # 1. State assignment
        s = self.state_tracker.update(x)

        # 2. Update expert reliability
        self.expert_tracker.update(expert_id, s, loss, tau=self.tau)

        # 3. Classify sample
        classification = self._classify_sample(s, expert_id, loss)

        # 4. Update running stats
        self._state_sample_counts[s] += 1
        self._state_loss_sums[s] += loss

        # Track best expert changes (for expert-dependent detection)
        R, SCX = self.expert_tracker.get_reliability()
        best_expert = int(np.argmin(R[:, s]))
        if best_expert != expert_id:
            self._state_best_expert_changes[s] += 1

        # 5. History record
        record = {
            "state": s,
            "expert": expert_id,
            "loss": float(loss),
            "classification": classification,
            "state_proportion": float(self.state_tracker.get_state_proportions()[s]),
            "y_true": y_true,
        }
        self.history.append(record)

        return record

    def _classify_sample(
        self,
        s: int,
        expert_id: int,
        loss: float,
    ) -> str:
        """Classify a sample into one of four types.

        Returns
        -------
        str
            One of ``'valuable'``, ``'redundant'``, ``'noisy'``,
            ``'expert_dependent'``, or ``'unclassified'``.
        """
        R, SCX = self.expert_tracker.get_reliability()
        state_proportion = self.state_tracker.get_state_proportions()[s]

        # High loss for this expert in this state
        state_loss = R[expert_id, s]
        scx_val = SCX[expert_id, s]

        # Expert-dependent: large gap between best and current expert
        best_R = float(np.min(R[:, s]))
        expert_gap = float(R[expert_id, s] - best_R)

        if state_proportion > 0.2 and scx_val < 0.3 and loss > self.tau:
            return "valuable"
        if state_proportion > 0.3 and scx_val > 0.7 and loss < self.tau * 0.5:
            return "redundant"
        if state_proportion < 0.05 and scx_val < 0.3 and loss > self.tau:
            return "noisy"
        if expert_gap > 0.3 * self.tau:
            return "expert_dependent"
        return "unclassified"

    def get_data_classification(self) -> dict[str, int]:
        """Aggregate sample classifications across the stream.

        Returns
        -------
        dict
            Keys: ``'valuable'``, ``'redundant'``, ``'noisy'``,
            ``'expert_dependent'``, ``'unclassified'``.
            Values: count of samples in each category.
        """
        counts: dict[str, int] = {
            "valuable": 0,
            "redundant": 0,
            "noisy": 0,
            "expert_dependent": 0,
            "unclassified": 0,
        }
        for record in self.history:
            cat = record["classification"]
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def summary(self) -> str:
        """Return a textual summary of the online SCX state.

        Returns
        -------
        str
            Multi-line summary string.
        """
        lines: list[str] = []
        lines.append("=" * 50)
        lines.append("  OnlineSCXFramework Summary")
        lines.append("=" * 50)
        lines.append(f"  States (K):          {self.K}")
        lines.append(f"  Experts (M):         {self.M}")
        lines.append(f"  Samples processed:   {len(self.history)}")

        prop = self.state_tracker.get_state_proportions()
        lines.append(f"  State proportions:   {np.round(prop, 4)}")

        classification = self.get_data_classification()
        lines.append(f"  Classification:      {classification}")

        resplit = self.state_tracker.should_resplit()
        lines.append(f"  Re-split advised:    {resplit}")
        lines.append("=" * 50)
        return "\n".join(lines)
