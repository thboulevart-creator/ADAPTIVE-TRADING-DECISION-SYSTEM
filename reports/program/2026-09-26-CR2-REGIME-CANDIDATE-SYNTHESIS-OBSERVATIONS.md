# CR2 — Regime-Candidate Synthesis — observations

Date: 2026-09-26

## C01 — ABS_VOL × TICK

C01 is SUPPORTED_N0_SYNTHESIS.

The nine-state joint context carries incremental information about the joint future volatility/activity environment beyond:
- hour+weekday + absolute-volatility state alone;
- hour+weekday + tick-density state alone.

The result is fold-consistent in F1/F2/F3 and remains positive at the 60m secondary horizon.

This supports the existence of a **candidate joint dynamic context structure**.

It does not support semantic labels, direction, PnL, or a validated regime claim.

## C02 — REL_VOL × TICK

C02 has positive scores but is NOT_INTERPRETABLE.

Reason:
F2 state 2 has only 53 observations, below the frozen floor of 500.

No threshold/bin redesign is authorized after observing this result.

## Consequence

Only C01 has crossed the CR2 N0 synthesis gate.

The next scientific question is no longer "can we find another combination?"

It is:

> Can the exact frozen C01 construction reproduce its incremental information on genuinely new/pristine data?

That requires a separate confirmatory Charter before accessing the confirmation data.
