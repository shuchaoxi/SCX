import re
import sys

paths = [
    'papers/scx_compactness/main.tex',
    'papers/scx_distillation_hallucination/main.tex',
    'papers/scx_environment/env_gauge.tex'
]

for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    cjk = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]', content)
    if cjk:
        print(f'{path}: FOUND CJK chars ({len(cjk)}): {cjk[:20]}')
    else:
        print(f'{path}: No CJK chars found')
