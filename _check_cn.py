import subprocess, re

files = [
    'papers/scx_acad_mdta_ilh/main.tex',
    'papers/scx_agentic_audit/main.tex',
    'papers/scx_art/art_gauge.tex',
    'papers/scx_audit_economics/audit_economics.tex',
    'papers/scx_business/business_gauge.tex',
    'papers/scx_capstone/auditability_principle.tex',
    'papers/scx_causal_consensus/main.tex',
    'papers/scx_civilization/civ_gauge.tex',
    'papers/scx_collective_intelligence/main.tex',
]

cn = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')

for f in files:
    # HEAD
    with open(f, 'r', encoding='utf-8') as fh:
        head_cn = sum(1 for l in fh if cn.search(l))
    # 23c25e5
    result = subprocess.run(['git', 'show', f'23c25e5:{f}'], capture_output=True, text=True)
    prev_cn = sum(1 for l in result.stdout.split('\n') if cn.search(l))
    delta = head_cn - prev_cn
    print(f'{f}: HEAD={head_cn}, v23c25e5={prev_cn}, delta={delta:+d}')
