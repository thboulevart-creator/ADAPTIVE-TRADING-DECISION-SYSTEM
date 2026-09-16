from __future__ import annotations

import importlib.util

from tools.coverage_execution_window_boundary import BLOCKED
from tools.frozen_execution_window import evaluate_acquisition_after_persisted_freeze


def test_p1_0_existing_acquisition_still_blocked_before_gate() -> None:
    decision = evaluate_acquisition_after_persisted_freeze()
    assert decision.verdict == BLOCKED


def test_p1_0_promotion_gate_runtime_must_exist() -> None:
    # Pre-correction breaker: this is expected to FAIL until the explicit
    # promotion gate is implemented. The inherited acquisition boundary
    # above must remain blocked while this new boundary is absent.
    assert importlib.util.find_spec("src.promotion_gate") is not None
