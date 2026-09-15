from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE


def test_batch10_only_three_adjudicated_pass_dates_enter_special_session_evidence():
    expected = {
        date(2024, 12, 31): ("75799", frozenset({22, 23})),
        date(2025, 1, 20): ("76806", frozenset({18, 19, 20, 21, 22})),
        date(2025, 2, 17): ("78513", frozenset({18, 19, 20, 21, 22})),
    }
    for day, (record_id, hours) in expected.items():
        evidence = SPECIAL_SESSION_EVIDENCE[day]
        assert evidence["broker_record_id"] == record_id
        assert evidence["fully_closed_hours_utc"] == hours
        assert evidence["artifact_id"] == 10411022092
        assert evidence["artifact_sha256"] == "1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14"
        assert evidence["probe_commit"] == "443b3696e4e2740a54354787de231c886f90b26e"


def test_batch10_blocked_cross_date_targets_never_enter_resolving_evidence():
    for day in (date(2025, 1, 1), date(2025, 4, 18)):
        assert day not in SPECIAL_SESSION_EVIDENCE
        assert day not in NO_SPECIAL_CHANGE_EVIDENCE
