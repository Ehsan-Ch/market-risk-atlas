"""One-step risk forecasts. Each forecast uses only returns before its target."""
from statistics import NormalDist
import numpy as np

def forecast(returns,history=864,decay=.94,levels=(.95,.99)):
    r=np.asarray(returns,dtype=float)
    if r.ndim!=1 or not np.isfinite(r).all() or history<2 or len(r)<=history or not 0<decay<1 or not all(.5<x<1 for x in levels):raise ValueError('Invalid risk configuration or returns')
    variance=float(np.mean(r[:history]**2));rows=[]
    for i in range(history,len(r)):
        row={'index':i,'return_bps':float(r[i]),'sigma_bps':float(np.sqrt(variance)),'historical':{},'ewma':{}}
        for level in levels:
            key=str(int(level*100));row['historical'][key]=float(np.quantile(-r[i-history:i],level,method='linear'))
            row['ewma'][key]=float(NormalDist().inv_cdf(level)*np.sqrt(variance))
        rows.append(row);variance=decay*variance+(1-decay)*r[i]**2
    return rows

def summarize(rows,model,level):
    if not rows:raise ValueError('No evaluated forecasts')
    q=level/100;loss=np.array([-r['return_bps'] for r in rows]);var=np.array([r[model][str(level)] for r in rows]);breach=loss>var
    residual=loss-var;pinball=np.maximum(q*residual,(q-1)*residual)
    longest=streak=0
    for b in breach:streak=streak+1 if b else 0;longest=max(longest,streak)
    return {'n':len(rows),'breaches':int(breach.sum()),'breach_rate':float(breach.mean()),'expected_rate':1-q,'mean_var_bps':float(var.mean()),'pinball_bps':float(pinball.mean()),'longest_breach_run':longest,'worst_excess_bps':float(max(0,np.max(residual)))}

def drawdowns(prices):
    p=np.asarray(prices,dtype=float)
    if p.ndim!=1 or len(p)==0 or not np.isfinite(p).all() or (p<=0).any():raise ValueError('Invalid prices')
    return p/np.maximum.accumulate(p)-1
