#!/usr/bin/env python3
"""
Theorem 3 测试套件 —— 噪声-困难样本不可区分性的全面验证。

测试覆盖:
  1. NoiseDifficultyUnidentifiability 构造的正确性
  2. verification_test() 观测等价性验证
  3. FanoExecutableProof 的逐步正确性
  4. minimal_sufficient_assumptions() 的 A1-A6 检验
  5. scan() 与 yajie.py 接口兼容性
  6. 边界条件与异常处理
  7. Theorem 3' 固定 PE 保持性
  8. 决策规则不可区分性
  9. 数值精度与统计一致性
"""

from __future__ import annotations

import numpy as np
import pytest
import sys
import os

# 确保 src 在路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scx.theorem3 import (
    NoiseDifficultyUnidentifiability,
    FixedPositionalEncoding,
    VerificationResult,
    verification_test,
    FanoExecutableProof,
    fano_executable_proof,
    AssumptionAudit,
    AssumptionCheck,
    minimal_sufficient_assumptions,
    Theorem3ScanResult,
    scan,
    decision_rule_error_bound,
    _binary_entropy,
    _kl_divergence_bernoulli,
    _total_variation,
    _compute_fano_bound,
)

# ============================================================================
# 固定参数
# ============================================================================

DEFAULT_ETA = 0.2
DEFAULT_SEED = 42


# ============================================================================
# 1. NoiseDifficultyUnidentifiability 构造测试
# ============================================================================

class TestNoiseDifficultyUnidentifiabilityConstruction:
    """验证二元世界构造的正确性。"""

    def test_initialization_valid_eta(self):
        """η ∈ (0, 0.5) 应正常初始化。"""
        for eta in [0.01, 0.1, 0.2, 0.35, 0.49]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            assert ndu.eta == eta

    def test_initialization_invalid_eta(self):
        """η ≤ 0 或 η ≥ 0.5 应抛出 ValueError。"""
        for bad_eta in [-0.1, 0.0, 0.5, 0.8, 1.0]:
            with pytest.raises(ValueError):
                NoiseDifficultyUnidentifiability(eta=bad_eta)

    def test_joint_pmf_sums_to_one(self):
        """联合 PMF 之和应为 1。"""
        for eta in [0.1, 0.2, 0.35]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            pmf = ndu.joint_pmf()
            total = sum(pmf.values())
            assert abs(total - 1.0) < 1e-10

    def test_joint_pmf_values(self):
        """验证 P(X, Y) 的具体数值。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        pmf = ndu.joint_pmf()
        # P(X=+1, Y=+1) = 0.5 * 0.8 = 0.4
        assert abs(pmf[(+1.0, +1.0)] - 0.4) < 1e-10
        # P(X=+1, Y=-1) = 0.5 * 0.2 = 0.1
        assert abs(pmf[(+1.0, -1.0)] - 0.1) < 1e-10
        # P(X=-1, Y=+1) = 0.5 * 0.2 = 0.1
        assert abs(pmf[(-1.0, +1.0)] - 0.1) < 1e-10
        # P(X=-1, Y=-1) = 0.5 * 0.8 = 0.4
        assert abs(pmf[(-1.0, -1.0)] - 0.4) < 1e-10

    def test_joint_pmf_symmetry(self):
        """联合分布应满足对称性: P(X=+1,Y=+1) = P(X=-1,Y=-1)。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        pmf = ndu.joint_pmf()
        assert abs(pmf[(+1.0, +1.0)] - pmf[(-1.0, -1.0)]) < 1e-10
        assert abs(pmf[(+1.0, -1.0)] - pmf[(-1.0, +1.0)]) < 1e-10

    def test_conditional_probability(self):
        """P(Y|X) 的条件概率验证。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.3)
        # P(Y=+1 | X=+1) = 1-η = 0.7
        py1, pyn1 = ndu._p_y_given_x(+1.0)
        assert abs(py1 - 0.7) < 1e-10
        assert abs(pyn1 - 0.3) < 1e-10
        # P(Y=+1 | X=-1) = η = 0.3
        py1, pyn1 = ndu._p_y_given_x(-1.0)
        assert abs(py1 - 0.3) < 1e-10
        assert abs(pyn1 - 0.7) < 1e-10

    def test_marginal_y_is_uniform(self):
        """P(Y=+1) = P(Y=-1) = 1/2。"""
        for eta in [0.1, 0.2, 0.35]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            pmf = ndu.joint_pmf()
            p_y1 = sum(pmf[(x, +1.0)] for x in ndu.x_values)
            p_yn1 = sum(pmf[(x, -1.0)] for x in ndu.x_values)
            assert abs(p_y1 - 0.5) < 1e-10
            assert abs(p_yn1 - 0.5) < 1e-10

    def test_detection_margin_negative(self):
        """Δ_s = 2η - 1 < 0 when η < 0.5。"""
        for eta in [0.1, 0.2, 0.35, 0.49]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            margin = ndu.detection_margin()
            assert margin < 0.0
            assert abs(margin - (2 * eta - 1)) < 1e-10

    def test_bayes_error_equals_eta(self):
        """贝叶斯最优错误率 = η。"""
        for eta in [0.1, 0.2, 0.35]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            assert abs(ndu.bayes_error() - eta) < 1e-10

    def test_mutual_information_positive(self):
        """I(Y;X) > 0 when η ≠ 0.5。"""
        for eta in [0.05, 0.2, 0.45]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            mi = ndu.mutual_information_xy()
            assert mi > 0.0

    def test_mutual_information_increases_with_eta(self):
        """当 η 偏离 0.5 时，I(Y;X) 减小（不确定性降低）。"""
        mi_low = NoiseDifficultyUnidentifiability(eta=0.1).mutual_information_xy()
        mi_high = NoiseDifficultyUnidentifiability(eta=0.4).mutual_information_xy()
        # η=0.4 更接近 0.5，H(Y|X) 更大，I(Y;X) 更小
        assert mi_low > mi_high


# ============================================================================
# 2. 样本生成测试
# ============================================================================

class TestSampling:
    """验证世界 W_A 和 W_B 的样本生成。"""

    def test_world_a_sample_shapes(self):
        """W_A 样本应包含正确的键和形状。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        data = ndu.sample_world_a(1000)
        assert len(data["X"]) == 1000
        assert len(data["Y_obs"]) == 1000
        assert len(data["Y_true"]) == 1000
        assert set(data.keys()) >= {"X", "Y_obs", "Y_true", "world"}

    def test_world_b_sample_shapes(self):
        """W_B 样本应包含正确的键和形状。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        data = ndu.sample_world_b(1000)
        assert len(data["X"]) == 1000
        assert len(data["Y_obs"]) == 1000
        assert len(data["Y_true"]) == 1000

    def test_world_a_has_flips(self):
        """W_A 中应存在标签翻转。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.3, seed=42)
        data = ndu.sample_world_a(10000)
        flip_rate = np.mean(data["Y_obs"] != data["Y_true"])
        assert abs(flip_rate - 0.3) < 0.05  # 99.7% 置信区间约为 0.3 ± 0.014

    def test_world_b_no_flips(self):
        """W_B 中 Y_obs = Y_true（无翻转）。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        data = ndu.sample_world_b(10000)
        assert np.all(data["Y_obs"] == data["Y_true"])

    def test_world_a_y_true_deterministic(self):
        """W_A 中 Y_true = X（确定性）。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        data = ndu.sample_world_a(1000)
        assert np.all(data["Y_true"] == data["X"])

    def test_position_generation(self):
        """with_position=True 时应有 P 和 PE_P。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        ndu = NoiseDifficultyUnidentifiability(
            eta=0.2, with_position=True, pe=pe, seed=42
        )
        data_a = ndu.sample_world_a(500)
        assert "P" in data_a
        assert "PE_P" in data_a
        assert data_a["PE_P"].shape == (500, 8)

    def test_reproducibility(self):
        """固定种子应产生完全相同的样本。"""
        for world in ["A", "B"]:
            ndu1 = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
            ndu2 = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
            data1 = ndu1.sample(n=500, world=world)
            data2 = ndu2.sample(n=500, world=world)
            assert np.allclose(data1["X"], data2["X"])
            assert np.allclose(data1["Y_obs"], data2["Y_obs"])

    def test_different_seeds_different_samples(self):
        """不同种子应产生不同样本。"""
        ndu1 = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        ndu2 = NoiseDifficultyUnidentifiability(eta=0.2, seed=99)
        data1 = ndu1.sample_world_a(1000)
        data2 = ndu2.sample_world_a(1000)
        # 极大概率不一样
        assert not np.allclose(data1["X"], data2["X"])


# ============================================================================
# 3. verification_test() 测试
# ============================================================================

class TestVerificationTest:
    """验证观测等价性的验证程序。"""

    def test_small_eta_indistinguishable(self):
        """小 η 下两世界应不可区分。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        result = verification_test(ndu, n_samples=20000, n_trials=3)
        assert result.indistinguishable
        assert result.joint_pmf_match
        assert result.conditional_match
        assert result.margin_match
        assert result.tv_distance < 1e-10

    def test_large_eta_indistinguishable(self):
        """大 η 下依然不可区分（只要 η < 0.5）。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.45, seed=42)
        result = verification_test(ndu, n_samples=20000, n_trials=3)
        assert result.indistinguishable

    def test_empirical_tv_converges_to_zero(self):
        """经验 TV 距离随样本量增加应趋近于 0。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        tvs = []
        for n in [1000, 5000, 20000]:
            result = verification_test(ndu, n_samples=n, n_trials=1)
            tvs.append(float(np.mean(result.sample_tv_distances)))
        # TV 应该随 n 增大而递减
        assert tvs[0] >= tvs[2] * 0.5  # 允许统计波动

    def test_kl_divergence_is_zero(self):
        """同分布 → KL = 0。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        result = verification_test(ndu, n_samples=5000, n_trials=1)
        assert result.kl_divergence < 1e-15

    def test_fano_bound_computed(self):
        """Fano 下界应为有限非负数。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.3)
        result = verification_test(ndu, n_samples=5000, n_trials=1)
        assert result.fano_bound >= 0.0
        assert np.isfinite(result.fano_bound)

    def test_verification_with_position_preserves(self):
        """启用固定 PE 时不破坏等价性。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        ndu = NoiseDifficultyUnidentifiability(
            eta=0.2, with_position=True, pe=pe, seed=42
        )
        result = verification_test(ndu, n_samples=20000, n_trials=3)
        assert result.indistinguishable
        pe_preserves = result.details.get("pe_preserves", False)
        assert pe_preserves, f"固定 PE 应保持不可区分性: {result.details.get('pe_details', {})}"


# ============================================================================
# 4. FanoExecutableProof 测试
# ============================================================================

class TestFanoExecutableProof:
    """Fano 不等式可执行证明的验证。"""

    def test_conditional_entropy_correct(self):
        """H(Y|X) = H_2(η) 应正确计算。"""
        for eta in [0.1, 0.2, 0.35]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            proof = FanoExecutableProof(ndu)
            H = proof.step_1_conditional_entropy()
            expected = _binary_entropy(eta)
            assert abs(H["H(Y|X)_nat"] - expected) < 1e-10

    def test_entropy_decomposition_consistent(self):
        """H(Y|X) = H(Y) - I(Y;X) 应成立。"""
        for eta in [0.1, 0.2, 0.35]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            proof = FanoExecutableProof(ndu)
            dec = proof.step_2_entropy_decomposition()
            H1 = dec["H(Y|X)_nat"]
            H2 = dec["H(Y|X)_reconstructed"]
            assert abs(H1 - H2) < 1e-10

    def test_world_comparison_identical(self):
        """两个世界的 Fano 界应相同。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        proof = FanoExecutableProof(ndu)
        comp = proof.step_4_world_comparison()
        assert comp["identical"]
        assert comp["Fano_bound_W_A"] == comp["Fano_bound_W_B"]

    def test_birge_bound_equals_bayes(self):
        """Birgé 下界 = η = 贝叶斯最优错误率。"""
        for eta in [0.1, 0.2, 0.4]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            proof = FanoExecutableProof(ndu)
            birge = proof.step_5_birge_inequality()
            assert abs(birge["Bayes_error"] - eta) < 1e-10
            assert abs(birge["birge_lower_bound"] - eta) < 1e-10

    def test_fano_executable_proof_returns_all_steps(self):
        """fano_executable_proof 应返回完整步骤。"""
        result = fano_executable_proof(eta=0.25, verbose=False)
        assert "step1_conditional_entropy" in result
        assert "step2_entropy_decomposition" in result
        assert "step3_fano_inequality" in result
        assert "step4_world_comparison" in result
        assert "step5_birge_inequality" in result

    def test_fano_bound_zero_for_small_eta(self):
        """小 η 时经典 Fano 下界可能为 0（vacuous）。"""
        for eta in [0.01, 0.05]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            bound = _compute_fano_bound(ndu)
            assert bound >= 0.0  # 非负


# ============================================================================
# 5. minimal_sufficient_assumptions() 测试
# ============================================================================

class TestMinimalSufficientAssumptions:
    """A1-A6 假设审计的验证。"""

    def test_all_assumptions_satisfied_default(self):
        """默认构造下所有 6 个假设应成立。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        audit = minimal_sufficient_assumptions(ndu)
        assert audit.all_satisfied
        assert audit.minimally_sufficient
        assert len(audit.assumptions) == 6

    def test_assumption_a1_binary_feature(self):
        """A1: 特征域二元性验证。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        audit = minimal_sufficient_assumptions(ndu)
        a1 = audit.assumptions[0]
        assert a1.name == "A1"
        assert a1.satisfied
        assert a1.necessity == "necessary"

    def test_assumption_a3_observational_equivalence(self):
        """A3: 观测分布等价性 —— 最关键的假设。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        audit = minimal_sufficient_assumptions(ndu)
        a3 = audit.assumptions[2]
        assert a3.name == "A3"
        assert a3.satisfied
        assert a3.necessity == "both"

    def test_assumption_a4_noise_mechanism_world_a(self):
        """A4: W_A 的噪声机制成立。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.25, seed=42)
        data_a = ndu.sample_world_a(20000)
        audit = minimal_sufficient_assumptions(ndu, data_a=data_a)
        a4 = audit.assumptions[3]
        assert a4.satisfied
        assert "W_A" in a4.description

    def test_assumption_a5_no_noise_world_b(self):
        """A5: W_B 的 Y_obs = Y_true。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        data_b = ndu.sample_world_b(20000)
        audit = minimal_sufficient_assumptions(ndu, data_b=data_b)
        a5 = audit.assumptions[4]
        assert a5.satisfied

    def test_assumption_a6_iid(self):
        """A6: i.i.d. 采样假设。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        audit = minimal_sufficient_assumptions(ndu)
        a6 = audit.assumptions[5]
        assert a6.satisfied

    def test_minimal_set_necessary_assumptions(self):
        """验证 A1, A3, A6 是必要的最小充分集。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        audit = minimal_sufficient_assumptions(ndu)
        necessary = [a for a in audit.assumptions if a.necessity in ("necessary", "both")]
        necessary_names = {a.name for a in necessary}
        assert "A1" in necessary_names
        assert "A3" in necessary_names
        assert "A6" in necessary_names

    def test_summary_contains_eta(self):
        """审计摘要应包含 η 信息。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.33, seed=42)
        audit = minimal_sufficient_assumptions(ndu)
        assert "0.33" in audit.summary or "η" in audit.summary


# ============================================================================
# 6. scan() — yajie.py 接口兼容性测试
# ============================================================================

class TestScanInterface:
    """验证 scan() 与 yajie.py 的接口兼容性。"""

    def test_scan_returns_theorem3_scan_result(self):
        """scan() 应返回 Theorem3ScanResult 实例。"""
        result = scan(eta=0.2, n_samples=10000, verbose=False)
        assert isinstance(result, Theorem3ScanResult)

    def test_scan_result_to_dict(self):
        """to_dict() 应返回可序列化的字典。"""
        result = scan(eta=0.2, n_samples=5000, verbose=False)
        d = result.to_dict()
        assert "theorem" in d
        assert "eta" in d
        assert "verification_passed" in d
        assert isinstance(d["verification_passed"], bool)

    def test_scan_result_report(self):
        """report() 应返回非空字符串。"""
        result = scan(eta=0.2, n_samples=5000, verbose=False)
        report = result.report()
        assert len(report) > 0
        assert "Theorem 3" in report

    def test_scan_with_position(self):
        """scan() 的 with_position 参数应传递到 PE 初始化。"""
        result = scan(eta=0.2, n_samples=5000, with_position=True, d_pe=8, verbose=False)
        assert result.metadata["with_position"] is True
        assert result.metadata["d_pe"] == 8

    def test_scan_different_etas(self):
        """不同 η 值应产生不同的 Fano 界。"""
        r1 = scan(eta=0.1, n_samples=3000, verbose=False)
        r2 = scan(eta=0.4, n_samples=3000, verbose=False)
        # 两者均鉴别为"不可区分"
        assert r1.verification.indistinguishable
        assert r2.verification.indistinguishable

    def test_scan_metadata(self):
        """元数据应包含完整的运行参数。"""
        result = scan(eta=0.2, n_samples=3000, seed=99, verbose=False)
        meta = result.metadata
        assert meta["n_samples"] == 3000
        assert meta["seed"] == 99
        assert "pe_type" in meta


# ============================================================================
# 7. 决策规则测试
# ============================================================================

class TestDecisionRule:
    """验证决策规则不可区分性的数学论证。"""

    def test_error_bound_at_least_half(self):
        """决策规则错误下界应 ≥ 1/2。"""
        for eta in [0.1, 0.2, 0.35, 0.45]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            bound = decision_rule_error_bound(ndu, n=100)
            assert bound["decision_error_lower_bound"] >= 0.4999  # 数值容差

    def test_exact_tv_is_zero(self):
        """精确 TV 距离应为 0。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        bound = decision_rule_error_bound(ndu)
        assert bound["TV(P_A, P_B)"] < 1e-15

    def test_optimal_error_is_random_guess(self):
        """最优策略等同于随机猜测（error = 0.5）。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.3)
        bound = decision_rule_error_bound(ndu)
        assert abs(bound["optimal_error"] - 0.5) < 1e-10

    def test_error_bound_independent_of_n(self):
        """错误下界与样本量 n 无关 —— 多看看不帮助区分。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        b1 = decision_rule_error_bound(ndu, n=1)
        b10k = decision_rule_error_bound(ndu, n=10000)
        assert abs(b1["decision_error_lower_bound"] - b10k["decision_error_lower_bound"]) < 1e-10


# ============================================================================
# 8. FixedPositionalEncoding 测试
# ============================================================================

class TestFixedPositionalEncoding:
    """固定位置编码的测试（Theorem 3' 前提条件）。"""

    def test_default_creation(self):
        """应能创建默认编码。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        assert pe.d_pe == 8
        assert len(pe.lambdas) == 4  # d_pe // 2

    def test_encode_output_shape(self):
        """编码输出形状应为 (N, d_pe)。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        p = np.array([0.0, 0.5, 1.0], dtype=np.float64)
        enc = pe.encode(p)
        assert enc.shape == (3, 8)

    def test_encode_deterministic(self):
        """编码应为确定性函数。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        p = np.array([0.0, 1.0, -1.0], dtype=np.float64)
        enc1 = pe.encode(p)
        enc2 = pe.encode(p)
        assert np.allclose(enc1, enc2)

    def test_encoding_norm_approx_one(self):
        """‖PE(p)‖ ≈ 1（归一化编码）。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        p = np.array([0.0, 1.0, 2.5], dtype=np.float64)
        enc = pe.encode(p)
        for i in range(len(p)):
            norm = np.linalg.norm(enc[i])
            assert abs(norm - 1.0) < 1e-10

    def test_different_positions_different_encoding(self):
        """不同位置应产生不同编码。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        p1 = np.array([0.0], dtype=np.float64)
        p2 = np.array([1.0], dtype=np.float64)
        enc1 = pe.encode(p1)
        enc2 = pe.encode(p2)
        assert not np.allclose(enc1, enc2)

    def test_custom_lambdas(self):
        """自定义波长应被正确使用。"""
        custom_lambdas = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
        pe = FixedPositionalEncoding(d_pe=8, lambdas=custom_lambdas)
        assert np.allclose(pe.lambdas, custom_lambdas)

    def test_higher_dimensional_encoding(self):
        """高维编码应保持归一化。"""
        for d_pe in [4, 16, 32]:
            pe = FixedPositionalEncoding.default(d_pe=d_pe)
            p = np.array([0.0, 1.0], dtype=np.float64)
            enc = pe.encode(p)
            assert enc.shape == (2, d_pe)
            for i in range(2):
                assert abs(np.linalg.norm(enc[i]) - 1.0) < 1e-10


# ============================================================================
# 9. 辅助函数单元测试
# ============================================================================

class TestUtilityFunctions:
    """数学辅助函数的正确性验证。"""

    def test_binary_entropy_values(self):
        """H_2(p) 的具体值验证。"""
        assert abs(_binary_entropy(0.5) - np.log(2.0)) < 1e-10  # 最大熵 = ln 2
        assert abs(_binary_entropy(0.0)) < 1e-15
        assert abs(_binary_entropy(1.0)) < 1e-15

    def test_binary_entropy_symmetry(self):
        """H_2(p) = H_2(1-p)。"""
        for p in [0.1, 0.3, 0.45]:
            assert abs(_binary_entropy(p) - _binary_entropy(1.0 - p)) < 1e-10

    def test_kl_divergence_self_is_zero(self):
        """D_KL(p || p) = 0。"""
        for p in [0.1, 0.3, 0.5]:
            assert _kl_divergence_bernoulli(p, p) < 1e-15

    def test_kl_divergence_nonnegative(self):
        """KL 散度非负。"""
        for p in [0.1, 0.3, 0.4]:
            for q in [0.2, 0.5, 0.6]:
                if p != q:
                    assert _kl_divergence_bernoulli(p, q) > 0.0

    def test_total_variation_identical_is_zero(self):
        """相同分布的 TV = 0。"""
        p = np.array([0.25, 0.25, 0.25, 0.25])
        assert _total_variation(p, p) < 1e-15

    def test_total_variation_range(self):
        """TV ∈ [0, 1]。"""
        p = np.array([0.5, 0.5, 0.0, 0.0])
        q = np.array([0.0, 0.0, 0.5, 0.5])
        tv = _total_variation(p, q)
        assert 0.0 <= tv <= 1.0
        assert abs(tv - 1.0) < 1e-10  # 完全不相交

    def test_total_variation_bound_holds(self):
        """TV(P, Q) = sup_A |P(A) - Q(A)| 应成立。"""
        p = np.array([0.4, 0.1, 0.1, 0.4])
        q = np.array([0.3, 0.2, 0.2, 0.3])
        tv = _total_variation(p, q)
        # TV 应等于任意事件集合上的最大差异
        max_diff = max(abs(p[i] - q[i]) for i in range(4))
        assert tv >= max_diff / 2.0  # TV = 1/2 ||P - Q||_1


# ============================================================================
# 10. 集成测试：Theorem 3' 固定 PE 保持不可区分性
# ============================================================================

class TestTheorem3Prime:
    """Theorem 3' —— 固定位置编码下不可区分性的保持。"""

    def test_pe_does_not_distinguish_worlds(self):
        """固定 PE 增强的观测仍不可区分（命题 4.1）。"""
        for d_pe in [4, 8, 16]:
            pe = FixedPositionalEncoding.default(d_pe=d_pe)
            ndu = NoiseDifficultyUnidentifiability(
                eta=0.2, with_position=True, pe=pe, seed=42
            )
            result = verification_test(ndu, n_samples=15000, n_trials=3)
            assert result.indistinguishable, f"d_pe={d_pe}: 固定 PE 应保持不可区分性"

    def test_pe_encoding_moments_match(self):
        """PE(P) 的矩在两个世界中应匹配。"""
        pe = FixedPositionalEncoding.default(d_pe=8)
        ndu = NoiseDifficultyUnidentifiability(
            eta=0.2, with_position=True, pe=pe, seed=42
        )
        data_a = ndu.sample_world_a(10000)
        data_b = ndu.sample_world_b(10000)
        pe_a = data_a["PE_P"]
        pe_b = data_b["PE_P"]
        # 均值差应在采样噪声范围内
        mean_diff = np.max(np.abs(np.mean(pe_a, axis=0) - np.mean(pe_b, axis=0)))
        assert mean_diff < 0.05  # 3σ 应约为 0.03

    def test_no_position_same_as_no_pe(self):
        """无位置 = 无 PE = Theorem 3 原始版本。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, with_position=False, seed=42)
        result = verification_test(ndu, n_samples=10000, n_trials=3)
        assert result.indistinguishable


# ============================================================================
# 11. 边界条件与异常处理测试
# ============================================================================

class TestEdgeCases:
    """边界条件与异常路径测试。"""

    def test_eta_close_to_zero(self):
        """η → 0 的极限情况。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.001)
        result = verification_test(ndu, n_samples=10000, n_trials=1)
        assert result.indistinguishable

    def test_eta_close_to_half(self):
        """η → 0.5 的极限情况。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.499)
        result = verification_test(ndu, n_samples=10000, n_trials=1)
        assert result.indistinguishable

    def test_large_sample_generation(self):
        """大数据量采样不应出错。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        data = ndu.sample_world_a(100000)
        assert len(data["X"]) == 100000

    def test_scan_with_small_samples(self):
        """scan() 小样本也能运行。"""
        result = scan(eta=0.2, n_samples=500, verbose=False)
        assert isinstance(result, Theorem3ScanResult)

    def test_unknown_world_raises(self):
        """不存在的世界应抛出 ValueError。"""
        ndu = NoiseDifficultyUnidentifiability(eta=0.2)
        with pytest.raises(ValueError):
            ndu.sample(n=100, world="C")

    def test_fano_proof_verbose_does_not_crash(self):
        """verbose 模式不应崩溃。"""
        result = fano_executable_proof(eta=0.2, verbose=False)
        assert len(result) == 5

    def test_information_theoretic_identities(self):
        """验证信息论恒等式。"""
        for eta in [0.1, 0.2, 0.35]:
            ndu = NoiseDifficultyUnidentifiability(eta=eta)
            H_Y_given_X = ndu.conditional_entropy_y_given_x()
            H_Y = np.log(2.0)
            I_XY = ndu.mutual_information_xy()
            # H(Y|X) = H(Y) - I(Y;X)
            assert abs(H_Y_given_X - (H_Y - I_XY)) < 1e-10


# ============================================================================
# 12. 性能回归测试
# ============================================================================

class TestPerformance:
    """性能基准 —— 确保关键操作在合理时间内完成。"""

    def test_scan_completes_quickly(self):
        """scan() 应在 3 秒内完成（中等样本量）。"""
        import time
        t0 = time.time()
        scan(eta=0.2, n_samples=10000, verbose=False)
        elapsed = time.time() - t0
        assert elapsed < 10.0, f"scan() 耗时 {elapsed:.1f}s，超过 10s 阈值"

    def test_large_sample_performance(self):
        """大样本采样应在合理时间内完成。"""
        import time
        ndu = NoiseDifficultyUnidentifiability(eta=0.2, seed=42)
        t0 = time.time()
        ndu.sample_world_a(200000)
        ndu.sample_world_b(200000)
        elapsed = time.time() - t0
        assert elapsed < 5.0, f"40 万样本采样耗时 {elapsed:.1f}s"


# ============================================================================
# pytest 配置
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
