#!/usr/bin/env python3
"""Additional R5 fixes for Phase Field paper."""
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_phase_field/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Fix Delta f line (line 500)
old = "- $\\Delta f = f_g(g_{eq}) - f_g(0) = B^2/(4A)$"
new = "- $\\Delta f = |f_g(g_{eq}) - f_g(0)| = B^2/(4A)$"
if old in content:
    content = content.replace(old, new)
    changes.append("Fixed Delta f: clarified absolute value")

# Fix appendix derivation (line 975)
old_app = "f_g(\\gf) = \\frac{A}{4}\\|\\gf\\|^4 - \\frac{B}{2}\\|\\gf\\|^2"
new_app = "f_g(\\gf) = \\frac{A}{4}\\left(\\|\\gf\\|^2 - \\frac{B}{A}\\right)^2"
if old_app in content:
    content = content.replace(old_app, new_app)
    changes.append("Fixed appendix derivation: updated f_g form")

# Fix the remark about spinodal condition (line 305-306)
# The condition f_S''(bar) < 0 defines the spinodal
# Currently the expanded form is: bar^2 > alpha/(3*beta) - Sf_0*alpha/(3*beta*bar)
# This should be verified for correctness

# Fix the coupling current sign description (line 323)
# The text says "Potential flows AWAY from high-bias regions" but
# the opposite sign in the gauge equation creates positive feedback
# This is described correctly, but let me ensure clarity

# Fix Theorem 12 nucleation correspondence (line 811-813)
# Check that T_k formula references are consistent
old_tk = "T_k = T_0 \\exp\\left(\\frac{16\\pi}{3} \\frac{\\sigma_g^3}{(\\Delta f)^2}"
new_tk = "T_k = T_0 \\exp\\left(\\frac{16\\pi}{3} \\frac{\\sigma_g^3}{(|\\Delta f|)^2}"
if old_tk in content:
    content = content.replace(old_tk, new_tk)
    changes.append("Fixed Thm12: added absolute value to Delta f in exponent")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(f"  [FIX] {c}")
if not changes:
    print("No additional changes")

# Verify key lines
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'Delta f' in line and 'B^2' in line:
        print(f"Line {i+1}: {line.rstrip()}")
    if 'frac{A}{4}\\|\\gf\\|^4' in line:
        print(f"Line {i+1}: {line.rstrip()}")
