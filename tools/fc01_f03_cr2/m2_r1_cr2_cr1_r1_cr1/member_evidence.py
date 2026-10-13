"""R1-CR1-RED-R1 / synthetic-only HISTORICAL BEHAVIOR ADAPTER.

This is NOT a fix, GREEN implementation, Windows observation, or descendant
relationship proof. It only maps synthetic fixture records to the ORIGINAL R1
forensic_contract check_descendants/check_independent_tree interfaces.
In particular, a child marker is NOT independent parenthood evidence.
"""
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
LEGACY=ROOT/"m2_r1_cr2_cr1_r1"/"forensic_contract.py"
spec=importlib.util.spec_from_file_location("r1_cr1_frozen_original_contract",LEGACY)
_original=importlib.util.module_from_spec(spec)
spec.loader.exec_module(_original)

RULE_VERSION="R1-CR1-RED-HISTORICAL-ADAPTER-V0.1"
OBSERVED_WINDOWS_EVIDENCE=False

def classify_and_validate_members(obs):
    """Expose the OLD evidence rules without treating a marker as lineage proof."""
    worker=obs.get("worker") or {}
    nodes=obs.get("members_before")
    if not isinstance(nodes,list):
        nodes=[]
    wpid=worker.get("pid")
    stamp=worker.get("start")
    before=[]
    labels={}
    explicit=obs.get("explicit_child_marker") is True
    explicit_pid=obs.get("explicit_child_pid")
    for node in nodes:
        if not isinstance(node,dict):
            continue
        pid=node.get("pid")
        start=node.get("start")
        is_worker=pid==wpid and start==stamp
        if is_worker:
            labels[str(pid)]="PRIMARY_WORKER"
        elif explicit and pid==explicit_pid:
            labels[str(pid)]="EXPLICIT_CHILD_MARKER_ONLY"
        else:
            labels[str(pid)]="UNCLASSIFIED_MEMBER"
        before.append({
          "pid":pid,"start":start,
          "identity_handle_observed":True,
          "exit_wait_zero":node.get("exit_wait_zero"),
          "exit_code_observed":node.get("exit_code"),
        })
    pre_legacy={
      "worker":worker,
      "job_before_ids":before,
      "job_assigned_before_resume":True,
      "worker_exit_proven":any(n.get("pid")==wpid and n.get("exit_wait_zero") is True for n in before),
      "job_post_query_observed":obs.get("post_query_observed"),
      "job_post_active_count":obs.get("job_members_post_count"),
      "identities_reconciled":bool(before) and all(n.get("exit_wait_zero") is True for n in before),
      "tree_escape_evidence":"NEGATIVE_WITH_OBSERVATION",
      "termination_action":obs.get("termination_action")
    }
    old_tree=_original.check_independent_tree(pre_legacy)
    old_members=[]
    if explicit:
        old_members=[{
          "pid":obs.get("explicit_child_pid"),
          "start":obs.get("explicit_child_start"),
          "in_expected_job":True,
          "pre_exit_identity_verified":True,
          "post_exit_identity_verified":True,
          "exit_wait_zero":True,
          "exit_code":88,
          "termination_action":obs.get("termination_action")
        }]
    # Exactly mirrors previous receipt's absence gate: only worker in job.
    absence=("ENUMERATED_EMPTY" if not explicit and len(before)==1
             and before[0].get("pid")==wpid else "NOT_PROVEN")
    old_desc=_original.check_descendants({
      "created":explicit,
      "members":old_members,
      "membership_enumerated":bool(before),
      "all_identities_reconciled":pre_legacy["identities_reconciled"],
      "absence_evidence":absence
    })
    errors=sorted(set(old_tree["violations"]+old_desc["violations"]))
    return {
      "status":"BLOCKED" if errors else "PASS",
      "violations":errors,
      "classifications":labels,
      "unclassified_count":sum(x=="UNCLASSIFIED_MEMBER" for x in labels.values()),
      "descendant_absence_proven":absence=="ENUMERATED_EMPTY" and old_desc["status"]=="PASS",
      "absence_evidence":absence,
      "all_member_exits_verified":old_tree["status"]=="PASS",
      "evidence_kind":"SYNTHETIC_LEGACY_ADAPTER_NO_WINDOWS_OBSERVATION",
      "rule_version":RULE_VERSION
    }
