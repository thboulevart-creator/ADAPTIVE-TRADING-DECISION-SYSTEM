# B-PE-02 — PROVIDER / REFERENCE EVIDENCE ADJUDICATION — CORRECTED CANDIDATE

**Date:** 2026-09-20
**Initial candidate commit:** `428ac771e238ea1988c8fe2d8cad2d7e7b83adf9`
**Adversarial record:** `reports/data-qualification/bpe02_native_bi5_provider_reference_adjudication_adversarial_break_2026-09-20.md`
**Scope:** documentary/reference evidence only.

## Corrections

Closed only the demonstrated defects:

```text
BPE02-F01 — recursive canonical seals/digests
BPE02-F02 — live provider pages demoted to source-level BLOCKED
BPE02-F03 — one closed ClaimEvidenceAssertion per exact dimension
BPE02-F04 — one exact GitHub file per EvidenceSourceRecord
```

## Provider source status

```text
E01 Dukascopy Historical Price Data = BLOCKED
E02 Dukascopy USATECH CFD page      = BLOCKED
```

Reason:

the pages are live, have no immutable provider version, and the exact captured provider source snapshot bytes are not durably materialized under the B-PE-01 source rule.

Their observations remain contextual diagnostics only and contribute zero PASS/FAIL evidentiary weight.

## Independent source status

Exact pinned GitHub files from duka-data, ninety47 and leoclc are ADMISSIBLE EC-I2.

Project V4.3 is REJECTED as EC-PROJECT.

Pairwise independence among the three third-party semantic lineages remains conservatively UNRESOLVED; it is not used to manufacture multiple corroborating votes.

## Corrected dimension adjudication

Because B-PE-01 requires at least one **ADMISSIBLE provider-primary lineage** for each dimension, and E01/E02 are source-level BLOCKED:

```text
every mandatory C01-C08 dimension = BLOCKED
every C01-C08 claim = BLOCKED
```

Additional preserved diagnostics:

- independent legacy hourly implementations strongly corroborate many physical facts;
- C03-D3/C05-D2 retain signed-vs-unsigned disagreement across independent implementations;
- C06-D2 retains independent USATECH divisor 1000 corroboration but no admissible provider-primary raw scale source;
- C08-D5 retains the missing legacy-hourly → target 2021–2026 provider continuity gap.

## Corrected verdict

```text
B-PE-02 PROVIDER / REFERENCE EVIDENCE ADJUDICATION = BLOCKED
overall_provider_evidence_status = BLOCKED
B global executable gate = BLOCKED
```

No C01-C08 claim is FAIL.

Next inside current block: persisted-HEAD integrity + adversarial re-break of this corrected adjudication.
