# 明日推进 TODO — 2026-06-29

## 🔴 全药物数据库下载 + Yajie 一次性全筛

### 数据库清单（全量，不仅限于 HIV）

| # | 数据库 | 内容 | 大小 | 优先级 |
|:--:|------|------|:--:|:--:|
| 1 | **ChEMBL** | 全量生物活性数据（所有靶点、所有化合物） | ~50GB | 🔴 |
| 2 | **DrugBank** | 全部已批准+实验性药物，带靶点 | ~1GB | 🔴 |
| 3 | **PubChem BioAssay** | 全部检测数据 | ~50GB | 🔴 |
| 4 | **BindingDB** | 全量蛋白-配体结合亲和力 | ~2GB | 🔴 |
| 5 | **PDBbind** | 蛋白-配体复合物+结合亲和力（最精确） | ~5GB | 🟡 |
| 6 | **TTD** (Therapeutic Target Database) | 已知治疗靶点+对应药物 | ~500MB | 🔴 |
| 7 | **DrugCentral** | FDA批准药物的靶点+适应症 | ~1GB | 🟡 |
| 8 | **Open Targets** | 靶点-疾病关联（GWAS+文献） | ~10GB | 🟡 |
| 9 | **PharmGKB** | 药物基因组学（基因×药物×反应） | ~2GB | 🟡 |
| 10 | **Stanford HIVDB** | HIV耐药突变（保留） | <100MB | 🔴 |
| 11 | **SIDER** | 药物副作用数据库 | ~1GB | 🟡 |
| 12 | **STITCH** | 化合物-蛋白相互作用网络 | ~20GB | 🟢 |

### 硬盘需求
```
🔴 优先级 (必须): ~105GB
🟡 强推荐:         ~20GB  
🟢 可选:           ~20GB
缓冲+解压:        ~50GB
─────────────────────────
总计:             ~200GB
```

### 预处理管道
- [x] 所有 SMILES → 标准化 → ECFP4/MACCS 指纹 （screen_all_databases.py Phase 2）
- [x] 统一 schema: drug_id, target_id, assay_type, value, units, source_db
- [x] 去重（同一 drug-target 对在多个数据库中重复出现 = 专家共识）

### Yajie 运行
- [x] N 个专家（每数据库一个 + 物理化学性质 + 结构相似性）
- [x] 一次性筛选：所有药物 × 所有靶点 （screen_all_databases.py）
- [x] 输出：
  - 高共识 drug-target 对（多数据库交叉验证） → mt_high_confidence.csv
  - 数据库质量报告（哪个数据库矛盾最多） → mt_quality_report.json
  - 新兴靶点（高新颖性低共识 → Spring 待复活） → mt_novel_candidates.csv

### 验证
- [ ] 已知 HIV 药物是否被 Yajie 高分筛出
- [ ] Yajie 是否发现已知的跨界靶点（HIV/自身免疫/炎症共靶点）
- [ ] 假阳性分析（高分但文献无支持的 → 新发现候选）

---

## 🟡 arXiv 投稿
- [ ] Paper 1 (Yajie) — PDF已编译（含S1-S8）
- [ ] Paper 2 (Spring) — PDF已编译（13页）

---

## ✅ 已完成
- [x] Spring 代码 (1551行) + Yajie fit() + HIV 审计原型
- [x] 9篇论文框架 + 18层博弈论 + 445测试全过
- [x] **全药物数据库下载脚本** `drug-module/scripts/download_databases.py` (~1050行)
  - 12个数据库完整覆盖（ChEMBL, DrugBank, PubChem BioAssay, BindingDB, TTD, Stanford HIVDB, PDBbind, DrugCentral, Open Targets, PharmGKB, SIDER, STITCH）
  - 分层下载（Tier 1/2/3）约205GB
  - 每个数据库写入 provenance.json（SHA256校验、下载日期、版本、URL）
  - 进度条+ETA、断点续传、认证数据库占位符
  - 自动化解析: ChEMBL SQLite→Parquet, DrugBank XML→Parquet, BindingDB TSV→Parquet, PubChem PUG REST API, Open Targets GraphQL API
- [x] **Yajie全数据库筛查脚本** `drug-module/scripts/screen_all_databases.py` (~930行)
  - Phase 1: 加载所有数据库 Parquet/CSV + provenance 元数据
  - Phase 2: SMILES→ECFP4指纹标准化 + 靶点→UniProt ID映射
  - Phase 3: 药物-靶点统一证据矩阵（行=药靶对, 列=数据库专家）
  - Phase 4: Yajie多专家共识评分（Theorem 1: CLEAN/NOISY/AMBIGUOUS分类）
  - Phase 5: 8个输出文件（MT Gold Standard CSV, 分类摘要, 数据库一致性矩阵, 高置信度对, 分歧报告, 新候选, 质量报告JSON, 溯源审计JSON）
  - 完全可溯源：每对记录包含source_databases, database_links, download_date, mt_report_version
