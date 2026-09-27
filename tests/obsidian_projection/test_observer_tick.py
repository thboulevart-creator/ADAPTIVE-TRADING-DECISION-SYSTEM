from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tools.obsidian_projection.observer_tick import (
    DECISION_SCHEMA,
    EVENT_SCHEMA,
    INPUT_SCHEMA,
    RESULT_SCHEMA,
    STATE_SCHEMA,
    ObserverTickError,
    canonical_result_bytes,
    make_initial_state,
    one_shot_tick,
)


H1 = "1" * 40
H2 = "2" * 40
H3 = "3" * 40
H4 = "4" * 40


def event(
    sequence: int,
    event_type: str,
    *,
    observed_head: str | None = None,
    transition_class: str | None = None,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": sequence,
        "observed_head": observed_head,
        "transition_class": transition_class,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }


def tick(
    state: dict,
    event_type: str,
    **kwargs,
) -> dict:
    payload = event(
        state["last_event_sequence"] + 1,
        event_type,
        **kwargs,
    )
    return one_shot_tick(state, payload)


def bootstrap() -> dict:
    state = make_initial_state()
    return tick(
        state,
        "BOOTSTRAP",
    )["next_state"]


def observe_initial(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "REMOTE_HEAD_OBSERVED",
        observed_head=head,
        transition_class="INITIAL",
    )["next_state"]


def begin_evaluation(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_STARTED",
        candidate_head=head,
    )["next_state"]


def qualify(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_PASSED",
        candidate_head=head,
    )["next_state"]


def promote(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "PROMOTION_CONFIRMED",
        candidate_head=head,
    )["next_state"]


def make_current_state() -> dict:
    state = bootstrap()
    state = observe_initial(state, H1)
    state = begin_evaluation(state, H1)
    state = qualify(state, H1)
    state = promote(state, H1)
    return state


class ObserverTickTests(unittest.TestCase):
    def test_initial_state_is_canonical(self) -> None:
        state = make_initial_state()
        self.assertEqual(state["schema"], STATE_SCHEMA)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(
            state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            state["projection_state"],
            "MISSING",
        )
        self.assertEqual(state["pending_heads"], [])
        self.assertEqual(state["last_event_sequence"], 0)

    def test_bootstrap_changes_only_sequence(self) -> None:
        state = make_initial_state()
        result = tick(state, "BOOTSTRAP")
        next_state = result["next_state"]
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] = 1
        self.assertEqual(next_state, expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )
        self.assertEqual(
            result["decision"]["reason_code"],
            "BOOTSTRAP_ACCEPTED",
        )

    def test_bootstrap_rejects_noncanonical_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["remote_freshness"] = "KNOWN"
        with self.assertRaises(ObserverTickError):
            tick(state, "BOOTSTRAP")

    def test_initial_head_is_queued_exactly_once(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["latest_observed_head"],
            H1,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1],
        )
        self.assertEqual(
            next_state["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "MISSING",
        )
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )

    def test_initial_rejected_after_previous_observation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="INITIAL",
            )

    def test_same_head_is_strict_noop_for_queue(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        before_pending = copy.deepcopy(
            state["pending_heads"]
        )
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            before_pending,
        )
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_same_requires_previous_observed_equality(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_network_failure_from_current_becomes_stale(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            "NETWORK_UNAVAILABLE",
        )

    def test_same_head_restores_current_after_network_failure(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "CURRENT",
        )

    def test_same_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_fast_forward_queues_without_retargeting_active(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1, H2],
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )

    def test_fast_forward_requires_previous_observed_head(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["blocked_head"],
            H2,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertNotIn(H2, next_state["pending_heads"])

    def test_unknown_ancestry_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="UNKNOWN",
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )
        self.assertNotIn(
            H2,
            result["next_state"]["pending_heads"],
        )

    def test_evaluation_start_binds_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        result = tick(
            state,
            "EVALUATION_STARTED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H1],
        )
        self.assertEqual(
            result["decision"]["candidate_head"],
            H1,
        )

    def test_evaluation_start_rejects_non_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H2,
            )

    def test_evaluation_start_requires_idle(self) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H1,
            )

    def test_evaluation_pass_advances_qualified_not_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["last_qualified_head"],
            H1,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [],
        )
        self.assertEqual(
            next_state["observer_phase"],
            "CANDIDATE_PENDING",
        )

    def test_evaluation_pass_preserves_newer_queued_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )
        self.assertEqual(
            result["next_state"]["last_qualified_head"],
            H1,
        )

    def test_evaluation_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_FAILED",
            candidate_head=H2,
            failure_code="CANDIDATE_INVALID",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["blocked_head"],
            H2,
        )

    def test_promotion_confirmation_is_logical_only(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["live_projection_head"],
            H1,
        )
        self.assertEqual(
            next_state["projection_state"],
            "CURRENT",
        )
        self.assertEqual(
            result["decision"][
                "production_write_authorized"
            ],
            False,
        )
        self.assertEqual(
            result["decision"][
                "automatic_promotion_authorized"
            ],
            False,
        )

    def test_promotion_confirmation_stays_stale_if_newer_remote(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            H1,
        )
        self.assertEqual(
            result["next_state"]["latest_observed_head"],
            H2,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "STALE",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )

    def test_promotion_rejects_nonqualified_candidate(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "PROMOTION_CONFIRMED",
                candidate_head=H2,
            )

    def test_promotion_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        state = qualify(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "PROMOTION_FAILED",
            candidate_head=H2,
            failure_code="POINTER_NOT_CONFIRMED",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_lock_contended_changes_only_sequence(
        self,
    ) -> None:
        state = make_current_state()
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] += 1
        result = tick(
            state,
            "LOCK_CONTENDED",
            failure_code="LOCK_CONTENDED",
        )
        self.assertEqual(result["next_state"], expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_shutdown_preserves_pending_and_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "STOPPED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )

    def test_stopped_state_accepts_no_further_event(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )["next_state"]
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_input_sequence_skip_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 2,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_input_sequence_replay_is_rejected(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"],
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_boolean_sequence_is_rejected(self) -> None:
        state = make_initial_state()
        payload = event(
            True,
            "BOOTSTRAP",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_extra_input_field_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["unexpected"] = "x"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_wrong_input_schema_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["schema"] = "WRONG"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_remote_observed_requires_head(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                transition_class="INITIAL",
            )

    def test_remote_observed_requires_transition_class(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
            )

    def test_invalid_repository_is_rejected(self) -> None:
        state = make_initial_state()
        state["repository"] = "wrong/repo"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_invalid_branch_is_rejected(self) -> None:
        state = make_initial_state()
        state["branch"] = "main"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_uppercase_head_is_rejected(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head="A" * 40,
                transition_class="INITIAL",
            )

    def test_duplicate_pending_heads_are_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["pending_heads"] = [H1, H1]
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_current_unknown_freshness_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["remote_freshness"] = "UNKNOWN"
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_current_head_mismatch_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["latest_observed_head"] = H2
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_evaluating_empty_queue_is_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "EVALUATING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_caller_inputs_are_not_mutated(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        state_before = copy.deepcopy(state)
        payload_before = copy.deepcopy(payload)
        one_shot_tick(state, payload)
        self.assertEqual(state, state_before)
        self.assertEqual(payload, payload_before)

    def test_result_schemas_and_authority_flags(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        self.assertEqual(result["schema"], RESULT_SCHEMA)
        self.assertEqual(
            result["next_state"]["schema"],
            STATE_SCHEMA,
        )
        self.assertEqual(
            result["decision"]["schema"],
            DECISION_SCHEMA,
        )
        self.assertEqual(
            result["audit"]["schema"],
            EVENT_SCHEMA,
        )
        self.assertFalse(
            result["decision"][
                "automatic_promotion_authorized"
            ]
        )
        self.assertFalse(
            result["decision"][
                "production_write_authorized"
            ]
        )

    def test_same_inputs_are_byte_deterministic(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        first = one_shot_tick(state, payload)
        second = one_shot_tick(state, payload)
        self.assertEqual(first, second)
        self.assertEqual(
            canonical_result_bytes(first),
            canonical_result_bytes(second),
        )

    def test_canonical_result_is_compact_sorted_lf(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        raw = canonical_result_bytes(result)
        self.assertTrue(raw.endswith(b"\n"))
        self.assertNotIn(b": ", raw)
        self.assertNotIn(b", ", raw)
        decoded = json.loads(raw.decode("utf-8"))
        self.assertEqual(decoded, result)

    def test_audit_digests_match_canonical_values(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        result = one_shot_tick(state, payload)

        def digest(value: dict) -> str:
            raw = (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
            return hashlib.sha256(raw).hexdigest()

        audit = result["audit"]
        self.assertEqual(
            audit["previous_state_digest"],
            digest(state),
        )
        self.assertEqual(
            audit["input_digest"],
            digest(payload),
        )
        self.assertEqual(
            audit["decision_digest"],
            digest(result["decision"]),
        )
        self.assertEqual(
            audit["next_state_digest"],
            digest(result["next_state"]),
        )

    def test_audit_has_no_volatile_host_fields(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        audit = result["audit"]
        for forbidden in (
            "observed_at",
            "timestamp",
            "host_id",
            "process_id",
            "pid",
            "path",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, audit)


if __name__ == "__main__":
    unittest.main()
