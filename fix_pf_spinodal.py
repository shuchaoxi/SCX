#!/usr/bin/env python3
"""Fix the spinodal potential in Phase Field paper."""
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_phase_field/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Fix the potential: add negative sign to quadratic term for non-convexity
old = "f_S(\\Sf) = \\frac{\\alpha}{2} (\\Sf - \\Sf_0)^2 + \\frac{\\beta}{4} \\Sf^4"
new = "f_S(\\Sf) = -\\frac{\\alpha}{2} (\\Sf - \\Sf_0)^2 + \\frac{\\beta}{4} \\Sf^4"

# Fix in the definition
if old in content:
    content = content.replace(old, new)
    changes.append("Fixed f_S: added negative sign for non-convexity")
else:
    # Try alternative escaping
    idx = content.find("\\Sf - \\Sf_0)^2")
    if idx >= 0:
        snippet = content[idx-30:idx+5]
        print(f"Found: {repr(snippet)}")

# Fix in description text
old_desc = "势能密度 $f_S$（极值在参考势能 $\\Sf_0$ 附近）"
new_desc = "势能密度 $f_S$（负二次项产生旋节分解所需非凸性，正四次项确保全局稳定性）"
if old_desc in content:
    content = content.replace(old_desc, new_desc)
    changes.append("Fixed f_S description: added non-convexity explanation")

# Fix chemical potential (mu_S) - add negative sign
old_mu = "\\alpha(\\Sf - \\Sf_0) + \\beta \\Sf^3 - \\kappa_S \\lap \\Sf + \\lambda \\|\\gf\\|^2"
new_mu = "-\\alpha(\\Sf - \\Sf_0) + \\beta \\Sf^3 - \\kappa_S \\lap \\Sf + \\lambda \\|\\gf\\|^2"
if old_mu in content:
    content = content.replace(old_mu, new_mu)
    changes.append("Fixed mu_S: sign to match potential")

# Fix the critical inequality threshold
old_crit = "\\Delta_{crit}^2 \\approx \\alpha \\Sf_0^2 / \\beta"
new_crit = "\\Delta_{crit}^2 \\approx \\frac{\\alpha \\Sf_0^2}{3\\beta} \\quad (from f_S''(\\bar{S})=0)"
if old_crit in content:
    content = content.replace(old_crit, new_crit)
    changes.append("Fixed Delta_crit^2: corrected scaling from spinodal condition")

# Fix the spinodal condition text
old_spin = "\\bar^2 > \\alpha/(3\\beta) - \\Sf_0\\alpha/(3\\beta\\bar)"
new_spin = "\\bar{S}^2 < \\frac{\\alpha}{3\\beta} \\quad (when \\alpha > 0)"
if old_spin in content:
    content = content.replace(old_spin, new_spin)
    changes.append("Fixed spinodal condition: corrected inequality and S_0 dependence")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(f"  [FIX] {c}")
if not changes:
    print("No changes - pattern matching failed")

# Verify key lines
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'f_S(\\Sf)' in line and 'alpha' in line:
        print(f"  Line {i+1}: {line.rstrip()[:80]}")
    if 'mu_S' in line:
        print(f"  Line {i+1}: {line.rstrip()[:80]}")
