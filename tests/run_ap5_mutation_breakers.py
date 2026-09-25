from __future__ import annotations
import os, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).parents[1]
SRC=(ROOT/"tools"/"ap5_microstructure_price_core.py").read_text(encoding="utf-8")
TEST=ROOT/"tests"/"test_ap5_microstructure_price_core.py"
MUTANTS=[
 ("UNWEIGHTED_SPREAD","return float(np.sum(spread_mean * tick_count, dtype=np.float64) / ticks)","return float(np.mean(spread_mean))"),
 ("CROSS_GAP_RETURN","valid = (segment[1:] == segment[:-1]) & ((minute[1:] - minute[:-1]) == 60_000)","valid = ((minute[1:] - minute[:-1]) > 0)"),
 ("RANGE_CLOSE_DENOM","return (hi - lo) / op * 10000.0","return (hi - lo) / hi * 10000.0"),
 ("CASH_1600_INCLUDED","cash = (wd < 5) & (md >= 9 * 60 + 30) & (md < 16 * 60)","cash = (wd < 5) & (md >= 9 * 60 + 30) & (md <= 16 * 60)"),
 ("QUINTILE_LEFT","return thresholds, np.searchsorted(thresholds, x, side=\"right\").astype(np.int8)","return thresholds, np.searchsorted(thresholds, x, side=\"left\").astype(np.int8)"),
 ("PATH_CHAIN_BYPASS","if is_reparse_or_symlink(cur):\n                return True","if is_reparse_or_symlink(cur):\n                return False"),
]
results=[]
for name,old,new in MUTANTS:
    if SRC.count(old)!=1:
        print(f"RUNNER_ERROR {name}: replacement count {SRC.count(old)}"); sys.exit(2)
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"mutant.py"; p.write_text(SRC.replace(old,new),encoding="utf-8")
        env=os.environ.copy(); env["AP5_HELPER_PATH"]=str(p)
        r=subprocess.run([sys.executable,str(TEST)],env=env,capture_output=True,text=True)
        killed=r.returncode!=0
        results.append((name,killed))
        print(f"{name}: {'KILLED' if killed else 'SURVIVED'}")
if not all(k for _,k in results): sys.exit(1)
print(f"AP5_MUTATION_BREAKERS_PASS {sum(k for _,k in results)}/{len(results)}")
