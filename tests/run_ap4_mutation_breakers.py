"""Bounded mutation checks; mutate only disposable copies of AP4."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'tools/ap4_price_structure.py').read_text(encoding='utf-8')
tests=(ROOT/'tests/test_ap4_price_structure.py').read_text(encoding='utf-8')
mutants={
 'include_current_bar':('j = t-1','j = t'),
 'ignore_gap_window':('result[t] = bad[t+1]-bad[t-h+1] == 0','result[t] = True'),
 'include_zero_in_runs':('active = valid & (s!=0)','active = valid'),
 'inclusive_breakout':('up=ok & (close>upper); down=ok & (close<lower)','up=ok & (close>=upper); down=ok & (close<=lower)'),
 'ignore_reentry_gap':('alive &= inside & cont','alive &= inside'),
 'reject_valid_nullable_gap':("require(np.all(np.isnan(a['gap_before_ms'][~np.r_[False,ds==1]])), 'Unexpected non-boundary gap value')","require(np.all(np.isfinite(a['gap_before_ms'])), 'Reject all null gaps')")}
results={}
for name,(old,new) in mutants.items():
    if src.count(old)!=1:raise RuntimeError('Mutation target drift: '+name)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);(root/'tools').mkdir();(root/'tests').mkdir()
        (root/'tools/ap4_price_structure.py').write_text(src.replace(old,new),encoding='utf-8')
        (root/'tests/test_ap4_price_structure.py').write_text(tests,encoding='utf-8')
        r=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(root/'tests'),'-p','test_ap4_price_structure.py'],capture_output=True,text=True)
        # A harness/import failure does not count as a killed semantic mutant.
        assertion_failure = 'FAILED (failures=' in r.stderr
        expected_rejection = (name=='reject_valid_nullable_gap' and
                              'ValueError: Reject all null gaps' in r.stderr and
                              'FAILED (errors=2)' in r.stderr)
        if 'Ran 9 tests' not in r.stderr or not (assertion_failure or expected_rejection):
            raise RuntimeError('Missing assertion-failure evidence: '+name+'\n'+r.stderr)
        results[name]='KILLED' if r.returncode else 'SURVIVED'
        if not r.returncode:raise RuntimeError('Survived: '+name)
print(json.dumps(results,indent=2))
