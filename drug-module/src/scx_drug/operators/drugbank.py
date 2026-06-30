"""DrugBank knowledge-base query operator.

Queries local DrugBank / ChEMBL / BindingDB extracts (stored as Parquet or
SQLite) to populate ``knowledge_hit`` and ``knowledge_score`` columns in
the pairs DataFrame.  This is the first and fastest stage of the target
profiling pipeline.

Architecture
------------
The operator expects pre-processed database extracts in a directory
structure::

    db_path/
    ├── drugbank_targets.parquet     # columns: drug_id, smiles, uniprot_id, action_type, score
    ├── chembl_activities.parquet    # columns: molregno, smiles, target_chembl_id, pchembl_value
    ├── bindingdb_affinities.parquet # columns: smiles, uniprot_id, ki_nm, ic50_nm
    └── stitch_links.parquet         # columns: smiles, uniprot_id, combined_score

If only SMILES are available (no database), the operator is a no-op and
simply passes the state through — all predictions fall to downstream
operators (similarity, ML, docking).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from scx_drug.operators.base import DrugOperator, DrugStepContext, next_state
from scx_drug.state import TargetProfileState


@dataclass
class KnowledgeBaseConfig:
    """Configuration for the knowledge-base lookup operator."""

    db_path: str | Path = "data/knowledge_bases"
    enabled_databases: list[str] = field(
        default_factory=lambda: ["drugbank", "chembl", "bindingdb"]
    )
    min_confidence: float = 0.5
    use_smiles_lookup: bool = True  # fall back to SMILES hash match
    metadata: dict[str, Any] = field(default_factory=dict)


class KnowledgeBaseLookupOperator:
    """Query pre-extracted drug-target knowledge bases.

    Recipe keys
    -----------
    db_path : str
        Path to the directory containing ``*.parquet`` database extracts.
    enabled_databases : list[str]
        Which databases to query. Default: ``["drugbank", "chembl", "bindingdb"]``.
    min_confidence : float
        Minimum confidence score to mark a pair as ``knowledge_hit``.
        Default 0.5.
    """

    name = "drugbank_kb_lookup"

    def __init__(self, config: KnowledgeBaseConfig | None = None):
        self.config = config or KnowledgeBaseConfig()

    def apply(
        self,
        state: TargetProfileState,
        context: DrugStepContext,
    ) -> TargetProfileState:
        out = next_state(state, context)
        recipe = context.recipe

        db_path = Path(recipe.get("db_path", self.config.db_path))
        enabled = recipe.get("enabled_databases", self.config.enabled_databases)
        min_conf = float(recipe.get("min_confidence", self.config.min_confidence))

        # Try to load each enabled database
        hits: list[pd.DataFrame] = []
        for db_name in enabled:
            db_file = db_path / f"{db_name}_targets.parquet"
            if not db_file.exists():
                db_file = db_path / f"{db_name}_links.parquet"
            if not db_file.exists():
                db_file = db_path / f"{db_name}_activities.parquet"
            if not db_file.exists():
                continue

            try:
                db = pd.read_parquet(db_file)
                # Normalise columns: every DB extract must have at minimum
                # a SMILES column and a target_id column.
                db_smiles_col = _find_column(db, ["smiles", "canonical_smiles", "SMILES"])
                db_target_col = _find_column(db, ["target_id", "uniprot_id", "target_chembl_id"])
                if db_smiles_col is None or db_target_col is None:
                    continue

                # Match pairs
                merged = out.pairs.merge(
                    db,
                    left_on=["smiles", "target_id"],
                    right_on=[db_smiles_col, db_target_col],
                    how="inner",
                    suffixes=("", f"_{db_name}"),
                )
                if merged.empty:
                    continue

                # Score column
                score_col = _find_column(
                    merged,
                    ["score", "confidence_score", "pchembl_value", "combined_score"],
                )
                if score_col is not None:
                    merged["match_score"] = merged[score_col].astype(float)
                else:
                    merged["match_score"] = 1.0

                merged["source_db"] = db_name
                hits.append(merged[["pair_id", "match_score", "source_db"]])
            except Exception:
                continue

        if hits:
            all_hits = pd.concat(hits, ignore_index=True)
            # Keep best score per pair
            best = all_hits.loc[
                all_hits.groupby("pair_id")["match_score"].idxmax()
            ].copy()

            pairs = out.pairs.copy()
            mask = pairs["pair_id"].isin(best["pair_id"])
            pairs.loc[mask, "knowledge_hit"] = (
                best.set_index("pair_id").loc[pairs.loc[mask, "pair_id"], "match_score"].values
                >= min_conf
            )
            pairs.loc[mask, "knowledge_score"] = best.set_index("pair_id").loc[
                pairs.loc[mask, "pair_id"], "match_score"
            ].values
            pairs.loc[mask, "knowledge_source"] = best.set_index("pair_id").loc[
                pairs.loc[mask, "pair_id"], "source_db"
            ].values
            pairs.loc[mask & (pairs["knowledge_score"] >= min_conf), "evidence_level"] = (
                "experimental"
            )
            out.pairs = pairs

        out.metadata["knowledge_bases_queried"] = enabled
        out.metadata["knowledge_hits_found"] = int(out.pairs["knowledge_hit"].sum())
        return out


# ── helpers ────────────────────────────────────────────────────────────────

def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first column name from *candidates* that exists in *df*."""
    for col in candidates:
        if col in df.columns:
            return col
    return None
