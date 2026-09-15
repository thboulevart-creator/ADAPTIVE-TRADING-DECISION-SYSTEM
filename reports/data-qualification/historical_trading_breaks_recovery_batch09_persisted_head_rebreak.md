# HISTORICAL TRADING BREAKS RECOVERY — BATCH 09 PERSISTED-HEAD RE-BREAK

**PASS — `BATCH09_PERSISTED_HEAD_REBREAK_CONFIRMS_ATOMIC_INTEGRATION`**

## Independent verifier identity

- workflow run: `34998844423`
- job: `104481875172`
- verifier trigger commit: `21965fd00fc92f606665b5db3c20c265b8ad83fe`
- verified checkpoint parent state: `4a0827a720a086ff084ca1388b1b8ae8b11ad060`
- authoritative atomic integration commit: `126ff25129728dc9f5c26cfeff701c1e04270843`
- permissions: `contents: read`
- verifier trigger delta from checkpoint: exactly `.github/workflows/trading-breaks-recovery-batch09-persisted-head.yml`
- browser/network/capture execution: NONE
- governed state mutation by verifier: NONE

## Re-break result

- full governed + adversarial regression: **`399 passed in 1.82s`**
- integrated commit ancestry: PASS
- exact branch HEAD at verifier execution: PASS
- governed-state immutability since atomic integration: PASS
- exact Batch 09 calendar evidence: PASS
- exact Batch 09 ledger sequences `41..45`: PASS
- exact Dec 25 unresolved/ineligible state: PASS
- deterministic progression regeneration: PASS
- byte-stable persisted progression runtime after regeneration: PASS
- final `git diff --exit-code`: PASS
- final `git status --porcelain`: empty

## Persisted calendar evidence independently recovered

Exactly these four Batch 09 targets resolve through `SPECIAL_SESSION_EVIDENCE`:

1. `2024-09-02 — LABOR_DAY` — record `70878` — whole closed UTC hours `[17,18,19,20,21]`.
2. `2024-11-28 — THANKSGIVING_DAY` — record `72887` — whole closed UTC hours `[18,19,20,21,22]`.
3. `2024-11-29 — THANKSGIVING_FRIDAY` — record `72888` — whole closed UTC hours `[19,20,21,22,23]`; hour 18 remains partial/open.
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION` — record `74339` — whole closed UTC hours `[19,20,21,22,23]`; hour 18 remains partial/open.

All four retain:

- artifact `10406357435`;
- artifact SHA-256 `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`;
- probe commit `0b5dedf6028add27040af112d0bceef76be25827`.

`2024-12-25 — CHRISTMAS_OBSERVED` is absent from both `SPECIAL_SESSION_EVIDENCE` and `NO_SPECIAL_CHANGE_EVIDENCE`.

## Persisted attempt ledger independently recovered

The ledger contains exactly `45` contiguous unique attempts and exactly these Batch 09 entries in immutable frozen order:

- `41 — batch09:2024-09-02 — PASS`
- `42 — batch09:2024-11-28 — PASS`
- `43 — batch09:2024-11-29 — PASS`
- `44 — batch09:2024-12-24 — PASS`
- `45 — batch09:2024-12-25 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

All five preserve authoritative execution provenance:

- run `34993614373`;
- job `104464228483`;
- artifact `10406357435`;
- artifact SHA-256 `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`;
- probe commit `0b5dedf6028add27040af112d0bceef76be25827`;
- capability `TRADING_BREAKS_PRIMARY_WIDGET_V1`.

## Persisted progression independently recovered

Exact post-Batch09 state:

- raw unresolved queue: `34`;
- attempt ledger: `45`;
- registered material capability changes: `0`;
- same-capability attempted BLOCKED/ineligible: `11`;
- execution-eligible unresolved: `23`;
- first eligible unresolved: `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`.

For `2024-12-25` specifically:

- calendar state: `UNRESOLVED`;
- latest attempt: `batch09:2024-12-25`;
- latest outcome: `BLOCKED`;
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`;
- eligibility: `false`;
- reason: `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- contract verdict: `PASS`.

## Coverage accounting independently recovered

Global:

`111 candidates / 57 resolved / 54 unresolved / 0 FAIL`

Execution-window candidate:

`68 candidates / 34 resolved / 34 unresolved / 0 FAIL`

Calendar structural checks:

- evidence-shape errors: `0`;
- orphan special evidence: `0`;
- contradictory evidence dates: `0`.

## Boundary

The persisted-HEAD re-break is PASS, but the execution window remains unfrozen because unresolved dates remain inside it.

- Batch 10 membership: **NOT FROZEN** during this re-break.
- `.bi5`: FORBIDDEN.
- real backtest: NOT AUTHORIZED.

The completed verifier workflow is archived manual-only after this PASS.
