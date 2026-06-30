"""SCX Drug — molecular computation module for drug-target interaction prediction.

This is the drug-domain vertical of the SCX platform, parallel to the
semiconductor process modules (cmp-model, deposition-model, etc.).

Quick start
-----------
>>> from scx_drug import DrugPipeline, make_initial_state
>>> state = make_initial_state("compounds.csv", "targets.csv")
>>> pipeline = DrugPipeline.from_yaml("configs/dti_pipeline.yaml")
>>> states = pipeline.run(state)
>>> pipeline.write_target_profiles(states[-1], "outputs/")
"""

__version__ = "0.2.0"

from scx_drug.pipeline import DrugPipeline, make_initial_state
from scx_drug.state import TargetProfileState

__all__ = [
    "DrugPipeline",
    "TargetProfileState",
    "make_initial_state",
    "__version__",
]
