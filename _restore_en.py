import subprocess, os

files = [
    'theory/definitions/01_state_conditioned_risk.tex',
    'theory/explorations/a2_correlation_analysis.tex',
    'theory/explorations/a2_rigorous_analysis.tex',
    'theory/explorations/exact_constant_minimax.tex',
    'theory/explorations/scx_complexity.tex',
    'theory/explorations/scx_galois_deep.tex',
    'theory/explorations/turbulence_unidentifiability.tex',
    'theory/explorations/verification_exact_constant.tex',
    'theory/information_theory/fano_scx.tex',
    'theory/information_theory/information_limits.tex',
    'theory/information_theory/landauer_scx.tex',
    'theory/propositions/01_global_ranking_insufficiency.tex',
    'theory/propositions/01_regret_lower_bound.tex',
    'theory/propositions/02_higherror_suboptimality.tex',
]

for fpath in files:
    try:
        out = subprocess.check_output(['git', 'show', f'b4374e7:{fpath}'], 
                                       cwd=r'F:\scx', text=True, stderr=subprocess.DEVNULL)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f'✓ Restored: {os.path.basename(fpath)}')
    except Exception as e:
        print(f'✗ Failed: {os.path.basename(fpath)}: {e}')
