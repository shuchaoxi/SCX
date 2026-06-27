#!/usr/bin/env python3
"""
Fig 1: EOS Curve Comparison — Single ACE vs Model B against DFT reference.

Shows the Birch-Murnaghan EOS fitted curves for each model alongside
the raw DFT reference points, with the equilibrium volume V0 marked.
"""
import sys
sys.path.insert(0, r'C:/Users/admin/.claude/skills/scipilot-figure-skill/scripts')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate

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

# Okabe-Ito colour-blind safe palette
COLOR_DFT = '#333333'
COLOR_SA  = '#E69F00'
COLOR_MB  = '#0072B2'


def main():
    setup_style(journal='nature', lang='en', constrained_layout=True)

    data = pd.read_csv(f'{DATA_DIR}/eos_curve_data.csv')
    dft = data[data['dataset'] == 'DFT'].sort_values('vol_per_atom_A3').reset_index(drop=True)
    sa  = data[data['dataset'] == 'Single_ACE'].sort_values('vol_per_atom_A3').reset_index(drop=True)
    mb  = data[data['dataset'] == 'Model_B'].sort_values('vol_per_atom_A3').reset_index(drop=True)

    # --- Smooth EOS curves via cubic spline ---
    v_vals = dft['vol_per_atom_A3'].values
    v_fine = np.linspace(v_vals.min(), v_vals.max(), 300)

    curves = {}
    for name, df in [('DFT', dft), ('SA', sa), ('MB', mb)]:
        cs = interpolate.CubicSpline(
            df['vol_per_atom_A3'].values,
            df['energy_fit_eV'].values,
            bc_type='natural',
        )
        curves[name] = cs(v_fine)

    # --- V0: equilibrium volume from DFT EOS minimum ---
    v0 = v_fine[np.argmin(curves['DFT'])]

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(7.0, 4.5))

    # DFT reference: thin EOS curve + scatter points (legend only on scatter)
    ax.plot(v_fine, curves['DFT'], '-', color=COLOR_DFT, linewidth=1.0, alpha=0.5,
            zorder=2, label=None)
    ax.scatter(dft['vol_per_atom_A3'], dft['energy_per_atom_eV'],
               s=65, color=COLOR_DFT, marker='o',
               facecolors='white', edgecolors=COLOR_DFT,
               linewidths=1.2, zorder=4,
               label='DFT (reference)')

    # Single ACE: dashed curve
    ax.plot(v_fine, curves['SA'], '--', color=COLOR_SA, linewidth=1.8,
            label='Single ACE', zorder=2)
    ax.scatter(sa['vol_per_atom_A3'], sa['energy_fit_eV'],
               s=40, color=COLOR_SA, marker='D', zorder=3, label=None)

    # Model B: solid curve
    ax.plot(v_fine, curves['MB'], '-', color=COLOR_MB, linewidth=1.8,
            label='Model B', zorder=2)
    ax.scatter(mb['vol_per_atom_A3'], mb['energy_fit_eV'],
               s=40, color=COLOR_MB, marker='s', zorder=3, label=None)

    # V0 marker
    ax.axvline(x=v0, color=COLOR_DFT, linestyle=':', linewidth=0.9, alpha=0.6, zorder=1)
    ylo, yhi = ax.get_ylim()
    ax.annotate(f'$V_0$ = {v0:.2f} $\\AA^3$',
                xy=(v0, ylo + 0.08 * (yhi - ylo)),
                fontsize=8, color=COLOR_DFT, ha='center', va='bottom',
                rotation=0)

    ax.set_xlabel(r'Volume ($\AA^3$/atom)')
    ax.set_ylabel('Energy per atom (eV)')
    ax.legend(frameon=True, fancybox=False, edgecolor='#999999', fontsize=8,
              loc='lower right')
    ax.grid(True, alpha=0.25, linestyle=':')

    finalize_figure(fig)
    add_panel_labels(fig, style='nature', labels=['a'],
                     x_offset_pt=-22, y_offset_pt=3)

    # --- QA ---
    try:
        png = render_preview(fig, f'{OUT_DIR}/_preview_fig1.png', dpi=150)
    except Exception:
        pass
    issues = audit_layout(fig)
    print_report(issues)

    # --- Export ---
    paths = export_figure(
        fig,
        basename=f'{OUT_DIR}/fig1_eos_comparison',
        formats=['pdf', 'png'],
        size_inches=(7.0, 4.5),
        dpi=300,
        grayscale_preview=True,
    )
    print(f'[Fig 1] Done: {paths}')
    plt.close(fig)


if __name__ == '__main__':
    main()
