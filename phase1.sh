#!/bin/bash
# Phase 1: Structural changes for ALL 8 files
cd /f/scx

for f in \
  papers/scx_industry/main.tex \
  papers/scx_information_theory/main.tex \
  papers/scx_instanton/audit_instanton.tex \
  papers/scx_journalism/main.tex \
  papers/scx_lambda/lambda_gauge.tex \
  papers/scx_law/main.tex \
  papers/scx_maintainer_analysis/maintainer_analysis.tex \
  papers/scx_matrix_theory/main.tex; do
  
  echo "=== Structuring $f ==="
  
  # 1. ctexart -> article
  sed -i 's/\\documentclass\[.*\]{ctexart}/\\documentclass[12pt,a4paper]{article}/g' "$f"
  
  # 2. Remove ctex package
  sed -i '/\\usepackage\[UTF8\]{ctex}/d' "$f"
  sed -i '/\\usepackage{ctex}/d' "$f"
  
  # 3. Remove xeCJK
  sed -i '/\\usepackage{xeCJK}/d' "$f"
  
  # 4. Remove CJK font settings  
  sed -i '/\\setCJKmainfont{/d' "$f"
  sed -i '/\\setmainfont{/d' "$f"
  
  # 5. \mathsf -> \textsf (ONLY in command definitions and usage, not in package names)
  sed -i 's/\\newcommand{\\Yajie}{\\mathsf{Yajie}}/\\newcommand{\\Yajie}{\\textsf{Yajie}}/g' "$f"
  sed -i 's/\\newcommand{\\Spring}{\\mathsf{Spring}}/\\newcommand{\\Spring}{\\textsf{Spring}}/g' "$f"
  sed -i 's/\\newcommand{\\Situs}{\\mathsf{Situs}}/\\newcommand{\\Situs}{\\textsf{Situs}}/g' "$f"
  sed -i 's/\\newcommand{\\Cercis}{\\mathsf{Cercis}}/\\newcommand{\\Cercis}{\\textsf{Cercis}}/g' "$f"
  sed -i 's/\\newcommand{\\SCX}{\\mathsf{SCX}}/\\newcommand{\\SCX}{\\textsf{SCX}}/g' "$f"
  sed -i 's/\\renewcommand{\\SCX}{\\mathsf{SCX}}/\\renewcommand{\\SCX}{\\textsf{SCX}}/g' "$f"
  
  # 6. Fix theorem names - direct Chinese -> English replacement
  sed -i 's/{定理}/{Theorem}/g' "$f"
  sed -i 's/{引理}/{Lemma}/g' "$f"
  sed -i 's/{推论}/{Corollary}/g' "$f"
  sed -i 's/{定义}/{Definition}/g' "$f"
  sed -i 's/{注记}/{Remark}/g' "$f"
  sed -i 's/{猜想}/{Conjecture}/g' "$f"
  sed -i 's/{例}/{Example}/g' "$f"
  sed -i 's/{命题}/{Proposition}/g' "$f"
  sed -i 's/{假设}/{Assumption}/g' "$f"
  sed -i 's/{判据}/{Criterion}/g' "$f"
  
  # 7. Fix \author -> SCX (if not already SCX)
  if ! grep -q '\\author{SCX}' "$f"; then
    # Multi-line author blocks
    perl -i -0777 -pe 's/\\author\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}/\\author{SCX}/gs' "$f"
  fi
  
  echo "  Structured: $f"
done

echo "=== Phase 1 complete ==="
