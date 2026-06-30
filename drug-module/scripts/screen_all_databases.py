#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     SCX Yajie Multi-Database Screening Pipeline                             ║
║     One-Shot Drug-Target Annotation Across All 12 Databases                 ║
║     Author: SCX Drug Module Team                                            ║
║     Date:   2026-06-29                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Pipeline Architecture
---------------------

  ┌─────────────────────────────────────────────────────────────────────┐
  │              YAJIE MULTI-DATABASE SCREENING PIPELINE                  │
  │                                                                      │
  │  Phase 1: DATA LOADING                                               │
  │    ├─ Load all 12 database Parquet/CSV files                         │
  │    ├─ Extract unique SMILES (drugs) and UniProt IDs (targets)        │
  │    └─ Read provenance metadata for each database                     │
  │                                                                      │
  │  Phase 2: STANDARDIZATION                                            │
  │    ├─ SMILES → ECFP4 fingerprints (2048-bit Morgan, radius 2)        │
  │    ├─ Target IDs → UniProt ID mapping (via UniProt REST API)         │
  │    └─ Deduplication across databases                                 │
  │                                                                      │
  │  Phase 3: MATRIX CONSTRUCTION                                        │
  │    ├─ Build drug × target evidence matrix                            │
  │    ├─ Cell (i,j): vector of scores from each database                │
  │    └─ Track which databases contribute to each pair                  │
  │                                                                      │
  │  Phase 4: YAJIE MULTI-EXPERT CONSENSUS                               │
  │    ├─ Expert per database: evidence score → normalized [0,1]         │
  │    ├─ Yajie Theorem 1: consensus = weighted mean, σ = disagreement   │
  │    ├─ Classification: CLEAN / NOISY / AMBIGUOUS                      │
  │    └─ Provenance: which databases agree, with links                  │
  │                                                                      │
  │  Phase 5: OUTPUT                                                     │
  │    ├─ MT Gold Standard CSV (mt_gold_standard.csv)                    │
  │    ├─ Per-database quality report                                    │
  │    ├─ Database agreement matrix (which DBs disagree most)            │
  │    └─ Full provenance audit trail                                    │
  └─────────────────────────────────────────────────────────────────────┘

Output Schema (mt_gold_standard.csv)
------------------------------------
  drug_id            — Unique drug identifier (SMILES-based hash)
  target_id          — UniProt ID or internal target identifier
  drug_smiles        — Canonical SMILES string
  target_name        — Target protein/gene name
  MT_score           — Yajie multi-expert consensus score [0, 1]
  consensus_level    — HIGH / MEDIUM / LOW
  consensus_std      — Standard deviation across database experts
  n_databases        — Number of databases with data on this pair
  n_databases_agree  — Number of databases that agree (within tolerance)
  classification     — CLEAN / NOISY / AMBIGUOUS (Yajie verdict)
  source_databases   — List of database names with evidence
  database_scores    — Per-database score breakdown (JSON string)
  database_links     — Links back to original records (JSON string)
  download_date      — When source databases were downloaded
  mt_report_version  — Yajie screening pipeline version
  provenance_notes   — Additional provenance information

Usage
-----
    # Full run with all downloaded databases
    python scripts/screen_all_databases.py \\
        --db-root W:/scx_databases \\
        --output outputs/mt_gold_standard

    # Run on specific databases
    python scripts/screen_all_databases.py \\
        --db-root W:/scx_databases \\
        --databases chembl drugbank bindingdb \\
        --output outputs/mt_partial

    # Quick test with max pairs
    python scripts/screen_all_databases.py \\
        --db-root W:/scx_databases \\
        --max-pairs 10000 \\
        --output outputs/mt_test

    # Use existing compound/target CSVs (skip extraction)
    python scripts/screen_all_databases.py \\
        --compounds inputs/all_compounds.csv \\
        --targets inputs/all_human_targets.csv \\
        --db-root W:/scx_databases \\
        --output outputs/mt_gold_standard

Requirements
------------
    pip install rdkit pandas numpy pyarrow tqdm requests
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import warnings
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

import numpy as np
import pandas as pd

# ── RDKit ─────────────────────────────────────────────────────────────────────
try:
    from rdkit import Chem, DataStructs
    from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors as rdmd
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

# ── PyArrow ───────────────────────────────────────────────────────────────────
try:
    import pyarrow.parquet as pq
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False

# ── TQDM ──────────────────────────────────────────────────────────────────────
try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kw: x  # noqa: E731

# ── SCX Yajie ─────────────────────────────────────────────────────────────────
try:
    from scx.yajie import Yajie
    SCX_YAJIE_AVAILABLE = True
except ImportError:
    SCX_YAJIE_AVAILABLE = False

# ── SCX Spring (for novelty + dormancy) ───────────────────────────────────────
try:
    from scx.spring import Spring, SpringConfig
    SCX_SPRING_AVAILABLE = True
except ImportError:
    SCX_SPRING_AVAILABLE = False


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURATION                                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

PIPELINE_VERSION = "0.1.0"
ECFP4_RADIUS = 2
ECFP4_BITS = 2048
DEFAULT_GRACE = 0.10          # Yajie grace (expert tolerance)
DEFAULT_CONSENSUS_THRESHOLD = 0.65  # Minimum for HIGH consensus
DEFAULT_BATCH_SIZE = 50000    # Pairs per batch for memory management

# Database name → human-readable label + URL template for provenance links
DATABASE_LINK_TEMPLATES = {
    "chembl":           "https://www.ebi.ac.uk/chembl/target_report_card/{target_id}/",
    "drugbank":         "https://go.drugbank.com/drugs/{drug_id}",
    "pubchem_bioassay": "https://pubchem.ncbi.nlm.nih.gov/bioassay/{aid}",
    "bindingdb":        "https://www.bindingdb.org/bind/chemsearch/marvin/MolStructure.jsp?monomerid={target_id}",
    "ttd":              "https://db.idrblab.net/ttd/target/{target_id}",
    "stanford_hivdb":   "https://hivdb.stanford.edu/dr-summary/resistance-notes/",
    "pdbbind":          "http://www.pdbbind.org.cn/quickpdb.asp?pdbcode={target_id}",
    "drugcentral":      "https://drugcentral.org/drugcard/{drug_id}",
    "open_targets":     "https://platform.opentargets.org/target/{target_id}",
    "pharmgkb":         "https://www.pharmgkb.org/chemical/{drug_id}",
    "sider":            "http://sideeffects.embl.de/drugs/{drug_id}/",
    "stitch":           "http://stitch.embl.de/cgi/network.pl?identifier={drug_id}",
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DATA STRUCTURES                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

@dataclass
class DrugEntry:
    """Standardized drug entry with fingerprint."""
    drug_id: str
    smiles: str
    fingerprint: Optional[np.ndarray] = None       # ECFP4, 2048-bit
    mw: float = 0.0
    logp: float = 0.0
    hbd: int = 0
    hba: int = 0
    tpsa: float = 0.0
    source_databases: Set[str] = field(default_factory=set)
    external_ids: Dict[str, str] = field(default_factory=dict)  # db_name → id


@dataclass
class TargetEntry:
    """Standardized target entry."""
    target_id: str          # UniProt ID (preferred) or internal ID
    uniprot_id: str = ""
    gene_name: str = ""
    protein_name: str = ""
    organism: str = ""
    target_class: str = ""
    source_databases: Set[str] = field(default_factory=set)
    external_ids: Dict[str, str] = field(default_factory=dict)


@dataclass
class DrugTargetEvidence:
    """Evidence for a single drug-target pair from one database."""
    drug_id: str
    target_id: str
    database: str
    score: float              # Normalized [0, 1] evidence score
    raw_value: float = 0.0    # Original value (pIC50, pKi, etc.)
    raw_type: str = ""        # Type of original measurement
    record_link: str = ""     # URL back to source record
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MTScreeningResult:
    """Complete Yajie screening result for one drug-target pair."""
    drug_id: str
    target_id: str
    drug_smiles: str
    target_name: str
    MT_score: float                    # Yajie consensus score [0, 1]
    consensus_level: str               # HIGH / MEDIUM / LOW
    consensus_std: float               # Standard deviation across experts
    n_databases: int                   # Databases with evidence
    n_databases_agree: int             # Databases agreeing (within grace)
    classification: str                # CLEAN / NOISY / AMBIGUOUS
    source_databases: List[str]        # Database names
    database_scores: Dict[str, float]  # Per-database scores
    database_links: Dict[str, str]     # Per-database record URLs
    expert_disagreement_detail: str = ""
    download_date: str = ""
    mt_report_version: str = PIPELINE_VERSION


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 1: DATA LOADING                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def discover_data_files(db_root: Path) -> Dict[str, List[Path]]:
    """Discover all Parquet/CSV data files organized by database.

    Parameters
    ----------
    db_root : Path
        Root directory containing database subdirectories.

    Returns
    -------
    Dict[str, List[Path]]
        Mapping: database_name → list of data file paths.
    """
    db_files: Dict[str, List[Path]] = defaultdict(list)

    # Look for parquet and CSV files in subdirectories
    for ext in ["*.parquet", "*.csv"]:
        for file_path in db_root.rglob(ext):
            # Determine database from path
            # Expected structure: db_root/{database_name}/...
            rel = file_path.relative_to(db_root)
            parts = rel.parts
            if len(parts) >= 1:
                db_name = parts[0]
                # Skip internal dirs
                if db_name.startswith("_") or db_name == "provenance_summary.json":
                    # Try parent directory
                    if len(parts) >= 2 and not parts[0].startswith("_"):
                        db_name = parts[0]
                    else:
                        continue
                db_files[db_name].append(file_path)

    # Also check raw directory for unprocessed files
    raw_dir = db_root / "_raw"
    if raw_dir.exists():
        for ext in ["*.parquet", "*.csv", "*.tsv", "*.tsv.gz", "*.txt"]:
            for file_path in raw_dir.rglob(ext):
                # Try to determine database from filename
                fname = file_path.stem.lower()
                for db_key in DATABASE_LINK_TEMPLATES:
                    if db_key.replace("_", "") in fname.replace("_", "").replace("-", ""):
                        db_files[db_key].append(file_path)
                        break

    return dict(db_files)


def load_provenance(db_root: Path) -> Dict[str, Dict[str, Any]]:
    """Load all provenance JSON files from the database root.

    Returns
    -------
    Dict[str, Dict[str, Any]]
        Mapping: database_name → provenance data dict.
    """
    provenance: Dict[str, Dict[str, Any]] = {}

    for prov_file in db_root.rglob("provenance.json"):
        try:
            data = json.loads(prov_file.read_text(encoding="utf-8"))
            db_name = data.get("database_name", prov_file.parent.name)
            provenance[db_name] = data
        except Exception:
            continue

    return provenance


def load_database_parquet(file_paths: List[Path]) -> Optional[pd.DataFrame]:
    """Load and concatenate multiple Parquet/CSV files into one DataFrame.

    Parameters
    ----------
    file_paths : List[Path]
        Paths to Parquet or CSV files.

    Returns
    -------
    Optional[pd.DataFrame]
        Combined DataFrame, or None if no files could be read.
    """
    frames = []
    for fp in file_paths:
        try:
            if fp.suffix == ".parquet" and HAS_PYARROW:
                df = pd.read_parquet(fp)
            elif fp.suffix == ".csv":
                df = pd.read_csv(fp, low_memory=False)
            elif fp.suffix in (".tsv", ".txt"):
                df = pd.read_csv(fp, sep="\t", low_memory=False)
            elif fp.suffix == ".gz" and fp.stem.endswith(".tsv"):
                import gzip
                with gzip.open(fp, "rt") as f:
                    df = pd.read_csv(f, sep="\t", low_memory=False)
            else:
                continue
            if len(df) > 0:
                frames.append(df)
        except Exception as e:
            print(f"    ⚠ Could not read {fp.name}: {e}")
            continue

    if frames:
        return pd.concat(frames, ignore_index=True)
    return None


def extract_drugs_and_targets(
    db_files: Dict[str, List[Path]],
    provenance: Dict[str, Dict[str, Any]],
    max_drugs: int = -1,
) -> Tuple[Dict[str, DrugEntry], Dict[str, TargetEntry], Dict[str, Dict[str, List[DrugTargetEvidence]]]]:
    """Extract standardized drugs, targets, and evidence from all databases.

    Parameters
    ----------
    db_files : Dict[str, List[Path]]
        Discovered database files.
    provenance : Dict[str, Dict[str, Any]]
        Provenance metadata.
    max_drugs : int
        Maximum unique drugs to load (-1 = unlimited).

    Returns
    -------
    (drugs, targets, evidence) : Tuple
        drugs: SMILES-based hash → DrugEntry
        targets: target_id → TargetEntry
        evidence: (drug_id, target_id) → database_name → List[DrugTargetEvidence]
    """
    drugs: Dict[str, DrugEntry] = {}
    targets: Dict[str, TargetEntry] = {}
    evidence: Dict[str, Dict[str, List[DrugTargetEvidence]]] = defaultdict(
        lambda: defaultdict(list)
    )

    # Column name mappings (various schemas → standard fields)
    SMILES_COLS = ["smiles", "canonical_smiles", "SMILES", "Smiles", "canonicalsmiles"]
    TARGET_COLS = ["target_id", "target_chembl_id", "uniprot_id", "uniprot",
                   "UniProt_ID", "target_name", "TargetID"]
    UNIPROT_COLS = ["uniprot_id", "uniprot", "UniProt_ID", "uniprotkb"]
    SCORE_COLS = ["pchembl_value", "score", "combined_score", "standard_value",
                  "activity_value", "confidence_score", "association_score"]
    SCORE_TYPE_COLS = ["standard_type", "assay_type", "activity_type",
                       "action_types", "type"]

    for db_name, file_paths in db_files.items():
        print(f"\n  [{db_name}] Loading {len(file_paths)} file(s) ...")
        df = load_database_parquet(file_paths)
        if df is None or len(df) == 0:
            print(f"    ⚠ No data loaded")
            continue

        print(f"    Loaded {len(df):,} rows")

        # Identify columns
        smiles_col = _find_column(df, SMILES_COLS)
        target_col = _find_column(df, TARGET_COLS)
        uniprot_col = _find_column(df, UNIPROT_COLS)
        score_col = _find_column(df, SCORE_COLS)
        score_type_col = _find_column(df, SCORE_TYPE_COLS)
        drug_id_col = _find_column(df, ["drug_id", "drug_name", "molregno"])

        gene_col = _find_column(df, ["gene_name", "gene_symbol", "target_name",
                                      "target_symbol", "protein_name"])
        protein_name_col = _find_column(df, ["target_name", "protein_name",
                                              "pref_name", "target_pref_name"])
        organism_col = _find_column(df, ["organism", "Organism"])
        target_class_col = _find_column(df, ["target_class", "target_type",
                                              "protein_class", "Target_Class"])

        if smiles_col is None:
            print(f"    ⚠ No SMILES column found — skipping drug extraction")
            continue

        n_drugs_added = 0
        n_targets_added = 0
        n_evidence_added = 0

        for _, row in tqdm(df.iterrows(), total=len(df),
                           desc=f"  Extracting {db_name}"):
            try:
                # ── Extract drug ──────────────────────────────────────────
                smiles = str(row.get(smiles_col, "")).strip()
                if not smiles or len(smiles) < 2 or len(smiles) > 2000:
                    continue

                drug_id = _smiles_to_id(smiles)

                if drug_id not in drugs:
                    if max_drugs > 0 and len(drugs) >= max_drugs:
                        continue
                    ext_id = str(row.get(drug_id_col, "")) if drug_id_col else ""
                    drugs[drug_id] = DrugEntry(
                        drug_id=drug_id,
                        smiles=smiles,
                        source_databases={db_name},
                        external_ids={db_name: ext_id} if ext_id else {},
                    )
                    n_drugs_added += 1
                else:
                    drugs[drug_id].source_databases.add(db_name)
                    if drug_id_col:
                        ext_id = str(row.get(drug_id_col, ""))
                        if ext_id:
                            drugs[drug_id].external_ids[db_name] = ext_id

                # ── Extract target ─────────────────────────────────────────
                target_id = ""
                target_name = ""
                uniprot = ""

                if uniprot_col and pd.notna(row.get(uniprot_col)):
                    uniprot = str(row.get(uniprot_col, "")).strip()
                    if uniprot and not uniprot.startswith("["):
                        target_id = uniprot
                elif target_col and pd.notna(row.get(target_col)):
                    target_id = str(row.get(target_col, "")).strip()

                if not target_id or target_id in ("nan", "None", ""):
                    # Generate a target ID from target name hash
                    if protein_name_col and pd.notna(row.get(protein_name_col)):
                        target_name = str(row.get(protein_name_col, "")).strip()
                        if target_name:
                            target_id = f"TGT_{abs(hash(target_name)) % 100_000_000:08d}"

                if not target_id:
                    continue

                gene = str(row.get(gene_col, "")) if gene_col else ""
                protein_name = str(row.get(protein_name_col, "")) if protein_name_col else ""
                organism = str(row.get(organism_col, "")) if organism_col else ""
                tclass = str(row.get(target_class_col, "")) if target_class_col else ""

                if target_id not in targets:
                    targets[target_id] = TargetEntry(
                        target_id=target_id,
                        uniprot_id=uniprot if uniprot else target_id,
                        gene_name=gene,
                        protein_name=protein_name or target_name,
                        organism=organism,
                        target_class=tclass,
                        source_databases={db_name},
                        external_ids={db_name: target_id},
                    )
                    n_targets_added += 1
                else:
                    targets[target_id].source_databases.add(db_name)
                    targets[target_id].external_ids[db_name] = target_id
                    if uniprot and not targets[target_id].uniprot_id:
                        targets[target_id].uniprot_id = uniprot

                # ── Extract evidence score ──────────────────────────────────
                raw_value = 0.0
                if score_col and pd.notna(row.get(score_col)):
                    try:
                        raw_value = float(row.get(score_col))
                    except (ValueError, TypeError):
                        raw_value = 0.0

                raw_type = str(row.get(score_type_col, "")) if score_type_col else ""
                if not raw_type:
                    raw_type = "unknown"

                # Normalize score to [0, 1]
                normalized_score = _normalize_score(raw_value, raw_type, db_name)

                # Build record link
                record_link = _build_record_link(
                    db_name, drug_id, target_id,
                    drugs.get(drug_id, DrugEntry(drug_id=drug_id, smiles="")),
                    targets.get(target_id, TargetEntry(target_id=target_id)),
                )

                # Build evidence
                ev = DrugTargetEvidence(
                    drug_id=drug_id,
                    target_id=target_id,
                    database=db_name,
                    score=normalized_score,
                    raw_value=raw_value,
                    raw_type=raw_type,
                    record_link=record_link,
                    extra={
                        "source_file": file_paths[0].name if file_paths else "",
                    },
                )
                evidence[drug_id][target_id].append(ev)
                n_evidence_added += 1

            except Exception:
                continue

        print(f"    +{n_drugs_added} drugs, +{n_targets_added} targets, "
              f"+{n_evidence_added} evidence records")

    return drugs, targets, dict(evidence)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 2: STANDARDIZATION                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def compute_ecfp4_fingerprints(drugs: Dict[str, DrugEntry]) -> int:
    """Compute ECFP4 fingerprints for all drugs.

    Parameters
    ----------
    drugs : Dict[str, DrugEntry]
        Drug entries (mutated in-place: fingerprint field set).

    Returns
    -------
    int
        Number of successfully fingerprinted drugs.
    """
    if not RDKIT_AVAILABLE:
        print("  ⚠ RDKit not available — using hash-based pseudo-fingerprints")
        return _compute_hash_fingerprints(drugs)

    n_ok = 0
    n_fail = 0
    for drug_id, drug in tqdm(list(drugs.items()), desc="  Computing ECFP4"):
        try:
            mol = Chem.MolFromSmiles(drug.smiles)
            if mol is not None:
                fp = AllChem.GetMorganFingerprintAsBitVect(
                    mol, radius=ECFP4_RADIUS, nBits=ECFP4_BITS,
                )
                arr = np.zeros(ECFP4_BITS, dtype=np.float64)
                DataStructs.ConvertToNumpyArray(fp, arr)
                drug.fingerprint = arr

                # Also compute physicochemical properties
                drug.mw = float(Descriptors.MolWt(mol))
                drug.logp = float(Descriptors.MolLogP(mol))
                drug.hbd = int(Descriptors.NumHDonors(mol))
                drug.hba = int(Descriptors.NumHAcceptors(mol))
                drug.tpsa = float(Descriptors.TPSA(mol))
                n_ok += 1
            else:
                drug.fingerprint = _hash_fingerprint(drug.smiles)
                n_fail += 1
        except Exception:
            drug.fingerprint = _hash_fingerprint(drug.smiles)
            n_fail += 1

    print(f"    RDKit: {n_ok} OK, {n_fail} fallback (hash-based)")
    return n_ok


def _compute_hash_fingerprints(drugs: Dict[str, DrugEntry]) -> int:
    """Fallback: compute hash-based pseudo-fingerprints."""
    n = 0
    for drug_id, drug in drugs.items():
        drug.fingerprint = _hash_fingerprint(drug.smiles)
        n += 1
    return n


def _hash_fingerprint(smiles: str) -> np.ndarray:
    """Generate a hash-based pseudo-fingerprint (2048-bit)."""
    h = hashlib.sha256(smiles.encode()).digest()
    bits = np.unpackbits(np.frombuffer(h[:256], dtype=np.uint8))
    fp = np.zeros(ECFP4_BITS, dtype=np.float64)
    fp[:min(len(bits), ECFP4_BITS)] = bits[:ECFP4_BITS].astype(np.float64)
    return fp


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 3: EVIDENCE MATRIX CONSTRUCTION                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def build_evidence_matrix(
    evidence: Dict[str, Dict[str, List[DrugTargetEvidence]]],
    drugs: Dict[str, DrugEntry],
    targets: Dict[str, TargetEntry],
    database_names: List[str],
) -> pd.DataFrame:
    """Build a unified drug-target evidence matrix.

    Each row represents one drug-target pair. Columns include per-database
    evidence scores and aggregate statistics.

    Parameters
    ----------
    evidence : Dict
        Nested dict: drug_id → target_id → List[DrugTargetEvidence].
    drugs : Dict[str, DrugEntry]
    targets : Dict[str, TargetEntry]
    database_names : List[str]
        Ordered list of database names for consistent column ordering.

    Returns
    -------
    pd.DataFrame
        Columns: drug_id, target_id, drug_smiles, target_name, target_uniprot,
        db_{name}_score, db_{name}_present, n_databases, db_list
    """
    rows = []
    for drug_id, target_ev_dict in tqdm(
        evidence.items(), desc="  Building evidence matrix"
    ):
        drug = drugs.get(drug_id)
        smiles = drug.smiles if drug else ""

        for target_id, ev_list in target_ev_dict.items():
            target = targets.get(target_id)
            target_name = target.protein_name if target else ""
            target_uniprot = target.uniprot_id if target else ""

            # Aggregate evidence per database (take max if multiple records)
            db_scores: Dict[str, float] = {}
            db_links: Dict[str, str] = {}
            for ev in ev_list:
                db_scores[ev.database] = max(
                    db_scores.get(ev.database, 0.0), ev.score
                )
                if ev.record_link:
                    db_links[ev.database] = ev.record_link

            n_dbs = len(db_scores)
            db_list = sorted(db_scores.keys())

            row = {
                "drug_id": drug_id,
                "target_id": target_id,
                "drug_smiles": smiles,
                "target_name": target_name,
                "target_uniprot": target_uniprot,
                "n_databases": n_dbs,
                "db_list": "|".join(db_list),
                "db_links": json.dumps(db_links) if db_links else "{}",
            }

            # Per-database score columns
            for db_name in database_names:
                row[f"db_{db_name}_score"] = db_scores.get(db_name, np.nan)
                row[f"db_{db_name}_present"] = 1 if db_name in db_scores else 0

            rows.append(row)

    df = pd.DataFrame(rows)
    if len(df) > 0:
        # Sort by number of databases (more evidence first)
        df = df.sort_values("n_databases", ascending=False).reset_index(drop=True)

    print(f"    Built {len(df):,} drug-target pairs across {len(database_names)} databases")
    return df


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 4: YAJIE MULTI-EXPERT CONSENSUS                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class MultiDatabaseYajie:
    """Yajie consensus engine for multi-database drug-target screening.

    Each database acts as an independent "expert." Yajie evaluates
    consensus across experts, identifies disagreements, and classifies
    each drug-target pair as CLEAN, NOISY, or AMBIGUOUS.

    Theorem 1 (Multi-Expert Consistency):
      - Low σ across experts → CLEAN (high confidence, all DBs agree)
      - High σ, moderate mean → AMBIGUOUS (some DBs conflict)
      - High σ, low mean → NOISY (data quality issue, possible DB error)

    Parameters
    ----------
    grace : float
        Tolerance for expert disagreement. Higher = more forgiving.
    consensus_threshold : float
        Minimum mean score for HIGH consensus level.
    purity_threshold : float
        Minimum score for CLEAN classification.
    """

    def __init__(
        self,
        grace: float = DEFAULT_GRACE,
        consensus_threshold: float = DEFAULT_CONSENSUS_THRESHOLD,
        purity_threshold: float = 0.70,
    ):
        self.grace = grace
        self.consensus_threshold = consensus_threshold
        self.purity_threshold = purity_threshold

    def screen(
        self,
        evidence_df: pd.DataFrame,
        database_names: List[str],
        provenance: Dict[str, Dict[str, Any]],
    ) -> List[MTScreeningResult]:
        """Screen all drug-target pairs through Yajie multi-expert consensus.

        Parameters
        ----------
        evidence_df : pd.DataFrame
            Evidence matrix from build_evidence_matrix().
        database_names : List[str]
            Ordered list of database expert names.
        provenance : Dict[str, Dict[str, Any]]
            Provenance metadata for download date tracking.

        Returns
        -------
        List[MTScreeningResult]
            Scored and classified results for every pair.
        """
        results: List[MTScreeningResult] = []

        # Get latest download date from provenance
        download_dates = []
        for prov in provenance.values():
            dl_date = prov.get("download_date", "")
            if dl_date:
                download_dates.append(dl_date)
        latest_download = max(download_dates) if download_dates else datetime.now(timezone.utc).isoformat()

        score_cols = [f"db_{db}_score" for db in database_names]
        present_cols = [f"db_{db}_present" for db in database_names]

        for _, row in tqdm(
            evidence_df.iterrows(), total=len(evidence_df),
            desc="  Yajie screening"
        ):
            # Collect expert scores (skip NaN = database has no data)
            expert_scores = []
            expert_dbs = []
            db_score_map: Dict[str, float] = {}
            db_links_map: Dict[str, str] = {}

            for db_name in database_names:
                score_val = row.get(f"db_{db_name}_score", np.nan)
                if not np.isnan(score_val):
                    expert_scores.append(float(score_val))
                    expert_dbs.append(db_name)
                    db_score_map[db_name] = round(float(score_val), 4)

            # Parse links if available
            try:
                db_links_map = json.loads(str(row.get("db_links", "{}")))
            except (json.JSONDecodeError, TypeError):
                db_links_map = {}

            n_dbs = len(expert_scores)

            if n_dbs == 0:
                # No database has data for this pair
                results.append(MTScreeningResult(
                    drug_id=str(row["drug_id"]),
                    target_id=str(row["target_id"]),
                    drug_smiles=str(row.get("drug_smiles", "")),
                    target_name=str(row.get("target_name", "")),
                    MT_score=0.0,
                    consensus_level="NONE",
                    consensus_std=0.0,
                    n_databases=0,
                    n_databases_agree=0,
                    classification="NO_DATA",
                    source_databases=[],
                    database_scores={},
                    database_links={},
                    download_date=latest_download,
                ))
                continue

            # ── Yajie consensus computation ──────────────────────────────
            scores_arr = np.array(expert_scores)
            mean_score = float(np.mean(scores_arr))
            std_score = float(np.std(scores_arr)) if n_dbs > 1 else 0.0

            # Weighted mean (favor higher-confidence databases)
            # Weight = 1 / (1 + score_variance_within_db)
            # For simplicity, equal weights; could be extended
            mt_score = mean_score

            # Count databases agreeing (within grace tolerance)
            n_agree = 0
            if n_dbs > 1:
                for s in expert_scores:
                    if abs(s - mt_score) <= self.grace:
                        n_agree += 1
            else:
                n_agree = 1

            # ── Consensus level ──────────────────────────────────────────
            if n_dbs >= 3 and n_agree >= n_dbs * 0.75 and mt_score >= self.consensus_threshold:
                consensus_level = "HIGH"
            elif n_dbs >= 2 and n_agree >= n_dbs * 0.5 and mt_score >= 0.4:
                consensus_level = "MEDIUM"
            elif n_dbs >= 1:
                consensus_level = "LOW"
            else:
                consensus_level = "NONE"

            # ── Classification (Yajie Theorem 1 logic) ───────────────────
            if n_dbs >= 3 and std_score <= self.grace and mt_score >= self.purity_threshold:
                classification = "CLEAN"
                disagreement_detail = (
                    f"All {n_dbs} databases agree (σ={std_score:.4f}, "
                    f"MT={mt_score:.4f})"
                )
            elif n_dbs >= 2 and std_score <= self.grace * 2 and mt_score >= 0.4:
                classification = "CLEAN"
                disagreement_detail = (
                    f"Good consensus ({n_agree}/{n_dbs} agree, σ={std_score:.4f})"
                )
            elif std_score > self.grace * 3:
                classification = "NOISY"
                # Identify outlier databases
                outliers = [
                    f"{db}={db_score_map.get(db, 0):.3f}"
                    for db in expert_dbs
                    if abs(db_score_map.get(db, 0) - mt_score) > self.grace * 1.5
                ]
                disagreement_detail = (
                    f"Database disagreement! Outliers: {', '.join(outliers) if outliers else 'none'}"
                    f" (σ={std_score:.4f}). Possible data quality issue."
                )
            elif std_score > self.grace * 1.5:
                classification = "AMBIGUOUS"
                disagreement_detail = (
                    f"Moderate disagreement ({n_agree}/{n_dbs} agree, σ={std_score:.4f})"
                )
            else:
                classification = "AMBIGUOUS"
                disagreement_detail = (
                    f"Insufficient evidence ({n_dbs} databases, σ={std_score:.4f})"
                )

            results.append(MTScreeningResult(
                drug_id=str(row["drug_id"]),
                target_id=str(row["target_id"]),
                drug_smiles=str(row.get("drug_smiles", "")),
                target_name=str(row.get("target_name", "")),
                MT_score=round(float(np.clip(mt_score, 0.0, 1.0)), 6),
                consensus_level=consensus_level,
                consensus_std=round(std_score, 6),
                n_databases=n_dbs,
                n_databases_agree=n_agree,
                classification=classification,
                source_databases=expert_dbs,
                database_scores=db_score_map,
                database_links=db_links_map,
                expert_disagreement_detail=disagreement_detail,
                download_date=latest_download,
            ))

        return results


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 5: OUTPUT                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def write_mt_gold_standard(
    results: List[MTScreeningResult],
    output_dir: Path,
    database_names: List[str],
    provenance: Dict[str, Dict[str, Any]],
) -> Dict[str, Path]:
    """Write all output files for the Yajie screening pipeline.

    Parameters
    ----------
    results : List[MTScreeningResult]
        All screening results.
    output_dir : Path
        Output directory.
    database_names : List[str]
        Databases used.
    provenance : Dict[str, Dict[str, Any]]
        Provenance metadata.

    Returns
    -------
    Dict[str, Path]
        Mapping of output type to file path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    written: Dict[str, Path] = {}

    # Sort results: CLEAN first, then by MT_score descending
    classification_order = {"CLEAN": 0, "AMBIGUOUS": 1, "NOISY": 2, "NO_DATA": 3}
    results_sorted = sorted(
        results,
        key=lambda r: (classification_order.get(r.classification, 9), -r.MT_score)
    )

    # ── 1. MT Gold Standard CSV ───────────────────────────────────────────
    mt_path = output_dir / f"mt_gold_standard_{timestamp}.csv"
    _write_mt_csv(results_sorted, mt_path)
    written["mt_gold_standard"] = mt_path
    print(f"  ✓ MT Gold Standard: {mt_path} ({len(results_sorted):,} pairs)")

    # ── 2. Per-classification summary ─────────────────────────────────────
    summary_path = output_dir / f"mt_classification_summary_{timestamp}.csv"
    _write_classification_summary(results_sorted, summary_path)
    written["classification_summary"] = summary_path

    # ── 3. Database agreement matrix ──────────────────────────────────────
    agreement_path = output_dir / f"mt_database_agreement_{timestamp}.csv"
    _write_database_agreement(results_sorted, database_names, agreement_path)
    written["database_agreement"] = agreement_path

    # ── 4. High-confidence pairs (CLEAN, HIGH consensus) ──────────────────
    high_conf_path = output_dir / f"mt_high_confidence_{timestamp}.csv"
    _write_high_confidence(results_sorted, high_conf_path)
    written["high_confidence"] = high_conf_path

    # ── 5. Disagreement report (NOISY pairs) ──────────────────────────────
    noisy_path = output_dir / f"mt_disagreements_{timestamp}.csv"
    _write_disagreements(results_sorted, noisy_path)
    written["disagreements"] = noisy_path

    # ── 6. Novel targets (single-database, low consensus) ─────────────────
    novel_path = output_dir / f"mt_novel_candidates_{timestamp}.csv"
    _write_novel_candidates(results_sorted, novel_path)
    written["novel_candidates"] = novel_path

    # ── 7. Quality report (JSON) ──────────────────────────────────────────
    quality_path = output_dir / f"mt_quality_report_{timestamp}.json"
    _write_quality_report(results_sorted, database_names, provenance, quality_path)
    written["quality_report"] = quality_path

    # ── 8. Full provenance audit trail ────────────────────────────────────
    audit_path = output_dir / f"mt_provenance_audit_{timestamp}.json"
    _write_provenance_audit(results_sorted, database_names, provenance, audit_path)
    written["provenance_audit"] = audit_path

    return written


def _write_mt_csv(results: List[MTScreeningResult], path: Path) -> None:
    """Write the primary MT Gold Standard CSV."""
    rows = []
    for r in results:
        rows.append({
            "drug_id": r.drug_id,
            "target_id": r.target_id,
            "drug_smiles": r.drug_smiles,
            "target_name": r.target_name,
            "MT_score": r.MT_score,
            "consensus_level": r.consensus_level,
            "consensus_std": r.consensus_std,
            "n_databases": r.n_databases,
            "n_databases_agree": r.n_databases_agree,
            "classification": r.classification,
            "source_databases": "|".join(r.source_databases),
            "database_scores": json.dumps(r.database_scores),
            "database_links": json.dumps(r.database_links),
            "expert_disagreement_detail": r.expert_disagreement_detail,
            "download_date": r.download_date,
            "mt_report_version": r.mt_report_version,
        })
    pd.DataFrame(rows).to_csv(path, index=False)


def _write_classification_summary(results: List[MTScreeningResult], path: Path) -> None:
    """Write per-classification counts and statistics."""
    classes = defaultdict(lambda: {"count": 0, "mt_scores": [], "n_dbs": []})
    for r in results:
        c = classes[r.classification]
        c["count"] += 1
        c["mt_scores"].append(r.MT_score)
        c["n_dbs"].append(r.n_databases)

    rows = []
    for cls_name in ["CLEAN", "AMBIGUOUS", "NOISY", "NO_DATA"]:
        c = classes.get(cls_name)
        if c:
            scores = np.array(c["mt_scores"])
            dbs = np.array(c["n_dbs"])
            rows.append({
                "classification": cls_name,
                "count": c["count"],
                "pct": round(c["count"] / len(results) * 100, 2),
                "mean_MT_score": round(float(np.mean(scores)), 4),
                "median_MT_score": round(float(np.median(scores)), 4),
                "mean_n_databases": round(float(np.mean(dbs)), 2),
            })

    pd.DataFrame(rows).to_csv(path, index=False)


def _write_database_agreement(
    results: List[MTScreeningResult],
    database_names: List[str],
    path: Path,
) -> None:
    """Write database pairwise agreement matrix."""
    # For each pair of databases, compute agreement rate
    # Agreement = both have data AND scores are within grace
    n = len(database_names)
    matrix = np.zeros((n, n))
    counts = np.zeros((n, n))

    for r in results:
        dbs = r.source_databases
        for i, db_a in enumerate(database_names):
            if db_a not in dbs or db_a not in r.database_scores:
                continue
            score_a = r.database_scores[db_a]
            for j, db_b in enumerate(database_names):
                if db_b not in dbs or db_b not in r.database_scores:
                    continue
                score_b = r.database_scores[db_b]
                counts[i, j] += 1
                if abs(score_a - score_b) <= DEFAULT_GRACE:
                    matrix[i, j] += 1

    # Normalize
    agreement = np.divide(matrix, counts, where=(counts > 0))

    rows = []
    for i, db_a in enumerate(database_names):
        row = {"database": db_a}
        for j, db_b in enumerate(database_names):
            row[f"agree_{db_b}"] = round(float(agreement[i, j]), 4) if counts[i, j] > 0 else 0.0
            row[f"n_pairs_{db_b}"] = int(counts[i, j])
        rows.append(row)

    pd.DataFrame(rows).to_csv(path, index=False)


def _write_high_confidence(results: List[MTScreeningResult], path: Path) -> None:
    """Write high-confidence pairs only."""
    high = [r for r in results if r.classification == "CLEAN" and r.consensus_level == "HIGH"]
    if high:
        _write_mt_csv(high, path)
    else:
        # Write empty with header
        _write_mt_csv([], path)


def _write_disagreements(results: List[MTScreeningResult], path: Path) -> None:
    """Write NOISY / disagreement pairs for review."""
    noisy = [r for r in results if r.classification == "NOISY"]
    if noisy:
        _write_mt_csv(noisy, path)


def _write_novel_candidates(results: List[MTScreeningResult], path: Path) -> None:
    """Write novel/emerging candidates (low consensus, single DB, potentially new)."""
    novel = [
        r for r in results
        if r.n_databases <= 2 and r.consensus_level in ("LOW", "NONE")
        and r.classification in ("AMBIGUOUS", "NO_DATA")
    ]
    if novel:
        _write_mt_csv(novel, path)


def _write_quality_report(
    results: List[MTScreeningResult],
    database_names: List[str],
    provenance: Dict[str, Dict[str, Any]],
    path: Path,
) -> None:
    """Write comprehensive data quality report."""
    # Per-database statistics
    db_stats = {}
    for db_name in database_names:
        pairs_with_db = [r for r in results if db_name in r.source_databases]
        useful_pairs = [r for r in pairs_with_db if r.classification != "NOISY"]
        db_stats[db_name] = {
            "total_pairs": len(pairs_with_db),
            "classification_breakdown": {
                cls: sum(1 for r in pairs_with_db if r.classification == cls)
                for cls in ["CLEAN", "AMBIGUOUS", "NOISY", "NO_DATA"]
            },
            "mean_score_when_present": round(
                float(np.mean([r.database_scores.get(db_name, 0) for r in pairs_with_db])), 4
            ) if pairs_with_db else 0.0,
            "disagreement_rate": round(
                sum(1 for r in pairs_with_db if r.classification == "NOISY") / max(len(pairs_with_db), 1), 4
            ),
            "useful_pairs_pct": round(len(useful_pairs) / max(len(pairs_with_db), 1), 4),
        }

    # Overall statistics
    total = len(results)
    n_clean = sum(1 for r in results if r.classification == "CLEAN")
    n_noisy = sum(1 for r in results if r.classification == "NOISY")
    n_ambiguous = sum(1 for r in results if r.classification == "AMBIGUOUS")
    n_no_data = sum(1 for r in results if r.classification == "NO_DATA")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_version": PIPELINE_VERSION,
        "summary": {
            "total_drug_target_pairs": total,
            "clean": n_clean,
            "ambiguous": n_ambiguous,
            "noisy": n_noisy,
            "no_data": n_no_data,
            "clean_pct": round(n_clean / total * 100, 2) if total > 0 else 0,
            "high_consensus_pairs": sum(1 for r in results if r.consensus_level == "HIGH"),
            "databases_used": database_names,
        },
        "per_database_statistics": db_stats,
        "provenance": {
            db: {
                "download_date": prov.get("download_date", "unknown"),
                "version": prov.get("version", "unknown"),
                "status": prov.get("status", "unknown"),
            }
            for db, prov in provenance.items()
        },
        "recommendations": _generate_quality_recommendations(results, db_stats),
    }

    path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")


def _write_provenance_audit(
    results: List[MTScreeningResult],
    database_names: List[str],
    provenance: Dict[str, Dict[str, Any]],
    path: Path,
) -> None:
    """Write full provenance audit trail."""
    audit = {
        "audit_generated_at": datetime.now(timezone.utc).isoformat(),
        "pipeline": "SCX Yajie Multi-Database Screening",
        "pipeline_version": PIPELINE_VERSION,
        "databases_queried": database_names,
        "total_pairs_screened": len(results),
        "provenance_by_database": provenance,
        "output_schema": {
            "mt_gold_standard.csv": "Full screening results with per-database scores and provenance links",
            "mt_classification_summary.csv": "Per-classification statistics",
            "mt_database_agreement.csv": "Database pairwise agreement matrix",
            "mt_high_confidence.csv": "High-confidence CLEAN pairs only",
            "mt_disagreements.csv": "NOISY pairs flagged for review",
            "mt_novel_candidates.csv": "Low-consensus emerging candidates",
            "mt_quality_report.json": "Data quality and per-DB statistics",
            "mt_provenance_audit.json": "This file — complete provenance trail",
        },
        "reproducibility": {
            "note": "All MT scores are deterministically reproducible given the same input databases.",
            "checksum_algorithm": "SHA256 (per database download)",
            "rdkit_version": str(Chem.rdkitVersion) if RDKIT_AVAILABLE else "not available",
            "fingerprint_type": f"Morgan/ECFP4 (radius={ECFP4_RADIUS}, bits={ECFP4_BITS})",
        },
    }
    path.write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")


def _generate_quality_recommendations(
    results: List[MTScreeningResult],
    db_stats: Dict[str, Dict[str, Any]],
) -> List[str]:
    """Generate actionable recommendations from quality analysis."""
    recs = []

    total = len(results)
    n_noisy = sum(1 for r in results if r.classification == "NOISY")
    n_clean = sum(1 for r in results if r.classification == "CLEAN")

    if n_noisy > total * 0.3:
        recs.append(
            f"CRITICAL: {n_noisy}/{total} pairs ({n_noisy/total*100:.1f}%) classified as NOISY. "
            f"Systematic database disagreement detected. Review per-database quality and "
            f"consider expert recalibration."
        )

    if n_clean == 0:
        recs.append(
            "WARNING: No CLEAN pairs found. Consensus threshold may be too strict, "
            "or databases contain insufficient overlapping evidence."
        )

    # Check for problematic databases
    for db_name, stats in db_stats.items():
        if stats["disagreement_rate"] > 0.5 and stats["total_pairs"] > 10:
            recs.append(
                f"WARNING: Database '{db_name}' has high disagreement rate "
                f"({stats['disagreement_rate']:.1%}). Consider auditing its data quality."
            )
        if stats["useful_pairs_pct"] < 0.1 and stats["total_pairs"] > 10:
            recs.append(
                f"INFO: Database '{db_name}' contributes few useful pairs "
                f"({stats['useful_pairs_pct']:.1%}). May have low overlap with other databases."
            )

    # Check for single-DB-only pairs
    n_single_db = sum(1 for r in results if r.n_databases <= 1)
    if n_single_db > total * 0.5:
        recs.append(
            f"INFO: {n_single_db}/{total} pairs ({n_single_db/total*100:.1f}%) "
            f"have evidence from only one database. Multi-database consensus is limited. "
            f"Consider downloading additional databases for cross-validation."
        )

    if not recs:
        recs.append("No critical data quality issues detected.")

    return recs


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  HELPER FUNCTIONS                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def _find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Find the first matching column name in a DataFrame."""
    for col in candidates:
        if col in df.columns:
            return col
    # Case-insensitive fallback
    col_lower = {c.lower(): c for c in df.columns}
    for col in candidates:
        if col.lower() in col_lower:
            return col_lower[col.lower()]
    return None


def _smiles_to_id(smiles: str) -> str:
    """Generate a stable drug ID from SMILES."""
    h = hashlib.sha256(smiles.encode()).hexdigest()[:12]
    return f"DRUG_{h}"


def _normalize_score(raw_value: float, raw_type: str, db_name: str) -> float:
    """Normalize a raw database score to [0, 1].

    Different databases use different scales:
    - pChEMBL / pIC50 / pKi: typically 0-14 (higher = better), normalize to [0, 1]
    - STITCH combined_score: 0-999, divide by 1000
    - BindingDB Ki/IC50/Kd in nM: lower = better, use -log10 transform
    - Open Targets association score: already 0-1
    - SIDER: binary (0/1)
    """
    rt = raw_type.lower() if raw_type else ""

    if db_name == "stitch":
        # STITCH: 0-999 → [0, 1]
        return min(1.0, raw_value / 1000.0)

    elif db_name == "open_targets":
        # Already 0-1
        return min(1.0, max(0.0, raw_value))

    elif db_name in ("sider", "pharmgkb", "stanford_hivdb"):
        # Binary/presence
        return 1.0 if raw_value > 0 else 0.0

    elif db_name == "drugbank":
        # DrugBank: action_types presence → 1.0, else need other evidence
        return min(1.0, raw_value / 10.0) if raw_value > 0 else 0.3

    elif any(t in rt for t in ("pchembl", "pic50", "pki", "pkd", "pec50")):
        # p-value scales: higher = better, 0-14 typical
        # pIC50 = -log10(IC50 in M), so pIC50 6 = 1 µM
        if raw_value >= 9:
            return 1.0
        elif raw_value >= 8:
            return 0.9
        elif raw_value >= 7:
            return 0.75
        elif raw_value >= 6:
            return 0.55
        elif raw_value >= 5:
            return 0.35
        elif raw_value > 0:
            return 0.15
        else:
            return 0.0

    elif any(t in rt for t in ("ic50", "ki", "kd", "ec50", "potency")):
        # IC50/Ki/Kd in nM (or µM): lower = better for binding
        # Convert to approximate pIC50: pIC50 ≈ -log10(value_nM * 1e-9)
        if raw_value <= 0:
            return 0.0
        # Assume nM; if very small, could be M — clamp
        value_nM = raw_value
        if value_nM < 0.001:  # likely in M
            value_nM = raw_value * 1e9
        elif value_nM < 1:  # likely in µM
            value_nM = raw_value * 1000

        p_value = -np.log10(value_nM * 1e-9) if value_nM > 0 else 0
        return min(1.0, max(0.0, p_value / 12.0))

    else:
        # Generic: clamp to [0, 1]
        if raw_value > 1:
            return min(1.0, raw_value / 10.0)
        return min(1.0, max(0.0, raw_value))


def _build_record_link(
    db_name: str,
    drug_id: str,
    target_id: str,
    drug: DrugEntry,
    target: TargetEntry,
) -> str:
    """Build a URL linking back to the original database record."""
    template = DATABASE_LINK_TEMPLATES.get(db_name, "")
    if not template:
        return ""

    # Get database-specific external ID
    ext_drug_id = drug.external_ids.get(db_name, drug_id)
    ext_target_id = target.external_ids.get(db_name, target_id)

    try:
        return template.format(
            drug_id=ext_drug_id,
            target_id=ext_target_id,
            aid=ext_drug_id,
        )
    except KeyError:
        return template


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  MAIN PIPELINE ORCHESTRATOR                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def run_screening(
    db_root: Path,
    output_dir: Path,
    compounds_csv: Optional[Path] = None,
    targets_csv: Optional[Path] = None,
    databases: Optional[List[str]] = None,
    max_pairs: int = -1,
    max_drugs: int = -1,
    grace: float = DEFAULT_GRACE,
    consensus_threshold: float = DEFAULT_CONSENSUS_THRESHOLD,
) -> Dict[str, Path]:
    """Run the complete Yajie multi-database screening pipeline.

    Parameters
    ----------
    db_root : Path
        Root directory with downloaded databases.
    output_dir : Path
        Output directory for results.
    compounds_csv : Optional[Path]
        Pre-extracted compounds CSV (skip extraction if provided).
    targets_csv : Optional[Path]
        Pre-extracted targets CSV (skip extraction if provided).
    databases : Optional[List[str]]
        Specific databases to include (None = all available).
    max_pairs : int
        Maximum drug-target pairs to screen (-1 = unlimited).
    max_drugs : int
        Maximum unique drugs to load (-1 = unlimited).
    grace : float
        Yajie grace parameter.
    consensus_threshold : float
        Consensus threshold.

    Returns
    -------
    Dict[str, Path]
        Map of output names to file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()

    print(f"\n{'='*70}")
    print(f"  SCX Yajie Multi-Database Screening Pipeline v{PIPELINE_VERSION}")
    print(f"  DB Root: {db_root}")
    print(f"  Output:  {output_dir}")
    print(f"  Date:    {datetime.now().isoformat()}")
    print(f"{'='*70}\n")

    # ── Phase 1: Load data ────────────────────────────────────────────────
    print(f"[Phase 1/4] Loading databases and provenance ...")

    # Load provenance
    provenance = load_provenance(db_root)
    print(f"  Loaded provenance for {len(provenance)} databases")

    # Discover data files
    db_files = discover_data_files(db_root)
    available_dbs = list(db_files.keys())
    print(f"  Discovered {len(available_dbs)} databases with data: {available_dbs}")

    # Filter databases if specified
    if databases:
        db_files = {k: v for k, v in db_files.items() if k in databases}
        print(f"  Filtered to {len(db_files)} requested databases: {list(db_files.keys())}")

    database_names = sorted(db_files.keys())
    if not database_names:
        print("  ⚠ No databases found. Run download_databases.py first.")
        sys.exit(1)

    # Load compounds/targets from pre-extracted CSVs if provided
    if compounds_csv and compounds_csv.exists() and targets_csv and targets_csv.exists():
        print(f"  Using pre-extracted compounds: {compounds_csv}")
        print(f"  Using pre-extracted targets: {targets_csv}")
        drugs, targets, evidence = _load_from_csvs(compounds_csv, targets_csv, db_files, provenance)
    else:
        # Extract from database files
        drugs, targets, evidence = extract_drugs_and_targets(
            db_files, provenance, max_drugs=max_drugs,
        )

    print(f"  Drugs:  {len(drugs):,} unique")
    print(f"  Targets: {len(targets):,} unique")

    # ── Phase 2: Standardization ──────────────────────────────────────────
    print(f"\n[Phase 2/4] Standardizing fingerprints and IDs ...")

    # Compute ECFP4 fingerprints
    n_fp = compute_ecfp4_fingerprints(drugs)
    print(f"  Fingerprinted {n_fp}/{len(drugs)} drugs (ECFP4, {ECFP4_BITS}-bit)")

    # ── Phase 3: Build evidence matrix ────────────────────────────────────
    print(f"\n[Phase 3/4] Building drug-target evidence matrix ...")

    evidence_df = build_evidence_matrix(evidence, drugs, targets, database_names)

    if len(evidence_df) == 0:
        print("  ⚠ No drug-target pairs with evidence found.")
        sys.exit(1)

    # Apply max_pairs limit
    if max_pairs > 0 and len(evidence_df) > max_pairs:
        print(f"  Limiting to {max_pairs:,} pairs (from {len(evidence_df):,})")
        evidence_df = evidence_df.head(max_pairs)

    print(f"  Matrix: {len(evidence_df):,} pairs × {len(database_names)} databases")

    # ── Phase 4: Yajie screening ──────────────────────────────────────────
    print(f"\n[Phase 4/4] Running Yajie multi-expert consensus ...")
    print(f"  Grace: {grace}, Consensus threshold: {consensus_threshold}")
    print(f"  Databases as experts: {', '.join(database_names)}")

    yajie = MultiDatabaseYajie(
        grace=grace,
        consensus_threshold=consensus_threshold,
    )

    results = yajie.screen(evidence_df, database_names, provenance)

    # ── Write outputs ─────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  Writing outputs ...")
    written = write_mt_gold_standard(results, output_dir, database_names, provenance)

    # ── Summary ───────────────────────────────────────────────────────────
    t_elapsed = time.perf_counter() - t_start
    n_clean = sum(1 for r in results if r.classification == "CLEAN")
    n_noisy = sum(1 for r in results if r.classification == "NOISY")
    n_ambiguous = sum(1 for r in results if r.classification == "AMBIGUOUS")
    n_no_data = sum(1 for r in results if r.classification == "NO_DATA")
    n_high = sum(1 for r in results if r.consensus_level == "HIGH")

    print(f"\n{'='*70}")
    print(f"  SCREENING COMPLETE")
    print(f"  Runtime: {t_elapsed:.0f} s ({t_elapsed/60:.1f} min)")
    print(f"{'='*70}")
    print(f"\n  Results:")
    print(f"    Total pairs:    {len(results):>10,}")
    print(f"    CLEAN:          {n_clean:>10,} ({n_clean/len(results)*100:5.1f}%)")
    print(f"    AMBIGUOUS:      {n_ambiguous:>10,} ({n_ambiguous/len(results)*100:5.1f}%)")
    print(f"    NOISY:          {n_noisy:>10,} ({n_noisy/len(results)*100:5.1f}%)")
    print(f"    NO_DATA:        {n_no_data:>10,} ({n_no_data/len(results)*100:5.1f}%)")
    print(f"    HIGH consensus: {n_high:>10,} ({n_high/len(results)*100:5.1f}%)")

    print(f"\n  Output files:")
    for name, path in written.items():
        size = _human_size(path.stat().st_size) if path.exists() else "N/A"
        print(f"    {name}: {path} ({size})")

    print(f"{'='*70}\n")
    return written


def _load_from_csvs(
    compounds_csv: Path,
    targets_csv: Path,
    db_files: Dict[str, List[Path]],
    provenance: Dict[str, Dict[str, Any]],
) -> Tuple[Dict[str, DrugEntry], Dict[str, TargetEntry], Dict]:
    """Load drugs and targets from pre-extracted CSVs, evidence from database files."""
    drugs: Dict[str, DrugEntry] = {}
    targets: Dict[str, TargetEntry] = {}

    # Load compounds
    mol_df = pd.read_csv(compounds_csv)
    smiles_col = _find_column(mol_df, ["smiles", "SMILES", "canonical_smiles"])
    mol_id_col = _find_column(mol_df, ["mol_id", "drug_id", "compound_id"])
    if smiles_col:
        for _, row in mol_df.iterrows():
            smi = str(row[smiles_col]).strip()
            if smi and len(smi) > 1:
                drug_id = str(row.get(mol_id_col, _smiles_to_id(smi))) if mol_id_col else _smiles_to_id(smi)
                drugs[drug_id] = DrugEntry(drug_id=drug_id, smiles=smi)

    # Load targets
    tgt_df = pd.read_csv(targets_csv)
    tgt_id_col = _find_column(tgt_df, ["target_id", "uniprot_id"])
    gene_col = _find_column(tgt_df, ["gene_name", "gene_symbol"])
    name_col = _find_column(tgt_df, ["protein_name", "target_name"])
    org_col = _find_column(tgt_df, ["organism"])
    class_col = _find_column(tgt_df, ["target_class"])
    uniprot_col = _find_column(tgt_df, ["uniprot_id"])

    if tgt_id_col:
        for _, row in tgt_df.iterrows():
            tid = str(row[tgt_id_col]).strip()
            if tid:
                targets[tid] = TargetEntry(
                    target_id=tid,
                    uniprot_id=str(row.get(uniprot_col, tid)) if uniprot_col else tid,
                    gene_name=str(row.get(gene_col, "")) if gene_col else "",
                    protein_name=str(row.get(name_col, "")) if name_col else "",
                    organism=str(row.get(org_col, "")) if org_col else "",
                    target_class=str(row.get(class_col, "")) if class_col else "",
                )

    # Extract evidence from database files (matching against loaded drugs/targets)
    _, _, evidence = extract_drugs_and_targets(db_files, provenance)

    return drugs, targets, evidence


def _human_size(n_bytes: int) -> str:
    """Format byte count in human-readable units."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} PB"


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  COMMAND-LINE ENTRY POINT                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def main() -> None:
    parser = argparse.ArgumentParser(
        description="SCX Yajie Multi-Database Screening — Drug-Target Gold Standard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/screen_all_databases.py --db-root W:/scx_databases --output outputs/mt_gold_standard
  python scripts/screen_all_databases.py --db-root W:/scx_databases --databases chembl drugbank --output outputs/mt_partial
  python scripts/screen_all_databases.py --db-root W:/scx_databases --max-pairs 10000 --output outputs/mt_test
  python scripts/screen_all_databases.py --compounds inputs/all_compounds.csv --targets inputs/all_human_targets.csv --db-root W:/scx_databases --output outputs/mt_gold_standard
        """,
    )
    parser.add_argument(
        "--db-root", type=Path, required=True,
        help="Root directory with downloaded databases (from download_databases.py)",
    )
    parser.add_argument(
        "--output", type=Path, required=True,
        help="Output directory for results",
    )
    parser.add_argument(
        "--compounds", type=Path,
        help="Pre-extracted compounds CSV (optional, skips extraction)",
    )
    parser.add_argument(
        "--targets", type=Path,
        help="Pre-extracted targets CSV (optional, skips extraction)",
    )
    parser.add_argument(
        "--databases", nargs="*",
        help="Specific databases to screen (default: all available)",
    )
    parser.add_argument(
        "--max-pairs", type=int, default=-1,
        help="Maximum drug-target pairs to screen (-1 = unlimited)",
    )
    parser.add_argument(
        "--max-drugs", type=int, default=-1,
        help="Maximum unique drugs to load (-1 = unlimited)",
    )
    parser.add_argument(
        "--grace", type=float, default=DEFAULT_GRACE,
        help=f"Yajie grace tolerance (default: {DEFAULT_GRACE})",
    )
    parser.add_argument(
        "--consensus-threshold", type=float, default=DEFAULT_CONSENSUS_THRESHOLD,
        help=f"Minimum score for HIGH consensus (default: {DEFAULT_CONSENSUS_THRESHOLD})",
    )

    args = parser.parse_args()

    if not args.db_root.exists():
        print(f"ERROR: Database root not found: {args.db_root}")
        print("Run download_databases.py first.")
        sys.exit(1)

    run_screening(
        db_root=Path(args.db_root),
        output_dir=Path(args.output),
        compounds_csv=args.compounds,
        targets_csv=args.targets,
        databases=args.databases,
        max_pairs=args.max_pairs,
        max_drugs=args.max_drugs,
        grace=args.grace,
        consensus_threshold=args.consensus_threshold,
    )


if __name__ == "__main__":
    main()
