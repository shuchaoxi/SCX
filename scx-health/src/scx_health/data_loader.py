"""Data loaders for MedMNIST and HAM10000 datasets."""

import torch
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader, Subset
import numpy as np
from typing import Optional, Tuple, Callable, Dict


def get_medmnist_transforms(img_size: int = 28) -> transforms.Compose:
    """Standard transforms for MedMNIST datasets."""
    return transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ])


def load_medmnist(
    name: str,
    root: str = './data',
    batch_size: int = 64,
    num_workers: int = 0,
    transform: Optional[Callable] = None,
) -> Dict[str, DataLoader]:
    """Load a MedMNIST v2 dataset by name.

    Args:
        name: One of 'pathmnist', 'dermamnist', 'bloodmnist'.
        root: Root directory for dataset storage.
        batch_size: Batch size for DataLoaders.
        num_workers: Number of DataLoader workers.
        transform: Torchvision transforms. If None, uses default.

    Returns:
        dict with keys 'train', 'val', 'test' mapping to DataLoaders.
    """
    import medmnist
    from medmnist import PathMNIST, DermaMNIST, BloodMNIST

    dataset_map = {
        'pathmnist': PathMNIST,
        'dermamnist': DermaMNIST,
        'bloodmnist': BloodMNIST,
    }

    if name.lower() not in dataset_map:
        raise ValueError(f"Unknown dataset '{name}'. Choose from {list(dataset_map.keys())}")

    DatasetClass = dataset_map[name.lower()]

    if transform is None:
        transform = get_medmnist_transforms()

    train_set = DatasetClass(split='train', transform=transform, download=False, root=root)
    val_set = DatasetClass(split='val', transform=transform, download=False, root=root)
    test_set = DatasetClass(split='test', transform=transform, download=False, root=root)

    loaders = {
        'train': DataLoader(train_set, batch_size=batch_size, shuffle=True,
                            num_workers=num_workers),
        'val': DataLoader(val_set, batch_size=batch_size, shuffle=False,
                          num_workers=num_workers),
        'test': DataLoader(test_set, batch_size=batch_size, shuffle=False,
                           num_workers=num_workers),
    }
    return loaders


def load_ham10000(
    root: str = './data/ham10000',
    batch_size: int = 32,
    num_workers: int = 0,
    transform: Optional[Callable] = None,
) -> Dict[str, DataLoader]:
    """Load HAM10000 dataset from local directory.

    Expected structure:
        ./data/ham10000/
            HAM10000_images_part_1/
            HAM10000_images_part_2/
            HAM10000_metadata.csv

    Note: HAM10000 must be downloaded manually from Harvard Dataverse.

    Args:
        root: Path to the HAM10000 data directory.
        batch_size: Batch size for DataLoaders.
        num_workers: Number of DataLoader workers.
        transform: Torchvision transforms.

    Returns:
        dict with keys 'train', 'val', 'test' or raises FileNotFoundError.
    """
    import os
    import pandas as pd
    from torchvision.datasets import ImageFolder

    meta_path = os.path.join(root, 'HAM10000_metadata.csv')
    if not os.path.exists(meta_path):
        raise FileNotFoundError(
            f"HAM10000 metadata not found at {meta_path}. "
            "Please download the dataset manually from "
            "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T"
        )

    if transform is None:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    # HAM10000 as ImageFolder requires pre-organized directories.
    # For now, raise a clear error if not structured.
    if not os.path.exists(os.path.join(root, 'train')):
        raise FileNotFoundError(
            "HAM10000 must be organized as train/val/test subdirectories. "
            "Run prepare_ham10000_split() first."
        )

    datasets = {}
    for split in ['train', 'val', 'test']:
        split_path = os.path.join(root, split)
        if os.path.exists(split_path):
            dataset = ImageFolder(split_path, transform=transform)
            datasets[split] = DataLoader(dataset, batch_size=batch_size,
                                         shuffle=(split == 'train'),
                                         num_workers=num_workers)
    return datasets


def extract_features(
    model: torch.nn.Module,
    loader: DataLoader,
    device: str = 'cuda',
) -> Tuple[np.ndarray, np.ndarray]:
    """Extract penultimate-layer features from a model.

    Args:
        model: PyTorch model (should return features when called with
               return_features=True or have a forward_features method).
        loader: DataLoader yielding (inputs, labels).
        device: Device to run inference on.

    Returns:
        (features, labels) as numpy arrays.
    """
    model.eval()
    all_features, all_labels = [], []

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            # Attempt to get penultimate features
            if hasattr(model, 'forward_features'):
                feats = model.forward_features(inputs)
            elif hasattr(model, 'features'):
                feats = model.features(inputs)
            else:
                # Default: remove the last linear layer
                feats = model.encoder(inputs) if hasattr(model, 'encoder') else model(inputs)

            if isinstance(feats, tuple):
                feats = feats[0]
            all_features.append(feats.cpu().numpy())
            all_labels.append(labels.numpy())

    return np.concatenate(all_features, axis=0), np.concatenate(all_labels, axis=0)
