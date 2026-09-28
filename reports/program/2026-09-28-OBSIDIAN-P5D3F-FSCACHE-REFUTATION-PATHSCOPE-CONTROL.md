# OBSIDIAN P5-D3F — FSCACHE REFUTATION AND PATHSCOPE CONTROL

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

Not independent execution evidence.

## Branch state before persistence

Verified remote HEAD:

    d75fa1ecaccf22610bda50dad9e3361004eee10a

## FSCACHE diagnostic

Representative path:

    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

Baseline with system Git configuration:

    1 .M N... 100644 100644 100644
    64744325251db350d26c0269090ce62d5fa5f2e8
    64744325251db350d26c0269090ce62d5fa5f2e8
    <path>

Process-local:

    -c core.fscache=false

produced the same .M classification.

git diff-files with core.fscache=false also continued to report the path modified.

Content identities remained equal:

    HEAD     = 64744325251db350d26c0269090ce62d5fa5f2e8
    INDEX    = 64744325251db350d26c0269090ce62d5fa5f2e8
    RAW      = 64744325251db350d26c0269090ce62d5fa5f2e8
    FILTERED = 64744325251db350d26c0269090ce62d5fa5f2e8

## Adjudication

    core.fscache=true AS SUFFICIENT CAUSE = REFUTED

No runner change is justified from this configuration setting.

## Experimental correction

A previously uncontrolled variable was identified:

- the real-index recovery attempt used:
      git update-index --really-refresh
  against the whole index;

- the temporary-index experiment that cleared the representative .M used:
      git update-index --really-refresh -- <representative-path>
  with a pathspec.

Therefore the prior inference "temporary index succeeds while real index fails" is not yet causally isolated.

## Next bounded test

Use two fresh temporary copies of the same real index:

A. whole-index:
       git update-index --really-refresh

B. representative-path only:
       git update-index --really-refresh -- <path>

For each copy:

- capture full staged mode/OID/stage snapshot before and after;
- record return code;
- observe representative path with --no-optional-locks status;
- leave the real index and worktree unchanged.

Only after this pathscope variable is isolated may the real-index-vs-temp-index distinction be evaluated.
