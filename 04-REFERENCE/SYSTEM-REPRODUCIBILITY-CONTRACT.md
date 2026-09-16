# SYSTEM REPRODUCIBILITY — TIER-A CONTRACT V1

**Contract ID:** `SYSTEM_REPRODUCIBILITY_ENVELOPE_V1`  
**Boundary:** repository qualification environment → reproducible P0.2–P0.5 execution  
**Tier:** `A`  
**Initial status:** `BLOCKED` until adversarial qualification

## 1. Purpose

P0.2–P0.5 are behaviorally qualified, but their execution environment is not yet a versioned authority.

Observed pre-P0.6 qualification currently depends on ambient GitHub Actions state:

- workflow Python is declared as `3.12`, while the final P0.5 runner resolved CPython `3.12.14`;
- durable boundary workflows still use `ubuntu-latest` while integration gates use `ubuntu-24.04`;
- `pytest==8.4.2` is pinned directly but its resolved transitive dependencies are not versioned;
- `actions/checkout@v4` and `actions/setup-python@v5` are moving tags rather than immutable action commits;
- no repository-wide qualification dependency lock or machine-verifiable environment lock exists.

A green gate under one ambient runner state is therefore not yet proof that the same qualification can be reconstructed later or on another compatible runner.

## 2. Observed dependency inventory

The currently qualified P0.2–P0.5 runtime path uses Python standard-library modules only.

The final P0.5 persisted-HEAD run resolved the test stack to:

- `pytest==8.4.2`;
- `iniconfig==2.3.0`;
- `packaging==26.3`;
- `pluggy==1.6.0`;
- `Pygments==2.21.0`.

The same run resolved:

- CPython `3.12.14`;
- runner family `ubuntu-24.04` / Ubuntu `24.04.5`;
- `actions/checkout` commit `11d5960a326750d5838078e36cf38b85af677262`;
- `actions/setup-python` commit `a26af69be951a213d495a4c3e4e4022e16d87065`.

The exact hosted-runner image build observed (`20260907.300.1`) is evidence, not an authority: GitHub-hosted image internals are not directly pin-able by `runs-on` and MUST NOT be misrepresented as immutable.

`tools/probe_research_execution_compatibility_v4_3.py` contains an optional runtime import of `pyarrow` only for Parquet input. No qualified P0.2–P0.5 run installs or exercises that path. P0.6 MUST therefore mark that optional Parquet dependency as outside the current reproducibility envelope instead of inventing a version.

## 3. Smallest authoritative lock

P0.6 must introduce exactly the minimum machine-verifiable authority needed for the current qualification path:

1. one exact qualification requirements lock containing every observed PyPI package used by the qualified test stack;
2. one environment lock declaring the exact CPython version, supported runner family, immutable action commits, deterministic environment variables, and the SHA-256 identity of the requirements lock;
3. one verifier that fails closed when the running qualification environment or persisted workflow configuration differs from that lock.

No application package manager, container platform, virtual-environment framework or second dependency system may be added merely to satisfy P0.6.

## 4. Authoritative environment semantics

The P0.6 qualification envelope is:

- implementation: CPython;
- exact Python: `3.12.14`;
- OS family: Linux;
- GitHub hosted runner label: `ubuntu-24.04`;
- qualification architecture: `X64` when executed in GitHub Actions;
- deterministic environment values:
  - `PYTHONDONTWRITEBYTECODE=1`;
  - `PYTHONHASHSEED=0`;
  - `TZ=UTC`;
  - `LANG=C.UTF-8`;
  - `LC_ALL=C.UTF-8`;
- exact qualification package versions from the requirements lock;
- immutable checkout/setup-python action commits recorded by the environment lock.

The hosted-runner image revision, Linux kernel patch level, Azure region and ephemeral runner identity are observational metadata, not lock fields.

## 5. Workflow requirements

Every qualification workflow protecting the current P0.2–P0.5 system MUST:

- use `ubuntu-24.04`, never `ubuntu-latest`;
- use the immutable checkout/setup-python commits from the environment lock;
- request Python `3.12.14`, never a floating `3.12` line;
- install the qualification stack only from the authoritative requirements lock;
- run the environment verifier before protected tests;
- carry the deterministic environment variables from section 4;
- remain `contents: read`;
- trigger when the reproducibility contract, environment lock, requirements lock or verifier changes where the workflow is path-scoped.

P0.6 does not require making integration-lineage gates semantically valid on unrelated histories. Transportability means their execution environment is reconstructible and their reusable boundary workflows are branch-neutral where already intended; it does not erase lineage checks.

## 6. Fail-closed verification

The verifier MUST reject at least:

- wrong Python implementation;
- Python patch/minor drift;
- unsupported OS family;
- wrong GitHub runner family or architecture when running under Actions;
- missing required deterministic environment variable;
- changed deterministic environment value;
- missing locked package;
- locked package version drift;
- requirements-lock content/hash drift;
- environment-lock schema drift;
- workflow use of floating action tags;
- workflow use of `ubuntu-latest`;
- workflow use of floating `3.12`;
- direct one-off `pip install pytest...` that bypasses the lock.

The verifier must distinguish current-environment verification from synthetic adversarial snapshots so attacks do not mutate the actual CI environment.

## 7. Required adversarial attacks

P0.6 must at minimum prove:

- `E0` positive current locked environment;
- `E1` Python implementation drift rejected;
- `E2` Python version drift rejected;
- `E3` OS drift rejected;
- `E4` GitHub runner family/architecture drift rejected;
- `E5` deterministic environment variable missing/drift rejected;
- `E6` required package missing rejected;
- `E7` required package version drift rejected;
- `E8` requirements file modified while environment lock keeps the old digest rejected;
- `E9` environment-lock unknown/missing/schema-substituted fields rejected;
- `E10` floating action tag rejected;
- `E11` `ubuntu-latest`, floating Python or direct pytest installation rejected;
- `E12` optional `pyarrow` Parquet path remains explicitly outside P0.6 and cannot be silently represented as locked;
- `E13` P0.2, P0.3, P0.4 and P0.5 adversarial suites all survive under the locked environment;
- `E14` full repository regression and acquisition/backtest prohibitions survive.

## 8. Qualification rule

P0.6 may be PASS only after:

`formalisation → observed FAIL on pre-lock state → minimal lock/verifier/workflow correction → E0–E14 re-break → full repository regression → P0.2→P0.5 re-break → persisted-HEAD re-break → bounded JIT audit/report/checkpoint/backup → final documentary persisted-HEAD re-break`

A requirements file alone is insufficient. A workflow that still floats Python, actions or runner family is insufficient.

## 9. Explicitly outside P0.6

P0.6 does not authorize or close:

- `pyarrow`/Parquet qualification beyond documenting that it is currently outside the envelope;
- native `.bi5` acquisition or acquisition readiness;
- exact OOS split;
- real-data backtest;
- non-replay cryptographic bearer attestation;
- `DECISION → RISK → ACTION → RESULT → TRACE` completion;
- promotion gate or live activation;
- immutable pinning of GitHub-hosted runner image internals that GitHub does not expose as a stable `runs-on` target.
