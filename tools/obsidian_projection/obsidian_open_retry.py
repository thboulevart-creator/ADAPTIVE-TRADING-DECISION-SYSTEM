from __future__ import annotations

import ctypes
import hashlib
import json
import os
import tempfile
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from .obsidian_open_compatibility import (
    LIVE_VAULT,
    SANDBOX_VAULT,
    SNAPSHOT_SCHEMA,
    ObsidianOpenCompatibilityError,
    OpenPointerMissingError,
    OpenPointerMixedError,
    OpenPointerPartialError,
    _canonical_json_bytes,
    _current_note_bytes,
    _load_snapshot,
    _require_generation_immutability,
    _require_snapshot_live_digests,
    _safe_obsidian_state,
    _sha256,
    build_markdown_generation,
    obsidian_running,
    validate_current_pointer,
    write_current_atomic,
)


class ObsidianOpenRetryError(RuntimeError):
    pass


class ReplaceRetryDeadlineExceeded(ObsidianOpenRetryError):
    pass


class ReaderAccessRetryDeadlineExceeded(ObsidianOpenRetryError):
    pass


CONTRACT_SCHEMA = "ATDS_OBSIDIAN_OPEN_RETRY_CONTRACT_V0_1"
CONTRACT_BLOB = "5648b2f7d3d3beb528539cd7c711c39210270064"

PROMOTION_CYCLES = 250
MIN_READER_SAMPLES = 5000
READER_INTERVAL_SECONDS = 0.001

WRITE_RETRY_DEADLINE_SECONDS = 5.0
WRITE_INITIAL_BACKOFF_SECONDS = 0.010
WRITE_MAX_BACKOFF_SECONDS = 0.500

READ_RETRY_DEADLINE_SECONDS = 0.500
READ_INITIAL_BACKOFF_SECONDS = 0.005
READ_MAX_BACKOFF_SECONDS = 0.050

RETRY_METRICS_SCHEMA = "ATDS_OBSIDIAN_P5C3R_OPEN_METRICS_V0_1"
RECOVERY_SCHEMA = "ATDS_OBSIDIAN_P5C3R_RECOVERY_REPORT_V0_1"
LOCK_BREAKER_SCHEMA = "ATDS_OBSIDIAN_P5C3R_SYNTHETIC_LOCK_BREAKER_V0_1"
POST_CLOSE_SCHEMA = "ATDS_OBSIDIAN_P5C3R_POST_CLOSE_REPORT_V0_1"


def _git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def verify_retry_contract(package_dir: Path) -> dict[str, Any]:
    path = package_dir / "obsidian_open_retry_contract_v0_1.json"
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise ObsidianOpenRetryError(
            "P5-C3R retry contract unreadable"
        ) from exc

    if _git_blob_oid(raw) != CONTRACT_BLOB:
        raise ObsidianOpenRetryError(
            "P5-C3R retry contract blob mismatch"
        )
    if value.get("schema") != CONTRACT_SCHEMA:
        raise ObsidianOpenRetryError(
            "unexpected P5-C3R retry contract schema"
        )
    return value


def _event_log_path() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise ObsidianOpenRetryError(
            "LOCALAPPDATA unavailable"
        )
    return (
        Path(local)
        / "ATDS"
        / "obsidian_projection"
        / "p5c3r"
        / "retry-events.jsonl"
    )


def _append_event(report: dict[str, Any]) -> Path:
    path = _event_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as handle:
        handle.write(_canonical_json_bytes(report))
        handle.flush()
        os.fsync(handle.fileno())
    return path


def _is_winerror_5(exc: BaseException) -> bool:
    current: BaseException | None = exc
    seen: set[int] = set()

    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if (
            isinstance(current, PermissionError)
            and getattr(current, "winerror", None) == 5
        ):
            return True
        current = current.__cause__

    return False


@dataclass
class ReaderAccessTelemetry:
    access_denied_retry_count: int = 0
    terminal_access_error_count: int = 0
    max_retry_depth: int = 0


def _read_bytes_with_access_retry(
    path: Path,
    telemetry: ReaderAccessTelemetry,
) -> bytes:
    started = time.monotonic()
    delay = READ_INITIAL_BACKOFF_SECONDS
    depth = 0

    while True:
        try:
            return path.read_bytes()
        except PermissionError as exc:
            if getattr(exc, "winerror", None) != 5:
                raise

            telemetry.access_denied_retry_count += 1
            depth += 1
            telemetry.max_retry_depth = max(
                telemetry.max_retry_depth,
                depth,
            )

            elapsed = time.monotonic() - started
            remaining = (
                READ_RETRY_DEADLINE_SECONDS
                - elapsed
            )
            if remaining <= 0:
                telemetry.terminal_access_error_count += 1
                raise ReaderAccessRetryDeadlineExceeded(
                    "reader access-denied retry deadline exceeded"
                ) from exc

            time.sleep(min(delay, remaining))
            delay = min(
                delay * 2,
                READ_MAX_BACKOFF_SECONDS,
            )


def validate_current_with_access_retry(
    sandbox: Path,
    telemetry: ReaderAccessTelemetry,
) -> dict[str, Any]:
    started = time.monotonic()
    delay = READ_INITIAL_BACKOFF_SECONDS
    depth = 0

    while True:
        try:
            return validate_current_pointer(sandbox)
        except (
            OpenPointerMissingError,
            OpenPointerMixedError,
        ):
            raise
        except OpenPointerPartialError as exc:
            if not _is_winerror_5(exc):
                raise

            telemetry.access_denied_retry_count += 1
            depth += 1
            telemetry.max_retry_depth = max(
                telemetry.max_retry_depth,
                depth,
            )

            elapsed = time.monotonic() - started
            remaining = (
                READ_RETRY_DEADLINE_SECONDS
                - elapsed
            )
            if remaining <= 0:
                telemetry.terminal_access_error_count += 1
                raise ReaderAccessRetryDeadlineExceeded(
                    "reader access-denied retry deadline exceeded"
                ) from exc

            time.sleep(min(delay, remaining))
            delay = min(
                delay * 2,
                READ_MAX_BACKOFF_SECONDS,
            )


@dataclass
class ReplaceRetryStats:
    attempts: int
    access_denied_conflicts: int
    elapsed_ms: float
    max_backoff_ms: float
    verification_read_access_denied_retries: int


def write_current_atomic_with_retry(
    sandbox: Path,
    generation_id: str,
    generation_digest: str,
    *,
    expected_old_generation_id: str,
) -> ReplaceRetryStats:
    pointer = sandbox / "CURRENT.md"
    temporary = sandbox / "CURRENT.tmp"

    if temporary.exists():
        raise ObsidianOpenRetryError(
            "CURRENT.tmp exists before retry promotion"
        )

    candidate = _current_note_bytes(
        generation_id,
        generation_digest,
    )
    candidate_sha = _sha256(candidate)

    with temporary.open("xb") as handle:
        handle.write(candidate)
        handle.flush()
        os.fsync(handle.fileno())

    if _sha256(temporary.read_bytes()) != candidate_sha:
        raise ObsidianOpenRetryError(
            "CURRENT.tmp integrity mismatch before replace"
        )

    started = time.monotonic()
    delay = WRITE_INITIAL_BACKOFF_SECONDS
    attempts = 0
    conflicts = 0
    max_backoff = 0.0
    verification_telemetry = ReaderAccessTelemetry()

    while True:
        attempts += 1
        try:
            os.replace(temporary, pointer)
            break
        except PermissionError as exc:
            if getattr(exc, "winerror", None) != 5:
                raise

            conflicts += 1

            if not temporary.is_file():
                raise ObsidianOpenRetryError(
                    "CURRENT.tmp missing after retryable replace failure"
                ) from exc

            if _sha256(temporary.read_bytes()) != candidate_sha:
                raise ObsidianOpenRetryError(
                    "CURRENT.tmp changed after retryable replace failure"
                ) from exc

            current = validate_current_with_access_retry(
                sandbox,
                verification_telemetry,
            )
            if (
                current["generation_id"]
                != expected_old_generation_id
            ):
                raise ObsidianOpenRetryError(
                    "CURRENT changed despite failed atomic replace"
                ) from exc

            elapsed = time.monotonic() - started
            remaining = (
                WRITE_RETRY_DEADLINE_SECONDS
                - elapsed
            )
            if remaining <= 0:
                raise ReplaceRetryDeadlineExceeded(
                    "atomic replace access-denied retry deadline exceeded"
                ) from exc

            sleep_seconds = min(
                delay,
                remaining,
            )
            max_backoff = max(
                max_backoff,
                sleep_seconds,
            )
            time.sleep(sleep_seconds)
            delay = min(
                delay * 2,
                WRITE_MAX_BACKOFF_SECONDS,
            )

    elapsed_ms = (
        time.monotonic() - started
    ) * 1000.0

    if temporary.exists():
        raise ObsidianOpenRetryError(
            "CURRENT.tmp remains after successful replace"
        )

    observed = _read_bytes_with_access_retry(
        pointer,
        verification_telemetry,
    )
    if observed != candidate:
        raise ObsidianOpenRetryError(
            "successful CURRENT replace bytes differ from candidate"
        )

    current = validate_current_with_access_retry(
        sandbox,
        verification_telemetry,
    )
    if current["generation_id"] != generation_id:
        raise ObsidianOpenRetryError(
            "successful CURRENT replace generation mismatch"
        )
    if (
        current["generation_tree_digest_sha256"]
        != generation_digest
    ):
        raise ObsidianOpenRetryError(
            "successful CURRENT replace digest mismatch"
        )

    return ReplaceRetryStats(
        attempts=attempts,
        access_denied_conflicts=conflicts,
        elapsed_ms=round(elapsed_ms, 6),
        max_backoff_ms=round(
            max_backoff * 1000.0,
            6,
        ),
        verification_read_access_denied_retries=(
            verification_telemetry.access_denied_retry_count
        ),
    )


def recover_failed_p5c3(
    snapshot_path: Path,
) -> dict[str, Any]:
    verify_retry_contract(
        Path(__file__).resolve().parent
    )
    payload, token = _load_snapshot(snapshot_path)

    if obsidian_running():
        raise ObsidianOpenRetryError(
            "Obsidian must be closed during P5-C3R recovery"
        )

    if payload.get("schema") != SNAPSHOT_SCHEMA:
        raise ObsidianOpenRetryError(
            "snapshot schema mismatch"
        )
    if payload.get("sandbox_path") != str(
        SANDBOX_VAULT
    ):
        raise ObsidianOpenRetryError(
            "snapshot sandbox mismatch"
        )

    _require_snapshot_live_digests(payload)
    _require_generation_immutability(payload)

    telemetry = ReaderAccessTelemetry()
    current = validate_current_with_access_retry(
        SANDBOX_VAULT,
        telemetry,
    )
    if current["generation_id"] != "GEN_A":
        raise ObsidianOpenRetryError(
            "recovery requires CURRENT GEN_A"
        )

    temporary = SANDBOX_VAULT / "CURRENT.tmp"
    stale_temp_action = "ABSENT"

    if temporary.exists():
        expected = _current_note_bytes(
            "GEN_B",
            payload[
                "generation_content_digests"
            ]["GEN_B"],
        )
        actual = temporary.read_bytes()
        if actual != expected:
            raise ObsidianOpenRetryError(
                "stale CURRENT.tmp does not match expected failed GEN_B candidate"
            )
        temporary.unlink()
        stale_temp_action = "VERIFIED_AND_REMOVED"

    if temporary.exists():
        raise ObsidianOpenRetryError(
            "CURRENT.tmp remains after recovery"
        )

    current_after = validate_current_with_access_retry(
        SANDBOX_VAULT,
        telemetry,
    )
    if current_after["generation_id"] != "GEN_A":
        raise ObsidianOpenRetryError(
            "CURRENT changed during recovery"
        )

    _require_generation_immutability(payload)
    _require_snapshot_live_digests(payload)

    report = {
        "schema": RECOVERY_SCHEMA,
        "status": "PASS",
        "snapshot_token": token,
        "sandbox_path": str(SANDBOX_VAULT),
        "current_generation": "GEN_A",
        "stale_temp_action": stale_temp_action,
        "reader_access_denied_retry_count":
            telemetry.access_denied_retry_count,
        "live_vault_modified": False,
        "generation_rebuild_performed": False,
        "production_promotion_authorized": False,
        "continuous_observer_authorized": False,
    }
    event_log = _append_event(report)
    report["append_only_event_log"] = str(event_log)
    return report


def _open_no_delete_share(path: Path) -> int:
    if os.name != "nt":
        raise ObsidianOpenRetryError(
            "synthetic lock breaker requires Windows"
        )

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )
    create_file = kernel32.CreateFileW
    create_file.argtypes = (
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    )
    create_file.restype = ctypes.c_void_p

    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x00000080

    handle = create_file(
        str(path),
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )

    invalid = ctypes.c_void_p(-1).value
    if handle in (None, invalid):
        error = ctypes.get_last_error()
        raise ObsidianOpenRetryError(
            f"synthetic lock CreateFileW failed: {error}"
        )
    return int(handle)


def _close_handle(handle: int) -> None:
    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )
    close = kernel32.CloseHandle
    close.argtypes = (ctypes.c_void_p,)
    close.restype = ctypes.c_int

    if not close(ctypes.c_void_p(handle)):
        error = ctypes.get_last_error()
        raise ObsidianOpenRetryError(
            f"synthetic lock CloseHandle failed: {error}"
        )


def run_synthetic_lock_breaker() -> dict[str, Any]:
    verify_retry_contract(
        Path(__file__).resolve().parent
    )

    if os.name != "nt":
        raise ObsidianOpenRetryError(
            "synthetic Windows lock breaker requires Windows"
        )

    with tempfile.TemporaryDirectory(
        prefix="ATDS-P5C3R-LOCK-"
    ) as td:
        root = Path(td)
        generations = root / "generations"
        generations.mkdir()

        manifests: dict[str, dict[str, Any]] = {}
        for generation_id in ("GEN_A", "GEN_B"):
            manifests[generation_id] = (
                build_markdown_generation(
                    generations / generation_id,
                    generation_id,
                )
            )

        write_current_atomic(
            root,
            "GEN_A",
            manifests["GEN_A"][
                "generation_tree_digest_sha256"
            ],
        )

        handle = _open_no_delete_share(
            root / "CURRENT.md"
        )
        released = threading.Event()
        close_error: list[str] = []

        def release_lock() -> None:
            try:
                time.sleep(0.200)
                _close_handle(handle)
            except Exception as exc:
                close_error.append(
                    f"{type(exc).__name__}: {exc}"
                )
            finally:
                released.set()

        thread = threading.Thread(
            target=release_lock,
            daemon=True,
        )
        thread.start()

        stats = write_current_atomic_with_retry(
            root,
            "GEN_B",
            manifests["GEN_B"][
                "generation_tree_digest_sha256"
            ],
            expected_old_generation_id="GEN_A",
        )

        thread.join(timeout=5.0)
        if not released.is_set():
            raise ObsidianOpenRetryError(
                "synthetic lock release thread timeout"
            )
        if close_error:
            raise ObsidianOpenRetryError(
                close_error[0]
            )

        current = validate_current_pointer(root)
        if current["generation_id"] != "GEN_B":
            raise ObsidianOpenRetryError(
                "synthetic lock breaker final generation mismatch"
            )
        if stats.access_denied_conflicts <= 0:
            raise ObsidianOpenRetryError(
                "synthetic lock breaker observed zero access-denied conflicts"
            )
        if (root / "CURRENT.tmp").exists():
            raise ObsidianOpenRetryError(
                "synthetic lock breaker left CURRENT.tmp"
            )

        report = {
            "schema": LOCK_BREAKER_SCHEMA,
            "status": "PASS",
            "lock_release_delay_ms": 200,
            "replace_stats": asdict(stats),
            "final_generation": "GEN_B",
            "stale_temp_present": False,
            "production_promotion_authorized": False,
        }
        return report


@dataclass
class RetryReaderMetrics:
    samples: int = 0
    mixed_generation_count: int = 0
    missing_entrypoint_count: int = 0
    semantic_partial_generation_count: int = 0
    parse_error_count: int = 0
    terminal_reader_access_error_count: int = 0


class RetryReaderProbe:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.metrics = RetryReaderMetrics()
        self.access = ReaderAccessTelemetry()

    def start(self) -> None:
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="P5C3RRetryReader",
        )
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            started = time.perf_counter()
            try:
                validate_current_with_access_retry(
                    SANDBOX_VAULT,
                    self.access,
                )
            except OpenPointerMissingError:
                self.metrics.missing_entrypoint_count += 1
            except OpenPointerMixedError:
                self.metrics.mixed_generation_count += 1
            except ReaderAccessRetryDeadlineExceeded:
                self.metrics.terminal_reader_access_error_count += 1
            except OpenPointerPartialError:
                self.metrics.semantic_partial_generation_count += 1
            except Exception:
                self.metrics.parse_error_count += 1
            finally:
                self.metrics.samples += 1

            elapsed = time.perf_counter() - started
            delay = READER_INTERVAL_SECONDS - elapsed
            if delay > 0:
                time.sleep(delay)

    def wait_for_progress(
        self,
        baseline: int,
        *,
        timeout_seconds: float = 10.0,
    ) -> None:
        deadline = time.monotonic() + timeout_seconds
        while self.metrics.samples <= baseline:
            if time.monotonic() >= deadline:
                raise ObsidianOpenRetryError(
                    "reader did not progress during retry promotion"
                )
            time.sleep(0.0005)

    def wait_for_samples(
        self,
        minimum: int,
        *,
        timeout_seconds: float = 300.0,
    ) -> None:
        deadline = time.monotonic() + timeout_seconds
        while self.metrics.samples < minimum:
            if time.monotonic() >= deadline:
                raise ObsidianOpenRetryError(
                    "reader sample target timeout"
                )
            time.sleep(0.01)

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            if self._thread.is_alive():
                raise ObsidianOpenRetryError(
                    "retry reader thread did not stop"
                )


def run_retry_open_experiment(
    snapshot_path: Path,
) -> dict[str, Any]:
    verify_retry_contract(
        Path(__file__).resolve().parent
    )
    payload, token = _load_snapshot(snapshot_path)

    if payload.get("schema") != SNAPSHOT_SCHEMA:
        raise ObsidianOpenRetryError(
            "snapshot schema mismatch"
        )
    if payload.get("sandbox_path") != str(
        SANDBOX_VAULT
    ):
        raise ObsidianOpenRetryError(
            "snapshot sandbox mismatch"
        )
    if not obsidian_running():
        raise ObsidianOpenRetryError(
            "Obsidian must be running during P5-C3R open experiment"
        )
    if (SANDBOX_VAULT / "CURRENT.tmp").exists():
        raise ObsidianOpenRetryError(
            "CURRENT.tmp exists before P5-C3R open experiment"
        )

    obsidian_state_before = _safe_obsidian_state(
        SANDBOX_VAULT,
        require_workspace_current=True,
    )
    _require_snapshot_live_digests(payload)
    _require_generation_immutability(payload)

    start_read_telemetry = ReaderAccessTelemetry()
    current_start = validate_current_with_access_retry(
        SANDBOX_VAULT,
        start_read_telemetry,
    )
    if current_start["generation_id"] != "GEN_A":
        raise ObsidianOpenRetryError(
            "P5-C3R open experiment must start at GEN_A"
        )

    reader = RetryReaderProbe()
    reader.start()

    completed = 0
    terminal_pointer_write_error_count = 0
    retry_deadline_exceeded_count = 0
    total_replace_attempts = 0
    total_access_denied_conflicts = 0
    total_verification_read_retries = 0
    max_retry_depth = 0
    max_promotion_latency_ms = 0.0
    failure_phase: str | None = None
    failure_cycle: int | None = None
    failure_type: str | None = None
    failure_message: str | None = None
    samples_at_start = reader.metrics.samples

    try:
        for cycle in range(PROMOTION_CYCLES):
            if (
                cycle % 25 == 0
                and not obsidian_running()
            ):
                raise ObsidianOpenRetryError(
                    "Obsidian stopped during P5-C3R open experiment"
                )

            target = (
                "GEN_B"
                if cycle % 2 == 0
                else "GEN_A"
            )
            old = (
                "GEN_A"
                if target == "GEN_B"
                else "GEN_B"
            )
            before_samples = reader.metrics.samples

            try:
                stats = write_current_atomic_with_retry(
                    SANDBOX_VAULT,
                    target,
                    payload[
                        "generation_content_digests"
                    ][target],
                    expected_old_generation_id=old,
                )
            except ReplaceRetryDeadlineExceeded:
                retry_deadline_exceeded_count += 1
                terminal_pointer_write_error_count += 1
                raise
            except Exception:
                terminal_pointer_write_error_count += 1
                raise

            completed += 1
            total_replace_attempts += stats.attempts
            total_access_denied_conflicts += (
                stats.access_denied_conflicts
            )
            total_verification_read_retries += (
                stats.verification_read_access_denied_retries
            )
            max_retry_depth = max(
                max_retry_depth,
                stats.access_denied_conflicts,
            )
            max_promotion_latency_ms = max(
                max_promotion_latency_ms,
                stats.elapsed_ms,
            )

            reader.wait_for_progress(
                before_samples
            )

        samples_after_promotions = reader.metrics.samples
        reader.wait_for_samples(
            MIN_READER_SAMPLES
        )
    except Exception as exc:
        failure_phase = "PROMOTION_LOOP"
        failure_cycle = completed
        failure_type = type(exc).__name__
        failure_message = str(exc)
    finally:
        reader.stop()

    current_end: dict[str, Any] | None = None
    postcondition_failure_gate: str | None = None

    try:
        if not obsidian_running():
            raise ObsidianOpenRetryError(
                "Obsidian is not running at end of P5-C3R open experiment"
            )
        _safe_obsidian_state(
            SANDBOX_VAULT,
            require_workspace_current=True,
        )
        _require_generation_immutability(payload)
        _require_snapshot_live_digests(payload)
        end_telemetry = ReaderAccessTelemetry()
        current_end = validate_current_with_access_retry(
            SANDBOX_VAULT,
            end_telemetry,
        )
        if (SANDBOX_VAULT / "CURRENT.tmp").exists():
            raise ObsidianOpenRetryError(
                "CURRENT.tmp remains after P5-C3R open experiment"
            )
    except Exception as exc:
        postcondition_failure_gate = type(exc).__name__
        if failure_type is None:
            failure_phase = "POSTCONDITION"
            failure_cycle = completed
            failure_type = type(exc).__name__
            failure_message = str(exc)

    metrics = reader.metrics
    samples_during_promotions = (
        samples_after_promotions - samples_at_start
        if "samples_after_promotions" in locals()
        else metrics.samples - samples_at_start
    )

    semantic_zero = (
        metrics.mixed_generation_count == 0
        and metrics.missing_entrypoint_count == 0
        and metrics.semantic_partial_generation_count == 0
        and metrics.parse_error_count == 0
        and metrics.terminal_reader_access_error_count == 0
    )

    passed = (
        failure_type is None
        and postcondition_failure_gate is None
        and completed == PROMOTION_CYCLES
        and metrics.samples >= MIN_READER_SAMPLES
        and samples_during_promotions >= PROMOTION_CYCLES
        and terminal_pointer_write_error_count == 0
        and retry_deadline_exceeded_count == 0
        and semantic_zero
        and current_end is not None
        and current_end["generation_id"] == "GEN_A"
    )

    report = {
        "schema": RETRY_METRICS_SCHEMA,
        "status":
            "PASS_AUTOMATED_OPEN_RETRY_EXPERIMENT"
            if passed
            else "FAIL",
        "snapshot_token": token,
        "sandbox_path": str(SANDBOX_VAULT),
        "cycles_requested": PROMOTION_CYCLES,
        "cycles_completed": completed,
        "samples": metrics.samples,
        "samples_during_promotions":
            samples_during_promotions,
        "terminal_pointer_write_error_count":
            terminal_pointer_write_error_count,
        "retry_deadline_exceeded_count":
            retry_deadline_exceeded_count,
        "total_replace_attempts":
            total_replace_attempts,
        "access_denied_retry_conflict_count":
            total_access_denied_conflicts,
        "max_retry_depth":
            max_retry_depth,
        "max_promotion_latency_ms":
            round(max_promotion_latency_ms, 6),
        "verification_read_access_denied_retry_count":
            total_verification_read_retries,
        "reader_access_denied_retry_count":
            reader.access.access_denied_retry_count,
        "reader_max_retry_depth":
            reader.access.max_retry_depth,
        "reader_terminal_access_error_count":
            metrics.terminal_reader_access_error_count,
        "mixed_generation_count":
            metrics.mixed_generation_count,
        "missing_entrypoint_count":
            metrics.missing_entrypoint_count,
        "semantic_partial_generation_count":
            metrics.semantic_partial_generation_count,
        "parse_error_count":
            metrics.parse_error_count,
        "failure_phase": failure_phase,
        "failure_cycle": failure_cycle,
        "failure_type": failure_type,
        "failure_message": failure_message,
        "postcondition_failure_gate":
            postcondition_failure_gate,
        "final_generation_id": (
            None
            if current_end is None
            else current_end["generation_id"]
        ),
        "final_generation_tree_digest_sha256": (
            None
            if current_end is None
            else current_end[
                "generation_tree_digest_sha256"
            ]
        ),
        "manual_visual_acceptance_required": True,
        "manual_visual_acceptance_pending":
            passed,
        "expected_visible_note": "CURRENT.md",
        "expected_visible_generation": "GEN_A",
        "expected_visible_link":
            "generations/GEN_A/INDEX",
        "live_vault_modified": False,
        "obsidian_open_retry_qualified": False,
        "production_promotion_authorized": False,
        "continuous_observer_authorized": False,
    }

    event_log = _append_event(report)
    report["append_only_event_log"] = str(event_log)
    return report


def post_close_retry_verify(
    snapshot_path: Path,
    *,
    manual_visual_accepted: bool,
) -> dict[str, Any]:
    verify_retry_contract(
        Path(__file__).resolve().parent
    )
    payload, token = _load_snapshot(snapshot_path)

    if not manual_visual_accepted:
        raise ObsidianOpenRetryError(
            "manual visual acceptance not supplied"
        )
    if obsidian_running():
        raise ObsidianOpenRetryError(
            "Obsidian must be fully closed before P5-C3R post-close verify"
        )
    if (SANDBOX_VAULT / "CURRENT.tmp").exists():
        raise ObsidianOpenRetryError(
            "CURRENT.tmp present during P5-C3R post-close verify"
        )

    _safe_obsidian_state(
        SANDBOX_VAULT,
        require_workspace_current=True,
    )
    _require_generation_immutability(payload)
    _require_snapshot_live_digests(payload)

    telemetry = ReaderAccessTelemetry()
    current = validate_current_with_access_retry(
        SANDBOX_VAULT,
        telemetry,
    )
    if current["generation_id"] != "GEN_A":
        raise ObsidianOpenRetryError(
            "P5-C3R post-close final generation is not GEN_A"
        )

    report = {
        "schema": POST_CLOSE_SCHEMA,
        "status": "PASS",
        "snapshot_token": token,
        "manual_visual_acceptance": True,
        "final_generation_id": "GEN_A",
        "reader_access_denied_retry_count":
            telemetry.access_denied_retry_count,
        "obsidian_open_retry_qualified": True,
        "p5c3r_qualified": True,
        "live_vault_modified": False,
        "production_promotion_authorized": False,
        "continuous_observer_authorized": False,
        "graph_current_pointer_semantics_qualified": False,
    }
    event_log = _append_event(report)
    report["append_only_event_log"] = str(event_log)
    return report
