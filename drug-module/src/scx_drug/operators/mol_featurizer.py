"""Molecular feature extraction operator.

Parses SMILES strings and computes molecular descriptors and fingerprints
using RDKit.  This is the drug-module analogue of ``scx.features.FeatureExtractor``.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from scx_drug.operators.base import DrugOperator, DrugStepContext, next_state
from scx_drug.state import MoleculeRecord, TargetProfileState

# RDKit is an optional dependency; the operator imports it lazily so that
# the drug module can be imported even without RDKit installed.
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, MACCSkeys
    from rdkit.Chem import rdMolDescriptors as rdmd

    HAS_RDKIT = True
except ImportError:  # pragma: no cover
    HAS_RDKIT = False


class MoleculeFeaturizeOperator:
    """Parse SMILES and compute molecular descriptors + fingerprints.

    Reads a ``TargetProfileState`` whose ``molecules`` DataFrame contains a
    ``smiles`` column and writes computed descriptors and fingerprint columns.

    Recipe keys
    -----------
    fingerprint_types : list[str]
        Which fingerprints to compute.  Supported: ``"ecfp4"``, ``"maccs"``,
        ``"morgan2"`` (alias for ECFP4 folded to 2048 bits), ``"rdkit"``
        (2048-bit RDKit topological fingerprint).  Default: ``["ecfp4"]``.
    descriptor_list : list[str] | "all"
        Which RDKit descriptors to compute.  ``"all"`` computes everything.
        Default: ``["MolWt", "MolLogP", "NumHDonors", "NumHAcceptors",
        "TPSA", "NumRotatableBonds", "RingCount", "FractionCSP3"]``.
    add_hydrogens : bool
        Whether to add explicit hydrogens before computing.  Default ``False``.
    sanitize : bool
        Whether to sanitize molecules.  Default ``True``.
    """

    name = "molecule_featurize"

    # Default descriptors (lightweight, interpretable)
    DEFAULT_DESCRIPTORS = [
        "MolWt",
        "MolLogP",
        "NumHDonors",
        "NumHAcceptors",
        "TPSA",
        "NumRotatableBonds",
        "RingCount",
        "FractionCSP3",
        "HeavyAtomCount",
        "NHOHCount",
        "NOCount",
        "NumAromaticRings",
        "NumSaturatedRings",
        "NumAliphaticRings",
        "qed",
    ]

    def __init__(self) -> None:
        if not HAS_RDKIT:
            raise ImportError(
                "MoleculeFeaturizeOperator requires RDKit.  "
                "Install it with: pip install rdkit"
            )

    # ── Public API ──────────────────────────────────────────────────────

    def apply(
        self,
        state: TargetProfileState,
        context: DrugStepContext,
    ) -> TargetProfileState:
        out = next_state(state, context)
        recipe = context.recipe
        fp_types = recipe.get("fingerprint_types", ["ecfp4"])
        desc_list = recipe.get("descriptor_list", self.DEFAULT_DESCRIPTORS)
        add_h = bool(recipe.get("add_hydrogens", False))
        sanitize = bool(recipe.get("sanitize", True))

        # Parse every SMILES in the molecules DataFrame
        mol_objects: dict[str, Chem.rdchem.Mol] = {}
        for _, row in out.molecules.iterrows():
            mol = Chem.MolFromSmiles(str(row["smiles"]), sanitize=sanitize)
            if mol is None:
                mol_objects[row["mol_id"]] = Chem.MolFromSmiles("C")  # fallback: methane
            else:
                if add_h:
                    mol = Chem.AddHs(mol)
                mol_objects[row["mol_id"]] = mol

        # Compute descriptors
        mol_df = out.molecules.copy()
        if desc_list == "all":
            desc_names = [desc_name for desc_name, _ in Descriptors._descList]
        else:
            desc_names = list(desc_list)

        for desc_name in desc_names:
            fn = getattr(Descriptors, desc_name, None)
            if fn is None:
                continue
            col_name = desc_name.lower()
            values = []
            for _, row in mol_df.iterrows():
                mol = mol_objects.get(row["mol_id"])
                if mol is not None:
                    values.append(float(fn(mol)))
                else:
                    values.append(0.0)
            mol_df[col_name] = values

        # Compute fingerprints
        for fp_type in fp_types:
            fp_arrays = []
            for _, row in mol_df.iterrows():
                mol = mol_objects.get(row["mol_id"])
                fp_array = self._compute_fingerprint(mol, fp_type)
                fp_arrays.append(fp_array)
            # Store fingerprint as numpy array in a column
            # We use object dtype so each cell holds a 1-D numpy array
            mol_df[f"fp_{fp_type}"] = fp_arrays

        out.molecules = mol_df
        return out

    # ── Static helpers ──────────────────────────────────────────────────

    @staticmethod
    def featurize_single(smiles: str, fp_types: list[str] | None = None) -> MoleculeRecord:
        """Convenience: featurize a single SMILES into a MoleculeRecord.

        Does NOT require a full TargetProfileState.
        """
        if not HAS_RDKIT:
            raise ImportError("RDKit is required for MoleculeFeaturizeOperator")
        if fp_types is None:
            fp_types = ["ecfp4"]

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"RDKit could not parse SMILES: {smiles}")

        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        tpsa = Descriptors.TPSA(mol)
        rot = Descriptors.NumRotatableBonds(mol)
        rings = Descriptors.RingCount(mol)

        fps: dict[str, np.ndarray] = {}
        for ft in fp_types:
            fps[ft] = MoleculeFeaturizeOperator._compute_fingerprint(mol, ft)

        return MoleculeRecord(
            mol_id=Chem.MolToInchiKey(mol)[:14] if mol else "unknown",
            smiles=smiles,
            inchi_key=Chem.MolToInchiKey(mol) if mol else "",
            mw=float(mw),
            logp=float(logp),
            hbd=int(hbd),
            hba=int(hba),
            tpsa=float(tpsa),
            rotatable_bonds=int(rot),
            ring_count=int(rings),
            fingerprint_ecfp4=fps.get("ecfp4"),
        )

    # ── Internal helpers ────────────────────────────────────────────────

    @staticmethod
    def _compute_fingerprint(
        mol: Chem.rdchem.Mol | None,
        fp_type: str,
    ) -> np.ndarray:
        """Compute a fingerprint for a single RDKit Mol."""
        if mol is None:
            return np.zeros(2048, dtype=np.float64)

        if fp_type in ("ecfp4", "morgan2"):
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
            arr = np.zeros(2048, dtype=np.float64)
            Chem.DataStructs.ConvertToNumpyArray(fp, arr)
            return arr

        if fp_type == "maccs":
            fp = MACCSkeys.GenMACCSKeys(mol)
            arr = np.zeros(167, dtype=np.float64)
            Chem.DataStructs.ConvertToNumpyArray(fp, arr)
            return arr

        if fp_type == "rdkit":
            fp = Chem.RDKFingerprint(mol, fpSize=2048)
            arr = np.zeros(2048, dtype=np.float64)
            Chem.DataStructs.ConvertToNumpyArray(fp, arr)
            return arr

        raise ValueError(
            f"Unknown fingerprint type: {fp_type}. "
            f"Supported: ecfp4, morgan2, maccs, rdkit"
        )
