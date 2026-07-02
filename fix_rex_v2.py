#!/usr/bin/env python3
"""Fix REX formula - ensure LaTeX has single backslash \tau."""
import sys

filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We need the file to contain \tau (single backslash)
# Currently it probably contains \\tau (double backslash)
# Fix: replace \\\\ (double backslash in file) with \\ (single backslash)
# But only in the LaTeX math context of the REX formula

# Replace the problematic block
old_block = ">     \\\\tau_{mix}^{REX}(T_1) \\\\sim\n>     \\\\tau_{mix}(T_R) \\\\cdot \\\\frac{R}{\\\\min_r \\\\bar{A}_{r,r+1}}"
new_block = ">     \\tau_{mix}^{REX}(T_1) \\sim\n>     \\tau_{mix}(T_R) \\cdot \\frac{R}{\\min_r \\bar{A}_{r,r+1}}"

if old_block in content:
    content = content.replace(old_block, new_block)
    print("REX formula fixed!")
else:
    # Debug: show what's actually in the content
    idx = content.find('mix}^{REX}')
    if idx >= 0:
        snippet = content[idx-10:idx+80]
        print(f"Content has: {repr(snippet)}")
    else:
        idx = content.find('tau_{mix}')
        if idx >= 0:
            snippet = content[idx-5:idx+80]
            print(f"Content has (tau_mix): {repr(snippet)}")
        else:
            print("tau_mix not found in content")
            # Try to find anywhere near rex_mixing
            idx = content.find('rex_mixing_time')
            if idx >= 0:
                snippet = content[idx:idx+150]
                print(f"rex area: {repr(snippet)}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
