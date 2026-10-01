import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_end_to_end_near_real_time_contract_v0_1.json"
)
MODEL = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_near_real_time_model.py"
)


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model_adv", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_contract_invariants(contract: dict) -> None:
    assert (
        contract["schema"]
        == "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1"
    )
    assert contract["qualification_stage"] == (
        "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY"
    )
    assert contract["real_p5e_execution_authorized"] is False

    timing = contract["near_real_time_timing"]
    assert timing["poll_interval_seconds"] == 30
    assert timing["detection_latency_seconds_max"] == 60
    assert timing["instantaneous_realtime_claim_forbidden"] is True
    assert timing["silent_interval_widening_forbidden"] is True
    assert timing["silent_latency_bound_widening_forbidden"] is True

    authority = contract["authority_boundary"]
    for field in (
        "pending_head_evaluation_authorized",
        "evaluation_authorized",
        "stage_a_authorized",
        "stage_b_authorized",
        "promotion_authorized",
        "publication_authorized",
        "real_vault_mutation_authorized",
        "current_mutation_authorized",
        "current_tmp_mutation_authorized",
        "real_polling_loop_authorized",
        "daemon_authorized",
        "startup_registration_authorized",
        "scheduled_task_authorized",
        "windows_service_authorized",
        "p6_authorized",
    ):
        assert authority[field] is False

    queue = contract["queue_and_supersession"]
    assert queue["fifo_required"] is True
    assert queue["silent_drop_forbidden"] is True
    assert queue["silent_reorder_forbidden"] is True
    assert queue["latest_only_replacement_forbidden"] is True
    assert queue["coalescing_authorized"] is False
    assert queue["new_coalescing_semantic_event_authorized"] is False
    assert queue["pending_head_retarget_forbidden"] is True
    assert (
        queue["capacity_exhausted_result"]
        == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    )
    assert queue["precedence_rule"] == (
        "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_"
        "EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT"
    )

    claims = contract["claim_boundary"]
    assert claims["maximum_current_claim"] == (
        "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED"
    )
    assert claims["real_end_to_end_qualification_requires_separate_authorization"]
    forbidden = set(claims["forbidden_current_claims"])
    assert "P5E_REAL_END_TO_END_QUALIFIED" in forbidden
    assert "REAL_60_SECOND_SLA_QUALIFIED" in forbidden
    assert "CONTINUOUS_SYNCHRONIZATION_QUALIFIED" in forbidden


class TestP5EAdversarialV01(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract()
        assert_contract_invariants(self.contract)

    def assert_mutation_rejected(self, mutator) -> None:
        candidate = copy.deepcopy(self.contract)
        mutator(candidate)
        with self.assertRaises(AssertionError):
            assert_contract_invariants(candidate)

    def test_poll_interval_31_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["near_real_time_timing"].__setitem__(
                "poll_interval_seconds", 31
            )
        )

    def test_detection_bound_61_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["near_real_time_timing"].__setitem__(
                "detection_latency_seconds_max", 61
            )
        )

    def test_real_execution_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c.__setitem__("real_p5e_execution_authorized", True)
        )

    def test_evaluation_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "evaluation_authorized", True
            )
        )

    def test_promotion_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "promotion_authorized", True
            )
        )

    def test_publication_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "publication_authorized", True
            )
        )

    def test_real_polling_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "real_polling_loop_authorized", True
            )
        )

    def test_p6_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "p6_authorized", True
            )
        )

    def test_coalescing_reintroduction_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "coalescing_authorized", True
            )
        )

    def test_latest_only_replacement_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "latest_only_replacement_forbidden", False
            )
        )

    def test_capacity_exhaustion_silent_continue_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "capacity_exhausted_result", "CONTINUE_WITH_LATEST"
            )
        )

    def test_p5a_design_intent_cannot_override_current_p5d4(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "precedence_rule", "P5A_SUPERSESSION_WINS"
            )
        )

    def test_synthetic_pass_cannot_be_relabelled_real_pass(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["claim_boundary"].__setitem__(
                "maximum_current_claim", "P5E_REAL_END_TO_END_QUALIFIED"
            )
        )

    def test_real_pass_must_remain_forbidden_claim(self) -> None:
        def mutate(c):
            c["claim_boundary"]["forbidden_current_claims"].remove(
                "P5E_REAL_END_TO_END_QUALIFIED"
            )

        self.assert_mutation_rejected(mutate)

    def test_required_breakers_are_unique_and_broad(self) -> None:
        breakers = self.contract["required_breakers"]
        self.assertEqual(len(breakers), len(set(breakers)))
        self.assertGreaterEqual(len(breakers), 25)

    def test_synthetic_model_has_no_dynamic_import_escape(self) -> None:
        source = MODEL.read_text(encoding="utf-8")
        for token in (
            "__import__",
            "importlib",
            "eval(",
            "exec(",
            "globals(",
            "locals(",
        ):
            self.assertNotIn(token, source)

    def test_exact_60_second_boundary_passes(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=0,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_success_before_source_availability_is_not_detection(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=31,
            observations=[
                {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
                {"at_seconds": 90, "outcome": "READ_FAILURE"},
            ],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertIsNone(result["detection_latency_seconds"])

    def test_negative_source_time_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=-1,
                observations=[
                    {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )

    def test_boolean_source_time_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=True,
                observations=[
                    {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )

    def test_empty_observation_list_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=[],
            )

    def test_duplicate_observation_time_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=[
                    {"at_seconds": 30, "outcome": "READ_FAILURE"},
                    {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )

    def test_invalid_observation_outcome_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=[
                    {"at_seconds": 30, "outcome": "PROMOTE"},
                ],
            )

    def test_incomplete_window_does_not_claim_pass(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
            ],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertFalse(result["real_end_to_end_qualified"])
        self.assertFalse(result["continuous_synchronization_qualified"])

    def test_all_model_results_keep_downstream_authority_false(self) -> None:
        m = load_model()
        cases = [
            [
                {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
            [
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
            ],
            [
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
                {"at_seconds": 90, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        ]
        for observations in cases:
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=observations,
            )
            self.assertFalse(result["automatic_evaluation_authorized"])
            self.assertFalse(result["automatic_promotion_authorized"])
            self.assertFalse(result["automatic_publication_authorized"])


if __name__ == "__main__":
    unittest.main()
