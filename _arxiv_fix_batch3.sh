#!/bin/bash
# arXiv fixes Batch 3 — mechanical fixes for all .tex files under papers/
set -e

FIX_LOG="/f/scx/_arxiv_fix_log.txt"
> "$FIX_LOG"

fix_count=0
total=0

# Find all .tex files under papers/
while IFS= read -r -d '' f; do
    total=$((total + 1))
    modified=false
    
    # Read the file
    content=$(cat "$f")
    original="$content"
    
    # Fix 1: Add \pdfoutput=1 before \documentclass (if not already there)
    if ! echo "$content" | head -5 | grep -q '\\pdfoutput=1'; then
        content=$(echo "$content" | sed '1s/^/\\pdfoutput=1\n/')
        modified=true
    fi
    
    # Fix 2: Remove \usepackage[utf8]{inputenc}
    if echo "$content" | grep -q '\\usepackage\[utf8\]{inputenc}'; then
        content=$(echo "$content" | sed '/\\usepackage\[utf8\]{inputenc}/d')
        modified=true
    fi
    # Remove \usepackage{inputenc}
    if echo "$content" | grep -q '\\usepackage{inputenc}'; then
        content=$(echo "$content" | sed '/\\usepackage{inputenc}/d')
        modified=true
    fi
    
    # Fix 3: Remove \usepackage{physics}
    if echo "$content" | grep -q '\\usepackage{physics}'; then
        content=$(echo "$content" | sed '/\\usepackage{physics}/d')
        modified=true
    fi
    
    # Fix 4: Remove linkcolor=blue, from hyperref options
    if echo "$content" | grep -q 'linkcolor'; then
        content=$(echo "$content" | sed 's/linkcolor=blue,\s*//g')
        content=$(echo "$content" | sed 's/,\s*linkcolor=blue//g')
        content=$(echo "$content" | sed 's/linkcolor=blue//g')
        modified=true
    fi
    
    # Fix 5: \documentclass{ctexart} → \documentclass{article}
    if echo "$content" | grep -q 'ctexart'; then
        content=$(echo "$content" | sed 's/\\documentclass{ctexart}/\\documentclass{article}/g')
        content=$(echo "$content" | sed 's/\\documentclass\[\(.*\)\]{ctexart}/\\documentclass[\1]{article}/g')
        # Remove ctex/xeCJK/fontspec/CJK packages
        content=$(echo "$content" | sed '/\\usepackage.*{ctex}/d')
        content=$(echo "$content" | sed '/\\usepackage.*{xeCJK}/d')
        content=$(echo "$content" | sed '/\\usepackage.*{fontspec}/d')
        content=$(echo "$content" | sed '/\\usepackage.*{CJK}/d')
        modified=true
    fi
    
    # Fix 6: \author{...} → \author{SCX}
    if echo "$content" | grep -q '\\author{'; then
        content=$(echo "$content" | sed 's/\\author{[^}]*}/\\author{SCX}/g')
        modified=true
    fi
    
    if $modified; then
        echo "$content" > "$f"
        fix_count=$((fix_count + 1))
        echo "  FIXED: $f" | tee -a "$FIX_LOG"
    fi
done < <(find /f/scx/papers -name "*.tex" -type f -print0)

echo ""
echo "Total: $fix_count files modified out of $total" | tee -a "$FIX_LOG"
echo "Done."
