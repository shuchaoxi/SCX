---
tags: [TODO, 代码, 工程]
created: 2026-06-27
status: active
---

# 💻 代码工程 · 任务清单

---

## 一、SCX 核心修复

### C1: 修复 V(s) 循环定义 ✅ 已完成 (2026-06-27)

- [x] C1.1 deprecated 标记
- [x] C1.2 StateValue 重构（定理方法替代）
- [x] C1.3 所有引用更新
- [x] C1.4 测试通过 (427 tests)

**问题**：$V(s) = \bar{r}(s) \cdot \rho(s) \cdot L(s) \cdot [1-D(s)] \cdot \max_m SCX_m(s)$ 中 $L(s)$ 和 $D(s)$ 依赖 ground truth，形成循环。

- [x] **C1.1** 方案 B+C 混合 ✅ 2026-06-27: deprecated + 定理方法
- [x] **C1.2** StateValue 重构 ✅ 2026-06-27
- [x] **C1.3** 5 文件更新 ✅ 2026-06-27
- [x] **C1.4** 427 tests pass ✅ 2026-06-27

### C2: 命题代码同步 ✅ 文档已更新 (2026-06-27)

- [x] **C2.1** 命题 1 重构：regret 下界不影响 discovery.py（理论结果） ✅
- [x] **C2.2** 命题 3 证明：router.py 权重理论基础已验证 ✅
- [x] **C2.3** 命题 4 修复：compress.py bound 已用 C̄(s) 替代 r̄(s) ✅

---

## 二、论文级代码准备

### C3: Paper 2 可复现代码

- [ ] **C3.1** 整理 EGP gauge fixing 的独立可运行脚本
  - 需要：训练脚本、gauge fixing 脚本、评估脚本
  - 位置：`paper/paper1_mlip/code/`

- [ ] **C3.2** 确保所有 Paper 2 figures 可一键复现
  - `python reproduce_figures.py` → 生成全部 4 张图

- [ ] **C3.3** 准备 requirements.txt

### C4: SCX-Research 开源准备

- [ ] **C4.1** 决定开源范围
  - 论文复现所需的最小代码
  - 不含商业层（大规模 pipeline、dashboard 等）

- [ ] **C4.2** 清理代码
  - 移除商业层代码到 `scx-pro/` （不入开源仓库）
  - 统一 API 文档

- [ ] **C4.3** 准备示例 notebooks
  - `notebooks/01_scx_noise_detection.ipynb`
  - `notebooks/02_scx_compression.ipynb`
  - `notebooks/03_scx_expert_routing.ipynb`

- [ ] **C4.4** 选择开源许可证
  - 参考 `CodexKnowledge/整理_IP保护与开源策略与商业模式.md`

---

## 三、新模块规划（远期）

### 🌊 Spring — 持续涓流净化

> **三义合一**：泉（活水不断）+ 春（复苏新生）+ 弹簧（韧性回弹）

| 子模块 | 含义 | 功能 | 技术对应 |
|--------|------|------|---------|
| **Spring-Flow** | 泉 | 在线流式 SCX 诊断。对每个 incoming batch 做轻量级一致性检测，增量更新专家可靠性，标记异常。不停、不堵、不溢出。 | `core/online.py` → `OnlineSCXFramework` |
| **Spring-Grow** | 春 | 去噪重训 pipeline。雅洁扫完噪音 → Spring 在干净数据上重新训练，恢复被噪声伤害的权重。"春回大地"。 | Paper 1 的 AlN v3 去噪重训实验 |
| **Spring-Back** | 弹簧 | 抗中毒自动回弹。检测到数据分布异常 → 自动回滚到上一个安全 checkpoint → 恢复。压下去，弹回来。 | Governance Protocol 回退策略 + checkpoint 管理 |

**与雅洁的关系**：
```
雅洁 (Yajie)  →  一次性深度清理（scan → purify → bless）
Spring        →  持续涓流维护（watch → refresh → recover）
                 ┌── Spring-Flow: 在线监测（泉）
                 ├── Spring-Grow: 模型复苏（春）
                 └── Spring-Back: 弹性回滚（弹簧）
```

- [ ] **Spring-Flow**: 封装 `OnlineSCXFramework`，提供流式 `watch()` → `alert()` API
- [ ] **Spring-Grow**: 去噪重训 pipeline，`heal()` → 在雅洁清洗后的数据上重训
- [ ] **Spring-Back**: checkpoint 管理 + 自动回滚，`guard()` → 异常检测 → 自动恢复

---

## 四、代码质量

### C5: 测试增强

- [x] **C5.1** Yajie 模块 18 tests ✅ 2026-06-27
- [x] **C5.2** StateValue 定理方法 25 tests ✅ 2026-06-27
- [x] **C5.3** 427 tests 全部通过 ✅ 2026-06-27

### C6: 环境配置

- [ ] **C6.1** 在当前 Python 环境安装 scx
  ```bash
  pip install -e G:\Xiaogan_Supercomputing_data\SCX
  ```

- [ ] **C6.2** 验证 370 tests 全部通过

- [ ] **C6.3** 如果需要 GPU 实验，确认 EGP .venv 可用
  ```bash
  D:/SHEprogram/EGP/.venv/Scripts/python.exe -c "import torch; print(torch.__version__)"
  ```

---

## 四、文档

- [ ] **C7.1** 更新 README.md 反映当前版本状态
- [ ] **C7.2** 更新 API 文档（如使用了自动文档工具）
- [ ] **C7.3** 为 deleted/deprecated 的命题添加 deprecation warnings

---

*关联：[[NOW_理论]], [[NOW_论文]]*
