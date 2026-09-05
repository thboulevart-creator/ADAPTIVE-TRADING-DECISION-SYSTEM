# GROK — adversarial audit request

You are the hostile reviewer. Audit the V3.3 downloader in this directory against `README.md`.

Do not assume any claimed PASS is true. Recompute it from source and, where execution is available, from executable evidence. Search specifically for hidden failure modes, PowerShell compatibility defects, state-machine/idempotence errors, manifest authorization errors, data-boundary leakage, silent corruption, and 10-year scalability hazards.

Do not modify the implementation. Produce a findings report with:
- PASS / FAIL / BLOCKED only;
- severity;
- exact file + line/function evidence;
- attack/falsification attempted;
- observed result;
- minimal fix;
- whether the issue is a current violation, architectural exposure, or absence of proof.

Highest priority: try to falsify `VALID -> SKIP -> SKIP`, RAW immutability, failure classification, exact tick schema, timestamp/order/price/volume validation, daily boundaries, SHA integrity, and deterministic exit codes.

A review opinion is not proof. If execution is impossible, mark BLOCKED rather than PASS.
