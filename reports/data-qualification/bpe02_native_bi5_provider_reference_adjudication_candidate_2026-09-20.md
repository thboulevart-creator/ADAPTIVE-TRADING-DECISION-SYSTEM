# B-PE-02 — NATIVE BI5 PROVIDER / REFERENCE EVIDENCE ADJUDICATION — CANDIDATE

**Date:** 2026-09-20
**Starting HEAD:** `67c8de7a80a3ecd3f8688663344b7dd5dc2e3ebf`
**B-PE-01 contract blob:** `278a691b17cdd4b37e9c0e739f0fe9b56f014b29`
**Scope:** documentary/reference evidence only. No project BI5 downloaded or processed.

## Evidence set

Persisted structured evidence bundle:

`evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json`

Sources:

1. `BPE02-E01` — Dukascopy provider-primary Historical Price Data page — ADMISSIBLE, but current-daily scope with only a warning about legacy hourly.
2. `BPE02-E02` — Dukascopy provider-primary USATECH CFD metadata — ADMISSIBLE for instrument/current quote metadata, not raw BI5 divisor.
3. `BPE02-E03` — saleem-latif/duka-data exact commit — ADMISSIBLE EC-I2.
4. `BPE02-E04` — ninety47/dukascopy exact commit — ADMISSIBLE EC-I2.
5. `BPE02-E05` — leoclc/dukascopy-tick exact commit — ADMISSIBLE EC-I2.
6. `BPE02-E06` — project V4.3 — REJECTED as EC-PROJECT independent support.

No project implementation contributes evidentiary weight.

## Critical observed scope conflict

Provider-primary current documentation establishes a current daily BI5 layout and explicitly warns that legacy hourly files can use a different timestamp basis.

It does not state the transition date and does not bind the legacy-hourly physical semantics to the project's intended 2021–2026 hourly acquisition representation.

Therefore:

```text
current provider BI5 documentation
≠ target legacy-hourly provider-version continuity proof
```

This is the dominant B-PE-02 blocker.

## Independent corroboration

Three independently hosted non-project implementations strongly corroborate legacy hourly behavior:

- hourly `h_ticks.bi5` path family;
- LZMA decompression;
- 20-byte records;
- big-endian field layout;
- ms offset added to an hourly start;
- ask/bid followed by ask/bid volumes;
- USATECH divisor/decimalFactor 1000 in two modern implementations.

However, B-PE-01 requires provider-primary + distinct corroboration on the **exact target scope**.

Independent corroboration cannot substitute for missing provider-primary target-version continuity.

A material independent disagreement is also preserved:

```text
ninety47 → unsigned integer decoding
duka-data / leoclc → signed integer decoding
```

No majority vote is permitted.

## Claim verdicts

```text
BPE-C01 compression / envelope = BLOCKED
BPE-C02 physical framing       = BLOCKED
BPE-C03 primitive layout       = BLOCKED
BPE-C04 timestamp semantics    = BLOCKED
BPE-C05 ask/bid raw roles      = BLOCKED
BPE-C06 USATECH price scaling  = BLOCKED
BPE-C07 volume semantics       = BLOCKED
BPE-C08 target applicability   = BLOCKED
```

C08 contains two dimension-level PASS states:

```text
C08-D1 provider identity = PASS
C08-D2 existence of legacy hourly BI5 family = PASS
```

but C08-D3/D4/D5 remain BLOCKED, especially:

```text
C08-D5 target temporal/version continuity = BLOCKED
```

## Specific unresolved points

- C01: provider current page says raw LZMA; target candidate says LZMA-Alone. Exact legacy-hourly envelope semantics are not provider-bound.
- C02: 20-byte records are strongly corroborated, but target-epoch framing/header/residual semantics are not provider-primary closed.
- C03: target signedness is unresolved; independent implementations disagree and current provider uint32 is for current daily format.
- C04: provider says legacy files **may** use ms since hour; no exact target-epoch binding/range.
- C05: ask/bid roles strongly corroborated, but exact legacy target provider binding remains absent.
- C06: USATECH /1000 is independently corroborated; provider current CFD 0.01 point value does not prove raw BI5 divisor and provider historical-data guide says indices vary.
- C07: volume roles/float32 strongly corroborated; target legacy transform/scale semantics are not provider-primary closed.
- C08: decisive provider transition/continuity evidence is absent.

## Candidate adjudication verdict

```text
B-PE-02 PROVIDER / REFERENCE EVIDENCE ADJUDICATION = BLOCKED
overall_provider_evidence_status = BLOCKED
B global executable gate = BLOCKED
```

No claim is FAIL because no exact-target provider-primary evidence positively disproves the candidate. The correct result is lack of target-scope proof, not contradiction.

## Next inside this block

Adversarially break this exact persisted adjudication before accepting the BLOCKED classification as governed closure.
