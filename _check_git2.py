import sys, re, subprocess, os

files_to_check = [
    'theory/definitions/01_state_conditioned_risk.tex',
    'theory/explorations/a2_correlation_analysis.tex',
    'theory/explorations/a2_rigorous_analysis.tex',
    'theory/explorations/exact_constant_minimax.tex',
    'theory/explorations/scx_galois_deep.tex',
    'theory/explorations/turbulence_unidentifiability.tex',
    'theory/information_theory/fano_scx.tex',
    'theory/information_theory/information_limits.tex',
    'theory/information_theory/landauer_scx.tex',
    'theory/propositions/01_global_ranking_insufficiency.tex',
    'theory/propositions/02_higherror_suboptimality.tex',
]

cn_re = re.compile(r'[\u4e00-\u9fff]+')
commits = ['b4374e7', '566dfb6', '23b3b65', 'bc6cacd']

for fpath in files_to_check:
    with open(fpath, encoding='utf-8') as f:
        cur = f.read()
    cur_cn = len(cn_re.findall(cur))
    
    best_commit = None
    best_cn = cur_cn
    
    for commit in commits:
        try:
            out = subprocess.check_output(['git', 'show', f'{commit}:{fpath}'], 
                                           cwd=r'F:\scx', text=True, stderr=subprocess.DEVNULL)
            git_cn = len(cn_re.findall(out))
            if git_cn < best_cn:
                best_cn = git_cn
                best_commit = commit
        except:
            pass
    
    if best_commit:
        print(f'{os.path.basename(fpath)}: cur={cur_cn}, best={best_cn} @ {best_commit}')
    else:
        print(f'{os.path.basename(fpath)}: cur={cur_cn}, no better git found')
