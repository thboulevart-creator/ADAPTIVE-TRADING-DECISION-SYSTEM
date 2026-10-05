from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

CONTRACT_PATH = Path("GOVERNANCE/BEPD-01B-FROZEN-EXECUTABLE-SEMANTIC-BREAKER-V0.1.json")
BEPD01A_CONTRACT_PATH = Path("GOVERNANCE/BEPD-01A-WEEKLY-LIQUIDITY-MEASUREMENT-CONTRACT-V0.1.md")
FIXTURE_PATH = Path("GOVERNANCE/BEPD-01A-WEEKLY-LIQUIDITY-CALIBRATION-FIXTURE-R1.json")
ADJUDICATION_PATH = Path("GOVERNANCE/BEPD-01A-HUMAN-ADJUDICATION-2026-10-05.md")\nCORRECTION_PATH = Path("GOVERNANCE/BEPD-01A-TARGETED-FIXTURE-IDENTITY-CORRECTION-R1.md")\nCORRECTION_ADJUDICATION_PATH = Path("GOVERNANCE/BEPD-01A-TARGETED-FIXTURE-IDENTITY-CORRECTION-R1-HUMAN-ADJUDICATION-2026-10-05.md")
TARGET_PATH = Path("tools/bepd_01_weekly_liquidity_engine.py")

EXPECTED_GIT_BLOBS = {
    BEPD01A_CONTRACT_PATH: "341f6267f7f1add350759d6d95dfebfb5b9e46f7",
    FIXTURE_PATH: "d2e663eaef865507c1cb92f5baa0074dcfc11032",
    ADJUDICATION_PATH: "66ae9ff193c5734c32490300ef24d2c1895492c1",
    CORRECTION_PATH: "4def4dbcfa314c3be3d12129ebbc6a854619dd32",\n    CORRECTION_ADJUDICATION_PATH: "d1b9e466e9647cb748634c77eae24fa1437dd186",\n    CONTRACT_PATH: "d602a0666ab92662f2355ce0f44893934a7943a1",
}
EXPECTED_FIXTURE_SHA256 = "ceadd3844b9c10e52fa750d9e680e9124ed37ac139621c8b9ad5c0a3724385b2"\nEXPECTED_FIXTURE_SEMANTIC_SHA256 = "5fbaae622527a4f7499fd18825026ecc45319d76efa4af743bb866e540dff6dd"


class BreakerFailure(AssertionError):
    pass


def fail(code: str) -> None:
    print(code)
    raise SystemExit(1)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def worktree_bytes(root: Path, rel: Path) -> bytes:
    p = root / rel
    if not p.is_file():
        raise BreakerFailure(f"MISSING_BOUND_FILE:{rel.as_posix()}")
    return p.read_bytes()


def git_object_bytes(root: Path, rel: Path) -> bytes | None:
    try:
        cp = subprocess.run(
            ["git", "-C", str(root), "show", f"HEAD:{rel.as_posix()}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout


def git_object_sha(root: Path, rel: Path) -> str | None:
    try:
        cp = subprocess.run(
            ["git", "-C", str(root), "rev-parse", f"HEAD:{rel.as_posix()}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )
    except OSError:
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def canonical_bytes(root: Path, rel: Path) -> bytes:
    data = git_object_bytes(root, rel)
    return data if data is not None else worktree_bytes(root, rel)


def canonical_blob_sha(root: Path, rel: Path) -> str:
    sha = git_object_sha(root, rel)
    return sha if sha is not None else git_blob_sha(worktree_bytes(root, rel))


def assert_equal(actual, expected, code: str) -> None:
    if actual != expected:
        raise BreakerFailure(f"{code}: expected={expected!r} actual={actual!r}")


def assert_close(actual: float, expected: float, code: str, tol: float = 1e-9) -> None:
    if abs(float(actual) - float(expected)) > tol:
        raise BreakerFailure(f"{code}: expected={expected!r} actual={actual!r}")


def validate_frozen_inputs(root: Path) -> tuple[dict, dict]:
    for rel, expected in EXPECTED_GIT_BLOBS.items():
        assert_equal(canonical_blob_sha(root, rel), expected, f"GIT_BLOB_MISMATCH:{rel.as_posix()}")

    fixture_bytes = canonical_bytes(root, FIXTURE_PATH)
    assert_equal(
        hashlib.sha256(fixture_bytes).hexdigest(),
        EXPECTED_FIXTURE_SHA256,
        "FIXTURE_SHA256_MISMATCH",
    )

    contract = json.loads(canonical_bytes(root, CONTRACT_PATH).decode("utf-8"))
    fixture = json.loads(fixture_bytes.decode("utf-8"))
    semantic_bytes = json.dumps(fixture, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert_equal(hashlib.sha256(semantic_bytes).hexdigest(), EXPECTED_FIXTURE_SEMANTIC_SHA256, "FIXTURE_SEMANTIC_SHA256_MISMATCH")

    assert_equal(contract["status"], "FROZEN_TEST_FIRST_RED_EXPECTED", "BREAKER_STATUS_DRIFT")
    assert_equal(contract["bindings"]["bepd_01a_contract_blob"], EXPECTED_GIT_BLOBS[BEPD01A_CONTRACT_PATH], "BOUND_CONTRACT_DRIFT")
    assert_equal(contract["bindings"]["bepd_01a_fixture_blob"], EXPECTED_GIT_BLOBS[FIXTURE_PATH], "BOUND_FIXTURE_DRIFT")\n    assert_equal(contract["bindings"]["bepd_01a_fixture_sha256"], EXPECTED_FIXTURE_SHA256, "BOUND_FIXTURE_SHA256_DRIFT")\n    assert_equal(contract["bindings"]["bepd_01a_fixture_semantic_sha256"], EXPECTED_FIXTURE_SEMANTIC_SHA256, "BOUND_FIXTURE_SEMANTIC_SHA256_DRIFT")\n    assert_equal(contract["bindings"]["bepd_01a_fixture_correction_blob"], EXPECTED_GIT_BLOBS[CORRECTION_PATH], "BOUND_FIXTURE_CORRECTION_DRIFT")\n    assert_equal(contract["bindings"]["bepd_01a_fixture_correction_human_adjudication_blob"], EXPECTED_GIT_BLOBS[CORRECTION_ADJUDICATION_PATH], "BOUND_FIXTURE_CORRECTION_ADJUDICATION_DRIFT")
    assert_equal(contract["bindings"]["bepd_01a_human_adjudication_blob"], EXPECTED_GIT_BLOBS[ADJUDICATION_PATH], "BOUND_ADJUDICATION_DRIFT")
    assert_equal(contract["authority"]["general_implementation"], False, "AUTHORITY_LAUNDERING_IMPLEMENTATION")
    assert_equal(contract["authority"]["five_year_scan"], False, "AUTHORITY_LAUNDERING_FIVE_YEAR")
    assert_equal(contract["authority"]["strategy"], False, "AUTHORITY_LAUNDERING_STRATEGY")

    assert_equal(fixture["price_surface"], "mid", "FIXTURE_PRICE_SURFACE_DRIFT")
    assert_equal(fixture["calendar_timezone"], "Europe/Paris", "FIXTURE_TIMEZONE_DRIFT")
    assert_equal(fixture["h1_rule"]["strict_inequality"], True, "FIXTURE_STRICTNESS_DRIFT")
    assert_equal(len(fixture["weekly_bars"]), 6, "FIXTURE_WEEK_COUNT_DRIFT")
    assert_equal(len(fixture["expected_clusters"]), 5, "FIXTURE_CLUSTER_COUNT_DRIFT")

    clusters = {x["target_week"]: x for x in fixture["expected_clusters"]}
    assert_equal(len(clusters["2026-01-19"]["events"]), 1, "FIXTURE_JAN19_EVENT_COUNT")
    assert_equal(len(clusters["2026-01-26"]["events"]), 2, "FIXTURE_JAN26_EVENT_COUNT")
    assert_equal(len(clusters["2026-02-02"]["events"]), 2, "FIXTURE_FEB02_EVENT_COUNT")
    assert_equal(len(clusters["2026-02-09"]["events"]), 0, "FIXTURE_FEB09_EVENT_COUNT")
    assert_equal(len(clusters["2026-02-16"]["events"]), 1, "FIXTURE_FEB16_EVENT_COUNT")

    feb02 = clusters["2026-02-02"]["events"]
    assert any(float(x["close_displacement"]) < 0 for x in feb02), "FIXTURE_MUST_CONTAIN_NEGATIVE_D"
    assert any(float(x["close_displacement"]) > 0 for x in feb02), "FIXTURE_MUST_CONTAIN_POSITIVE_D"
    return contract, fixture


def load_target(root: Path):
    target = root / TARGET_PATH
    if not target.is_file():
        fail("BEPD_01B_RED_MISSING_IMPLEMENTATION")
    spec = importlib.util.spec_from_file_location("bepd_01_weekly_liquidity_engine", target)
    if spec is None or spec.loader is None:
        fail("BEPD_01B_RED_TARGET_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ("evaluate_level_event", "advance_week", "replay_calibration"):
        if not hasattr(module, name):
            fail(f"BEPD_01B_RED_MISSING_CALLABLE:{name}")
    return module


def bar(close: float, high: float | None = None, low: float | None = None) -> dict:
    return {
        "close": float(close),
        "high": float(close if high is None else high),
        "low": float(close if low is None else low),
    }


def test_evaluate_level_event(m) -> None:
    r = m.evaluate_level_event("HIGH", 100.0, [bar(99.5, high=101.0)], 95.0)
    assert_equal(r["taken"], False, "B02_WICK_HIGH_MUST_NOT_TAKE")

    r = m.evaluate_level_event("LOW", 100.0, [bar(100.5, low=99.0)], 105.0)
    assert_equal(r["taken"], False, "B03_WICK_LOW_MUST_NOT_TAKE")

    assert_equal(m.evaluate_level_event("HIGH", 100.0, [bar(100.0)], 90.0)["taken"], False, "B04_HIGH_EQUALITY")
    assert_equal(m.evaluate_level_event("LOW", 100.0, [bar(100.0)], 110.0)["taken"], False, "B05_LOW_EQUALITY")

    r = m.evaluate_level_event("HIGH", 100.0, [bar(99), bar(101), bar(100), bar(99)], 90.0)
    assert_equal(r["taken"], True, "B06_HIGH_MUST_TAKE")
    assert_equal(r["take_index"], 1, "B06_FIRST_HIGH_TAKE_INDEX")
    assert_equal(r["reintegration_index"], 3, "B08_HIGH_EQUALITY_NOT_REINTEGRATION")
    assert_equal(r["same_week_reintegration"], True, "B08_HIGH_REINTEGRATION_FLAG")
    assert_close(r["close_displacement"], 10.0, "B06_HIGH_D")

    r = m.evaluate_level_event("HIGH", 100.0, [bar(101, high=105, low=95), bar(99)], 98.0)
    assert_equal(r["take_index"], 0, "B07_TAKE_INDEX")
    assert_equal(r["reintegration_index"], 1, "B07_REINTEGRATION_STRICTLY_LATER")

    r = m.evaluate_level_event("LOW", 100.0, [bar(99), bar(100), bar(101)], 110.0)
    assert_equal(r["take_index"], 0, "B09_LOW_TAKE_INDEX")
    assert_equal(r["reintegration_index"], 2, "B09_LOW_EQUALITY_NOT_REINTEGRATION")
    assert_close(r["close_displacement"], 10.0, "B09_LOW_D")

    r = m.evaluate_level_event("HIGH", 100.0, [bar(101), bar(99)], 105.0)
    assert_equal(r["taken"], True, "B10_NEGATIVE_TAKEN")
    assert_close(r["close_displacement"], -5.0, "B10_NEGATIVE_D_RETAINED")

    r = m.evaluate_level_event("HIGH", 100.0, [bar(101), bar(102)], 102.0)
    assert_equal(r["taken"], True, "B11_TAKE_RETAINED")
    assert_equal(r["reintegration_index"], None, "B11_NO_REINTEGRATION_INDEX")
    assert_equal(r["same_week_reintegration"], False, "B11_REINTEGRATION_FALSE")
    assert_close(r["close_displacement"], -2.0, "B11_D_RETAINED")

    try:
        m.evaluate_level_event("SIDEWAYS", 100.0, [bar(101)], 100.0)
    except ValueError:
        pass
    else:
        raise BreakerFailure("B17_INVALID_SIDE_MUST_RAISE_VALUE_ERROR")


def normalize_active(rows: list[dict]) -> list[dict]:
    keys = ("source_week", "side", "level", "age_weeks")
    return sorted(
        [{k: x[k] for k in keys} for x in rows],
        key=lambda x: (x["source_week"], x["side"], float(x["level"])),
    )


def test_advance_week(m) -> None:
    active = [
        {"source_week": "W1", "side": "HIGH", "level": 100.0, "age_weeks": 0},
        {"source_week": "W1", "side": "LOW", "level": 90.0, "age_weeks": 0},
    ]
    out = m.advance_week(active, "W2", [bar(95), bar(105), bar(95)], 96.0, 110.0, 80.0)
    events = out["cluster"]["events"]
    assert_equal(len(events), 1, "B12_ONE_CONSUMED_EVENT")
    assert_equal(events[0]["side"], "HIGH", "B12_CONSUMED_HIGH")
    after = normalize_active(out["active_after"])
    if any(x["source_week"] == "W1" and x["side"] == "HIGH" for x in after):
        raise BreakerFailure("B12_CONSUMED_LEVEL_REACTIVATED")
    low = [x for x in after if x["source_week"] == "W1" and x["side"] == "LOW"]
    assert_equal(len(low), 1, "B13_OLDER_LOW_PERSISTS")
    assert_equal(low[0]["age_weeks"], 1, "B13_OLDER_LOW_AGES")

    active = [
        {"source_week": "W0", "side": "HIGH", "level": 110.0, "age_weeks": 1},
        {"source_week": "W1", "side": "HIGH", "level": 100.0, "age_weeks": 0},
    ]
    out = m.advance_week(active, "W2", [bar(105), bar(115), bar(95)], 105.0, 120.0, 80.0)
    events = out["cluster"]["events"]
    assert_equal(out["cluster"]["target_week"], "W2", "B14_CLUSTER_ID")
    assert_equal(len(events), 2, "B14_TWO_LEVEL_EVENTS")
    ds = sorted(float(x["close_displacement"]) for x in events)
    assert_equal(ds, [-5.0, 5.0], "B15_RETAIN_POSITIVE_AND_NEGATIVE")

    out = m.advance_week([], "W3", [bar(150)], 150.0, 140.0, 80.0)
    assert_equal(len(out["cluster"]["events"]), 0, "B16_NO_SELF_CONSUMPTION")
    after = normalize_active(out["active_after"])
    assert_equal(
        after,
        [
            {"source_week": "W3", "side": "HIGH", "level": 140.0, "age_weeks": 0},
            {"source_week": "W3", "side": "LOW", "level": 80.0, "age_weeks": 0},
        ],
        "B16_ADD_NEW_LEVELS_AFTER_EVALUATION",
    )


def test_authority_constants(m) -> None:
    assert_equal(getattr(m, "PRICE_SURFACE", None), "mid", "B18_PRICE_SURFACE")
    assert_equal(getattr(m, "MID_IS_EXECUTION_PRICE", None), False, "B18_EXECUTION_PRICE_LAUNDERING")
    assert_equal(getattr(m, "FIVE_YEAR_SCAN_AUTHORIZED", None), False, "B20_FIVE_YEAR_AUTHORITY")
    assert_equal(getattr(m, "TRADING_AUTHORITY", None), False, "B20_TRADING_AUTHORITY")


def test_calibration_replay(m, fixture: dict, ap0_root: Path | None) -> None:
    if ap0_root is None:
        print("BEPD_01B_BLOCKED_AP0_ROOT_REQUIRED_FOR_GREEN")
        raise SystemExit(2)
    replay = m.replay_calibration(ap0_root, fixture)
    assert_equal(replay["weekly_bars"], fixture["weekly_bars"], "B19_WEEKLY_BARS_EXACT_REPLAY")
    assert_equal(replay["expected_clusters"], fixture["expected_clusters"], "B19_CLUSTERS_EXACT_REPLAY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--ap0-root", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        _, fixture = validate_frozen_inputs(root)
    except (BreakerFailure, KeyError, json.JSONDecodeError) as exc:
        fail(f"BEPD_01B_BREAKER_INPUT_FAILURE:{exc}")

    m = load_target(root)

    try:
        test_authority_constants(m)
        test_evaluate_level_event(m)
        test_advance_week(m)
        ap0_root = args.ap0_root
        if ap0_root is None:
            env = os.environ.get("ATDS_AP0_ROOT")
            ap0_root = Path(env) if env else None
        test_calibration_replay(m, fixture, ap0_root)
    except BreakerFailure as exc:
        fail(f"BEPD_01B_SEMANTIC_FAILURE:{exc}")

    print("BEPD_01B_BREAKER_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())