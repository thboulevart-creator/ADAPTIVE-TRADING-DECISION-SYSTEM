from __future__ import annotations
import copy, importlib.util, json, math, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=load('primary',ROOT/'tools/bepd09c_runtime.py'); R=load('reference',ROOT/'tools/bepd09c_reference.py'); F=load('fixture',ROOT/'tools/bepd09c_synthetic_fixture.py')
FX=F.build_fixture(); ROWS=FX['rows']; CAL=FX['calendar']; ATOL=P.NUMERIC_PARITY_ATOL

def close(a,b,t=ATOL): return abs(float(a)-float(b))<=t

class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pr=P.run_protocol(ROWS,CAL); cls.rr=R.run_reference(ROWS,CAL)
    def assertBreaker(self, fn, *a, **k):
        with self.assertRaises(Exception): fn(*a,**k)
    def test_01_contract(self): self.assertEqual(P.CONTRACT,'ATDS_BEPD_09C_C1_EXECUTABLE_RUNTIME_V0_1')
    def test_02_dst_167(self): self.assertEqual(P.exposure_values('2026-03-02','2026-03-08T21:00:00Z')[0],167)
    def test_03_dst_168(self): self.assertEqual(P.exposure_values('2026-02-23','2026-03-01T22:00:00Z')[0],168)
    def test_04_dst_169(self): self.assertEqual(P.exposure_values('2026-10-26','2026-11-01T22:00:00Z')[0],169)
    def test_05_basis_025(self): self.assertEqual(P.spline_basis(.25),[.25,.015625,0.0,0.0])
    def test_06_basis_050(self): self.assertEqual(P.spline_basis(.5),[.5,.125,.015625,0.0])
    def test_07_basis_075(self): self.assertEqual(P.spline_basis(.75),[.75,.421875,.125,.015625])
    def test_08_basis_100(self): self.assertEqual(P.spline_basis(1.0),[1.0,.9375,.375,.09375])
    def test_09_invalid_exp_zero(self): self.assertBreaker(P.spline_basis,0)
    def test_10_invalid_exp_above(self): self.assertBreaker(P.spline_basis,1.01)
    def test_11_six_blocks(self): self.assertEqual(len(P.partition_calendar(CAL)),6)
    def test_12_block_sizes(self): self.assertLessEqual(max(map(len,P.partition_calendar(CAL)))-min(map(len,P.partition_calendar(CAL))),1)
    def test_13_empty_weeks_preserved(self):
        flat=[x for b in self.pr['blocks'] for x in b]; self.assertEqual(flat,CAL)
        for w in FX['special_cases']['empty_weeks']: self.assertIn(w,flat)
    def test_14_five_folds(self): self.assertEqual(len(self.pr['folds']),5)
    def test_15_train_test_week_disjoint(self):
        for f in self.pr['folds']:
            tr={x for b in f['train_weeks'] for x in b}; self.assertFalse(tr & set(f['test_weeks']))
    def test_16_multiple_events_same_week_cluster(self):
        by={}
        for r in ROWS: by.setdefault(r['target_week_id'],[]).append(r)
        self.assertTrue(any(len(v)>=3 and len({x['sweep_cluster_id'] for x in v})==1 for v in by.values()))
    def test_17_train_only_stats_exist(self):
        self.assertTrue(all(set(f['standardization'])=={'age','active','overshoot'} for f in self.pr['folds']))
    def test_18_baseline_context_basis_parity(self):
        for f in self.pr['folds']:
            for b,c in zip(f['baseline_design'],f['context_design']): self.assertEqual(b,c[:5])
    def test_19_side_not_standardized(self):
        self.assertTrue(all(row[5] in (0.0,1.0) for f in self.pr['folds'] for row in f['context_design']))
    def test_20_no_auto_verdict(self): self.assertEqual(self.pr['automatic_verdict'],'NONE_HUMAN_ADJUDICATION_REQUIRED')
    def test_21_deterministic_replay(self): self.assertEqual(self.pr['deterministic_replay_identity'],P.run_protocol(ROWS,CAL)['deterministic_replay_identity'])
    def test_22_reference_blocks_exact(self): self.assertEqual(self.pr['blocks'],self.rr['blocks'])
    def test_23_reference_design_parity(self):
        for a,b in zip(self.pr['folds'],self.rr['folds']):
            self.assertEqual(a['test_weeks'],b['test_weeks'])
            for xa,xb in zip(a['baseline_design'],b['baseline_design']): self.assertTrue(all(close(x,y,1e-12) for x,y in zip(xa,xb)))
            for xa,xb in zip(a['context_design'],b['context_design']): self.assertTrue(all(close(x,y,1e-12) for x,y in zip(xa,xb)))
    def test_24_reference_probability_parity(self):
        for a,b in zip(self.pr['folds'],self.rr['folds']):
            self.assertTrue(all(close(x,y) for x,y in zip(a['baseline_probabilities'],b['baseline_probabilities'])))
            self.assertTrue(all(close(x,y) for x,y in zip(a['context_probabilities'],b['context_probabilities'])))
    def test_25_reference_metric_parity(self):
        for k,v in self.pr['aggregate'].items(): self.assertTrue(close(v,self.rr['aggregate'][k]))
    def test_26_missing_value_breaker(self):
        x=copy.deepcopy(ROWS);x[0].pop('side');self.assertBreaker(P.run_protocol,x,CAL)
    def test_27_invalid_side_breaker(self):
        x=copy.deepcopy(ROWS);x[0]['side']='X';self.assertBreaker(P.run_protocol,x,CAL)
    def test_28_nonfinite_breaker(self):
        x=copy.deepcopy(ROWS);x[0]['level_age_weeks']=float('nan');self.assertBreaker(P.run_protocol,x,CAL)
    def test_29_zero_price_breaker(self):
        x=copy.deepcopy(ROWS);x[0]['level_price_mid']=0;self.assertBreaker(P.run_protocol,x,CAL)
    def test_30_duplicate_breaker(self):
        x=copy.deepcopy(ROWS);x[1]['event_id']=x[0]['event_id'];self.assertBreaker(P.run_protocol,x,CAL)
    def test_31_week_mismatch_breaker(self):
        x=copy.deepcopy(ROWS);x[0]['target_week_id']='2030-01-07';self.assertBreaker(P.run_protocol,x,CAL)
    def test_32_cluster_mismatch_breaker(self):
        x=copy.deepcopy(ROWS);x[1]['sweep_cluster_id']=x[0]['sweep_cluster_id'];x[1]['target_week_id']=CAL[1];self.assertBreaker(P.run_protocol,x,CAL)
    def test_33_one_class_breaker(self):
        x=copy.deepcopy(ROWS)
        first=set(P.partition_calendar(CAL)[0])
        for r in x:
            if r['target_week_id'] in first:r['same_week_reintegration']=True
        self.assertBreaker(P.run_protocol,x,CAL)
    def test_34_zero_variance_breaker(self):
        x=copy.deepcopy(ROWS)
        for r in x:r['level_age_weeks']=3
        self.assertBreaker(P.run_protocol,x,CAL)
    def test_35_perfect_separation_breaker(self):
        import numpy as np
        X=np.array([[1,-2],[1,-1],[1,1],[1,2]],float);y=np.array([0,0,1,1],float);self.assertBreaker(P.fit_logistic,X,y)
    def test_36_nonconvergence_breaker(self):
        import numpy as np
        X=np.array([[1,-1],[1,-.5],[1,.5],[1,1]],float);y=np.array([0,1,0,1],float);self.assertBreaker(P.fit_logistic,X,y,1,1e-30)
    def test_37_target_week_split_breaker(self):
        a=[{'target_week_id':'2026-01-05','sweep_cluster_id':'A'}];b=[{'target_week_id':'2026-01-05','sweep_cluster_id':'B'}];self.assertBreaker(P.validate_fold_integrity,a,b)
    def test_38_cluster_split_breaker(self):
        a=[{'target_week_id':'2026-01-05','sweep_cluster_id':'A'}];b=[{'target_week_id':'2026-01-12','sweep_cluster_id':'A'}];self.assertBreaker(P.validate_fold_integrity,a,b)
    def test_39_post_t0_feature_attempt(self): self.assertBreaker(P.run_protocol,ROWS,CAL,P.CONTEXT_FEATURES+('target_week_close_mid',))
    def test_40_output_no_forbidden_fields(self):
        s=json.dumps(self.pr)
        for x in ('P_VALUE','CONFIDENCE_INTERVAL','AUC','OPTIMAL_THRESHOLD','TRADING_SIGNAL'): self.assertNotIn(x,s)

    def test_41_reference_exposure_basis_parity(self):
        a=P.validate_rows(ROWS,CAL); b=R._prep(ROWS,CAL)
        self.assertEqual(len(a),len(b))
        for x,y in zip(a,b):
            self.assertTrue(close(x['exposure_fraction'],y['exposure'],1e-12))
            self.assertTrue(all(close(u,v,1e-12) for u,v in zip(x['basis'],y['basis'])))
    def test_42_reference_standardization_parity(self):
        for a,b in zip(self.pr['folds'],self.rr['folds']):
            for k in ('age','active','overshoot'):
                self.assertTrue(close(a['standardization'][k]['mean'],b['standardization'][k]['mean'],1e-12))
                self.assertTrue(close(a['standardization'][k]['sample_sd'],b['standardization'][k]['sample_sd'],1e-12))
    def test_43_reference_weekly_loss_parity(self):
        for a,b in zip(self.pr['folds'],self.rr['folds']):
            self.assertEqual(set(a['weekly']),set(b['weekly']))
            for w in a['weekly']:
                for k,v in a['weekly'][w].items(): self.assertTrue(close(v,b['weekly'][w][k]))
    def test_44_reference_deterministic_replay(self):
        self.assertEqual(self.rr['deterministic_replay_identity'],R.run_reference(ROWS,CAL)['deterministic_replay_identity'])

if __name__=='__main__': unittest.main()
