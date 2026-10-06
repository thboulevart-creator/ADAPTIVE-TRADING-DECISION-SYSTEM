# BEPD-07B — IMPLEMENTATION REQUALIFICATION R1 AFTER AP0 FILE-SET IDENTITY CORRECTION

## Verdict

```text
BEPD-07B IMPLEMENTATION R1 =
REQUALIFIED PRE-RESULT

SCIENTIFIC SEMANTICS CHANGED =
NO

REAL AP0 PRICE COLUMN READ AFTER CORRECTION =
NO

REAL EXCURSION STATISTICS =
NOT CALCULATED

REAL EXCURSION DISTRIBUTION EXPOSURE =
NO
```

## Failure discovered by first real pre-read

The initial frozen implementation failed closed while verifying AP0 provenance.

```text
AP0 MANIFEST SHA256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce

DATASET =
USTECH_PROFILE_MINUTE_CORE_V0_1

FILE COUNT =
61

ROW COUNT =
1709180

BEPD-02-STYLE DIGEST OBSERVED =
60d6a2f1ddfa7b1daf8589f6ab80c417a153554cf8aba33cab60842c0908601d

DATA-02 ADMISSION DIGEST REQUIRED =
1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a
```

No price columns were loaded and no excursion result was produced.

## Root cause

DATA-02 defines file-set identity from canonical JSON material containing, in manifest order:

```text
relative_path
size_bytes
sha256
```

The original BEPD-07B implementation instead reconstructed a BEPD-02-style LF-joined `relative_path:sha256` digest.

This was an identity-algorithm defect, not a data-content mismatch.

## Corrective delta

Only the following implementation surface changed:

```text
RUNNER =
5b1108cc0fe703d9c45cfebc2ba12eb33c6552de

INDEPENDENT RECOMPUTATION =
27963b7ab2bea48d12bb3da584b430f2c047bb78

SYNTHETIC TESTS =
f14aa4178f630f60e423f2357cb4e342b2e96957
```

The corrected implementations now compute the adopted DATA-02 file-set digest from canonical JSON and also verify each file's size and SHA-256 before any Parquet price-column read.

## Requalification evidence

```text
WORKFLOW RUN =
37480467696

JOB =
112326940993

CONCLUSION =
SUCCESS

SYNTHETIC TESTS =
35 / 35 PASS

BEPD-07A EXECUTABLE-EQUIVALENT BREAKER =
40 / 40 PASS

DATA-02 FILE-SET DIGEST SEMANTICS TEST =
PASS

REAL_AP0_PATH_SCAN =
NOT_EXECUTED

REAL_EXCURSION_STATISTICS =
NOT_CALCULATED

REAL_EXCURSION_DISTRIBUTION_EXPOSURE =
NO
```

## Preserved scientific boundary

```text
BASE N =
472

ANCHOR =
take_h1_close_mid

PATH START =
STRICTLY AFTER take_h1_close_utc

PATH END =
SAME CANONICAL TARGET WEEK END

EXTREMA =
mid_high + mid_low

MAX_REINTEGRATIVE_EXCURSION FORMULA =
UNCHANGED

MAX_EXTERNAL_EXCURSION FORMULA =
UNCHANGED

SUBGROUPS =
NONE

JOINT METRICS =
NONE

PREDICTION =
NO

EDGE =
NO

TRADING AUTHORITY =
NONE
```

## Next action

```text
CREATE DISTINCT REAL EXECUTION FREEZE R1
BINDING THE CORRECTED IMPLEMENTATIONS

THEN

REQUALIFY ACTUAL AP0 MANIFEST + 61 FILE SHA/SIZE + DATA-02 FILE-SET DIGEST

THEN

ONE FIRST REAL GLOBAL BEHAVIORAL EXCURSION EXECUTION

STOP AFTER TECHNICAL QUALIFICATION
```
