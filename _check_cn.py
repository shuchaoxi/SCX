import re, os
files = [
'theory/self_evolution/ppe_rigorous_derivation.tex',
'theory/self_evolution/spring_hostile_review.tex',
'theory/self_evolution/spring_convergence_analysis.tex',
'theory/self_evolution/situs_physical_validation.tex',
'theory/theorems/03_unidentifiability_theorem.tex',
'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
'theory/self_evolution/hostile_review.tex',
'theory/SCX_Undiscovered_Theorems.tex',
'theory/theorems/02_weak_feature_failure.tex',
'theory/theorems/01_noise_detection_guarantee.tex',
'theory/self_evolution/situs_final_verification.tex',
'theory/self_evolution/README.tex',
'theory/self_evolution/final_review_nature.tex',
'theory/self_evolution/final_review_jmlr.tex',
'theory/self_evolution/CERCIS_NAMING.tex',
'theory/self_evolution/01_symbol_system.tex',
]
pat = re.compile(r'[\u4e00-\u9fff]')
for f in files:
    path = os.path.join('F:/scx', f.replace('/', '\\'))
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        chars = pat.findall(content)
        if chars:
            unique = list(dict.fromkeys(chars))[:30]
            print(f'{f}: {len(chars)} ch, unique: {" ".join(unique)}')
        else:
            print(f'{f}: CLEAN')
    except FileNotFoundError:
        print(f'{f}: NOT FOUND')
