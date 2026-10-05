"""P1-21 executable breaker, frozen before real-producer capability implementation."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import p1_12c_qualified_producer_execution as p12c

ROOT = Path(__file__).resolve().parents[1]
FROZEN = json.loads((ROOT / "GOVERNANCE" / "P1-21-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json").read_text(encoding="utf-8"))
EXPECTED_IDS = [f"P121-B{i:02d}" for i in range(1, 30)]
assert [row["id"] for row in FROZEN["cases"]] == EXPECTED_IDS
BY_ID = {row["id"]: row for row in FROZEN["cases"]}


def _expect(case_id: str) -> None:
    if not hasattr(p12c, "validate_real_producer_capability_attack"):
        pytest.fail("P1_21_REAL_PRODUCER_CAPABILITY_ABSENT_EXPECTED_RED", pytrace=False)
    out = p12c.validate_real_producer_capability_attack(case_id)
    assert out["status"] in {"BLOCKED", "REJECTED"}, out
    assert out["reason"] == BY_ID[case_id]["expected"], out


@pytest.mark.parametrize("case_id", EXPECTED_IDS)
def test_p1_21_frozen_breakers(case_id: str):
    _expect(case_id)
