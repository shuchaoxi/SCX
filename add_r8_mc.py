#!/usr/bin/env python3
"""Add R8 final review record to Monte Carlo paper."""
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

record = """

---

## R8 审查记录 (Hostile Review Round 8) -- 终审

### 审查日期：2026-07-02

### 核查清单（R5+R6+R7 修复验证）：

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Cercis 函数符号 | 通过 | +lambda，Boltzmann 分布适定 |
| Situs 度规定义 | 通过 | 显式 Hessian 定义 |
| 运动方程符号 | 通过 | dp/dt 度量项为负号 |
| 蛙跳积分器 epsilon | 通过 | 所有 frac{2},frac{4} 已补 epsilon |
| 自适应步长 1/d | 通过 | 迹-特征值转换正确 |
| ESS 概率界 | 通过 | 去除无根据的 log(1/delta) 项 |
| MSE 指数界 | 通过 | B^{2t}->B^2*t |
| REX 混合时间公式 | 通过 | 公式重构 |
| MCMC 分类 | 通过 | 区分核心方法/辅助技术 |
| lambda 参数名冲突 | 通过 | lambda_max 区分 |
| 边界条件 (lambda->0) | 通过 | 已注明相变需 lambda>0 |
| Situs 度规稀疏结构 | 通过 | 已补充分块对角说明 |

### 终审发现
未发现剩余未修复的数学错误或逻辑漏洞。

### 裁决
蒙特卡洛论文在 R5-R7 中共发现并修复 **12 个问题**，
其中 **2 个关键错误**（Cercis 符号、运动方程符号）、
**5 个中等错误**（蛙跳、自适应步长、MSE 界、REX 公式、方法分类）、
**5 个边界/说明性问题**。

论文已达到收敛标准。**R8 终审通过。**
"""

content += record

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("R8 review record added")
