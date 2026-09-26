import importlib.util, os, pathlib, tempfile
import numpy as np

MODULE_PATH=os.environ.get('AP6_MODULE_PATH','/mnt/data/ap6_seasonality_stability.py')
spec=importlib.util.spec_from_file_location('ap6_under_test',MODULE_PATH); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def ck(cond,msg):
    if not cond: raise AssertionError(msg)

def test_gap_return():
    minute=np.array([0,60000,180000],np.int64); seg=np.array([0,0,0]); close=np.array([100.,101.,102.])
    r,v=m.signed_return_1m_bps(minute,seg,close)
    ck(v.tolist()==[False,True,False],'gap return crossed')

def test_rv_gap_and_efficiency():
    minute=np.arange(0,17)*60000; minute[8:]+=60000
    seg=np.zeros(17,dtype=np.int64); close=np.exp(np.arange(17)*0.001)*100
    r,v=m.signed_return_1m_bps(minute,seg,close)
    rv=m.rolling_realized_vol_bps(r,v,minute,seg,15); ef=m.efficiency_array(r,v,15)
    ck(not np.isfinite(rv[15]) and not np.isfinite(ef[15]),'gap window accepted')

def test_segment_boundary():
    minute=np.arange(0,17)*60000; seg=np.zeros(17,dtype=np.int64); seg[8:]=1; close=np.exp(np.arange(17)*0.001)*100
    r,v=m.signed_return_1m_bps(minute,seg,close); rv=m.rolling_realized_vol_bps(r,v,minute,seg,15)
    ck(not np.isfinite(rv[15]),'segment-cross RV accepted')

def test_rv_boundary_gap_direct():
    minute=np.arange(16,dtype=np.int64)*60000; minute[8:]+=60000
    seg=np.zeros(16,dtype=np.int64); signed=np.ones(16,dtype=float); valid=np.ones(16,dtype=bool)
    rv=m.rolling_realized_vol_bps(signed,valid,minute,seg,15)
    ck(not np.isfinite(rv[15]),'RV boundary gap accepted directly')

def test_dst_hour():
    ts=np.array([1741501800000,1741505400000],np.int64)
    h,w,mo,y,q=m.time_dimensions(ts); ck(h.tolist()==[1,3],'DST hour mapping broken')

def test_ny_month_not_utc():
    ts=np.array([1740789000000],np.int64); h,w,mo,y,q=m.time_dimensions(ts)
    ck(int(mo[0])==2 and int(y[0])==2025,'NY month mapping broken')

def test_weekday():
    ts=np.array([1758542400000],np.int64); h,w,mo,y,q=m.time_dimensions(ts); ck(int(w[0])==0,'weekday shifted')

def test_quarter():
    ts=np.array([1740789000000,1748736000000],np.int64); h,w,mo,y,q=m.time_dimensions(ts)
    ck(q.tolist()==[20251,20252],'UTC quarter wrong')

def test_reference_mask():
    y=np.array([2021,2022,2023,2024,2025,2026]); ck(m.reference_mask(y).tolist()==[False,True,True,True,True,False],'partial years leaked')

def test_cdf_fixed_thresholds():
    ref=np.arange(100,dtype=float); thresholds=np.percentile(ref,m.DECILES,method='linear'); rc=m.cdf_at_thresholds(ref,thresholds)
    d=m.cdf_distance(np.arange(100,200,dtype=float),thresholds,rc); ck(d>0.8,'CDF drift not detected')

def test_spearman_ties():
    r=m.spearman([1,1,2,3],[4,4,5,6]); ck(abs(r-1.0)<1e-12,'Spearman tie ranks wrong')

def test_spearman_not_pearson():
    x=[1,2,3,4]; y=[1,4,9,16]; r=m.spearman(x,y); ck(abs(r-1.0)<1e-12,'Spearman raw Pearson substitution')

def test_persistence_period_boundary():
    r=np.array([np.nan,1,1,1,1],float); v=np.array([False,True,True,True,True]); b=np.array([False,False,True,True,True])
    p=m.persistence_summary(r,v,b); ck(p['eligible_pairs']==2,'cross-bucket adjacency counted')

def test_binding_chain():
    ap3={'schema':'ATDS_AP3_EXPANSION_COMPRESSION_V0_1','status':'AP3_COMPLETE','binding':{'ap2_sha256':m.EXPECTED_AP2_SHA256,'ap0_manifest_sha256':m.EXPECTED_AP0_MANIFEST_SHA256}}
    ap4={'schema':'ATDS_AP4_PRICE_STRUCTURE_V0_1','status':'AP4_COMPLETE','binding':{'ap3_sha256':m.EXPECTED_AP3_SHA256,'ap0_manifest_sha256':m.EXPECTED_AP0_MANIFEST_SHA256}}
    ap5={'schema':'ATDS_AP5_MICROSTRUCTURE_PRICE_CORE_V0_1','status':'AP5_COMPLETE','binding':{'ap4_sha256':m.EXPECTED_AP4_SHA256,'ap0_manifest_sha256':m.EXPECTED_AP0_MANIFEST_SHA256}}
    m.validate_upstream_bindings(ap3,ap4,ap5)
    ap5['binding']['ap4_sha256']='bad'
    try: m.validate_upstream_bindings(ap3,ap4,ap5); raise AssertionError('bad binding accepted')
    except RuntimeError: pass

def test_symlink_chain():
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td); real=root/'real'; real.mkdir(); (real/'f').write_text('x')
        link=root/'link'
        try: link.symlink_to(real,target_is_directory=True)
        except OSError: return
        ck(m.path_chain_has_reparse_or_symlink(link/'f'),'symlink chain bypass')

def test_scope():
    ck(m.SCOPE['source_volume_used'] is False,'volume scope'); ck(m.SCOPE['stability_threshold_applied'] is False,'threshold scope'); ck(m.SCOPE['pnl_calculated'] is False,'PnL scope')

def test_average_ranks_tie_exact():
    r=m.average_ranks([10,10,20]); ck(np.allclose(r,[1.5,1.5,3.0]),'average tie ranks wrong')

def test_partition_conservation():
    vals=np.array([1.,2.,3.]); metrics={'x':vals}
    buckets=[{'minute_count':1,'source_tick_count':2,'metrics':{'x':{'count':1}}},{'minute_count':2,'source_tick_count':5,'metrics':{'x':{'count':2}}}]
    m.assert_partition_conservation(buckets,metrics,3,7)
    bad=[dict(b) for b in buckets]; bad[1]=dict(bad[1]); bad[1]['minute_count']=1
    try: m.assert_partition_conservation(bad,metrics,3,7); raise AssertionError('partition violation accepted')
    except RuntimeError: pass

def test_population_cv():
    ck(abs(m.population_cv([2,2,2,2]))<1e-15,'CV constant wrong')

def main():
    tests=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
    for t in tests: t(); print('PASS',t.__name__)
    print(f'{len(tests)}/{len(tests)} PASS')
if __name__=='__main__': main()
