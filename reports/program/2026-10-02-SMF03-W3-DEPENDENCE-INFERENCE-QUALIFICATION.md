# SMF-03 — W3 DEPENDENCE / INFERENCE QUALIFICATION

Date: 2026-10-02

Branch:
`feat/smf03-core-implementation-v0.1`

Qualified surface:

```text
SMF-03-W3
M04 + M05 + M06
SYNTHETIC ONLY
```

Base SMF-03 identity:

```text
BASE HEAD = 88f6978a77e87bed4ccef0708cdde7bfbbf7e929
BASE TREE = 586bc319990d7f1e0c45b38d6e32a5cea7203765
```

Qualification head:

```text
HEAD = 51cb2e176fe44e6f4c69cba8e1780e5e4d350805
TREE = c801f4617d78cd7e2933b845cc3993570f2e7d90
```

Exact blobs:

```text
CONTRACT = 618171fd013f7f9cfe39f233048e650fc276b729
BREAKER = b190848223210467b8535ebcf98ba190e9ab65b7
RUNTIME = fce7998167745659cb0fd5d03a8de14946b0394d
REFERENCE = f134c0a8c7a1832be3e851a2597f2f7218fab6c9
CI_WORKFLOW = cc69c1e63edea511516de940d9fd276e90ceaadc
```

Test-first sequence:

```text
EXPECTED RED:
27 failed
reason = MODULE_ABSENT_EXPECTED_RED

FIRST GREEN ATTEMPT:
25 passed / 2 failed
```

Initial findings:

```text
F01:
independent ACF paths differed only by floating last-bit representation.
Correction:
freeze independent-reference parity tolerance:
rel = 1e-12
abs = 1e-15

F02:
the first bootstrap fixture was symmetric enough for PERCENTILE and BASIC
to return the same interval.
Correction:
replace it with a discriminating asymmetric synthetic fixture.
```

Final local re-break:

```text
27 passed in 0.12s
pytest = 8.4.2
```

Canonical CI:

```text
GitHub Actions run = 37048517793
runner = ubuntu-24.04
python = 3.12.14
requirements = requirements/qualification.lock.txt
head = 51cb2e176fe44e6f4c69cba8e1780e5e4d350805
conclusion = SUCCESS
```

Qualified implementation semantics:

```text
M04:
explicit lags + explicit estimator + explicit threshold
structural dependence remains distinct from ACF diagnostics
no "independence proven" claim

M05:
IID or MOVING_BLOCK only under explicit routing
IID requires explicit justification
MOVING_BLOCK requires explicit block length
unresolved non-stationarity blocks global resampling
interval method / confidence / replications / seed are explicit

M06:
only explicit NORMAL_MEAN_KNOWN_SIGMA synthetic qualification model
no automatic model selection
no post-hoc observed power as evidence
precision and power targets must be explicit
```

Verdict:

```text
SMF03_W3 =
QUALIFIED_WITHIN_DEFINED_SYNTHETIC_SURFACE

M04 =
QUALIFIED_IMPLEMENTATION_CANDIDATE

M05 =
QUALIFIED_IMPLEMENTATION_CANDIDATE

M06 =
QUALIFIED_IMPLEMENTATION_CANDIDATE
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
MODEL VALIDITY OUTSIDE EXPLICIT CONTRACTS
PAPER / BROKER / LIVE / CAPITAL
```
