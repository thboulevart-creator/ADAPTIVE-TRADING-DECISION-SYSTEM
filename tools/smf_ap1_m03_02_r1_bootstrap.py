from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
from pathlib import Path

SCHEMA = "ATDS_SMF_AP1_M03_02_R1_TRANSPORT_BOOTSTRAP_V0_1"
TARGET_MODULE = "tools.smf_ap1_m03_02_real_execution"

def _repo_root(value: str) -> Path:
    repo = Path(value).expanduser().resolve(strict=True)
    expected = Path(__file__).resolve().parents[1]
    if repo != expected:
        raise SystemExit("REPO_ROOT_MISMATCH")
    return repo

def _inject(repo: Path) -> None:
    repo_s = str(repo)
    if repo_s in sys.path:
        sys.path.remove(repo_s)
    sys.path.insert(0, repo_s)

def _base_observation(repo: Path) -> dict:
    return {
        "schema": SCHEMA,
        "repo_root": str(repo),
        "repo_root_explicitly_injected": sys.path[0] == str(repo),
        "implicit_cwd_dependency": False,
        "pythonpath_dependency": False,
        "cwd": os.getcwd(),
        "sys_executable": sys.executable,
        "sys_path": list(sys.path),
        "python_flags": ["-E", "-P"],
    }

def _probe_imports(repo: Path) -> int:
    _inject(repo)
    import tools.smf_ap1_m03_02_real_execution as real
    import src.smf_ap1_m03_binding as binding
    import tools.smf03_core_foundation as core
    payload = {
        **_base_observation(repo),
        "mode": "probe-imports",
        "imports": {
            "executor": real.CONTRACT,
            "binding": binding.CONTRACT,
            "core_has_ecdf_quantiles": hasattr(core, "ecdf_quantiles"),
        },
    }
    print(json.dumps(payload, sort_keys=True))
    return 0

def _probe_synthetic(repo: Path) -> int:
    _inject(repo)
    from src.smf_ap1_m03_binding import create_m03_activation, execute_m03_observations
    activation = create_m03_activation(result_exposed=False)
    result = execute_m03_observations(
        [1.0, 2.0, 3.0, 4.0],
        metric="minute_range",
        bucket_id="SYNTHETIC_R1",
        activation=activation,
    )
    expected = {"0.5": 2.5, "0.9": 3.7, "0.95": 3.8499999999999996, "0.99": 3.9699999999999998}
    ok = result["quantiles"] == expected and result["procedure_ref"].endswith("#ecdf_quantiles")
    payload = {
        **_base_observation(repo),
        "mode": "probe-synthetic-m03",
        "status": "PASS" if ok else "FAIL",
        "procedure_ref": result["procedure_ref"],
        "quantiles": result["quantiles"],
        "authority": result["authority"],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if ok and all(v is False for v in result["authority"].values()) else 2

def _execute(repo: Path, forwarded: list[str]) -> int:
    _inject(repo)
    sys.argv = [TARGET_MODULE, *forwarded]
    runpy.run_module(TARGET_MODULE, run_name="__main__", alter_sys=True)
    return 0

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True)
    p.add_argument("--mode", choices=("probe-imports", "probe-synthetic-m03", "execute"), required=True)
    p.add_argument("forwarded", nargs=argparse.REMAINDER)
    ns = p.parse_args()
    repo = _repo_root(ns.repo_root)
    if ns.mode == "probe-imports":
        return _probe_imports(repo)
    if ns.mode == "probe-synthetic-m03":
        return _probe_synthetic(repo)
    forwarded = list(ns.forwarded)
    if forwarded[:1] == ["--"]:
        forwarded = forwarded[1:]
    return _execute(repo, forwarded)

if __name__ == "__main__":
    raise SystemExit(main())
