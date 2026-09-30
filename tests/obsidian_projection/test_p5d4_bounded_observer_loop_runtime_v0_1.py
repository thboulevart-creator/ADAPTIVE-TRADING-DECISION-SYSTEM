import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection.observer_tick import INPUT_SCHEMA, make_initial_state

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_PATH = ROOT / "tools" / "obsidian_projection" / "p5d4_bounded_observer_loop.py"
PREREG_REL = "tools/obsidian_projection/p5d4_bounded_observer_loop_runtime_preregistration_v0_1.json"
PREREG_BLOB = "7645a96ae8b9b827a78c3313127219023dd2c7ac"
HEAD_A, HEAD_B = "1" * 40, "2" * 40
SHA_A, SHA_B, SHA_C = "a" * 64, "b" * 64, "c" * 64

def _git_blob(relative):
    return subprocess.run(["git","rev-parse",f"HEAD:{relative}"],cwd=str(ROOT),
        check=True,text=True,capture_output=True).stdout.strip()

def _event(state, event_type, observed=None, transition=None, candidate=None, failure=None):
    return {"schema":INPUT_SCHEMA,"event_type":event_type,
        "sequence":state["last_event_sequence"]+1,"observed_head":observed,
        "transition_class":transition,"candidate_head":candidate,"failure_code":failure}

def _evidence(head=HEAD_A):
    return {"schema":"ATDS_OBSIDIAN_P5D4_VERIFIED_PUBLICATION_EVIDENCE_V0_1",
        "candidate_head":head,"status":"PASS_LIVE_PUBLICATION_CONFIRMED",
        "transaction_plan_digest_sha256":SHA_C,"physical_receipt_digest_sha256":SHA_A,
        "logical_receipt_digest_sha256":SHA_B,"p5d2_promotion_confirmed_emitted":True}
class P5D4RuntimeV01Tests(unittest.TestCase):
    def _runtime(self):
        self.assertTrue(RUNTIME_PATH.exists(), "RED: P5-D4 runtime candidate does not exist yet")
        spec = importlib.util.spec_from_file_location(
            "tools.obsidian_projection.p5d4_bounded_observer_loop", RUNTIME_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _plan(self, rt, **overrides):
        values = dict(loop_id="synthetic-loop-01", max_cycles=4,
            max_remote_observations=4, max_evaluations=2,
            max_pending_heads=2, max_consecutive_failures=1)
        values.update(overrides)
        return rt.make_loop_plan(**values)

    def test_00_preregistration_blob_is_exact(self):
        self.assertEqual(_git_blob(PREREG_REL), PREREG_BLOB)

    def test_01_runtime_surface_and_api(self):
        rt = self._runtime()
        for name in ("make_loop_plan","validate_loop_plan","acquire_ownership",
            "release_ownership","load_event_log","load_checkpoint",
            "reconcile_control_state","reconstruct_from_verified_publication_evidence",
            "persist_tick","run_bounded_loop"):
            self.assertTrue(callable(getattr(rt,name,None)), name)

    def test_02_loop_plan_is_digest_bound_and_strict(self):
        rt = self._runtime()
        first, second = self._plan(rt), self._plan(rt)
        self.assertEqual(first, second)
        self.assertRegex(first["plan_digest_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(rt.validate_loop_plan(first), first)
        for field,value in (("max_cycles",0),("max_pending_heads",0),
            ("max_evaluations",-1),("max_cycles",True)):
            with self.assertRaises(rt.LoopPlanError):
                self._plan(rt, **{field:value})
    def test_03_ownership_exclusive_and_no_auto_steal(self):
        rt = self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            owner=rt.acquire_ownership(root,loop_id="a",owner_token="one")
            with self.assertRaises(rt.OwnershipContended):
                rt.acquire_ownership(root,loop_id="b",owner_token="two")
            wrong=dict(owner); wrong["owner_token"]="wrong"
            with self.assertRaises(rt.OwnershipError):
                rt.release_ownership(root,wrong)
            self.assertTrue((root/"ownership.lock").exists())
            rt.release_ownership(root,owner)
            self.assertFalse((root/"ownership.lock").exists())

    def test_04_persist_tick_event_then_checkpoint(self):
        rt=self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            result=rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            log=rt.load_event_log(root); cp=rt.load_checkpoint(root)
            self.assertEqual(len(log),1)
            self.assertIsNone(log[0]["previous_record_digest_sha256"])
            self.assertEqual(cp["last_event_digest_sha256"],log[0]["record_digest_sha256"])
            self.assertEqual(cp["observer_state"],result["tick_result"]["next_state"])

    def test_05_crash_window_replays_exactly_one_event(self):
        rt=self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            def fault(point):
                if point=="AFTER_EVENT_DURABLE_BEFORE_CHECKPOINT_REPLACE":
                    raise RuntimeError("synthetic crash")
            with self.assertRaises(RuntimeError):
                rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                    normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                    loop_id=plan["loop_id"],cycle_index=1,fault_injector=fault)
            self.assertIsNone(rt.load_checkpoint(root))
            rec=rt.reconcile_control_state(control_root=root,plan=plan,
                verified_current_head=None,promotion_evidence=None)
            self.assertEqual(rec["status"],"PASS_RECONCILED_ONE_RECORD_AHEAD")
            self.assertEqual(rec["observer_state"]["last_event_sequence"],1)
    def test_06_checkpoint_or_log_corruption_fails_closed(self):
        rt=self._runtime()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            (root/"observer-events.jsonl").write_bytes(b"")
            with self.assertRaises(rt.ReconciliationError):
                rt.reconcile_control_state(control_root=root,plan=plan,
                    verified_current_head=None,promotion_evidence=None)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); plan=self._plan(rt); state=make_initial_state()
            rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            p=root/"observer-checkpoint.json"; value=json.loads(p.read_text())
            value["observer_state_digest_sha256"]=SHA_A
            p.write_text(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
            with self.assertRaises(rt.PersistenceError):
                rt.load_checkpoint(root)

    def test_07_queue_capacity_blocks_before_tick(self):
        rt=self._runtime(); plan=self._plan(rt,max_pending_heads=1)
        state=make_initial_state()
        state=rt.persist_tick
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); initial=make_initial_state()
            first=rt.persist_tick(control_root=root,plan=plan,previous_state=initial,
                normalized_input=_event(initial,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=1)
            queued=first["tick_result"]["next_state"]
            with self.assertRaises(rt.QueueCapacityError):
                rt.persist_tick(control_root=root,plan=plan,previous_state=queued,
                    normalized_input=_event(queued,"REMOTE_HEAD_OBSERVED",HEAD_B,"FAST_FORWARD"),
                    loop_id=plan["loop_id"],cycle_index=2)
            self.assertEqual(len(rt.load_event_log(root)),1)
    def test_08_existing_current_reconstructs_via_four_evidence_events(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            result=rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=_evidence())
            state=result["observer_state"]; log=rt.load_event_log(root)
            self.assertEqual(state["projection_state"],"CURRENT")
            self.assertEqual(state["live_projection_head"],HEAD_A)
            self.assertEqual(len(log),4)
            self.assertEqual([x["normalized_input"]["event_type"] for x in log],
                ["REMOTE_HEAD_OBSERVED","EVALUATION_STARTED",
                 "EVALUATION_PASSED","PROMOTION_CONFIRMED"])
            self.assertTrue(all(x["record_origin"]=="EVIDENCE_RECONSTRUCTION" for x in log))
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(rt.ReconciliationError):
                rt.reconstruct_from_verified_publication_evidence(
                    control_root=Path(td),plan=plan,verified_current_head=HEAD_A,
                    promotion_evidence=None)

    def test_09_two_cycles_qualify_then_stop_for_promotion_authority(self):
        rt=self._runtime(); plan=self._plan(rt,max_cycles=2); calls={"obs":0,"eval":0}
        def observe(state):
            calls["obs"]+=1
            return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL")
        def evaluate(candidate,activation):
            calls["eval"]+=1
            self.assertEqual(candidate,HEAD_A)
            self.assertEqual(activation["decision"]["action"],"START_EXACT_HEAD_EVALUATION")
            return {"outcome":"QUALIFIED","failure_code":None}
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,evaluation_adapter=evaluate,
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"PROMOTION_AUTHORITY_REQUIRED")
            self.assertEqual(report["cycles_started"],2)
            self.assertEqual(report["evaluations_started"],1)
            self.assertFalse(report["automatic_promotion_authorized"])
            self.assertEqual(calls,{"obs":1,"eval":1})
    def test_10_same_current_is_noop_without_evaluation(self):
        rt=self._runtime(); plan=self._plan(rt); calls={"eval":0}
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=_evidence())
            def observe(state):
                return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"SAME")
            def evaluate(*args):
                calls["eval"]+=1
                raise AssertionError("SAME must not evaluate")
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=observe,evaluation_adapter=evaluate,
                verified_current_head=HEAD_A,promotion_evidence=_evidence(),
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"NO_PENDING_WORK")
            self.assertEqual(report["observer_state"]["projection_state"],"CURRENT")
            self.assertEqual(calls["eval"],0)

    def test_11_non_fast_forward_blocks_without_evaluation(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rt.reconstruct_from_verified_publication_evidence(
                control_root=root,plan=plan,verified_current_head=HEAD_A,
                promotion_evidence=_evidence())
            def observe(state):
                return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_B,"NON_FAST_FORWARD")
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=observe,
                evaluation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                verified_current_head=HEAD_A,promotion_evidence=_evidence(),
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(report["observer_state"]["observer_phase"],"BLOCKED")
    def test_12_rejected_and_blocked_evaluation_remain_distinct(self):
        rt=self._runtime(); plan=self._plan(rt,max_cycles=2)
        def observe(state):
            return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,
                evaluation_adapter=lambda *_:{"outcome":"REJECTED","failure_code":"BREAK"},
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["observer_state"]["observer_phase"],"BLOCKED")
            self.assertEqual(report["observer_state"]["last_failure_code"],"BREAK")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,
                evaluation_adapter=lambda *_:{"outcome":"BLOCKED","failure_code":"INFRA"},
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(report["observer_state"]["observer_phase"],"EVALUATING")

    def test_13_cycle_and_evaluation_budgets_are_hard_bounds(self):
        rt=self._runtime(); plan=self._plan(rt,max_cycles=1)
        calls={"obs":0,"eval":0}
        def observe(state):
            calls["obs"]+=1
            return _event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL")
        with tempfile.TemporaryDirectory() as td:
            report=rt.run_bounded_loop(plan=plan,control_root=Path(td),
                observation_adapter=observe,
                evaluation_adapter=lambda *_: calls.__setitem__("eval",calls["eval"]+1),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"BOUND_REACHED")
            self.assertEqual(report["cycles_started"],1)
            self.assertEqual(calls,{"obs":1,"eval":0})
    def test_14_second_runner_writes_nothing(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            owner=rt.acquire_ownership(root,loop_id="held",owner_token="held")
            before={p.relative_to(root).as_posix():p.read_bytes()
                for p in root.rglob("*") if p.is_file()}
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                evaluation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="second")
            after={p.relative_to(root).as_posix():p.read_bytes()
                for p in root.rglob("*") if p.is_file()}
            self.assertEqual(report["terminal_reason"],"LOCK_CONTENDED")
            self.assertEqual(before,after)
            rt.release_ownership(root,owner)

    def test_15_restart_in_evaluating_never_repeats_evaluation(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); state=make_initial_state()
            first=rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"REMOTE_HEAD_OBSERVED",HEAD_A,"INITIAL"),
                loop_id=plan["loop_id"],cycle_index=0)
            state=first["tick_result"]["next_state"]
            rt.persist_tick(control_root=root,plan=plan,previous_state=state,
                normalized_input=_event(state,"EVALUATION_STARTED",candidate=HEAD_A),
                loop_id=plan["loop_id"],cycle_index=0)
            calls={"eval":0}
            report=rt.run_bounded_loop(plan=plan,control_root=root,
                observation_adapter=lambda *_: (_ for _ in ()).throw(AssertionError()),
                evaluation_adapter=lambda *_: calls.__setitem__("eval",calls["eval"]+1),
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="owner")
            self.assertEqual(report["terminal_reason"],"RECONCILIATION_REQUIRED")
            self.assertEqual(calls["eval"],0)
    def test_16_control_root_boundary_and_static_authority_surface(self):
        rt=self._runtime(); plan=self._plan(rt)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            with self.assertRaises(rt.P5D4RuntimeError):
                rt.run_bounded_loop(plan=plan,control_root=root,
                    observation_adapter=lambda *_:None,evaluation_adapter=lambda *_:None,
                    verified_current_head=None,promotion_evidence=None,
                    forbidden_roots=(root,),owner_token="owner")
        source=RUNTIME_PATH.read_text(encoding="utf-8")
        for token in ("while True","time.sleep","asyncio.sleep","Timer(","schtasks",
            "WindowsService","p5d3f_promotion_handoff","p5d3g_stageb_real_execution",
            "execute_one_real_live_publication","execute_finite_live_publication",
            "build_current_head_projection","stage_candidate_generation"):
            self.assertNotIn(token,source)
        self.assertIn("one_shot_tick",source)
        self.assertIn("make_initial_state",source)

if __name__ == "__main__":
    unittest.main()
