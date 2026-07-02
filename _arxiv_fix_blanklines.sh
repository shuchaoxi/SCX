#!/bin/bash
# Fix blank lines inside hypersetup/hyperref options caused by linkcolor=blue removal

cd /f/scx

# Find files with blank lines right after colorlinks=true,
FILES=$(grep -rln 'colorlinks=true' papers --include='*.tex' | grep -v 'supplementary' | grep -v '\.bak')

for f in $FILES; do
    # Check if the very next line after 'colorlinks=true,' is blank
    # Use awk to process
    awk '
    /colorlinks=true, *$/ {
        print
        # Read next line
        if (getline nextline > 0) {
            if (nextline ~ /^[[:space:]]*$/) {
                # Skip blank line - read the next one instead
                if (getline nextline2 > 0) {
                    print nextline2
                }
            } else {
                print nextline
            }
        }
        next
    }
    { print }
    ' "$f" > "${f}.tmp" && mv "${f}.tmp" "$f"
done

echo "Fixed blank lines after colorlinks=true in all files"
