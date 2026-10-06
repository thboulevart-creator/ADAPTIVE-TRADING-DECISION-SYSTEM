from __future__ import annotations
import hashlib, json, statistics, zipfile
from pathlib import Path

EXPECTED_ZIP_SHA256="a6588ef94d6cf15447ee8f7d2be0b7d3642ae857f2d64fcf86c77070ced0ca84"
EXPECTED_RESULT_CANONICAL_DIGEST="56eaf2626629bff2ff7b6dcd13e2ca178edddf06aade81f9480c4e3d142cf738"
EXPECTED_RECORDS_DIGEST="f890dd32f3e14b20430cb5898a05946a5d71231a9103b755fa0eb683f8834fc4"

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def recover_and_measure(path: Path) -> dict:
    if sha256_file(path)!=EXPECTED_ZIP_SHA256:
        raise ValueError("ZIP_DIGEST_MISMATCH")
    with zipfile.ZipFile(path) as z:
        raw=z.read("E1-REAL-003-RESULT.json")
    obj=json.loads(raw)
    if obj.get("canonical_digest")!=EXPECTED_RESULT_CANONICAL_DIGEST:
        raise ValueError("RESULT_CANONICAL_DIGEST_MISMATCH")
    br=obj["base_result"]
    if br.get("records_digest")!=EXPECTED_RECORDS_DIGEST:
        raise ValueError("RECORDS_DIGEST_MISMATCH")
    trades=br["trade_ledger"]["closed_trades"]
    if len(trades)!=650:
        raise ValueError("CLOSED_TRADE_COUNT_MISMATCH")
    def xs(part=None):
        return [float(r["realized_unit_pnl"]) for r in trades if part is None or r["partition"]==part]
    full=xs(); pre=xs("PRE_OOS"); oos=xs("OOS")
    return {
      "closed_trade_count":len(full),
      "full_sample_sample_stddev":statistics.stdev(full),
      "pre_oos_sample_stddev":statistics.stdev(pre),
      "exposed_oos_sample_stddev":statistics.stdev(oos),
      "full_sample_population_stddev":statistics.pstdev(full),
      "planning_stddev_candidate":statistics.stdev(full),
      "epistemic_class":"EXPOSED_E1_PLANNING_PROXY_ONLY"
    }
