#!/usr/bin/env python3
"""
plot_all.py — Master script to generate all 4 figures for the
AlN Single ACE vs Model B comparison paper.

Usage:
    # Use Python 3.11 with required packages (numpy, matplotlib, scipy, pandas):
    "C:/Users/admin/AppData/Local/Programs/Python/Python311/python.exe" plot_all.py

    python plot_all.py          # generate all figures
    python plot_all.py 1        # generate only Fig 1
    python plot_all.py 1 3 4    # generate selected figures

Output directory: figures/ (same folder as this script)
"""
import sys
import os
import time

# Add skill scripts to path if not already
SKILL_DIR = r'C:/Users/admin/.claude/skills/scipilot-figure-skill/scripts'
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

# Make sure we can import our modules
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

SCRIPT_MAP = {
    1: ('plot_fig1_eos', 'Fig 1: EOS Curve Comparison'),
    2: ('plot_fig2_elastic', 'Fig 2: Elastic Constants Comparison'),
    3: ('plot_fig3_grouped', 'Fig 3: Grouped Error Comparison'),
    4: ('plot_fig4_gauge', 'Fig 4: Gauge Trade-off'),
}


def run_figure(fig_id: int) -> float:
    """Import and run one figure script; return elapsed seconds."""
    if fig_id not in SCRIPT_MAP:
        print(f'Unknown figure id: {fig_id}')
        return 0.0

    module_name, description = SCRIPT_MAP[fig_id]
    print(f'\n{"=" * 60}')
    print(f'  {description}')
    print(f'{"=" * 60}')

    t0 = time.time()
    try:
        # Import and run the module's main()
        mod = __import__(module_name)
        mod.main()
        elapsed = time.time() - t0
        print(f'  [OK] Finished in {elapsed:.1f} s')
        return elapsed
    except Exception as e:
        elapsed = time.time() - t0
        print(f'  [FAIL] {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        return elapsed


def main():
    # Parse which figures to generate
    if len(sys.argv) > 1:
        fig_ids = [int(a) for a in sys.argv[1:] if a.isdigit()]
    else:
        fig_ids = [1, 2, 3, 4]

    total_time = 0.0
    for fid in sorted(fig_ids):
        total_time += run_figure(fid)

    print(f'\n{"=" * 60}')
    print(f'  All requested figures generated in {total_time:.1f} s')
    print(f'  Output: {THIS_DIR}/')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
