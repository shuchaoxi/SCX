#!/usr/bin/env python3
"""Add R6 review record to Monte Carlo paper."""
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

record = """

---

## R6 审查记录 (Hostile Review Round 6)

### 审查日期：2026-07-02

### 跨域一致性与深层问题：

1. **方法分类不准确**：论文声称"五个 MCMC 方法"，但热力学积分(TI)不是
   独立 MCMC 方法（它是基于 MCMC 后处理的校准技术），收敛诊断更不是采样方法。
   修正描述为"五个互补的采样与推断方法"，明确区分核心MCMC方法(HMC,SMC,REX)
   与辅助技术(TI,诊断)。

2. **自适应步长参数名冲突**：自适应步长公式中的 lambda_ 与 Cercis
   定义中的 lambda 参数名相同，可能混淆。修正为 lambda_{max}，
   与论文中的用法一致。

3. **Situs 度量与 Cercis 的一致性验证**：修正后 Cercis(E) 的 Hessian
   矩阵 h_{ij,kl} = delta_{ik}delta_{jl} + 2lambda 点 delta_{ik}，
   确保 Situs 度规正定性，验证通过。

4. **数值示例无实际验证输出**：m=5, n=3 的示例只列出了预期结果而无
   实际数值输出。建议补充 verification script 的实际运行结果作为附录。

### 裁决
R6 发现 4 个问题，3 个已修复，1 个（缺少实际验证输出）作为已知记录。
通过 R6 审查。
"""

content += record

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("R6 record added")
