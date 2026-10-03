# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — PRE-DRAFT

Base: RPE-01 adoption commit 8ed3ec4079f3f996a5159b78fc40d0f32a917b25.

RPE-03 defines a no-network local Git ancestry classifier whose only results are INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD and UNKNOWN.

The classifier must verify the local Git object domain before ancestry classification. It strips inherited Git authority, disables replace-object and commit-graph influence, rejects shallow/graft/alternate domains, verifies requested objects are commits, and maps timeout, corruption or unprovable state to UNKNOWN.

merge-base --is-ancestor exit 1 may mean NON_FAST_FORWARD only after both commit identities and the local object domain are verified.

No fetch, ls-remote, remote observation, RPE-04/05/06, P5-D4 real-state mutation, Vault/CURRENT mutation or REAL P5-E is authorized.
