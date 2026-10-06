from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
FIX=json.loads((ROOT/"tests/fixtures/bepd_04e_synthetic_v0_1.json").read_text())
try:
    from tools.bepd_04e_response_generalization_v0_1 import (
        aggregate_week_counts, ratio_of_sums, moving_block_ratio_ci,
        temporal_stability_synthetic, nonstationarity_gate_support,
    )
except Exception as exc:
    raise RuntimeError("BEPD04E_RUNTIME_ABSENT_EXPECTED_RED") from exc
class TestBEPD04E(unittest.TestCase):
    def case(self,name): return FIX["cases"][name]
    def test_one_event(self):
        c=self.case("S01_ONE_EVENT_ONE_WEEK"); a=aggregate_week_counts(c["calendar"],c["events"])
        self.assertEqual(a,[{"target_week_id":"2026-01-05","success_count":1,"event_count":1}]); self.assertEqual(ratio_of_sums(a),1.0)
    def test_zero_week_preserved(self):
        c=self.case("S03_ZERO_EVENT_WEEK_BETWEEN"); a=aggregate_week_counts(c["calendar"],c["events"])
        self.assertEqual((a[1]["success_count"],a[1]["event_count"]),(0,0)); self.assertEqual(ratio_of_sums(a),0.5)
    def test_mixed_ratio_is_ratio_of_sums(self):
        c=self.case("S06_MIXED_MULTI_CLUSTER"); a=aggregate_week_counts(c["calendar"],c["events"])
        self.assertEqual((sum(x["success_count"] for x in a),sum(x["event_count"] for x in a)),(3,5)); self.assertEqual(ratio_of_sums(a),0.6)
    def test_deterministic_moving_block(self):
        c=self.case("S06_MIXED_MULTI_CLUSTER"); kw=dict(block_length=2,replications=200,seed=40420261006,confidence_level=.95,interval_method="PERCENTILE")
        self.assertEqual(moving_block_ratio_ci(c["calendar"],c["events"],execution_scope="SYNTHETIC_QUALIFICATION",**kw),moving_block_ratio_ci(c["calendar"],c["events"],execution_scope="SYNTHETIC_QUALIFICATION",**kw))
    def test_basic_and_percentile_supported(self):
        c=self.case("S06_MIXED_MULTI_CLUSTER")
        for m in ("PERCENTILE","BASIC"):
            self.assertEqual(moving_block_ratio_ci(c["calendar"],c["events"],execution_scope="SYNTHETIC_QUALIFICATION",block_length=2,replications=100,seed=7,confidence_level=.9,interval_method=m)["interval_method"],m)
    def test_invalid_block_lengths(self):
        c=self.case("S06_MIXED_MULTI_CLUSTER")
        for bl in (0,99):
            with self.assertRaisesRegex(ValueError,"BLOCK_LENGTH"): moving_block_ratio_ci(c["calendar"],c["events"],execution_scope="SYNTHETIC_QUALIFICATION",block_length=bl,replications=20,seed=1,confidence_level=.9,interval_method="PERCENTILE")
    def test_real_scope_fails_without_authority(self):
        c=self.case("S06_MIXED_MULTI_CLUSTER")
        with self.assertRaisesRegex(ValueError,"REAL_EXECUTION_NOT_AUTHORIZED"): moving_block_ratio_ci(c["calendar"],c["events"],execution_scope="REAL_AUTHORIZED",block_length=2,replications=20,seed=1,confidence_level=.9,interval_method="PERCENTILE")
    def test_calendar_fail_closed(self):
        c=self.case("S01_ONE_EVENT_ONE_WEEK")
        for cal,err in [(["2026-01-05","2026-01-05"],"DUPLICATE_TARGET_WEEK"),(["2026-01-12","2026-01-05"],"UNSORTED_TARGET_WEEK"),(["2026-01-05","2026-01-19"],"CALENDAR_GAP")]:
            with self.assertRaisesRegex(ValueError,err): aggregate_week_counts(cal,c["events"])
    def test_unknown_event_week_fails(self):
        with self.assertRaisesRegex(ValueError,"EVENT_WEEK_OUTSIDE_CALENDAR"): aggregate_week_counts(["2026-01-05"],[{"event_id":"e","target_week_id":"2026-01-12","sweep_cluster_id":"c","same_week_reintegration":True}])
    def test_cluster_split_fails(self):
        with self.assertRaisesRegex(ValueError,"SWEEP_CLUSTER_SPLIT"): aggregate_week_counts(["2026-01-05","2026-01-12"],[{"event_id":"e1","target_week_id":"2026-01-05","sweep_cluster_id":"c","same_week_reintegration":True},{"event_id":"e2","target_week_id":"2026-01-12","sweep_cluster_id":"c","same_week_reintegration":False}])
    def test_m10_synthetic(self):
        o=temporal_stability_synthetic([1,0,1,1,0,0,1,0],strata=["A"]*4+["B"]*4,declared_strata=["A","B"],minimum_n_per_stratum=4,max_mean_spread=.6)
        self.assertEqual(o["status"],"STABLE_WITHIN_DECLARED_TOLERANCE")
    def test_gate_unresolved_when_m04_blocked(self):
        o=nonstationarity_gate_support(m04_status="BLOCKED_BY_REPRESENTATION_CONSTRAINT",m10_status="STABLE_WITHIN_DECLARED_TOLERANCE",conflicting_policy="ANY_BLOCK_OR_CONFLICT_UNRESOLVED")
        self.assertEqual(o["state"],"NONSTATIONARITY_UNRESOLVED")
if __name__=="__main__": unittest.main()
