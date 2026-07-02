#!/usr/bin/env python
"""Mechanical fixes for Batch A: macros, theorem names, author."""
import re
import os

FILES = [
    "papers/egp_merging/main.tex",
    "papers/meta/SCX_HISTORY.tex",
    "papers/meta/SCX_HISTORY_v2.tex",
    "papers/meta/SCX_MANIFESTO.tex",
    "papers/scx_acad_mdta_ilh/main.tex",
    "papers/scx_agentic_audit/main.tex",
    "papers/scx_art/art_gauge.tex",
    "papers/scx_astronomy/main.tex",
    "papers/scx_audit_economics/audit_economics.tex",
    "papers/scx_audit_sword/main.tex",
    "papers/scx_blockchain/main.tex",
    "papers/scx_business/business_gauge.tex",
    "papers/scx_business_architecture/main.tex",
    "papers/scx_capstone/auditability_principle.tex",
    "papers/scx_causal_consensus/main.tex",
    "papers/scx_cfd/main.tex",
    "papers/scx_civilization/civ_gauge.tex",
    "papers/scx_claude_meta/main.tex",
    "papers/scx_clean_room/main.tex",
    "papers/scx_climate/main.tex",
    "papers/scx_collective_intelligence/main.tex",
    "papers/scx_community/main.tex",
    "papers/scx_compactness/main.tex",
    "papers/scx_company_valuation/company_valuation.tex",
    "papers/scx_dev_log/main.tex",
    "papers/scx_distillation_hallucination/main.tex",
    "papers/scx_education/edu_gauge.tex",
    "papers/scx_education/main.tex",
    "papers/scx_elections/main.tex",
    "papers/scx_environment/env_gauge.tex",
    "papers/scx_galois/main.tex",
    "papers/scx_galois_falsifiability/main.tex",
    "papers/scx_genomics/main.tex",
    "papers/scx_geopolitics/main.tex",
    "papers/scx_goodhart/goodhart_gauge.tex",
    "papers/scx_governance/main.tex",
    "papers/scx_grand_unification/grand_unification.tex",
    "papers/scx_hamiltonian/scx_hamiltonian.tex",
    "papers/scx_hamiltonian_audit/main.tex",
    "papers/scx_hardware/checklist.tex",
    "papers/scx_hardware/spec.tex",
    "papers/scx_hardware/ultimate.tex",
    "papers/scx_industry/main.tex",
    "papers/scx_information_theory/main.tex",
    "papers/scx_instanton/audit_instanton.tex",
    "papers/scx_ip_note/main.tex",
    "papers/scx_journalism/main.tex",
    "papers/scx_lambda/lambda_gauge.tex",
    "papers/scx_law/main.tex",
    "papers/scx_llm/llm_todo.tex",
    "papers/scx_maintainer_analysis/maintainer_analysis.tex",
    "papers/scx_matrix_theory/main.tex",
    "papers/scx_medicine/main.tex",
    "papers/scx_medicine/med_gauge.tex",
    "papers/scx_meta_audit/meta_audit.tex",
    "papers/scx_ml_audit/main.tex",
    "papers/scx_ml_history/main.tex",
]

# Theorem environment name replacements
THEOREM_MAP = {
    '定理': 'Theorem',
    '引理': 'Lemma',
    '推论': 'Corollary',
    '定义': 'Definition',
    '注记': 'Remark',
    '证明': 'Proof',
    '假设': 'Assumption',
    '命题': 'Proposition',
    '例子': 'Example',
    '问题': 'Problem',
    '猜想': 'Conjecture',
    '公理': 'Axiom',
    '练习': 'Exercise',
    '注': 'Note',
}

# Math macro fixes
MACRO_FIXES = [
    (r'\\mathsf\{SCX\}', r'\\textsf{SCX}'),
    (r'\\mathsf\{Yajie\}', r'\\textsf{Yajie}'),
    (r'\\mathsf\{Cercis\}', r'\\textsf{Cercis}'),
    (r'\\mathsf\{Spring\}', r'\\textsf{Spring}'),
    (r'\\mathsf\{Hermes\}', r'\\textsf{Hermes}'),
    (r'\\mathsf\{Situs\}', r'\\textsf{Situs}'),
    (r'\\mathsf\{scx\}', r'\\textsf{scx}'),
]

base_dir = r"F:\scx"

for relpath in FILES:
    fpath = os.path.join(base_dir, relpath)
    if not os.path.exists(fpath):
        print(f"MISSING: {fpath}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changed = False
    
    # Fix \mathsf macros
    for old, new in MACRO_FIXES:
        if old in content:
            content = content.replace(old, new)
            changed = True
    
    # Fix theorem environment names in Chinese contexts
    # In \newtheorem or \begin{...} or text
    for cn, en in THEOREM_MAP.items():
        # Replace in \begin{cn} and \end{cn}
        old_begin = f'\\begin{{{cn}}}'
        new_begin = f'\\begin{{{en}}}'
        if old_begin in content:
            content = content.replace(old_begin, new_begin)
            changed = True
        
        old_end = f'\\end{{{cn}}}'
        new_end = f'\\end{{{en}}}'
        if old_end in content:
            content = content.replace(old_end, new_end)
            changed = True
        
        # Replace in \newtheorem{xxx}{cn}
        old_thm = f'{{{cn}}}'
        new_thm = f'{{{en}}}'
        # Only replace if preceded by \newtheorem
        pattern = re.compile(r'(\\newtheorem\{[^}]*\})' + re.escape(old_thm))
        if pattern.search(content):
            content = pattern.sub(r'\1' + new_thm, content)
            changed = True
    
    # Fix \author - ensure it's \author{SCX}
    content = re.sub(r'\\author\{[^}]*\}', r'\\author{SCX}', content)
    
    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {relpath}")
    else:
        print(f"OK: {relpath}")

print("\nDONE: Mechanical fixes complete.")
