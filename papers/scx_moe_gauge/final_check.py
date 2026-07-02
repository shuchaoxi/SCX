import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for remaining LaTeX artifacts
artifacts = [
    '\\addcontentsline', '\\fbox{', '\\begin{minipage}', '\\end{minipage}',
    '\\begin{assumption_env}', '\\end{assumption_env}', '\\begin{algorithm}',
    '\\end{algorithm}', '\\Require', '\\Ensure', '\\State', '\\Return',
    '\\Caption', '\\newcommand', '\\resizebox', '\\tikzcd', '\\rule',
    '\\begin{keyeq}', '\\end{keyeq}', '\\begin{flushright}',
    '\\end{flushright}', '\\rigorFull', '\\begin{compactenum}', '\\end{compactenum}',
    '\\begin{thebibliography}', '\\end{thebibliography}',
]

print('Checking for remaining LaTeX artifacts:')
found = False
for art in artifacts:
    count = content.count(art)
    if count > 0:
        print(f'  FOUND ({count}): {art}')
        found = True
if not found:
    print('  None found - ALL CLEAN!')

# Count Chinese lines
cjk = re.compile(r'[一-鿿]+')
lines = content.split('\n')
remaining = [(i+1, l[:100]) for i, l in enumerate(lines) if cjk.search(l)]
print(f'\nRemaining Chinese lines: {len(remaining)}')

# Check for unescaped math commands
math_cmds = ['\\R', '\\N', '\\Pbb', '\\softmax', '\\loss', '\\argmax', '\\argmin', '\\diag', '\\Tr']
print('\nChecking for remaining raw LaTeX commands:')
for cmd in math_cmds:
    count = content.count(cmd)
    if count > 0:
        print(f'  Found {count} occurrences of {cmd}')
print('Check complete')
