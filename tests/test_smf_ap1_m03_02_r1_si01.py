from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "reports" / "program"

def load(name):
    return json.loads((R / name).read_text(encoding="utf-8-sig"))

def test_direct_facts_identity_and_inventory():
    d = load("2026-10-06-SMF-AP1-M03-02-R1-SI-01-DIRECT-FACTS-V0.1.json")
    assert d["source"]["output_sha256"] == "7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
    assert d["inventory"]["total_buckets"] == 230
    assert d["source"]["coverage_utc"]["minute_rows"] == 1709180
    assert d["parity"] == {
        "overall": "PASS",
        "pass_count": 1925,
        "fail_count": 0,
        "not_comparable_count": 165,
        "max_abs_diff": 0.0,
        "not_comparable_explanation": "55 empty time buckets x 3 metrics = 165 metric-level NOT_COMPARABLE entries",
    }

def test_candidate_set_is_bounded_and_not_adopted():
    c = load("2026-10-06-SMF-AP1-M03-02-R1-SI-01-CANDIDATE-SET-V0.1.json")
    assert c["status"] == "SCIENTIFIC_INTERPRETATION_CANDIDATE_SET"
    assert c["verdict"] == "QUALIFIED_FOR_HUMAN_SCIENTIFIC_ADJUDICATION"
    assert len(c["candidates"]) == 5
    assert [x["id"] for x in c["candidates"]] == ["SI01-C01","SI01-C02","SI01-C03","SI01-C04","SI01-C05"]
    assert all(v is False for v in c["authority"].values())
    assert c["priority_for_next_scientific_question"]["candidate"] == "SI01-C04"
    assert c["priority_for_next_scientific_question"]["next_method"].startswith("M10")
    assert c["priority_for_next_scientific_question"]["method_not_opened"] is True

def test_exploratory_flags_and_exact_evidence():
    c = load("2026-10-06-SMF-AP1-M03-02-R1-SI-01-CANDIDATE-SET-V0.1.json")
    by_id={x["id"]:x for x in c["candidates"]}
    assert by_id["SI01-C01"]["exploratory_search"] is True
    assert by_id["SI01-C02"]["exploratory_search"] is True
    assert by_id["SI01-C03"]["exploratory_search"] is True
    assert by_id["SI01-C04"]["exploratory_search"] is True
    assert by_id["SI01-C05"]["exploratory_search"] is False
    assert by_id["SI01-C02"]["exact_evidence"]["tick_count"]["p50_max"]["value"] == 455.0
    assert by_id["SI01-C03"]["exact_evidence"]["saturday_index_5"]["n"] == 0
    assert by_id["SI01-C04"]["exact_evidence"]["spread_mean_p50"]["y2026"] == 1.120975719391394
    assert by_id["SI01-C05"]["exact_evidence"]["parity_not_comparable_metric_entries"] == 165

def test_no_forbidden_claim_promoted():
    c = load("2026-10-06-SMF-AP1-M03-02-R1-SI-01-CANDIDATE-SET-V0.1.json")
    joined=" ".join(c["claims_not_supported_still_unknown"]).lower()
    for term in ["causal","statistical significance","predictive","generalization","profitability","trading"]:
        assert term in joined
    for cand in c["candidates"]:
        assert "adopted" not in cand["retrospective_candidate_statement"].lower()
