# B-PE-03 — LEGACY-HOURLY BI5 PROVIDER-PRIMARY SCOPE / VERSION CONTINUITY — CANDIDATE

**Date:** 2026-09-20
**Starting HEAD:** `e7d844e4ad823526c0e92232b1fd2c9ce06b5a03`
**Scope:** provider-owned/versioned/archived evidence only; no BI5 project data.

## Provider evidence collected

1. Dukascopy API Support, dated 2013:
   establishes the historical tick file-server family and an hour-addressed `h_ticks.bi5` object.
2. Dukascopy provider Maven index:
   immutable/versioned JForex client artifact timeline from 2021 through 2025.
3. Dukascopy JForex 4.8.0 release note:
   on 2026-03-03, JForex introduced a new historical-price-data source named JETTA.

All three provider extracts are persisted as immutable project evidence snapshots with SHA-256 binding and exact source anchors.

## What is established

The re-adjudication promotes only:

```text
C08-D1 provider identity applicability             = PASS
C08-D2 legacy native hourly BI5 family existence   = PASS
C08-D3 historical tick file-object family binding  = PASS
```

These PASS dimensions are supported by one provider-primary lineage plus distinct B-PE-02 independent corroboration.

## What is NOT established

```text
C08-D4 USATECH legacy-hourly applicability = BLOCKED
C08-D5 temporal/version continuity 2021–2026 = BLOCKED
```

Why C08-D5 remains BLOCKED:

- provider Maven releases prove client release continuity, not unchanged historical file format;
- provider release notes prove a history backend change to JETTA on 2026-03-03;
- no provider-owned artifact found states the public hourly→daily BI5 transition date;
- no provider-owned artifact found states that the legacy hourly physical format remained unchanged through the target 2021–2026 epoch.

The JETTA release cannot be silently equated to the public BI5 bucket transition.

## Claim result

```text
BPE-C08 = BLOCKED
```

No C01-C07 dimension is reopened because B-PE-03 found no provider-primary exact legacy-hourly byte-layout specification.

Therefore:

```text
overall_provider_evidence_status = BLOCKED
B global executable gate = BLOCKED
```

Next inside B-PE-03: adversarially break this exact persisted scope/continuity adjudication.
