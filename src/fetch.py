"""Cache small, untruncated UN Comtrade public API responses; no credentials."""
import json, hashlib, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw'

def fetch(freq,year,reporter,flow):
    params=dict(period=str(year) if freq=='A' else str(year),reporterCode=reporter,cmdCode='720230',flowCode=flow,partner2Code=0,customsCode='C00',motCode=0,maxRecords=500)
    url=f'https://comtradeapi.un.org/public/v1/preview/C/{freq}/HS?'+urlencode(params)
    p=RAW/f'{freq}_{year}_{reporter}_{flow}.json'
    if not p.exists():
        for attempt in range(5):
            try:
                b=urlopen(url,timeout=60).read(); d=json.loads(b)
                assert not d.get('error'),d
                assert d['count']<500,'Potentially truncated response'
                assert d['count']==len(d['data'])
                p.write_bytes(b);break
            except Exception:
                if attempt==4: raise
                time.sleep(2**attempt)
        time.sleep(0.5)
    b=p.read_bytes();d=json.loads(b)
    return dict(file=str(p.relative_to(ROOT)),url=url,sha256=hashlib.sha256(b).hexdigest(),records=d['count'],retrieval_session_date='2026-10-16')

if __name__=='__main__':
    manifest=[]
    for freq,years in [('A',range(2015,2026)),('M',[y*100+m for y in range(2021,2026) for m in range(1,13)])]:
        for year in years:
            for reporter,flow in ([(268,'X'),(842,'M')] if freq=='A' else [(268,'X')]):
                r=fetch(freq,year,reporter,flow);manifest.append(r)
                print(r['file'],r['records'],flush=True)
                (ROOT/'data/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
