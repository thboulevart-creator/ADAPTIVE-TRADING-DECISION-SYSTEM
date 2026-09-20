# B-PE-03 — LEGACY-HOURLY PROVIDER SCOPE / CONTINUITY — CORRECTED CANDIDATE

**Date:** 2026-09-20  
**Initial candidate commit:** `3a116ab4c6b8766fb27360b346421ba91ccd1e98`  
**Adversarial break:** `reports/data-qualification/bpe03_legacy_hourly_provider_scope_continuity_adversarial_break_2026-09-20.md`

## Corrections

Closed only:

```text
BPE03-F01 — free-text BPE02 corroboration removed;
             exact BPE02-E03/E09 source records + sealed admissibility decisions imported
             and exact closed BPE03 assertions created.

BPE03-F02 — JETTA release removed from claim stance;
             retained as contextual provider evidence only.
```

## Corrected C08 dimension state

```text
C08-D1 provider identity applicability            = PASS
C08-D2 legacy hourly BI5 family existence         = PASS
C08-D3 historical tick file-object family binding = PASS
C08-D4 USATECH legacy-hourly applicability        = BLOCKED
C08-D5 target temporal/version continuity          = BLOCKED
```

Every PASS dimension now binds:

```text
one exact provider-primary BPE03 assertion
+
one exact imported BPE02 EC-I2 source/decision/assertion
```

No free-text evidence dependency remains.

## Continuity conclusion

Provider evidence establishes the legacy hourly family historically and a provider client release timeline through 2025.

It does not establish that the same hourly BI5 representation/physical semantics applied to USATECHIDXUSD throughout 2021-08-14 → 2026-08-14.

JForex 4.8.0 / JETTA is retained only as evidence that a history-source change occurred on 2026-03-03; it is not treated as the public BI5 format transition date.

## Corrected verdict

```text
BPE-C08 = BLOCKED
B-PE-03 overall provider evidence = BLOCKED
B global executable gate = BLOCKED
```

No C01-C07 dimension is reopened.

Next: persisted-HEAD integrity and semantic adversarial re-break.
