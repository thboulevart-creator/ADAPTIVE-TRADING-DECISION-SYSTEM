# AP5 R3 — AP5_COMPLETE output not qualified due to helper byte mismatch

Date: 2026-09-25
Branch: `integration/system-v1`
Fresh HEAD before persistence: `56f88db65a37245c47256aac65eb9ca9869703bf`

## R3 terminal evidence

The local run reported:
- canonical AP4 atomic rewrite succeeded;
- AP4 length = 15,488;
- AP4 SHA-256 = `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`;
- AP5 printed `AP5_COMPLETE`;
- exit code = 0;
- output length = 39,460 bytes;
- output SHA-256 = `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406`.

Uploaded output was independently rehashed and exactly matched those length/SHA values.

## Blocking provenance issue

Before execution, the staged helper hashed to:
`92855187374b80651ef67dcf1224132c80d839f3c3516ad634693def6420a399`.

The frozen helper required:
`fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`.

The guard explicitly raised `BLOCKED: helper différent du helper figé.`, but later commands were manually continued.

Canonical helper facts at commit `715c3e4affa44778785d6c222782eda257ed19e7`:
- Git blob: `21de65a7fbf8277dd2eb0afc99f4c2b80912af06`;
- SHA-256: `fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`;
- 566 LF lines.

A pure LF→CRLF conversion would hash to:
`faa0f90d030f655bdefbc13f01ce6df4bd341b946600b253f3f00ecb81e6269e`,
which does not equal the observed staged helper hash.

Therefore the exact helper bytes used by R3 are not proven equivalent to the frozen helper.

## JSON internal checks

The R3 JSON is internally coherent and passed the registered AP5 numerical/coverage/scope checks, including:
- AP0 manifest exact;
- AP4 SHA exact;
- 61 AP0 files rehashed;
- 1,709,180 minute rows;
- 376,003,618 source ticks;
- 1,606 segments / 1,606 segment starts;
- F2/AP1 spread reconciliation;
- AP2 minute-range and 1m-return reconciliation;
- partition conservation for NY hours, session proxy, range quintiles, tick-density quintiles and UTC years;
- strategy-agnostic scope flags;
- no volume/depth/order-flow claim;
- descriptive-only correlations.

These checks do not cure the provenance defect.

## Verdict

**BLOCKED — R3 AP5_COMPLETE output is a candidate only, not qualified AP5 evidence.**

No AP5 PASS is declared.
AP6 remains closed.

## Next action

Create a brand-new empty stage and materialize both:
1. the exact frozen helper from raw Git blob `21de65a7fbf8277dd2eb0afc99f4c2b80912af06`;
2. the exact AP4 evidence from raw Git blob `3bc22e33956dc422ad45d4a825c89255bf60c432`.

Verify both exact SHA-256 values in-process and independently, then execute AP5 to a fresh R4 output.
