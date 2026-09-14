import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "tools" / "download_dukascopy_tick_corpus.py"


def _run_dry(tmp_path: Path, day: str, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--start-date",
            day,
            "--end-date",
            day,
            "--output",
            str(tmp_path / "data"),
            "--manifest",
            str(tmp_path / "manifest.jsonl"),
            "--dry-run",
            *extra,
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _last_json(stdout: str) -> dict:
    # The downloader prints line-level classifications before its indented final
    # object, so locate the final multi-line JSON object by its instrument marker.
    marker = '{\n  "instrument": "USATECHIDXUSD"'
    index = stdout.rfind(marker)
    assert index >= 0, stdout
    return json.loads(stdout[index:])


def test_unqualified_special_date_blocks_before_any_network(tmp_path: Path) -> None:
    # Christmas Observed 2021 remains unresolved after Batch 01 adjudication.
    result = _run_dry(tmp_path, "2021-12-24")
    assert result.returncode == 2
    assert "CALENDAR_COVERAGE_GATE verdict=BLOCKED" in result.stdout

    summary = _last_json(result.stdout)
    assert summary["verdict"] == "BLOCKED"
    assert summary["network_calls"] == 0
    assert summary["calendar_coverage_unresolved_dates"] > 0


def test_probe_can_inspect_unqualified_date_but_cannot_upgrade_to_pass(
    tmp_path: Path,
) -> None:
    result = _run_dry(
        tmp_path,
        "2021-12-24",
        "--calendar-qualification-probe",
    )
    assert result.returncode == 2
    assert "CALENDAR_CLASSIFICATION" in result.stdout

    summary = _last_json(result.stdout)
    assert summary["calendar_qualification_probe"] is True
    assert summary["calendar_coverage_verdict"] == "BLOCKED"
    assert summary["network_calls"] == 0
    assert summary["verdict"] == "BLOCKED"
    assert summary["reason"] == "CALENDAR_EVIDENCE_INCOMPLETE_PROBE_ONLY"


def test_regular_non_candidate_day_passes_calendar_coverage_gate(tmp_path: Path) -> None:
    result = _run_dry(tmp_path, "2025-01-22")
    assert result.returncode == 0, result.stdout + result.stderr
    summary = _last_json(result.stdout)
    assert summary["calendar_coverage_verdict"] == "PASS"
    assert summary["expected_open_slots"] == 23
    assert summary["expected_closed_slots"] == 1
    assert summary["verdict"] == "PASS"


def test_qualified_special_day_passes_calendar_coverage_gate(tmp_path: Path) -> None:
    result = _run_dry(tmp_path, "2025-01-09")
    assert result.returncode == 0, result.stdout + result.stderr
    summary = _last_json(result.stdout)
    assert summary["calendar_coverage_verdict"] == "PASS"
    assert summary["expected_open_slots"] == 16
    assert summary["expected_closed_slots"] == 8
    assert summary["verdict"] == "PASS"
