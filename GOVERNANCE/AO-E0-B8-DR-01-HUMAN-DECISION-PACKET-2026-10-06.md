# AO-E0-B8-DR-01 — HUMAN DECISION PACKET

STATUS =
QUALIFIED_CANDIDATE / HUMAN_DECISION_PENDING

FINAL_QUALIFICATION_DECISION_RULE =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

## Candidate identity

CANDIDATE =
7b08d0af9cb733be186ddc2f4fa6ca22768284fd

DECISION TABLE =
1126cf429dc064104bdfe0615cea0a96b95b540e

RUNTIME =
bcf4b8541a7c223ee52f990e6dee621e1d83baa9

TESTS =
952f9f4b97e626495608517ccdde734694aa3a5e

## Rule summary

SUPPORT requires:
- n >= 58927;
- valid/resolved inference;
- M05 99% percentile CI lower > 5.0;
- F2_S4 COST_ROBUSTNESS_PASS;
- no M07 material influence;
- no M07 sign reversal;
- no M08 material selection asymmetry;
- exact NEW_FORWARD_DATA_ONLY route;
- preserved B9 state CONTAMINATED / PARTIAL_SEARCH_UNIVERSE / n_trials=null.

SUPPORT maps to:
QUALIFIED
with mandatory provenance limitations.

REFUTE requires:
- all validity gates clean;
- M05 CI upper <= 5.0;
- F2_S4 COST_ROBUSTNESS_FAIL.

REFUTE maps to:
NOT_QUALIFIED / REFUTED.

Everything that blocks reliable interpretation without direct contrary evidence maps to:
INCONCLUSIVE
→ NOT_QUALIFIED
with exact reasons preserved.

## Multiplicity decision

PARTIAL_SEARCH_UNIVERSE is preserved as a mandatory limitation rather than erased or converted into an invented numerical correction.

The candidate never claims:
- pristine hypothesis origin;
- known n_trials;
- multiplicity-adjusted alpha.

## Qualification

INDEPENDENT LOCAL REPLAY =
22 / 22 PASS

NO NEW NUMERIC THRESHOLD =
PASS

NO FREE MATERIAL DECISION =
PASS

CANONICAL EXECUTABLE TESTS =
PERSISTED

CI PASS =
NOT CLAIMED

## Recommendation

RECOMMENDED HUMAN DECISION =
ADOPT EXACT DR-01 CANDIDATE

If adopted, the decision rule becomes prospectively binding and frozen.

That adoption still does NOT close B8 and does NOT open B12.

Only after separate adoption may AO-E0-B8-02 be separately authorized for rerun.

## Current authority

DR01_RULE =
NOT_HUMAN_ADOPTED

B8 =
BLOCKED

B12 =
CLOSED

AO-E0-B8-02 =
NOT_RERUN

AO_E0_EXECUTION =
NOT_AUTHORIZED

FORWARD_DATA_OBSERVATION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

FORCE =
FALSE
