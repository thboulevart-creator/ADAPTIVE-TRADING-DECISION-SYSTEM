import importlib.util
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve().parents[1] / "tools" / "bepd_07b_behavioral_excursion.py"
SPEC = importlib.util.spec_from_file_location("bepd07b_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(runner)


class TestBEPD07B(unittest.TestCase):
    def test_high_reintegrative_formula(self):
        r, x = runner.compute_excursions("HIGH", 100, [103, 102], [95, 97])
        self.assertEqual(r, Decimal("5"))
        self.assertEqual(x, Decimal("3"))

    def test_high_external_formula(self):
        r, x = runner.compute_excursions("HIGH", 100, [110, 101], [99, 98])
        self.assertEqual(x, Decimal("10"))
        self.assertEqual(r, Decimal("2"))

    def test_low_reintegrative_formula(self):
        r, x = runner.compute_excursions("LOW", 100, [107, 102], [96, 99])
        self.assertEqual(r, Decimal("7"))
        self.assertEqual(x, Decimal("4"))

    def test_low_external_formula(self):
        r, x = runner.compute_excursions("LOW", 100, [101, 102], [91, 95])
        self.assertEqual(x, Decimal("9"))
        self.assertEqual(r, Decimal("2"))

    def test_high_reintegrative_floor_zero(self):
        r, _ = runner.compute_excursions("HIGH", 100, [104], [101])
        self.assertEqual(r, Decimal("0"))

    def test_high_external_floor_zero(self):
        _, x = runner.compute_excursions("HIGH", 100, [99], [90])
        self.assertEqual(x, Decimal("0"))

    def test_low_reintegrative_floor_zero(self):
        r, _ = runner.compute_excursions("LOW", 100, [99], [95])
        self.assertEqual(r, Decimal("0"))

    def test_low_external_floor_zero(self):
        _, x = runner.compute_excursions("LOW", 100, [110], [101])
        self.assertEqual(x, Decimal("0"))

    def test_invalid_side_fails(self):
        with self.assertRaisesRegex(ValueError, "invalid side"):
            runner.compute_excursions("OTHER", 100, [101], [99])

    def test_strict_post_take_path_start(self):
        ts = [1000, 1060, 1120, 1180]
        lo, hi = runner.path_slice_indices(ts, 1060, 2000)
        self.assertEqual((lo, hi), (2, 4))

    def test_same_h1_or_equal_start_excluded(self):
        ts = [1000, 1060, 1120]
        lo, hi = runner.path_slice_indices(ts, 1060, 9999)
        self.assertEqual(ts[lo:hi], [1120])

    def test_target_week_end_excluded(self):
        ts = [1000, 1060, 1120, 1180]
        lo, hi = runner.path_slice_indices(ts, 900, 1180)
        self.assertEqual(ts[lo:hi], [1000, 1060, 1120])

    def test_empty_path_indices_are_equal(self):
        ts = [1000, 1060]
        lo, hi = runner.path_slice_indices(ts, 1060, 1120)
        self.assertEqual(lo, hi)

    def test_new_york_dst_spring_week_is_167_utc_hours(self):
        start, end = runner.target_week_bounds_ms("2024-03-04")
        hours = Decimal(end - start) / Decimal(3_600_000)
        self.assertEqual(hours, Decimal("167"))

    def test_new_york_dst_fall_week_is_169_utc_hours(self):
        start, end = runner.target_week_bounds_ms("2024-10-28")
        hours = Decimal(end - start) / Decimal(3_600_000)
        self.assertEqual(hours, Decimal("169"))

    def test_normal_week_is_168_utc_hours(self):
        start, end = runner.target_week_bounds_ms("2024-01-08")
        hours = Decimal(end - start) / Decimal(3_600_000)
        self.assertEqual(hours, Decimal("168"))

    def test_type7_quartiles(self):
        s = runner.metric_surface([Decimal("1"), Decimal("2"), Decimal("3"), Decimal("4"), Decimal("5")])
        self.assertEqual(s["P25"], "2.000000000000000000")
        self.assertEqual(s["P50"], "3.000000000000000000")
        self.assertEqual(s["P75"], "4.000000000000000000")

    def test_p50_equals_median(self):
        s = runner.metric_surface([Decimal("1"), Decimal("2"), Decimal("7"), Decimal("9")])
        self.assertEqual(s["P50"], s["MEDIAN"])

    def test_exact_ecdf_terminal_count(self):
        s = runner.metric_surface([Decimal("0"), Decimal("1"), Decimal("1"), Decimal("2")])
        self.assertEqual(s["EMPIRICAL_CDF"][-1]["cumulative_count"], 4)
        self.assertEqual(s["EMPIRICAL_CDF"][-1]["cumulative_fraction"], "1")

    def test_zero_count_semantics(self):
        s = runner.metric_surface([Decimal("0"), Decimal("0"), Decimal("1"), Decimal("2")])
        self.assertEqual(s["ZERO_COUNT"], 2)
        self.assertEqual(s["ZERO_FRACTION"], "1/2")
        self.assertEqual(s["ZERO_FRACTION_DECIMAL"], "0.500000000000000000")

    def test_negative_metric_surface_fails(self):
        with self.assertRaisesRegex(ValueError, "negative excursion"):
            runner.metric_surface([Decimal("0"), Decimal("-1")])

    def test_source_file_window_binding(self):
        files = [
            {"relative_path": "a", "first_minute_ms_utc": 100, "last_minute_ms_utc": 199},
            {"relative_path": "b", "first_minute_ms_utc": 200, "last_minute_ms_utc": 299},
            {"relative_path": "c", "first_minute_ms_utc": 300, "last_minute_ms_utc": 399},
        ]
        self.assertEqual(runner.source_files_for_window(files, 150, 350), ["a", "b", "c"])

    def test_source_file_equal_start_boundary_excluded_when_file_ends_at_start(self):
        files = [
            {"relative_path": "a", "first_minute_ms_utc": 0, "last_minute_ms_utc": 100},
            {"relative_path": "b", "first_minute_ms_utc": 101, "last_minute_ms_utc": 200},
        ]
        self.assertEqual(runner.source_files_for_window(files, 100, 300), ["b"])

    def test_parse_utc_requires_utc_offset(self):
        with self.assertRaisesRegex(ValueError, "must be UTC"):
            runner.parse_utc_ms("2026-01-01T12:00:00+01:00")

    def test_parse_utc_exact_minute(self):
        ms = runner.parse_utc_ms("1970-01-01T00:01:00+00:00")
        self.assertEqual(ms, 60000)

    def test_no_outcome_dependent_endpoint_in_runner_source(self):
        src = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("reintegration_h1_close_utc", src)
        self.assertNotIn("same_week_reintegration", src)

    def test_no_mid_close_substitution_in_runner_source(self):
        src = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("mid_close", src)

    def test_no_level_price_anchor_in_runner_source(self):
        src = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("level_price_mid", src)

    def test_gap_interpolation_not_present(self):
        src = RUNNER_PATH.read_text(encoding="utf-8").lower()
        self.assertNotIn("interpolate(", src)
        self.assertNotIn("fillna(", src)
        self.assertNotIn("ffill(", src)
        self.assertNotIn("bfill(", src)

    def test_missing_path_fail_closed_marker_present(self):
        src = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn("EMPTY_PATH:", src)

    def test_no_joint_metric_output(self):
        src = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn('"joint_excursion_metrics": "NOT_AUTHORIZED"', src)
        self.assertNotIn("MFE_MAE_RATIO", src)

    def test_no_subgroup_output(self):
        src = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn('"subgroups": []', src)

    def test_expected_dataset_binding(self):
        self.assertEqual(runner.EXPECTED_DATASET, "USTECH_PROFILE_MINUTE_CORE_V0_1")
        self.assertEqual(runner.EXPECTED_FILE_COUNT, 61)
        self.assertEqual(runner.EXPECTED_AP0_ROWS, 1709180)


    def test_data02_file_set_digest_semantics(self):
        files = [
            {"relative_path":"b","size_bytes":2,"sha256":"bb"},
            {"relative_path":"a","size_bytes":1,"sha256":"aa"},
        ]
        import hashlib, json
        material = [
            {"relative_path":"b","size_bytes":2,"sha256":"bb"},
            {"relative_path":"a","size_bytes":1,"sha256":"aa"},
        ]
        expected = hashlib.sha256(
            json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(runner.data02_file_set_digest(files), expected)

    def test_manifest_and_file_set_bindings(self):
        self.assertEqual(
            runner.EXPECTED_MANIFEST_SHA256,
            "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce",
        )
        self.assertEqual(
            runner.EXPECTED_FILE_SET_DIGEST,
            "1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a",
        )


if __name__ == "__main__":
    unittest.main()
