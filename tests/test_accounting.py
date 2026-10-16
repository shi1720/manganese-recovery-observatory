import unittest,sys,json,random
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze import hhi,midpoint,group_shapley,load,ROOT
class AccountingTests(unittest.TestCase):
 def test_midpoint_exact(self):
  rng=random.Random(20261016)
  for _ in range(1000):
   q0,q1=rng.uniform(1,1e6),rng.uniform(1,1e6);v0,v1=q0*rng.uniform(.1,5),q1*rng.uniform(.1,5)
   c,p=midpoint(v0,q0,v1,q1);self.assertAlmostEqual(c+p,v1-v0,places=7)
 def test_zero_quantity_rejected(self):
  with self.assertRaises(AssertionError):midpoint(1,0,2,1)
 def test_hhi_scale_invariance(self):
  self.assertAlmostEqual(hhi([1,2,3]),hhi([100,200,300]))
 def test_hhi_known(self):
  self.assertEqual(hhi([1,1,1,1]),.25);self.assertEqual(hhi([7,0]),1)
 def test_group_attribution_exact(self):
  rng=np.random.default_rng(20261016)
  for _ in range(1000):
   a,b=rng.uniform(0,100,(2,8));g=rng.integers(0,2,8).astype(bool)
   sh=group_shapley(a,b,g);self.assertAlmostEqual(sum(sh),hhi(b)-hhi(a),places=12)
 def test_group_permutation(self):
  a=[3,5,2];b=[1,2,7]
  x,y=group_shapley(a,b,[True,False,False]);yy,xx=group_shapley(a,b,[False,True,True]);self.assertAlmostEqual(x,xx);self.assertAlmostEqual(y,yy)
 def test_manifest_keys_and_hashes(self):load()
 def test_georgia_all_partner_sums(self):
  d=load();g=d[d.reporterCode==268]
  for key,a in g.groupby(['freqCode','period']):
   self.assertEqual(len(a[a.partnerCode==0]),1,key)
   w=a[a.partnerCode==0].iloc[0];p=a[a.partnerCode!=0]
   self.assertLess(abs(p.primaryValue.sum()-w.primaryValue),.02,key)
   self.assertLess(abs(p.netWgt.sum()-w.netWgt),.02,key)
 def test_georgia_weights_nonestimated(self):
  d=load();g=d[d.reporterCode==268];self.assertFalse(g.isNetWgtEstimated.any());self.assertTrue((g.qtyUnitCode==8).all());bad=g[(g.qty-g.netWgt).abs()>.01];self.assertEqual(set(zip(bad.freqCode,bad.period.astype(int),bad.partnerCode)),{('A',2015,0),('A',2015,643),('A',2015,792)})
 def test_full_annual_window(self):
  d=load();self.assertEqual(set(d[(d.freqCode=='A')&(d.reporterCode==268)].refYear),set(range(2015,2026)))
 def test_full_monthly_window(self):
  d=load();m=d[(d.freqCode=='M')&(d.reporterCode==268)&(d.partnerCode==0)];self.assertEqual(set(m.period.astype(int)),{y*100+i for y in range(2021,2026) for i in range(1,13)})
 def test_monthly_vs_annual(self):
  d=load();g=d[(d.reporterCode==268)&(d.partnerCode==0)]
  for y in range(2021,2026):
   a=g[(g.freqCode=='A')&(g.refYear==y)].iloc[0];m=g[(g.freqCode=='M')&(g.refYear==y)]
   self.assertLess(abs(m.primaryValue.sum()-a.primaryValue),.1)
   self.assertAlmostEqual(m.netWgt.sum()-a.netWgt,171.5 if y==2022 else 0.,places=3)
 def test_reference_endpoint_weights(self):
  d=load();r=d[(d.reporterCode.isin([710,699,458,579]))&(d.refYear.isin([2022,2024,2025]))]
  self.assertEqual(len(r),12);self.assertTrue((r.netWgt>0).all());self.assertFalse(r.isNetWgtEstimated.any())
if __name__=='__main__':unittest.main(verbosity=2)
