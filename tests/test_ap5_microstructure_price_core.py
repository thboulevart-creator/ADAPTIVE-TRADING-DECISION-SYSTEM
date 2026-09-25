from __future__ import annotations
import importlib.util
import math
import os
import unittest
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def load_module():
    p=Path(os.environ.get("AP5_HELPER_PATH", Path(__file__).parents[1]/"tools"/"ap5_microstructure_price_core.py"))
    spec=importlib.util.spec_from_file_location("ap5mod",p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M=load_module()

class AP5Tests(unittest.TestCase):
    def test_tick_weighted_mean_is_not_simple_mean(self):
        self.assertAlmostEqual(M.tick_weighted_mean(np.array([1.0,3.0]),np.array([1,9])),2.8)
        self.assertNotAlmostEqual(M.tick_weighted_mean(np.array([1.0,3.0]),np.array([1,9])),2.0)

    def test_gap_and_segment_cut_return(self):
        minute=np.array([0,60_000,180_000,240_000],dtype=np.int64)
        seg=np.array([0,0,1,1],dtype=np.int64)
        close=np.array([100.0,101.0,200.0,202.0])
        x=M.compute_abs_return_1m_bps(minute,seg,close)
        self.assertTrue(np.isnan(x[0]))
        self.assertAlmostEqual(x[1],abs(math.log(101/100))*10000)
        self.assertTrue(np.isnan(x[2]))
        self.assertAlmostEqual(x[3],abs(math.log(202/200))*10000)

    def test_minute_range_uses_open_denominator(self):
        x=M.compute_minute_range_bps(np.array([100.0]),np.array([102.0]),np.array([99.0]))
        self.assertAlmostEqual(float(x[0]),300.0)

    def test_cash_clock_boundaries_and_dst(self):
        # 2025-01-06 14:29/14:30/20:59/21:00 UTC => 09:29/09:30/15:59/16:00 NY (EST)
        vals=[datetime(2025,1,6,14,29,tzinfo=timezone.utc),datetime(2025,1,6,14,30,tzinfo=timezone.utc),datetime(2025,1,6,20,59,tzinfo=timezone.utc),datetime(2025,1,6,21,0,tzinfo=timezone.utc)]
        ms=np.array([int(v.timestamp()*1000) for v in vals],dtype=np.int64)
        h,w,mday,_=M.ny_time_dimensions(ms); codes=M.cash_clock_proxy_codes(w,mday)
        self.assertEqual(codes.tolist(),[1,0,0,1])
        # Summer EDT: 13:30 UTC => 09:30 NY.
        summer=np.array([int(datetime(2025,7,7,13,30,tzinfo=timezone.utc).timestamp()*1000)],dtype=np.int64)
        h,w,mday,_=M.ny_time_dimensions(summer); self.assertEqual(M.cash_clock_proxy_codes(w,mday).tolist(),[0])

    def test_weekend_is_separate(self):
        ms=np.array([int(datetime(2025,1,4,15,0,tzinfo=timezone.utc).timestamp()*1000)],dtype=np.int64)
        _,w,mday,_=M.ny_time_dimensions(ms); self.assertEqual(M.cash_clock_proxy_codes(w,mday).tolist(),[2])

    def test_quintile_equality_goes_right(self):
        th,c=M.quintile_codes(np.array([1.,2.,3.,4.,5.]),thresholds=np.array([1.,2.,3.,4.]))
        self.assertEqual(c.tolist(),[1,2,3,4,4])
        self.assertEqual(len(c),5)

    def test_pearson_oracle_and_constant(self):
        r=M.pearson_summary(np.array([1.,2.,3.]),np.array([2.,4.,6.]))
        self.assertAlmostEqual(r["pearson"],1.0)
        self.assertIsNone(M.pearson_summary(np.array([1.,1.,1.]),np.array([1.,2.,3.]))["pearson"])

    def test_validate_arrays_rejects_tick_and_spread_violations(self):
        minute=np.array([0,60_000],dtype=np.int64); tick=np.array([1,2],dtype=np.int64); seg=np.array([0,0],dtype=np.int64); ss=np.array([True,False])
        op=np.array([100.,101.]); hi=np.array([101.,102.]); lo=np.array([99.,100.]); cl=np.array([100.5,101.5]); sm=np.array([2.,2.]); smin=np.array([1.,1.]); smax=np.array([3.,3.])
        M.validate_arrays(minute,tick,seg,ss,op,hi,lo,cl,sm,smin,smax,None)
        with self.assertRaises(ValueError): M.validate_arrays(minute,np.array([1,0]),seg,ss,op,hi,lo,cl,sm,smin,smax,None)
        with self.assertRaises(ValueError): M.validate_arrays(minute,tick,seg,ss,op,hi,lo,cl,np.array([0.5,2.]),smin,smax,None)

    def test_bucket_summary_conserves_counts(self):
        tick=np.array([1,2,3,4]); sm=np.array([1.,2.,3.,4.]); sx=np.array([2.,3.,4.,5.]); rg=np.array([10.,20.,30.,40.])
        a=M.bucket_summary(np.array([True,False,True,False]),tick,sm,sx,rg)
        self.assertEqual(a["minute_count"],2); self.assertEqual(a["source_tick_count"],4)
        self.assertAlmostEqual(a["spread_tick_weighted_mean"],2.5)

    def test_read_columns_exclude_source_volume(self):
        self.assertFalse(any("volume" in c.lower() for c in M.READ_COLUMNS))

    def test_path_chain_rejects_symlink_component(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); target=base/"target"; target.mkdir(); link=base/"link"
            try:
                link.symlink_to(target, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            self.assertTrue(M.path_chain_has_reparse_or_symlink(link/"child.json"))
            self.assertFalse(M.path_chain_has_reparse_or_symlink(target/"child.json"))

if __name__=="__main__": unittest.main()
