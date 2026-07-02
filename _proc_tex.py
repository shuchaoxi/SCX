#!/usr/bin/env python3
"""Process turbulence_moduli main.tex: remove all Chinese, keep English."""
import re
import sys

def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def process_turbulence_moduli(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip pure Chinese comment lines (but keep English comment lines)
        stripped = line.strip()
        if stripped.startswith('%') and has_chinese(stripped):
            # Check if there's also English in this comment
            if not re.search(r'[a-zA-Z]{3,}', stripped):
                i += 1
                continue
            # Mixed comment - keep but remove Chinese part
            # For now, skip if mostly Chinese
            cn_chars = len(re.findall(r'[\u4e00-\u9fff]', stripped))
            en_chars = len(re.findall(r'[a-zA-Z]', stripped))
            if cn_chars > en_chars:
                i += 1
                continue
        
        # Skip section headers that are Chinese-only (English follows)
        if stripped.startswith('\\section{') and has_chinese(stripped):
            # Check if next line has English section
            if i + 1 < len(lines) and '\\section{' in lines[i+1] and not has_chinese(lines[i+1]):
                i += 1
                continue
        
        if stripped.startswith('\\subsection{') and has_chinese(stripped):
            if i + 1 < len(lines) and '\\subsection{' in lines[i+1] and not has_chinese(lines[i+1]):
                i += 1
                continue
        
        # Remove Chinese-only body text (paragraphs between section headers)
        # A line is Chinese body text if it has Chinese and no LaTeX commands or English
        if has_chinese(line) and not stripped.startswith('\\') and not stripped.startswith('%'):
            # Check if this line has significant English too
            en_chars = len(re.findall(r'[a-zA-Z]', line))
            cn_chars = len(re.findall(r'[\u4e00-\u9fff]', line))
            if cn_chars > en_chars * 2 and en_chars < 20:
                # Mostly Chinese, and next or prev line has English equivalent
                # Check if surrounding lines suggest this is part of a bilingual pair
                look_ahead = ''
                look_behind = ''
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip() and not lines[j].strip().startswith('\\') and not lines[j].strip().startswith('%'):
                        look_ahead = lines[j]
                        break
                for j in range(i-1, max(i-5, -1), -1):
                    if lines[j].strip() and not lines[j].strip().startswith('\\') and not lines[j].strip().startswith('%'):
                        look_behind = lines[j]
                        break
                
                if has_chinese(look_ahead) or (look_behind and not has_chinese(look_behind)):
                    i += 1
                    continue
        
        result.append(line)
        i += 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(result)
    
    print(f"Processed {input_path} -> {output_path}")
    # Count remaining Chinese
    remaining = sum(1 for l in result if has_chinese(l))
    print(f"Remaining Chinese lines: {remaining}")

if __name__ == '__main__':
    process_turbulence_moduli(sys.argv[1], sys.argv[1])
