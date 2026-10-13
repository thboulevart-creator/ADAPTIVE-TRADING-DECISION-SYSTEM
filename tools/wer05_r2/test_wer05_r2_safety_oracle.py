"""Pure synthetic fixtures only. Neither OS nor guest environment is touched."""
from dataclasses import replace
import unittest
from wer05_r2_safety_oracle import MockObservation, Decision, evaluate


BASE = frozenset({"preexisting-CmService-saved-template"})
GUEST = "synthetic-guest-unique-a"


def fixture(**kw):
    obs = MockObservation(
        monotonic_elapsed_seconds=10, previous_monotonic_elapsed_seconds=0,
        baseline_ids=BASE, current_ids=BASE | {GUEST},
        claimed_guest_id=GUEST, trusted_unique_launch_binding=True,
        hcs_identity_metadata_qualified=True, local_watchdog_independent=True,
        privileged_control_permission_proven=True,
        graceful_path_qualified=True, fallback_path_qualified=True,
        remote_control_connected=True, graceful_proposed=False,
        fallback_proposed=False, host_process_absence_confirmed=False,
        independent_lifecycle_terminal_record=False,
    )
    return replace(obs, **kw)


class SafetyGateTests(unittest.TestCase):
    def test_01_no_guest_attestation(self):
        self.assertEqual(evaluate(fixture(trusted_unique_launch_binding=False)), Decision.STOP_UNQUALIFIED)

    def test_02_no_identity_metadata(self):
        self.assertEqual(evaluate(fixture(hcs_identity_metadata_qualified=False)), Decision.STOP_UNQUALIFIED)

    def test_03_preexisting_vm_target(self):
        self.assertEqual(evaluate(fixture(claimed_guest_id=next(iter(BASE)))), Decision.STOP_UNQUALIFIED)

    def test_04_multiple_new_vms(self):
        self.assertEqual(evaluate(fixture(current_ids=BASE | {GUEST, "unrelated"})), Decision.STOP_UNQUALIFIED)

    def test_05_no_watchdog(self):
        self.assertEqual(evaluate(fixture(local_watchdog_independent=False)), Decision.STOP_UNQUALIFIED)

    def test_06_no_privileges(self):
        self.assertEqual(evaluate(fixture(privileged_control_permission_proven=False)), Decision.STOP_UNQUALIFIED)

    def test_07_fallback_not_qualified(self):
        self.assertEqual(evaluate(fixture(fallback_path_qualified=False)), Decision.STOP_UNQUALIFIED)

    def test_08_early_observe(self):
        self.assertEqual(evaluate(fixture(monotonic_elapsed_seconds=239)), Decision.OBSERVE)

    def test_09_graceful_at_240(self):
        self.assertEqual(evaluate(fixture(monotonic_elapsed_seconds=240)), Decision.PROPOSE_GRACEFUL)

    def test_10_fallback_at_270(self):
        self.assertEqual(evaluate(fixture(monotonic_elapsed_seconds=270,graceful_proposed=True)), Decision.PROPOSE_FALLBACK)

    def test_11_remote_disconnected_not_decision_authority(self):
        self.assertEqual(evaluate(fixture(monotonic_elapsed_seconds=240,remote_control_connected=False)), Decision.PROPOSE_GRACEFUL)

    def test_12_deadline_breach(self):
        self.assertEqual(evaluate(fixture(monotonic_elapsed_seconds=300, graceful_proposed=True,fallback_proposed=True)), Decision.DEADLINE_BREACH)

    def test_13_closed_without_independent_record(self):
        self.assertEqual(evaluate(fixture(current_ids=BASE,graceful_proposed=True,host_process_absence_confirmed=True)),Decision.CLOSED_PENDING_INDEPENDENT_PROOF)

    def test_14_closed_without_host_process_proof(self):
        self.assertEqual(evaluate(fixture(current_ids=BASE,graceful_proposed=True,independent_lifecycle_terminal_record=True)),Decision.CLOSED_PENDING_INDEPENDENT_PROOF)

    def test_15_closed_with_all_independent_proofs(self):
        self.assertEqual(evaluate(fixture(current_ids=BASE,graceful_proposed=True,host_process_absence_confirmed=True,independent_lifecycle_terminal_record=True)), Decision.CLOSED_PROVEN_IN_MODEL)

    def test_16_reversed_clock(self):
        self.assertEqual(evaluate(fixture(monotonic_elapsed_seconds=50,previous_monotonic_elapsed_seconds=80)),Decision.STOP_UNQUALIFIED)

    def test_17_no_post_launch_hcs_system(self):
        self.assertEqual(evaluate(fixture(current_ids=BASE)),Decision.STOP_UNQUALIFIED)

    def test_18_unknown_guest_identifier(self):
        self.assertEqual(evaluate(fixture(claimed_guest_id=None)),Decision.STOP_UNQUALIFIED)

    def test_19_no_graceful_path(self):
        self.assertEqual(evaluate(fixture(graceful_path_qualified=False)),Decision.STOP_UNQUALIFIED)

    def test_20_closed_with_unrelated_system(self):
        self.assertEqual(evaluate(fixture(current_ids=BASE | {"unrelated"},graceful_proposed=True,host_process_absence_confirmed=True,independent_lifecycle_terminal_record=True)),Decision.STOP_UNQUALIFIED)

if __name__=='__main__':
    unittest.main(verbosity=2)
