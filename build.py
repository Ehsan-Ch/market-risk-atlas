"""Build the fixed historical study from hash-verified source archives."""
import argparse,csv,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from ingest import aggregate_archive,sha256
from risk import forecast,summarize,drawdowns
ROOT=Path(__file__).parent
def iso(ms):return datetime.fromtimestamp(int(ms)/1000,timezone.utc).isoformat().replace('+00:00','Z')
def run(raw_dir):
    c=json.loads((ROOT/'config.json').read_text());manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
    closes=[];times=[];qualities=[]
    for source in manifest:
        p=raw_dir/source['url'].split('/')[-1]
        if sha256(p)!=source['sha256']:raise ValueError('Source archive digest mismatch')
        bars,quality=aggregate_archive(p,source['date'],c['bar_seconds'])
        if not np.isfinite(bars['close']).all() or (bars['age']>30).any():raise ValueError('Missing/stale source price')
        closes.extend(bars['close']);times.extend(bars['end']);qualities.append(quality);print('Verified '+source['date'],flush=True)
    prices=np.array(closes);times=np.array(times);returns=1e4*np.diff(np.log(prices));dd=drawdowns(prices)
    rows=forecast(returns,c['history_returns'],c['ewma_lambda'],c['levels'])
    for row in rows:
        i=row['index'];row.update(prediction_time=iso(times[i]),target_end=iso(times[i+1]),date=iso(times[i+1]-1)[:10],price_index=float(prices[i+1]/prices[0]*100),drawdown_pct=float(dd[i+1]*100))
    summary=[{'model':m,'level':l,**summarize(rows,m,l)} for m in ['historical','ewma'] for l in [95,99]]
    daily=[]
    for date in sorted(set(row['date'] for row in rows)):
        subset=[r for r in rows if r['date']==date]
        daily.append({'date':date,'n':len(subset),'realized_vol_bps':float(np.sqrt(sum(r['return_bps']**2 for r in subset))),'worst_return_bps':min(r['return_bps'] for r in subset),'summary':[{'model':m,'level':l,**summarize(subset,m,l)}for m in ['historical','ewma']for l in [95,99]]})
    report={'schema_version':1,'config':c,'config_sha256':sha256(ROOT/'config.json'),'manifest_sha256':sha256(ROOT/'data/source_manifest.json'),'quality':qualities,'bar_count':len(prices),'evaluated':len(rows),'max_drawdown_pct':float(dd.min()*100),'total_return_pct':float((prices[-1]/prices[0]-1)*100),'summary':summary,'daily':daily,'rows':rows}
    (ROOT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    with open(ROOT/'forecasts.csv','w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['prediction_time','target_end','return_bps','historical95','historical99','ewma95','ewma99'])
        for r in rows:w.writerow([r['prediction_time'],r['target_end'],r['return_bps'],r['historical']['95'],r['historical']['99'],r['ewma']['95'],r['ewma']['99']])
    print(json.dumps({'evaluated':len(rows),'summary':summary,'max_drawdown_pct':report['max_drawdown_pct']},indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--raw-dir',type=Path,default=ROOT/'data/raw');run(parser.parse_args().raw_dir)
