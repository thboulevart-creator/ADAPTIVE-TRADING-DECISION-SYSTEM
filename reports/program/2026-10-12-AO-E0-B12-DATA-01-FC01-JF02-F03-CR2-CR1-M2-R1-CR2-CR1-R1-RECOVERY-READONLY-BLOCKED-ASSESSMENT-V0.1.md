# R1 ENVIRONMENT RECOVERY — READ-ONLY FORENSIC RECONCILIATION V0.1

## Terminal decision

```text
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1
RECOVERY_AUTHORIZATION = HUMAN_ADOPTED_AND_EXECUTION_AUTHORIZED
R1_CAMPAIGN_ID = R1RECOVERY_20261011_CAMPAIGN_A
M2_R1_CR2_CR1_R1 = BLOCKED
RECOVERY_RECONCILIATION = COMPLETED_READ_ONLY
NEW_WORKERS_LAUNCHED_DURING_THIS_RECOVERY_CHECK = 0
HISTORICAL_CAMPAIGN_WORKERS_CONSUMED = 4/13
CAMPAIGN_REPLAY = FORBIDDEN
TERMINAL_CAUSE = DESCENDANT_ABSENCE_UNPROVEN
STOP_AFTER_R1_RECOVERY = APPLIED
```

## Fresh source identity and unchanged boundaries

Local and GitHub canonical HEAD: `797a88e388dba1e9346c75466ec9801c8ecaa7ba`; TREE: `5d62da2ba1c879d7c037f4c8eb0d6b2816704e9b`; branch `integration/system-v1`. Local tracked diff was empty. Protected FC01 Git blob `44ccaeafdd22cede207fef6038e5c747ff5d1454`; E1 Git blob `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`.

At recovery start, an untracked local R1 source tree and a frozen campaign directory already existed. They were preserved. No new worker was created, no older receipt was overwritten, no provider/JForex access was attempted.

## Existing campaign evidence

The existing NTFS directory `%TEMP%\ATDS_M2_R1_CR2_CR1_R1_CAMPAIGN_20261011_A` contained a `terminal.json`, four per-run receipts and four immutable checkpoints, frozen parameters, compiler receipts and a four-line launch ledger.

| Run | Supervisor result | Validator | Supervisor exit |
|---|---|---|---:|
| normal_A | PUBLISHED | PASS | 0 |
| normal_B | PUBLISHED | PASS | 0 |
| java_oom | BLOCKED_MEMORY | PASS | 22 |
| timeout | BLOCKED_TIMEOUT | BLOCKED | 21 |

The `terminal.json` recorded `spent=4`, `status=BLOCKED` and error `RuntimeError:RECEIPT_BLOCKED_timeout:['DESCENDANT_ABSENCE_UNPROVEN']`. The outstanding nine planned launches have no continuing authority under the stopped campaign.

The timeout receipt says `descendant_created=false`, `descendant_identities=[]`, while recording `termination_confirmed=true` and `tree_terminated=true`. The raw supervisor stream, however, recorded two Job members before termination:

```text
R1_JOB_MEMBER_COUNT_BEFORE=2
R1_JOB_MEMBER_PRE_33536=33536|134361969930150189
R1_JOB_MEMBER_PRE_36448=36448|134361969930287894
R1_JOB_MEMBER_POST_33536=33536|134361969930150189|True|88
R1_JOB_MEMBER_POST_36448=36448|134361969930287894|True|88
R1_JOB_MEMBERS_POST_COUNT=0
CR1_TERMINATION_REQUEST=TERMINATE_JOB
CR1_WORKER_TERMINATED=True
RESULT=BLOCKED_TIMEOUT
```

This establishes a **material inconsistency in the descendant-absence classification/receipt contract**: two observed job members cannot be reconciled with an unproven assertion of no descendant solely from `descendant_created=false`. The raw record suggests termination of both identified members; it cannot bypass the independently blocking descendant-proof gate. No historical receipt was repaired or promoted.

## Previously completed preparation, not repeated

The frozen `frozen_packet.json` at that campaign includes `p0_static_result=QUALIFIED_WITH_FIVE_ADOPTED_REPAIR_UNITS`, `p1_test_first=RED_34_EXPECTED_FAILURES_THEN_ADVERSARIAL_ADDITIONS`, `p2_static_green=47_OF_47_PASS_AT_FREEZE` and distinct preregistration of 36 Windows-supervised and 14 Java-mock regression processes. These are assertions in the existing frozen packet; the recovery check did not rerun or independently certify these RED/GREEN results.

## Required next authority

A separate human adjudication is required for `DESCENDANT_ABSENCE_UNPROVEN`, specifically to reconcile actual Job membership (PID and immutable process creation identity) with an evidence-grade descendant classification. No attempt may retroactively amend the four historical receipts or reuse the remaining campaign launch budget.

```text
M2_MEMORY_POLICY=HUMAN_ADOPTED
M2_R1=BLOCKED
M2_R1_CR1=BLOCKED
M2_R1_CR2=BLOCKED
M2_R1_CR2_CR1=BLOCKED
M2_R1_CR2_CR1_R1=BLOCKED
WINDOWS_INTERNAL_ROOT_CAUSE=NOT_PROVEN
FC01_REAL_MEMORY_SAFETY=NOT_QUALIFIED
READ_A_RETRY=FALSE
READ_B=FALSE
B12=CLOSED
FORCE=FALSE
FAIL_CLOSED=TRUE
STOP_AFTER_R1_RECOVERY=APPLIED
```
