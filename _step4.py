#!/usr/bin/env python3
"""Step 4: Apply universal translation to remaining 8 large files."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _step4_dict import UNIVERSAL

BASE = r"F:\scx"

files = [
    'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
    'theory/self_evolution/ppe_rigorous_derivation.tex',
    'theory/self_evolution/situs_physical_validation.tex',
    'theory/self_evolution/spring_convergence_analysis.tex',
    'theory/self_evolution/spring_hostile_review.tex',
    'theory/theorems/01_noise_detection_guarantee.tex',
    'theory/theorems/02_weak_feature_failure.tex',
    'theory/theorems/03_unidentifiability_theorem.tex',
]

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    before = len(re.findall(r'[\u4e00-\u9fff]+', c))
    
    # Apply all translations, longest first
    items = sorted(UNIVERSAL.items(), key=lambda x: -len(x[0]))
    for cn, en in items:
        if cn in c:
            c = c.replace(cn, en)
    
    after = len(re.findall(r'[\u4e00-\u9fff]+', c))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    
    return before, after

for f in files:
    path = os.path.join(BASE, f)
    if os.path.exists(path):
        b, a = translate_file(path)
        print(f"{os.path.basename(f)}: {b} -> {a} remaining ({b-a} translated)")
    else:
        print(f"MISSING: {f}")

print("Step 4 complete")
