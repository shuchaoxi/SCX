"""Download MedMNIST v2 datasets via medmnist package."""
import medmnist
from medmnist import PathMNIST, DermaMNIST, BloodMNIST
import os

DATASETS = {
    'pathmnist': PathMNIST,
    'dermamnist': DermaMNIST,
    'bloodmnist': BloodMNIST,
}

def download_all(data_dir='./data'):
    for name, DatasetClass in DATASETS.items():
        print(f'Downloading {name}...')
        train = DatasetClass(split='train', download=True, root=data_dir)
        val = DatasetClass(split='val', download=True, root=data_dir)
        test = DatasetClass(split='test', download=True, root=data_dir)
        print(f'  {name}: {len(train)} train, {len(val)} val, {len(test)} test')

if __name__ == '__main__':
    download_all()
