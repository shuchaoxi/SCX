#!/usr/bin/env python3
"""
Fig 2: Elastic Constants Comparison — Single ACE vs Model B against DFT.

Grouped bar chart of the five independent elastic constants (C11, C12, C13,
C33, C44) with DFT reference, Single ACE, and Model B side by side.
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
    r'/AlN_ModelB_v3_rich_physics/reports/validation/phase3c'
    r'/comparison_report/data'
)
OUT_DIR = (
    r'G:/Xiaogan_Supercomputing_data/egp/EGP-milp/papers'
    r'/v3_single_vs_modelb/figures'
)

COLOR_DFT = '#333333'
COLOR_SA  = '#E69F00'
COLOR_MB  = '#0072B2'

# Which constants to display (exclude C66 which is not independent)
CONSTANTS = ['C11', 'C12', 'C13', 'C33', 'C44']
LABELS    = ['$C_{11}$', '$C_{12}$', '$C_{13}$', '$C_{33}$', '$C_{44}$']


def main():
    setup_style(journal='nature', lang='en', constrained_layout=True)

    df = pd.read_csv(f'{DATA_DIR}/elastic_comparison_table.csv')

    # Extract values
    dft_vals = df[df['constant'].isin(CONSTANTS)]['DFT_GPa'].values
    sa_vals  = df[df['constant'].isin(CONSTANTS)]['Single_ACE_GPa'].values
    mb_vals  = df[df['constant'].isin(CONSTANTS)]['Model_B_GPa'].values

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(7.0, 4.5))

    n_groups = len(CONSTANTS)
    x = np.arange(n_groups)
    width = 0.25

    bars_dft = ax.bar(x - width, dft_vals, width,
                      color=COLOR_DFT, edgecolor='white', linewidth=0.4,
                      label='DFT')
    bars_sa  = ax.bar(x, sa_vals, width,
                      color=COLOR_SA, edgecolor='white', linewidth=0.4,
                      label='Single ACE')
    bars_mb  = ax.bar(x + width, mb_vals, width,
                      color=COLOR_MB, edgecolor='white', linewidth=0.4,
                      label='Model B')

    # Value labels on bars
    def _label_bars(bars, fmt='.0f', fontsize=6.5):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 3,
                    f'{h:{fmt}}', ha='center', va='bottom',
                    fontsize=fontsize, fontweight='normal')

    _label_bars(bars_dft)
    _label_bars(bars_sa)
    _label_bars(bars_mb)

    ax.set_xticks(x)
    ax.set_xticklabels(LABELS)
    ax.set_ylabel('Elastic constant (GPa)')
    ax.legend(frameon=True, fancybox=False, edgecolor='#999999', fontsize=8,
              loc='upper right')
    ax.grid(True, axis='y', alpha=0.25, linestyle=':')

    # Expand y-limit to leave room for bar labels
    ymax = max(dft_vals.max(), sa_vals.max(), mb_vals.max()) * 1.18
    ax.set_ylim(0, ymax)

    finalize_figure(fig)
    add_panel_labels(fig, style='nature', labels=['a'],
                     x_offset_pt=-22, y_offset_pt=3)

    # --- QA ---
    try:
        png = render_preview(fig, f'{OUT_DIR}/_preview_fig2.png', dpi=150)
    except Exception:
        pass
    issues = audit_layout(fig)
    print_report(issues)

    # --- Export ---
    paths = export_figure(
        fig,
        basename=f'{OUT_DIR}/fig2_elastic_comparison',
        formats=['pdf', 'png'],
        size_inches=(7.0, 4.5),
        dpi=300,
        grayscale_preview=True,
    )
    print(f'[Fig 2] Done: {paths}')
    plt.close(fig)


if __name__ == '__main__':
    main()
