"""
Convert fullwidth Chinese punctuation to ASCII equivalents in LaTeX files.
Also fixes common artifacts.
"""
import re

FILES = [
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

# Fullwidth → ASCII mapping
FW_MAP = {
    '\uff08': '(',   # （
    '\uff09': ')',   # ）
    '\uff3b': '[',   # 【 → [
    '\uff3d': ']',   # 】 → ]
    '\uff0c': ',',   # ，
    '\u3001': ',',   # 、
    '\uff0e': '.',   # ．
    '\u3002': '.',   # 。
    '\uff1a': ':',   # ：
    '\uff1b': ';',   # ；
    '\uff1f': '?',   # ？
    '\uff01': '!',   # ！
    '\uff5e': '~',   # ～
    '\uff5b': '{',   # ｛
    '\uff5d': '}',   # ｝
    '\uff1c': '<',   # ＜
    '\uff1e': '>',   # ＞
    '\u300a': '<',   # 《
    '\u300b': '>',   # 》
    '\u300c': '"',   # 「
    '\u300d': '"',   # 」
    '\u300e': "'",   # 『
    '\u300f': "'",   # 』
    '\uff0f': '/',   # ／
    '\uff04': '$',   # ＄
    '\uff05': '%',   # ％
    '\uff03': '#',   # ＃
    '\uff06': '&',   # ＆
    '\uff0a': '*',   # ＊
    '\uff0b': '+',   # ＋
    '\uff0d': '-',   # －
    '\uff1d': '=',   # ＝
    '\uff20': '@',   # ＠
    '\uff3e': '^',   # ＾
    '\uff3c': '\\',  # ＼
    '\uff5c': '|',   # ｜
    '\u2018': "'",   # '
    '\u2019': "'",   # '
    '\u201c': '"',   # "
    '\u201d': '"',   # "
    '\u2026': '...', # …
}

def fix_line(line):
    """Fix a line by converting fullwidth chars and cleaning up."""
    # Convert fullwidth characters
    for fw, ascii in FW_MAP.items():
        line = line.replace(fw, ascii)
    
    # Fix common artifacts after conversion
    # Multiple spaces
    line = re.sub(r'  +', ' ', line)
    # Space before period
    line = re.sub(r' \.', '.', line)
    # Space before comma
    line = re.sub(r' ,', ',', line)
    # Space before closing paren
    line = re.sub(r' \)', ')', line)
    # Opening paren with space after
    line = re.sub(r'\( ', '(', line)
    # Triple em-dash → real em-dash
    line = line.replace('---', '—')
    
    return line

for filepath in FILES:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = [fix_line(l) for l in lines]
    fixed = '\n'.join(fixed_lines)
    
    # Count changes
    changes = sum(1 for a, b in zip(content, fixed) if a != b)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    print(f'{filepath}: {changes} char changes')

print('Done!')
