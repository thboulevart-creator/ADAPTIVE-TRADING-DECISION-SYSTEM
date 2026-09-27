# OBSIDIAN P5-C3R — SEMANTIC PARTIAL FORENSICS PREFLIGHT

Date: 2026-09-27

## Source failure

First P5-C3R RUN-OPEN runtime candidate:

    ae7d1adbb146fffb60c4e302750abb896136d968

Persisted user-reported failure record:

    reports/program/2026-09-27-OBSIDIAN-P5C3R-RUN-OPEN-FAILURE-USER-REPORTED.md
    blob: d30ddf348c7be2de18cd0c7feca20d0517e61463

Observed failing metric:

    semantic_partial_generation_count = 19

## Forensic branch

    feat/obsidian-projection-p5c3r-semantic-partial-forensics-v0.1

Candidate HEAD before local re-break:

    71aaf98954e735d417d0b00b81c28b12c2247341

## Exact persisted artifacts

Forensic implementation:

    tools/obsidian_projection/obsidian_open_retry.py
    blob: 318eea1608cdd1f0d54d24903314c4ed2e105ddd

Unit tests:

    tests/obsidian_projection/test_obsidian_open_retry.py
    blob: b4eae74f0f72cf26126a7c16d8c06cfe557d6455

Adversarial breakers:

    tests/obsidian_projection/test_p5c3r_adversarial.py
    blob: 9969b50cc63f961deec78477f5345e28a69f9577

Forensic protocol:

    docs/OBSIDIAN-P5C3R-SEMANTIC-PARTIAL-FORENSICS-V0.1.md
    blob: af88d40796870fa6e27f413d61d79f9109da3b20

Unchanged retry contract:

    tools/obsidian_projection/obsidian_open_retry_contract_v0_1.json
    blob: 82cc7e100017d5e2db671ccce989f5e0e2afe912

Unchanged open runner:

    tools/obsidian_projection/run_p5c3r_open.ps1
    blob: ea6dc7d45d98df9507db4015d4e15b76fbc1fd52

Unchanged base P5-C3 harness:

    tools/obsidian_projection/obsidian_open_compatibility.py
    blob: b970e65f21792cccc6ee2e4271d630f371102ff7

## Delta purpose

The implementation adds only:

- a stable semantic-partial signature formatter;
- per-signature counting in the reader metrics;
- total signature accounting;
- report fields carrying those signatures.

The tests add:

- direct signature coverage for FileNotFoundError;
- direct signature coverage for a non-retryable WinError;
- reader accounting coverage for one synthetic semantic partial;
- adversarial assertions that the qualification failure criterion remains unchanged.

## Explicit non-changes

The following remain unchanged:

    retryable WinErrors = {5, 32}
    write deadline = 5000 ms
    reader deadline = 500 ms
    promotion cycles = 250
    minimum reader samples = 5000
    atomic publication = os.replace(CURRENT.tmp, CURRENT.md)
    semantic_partial_generation_count required for PASS = 0

No semantic partial is converted into a retry by this candidate.

## Required local re-break before forensic runtime

With Obsidian closed:

1. checkout exact candidate;
2. run targeted P5-C3R tests;
3. run full Obsidian test suite;
4. require clean working tree;
5. no recovery unless state evidence requires it.

Only after those gates pass may a new Obsidian-open diagnostic run be considered.

## Runtime interpretation rule

A future diagnostic run remains FAIL whenever:

    semantic_partial_generation_count > 0

The new signatures may explain the failure but do not waive it.

No new retry code may be added solely because a signature appears. Any policy change requires separate preregistration and breakers.

## Non-authorizations

    p5c3r_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false
