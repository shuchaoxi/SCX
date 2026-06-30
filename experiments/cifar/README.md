# SCX CIFAR Experiments

验证 SCX 框架在通用图像分类上的有效性。

## 实验

### 1. SCX-Compress on CIFAR-10
数据冗余压缩保持精度。训练 ResNet-18/SimpleCNN 后用 SCX StateDiscovery 发现状态，SCX RedundancyScore 计算冗余度，按 20%-50% 压缩率压缩训练集后重训练比较。

```bash
python run_cifar10_compress.py --epochs 10 --simple-cnn
```

预期: 压缩 50% 数据，精度损失 < 3%

### 2. SCX-Noise on CIFAR-10
区分标签噪声和困难样本。注入 10%/20%/30% 对称标签噪声后训练，用 SCX NoiseScore 检测噪声。

```bash
python run_cifar10_noise.py --epochs 10 --simple-cnn
```

预期: 噪声检测 F1 > 0.7

### 3. SCX-Routing on CIFAR-100
状态条件专家路由。将 CIFAR-100 分为 5 个大类组，训练 5 个专家，用 SCX ExpertReliability 计算专家-状态可靠性矩阵，ExpertRouter 路由测试样本到最佳专家。

```bash
python run_cifar100_routing.py --epochs 10
```

预期: 路由精度 > 均匀 ensemble > 最佳单专家

### 4. Baseline 对比
```bash
python run_baselines.py --epochs 10 --simple-cnn
```

## 方法对比

| 方法 | 描述 | 接口 |
|------|------|------|
| Random | 随机采样 | `random_sample(X, y, ratio)` |
| Uncertainty | 预测熵排序 | `uncertainty_sample(X, y, ratio, probabilities)` |
| Diversity | 特征空间最远点 | `diversity_sample(X, y, ratio)` |
| Coreset | K-Center 贪心 | `coreset_sample(X, y, ratio)` |
| High-loss | 最高损失采样 | `highloss_sample(X, y, ratio, losses)` |

## 依赖

- PyTorch >= 1.13
- torchvision >= 0.14
- numpy, scikit-learn
- SCX (本仓库 `src/scx/`)

## 结果目录

所有实验结果自动保存为 JSON 到 `results/` 目录。
