#!/usr/bin/env python3
"""AP4: aggregate descriptive minute price structure; no trading simulation."""
from __future__ import annotations
import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import sys
import tempfile
import numpy as np

AP0_SHA = '62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce'
AP3_SHA = 'caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef'
IDENTITY = 'USTECH_PROFILE_MINUTE_CORE_V0_1'
N_ROWS, N_FILES, N_SEGMENTS = 1709180, 61, 1606
READ = ['minute_start_ms_utc','first_tick_ms','last_tick_ms','segment_id',
        'segment_start','gap_before_ms','mid_open','mid_high','mid_low','mid_close']
EXPECTED_TYPES = ['int64']*4 + ['bool','int64'] + ['double']*4


def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def no_links(p):
    p = Path(p).absolute()
    for q in (p, *p.parents):
        if q.exists() or q.is_symlink():
            s = q.lstat()
            require(not stat.S_ISLNK(s.st_mode) and not
                    (getattr(s, 'st_file_attributes', 0) & 0x400), f'Link/reparse: {q}')


def output_guard(output, root, inputs):
    no_links(output)
    output, root = output.resolve(), root.resolve()
    require(not output.exists(), 'Output exists; choose a new output path')
    require(output != root and root not in output.parents, 'Output inside AP0 corpus')
    require(output not in [p.resolve() for p in inputs], 'Output aliases input')
    return output


def summary(x):
    x = np.asarray(x, dtype=float)
    require(np.all(np.isfinite(x)), 'Nonfinite summary input')
    if not len(x):
        return dict(count=0, mean=None, p50=None, p90=None, p99=None, min=None, max=None)
    q = np.percentile(x, [50,90,99], method='linear')
    return dict(count=len(x), mean=float(x.mean()), p50=float(q[0]), p90=float(q[1]),
                p99=float(q[2]), min=float(x.min()), max=float(x.max()))


def continuous_returns(minute, segment, close):
    valid = np.zeros(len(close), dtype=bool)
    valid[1:] = (np.diff(minute)==60000) & (np.diff(segment)==0)
    r = np.full(len(close), np.nan)
    r[1:][valid[1:]] = np.log(close[1:][valid[1:]]/close[:-1][valid[1:]])*10000
    return r, valid


def window_valid(valid, h):
    n = len(valid)
    result = np.zeros(n, dtype=bool)
    bad = np.r_[0, np.cumsum(~valid)]
    t = np.arange(h,n)
    result[t] = bad[t+1]-bad[t-h+1] == 0
    return result


def persistence(r, valid, bucket=None):
    signs = np.sign(np.nan_to_num(r)).astype(np.int8)
    eligible = valid[1:] & valid[:-1]
    if bucket is not None:
        eligible &= bucket[1:] & bucket[:-1]
    matrix = np.zeros((3,3),dtype=np.int64)
    np.add.at(matrix, (signs[:-1][eligible]+1,signs[1:][eligible]+1),1)
    same = int(matrix[0,0]+matrix[2,2]); reversal = int(matrix[0,2]+matrix[2,0])
    den = same+reversal
    v = valid if bucket is None else valid & bucket
    return dict(sign_order=['DOWN','ZERO','UP'], valid_return_count=int(v.sum()),
                sign_counts=[int(np.count_nonzero(v & (signs==s))) for s in (-1,0,1)],
                adjacent_pair_counts=matrix.tolist(), eligible_pairs=int(matrix.sum()),
                nonzero_pairs=den, zero_involving_pairs=int(matrix.sum())-den,
                persistence_rate=same/den if den else None,
                reversal_rate=reversal/den if den else None)


def runs(r, valid):
    s = np.sign(np.nan_to_num(r)).astype(np.int8)
    active = valid & (s!=0)
    continuation = np.zeros(len(r),dtype=bool)
    continuation[1:] = active[1:] & active[:-1] & (s[1:]==s[:-1])
    starts = np.flatnonzero(active & ~continuation)
    ends = np.flatnonzero(active & ~np.r_[continuation[1:],False])
    require(len(starts)==len(ends), 'Run boundaries')
    cs = np.r_[0.,np.cumsum(np.where(active,np.abs(r),0.))]
    length = ends-starts+1
    amp = cs[ends+1]-cs[starts]
    require(int(length.sum())==int(active.sum()), 'Run duration conservation')
    return {name:dict(duration_minutes=summary(length[s[starts]==sign]),
                      amplitude_abs_log_bps=summary(amp[s[starts]==sign]))
            for name,sign in [('DOWN',-1),('UP',1)]} | {'nonzero_return_count':int(active.sum())}


def efficiency(r, valid, h):
    ok = window_valid(valid,h)
    clean = np.where(valid,r,0.)
    cs = np.r_[0.,np.cumsum(clean)]; ca = np.r_[0.,np.cumsum(np.abs(clean))]
    idx = np.flatnonzero(ok)
    signed = cs[idx+1]-cs[idx-h+1]; travel = ca[idx+1]-ca[idx-h+1]
    # Count exact flat windows independently of floating point prefix differences.
    nz = np.r_[0,np.cumsum(valid & (r!=0))]
    nonflat = (nz[idx+1]-nz[idx-h+1])>0
    require(np.all(travel[nonflat]>0), 'Nonflat denominator lost to precision')
    values = np.full(len(r),np.nan); disp = np.full(len(r),np.nan)
    values[idx[nonflat]] = np.abs(signed[nonflat])/travel[nonflat]
    require(np.all(values[idx[nonflat]]<=1+1e-9), 'Efficiency above one')
    values[idx[nonflat]] = np.clip(values[idx[nonflat]],0.,1.)
    disp[idx] = signed
    return values, disp, ok, int((~nonflat).sum())


def past_extreme(x, h, maximum):
    """Extreme on [t-h,t), explicitly excluding t."""
    out = np.full(len(x),np.nan); queue = deque()
    for t in range(len(x)):
        j = t-1
        if j>=0:
            while queue and ((x[queue[-1]]<=x[j]) if maximum else (x[queue[-1]]>=x[j])):
                queue.pop()
            queue.append(j)
        while queue and queue[0]<t-h:
            queue.popleft()
        if t>=h:
            out[t]=x[queue[0]]
    return out


def reentries(events, lower, upper, close, valid, horizon=15):
    require(horizon==15, 'Only preregistered horizon 15')
    idx = np.flatnonzero(events)
    available = np.zeros(len(idx),dtype=np.int16)
    lag = np.zeros(len(idx),dtype=np.int16)
    alive = np.ones(len(idx),dtype=bool)
    for k in range(1,horizon+1):
        target=idx+k; inside=target<len(close)
        cont=np.zeros(len(idx),dtype=bool)
        cont[inside]=valid[target[inside]]
        alive &= inside & cont
        available[alive]=k
        pending=alive & (lag==0)
        positions=np.flatnonzero(pending)
        hit=(close[target[positions]]>=lower[idx[positions]]) & (close[target[positions]]<=upper[idx[positions]])
        lag[positions[hit]]=k
    hit=lag>0
    full=(~hit) & (available==horizon)
    censored=(~hit) & ~full
    require(int(hit.sum()+full.sum()+censored.sum())==len(idx), 'Event conservation')
    return dict(event_count=len(idx), reentered=int(hit.sum()),
                not_reentered_full_15m=int(full.sum()), censored=int(censored.sum()),
                first_reentry_lag_minutes=summary(lag[hit]))


def breakout(close, high, low, valid, h):
    upper=past_extreme(high,h,True); lower=past_extreme(low,h,False)
    ok=window_valid(valid,h)
    up=ok & (close>upper); down=ok & (close<lower)
    return dict(eligible_count=int(ok.sum()),
                up=reentries(up,lower,upper,close,valid),
                down=reentries(down,lower,upper,close,valid))


def load_inputs(root, manifest_path, ap3_path):
    for p in (root,manifest_path,ap3_path): no_links(p)
    require(digest(manifest_path)==AP0_SHA,'AP0 manifest hash mismatch')
    require(digest(ap3_path)==AP3_SHA,'AP3 report hash mismatch')
    import pyarrow.parquet as pq
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    ap3=json.loads(ap3_path.read_text(encoding='utf-8'))
    require(manifest['status']=='AP0_COMPLETE' and manifest['output_identity']==IDENTITY,'AP0 contract')
    require(ap3['status']=='AP3_COMPLETE' and ap3['input_identity']==IDENTITY,'AP3 contract')
    files=manifest['files']
    require(len(files)==N_FILES and len({f['relative_path'] for f in files})==N_FILES,'File count')
    require(sum(f['size_bytes'] for f in files)==91734766,'AP0 byte coverage')
    chunks={k:[] for k in READ}
    for rec in files:
        p=root/rec['relative_path'];no_links(p);p=p.resolve()
        require(root in p.parents,'Path escape')
        require(p.stat().st_size==rec['size_bytes'] and digest(p)==rec['sha256'],'Parquet identity')
        pf=pq.ParquetFile(p)
        require(pf.metadata.num_rows==rec['rows'],'Parquet rows')
        schema=pf.schema_arrow
        for k,typ in zip(READ,EXPECTED_TYPES): require(str(schema.field(k).type)==typ,'Column type '+k)
        meta=schema.metadata or {}
        require(meta.get(b'dataset_identity')==IDENTITY.encode(),'Dataset metadata')
        require(meta.get(b'volumes_used')==b'false','Volume metadata')
        require(meta.get(b'mid_semantics')==b'descriptive_only_not_execution_price','Mid metadata')
        table=pf.read(columns=READ,use_threads=False)
        for k in READ:
            if k != 'gap_before_ms':
                require(table[k].null_count==0,'Null '+k)
            chunks[k].append(table[k].combine_chunks().to_numpy(zero_copy_only=False).copy())
        require(digest(p)==rec['sha256'],'Parquet changed during read')
    a={k:np.concatenate(v) for k,v in chunks.items()}
    require(len(a['mid_close'])==N_ROWS,'Total rows')
    return a


def validate_arrays(a):
    t=a['minute_start_ms_utc'];s=a['segment_id'];f=a['first_tick_ms'];last=a['last_tick_ms']
    require(np.all(np.diff(t)>0) and np.all(t%60000==0),'Minute order/alignment')
    ds=np.diff(s)
    require(s[0]==0 and s[-1]==N_SEGMENTS-1 and np.all((ds==0)|(ds==1)),'Segments')
    start=np.r_[True,ds==1]
    require(np.array_equal(start,a['segment_start']),'Segment starts')
    require(np.all((f>=t)&(last<t+60000)&(last>=f)),'Tick envelope')
    gap=f[1:]-last[:-1]
    require(np.all(gap>0) and np.array_equal(gap>60000,ds==1),'Gap-segment binding')
    require(np.array_equal(a['gap_before_ms'][1:][ds==1],gap[ds==1]),'Reopen gap binding')
    require(np.all(np.isnan(a['gap_before_ms'][~np.r_[False,ds==1]])), 'Unexpected non-boundary gap value')
    o,h,l,c=[a[k] for k in ['mid_open','mid_high','mid_low','mid_close']]
    require(all(np.all(np.isfinite(x)&(x>0)) for x in (o,h,l,c)),'Invalid OHLC')
    require(np.all((l<=o)&(l<=c)&(h>=o)&(h>=c)&(h>=l)),'OHLC envelope')
    return gap,ds==1


def analyze(a, enforce=True):
    t=a['minute_start_ms_utc'];s=a['segment_id'];c=a['mid_close']
    gap,boundary=validate_arrays(a)
    r,valid=continuous_returns(t,s,c)
    if enforce: require(int(valid.sum())==1707574,'AP2 1m coverage mismatch')
    year=np.array([datetime.fromtimestamp(int(v)*86400,tz=timezone.utc).year for v in np.unique(t//86400000)],dtype=np.int16)
    _,inv=np.unique(t//86400000,return_inverse=True);year=year[inv]
    result=dict(direction=persistence(r,valid), directional_runs=runs(r,valid), horizons={},utc_years=[])
    caches={}
    for h,expected in [(15,1686423),(60,1620195)]:
        e,d,ok,flat=efficiency(r,valid,h)
        if enforce: require(int(ok.sum())==expected,'AP2 window coverage mismatch')
        caches[h]=(e,d,ok)
        result['horizons'][str(h)]=dict(valid_windows=int(ok.sum()),zero_travel_excluded=flat,
            efficiency=summary(e[np.isfinite(e)]),signed_displacement_bps=summary(d[ok]),
            abs_displacement_bps=summary(np.abs(d[ok])),
            breakouts=breakout(c,a['mid_high'],a['mid_low'],valid,h))
    for y in range(2021,2027):
        mask=year==y
        result['utc_years'].append(dict(year=y,partial_period=y in (2021,2026),
            minute_rows=int(mask.sum()),direction=persistence(r,valid,mask),
            efficiency={str(h):summary(e[mask & np.isfinite(e)]) for h,(e,d,ok) in caches.items()}))
    idx=np.flatnonzero(boundary)+1
    reopen=np.log(a['mid_open'][idx]/c[idx-1])*10000
    result['reopen']=dict(boundary_count=len(idx),gap_ms=summary(gap[boundary]),
        signed_discontinuous_log_bps=summary(reopen),absolute_discontinuous_log_bps=summary(np.abs(reopen)))
    if enforce: require(len(idx)==1605,'Reopen coverage')
    result['coverage']=dict(minute_rows=len(c),segments=int(s[-1])+1,valid_1m_returns=int(valid.sum()))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ap0-root',required=True);p.add_argument('--ap0-manifest',required=True)
    p.add_argument('--ap3-report',required=True)
    p.add_argument('--output',default=str(Path(tempfile.gettempdir())/'ATDS-AP4-PRICE-STRUCTURE.json'))
    args=p.parse_args()
    root=Path(args.ap0_root).absolute();manifest=Path(args.ap0_manifest).absolute();ap3=Path(args.ap3_report).absolute()
    try:
        output=output_guard(Path(args.output).absolute(),root,[manifest,ap3,Path(__file__)])
        a=load_inputs(root.resolve(),manifest,ap3)
        result=analyze(a)
        import pyarrow as pa
        payload=dict(schema='ATDS_AP4_PRICE_STRUCTURE_V0_1',status='AP4_COMPLETE',input_identity=IDENTITY,
            binding=dict(ap0_manifest_sha256=AP0_SHA,ap3_sha256=AP3_SHA,ap0_files_rehashed=N_FILES,
                         helper_sha256=digest(__file__)),
            scope=dict(strategy_agnostic=True,causal_deployable=False,future_observations_used=True,
                       predictive_labels_exported=False,signals_calculated=False,pnl_calculated=False,
                       source_volume_used=False,optimization=False),
            metric_contract=dict(horizons_minutes=[15,60],reentry_horizon_minutes=15,
                breakout='close strictly outside previous H minute high/low range; current excluded',
                reentry='first future close inside frozen inclusive event range, censored at discontinuity',
                runs='consecutive same-sign nonzero 1m close returns; zero breaks',
                efficiency='abs(sum(r))/sum(abs(r)); zero denominator excluded',
                reopen='explicitly discontinuous current open vs previous close',
                percentiles='linear',stability='AP6 pending; overlapping observations not independent'),
            runtime=dict(numpy_version=np.__version__,pyarrow_version=pa.__version__),**result)
        raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
        require(len(raw)<=32*1024*1024,'Output exceeds 32 MiB')
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('xb') as f:f.write(raw)
        print('AP4_COMPLETE');print('Minute rows:',result['coverage']['minute_rows'])
        print('Reopen boundaries:',result['reopen']['boundary_count'])
        print('SHA-256:',hashlib.sha256(raw).hexdigest());print('Report:',output)
        return 0
    except Exception as exc:
        print('BLOCKED_AP4');print(type(exc).__name__+': '+str(exc))
        print('No report overwritten. Send this terminal output.');return 2

if __name__=='__main__':
    sys.exit(main())
