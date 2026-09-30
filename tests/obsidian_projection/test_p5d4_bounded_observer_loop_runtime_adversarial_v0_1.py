import json
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection import p5d4_bounded_observer_loop as rt
from tools.obsidian_projection.observer_tick import INPUT_SCHEMA, make_initial_state

HEAD_A, HEAD_B = "1" * 40, "2" * 40
SHA_A, SHA_B, SHA_C = "a" * 64, "b" * 64, "c" * 64

def event(state, kind, observed=None, transition=None, candidate=None, failure=None):
    return {"schema":INPUT_SCHEMA,"event_type":kind,
        "sequence":state["last_event_sequence"]+1,"observed_head":observed,
        "transition_class":transition,"candidate_head":candidate,"failure_code":failure}

def evidence(head=HEAD_A):
    return {"schema":rt.EVIDENCE_SCHEMA,"candidate_head":head,
        "status":"PASS_LIVE_PUBLICATION_CONFIRMED",
        "transaction_plan_digest_sha256":SHA_C,
        "physical_receipt_digest_sha256":SHA_A,
        "logical_receipt_digest_sha256":SHA_B,
        "p5d2_promotion_confirmed_emitted":True}

class P5D4RuntimeAdversarialV01Tests(unittest.TestCase):
    def plan(self, **kw):
        values=dict(loop_id="adv-loop",max_cycles=5,max_remote_observations=5,
            max_evaluations=2,max_pending_heads=3,max_consecutive_failures=1)
        values.update(kw)
        return rt.make_loop_plan(**values)

    def persist(self, root, plan, state, evt, cycle=1):
        return rt.persist_tick(control_root=root,plan=plan,previous_state=state,
            normalized_input=evt,loop_id=plan["loop_id"],cycle_index=cycle)
    def test_unterminated_event_log_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/"observer-events.jsonl").write_bytes(b"{}")
            with self.assertRaises(rt.PersistenceError):
                rt.load_event_log(root)

    def test_tampered_event_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan(); state=make_initial_state()
            self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"))
            path=root/"observer-events.jsonl"
            path.write_text(path.read_text().replace('"cycle_index":1','"cycle_index":9'),
                encoding="utf-8",newline="\n")
            with self.assertRaises(rt.PersistenceError):
                rt.load_event_log(root)

    def test_record_origin_outside_contract_is_rejected_even_if_rehashed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan(); state=make_initial_state()
            self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"))
            path=root/"observer-events.jsonl"
            row=json.loads(path.read_text(encoding="utf-8"))
            row["record_origin"]="FORGED_ORIGIN"
            row["record_digest_sha256"]=rt._event_record_digest(row)
            path.write_bytes(rt._canonical_bytes(row))
            with self.assertRaises(rt.PersistenceError):
                rt.load_event_log(root)

    def test_log_more_than_one_record_ahead_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan(); state=make_initial_state()
            r1=self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"))
            cp1=(root/"observer-checkpoint.json").read_bytes()
            state=r1["tick_result"]["next_state"]
            r2=self.persist(root,plan,state,event(state,"EVALUATION_STARTED",candidate=HEAD_A),2)
            state=r2["tick_result"]["next_state"]
            self.persist(root,plan,state,event(state,"EVALUATION_PASSED",candidate=HEAD_A),2)
            (root/"observer-checkpoint.json").write_bytes(cp1)
            with self.assertRaises(rt.ReconciliationError):
                rt.reconcile_control_state(control_root=root,plan=plan,
                    verified_current_head=None,promotion_evidence=None)
    def test_one_record_ahead_with_nonreplayable_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan(); state=make_initial_state()
            r1=self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"))
            cp1=(root/"observer-checkpoint.json").read_bytes()
            state=r1["tick_result"]["next_state"]
            self.persist(root,plan,state,event(state,"EVALUATION_STARTED",candidate=HEAD_A),2)
            lines=(root/"observer-events.jsonl").read_text().splitlines()
            row=json.loads(lines[1]); row["normalized_input"]["candidate_head"]=HEAD_B
            row["record_digest_sha256"]=rt._event_record_digest(row)
            lines[1]=rt._canonical_bytes(row).decode().rstrip("\n")
            (root/"observer-events.jsonl").write_text("\n".join(lines)+"\n",
                encoding="utf-8",newline="\n")
            (root/"observer-checkpoint.json").write_bytes(cp1)
            with self.assertRaises(rt.ReconciliationError):
                rt.reconcile_control_state(control_root=root,plan=plan,
                    verified_current_head=None,promotion_evidence=None)

    def test_checkpoint_pending_queue_reorder_is_detected_against_log(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan(); state=make_initial_state()
            r1=self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"))
            state=r1["tick_result"]["next_state"]
            self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_B,"FAST_FORWARD"),2)
            p=root/"observer-checkpoint.json"; cp=json.loads(p.read_text())
            cp["observer_state"]["pending_heads"]=[HEAD_B,HEAD_A]
            cp["observer_state_digest_sha256"]=rt._digest(cp["observer_state"])
            p.write_bytes(rt._canonical_bytes(cp))
            with self.assertRaises(rt.ReconciliationError):
                rt.reconcile_control_state(control_root=root,plan=plan,
                    verified_current_head=None,promotion_evidence=None)
    def test_current_and_checkpoint_live_head_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan()
            rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=evidence())
            with self.assertRaises(rt.ReconciliationError):
                rt.reconcile_control_state(control_root=root,plan=plan,
                    verified_current_head=HEAD_B,promotion_evidence=evidence(HEAD_B))

    def test_unknown_ancestry_stops_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self.plan()
            rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=evidence())
            def observe(state):
                return event(state,"REMOTE_HEAD_OBSERVED",HEAD_B,"UNKNOWN")
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=observe,evaluation_adapter=lambda *_:None,
                verified_current_head=HEAD_A,promotion_evidence=evidence(),
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(report["observer_state"]["last_failure_code"],
                "UNKNOWN_ANCESTRY_REQUIRES_ADJUDICATION")

    def test_remote_observation_budget_is_hard_bound(self):
        plan=self.plan(max_remote_observations=1,max_consecutive_failures=5)
        def observe(state):
            return event(state,"REMOTE_OBSERVATION_FAILED",failure="NETWORK")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,evaluation_adapter=lambda *_:None,
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["remote_observations"],1)
            self.assertEqual(report["terminal_reason"],"BOUND_REACHED")
    def test_consecutive_failure_budget_zero_stops_after_first_failure(self):
        plan=self.plan(max_consecutive_failures=0)
        def observe(state):
            return event(state,"REMOTE_OBSERVATION_FAILED",failure="NETWORK")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,evaluation_adapter=lambda *_:None,
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["remote_observations"],1)
            self.assertEqual(report["terminal_reason"],"BOUND_REACHED")

    def test_evaluation_budget_zero_never_calls_evaluator_or_observer_when_pending(self):
        plan=self.plan(max_evaluations=0)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state=make_initial_state()
            self.persist(root,plan,state,event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"))
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                evaluation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["evaluations_started"],0)
            self.assertEqual(report["remote_observations"],0)
            self.assertEqual(report["terminal_reason"],"BOUND_REACHED")

    def test_unexpected_adapter_exception_becomes_fatal_and_releases_lock(self):
        plan=self.plan()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda *_: (_ for _ in ()).throw(RuntimeError("boom")),
                evaluation_adapter=lambda *_:None,verified_current_head=None,
                promotion_evidence=None,forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"FATAL_INCONSISTENCY")
            self.assertFalse((root/"ownership.lock").exists())
            persisted=json.loads((root/"last-run.json").read_text())
            self.assertEqual(persisted["terminal_reason"],"FATAL_INCONSISTENCY")
    def test_synthetic_runner_never_touches_forbidden_root(self):
        plan=self.plan(max_cycles=1)
        with tempfile.TemporaryDirectory() as ctl, tempfile.TemporaryDirectory() as protected:
            control=Path(ctl); root=Path(protected); sentinel=root/"sentinel.txt"
            sentinel.write_text("UNCHANGED",encoding="utf-8")
            before=sentinel.read_bytes()
            report=rt.run_bounded_loop(plan=plan,control_root=control,
                observation_adapter=lambda s:event(s,"REMOTE_OBSERVATION_FAILED",failure="N"),
                evaluation_adapter=lambda *_:None,verified_current_head=None,
                promotion_evidence=None,forbidden_roots=(root,),owner_token="owner")
            self.assertEqual(sentinel.read_bytes(),before)
            self.assertFalse(report["production_write_authorized"])

    def test_runtime_has_no_direct_semantic_state_assignment_or_external_process_surface(self):
        source=(Path(rt.__file__)).read_text(encoding="utf-8")
        self.assertNotRegex(
            source,
            r'state\["(?:observer_phase|pending_heads|live_projection_head)"\]\s*=(?!=)',
        )
        for token in (
            "import subprocess","import socket","os.system","Popen(",
            "check_output(","execute_one_real_live_publication",
        ):
            self.assertNotIn(token,source)

    def test_normal_stop_persists_terminal_reason_and_releases_lock(self):
        plan=self.plan()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda s:event(s,"REMOTE_OBSERVATION_FAILED",failure="N"),
                evaluation_adapter=lambda *_:None,verified_current_head=None,
                promotion_evidence=None,forbidden_roots=(),owner_token="owner")
            persisted=json.loads((root/"last-run.json").read_text())
            self.assertEqual(persisted["terminal_reason"],report["terminal_reason"])
            self.assertFalse((root/"ownership.lock").exists())

if __name__ == "__main__":
    unittest.main()
