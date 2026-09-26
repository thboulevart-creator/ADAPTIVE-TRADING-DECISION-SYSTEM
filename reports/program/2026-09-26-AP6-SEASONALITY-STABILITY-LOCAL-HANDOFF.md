# AP6 — Seasonality / Stability — local execution handoff

Date : 2026-09-26  
Branch of authority : `integration/system-v1`

## Qualified helper

- Git blob: `28b5a298156616b9385dc0d8e4b0cfbaa3705497`
- SHA-256: `e5463af97783e193f54e1ef25d96626c6a9a511e7236469054b69a788f6dfc6c`

Exact bound evidence:
- AP3 blob `4c6cca91e6f7f972702c1859226bd3612e3ec920`, SHA-256 `caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef`
- AP4 blob `3bc22e33956dc422ad45d4a825c89255bf60c432`, SHA-256 `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`
- AP5 blob `061efdaedbc2cfa158e855b0d8bb6c679a782358`, SHA-256 `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406`
- AP0 manifest SHA-256 `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`

## Required execution pattern

Preserve the user's current local checkout unchanged.

For the corpus attempt:
1. fetch `origin/integration/system-v1`;
2. require the exact authorized remote HEAD;
3. verify local AP0 manifest SHA;
4. create a brand-new temporary stage;
5. materialize helper + AP3 + AP4 + AP5 as **raw Git blob bytes**;
6. verify each SHA-256 in-process;
7. independently rehash helper/evidence after materialization;
8. py_compile helper;
9. execute once to a unique AP6 output path;
10. preserve any BLOCKED output; never overwrite/delete it;
11. if exit 0 / AP6_COMPLETE, copy exact JSON to the handoff directory and return terminal + file.

No branch switch/reset/rebase/merge is required.
