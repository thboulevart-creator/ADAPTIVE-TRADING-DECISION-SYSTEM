from dataclasses import replace

import pytest

from src.context import build_context
from src.context_identity import context_id
from src.data.dataset_admissibility import DatasetIdentity
from src.research_run_evidence import from_v43_report


CODE_VERSION = "963f02e93db63bef36c25d58c3634096a2247e6a"


def v43_report() -> dict:
    return {
        "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
        "version": "V4.3",
        "status": "UNVERIFIED",
        "scope": {
            "research_instrument": "Dukascopy USATECHIDXUSD",
            "execution_instrument": "VT Markets NAS100.s",
            "minimum_research_years": 5.0,
        },
        "research": {
            "files": [
                {"path": "research/a.bi5", "sha256": "aaa"},
                {"path": "research/b.bi5", "sha256": "bbb"},
            ],
            "rows": 100,
            "first": "2020-01-01T00:00:00+00:00",
            "last": "2025-01-01T00:00:00+00:00",
        },
    }


def coherent_inputs():
    report = v43_report()
    from src.research_run_evidence import _stable_hash

    source_hashes = ["aaa", "bbb"]
    dataset_id = "DATA-" + _stable_hash({"research_files": source_hashes})[:16]
    dataset_version = _stable_hash(report["research"])[:16]
    configuration_version = "CFG-" + _stable_hash(report["scope"])[:16]
    dataset = DatasetIdentity(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        content_hash="content-hash",
        format="csv",
        schema_version="tick-csv-v1",
        instrument="VT Markets NAS100.s",
        granularity="tick",
        timezone_storage="UTC",
    )
    context = build_context(
        dataset,
        configuration_version=configuration_version,
        observation_start="2020-01-01T00:00:00+00:00",
        observation_end="2025-01-01T00:00:00+00:00",
    )
    return report, dataset, context


def test_c0_valid_context_is_accepted_and_propagated() -> None:
    report, dataset, context = coherent_inputs()
    evidence = from_v43_report(report, code_version=CODE_VERSION, context=context, dataset=dataset)
    assert evidence.context_id == context.context_id


@pytest.mark.parametrize(
    "case, mutate",
    [
        ("C1", lambda c: replace(c, context_id="CTX-forged")),
        ("C2", lambda c: replace(c, dataset_id="foreign-dataset")),
        ("C3", lambda c: replace(c, dataset_version="foreign-version")),
        ("C4", lambda c: replace(c, content_hash="foreign-hash")),
        ("C5", lambda c: replace(c, instrument="foreign-instrument")),
        ("C6", lambda c: replace(c, granularity="foreign-granularity")),
        ("C7", lambda c: replace(c, timezone_storage="foreign-timezone")),
        ("C8", lambda c: replace(c, configuration_version="foreign-config")),
        (
            "C9",
            lambda c: replace(
                c,
                dataset_id="foreign-dataset",
                content_hash="foreign-hash",
                instrument="foreign-instrument",
                granularity="foreign-granularity",
            ),
        ),
    ],
)
def test_c1_to_c9_foreign_or_falsified_context_is_rejected(case, mutate) -> None:
    report, dataset, context = coherent_inputs()
    with pytest.raises(ValueError):
        from_v43_report(
            report,
            code_version=CODE_VERSION,
            context=mutate(context),
            dataset=dataset,
        )


def test_c10_absent_context_is_rejected() -> None:
    report, dataset, _ = coherent_inputs()
    with pytest.raises(ValueError):
        from_v43_report(report, code_version=CODE_VERSION, context=None, dataset=dataset)


def test_bypass_no_fallback_when_context_is_omitted() -> None:
    report, dataset, _ = coherent_inputs()
    with pytest.raises(TypeError):
        from_v43_report(report, code_version=CODE_VERSION, dataset=dataset)


def test_bypass_context_id_alone_is_rejected() -> None:
    report, dataset, context = coherent_inputs()

    class ContextIdOnly:
        def __init__(self, context_id: str) -> None:
            self.context_id = context_id

    with pytest.raises(ValueError, match="full Context"):
        from_v43_report(
            report,
            code_version=CODE_VERSION,
            context=ContextIdOnly(context.context_id),
            dataset=dataset,
        )


def test_bypass_reconstructed_context_with_wrong_identity_is_rejected() -> None:
    report, dataset, context = coherent_inputs()
    reconstructed = replace(context, instrument="reconstructed-foreign-instrument")
    with pytest.raises(ValueError, match="identity mismatch"):
        from_v43_report(
            report,
            code_version=CODE_VERSION,
            context=reconstructed,
            dataset=dataset,
        )


def test_bypass_forged_context_id_cannot_override_identity_validation() -> None:
    report, dataset, context = coherent_inputs()
    foreign = replace(context, instrument="foreign-instrument")
    forged = replace(foreign, context_id=context.context_id)
    with pytest.raises(ValueError, match="identity mismatch"):
        from_v43_report(
            report,
            code_version=CODE_VERSION,
            context=forged,
            dataset=dataset,
        )


def test_bypass_reconstruction_with_report_ids_only_is_rejected() -> None:
    report, dataset, context = coherent_inputs()
    report_ids_only = replace(
        context,
        dataset_id="DATA-reconstructed",
        dataset_version="reconstructed-version",
        content_hash="reconstructed-hash",
        context_id=context.context_id,
    )
    with pytest.raises(ValueError, match="identity mismatch"):
        from_v43_report(
            report,
            code_version=CODE_VERSION,
            context=report_ids_only,
            dataset=dataset,
        )


def test_context_identity_contract_is_deterministic_for_the_boundary() -> None:
    report, dataset, context = coherent_inputs()
    expected = context_id(
        {
            "dataset_id": dataset.dataset_id,
            "dataset_version": dataset.dataset_version,
            "content_hash": dataset.content_hash,
            "instrument": dataset.instrument,
            "granularity": dataset.granularity,
            "timezone_storage": dataset.timezone_storage,
            "configuration_version": context.configuration_version,
        }
    )
    assert context.context_id == expected
