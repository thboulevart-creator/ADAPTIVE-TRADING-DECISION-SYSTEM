# COVERAGE ENVELOPE / EXECUTION WINDOW BOUNDARY — QUALIFICATION REPORT

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Objective

Determine whether later calendar qualification may continue while an earlier historical broker-evidence gap remains BLOCKED, without converting the global envelope to PASS, cherry-picking a future execution window, or authorizing massive acquisition.

## Formalized actions

The rule distinguishes four actions:

1. `CONTINUE_LATER_QUALIFICATION`
2. `DECLARE_GLOBAL_COVERAGE_PASS`
3. `FREEZE_EXECUTION_WINDOW`
4. `AUTHORIZE_MASSIVE_ACQUISITION`

PASS for one action is never inherited by another.

## Candidate rule

- Later qualification may continue if prior gaps remain durably preserved and unchanged.
- Global coverage remains BLOCKED until global unresolved count is zero.
- A future execution window may be admissible despite outside global gaps only if it is contiguous, >=5 calendar years, independently selected, versioned, fully enumerated, and has zero unresolved/FAIL dates inside it.
- Window shifting or date deletion to avoid known gaps is FAIL.
- Acquisition remains a separate gate and cannot be inferred from qualification continuation or window admissibility.

## Adversarial attacks

The executable tests attacked:

- continuing later qualification with 87 unresolved global dates;
- hiding/reclassifying a prior gap;
- false global PASS with unresolved dates;
- global FAIL contamination;
- an independently selected >=5-year window with an outside gap;
- explicit window shifting to avoid a known gap;
- missing independent selection rationale;
- unversioned rationale;
- unresolved/FAIL dates inside the window;
- manual deletion of a bad date inside an otherwise contiguous window;
- a sub-five-year window with perfect evidence;
- window freeze before candidate enumeration;
- acquisition before window freeze;
- misuse of `CONTINUE_LATER_QUALIFICATION = PASS` as acquisition permission;
- acquisition after window freeze but before mandatory gates;
- final acquisition route requiring every separate condition;
- unknown actions failing closed.

## Execution

Observed local execution of the versioned gate logic and adversarial test set:

```text
..................                                                       [100%]
18 passed in 0.05s
```

The execution environment used a local materialization of the versioned files with `PYTHONPATH` set to that materialization. This was not a GitHub Actions run.

## Adversarial result

No false-PASS path survived.

Most importantly:

- outside gaps do not automatically poison an independently selected future window;
- but a window selected or shifted because of a known gap is FAIL;
- unresolved inside the window is BLOCKED;
- a prior gap must remain visible globally;
- later qualification PASS does not authorize acquisition.

## Verdict

**PASS**

Reason:

`BOUNDARY_ACTIONS_SEPARATED_AND_ADVERSARIAL_BYPASSES_REJECTED`

This PASS certifies the governance boundary only. It does not certify global calendar completeness, a particular execution window, or acquisition readiness.
