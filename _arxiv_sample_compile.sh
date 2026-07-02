#!/bin/bash
# Targeted compile test — representative sample of fixed files
export PATH="/c/Users/shuchaoxi/AppData/Local/Programs/MiKTeX/miktex/bin/x64:$PATH"

cd /f/scx

# Test files covering all fix types
FILES=(
    # ctexart→article + physics + linkcolor
    "papers/scx_moe_gauge/main.tex"
    "papers/scx_monte_carlo/main.tex"
    "papers/scx_open_problems/main.tex"
    "papers/scx_peer_review/peer_gauge.tex"
    "papers/scx_phase_field/main.tex"
    "papers/scx_prize/scx_prize.tex"
    "papers/scx_protocol_governance/protocol_governance.tex"
    "papers/scx_resistance/resistance_paradox.tex"
    "papers/scx_singularity/singularity_theory.tex"
    # ctexart→article only
    "papers/scx_ml_audit/main.tex"
    "papers/scx_ml_history/main.tex"
    "papers/scx_ml_verdict/main.tex"
    "papers/scx_hardware/ultimate.tex"
    "papers/scx_ip_note/main.tex"
    # physics + linkcolor (non-ctexart)
    "papers/scx_gauge_formalized/gauge_formalized.tex"
    "papers/scx_gauge_physics/gauge_physics.tex"
    "papers/scx_hamiltonian_audit/main.tex"
    "papers/scx_maintainer_analysis/maintainer_analysis.tex"
    "papers/scx_unified_field/main.tex"
    # physics only
    "papers/scx_acad_mdta_ilh/main.tex"
    "papers/scx_grand_unification/grand_unification.tex"
    "papers/scx_hamiltonian/scx_hamiltonian.tex"
    # inputenc removal
    "papers/scx_audit_sword/main.tex"
    "papers/scx_review/main.tex"
    "papers/scx_economics/main.tex"
    # fontspec/xeCJK removal  
    "papers/scx_genomics/main.tex"
    "papers/scx_nv_center/main.tex"
    "papers/scx_parenting/parent_gauge.tex"
    # plain (just pdfoutput)
    "papers/scx_climate/main.tex"
    "papers/scx_alignment/main.tex"
    "papers/scx_blockchain/main.tex"
    "papers/scx_community/main.tex"
    "papers/scx_complexity/main.tex"
    "papers/scx_consciousness/main.tex"
    "papers/scx_hallucination/main.tex"
    "papers/scx_information_theory/main.tex"
    "papers/scx_kappa_suppression/main.tex"
    "papers/scx_law/main.tex"
    "papers/scx_matrix_theory/main.tex"
    "papers/scx_meta_audit/meta_audit.tex"
)

PASS=0
FAIL=0
FAIL_LIST=""

for f in "${FILES[@]}"; do
    dir=$(dirname "$f")
    base=$(basename "$f")
    name="${base%.tex}"
    
    if [ ! -f "$f" ]; then
        echo "MISSING: $f"
        continue
    fi
    
    pushd "$dir" > /dev/null
    if pdflatex -interaction=nonstopmode "$base" > /dev/null 2>&1; then
        echo "✅ $f"
        PASS=$((PASS + 1))
        # Clean up
        rm -f "$name.aux" "$name.log" "$name.out" "$name.pdf" 2>/dev/null
    else
        echo "❌ $f"
        FAIL=$((FAIL + 1))
        FAIL_LIST="$FAIL_LIST $f"
        # Keep log for debugging
    fi
    popd > /dev/null
done

echo ""
echo "========== RESULTS =========="
echo "Pass: $PASS / $((PASS + FAIL))"
echo "Fail: $FAIL"
if [ $FAIL -gt 0 ]; then
    echo "Failed:$FAIL_LIST"
fi
