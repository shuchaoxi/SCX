#!/usr/bin/env python3
"""arXiv fixes Batch 3 — mechanical fixes for all .tex files under papers/"""
import os, re, sys

FILES = []
for root, dirs, filenames in os.walk('papers'):
    for fn in filenames:
        if fn.endswith('.tex'):
            FILES.append(os.path.join(root, fn).replace('\\', '/'))

print(f"Found {len(FILES)} .tex files under papers/")

# Physics package replacements: \dv, \pdv, \abs, \norm, \ket, \bra
PHYSICS_REPLACEMENTS = [
    # \dv{x}{y} -> \frac{d x}{d y}
    (re.compile(r'\\dv\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{d \1}{d \2}'),
    # \dv*{x}{y}
    (re.compile(r'\\dv\*\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{d \1}{d \2}'),
    # \pdv{x}{y} -> \frac{\partial x}{\partial y}
    (re.compile(r'\\pdv\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{\\partial \1}{\\partial \2}'),
    # \pdv*{x}{y}
    (re.compile(r'\\pdv\*\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\frac{\\partial \1}{\\partial \2}'),
    # \abs{x} -> \left|x\right|  (keep it simple)
    (re.compile(r'\\abs\s*\{([^}]+)\}'), r'\\left|\1\\right|'),
    # \norm{x} -> \left\|x\right\|
    (re.compile(r'\\norm\s*\{([^}]+)\}'), r'\\left\\|\1\\right\\|'),
    # \ket{x} -> |x\rangle
    (re.compile(r'\\ket\s*\{([^}]+)\}'), r'|\1\\rangle'),
    # \bra{x} -> \langle x|
    (re.compile(r'\\bra\s*\{([^}]+)\}'), r'\\langle \1|'),
    # \braket{x}{y} -> \langle x | y \rangle
    (re.compile(r'\\braket\s*\{([^}]+)\}\s*\{([^}]+)\}'), r'\\langle \1 | \2 \\rangle'),
]

def apply_physics_replacements(content):
    """Replace physics package commands with standard LaTeX"""
    for pattern, replacement in PHYSICS_REPLACEMENTS:
        content = pattern.sub(replacement, content)
    return content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # Fix 1: Add \pdfoutput=1 as first line (before \documentclass)
    if not content.lstrip().startswith('\\pdfoutput=1'):
        # Find \documentclass
        m = re.search(r'(\\documentclass)', content)
        if m:
            # Insert before \documentclass
            idx = m.start()
            # Find start of line containing \documentclass
            line_start = content.rfind('\n', 0, idx)
            if line_start == -1:
                line_start = 0
            # Insert \pdfoutput=1 on its own line before \documentclass
            content = content[:line_start] + '\n\\pdfoutput=1\n' + content[line_start:]
            modified = True
    
    # Fix 2: Remove \usepackage[utf8]{inputenc} or similar
    new_content = re.sub(
        r'\\usepackage\[utf8?\]\{inputenc\}\s*\n?',
        '',
        content
    )
    new_content = re.sub(
        r'\\usepackage\{inputenc\}\s*\n?',
        '',
        new_content
    )
    if new_content != content:
        modified = True
        content = new_content
    
    # Fix 3: Remove \usepackage{physics} & replace physics commands
    if '\\usepackage{physics}' in content:
        # First, replace physics commands
        content = apply_physics_replacements(content)
        # Then remove the physics package
        content = re.sub(r'\\usepackage\{physics\}\s*\n?', '', content)
        modified = True
    
    # Fix 4: Remove linkcolor=blue, from hyperref options
    new_content = re.sub(
        r'linkcolor\s*=\s*blue\s*,?\s*',
        '',
        content
    )
    # Also handle linkcolor=blue without trailing comma
    new_content = re.sub(
        r',?\s*linkcolor\s*=\s*blue',
        '',
        new_content
    )
    if new_content != content:
        modified = True
        content = new_content
    
    # Fix 5: \documentclass{ctexart} → \documentclass{article}
    if '\\documentclass{ctexart}' in content or '\\documentclass[ctexart' in content or 'ctexart' in content:
        content = content.replace('\\documentclass{ctexart}', '\\documentclass{article}')
        content = re.sub(r'\\documentclass\[([^\]]*)\]\{ctexart\}', r'\\documentclass[\1]{article}', content)
        modified = True
    
    # Remove ctex/xeCJK/fontspec/CJK related packages
    cjk_packages = [
        r'\\usepackage(\[[^\]]*\])?\{ctex\}',
        r'\\usepackage(\[[^\]]*\])?\{xeCJK\}',
        r'\\usepackage(\[[^\]]*\])?\{fontspec\}',
        r'\\usepackage(\[[^\]]*\])?\{CJK\}',
        r'\\usepackage(\[[^\]]*\])?\{CJKutf8\}',
        r'\\usepackage(\[[^\]]*\])?\{CJKspace\}',
    ]
    for pkg in cjk_packages:
        new_content = re.sub(pkg + r'\s*\n?', '', content)
        if new_content != content:
            modified = True
            content = new_content
    
    # Fix 6: \author{...} → \author{SCX}
    new_content = re.sub(r'\\author\{[^}]*\}', r'\\author{SCX}', content)
    if new_content != content:
        modified = True
        content = new_content
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for f in FILES:
    if fix_file(f):
        count += 1
        print(f"  FIXED: {f}")

print(f"\nTotal: {count} files modified out of {len(FILES)}")
