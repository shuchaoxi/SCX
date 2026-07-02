#!/usr/bin/env python3
"""Translate Chinese content to English in Batch C .tex files."""
import re, os

BASE = "F:/scx"

files = [
    'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
    'theory/self_evolution/ppe_rigorous_derivation.tex',
    'theory/self_evolution/README.tex',
    'theory/self_evolution/situs_final_verification.tex',
    'theory/self_evolution/situs_physical_validation.tex',
    'theory/self_evolution/spring_convergence_analysis.tex',
    'theory/self_evolution/spring_hostile_review.tex',
    'theory/self_evolution/SPRING_NAMING.tex',
    'theory/theorems/01_noise_detection_guarantee.tex',
    'theory/theorems/02_weak_feature_failure.tex',
    'theory/theorems/03_unidentifiability_theorem.tex',
    'theory/theorems/README.tex',
    'theory/THEOREMS_UNIFIED.tex',
    'paper/archive/scx_llm/main.tex',
]

cn_pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+')

for f in files:
    full = os.path.join(BASE, f)
    if not os.path.exists(full):
        print(f'=== {f}: FILE NOT FOUND ===')
        continue
    with open(full, 'r', encoding='utf-8') as fh:
        content = fh.read()
    matches = cn_pattern.findall(content)
    if matches:
        print(f'=== {f}: {len(matches)} Chinese segments ===')
        for m in matches[:25]:
            print(f'  [{len(m)}] {m[:120]}')
        if len(matches) > 25:
            print(f'  ... and {len(matches)-25} more')
    else:
        print(f'=== {f}: NO Chinese found ===')
