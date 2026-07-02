import re, os

files = [
    ('papers/scx_acad_mdta_ilh/main.tex', 'acad'),
    ('papers/scx_agentic_audit/main.tex', 'agentic'),
    ('papers/scx_art/art_gauge.tex', 'art'),
    ('papers/scx_audit_economics/audit_economics.tex', 'econ'),
    ('papers/scx_business/business_gauge.tex', 'biz'),
    ('papers/scx_capstone/auditability_principle.tex', 'cap'),
    ('papers/scx_causal_consensus/main.tex', 'causal'),
    ('papers/scx_civilization/civ_gauge.tex', 'civ'),
    ('papers/scx_collective_intelligence/main.tex', 'ci'),
]

cn = re.compile(r'[\u4e00-\u9fff]')
fn = re.compile(r'[\uff00-\uffef\u3000-\u303f]')

for fpath, tag in files:
    with open(fpath, 'r', encoding='utf-8') as fh:
        text = fh.read()
    cn_chars = len(cn.findall(text))
    fn_chars = len(fn.findall(text))
    lines = text.split('\n')
    cn_lines = sum(1 for l in lines if cn.search(l) or fn.search(l))
    print(f'{tag}: {cn_chars} CJK chars, {fn_chars} fullwidth chars, {cn_lines} lines, {len(lines)} total lines')
