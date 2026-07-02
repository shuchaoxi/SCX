#!/usr/bin/env python3
"""Final round of fixes for Monte Carlo paper."""
import re

filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Fix adaptive step trace formula
old_adaptive = '\\bar = \\frac{1}{|\\Situs|} \\int_ \\Tr(h_(q)) \\, dq'
new_adaptive = '\\bar = \\frac{1}{d \\cdot |\\Situs|} \\int_ \\Tr(h_(q)) \\, dq'
if old_adaptive in content:
    content = content.replace(old_adaptive, new_adaptive)
    changes.append("Fixed adaptive step: added 1/d factor")
else:
    print("Adaptive pattern exact:", repr(old_adaptive in content))

# Fix REX block - read lines to handle multi-line pattern
# Find ALL blocks, deduplicate
lines = content.split('\n')
new_lines = []
skip_next = False
rex_count = 0
for i, line in enumerate(lines):
    # Check for duplicate REX label - skip the second occurrence
    if 'eq:rex_mixing_time' in line:
        rex_count += 1
        if rex_count == 2:
            # This is the duplicate label / start of duplicate block
            # Skip this line and the next content line
            skip_next = True
            changes.append(f"Removed duplicate REX block starting at line {i+1}")
            continue
        if rex_count == 1:
            new_lines.append(line)
            # Skip the broken content after first label
            skip_next = True
            continue
    if skip_next:
        # Check if this is a formula continuation line
        if line.strip().startswith('>') and ('\\tau' in line or '$$' in line):
            skip_next = False
            continue
        elif rex_count == 1 and line.strip() == '>':
            skip_next = False
            continue
        else:
            # Keep checking for end of broken block
            if rex_count == 1 and '>' in line:
                skip_next = False
                new_lines.append(line)
                continue
            elif rex_count == 2:
                skip_next = False
                new_lines.append(line)
                continue
    else:
        new_lines.append(line)

# Fix: after 'rex_mixing_time' label, the next content should be the formula
for i, line in enumerate(new_lines):
    if 'eq:rex_mixing_time' in line:
        # The next few lines should contain the actual formula
        # Make sure lines after are the correct formula
        pass

content = '\n'.join(new_lines)

# Remove empty lines between > lines in the REX block
# Also fix the REX formula - it currently has T_ which is undefined
# Should be T_1

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(c)
if not changes:
    print("No changes")

# Verify REX area
with open(filepath, 'r', encoding='utf-8') as f:
    verify_lines = f.readlines()
for i, line in enumerate(verify_lines):
    if 'rex_mixing' in line or 'REX 的混合加速' in line:
        print(f"\nREX area around line {i+1}:")
        for j in range(max(0, i-5), min(len(verify_lines), i+8)):
            print(f"  {j+1}: {verify_lines[j].rstrip()}")
