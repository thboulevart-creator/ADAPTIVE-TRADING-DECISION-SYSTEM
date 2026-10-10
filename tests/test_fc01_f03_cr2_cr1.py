"""CR2-CR1 bounded orphan recovery RED tests; no network/provider."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import uuid
import pytest

ROOT=Path(__file__).resolve().parents[1]
CODE=ROOT/"tools/fc01_f03_cr2/F03CR2Recovery.cs"
CSC=Path(os.environ.get("WINDIR",r"C:\Windows"))/"Microsoft.NET/Framework64/v4.0.30319/csc.exe"
FREEZE=ROOT/"GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-TEST-FREEZE-V0.1.json"
FIELDS=("RUN_ID","RUN_DIR","SUPERVISOR_PID","WORKER_PID","WORKER_START_TICKS","FINAL_PATH","EXPECTED_SHA256")

@pytest.fixture(scope="session")
def recovered(tmp_path_factory):
    if not CODE.exists():
        return None
    target=tmp_path_factory.mktemp("cr2_cr1_build")/"F03CR2Recovery.exe"
    p=subprocess.run([str(CSC),"/nologo","/target:exe","/out:"+str(target),str(CODE)],
                     capture_output=True,text=True,timeout=35)
    assert p.returncode==0,(p.stdout,p.stderr)
    return target

def manifest(lab,pid=4294967290,foreign=False,final=False,tamper=False,readonly=False):
    runid="cr2_"+uuid.uuid4().hex
    sub=lab/runid
    sub.mkdir()
    target=lab/"final.csv"
    if final: target.write_bytes(b"DO_NOT_TOUCH_VALID_FINAL")
    (sub/"worker.partial").write_bytes(b"PRIVATE_UNPUBLISHED")
    if foreign: (sub/"foreign.dat").write_bytes(b"PRESERVE")
    if readonly:
        (sub/"worker.partial").chmod(0o444)
    data={
      "RUN_ID":runid,"RUN_DIR":str(sub),"SUPERVISOR_PID":"0",
      "WORKER_PID":str(pid),"WORKER_START_TICKS":"0","FINAL_PATH":str(target),
      "EXPECTED_SHA256":hashlib.sha256(b"PRIVATE_UNPUBLISHED").hexdigest()
    }
    body="".join(k+"="+data[k]+"\n" for k in FIELDS)
    digest=hashlib.sha256(body.encode("utf-8")).hexdigest()
    if tamper: digest="0"*64
    (sub/"run.manifest").write_text(body+"MANIFEST_SHA256="+digest+"\n",encoding="utf-8",newline="\n")
    return sub,target

def call(exe,lab,run):
    assert exe is not None,"RED: independent CR2 orphan recovery executable missing"
    p=subprocess.run([str(exe),str(lab),run.name],
                     capture_output=True,text=True,timeout=8)
    return p,dict(line.split("=",1) for line in p.stdout.splitlines() if "=" in line)

def test_orphan_recovered_without_pytest_cleanup(recovered,tmp_path):
    run,final=manifest(tmp_path)
    p,j=call(recovered,tmp_path,run)
    assert p.returncode==0,(p.stdout,p.stderr)
    assert j["RESULT"]=="ORPHAN_RECOVERED"
    assert not run.exists()
    assert not final.exists()

def test_active_worker_protected(recovered,tmp_path):
    run,final=manifest(tmp_path,pid=os.getpid())
    p,j=call(recovered,tmp_path,run)
    assert p.returncode!=0
    assert j["RESULT"]=="BLOCKED_ACTIVE_OR_UNVERIFIED_WORKER"
    assert (run/"worker.partial").exists()

def test_foreign_artifact_protected(recovered,tmp_path):
    run,final=manifest(tmp_path,foreign=True)
    p,j=call(recovered,tmp_path,run)
    assert p.returncode!=0 and j["RESULT"]=="BLOCKED_FOREIGN_ARTIFACT"
    assert (run/"foreign.dat").read_bytes()==b"PRESERVE"

def test_valid_final_preserved(recovered,tmp_path):
    run,final=manifest(tmp_path,final=True)
    p,j=call(recovered,tmp_path,run)
    assert p.returncode==0 and j["RESULT"]=="ORPHAN_RECOVERED"
    assert final.read_bytes()==b"DO_NOT_TOUCH_VALID_FINAL"

def test_idempotent_recovery(recovered,tmp_path):
    run,_=manifest(tmp_path)
    p,j=call(recovered,tmp_path,run)
    assert j["RESULT"]=="ORPHAN_RECOVERED"
    p2,j2=call(recovered,tmp_path,run)
    assert p2.returncode==0 and j2["RESULT"]=="NO_ORPHAN"

def test_concurrent_recovery(recovered,tmp_path):
    run,_=manifest(tmp_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        answers=list(pool.map(lambda _i:call(recovered,tmp_path,run),range(4)))
    results=[x[1].get("RESULT") for x in answers]
    assert results.count("ORPHAN_RECOVERED")==1,results
    assert all(k in ("ORPHAN_RECOVERED","NO_ORPHAN","BLOCKED_BUSY") for k in results)
    assert not run.exists()

def test_readonly_cleanup_failure_preserves_manifest(recovered,tmp_path):
    run,_=manifest(tmp_path,readonly=True)
    p,j=call(recovered,tmp_path,run)
    assert p.returncode!=0
    assert j["RESULT"]=="BLOCKED_CLEANUP_DENIED"
    assert (run/"run.manifest").is_file()

def test_manifest_tamper_rejected(recovered,tmp_path):
    run,_=manifest(tmp_path,tamper=True)
    p,j=call(recovered,tmp_path,run)
    assert p.returncode!=0 and j["RESULT"]=="BLOCKED_MANIFEST_INTEGRITY"
    assert (run/"worker.partial").is_file()

def test_out_of_root_rejected(recovered,tmp_path):
    other=tmp_path/"other"
    other.mkdir()
    run,_=manifest(other)
    p,j=call(recovered,tmp_path,run)
    assert p.returncode==0 and j["RESULT"]=="NO_ORPHAN"
    assert (run/"worker.partial").exists()

def test_freeze_identity():
    j=json.loads(FREEZE.read_text(encoding="utf-8"))
    assert j["baseline_head"]=="2ab0975dfab3ec2124f506edba611d8f65bddfdf"
    assert j["frozen_cr2_packet_sha256"]=="f74bbaec8ad148c65599207053e9e91f0f6dc858b755b7908530dd1518416fc9"


def test_actual_supervisor_crash_recovery(recovered,tmp_path):
    """Start actual synthetic Java worker through Win32 Job, kill supervisor, recover without pytest deleting."""
    assert recovered is not None
    java=Path.home()/"ATDS-TOOLS/jforex-runtime-v0.1/jdk8/jdk8u504-b01/bin/java.exe"
    javac=java.with_name("javac.exe")
    api=Path.home()/".m2/repository/com/dukascopy/api/JForex-API/2.13.99/JForex-API-2.13.99.jar"
    supervisor_src=ROOT/"tools/fc01_f03_cr2/F03CR2Supervisor.cs"
    worker_src=ROOT/"tools/fc01_f03_cr2/SyntheticHistoryWorker.java"
    child_src=ROOT/"tools/fc01_f03_cr2/F03CR2SyntheticChild.cs"
    exe=tmp_path/"F03CR2Supervisor.exe"
    child=tmp_path/"F03CR2SyntheticChild.exe"
    for source,output in ((supervisor_src,exe),(child_src,child)):
        c=subprocess.run([str(CSC),"/nologo","/target:exe","/out:"+str(output),str(source)],
                         capture_output=True,text=True,timeout=30)
        assert c.returncode==0,(c.stdout,c.stderr)
    classes=tmp_path/"classes"
    classes.mkdir()
    c=subprocess.run([str(javac),"-encoding","UTF-8","-cp",str(api),"-d",str(classes),
                      str(worker_src)],capture_output=True,text=True,timeout=40)
    assert c.returncode==0,(c.stdout,c.stderr)
    classpath=os.pathsep.join((str(classes),str(api)))
    lab=tmp_path/"lab"
    lab.mkdir()
    proc=subprocess.Popen([str(exe),str(java),classpath,"pause_after_partial",str(lab)],
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        assigned=False
        for _ in range(5):
            line=proc.stdout.readline()
            if line.strip()=="JOB_ASSIGNED_BEFORE_RESUME=TRUE":
                assigned=True
                break
        assert assigned
        deadline=time.monotonic()+1.5
        runs=[]
        while time.monotonic()<deadline:
            runs=list(lab.glob("cr2_*"))
            if runs and (runs[0]/"worker.partial").exists():
                break
            time.sleep(0.03)
        assert runs and (runs[0]/"run.manifest").exists()
        assert (runs[0]/"worker.partial").exists()
        proc.kill()
        proc.wait(timeout=5)
        deadline=time.monotonic()+2.0
        while True:
            p,d=call(recovered,lab,runs[0])
            if d.get("RESULT")=="ORPHAN_RECOVERED" or time.monotonic()>deadline:
                break
            time.sleep(0.05)
        assert p.returncode==0,(p.stdout,p.stderr)
        assert d["RESULT"]=="ORPHAN_RECOVERED"
        assert not runs[0].exists()
        assert not (lab/"final.csv").exists()
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)
