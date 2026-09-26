import argparse
import hashlib
import importlib.util
import json
import os
import stat
import tempfile
from pathlib import Path

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606

EXPECTED_CR1_HELPER_PATH = Path("tools/cr1_context_informativeness.py")
EXPECTED_CR1_HELPER_BLOB = "bb5cd4acd1b48141019c0ec3796ea61627dc0dbf"
EXPECTED_CR2_HELPER_PATH = Path("tools/cr2_regime_candidate_synthesis.py")
EXPECTED_CR2_HELPER_BLOB = "34c702e926b3baec90c57b8366177c2db1eca074"
EXPECTED_CR2_EVIDENCE_PATH = Path("reports/program/evidence/2026-09-26-CR2-REGIME-CANDIDATE-SYNTHESIS.json")
EXPECTED_CR2_EVIDENCE_BLOB = "d6543d12fc01405fedb006ddb5d714a772f32678"
EXPECTED_CHARTER_PATH = Path("reports/program/evidence/2026-09-26-C01-CONFIRMATORY-CHARTER-V0.2.json")
EXPECTED_CHARTER_BLOB = "ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1"

EXPECTED_VOL_THRESHOLDS = (5.371776146488064, 10.71209216288787)
EXPECTED_TICK_THRESHOLDS = (0.8005586592178772, 1.2183908045977012)
EXPECTED_RV_QUINTILES = (3.973523081929233, 6.185588239477184, 9.29219887827349, 15.11786314181646)
EXPECTED_TICK_QUINTILES = (91.53333333333333, 144.26666666666668, 220.66666666666666, 338.8)

EXPECTED_C01_STATUS = "SUPPORTED_N0_SYNTHESIS"
EXPECTED_C02_STATUS = "NOT_INTERPRETABLE"
TARGET_CLASSES = 25
ALPHA = 1.0
MAX_OUTPUT_BYTES = 16 * 1024 * 1024
READ_COLUMNS = ["minute_start_ms_utc", "tick_count", "segment_id", "mid_close"]
SCOPE = {
    "confirmation_model_only": True,
    "confirmation_data_accessed": False,
    "direction_target_used": False,
    "pnl_calculated": False,
    "trades_calculated": False,
    "signals_calculated": False,
    "semantic_regime_labels_instantiated": False,
    "optimization": False,
    "threshold_search": False,
    "feature_search": False,
    "interaction_search": False,
    "winner_selection": False,
    "mt5_used": False,
}


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1_bytes(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def git_blob_sha1_path(path: Path) -> str:
    return git_blob_sha1_bytes(path.read_bytes())


def path_chain_has_reparse_or_symlink(path: Path) -> bool:
    p = path.expanduser()
    parts = p.parts
    if not parts:
        return False
    cur = Path(parts[0])
    start = 1
    if len(parts) >= 2 and parts[0] == os.sep:
        cur = Path(os.sep)
        start = 1
    for part in parts[start:]:
        cur = cur / part
        try:
            st = os.lstat(cur)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            return True
    return False


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_bound_file(repo_root: Path, rel: Path, git_blob: str) -> Path:
    raw = repo_root / rel
    if path_chain_has_reparse_or_symlink(raw):
        raise RuntimeError(f"reparse/symlink in bound path: {rel}")
    p = raw.resolve(strict=True)
    if not is_within(p, repo_root):
        raise RuntimeError(f"bound file escaped repo-root: {rel}")
    if git_blob_sha1_path(p) != git_blob:
        raise RuntimeError(f"Git blob mismatch: {rel}")
    return p


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_charter(ch: dict) -> None:
    if ch.get("schema") != "ATDS_C01_CONFIRMATORY_RESEARCH_CHARTER_V0_2":
        raise RuntimeError("charter schema mismatch")
    if ch.get("status") != "FROZEN_BEFORE_CONFIRMATION_DATA_ACCESS":
        raise RuntimeError("charter status mismatch")
    cand = ch.get("candidate") or {}
    if cand.get("id") != "CR2-C01-ABS_VOL_X_TICK" or cand.get("cr2_status") != EXPECTED_C01_STATUS:
        raise RuntimeError("charter candidate mismatch")
    conf = ch.get("confirmation_data") or {}
    if conf.get("eligible_start_utc") != "2026-05-25T00:00:00Z" or conf.get("fixed_end_utc") != "2027-05-24T23:59:59Z":
        raise RuntimeError("charter confirmation window mismatch")
    ev = (ch.get("development_freeze") or {}).get("already_registered_thresholds") or {}
    exact = {
        "abs_rv15_state": list(EXPECTED_VOL_THRESHOLDS),
        "tick5_hour_relative_state": list(EXPECTED_TICK_THRESHOLDS),
        "rv15_target_quintiles": list(EXPECTED_RV_QUINTILES),
        "tick15_target_quintiles": list(EXPECTED_TICK_QUINTILES),
    }
    if ev != exact:
        raise RuntimeError("charter frozen threshold mismatch")


def validate_cr2_evidence(ev: dict) -> None:
    if ev.get("schema") != "ATDS_CR2_REGIME_CANDIDATE_SYNTHESIS_V0_1" or ev.get("status") != "CR2_COMPLETE":
        raise RuntimeError("CR2 evidence schema/status mismatch")
    if ev.get("research_class") != "N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS":
        raise RuntimeError("CR2 evidence research class mismatch")
    got = {x.get("candidate_id"): x.get("scientific_status") for x in ev.get("candidates", [])}
    expected = {"CR2-C01-ABS_VOL_X_TICK": EXPECTED_C01_STATUS, "CR2-C02-REL_VOL_X_TICK": EXPECTED_C02_STATUS}
    if got != expected:
        raise RuntimeError("CR2 candidate status mismatch")
    scope = ev.get("scope") or {}
    forbidden = ("direction_target_used", "pnl_calculated", "optimization", "feature_search", "interaction_search", "winner_selection", "semantic_regime_labels_instantiated", "mt5_used")
    if any(scope.get(k) is not False for k in forbidden):
        raise RuntimeError("CR2 scope mismatch")


def pad_counts(counts, nkeys: int, k: int = TARGET_CLASSES):
    import numpy as np
    a = np.asarray(counts, dtype=np.int64)
    if a.ndim != 2 or a.shape[1] != k or a.shape[0] > nkeys:
        raise RuntimeError("invalid count matrix shape")
    out = np.zeros((nkeys, k), dtype=np.int64)
    out[: a.shape[0]] = a
    return out


def probabilities_from_counts(counts, alpha: float = ALPHA):
    import numpy as np
    c = np.asarray(counts, dtype=np.float64)
    if c.ndim != 2 or np.any(c < 0):
        raise RuntimeError("invalid counts")
    return (c + alpha) / (c.sum(axis=1, keepdims=True) + alpha * c.shape[1])


def canonical_model_digest(hour_medians, vol_th, tick_th, rv_q, tick_q, vol_counts, tick_counts, cand_counts) -> str:
    import numpy as np
    h = hashlib.sha256()
    for arr, dtype in (
        (hour_medians, "<f8"), (vol_th, "<f8"), (tick_th, "<f8"), (rv_q, "<f8"), (tick_q, "<f8"),
        (vol_counts, "<i8"), (tick_counts, "<i8"), (cand_counts, "<i8"),
    ):
        a = np.asarray(arr).astype(dtype, copy=False)
        h.update(str(a.shape).encode("ascii") + b"\0")
        h.update(a.tobytes(order="C"))
    h.update(b"laplace-alpha=1.0")
    return h.hexdigest()


def compare_tuple(got, expected, atol=1e-12, label="value"):
    import numpy as np
    g = np.asarray(got, dtype=np.float64)
    e = np.asarray(expected, dtype=np.float64)
    if g.shape != e.shape or not np.allclose(g, e, rtol=0.0, atol=atol, equal_nan=False):
        raise RuntimeError(f"{label} mismatch: {g.tolist()} != {e.tolist()}")


def extract_c01_from_evidence(ev: dict) -> dict:
    for c in ev.get("candidates", []):
        if c.get("candidate_id") == "CR2-C01-ABS_VOL_X_TICK":
            return c
    raise RuntimeError("C01 missing from CR2 evidence")


def validate_d2026_reproduction(c01: dict, result: dict, atol=1e-12) -> None:
    ref = c01.get("primary_15m", {}).get("D2026") or {}
    for comp in ("vs_vol", "vs_tick"):
        rr = (ref.get("comparisons") or {}).get(comp) or {}
        gg = (result.get("comparisons") or {}).get(comp) or {}
        for key in ("delta_log_loss", "delta_brier"):
            if abs(float(rr[key]) - float(gg[key])) > atol:
                raise RuntimeError(f"D2026 reproduction mismatch {comp}.{key}")
        if int(rr["n"]) != int(gg["n"]):
            raise RuntimeError(f"D2026 reproduction sample mismatch {comp}")
    if ref.get("joint_state_counts_test") != result.get("joint_state_counts_test"):
        raise RuntimeError("D2026 joint-state count reproduction mismatch")


def write_json_exclusive(path: Path, payload: dict) -> None:
    raw = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if len(raw) > MAX_OUTPUT_BYTES:
        raise RuntimeError("model artifact exceeds output bound")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(raw)


def main():
    ap = argparse.ArgumentParser(description="C01 frozen confirmatory model artifact producer")
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--ap0-manifest", required=True)
    ap.add_argument("--charter-json", required=True)
    ap.add_argument("--cr2-evidence-json", required=True)
    ap.add_argument("--output", default=str(Path(tempfile.gettempdir()) / "ATDS-C01-FROZEN-MODEL.json"))
    args = ap.parse_args()

    repo_raw = Path(args.repo_root).expanduser()
    root_raw = Path(args.ap0_root).expanduser()
    manifest_raw = Path(args.ap0_manifest).expanduser()
    charter_raw = Path(args.charter_json).expanduser()
    evidence_raw = Path(args.cr2_evidence_json).expanduser()
    output_raw = Path(args.output).expanduser()

    if os.path.lexists(output_raw):
        print("BLOCKED_C01_MODEL_OUTPUT_EXISTS"); print(output_raw); return 2
    for raw, label in ((repo_raw, "repo-root"), (root_raw, "AP0 root"), (manifest_raw, "AP0 manifest"), (charter_raw, "charter"), (evidence_raw, "CR2 evidence"), (output_raw.parent, "output parent")):
        if path_chain_has_reparse_or_symlink(raw):
            print("BLOCKED_C01_MODEL_REPARSE"); print(f"{label}: {raw}"); return 2

    repo_root = repo_raw.resolve(strict=False)
    root = root_raw.resolve(strict=False)
    manifest_path = manifest_raw.resolve(strict=False)
    charter_path = charter_raw.resolve(strict=False)
    evidence_path = evidence_raw.resolve(strict=False)
    output = output_raw.resolve(strict=False)

    def block(code, reason):
        payload = {"schema": "ATDS_C01_FROZEN_MODEL_BLOCKED_V0_1", "status": code, "reason": reason}
        try:
            if not output.exists():
                write_json_exclusive(output, payload)
        except Exception:
            pass
        print(code); print(reason); print(f"Report: {output}"); return 2

    try:
        if not repo_root.is_dir() or not root.is_dir() or not manifest_path.is_file():
            raise RuntimeError("required input missing")
        if output == root or is_within(output, root):
            raise RuntimeError("output inside AP0 input")
        if sha256_path(manifest_path) != EXPECTED_AP0_MANIFEST_SHA256:
            raise RuntimeError("AP0 manifest SHA mismatch")

        cr1_path = resolve_bound_file(repo_root, EXPECTED_CR1_HELPER_PATH, EXPECTED_CR1_HELPER_BLOB)
        cr2_path = resolve_bound_file(repo_root, EXPECTED_CR2_HELPER_PATH, EXPECTED_CR2_HELPER_BLOB)
        bound_charter = resolve_bound_file(repo_root, EXPECTED_CHARTER_PATH, EXPECTED_CHARTER_BLOB)
        bound_evidence = resolve_bound_file(repo_root, EXPECTED_CR2_EVIDENCE_PATH, EXPECTED_CR2_EVIDENCE_BLOB)
        if charter_path != bound_charter or evidence_path != bound_evidence:
            raise RuntimeError("governance input path mismatch")

        cr1 = load_module(cr1_path, "atds_cr1_frozen_model")
        cr2 = load_module(cr2_path, "atds_cr2_frozen_model")
        charter = json.loads(charter_path.read_text(encoding="utf-8"))
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        validate_charter(charter)
        validate_cr2_evidence(evidence)
        c01 = extract_c01_from_evidence(evidence)

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") != "AP0_COMPLETE" or manifest.get("output_identity") != EXPECTED_AP0_IDENTITY:
            raise RuntimeError("AP0 identity/status mismatch")
        files = manifest.get("files")
        cov = manifest.get("coverage") or {}
        if not isinstance(files, list) or len(files) != EXPECTED_FILES:
            raise RuntimeError("AP0 file count mismatch")
        if cov.get("minute_rows_written") != EXPECTED_MINUTES or cov.get("source_ticks_read") != EXPECTED_SOURCE_TICKS or cov.get("segments") != EXPECTED_SEGMENTS:
            raise RuntimeError("AP0 coverage mismatch")

        import numpy as np
        import pyarrow as pa
        import pyarrow.parquet as pq
        chunks = {k: [] for k in ("minute", "tick", "seg", "close")}
        rows = 0; ticks = 0; previous = None
        for rec in files:
            rel = rec["relative_path"]
            p = cr1.resolve_manifest_member(root, rel)
            if int(p.stat().st_size) != int(rec["size_bytes"]) or sha256_path(p) != rec["sha256"]:
                raise RuntimeError(f"AP0 identity mismatch: {rel}")
            pf = pq.ParquetFile(p)
            if int(pf.metadata.num_rows) != int(rec["rows"]):
                raise RuntimeError(f"AP0 rows mismatch: {rel}")
            meta = pf.schema_arrow.metadata or {}
            if meta.get(b"dataset_identity") != EXPECTED_AP0_IDENTITY.encode() or meta.get(b"volumes_used") != b"false":
                raise RuntimeError(f"AP0 metadata mismatch: {rel}")
            table = pf.read(columns=READ_COLUMNS, use_threads=False)
            if table.column_names != READ_COLUMNS:
                raise RuntimeError("column scope violation")
            vals = {
                "minute": table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False),
                "tick": table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False),
                "seg": table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False),
                "close": table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False),
            }
            n = len(vals["minute"])
            if n == 0 or any(len(v) != n for v in vals.values()):
                raise RuntimeError("decoded row mismatch")
            if np.any(np.diff(vals["minute"]) <= 0) or np.any(vals["tick"] <= 0) or np.any(~np.isfinite(vals["close"])) or np.any(vals["close"] <= 0):
                raise RuntimeError("AP0 array invariant violation")
            if previous is not None and (int(vals["minute"][0]) <= previous[0] or int(vals["seg"][0]) - previous[1] not in (0, 1)):
                raise RuntimeError("global AP0 boundary violation")
            if np.any(np.diff(vals["seg"]) < 0) or np.any(np.diff(vals["seg"]) > 1):
                raise RuntimeError("segment jump violation")
            previous = (int(vals["minute"][-1]), int(vals["seg"][-1]))
            rows += n; ticks += int(np.sum(vals["tick"], dtype=np.int64))
            for k, v in vals.items(): chunks[k].append(v.copy())
            if sha256_path(p) != rec["sha256"]:
                raise RuntimeError(f"AP0 changed during model freeze: {rel}")
        if rows != EXPECTED_MINUTES or ticks != EXPECTED_SOURCE_TICKS:
            raise RuntimeError("coverage mismatch")
        a = {k: np.concatenate(v) for k, v in chunks.items()}
        if int(a["seg"][0]) != 0 or int(a["seg"][-1]) != EXPECTED_SEGMENTS - 1:
            raise RuntimeError("segment coverage mismatch")

        signed, valid = cr1.signed_return_1m_bps(a["minute"], a["seg"], a["close"])
        rv15 = cr1.rolling_realized_vol_bps(signed, valid, a["minute"], a["seg"], 15)
        tick5 = cr1.trailing_mean(a["tick"], a["minute"], a["seg"], 5)
        fwd_rv15 = cr1.forward_from_endpoint(rv15, a["minute"], a["seg"], 15)
        fwd_tick15 = cr1.forward_mean(a["tick"], a["minute"], a["seg"], 15)
        ny_hour, ny_weekday, utc_year = cr1.time_dimensions(a["minute"])

        train_anchor = np.asarray(utc_year) <= 2025
        d2026 = np.asarray(utc_year) == 2026
        hour_medians = cr1.hour_medians(tick5, ny_hour, train_anchor)
        tick_rel = cr1.relative_by_hour(tick5, ny_hour, hour_medians)

        vol_state, vol_th = cr2.tertile_states(rv15, train_anchor)
        tick_state, tick_th = cr2.tertile_states(tick_rel, train_anchor)
        joint = cr2.joint_state(vol_state, tick_state)
        base = cr2.b2_codes(ny_hour, ny_weekday)

        target_valid = np.isfinite(fwd_rv15) & np.isfinite(fwd_tick15)
        context_valid = joint >= 0
        train_valid = train_anchor & target_valid & context_valid
        test_valid = d2026 & target_valid & context_valid
        classes, rv_q, tick_q = cr2.joint_target_classes(fwd_rv15, fwd_tick15, train_valid)

        compare_tuple(vol_th, EXPECTED_VOL_THRESHOLDS, label="ABS RV15 thresholds")
        compare_tuple(tick_th, EXPECTED_TICK_THRESHOLDS, label="tick relative thresholds")
        compare_tuple(rv_q, EXPECTED_RV_QUINTILES, label="RV target quintiles")
        compare_tuple(tick_q, EXPECTED_TICK_QUINTILES, label="TICK target quintiles")

        cand_keys = cr2.conditional_codes(base, joint, 9)
        vol_keys = cr2.conditional_codes(base, vol_state, 3)
        tick_keys = cr2.conditional_codes(base, tick_state, 3)
        ytr = classes[train_valid]
        cand_counts = pad_counts(cr2.fit_model(cand_keys[train_valid], ytr), 24 * 7 * 9)
        vol_counts = pad_counts(cr2.fit_model(vol_keys[train_valid], ytr), 24 * 7 * 3)
        tick_counts = pad_counts(cr2.fit_model(tick_keys[train_valid], ytr), 24 * 7 * 3)

        yte = classes[test_valid]
        reproduction = {
            "comparisons": {
                "vs_vol": cr2.comparison_result(vol_counts, cand_counts, vol_keys[test_valid], cand_keys[test_valid], yte),
                "vs_tick": cr2.comparison_result(tick_counts, cand_counts, tick_keys[test_valid], cand_keys[test_valid], yte),
            },
            "joint_state_counts_test": {str(v): int(np.count_nonzero(test_valid & (joint == v))) for v in range(9)},
        }
        validate_d2026_reproduction(c01, reproduction)

        vol_probs = probabilities_from_counts(vol_counts)
        tick_probs = probabilities_from_counts(tick_counts)
        cand_probs = probabilities_from_counts(cand_counts)
        model_digest = canonical_model_digest(hour_medians, vol_th, tick_th, rv_q, tick_q, vol_counts, tick_counts, cand_counts)

        payload = {
            "schema": "ATDS_C01_FROZEN_CONFIRMATORY_MODEL_V0_1",
            "status": "C01_MODEL_FROZEN",
            "candidate_id": "CR2-C01-ABS_VOL_X_TICK",
            "binding": {
                "ap0_manifest_sha256": EXPECTED_AP0_MANIFEST_SHA256,
                "ap0_files_rehashed": EXPECTED_FILES,
                "cr1_helper_git_blob": EXPECTED_CR1_HELPER_BLOB,
                "cr2_helper_git_blob": EXPECTED_CR2_HELPER_BLOB,
                "cr2_evidence_git_blob": EXPECTED_CR2_EVIDENCE_BLOB,
                "charter_git_blob": EXPECTED_CHARTER_BLOB,
            },
            "coverage": {"minute_rows": rows, "source_ticks_accounted": ticks, "segments": EXPECTED_SEGMENTS},
            "development": {
                "anchor_rule": "utc_year(t)<=2025",
                "train_valid_n": int(np.count_nonzero(train_valid)),
                "laplace_alpha": ALPHA,
                "target_classes": TARGET_CLASSES,
            },
            "frozen_parameters": {
                "tick5_ny_hour_medians": [float(x) for x in hour_medians],
                "abs_rv15_state_thresholds": [float(x) for x in vol_th],
                "tick5_hour_relative_state_thresholds": [float(x) for x in tick_th],
                "rv15_target_quintiles": [float(x) for x in rv_q],
                "tick15_target_quintiles": [float(x) for x in tick_q],
            },
            "models": {
                "b2_abs_vol": {"key_space": 24 * 7 * 3, "counts": vol_counts.tolist(), "probabilities": vol_probs.tolist()},
                "b2_tick": {"key_space": 24 * 7 * 3, "counts": tick_counts.tolist(), "probabilities": tick_probs.tolist()},
                "b2_abs_vol_tick": {"key_space": 24 * 7 * 9, "counts": cand_counts.tolist(), "probabilities": cand_probs.tolist()},
            },
            "model_digest_sha256": model_digest,
            "d2026_reproduction": reproduction,
            "scope": SCOPE,
            "runtime": {"numpy_version": np.__version__, "pyarrow_version": pa.__version__},
        }
        write_json_exclusive(output, payload)
        print("C01_MODEL_FROZEN")
        print(f"Minute rows: {rows}")
        print(f"Train valid: {payload['development']['train_valid_n']}")
        print(f"Model digest: {model_digest}")
        print(f"Report: {output}")
        return 0
    except Exception as exc:
        return block("BLOCKED_C01_MODEL_RUNTIME", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
