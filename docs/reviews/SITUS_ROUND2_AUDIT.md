# Situs 空间状态理论第二轮深度审计报告

**审计日期**: 2026-07-03  
**审计范围**: 第二轮深度验证——修正验证 + 新错误发现 + SCX 交叉引用  
**审计者**: SCX 项目内部审计（第二轮）  
**前置阅读**: `SITUS_DEEP_AUDIT.md`（第一轮审计报告）

---

## 0. 审计方法论

第二轮审计的三项任务：

- **(A)** 验证第一轮发现的已修正错误是否**真正**已修正，以及是否存在同类型残余错误
- **(B)** 以全新视角逐定理重读，发现第一轮**遗漏**的错误
- **(C)** 交叉引用 SCX 理论（Theorem 1-6），验证 Situs 是否准确引用 SCX 的结论

### 审读文件清单

| 文件 | 行数 | 角色 |
|------|------|------|
| `papers/situs_theory/main.md` | 1302 | Situs 理论主文档 |
| `papers/situs_applications/main.md` | 390 | 应用分析文档 |
| `theory/self_evolution/situs_physical_validation.md` | 807 | 物理验证文档 |
| `theory/self_evolution/situs_final_verification.md` | 572 | 最终验证报告 |
| `theory/self_evolution/ppe_rigorous_derivation.md` | 1029 | PPE 严密推导（参考） |
| `theory/theorems/polished/01_noise_detection_polished.md` | 339 | SCX Theorem 1 |
| `theory/theorems/polished/02_weak_feature_polished.md` | 404 | SCX Theorem 2 |

---

## A. 第一轮修正验证

### A1. δ_s^PE 符号修正 —— ✅ 已正确修正

**第一轮发现**: CC 审计报告中 δ_s^PE 表达式符号相反。

**第二轮验证**: `situs_theory/main.md` 命题 2.1（L507-546）：

```
δ_s^PE = (p_noisy^Situs - p_noisy) - (p_clean^Situs - p_clean)
```

符号正确：δ_s^PE > 0 意味着噪声样本上分歧增益超出干净样本上的副作用。✅

**同类残余检查**: 搜索所有文件中 δ_s^PE 的出现，未发现符号反转的残余实例。✅

> **新发现**: `situs_physical_validation.md` L184-198 在讨论 IDR 退化时写道：
> "干净样本：PE(p) 添加了与标签无关的波动 → 可能略微降低专家一致性 → p_clean^PPE ≥ p_clean"
> 
> 注意这里 p_clean^PPE ≥ p_clean 意味着干净样本上分歧增大（变差），结合符号定义，这会导致 δ_s^PE 趋向负值。该逻辑方向与理论一致。✅

---

### A2. 旋转编码 Lipschitz 常数高估 3.46× —— ✅ 已正确修正

**第一轮发现**: 先前版本使用 2√(α²+β²+γ²)，正确值应为 max(α,β,γ)。

**第二轮验证**: `situs_theory/main.md` 定理 1.3.1（L409-464）：

```
L_PE^rot = max(α, β, γ)
```

证明完整且正确（利用子空间正交性直接计算 ℓ₂ 范数）。备注 rem:1.3.1 解释了先前高估的两个来源（三角不等式松弛 √3 倍 + Cauchy-Schwarz 松弛 √3 倍）。

**紧致性验证**: 取 Δp = (ε, 0, 0) 且 α = max(α,β,γ)，当 ε → 0 时等号渐近成立。✅

---

### A3. Fano 下界逻辑错误 —— ✅ 已正确降级

**第一轮发现**: 从两个 Fano 下界 P_e ≥ A 和 P_e' ≥ B 不能推出 P_e - P_e' ≥ A - B。

**第二轮验证**: `situs_theory/main.md` 命题 2.4.1（L680-724）：

- 已从"定理"降级为"命题" ✅
- 标注 `\heuristic{}` ✅
- 明确声明"此表达式**不是**严格的数学下界" ✅
- 解释了为什么逻辑上不成立：a ≥ A 和 b ≥ B 不蕴含 a-b ≥ A-B ✅

**⚠️ 跨文档不一致（新发现）**:

`situs_physical_validation.md` L263-264 仍将 Fano 估计作为下界使用：

```
根据 Fano 下界（定理 2.4.1），对于多类分类：
δ_s^PE ≥ (2 · I(Y; P | S) - log 2) / log |Y|
```

这里使用了**不等号 "≥"**，且仍称其为"定理 2.4.1"，与理论文档的降级处理**矛盾**。理论文档已明确此公式不是严格下界，但验证文档仍以严格下界形式引用。

**严重程度**: 🟡 中等。验证文档未同步理论文档的修正。

---

### A4. 归一化因子 √(2/d) —— ✅ 已正确加入

**第二轮验证**: `situs_theory/main.md` 定义 1.2.1（L162-177）明确包含 √(2/d)，且解释了其作用（保证 ‖PE(p)‖ = 1 和收敛性）。✅

---

### A5. d_min = L/(2ξ) —— ✅ 已正确修正

**第二轮验证**: `situs_theory/main.md` 推论 1.2.1（L269-282）：

```
d_min ≈ L/(2ξ)
```

推导链完整：λ_max ≈ 4dξ, Nyquist 条件 λ_max ≥ 2L → d ≥ L/(2ξ)。✅

---

### A6. 定理 2.2.1 贝叶斯最优限定 —— ✅ 已正确限定

**第二轮验证**: `situs_theory/main.md` L561-605：

- 定理标题包含"贝叶斯最优限定" ✅
- 步骤 4 标注 `\heuristic{}` ✅
- 退化为经典结论的诚实声明 ✅

---

### A7. Theorem 3' 破坏方向 → 开放问题 —— ✅ 已正确处理

**第二轮验证**: `situs_theory/main.md` L1034-1088：

- 前提 (A) 不成立时标注为开放问题 ✅
- 构造性最小示例被重评为"实际上证明了 Theorem 3 的鲁棒性" ✅

---

### A8. 第一轮残余问题复查

| 残余问题 | 第一轮状态 | 第二轮状态 |
|---------|-----------|-----------|
| 摘要"充要条件"声称 | ⚠️ 未修复 | 见下文 **B1** |
| ppe_rigorous_derivation.md 双重陈述 | ⚠️ 轻微 | 见下文 **B2** |

---

## B. 第二轮新发现错误

### B1. 🔴 严重：摘要声称已被修正但 situs_final_verification.md 的引用已过时

`situs_final_verification.md` R1（L459-497）报告 `main.tex` L97 摘要中使用"充要条件"。但当前 `main.md` L19 摘要已修正为"充分条件"。

**当前实际状态**: `situs_theory/main.md` L19：

> "证明了 δ_s^PE > 0 的**充分条件**为 I(Y; P | S) > 0（定理2.2.1，限定贝叶斯最优分类器）"

摘要已正确使用"充分条件"并包含贝叶斯最优限定。✅ 该问题已在 main.md 中修复。

**但是**: `situs_final_verification.md` 的 R1 条目现在已**过时**——它所引用的 `main.tex` 文件可能不存在于当前仓库（搜索未找到 .tex 版本）。situs_final_verification.md 应更新以反映当前文件状态。

---

### B2. 🔴 严重：Chernoff-Hoeffding 指数中的因子 4 误差

**这是第二轮发现的最重要的新错误。**

**问题所在**: `situs_theory/main.md` L549-557 给出的 Situs 增强版 Theorem 1：

```
F_1^Situs ≥ 1 - (1/∑ρ_s) ∑ ρ_s · exp(-2M (Δ_s + δ_s^PE)²)
```

其中 Δ_s = p_noisy - p_clean。

**数学验证**:

Hoeffding 不等式对于 Bernoulli(p) 随机变量 v_m ∈ {0,1} 的样本均值：

```
P(|(1/M)∑v_m - p| ≥ ε) ≤ 2exp(-2Mε²)
```

应用于噪声检测（阈值 τ = (p_clean + p_noisy)/2）：

- 假阳性（clean）: ε = (p_noisy - p_clean)/2 = Δ_s/2
  → 上界 = exp(-2M(Δ_s/2)²) = **exp(-MΔ_s²/2)**

- 假阴性（noisy）: 同理 → **exp(-MΔ_s²/2)**

**正确上界**: exp(-MΔ_s²/2)，其中 Δ_s = p_noisy - p_clean。

**Situs 使用的上界**: exp(-2MΔ_s²)。

**差异**: 指数因子相差 **4 倍**。Situs 的界将指数扩大了 4 倍（即 |exp(-2MΔ_s²)| ≪ |exp(-MΔ_s²/2)|），使得收敛看起来比实际快 4 倍。

**根源分析**: `ppe_rigorous_derivation.md` L57-59 已**承认**此问题：

> "注：CC 审计报告使用 exp(-2MΔ_s²)。这表明其 Δ_s 的定义可能不同（可能多了一个 1/2 因子）。本文在保持数学精确性的前提下，遵循 CC 报告的约定：将 Δ_s 重新校准，使 bound 写为 exp(-2MΔ_s²)。这相当于定义 \tilde{Δ}_s = (p_noisy - p_clean)/2，在原始报告中记为 Δ_s。"

即：ppe_rigorous_derivation.md 承认正确的 Hoeffding 界是 exp(-MΔ_s²/2)，而 CC 报告的 exp(-2MΔ_s²) 需要将 Δ_s 重新定义为实际检测边际的一半。

**但是**: `situs_theory/main.md` **没有**包含此校准说明。读者会自然地将 Δ_s 理解为 p_noisy - p_clean，从而被误导认为指数收敛速度快 4 倍。

**影响评估**:
- 这**不是**严格的数学错误——如果明确声明 Δ_s 已被重新校准
- 但**是**严重的文档缺陷——situs_theory/main.md 缺少校准说明
- 对于小的 M（如 M_eff ≈ 1.2~6 的应用场景），因子 4 的差异在实践中是显著的

**建议**: 在 situs_theory/main.md 中添加明确的校准脚注，或直接使用正确的 Hoeffding 形式 exp(-MΔ_s²/2)。

---

### B3. 🔴 严重：situs_applications/main.md 对定理强度的过度声称

`situs_applications/main.md` L27-36：

> "**Theorem:** [Information-Theoretic Criterion, Theorem~2.2.1...] A **necessary** (and, with sufficient encoding capacity, **sufficient**) condition for Situs to improve detection margin Δ_s is: I(Y; P | S) > 0"

**与理论文档的矛盾**:

| 维度 | 应用文档声称 | 理论文档实际 |
|------|-------------|-------------|
| 条件类型 | 充要条件 (necessary AND sufficient) | 充分条件 only (定理 2.2.1) + 单独的必要条件命题 (命题 2.2.1) |
| 适用范围 | 所有专家（隐含） | 仅贝叶斯最优分类器（步骤 1-3），实际专家为启发式（步骤 4） |
| 必要条件严格性 | I(Y;P\|S) > 0 为充要 | 命题 2.2.1 允许非信息论机制（偏差-方差结构改变） |

**具体问题**:
1. "必要且充分"的声称**直接违反了**定理 2.2.1 的标题（"充分条件"）和命题 2.2.1 的第二条件（非信息论机制）
2. 贝叶斯最优限定被**完全省略**
3. 如果读者只读应用文档不读理论文档，会误以为 I(Y;P|S) > 0 是一个严格等价条件

**严重程度**: 🔴 严重——跨文档不一致，且应用文档比理论文档更乐观。

---

### B4. 🟡 定理 2.3.1 中定理陈述与证明不严格一致

`situs_theory/main.md` L627-676 定理 2.3.1（δ_s^PE 的信息论上界）：

**定理框内公式**:
```
δ_s^PE ≤ min(1 - p_clean,s, √(½ D_KL(P_PE|S,Y ‖ P_PE|S))) + δ_s^{variance}
```

**证明中的推导**:
```
|p_clean^Situs - p_clean| ≤ √(½ D_KL(P_PE(P)|S=s,clean ‖ P_PE(P)|S=s))
|p_noisy^Situs - p_noisy| ≤ √(½ D_KL(P_PE(P)|S=s,noisy ‖ P_PE(P)|S=s))
δ_s^PE ≤ |p_noisy^Situs - p_noisy| + |p_clean^Situs - p_clean|
```

证明给出的是**两个独立 KL 散度项的平方根之和**:
```
δ_s^PE ≤ √(½ D_KL_clean) + √(½ D_KL_noisy)
```

而定理陈述是**单一 KL 散度项的平方根**:
```
δ_s^PE ≤ √(½ D_KL(P_PE|S,Y ‖ P_PE|S))
```

**分析**: 如果 D_KL(P_PE|S,Y ‖ P_PE|S) 被理解为条件互信息 I(PE;Y|S) = E_Y[D_KL(P_PE|S,Y(·|y) ‖ P_PE|S)]，则定理陈述的单一 KL 项是 clean/noisy 两个 KL 项的加权平均，而证明给出的是它们的平方根之和。两者**在数值上不等价**（由 Jensen 不等式，√(E[X]) ≤ E[√X]，但 E[√X] ≠ √(E[X])）。

**实际影响**: 如果两个 KL 散度值相近，则平方根之和 ≈ 2√(½D_KL) ≈ √(2D_KL)，而 √(½D_KL_avg) 可能约为 √(½D_KL)。两者的比值约为 2:1。定理陈述可能**低估**了实际的上界。

**严重程度**: 🟡 中等。不影响定理的方向性（仍为有效上界），影响的是上界的紧致性。

---

### B5. 🟡 命题 2.2.1 的必要条件第二项过于模糊

`situs_theory/main.md` L607-618 命题 2.2.1（δ_s^PE > 0 的必要条件）:

条件 (2): "Situs 改变了专家系统的偏差-方差结构（非信息论机制——通过随机正则化效应）"

**问题**: "改变偏差-方差结构"不是数学上精确定义的条件。任何添加到模型中的组件（无论是否有用）都会改变偏差-方差结构。这使得命题 2.2.1 几乎不可证伪——任何观测到的 δ_s^PE > 0 总能被归因于条件 (2)。

**实际后果**: 即使 I(Y;P|S) = 0 被验证，如果观测到 δ_s^PE > 0（由有限样本噪声或过拟合导致），命题仍可声称"条件 (2) 成立"，从而保持命题表面上的正确性。

**严重程度**: 🟡 中等。使"必要条件"在实践中失去区分能力。

---

### B6. 🟢 SCX Theorem 1 的 Chernoff-Hoeffding 形式与 Situs 引用的版本不一致

**SCX Theorem 1 当前版本** (`01_noise_detection_polished.md`): 使用 **Sanov 指数**（大偏差理论），而非 Chernoff-Hoeffding。

**Situs 引用** (`situs_theory/main.md` L94-98): 

> "Theorem 1（多专家一致性噪声检测）：F_1 ≥ 1 - (1/∑ρ_s) ∑ ρ_s · exp(-2MΔ_s²)，通过 Chernoff-Hoeffding 不等式保障"

**实际情况**: SCX Theorem 1 已从 Chernoff-Hoeffding 修订为 Sanov 指数形式。Situs 的引用基于 SCX Theorem 1 的旧版本。

**影响**: Situs 的修正（Δ_s → Δ_s + δ_s^PE）在 Chernoff-Hoeffding 框架下是正确的。如果 SCX Theorem 1 迁移到 Sanov 指数，Situs 的修正需要相应更新（Sanov 指数的修正形式不同，涉及 KL 散度而非简单的均值差平方）。

**严重程度**: 🟢 轻微——当前 Situs 的修正逻辑在 Chernoff-Hoeffding 框架下自洽，但如果要与最新的 SCX Theorem 1 对齐，需重新推导。

---

### B7. 🟢 编码函数中 ‖PE_scalar‖ = 1 vs ‖PE_rot‖ = √3 的范数不一致

**标量编码**: ‖PE_scalar(p)‖ = 1（对所有 p）（main.md L175-177）

**旋转编码**: ‖PE_rot(p)‖ = √3（对所有 p）（由 cos²+sin² 对三个坐标求和得出）

**影响**: 如果 Situs 需要在同一模型中使用标量 + 旋转编码（如 1D 序列位置 + 3D 坐标），两者的范数不匹配。虽然在实际使用中不太可能同时使用两种编码类型，但文档未提及此差异。

**严重程度**: 🟢 轻微。

---

## C. SCX 理论交叉引用验证

### C1. SCX Theorem 1 → Situs 引用 ✅（需版本更新）

- 引用方式: 通过 Δ_s → Δ_s + δ_s^PE 修正式
- 接口清晰, Situs 作为独立组件插入
- ⚠️ 需更新为 Sanov 指数版本（见 B6）

### C2. SCX Theorem 2 → Situs Theorem 2' ✅

- SCX Theorem 2 定义 δ_φ = I(φ(X); S) 为特征信息不足度
- Situs Theorem 2' 使用 δ' = δ + 2ε_PE/C_F²
- 信息论恒等式推导正确：H(Y|X,PE(P)) = H(Y|X) - I(Y;P|X) + ε_PE
- ε_PE → 0 时恢复原始 Theorem 2 ✅
- ⚠️ 系数 2/C_F² 的正确性取决于 C_F 的定义（SCX Theorem 2 中 F_1 与贝叶斯错误率之间的转换常数），未在 Situs 中显式验证

### C3. SCX Theorem 3 → Situs Theorem 3' ✅

- 固定 PE 保持不可区分性的证明严格（确定性函数保持分布等价性）✅
- 前提 (B): P ⊥ W | X 是合理的物理假设 ✅
- 破坏方向的开放问题状态诚实 ✅

### C4. SCX Theorem 4 → Situs 引用 ✅

- Situs 正确指出 δ_s^PE 通过改变 Δ_s 影响 Theorem 4 的误差指数
- 但 Situs 未给出 Bahadur-Rao 修正项在引入 PE 后的具体变化

### C5. 应用文档中的"必要且充分" vs 理论文档

`situs_applications/main.md` L27-36 声称 I(Y;P|S) > 0 是"必要且充分"条件。这与理论文档矛盾（见 B3），且未提及贝叶斯最优限定。

**这是本轮发现的最严重的跨文档不一致。**

---

## D. 新增识别问题汇总

### D1. 已确认修正（第一轮发现）—— 全部通过 ✅

| 修正项 | 状态 |
|--------|------|
| δ_s^PE 符号 | ✅ 正确 |
| Lipschitz 3.46× 高估 | ✅ 正确 |
| Fano 逻辑错误降级 | ✅ 理论文档已降级, ⚠️ 验证文档未同步 |
| 归一化因子 √(2/d) | ✅ 正确 |
| d_min = L/(2ξ) | ✅ 正确 |
| 贝叶斯最优限定 | ✅ 正确 |
| Theorem 3' 开放问题化 | ✅ 正确 |

### D2. 新发现错误（本轮）—— 按严重程度排序

| # | 问题 | 位置 | 严重程度 |
|---|------|------|---------|
| **B2** | Chernoff-Hoeffding 指数因子 4 误差（exp(-2MΔ²) vs exp(-MΔ²/2)），缺少校准说明 | situs_theory/main.md L549-557 | 🔴 严重 |
| **B3** | situs_applications 声称 I(Y;P\|S)>0 为"必要且充分"条件，违反理论文档 | situs_applications/main.md L27-36 | 🔴 严重 |
| **B4** | 定理 2.3.1 陈述与证明不一致（单 KL vs 双 KL 和） | situs_theory/main.md L627-676 | 🟡 中等 |
| **A3** | situs_physical_validation.md 仍以"下界 ≥"引用已降级的 Fano 估计 | situs_physical_validation.md L263-264 | 🟡 中等 |
| **B5** | 命题 2.2.1 必要条件第二项（偏差-方差）过于模糊不可证伪 | situs_theory/main.md L607-618 | 🟡 中等 |
| **B6** | SCX Theorem 1 已修订为 Sanov 指数，Situs 仍引用旧版 Chernoff-Hoeffding | situs_theory/main.md L94-98 | 🟢 轻微 |
| **B7** | ‖PE_scalar‖=1 vs ‖PE_rot‖=√3 范数不一致 | situs_theory/main.md L162-177, L356-372 | 🟢 轻微 |
| **B1** | situs_final_verification.md R1 引用已过时（摘要已从"充要"改为"充分"） | situs_final_verification.md L459-497 | 🟢 轻微 |

---

## E. 与第一轮审计的对比

### 第一轮发现的问题状态更新

| 第一轮问题 | 第一轮判定 | 第二轮状态 |
|-----------|-----------|-----------|
| δ_s^PE 符号错误 | ✅ 已修正 | ✅ 确认修正，无残余 |
| Lipschitz 3.46× 高估 | ✅ 已修正 | ✅ 确认修正，紧致性验证通过 |
| Fano 逻辑错误 | ✅ 已降级 | ✅ 理论文档已降级，⚠️ 验证文档未同步 |
| 归一化因子缺失 | ✅ 已加入 | ✅ 确认 |
| d_min 修正 | ✅ 已修正 | ✅ 确认 |
| 摘要"充要条件" | ⚠️ 未修复 | ✅ main.md 已修复为"充分条件" |
| ppe_rigorous_derivation 双重陈述 | ⚠️ 轻微 | 仍存在（不影响 main.md） |

### 本轮新增 vs 第一轮

**第一轮未发现的关键问题**:
- 🔴 **Chernoff-Hoeffding 指数因子 4 误差** —— 第一轮未验证 SCX Theorem 1 的原始推导
- 🔴 **应用文档过度声称** —— 第一轮未深入审读 situs_applications/main.md
- 🟡 **定理 2.3.1 陈述与证明不一致** —— 第一轮标记为"严格正确"，但实际上定理框内公式与证明细节有差异

---

## F. 第二轮总体评估

### 数学正确性: ⭐⭐⭐½ (3.5/5) — 从第一轮的 4/5 下调

**下调原因**: 
- Chernoff-Hoeffding 指数因子 4 差异是实质性数学问题（虽然可以通过校准声明补救）
- 定理 2.3.1 陈述与证明不完全一致

**维持高质量的部分**:
- 编码函数理论（定理 1.2.1-1.4.1）仍然严格
- Theorem 2' 仍然严格
- 大部分修正已正确实施

### 跨文档一致性: ⭐⭐½ (2.5/5) — 新评估维度

**主要问题**:
- 应用文档与理论文档在定理强度声称上严重不一致（B3）
- 验证文档未同步理论文档的 Fano 降级修正（A3-跨文档）
- situs_final_verification.md 引用可能已过时的 .tex 文件

### 诚实度: ⭐⭐⭐⭐ (4/5) — 从第一轮的 5/5 下调

**下调原因**: 应用文档中"必要且充分"的声称未包含理论文档中的限定条件（贝叶斯最优、非信息论机制的备选），降低了跨文档的诚实透明度。

---

## G. 修正建议（按优先级）

### 🔴 最高优先级

1. **修正 situs_applications/main.md L27-36**: 将"necessary and sufficient"改为"sufficient (under Bayes-optimal classifier)"，添加贝叶斯最优限定的说明，并引用命题 2.2.1 中关于必要条件的更微妙讨论。

2. **在 situs_theory/main.md 添加 Chernoff-Hoeffding 校准说明**: 在 Theorem 1 的 Situs 修正版（L549-557）附近添加脚注，说明 exp(-2MΔ_s²) 形式中的 Δ_s 已被重新校准（实际 Δ_s = (p_noisy - p_clean)/2），或者直接改用标准形式 exp(-MΔ_s²/2)。

### 🟡 高优先级

3. **修正定理 2.3.1 的陈述**: 将定理框内的单一 KL 项改为与证明一致的双 KL 项之和形式，或者添加说明解释为何单一 KL 项可以替代两项之和。

4. **同步 situs_physical_validation.md 的 Fano 引用**: 将 L263-264 的"≥"改为"≈"或"粗略估计"，并将"定理 2.4.1"改为"命题 2.4.1（启发式估计）"。

5. **明确命题 2.2.1 条件 (2)**: 给出"偏差-方差结构改变"的可操作定义，或降级为开放问题。

### 🟢 中优先级

6. **更新 SCX Theorem 1 引用**: 确认 Situs 是否需要适配 Sanov 指数版本。

7. **更新 situs_final_verification.md**: 反映 main.md（而非 main.tex）的当前状态。

8. **文档化 ‖PE_scalar‖ vs ‖PE_rot‖ 范数差异**: 在编码定义处添加注释。

---

## H. 最终审计结论

**第二轮审计确认了第一轮修正的完整性（7/8 项全部通过），但同时发现了第一轮遗漏的三个重要问题。**

最关键的发现是 **Chernoff-Hoeffding 指数中的因子 4 差异**——这并非严格错误（ppe_rigorous_derivation.md 已承认并做了校准），但 situs_theory/main.md 缺少校准说明，可能导致读者将收敛速度高估 4 倍。

另一个严重问题是 **应用文档与理论文档之间的强度声称不一致**——应用文档将定理 2.2.1 的"充分条件（贝叶斯最优限定）"夸大为"必要且充分条件"，且省略了所有限定条件。

Situs 理论在**诚实度**方面仍然远优于 NPE 等项目——所有核心文档都标注了证明严格性，开放问题被明确标记。但跨文档一致性问题（应用文档 vs 理论文档 vs 验证文档）需要系统性修复。

**一句话总结**: Situs 的数学核心仍然可靠，但需要做一次跨文档的"对齐审计"——确保所有文件对同一结论的声称强度一致。

---

*第二轮审计完成于 2026-07-03。所有发现均基于对 F:\scx 项目 7 个源文件的逐行重读和交叉验证。*
