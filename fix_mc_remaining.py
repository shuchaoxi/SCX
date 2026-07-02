#!/usr/bin/env python3
"""Fix remaining issues in Monte Carlo paper: adaptive step formula and REX duplicate block."""

filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Fix adaptive step: the trace formula needs 1/d factor
old = "{\\bar = \\frac{1}{|\\Situs|} \\int_ \\Tr(h_(q)) \\, dq}"
new = "{\\bar = \\frac{1}{d \\cdot |\\Situs|} \\int_ \\Tr(h_(q)) \\, dq}"
if old in content:
    content = content.replace(old, new)
    changes.append("Fixed adaptive step: added 1/d factor to average eigenvalue formula")
else:
    # Try alternative format
    idx = content.find("\\bar = \\frac{1}{|\\Situs|}")
    if idx >= 0:
        print(f"Found at {idx}: {repr(content[idx:idx+80])}")

# Fix REX duplicate block - find and remove the duplicate eq:rex_mixing_time label
# The block currently has:
# > $$<!-- label: eq:rex_mixing_time -->
# >     \tau_{mix}^{REX}(T_) \leq
# > $$<!-- label: eq:rex_mixing_time -->
# >     \tau_{mix}^{REX}(T_1) \sim
# >     \tau_{mix}(T_R) \cdot \frac{R}{\min_r \bar{A}_{r,r+1}}
# > $$
# Clean it up to a single block

old_rex = """\
> $$<!-- label: eq:rex_mixing_time -->
>     \\tau_{mix}^{REX}(T_) \\leq
> $$<!-- label: eq:rex_mixing_time -->
>     \\tau_{mix}^{REX}(T_1) \\sim
>     \\tau_{mix}(T_R) \\cdot \\frac{R}{\\min_r \\bar{A}_{r,r+1}}
> $$"""

new_rex = """\
> $$<!-- label: eq:rex_mixing_time -->
>     \\tau_{mix}^{REX}(T_1) \\sim
>     \\tau_{mix}(T_R) \\cdot \\frac{R}{\\min_r \\bar{A}_{r,r+1}}
> $$"""

if old_rex in content:
    content = content.replace(old_rex, new_rex)
    changes.append("Fixed REX duplicate block")
else:
    print("REX pattern not found with exact match, looking...")
    if 'rex_mixing_time' in content:
        # Check how many occurrences
        count = content.count('rex_mixing_time')
        print(f"  Found {count} occurrences of 'rex_mixing_time'")

# Fix the description text for Cercis to match the new + sign
if "- lambda" in content:
    content = content.replace("- lambda", "+ lambda")
    changes.append("Fixed any remaining negative lambda in Cercis description")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(c)
if not changes:
    print("No changes made")
