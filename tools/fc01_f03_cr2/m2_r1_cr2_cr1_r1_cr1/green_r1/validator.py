"""R1-CR1-GREEN-R1 V0.1: isolated, SYNTHETIC-ONLY evidence contract.

NEVER an independent Windows process observation. Pure deterministic validation
of declared synthetic fixtures; no Job Object API, subprocess, provider or IO.
Requires subsequent independent Windows qualification under separate authority.
"""
from __future__ import annotations
from collections.abc import Mapping

EVIDENCE_CLASS="SYNTHETIC_CONTRACT"
INDEPENDENT_WINDOWS_EVIDENCE=False
PRODUCTION_QUALIFICATION=False
ALLOWED_RAW_PROVENANCE="R1_JOB_MEMBER_PRE_AND_POST_OBSERVED"
TERMINATION_ACTIONS=frozenset(("TERMINATE_JOB","NORMAL_WORKER_EXIT"))
ABSENCE_PROVEN="ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS"

def positive(value):
    return type(value) is int and value>0

def identity(n):
    if not isinstance(n,Mapping):
        return None
    pid,start=n.get("pid"),n.get("start")
    return (pid,start) if positive(pid) and positive(start) else None

def valid_identity_claims(data):
    return isinstance(data,list) and all(identity(x) is not None for x in data)

def classify_and_validate_members(obs):
    """Return fail-closed result, with SYNTHETIC evidence class always explicit."""
    e=set()
    classes={}
    descendants=set()
    if not isinstance(obs,Mapping):
        obs={}
        e.add("INVALID_RECEIPT_OBJECT")

    worker_id=identity(obs.get("worker"))
    supervisor_id=identity(obs.get("supervisor"))
    if worker_id is None:e.add("WORKER_IDENTITY_INVALID")
    if supervisor_id is None:e.add("SUPERVISOR_IDENTITY_INVALID")

    incoming=obs.get("members_before")
    if not isinstance(incoming,list) or not incoming:
        e.add("PRE_TERMINATION_JOB_MEMBERS_UNKNOWN")
        members=[]
    else:
        members=incoming
    pre_count=obs.get("job_member_count_before")
    if type(pre_count) is not int or pre_count!=len(members):
        e.add("JOB_MEMBER_COUNT_MISMATCH")
    post_count=obs.get("job_members_post_count")
    if obs.get("post_query_observed") is not True:
        e.add("JOB_POST_QUERY_NOT_VERIFIED")
    if type(post_count) is not int or post_count!=0:
        e.add("MEMBER_TERMINATION_NOT_VERIFIED")
    action=obs.get("termination_action")
    if type(action) is not str or action not in TERMINATION_ACTIONS:
        e.add("TERMINATION_ACTION_MISSING")

    if "evidence_class" in obs and obs["evidence_class"]!=EVIDENCE_CLASS:
        e.add("UNAUTHORIZED_EVIDENCE_CLASS")
    if obs.get("independent_windows_evidence") is True or obs.get("production_qualification") is True:
        e.add("UNAUTHORIZED_EVIDENCE_CLASS")

    seen=set()
    seen_pid=set()
    scanned=[]
    member_identities_valid=True
    provenance_valid=True
    membership_valid=True
    exit_waits_valid=True

    for idx,n in enumerate(members):
        node=n if isinstance(n,Mapping) else {}
        ident=identity(n)
        pid=node.get("pid")
        label=str(pid) if positive(pid) else "INVALID_"+str(idx)
        if ident is None:
            e.add("MEMBER_IDENTITY_INVALID")
            member_identities_valid=False
        else:
            if ident in seen or pid in seen_pid:
                e.add("DUPLICATE_JOB_MEMBER_IDENTITY")
                member_identities_valid=False
            seen.add(ident)
            seen_pid.add(pid)
        if ident is not None and (
                type(node.get("post_start")) is not int or
                node.get("post_start")!=node.get("start")):
            e.add("MEMBER_START_IDENTITY_MISMATCH")
            member_identities_valid=False
        if ident is None:
            member_identities_valid=False
        if node.get("membership_verified") is not True:
            e.add("MEMBER_JOB_MEMBERSHIP_UNVERIFIED")
            membership_valid=False
        provenance=node.get("raw_provenance")
        if provenance is None:
            e.add("MEMBER_RAW_PROVENANCE_MISSING")
            provenance_valid=False
        elif type(provenance) is not str or provenance!=ALLOWED_RAW_PROVENANCE:
            e.add("MEMBER_RAW_PROVENANCE_INVALID")
            provenance_valid=False
        code=node.get("exit_code")
        if node.get("exit_wait_zero") is not True or type(code) is not int or code<0 or code==259:
            e.add("MEMBER_TERMINATION_NOT_VERIFIED")
            exit_waits_valid=False
        scanned.append((node,ident,label))

    # Step 1: exactly one primary worker must have a verified synthetic parent
    # identity that equals the stated supervisor. Job membership alone is NOT a
    # parent/child observation, including in these synthetic contract fixtures.
    has_worker=False
    for n,ident,label in scanned:
        cls="UNCLASSIFIED_MEMBER"
        parent_id=(n.get("parent_pid"),n.get("parent_start"))
        parent_ok=(positive(n.get("parent_pid")) and positive(n.get("parent_start"))
                   and n.get("parent_identity_verified") is True)
        if (ident is not None and worker_id is not None and ident==worker_id and
                n.get("membership_verified") is True and parent_ok and
                parent_id==supervisor_id):
            cls="PRIMARY_WORKER"
            has_worker=True
        classes[label]=cls

    # Step 2: discover transitive descendants by verified synthetic chains.
    # Full (PID, creation FILETIME) pairs are required at every link.
    chain={worker_id} if has_worker else set()
    remaining=[(n,ident,label) for n,ident,label in scanned
               if classes[label]=="UNCLASSIFIED_MEMBER"]
    changed=True
    while changed:
        changed=False
        for n,ident,label in remaining:
            if (classes[label]!="UNCLASSIFIED_MEMBER" or ident is None or
                n.get("membership_verified") is not True):
                continue
            parent_id=(n.get("parent_pid"),n.get("parent_start"))
            if (positive(n.get("parent_pid")) and positive(n.get("parent_start"))
                    and n.get("parent_identity_verified") is True and
                    parent_id in chain and ident!=worker_id):
                classes[label]="VERIFIED_DESCENDANT"
                descendants.add(ident)
                chain.add(ident)
                changed=True

    # Step 3: non-descendant Job members require external lineage classification.
    # Never disguise the worker's PID with the wrong creation FILETIME as external.
    job_ids={ident for _,ident,_ in scanned if ident is not None}
    for n,ident,label in scanned:
        if (classes[label]!="UNCLASSIFIED_MEMBER" or ident is None or
            n.get("membership_verified") is not True):
            continue
        parent_id=(n.get("parent_pid"),n.get("parent_start"))
        parent_ok=(positive(n.get("parent_pid")) and positive(n.get("parent_start"))
                   and n.get("parent_identity_verified") is True)
        shadows_worker=(worker_id is not None and n.get("parent_pid")==worker_id[0] and
                        parent_id!=worker_id)
        if (ident!=worker_id and parent_ok and
                n.get("external_lineage_proven") is True and
                not shadows_worker and parent_id not in job_ids):
            classes[label]="OTHER_IDENTIFIED_JOB_MEMBER"

    unknown=sum(v=="UNCLASSIFIED_MEMBER" for v in classes.values())
    if unknown:e.add("UNCLASSIFIED_JOB_MEMBER")
    if worker_id is None or classes.get(str(worker_id[0]))!="PRIMARY_WORKER":
        e.add("WORKER_MISSING_FROM_JOB_BEFORE_LIST")

    # A synthetic relationship declaration may satisfy this purely synthetic
    # contract, but never licenses any independent Windows evidence assertion.
    descendant_count=sum(v=="VERIFIED_DESCENDANT" for v in classes.values())
    if len(descendants)!=descendant_count:
        e.add("DESCENDANT_IDENTITY_MISMATCH")
    if "claimed_descendant_absent" in obs:
        v=obs["claimed_descendant_absent"]
        if type(v) is not bool or (v is True and descendant_count>0):
            e.add("CONTRADICTORY_DESCENDANT_ABSENCE")
    if "descendant_created" in obs:
        v=obs["descendant_created"]
        if type(v) is not bool or v!=(descendant_count>0):
            e.add("CONTRADICTORY_DESCENDANT_CREATED")
    if "descendant_identities" in obs:
        actual=obs["descendant_identities"]
        if (not valid_identity_claims(actual) or len(actual)!=len(descendants) or
            {identity(x) for x in actual}!=descendants):
            e.add("DESCENDANT_IDENTITY_MISMATCH")
    marker=obs.get("explicit_child_marker")
    if type(marker) is not bool:
        e.add("DESCENDANT_MARKER_UNVERIFIED")
    elif marker:
        child_id=(obs.get("explicit_child_pid"),obs.get("explicit_child_start"))
        if not positive(child_id[0]) or not positive(child_id[1]) or child_id not in descendants:
            e.add("DESCENDANT_MARKER_UNVERIFIED")

    exits_verified=(
        len(members)>0 and member_identities_valid and provenance_valid and
        membership_valid and exit_waits_valid and
        type(pre_count) is int and pre_count==len(members) and
        obs.get("post_query_observed") is True and
        type(post_count) is int and post_count==0 and
        type(action) is str and action in TERMINATION_ACTIONS
    )
    all_valid_for_absence=(
        exits_verified and worker_id is not None and supervisor_id is not None and
        has_worker and unknown==0 and descendant_count==0 and
        len(classes)==len(members) and not e
    )

    if "descendant_absence_proven" in obs:
        val=obs["descendant_absence_proven"]
        if type(val) is not bool or val!=all_valid_for_absence:
            e.add("CONTRADICTORY_DESCENDANT_ABSENCE_PROOF")
    if "global_status" in obs:
        claimed=obs["global_status"]
        if type(claimed) is not str or claimed!=("BLOCKED" if e else "PASS"):
            e.add("CONTRADICTORY_GLOBAL_STATUS")

    absence=all_valid_for_absence and not e
    return {
        "status":"BLOCKED" if e else "PASS",
        "violations":sorted(e),
        "classifications":classes,
        "unclassified_count":unknown,
        "verified_descendant_count":descendant_count,
        "descendant_identities":[{"pid":pid,"start":start} for pid,start in sorted(descendants)],
        "descendant_absence_proven":bool(absence),
        "absence_evidence":ABSENCE_PROVEN if absence else "NOT_PROVEN",
        "all_member_exits_verified":bool(exits_verified),
        "evidence_class":EVIDENCE_CLASS,
        "fixture_class":"SYNTHETIC_CONTRACT",
        "independent_windows_evidence":False,
        "production_qualification":False,
        "green_scope":"ISOLATED_CONTRACT_ONLY",
    }
