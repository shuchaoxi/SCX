# 🏗️ SCX 研究超级配置清单

> 面壁者研发工作站 · 2026-06-30

---

## 一、算力层

| 组件 | 配置 | 用途 | 预算 |
|------|------|------|------|
| **主力 GPU** | 1× RTX 4090 24GB (已有) | NEP 训练、小模型推理、Spring 自进化 | — |
| **推理 GPU 池** | 4× RTX 4090 24GB | 并行 CC 会话、多专家投票、M-seed 解码 | ¥50,000 |
| **超算** | 孝感超算 (已有) | DFT 计算、大规模数据库全量筛选 | — |
| **CPU** | AMD Threadripper 7970X (32核) | 数据预处理、特征提取 | ¥15,000 |
| **内存** | 128GB DDR5 ECC | 200GB 药物数据库内存映射 | ¥4,000 |
| **存储** | 2× 4TB NVMe SSD (RAID0) | 数据库高速读写、CC workspace | ¥6,000 |
| **存储** | 1× 20TB HDD | 冷数据归档、DFT 轨迹 | ¥3,000 |
| **网络** | 万兆光纤 | 超算数据传输 | — |

---

## 二、AI 引擎层

| 引擎 | 模型 | 用途 | 月费 |
|------|------|------|------|
| **CC 主力** | DeepSeek V4 Pro (anthropic 端点) | 数学推导、论文写作、代码生成 | ¥500 |
| **CC 审查** | DeepSeek V4 Pro × 3 并行 | 多专家 hostile review | ¥1,500 |
| **本地推理** | Qwen-7B / DeepSeek-7B (4090) | 快速原型、M-seed 解码 | 免费 |
| **API 备份** | Claude Sonnet 4 (OpenRouter) | DeepSeek 过载时的 fallback | ¥200 |
| **嵌入模型** | BGE-M3 (本地) | State Crystallization 特征聚类 | 免费 |

---

## 三、软件栈

| 层 | 工具 | 配置 |
|----|------|------|
| **OS** | Ubuntu 24.04 LTS | WSL2 或裸金属 |
| **Shell** | zsh + tmux | 多 CC 会话管理 |
| **Python** | 3.11 + uv | 项目依赖管理 |
| **LaTeX** | TeX Live 2025 | 论文编译 |
| **Git** | main + feature 分支 | SCX 版本管理 |
| **编辑器** | VS Code + LaTeX Workshop | 论文写作 |
| **容器** | Docker + NVIDIA Container Toolkit | 环境隔离 |

---

## 四、CC 工作流优化

| 配置项 | 推荐值 | 理由 |
|--------|--------|------|
| `max-turns` | 50 (数学推导) / 30 (论文编辑) | 复杂证明需要更多轮次 |
| `effort` | max (推导) / high (审查) | 数学需要深度推理 |
| 并行 CC 数 | 3-4 路 | RTX 4090 × 4 支撑 |
| 单路超时 | 600s | 50 轮 max effort 通常 3-8 分钟 |
| `--allowedTools` | Read,Write,Edit (论文); Read,Write,Edit,Bash (代码) | 避免意外 |
| 工作目录 | `/g/Xiaogan_Supercomputing_data/SCX` | 统一路径 |
| 完整路径写法 | `G:/Xiaogan_Supercomputing_data/SCX/...` | CC workspace 在 D: 盘，需绝对路径 |

---

## 五、数据层

| 数据集 | 规模 | 用途 | 状态 |
|--------|------|------|------|
| AlN v3 (DFT) | 534 帧 | SCX 验证 | ✅ 已有 |
| DrugBank 5.0 | 6,784 条 | Yajie 药物审计 | ⬜ 待下载 |
| ChEMBL 34 | ~2M 条 | 全量筛选 | ⬜ 待下载 |
| PubChem | ~100M 条 | 全量筛选 | ⬜ 待下载 |
| BindingDB | ~2M 条 | 全量筛选 | ⬜ 待下载 |
| PDBbind | ~20K 条 | 全量筛选 | ⬜ 待下载 |
| 其他 7 数据库 | ~50GB | 全量筛选 | ⬜ 待下载 |
| **药物总计** | **~200GB** | **12 数据库全量** | |

---

## 六、安全层

| 措施 | 配置 |
|------|------|
| Git 远程备份 | GitHub private repo |
| 冷备份 | 外置硬盘，每周 rsync |
| `.env` 保护 | `.gitignore` 排除 API key |
| 论文版本 | 每轮 hostile review 后 commit |
| 理论文件 | `theory/` 下按日期归档 |

---

## 七、待购清单（优先级）

| 优先级 | 设备 | 预算 | 理由 |
|--------|------|------|------|
| 🔴 P0 | 4× RTX 4090 | ¥50,000 | 并行 CC + NEP 训练 |
| 🟠 P1 | 4TB NVMe SSD × 2 | ¥6,000 | 200GB 数据库 + workspace |
| 🟡 P2 | Threadripper + 128GB | ¥19,000 | 数据预处理 |
| 🟢 P3 | 20TB HDD | ¥3,000 | 冷备份 |
| **总计** | | **¥78,000** | |

---

## 八、不买的

| 项目 | 理由 |
|------|------|
| A100/H100 | 不需要。DeepSeek API + 4090 足够所有推导 |
| 云计算 | 超算已有。API 月费 ¥2,000 足够 |
| Mac Studio | 生态不兼容 CUDA |
| 多机集群 | 单人研究不需要 |
