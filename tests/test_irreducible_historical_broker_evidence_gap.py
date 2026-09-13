from tools.irreducible_historical_broker_evidence_gap import (
    BLOCKED,
    FAIL,
    PASS,
    EvidenceBundle,
    qualify_evidence_gap,
)


def test_exact_primary_broker_witness_passes() -> None:
    decision = qualify_evidence_gap(EvidenceBundle(exact_broker_primary=True))
    assert decision.verdict == PASS
    assert decision.route == "PASS-A"


def test_exact_archived_broker_witness_requires_verified_provenance() -> None:
    unverified = qualify_evidence_gap(
        EvidenceBundle(
            exact_broker_archive=True,
            retrieval_exhausted=True,
        )
    )
    assert unverified.verdict == BLOCKED

    verified = qualify_evidence_gap(
        EvidenceBundle(
            exact_broker_archive=True,
            broker_archive_provenance_verified=True,
        )
    )
    assert verified.verdict == PASS
    assert verified.route == "PASS-B"


def test_pass_c_requires_every_component() -> None:
    complete = dict(
        date_specific_broker_event=True,
        broker_target_instrument_explicit=True,
        broker_special_session_mapping_contract=True,
        exact_exchange_schedule=True,
        exchange_provenance_verified=True,
    )

    decision = qualify_evidence_gap(EvidenceBundle(**complete))
    assert decision.verdict == PASS
    assert decision.route == "PASS-C"

    for missing in complete:
        weakened = complete.copy()
        weakened[missing] = False
        decision = qualify_evidence_gap(
            EvidenceBundle(**weakened, retrieval_exhausted=True)
        )
        assert decision.verdict == BLOCKED, missing


def test_exchange_only_never_passes() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            exact_exchange_schedule=True,
            exchange_provenance_verified=True,
            retrieval_exhausted=True,
        )
    )
    assert decision.verdict == BLOCKED


def test_same_date_broker_event_plus_exchange_without_mapping_never_passes() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            date_specific_broker_event=True,
            broker_target_instrument_explicit=True,
            exact_exchange_schedule=True,
            exchange_provenance_verified=True,
            retrieval_exhausted=True,
        )
    )
    assert decision.verdict == BLOCKED


def test_mapping_plus_exchange_without_same_date_broker_event_never_passes() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            broker_special_session_mapping_contract=True,
            exact_exchange_schedule=True,
            exchange_provenance_verified=True,
            retrieval_exhausted=True,
        )
    )
    assert decision.verdict == BLOCKED


def test_generic_broker_event_without_explicit_target_instrument_never_passes() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            date_specific_broker_event=True,
            broker_target_instrument_explicit=False,
            broker_special_session_mapping_contract=True,
            exact_exchange_schedule=True,
            exchange_provenance_verified=True,
            retrieval_exhausted=True,
        )
    )
    assert decision.verdict == BLOCKED


def test_cross_year_broker_pattern_has_no_pass_bearing_field() -> None:
    # Deliberately only the target-year exchange evidence is representable.
    # Other-year broker schedules are corroborative-only by contract.
    decision = qualify_evidence_gap(
        EvidenceBundle(
            exact_exchange_schedule=True,
            exchange_provenance_verified=True,
            retrieval_exhausted=True,
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP"


def test_missing_data_or_http_failure_cannot_be_encoded_as_pass_evidence() -> None:
    # Missing BI5 / HTTP failures intentionally have no PASS-bearing fields.
    decision = qualify_evidence_gap(EvidenceBundle(retrieval_exhausted=True))
    assert decision.verdict == BLOCKED


def test_unfinished_retrieval_stays_blocked_but_not_irreducible() -> None:
    decision = qualify_evidence_gap(EvidenceBundle())
    assert decision.verdict == BLOCKED
    assert decision.reason == "RETRIEVAL_INCOMPLETE"


def test_exact_broker_contradiction_overrides_apparent_pass() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            exact_broker_primary=True,
            strong_broker_contradiction=True,
        )
    )
    assert decision.verdict == FAIL


def test_wrong_date_or_instrument_witness_is_fail_not_pass() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            exact_broker_primary=True,
            witness_identity_mismatch=True,
        )
    )
    assert decision.verdict == FAIL


def test_falsified_archive_provenance_is_fail() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            exact_broker_archive=True,
            broker_archive_provenance_verified=True,
            archive_provenance_falsified=True,
        )
    )
    assert decision.verdict == FAIL


def test_bad_bucket_conversion_is_fail_even_with_exact_broker_source() -> None:
    decision = qualify_evidence_gap(
        EvidenceBundle(
            exact_broker_primary=True,
            bucket_conversion_contradiction=True,
        )
    )
    assert decision.verdict == FAIL
