# RPE-04 — HARDENING TEST CORRECTION — INTERNAL ADJUDICATION

Date: 2026-10-04

The frozen hardening RED test blob was:

d1bf928dd205a4d6c47761cf0a535aa5b315f10a

After implementing the runtime-binding requirement, 4/5 hardening tests became GREEN.

The remaining test failed because the test monkeypatched the pre-existing helper named _sha256_file, while the new runtime dependency binding intentionally uses a distinct helper named _raw_sha256_file.

This is a test harness defect. The requirement remains unchanged:
a mismatched runtime dependency digest must make _verify_runtime_bindings() return false.

Authorized correction:
- replace only the monkeypatch target _sha256_file with _raw_sha256_file;
- change no expected verdict;
- change no implementation requirement;
- change no authority or claim scope.

Corrected hardening test worktree blob:

aeab0dd79b2e90d108525323ac401c062cc49ec8
