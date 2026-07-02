#!/bin/bash
# Batch compile test for arXiv-fixed files
export PATH="/c/Users/shuchaoxi/AppData/Local/Programs/MiKTeX/miktex/bin/x64:$PATH"

cd /f/scx

PASS=0
FAIL=0
SKIP=0
FAIL_FILES=""

for f in $(find papers -name '*.tex' ! -path '*/supplementary/*' ! -path '*/archive/*' | sort); do
    # Skip fragments (no \documentclass)
    if ! grep -q '\\documentclass' "$f"; then
        SKIP=$((SKIP + 1))
        continue
    fi
    
    dir=$(dirname "$f")
    base=$(basename "$f")
    name="${base%.tex}"
    
    pushd "$dir" > /dev/null
    if pdflatex -interaction=nonstopmode "$base" > /dev/null 2>&1; then
        PASS=$((PASS + 1))
        echo "OK: $f"
    else
        FAIL=$((FAIL + 1))
        FAIL_FILES="$FAIL_FILES
  $f"
        echo "FAIL: $f"
    fi
    popd > /dev/null
    
    # Clean up aux files
    rm -f "$dir/$name.aux" "$dir/$name.log" "$dir/$name.out" "$dir/$name.pdf" 2>/dev/null
done

echo ""
echo "========== RESULTS =========="
echo "Pass: $PASS"
echo "Fail: $FAIL"
echo "Skip (fragments): $SKIP"
if [ $FAIL -gt 0 ]; then
    echo "Failed files:$FAIL_FILES"
fi
