# OBSIDIAN P5-C3R — STATIC REVIEW

Date: 2026-09-27

## Candidate reviewed

Branch:

    feat/obsidian-projection-p5c3r-access-denied-retry-v0.1

Reviewed HEAD:

    3605fe9330e68f40c2f0e5f12e78cba4f711f9d5

Failed predecessor:

    65003f36eef5bb8b4759d62735d7bf9f08e90ddb

## Delta

The candidate adds exactly eleven P5-C3R artifacts relative to the persisted P5-C3 failure closure:

- retry contract;
- retry implementation;
- retry CLI;
- contract tests;
- unit tests;
- adversarial breakers;
- recovery runner;
- open runner;
- post-close runner;
- protocol documentation;
- preflight report.

## Static checks

All reviewed checks passed:

    base P5-C3 harness byte-identical                   PASS
    retry contract blob pinned                         PASS
    retryable Windows codes exactly {5,32}             PASS
    write retry deadline/backoff bounded                PASS
    read retry deadline/backoff bounded                 PASS
    CURRENT.tmp written once before replace loop        PASS
    temp integrity checked after retryable failure      PASS
    recovery rebuild forbidden                          PASS
    recovery requires Obsidian closed                   PASS
    real Windows no-FILE_SHARE_DELETE breaker present   PASS
    synthetic breaker requires >0 sharing conflicts     PASS
    retry telemetry fields present                      PASS
    production authorization absent                     PASS
    governed CLI modes present                          PASS
    recovery runner ordering correct                    PASS
    open runner precheck precedes mutation               PASS
    open runner verifier/mode binding exact               PASS
    post-close manual acceptance required               PASS
    WinError 5 and 32 unit coverage present             PASS
    preflight identity pins current                     PASS

## Preserved failed implementation

The original P5-C3 open harness remains:

    tools/obsidian_projection/obsidian_open_compatibility.py
    blob:
    b970e65f21792cccc6ee2e4271d630f371102ff7

P5-C3R is implemented separately and does not silently rewrite the failed predecessor.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK, SYNTHETIC WINDOWS LOCK BREAKER AND RECOVERY REQUIRED**

No P5-C3R runtime qualification claim is made by this report.
