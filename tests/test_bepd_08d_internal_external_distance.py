import importlib.util,unittest
from decimal import Decimal
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"tools"/"bepd_08d_internal_external_distance.py"
S=importlib.util.spec_from_file_location("r",P);r=importlib.util.module_from_spec(S);S.loader.exec_module(r)
def row(i,v,**extra):
 x={"event_id":f"e{i}","close_displacement":Decimal(v),"same_week_reintegration":extra.get("reintegration",False),"side":extra.get("side","HIGH")}
 return x
class T(unittest.TestCase):
 def test_classification(self):
  self.assertEqual(r.classify(Decimal("1")),"INTERNAL");self.assertEqual(r.classify(Decimal("-1")),"EXTERNAL");self.assertEqual(r.classify(Decimal("0")),"EXACT_LEVEL")
 def test_zero_not_internal_external(self):
  self.assertNotIn(r.classify(Decimal("0")),["INTERNAL","EXTERNAL"])
 def test_distances_positive(self):
  g=r.partition_rows([row(1,"2"),row(2,"-3"),row(3,"0")],3,1,1,1);self.assertEqual(g["INTERNAL"],[Decimal("2")]);self.assertEqual(g["EXTERNAL"],[Decimal("3")])
 def test_no_negative_conditional(self):
  with self.assertRaises(ValueError):r.aggregate([Decimal("-1")])
 def test_rows_retained(self):
  g=r.partition_rows([row(1,"1"),row(2,"2"),row(3,"-1"),row(4,"-2")],4,2,2,0);self.assertEqual((len(g["INTERNAL"]),len(g["EXTERNAL"])),(2,2))
 def test_partition_mutual_exhaustive(self):
  g=r.partition_rows([row(1,"1"),row(2,"-1"),row(3,"0")],3,1,1,1);self.assertEqual(sum(map(len,g.values())),3)
 def test_irrelevant_fields_ignored(self):
  a=r.partition_rows([row(1,"1",reintegration=False,side="HIGH"),row(2,"-1",reintegration=True,side="LOW")],2,1,1,0)
  self.assertEqual((len(a["INTERNAL"]),len(a["EXTERNAL"])),(1,1))
 def test_missing(self):
  with self.assertRaisesRegex(ValueError,"missing close_displacement"):r.partition_rows([{"event_id":"x"}],1,0,0,1)
 def test_nonfinite(self):
  with self.assertRaisesRegex(ValueError,"non-finite"):r.partition_rows([row(1,"NaN")],1,0,0,1)
 def test_duplicate(self):
  x=[row(1,"1"),row(1,"-1")]
  with self.assertRaisesRegex(ValueError,"duplicate"):r.partition_rows(x,2,1,1,0)
 def test_population_mismatch(self):
  with self.assertRaisesRegex(ValueError,"partition population mismatch"):r.partition_rows([row(1,"1"),row(2,"-1")],2,2,0,0)
 def test_type7(self):
  xs=[Decimal("0"),Decimal("10")];self.assertEqual(r.q18(r.type7(xs,Decimal(".25"))),"2.500000000000000000")
 def test_p50_median(self):
  c=r.aggregate([Decimal("1"),Decimal("2"),Decimal("3")]);self.assertEqual(c["P50"],c["MEDIAN"])
 def test_internal_ecdf(self):
  c=r.aggregate([Decimal("1"),Decimal("1"),Decimal("2")]);self.assertEqual(c["EMPIRICAL_CDF"][-1]["cumulative_count"],3);self.assertEqual(c["EMPIRICAL_CDF"][-1]["cumulative_fraction"],"1")
 def test_external_ecdf(self):
  c=r.aggregate([Decimal("4"),Decimal("5")]);self.assertEqual(c["EMPIRICAL_CDF"][-1]["cumulative_count"],2)
 def test_half_even(self):
  self.assertEqual(r.q18(Decimal("1.0000000000000000005")),"1.000000000000000000")
 def test_surface_exact(self):
  self.assertEqual(set(r.aggregate([Decimal("1")])) , r.ALLOWED_CORE)
 def test_no_comparative(self):
  for k in ["comparative_metrics","difference_of_means","difference_of_medians","ratios","effect_size","significance_test","confidence_interval"]:
   self.assertFalse(r.POLICY[k])
 def test_no_threshold_tp_pnl_prediction(self):
  for k in ["threshold_search","tp_sl","pnl","prediction","edge","strategy_validation"]:self.assertFalse(r.POLICY[k])
  self.assertEqual(r.POLICY["trading_authority"],"NONE")
if __name__=="__main__":unittest.main()
