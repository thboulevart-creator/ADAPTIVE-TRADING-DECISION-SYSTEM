"""ATDS EA-03-P1: standalone synthetic-only adapter adversarial specification."""
import copy
import json
import unittest
from pathlib import Path

from src.ea_observation.synthetic_adapter import adapt_synthetic_feed
from src.ea_observation.validation import validate_batch

FIXTURE = Path(__file__).parent / "fixtures" / "ea03_p1_synthetic_feed_v0_1.json"
D1_FIXTURE = Path(__file__).parent / "fixtures" / "ea_observation_synthetic_v0_1.json"


def sample():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def get_record(batch, kind):
    return next(r for r in batch["feeds"][0]["records"] if r["kind"] == kind)


def check_fail(test, changed, label=None):
    result = adapt_synthetic_feed(changed)
    test.assertEqual(result["status"], "FAIL")
    test.assertIsNone(result["batch"])
    test.assertFalse(result["authority"]["trading"])
    test.assertFalse(result["authority"]["capital"])
    test.assertFalse(result["authority"]["real_data"])
    if label:
        test.assertIn(label, result["errors"])
    return result


class TestEA03P1SyntheticAdapter(unittest.TestCase):
    def test_P01_fixture_roundtrip_validated(self):
        result = adapt_synthetic_feed(sample())
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["validation"]["errors"], [])
        self.assertEqual(result["validation"]["overall_status"], "STRUCTURALLY_VALID")
        self.assertEqual(result["batch"], json.loads(D1_FIXTURE.read_text(encoding="utf-8")))
        self.assertEqual(result["validation"]["scientific_status"], "NOT_ASSESSED")

    def test_P02_seven_collections_present(self):
        result = adapt_synthetic_feed(sample())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual({k for k in result["batch"] if k in (
            "ea_registry", "run_manifest", "source_manifest", "trade_events",
            "position_snapshots", "account_snapshots", "market_context_refs")}, {
            "ea_registry", "run_manifest", "source_manifest", "trade_events",
            "position_snapshots", "account_snapshots", "market_context_refs"})
        self.assertEqual(result["batch"]["source_manifest"][0]["record_count"], 6)

    def test_P03_cash_flow_is_not_trading_profit(self):
        b = sample()
        raw = get_record(b, "MT5_DEAL")
        flow = copy.deepcopy(raw)
        flow["ref"] = "synthetic-deposit-new"
        flow["kind"] = "MT5_CASH_FLOW"
        flow["values"] = {
            "cash_flow_kind": "DEPOSIT", "amount": "900.00",
            "source_seq": 3, "timestamp_raw": "2026-01-01T10:01:30Z",
            "timestamp_utc": "2026-01-01T10:01:30Z"}
        flow["annotation"] = {
            "event_id": "SYNTH-CASH-3", "run_id": "RUN-1",
            "time_precision": "SECONDS", "timezone_status": "KNOWN_OFFSET",
            "observation_class": "OBSERVED_DIRECT",
            "ea_attribution": {"status": "UNASSIGNED"}}
        b["feeds"][0]["records"].append(flow)
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["validation"]["trading_realized_gross_synthetic"], "0.00")
        self.assertEqual(r["batch"]["trade_events"][-1]["event_type"], "CASH_FLOW")

    def test_P04_refuses_non_synthetic_marker(self):
        b = sample()
        b["synthetic"] = False
        check_fail(self, b, "NON_SYNTHETIC_INPUT")

    def test_P05_refuses_unapproved_schema(self):
        b = sample()
        b["input_schema"] = "REAL_MT5_FEED"
        check_fail(self, b, "INVALID_INPUT_SCHEMA")

    def test_P06_refuses_broker_or_trading_authority(self):
        b = sample()
        b["authority"]["trading"] = True
        check_fail(self, b, "UNAUTHORIZED_INPUT_AUTHORITY")

    def test_P07_refuses_non_synthetic_source(self):
        b = sample()
        b["feeds"][0]["synthetic"] = False
        check_fail(self, b, "NON_SYNTHETIC_SOURCE")

    def test_P08_refuses_invented_source_reference(self):
        b = sample()
        b["feeds"][0]["records"][1]["ref"] = []
        check_fail(self, b, "INVALID_SOURCE_REFERENCE")

    def test_P09_refuses_two_observations_one_raw_record(self):
        b = sample()
        dup = copy.deepcopy(get_record(b, "MT5_DEAL"))
        dup["annotation"]["event_id"] = "FAKE-DEAL"
        b["feeds"][0]["records"].append(dup)
        check_fail(self, b, "DUPLICATE_SOURCE_REFERENCE")

    def test_P10_refuses_unrecognized_event_type(self):
        b = sample()
        get_record(b, "MT5_DEAL")["kind"] = "MT5_TRADE_HISTORY"
        check_fail(self, b, "UNSUPPORTED_SYNTHETIC_TAG")

    def test_P11_refuses_misplaced_money_in_annotation(self):
        b = sample()
        get_record(b, "MT5_DEAL")["annotation"]["profit"] = "9999.00"
        check_fail(self, b, "ANNOTATION_SOURCE_FIELD_OVERRIDE")

    def test_P12_refuses_missing_bound_value(self):
        b = sample()
        del get_record(b, "MT5_DEAL")["values"]["profit"]
        check_fail(self, b, "SOURCE_VALUES_MISSING")

    def test_P13_refuses_floating_point_value(self):
        b = sample()
        get_record(b, "MT5_DEAL")["values"]["volume"] = 0.1
        check_fail(self, b)

    def test_P14_preserves_missing_cost_not_zero(self):
        b = sample()
        get_record(b, "MT5_DEAL")["values"]["commission"] = None
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertIsNone(r["batch"]["trade_events"][1]["commission"])
        self.assertNotEqual(r["validation"]["economic_status"], "FULLY_QUALIFIED")

    def test_P15_tampered_negative_volume_rejected(self):
        b = sample()
        get_record(b, "MT5_DEAL")["values"]["volume"] = "-0.20"
        check_fail(self, b, "INVALID_DEAL_VOLUME")

    def test_P16_refuses_real_run(self):
        b = sample()
        b["run_manifest"][0]["mode"] = "LIVE"
        check_fail(self, b, "REAL_RUN_FORBIDDEN")

    def test_P17_refuses_economic_overclaim(self):
        b = sample()
        b["requested_claim"] = "EA_NET_PNL"
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertIsNone(r["batch"])
        self.assertFalse(r["authority"]["capital"])

    def test_P18_ambiguous_attribution_stays_partial(self):
        b = sample()
        get_record(b, "MT5_DEAL")["annotation"]["ea_attribution"] = {"status": "AMBIGUOUS"}
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["validation"]["overall_status"], "PARTIAL_DESCRIPTIVE_ONLY")

    def test_P19_missing_known_timezone_does_not_mint_utc(self):
        b = sample()
        row = get_record(b, "MT5_DEAL")
        row["annotation"]["timezone_status"] = "UNKNOWN"
        row["values"]["timestamp_utc"] = None
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertIsNone(r["batch"]["trade_events"][1]["timestamp_utc"])

    def test_P20_rejects_future_context_as_decision_data(self):
        b = sample()
        get_record(b, "MT5_CONTEXT")["values"]["available_at_utc"] = "2026-01-01T11:00:00Z"
        check_fail(self, b, "LOOKAHEAD_CONTEXT_FORBIDDEN")

    def test_P21_rejects_wrong_run_binding(self):
        b = sample()
        get_record(b, "MT5_DEAL")["annotation"]["run_id"] = "MADE-UP-RUN"
        check_fail(self, b, "EVENT_RUN_SOURCE_MISMATCH")

    def test_P22_rejects_derived_pnl_without_qualified_rule(self):
        b = sample()
        get_record(b, "MT5_DEAL")["annotation"]["observation_class"] = "DERIVED_DETERMINISTIC"
        check_fail(self, b, "NON_DIRECT_SYNTHETIC_OBSERVATION")

    def test_P23_rejects_malformed_structures(self):
        for invalid in (None, [], {"input_schema": "EA03_P1_SYNTHETIC_FEED_V0_1"},
                        {"input_schema": ["EA03_P1_SYNTHETIC_FEED_V0_1"]}):
            with self.subTest(invalid=type(invalid).__name__):
                check_fail(self, invalid)

    def test_P24_idempotent_generated_evidence(self):
        a = adapt_synthetic_feed(sample())
        b = adapt_synthetic_feed(sample())
        self.assertEqual(a["batch"], b["batch"])
        self.assertEqual(a["batch"]["source_manifest"][0]["sha256"],
                         b["batch"]["source_manifest"][0]["sha256"])

    def test_P25_deny_unrecognized_annotation_key(self):
        b = sample()
        get_record(b, "MT5_DEAL")["annotation"]["invented_magic_truth"] = 123
        check_fail(self, b, "INVALID_ANNOTATION_FIELD")

    def test_P26_deny_real_ea_identity(self):
        b = sample()
        b["ea_registry"][0]["ownership"] = "THIRD_PARTY_PRIVATE"
        check_fail(self, b, "NON_SYNTHETIC_EA_IDENTITY")

    def test_P27_record_values_are_not_changed_by_adapter(self):
        b = sample()
        get_record(b, "MT5_DEAL")["values"]["profit"] = "3.456700"
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["batch"]["trade_events"][1]["profit"], "3.456700")
        self.assertEqual(r["batch"]["source_manifest"][0]["raw_records"][2]["values"]["profit"], "3.456700")


if __name__ == "__main__":
    unittest.main()


class TestEA03P1AccountingBoundaries(unittest.TestCase):
    def _additional_deal(self, b, *, entry="IN", vol="0.05", side="BUY"):
        rec = copy.deepcopy(get_record(b, "MT5_DEAL"))
        rec["ref"] = "deal-2"
        rec["values"].update(native_deal_id="2002", entry_type=entry, volume=vol,
                             side=side, source_seq=3, timestamp_raw="2026-01-01T10:01:30Z",
                             timestamp_utc="2026-01-01T10:01:30Z")
        rec["annotation"]["event_id"] = "E-DEAL-2"
        b["feeds"][0]["records"].append(rec)
        return rec

    def _additional_position(self, b):
        rec = copy.deepcopy(get_record(b, "MT5_POSITION_SNAPSHOT"))
        rec["ref"] = "pos-2"
        rec["values"].update(native_position_id="3002", side="SELL")
        rec["annotation"]["snapshot_id"] = "POS-SNAP-2"
        b["feeds"][0]["records"].append(rec)
        return rec

    def test_P28_two_fills_same_order_preserve_distinct_deal_ids(self):
        b = sample()
        self._additional_deal(b)
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual([x["native_deal_id"] for x in r["batch"]["trade_events"]
                          if x["event_type"] == "DEAL"], ["2001", "2002"])
        self.assertEqual(r["batch"]["source_manifest"][0]["record_count"], 7)

    def test_P29_bounded_partial_close_with_remaining_position(self):
        b = sample()
        b["run_manifest"][0].update(deal_replay_qualified=True, opening_state="FLAT")
        self._additional_deal(b, entry="OUT", vol="0.05", side="SELL")
        get_record(b, "MT5_POSITION_SNAPSHOT")["values"]["volume"] = "0.05"
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["batch"]["position_snapshots"][0]["volume"], "0.05")

    def test_P30_netting_one_aggregate_position_is_descriptive(self):
        b = sample()
        b["run_manifest"][0]["position_mode"] = "NETTING"
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(len(r["batch"]["position_snapshots"]), 1)

    def test_P31_hedging_two_distinct_positions_valid(self):
        b = sample()
        self._additional_position(b)
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(len(r["batch"]["position_snapshots"]), 2)

    def test_P32_netting_conflicting_aggregate_positions_rejected(self):
        b = sample()
        b["run_manifest"][0]["position_mode"] = "NETTING"
        self._additional_position(b)
        check_fail(self, b, "MULTIPLE_NETTING_POSITIONS_SAME_SYMBOL")

    def test_P33_floating_loss_preserved_and_never_claims_ea_risk(self):
        b = sample()
        get_record(b, "MT5_POSITION_SNAPSHOT")["values"]["floating_pnl"] = "-900.50"
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["batch"]["position_snapshots"][0]["floating_pnl"], "-900.50")
        self.assertEqual(r["validation"]["scientific_status"], "NOT_ASSESSED")
        self.assertFalse(r["validation"]["trading_authority"])

    def test_P34_simultaneous_order_deal_time_not_minted_as_causality(self):
        b = sample()
        get_record(b, "MT5_DEAL")["values"].update(
            timestamp_raw="2026-01-01T10:00:00Z",
            timestamp_utc="2026-01-01T10:00:00Z")
        r = adapt_synthetic_feed(b)
        self.assertEqual(r["status"], "PASS", r)
        self.assertIn("SIMULTANEOUS_EVENTS_CAUSAL_ORDER_UNKNOWN",
                      r["validation"]["warnings"])
