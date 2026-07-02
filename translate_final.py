#!/usr/bin/env python3
"""Final pass: replace any remaining individual Chinese characters."""
import os

char_map = {
    '后': 'after', '新': 're-', '重': 're-', '工': 'work', '作': '',
    '泛': 'functional', '函': '', '跨': 'cross-', '架': 'architecture', 
    '创': 'contribut', '制': 'enforc', '认': 'certifi', '估': 'estimat',
    '码': 'code', '应': 'correspond', '之': 'whether', '仲': 'arbitrat',
    '裁': 'ion', '发': 'occur', '生': '', '次': 'layer', '访': 'access',
    '且': 'and', '分': 'respectively', '别': '', '情': 'situation',
    '越': 'the more ', '坚': 'solid', '固': '', '势': 'advantage',
    '开': 'open', '享': 'shar', '资': 'resource', '对': 'commut',
    '易': 'ity', '动': 'disturb', '息': 'e', '添': 'add', '散': 'divergence',
    '输': 'output', '询': 'quer', '全': 'full', '操': 'operate', '盖': 'cover',
    '忽': 'ignor', '版': 'version', '衡': 'balanc', '抵': 'cancel',
    '亚': 'sub-', '剩': 'remain', '李': 'Lie', '彼': 'mutual', '交': 'commut',
    '耦': 'coupl', '紧': 'tight', '先': 'previous', '估': 'estimat',
    '净': 'net', '收': 'receive', '负': 'negative', '氮': 'nitrogen',
    '强': 'strong', '烈': 'ly', '弛': 'relaxat', '豫': 'ion',
    '释': 'releas', '辨': 'resolv', '衡': 'tradeoff',
    '固' : 'intrinsically', '脯': 'proline', '滑': 'smooth', '零': 'zero',
    '膨': 'inflat', '胀': 'ion', '读': 'read', '困': 'confus',
    '惑': 'ion', '章': 'chapter', '节': '', '随': 'with',
    '弃': 'discard', '忘': 'forget', '早': 'early', '待': 'wait',
    '拒': 'reject', '绝': '', '访': 'revisit', '续': 'subsequen',
    '活': 'resurre', '灾': 'catastrophi', '替': 'replac',
    '旧': 'old', '游': 'game', '辍': 'stop', '虽': 'although',
    '朝': 'toward',
}

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for ch, en in char_map.items():
        content = content.replace(ch, en)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

files = [
    'theory/propositions/05_expert_governance_protocol.tex',
    'theory/SCX_Undiscovered_Theorems.tex',
    'theory/self_evolution/MATHEMATICAL_GENEALOGY.tex',
    'theory/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex',
    'theory/self_evolution/ppe_rigorous_derivation.tex',
    'theory/self_evolution/situs_final_verification.tex',
    'theory/self_evolution/situs_physical_validation.tex',
]

for f in files:
    path = os.path.join('F:/scx', f)
    if os.path.exists(path):
        changed = fix_file(path)
        with open(path, 'r', encoding='utf-8') as fh:
            cnt = sum(1 for c in fh.read() if '\u4e00' <= c <= '\u9fff')
        print(f'{f}: {"FIXED" if changed else "UNCHANGED"}, {cnt} Chinese chars remain')
