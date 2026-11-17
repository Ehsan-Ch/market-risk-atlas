"""Reconcile exported forecasts, summaries and source/protocol digests."""
import csv,json
from pathlib import Path
import numpy as np
from risk import summarize
from ingest import sha256
root=Path(__file__).parent;r=json.loads((root/'report.json').read_text(encoding='utf-8'))
assert sha256(root/'config.json')==r['config_sha256'];assert sha256(root/'data/source_manifest.json')==r['manifest_sha256']
with open(root/'forecasts.csv',encoding='utf-8') as f:export=list(csv.DictReader(f))
assert len(export)==len(r['rows'])==r['evaluated']
for a,b in zip(export,r['rows']):
 assert a['prediction_time']==b['prediction_time'] and a['target_end']==b['target_end'];assert float(a['return_bps'])==b['return_bps']
 assert a['prediction_time']<a['target_end']
 for model in ['historical','ewma']:
  for level in [95,99]:assert float(a[model+str(level)])==b[model][str(level)]
for m in r['summary']:
 actual=summarize(r['rows'],m['model'],m['level'])
 for key,value in actual.items():assert abs(value-m[key])<1e-10
for day in r['daily']:
 rows=[x for x in r['rows'] if x['date']==day['date']];assert len(rows)==day['n'];assert abs(np.sqrt(sum(x['return_bps']**2 for x in rows))-day['realized_vol_bps'])<1e-9
print(f"Verified {len(export):,} exported forecasts, all model summaries and daily volatility; protocol/source hashes match.")
