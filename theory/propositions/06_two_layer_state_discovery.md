# Proposition 6: Error-Driven State Discovery

> 最优状态划分不是由人类预设的，而是在误差相关特征子空间中自动发现的。状态应由"模型在哪里失败"来定义，而非"人类觉得什么重要"。

---

## 1 Statement

### 1.1 正式陈述

最优状态划分 $\mathcal{S}^*$ 不是由人类预设的，而是在误差相关特征子空间中自动发现的。

具体地，给定 Layer 1 编码 $\varphi_1$ 和 residual vector $r$，状态应该在与 $r$ 最相关的 $\varphi_1$ 维度子集中聚类：

$$\mathcal{S}^* = \text{Cluster}(\varphi_1[:, \text{top\_dims}], K)$$

其中：

$$\text{top\_dims} = \text{argsort}(\text{MI}(\varphi_1[:, j], r))$$

即选择与残差 $r$ 互信息最大的 $\varphi_1$ 维度子集作为聚类空间。

### 1.2 两层描述符体系

**第一层描述符（研究人员提供）**：材料的"身份标签"
- 元素种类、化学计量比、晶体结构
- 温度/压力范围、结构类型（bulk/surface/defect/interface）
- 这些描述符定义了**初始采样空间**

**第二层描述符（算法发现）**：误差分析揭示的失败模式
- 配位数 (CN)、最大键拉伸、局域应变
- sp2/sp3 比例、原子位移范数、局部配位变化
- ACE basis 残差分量、力误差的角向分布
- 这些描述符**不是研究人员手动指定的**——由算法在误差分析阶段自动计算、筛选、组合

### 1.3 核心思想

> 人类定义的描述符可能不捕捉模型的真实失败模式。
>
> 状态应该由"模型在哪里失败"来定义，而非"人类觉得什么重要"。

---

## 2 Formal Statement

### 2.1 数学形式化

令 $\varphi_1(x)$ 为 Layer 1 编码（如 SCXStateEncoder 的嵌入输出），$r(x) = |f_{\text{model}}(x) - f_{\text{true}}(x)|$ 为残差。

定义 error-relevant subspace：

$$D^* = \{j: \text{MI}(\varphi_1[:, j], r) > \tau\}$$

即在第一层编码的各维度中，与残差 $r$ 的互信息超过阈值 $\tau$ 的维度索引集。

则在 $D^*$ 上的聚类 $\mathcal{S}^*$ 满足：

$$\mathbb{E}[\text{Var}(r \mid s \in \mathcal{S}^*)] \leq \mathbb{E}[\text{Var}(r \mid s \in \mathcal{S}_{\text{human}})]$$

即 error-driven states 的组内残差方差不超过人类定义状态的组内残差方差。

### 2.2 算法工作流

**Phase A: 初始训练**
```
输入: 第一层描述符定义的初始 DFT 数据集 D₀
过程: 训练 Single ACE baseline M₀
输出: M₀, 测试集误差分布
```

**Phase B: 误差景观分析**
```
输入: M₀, 测试集
过程:
  1. 对每个测试结构计算 per-atom force error 和 per-structure error
  2. 为每个原子计算候选第二层描述符:
     - CN（不同截断半径）、最大/平均键拉伸
     - 局域应变张量不变量、键角分布统计
     - Voronoi 体积、ACE basis 各分量贡献
  3. 用互信息 / SHAP / permutation importance 筛选与误差最相关的描述符
  4. 在选中的描述符空间中做 UMAP/PCA 降维
  5. HDBSCAN 聚类发现误差簇
输出:
  - 误差簇地图 (cluster_id → 描述符范围 → 平均误差 → 样本数)
  - 高误差区域的定义（描述符空间中的凸包或区间）
```

**Phase C: 结构建议**
```
输入: 高误差区域定义
过程:
  1. 在高误差描述符区域中生成候选结构
  2. 去重（与已有训练集比较结构指纹）
  3. 排序（优先添加误差最大、信息量最大的结构）
输出: 结构建议文件 + 预期误差改善估计
```

**Phase D: 迭代增强**
```
输入: 新增 DFT 数据 D_new
过程:
  1. 合并 D = D_old ∪ D_new
  2. 重新训练或增量训练
  3. 回到 Phase B 重新评估误差景观
  4. 如果出现新的高误差簇 → Phase C
  5. 如果误差景观平坦化 → 结束
```

**Phase E（可选）: Expert 化**
```
输入: 最终的误差簇定义
过程:
  1. 每个误差簇自动定义一个 expert domain
  2. 为每个 domain 训练 residual expert
  3. 用 Expert Algebra 管理 expert 模块
  4. 导出为可部署的势函数
```

---

## 3 Theorem: Error-Driven States Dominate Human-Defined States

**定理 6.1（误差驱动状态的优势）**：令 $\mathcal{S}_{\text{human}}$ 为由人类先验知识定义的状态划分（如按晶体结构、化学组分等分类），$\mathcal{S}^*$ 为通过误差驱动发现的状态划分。在相同的状态数 $K = |\mathcal{S}|$ 下：

$$\mathbb{E}_{s \sim \mathcal{S}^*}[\text{Var}(r \mid s)] \leq \mathbb{E}_{s \sim \mathcal{S}_{\text{human}}}[\text{Var}(r \mid s)]$$

**证明概要**：由互信息的数据处理不等式，误差相关子空间 $D^*$ 保留了最多关于 $r$ 的信息。K-means 或 HDBSCAN 在 $D^*$ 上的聚类目标等价于最小化组内方差：

$$\min_{\mathcal{S}} \sum_{s \in \mathcal{S}} \sum_{x \in s} \|\varphi_1(x)[D^*] - \mu_s\|^2$$

而 $\mathcal{S}_{\text{human}}$ 是在原始空间 $\varphi_1$（可能包含与 $r$ 无关的维度）上定义的。因此 $\mathcal{S}^*$ 在 $r$ 上的条件方差至少不劣于 $\mathcal{S}_{\text{human}}$。$\square$

---

## 4 Connection to SCX Core

### 4.1 架构映射

- **Layer 1** = SCXStateEncoder.encode() — 初始嵌入映射
- **Layer 2** = ErrorDrivenEncoder.fit_error_states() — 误差条件状态发现
- **两层整合** = TwoLayerStateDiscovery — 完整的自动状态发现管线

### 4.2 为什么一层 encoder 不够

单纯的一层 encoder（如 12 维 MLIP encoder）的失败原因：

1. **通用嵌入与误差无关**：预训练嵌入可能编码了大量与专家失败模式无关的全局结构信息
2. **固定维度容量有限**：12 维嵌入可能无法同时编码化学环境信息和误差模式信息
3. **缺乏误差反馈**：没有将误差信号反向传播到状态构造过程

两层描述符体系通过误差条件投影解决了这些问题。

### 4.3 与信息瓶颈的关系

两层状态发现对应于**条件信息瓶颈**的迭代求解：

$$\min_{\Pi} I(\varphi_1; \tilde{X} \mid \mathcal{F}) - \beta I(\tilde{X}; r \mid \mathcal{F})$$

其中 $\mathcal{F} = \{f_1, \dots, f_M\}$ 为专家集合，$r$ 为残差，$\tilde{X}$ 为状态表示。

---

## 5 Implications

1. **状态划分不是固定的**——随模型改进而演化。随着模型误差景观变平坦，状态边界需要重新定义。

2. **第二层描述符 = 第一层特征的 error-conditioned subset**——自动筛选出与模型失败最相关的特征维度，排除无关的"背景"维度。

3. **这使 SCX 区别于所有基于人类特征的聚类方法**：
   - 传统方法：研究人员定义状态（"bulk", "surface", "defect"），但这些可能不反映模型的真实失败模式
   - SCX + 两层描述符：算法从误差分布中自动发现状态

4. **专家分区的涌现性**：专家分区不应由人凭经验定义，而应由算法从误差分布中涌现。

5. **与 Expert Governance Protocol 的整合**：
   ```
   两层描述符框架（上层：自动发现 expert 边界）
        │
        ▼
   Expert Algebra 框架（下层：管理 expert 模块）
   ```

---

## 6 关键验证实验

| 实验 | 假设 | 成功标准 |
|------|------|----------|
| Error vs CN | CN<3.5 区域误差 > CN≈4 区域 | p<0.01, effect size>2x |
| Error vs bond stretch | stretch>10% 区域误差显著增大 | p<0.01 |
| 描述符分离度 | 不同 batch 在描述符空间中可分离 | silhouette score > 0.3 |
| Targeted vs uniform | error-guided 采样用更少 DFT 达到同精度 | 等预算下 RMSE 降低 > 20% |
| 自动 expert vs 手动 expert | 算法发现的 expert 分区不差于手动 | 等 expert 数下 metrics 相当 |

---

## 参考文献

1. EGP 两层描述符框架. `EGP_两层描述符_算法驱动专家分区_2026-06-24.md`
2. Tishby, N., Pereira, F. C., & Bialek, W. (1999). The information bottleneck method. *Allerton Conference*.
3. Gauge-Normalized Residual ACE Expert Algebra Framework. `CodexKnowledge/`
4. SCX State-Conditioned eXpertise 核心框架. `01_SCX_核心框架_数学分析.md`
