#!/usr/bin/env python3
"""Fix leapfrog integrator - missing epsilon in frac commands."""
import sys

filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes_made = 0
for i, line in enumerate(lines):
    # Find lines containing \frac{2} or \frac{4} without \epsilon (only in leapfrog)
    # We specifically target the leapfrog pattern: \frac{NUMBER} \nabla_q
    # But only when NUMBER is 2 or 4 alone (not \epsilon/2)

    if '\\frac{2} \\nabla_q' in line:
        old = line
        lines[i] = line.replace('\\frac{2} \\nabla_q', '\\frac{\\epsilon}{2} \\nabla_q')
        if old != lines[i]:
            print(f"Fixed line {i+1}: replaced \\frac{{2}} with \\frac{{\\epsilon}}{{2}}")
            changes_made += 1

    if '\\frac{4} \\nabla_q' in line:
        old = line
        lines[i] = line.replace('\\frac{4} \\nabla_q', '\\frac{\\epsilon}{4} \\nabla_q')
        if old != lines[i]:
            print(f"Fixed line {i+1}: replaced \\frac{{4}} with \\frac{{\\epsilon}}{{4}}")
            changes_made += 1

if changes_made:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"\nTotal: {changes_made} fixes applied")
else:
    print("No changes made. Debugging...")
    for i in range(189, 207):
        if i < len(lines):
            print(f"Line {i+1}: {repr(lines[i])}")
