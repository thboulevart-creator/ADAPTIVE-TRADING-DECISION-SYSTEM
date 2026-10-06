from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "tools" / "smf_ap1_m03_02_r1_bootstrap.py"


def run_boot(tmp_path: Path, mode: str):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tmp_path / "nonexistent-pythonpath")
    return subprocess.run(
        [
            sys.executable,
            "-E",
            "-P",
            str(BOOT),
            "--repo-root",
            str(ROOT),
            "--mode",
            mode,
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_old_transport_fails_outside_repo(tmp_path: Path):
    cp = subprocess.run(
        [
            sys.executable,
            "-E",
            "-P",
            "-m",
            "tools.smf_ap1_m03_02_real_execution",
            "--help",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert cp.returncode != 0
    assert "No module named 'tools'" in cp.stderr


def test_bootstrap_imports_exact_modules_without_cwd_or_pythonpath_dependency(tmp_path: Path):
    cp = run_boot(tmp_path, "probe-imports")
    assert cp.returncode == 0, cp.stderr
    payload = json.loads(cp.stdout)
    assert payload["repo_root"] == str(ROOT)
    assert payload["repo_root_explicitly_injected"] is True
    assert payload["implicit_cwd_dependency"] is False
    assert payload["pythonpath_dependency"] is False
    assert payload["sys_path"][0] == str(ROOT)
    assert payload["imports"]["executor"] == "ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
    assert payload["imports"]["binding"] == "ATDS_SMF_AP1_M03_01_BINDING_V0_1"
    assert payload["imports"]["core_has_ecdf_quantiles"] is True


def test_bootstrap_synthetic_m03_uses_exact_binding_and_no_authority(tmp_path: Path):
    cp = run_boot(tmp_path, "probe-synthetic-m03")
    assert cp.returncode == 0, cp.stderr
    payload = json.loads(cp.stdout)
    assert payload["status"] == "PASS"
    assert payload["procedure_ref"].endswith("#ecdf_quantiles")
    assert payload["quantiles"] == {
        "0.5": 2.5,
        "0.9": 3.7,
        "0.95": 3.8499999999999996,
        "0.99": 3.9699999999999998,
    }
    assert all(value is False for value in payload["authority"].values())


def test_bootstrap_rejects_wrong_repo_root(tmp_path: Path):
    cp = subprocess.run(
        [
            sys.executable,
            "-E",
            "-P",
            str(BOOT),
            "--repo-root",
            str(tmp_path),
            "--mode",
            "probe-imports",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert cp.returncode != 0
    assert "REPO_ROOT_MISMATCH" in cp.stderr
