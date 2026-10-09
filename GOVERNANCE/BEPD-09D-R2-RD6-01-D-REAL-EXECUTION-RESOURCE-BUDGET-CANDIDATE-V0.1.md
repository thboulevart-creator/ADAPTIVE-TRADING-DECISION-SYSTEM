# BEPD-09D-R2-RD6-01-D — REAL EXECUTION RESOURCE BUDGET CANDIDATE V0.1
**DOCUMENTARY CANDIDATE; ZERO ACTUAL PERMISSION, ZERO NEW COST AUTHORITY.** 2026-10-09.

## Historical exposure ledger (pre-existing, not rerun)
Prior real C1 run `37675309127` (historical documented receipt, NOT newly executed): recorded 472 real rows read, primary started but `MODEL_NONCONVERGENCE` in Fold3 evidence, reference not executed, no valid C1 scientific result. RD4 source notes prior numerical forensics are known: these are exploratory exposure and MUST NOT be used to retune TAU, solver, feature selection, numerical tolerance, input population, stopping policy or training order. The ledger count is historical declaration, not a fresh row count.

## Candidate fit events and exact order
Each fold f=1..5 uses fixed training blocks B1..Bf and protects B(f+1) as test. Each f has roles BASELINE then CONTEXT. For each role, after all identity, scope, parser, schema, finite, LP and rank preflight breakers pass, candidate schedule:
```text
for fold in [1,2,3,4,5]:
  for role in [BASELINE,CONTEXT]:
    authenticate immutable fold-local train view
    apply structural/LP preflight without fitting
    [if separately authorized] primary_fit_exactly_once
    verify exact RD2 Candidate B gate
    [if separately authorized + primary PASS + parity contract adopted]
       reference_fit_exactly_once on same X_train/y_train
       verify independent gate and candidate cross-solver parity
    produce bounded receipt + advance only on PASS
  no test scoring or fold-test matrix, ever
```
Maximum *proposal* 10 primary + 10 reference = 20 numerical fits, zero retries, one attempt for each scheduled pair, no fold skipping, no extra diagnostic re-fit, no optimizer fallback or conditional tuning. The actual human authorized budget remains **0+0** until a new signed decision. Even if the candidate budget were adopted in future, if stage 1 fails, stage 2 and remaining fold events **must not run**.

## Candidate resource caps to be decided, not empirical measurements
```text
EXECUTOR = SINGLE_EPHEMERAL_ISOLATED_WORKER
CONCURRENCY = 1
CPU_QUOTA = 2 vCPU maximum
MEMORY_HARD_LIMIT = 4 GiB
PRIMARY_FIT_TIMEOUT = 120 s each maximum
REFERENCE_FIT_TIMEOUT = 120 s each maximum
TOTAL_WORKFLOW_WALL_CLOCK = 60 min maximum
NETWORK_EGRESS = DISABLED
REAL_DATA_OWNER_IDENTITY = SEPARATE_FROM_WORKER
SOURCE_LEDGER_FILESYSTEM_MOUNT = ABSENT_FROM_WORKER
CLOUD_NEW_BILLING = 0 permitted
AUTOMATIC_RETRY = 0
TRADING_ACCOUNT_ACCESS = NONE
```
These caps are **candidate planning numbers**, not benchmarked, not committed, and potentially too restrictive; an authorized synthetic resource benchmark is required before adoption. Use an existing no-additional-cost runtime only if quota, runner data privacy, and exact zero marginal spending are proven; if any charge may occur, STOP pending explicit approval. Future output artifacts may include only timing/resource counters and stop codes allowed by a separately adopted serializer; never raw observations, model parameters, scientific performance metrics, PNL or test responses.

## Physical read authorization must be independent of fit authorization
An existing 754544-byte monolithic ledger (metadata only) does not become fold-isolated merely by filtering after read. Any future authorized owner pass that physically reads it must specify: whether protected test responses can be accessed by producer, byte/row quotas, exactly one identity-preserving read (if adopted), force=false refs, materialization proof, new exposure ledger increment, destruction/retention and stop conditions. **No such real pass or authority is granted.**

## Deterministic evidence sequence proposal
P0 fresh Git HEAD/TREE and frozen blob readback; P1 human authority and signed manifest; P2 authenticated producer-view seal and input scope attestation; P3 executable isolation and leakage guards; P4 prefit structural/LP checks; P5 primary fit and frozen RD2 gate; P6 independent reference and preregistered metric; P7 bounded receipt seal + fail-closed progression. Every failure produces STOP with consumed budget, never silent retry or selective omission. Make receipts append-only and deterministic (minus separately bound wall timestamps); version-lock runtime and exact Python/numpy/scipy environment.

## Cost/risk and go/no-go
The worker-time numerical proposal does NOT cover costs of materializer privileges, source storage, audit infrastructure, external review or data transfer; each needs its own authority and independently scoped cap. Until adopted:
`REAL_LEDGER_READS_AUTHORIZED=0`
`REAL_PRIMARY_FITS_AUTHORIZED=0`
`REAL_REFERENCE_FITS_AUTHORIZED=0`
`REAL_RETRIES_AUTHORIZED=0`
`NEW_SPEND_AUTHORIZED=0`
`REAL_WORKFLOW_ACTIVATION=FORBIDDEN`

## Material decisions for future humans
D-MAT-01: actual complete fit count/order including atomic failure semantics. D-MAT-02: physical-byte read/row exposure grant and ledger owner. D-MAT-03: resource caps and proven cost cap. D-MAT-04: single-attempt, timeouts and abort receipt schema. D-MAT-05: cross-parity adoption and independent review. D-MAT-06: historical exposure contamination policy and exploratory-only C1 designation.

`D_BUDGET_CANDIDATE_DESIGNED=PASS_DOCUMENTARY`; `D_REAL_RESOURCE_BUDGET_ADOPTED=BLOCKED`; `D_REAL_EXECUTION=FORBIDDEN`.
