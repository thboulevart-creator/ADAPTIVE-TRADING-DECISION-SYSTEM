from __future__ import annotations

import json
import re
from pathlib import Path

MANIFEST = Path(__file__).with_name("historical_regression_baselines.json")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def _load() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_historical_regression_manifest_is_exact_and_fail_closed() -> None:
    data = _load()
    entries = data["entries"]
    files = {nodeid.split("::", 1)[0] for nodeid in entries}

    assert data["schema"] == "HISTORICAL_REGRESSION_BASELINES_V1"
    assert data["historical_node_count"] == len(entries) == 115
    assert data["historical_file_count"] == len(files) == 42
    assert len(set(entries)) == 115
    assert all(nodeid.startswith("tests/") and "::test_" in nodeid for nodeid in entries)
    assert all(_COMMIT_RE.fullmatch(commit) for commit in entries.values())


def test_historical_regression_manifest_preserves_real_tests_not_skips() -> None:
    data = _load()
    for nodeid in data["entries"]:
        path_text, test_name = nodeid.split("::", 1)
        source = Path(path_text).read_text(encoding="utf-8")
        assert f"def {test_name}(" in source
