import re
with open('main_orig.tex', encoding='utf-8') as f:
    content = f.read()
cn = re.findall(r'[\u4e00-\u9fff]', content)
print(f'Chinese characters: {len(cn)}')
lines_with_cn = 0
for i, line in enumerate(content.split('\n'), 1):
    if re.search(r'[\u4e00-\u9fff]', line):
        lines_with_cn += 1
print(f'Lines with Chinese: {lines_with_cn}')
