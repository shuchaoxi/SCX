import os
os.chdir(r'F:\scx')
for fname in ['papers/scx_goodhart/goodhart_gauge.tex', 'papers/scx_company_valuation/company_valuation.tex', 'papers/scx_capstone/auditability_principle.tex']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    cjk = [c for c in content if '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf']
    print(f'{fname}: {len(cjk)} CJK chars')
    if cjk:
        lines = content.split('\n')
        count = 0
        for i, line in enumerate(lines, 1):
            if any('\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf' for c in line):
                count += 1
                if count <= 8:
                    print(f'  Line {i}: {line[:150]}')
        print(f'  Total lines with CJK: {count}')
