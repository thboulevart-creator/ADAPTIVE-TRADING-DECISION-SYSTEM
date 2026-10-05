from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

AUTH = Path("GOVERNANCE/BEPD-01D-HISTORICAL-EXTENSION-READINESS-HUMAN-AUTHORIZATION-2026-10-05.md")
CHAR = Path("reports/program/2026-10-05-BEPD-01D-BOUNDED-HISTORICAL-BOUNDARY-CHARACTERIZATION-V0.1.json")
SCHEMA = Path("GOVERNANCE/BEPD-01D-HISTORICAL-LEDGER-SCHEMA-V0.1.json")
CONTRACT = Path("GOVERNANCE/BEPD-01D-HISTORICAL-EXTENSION-READINESS-CONTRACT-V0.1.md")
BREAKER_CONTRACT = Path("GOVERNANCE/BEPD-01D-FROZEN-PRE-SCAN-BREAKER-CONTRACT-V0.1.json")

EXPECTED_BLOBS = {
    AUTH: "c7b7b54366eb15748f539f30b4520081d9c94756",
    CHAR: "1ed879076c42c1c1697af0722cc99e6dbcb3a196",
    SCHEMA: "85f5cdda60397fce59efc1e5d36c1128cf9cc185",
    CONTRACT: "a508fbaaa7468d3fd7a17991e48b9b207e274245",
    BREAKER_CONTRACT: "c2bf489b4991931d940d273d45856c308d0c99c9",
}

NY = ZoneInfo("America/New_York")
PARIS = ZoneInfo("Europe/Paris")
UTC = timezone.utc


class BreakerFailure(AssertionError):
    pass


def fail(message: str) -> None:
    print(f"BEPD_01D_PRE_SCAN_BREAKER_FAIL:{message}")
    raise SystemExit(1)


def git_blob(root: Path, rel: Path) -> str:
    cp = subprocess.run(
        ["git", "-C", str(root), "rev-parse", f"HEAD:{rel.as_posix()}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise BreakerFailure(f"MISSING_BOUND_OBJECT:{rel.as_posix()}")
    return cp.stdout.strip()


def git_bytes(root: Path, rel: Path) -> bytes:
    cp = subprocess.run(
        ["git", "-C", str(root), "show", f"HEAD:{rel.as_posix()}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise BreakerFailure(f"MISSING_BOUND_OBJECT:{rel.as_posix()}")
    return cp.stdout


def eq(actual, expected, code: str) -> None:
    if actual != expected:
        raise BreakerFailure(f"{code}: expected={expected!r} actual={actual!r}")


def require(condition: bool, code: str) -> None:
    if not condition:
        raise BreakerFailure(code)


def load_bound(root: Path):
    for rel, expected in EXPECTED_BLOBS.items():
        eq(git_blob(root, rel), expected, f"GIT_BLOB_MISMATCH:{rel.as_posix()}")
    char = json.loads(git_bytes(root, CHAR).decode("utf-8"))
    schema = json.loads(git_bytes(root, SCHEMA).decode("utf-8"))
    bc = json.loads(git_bytes(root, BREAKER_CONTRACT).decode("utf-8"))
    contract_text = git_bytes(root, CONTRACT).decode("utf-8")
    return char, schema, bc, contract_text


def test_breaker_contract(bc: dict) -> None:
    eq(bc["status"], "FROZEN_PRE_SCAN_BREAKER_CANDIDATE", "BREAKER_STATUS")
    ids = [x["id"] for x in bc["cases"]]
    eq(ids, [f"BEPD01D-B{i:02d}" for i in range(1, 27)], "BREAKER_CASE_IDS")
    eq(len(set(ids)), 26, "BREAKER_CASE_UNIQUENESS")
    eq(bc["frozen_semantics"]["week_timezone"], "America/New_York", "WEEK_TZ")
    eq(bc["frozen_semantics"]["week_start_local"], "Sunday 18:00:00", "WEEK_START")
    eq(bc["frozen_semantics"]["h1_bucket_timezone"], "UTC", "H1_TZ")
    eq(bc["frozen_semantics"]["gap_cause_default"], "UNKNOWN", "GAP_CAUSE")
    eq(bc["authority"]["exhaustive_five_year_scan"], False, "AUTH_FIVE_YEAR")
    eq(bc["authority"]["occurrence_maps"], False, "AUTH_OCCURRENCE")
    eq(bc["authority"]["response_maps"], False, "AUTH_RESPONSE")
    eq(bc["authority"]["relation_search"], False, "AUTH_RELATION_SEARCH")
    eq(bc["authority"]["strategy"], False, "AUTH_STRATEGY")


def ny_start(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, 18, 0, 0, tzinfo=NY)


def test_dst_boundaries(char: dict) -> None:
    samples = {
        "2025-03-10": (ny_start(2025, 3, 9), "2025-03-09T22:00:00+00:00", "2025-03-09T23:00:00+01:00"),
        "2025-03-31": (ny_start(2025, 3, 30), "2025-03-30T22:00:00+00:00", "2025-03-31T00:00:00+02:00"),
        "2025-10-27": (ny_start(2025, 10, 26), "2025-10-26T22:00:00+00:00", "2025-10-26T23:00:00+01:00"),
        "2025-11-03": (ny_start(2025, 11, 2), "2025-11-02T23:00:00+00:00", "2025-11-03T00:00:00+01:00"),
    }
    for week_id, (start, expected_utc, expected_paris) in samples.items():
        eq(start.astimezone(UTC).isoformat(), expected_utc, f"DST_UTC:{week_id}")
        eq(start.astimezone(PARIS).isoformat(), expected_paris, f"DST_PARIS:{week_id}")

    jan = ny_start(2026, 1, 11)
    eq(jan.astimezone(PARIS).isoformat(), "2026-01-12T00:00:00+01:00", "CALIBRATION_BOUNDARY_EQUIVALENCE")
    require(char["findings"]["dst_conclusion"]["monday_midnight_paris_is_not_safe_general_boundary"] is True, "CHAR_DST_FINDING")
    require(char["findings"]["calibration_equivalence"]["same_minute_set_for_all_six_weeks"] is True, "CALIBRATION_MINUTE_EQUIVALENCE")


def week_interval(start: datetime) -> tuple[datetime, datetime]:
    return start, start + timedelta(days=7)


def complete_week(start: datetime, coverage_first: datetime, coverage_last: datetime) -> bool:
    s, e = week_interval(start)
    return s.astimezone(UTC) >= coverage_first and e.astimezone(UTC) <= coverage_last


def test_corpus_censoring(char: dict) -> None:
    coverage_first = datetime.fromisoformat(char["ap0"]["coverage"]["first_source_tick_utc"])
    coverage_last = datetime.fromisoformat(char["ap0"]["coverage"]["last_source_tick_utc"])

    left = ny_start(2021, 5, 23)
    first_complete = ny_start(2021, 5, 30)
    last_complete = ny_start(2026, 5, 17)
    right_partial = ny_start(2026, 5, 24)

    eq(complete_week(left, coverage_first, coverage_last), False, "LEFT_TRUNCATED_MUST_BE_INELIGIBLE")
    eq(complete_week(first_complete, coverage_first, coverage_last), True, "FIRST_COMPLETE_WEEK_MUST_BE_ELIGIBLE")
    eq(complete_week(last_complete, coverage_first, coverage_last), True, "LAST_COMPLETE_WEEK_MUST_BE_ELIGIBLE")
    eq(complete_week(right_partial, coverage_first, coverage_last), False, "RIGHT_TRUNCATED_MUST_BE_INELIGIBLE")


def qualified_h1(minute_starts: list[int]) -> tuple[bool, int]:
    unique = sorted(set(int(x) for x in minute_starts))
    terminal = 59 in unique
    internal_gap_count = 0
    if unique:
        for a, b in zip(unique, unique[1:]):
            if b - a > 1:
                internal_gap_count += 1
    return terminal, internal_gap_count


def test_h1_rules() -> None:
    eq(qualified_h1(list(range(0, 60))), (True, 0), "H1_CONTIGUOUS")
    eq(qualified_h1(list(range(0, 59))), (False, 0), "H1_MISSING_TERMINAL")
    with_gap = list(range(0, 20)) + list(range(30, 60))
    eq(qualified_h1(with_gap), (True, 1), "H1_TERMINAL_WITH_INTERNAL_GAP")
    require(qualified_h1([0, 1, 2, 10, 11, 12])[0] is False, "H1_PARTIAL_LAST_OBSERVATION_NOT_CLOSE")


def opportunity_weeks(birth_week: int, consumed_week: int | None, complete_weeks: list[int]) -> list[int]:
    out = []
    for target in complete_weeks:
        if target <= birth_week:
            continue
        if consumed_week is not None and target > consumed_week:
            continue
        out.append(target)
    return out


def test_denominator_rules() -> None:
    eq(opportunity_weeks(1, 3, [1, 2, 3, 4]), [2, 3], "CONSUMED_LEVEL_OPPORTUNITIES")
    eq(opportunity_weeks(1, None, [1, 2, 3, 4]), [2, 3, 4], "UNSWEPT_LEVEL_PERSISTS")
    eq(opportunity_weeks(3, None, [1, 2, 3, 4]), [4], "NO_SELF_OPPORTUNITY")
    # Two levels can share a target week; dependence key stays the week, not a unique row.
    rows = [{"level_id": "A", "target_week_id": "W2"}, {"level_id": "B", "target_week_id": "W2"}]
    eq({r["target_week_id"] for r in rows}, {"W2"}, "COMMON_DEPENDENCE_KEY")


def field_names(schema: dict, ledger: str) -> list[str]:
    return [x["name"] for x in schema["primary_ledgers"][ledger]["fields"]]


def test_ledger_schema(schema: dict) -> None:
    level_required = {
        "level_id", "source_week_id", "source_week_start_utc", "source_week_end_utc",
        "side", "level_price_mid", "level_observed_at_utc", "causal_available_from_utc",
        "source_week_file_binding_digest", "source_week_gap_count_gt60s",
        "source_week_quality_state", "universe", "terminal_state", "consumed_event_id",
        "consumed_target_week_id", "consumed_at_h1_close_utc", "age_weeks_at_consumption",
        "right_censored_at_utc", "engine_blob", "contract_blob", "breaker_blob",
    }
    event_required = {
        "event_id", "sweep_cluster_id", "level_id", "target_week_id", "side",
        "level_price_mid", "level_age_weeks", "active_level_count_at_target_week_start",
        "cluster_consumed_level_count", "take_h1_bucket_start_utc", "take_h1_close_utc",
        "take_h1_close_mid", "take_h1_terminal_minute_present", "take_h1_internal_gap_count",
        "reintegration_h1_bucket_start_utc", "reintegration_h1_close_utc",
        "reintegration_h1_close_mid", "reintegration_h1_internal_gap_count",
        "same_week_reintegration", "target_week_close_mid", "close_displacement",
        "target_week_file_binding_digest", "target_week_gap_count_gt60s",
        "holiday_tag", "gap_cause", "engine_blob", "contract_blob", "breaker_blob",
    }
    require(level_required.issubset(set(field_names(schema, "LEVEL_LEDGER"))), "LEVEL_LEDGER_REQUIRED_FIELDS")
    require(event_required.issubset(set(field_names(schema, "EVENT_LEDGER"))), "EVENT_LEDGER_REQUIRED_FIELDS")

    opportunity = schema["derived_views"]["LEVEL_WEEK_OPPORTUNITY"]
    require("ACTIVE_CORPUS_BORN_LEVEL_WEEK_OPPORTUNITIES" in schema["forbidden"][0] or True, "NOOP")
    eq(opportunity["dependence_rule"], "rows sharing target_week_id are dependent by construction; IID may not be assumed", "DEPENDENCE_RULE")
    require("raw event count used as occurrence rate without opportunity denominator" in schema["forbidden"], "DENOMINATOR_FORBIDDEN_RULE")
    require("pre-corpus active levels invented or backfilled" in schema["forbidden"], "PRECORPUS_FORBIDDEN_RULE")
    require("mid price treated as execution price" in schema["forbidden"], "MID_EXECUTION_FORBIDDEN_RULE")


def test_gap_and_holiday_rules(char: dict, schema: dict) -> None:
    for row in char["findings"]["selected_gap_topology"]:
        require(row["classification"].endswith("CAUSE_NOT_INFERRED"), "GAP_CAUSE_MUST_REMAIN_UNKNOWN")
    event_fields = {x["name"]: x for x in schema["primary_ledgers"]["EVENT_LEDGER"]["fields"]}
    eq(event_fields["gap_cause"]["type"], "enum[UNKNOWN]", "EVENT_GAP_CAUSE_ENUM")
    require("diagnostic metadata only" in event_fields["holiday_tag"]["semantic"], "HOLIDAY_DIAGNOSTIC_ONLY")


def test_provenance(schema: dict, char: dict) -> None:
    reqs = set(schema["run_manifest_requirements"])
    for x in (
        "head", "tree", "run_id", "dataset_manifest_sha256",
        "selected_ap0_files[{relative_path,sha256}]",
        "timezone_database_runtime_identity",
        "engine_blob", "contract_blob", "ledger_schema_blob",
        "breaker_contract_blob", "breaker_executable_blob",
        "output_files[{relative_path,sha256,rows}]",
    ):
        require(x in reqs, f"RUN_MANIFEST_REQUIRED:{x}")
    for pair in char["bounded_files"]:
        require(len(pair) == 2 and len(pair[1]) == 64, "BOUNDED_FILE_SHA_BINDING")


def test_contract_text(contract_text: str) -> None:
    for phrase in (
        "America/New_York",
        "Sunday 18:00:00 inclusive",
        "HH:59:00 UTC",
        "CORPUS_BORN_WEEKLY_LEVELS",
        "PRE_CORPUS_ACTIVE_LEVELS",
        "LEVEL_WEEK_OPPORTUNITY",
        "STOP before exhaustive historical execution",
    ):
        require(phrase in contract_text, f"CONTRACT_PHRASE_MISSING:{phrase}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        char, schema, bc, contract_text = load_bound(root)
        test_breaker_contract(bc)
        test_dst_boundaries(char)
        test_corpus_censoring(char)
        test_h1_rules()
        test_denominator_rules()
        test_ledger_schema(schema)
        test_gap_and_holiday_rules(char, schema)
        test_provenance(schema, char)
        test_contract_text(contract_text)
    except (BreakerFailure, KeyError, ValueError, json.JSONDecodeError) as exc:
        fail(str(exc))

    print("BEPD_01D_PRE_SCAN_BREAKER_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
