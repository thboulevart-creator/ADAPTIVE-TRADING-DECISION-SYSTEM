# OBSIDIAN P5-D3F — RUNNER RE-EXEC CORRECTION STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review.

Not independent execution evidence.
Does not qualify P5-D3F.

## Triggering local evidence

USER-REPORTED LOCAL EXECUTION established a bootstrap defect:

- process loaded from f4d8258...
- runner changed worktree to a12bc12...
- process continued with stale in-memory constants from the old runner.

This produced a false blob mismatch after checkout.

## Correction

Functional correction candidate:

    6ed8a755499c73b80eacfa0886fac6702d591d78

Runner blob:

    6e1d8980fcd41971de4ab61deb3b9f85ddd1ea7b

Runner-test blob:

    843f3b7d97fbe2750379709b777bc4eceac3e2e8

Contract blob unchanged:

    64744325251db350d26c0269090ce62d5fa5f2e8

Contract-test blob unchanged:

    3dc1d7315874d4352eeaf05407f266961c878e70

## Corrected runner semantics

The runner now:

1. verifies repository identity and clean worktree;
2. fetches the P5-D3F branch and enforces the remote race guard;
3. resolves the currently loaded HEAD;
4. if the loaded HEAD differs from the requested functional candidate:
   - detaches to the exact candidate;
   - verifies the switched HEAD;
   - verifies the runner file exists at the target;
   - emits P5D3F_REEXEC_AFTER_CHECKOUT=REQUIRED;
   - re-execs the current Python interpreter against the runner file from the new checkout;
5. guards re-exec with a one-shot environment counter;
6. only the freshly loaded target runner proceeds to blob checks and qualification.

Therefore qualification code and checked-out source are now the same revision before evidence-critical checks.

## Blob authority strengthening

The runner no longer uses working-tree git hash-object as its authority for contract/test identity.

It now resolves:

    git rev-parse HEAD:<path>

after requiring a clean worktree.

This binds checks to the committed Git object identity and removes checkout newline materialization from the authority decision.

## Added runner tests

The runner-test surface now includes explicit checks that:

- committed contract blob comes from Git authority;
- re-exec argv points to the runner at the target checkout;
- -B is preserved;
- original qualification arguments are preserved;
- repository root remains independent of shell cwd.

## Boundary preservation

No P5-D3F contract semantic changed.

No handoff runtime was implemented.

No real Vault write was introduced.

No CURRENT mutation was introduced.

No promotion authority was granted.

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL LOCAL CONTRACT RE-BREAK REQUIRED**

Next local candidate:

    6ed8a755499c73b80eacfa0886fac6702d591d78
