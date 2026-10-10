"""Bounded, human-authorized M2-R1 policy tests. No trading or provider calls."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "tools/fc01_f03_cr2/m2_r1"
CANDIDATE = HERE / "memory_policy.py"
FROZEN = ROOT / "GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-QUALIFICATION-FREEZE-V0.1.json"
CR2_SOURCE = HERE / "F03CR2SupervisorM2.cs"
CR2_WORKER = ROOT / "tools/fc01_f03_cr2/SyntheticHistoryWorker.java"
CR2_CHILD = ROOT / "tools/fc01_f03_cr2/F03CR2SyntheticChild.cs"
RECOVERY = ROOT / "tools/fc01_f03_cr2/F03CR2Recovery.cs"
RUNTIME = Path.home() / "ATDS-TOOLS/jforex-runtime-v0.1/jdk8/jdk8u504-b01/bin"
API = Path.home() / ".m2/repository/com/dukascopy/api/JForex-API/2.13.99/JForex-API-2.13.99.jar"
CSC = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Microsoft.NET/Framework64/v4.0.30319/csc.exe"


@pytest.fixture(scope="module")
def freeze():
    obj = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert obj["limits"]["max_supervised_worker_launches"] == 24
    assert obj["limits"]["planned_direct_worker_launches"] == 13
    assert obj["outcomes"]["existing_F03_CR2"] == "BLOCKED"
    assert obj["outcomes"]["peak_internal_root_cause"] == "NOT_PROVEN"
    assert set(obj["scenarios"]) == {"MS-" + str(i).zfill(2) for i in range(1, 21)}
    return obj


@pytest.fixture(scope="module")
def engine(freeze):
    if not CANDIDATE.is_file():
        return None
    spec = importlib.util.spec_from_file_location("m2_memory_policy", CANDIDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DEFAULT = {
    "job_configured": True, "job_limit_bytes": 268435456,
    "job_readback_bytes": 268435456, "assigned_before_resume": True,
    "descendants_confined": True, "current_commit_bytes": 50000000,
    "peak_job_memory_bytes": 50000000, "memory_error": None,
    "termination_confirmed": True, "tree_terminated": True,
    "timeout": False, "publication_after_failure": False,
    "collision": False, "recovery_complete": True,
    "supervisor_crash": False, "unexplained_peak": False,
}


CASES = {
    "MS-01": ({}, "CONTINUE_ELIGIBLE"),
    "MS-02": ({"job_configured": False}, "BLOCKED_JOB_LIMIT"),
    "MS-03": ({"job_readback_bytes": 267000000}, "BLOCKED_JOB_LIMIT"),
    "MS-04": ({"assigned_before_resume": False}, "BLOCKED_JOB_ASSIGNMENT"),
    "MS-05": ({"descendants_confined": False, "timeout": True}, "BLOCKED_PROCESS_TREE"),
    "MS-06": ({"current_commit_bytes": 90000000}, "CONTINUE_ELIGIBLE"),
    "MS-07": ({"memory_error": "NATIVE_COMMIT_DENIED", "peak_job_memory_bytes": 286000000}, "MEMORY_FAILURE"),
    "MS-08": ({"memory_error": "JAVA_OUT_OF_MEMORY"}, "MEMORY_FAILURE"),
    "MS-09": ({"current_commit_bytes": None}, "BLOCKED_OBSERVABILITY"),
    "MS-10": ({"current_commit_bytes": 268435457}, "BLOCKED_LIMIT_INTEGRITY"),
    "MS-11": ({"memory_error": "NATIVE_COMMIT_DENIED", "peak_job_memory_bytes": 286000000}, "MEMORY_FAILURE"),
    "MS-12": ({"unexplained_peak": True, "peak_job_memory_bytes": 286000000}, "BLOCKED_UNEXPLAINED_MEMORY_ANOMALY"),
    "MS-13": ({"timeout": True}, "BLOCKED_TIMEOUT"),
    "MS-14": ({"memory_error": "JAVA_OUT_OF_MEMORY", "termination_confirmed": False}, "BLOCKED_TERMINATION_NOT_PROVEN"),
    "MS-15": ({"tree_terminated": False, "timeout": True}, "BLOCKED_PROCESS_TREE"),
    "MS-16": ({"memory_error": "NATIVE_COMMIT_DENIED", "publication_after_failure": True}, "CRITICAL_FAIL"),
    "MS-17": ({"collision": True}, "BLOCKED_COLLISION"),
    "MS-18": ({"memory_error": "JAVA_OUT_OF_MEMORY", "recovery_complete": False}, "BLOCKED_RECOVERY"),
    "MS-19": ({"supervisor_crash": True, "recovery_complete": True}, "ORPHAN_RECOVERED"),
    "MS-20": ({}, "CONTINUE_ELIGIBLE"),
}


@pytest.mark.parametrize("sid", list(CASES))
def test_ms_policy_scenario(engine, sid):
    assert engine is not None, "RED: separate, bounded M2-R1 policy evaluator absent"
    diff, expected = CASES[sid]
    packet = {**DEFAULT, **diff}
    result = engine.evaluate(packet)
    assert result["decision"] == expected, (sid, packet, result)
    assert result["peak_job_memory_used"] == packet["peak_job_memory_bytes"]
    assert result["primary_control"] == "OS_ENFORCED_JOB_COMMIT_LIMIT"
    assert result["observation"] == "CURRENT_JOB_COMMITTED_MEMORY"


@pytest.fixture(scope="module")
def offline_built(freeze, tmp_path_factory):
    if not engine_exists_or_red():
        return None  # RED must fail explicitly in the test body, not fixture setup
    assert CSC.is_file() and (RUNTIME / "java.exe").is_file()
    assert (RUNTIME / "javac.exe").is_file() and API.is_file()
    temp = tmp_path_factory.mktemp("m2r1_offline_build")
    targets = [(CR2_SOURCE, temp/"F03CR2Supervisor.exe"),
               (CR2_CHILD, temp/"F03CR2SyntheticChild.exe"),
               (RECOVERY, temp/"F03CR2Recovery.exe")]
    for source, exe in targets:
        p = subprocess.run([str(CSC), "/nologo", "/target:exe", "/out:"+str(exe), str(source)],
                           capture_output=True, text=True, timeout=40)
        assert p.returncode == 0, (source, p.stdout, p.stderr)
    classes = temp / "classes"
    classes.mkdir()
    p = subprocess.run([str(RUNTIME/"javac.exe"), "-encoding", "UTF-8", "-cp",
                        str(API), "-d", str(classes), str(CR2_WORKER)],
                       capture_output=True, text=True, timeout=40)
    assert p.returncode == 0, (p.stdout, p.stderr)
    return temp/"F03CR2Supervisor.exe", temp/"F03CR2Recovery.exe", os.pathsep.join((str(classes),str(API)))


def engine_exists_or_red():
    return CANDIDATE.is_file()


def record_launch(audit, scenario):
    with open(audit, "a", encoding="utf-8") as out:
        out.write(scenario + "\n")


def invocation(exe, cp, mode, folder):
    return [str(exe), str(RUNTIME/"java.exe"), cp, mode, str(folder)]


def read_result(result):
    return dict(line.split("=",1) for line in result.stdout.splitlines() if "=" in line)


def test_windows_job_policy_adapters(freeze, engine, offline_built, tmp_path):
    """Exactly 13 synthetic supervised launches; no retries or provider traffic."""
    assert engine is not None and offline_built is not None, "RED: bounded Windows adapter absent"
    exe, recovery, cp = offline_built
    audit = tmp_path / "m2r1_launch_ledger.txt"

    def run(name, mode, prep=None):
        directory = tmp_path / name
        directory.mkdir()
        if prep:
            prep(directory)
        record_launch(audit, name + ":" + mode)
        result = subprocess.run(invocation(exe,cp,mode,directory),
                                capture_output=True,text=True,timeout=17)
        return directory,result,read_result(result)

    # 1,2: repeated normal execution and byte-for-byte determinism.
    first = run("normal_A","valid")
    second = run("normal_B","valid")
    for folder,p,obs in [first,second]:
        assert p.returncode == 0 and obs["RESULT"] == "PUBLISHED"
        assert obs["JOB_ASSIGNED_BEFORE_RESUME"] == "TRUE"
        assert obs["JOB_LIMIT_READBACK_BYTES"] == "268435456"
        assert 0 <= int(obs["M2_CURRENT_JOB_COMMIT_BYTES"]) <= 268435456
        assert int(obs["M2_DIAGNOSTIC_PEAK_BYTES"]) >= 0
        bound = engine.evaluate({**DEFAULT,
             "current_commit_bytes": int(obs["M2_CURRENT_JOB_COMMIT_BYTES"]),
             "peak_job_memory_bytes": int(obs["M2_DIAGNOSTIC_PEAK_BYTES"])})
        assert bound["decision"] == "CONTINUE_ELIGIBLE"
        assert not list(folder.glob("cr2_*"))
    assert (first[0]/"final.csv").read_bytes() == (second[0]/"final.csv").read_bytes()

    # 3: JVM OutOfMemoryError under OS Job limit, no final output.
    folder,p,obs=run("java_oom","oom")
    assert p.returncode != 0 and obs["RESULT"] == "BLOCKED_MEMORY"
    assert 0 <= int(obs["M2_CURRENT_JOB_COMMIT_BYTES"]) <= 268435456
    observed_failure = engine.evaluate({**DEFAULT,
        "current_commit_bytes": int(obs["M2_CURRENT_JOB_COMMIT_BYTES"]),
        "peak_job_memory_bytes": int(obs["M2_DIAGNOSTIC_PEAK_BYTES"]),
        "memory_error": "JAVA_OUT_OF_MEMORY"})
    assert observed_failure["decision"] == "MEMORY_FAILURE"
    assert not (folder/"final.csv").exists() and not list(folder.glob("cr2_*"))

    # 4,5: forced timeout and confined descendant; positive termination evidence.
    for name,mode in [("timeout","hang"),("child_confined","child_hang")]:
        folder,p,obs=run(name,mode)
        assert p.returncode != 0 and obs["RESULT"] == "BLOCKED_TIMEOUT", obs
        assert obs["JOB_ASSIGNED_BEFORE_RESUME"] == "TRUE"
        if mode=="child_hang":
            assert obs["CHILD_STARTED_BEFORE_TERMINATION"]=="True"
            assert obs["CHILD_TERMINATED"]=="True"
        assert not (folder/"final.csv").exists() and not list(folder.glob("cr2_*"))

    # 6: existing final retained with no-replace collision.
    folder,p,obs=run("sentinel","valid",lambda d:(d/"final.csv").write_bytes(b"FROZEN_SENTINEL"))
    assert obs["RESULT"]=="BLOCKED_COLLISION" and p.returncode != 0
    assert (folder/"final.csv").read_bytes()==b"FROZEN_SENTINEL"

    # 7: kill supervisor mid synthetic partial, recover using independently compiled CR2 recovery.
    crashdir=tmp_path/"supervisor_crash"
    crashdir.mkdir()
    record_launch(audit,"supervisor_crash:pause_after_partial")
    proc=subprocess.Popen(invocation(exe,cp,"pause_after_partial",crashdir),
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        witnessed=False
        for _ in range(6):
            line=proc.stdout.readline()
            if "JOB_ASSIGNED_BEFORE_RESUME=TRUE" in line:
                witnessed=True
                break
        assert witnessed
        until=time.monotonic()+1.5
        while time.monotonic()<until:
            orphans=list(crashdir.glob("cr2_*"))
            if orphans and (orphans[0]/"worker.partial").is_file():
                break
            time.sleep(0.03)
        assert orphans and (orphans[0]/"worker.partial").is_file()
        proc.kill()
        proc.wait(timeout=5)
        # Re-invoke a separate recovery program, not pytest cleanup.
        deadline=time.monotonic()+2
        while True:
            recovered=subprocess.run([str(recovery),str(crashdir),orphans[0].name],
                                     capture_output=True,text=True,timeout=5)
            if "RESULT=ORPHAN_RECOVERED" in recovered.stdout or time.monotonic()>deadline:
                break
            time.sleep(0.04)
        assert recovered.returncode==0 and "RESULT=ORPHAN_RECOVERED" in recovered.stdout
        assert not orphans[0].exists()
        assert not (crashdir/"final.csv").exists()
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)

    # 8..13: six simultaneous publishers, exactly one valid final. No overwrite.
    race=tmp_path/"race"
    race.mkdir()
    processes=[]
    for idx in range(6):
        record_launch(audit,"race_"+str(idx)+":valid")
        processes.append(subprocess.Popen(invocation(exe,cp,"valid",race),
                      stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True))
    outcomes=[]
    for process in processes:
        stdout,stderr=process.communicate(timeout=18)
        outcomes.append((process.returncode,stdout,stderr))
    assert sum("RESULT=PUBLISHED" in x[1] for x in outcomes)==1
    assert sum("RESULT=BLOCKED_COLLISION" in x[1] for x in outcomes)==5, outcomes
    assert (race/"final.csv").is_file()
    assert not list(race.glob("cr2_*"))

    events=audit.read_text(encoding="utf-8").splitlines()
    assert len(events)==13, events
    assert len(events)<=freeze["limits"]["max_supervised_worker_launches"]
    assert len(events)==freeze["limits"]["planned_direct_worker_launches"]
    # Store the audit in pytest sandbox, included in receipt snapshot after GREEN.
    print("M2_R1_LAUNCH_AUDIT=" + str(audit))
    print("M2_R1_LAUNCH_COUNT="+str(len(events)))


def test_policy_source_has_no_real_provider_entrypoints(engine):
    assert engine is not None, "RED: policy implementation absent"
    src=CANDIDATE.read_text(encoding="utf-8")
    assert "ClientFactory" not in src and "connect(" not in src
    assert "MetaTrader" not in src and "sendOrder" not in src
