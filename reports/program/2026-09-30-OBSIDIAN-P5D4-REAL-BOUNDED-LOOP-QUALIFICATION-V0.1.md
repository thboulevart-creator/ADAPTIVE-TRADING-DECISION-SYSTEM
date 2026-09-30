# P5-D4 — REAL BOUNDED LOOP QUALIFICATION V0.1

Date: 2026-09-30

## Verdict

```
P5D4_REAL_LOOP_LOGIC                  = PASS
P5D4_REAL_BOOTSTRAP_RECONSTRUCTION    = PASS
P5D4_REAL_REMOTE_OBSERVATION          = PASS
P5D4_REAL_NO_EVALUATION_BOUNDARY      = PASS
P5D4_REAL_NO_PROMOTION_BOUNDARY       = PASS
P5D4_REAL_VAULT_NON_MUTATION          = PASS
P5D4_REAL_CONTROL_ROOT_LOGICAL_STATE  = PASS
P5D4_REAL_CONTROL_ROOT_PHYSICAL_BINDING = BLOCKED
P5D4_REAL_SINGLE_INSTANCE_CROSS_INTERPRETER = NOT_PROVEN

P5-D4 REAL BOUNDED LOOP QUALIFICATION V0.1
= BLOCKED
```

P5-D4 is not CLOSED/PASS.

P5-E remains CLOSED.

## Authorized runtime basis

- Runtime HEAD: `fdb4cb98ccd93b829fb491e80a90c795a8afa792`
- Runtime blob: `b41c6b5172dd8ffe01d49717f5d796e4b5ad8f90`
- Runtime qualification report blob: `14784ce96172c07007e78f8fb58c806136d1591e`
- Source branch: `integration/system-v1`
- Expected source HEAD: `59f1dc26973b0b50efefccf12b26784d1e41f546`
## Real preflight

The final read-only preflight passed before the real P5-D4 control mutation.

Verified:
- local runtime HEAD = remote runtime HEAD;
- worktree CLEAN;
- Obsidian process count = 0;
- source HEAD exact;
- CURRENT exact;
- CURRENT.tmp absent;
- physical P5-D3G generation verified;
- P5-D3G physical/logical receipt digests exact;
- P5-D4 control root absent before invocation.

CURRENT SHA-256:

`867c639b164d9bd9a37bf0045c3181c6dde93aebfcf47f1a384bb4c3668107b9`

Vault prestate tree digest:

`c068645d88578326fd9878b3e1dcbb50620b3a8e6739f9a1ecdc179b8daaf3c1`

.obsidian prestate tree digest:

`864fe0571aa4f3cb7535311db26a343a14bcfc0b998878df84540447620ce129`

P5-D3G physical receipt digest:

`cbd2b3721e054883a5217f16ee64abfdab99f35608ea656b21ad3d3af94126c4`

P5-D3G logical receipt digest:

`b6c29d9cc6c8a16e4132908cda93e9f2ce1ae5fd88da5d45c493ada126bbfed6`
## Real loop plan

The exact real plan was:

```
loop_id = p5d4-real-qualification-01
max_cycles = 2
max_remote_observations = 2
max_evaluations = 0
max_pending_heads = 1
max_consecutive_failures = 0
```

Canonical plan digest:

`a7790a620ec2b0f6814341bf1b2bc0f53d78bf9ad9a163a1856739e200e35edb`

Exactly one real loop invocation was executed.

No automatic second attempt was made.

## Real invocation result

```
terminal_reason = NO_PENDING_WORK
cycles_started = 1
remote_observations = 1
evaluations_started = 0
automatic_promotion_authorized = false
production_write_authorized = false
```

Final observer state:
- projection_state = CURRENT;
- observer_phase = IDLE;
- live_projection_head = `59f1dc26973b0b50efefccf12b26784d1e41f546`;
- latest_observed_head = same HEAD;
- last_qualified_head = same HEAD;
- pending_heads = [];
- last_event_sequence = 5;
- last_failure_code = null.

The real observation classified the source as:

`SAME`

with P5-D2 audit reason:

`REMOTE_HEAD_SAME`

No evaluation adapter execution occurred.
## Bootstrap evidence reconstruction

The event log contains exactly five semantic transitions:

1. `REMOTE_HEAD_OBSERVED / INITIAL`
2. `EVALUATION_STARTED`
3. `EVALUATION_PASSED`
4. `PROMOTION_CONFIRMED`
5. `REMOTE_HEAD_OBSERVED / SAME`

Origins:

```
1-4 = EVIDENCE_RECONSTRUCTION
5   = LIVE_BOUNDED_LOOP
```

The first four events reconstructed the existing verified P5-D3G publication via P5-D2 only. They did not execute a new evaluation or publication.

## Control-state integrity

Logical control-state postcheck passed.

Persisted control files:
- `observer-events.jsonl`
- `observer-checkpoint.json`
- `last-run.json`

No ownership lock remained.
No temporary control files remained.

Event log SHA-256:

`b1344dd8b47c9e0dc61dfd17e68b964b769e861ec77b49ed24e8d415d8f619e2`

Checkpoint SHA-256:

`e7d2e0e2b0fd9c4fd68a8dd725aeb9779d27a0416d4206f7930a40073641dbf6`

Last-run SHA-256:

`b0e793e527eb26a5c5c041a42efa15b5532b2f593b73b05dcd0b7fe2892275dd`

The event log was canonical, sequence-monotonic, and hash-chain consistent.
The checkpoint matched event sequence 5 and the final record digest.
## Vault and authority non-mutation

Post-run Vault tree digest:

`c068645d88578326fd9878b3e1dcbb50620b3a8e6739f9a1ecdc179b8daaf3c1`

This is byte-identical to the prestate digest.

Post-run .obsidian tree digest:

`864fe0571aa4f3cb7535311db26a343a14bcfc0b998878df84540447620ce129`

This is byte-identical to the prestate digest.

CURRENT SHA-256 remained:

`867c639b164d9bd9a37bf0045c3181c6dde93aebfcf47f1a384bb4c3668107b9`

CURRENT.tmp remained absent.

P5-D3G physical/logical receipt digests remained unchanged.

Repository HEAD remained:

`fdb4cb98ccd93b829fb491e80a90c795a8afa792`

Worktree remained CLEAN during the real invocation and adjudication before this report.

No Stage A, Stage B, P5-D3F, P5-D3G publication, Vault write, or promotion authority was invoked by the real loop.
## Blocking finding — Microsoft Store path virtualization

The authorized and contractually expected real control root was:

`C:\Users\Boulevart\AppData\Local\ATDS-OBSIDIAN-PROJECTION\P5D4`

The real invocation used the default `python` command, which resolves first to the Microsoft Store Python 3.13 execution alias.

Under that interpreter, Windows redirected writes physically to:

`C:\Users\Boulevart\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Local\ATDS-OBSIDIAN-PROJECTION\P5D4`

PowerShell reports the contract path as absent while the redirected physical path exists.

The redirected physical path contains the three valid P5-D4 control artifacts.

A second native Python installation also exists:

`C:\Users\Boulevart\AppData\Local\Python\pythoncore-3.14-64\python.exe`

Read-only visibility check under that native interpreter:

```
ALT_SEES_ALIAS = False
ALT_SEES_PHYSICAL_REDIRECT = True
```

Therefore the logical root string is not a single stable physical lock namespace across interpreters.

This is material to the P5-D4 single-instance guarantee. A process launched under a different Python interpreter could fail to observe the Microsoft Store redirected ownership path and could therefore operate in a distinct lock domain.

The real control-root physical binding required for production qualification is not proven.
## Qualification adjudication

The real bounded-loop logic itself behaved exactly as expected:

`CURRENT bootstrap -> real SAME observation -> NOOP -> NO_PENDING_WORK -> STOP`

However, P5-D4 real qualification includes durable control-state and single-instance ownership semantics, not only state-machine behavior.

Because the physical persistence/lock path is interpreter-dependent in the current environment, the real qualification cannot be declared PASS.

```
P5D4_REAL_LOOP_BEHAVIOR = PASS
P5D4_REAL_CONTROL_STATE_CONTENT = PASS
P5D4_REAL_CONTROL_ROOT_PATH = BLOCKED
P5D4_REAL_SINGLE_INSTANCE = BLOCKED
P5D4_REAL_QUALIFICATION = BLOCKED
```

## Mandatory stop

No second real P5-D4 invocation is authorized or performed.

The next governed frontier is:

`P5-D4 — REAL CONTROL ROOT / INTERPRETER BINDING REMEDIATION V0.1`

That frontier must establish one physically stable control/lock namespace across the interpreter used for real execution and external verification before another real bounded-loop qualification can be authorized.

P5-E remains closed.
