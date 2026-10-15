# Python Environment Baseline — MT5 Source Discovery

**Status:** EXECUTABLE BASELINE
**Scope:** MT5 source discovery only
**Branch:** `feat/min-experiment-gaps-batch-v1`

## 1. Purpose

The repository previously had no explicit Python environment contract. This document establishes the minimum reproducible baseline required to execute the read-only MT5 tick-source probe.

This is an environment contract, not a claim that the MT5 market-data source is qualified.

## 2. Baseline

```text
Interpreter: CPython 3.13.x
Platform: Windows x64
Isolation: repository-local .venv
Direct dependency: MetaTrader5==5.0.6180
```

Python 3.13 is selected because the current official `MetaTrader5` release used by this contract publishes a Windows x64 CPython 3.13 wheel. The exact interpreter micro-version remains part of the runtime evidence captured by the verification step.

## 3. Dependency contract

The direct MT5 integration dependency is pinned in:

```text
requirements-mt5.txt
```

The contract intentionally starts with only the dependency required by the probe. It must not be interpreted as the complete dependency set for the future research stack.

Transitive dependencies are resolved by pip and must be captured in the environment evidence before an experiment is treated as reproducible.

## 4. Environment creation

From the repository root on Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap_python_env.ps1
```

The bootstrap script:

1. requires the Windows Python Launcher;
2. verifies CPython 3.13 is available;
3. creates `.venv` if absent;
4. installs the pinned MT5 dependency;
5. verifies the `MetaTrader5` import and exact package version.

No trading action and no market-data acquisition occurs during bootstrap.

## 5. Environment verification

After bootstrap:

```powershell
.\.venv\Scripts\python.exe .\tools\verify_python_environment.py
```

Expected result:

```text
status = PASS
PYTHON_BASELINE = PASS
MT5_IMPORT = PASS
```

A mismatch is a failure of the environment prerequisite, not evidence that MT5 market data is unavailable.

## 6. MT5 probe boundary

The existing read-only probe remains the next executable layer:

```text
Python baseline
    ↓
isolated .venv
    ↓
MetaTrader5==5.0.6180
    ↓
tools/probe_mt5_tick_source.py
    ↓
Nas100.s / Nas100cash
    ↓
source qualification evidence
```

The probe does not sort, deduplicate, repair, normalize, resample, or persist market data. It only tests terminal connectivity and historical tick availability for an explicitly requested symbol and UTC interval.

## 7. Qualification boundary

Environment PASS does **not** imply source PASS.

The following remain separate gates:

- `ENVIRONMENT BASELINE` — can the controlled probe execute?
- `TERMINAL CONNECTIVITY` — can the Python integration initialize the user's MT5 terminal?
- `SYMBOL IDENTITY` — does the exact requested symbol exist and correspond to the intended VT Markets instrument?
- `TICK AVAILABILITY` — does `COPY_TICKS_ALL` return usable ticks?
- `HISTORICAL DEPTH` — how far back is usable history available?
- `DATA QUALITY` — are Bid/Ask, timestamps, ordering, gaps and coverage adequate?
- `EXPERIMENTAL ADMISSIBILITY` — does the resulting dataset satisfy the repository data contract?

No gate may be silently promoted from unknown or blocked to pass.

## 8. Current status

Before this baseline, the MT5 probe was blocked because the active Python interpreter did not contain the `MetaTrader5` package.

After this commit, the repository contains an explicit environment contract and a controlled bootstrap path. Actual execution remains pending on the user's Windows machine because the MT5 Python package and terminal are machine-local prerequisites.
