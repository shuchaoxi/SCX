#!/usr/bin/env python3
"""Final cleanup: fullwidth punctuation → ASCII, CJK symbols, encoding fixes."""
import os

# Fullwidth → ASCII mapping
REPLACEMENTS = [
    ('：', ': '),        # fullwidth colon
    ('，', ', '),        # fullwidth comma
    ('。', '.'),         # ideographic full stop
    ('、', ', '),        # ideographic comma (enumeration)
    ('〇', '0'),         # ideographic number zero
    ('＂', '"'),         # fullwidth quote
    ('＇', "'"),         # fullwidth apostrophe
    ('（', '('),         # fullwidth left paren
    ('）', ')'),         # fullwidth right paren
    ('［', '['),         # fullwidth left bracket
    ('］', ']'),         # fullwidth right bracket
    ('｛', '{'),         # fullwidth left brace
    ('｝', '}'),         # fullwidth right brace
    ('＜', '<'),         # fullwidth less than
    ('＞', '>'),         # fullwidth greater than
    ('｜', '|'),         # fullwidth vertical bar
    ('～', '~'),         # fullwidth tilde
    ('＝', '='),         # fullwidth equals
    ('＋', '+'),         # fullwidth plus
    ('－', '-'),         # fullwidth minus
    ('＊', '*'),         # fullwidth asterisk
    ('／', '/'),         # fullwidth slash
    ('＠', '@'),         # fullwidth at sign
    ('＃', '#'),         # fullwidth hash
    ('＄', '$'),         # fullwidth dollar
    ('％', '%'),         # fullwidth percent
    ('＾', '^'),         # fullwidth caret
    ('＆', '&'),         # fullwidth ampersand
    # Also fix replacement characters
    ('�', ''),           # remove replacement chars (encoding corruption)
]

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
    
    modified = False
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    if modified:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"  CLEANED: {fn}")
    else:
        print(f"  CLEAN: {fn}")
