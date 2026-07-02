#!/usr/bin/env python3
"""
SCX Paper Audit Script — Quality Gate for All Papers
Run: python audit_papers.py [--fix] [--dir papers/]

Checks:
  1. Chinese characters in .tex files
  2. Missing English theorem names
  3. \mathsf vs \textsf macros
  4. Missing \author{SCX}
  5. pdflatex/xelatex compilation
  6. Abstract presence
  7. Bibliography completeness
"""

import os, re, subprocess, sys, glob

SCX_DIR = os.path.dirname(os.path.abspath(__file__))
PAPERS_DIR = os.path.join(SCX_DIR, "papers")

# Chinese character range
CN_RE = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')

# Problematic patterns
CN_THEOREM_RE = re.compile(r'\\(newtheorem\{[^}]*\}\{[^}]*\}.*[\u4e00-\u9fff])')
MATHF_RE = re.compile(r'\\mathsf\{(SCX|Yajie|Situs|Cercis|Spring|MoE)\}')
CN_SECTION_RE = re.compile(r'\\(section|subsection|subsubsection)\{.*[\u4e00-\u9fff]')


def find_tex_files():
    """Find all .tex files in papers/"""
    return sorted(glob.glob(os.path.join(PAPERS_DIR, "**/*.tex"), recursive=True))


def check_chinese(filepath):
    """Return list of (line_num, line) with Chinese characters"""
    issues = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if CN_RE.search(line):
                # Skip comment lines (they're less critical)
                stripped = line.strip()
                if stripped.startswith('%'):
                    issues.append((i, f"[COMMENT] {stripped[:100]}"))
                else:
                    issues.append((i, f"[CODE] {stripped[:100]}"))
    return issues


def check_theorem_names(filepath):
    """Check theorem environments use English names"""
    issues = []
    cn_names = {'定理': 'Theorem', '引理': 'Lemma', '推论': 'Corollary',
                '定义': 'Definition', '注记': 'Remark', '猜想': 'Conjecture',
                '命题': 'Proposition', '例': 'Example', '假设': 'Assumption'}
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for cn, en in cn_names.items():
        if cn in content:
            issues.append(f"Chinese theorem name: '{cn}' (should be '{en}')")
    return issues


def check_mathsf(filepath):
    """Check for \mathsf instead of \textsf"""
    issues = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if MATHF_RE.search(line):
                issues.append((i, line.strip()[:100]))
    return issues


def check_author(filepath):
    """Check \author{SCX} is present"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if r'\author{SCX}' not in content and r'\author{SCX}' not in content:
        return "Missing \\author{SCX}"
    return None


def check_abstract(filepath):
    """Check abstract exists"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if r'\begin{abstract}' not in content:
        return "Missing abstract"
    return None


def check_compile(filepath):
    """Try to compile with pdflatex"""
    d = os.path.dirname(filepath)
    f = os.path.basename(filepath)
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', d, f],
            cwd=d, capture_output=True, text=True, timeout=30
        )
        errors = [l for l in result.stdout.split('\n') if l.startswith('!')]
        return errors[:5] if errors else []
    except Exception as e:
        return [str(e)]


def check_bib(filepath):
    """Check if bibliography is present"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if r'\bibliography' not in content and r'\begin{thebibliography}' not in content:
        return "No bibliography"
    return None


# ===================================================================
# AUTO-FIX FUNCTIONS
# ===================================================================

def fix_mathsf(filepath):
    """Replace \mathsf{SCX} etc with \textsf{SCX} etc"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    macros = ['SCX', 'Yajie', 'Spring', 'Cercis', 'Situs', 'MoE']
    changed = False
    for m in macros:
        old = f'\\mathsf{{{m}}}'
        new = f'\\textsf{{{m}}}'
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed


def fix_theorem_names(filepath):
    """Replace Chinese theorem names with English"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    mapping = {
        '定理': 'Theorem', '引理': 'Lemma', '推论': 'Corollary',
        '定义': 'Definition', '注记': 'Remark', '猜想': 'Conjecture',
        '命题': 'Proposition', '例': 'Example', '假设': 'Assumption',
        '操作流程': 'Protocol', '证明': 'Proof', '参考文献': 'References',
        '摘要': 'Abstract', '目录': 'Contents',
    }
    changed = False
    for cn, en in mapping.items():
        if cn in content:
            content = content.replace(cn, en)
            changed = True
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed


# ===================================================================
# MAIN REPORT
# ===================================================================

def audit_all(fix=False):
    """Run full audit on all papers"""
    papers = find_tex_files()
    report = []
    total_chinese = 0
    total_issues = 0
    clean_papers = 0

    print("=" * 70)
    print("SCX PAPER AUDIT — English-Only Quality Gate")
    print(f"Auditing {len(papers)} .tex files in {PAPERS_DIR}")
    print("=" * 70)

    for path in papers:
        rel = os.path.relpath(path, SCX_DIR)
        issues = []

        # Chinese check
        cn = check_chinese(path)
        if cn:
            code_lines = [l for l in cn if '[CODE]' in l[1]]
            comment_lines = [l for l in cn if '[COMMENT]' in l[1]]
            if code_lines:
                issues.append(f"CHINESE: {len(code_lines)} code lines with Chinese")
                total_chinese += len(code_lines)
            if comment_lines:
                issues.append(f"CHINESE-COMMENT: {len(comment_lines)} comment lines")

        # Theorem names
        tn = check_theorem_names(path)
        if tn:
            issues.append(f"THEOREM: {len(tn)} Chinese theorem names")
            if fix:
                fix_theorem_names(path)

        # \mathsf check
        sf = check_mathsf(path)
        if sf:
            issues.append(f"\\MATHF: {len(sf)} occurrences")
            if fix:
                fix_mathsf(path)

        # Author
        au = check_author(path)
        if au:
            issues.append(au)

        # Abstract
        ab = check_abstract(path)
        if ab:
            issues.append(ab)

        # Bibliography
        bb = check_bib(path)
        if bb:
            issues.append(bb)

        # Compile
        ce = check_compile(path)
        if ce:
            issues.append(f"COMPILE: {len(ce)} errors")

        if issues:
            total_issues += len(issues)
            print(f"\n❌ {rel}")
            for iss in issues:
                print(f"   {iss}")
            if cn:
                for ln, line in cn[:3]:
                    print(f"   L{ln}: {line}")
        else:
            clean_papers += 1

    # Clean up aux files
    for f in glob.glob(os.path.join(PAPERS_DIR, "**/*.aux"), recursive=True):
        os.remove(f)
    for f in glob.glob(os.path.join(PAPERS_DIR, "**/*.log"), recursive=True):
        os.remove(f)

    print("\n" + "=" * 70)
    print(f"SUMMARY")
    print(f"  Total papers:     {len(papers)}")
    print(f"  Clean (no issues): {clean_papers}")
    print(f"  Issues found:     {total_issues}")
    print(f"  Chinese code lines: {total_chinese}")
    print("=" * 70)

    if total_chinese == 0 and total_issues == 0:
        print("✅ ALL PAPERS CLEAN — English-only, no compilation errors")
    else:
        print(f"⚠️  {total_issues} issues to fix. Run with --fix to auto-correct.")

    return 0 if (total_issues == 0) else 1


if __name__ == '__main__':
    fix = '--fix' in sys.argv
    sys.exit(audit_all(fix=fix))
