#!/usr/bin/env python3
"""
Fig 4: Gauge Trade-off — Gauge violation vs Energy RMSE across lambda sweep.

Demonstrates that no single lambda value can simultaneously zero the gauge
while preserving accuracy: the soft-constraint failure is fundamental.

Left Y:  Gauge violation (log scale)
Right Y: Energy RMSE (eV/atom, linear)
X:       lambda (log scale)

Horizontal dashed lines mark the unconstrained (lambda=0) baseline.
"""
import sys
sys.path.insert(0, r'C:/Users/admin/.claude/skills/scipilot-figure-skill/scripts')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from setup_style import setup_style
from export_figure import export_figure
from layout_tools import add_panel_labels, finalize_figure
from visual_qa import render_preview, audit_layout, print_report


DATA_DIR = (
    r'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces'
    r'/AlN_ModelB_v3_rich_physics/reports/validation/p0_fixes'
    r'/lambda_sweep'
)
OUT_DIR = (
    r'G:/Xiaogan_Supercomputing_data/egp/EGP-milp/papers'
    r'/v3_single_vs_modelb/figures'
)

COLOR_GAUGE = '#0072B2'
COLOR_RMSE  = '#D55E00'
COLOR_BASE  = '#999999'


def main():
    setup_style(journal='nature', lang='en', constrained_layout=True)

    df = pd.read_csv(f'{DATA_DIR}/lambda_sweep_results.csv')

    # Separate unconstrained (lambda=0) from the sweep
    base = df[df['lambda'] == 0].iloc[0]
    sweep = df[df['lambda'] > 0].sort_values('lambda').reset_index(drop=True)

    lambdas = sweep['lambda'].values
    gauge   = sweep['gauge_violation'].values
    rmse    = sweep['energy_rmse'].values  # already in eV/atom

    gauge0 = base['gauge_violation']
    rmse0  = base['energy_rmse']

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(7.0, 4.5))
    ax2 = ax1.twinx()

    # Left axis: gauge violation (log)
    ax1.plot(lambdas, gauge, 'o-', color=COLOR_GAUGE, linewidth=1.8,
             markersize=7, markerfacecolor='white', markeredgewidth=1.2,
             label='Gauge violation', zorder=3)
    ax1.axhline(y=gauge0, color=COLOR_BASE, linestyle=':', linewidth=0.9,
                alpha=0.7, zorder=1)
    ax1.annotate(f'  Unconstrained (λ=0): {gauge0:.2f}',
                 xy=(lambdas[0], gauge0),
                 fontsize=7, color=COLOR_BASE, va='bottom',
                 fontstyle='italic')

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('λ (log scale)')
    ax1.set_ylabel('Gauge violation (log)', color=COLOR_GAUGE)
    ax1.tick_params(axis='y', colors=COLOR_GAUGE)
    ax1.grid(True, alpha=0.25, linestyle=':')

    # Right axis: Energy RMSE (linear)
    ax2.plot(lambdas, rmse, 's--', color=COLOR_RMSE, linewidth=1.8,
             markersize=7, markerfacecolor='white', markeredgewidth=1.2,
             label='Energy RMSE', zorder=3)
    ax2.axhline(y=rmse0, color=COLOR_BASE, linestyle=':', linewidth=0.9,
                alpha=0.7, zorder=1)
    ax2.annotate(f'Unconstrained (λ=0): {rmse0:.4f} eV/atom',
                 xy=(lambdas[-1], rmse0),
                 fontsize=7, color=COLOR_BASE, va='bottom', ha='right',
                 fontstyle='italic')

    ax2.set_ylabel('Energy RMSE (eV/atom)', color=COLOR_RMSE)
    ax2.tick_params(axis='y', colors=COLOR_RMSE)

    # Combined legend
    lines1, labs1 = ax1.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labs1 + labs2,
               frameon=True, fancybox=False, edgecolor='#999999',
               fontsize=8, loc='upper right')

    # Title
    ax1.set_title('Gauge vs Accuracy Trade-off across λ Sweep', fontsize=9)

    finalize_figure(fig)
    add_panel_labels(fig, style='nature', labels=['a'],
                     x_offset_pt=-22, y_offset_pt=3,
                     axes=[ax1])

    # --- QA ---
    try:
        png = render_preview(fig, f'{OUT_DIR}/_preview_fig4.png', dpi=150)
    except Exception:
        pass
    issues = audit_layout(fig)
    print_report(issues)

    # --- Export ---
    paths = export_figure(
        fig,
        basename=f'{OUT_DIR}/fig4_gauge_tradeoff',
        formats=['pdf', 'png'],
        size_inches=(7.0, 4.5),
        dpi=300,
        grayscale_preview=True,
    )
    print(f'[Fig 4] Done: {paths}')
    plt.close(fig)


if __name__ == '__main__':
    main()
