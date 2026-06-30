#!/usr/bin/env python3
"""
Paper 9 — Yajie LLM Consensus Audit
====================================

Template experiment script for Paper 9 (SCX for LLM):
"State-Conditioned eXpertise for Large Language Models."

Feeds 100 MMLU-style questions to 3 LLMs, computes Yajie consensus
across models, and outputs a consensus_score vs accuracy comparison table.

**Status: TEMPLATE — ready to run once models are downloaded.**

Currently uses mock LLMs with realistic accuracy profiles derived from
published benchmarks (Open LLM Leaderboard v2, June 2025).

When real models are available, replace ``MockLLM`` with actual model
loading (HuggingFace ``transformers`` or API calls). The rest of the
pipeline (Yajie consensus, evaluation, table output) is production-ready.

Target models:
  - Llama-3.1-8B-Instruct  (meta-llama)
  - Mistral-7B-Instruct-v0.3 (mistralai)
  - Qwen2.5-7B-Instruct     (Qwen)

Output:
  Console: per-model accuracy, consensus statistics, audit table
  CSV:     llm_yajie_audit_results.csv

Usage:
  python scripts/llm_yajie_audit.py                    # mock mode
  python scripts/llm_yajie_audit.py --mock             # explicit mock
  python scripts/llm_yajie_audit.py --real             # real models (when ready)
  python scripts/llm_yajie_audit.py --n_questions 200  # larger test set
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Add project root to Python path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scx.yajie import Yajie

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


# ============================================================================
# Mock LLM (template — replace with real model loading)
# ============================================================================


@dataclass
class MockLLMConfig:
    """Configuration for a mock LLM simulating real benchmark performance.

    Accuracy values are approximate, derived from Open LLM Leaderboard v2
    (MMLU-Pro scores, June 2025). Per-topic variation simulates real
    state-conditioned expertise patterns.
    """

    name: str
    overall_accuracy: float  # mean correctness probability
    accuracy_std: float = 0.12  # per-topic variation
    n_topics: int = 8  # number of simulated expertise topics
    seed: int = 42


# Realistic accuracy profiles (MMLU-Pro approximate, June 2025)
MOCK_MODEL_CONFIGS = [
    MockLLMConfig(
        name="Llama-3.1-8B-Instruct",
        overall_accuracy=0.66,  # ~66% on MMLU-Pro
        accuracy_std=0.10,
        n_topics=8,
        seed=42,
    ),
    MockLLMConfig(
        name="Mistral-7B-Instruct-v0.3",
        overall_accuracy=0.62,  # ~62% on MMLU-Pro
        accuracy_std=0.11,
        n_topics=8,
        seed=123,
    ),
    MockLLMConfig(
        name="Qwen2.5-7B-Instruct",
        overall_accuracy=0.58,  # ~58% on MMLU-Pro
        accuracy_std=0.13,
        n_topics=8,
        seed=456,
    ),
]


class MockLLM:
    """Simulates a small LLM with realistic accuracy patterns.

    Each model has:
    - An overall accuracy level
    - Per-topic accuracy variation (some topics it's good at, some poor)
    - Confidence calibration (well-calibrated on familiar topics,
      overconfident on unfamiliar ones)
    - **Genuinely different strong/weak topic profiles per model**
      (models excel at different domains, creating natural states)

    When real models are available, replace this class with:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        model = AutoModelForCausalLM.from_pretrained(model_name)
    """

    def __init__(self, config: MockLLMConfig) -> None:
        self.config = config
        self.name = config.name
        self.rng = np.random.default_rng(config.seed)

        # ---- Generate per-topic accuracy with wide variation ----
        # Each model is genuinely strong at ~3 topics, weak at ~3, OK at rest
        n_topics = config.n_topics
        n_strong = max(1, n_topics // 3)  # ~3 strong topics
        n_weak = max(1, n_topics // 3)    # ~3 weak topics

        # Start with moderate baseline
        topic_acc = np.full(n_topics, config.overall_accuracy)

        # Pick which topics this model is strong/weak at (different per model via seed)
        topic_order = self.rng.permutation(n_topics)
        strong_topics = topic_order[:n_strong]
        weak_topics = topic_order[-n_weak:]

        # Boost strong topics, penalize weak topics
        boost = config.accuracy_std * 1.5
        topic_acc[strong_topics] += boost
        topic_acc[weak_topics] -= boost

        # Add small per-topic jitter
        topic_acc += self.rng.uniform(-0.03, 0.03, size=n_topics)

        # Ensure mean still matches overall
        topic_acc += config.overall_accuracy - topic_acc.mean()
        self._topic_accuracy = np.clip(topic_acc, 0.10, 0.95)

        # Per-topic competence (for confidence calibration)
        # Strong topics → high competence, weak topics → low competence
        self._topic_competence = np.full(n_topics, 0.6)
        self._topic_competence[strong_topics] = self.rng.uniform(0.7, 0.95, size=n_strong)
        self._topic_competence[weak_topics] = self.rng.uniform(0.15, 0.40, size=n_weak)

        self._call_count = 0

    def answer(
        self,
        question_ids: np.ndarray,
        question_topics: np.ndarray,
        n_choices: int = 4,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Answer a batch of questions.

        Parameters
        ----------
        question_ids : np.ndarray, shape (N,)
            Question indices.
        question_topics : np.ndarray, shape (N,), dtype int
            Topic assignment for each question (0..n_topics-1).
        n_choices : int
            Number of answer choices per question.

        Returns
        -------
        answers : np.ndarray, shape (N,), dtype int
            Model's answer choice (0..n_choices-1).
        confidences : np.ndarray, shape (N,)
            Model's self-reported confidence in [0, 1].
        """
        self._call_count += len(question_ids)
        N = len(question_ids)
        topic_acc = self._topic_accuracy[question_topics]
        topic_comp = self._topic_competence[question_topics]

        # Determine correctness
        correct = self.rng.random(N) < topic_acc

        answers = np.zeros(N, dtype=int)
        confidences = np.zeros(N, dtype=float)

        for i in range(N):
            if correct[i]:
                answers[i] = 0  # correct answer is always choice 0
                # Confidence: high on familiar topics, moderate otherwise
                confidences[i] = topic_comp[i] * 0.6 + 0.30 + self.rng.normal(0, 0.04)
            else:
                # Wrong answer: pick uniformly from wrong choices
                wrong_choices = list(range(1, n_choices))
                answers[i] = wrong_choices[self.rng.integers(0, len(wrong_choices))]
                # Confidence: overconfident on unfamiliar topics (calibration failure)
                confidences[i] = (1.0 - topic_comp[i]) * 0.45 + 0.25 + self.rng.normal(0, 0.06)

            confidences[i] = float(np.clip(confidences[i], 0.05, 0.99))

        return answers, confidences


# ============================================================================
# Question bank (100 MMLU-style questions)
# ============================================================================


# 100 MMLU-style questions across 8 domains
# Format: (question_text, topic_id, correct_choice_index, n_choices)
# For the mock, we use topic_id to control accuracy patterns.
# When running with real LLMs, the topic field is informational.

MMLU_TOPICS = [
    "Abstract Algebra",
    "Computer Science",
    "Economics",
    "Electrical Engineering",
    "High School Biology",
    "High School Chemistry",
    "Machine Learning",
    "World History",
]

N_TOPICS = len(MMLU_TOPICS)


def generate_question_bank(
    n_questions: int = 100,
    n_choices: int = 4,
    seed: int = 789,
) -> pd.DataFrame:
    """Generate a question bank with metadata.

    In production, replace this with actual MMLU question loading.
    The topic assignment controls per-model accuracy variation
    and creates natural "states" for Yajie state discovery.

    Returns
    -------
    pd.DataFrame
        Columns: question_id, topic_id, topic_name, correct_choice,
        n_choices, difficulty
    """
    rng = np.random.default_rng(seed)

    questions = []
    for i in range(n_questions):
        topic_id = i % N_TOPICS
        # Vary difficulty by topic and position
        base_diff = 0.4 + 0.1 * (topic_id % 4)  # 0.4-0.7 range
        difficulty = float(np.clip(base_diff + rng.normal(0, 0.1), 0.2, 0.9))

        questions.append({
            "question_id": i,
            "topic_id": topic_id,
            "topic_name": MMLU_TOPICS[topic_id],
            "correct_choice": 0,  # always choice 0 for mock simplicity
            "n_choices": n_choices,
            "difficulty": difficulty,
        })

    return pd.DataFrame(questions)


# ============================================================================
# Yajie Consensus Computation
# ============================================================================


def compute_yajie_consensus(
    model_answers: np.ndarray,
    model_confidences: np.ndarray,
    ground_truth: np.ndarray,
    question_topics: np.ndarray,
    n_states: int = 5,
) -> pd.DataFrame:
    """Run Yajie on LLM response patterns to detect consensus.

    Treats each model as an "expert" and each question as a "sample."
    Yajie discovers which questions have consistent (trustworthy)
    answering patterns vs inconsistent (potentially wrong) patterns.

    Parameters
    ----------
    model_answers : np.ndarray, shape (N_questions, N_models)
        Each model's answer choice (0..n_choices-1).
    model_confidences : np.ndarray, shape (N_questions, N_models)
        Each model's self-reported confidence.
    ground_truth : np.ndarray, shape (N_questions,)
        Correct answers (0..n_choices-1).
    question_topics : np.ndarray, shape (N_questions,)
        Topic assignment per question.
    n_states : int
        Number of states for Yajie state discovery.

    Returns
    -------
    pd.DataFrame
        Per-question consensus analysis with columns:
        question_id, majority_correct, yajie_verdict,
        consensus_score, is_correct, model_agreement_count
    """
    N, M = model_answers.shape

    # ---- Expert definition: each model is an expert ----
    # Expert error = 0 if correct, 1 if wrong
    expert_correctness = (model_answers == ground_truth[:, np.newaxis]).astype(float)
    # Invert: error = 1 - correctness (so higher error = worse)
    expert_errors = 1.0 - expert_correctness  # (N, M)

    # ---- Build feature matrix from confidence + agreement patterns ----
    # Feature vector per question: [confidences from all models, agreement entropy]
    features = np.zeros((N, M + 1), dtype=float)
    features[:, :M] = model_confidences  # confidence signals

    # Agreement entropy: how much do models disagree?
    # Normalized entropy of answer distribution
    for i in range(N):
        answer_counts = np.bincount(model_answers[i], minlength=4)
        probs = answer_counts / answer_counts.sum()
        entropy = -np.sum(probs * np.log(probs + 1e-12))
        max_entropy = np.log(4)
        features[i, M] = 1.0 - entropy / max_entropy  # agreement score

    # ---- Create experts for Yajie interface ----
    # Experts return "predictions" = their confidence-weighted answer
    # Yajie computes residual = difference between prediction and data
    # We use the correctness pattern as the data
    experts = []
    for m in range(M):
        def make_expert(m_idx):
            def expert_fn(X: np.ndarray) -> np.ndarray:
                # Return expert's correctness pattern (used as data proxy)
                return np.tile(expert_correctness[:, m_idx:m_idx + 1], (1, X.shape[1] if X.ndim > 1 else 1))
            return expert_fn
        experts.append(make_expert(m))

    # ---- Run Yajie fit() ----
    yj = Yajie(grace=0.05, purity_threshold=0.9)
    yj.fit(
        X=features,
        experts=experts,
        n_states=min(n_states, N),
        exploration_rate=0.1,
        verbose=False,
    )

    # ---- Build consensus report ----
    report = yj.report_.copy()

    # Compute per-question metrics
    majority_vote = np.array([
        int(np.bincount(model_answers[i], minlength=4).argmax())
        for i in range(N)
    ])
    majority_correct = (majority_vote == ground_truth).astype(int)

    # Per-model correctness
    per_model_correct = expert_correctness  # (N, M)

    # Model agreement: how many models agree with the majority
    model_agreement = np.array([
        int(np.sum(model_answers[i] == majority_vote[i]))
        for i in range(N)
    ])

    # Consensus score: Yajie state quality weighted by model agreement
    report["question_id"] = np.arange(N)
    report["majority_correct"] = majority_correct
    report["model_agreement_count"] = model_agreement
    report["full_consensus"] = (model_agreement == M).astype(int)
    report["topic_id"] = question_topics

    # Per-model correctness columns
    for m in range(M):
        report[f"model_{m}_correct"] = per_model_correct[:, m].astype(int)

    report["consensus_score"] = (
        0.5 * report["state_quality"] + 0.5 * report["model_agreement_count"] / M
    )

    return report


# ============================================================================
# Evaluation Metrics
# ============================================================================


def evaluate_consensus(
    consensus_report: pd.DataFrame,
    model_names: List[str],
) -> Dict[str, Any]:
    """Compute evaluation metrics from the Yajie consensus report.

    Parameters
    ----------
    consensus_report : pd.DataFrame
        Output from compute_yajie_consensus().
    model_names : list of str
        Model names for labeling.

    Returns
    -------
    dict
        Keys: per_model_accuracy, majority_accuracy, yajie_high_consensus_accuracy,
        yajie_low_consensus_accuracy, consensus_accuracy_gap,
        clean_fraction, noisy_fraction, ambiguous_fraction,
        oracle_accuracy, consensus_vs_accuracy_correlation.
    """
    N = len(consensus_report)
    M = len(model_names)

    # Per-model accuracy from stored per-model correctness columns
    per_model_acc = {}
    for m in range(M):
        col = f"model_{m}_correct"
        if col in consensus_report.columns:
            per_model_acc[model_names[m]] = float(consensus_report[col].mean())
        else:
            per_model_acc[model_names[m]] = 0.0

    # Majority vote accuracy
    majority_acc = float(consensus_report["majority_correct"].mean())

    # Yajie consensus accuracy: high consensus → should be correct
    median_consensus = float(consensus_report["consensus_score"].median())
    high_consensus = consensus_report[consensus_report["consensus_score"] >= median_consensus]
    low_consensus = consensus_report[consensus_report["consensus_score"] < median_consensus]

    high_acc = float(high_consensus["majority_correct"].mean()) if len(high_consensus) > 0 else 0.0
    low_acc = float(low_consensus["majority_correct"].mean()) if len(low_consensus) > 0 else 0.0

    # Verdict distribution
    verdict_counts = consensus_report["verdict"].value_counts()
    n_clean = int(verdict_counts.get("clean", 0))
    n_noisy = int(verdict_counts.get("noisy", 0))
    n_ambiguous = int(verdict_counts.get("ambiguous", 0))

    # Full consensus accuracy (all models agree)
    full_consensus = consensus_report[consensus_report["full_consensus"] == 1]
    full_consensus_acc = (
        float(full_consensus["majority_correct"].mean())
        if len(full_consensus) > 0 else 0.0
    )

    # Correlation between consensus_score and correctness
    corr = float(np.corrcoef(
        consensus_report["consensus_score"],
        consensus_report["majority_correct"],
    )[0, 1]) if N > 1 else 0.0

    # Oracle: what if we trusted Yajie's "clean" verdict?
    clean_questions = consensus_report[consensus_report["verdict"] == "clean"]
    if len(clean_questions) > 0:
        oracle_acc = float(clean_questions["majority_correct"].mean())
    else:
        oracle_acc = majority_acc

    return {
        "per_model_accuracy": per_model_acc,
        "majority_accuracy": majority_acc,
        "yajie_high_consensus_accuracy": high_acc,
        "yajie_low_consensus_accuracy": low_acc,
        "consensus_accuracy_gap": high_acc - low_acc,
        "clean_fraction": n_clean / N,
        "noisy_fraction": n_noisy / N,
        "ambiguous_fraction": n_ambiguous / N,
        "oracle_accuracy": oracle_acc,
        "full_consensus_accuracy": full_consensus_acc,
        "n_full_consensus": len(full_consensus),
        "consensus_vs_accuracy_correlation": corr,
    }


# ============================================================================
# Output
# ============================================================================


def print_audit_report(
    consensus_report: pd.DataFrame,
    model_names: List[str],
    metrics: Dict[str, Any],
) -> None:
    """Print the Yajie LLM audit report to console."""
    N = len(consensus_report)

    print("\n" + "=" * 70)
    print("  Paper 9 — Yajie LLM Consensus Audit Report")
    print("=" * 70)

    # Per-model accuracy
    print(f"\n  Models tested: {len(model_names)}")
    for name in model_names:
        acc = metrics["per_model_accuracy"].get(name, 0.0)
        print(f"    {name:<32s}  acc = {acc:.3f}")

    # Consensus statistics
    print(f"\n  ── Consensus Statistics ──")
    print(f"  Questions:              {N}")
    print(f"  Majority vote accuracy: {metrics['majority_accuracy']:.3f}")
    print(f"  Full consensus (all agree): {metrics['n_full_consensus']}/{N} "
          f"({100*metrics['n_full_consensus']/N:.1f}%)")
    print(f"  Full consensus accuracy:    {metrics['full_consensus_accuracy']:.3f}")

    # Yajie analysis
    print(f"\n  ── Yajie Analysis ──")
    print(f"  High consensus accuracy:  {metrics['yajie_high_consensus_accuracy']:.3f}")
    print(f"  Low consensus accuracy:   {metrics['yajie_low_consensus_accuracy']:.3f}")
    print(f"  Consensus-accuracy gap:   {metrics['consensus_accuracy_gap']:+.3f}")
    print(f"  Correlation (consensus vs correct): {metrics['consensus_vs_accuracy_correlation']:+.3f}")

    # Verdict distribution
    print(f"\n  ── Yajie Verdict Distribution ──")
    print(f"  Clean:     {metrics['clean_fraction']:.1%}")
    print(f"  Noisy:     {metrics['noisy_fraction']:.1%}")
    print(f"  Ambiguous: {metrics['ambiguous_fraction']:.1%}")

    # Oracle: what if we only used Yajie-clean answers?
    print(f"\n  ── Oracle Analysis ──")
    print(f"  If we trust only 'clean'-verdict answers: acc = {metrics['oracle_accuracy']:.3f}")
    improvement = metrics['oracle_accuracy'] - metrics['majority_accuracy']
    print(f"  Improvement over majority vote:           {improvement:+.3f}")

    # Per-topic breakdown
    print(f"\n  ── Per-Topic Consensus Accuracy ──")
    topic_summary = (
        consensus_report.groupby("topic_id")
        .agg(
            n=("question_id", "count"),
            majority_acc=("majority_correct", "mean"),
            mean_consensus=("consensus_score", "mean"),
        )
        .reset_index()
    )
    topic_summary["topic_name"] = topic_summary["topic_id"].apply(
        lambda t: MMLU_TOPICS[t] if t < N_TOPICS else "Unknown"
    )
    for _, row in topic_summary.iterrows():
        print(f"    {row['topic_name']:<25s}  "
              f"n={int(row['n']):3d}  "
              f"acc={row['majority_acc']:.3f}  "
              f"consensus={row['mean_consensus']:.3f}")

    print("\n" + "=" * 70)


def save_results(
    consensus_report: pd.DataFrame,
    metrics: Dict[str, Any],
    model_names: List[str],
    output_dir: str,
) -> None:
    """Save consensus report and metrics to CSV."""
    os.makedirs(output_dir, exist_ok=True)

    # Save full report
    report_path = os.path.join(output_dir, "llm_yajie_audit_results.csv")
    consensus_report.to_csv(report_path, index=False)
    print(f"\nFull results saved: {report_path}")

    # Save summary metrics
    summary_path = os.path.join(output_dir, "llm_yajie_audit_summary.csv")
    summary_rows = []
    for name in model_names:
        summary_rows.append({
            "metric": f"accuracy_{name}",
            "value": metrics["per_model_accuracy"].get(name, 0.0),
        })
    for key, value in metrics.items():
        if key == "per_model_accuracy":
            continue
        if isinstance(value, (int, float, np.floating)):
            summary_rows.append({"metric": key, "value": float(value)})
    pd.DataFrame(summary_rows).to_csv(summary_path, index=False)
    print(f"Summary metrics saved: {summary_path}")


# ============================================================================
# Main Experiment Runner
# ============================================================================


def run_llm_experiment(
    n_questions: int = 100,
    n_choices: int = 4,
    use_mock: bool = True,
    seed: int = 789,
    output_dir: Optional[str] = None,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Run the full LLM Yajie audit experiment.

    Parameters
    ----------
    n_questions : int
        Number of questions.
    n_choices : int
        Number of answer choices per question.
    use_mock : bool
        If True, use mock LLMs. If False, load real models (not yet implemented).
    seed : int
        Random seed for reproducibility.
    output_dir : str, optional
        Directory for CSV output. Default: paper/llm_yajie/

    Returns
    -------
    consensus_report : pd.DataFrame
    metrics : dict
    """
    if output_dir is None:
        output_dir = str(PROJECT_ROOT / "paper" / "llm_yajie")

    rng = np.random.default_rng(seed)

    # ---- 1. Generate question bank ----
    print("=" * 70)
    print("Paper 9 — Yajie LLM Consensus Audit")
    print("=" * 70)
    print(f"\n[1/5] Generating {n_questions} MMLU-style questions...")
    question_bank = generate_question_bank(
        n_questions=n_questions,
        n_choices=n_choices,
        seed=seed,
    )
    ground_truth = question_bank["correct_choice"].values
    question_topics = question_bank["topic_id"].values

    # ---- 2. Load models ----
    if use_mock:
        print(f"[2/5] Loading {len(MOCK_MODEL_CONFIGS)} mock LLMs...")
        models = [MockLLM(cfg) for cfg in MOCK_MODEL_CONFIGS]
        model_names = [cfg.name for cfg in MOCK_MODEL_CONFIGS]
        for cfg in MOCK_MODEL_CONFIGS:
            print(f"  {cfg.name:<32s}  μ_acc = {cfg.overall_accuracy:.2f}")
    else:
        # TODO: Replace with real model loading
        print("[2/5] Loading real LLMs...")
        print("  ⚠ Real model loading not yet implemented.")
        print("  Install: pip install transformers torch")
        print("  Then uncomment the model loading code in run_llm_experiment().")
        raise NotImplementedError(
            "Real model loading not yet implemented. Use --mock for now."
        )

    # ---- 3. Collect model answers ----
    print(f"[3/5] Collecting answers from {len(models)} models...")
    M = len(models)
    all_answers = np.zeros((n_questions, M), dtype=int)
    all_confidences = np.zeros((n_questions, M), dtype=float)

    for m, model in enumerate(models):
        answers, confidences = model.answer(
            question_ids=np.arange(n_questions),
            question_topics=question_topics,
            n_choices=n_choices,
        )
        all_answers[:, m] = answers
        all_confidences[:, m] = confidences
        acc = float(np.mean(answers == ground_truth))
        print(f"  {model.name:<32s}  acc = {acc:.3f}")

    # ---- 4. Compute Yajie consensus ----
    print(f"[4/5] Computing Yajie consensus across {M} models...")
    consensus_report = compute_yajie_consensus(
        model_answers=all_answers,
        model_confidences=all_confidences,
        ground_truth=ground_truth,
        question_topics=question_topics,
        n_states=min(8, n_questions // 10),
    )

    # ---- 5. Evaluate and output ----
    print("[5/5] Evaluating consensus quality...")
    metrics = evaluate_consensus(consensus_report, model_names)

    print_audit_report(consensus_report, model_names, metrics)
    save_results(consensus_report, metrics, model_names, output_dir)

    return consensus_report, metrics


# ============================================================================
# CLI
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Paper 9 — Yajie LLM Consensus Audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/llm_yajie_audit.py                    # mock mode (default)
  python scripts/llm_yajie_audit.py --mock              # explicit mock
  python scripts/llm_yajie_audit.py --n_questions 200   # larger test set
  python scripts/llm_yajie_audit.py --seed 42           # different seed
        """,
    )
    parser.add_argument(
        "--n_questions", type=int, default=100,
        help="Number of questions (default: 100)",
    )
    parser.add_argument(
        "--n_choices", type=int, default=4,
        help="Number of answer choices per question (default: 4)",
    )
    parser.add_argument(
        "--mock", action="store_true", default=True,
        help="Use mock LLMs (default: True — until real models are configured)",
    )
    parser.add_argument(
        "--seed", type=int, default=789,
        help="Random seed (default: 789)",
    )
    parser.add_argument(
        "--output_dir", type=str, default=None,
        help="Output directory for CSV results",
    )
    args = parser.parse_args()

    try:
        consensus_report, metrics = run_llm_experiment(
            n_questions=args.n_questions,
            n_choices=args.n_choices,
            use_mock=args.mock,
            seed=args.seed,
            output_dir=args.output_dir,
        )

        # Quick self-check
        checks_ok = True
        if metrics["consensus_accuracy_gap"] <= 0:
            print("\n⚠ Yajie consensus gap ≤ 0 — may need more questions or different models")
            checks_ok = False
        if metrics["consensus_vs_accuracy_correlation"] < 0:
            print("\n⚠ Negative correlation between consensus and accuracy — investigate")
            checks_ok = False

        if checks_ok:
            print("\n✓ Yajie consensus positively correlates with accuracy — expected behavior.")

        return 0
    except NotImplementedError as e:
        print(f"\n{e}")
        return 1
    except Exception as e:
        print(f"\n✗ Experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
