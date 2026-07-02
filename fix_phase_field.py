#!/usr/bin/env python3
"""Fix critical errors in Phase Field paper (R5 review)."""
import sys

filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_phase_field/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Fix 1: CRITICAL - Double-well potential f_g
# OLD: f_g(gf) = (A/4)||gf||^4 - (B/2)||gf||^2
# This makes g=0 a MAXIMUM, contradicting the claim that g=0 is a minimum (honest phase)
# NEW: f_g(gf) = (A/4)(||gf||^2 - B/A)^2 = (A/4)||gf||^4 - (B/2)||gf||^2 + B^2/(4A)
# This gives minima at both gf=0 and gf=sqrt(B/A)

old_fg = "f_g(\\gf) = \\frac{A}{4} \\|\\gf\\|^4 - \\frac{B}{2} \\|\\gf\\|^2"
new_fg = "f_g(\\gf) = \\frac{A}{4} \\left(\\|\\gf\\|^2 - \\frac{B}{A}\\right)^2 = \\frac{A}{4} \\|\\gf\\|^4 - \\frac{B}{2} \\|\\gf\\|^2 + \\frac{B^2}{4A}"

if old_fg in content:
    content = content.replace(old_fg, new_fg)
    changes.append("Fixed f_g: now true double-well with minima at gf=0 and gf=sqrt(B/A)")
else:
    # Try with just the equation part
    idx = content.find("\\frac{A}{4} \\|\\gf\\|^4 - \\frac{B}{2} \\|\\gf\\|^2")
    if idx >= 0:
        snippet = content[idx-20:idx+50]
        print(f"Found related: {repr(snippet)}")

# Fix 2: Update the description text about f_g minima
old_desc = "规范双阱势 $f_g$（极值在诚实地带 $\\|\\gf\\|=0$ 和不诚实地带 $\\|\\gf\\|=\\sqrt{B/A}$）"
new_desc = "规范双阱势 $f_g$（双稳态在诚实地带 $\\|\\gf\\|=0$ 和不诚实地带 $\\|\\gf\\|=\\sqrt{B/A}$，两者均为局部极小值）"

if old_desc in content:
    content = content.replace(old_desc, new_desc)
    changes.append("Fixed f_g description: both minima not extreme values")

# Fix 3: The nucleation free energy gain Delta f
# With corrected f_g: f_g(g_eq) = 0, f_g(0) = B^2/(4A)
# Delta f = f_g(g_eq) - f_g(0) = -B^2/(4A) but |Delta f| = B^2/(4A)
# The nucleation formula uses -Delta f * V, so we need the magnitude
# Keep the magnitude but clarify

old_df = "\\Delta f = f_g(g_{eq}) - f_g(0) = B^2/(4A) —"
new_df = "\\Delta f = |f_g(g_{eq}) - f_g(0)| = B^2/(4A) —"

if old_df in content:
    content = content.replace(old_df, new_df)
    changes.append("Fixed Delta_f: clarified absolute value")

# Fix 4: Critical radius formula - need to recalculate
# With sigma_g = (2√(2κ_g)/3) * B^{3/2}/A and |Delta f| = B^2/(4A):
# R_c(2D) = sigma_g / |Delta f| = (8√(2κ_g)/3) / sqrt(B)
# The old formula had sqrt(B)/sqrt(A) dependence which was wrong

# Fix the 2D critical radius formula
old_rc2d = "\\Rc^{(2)} &= \\frac{\\sigma_g}{\\Delta f}\n>   = \\frac{8\\sqrt{2\\kappa_g}}{3} \\cdot \\frac{\\sqrt{B}}{A^{1/2}}"
new_rc2d = "\\Rc^{(2)} &= \\frac{\\sigma_g}{\\Delta f}\n>   = \\frac{8\\sqrt{2\\kappa_g}}{3} \\cdot \\frac{1}{\\sqrt{B}}"

if old_rc2d in content:
    content = content.replace(old_rc2d, new_rc2d)
    changes.append("Fixed R_c(2D): corrected B and A dependence")
else:
    # Try without newline
    old_rc2d_flat = "\\Rc^{(2)} &= \\frac{\\sigma_g}{\\Delta f}\n>   = \\frac{8\\sqrt{2\\kappa_g}}{3} \\cdot \\frac{\\sqrt{B}}{A^{1/2}}"
    if old_rc2d_flat in content:
        content = content.replace(old_rc2d_flat, new_rc2d)
        changes.append("Fixed R_c(2D): corrected B and A dependence")

# Fix the 3D critical radius formula
old_rc3d = "\\Rc^{(3)} &= \\frac{2\\sigma_g}{\\Delta f}\n>   = \\frac{16\\sqrt{2\\kappa_g}}{3} \\cdot \\frac{\\sqrt{B}}{A^{1/2}}"
new_rc3d = "\\Rc^{(3)} &= \\frac{2\\sigma_g}{\\Delta f}\n>   = \\frac{16\\sqrt{2\\kappa_g}}{3} \\cdot \\frac{1}{\\sqrt{B}}"

if old_rc3d in content:
    content = content.replace(old_rc3d, new_rc3d)
    changes.append("Fixed R_c(3D): corrected B and A dependence")

# Fix 5: Gibbs-Thomson capillary length
# d_0 = sigma_g / (2*Delta_f)
old_d0 = "d_0 = \\sigma_g/(2\\Delta f)"
new_d0 = "d_0 = \\frac{\\sigma_g}{2|\\Delta f|}"

if old_d0 in content:
    content = content.replace(old_d0, new_d0)
    changes.append("Fixed capillary length: added absolute value")

# Fix 6: Interface energy derivation - ensure references are consistent
# The derivation uses the shifted potential f_g - f_g(g_eq)
# This is fine with the corrected f_g since f_g(g_eq) = 0 now

# Fix 7: The spinodal decomposition condition
# The condition f_S''(bar) < 0 depends on the quartic potential form
# The paper's f_S has f_S''(S) = alpha + 3*beta*S^2
# The "spinodal region" condition needs to be verified

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(f"  [FIX] {c}")
if not changes:
    print("No changes applied - pattern matching failed")
else:
    print(f"\nTotal: {len(changes)} changes applied")

# Verify key fixes
with open(filepath, 'r', encoding='utf-8') as f:
    verify_lines = f.readlines()

for i, line in enumerate(verify_lines):
    if 'f_g(\\gf)' in line or 'f_g(' in line:
        if 'frac{A}{4}' in line:
            print(f"\nLine {i+1}: {line.rstrip()}")
    if '\Rc^{(2)}' in line or 'Rc^{(2)}' in line:
        print(f"Line {i+1}: {line.rstrip()}")
