# scx/state/space.py
# StateSpace -- container and query interface for the state space S = {s1, ..., sK}.

from __future__ import annotations

import pickle
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd


@dataclass
class StateInfo:
    """Metadata for a single state.

    Attributes
    ----------
    id : int
        State index / identifier.
    label : str
        Human-readable label (optional).
    centroid : np.ndarray
        Centroid coordinate in phi-space, shape (d,).
    radius : float
        Radius -- mean intra-state distance to centroid.
    count : int
        Number of samples belonging to this state.
    proportion : float
        Sample proportion rho(s) = count / total.
    """

    id: int
    label: str
    centroid: np.ndarray
    radius: float
    count: int
    proportion: float


class StateSpace:
    """Manages the state space S = {s_1, ..., s_K}.

    Stores per-state metadata (centroids, radii, counts, proportions) and
    optional hard / soft assignments from the discovery step.

    Parameters
    ----------
    n_states : int
        Number of states (K).
    """

    def __init__(self, n_states: int):
        self.n_states = n_states
        self.states: dict[int, StateInfo] = {}
        self.assignment: np.ndarray | None = None  # (N,) hard labels
        self.soft_assignment: np.ndarray | None = None  # (N, K) soft matrix

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_state(self, state: StateInfo) -> None:
        """Register a new state.

        Parameters
        ----------
        state : StateInfo
            State metadata to add.
        """
        self.states[state.id] = state

    def get_state(self, state_id: int) -> StateInfo:
        """Retrieve state metadata by id.

        Parameters
        ----------
        state_id : int
            State identifier.

        Returns
        -------
        StateInfo
        """
        if state_id not in self.states:
            raise KeyError(f"State {state_id} not found in state space.")
        return self.states[state_id]

    def remove_state(self, state_id: int) -> None:
        """Remove a state from the space.

        Parameters
        ----------
        state_id : int
            State identifier to remove.
        """
        if state_id not in self.states:
            raise KeyError(f"State {state_id} not found; cannot remove.")
        del self.states[state_id]
        self.n_states = len(self.states)

    # ------------------------------------------------------------------
    # Batch accessors
    # ------------------------------------------------------------------

    def get_centroids(self) -> np.ndarray:
        """Return all centroids as a matrix.

        Returns
        -------
        centroids : np.ndarray, shape (K, d)
        """
        ordered = sorted(self.states.values(), key=lambda s: s.id)
        return np.array([s.centroid for s in ordered])

    def get_proportions(self) -> np.ndarray:
        """Return all state proportions.

        Returns
        -------
        proportions : np.ndarray, shape (K,)
        """
        ordered = sorted(self.states.values(), key=lambda s: s.id)
        return np.array([s.proportion for s in ordered])

    # ------------------------------------------------------------------
    # Summary & serialization
    # ------------------------------------------------------------------

    def summary(self) -> pd.DataFrame:
        """Return a DataFrame summary of all states.

        Columns: id, label, radius, count, proportion.
        """
        ordered = sorted(self.states.values(), key=lambda s: s.id)
        rows = []
        for s in ordered:
            rows.append(
                {
                    "id": s.id,
                    "label": s.label,
                    "radius": s.radius,
                    "count": s.count,
                    "proportion": s.proportion,
                }
            )
        return pd.DataFrame(rows)

    def save(self, path: str) -> None:
        """Serialize the StateSpace to disk via pickle.

        Parameters
        ----------
        path : str
            File path to write.
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str) -> StateSpace:
        """Load a serialized StateSpace from disk.

        Parameters
        ----------
        path : str
            File path to read.

        Returns
        -------
        StateSpace
        """
        with open(path, "rb") as f:
            obj = pickle.load(f)
        if not isinstance(obj, StateSpace):
            raise TypeError(f"Loaded object is not a StateSpace (got {type(obj)}).")
        return obj
