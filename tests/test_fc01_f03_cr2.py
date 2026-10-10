"""F03-CR2 offline synthetic RED; production FC01 and provider are forbidden."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "tools" / "fc01_f03_cr2"
PARAM = ROOT / "GOVERNANCE" / "AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-PARAMETER-PACKET-V0.1.json"
C_SHARP = HERE / "F03CR2Supervisor.cs"
JAVA_SRC = HERE / "SyntheticHistoryWorker.java"
JAVAC = Path.home() / "ATDS-TOOLS/jforex-runtime-v0.1/jdk8/jdk8u504-b01/bin/javac.exe"
JAVA = Path.home() / "ATDS-TOOLS/jforex-runtime-v0.1/jdk8/jdk8u504-b01/bin/java.exe"
CSC = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Microsoft.NET/Framework64/v4.0.30319/csc.exe"
API = Path.home() / ".m2/repository/com/dukascopy/api/JForex-API/2.13.99/JForex-API-2.13.99.jar"


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    if not C_SHARP.is_file() or not JAVA_SRC.is_file():
        return None  # test bodies fail RED explicitly, not fixture errors
    cfg = json.loads(PARAM.read_text(encoding="utf-8"))
    assert cfg["memory"]["job_memory_limit_bytes"] == 268435456
    assert cfg["memory"]["jvm_max_heap_bytes"] == 134217728
    assert cfg["timeout"]["hard_timeout_ms"] == 2000
    assert CSC.is_file() and JAVAC.is_file() and JAVA.is_file() and API.is_file()
    path = tmp_path_factory.mktemp("fc01_cr2_offline_build")
    output = path / "F03CR2Supervisor.exe"
    result = subprocess.run([str(CSC), "/nologo", "/target:exe", "/out:" + str(output),
                             str(C_SHARP)], capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stdout + result.stderr
    child_source = HERE / "F03CR2SyntheticChild.cs"
    child_exe = path / "F03CR2SyntheticChild.exe"
    result = subprocess.run([str(CSC), "/nologo", "/target:exe", "/out:" + str(child_exe),
                             str(child_source)], capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stdout + result.stderr
    classes = path / "classes"
    classes.mkdir()
    result = subprocess.run([str(JAVAC), "-encoding", "UTF-8", "-cp", str(API),
                             "-d", str(classes), str(JAVA_SRC)],
                            capture_output=True, text=True, timeout=45)
    assert result.returncode == 0, result.stdout + result.stderr
    return output, os.pathsep.join([str(classes), str(API)])


def run_case(built, path, mode, timeout=15):
    assert built is not None, "RED: isolated supervisor/worker behavior absent"
    exe, classpath = built
    result = subprocess.run([str(exe), str(JAVA), classpath, mode, str(path)],
                            capture_output=True, text=True, timeout=timeout)
    data = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    return result, data


@pytest.mark.parametrize("mode,expected", [
    ("valid", "PUBLISHED"),
    ("null", "BLOCKED_HISTORY_LOAD_NULL"),
    ("empty", "BLOCKED_EMPTY"),
    ("invalid_price", "BLOCKED_TICK_VALIDATION"),
    ("out_of_order", "BLOCKED_SOURCE_ORDERING"),
    ("write_failure", "BLOCKED_OUTPUT_WRITE"),
    ("oom", "BLOCKED_MEMORY"),
    ("hang", "BLOCKED_TIMEOUT"),
    ("child_hang", "BLOCKED_TIMEOUT"),
    ("crash", "BLOCKED_WORKER"),
])
def test_worker_fail_closed(built, tmp_path, mode, expected):
    result, data = run_case(built, tmp_path, mode)
    assert data.get("RESULT") == expected, (result.returncode, result.stdout, result.stderr)
    assert data.get("JOB_ASSIGNED_BEFORE_RESUME") == "TRUE"
    assert data.get("JOB_LIMIT_READBACK_BYTES") == "268435456"
    assert data.get("PARAMETER_FREEZE_VERIFIED") == "TRUE"
    final = tmp_path / "final.csv"
    assert final.is_file() == (mode == "valid")
    assert not (tmp_path / "worker.partial").exists()
    assert not list(tmp_path.glob("cr2_*")), "Run directory or file residue after supervised exit"
    if mode == "child_hang":
        assert data.get("CHILD_STARTED_BEFORE_TERMINATION") == "True", data
    if mode == "valid":
        raw = final.read_bytes()
        assert raw == (
            b"timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
            b"2026-10-08T08:00:00.001Z,25000.5,25000.0,1.25,1.5\n"
        )
        assert data.get("SHA256") == hashlib.sha256(raw).hexdigest()
        assert result.returncode == 0
    else:
        assert result.returncode != 0


def test_preexisting_final_never_replaced(built, tmp_path):
    target = tmp_path / "final.csv"
    target.write_bytes(b"FROZEN_SENTINEL")
    result, data = run_case(built, tmp_path, "valid")
    assert data.get("RESULT") == "BLOCKED_COLLISION", result.stdout
    assert target.read_bytes() == b"FROZEN_SENTINEL"
    assert not (tmp_path / "worker.partial").exists()
    assert not list(tmp_path.glob("cr2_*"))


def test_concurrent_publishers_only_one_winner(built, tmp_path):
    assert built is not None, "RED: concurrent no-replace publisher absent"
    exe, cp = built
    cmds = [[str(exe), str(JAVA), cp, "valid", str(tmp_path)] for _ in range(6)]
    procs = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for cmd in cmds]
    outputs = [p.communicate(timeout=20)[0] for p in procs]
    wins = [out for out in outputs if "RESULT=PUBLISHED" in out]
    assert len(wins) == 1, outputs
    assert (tmp_path / "final.csv").is_file()
    assert not list(tmp_path.glob("cr2_*"))


def test_no_network_or_real_provider_entrypoints():
    assert C_SHARP.is_file() and JAVA_SRC.is_file()
    code = C_SHARP.read_text(encoding="utf-8") + JAVA_SRC.read_text(encoding="utf-8")
    assert "ClientFactory" not in code
    assert "client.connect(" not in code
    assert "getDefaultInstance()" not in code
    assert "JFOREX_USER" not in code and "JFOREX_PASSWORD" not in code
    assert "getTicks(" in code
    assert "CreateHardLink" in code
    assert "TerminateJobObject" in code
    assert "AssignProcessToJobObject" in code


def test_exact_immutable_fc01_contract():
    data = json.loads(PARAM.read_text(encoding="utf-8"))
    assert data["bindings"] == {
        "instrument": "USATECH.IDX/USD",
        "from_ms": 1791446400000,
        "to_ms_inclusive": 1791449999999,
        "environment": "DEMO_NOT_CONNECTED",
        "csv_header": "timestamp,askPrice,bidPrice,askVolume,bidVolume",
    }
    assert data["firewall"]["provider_requests"] == 0
    assert data["firewall"]["b12"] == "CLOSED"
    assert not data["operational_adoption"]


def test_real_fc01_collector_unchanged():
    filename = ROOT / "tools/jforex_fc01_jf02/src/main/java/atds/fc01jf02/FC01JF02HistoryRead.java"
    src = filename.read_text(encoding="utf-8")
    assert "context.getHistory().readTicks(" in src
    assert "ClientFactory.getDefaultInstance()" in src


def test_memory_counter_anomaly_must_remain_visible():
    data = json.loads(PARAM.read_text(encoding="utf-8"))
    assert data["memory"]["peak_job_metric"].startswith("UNRESOLVED_FROM_CR1")


def test_replay_is_byte_deterministic(built, tmp_path):
    records = []
    for i in range(3):
        directory = tmp_path / ("replay_" + str(i))
        directory.mkdir()
        result, data = run_case(built, directory, "valid")
        assert result.returncode == 0 and data["RESULT"] == "PUBLISHED"
        records.append((data["SHA256"], (directory / "final.csv").read_bytes()))
        assert not list(directory.glob("cr2_*"))
    assert records[0] == records[1] == records[2]


def test_out_of_sandbox_path_rejected(built):
    exe, cp = built
    result = subprocess.run([str(exe), str(JAVA), cp, "valid", str(ROOT)],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode != 0
    assert "RESULT=BLOCKED_P0_ENVIRONMENT" in result.stdout


def test_supervisor_death_terminates_worker_job(built, tmp_path):
    import ctypes
    import shutil
    import time
    exe, cp = built
    process = subprocess.Popen([str(exe), str(JAVA), cp, "hang", str(tmp_path)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pid = None
    assigned = False
    try:
        for _ in range(9):
            line = process.stdout.readline()
            if line.startswith("WORKER_PID="):
                pid = int(line.partition("=")[2])
            if line.startswith("JOB_ASSIGNED_BEFORE_RESUME=TRUE"):
                assigned = True
                break
        assert assigned and pid is not None, "Supervisor did not establish job membership"
        process.kill()
        process.wait(timeout=5)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        handle = kernel.OpenProcess(0x00100000, 0, pid)
        if handle:
            kernel.WaitForSingleObject.restype = ctypes.c_ulong
            state = kernel.WaitForSingleObject(handle, 3000)
            kernel.CloseHandle(handle)
            assert state == 0, "Worker survived supervisor termination"
        else:
            assert ctypes.get_last_error() == 87, "Unable to prove worker termination"
        assert not (tmp_path / "final.csv").exists()
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        # Only clean this pytest-owned sandbox. Production recovery remains unqualified.
        for directory in tmp_path.glob("cr2_*"):
            shutil.rmtree(directory, ignore_errors=True)
