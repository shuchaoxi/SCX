#!/bin/bash
# Clean up orphaned fontspec/xeCJK commands after ctex removal

FILES="papers/scx_art/art_gauge.tex
papers/scx_audit_economics/audit_economics.tex
papers/scx_business/business_gauge.tex
papers/scx_collective_intelligence/main.tex
papers/scx_company_valuation/company_valuation.tex
papers/scx_environment/env_gauge.tex
papers/scx_genomics/main.tex
papers/scx_nv_center/main.tex
papers/scx_parenting/parent_gauge.tex
papers/scx_philosophy_education/main.tex
papers/scx_philosophy_law/main.tex
papers/scx_philosophy_science/main.tex
papers/scx_protocol_governance/protocol_governance.tex
papers/scx_pseudopotential/main.tex
papers/scx_social_media/social_gauge.tex
papers/scx_temporal/main.tex
papers/scx_world_government/world_government.tex
papers/scx_world_model/main.tex"

for f in $FILES; do
    echo "=== Processing: $f ==="
    # Remove \setCJKmainfont, \setmainfont, \setCJKsansfont, \setsansfont, etc.
    sed -i '/\\setCJKmainfont/d' "$f"
    sed -i '/\\setCJKsansfont/d' "$f"
    sed -i '/\\setCJKmonofont/d' "$f"
    sed -i '/\\setmainfont/d' "$f"
    sed -i '/\\setsansfont/d' "$f"
    sed -i '/\\setmonofont/d' "$f"
    # Remove xeCJK specific options from \documentclass if any
    sed -i 's/,CJKmath=true//g' "$f"
    echo "  Cleaned fontspec/xeCJK commands"
done

echo "Done!"
