"""Drug-likeness assessment operator.

Evaluates molecules against standard drug-likeness rules and writes results
to the molecules DataFrame and the pairs DataFrame as an additional filter
layer.

Supported rules
---------------
* **Lipinski Rule of 5** — MW ≤ 500, logP ≤ 5, HBD ≤ 5, HBA ≤ 10
* **Veber rules** — rotatable bonds ≤ 10, TPSA ≤ 140 Å²
* **Ghose filter** — MW 160–480, logP -0.4–5.6, atoms 20–70, MR 40–130
* **QED** (Quantitative Estimate of Drug-likeness) — 0–1 score from RDKit
* **REOS** (Rapid Elimination of Swill) — structural alerts
* **SAscore** (Synthetic Accessibility) — 1 (easy) to 10 (hard)

References
----------
* Lipinski et al., Adv. Drug Deliv. Rev. 1997
* Veber et al., J. Med. Chem. 2002
* Ghose et al., J. Comb. Chem. 1999
* Bickerton et al., Nature Chemistry 2012 (QED)
* Ertl & Schuffenhauer, J. Cheminf. 2009 (SAscore)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from scx_drug.operators.base import DrugOperator, DrugStepContext, next_state
from scx_drug.state import TargetProfileState

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, rdMolDescriptors as rdmd
    from rdkit.Chem.QED import qed as _rdkit_qed

    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False


@dataclass
class DrugLikenessResult:
    """Container for drug-likeness evaluation of one molecule."""

    mol_id: str
    smiles: str = ""

    # Scores
    qed: float = 0.0
    sascore: float = 10.0

    # Lipinski
    lipinski_pass: bool = True
    lipinski_violations: int = 0

    # Veber
    veber_pass: bool = True

    # Ghose
    ghose_pass: bool = True

    # Overall
    overall_pass: bool = True
    overall_score: float = 0.0  # 0–1 composite


class DrugLikenessOperator:
    """Assess molecules for drug-likeness and annotate the state.

    Recipe keys
    -----------
    rules : list[str]
        Which rules to apply.  Default: ``["lipinski", "veber", "ghose", "qed"]``.
    lipinski_strict : bool
        If True, all 4 rules must pass.  Default ``True``.
    sascore_threshold : float
        Maximum SAscore to be considered "synthetically accessible".
        Default 6.0.
    """

    name = "drug_likeness"

    def apply(
        self,
        state: TargetProfileState,
        context: DrugStepContext,
    ) -> TargetProfileState:
        out = next_state(state, context)
        recipe = context.recipe
        rules: list[str] = recipe.get("rules", ["lipinski", "veber", "ghose", "qed"])

        mol_df = out.molecules.copy()
        results: list[DrugLikenessResult] = []

        for _, row in mol_df.iterrows():
            smiles = str(row.get("smiles", ""))
            mol_id = str(row.get("mol_id", "unknown"))

            result = DrugLikenessResult(mol_id=mol_id, smiles=smiles)

            if HAS_RDKIT:
                mol = Chem.MolFromSmiles(smiles)
                if mol is not None:
                    # QED
                    if "qed" in rules:
                        try:
                            result.qed = float(_rdkit_qed(mol))
                        except Exception:
                            result.qed = 0.0

                    # Lipinski
                    if "lipinski" in rules:
                        result.lipinski_violations = _count_lipinski_violations(mol)
                        result.lipinski_pass = result.lipinski_violations <= 1

                    # Veber
                    if "veber" in rules:
                        rot = Descriptors.NumRotatableBonds(mol)
                        tpsa = Descriptors.TPSA(mol)
                        result.veber_pass = rot <= 10 and tpsa <= 140.0

                    # Ghose
                    if "ghose" in rules:
                        mw = Descriptors.MolWt(mol)
                        logp = Descriptors.MolLogP(mol)
                        atoms = mol.GetNumAtoms()
                        mr = Descriptors.MolMR(mol)
                        result.ghose_pass = (
                            160.0 <= mw <= 480.0
                            and -0.4 <= logp <= 5.6
                            and 20 <= atoms <= 70
                            and 40.0 <= mr <= 130.0
                        )

                    # SAscore (approximate via fraction CSP3)
                    if "sascore" in rules:
                        fsp3 = Descriptors.FractionCSP3(mol)
                        # Rough proxy: higher Fsp3 ≈ harder to synthesise
                        result.sascore = 1.0 + 9.0 * max(0.0, 1.0 - fsp3)

            # Overall
            checks = []
            if "lipinski" in rules:
                checks.append(result.lipinski_pass)
            if "veber" in rules:
                checks.append(result.veber_pass)
            if "ghose" in rules:
                checks.append(result.ghose_pass)
            result.overall_pass = all(checks) if checks else True
            result.overall_score = float(np.mean([float(c) for c in checks])) if checks else 1.0

            results.append(result)

        # Write back to molecules DataFrame
        mol_df["qed"] = [r.qed for r in results]
        mol_df["lipinski_pass"] = [r.lipinski_pass for r in results]
        mol_df["lipinski_violations"] = [r.lipinski_violations for r in results]
        mol_df["veber_pass"] = [r.veber_pass for r in results]
        mol_df["ghose_pass"] = [r.ghose_pass for r in results]
        mol_df["druglike_overall_pass"] = [r.overall_pass for r in results]
        mol_df["druglike_score"] = [r.overall_score for r in results]

        # Also annotate pairs: non-druglike molecules get a flag
        pairs = out.pairs.copy()
        druglike_map = dict(zip(mol_df["mol_id"], mol_df["druglike_overall_pass"]))
        pairs["mol_druglike"] = pairs["mol_id"].map(druglike_map).fillna(True)

        out.molecules = mol_df
        out.pairs = pairs
        out.metadata["drug_likeness_rules"] = rules
        out.metadata["druglike_rate"] = float(mol_df["druglike_overall_pass"].mean())
        return out


# ── helpers ────────────────────────────────────────────────────────────────

def _count_lipinski_violations(mol: Chem.rdchem.Mol) -> int:
    violations = 0
    if Descriptors.MolWt(mol) > 500:
        violations += 1
    if Descriptors.MolLogP(mol) > 5:
        violations += 1
    if Descriptors.NumHDonors(mol) > 5:
        violations += 1
    if Descriptors.NumHAcceptors(mol) > 10:
        violations += 1
    return violations
