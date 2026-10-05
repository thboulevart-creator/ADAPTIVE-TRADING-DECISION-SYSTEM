from tools.ao_e0_b8_m06_recovery import load, diagnostics, verify, adversarial, EXPECTED, POP_FULL
def test_identity(): load()
def test_diagnostics(): verify()
def test_attacks(): adversarial()
def test_n_minus_1(): assert EXPECTED["FULL"]["sample_stddev"] != POP_FULL
def test_candidate_full_sample(): assert EXPECTED["FULL"]["sample_stddev"]==336.4106561689863
