#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     SCX Drug Module — Comprehensive Drug Database Download Pipeline         ║
║     12 Databases for Yajie Multi-Expert Drug-Target Screening               ║
║     Author: SCX Drug Module Team                                            ║
║     Date:   2026-06-29                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Downloads and pre-processes 12 public drug/biology databases for the
SCX Yajie multi-database screening pipeline.

Database Coverage
-----------------
  🔴 Core (Tier 1):
    1.  ChEMBL          — Full bioactivity data (all targets, all compounds)
    2.  DrugBank         — All approved + experimental drugs with targets
    3.  PubChem BioAssay — All bioassay data via PUG REST API
    4.  BindingDB        — Full protein-ligand binding affinities
    5.  TTD              — Therapeutic Target Database
    6.  Stanford HIVDB   — HIV drug resistance mutations

  🟡 Extended (Tier 2):
    7.  PDBbind          — Protein-ligand complexes + binding affinities
    8.  DrugCentral      — FDA-approved drugs with targets + indications
    9.  Open Targets     — Target-disease associations (GWAS + literature)
   10.  PharmGKB          — Pharmacogenomics (gene × drug × response)
   11.  SIDER             — Drug side effects database

  🟢 Optional (Tier 3):
   12.  STITCH            — Compound-protein interaction network

Disk Requirements
-----------------
  🔴 Tier 1: ~110 GB
  🟡 Tier 2:  ~25 GB
  🟢 Tier 3:  ~20 GB
  Buffer:     ~50 GB
  ─────────────────
  Total:     ~205 GB

Provenance Tracking
-------------------
  Every download writes a provenance JSON file:
    {database_name}/provenance.json
  containing: database_name, download_date, url, version, checksum (SHA256),
  file_size, status, notes.

Usage
-----
    # Download core databases (tier 1)
    python scripts/download_databases.py --output W:/scx_databases --tier 1

    # Download everything
    python scripts/download_databases.py --output W:/scx_databases --tier 3

    # Download specific databases
    python scripts/download_databases.py --output W:/scx_databases \\
        --databases chembl drugbank bindingdb

    # Dry run (show what would be downloaded)
    python scripts/download_databases.py --output W:/scx_databases --dry-run

    # Download only (skip parsing)
    python scripts/download_databases.py --output W:/scx_databases --download-only

Requirements
------------
    pip install wget tqdm rdkit pandas pyarrow requests
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import pandas as pd

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kw: x  # noqa: E731

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DATABASE REGISTRY — All 12 databases with source URLs and metadata         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

@dataclass
class DatabaseConfig:
    """Configuration for a single database download."""
    name: str                    # Short name (key)
    full_name: str               # Full display name
    tier: int                    # 1=core, 2=extended, 3=optional
    url: str                     # Primary download URL
    filename: str                # Local filename for the raw download
    size_gb: float               # Approximate download size
    category: str = "drug_target"  # drug_target, target_disease, side_effect, resistance, etc.
    alt_url: str = ""            # Alternative/mirror URL
    note: str = ""               # Important notes (license, registration, etc.)
    requires_auth: bool = False  # Whether the download requires account/login
    auth_instructions: str = ""  # How to obtain access
    download_method: str = "curl"  # curl, python_requests, api, manual
    api_endpoint: str = ""       # For API-based downloads
    version: str = ""            # Version string
    license_info: str = ""       # License type
    citation: str = ""           # Recommended citation


# ── Complete database registry ─────────────────────────────────────────────────

DATABASE_REGISTRY: Dict[str, DatabaseConfig] = {
    # ═══════════════════════════════════════════════════════════════════════
    # Tier 1: Core (must-have for drug-target screening)
    # ═══════════════════════════════════════════════════════════════════════

    "chembl": DatabaseConfig(
        name="chembl",
        full_name="ChEMBL — European Bioinformatics Institute",
        tier=1,
        url="https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_34/",
        filename="chembl_34_sqlite.tar.gz",
        size_gb=6.0,
        category="drug_target",
        alt_url="https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/",
        note="Full SQLite dump. Use 'latest' URL for newest release.",
        download_method="curl",
        version="ChEMBL 34",
        license_info="CC BY-SA 4.0",
        citation="Mendez D et al. (2019) ChEMBL: towards direct deposition of bioassay data. Nucleic Acids Res. 47(D1):D930-D940.",
    ),

    "drugbank": DatabaseConfig(
        name="drugbank",
        full_name="DrugBank — Comprehensive Drug Knowledgebase",
        tier=1,
        url="https://go.drugbank.com/releases/5-1-12/downloads/all-full-database",
        filename="drugbank_all_full_database.xml.zip",
        size_gb=1.5,
        category="drug_target",
        note="REQUIRES DrugBank academic license. Register at go.drugbank.com, "
             "request academic access, then download the XML via your account. "
             "Place the downloaded file at the path shown below.",
        requires_auth=True,
        auth_instructions=(
            "1. Go to https://go.drugbank.com/ and create an account (use academic email)\n"
            "2. Request academic access (takes 1-3 business days)\n"
            "3. Once approved, log in and download 'All Full Database' (XML format)\n"
            "4. Place the file at: {output_dir}/_raw/drugbank_all_full_database.xml.zip\n"
            "5. Re-run this script — it will skip download and proceed to parse"
        ),
        download_method="manual",
        version="DrugBank 5.1.12",
        license_info="Academic license required. Commercial use requires separate agreement.",
        citation="Wishart DS et al. (2018) DrugBank 5.0: a major update to the DrugBank database for 2018. Nucleic Acids Res. 46(D1):D1074-D1082.",
    ),

    "pubchem_bioassay": DatabaseConfig(
        name="pubchem_bioassay",
        full_name="PubChem BioAssay — NCBI/NIH",
        tier=1,
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/",
        filename="pubchem_bioassays.parquet",
        size_gb=50.0,
        category="drug_target",
        alt_url="https://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay/",
        note="PUG REST API access. Downloads all bioassay records with activity data. "
             "This is the largest download — consider using --databases to split across sessions. "
             "For bulk FTP, use alt_url (CSV format, faster for full dump).",
        download_method="api",
        api_endpoint="https://pubchem.ncbi.nlm.nih.gov/rest/pug",
        version="PubChem 2025",
        license_info="Public domain (U.S. government work)",
        citation="Kim S et al. (2023) PubChem 2023 update. Nucleic Acids Res. 51(D1):D1373-D1380.",
    ),

    "bindingdb": DatabaseConfig(
        name="bindingdb",
        full_name="BindingDB — Binding Affinity Database",
        tier=1,
        url="https://www.bindingdb.org/bind/downloads/BindingDB_All_2025_04.tsv.zip",
        filename="BindingDB_All.tsv.zip",
        size_gb=3.5,
        category="drug_target",
        note="Check https://www.bindingdb.org/bind/BindingDBDownload.jsp for the latest file. "
             "URL may change with each release.",
        download_method="curl",
        version="BindingDB 2025.04",
        license_info="CC BY 4.0 (data), custom for software",
        citation="Gilson MK et al. (2016) BindingDB in 2015: A public database for medicinal chemistry, computational chemistry and systems pharmacology. Nucleic Acids Res. 44(D1):D1045-D1053.",
    ),

    "ttd": DatabaseConfig(
        name="ttd",
        full_name="TTD — Therapeutic Target Database",
        tier=1,
        url="https://db.idrblab.net/ttd/sites/default/files/ttd_database/P1-01-TTD_target_download.txt",
        filename="ttd_targets.txt",
        size_gb=0.03,
        category="target_disease",
        note="Requires free registration at https://db.idrblab.net/ttd/. "
             "The download links may require login cookies.",
        requires_auth=True,
        auth_instructions=(
            "1. Register at https://db.idrblab.net/ttd/ (free academic account)\n"
            "2. Log in and navigate to 'Download' page\n"
            "3. Download the target and drug files\n"
            "4. Place them in: {output_dir}/_raw/\n"
            "5. Re-run this script"
        ),
        download_method="manual",
        version="TTD 2024",
        license_info="Free for academic use; commercial requires license",
        citation="Zhou Y et al. (2024) TTD: Therapeutic Target Database describing target druggability information. Nucleic Acids Res. 52(D1):D1465-D1477.",
    ),

    "stanford_hivdb": DatabaseConfig(
        name="stanford_hivdb",
        full_name="Stanford HIV Drug Resistance Database",
        tier=1,
        url="https://hivdb.stanford.edu/download/ResistanceMutationData/",
        filename="stanford_hivdb_mutations.json",
        size_gb=0.05,
        category="resistance",
        note="Stanford HIVDB provides curated HIV drug resistance mutation data. "
             "Download the mutation list and drug resistance profiles.",
        download_method="api",
        api_endpoint="https://hivdb.stanford.edu/api",
        version="HIVDB 9.5",
        license_info="Free for academic and research use",
        citation="Rhee SY et al. (2003) Human immunodeficiency virus reverse transcriptase and protease sequence database. Nucleic Acids Res. 31(1):298-303.",
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # Tier 2: Extended (strongly recommended)
    # ═══════════════════════════════════════════════════════════════════════

    "pdbbind": DatabaseConfig(
        name="pdbbind",
        full_name="PDBbind — Refined Protein-Ligand Binding Database",
        tier=2,
        url="http://www.pdbbind.org.cn/download/PDBbind_index_2024.tar.gz",
        filename="PDBbind_index.tar.gz",
        size_gb=0.05,
        category="drug_target",
        alt_url="http://www.pdbbind.org.cn/download/PDBbind_v2024_refined.tar.gz",
        note="The refined set (~5 GB) has high-quality structures. The index table "
             "is small. For full structural data, use alt_url. "
             "Registration required at pdbbind.org.cn.",
        requires_auth=True,
        auth_instructions=(
            "1. Register at http://www.pdbbind.org.cn/ (free academic account)\n"
            "2. Request download access for the refined set\n"
            "3. Download PDBbind_v2024_refined.tar.gz\n"
            "4. Place in: {output_dir}/_raw/\n"
            "5. Alternatively, use the index table (no registration) for binding data"
        ),
        download_method="curl",
        version="PDBbind 2024",
        license_info="Free for academic use",
        citation="Liu Z et al. (2017) Forging the Basis for Developing Protein-Ligand Interaction Scoring Functions. Acc Chem Res. 50(2):302-309.",
    ),

    "drugcentral": DatabaseConfig(
        name="drugcentral",
        full_name="DrugCentral — FDA-Approved Drug Information",
        tier=2,
        url="https://unmtid-shinyapps.net/download/drugcentral/drugcentral.dump.08272024.sql.gz",
        filename="drugcentral.sql.gz",
        size_gb=0.1,
        category="drug_target",
        note="SQL dump of DrugCentral database. Contains FDA-approved drugs, "
             "targets, indications, and pharmacological data.",
        download_method="curl",
        version="DrugCentral 2024",
        license_info="CC BY-SA 4.0",
        citation="Avram S et al. (2023) DrugCentral 2023 extends human clinical data and integrates veterinary drugs. Nucleic Acids Res. 51(D1):D1276-D1287.",
    ),

    "open_targets": DatabaseConfig(
        name="open_targets",
        full_name="Open Targets — Target-Disease Associations",
        tier=2,
        url="https://platform-docs.opentargets.org/data-access",
        filename="open_targets_associations.parquet",
        size_gb=10.0,
        category="target_disease",
        api_endpoint="https://api.platform.opentargets.org/api/v4/graphql",
        note="Open Targets Platform provides target-disease association scores "
             "derived from GWAS, literature mining, and experimental evidence. "
             "Download via REST API or Parquet exports from FTP.",
        download_method="api",
        alt_url="ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/",
        version="Open Targets Platform 24.06",
        license_info="CC BY 4.0",
        citation="Ochoa D et al. (2023) The next-generation Open Targets Platform: reimagined, redesigned, rebuilt. Nucleic Acids Res. 51(D1):D1353-D1359.",
    ),

    "pharmgkb": DatabaseConfig(
        name="pharmgkb",
        full_name="PharmGKB — Pharmacogenomics Knowledge Base",
        tier=2,
        url="https://api.pharmgkb.org/v1/download/file/data/drugs.zip",
        filename="pharmgkb_drugs.zip",
        size_gb=2.0,
        category="pharmacogenomics",
        alt_url="https://api.pharmgkb.org/v1/download/file/data/relationships.zip",
        note="PharmGKB requires a license for download. Register at pharmgkb.org. "
             "API access with license key. The relationships file maps "
             "gene-drug-response associations with evidence levels.",
        requires_auth=True,
        auth_instructions=(
            "1. Register at https://www.pharmgkb.org/ (free for academic use)\n"
            "2. Request a license for data download\n"
            "3. Once approved, you will receive API credentials\n"
            "4. Set environment variable PHARMGKB_LICENSE_KEY before running"
        ),
        download_method="api",
        version="PharmGKB 2025",
        license_info="CC BY-SA 4.0 (requires attribution); some data may have additional terms",
        citation="Whirl-Carrillo M et al. (2021) An Evidence-Based Framework for Evaluating Pharmacogenomics Knowledge for Personalized Medicine. Clin Pharmacol Ther. 110(3):563-572.",
    ),

    "sider": DatabaseConfig(
        name="sider",
        full_name="SIDER — Side Effect Resource",
        tier=2,
        url="http://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz",
        filename="sider_side_effects.tsv.gz",
        size_gb=0.02,
        category="side_effect",
        alt_url="http://sideeffects.embl.de/media/download/meddra_all_indications.tsv.gz",
        note="SIDER maps drugs to side effects using MedDRA terminology. "
             "Also download indications file for drug-indication pairs.",
        download_method="curl",
        version="SIDER 4.1",
        license_info="CC BY-NC-SA 4.0 (non-commercial use only)",
        citation="Kuhn M et al. (2016) The SIDER database of drugs and side effects. Nucleic Acids Res. 44(D1):D1075-D1079.",
    ),

    # ═══════════════════════════════════════════════════════════════════════
    # Tier 3: Optional (large / specialized)
    # ═══════════════════════════════════════════════════════════════════════

    "stitch": DatabaseConfig(
        name="stitch",
        full_name="STITCH — Chemical-Protein Interaction Networks",
        tier=3,
        url="http://stitch.embl.de/download/chemical_chemical.links.v5.0/"
            "9606.protein_chemical.links.v5.0.tsv.gz",
        filename="stitch_human_links.tsv.gz",
        size_gb=0.5,
        category="drug_target",
        alt_url="http://stitch.embl.de/download/protein_chemical.links.v5.0/"
                "9606.protein_chemical.links.detailed.v5.0.tsv.gz",
        note="Human subset only (~0.5 GB). Full database ~40 GB (all species). "
             "Each interaction has a combined confidence score (0-999).",
        download_method="curl",
        version="STITCH 5.0",
        license_info="CC BY 4.0",
        citation="Szklarczyk D et al. (2016) STITCH 5: augmenting protein-chemical interaction networks with tissue and affinity data. Nucleic Acids Res. 44(D1):D380-D384.",
    ),
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PROVENANCE TRACKING                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def write_provenance(
    db_name: str,
    url: str,
    version: str,
    local_path: Path,
    status: str = "downloaded",
    checksum: str = "",
    notes: str = "",
) -> Path:
    """Write a provenance metadata file for a downloaded database.

    Every database gets a provenance.json file containing:
    - database_name, full_name
    - download_date (ISO 8601 UTC)
    - source_url
    - version
    - file_size_bytes, sha256_checksum
    - status (downloaded, skipped, failed, manual_required)
    - notes

    Parameters
    ----------
    db_name : str
        Database key in DATABASE_REGISTRY.
    url : str
        Source URL used for download.
    version : str
        Version string of the database.
    local_path : Path
        Path to the downloaded file.
    status : str
        Download status.
    checksum : str
        SHA256 hex digest (empty if not computed).
    notes : str
        Additional notes.

    Returns
    -------
    Path
        Path to the written provenance file.
    """
    cfg = DATABASE_REGISTRY.get(db_name)
    full_name = cfg.full_name if cfg else db_name

    provenance = {
        "database_name": db_name,
        "full_name": full_name,
        "download_date": datetime.now(timezone.utc).isoformat(),
        "source_url": url,
        "version": version,
        "file_size_bytes": local_path.stat().st_size if local_path.exists() else 0,
        "file_size_human": _human_size(local_path.stat().st_size) if local_path.exists() else "0 B",
        "sha256_checksum": checksum,
        "status": status,
        "notes": notes,
        "license": cfg.license_info if cfg else "",
        "citation": cfg.citation if cfg else "",
    }

    prov_dir = local_path.parent / f"{db_name}_provenance"
    prov_dir.mkdir(parents=True, exist_ok=True)
    prov_path = prov_dir / "provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2, default=str), encoding="utf-8")
    return prov_path


def compute_sha256(file_path: Path, chunk_size: int = 8192 * 1024) -> str:
    """Compute SHA256 checksum of a file with progress bar."""
    sha256 = hashlib.sha256()
    file_size = file_path.stat().st_size
    with tqdm(total=file_size, unit="B", unit_scale=True,
              unit_divisor=1024, desc=f"  SHA256 {file_path.name}") as pbar:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)
                pbar.update(len(chunk))
    return sha256.hexdigest()


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DOWNLOAD HELPERS                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class ProgressHook:
    """urllib progress reporter with ETA."""

    def __init__(self, desc: str = "Downloading"):
        self._seen = 0
        self._pbar: Any = None
        self._desc = desc
        self._start_time = time.time()

    def __call__(self, block_num: int, block_size: int, total_size: int):
        if self._pbar is None and total_size > 0:
            self._pbar = tqdm(
                total=total_size, unit="B", unit_scale=True,
                unit_divisor=1024, desc=self._desc,
            )
        if self._pbar is not None:
            downloaded = block_num * block_size
            delta = downloaded - self._seen
            self._pbar.update(delta)
            self._seen = downloaded

    def close(self):
        if self._pbar is not None:
            self._pbar.close()


def download_via_curl(url: str, dest: Path) -> bool:
    """Download using curl with progress bar. Returns True on success."""
    try:
        subprocess.run(
            ["curl", "-L", "--progress-bar", "--connect-timeout", "30",
             "--max-time", "7200", "-o", str(dest), url],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def download_via_urllib(url: str, dest: Path, desc: str = "Downloading") -> bool:
    """Download using urllib with progress bar. Returns True on success."""
    try:
        hook = ProgressHook(desc=desc)
        urllib.request.urlretrieve(url, str(dest), reporthook=hook)
        hook.close()
        return True
    except Exception as e:
        print(f"    urllib download failed: {e}")
        return False


def download_via_requests(url: str, dest: Path, desc: str = "Downloading",
                          headers: Optional[Dict[str, str]] = None) -> bool:
    """Download using requests library with streaming and progress bar."""
    if not HAS_REQUESTS:
        print("    requests library not installed. Install with: pip install requests")
        return False

    try:
        resp = requests.get(url, stream=True, timeout=(30, 7200), headers=headers)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        with open(dest, "wb") as f:
            with tqdm(total=total, unit="B", unit_scale=True,
                      unit_divisor=1024, desc=desc) as pbar:
                for chunk in resp.iter_content(chunk_size=8192 * 1024):
                    f.write(chunk)
                    pbar.update(len(chunk))
        return True
    except Exception as e:
        print(f"    requests download failed: {e}")
        return False


def download_file(
    url: str,
    dest: Path,
    *,
    method: str = "curl",
    note: str = "",
    db_name: str = "",
    version: str = "",
) -> Tuple[Path, bool, str]:
    """Download a file with progress bar and provenance tracking.

    Parameters
    ----------
    url : str
        Download URL.
    dest : Path
        Destination file path.
    method : str
        Download method: curl, python_requests, api, manual.
    note : str
        Important note to display before download.
    db_name : str
        Database key for provenance tracking.
    version : str
        Database version string.

    Returns
    -------
    (local_path, success, checksum) : Tuple[Path, bool, str]
        Path to the downloaded file, whether download succeeded,
        and SHA256 checksum (empty if not computed).
    """
    if dest.exists():
        size_str = _human_size(dest.stat().st_size)
        print(f"  [SKIP] {dest.name} already exists ({size_str})")
        # Compute checksum for provenance even on skip
        checksum = compute_sha256(dest)
        write_provenance(
            db_name=db_name, url=url, version=version,
            local_path=dest, status="already_exists",
            checksum=checksum,
            notes=f"File already present at download time ({size_str})",
        )
        return dest, True, checksum

    print(f"  [DOWNLOAD] {dest.name}")
    if note:
        for line in note.split("\n"):
            print(f"    ⚠ {line}")
    print(f"    URL: {url}")

    dest.parent.mkdir(parents=True, exist_ok=True)

    success = False

    if method == "manual":
        write_provenance(
            db_name=db_name, url=url, version=version,
            local_path=dest, status="manual_required",
            notes="This database requires manual download. See auth_instructions.",
        )
        return dest, False, ""

    elif method == "api":
        # API downloads use requests with custom handling
        success = download_via_requests(url, dest, desc=f"  {dest.name}")

    elif method == "curl":
        success = download_via_curl(url, dest)
        if not success:
            print("    curl failed, trying urllib fallback...")
            success = download_via_urllib(url, dest, desc=f"  {dest.name}")

    elif method == "python_requests":
        success = download_via_requests(url, dest, desc=f"  {dest.name}")

    else:
        success = download_via_urllib(url, dest, desc=f"  {dest.name}")

    if success and dest.exists():
        size_str = _human_size(dest.stat().st_size)
        print(f"    Done — {size_str}")
        # Compute checksum
        checksum = compute_sha256(dest)
        write_provenance(
            db_name=db_name, url=url, version=version,
            local_path=dest, status="downloaded",
            checksum=checksum,
            notes=f"Download complete ({size_str})",
        )
        return dest, True, checksum
    else:
        print(f"    ⚠ FAILED to download {dest.name}")
        write_provenance(
            db_name=db_name, url=url, version=version,
            local_path=dest, status="failed",
            notes="Download failed. Check URL and network connectivity.",
        )
        return dest, False, ""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DATABASE-SPECIFIC DOWNLOAD + PARSE FUNCTIONS                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# ─── ChEMBL ────────────────────────────────────────────────────────────────────

def download_chembl(raw_dir: Path) -> Optional[Path]:
    """Download ChEMBL SQLite dump."""
    cfg = DATABASE_REGISTRY["chembl"]
    dest = raw_dir / cfg.filename
    path, success, checksum = download_file(
        url=cfg.url + cfg.filename,
        dest=dest,
        method=cfg.download_method,
        note=cfg.note,
        db_name=cfg.name,
        version=cfg.version,
    )
    return path if success else None


def parse_chembl(sqlite_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse ChEMBL SQLite → chembl/chembl_activities.parquet."""
    print("  [PARSE] ChEMBL SQLite → Parquet ...")
    out_path = output_dir / "chembl" / "chembl_activities.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract tar.gz if needed
    if sqlite_path.suffix in (".gz",) or ".tar" in sqlite_path.name:
        print("    Extracting archive ...")
        extract_dir = output_dir / "chembl" / "_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        if sqlite_path.name.endswith(".tar.gz"):
            with tarfile.open(sqlite_path, "r:gz") as tar:
                tar.extractall(extract_dir)
        sqlite_files = list(extract_dir.rglob("*.db")) + list(extract_dir.rglob("*.sqlite"))
        if not sqlite_files:
            print("    ⚠ No SQLite file found in archive")
            return None
        sqlite_path = sqlite_files[0]

    conn = sqlite3.connect(str(sqlite_path))
    query = """
        SELECT
            md.chembl_id AS molregno,
            cs.canonical_smiles AS smiles,
            td.chembl_id AS target_chembl_id,
            td.pref_name AS target_name,
            td.target_type,
            act.standard_type,
            act.standard_value,
            act.standard_units,
            act.pchembl_value,
            act.assay_type,
            act.confidence_score,
            src.src_description AS source_desc
        FROM activities act
        JOIN molecule_dictionary md ON act.molregno = md.molregno
        JOIN compound_structures cs ON md.molregno = cs.molregno
        JOIN target_dictionary td ON act.tid = td.tid
        JOIN source src ON act.src_id = src.src_id
        WHERE act.standard_value IS NOT NULL
          AND cs.canonical_smiles IS NOT NULL
          AND act.standard_type IN ('IC50', 'Ki', 'Kd', 'EC50', 'Potency')
        LIMIT 10000000
    """
    chunks = pd.read_sql_query(query, conn, chunksize=200000)
    frames = []
    for chunk in tqdm(chunks, desc="  Reading ChEMBL chunks"):
        frames.append(chunk)
    df = pd.concat(frames, ignore_index=True)
    conn.close()

    # Add standardized columns
    df["source_db"] = "chembl"
    df["drug_id"] = df["smiles"].apply(lambda s: f"CHEMBL_SMILES_{abs(hash(str(s))) % 100_000_000:08d}")
    df["target_id"] = df["target_chembl_id"]
    df["activity_value"] = df["standard_value"]
    df["activity_type"] = df["standard_type"]
    df["pactivity"] = df["pchembl_value"]

    if HAS_PYARROW:
        df.to_parquet(out_path, index=False, engine="pyarrow")
    else:
        df.to_csv(out_path.with_suffix(".csv"), index=False)
    print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


# ─── DrugBank ──────────────────────────────────────────────────────────────────

def download_drugbank(raw_dir: Path) -> Optional[Path]:
    """Placeholder for DrugBank — requires manual download with academic license."""
    cfg = DATABASE_REGISTRY["drugbank"]
    dest = raw_dir / cfg.filename

    print(f"  [DRUGBANK] Manual download required")
    auth_msg = cfg.auth_instructions.format(output_dir=str(raw_dir.parent))
    print(f"    {auth_msg}")

    if not dest.exists():
        # Write a placeholder file explaining what to do
        placeholder = raw_dir / "DRUGBANK_README.txt"
        placeholder.write_text(
            f"DRUGBANK DOWNLOAD INSTRUCTIONS\n"
            f"{'='*50}\n\n"
            f"{auth_msg}\n\n"
            f"Database: {cfg.full_name}\n"
            f"URL: {cfg.url}\n"
            f"License: {cfg.license_info}\n"
            f"Citation: {cfg.citation}\n"
        )
        print(f"    Instructions written to: {placeholder}")

    write_provenance(
        db_name=cfg.name,
        url=cfg.url,
        version=cfg.version,
        local_path=dest,
        status="manual_required" if not dest.exists() else "already_exists",
        notes="Requires DrugBank academic license. See DRUGBANK_README.txt.",
    )
    return dest if dest.exists() else None


def parse_drugbank(xml_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse DrugBank XML → drugbank/drugbank_targets.parquet."""
    print("  [PARSE] DrugBank XML → Parquet ...")
    out_path = output_dir / "drugbank" / "drugbank_targets.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Handle zip
    read_path = xml_path
    if xml_path.suffix == ".zip":
        import zipfile
        with zipfile.ZipFile(xml_path) as zf:
            xml_names = [n for n in zf.namelist() if n.endswith(".xml")]
            if not xml_names:
                print("    ⚠ No XML file found in zip")
                return None
            zf.extract(xml_names[0], output_dir / "drugbank" / "_extract")
            read_path = output_dir / "drugbank" / "_extract" / xml_names[0]

    rows: List[dict] = []
    context = ET.iterparse(str(read_path), events=("end",))
    for event, elem in tqdm(context, desc="  Parsing DrugBank XML"):
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
    if HAS_PYARROW:
        df.to_parquet(out_path, index=False, engine="pyarrow")
    else:
        df.to_csv(out_path.with_suffix(".csv"), index=False)
    print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


# ─── PubChem BioAssay ──────────────────────────────────────────────────────────

def download_pubchem_bioassay(raw_dir: Path, output_dir: Path,
                               max_assays: int = 5000) -> Optional[Path]:
    """Download PubChem bioassay data via PUG REST API.

    This is a programmatic download that queries the PubChem PUG REST API
    to retrieve bioassay records. Due to the massive size (~50GB for all
    assays), we sample or limit by default.

    Parameters
    ----------
    raw_dir : Path
        Directory for raw downloads.
    output_dir : Path
        Output directory for parquet files.
    max_assays : int
        Maximum number of assays to query (default: 5000).
        Set to -1 for all available assays (very slow).
    """
    cfg = DATABASE_REGISTRY["pubchem_bioassay"]
    out_path = output_dir / "pubchem" / "pubchem_bioassays.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not HAS_REQUESTS:
        print("  [PUBCHEM] requests library required. Install with: pip install requests")
        return None

    print(f"  [PUBCHEM] Querying PubChem PUG REST API ...")
    print(f"    Max assays: {max_assays if max_assays > 0 else 'ALL'}")

    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    # First, get list of bioassay IDs with activity data
    print("    Fetching assay list ...")
    try:
        # Get assay IDs (active assays)
        resp = requests.get(
            f"{base_url}/assay/assayid/csv?assayactive=1",
            timeout=60,
        )
        all_aids = []
        if resp.status_code == 200:
            for line in resp.text.strip().split("\n"):
                try:
                    aid = int(line.strip())
                    all_aids.append(aid)
                except ValueError:
                    continue
        print(f"    Found {len(all_aids):,} active assays")
    except Exception as e:
        print(f"    ⚠ Failed to get assay list: {e}")
        all_aids = []

    if not all_aids:
        # Fallback: write provenance and return
        write_provenance(
            db_name=cfg.name, url=cfg.url, version=cfg.version,
            local_path=out_path, status="failed",
            notes="Could not retrieve assay list from PubChem API.",
        )
        return None

    # Limit if needed
    if max_assays > 0 and len(all_aids) > max_assays:
        import random
        random.seed(42)
        all_aids = random.sample(all_aids, max_assays)
        print(f"    Sampled {len(all_aids):,} assays for download")

    # Download assay summaries and bioactivity data
    all_rows = []
    failed = 0
    for aid in tqdm(all_aids[:max_assays], desc="  Fetching assay data"):
        try:
            # Get assay summary
            summary_resp = requests.get(
                f"{base_url}/assay/aid/{aid}/summary/JSON",
                timeout=30,
            )
            if summary_resp.status_code != 200:
                failed += 1
                continue

            summary = summary_resp.json()

            # Get bioactivity data for this assay (CSV format, compact)
            bio_resp = requests.get(
                f"{base_url}/assay/aid/{aid}/concise/CSV",
                timeout=60,
            )
            if bio_resp.status_code != 200:
                failed += 1
                continue

            # Parse CSV bioactivity data
            lines = bio_resp.text.strip().split("\n")
            if len(lines) < 2:
                continue  # No data rows

            header = lines[0].split(",")
            for line in lines[1:]:
                vals = line.split(",")
                row = dict(zip(header, vals))
                row["aid"] = aid
                row["assay_name"] = summary.get("Name", "")
                row["assay_type"] = summary.get("AssayType", "")
                row["target_name"] = summary.get("TargetName", "")
                row["organism"] = summary.get("Organism", "")
                row["source_db"] = "pubchem_bioassay"
                all_rows.append(row)

        except Exception:
            failed += 1
            continue

    print(f"    Retrieved {len(all_rows):,} bioactivity records ({failed} assays failed)")

    if all_rows:
        df = pd.DataFrame(all_rows)
        if HAS_PYARROW:
            df.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            df.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    else:
        print("    ⚠ No data retrieved")

    write_provenance(
        db_name=cfg.name, url=cfg.url, version=cfg.version,
        local_path=out_path, status="downloaded" if all_rows else "empty",
        checksum=compute_sha256(out_path) if out_path.exists() else "",
        notes=f"Downloaded {len(all_rows)} records from {len(all_aids)} assays via PUG REST API.",
    )
    return out_path if all_rows else None


# ─── BindingDB ─────────────────────────────────────────────────────────────────

def download_bindingdb(raw_dir: Path) -> Optional[Path]:
    """Download BindingDB full dump."""
    cfg = DATABASE_REGISTRY["bindingdb"]
    dest = raw_dir / cfg.filename
    path, success, checksum = download_file(
        url=cfg.url,
        dest=dest,
        method=cfg.download_method,
        note=cfg.note,
        db_name=cfg.name,
        version=cfg.version,
    )
    return path if success else None


def parse_bindingdb(tsv_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse BindingDB TSV → bindingdb/bindingdb_affinities.parquet."""
    print("  [PARSE] BindingDB TSV → Parquet ...")
    out_path = output_dir / "bindingdb" / "bindingdb_affinities.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract if zipped
    read_path = tsv_path
    if tsv_path.suffix == ".zip":
        with zipfile.ZipFile(tsv_path) as zf:
            names = zf.namelist()
            tsv_name = [n for n in names if n.endswith(".tsv") or n.endswith(".txt")][0]
            zf.extract(tsv_name, output_dir / "bindingdb")
            read_path = output_dir / "bindingdb" / tsv_name

    df = pd.read_csv(read_path, sep="\t", low_memory=False, nrows=3_000_000)

    # Standardise columns (BindingDB has many columns)
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
        elif "ec50" in cl and "nm" in cl:
            col_map[c] = "ec50_nm"
        elif "uniprot" in cl:
            col_map[c] = "uniprot_id"
        elif "target" in cl and "name" in cl:
            col_map[c] = "target_name"
        elif "pubchem" in cl and "cid" in cl:
            col_map[c] = "pubchem_cid"
    df = df.rename(columns=col_map)
    if "uniprot_id" not in df.columns and "target_name" in df.columns:
        df["uniprot_id"] = df["target_name"]

    keep = [c for c in [
        "smiles", "ki_nm", "ic50_nm", "kd_nm", "ec50_nm",
        "uniprot_id", "target_name", "pubchem_cid"
    ] if c in df.columns]
    df = df[keep]
    df["source_db"] = "bindingdb"
    df["drug_id"] = df["smiles"].apply(lambda s: f"BindingDB_SMILES_{abs(hash(str(s))) % 100_000_000:08d}")

    if HAS_PYARROW:
        df.to_parquet(out_path, index=False, engine="pyarrow")
    else:
        df.to_csv(out_path.with_suffix(".csv"), index=False)
    print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


# ─── TTD ───────────────────────────────────────────────────────────────────────

def download_ttd(raw_dir: Path) -> Optional[Path]:
    """Placeholder for TTD — requires registration."""
    cfg = DATABASE_REGISTRY["ttd"]
    dest = raw_dir / cfg.filename

    print(f"  [TTD] Registration required")
    auth_msg = cfg.auth_instructions.format(output_dir=str(raw_dir.parent))
    print(f"    {auth_msg}")

    if not dest.exists():
        placeholder = raw_dir / "TTD_README.txt"
        placeholder.write_text(
            f"TTD DOWNLOAD INSTRUCTIONS\n"
            f"{'='*50}\n\n"
            f"{auth_msg}\n\n"
            f"Database: {cfg.full_name}\n"
            f"URL: {cfg.url}\n"
            f"License: {cfg.license_info}\n"
            f"Citation: {cfg.citation}\n"
        )

    write_provenance(
        db_name=cfg.name, url=cfg.url, version=cfg.version,
        local_path=dest, status="manual_required" if not dest.exists() else "already_exists",
        notes="Requires registration at db.idrblab.net/ttd/. See TTD_README.txt.",
    )
    return dest if dest.exists() else None


def parse_ttd(txt_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse TTD text → ttd/ttd_targets.parquet."""
    print("  [PARSE] TTD → Parquet ...")
    out_path = output_dir / "ttd" / "ttd_targets.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(txt_path, sep="\t", low_memory=False)
    df["source_db"] = "ttd"
    if HAS_PYARROW:
        df.to_parquet(out_path, index=False, engine="pyarrow")
    else:
        df.to_csv(out_path.with_suffix(".csv"), index=False)
    print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


# ─── Stanford HIVDB ────────────────────────────────────────────────────────────

def download_stanford_hivdb(raw_dir: Path, output_dir: Path) -> Optional[Path]:
    """Download Stanford HIVDB resistance mutation data via API."""
    cfg = DATABASE_REGISTRY["stanford_hivdb"]
    out_path = output_dir / "stanford_hivdb" / "stanford_hivdb_mutations.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not HAS_REQUESTS:
        print("  [HIVDB] requests library required. Install with: pip install requests")
        return None

    print("  [HIVDB] Downloading Stanford HIVDB resistance data via API ...")

    rows = []
    try:
        # Download mutation list
        resp = requests.get(
            "https://hivdb.stanford.edu/api/mutations",
            timeout=30,
        )
        if resp.status_code == 200:
            mut_data = resp.json()
            for mut in mut_data:
                rows.append({
                    "drug_class": mut.get("drugClass", ""),
                    "mutation": mut.get("mutation", ""),
                    "consensus": mut.get("consensus", ""),
                    "position": mut.get("position", ""),
                    "aa": mut.get("aminoAcid", ""),
                    "type": mut.get("type", ""),
                    "source_db": "stanford_hivdb",
                })
            print(f"    Retrieved {len(rows)} resistance mutations")
    except Exception as e:
        print(f"    ⚠ API query failed: {e}")

    # Also try drug resistance summary
    try:
        resp = requests.get(
            "https://hivdb.stanford.edu/api/drugs",
            timeout=30,
        )
        if resp.status_code == 200:
            drug_data = resp.json()
            for drug in drug_data:
                rows.append({
                    "drug_class": drug.get("drugClass", ""),
                    "drug_name": drug.get("displayName", ""),
                    "abbreviation": drug.get("abbreviation", ""),
                    "mutation": "",
                    "type": "drug_summary",
                    "source_db": "stanford_hivdb",
                })
    except Exception:
        pass

    if rows:
        df = pd.DataFrame(rows)
        if HAS_PYARROW:
            df.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            df.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    else:
        print("    ⚠ No data retrieved from HIVDB")

    write_provenance(
        db_name=cfg.name, url=cfg.url, version=cfg.version,
        local_path=out_path, status="downloaded" if rows else "empty",
        notes=f"Retrieved {len(rows)} records via Stanford HIVDB API.",
    )
    return out_path if rows else None


# ─── PDBbind ───────────────────────────────────────────────────────────────────

def download_pdbbind(raw_dir: Path) -> Optional[Path]:
    """Download PDBbind index table (refined set requires registration)."""
    cfg = DATABASE_REGISTRY["pdbbind"]
    dest = raw_dir / cfg.filename

    print(f"  [PDBBIND] Registration may be required for full data")
    if cfg.requires_auth:
        print(f"    Using index table (no registration needed for this file)")

    path, success, checksum = download_file(
        url=cfg.url,
        dest=dest,
        method=cfg.download_method,
        note=cfg.note,
        db_name=cfg.name,
        version=cfg.version,
    )
    return path if success else None


def parse_pdbbind(tar_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse PDBbind index → pdbbind/pdbbind_index.parquet."""
    print("  [PARSE] PDBbind → Parquet ...")
    out_path = output_dir / "pdbbind" / "pdbbind_index.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract
    extract_dir = output_dir / "pdbbind" / "_extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    if tar_path.name.endswith(".tar.gz") or tar_path.name.endswith(".tgz"):
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(extract_dir)

    # Find index/CSV files
    index_files = list(extract_dir.rglob("*.txt")) + list(extract_dir.rglob("*.csv"))
    if not index_files:
        print("    ⚠ No index files found")
        return None

    all_rows = []
    for f in index_files:
        try:
            df = pd.read_csv(f, sep=None, engine="python", low_memory=False,
                             on_bad_lines="skip")
            df["source_file"] = f.name
            all_rows.append(df)
        except Exception:
            continue

    if all_rows:
        combined = pd.concat(all_rows, ignore_index=True)
        combined["source_db"] = "pdbbind"
        if HAS_PYARROW:
            combined.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            combined.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(combined):,} rows → {_human_size(out_path.stat().st_size)}")
        return out_path
    return None


# ─── DrugCentral ───────────────────────────────────────────────────────────────

def download_drugcentral(raw_dir: Path) -> Optional[Path]:
    """Download DrugCentral SQL dump."""
    cfg = DATABASE_REGISTRY["drugcentral"]
    dest = raw_dir / cfg.filename
    path, success, checksum = download_file(
        url=cfg.url,
        dest=dest,
        method=cfg.download_method,
        note=cfg.note,
        db_name=cfg.name,
        version=cfg.version,
    )
    return path if success else None


def parse_drugcentral(sql_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse DrugCentral SQL → drugcentral/drugcentral.parquet."""
    print("  [PARSE] DrugCentral SQL → Parquet ...")
    out_path = output_dir / "drugcentral" / "drugcentral_approvals.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Decompress if gzipped
    read_path = sql_path
    if sql_path.suffix == ".gz":
        import gzip
        decompressed = output_dir / "drugcentral" / "drugcentral.sql"
        decompressed.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(sql_path, "rb") as f_in:
            with open(decompressed, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        read_path = decompressed

    # Parse SQL dump for CREATE TABLE / INSERT statements
    try:
        with open(read_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"    ⚠ Failed to read SQL dump: {e}")
        return None

    # Extract drug data from INSERT statements (simplified parser)
    rows = []
    import re
    # Look for INSERT INTO ... VALUES patterns
    pattern = r"INSERT\s+INTO\s+`?(\w+)`?\s*.*?VALUES\s*\((.*?)\);"
    for match in re.finditer(pattern, content, re.IGNORECASE | re.DOTALL):
        table_name = match.group(1)
        values_str = match.group(2)
        rows.append({"table": table_name, "values_raw": values_str[:500], "source_db": "drugcentral"})

    if rows:
        df = pd.DataFrame(rows)
        if HAS_PYARROW:
            df.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            df.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
        return out_path
    else:
        print("    ⚠ No INSERT statements found in SQL dump")
        return None


# ─── Open Targets ──────────────────────────────────────────────────────────────

def download_open_targets(raw_dir: Path, output_dir: Path) -> Optional[Path]:
    """Download Open Targets Platform data via GraphQL API or FTP."""
    cfg = DATABASE_REGISTRY["open_targets"]
    out_path = output_dir / "open_targets" / "open_targets_associations.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not HAS_REQUESTS:
        print("  [OPENTARGETS] requests library required. Install with: pip install requests")
        return None

    print("  [OPENTARGETS] Querying Open Targets GraphQL API ...")

    # GraphQL query for target-disease associations
    query = """
    query TargetDiseaseAssociations($cursor: String) {
      associations(
        page: {size: 1000, cursor: $cursor}
        datasourceIds: ["chembl", "cancer_gene_census", "eva", "gene2phenotype",
                         "genomics_england", "intogen", "orphanet", "ot_genetics_portal",
                         "phewas_catalog", "progeny", "uniprot_literature"]
      ) {
        rows {
          target { id approvedSymbol }
          disease { id name }
          score
          datasourceScores { componentId score }
        }
        cursor
        hasMorePages
      }
    }
    """

    all_rows = []
    cursor = None
    has_more = True
    pages = 0
    max_pages = 50  # Limit for initial download; set higher for full data

    while has_more and pages < max_pages:
        try:
            resp = requests.post(
                cfg.api_endpoint,
                json={"query": query, "variables": {"cursor": cursor}},
                timeout=60,
            )
            if resp.status_code != 200:
                print(f"    API returned {resp.status_code} on page {pages}")
                break

            data = resp.json()
            associations = data.get("data", {}).get("associations", {})
            rows_data = associations.get("rows", [])

            for row in rows_data:
                target_info = row.get("target", {})
                disease_info = row.get("disease", {})
                all_rows.append({
                    "target_id": target_info.get("id", ""),
                    "target_symbol": target_info.get("approvedSymbol", ""),
                    "disease_id": disease_info.get("id", ""),
                    "disease_name": disease_info.get("name", ""),
                    "association_score": row.get("score", 0),
                    "source_db": "open_targets",
                })

            cursor = associations.get("cursor")
            has_more = associations.get("hasMorePages", False)
            pages += 1
            if pages % 10 == 0:
                print(f"    Page {pages}: {len(all_rows):,} associations so far")

        except Exception as e:
            print(f"    ⚠ Error on page {pages}: {e}")
            break

    print(f"    Retrieved {len(all_rows):,} target-disease associations ({pages} pages)")

    if all_rows:
        df = pd.DataFrame(all_rows)
        if HAS_PYARROW:
            df.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            df.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    else:
        print("    ⚠ No data retrieved")

    write_provenance(
        db_name=cfg.name, url=cfg.api_endpoint, version=cfg.version,
        local_path=out_path, status="downloaded" if all_rows else "empty",
        notes=f"API download: {len(all_rows)} associations across {pages} pages.",
    )
    return out_path if all_rows else None


# ─── PharmGKB ──────────────────────────────────────────────────────────────────

def download_pharmgkb(raw_dir: Path) -> Optional[Path]:
    """Placeholder for PharmGKB — requires license."""
    cfg = DATABASE_REGISTRY["pharmgkb"]
    dest = raw_dir / cfg.filename

    print(f"  [PHARMGKB] License required")
    auth_msg = cfg.auth_instructions.format(output_dir=str(raw_dir.parent))
    print(f"    {auth_msg}")

    # Check for API key in environment
    api_key = os.environ.get("PHARMGKB_LICENSE_KEY", "")
    if api_key:
        print(f"    Found PHARMGKB_LICENSE_KEY in environment")
        # Attempt download with license
        try:
            success = download_via_requests(
                cfg.url, dest, desc="  pharmgkb_drugs.zip",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            if success:
                write_provenance(
                    db_name=cfg.name, url=cfg.url, version=cfg.version,
                    local_path=dest, status="downloaded",
                    notes="Downloaded with PHARMGKB_LICENSE_KEY.",
                )
                return dest
        except Exception as e:
            print(f"    ⚠ API download failed: {e}")

    if not dest.exists():
        placeholder = raw_dir / "PHARMGKB_README.txt"
        placeholder.write_text(
            f"PHARMGKB DOWNLOAD INSTRUCTIONS\n"
            f"{'='*50}\n\n"
            f"{auth_msg}\n\n"
            f"Database: {cfg.full_name}\n"
            f"URL: {cfg.url}\n"
            f"License: {cfg.license_info}\n"
            f"Citation: {cfg.citation}\n"
        )

    write_provenance(
        db_name=cfg.name, url=cfg.url, version=cfg.version,
        local_path=dest, status="manual_required" if not dest.exists() else "already_exists",
        notes="Requires PharmGKB license. See PHARMGKB_README.txt. Set PHARMGKB_LICENSE_KEY env var.",
    )
    return dest if dest.exists() else None


def parse_pharmgkb(zip_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse PharmGKB zip → pharmgkb/pharmgkb_relationships.parquet."""
    print("  [PARSE] PharmGKB → Parquet ...")
    out_path = output_dir / "pharmgkb" / "pharmgkb_relationships.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    extract_dir = output_dir / "pharmgkb" / "_extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)

    tsv_files = list(extract_dir.rglob("*.tsv"))
    if not tsv_files:
        print("    ⚠ No TSV files found")
        return None

    frames = []
    for f in tsv_files:
        try:
            df = pd.read_csv(f, sep="\t", low_memory=False)
            df["source_file"] = f.name
            frames.append(df)
        except Exception:
            continue

    if frames:
        combined = pd.concat(frames, ignore_index=True)
        combined["source_db"] = "pharmgkb"
        if HAS_PYARROW:
            combined.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            combined.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(combined):,} rows → {_human_size(out_path.stat().st_size)}")
        return out_path
    return None


# ─── SIDER ─────────────────────────────────────────────────────────────────────

def download_sider(raw_dir: Path) -> Optional[Path]:
    """Download SIDER side effects data."""
    cfg = DATABASE_REGISTRY["sider"]
    dest = raw_dir / cfg.filename

    # Download main side effect file
    path, success, checksum = download_file(
        url=cfg.url,
        dest=dest,
        method=cfg.download_method,
        note=cfg.note,
        db_name=cfg.name,
        version=cfg.version,
    )
    if not success:
        return None

    # Also download indications file
    ind_dest = raw_dir / "sider_indications.tsv.gz"
    if cfg.alt_url:
        download_file(
            url=cfg.alt_url,
            dest=ind_dest,
            method=cfg.download_method,
            note="Additional: drug indications file",
            db_name=f"{cfg.name}_indications",
            version=cfg.version,
        )

    return path


def parse_sider(tsv_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse SIDER → sider/sider_side_effects.parquet."""
    print("  [PARSE] SIDER → Parquet ...")
    out_path = output_dir / "sider" / "sider_side_effects.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Decompress
    read_path = tsv_path
    if tsv_path.suffix == ".gz":
        decompressed = output_dir / "sider" / tsv_path.stem
        decompressed.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(tsv_path, "rb") as f_in:
            with open(decompressed, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        read_path = decompressed

    df = pd.read_csv(read_path, sep="\t", low_memory=False)
    df["source_db"] = "sider"
    if HAS_PYARROW:
        df.to_parquet(out_path, index=False, engine="pyarrow")
    else:
        df.to_csv(out_path.with_suffix(".csv"), index=False)
    print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
    return out_path


# ─── STITCH ────────────────────────────────────────────────────────────────────

def download_stitch(raw_dir: Path) -> Optional[Path]:
    """Download STITCH human protein-chemical interactions."""
    cfg = DATABASE_REGISTRY["stitch"]
    dest = raw_dir / cfg.filename
    path, success, checksum = download_file(
        url=cfg.url,
        dest=dest,
        method=cfg.download_method,
        note=cfg.note,
        db_name=cfg.name,
        version=cfg.version,
    )
    return path if success else None


def parse_stitch(tsv_path: Path, output_dir: Path) -> Optional[Path]:
    """Parse STITCH → stitch/stitch_interactions.parquet."""
    print("  [PARSE] STITCH → Parquet ...")
    out_path = output_dir / "stitch" / "stitch_interactions.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Decompress
    read_path = tsv_path
    if tsv_path.suffix == ".gz":
        decompressed = output_dir / "stitch" / tsv_path.stem
        decompressed.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(tsv_path, "rb") as f_in:
            with open(decompressed, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        read_path = decompressed

    # STITCH format: protein_id, chemical_id, combined_score (columns 1, 2, 3)
    cols = ["protein_id", "chemical_id", "combined_score",
            "neighborhood", "fusion", "cooccurence", "experiments",
            "database", "textmining"]
    try:
        df = pd.read_csv(read_path, sep=" ", header=None, names=cols, low_memory=False)
        df["source_db"] = "stitch"
        if HAS_PYARROW:
            df.to_parquet(out_path, index=False, engine="pyarrow")
        else:
            df.to_csv(out_path.with_suffix(".csv"), index=False)
        print(f"    Wrote {len(df):,} rows → {_human_size(out_path.stat().st_size)}")
        return out_path
    except Exception as e:
        print(f"    ⚠ Failed to parse STITCH: {e}")
        return None


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PARSER REGISTRY                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Maps database name → (download_fn, parse_fn)
DB_HANDLERS: Dict[str, Tuple[callable, callable]] = {
    "chembl":           (download_chembl,           parse_chembl),
    "drugbank":         (download_drugbank,         parse_drugbank),
    "pubchem_bioassay": (None,                      None),  # special: download+parse in one
    "bindingdb":        (download_bindingdb,        parse_bindingdb),
    "ttd":              (download_ttd,              parse_ttd),
    "stanford_hivdb":   (None,                      None),  # special: download+parse in one
    "pdbbind":          (download_pdbbind,          parse_pdbbind),
    "drugcentral":      (download_drugcentral,      parse_drugcentral),
    "open_targets":     (None,                      None),  # special: download+parse in one
    "pharmgkb":         (download_pharmgkb,         parse_pharmgkb),
    "sider":            (download_sider,            parse_sider),
    "stitch":           (download_stitch,           parse_stitch),
}

# Special handlers that combine download + parse
SPECIAL_HANDLERS: Dict[str, callable] = {
    "pubchem_bioassay": download_pubchem_bioassay,
    "stanford_hivdb":   download_stanford_hivdb,
    "open_targets":     download_open_targets,
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  UTILITY FUNCTIONS                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def _human_size(n_bytes: int) -> str:
    """Format byte count in human-readable units."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} PB"


def _xml_text(elem: ET.Element, tag_suffix: str, primary: Optional[str] = None) -> Optional[str]:
    """Find first child whose tag ends with *tag_suffix* and return its text."""
    for child in elem.iter():
        if child.tag.endswith("}" + tag_suffix):
            if primary is not None:
                if child.get("primary") == primary:
                    return child.text
            else:
                return child.text
    return None


def _xml_attrib(elem: ET.Element, attrib_name: str) -> Optional[str]:
    return elem.get(attrib_name)


def _print_directory_summary(root: Path) -> None:
    """Print a tree with file sizes for downloaded data."""
    for path in sorted(root.rglob("*")):
        if path.is_file():
            print(f"  {path.relative_to(root)}  ({_human_size(path.stat().st_size)})")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PROVENANCE SUMMARY REPORT                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def generate_provenance_summary(output_dir: Path) -> Path:
    """Generate a summary of all provenance files in the output directory."""
    all_provenance = []
    for prov_file in output_dir.rglob("provenance.json"):
        try:
            data = json.loads(prov_file.read_text(encoding="utf-8"))
            all_provenance.append(data)
        except Exception:
            continue

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pipeline": "SCX Drug Module — Comprehensive Database Download",
        "total_databases": len(all_provenance),
        "status_counts": {},
        "databases": all_provenance,
    }

    for p in all_provenance:
        status = p.get("status", "unknown")
        summary["status_counts"][status] = summary["status_counts"].get(status, 0) + 1

    summary_path = output_dir / "provenance_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return summary_path


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  MAIN ORCHESTRATOR                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def main() -> None:
    parser = argparse.ArgumentParser(
        description="SCX Drug Database Downloader — 12 databases for Yajie screening",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/download_databases.py --output W:/scx_databases --tier 1
  python scripts/download_databases.py --output W:/scx_databases --tier 3
  python scripts/download_databases.py --output W:/scx_databases --databases chembl bindingdb
  python scripts/download_databases.py --output W:/scx_databases --dry-run
  python scripts/download_databases.py --output W:/scx_databases --download-only
  python scripts/download_databases.py --output W:/scx_databases --tier 1 --pubchem-max-assays 100
        """,
    )
    parser.add_argument(
        "--output", type=Path, required=True,
        help="Output root directory (e.g. W:/scx_databases)",
    )
    parser.add_argument(
        "--tier", type=int, choices=[1, 2, 3], default=1,
        help="Download tier: 1=core (~110GB), 2=extended (+25GB), 3=full (+20GB)",
    )
    parser.add_argument(
        "--databases", nargs="*",
        help="Specific databases to download (overrides --tier)",
    )
    parser.add_argument(
        "--download-only", action="store_true",
        help="Download raw files only, skip parsing to Parquet",
    )
    parser.add_argument(
        "--no-checksum", action="store_true",
        help="Skip SHA256 checksum computation (faster)",
    )
    parser.add_argument(
        "--pubchem-max-assays", type=int, default=5000,
        help="Max PubChem assays to download (default: 5000, -1 for all)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be downloaded without downloading",
    )
    parser.add_argument(
        "--skip-auth", action="store_true",
        help="Skip databases that require authentication",
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
            name for name, cfg in DATABASE_REGISTRY.items()
            if cfg.tier <= args.tier
        ]

    # Filter out auth-required if --skip-auth
    if args.skip_auth:
        selected = [
            name for name in selected
            if not DATABASE_REGISTRY[name].requires_auth
        ]

    # ── Print header ──────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  SCX Drug Database Download Pipeline")
    print(f"  Tier: {args.tier}  |  Output: {output}")
    print(f"  Date:  {datetime.now().isoformat()}")
    print(f"{'='*70}")
    print(f"\n  Selected databases ({len(selected)}):")
    total_size = 0.0
    for name in selected:
        cfg = DATABASE_REGISTRY[name]
        auth_mark = " 🔒" if cfg.requires_auth else ""
        print(f"    [{cfg.tier}] {name:<25s} ~{cfg.size_gb:6.1f} GB  {cfg.category}{auth_mark}")
        total_size += cfg.size_gb
    print(f"\n  Estimated total download: ~{total_size:.1f} GB")
    print(f"  Estimated disk needed:   ~{total_size * 2.0:.1f} GB (with unpack buffer)")
    print(f"{'='*70}\n")

    if args.dry_run:
        print("[DRY RUN] No files downloaded. Use without --dry-run to execute.")
        sys.exit(0)

    # ── Download + Parse each database ─────────────────────────────────────
    t_start = time.perf_counter()
    results: Dict[str, Dict[str, Any]] = {}

    for i, db_name in enumerate(selected):
        cfg = DATABASE_REGISTRY[db_name]
        print(f"\n── [{i+1}/{len(selected)}] {db_name} ({cfg.full_name}) ──")
        print(f"    Tier: {cfg.tier}  |  Size: ~{cfg.size_gb:.1f} GB  |  Type: {cfg.category}")
        if cfg.requires_auth:
            print(f"    ⚠ Requires authentication: {cfg.license_info}")
        if cfg.note:
            print(f"    ℹ {cfg.note.split(chr(10))[0]}")

        result = {"name": db_name, "status": "not_started", "parsed_path": None}
        try:
            # Special handlers (combined download + parse)
            if db_name in SPECIAL_HANDLERS:
                handler = SPECIAL_HANDLERS[db_name]
                if db_name == "pubchem_bioassay":
                    parsed = handler(raw_dir, output, max_assays=args.pubchem_max_assays)
                else:
                    parsed = handler(raw_dir, output)
                result["status"] = "success" if parsed else "failed"
                result["parsed_path"] = parsed
            else:
                # Standard: download then parse
                dl_fn, parse_fn = DB_HANDLERS.get(db_name, (None, None))
                if dl_fn is None and parse_fn is None:
                    print(f"    ⚠ No handler registered for {db_name}")
                    result["status"] = "no_handler"
                    results[db_name] = result
                    continue

                # Download
                if dl_fn:
                    raw_path = dl_fn(raw_dir)
                else:
                    raw_path = raw_dir / cfg.filename

                if raw_path and raw_path.exists() and not args.download_only:
                    # Parse
                    if parse_fn:
                        parsed_path = parse_fn(raw_path, output)
                        result["status"] = "success" if parsed_path else "parse_failed"
                        result["parsed_path"] = parsed_path
                    else:
                        result["status"] = "downloaded_only"
                elif raw_path and raw_path.exists():
                    result["status"] = "downloaded_only"
                elif raw_path is None and args.skip_auth and cfg.requires_auth:
                    result["status"] = "skipped_auth"
                else:
                    result["status"] = "failed"
        except Exception as e:
            print(f"    ⚠ ERROR: {e}")
            result["status"] = "error"
            result["error"] = str(e)

        results[db_name] = result

    # ── Generate provenance summary ────────────────────────────────────────
    prov_summary_path = generate_provenance_summary(output)

    # ── Print final report ─────────────────────────────────────────────────
    t_elapsed = time.perf_counter() - t_start
    print(f"\n{'='*70}")
    print(f"  DOWNLOAD COMPLETE")
    print(f"  Runtime: {t_elapsed:.0f} s ({t_elapsed/60:.1f} min)")
    print(f"{'='*70}")
    print(f"\n  Results:")
    status_counts: Dict[str, int] = {}
    for name, r in results.items():
        s = r["status"]
        status_counts[s] = status_counts.get(s, 0) + 1
        icon = {"success": "✓", "downloaded_only": "⬇", "already_exists": "✓",
                "manual_required": "🔒", "failed": "✗", "error": "✗",
                "skipped_auth": "⏭", "no_handler": "?", "empty": "⚠",
                "not_started": "?"}.get(s, "?")
        path_str = str(r.get("parsed_path", "")).replace(str(output), "[output]")
        print(f"    {icon} {name:<25s} {s:<20s} {path_str}")

    print(f"\n  Status summary: {json.dumps(status_counts)}")
    print(f"\n  Provenance:     {prov_summary_path}")
    print(f"  Raw files:      {raw_dir}")
    print(f"  Parsed output:  {output}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
