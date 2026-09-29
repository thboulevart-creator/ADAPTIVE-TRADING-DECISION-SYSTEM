# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT — DOWNSTREAM DEPENDENCY-PIN REQUALIFICATION V0.1 — QUALIFICATION

Date: 2026-09-29

## Evidence status

VERIFIED LOCAL EXECUTION plus VERIFIED GITHUB state.

## Authorized frontier

`P5-D3G — PRODUCTION ENABLEMENT — DOWNSTREAM DEPENDENCY-PIN REQUALIFICATION V0.1`

The governed scope was limited to the stale tooling-identity dependency between `production_enablement.py` and the requalified P5-D3G live-publication runtime.

No real P5-D3F handoff execution, no real Vault access, no live publication, no CURRENT mutation, no PROMOTION_CONFIRMED, no Stage B, no P5-D4, and no P6 were authorized or executed.

## Source state

Source branch:

`feat/obsidian-projection-p5d3g-downstream-dependency-pin-requalification-v0.1`

Source HEAD:

`c5d4ae4f70e3d1f3b246bd9125ffbc072e176a26`

Requalified P5-D3G live-publication blob:

`2fb34e1c04b4dd32d19b85b488d89f8a702204d0`

Historical production-enablement live-publication pin:

`b8875f8973ddf1076ff20d8e725ce04abbb814a8`
## Requalification artifacts

Working branch:

`feat/obsidian-projection-p5d3g-production-enablement-dependency-pin-requalification-v0.1`

Amendment contract blob:

`6f938414059b2bde425ea17febfbb77635fd91e5`

RED test blob:

`95b5c77c36b261c61b80a9e19ec95e5edcb00658`

Requalified production-enablement runtime blob:

`a9c0b46e5e623d765811d6d9b7766f172ca817a6`

The historical contract, historical production-enablement test, and historical production-enablement implementation re-break remained byte-exact:

- contract: `5de65f5d13a93d1325d53e1b58536ed0860921f2`
- test: `5a05ac5fccaf7032248f35f8fd2933d5943b100c`
- re-break: `1c126f27d7a48ec44cbfc6e7eafe056dd5a9cefb`

The historical symbol `QUALIFIED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB` remains bound to the original historical blob. A distinct effective binding now carries the requalified runtime identity.

## Test-first evidence

RED before implementation:

- amendment/preservation controls: 4 PASS
- missing effective runtime binding: ERROR
- missing amendment-contract runtime binding: ERROR

The RED therefore discriminated the intended missing surface before implementation.

After the minimal runtime change:

- production-enablement requalification tests: 6/6 PASS
- historical `test_p5d3g_production_enablement`: 17/17 PASS
- governed production-enablement requalification re-break: 41/41 PASS
- direct P5-D3G requalification + implementation class: 25/25 PASS
- P5-D3F persistent-verifier amendment targeted re-break: 85/85 PASS
## Full re-break

Full Obsidian suite:

`Ran 1310 tests in 168.123s`

`OK`

Observed terminal markers:

- `P5D3F_PERSISTENT_VERIFIER_AMENDMENT_TARGETED=PASS`
- `P5D3F_PERSISTENT_VERIFIER_AMENDMENT_FULL_REBREAK=PASS`
- `CONTROL_CLONE_CLEAN=PASS`
- `P5D3F_PERSISTENT_VERIFIER_AMENDMENT_REBREAK_COMPLETED=PASS`

No further downstream stale dependency was exposed by the full suite.

## Adjudication

`PRODUCTION_ENABLEMENT_DEPENDENCY_PIN_REQUALIFICATION = PASS`

`P5D3G_DIRECT_REQUALIFICATION = PASS`

`P5D3F_TARGETED_REBREAK = PASS`

`FULL_OBSIDIAN_REBREAK = PASS`

`NEW_DOWNSTREAM_STALE_DEPENDENCY = NONE_OBSERVED`

`REAL_P5D3F_EXECUTION = NOT_STARTED`

`P5D3F_ONE_SHOT_AUTHORIZATION = NOT_CONSUMED`

`LIVE_PUBLICATION = NOT_EXECUTED`

`STAGE_B = NOT_AUTHORIZED`

## Boundary after qualification

This qualification closes only the demonstrated dependency-pin propagation chain.

The next permitted action, under a separate still-valid human one-shot authorization, is a fresh P5-D3F real-handoff preflight. That preflight must reverify repository identity, branch/HEAD, qualified blobs, persistent staging prestate, fresh `integration/system-v1` remote identity, and all zero-real-Vault-mutation prerequisites before any real handoff execution begins.
