import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

from tools.obsidian_projection import p5d4_bounded_observer_loop as rt
from tools.obsidian_projection.observer_tick import INPUT_SCHEMA, make_initial_state

ROOT = Path(__file__).resolve().parents[2]
USERPROFILE = Path(os.environ["USERPROFILE"])
CANONICAL = USERPROFILE / "ATDS-CONTROL" / "OBSIDIAN-PROJECTION" / "P5D4"
QUAL = USERPROFILE / "ATDS-CONTROL" / "_QUALIFICATION"
NATIVE = Path(os.environ["LOCALAPPDATA"]) / "Python" / "bin" / "python.exe"
OLD_ALIAS = Path(os.environ["LOCALAPPDATA"]) / "ATDS-OBSIDIAN-PROJECTION" / "P5D4"
HISTORICAL_REDIRECT = (
    Path(os.environ["LOCALAPPDATA"]) / "Packages"
    / "PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0"
    / "LocalCache" / "Local" / "ATDS-OBSIDIAN-PROJECTION" / "P5D4"
)
HEAD = "1" * 40

def cleanup(path):
    shutil.rmtree(path, ignore_errors=True)

def tree_hash(path):
    if not path.exists():
        return None
    h = hashlib.sha256()
    for p in sorted(path.rglob("*"), key=lambda x: x.as_posix().lower()):
        rel = p.relative_to(path).as_posix().encode()
        h.update(rel + b"\0")
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()

def event(state):
    return {
        "schema": INPUT_SCHEMA,
        "event_type": "REMOTE_HEAD_OBSERVED",
        "sequence": state["last_event_sequence"] + 1,
        "observed_head": HEAD,
        "transition_class": "INITIAL",
        "candidate_head": None,
        "failure_code": None,
    }

class P5D4ControlRootBindingAdversarialV01Tests(unittest.TestCase):
    def test_00_production_root_lifecycle_state_preserves_exact_binding(self):
        resolved = rt.resolve_and_validate_control_root(CANONICAL)
        self.assertEqual(
            os.path.normcase(str(resolved)),
            os.path.normcase(str(CANONICAL.resolve(strict=False))),
        )
        if CANONICAL.exists():
            self.assertTrue(CANONICAL.is_dir())
            self.assertFalse(CANONICAL.is_symlink())
            is_junction = getattr(CANONICAL, "is_junction", None)
            if callable(is_junction):
                self.assertFalse(is_junction())

    def test_01_store_native_and_powershell_compute_same_production_root(self):
        self.assertTrue(NATIVE.is_file())
        store_value = str(rt.canonical_production_control_root())
        native = subprocess.run(
            [str(NATIVE), "-B", "-c",
             "from tools.obsidian_projection import p5d4_bounded_observer_loop as r;"
             "print(r.canonical_production_control_root())"],
            cwd=str(ROOT), check=True, text=True, capture_output=True,
        ).stdout.strip()
        ps = subprocess.run(
            ["powershell","-NoProfile","-Command",
             r"$p=Join-Path $env:USERPROFILE 'ATDS-CONTROL\OBSIDIAN-PROJECTION\P5D4';"
             "[IO.Path]::GetFullPath($p)"],
            check=True,text=True,capture_output=True,
        ).stdout.strip()
        expected = os.path.normcase(str(CANONICAL.resolve(strict=False)))
        self.assertEqual(os.path.normcase(store_value), expected)
        self.assertEqual(os.path.normcase(native), expected)
        self.assertEqual(os.path.normcase(ps), expected)
    def test_02_old_alias_rejected_before_any_control_mutation(self):
        candidate = OLD_ALIAS / ("forbidden-" + uuid.uuid4().hex)
        self.assertFalse(candidate.exists())
        with self.assertRaises(rt.ControlRootBindingError):
            rt._validate_control_root(candidate)
        self.assertFalse(candidate.exists())

    def test_03_historical_redirect_is_evidence_only_and_unchanged(self):
        if not HISTORICAL_REDIRECT.exists():
            self.skipTest("historical redirected evidence unavailable")
        before = tree_hash(HISTORICAL_REDIRECT)
        with self.assertRaises(rt.ControlRootBindingError):
            rt.resolve_and_validate_control_root(HISTORICAL_REDIRECT)
        after = tree_hash(HISTORICAL_REDIRECT)
        self.assertEqual(before, after)

    def test_04_store_lock_is_visible_to_powershell(self):
        root = QUAL / ("ps-lock-" + uuid.uuid4().hex)
        try:
            owner = rt.acquire_ownership(root, loop_id="cross", owner_token="store")
            ps = subprocess.run(
                ["powershell","-NoProfile","-Command",
                 f"$p='{str(root / 'ownership.lock')}'; if(Test-Path -LiteralPath $p){{'VISIBLE'}}else{{'ABSENT'}}"],
                check=True,text=True,capture_output=True,
            ).stdout.strip()
            self.assertEqual(ps, "VISIBLE")
            rt.release_ownership(root, owner)
        finally:
            cleanup(root)

    def test_05_second_native_runner_cannot_write_or_call_adapters(self):
        root = QUAL / ("runner-native-" + uuid.uuid4().hex)
        try:
            owner = rt.acquire_ownership(root, loop_id="held", owner_token="store-owner")
            script = f"""
import json
from pathlib import Path
from tools.obsidian_projection import p5d4_bounded_observer_loop as r

root = Path({str(root)!r})
plan = r.make_loop_plan(
    loop_id="second",
    max_cycles=1,
    max_remote_observations=1,
    max_evaluations=0,
    max_pending_heads=1,
    max_consecutive_failures=0,
)
marker = root / "ADAPTER_CALLED"

def obs(state):
    marker.write_text("OBS", encoding="utf-8")
    raise RuntimeError("must not call")

def ev(*args):
    marker.write_text("EVAL", encoding="utf-8")
    raise RuntimeError("must not call")

out = r.run_bounded_loop(
    plan=plan,
    control_root=root,
    observation_adapter=obs,
    evaluation_adapter=ev,
    verified_current_head=None,
    promotion_evidence=None,
    forbidden_roots=(),
    owner_token="native-second",
)
print(json.dumps(out, sort_keys=True, separators=(",", ":")))
"""
            out = subprocess.run(
                [str(NATIVE),"-B","-c",script],cwd=str(ROOT),
                check=True,text=True,capture_output=True,
            )
            result = json.loads(out.stdout.strip())
            self.assertEqual(result["terminal_reason"], "LOCK_CONTENDED")
            self.assertFalse((root / "ADAPTER_CALLED").exists())
            self.assertFalse((root / "observer-checkpoint.json").exists())
            self.assertFalse((root / "observer-events.jsonl").exists())
            rt.release_ownership(root, owner)
        finally:
            cleanup(root)
    def test_06_store_runner_is_blocked_by_native_ownership(self):
        root = QUAL / ("runner-store-" + uuid.uuid4().hex)
        root.parent.mkdir(parents=True, exist_ok=True)
        script = (
            "from pathlib import Path; "
            "from tools.obsidian_projection import p5d4_bounded_observer_loop as r; "
            f"root=Path({str(root)!r}); "
            "o=r.acquire_ownership(root,loop_id='native-held',owner_token='native'); "
            "print('READY',flush=True); input(); r.release_ownership(root,o)"
        )
        proc = subprocess.Popen(
            [str(NATIVE),"-B","-c",script],cwd=str(ROOT),
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
        )
        try:
            self.assertEqual(proc.stdout.readline().strip(), "READY")
            plan = rt.make_loop_plan(
                loop_id="store-second",max_cycles=1,max_remote_observations=1,
                max_evaluations=0,max_pending_heads=1,max_consecutive_failures=0,
            )
            calls = {"obs":0,"eval":0}
            def obs(state):
                calls["obs"] += 1
                raise AssertionError("must not observe")
            def ev(*args):
                calls["eval"] += 1
                raise AssertionError("must not evaluate")
            result = rt.run_bounded_loop(
                plan=plan,control_root=root,observation_adapter=obs,evaluation_adapter=ev,
                verified_current_head=None,promotion_evidence=None,
                forbidden_roots=(),owner_token="store-second",
            )
            self.assertEqual(result["terminal_reason"], "LOCK_CONTENDED")
            self.assertEqual(calls, {"obs":0,"eval":0})
            proc.stdin.write("\n"); proc.stdin.flush()
            self.assertEqual(proc.wait(timeout=20), 0, proc.stderr.read())
        finally:
            if proc.poll() is None:
                proc.kill()
            for stream in (proc.stdin,proc.stdout,proc.stderr):
                if stream is not None:
                    stream.close()
            cleanup(root)
    def test_07_checkpoint_and_log_survive_interpreter_change(self):
        root = QUAL / ("restart-state-" + uuid.uuid4().hex)
        try:
            plan = rt.make_loop_plan(
                loop_id="restart",max_cycles=2,max_remote_observations=2,
                max_evaluations=1,max_pending_heads=2,max_consecutive_failures=1,
            )
            state = make_initial_state()
            saved = rt.persist_tick(
                control_root=root,plan=plan,previous_state=state,
                normalized_input=event(state),loop_id=plan["loop_id"],cycle_index=1,
            )
            expected_cp_digest = hashlib.sha256((root/"observer-checkpoint.json").read_bytes()).hexdigest()
            expected_log_digest = hashlib.sha256((root/"observer-events.jsonl").read_bytes()).hexdigest()
            script = (
                "import hashlib,json; from pathlib import Path; "
                "from tools.obsidian_projection import p5d4_bounded_observer_loop as r; "
                f"root=Path({str(root)!r}); "
                "cp=r.load_checkpoint(root); log=r.load_event_log(root); "
                "print(json.dumps({'seq':cp['last_event_sequence'],'events':len(log),"
                "'cp':hashlib.sha256((root/'observer-checkpoint.json').read_bytes()).hexdigest(),"
                "'log':hashlib.sha256((root/'observer-events.jsonl').read_bytes()).hexdigest()},"
                "sort_keys=True,separators=(',',':')))"
            )
            out = subprocess.run(
                [str(NATIVE),"-B","-c",script],cwd=str(ROOT),
                check=True,text=True,capture_output=True,
            )
            observed = json.loads(out.stdout.strip())
            self.assertEqual(observed["seq"], 1)
            self.assertEqual(observed["events"], 1)
            self.assertEqual(observed["cp"], expected_cp_digest)
            self.assertEqual(observed["log"], expected_log_digest)
            self.assertEqual(saved["checkpoint"]["last_event_sequence"], 1)
        finally:
            cleanup(root)

    def test_08_runtime_source_has_no_localappdata_or_store_package_binding(self):
        source = Path(rt.__file__).read_text(encoding="utf-8").lower()
        self.assertNotIn('localappdata") / "atds-obsidian-projection', source)
        self.assertNotIn("pythonsoftwarefoundation.python.3.13_qbz5n2kfra8p0", source)
        self.assertNotIn("localcache\\local\\atds-obsidian-projection", source)

if __name__ == "__main__":
    unittest.main()
