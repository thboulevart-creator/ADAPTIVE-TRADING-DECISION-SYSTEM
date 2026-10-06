from __future__ import annotations
from datetime import datetime, timezone
import json

CUTOVER="2026-10-06T09:22:55Z"
FIRST_H1_START="2026-10-06T10:00:00Z"
FIRST_DECISION="2026-10-06T11:00:00Z"
OLD_END="2026-05-24T23:59:59.963Z"
N=58927

def parse_z(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def validate(d):
    assert d["bindings"]["m06_final_required_n"] == N
    assert d["temporal_rule"]["cutover_utc"] == CUTOVER
    assert d["temporal_rule"]["first_full_post_cutover_h1_start_utc"] == FIRST_H1_START
    assert d["temporal_rule"]["first_forward_signal_decision_time_utc"] == FIRST_DECISION
    assert parse_z(FIRST_H1_START) > parse_z(CUTOVER)
    assert parse_z(FIRST_DECISION) > parse_z(FIRST_H1_START)
    assert parse_z(FIRST_DECISION) > parse_z(OLD_END)
    assert d["temporal_rule"]["warmup_performance_inclusion"] is False
    assert d["terminal_rule"]["performance_values_may_determine_end"] is False
    assert d["terminal_rule"]["optional_stopping_on_pnl_or_ci"] is False
    assert d["terminal_rule"]["if_sample_count_below_58927"] == "WAIT_NOT_READY_NO_PERFORMANCE_OBSERVATION"
    assert d["data_family"]["new_forward_instance_must_have_distinct_manifest"] is True
    assert d["data_family"]["historical_manifest_reuse_as_forward_instance"] is False
    assert d["instance_identity_rule"]["instance_digest_available_now"] is False
    assert all(v is False for v in d["authority"].values())
    assert d["force"] is False
    return True

if __name__=="__main__":
    from pathlib import Path
    p=Path(__file__).resolve().parents[1]/"GOVERNANCE"/"AO-E0-B12-DATA-01-PROSPECTIVE-FORWARD-INSTANCE-FORMATION-CONTRACT-V0.1.json"
    d=json.loads(p.read_text())
    validate(d)
    print("AO_E0_B12_DATA_01_FORMATION_RULE_PASS")
