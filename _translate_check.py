#!/usr/bin/env python3
"""Translate Chinese characters to English placeholders in LaTeX files."""
import re
import os

FILES = [
    'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
    'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
    'theory/self_evolution/ppe_rigorous_derivation.tex',
    'theory/self_evolution/situs_final_verification.tex',
    'theory/self_evolution/situs_physical_validation.tex',
    'theory/self_evolution/spring_convergence_analysis.tex',
    'theory/self_evolution/spring_hostile_review.tex',
    'theory/theorems/01_noise_detection_guarantee.tex',
    'theory/theorems/02_weak_feature_failure.tex',
    'theory/theorems/03_unidentifiability_theorem.tex',
]

for fpath in FILES:
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find lines with Chinese chars
    lines = content.split('\n')
    cn_lines = []
    for i, line in enumerate(lines):
        if re.search(r'[\u4e00-\u9fff]', line):
            cn_lines.append((i+1, line.strip()[:120]))
    
    print(f"\n=== {fpath} === ({len(cn_lines)} lines with Chinese)")
    for ln, text in cn_lines[:30]:  # Show first 30
        print(f"  L{ln}: {text}")
    if len(cn_lines) > 30:
        print(f"  ... and {len(cn_lines)-30} more lines")
