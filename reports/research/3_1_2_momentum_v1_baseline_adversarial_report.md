# 3.1.2 — ADVERSARIAL QUALIFICATION REPORT

## Verdict

**PASS — PROTOCOLE DE BASELINE**

This PASS validates the experiment protocol, not Momentum profitability.

## Candidate

`docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md`

## Attack 1 — Dataset ambiguity

**Failure:** the one-month B05 corpus could be mistakenly used as if it satisfied the research backtest gate.

**Correction:** minimum five-year requirement is explicit; B05 January-2025 is explicitly insufficient.

**Re-break:** execution on B05 alone is inadmissible. PASS.

## Attack 2 — Look-ahead

**Failure risk:** calculate the close signal at `t` and execute before the close or inside the same bar.

**Correction:** signal is frozen after close of `t`; first admissible action is `t+1`.

**Re-break:** same-bar execution violates protocol. PASS.

## Attack 3 — Hidden optimization

**Failure risk:** change horizon, threshold, asset, costs, or harness after seeing results.

**Correction:** baseline forbids all such tuning; changed candidates become separate experiments.

**Re-break:** optimization cannot overwrite baseline. PASS.

## Attack 4 — Invented exit / position rule

**Failure found:** 3.1.1 is a directional expert, so an executable backtest needs a separate deterministic harness.

**Correction:** the protocol now freezes one normalized-unit convention before execution:
- LONG signal → +1 at first admissible price of `t+1`;
- SHORT signal → -1 at first admissible price of `t+1`;
- NEUTRE → flat;
- opposite signal → close/reverse at first admissible price of the next bar;
- no SL, TP, trailing, BE, pyramiding, scaling, or discretionary exit.

**Re-break:** changing the harness after seeing results invalidates the baseline. PASS.

## Attack 5 — Cost omission

**Failure risk:** zero spread/commission/slippage manufactures an artificial result.

**Correction:** required costs must be explicitly identified; unknown required cost → BLOCKED, never zero by assumption.

**Re-break:** cost-free execution without evidence is inadmissible. PASS.

## Attack 6 — OOS contamination

**Failure risk:** move the OOS dates after observing results.

**Correction:** exact split is fixed before execution; no baseline calibration.

**Re-break:** changing split invalidates the run. PASS.

## Attack 7 — Metric cherry-picking

**Failure risk:** one attractive metric becomes the verdict.

**Correction:** minimum metric set is fixed and no single metric is an acceptance criterion for Momentum.

**Re-break:** protocol PASS cannot be derived from a chosen performance metric. PASS.

## Attack 8 — Reproducibility failure

**Failure risk:** code/data/protocol/cost identities are missing.

**Correction:** all identities and run artifacts are mandatory.

**Re-break:** missing identity makes execution evidence incomplete. PASS.

## Attack 9 — Protocol vs strategy confusion

**Failure risk:** protocol PASS is misreported as a strategy PASS.

**Correction:** protocol PASS, execution verdict, and economic interpretation are explicitly separated.

**Re-break:** protocol PASS cannot certify profitability. PASS.

## Final qualification

The protocol survived the first adversarial break, correction, and re-break.

**3.1.2 — PROTOCOLE BASELINE = PASS**

## Execution gate

Actual baseline execution is currently:

**BLOCKED**

Reason: the accessible GitHub context does not contain a verified five-year execution dataset nor the required live/local execution environment needed to identify the first admissible `t+1` execution price and realistic costs. The one-month B05 corpus cannot be substituted.

No partial or fabricated backtest is executed.

## Prohibitions retained

- no B02–B08 rerun;
- no B09.7 rerun;
- no regime filter;
- no optimization;
- no retrospective harness changes;
- no zero-cost assumption without evidence;
- no claim that protocol PASS means strategy profitability.
