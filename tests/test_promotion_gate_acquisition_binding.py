from __future__ import annotations

from types import SimpleNamespace

import tools.frozen_execution_window as frozen_module
from tools.coverage_execution_window_boundary import (
    AUTHORIZE_MASSIVE_ACQUISITION,
    BLOCKED,
    PASS,
    BoundaryDecision,
)


def test_forced_underlying_acquisition_pass_is_still_blocked_by_p1_0(monkeypatch) -> None:
    fake_frozen = SimpleNamespace(
        evidence=SimpleNamespace(frozen_state=object()),
        decision=SimpleNamespace(verdict=PASS),
    )
    monkeypatch.setattr(
        frozen_module,
        "evaluate_persisted_execution_window_freeze",
        lambda: fake_frozen,
    )
    monkeypatch.setattr(
        frozen_module,
        "evaluate_boundary",
        lambda action, state: BoundaryDecision(
            AUTHORIZE_MASSIVE_ACQUISITION,
            PASS,
            "FORCED_UNDERLYING_PASS_FOR_ADVERSARIAL_TEST",
        ),
    )

    decision = frozen_module.evaluate_acquisition_after_persisted_freeze()

    assert decision.verdict == BLOCKED
    assert decision.reason.startswith("PROMOTION_GATE:")
    assert "PASS" not in decision.reason
