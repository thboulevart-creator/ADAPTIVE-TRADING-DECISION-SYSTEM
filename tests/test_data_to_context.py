from dataclasses import replace

import pytest

from src.context import build_context, validate_context
from src.data.dataset_admissibility import DatasetIdentity


DATASET = DatasetIdentity(
    dataset_id="DATA-001",
    dataset_version="v1",
    content_hash="sha256-content-001",
    format="csv",
    schema_version="tick-csv-v1",
    instrument="NAS100",
    granularity="tick",
    timezone_storage="UTC",
)


def make_context():
    return build_context(
        DATASET,
        configuration_version="CFG-001",
        observation_start="2025-01-01T00:00:00+00:00",
        observation_end="2025-01-01T01:00:00+00:00",
    )


def test_data_to_context_preserves_dataset_identity():
    context = make_context()
    assert validate_context(context, DATASET)
    assert context.dataset_id == DATASET.dataset_id
    assert context.dataset_version == DATASET.dataset_version
    assert context.content_hash == DATASET.content_hash


@pytest.mark.parametrize(
    "field,foreign_value",
    [
        ("dataset_id", "DATA-FOREIGN"),
        ("dataset_version", "v-FOREIGN"),
        ("content_hash", "sha256-FOREIGN"),
        ("instrument", "OTHER-INSTRUMENT"),
        ("granularity", "m1"),
        ("timezone_storage", "Europe/Paris"),
    ],
)
def test_foreign_dataset_identity_is_rejected_for_every_identity_field(field, foreign_value):
    context = make_context()
    foreign = replace(DATASET, **{field: foreign_value})
    assert not validate_context(context, foreign), field


def test_foreign_configuration_is_rejected():
    context = make_context()
    foreign_configuration = replace(context, configuration_version="CFG-FOREIGN")
    assert not validate_context(foreign_configuration, DATASET)


@pytest.mark.parametrize(
    "field,foreign_value",
    [
        ("dataset_id", "DATA-FOREIGN"),
        ("dataset_version", "v-FOREIGN"),
        ("content_hash", "sha256-FOREIGN"),
        ("instrument", "OTHER-INSTRUMENT"),
        ("granularity", "m1"),
        ("timezone_storage", "Europe/Paris"),
        ("configuration_version", "CFG-FOREIGN"),
    ],
)
def test_mutated_context_identity_is_rejected_for_every_identity_field(field, foreign_value):
    context = make_context()
    mutated = replace(context, **{field: foreign_value})
    assert not validate_context(mutated, DATASET), field


def test_combined_foreign_identity_is_rejected():
    context = make_context()
    mutated = replace(
        context,
        dataset_id="DATA-FOREIGN",
        dataset_version="v-FOREIGN",
        content_hash="sha256-FOREIGN",
        instrument="OTHER-INSTRUMENT",
        granularity="m1",
        timezone_storage="Europe/Paris",
        configuration_version="CFG-FOREIGN",
    )
    assert not validate_context(mutated, DATASET)
