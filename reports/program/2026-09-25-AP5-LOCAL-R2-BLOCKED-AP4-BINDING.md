# AP5 R2 — repeated local block on AP4 binding

Date: 2026-09-25
Branch: `integration/system-v1`
Fresh HEAD before persistence: `afb1d07ed24375072397df8161a539d4f71dea46`

R2 evidence received from the owner:
- 151 bytes;
- SHA-256 `89bb73dd6008ae66a55306f73a29edb25b586496067d050557f8b258dcaa1860`;
- status `BLOCKED_AP5_AP4_BINDING`;
- same reason as R1.

R2 therefore does not constitute a new AP5 corpus observation. It repeats the same pre-corpus binding failure.

The attempted raw-blob repair was not demonstrated to have produced canonical AP4 bytes before the R2 run, because both the size and SHA checks failed.

Next action:
diagnose the bytes returned by local `git cat-file blob 3bc22e33956dc422ad45d4a825c89255bf60c432` versus the staged AP4 file. Do not run AP5 again until the raw Git-object bytes themselves are proven canonical.
