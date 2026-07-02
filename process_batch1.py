#!/usr/bin/env python3
"""Process SCX LaTeX papers: remove Chinese, fix formatting, prepare for pdflatex."""

import re
import sys

def contains_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def process_consciousness(content):
    """Process scx_consciousness/main.tex"""
    lines = content.split('\n')
    new_lines = []
    skip_until_english = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Remove ctex package
        if r'\usepackage[UTF8]{ctex}' in line:
            i += 1
            continue
        
        # Fix author
        if line.strip() == r'\author{}':
            new_lines.append(r'\author{SCX}')
            i += 1
            continue
        
        # Handle bilingual section headings
        sec_match = re.match(r'(\\section\{)(.+)(\})', line)
        sub_match = re.match(r'(\\subsection\{)(.+)(\})', line)
        if sec_match:
            title = sec_match.group(2)
            # Check if it's bilingual "中文 / English" or "English / 中文"
            if '/' in title and contains_chinese(title):
                # Extract English part
                parts = title.split('/')
                # Find the part without Chinese
                for p in parts:
                    p_stripped = p.strip()
                    if not contains_chinese(p_stripped):
                        new_lines.append(sec_match.group(1) + p_stripped + sec_match.group(3))
                        break
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            i += 1
            continue
        
        if sub_match:
            title = sub_match.group(2)
            if '/' in title and contains_chinese(title):
                parts = title.split('/')
                for p in parts:
                    p_stripped = p.strip()
                    if not contains_chinese(p_stripped):
                        new_lines.append(sub_match.group(1) + p_stripped + sub_match.group(3))
                        break
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            i += 1
            continue
        
        # Handle abstract tag / Chinese paragraph markers
        if line.strip() == r'\textbf{中文.}' or line.strip() == r'\textbf{中文}' or r'\textbf{中文}' in line:
            # Skip Chinese abstract paragraph - skip until \textbf{English.} or \vspace or empty line+next block
            j = i + 1
            while j < len(lines):
                if r'\textbf{English.}' in lines[j] or r'\textbf{English}' in lines[j]:
                    i = j
                    break
                # Check for end of abstract (next section or end of abstract env)
                if lines[j].strip().startswith(r'\end{abstract}') or lines[j].strip().startswith(r'\vspace'):
                    # No English version found, just skip
                    i = j
                    break
                j += 1
            else:
                i += 1
            continue
        
        # Handle bilingual block: Chinese paragraph followed by English paragraph
        # Pattern: \noindent\n\textbf{中文.}\n... Chinese text ...\n\vspace\n\noindent\n\textbf{English.}
        if '\\noindent' in line or line.strip().startswith('\\textbf{中文'):
            # Look ahead to see if this starts a Chinese block
            remaining = '\n'.join(lines[i:i+20])
            if contains_chinese(line) and not ('English' in line or 'english' in line):
                # This is a Chinese block - skip until we find English or next section
                j = i + 1
                depth = 0
                while j < len(lines):
                    lj = lines[j].strip()
                    if '\\textbf{English.}' in lj or '\\textbf{English}' in lj:
                        i = j  # Jump to English block start
                        break
                    if lj.startswith('\\section{') or lj.startswith('\\subsection{') or lj.startswith('\\begin{theorem}') or lj.startswith('\\begin{definition}') or lj.startswith('\\begin{proof}') or lj.startswith('\\end{') or lj == '}':
                        i = j
                        break
                    j += 1
                else:
                    i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def process_instanton_k2(content):
    """Process scx_instanton_k2/main.tex"""
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Remove ctex package
        if r'\usepackage[UTF8]{ctex}' in line:
            i += 1
            continue
        
        # Fix author
        if r'\author{SCX理论架构师}' in line:
            new_lines.append(r'\author{SCX}')
            i += 1
            continue
        
        # Fix date
        if '2026年7月' in line:
            new_lines.append(r'\date{July 2026}')
            i += 1
            continue
        
        # Bilingual section/subsection headings
        sec_match = re.match(r'(\\section\{)(.+)(\})', line)
        sub_match = re.match(r'(\\subsection\{)(.+)(\})', line)
        if sec_match:
            title = sec_match.group(2)
            if '/' in title and contains_chinese(title):
                parts = title.split('/')
                for p in parts:
                    p_stripped = p.strip()
                    if not contains_chinese(p_stripped):
                        new_lines.append(sec_match.group(1) + p_stripped + sec_match.group(3))
                        break
                else:
                    new_lines.append(line)
            elif contains_chinese(title):
                # Pure Chinese heading - translate
                # These are rare, handle case by case
                eng_title = translate_heading(title)
                if eng_title:
                    new_lines.append(sec_match.group(1) + eng_title + sec_match.group(3))
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            i += 1
            continue
        
        if sub_match:
            title = sub_match.group(2)
            if '/' in title and contains_chinese(title):
                parts = title.split('/')
                for p in parts:
                    p_stripped = p.strip()
                    if not contains_chinese(p_stripped):
                        new_lines.append(sub_match.group(1) + p_stripped + sub_match.group(3))
                        break
                else:
                    new_lines.append(line)
            elif contains_chinese(title):
                eng_title = translate_heading(title)
                if eng_title:
                    new_lines.append(sub_match.group(1) + eng_title + sub_match.group(3))
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            i += 1
            continue
        
        # Chinese abstract paragraph
        if line.strip() == r'\textbf{中文.}' or (r'\textbf{中文}' in line and 'English' not in line):
            j = i + 1
            while j < len(lines):
                if r'\textbf{English.}' in lines[j] or r'\textbf{English}' in lines[j]:
                    i = j
                    break
                if lines[j].strip().startswith(r'\end{abstract}') or lines[j].strip().startswith(r'\vspace'):
                    i = j
                    break
                j += 1
            else:
                i += 1
            continue
        
        # Chinese-only headings (like 预备知识, 形式化模型, etc.)
        if contains_chinese(line) and not any(eng_word in line for eng_word in ['English', 'english', 'Definition', 'Theorem', 'Proof', 'Algorithm', 'Remark', 'Proposition']):
            # Check if this is a standalone Chinese line (not part of a bilingual block)
            if line.strip().startswith('\\noindent') or line.strip().startswith('\\textbf{中文'):
                j = i + 1
                while j < len(lines):
                    if '\\textbf{English.}' in lines[j] or '\\textbf{English}' in lines[j]:
                        i = j
                        break
                    if lines[j].strip().startswith('\\section{') or lines[j].strip().startswith('\\subsection{') or lines[j].strip().startswith('\\begin{') or lines[j].strip().startswith('\\end{'):
                        i = j
                        break
                    j += 1
                else:
                    i += 1
                continue
            elif line.strip().startswith('\\subsection{') or line.strip().startswith('\\section{'):
                # Already handled above
                new_lines.append(line)
                i += 1
                continue
            elif not line.strip() or line.strip().startswith('%'):
                new_lines.append(line)
                i += 1
                continue
            else:
                # Chinese text in body - skip it
                # Check if there's an English version coming
                j = i + 1
                found_english = False
                while j < min(len(lines), i + 30):
                    if '\\textbf{English.}' in lines[j] or '\\textbf{English}' in lines[j]:
                        i = j
                        found_english = True
                        break
                    if lines[j].strip().startswith('\\begin{') or lines[j].strip().startswith('\\end{') or lines[j].strip().startswith('\\section{'):
                        break
                    j += 1
                if not found_english:
                    new_lines.append(line)
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def translate_heading(chinese_text):
    """Translate common Chinese headings to English."""
    translations = {
        '预备知识：Situs复形与微分形式': 'Preliminaries: Situs Complex and Differential Forms',
        'Situs复形的构造': 'Construction of the Situs Complex',
        '上链复形与上边缘算子': 'Cochain Complex and Coboundary Operator',
        '审计瞬子场：形式化定义': 'Audit Instanton Field: Formal Definition',
        '超越线性框架：非平坦联络的产生': 'Beyond the Linear Framework: Emergence of Non-Flat Connections',
        '场强与共存部分的关系': 'Field-Strength and Co-Exact Part Relation',
        '专家图上的2-闭链结构': '2-Cycle Structure on the Expert Graph',
        '校准非传递性的代数判据': 'Algebraic Criterion for Calibration Non-Transitivity',
        '非传递性的信息论度量': 'Information-Theoretic Measure of Non-Transitivity',
        '三角不一致性的信息论模型': 'Information-Theoretic Model of Triangular Inconsistency',
        '形式化模型': 'Formal Model',
        '信息论下界': 'Information-Theoretic Lower Bound',
        '算法描述': 'Algorithm Description',
        '复杂度分析': 'Complexity Analysis',
        '密度滤过与$H_2$': 'Density Filtration and $H_2$',
        '审计通量谱与持久条形码': 'Audit Flux Spectrum and Persistence Barcode',
        '实验设置': 'Experimental Setup',
        '结果': 'Results',
        '审计不一致性的谱特征': 'Spectral Signature of Audit Inconsistency',
        '全局一致性检测': 'Global Consistency Detection',
    }
    return translations.get(chinese_text.strip(), None)

def process_kappa_suppression(content):
    """Process scx_kappa_suppression/main.tex"""
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Remove ctex package
        if r'\usepackage[UTF8]{ctex}' in line:
            i += 1
            continue
        
        # Fix author
        if r'\author{\SCX\ Theory Group}' in line:
            new_lines.append(r'\author{SCX}')
            i += 1
            continue
        
        # Bilingual section headings
        sec_match = re.match(r'(\\section\{)(.+)(\})', line)
        sub_match = re.match(r'(\\subsection\{)(.+)(\})', line)
        if sec_match:
            title = sec_match.group(2)
            if '/' in title and contains_chinese(title):
                parts = title.split('/')
                for p in parts:
                    p_stripped = p.strip()
                    if not contains_chinese(p_stripped):
                        new_lines.append(sec_match.group(1) + p_stripped + sec_match.group(3))
                        break
                else:
                    new_lines.append(line)
            elif contains_chinese(title) and 'English' not in title:
                # Pure Chinese heading
                eng = translate_kappa_heading(title)
                if eng:
                    new_lines.append(sec_match.group(1) + eng + sec_match.group(3))
                else:
                    # Remove and use next line's English
                    pass
            else:
                new_lines.append(line)
            i += 1
            continue
        
        if sub_match:
            title = sub_match.group(2)
            if '/' in title and contains_chinese(title):
                parts = title.split('/')
                for p in parts:
                    p_stripped = p.strip()
                    if not contains_chinese(p_stripped):
                        new_lines.append(sub_match.group(1) + p_stripped + sub_match.group(3))
                        break
                else:
                    new_lines.append(line)
            elif contains_chinese(title) and 'English' not in title:
                eng = translate_kappa_heading(title)
                if eng:
                    new_lines.append(sub_match.group(1) + eng + sub_match.group(3))
                else:
                    pass
            else:
                new_lines.append(line)
            i += 1
            continue
        
        # Chinese abstract paragraph
        if line.strip() == r'\textbf{中文.}' or (r'\textbf{中文}' in line and 'English' not in line):
            j = i + 1
            while j < len(lines):
                if r'\textbf{English.}' in lines[j] or r'\textbf{English}' in lines[j]:
                    i = j
                    break
                if lines[j].strip().startswith(r'\end{abstract}') or lines[j].strip().startswith(r'\vspace'):
                    i = j
                    break
                j += 1
            else:
                i += 1
            continue
        
        # Chinese body text blocks
        if '\\noindent' in line or line.strip().startswith('\\textbf{中文'):
            if contains_chinese(line) and 'English' not in line and 'english' not in line:
                j = i + 1
                while j < len(lines):
                    if '\\textbf{English.}' in lines[j] or '\\textbf{English}' in lines[j]:
                        i = j
                        break
                    if lines[j].strip().startswith('\\section{') or lines[j].strip().startswith('\\subsection{') or lines[j].strip().startswith('\\begin{theorem}') or lines[j].strip().startswith('\\begin{definition}') or lines[j].strip().startswith('\\begin{proof}') or lines[j].strip().startswith('\\begin{protocol}') or lines[j].strip().startswith('\\end{'):
                        i = j
                        break
                    j += 1
                else:
                    i += 1
                continue
        
        # Chinese comments
        if line.strip().startswith('%') and contains_chinese(line):
            # Translate comment or remove Chinese
            new_lines.append('% ' + re.sub(r'[\u4e00-\u9fff]+', '', line.lstrip('% ')).strip())
            i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def translate_kappa_heading(chinese_text):
    """Translate Chinese kappa headings."""
    translations = {
        '引言：为什么抑制会适得其反？': 'Introduction: Why Does Suppression Backfire?',
        '抑制的工程直觉与数学陷阱': 'Engineering Intuition and the Mathematical Trap',
        '$\\kappa$抑制函数的精确形式': 'Precise Form of the $\\kappa$ Suppression Function',
        '基本定义': 'Basic Definitions',
        '三重分解': 'Triple Decomposition',
        '常用参数化形式': 'Common Parametric Forms',
        '精英侵蚀定理': 'The Elite Erosion Theorem',
        '问题陈述': 'Problem Statement',
        '精英侵蚀的信息论代价': 'Information-Theoretic Cost of Elite Erosion',
        '抑制相变：临界阈值与退化边界': 'Suppression Phase Transition: Critical Threshold and Degradation Boundary',
        '审计质量的度量': 'Measuring Audit Quality',
        '相图与区域划分': 'Phase Diagram and Regime Classification',
        '三重机制的标度律': 'Scaling Laws of the Triple Mechanism',
        '信息抑制 $\\kappa_I$': 'Information Suppression $\\kappa_I$',
        '力抑制 $\\kappa_F$': 'Force Suppression $\\kappa_F$',
        '信念抑制 $\\kappa_B$': 'Belief Suppression $\\kappa_B$',
        '三重机制的交互效应': 'Interaction Effects of the Triple Mechanism',
        '恢复策略：自适应$\\kappa$-退火': 'Recovery Strategy: Adaptive $\\kappa$-Annealing',
        'Cercis一致性条件': 'Cercis Consistency Condition',
        '自适应退火协议': 'Adaptive Annealing Protocol',
        '与SCX核心定理的联系': 'Connections to SCX Core Theorems',
        'Theorem 3 (S3) 的直接推论': 'Direct Corollary of Theorem 3 (S3)',
        'Spring SE-1 的退化': 'Degradation of Spring SE-1',
        '数值实验': 'Numerical Experiments',
        '实验设计': 'Experimental Design',
        '关键数值结果': 'Key Numerical Results',
        '讨论：抑制的文化与制度根源': 'Discussion: Cultural and Institutional Roots of Suppression',
        '为什么抑制在实践中流行？': 'Why Is Suppression Popular in Practice?',
        '开放问题': 'Open Problems',
        '结论': 'Conclusion',
        '与SCX公理体系的关系': 'Relation to the SCX Axiom System',
        '核心贡献': 'Core Contributions',
        '精英侵蚀定理 / Elite Erosion Theorem': 'Elite Erosion Theorem',
        '抑制相变定理 / Suppression Phase Transition Theorem': 'Suppression Phase Transition Theorem',
        '三重分解 / Triple Decomposition': 'Triple Decomposition',
        '精英侵蚀的信息论代价 / Information Diversity Loss': 'Information Diversity Loss',
        '三重机制的不可加性 / Non-Additivity of the Triple Mechanism': 'Non-Additivity of the Triple Mechanism',
        '退火收敛性 / Annealing Convergence': 'Annealing Convergence',
    }
    return translations.get(chinese_text.strip(), None)

def final_cleanup(content):
    """Final cleanup: remove consecutive blank lines, fix any remaining issues."""
    lines = content.split('\n')
    new_lines = []
    prev_blank = False
    
    for line in lines:
        is_blank = not line.strip()
        if is_blank and prev_blank:
            continue
        new_lines.append(line)
        prev_blank = is_blank
    
    # Remove trailing whitespace
    result = '\n'.join(new_lines)
    result = re.sub(r'[ \t]+$', '', result, flags=re.MULTILINE)
    return result

def main():
    files = {
        'papers/scx_consciousness/main.tex': process_consciousness,
        'papers/scx_instanton_k2/main.tex': process_instanton_k2,
        'papers/scx_kappa_suppression/main.tex': process_kappa_suppression,
    }
    
    for filepath, processor in files.items():
        print(f"Processing {filepath}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        processed = processor(content)
        processed = final_cleanup(processed)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(processed)
        
        # Count remaining Chinese
        remaining = len(re.findall(r'[\u4e00-\u9fff]', processed))
        print(f"  Remaining Chinese characters: {remaining}")
    
    print("Done!")

if __name__ == '__main__':
    main()
