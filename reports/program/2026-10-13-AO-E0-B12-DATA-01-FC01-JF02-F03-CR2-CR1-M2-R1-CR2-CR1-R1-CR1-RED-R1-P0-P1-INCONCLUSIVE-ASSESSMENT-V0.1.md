# R1-CR1-RED-R1 V0.1 — TEST-FIRST FORENSIC RECEIPT

## Terminal decision

```text
CONTROL_ID = AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1
USER_AUTHORITY = EXPLICITLY_AUTHORIZED_IN_CURRENT_CONVERSATION
R1_CR1_RED_R1 = INCONCLUSIVE
P0_REPOSITORY_PROTECTED_READINESS = PASS_WITH_QUALIFIED_DOCUMENTARY_DRIFT
P1_EXECUTION_POLICY = PERMITTED
P1_PYTEST_COLLECTION = PASS
P1_SYNTHETIC_OBSERVATION = 12_CASES_EXECUTED
P1_TEST_FIRST_RED = MIXED_NOT_FULLY_BEHAVIORALLY_QUALIFIED
P1_ASSERTIONS = 11_FAILED_1_PASSED
P2_GREEN = NOT_AUTHORIZED
WINDOWS_CAMPAIGN = FORBIDDEN
WORKER_LAUNCHES = 0
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP_AFTER_R1_CR1_RED_R1 = APPLIED
```

## P0 canonical identity and drift classification

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`, governed branch `integration/system-v1`.

Observed remote HEAD `cafa5b3887b9bbc0b03ee839f2b4b41097f41856`; TREE `e34d11b15cbe8c6b30cd9e59dc2e9084b896f5ea`. Local HEAD before documentary fast-forward: `3931de13d7976047c8fbe3716b403569c78e2c98`, TREE `a9de4bfe1380b3647fe2b8c79588d7fcd3d75742`. Their only changed path is the previous BLOCKED forensic report; it is non-material for P1. No tracked local changes or staged content existed before this attempt.

Protected blobs: FC01 `44ccaeafdd22cede207fef6038e5c747ff5d1454` and E1 `2dcacfde5fdf9b39ce0c9647c4413f2d2fc67a0b`.

Frozen test file `tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1.py`: SHA-256 `65cb60153e6a7458adce0373ad51d95e84c3c4fb84ca19e2843dceb8a8944282`; 12 function definitions JM-01..JM-12; no subprocess, worker spawn or network calls.

Test-only historical behavior adapter: `tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/member_evidence.py`; SHA-256 `6260021b5e1259677413c341587de92d71168e96ce2d2abc5b51446434fa2c85`. It maps synthetic inputs to the prior `forensic_contract.check_independent_tree` and `check_descendants` behavior. It is not a GREEN fix, not an independent Windows observation, and not production code.

## Execution/readiness restriction resolution

Initial normal pytest invocation ran with the Remote Desktop Commander's default working directory and failed during discovery: missing unrelated `Documents\Mes vidéos` path. This was `COLLECTION_ERROR`, not a RED result. The same standard pytest command executed successfully after setting the working directory to the ATDS project. This was not an evasion of a security denial; no subsequent tool execution was rejected.

Final capture was performed through normal `py -3.12 -m pytest` with `-p no:cacheprovider`, `--junitxml`, and no worker launches. Pytest exit code = `1` (expected for failing assertions); collection errors = `0`, tests run = `12`, failures = `11`, passes = `1`.

Raw test output:
`reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-P1-RAW-TEST-OUTPUT-V0.1.txt`
SHA-256: `ff894570b917f7ad5c0af88239878bf564200fe378a6933cc90bdf3b98538d3f`.

JUnit:
`reports/program/2026-10-13-AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-CR1-R1-CR1-RED-R1-P1-JUNIT-V0.1.xml`
SHA-256: `882783cf85c4ebb7f65e6ae24a6e00546fe11bef05c2584bf47d4db8da2b8589`.

## Individual case adjudication

| Test | Actual assertion result | Interpretation |
|---|---|---|
| JM-01 | PASS | Le worker principal unique est reconnu par le contrat historique. |
| JM-02 | RED_FAILED | Parenté vérifiée dans le fixture, mais le contrat historique bloque le deuxième membre faute de classification. |
| JM-03 | RED_FAILED | Le membre inconnu est refusé, mais sans le motif contractuel UNCLASSIFIED_JOB_MEMBER attendu. |
| JM-04 | RED_FAILED | L'identité de création invalide conduit à un refus, mais sous un motif historique différent. |
| JM-05 | RED_FAILED | Une identité de démarrage différente après terminaison est acceptée par le contrat historique synthétique. |
| JM-06 | RED_FAILED | L'affirmation d'absence contradictoire est bloquée, mais sans le motif spécifique attendu. |
| JM-07 | RED_FAILED | Le membre non terminé est bloqué, mais sans le motif spécifique attendu. |
| JM-08 | RED_FAILED | Un compteur de membres contradictoire est accepté par l'adaptateur historique. |
| JM-09 | RED_FAILED | L'absence est acceptée, mais le niveau et le libellé de preuve exigés ne sont pas produits. |
| JM-10 | RED_FAILED | Les membres parent/enfant du fixture ne sont pas classifiés comme descendant vérifié. |
| JM-11 | RED_FAILED | L'absence de provenance des observations brutes n'est pas refusée par le contrat historique synthétique. |
| JM-12 | RED_FAILED | Un membre distinct avec filiation extérieure vérifiée n'est pas classé : faux blocage. |

The 11 failing assertions **must not be interpreted as eleven distinct independently proven material defects**. JM-05, JM-08 and JM-11 exhibit synthetic acceptance of missing/mismatched evidence; JM-02, JM-10 and JM-12 show absent independent classification/false blocking; JM-03, JM-04, JM-06, JM-07 and JM-09 involve assertion/receipt-label differences where the historical contract already blocks or accepts part of the requested behavior.

Consequently this is an observed, reproducible, mixed RED baseline, **not fully behaviorally qualified across all twelve cases**. A separate human adjudication of test oracle semantics is needed before treating it as `PASS_RED_QUALIFIED` or authorizing implementation P2.

## Historical invariant and STOP

The old campaign `R1RECOVERY_20261011_CAMPAIGN_A` remains BLOCKED, 4/13 worker launches historically consumed, with immutable receipts. This attempt launched 0 workers, conducted no JForex login/provider call/real-data read/trading, and made no FC01/E1/M2 production changes.

```text
R1_CR1_RED_R1 = INCONCLUSIVE
P1_SYNTHETIC_RED = OBSERVED_MIXED
P1_FULL_BEHAVIORAL_QUALIFICATION = NOT_QUALIFIED
P2_IMPLEMENTATION = NOT_AUTHORIZED
P3_CAMPAIGN = NOT_AUTHORIZED
P4_WINDOWS_WORKERS = 0
M2_POLICY = HUMAN_ADOPTED
FC01_REAL_MEMORY_SAFETY = NOT_QUALIFIED
READ_A_RETRY = FALSE
READ_B = FALSE
B12 = CLOSED
HISTORY_REWRITE = FALSE
FORCE = FALSE
FAIL_CLOSED = TRUE
STOP = APPLIED
```
