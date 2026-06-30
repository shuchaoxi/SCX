"""SCX framework configuration dataclass with validation."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any

_VALID_STATE_METHODS = {"kmeans", "gmm", "spectral", "hdbscan"}
_VALID_RELIABILITY_METHODS = {"supervised", "unsupervised", "hybrid"}
_VALID_ACTION_MODES = {"proportional", "threshold", "hybrid"}


@dataclass
class SCXConfig:
    """SCX framework global configuration.

    Parameters
    ----------
    state_method : str
        State discovery algorithm. One of {'kmeans', 'gmm', 'spectral', 'hdbscan'}.
    n_states : int
        Target number of states (ignored by HDBSCAN).
    state_random_state : int
        Random seed for state discovery reproducibility.

    n_experts : int
        Number of experts in the system.
    expert_cost : list[float] | None
        Per-expert annotation cost C_m. Length must match n_experts.

    reliability_method : str
        Reliability estimation strategy.
    reliability_alpha : float
        Smoothing parameter for reliability estimates.

    error_threshold : float
        Threshold tau_r for high-error state classification.
    density_threshold : float
        Threshold tau_rho for high-density state classification.
    consistency_threshold : float
        Threshold tau_C for consistent state classification.
    redundancy_threshold : float
        Threshold tau_D for redundant state classification.
    noise_threshold : float
        Threshold for noise score classification.

    acquisition_budget : int
        Total budget for active data acquisition.
    action_mode : str
        Action allocation strategy.

    verbose : bool
        Whether to print progress information.
    output_dir : str
        Directory for saving outputs (logs, plots, serialized models).
    """

    # State discovery
    state_method: str = "kmeans"
    n_states: int = 10
    state_random_state: int = 42

    # Expert
    n_experts: int = 3
    expert_cost: list[float] | None = None

    # Reliability estimation
    reliability_method: str = "supervised"
    reliability_alpha: float = 1.0

    # Data classification thresholds
    error_threshold: float = 0.05
    density_threshold: float = 0.05
    consistency_threshold: float = 0.7
    redundancy_threshold: float = 0.8
    noise_threshold: float = 0.5

    # Action policy
    acquisition_budget: int = 100
    action_mode: str = "proportional"

    # Misc
    verbose: bool = True
    output_dir: str = "./scx_outputs"

    # Internal: extra keyword arguments forwarded to specific submodules
    _extra: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate configuration parameters.

        Returns
        -------
        bool
            True if all parameters are valid.

        Raises
        ------
        ValueError
            If any parameter is out of range or invalid.
        """
        if self.state_method not in _VALID_STATE_METHODS:
            raise ValueError(
                f"state_method={self.state_method!r} not in {_VALID_STATE_METHODS}"
            )
        if self.n_states < 2:
            raise ValueError(f"n_states must be >= 2, got {self.n_states}")
        if self.n_experts < 1:
            raise ValueError(f"n_experts must be >= 1, got {self.n_experts}")
        if self.expert_cost is not None:
            if len(self.expert_cost) != self.n_experts:
                raise ValueError(
                    f"expert_cost length {len(self.expert_cost)} != "
                    f"n_experts {self.n_experts}"
                )
            if any(c <= 0 for c in self.expert_cost):
                raise ValueError("All expert_cost values must be positive")
        if self.reliability_method not in _VALID_RELIABILITY_METHODS:
            raise ValueError(
                f"reliability_method={self.reliability_method!r} "
                f"not in {_VALID_RELIABILITY_METHODS}"
            )
        if not (0.0 <= self.reliability_alpha <= 10.0):
            raise ValueError(
                f"reliability_alpha should be in [0, 10], got {self.reliability_alpha}"
            )
        for name, val in [
            ("error_threshold", self.error_threshold),
            ("density_threshold", self.density_threshold),
            ("consistency_threshold", self.consistency_threshold),
            ("redundancy_threshold", self.redundancy_threshold),
            ("noise_threshold", self.noise_threshold),
        ]:
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"{name} must be in [0, 1], got {val}")
        if self.acquisition_budget < 1:
            raise ValueError(
                f"acquisition_budget must be >= 1, got {self.acquisition_budget}"
            )
        if self.action_mode not in _VALID_ACTION_MODES:
            raise ValueError(
                f"action_mode={self.action_mode!r} not in {_VALID_ACTION_MODES}"
            )
        return True

    def to_dict(self) -> dict[str, Any]:
        """Convert config to a plain dictionary."""
        d = asdict(self)
        d.pop("_extra", None)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SCXConfig":
        """Create config from a dictionary (unknown keys go to _extra)."""
        valid_keys = set(cls.__dataclass_fields__)
        known = {k: v for k, v in d.items() if k in valid_keys and k != "_extra"}
        extra = {k: v for k, v in d.items() if k not in valid_keys}
        config = cls(**known)
        config._extra = extra
        return config

    @classmethod
    def from_json(cls, path: str) -> "SCXConfig":
        """Load config from a JSON file."""
        with open(path, "r") as f:
            d = json.load(f)
        return cls.from_dict(d)

    def save(self, path: str) -> None:
        """Serialize config to a JSON file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def __repr__(self) -> str:
        items = [f"{k}={v!r}" for k, v in self.to_dict().items()]
        return f"SCXConfig({', '.join(items)})"
