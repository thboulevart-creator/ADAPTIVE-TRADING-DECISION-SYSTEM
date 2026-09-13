# 3.1.2 — ADVERSARIAL QUALIFICATION REPORT

## Verdict

**PASS — PROTOCOLE DE BASELINE**

This PASS validates the experiment protocol, not the trading performance of Momentum V1.

## Candidate under attack

`docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md`

## Attack 1 — Dataset ambiguity

**Failure found:** a baseline could accidentally execute on the one-month B05 corpus while being described as a research backtest.

**Correction:** protocol now explicitly requires dataset identity and a minimum five-year gate for a real backtest qualification. B05 January-2025 is explicitly marked insufficient by itself.

**Re-break:** no execution is admissible without a dataset satisfying the gate. PASS.

## Attack 2 — Look-ahead through current bar

**Failure risk:** computing the close-based signal at `t` and acting within the same bar could leak information into execution.

**Correction:** signal is computed after close of `t` and becomes actionable only at `t+1`.

**Re-break:** any execution before `t+1` violates the protocol. PASS.

## Attack 3 — Hidden optimization

**Failure risk:** changing the 20-bar horizon, threshold, asset, costs, or exit model after seeing results would convert a baseline into a selected candidate.

**Correction:** all such changes are explicitly prohibited in the baseline and must become separate experiments.

**Re-break:** a parameter sweep cannot be accepted as the baseline result. PASS.

## Attack 4 — Invented exits

**Failure found:** Momentum V1 is only a directional expert. A backtest still needs a position/exit harness.

**Correction:** protocol explicitly separates signal definition from the experimental execution/position convention and requires that convention to be frozen before results are seen.

**Re-break:** no implicit SL/TP/RR may be introduced after the fact. PASS.

## Attack 5 — Zero-cost illusion

**Failure risk:** omitting spread/commission/slippage could manufacture an artificial result.

**Correction:** required costs must be explicitly recorded; unknown required costs cause BLOCKED, not zero.

**Re-break:** zero-cost execution without evidence is inadmissible. PASS.

## Attack 6 — OOS contamination

**Failure risk:** selecting OOS dates or interpreting OOS after seeing results can contaminate the evaluation.

**Correction:** split dates must be fixed before execution and persisted; no parameter calibration is permitted in the baseline.

**Re-break:** changing the split after results invalidates the run. PASS.

## Attack 7 — Metric cherry-picking

**Failure risk:** declaring success from one attractive metric.

**Correction:** minimum metric set is fixed and results must preserve gross/net costs, drawdown, trades, expectancy, long/short and temporal views, plus OOS separately.

**Re-break:** no single metric constitutes a Momentum acceptance criterion. PASS.

## Attack 8 — Reproducibility failure

**Failure risk:** a result cannot be reproduced because code, data, protocol, contract, or cost assumptions are not identified.

**Correction:** all identities and run artifacts are mandatory evidence.

**Re-break:** missing identity makes the execution evidence incomplete. PASS.

## Attack 9 — Confusion between protocol PASS and strategy PASS

**Failure risk:** a protocol validation could be misread as proof that Momentum is profitable.

**Correction:** document explicitly separates protocol PASS from execution result and from economic value.

**Re-break:** the protocol PASS cannot certify profitability. PASS.

## Final qualification

The protocol survives the identified attacks after correction and re-break.

**3.1.2 — PROTOCOLE BASELINE = PASS**

### What is now allowed

Proceed to an actual baseline execution only when the execution dataset and fixed execution/exit harness are available and satisfy the protocol.

### What is not allowed

- no parameter optimization;
- no regime filter;
- no retrospective exit changes;
- no zero-cost assumption without evidence;
- no use of the one-month B05 corpus as a substitute for the five-year research gate;
- no claim that protocol PASS means strategy profitability.

## Execution status at this checkpoint

**BLOCKED — execution environment/data gate not yet satisfied in the current accessible GitHub context.**

The protocol is PASS, but the accessible environment does not contain the required five-year execution dataset nor a verified fixed position/exit harness. Therefore no fabricated or partial backtest is executed.
