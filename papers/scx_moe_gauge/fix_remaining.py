# -*- coding: utf-8 -*-
"""
Fix remaining Chinese text in main.md.
Written to a file so bash doesn't eat our backslashes.
"""
import re

INPUT = r'G:\Xiaogan_Supercomputing_data\SCX\papers\scx_moe_gauge\main.md'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ====== LINES 1-100 ======

# Line 31: Ruler metaphor
old = '- **\xe5\xb0\xba\xe5\xad\x90 = MoE \xe4\xb8\x93\xe5\xae\xb6\xe7\xbd\x91\xe7\xbb\x9c** $E_m$\xe3\x80\x82\xe6\xaf\x8f\xe4\xb8\xaa\xe4\xb8\x93\xe5\xae\xb6\xe5\x8d\x95\xe7\x8b\xac\xe8\xae\xad\xe7\xbb\x83\xef\xbc\x8c\xe5\x9c\xa8\xe8\x87\xaa\xe5\xb7\xb1\xe7\x9a\x84\xe9\xa2\x86\xe5\x9f\x9f\xe9\x87\x8c\xe6\x98\xaf\\"\xe5\x87\x86\xe7\x9a\x84\\"\xef\xbc\x88loss \xe4\xbd\x8e\xef\xbc\x89'
new = '- **Ruler = MoE expert network** $E_m$. Each expert is trained independently and is \\"accurate\\" in its own domain (low loss).'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("Fixed: ruler metaphor line 31")
else:
    print("MISS: ruler metaphor line 31")

# Line 33: Ruler metaphor continued
old = '- **\xe6\x8b\xbc\xe5\xb0\xba\xe5\xad\x90 = \xe8\xb7\xaf\xe7\x94\xb1\xe5\x99\xa8\xe6\xaf\x94\xe8\xbe\x83\xe4\xb8\x93\xe5\xae\xb6**\xe3\x80\x82\xe8\xb7\xaf\xe7\x94\xb1\xe5\x99\xa8\xe7\x94\xa8\xe4\xb8\x80\xe4\xb8\xaa\xe7\xba\xbf\xe6\x80\xa7\xe5\x87\xbd\xe6\x95\xb0\xe6\xaf\x94\xe8\xbe\x83 8 \xe4\xb8\xaa\xe4\xb8\x93\xe5\xae\xb6\xe7\x9a\x84\\"\xe5\x88\xbb\xe5\xba\xa6\\"\xef\xbc\x8c\xe4\xbd\x86\xe5\xae\x83\xe4\xb8\x8d\xe7\x9f\xa5\xe9\x81\x93\xe6\xaf\x8f\xe4\xb8\xaa\xe4\xb8\x93\xe5\xae\xb6\xe7\x9a\x84\xe9\x9b\xb6\xe5\x88\xbb\xe5\xba\xa6\xe5\x9c\xa8\xe5\x93\xaa'
new = '- **Piecing rulers = router comparing experts**. The router uses a linear function to compare the \\"markings\\" of 8 experts, but it does not know where each expert\'s zero mark is.'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("Fixed: ruler metaphor line 33")
else:
    print("MISS: ruler metaphor line 33")

# Now let's use a different approach - find all Chinese text and show it
cjk = re.compile(r'[一-鿿]+')
# Find all lines with Chinese
lines = content.split('\n')
cn_lines = []
for i, line in enumerate(lines):
    if cjk.search(line):
        cn_lines.append((i+1, line))

print(f"\nTotal lines with Chinese remaining: {len(cn_lines)}")
for num, line in cn_lines[:20]:
    print(f"  L{num}: {line[:100]}")

with open(INPUT, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"\nApplied {changes} changes")
