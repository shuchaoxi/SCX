# SCX Valuation Module
#
# Data value assessment: learnability, noise score, redundancy, state-value,
# and the four-way data classifier.
#
# V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s)  (deprecated)
#
# Theorem-based methods (v0.6):
#   Theorem 1 — hoeffding_bound, chernoff_bound, StateValue.noise_consistency_score,
#               StateValue.optimal_noise_threshold, StateValue.noise_detection_f1_bound
#   Theorem 2 — StateValue.feature_strength_diagnostic

from .learnability import LearnabilityScore
from .noise_score import NoiseScore
from .redundancy import RedundancyScore
from .classifier import DataClassifier
from .state_value import StateValue, hoeffding_bound, chernoff_bound
from .adaptive import AdaptiveThreshold
from .influence import StateConditionedInfluence

__all__ = [
    "LearnabilityScore",
    "NoiseScore",
    "RedundancyScore",
    "DataClassifier",
    "StateValue",
    "AdaptiveThreshold",
    "StateConditionedInfluence",
    "hoeffding_bound",
    "chernoff_bound",
]
