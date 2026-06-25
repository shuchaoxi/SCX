"""SCXFramework — top-level orchestration class for the SCX pipeline."""

from __future__ import annotations

import json
import os
import pickle
from typing import Any, Callable

import numpy as np

from scx.core.config import SCXConfig
from scx.core.metrics import SCXMetrics

# ---------------------------------------------------------------------------
# Forward references for submodules not yet implemented.
# Import them only when type-checking to avoid runtime errors until the
# submodules are available.
# ---------------------------------------------------------------------------
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scx.state.space import StateSpace  # noqa: TC004
    from scx.state.discovery import StateDiscovery  # noqa: TC004
    from scx.expert.registry import ExpertRegistry  # noqa: TC004
    from scx.valuation.classifier import DataClassifier  # noqa: TC004
    from scx.action.policy import ActionPolicy  # noqa: TC004


class SCXFramework:
    """SCX main framework: unified entry point orchestrating all submodules.

    The framework runs a complete pipeline:
        1. State discovery on the representation space phi(X)
        2. State-conditioned expert reliability estimation
        3. Data four-classification (valuable / redundant / noisy / expert-dependent)
        4. Action policy execution (acquisition, routing, compression)

    Parameters
    ----------
    config : SCXConfig, optional
        Framework configuration. A default config is used when ``None``.
    """

    def __init__(self, config: SCXConfig | None = None) -> None:
        self.config = config or SCXConfig()
        self.config.validate()

        # Submodules — populated during fit()
        self.state_space: StateSpace | None = None
        self.state_discovery: StateDiscovery | None = None
        self.expert_registry: ExpertRegistry | None = None
        self.classifier: DataClassifier | None = None
        self.action_policy: ActionPolicy | None = None

        # Internal state
        self._phi_fn: Callable | None = None
        self._X_phi: np.ndarray | None = None
        self._state_assignment: np.ndarray | None = None
        self._risk_matrix: np.ndarray | None = None
        self._scx_matrix: np.ndarray | None = None
        self._state_values: np.ndarray | None = None
        self._history: list[dict[str, Any]] = []

        self.metrics = SCXMetrics()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray | None = None,
        experts: list[Callable] | None = None,
        phi: Callable | None = None,
    ) -> SCXFramework:
        """Run the full SCX pipeline.

        Pipeline steps:
            1. Compute representation phi(X) if a ``phi`` function is given.
            2. Discover states via the configured ``state_method``.
            3. Build a ``StateSpace`` from the discovered clusters.
            4. Estimate state-conditioned expert reliability.
            5. Compute learnability, redundancy, and state value V(s).
            6. Run data four-classification.
            7. Instantiate the action policy.

        Parameters
        ----------
        X : np.ndarray, shape (N, d_x)
            Input samples.
        y : np.ndarray, shape (N,), optional
            Labels for supervised reliability estimation.
        experts : list[Callable], optional
            List of expert prediction functions ``f_m: X -> y``.
        phi : Callable, optional
            Representation mapping ``phi: X -> R^d``.

        Returns
        -------
        SCXFramework
            The fitted instance (self).
        """
        # --- Step 1: Representation -------------------------------------------
        self._phi_fn = phi or (lambda x: x)
        self._X_phi = self._phi_fn(X)

        # --- Step 2: State discovery ------------------------------------------
        # TODO: instantiate StateDiscovery from scx.state.discovery
        # self.state_discovery = StateDiscovery(
        #     method=self.config.state_method,
        #     n_states=self.config.n_states,
        #     random_state=self.config.state_random_state,
        # )
        # self.state_discovery.fit(self._X_phi)
        # self._state_assignment = self.state_discovery.predict(self._X_phi)
        raise NotImplementedError(
            "fit() requires scx.state.discovery.StateDiscovery — "
            "not yet implemented."
        )

        # --- Step 3: Build StateSpace -----------------------------------------
        # TODO: build StateSpace from centroids and assignments

        # --- Step 4: Expert reliability ---------------------------------------
        # TODO: instantiate ExpertReliability, run estimate_joint

        # --- Step 5: Compute V(s) components ----------------------------------
        # TODO: LearnabilityScore, RedundancyScore, StateValue

        # --- Step 6: Data four-classification ---------------------------------
        # TODO: DataClassifier.classify_all_states

        # --- Step 7: Action policy --------------------------------------------
        # TODO: ActionPolicy

        # return self

    def predict_expert(self, x: np.ndarray) -> int:
        """Recommend the best expert index for a single sample.

        Parameters
        ----------
        x : np.ndarray, shape (d_x,)
            Input sample.

        Returns
        -------
        int
            Index of the recommended expert.
        """
        # TODO: delegate to ExpertRouter.hard_route
        raise NotImplementedError(
            "predict_expert() requires scx.expert.router.ExpertRouter."
        )

    def value(
        self,
        x: np.ndarray | None = None,
        state_id: int | None = None,
    ) -> float:
        """Compute the data value of a sample or state.

        Parameters
        ----------
        x : np.ndarray, optional
            Single sample. If given, value is computed via its state assignment.
        state_id : int, optional
            State ID to query directly.

        Returns
        -------
        float
            Data value V(s) or V(x).
        """
        if state_id is not None:
            if self._state_values is None:
                return 0.0
            return float(self._state_values[state_id])
        if x is not None:
            if self._phi_fn is None or self._state_assignment is None:
                return 0.0
            # TODO: project x -> phi(x) -> nearest state -> return V(s)
            raise NotImplementedError(
                "Per-sample value requires scx.state.assignment.StateAssignment."
            )
        return 0.0

    def recommend_action(self, state_id: int) -> str:
        """Recommend an action for a given state.

        Actions: ``'acquire'``, ``'skip'``, ``'downweight'``, ``'route'``.

        Parameters
        ----------
        state_id : int
            State identifier.

        Returns
        -------
        str
            Recommended action name.
        """
        if self.action_policy is None:
            return "acquire"
        # TODO: action_policy.decide(classification, V(s), budget)
        raise NotImplementedError(
            "recommend_action() requires ActionPolicy to be fitted."
        )

    def compress(
        self,
        X: np.ndarray,
        y: np.ndarray,
        compression_ratio: float = 0.5,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compress a dataset by removing redundant samples.

        Parameters
        ----------
        X : np.ndarray, shape (N, d_x)
            Feature matrix.
        y : np.ndarray, shape (N,)
            Labels.
        compression_ratio : float
            Fraction of samples to keep (between 0 and 1).

        Returns
        -------
        X_sub : np.ndarray
            Compressed feature matrix.
        y_sub : np.ndarray
            Corresponding labels.
        """
        # TODO: delegate to CompressStrategy.weighted_coreset
        raise NotImplementedError(
            "compress() requires scx.action.compress.CompressStrategy."
        )

    def summary(self) -> str:
        """Return a textual summary of the framework state.

        Returns
        -------
        str
            Multi-line summary string.
        """
        lines: list[str] = []
        lines.append("=" * 55)
        lines.append("  SCXFramework Summary")
        lines.append("=" * 55)
        lines.append(f"  Config:            {self.config.state_method}, "
                      f"K={self.config.n_states}, M={self.config.n_experts}")
        lines.append(f"  State space:       "
                      f"{'fitted' if self.state_space is not None else 'not fitted'}")
        lines.append(f"  Expert registry:   "
                      f"{'registered' if self.expert_registry is not None else 'empty'}")
        lines.append(f"  State values:      "
                      f"{'computed' if self._state_values is not None else 'N/A'}")
        lines.append(f"  Action policy:     "
                      f"{'ready' if self.action_policy is not None else 'N/A'}")
        lines.append(f"  History length:    {len(self._history)}")
        lines.append("=" * 55)
        return "\n".join(lines)

    def save(self, path: str) -> None:
        """Serialize the framework to disk.

        Parameters
        ----------
        path : str
            File path (convention: ``.pkl`` extension).
        """
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        state = {
            "config": self.config,
            "state_space": self.state_space,
            "state_discovery": self.state_discovery,
            "expert_registry": self.expert_registry,
            "classifier": self.classifier,
            "action_policy": self.action_policy,
            "_X_phi": self._X_phi,
            "_state_assignment": self._state_assignment,
            "_risk_matrix": self._risk_matrix,
            "_scx_matrix": self._scx_matrix,
            "_state_values": self._state_values,
            "_history": self._history,
            "metrics_history": self.metrics._history,
        }
        with open(path, "wb") as f:
            pickle.dump(state, f)

    @classmethod
    def load(cls, path: str) -> SCXFramework:
        """Deserialize a previously saved framework from disk.

        Parameters
        ----------
        path : str
            Path to the pickle file.

        Returns
        -------
        SCXFramework
            Restored instance.
        """
        with open(path, "rb") as f:
            state = pickle.load(f)

        obj = cls.__new__(cls)
        obj.config = state["config"]
        obj.state_space = state["state_space"]
        obj.state_discovery = state["state_discovery"]
        obj.expert_registry = state["expert_registry"]
        obj.classifier = state["classifier"]
        obj.action_policy = state["action_policy"]
        obj._phi_fn = None
        obj._X_phi = state["_X_phi"]
        obj._state_assignment = state["_state_assignment"]
        obj._risk_matrix = state["_risk_matrix"]
        obj._scx_matrix = state["_scx_matrix"]
        obj._state_values = state["_state_values"]
        obj._history = state["_history"]
        obj.metrics = SCXMetrics()
        obj.metrics._history = state.get("metrics_history", [])
        return obj
