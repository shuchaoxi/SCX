import re
with open('world_government.tex', 'r', encoding='utf-8') as f:
    content = f.read()
chinese = re.findall(r'[\u4e00-\u9fff]+', content)
print(f'Chinese groups: {len(chinese)}')
for c in chinese[:15]:
    print(repr(c[:60]))
