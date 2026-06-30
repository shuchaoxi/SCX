"""SCX-Life: State-Conditioned eXpertise for Life Sciences.

SCX-Life unifies two life-science verticals of the SCX platform:

  health/   Medical imaging and clinical data valuation
            (MedMNIST, HAM10000, SCX-Noise, SCX-Compress, SCX-Routing)

  drug/     Drug-target interaction prediction and molecular profiling
            (SMILES featurization, drug-likeness, DTI, targetome screening)

  common/   Shared utilities reused across health and drug modules

References
----------
- SCX framework:     https://github.com/SCX-Platform
- MedMNIST v2:       https://medmnist.com
- DrugBank:          https://go.drugbank.com
"""

__version__ = "0.1.0"

from scx_life.common import (
    ensure_dir,
    load_json,
    save_json,
    Timer,
)
