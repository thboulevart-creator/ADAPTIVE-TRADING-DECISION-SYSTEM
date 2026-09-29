# OBSIDIAN P5-D3F — RECOVERY V0.4 LOCAL HEAD MISMATCH CONFIRMATION V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL READ-ONLY CONFIRMATION plus VERIFIED GITHUB remote state.

## Confirmed local state after blocked V0.4 invocation

    LOCAL_HEAD = d2445091ad1a0d646cbf016e52f5c9a19057e89b
    git status --porcelain --untracked-files=all = EMPTY

Therefore the control clone was clean but remained on the functional qualification candidate rather than the authorization-bearing runner HEAD.

## Authorized runner HEAD for the consumed attempt

    1d725a35490fbf0c137072152d2876c53d63f183

## Root-cause closure

The blocked outcome:

    RealExecutionRunnerError: local HEAD is not the authorized runner HEAD

is fully explained by the local repository identity mismatch:

    actual   = d2445091ad1a0d646cbf016e52f5c9a19057e89b
    expected = 1d725a35490fbf0c137072152d2876c53d63f183

No repository dirtiness contributed.

## Post-confirmation GitHub state

V0.4 runner branch:

    1d725a35490fbf0c137072152d2876c53d63f183

V0.4 runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

integration/system-v1:

    59f1dc26973b0b50efefccf12b26784d1e41f546

## Governance consequence

The prior one-shot authorization remains consumed.

No retry is authorized.

Before requesting a fresh one-shot authorization, the local clone should first be positioned on the exact current V0.4 runner branch HEAD and reverified clean, then the monitored head and recovery staging prestate should be rechecked.
