"""D1 scenarios T15-T26 and targeted adversarial breakers; entirely synthetic."""
import copy
import unittest

from src.ea_observation.provenance import sha256_records
from src.ea_observation.validation import validate_batch
from test_ea_observation_schema import sample, extra_deal, add_source_ref, sync_source


class TestExtendedScenarios(unittest.TestCase):
    def test_T15_missing_set_identity_stays_unknown(self):
        b = sample()
        b["ea_registry"][0]["config_sha256"] = None
        b["run_manifest"][0]["config_sha256"] = None
        b["requested_claim"] = "EA_NET_PNL"
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "BLOCKED")
        self.assertEqual(r["structural_status"], "STRUCTURALLY_VALID")

    def test_T16_symbol_equivalence_not_assumed(self):
        b = sample()
        b["market_context_refs"][0]["market_symbol"] = "OTHER-BROKER-NAS"
        self.assertIn("UNATTESTED_SYMBOL_EQUIVALENCE", validate_batch(b)["errors"])

    def test_T17_future_context_forbidden(self):
        b = sample()
        b["market_context_refs"][0]["available_at_utc"] = "2026-01-01T10:05:00Z"
        self.assertIn("LOOKAHEAD_CONTEXT_FORBIDDEN", validate_batch(b)["errors"])

    def test_T18_synthetic_batch_cannot_mint_orders(self):
        b = sample()
        b["requested_claim"] = "TRADING_AUTHORIZATION"
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "BLOCKED")
        self.assertFalse(r["trading_authority"])

    def test_T19_dca_floating_losses_block_unproven_exact_risk(self):
        b = sample()
        extra_deal(b, "E-DEAL-2", "2002", entry="IN", volume="0.10", side="BUY")
        b["position_snapshots"][0].update(volume="0.20", floating_pnl="-150.00")
        sync_source(b, b["position_snapshots"][0])
        b["requested_claim"] = "EXACT_EA_RISK"
        r = validate_batch(b)
        self.assertIn("EXACT_EA_RISK_UNPROVEN", r["warnings"])
        self.assertEqual(b["position_snapshots"][0]["floating_pnl"], "-150.00")

    def test_T20_real_provenance_in_synthetic_fixture_rejected(self):
        b = sample()
        b["source_manifest"][0].update(kind="MT5_HISTORY_EXPORT", synthetic=False)
        self.assertIn("REAL_SOURCE_IN_SYNTHETIC_SCOPE", validate_batch(b)["errors"])

    def test_T21_deposit_not_realized_trading_pnl(self):
        b = sample()
        add_source_ref(b, "cash-1", "BALANCE_OPERATION")
        cash = copy.deepcopy(b["trade_events"][0])
        cash.update(event_id="E-CASH", source_record_ref="cash-1", source_seq=3,
                    event_type="CASH_FLOW", timestamp_raw="2026-01-01T10:02:00Z",
                    timestamp_utc="2026-01-01T10:02:00Z", cash_flow_kind="DEPOSIT",
                    amount="500.00")
        cash["ea_attribution"] = {"status": "UNASSIGNED"}
        cash.pop("native_order_id", None)
        cash.pop("order_state", None)
        b["trade_events"].append(cash)
        sync_source(b, cash)
        r = validate_batch(b)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["trading_realized_gross_synthetic"], "0.00")

    def test_T22_shared_netting_exact_EA_ownership_fails(self):
        b = sample()
        b["run_manifest"][0].update(ea_isolated=False, position_mode="NETTING")
        r = validate_batch(b)
        self.assertIn("UNPROVEN_EXACT_ATTRIBUTION", r["errors"])

    def test_T23_final_equity_only_cannot_show_exact_drawdown(self):
        b = sample()
        b["requested_claim"] = "EXACT_DRAWDOWN"
        self.assertEqual(validate_batch(b)["overall_status"], "BLOCKED")

    def test_T24_same_binary_different_parameter_sets_distinct(self):
        b = sample()
        second = copy.deepcopy(b["run_manifest"][0])
        second.update(run_id="RUN-2", config_sha256="c" * 64)
        b["run_manifest"].append(second)
        r = validate_batch(b)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["configuration_count"], 2)

    def test_T25_unknown_conversion_blocks_net(self):
        b = sample()
        b["run_manifest"][0]["cost_conversion_status"] = "UNKNOWN"
        b["requested_claim"] = "EA_NET_PNL"
        self.assertEqual(validate_batch(b)["overall_status"], "BLOCKED")

    def test_T26_real_trading_claim_disguised_as_synthetic(self):
        b = sample()
        b["run_manifest"][0]["mode"] = "REAL"
        self.assertIn("REAL_RUN_FORBIDDEN", validate_batch(b)["errors"])


class TestAdversarial(unittest.TestCase):
    def test_B01_binary_float_rejected(self):
        b = sample()
        b["trade_events"][1]["price"] = 100.0
        self.assertIn("BINARY_FLOAT_FORBIDDEN", validate_batch(b)["errors"])

    def test_B02_unbound_ea_attestation(self):
        b = sample()
        b["trade_events"][1]["ea_attribution"]["binding_evidence_ref"] = "MISSING"
        self.assertIn("UNPROVEN_EXACT_ATTRIBUTION", validate_batch(b)["errors"])

    def test_B03_unbound_source_record(self):
        b = sample()
        b["trade_events"][1]["source_record_ref"] = "MISSING"
        self.assertIn("UNBOUND_SOURCE_RECORD", validate_batch(b)["errors"])

    def test_B04_native_deal_id_collision(self):
        b = sample()
        extra_deal(b, "E-DEAL-2", "2001", entry="IN", volume="0.30", side="BUY")
        self.assertIn("CONFLICTING_NATIVE_DEAL", validate_batch(b)["errors"])

    def test_B05_unknown_timezone_no_fake_UTC(self):
        b = sample()
        b["trade_events"][1]["timezone_status"] = "UNKNOWN"
        self.assertIn("FABRICATED_UTC_FROM_UNKNOWN_TIMEZONE", validate_batch(b)["errors"])

    def test_B06_double_netting_position(self):
        b = sample()
        b["run_manifest"][0]["position_mode"] = "NETTING"
        p = copy.deepcopy(b["position_snapshots"][0])
        p.update(snapshot_id="POS-OTHER", native_position_id="999")
        b["position_snapshots"].append(p)
        self.assertIn("MULTIPLE_NETTING_POSITIONS_SAME_SYMBOL", validate_batch(b)["errors"])

    def test_B07_overclose_in_bounded_replay(self):
        b = sample()
        b["run_manifest"][0].update(deal_replay_qualified=True, opening_state="FLAT")
        extra_deal(b, "E-DEAL-2", "2002", entry="OUT", volume="0.50")
        self.assertIn("REPLAY_OVER_CLOSE_OR_INVALID_SIDE", validate_batch(b)["errors"])

    def test_B08_hedging_inout_rejected(self):
        b = sample()
        extra_deal(b, "E-DEAL-2", "2002", entry="INOUT", volume="0.20")
        self.assertIn("NETTING_REVERSAL_IN_HEDGING", validate_batch(b)["errors"])

    def test_B09_unknown_claim_fails(self):
        b = sample()
        b["requested_claim"] = "GUARANTEED_PROFIT"
        self.assertIn("UNKNOWN_CLAIM", validate_batch(b)["errors"])

    def test_B10_unauthorized_broker_flag(self):
        b = sample()
        b["authority"]["trading"] = True
        self.assertIn("AUTHORITY_NOT_FAIL_CLOSED", validate_batch(b)["errors"])

    def test_B11_missing_immutable_source_id(self):
        b = sample()
        b["source_manifest"][0]["sha256"] = "0" * 64
        self.assertIn("RAW_SOURCE_HASH_MISMATCH", validate_batch(b)["errors"])

    def test_B12_partial_close_snapshot_wrong_size(self):
        b = sample()
        b["run_manifest"][0].update(deal_replay_qualified=True, opening_state="FLAT")
        extra_deal(b, "E-DEAL-2", "2002", entry="OUT", volume="0.05")
        b["position_snapshots"][0]["volume"] = "0.20"
        self.assertIn("REPLAY_SNAPSHOT_MISMATCH", validate_batch(b)["errors"])

    def test_B13_funding_operation_not_profit(self):
        b = sample()
        b["trade_events"][1]["profit"] = None
        self.assertIsNone(validate_batch(b)["trading_realized_gross_synthetic"])

    def test_B14_unknown_full_case_not_economic(self):
        b = sample()
        b["source_manifest"][0]["completeness"]["deals"] = "PARTIAL"
        b["requested_claim"] = "EA_NET_PNL"
        self.assertEqual(validate_batch(b)["overall_status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()


class TestClaimFirewall(unittest.TestCase):
    def test_B15_complete_synthetic_cost_is_not_economic_authority(self):
        b = sample()
        b["requested_claim"] = "EA_NET_PNL"
        r = validate_batch(b)
        self.assertEqual(r["economic_status"], "STRUCTURALLY_ELIGIBLE_SYNTHETIC_ONLY")
        self.assertEqual(r["overall_status"], "BLOCKED")
        self.assertIn("ECONOMIC_CLAIM_OUTSIDE_D1", r["warnings"])

    def test_B16_claimed_complete_equity_not_exact_path_proof(self):
        b = sample()
        b["requested_claim"] = "EXACT_DRAWDOWN"
        b["run_manifest"][0]["equity_coverage"] = "COMPLETE_MARKED_PATH"
        self.assertEqual(validate_batch(b)["overall_status"], "BLOCKED")

    def test_B17_claimed_complete_risk_not_authorized(self):
        b = sample()
        b["requested_claim"] = "EXACT_EA_RISK"
        b["run_manifest"][0]["equity_coverage"] = "COMPLETE_MARKED_PATH"
        b["source_manifest"][0]["completeness"]["positions"] = "COMPLETE"
        b["source_manifest"][0]["completeness"]["account"] = "COMPLETE"
        self.assertEqual(validate_batch(b)["overall_status"], "BLOCKED")

    def test_B18_all_real_capabilities_remain_false(self):
        b = sample()
        for claim in ("DESCRIPTIVE", "EA_NET_PNL", "PORTFOLIO_NET_PNL",
                      "EXACT_DRAWDOWN", "EXACT_EA_RISK", "TRADING_AUTHORIZATION"):
            b["requested_claim"] = claim
            r = validate_batch(b)
            self.assertFalse(r["real_observation_authority"])
            self.assertFalse(r["trading_authority"])
            self.assertFalse(r["capital_authority"])
            self.assertEqual(r["scientific_status"], "NOT_ASSESSED")


class TestCR1RedTargets(unittest.TestCase):
    """Mandatory CR1 controls. Run RED against unmodified D1 candidate."""
    def test_CR1_F01_tampered_profit_rejected_without_source_change(self):
        b = sample()
        b["trade_events"][1]["profit"] = "999999.99"
        self.assertIn("SOURCE_VALUE_MISMATCH", validate_batch(b)["errors"])

    def test_CR1_F01_tampered_floating_exposure_rejected(self):
        b = sample()
        b["position_snapshots"][0]["floating_pnl"] = "8888888.00"
        self.assertIn("SOURCE_VALUE_MISMATCH", validate_batch(b)["errors"])

    def test_CR1_F02_two_distinct_deals_same_source_ref(self):
        b = sample()
        other = copy.deepcopy(b["trade_events"][1])
        other.update(event_id="DUPLICATED", native_deal_id="ALT-001", profit="100.00")
        b["trade_events"].append(other)
        self.assertIn("SOURCE_RECORD_CARDINALITY_VIOLATION", validate_batch(b)["errors"])

    def test_CR1_F03_negative_deal_volume_fails(self):
        b = sample()
        b["trade_events"][1]["volume"] = "-100.00"
        self.assertIn("INVALID_DEAL_VOLUME", validate_batch(b)["errors"])

    def test_CR1_F03_zero_deal_volume_fails(self):
        b = sample()
        b["trade_events"][1]["volume"] = "0"
        self.assertIn("INVALID_DEAL_VOLUME", validate_batch(b)["errors"])

    def test_CR1_F03_bad_direction_fails(self):
        b = sample()
        b["trade_events"][1]["side"] = "UPSIDE"
        self.assertIn("INVALID_DEAL_SIDE", validate_batch(b)["errors"])

    def test_CR1_F04_unhashable_record_ref_is_safe(self):
        b = sample()
        b["trade_events"][1]["source_record_ref"] = []
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "FAIL")
        self.assertIn("INVALID_INPUT", r["errors"])

    def test_CR1_F04_unhashable_claim_is_safe(self):
        b = sample()
        b["requested_claim"] = []
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "FAIL")
        self.assertIn("INVALID_INPUT", r["errors"])

    def test_CR1_F04_nonfinite_extension_is_safe(self):
        b = sample()
        b["trade_events"][1]["weird_extra"] = float("nan")
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "FAIL")
        self.assertIn("INVALID_INPUT", r["errors"])

    def test_CR1_F05_negative_price_unattested_is_uncertain(self):
        b = sample()
        b["trade_events"][1]["price"] = "-3.50"
        r = validate_batch(b)
        self.assertIn("PRICE_SEMANTICS_UNATTESTED", r["warnings"])
        self.assertNotEqual(r["overall_status"], "STRUCTURALLY_VALID")

    def test_CR1_F05_attested_nonnegative_symbol_blocks_negative(self):
        b = sample()
        b["trade_events"][1]["price"] = "-3.50"
        b["run_manifest"][0]["instrument_price_spec"] = {"symbol": "SYNTH-NAS",
            "minimum_price": "0", "source_id": "SRC-1", "source_record_ref": "spec-1"}
        add_source_ref(b, "spec-1", "INSTRUMENT_SPEC")
        raw = b["source_manifest"][0]["raw_records"][-1]
        raw["values"] = {"symbol": "SYNTH-NAS", "minimum_price": "0"}
        b["source_manifest"][0]["sha256"] = sha256_records(b["source_manifest"][0]["raw_records"])
        sync_source(b, b["trade_events"][1])
        r = validate_batch(b)
        self.assertIn("PRICE_BELOW_ATTESTED_MINIMUM", r["errors"])


class TestCR1IndependentRebreak(unittest.TestCase):
    """Additional vectors identified after the original RED set; retained as regressions."""
    def test_CR1_R01_commission_changed_without_source_change(self):
        b = sample()
        b["trade_events"][1]["commission"] = "300.00"
        self.assertIn("SOURCE_VALUE_MISMATCH", validate_batch(b)["errors"])

    def test_CR1_R02_equity_changed_without_source_change(self):
        b = sample()
        b["account_snapshots"][0]["equity"] = "99999.00"
        self.assertIn("SOURCE_VALUE_MISMATCH", validate_batch(b)["errors"])

    def test_CR1_R03_forged_derived_profit_not_qualified(self):
        b = sample()
        row = b["trade_events"][1]
        row["observation_class"] = "DERIVED_DETERMINISTIC"
        row["profit"] = "5555.55"
        row["derivation"] = {
            "rule_id": "FAKE", "source_record_ref": row["source_record_ref"],
            "output_field": "profit",
        }
        r = validate_batch(b)
        self.assertIn("DERIVATION_RULE_UNQUALIFIED", r["errors"])
        self.assertIsNone(r["trading_realized_gross_synthetic"])

    def test_CR1_R04_inferred_profit_not_accounted(self):
        b = sample()
        row = b["trade_events"][1]
        row["observation_class"] = "INFERRED_HYPOTHESIS"
        row["profit"] = "4444.44"
        r = validate_batch(b)
        self.assertIsNone(r["trading_realized_gross_synthetic"])
        self.assertEqual(r["economic_status"], "INSUFFICIENT_FOR_ECONOMIC_CLAIM")

    def test_CR1_R05_zero_position_volume_fails(self):
        b = sample()
        b["position_snapshots"][0]["volume"] = "0"
        self.assertIn("INVALID_POSITION_VOLUME", validate_batch(b)["errors"])

    def test_CR1_R06_string_attestation_cannot_be_exact(self):
        b = sample()
        b["run_manifest"][0]["ea_isolated"] = "true"
        self.assertIn("UNPROVEN_EXACT_ATTRIBUTION", validate_batch(b)["errors"])

    def test_CR1_R07_source_sequence_change_requires_source_proof(self):
        b = sample()
        b["trade_events"][1]["source_seq"] = 999
        self.assertIn("SOURCE_VALUE_MISMATCH", validate_batch(b)["errors"])

    def test_CR1_R08_verified_negative_price_bound_is_allowed(self):
        b = sample()
        b["trade_events"][1]["price"] = "-3.50"
        sync_source(b, b["trade_events"][1])
        add_source_ref(b, "spec-negative", "INSTRUMENT_SPEC")
        b["source_manifest"][0]["raw_records"][-1]["values"] = {
            "symbol": "SYNTH-NAS", "minimum_price": "-10.00"}
        b["source_manifest"][0]["sha256"] = sha256_records(
            b["source_manifest"][0]["raw_records"])
        b["run_manifest"][0]["instrument_price_spec"] = {
            "symbol": "SYNTH-NAS", "minimum_price": "-10.00",
            "source_id": "SRC-1", "source_record_ref": "spec-negative"}
        r = validate_batch(b)
        self.assertEqual(r["errors"], [])
        self.assertNotIn("PRICE_SEMANTICS_UNATTESTED", r["warnings"])

    def test_CR1_R09_unattested_price_spec_not_accepted(self):
        b = sample()
        b["run_manifest"][0]["instrument_price_spec"] = {
            "symbol": "SYNTH-NAS", "minimum_price": "0",
            "source_id": "SRC-1", "source_record_ref": "forged-spec"}
        self.assertIn("INSTRUMENT_PRICE_SPEC_UNATTESTED",
                      validate_batch(b)["errors"])

    def test_CR1_R10_no_unhandled_exception_for_nonhashable_source_id(self):
        b = sample()
        b["trade_events"][1]["source_id"] = {"not": "a string"}
        r = validate_batch(b)
        self.assertEqual(r["overall_status"], "FAIL")
        self.assertIn("INVALID_INPUT", r["errors"])
