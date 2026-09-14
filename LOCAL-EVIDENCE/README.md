# LOCAL-EVIDENCE

This directory is the governed workstation-side evidence area for runtime artifacts that should remain available locally without committing opaque binary archives to Git.

## Dukascopy Trading Breaks widget runtime evidence

Canonical local root on the workstation:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Raw ZIP archives belong in:

`raw-zips\`

The ZIP files themselves are ignored by `.gitignore`.

A local manifest should be generated alongside them at:

`manifest-sha256.csv`

The manifest is intended to be versioned so that each retained local archive is identified by filename, size, relative path, timestamp and SHA-256.

Known authoritative GitHub Actions artifacts for the qualified route:

1. Calibration witness `2020-02-17 — PRESIDENTS_DAY`
   - artifact name: `dukascopy-trading-breaks-widget-2020-02-17`
   - artifact ID: `10356927580`
   - SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
   - workflow run: `34866241511`

2. Unresolved-date pilot `2021-09-06 — LABOR_DAY`
   - artifact name: `dukascopy-trading-breaks-widget-pilot-2021-09-06`
   - artifact ID: `10357256669`
   - SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
   - workflow run: `34866699952`

Any additional downloaded ZIP retained in `raw-zips\` must be recorded by the generated SHA-256 manifest before it is treated as durable local evidence.

Do not infer proof from archive presence alone. The authoritative qualification remains the versioned reports and governed route contracts in the repository.
