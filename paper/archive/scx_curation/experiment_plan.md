# Devirus-Distill 实验计划

> **论文目标**: Nature / Nature Computational Science  
> **核心叙事**: 提取多模型共识，蒸馏到一个轻量 student 中——在材料和药物两个世界同时成立  
> **硬件**: 1× RTX 4090 (24GB)  
> **时间线**: 6-12 个月

---

## Phase 0: 基础设施搭建 (Week 1-2)

### 0.1 环境安装
```bash
# Materials 侧
pip install mace-torch chgnet orb-models sevenn calorine deepmd-kit nequip
pip install ase pymatgen

# Life 侧
pip install rdkit
# DTI teacher 模型
pip install torch torch-geometric
```

### 0.2 数据准备
- [ ] 下载 Materials 侧 teacher 模型权重 (~8 GB)
- [ ] 下载 Life 侧 teacher 模型权重 (~1 GB)
- [ ] 下载 Materials Project 核心数据集 (~5 TB)
- [ ] 下载 C-MAPSS / SECOM 公开 benchmark

---

…[完整 Phase 1-6 见 D 盘原文件]…

---

## 里程碑时间线

```
Week 1-2:   环境 + 代码框架
Week 3-4:   Materials teacher 推理 + 分歧分析
Week 5-6:   三层对齐
Week 7-8:   NEP student 训练 + 对比实验
Week 9-12:  Life 世界完整流水
Week 13-14: 跨域分析
Week 15-20: 论文撰写 + 修改
Week 20+:   投稿 Nature
```

*Experiment Plan v1.0 — SCX Devirus-Distill Project*
