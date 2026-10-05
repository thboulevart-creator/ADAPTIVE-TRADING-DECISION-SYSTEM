# ATDS — BEPD-00 — BEHAVIORAL EVIDENCE & PATTERN DISCOVERY
## CONDENSED DESIGN V0.1 — CANDIDATE

**Date:** 2026-10-05
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
**Governed branch:** `integration/system-v1`
**Status:** DESIGN_CANDIDATE / NOT_YET_HUMAN_ADOPTED
**Implementation authority:** NONE
**Real pattern-mining authority:** NONE
**Strategy / trading / capital authority:** NONE

## 1. Foundational question

> Parmi tout ce que les traders pensent voir sur les marchés, qu'est-ce qui se répète réellement, dans quelles conditions, avec quelle force, depuis combien de temps, et est-ce que le savoir avant l'événement suivant améliore réellement notre décision ?

For the first vertical slice:

> Pour chaque prise de liquidité sur un niveau H4, Daily ou Weekly précisément défini, construire la distribution empirique de la réaction post-sweep — amplitude, délai, MFE, MAE, continuation, retracement — puis mesurer comment cette distribution change selon le contexte et par rapport à un taux de base approprié.

Target capability:

> ATDS doit pouvoir répondre : quelles liquidités produisent historiquement une réaction, de combien, en combien de temps, avec quel risque adverse, dans quelles conditions, quelle information additionnelle cette prise de liquidité apporte réellement, et si cette relation est encore présente aujourd'hui.

## 2. Core architecture

```text
QUALIFIED MARKET DATA
        ↓
MARKET EVENT ONTOLOGY
        ↓
CAUSAL EVENT DETECTION
        ↓
EVENT INSTANCE LEDGER
        ↓
SEQUENCE REPRESENTATION
        ↓
POST-EVENT RESPONSE PROFILING
        ↓
CONTEXTUAL BASELINES
        ↓
BOUNDED PATTERN DISCOVERY
        ↓
SEARCH-PROVENANCE / MULTIPLICITY CONTROL
        ↓
TEMPORAL / REGIME STABILITY
        ↓
PROSPECTIVE INFORMATION-VALUE TEST
        ↓
PATTERN REGISTRY
        ↓
HYPOTHESIS GENERATION
        ↓
SEPARATE STRATEGY RESEARCH
```

## 3. Fundamental separations

```text
CONCEPT_NAME != FORMAL_EVENT_DEFINITION
EVENT_TIME != CAUSAL_AVAILABILITY_TIME
OBSERVED_EVENT != DESCRIPTIVE_RELATION
DESCRIPTIVE_RELATION != CANDIDATE_PATTERN
CANDIDATE_PATTERN != FORWARD_SUPPORTED_PATTERN
FORWARD_SUPPORTED_PATTERN != EDGE
EDGE != STRATEGY
STRATEGY != AUTHORIZED_ALGORITHM
RETROSPECTIVE_CLASSIFICATION != PROSPECTIVE_RECOGNITION
CONDITIONAL_FREQUENCY != CERTAIN_NEXT_EVENT_PROBABILITY
ASSOCIATION != CAUSATION
HISTORICAL_SUPPORT != CURRENT_VALIDITY
MULTIPLE_LABELS != MULTIPLE_INDEPENDENT_EVENTS
HIGH_CONDITIONAL_RATE != INCREMENTAL_INFORMATION
PATTERN_EXISTS != DECISION_VALUE
DISCOVERY_SUPPORT != PRISTINE_CONFIRMATION
BEPD_RESEARCH_RESULT != TRADING_AUTHORITY
```

## 4. Market-event ontology

The primitive vocabulary is strategy-agnostic and versioned. Candidate primitives include SWING_HIGH/LOW, REFERENCE_HIGH/LOW, LIQUIDITY_SWEEP, COMPRESSION, EXPANSION, BREAKOUT, REINTEGRATION, DISPLACEMENT, RETRACEMENT, REVERSAL, RANGE, GAP/REOPEN, VOLATILITY_STATE, DIVERGENCE, CROSS_ASSET_DIVERGENCE, SESSION_BOUNDARY and TIME_WINDOW.

The list is not normative or exhaustive. Each event definition must specify WHAT, WHEN, WHERE, MAGNITUDE, DURATION, SPEED where meaningful, CONTEXT, DATA REQUIREMENTS, VERSION and CAUSAL AVAILABILITY.

## 5. Multi-scale representation

Absolute values are preserved but are not sufficient alone. Candidate representations include raw distance, percent distance, backward volatility normalization, historical percentile, duration, velocity and acceleration.

Any normalization used prospectively must itself be computable from information available at the event's causal cutoff.

## 6. Event instance ledger

Each detected event must be reconstructible from immutable identities and should bind EVENT_ID, EVENT_DEFINITION_VERSION, ASSET, DATASET_IDENTITY, EVENT_TYPE, REFERENCE_TIMEFRAME, REFERENCE_LEVEL, REFERENCE_LEVEL_TYPE, EVENT_START, EVENT_CONFIRMATION_TIME, EVENT_CAUSAL_AVAILABILITY_TIME, DIRECTION, RAW_DISTANCE, NORMALIZED_DISTANCE, DURATION, VOLATILITY_CONTEXT, TIME_OF_DAY, WEEKDAY, SESSION, SEGMENT_ID, DATA_QUALITY_STATE and CONTEXT_SNAPSHOT_ID.

Event presence grants no strategy authority.

## 7. Causal availability firewall

Information may be used prospectively only once actually knowable. A previous closed H4 high is distinct from a confirmed H4 swing high. If a swing definition requires later bars, its known-time is later than its physical high-time.

All prospective research must use causal availability, never hindsight availability.

## 8. Event sequences

BEPD must support bounded event sequences such as COMPRESSION → LIQUIDITY_SWEEP → DISPLACEMENT → RETRACEMENT → EXPANSION and compare conditional response distributions such as P(Y|A), P(Y|A,B), P(Y|A,B,C).

Additional conditions are not assumed valuable merely because they increase apparent selectivity.

## 9. Human concept registry

Named concepts such as Macro Breaker, SMT divergence, RSI divergence, Power of Three or OTE enter initially as HUMAN_CONCEPT / HYPOTHESIS.

Each requires an exact versioned definition, measurable primitives, causal detection rules, parameter semantics, ambiguities and alternative definitions. Concept names are never authority.

## 10. Complexity decomposition

For a compound concept, BEPD should test whether the full concept adds information beyond simpler components.

```text
NO COMPLEXITY WITHOUT INCREMENTAL INFORMATION
```

A simpler representation is preferred when it preserves the relevant information.

## 11. Response profile

Post-event outputs are initially behavioral, not trading outcomes. Candidate measurements include FORWARD_DISPLACEMENT, MFE, MAE, TIME_TO_DISTANCE, MAX_CONTINUATION, MAX_RETRACEMENT, REINTEGRATION, REVERSAL, CONTINUATION, TIME_TO_MEAN and RESPONSE_DURATION.

Anchors, direction, horizon and start time must be defined before interpretation.

## 12. First vertical slice — liquidity sweep response

Initial reference levels:

```text
PREVIOUS_H4_HIGH / PREVIOUS_H4_LOW
PREVIOUS_DAILY_HIGH / PREVIOUS_DAILY_LOW
PREVIOUS_WEEKLY_HIGH / PREVIOUS_WEEKLY_LOW
```

Confirmed swing highs/lows are deferred because their confirmation semantics are more complex.

The initial empirical question is the post-sweep response distribution, not trade profitability.

## 13. Current data limitations

The qualified USTECH price-core currently does not qualify traded volume, market depth, order flow, sub-minute ordering universally, or execution-price realism.

Therefore unqualified volume/order-flow semantics remain UNKNOWN / NOT_QUALIFIED and may not be silently introduced.

## 14. Intrabar ambiguity

Minute data does not necessarily reveal the order of sweep, favorable movement and adverse movement occurring within one minute.

A minimal safe first implementation may detect the event in minute t and begin forward response measurement at t+1, unless finer data is separately qualified for the exact claim.

## 15. Response surfaces before TP claims

The primary output is a response surface/distribution such as P(reaction >= d | event, context), time-to-distance, MFE and MAE distributions.

It must not be silently rewritten as a TP win-rate or strategy claim.

## 16. Contextual baseline requirement

A conditional rate is informative only relative to an appropriate baseline.

```text
P(Y | EVENT, CONTEXT)
versus
P(Y | CONTEXT)
```

Known material context dimensions include, when applicable, New York time-of-day, weekday, backward volatility state and continuity/reopen state. Exact baseline semantics belong to the experiment contract.

## 17. Recent windows

Rolling windows such as the last 50 or 100 events may be useful for monitoring but must not be selected after outcome exposure.

An observed frequency such as 80/100 does not automatically imply an exact 80% probability for the next event. Uncertainty, dependence, overlap, regime mixture and temporal drift remain material.

## 18. Dependence and overlap

H4, Daily and Weekly labels may refer to one underlying market event. Overlapping forward windows may also induce dependence.

BEPD must distinguish multiple independent observations from one event possessing multiple properties and activate dependence-aware methods when required.

## 19. Discovery and confirmation

```text
DISCOVERY != CONFIRMATION
```

Discovery may explore a bounded recorded search universe and remains exploratory. Confirmation must not silently reuse contaminated discovery evidence as pristine confirmation.

The already-inspected USTECH corpus cannot be newly represented as pristine independent evidence for claims discovered on that corpus.

## 20. Search provenance and multiplicity

Every discovery process must retain search universe, available/tested features, interactions, outcomes, horizons, thresholds, candidate count, selection rule, discovery data and code identity.

Search-universe uncertainty remains explicit. Winner-only reporting is forbidden.

## 21. Conditional support and threshold stability

Higher apparent rates cannot compensate silently for vanishing sample size, evidence concentration or large uncertainty.

Relations should be examined as distributions/response surfaces and local sensitivity where possible. Confirmatory thresholds must be frozen before the evaluated result.

## 22. Epistemic states

```text
OBSERVED_EVENT
DESCRIPTIVE_RELATION
CANDIDATE_PATTERN
FORWARD_SUPPORTED_PATTERN
UNSTABLE_PATTERN
DEGRADED_PATTERN
REFUTED_PATTERN
```

These remain distinct from EDGE, STRATEGY and AUTHORIZED_ALGORITHM.

## 23. Descriptive, predictive and exploitable

```text
DESCRIPTIVE != PREDICTIVE != EXPLOITABLE
```

Predictive requires prospective incremental information relative to baseline. Exploitable additionally requires strategy, execution, cost, risk, robustness and OOS semantics under separate authority.

## 24. Prospective information value

The ultimate scientific question is whether information actually available at t improves a decision-relevant forecast for outcomes beginning after t, not whether a pattern can be recognized after completion.

## 25. Temporal drift and non-causality

Historical support and current validity remain separate. A relation may be historically supported and currently degraded simultaneously.

RTMA evidence cannot silently rewrite historical evidence or self-adjudicate scientific refutation.

Association and recurrence do not establish causal mechanism.

## 26. First research loop

Recommended future loop, under separate authority:

```text
USTECH
→ PREVIOUS CLOSED H4 / DAILY / WEEKLY HIGH/LOW
→ CAUSAL SWEEP DETECTION
→ POST-SWEEP RESPONSE DISTRIBUTION
→ PREDECLARED CONTEXTUAL BASELINE
→ UNCERTAINTY / DEPENDENCE
→ TEMPORAL STABILITY
→ NO STRATEGY CONCLUSION
```

Initial context dimensions may include reference timeframe, high/low, NY time-of-day, weekday, backward volatility state, continuity state and multi-level overlap.

SMT, Macro Breaker, RSI, broad indicator sets, traded volume and large interaction mining remain later extensions.

## 27. Valid negative result

```text
NO INCREMENTAL INFORMATION FOUND
```

is a scientifically valid result. The system must not respond by searching variants until a favorable pattern appears.

## 28. Inheritance and authority

BEPD inherits and must not override applicable DATA, temporal, SMF, MCEPR, RTMA, RVO, execution and governance owner boundaries.

The current Context/Regime V0.1 forbids interaction search and feature-subset search. BEPD pattern discovery therefore requires a distinct governed research contract or explicit extension; it may not execute silently under CR V0.1 authority.

## 29. Scope

This V0.1 is semantic/architectural design only. It does not authorize implementation, real historical pattern mining, OOS consumption, strategy research, backtest, PnL, paper, broker, live, capital or automatic scientific promotion.

## 30. Success criterion

The first vertical slice succeeds if ATDS can reproducibly answer, for a precisely defined liquidity-sweep class:

- what post-event response distribution was observed;
- how it differs from an appropriate contextual baseline;
- what uncertainty and dependence apply;
- whether the relation is temporally stable;
- whether the defining information was actually available before the measured response.

No profitability result is required for scientific success.
