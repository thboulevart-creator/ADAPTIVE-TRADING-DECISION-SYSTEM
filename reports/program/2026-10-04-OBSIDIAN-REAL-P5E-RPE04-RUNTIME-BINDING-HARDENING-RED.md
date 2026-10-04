# RPE-04 — RUNTIME BINDING + POST-FETCH REVALIDATION HARDENING — RED

Date: 2026-10-04

## Why this hardening exists

A self-audit before external review identified that the candidate loaded the governed preregistration/schema and the adopted RPE-01/RPE-03 code from disk without independently binding the exact bytes consumed at runtime.

The audit also identified a small time-of-check/time-of-use surface between the pre-fetch checks and the RPE-03 classification.

No external reviewer finding was required to identify these issues.

## Frozen hardening test

tests/obsidian_projection/test_rpe04_runtime_binding_hardening_v0_1.py

Worktree blob before persistence:

d1bf928dd205a4d6c47761cf0a535aa5b315f10a

## RED result

Ran 5 tests.

- 2 ERROR: runtime binding function/identity map absent.
- 3 FAIL: Git identity, local-config allowlist, and physical object-domain checks occur only once before fetch.

HARDENING_RED_EXIT = 1

## Required closure

The implementation must:
- bind the raw SHA-256 bytes of the exact preregistration, schema, RPE-01 guard, and RPE-03 classifier it reads;
- fail closed on any runtime binding mismatch;
- reverify physical object-domain containment after fetch;
- reverify exact Git executable identity before RPE-03 classification;
- reverify local config allowlist before RPE-03 classification.

No claim scope or authority expansion is introduced.
