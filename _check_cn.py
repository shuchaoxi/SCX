import re, os

fpath = 'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex'
with open(fpath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cn_lines = []
for i, line in enumerate(lines):
    if re.search(r'[\u4e00-\u9fff]', line):
        cn_lines.append((i+1, line.rstrip()[:150]))

for ln, text in cn_lines:
    print(f"L{ln}: {text}")
