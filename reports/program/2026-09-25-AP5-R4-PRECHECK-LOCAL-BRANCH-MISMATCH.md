# AP5 R4 precheck — local branch mismatch is not an AP5 blocker

Date: 2026-09-25
Branch of record: `integration/system-v1`
Fresh HEAD before persistence: `7119a15dbe7766ce39df669c0d49f971dbdb0bff`

Local checkout reported by owner:
`feat/min-experiment-gaps-batch-v1`.

GitHub verification:
- remote branch exists;
- remote head: `2951345d8f0b47400b8b2d52885615f01f11556b`;
- comparison versus `integration/system-v1`: diverged;
- ahead by 25;
- behind by 884;
- merge base: `ff50b6d5d123969e091b5df18c46d438f7cb8052`.

Adjudication:
the local checkout must not be reset, merged, rebased, or otherwise altered merely to execute AP5 R4.

R4 only requires:
1. correct repository origin;
2. successful fetch of `origin/integration/system-v1`;
3. exact remote HEAD binding;
4. raw Git blob access to the frozen helper and AP4 evidence;
5. AP0 local corpus paths.

Therefore the local checked-out branch is not part of the R4 execution identity and the branch guard is removed.

Next action:
run R4 from the existing checkout while leaving `feat/min-experiment-gaps-batch-v1` untouched.
