# SCX-Health

State-Conditioned eXpertise for Medical Data Valuation

## Overview
SCX-Health demonstrates SCX framework on medical imaging data:
- Redundancy compression (which training samples are redundant?)
- Noise detection (which samples have label noise?)
- Expert routing (which model is best for which diagnostic state?)

## Datasets
- MedMNIST v2 (PathMNIST, DermaMNIST, BloodMNIST)
- HAM10000 (skin lesion classification)

## Experiments
1. SCX-Compress: 20-40% compression with <2% accuracy loss
2. SCX-Noise: distinguish noisy labels from hard cases
3. SCX-Routing: state-conditioned expert selection outperforms uniform ensemble

## License
Apache 2.0 — fully open source
