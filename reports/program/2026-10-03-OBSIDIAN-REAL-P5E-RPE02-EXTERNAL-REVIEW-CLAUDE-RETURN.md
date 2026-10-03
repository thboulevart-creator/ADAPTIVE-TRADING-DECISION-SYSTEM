# RPE-02 — EXTERNAL REVIEW RETURN — CLAUDE

Date: 2026-10-03

## Verdict

`VERDICT = FAIL`

## Blocking finding

### BF-1 — malformed observation integrity

Observed behavior:
- arbitrary non-empty strings are accepted as `outcome`;
- `REMOTE_HEAD_OBSERVED` does not require a head;
- `READ_FAILURE` may carry a head;
- malformed records can become `FAIL_NO_DETECTION_BY_BOUND` instead of being rejected or blocked.

Required closure:
- vocabulary exactly `READ_FAILURE | REMOTE_HEAD_OBSERVED`;
- `REMOTE_HEAD_OBSERVED -> observed_head = lowercase 40-hex`;
- `READ_FAILURE -> observed_head = null`;
- malformed evidence must fail closed before any SLA business verdict.

## Non-blocking findings carried into targeted closure

### NB-1 — insufficient test lock

Additional discrimination required for:
- actual-start versus scheduled-slot release eligibility;
- started < scheduled;
- remote completion < actual start;
- attempt completion < remote completion;
- duplicate slot;
- cadence gap;
- skipped required attempt;
- no-detection exact boundary.

### NB-2 — exact-grid parity divergence

Two observed counterexamples distinguish:
- `FAIL_NO_DETECTION_BY_BOUND`;
- `INCOMPLETE_REAL_TIME_WINDOW`.

The current implementation uses last remote completion rather than feasibility of the next required fixed-rate slot. Exact-grid parity is therefore overclaimed until corrected.

### NB-3 — silent sorting

Input observations are sorted internally. Input order should instead be treated as evidence integrity.

### NB-4 — final full-attempt completion

The reviewer noted that the last attempt's full completion may extend far beyond the next slot. Human adjudication for targeted closure keeps:
- remote completion = SLA endpoint;
- full attempt completion = timeline/overlap evidence;
- real no-overlap execution guarantee deferred to RPE-05.

### NB-5 — packet fidelity

The previous packet labeled the final test as the RED test. The replacement packet must distinguish historical RED blob from final test blob.

## Adoption readiness

`RPE-02 = NOT_READY_FOR_HUMAN_ADOPTION`

This review creates no authority.

`RPE-04 = CLOSED`
`REAL_P5E = CLOSED`
