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
PREREG = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_end_to_end_near_real_time_preregistration_v0_1.json"
)
MODEL = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_near_real_time_model.py"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestP5EContractV01(unittest.TestCase):
    def test_preregistration_is_present_and_frozen_before_contract(self) -> None:
        p = load_json(PREREG)
        self.assertEqual(
            p["status"],
            "PREREGISTERED_BEFORE_RED",
        )
        self.assertFalse(p["real_p5e_execution_authorized"])

    def test_contract_exists(self) -> None:
        self.assertTrue(CONTRACT.is_file())

    def test_contract_schema_and_stage_are_exact(self) -> None:
        c = load_json(CONTRACT)
        self.assertEqual(
            c["schema"],
            "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
        )
        self.assertEqual(
            c["qualification_stage"],
            "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
        )
        self.assertFalse(c["real_p5e_execution_authorized"])

    def test_predecessor_blobs_are_exact(self) -> None:
        c = load_json(CONTRACT)
        self.assertEqual(
            c["predecessors"]["p5a_continuous_projection_contract_blob"],
            "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
        )
        self.assertEqual(
            c["predecessors"]["p5d4_loop_contract_blob"],
            "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
        )
        self.assertEqual(
            c["predecessors"]["p5d4_runtime_blob"],
            "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
        )
        self.assertEqual(
            c["predecessors"]["p5d4_human_adjudication_blob"],
            "ef5e07c6641db94e91d9f2bc0e8093b244baa507",
        )

    def test_timing_inheritance_is_exact_30_and_60(self) -> None:
        c = load_json(CONTRACT)
        t = c["near_real_time_timing"]
        self.assertEqual(t["poll_interval_seconds"], 30)
        self.assertEqual(t["detection_latency_seconds_max"], 60)
        self.assertTrue(t["instantaneous_realtime_claim_forbidden"])
        self.assertTrue(t["silent_interval_widening_forbidden"])
        self.assertTrue(t["silent_latency_bound_widening_forbidden"])

    def test_detection_latency_definition_is_explicit(self) -> None:
        c = load_json(CONTRACT)
        t = c["near_real_time_timing"]
        self.assertEqual(
            t["detection_latency_definition"],
            "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
        )
        self.assertEqual(
            t["future_real_bound_clock"],
            "MONOTONIC_ELAPSED_TIME",
        )

    def test_contract_forbids_authority_expansion(self) -> None:
        c = load_json(CONTRACT)
        a = c["authority_boundary"]
        for field in (
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
            self.assertFalse(a[field], field)

    def test_queue_conflict_resolves_in_favor_of_current_p5d4_semantics(self) -> None:
        c = load_json(CONTRACT)
        q = c["queue_and_supersession"]
        self.assertFalse(q["coalescing_authorized"])
        self.assertTrue(q["fifo_required"])
        self.assertTrue(q["silent_drop_forbidden"])
        self.assertTrue(q["latest_only_replacement_forbidden"])
        self.assertEqual(
            q["capacity_exhausted_result"],
            "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
        )
        self.assertTrue(q["pending_head_retarget_forbidden"])

    def test_contract_cannot_launder_synthetic_pass_into_real_p5e_pass(self) -> None:
        c = load_json(CONTRACT)
        claims = c["claim_boundary"]
        self.assertEqual(
            claims["maximum_current_claim"],
            "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED",
        )
        self.assertTrue(claims["real_end_to_end_qualification_requires_separate_authorization"])
        forbidden = set(claims["forbidden_current_claims"])
        self.assertIn("P5E_REAL_END_TO_END_QUALIFIED", forbidden)
        self.assertIn("REAL_60_SECOND_SLA_QUALIFIED", forbidden)
        self.assertIn("CONTINUOUS_SYNCHRONIZATION_QUALIFIED", forbidden)

    def test_required_breakers_cover_latency_queue_and_authority(self) -> None:
        c = load_json(CONTRACT)
        breakers = set(c["required_breakers"])
        required = {
            "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
            "DETECTION_BOUND_ABOVE_60_ACCEPTED",
            "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
            "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
            "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
            "EVALUATION_AUTHORITY_BECOMES_TRUE",
            "PROMOTION_AUTHORITY_BECOMES_TRUE",
            "PUBLICATION_AUTHORITY_BECOMES_TRUE",
            "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS",
        }
        self.assertTrue(required.issubset(breakers))

    def test_synthetic_model_exists_and_has_no_real_runtime_primitives(self) -> None:
        self.assertTrue(MODEL.is_file())
        source = MODEL.read_text(encoding="utf-8")
        forbidden = (
            "import time",
            "from time",
            "sleep(",
            "subprocess",
            "socket",
            "urllib",
            "requests",
            "pathlib",
            "open(",
            "os.",
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)

    def test_model_freezes_exact_plan(self) -> None:
        m = load_model()
        plan = m.make_timing_plan()
        self.assertEqual(plan["poll_interval_seconds"], 30)
        self.assertEqual(plan["detection_latency_seconds_max"], 60)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(poll_interval_seconds=31)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(detection_latency_seconds_max=61)

    def test_change_just_after_poll_detected_at_next_slot_passes(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 29)
        self.assertFalse(result["real_end_to_end_qualified"])

    def test_one_transient_failure_then_success_by_60_passes(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 59)

    def test_detection_after_60_seconds_is_rejected(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
                {"at_seconds": 90, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(
            result["status"],
            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
        )
        self.assertEqual(result["detection_latency_seconds"], 89)

    def test_no_detection_by_bound_is_rejected(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=0,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
            ],
        )
        self.assertEqual(
            result["status"],
            "FAIL_NO_DETECTION_BY_BOUND",
        )
        self.assertIsNone(result["detection_latency_seconds"])

    def test_model_rejects_non_30_second_schedule(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=1,
                observations=[
                    {"at_seconds": 31, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )


if __name__ == "__main__":
    unittest.main()
