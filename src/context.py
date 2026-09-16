"""Minimal CONTEXT object at the DATA -> CONTEXT boundary.

CONTEXT describes the data and execution/research configuration relevant to an
observation. It deliberately contains no decision, action, result, prediction,
or future-derived information.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.context_identity import context_id
from src.data.dataset_admissibility import DatasetIdentity


@dataclass(frozen=True)
class Context:
    context_id: str
    dataset_id: str
    dataset_version: str
    content_hash: str
    instrument: str
    granularity: str
    timezone_storage: str
    configuration_version: str
    observation_start: str
    observation_end: str


def build_context(
    dataset: DatasetIdentity,
    *,
    configuration_version: str,
    observation_start: str,
    observation_end: str,
) -> Context:
    """Create a CONTEXT directly from an identified dataset and explicit bounds."""
    identity = {
        "dataset_id": dataset.dataset_id,
        "dataset_version": dataset.dataset_version,
        "content_hash": dataset.content_hash,
        "instrument": dataset.instrument,
        "granularity": dataset.granularity,
        "timezone_storage": dataset.timezone_storage,
        "configuration_version": configuration_version,
    }
    return Context(
        context_id=context_id(identity),
        dataset_id=dataset.dataset_id,
        dataset_version=dataset.dataset_version,
        content_hash=dataset.content_hash,
        instrument=dataset.instrument,
        granularity=dataset.granularity,
        timezone_storage=dataset.timezone_storage,
        configuration_version=configuration_version,
        observation_start=observation_start,
        observation_end=observation_end,
    )


def validate_context(context: Context, dataset: DatasetIdentity) -> bool:
    """Require the CONTEXT identity to remain anchored to the supplied DATA."""
    identity = {
        "dataset_id": context.dataset_id,
        "dataset_version": context.dataset_version,
        "content_hash": context.content_hash,
        "instrument": context.instrument,
        "granularity": context.granularity,
        "timezone_storage": context.timezone_storage,
        "configuration_version": context.configuration_version,
    }
    return (
        context.context_id == context_id(identity)
        and context.dataset_id == dataset.dataset_id
        and context.dataset_version == dataset.dataset_version
        and context.content_hash == dataset.content_hash
        and context.instrument == dataset.instrument
        and context.granularity == dataset.granularity
        and context.timezone_storage == dataset.timezone_storage
    )
