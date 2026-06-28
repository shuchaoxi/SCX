#!/usr/bin/env python3
"""
Fig 3: Grouped Error Comparison — Energy and Force RMSE per validation batch.

Upper panel: Energy RMSE (meV/atom)
Lower panel: Force RMSE (eV/AA)

Model B wins in 5/6 batches; Single ACE wins only in the EOS batch.
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

COLOR_SA = '#E69F00'
COLOR_MB = '#0072B2'

# Short labels for the 6 batches (excl. __ALL__ row)
BATCH_LABELS = [
    '01 EOS\nhydrostatic',
    '02 Elastic\nstrain',
    '03 Strain\ndisplacement',
    '04 Phonon\ndisplacement',
    '05 Thermal\nsnapshot',
    '06 Stress10\nMLMD',
]
N_BATCHES = 6


def main():
    setup_style(journal='nature', lang='en', constrained_layout=True)

    df = pd.read_csv(f'{DATA_DIR}/grouped_comparison.csv')
    # Exclude the __ALL__ summary row
    batches = df[df['batch'] != '__ALL__'].iloc[:N_BATCHES].reset_index(drop=True)

    # Data
    x = np.arange(N_BATCHES)
    width = 0.30

    e_sa = batches['Single_ACE_E_RMSE_meV'].values
    e_mb = batches['Model_B_E_RMSE_meV'].values
    f_sa = batches['Single_ACE_F_RMSE'].values
    f_mb = batches['Model_B_F_RMSE'].values

    # --- Plot: 2 rows, 1 col, share x ---
    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(7.0, 5.5), sharex=True,
    )

    # ---- Upper panel: Energy RMSE ----
    bars_e_sa = ax_top.bar(x - width / 2, e_sa, width,
                           color=COLOR_SA, edgecolor='white', linewidth=0.4,
                           label='Single ACE')
    bars_e_mb = ax_top.bar(x + width / 2, e_mb, width,
                           color=COLOR_MB, edgecolor='white', linewidth=0.4,
                           label='Model B')

    # Value labels
    for i in range(N_BATCHES):
        ax_top.text(x[i] - width / 2, e_sa[i] + 1.5, f'{e_sa[i]:.1f}',
                    ha='center', va='bottom', fontsize=6)
        ax_top.text(x[i] + width / 2, e_mb[i] + 1.5, f'{e_mb[i]:.1f}',
                    ha='center', va='bottom', fontsize=6)

    ax_top.set_ylabel('Energy RMSE (meV/atom)')
    ax_top.legend(frameon=True, fancybox=False, edgecolor='#999999',
                  fontsize=7, loc='upper left')
    ax_top.grid(True, axis='y', alpha=0.25, linestyle=':')

    # ---- Lower panel: Force RMSE ----
    bars_f_sa = ax_bot.bar(x - width / 2, f_sa, width,
                           color=COLOR_SA, edgecolor='white', linewidth=0.4,
                           label='Single ACE')
    bars_f_mb = ax_bot.bar(x + width / 2, f_mb, width,
                           color=COLOR_MB, edgecolor='white', linewidth=0.4,
                           label='Model B')

    for i in range(N_BATCHES):
        ax_bot.text(x[i] - width / 2, f_sa[i] + 0.0008, f'{f_sa[i]:.4f}',
                    ha='center', va='bottom', fontsize=6, rotation=45)
        ax_bot.text(x[i] + width / 2, f_mb[i] + 0.0008, f'{f_mb[i]:.4f}',
                    ha='center', va='bottom', fontsize=6, rotation=45)

    ax_bot.set_xticks(x)
    ax_bot.set_xticklabels(BATCH_LABELS, fontsize=7)
    ax_bot.set_ylabel('Force RMSE (eV/AA)')
    ax_bot.legend(frameon=True, fancybox=False, edgecolor='#999999',
                  fontsize=7, loc='upper left')
    ax_bot.grid(True, axis='y', alpha=0.25, linestyle=':')

    # Winner annotation
    ax_top.text(0.98, 0.95,
                'Model B wins 5/6 batches',
                transform=ax_top.transAxes, fontsize=8,
                ha='right', va='top', fontstyle='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#EEEEEE',
                          edgecolor='#999999', alpha=0.85))

    finalize_figure(fig)
    add_panel_labels(fig, style='nature', labels=['a', 'b'],
                     x_offset_pt=-22, y_offset_pt=3)

    # --- QA ---
    try:
        png = render_preview(fig, f'{OUT_DIR}/_preview_fig3.png', dpi=150)
    except Exception:
        pass
    issues = audit_layout(fig)
    print_report(issues)

    # --- Export ---
    paths = export_figure(
        fig,
        basename=f'{OUT_DIR}/fig3_grouped_error',
        formats=['pdf', 'png'],
        size_inches=(7.0, 5.5),
        dpi=300,
        grayscale_preview=True,
    )
    print(f'[Fig 3] Done: {paths}')
    plt.close(fig)


if __name__ == '__main__':
    main()
