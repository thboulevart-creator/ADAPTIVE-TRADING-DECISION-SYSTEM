from __future__ import annotations
import math, random
from datetime import date

def _calendar(calendar):
    if not calendar: raise ValueError("EMPTY_CALENDAR")
    parsed=[]
    for x in calendar:
        d=date.fromisoformat(x)
        if d.weekday()!=0: raise ValueError("TARGET_WEEK_NOT_MONDAY")
        parsed.append((x,d))
    if len({x for x,_ in parsed})!=len(parsed): raise ValueError("DUPLICATE_TARGET_WEEK")
    for i in range(1,len(parsed)):
        delta=(parsed[i][1]-parsed[i-1][1]).days
        if delta<0: raise ValueError("UNSORTED_TARGET_WEEK")
        if delta!=7: raise ValueError("CALENDAR_GAP")
    return [x for x,_ in parsed]

def reference_week_counts(calendar,events):
    cal=_calendar(calendar); valid=set(cal)
    clusters={}; week_clusters={}; ids=set()
    counts={w:[0,0] for w in cal}
    for e in events:
        if e["event_id"] in ids: raise ValueError("DUPLICATE_EVENT_ID")
        ids.add(e["event_id"])
        w=e["target_week_id"]; c=e["sweep_cluster_id"]; y=e["same_week_reintegration"]
        if w not in valid: raise ValueError("EVENT_WEEK_OUTSIDE_CALENDAR")
        if type(y) is not bool: raise ValueError("RESPONSE_NOT_BOOLEAN")
        if c in clusters and clusters[c]!=w: raise ValueError("SWEEP_CLUSTER_SPLIT")
        clusters[c]=w
        if w in week_clusters and week_clusters[w]!=c: raise ValueError("TARGET_WEEK_CLUSTER_SPLIT")
        week_clusters[w]=c
        counts[w][1]+=1; counts[w][0]+=1 if y else 0
    return [{"target_week_id":w,"success_count":counts[w][0],"event_count":counts[w][1]} for w in cal]

def _quantile(x,p):
    x=sorted(x); h=(len(x)-1)*p; l=int(math.floor(h)); r=int(math.ceil(h))
    if l==r:return x[l]
    return x[l]+(h-l)*(x[r]-x[l])

def reference_moving_block_ratio_ci(calendar,events,*,block_length,replications,seed,confidence_level,interval_method):
    rows=reference_week_counts(calendar,events); n=len(rows)
    if block_length<=0 or block_length>n: raise ValueError("BLOCK_LENGTH_REQUIRED")
    rng=random.Random(seed); total=sum(x["event_count"] for x in rows)
    if total<=0: raise ValueError("ZERO_TOTAL_EVENT_DENOMINATOR")
    point=sum(x["success_count"] for x in rows)/total; dist=[]
    for _ in range(replications):
        tmp=[]
        while len(tmp)<n:
            start=rng.randrange(n-block_length+1)
            for j in range(block_length):
                tmp.append(rows[start+j])
                if len(tmp)==n: break
        d=sum(x["event_count"] for x in tmp)
        if d<=0: raise ValueError("ZERO_DENOMINATOR_REPLICATE")
        dist.append(sum(x["success_count"] for x in tmp)/d)
    a=(1-confidence_level)/2; ql=_quantile(dist,a); qh=_quantile(dist,1-a)
    if interval_method=="PERCENTILE": lo,hi=ql,qh
    elif interval_method=="BASIC": lo,hi=2*point-qh,2*point-ql
    else: raise ValueError("INTERVAL_METHOD_UNSUPPORTED")
    return {"point_estimate":point,"lower":lo,"upper":hi}
