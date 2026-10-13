"""WER-02 offline static candidate: SYNTHETIC CONTRACT ONLY, NEVER a Windows observer.

Five pure units: IT01 identity, IT02 event lineage, IT03 specific-Job
membership, IT04 per-member exit, IT05 receipt consistency. Every assertion in
a fixture is *only an input claim*, not OS provenance. All Windows event
provider names below are provisional labels, not ETW runtime integration.
"""
from __future__ import annotations
import hashlib
import json
import re
from collections.abc import Mapping

CLASS="SYNTHETIC_CONTRACT"
PROPOSED_EVENT_SOURCE="ETW_KERNEL_PROCESS_PROPOSED"
ABSENCE="COMPLETE_SYNTHETIC_COVERAGE_NO_DESCENDANTS"
MAXFILETIME=(1<<64)-1

def _integer(x, *, allow_zero=False):
    return type(x) is int and (x>=0 if allow_zero else x>0)

def _filetime(x):
    """Reject floats, scientific notation, booleans, whitespace and lossy conversions."""
    if type(x) is int:
        v=x
    elif type(x) is str and bool(re.fullmatch(r"[1-9][0-9]*",x)):
        try:v=int(x)
        except (ValueError,OverflowError):return None
    else:return None
    return str(v) if 0<v<=MAXFILETIME else None

def _ident(x,err):
    if not isinstance(x,Mapping):err.add("INVALID_PROCESS_IDENTITY");return None
    pid=x.get("pid")
    raw=x.get("creation_filetime")
    if type(raw) is float:err.add("LOSSY_FILETIME")
    clock=_filetime(raw)
    if not _integer(pid) or clock is None:
        err.add("INVALID_PROCESS_IDENTITY")
        return None
    return (pid,clock)

def _as_dict(ident):
    return {"pid":ident[0],"creation_filetime":ident[1]}

def _digest(packet):
    raw={key:packet.get(key) for key in ("worker","supervisor","event_stream","job")}
    # Self-consistency checksum of synthetic envelope; NOT event authenticity.
    return hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":"),
                     ensure_ascii=False).encode("utf-8")).hexdigest()

def evaluate(packet):
    e=set()
    if not isinstance(packet,Mapping):
        packet={}
        e.add("INVALID_EVIDENCE_PACKET")
    if packet.get("evidence_class")!=CLASS or packet.get("independent_windows_evidence") is not False:
        e.add("UNAUTHORIZED_WINDOWS_PROVENANCE")
    if packet.get("production_qualification") is True:
        e.add("UNAUTHORIZED_WINDOWS_PROVENANCE")

    # IT-01 -- creation FILETIME and full immutable (PID, start) identity
    worker=_ident(packet.get("worker"),e)
    supervisor=_ident(packet.get("supervisor"),e)
    if worker is not None and supervisor is not None and worker==supervisor:
        e.add("INVALID_PROCESS_IDENTITY")

    # IT-02 -- event stream must have an exact, gap-free synthetic envelope
    stream=packet.get("event_stream")
    stream=stream if isinstance(stream,Mapping) else {}
    source=stream.get("source")
    observer=stream.get("observer")
    if source!=PROPOSED_EVENT_SOURCE or type(observer) is not str or not observer.strip():
        e.add("EVENT_SOURCE_UNQUALIFIED")
    first,last=stream.get("seq_first"),stream.get("seq_last")
    start,end=stream.get("window_start"),stream.get("window_end")
    if (stream.get("continuous") is not True or
         not _integer(stream.get("dropped_events"),allow_zero=True) or
         stream.get("dropped_events")!=0):
        e.add("EVENT_COVERAGE_INCOMPLETE")
    if not _integer(start,allow_zero=True) or not _integer(end) or end<=start:
        e.add("EVENT_COVERAGE_INCOMPLETE")
    events=stream.get("events")
    events=events if isinstance(events,list) else []
    if (not _integer(first) or not _integer(last) or last<first or
        len(events)!=(last-first+1)):
        e.add("EVENT_SEQUENCE_GAP")
    child_to_parent={}
    observed=set()
    seen_event_pid={}
    last_timestamp=None
    for offset,ev in enumerate(events):
        if not isinstance(ev,Mapping):
            e.add("EVENT_SOURCE_UNQUALIFIED");continue
        if ev.get("source")!=source or ev.get("observer")!=observer:
            e.add("EVENT_SOURCE_UNQUALIFIED")
        if not _integer(ev.get("seq")) or not _integer(first) or ev["seq"]!=first+offset:
            e.add("EVENT_SEQUENCE_GAP")
        timestamp=ev.get("time")
        if not _integer(timestamp,allow_zero=True) or not _integer(start,allow_zero=True) or not _integer(end) or not start<=timestamp<=end:
            e.add("EVENT_TIME_OUTSIDE_COVERAGE")
        if type(timestamp) is int:
            if last_timestamp is not None and timestamp<last_timestamp:
                e.add("EVENT_CAUSAL_ORDER_INVALID")
            last_timestamp=timestamp
        child=_ident(ev.get("child"),e)
        parent=_ident(ev.get("parent"),e)
        if ev.get("parent_start_verified") is not True:
            e.add("PARENT_IDENTITY_UNVERIFIED")
        if child is None or parent is None:continue
        if child in observed:
            e.add("DUPLICATE_PROCESS_START_EVENT")
        if child[0] in seen_event_pid and seen_event_pid[child[0]]!=child:
            e.add("PID_REUSE_OR_IDENTITY_MISMATCH")
        seen_event_pid[child[0]]=child
        observed.add(child)
        child_to_parent[child]=parent

    # IT-03 -- inventory must explicitly bind the *specific* synthetic Job
    job=packet.get("job")
    job=job if isinstance(job,Mapping) else {}
    job_id=job.get("job_id")
    if type(job_id) is not str or not job_id.strip():
        e.add("JOB_IDENTITY_MISSING")
    members=job.get("members")
    if not isinstance(members,list) or not members:
        e.add("JOB_INVENTORY_INCOMPLETE");members=[]
    if job.get("query_complete") is not True:
        e.add("JOB_INVENTORY_INCOMPLETE")
    if type(job.get("member_count")) is not int or job.get("member_count")!=len(members):
        e.add("JOB_MEMBER_COUNT_MISMATCH")
    identities={}
    all_exit_proven=True
    for index,item in enumerate(members):
        if not isinstance(item,Mapping):
            e.add("INVALID_PROCESS_IDENTITY");all_exit_proven=False;continue
        member=_ident(item.get("identity"),e)
        post=_ident(item.get("post_identity"),e)
        if member is not None and post!=member:
            e.add("PID_REUSE_OR_IDENTITY_MISMATCH")
            all_exit_proven=False
        if item.get("job_id")!=job_id:
            e.add("MEMBERSHIP_WRONG_JOB")
        if item.get("membership_verified") is not True:
            e.add("JOB_MEMBERSHIP_UNVERIFIED")
        if item.get("raw_provenance")!="OFFLINE_FIXTURE":
            e.add("RAW_PROVENANCE_MISSING")
            all_exit_proven=False
        exit_code=item.get("exit_code")
        if (item.get("handle_retained") is not True or
            item.get("wait_signaled") is not True or
            type(exit_code) is not int or exit_code<0 or exit_code==259):
            e.add("MEMBER_EXIT_UNVERIFIED")
            all_exit_proven=False
        if member is not None:
            if member in identities:
                e.add("DUPLICATE_JOB_MEMBER_IDENTITY")
            identities[member]=item

    # IT-04 -- termination and matching identity of *every* member
    if job.get("post_query_observed") is not True or type(job.get("post_count")) is not int or job.get("post_count")!=0:
        e.add("MEMBER_EXIT_UNVERIFIED");all_exit_proven=False

    for member in identities:
        if member not in observed:
            e.add("JOB_MEMBER_START_EVENT_MISSING")
    for observed_identity in observed:
        if observed_identity not in identities:
            e.add("UNACCOUNTED_PROCESS_START_EVENT")

    # Classify from the full synthetic parent-start pairs; not from Job membership.
    descend=set()
    classified=set()
    if worker is not None:
        if child_to_parent.get(worker)==supervisor and worker in identities:
            classified.add(worker)
        else:
            e.add("PARENT_LINEAGE_NOT_BOUND")
    # Look for parent PID reuse with mismatched start identity in job member event.
    for member in identities:
        parent=child_to_parent.get(member)
        if parent is None:continue
        if worker is not None and parent[0]==worker[0] and parent!=worker:
            e.add("PARENT_LINEAGE_NOT_BOUND")
        if any(parent[0]==ident[0] and parent!=ident for ident in identities):
            e.add("PARENT_LINEAGE_NOT_BOUND")
    changed=True
    while changed:
        changed=False
        for member in identities:
            if member==worker or member in classified:continue
            parent=child_to_parent.get(member)
            if parent in classified:
                classified.add(member)
                descend.add(member)
                changed=True
    classes={}
    for member in identities:
        if member==worker and member in classified:category="PRIMARY_WORKER"
        elif member in descend:category="VERIFIED_DESCENDANT"
        elif member in observed and child_to_parent.get(member) is not None:
            parent=child_to_parent[member]
            if parent not in identities and (worker is None or parent[0]!=worker[0]):
                category="OTHER_IDENTIFIED_JOB_MEMBER"
            else:category="UNCLASSIFIED_MEMBER"
        else:category="UNCLASSIFIED_MEMBER"
        classes[str(member[0])]=category
        if category=="UNCLASSIFIED_MEMBER":e.add("UNKNOWN_MEMBER")
    if worker not in identities:
        e.add("PRIMARY_WORKER_MISSING")
    if any(v=="UNCLASSIFIED_MEMBER" for v in classes.values()):
        e.add("UNKNOWN_MEMBER")

    # IT-05 -- cryptographic *consistency*, not source authenticity.
    receipt=packet.get("receipt")
    receipt=receipt if isinstance(receipt,Mapping) else {}
    for nested in (stream,job,receipt):
        if ("evidence_class" in nested and nested["evidence_class"]!=CLASS) or nested.get("independent_windows_evidence") is True:
            e.add("UNAUTHORIZED_WINDOWS_PROVENANCE")
    actual_desc=[_as_dict(x) for x in sorted(descend)]
    declared=receipt.get("descendant_identities")
    normalized=[]
    if isinstance(declared,list):
        for item in declared:
            iid=_ident(item,e)
            if iid is not None:normalized.append(iid)
    else:
        e.add("RECEIPT_CONTRADICTION")
    if (receipt.get("descendant_created") is not (len(descend)>0) or
        not isinstance(declared,list) or len(declared)!=len(descend) or
        set(normalized)!=descend or
        receipt.get("descendant_absence_proven") is not (len(descend)==0)):
        e.add("RECEIPT_CONTRADICTION")
    raw_sha=receipt.get("raw_evidence_sha256")
    if type(raw_sha) is not str or raw_sha!=_digest(packet):
        e.add("RAW_DIGEST_MISMATCH")
    if receipt.get("global_status")!=("BLOCKED" if e else "PASS"):
        e.add("RECEIPT_CONTRADICTION")

    absence=(not e and len(descend)==0 and
              worker in classified and len(classified)==len(identities) and
              all_exit_proven)
    return {
        "status":"BLOCKED" if e else "PASS",
        "violations":sorted(e),
        "worker_identity":_as_dict(worker) if worker else None,
        "classifications":classes,
        "verified_descendant_count":len(descend),
        "descendant_identities":actual_desc,
        "descendant_absence_proven":bool(absence),
        "absence_evidence":ABSENCE if absence else "NOT_PROVEN",
        "all_member_exits_verified":bool(all_exit_proven and not
                                  ("PID_REUSE_OR_IDENTITY_MISMATCH" in e or
                                   "MEMBER_EXIT_UNVERIFIED" in e)),
        "evidence_class":CLASS,
        "independent_windows_evidence":False,
        "production_qualification":False,
        "scope":"STATIC_SYNTHETIC_CONTRACT_ONLY",
        "collector_implemented":False
    }
