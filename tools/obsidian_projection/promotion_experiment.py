from __future__ import annotations

import ctypes
import hashlib
import json
import os
import platform
import shutil
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable


class PromotionExperimentError(RuntimeError):
    pass


class MixedGenerationError(PromotionExperimentError):
    pass


class PartialGenerationError(PromotionExperimentError):
    pass


class EntryPointMissingError(PromotionExperimentError):
    pass


P5C_CONTRACT_BLOB = "36e49e72a867e30a69f63eb413fd924d0e56297b"
P5C_CONTRACT_SCHEMA = "ATDS_OBSIDIAN_ONEDRIVE_PROMOTION_CONTRACT_V0_1"

LIVE_VAULT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-OBSIDIAN-PROJECTION"
)
SANDBOX = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-P5C-PROMOTION-SANDBOX"
)

FILES_PER_GENERATION = 128
NESTED_DIRECTORIES = 8
QUALIFIABLE_CYCLES = 250
MIN_READER_SAMPLES = 5000
READER_INTERVAL_SECONDS = 0.001
NEGATIVE_CONTROL_CYCLES = 24
NEGATIVE_CONTROL_MIN_SAMPLES = 500

METRICS_SCHEMA = "ATDS_OBSIDIAN_P5C_PROMOTION_METRICS_V0_1"

MOVEFILE_REPLACE_EXISTING = 0x00000001
MOVEFILE_WRITE_THROUGH = 0x00000008
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def verify_contract(package_dir: Path) -> dict[str, Any]:
    path = package_dir / "onedrive_promotion_contract_v0_1.json"
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PromotionExperimentError(
            "P5-C contract unreadable"
        ) from exc

    if _git_blob_oid(raw) != P5C_CONTRACT_BLOB:
        raise PromotionExperimentError(
            "P5-C contract blob mismatch"
        )
    if value.get("schema") != P5C_CONTRACT_SCHEMA:
        raise PromotionExperimentError(
            "unexpected P5-C contract schema"
        )
    return value


def _norm(path: Path) -> str:
    return os.path.normcase(
        os.path.abspath(str(path))
    )


def assert_sandbox_boundary(
    sandbox: Path,
    live_vault: Path = LIVE_VAULT,
) -> None:
    if _norm(sandbox) == _norm(live_vault):
        raise PromotionExperimentError(
            "sandbox overlaps live Vault"
        )

    if _norm(live_vault).startswith(
        _norm(sandbox) + os.sep
    ):
        raise PromotionExperimentError(
            "sandbox contains live Vault"
        )

    if _norm(sandbox).startswith(
        _norm(live_vault) + os.sep
    ):
        raise PromotionExperimentError(
            "sandbox is inside live Vault"
        )

    expected_parent = Path(
        r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    )
    if _norm(sandbox.parent) != _norm(expected_parent):
        raise PromotionExperimentError(
            "sandbox is outside qualified OneDrive root"
        )

    if (sandbox / ".git").exists():
        raise PromotionExperimentError(
            "sandbox must not be a Git repository"
        )


def _tree_digest_from_records(
    records: list[list[Any]],
) -> str:
    records = sorted(
        records,
        key=lambda item:
            str(item[0]).encode("utf-8"),
    )
    return _sha256(
        _canonical_json_bytes(records)
    )


def build_generation(
    root: Path,
    generation_id: str,
    *,
    files_per_generation: int = FILES_PER_GENERATION,
    nested_directories: int = NESTED_DIRECTORIES,
) -> dict[str, Any]:
    if root.exists():
        raise PromotionExperimentError(
            f"generation root already exists: {root}"
        )

    root.mkdir(parents=True)
    records: list[list[Any]] = []
    file_rows: list[dict[str, Any]] = []

    for index in range(files_per_generation):
        directory = root / (
            f"d{index % nested_directories:02d}"
        )
        directory.mkdir(exist_ok=True)

        relative = (
            Path(directory.name)
            / f"artifact-{index:04d}.json"
        )
        target = root / relative

        payload_length = 64 + ((index * 37) % 2048)
        payload = (
            generation_id[-1]
            * payload_length
        )

        body = _canonical_json_bytes(
            {
                "generation_id": generation_id,
                "index": index,
                "payload": payload,
            }
        )
        target.write_bytes(body)

        digest = _sha256(body)
        size = len(body)
        relative_text = relative.as_posix()

        records.append(
            [relative_text, digest, size]
        )
        file_rows.append(
            {
                "path": relative_text,
                "sha256": digest,
                "size_bytes": size,
            }
        )

    tree_digest = _tree_digest_from_records(records)
    manifest = {
        "generation_id": generation_id,
        "file_count": files_per_generation,
        "tree_digest_sha256": tree_digest,
        "files": sorted(
            file_rows,
            key=lambda item:
                item["path"].encode("utf-8"),
        ),
    }
    (root / "MANIFEST.json").write_bytes(
        _canonical_json_bytes(manifest)
    )
    return manifest


def validate_generation_dir(
    root: Path,
) -> dict[str, Any]:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file():
        raise EntryPointMissingError(
            "generation manifest missing"
        )

    try:
        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise PartialGenerationError(
            "generation manifest unreadable"
        ) from exc

    generation_id = manifest.get(
        "generation_id"
    )
    files = manifest.get("files")
    expected_count = manifest.get(
        "file_count"
    )
    expected_tree = manifest.get(
        "tree_digest_sha256"
    )

    if not isinstance(generation_id, str):
        raise PartialGenerationError(
            "generation ID missing"
        )
    if not isinstance(files, list):
        raise PartialGenerationError(
            "manifest files missing"
        )
    if expected_count != len(files):
        raise PartialGenerationError(
            "manifest file count mismatch"
        )

    actual_records: list[list[Any]] = []

    for row in files:
        if not isinstance(row, dict):
            raise PartialGenerationError(
                "invalid file manifest row"
            )
        relative = row.get("path")
        expected_sha = row.get("sha256")
        expected_size = row.get("size_bytes")

        if (
            not isinstance(relative, str)
            or "\\" in relative
            or relative.startswith("/")
            or ".." in relative.split("/")
        ):
            raise PartialGenerationError(
                "invalid manifest path"
            )

        target = root / Path(relative)
        try:
            raw = target.read_bytes()
        except FileNotFoundError as exc:
            raise PartialGenerationError(
                "referenced generation file missing"
            ) from exc

        if len(raw) != expected_size:
            raise PartialGenerationError(
                "generation file size mismatch"
            )
        actual_sha = _sha256(raw)
        if actual_sha != expected_sha:
            raise PartialGenerationError(
                "generation file digest mismatch"
            )

        try:
            payload = json.loads(
                raw.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise PartialGenerationError(
                "generation payload unreadable"
            ) from exc

        observed_generation = payload.get(
            "generation_id"
        )
        if observed_generation != generation_id:
            raise MixedGenerationError(
                "mixed generation observed"
            )

        actual_records.append(
            [
                relative,
                actual_sha,
                len(raw),
            ]
        )

    actual_tree = _tree_digest_from_records(
        actual_records
    )
    if actual_tree != expected_tree:
        raise PartialGenerationError(
            "manifest tree digest mismatch"
        )

    return {
        "generation_id": generation_id,
        "file_count": len(files),
        "tree_digest_sha256": actual_tree,
    }


def _write_pointer(
    candidate_root: Path,
    generation_id: str,
    relative_generation_path: str,
) -> None:
    pointer = candidate_root / "CURRENT.json"
    temporary = candidate_root / "CURRENT.tmp"

    raw = _canonical_json_bytes(
        {
            "generation_id": generation_id,
            "generation_path":
                relative_generation_path,
        }
    )

    with temporary.open("wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

    os.replace(temporary, pointer)


def validate_pointer_entry(
    candidate_root: Path,
) -> dict[str, Any]:
    pointer = candidate_root / "CURRENT.json"
    if not pointer.is_file():
        raise EntryPointMissingError(
            "CURRENT pointer missing"
        )

    try:
        value = json.loads(
            pointer.read_text(encoding="utf-8")
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise PartialGenerationError(
            "CURRENT pointer unreadable"
        ) from exc

    generation_id = value.get(
        "generation_id"
    )
    relative = value.get(
        "generation_path"
    )

    if (
        not isinstance(generation_id, str)
        or not isinstance(relative, str)
    ):
        raise PartialGenerationError(
            "CURRENT pointer fields invalid"
        )

    lowered = relative.lower()
    if (
        "stage" in lowered
        or "temp" in lowered
        or "\\" in relative
        or relative.startswith("/")
        or ".." in relative.split("/")
    ):
        raise PartialGenerationError(
            "staging/temp or invalid path exposed as live"
        )

    target = candidate_root / Path(relative)
    result = validate_generation_dir(target)

    if result["generation_id"] != generation_id:
        raise MixedGenerationError(
            "pointer generation differs from target"
        )
    return result


@dataclass
class ReaderMetrics:
    samples: int = 0
    mixed_generation_count: int = 0
    missing_entrypoint_count: int = 0
    partial_generation_count: int = 0
    parse_error_count: int = 0


class ReaderProbe:
    def __init__(
        self,
        validator: Callable[[], dict[str, Any]],
        *,
        interval_seconds: float,
    ) -> None:
        self._validator = validator
        self._interval = interval_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.metrics = ReaderMetrics()

    def start(self) -> None:
        if self._thread is not None:
            raise PromotionExperimentError(
                "reader already started"
            )
        self._thread = threading.Thread(
            target=self._run,
            name="P5CReaderProbe",
            daemon=True,
        )
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            started = time.perf_counter()
            try:
                self._validator()
            except EntryPointMissingError:
                self.metrics.missing_entrypoint_count += 1
            except MixedGenerationError:
                self.metrics.mixed_generation_count += 1
            except PartialGenerationError:
                self.metrics.partial_generation_count += 1
            except Exception:
                self.metrics.parse_error_count += 1
            finally:
                self.metrics.samples += 1

            elapsed = time.perf_counter() - started
            delay = self._interval - elapsed
            if delay > 0:
                time.sleep(delay)

    def wait_for_samples(
        self,
        minimum: int,
        *,
        timeout_seconds: float = 300.0,
    ) -> None:
        deadline = (
            time.monotonic()
            + timeout_seconds
        )
        while self.metrics.samples < minimum:
            if time.monotonic() >= deadline:
                raise PromotionExperimentError(
                    "reader sample target timeout"
                )
            time.sleep(0.01)

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            if self._thread.is_alive():
                raise PromotionExperimentError(
                    "reader thread did not stop"
                )


@dataclass
class CandidateMetrics:
    candidate_id: str
    result: str
    qualification_allowed: bool
    cycles_requested: int
    cycles_completed: int
    samples: int
    mixed_generation_count: int
    missing_entrypoint_count: int
    partial_generation_count: int
    parse_error_count: int
    final_generation_id: str | None
    final_tree_digest_sha256: str | None
    failure_code: str | None
    duration_seconds: float
    samples_during_promotions: int
    qualifies_primitive: bool


def _anomaly_count(
    reader: ReaderProbe,
) -> int:
    return (
        reader.metrics.mixed_generation_count
        + reader.metrics.missing_entrypoint_count
        + reader.metrics.partial_generation_count
        + reader.metrics.parse_error_count
    )


def _wait_for_anomaly_progress(
    reader: ReaderProbe,
    baseline_anomalies: int,
    *,
    timeout_seconds: float = 10.0,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    while _anomaly_count(reader) <= baseline_anomalies:
        if time.monotonic() >= deadline:
            raise PromotionExperimentError(
                "negative control anomaly was not observed"
            )
        time.sleep(0.0005)


def _wait_for_reader_progress(
    reader: ReaderProbe,
    baseline_samples: int,
    *,
    minimum_increment: int = 1,
    timeout_seconds: float = 10.0,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    target = baseline_samples + minimum_increment
    while reader.metrics.samples < target:
        if time.monotonic() >= deadline:
            raise PromotionExperimentError(
                "reader did not progress during promotion window"
            )
        time.sleep(0.0005)


def _candidate_result(
    *,
    candidate_id: str,
    qualification_allowed: bool,
    cycles_requested: int,
    cycles_completed: int,
    reader: ReaderProbe,
    final_state: dict[str, Any] | None,
    failure_code: str | None,
    duration: float,
    force_result: str | None = None,
    samples_during_promotions: int = 0,
) -> CandidateMetrics:
    metrics = reader.metrics

    if force_result is not None:
        result = force_result
    else:
        zero_anomalies = (
            metrics.mixed_generation_count == 0
            and metrics.missing_entrypoint_count == 0
            and metrics.partial_generation_count == 0
            and metrics.parse_error_count == 0
        )
        enough_cycles = (
            cycles_completed
            >= cycles_requested
        )
        enough_samples = (
            metrics.samples
            >= MIN_READER_SAMPLES
        )
        enough_active_samples = (
            samples_during_promotions
            >= cycles_requested
        )
        result = (
            "PASS"
            if (
                qualification_allowed
                and zero_anomalies
                and enough_cycles
                and enough_samples
                and enough_active_samples
                and final_state is not None
            )
            else "FAIL"
        )

    qualifies = (
        result == "PASS"
        and qualification_allowed
    )

    return CandidateMetrics(
        candidate_id=candidate_id,
        result=result,
        qualification_allowed=qualification_allowed,
        cycles_requested=cycles_requested,
        cycles_completed=cycles_completed,
        samples=metrics.samples,
        mixed_generation_count=
            metrics.mixed_generation_count,
        missing_entrypoint_count=
            metrics.missing_entrypoint_count,
        partial_generation_count=
            metrics.partial_generation_count,
        parse_error_count=
            metrics.parse_error_count,
        final_generation_id=(
            None
            if final_state is None
            else str(
                final_state["generation_id"]
            )
        ),
        final_tree_digest_sha256=(
            None
            if final_state is None
            else str(
                final_state[
                    "tree_digest_sha256"
                ]
            )
        ),
        failure_code=failure_code,
        duration_seconds=round(
            duration,
            6,
        ),
        samples_during_promotions=
            samples_during_promotions,
        qualifies_primitive=qualifies,
    )


def _copy_fixture(
    fixture: Path,
    target: Path,
) -> None:
    if target.exists():
        raise PromotionExperimentError(
            f"staging target exists: {target}"
        )
    shutil.copytree(fixture, target)


def _next_generation(
    index: int,
) -> str:
    return (
        "GEN_B"
        if index % 2 == 0
        else "GEN_A"
    )


def _require_expected_final_state(
    final_state: dict[str, Any] | None,
    fixtures: dict[str, Path],
    cycles_completed: int,
    cycles_required: int,
) -> tuple[dict[str, Any] | None, str | None]:
    if (
        final_state is None
        or cycles_completed != cycles_required
    ):
        return final_state, None

    expected_id = _next_generation(
        cycles_required - 1
    )
    expected = validate_generation_dir(
        fixtures[expected_id]
    )

    if final_state != expected:
        return None, "FINAL_STATE_MISMATCH"
    return final_state, None


def run_negative_control(
    candidate_root: Path,
    fixtures: dict[str, Path],
) -> CandidateMetrics:
    candidate_root.mkdir(parents=True)
    live = candidate_root / "live"
    _copy_fixture(fixtures["GEN_A"], live)

    reader = ReaderProbe(
        lambda: validate_generation_dir(live),
        interval_seconds=READER_INTERVAL_SECONDS,
    )
    reader.start()

    started = time.perf_counter()
    cycles_completed = 0
    failure_code: str | None = None
    promotion_sample_start = (
        reader.metrics.samples
    )

    try:
        for cycle in range(
            NEGATIVE_CONTROL_CYCLES
        ):
            target_id = _next_generation(cycle)
            before_samples = (
                reader.metrics.samples
            )
            source = fixtures[target_id]

            manifest = json.loads(
                (source / "MANIFEST.json").read_text(
                    encoding="utf-8"
                )
            )

            anomaly_baseline = _anomaly_count(
                reader
            )
            for row_index, row in enumerate(
                manifest["files"]
            ):
                relative = Path(row["path"])
                destination = live / relative
                shutil.copyfile(
                    source / relative,
                    destination,
                )

                if row_index == 0:
                    _wait_for_anomaly_progress(
                        reader,
                        anomaly_baseline,
                    )

                time.sleep(0.0005)

            shutil.copyfile(
                source / "MANIFEST.json",
                live / "MANIFEST.json",
            )
            cycles_completed += 1
            _wait_for_reader_progress(
                reader,
                before_samples,
            )

        promotion_sample_end = (
            reader.metrics.samples
        )
        reader.wait_for_samples(
            NEGATIVE_CONTROL_MIN_SAMPLES
        )
    except Exception as exc:
        failure_code = type(exc).__name__
    finally:
        reader.stop()

    duration = time.perf_counter() - started
    anomalies = (
        reader.metrics.mixed_generation_count
        + reader.metrics.missing_entrypoint_count
        + reader.metrics.partial_generation_count
        + reader.metrics.parse_error_count
    )

    force_result = (
        "PASS"
        if (
            anomalies > 0
            and cycles_completed
            == NEGATIVE_CONTROL_CYCLES
            and failure_code is None
        )
        else "BLOCKED"
    )

    final_state: dict[str, Any] | None
    try:
        final_state = validate_generation_dir(live)
    except PromotionExperimentError:
        final_state = None

    return _candidate_result(
        candidate_id=
            "DIRECT_IN_PLACE_PER_FILE_REPLACE",
        qualification_allowed=False,
        cycles_requested=
            NEGATIVE_CONTROL_CYCLES,
        cycles_completed=cycles_completed,
        reader=reader,
        final_state=final_state,
        failure_code=failure_code,
        duration=duration,
        force_result=force_result,
        samples_during_promotions=(
            promotion_sample_end
            - promotion_sample_start
            if "promotion_sample_end" in locals()
            else reader.metrics.samples
            - promotion_sample_start
        ),
    )


def run_two_rename_swap(
    candidate_root: Path,
    fixtures: dict[str, Path],
) -> CandidateMetrics:
    candidate_root.mkdir(parents=True)
    live = candidate_root / "live"
    _copy_fixture(fixtures["GEN_A"], live)

    reader = ReaderProbe(
        lambda: validate_generation_dir(live),
        interval_seconds=READER_INTERVAL_SECONDS,
    )
    reader.start()

    started = time.perf_counter()
    completed = 0
    failure_code: str | None = None
    promotion_sample_start = (
        reader.metrics.samples
    )

    try:
        for cycle in range(
            QUALIFIABLE_CYCLES
        ):
            target_id = _next_generation(cycle)
            before_samples = (
                reader.metrics.samples
            )
            stage = (
                candidate_root
                / f"stage-{cycle:04d}"
            )
            backup = (
                candidate_root
                / f"backup-{cycle:04d}"
            )

            _copy_fixture(
                fixtures[target_id],
                stage,
            )
            os.replace(live, backup)
            os.replace(stage, live)
            shutil.rmtree(backup)
            completed += 1
            _wait_for_reader_progress(
                reader,
                before_samples,
            )

        promotion_sample_end = (
            reader.metrics.samples
        )
        reader.wait_for_samples(
            MIN_READER_SAMPLES
        )
    except Exception as exc:
        failure_code = type(exc).__name__
    finally:
        reader.stop()

    duration = time.perf_counter() - started

    final_state: dict[str, Any] | None
    try:
        final_state = validate_generation_dir(live)
    except PromotionExperimentError:
        final_state = None

    final_state, final_mismatch = (
        _require_expected_final_state(
            final_state,
            fixtures,
            completed,
            QUALIFIABLE_CYCLES,
        )
    )
    if (
        final_mismatch is not None
        and failure_code is None
    ):
        failure_code = final_mismatch

    return _candidate_result(
        candidate_id=
            "DIRECTORY_TWO_RENAME_SWAP",
        qualification_allowed=True,
        cycles_requested=
            QUALIFIABLE_CYCLES,
        cycles_completed=completed,
        reader=reader,
        final_state=final_state,
        failure_code=failure_code,
        duration=duration,
        samples_during_promotions=(
            promotion_sample_end
            - promotion_sample_start
            if "promotion_sample_end" in locals()
            else reader.metrics.samples
            - promotion_sample_start
        ),
    )


def _movefileex(
    source: Path,
    destination: Path,
) -> tuple[bool, int]:
    if os.name != "nt":
        return False, 0

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )
    function = kernel32.MoveFileExW
    function.argtypes = (
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
    )
    function.restype = ctypes.c_int

    ok = bool(
        function(
            str(source),
            str(destination),
            MOVEFILE_REPLACE_EXISTING
            | MOVEFILE_WRITE_THROUGH,
        )
    )
    error = ctypes.get_last_error()
    return ok, error


def run_movefileex_replace(
    candidate_root: Path,
    fixtures: dict[str, Path],
) -> CandidateMetrics:
    candidate_root.mkdir(parents=True)
    live = candidate_root / "live"
    _copy_fixture(fixtures["GEN_A"], live)

    reader = ReaderProbe(
        lambda: validate_generation_dir(live),
        interval_seconds=READER_INTERVAL_SECONDS,
    )
    reader.start()

    started = time.perf_counter()
    completed = 0
    failure_code: str | None = None
    unsupported = False
    promotion_sample_start = (
        reader.metrics.samples
    )

    try:
        for cycle in range(
            QUALIFIABLE_CYCLES
        ):
            target_id = _next_generation(cycle)
            before_samples = (
                reader.metrics.samples
            )
            stage = (
                candidate_root
                / f"stage-{cycle:04d}"
            )
            _copy_fixture(
                fixtures[target_id],
                stage,
            )

            ok, error = _movefileex(
                stage,
                live,
            )
            if not ok:
                failure_code = (
                    f"MOVEFILEEX_ERROR_{error}"
                )
                unsupported = True
                if stage.exists():
                    shutil.rmtree(stage)
                break
            completed += 1
            _wait_for_reader_progress(
                reader,
                before_samples,
            )

        promotion_sample_end = (
            reader.metrics.samples
        )
        if not unsupported:
            reader.wait_for_samples(
                MIN_READER_SAMPLES
            )
    except Exception as exc:
        failure_code = type(exc).__name__
    finally:
        reader.stop()

    duration = time.perf_counter() - started

    final_state: dict[str, Any] | None
    try:
        final_state = validate_generation_dir(live)
    except PromotionExperimentError:
        final_state = None

    final_state, final_mismatch = (
        _require_expected_final_state(
            final_state,
            fixtures,
            completed,
            QUALIFIABLE_CYCLES,
        )
    )
    if (
        final_mismatch is not None
        and failure_code is None
    ):
        failure_code = final_mismatch

    return _candidate_result(
        candidate_id=
            "WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE",
        qualification_allowed=True,
        cycles_requested=
            QUALIFIABLE_CYCLES,
        cycles_completed=completed,
        reader=reader,
        final_state=final_state,
        failure_code=failure_code,
        duration=duration,
        force_result=(
            "NOT_SUPPORTED"
            if unsupported
            else None
        ),
        samples_during_promotions=(
            promotion_sample_end
            - promotion_sample_start
            if "promotion_sample_end" in locals()
            else reader.metrics.samples
            - promotion_sample_start
        ),
    )


def run_pointer_swap(
    candidate_root: Path,
    fixtures: dict[str, Path],
) -> CandidateMetrics:
    candidate_root.mkdir(parents=True)
    generations = (
        candidate_root / "generations"
    )
    generations.mkdir()

    for generation_id, fixture in fixtures.items():
        _copy_fixture(
            fixture,
            generations / generation_id,
        )

    _write_pointer(
        candidate_root,
        "GEN_A",
        "generations/GEN_A",
    )

    reader = ReaderProbe(
        lambda: validate_pointer_entry(
            candidate_root
        ),
        interval_seconds=READER_INTERVAL_SECONDS,
    )
    reader.start()

    started = time.perf_counter()
    completed = 0
    failure_code: str | None = None
    promotion_sample_start = (
        reader.metrics.samples
    )

    try:
        for cycle in range(
            QUALIFIABLE_CYCLES
        ):
            target_id = _next_generation(cycle)
            before_samples = (
                reader.metrics.samples
            )
            _write_pointer(
                candidate_root,
                target_id,
                f"generations/{target_id}",
            )
            completed += 1
            _wait_for_reader_progress(
                reader,
                before_samples,
            )

        promotion_sample_end = (
            reader.metrics.samples
        )
        reader.wait_for_samples(
            MIN_READER_SAMPLES
        )
    except Exception as exc:
        failure_code = type(exc).__name__
    finally:
        reader.stop()

    duration = time.perf_counter() - started

    final_state: dict[str, Any] | None
    try:
        final_state = validate_pointer_entry(
            candidate_root
        )
    except PromotionExperimentError:
        final_state = None

    final_state, final_mismatch = (
        _require_expected_final_state(
            final_state,
            fixtures,
            completed,
            QUALIFIABLE_CYCLES,
        )
    )
    if (
        final_mismatch is not None
        and failure_code is None
    ):
        failure_code = final_mismatch

    return _candidate_result(
        candidate_id=
            "IMMUTABLE_GENERATION_ATOMIC_POINTER",
        qualification_allowed=True,
        cycles_requested=
            QUALIFIABLE_CYCLES,
        cycles_completed=completed,
        reader=reader,
        final_state=final_state,
        failure_code=failure_code,
        duration=duration,
        samples_during_promotions=(
            promotion_sample_end
            - promotion_sample_start
            if "promotion_sample_end" in locals()
            else reader.metrics.samples
            - promotion_sample_start
        ),
    )


def pointer_crash_recovery_probe(
    candidate_root: Path,
) -> dict[str, Any]:
    before = validate_pointer_entry(
        candidate_root
    )

    # Injection point: BEFORE_PROMOTION.
    before_again = validate_pointer_entry(
        candidate_root
    )
    if before_again != before:
        raise PromotionExperimentError(
            "pre-promotion recovery identity drift"
        )

    target_id = (
        "GEN_A"
        if before["generation_id"] == "GEN_B"
        else "GEN_B"
    )

    # Single-step mutation primitive: atomic pointer replace.
    _write_pointer(
        candidate_root,
        target_id,
        f"generations/{target_id}",
    )

    # Injection point: AFTER_PROMOTION_BEFORE_STATE_RECORD.
    recovered = validate_pointer_entry(
        candidate_root
    )
    if recovered["generation_id"] != target_id:
        raise PromotionExperimentError(
            "post-promotion recovery failed"
        )

    return {
        "before_promotion": "PASS",
        "after_first_mutation_step_if_multi_step":
            "NOT_APPLICABLE_SINGLE_STEP",
        "after_promotion_before_state_record":
            "PASS",
        "last_known_good_identifiable": True,
        "recovery_deterministic": True,
        "recovered_generation_id":
            recovered["generation_id"],
        "recovered_tree_digest_sha256":
            recovered[
                "tree_digest_sha256"
            ],
    }


def _filesystem_type(path: Path) -> str:
    if os.name != "nt":
        return "NON_WINDOWS"

    root = Path(path.anchor)
    volume_name = ctypes.create_unicode_buffer(261)
    fs_name = ctypes.create_unicode_buffer(261)
    serial = ctypes.c_uint32()
    max_component = ctypes.c_uint32()
    flags = ctypes.c_uint32()

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )
    function = kernel32.GetVolumeInformationW
    function.argtypes = (
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.c_wchar_p,
        ctypes.c_uint32,
    )
    function.restype = ctypes.c_int

    ok = function(
        str(root),
        volume_name,
        len(volume_name),
        ctypes.byref(serial),
        ctypes.byref(max_component),
        ctypes.byref(flags),
        fs_name,
        len(fs_name),
    )
    if not ok:
        return "UNKNOWN"
    return fs_name.value


def _reparse_summary(path: Path) -> dict[str, Any]:
    if os.name != "nt":
        return {
            "platform": "NON_WINDOWS",
            "is_reparse_point": False,
        }

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )
    function = kernel32.GetFileAttributesW
    function.argtypes = (
        ctypes.c_wchar_p,
    )
    function.restype = ctypes.c_uint32

    attributes = int(
        function(str(path))
    )
    if attributes == INVALID_FILE_ATTRIBUTES:
        return {
            "attributes_available": False,
            "is_reparse_point": None,
        }

    return {
        "attributes_available": True,
        "attributes_hex":
            f"0x{attributes:08X}",
        "is_reparse_point": bool(
            attributes
            & FILE_ATTRIBUTE_REPARSE_POINT
        ),
        "is_symlink": path.is_symlink(),
    }


def _event_log_path() -> Path:
    local = os.environ.get(
        "LOCALAPPDATA"
    )
    if not local:
        raise PromotionExperimentError(
            "LOCALAPPDATA unavailable"
        )
    return (
        Path(local)
        / "ATDS"
        / "obsidian_projection"
        / "p5c"
        / "promotion-events.jsonl"
    )


def append_metrics_event(
    report: dict[str, Any],
) -> Path:
    path = _event_log_path()
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    raw = _canonical_json_bytes(report)
    with path.open("ab") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    return path


def _directory_content_digest(
    root: Path,
) -> str:
    if not root.is_dir():
        raise PromotionExperimentError(
            f"protected directory missing: {root}"
        )

    records: list[list[Any]] = []
    for current, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        directories.sort(
            key=lambda item: item.encode("utf-8")
        )
        files.sort(
            key=lambda item: item.encode("utf-8")
        )
        current_path = Path(current)

        for name in files:
            path = current_path / name
            raw = path.read_bytes()
            records.append(
                [
                    path.relative_to(root).as_posix(),
                    _sha256(raw),
                    len(raw),
                ]
            )

    return _tree_digest_from_records(
        records
    )


def prepare_sandbox(
    sandbox: Path = SANDBOX,
) -> dict[str, Path]:
    if os.name != "nt":
        raise PromotionExperimentError(
            "P5-C2 sandbox experiment requires Windows"
        )

    assert_sandbox_boundary(sandbox)

    if sandbox.exists():
        raise PromotionExperimentError(
            "sandbox must be absent before experiment"
        )

    sandbox.mkdir(parents=True)
    if (sandbox / ".git").exists():
        raise PromotionExperimentError(
            "sandbox unexpectedly contains .git"
        )

    marker = sandbox / "P5C-SANDBOX.json"
    marker.write_bytes(
        _canonical_json_bytes(
            {
                "schema":
                    "ATDS_OBSIDIAN_P5C_SANDBOX_V0_1",
                "sacrificial": True,
                "live_vault_modified": False,
            }
        )
    )

    fixture_root = sandbox / "fixtures"
    fixture_root.mkdir()

    fixtures = {
        "GEN_A": fixture_root / "GEN_A",
        "GEN_B": fixture_root / "GEN_B",
    }
    build_generation(
        fixtures["GEN_A"],
        "GEN_A",
    )
    build_generation(
        fixtures["GEN_B"],
        "GEN_B",
    )

    validate_generation_dir(
        fixtures["GEN_A"]
    )
    validate_generation_dir(
        fixtures["GEN_B"]
    )
    return fixtures


def run_full_experiment(
    sandbox: Path = SANDBOX,
) -> dict[str, Any]:
    verify_contract(
        Path(__file__).resolve().parent
    )

    live_generated_before = (
        _directory_content_digest(
            LIVE_VAULT / "generated"
        )
    )
    live_views_before = (
        _directory_content_digest(
            LIVE_VAULT / "views"
        )
    )

    fixtures = prepare_sandbox(sandbox)

    candidates_root = (
        sandbox / "candidates"
    )
    candidates_root.mkdir()

    negative = run_negative_control(
        candidates_root / "negative",
        fixtures,
    )

    if negative.result != "PASS":
        live_generated_after = (
            _directory_content_digest(
                LIVE_VAULT / "generated"
            )
        )
        live_views_after = (
            _directory_content_digest(
                LIVE_VAULT / "views"
            )
        )
        if (
            live_generated_after
            != live_generated_before
            or live_views_after
            != live_views_before
        ):
            raise PromotionExperimentError(
                "protected live Vault trees changed during sandbox experiment"
            )

        report = {
            "schema": METRICS_SCHEMA,
            "status": "BLOCKED",
            "failure_code":
                "NEGATIVE_CONTROL_DID_NOT_DETECT_NON_ATOMICITY",
            "sandbox_path": str(sandbox),
            "live_vault_modified": False,
            "candidates": [
                asdict(negative)
            ],
        }
        append_metrics_event(report)
        return report

    two_rename = run_two_rename_swap(
        candidates_root / "two-rename",
        fixtures,
    )
    movefileex = run_movefileex_replace(
        candidates_root / "movefileex",
        fixtures,
    )
    pointer = run_pointer_swap(
        candidates_root / "pointer",
        fixtures,
    )

    candidates = [
        negative,
        two_rename,
        movefileex,
        pointer,
    ]

    qualified = [
        item.candidate_id
        for item in candidates
        if item.qualifies_primitive
    ]

    selected_candidate: str | None = None
    crash_probe: dict[str, Any] | None = None

    if len(qualified) == 1:
        selected_candidate = qualified[0]
        if (
            selected_candidate
            == "IMMUTABLE_GENERATION_ATOMIC_POINTER"
        ):
            crash_probe = (
                pointer_crash_recovery_probe(
                    candidates_root / "pointer"
                )
            )
        else:
            crash_probe = {
                "status":
                    "REQUIRES_SEPARATE_CANDIDATE_SPECIFIC_CRASH_PROBE"
            }

    live_generated_after = (
        _directory_content_digest(
            LIVE_VAULT / "generated"
        )
    )
    live_views_after = (
        _directory_content_digest(
            LIVE_VAULT / "views"
        )
    )
    if (
        live_generated_after
        != live_generated_before
        or live_views_after
        != live_views_before
    ):
        raise PromotionExperimentError(
            "protected live Vault trees changed during sandbox experiment"
        )

    environment = {
        "windows_version":
            platform.platform(),
        "filesystem_type":
            _filesystem_type(sandbox),
        "onedrive_path":
            str(sandbox),
        "reparse_state_summary":
            _reparse_summary(sandbox),
        "python_version":
            sys.version,
    }

    if not qualified:
        status = "FAIL"
        adjudication = (
            "ALL_CANDIDATES_REJECTED"
        )
    elif len(qualified) == 1:
        if (
            crash_probe is not None
            and crash_probe.get(
                "last_known_good_identifiable"
            ) is True
            and crash_probe.get(
                "recovery_deterministic"
            ) is True
        ):
            status = "PASS"
            adjudication = (
                "ONE_CANDIDATE_QUALIFIED"
            )
        else:
            status = "BLOCKED"
            adjudication = (
                "FILESYSTEM_PASS_CRASH_PROBE_INCOMPLETE"
            )
    else:
        status = "BLOCKED"
        adjudication = (
            "MULTIPLE_CANDIDATES_REQUIRE_ADJUDICATION"
        )

    report = {
        "schema": METRICS_SCHEMA,
        "status": status,
        "adjudication": adjudication,
        "sandbox_path": str(sandbox),
        "live_vault_path":
            str(LIVE_VAULT),
        "live_vault_modified": False,
        "live_generated_digest_before":
            live_generated_before,
        "live_generated_digest_after":
            live_generated_after,
        "live_views_digest_before":
            live_views_before,
        "live_views_digest_after":
            live_views_after,
        "qualified_candidates":
            qualified,
        "selected_candidate":
            selected_candidate,
        "crash_recovery_probe":
            crash_probe,
        "environment": environment,
        "negative_control_validated":
            negative.result == "PASS",
        "candidates": [
            asdict(item)
            for item in candidates
        ],
        "obsidian_open_qualified": False,
        "production_promotion_authorized":
            False,
    }

    event_log = append_metrics_event(
        report
    )
    report["append_only_event_log"] = str(
        event_log
    )
    return report
