import os

files = [
    'theory/archive/arrow_analogy_removed.tex',
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

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        cn_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
        print(f'{f}: {cn_chars} Chinese chars, {len(content)} total chars')
    else:
        print(f'{f}: NOT FOUND')
