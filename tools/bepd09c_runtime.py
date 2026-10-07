from __future__ import annotations
import hashlib, json, math
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
import numpy as np
from scipy.optimize import minimize, linprog

CONTRACT='ATDS_BEPD_09C_C1_EXECUTABLE_RUNTIME_V0_1'
NY=ZoneInfo('America/New_York')
CONTEXT_FEATURES=('SIDE_HIGH_INDICATOR','LEVEL_AGE_WEEKS','ACTIVE_LEVEL_COUNT_AT_TARGET_WEEK_START','SWEEP_OVERSHOOT_RELATIVE')
NUMERIC_PARITY_ATOL=2e-5
FIT_TOL=1e-10
MAX_ITER=100
PROB_CLIP=1e-15

class BreakerError(RuntimeError): pass

def _utc(s):
    try: d=datetime.fromisoformat(str(s).replace('Z','+00:00'))
    except Exception as e: raise BreakerError('INVALID_TIMESTAMP') from e
    if d.tzinfo is None: raise BreakerError('NAIVE_TIMESTAMP')
    return d.astimezone(timezone.utc)

def week_bounds(w):
    try: m=date.fromisoformat(w)
    except Exception as e: raise BreakerError('INVALID_TARGET_WEEK_ID') from e
    if m.weekday()!=0: raise BreakerError('TARGET_WEEK_ID_NOT_MONDAY')
    a=datetime.combine(m-timedelta(days=1),time(18),tzinfo=NY).astimezone(timezone.utc)
    z=datetime.combine(m+timedelta(days=6),time(18),tzinfo=NY).astimezone(timezone.utc)
    return a,z

def exposure_values(w,take):
    a,z=week_bounds(w); t=_utc(take)
    dur=(z-a).total_seconds()/3600.0; rem=(z-t).total_seconds()/3600.0; x=rem/dur
    if not all(math.isfinite(v) for v in (dur,rem,x)): raise BreakerError('NONFINITE_EXPOSURE')
    if x<=0: raise BreakerError('EXPOSURE_FRACTION_NONPOSITIVE')
    if x>1: raise BreakerError('EXPOSURE_FRACTION_ABOVE_ONE')
    return dur,rem,x

def spline_basis(x):
    x=float(x)
    if not math.isfinite(x) or not (0<x<=1): raise BreakerError('INVALID_EXPOSURE_FRACTION')
    P=lambda k:max(x-k,0.0)**3; out=[x]
    for tj in (0.0,0.25,0.50): out.append(P(tj)-P(0.75)*(1-tj)/0.25+P(1.0)*(0.75-tj)/0.25)
    return out

def partition_calendar(cal):
    if len(cal)<6 or len(set(cal))!=len(cal): raise BreakerError('INVALID_CALENDAR')
    ds=[date.fromisoformat(x) for x in cal]
    if any(d.weekday()!=0 for d in ds) or any((ds[i+1]-ds[i]).days!=7 for i in range(len(ds)-1)): raise BreakerError('CALENDAR_NOT_CONTIGUOUS')
    q,r=divmod(len(cal),6); out=[]; p=0
    for i in range(6):
        n=q+(1 if i<r else 0); out.append(list(cal[p:p+n])); p+=n
    return out

def validate_rows(rows,cal,requested_context_features=CONTEXT_FEATURES):
    if tuple(requested_context_features)!=CONTEXT_FEATURES: raise BreakerError('POST_T0_OR_UNAUTHORIZED_FEATURE_ATTEMPT')
    partition_calendar(cal); cs=set(cal); ids=set(); cw={}; out=[]
    req=('event_id','target_week_id','sweep_cluster_id','side','level_price_mid','take_h1_close_mid','take_h1_close_utc','level_age_weeks','active_level_count_at_target_week_start','same_week_reintegration')
    for r in rows:
        if any(k not in r for k in req): raise BreakerError('MISSING_REQUIRED_VALUE')
        if r['event_id'] in ids: raise BreakerError('DUPLICATE_EVENT_ID')
        ids.add(r['event_id']); w=r['target_week_id']; cl=r['sweep_cluster_id']
        if w not in cs: raise BreakerError('TARGET_WEEK_CALENDAR_MISMATCH')
        if cl in cw and cw[cl]!=w: raise BreakerError('CLUSTER_WEEK_MISMATCH')
        cw[cl]=w
        if r['side'] not in ('HIGH','LOW'): raise BreakerError('INVALID_SIDE')
        nums=[r['level_price_mid'],r['take_h1_close_mid'],r['level_age_weeks'],r['active_level_count_at_target_week_start']]
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(float(v)) for v in nums): raise BreakerError('NONFINITE_NUMERIC')
        lp=float(r['level_price_mid'])
        if lp==0: raise BreakerError('ZERO_LEVEL_PRICE')
        if type(r['same_week_reintegration']) is not bool: raise BreakerError('INVALID_RESPONSE')
        dur,rem,x=exposure_values(w,r['take_h1_close_utc']); ov=abs(float(r['take_h1_close_mid'])-lp)/abs(lp)
        out.append({'event_id':r['event_id'],'target_week_id':w,'sweep_cluster_id':cl,'side_high':1.0 if r['side']=='HIGH' else 0.0,'age':float(r['level_age_weeks']),'active':float(r['active_level_count_at_target_week_start']),'overshoot':ov,'y':1.0 if r['same_week_reintegration'] else 0.0,'duration_hours':dur,'remaining_hours':rem,'exposure_fraction':x,'basis':spline_basis(x)})
    return out

def validate_fold_integrity(train,test):
    if {r['target_week_id'] for r in train}&{r['target_week_id'] for r in test}: raise BreakerError('TARGET_WEEK_SPLIT_ATTEMPT')
    if {r['sweep_cluster_id'] for r in train}&{r['sweep_cluster_id'] for r in test}: raise BreakerError('CLUSTER_SPLIT_ATTEMPT')

def _stats(train):
    s={}
    for k in ('age','active','overshoot'):
        v=np.array([r[k] for r in train],dtype=float); m=float(v.mean()); sd=float(v.std(ddof=1))
        if not math.isfinite(sd) or sd==0: raise BreakerError('ZERO_OR_NONFINITE_TRAINING_SD')
        s[k]=(m,sd)
    return s

def _mats(rs,s):
    xb=[]; xc=[]
    for r in rs:
        base=[1.0]+list(r['basis'])
        xb.append(base); xc.append(base+[r['side_high']]+[(r[k]-s[k][0])/s[k][1] for k in ('age','active','overshoot')])
    return np.array(xb,float),np.array(xc,float)

def _sig(z):
    z=np.asarray(z,float); return np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))

def _ll(X,y,b):
    z=X@b
    return float(np.sum(y*z-np.logaddexp(0,z)))

def fit_logistic(X,y,max_iter=MAX_ITER,tol=FIT_TOL):
    X=np.asarray(X,float); y=np.asarray(y,float)
    if X.ndim!=2 or len(X)!=len(y) or len(X)==0: raise BreakerError('INVALID_MODEL_INPUT')
    if len(set(y.tolist()))<2: raise BreakerError('ONE_CLASS_TRAINING_FOLD')
    signs=np.where(y>0.5,1.0,-1.0)
    sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method='highs')
    if sep.success: raise BreakerError('PERFECT_SEPARATION')
    def fun(b):
        z=X@b; return float(np.sum(np.logaddexp(0,z)-y*z))
    def jac(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return X.T@(p-y)
    def hess(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); w=p*(1-p); return X.T@(X*w[:,None])
    res=minimize(fun,np.zeros(X.shape[1]),jac=jac,hess=hess,method='Newton-CG',options={'xtol':tol,'maxiter':max_iter,'disp':False})
    if not res.success: raise BreakerError('MODEL_NONCONVERGENCE')
    return res.x

def _score(rows,pb,pc):
    by={}; ev=[[],[],[],[]]
    for r,b,c in zip(rows,pb,pc):
        b=min(max(float(b),PROB_CLIP),1-PROB_CLIP); c=min(max(float(c),PROB_CLIP),1-PROB_CLIP); y=r['y']
        vals=[-(y*math.log(b)+(1-y)*math.log(1-b)),-(y*math.log(c)+(1-y)*math.log(1-c)),(y-b)**2,(y-c)**2]
        by.setdefault(r['target_week_id'],[[],[],[],[]])
        for j,v in enumerate(vals): by[r['target_week_id']][j].append(v); ev[j].append(v)
    weekly={w:{'baseline_logloss':sum(v[0])/len(v[0]),'context_logloss':sum(v[1])/len(v[1]),'baseline_brier':sum(v[2])/len(v[2]),'context_brier':sum(v[3])/len(v[3])} for w,v in sorted(by.items())}
    return weekly,tuple(sum(x)/len(x) for x in ev)

def run_protocol(rows,calendar,requested_context_features=CONTEXT_FEATURES):
    rs=validate_rows(rows,calendar,requested_context_features); blocks=partition_calendar(calendar); folds=[]; allw={}; ev=[]
    for i in range(1,6):
        trw={w for b in blocks[:i] for w in b}; tew=set(blocks[i]); tr=[r for r in rs if r['target_week_id'] in trw]; te=[r for r in rs if r['target_week_id'] in tew]
        if not te: raise BreakerError('TEST_BLOCK_ZERO_QUALIFIED_EVENTS')
        validate_fold_integrity(tr,te); s=_stats(tr); xb,xc=_mats(tr,s); vb,vc=_mats(te,s); y=np.array([r['y'] for r in tr],float)
        bb=fit_logistic(xb,y); bc=fit_logistic(xc,y); pb=_sig(vb@bb); pc=_sig(vc@bc); weekly,e=_score(te,pb,pc); allw.update(weekly); ev.append((e,len(te)))
        folds.append({'fold':i,'train_weeks':blocks[:i],'test_weeks':blocks[i],'train_event_count':len(tr),'test_event_count':len(te),'train_response_class_counts':{'0':sum(r['y']==0 for r in tr),'1':sum(r['y']==1 for r in tr)},'standardization':{k:{'mean':v[0],'sample_sd':v[1]} for k,v in s.items()},'baseline_design':vb.tolist(),'context_design':vc.tolist(),'baseline_probabilities':pb.tolist(),'context_probabilities':pc.tolist(),'weekly':weekly,'convergence_status':'PASS'})
    mean=lambda v:sum(v)/len(v)
    abl=mean([v['baseline_logloss'] for v in allw.values()]); acl=mean([v['context_logloss'] for v in allw.values()]); abb=mean([v['baseline_brier'] for v in allw.values()]); acb=mean([v['context_brier'] for v in allw.values()]); total=sum(n for _,n in ev); ew=[sum(v[j]*n for v,n in ev)/total for j in range(4)]
    out={'contract':CONTRACT,'status':'SYNTHETIC_RESULT_ONLY','blocks':blocks,'folds':folds,'aggregate':{'baseline_week_balanced_logloss':abl,'context_week_balanced_logloss':acl,'primary_logloss_improvement_delta':abl-acl,'baseline_week_balanced_brier':abb,'context_week_balanced_brier':acb,'secondary_brier_improvement_delta':abb-acb,'event_weighted_baseline_logloss':ew[0],'event_weighted_context_logloss':ew[1],'event_weighted_baseline_brier':ew[2],'event_weighted_context_brier':ew[3]},'automatic_verdict':'NONE_HUMAN_ADJUDICATION_REQUIRED'}
    out['deterministic_replay_identity']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest(); return out
