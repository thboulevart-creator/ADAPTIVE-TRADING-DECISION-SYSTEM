# RPE-04 — REAL REMOTE OBSERVATION ADAPTER V0.1 — RED

Date: 2026-10-04

## Frozen preregistration

- preregistration blob: `0416bc26222b48713014e503ee39abfbfd40326f`
- schema blob: `ca3e5205a6bd902991376ae77852a40b4a505aca`
- preregistration HEAD: `5fba272905793ca4ac86ac5ba9ceb2803adda8bc`
- RPE-01 guard validation: PASS

## RED test identity

`tests/obsidian_projection/test_rpe04_real_remote_observation_adapter_v0_1.py`

Worktree blob before persistence:

`eec1d9b39714b5e841438fc76180d851b6494bce`

## Observed RED result

```text
Ran 24 tests

2 PASS
22 FAIL

RED_EXIT = 1
```

The two passing tests validate the preregistration and its RPE-01 governed boundary.

All 22 functional adapter tests fail because the preregistered implementation file does not yet exist:

`tools/obsidian_projection/rpe04_real_remote_observation_adapter_v0_1.py`

This is the expected test-first RED state.

## Functional surfaces already frozen by the RED suite

The frozen suite covers:
- exact public interface without caller-supplied observed head/transition/containment authority;
- exact observed remote tip evidence;
- integer monotonic nanosecond timestamps;
- exactly one fetch transaction per attempt;
- FAST_FORWARD and NON_FAST_FORWARD derivation through RPE-03;
- contained-history non-laundering;
- missing remote ref and timeout fail-closed behavior;
- unexpected isolated-namespace refs;
- malformed and unmaterialized observed SHA;
- RPE-03 UNKNOWN propagation without positive laundering;
- local include.path/includeIf rejection;
- inherited/global/system Git authority neutralization;
- exact fetch argv protections;
- Git executable identity binding;
- physical object-domain acceptance and indirection rejection;
- no intermediate observed-tip injection.

No implementation exists at this RED checkpoint.
