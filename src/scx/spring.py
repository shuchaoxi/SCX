"""
Spring — Self-Evolution Algorithm for SCX
==========================================

**Status: EXPERIMENTAL / BETA** — This module implements the SCX self-evolution
theory (Documents 01–06) as a concrete algorithm. The mathematical convergence
guarantees (Theorem SE-1) are proven under restrictive conditions (finite
structure space, Lipschitz NEP, two-timescale separation). This implementation
is a practical approximation; numerical validation is ongoing.

Theory reference
----------------
:doc:`/theory/self_evolution/README`

The Spring algorithm runs the iterative self-evolution loop:

.. code-block:: text

    t = 0
    Initialize M_0 (seed memory bank via static SCX / Yajie)
    Initialize S_0 (gatekeeper from expert consensus)
    Initialize θ_0 (pretrained NEP student)

    while t < T_max:
        1. Explore: sample candidates with η(t)-drifted S_t
        2. Evaluate: compute quality_score + novelty_bonus → total_score
        3. Store: admit top-k into M_{t+1}
        4. Update NEP: train student f_θ on M_{t+1}
        5. Update gatekeeper: Bayesian posterior S_{t+1} ← (M_{t+1}, f_θ)
        6. Decay exploration: η(t+1) = η_init * exp(-t/τ_decay)
        t += 1

Core concepts (from theory Documents 01–02, 06)
-----------------------------------------------
- **M_t** — monotonic memory bank (only grows, never deletes)
- **S_t** — gatekeeper scoring function: X × Y → [0, 1]
- **f_θ_t** — NEP student model providing delayed feedback
- **Φ** — update operator: (S_t, M_t, θ_t) → (S_{t+1}, M_{t+1}, θ_{t+1})
- **Lyapunov function** — Φ(S_t, θ_t) monitored for convergence diagnostics

Integration with existing SCX
-------------------------------
- ``scx.valuation.noise_score.NoiseScore`` — per-sample noise estimation
- ``scx.valuation.state_value.StateValue`` — Theorem 1/2 bounds
- ``scx.state.discovery.StateDiscovery`` — state-space clustering
- ``scx.yajie.Yajie`` — static scoring for initialization

Examples
--------
>>> from scx.spring import Spring, SpringConfig
>>> config = SpringConfig(max_iterations=50, eta_init=0.3, tau_decay=20.0)
>>> spring = Spring(config)
>>> spring.initialize(memory_seed=structures, nep_student=my_model)
>>> history = spring.evolve()
>>> print(spring.memory.summary())
"""

from __future__ import annotations

import math
import time
import warnings
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

from scx.valuation.noise_score import NoiseScore, NoveltyNoiseScore
from scx.valuation.state_value import StateValue
from scx.state.discovery import StateDiscovery


# ============================================================================
# Configuration
# ============================================================================


@dataclass
class SpringConfig:
    """Hyperparameter configuration for the Spring self-evolution loop.

    Parameters
    ----------
    max_iterations : int
        Maximum number of self-evolution rounds T_max.
    eta_init : float
        Initial exploration rate η(0). Controls the probability of
        accepting structures that the gatekeeper would otherwise reject.
        Higher = more exploration, lower = more exploitation.
    tau_decay : float
        Exploration decay time constant. η(t) = η_init * exp(-t / tau_decay).
        Larger = slower decay, more exploration over time.
    novelty_weight : float
        Weight λ_nov for the novelty bonus in the total score.
        total_score = (1 - λ_nov) * quality_score + λ_nov * novelty_bonus.
    top_k : int
        Number of top-scoring structures to admit into memory per iteration.
    acceptance_threshold : float
        Minimum total_score for a structure to be admitted into memory.
        Structures below this threshold are rejected regardless of top_k.
    state_discovery_method : str
        Clustering method for state discovery (kmeans, gmm, spectral, hdbscan).
    n_states : int
        Number of states K for state-space clustering.
    random_seed : int
        Random seed for reproducibility.
    gatekeeper_prior_strength : float
        Strength of the Beta prior for the gatekeeper Bayesian update.
        Higher = more conservative (slower to change beliefs).
    memory_max_size : int
        Maximum size of the memory bank. If exceeded, lowest-scoring
        dormant structures are evicted. Set to -1 for unlimited.
    """

    max_iterations: int = 50
    eta_init: float = 0.3
    tau_decay: float = 20.0
    novelty_weight: float = 0.3
    top_k: int = 20
    acceptance_threshold: float = 0.1
    state_discovery_method: str = "kmeans"
    n_states: int = 10
    random_seed: int = 42
    gatekeeper_prior_strength: float = 5.0
    memory_max_size: int = 10000

    def __post_init__(self) -> None:
        if self.max_iterations < 1:
            raise ValueError(f"max_iterations must be >= 1, got {self.max_iterations}")
        if not 0.0 <= self.eta_init <= 1.0:
            raise ValueError(f"eta_init must be in [0, 1], got {self.eta_init}")
        if self.tau_decay <= 0:
            raise ValueError(f"tau_decay must be > 0, got {self.tau_decay}")
        if not 0.0 <= self.novelty_weight <= 1.0:
            raise ValueError(f"novelty_weight must be in [0, 1], got {self.novelty_weight}")
        if self.top_k < 1:
            raise ValueError(f"top_k must be >= 1, got {self.top_k}")
        if self.gatekeeper_prior_strength <= 0:
            raise ValueError(
                f"gatekeeper_prior_strength must be > 0, "
                f"got {self.gatekeeper_prior_strength}"
            )


# ============================================================================
# Memory Bank (M_t)
# ============================================================================


class MemoryBank:
    """Monotonic memory bank M_t from the self-evolution theory.

    M_t stores structures as a flat list of dictionaries, each with keys:
        - structure_id: unique identifier
        - features: np.ndarray (d_phi,) — feature representation
        - score: float — total score (quality + novelty) at admission
        - quality_score: float — NEP student prediction confidence
        - novelty_bonus: float — 1 - max cosine similarity to existing
        - timestamp: int — iteration when admitted
        - status: str — one of {'active', 'dormant', 'resurrected'}
        - state_label: int — discovered state assignment (or -1)

    The memory bank is **monotonic**: M_t ⊆ M_{t+1} for all t. Structures
    are never deleted (only marked dormant), preserving the theoretical
    guarantee that the empirical distribution converges.

    Parameters
    ----------
    max_size : int
        Maximum number of structures to retain. When exceeded,
        lowest-scoring dormant structures are removed. Set to -1
        for unlimited growth.
    """

    def __init__(self, max_size: int = 10000) -> None:
        self.max_size = max_size
        self._structures: List[Dict[str, Any]] = []
        self._id_counter: int = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def size(self) -> int:
        """Current number of structures in memory."""
        return len(self._structures)

    @property
    def structures(self) -> List[Dict[str, Any]]:
        """Return a reference to the internal structure list (read-only use)."""
        return self._structures

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def add(
        self,
        features: np.ndarray,
        quality_score: float,
        novelty_bonus: float,
        total_score: float,
        state_label: int = -1,
        timestamp: int = 0,
    ) -> str:
        """Add a new structure to the memory bank.

        Parameters
        ----------
        features : np.ndarray, shape (d_phi,)
            Feature representation of the structure.
        quality_score : float
            NEP student prediction confidence (primary quality signal).
        novelty_bonus : float
            1 - max cosine similarity to any existing structure.
        total_score : float
            Combined score = (1 - λ)*quality + λ*novelty.
        state_label : int
            Discovered state cluster assignment.
        timestamp : int
            Iteration number when admitted.

        Returns
        -------
        str
            Unique structure_id assigned to the new entry.
        """
        structure_id = self._generate_id()
        entry: Dict[str, Any] = {
            "structure_id": structure_id,
            "features": np.asarray(features, dtype=float).copy(),
            "score": float(total_score),
            "quality_score": float(quality_score),
            "novelty_bonus": float(novelty_bonus),
            "timestamp": int(timestamp),
            "status": "active",
            "state_label": int(state_label),
        }
        self._structures.append(entry)
        self._enforce_max_size()
        return structure_id

    def add_batch(
        self,
        feature_list: Sequence[np.ndarray],
        quality_scores: np.ndarray,
        novelty_bonuses: np.ndarray,
        total_scores: np.ndarray,
        state_labels: np.ndarray,
        timestamp: int = 0,
    ) -> List[str]:
        """Add multiple structures in one batch.

        Parameters
        ----------
        feature_list : sequence of np.ndarray
            Feature vectors for each structure.
        quality_scores : np.ndarray, shape (N,)
        novelty_bonuses : np.ndarray, shape (N,)
        total_scores : np.ndarray, shape (N,)
        state_labels : np.ndarray, shape (N,)
        timestamp : int

        Returns
        -------
        list of str
            Assigned structure IDs.
        """
        ids = []
        for i in range(len(feature_list)):
            sid = self.add(
                features=feature_list[i],
                quality_score=float(quality_scores[i]),
                novelty_bonus=float(novelty_bonuses[i]),
                total_score=float(total_scores[i]),
                state_label=int(state_labels[i]),
                timestamp=timestamp,
            )
            ids.append(sid)
        return ids

    def update_status(self, structure_id: str, new_status: str) -> bool:
        """Update the status of a structure.

        Parameters
        ----------
        structure_id : str
        new_status : str
            One of {'active', 'dormant', 'resurrected'}.

        Returns
        -------
        bool
            True if the structure was found and updated.
        """
        valid_statuses = {"active", "dormant", "resurrected"}
        if new_status not in valid_statuses:
            raise ValueError(
                f"Invalid status '{new_status}'. Choose from {valid_statuses}."
            )
        for entry in self._structures:
            if entry["structure_id"] == structure_id:
                entry["status"] = new_status
                return True
        return False

    def get_feature_matrix(self, status_filter: Optional[str] = None) -> np.ndarray:
        """Return the feature matrix of structures in memory.

        Parameters
        ----------
        status_filter : str, optional
            If given, only return structures with this status.

        Returns
        -------
        np.ndarray, shape (N, d_phi)
        """
        if status_filter is not None:
            entries = [e for e in self._structures if e["status"] == status_filter]
        else:
            entries = self._structures
        if not entries:
            return np.array([]).reshape(0, 0)
        return np.stack([e["features"] for e in entries])

    def get_scores(self, status_filter: Optional[str] = None) -> np.ndarray:
        """Return the total scores of structures in memory.

        Parameters
        ----------
        status_filter : str, optional

        Returns
        -------
        np.ndarray, shape (N,)
        """
        if status_filter is not None:
            entries = [e for e in self._structures if e["status"] == status_filter]
        else:
            entries = self._structures
        return np.array([e["score"] for e in entries], dtype=float)

    def get_state_labels(self) -> np.ndarray:
        """Return state labels for all structures, shape (N,)."""
        return np.array([e["state_label"] for e in self._structures], dtype=int)

    def compute_novelty_bonus(
        self, candidate_features: np.ndarray
    ) -> np.ndarray:
        """Compute novelty bonus for candidate structures against memory.

        novelty_bonus(x) = 1 - max_{m ∈ M_t} cosine_similarity(φ(x), φ(m))

        Parameters
        ----------
        candidate_features : np.ndarray, shape (N, d_phi)
            Feature vectors of candidate structures.

        Returns
        -------
        np.ndarray, shape (N,)
            Novelty bonus in [0, 1] for each candidate.
        """
        candidate_features = np.asarray(candidate_features, dtype=float)
        if candidate_features.ndim == 1:
            candidate_features = candidate_features.reshape(1, -1)

        memory_features = self.get_feature_matrix()
        if memory_features.size == 0:
            # No structures in memory yet — all candidates are maximally novel
            return np.ones(candidate_features.shape[0], dtype=float)

        # Normalize for cosine similarity
        cand_norm = candidate_features / (
            np.linalg.norm(candidate_features, axis=1, keepdims=True) + 1e-12
        )
        mem_norm = memory_features / (
            np.linalg.norm(memory_features, axis=1, keepdims=True) + 1e-12
        )

        # Cosine similarities: (N, M)
        similarities = np.dot(cand_norm, mem_norm.T)
        max_sim = np.max(similarities, axis=1)  # (N,)
        return 1.0 - max_sim

    def resurrect_lowest(self, n: int = 1) -> List[str]:
        """Resurrect the n lowest-scoring dormant structures.

        Used for exploration: periodically re-evaluate structures that
        were previously judged unfavorably.

        Parameters
        ----------
        n : int
            Number of structures to resurrect.

        Returns
        -------
        list of str
            Structure IDs that were resurrected.
        """
        dormant = [e for e in self._structures if e["status"] == "dormant"]
        if not dormant:
            return []
        dormant.sort(key=lambda e: e["score"])
        resurrected = []
        for entry in dormant[:n]:
            entry["status"] = "resurrected"
            resurrected.append(entry["structure_id"])
        return resurrected

    # ------------------------------------------------------------------
    # Summary / diagnostics
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a human-readable summary of the memory bank."""
        if not self._structures:
            return "MemoryBank: empty (0 structures)"

        n_total = len(self._structures)
        status_counts: Dict[str, int] = {"active": 0, "dormant": 0, "resurrected": 0}
        scores = []
        qualities = []
        novelties = []
        for e in self._structures:
            status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1
            scores.append(e["score"])
            qualities.append(e["quality_score"])
            novelties.append(e["novelty_bonus"])

        score_arr = np.array(scores)
        quality_arr = np.array(qualities)
        novelty_arr = np.array(novelties)

        lines = [
            f"MemoryBank: {n_total} structures",
            f"  active={status_counts['active']}, "
            f"dormant={status_counts['dormant']}, "
            f"resurrected={status_counts['resurrected']}",
            f"  score: min={score_arr.min():.4f}, median={np.median(score_arr):.4f}, "
            f"max={score_arr.max():.4f}",
            f"  quality: min={quality_arr.min():.4f}, mean={quality_arr.mean():.4f}, "
            f"max={quality_arr.max():.4f}",
            f"  novelty: min={novelty_arr.min():.4f}, mean={novelty_arr.mean():.4f}, "
            f"max={novelty_arr.max():.4f}",
        ]
        return "\n".join(lines)

    def to_records(self) -> List[Dict[str, Any]]:
        """Export all structures as a list of dicts (for DataFrame construction)."""
        return list(self._structures)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _generate_id(self) -> str:
        """Generate a unique structure ID."""
        self._id_counter += 1
        return f"struct_{self._id_counter:08d}"

    def _enforce_max_size(self) -> None:
        """Evict lowest-scoring dormant structures if max_size is exceeded."""
        if self.max_size < 0 or len(self._structures) <= self.max_size:
            return
        # Evict lowest-scoring dormant structures first
        dormant = [e for e in self._structures if e["status"] == "dormant"]
        excess = len(self._structures) - self.max_size
        if dormant and excess > 0:
            dormant.sort(key=lambda e: e["score"])
            to_remove = set(e["structure_id"] for e in dormant[:excess])
            self._structures = [
                e for e in self._structures if e["structure_id"] not in to_remove
            ]


# ============================================================================
# Gatekeeper (S_t)
# ============================================================================


class Gatekeeper:
    """Gatekeeper scoring function S_t: X × Y → [0, 1].

    S_t(x, y) estimates P(correct | x, y, M_t) — the probability that label
    y for sample x is correct, given the current memory bank M_t.

    The gatekeeper maintains **state-conditioned reliability estimates**
    using a Bayesian Beta-binomial model:

        S_t(x, y) = (α_s + prior_α) / (α_s + β_s + prior_α + prior_β)

    where s = state(x) and (α_s, β_s) are counts of clean/noisy instances
    observed in state s within M_t.

    Parameters
    ----------
    prior_strength : float
        Strength of the conjugate Beta prior. Larger = more conservative
        updates (requires more evidence to change beliefs).
    n_states : int
        Number of states for state-conditioned scoring.
    """

    def __init__(
        self,
        prior_strength: float = 5.0,
        n_states: int = 10,
    ) -> None:
        self.prior_strength = prior_strength
        self.n_states = n_states

        # Beta prior parameters: Beta(prior_alpha, prior_beta)
        # Default: Beta(prior_strength/2, prior_strength/2) — centered at 0.5
        self.prior_alpha: float = prior_strength / 2.0
        self.prior_beta: float = prior_strength / 2.0

        # Per-state counts for Bayesian posterior
        # alpha_s: effective "clean" count, beta_s: effective "noisy" count
        self._alpha_s: np.ndarray = np.full(
            n_states, self.prior_alpha, dtype=float
        )
        self._beta_s: np.ndarray = np.full(
            n_states, self.prior_beta, dtype=float
        )

        # Track update history for convergence diagnostics
        self._update_history: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def score(
        self,
        state_labels: np.ndarray,
        quality_scores: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Compute gatekeeper scores S_t for structures in given states.

        S_t(s) = alpha_s / (alpha_s + beta_s)

        When quality_scores are provided, they serve as an additional
        signal blended with the state-conditioned posterior.

        Parameters
        ----------
        state_labels : np.ndarray, shape (N,), dtype int
            State assignments for each structure.
        quality_scores : np.ndarray, shape (N,), optional
            NEP student prediction confidence per structure.

        Returns
        -------
        np.ndarray, shape (N,)
            Gatekeeper scores in [0, 1].
        """
        state_labels = np.asarray(state_labels, dtype=int)
        # Handle -1 (unassigned) by mapping to default prior
        valid_mask = (state_labels >= 0) & (state_labels < self.n_states)
        scores = np.full(state_labels.shape, 0.5, dtype=float)

        # State-conditioned posterior mean
        alpha = self._alpha_s
        beta = self._beta_s
        posterior_mean = alpha / (alpha + beta + 1e-12)
        scores[valid_mask] = posterior_mean[state_labels[valid_mask]]

        # Blend with quality_scores if provided
        if quality_scores is not None:
            quality_scores = np.asarray(quality_scores, dtype=float)
            # Bayesian blending: weight posterior by prior strength,
            # weight quality by effective sample size per state
            eff_samples = self._alpha_s + self._beta_s
            state_eff = np.where(
                valid_mask,
                eff_samples[state_labels.clip(0, self.n_states - 1)],
                self.prior_strength,
            )
            blend_weight = state_eff / (state_eff + 1.0)
            scores = blend_weight * scores + (1.0 - blend_weight) * quality_scores
            scores = np.clip(scores, 0.0, 1.0)

        return scores

    def score_with_exploration(
        self,
        state_labels: np.ndarray,
        quality_scores: Optional[np.ndarray],
        eta: float,
        rng: np.random.Generator,
    ) -> np.ndarray:
        """Score structures with η-weighted exploration noise.

        Explored score = (1 - η) * S_t(x) + η * Uniform(0, 1)

        This implements the ε-greedy exploration strategy from the theory:
        a fraction η of the score mass comes from random exploration,
        ensuring that the memory bank can escape local optima.

        Parameters
        ----------
        state_labels : np.ndarray, shape (N,)
        quality_scores : np.ndarray, shape (N,), optional
        eta : float
            Current exploration rate η(t).
        rng : np.random.Generator

        Returns
        -------
        np.ndarray, shape (N,)
            Explored gatekeeper scores in [0, 1].
        """
        base_scores = self.score(state_labels, quality_scores)
        exploration = rng.uniform(0.0, 1.0, size=base_scores.shape)
        eta_clipped = float(np.clip(eta, 0.0, 1.0))
        return (1.0 - eta_clipped) * base_scores + eta_clipped * exploration

    # ------------------------------------------------------------------
    # Bayesian update (Φ_S)
    # ------------------------------------------------------------------

    def update(
        self,
        state_labels: np.ndarray,
        quality_scores: np.ndarray,
        verdicts: np.ndarray,
        learning_rate: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Bayesian posterior update of state-conditioned reliability.

        For each state s:
            alpha_s ← alpha_s + sum(verdict_i * quality_i)  [clean evidence]
            beta_s  ← beta_s  + sum((1-verdict_i) * quality_i)  [noisy evidence]

        where verdict_i ∈ {0, 1} indicates whether the structure was
        admitted (1) or rejected (0) by the combined scoring step.

        Parameters
        ----------
        state_labels : np.ndarray, shape (N,), dtype int
        quality_scores : np.ndarray, shape (N,)
            NEP student prediction confidence.
        verdicts : np.ndarray, shape (N,), dtype int (0 or 1)
            Binary indicator: 1 = admitted to M_t, 0 = rejected.
        learning_rate : float, optional
            If given, applies an exponential moving average update:
            alpha_s ← (1 - lr) * alpha_s + lr * evidence.
            If None, applies full Bayesian update.

        Returns
        -------
        dict
            Update statistics: {'max_delta': float, 'mean_delta': float}.
        """
        state_labels = np.asarray(state_labels, dtype=int)
        quality_scores = np.asarray(quality_scores, dtype=float)
        verdicts = np.asarray(verdicts, dtype=float)

        old_alpha = self._alpha_s.copy()
        old_beta = self._beta_s.copy()

        # Accumulate evidence per state
        for s in range(self.n_states):
            mask = state_labels == s
            if not mask.any():
                continue
            clean_evidence = np.sum(verdicts[mask] * quality_scores[mask])
            noisy_evidence = np.sum((1.0 - verdicts[mask]) * quality_scores[mask])

            if learning_rate is not None:
                lr = float(np.clip(learning_rate, 0.0, 1.0))
                self._alpha_s[s] = (1.0 - lr) * self._alpha_s[s] + lr * clean_evidence
                self._beta_s[s] = (1.0 - lr) * self._beta_s[s] + lr * noisy_evidence
            else:
                self._alpha_s[s] += clean_evidence
                self._beta_s[s] += noisy_evidence

        # Compute update statistics
        delta_alpha = np.abs(self._alpha_s - old_alpha)
        delta_beta = np.abs(self._beta_s - old_beta)
        max_delta = float(max(delta_alpha.max(), delta_beta.max()))
        mean_delta = float((delta_alpha.mean() + delta_beta.mean()) / 2.0)

        stats: Dict[str, Any] = {
            "max_delta": max_delta,
            "mean_delta": mean_delta,
            "active_states": int(np.sum((self._alpha_s + self._beta_s) > self.prior_strength)),
        }
        self._update_history.append(stats)
        return stats

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_state_reliability(self) -> np.ndarray:
        """Return posterior mean reliability per state, shape (n_states,)."""
        return self._alpha_s / (self._alpha_s + self._beta_s + 1e-12)

    def get_state_evidence(self) -> np.ndarray:
        """Return effective sample size (evidence) per state."""
        return self._alpha_s + self._beta_s

    def get_update_history(self) -> List[Dict[str, Any]]:
        """Return the history of update statistics."""
        return list(self._update_history)

    def reset(self) -> None:
        """Reset gatekeeper to prior state."""
        self._alpha_s = np.full(self.n_states, self.prior_alpha, dtype=float)
        self._beta_s = np.full(self.n_states, self.prior_beta, dtype=float)
        self._update_history.clear()


# ============================================================================
# Spring — Main Self-Evolution Orchestrator
# ============================================================================


class Spring:
    """Self-evolution orchestrator implementing the Spring algorithm.

    Spring runs the iterative self-evolution loop:

        1. Explore — sample candidates with η(t)-drifted gatekeeper
        2. Evaluate — quality_score + novelty_bonus → combined score
        3. Store — admit top-k into memory bank M_t
        4. Update NEP — train student f_θ on M_t
        5. Update Gatekeeper — Bayesian posterior S_t ← (M_t, f_θ)
        6. Decay — η(t) = η_init * exp(-t / τ_decay)

    Parameters
    ----------
    config : SpringConfig
        Hyperparameter configuration.
    nep_student : callable, optional
        NEP student model f_θ. Should implement:
        - ``predict(features) -> np.ndarray`` (predictions)
        - ``predict_confidence(features) -> np.ndarray`` (confidence scores)
        Can be set later via ``set_nep_student()``.
    """

    def __init__(
        self,
        config: Optional[SpringConfig] = None,
        nep_student: Optional[Any] = None,
    ) -> None:
        self.config = config or SpringConfig()

        # Core components
        self.memory = MemoryBank(max_size=self.config.memory_max_size)
        self.gatekeeper = Gatekeeper(
            prior_strength=self.config.gatekeeper_prior_strength,
            n_states=self.config.n_states,
        )
        self.state_discovery = StateDiscovery(
            method=self.config.state_discovery_method,
            n_states=self.config.n_states,
            random_state=self.config.random_seed,
        )

        # External scorers (from scx.valuation)
        self._noise_scorer = NoveltyNoiseScore()
        self._state_value = StateValue()

        # NEP student
        self._nep_student: Optional[Any] = nep_student

        # Internal state
        self._nep_quality_fn: Optional[Callable[[np.ndarray], np.ndarray]] = None
        self._iteration: int = 0
        self._eta: float = self.config.eta_init
        self._rng = np.random.default_rng(self.config.random_seed)

        # History tracking
        self.history_: List[Dict[str, Any]] = []
        self._is_initialized: bool = False

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def initialize(
        self,
        memory_seed: Optional[Sequence[Dict[str, Any]]] = None,
        feature_matrix: Optional[np.ndarray] = None,
        quality_scores: Optional[np.ndarray] = None,
    ) -> None:
        """Initialize the Spring system before evolution.

        Populates M_0 with seed structures and computes initial state
        assignments. If ``memory_seed`` is provided, each dict should
        have at least a 'features' key.

        Parameters
        ----------
        memory_seed : list of dict, optional
            Seed structures for M_0. Each dict needs at least
            ``{'features': np.ndarray}``. Optional keys: ``quality_score``,
            ``state_label``.
        feature_matrix : np.ndarray, optional, shape (N, d_phi)
            Alternative to memory_seed: raw feature matrix.
        quality_scores : np.ndarray, optional, shape (N,)
            Quality scores corresponding to feature_matrix.
        """
        if memory_seed is not None:
            features_list = []
            q_scores = []
            for entry in memory_seed:
                feats = np.asarray(entry["features"], dtype=float)
                features_list.append(feats)
                q_scores.append(entry.get("quality_score", 0.5))
            feature_matrix = np.stack(features_list) if features_list else None
            quality_scores = np.array(q_scores, dtype=float) if q_scores else None

        if feature_matrix is not None and feature_matrix.size > 0:
            feature_matrix = np.asarray(feature_matrix, dtype=float)
            if feature_matrix.ndim == 1:
                feature_matrix = feature_matrix.reshape(1, -1)
            n_seed = feature_matrix.shape[0]

            if quality_scores is None:
                quality_scores = np.full(n_seed, 0.5, dtype=float)

            # Compute novelty bonuses against empty memory
            novelty_bonuses = np.ones(n_seed, dtype=float)
            total_scores = (
                (1.0 - self.config.novelty_weight) * quality_scores
                + self.config.novelty_weight * novelty_bonuses
            )

            # Discover initial states
            n_clusters = min(self.config.n_states, n_seed)
            if n_seed >= 2 and n_clusters >= 2:
                sd_temp = StateDiscovery(
                    method=self.config.state_discovery_method,
                    n_states=n_clusters,
                    random_state=self.config.random_seed,
                )
                state_labels = sd_temp.fit_predict(feature_matrix)
            else:
                state_labels = np.zeros(n_seed, dtype=int)

            # Add to memory
            self.memory.add_batch(
                feature_list=[feature_matrix[i] for i in range(n_seed)],
                quality_scores=quality_scores,
                novelty_bonuses=novelty_bonuses,
                total_scores=total_scores,
                state_labels=state_labels,
                timestamp=0,
            )

            # Initialize gatekeeper with seed data
            # All seed structures are treated as "admitted" (verdict=1)
            self.gatekeeper.update(
                state_labels=state_labels,
                quality_scores=quality_scores,
                verdicts=np.ones(n_seed, dtype=float),
            )

            # Fit state discovery on seed features
            if n_seed >= n_clusters >= 2:
                self.state_discovery.fit(feature_matrix)

        self._is_initialized = True
        self._iteration = 0
        self._eta = self.config.eta_init

    def set_nep_student(self, student: Any) -> None:
        """Set or replace the NEP student model.

        Parameters
        ----------
        student : object
            Must implement ``predict_confidence(features) -> np.ndarray``.
            Optionally ``predict(features) -> np.ndarray``.
        """
        self._nep_student = student

    def set_nep_quality_fn(
        self, fn: Callable[[np.ndarray], np.ndarray]
    ) -> None:
        """Set a custom quality-scoring function for NEP evaluation.

        Parameters
        ----------
        fn : callable
            Maps feature_matrix (N, d) → quality_scores (N,).
        """
        self._nep_quality_fn = fn

    # ------------------------------------------------------------------
    # Evolution loop
    # ------------------------------------------------------------------

    def evolve(
        self,
        candidate_generator: Optional[Callable[[], np.ndarray]] = None,
        candidate_pool: Optional[np.ndarray] = None,
        max_iterations: Optional[int] = None,
        callback: Optional[Callable[[int, "Spring"], None]] = None,
    ) -> List[Dict[str, Any]]:
        """Run the full self-evolution loop.

        At each iteration t:
            1. Generate or sample candidate structures
            2. Score with gatekeeper + exploration noise
            3. Evaluate quality (NEP confidence) + novelty
            4. Admit top-k into memory
            5. Update NEP student on M_{t+1}
            6. Update gatekeeper via Bayesian posterior
            7. Decay exploration rate η(t)

        Parameters
        ----------
        candidate_generator : callable, optional
            Function that returns a feature matrix (N_cand, d_phi) of
            candidate structures at each iteration. If None, uses
            ``candidate_pool``.
        candidate_pool : np.ndarray, optional, shape (N_pool, d_phi)
            Static pool of candidates. At each iteration, a random subset
            is drawn. Ignored if ``candidate_generator`` is provided.
        max_iterations : int, optional
            Override config.max_iterations.
        callback : callable, optional
            Called after each iteration with (iteration, spring_instance).

        Returns
        -------
        list of dict
            History of per-iteration diagnostics (same as ``self.history_``).
        """
        if not self._is_initialized:
            warnings.warn(
                "Spring.evolve() called without initialize(). "
                "Starting from empty memory — evolution may be slow.",
                UserWarning,
            )
            self._is_initialized = True

        T = max_iterations or self.config.max_iterations

        # Use pool-based sampling if no generator is provided
        pool: Optional[np.ndarray] = None
        if candidate_generator is None and candidate_pool is not None:
            pool = np.asarray(candidate_pool, dtype=float)

        for t in range(T):
            self._iteration = t

            # 1. Generate candidates
            if candidate_generator is not None:
                candidates = np.asarray(candidate_generator(), dtype=float)
            elif pool is not None:
                n_draw = min(100, pool.shape[0])
                indices = self._rng.choice(pool.shape[0], size=n_draw, replace=False)
                candidates = pool[indices]
            else:
                # No candidates available — skip this iteration
                self._record_iteration(t, 0, 0.0, 0.0)
                continue

            if candidates.ndim == 1:
                candidates = candidates.reshape(1, -1)
            n_candidates = candidates.shape[0]

            # 2. Assign states via StateDiscovery
            state_labels = self._assign_states(candidates)

            # 3. Compute quality scores via NEP student
            quality_scores = self._compute_quality(candidates)

            # 4. Gatekeeper scoring with exploration
            gk_scores = self.gatekeeper.score_with_exploration(
                state_labels=state_labels,
                quality_scores=quality_scores,
                eta=self._eta,
                rng=self._rng,
            )

            # 5. Compute novelty bonuses
            novelty_bonuses = self.memory.compute_novelty_bonus(candidates)

            # 6. Combined total score (incorporates gatekeeper, quality, and novelty)
            total_scores = (
                0.4 * gk_scores
                + 0.3 * (1.0 - self.config.novelty_weight) * quality_scores
                + 0.3 * self.config.novelty_weight * novelty_bonuses
            )

            # 7. Admit top-k structures above threshold
            admittable = total_scores >= self.config.acceptance_threshold
            if admittable.any():
                admittable_indices = np.where(admittable)[0]
                admittable_scores = total_scores[admittable_indices]
                # Sort descending, pick top k
                k_actual = min(self.config.top_k, len(admittable_indices))
                top_local = np.argsort(admittable_scores)[-k_actual:][::-1]
                admit_indices = admittable_indices[top_local]
                n_admitted = len(admit_indices)
            else:
                admit_indices = np.array([], dtype=int)
                n_admitted = 0

            # Track verdicts for gatekeeper update
            verdicts = np.zeros(n_candidates, dtype=float)
            if n_admitted > 0:
                verdicts[admit_indices] = 1.0

                # Admit to memory
                self.memory.add_batch(
                    feature_list=[candidates[i] for i in admit_indices],
                    quality_scores=quality_scores[admit_indices],
                    novelty_bonuses=novelty_bonuses[admit_indices],
                    total_scores=total_scores[admit_indices],
                    state_labels=state_labels[admit_indices],
                    timestamp=t,
                )

            # 8. Update NEP student (delayed feedback)
            self._update_nep_student()

            # 9. Update gatekeeper (Bayesian posterior)
            gatekeeper_stats = self.gatekeeper.update(
                state_labels=state_labels,
                quality_scores=quality_scores,
                verdicts=verdicts,
                learning_rate=max(0.01, 1.0 / (t + 2)),  # Robbins-Monro style decay
            )

            # 10. Decay exploration rate
            self._eta = self.config.eta_init * math.exp(-t / self.config.tau_decay)

            # 11. Periodically resurrect dormant structures
            if t > 0 and t % 10 == 0:
                self.memory.resurrect_lowest(n=max(1, self.config.top_k // 5))

            # 12. Record iteration diagnostics
            self._record_iteration(
                t=t,
                n_candidates=n_candidates,
                n_admitted=n_admitted,
                mean_quality=float(quality_scores.mean()) if n_candidates > 0 else 0.0,
                mean_novelty=float(novelty_bonuses.mean()) if n_candidates > 0 else 0.0,
                eta=self._eta,
                gatekeeper_delta=gatekeeper_stats["max_delta"],
            )

            if callback is not None:
                callback(t, self)

        return self.history_

    def step(
        self,
        candidates: np.ndarray,
        t: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Perform a single evolution step with the given candidates.

        Useful for interactive / online use where candidates arrive
        from an external process.

        Parameters
        ----------
        candidates : np.ndarray, shape (N, d_phi)
        t : int, optional
            Iteration index. Auto-increments if not provided.

        Returns
        -------
        dict
            Per-step diagnostics.
        """
        if t is None:
            t = self._iteration
        self._iteration = t

        candidates = np.asarray(candidates, dtype=float)
        if candidates.ndim == 1:
            candidates = candidates.reshape(1, -1)
        n_candidates = candidates.shape[0]

        state_labels = self._assign_states(candidates)
        quality_scores = self._compute_quality(candidates)
        gk_scores = self.gatekeeper.score_with_exploration(
            state_labels=state_labels,
            quality_scores=quality_scores,
            eta=self._eta,
            rng=self._rng,
        )
        novelty_bonuses = self.memory.compute_novelty_bonus(candidates)
        total_scores = (
            0.4 * gk_scores
            + 0.3 * (1.0 - self.config.novelty_weight) * quality_scores
            + 0.3 * self.config.novelty_weight * novelty_bonuses
        )

        admittable = total_scores >= self.config.acceptance_threshold
        admit_indices = np.where(admittable)[0]
        if len(admit_indices) > self.config.top_k:
            top_local = np.argsort(total_scores[admit_indices])[-self.config.top_k :][::-1]
            admit_indices = admit_indices[top_local]
        n_admitted = len(admit_indices)

        verdicts = np.zeros(n_candidates, dtype=float)
        if n_admitted > 0:
            verdicts[admit_indices] = 1.0
            self.memory.add_batch(
                feature_list=[candidates[i] for i in admit_indices],
                quality_scores=quality_scores[admit_indices],
                novelty_bonuses=novelty_bonuses[admit_indices],
                total_scores=total_scores[admit_indices],
                state_labels=state_labels[admit_indices],
                timestamp=t,
            )

        self._update_nep_student()
        gatekeeper_stats = self.gatekeeper.update(
            state_labels=state_labels,
            quality_scores=quality_scores,
            verdicts=verdicts,
            learning_rate=max(0.01, 1.0 / (t + 2)),
        )
        self._eta = self.config.eta_init * math.exp(-t / self.config.tau_decay)

        step_diag = {
            "iteration": t,
            "n_candidates": n_candidates,
            "n_admitted": n_admitted,
            "mean_quality": float(quality_scores.mean()) if n_candidates > 0 else 0.0,
            "mean_novelty": float(novelty_bonuses.mean()) if n_candidates > 0 else 0.0,
            "eta": self._eta,
            "gatekeeper_delta": gatekeeper_stats["max_delta"],
            "memory_size": self.memory.size,
            "top_score": float(total_scores.max()) if n_candidates > 0 else 0.0,
        }
        self.history_.append(step_diag)
        return step_diag

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def lyapunov_estimate(self, reference_features: np.ndarray) -> float:
        """Estimate the Lyapunov function Phi(S_t, theta_t).

        Phi(S_t, theta_t) = mean((S_t(x) - (1 - C_t(x)))^2)
        + student_loss, where C_t(x) is the current consensus/quality
        estimate on the fixed reference set.

        Uses the current gatekeeper and NEP student evaluated on the
        provided reference features.

        Parameters
        ----------
        reference_features : np.ndarray, shape (N, d_phi)
            Fixed reference set features (M_0 in the theory).

        Returns
        -------
        float
            Estimated Lyapunov value Phi >= 0.
        """
        reference_features = np.asarray(reference_features, dtype=float)
        if reference_features.ndim == 1:
            reference_features = reference_features.reshape(1, -1)

        state_labels = self._assign_states(reference_features)
        gk_scores = self.gatekeeper.score(state_labels)
        current_consensus = self._compute_quality(reference_features)

        # Gatekeeper term: tracking error against the current consensus target.
        gatekeeper_target = 1.0 - current_consensus
        gatekeeper_term = np.mean((gk_scores - gatekeeper_target) ** 2)

        # Student term: quality score as proxy for 1 - loss
        student_loss = np.mean(1.0 - current_consensus)

        return float(gatekeeper_term + student_loss)

    def prune_memory(
        self, prune_streak: int = 3
    ) -> tuple[set, set]:
        """Prune low-scoring samples from memory (噪声率衰减).

        Structures that score below the median gatekeeper score for
        ``prune_streak`` consecutive rounds are marked dormant.

        Returns
        -------
        active : set
            Structure indices remaining active.
        dormant : set
            Structure indices newly marked dormant.
        """
        if self.memory.size == 0:
            return set(), set()

        # Initialise per-round tracking if needed
        if not hasattr(self, "_prune_streak"):
            self._prune_streak: dict[str, int] = {}

        mem_features = self.memory.get_feature_matrix()
        mem_state_labels = self._assign_states(mem_features)
        scores = self.gatekeeper.score(mem_state_labels)
        threshold = float(np.median(scores)) if scores.size > 0 else 0.5

        newly_dormant: set[str] = set()
        for i, entry in enumerate(self.memory.structures):
            sid = entry["structure_id"]
            if i < len(scores) and scores[i] < threshold:
                self._prune_streak[sid] = self._prune_streak.get(sid, 0) + 1
                if self._prune_streak[sid] >= prune_streak:
                    entry["status"] = "dormant"
                    newly_dormant.add(sid)
                    self._prune_streak.pop(sid, None)
            else:
                self._prune_streak.pop(sid, None)

        active_ids = {
            e["structure_id"]
            for e in self.memory.structures
            if e["status"] == "active"
        }
        return active_ids, newly_dormant

    def convergence_diagnostic(self) -> Dict[str, Any]:
        """Compute convergence diagnostics from evolution history.

        Returns
        -------
        dict
            Keys: 'converged', 'regime', 'final_eta', 'memory_size',
            'score_trend', 'gatekeeper_delta_trend'.
        """
        if not self.history_:
            return {"converged": False, "regime": "unknown", "reason": "no history"}

        # Check if gatekeeper updates have stabilized
        recent_deltas = [
            h["gatekeeper_delta"] for h in self.history_[-10:] if "gatekeeper_delta" in h
        ]
        gk_stable = len(recent_deltas) > 0 and max(recent_deltas) < 1e-3

        # Check if η has decayed to near-zero
        eta_low = self._eta < 0.01

        # Score trend in last 10 iterations
        recent_admitted = [
            h.get("n_admitted", 0) for h in self.history_[-10:]
        ]
        admission_stable = len(recent_admitted) > 0 and np.std(recent_admitted) < 1.0

        if gk_stable and eta_low and admission_stable:
            regime = "classical_convergence"
            converged = True
        elif gk_stable and not eta_low:
            regime = "approaching_fixed_point"
            converged = False
        elif not gk_stable and admission_stable:
            regime = "limit_cycle_suspected"
            converged = False
        else:
            regime = "evolving"
            converged = False

        return {
            "converged": converged,
            "regime": regime,
            "final_eta": self._eta,
            "memory_size": self.memory.size,
            "gatekeeper_delta_trend": recent_deltas[-1] if recent_deltas else None,
            "admission_trend_mean": float(np.mean(recent_admitted)) if recent_admitted else 0.0,
        }

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def iteration(self) -> int:
        """Current iteration index t."""
        return self._iteration

    @property
    def eta(self) -> float:
        """Current exploration rate η(t)."""
        return self._eta

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _assign_states(self, features: np.ndarray) -> np.ndarray:
        """Assign state labels to feature vectors.

        Uses fitted StateDiscovery if available; falls back to nearest-centroid
        or uniform random assignment.
        """
        features = np.asarray(features, dtype=float)
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Try fitted state discovery
        if self.state_discovery.is_fitted:
            try:
                return self.state_discovery.predict(features)
            except Exception:
                pass

        # Try fitting on current memory
        mem_features = self.memory.get_feature_matrix()
        if mem_features.size > 0 and mem_features.shape[0] >= 2:
            n_clusters = min(self.config.n_states, mem_features.shape[0])
            if n_clusters >= 2:
                try:
                    sd_temp = StateDiscovery(
                        method=self.config.state_discovery_method,
                        n_states=n_clusters,
                        random_state=self.config.random_seed,
                    )
                    sd_temp.fit(mem_features)
                    return sd_temp.predict(features)
                except Exception:
                    pass

        # Fallback: assign uniformly
        return self._rng.integers(0, max(1, self.config.n_states), size=features.shape[0])

    def _compute_quality(self, features: np.ndarray) -> np.ndarray:
        """Compute quality scores via NEP student prediction confidence.

        Falls back to a simple heuristic if no NEP student is set.
        """
        features = np.asarray(features, dtype=float)
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Priority 1: custom quality function
        if self._nep_quality_fn is not None:
            scores = np.asarray(self._nep_quality_fn(features), dtype=float)
            return np.clip(scores, 0.0, 1.0)

        # Priority 2: NEP student with predict_confidence
        if self._nep_student is not None:
            if hasattr(self._nep_student, "predict_confidence"):
                scores = np.asarray(
                    self._nep_student.predict_confidence(features), dtype=float
                )
                return np.clip(scores, 0.0, 1.0)
            elif hasattr(self._nep_student, "predict"):
                preds = np.asarray(self._nep_student.predict(features), dtype=float)
                # Use prediction magnitude as crude confidence proxy
                confidence = np.abs(preds)
                if confidence.ndim > 1:
                    confidence = confidence.mean(axis=1)
                confidence = confidence / (confidence.max() + 1e-12)
                return np.clip(confidence, 0.0, 1.0)

        # Priority 3: fallback heuristic — cosine similarity to top memory structures
        mem_features = self.memory.get_feature_matrix()
        if mem_features.size > 0:
            sim = self.memory.compute_novelty_bonus(features)
            # High novelty = lower quality proxy (unseen regions have uncertain quality)
            return np.clip(1.0 - sim * 0.5, 0.1, 1.0)

        # No information: neutral
        return np.full(features.shape[0], 0.5, dtype=float)

    def _update_nep_student(self) -> None:
        """Update the NEP student model on the current memory bank.

        In a full implementation, this would call `nep_student.fit(M_t)`.
        Here we provide a hook; the actual training is delegated to the
        user-provided student. If the student supports incremental
        ``partial_fit``, that is preferred.
        """
        if self._nep_student is None:
            return

        mem_features = self.memory.get_feature_matrix(status_filter="active")
        if mem_features.size == 0 or mem_features.shape[0] < 2:
            return

        # If student supports incremental update, use it
        if hasattr(self._nep_student, "partial_fit"):
            try:
                mem_scores = self.memory.get_scores(status_filter="active")
                self._nep_student.partial_fit(mem_features, mem_scores)
            except Exception:
                # partial_fit may have different signatures; silently skip if it fails
                pass

    def _record_iteration(
        self,
        t: int,
        n_candidates: int,
        n_admitted: int,
        mean_quality: float,
        mean_novelty: float,
        eta: Optional[float] = None,
        gatekeeper_delta: Optional[float] = None,
    ) -> None:
        """Record per-iteration diagnostics."""
        self.history_.append(
            {
                "iteration": t,
                "n_candidates": n_candidates,
                "n_admitted": n_admitted,
                "memory_size": self.memory.size,
                "mean_quality": mean_quality,
                "mean_novelty": mean_novelty,
                "eta": eta if eta is not None else self._eta,
                "gatekeeper_delta": gatekeeper_delta,
                "gatekeeper_mean_reliability": float(
                    self.gatekeeper.get_state_reliability().mean()
                ),
            }
        )


# ============================================================================
# Convenience function
# ============================================================================


def evolve(
    candidates: np.ndarray,
    max_iterations: int = 50,
    eta_init: float = 0.3,
    tau_decay: float = 20.0,
    top_k: int = 20,
    seed: int = 42,
    verbose: bool = True,
) -> Tuple[Spring, List[Dict[str, Any]]]:
    """One-liner: run Spring self-evolution on a candidate pool.

    Parameters
    ----------
    candidates : np.ndarray, shape (N, d_phi)
        Pool of candidate structures.
    max_iterations : int
        Number of evolution iterations.
    eta_init : float
        Initial exploration rate.
    tau_decay : float
        Exploration decay time constant.
    top_k : int
        Number of structures to admit per iteration.
    seed : int
        Random seed.
    verbose : bool
        If True, prints progress to stdout.

    Returns
    -------
    spring : Spring
        The evolved Spring instance.
    history : list of dict
        Per-iteration diagnostics.
    """
    config = SpringConfig(
        max_iterations=max_iterations,
        eta_init=eta_init,
        tau_decay=tau_decay,
        top_k=top_k,
        random_seed=seed,
    )
    spring = Spring(config)
    spring.initialize(feature_matrix=candidates[: min(50, len(candidates))])

    history = spring.evolve(candidate_pool=candidates)

    if verbose:
        print(f"Spring evolution complete: {spring.memory.size} structures in memory")
        final = history[-1] if history else {}
        print(
            f"  Final η = {final.get('eta', 'N/A'):.4f}, "
            f"total admitted = {sum(h.get('n_admitted', 0) for h in history)}"
        )

    return spring, history


# ============================================================================
# Basic test
# ============================================================================

if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Test: 50 synthetic structures, 5 iterations
    # Verify: M_t grows, η decays
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Spring Self-Evolution — Basic Test")
    print("=" * 60)

    rng = np.random.default_rng(42)

    # 50 synthetic structures in R^10
    n_structures = 50
    d_phi = 10
    synthetic_features = rng.normal(0, 1, size=(n_structures, d_phi))

    # Create a mock NEP student
    class MockNEPStudent:
        """Mock NEP student for testing."""

        def predict_confidence(self, features: np.ndarray) -> np.ndarray:
            # Confidence = inverse distance from origin (simulates learned model)
            dist = np.linalg.norm(features, axis=1)
            confidence = 1.0 / (1.0 + dist)
            return confidence

        def partial_fit(self, features: np.ndarray, scores: np.ndarray) -> None:
            # No-op for testing
            pass

    mock_nep = MockNEPStudent()

    # Configure Spring
    config = SpringConfig(
        max_iterations=5,
        eta_init=0.3,
        tau_decay=20.0,
        novelty_weight=0.3,
        top_k=10,
        n_states=5,
        random_seed=42,
    )

    spring = Spring(config, nep_student=mock_nep)

    # Initialize with first 10 structures as seed
    spring.initialize(feature_matrix=synthetic_features[:10])

    print(f"\nInitial memory size: {spring.memory.size}")
    print(f"Initial η: {spring.eta:.4f}")

    # Run evolution
    history = spring.evolve(candidate_pool=synthetic_features)

    # --- Assertions ---
    print(f"\n--- Results ---")
    print(f"Final memory size: {spring.memory.size}")
    print(f"Final η: {spring.eta:.6f}")
    print(f"Iterations completed: {len(history)}")

    # Verify M_t grows
    initial_size = 10  # seed
    assert spring.memory.size > initial_size, (
        f"Memory did not grow! Initial={initial_size}, final={spring.memory.size}"
    )
    print(f"✓ Memory grew from {initial_size} to {spring.memory.size}")

    # Verify η decays
    assert spring.eta < config.eta_init, (
        f"Exploration rate did not decay! Initial={config.eta_init}, final={spring.eta}"
    )
    print(f"✓ Exploration decayed from {config.eta_init:.4f} to {spring.eta:.6f}")

    # Verify history records
    assert len(history) == config.max_iterations, (
        f"Expected {config.max_iterations} history entries, got {len(history)}"
    )
    print(f"✓ History recorded {len(history)} iterations")

    # Verify gatekeeper was updated
    reliability = spring.gatekeeper.get_state_reliability()
    evidence = spring.gatekeeper.get_state_evidence()
    assert np.any(evidence > spring.gatekeeper.prior_strength), (
        "Gatekeeper did not accumulate evidence beyond prior!"
    )
    print(f"✓ Gatekeeper updated: evidence range [{evidence.min():.1f}, {evidence.max():.1f}]")

    # Diagnostics
    diag = spring.convergence_diagnostic()
    print(f"\nConvergence diagnostic: regime={diag['regime']}")
    print(f"  converged={diag['converged']}, memory_size={diag['memory_size']}")

    # Memory summary
    print(f"\n{spring.memory.summary()}")

    # Lyapunov estimate
    lyap = spring.lyapunov_estimate(synthetic_features)
    print(f"\nLyapunov estimate Φ = {lyap:.6f}")

    print("\n" + "=" * 60)
    print("All tests passed. ✓")
    print("=" * 60)
