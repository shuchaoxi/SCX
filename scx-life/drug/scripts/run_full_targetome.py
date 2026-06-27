#!/usr/bin/env python3
"""Run the full-scale human targetome pipeline.

Prerequisites
-------------
1. Download databases::

    python scripts/download_databases.py --output W:/scx_databases --tier 1

2. Prepare molecule and target CSV files::

    python scripts/prepare_inputs.py \
        --db-root W:/scx_databases \
        --output-dir inputs/

3. (Optional) Install GPU dependencies::

    pip install torch torch-geometric rdkit

4. Run this script::

    python scripts/run_full_targetome.py \
        --molecules inputs/all_compounds.csv \
        --targets inputs/all_human_targets.csv \
        --config configs/full_scale_targetome.yaml \
        --output W:/scx_runs/full_targetome_2026
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

from scx_drug import DrugPipeline, make_initial_state
from scx_drug.state import TargetProfileState


def main() -> None:
    parser = argparse.ArgumentParser(description="SCX Full Targetome Run")
    parser.add_argument("--molecules", type=Path, required=True)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--config", type=Path,
                        default=Path("configs/full_scale_targetome.yaml"))
    parser.add_argument("--output", type=Path,
                        default=Path("W:/scx_runs/full_targetome_2026"))
    parser.add_argument("--skip-docking", action="store_true",
                        help="Skip the slow docking layer")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate config only, do not run")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Build initial state ─────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("Building initial TargetProfileState ...")
    print(f"  Molecules : {args.molecules}")
    print(f"  Targets   : {args.targets}")

    t0 = time.perf_counter()
    state = make_initial_state(args.molecules, args.targets)
    n_mol = state.summary()["n_molecules"]
    n_tgt = state.summary()["n_targets"]
    n_pairs = state.summary()["n_pairs"]
    t1 = time.perf_counter()
    print(f"  {n_mol} molecules × {n_tgt} targets = {n_pairs:,} pairs")
    print(f"  Build time: {t1 - t0:.1f} s")

    # ── Load pipeline config ────────────────────────────────────────────
    print(f"\nLoading pipeline from: {args.config}")
    pipeline = DrugPipeline.from_yaml(args.config)

    if args.skip_docking:
        pipeline.steps = [
            s for s in pipeline.steps
            if s.step_type != "docking_verification"
        ]
        print("  (docking verification skipped)")

    print(f"  Steps: {len(pipeline.steps)}")
    for s in pipeline.steps:
        print(f"    {s.step_index:02d}. {s.step_type:30s}  {s.step_name}")

    if args.dry_run:
        print("\n[Dry run] Config validated.  Exiting.")
        sys.exit(0)

    # ── Run ─────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("Running pipeline ...\n")

    t_start = time.perf_counter()
    states = pipeline.run(state)
    t_end = time.perf_counter()

    elapsed = t_end - t_start
    print(f"\nPipeline complete in {elapsed/60:.1f} minutes ({elapsed:.0f} s)")

    # ── Write results ───────────────────────────────────────────────────
    print(f"\nWriting outputs to {output_dir} ...")
    final = states[-1]

    # Summary
    summary_path = pipeline.write_summary(states, output_dir)
    print(f"  Summary     : {summary_path}")

    # Per-molecule target profiles
    profiles = pipeline.write_target_profiles(final, output_dir)
    print(f"  Profiles    : {len(profiles)} files → {output_dir / 'target_profiles'}")

    # Final statistics
    stats = final.summary()
    stats["runtime_minutes"] = round(elapsed / 60, 1)
    stats_path = output_dir / "run_statistics.json"
    stats_path.write_text(json.dumps(stats, indent=2, default=str))
    print(f"  Stats       : {stats_path}")

    # ── Print key results ───────────────────────────────────────────────
    pairs = final.pairs
    kb = pairs["knowledge_hit"].sum()
    sim = pairs["similarity_hit"].sum()
    ml = (pairs["ml_score"] >= 0.5).sum()
    dock = (pairs["docking_score"] < -7.0).sum()

    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"  Knowledge-base hits   : {kb:>12,} ({kb/len(pairs)*100:.2f}%)")
    print(f"  Similarity inferred   : {sim:>12,} ({sim/len(pairs)*100:.2f}%)")
    print(f"  ML predicted (≥0.5)   : {ml:>12,} ({ml/len(pairs)*100:.2f}%)")
    print(f"  Docking verified      : {dock:>12,} ({dock/len(pairs)*100:.2f}%)")
    print(f"  ─────────────────────")
    total_any = int((pairs["evidence_level"] != "none").sum())
    print(f"  Any evidence          : {total_any:>12,}")
    print(f"  Total pairs           : {len(pairs):>12,}")
    print(f"\n  Per-molecule avg      : {total_any / max(n_mol, 1):.1f} targets")
    print(f"  Runtime               : {elapsed/60:.1f} minutes")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
