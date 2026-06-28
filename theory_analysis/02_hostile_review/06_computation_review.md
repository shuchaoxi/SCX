# Hostile Review: SCX Framework — Practical Feasibility Assessment

**Reviewer role**: Computational Scientist (hostile)  
**Target**: SCX (State-Conditioned eXpertise) framework, v0.4.0-pre  
**Date**: 2026-06-28

---

## Executive Summary

SCX presents an elegant theoretical architecture (6 theorems, 427 tests, ~18,000 lines of Python), but the chasm between theory and practice is vast. The core orchestration class (`SCXFramework.fit()`) raises `NotImplementedError`. The "memory bank" does not exist in code. The V(s) gatekeeper formula is `DEPRECATED`. Real-world experiments beyond CIFAR-10/SimpleCNN are absent or blocked by "GPU 不可用." The codebase is a collection of well-tested individual components that have never been connected into a running pipeline. This review substantiates each claim with direct code evidence.

---

## 1. M >= 10 Expert Feasibility

### Claim
Theorem 1 guarantees F1 >= 1 - O(exp(-2M*Delta^2)) as a function of M experts. The framework claims to support "multi-expert" systems, and the paper narrative targets scenarios with M >= 10 (e.g., 10 ACE/MACE potentials in the MLIP setting, Paper IV).

### Code Evidence

**Default configuration caps M at 3:**
In `/g/Xiaogan_Supercomputing_data/SCX/src/scx/core/config.py`, line 66:
```python
n_experts: int = 3
```

**No hard upper bound, but no support for large M either:**
The config validator (line 110-111) only enforces `n_experts >= 1`. There is no validation for memory constraints, no distributed execution path, no batch-parallel expert evaluation.

**ExpertRegistry.predict_all() is O(M * N * d) with no parallelism:**
```python
# scx/expert/registry.py, line 136-158
def predict_all(self, X: np.ndarray) -> np.ndarray:
    preds = [
        info.predict_fn(X)[np.newaxis, ...]
        for info in self._experts.values()
    ]
    return np.concatenate(preds, axis=0)
```
This sequentially evaluates every expert on every sample. For M=10 and N=10^6 (ImageNet scale), this means 10^7 forward passes through potentially deep neural networks, with no GPU batching across experts.

**ExpertReliability._estimate_supervised() is O(M * K * N_s):**
```python
# scx/expert/reliability.py, line 170-183
for k in range(n_states):
    for m in range(M):
        loss_k = losses[m, mask]
        R_matrix[m, k] = float(np.mean(loss_k))
```
This double loop over states and experts is O(M * K). With M=10, K=100, this is 1000 iterations — fine. But the much larger cost is the loss computation: each expert produces predictions for all N samples first.

**The synthetic experiment uses only M=3:**
In `/g/Xiaogan_Supercomputing_data/SCX/experiments/synthetic/run_experiment.py`, line 474:
```python
cfg = {"n_experts": 3, ...}
```
No experiment tests M > 3.

### Analysis

For ImageNet-scale (1.2M images, 224x224), training 10 independent deep networks is a capital-intensive proposition:
- ResNet-50 training on ImageNet: ~150 GPU-hours per model (single-GPU equivalent)
- 10 models: ~1,500 GPU-hours at minimum
- This ignores the cost of maintaining 10 separate training loops, hyperparameter sweeps, and architecture choices

For the MLIP scenario (Paper IV), training 10 independent ACE/MACE potentials:
- A single MACE-MP-0 training on a medium dataset (~10^5 configurations) takes ~50 GPU-hours on an A100
- 10 such models: ~500 GPU-hours minimum
- The ACE potentials are cheaper (CPU-only), but still O(10) independent fits on O(10^5) structures requires substantial orchestration

**But more damning**: The current code cannot even orchestrate this. `SCXFramework.fit()` (framework.py, line 118) raises `NotImplementedError`:
```python
raise NotImplementedError(
    "fit() requires scx.state.discovery.StateDiscovery — "
    "not yet implemented."
)
```
The entire framework pipeline — the thing that would manage M experts at scale — is a stub.

### Verdict
**FAIL.** The theoretical convergence rate assumes M > 1 experts with conditionally independent errors (Assumption A1: disjoint training sets). But (1) the code never tests M > 3, (2) the orchestration pipeline for M=10 is `NotImplementedError`, (3) there is no distributed or batched expert evaluation, and (4) the computational cost of training 10 ImageNet-scale models is brushed under the rug. The paper's MLIP claims rest on training 10 ACE/MACE potentials — a ~500 GPU-hour undertaking — with zero evidence that such an experiment has been conducted or even planned.

---

## 2. Memory Bank — Infinite Growth

### Claim
SCX claims to maintain a "memory bank" (记忆库) recording all state interactions, enabling retrospective analysis and state-conditioned routing.

### Code Evidence

**There is NO memory bank data structure in the codebase.**  
A grep for "memory_bank", "memory", "bank", "buffer", "replay" across all source files returns nothing relevant.

**The closest existing structure is OnlineSCXFramework.history:**
```python
# scx/core/online.py, line 229
self.history: list[dict] = []
```
This list grows without bound:
```python
# line 298-306
record = {
    "state": s,
    "expert": expert_id,
    "loss": float(loss),
    "classification": classification,
    ...
}
self.history.append(record)
```

**OnlineExpertTracker uses fixed-size matrices, not a growing bank:**
```python
# scx/core/online.py, line 139-144
self.R_ema = np.zeros((M, K), dtype=float)
self.SCX_ema = np.ones((M, K), dtype=float)
self.N_ms = np.zeros((M, K), dtype=float)
```
This is an O(M*K) summary, not a per-sample memory bank. The per-sample data is lost.

**The history is used only for summary reporting:**
```python
# line 346-365
def get_data_classification(self) -> dict[str, int]:
    counts: dict[str, int] = {...}
    for record in self.history:
        cat = record["classification"]
        counts[cat] = counts.get(cat, 0) + 1
    return counts
```
It iterates the entire history list every time. There is no indexing, no summarization, no retrieval.

### Analysis

The gap between the paper's "memory bank" narrative and the code is striking:

1. **No vector index**: For N=10^7 samples, there is no FAISS, no Annoy, no HNSW, no KD-tree — nothing for nearest-neighbor retrieval. The only "assignment" is nearest-centroid via `cdist` (O(K*d) per sample).

2. **No persistent storage**: No SQLite, no HDF5, no LMDB. The entire "memory" is a Python list that lives in RAM.

3. **O(N) scan for classification**: Every call to `get_data_classification()` does a full O(N) scan of the history list.

4. **The theory assumes per-sample storage**: Theorem 1's per-sample consistency score C(x) requires per-sample expert error indicators `e_m(x,y)`. But the code stores only running EMA summaries per (expert, state) pair. The per-sample data needed to recompute C(x) at query time is discarded.

At N=10^7:
- Storing just (sample_id, expert_id, loss, state) as Python dictionaries: ~200 bytes/sample = 2 GB, manageable
- But retrieval: the only lookup mechanism is `cdist` (pairwise distances) — O(N*d) per query
- Any nearest-neighbor index would require rebuilding after state updates (EMA centroid changes)

### Verdict
**FAIL.** The "memory bank" is a rhetorical device, not an implemented data structure. The code uses running EMA summaries (O(M*K)) that discard per-sample information. There is no efficient nearest-neighbor index. At N=10^7, the `cdist`-based "retrieval" would take hours per query. The paper's claims about retrospective per-sample analysis are not supported by the implementation.

---

## 3. Gatekeeper V(s) Scoring Bottleneck

### Claim
V(s) = r-bar(s) * rho(s) * L(s) * [1 - D(s)] is the core gatekeeper equation that drives acquisition decisions, computed in real-time for each state.

### Code Evidence

**V(s) is DEPRECATED:**
```python
# scx/valuation/state_value.py, line 140-142
def acquisition_value(self, ...):
    """Acquisition value V_add(s).
    
    .. deprecated::
        Use :meth:`noise_detection_f1_bound` or
        :meth:`feature_strength_diagnostic` instead.
    """
    warnings.warn("...deprecated...", DeprecationWarning, stacklevel=2)
```

**The replacement is theorem-based, but still O(K) per acquisition:**
The new methods in StateValue (noise_detection_f1_bound, feature_strength_diagnostic, etc.) all operate on per-state arrays of shape (K,). Every acquisition decision iterates over all K states.

**K_S is hard-coded, not adaptive:**
```python
# scx/core/config.py, line 62
n_states: int = 10
```
The only adaptation mechanism is `StateMetrics.suggest_n_states()` (state/metrics.py, line 149-199), but this is a separate standalone function not integrated into the pipeline. The pipeline does not re-evaluate or adjust K automatically.

**State discovery must be re-run from scratch to change K:**
```python
# scx/state/discovery.py, line 100-190
def fit(self, X_phi: np.ndarray) -> StateDiscovery:
    if self.method == "kmeans":
        model = KMeans(n_clusters=K, n_init=n_init, ...)
        labels = model.fit_predict(X_phi)
    # ... HDBSCAN is the only method that can discover K automatically
```

### Analysis

The core acquisition loop, if it were implemented (it isn't), would look like:
```
for epoch in range(T):
    for state s in S:              # O(K) per epoch
        compute V(s)                # O(1) per state (deprecated) or O(d) for MI
    select s* = argmax V(s)         # O(K) sort
    for sample in acquisition_batch:
        query experts M times        # O(M * inference_cost)
        update reliability           # O(1) EMA update
```

For each acquisition step:
- **V(s) computation**: O(K) when using the deprecated formula, O(K*d) for feature_strength_diagnostic (requires mutual information estimation per state)
- **argmax**: O(K log K) sort
- **Total per-acquisition**: O(K * (1 + d) + M)

When K grows to 1000+ (which is what the state discovery methods like HDBSCAN can produce):
- 1000 V(s) computations per acquisition
- 1000 sorts per epoch
- The mutual information estimation (`feature_strength_diagnostic`) calls `sklearn.feature_selection.mutual_info_classif` which is O(N * d) — done over ALL samples, not per state

**The deprecated V(s) formula avoids the O(N*d) cost, but its components have their own costs:**
- `RedundancyScore.state_similarity()` computes full O(N_s^2) pairwise cosine similarities
- `RedundancyScore.boundary_score()` computes O(N_s * K) distances to all centroids
- These are computed once during initialization, not per-acquisition, so the per-acquisition cost is lower

### Verdict
**MODERATE FAIL.** The V(s) formula is already deprecated, so the bottleneck analysis partly targets a moving target. However, the replacement theorem-based methods are not cheaper. For K=1000, each acquisition decision requires iterating over all 1000 states. State discovery (the most expensive operation — O(N*K*d)) must be re-run from scratch to change K; there is no incremental state splitting or merging. The adaptive K mechanism (`suggest_n_states`) exists as a standalone function but is not wired into the pipeline.

---

## 4. Baseline Comparison Gaps

### Claim
SCX experiments demonstrate superiority over alternative approaches.

### Code Evidence

**Synthetic experiment baselines (run_experiment.py, lines 252-317):**
- Random sampling (random)
- Uncertainty sampling (expert prediction variance)
- Diversity sampling (farthest-point / k-center)
- High-error sampling (largest residuals)

**CIFAR-10 noise experiment baselines (run_cifar10_noise.py):**
- Confidence-based (softmax probability threshold)
- Loss-based (cross-entropy loss threshold)
- SCX-Noise (proposed)

**Missing baselines — every single one:**

1. **Query-by-Committee (QBC)**: The most direct competitor to SCX's multi-expert consensus approach. QBC measures disagreement among an ensemble and queries the most disagreed-upon samples. SCX uses expert agreement divergence for noise detection. Without QBC, there is no way to tell whether SCX's state-conditioned approach adds value over simple ensemble disagreement.

2. **Full training (100% data)**: The baseline experiments never compare SCX-selected subsets against the full dataset. Without this, the reader cannot assess how much data SCX "wastes" by discarding samples as noisy or redundant.

3. **Simple max-loss sampling**: While `highloss_sample` is implemented in `experiments/cifar/run_baselines.py`, it is never compared in the noise detection experiments. The CIFAR noise experiment only compares against confidence and loss — which are the weakest baselines.

4. **No random baseline in noise detection**: The CIFAR-10 noise experiment (`run_cifar10_noise.py`) has no random-noise-detection baseline. Random guessing at `eta=0.1` noise rate would achieve F1 ~ 0.18, but this reference point is never computed.

**Comparison metric is coverage, not F1, in the synthetic experiment:**
```python
# synthetic/run_experiment.py, lines 524-536
baselines = {
    "Random": {"indices": rand_idx, "score": coverage_metric(X, rand_idx)},
    "Uncertainty": {"indices": unc_idx, "score": coverage_metric(X, unc_idx)},
    ...
}
```
The SCX method is evaluated on coverage, not on the metrics the paper claims to optimize (noise detection F1, data value, expert routing accuracy).

**SCX's own metric is hand-picked:**
```python
# line 533
best_state = value_df.loc[value_df["V_add"].idxmax(), "state_id"]
scx_mask = scx_result["state_labels"] == best_state
scx_idx = np.where(scx_mask)[0][:budget]
scx_score = coverage_metric(X, scx_idx) if len(scx_idx) > 0 else 0.0
```
This selects ALL samples from the single "best" state — a strategy that no active learning paper would use. It is trivially beaten by diversity sampling.

### Analysis

The baseline comparisons are systematically biased in SCX's favor:

1. **Strawman baselines**: In the CIFAR noise experiment, confidence-thresholding (flag bottom 10% confidence) and loss-thresholding (flag top 10% loss) are the weakest possible baselines. They are single-threshold heuristics that any competent reviewer would reject. The absence of QBC — the standard approach in multi-expert noisy-label detection — is indefensible.

2. **No ablation study**: The experiments never ask: "Does state conditioning help beyond simple ensemble agreement?" Without ablating the state-conditioning mechanism and comparing against unstructured ensemble disagreement, there is no evidence that state discovery (the central innovation) adds value.

3. **Coverage is the wrong metric**: The synthetic experiment claims to evaluate "acquisition" but measures coverage (mean nearest-neighbor distance). Coverage favors diversity sampling by construction. The noise detection experiments measure F1, but only against two weak baselines.

4. **SCX's own method is implemented incorrectly**: The SCX acquisition strategy in the synthetic experiment (selecting ALL samples from the single highest-V_add state) is not how active learning works. Any reasonable baseline would sample proportionally across states or at least diversify within-state selection.

### Verdict
**FAIL.** The experimental evaluation is missing the most critical baselines (Query-by-Committee, full training, random noise detection, max-loss). The synthetic experiment evaluates on coverage (favoring diversity methods) rather than on any metric that SCX claims to optimize. The noise detection experiment compares against only two weak heuristics. Without QBC, there is zero evidence that SCX's state-conditioned approach outperforms simple unstructured ensemble disagreement — which is the entire point of the framework.

---

## 5. Evidence for "Changing Practice"

### Claim
SCX claims to "change the practice of data curation" (改变数据策展的实践), targeting Nature Computational Science. The paper series spans materials science (MLIP), medical imaging, and drug discovery.

### Code Evidence

**Synthetic 2D data is the only completed end-to-end experiment:**
The synthetic experiment (`experiments/synthetic/run_experiment.py`) runs on 500 points, 2D, 4 states, 3 experts. It does produce a full output.

**CIFAR-10 noise experiment uses SimpleCNN on synthetic noise only:**
```python
# experiments/cifar/run_cifar10_noise.py
model_fn = lambda: SimpleCNN(num_classes=num_classes) if use_simple_cnn else get_resnet18(num_classes=num_classes)
```
The experiment only injects synthetic symmetric label noise. It does not test on real-world noisy datasets like Clothing1M, WebVision, CIFAR-100N, or Red Mini-ImageNet. The default uses SimpleCNN (a lightweight model, ~1M parameters), not ResNet.

**Medical imaging (scx-health): experiments exist but no results are reported:**
The `scx-health/experiments/` directory has `run_noise.py`, `run_routing.py`, `run_compress.py`. Reading these files reveals they are experiment *skeletons* — they set up data loading and model definitions but produce no quantitative results. The experiment outputs directory does not contain medical imaging results.

**MLIP case runs but has critical limitations:**
```python
# experiments/mlip_case/run_scx_on_aln_v3.py
encoder = MLIPEncoder()
features = np.stack([encoder.encode(f) for f in frames])
discovery = StateDiscovery(method='kmeans', n_states=20)
labels = discovery.fit_predict(features)
```
This uses the average force magnitude per frame as a residual proxy (`fmax = np.linalg.norm(f.get_forces(), axis=1).max()`). This is a proxy for expert error, not actual multi-expert prediction. There is a single set of DFT forces — there are no MACE/ACE experts being evaluated. The "experts" are entirely absent from this experiment.

**Paper III (MLIP) and Paper V (Health) are blocked:**
From `DEVELOPMENT_LOG.md`:
> "当前阻塞: GPU 不可用"

The `DEVELOPMENT_LOG.md` explicitly states the entire project was developed on a personal computer. The synthetic data experiments are the only ones that can fully run.

### Analysis

The gap between the paper's claims and the experimental reality:

| Claimed Domain | Status | Evidence |
|---|---|---|
| General ML theory | Mathematical theorems only | 3 theorems + 6 propositions, no empirical validation on real data |
| CIFAR-10 noise detection | Partial | SimpleCNN, synthetic label noise only, no real-world noisy datasets |
| MLIP (Paper IV) | Stub | Single-force-field analysis with no multiple experts; uses force magnitude as residual proxy |
| Medical imaging (Paper V) | Empty | Experiment skeletons only; no results |
| Drug discovery | Empty | `drug-module/` contains only data-loading scripts and config files |
| Changing practice of data curation | No evidence | The only completed experiment is on synthetic 2D data with 500 samples |

The Nature Computational Science submission is particularly problematic. The journal requires:
- Demonstrated computational methods that advance scientific practice
- Validation on real-world scientific data
- Reproducible code and results

SCX has none of these. The only experiment that produces quantitative results is on synthetic 2D data. No real-world noisy dataset evaluation exists. The MLIP "experiment" uses a single force field (not multiple experts) and a hand-crafted residual proxy. The medical and drug modules are empty.

### Verdict
**FAIL.** The claim of "changing data curation practice" is not supported by the experimental record. The only complete experiment is on 500 synthetic 2D points. The MLIP experiment uses no multiple experts. The medical and drug modules are empty. The CIFAR-10 experiment uses a toy model and synthetic noise, not real-world label noise. The project has zero experiments on real-world noisy datasets (Clothing1M, WebVision, CIFAR-100N). A Nature Computational Science paper without real-world computational science experiments is not publishable.

---

## 6. Code Quality and Reproducibility

### Claim
SCX v0.4.0-pre has 427 tests, all passing. The codebase is well-documented and production-quality.

### Code Evidence

#### 6.1 Numeric Stability

**Most functions have epsilon guards:** `eps=1e-8` is the standard pattern across `StateValue`, `NoiseScore`, `LearnabilityScore`, `RedundancyScore`. This is good.

**_safe_kl handles edge cases:**
```python
# scx/valuation/state_value.py, line 1113-1124
def _safe_kl(p: float, q: float) -> float:
    eps = 1e-15
    p = np.clip(p, eps, 1.0 - eps)
    q = np.clip(q, eps, 1.0 - eps)
    if abs(p - q) < eps:
        return 0.0
    return float(p * np.log(p / q) + (1.0 - p) * np.log((1.0 - p) / (1.0 - q)))
```

**But several functions have no such guards:**
- `ExpertReliability._softmax_dist` (actually in discovery.py, line 43): Uses `np.exp(logits - logits.max(...))` — standard and safe.
- But `ExpertConflict.conflict_score` (conflict.py, line 217): `score = float(np.tanh(avg_diff))` — tanh is fine, but `avg_diff` can be NaN if all predictions are identical and the code dividing `predictions.reshape(M, -1)` produces identical rows.
- `StateAssignment.soft_assign_gmm` (assignment.py, line 121-131): Manually sets GMM internals including `precisions_cholesky_` via `np.linalg.cholesky(np.linalg.inv(covariances))`. If covariances are singular (e.g., all samples in a state are identical), `np.linalg.inv` will fail with `LinAlgError`. There is no try/except.
- `LossFunction._mse_loss` (reliability.py, line 25-28): `np.mean(diff ** 2, axis=...)` — fine, but the mean over a flattened dimension can hide per-sample numerical issues.

#### 6.2 Test Coverage

**427 tests is impressive for volume, but superficial for depth:**

| Module | Tests | What's Tested | What's NOT Tested |
|--------|-------|---------------|-------------------|
| Expert | ~70 | Registry CRUD, reliability shapes, router shapes | ExpertReliability.update() is NotImplemented — the test just checks it raises |
| State | ~60 | Discovery.fit shapes, StateSpace CRUD | No tests with real high-dimensional data; no tests for convergence |
| Valuation | ~120 | All scoring functions, StateValue theorem methods | feature_strength_diagnostic tested only on random data; adaptive threshold tested with dummy data |
| Action | ~40 | Policy budget allocation, acquisition, compress | No end-to-end acquisition test; no test that compress actually improves model performance |
| Online | ~30 | OnlineStateTracker, OnlineExpertTracker shapes | No streaming data test; no drift detection test |
| Yajie | ~50 | (new module) | Not reviewed in detail |

**Critical untested components:**
- `SCXFramework.fit()` — not testable (NotImplementedError)
- `SCXFramework.predict_expert()` — not testable (NotImplementedError)
- `SCXFramework.compress()` — not testable (NotImplementedError)
- `SCXFramework.recommend_action()` — not testable (NotImplementedError)
- The entire pipeline integration — never tested
- ExpertReliability.update() — specifically raises NotImplementedError (line 494)
- Pre-trained model integration — no tests load real PyTorch models
- MLIP encoder — not tested (requires ase dependency)

**Test quality concerns:**
```python
# tests/test_valuation.py, line 25-29
def test_consistency_label_discrete_perfect(self):
    ls = LearnabilityScore()
    X = np.random.randn(10, 2)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    c = ls.consistency(X_s=X, y_s=y)
    assert 0.0 <= c <= 1.0  # <-- This ONLY checks the range, not correctness!
```
Many tests follow this pattern: they assert that values are in [0, 1] or that shapes match, but never check that the *right answer* is produced. The tests verify that the code doesn't crash, not that it's correct.

#### 6.3 Documentation Quality

**API documentation is thorough:** All public methods have NumPy-style docstrings with Parameters, Returns, Examples blocks. This is a genuine strength.

**BUT:**
- There are no usage examples calling the pipeline end-to-end
- The README's "quick start" section has code that will crash (SCXFramework.fit() raises NotImplementedError)
- There are no Jupyter notebooks demonstrating the framework
- The theory documentation (THEOREMS_UNIFIED.md) is well-structured but disconnected from the code — it references theorems and proofs that the code does not actually implement

### Verdict
**MODERATE FAIL.** Numerical stability is reasonable (epsilon guards present in most places), but there are critical gaps (`np.linalg.inv` without exception handling, `soft_assign_gmm` with manual cholesky). Test coverage is wide but shallow — most tests check "does it crash?" not "is the result correct?" The pipeline tests are impossible because `fit()` raises `NotImplementedError`. Documentation is good at the docstring level but fails at the system level — there is no end-to-end example that actually runs.

---

## 7. Computational Complexity Analysis

Let me provide a rigorous Big-O analysis of the SCX core loop as it would execute if the pipeline were implemented.

### 7.1 The Hypothetical Core Loop

The following is reconstructed from the documented pipeline steps (framework.py docstring) and the individual component costs:

```
Given:
  N = dataset size
  d = feature dimension
  K = number of states (default 10)
  M = number of experts (default 3)
  T = number of acquisition rounds
  B = acquisition batch size per round
  n_init = k-means initializations (default 20)

=== PHASE 1: INITIALIZATION (one-time) ===

Step 1: State Discovery (k-means on phi(X))
  Cost: O(N * K * d * n_init)
  - Each k-means iteration: O(N * K * d)
  - n_init runs (default 20)
  - Lloyd's algorithm: typically ~O(log N) iterations if well-behaved
  Total: O(N * K * d * n_init * log N)
  
  For N=10^5, d=512, K=10: ~10^10 operations — hours on CPU

Step 2: Expert Reliability (supervised)
  Cost: O(M * N * d_eval) for predictions + O(M * N) for loss evaluation
  - Each expert evaluates all N samples
  - Loss computation per (expert, sample) pair
  Total: O(M * N * d_eval)
  
  For M=10, N=10^5, d_eval dependent on model complexity

Step 3: Per-state metrics
  O(K * N_s^2) for pairwise similarity (redundancy module)
  O(K * N_s * d) for boundary scores
  Total: O(N^2 / K + N * d) — the similarity is O(N_s^2) per state

=== PHASE 2: ACTIVE LEARNING LOOP (T rounds) ===

For each round t in 1..T:
  For each state s in 1..K:
    Compute V(s):
      - Deprecated: O(1) per state (multiplicative formula)
      - New (Theorem 1 bound): O(K) for f1_bound (sum over states)
      - feature_strength_diagnostic: O(N * d) for mutual_info_classif
    Total: O(K + K) = O(K) per round, or O(N * d) with MI

  Select s* = argmax V(s): O(K log K)

  For b in 1..B:
    Query M experts on sample x_b: O(M * inference_cost)
    Update memory: O(1) EMA update per (expert, state) pair
    Total per-sample: O(M)
  
  Update experts (retrain on newly labeled data):
    O(M * training_cost) — depends on model and dataset size

Total per round: O(K + B * M + M * training_cost)
Total all rounds: O(T * (K + B * M + M * training_cost))

=== OVERALL TOTAL ===
O( N*K*d*n_init*log N  +  M*N*d_eval  +  N^2/K  +  T*(K + B*M + M*train) )
```

### 7.2 Comparison Against Baselines

| Method | Training Cost | Inference Cost | Per-Acquisition Cost |
|--------|--------------|----------------|---------------------|
| Random sampling | O(N * d) | — | O(1) |
| Max-loss sampling | O(N * d) | O(N * d) | O(N) sort |
| Uncertainty sampling | O(N * d) | O(N * d) | O(N) sort |
| Query-by-Committee | O(M * N * d) | O(M * N * d) | O(N * M) |
| **SCX (full)** | **O(N*K*d*log N + M*N*d + N^2/K)** | O(M * d) | **O(K + B*M)** |

SCX's initialization is substantially more expensive than any baseline:
- The k-means state discovery with n_init=20 adds O(N*K*d*log N) overhead that baselines avoid
- The O(N^2/K) pairwise similarity for redundancy scoring is prohibitive for N > 10^4
- State discovery must be re-run if K changes (no incremental version)

SCX's per-acquisition cost is lower (O(K) vs O(N) for max-loss/uncertainty), but this is only meaningful if the expensive initialization is amortized over many acquisition rounds. The experiments use T=1 (single round).

### 7.3 The O(N^2) Problem

The most severe scaling issue is `RedundancyScore.state_similarity()`:
```python
# scx/valuation/redundancy.py, line 79-80
sim = X_norm @ X_norm.T  # (N_s, N_s) — O(N_s^2)
triu_vals = sim[np.triu_indices(N_s, k=1)]  # extracts O(N_s^2) elements
```
This computes ALL pairwise cosine similarities. For a state with N_s = 10^4 samples, this is 10^8 floating-point operations and a 400 MB matrix. For N_s = 10^5, it is 10^10 operations and a 40 GB matrix.

| N (total) | K (states) | N_s (avg/state) | Similarity cost | RAM for matrix |
|-----------|-----------|-----------------|-----------------|----------------|
| 10^3 | 10 | 100 | O(10^4) | 80 KB |
| 10^4 | 10 | 1,000 | O(10^6) | 8 MB |
| 10^5 | 10 | 10,000 | O(10^8) | **800 MB** |
| 10^6 | 10 | 100,000 | O(10^10) | **80 GB** |
| 10^7 | 10 | 1,000,000 | O(10^12) | **8 TB** |

At ImageNet scale (N=1.2M), the redundancy similarity alone requires more than 100 GB of RAM for a single similarity matrix.

### 7.4 The Online Approximation

`OnlineStateTracker` and `OnlineExpertTracker` use EMA updates (O(1) per sample), avoiding the O(N^2) redundancy cost. But:
- EMA state centroids drift and the code detects this via `should_resplit()`, which triggers a full re-clustering
- The online trackers never recompute per-state metrics like similarity or redundancy
- There is no online version of `StateValue` theorem methods

### Verdict
**FAIL at scale.** SCX's complexity is dominated by:
1. O(N * K * d * n_init) for initial state discovery
2. O(N^2 / K) for pairwise redundancy computation
3. Full re-clustering required if K changes or states drift

At N > 10^5, the pairwise similarity computation becomes infeasible in RAM. The O(N^2) cost of the redundancy module is unreported in the papers. The "solution" (online EMA trackers) avoids the O(N^2) cost but sacrifices the per-state metrics that the gating formula requires. The per-acquisition cost of O(K) is acceptable, but the initialization cost dwarfs any acquisition savings for realistic datasets.

---

## Overall Verdict Table

| Attack | Verdict | Severity | Key Evidence |
|--------|---------|----------|-------------|
| 1. M >= 10 Experts | FAIL | Critical | Framework.fit() raises NotImplementedError; no experiment with M > 3; no distributed evaluation |
| 2. Memory Bank | FAIL | Critical | No memory bank exists in code; per-sample data is discarded; no nearest-neighbor index |
| 3. V(s) Bottleneck | MODERATE FAIL | High | V(s) is deprecated; K is hard-coded at 10; no incremental K adaptation |
| 4. Baseline Gaps | FAIL | Critical | No Query-by-Committee; no full training baseline; coverage metric is inappropriate |
| 5. Changing Practice | FAIL | Critical | Only synthetic 2D experiment complete; no real-world noisy datasets; MLIP uses proxy residuals |
| 6. Code Quality | MODERATE FAIL | Medium | Pipeline untestable (NotImplemented); tests shallow; some numerical gaps |
| 7. Complexity | FAIL at scale | High | O(N^2) similarity computation infeasible for N > 10^5; unspecified in papers |

### Decisive Defects

1. **The pipeline does not run.** `SCXFramework.fit()` raises `NotImplementedError`. The central orchestrating class is a stub. Everything else is a collection of well-tested but disconnected components.

2. **No multiple experts in any experiment.** The MLIP experiment uses a single DFT calculation, not multiple ACE/MACE potentials. The synthetic experiment uses M=3 trivial experts. The "M >= 10" regime that the theorems require is never tested.

3. **The memory bank does not exist.** The paper's narrative about retrospective per-sample analysis from a memory bank is entirely fictional. The code stores only running EMA summaries.

4. **V(s) is deprecated.** The gatekeeper formula that drives the narrative has been replaced by theorem-based methods, but these are not integrated into any working pipeline either.

5. **No real-world data.** The only quantitative experiment is on 500 synthetic 2D points. No Clothing1M, no WebVision, no real medical data, no real materials data with multiple experts.

6. **O(N^2) complexity hidden.** The pairwise similarity computation in the redundancy module makes the approach infeasible for N > 10^5, but this is not mentioned in any document or paper.

### Recommendation

**Reject as non-functional.** The SCX project is an elaborate mathematical framework with a clean component-level Python implementation and thorough theoretical development, but it has never been assembled into a working end-to-end system. The central pipeline class raises `NotImplementedError`. The memory bank is a paper concept, not code. The V(s) formula that drives the application narrative is deprecated. The only experiment that runs end-to-end is on 500 synthetic 2D points.

For Nature Computational Science, the framework would need:
1. A working end-to-end pipeline
2. Validation on at least two real-world scientific datasets with domain-appropriate baselines (including QBC)
3. Multiple experts (M >= 5) actually deployed and compared
4. Analysis of the O(N^2) scalability bottleneck with proposed mitigation
5. Medical or materials science results that demonstrate practical impact

The theoretical development is solid. The code components are well-structured and well-tested individually. But the framework as a whole does not yet perform the tasks it claims to perform.

---

*本分析由 Codex orchestrator agent 6 (计算科学家审查) 生成，2026-06-28*
