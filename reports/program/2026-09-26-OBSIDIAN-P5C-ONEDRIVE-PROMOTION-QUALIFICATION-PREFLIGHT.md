# OBSIDIAN P5-C — ONEDRIVE PROMOTION QUALIFICATION PREFLIGHT

Date: 2026-09-26

## Scope

P5-C preregisters the empirical protocol for qualifying or rejecting Windows/OneDrive promotion primitives before continuous projection may modify the live machine-owned Obsidian layer.

No live Vault mutation is authorized.

## Exact predecessor

Qualified P5-B2 closure:

    eb7b3202c8c3c9ced8cb6d068051e0a922da5e22

## Candidate branch

    feat/obsidian-projection-p5c-onedrive-promotion-qualification-v0.1

## Persisted candidate artifacts

Contract:

    tools/obsidian_projection/onedrive_promotion_contract_v0_1.json
    blob: 36e49e72a867e30a69f63eb413fd924d0e56297b

Documentation:

    docs/OBSIDIAN-P5C-ONEDRIVE-PROMOTION-QUALIFICATION-CONTRACT-V0.1.md
    blob: fff34dd1aad090c03b6b860ad50301ce4fefbcc6

Contract breakers:

    tests/obsidian_projection/test_onedrive_promotion_contract_v0_1.py
    blob: c964fbc2fac8edc344c4090c498d560c4d3be473

## Sandbox-only experiment

Live Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

is protected and must not be used as the experiment target.

Required sacrificial sandbox:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C-PROMOTION-SANDBOX

The sandbox is chosen under the same OneDrive root to preserve relevant local filesystem/provider conditions without risking the real Vault.

## Primary invariant

    ZERO_MIXED_GENERATION_VISIBILITY

The reader probe also requires zero:

- missing entrypoint;
- partial generation;
- parse error.

## Candidate set

Negative control:

    DIRECT_IN_PLACE_PER_FILE_REPLACE

Qualifiable candidates:

    DIRECTORY_TWO_RENAME_SWAP
    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE
    IMMUTABLE_GENERATION_ATOMIC_POINTER

No candidate is assumed to work.

All candidates failing is a valid result.

## Scale

Each qualifiable candidate requires at least:

    250 promotion cycles
    5000 reader samples
    A→B and B→A transitions

The reader sampling interval must be <= 10 ms.

## Crash and Obsidian-open boundaries

The finally selected filesystem primitive requires crash-recovery testing.

Filesystem PASS alone does not authorize promotion while the real Vault is open in Obsidian.

Obsidian-open behavior requires a later sacrificial sandbox-Vault subqualification.

## Non-authorizations

P5-C contract does not authorize:

- sandbox execution yet;
- real Vault mutation;
- background observer;
- continuous synchronization;
- Windows Task Scheduler registration.

## Required re-break

Before P5-C2 implementation:

1. exact persisted P5-C control clone;
2. targeted P5-C contract breakers;
3. full Obsidian projection suite;
4. no tracked change;
5. no unexpected untracked files.

Python bytecode writing must remain disabled.

## Next gate

    P5-C2 — PROMOTION EXPERIMENT HARNESS CANDIDATE

## Current verdict

**P5-C CONTRACT CANDIDATE PERSISTED — LOCAL RE-BREAK REQUIRED**
