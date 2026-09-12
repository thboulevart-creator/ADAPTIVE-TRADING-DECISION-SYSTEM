import hashlib
import json

import pytest

from src.context_identity import context_id


BASE = {
    "dataset_id": "DATA-001",
    "dataset_version": "v1",
    "content_hash": "sha256-content-001",
    "instrument": "NAS100",
    "granularity": "tick",
    "timezone_storage": "UTC",
    "configuration_version": "CFG-001",
}


def independent_context_id(value: dict[str, str]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "CTX-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def test_same_inputs_produce_same_context_id():
    assert context_id(BASE) == context_id(dict(BASE))


@pytest.mark.parametrize("field", tuple(BASE))
def test_changing_each_identity_component_changes_context_id(field):
    changed = dict(BASE)
    changed[field] = BASE[field] + "-changed"

    assert context_id(changed) != context_id(BASE)


def test_independent_calculation_matches_context_id():
    assert context_id(BASE) == independent_context_id(BASE)
