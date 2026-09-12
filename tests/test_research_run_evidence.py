from src.research_run_evidence import decision_trace_from_v43_report, from_v43_report


CODE_VERSION = "963f02e93db63bef36c25d58c3634096a2247e6a"


def v43_report() -> dict:
    return {
        "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
        "version": "V4.3",
        "status": "UNVERIFIED",
        "scope": {
            "research_instrument": "Dukascopy USATECHIDXUSD",
            "execution_instrument": "VT Markets NAS100.s",
            "minimum_research_years": 5.0,
        },
        "research": {
            "files": [
                {"path": "research/a.bi5", "sha256": "aaa"},
                {"path": "research/b.bi5", "sha256": "bbb"},
            ],
            "rows": 100,
            "first": "2020-01-01T00:00:00+00:00",
            "last": "2025-01-01T00:00:00+00:00",
        },
    }


def test_v43_report_produces_stable_upstream_trace_ids() -> None:
    evidence = from_v43_report(v43_report(), code_version=CODE_VERSION)

    assert evidence.provenance_id.startswith("PROV-")
    assert evidence.research_run_id.startswith("RUN-")
    assert evidence.code_version == CODE_VERSION
    assert evidence.configuration_version.startswith("CFG-")
    assert evidence.dataset_id.startswith("DATA-")
    assert evidence.dataset_version


def test_real_research_evidence_does_not_fake_missing_decision_chain() -> None:
    trace = decision_trace_from_v43_report(v43_report(), code_version=CODE_VERSION)

    status, missing = trace.validate()

    assert status == "FAIL"
    assert missing == ("context_id", "decision", "action_id", "result_id")
