from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ctrl",ROOT/"src"/"ao_e0_b12_consumption_controller.py")
C=importlib.util.module_from_spec(spec); spec.loader.exec_module(C)

GOOD40="a"*40
GOOD64="b"*64

def gate(**kw):
    d=dict(
        b8_closed=True,
        b12_open=True,
        b12_human_opening_receipt_blob=GOOD40,
        forward_instance_digest=GOOD64,
        cell_identity=C.CELL_IDENTITY,
        strategy_version_identity=C.STRATEGY_VERSION_IDENTITY,
        dr01_adoption_blob=C.DR01_ADOPTION_BLOB,
        base_owner_blob=C.BASE_OWNER_BLOB,
        base_p1_12d_extension_blob=C.BASE_P1_12D_EXTENSION_BLOB,
        result_preexposed=False,
    )
    d.update(kw)
    return C.Gate(**d)

class T(unittest.TestCase):
    def test_01_pristine(self):
        self.assertEqual(C.ConsumptionState().state,"PRISTINE")
    def test_02_metadata_no_consume(self):
        s=C.metadata_preflight(C.ConsumptionState()); self.assertEqual(s.state,"PRISTINE")
    def test_03_b8_required(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"B8_NOT_CLOSED"): C.authorize(C.ConsumptionState(),gate(b8_closed=False))
    def test_04_b12_required(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"B12_NOT_HUMAN_OPEN"): C.authorize(C.ConsumptionState(),gate(b12_open=False))
    def test_05_receipt_required(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"INVALID_B12"): C.authorize(C.ConsumptionState(),gate(b12_human_opening_receipt_blob="bad"))
    def test_06_instance_required(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"INVALID_FORWARD"): C.authorize(C.ConsumptionState(),gate(forward_instance_digest="bad"))
    def test_07_cell(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"CELL_IDENTITY"): C.authorize(C.ConsumptionState(),gate(cell_identity="bad"))
    def test_08_strategy(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"STRATEGY_VERSION"): C.authorize(C.ConsumptionState(),gate(strategy_version_identity="bad"))
    def test_09_dr01(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"DR01_BINDING"): C.authorize(C.ConsumptionState(),gate(dr01_adoption_blob="0"*40))
    def test_10_owner(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"BASE_OWNER"): C.authorize(C.ConsumptionState(),gate(base_owner_blob="0"*40))
    def test_11_p112d(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"P1_12D"): C.authorize(C.ConsumptionState(),gate(base_p1_12d_extension_blob="0"*40))
    def test_12_preexposed(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"RESULT_PREEXPOSED"): C.authorize(C.ConsumptionState(),gate(result_preexposed=True))
    def test_13_authorize(self):
        s=C.authorize(C.ConsumptionState(),gate()); self.assertEqual(s.state,"AUTHORIZED_PENDING_READ")
    def test_14_no_read_before_auth(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"FIRST_READ"): C.first_performance_bearing_read(C.ConsumptionState())
    def test_15_first_read_consumes(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        self.assertEqual(s.state,"CONSUMED_EXPOSED"); self.assertFalse(s.independent_confirmation_eligible)
    def test_16_second_first_read_blocked(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        with self.assertRaisesRegex(C.B12ControllerBlocked,"FIRST_READ"): C.first_performance_bearing_read(s)
    def test_17_failure_before_read_restores_pristine(self):
        s=C.technical_failure(C.authorize(C.ConsumptionState(),gate())); self.assertEqual(s.state,"PRISTINE")
    def test_18_failure_after_read_stays_consumed(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        s=C.technical_failure(s); self.assertEqual(s.state,"TECHNICAL_FAILURE_CONSUMED"); self.assertFalse(s.independent_confirmation_eligible)
    def test_19_terminal_requires_consumption(self):
        with self.assertRaisesRegex(C.B12ControllerBlocked,"TERMINAL_PACKAGE"): C.terminal_package_ready(C.ConsumptionState(),GOOD64)
    def test_20_terminal_package(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        s=C.terminal_package_ready(s,GOOD64); self.assertEqual(s.state,"TERMINAL_PACKAGE_READY")
    def test_21_replay_not_independent(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        r=C.replay_semantics(s,GOOD64); self.assertFalse(r["new_independent_confirmation"]); self.assertFalse(r["pristine_restored"])
    def test_22_replay_wrong_instance(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        with self.assertRaisesRegex(C.B12ControllerBlocked,"REPLAY_INSTANCE_MISMATCH"): C.replay_semantics(s,"c"*64)
    def test_23_no_authority_laundering(self):
        s=C.first_performance_bearing_read(C.authorize(C.ConsumptionState(),gate()))
        self.assertFalse(s.trading_authority); self.assertFalse(s.broker_execution_authority); self.assertFalse(s.capital_authority)

if __name__=="__main__": unittest.main()
