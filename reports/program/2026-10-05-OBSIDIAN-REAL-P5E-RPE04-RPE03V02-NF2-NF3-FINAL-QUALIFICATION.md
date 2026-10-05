# RPE-04 — RPE-03 V0.2 REBIND + NF-2 + NF-3 — FINAL QUALIFICATION

Date: 2026-10-05

## Result

RPE04_REMOTE_OBSERVATION_ADAPTER
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

RPE-04 HUMAN ADOPTION
= PENDING

## Candidate closures

BF-1
= CLOSED_BY_EXACT_RPE03_V0.2_REBIND

NF-2
= CLOSED

NF-3
= CLOSED

NF-4
= CARRIED_TO_RPE-05

## Exact RPE-03 V0.2 rebind

Human-adopted RPE-03 V0.2 adoption commit:
f266121e6a65daa3bf19480412f1addd299b8172

Adoption blob:
73b5a951a2ed9ed42cb827b4fadc555fc3dd7a7d

Classifier blob:
5bbe455418fe1396ee5824379ad7450a1379cbba

Classifier raw SHA-256:
4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41

RPE-04 supplies only the governed absolute Git executable:
C:\Program Files\Git\cmd\git.exe

## NF-2 exact observed tip

The candidate no longer uses commit peeling to establish remote-tip authority.

The observed identity is taken from the exact isolated local observation ref without dereference.

The exact referenced object must itself be a commit.

Therefore:

REF -> commit C
=> C may become OBSERVED_REMOTE_TIP

REF -> annotated tag T -> commit C
=> T is not a commit
=> fail closed
=> C does not receive OBSERVED_REMOTE_TIP authority

## NF-3 full physical-domain containment

The candidate recursively checks the governed local bare observation domain and rejects filesystem indirection across authority-bearing and fetch-written surfaces.

The closure includes:
- repository root;
- objects;
- objects/info;
- objects/pack;
- refs;
- refs/rpe04;
- HEAD;
- config;
- packed-refs;
- objects/info/alternates;
- existing pack/index and loose-ref descendants.

Symlink, junction, reparse-point or equivalent indirection is blocked.

Uncontrolled alternates are blocked.

Material conditions are checked before fetch and rechecked after fetch before exact-tip acceptance and before RPE-03 classification.

## Final evidence

RPE-03 V0.2 rebind + NF-2 targeted:
5/5 PASS

NF-3 targeted:
7/7 PASS

Runtime-binding hardening:
5/5 PASS

NF-2/NF-3 mutation discrimination:
3/3 PASS

RPE-04 dedicated discovery:
55/55 PASS

RPE-03 final qualified protected surface:
59/59 PASS

RPE-02 protected regression:
51/51 PASS

RPE-01 protected regression:
46/46 PASS

P5-E protected regression:
67/67 PASS

Protected blob checks:
PASS

Detailed execution evidence:
reports/program/2026-10-05-OBSIDIAN-REAL-P5E-RPE04-RPE03V02-NF2-NF3-FINAL-TEST-EVIDENCE.md

## Final candidate identity

RPE-04 implementation Git blob:
e188414cd433f839d5efbe5d28840d7acf4938d5

RPE-04 implementation raw SHA-256:
1300e60a5cd353557cc16779a372979b436fcacfeb082435cd749987342d1638

Closure preregistration blob:
6f19ca7da0a791801f07b20d1645354666a6ffba

Closure preregistration schema blob:
ba35ddaa201e8bc11703a07efe794aaab2d3ab8c

## Protected predecessors

RPE-01 guard:
26f977961d72a062199d71ffd628d5a5cc047887

RPE-02 model:
31db5d944a25e54db81bd901a087cdc2039925ad

RPE-03 V0.1 historical classifier:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-03 V0.2 adopted classifier:
5bbe455418fe1396ee5824379ad7450a1379cbba

P5-E contract:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E synthetic model:
c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 runtime:
1825e53d195ba2a63b5b646a5b78eb77939b94b5

All remain exact.

## Claim boundary

This qualification is local-only.

It does not qualify:
- GitHub polling;
- production remote observation;
- real 60-second SLA;
- NF-4 failure-event handoff to RPE-02;
- RPE-05;
- RPE-06;
- REAL P5-E;
- promotion/publication;
- Vault/CURRENT;
- daemon, Scheduled Task, Windows Service or startup activation.

Next gate:
EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION
