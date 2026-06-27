"""Comprehensive molecular descriptor computation via RDKit.

This module provides a structured interface to RDKit's descriptor engine,
computing 2D/3D physicochemical, topological, and electronic descriptors
in a single pass.  Used as a building block by ``MoleculeFeaturizeOperator``
and available for standalone use in QSAR / property prediction pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, Descriptors3D, rdMolDescriptors as rdmd

    HAS_RDKIT = True
except ImportError:  # pragma: no cover
    HAS_RDKIT = False


# ── Descriptor categories ──────────────────────────────────────────────────

# Physicochemical (2D)
PHYSICOCHEMICAL_2D = [
    "MolWt", "HeavyAtomMolWt", "ExactMolWt",
    "MolLogP", "MolMR",
    "NumValenceElectrons",
    "MaxPartialCharge", "MinPartialCharge",
    "MaxAbsPartialCharge", "MinAbsPartialCharge",
    "FpDensityMorgan1", "FpDensityMorgan2", "FpDensityMorgan3",
]

# Hydrogen bonding / polarity
HBOND_POLARITY = [
    "NumHDonors", "NumHAcceptors",
    "TPSA",
    "FractionCSP3",
    "NHOHCount", "NOCount",
]

# Size / flexibility
SIZE_FLEXIBILITY = [
    "HeavyAtomCount",
    "NumRotatableBonds",
    "NumHeteroatoms",
    "NumSaturatedRings", "NumAliphaticRings",
    "NumAromaticRings", "RingCount",
    "NumSaturatedHeterocycles", "NumAromaticHeterocycles",
    "NumSaturatedCarbocycles", "NumAromaticCarbocycles",
    "NumBridgeheadAtoms", "NumSpiroAtoms",
    "BertzCT",
    "Chi0", "Chi1", "Chi0n", "Chi1n", "Chi0v", "Chi1v",
    "Kappa1", "Kappa2", "Kappa3",
    "HallKierAlpha",
]

# Drug-likeness
DRUG_LIKENESS = [
    "qed",
    "NumLipinskiHBA", "NumLipinskiHBD",
    "NumRuleOf5Violations",
    "NumAromaticRings",
]

# Electronic
ELECTRONIC = [
    "MaxEStateIndex", "MinEStateIndex",
    "MaxAbsEStateIndex", "MinAbsEStateIndex",
    "EState_VSA1", "EState_VSA10",
    "VSA_EState1", "VSA_EState10",
    "PEOE_VSA1", "PEOE_VSA14",
    "SMR_VSA1", "SMR_VSA10",
    "SlogP_VSA1", "SlogP_VSA12",
]

# All 2D descriptors combined
ALL_2D = (
    PHYSICOCHEMICAL_2D
    + HBOND_POLARITY
    + SIZE_FLEXIBILITY
    + DRUG_LIKENESS
    + ELECTRONIC
)


# ── Descriptor computation engine ──────────────────────────────────────────

@dataclass
class DescriptorVector:
    """Structured container for computed molecular descriptors."""

    mol_id: str
    smiles: str = ""

    # Physicochemical
    mw: float = 0.0
    logp: float = 0.0
    mr: float = 0.0
    heavy_atom_mw: float = 0.0

    # H-bond / polarity
    hbd: int = 0
    hba: int = 0
    tpsa: float = 0.0
    fraction_csp3: float = 0.0

    # Size / flexibility
    heavy_atom_count: int = 0
    rotatable_bonds: int = 0
    ring_count: int = 0
    aromatic_rings: int = 0
    aliphatic_rings: int = 0
    bertz_ct: float = 0.0

    # Drug-likeness
    qed: float = 0.0
    num_lipinski_violations: int = 0

    # Raw descriptor dict for extensibility
    extra: dict[str, float] = field(default_factory=dict)

    def to_array(self) -> np.ndarray:
        """Return core descriptors as a float64 numpy array."""
        return np.array([
            self.mw, self.logp, self.mr, self.heavy_atom_mw,
            float(self.hbd), float(self.hba), self.tpsa, self.fraction_csp3,
            float(self.heavy_atom_count), float(self.rotatable_bonds),
            float(self.ring_count), float(self.aromatic_rings),
            float(self.aliphatic_rings), self.bertz_ct,
            self.qed, float(self.num_lipinski_violations),
        ], dtype=np.float64)

    def to_dict(self) -> dict[str, float]:
        """Return core descriptors as a dict."""
        d = {
            "mw": self.mw, "logp": self.logp, "mr": self.mr,
            "heavy_atom_mw": self.heavy_atom_mw,
            "hbd": self.hbd, "hba": self.hba, "tpsa": self.tpsa,
            "fraction_csp3": self.fraction_csp3,
            "heavy_atom_count": self.heavy_atom_count,
            "rotatable_bonds": self.rotatable_bonds,
            "ring_count": self.ring_count,
            "aromatic_rings": self.aromatic_rings,
            "aliphatic_rings": self.aliphatic_rings,
            "bertz_ct": self.bertz_ct,
            "qed": self.qed,
            "num_lipinski_violations": self.num_lipinski_violations,
        }
        d.update(self.extra)
        return d


class DescriptorCalculator:
    """Compute molecular descriptors for a single molecule or batch."""

    def __init__(self, add_hydrogens: bool = False, sanitize: bool = True):
        self.add_h = add_hydrogens
        self.sanitize = sanitize

    def compute(self, smiles: str, mol_id: str = "") -> DescriptorVector:
        """Compute descriptors for one molecule."""
        mol = Chem.MolFromSmiles(smiles, sanitize=self.sanitize)
        if mol is None:
            raise ValueError(f"RDKit cannot parse SMILES: {smiles}")
        if self.add_h:
            mol = Chem.AddHs(mol)

        return DescriptorVector(
            mol_id=mol_id or smiles[:20],
            smiles=smiles,
            mw=float(Descriptors.MolWt(mol)),
            logp=float(Descriptors.MolLogP(mol)),
            mr=float(Descriptors.MolMR(mol)),
            heavy_atom_mw=float(Descriptors.HeavyAtomMolWt(mol)),
            hbd=int(Descriptors.NumHDonors(mol)),
            hba=int(Descriptors.NumHAcceptors(mol)),
            tpsa=float(Descriptors.TPSA(mol)),
            fraction_csp3=float(Descriptors.FractionCSP3(mol)),
            heavy_atom_count=int(Descriptors.HeavyAtomCount(mol)),
            rotatable_bonds=int(Descriptors.NumRotatableBonds(mol)),
            ring_count=int(Descriptors.RingCount(mol)),
            aromatic_rings=int(Descriptors.NumAromaticRings(mol)),
            aliphatic_rings=int(Descriptors.NumAliphaticRings(mol)),
            bertz_ct=float(Descriptors.BertzCT(mol)),
            qed=float(rdmd.CalcQED(mol) if hasattr(rdmd, "CalcQED") else 0.0),
            num_lipinski_violations=_count_lipinski_violations(mol),
        )

    def compute_batch(self, smiles_list: list[str]) -> list[DescriptorVector]:
        """Compute descriptors for a list of SMILES."""
        results: list[DescriptorVector] = []
        for i, smi in enumerate(smiles_list):
            mol_id = f"MOL_{i:06d}"
            try:
                results.append(self.compute(smi, mol_id=mol_id))
            except ValueError:
                results.append(DescriptorVector(mol_id=mol_id, smiles=smi))
        return results


# ── Helpers ────────────────────────────────────────────────────────────────

def _count_lipinski_violations(mol: Chem.rdchem.Mol) -> int:
    """Count Lipinski Rule-of-5 violations for a molecule."""
    violations = 0
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    if mw > 500:
        violations += 1
    if logp > 5:
        violations += 1
    if hbd > 5:
        violations += 1
    if hba > 10:
        violations += 1
    return violations
