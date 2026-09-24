param(
    [string]$RepositoryRoot = (Get-Location).Path,
    [string]$RelativeCorpusPath = "data/research_source_b_ustech/parquet",
    [string]$OutputPath = (Join-Path $env:TEMP "ATDS-E0-SOURCE-B-MANIFEST.json")
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Budget = [ordered]@{
    max_entries = 1000
    max_parquet_files = 500
    max_total_parquet_read_bytes = 17179869184 # 16 GiB
    max_footer_metadata_bytes = 134217728      # 128 MiB
    max_single_file_full_read_bytes = 8589934592 # 8 GiB
}

function Stop-WithManifest {
    param(
        [string]$Status,
        [string]$Reason,
        [object]$Manifest
    )
    $Manifest.status = $Status
    $Manifest.reason = $Reason
    $json = $Manifest | ConvertTo-Json -Depth 8
    $outParent = Split-Path -Parent $OutputPath
    if ($outParent -and -not (Test-Path -LiteralPath $outParent)) {
        New-Item -ItemType Directory -Path $outParent -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($OutputPath, $json, [System.Text.UTF8Encoding]::new($false))
    Write-Host $json
    Write-Host ""
    Write-Host "Manifest: $OutputPath"
    exit 2
}

$repoRootResolved = [System.IO.Path]::GetFullPath($RepositoryRoot)
$corpusPath = [System.IO.Path]::GetFullPath((Join-Path $repoRootResolved $RelativeCorpusPath))
$expectedPrefix = $repoRootResolved.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

$manifest = [ordered]@{
    schema = "ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1"
    generated_at_utc = [DateTime]::UtcNow.ToString("o")
    repository_root = $repoRootResolved
    relative_corpus_path = $RelativeCorpusPath
    resolved_corpus_path = $corpusPath
    budget = $Budget
    status = "PRECHECK"
    reason = $null
    read_only_contract = [ordered]@{
        corpus_writes = 0
        provider_network = $false
        strategy_calculation = $false
        pnl_calculation = $false
        backtest = $false
        follow_reparse_points = $false
    }
    inventory = [ordered]@{
        total_entries = 0
        parquet_files = 0
        total_parquet_bytes = 0
        sha256_complete = $false
        parquet_magic_checked = $false
        files = @()
    }
}

if (-not $corpusPath.StartsWith($expectedPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    Stop-WithManifest "BLOCKED_PATH_ESCAPE" "Resolved corpus path escapes RepositoryRoot." $manifest
}

if (-not (Test-Path -LiteralPath $corpusPath -PathType Container)) {
    Stop-WithManifest "BLOCKED_CORPUS_NOT_FOUND" "Exact corpus directory is not present." $manifest
}

$rootItem = Get-Item -LiteralPath $corpusPath -Force
if (($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
    Stop-WithManifest "BLOCKED_REPARSE_POINT" "Corpus root is a reparse point/symlink." $manifest
}

$allEntries = @(Get-ChildItem -LiteralPath $corpusPath -Force -Recurse)
$manifest.inventory.total_entries = $allEntries.Count
if ($allEntries.Count -gt $Budget.max_entries) {
    Stop-WithManifest "BLOCKED_ENTRY_BUDGET" "Entry count exceeds preregistered 1000-entry budget." $manifest
}

$reparse = @($allEntries | Where-Object { ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0 })
if ($reparse.Count -gt 0) {
    $manifest.reparse_points = @($reparse | ForEach-Object { $_.FullName })
    Stop-WithManifest "BLOCKED_REPARSE_POINT" "At least one reparse point/symlink exists inside the corpus." $manifest
}

$parquet = @(
    $allEntries |
    Where-Object { -not $_.PSIsContainer -and $_.Extension -ieq ".parquet" } |
    Sort-Object FullName
)

$manifest.inventory.parquet_files = $parquet.Count
if ($parquet.Count -eq 0) {
    Stop-WithManifest "BLOCKED_NO_PARQUET" "No .parquet files found in exact corpus directory." $manifest
}
if ($parquet.Count -gt $Budget.max_parquet_files) {
    Stop-WithManifest "BLOCKED_FILE_COUNT_BUDGET" "Parquet file count exceeds preregistered 500-file budget." $manifest
}

$totalBytes = [Int64](($parquet | Measure-Object -Property Length -Sum).Sum)
$manifest.inventory.total_parquet_bytes = $totalBytes

$fileRows = @()
foreach ($file in $parquet) {
    $relative = [System.IO.Path]::GetRelativePath($corpusPath, $file.FullName)
    $fileRows += [ordered]@{
        relative_path = $relative.Replace("\\","/")
        size_bytes = [Int64]$file.Length
        last_write_utc = $file.LastWriteTimeUtc.ToString("o")
        sha256 = $null
        sha256_status = "NOT_RUN"
        parquet_magic_head = $null
        parquet_magic_tail = $null
        parquet_magic_status = "NOT_RUN"
    }
}
$manifest.inventory.files = $fileRows

# Minimal 8-byte/file format sanity check, counted against metadata budget.
$magicReadBytes = [Int64]($parquet.Count * 8)
if ($magicReadBytes -gt $Budget.max_footer_metadata_bytes) {
    Stop-WithManifest "BLOCKED_METADATA_BUDGET" "Magic-byte checks exceed preregistered metadata budget." $manifest
}

for ($i=0; $i -lt $parquet.Count; $i++) {
    $file = $parquet[$i]
    if ($file.Length -lt 8) {
        $manifest.inventory.files[$i].parquet_magic_status = "FAIL_TOO_SMALL"
        continue
    }
    $stream = [System.IO.File]::Open($file.FullName, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try {
        $head = New-Object byte[] 4
        [void]$stream.Read($head, 0, 4)
        [void]$stream.Seek(-4, [IO.SeekOrigin]::End)
        $tail = New-Object byte[] 4
        [void]$stream.Read($tail, 0, 4)
        $headText = [System.Text.Encoding]::ASCII.GetString($head)
        $tailText = [System.Text.Encoding]::ASCII.GetString($tail)
        $manifest.inventory.files[$i].parquet_magic_head = $headText
        $manifest.inventory.files[$i].parquet_magic_tail = $tailText
        $manifest.inventory.files[$i].parquet_magic_status = if ($headText -eq "PAR1" -and $tailText -eq "PAR1") { "PASS" } else { "FAIL" }
    }
    finally {
        $stream.Dispose()
    }
}
$manifest.inventory.parquet_magic_checked = $true

if (@($manifest.inventory.files | Where-Object { $_.parquet_magic_status -ne "PASS" }).Count -gt 0) {
    Stop-WithManifest "BLOCKED_PARQUET_MAGIC" "One or more files do not have PAR1 head/tail magic." $manifest
}

if ($totalBytes -gt $Budget.max_total_parquet_read_bytes) {
    Stop-WithManifest "BLOCKED_TOTAL_READ_BUDGET" "Total Parquet bytes exceed preregistered 16 GiB hashing budget." $manifest
}

$oversized = @($parquet | Where-Object { $_.Length -gt $Budget.max_single_file_full_read_bytes })
if ($oversized.Count -gt 0) {
    $manifest.oversized_files = @($oversized | ForEach-Object {
        [ordered]@{ relative_path = [System.IO.Path]::GetRelativePath($corpusPath, $_.FullName).Replace("\\","/"); size_bytes = [Int64]$_.Length }
    })
    Stop-WithManifest "BLOCKED_SINGLE_FILE_BUDGET" "At least one Parquet file exceeds preregistered 8 GiB full-read budget." $manifest
}

for ($i=0; $i -lt $parquet.Count; $i++) {
    $hash = (Get-FileHash -LiteralPath $parquet[$i].FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    $manifest.inventory.files[$i].sha256 = $hash
    $manifest.inventory.files[$i].sha256_status = "PASS"
}
$manifest.inventory.sha256_complete = $true
$manifest.status = "MANIFEST_COMPLETE"
$manifest.reason = "Exact file inventory and SHA-256 completed within preregistered E0 budget."

$json = $manifest | ConvertTo-Json -Depth 8
$outParent = Split-Path -Parent $OutputPath
if ($outParent -and -not (Test-Path -LiteralPath $outParent)) {
    New-Item -ItemType Directory -Path $outParent -Force | Out-Null
}
[System.IO.File]::WriteAllText($OutputPath, $json, [System.Text.UTF8Encoding]::new($false))
Write-Host $json
Write-Host ""
Write-Host "Manifest: $OutputPath"
exit 0
