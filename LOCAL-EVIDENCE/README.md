# LOCAL-EVIDENCE

This directory is the governed workstation-side evidence area for runtime artifacts that should remain available locally without committing opaque binary archives to Git.

## Dukascopy Trading Breaks widget runtime evidence

Canonical local root on the workstation:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Raw ZIP archives belong in:

`raw-zips\`

The ZIP files themselves are ignored by `.gitignore`.

A local manifest must be generated alongside them at:

`manifest-sha256.csv`

The manifest identifies each retained local archive by filename, size, relative path, timestamp and SHA-256.

A versioned helper is provided:

`tools/archive_local_trading_breaks_evidence.ps1`

Run it from the repository after downloading the three retained ZIPs. It verifies the expected SHA-256 values before accepting the archives, moves them into the canonical `raw-zips\` directory, and regenerates the manifest.

## Retained GitHub Actions artifacts

### 1. Authoritative calibration witness — 2020-02-17 PRESIDENTS_DAY

- GitHub artifact name: `dukascopy-trading-breaks-widget-2020-02-17`
- retained local filename: `dukascopy-trading-breaks-widget-2020-02-17-authoritative.zip`
- artifact ID: `10356927580`
- workflow run: `34866241511`
- size: `810965` bytes
- SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
- role: authoritative calibration artifact used by the locked PASS verdict.

### 2. Calibration technical trace — headed-browser predecessor

- GitHub artifact name: `dukascopy-trading-breaks-widget-2020-02-17`
- retained local filename: `dukascopy-trading-breaks-widget-2020-02-17-headed-browser.zip`
- artifact ID: `10356971957`
- workflow run: `34865846126`
- size: `709841` bytes
- SHA-256: `aaf5341f3d7e10b60cc24622d6f16c2ffa3e3f31d6b108f69f53c6f3a2d48849`
- role: technical predecessor/trace from the headed-browser probe; retained for auditability only.
- authority boundary: this archive does **not** replace the final calibration artifact above and must not independently upgrade a calendar date.

### 3. Authoritative unresolved-date pilot — 2021-09-06 LABOR_DAY

- GitHub artifact name: `dukascopy-trading-breaks-widget-pilot-2021-09-06`
- retained local filename: `dukascopy-trading-breaks-widget-pilot-2021-09-06-authoritative.zip`
- artifact ID: `10357256669`
- workflow run: `34866699952`
- size: `797338` bytes
- SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
- role: authoritative pilot artifact supporting the locked PASS-A for 2021-09-06.

## Verification performed on 2026-09-14

The three GitHub artifacts above were re-downloaded after the original chat download links expired. Their locally recomputed SHA-256 values matched the GitHub artifact digests exactly.

This verifies artifact identity at re-download time. It does **not** claim that the files have already been placed on the user's workstation; workstation placement is completed only after the PowerShell archival helper is run locally.

## Evidence boundary

Do not infer proof from archive presence alone. The authoritative qualification remains the versioned reports, workflow/run/artifact identities, hashes, and governed route contracts in the repository.

An empty/no-record widget response is still non-evidence for normal trading until the separate negative-evidence/completeness contract is qualified.
