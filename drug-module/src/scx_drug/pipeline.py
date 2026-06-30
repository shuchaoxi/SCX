"""Drug-target profiling pipeline engine.

Mirrors ``scx.flow.ProcessFlow`` but operates on ``TargetProfileState``
and drug operators.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from scx_drug.operators.base import DrugOperator, DrugStepContext
from scx_drug.operators.dti import (
    DockingVerificationOperator,
    DTIDeepPredictor,
    KnowledgeBaseLookupOperator,
    SimilarityInferenceOperator,
)
from scx_drug.operators.drugbank import KnowledgeBaseLookupOperator as DrugBankQueryOperator
from scx_drug.operators.druglikeness import DrugLikenessOperator
from scx_drug.operators.mol_featurizer import MoleculeFeaturizeOperator
from scx_drug.state import TargetProfileState


DRUG_OPERATOR_REGISTRY: dict[str, type[DrugOperator]] = {
    "molecule_featurize": MoleculeFeaturizeOperator,
    "knowledge_base_lookup": KnowledgeBaseLookupOperator,
    "drugbank_kb_lookup": DrugBankQueryOperator,
    "similarity_inference": SimilarityInferenceOperator,
    "dti_deep_predictor": DTIDeepPredictor,
    "docking_verification": DockingVerificationOperator,
    "drug_likeness": DrugLikenessOperator,
}


@dataclass
class DrugPipeline:
    """A sequence of drug-prediction operators acting on one TargetProfileState."""

    steps: list[DrugStepContext]
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "DrugPipeline":
        """Create a pipeline from a YAML config file."""
        cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls.from_config(cfg)

    @classmethod
    def from_config(cls, cfg: dict[str, Any]) -> "DrugPipeline":
        """Create a pipeline from a dictionary."""
        steps: list[DrugStepContext] = []
        pipeline_cfg = cfg.get("pipeline", cfg)
        for index, step in enumerate(
            pipeline_cfg.get("steps", []), start=1
        ):
            step_type = str(step.get("type", step.get("step_type", "")))
            if step_type not in DRUG_OPERATOR_REGISTRY:
                raise ValueError(
                    f"Unknown drug step type: {step_type}. "
                    f"Available: {sorted(DRUG_OPERATOR_REGISTRY)}"
                )
            steps.append(
                DrugStepContext(
                    step_index=index,
                    step_name=str(step.get("name", step_type)),
                    step_type=step_type,
                    recipe=dict(step.get("recipe", {})),
                )
            )
        metadata = dict(cfg.get("metadata", {}))
        return cls(steps=steps, metadata=metadata)

    def run(
        self, initial_state: TargetProfileState
    ) -> list[TargetProfileState]:
        """Run all steps and return every state, including the initial one."""
        states = [initial_state]
        state = initial_state
        for step in self.steps:
            operator = DRUG_OPERATOR_REGISTRY[step.step_type]()
            state = operator.apply(state, step)
            states.append(state)
        return states

    def write_summary(
        self,
        states: list[TargetProfileState],
        output_dir: str | Path,
    ) -> Path:
        """Write a pipeline summary CSV with one row per state."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        rows = [s.summary() for s in states]
        path = out / "drug_pipeline_summary.csv"
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    def write_target_profiles(
        self,
        final_state: TargetProfileState,
        output_dir: str | Path,
    ) -> dict[str, Path]:
        """Write per-molecule target profile CSV files.

        Returns
        -------
        dict[str, Path]
            Mapping from mol_id to output CSV path.
        """
        out_dir = Path(output_dir) / "target_profiles"
        out_dir.mkdir(parents=True, exist_ok=True)
        paths: dict[str, Path] = {}

        pairs = final_state.pairs
        resolved = pairs[pairs["evidence_level"] != "none"].copy()
        resolved = resolved.sort_values(
            ["mol_id", "combined_score"], ascending=[True, False]
        )

        for mol_id, group in resolved.groupby("mol_id"):
            path = out_dir / f"{mol_id}_targets.csv"
            group.to_csv(path, index=False)
            paths[mol_id] = path

        full_path = out_dir / "all_drug_target_pairs.csv"
        pairs.to_csv(full_path, index=False)
        paths["_all"] = full_path

        return paths


# ── Convenience entry point ───────────────────────────────────────────────

def make_initial_state(
    molecules_csv: str | Path,
    targets_csv: str | Path,
    *,
    state_id: str = "initial",
) -> TargetProfileState:
    """Build an initial TargetProfileState from two CSV files.

    Parameters
    ----------
    molecules_csv : str or Path
        CSV with at minimum ``mol_id`` and ``smiles`` columns.
    targets_csv : str or Path
        CSV with at minimum ``target_id`` column.
    """
    mol_df = pd.read_csv(molecules_csv)
    tgt_df = pd.read_csv(targets_csv)

    for col in ["mol_id", "smiles"]:
        if col not in mol_df.columns:
            raise ValueError(f"molecules CSV must have a '{col}' column")
    if "target_id" not in tgt_df.columns:
        raise ValueError("targets CSV must have a 'target_id' column")

    mol_df["_key"] = 1
    tgt_df["_key"] = 1
    pairs = mol_df.merge(tgt_df, on="_key").drop(columns=["_key"])
    mol_df = mol_df.drop(columns=["_key"])
    tgt_df = tgt_df.drop(columns=["_key"])
    pairs["pair_id"] = pairs["mol_id"].astype(str) + "_" + pairs["target_id"].astype(str)

    for col, default in [
        ("knowledge_hit", False), ("knowledge_score", 0.0),
        ("knowledge_source", ""),
        ("similarity_hit", False), ("similarity_score", 0.0),
        ("similarity_analog", ""),
        ("ml_score", 0.0), ("ml_model", ""),
        ("docking_score", 999.0), ("docking_rmsd", 999.0),
        ("combined_score", 0.0), ("evidence_level", "none"),
        ("confidence", "low"),
    ]:
        if col not in pairs.columns:
            pairs[col] = default

    return TargetProfileState(
        state_id=state_id,
        molecules=mol_df,
        targets=tgt_df,
        pairs=pairs,
        metadata={"source": "make_initial_state"},
    )
