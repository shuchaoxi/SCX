---
tags: [时间线, 2026-06-15]
date: 2026-06-15
---

# 2026-06-15 · AlN Model B VASP 提交准备

## 当天产出

### AlN Model B VASP 提交集组织完成

基于前一天的结构生成计划，Agent 讨论 `20260615_aln_modelb_vasp_submission` 将 AlN Model B 的 VASP 结构组织为非破坏性的、manifest 驱动的分阶段提交集：

```
submission_sets/AlN_ModelB_v1/
├── MANIFEST.csv / MANIFEST.json
├── PRECHECK_REPORT.md
├── batches/
│   ├── 00_smoke (5 jobs)
│   ├── 01_minimal_static (21 jobs)
│   ├── 02_core_static_plus (41 jobs)
│   ├── 03_simple_defect_relax (14 jobs)
│   ├── 04_ood_static_deferred (15 jobs)
│   └── ...
```

### 推荐提交顺序

1. `00_smoke` → 验证 VASP/POTCAR/队列/提取管线
2. `01_minimal_static` → 首批干净 Model B 数据
3. `02_core_static_plus` → 论文核心静态扩展
4. `03_simple_defect_relax` → 缺陷修正数据

### 关键修复

- ASE + pymatgen 联合用于 POSCAR 解析和几何检查
- MLIP 静态作业 INCAR 统一设置：`LWAVE=.FALSE.`, `LCHARG=.FALSE.`, `LREAL=.FALSE.`, `LASPH=.TRUE.`, `ADDGRID=.TRUE.`, `ISYM=0`
- 表面 KPOINTS 修正（真空轴只有 1 个 k 点）
- Slurm 辅助脚本拒绝提交 `run_mode=hold` 作业

## 意义

这是 EGP 项目**第一次系统化的超算提交准备**，标志着从概念讨论进入实际 DFT 数据生成阶段。

## 关键文件

- [FINAL_SYNTHESIS.md](G:\仿真数据\egp_archive\agent_discussions\20260615_aln_modelb_vasp_submission\FINAL_SYNTHESIS.md)

## 相关笔记

- [[2026-06-14_EGP概念萌芽|← 前一天：概念萌芽]]
- [[2026-06-19_ACE专家代数|→ 下一突破：ACE 专家代数]]
