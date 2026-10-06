# BEPD-07B — FINAL HUMAN ADJUDICATION / CLOSURE — 2026-10-06

HUMAN_DECISION = ADOPT

BEPD-07B = HUMAN_ADOPTED
STATUS = QUALIFIED / HUMAN_ADOPTED / CLOSED
STOP = TRUE

## Binding identities

- Human authorization: `95a02c85b15f2d8e73bc4412ed6de4bf80888480`
- BEPD-07A final human adjudication: `5b8a8c9538363f8878acfa47c75db420438582be`
- BEPD-07A path/excursion contract: `d7b3aeed923a91e0e2aac530a952978c1f8fa5d6`
- BEPD-07A breaker: `42f2a720a0904c83c45a507cfa340af30ba73ae5`
- BEPD-07A pre-result freeze: `10fa2fc9011dded1567a054efb31fbabfa6dab8a`
- BEPD-07B corrective requalification receipt: `40228503c79798838f6dc2f6918b9aba00e15717`
- BEPD-07B corrected real execution freeze R1: `63b712c301f04496073251ad07055cf1786f956f`
- Corrected runner: `5b1108cc0fe703d9c45cfebc2ba12eb33c6552de`
- Corrected independent implementation: `27963b7ab2bea48d12bb3da584b430f2c047bb78`
- Canonical real result: `c78bc877f6b3af702ce6387b84331822027351ba`
- Run manifest: `abbc640481f9f0b4447fcef860c4a138a39f4819`
- Independent reference result: `db4e34dd9d134f02093aca287f240fb44af74199`
- Path/gap diagnostics: `8b14e129f4729d237120e7577f7d9dc09ad57906`
- Deterministic replay evidence: `c0197ea77b86e96c83f5c62504121d839dc224ed`
- Technical execution receipt: `8448fa23288dcea5442fed002f4c544903f6be27`
- Real result qualification receipt: `99bf4d9dba9dac10adba958e7be65ba23ad326eb`
- Real result qualification report: `07edd62f97c21c3fcab59b37de80821f192d1378`
- Persisted-head verification receipt: `be14458d994b58f099cf8ceca896c44d9896c786`

## Adopted result

The first real global historical distributions of `MAX_REINTEGRATIVE_EXCURSION` and `MAX_EXTERNAL_EXCURSION`, including their exact unbinned/unsmoothed ECDFs in the canonical result, are CANONICAL / HUMAN_ADOPTED.

Corrective lineage is accepted:
- initial pre-read attempt = FAIL_CLOSED before AP0 price-column read;
- no real excursion result from failed attempt;
- correction changed identity algorithm only;
- scientific semantics, path geometry, and excursion formulas unchanged;
- corrective qualification = 35/35 synthetic PASS and 40/40 breaker PASS.

AP0 provenance accepted:
- dataset = USTECH_PROFILE_MINUTE_CORE_V0_1;
- manifest SHA256 = 62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce;
- file count = 61;
- row count = 1709180;
- DATA-02 file-set digest = 1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a;
- all AP0 file SHA256 + size verified before price-column read.

Technical qualification remains PASS:
- base/path event count = 472;
- empty/filter/duplicate events = 0;
- no forward fill/interpolation/outcome-dependent endpoint;
- P50 = median for both;
- Hyndman-Fan Type 7 for both;
- ECDF terminal count = 472 and terminal fraction = 1 for both;
- independent recomputation = EXACT_PARITY_PASS;
- deterministic replay = EXACT_OBJECT_PARITY_PASS;
- persisted-head verification = PASS.

## Binding interpretation

- CANONICAL CLAIM = OBSERVED EXTREMA ONLY
- OBSERVED EXTREMA != TRUE CONTINUOUS-MARKET EXTREMA
- PRICE SURFACE = MID / DESCRIPTIVE_ONLY
- MID PRICE != EXECUTION PRICE
- BEHAVIORAL EXCURSION != TRADE EXCURSION
- MAX_REINTEGRATIVE_EXCURSION != TRADE PROFIT POTENTIAL
- MAX_EXTERNAL_EXCURSION != TRADE LOSS POTENTIAL

Scientific status:
- HISTORICAL CORPUS = ALREADY EXPOSED
- EVIDENCE STATUS = EXPOSED_EXPLORATORY_ONLY
- GENERALIZATION = NOT_ESTABLISHED
- CONFIRMATORY GENERALIZATION = FRESH_OOS_EVIDENCE_REQUIRED
- PREDICTION = NO
- CAUSATION = NOT ESTABLISHED
- EDGE = NO
- STRATEGY VALIDATION = NO
- TRADING AUTHORITY = NONE

## Boundaries preserved

No authority is granted for joint excursion metrics, MFE×MAE, ratios/differences/correlation, timing×excursion, close-displacement×excursion, HIGH/LOW or other subgroup analysis, survival analysis, Occurrence×Response, context ranking, positive-relation search, post-hoc thresholds, parameter optimization, OOS consumption, prediction, causation, edge, strategy validation, trade rules, TP/SL, PnL, trading authority, or capital deployment.

JOINT EXCURSION FRONTIER = NOT OPENED
SUBGROUP FRONTIER = NOT OPENED
TIMING × EXCURSION FRONTIER = NOT OPENED
OCCURRENCE × RESPONSE FRONTIER = NOT OPENED
OOS FRONTIER = NOT OPENED
NEXT SCIENTIFIC FRONTIER = NOT AUTOMATICALLY OPENED
NEW TRADING AUTHORITY = NONE

FINAL STATUS = QUALIFIED / HUMAN_ADOPTED / CLOSED
STOP.
