from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from src.experiments.run_record import ExperimentRunRecord


START = datetime(2026, 9, 9, 10, 0, tzinfo=timezone.utc)
END = datetime(2026, 9, 9, 10, 5, tzinfo=timezone.utc)
HASH = "a" * 64


def make_record(**overrides) -> ExperimentRunRecord:
    values = {
        "run_id": "RUN-001",
        "experiment_id": "EXP-NAS100-001",
        "code_version": "fc01ce8c7f70648ea3d1fcf399d0194b57fc328d",
        "configuration_version": "cfg-v1",
        "dataset_id": "NAS100-TICKS",
        "dataset_version": "v1",
        "dataset_hash": HASH,
        "environment_version": "python-3.12",
        "started_at": START,
        "ended_at": END,
        "status": "COMPLETED",
    }
    values.update(overrides)
    return ExperimentRunRecord(**values)


def test_valid_terminal_record_is_constructed_and_serialized():
    record = make_record()

    assert record.status == "COMPLETED"
    assert record.to_dict()["started_at"] == START.isoformat()
    assert record.to_dict()["ended_at"] == END.isoformat()
    assert record.to_dict()["dataset_hash"] == HASH


@pytest.mark.parametrize(
    "field",
    [
        "run_id",
        "experiment_id",
        "code_version",
        "configuration_version",
        "dataset_id",
        "dataset_version",
        "environment_version",
    ],
)
def test_required_identifier_cannot_be_empty(field):
    with pytest.raises(ValueError, match=field):
        make_record(**{field: ""})


def test_missing_dataset_hash_is_rejected():
    with pytest.raises(ValueError, match="dataset_hash"):
        make_record(dataset_hash="")


@pytest.mark.parametrize("dataset_hash", ["a" * 63, "a" * 65, "z" * 64])
def test_invalid_dataset_hash_is_rejected(dataset_hash):
    with pytest.raises(ValueError, match="dataset_hash"):
        make_record(dataset_hash=dataset_hash)


def test_end_before_start_is_rejected():
    with pytest.raises(ValueError, match="ended_at"):
        make_record(ended_at=datetime(2026, 9, 9, 9, 59, tzinfo=timezone.utc))


def test_invalid_status_is_rejected():
    with pytest.raises(ValueError, match="status"):
        make_record(status="RUNNING")


def test_invalidated_is_distinct_from_failed():
    invalidated = make_record(status="INVALIDATED")
    failed = make_record(status="FAILED")

    assert invalidated.status != failed.status
    assert invalidated.to_dict()["status"] == "INVALIDATED"


def test_record_is_immutable():
    record = make_record()

    with pytest.raises(FrozenInstanceError):
        record.status = "FAILED"


def test_all_frozen_terminal_statuses_are_supported():
    for status in ("COMPLETED", "FAILED", "BLOCKED", "ABORTED", "INVALIDATED"):
        assert make_record(status=status).status == status
