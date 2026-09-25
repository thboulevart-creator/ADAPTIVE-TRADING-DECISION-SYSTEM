# AP5 R4 pre-execution block — PowerShell/python -c wrapper syntax

Date: 2026-09-25
Branch of record: `integration/system-v1`
Fresh HEAD before persistence: `a9a4fc78c4880484774d14f3206ee289422b6914`

Observed local execution:
- repository origin verified;
- local branch intentionally preserved as `feat/min-experiment-gaps-batch-v1`;
- remote integration HEAD matched `a9a4fc78c4880484774d14f3206ee289422b6914`;
- AP0 manifest SHA matched `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`;
- a new R4 stage directory was created;
- Python failed before materializing helper/AP4 with a syntax error at the literal filename `2026-09-25-AP4-PRICE-STRUCTURE.json`.

Interpretation:
the multi-line Python program passed via Windows PowerShell `python -c` lost quoting during native-command argument handling. This is a wrapper/transport failure only.

No AP5 helper was executed.
No AP4/helper exact materialization was completed.
No R4 JSON was produced.
No AP5 evidence state changed.

Next action:
use a temporary Python source file written by PowerShell, then invoke `python <script.py>`. This removes the native-command quoting ambiguity while preserving the same binary Git-blob materialization contract.
