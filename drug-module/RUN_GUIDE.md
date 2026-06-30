# 🧬 药物数据库全量下载 & 筛选 — 一页纸运行指南

## 前置条件

```bash
# Python 环境（已有）
python --version   # 3.11.9
pip install requests tqdm rdkit pandas numpy   # 如缺失

# 存储位置（选一个）
# 方案A：外置硬盘
OUTDIR="W:/scx_databases"
# 方案B：NVMe 本地
OUTDIR="G:/Xiaogan_Supercomputing_data/databases/drug"
```

## 第一步：下载核心数据库（~110 GB）

```bash
cd G:/Xiaogan_Supercomputing_data/SCX

# Tier 1 — 8 个核心数据库
python drug-module/scripts/download_databases.py \
  --output W:/scx_databases \
  --tier 1
```

**预计时间：** 2-6 小时（取决于网络）

## 第二步：下载扩展数据库（~25 GB）

```bash
# Tier 2
python drug-module/scripts/download_databases.py \
  --output W:/scx_databases \
  --tier 2
```

## 第三步：全量筛选（耗时最长）

```bash
# 对所有 drug × target 对跑 Yajie 多专家审计
python drug-module/scripts/screen_all_databases.py \
  --input W:/scx_databases \
  --output W:/scx_results \
  --experts 10
```

**预计时间：** 数小时到数天（取决于是否有 GPU 加速）

## 第四步：验证已知结果

```bash
# 检查已知 HIV 药物的 MT 评分是否合理
python drug-module/scripts/validate_mt_scores.py \
  --results W:/scx_results \
  --drugs hiv_protease_inhibitors
```

## 存储需求

| 数据 | 大小 |
|------|------|
| 原始下载 | ~155 GB |
| 解压/处理 | ~50 GB |
| 筛选结果 | ~10 GB |
| **总计** | **~215 GB** |

## 监控命令

```bash
# 查看下载进度
watch -n 5 "du -sh W:/scx_databases/*"

# 查看筛选日志
tail -f W:/scx_results/screen.log
```

---

## ⚠️ 注意事项

1. **W: 盘必须是 NTFS** — 单个文件可能 > 4GB（如 ChEMBL SQLite ~30GB）
2. **网络稳定** — 部分数据库在国外，可能需要代理
3. **不要中断** — 下载断点续传未实现，中断需重来
4. **先在 Tier 1 跑通** — 确认环境 OK 后再加 Tier 2
