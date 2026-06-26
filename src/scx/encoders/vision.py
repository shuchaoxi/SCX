"""
Vision Encoder — 图像领域的状态编码器。

支持两种 backbone:
- simple_cnn: 轻量 CNN 提取特征 (无 torch 依赖)
- torch: 使用 torchvision 预训练模型 (如 resnet18)

Example
-------
>>> import numpy as np
>>> from scx.encoders.vision import VisionEncoder
>>> encoder = VisionEncoder(backbone="simple_cnn")
>>> image = np.random.rand(32, 32, 3).astype(np.float32)
>>> vec = encoder.encode(image)
>>> vec.shape
(256,)
"""

from __future__ import annotations

from typing import Any

import numpy as np

from scx.encoders.base import SCXStateEncoder


class VisionEncoder(SCXStateEncoder):
    """图像编码器: 将图像编码为固定维度的特征向量。

    Parameters
    ----------
    backbone : str
        特征提取 backbone:
        - "simple_cnn": 轻量 CNN (纯 numpy, 无 torch 依赖)
        - "resnet18", "resnet50" 等: torchvision 模型 (需 torch)
    device : str
        计算设备 ("cpu" 或 "cuda"), 仅 torch backbone 生效
    input_size : int
        输入图像大小 (input_size x input_size)
    """

    def __init__(
        self,
        backbone: str = "simple_cnn",
        device: str = "cpu",
        input_size: int = 32,
    ) -> None:
        self.backbone = backbone
        self.device = device
        self.input_size = input_size
        self._model = None

        if backbone == "simple_cnn":
            self._feature_dim = 256
        elif backbone.startswith("resnet"):
            self._feature_dim = 512
        elif backbone.startswith("vit"):
            self._feature_dim = 768
        else:
            self._feature_dim = 256

    def encode(self, image: Any) -> np.ndarray:
        """将图像编码为特征向量。

        Parameters
        ----------
        image : np.ndarray or torch.Tensor
            输入图像, 形状 (H, W, C) 或 (C, H, W) 或 (H, W)

        Returns
        -------
        np.ndarray, shape (d,)
        """
        if self.backbone == "simple_cnn":
            return self._encode_simple_cnn(image)
        else:
            return self._encode_torch(image)

    def batch_encode(self, images: list[Any]) -> np.ndarray:
        """批量编码图像。

        Parameters
        ----------
        images : list[np.ndarray or torch.Tensor]

        Returns
        -------
        np.ndarray, shape (N, d)
        """
        return np.stack([self.encode(img) for img in images])

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Euclidean 距离。"""
        return float(np.linalg.norm(a - b))

    def cluster(
        self, X: np.ndarray, n_clusters: int, **kwargs
    ) -> tuple[np.ndarray, np.ndarray]:
        """KMeans 聚类。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        n_clusters : int
        **kwargs
            random_state : int

        Returns
        -------
        labels : np.ndarray, shape (N,)
        centroids : np.ndarray, shape (K, d)
        """
        from sklearn.cluster import MiniBatchKMeans

        n = max(min(n_clusters, len(X) - 1), 1)
        rs = kwargs.get("random_state", 42)
        km = MiniBatchKMeans(n_clusters=n, random_state=rs)
        labels = km.fit_predict(X)
        return labels, km.cluster_centers_

    # ------------------------------------------------------------------
    # Simple CNN (pure numpy)
    # ------------------------------------------------------------------

    def _encode_simple_cnn(self, image: Any) -> np.ndarray:
        """轻量 CNN 特征提取: 卷积 + 池化 + 展平。"""
        img = self._to_numpy(image, target_size=self.input_size)

        # Simple feature: color histogram + texture + spatial layout
        # This avoids heavy CNN implementation while still capturing
        # meaningful image features.

        # 1. Color histogram (per channel, 16 bins) -> 48 dims
        h, w = img.shape[:2]
        hist_features = []
        for c in range(min(img.shape[2], 3)):
            channel = img[:, :, c]
            hist, _ = np.histogram(channel, bins=16, range=(0, 1))
            hist_features.append(hist / max(h * w, 1))
        hist_vec = np.concatenate(hist_features)  # 48

        # 2. Mean and std per channel -> 6 dims
        stats = []
        for c in range(min(img.shape[2], 3)):
            channel = img[:, :, c]
            stats.append(float(channel.mean()))
            stats.append(float(channel.std()))
        while len(stats) < 6:
            stats.extend([0.0, 0.0])

        # 3. Grid features: divide into 4x4 grid, per-channel mean -> 48 dims
        grid_features = []
        grid_h, grid_w = h // 4, w // 4
        for c in range(min(img.shape[2], 3)):
            channel = img[:, :, c]
            for gi in range(4):
                for gj in range(4):
                    patch = channel[
                        gi * grid_h : (gi + 1) * grid_h,
                        gj * grid_w : (gj + 1) * grid_w,
                    ]
                    grid_features.append(float(patch.mean()))

        # 4. Edge intensity (simple gradient) -> 154 dims (to reach 256)
        gray = img.mean(axis=2) if img.shape[2] >= 3 else img[:, :, 0]
        gx = np.abs(np.diff(gray, axis=1))
        gy = np.abs(np.diff(gray, axis=0))
        edge_intensity = float(gx.mean()) if gx.size > 0 else 0.0
        edge_std = float(gx.std()) if gx.size > 0 else 0.0

        # Assemble: 48 + 6 + 48 + 2 = 104, pad with zeros to 256
        base = np.concatenate([
            hist_vec,
            np.array(stats, dtype=np.float64),
            np.array(grid_features, dtype=np.float64),
            np.array([edge_intensity, edge_std], dtype=np.float64),
        ])

        if len(base) < self._feature_dim:
            base = np.pad(base, (0, self._feature_dim - len(base)))
        elif len(base) > self._feature_dim:
            base = base[: self._feature_dim]

        return base

    def _encode_torch(self, image: Any) -> np.ndarray:
        """使用 torchvision 模型提取特征。"""
        import torch
        import torchvision.transforms as T
        import torchvision.models as models

        if self._model is None:
            self._model = self._build_torch_backbone()
            self._model.to(self.device)
            self._model.eval()

        # Convert to tensor
        if isinstance(image, np.ndarray):
            img_tensor = torch.from_numpy(image).float()
        else:
            img_tensor = image.float()

        # Handle shape: (H, W, C) -> (C, H, W)
        if img_tensor.ndim == 3 and img_tensor.shape[-1] in (1, 3, 4):
            img_tensor = img_tensor.permute(2, 0, 1)

        # Add batch dim if missing
        if img_tensor.ndim == 3:
            img_tensor = img_tensor.unsqueeze(0)

        # Resize to expected input size
        transform = T.Compose([
            T.Resize((self.input_size, self.input_size)),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        img_tensor = transform(img_tensor.to(self.device))

        with torch.no_grad():
            if hasattr(self._model, "forward_features"):
                feat = self._model.forward_features(img_tensor)
            else:
                # Fallback: remove the classifier head
                feat = self._model(img_tensor)

        return feat.cpu().numpy().flatten()

    def _build_torch_backbone(self) -> Any:
        """根据 backbone 名称构建 torchvision 模型。"""
        import torchvision.models as models

        model_map = {
            "resnet18": models.resnet18,
            "resnet34": models.resnet34,
            "resnet50": models.resnet50,
            "resnet101": models.resnet101,
        }
        if self.backbone in model_map:
            model = model_map[self.backbone](weights="DEFAULT")
            # Remove the final classification layer
            model.fc = type(model.fc)(model.fc.in_features, self._feature_dim)
            return model

        # Fallback to resnet18
        model = models.resnet18(weights="DEFAULT")
        model.fc = type(model.fc)(model.fc.in_features, self._feature_dim)
        return model

    # ------------------------------------------------------------------
    # Image utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _to_numpy(image: Any, target_size: int = 32) -> np.ndarray:
        """统一转换为 (H, W, C) 的 numpy 数组, 值域 [0, 1]。"""
        if isinstance(image, np.ndarray):
            img = image.copy()
        else:
            try:
                from PIL import Image as PILImage
                if isinstance(image, PILImage.Image):
                    img = np.array(image, dtype=np.float32)
                else:
                    img = np.array(image, dtype=np.float32)
            except Exception:
                img = np.array(image, dtype=np.float32, copy=False)

        # Ensure float
        if img.dtype.kind == "i":
            img = img.astype(np.float32) / 255.0
        elif img.dtype == np.uint8:
            img = img.astype(np.float32) / 255.0

        # Ensure 3D (H, W, C)
        if img.ndim == 2:
            img = np.stack([img, img, img], axis=-1)
        elif img.ndim == 3 and img.shape[0] in (1, 3) and img.shape[-1] not in (1, 3, 4):
            # (C, H, W) -> (H, W, C)
            img = img.transpose(1, 2, 0)
        if img.shape[-1] == 1:
            img = np.repeat(img, 3, axis=-1)
        elif img.shape[-1] > 3:
            img = img[:, :, :3]

        # Resize if needed
        if img.shape[0] != target_size or img.shape[1] != target_size:
            try:
                from PIL import Image as PILImage
                pil_img = PILImage.fromarray((img * 255).astype(np.uint8))
                pil_img = pil_img.resize((target_size, target_size), PILImage.Resampling.BILINEAR)
                img = np.array(pil_img, dtype=np.float32) / 255.0
            except Exception:
                # Simple resize fallback
                img = img[:target_size, :target_size, :]

        return img
