#!/usr/bin/env python3
"""
Mechanical LaTeX-to-Markdown cleanup for scx_moe_gauge/main.md.
Only handles command replacements and LaTeX artifact removal, not Chinese translation.
"""

import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'
OUTPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    text = f.read()

original_len = len(text)

# =========================================================
# 1. MATH COMMAND REPLACEMENTS (inside math mode)
# =========================================================
# These appear inside $$...$$ or $...$ in MathJax
math_replacements = [
    (r'\R', r'\mathbb{R}'),
    (r'\N', r'\mathbb{N}'),
    (r'\Pbb', r'\mathbb{P}'),
    (r'\E', r'\mathbb{E}'),
    (r'\D', r'\mathcal{D}'),
    (r'\G', r'\mathcal{G}'),
    (r'\X', r'\mathcal{X}'),
    (r'\F', r'\mathcal{F}'),
    (r'\T', r'\mathcal{T}'),
    (r'\A', r'\mathcal{A}'),
    (r'\loss', r'\mathcal{L}'),
    (r'\topk', r'\text{top-}k'),
    (r'\softmax', r'\text{softmax}'),
    (r'\argmax', r'\arg\max'),
    (r'\argmin', r'\arg\min'),
    (r'\diag', r'\text{diag}'),
    (r'\Tr', r'\text{Tr}'),
    (r'\Cov', r'\text{Cov}'),
    (r'\Var', r'\text{Var}'),
    (r'\supp', r'\text{supp}'),
    (r'\gv', r'\mathbf{g}'),
    (r'\id', r'\text{id}'),
    (r'\Lie', r'\mathfrak{g}'),
]

for old, new in math_replacements:
    text = text.replace(old, new)

# =========================================================
# 2. REMOVE LaTeX ENVIRONMENTS AND ARTIFACTS
# =========================================================

# Remove environment begin/end tags
remove_envs = [
    'assumption_env', 'algorithm', 'algorithmic',
    'keyeq', 'flushright', 'compactenum',
    'thebibliography',
]
for env in remove_envs:
    text = re.sub(r'\\begin\{' + env + r'\}(\[.*?\])?', '', text)
    text = re.sub(r'\\end\{' + env + r'\}', '', text)

# Remove \addcontentsline
text = re.sub(r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}', '', text)

# Remove \rigorFull
text = text.replace(r'\rigorFull', '')

# Remove \fbox{ and ]}  (handle simple cases)
text = re.sub(r'\\fbox\s*\{', '', text)
text = re.sub(r'\\fbox\s*%', '', text)

# Remove minipage
text = re.sub(r'\\begin\{minipage\}\{[^}]*\}', '', text)
text = text.replace(r'\end{minipage}', '')

# Remove standalone closing braces (from fbox/minipage)
text = re.sub(r'^\s*\}\s*$', '', text, flags=re.MULTILINE)

# Remove \Caption
text = re.sub(r'\\Caption\{([^}]*)\}', r'**\1**', text)

# Remove \Require, \Ensure from algorithmic
text = text.replace(r'\Require ', '**Require:** ')
text = text.replace(r'\Ensure ', '**Ensure:** ')
text = text.replace(r'\State ', '- ')
text = text.replace(r'\Return ', '**Return:** ')
text = text.replace(r'\Comment{', '(')
text = text.replace(r'}', ')', 1)  # Try to close the comment - approximate

# Remove \resizebox
text = re.sub(r'\\resizebox\{[^}]*\}\{[^}]*\}\{', '', text)

# Remove \newcommand
text = re.sub(r'\\newcommand\{[^}]*\}\{[^}]*\}', '', text)

# Remove \tikzcd (if present)
text = re.sub(r'\\tikzcd\{[^}]*\}', '', text)

# Remove \rule
text = re.sub(r'\\rule\{[^}]*\}\{[^}]*\}', '', text)

# Convert \bibitem to markdown list item
text = re.sub(r'\\bibitem\{([^}]*)\}', r'- \1', text)

# Remove \textbf and \textit (keep content with markdown equivalents)
text = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', text)
text = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', text)

# Convert \item inside compactenum to numbered items
text = re.sub(r'\\item ', r'1. ', text)

# =========================================================
# 3. CLEAN UP
# =========================================================

# Remove lines that are just whitespace after cleanups
text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)

# Collapse multiple blank lines
text = re.sub(r'\n{3,}', '\n\n', text)

# Fix HTML comments
text = re.sub(r'<!--\s*label:\s*([^>]+)\s*-->', r'<!-- \1 -->', text)

# Remove trailing whitespace on each line
lines = [line.rstrip() for line in text.split('\n')]
text = '\n'.join(lines)

print(f"Original length: {original_len}")
print(f"Final length: {len(text)}")
print(f"Lines: {len(lines)}")

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(text)

print("Mechanical cleanup done!")
