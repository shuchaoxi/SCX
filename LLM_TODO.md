# 明日推进 TODO — 2026-06-29

## 🔴 HIV 药监数据库下载与运行

### 下载
- [ ] ChEMBL: HIV子集（SQL dump 或 Python API chembl_webresource_client）
- [ ] DrugBank: 申请学术账号 → XML下载
- [ ] PubChem BioAssay: HIV相关 AID（PUG REST API）
- [ ] Stanford HIVDB: 突变-耐药表直接下载
- [ ] BindingDB: 蛋白-配体亲和力

### 预处理
- [ ] 提取 SMILES → 标准化 → ECFP4/MACCS 指纹
- [ ] 统一格式: drug_id, target, assay_type, value, units

### 运行
- [ ] 4 专家设置: 结合亲和力 | 毒性 | 药性 | 耐药突变
- [ ] 跑 `drug-module/scripts/hiv_drug_audit.py`
- [ ] 输出: 高共识候选 + 观察名单 + 数据质量报告

### 扩展
- [ ] 加入原发性免疫缺陷 / 自身免疫病数据（可选）
- [ ] Yajie 自动区分 HIV vs 自身免疫的靶点重叠

---

## 🟡 arXiv 投稿
- [ ] Paper 1 (Yajie) — 编译已就绪，含 S1-S8
- [ ] Paper 2 (Spring) — 13 页，已就绪

---

## ✅ 已完成（本轮）
- [x] Spring 代码实现 (spring.py 1551行)
- [x] Yajie fit() 鲁棒实现 + 18 测试
- [x] Spring 验证脚本 + 噪声对比实验
- [x] Paper 9 LLM 审计脚本骨架
- [x] 协议论文 18 层博弈论
- [x] 综述双引擎架构重写
- [x] 分类学理论 + 内在可解释性
- [x] Anthropic 批判 + 自我怀疑 + 达摩克利斯之剑
- [x] 商业架构 (BUSINESS_ARCHITECTURE.md)
- [x] 战略笔记 (DEVELOPMENT_LOG.md)
- [x] 445 测试全部通过
- [x] 邮箱全部从论文中删除
