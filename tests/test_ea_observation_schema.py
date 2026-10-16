"""D1 scenarios T01-T14. Synthetic fixtures only; unittest standard library."""
import copy
import json
import unittest
from pathlib import Path

from src.ea_observation.provenance import sha256_records, record_tag, SOURCE_VALUE_FIELDS
from src.ea_observation.validation import validate_batch


FIXTURE = Path(__file__).parent / "fixtures" / "ea_observation_synthetic_v0_1.json"


def sample():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def add_source_ref(b, name, tag="DEAL"):
    raw = b["source_manifest"][0]["raw_records"]
    raw.append({"ref": name, "tag": tag})
    b["source_manifest"][0]["record_count"] = len(raw)
    b["source_manifest"][0]["sha256"] = sha256_records(raw)


def sync_source(b, row):
    """Synchronize a newly invented synthetic source with its intended observation.

    Only use for constructing VALID test fixtures, never for tampering RED cases.
    """
    src = b["source_manifest"][0]
    ref = row["source_record_ref"]
    matching = [x for x in src["raw_records"] if x["ref"] == ref]
    assert len(matching) == 1
    raw = matching[0]
    tag = record_tag(row)
    raw["tag"] = tag
    raw["values"] = {k: row[k] for k in SOURCE_VALUE_FIELDS[tag] if k in row}
    src["sha256"] = sha256_records(src["raw_records"])


def extra_deal(b, eid, native, *, entry="OUT", volume="0.05", side="SELL",
               time="2026-01-01T10:01:30Z", seq=3):
    add_source_ref(b, eid)
    row = copy.deepcopy(b["trade_events"][1])
    row.update(event_id=eid, source_record_ref=eid, source_seq=seq,
               native_deal_id=native, entry_type=entry, volume=volume,
               side=side, timestamp_raw=time, timestamp_utc=time)
    b["trade_events"].append(row)
    sync_source(b, row)
    return row


class TestCoreScenarios(unittest.TestCase):
    def test_T01_valid_synthetic_packet(self):
        r = validate_batch(sample())
        self.assertEqual(r["overall_status"], "STRUCTURALLY_VALID")
        self.assertEqual(r["errors"], [])
        self.assertFalse(r["trading_authority"])
        self.assertEqual(r["scientific_status"], "NOT_ASSESSED")

    def test_T02_modified_source_bytes(self):
        b = sample()
        b["source_manifest"][0]["raw_records"][0]["tag"] = "TAMPERED"
        self.assertIn("RAW_SOURCE_HASH_MISMATCH", validate_batch(b)["errors"])

    def test_T03_duplicate_idempotent_event(self):
        b = sample()
        b["trade_events"].append(copy.deepcopy(b["trade_events"][1]))
        r = validate_batch(b)
        self.assertEqual(r["effective_event_count"], 2)
        self.assertEqual(r["errors"], [])
        self.assertEqual(len(b["trade_events"]), 3)  # originals preserved

    def test_T04_conflicting_same_event_id(self):
        b = sample()
        duplicate = copy.deepcopy(b["trade_events"][1])
        duplicate["volume"] = "5.0"
        b["trade_events"].append(duplicate)
        self.assertIn("CONFLICTING_EVENT_ID", validate_batch(b)["errors"])

    def test_T05_multiple_deals_for_one_order(self):
        b = sample()
        extra_deal(b, "E-DEAL-2", "2002", entry="IN", volume="0.05", side="BUY")
        r = validate_batch(b)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["effective_event_count"], 3)

    def test_T06_partial_close_and_remaining_position(self):
        b = sample()
        b["run_manifest"][0].update(deal_replay_qualified=True, opening_state="FLAT")
        extra_deal(b, "E-DEAL-2", "2002")
        b["position_snapshots"][0]["volume"] = "0.05"
        sync_source(b, b["position_snapshots"][0])
        self.assertEqual(validate_batch(b)["errors"], [])

    def test_T07_netting_inout_reversal(self):
        b = sample()
        b["run_manifest"][0].update(position_mode="NETTING", deal_replay_qualified=True,
                                    opening_state="FLAT")
        extra_deal(b, "E-DEAL-2", "2002", entry="INOUT", volume="0.25")
        b["position_snapshots"][0].update(side="SELL", volume="0.15")
        sync_source(b, b["position_snapshots"][0])
        self.assertEqual(validate_batch(b)["errors"], [])

    def test_T08_hedging_independent_positions(self):
        b = sample()
        p = copy.deepcopy(b["position_snapshots"][0])
        p.update(snapshot_id="POS-SNAP-2", native_position_id="3002", side="SELL",
                 source_record_ref="pos-2")
        add_source_ref(b, "pos-2", "POSITION_SNAPSHOT")
        b["position_snapshots"].append(p)
        sync_source(b, p)
        self.assertEqual(validate_batch(b)["errors"], [])

    def test_T09_netting_multi_ea_attribution_not_automatic(self):
        b = sample()
        b["run_manifest"][0]["position_mode"] = "NETTING"
        b["run_manifest"][0]["ea_isolated"] = False
        b["requested_claim"] = "EA_NET_PNL"
        for x in b["trade_events"] + b["position_snapshots"]:
            x.get("ea_attribution", x.get("attribution"))["status"] = "AMBIGUOUS"
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "BLOCKED")
        self.assertEqual(r["attribution_status"], "AMBIGUOUS_OR_UNASSIGNED")

    def test_T10_magic_number_not_attribution_evidence(self):
        b = sample()
        b["requested_claim"] = "EA_NET_PNL"
        for row in b["trade_events"]:
            row["magic"] = 101
            row["ea_attribution"]["status"] = "AMBIGUOUS"
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "BLOCKED")
        self.assertIn("UNQUALIFIED_NET_ECONOMIC_CLAIM", r["warnings"])

    def test_T11_unknown_commission_blocks_net(self):
        b = sample()
        b["trade_events"][1]["commission"] = None
        sync_source(b, b["trade_events"][1])
        b["requested_claim"] = "EA_NET_PNL"
        self.assertEqual(validate_batch(b)["overall_status"], "BLOCKED")

    def test_T12_without_equity_history_exact_drawdown_blocked(self):
        b = sample()
        b["requested_claim"] = "EXACT_DRAWDOWN"
        self.assertIn("EXACT_DRAWDOWN_NOT_OBSERVABLE", validate_batch(b)["warnings"])

    def test_T13_arrival_order_not_assumed_causal(self):
        b = sample()
        b["trade_events"].reverse()
        r = validate_batch(b)
        self.assertEqual(r["errors"], [])
        self.assertIn("EVENT_ARRIVAL_NOT_CAUSAL", r["warnings"])

    def test_T14_equal_timestamps_causality_unknown(self):
        b = sample()
        b["trade_events"][1]["timestamp_raw"] = "2026-01-01T10:00:00Z"
        b["trade_events"][1]["timestamp_utc"] = "2026-01-01T10:00:00Z"
        sync_source(b, b["trade_events"][1])
        r = validate_batch(b)
        self.assertEqual(r["errors"], [])
        self.assertIn("SIMULTANEOUS_EVENTS_CAUSAL_ORDER_UNKNOWN", r["warnings"])


if __name__ == "__main__":
    unittest.main()
