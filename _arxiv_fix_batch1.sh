#!/bin/bash
# arXiv Batch 1 fixes — apply to all papers/*.tex files
# Excluding supplementary/history archives

set -e

FILES=$(find papers -name '*.tex' ! -path '*/supplementary/*' ! -path '*/archive/*' ! -path '*/_*/*' ! -path '*/docs/*' | sort)

count=0
for f in $FILES; do
    echo "=== Processing: $f ==="
    
    # 1. Add \pdfoutput=1 as first line if not already present
    if ! head -1 "$f" | grep -q '\\pdfoutput=1'; then
        # Insert \pdfoutput=1 as line 1
        sed -i '1i\\\pdfoutput=1' "$f"
        echo "  + Added \\pdfoutput=1"
    else
        echo "  - \\pdfoutput=1 already present"
    fi
    
    # 2. Remove \usepackage[utf8]{inputenc}
    if grep -q '\\usepackage\[utf8\]{inputenc}' "$f"; then
        sed -i '/\\usepackage\[utf8\]{inputenc}/d' "$f"
        echo "  - Removed \\usepackage[utf8]{inputenc}"
    fi
    
    # 2b. Remove \usepackage[utf8x]{inputenc}
    if grep -q '\\usepackage\[utf8x\]{inputenc}' "$f"; then
        sed -i '/\\usepackage\[utf8x\]{inputenc}/d' "$f"
        echo "  - Removed \\usepackage[utf8x]{inputenc}"
    fi
    
    # 3. Remove \usepackage{physics}
    if grep -q '\\usepackage{physics}' "$f"; then
        sed -i '/\\usepackage{physics}/d' "$f"
        echo "  - Removed \\usepackage{physics}"
    fi
    
    # 4. Remove linkcolor=blue, from hyperref
    if grep -q 'linkcolor=blue' "$f"; then
        sed -i 's/linkcolor=blue,\s*//g' "$f"
        sed -i 's/,\s*linkcolor=blue//g' "$f"
        sed -i 's/linkcolor=blue//g' "$f"
        echo "  - Removed linkcolor=blue"
    fi
    
    # 5. Change \documentclass[...]{ctexart} to \documentclass[...]{article}
    if grep -q 'ctexart' "$f"; then
        sed -i 's/{ctexart}/{article}/g' "$f"
        echo "  - Changed ctexart → article"
    fi
    
    # 6. Remove ctex/fontspec/xeCJK/CJK related packages
    for pkg in ctex fontspec xeCJK CJK CJKutf8 zhnumber; do
        if grep -q "\\\\usepackage.*{$pkg}" "$f" 2>/dev/null; then
            sed -i "/\\\\usepackage.*{$pkg}/d" "$f"
            echo "  - Removed \\usepackage{$pkg}"
        fi
    done
    
    count=$((count + 1))
done

echo ""
echo "Total files processed: $count"
