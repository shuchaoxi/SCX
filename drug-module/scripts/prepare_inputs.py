#!/usr/bin/env python3
"""Prepare molecule and target CSV inputs from downloaded databases.

Reads all Parquet files from a database root directory, deduplicates
by SMILES (molecules) and UniProt ID (targets), and writes two CSV files
ready for ``make_initial_state()``.

Output
------
    inputs/all_compounds.csv   — columns: mol_id, smiles
    inputs/all_human_targets.csv — columns: target_id, uniprot_id, gene_name, ...

Usage
-----
    python scripts/prepare_inputs.py \
        --db-root W:/scx_databases \
        --output-dir inputs/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare drug pipeline inputs")
    parser.add_argument(
        "--db-root", type=Path, required=True,
        help="Root directory with downloaded Parquet files (e.g. W:/scx_databases)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("inputs"),
    )
    parser.add_argument(
        "--organism", type=str, default="human",
        help="Target organism filter (default: human)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Collect all molecule SMILES from downloaded databases ────────────
    print("Collecting molecules from databases ...")
    molecules: dict[str, str] = {}  # SMILES → mol_id

    for parquet_file in args.db_root.rglob("*.parquet"):
        try:
            df = pd.read_parquet(parquet_file)
        except Exception:
            continue

        # Find the SMILES column (naming varies across databases)
        smiles_col = None
        for col in ["smiles", "canonical_smiles", "SMILES", "Smiles"]:
            if col in df.columns:
                smiles_col = col
                break
        if smiles_col is None:
            continue

        for smi in df[smiles_col].dropna().unique():
            smi = str(smi).strip()
            if smi and len(smi) > 1 and len(smi) < 2000:
                # Use SMILES hash as mol_id for dedup
                mol_id = f"Mol_{abs(hash(smi)) % 10_000_000:07d}"
                if smi not in molecules:
                    molecules[smi] = mol_id

    mol_df = pd.DataFrame(
        [{"mol_id": mid, "smiles": smi} for smi, mid in molecules.items()]
    )
    mol_path = output_dir / "all_compounds.csv"
    mol_df.to_csv(mol_path, index=False)
    print(f"  Molecules: {len(mol_df):,} unique → {mol_path}")

    # ── Collect all targets ─────────────────────────────────────────────
    print("Collecting targets from databases ...")
    targets: dict[str, dict] = {}  # uniprot_id → row

    for parquet_file in args.db_root.rglob("*.parquet"):
        try:
            df = pd.read_parquet(parquet_file)
        except Exception:
            continue

        uniprot_col = None
        for col in ["uniprot_id", "UniProt_ID", "uniprot", "uniprotkb"]:
            if col in df.columns:
                uniprot_col = col
                break
        if uniprot_col is None:
            continue

        gene_col = None
        for col in ["gene_name", "gene_symbol", "Gene_Name", "target_name"]:
            if col in df.columns:
                gene_col = col
                break

        target_class_col = None
        for col in ["target_class", "protein_class", "Target_Class"]:
            if col in df.columns:
                target_class_col = col
                break

        for _, row in df.iterrows():
            uid = str(row.get(uniprot_col, "")).strip()
            if not uid or len(uid) < 3:
                continue
            if uid not in targets:
                targets[uid] = {
                    "target_id": uid,
                    "uniprot_id": uid,
                    "gene_name": str(row.get(gene_col, uid)) if gene_col else uid,
                    "protein_name": str(row.get("target_name", "")) if "target_name" in df.columns else "",
                    "organism": str(row.get("organism", args.organism)),
                    "target_class": str(row.get(target_class_col, "")) if target_class_col else "",
                    "sequence": str(row.get("sequence", "")) if "sequence" in df.columns else "",
                }

    tgt_df = pd.DataFrame(list(targets.values()))
    tgt_path = output_dir / "all_human_targets.csv"
    tgt_df.to_csv(tgt_path, index=False)
    print(f"  Targets: {len(tgt_df):,} unique → {tgt_path}")

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*50}")
    print(f"Input files ready.")
    print(f"  {mol_path}")
    print(f"  {tgt_path}")
    total_pairs = len(mol_df) * len(tgt_df)
    print(f"  Expected pairs: {total_pairs:,}")
    approx_ram = total_pairs * 20 * 8 / 1e9
    print(f"  Approx RAM needed: ~{approx_ram:.1f} GB (DataFrame)")
    if approx_ram > 32:
        print(f"  ⚠ May exceed 32 GB RAM.  Consider downsizing or using chunked mode.")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
