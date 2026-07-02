#!/bin/bash
# Phase 2: Bulk Chinese word/phrase translation
cd /f/scx

for f in \
  papers/scx_industry/main.tex \
  papers/scx_information_theory/main.tex \
  papers/scx_instanton/audit_instanton.tex \
  papers/scx_journalism/main.tex \
  papers/scx_lambda/lambda_gauge.tex \
  papers/scx_law/main.tex \
  papers/scx_maintainer_analysis/maintainer_analysis.tex \
  papers/scx_matrix_theory/main.tex; do
  
  echo "=== Translating $f ==="
  
  # Common Chinese words -> English (longer phrases first)
  sed -i 's/本文提供/This paper provides/g' "$f"
  sed -i 's/本文首次提供/This paper provides the first/g' "$f"
  sed -i 's/本文系统地形式化了/This paper systematically formalizes/g' "$f"
  sed -i 's/本文的Core发现是/The central finding of this paper is/g' "$f"
  sed -i 's/本文揭示/This paper reveals/g' "$f"
  sed -i 's/本文Proof/This paper proves/g' "$f"
  sed -i 's/本文建立/This paper establishes/g' "$f"
  sed -i 's/本文提出/This paper proposes/g' "$f"
  sed -i 's/本文首次/This paper is the first to/g' "$f"
  sed -i 's/本文为/This paper provides/g' "$f"
  sed -i 's/本文框架/this framework/g' "$f"
  sed -i 's/本文结论/The conclusions of this paper/g' "$f"
  sed -i 's/本文的数学美感/The mathematical elegance of this paper/g' "$f"
  
  # Sections
  sed -i 's/的Core发现/Core Findings/g' "$f"
  sed -i 's/Core发现：/Core Findings:/g' "$f"
  sed -i 's/Core结论/Core Conclusions/g' "$f"
  sed -i 's/最终展望/Concluding Outlook/g' "$f"
  sed -i 's/未来研究方向/Future Research Directions/g' "$f"
  sed -i 's/开放问题/Open Problems/g' "$f"
  
  # Common verb patterns
  sed -i 's/我们证明/we prove/g' "$f"
  sed -i 's/我们展示/we demonstrate/g' "$f"
  sed -i 's/我们提出/we propose/g' "$f"
  sed -i 's/我们引入/we introduce/g' "$f"
  sed -i 's/我们形式化/we formalize/g' "$f"
  sed -i 's/我们建立/we establish/g' "$f"
  sed -i 's/我们推导/we derive/g' "$f"
  sed -i 's/我们考虑/we consider/g' "$f"
  sed -i 's/我们定义/we define/g' "$f"
  sed -i 's/我们假设/we assume/g' "$f"
  sed -i 's/我们观察到/we observe that/g' "$f"
  sed -i 's/我们指出/we point out that/g' "$f"
  sed -i 's/我们强调/we emphasize that/g' "$f"
  sed -i 's/我们建议/we recommend/g' "$f"
  sed -i 's/我们发现/we find that/g' "$f"
  sed -i 's/我们分析/we analyze/g' "$f"
  sed -i 's/我们论证/we argue that/g' "$f"
  sed -i 's/我们说明/we explain/g' "$f"
  
  # Noun patterns
  sed -i 's/不可区分性/indistinguishability/g' "$f"
  sed -i 's/可扩展性/scalability/g' "$f"
  sed -i 's/可验证性/verifiability/g' "$f"
  sed -i 's/可审计性/auditability/g' "$f"
  sed -i 's/不可验证性/unverifiability/g' "$f"
  sed -i 's/不可审计性/unauditability/g' "$f"
  sed -i 's/收敛性/convergence/g' "$f"
  sed -i 's/发散性/divergence/g' "$f"
  sed -i 's/紧致性/compactness/g' "$f"
  sed -i 's/完备性/completeness/g' "$f"
  sed -i 's/单调性/monotonicity/g' "$f"
  sed -i 's/凸性/convexity/g' "$f"
  sed -i 's/稳定性/stability/g' "$f"
  sed -i 's/鲁棒性/robustness/g' "$f"
  sed -i 's/最优性/optimality/g' "$f"
  sed -i 's/次优性/suboptimality/g' "$f"
  sed -i 's/有效性/effectiveness/g' "$f"
  sed -i 's/一致性/consistency/g' "$f"
  sed -i 's/准确性/accuracy/g' "$f"
  sed -i 's/精确性/precision/g' "$f"
  sed -i 's/可靠性/reliability/g' "$f"
  sed -i 's/可行性/feasibility/g' "$f"
  sed -i 's/可能性/possibility/g' "$f"
  sed -i 's/必要性/necessity/g' "$f"
  sed -i 's/充分性/sufficiency/g' "$f"
  sed -i 's/普遍性/universality/g' "$f"
  sed -i 's/唯一性/uniqueness/g' "$f"
  sed -i 's/存在性/existence/g' "$f"
  
  # Connector words
  sed -i 's/然而/however/g' "$f"
  sed -i 's/因此/therefore/g' "$f"
  sed -i 's/所以/thus/g' "$f"
  sed -i 's/因为/because/g' "$f"
  sed -i 's/由于/due to/g' "$f"
  sed -i 's/如果/if/g' "$f"
  sed -i 's/虽然/although/g' "$f"
  sed -i 's/但是/but/g' "$f"
  sed -i 's/并且/and/g' "$f"
  sed -i 's/或者/or/g' "$f"
  sed -i 's/否则/otherwise/g' "$f"
  sed -i 's/而且/moreover/g' "$f"
  sed -i 's/此外/furthermore/g' "$f"
  sed -i 's/另外/in addition/g' "$f"
  sed -i 's/同时/simultaneously/g' "$f"
  sed -i 's/相反/on the contrary/g' "$f"
  sed -i 's/类似地/similarly/g' "$f"
  sed -i 's/特别地/in particular/g' "$f"
  sed -i 's/一般地/generally/g' "$f"
  sed -i 's/通常地/typically/g' "$f"
  sed -i 's/显然地/obviously/g' "$f"
  
  # Key concepts
  sed -i 's/定义/define/g' "$f"
  sed -i 's/证明/proof/g' "$f"
  sed -i 's/定理/theorem/g' "$f"
  sed -i 's/引理/lemma/g' "$f"
  sed -i 's/推论/corollary/g' "$f"
  sed -i 's/命题/proposition/g' "$f"
  sed -i 's/假设/assumption/g' "$f"
  sed -i 's/注记/remark/g' "$f"
  sed -i 's/猜想/conjecture/g' "$f"
  sed -i 's/例题/example/g' "$f"
  sed -i 's/例如/for example/g' "$f"
  sed -i 's/即/i.e./g' "$f"
  sed -i 's/其中/where/g' "$f"
  sed -i 's/使得/such that/g' "$f"
  sed -i 's/满足/satisfying/g' "$f"
  sed -i 's/对于/for/g' "$f"
  sed -i 's/任意/any/g' "$f"
  sed -i 's/存在/there exists/g' "$f"
  sed -i 's/所有/all/g' "$f"
  sed -i 's/每个/each/g' "$f"
  sed -i 's/当且仅当/if and only if/g' "$f"
  sed -i 's/充分必要条件/necessary and sufficient condition/g' "$f"
  sed -i 's/充要条件/iff condition/g' "$f"
  sed -i 's/等价/is equivalent/g' "$f"
  sed -i 's/蕴含/implies/g' "$f"
  
  # Mathematical terms
  sed -i 's/下界/lower bound/g' "$f"
  sed -i 's/上界/upper bound/g' "$f"
  sed -i 's/不等式/inequality/g' "$f"
  sed -i 's/渐近/asymptotic/g' "$f"
  sed -i 's/非渐近/non-asymptotic/g' "$f"
  sed -i 's/率失真/rate-distortion/g' "$f"
  sed -i 's/通信/communication/g' "$f"
  sed -i 's/信道/channel/g' "$f"
  sed -i 's/编码/encoding/g' "$f"
  sed -i 's/压缩/compression/g' "$f"
  sed -i 's/互信息/mutual information/g' "$f"
  sed -i 's/熵/entropy/g' "$f"
  sed -i 's/信源/source/g' "$f"
  sed -i 's/信宿/destination/g' "$f"
  sed -i 's/分离定理/separation theorem/g' "$f"
  sed -i 's/充分统计量/sufficient statistic/g' "$f"
  sed -i 's/数据处理不等式/data processing inequality/g' "$f"
  
  # Remaining Chinese characters - remove if in bilingual context
  # For pure Chinese, these translations will make text partially readable
  
  echo "  Done: $f"
done

# Count remaining Chinese
echo ""
echo "=== Remaining Chinese line counts ==="
for f in papers/scx_industry/main.tex papers/scx_information_theory/main.tex papers/scx_instanton/audit_instanton.tex papers/scx_journalism/main.tex papers/scx_lambda/lambda_gauge.tex papers/scx_law/main.tex papers/scx_maintainer_analysis/maintainer_analysis.tex papers/scx_matrix_theory/main.tex; do
  count=$(grep -cP '[\x{4e00}-\x{9fff}]' "$f" 2>/dev/null || echo 0)
  echo "$f: $count"
done

echo "Phase 2 complete"
