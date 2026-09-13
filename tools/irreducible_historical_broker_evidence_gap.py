from __future__ import annotations

from dataclasses import dataclass


PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"

GOVERNANCE_CONTRACT = "IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1"


@dataclass(frozen=True)
class EvidenceBundle:
    """Evidence state for one historical broker-session fact.

    Boolean fields deliberately encode only evidence classes that may affect the
    verdict. Corroborative-only material (cross-year examples, HTTP failures,
    missing BI5 data, generic holiday names, regular-session similarity) has no
    PASS-bearing field and therefore cannot be accumulated into a false PASS.
    """

    # PASS-A: exact live/official broker witness for target date+instrument+hours.
    exact_broker_primary: bool = False

    # PASS-B: exact archived copy of official broker witness.
    exact_broker_archive: bool = False
    broker_archive_provenance_verified: bool = False

    # PASS-C: exact-date broker event + explicit special-session mapping + exact
    # reference/exchange timing.
    date_specific_broker_event: bool = False
    broker_target_instrument_explicit: bool = False
    broker_special_session_mapping_contract: bool = False
    exact_exchange_schedule: bool = False
    exchange_provenance_verified: bool = False

    # Whether normal + archive retrieval was materially exhausted.
    retrieval_exhausted: bool = False

    # Hard invalidation conditions.
    strong_broker_contradiction: bool = False
    witness_identity_mismatch: bool = False
    archive_provenance_falsified: bool = False
    bucket_conversion_contradiction: bool = False


@dataclass(frozen=True)
class GapDecision:
    verdict: str
    reason: str
    route: str | None
    contract: str = GOVERNANCE_CONTRACT


def qualify_evidence_gap(bundle: EvidenceBundle) -> GapDecision:
    """Qualify an irreducible historical broker-evidence gap.

    Order is intentional:
    1. proven contradictions/malformed witness identity are FAIL;
    2. exact broker proof wins via PASS-A/PASS-B;
    3. proxy reconstruction is allowed only through the fully explicit PASS-C
       chain;
    4. all weaker combinations remain BLOCKED.
    """

    if bundle.strong_broker_contradiction:
        return GapDecision(
            FAIL,
            "CONTRADICTORY_EXACT_BROKER_EVIDENCE",
            None,
        )

    if bundle.witness_identity_mismatch:
        return GapDecision(
            FAIL,
            "BROKER_WITNESS_DATE_OR_INSTRUMENT_MISMATCH",
            None,
        )

    if bundle.archive_provenance_falsified:
        return GapDecision(
            FAIL,
            "BROKER_ARCHIVE_PROVENANCE_FALSIFIED",
            None,
        )

    if bundle.bucket_conversion_contradiction:
        return GapDecision(
            FAIL,
            "BUCKET_CONVERSION_CONTRADICTS_PROVEN_TIMING",
            None,
        )

    if bundle.exact_broker_primary:
        return GapDecision(PASS, "EXACT_PRIMARY_BROKER_WITNESS", "PASS-A")

    if (
        bundle.exact_broker_archive
        and bundle.broker_archive_provenance_verified
    ):
        return GapDecision(PASS, "EXACT_ARCHIVED_BROKER_WITNESS", "PASS-B")

    pass_c = all(
        (
            bundle.date_specific_broker_event,
            bundle.broker_target_instrument_explicit,
            bundle.broker_special_session_mapping_contract,
            bundle.exact_exchange_schedule,
            bundle.exchange_provenance_verified,
        )
    )
    if pass_c:
        return GapDecision(
            PASS,
            "BROKER_EVENT_PLUS_EXPLICIT_SPECIAL_SESSION_MAPPING_PLUS_EXCHANGE",
            "PASS-C",
        )

    if bundle.retrieval_exhausted:
        return GapDecision(
            BLOCKED,
            "IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP",
            None,
        )

    return GapDecision(BLOCKED, "RETRIEVAL_INCOMPLETE", None)
