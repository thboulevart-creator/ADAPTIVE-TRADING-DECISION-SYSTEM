from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import p1_12c_qualified_producer_execution as p12c
from tools import p1_12c_sandbox_runner as runner
from tests.p1_21_fixture import build_real_capability_case

ROOT = Path(__file__).resolve().parents[1]
AP1 = ROOT / "tools" / "ap1_intraday_spread_census.py"
RUNNER = ROOT / "tools" / "p1_12c_sandbox_runner.py"


def test_rvo08f_profile_binds_runtime_python_flags(tmp_path: Path):
    profile = build_real_capability_case(tmp_path)["invocation_profile"]
    schema = json.loads(profile.child_argv_schema_json)
    assert schema["python_flags"] == ["-E", "-P"]


def test_rvo08f_real_runner_command_uses_bounded_nonisolated_flags(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    cmd = p12c.build_ap1_runner_command(
        case["plan"],
        case["invocation_profile"],
        python_executable="BOUND_PYTHON_BINARY",
        runner_path=RUNNER,
        producer_path=AP1,
    )
    assert cmd[0] == "BOUND_PYTHON_BINARY"
    assert cmd[1:3] == ("-E", "-P")
    assert "-I" not in cmd[:4]


class _Lib:
    def __init__(self, name: str):
        self._name = name


def test_rvo08f_sandbox_allows_only_observed_local_runtime_events():
    runner._audit("ctypes.dlopen", ("kernel32",))
    runner._audit("ctypes.dlopen", ("user32",))
    runner._audit("ctypes.dlopen", ("tzres.dll",))
    runner._audit("ctypes.dlsym", (_Lib("kernel32"), "GetLastError"))
    runner._audit("ctypes.dlsym", (_Lib("user32"), "LoadStringW"))
    runner._audit("socket.gethostname", ())


@pytest.mark.parametrize(
    ("event", "args"),
    [
        ("subprocess.Popen", ("cmd.exe",)),
        ("socket.__new__", ()),
        ("socket.connect", ()),
        ("ctypes.dlopen", ("RVO08F_NOT_ALLOWED.dll",)),
        ("ctypes.dlsym", (_Lib("kernel32"), "CreateProcessW")),
    ],
)
def test_rvo08f_sandbox_keeps_escape_events_blocked(event, args):
    with pytest.raises(RuntimeError, match="P1_12C_SANDBOX_FORBIDDEN_EVENT"):
        runner._audit(event, args)
