import sys, re, subprocess, os

files_to_check = [
    'theory/definitions/01_state_conditioned_risk.tex',
    'theory/explorations/a2_correlation_analysis.tex',
    'theory/explorations/a2_rigorous_analysis.tex',
    'theory/explorations/exact_constant_minimax.tex',
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

cn_re = re.compile(r'[\u4e00-\u9fff]+')

for fpath in files_to_check:
    # Check current CN
    with open(fpath, encoding='utf-8') as f:
        cur = f.read()
    cur_cn = len(cn_re.findall(cur))
    
    # Check git version
    try:
        out = subprocess.check_output(['git', 'show', f'1665241:{fpath}'], 
                                       cwd=r'F:\scx', text=True, stderr=subprocess.DEVNULL)
        git_cn = len(cn_re.findall(out))
        print(f'{os.path.basename(fpath)}: current={cur_cn} CN, git(1665241)={git_cn} CN')
        if git_cn < cur_cn:
            print(f'  -> git version has {cur_cn-git_cn} fewer CN segments!')
    except:
        print(f'{os.path.basename(fpath)}: current={cur_cn} CN, git=N/A')
