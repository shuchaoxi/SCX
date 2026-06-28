# 明日推进 TODO

## 🔴 代码 — 理论落地（今日最大缺口）

### Yajie 核心实现
- [x] 实现 `yajie.py` 的 `fit()` 方法（目前抛 NotImplementedError）
- [x] 实现 state discovery → cluster → 多专家评分 完整管道
- [x] 实现 Cercis Score: S(s) = Q(s) + η(t)·N(s)
- [x] 输出：clean / noisy / ambiguous 三分类
- [x] 加固：日志输出 + 边缘案例修复 + 18 个测试

### Spring 验证
- [x] 用合成数据跑 Spring 迭代 20 轮（spring.py 已有壳）
- [x] 验证：M_t 单调增长 + η(t) 衰减 + S_t 收敛
- [x] 画 Lyapunov 下降曲线
- [x] 记录收敛速率 → 与理论 O(t^{-a}) 对比
- [x] 标签噪声对比实验：20% 噪声率 + 4 面板对比图

### MLIP 实验
- [ ] 等超算 AlN 数据到 → 运行 scx_method 管道
- [ ] Yajie 评分 Materials Project 数据（等 GPU）
- [ ] 验证 Theorem 1 的 FPR bound

---

## ✅ 2026-06-29 下午完成
- [x] Yajie.fit() 加固：日志/进度输出 + 边缘案例修复 + 18 新测试
- [x] Spring 噪声对比实验：20% 标签噪声 + 清洁/噪声 4 面板对比图
- [x] Paper 9 LLM 实验脚本：3 mock LLM × 200 题 → Yajie 共识表 + CSV 导出

---

## 🟡 Paper 9 最小验证实验
- [ ] 下载 Llama-3-8B / Mistral-7B / Qwen-7B
- [ ] 准备 100 个 MMLU 问题（真实数据）
- [x] 写脚本：3 模型各自回答 → Yajie 共识 → 表格
- [ ] 跑实验（真实模型）
- [ ] 数据塞进 Paper 9 LaTeX

---

## 🟢 Paper 9 正文完善
- [ ] 验证实验数据更新
- [ ] §4.5 与实验结果对齐

---

## ✅ 今日已完成
- [x] Yajie 定理 (Thm 1-3) + 抛光
- [x] Spring 定理 (SE-1/2) + Lyapunov 闭合
- [x] Spring LaTeX 论文 (13pp, 可编译)
- [x] 协议论文 (博弈论 17 层)
- [x] 综述 (双引擎架构, 8 领域)
- [x] Paper 5 LaTeX (策展-探索, 5.5K词)
- [x] Paper 7 分类学理论 + 内在可解释性
- [x] Paper 9 最小验证实验设计
- [x] Anthropic 批评 + 达摩克利斯 + 耿同学 + 自我怀疑
- [x] spring.py (1551 行) + yajie.py (355 行) + HIV 审计
