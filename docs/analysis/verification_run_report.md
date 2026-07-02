# SCX Verification Run Report / SCX 验证运行报告

**Generated / 生成时间:** 2026-07-02 13:02:49

**Total Scripts / 脚本总数:** 32  
**Passed / 通过:** 30 | **Failed / 失败:** 2

---

## Detailed Results / 详细结果

| # | Script / 脚本 | Paper / 论文 | Lines / 行数 | Result / 结果 | Time / 耗时 | Errors / 错误 |
|---|---|---|---|---|---|---|
| 1 | `verify_acad_mdta_ilh.py` | scx_acad_mdta_ilh | 780 | PASS | 5s | - |
| 2 | `verify_audit_economics.py` | scx_audit_economics | 793 | PASS | 2s | - |
| 3 | `verify_business.py` | scx_business | 830 | PASS | 1s | - |
| 4 | `verify_capstone.py` | scx_capstone | 914 | PASS | 1s | - |
| 5 | `verify_civilization.py` | scx_civilization | 701 | PASS | 12s | - |
| 6 | `verify_community.py` | scx_community | 1217 | PASS | 1s | - |
| 7 | `verify_company_valuation.py` | scx_company_valuation | 664 | PASS | 1s | - |
| 8 | `verify_environment.py` | scx_environment | 742 | PASS | 1s | - |
| 9 | `verify_common.py` | scx_gauge_formalized | 1582 | PASS | 1s | - |
| 10 | `verify_gauge.py` | scx_gauge_formalized | 775 | PASS | 0s | - |
| 11 | `verify_geopolitics.py` | scx_geopolitics | 977 | FAIL | 1s |                              ^^^^^^^^^^^^^^^^^^^^^^^^^^   File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_geopoliticserify_geopolitics.py", line 406, in verify_audit_trust_curve     f"{sovereignty_costs[i]:12.4f} {premiums[i]:12.4f}")                                     ~~~~~~~~^^^ IndexEr |
| 12 | `verify_goodhart.py` | scx_goodhart | 724 | PASS | 42s | - |
| 13 | `verify_grand_unification.py` | scx_grand_unification | 919 | PASS | 1s | - |
| 14 | `verify_industry.py` | scx_industry | 927 | PASS | 1s | - |
| 15 | `verify_common.py` | scx_instanton | 1582 | PASS | 1s | - |
| 16 | `verify_tda.py` | scx_instanton | 868 | PASS | 1s | - |
| 17 | `verify_lambda.py` | scx_lambda | 757 | PASS | 2s | - |
| 18 | `verify_maintainer_analysis.py` | scx_maintainer_analysis | 773 | PASS | 1s | - |
| 19 | `verify_meta_audit.py` | scx_meta_audit | 635 | PASS | 2s | - |
| 20 | `verify_open_problems.py` | scx_open_problems | 796 | PASS | 15s | - |
| 21 | `verify_protocol_governance.py` | scx_protocol_governance | 983 | PASS | 1s | - |
| 22 | `verify_common.py` | scx_quantum_audit | 1582 | PASS | 1s | - |
| 23 | `verify_quantum.py` | scx_quantum_audit | 787 | PASS | 0s | - |
| 24 | `verify_resistance.py` | scx_resistance | 875 | PASS | 1s | - |
| 25 | `verify_S_operator.py` | scx_S_operator | 1025 | FAIL | 1s |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^   File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_S_operatorerify_S_operator.py", line 297, in verify_national_potential     r = compute_national_potential(**noisy_data)         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ TypeError: compute_nation |
| 26 | `verify_common.py` | scx_singularity | 1582 | PASS | 1s | - |
| 27 | `verify_singularity.py` | scx_singularity | 971 | PASS | 2s | - |
| 28 | `verify_social_media.py` | scx_social_media | 776 | PASS | 7s | - |
| 29 | `verify_world_government.py` | scx_world_government | 819 | PASS | 2s | - |
| 30 | `verify_common.py` | verify_common.py | 1582 | PASS | 1s | - |
| 31 | `verify_quantum.py` | theory_explorations | 730 | PASS | 5s | - |
| 32 | `verify_turbulence.py` | theory_explorations | 1192 | PASS | 10s | - |
---

## Failed Scripts Detail / 失败脚本详情

### 11. `verify_geopolitics.py` (scx_geopolitics)

- **RC:** 1
- **Time:** 1s
```

██████████████████████████████████████████████████████████████████████
█  SCX 地缘政治论文 - 全面验证
█  SCX Geopolitics Paper - Comprehensive Verification
██████████████████████████████████████████████████████████████████████
======================================================================
验证A: 中美相互审计均衡支付矩阵
Verify A: Mutual Audit Equilibrium Payoff Matrix US vs China
======================================================================

支付矩阵 (d_US=0.5, d_CN=0.5):
支付矩阵 / Payoff Matrix (d_US=0.5, d_CN=0.5):

   Profile |    US Payoff    CN Payoff
  ----------------------------------------
        AA |        0.250        0.500
        AN |        1.300        1.550
        NA |        3.200        2.200
        NN |        5.700        4.750

纯策略纳什均衡 / Pure-Strategy Nash Equilibria:
  NN: US=5.700, CN=4.750

混合策略纳什均衡 / Mixed-Strategy Nash Equilibrium:
  p* (US审计概率/Audit prob) = 1.0000
  q* (CN审计概率/Audit prob) = 1.0000
  EU_US = 0.2500
  EU_CN = 0.5000

混合均衡无差异验证 / Mixed Equilibrium Indifference Check:
  US: EU(Audit)=0.2500, EU(Not)=3.2000, 差异/Diff=2.950000
  CN: EU(Audit)=0.5000, EU(Not)=1.5500, 差异/Diff=1.050000

审计深度对均衡的影响 / Audit Depth Impact on Equilibrium:
   depth |      p*_US      q*_CN      EU_US      EU_CN      Pure NE
  -----------------------------------------------------------------
    0.10 |     0.0000     0.0000      5.700      4.750       ['NN']
    0.20 |     0.0000     0.0000      5.700      4.750       ['NN']
    0.30 |     0.0000     0.0000      5.700      4.750       ['NN']
    0.40 |     0.0000     0.0000      5.700      4.750       ['NN']
    0.50 |     1.0000     1.0000      0.250      0.500       ['NN']
    0.60 |     0.9014     1.0000      0.963      1.135       ['NN']
    0.70 |     0.6601     1.0000      1.677      1.568       ['NN']
    0.80 |     0.5402     0.8972      1.950      1.709 ['AA', 'NN']
    0.90 |     0.4669     0.7679      2.060      1.743 ['AA', 'NN']
    1.00 |     0.4163     0.6797      2.098      1.732 ['AA', 'NN']

最佳响应函数 / Best Response Functions:

  US Best Response to CN audit probability q:
    q_CN |    EU(Audit)      EU(Not)     Best
  ---------------------------------------------
    0.00 |       1.3000       5.7000      Not
    0.05 |       1.2475       5.5750      Not
    0.10 |       1.1950       5.4500      Not
    0.15 |       1.1425       5.3250      Not
    0.20 |       1.0900       5.2000      Not
    0.25 |       1.0375       5.0750      Not
    0.30 |       0.9850       4.9500      Not
    0.35 |       0.9325       4.8250      Not
    0.40 |       0.8800       4.7000      Not
    0.45 |       0.8275       4.5750      Not
    0.50 |       0.7750       4.4500      Not
    0.55 |       0.7225       4.3250      Not
    0.60 |       0.6700       4.2000      Not
    0.65 |       0.6175       4.0750      Not
    0.70 |       0.5650       3.9500      Not
    0.75 |       0.5125       3.8250      Not
    0.80 |       0.4600       3.7000      Not
    0.85 |       0.4075       3.5750      Not
    0.90 |       0.3550       3.4500      Not
    0.95 |       0.3025       3.3250      Not
    1.00 |       0.2500       3.2000      Not

  CN Best Response to US audit probability p:
    p_US |    EU(Audit)      EU(Not)     Best
  ---------------------------------------------
    0.00 |       2.2000       4.7500      Not
    0.05 |       2.1150       4.5900      Not
    0.10 |       2.0300       4.4300      Not
    0.15 |       1.9450       4.2700      Not
    0.20 |       1.8600       4.1100      Not
    0.25 |       1.7750       3.9500      Not
    0.30 |       1.6900       3.7900      Not
    0.35 |       1.6050       3.6300      Not
    0.40 |       1.5200       3.4700      Not
    0.45 |       1.4350       3.3100      Not
    0.50 |       1.3500       3.1500      Not
    0.55 |       1.2650       2.9900      Not
    0.60 |       1.1800       2.8300      Not
    0.65 |       1.0950       2.6700      Not
    0.70 |       1.0100       2.5100      Not
    0.75 |       0.9250       2.3500      Not
    0.80 |       0.8400       2.1900      Not
    0.85 |       0.7550       2.0300      Not
    0.90 |       0.6700       1.8700      Not
    0.95 |       0.5850       1.7100      Not
    1.00 |       0.5000       1.5500      Not

惩罚强度敏感性 / Penalty Strength Sensitivity:
  penalty=3: p*=0.000, q*=0.000, EU_US=5.70, EU_CN=4.75
  penalty=5: p*=1.000, q*=1.000, EU_US=0.25, EU_CN=0.50
  penalty=7: p*=1.000, q*=1.000, EU_US=0.25, EU_CN=0.50
  penalty=10: p*=1.000, q*=1.000, EU_US=0.25, EU_CN=0.50
  penalty=15: p*=1.000, q*=0.946, EU_US=0.31, EU_CN=0.56

成本不对称分析 / Cost Asymmetry Analysis:
  c_US/c_CN=0.5: p*=1.000, q*=1.000
  c_US/c_CN=0.8: p*=1.000, q*=1.000
  c_US/c_CN=1.0: p*=1.000, q*=1.000
  c_US/c_CN=1.2: p*=1.000, q*=1.000
  c_US/c_CN=1.5: p*=1.000, q*=1.000

[验证A完成 / Verify A Complete] ✓

摘要/Summary A: 中美审计博弈, 纯策略NE=1, 混合p*=1.000, q*=1.000

======================================================================
验证B: 审计深度vs信任溢价曲线
Verify B: Audit Depth vs Trust Premium Curve
======================================================================

审计深度-信任溢价关系 / Audit Depth vs Trust Premium:

     Depth |   Trust Gain   Audit Cost     Sov Cost  Net Premium
  -----------------------------------------------------------------
Traceback (most recent call last):
  File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_geopoliticserify_geopolitics.py", line 977, in <module>
    main()
  File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_geopoliticserify_geopolitics.py", line 952, in main
    opt_depth, opt_premium = verify_audit_trust_curve()
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_geopoliticserify_geopolitics.py", line 406, in verify_audit_trust_curve
    f"{sovereignty_costs[i]:12.4f} {premiums[i]:12.4f}")
                                    ~~~~~~~~^^^
IndexError: invalid index to scalar variable.
```

### 25. `verify_S_operator.py` (scx_S_operator)

- **RC:** 1
- **Time:** 1s
```

██████████████████████████████████████████████████████████████████████
█  SCX S算子论文 - 全面验证
█  SCX S-Operator Paper - Comprehensive Verification
██████████████████████████████████████████████████████████████████████
======================================================================
验证A: 国家潜力计算 (GDP/基尼系数/预期寿命)
Verify A: National Potential (GDP/Gini/Life Expectancy)
======================================================================

国家潜力得分 / National Potential Scores:
  Rank  Country  Potential        Q        N   Q_econ    Q_soc  Q_innov
  ---------------------------------------------------------------------------
     1       SG     0.8382   0.7552   0.2766   0.8434   0.6811   0.7118
     2       KR     0.8316   0.7716   0.2000   0.6817   0.7299   0.9331
     3       US     0.7887   0.7101   0.2618   0.6848   0.6158   0.8383
     4       AE     0.7869   0.7113   0.2519   0.7765   0.7332   0.6024
     5       DE     0.7840   0.7357   0.1609   0.7197   0.7106   0.7822
     6       NO     0.7835   0.7041   0.2645   0.6506   0.7551   0.7244
     7       JP     0.7795   0.7083   0.2375   0.6385   0.7257   0.7838
     8       GB     0.7627   0.7015   0.2040   0.6675   0.6890   0.7592
     9       FR     0.7577   0.6942   0.2114   0.6679   0.7184   0.7051
    10       CN     0.7308   0.6540   0.2560   0.6642   0.6441   0.6504
    11       RU     0.6583   0.5884   0.2330   0.6209   0.6175   0.5158
    12       IN     0.6317   0.5440   0.2923   0.6002   0.6016   0.4115
    13       BR     0.6181   0.5454   0.2423   0.5869   0.5205   0.5149
    14       NG     0.5550   0.4685   0.2883   0.5344   0.4948   0.3543
    15       ZA     0.5323   0.4709   0.2048   0.5742   0.3647   0.4392

分量分解详情 / Component Decomposition Details:
  US:
    GDP_norm=0.977, Gini_norm=0.585, Life_norm=0.688
    Q_economic=0.685, Q_social=0.616, Q_innovation=0.838
    Total Q=0.710, N=0.262, Potential=0.789
  CN:
    GDP_norm=0.821, Gini_norm=0.618, Life_norm=0.705
    Q_economic=0.664, Q_social=0.644, Q_innovation=0.650
    Total Q=0.654, N=0.256, Potential=0.731
  SG:
    GDP_norm=0.984, Gini_norm=0.614, Life_norm=0.838
    Q_economic=0.843, Q_social=0.681, Q_innovation=0.712
    Total Q=0.755, N=0.277, Potential=0.838
  IN:
    GDP_norm=0.683, Gini_norm=0.643, Life_norm=0.505
    Q_economic=0.600, Q_social=0.602, Q_innovation=0.412
    Total Q=0.544, N=0.292, Potential=0.632
  NO:
    GDP_norm=0.989, Gini_norm=0.723, Life_norm=0.830
    Q_economic=0.651, Q_social=0.755, Q_innovation=0.724
    Total Q=0.704, N=0.264, Potential=0.783

GDP边际贡献分析 / GDP Marginal Contribution:
  GDP=  5000: Potential=0.6428, Q_econ=0.5711, Q_innov=0.5699
  GDP= 15000: Potential=0.6823, Q_econ=0.6188, Q_innov=0.6176
  GDP= 30000: Potential=0.7079, Q_econ=0.6489, Q_innov=0.6477
  GDP= 50000: Potential=0.7270, Q_econ=0.6711, Q_innov=0.6699
  GDP= 80000: Potential=0.7447, Q_econ=0.6915, Q_innov=0.6903

基尼系数边际贡献分析 / Gini Marginal Contribution:
  Gini=0.25: Potential=0.7317, Q_social=0.7125
  Gini=0.30: Potential=0.7195, Q_social=0.6775
  Gini=0.35: Potential=0.7079, Q_social=0.6425
  Gini=0.45: Potential=0.6861, Q_social=0.5725
  Gini=0.55: Potential=0.6663, Q_social=0.5025
  Gini=0.65: Potential=0.6485, Q_social=0.4325

预期寿命边际贡献分析 / Life Expectancy Marginal Contribution:
  Life=55: Potential=0.6799, Q_social=0.4925
  Life=65: Potential=0.6886, Q_social=0.5675
  Life=72: Potential=0.7008, Q_social=0.6200
  Life=78: Potential=0.7161, Q_social=0.6650
  Life=85: Potential=0.7392, Q_social=0.7175

排名稳定性 (Bootstrap) / Ranking Stability:
Traceback (most recent call last):
  File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_S_operatorerify_S_operator.py", line 1025, in <module>
    main()
  File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_S_operatorerify_S_operator.py", line 988, in main
    nat_results = verify_national_potential()
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "G:\Xiaogan_Supercomputing_data\SCX\papers\scx_S_operatorerify_S_operator.py", line 297, in verify_national_potential
    r = compute_national_potential(**noisy_data)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: compute_national_potential() got an unexpected keyword argument 'gdp'
```

## Summary / 总结

- Total verify scripts executed: **32**
- All passed: **NO**
- Run time: 2026-07-02 13:02:49
