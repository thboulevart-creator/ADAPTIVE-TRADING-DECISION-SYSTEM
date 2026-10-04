# RPE-04 — PREREGISTRATION TARGETED CORRECTION BEFORE GREEN

Date: 2026-10-04

The initial preregistration was frozen before RED and validated by the RPE-01 public guard.

During the first implementation-candidate run, all functional failures converged on the local-config allowlist.

A fresh local calibration under the exact neutralized RPE-04 Git environment observed these five entries:

- core.repositoryformatversion=0
- core.filemode=false
- core.bare=true
- core.symlinks=false
- core.ignorecase=true

The initial calibration had omitted core.symlinks=false.

This correction adds only that observed entry to the closed local-config allowlist. It changes no fetch semantics, evidence semantics, timing semantics, claim scope, or authority.

The correction occurs before any GREEN result. The preregistration status is therefore explicitly changed to PREREGISTRATION_CORRECTED_AFTER_RED_BEFORE_GREEN.

The frozen RED test file is unchanged.
