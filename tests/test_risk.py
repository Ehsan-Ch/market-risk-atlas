import unittest
import numpy as np
from statistics import NormalDist
from risk import forecast,summarize,drawdowns
class RiskTests(unittest.TestCase):
 def test_future_changes_do_not_change_forecasts(self):
  x=np.sin(np.arange(100))*3;a=forecast(x,20);x[50:]=100;b=forecast(x,20)
  for r,s in zip(a,b):
   if r['index']<=50:self.assertEqual(r['historical'],s['historical']);self.assertEqual(r['ewma'],s['ewma'])
 def test_initial_sigma_from_training_only(self):
  x=[1,-2,3,-4,999];r=forecast(x,4)[0];self.assertAlmostEqual(r['sigma_bps'],np.sqrt(7.5))
 def test_ewma_update_after_outcome(self):
  r=forecast([1,-1,1,-1,10,0],4,decay=.5);self.assertAlmostEqual(r[1]['sigma_bps']**2,50.5)
 def test_historical_previous_window(self):
  r=forecast([1,2,3,4,-100,0],4);self.assertAlmostEqual(r[0]['historical']['95'],float(np.quantile([-1,-2,-3,-4],.95)));self.assertGreater(r[1]['historical']['95'],50)
 def test_normal_threshold(self):
  r=forecast([1,-1,1,-1,0],4)[0];self.assertAlmostEqual(r['ewma']['99'],NormalDist().inv_cdf(.99))
 def test_boundary_is_not_breach(self):
  r=[{'return_bps':-5,'historical':{'95':5}},{'return_bps':-6,'historical':{'95':5}}];m=summarize(r,'historical',95);self.assertEqual(m['breaches'],1);self.assertEqual(m['worst_excess_bps'],1)
 def test_pinball_scoring(self):
  r=[{'return_bps':-6,'historical':{'95':5}}];self.assertAlmostEqual(summarize(r,'historical',95)['pinball_bps'],.95)
 def test_drawdown_tracks_running_peak(self):
  np.testing.assert_allclose(drawdowns([100,120,90,130]),[0,0,-.25,0])
 def test_invalid_inputs(self):
  for x in [[1,float('nan'),3],[1,2]]:
   with self.assertRaises(ValueError):forecast(x,2)
  with self.assertRaises(ValueError):drawdowns([0,1])
 def test_longest_breach_streak(self):
  rows=[{'return_bps':x,'ewma':{'99':1}}for x in [-2,-3,0,-2]];self.assertEqual(summarize(rows,'ewma',99)['longest_breach_run'],2)
if __name__=='__main__':unittest.main()
