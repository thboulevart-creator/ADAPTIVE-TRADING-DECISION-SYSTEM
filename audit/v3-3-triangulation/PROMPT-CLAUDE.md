# CLAUDE — falsification and conformance request

Audit the V3.3 downloader in this directory against `README.md`.

Your role is to attempt to prove the implementation WRONG. Do not optimize for a PASS and do not trust prior conclusions. Inspect the complete source and identify invariant violations, edge cases, ambiguous states, unsafe recovery paths, and places where the implementation can claim VALID without sufficient evidence.

Pay particular attention to:
- manifest state transitions and historical VALID preservation;
- restart/idempotence behavior;
- RAW immutability and overwrite protection;
- NO_DATA vs FAILED semantics;
- exact tick schema and rejection of OHLC contamination;
- timestamp bounds, monotonicity and daily partition boundaries;
- finite/positive prices and ask >= bid;
- finite/non-negative volumes;
- exactly-one-output-file assumptions;
- pre/post-copy validation and SHA-256/size checks;
- provenance, runner hash and dependency pinning;
- PowerShell parameter compatibility;
- deterministic exit codes;
- memory/runtime behavior when scaled from one day to roughly ten years.

Do not modify the source. For every finding use PASS / FAIL / BLOCKED only, with exact evidence and a minimal corrective action. Explicitly distinguish current violation, architectural exposure, and absence of proof. Never convert inability to execute into PASS.
