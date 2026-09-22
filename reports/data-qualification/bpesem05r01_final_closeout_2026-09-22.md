# B-PE-SEM-05R-01 — FINAL CLOSEOUT

Date: 2026-09-22

Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch: integration/system-v1

## 1. Closed block

~~~text
B-PE-SEM-05R-01 —
PROVIDER-VERSIONED ARTIFACT
DOCUMENTARY RECOVERY
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

B-PE-SEM-05R-01 = CLOSED / BLOCKED

demonstrated final defects = 0
~~~

BLOCKED is substantive, not a package failure.

## 2. Starting authority

Starting checkpoint:

~~~text
18803a7463a9b9338e2fcee8dc4435447d90a113
checkpoint: select B-PE-SEM-05R-01 provider artifact recovery
~~~

B-PE-SEM-05 input remained:

~~~text
B-PE-SEM-05 = CLOSED / BLOCKED

package integrity = PASS
Lane S semantic authority = BLOCKED
target epoch = BLOCKED_UNRESOLVED_TARGET_EPOCH
~~~

Recovery route record:

~~~text
reports/data-qualification/
post_bpesem05_lane_s_blocked_authority_recovery_route_selection_2026-09-22.md

blob =
3a15319721970983fc49e5388f09ef97170108fe
~~~

## 3. Pre-acquisition freeze

Initial provider acquisition plan was persisted before artifact bytes were fetched:

~~~text
evidence/bpesem05r01/
provider_artifact_acquisition_plan_v0_1.json

commit =
584be15b7d266e1d67f8425cb525c21da3a29d37

blob =
e6e3c2a671ade38ec34f2dad03c02e2e20d06adc
~~~

Supplemental provider dependency acquisitions were separately frozen before their bytes were fetched:

~~~text
provider_artifact_acquisition_plan_v0_2.json
blob = 130f767ea4a470edbd604b8896a62354589f25b7

provider_artifact_acquisition_plan_v0_3.json
blob = 93067b75ecd2d5167b2efe4ebe39042fd3ba7bd8

provider_artifact_semantic_extraction_plan_v0_1.json
blob = b5dd1bfc3cbd217b7294407adf74855b2127a486
~~~

No market-data object coordinate was admitted.

## 4. Provider artifact acquisition

Provider channel:

~~~text
Dukascopy official Maven/public distribution
~~~

Acquired provider families:

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

Every acquired provider artifact used:
- exact Maven coordinate;
- official provider SHA-1 sidecar verification;
- computed SHA-256;
- POM SHA-1 verification;
- POM SHA-256 identity.

Provider artifact inventory:

~~~text
evidence/bpesem05r01/
provider_artifact_inventory_v0_1.json

blob =
a022e1c16b363477cec4de71a830dd1255992471

inventory seal =
5ea792ebbe779c6ae75627055404c6841bb85a7709749bbd2c3cd6fff8190ed5
~~~

Composite identity registry:

~~~text
evidence/bpesem05r01/
provider_artifact_identity_registry_composite_v0_1.json

blob =
aacc0b10e9f06d18119e318d4048a59caa53f77e

all exact identity checks =
PASS
~~~

## 5. Provider lineage

All acquired artifacts belong to one provider dependency lineage:

~~~text
LINEAGE-DUKASCOPY-OFFICIAL-MAVEN-DISTRIBUTION
~~~

Dependency chain:

~~~text
DDS2-jClient-JForex
→ DDS2-Charts
→ greed-common
→ msg
~~~

No provider dependency was counted as an independent source.

Lineage record:

~~~text
evidence/bpesem05r01/
artifact_lineage_resolution_v0_1.json

blob =
6c6285c2c37f643b2078a4e592e4603651fe829c
~~~

## 6. Relevant classes/resources

Composite resource inventory:

~~~text
evidence/bpesem05r01/
relevant_class_resource_inventory_composite_v0_1.json

blob =
c8916f5fd3dfcc0a33f2ab6313d9119d85a47076
~~~

Material provider classes/resources include:

~~~text
DataCacheUtils.class
DataCacheUtils$4.class
AbstractCurrencyConverter.class

CandleHistoryGroupMessage.class
DFHistoryStartRequestMessage.class
TickCacheDataRequestMessage.class
TickCacheDataResponseMessage.class
TickMessage.class
InstrumentSettings.class
~~~

Observed stable exact class hashes include:

~~~text
DataCacheUtils.class
337761c442e7d129095f69bbc1ac6cd71c18dc1ecf2a271f3a9169cd1bed951a

DataCacheUtils$4.class
013df7da4ef48abd90d6366953c309df1b6f589f9d035a734e7887b158f55d07

AbstractCurrencyConverter.class
2495e958ac7597302f088e34ea43eb6582e8fd365f70efda277107b5e56439c9
~~~

These three classes were byte-identical across all five selected greed-common versions.

Selected history/tick/settings message classes were byte-identical across:

~~~text
msg 1.1.98.2-JForex3
msg 1.1.98.4-JForex3
~~~

## 7. Recovery A

Target:

~~~text
exact immutable/provider-versioned
legacy-hourly K1 semantic authority
~~~

Finding:

~~~text
evidence/bpesem05r01/
legacy_hourly_semantic_artifact_finding_v0_1.json

blob =
43f6b95945b71e7beb70b2cd86a242e8a2e5a0cd
~~~

Exact provider facts recovered:

~~~text
DataCacheUtils defines:
VERSION_5_CACHE_FILE_EXTENSION = "bi5"

DataCacheUtils$4 explicitly recognizes:
_ticks.bi5
_ticks.bin
~~~

These findings are stable across the five inspected greed-common versions.

However the inspected provider artifacts did NOT expose exact authority for:

~~~text
compression/wrapper
20-byte native record width
five-field primitive layout
field roles
hour-relative timestamp semantics for target K1
native raw price divisor
volume encoding/roles
~~~

Therefore:

~~~text
Recovery A = AMBIGUOUS
~~~

Provider BI5 cache identity/usage was recovered, but exact public raw legacy-hourly payload semantics were not.

## 8. Recovery B

Target:

~~~text
exact provider-primary native BI5
USATECH raw scale/divisor authority
~~~

Finding:

~~~text
evidence/bpesem05r01/
usatech_raw_scale_artifact_finding_v0_1.json

blob =
fff29d789223dca2690d01b0918ee1527156e253
~~~

Provider facts recovered:

~~~text
Instrument.USATECHIDXUSD identity exists

provider API exposes pip/tick scale interfaces

InstrumentSettings exposes:
priceScale
pricePipValue

AbstractCurrencyConverter references USATECHIDXUSD
~~~

But no inspected provider artifact contained a static binding establishing the native BI5 raw integer divisor for USATECH.

The firewall remained:

~~~text
runtime/API priceScale
!=
native BI5 raw integer divisor authority
~~~

Third-party decimalFactor 1000 was not promoted to provider-primary evidence.

Therefore:

~~~text
Recovery B = NOT_FOUND
~~~

## 9. Recovery C

Target:

~~~text
exhaustive target-epoch
semantic change-point / continuity authority

2021-08-13T01:00:00Z
→
2026-08-14T20:00:00Z
~~~

Cross-version ledger:

~~~text
evidence/bpesem05r01/
cross_version_semantic_change_ledger_v0_1.json

blob =
9d1638b8391e259796e798c7fcfbfde4292ebc81
~~~

Provider release samples:

~~~text
DDS2 3.6.34
greed-common 318.4.115
msg 1.1.98.2-JForex3

DDS2 3.6.37
greed-common 318.4.118
msg 1.1.98.2-JForex3

DDS2 3.6.48
greed-common 318.4.125
msg 1.1.98.4-JForex3

DDS2 3.6.49
greed-common 318.4.127
msg 1.1.98.4-JForex3

DDS2 3.6.51
greed-common 318.4.128
msg 1.1.98.4-JForex3
~~~

Partial stability was recovered for selected client/cache/history/tick semantics.

But:

~~~text
public inspected DDS2 lineage ends in 2025

governed target ends 2026-08-14

2026 provider JETTA change has no matching inspected public DDS2 client artifact

client-side bytecode stability
!=
server/public raw-object semantic continuity
~~~

Therefore:

~~~text
Recovery C = INCOMPLETE_VERSION_COVERAGE
~~~

Full target semantic continuity remains unproven.

## 10. JETTA 2026-03-03

Finding:

~~~text
evidence/bpesem05r01/
jetta_change_impact_finding_v0_1.json

blob =
b83bb700ba9a4381dbc3d9b0a9253135d3f59ca7
~~~

Provider statement scope:

~~~text
JForex 4.8.0 historical price data retrieval from JETTA
~~~

Recovery observations:

~~~text
JETTA string found in acquired Maven artifacts = false

matching 2026 public DDS2 client artifact inspected = false

native K1 wire semantic effect = UNRESOLVED
~~~

The following were explicitly NOT inferred:

~~~text
NO_CHANGE_TO_K1
CHANGE_TO_K1
LEGACY_HOURLY_TO_DAILY_TRANSITION_DATE
~~~

JETTA remains:

~~~text
BLOCKED_UNRESOLVED_IMPACT
~~~

## 11. Documentary evidence horizon

Artifact:

~~~text
evidence/bpesem05r01/
documentary_evidence_horizon_v0_1.json

blob =
b9fb63bb9ecb729223fe4c40789d01ba321d62b1
~~~

Provider artifact families exhausted in this block:

~~~text
DDS2-jClient-JForex
JForex-API sources
DDS2-Charts
greed-common
msg
~~~

A generic dependency such as system-msg was not recursively followed because the inspected msg artifacts exposed no specific A/B/C semantic dependency requiring it.

Remaining authority gaps:

~~~text
exact provider binding of legacy-hourly K1 raw payload semantics

exact provider binding of USATECH native BI5 raw integer divisor

2026/JETTA and server-side/public-object semantic continuity through target end
~~~

Overall documentary horizon:

~~~text
BLOCKED
~~~

## 12. Candidate recovery package

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

Recovery package result:

~~~text
evidence/bpesem05r01/
recovery_package_result_v0_1.json

blob =
ab3ccfb4bdd7da1d93511b0d0523b70f974f2908

Recovery A = AMBIGUOUS
Recovery B = NOT_FOUND
Recovery C = INCOMPLETE_VERSION_COVERAGE

any full recovery = false

overall substantive result = BLOCKED
~~~

## 13. Adversarial break

Workflow:

~~~text
B-PE-SEM-05R-01 recovery package

run =
35759526546

job =
106853755887
~~~

Report:

~~~text
reports/data-qualification/
bpesem05r01_recovery_adversarial_break_2026-09-22.md

blob =
dce384f248153f4a7407bc1a3239f5e0f5d4e442
~~~

Result:

~~~text
breaker verdict = PASS
attack count = 30
demonstrated defects = 0
~~~

No correction of the candidate was justified.

The breaker specifically preserved:
- no overpromotion of provider BI5 cache identity;
- no /1000 plausibility inference;
- no false 2026 coverage;
- no JETTA stability/change inference;
- no Lane S self-readjudication;
- no Lane P authorization.

## 14. Final persisted-head re-break

Workflow:

~~~text
B-PE-SEM-05R-01 final rebreak

run =
35760024624

job =
106855452169
~~~

Final outputs persisted at:

~~~text
43fe21eb58a349a6a4e8ee66750307b1f8f79e87
audit: final re-break B-PE-SEM-05R-01 recovery
~~~

Qualification:

~~~text
evidence/bpesem05r01/
recovery_qualification_v0_1.json

blob =
cd260eb27ac31c0fc68dea4449923ac484544307

package integrity =
PASS

Recovery A =
AMBIGUOUS

Recovery B =
NOT_FOUND

Recovery C =
INCOMPLETE_VERSION_COVERAGE

any full recovery =
false

Lane S re-adjudication sufficient new authority =
false

Lane P authorized =
false

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

Final checks:

~~~text
candidate ancestor = PASS

full adversarial breaker =
PASS

attack count =
30

breaker defects =
0

post-candidate changed paths =
3

unresolved changed paths =
0

demonstrated final defects =
0
~~~

## 15. Market-data boundary

Attestation:

~~~text
evidence/bpesem05r01/
no_market_data_observation_attestation_v0_1.json

blob =
49430b7ae0994068988b842ac2583ab949e53321
~~~

Attested:

~~~text
provider software/documentary artifact acquisition = YES

provider BI5 market-data GET = NO
historical market-data object acquisition = NO
Lane P RequestManifest = NO
P-DIAG implementation = NO
physical semantic discrimination = NO
FULL_INTERVAL = NO
D materialization = NO
backtest = NO
~~~

## 16. Closure

~~~text
B-PE-SEM-05R-01 = CLOSED / BLOCKED

package integrity = PASS

A = AMBIGUOUS
B = NOT_FOUND
C = INCOMPLETE_VERSION_COVERAGE

new authority sufficient for Lane S re-adjudication = NO

Lane P = NOT AUTHORIZED
~~~

STOP.
