# scx/action/policy.py
# ActionPolicy -- action decision engine for SCX framework.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np
import pandas as pd


@dataclass
class ActionResult:
    """Result of executing one action on a state.

    Attributes
    ----------
    action : str
        The action that was executed.
    state_id : int
        The target state identifier.
    samples_selected : list[int]
        Indices of samples selected (acquire / relabel actions).
    samples_discarded : list[int]
        Indices of samples discarded (discard / downweight actions).
    expert_assigned : int | None
        Expert id assigned (route action), if applicable.
    metadata : dict
        Additional execution metadata.
    """

    action: str
    state_id: int
    samples_selected: list[int] = field(default_factory=list)
    samples_discarded: list[int] = field(default_factory=list)
    expert_assigned: int | None = None
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Action mapping from state classification category to default action
# ---------------------------------------------------------------------------
_DEFAULT_ACTION_MAP: dict[str, str] = {
    "valuable": "acquire",
    "redundant": "downweight",
    "noisy": "discard",
    "expert_dependent": "route",
}


class ActionPolicy:
    """Action decision engine.

    Determines which action to take for each state based on its
    classification category and estimated data value.

    Action space A = {acquire, relabel, downweight, discard, route, split}

    Parameters
    ----------
    budget : int
        Total budget (number of samples) available for acquisition.
    mode : str
        Budget allocation mode:

        - ``"proportional"`` : allocate budget proportionally to V(s).
        - ``"threshold"``    : allocate equally among states above a
          value percentile threshold.
        - ``"hybrid"``       : proportional allocation with a per-state
          minimum for valuable states.
    """

    def __init__(self, budget: int = 100, mode: str = "proportional"):
        if mode not in ("proportional", "threshold", "hybrid"):
            raise ValueError(
                f"Unknown mode '{mode}'. Expected one of: "
                f"proportional, threshold, hybrid."
            )
        self.budget = budget
        self.mode = mode

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def decide(
        self,
        state_classifications: pd.DataFrame,
        state_values: pd.DataFrame,
    ) -> dict[int, str]:
        """Decide an action for each state based on its classification.

        Parameters
        ----------
        state_classifications : pd.DataFrame
            Must contain columns ``state_id`` and ``category``.
        state_values : pd.DataFrame
            Must contain columns ``state_id`` and ``value``.

        Returns
        -------
        actions : dict[int, str]
            Mapping ``{state_id: action_name}``.
        """
        merged = state_classifications.merge(
            state_values, on="state_id", how="inner"
        )
        actions: dict[int, str] = {}

        for _, row in merged.iterrows():
            sid = int(row["state_id"])
            cat = str(row["category"])
            val = float(row["value"])

            base = _DEFAULT_ACTION_MAP.get(cat, "acquire")
            refined = self._refine_action(base, val)
            actions[sid] = refined

        return actions

    def allocate_budget(
        self,
        state_values: pd.DataFrame,
    ) -> dict[int, int]:
        """Allocate the acquisition budget across states.

        Parameters
        ----------
        state_values : pd.DataFrame
            Must contain columns ``state_id`` and ``value``.

        Returns
        -------
        allocation : dict[int, int]
            Mapping ``{state_id: n_samples_to_acquire}``.
        """
        vals = state_values.sort_values("state_id")
        sids = vals["state_id"].values
        V = vals["value"].values.astype(float)
        K = len(sids)

        B = self.budget
        alloc: dict[int, int] = {}

        if K == 0:
            return alloc

        if self.mode == "proportional":
            return self._allocate_proportional(sids, V, B)

        elif self.mode == "threshold":
            return self._allocate_threshold(sids, V, B)

        elif self.mode == "hybrid":
            return self._allocate_hybrid(sids, V, B)

        return alloc

    def execute(
        self,
        state_actions: dict[int, str],
        X: np.ndarray,
        state_assignments: np.ndarray,
        **kwargs: Any,
    ) -> dict[int, ActionResult]:
        """Execute the decided actions and return results.

        Parameters
        ----------
        state_actions : dict[int, str]
            Mapping ``{state_id: action}`` produced by ``decide()``.
        X : np.ndarray, shape (N, d)
            Feature matrix (or phi-space representation).
        state_assignments : np.ndarray, shape (N,)
            Hard state assignment for each sample.
        **kwargs : Any
            Additional keyword arguments (e.g. ``acquisition_strategy``,
            ``compress_strategy``, ``n_to_acquire``).

        Returns
        -------
        results : dict[int, ActionResult]
            Mapping ``{state_id: ActionResult}``.
        """
        results: dict[int, ActionResult] = {}
        unique_states = np.unique(state_assignments)

        for sid in unique_states:
            if sid not in state_actions:
                continue

            action = state_actions[sid]
            mask = state_assignments == sid
            indices = np.where(mask)[0].tolist()

            result = ActionResult(action=action, state_id=int(sid))

            if action == "acquire":
                n = kwargs.get("n_to_acquire", 10)
                # Perform sample selection inside the state
                strategy = kwargs.get("acquisition_strategy", None)
                if strategy is not None:
                    X_s = X[mask]
                    selected_local = strategy.select_samples(
                        X_s, n, state_id=int(sid), **kwargs
                    )
                    global_indices = np.where(mask)[0][selected_local].tolist()
                    result.samples_selected = global_indices
                else:
                    # Default: random selection within state
                    n = min(n, len(indices))
                    chosen = np.random.choice(indices, size=n, replace=False).tolist()
                    result.samples_selected = chosen

                result.metadata["n_acquired"] = len(result.samples_selected)

            elif action == "discard":
                result.samples_discarded = indices
                result.metadata["n_discarded"] = len(indices)

            elif action == "route":
                expert_id = kwargs.get("expert_assigned", None)
                result.expert_assigned = int(expert_id) if expert_id is not None else None
                result.metadata["n_routed"] = len(indices)

            elif action in ("downweight", "relabel"):
                result.samples_selected = indices
                result.metadata["action"] = action
                result.metadata["n_affected"] = len(indices)

            results[int(sid)] = result

        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _refine_action(self, base: str, value: float) -> str:
        """Refine a base action based on state value thresholds.

        Parameters
        ----------
        base : str
            Default action from the category map.
        value : float
            State data value V(s).

        Returns
        -------
        str
            Refined action name.
        """
        # If value is extremely low, downgrade acquire to skip
        if base == "acquire" and value < 1e-6:
            return "discard"
        return base

    def _allocate_proportional(
        self, sids: np.ndarray, V: np.ndarray, B: int
    ) -> dict[int, int]:
        """Proportional allocation: n_s ∝ V(s)."""
        total = V.sum()
        if total <= 0:
            # Equal split if all values are zero
            per_state = B // len(sids)
            remainder = B % len(sids)
            alloc = {}
            for i, sid in enumerate(sids):
                alloc[int(sid)] = per_state + (1 if i < remainder else 0)
            return alloc

        raw = B * V / total
        floor = np.floor(raw).astype(int)
        remainder = int(B - floor.sum())
        # Distribute remainder to the highest-value states
        order = np.argsort(-V)
        alloc = {}
        for i, sid in enumerate(sids):
            n = int(floor[i])
            if remainder > 0 and i in order[:remainder]:
                n += 1
            alloc[int(sid)] = max(1, n)
        return alloc

    def _allocate_threshold(
        self, sids: np.ndarray, V: np.ndarray, B: int, percentile: float = 70.0
    ) -> dict[int, int]:
        """Threshold allocation: only top percentile get budget."""
        thresh = np.percentile(V, percentile)
        top_mask = V >= thresh
        n_top = int(top_mask.sum())
        alloc: dict[int, int] = {}

        if n_top == 0:
            per_state = B // len(sids)
            for i, sid in enumerate(sids):
                alloc[int(sid)] = per_state
            return alloc

        base = B // n_top
        remainder = B % n_top
        top_order = np.argsort(-V[top_mask])

        j = 0
        for i, sid in enumerate(sids):
            if top_mask[i]:
                n = base + (1 if j < remainder and j in top_order[:remainder] else 0)
                alloc[int(sid)] = max(1, n)
                j += 1
            else:
                alloc[int(sid)] = 0
        return alloc

    def _allocate_hybrid(
        self,
        sids: np.ndarray,
        V: np.ndarray,
        B: int,
        top_percentile: float = 60.0,
        min_alloc: int = 1,
    ) -> dict[int, int]:
        """Hybrid allocation.

        70% budget to top percentile states (proportional),
        30% budget spread evenly among remaining valuable states.
        """
        thresh = np.percentile(V, 100.0 - top_percentile)
        top_mask = V >= thresh
        n_top = int(top_mask.sum())
        n_bottom = len(sids) - n_top

        primary = int(B * 0.7)
        secondary = B - primary

        alloc: dict[int, int] = {}

        # Primary: proportional among top states
        if n_top > 0:
            V_top = V[top_mask]
            total_top = V_top.sum()
            if total_top > 0:
                raw = primary * V_top / total_top
                floor = np.floor(raw).astype(int)
                rem = primary - int(floor.sum())
                top_order = np.argsort(-V_top)
                j = 0
                for i, sid in enumerate(sids):
                    if top_mask[i]:
                        n = int(floor[j])
                        if rem > 0 and j < rem:
                            n += 1
                        alloc[int(sid)] = max(min_alloc, n)
                        j += 1

        # Secondary: evenly among remaining
        if n_bottom > 0:
            per_state = secondary // n_bottom if n_bottom > 0 else 0
            for i, sid in enumerate(sids):
                if not top_mask[i]:
                    alloc[int(sid)] = max(0, per_state)

        return alloc
