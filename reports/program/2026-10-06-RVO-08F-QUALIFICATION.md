# RVO-08F — SINGLE AP1 EXECUTION FAILURE FORENSIC DIAGNOSIS V0.1

## Adjudication

```text
RVO-08F = QUALIFIED_FORENSIC_DIAGNOSIS
ROOT_CAUSE = PROVEN
REPAIR = SYNTHETICALLY_QUALIFIED_NON_AP1
RETRY_AUTHORIZED = FALSE
```

## Root cause

The failed RVO-08 command used Python `-I`. On the qualified Windows Store Python runtime this suppresses the user-site containing `tzdata`, NumPy and PyArrow.

AP1 evaluates `NY = ZoneInfo("America/New_York")` at module import, before `main()` and before AP1's blocked-output writer can run. Under the isolated runtime the timezone data is unavailable; the discriminating synthetic probe reproduces `ZoneInfoNotFoundError`, process exit code 1 and no output file.

The prior WindowsApps `Access denied` observation is not the root cause: the frozen interpreter path passed benign process-spawn probes and the P1.12C runner passed a synthetic no-op producer with that runtime.

## Repair

The bounded repair replaces `-I` with `-E -P` and allows only the Windows-local runtime events observed to be required by NumPy/tzdata. Subprocess creation, network sockets, arbitrary DLLs and exec/spawn events remain blocked.

Exact repaired blobs:

```text
src/p1_12c_qualified_producer_execution.py
87d2ef49c0b70b956ada19443f5ba693cfb5b242

tools/p1_12c_sandbox_runner.py
78aa1615a093c241774fdea1018b69f47728ecb6

tools/ap1_intraday_spread_census.py
9f613063fb8a190a1ff6f2f8b12c97c4ed97712a
```

## Test-first and regression evidence

```text
RED @ cc5012a70490a7bcf6b1b4b8f7a4809c27e3b1a4
3 failed / 5 passed

Fresh local qualification @ 695f4eb4232e4b80e19221b9b5f8270875068457
RVO-08F repair = 8 PASS
P1-21 breakers = 29 PASS
P1-21 positive = 18 PASS
RVO-08 controller = 5 PASS
RVO-07 breakers = 35 PASS
RVO-07 positive = 20 PASS
G05 breakers = 30 PASS
G05 positive = 19 PASS
SMF-AP1-M03 breakers = 28 PASS
SMF-AP1-M03 positive = 25 PASS
DATA-02 breakers = 32 PASS
```

## New derived identities

```text
INVOCATION_PROFILE_DIGEST =
7487a1ffc0adab8c60bd36caf196130402908367c676bb03ca9abe36b56c6d9c

RUNTIME_LOCK_ID =
RPRL-25a96a47d1a1e1677374974e9fe7c8db

RUNTIME_LOCK_DIGEST =
25a96a47d1a1e1677374974e9fe7c8dbd8e3abb37a0f3a1e0566ebd1d88fb306

SYNTHETIC_PLAN_ID =
QRPP-2ac33559a1e042362ef42940576c9f61

SYNTHETIC_PLAN_DIGEST =
2ac33559a1e042362ef42940576c9f61175fd07047b0c04c5872ba33ed562bd6
```

The old RVO-08 freeze and runtime lock cannot be reused for any retry.

## Boundary

```text
LEDGER INVOCATION COUNT = 1
NEW REAL AP1 INVOCATION = FALSE
REAL AP1 OUTPUT = ABSENT
REAL M03 = FALSE
BACKTEST = FALSE
NEW OOS = FALSE
PAPER = FALSE
BROKER/LIVE = FALSE
CAPITAL = FALSE
RETRY AUTHORITY = FALSE
```
