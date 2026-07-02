import re, os
os.chdir(r'F:\scx')
for f in ['papers/scx_pnp/main.tex','papers/scx_kappa_suppression/main.tex','papers/scx_cercis_bound/main.tex']:
    c = open(f, encoding='utf-8').read()
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]', c))
    print(f'{f}: CJK={cjk}')
