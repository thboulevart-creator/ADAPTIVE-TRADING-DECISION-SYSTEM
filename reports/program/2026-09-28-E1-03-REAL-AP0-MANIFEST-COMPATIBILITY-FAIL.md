# E1-03 — REAL AP0 MANIFEST COMPATIBILITY — OBSERVED FAIL

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Reviewed persisted HEAD:

`78a7fdd38bf58991971fafff696536fd5551553b`

Reviewed persisted TREE:

`d0fe90556de90c4d9ec8ded9f2719ea1ca7ae40f`

## 1. Scope

This artifact records the first real-input compatibility failure observed during:

`E1-03 — REAL AP0 → H1 QUALIFICATION`

No runtime correction is authorized or performed by this artifact.

No AP0 Parquet file was read and no real H1 build was started.

## 2. Protected E1-03 identities

```text
contract blob =
c2d4323039d65fcd9319d4f5eb02f45ee27c8afc

frozen H1-01..H1-21 breaker blob =
958e338a1e9e7c5b56198eb3585f25ca140aa331

runtime blob =
6abe23caea680a40c892cd5a470331ca63c67e2e
```

These objects were revalidated unchanged before the real-input compatibility check.

## 3. Exact real AP0 manifest identity

The AP0 manifest recovered from the governed prior execution evidence was materialized and independently hashed.

```text
size_bytes = 26900
sha256 = 62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce
schema = ATDS_AP0_USTECH_PROFILE_MINUTE_CORE_MANIFEST_V0_1
status = AP0_COMPLETE
output_identity = USTECH_PROFILE_MINUTE_CORE_V0_1
files = 61
```

The exact SHA-256 matches the previously governed AP0 identity.

The real file-record schema contains:

```text
relative_path
sha256
size_bytes
rows
source_ticks
first_minute_ms_utc
last_minute_ms_utc
first_segment_id
last_segment_id
```

The real file records do not contain a `path` field.

Example real value:

`year=2021/month=05/USTECH-PROFILE-M1-2021-05.parquet`

## 4. Observed compatibility defect

The persisted runtime `verify_ap0_binding()` currently resolves each AP0 file using:

`rec.get("path")`

The governed real AP0 manifest provides:

`rec["relative_path"]`

Therefore the real manifest fails before any Parquet open/read and the runtime returns:

```text
status = BLOCKED
reason = AP0_FILE_RECORD_INVALID
```

This is a runtime/fixture compatibility defect, not an AP0 identity mismatch.

## 5. Why the frozen synthetic suite did not catch it

The frozen H1-18/H1-19 synthetic helper constructs file records with:

`"path": rel`

Therefore the synthetic fixture reproduced the runtime assumption rather than the governed AP0 manifest schema.

Historical synthetic qualification remains true as an observation:

`H1-01..H1-21 = 21/21 PASS`

but it is insufficient to establish real AP0 compatibility.

## 6. Adjudication

```text
E1_03_AP0_MANIFEST_IDENTITY = PASS
E1_03_REAL_INPUT_COMPATIBILITY = FAIL

E1_03_REAL_AP0_FILE_REHASH = NOT_EXECUTED
E1_03_REAL_H1_BUILD = NOT_EXECUTED
E1_03_REAL_CANONICAL_DIGEST = UNKNOWN
E1_03_REAL_DETERMINISTIC_REBUILD = NOT_EXECUTED

E1_03_FINAL_VERDICT = FAIL
```

Fail-closed behavior was preserved. No field aliasing, manifest rewriting, silent conversion or runtime correction was performed.

## 7. Test-first regression preregistration

A new independent regression breaker is persisted with this evidence:

`breakers/e1_03_real_ap0_manifest_compatibility_breaker.py`

Case:

`RC01 — governed AP0 file records using files[].relative_path must be accepted and all 61 declared files re-hashed`

The fixture reproduces the relevant governed real AP0 schema and deliberately does not provide `files[].path`.

At this persistence point:

```text
RC01_PERSISTED_BEFORE_FIRST_EXECUTION = TRUE
RC01_EXECUTION = NOT_YET
RUNTIME_CORRECTION = NONE
```

The first permitted action after this commit is to execute RC01 against the unchanged persisted runtime and observe its RED profile.

No runtime mutation is authorized by this artifact.

## 8. Persisted RC01 execution

RC01 was executed only after its breaker had been persisted.

Persisted preregistration HEAD:

`cb794e2449c242c6906d2fa5eacbd37ee5a6ac27`

Persisted preregistration TREE:

`7410f84cf832386e715eab6c028fe4c626c7a823`

Protected runtime blob:

`6abe23caea680a40c892cd5a470331ca63c67e2e`

Persisted RC01 breaker blob:

`38db4d3c01d60b885a694183df6da8317fd30dc0`

Execution profile:

```text
PY_COMPILE = PASS

RC01_TOTAL = 1
RC01_PASS = 0
RC01_FAIL = 1

OBSERVED_STATUS = BLOCKED
OBSERVED_REASON = AP0_FILE_RECORD_INVALID
```

Ordering:

```text
RC01_PERSISTED_BEFORE_FIRST_EXECUTION = TRUE
```

Interpretation:

The regression test reproduces the governed AP0 manifest convention `files[].relative_path` against the unchanged runtime, while deliberately omitting the synthetic-only `files[].path` field.

The observed RED is therefore causal and interpretable:

```text
REAL AP0 file-record key = relative_path
CURRENT runtime key lookup = path
RESULT = AP0_FILE_RECORD_INVALID
```

No runtime correction occurred before or during this execution.

## 9. RC01 adjudication

```text
E1_03_RC01_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_03_RC01_PERSISTED_BEFORE_FIRST_EXECUTION = TRUE

E1_03_REAL_INPUT_COMPATIBILITY = FAIL
E1_03_RUNTIME_CORRECTION = NONE

E1_03_REAL_AP0_FILE_REHASH = NOT_EXECUTED
E1_03_REAL_H1_BUILD = NOT_EXECUTED
E1_03_FINAL_VERDICT = FAIL
```

The next governed boundary may be a separately authorized minimal runtime correction limited to the real AP0 manifest compatibility defect.

The frozen H1-01 → H1-21 breaker and RC01 must remain unchanged during that correction.

