# SESSION BACKUP — 2026-09-26 — CONTEXT / REGIME RESEARCH PREFLIGHT V0.1

Repo: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`.

Closed upstream:
AP0→AP6 PASS; ASSET BEHAVIORAL PROFILE CORE V0.1 PASS.

New frontier:
**CR1 CONTEXT INFORMATIVENESS — N0 EXPLORATORY.**

Preflight:
`reports/program/2026-09-26-CONTEXT-REGIME-RESEARCH-PREFLIGHT-V0.1.md`

Hypothesis registry:
`reports/program/evidence/2026-09-26-CONTEXT-REGIME-HYPOTHESIS-REGISTRY-V0.1.json`

Core design:
- no regime labels yet;
- 8 preregistered context axes;
- strict causal cutoff at t;
- future descriptive targets begin at t+1;
- chronological F1=2023, F2=2024, F3=2025;
- 2026 partial diagnostic only;
- no period is pristine OOS because AP0→AP6 already inspected the corpus;
- baselines B0/B1/B2;
- continuous states fixed to training-only tertiles;
- target classes fixed to training-only quintiles;
- scoring by out-of-fold delta log-loss + delta Brier;
- exact SUPPORTED_N0 / REFUTED_N0 / NOT_INTERPRETABLE rules frozen;
- no PnL, direction target, feature search, threshold search, interaction search or winner selection.

Next action:
build only the CR1 helper/tests/mutation breakers, qualify persisted bytes, then seek a separate corpus-run authorization.
