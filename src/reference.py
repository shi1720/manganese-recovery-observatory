"""Major-exporter comparison, keeping missing and estimated source fields visible."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
R=Path(__file__).resolve().parents[1];rows=[]
for code,name in [(710,'South Africa'),(699,'India'),(458,'Malaysia'),(579,'Norway')]:
 for year in range(2019,2026):
  r=json.loads((R/f'data/raw/REF_A_{year}_{code}_X.json').read_text())['data'][0]
  q=r['netWgt'];good=q is not None and q>0
  rows.append(dict(year=year,reporter=code,name=name,value_usd=r['primaryValue'],weight_kg=q,weight_estimated=r['isNetWgtEstimated'],weight_valid=good,unit_usd_kg=r['primaryValue']/q if good else np.nan))
d=pd.DataFrame(rows);d.to_csv(R/'data/derived/reference_exporters.csv',index=False)
summary=[]
for name,g in d.groupby('name',sort=False):
 g=g.set_index('year');assert all(g.loc[y,'weight_valid'] and not g.loc[y,'weight_estimated'] for y in [2022,2024,2025])
 p0,p1,p2=[float(g.loc[y,'unit_usd_kg']) for y in [2022,2024,2025]]
 summary.append(dict(name=name,unit_2022=p0,unit_2024=p1,unit_2025=p2,change_2022_2024_pct=100*(p1/p0-1),change_2022_2025_pct=100*(p2/p0-1)))
a=pd.read_csv(R/'data/derived/annual.csv').set_index('year');p0,p1,p2=[float(a.loc[y,'unit_usd_kg']) for y in [2022,2024,2025]]
summary.append(dict(name='Georgia',unit_2022=p0,unit_2024=p1,unit_2025=p2,change_2022_2024_pct=100*(p1/p0-1),change_2022_2025_pct=100*(p2/p0-1)))
s=pd.DataFrame(summary);s.to_csv(R/'data/derived/reference_comparison.csv',index=False);print(s.round(5).to_string(index=False))
