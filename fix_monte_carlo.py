#!/usr/bin/env python3
"""Fix Monte Carlo paper issues found in R5 review."""

import sys

def fix_file():
    with open('G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    changes = []

    # Fix 2: Situs metric definition (lines 90-91)
    # Old: lines 91 contains $h_ = \nabla^2 \mathcal{S}_{total}$
    # Need to find the exact lines
    for i, line in enumerate(lines):
        if '$h_ = \\\\nabla^2 \\\\mathcal{S}_{total}$' in line:
            lines[i] = '> $h_ = \\\\nabla^2 Cercis(E)$，即 $h_{ij,kl} = \\\\frac{\\\\partial^2 Cercis}{\\\\partial g_{ij} \\\\partial g_{kl}}$。\n'
            changes.append(f'Fixed line {i+1}: Situs metric definition')
            # Remove next line if it contained \mathcal{S}_{total} 为总势能面
            if i+1 < len(lines) and '总势能面' in lines[i+1]:
                lines[i+1] = ''
                changes.append(f'Removed obsolete line {i+2}')

    # Fix 3: Adaptive step size - trace vs average eigenvalue
    for i, line in enumerate(lines):
        if 'bar = \\\\frac{1}{|\\Situs|} \\\\int_ \\\\Tr(h_(q))' in line or 'bar = \\frac{1}{|\\Situs|} \\int_ \\Tr(h_(q))' in line:
            lines[i] = lines[i].replace(
                '\\bar{\\lambda} = \\frac{1}{|\\Situs|} \\int_ \\Tr(h_(q)) \\, dq',
                '\\bar{\\lambda} = \\frac{1}{d \\cdot |\\Situs|} \\int_ \\Tr(h_(q)) \\, dq'
            )
            changes.append(f'Fixed line {i+1}: Added dimension factor 1/d to average eigenvalue')

    # Fix 4: Equation of motion sign error (eq:eom_p)
    for i, line in enumerate(lines):
        if '\\dv{p}{t} &= -\\nabla_q U(q) + \\frac{1}{2} \\nabla_q \\big[ p^\\top M(q)^{-1} p \\big]' in line:
            lines[i] = lines[i].replace(
                '\\dv{p}{t} &= -\\nabla_q U(q) + \\frac{1}{2} \\nabla_q \\big[ p^\\top M(q)^{-1} p \\big]',
                '\\dv{p}{t} &= -\\nabla_q U(q) - \\frac{1}{2} \\nabla_q \\big[ p^\\top M(q)^{-1} p \\big]'
            )
            changes.append(f'Fixed line {i+1}: Changed + to - in metric correction term')

    # Fix 5: ESS probabilistic bound - the log(1/delta) scaling is questionable
    for i, line in enumerate(lines):
        if '\\ESS_t \\geq \\frac{K}{B^2 \\log(1/\\delta)}' in line:
            lines[i] = lines[i].replace(
                '\\ESS_t \\geq \\frac{K}{B^2 \\log(1/\\delta)} 以概率至少 $1-\\delta$ 成立',
                '\\ESS_t \\geq \\frac{K}{B^2} - \\mathcal{O}\\left(\\frac{K \\log(1/\\delta)}{B^2}\\right) 以概率至少 $1-\\delta$ 成立'
            )
            changes.append(f'Fixed line {i+1}: Corrected probabilistic ESS bound')

    # Fix 6: MSE bound - C_t = O(B^{2t} log t) is problematic
    for i, line in enumerate(lines):
        if 'C_t = \\Ocal(B^{2t} \\log t)' in line:
            lines[i] = lines[i].replace(
                'C_t = \\Ocal(B^{2t} \\log t)',
                'C_t = \\Ocal(B^2 \\cdot t)'
            )
            changes.append(f'Fixed line {i+1}: Corrected MSE bound from exponential to linear in t')

    # Fix 7: REX mixing time bound - formula is suspect
    # Look for the alternating pattern: \tau_{mix}^{REX}(T_1) \leq \tau_{mix}(T_1) \cdot \min_r
    # Need to fix the formula
    for i in range(len(lines)):
        if 'REX 的混合加速 Mixing Acceleration by REX' in lines[i]:
            # Fix the formula a few lines later
            for j in range(i+5, min(i+20, len(lines))):
                if 'min_{r} \\left\\{' in lines[j]:
                    lines[j] = '> $$<!-- label: eq:rex_mixing_time -->\n'
                    lines[j+1] = '>     \\tau_{mix}^{REX}(T_1) \\sim\n'
                    lines[j+2] = '>     \\tau_{mix}(T_R) \\cdot \\frac{R}{\\min_r \\bar{A}_{r,r+1}}\n'
                    lines[j+3] = '> $$\n'
                    changes.append(f'Fixed REX mixing time formula lines {j+1}-{j+3}')
                    break

    # Write changes
    with open('G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    for c in changes:
        print(c)
    if not changes:
        print("No changes were applied - patterns not matched")
    else:
        print(f"Applied {len(changes)} fixes")

if __name__ == '__main__':
    fix_file()
