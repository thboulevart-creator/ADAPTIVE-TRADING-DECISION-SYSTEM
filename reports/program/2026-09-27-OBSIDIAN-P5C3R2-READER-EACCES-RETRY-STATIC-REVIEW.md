# OBSIDIAN P5-C3R2 — READER-ONLY EACCES RETRY STATIC REVIEW

Date: 2026-09-27

## Review status

This review was performed by the same assistant that produced the P5-C3R2 candidate.

It is not independent validation.
It is not local runtime evidence.
It does not replace the required Windows re-break.

## Candidate reviewed

Branch:

    feat/obsidian-projection-p5c3r2-reader-eacces-retry-v0.1

Reviewed HEAD:

    41b21fc3850eb94e1cd638f05fd04ccdf6797ab6

## Static findings

    V0.2 contract schema pinned                            PASS
    V0.2 contract blob pinned by implementation            PASS
    write retry remains PermissionError WinError {5,32}    PASS
    write path contains no errno.EACCES fallback           PASS
    reader fallback requires PermissionError               PASS
    reader fallback accepts WinError 5                     PASS
    reader fallback accepts WinError 32                    PASS
    reader fallback accepts winerror=None + EACCES only    PASS
    non-PermissionError EACCES breaker present             PASS
    non-retryable WinError + errno EACCES breaker present  PASS
    unrelated PermissionError errno breaker present        PASS
    permanent reader EACCES deadline breaker present       PASS
    reader deadline remains 500 ms                         PASS
    semantic partial still forces FAIL                     PASS
    mixed generation still forces FAIL                     PASS
    missing entrypoint still forces FAIL                   PASS
    parse error still forces FAIL                          PASS
    reader terminal access error still forces FAIL         PASS
    promotion count remains 250                            PASS
    minimum reader samples remain 5000                     PASS
    new EACCES telemetry present                           PASS
    semantic forensic telemetry retained                   PASS
    P5-C3R2 metrics schema separated                       PASS
    P5-C3R2 lock-breaker schema separated                  PASS
    P5-C3R2 post-close schema separated                    PASS
    P5-C3R2 event-log namespace separated                  PASS
    dedicated P5-C3R2 CLI present                          PASS
    P5-C3R2 CLI exposes no recovery mode                   PASS
    dedicated P5-C3R2 open runner present                  PASS
    dedicated P5-C3R2 post-close runner present            PASS
    P5-C3R predecessor open runner unchanged               PASS
    P5-C3R predecessor post-close runner unchanged         PASS
    base P5-C3 harness unchanged                           PASS
    successor no-launch/no-git-mutation breakers present   PASS
    post-close keeps p5c3r_qualified false                PASS
    post-close can mark p5c3r2_qualified true only         PASS
    production promotion remains false                     PASS
    continuous observer remains false                      PASS
    Graph/Search authority remains unqualified             PASS

## Exact core blobs

Contract V0.2:

    a3fb7736f2c25f144b1d9bc4a50cbf4029e3dc33

Implementation:

    df1a6988c5ce09d52941793a98f2a88728aaed41

P5-C3R2 CLI:

    1290ad909b7e78251fedd13303e87832833d487c

P5-C3R2 open runner:

    125022e1e9c367d83bbc9d3394b73c5d1a585dd2

P5-C3R2 post-close runner:

    0ce328c326e2b13774d9a2e71101f85cefdecfaf

V0.2 contract tests:

    3757cb311be2b778d6f52f3c8db7781ab0bed2dd

Unit tests:

    633b15ddff45b720696faea8244f759db7ede0ab

Adversarial tests:

    44413620e0068a094c588c9a939bbd74f0f3c9bf

Base P5-C3 harness:

    b970e65f21792cccc6ee2e4271d630f371102ff7

P5-C3R predecessor open runner:

    ea6dc7d45d98df9507db4015d4e15b76fbc1fd52

P5-C3R predecessor post-close runner:

    1409ed062e7a1546ad0d7afa42168d8c47312840

## Important limitation

No Python tests, PowerShell runner, Windows synthetic lock breaker, or Obsidian-open experiment was executed by this static review.

Those results remain NOT YET PERFORMED for P5-C3R2.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK REQUIRED BEFORE ANY P5-C3R2 OPEN RUN.**

The predecessor P5-C3R failure remains authoritative.
No identical P5-C3R rerun is authorized.
No production promotion is authorized.
No continuous observer is authorized.
