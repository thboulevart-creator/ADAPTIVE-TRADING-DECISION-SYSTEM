# E1-TD-03C-JF02-D3-F2-A1 — POST-F2 JFOREX PATH NECESSITY / VALUE-OF-INFORMATION ADJUDICATION V0.1

## Executive result

```
PRIMARY_OPTION =
OPTION_A_STOP_JFOREX_AS_AWS_SUBSTITUTE_NOW

ONE_MORE_FRESH_CACHE_HISTORY_ONLY_EXPERIMENT =
NOT_NECESSARY_NOW

DECISION_THEORETIC_VOI_FOR_CURRENT_AWS_SUBSTITUTE_DECISION =
ZERO

JFOREX_SECONDARY_VALIDATION_ROLE =
RETAIN_DORMANT_OPTIONAL_PATH

AWS_CRITICALITY =
UNCHANGED

AWS_PATH =
REMAINS_FROZEN_EXTERNAL_DEPENDENCY
```

The reason is stronger than "another test is unlikely to work." The reason is that **all four preregistered outcomes H1-H4 lead to the same governed decision for the AWS-substitute question**.

## 1. D1 → D2 → D3 → F1 → F2 synthesis

D1 proved that official Dukascopy historical data exist for the exact fixed interval: the Historical Data Export contained 22,985 BID tick rows, while the JForex `getTicks` attempt returned zero. The cross-interface discrepancy is therefore real, while the exact root cause remained unresolved.

D2 proved a zero-byte JForex cache chunk and the static disk-cache call path. Cache-state dependency became the strongest explanation, coupled with a possible transient provider history-service failure, but cache causality was not proven.

D3 was designed to execute the fresh-cache counterfactual, but failed during the connection phase before `startStrategy` and before `getTicks`. It therefore did not test cache causality.

F1 showed that the D3 terminal marker did not prove provider rejection; the original collector lacked enough state observability to distinguish transport/session initialization states.

F2 then demonstrated that the same SDK 3.6.51 / API 2.13.99 / DEMO stack could complete connection/session readiness well inside the original 30-second bound. This weakened a persistent/static connection failure and supported transience, but did not resolve the historical-data path itself.

## 2. Why H1 still does not justify the experiment

The strongest possible outcome is:

```
H1 = FRESH_CACHE_GETTICKS_RETURNS_NONZERO_TICKS
```

H1 would newly prove only that one fresh-cache JForex history attempt can return real ticks for the fixed interval.

It would **not** prove:

- repeat JForex byte identity;
- exact cross-interface parity;
- raw provider-object identity;
- BI5 object identity;
- S3 key/object identity;
- Source-B equivalence;
- AWS raw-object substitution.

The original JF02 contract itself requires repeat JForex byte identity and exact cross-interface parity for adoption. The existing D1 HDE artifact cannot satisfy that exact parity requirement because it is BID-only and its observed timestamps are second-precision while JForex targets millisecond ticks.

Thus a successful "one final" `getTicks` would not actually finish the JF02 qualification. It would create additional required work.

## 3. Counterfactual decision invariance

| Outcome | New information | AWS-substitute decision |
|---|---|---|
| H1 nonzero ticks | JForex operational once | STOP unchanged |
| H2 zero ticks | cache-only explanation weakened | STOP unchanged |
| H3 network timeout | recurrence of known failure class | STOP unchanged |
| H4 other load failure | possible causal narrowing | STOP unchanged |

This is the central VOI result:

```
ACTION(H1) = ACTION(H2) = ACTION(H3) = ACTION(H4)
           = STOP_JFOREX_AS_AWS_SUBSTITUTE
```

Therefore the experiment has zero decision-theoretic information value for the current AWS-substitute decision, even though H1 could have moderate scientific value for a different future question.

## 4. AWS substitution relevance

The Lane-B continuity contract requires raw-object integrity and preserves a distinction between raw preservation and decoded-value authority.

The JF02 contract explicitly targets an AWS-independent JForex provider-history evidence model **without claiming S3 raw-object equivalence**.

A JForex API payload is therefore a different evidence object from the Requester-Pays S3 BI5 object.

A successful JForex history call cannot establish:

```
S3_RAW_OBJECT_IDENTITY
S3_KEY_IDENTITY
BI5_BINARY_IDENTITY
REQUESTER_PAYS_OBJECT_IDENTITY
SOURCE_B_EQUIVALENCE
```

Accordingly:

```
AWS_CRITICALITY_DEMOTION_FROM_ONE_GETTICKS = FORBIDDEN / UNSUPPORTED
```

## 5. JForex still has non-AWS utility

Stopping JForex as the AWS substitute does **not** mean deleting or dequalifying JForex globally.

JForex may still be useful later as:

- an official Dukascopy content interface;
- a secondary cross-interface check;
- a data-validation mechanism;
- a non-raw provider evidence channel.

That role should remain dormant until a concrete future decision actually requires it. At that point a new experiment can be designed around that decision rather than continuing JF02 for completion's sake.

## 6. Recommendation

```
PRIMARY_OPTION =
OPTION_A_STOP_JFOREX_AS_AWS_SUBSTITUTE_NOW
```

Secondary disposition:

```
JFOREX_SECONDARY_VALIDATION_ROLE =
RETAIN_DORMANT_OPTIONAL_PATH
```

Do not authorize another JF02 history read now.

The AWS path remains frozen, not demoted and not abandoned. R2A may only be revisited under a separate human decision after credential capability exists and the AWS path is explicitly unfrozen.

## 7. Stop

No provider action, market-data request, AWS request, cache mutation, code repair or launcher execution occurred during A1.
