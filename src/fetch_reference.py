"""External unit-receipts comparator: four major suppliers identified before querying."""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
import json,hashlib,time
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'data/manifest.json').read_text());seen={r['file'] for r in manifest}
for reporter,name in [(710,'South Africa'),(699,'India'),(458,'Malaysia'),(579,'Norway')]:
 for year in range(2019,2026):
  params=dict(period=year,reporterCode=reporter,cmdCode='720230',flowCode='X',partnerCode=0,partner2Code=0,customsCode='C00',motCode=0,maxRecords=500)
  u='https://comtradeapi.un.org/public/v1/preview/C/A/HS?'+urlencode(params);p=R/f'data/raw/REF_A_{year}_{reporter}_X.json'
  if not p.exists():
   for attempt in range(6):
    try:
     b=urlopen(u,timeout=60).read();d=json.loads(b);assert not d.get('error');assert d['count']==len(d['data'])==1;(p).write_bytes(b);break
    except Exception:
     if attempt==5:raise
     time.sleep(2**attempt)
   time.sleep(.6)
  b=p.read_bytes();entry=dict(file=str(p.relative_to(R)),url=u,sha256=hashlib.sha256(b).hexdigest(),records=1,retrieval_session_date='2026-10-16')
  if entry['file'] not in seen:manifest.append(entry);seen.add(entry['file']);(R/'data/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  print(name,year,flush=True)
