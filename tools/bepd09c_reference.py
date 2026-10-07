from __future__ import annotations
import hashlib,json,math
from datetime import date,datetime,time,timedelta,timezone
from zoneinfo import ZoneInfo
import numpy as np
from scipy.optimize import root, linprog

CONTRACT='ATDS_BEPD_09C_C1_INDEPENDENT_REFERENCE_V0_1'
NY=ZoneInfo('America/New_York'); FEATURES=('SIDE_HIGH_INDICATOR','LEVEL_AGE_WEEKS','ACTIVE_LEVEL_COUNT_AT_TARGET_WEEK_START','SWEEP_OVERSHOOT_RELATIVE'); PROB_CLIP=1e-15
class ReferenceError(RuntimeError): pass

def _bounds(w):
    m=date.fromisoformat(w)
    if m.weekday()!=0: raise ReferenceError('TARGET_WEEK_ID_NOT_MONDAY')
    return datetime.combine(m-timedelta(days=1),time(18),tzinfo=NY).astimezone(timezone.utc),datetime.combine(m+timedelta(days=6),time(18),tzinfo=NY).astimezone(timezone.utc)
def _utc(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'))
    if d.tzinfo is None: raise ReferenceError('NAIVE_TIMESTAMP')
    return d.astimezone(timezone.utc)
def _basis(x):
    if not math.isfinite(x) or not (0<x<=1): raise ReferenceError('INVALID_EXPOSURE')
    P=lambda k:max(x-k,0.0)**3; return [x]+[P(k)-P(0.75)*(1-k)/0.25+P(1)*(0.75-k)/0.25 for k in (0,0.25,0.5)]
def _blocks(cal):
    if len(cal)<6 or len(set(cal))!=len(cal): raise ReferenceError('INVALID_CALENDAR')
    ds=[date.fromisoformat(x) for x in cal]
    if any(d.weekday()!=0 for d in ds) or any((ds[i+1]-ds[i]).days!=7 for i in range(len(ds)-1)): raise ReferenceError('INVALID_CALENDAR')
    q,r=divmod(len(cal),6); out=[]; p=0
    for i in range(6): n=q+(i<r);out.append(list(cal[p:p+n]));p+=n
    return out
def _prep(rows,cal,features=FEATURES):
    if tuple(features)!=FEATURES: raise ReferenceError('UNAUTHORIZED_FEATURE')
    _blocks(cal); cs=set(cal); ids=set(); cw={}; out=[]; need=('event_id','target_week_id','sweep_cluster_id','side','level_price_mid','take_h1_close_mid','take_h1_close_utc','level_age_weeks','active_level_count_at_target_week_start','same_week_reintegration')
    for r in rows:
        if any(k not in r for k in need): raise ReferenceError('MISSING_REQUIRED_VALUE')
        if r['event_id'] in ids: raise ReferenceError('DUPLICATE_EVENT_ID')
        ids.add(r['event_id']);w=r['target_week_id'];cl=r['sweep_cluster_id']
        if w not in cs: raise ReferenceError('TARGET_WEEK_CALENDAR_MISMATCH')
        if cl in cw and cw[cl]!=w: raise ReferenceError('CLUSTER_WEEK_MISMATCH')
        cw[cl]=w
        if r['side'] not in ('HIGH','LOW'): raise ReferenceError('INVALID_SIDE')
        nums=[r['level_price_mid'],r['take_h1_close_mid'],r['level_age_weeks'],r['active_level_count_at_target_week_start']]
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(float(v)) for v in nums): raise ReferenceError('NONFINITE_NUMERIC')
        lp=float(r['level_price_mid'])
        if lp==0: raise ReferenceError('ZERO_LEVEL_PRICE')
        if type(r['same_week_reintegration']) is not bool: raise ReferenceError('INVALID_RESPONSE')
        a,z=_bounds(w);t=_utc(r['take_h1_close_utc']);dur=(z-a).total_seconds()/3600;rem=(z-t).total_seconds()/3600;x=rem/dur
        out.append({'event_id':r['event_id'],'target_week_id':w,'sweep_cluster_id':cl,'side':1.0 if r['side']=='HIGH' else 0.0,'age':float(r['level_age_weeks']),'active':float(r['active_level_count_at_target_week_start']),'overshoot':abs(float(r['take_h1_close_mid'])-lp)/abs(lp),'y':1.0 if r['same_week_reintegration'] else 0.0,'basis':_basis(x),'exposure':x})
    return out
def _fit(X,y):
    X=np.asarray(X,float);y=np.asarray(y,float)
    if len(set(y.tolist()))<2: raise ReferenceError('ONE_CLASS_TRAINING_FOLD')
    signs=np.where(y>0.5,1.0,-1.0)
    sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method='highs')
    if sep.success: raise ReferenceError('PERFECT_SEPARATION')
    def score(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return X.T@(p-y)
    def jac(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); w=p*(1-p); return X.T@(X*w[:,None])
    res=root(score,np.zeros(X.shape[1]),jac=jac,method='hybr',options={'xtol':1e-10,'maxfev':5000})
    if (not res.success) and float(np.max(np.abs(score(res.x))))>1e-8: raise ReferenceError('MODEL_NONCONVERGENCE')
    return res.x

def run_reference(rows,calendar,features=FEATURES):
    rs=_prep(rows,calendar,features);bs=_blocks(calendar);folds=[];allw={};ev=[]
    for i in range(1,6):
        trw={w for b in bs[:i] for w in b};tew=set(bs[i]);tr=[r for r in rs if r['target_week_id'] in trw];te=[r for r in rs if r['target_week_id'] in tew]
        if not te: raise ReferenceError('TEST_BLOCK_ZERO_QUALIFIED_EVENTS')
        if {r['target_week_id'] for r in tr}&{r['target_week_id'] for r in te}: raise ReferenceError('TARGET_WEEK_SPLIT_ATTEMPT')
        if {r['sweep_cluster_id'] for r in tr}&{r['sweep_cluster_id'] for r in te}: raise ReferenceError('CLUSTER_SPLIT_ATTEMPT')
        stats={}
        for k in ('age','active','overshoot'):
            v=np.array([r[k] for r in tr]);m=float(v.mean());sd=float(v.std(ddof=1))
            if not math.isfinite(sd) or sd==0: raise ReferenceError('ZERO_OR_NONFINITE_TRAINING_SD')
            stats[k]=(m,sd)
        def mats(v):
            xb=[];xc=[]
            for r in v:
                base=[1.0]+r['basis'];xb.append(base);xc.append(base+[r['side']]+[(r[k]-stats[k][0])/stats[k][1] for k in ('age','active','overshoot')])
            return np.array(xb),np.array(xc)
        xb,xc=mats(tr);vb,vc=mats(te);y=np.array([r['y'] for r in tr]);bb=_fit(xb,y);bc=_fit(xc,y)
        sig=lambda z:np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)));pb=sig(vb@bb);pc=sig(vc@bc);by={};vals=[[],[],[],[]]
        for r,p0,p1 in zip(te,pb,pc):
            p0=min(max(float(p0),PROB_CLIP),1-PROB_CLIP);p1=min(max(float(p1),PROB_CLIP),1-PROB_CLIP);yy=r['y'];q=[-(yy*math.log(p0)+(1-yy)*math.log(1-p0)),-(yy*math.log(p1)+(1-yy)*math.log(1-p1)),(yy-p0)**2,(yy-p1)**2];by.setdefault(r['target_week_id'],[[],[],[],[]])
            for j,x in enumerate(q): by[r['target_week_id']][j].append(x);vals[j].append(x)
        weekly={w:{'baseline_logloss':sum(v[0])/len(v[0]),'context_logloss':sum(v[1])/len(v[1]),'baseline_brier':sum(v[2])/len(v[2]),'context_brier':sum(v[3])/len(v[3])} for w,v in sorted(by.items())};allw.update(weekly);e=tuple(sum(x)/len(x) for x in vals);ev.append((e,len(te)))
        folds.append({'fold':i,'train_weeks':bs[:i],'test_weeks':bs[i],'train_event_count':len(tr),'test_event_count':len(te),'train_response_class_counts':{'0':sum(r['y']==0 for r in tr),'1':sum(r['y']==1 for r in tr)},'standardization':{k:{'mean':v[0],'sample_sd':v[1]} for k,v in stats.items()},'baseline_design':vb.tolist(),'context_design':vc.tolist(),'baseline_probabilities':pb.tolist(),'context_probabilities':pc.tolist(),'weekly':weekly,'convergence_status':'PASS'})
    mean=lambda v:sum(v)/len(v);abl=mean([v['baseline_logloss'] for v in allw.values()]);acl=mean([v['context_logloss'] for v in allw.values()]);abb=mean([v['baseline_brier'] for v in allw.values()]);acb=mean([v['context_brier'] for v in allw.values()]);tot=sum(n for _,n in ev);ew=[sum(v[j]*n for v,n in ev)/tot for j in range(4)]
    out={'contract':CONTRACT,'status':'SYNTHETIC_RESULT_ONLY','blocks':bs,'folds':folds,'aggregate':{'baseline_week_balanced_logloss':abl,'context_week_balanced_logloss':acl,'primary_logloss_improvement_delta':abl-acl,'baseline_week_balanced_brier':abb,'context_week_balanced_brier':acb,'secondary_brier_improvement_delta':abb-acb,'event_weighted_baseline_logloss':ew[0],'event_weighted_context_logloss':ew[1],'event_weighted_baseline_brier':ew[2],'event_weighted_context_brier':ew[3]},'automatic_verdict':'NONE_HUMAN_ADJUDICATION_REQUIRED'};out['deterministic_replay_identity']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();return out
