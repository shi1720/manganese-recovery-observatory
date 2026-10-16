"""Independently recompute headlines using only Python's standard library."""
from pathlib import Path
import json
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1]
annual={}
for y in range(2015,2026):
 p=ROOT/f'data/raw/A_{y}_268_X.json'
 rows=json.loads(p.read_text(),parse_float=D)['data'];r=[x for x in rows if x['partnerCode']!=0]
 v=sum(D(str(x['primaryValue'])) for x in r);q=sum(D(str(x['netWgt'])) for x in r)
 h=sum((D(str(x['primaryValue']))/v)**2 for x in r)
 annual[y]=(v,q,h)
results=[]
for b,t in [(2022,2024),(2023,2024),(2024,2025),(2019,2024)]:
 v0,q0,h0=annual[b];v1,q1,h1=annual[t]
 results.append(dict(base=b,target=t,value_change_pct=str(100*(v1/v0-1)),weight_change_pct=str(100*(q1/q0-1)),hhi_change_pct=str(100*(h1/h0-1))))
# Compare with the independently generated CSV, allowing only rounding noise.
import csv
with open(ROOT/'data/derived/baseline_sensitivity.csv') as f:csvrows=list(csv.DictReader(f))
for x in results:
 c=next(r for r in csvrows if int(r['base'])==x['base'] and int(r['target'])==x['target'])
 for a,b in [('value_change_pct','value_usd_change_pct'),('weight_change_pct','weight_kg_change_pct'),('hhi_change_pct','hhi_value_change_pct')]:
  assert abs(D(x[a])-D(c[b]))<D('0.000001'),(a,x,c)
(ROOT/'data/derived/independent_verification.json').write_text(json.dumps(results,indent=2)+'\n')
print('Independent Decimal recomputation agrees with primary results at < 0.000001 percentage point.')
