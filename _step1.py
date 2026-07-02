#!/usr/bin/env python3
"""Step 1: Translate small files in Batch C."""
import re, os
BASE = r"F:\scx"

def replace_all(path, mapping):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    for cn, en in sorted(mapping.items(), key=lambda x: -len(x[0])):
        c = c.replace(cn, en)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    return len(re.findall(r'[\u4e00-\u9fff]+', c))

# File 1: SPRING_NAMING.tex
replace_all(os.path.join(BASE, 'theory/self_evolution/SPRING_NAMING.tex'), {
    '春季算法': 'Spring Algorithm',
    '复苏': 'resurrection',
})
print("SPRING_NAMING done")

# File 2: THEOREMS_UNIFIED.tex  
replace_all(os.path.join(BASE, 'theory/THEOREMS_UNIFIED.tex'), {
    '越小，界越宽松': 'The smaller it is, the looser the bound',
    '这反映了检测稀有噪声的内在困难。': 'This reflects the inherent difficulty of detecting rare noise.',
})
print("THEOREMS_UNIFIED done")

# File 3: scx_llm/main.tex
replace_all(os.path.join(BASE, 'paper/archive/scx_llm/main.tex'), {
    '雅洁': 'Yajie',
})
print("scx_llm done")

print("Step 1 complete")
