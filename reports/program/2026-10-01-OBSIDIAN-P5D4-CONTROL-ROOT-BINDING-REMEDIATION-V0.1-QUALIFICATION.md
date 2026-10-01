# P5-D4 — REAL CONTROL ROOT / INTERPRETER BINDING REMEDIATION V0.1 — QUALIFICATION

Date: 2026-10-01

## Verdict

```
P5D4_CONTROL_ROOT_PREREGISTRATION          = PASS
P5D4_CONTROL_ROOT_RED_TEST_FIRST           = PASS
P5D4_CANONICAL_PHYSICAL_ROOT_BINDING       = PASS
P5D4_LOCALAPPDATA_VIRTUALIZATION_CLOSED    = PASS
P5D4_STORE_NATIVE_POWERSHELL_CONVERGENCE   = PASS
P5D4_CROSS_INTERPRETER_LOCK_VISIBILITY     = PASS
P5D4_CROSS_INTERPRETER_SECOND_RUNNER_BLOCK = PASS
P5D4_RESTART_INTERPRETER_CHANGE            = PASS
P5D4_REPARSE_JUNCTION_GUARD                = PASS
P5D4_TARGETED_REGRESSION                    = 332 / 332 PASS
FULL_OBSIDIAN_REBREAK                       = 1424 / 1424 PASS

P5-D4 CONTROL ROOT BINDING REMEDIATION V0.1
= QUALIFIED
```

No real P5-D4 bounded loop was executed by this remediation.
P5-E remains CLOSED.

## Source authority

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/obsidian-projection-p5d4-control-root-binding-remediation-v0.1`
- Base HEAD: `4e36165a289e51d0d7f2ab1a7bd098697bfeabe0`
- Blocked real-qualification report blob: `d28ec65c2a69515fb58a21482ec3887eee2a3e72`
- Pre-remediation runtime blob: `b41c6b5172dd8ffe01d49717f5d796e4b5ad8f90`

## Blocking finding closed

The previous real qualification proved that:

`%LOCALAPPDATA%\ATDS-OBSIDIAN-PROJECTION\P5D4`

did not bind to one physical namespace across interpreters.

The Microsoft Store Python redirected writes to its package LocalCache while native Python and PowerShell saw the logical LocalAppData path as absent.

That made cross-interpreter single-instance ownership unproven.
## Preregistration

Preregistration commit:

`aac97c95457cd86943f5110f396957fc30dfb50a`

Artifact:

`tools/obsidian_projection/p5d4_control_root_binding_remediation_contract_v0_1.json`

Blob:

`3f62c901d7e7ac466114780859075489c9163a29`

The preregistration froze the new canonical namespace as:

`%USERPROFILE%\ATDS-CONTROL\OBSIDIAN-PROJECTION\P5D4`

and explicitly forbade real P5-D4 control-state dependence on:
- `%LOCALAPPDATA%`;
- `%APPDATA%`;
- Microsoft Store `Packages\...\LocalCache`;
- relative roots;
- symlink/reparse/junction chains;
- roots intersecting the repository or real Vault.

OS-temp roots remain allowed for synthetic tests only.

A separate synthetic qualification namespace under:

`%USERPROFILE%\ATDS-CONTROL\_QUALIFICATION`

was used only for cross-interpreter qualification and was removed after testing.
## RED test-first

RED commit:

`d480e0b16eca69c8afbfeb1514a32ece7881054f`

RED test blob:

`a38a0542ab25970bff2b5aef8f5b734a292cbff8`

Initial result before remediation implementation:

```
Ran 13 tests
4 PASS
1 FAIL
8 ERROR
```

The failures/errors were caused by the intentionally missing binding primitive:
- `canonical_production_control_root()`;
- `resolve_and_validate_control_root()`;
- `ControlRootBindingError`.

The already-passing cross-interpreter filesystem tests showed that the selected USERPROFILE namespace itself was physically shared by the tested interpreters.

## Minimal remediation

Initial implementation commit:

`028df4f89318ca96fa145c819c4b16ee02e54b8e`

Initial remediated runtime blob:

`b64d6c4335283b710ae1de81c82a01ca632dad6a`

The runtime gained only the control-root binding surface:
- explicit canonical production root;
- absolute-path requirement;
- USERPROFILE anchor;
- LocalAppData/AppData rejection for production;
- Store LocalCache rejection;
- synthetic OS-temp qualification allowance;
- explicit USERPROFILE qualification namespace;
- reparse/symlink/junction-chain rejection;
- canonical path normalization;
- integration through the existing `_validate_control_root()` gate.

No P5-D2 state-machine, budget, queue, evaluation, reconciliation, or promotion semantics were changed.

Frozen RED after implementation:

```
13 / 13 PASS
```
## Adversarial cross-interpreter qualification

Adversarial test commit:

`38acdec7c065a9e00eb9fead2885cf0bfc9b7c1e`

Adversarial test blob:

`5613ba5afeb8adaba2165c5829f1f94a30cd9089`

Final adversarial result:

```
9 / 9 PASS
```

The qualification demonstrated:
- Store Python, native Python and PowerShell compute the same production root;
- the old LocalAppData root is rejected before mutation;
- historical Store-redirected evidence is rejected as operational authority and remains unchanged;
- a lock created by Store Python is externally visible to PowerShell;
- a lock held by Store Python blocks a native-Python bounded runner before adapters or control-state writes;
- a lock held by native Python blocks the Store-Python bounded runner before observation/evaluation;
- checkpoint/event-log data written through one interpreter is byte-identical and readable after interpreter change.

Interpreters explicitly exercised:

Microsoft Store Python 3.13 execution alias:
`C:\Users\Boulevart\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe`

Native Python 3.14.7:
`C:\Users\Boulevart\AppData\Local\Python\pythoncore-3.14-64\python.exe`

External filesystem verifier:
PowerShell.
## Bounded path-chain correction

The first complete P5-D4 regression found one static-surface conflict: the reparse-chain inspection used the literal construct `while True`.

This was not the P5-D4 loop runner, but P5-D4 already forbids that unbounded construct anywhere in its runtime surface.

The traversal was mechanically replaced with an explicit maximum depth of 512 ancestors.

Stabilization commit:

`cc9fa31dd67b39692d8c6b5c35d6f38b918858b8`

Final remediated runtime blob:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

Complete P5-D4 result after stabilization:

```
83 / 83 PASS
```

## Targeted predecessor regression

The targeted regression covered the P5-D4 contract/runtime/remediation surfaces and the directly affected P5-D1/P5-D2/P5-D3 observer/evaluator/handoff/publication contracts and runtimes.

Result:

```
Ran 332 tests in 110.879s
OK
```
## Final full Obsidian re-break

Exactly one full Obsidian re-break was executed after stabilization.

HEAD and remote HEAD:

`cc9fa31dd67b39692d8c6b5c35d6f38b918858b8`

Production control root before full re-break:

`ABSENT`

Result:

```
Ran 1424 tests in 267.986s
OK

FULL_SECONDS = 269.765
FULL_EXIT = 0
FULL_OBSIDIAN_REBREAK = PASS
```

Production control root after full re-break:

`ABSENT`

The historical sample.txt line-ending warning remained non-failing.

The frozen RED harness also emitted ResourceWarning messages from subprocess pipe handles. These were test-harness warnings only; they produced no failed test, no runtime authority expansion, and no persistent repository mutation.

Generated native-Python bytecode artifacts were mechanically removed before final worktree adjudication.

## Historical redirected evidence preservation

The blocked real-qualification artifacts remain preserved at the Microsoft Store redirected historical evidence location.

Their digests remain:

`observer-events.jsonl = b1344dd8b47c9e0dc61dfd17e68b964b769e861ec77b49ed24e8d415d8f619e2`

`observer-checkpoint.json = e7d2e0e2b0fd9c4fd68a8dd725aeb9779d27a0416d4206f7930a40073641dbf6`

`last-run.json = b0e793e527eb26a5c5c041a42efa15b5532b2f593b73b05dcd0b7fe2892275dd`

They remain historical evidence only and are not migrated or adopted as new production control-state authority.
## Final authority adjudication

```
P5D2_SEMANTIC_STATE_AUTHORITY        = UNCHANGED
BOUNDED_LOOP_SEMANTICS               = UNCHANGED
EVENT_BEFORE_CHECKPOINT              = UNCHANGED
HASH_CHAIN                           = UNCHANGED
ATOMIC_CHECKPOINT_REPLACE            = UNCHANGED
QUEUE_POLICY                         = UNCHANGED
RESTART_RECONCILIATION               = UNCHANGED
PROMOTION_AUTHORITY                  = CLOSED

CANONICAL_PRODUCTION_CONTROL_ROOT     = %USERPROFILE%\ATDS-CONTROL\OBSIDIAN-PROJECTION\P5D4
LOCALAPPDATA_PRODUCTION_ROOT          = FORBIDDEN
STORE_LOCALCACHE_PRODUCTION_ROOT      = FORBIDDEN
CROSS_INTERPRETER_LOCK_NAMESPACE     = QUALIFIED
PRODUCTION_ROOT_CREATED               = FALSE
REAL_P5D4_LOOP_EXECUTED               = FALSE
P5E_AUTHORITY                         = FALSE
P6_AUTHORITY                          = FALSE
```

## Mandatory stop and next frontier

The remediation is qualified.

The next governed frontier is:

`P5-D4 — REAL BOUNDED LOOP REQUALIFICATION V0.2`

That requalification must use the new canonical production control root and must be separately authorized.

No real P5-D4 bounded loop is authorized by this report.

P5-E remains CLOSED until the real bounded-loop requalification passes.
