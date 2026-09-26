import os, pathlib, subprocess, tempfile, sys
SOURCE=pathlib.Path('/mnt/data/ap6_seasonality_stability.py').read_text()
TEST='/mnt/data/test_ap6_seasonality_stability.py'
MUTANTS=[
('RETURN_CROSS_GAP', '((minute[1:]-minute[:-1])==60_000)', '((minute[1:]-minute[:-1])>=60_000)'),
('RV_CROSS_GAP', '((minute[endpoints]-minute[endpoints-h])==h*60_000)', '((minute[endpoints]-minute[endpoints-h])>=h*60_000)'),
('EFFICIENCY_BAD_WINDOW', '(bad[t+1]-bad[t-h+1])==0', '(bad[t+1]-bad[t-h+1])<=1'),
('NY_TIMEZONE_UTC', 'NY = ZoneInfo("America/New_York")', 'NY = timezone.utc'),
('WEEKDAY_SHIFT', 'ny_weekday[i]=ny.weekday()', 'ny_weekday[i]=(ny.weekday()+1)%7'),
('NY_MONTH_REPLACED_UTC', 'ny_month[i]=ny.month', 'ny_month[i]=dt.month'),
('QUARTER_OFF_BY_ONE', '((dt.month-1)//3+1)', '(dt.month//3+1)'),
('PARTIAL_YEARS_LEAK_REFERENCE', 'return (y>=2022)&(y<=2025)', 'return (y>=2021)&(y<=2026)'),
('PERIOD_SPECIFIC_CDF_THRESHOLDS', 'c=np.asarray(cdf_at_thresholds(x,thresholds),dtype=np.float64); r=np.asarray(reference_cdf,dtype=np.float64)', 'thresholds=np.percentile(x,DECILES,method="linear"); c=np.asarray(cdf_at_thresholds(x,thresholds),dtype=np.float64); r=np.asarray(reference_cdf,dtype=np.float64)'),
('SPEARMAN_TO_PEARSON', 'return pearson(average_ranks(x),average_ranks(y))', 'return pearson(x,y)'),
('TIE_RANK_FIRST', 'rank=((i+1)+j)/2.0', 'rank=float(i+1)'),
('PERSISTENCE_CROSS_BUCKET', 'eligible &= b[1:] & b[:-1]', 'eligible &= b[1:]'),
('AP5_BINDING_BYPASS', 'if (ap5.get("binding") or {}).get("ap4_sha256") != EXPECTED_AP4_SHA256:', 'if False and (ap5.get("binding") or {}).get("ap4_sha256") != EXPECTED_AP4_SHA256:'),
('SYMLINK_CHAIN_BYPASS', 'if is_reparse_or_symlink(cur):\n                return True', 'if False and is_reparse_or_symlink(cur):\n                return True'),
('SOURCE_VOLUME_SCOPE_TRUE', '"source_volume_used": False,', '"source_volume_used": True,'),
('STABILITY_THRESHOLD_TRUE', '"stability_threshold_applied": False,', '"stability_threshold_applied": True,'),
('PNL_SCOPE_TRUE', '"pnl_calculated": False,', '"pnl_calculated": True,'),
('PARTITION_MINUTE_CHECK_BYPASS', 'if sum(b["minute_count"] for b in buckets)!=expected_minutes: raise RuntimeError("minute partition conservation failed")', 'if False and sum(b["minute_count"] for b in buckets)!=expected_minutes: raise RuntimeError("minute partition conservation failed")'),
]
killed=[]; survived=[]
for name,old,new in MUTANTS:
    if old not in SOURCE:
        print('SETUP_FAIL',name,'replacement not found'); sys.exit(2)
    mutated=SOURCE.replace(old,new,1)
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/'ap6_mutant.py'; p.write_text(mutated)
        env=os.environ.copy(); env['AP6_MODULE_PATH']=str(p)
        r=subprocess.run([sys.executable,TEST],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode!=0:
            killed.append(name); print('KILLED',name)
        else:
            survived.append(name); print('SURVIVED',name); print(r.stdout)
print(f'{len(killed)}/{len(MUTANTS)} KILLED')
if survived:
    print('SURVIVORS',','.join(survived)); sys.exit(1)
