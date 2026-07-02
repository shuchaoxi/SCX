import re
from collections import Counter

with open('papers/scx_acad_mdta_ilh/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

non_ascii = re.findall(r'[^\x00-\x7f]', text)
ranges = Counter()
for c in non_ascii:
    cp = ord(c)
    if 0x4e00 <= cp <= 0x9fff: ranges['CJK Unified'] += 1
    elif 0x3400 <= cp <= 0x4dbf: ranges['CJK Ext A'] += 1
    elif 0xf900 <= cp <= 0xfaff: ranges['CJK Compat'] += 1
    elif 0xff00 <= cp <= 0xffef: ranges['Fullwidth'] += 1
    elif 0x3000 <= cp <= 0x303f: ranges['CJK Punct'] += 1
    elif 0x2000 <= cp <= 0x206f: ranges['General Punct'] += 1
    elif cp == 0x2014: ranges['Em Dash'] += 1
    else: ranges[f'U+{cp:04X}'] += 1

for k, v in ranges.most_common(15):
    print(f'{k}: {v}')
print(f'Total non-ASCII: {len(non_ascii)}')

# Show a sample of what fullwidth chars look like
fw = [c for c in non_ascii if 0xff00 <= ord(c) <= 0xffef]
print(f'\nSample fullwidth chars (first 30): {"".join(fw[:30])}')
print(f'Sample fullwidth chars Unicode: {[f"U+{ord(c):04X}" for c in fw[:10]]}')
