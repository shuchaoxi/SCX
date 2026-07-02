import re, os

files = [
    'theory/propositions/05_expert_governance_protocol.tex',
    'theory/SCX_Undiscovered_Theorems.tex',
    'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
    'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
    'theory/self_evolution/ppe_rigorous_derivation.tex',
    'theory/self_evolution/situs_final_verification.tex',
    'theory/self_evolution/situs_physical_validation.tex',
]
for f in files:
    path = os.path.join('F:/scx', f)
    if not os.path.exists(path):
        print(f'{f}: NOT FOUND')
        continue
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    chinese = [i for i, c in enumerate(content) if '\u4e00' <= c <= '\u9fff']
    if chinese:
        print(f'=== {f}: {len(chinese)} Chinese chars ===')
        for pos in chinese[:20]:
            ctx = content[max(0,pos-30):pos+30]
            print(f'  pos={pos}: ...{repr(ctx)}...')
        if len(chinese) > 20:
            print(f'  ... and {len(chinese)-20} more')
    else:
        print(f'=== {f}: CLEAN ===')
