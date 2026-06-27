#!/usr/bin/env python3
"""Fix Fig 1: EOS + SCX data cleaning context (two-panel)."""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.gridspec import GridSpec

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(THIS_DIR, 'scx_figures')
os.makedirs(OUT_DIR, exist_ok=True)
PHASE3C_DATA = (
    r'G:/Xiaogan_Supercomputing_data/egp/VASP/training_workspaces'
    r'/AlN_ModelB_v3_rich_physics/reports/validation/phase3c'
    r'/comparison_report/data'
)

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 11,
    'axes.titlesize': 13, 'axes.labelsize': 12,
    'legend.fontsize': 9, 'figure.dpi': 150,
    'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'axes.spines.top': False, 'axes.spines.right': False,
})

C_DFT  = '#333333'
C_SA   = '#E69F00'
C_MB   = '#0072B2'
C_SCX  = '#009E73'
C_NOISE = '#D55E00'
C_CLEAN = '#999999'

# ═══════════════════════════════════════════
def main():
    # ── Left: EOS comparison (DFT/SA/MB) ──
    data = pd.read_csv(os.path.join(PHASE3C_DATA, 'eos_curve_data.csv'))
    dft = data[data['dataset']=='DFT'].sort_values('vol_per_atom_A3')
    sa  = data[data['dataset']=='Single_ACE'].sort_values('vol_per_atom_A3')
    mb  = data[data['dataset']=='Model_B'].sort_values('vol_per_atom_A3')
    v_fine = np.linspace(dft['vol_per_atom_A3'].min(), dft['vol_per_atom_A3'].max(), 300)

    fig = plt.figure(figsize=(13, 5.5))
    gs = GridSpec(1, 2, width_ratios=[1.2, 1], wspace=0.35)

    # ── Left panel: EOS curves ──
    ax1 = fig.add_subplot(gs[0])

    cs_dft = interpolate.CubicSpline(dft['vol_per_atom_A3'], dft['energy_fit_eV'], bc_type='natural')
    e_dft = cs_dft(v_fine)
    v0_dft = v_fine[np.argmin(e_dft)]
    ax1.plot(v_fine, e_dft - e_dft.min(), '-', color=C_DFT, lw=2.5, label=f'DFT (V$_0$={v0_dft:.1f})')
    ax1.scatter(dft['vol_per_atom_A3'], dft['energy_per_atom_eV'] - e_dft.min(),
                c=C_DFT, marker='s', s=50, zorder=5, edgecolors='white', linewidth=0.5)

    cs_sa = interpolate.CubicSpline(sa['vol_per_atom_A3'], sa['energy_fit_eV'], bc_type='natural')
    e_sa = cs_sa(v_fine)
    v0_sa = v_fine[np.argmin(e_sa)]
    ax1.plot(v_fine, e_sa - e_sa.min(), '--', color=C_SA, lw=2, label=f'Single ACE (V$_0$={v0_sa:.1f}, B$_0$=209.5)')
    ax1.scatter(sa['vol_per_atom_A3'], sa['energy_per_atom_eV'] - e_sa.min(),
                c=C_SA, marker='^', s=40, zorder=4, edgecolors='white', linewidth=0.5)

    cs_mb = interpolate.CubicSpline(mb['vol_per_atom_A3'], mb['energy_fit_eV'], bc_type='natural')
    e_mb = cs_mb(v_fine)
    v0_mb = v_fine[np.argmin(e_mb)]
    ax1.plot(v_fine, e_mb - e_mb.min(), '-.', color=C_MB, lw=2, label=f'Model B (V$_0$={v0_mb:.1f}, B$_0$=201.8)')
    ax1.scatter(mb['vol_per_atom_A3'], mb['energy_per_atom_eV'] - e_mb.min(),
                c=C_MB, marker='o', s=40, zorder=4, edgecolors='white', linewidth=0.5)

    ax1.set_xlabel('Volume per atom (A$^3$)')
    ax1.set_ylabel('Energy per atom (eV)')
    ax1.set_title('(a) EOS Comparison: DFT vs Single ACE vs Model B', fontweight='bold', loc='left')
    ax1.legend(frameon=True, fancybox=False, edgecolor='gray')

    # ── Right panel: SCX data cleaning context ──
    ax2 = fig.add_subplot(gs[1])

    batches = ['Equil.', 'EOS', 'Elastic', 'Cross', 'Phonon', 'Thermal', 'MLMD']
    totals  = [6, 34, 126, 80, 120, 108, 60]
    noises  = [0,  0,   0,   0,   0,  53, 21]
    pct     = [0,  0,   0,   0,   0,  49.1, 35.0]

    x = np.arange(len(batches))
    w = 0.35

    # Stacked: clean (gray) + noisy (red)
    clean = [t - n for t, n in zip(totals, noises)]
    bars_clean = ax2.bar(x, clean, w, color=C_CLEAN, label='Clean frames', edgecolor='white')
    bars_noise = ax2.bar(x, noises, w, bottom=clean, color=C_NOISE, label='SCX-detected noise (fmax>5)', edgecolor='white')

    # Annotate noise %
    for i in range(len(batches)):
        if pct[i] > 0:
            ax2.annotate(f'{pct[i]:.0f}%', (x[i], totals[i] + 3),
                        ha='center', fontsize=9, fontweight='bold', color=C_NOISE)

    # Highlight EOS region (clean → SCX不需要动)
    ax2.axvspan(-0.5, 4.5, alpha=0.06, color=C_SCX)
    ax2.annotate('SCX keeps these\n(0% noise)', xy=(2, max(totals)*0.75),
                fontsize=11, color=C_SCX, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85, edgecolor=C_SCX))

    # Highlight thermal/MLMD (dirty → SCX removes)
    ax2.axvspan(4.5, 6.5, alpha=0.08, color=C_NOISE)
    ax2.annotate('SCX removes\nthese', xy=(5.5, max(totals)*0.45),
                fontsize=11, color=C_NOISE, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85, edgecolor=C_NOISE))

    ax2.set_xticks(x)
    ax2.set_xticklabels(batches, rotation=25, fontsize=10)
    ax2.set_ylabel('Number of Training Frames')
    ax2.set_title('(b) SCX Data Audit: Which batches are clean vs noisy', fontweight='bold', loc='left')
    ax2.legend(frameon=True, fancybox=False, fontsize=9, loc='upper left')

    # ── Overall title ──
    fig.suptitle('Fig 1: EOS + SCX Data Quality — AlN v3 Training Data (534 frames)',
                 fontsize=15, fontweight='bold', y=1.02)
    fig.savefig(os.path.join(OUT_DIR, 'fig1_eos_comparison.png'))
    plt.close(fig)
    print('[OK] Fig 1 (fixed): two-panel EOS + SCX audit')

if __name__ == '__main__':
    main()
