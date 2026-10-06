from pathlib import Path
import json, math
C=json.loads((Path(__file__).resolve().parents[1]/"GOVERNANCE"/"AO-E0-B8-M06-01-EXPOSED-E1-PLANNING-DISPERSION-CONTRACT-V0.1.json").read_text())
def test_candidate_value(): assert math.isclose(C["dispersion"]["selected_planning_stddev_candidate"],336.4106561689863,abs_tol=1e-12)
def test_candidate_only(): assert C["status"]=="QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION"
def test_b8_not_closed(): assert C["authority"]["b8_closure"] is False
def test_b12_closed(): assert C["authority"]["b12_open"] is False
