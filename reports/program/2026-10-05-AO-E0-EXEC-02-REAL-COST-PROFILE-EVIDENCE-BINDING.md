# AO-E0-EXEC-02 — REAL COST PROFILE EVIDENCE BINDING

## Verdict

```text
REAL_COST_PROFILE =
BLOCKED

BLOCKER =
BLOCKED_BY_HUMAN_DECISION

OOS_CONSUMPTION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

B12 =
CLOSED
```

## Canonical finding

The governed research dataset is identified as:

```text
SOURCE_B_USTECH_PRICE_CORE_V0_1
USTECH / Nasdaq 100 Index CFD
publisher dataset = CarlosSilva1/ustech-ticks
publisher provenance = Dukascopy via Tickstory
```

The canonical provenance report explicitly does **not** establish:
- native Dukascopy tick-for-tick equivalence;
- an exact third-party broker symbol identity;
- VT Markets NAS100 feed/price equivalence.

Therefore Source-B cannot be promoted into an execution venue or broker-cost identity.

## External evidence

Current public evidence is consistent with multiple materially different execution profiles.

Dukascopy currently lists `USATECH.IDX/USD` as its US 100 Tech Index CFD, but current product availability does not prove that Source-B is the native Dukascopy feed, nor does it prove an exact historical account/cost profile over the full OOS.

VT Markets currently exposes multiple account structures, including Standard STP and Raw ECN, with different commission and swap semantics. Its current NAS100 guidance tells the trader to verify exact contract specifications inside the trading platform and labels worked specification figures as illustrative.

Therefore current public pages do not uniquely determine:

```text
VENUE
×
ACCOUNT PROFILE
×
SYMBOL CONTRACT
×
HISTORICAL EFFECTIVE PERIOD
```

for AO-E0.

## Binding matrix

```text
EXECUTION_VENUE_IDENTITY =
UNKNOWN_NOT_GOVERNED

ACCOUNT_COST_PROFILE_IDENTITY =
UNKNOWN_NOT_GOVERNED

USTECH_SYMBOL_CONTRACT_IDENTITY =
UNKNOWN_NOT_GOVERNED

COMMISSION_SCHEDULE_IDENTITY =
UNKNOWN

SLIPPAGE_BOUND_IDENTITY =
UNKNOWN

FINANCING_OR_SWAP_SCHEDULE_IDENTITY =
UNKNOWN

FULL_OOS_COST_SCHEDULE_COVERAGE =
NOT_ESTABLISHED

UNIT_CONVERSION_IDENTITY =
UNKNOWN
```

Spread remains the sole already-bound cost component through E1-04 raw BID/ASK execution and must not be counted again.

## Why the phase stops here

Choosing Dukascopy merely because the publisher says “Dukascopy via Tickstory” would violate:

```text
PUBLISHER PROVENANCE
!=
NATIVE FEED IDENTITY
!=
EXECUTION VENUE IDENTITY
```

Choosing VT Markets because an earlier comparison mentioned `VT Markets NAS100` would violate:

```text
BROKER COMPARISON REFERENCE
!=
HUMAN-ADOPTED VENUE
```

Choosing Standard STP, Raw ECN, swap-free, a currency, or a NAS100 contract variant would also be a new human normative decision.

## Human decision now required

Before EXEC-02 can continue, the governed AO-E0 target must bind exactly:

1. execution venue / broker;
2. account type or exact account-cost profile;
3. exact tradable USTECH/NAS100 symbol/contract.

No account number, login, credential, or secret is required.

Once those three identities are fixed, EXEC-02 can resume and attempt to establish the historical commission, financing/swap, slippage bound, effective-date coverage and unit conversion.

If those historical documents cannot then be established from admissible sources:

```text
BLOCKED_BY_MISSING_EXTERNAL_EVIDENCE
```

must replace any invented cost assumption.

## Preserved invariants

```text
MISSING COST != ZERO
UNKNOWN != ZERO
UNKNOWN != PASS
CURRENT TERMS != HISTORICAL TERMS
PUBLISHER PROVENANCE != VENUE IDENTITY
GENERIC BROKER TERMS != EXACT ACCOUNT TERMS
COST PROFILE QUALIFICATION != STRATEGY QUALIFICATION
COST PROFILE QUALIFICATION != OOS AUTHORITY
```

`STOP = AO-E0-EXEC-02 FAIL-CLOSED BLOCKER IDENTIFIED`