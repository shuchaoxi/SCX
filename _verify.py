import re, os

cn_re = re.compile(r'[\u4e00-\u9fff]+')

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

total_cn = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        c = fh.read()
    cn = len(cn_re.findall(c))
    total_cn += cn
    author = 'SCX' if '\\author{SCX}' in c else 'MISSING'
    has_textsf = '\\textsf' in c
    has_mathsf = '\\mathsf' in c
    status = '✓' if cn == 0 else f'✗ ({cn} CN)'
    issues = []
    if not has_textsf and has_mathsf:
        issues.append('has \\mathsf')
    print(f'{status} {os.path.basename(f):50s} author={author} textsf={has_textsf} mathsf={has_mathsf} {" ".join(issues)}')

print(f'\nTotal CN segments: {total_cn}')
