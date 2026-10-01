# P5-E V0.1 — TARGETED CLOSURE PREDECESSOR REGRESSION

Date: 2026-10-01

## Scope

Targeted regression after B1→B5 closure and requirement/evidence matrix qualification.

Covered surfaces:

- P5-A continuous projection contract;
- P5-D1 continuous observer core contract;
- P5-D2 one-shot observer contract;
- P5-D2 observer tick implementation;
- P5-D4 bounded-loop contract;
- P5-D4 bounded-loop runtime;
- P5-D4 bounded-loop adversarial runtime;
- P5-D4 control-root remediation base;
- P5-D4 control-root remediation adversarial;
- corrected P5-E contract/base tests;
- corrected P5-E adversarial tests;
- external-review B1→B5 targeted-closure tests;
- P5-E requirement/evidence matrix tests.

## Result

```text
Ran 270 tests in 5.173s

OK

TARGETED_REGRESSION_EXIT=0
```

P5-D4 runtime blob during regression:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

No P5-D4 runtime modification occurred.

## Non-failing observations

Historical subprocess tests emitted `ResourceWarning` messages for unclosed text streams.

They did not change the unittest verdict.

Three Python 3.14 bytecode-cache files were produced by cross-interpreter tests and are removed before persistence.

## Authority

No real P5-E polling, head evaluation, Stage A/B, promotion, publication, Vault mutation, CURRENT mutation, daemon, Scheduled Task, Windows Service, startup registration, P6, or normative human adoption occurred.

```text
TARGETED_PREDECESSOR_REGRESSION = 270 / 270 PASS
REAL_P5E = CLOSED
```

The next preregistered operation is exactly one full Obsidian re-break.
