"""EA-03-P2-I1 RED/GREEN checks: synthetic read facade, never a terminal client."""
import copy
import inspect
import json
import unittest
from pathlib import Path

from src.ea_observation.mock_read_firewall import (
    MockReadFirewall, PROTOCOL_VERSION, READ_CAPABILITIES,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "ea03_p2_i1_mock_feed_v0_1.json"

def fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

def req(capability, *, filters=None, request_id="MOCK-REQUEST-01"):
    if filters is None:
        filters = {} if capability == "read_ea_registry" else {"run_id": "MOCK-RUN-01"}
    return {"protocol_version": PROTOCOL_VERSION, "request_id": request_id,
            "capability": capability, "filters": filters}

def denied(test, fw, request):
    r = fw.execute(request)
    test.assertEqual(r["status"], "DENIED", r)
    test.assertEqual(r["records"], [])
    test.assertEqual(r["authority"],
                     {"trading": False, "capital": False, "real_data": False, "network": False})
    return r


class MockReadFirewallTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.fw = MockReadFirewall(self.data)

    def test_I01_protocol_is_fixed(self):
        self.assertEqual(PROTOCOL_VERSION, "ATDS_EA03_P2_I1_READ_V0_1")

    def test_I02_seven_read_capabilities_only(self):
        self.assertEqual(READ_CAPABILITIES, frozenset({
            "read_ea_registry", "read_run_manifest", "read_orders",
            "read_deals", "read_positions", "read_account_snapshots",
            "read_market_context"}))

    def test_I03_all_allowed_reads_return_mock_records(self):
        for capability in sorted(READ_CAPABILITIES):
            with self.subTest(capability=capability):
                r = self.fw.execute(req(capability))
                self.assertEqual(r["status"], "OK", r)
                self.assertEqual(r["source"], "SYNTHETIC_MOCK")
                self.assertEqual(len(r["records"]), 1)
                self.assertTrue(r["records"][0]["synthetic"])

    def test_I04_read_deal_fields_do_not_invent_cost(self):
        r = self.fw.execute(req("read_deals"))
        self.assertIsNone(r["records"][0]["commission"])
        self.assertEqual(r["records"][0]["volume"], "0.10")

    def test_I05_read_position_preserves_floating_loss(self):
        self.assertEqual(self.fw.execute(req("read_positions"))["records"][0]["floating_pnl"],
                         "-12.50")

    def test_I06_send_order_denied(self):
        denied(self, self.fw, req("order_send"))

    def test_I07_close_position_denied(self):
        denied(self, self.fw, req("close_position"))

    def test_I08_change_stop_loss_denied(self):
        denied(self, self.fw, req("order_modify"))

    def test_I09_account_login_denied(self):
        denied(self, self.fw, req("login"))

    def test_I10_terminal_initialize_denied(self):
        denied(self, self.fw, req("initialize"))

    def test_I11_copy_rates_denied_not_implemented(self):
        denied(self, self.fw, req("copy_rates_from_pos"))

    def test_I12_case_perturbation_denied(self):
        denied(self, self.fw, req("READ_ORDERS"))

    def test_I13_whitespace_perturbation_denied(self):
        denied(self, self.fw, req(" read_orders "))

    def test_I14_nested_trade_request_denied(self):
        b = req("read_orders")
        b["filters"]["order_send"] = {"symbol": "EURUSD", "volume": "1"}
        denied(self, self.fw, b)

    def test_I15_extra_root_trade_instruction_denied(self):
        b = req("read_orders")
        b["order"] = "BUY"
        denied(self, self.fw, b)

    def test_I16_method_injection_denied(self):
        b = req("read_orders")
        b["callback"] = lambda: True
        denied(self, self.fw, b)

    def test_I17_class_internal_method_not_a_capability(self):
        denied(self, self.fw, req("__class__"))
        denied(self, self.fw, req("__getattribute__"))

    def test_I18_unknown_run_returns_empty_not_other_run(self):
        r = self.fw.execute(req("read_deals", filters={"run_id": "MOCK-UNKNOWN"}))
        self.assertEqual(r["status"], "OK")
        self.assertEqual(r["records"], [])

    def test_I19_unscoped_deal_read_denied(self):
        denied(self, self.fw, req("read_deals", filters={}))

    def test_I20_registry_cannot_accept_run_filter(self):
        denied(self, self.fw, req("read_ea_registry", filters={"run_id": "MOCK-RUN-01"}))

    def test_I21_response_is_not_a_live_authority(self):
        for cap in READ_CAPABILITIES:
            r = self.fw.execute(req(cap))
            self.assertEqual(r["authority"],
                             {"trading": False, "capital": False, "real_data": False, "network": False})
            self.assertNotIn("callback", r)
            self.assertNotIn("connector", r)

    def test_I22_returned_data_modification_does_not_mutate_store(self):
        r = self.fw.execute(req("read_deals"))
        r["records"][0]["volume"] = "9999"
        self.assertEqual(self.fw.execute(req("read_deals"))["records"][0]["volume"], "0.10")

    def test_I23_mutating_original_fixture_does_not_mutate_store(self):
        self.data["collections"]["deals"][0]["volume"] = "9999"
        self.assertEqual(self.fw.execute(req("read_deals"))["records"][0]["volume"], "0.10")

    def test_I24_refuse_real_dataset_marker(self):
        b = fixture()
        b["synthetic"] = False
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I25_refuse_forged_capital_authority(self):
        b = fixture()
        b["authority"]["capital"] = True
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I26_refuse_forged_network_authority(self):
        b = fixture()
        b["authority"]["network"] = True
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I27_refuse_real_mode_in_manifest(self):
        b = fixture()
        b["collections"]["run_manifest"][0]["mode"] = "LIVE"
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I28_refuse_private_ea_in_mock_fixture(self):
        b = fixture()
        b["collections"]["ea_registry"][0]["ownership"] = "THIRD_PARTY_PRIVATE"
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I29_refuse_record_synthetic_false(self):
        b = fixture()
        b["collections"]["deals"][0]["synthetic"] = False
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I30_refuse_real_connection_credential_in_mock_data(self):
        b = fixture()
        b["collections"]["account_snapshots"][0]["login"] = "123456"
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I31_refuse_binary_floats_in_mock_data(self):
        b = fixture()
        b["collections"]["positions"][0]["floating_pnl"] = 1.25
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I32_refuse_nonfinite_numbers_in_mock_data(self):
        b = fixture()
        b["collections"]["deals"][0]["profit"] = "NaN"
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I33_refuse_unknown_fixture_collection(self):
        b = fixture()
        b["collections"]["commands"] = []
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I34_refuse_missing_fixture_collection(self):
        b = fixture()
        del b["collections"]["orders"]
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I35_refuse_duplicate_run_id(self):
        b = fixture()
        b["collections"]["run_manifest"].append(copy.deepcopy(b["collections"]["run_manifest"][0]))
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I36_refuse_malformed_request(self):
        for b in (None, "", [], 4, {"protocol_version": PROTOCOL_VERSION},
                  {"protocol_version": [PROTOCOL_VERSION], "capability": "read_orders",
                   "request_id": "MOCK", "filters": {"run_id": "MOCK-RUN-01"}}):
            with self.subTest(type=str(type(b))):
                denied(self, self.fw, b)

    def test_I37_refuse_wrong_protocol(self):
        b = req("read_deals")
        b["protocol_version"] = "ATDS_EA03_P2_I1_LIVE_V1"
        denied(self, self.fw, b)

    def test_I38_refuse_invalid_request_id(self):
        for rid in ("", "../token", "x" * 129, None):
            denied(self, self.fw, req("read_deals", request_id=rid))

    def test_I39_refuse_nested_or_unhashable_capability(self):
        for cap in (["read_orders"], {"read_orders": True}, 0, True):
            denied(self, self.fw, req(cap))

    def test_I40_no_injected_callback_or_backend_parameter(self):
        signature = inspect.signature(MockReadFirewall)
        self.assertEqual(list(signature.parameters), ["dataset"])
        self.assertFalse(hasattr(self.fw, "order_send"))
        self.assertFalse(hasattr(self.fw, "login"))
        self.assertFalse(hasattr(self.fw, "initialize"))

    def test_I41_refuse_json_serializable_but_unknown_parameter(self):
        b = req("read_orders")
        b["filters"]["offset"] = 12
        denied(self, self.fw, b)

    def test_I42_adversarial_input_mutation_never_promotes_status(self):
        b = req("read_orders")
        b["capability"] = "order_send"
        for payload in ({}, {"run_id": "MOCK-RUN-01"}, {"run_id": "MOCK-RUN-01", "volume": "5"}):
            b["filters"] = payload
            denied(self, self.fw, b)

    def test_I43_fixture_unknown_root_field_denied(self):
        b = fixture()
        b["connector_uri"] = "example://nonexistent"
        with self.assertRaises(ValueError):
            MockReadFirewall(b)

    def test_I44_request_does_not_mutate_original_request(self):
        b = req("read_deals")
        prior = copy.deepcopy(b)
        self.fw.execute(b)
        self.assertEqual(b, prior)

    def test_I45_denied_response_does_not_leak_records(self):
        r = denied(self, self.fw, req("account_info"))
        self.assertEqual(r["source"], "SYNTHETIC_MOCK")
        self.assertEqual(r["errors"], ["CAPABILITY_NOT_GRANTED"])

    def test_I46_preserve_raw_synthetic_timestamp(self):
        result = self.fw.execute(req("read_orders"))
        self.assertEqual(result["records"][0]["event_time_utc"], "2026-01-01T10:00:00Z")

if __name__ == "__main__":
    unittest.main()
