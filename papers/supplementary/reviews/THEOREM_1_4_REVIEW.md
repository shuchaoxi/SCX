# SCX 核心定理 1-4 审查报告

**日期**: 2026-07-01  
**审查者**: Hermes Agent (多文件全文审查)  
**审查范围**: `papers/theorems/`, `papers/scx_moe_gauge/main.tex`, `papers/yajie_protocol/main.tex`, `src/scx/valuation/state_value.py`, `src/scx/yajie.py`

---

## 总体评估

SCX 定理框架在核心洞察上**基本正确**。作者通过"诚实暴击"章节展示了多数限制的自觉。关键缺口：定理 2 缺形式化证明。定理 3 偏好域构造未闭合。定理 1 的 Hoeffding 常数偏保守但不致命。

---

## 定理 1: 多专家噪声检测

**来源**: AC-Theorem §3.1, state_value.py line 462

**陈述**: 
$$F_1 \geq 1 - \frac{1}{\eta}\sum_{s \in \mathcal{S}} \rho_s \cdot \exp(-2M\Delta_s^2)$$

**结论**: ✅ 正确
- Hoeffding 应用正确。使用双侧界用于单侧检验——保守但不致命（多估专家数最多 4 倍）
- 代码同时提供了 Chernoff/KL 版本（更紧）
- 独立性假设已正确陈述（条件独立于噪声状态 ε）
- H₁ 分布需要额外的条件化论证——可修复
- Δ_s = 0 退化情况已在代码中处理
- 1/η 奇点（η→0 时发散）是界的形式伪影

**常数问题**: 单侧检验最优界应为 $\exp(-M\Delta^2/2)$，不是 $\exp(-2M\Delta^2)$。因子 4 差异。

---

## 定理 2: 弱特征失效界

**来源**: state_value.py line 589

**陈述**:
$$F_1 \leq F_{1,\text{base}} + C_F \cdot \sqrt{2\delta}$$
其中 $\delta = I(\phi(X); S)$ 为特征-状态互信息

**结论**: ⚠️ 无形式化证明
- 代码实现了 `feature_strength_diagnostic`（sklearn mutual_info_classif 或直方图回退）
- $\sqrt{2\delta}$ 形式来源于 Fano 不等式 + 高斯近似的组合——推导**未写入任何文件**
- 互信息估计器本身无小样本理论保证
- **优先修复项**

---

## 定理 3: 老实人定理（噪声-困难不可区分性）

**来源**: AA-Theorem §2, CD-Theorem, HC-Theorem

**陈述**: 存在两个数据生成过程 $\mathcal{P}_{\text{noise}}$ 和 $\mathcal{P}_{\text{hard}}$，对所有可观测 SCX 量产生相同联合分布，但在 $\mathcal{P}_{\text{noise}}$ 中标签错误由噪声引起，在 $\mathcal{P}_{\text{hard}}$ 中所有标签正确但部分样本固有困难。

**结论**: 逻辑正确，构造有缺口
- **因果域（CD-Theorem）**: 证明完整——通过卷积构造 $\varepsilon' = \varepsilon + \beta z$
- **偏好域（AA-Theorem）**: 构造未闭合——两个世界分布不等式（$S_{\text{pref}}^{(A)} = 1/2 - \eta \neq \eta = S_{\text{pref}}^{(B)}$，除非 $\eta=1/4$）。论文自行标注了此缺口
- 隐藏假设：需要 $\eta \perp (\varepsilon, z)$（非仅 $\eta \perp z$），在 CD.tex 中作为 A2' 中程添加

---

## 定理 4': 精确常数极小极大最优性

**来源**: state_value.py lines 723-830

**陈述**: Bahadur-Rao 精确渐近：$1 - F_1 \sim \frac{C_{\min}}{\eta} \cdot \frac{e^{-M\kappa}}{\sqrt{2\pi M}}$

**结论**: ✅ 正确
- Chernoff 信息 $\kappa = \text{KL}(\theta^*\|p_0)$ 计算正确
- Bahadur-Rao 定理适用于伯努利分布（矩母函数在零点邻域有限）
- $C_{\min}$ 从鞍点到闭式的推导未在定理文件中展示——代码正确但缺中间引理
- 多状态聚合使用 min-$\kappa$ 支配——在大 $M$ 极限正确，有限 $M$ 需加权和

---

## 优先修复

1. **定理 2 形式化证明** —— 最高优先
2. **定理 3 偏好域构造闭合** —— 中优先
3. **定理 1 单侧界常数修正** —— 低优先（已有 Chernoff 版本替代）
