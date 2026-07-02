#!/usr/bin/env python3
"""Extract all remaining Chinese fragments after first-pass translation."""
import re, sys

files = [
    'F:/scx/theory/self_evolution/spring_convergence_analysis.tex',
    'F:/scx/theory/self_evolution/spring_hostile_review.tex',
    'F:/scx/theory/theorems/01_noise_detection_guarantee.tex',
    'F:/scx/theory/theorems/02_weak_feature_failure.tex',
    'F:/scx/theory/theorems/03_unidentifiability_theorem.tex',
]

all_chinese = set()
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    for m in re.finditer(r'[\u4e00-\u9fff]{1,}', text):
        all_chinese.add(m.group())

for phrase in sorted(all_chinese, key=lambda x: (-len(x), x)):
    print(phrase)
