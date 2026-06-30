"""Simple CNN and ResNet encoders for medical image classification."""

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Optional


class SimpleCNN(nn.Module):
    """A simple CNN encoder for small medical images (e.g. MedMNIST 28x28)."""

    def __init__(
        self,
        in_channels: int = 1,
        num_classes: int = 9,
        hidden_dim: int = 128,
    ):
        super().__init__()
        self.num_classes = num_classes
        self.hidden_dim = hidden_dim

        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )

        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128, hidden_dim),
            nn.ReLU(inplace=True),
        )

        self.classifier = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor, return_features: bool = False):
        x = self.features(x)
        features = self.encoder(x)
        logits = self.classifier(features)
        if return_features:
            return logits, features
        return logits

    def forward_features(self, x: torch.Tensor) -> torch.Tensor:
        """Return penultimate layer features."""
        x = self.features(x)
        return self.encoder(x)


class ResNetEncoder(nn.Module):
    """ResNet-18 encoder wrapper for medical images.

    Supports both 1-channel (MedMNIST) and 3-channel (HAM10000) inputs.
    """

    def __init__(
        self,
        in_channels: int = 1,
        num_classes: int = 9,
        pretrained: bool = False,
        hidden_dim: int = 512,
    ):
        super().__init__()
        self.num_classes = num_classes
        self.hidden_dim = hidden_dim

        # Load ResNet-18 backbone
        self.backbone = models.resnet18(weights='DEFAULT' if pretrained else None)

        # Adjust first conv for grayscale input
        if in_channels == 1:
            old_conv = self.backbone.conv1
            self.backbone.conv1 = nn.Conv2d(
                1, old_conv.out_channels,
                kernel_size=old_conv.kernel_size,
                stride=old_conv.stride,
                padding=old_conv.padding,
                bias=False,
            )
            # Initialize with mean of RGB weights
            with torch.no_grad():
                self.backbone.conv1.weight.data = old_conv.weight.data.mean(
                    dim=1, keepdim=True
                )

        # Remove the final classification layer
        self.backbone.fc = nn.Identity()

        self.encoder = nn.Sequential(
            nn.Linear(512, hidden_dim),
            nn.ReLU(inplace=True),
        )

        self.classifier = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor, return_features: bool = False):
        x = self.backbone(x)
        features = self.encoder(x)
        logits = self.classifier(features)
        if return_features:
            return logits, features
        return logits

    def forward_features(self, x: torch.Tensor) -> torch.Tensor:
        """Return penultimate layer features."""
        x = self.backbone(x)
        return self.encoder(x)


def create_encoder(
    model_name: str = 'resnet18',
    in_channels: int = 1,
    num_classes: int = 9,
    pretrained: bool = False,
) -> nn.Module:
    """Factory function to create an encoder model.

    Args:
        model_name: 'simple_cnn' or 'resnet18'.
        in_channels: Number of input channels (1 for MedMNIST, 3 for HAM10000).
        num_classes: Number of output classes.
        pretrained: Use pretrained weights (ResNet only).

    Returns:
        A PyTorch nn.Module.
    """
    if model_name == 'simple_cnn':
        return SimpleCNN(in_channels=in_channels, num_classes=num_classes)
    elif model_name == 'resnet18':
        return ResNetEncoder(
            in_channels=in_channels,
            num_classes=num_classes,
            pretrained=pretrained,
        )
    else:
        raise ValueError(f"Unknown model: {model_name}. Choose 'simple_cnn' or 'resnet18'.")
