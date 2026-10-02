# SMF-03 — W4 EVIDENCE GOVERNANCE QUALIFICATION

Date: 2026-10-02

Branch:
`feat/smf03-core-implementation-v0.1`

Qualified surface:

```text
SMF-03-W4
M07 + M08 + M09 + M10 + M11
SYNTHETIC ONLY
```

Qualification head:

```text
HEAD = 26018c1ac911fcd69e1f08e4c4571b474599fc2c
TREE = 67a3facf45d18f00e1c63855592cb4054d85bc04
```

Exact blobs:

```text
CONTRACT = 67014f4fb753e3165cacc0ae59a49b522e84fa87
BREAKER = c913f1bd8fdb6f48e046aa78bd906c55c19f34b8
RUNTIME = 7ba33f9f9ce8dda49abdd1a7dff7a1b1cc0a0222
REFERENCE = 55c47f98f574286242e8bf9a09156d24134130bd
CI_WORKFLOW = 08d12fc3f8ff64aae4a8724b8d2114db939e799a
```

Test-first sequence:

```text
EXPECTED RED:
33 failed
reason = MODULE_ABSENT_EXPECTED_RED

FIRST GREEN ATTEMPT:
32 passed / 1 failed

FINDING:
breaker EG-09 compared declared threshold 0.6
to observed inclusion-rate gap 0.5.

TARGETED CORRECTION:
assert observed_inclusion_rate_gap == 0.5
and max_inclusion_rate_gap == 0.6 separately.

FINAL LOCAL RE-BREAK:
33 passed in 0.11s
```

Canonical same-head CI:

```text
HEAD = 26018c1ac911fcd69e1f08e4c4571b474599fc2c

W1-W2 run = 37049159949 = SUCCESS
W3 run = 37049160070 = SUCCESS
W4 run = 37049160217 = SUCCESS

runner = ubuntu-24.04
python = 3.12.14
requirements = requirements/qualification.lock.txt
```

Qualified implementation semantics:

```text
M07:
leave-one-dependence-unit-out influence
explicit materiality threshold
no automatic outlier deletion

M08:
explicit inclusion/exclusion reasons
stratum-level inclusion rates
explicit material asymmetry threshold

M09:
PRISTINE -> EXPOSED -> CONTAMINATED
monotonic exposure only
no reset to pristine

M10:
predeclared strata only for confirmatory stability
explicit minimum N per stratum
explicit mean-spread tolerance
post-hoc regime rescue forbidden

M11:
search universe status explicit
KNOWN requires explicit governed n_trials
PARTIAL/UNKNOWN => n_trials = null
registry count never becomes n_trials
```

Verdict:

```text
SMF03_W4 =
QUALIFIED_WITHIN_DEFINED_SYNTHETIC_SURFACE

M07-M11 =
QUALIFIED_IMPLEMENTATION_CANDIDATES
```

Meaning of PASS:

```text
NO FAILURE FOUND
WITHIN THE DEFINED
AND ACTUALLY TESTED
IMPLEMENTATION SURFACE
```

Not authorized or claimed:

```text
REAL BACKTEST
REAL PERFORMANCE OBSERVATION
OOS CONSUMPTION
STRATEGY QUALIFICATION
GENERALIZABLE EDGE
PAPER / BROKER / LIVE / CAPITAL
```
