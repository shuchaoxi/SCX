"""Smoke tests for the scx.expert module.

Run with: python tests/test_expert_module.py
"""

import sys
import os

# Ensure the src directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# ---- Patch scx/__init__.py to avoid pandas dependency during test ----
# We do this by providing a mock 'scx.core' that doesn't require pandas
import types
from unittest.mock import MagicMock

# Pre-register a minimal scx.core so the __init__.py import chain is satisfied
core_metrics_mod = types.ModuleType("scx.core.metrics")
core_metrics_mod.SCXMetrics = MagicMock()
sys.modules["scx.core.metrics"] = core_metrics_mod

core_framework_mod = types.ModuleType("scx.core.framework")
core_framework_mod.SCXFramework = MagicMock()
sys.modules["scx.core.framework"] = core_framework_mod

# Now we can import scx.expert without triggering pandas imports
import numpy as np
from scx.expert import ExpertInfo, ExpertRegistry, ExpertReliability, ExpertRouter, ExpertConflict

print("=== All imports OK ===")

# -----------------------------------------------------------------------
# 1. Registry
# -----------------------------------------------------------------------
reg = ExpertRegistry()
e1 = reg.register("linear", lambda x: x.sum(axis=1), cost=0.5, type="linear")
e2 = reg.register("rf", lambda x: x.mean(axis=1), cost=2.0, type="ensemble")
e3 = reg.register("knn", lambda x: x[:, 0], cost=1.0)
assert len(reg) == 3, f"Expected 3, got {len(reg)}"

info = reg.get(e1)
assert info.name == "linear"
assert info.cost == 0.5
assert info.metadata == {"type": "linear"}
assert isinstance(info.id, int)
assert callable(info.predict_fn)

# list
lst = reg.list()
assert len(lst) == 3

# unregister
reg.unregister(e3)
assert len(reg) == 2

# re-register
e3 = reg.register("knn", lambda x: x[:, 0], cost=1.0)
assert len(reg) == 3

# predict_all
X = np.random.randn(5, 4)
preds = reg.predict_all(X)
assert preds.shape == (3, 5), f"Expected (3, 5), got {preds.shape}"

# __len__
assert len(reg) == 3

# __repr__
rep = repr(reg)
assert "ExpertRegistry" in rep
assert "linear" in rep

# Error cases
try:
    reg.get(999)
    assert False, "Should have raised KeyError"
except KeyError:
    pass

try:
    reg.unregister(999)
    assert False, "Should have raised KeyError"
except KeyError:
    pass

print("OK: Registry")

# -----------------------------------------------------------------------
# 2. Reliability
# -----------------------------------------------------------------------
state_assignments = np.array([0, 0, 1, 1, 2])
y = np.random.randn(5)

# supervised
rel = ExpertReliability(method="supervised")
res = rel.estimate(reg, X, y, state_assignments, n_states=3)
assert res["R_matrix"].shape == (3, 3), f"Expected (3, 3), got {res['R_matrix'].shape}"
assert res["SCX_matrix"].shape == (3, 3)
assert res["uncertainties"].shape == (3, 3)
assert "n_per_state" in res
assert res["n_per_state"].shape == (3,)
print("OK: Reliability supervised")

# unsupervised
rel_u = ExpertReliability(method="unsupervised")
res_u = rel_u.estimate(reg, X, None, state_assignments, n_states=3)
assert res_u["R_matrix"].shape == (3, 3)
assert np.all((res_u["R_matrix"] >= 0) | np.isnan(res_u["R_matrix"]))
print("OK: Reliability unsupervised")

# bayesian
rel_b = ExpertReliability(method="bayesian")
res_b = rel_b.estimate(reg, X, y, state_assignments, n_states=3)
assert res_b["R_matrix"].shape == (3, 3)
print("OK: Reliability bayesian")

# hybrid
rel_h = ExpertReliability(method="hybrid")
res_h = rel_h.estimate(reg, X, y, state_assignments, n_states=3)
assert res_h["R_matrix"].shape == (3, 3)
print("OK: Reliability hybrid")

# hybrid with y=None should fall back to unsupervised
res_h2 = rel_h.estimate(reg, X, None, state_assignments, n_states=3)
assert res_h2["R_matrix"].shape == (3, 3)
print("OK: Reliability hybrid (y=None fallback)")

# compute_scx_from_risk
risk = np.array([[0.1, 0.5], [0.3, 0.2]])
scx = ExpertReliability.compute_scx_from_risk(risk)
assert scx.shape == (2, 2)
assert np.all(scx > 0)
assert np.all(scx < 1.0)
print("OK: compute_scx_from_risk")

# reliability with custom loss_fn
rel_custom = ExpertReliability(method="supervised", loss_fn=lambda yp, yt: (yp - yt) ** 2)
res_c = rel_custom.estimate(reg, X, y, state_assignments, n_states=3)
assert res_c["R_matrix"].shape == (3, 3)
print("OK: Reliability custom loss_fn")

# reliability unknown method
try:
    ExpertReliability(method="unknown")
    assert False
except ValueError:
    pass
print("OK: Reliability unknown method error")

# -----------------------------------------------------------------------
# 3. Router
# -----------------------------------------------------------------------
router = ExpertRouter(reg, alpha=1.0)

# hard route
hard = router.route_hard(X, state_assignments, res["R_matrix"])
assert hard.shape == (5,)
assert all(hid in [info.id for info in reg.list()] for hid in hard)
print("OK: Router hard")

# weighted
weights = router.route_weighted(X, state_assignments, res["R_matrix"])
assert weights.shape == (5, 3)
np.testing.assert_almost_equal(weights.sum(axis=1), np.ones(5))
assert np.all(weights >= 0)
print("OK: Router weighted")

# weighted with temperature
weights_hot = router.route_weighted(X, state_assignments, res["R_matrix"], temperature=10.0)
assert weights_hot.shape == (5, 3)
np.testing.assert_almost_equal(weights_hot.sum(axis=1), np.ones(5))
print("OK: Router weighted (high temperature)")

# ensemble
ensemble = router.ensemble_predict(X, state_assignments, res["R_matrix"])
assert ensemble.shape == (5,)
print("OK: Router ensemble")

# cost-sensitive
cs = router.route_cost_sensitive(X, state_assignments, res["R_matrix"], lambda_cost=0.5)
assert cs.shape == (5,)
print("OK: Router cost-sensitive")

# cost-sensitive with lambda=0 (should match hard route)
cs_zero = router.route_cost_sensitive(X, state_assignments, res["R_matrix"], lambda_cost=0.0)
assert cs_zero.shape == (5,)
print("OK: Router cost-sensitive (lambda=0)")

print("OK: All router methods")

# -----------------------------------------------------------------------
# 4. Conflict
# -----------------------------------------------------------------------
# conflict_matrix
cm = ExpertConflict.conflict_matrix(X, reg, state_assignments, 3)
assert cm.shape == (3, 3, 3), f"Expected (3, 3, 3), got {cm.shape}"
# Check symmetry
for k in range(3):
    assert np.allclose(cm[:, :, k], cm[:, :, k].T), f"State {k} matrix not symmetric"
    assert np.allclose(np.diag(cm[:, :, k]), 0.0), f"State {k} diagonal not zero"
print("OK: Conflict matrix")

# conflict_score
score = ExpertConflict.conflict_score(X, reg)
assert 0.0 <= score <= 1.0
print(f"OK: Conflict score = {score:.4f}")

# conflict_score with 1 expert
reg1 = ExpertRegistry()
reg1.register("only", lambda x: x[:, 0])
score1 = ExpertConflict.conflict_score(X, reg1)
assert score1 == 0.0
print("OK: Conflict score (1 expert = 0)")

# conflict_score with empty X
score_empty = ExpertConflict.conflict_score(np.empty((0, 4)), reg)
assert score_empty == 0.0
print("OK: Conflict score (empty)")

# detect
detected = ExpertConflict.detect(0, reg, X, threshold=0.1)
print(f"OK: Conflict detect = {detected}")

# arbitrate
R = res["R_matrix"]
arb = ExpertConflict.arbitrate(X, reg, R, 0, method="lowest_risk")
assert arb in [info.id for info in reg.list()]
print(f"OK: Arbitrate (lowest_risk) = {arb}")

arb_vote = ExpertConflict.arbitrate(X, reg, R, 0, method="weighted_vote")
assert arb_vote == -1
print("OK: Arbitrate (weighted_vote)")

arb_avg = ExpertConflict.arbitrate(X, reg, R, 0, method="average")
assert arb_avg == -1
print("OK: Arbitrate (average)")

# unknown method
try:
    ExpertConflict.arbitrate(X, reg, R, 0, method="invalid")
    assert False
except ValueError:
    pass
print("OK: Arbitrate unknown method error")

# pairwise_disagreement
preds = reg.predict_all(X)
D = ExpertConflict.pairwise_disagreement(preds)
assert D.shape == (3, 3)
assert np.allclose(D, D.T)
assert np.allclose(np.diag(D), 0.0)
assert np.all(D >= 0)
print("OK: Pairwise disagreement")

# -----------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------
print()
print("=== ALL TESTS PASSED ===")
