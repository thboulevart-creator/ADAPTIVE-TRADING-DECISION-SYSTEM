# SESSION BACKUP — 2026-09-20 — B-PE-02 PROVIDER EVIDENCE BLOCKED

## Recovery

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Starting HEAD:

`67c8de7a80a3ecd3f8688663344b7dd5dc2e3ebf`

Action:

`B-PE-02 — native BI5 provider/reference evidence collection and C01-C08 adjudication`

## Collected evidence

Provider-primary:

- Dukascopy Historical Price Data live documentation;
- Dukascopy USATECH CFD current market metadata.

Independent exact revisions:

- saleem-latif/duka-data @ `2220708e7d0be9d2b6feaf6efe4d3f89c6bb040c`;
- ninety47/dukascopy @ `8654ad197bdf55579544cf71735369f0d227569f`;
- leoclc/dukascopy-tick @ `989987db0808e215962e136ce043797992d1a1a2`.

Project V4.3 was explicitly REJECTED as independent support.

## Material evidence findings

Strong independent corroboration exists for legacy-hourly:

- LZMA;
- 20-byte records;
- big-endian field structure;
- hourly timestamp offset behavior;
- ask/bid + volume field order;
- USATECH divisor/decimalFactor 1000 in two current independent implementations.

But provider-primary current documentation describes a current DAILY format and only warns that legacy hourly may differ. It gives no transition date or immutable legacy target-version binding.

Independent implementations also disagree on integer signedness.

Therefore evidence strength does not meet B-PE-01 exact-target provider-primary requirements.

## Adjudication defects corrected

```text
F01 canonical seals
F02 live provider snapshot immutability
F03 assertion schema
F04 multi-file digest projection
```

Final corrected bundle:

`evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json`

blob:

`df22332709377591d73571a4940c1fda39565867`

Final seal:

`d27771bc8c2023571b4fbbe66238dbc28b29ca69949a1db114480346f1c90a76`

## Final verdict

```text
C01-C08 = BLOCKED
overall provider evidence = BLOCKED
B global executable gate = BLOCKED
```

No claim FAIL.

## Exactly one next governed action

Open only:

```text
B-PE-03 — legacy-hourly BI5 provider-primary immutable scope/version continuity evidence
```

Purpose:

find and qualify an immutable/versioned provider-owned source that closes the exact relation:

```text
Dukascopy legacy hourly BI5
→ exact physical semantics
→ applicability / transition boundary
→ target USATECHIDXUSD 2021–2026 hourly representation
```

If no such provider-primary immutable source exists, persist that absence and determine the smallest permitted alternative evidence path under B-PE-01; do not lower the evidence threshold silently.

Still no project BI5 download/processing/acquisition/backtest.
