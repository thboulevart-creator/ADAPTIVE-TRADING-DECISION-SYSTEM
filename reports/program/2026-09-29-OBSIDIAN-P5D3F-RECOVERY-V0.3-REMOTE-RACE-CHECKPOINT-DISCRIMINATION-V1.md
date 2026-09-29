# OBSIDIAN P5-D3F — RECOVERY V0.3 REMOTE RACE CHECKPOINT DISCRIMINATION V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL READ-ONLY INCIDENT PROBE plus VERIFIED GITHUB state plus SAME-ASSISTANT STATIC CONTROL-FLOW REVIEW.

## Preserved temporary root

    C:\Users\Boulevart\AppData\Local\Temp\ATDS-P5D3F-PERSISTENT-HANDOFF-pg0epofm

## User-reported identities

Control repository FETCH_HEAD after the failed run:

    fbe8c3148787dca693829364d663d8c6cbe44436

Temporary candidate FETCH_HEAD:

    fbe8c3148787dca693829364d663d8c6cbe44436

Temporary candidate HEAD:

    fbe8c3148787dca693829364d663d8c6cbe44436

Temporary candidate TREE:

    a3b0902b1459696629847789d3a2e162fcc4e98d

Remote integration/system-v1 observed by the user immediately after failure:

    4b08aa09f8ab620278500e2c44dce757c46595d1

## Independently verified GitHub state

At report-verification time, integration/system-v1 had advanced again to:

    fda1d9724165192385fed1c22817d9c33334fde8

Compared with the frozen candidate HEAD:

    status    = ahead
    ahead_by  = 5
    behind_by = 0

Current observed head commit message:

    P22-03: persist evidence envelope recorder qualification

The branch is therefore actively advancing during this incident-analysis window.

## Exact race checkpoint adjudication

The temporary candidate FETCH_HEAD exactly equals the initially captured control FETCH_HEAD.

The temporary candidate was also successfully switched to that same HEAD and has a resolved TREE.

Therefore the race guard inside temporary candidate fetch/preparation did NOT fire.

The qualified recovery implementation contains only one remaining BLOCKED_REMOTE_HEAD_RACE checkpoint after successful candidate preparation:

    _ensure_remote_still_exact(control_repo, expected_head)

Accordingly:

    EXACT FAILED CHECKPOINT
    = FINAL PRE-HANDOFF REMOTE RECHECK

The monitored branch advanced after candidate identity had been frozen and after the clean temporary candidate had been prepared, but before the qualified P5-D3F handoff runtime was invoked.

## Governance meaning

This is expected fail-closed behavior, not an implementation defect.

The system correctly refused to materialize a READY_UNAUTHORIZED handoff from a candidate that had become stale relative to integration/system-v1.

No weakening or removal of the race guard is warranted.

## State after failure

The prior runner residual showed only:

    staging/
      packages/

No handoff success result was emitted.
No REAL_VAULT_ZERO_MUTATION PASS result was emitted.
The one-shot authorization is consumed.

## Next gate

Before another one-shot authorization can be considered:

1. verify staging remains exactly PRESENT_EMPTY_PACKAGES_RECOVERY;
2. verify integration/system-v1 remains stable across a bounded read-only quiet window;
3. bind any later authorization to the then-current remote HEAD and unchanged qualified V0.3 runner blob;
4. perform at most one new real attempt.

No retry is authorized by this report.
