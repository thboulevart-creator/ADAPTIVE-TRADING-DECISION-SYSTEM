from __future__ import annotations
import pytest

MARKER="G05_01_WORKSPACE_RUNTIME_ABSENT_EXPECTED_RED"
CASE_IDS=["G0501-B01","G0501-B02","G0501-B03","G0501-B04","G0501-B05","G0501-B06","G0501-B07","G0501-B08","G0501-B09","G0501-B10","G0501-B11","G0501-B12","G0501-B13","G0501-B14","G0501-B15","G0501-B16","G0501-B17","G0501-B18","G0501-B19","G0501-B20","G0501-B21","G0501-B22","G0501-B23","G0501-B24","G0501-B25","G0501-B26","G0501-B27","G0501-B28","G0501-B29","G0501-B30"]

def _runtime():
    try:
        import tools.g05_01_workspace_dry_readiness as m
    except ModuleNotFoundError:
        pytest.fail(MARKER)
    return m

@pytest.mark.parametrize("case_id", CASE_IDS)
def test_g05_01_frozen_breakers(case_id):
    m=_runtime()
    assert m.evaluate_frozen_breaker_case(case_id) is True
