#!/usr/bin/env python3
"""Independent BEPD-08D recomputation; no canonical-runner import."""
from __future__ import annotations
import argparse,json
from collections import defaultdict
from decimal import Decimal,ROUND_HALF_EVEN,getcontext
from fractions import Fraction
from pathlib import Path
getcontext().prec=80
Q18=Decimal("0.000000000000000001")
PROBS={"P01":Decimal(".01"),"P05":Decimal(".05"),"P10":Decimal(".10"),"P25":Decimal(".25"),"P50":Decimal(".50"),"P75":Decimal(".75"),"P90":Decimal(".90"),"P95":Decimal(".95"),"P99":Decimal(".99")}
def q18(x):return format(x.quantize(Q18,rounding=ROUND_HALF_EVEN),"f")
def frac(n,d):
 f=Fraction(n,d);return str(f.numerator) if f.denominator==1 else f"{f.numerator}/{f.denominator}"
def t7(v,p):
 n=len(v);h=Decimal(1)+Decimal(n-1)*p;j=int(h);g=h-Decimal(j)
 return v[-1] if j>=n else v[j-1]+g*(v[j]-v[j-1])
def agg(v):
 v=sorted(v);n=len(v);qs={k:q18(t7(v,p)) for k,p in PROBS.items()};z=sum(x==0 for x in v);c=defaultdict(int)
 for x in v:c[x]+=1
 cum=0;e=[]
 for x in sorted(c):
  cum+=c[x];e.append({"support_value":format(x,"f"),"support_count":c[x],"cumulative_count":cum,"cumulative_fraction":frac(cum,n),"cumulative_decimal":q18(Decimal(cum)/Decimal(n))})
 return {"N":n,"MINIMUM":q18(v[0]),"MAXIMUM":q18(v[-1]),"MEAN":q18(sum(v,Decimal(0))/Decimal(n)),"MEDIAN":qs["P50"],**qs,"ZERO_COUNT":z,"ZERO_FRACTION":{"fraction":frac(z,n),"decimal":q18(Decimal(z)/Decimal(n))},"EMPIRICAL_CDF":e}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
 rows=[json.loads(x,parse_float=Decimal) for x in Path(a.input).read_text(encoding="utf-8").splitlines() if x.strip()]
 if len(rows)!=472:raise RuntimeError("N")
 ids=[r.get("event_id") for r in rows]
 if len(set(ids))!=472:raise RuntimeError("duplicate")
 I=[];E=[];Z=[]
 for r in rows:
  if "close_displacement" not in r:raise RuntimeError("missing")
  v=r["close_displacement"] if isinstance(r["close_displacement"],Decimal) else Decimal(str(r["close_displacement"]))
  if not v.is_finite():raise RuntimeError("nonfinite")
  if v>0:I.append(abs(v))
  elif v<0:E.append(abs(v))
  else:Z.append(abs(v))
 if (len(I),len(E),len(Z))!=(207,265,0):raise RuntimeError("partition")
 out={"schema":"ATDS_BEPD_08D_INDEPENDENT_REFERENCE_V0_1","implementation":"INDEPENDENT_NO_IMPORT_FROM_CANONICAL_RUNNER","partition":{"TOTAL_N":472,"INTERNAL_N":207,"EXTERNAL_N":265,"EXACT_LEVEL_N":0},"INTERNAL":agg(I),"EXTERNAL":agg(E)}
 Path(a.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
