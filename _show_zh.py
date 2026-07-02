import re, os

# Read each file and show lines with Chinese characters
files = [
    'theory/propositions/03_state_conditioned_weighting.tex',
    'theory/propositions/04_compression_fidelity.tex',
    'theory/propositions/05_expert_governance_protocol.tex',
    'theory/README.tex',
    'theory/scx_8theorems_review.tex',
    'theory/SCX_Next_Theorems.tex',
    'theory/SCX_Undiscovered_Theorems.tex',
    'theory/self_evolution/hostile_review.tex',
    'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
]

for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    
    zh_lines = []
    for i, line in enumerate(lines, 1):
        if re.search(r'[\u4e00-\u9fff]', line):
            zh_lines.append(f"  L{i}: {line.rstrip()[:120]}")
    
    if zh_lines:
        print(f"\n=== {f} ({len(zh_lines)} lines) ===")
        for l in zh_lines[:30]:
            print(l)
        if len(zh_lines) > 30:
            print(f"  ... and {len(zh_lines)-30} more")
