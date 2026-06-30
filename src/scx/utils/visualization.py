# scx/utils/visualization.py
# Visualizer -- dual-backend (matplotlib + plotly) visualization tools for SCX.

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Lazy imports (matplotlib / plotly are heavy and may not be installed)
# ---------------------------------------------------------------------------
def _import_mpl():
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    return plt, mpl


def _import_plotly():
    import plotly.graph_objects as go
    import plotly.express as px
    import plotly.figure_factory as ff
    return go, px, ff


def _import_sns():
    import seaborn as sns
    return sns


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
_CATEGORY_COLORS = {
    "valuable": "#2E86AB",  # blue
    "redundant": "#A23B72",  # magenta
    "noisy": "#F18F01",  # orange
    "expert_dependent": "#C73E1D",  # red
    "unknown": "#6C757D",  # gray
}
_CATEGORY_LIST = ["valuable", "redundant", "noisy", "expert_dependent"]


class Visualizer:
    """Visualization toolkit for the SCX framework.

    Supports both **matplotlib** (static, publication-quality) and **plotly**
    (interactive, web-ready) backends.
    """

    # ==================================================================
    # Static visualizations (matplotlib + seaborn)
    # ==================================================================

    @staticmethod
    def state_map(
        X_2d: np.ndarray,
        labels: np.ndarray,
        title: str = "State Map",
        save_path: str | None = None,
    ) -> None:
        """Scatter plot of 2D-projected data colored by state assignment.

        Parameters
        ----------
        X_2d : np.ndarray, shape (N, 2)
            2D coordinates (e.g. PCA / t-SNE projection).
        labels : np.ndarray, shape (N,)
            State assignment per sample.
        title : str
            Plot title.
        save_path : str or None
            If provided, save the figure to this path.
        """
        plt, mpl = _import_mpl()
        sns = _import_sns()

        fig, ax = plt.subplots(figsize=(8, 6))
        n_states = len(np.unique(labels))
        palette = sns.color_palette("husl", n_states)
        scatter = ax.scatter(
            X_2d[:, 0], X_2d[:, 1],
            c=labels, cmap=mpl.colors.ListedColormap(palette),
            s=20, alpha=0.7, edgecolors="none",
        )
        cbar = plt.colorbar(scatter, ax=ax, ticks=sorted(np.unique(labels)))
        cbar.set_label("State ID")
        ax.set_xlabel("Component 1")
        ax.set_ylabel("Component 2")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()

    @staticmethod
    def reliability_heatmap(
        R_matrix: np.ndarray,
        expert_names: list[str],
        state_labels: list[str],
        save_path: str | None = None,
    ) -> None:
        """Heatmap of the expert reliability matrix R_m(s) or SCX_m(s).

        Parameters
        ----------
        R_matrix : np.ndarray, shape (M, K)
            Reliability or SCX matrix.
        expert_names : list[str], length M
        state_labels : list[str], length K
        save_path : str or None
        """
        plt, _ = _import_mpl()
        sns = _import_sns()

        fig, ax = plt.subplots(figsize=(max(6, len(state_labels) * 0.8), max(4, len(expert_names) * 0.8)))
        sns.heatmap(
            R_matrix,
            annot=True, fmt=".3f",
            xticklabels=state_labels,
            yticklabels=expert_names,
            cmap="YlOrRd",
            ax=ax,
            cbar_kws={"label": "Risk / SCX"},
        )
        ax.set_xlabel("State")
        ax.set_ylabel("Expert")
        ax.set_title("Expert Reliability Matrix R_m(s)")

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()

    @staticmethod
    def value_bar(
        state_values: np.ndarray,
        title: str = "State Data Value V(s)",
        save_path: str | None = None,
    ) -> None:
        """Bar chart of state data values V(s).

        Parameters
        ----------
        state_values : np.ndarray, shape (K,)
        title : str
        save_path : str or None
        """
        plt, _ = _import_mpl()
        sns = _import_sns()

        fig, ax = plt.subplots(figsize=(10, 5))
        K = len(state_values)
        colors = sns.color_palette("viridis", K)
        ax.bar(range(K), state_values, color=colors, edgecolor="black", linewidth=0.5)
        ax.set_xlabel("State ID")
        ax.set_ylabel("V(s)")
        ax.set_title(title)
        ax.set_xticks(range(K))
        ax.grid(axis="y", alpha=0.3)

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()

    @staticmethod
    def confusion_matrix(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        labels: list[str] | None = None,
        save_path: str | None = None,
    ) -> None:
        """Plot a confusion matrix heatmap.

        Parameters
        ----------
        y_true : np.ndarray, shape (N,)
        y_pred : np.ndarray, shape (N,)
        labels : list[str] or None
            Class label names.
        save_path : str or None
        """
        from sklearn.metrics import confusion_matrix as sk_cm

        plt, _ = _import_mpl()
        sns = _import_sns()

        cm = sk_cm(y_true, y_pred)
        fig, ax = plt.subplots(figsize=(max(6, cm.shape[0] * 0.8), max(5, cm.shape[1] * 0.8)))
        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=labels or range(cm.shape[1]),
            yticklabels=labels or range(cm.shape[0]),
            ax=ax,
        )
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        ax.set_title("Confusion Matrix")

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()

    @staticmethod
    def acquisition_progress(
        history: list[dict[str, Any]],
        save_path: str | None = None,
    ) -> None:
        """Plot acquisition progress: performance vs. budget.

        Parameters
        ----------
        history : list[dict]
            Each dict must contain at least ``"budget_used"`` and
            ``"performance"`` (or ``"accuracy"`` / ``"score"``).
        save_path : str or None
        """
        plt, _ = _import_mpl()

        df = pd.DataFrame(history)
        budget_col = "budget_used" if "budget_used" in df.columns else "step"
        perf_col = None
        for candidate in ("performance", "accuracy", "score", "test_score", "val_score"):
            if candidate in df.columns:
                perf_col = candidate
                break
        if perf_col is None:
            raise KeyError(
                "history must contain one of: performance, accuracy, score"
            )

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df[budget_col], df[perf_col], marker="o", linewidth=2, color="#2E86AB")
        ax.fill_between(df[budget_col], df[perf_col], alpha=0.15, color="#2E86AB")
        ax.set_xlabel("Budget Used")
        ax.set_ylabel(perf_col.replace("_", " ").title())
        ax.set_title("Acquisition Progress")
        ax.grid(True, alpha=0.3)

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()

    @staticmethod
    def expert_comparison(
        predictions_list: list[np.ndarray],
        y_true: np.ndarray,
        expert_names: list[str],
        save_path: str | None = None,
    ) -> None:
        """Compare multiple expert predictions against ground truth.

        For regression: scatter plots of predicted vs. true.
        For classification: grouped bar chart of accuracy per expert.

        Parameters
        ----------
        predictions_list : list[np.ndarray], shape (M, N)
        y_true : np.ndarray, shape (N,)
        expert_names : list[str], length M
        save_path : str or None
        """
        plt, _ = _import_mpl()
        M = len(predictions_list)
        y_true = np.asarray(y_true)
        is_classification = y_true.dtype in (np.int32, np.int64, int, bool) or (
            len(np.unique(y_true)) < 20
        )

        if is_classification:
            from sklearn.metrics import accuracy_score

            fig, ax = plt.subplots(figsize=(8, 5))
            accs = []
            for i, (preds, name) in enumerate(zip(predictions_list, expert_names)):
                acc = accuracy_score(y_true, preds)
                accs.append(acc)
            colors = plt.cm.viridis(np.linspace(0.2, 0.8, M))
            ax.bar(expert_names, accs, color=colors, edgecolor="black")
            ax.set_ylabel("Accuracy")
            ax.set_title("Expert Comparison (Accuracy)")
            ax.set_ylim(0, 1.05)
            for i, acc in enumerate(accs):
                ax.text(i, acc + 0.01, f"{acc:.3f}", ha="center", fontsize=9)
        else:
            from sklearn.metrics import r2_score

            n_cols = min(3, M)
            n_rows = int(np.ceil(M / n_cols))
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows))
            axes = np.atleast_1d(axes).ravel()
            for i, (preds, name) in enumerate(zip(predictions_list, expert_names)):
                ax = axes[i]
                r2 = r2_score(y_true, preds)
                ax.scatter(y_true, preds, s=10, alpha=0.5)
                lims = [
                    min(y_true.min(), preds.min()),
                    max(y_true.max(), preds.max()),
                ]
                ax.plot(lims, lims, "r--", linewidth=1, alpha=0.7)
                ax.set_xlim(lims)
                ax.set_ylim(lims)
                ax.set_xlabel("True")
                ax.set_ylabel("Predicted")
                ax.set_title(f"{name} (R2 = {r2:.3f})")
                ax.grid(True, alpha=0.3)
            for j in range(i + 1, len(axes)):
                axes[j].set_visible(False)

        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.show()

    @staticmethod
    def classification_sunburst(
        state_classifications: list[Any],
        save_path: str | None = None,
    ) -> None:
        """Plot a sunburst chart of state classification categories (plotly).

        Parameters
        ----------
        state_classifications : list
            List of objects with attributes ``state_id``, ``category``.
            If the elements are dicts, keys ``state_id`` and ``category``
            are used.
        save_path : str or None
            If provided, save as HTML.
        """
        go, _, _ = _import_plotly()

        # Extract categories
        cats = []
        for item in state_classifications:
            if isinstance(item, dict):
                cats.append(str(item.get("category", "unknown")))
            else:
                cats.append(str(getattr(item, "category", "unknown")))

        cat_counts = pd.Series(cats).value_counts()
        labels = cat_counts.index.tolist()
        values = cat_counts.values.tolist()
        parents = [""] * len(labels)  # all root-level

        colors = [_CATEGORY_COLORS.get(l, "#6C757D") for l in labels]

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>",
        ))
        fig.update_layout(
            title="State Classification Sunburst",
            width=600,
            height=600,
        )
        if save_path:
            fig.write_html(save_path)
        fig.show()

    @staticmethod
    def dashboard(
        framework: Any,
        save_path: str | None = None,
    ) -> None:
        """Generate a comprehensive interactive dashboard (plotly subplots).

        Parameters
        ----------
        framework : SCXFramework
            An instance of the SCX framework (expected to have
            ``state_space``, ``history``, and related attributes).
        save_path : str or None
            If provided, save as HTML.
        """
        go, px, _ = _import_plotly()
        from plotly.subplots import make_subplots

        # -- Collect data -------------------------------------------------
        state_space = getattr(framework, "state_space", None)
        history = getattr(framework, "history", [])
        expert_registry = getattr(framework, "expert_registry", None)
        action_policy = getattr(framework, "action_policy", None)

        n_rows = 2
        n_cols = 2

        fig = make_subplots(
            rows=n_rows, cols=n_cols,
            subplot_titles=(
                "State Proportions",
                "State Values",
                "Acquisition Progress",
                "Expert Reliability (heatmap)",
            ),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "heatmap"}]],
        )

        # -- (1, 1) State proportions ------------------------------------
        if state_space is not None:
            try:
                props = state_space.get_proportions()
                sids = sorted(state_space.states.keys())
                fig.add_trace(
                    go.Bar(x=[str(s) for s in sids], y=props,
                           name="Proportion", marker_color="#2E86AB"),
                    row=1, col=1,
                )
            except Exception:
                pass

        # -- (1, 2) State values -----------------------------------------
        if framework is not None:
            sv = getattr(framework, "state_value", None)
            if sv is not None and hasattr(sv, "components"):
                comps = sv.components
                if "value" in comps:
                    vals = comps["value"]
                    fig.add_trace(
                        go.Bar(x=[str(i) for i in range(len(vals))], y=vals,
                               name="V(s)", marker_color="#A23B72"),
                        row=1, col=2,
                    )

        # -- (2, 1) Acquisition progress ---------------------------------
        if history:
            df_hist = pd.DataFrame(history)
            bc = "budget_used" if "budget_used" in df_hist.columns else None
            if bc is None:
                bc = "step" if "step" in df_hist.columns else None
            pc = None
            for c in ("performance", "accuracy", "score", "test_score"):
                if c in df_hist.columns:
                    pc = c
                    break
            if bc and pc:
                fig.add_trace(
                    go.Scatter(x=df_hist[bc], y=df_hist[pc],
                               mode="lines+markers", name="Progress",
                               line=dict(color="#F18F01", width=2)),
                    row=2, col=1,
                )

        # -- (2, 2) Expert reliability heatmap placeholder ---------------
        try:
            if expert_registry is not None and state_space is not None:
                M = expert_registry.size
                K = state_space.n_states
                R = np.random.rand(M, K) * 0.5  # placeholder if not computed
                # Actually try to get real data
                er = getattr(framework, "expert_reliability", None)
                if er is not None and hasattr(er, "risk_matrix"):
                    R = er.risk_matrix
                fig.add_trace(
                    go.Heatmap(z=R, colorscale="YlOrRd", showscale=True),
                    row=2, col=2,
                )
        except Exception:
            pass

        fig.update_layout(
            title="SCX Framework Dashboard",
            height=800,
            showlegend=False,
            template="plotly_white",
        )
        fig.update_xaxes(title_text="State", row=1, col=1)
        fig.update_xaxes(title_text="State", row=1, col=2)
        fig.update_xaxes(title_text="Budget", row=2, col=1)
        fig.update_yaxes(title_text="Proportion", row=1, col=1)
        fig.update_yaxes(title_text="Value", row=1, col=2)

        if save_path:
            fig.write_html(save_path)
        fig.show()
