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


def test_data_to_context_preserves_dataset_identity():
    context = build_context(
        DATASET,
        configuration_version="CFG-001",
        observation_start="2025-01-01T00:00:00+00:00",
        observation_end="2025-01-01T01:00:00+00:00",
    )

    assert validate_context(context, DATASET)
    assert context.dataset_id == DATASET.dataset_id
    assert context.dataset_version == DATASET.dataset_version
    assert context.content_hash == DATASET.content_hash


def test_foreign_dataset_identity_is_rejected():
    context = build_context(
        DATASET,
        configuration_version="CFG-001",
        observation_start="2025-01-01T00:00:00+00:00",
        observation_end="2025-01-01T01:00:00+00:00",
    )
    foreign = DatasetIdentity(
        dataset_id="DATA-FOREIGN",
        dataset_version=DATASET.dataset_version,
        content_hash=DATASET.content_hash,
        format=DATASET.format,
        schema_version=DATASET.schema_version,
        instrument=DATASET.instrument,
        granularity=DATASET.granularity,
        timezone_storage=DATASET.timezone_storage,
    )

    assert not validate_context(context, foreign)


def test_mutating_context_dataset_id_invalidates_context():
    context = build_context(
        DATASET,
        configuration_version="CFG-001",
        observation_start="2025-01-01T00:00:00+00:00",
        observation_end="2025-01-01T01:00:00+00:00",
    )
    mutated = context.__class__(
        **{**context.__dict__, "dataset_id": "DATA-FOREIGN"}
    )

    assert not validate_context(mutated, DATASET)
