# P5-E V0.1 — BB1 TARGETED PREDECESSOR REGRESSION

Date: 2026-10-02

## Execution identity

Branch:
`feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure`

HEAD:
`e276962b9e5c89e32c75fc35e16fb07b200d06ee`

P5-D4 runtime blob:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## Covered surfaces

- P5-A continuous projection contract;
- P5-D1 continuous observer core;
- P5-D2 one-shot observer contract and behavioral runtime tests;
- P5-D4 bounded-loop contract/runtime/adversarial/control-root remediation;
- P5-E contract, adversarial, B1→B5 closure, evidence matrix;
- BB1 normative-guard closure.
## Result

```text
Ran 282 tests in 5.356s

OK

TARGETED_REGRESSION_EXIT=0
```

Historical subprocess tests emitted three non-failing `ResourceWarning` messages for unclosed text streams.

Cross-interpreter tests generated three Python 3.14 bytecode-cache files.

Those cache files are runtime residue only and are removed before persistence.

## Verdict

```text
TARGETED_PREDECESSOR_REGRESSION = 282 / 282 PASS
P5D4_RUNTIME = UNCHANGED
REAL_P5E = CLOSED
```

The next preregistered step is exactly one full Obsidian suite in a disposable clone.
