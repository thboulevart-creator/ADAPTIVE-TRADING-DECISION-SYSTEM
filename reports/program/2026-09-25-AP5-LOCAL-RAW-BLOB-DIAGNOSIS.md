# AP5 — local raw Git blob diagnosis

Date: 2026-09-25
Branch: `integration/system-v1`
Fresh HEAD before persistence: `b74436379dbfbc54ce057703e1e9a0691fb40236`

Read-only local diagnostic supplied by the owner:

Canonical raw Git object:
- length: 15,488 bytes
- SHA-256: `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`
- LF count: 644
- CRLF count: 0

Current staged AP4:
- length: 16,132 bytes
- SHA-256: `7019e769da721d757bc8f0cf9fc1203e96bfd1923acc92b1cd3e332d5a96e78e`
- LF count: 644
- CRLF count: 644
- equality with raw Git blob: false

Diagnostic command exited 0.

## Adjudication

Local Git object storage is canonical and not the source of the corruption.

The staged AP4 file alone contains full CRLF normalization. The exact byte delta and line-ending counts prove the mismatch.

Next action:
perform an atomic binary rewrite of the staged AP4 from the canonical raw Git blob and verify the just-written bytes in the same Python process. AP5 R3 is authorized only if that in-process verification reports exact size 15,488 and exact canonical SHA-256.
