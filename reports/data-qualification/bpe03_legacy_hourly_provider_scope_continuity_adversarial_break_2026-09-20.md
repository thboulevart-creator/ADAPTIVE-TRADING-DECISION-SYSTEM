# B-PE-03 — PROVIDER-PRIMARY SCOPE / VERSION CONTINUITY — ADVERSARIAL BREAK

**Date:** 2026-09-20
**Candidate HEAD:** `3a116ab4c6b8766fb27360b346421ba91ccd1e98`
**Candidate evidence bundle blob:** `fffd2d45275a41424a5458ea4c67a822a0e065f1`

## Demonstrated defects

### BPE03-F01 — FREE-TEXT CORROBORATION BYPASSES EVIDENCE BINDING

Candidate C08-D1 and C08-D3 PASS rows include free-text placeholders such as:

```text
BPE02-E03 BASE_URL/provider identity (admissible EC-I2)
BPE02-E09 hourly URL family + BPE02-E03 legacy hourly downloader semantics
```

These are not closed ClaimEvidenceAssertion IDs bound into the BPE03 evidence set.

Result:

a dimension PASS can depend on evidence that is not part of the current evidence-set digest / assertion-set digest.

Verdict:

`DEMONSTRATED DEFECT`.

Correction:

import the exact BPE02 independent EvidenceSourceRecords + admissibility decisions actually used and create closed BPE03 assertions against them.

### BPE03-F02 — JETTA BACKEND CHANGE MISCLASSIFIED AS CONTRADICTION

The JForex 4.8.0 release note proves:

```text
historical price data source changed to JETTA on 2026-03-03
```

It does not prove:

```text
legacy hourly BI5 stopped on that date
or
public hourly→daily bucket transition occurred on that date
```

Therefore assigning `stance=CONTRADICT` against C08-D5 is stronger than the source supports.

Verdict:

`DEMONSTRATED DEFECT`.

Correction:

retain E03 as admissible contextual boundary evidence but remove it from SUPPORT/CONTRADICT claim assertions. C08-D5 remains BLOCKED because the transition date is absent.

## Attacks that did not demonstrate defects

- provider API Support statement is sufficient to establish historical hourly BI5 family existence, but not byte semantics;
- Maven client version timeline was not treated as proof of file-format continuity;
- no current daily format fact was transplanted into legacy hourly semantics;
- no USATECH-specific legacy applicability was fabricated;
- no C01-C07 dimension was reopened;
- no JETTA date was equated to the public BI5 transition.

## Initial verdict

```text
B-PE-03 CANDIDATE = FAIL
```

Only BPE03-F01 and BPE03-F02 may be corrected.
