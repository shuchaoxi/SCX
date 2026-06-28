#!/usr/bin/env python3
"""
Spring Self-Evolution Validation Script
========================================

Validates the Spring self-evolution algorithm on synthetic data:
  - 200 synthetic structures in R^20
  - 5 mock experts with state-conditioned reliability patterns
  - 20 self-evolution iterations

Produces four diagnostic plots:
  1. |M_t| growth — monotonic memory bank expansion
  2. η(t) decay — exploration rate exponential annealing
  3. S_t convergence — gatekeeper reliability stabilisation
  4. Resurrection rate — dormant structure revival frequency

Output:
  Figures saved to: paper/spring_config/figures/
  Console: per-iteration diagnostics + convergence verdict

Usage:
  python scripts/spring_validation.py
  # or with custom config:
  python scripts/spring_validation.py --n_structures 500 --n_iterations 50
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Add project root to Python path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scx.spring import Spring, SpringConfig


# ============================================================================
# Data generation
# ============================================================================


def generate_synthetic_structures(
    n_structures: int = 200,
    d_phi: int = 20,
    n_clusters: int = 5,
    seed: int = 42,
) -> np.ndarray:
    """Generate synthetic structures in feature space R^{d_phi}.

    Structures are drawn from n_clusters Gaussian clusters with varying
    separation, creating natural "states" for the state discovery step.

    Parameters
    ----------
    n_structures : int
        Total number of structures.
    d_phi : int
        Feature dimension.
    n_clusters : int
        Number of underlying clusters (states).
    seed : int
        Random seed.

    Returns
    -------
    np.ndarray, shape (n_structures, d_phi)
    """
    rng = np.random.default_rng(seed)
    structures_per_cluster = n_structures // n_clusters
    remainder = n_structures % n_clusters

    features_list = []
    for k in range(n_clusters):
        n_k = structures_per_cluster + (1 if k < remainder else 0)
        # Each cluster has a different center and variance
        center = rng.normal(k * 3.0, 1.0, size=d_phi)
        cluster = rng.normal(center, 0.3 + k * 0.3, size=(n_k, d_phi))
        features_list.append(cluster)

    return np.vstack(features_list)


def create_mock_experts(
    n_experts: int = 5,
    d_phi: int = 20,
    n_clusters: int = 5,
    seed: int = 42,
) -> list:
    """Create mock NEP experts with state-conditioned reliability profiles.

    Each expert is good at some clusters and poor at others, simulating
    real-world state-conditioned expertise patterns.

    Returns
    -------
    list of MockNEPExpert
    """
    rng = np.random.default_rng(seed)

    class MockNEPExpert:
        """Mock NEP student model for Spring validation.

        Each expert has a 'competence map' over clusters — some clusters
        it predicts well (high confidence), others poorly.
        """

        def __init__(self, expert_id: int, competence: np.ndarray, rng: np.random.Generator):
            self.expert_id = expert_id
            self.competence = competence  # shape (n_clusters,)
            self._rng = rng
            self._fit_count = 0

        def predict_confidence(self, features: np.ndarray) -> np.ndarray:
            """Return state-conditioned prediction confidence in [0, 1]."""
            # Simulate: confidence depends on which cluster the feature is from
            # We don't know the cluster at prediction time, so use a smooth
            # distance-based mixture
            n = features.shape[0]
            # Use norm as proxy for cluster identity
            norms = np.linalg.norm(features, axis=1)
            # Map to competence: closer to origin = cluster 0, farther = higher
            norm_bins = np.linspace(norms.min(), norms.max(), len(self.competence))
            bin_indices = np.digitize(norms, norm_bins) - 1
            bin_indices = np.clip(bin_indices, 0, len(self.competence) - 1)
            base_conf = self.competence[bin_indices]
            # Add exploration noise proportional to fit_count (improves with training)
            noise = self._rng.uniform(-0.1, 0.1, size=n)
            # As expert is trained more, confidence increases slightly
            training_bonus = min(0.05 * self._fit_count, 0.15)
            return np.clip(base_conf + noise + training_bonus, 0.05, 0.95)

        def partial_fit(self, features: np.ndarray, scores: np.ndarray) -> None:
            """Simulate incremental training."""
            self._fit_count += 1

    experts = []
    for m in range(n_experts):
        # Each expert has high competence in 1-2 clusters, low in others
        competence = rng.uniform(0.3, 0.7, size=n_clusters)
        # Boost 1-2 random clusters
        strong_clusters = rng.choice(n_clusters, size=rng.integers(1, 3), replace=False)
        competence[strong_clusters] = rng.uniform(0.7, 0.95)
        # Weaken 1-2 other clusters
        weak_clusters = rng.choice(
            [c for c in range(n_clusters) if c not in strong_clusters],
            size=rng.integers(1, 3),
            replace=False,
        )
        competence[weak_clusters] = rng.uniform(0.1, 0.35)
        experts.append(MockNEPExpert(m, competence, rng))

    return experts


# ============================================================================
# Spring validation runner
# ============================================================================


def run_spring_validation(
    n_structures: int = 200,
    n_experts: int = 5,
    n_iterations: int = 20,
    d_phi: int = 20,
    n_clusters: int = 5,
    seed: int = 42,
) -> dict:
    """Run Spring self-evolution and collect diagnostics.

    Returns
    -------
    dict with keys:
        spring : Spring instance (fitted)
        history : list of per-iteration diagnostics
        diagnostics : convergence diagnostic dict
        lyapunov_history : list of Lyapunov estimates per iteration
        resurrection_events : list of (iteration, n_resurrected)
    """
    rng = np.random.default_rng(seed)

    # Generate synthetic structures
    print(f"Generating {n_structures} synthetic structures in R^{d_phi}...")
    structures = generate_synthetic_structures(
        n_structures=n_structures,
        d_phi=d_phi,
        n_clusters=n_clusters,
        seed=seed,
    )

    # Create mock experts
    print(f"Creating {n_experts} mock experts...")
    experts = create_mock_experts(
        n_experts=n_experts,
        d_phi=d_phi,
        n_clusters=n_clusters,
        seed=seed,
    )

    # Configure Spring
    config = SpringConfig(
        max_iterations=n_iterations,
        eta_init=0.3,
        tau_decay=10.0,  # Faster decay for validation
        novelty_weight=0.3,
        top_k=15,
        n_states=n_clusters,
        random_seed=seed,
        gatekeeper_prior_strength=5.0,
        memory_max_size=10000,
    )

    # Custom quality function using ensemble of all experts
    def ensemble_quality(features: np.ndarray) -> np.ndarray:
        """Average confidence across all experts."""
        confs = np.array([e.predict_confidence(features) for e in experts])
        return confs.mean(axis=0)

    # Initialize Spring with first expert as NEP student
    spring = Spring(config, nep_student=experts[0])
    spring.set_nep_quality_fn(ensemble_quality)

    # Initialize memory with first 30 structures as seed
    seed_structures = structures[:30]
    spring.initialize(feature_matrix=seed_structures)

    print(f"Initial memory: {spring.memory.size} structures")
    print(f"Initial η: {spring.eta:.4f}")

    # Track resurrection events by wrapping memory
    resurrection_events = []
    original_resurrect = spring.memory.resurrect_lowest

    def tracked_resurrect(n: int = 1):
        result = original_resurrect(n)
        if result:
            resurrection_events.append((spring._iteration, len(result)))
        return result

    spring.memory.resurrect_lowest = tracked_resurrect

    # Track Lyapunov estimates
    lyapunov_history = []

    def lyapunov_callback(t: int, sp: Spring) -> None:
        lyap = sp.lyapunov_estimate(structures)
        lyapunov_history.append(lyap)

    # Run evolution
    print(f"\nRunning {n_iterations} Spring iterations...")
    print("-" * 60)

    history = spring.evolve(
        candidate_pool=structures,
        max_iterations=n_iterations,
        callback=lyapunov_callback,
    )

    # Final diagnostics
    diag = spring.convergence_diagnostic()
    print("-" * 60)
    print(f"\nFinal memory: {spring.memory.size} structures")
    print(f"Final η: {spring.eta:.6f}")
    print(f"Convergence: {diag['regime']}")

    return {
        "spring": spring,
        "history": history,
        "diagnostics": diag,
        "lyapunov_history": lyapunov_history,
        "resurrection_events": resurrection_events,
        "structures": structures,
        "experts": experts,
    }


# ============================================================================
# Plotting
# ============================================================================


def plot_results(results: dict, output_dir: str) -> None:
    """Generate four-panel validation plot.

    Panels:
      1. |M_t| growth — memory bank size vs iteration
      2. η(t) decay — exploration rate with theoretical curve
      3. S_t convergence — gatekeeper mean reliability
      4. Resurrection rate — dormant structure revival events
    """
    history = results["history"]
    diag = results["diagnostics"]
    lyapunov_history = results["lyapunov_history"]
    resurrection_events = results["resurrection_events"]
    spring = results["spring"]

    iterations = np.array([h["iteration"] for h in history])
    memory_sizes = np.array([h["memory_size"] for h in history])
    etas = np.array([h.get("eta", 0.0) for h in history])
    n_admitted = np.array([h.get("n_admitted", 0) for h in history])
    gatekeeper_reliabilities = np.array(
        [h.get("gatekeeper_mean_reliability", 0.5) for h in history]
    )
    gatekeeper_deltas = np.array(
        [h.get("gatekeeper_delta", 0.0) for h in history]
    )

    # Set up figure with publication-quality styling
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "legend.fontsize": 9,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(
        "Spring Self-Evolution Validation\n"
        f"({len(history)} iterations, {spring.memory.size} final structures, "
        f"regime: {diag['regime']})",
        fontsize=13,
        fontweight="bold",
    )

    # ---- Panel 1: |M_t| growth ----
    ax1 = axes[0, 0]
    ax1.plot(iterations, memory_sizes, "b-o", markersize=4, linewidth=1.5, label=r"$|M_t|$")
    ax1.fill_between(iterations, memory_sizes, alpha=0.15, color="blue")
    ax1.set_xlabel("Iteration t")
    ax1.set_ylabel(r"$|M_t|$ (Memory Bank Size)")
    ax1.set_title(r"(a) $|M_t|$ Monotonic Growth")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)
    # Annotate growth
    growth = memory_sizes[-1] - memory_sizes[0] if len(memory_sizes) > 0 else 0
    ax1.annotate(
        f"Δ = +{growth}",
        xy=(iterations[-1], memory_sizes[-1]),
        xytext=(iterations[-1] * 0.7, memory_sizes[-1] * 0.92),
        arrowprops=dict(arrowstyle="->", color="gray"),
        fontsize=9,
        color="gray",
    )

    # ---- Panel 2: η(t) decay ----
    ax2 = axes[0, 1]
    ax2.plot(iterations, etas, "r-s", markersize=4, linewidth=1.5, label=r"$\eta(t)$ (actual)")
    # Theoretical exponential decay
    if len(etas) > 0:
        eta_theory = etas[0] * np.exp(-iterations / 10.0)
        ax2.plot(iterations, eta_theory, "r--", linewidth=1, alpha=0.5,
                 label=r"$\eta_0 e^{-t/\tau}$ (theory)")
    ax2.set_xlabel("Iteration t")
    ax2.set_ylabel(r"$\eta(t)$ (Exploration Rate)")
    ax2.set_title(r"(b) $\eta(t)$ Exponential Decay")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(bottom=0)

    # ---- Panel 3: S_t convergence ----
    ax3 = axes[1, 0]
    color = "tab:green"
    ax3.plot(iterations, gatekeeper_reliabilities, "-", color=color, linewidth=1.5,
             label=r"$\mathbb{E}[S_t]$")
    ax3.set_xlabel("Iteration t")
    ax3.set_ylabel(r"$\mathbb{E}[S_t]$ (Gatekeeper Reliability)", color=color)
    ax3.tick_params(axis="y", labelcolor=color)
    ax3.set_title(r"(c) $S_t$ Gatekeeper Convergence")

    # Add gatekeeper delta on secondary axis
    ax3b = ax3.twinx()
    ax3b.fill_between(iterations, gatekeeper_deltas, alpha=0.2, color="orange",
                      label=r"$\|\Delta S_t\|$")
    ax3b.plot(iterations, gatekeeper_deltas, "-", color="orange", linewidth=1, alpha=0.7,
              label=r"$\|\Delta S_t\|$")
    ax3b.set_ylabel(r"$\|\Delta S_t\|$ (Update Magnitude)", color="orange")
    ax3b.tick_params(axis="y", labelcolor="orange")
    ax3b.set_ylim(bottom=0)

    # Combine legends
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3b.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)
    ax3.grid(True, alpha=0.3)

    # ---- Panel 4: Resurrection rate ----
    ax4 = axes[1, 1]
    # Plot admitted per iteration as bar chart
    colors_admit = ["#2ecc71" if a > 0 else "#e74c3c" for a in n_admitted]
    ax4.bar(iterations, n_admitted, color=colors_admit, alpha=0.7, label="Admitted")
    ax4.set_xlabel("Iteration t")
    ax4.set_ylabel("Structures Admitted")
    ax4.set_title(r"(d) Admitted per Iteration + Resurrection")

    # Overlay resurrection events
    if resurrection_events:
        res_iters = [e[0] for e in resurrection_events]
        res_counts = [e[1] for e in resurrection_events]
        ax4.scatter(res_iters, res_counts, marker="^", color="purple", s=80,
                    zorder=5, label="Resurrected")
        for ri, rc in zip(res_iters, res_counts):
            ax4.annotate(
                str(rc), (ri, rc), textcoords="offset points",
                xytext=(0, 8), fontsize=8, color="purple", ha="center",
            )

    ax4.legend(loc="upper right", fontsize=8)
    ax4.grid(True, alpha=0.3, axis="y")

    # ---- Lyapunov inset in Panel 3 ----
    if lyapunov_history:
        # Add small inset showing Lyapunov trajectory
        inset_ax = ax3.inset_axes([0.55, 0.15, 0.4, 0.35])
        lyap_iters = np.arange(len(lyapunov_history))
        inset_ax.plot(lyap_iters, lyapunov_history, "k-", linewidth=1)
        inset_ax.set_title(r"$\Phi_t$", fontsize=8)
        inset_ax.set_xlabel("t", fontsize=7)
        inset_ax.tick_params(labelsize=6)
        inset_ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save
    os.makedirs(output_dir, exist_ok=True)
    fig_path = os.path.join(output_dir, "spring_validation.png")
    fig.savefig(fig_path)
    print(f"\nFigure saved: {fig_path}")

    # Also save individual panels for paper inclusion
    panel_names = ["a_mt_growth", "b_eta_decay", "c_st_convergence", "d_admission_resurrection"]
    for ax, name in zip(axes.flat, panel_names):
        # Extract the individual panel
        bbox = ax.get_tightbbox(fig.canvas.get_renderer())
        panel_path = os.path.join(output_dir, f"spring_{name}.png")
        fig.savefig(panel_path, bbox_inches=bbox.transformed(fig.dpi_scale_trans.inverted()),
                    pad_inches=0.05)
        print(f"  Panel saved: {panel_path}")

    plt.close(fig)


# ============================================================================
# Main
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Spring Self-Evolution Validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--n_structures", type=int, default=200,
                        help="Number of synthetic structures (default: 200)")
    parser.add_argument("--n_experts", type=int, default=5,
                        help="Number of mock experts (default: 5)")
    parser.add_argument("--n_iterations", type=int, default=20,
                        help="Number of evolution iterations (default: 20)")
    parser.add_argument("--d_phi", type=int, default=20,
                        help="Feature dimension (default: 20)")
    parser.add_argument("--n_clusters", type=int, default=5,
                        help="Number of underlying clusters (default: 5)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    parser.add_argument("--output_dir", type=str,
                        default=str(PROJECT_ROOT / "paper" / "spring_config" / "figures"),
                        help="Output directory for figures")
    args = parser.parse_args()

    print("=" * 60)
    print("Spring Self-Evolution Validation")
    print("=" * 60)
    print(f"  Structures: {args.n_structures}")
    print(f"  Experts:    {args.n_experts}")
    print(f"  Iterations: {args.n_iterations}")
    print(f"  Dim(φ):     {args.d_phi}")
    print(f"  Clusters:   {args.n_clusters}")
    print(f"  Seed:       {args.seed}")
    print("=" * 60)
    print()

    # Run validation
    results = run_spring_validation(
        n_structures=args.n_structures,
        n_experts=args.n_experts,
        n_iterations=args.n_iterations,
        d_phi=args.d_phi,
        n_clusters=args.n_clusters,
        seed=args.seed,
    )

    # Generate plots
    print("\nGenerating plots...")
    plot_results(results, args.output_dir)

    # Summary statistics
    history = results["history"]
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)

    if history:
        initial_memory = history[0]["memory_size"]
        final_memory = history[-1]["memory_size"]
        total_admitted = sum(h.get("n_admitted", 0) for h in history)
        initial_eta = history[0].get("eta", 0.3)
        final_eta = history[-1].get("eta", 0.0)
        final_reliability = history[-1].get("gatekeeper_mean_reliability", 0.5)

        print(f"  Memory growth:       {initial_memory} → {final_memory} (+{final_memory - initial_memory})")
        print(f"  Total admitted:      {total_admitted}")
        print(f"  η decay:             {initial_eta:.4f} → {final_eta:.6f}")
        print(f"  Final reliability:   {final_reliability:.4f}")
        print(f"  Convergence regime:  {results['diagnostics']['regime']}")
        print(f"  Resurrection events: {len(results['resurrection_events'])}")

    # Theoretical checks
    checks_passed = []
    checks_failed = []

    # Check 1: Monotonic M_t growth
    if history and len(history) >= 2:
        mem_sizes = [h["memory_size"] for h in history]
        is_monotonic = all(mem_sizes[i] <= mem_sizes[i + 1] for i in range(len(mem_sizes) - 1))
        if is_monotonic:
            checks_passed.append("M_t monotonic growth ✓")
        else:
            checks_failed.append("M_t NOT monotonic ✗")

    # Check 2: η decay
    if history and len(history) >= 2:
        eta_decayed = history[-1].get("eta", 0) < history[0].get("eta", 0.3)
        if eta_decayed:
            checks_passed.append("η(t) exponential decay ✓")
        else:
            checks_failed.append("η(t) did not decay ✗")

    # Check 3: S_t convergence
    if history and len(history) >= 5:
        recent_deltas = [h.get("gatekeeper_delta", 0) for h in history[-5:]]
        mean_recent_delta = np.mean(recent_deltas) if recent_deltas else 1.0
        early_deltas = [h.get("gatekeeper_delta", 0) for h in history[:5]]
        mean_early_delta = np.mean(early_deltas) if early_deltas else 0.0
        if mean_recent_delta < mean_early_delta:
            checks_passed.append(f"S_t convergence (Δ: {mean_early_delta:.4f} → {mean_recent_delta:.4f}) ✓")
        else:
            checks_failed.append("S_t not converging ✗")

    print("\n  Theoretical Checks:")
    for check in checks_passed:
        print(f"    {check}")
    for check in checks_failed:
        print(f"    {check}")

    if not checks_failed:
        print("\n  ✓ All theoretical predictions verified!")
    else:
        print(f"\n  ⚠ {len(checks_failed)} checks failed — see above")

    print("=" * 60)

    return 0 if not checks_failed else 1


if __name__ == "__main__":
    sys.exit(main())
