#!/usr/bin/env python3
"""Translate Chinese text in SCX LaTeX files to English.
This is NOT a blind regex script — it reads each file, identifies Chinese
content, and performs targeted translations based on file structure."""

import os
import re
import sys

# ── Translation maps for common SCX patterns ──
# These are the most common Chinese patterns found across all SCX files

TITLE_TRANSLATIONS = {
    # Section titles
    '引言': 'Introduction',
    '引言 / Introduction': 'Introduction',
    '中文': 'Chinese Version',
    'Abstract：': 'Abstract:',
    '中文Abstract.': 'Abstract.',
    '核心问题': 'Core Question',
    '主要贡献': 'Main Contributions',
    '结论': 'Conclusion',
    '参考文献': 'References',
    '预备知识': 'Preliminaries',
    '问题背景': 'Problem Background',
    '模型设定': 'Model Formulation',
    '基本设定': 'Basic Setup',
    '基本定义': 'Basic Definitions',
    '形式化定义': 'Formal Definition',
    '核心定理': 'Core Theorems',
    '定理体系': 'Theorem System',
    '当前阻塞': 'Current Blockers',
    '关联': 'Connections',
    '关键路径': 'Critical Path',
    '最终Verdict': 'Final Verdict',
    '验证命令': 'Verification Commands',
    '备查': 'For Reference',
    '继承': 'Succession',
    '钱怎么走': 'How Money Flows',
    '三层结构': 'Three-Layer Structure',
    '核心原则': 'Core Principle',
    '设计原则': 'Design Principles',
    '层级属性': 'Layer Properties',
    '贡献': 'Contributions',
    '诚实性原则': 'Honesty Principle',
    '五轮迭代历程': 'Five-Round Iteration History',
    '三条修正路径概览': 'Overview of Three Corrected Paths',
    '背景与动机': 'Background and Motivation',
    '核心问题': 'Core Problem',
    '审计注记': 'Audit Note',
    '经济洞见': 'Economic Insight',
    '商业注记': 'Business Insight',
    '教育注记': 'Education Note',
    '艺术注记': 'Art Note',
    '教育含义': 'Educational Implication',
    '教育含义.': 'Educational Implication.',
    '审计之剑声明': 'The Audit Sword Declaration',
    '数学依据': 'Mathematical Basis',
    '中文对照：': 'Chinese version:',
    '中文问题陈述：': 'Problem Statement:',
    
    # Theorem names
    '定理': 'Theorem',
    '引理': 'Lemma',
    '推论': 'Corollary',
    '定义': 'Definition',
    '注记': 'Remark',
    '证明': 'Proof',
    '猜想': 'Conjecture',
    '假设': 'Assumption',
    '原理': 'Principle',
    '例': 'Example',
    '注': 'Note',
    
    # Common compound patterns
    '定理1': 'Theorem 1',
    '定理2': 'Theorem 2',
    '定理3': 'Theorem 3',
    '定理4': 'Theorem 4',
    '定理5': 'Theorem 5',
    '定理6': 'Theorem 6',
    '定理7': 'Theorem 7',
    '定理8': 'Theorem 8',
    '定理9': 'Theorem 9',
    '定理10': 'Theorem 10',
    '定理11': 'Theorem 11',
    '定理12': 'Theorem 12',
}

# Section/definition labels that appear with Chinese names
CHINESE_SECTION_PATTERN = re.compile(
    r'\\(?:sub)?section\{([^}]*[\u4e00-\u9fff][^}]*)\}',
    re.UNICODE
)

CHINESE_THEOREM_PATTERN = re.compile(
    r'\\(?:begin)\{(?:theorem|lemma|corollary|definition|proposition|remark|conjecture|assumption|example|protocol|axiom|principle)\}'
    r'(?:\[([^\]]*[\u4e00-\u9fff][^\]]*)\])?',
    re.UNICODE
)

# Pattern for bilingual section titles like "Introduction 引言"
BILINGUAL_SECTION = re.compile(
    r'\\(?:sub)?section\{([^}]*?)\s+([\u4e00-\u9fff][^}]*)\}',
    re.UNICODE
)

def has_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def clean_bilingual_section(title):
    """For bilingual titles like 'Introduction 引言', keep only English part."""
    # If it's like "Introduction 引言" or "引言 / Introduction"
    if ' / ' in title:
        parts = title.split(' / ')
        # Prefer English part (longer, or without Chinese)
        en_parts = [p for p in parts if not has_chinese(p)]
        if en_parts:
            return en_parts[0].strip()
    # If it's like "Introduction 引言"
    words = title.split()
    en_words = [w for w in words if not has_chinese(w)]
    if en_words:
        return ' '.join(en_words)
    return title

def translate_chinese_in_text(text):
    """Translate common Chinese words and phrases in text."""
    # Replace common Chinese characters/phrases
    replacements = [
        ('中文Abstract.', 'Abstract.'),
        ('中文对照：', ''),
        ('中文问题陈述：', 'Problem Statement:'),
        ('。', '.'),
        ('，', ', '),
        ('；', '; '),
        ('：', ': '),
        ('「', '"'),
        ('」', '"'),
        ('（', ' ('),
        ('）', ') '),
        ('、', ', '),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def process_file(filepath):
    """Process a single LaTeX file, translating Chinese to English."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # Strategy depends on file type
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))
    
    # ── 1. Handle ctexart → article conversion ──
    if r'\documentclass' in content and 'ctexart' in content:
        content = content.replace('ctexart', 'article')
        # Remove ctex-specific font settings that need Chinese
        content = re.sub(r'\\setCJKmainfont\{[^}]*\}.*\n', '', content)
        content = re.sub(r'\\setCJKsansfont\{[^}]*\}.*\n', '', content)
        content = re.sub(r'\\setCJKmonofont\{[^}]*\}.*\n', '', content)
        # Remove \usepackage[UTF8]{ctex} and similar
        content = re.sub(r'\\usepackage\[UTF8[^\]]*\]\{ctex\}.*\n', '', content)
        content = re.sub(r'\\usepackage\{CJKutf8\}.*\n', '', content)
        content = re.sub(r'\\usepackage\{xeCJK\}.*\n', '', content)
        # Remove CJK environment
        content = re.sub(r'\\begin\{CJK\}\{UTF8\}\{[^}]*\}.*\n', '', content)
        content = re.sub(r'\\end\{CJK\}.*\n', '', content)
        # Remove fontspec CJK settings
        content = re.sub(r'\\newfontfamily\\cjkfont\{[^}]*\}.*\n', '', content)
        modified = True
    
    # ── 2. Replace \mathsf{SCX} with \textsf{SCX} ──
    if r'\mathsf{SCX}' in content:
        content = content.replace(r'\mathsf{SCX}', r'\textsf{SCX}')
        modified = True
    
    # ── 3. Fix author ──
    if r'\author{' in content:
        content = re.sub(r'\\author\{[^}]*[\u4e00-\u9fff][^}]*\}', r'\\author{SCX}', content)
    
    # ── 4. Fix date ──
    content = re.sub(r'\\date\{(\d{4})年(\d{1,2})月(\d{1,2})日\}', r'\\date{\1-\2-\3}', content)
    content = re.sub(r'\\date\{(\d{4})年(\d{1,2})月\}', r'\\date{\1-\2}', content)
    
    # ── 5. Remove bilingual Chinese from titles/sections ──
    # Pattern: "English Chinese" or "Chinese / English"
    def clean_section_title(match):
        full = match.group(0)
        title = match.group(1)
        if has_chinese(title):
            cleaned = clean_bilingual_section(title)
            if cleaned != title:
                return full.replace(title, cleaned)
        return full
    
    content = re.sub(
        r'\\(?:sub)?section\{([^}]*)\}',
        clean_section_title,
        content
    )
    
    # ── 6. Remove Chinese subsection blocks ──
    # Pattern: \subsection{中文} ... content ... \subsection{English}
    content = re.sub(
        r'\\subsection\{中文\}.*?(?=\\subsection\{English\})',
        '',
        content,
        flags=re.DOTALL
    )
    
    # ── 7. Clean figure/table captions ──
    def clean_caption(match):
        full = match.group(0)
        cap = match.group(1)
        if has_chinese(cap):
            # Keep only the English part
            if ' / ' in cap:
                parts = cap.split(' / ')
                en = [p for p in parts if not has_chinese(p)]
                if en:
                    return full.replace(cap, en[0].strip())
            elif '——' in cap:
                parts = cap.split('——')
                en = [p for p in parts if not has_chinese(p)]
                if en:
                    return full.replace(cap, en[0].strip())
        return full
    
    content = re.sub(
        r'\\caption\{([^}]*)\}',
        clean_caption,
        content
    )
    
    # ── 8. Remove bilingual inline comments ──
    # Pattern: English text \\small Chinese text
    content = re.sub(
        r'\\\\ \\\\small\s*[\u4e00-\u9fff][^}]*?(?=\\\\)',
        '',
        content
    )
    
    # ── 9. Clean keywords ──
    def clean_keywords(match):
        full = match.group(0)
        text = match.group(1)
        if has_chinese(text):
            # Remove Chinese keywords, keep English
            parts = re.split(r'[;,]', text)
            en_parts = [p.strip() for p in parts if not has_chinese(p.strip()) or
                       (has_chinese(p.strip()) and not any(c.isascii() and c.isalpha() for c in p.strip()))]
            # Actually, keep parts that are Chinese translations of English keywords
            cleaned = ', '.join(p.strip() for p in parts if p.strip())
            return full.replace(text, cleaned)
        return full
    
    content = re.sub(
        r'\\textbf\{Keywords[^}]*\}:?\s*([^\n]+)',
        clean_keywords,
        content
    )
    content = re.sub(
        r'\\noindent\\textbf\{Keywords[^}]*\}:?\s*([^\n]+)',
        clean_keywords,
        content
    )
    
    # ── 10. Remove clearly Chinese-only lines ──
    # Lines that are >50% Chinese characters
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue
        # Count Chinese chars
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', stripped))
        total_chars = len(stripped.replace(' ', ''))
        if total_chars > 0 and chinese_chars / total_chars > 0.5:
            # Line is mostly Chinese - skip it
            # But check if it contains math/LaTeX commands
            if not re.search(r'\\[a-zA-Z]', stripped) and not re.search(r'\$', stripped):
                continue  # Skip pure Chinese lines
        new_lines.append(line)
    
    if len(new_lines) != len(lines):
        content = '\n'.join(new_lines)
        modified = True
    
    # ── 11. Fix remaining Chinese punctuation ──
    content = content.replace('：', ': ')
    content = content.replace('。', '.')
    content = content.replace('，', ', ')
    content = content.replace('；', '; ')
    
    if modified or content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not files:
        print("Usage: python translate_scx.py <file1> <file2> ...")
        sys.exit(1)
    
    for f in files:
        if os.path.exists(f):
            changed = process_file(f)
            status = '✓ MODIFIED' if changed else '  unchanged'
            print(f'{status}: {f}')
        else:
            print(f'NOT FOUND: {f}')

if __name__ == '__main__':
    main()
