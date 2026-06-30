#!/usr/bin/env python3
"""Download and pre-process public drug databases for SCX drug-module.

Usage
-----
    python scripts/download_databases.py --output W:/scx_databases --tier 1

Tiers
-----
    1 : Core (DrugBank + ChEMBL + BindingDB + DGIdb + TTD + UniProt)  ~3.5 GB
    2 : Extended (+ STITCH human + SIDER + DrugCentral)                ~12 GB
    3 : Full (+ AlphaFold human subset + PDBbind table)                ~30 GB

Requirements
------------
    pip install wget tqdm rdkit pandas pyarrow
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kw: x  # noqa: E731


# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

DATABASE_CONFIGS: dict[str, dict[str, Any]] = {
    "drugbank": {
        "tier": 1,
        "url": "https://go.drugbank.com/releases/5-1-12/downloads/all-full-database",
        "filename": "drugbank_all_full_database.xml.zip",
        "size_gb": 1.5,
        "note": "Requires DrugBank academic license.  Login at go.drugbank.com first.  "
                "If you cannot get the XML, use the public DrugBank vocabulary CSV instead: "
                "https://go.drugbank.com/releases/latest/downloads/all-drugbank-vocabulary",
    },
    "chembl": {
        "tier": 1,
        "url": "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_34/",
        "filename": "chembl_34_sqlite.tar.gz",
        "size_gb": 6.0,
        "alt_url": "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/",
    },
    "bindingdb": {
        "tier": 1,
        "url": "https://www.bindingdb.org/bind/downloads/BindingDB_All_2025_04.tsv.zip",
        "filename": "BindingDB_All.tsv.zip",
        "size_gb": 3.5,
        "note": "Check https://www.bindingdb.org/bind/BindingDBDownload.jsp for latest",
    },
    "dgidb": {
        "tier": 1,
        "url": "https://www.dgidb.org/data/monthly_tsvs/2025-Apr/interactions.tsv",
        "filename": "dgidb_interactions.tsv",
        "size_gb": 0.05,
    },
    "ttd": {
        "tier": 1,
        "url": "https://db.idrblab.net/ttd/sites/default/files/ttd_database/P1-01-TTD_target_download.txt",
        "filename": "ttd_targets.txt",
        "size_gb": 0.03,
        "note": "Requires free registration at https://db.idrblab.net/ttd/",
    },
    "uniprot": {
        "tier": 1,
        "url": "https://rest.uniprot.org/uniprotkb/stream?"
               "format=fasta&query=(organism_id:9606)+AND+(reviewed:true)",
        "filename": "uniprot_human_reviewed.fasta",
        "size_gb": 0.05,
    },
    "stitch": {
        "tier": 2,
        "url": "http://stitch.embl.de/download/chemical_chemical.links.v5.0/"
               "9606.protein_chemical.links.v5.0.tsv.gz",
        "filename": "stitch_human_links.tsv.gz",
        "size_gb": 0.5,
        "note": "Human subset only.  Full database is ~40 GB.",
    },
    "sider": {
        "tier": 2,
        "url": "http://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz",
        "filename": "sider_side_effects.tsv.gz",
        "size_gb": 0.02,
    },
    "drugcentral": {
        "tier": 2,
        "url": "https://unmtid-shinyapps.net/download/drugcentral/drugcentral.dump.08272024.sql.gz",
        "filename": "drugcentral.sql.gz",
        "size_gb": 0.1,
    },
    "pdbind_table": {
        "tier": 3,
        "url": "http://www.pdbbind.org.cn/download/PDBbind_index_2024.tar.gz",
        "filename": "PDBbind_index.tar.gz",
        "size_gb": 0.05,
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# Download helpers
# ═══════════════════════════════════════════════════════════════════════════

class ProgressHook:
    """urllib progress reporter."""

    def __init__(self):
        self._seen = 0
        self._pbar: Any = None

    def __call__(self, block_num: int, block_size: int, total_size: int):
        if self._pbar is None and total_size > 0:
            self._pbar = tqdm(
                total=total_size, unit="B", unit_scale=True,
                unit_divisor=1024, desc="Downloading",
            )
        if self._pbar is not None:
            downloaded = block_num * block_size
            self._pbar.update(downloaded - self._seen)
            self._seen = downloaded


def download_file(url: str, dest: Path, *, note: str = "") -> Path:
    """Download a file with progress bar.  Skips if already present."""
    if dest.exists():
        print(f"  [SKIP] {dest.name} already exists ({_human_size(dest.stat().st_size)})")
        return dest

    print(f"  [DOWNLOAD] {dest.name}")
    if note:
        print(f"    ⚠ {note}")
    print(f"    URL: {url}")

    dest.parent.mkdir(parents=True, exist_ok=True)

    # Try curl first (more reliable for large files), fall back to urllib
    try:
        subprocess.run(
            ["curl", "-L", "--progress-bar", "-o", str(dest), url],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        hook = ProgressHook()
        urllib.request.urlretrieve(url, str(dest), reporthook=hook)
        if hook._pbar is not None:
            hook._pbar.close()

    size = dest.stat().st_size
    print(f"    Done — {_human_size(size)}")
    return dest


# ═══════════════════════════════════════════════════════════════════════════
# Database-specific parsers (raw → standardised Parquet)
# ═══════════════════════════════════════════════════════════════════════════

def parse_drugbank(xml_path: Path, output_dir: Path) -> Path:
    """Parse DrugBank XML → drugbank_targets.parquet."""
    print("  [PARSE] DrugBank XML → Parquet ...")
    out_path = output_dir / "drugbank" / "drugbank_targets.parquet"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    context = ET.iterparse(str(xml_path), events=("end",))
    for event, elem in tqdm(context, desc="Parsing DrugBank XML"):
        if elem.tag.endswith("}drug"):
            drug_id = _xml_text(elem, "drugbank-id", primary="true") or ""
            if not drug_id:
                drug_id = _xml_text(elem, "drugbank-id") or ""
            name = _xml_text(elem, "name") or ""
            smiles = ""
            for prop in elem.iter():
                if prop.tag.endswith("}calculated-properties"):
                    for child in prop:
                        if child.tag.endswith("}property"):
                            kind = _xml_text(child, "kind")
                            if kind == "SMILES":
                                smiles = _xml_text(child, "value") or ""
                                break
                if smiles:
                    break

            for tgt_elem in elem.iter():
                if tgt_elem.tag.endswith("}targets"):
                    for tgt in tgt_elem:
                        tgt_id = _xml_text(tgt, "id") or ""
                        tgt_name = _xml_text(tgt, "name") or ""
                        uniprot = ""
                        for poly in tgt.iter():
                            if poly.tag.endswith("}polypeptide"):
                                uniprot = (
                                    _xml_attrib(poly, "id") or ""
                                    or _xml_attrib(poly, "source") or ""
                                )
                                break
                        for act in tgt.iter():
                            if act.tag.endswith("}actions"):
                                action_types = [
                                    (_xml_text(a, "text") or "")
                                    for a in act
                                ]
                                break
                        else:
                            action_types = []

                        rows.append({
                            "drug_id": drug_id,
                            "drug_name": name,
                            "smiles": smiles,
                            "target_id": tgt_id,
                            "target_name": tgt_name,
                            "uniprot_id": uniprot,
                            "action_types": "|".join(action_types),
                            "source_db": "drugbank",
                            "score": 1.0,
                        })
            elem.clear()

    df = pd.DataFrame(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"    Wrote {len(df)} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


def parse_chembl_sqlite(sqlite_path: Path, output_dir: Path) -> Path:
    """Extract activities from ChEMBL SQLite → chembl_activities.parquet."""
    print("  [PARSE] ChEMBL SQLite → Parquet ...")
    import sqlite3

    out_path = output_dir / "chembl" / "chembl_activities.parquet"
    output_dir.mkdir(parents=True, exist_ok=True)

    # If it's a tar.gz, extract the SQLite file
    if sqlite_path.suffix == ".gz" or ".tar" in sqlite_path.name:
        print("    Extracting archive ...")
        extract_dir = output_dir / "chembl" / "_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        if sqlite_path.name.endswith(".tar.gz"):
            with tarfile.open(sqlite_path, "r:gz") as tar:
                tar.extractall(extract_dir)
        sqlite_files = list(extract_dir.rglob("*.db")) + list(extract_dir.rglob("*.sqlite"))
        if not sqlite_files:
            raise FileNotFoundError(f"No SQLite file found in {extract_dir}")
        sqlite_path = sqlite_files[0]

    conn = sqlite3.connect(str(sqlite_path))
    query = """
        SELECT
            md.chembl_id AS molregno,
            cs.canonical_smiles AS smiles,
            td.chembl_id AS target_chembl_id,
            td.pref_name AS target_name,
            act.standard_type,
            act.standard_value,
            act.standard_units,
            act.pchembl_value,
            act.assay_type,
            act.confidence_score,
            src.src_description AS source_db
        FROM activities act
        JOIN molecule_dictionary md ON act.molregno = md.molregno
        JOIN compound_structures cs ON md.molregno = cs.molregno
        JOIN target_dictionary td ON act.tid = td.tid
        JOIN source src ON act.src_id = src.src_id
        WHERE act.standard_value IS NOT NULL
          AND cs.canonical_smiles IS NOT NULL
        LIMIT 5000000
    """
    chunks = pd.read_sql_query(query, conn, chunksize=200000)
    frames = []
    for chunk in tqdm(chunks, desc="Reading ChEMBL chunks"):
        frames.append(chunk)
    df = pd.concat(frames, ignore_index=True)
    conn.close()

    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"    Wrote {len(df)} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


def parse_bindingdb(tsv_path: Path, output_dir: Path) -> Path:
    """Parse BindingDB TSV → bindingdb_affinities.parquet."""
    print("  [PARSE] BindingDB TSV → Parquet ...")
    out_path = output_dir / "bindingdb" / "bindingdb_affinities.parquet"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract if zipped
    read_path = tsv_path
    if tsv_path.suffix == ".zip":
        import zipfile
        with zipfile.ZipFile(tsv_path) as zf:
            names = zf.namelist()
            tsv_name = [n for n in names if n.endswith(".tsv") or n.endswith(".txt")][0]
            zf.extract(tsv_name, output_dir / "bindingdb")
            read_path = output_dir / "bindingdb" / tsv_name

    df = pd.read_csv(read_path, sep="\t", low_memory=False, nrows=2_000_000)
    # Standardise columns
    col_map = {}
    for c in df.columns:
        cl = c.lower().replace(" ", "_")
        if "smiles" in cl:
            col_map[c] = "smiles"
        elif "ki" in cl and "nm" in cl:
            col_map[c] = "ki_nm"
        elif "ic50" in cl and "nm" in cl:
            col_map[c] = "ic50_nm"
        elif "kd" in cl and "nm" in cl:
            col_map[c] = "kd_nm"
        elif "uniprot" in cl:
            col_map[c] = "uniprot_id"
        elif "target" in cl and "name" in cl:
            col_map[c] = "target_name"
    df = df.rename(columns=col_map)
    if "uniprot_id" not in df.columns and "target_name" in df.columns:
        df["uniprot_id"] = df["target_name"]

    keep = [c for c in ["smiles", "ki_nm", "ic50_nm", "kd_nm", "uniprot_id", "target_name"]
            if c in df.columns]
    df = df[keep]
    df["source_db"] = "bindingdb"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"    Wrote {len(df)} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


def parse_dgidb(tsv_path: Path, output_dir: Path) -> Path:
    """Parse DGIdb TSV → dgidb_interactions.parquet."""
    print("  [PARSE] DGIdb TSV → Parquet ...")
    out_path = output_dir / "dgidb" / "dgidb_interactions.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(tsv_path, sep="\t")
    df["source_db"] = "dgidb"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"    Wrote {len(df)} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


def parse_ttd(txt_path: Path, output_dir: Path) -> Path:
    """Parse TTD text → ttd_disease_target.parquet."""
    print("  [PARSE] TTD → Parquet ...")
    out_path = output_dir / "ttd" / "ttd_disease_target.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(txt_path, sep="\t", low_memory=False)
    df["source_db"] = "ttd"
    df.to_parquet(out_path, index=False, engine="pyarrow")
    print(f"    Wrote {len(df)} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


# ═══════════════════════════════════════════════════════════════════════════

PARSERS = {
    "drugbank": parse_drugbank,
    "chembl": parse_chembl_sqlite,
    "bindingdb": parse_bindingdb,
    "dgidb": parse_dgidb,
    "ttd": parse_ttd,
}


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(description="Download SCX drug databases")
    parser.add_argument(
        "--output", type=Path, required=True,
        help="Output root directory (e.g. W:/scx_databases)",
    )
    parser.add_argument(
        "--tier", type=int, choices=[1, 2, 3], default=1,
        help="Download tier: 1=core (3.5GB), 2=extended (12GB), 3=full (30GB)",
    )
    parser.add_argument(
        "--databases", nargs="*",
        help="Specific databases to download (overrides --tier)",
    )
    parser.add_argument(
        "--download-only", action="store_true",
        help="Download raw files only, skip parsing",
    )
    args = parser.parse_args()

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    raw_dir = output / "_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Select databases
    if args.databases:
        selected = args.databases
    else:
        selected = [
            name for name, cfg in DATABASE_CONFIGS.items()
            if cfg["tier"] <= args.tier
        ]

    print(f"\n{'='*60}")
    print(f"SCX Drug Database Downloader")
    print(f"Tier: {args.tier}  |  Output: {output}")
    print(f"Databases: {', '.join(selected)}")
    total_size = sum(
        DATABASE_CONFIGS[n]["size_gb"] for n in selected
    )
    print(f"Estimated download: ~{total_size:.1f} GB")
    print(f"{'='*60}\n")

    for db_name in selected:
        cfg = DATABASE_CONFIGS[db_name]
        print(f"[{db_name}] (tier {cfg['tier']}, ~{cfg['size_gb']:.1f} GB)")

        try:
            # Download
            filename = cfg["filename"]
            dest = raw_dir / filename
            download_file(cfg["url"], dest, note=cfg.get("note", ""))

            # Parse (unless --download-only)
            if not args.download_only and db_name in PARSERS:
                PARSERS[db_name](dest, output)
        except Exception as e:
            print(f"    ⚠ FAILED: {e}")
            continue

    print(f"\n{'='*60}")
    print("Download complete.")
    _print_directory_summary(output)
    print(f"{'='*60}\n")


def _print_directory_summary(root: Path) -> None:
    """Print a tree with file sizes."""
    for path in sorted(root.rglob("*")):
        if path.is_file():
            print(f"  {path.relative_to(root)}  ({_human_size(path.stat().st_size)})")


def _human_size(n_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} PB"


def _xml_text(elem: ET.Element, tag_suffix: str, primary: str | None = None) -> str | None:
    """Find first child whose tag ends with *tag_suffix* and return its text."""
    for child in elem.iter():
        if child.tag.endswith("}" + tag_suffix):
            if primary is not None:
                if child.get("primary") == primary:
                    return child.text
            else:
                return child.text
    return None


def _xml_attrib(elem: ET.Element, attrib_name: str) -> str | None:
    return elem.get(attrib_name)


if __name__ == "__main__":
    main()
