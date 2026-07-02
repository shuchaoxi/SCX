#!/usr/bin/env python3
"""Rewrite the REX formula block correctly."""
import sys

filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the rex_mixing_time block
start = None
end = None
for i, line in enumerate(lines):
    if 'eq:rex_mixing_time' in line:
        start = i
    if start is not None and i > start:
        if '\\bar{A}_{r,r+1}' in line:
            end = i + 1  # include this line
            break

if start is None:
    print("Could not find rex_mixing_time label")
    sys.exit(1)

print(f"Found REX block at lines {start+1} to {end}")

# Build replacement block
new_block = [
    '> $$<!-- label: eq:rex_mixing_time -->\n',
    '>     \\\\tau_{mix}^{REX}(T_1) \\\\sim\n',
    '>     \\\\tau_{mix}(T_R) \\\\cdot \\\\frac{R}{\\\\min_r \\\\bar{A}_{r,r+1}}\n',
    '> $$\n',
]

# Replace old block with new
old_len = end - start
lines[start:end] = new_block

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("REX block rewritten. Verifying:")
with open(filepath, 'r', encoding='utf-8') as f:
    verify = f.readlines()
for i, line in enumerate(verify):
    if 'rex_mixing' in line or 'RET' in line or 'tau_{mix}' in line:
        if i >= start - 2 and i <= end + 2:
            print(f"  {i+1}: {repr(line.rstrip())}")
