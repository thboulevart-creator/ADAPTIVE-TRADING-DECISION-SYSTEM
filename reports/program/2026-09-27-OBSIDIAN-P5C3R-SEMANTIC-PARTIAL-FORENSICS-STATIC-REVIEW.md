# OBSIDIAN P5-C3R — SEMANTIC PARTIAL FORENSICS STATIC REVIEW

Date: 2026-09-27

## Review status

This is a static review by the same assistant that produced the forensic delta.

It is not an independent review and it is not runtime evidence.

## Candidate reviewed

Branch:

    feat/obsidian-projection-p5c3r-semantic-partial-forensics-v0.1

Reviewed HEAD:

    7b28af0df36e7a0079f3f31c69d33960e59b0c72

Source failed runtime candidate:

    ae7d1adbb146fffb60c4e302750abb896136d968

## Scope reviewed

The delta from the failure checkpoint was reviewed for:

- retry-policy changes;
- atomic-publication changes;
- qualification-criterion changes;
- telemetry-only intent;
- bounded signature contents;
- mutable-default hazards;
- forensic accounting;
- breaker coverage;
- base-harness preservation;
- runner preservation.

## Findings

    retryable WinErrors remain exactly {5,32}                PASS
    write retry policy unchanged                            PASS
    reader retry policy unchanged                           PASS
    os.replace publication primitive unchanged              PASS
    CURRENT.tmp write-once semantics unchanged              PASS
    semantic partial still forces semantic_zero false       PASS
    PASS criterion still requires semantic count == 0       PASS
    forensic signature records top-level message            PASS
    forensic signature records immediate cause type         PASS
    forensic signature records errno                        PASS
    forensic signature records winerror                     PASS
    signature map uses dataclass default_factory            PASS
    reader increments semantic count before attribution     PASS
    signature total is separately reported                  PASS
    unit fixture for FileNotFoundError attribution present  PASS
    unit fixture for unrelated WinError attribution present PASS
    reader accounting breaker present                       PASS
    adversarial non-relaxation breaker present              PASS
    retry contract blob unchanged                           PASS
    open runner blob unchanged                              PASS
    base P5-C3 harness blob unchanged                       PASS
    production authorization remains false                  PASS
    continuous observer authorization remains false         PASS

## Exact important blobs

    forensic implementation
    318eea1608cdd1f0d54d24903314c4ed2e105ddd

    forensic unit tests
    b4eae74f0f72cf26126a7c16d8c06cfe557d6455

    forensic adversarial breakers
    9969b50cc63f961deec78477f5345e28a69f9577

    retry contract
    82cc7e100017d5e2db671ccce989f5e0e2afe912

    open runner
    ea6dc7d45d98df9507db4015d4e15b76fbc1fd52

    base P5-C3 harness
    b970e65f21792cccc6ee2e4271d630f371102ff7

## Important limitation

No local Python test, Windows sharing-lock breaker, Obsidian-open execution, or full suite was executed by this static review.

Those remain required local evidence.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK REQUIRED BEFORE ANY FORENSIC RUN-OPEN.**

The prior P5-C3R failure remains authoritative.

No retry expansion has been authorized.
No P5-C3R qualification claim is made.
