# P5-D4 — REAL BOUNDED LOOP REQUALIFICATION V0.2

Date: 2026-10-01

## Verdict

```
P5D4_V02_PREREGISTRATION                    = PASS
P5D4_V02_FINAL_FAIL_CLOSED_PREFLIGHT        = PASS
P5D4_V02_REAL_INVOCATION_COUNT              = 1
P5D4_V02_REAL_REMOTE_OBSERVATION             = PASS
P5D4_V02_FAST_FORWARD_CLASSIFICATION         = PASS
P5D4_V02_PENDING_HEAD_QUEUE                  = PASS
P5D4_V02_EVALUATIONS_STARTED                 = 0
P5D4_V02_AUTOMATIC_PROMOTION_AUTHORITY       = FALSE
P5D4_V02_REAL_VAULT_MUTATION                 = FALSE
P5D4_V02_CANONICAL_PHYSICAL_ROOT_BINDING     = PASS
P5D4_V02_STORE_NATIVE_POWERSHELL_VISIBILITY  = PASS
P5D4_V02_LOCK_AND_TEMP_CLEANUP               = PASS
P5D4_V02_HISTORICAL_REDIRECT_EVIDENCE        = UNCHANGED

P5-D4 REAL BOUNDED LOOP REQUALIFICATION V0.2
= QUALIFIED

HUMAN_ADOPTION
= PENDING
```

P5-E and P6 remain CLOSED.

## Authority and scope

Human authorization covered exactly one governed P5-D4 real bounded-loop requalification using the qualified branch/runtime and the remediated canonical control root.

It did not authorize P5-E, P6, evaluation, promotion, real-Vault mutation, CURRENT/CURRENT.tmp mutation, Stage A, Stage B, daemonization, periodic polling, startup registration, Scheduled Task, or Windows Service.

Exactly one real invocation was executed.

## Qualified execution identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/obsidian-projection-p5d4-control-root-binding-remediation-v0.1`
- Qualified remediation base HEAD: `2d47dacf57a6da71f2ac3aef58ebdc22f69f491a`
- Qualified runtime blob: `1825e53d195ba2a63b5b646a5b78eb77939b94b5`
- P5-D2 observer blob: `fd212f61ec38332b677110f40265638af55a73e2`
- Control-root remediation report blob: `7c2e6e9f8f1a1a3ceb70b04e0d40d71b0857439e`

## V0.2 preregistration

Preregistration commit:

`16f001e7aaafa55fcba254a7bee16d1588ed90b0`

Artifact:

`tools/obsidian_projection/p5d4_real_bounded_loop_requalification_v0_2_preregistration.json`

Blob:

`635478c1d33101ccdaf4832e632509deab997829`

The preregistration fixed the real plan, exact source/current identities, prestate fingerprints, authority boundaries, expected FAST_FORWARD behavior, one-invocation limit, and fail-closed breakers before creation of the real production control root.

## Real preflight

Immediately before the real invocation:

- execution branch HEAD = remote execution branch HEAD = `16f001e7aaafa55fcba254a7bee16d1588ed90b0`;
- worktree = CLEAN;
- Obsidian process count = 0;
- canonical production control root = ABSENT;
- `CURRENT.md` SHA-256 = `867c639b164d9bd9a37bf0045c3181c6dde93aebfcf47f1a384bb4c3668107b9`;
- `CURRENT.tmp` = ABSENT;
- verified CURRENT candidate HEAD = `59f1dc26973b0b50efefccf12b26784d1e41f546`;
- remote `integration/system-v1` HEAD = `1d4c2f3d657b36ecaa6ab25b967e46b3620190d1`;
- remote tree = `bff033bf559d1e61995052be3876d20f0c47223d`;
- ancestry `59f1dc... -> 1d4c2f3...` = FAST_FORWARD.

The only commit between the live projection HEAD and the observed source HEAD was:

`1d4c2f3 governance: persist ATDS Architecture V2 human adoption`

## Verified publication evidence used for reconstruction

P5-D3G publication event log SHA-256:

`ad414d170626a0d238fc37161c4c04f54c660a17573d7f77607c0374045d7af2`

Publication plan digest:

`45e0c918825ce49bf5251b335d0653d17153dd62f35ae63e521f2a8f6dc2e10d`

Physical receipt digest:

`cbd2b3721e054883a5217f16ee64abfdab99f35608ea656b21ad3d3af94126c4`

Logical confirmation receipt digest:

`b6c29d9cc6c8a16e4132908cda93e9f2ce1ae5fd88da5d45c493ada126bbfed6`

## Real loop plan

```
loop_id = p5d4-real-requalification-v0.2-01
max_cycles = 2
max_remote_observations = 2
max_evaluations = 0
max_pending_heads = 1
max_consecutive_failures = 0
```

Plan digest:

`3cf5fdaf51da674eb4af090f7cff29dc07fa832109916c51cd9e8549c2379af1`

A synthetic preregistration preview produced the exact expected terminal shape before any real production control-state mutation.

`BOUND_REACHED` is an allowed P5-D4 terminal reason and is contractually a runner stop, not a P5-D2 semantic shutdown transition.

## Single real invocation result

The real invocation was executed under the Microsoft Store Python 3.13 execution alias, intentionally exercising the interpreter that exposed the V0.1 LocalAppData virtualization defect.

```
terminal_reason = BOUND_REACHED
cycles_started = 2
remote_observations = 1
evaluations_started = 0
consecutive_failures = 0
automatic_promotion_authorized = false
production_write_authorized = false
```

Final observer state:

- `last_qualified_head = 59f1dc26973b0b50efefccf12b26784d1e41f546`;
- `live_projection_head = 59f1dc26973b0b50efefccf12b26784d1e41f546`;
- `latest_observed_head = 1d4c2f3d657b36ecaa6ab25b967e46b3620190d1`;
- `pending_heads = [1d4c2f3d657b36ecaa6ab25b967e46b3620190d1]`;
- `projection_state = STALE`;
- `remote_freshness = KNOWN`;
- `last_event_sequence = 5`;
- `blocked_head = null`;
- `last_failure_code = null`.

The live event was classified `FAST_FORWARD` with P5-D2 reason:

`REMOTE_HEAD_FAST_FORWARD_QUEUED`

No evaluation adapter execution occurred.

## Event lineage and durable control state

The canonical control root is:

`C:\Users\Boulevart\ATDS-CONTROL\OBSIDIAN-PROJECTION\P5D4`

The event log contains exactly five records:

1. `REMOTE_HEAD_OBSERVED / INITIAL` — EVIDENCE_RECONSTRUCTION
2. `EVALUATION_STARTED` — EVIDENCE_RECONSTRUCTION
3. `EVALUATION_PASSED` — EVIDENCE_RECONSTRUCTION
4. `PROMOTION_CONFIRMED` — EVIDENCE_RECONSTRUCTION
5. `REMOTE_HEAD_OBSERVED / FAST_FORWARD` — LIVE_BOUNDED_LOOP

Durable control-state SHA-256 values:

- `observer-events.jsonl = 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af`
- `observer-checkpoint.json = c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4`
- `last-run.json = eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259`

No `ownership.lock`, `observer-checkpoint.tmp`, or `last-run.tmp` remained after the invocation.

## Physical binding requalification

After the Store-Python real write:

- PowerShell sees the canonical USERPROFILE root and all three durable artifacts;
- native Python 3.14.7 resolves the same canonical root and successfully validates/reads the same event log, checkpoint and last-run state;
- no new Store `LocalCache\\Local\\ATDS-CONTROL\\...` redirected root exists;
- the canonical root has normal Directory attributes and no observed reparse/junction attribute.

Therefore the former cross-interpreter production control-root blocker is closed in a real invocation, not only synthetically.

## Vault non-mutation proof

Before and after the single real invocation:

- Vault content tree excluding `.obsidian`: `1f9d192845950f3929714faa7a2f09fadad6a264aab3158ee22523951122ed9a` across 2210 files;
- `.obsidian` tree: `3d0b8704f662d5c1fe385ca15b99beca27f37c94b2284e392c2b0ba1ac98f7a9` across 5 files;
- current generation tree: `f6aee8f8e2dc1044946f0aae121c23b35d9887a3e7b2642753d29c03e15f22d3` across 2110 files;
- `CURRENT.md` SHA-256 remained `867c639b164d9bd9a37bf0045c3181c6dde93aebfcf47f1a384bb4c3668107b9`;
- `CURRENT.tmp` remained absent.

Real Vault mutation = FALSE.

## Historical redirected evidence preservation

The old Store-redirected V0.1 evidence remains unchanged:

- `observer-events.jsonl = b1344dd8b47c9e0dc61dfd17e68b964b769e861ec77b49ed24e8d415d8f619e2`
- `observer-checkpoint.json = e7d2e0e2b0fd9c4fd68a8dd725aeb9779d27a0416d4206f7930a40073641dbf6`
- `last-run.json = b0e793e527eb26a5c5c041a42efa15b5532b2f593b73b05dcd0b7fe2892275dd`

They remain historical evidence only.

## Adjudication

The V0.1 blocker was not loop logic; it was physical lock/control-state namespace divergence under Microsoft Store LocalAppData virtualization.

V0.2 exercised the remediated USERPROFILE namespace in a real Store-Python invocation and independently re-read the resulting physical state from native Python and PowerShell.

The real source was one FAST_FORWARD ahead of CURRENT. The bounded loop detected that exact head, durably queued it, changed the projection classification to STALE, and stopped at the preregistered evaluation budget of zero.

No evaluation, publication, promotion, Vault mutation, or authority expansion occurred.

```
P5D4_REAL_LOOP_BEHAVIOR              = PASS
P5D4_REAL_CONTROL_STATE_CONTENT      = PASS
P5D4_REAL_CONTROL_ROOT_BINDING       = PASS
P5D4_REAL_SINGLE_INSTANCE_NAMESPACE  = PASS
P5D4_REAL_VAULT_NON_MUTATION         = PASS
P5D4_REAL_REQUALIFICATION_V0_2       = QUALIFIED
```

## Residual state and mandatory stop

The exact observed source HEAD `1d4c2f3d657b36ecaa6ab25b967e46b3620190d1` remains durably queued and unevaluated by design.

No background process, polling loop, timer, Scheduled Task, Windows Service, evaluation, promotion, or publication has been started.

P5-E is now eligible for separate human consideration because the real P5-D4 bounded loop has been qualified, but P5-E is not opened or authorized by this report.

Mandatory stop after persistence of this qualification report.
