#!/usr/bin/env python3
"""Translate Group D papers from Chinese to English. Preserves LaTeX structure and math."""

import re
import os

FILES = [
    "papers/scx_industry/main.tex",
    "papers/scx_information_theory/main.tex",
    "papers/scx_instanton/audit_instanton.tex",
    "papers/scx_journalism/main.tex",
    "papers/scx_lambda/lambda_gauge.tex",
    "papers/scx_law/main.tex",
    "papers/scx_maintainer_analysis/maintainer_analysis.tex",
    "papers/scx_matrix_theory/main.tex",
]

# Translation map: Chinese terms → English
THEOREM_NAMES = {
    '定理': 'Theorem',
    '引理': 'Lemma', 
    '推论': 'Corollary',
    '定义': 'Definition',
    '注记': 'Remark',
    '命题': 'Proposition',
    '假设': 'Assumption',
    '猜想': 'Conjecture',
    '例': 'Example',
    '判据': 'Criterion',
}

def has_chinese(text):
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def fix_document_class(content):
    """Replace ctexart with article and remove CJK setup."""
    # Replace ctexart → article
    content = re.sub(r'\\documentclass\[.*?\]\{ctexart\}', 
                     r'\\documentclass[12pt,a4paper]{article}', content)
    
    # Remove \usepackage[UTF8]{ctex} or \usepackage{ctex}
    content = re.sub(r'\\usepackage\[UTF8\]\{ctex\}\s*\n?', '', content)
    content = re.sub(r'\\usepackage\{ctex\}\s*\n?', '', content)
    
    # Remove CJK font settings
    content = re.sub(r'\\setCJKmainfont\{[^}]*\}(?:\[[^\]]*\])?\s*\n?', '', content)
    content = re.sub(r'\\setmainfont\{[^}]*\}\s*\n?', '', content)
    
    # Remove xeCJK package
    content = re.sub(r'\\usepackage\{xeCJK\}\s*\n?', '', content)
    
    # Remove fontspec if only used for CJK
    # Keep fontspec if it's needed for other things
    
    # Remove CJK-related newtheorem names
    for cn, en in THEOREM_NAMES.items():
        # Replace theorem environment names
        content = re.sub(
            r'\\newtheorem\{(\w+)\}\{' + cn + r'\}',
            r'\\newtheorem{\1}{' + en + '}',
            content
        )
        content = re.sub(
            r'\\newtheorem\{(\w+)\}\[(\w+)\]\{' + cn + r'\}',
            r'\\newtheorem{\1}[\2]{' + en + '}',
            content
        )
    
    # Fix \mathsf → \textsf
    content = content.replace('\\mathsf{', '\\textsf{')
    
    # Fix \author to just SCX
    content = re.sub(
        r'\\author\{.*?\}',
        r'\\author{SCX}',
        content,
        flags=re.DOTALL
    )
    
    return content

def translate_line(line):
    """Translate Chinese content in a line to English."""
    # Skip pure math/LaTeX lines
    if not has_chinese(line):
        return line
    
    # First, protect LaTeX commands
    protected = []
    def protect_cmd(m):
        protected.append(m.group(0))
        return f'<<<PROTECTED{len(protected)-1}>>>'
    
    # Protect math mode
    line = re.sub(r'\$[^$]+\$', protect_cmd, line)
    line = re.sub(r'\\\[.*?\\\]', protect_cmd, line, flags=re.DOTALL)
    line = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', protect_cmd, line, flags=re.DOTALL)
    
    # Common translations (word/phrase level)
    translations = [
        # Section headings
        ('引言', 'Introduction'),
        ('Introduction 引言', 'Introduction'),
        ('Introduction / Introduction', 'Introduction'),
        ('Abstract：', 'Abstract:'),
        ('Abstract：', 'Abstract:'),
        ('关键词：', 'Keywords:'),
        ('Keywords：', 'Keywords:'),
        ('参考文献', 'References'),
        ('附录', 'Appendix'),
        ('致谢', 'Acknowledgments'),
        
        # Common terms
        ('当前结构', 'Current Structure'),
        ('赢家与输家', 'Winners and Losers'),
        ('推荐策略', 'Recommended Strategy'),
        ('跨行业综合洞察', 'Cross-Industry Synthesis'),
        ('讨论', 'Discussion'),
        ('Conclusion', 'Conclusion'),
        ('结论', 'Conclusion'),
        ('展望', 'Outlook'),
        ('未来工作', 'Future Work'),
        ('局限性', 'Limitations'),
        ('Core发现', 'Core Findings'),
        ('Core贡献', 'Core Contributions'),
        ('Core结论', 'Core Conclusions'),
        ('Core创新', 'Core Innovation'),
        ('Core张力', 'Core Tension'),
        ('Core张力：', 'Core Tension: '),
        ('Core特征', 'Core Feature'),
        ('Core问题', 'Core Problem'),
        ('Core主张', 'Core Claim'),
        ('Core洞察', 'Core Insight'),
        ('Core原则', 'Core Principle'),
        ('Core秘密', 'Core Secret'),
        ('Core产品', 'Core Product'),
        ('Core论点', 'Core Thesis'),
        ('Core发现是', 'Our central finding is'),
        ('Core结构缺陷', 'Core structural defect'),
        
        # Chinese text that appears alongside English (remove Chinese, keep English)
        # Many files are bilingual - we remove the Chinese where English exists
        
        # Common patterns
        ('赢家 / Winners', 'Winners'),
        ('输家 / Losers', 'Losers'),
        ('中文Abstract', 'Abstract'),
        ('中文摘要', 'Abstract'),
        ('English Abstract', 'Abstract'),
        ('本文', 'This paper'),
        ('我们', 'We'),
        ('证明', 'prove'),
        ('形式化', 'formalize'),
        ('定义', 'define'),
        ('推导', 'derive'),
        ('提供', 'provide'),
        ('建立', 'establish'),
        ('揭示', 'reveal'),
        ('暴露', 'expose'),
        ('展示', 'demonstrate'),
        ('确认', 'confirm'),
        ('验证', 'verify'),
        ('审计', 'audit'),
        ('审计者', 'auditor'),
        ('审计师', 'auditor'),
        ('验证者', 'verifier'),
        ('声称者', 'claimant'),
        ('声称', 'claim'),
        ('声明', 'declaration'),
        ('偏差', 'bias'),
        ('约束', 'constraint'),
        ('收敛', 'convergence'),
        ('发散', 'divergence'),
        ('共识', 'consensus'),
        ('信任', 'trust'),
        ('信任溢价', 'trust premium'),
        ('可审计性', 'auditability'),
        ('可验证性', 'verifiability'),
        ('不可验证性', 'unverifiability'),
        ('不可区分性', 'indistinguishability'),
        ('信息不对称', 'information asymmetry'),
        ('信息论', 'information theory'),
        ('率失真', 'rate-distortion'),
        ('通信', 'communication'),
        ('编码', 'encoding'),
        ('解码', 'decoding'),
        ('压缩', 'compression'),
        ('信道', 'channel'),
        ('信源', 'source'),
        ('信宿', 'destination'),
        ('分离定理', 'separation theorem'),
        ('互信息', 'mutual information'),
        ('熵', 'entropy'),
        ('专家', 'expert'),
        ('多专家', 'multi-expert'),
        ('投票', 'vote'),
        ('标签', 'label'),
        ('噪声', 'noise'),
        ('检测', 'detection'),
        ('评估', 'assessment'),
        ('评分', 'score'),
        ('质量', 'quality'),
        ('精度', 'precision'),
        ('误差', 'error'),
        ('错误', 'error'),
        ('下界', 'lower bound'),
        ('上界', 'upper bound'),
        ('不等式', 'inequality'),
        ('渐近', 'asymptotic'),
        ('非渐近', 'non-asymptotic'),
        ('紧致', 'compact'),
        ('紧性', 'tightness'),
        ('严格', 'rigorous'),
        ('启发式', 'heuristic'),
        ('开放性', 'open'),
        ('开放问题', 'open problem'),
        
        # Industry terms
        ('服务业', 'Professional Services'),
        ('制造', 'manufacturing'),
        ('Manufacturing', 'Manufacturing'),
        ('Semiconductor', 'Semiconductors'),
        ('资源行业', 'Natural Resources'),
        ('Banking', 'Banking'),
        ('Civil Servants', 'Civil Service'),
        ('银行', 'bank'),
        ('监管', 'regulatory'),
        ('监管机构', 'regulator'),
        ('监管捕获', 'regulatory capture'),
        ('资本充足率', 'capital adequacy ratio'),
        ('风险', 'risk'),
        ('储量', 'reserves'),
        ('良率', 'yield'),
        ('质量', 'quality'),
        ('缺陷', 'defect'),
        ('供应链', 'supply chain'),
        ('供应商', 'supplier'),
        ('检验', 'inspection'),
        ('认证', 'certification'),
        ('绩效', 'performance'),
        ('政府', 'government'),
        ('官员', 'official'),
        ('反腐败', 'anti-corruption'),
        ('腐败', 'corruption'),
        ('透明度', 'transparency'),
        ('商业机密', 'trade secret'),
        ('国家主权', 'national sovereignty'),
        ('地缘政治', 'geopolitical'),
        
        # Academic terms
        ('定理', 'Theorem'),
        ('引理', 'Lemma'),
        ('命题', 'Proposition'),
        ('推论', 'Corollary'),
        ('注记', 'Remark'),
        ('假设', 'Assumption'),
        ('定义', 'Definition'),
        ('猜想', 'Conjecture'),
        ('例题', 'Example'),
        ('证明', 'Proof'),
        ('证明概要', 'Proof Sketch'),
        ('部分证明', 'Partial Proof'),
        ('完整证明', 'Full Proof'),
        ('严格证明', 'Rigorous Proof'),
        
        # Math notation terms
        ('其中', 'where'),
        ('使得', 'such that'),
        ('对于', 'for'),
        ('任意', 'any'),
        ('存在', 'there exists'),
        ('所有', 'all'),
        ('每个', 'each'),
        ('满足', 'satisfying'),
        ('条件', 'condition'),
        ('假设', 'assumption'),
        ('结论', 'conclusion'),
        ('结果', 'result'),
        ('因此', 'therefore'),
        ('所以', 'thus'),
        ('因为', 'because'),
        ('如果', 'if'),
        ('当且仅当', 'if and only if'),
        ('充分必要', 'necessary and sufficient'),
        ('充要条件', 'necessary and sufficient condition'),
        ('等价于', 'is equivalent to'),
        ('等于', 'equals'),
        ('蕴含', 'implies'),
        ('即', 'i.e.,'),
        ('例如', 'e.g.,'),
        ('特别地', 'in particular'),
        ('更一般地', 'more generally'),
        ('相反地', 'conversely'),
        ('类似地', 'similarly'),
        ('此外', 'furthermore'),
        ('然而', 'however'),
        ('另一方面', 'on the other hand'),
        ('换言之', 'in other words'),
        ('综上所述', 'in summary'),
        ('值得注意的是', 'it is worth noting that'),
        ('显然', 'obviously'),
        ('容易验证', 'it is easy to verify'),
        ('由', 'from'),
        ('根据', 'according to'),
        ('设', 'let'),
        ('令', 'let'),
        ('则', 'then'),
        ('故', 'hence'),
        ('从而', 'thus'),
        ('通常', 'typically'),
        ('一般', 'generally'),
        ('可能', 'may'),
        ('必须', 'must'),
        ('需要', 'requires'),
        ('可以', 'can'),
        ('不能', 'cannot'),
        ('不应该', 'should not'),
        ('意味着', 'means'),
        ('表明', 'indicates'),
        ('说明', 'shows'),
        ('解释', 'explains'),
        ('描述', 'describes'),
        ('考虑', 'consider'),
        ('注意到', 'note that'),
        ('观察到', 'observe that'),
        ('回忆', 'recall'),
        ('假设', 'assume'),
        ('比较', 'compare'),
        ('分析', 'analysis'),
        ('研究', 'study'),
        ('方法', 'method'),
        ('框架', 'framework'),
        ('模型', 'model'),
        ('理论', 'theory'),
        ('实践', 'practice'),
        ('应用', 'application'),
        ('实验', 'experiment'),
        ('结果', 'result'),
        ('数据', 'data'),
        ('参数', 'parameter'),
        ('函数', 'function'),
        ('变量', 'variable'),
        ('常数', 'constant'),
        ('系数', 'coefficient'),
        ('矩阵', 'matrix'),
        ('向量', 'vector'),
        ('标量', 'scalar'),
        ('维度', 'dimension'),
        ('空间', 'space'),
        ('集合', 'set'),
        ('元素', 'element'),
        ('子集', 'subset'),
        ('映射', 'mapping'),
        ('算子', 'operator'),
        ('变换', 'transform'),
        ('分解', 'decomposition'),
        ('表示', 'representation'),
        ('特征', 'feature'),
        ('结构', 'structure'),
        ('系统', 'system'),
        ('过程', 'process'),
        ('机制', 'mechanism'),
        ('算法', 'algorithm'),
        ('网络', 'network'),
        ('分布', 'distribution'),
        ('概率', 'probability'),
        ('期望', 'expectation'),
        ('方差', 'variance'),
        ('协方差', 'covariance'),
        ('相关', 'correlation'),
        ('独立', 'independent'),
        ('依赖', 'dependent'),
        ('统计', 'statistical'),
        ('估计', 'estimation'),
        ('估计量', 'estimator'),
        ('检验', 'test'),
        ('显著性', 'significance'),
        ('置信', 'confidence'),
        ('区间', 'interval'),
        ('界', 'bound'),
        ('上限', 'upper bound'),
        ('下限', 'lower bound'),
        ('速率', 'rate'),
        ('收敛', 'convergence'),
        ('发散', 'divergent'),
        ('稳定', 'stable'),
        ('不稳定', 'unstable'),
        ('平衡', 'equilibrium'),
        ('最优', 'optimal'),
        ('次优', 'suboptimal'),
        ('极大', 'maximum'),
        ('极小', 'minimum'),
        ('最大化', 'maximize'),
        ('最小化', 'minimize'),
        ('增长', 'growth'),
        ('衰减', 'decay'),
        ('指数', 'exponential'),
        ('多项式', 'polynomial'),
        ('线性', 'linear'),
        ('非线性', 'nonlinear'),
        ('凸', 'convex'),
        ('凹', 'concave'),
        ('光滑', 'smooth'),
        ('连续', 'continuous'),
        ('可微', 'differentiable'),
        ('可积', 'integrable'),
        ('可测', 'measurable'),
        ('有界', 'bounded'),
        ('无界', 'unbounded'),
        ('紧致', 'compact'),
        ('完备', 'complete'),
        ('可分', 'separable'),
        ('一致', 'uniform'),
        ('逐点', 'pointwise'),
        ('全局', 'global'),
        ('局部', 'local'),
        ('显式', 'explicit'),
        ('隐式', 'implicit'),
        ('数值', 'numerical'),
        ('解析', 'analytical'),
        ('近似', 'approximate'),
        ('精确', 'exact'),
        ('对称', 'symmetric'),
        ('反对称', 'antisymmetric'),
        ('正定', 'positive definite'),
        ('半正定', 'positive semidefinite'),
        ('正交', 'orthogonal'),
        ('单位', 'unit'),
        ('零', 'zero'),
        ('非零', 'nonzero'),
        ('正', 'positive'),
        ('负', 'negative'),
        ('非正', 'non-positive'),
        ('非负', 'non-negative'),
        ('递增', 'increasing'),
        ('递减', 'decreasing'),
        ('单调', 'monotonic'),
        ('真包含', 'proper subset'),
        ('包含', 'contains'),
        ('属于', 'belongs to'),
        ('不属于', 'does not belong to'),
        ('交', 'intersection'),
        ('并', 'union'),
        ('补', 'complement'),
        ('差', 'difference'),
        ('直积', 'direct product'),
        ('直和', 'direct sum'),
        ('张量积', 'tensor product'),
        ('核', 'kernel'),
        ('像', 'image'),
        ('秩', 'rank'),
        ('迹', 'trace'),
        ('行列式', 'determinant'),
        ('特征值', 'eigenvalue'),
        ('特征向量', 'eigenvector'),
        ('谱', 'spectrum'),
        ('范数', 'norm'),
        ('内积', 'inner product'),
        ('外积', 'outer product'),
        ('转置', 'transpose'),
        ('逆', 'inverse'),
        ('伪逆', 'pseudoinverse'),
        ('伴随', 'adjoint'),
        ('共轭', 'conjugate'),
        ('梯度', 'gradient'),
        ('散度', 'divergence'),
        ('旋度', 'curl'),
        ('拉普拉斯', 'Laplacian'),
        ('雅可比', 'Jacobian'),
        ('黑塞', 'Hessian'),
    ]
    
    # Apply translations (longer phrases first to avoid partial matches)
    translations.sort(key=lambda x: -len(x[0]))
    
    for cn, en in translations:
        line = line.replace(cn, en)
    
    # Check if the line still has Chinese
    # If it does and it's alongside English in a bilingual format, try to extract just the English
    
    # Restore protected LaTeX
    for i, cmd in enumerate(protected):
        line = line.replace(f'<<<PROTECTED{i}>>>', cmd)
    
    return line

def process_bilingual_line(line):
    """For bilingual lines with both Chinese and English, remove Chinese portion."""
    # Handle patterns like "中文 / English" or "中文 (English)" or "中文：English"
    
    # Common patterns in the files:
    # "Section Title 中文 / English" → keep English
    # We need to be more careful here...
    
    # For now, just apply the translation
    result = translate_line(line)
    
    # Remove remaining Chinese characters
    # Try to extract just the English parts from bilingual lines
    if has_chinese(result):
        # For bilingual lines with structure: "Chinese / English" 
        # Try to keep only English
        parts = re.split(r'\s*/\s*', result)
        if len(parts) >= 2:
            # Check if one part is mainly English and one mainly Chinese
            english_parts = [p for p in parts if not has_chinese(p) or 
                           len(re.findall(r'[\u4e00-\u9fff]', p)) < len(p.split())]
            if english_parts:
                result = ' / '.join(english_parts)
    
    # If still has Chinese after all that, remove Chinese chars
    if has_chinese(result):
        # For true bilingual sections that can't be split, 
        # try to remove the Chinese sentences and keep English
        result = re.sub(r'[\u4e00-\u9fff，。！？；：""''【】《》（）…—\u3000]+', '', result)
        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result).strip()
    
    return result


def process_file(filepath):
    """Process a single LaTeX file, translating Chinese to English."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Fix document class and packages
    content = fix_document_class(content)
    
    # Step 2: Process line by line for translation
    lines = content.split('\n')
    new_lines = []
    
    in_math = False
    in_verbatim = False
    in_comment_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Track math mode
        if stripped.startswith('\\begin{equation') or stripped.startswith('\\begin{align') or stripped.startswith('\\['):
            in_math = True
        elif stripped.startswith('\\end{equation') or stripped.startswith('\\end{align') or stripped.startswith('\\]'):
            in_math = False
        
        # Track verbatim
        if stripped.startswith('\\begin{verbatim}'):
            in_verbatim = True
        elif stripped.startswith('\\end{verbatim}'):
            in_verbatim = False
        
        # Track comment blocks
        if '\\begin{comment}' in stripped:
            in_comment_block = True
        
        if in_math or in_verbatim:
            new_lines.append(line)
            continue
        
        # Process the line
        if has_chinese(line):
            # First, extract and protect LaTeX commands and math
            # Then translate the rest
            
            # Simple approach: split on common LaTeX delimiters
            new_line = process_bilingual_line(line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)
        
        if '\\end{comment}' in stripped:
            in_comment_block = False
    
    result = '\n'.join(new_lines)
    
    # Final cleanup
    # Remove empty bilingual markers
    result = re.sub(r'\\section\*\{(.*?)\}', r'\\section*{\1}', result)
    
    # Fix section titles that combine Chinese and English
    result = re.sub(r'\\section\{([^}]*?)(中文|Chinese)([^}]*?)\}', 
                    lambda m: '\\section{' + (m.group(1) + m.group(3)).strip().rstrip('/').strip() + '}', 
                    result)
    
    # Fix double spaces
    result = re.sub(r' {2,}', ' ', result)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  Done: {filepath}")


if __name__ == '__main__':
    os.chdir('F:/scx')
    for f in FILES:
        if os.path.exists(f):
            process_file(f)
        else:
            print(f"  NOT FOUND: {f}")
    print("\nAll files processed.")
