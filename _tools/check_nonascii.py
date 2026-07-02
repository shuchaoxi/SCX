#!/usr/bin/env python3
"""Check for non-ASCII in target files."""
import os

base = "F:/scx"
files = [
    "theory/self_evolution/final_review_jmlr.tex",
    "theory/self_evolution/final_review_nature.tex",
    "theory/self_evolution/README.tex",
    "theory/self_evolution/situs_final_verification.tex",
    "theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex",
    "theory/self_evolution/ppe_rigorous_derivation.tex",
    "theory/self_evolution/situs_physical_validation.tex",
    "theory/self_evolution/spring_convergence_analysis.tex",
    "theory/self_evolution/spring_hostile_review.tex",
    "theory/theorems/01_noise_detection_guarantee.tex",
    "theory/theorems/02_weak_feature_failure.tex",
    "theory/theorems/03_unidentifiability_theorem.tex",
]

for fn in files:
    path = os.path.join(base, fn)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    cjk = []
    other = []
    for i, c in enumerate(content):
        cp = ord(c)
        if 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or 0xF900 <= cp <= 0xFAFF:
            cjk.append((i, c, hex(cp)))
        elif cp > 127:
            other.append((i, c, hex(cp)))
    
    print(f"\n=== {fn} ===")
    print(f"  CJK chars: {len(cjk)}")
    print(f"  Other non-ASCII: {len(other)}")
    
    if cjk:
        print("  CJK samples:")
        for pos, char, cp in cjk[:10]:
            ctx = content[max(0,pos-10):pos+11]
            print(f"    pos={pos} char={repr(char)} cp={cp}")
            print(f"    context: {repr(ctx)}")
    
    if other:
        print("  Other non-ASCII samples:")
        for pos, char, cp in other[:10]:
            print(f"    pos={pos} char={repr(char)} cp={cp}")
