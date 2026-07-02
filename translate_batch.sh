#!/bin/bash
# Batch Chinese→English translation for Group D papers
cd /f/scx

# Common translate function
translate_file() {
  local f="$1"
  echo "Translating $f..."
  
  # === Remove CJK from bilingual patterns (Chinese/English → English) ===
  
  # Section headings with Chinese
  sed -i 's/\\section{引言 \/ Introduction}/\\section{Introduction}/g' "$f"
  sed -i 's/\\section{引言}/\\section{Introduction}/g' "$f"
  sed -i 's/\\subsection{信任的结构性缺陷 \/ The Structural Defect of Trust}/\\subsection{The Structural Defect of Trust}/g' "$f"
  
  # Abstract patterns
  sed -i 's/\\textbf{Abstract：}/\\textbf{Abstract:}/g' "$f"
  sed -i 's/\\textbf{中文Abstract：}/\\textbf{Abstract:}/g' "$f"
  sed -i 's/\\textbf{English Abstract:}/\\textbf{Abstract:}/g' "$f"
  sed -i 's/\\textbf{Keywords：}/\\textbf{Keywords:}/g' "$f"
  sed -i 's/Keywords：/Keywords:/g' "$f"
  
  # Common bilingual section patterns - remove Chinese, keep English
  sed -i 's/\\section{\([^}]*\) \/ \1}/\\section{\1}/g' "$f"
  
  # Theorem/Proof environments
  sed -i 's/\\begin{proof}\[.*证明.*\]/\\begin{proof}/g' "$f"
  sed -i 's/\\begin{proof}\[.*Proof.*\]/\\begin{proof}/g' "$f"
  
  # Bilingual table captions
  sed -i 's/\\caption{\(.*\) \/ \1}/\\caption{\1}/g' "$f"
  sed -i 's/\\caption{\(.*\)\\te.*\\te.*}/\\caption{\1}/g' "$f"
  
  # Common Chinese phrases → English
  sed -i 's/当前结构：/Current Structure: /g' "$f"
  sed -i 's/当前结构: /Current Structure: /g' "$f"
  sed -i 's/赢家与输家/Winners and Losers/g' "$f"
  sed -i 's/推荐策略/Recommended Strategy/g' "$f"
  sed -i 's/跨行业综合洞察/Cross-Industry Synthesis/g' "$f"
  sed -i 's/讨论：风险与挑战/Discussion: Risks and Challenges/g' "$f"
  sed -i 's/讨论：/Discussion: /g' "$f"
  sed -i 's/结论与行动框架/Conclusion and Action Framework/g' "$f"
  sed -i 's/最终展望/Concluding Outlook/g' "$f"
  sed -i 's/附录/Appendix/g' "$f"
  
  # Core findings etc
  sed -i 's/Core发现：/Core Findings: /g' "$f"
  sed -i 's/Core结论/Core Conclusions/g' "$f"
  sed -i 's/Core张力/Core Tension/g' "$f"
  sed -i 's/Core张力：/Core Tension: /g' "$f"
  sed -i 's/Core创新/Core Innovation/g' "$f"
  sed -i 's/Core主张/Core Claim/g' "$f"
  sed -i 's/Core洞察/Core Insight/g' "$f"
  sed -i 's/Core原则/Core Principle/g' "$f"
  sed -i 's/Core秘密/Core Secret/g' "$f"
  sed -i 's/Core发现是/Our central finding is/g' "$f"
  sed -i 's/Core结构缺陷/Core structural defect/g' "$f"
  sed -i 's/Core贡献/Core Contributions/g' "$f"
  
  # Common words
  sed -i 's/服务商/Service Provider/g' "$f"
  sed -i 's/声称者/Claimant/g' "$f"
  sed -i 's/验证者/Verifier/g' "$f"
  sed -i 's/审计者/Auditor/g' "$f"
  sed -i 's/审计师/Auditor/g' "$f"
  sed -i 's/声称/claim/g' "$f"
  sed -i 's/声明/declaration/g' "$f"
  sed -i 's/偏差/bias/g' "$f"
  sed -i 's/约束/constraint/g' "$f"
  sed -i 's/收敛/convergence/g' "$f"
  sed -i 's/共识/consensus/g' "$f"
  sed -i 's/信任/trust/g' "$f"
  sed -i 's/信任溢价/trust premium/g' "$f"
  sed -i 's/信息不对称/information asymmetry/g' "$f"
  
  # Remove standalone Chinese explanatory phrases in bilingual docs
  sed -i 's/（审计前评估是方向性的，不是决定性的）/(pre-audit assessment is directional, not dispositive)/g' "$f"
  sed -i 's/（不构成正式审计——只有\$M>1\$独立审计及公开日志才能做到）/(it does not constitute a formal audit---only \$M>1\$ independent audit with published logs can do that)/g' "$f"
  
  echo "  Done: $f"
}

# Process all files
for f in papers/scx_industry/main.tex papers/scx_information_theory/main.tex papers/scx_instanton/audit_instanton.tex papers/scx_journalism/main.tex papers/scx_lambda/lambda_gauge.tex papers/scx_law/main.tex papers/scx_maintainer_analysis/maintainer_analysis.tex papers/scx_matrix_theory/main.tex; do
  translate_file "$f"
done

echo "ALL DONE"
