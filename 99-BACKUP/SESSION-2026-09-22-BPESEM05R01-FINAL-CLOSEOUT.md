# SESSION BACKUP — B-PE-SEM-05R-01 FINAL CLOSEOUT

Date: 2026-09-22

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch: integration/system-v1

## Closed block

~~~text
B-PE-SEM-05R-01 —
PROVIDER-VERSIONED ARTIFACT
DOCUMENTARY RECOVERY

= CLOSED / BLOCKED
~~~

Final governed result:

~~~text
package integrity = PASS

Recovery A = AMBIGUOUS
Recovery B = NOT_FOUND
Recovery C = INCOMPLETE_VERSION_COVERAGE

any full recovery = NO
Lane S re-adjudication sufficient new authority = NO
Lane P authorized = NO

demonstrated final defects = 0
~~~

## Starting checkpoint

~~~text
18803a7463a9b9338e2fcee8dc4435447d90a113
checkpoint: select B-PE-SEM-05R-01 provider artifact recovery
~~~

## Provider artifact recovery

Provider channel:

~~~text
Dukascopy official Maven/public distribution
~~~

Acquired/inspected provider families:

~~~text
DDS2-jClient-JForex
JForex-API sources
DDS2-Charts
greed-common
msg
~~~

Unique provider coordinates:

~~~text
19
~~~

Artifact inventory:

~~~text
evidence/bpesem05r01/
provider_artifact_inventory_v0_1.json

blob =
a022e1c16b363477cec4de71a830dd1255992471

inventory seal =
5ea792ebbe779c6ae75627055404c6841bb85a7709749bbd2c3cd6fff8190ed5
~~~

Every persisted evidence identity used exact provider coordinate, official SHA-1 verification and computed SHA-256.

All acquired artifacts belong to one provider lineage:

~~~text
LINEAGE-DUKASCOPY-OFFICIAL-MAVEN-DISTRIBUTION
~~~

No dependency was counted as independent evidence.

## Recovery A

Exact positive provider findings:

~~~text
DataCacheUtils:
VERSION_5_CACHE_FILE_EXTENSION = bi5

DataCacheUtils$4:
recognizes _ticks.bi5 and _ticks.bin
~~~

These relevant classes were byte-identical across the five selected greed-common versions.

But exact authority was not recovered for:

~~~text
compression/wrapper
20-byte record width
five-field primitive layout
field roles
hour-relative K1 timestamp semantics
raw price divisor
volume encoding/roles
~~~

Result:

~~~text
A = AMBIGUOUS
~~~

Finding:

~~~text
evidence/bpesem05r01/
legacy_hourly_semantic_artifact_finding_v0_1.json

blob =
43f6b95945b71e7beb70b2cd86a242e8a2e5a0cd
~~~

## Recovery B

Provider evidence recovered:

~~~text
Instrument.USATECHIDXUSD identity
pip/tick scale interfaces
InstrumentSettings.priceScale
InstrumentSettings.pricePipValue
USATECH reference in AbstractCurrencyConverter
~~~

No exact provider static native BI5 raw divisor binding was found.

No /1000 inference was made from runtime/API scale or third-party corroboration.

Result:

~~~text
B = NOT_FOUND
~~~

Finding:

~~~text
evidence/bpesem05r01/
usatech_raw_scale_artifact_finding_v0_1.json

blob =
fff29d789223dca2690d01b0918ee1527156e253
~~~

## Recovery C

Cross-version samples:

~~~text
DDS2 3.6.34 / greed-common 318.4.115 / msg 1.1.98.2-JForex3
DDS2 3.6.37 / greed-common 318.4.118 / msg 1.1.98.2-JForex3
DDS2 3.6.48 / greed-common 318.4.125 / msg 1.1.98.4-JForex3
DDS2 3.6.49 / greed-common 318.4.127 / msg 1.1.98.4-JForex3
DDS2 3.6.51 / greed-common 318.4.128 / msg 1.1.98.4-JForex3
~~~

Partial client/cache/history/tick stability was recovered.

But:

~~~text
public inspected DDS2 lineage ends in 2025

target ends 2026-08-14

2026-03-03 JETTA has no matching inspected public DDS2 client artifact

client-side stability != server/raw-object semantic continuity
~~~

Result:

~~~text
C = INCOMPLETE_VERSION_COVERAGE
~~~

Cross-version ledger:

~~~text
evidence/bpesem05r01/
cross_version_semantic_change_ledger_v0_1.json

blob =
9d1638b8391e259796e798c7fcfbfde4292ebc81
~~~

## JETTA

~~~text
event =
2026-03-03 JForex 4.8.0 historical-data retrieval from JETTA

native K1 wire semantic effect =
UNRESOLVED

matching 2026 public DDS2 artifact inspected =
NO

JETTA string in acquired Maven artifacts =
NO
~~~

Explicitly not inferred:

~~~text
NO_CHANGE_TO_K1
CHANGE_TO_K1
LEGACY_HOURLY_TO_DAILY_TRANSITION_DATE
~~~

Finding:

~~~text
evidence/bpesem05r01/
jetta_change_impact_finding_v0_1.json

blob =
b83bb700ba9a4381dbc3d9b0a9253135d3f59ca7
~~~

## Documentary horizon

~~~text
evidence/bpesem05r01/
documentary_evidence_horizon_v0_1.json

blob =
b9fb63bb9ecb729223fe4c40789d01ba321d62b1

overall status =
BLOCKED
~~~

Remaining gaps:

~~~text
exact provider legacy-hourly K1 raw-payload semantic binding

exact provider USATECH native BI5 raw divisor

2026/JETTA and server-side/public-object semantic continuity through target end
~~~

## Candidate / break

Candidate commit:

~~~text
b98a011e21f539c10d3064b30513efc9817bedf4
~~~

Candidate report:

~~~text
reports/data-qualification/
bpesem05r01_recovery_candidate_2026-09-22.md

blob =
4567f710b7af4b116e35e76569c01a4fb1c7ca08
~~~

Adversarial break:

~~~text
run =
35759526546

job =
106853755887

report blob =
dce384f248153f4a7407bc1a3239f5e0f5d4e442

verdict =
PASS

attack count =
30

defects =
0
~~~

No candidate correction was justified.

## Final persisted-head re-break

~~~text
run =
35760024624

job =
106855452169

final output commit =
43fe21eb58a349a6a4e8ee66750307b1f8f79e87
~~~

Qualification:

~~~text
evidence/bpesem05r01/
recovery_qualification_v0_1.json

blob =
cd260eb27ac31c0fc68dea4449923ac484544307

package integrity =
PASS

A =
AMBIGUOUS

B =
NOT_FOUND

C =
INCOMPLETE_VERSION_COVERAGE

overall governed result =
BLOCKED

qualification seal =
7ecc77a75c4bcf333edce03ec2a6504a8f0ded39fc49789d0556d7bd54f3866a
~~~

Final report:

~~~text
reports/data-qualification/
bpesem05r01_final_persisted_head_rebreak_2026-09-22.md

blob =
6f987953fdc275fddc241bd9ffb051c4024dff62
~~~

## Closeout

~~~text
reports/data-qualification/
bpesem05r01_final_closeout_2026-09-22.md

commit =
9fea4447e3b181ea1d8b30b9496e846bfbb63349

blob =
6a755acb75569a4f402b8c62c335cbaabed0f5d3
~~~

## Execution boundary

Performed:

~~~text
provider software/documentary artifact acquisition = YES
~~~

Not performed:

~~~text
provider BI5 market-data GET
historical market-data object acquisition
Lane P RequestManifest
P-DIAG implementation
physical semantic discrimination
B-PE-SEM-06
B-FIQ-02R
FULL_INTERVAL
D materialization
backtest
paper/broker/live
~~~

No new authority sufficient for Lane S re-adjudication was recovered.

STOP.
