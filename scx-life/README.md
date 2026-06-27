# SCX-Life: State-Conditioned eXpertise for Life Sciences

> Merged module combining SCX-Health (medical imaging valuation) and SCX-Drug (drug-target interaction prediction) under a unified interface.

## Overview

SCX-Life applies the SCX (State-Conditioned eXpertise) framework to two
life-science verticals:

| Submodule | Domain | Key Capabilities |
|-----------|--------|-----------------|
| `health/` | Medical imaging | Redundancy compression, label-noise detection, state-conditioned expert routing on MedMNIST / HAM10000 |
| `drug/`   | Drug discovery | SMILES featurization, drug-likeness assessment, multi-layer DTI prediction (KB, similarity, ML, docking), full targetome screening |

These two modules share a common mathematical foundation — the SCX theorems
about state-conditional expert diversity — but operate on different data
modalities (pixels vs molecules).

## Directory Structure

```
scx-life/
├── README.md                  # This file
├── __init__.py                # Unified package entry point
├── LICENSE                    # Apache 2.0
├── health/                    # Medical imaging (from scx-health)
│   ├── __init__.py
│   ├── data_loader.py         # MedMNIST / HAM10000 loaders
│   ├── encoder.py             # SimpleCNN, ResNet encoder
│   ├── data/                  # Dataset downloads and references
│   ├── experiments/
│   │   ├── compress/          # SCX-Compress: redundancy scoring
│   │   ├── noise/             # SCX-Noise: label-noise detection
│   │   └── routing/           # SCX-Routing: state-conditioned expert routing
│   └── results/               # Experiment outputs and reports
├── drug/                      # Drug-target interaction (from drug-module)
│   ├── __init__.py
│   ├── kernel.py              # Molecular kernels (Tanimoto, Dice, graph RBF)
│   ├── pipeline.py            # DrugPipeline — multi-step DTI pipeline
│   ├── state.py               # TargetProfileState — drug-target state container
│   ├── operators/
│   │   ├── base.py            # DrugOperator protocol, DrugStepContext
│   │   ├── descriptors.py     # Comprehensive molecular descriptor engine
│   │   ├── drugbank.py        # DrugBank/ChEMBL/BindingDB KB lookup
│   │   ├── druglikeness.py    # Lipinski, Veber, Ghose, QED, SAscore
│   │   ├── dti.py             # KB lookup, similarity inference, deep DTI, docking
│   │   └── mol_featurizer.py  # SMILES parsing, fingerprints (ECFP4, MACCS, RDKit)
│   ├── configs/               # YAML pipeline configs (demo + full-scale)
│   ├── scripts/               # Run scripts for database download and targetome
│   └── docs/                  # Targetome TOP-10 analysis report
└── common/                    # Shared utilities
    ├── __init__.py
    └── utils.py               # ensure_dir, load/save_json, Timer
```

## Quick Start

### Medical Imaging (health)

```python
from scx_life.health.data_loader import load_medmnist
from scx_life.health.encoder import create_encoder

loaders = load_medmnist("dermamnist", root="./data")
model = create_encoder("resnet18", in_channels=3, num_classes=7)
```

Run experiments:
```bash
python -m scx_life.health.experiments.noise.run_noise --dataset dermamnist
python -m scx_life.health.experiments.routing.run_routing --dataset bloodmnist
python -m scx_life.health.experiments.compress.run_compress --dataset pathmnist
```

### Drug-Target Interaction (drug)

```python
from scx_life.drug import DrugPipeline, make_initial_state

state = make_initial_state("compounds.csv", "targets.csv")
pipeline = DrugPipeline.from_yaml("drug/configs/dti_pipeline_demo.yaml")
states = pipeline.run(state)
pipeline.write_target_profiles(states[-1], "outputs/")
```

Run full targetome:
```bash
python -m scx_life.drug.scripts.run_full_targetome \
    --molecules inputs/all_compounds.csv \
    --targets inputs/all_human_targets.csv \
    --config drug/configs/full_scale_targetome.yaml
```

## Dependencies

The module is split by dependency tier:

| Tier | Packages | Submodule |
|------|----------|-----------|
| Core | numpy, scipy, pandas, pyyaml | `drug/` only |
| Health | torch, torchvision, medmnist, scikit-learn | `health/` only |
| Drug (RDKit) | rdkit | `drug/` featurization + drug-likeness |
| Drug (full) | rdkit, torch, torch-geometric, duckdb | Full drug pipeline |

Install what you need:

```bash
# Health experiments only
pip install -r health/requirements.txt

# Drug module only
pip install numpy pandas pyyaml scipy

# Drug module with RDKit
pip install rdkit numpy pandas pyyaml scipy

# Everything
pip install -r health/requirements.txt rdkit duckdb
```

## Relationship to SCX Framework

SCX-Life is an **application module** built on top of the core SCX framework.
It inherits the mathematical theorems from the SCX theory paper and
demonstrates them in concrete life-science domains.

| SCX Component | Used In | Purpose |
|--------------|---------|---------|
| `scx.state.discovery.StateDiscovery` | health experiments | Discover data states via k-means on feature space |
| `scx.valuation.noise_score.NoiseScore` | health/noise | Per-sample label-noise scoring |
| `scx.valuation.redundancy.RedundancyScore` | health/compress | Per-sample redundancy scoring |
| `scx.expert.router.ExpertRouter` | health/routing | State-conditioned expert selection |
| `scx.kernel.*` | drug/kernel | Distance/similarity kernels |

## License

Apache 2.0 — see `LICENSE`.

## References

- Yang et al., "MedMNIST v2", 2023
- Lipinski et al., "Experimental and computational approaches to estimate solubility and permeability", Adv. Drug Deliv. Rev. 1997
- Bickerton et al., "Quantifying the chemical beauty of drugs", Nature Chemistry 2012
- SCX Platform: `https://github.com/SCX-Platform`
