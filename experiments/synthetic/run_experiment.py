"""
Synthetic Experiment for SCX Framework.

Runs a complete SCX pipeline (state discovery, expert reliability,
data classification, state value, action policy) on synthetic data
and compares against baselines (random, uncertainty, diversity,
high-error sampling).

Usage:
    python experiments/synthetic/run_experiment.py
"""

from __future__ import annotations

import sys
import os
from typing import Any

import numpy as np
import pandas as pd

# Ensure src and project root are on path
_script_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_script_dir, "..", "..", "src"))
sys.path.insert(0, os.path.join(_script_dir, "..", ".."))  # for experiments package

# Convenience: capture the real print in case something shadows it
_builtin_print = __builtins__["print"] if isinstance(__builtins__, dict) else __builtins__.print

from scx.state.discovery import StateDiscovery
from scx.state.assignment import StateAssignment
from scx.state.metrics import StateMetrics
from scx.state.space import StateInfo, StateSpace
from scx.expert.registry import ExpertRegistry
from scx.expert.reliability import ExpertReliability
from scx.expert.router import ExpertRouter
from scx.valuation.learnability import LearnabilityScore
from scx.valuation.noise_score import NoiseScore
from scx.valuation.redundancy import RedundancyScore
from scx.valuation.classifier import DataClassifier
from scx.valuation.state_value import StateValue
from scx.action.policy import ActionPolicy
from scx.action.acquisition import AcquisitionStrategy
from scx.action.compress import CompressStrategy

from experiments.synthetic.data_generator import SyntheticDataGenerator

# Optional: matplotlib for result visualisation
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False


# ======================================================================
# SCX Pipeline
# ======================================================================


def run_scx_pipeline(
    data: dict[str, Any],
    n_states: int = 4,
    n_experts: int = 3,
    acquisition_budget: int = 50,
) -> dict[str, Any]:
    """Run a full SCX pipeline on the generated data.

    Parameters
    ----------
    data : dict
        Output from ``SyntheticDataGenerator.generate()``.
    n_states : int
    n_experts : int
    acquisition_budget : int

    Returns
    -------
    result : dict
        Pipeline outputs including state metrics, classifications, values.
    """
    X = data["X"]
    y_true = data["y_true"]
    state_labels = data["state_labels"]
    expert_preds = data["expert_predictions"]  # (M, N)
    centers = data["centers"]

    # --- 1. State discovery ---
    print("  [SCX] State discovery...")
    discovery = StateDiscovery(method="kmeans", n_states=n_states, random_state=42)
    pred_labels = discovery.fit_predict(X)
    centroids = discovery.get_centroids()

    # Build StateSpace
    space = StateSpace(n_states=n_states)
    for k in range(n_states):
        mask = pred_labels == k
        n_k = int(mask.sum())
        if n_k == 0:
            continue
        centroid = centroids[k]
        radius = float(np.mean(np.linalg.norm(X[mask] - centroid, axis=1)))
        space.add_state(StateInfo(
            id=k, label=f"S{k}", centroid=centroid,
            radius=radius, count=n_k, proportion=n_k / len(X),
        ))

    # --- 2. Expert reliability ---
    print("  [SCX] Expert reliability (supervised)...")
    registry = ExpertRegistry()
    for m in range(n_experts):
        # Build an expert function from the precomputed predictions
        def make_expert_fn(preds: np.ndarray) -> callable:
            return lambda x, p=preds: p[:len(x)] if len(x) <= len(p) else np.tile(p, int(np.ceil(len(x)/len(p))))[:len(x)]

        registry.register(
            f"expert_{chr(65+m)}",
            make_expert_fn(expert_preds[m]),
            cost=1.0,
        )

    reliability = ExpertReliability(method="supervised", alpha=1.0, min_samples=5)
    rel_result = reliability.estimate(
        registry, X, y_true, pred_labels, n_states=n_states,
    )
    R_matrix = rel_result["R_matrix"]
    SCX_matrix = rel_result["SCX_matrix"]

    # --- 3. Per-state metrics ---
    print("  [SCX] Computing state metrics...")
    ls = LearnabilityScore()
    ns = NoiseScore()
    rs = RedundancyScore()

    state_metrics: dict[int, dict[str, float]] = {}
    for k in range(n_states):
        mask = pred_labels == k
        X_s = X[mask]
        y_s = y_true[mask]
        n_k = len(X_s)
        if n_k == 0:
            continue

        # Residuals
        residual = np.abs(y_s - state_labels[mask]) if y_s.dtype.kind in ("i", "u", "f") else np.abs(y_s.astype(float) - state_labels[mask].astype(float))
        mean_res = float(np.mean(residual)) if len(residual) > 0 else 0.0

        # Consistency
        consistency = ls.consistency(X_s, y_s)

        # Noise score
        noise_score = ns.compute_state_level(
            mean_res, state_proportion=n_k / len(X), consistency=consistency,
        )

        # Redundancy
        sim = rs.state_similarity(X_s)
        boundary = rs.boundary_score(X_s, centroids, state_id=k)
        redundancy_d = rs.redundancy(
            state_proportion=n_k / len(X),
            mean_residual=mean_res,
            similarity=sim,
            boundary=boundary,
        )

        # Learnability
        learnability = ls.learnability(consistency, noise_score)

        # Expert gap
        expert_gap = float(np.max(R_matrix[:, k]) - np.min(R_matrix[:, k]))

        state_metrics[k] = {
            "mean_residual": mean_res,
            "proportion": n_k / len(X),
            "consistency": consistency,
            "redundancy": redundancy_d,
            "noise_score": noise_score,
            "similarity": sim,
            "boundary": boundary,
            "learnability": learnability,
            "expert_gap": expert_gap,
        }

    # --- 4. Data classification ---
    print("  [SCX] Data classification...")
    classifier = DataClassifier()
    class_df = classifier.classify_all(state_metrics, R_matrix=R_matrix)
    print(classifier.summary(class_df))

    # --- 5. State value ---
    print("  [SCX] Computing state values...")
    sv = StateValue()
    value_df = sv.compute_all(state_metrics, SCX_matrix)
    print(f"\n  State values:\n{value_df.to_string(index=False)}\n")

    # --- 6. Action policy ---
    print("  [SCX] Action policy...")
    action_df = class_df.rename(columns={"category": "category_str"})
    action_df["category"] = action_df["category_str"]
    # Map categories using classifier's default action mapping
    action_map = {"valuable": "acquire", "redundant": "compress", "noisy": "downweight", "expert_dependent": "route"}
    action_input_df = pd.DataFrame({
        "state_id": class_df["state_id"],
        "category": class_df["category"],
    })
    value_input_df = pd.DataFrame({
        "state_id": value_df["state_id"],
        "value": value_df["V_add"],
    })

    policy = ActionPolicy(budget=acquisition_budget, mode="proportional")
    actions = policy.decide(action_input_df, value_input_df)
    allocation = policy.allocate_budget(value_input_df)

    print(f"  Actions: {actions}")
    print(f"  Budget allocation: {allocation}")

    return {
        "state_discovery": discovery,
        "state_space": space,
        "state_labels": pred_labels,
        "R_matrix": R_matrix,
        "SCX_matrix": SCX_matrix,
        "state_metrics": state_metrics,
        "classifications": class_df,
        "state_values": value_df,
        "actions": actions,
        "budget_allocation": allocation,
    }


# ======================================================================
# Baseline methods
# ======================================================================


def run_random_baseline(
    X: np.ndarray,
    budget: int,
) -> tuple[np.ndarray, float]:
    """Random sampling baseline: randomly selects samples.

    Returns
    -------
    selected_indices : np.ndarray
    efficiency : float (always 0.5 by construction in simulation)
    """
    rng = np.random.default_rng(42)
    n = min(budget, len(X))
    indices = rng.choice(len(X), size=n, replace=False)
    return indices, 0.5  # placeholder


def run_uncertainty_baseline(
    X: np.ndarray,
    expert_preds: np.ndarray,
    y_true: np.ndarray,
    budget: int,
) -> tuple[np.ndarray, float]:
    """Uncertainty sampling: select samples with highest expert disagreement.

    Uses variance across expert predictions as the uncertainty measure.
    """
    # Variance across experts
    uncertainty = np.var(expert_preds, axis=0)  # (N,)
    n = min(budget, len(X))
    indices = np.argsort(uncertainty)[::-1][:n]
    return indices, float(np.mean(uncertainty[indices]))


def run_diversity_baseline(
    X: np.ndarray,
    budget: int,
) -> tuple[np.ndarray, float]:
    """Diversity sampling: farthest-point traversal (k-center)."""
    from sklearn.metrics.pairwise import pairwise_distances

    n = min(budget, len(X))
    if n >= len(X):
        return np.arange(len(X)), 1.0

    D = pairwise_distances(X, metric="euclidean")
    chosen = [np.random.randint(len(X))]
    dist_to_set = D[chosen[0]].copy()

    for _ in range(1, n):
        farthest = np.argmax(dist_to_set)
        chosen.append(farthest)
        dist_to_set = np.minimum(dist_to_set, D[farthest])

    return np.array(chosen, dtype=int), float(dist_to_set.max())


def run_high_error_baseline(
    X: np.ndarray,
    residuals: np.ndarray,
    budget: int,
) -> tuple[np.ndarray, float]:
    """High-error sampling: select samples with largest residuals."""
    n = min(budget, len(X))
    indices = np.argsort(residuals)[::-1][:n]
    return indices, float(np.mean(residuals[indices]))


# ======================================================================
# Evaluation helpers
# ======================================================================


def compute_residuals(
    X: np.ndarray,
    y_true: np.ndarray,
    expert_preds: np.ndarray,
) -> np.ndarray:
    """Compute per-sample residual as mean absolute expert error."""
    residuals = np.mean(np.abs(expert_preds - y_true[np.newaxis, :]), axis=0)
    return residuals


def coverage_metric(
    X: np.ndarray,
    selected_indices: np.ndarray,
) -> float:
    """Compute coverage of selected set (mean NN distance)."""
    from sklearn.metrics.pairwise import pairwise_distances

    if len(selected_indices) == 0:
        return 0.0
    selected = X[selected_indices]
    D = pairwise_distances(selected, X, metric="euclidean")
    min_dists = D.min(axis=0)
    return float(min_dists.mean())


# ======================================================================
# Visualisation
# ======================================================================


def plot_results(
    data: dict[str, Any],
    scx_result: dict[str, Any],
    baselines: dict[str, Any],
    save_path: str | None = None,
) -> None:
    """Generate result figures.

    Parameters
    ----------
    data : dict
        Generated data.
    scx_result : dict
        SCX pipeline output.
    baselines : dict
        Baseline method outputs.
    save_path : str, optional
    """
    if not _HAS_MPL:
        print("  matplotlib not installed; skipping plots.")
        return

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    X = data["X"]
    state_labels = data["state_labels"]
    pred_labels = scx_result["state_labels"]
    R_matrix = scx_result["R_matrix"]
    value_df = scx_result["state_values"]
    class_df = scx_result["classifications"]

    # --- Panel 1: Ground-truth states ---
    ax = axes[0, 0]
    scatter = ax.scatter(X[:, 0], X[:, 1], c=state_labels, cmap="viridis",
                         s=12, alpha=0.6)
    ax.set_title("Ground-Truth States")
    fig.colorbar(scatter, ax=ax)

    # --- Panel 2: Discovered states ---
    ax = axes[0, 1]
    scatter = ax.scatter(X[:, 0], X[:, 1], c=pred_labels, cmap="plasma",
                         s=12, alpha=0.6)
    ax.set_title("Discovered States (K-Means)")
    fig.colorbar(scatter, ax=ax)

    # --- Panel 3: Expert reliability heatmap ---
    ax = axes[0, 2]
    im = ax.imshow(R_matrix, aspect="auto", cmap="Reds")
    ax.set_xlabel("State ID")
    ax.set_ylabel("Expert ID")
    ax.set_title("Expert Risk R_m(s)")
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(R_matrix.shape[1]))
    ax.set_yticks(range(R_matrix.shape[0]))
    for i in range(R_matrix.shape[0]):
        for j in range(R_matrix.shape[1]):
            ax.text(j, i, f"{R_matrix[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color="white" if R_matrix[i, j] > 0.4 else "black")

    # --- Panel 4: State value bar chart ---
    ax = axes[1, 0]
    sids = value_df["state_id"].values
    v_add = value_df["V_add"].values
    v_remove = value_df["V_remove"].values
    x = np.arange(len(sids))
    width = 0.35
    ax.bar(x - width / 2, v_add, width, label="V_add", color="steelblue")
    ax.bar(x + width / 2, v_remove, width, label="V_remove", color="coral")
    ax.set_xticks(x)
    ax.set_xticklabels([f"S{s}" for s in sids])
    ax.set_title("State Values")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # --- Panel 5: Classification pie chart ---
    ax = axes[1, 1]
    counts = class_df["category"].value_counts()
    colors = {"valuable": "#2ecc71", "redundant": "#3498db",
              "noisy": "#e74c3c", "expert_dependent": "#f39c12"}
    patch_colors = [colors.get(c, "#95a5a6") for c in counts.index]
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%",
           colors=patch_colors, startangle=90)
    ax.set_title("State Classification")

    # --- Panel 6: Acquisition progress (baseline comparison) ---
    ax = axes[1, 2]
    methods = list(baselines.keys())
    scores = [baselines[m]["score"] for m in methods]
    colors_bar = ["#2ecc71" if "SCX" in m else "#3498db" for m in methods]
    ax.barh(methods, scores, color=colors_bar)
    ax.set_xlabel("Coverage Score")
    ax.set_title("Method Comparison")
    for i, v in enumerate(scores):
        ax.text(v + 0.01, i, f"{v:.3f}", va="center")

    fig.suptitle("SCX Synthetic Experiment Results", fontsize=14)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Figure saved to {save_path}")
    else:
        plt.show()


# ======================================================================
# Main
# ======================================================================


def main():
    """Run the full synthetic experiment."""
    print("=" * 60)
    print("SCX Synthetic Experiment")
    print("=" * 60)

    # --- Configuration ---
    cfg = {
        "n_states": 4,
        "n_experts": 3,
        "n_samples": 500,
        "noise_ratio": 0.05,
        "redundancy_ratio": 0.20,
        "acquisition_budget": 50,
        "random_state": 42,
    }

    print("\nConfiguration:")
    for k, v in cfg.items():
        print(f"  {k}: {v}")

    # --- Step 1: Generate data ---
    print("\n[1] Generating synthetic data...")
    gen = SyntheticDataGenerator(
        n_states=cfg["n_states"],
        n_experts=cfg["n_experts"],
        n_samples=cfg["n_samples"],
        noise_ratio=cfg["noise_ratio"],
        redundancy_ratio=cfg["redundancy_ratio"],
        random_state=cfg["random_state"],
    )
    data = gen.generate()
    print(f"  Data shape: {data['X'].shape}")
    print(f"  States: {len(np.unique(data['state_labels']))}")
    print(f"  Noisy samples: {data['noisy_mask'].sum()}")
    print(f"  Redundant samples: {data['redundant_mask'].sum()}")

    # --- Step 2: Run SCX pipeline ---
    print("\n[2] Running SCX pipeline...")
    scx_result = run_scx_pipeline(
        data,
        n_states=cfg["n_states"],
        n_experts=cfg["n_experts"],
        acquisition_budget=cfg["acquisition_budget"],
    )

    # --- Step 3: Run baselines ---
    print("\n[3] Running baseline methods...")
    X = data["X"]
    residuals = compute_residuals(X, data["y_true"], data["expert_predictions"])

    budget = cfg["acquisition_budget"]

    rand_idx, _ = run_random_baseline(X, budget)
    unc_idx, _ = run_uncertainty_baseline(X, data["expert_predictions"], data["y_true"], budget)
    div_idx, _ = run_diversity_baseline(X, budget)
    err_idx, _ = run_high_error_baseline(X, residuals, budget)

    baselines = {
        "Random": {"indices": rand_idx, "score": coverage_metric(X, rand_idx)},
        "Uncertainty": {"indices": unc_idx, "score": coverage_metric(X, unc_idx)},
        "Diversity": {"indices": div_idx, "score": coverage_metric(X, div_idx)},
        "High-Error": {"indices": err_idx, "score": coverage_metric(X, err_idx)},
    }
    # SCX score: use state values to guide acquisition
    value_df = scx_result["state_values"]
    best_state = value_df.loc[value_df["V_add"].idxmax(), "state_id"]
    scx_mask = scx_result["state_labels"] == best_state
    scx_idx = np.where(scx_mask)[0][:budget]
    scx_score = coverage_metric(X, scx_idx) if len(scx_idx) > 0 else 0.0
    baselines["SCX (ours)"] = {"indices": scx_idx, "score": scx_score}

    # --- Step 4: Print comparison report ---
    print("\n[4] Results report")
    print("=" * 60)
    print(f"\n{'Method':<20} {'Coverage':<12} {'n_selected':<12}")
    print("-" * 44)
    for method, result in sorted(baselines.items(), key=lambda x: -x[1]["score"]):
        print(f"{method:<20} {result['score']:<12.4f} {len(result['indices']):<12d}")

    # --- Step 5: Summarise state classification ---
    print("\n[5] State Classification Details")
    print("=" * 60)
    class_df = scx_result["classifications"]
    print(class_df.to_string(index=False))

    # --- Step 6: State values ---
    print("\n[6] State Values (V_add and V_remove)")
    print("=" * 60)
    print(value_df.to_string(index=False))

    # --- Step 7: State quality metrics ---
    print("\n[7] State Quality Metrics")
    print("=" * 60)
    state_metrics = scx_result["state_metrics"]
    metrics_rows = []
    for k, m in sorted(state_metrics.items()):
        metrics_rows.append({
            "State": f"S{k}",
            "MeanResid": f"{m['mean_residual']:.4f}",
            "Proportion": f"{m['proportion']:.4f}",
            "Consist": f"{m['consistency']:.4f}",
            "Redund": f"{m['redundancy']:.4f}",
            "Noise": f"{m['noise_score']:.4f}",
            "Learn": f"{m['learnability']:.4f}",
        })
    print(pd.DataFrame(metrics_rows).to_string(index=False))

    # --- Step 8: Budget allocation ---
    print("\n[8] SCX Budget Allocation")
    print("=" * 60)
    allocation = scx_result["budget_allocation"]
    for sid, n in sorted(allocation.items()):
        cat = class_df.loc[class_df["state_id"] == sid, "category"].values[0] if sid in class_df["state_id"].values else "?"
        print(f"  State S{sid} ({cat:20s}): {n} samples")

    # --- Step 9: Visualise ---
    plot_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(plot_dir, exist_ok=True)
    plot_path = os.path.join(plot_dir, "scx_synthetic_results.png")

    print(f"\n[9] Generating visualisation...")
    plot_results(data, scx_result, baselines, save_path=plot_path)

    # --- Step 10: Summary ---
    print("\n" + "=" * 60)
    print("Experiment Complete")
    print("=" * 60)
    best_method = max(baselines, key=lambda m: baselines[m]["score"])
    print(f"  Best coverage: {best_method} ({baselines[best_method]['score']:.4f})")
    print(f"  SCX coverage:  {baselines['SCX (ours)']['score']:.4f}")
    improvement = baselines['SCX (ours)']['score'] - max(v['score'] for k, v in baselines.items() if k != 'SCX (ours)')
    print(f"  Improvement over best baseline: {improvement:+.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
