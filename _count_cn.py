import re, os

cn_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

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

for f in files:
    if not os.path.exists(f):
        print(f'MISSING: {f}')
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    segments = cn_pattern.findall(content)
    total_cn = sum(len(s) for s in segments)
    print(f'{f}: {len(segments)} segments, {total_cn} Chinese chars')
