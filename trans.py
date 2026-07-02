#!/usr/bin/env python3
"""More aggressive Chinese-to-English translation for SCX LaTeX files.
Handles bilingual content by stripping Chinese, translates common patterns."""
import re, sys, os

def strip_chinese_from_brackets(text):
    """Remove Chinese from LaTeX section/caption/etc brackets, keeping English."""
    def clean(m):
        full = m.group(0)
        inner = m.group(1)
        # Split by common separators
        for sep in [' / ', ' --- ', '——', ' -- ']:
            if sep in inner:
                parts = inner.split(sep)
                en = [p.strip() for p in parts if not re.search(r'[\u4e00-\u9fff]', p)]
                if en:
                    return full.replace(inner, en[0])
        # Try removing Chinese words
        words = inner.split()
        en = [w for w in words if not re.search(r'[\u4e00-\u9fff]', w)]
        if en and len(en) >= len(words) * 0.3:
            return full.replace(inner, ' '.join(en))
        return full
    
    # Process section titles, captions, labels
    text = re.sub(r'\\(?:sub)?section\{([^}]*)\}', clean, text)
    text = re.sub(r'\\caption\{([^}]*)\}', clean, text)
    text = re.sub(r'\\textbf\{([^}]*)\}', clean, text)
    text = re.sub(r'\\textit\{([^}]*)\}', clean, text)
    return text

def remove_chinese_lines(text):
    """Remove lines that are predominantly Chinese."""
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append(line)
            continue
        chinese = len(re.findall(r'[\u4e00-\u9fff]', stripped))
        total = len(stripped.replace(' ', '').replace('\\', '').replace('{', '').replace('}', ''))
        if total > 0 and chinese / max(total, 1) > 0.4:
            # Skip lines that are >40% Chinese unless they contain LaTeX commands
            if not re.search(r'\\[a-zA-Z]', stripped) and not re.search(r'\$', stripped):
                continue
        result.append(line)
    return '\n'.join(result)

def remove_chinese_blocks(text):
    """Remove blocks of text that are purely Chinese (bilingual sections)."""
    # Remove "中文" subsection blocks
    text = re.sub(r'\\subsection\{中文\}.*?(?=\\subsection|\\section)', '', text, flags=re.DOTALL)
    # Remove Chinese abstract blocks
    text = re.sub(r'\\noindent\\textbf\{中文Abstract\.\}.*?(?=\\medskip|\\noindent\\textbf)', '', text, flags=re.DOTALL)
    # Remove "中文对照" blocks
    text = re.sub(r'\\noindent\\textbf\{中文对照：?\}.*?(?=\\medskip|\\noindent)', '', text, flags=re.DOTALL)
    # Remove Chinese-only paragraphs (entire paragraph is Chinese)
    text = re.sub(r'\n\s*[\u4e00-\u9fff][\u4e00-\u9fff\s，。；：、！？""''《》（）\d\w\\{}%&$#@!.,;:+\-*\/=<>\[\]|~`\'\"^\(\)\n]{50,}.*?(?=\n\n|\n\\|\n\s*[A-Z])', '\n', text, flags=re.DOTALL)
    return text

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Basic replacements
    content = content.replace(r'\mathsf{SCX}', r'\textsf{SCX}')
    content = content.replace('ctexart', 'article')
    
    # Remove CJK packages
    content = re.sub(r'\\usepackage\[UTF8[^\]]*\]\{ctex\}.*\n', '', content)
    content = re.sub(r'\\usepackage\{CJKutf8\}.*\n', '', content)
    content = re.sub(r'\\usepackage\{xeCJK\}.*\n', '', content)
    content = re.sub(r'\\setCJKmainfont\{[^}]*\}.*\n', '', content)
    content = re.sub(r'\\setCJKsansfont\{[^}]*\}.*\n', '', content)
    content = re.sub(r'\\setCJKmonofont\{[^}]*\}.*\n', '', content)
    content = re.sub(r'\\newfontfamily\\cjkfont\{[^}]*\}.*\n', '', content)
    
    # Theorem names
    for cn, en in [('定理', 'Theorem'), ('引理', 'Lemma'), ('推论', 'Corollary'),
                    ('定义', 'Definition'), ('注记', 'Remark'), ('猜想', 'Conjecture'),
                    ('假设', 'Assumption'), ('例', 'Example'), ('原理', 'Principle'),
                    ('注', 'Note'), ('证明', 'Proof')]:
        content = content.replace('{' + cn + '}', '{' + en + '}')
        content = content.replace('{' + cn + ' ', '{' + en + ' ')
    
    # Chinese dates
    content = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', r'\1-\2-\3', content)
    content = re.sub(r'(\d{4})年(\d{1,2})月', r'\1-\2', content)
    
    # Chinese punctuation
    content = content.replace('：', ': ')
    content = content.replace('。', '.')
    content = content.replace('，', ', ')
    content = content.replace('；', '; ')
    
    # Strip Chinese from brackets
    content = strip_chinese_from_brackets(content)
    
    # Remove Chinese blocks
    content = remove_chinese_blocks(content)
    
    # Remove Chinese lines
    content = remove_chinese_lines(content)
    
    # Fix author
    content = re.sub(r'\\author\{[^}]*[\u4e00-\u9fff][^}]*\}', r'\\author{SCX}', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        chinese_after = len(re.findall(r'[\u4e00-\u9fff]', content))
        return chinese_after
    return -1

if __name__ == '__main__':
    for f in sys.argv[1:]:
        if os.path.exists(f):
            remaining = process_file(f)
            print(f'{remaining:>5} Chinese chars remaining: {f}')
