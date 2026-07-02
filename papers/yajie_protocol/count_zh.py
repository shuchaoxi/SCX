import re

with open('main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Count [ZH] instances
zh_count = content.count('[ZH]')
print(f'Total [ZH] instances: {zh_count}')

# Find Chinese chars
cn = re.findall(r'[\u4e00-\u9fff]+', content)
print(f'Chinese text segments: {len(cn)}')
if cn[:10]:
    for c in cn[:10]:
        s = f'  "{c[:80]}..."' if len(c) > 80 else f'  "{c}"'
        print(s)
