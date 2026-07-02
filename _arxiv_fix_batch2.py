#!/usr/bin/env python3
"""arXiv fixes Batch 2 — mechanical fixes for 60 .tex files"""
import os, re, sys

FILES = [
    "papers/scx_prize/scx_prize.tex",
    "papers/scx_protocol_governance/protocol_governance.tex",
    "papers/scx_pseudopotential/main.tex",
    "papers/scx_qg_audit/main.tex",
    "papers/scx_quant_finance/main.tex",
    "papers/scx_quantum/main.tex",
    "papers/scx_quantum_audit/quantum_audit.tex",
    "papers/scx_resistance/resistance_paradox.tex",
    "papers/scx_review/main.tex",
    "papers/scx_review/supp.tex",
    "papers/scx_S_operator/S_operator.tex",
    "papers/scx_science_audit/main.tex",
    "papers/scx_security/main.tex",
    "papers/scx_singularity/singularity_theory.tex",
    "papers/scx_social_media/social_gauge.tex",
    "papers/scx_spring_framework/spring_framework.tex",
    "papers/scx_spring_limits/spring_limits.tex",
    "papers/scx_spring_md/spring_md.tex",
    "papers/scx_spring_trainer/spring_trainer.tex",
    "papers/scx_string_unified/main.tex",
    "papers/scx_supplementary_docs/main.tex",
    "papers/scx_supply_chain/main.tex",
    "papers/scx_temporal/main.tex",
    "papers/scx_theory/main.tex",
    "papers/scx_theory/S1_thm1_noise_detection.tex",
    "papers/scx_theory/S2_thm2_weak_features.tex",
    "papers/scx_theory/S3_thm3_unidentifiability.tex",
    "papers/scx_theory/S4_thm4_exact_constant_minimax.tex",
    "papers/scx_theory/S5_thm5_cluster_consistency.tex",
    "papers/scx_theory/S6_prop6_bootstrap_stability.tex",
    "papers/scx_theory/S7_experimental_details.tex",
    "papers/scx_theory/S8_numerical_verification.tex",
    "papers/scx_turbulence/main.tex",
    "papers/scx_turbulence_moduli/main.tex",
    "papers/scx_turbulence_moduli/main_staged.tex",
    "papers/scx_unified_field/main.tex",
    "papers/scx_world_government/world_government.tex",
    "papers/scx_world_model/main.tex",
    "papers/situs_applications/main.tex",
    "papers/situs_theory/main.tex",
    "papers/spring_config/main.tex",
    "papers/taxonomic_nn/main.tex",
    "papers/taxonomic_nn/theorem3.tex",
    "papers/taxonomic_nn/theorem3_short.tex",
    "papers/theorems/theorem_2_weak_feature.tex",
    "papers/theorems/theorem_aa_alignment.tex",
    "papers/theorems/theorem_ac_complexity.tex",
    "papers/theorems/theorem_ae_entropy.tex",
    "papers/theorems/theorem_ar_adversarial.tex",
    "papers/theorems/theorem_cd_causal.tex",
    "papers/theorems/theorem_fa_federated.tex",
    "papers/theorems/theorem_hc_human.tex",
    "papers/theorems/theorem_q_quantum.tex",
    "papers/theorems/theorem_ra_recursive.tex",
    "papers/theorems/theorem_ts_temporal.tex",
    "papers/theorems/theorem5_active_learning.tex",
    "papers/theorems/theorem6_protocol_game.tex",
    "papers/theorems/theorem7_cross_domain.tex",
    "papers/yajie_protocol/human_future.tex",
    "papers/yajie_protocol/main.tex",
]

# Physics package replacements
PHYSICS_REPLACEMENTS = [
    (re.compile(r'\\dv\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{d \1}{d \2}'),
    (re.compile(r'\\dv\*\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{d \1}{d \2}'),
    (re.compile(r'\\pdv\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{\\partial \1}{\\partial \2}'),
    (re.compile(r'\\pdv\*\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{\\partial \1}{\\partial \2}'),
    (re.compile(r'\\abs\s*\{([^}]+)\}'), r'\\left|\1\\right|'),
    (re.compile(r'\\norm\s*\{([^}]+)\}'), r'\\left\\|\1\\right\\|'),
    (re.compile(r'\\ket\s*\{([^}]+)\}'), r'|\1\\rangle'),
    (re.compile(r'\\bra\s*\{([^}]+)\}'), r'\\langle \1|'),
    (re.compile(r'\\braket\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\langle \1 | \2 \\rangle'),
]

def apply_physics_replacements(content):
    for pattern, replacement in PHYSICS_REPLACEMENTS:
        content = pattern.sub(replacement, content)
    return content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content
    modified = False
    fix_reasons = []

    # Fix 1: Add \pdfoutput=1 as first line (before \documentclass)
    if not content.lstrip().startswith('\\pdfoutput=1'):
        m = re.search(r'(\\documentclass)', content)
        if m:
            idx = m.start()
            line_start = content.rfind('\n', 0, idx)
            if line_start == -1:
                # \documentclass is on first line, prepend
                content = '\\pdfoutput=1\n' + content
            else:
                content = content[:line_start] + '\n\\pdfoutput=1\n' + content[line_start:]
            modified = True
            fix_reasons.append('pdfoutput=1')

    # Fix 2: Remove \usepackage[utf8]{inputenc}
    new_content = re.sub(r'\\usepackage\[utf8?\]\{inputenc\}\s*\n?', '', content)
    new_content = re.sub(r'\\usepackage\{inputenc\}\s*\n?', '', new_content)
    if new_content != content:
        modified = True
        fix_reasons.append('remove inputenc')
        content = new_content

    # Fix 3: Remove \usepackage{physics} & replace physics commands
    if '\\usepackage{physics}' in content:
        content = apply_physics_replacements(content)
        content = re.sub(r'\\usepackage\{physics\}\s*\n?', '', content)
        modified = True
        fix_reasons.append('remove physics')

    # Fix 4: Remove linkcolor=blue from hyperref options
    new_content = re.sub(r'linkcolor\s*=\s*blue\s*,?\s*', '', content)
    new_content = re.sub(r',?\s*linkcolor\s*=\s*blue', '', new_content)
    if new_content != content:
        modified = True
        fix_reasons.append('remove linkcolor=blue')
        content = new_content

    # Fix 5: \documentclass{ctexart} → \documentclass{article}
    if 'ctexart' in content:
        content = content.replace('\\documentclass{ctexart}', '\\documentclass{article}')
        content = re.sub(r'\\documentclass\[([^\]]*)\]\{ctexart\}', r'\\documentclass[\1]{article}', content)
        modified = True
        fix_reasons.append('ctexart→article')

    # Remove ctex/xeCJK/fontspec/CJK related packages
    cjk_packages = [
        r'\\usepackage(\[[^\]]*\])?\{ctex\}',
        r'\\usepackage(\[[^\]]*\])?\{xeCJK\}',
        r'\\usepackage(\[[^\]]*\])?\{fontspec\}',
        r'\\usepackage(\[[^\]]*\])?\{CJK\}',
        r'\\usepackage(\[[^\]]*\])?\{CJKutf8\}',
        r'\\usepackage(\[[^\]]*\])?\{CJKspace\}',
    ]
    for pkg in cjk_packages:
        new_content = re.sub(pkg + r'\s*\n?', '', content)
        if new_content != content:
            modified = True
            fix_reasons.append('remove CJK/pkg')
            content = new_content

    # Fix 6: \author{...} → \author{SCX}
    new_content = re.sub(r'\\author\{[^}]*\}', r'\\author{SCX}', content)
    if new_content != content:
        modified = True
        fix_reasons.append('author→SCX')
        content = new_content

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return fix_reasons
    return None

if __name__ == '__main__':
    print(f"Processing {len(FILES)} files...\n")
    count = 0
    for f in FILES:
        reasons = fix_file(f)
        if reasons:
            count += 1
            print(f"  FIXED: {f}  [{', '.join(reasons)}]")
        else:
            print(f"  SKIP:  {f}  [no changes needed]")

    print(f"\nTotal: {count} files modified out of {len(FILES)}")
