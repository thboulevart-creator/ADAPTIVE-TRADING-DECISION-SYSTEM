import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

from tools.obsidian_projection import p5d4_bounded_observer_loop as rt

ROOT = Path(__file__).resolve().parents[2]
PREREG_REL = "tools/obsidian_projection/p5d4_control_root_binding_remediation_contract_v0_1.json"
PREREG_BLOB = "3f62c901d7e7ac466114780859075489c9163a29"
USERPROFILE = Path(os.environ["USERPROFILE"])
CANONICAL = USERPROFILE / "ATDS-CONTROL" / "OBSIDIAN-PROJECTION" / "P5D4"
QUAL_ANCHOR = USERPROFILE / "ATDS-CONTROL" / "_QUALIFICATION"
NATIVE_PYTHON = Path(os.environ["LOCALAPPDATA"]) / "Python" / "bin" / "python.exe"

def git_blob(relative):
    return subprocess.run(
        ["git","rev-parse",f"HEAD:{relative}"],cwd=str(ROOT),
        check=True,text=True,capture_output=True
    ).stdout.strip()

def cleanup(path):
    shutil.rmtree(path, ignore_errors=True)

class P5D4ControlRootBindingRemediationV01Tests(unittest.TestCase):
    def test_00_preregistration_blob_is_exact(self):
        self.assertEqual(git_blob(PREREG_REL), PREREG_BLOB)

    def test_01_binding_primitive_exists(self):
        self.assertTrue(callable(getattr(rt, "resolve_and_validate_control_root", None)))
        self.assertTrue(callable(getattr(rt, "canonical_production_control_root", None)))

    def test_02_canonical_production_root_is_userprofile_bound_not_appdata(self):
        resolver = rt.canonical_production_control_root
        value = resolver()
        self.assertEqual(os.path.normcase(str(value)), os.path.normcase(str(CANONICAL)))
        lowered = str(value).lower()
        self.assertNotIn("\\appdata\\", lowered)
        self.assertNotIn("\\packages\\", lowered)
        self.assertNotIn("\\localcache\\", lowered)
    def test_03_exact_canonical_root_resolution_is_non_mutating(self):
        existed_before = CANONICAL.exists()
        children_before = (
            sorted(p.name for p in CANONICAL.iterdir())
            if existed_before
            else None
        )
        resolved = rt.resolve_and_validate_control_root(CANONICAL)
        self.assertEqual(
            os.path.normcase(str(resolved)),
            os.path.normcase(str(CANONICAL.resolve(strict=False))),
        )
        self.assertEqual(CANONICAL.exists(), existed_before)
        if existed_before:
            self.assertTrue(CANONICAL.is_dir())
            self.assertFalse(CANONICAL.is_symlink())
            is_junction = getattr(CANONICAL, "is_junction", None)
            if callable(is_junction):
                self.assertFalse(is_junction())
            self.assertEqual(
                sorted(p.name for p in CANONICAL.iterdir()),
                children_before,
            )

    def test_04_old_localappdata_and_store_redirect_roots_are_rejected(self):
        old = Path(os.environ["LOCALAPPDATA"]) / "ATDS-OBSIDIAN-PROJECTION" / "P5D4"
        redirected = (
            Path(os.environ["LOCALAPPDATA"])
            / "Packages"
            / "PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0"
            / "LocalCache"
            / "Local"
            / "ATDS-OBSIDIAN-PROJECTION"
            / "P5D4"
        )
        for candidate in (old, redirected):
            with self.subTest(candidate=str(candidate)):
                with self.assertRaises(rt.ControlRootBindingError):
                    rt.resolve_and_validate_control_root(candidate)

    def test_05_relative_path_is_rejected(self):
        with self.assertRaises(rt.ControlRootBindingError):
            rt.resolve_and_validate_control_root(Path("relative-control-root"))

    @unittest.skipUnless(os.name == "nt", "Windows case semantics")
    def test_06_windows_case_variation_of_exact_canonical_root_is_equivalent(self):
        varied = Path(str(CANONICAL).swapcase())
        resolved = rt.resolve_and_validate_control_root(varied)
        self.assertEqual(os.path.normcase(str(resolved)), os.path.normcase(str(CANONICAL.resolve(strict=False))))
    @unittest.skipUnless(os.name == "nt", "Windows junction semantics")
    def test_07_junction_or_reparse_in_chain_is_rejected(self):
        token = "junction-" + uuid.uuid4().hex
        base = Path(tempfile.gettempdir()) / "atds-p5d4-binding" / token
        target = base / "target"
        junction = base / "junction"
        child = junction / "child"
        try:
            target.mkdir(parents=True)
            subprocess.run(
                ["cmd","/c","mklink","/J",str(junction),str(target)],
                check=True,text=True,capture_output=True
            )
            with self.assertRaises(rt.ControlRootBindingError):
                rt.resolve_and_validate_control_root(child)
        finally:
            if junction.exists():
                subprocess.run(["cmd","/c","rmdir",str(junction)],check=False,capture_output=True)
            cleanup(base)

    def test_08_os_temp_root_remains_allowed_for_synthetic_tests(self):
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / "p5d4"
            resolved = rt.resolve_and_validate_control_root(candidate)
            self.assertEqual(resolved, candidate.resolve(strict=False))

    def test_09_userprofile_qualification_namespace_is_physically_shared_store_native_powershell(self):
        self.assertTrue(NATIVE_PYTHON.is_file())
        root = QUAL_ANCHOR / ("namespace-" + uuid.uuid4().hex)
        marker = root / "store-marker.txt"
        native_marker = root / "native-marker.txt"
        try:
            root.mkdir(parents=True)
            marker.write_text("STORE", encoding="utf-8")
            native = subprocess.run(
                [str(NATIVE_PYTHON),"-c",
                 "from pathlib import Path; import sys; "
                 f"r=Path({str(root)!r}); "
                 f"assert (r/'store-marker.txt').read_text(encoding='utf-8')=='STORE'; "
                 "(r/'native-marker.txt').write_text('NATIVE',encoding='utf-8'); "
                 "print(r.resolve())"],
                check=True,text=True,capture_output=True,cwd=str(ROOT)
            )
            self.assertIn(str(root.resolve()), native.stdout.strip())
            self.assertEqual(native_marker.read_text(encoding="utf-8"), "NATIVE")
            ps = subprocess.run(
                ["powershell","-NoProfile","-Command",
                 f"$r='{str(root)}'; "
                 "if((Get-Content -LiteralPath (Join-Path $r 'store-marker.txt') -Raw) -ne 'STORE'){exit 7}; "
                 "if((Get-Content -LiteralPath (Join-Path $r 'native-marker.txt') -Raw) -ne 'NATIVE'){exit 8}; "
                 "(Resolve-Path -LiteralPath $r).Path"],
                check=True,text=True,capture_output=True
            )
            self.assertEqual(os.path.normcase(ps.stdout.strip()), os.path.normcase(str(root.resolve())))
        finally:
            cleanup(root)
    def test_10_lock_created_by_store_is_seen_by_native_python(self):
        self.assertTrue(NATIVE_PYTHON.is_file())
        root = QUAL_ANCHOR / ("lock-store-" + uuid.uuid4().hex)
        try:
            owner = rt.acquire_ownership(root, loop_id="cross", owner_token="store-owner")
            script = (
                "from pathlib import Path; "
                "from tools.obsidian_projection import p5d4_bounded_observer_loop as rt; "
                f"r=Path({str(root)!r}); "
                "ok=False; "
                "\ntry:\n rt.acquire_ownership(r,loop_id='cross',owner_token='native-owner')"
                "\nexcept rt.OwnershipContended:\n ok=True"
                "\nraise SystemExit(0 if ok else 9)"
            )
            subprocess.run([str(NATIVE_PYTHON),"-c",script],cwd=str(ROOT),check=True)
            rt.release_ownership(root, owner)
        finally:
            cleanup(root)

    def test_11_lock_created_by_native_is_seen_by_store_runtime(self):
        self.assertTrue(NATIVE_PYTHON.is_file())
        root = QUAL_ANCHOR / ("lock-native-" + uuid.uuid4().hex)
        root.parent.mkdir(parents=True, exist_ok=True)
        script = (
            "from pathlib import Path; "
            "from tools.obsidian_projection import p5d4_bounded_observer_loop as rt; "
            f"r=Path({str(root)!r}); "
            "o=rt.acquire_ownership(r,loop_id='cross',owner_token='native-owner'); "
            "print('READY',flush=True); "
            "input(); "
            "rt.release_ownership(r,o)"
        )
        proc = subprocess.Popen(
            [str(NATIVE_PYTHON),"-c",script],cwd=str(ROOT),
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            text=True
        )
        try:
            self.assertEqual(proc.stdout.readline().strip(), "READY")
            with self.assertRaises(rt.OwnershipContended):
                rt.acquire_ownership(root, loop_id="cross", owner_token="store-owner")
            proc.stdin.write("\n"); proc.stdin.flush()
            self.assertEqual(proc.wait(timeout=20), 0, proc.stderr.read())
        finally:
            if proc.poll() is None:
                proc.kill()
            cleanup(root)
    def test_12_restart_with_interpreter_change_reads_same_control_state(self):
        self.assertTrue(NATIVE_PYTHON.is_file())
        root = QUAL_ANCHOR / ("restart-" + uuid.uuid4().hex)
        try:
            owner = rt.acquire_ownership(root, loop_id="restart", owner_token="store-owner")
            rt.release_ownership(root, owner)
            marker = root / "cross-interpreter-checkpoint.marker"
            marker.write_text("VISIBLE", encoding="utf-8")
            script = (
                "from pathlib import Path; "
                f"p=Path({str(marker)!r}); "
                "assert p.read_text(encoding='utf-8')=='VISIBLE'; "
                "print(p.resolve())"
            )
            native = subprocess.run(
                [str(NATIVE_PYTHON),"-c",script],check=True,text=True,
                capture_output=True,cwd=str(ROOT)
            )
            self.assertEqual(
                os.path.normcase(native.stdout.strip()),
                os.path.normcase(str(marker.resolve()))
            )
        finally:
            cleanup(root)

if __name__ == "__main__":
    unittest.main()
