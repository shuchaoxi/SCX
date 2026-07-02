#!/bin/bash
# Translate common Chinese patterns in SCX LaTeX files
# Targeted replacements, not blind regex

set -e

FILE="$1"
if [ -z "$FILE" ]; then
    echo "Usage: $0 <file.tex>"
    exit 1
fi

TMP="${FILE}.tmp"

# Read file
cp "$FILE" "$TMP"

# ── 1. Remove xeCJK/CJK packages ──
sed -i '/\\usepackage.*xeCJK/d' "$TMP"
sed -i '/\\usepackage.*CJKutf8/d' "$TMP" 
sed -i '/\\usepackage\[UTF8.*\]{ctex}/d' "$TMP"
sed -i '/\\setCJKmainfont/d' "$TMP"
sed -i '/\\setCJKsansfont/d' "$TMP"
sed -i '/\\setCJKmonofont/d' "$TMP"
sed -i '/\\newfontfamily\\cjkfont/d' "$TMP"
sed -i '/\\begin{CJK}/d' "$TMP"
sed -i '/\\end{CJK}/d' "$TMP"

# ── 2. ctexart → article ──
sed -i 's/ctexart/article/g' "$TMP"

# ── 3. \mathsf{SCX} → \textsf{SCX} ──
sed -i 's/\\mathsf{SCX}/\\textsf{SCX}/g' "$TMP"

# ── 4. Common theorem name replacements ──
sed -i 's/{定理}/Theorem/g' "$TMP"
sed -i 's/{引理}/Lemma/g' "$TMP"  
sed -i 's/{推论}/Corollary/g' "$TMP"
sed -i 's/{定义}/Definition/g' "$TMP"
sed -i 's/{注记}/Remark/g' "$TMP"
sed -i 's/{猜想}/Conjecture/g' "$TMP"
sed -i 's/{假设}/Assumption/g' "$TMP"
sed -i 's/{例}/Example/g' "$TMP"
sed -i 's/{原理}/Principle/g' "$TMP"
sed -i 's/{注}/Note/g' "$TMP"

# ── 5. Chinese dates ──
sed -i 's/\([0-9]\{4\}\)年\([0-9]\{1,2\}\)月\([0-9]\{1,2\}\)日/\1-\2-\3/g' "$TMP"
sed -i 's/\([0-9]\{4\}\)年\([0-9]\{1,2\}\)月/\1-\2/g' "$TMP"

# ── 6. Chinese punctuation in body ──
sed -i 's/：/: /g' "$TMP"
sed -i 's/。/./g' "$TMP"
sed -i 's/，/, /g' "$TMP"
sed -i 's/；/; /g' "$TMP"

# ── 7. Remove bilingual section titles - keep English only ──
# Pattern: "Introduction 引言" → "Introduction"
# Pattern: "English / Chinese" → "English"

# ── 8. Fix keywords - remove Chinese translations ──
# Keywords: "SCX auditing, electoral integrity 选举诚信" → "SCX auditing, electoral integrity"

# Move back
mv "$TMP" "$FILE"
echo "Processed: $FILE"
