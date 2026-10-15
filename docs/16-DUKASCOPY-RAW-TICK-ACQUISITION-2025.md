# Dukascopy Raw Tick Acquisition — USATECHIDXUSD / 2025

**Status:** EXECUTABLE ACQUISITION PROCEDURE — NOT YET EXECUTED
**Instrument:** `USATECHIDXUSD`
**Period:** `2025-01-01 00:00:00 UTC` through `2025-12-31 23:00:00 UTC`
**Granularity:** native Dukascopy hourly tick files (`.bi5`)
**Acquisition script:** `tools/download_ticks_v1.ps1`

## Objective

Acquire the native Dukascopy tick payloads for the full 2025 calendar year while preserving the source bytes exactly as received.

This acquisition step is deliberately separated from any later decoding or CSV conversion. The raw `.bi5` files are the immutable acquisition layer; any decoded/normalized representation must be a separate derived dataset with its own identity and hash.

## Source

The script uses Dukascopy's public datafeed URL pattern:

`https://datafeed.dukascopy.com/datafeed/{SYMBOL}/{YEAR}/{MONTH_ZERO_BASED}/{DAY}/{HOUR}h_ticks.bi5`

Dukascopy's datafeed uses zero-based months in this URL: January=`00`, February=`01`, ..., December=`11`.

## Integrity and journalization

For every hourly request the script records:

- run ID;
- UTC recording timestamp;
- instrument;
- exact source URL;
- local raw-file path;
- byte count;
- SHA-256 of the received file;
- retry count;
- acquisition status;
- error text when applicable.

Outputs are:

- per-run CSV manifest;
- per-run JSONL event log;
- per-run JSON summary.

An existing non-empty file is not overwritten unless `-Force` is explicitly supplied. A missing source hour is recorded as `MISSING_404`; the script never fabricates a file or fills missing data.

## Non-transformation invariant

The acquisition script MUST NOT:

- decompress `.bi5` files;
- sort ticks;
- deduplicate ticks;
- repair timestamps;
- repair quotes or volumes;
- filter market conditions;
- resample to OHLC/M1/H1;
- convert to CSV;
- infer missing ticks.

The downloaded binary payload is the source artifact. Decoding, if later required by the experiment, belongs to a separate explicitly identified derivation step.

## Recommended execution

Run from PowerShell in the repository checkout:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\download_ticks_v1.ps1 `
  -Symbol USATECHIDXUSD `
  -StartDate ([datetime]::Parse("2025-01-01T00:00:00Z")) `
  -EndDate ([datetime]::Parse("2025-12-31T23:00:00Z")) `
  -OutputRoot "C:\ALGO-DATA\raw\dukascopy" `
  -MaxRetries 3
```

The data should remain outside the Git repository unless a future, explicit storage policy authorizes otherwise.

## Qualification boundary

Successful download does **not** qualify the dataset for the trading experiment by itself.

The next controls remain mandatory:

1. verify acquisition completeness from the manifest;
2. preserve the exact raw-file hashes;
3. establish the dataset identity/provenance record;
4. decode only through a separately controlled derivation step if required;
5. run dataset admissibility checks on the derived experiment input;
6. execute the minimum experiment;
7. capture the immutable run/result/validation/failure records;
8. perform the adversarial post-run audit.

Until these controls are executed and evidenced, the real NAS100 experiment remains **BLOCKED**.
