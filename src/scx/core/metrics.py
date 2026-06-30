"""SCX metrics collection, reporting, and convergence visualization."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False


class SCXMetrics:
    """Evaluation metrics collector and reporter for SCX framework runs.

    Accumulates step-wise metrics into an internal history list and provides
    summary statistics, convergence plots, and a human-readable report.
    """

    def __init__(self) -> None:
        self._history: list[dict[str, Any]] = []

    def update(self, step: int, metrics: dict[str, Any]) -> None:
        """Record a snapshot of metrics at a given step.

        Parameters
        ----------
        step : int
            Step or iteration number.
        metrics : dict
            Key-value pairs of metric names and values at this step.
        """
        record = {"step": step, **metrics}
        self._history.append(record)

    def get_history(self) -> pd.DataFrame:
        """Return the full metric history as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Columns include 'step' plus all metric keys passed to ``update``.
        """
        return pd.DataFrame(self._history)

    def summary(self) -> dict[str, Any]:
        """Aggregate key metrics across all recorded steps.

        Returns
        -------
        dict
            Contains ``n_steps``, final values of each metric,
            and per-metric min / max / mean / std.
        """
        if not self._history:
            return {"n_steps": 0}

        df = self.get_history()
        summary: dict[str, Any] = {"n_steps": len(df)}
        metric_cols = [c for c in df.columns if c != "step"]

        for col in metric_cols:
            values = df[col].dropna().values
            if len(values) == 0:
                continue
            summary[f"{col}_final"] = float(values[-1])
            summary[f"{col}_min"] = float(values.min())
            summary[f"{col}_max"] = float(values.max())
            summary[f"{col}_mean"] = float(values.mean())
            summary[f"{col}_std"] = float(values.std()) if len(values) > 1 else 0.0

        return summary

    def plot_convergence(self, save_path: str | None = None) -> None:
        """Plot per-metric convergence curves over steps.

        Parameters
        ----------
        save_path : str, optional
            If provided, save the figure to this path instead of showing it.
        """
        if not _HAS_MPL:
            raise ImportError(
                "matplotlib is required for convergence plotting. "
                "Install it with: pip install matplotlib"
            )

        df = self.get_history()
        if df.empty:
            print("No metrics recorded.")
            return

        metric_cols = [c for c in df.columns if c != "step"]
        n_metrics = len(metric_cols)
        if n_metrics == 0:
            print("No metric columns to plot.")
            return

        n_cols = min(3, n_metrics)
        n_rows = int(np.ceil(n_metrics / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
        axes = np.atleast_1d(axes).ravel()

        for i, col in enumerate(metric_cols):
            ax = axes[i]
            ax.plot(df["step"].values, df[col].values, marker="o", linestyle="-",
                    markersize=3)
            ax.set_xlabel("Step")
            ax.set_ylabel(col)
            ax.set_title(col)
            ax.grid(True, alpha=0.3)

        # Hide unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)

        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
            plt.close(fig)
        else:
            plt.show()

    def report(self) -> str:
        """Generate a human-readable text report of the recorded metrics.

        Returns
        -------
        str
            Formatted report string.
        """
        df = self.get_history()
        if df.empty:
            return "SCXMetrics: no data recorded."

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("SCX Framework — Metrics Report")
        lines.append("=" * 60)

        summary = self.summary()
        lines.append(f"  Total steps:  {summary['n_steps']}")

        metric_cols = [c for c in df.columns if c != "step"]
        for col in sorted(metric_cols):
            final_key = f"{col}_final"
            if final_key not in summary:
                continue
            lines.append(f"  {col}:")
            lines.append(f"    final = {summary[final_key]:.4f}")
            if f"{col}_min" in summary:
                lines.append(f"    range = [{summary[f'{col}_min']:.4f}, "
                             f"{summary[f'{col}_max']:.4f}]")
                lines.append(f"    mean  = {summary[f'{col}_mean']:.4f} "
                             f"+- {summary[f'{col}_std']:.4f}")

        lines.append("=" * 60)
        return "\n".join(lines)
