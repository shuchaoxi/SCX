"""Drug module state data models.

Mirrors the SCX ``ProcessState`` pattern but designed for molecular
entities and drug-target interaction (DTI) computations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd


# ── Molecule-level record ────────────────────────────────────────────────

@dataclass
class MoleculeRecord:
    """Single molecule descriptor and fingerprint record.

    This is the molecular analogue of one row in ``ProcessState.grid``.
    """

    mol_id: str
    smiles: str
    inchi_key: str = ""
    mw: float = 0.0
    logp: float = 0.0
    hbd: int = 0
    hba: int = 0
    tpsa: float = 0.0
    rotatable_bonds: int = 0
    ring_count: int = 0
    fingerprint_ecfp4: np.ndarray | None = None
    fingerprint_maccs: np.ndarray | None = None
    graph_data: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


# ── Target-level record ──────────────────────────────────────────────────

@dataclass
class TargetRecord:
    """Single protein target descriptor record."""

    target_id: str
    uniprot_id: str = ""
    gene_name: str = ""
    protein_name: str = ""
    organism: str = "human"
    target_class: str = ""
    sequence: str = ""
    domains: list[str] = field(default_factory=list)
    pdb_ids: list[str] = field(default_factory=list)
    alpha_fold_id: str = ""
    binding_pocket_residues: list[int] | None = None
    disease_associations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


# ── Drug-target pair (grid cell) ─────────────────────────────────────────

@dataclass
class DrugTargetPairRecord:
    """One drug-target interaction pair — the fundamental grid unit."""

    pair_id: str
    mol_id: str
    target_id: str
    smiles: str = ""
    target_class: str = ""

    # Evidence layers (populated by operators)
    knowledge_hit: bool = False
    knowledge_score: float = 0.0
    knowledge_source: str = ""

    similarity_hit: bool = False
    similarity_score: float = 0.0
    similarity_analog: str = ""

    ml_score: float = 0.0
    ml_model: str = ""

    docking_score: float = 999.0
    docking_rmsd: float = 999.0

    # Combined
    combined_score: float = 0.0
    evidence_level: str = "none"
    confidence: str = "low"

    metadata: dict[str, Any] = field(default_factory=dict)


# ── TargetProfileState — the top-level state container ───────────────────

@dataclass
class TargetProfileState:
    """Drug-target interaction state container.

    Design pattern
    --------------
    This class is the drug-domain analogue of ``ProcessState``.  Instead of a
    spatial grid we have a ``pairs`` DataFrame that holds every drug×target
    combination (the Cartesian product).  Each operator adds prediction columns
    to this DataFrame, accumulating evidence through the pipeline.
    """

    state_id: str
    molecules: pd.DataFrame       # columns: mol_id, smiles, descriptors, fingerprints...
    targets: pd.DataFrame         # columns: target_id, uniprot_id, sequence, class...
    pairs: pd.DataFrame           # the core grid — drug × target Cartesian product
    metadata: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def clone(
        self,
        *,
        state_id: str,
        history_event: dict[str, Any] | None = None,
    ) -> "TargetProfileState":
        """Return a deep-enough copy with new state id and optional history."""
        history = [*self.history]
        if history_event is not None:
            history.append(history_event)
        return TargetProfileState(
            state_id=state_id,
            molecules=self.molecules.copy(),
            targets=self.targets.copy(),
            pairs=self.pairs.copy(),
            metadata=dict(self.metadata),
            history=history,
        )

    def with_pairs(
        self,
        pairs: pd.DataFrame,
        *,
        state_id: str,
        history_event: dict[str, Any],
    ) -> "TargetProfileState":
        """Return a new state with replaced pairs DataFrame."""
        return TargetProfileState(
            state_id=state_id,
            molecules=self.molecules.copy(),
            targets=self.targets.copy(),
            pairs=pairs,
            metadata=dict(self.metadata),
            history=[*self.history, history_event],
        )

    @classmethod
    def from_molecule_records(
        cls,
        molecules: list[MoleculeRecord],
        targets: list[TargetRecord],
        *,
        state_id: str = "initial",
    ) -> "TargetProfileState":
        """Build a TargetProfileState from molecule and target record lists.

        The ``pairs`` DataFrame is the Cartesian product: every molecule ×
        every target.
        """
        mol_rows = []
        for m in molecules:
            fp = m.fingerprint_ecfp4
            mol_rows.append({
                "mol_id": m.mol_id,
                "smiles": m.smiles,
                "inchi_key": m.inchi_key,
                "mw": m.mw,
                "logp": m.logp,
                "hbd": m.hbd,
                "hba": m.hba,
                "tpsa": m.tpsa,
                "rotatable_bonds": m.rotatable_bonds,
                "ring_count": m.ring_count,
                "fingerprint_ecfp4": fp.tolist() if fp is not None else None,
            })
        mol_df = pd.DataFrame(mol_rows)

        tgt_rows = []
        for t in targets:
            tgt_rows.append({
                "target_id": t.target_id,
                "uniprot_id": t.uniprot_id,
                "gene_name": t.gene_name,
                "protein_name": t.protein_name,
                "organism": t.organism,
                "target_class": t.target_class,
                "sequence": t.sequence,
            })
        tgt_df = pd.DataFrame(tgt_rows)

        # Cartesian product
        mol_df["_key"] = 1
        tgt_df["_key"] = 1
        pairs = mol_df.merge(tgt_df, on="_key").drop(columns=["_key"])
        pairs["pair_id"] = pairs["mol_id"] + "_" + pairs["target_id"]

        # Initialise evidence columns
        for col in [
            "knowledge_hit", "knowledge_score", "knowledge_source",
            "similarity_hit", "similarity_score", "similarity_analog",
            "ml_score", "ml_model",
            "docking_score", "docking_rmsd",
            "combined_score", "evidence_level", "confidence",
        ]:
            if col not in pairs.columns:
                if col in ("knowledge_hit", "similarity_hit"):
                    pairs[col] = False
                elif col in ("evidence_level",):
                    pairs[col] = "none"
                elif col in ("confidence",):
                    pairs[col] = "low"
                elif col in ("knowledge_source", "similarity_analog", "ml_model"):
                    pairs[col] = ""
                else:
                    pairs[col] = 0.0

        return cls(
            state_id=state_id,
            molecules=mol_df,
            targets=tgt_df,
            pairs=pairs,
            metadata={"source": "from_molecule_records"},
        )

    def summary(self) -> dict[str, Any]:
        """Return compact summary for reports."""
        pairs = self.pairs
        return {
            "state_id": self.state_id,
            "n_molecules": int(len(self.molecules)),
            "n_targets": int(len(self.targets)),
            "n_pairs": int(len(pairs)),
            "knowledge_hits": int(pairs["knowledge_hit"].sum()) if "knowledge_hit" in pairs else 0,
            "similarity_inferred": int(pairs["similarity_hit"].sum()) if "similarity_hit" in pairs else 0,
            "ml_predicted": int((pairs.get("ml_score", 0.0) > 0.5).sum()),
            "docking_validated": int((pairs.get("docking_score", 999.0) < -7.0).sum()),
        }
