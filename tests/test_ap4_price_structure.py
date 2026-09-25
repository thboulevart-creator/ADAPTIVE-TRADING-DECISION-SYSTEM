"""Pre-registered AP4 boundary tests with loop oracles, no market corpus."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

PATH=Path(__file__).resolve().parents[1]/'tools'/'ap4_price_structure.py'
spec=importlib.util.spec_from_file_location('ap4',PATH)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class AP4Tests(unittest.TestCase):
    def test_continuity_and_signs(self):
        t=np.array([0,1,2,3,5,6,7,8])*60000
        s=np.array([0,0,0,1,1,1,1,1]);c=np.array([100,101,101,99,120,121,120,119.])
        r,v=m.continuous_returns(t,s,c)
        self.assertEqual(v.tolist(),[False,True,True,False,False,True,True,True])
        z=m.persistence(r,v)
        self.assertEqual(z['eligible_pairs'],3)
        self.assertEqual(z['zero_involving_pairs'],1)
        self.assertEqual(z['nonzero_pairs'],2)
        self.assertEqual(z['reversal_rate'],.5)
        runs=m.runs(r,v)
        self.assertEqual(runs['UP']['duration_minutes']['count'],2)
        self.assertEqual(runs['DOWN']['duration_minutes']['max'],2)
        self.assertEqual(runs['nonzero_return_count'],4)

    def test_random_window_oracle(self):
        rng=np.random.default_rng(974)
        n=301;t=np.arange(n)*60000;s=np.zeros(n,dtype=int)
        t[67:]+=60000;s[153:]+=1
        c=np.exp(np.cumsum(rng.normal(0,.001,n)))*100
        r,v=m.continuous_returns(t,s,c)
        hi=c+1;lo=c-1
        for h in (15,60):
            e,d,ok,flat=m.efficiency(r,v,h)
            up=m.past_extreme(hi,h,True);down=m.past_extreme(lo,h,False)
            for i in range(n):
                expected=i>=h and all(s[j]==s[j-1] and t[j]-t[j-1]==60000 for j in range(i-h+1,i+1))
                self.assertEqual(bool(ok[i]),expected)
                if i>=h:
                    self.assertEqual(up[i],max(hi[i-h:i]))
                    self.assertEqual(down[i],min(lo[i-h:i]))
                if expected:
                    vals=[float(np.log(c[j]/c[j-1])*10000) for j in range(i-h+1,i+1)]
                    self.assertAlmostEqual(d[i],sum(vals),places=9)
                    self.assertAlmostEqual(e[i],abs(sum(vals))/sum(map(abs,vals)),places=9)

    def test_flat_excluded(self):
        r=np.r_[np.nan,np.zeros(70)];v=np.isfinite(r)
        e,d,ok,flat=m.efficiency(r,v,15)
        self.assertEqual(flat,56);self.assertEqual(np.isfinite(e).sum(),0)
        self.assertEqual(m.runs(r,v)['nonzero_return_count'],0)

    def event(self,close,break_at=None):
        c=np.array(close,float);n=len(c);v=np.ones(n,bool);v[0]=False
        if break_at is not None:v[break_at]=False
        events=np.zeros(n,bool);events[0]=True
        return m.reentries(events,np.full(n,9.),np.full(n,11.),c,v)

    def test_reentry_endpoints_and_censor(self):
        self.assertEqual(self.event([12,11])['first_reentry_lag_minutes']['p50'],1)
        z=self.event([12]*15+[9]);self.assertEqual(z['reentered'],1)
        self.assertEqual(z['first_reentry_lag_minutes']['max'],15)
        z=self.event([12]*16+[10]);self.assertEqual(z['not_reentered_full_15m'],1)
        self.assertEqual(self.event([12]*10)['censored'],1)
        self.assertEqual(self.event([12,10],break_at=1)['censored'],1)
        self.assertEqual(self.event([12,10,12],break_at=2)['reentered'],1)
        # Skipping across the entire range is not reentry.
        self.assertEqual(self.event([12]+[8]*15)['not_reentered_full_15m'],1)
        self.assertEqual(self.event([8]+[12]*15)['not_reentered_full_15m'],1)

    def test_random_reentry_oracle(self):
        rng=np.random.default_rng(42);n=200;c=rng.uniform(5,15,n)
        lo=rng.uniform(6,8,n);hi=rng.uniform(10,12,n)
        events=rng.random(n)<.4;v=rng.random(n)>.08;v[0]=False
        hit=[];full=0;censor=0
        for i in np.flatnonzero(events):
            for k in range(1,16):
                j=i+k
                if j>=n or not v[j]:censor+=1;break
                if lo[i]<=c[j]<=hi[i]:hit.append(k);break
            else:full+=1
        z=m.reentries(events,lo,hi,c,v)
        self.assertEqual(z['reentered'],len(hit));self.assertEqual(z['censored'],censor)
        self.assertEqual(z['not_reentered_full_15m'],full)
        self.assertEqual(z['first_reentry_lag_minutes'],m.summary(hit))

    def test_breakout_excludes_current_and_strict_equal(self):
        c=np.full(35,10.);high=np.full(35,11.);low=np.full(35,9.)
        c[15]=12;high[15]=13;c[16]=13;high[16]=13
        c[17]=8;low[17]=7
        v=np.ones(35,bool);v[0]=False
        z=m.breakout(c,high,low,v,15)
        self.assertEqual(z['up']['event_count'],1)
        self.assertEqual(z['down']['event_count'],1)
        self.assertEqual(z['up']['first_reentry_lag_minutes']['max'],3)
        v[14]=False
        z=m.breakout(c,high,low,v,15)
        self.assertEqual(z['up']['event_count'],0);self.assertEqual(z['down']['event_count'],0)

    def arrays(self):
        t=np.array([0,60000,180000]);c=np.array([100.,101.,110.])
        return dict(minute_start_ms_utc=t,first_tick_ms=t+100,last_tick_ms=t+59000,
                    segment_id=np.array([0,0,1]),segment_start=np.array([True,False,True]),
                    gap_before_ms=np.array([np.nan,np.nan,61100.]),
                    mid_open=c,mid_high=c+1,mid_low=c-1,mid_close=c)

    def test_reopen_nullable_contract_and_gap(self):
        a=self.arrays()
        with patch.object(m,'N_SEGMENTS',2):
            gaps,boundary=m.validate_arrays(a)
            self.assertEqual(gaps[boundary].tolist(),[61100])
            a['gap_before_ms'][1]=0
            with self.assertRaisesRegex(ValueError,'Unexpected non-boundary'):m.validate_arrays(a)
            a['gap_before_ms'][1]=np.nan;a['gap_before_ms'][2]=61101
            with self.assertRaisesRegex(ValueError,'Reopen gap'):m.validate_arrays(a)

    def test_output_guards_and_hash_substitution(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);root=p/'corpus';root.mkdir();proof=p/'proof';proof.write_bytes(b'forged')
            with self.assertRaisesRegex(ValueError,'inside AP0'):m.output_guard(root/'out',root,[proof])
            with self.assertRaisesRegex(ValueError,'exists'):m.output_guard(proof,root,[proof])
            with self.assertRaisesRegex(ValueError,'AP0 manifest hash'):m.load_inputs(root,proof,proof)
            with patch.object(m,'AP0_SHA',m.digest(proof)):
                with self.assertRaisesRegex(ValueError,'AP3 report hash'):m.load_inputs(root,proof,proof)
            alias=p/'alias';alias.symlink_to(root,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'Link/reparse'):m.output_guard(alias/'out',root,[proof])
            self.assertEqual(proof.read_bytes(),b'forged')
            self.assertEqual(m.output_guard(p/'new.json',root,[proof]),p/'new.json')

    def test_aggregate_analysis_reopen_separate(self):
        n=160;t=1609459200000+np.arange(n)*60000;t[80:]+=60000
        c=100+np.arange(n)*.01;c[80:]+=10
        seg=np.zeros(n,dtype=int);seg[80:]=1
        gaps=np.full(n,np.nan);gaps[80]=61100
        a=dict(minute_start_ms_utc=t,first_tick_ms=t+100,last_tick_ms=t+59000,
               segment_id=seg,segment_start=np.isin(np.arange(n),[0,80]),
               gap_before_ms=gaps,mid_open=c,mid_close=c,mid_high=c+.001,mid_low=c-.001)
        with patch.object(m,'N_SEGMENTS',2):z=m.analyze(a,enforce=False)
        self.assertEqual(z['coverage']['valid_1m_returns'],158)
        self.assertEqual(z['horizons']['15']['valid_windows'],130)
        self.assertEqual(z['horizons']['60']['valid_windows'],40)
        self.assertEqual(z['reopen']['boundary_count'],1)
        self.assertAlmostEqual(z['reopen']['signed_discontinuous_log_bps']['mean'],np.log(c[80]/c[79])*10000)
        self.assertLess(z['horizons']['60']['signed_displacement_bps']['max'],100)
        self.assertEqual(sum(v['minute_rows'] for v in z['utc_years']),n)

if __name__=='__main__':unittest.main(verbosity=2)
