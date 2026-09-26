# SESSION BACKUP — 2026-09-26 — CR1 V0.2 HELPER QUALIFIED

Root cause closed:
registry Git blob was correct; auxiliary SHA-256 metadata was wrong.

Correct registry SHA-256:
`24db0f82a602fa9e1abc04d2793898847c98dc27ed5fe4a16bcd12502fd787a4`.

Corrected helper:
- blob `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- SHA-256 `423eed0f22b87a92210f53c6668c5b242c8ddb687da3292415c43879fb1f4eac`
- py_compile PASS
- 26/26 synthetic PASS
- 20/20 mutants killed

Next action:
one governed local CR1 N0 corpus run.
