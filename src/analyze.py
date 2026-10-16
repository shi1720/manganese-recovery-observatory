"""Deterministic accounting of HS720230 exports. Units: kg and current USD."""
import json,hashlib,itertools
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/derived';OUT.mkdir(exist_ok=True)
NAMES={0:'World',12:'Algeria',31:'Azerbaijan',36:'Australia',124:'Canada',156:'China',251:'France',268:'Georgia',276:'Germany',300:'Greece',380:'Italy',458:'Malaysia',484:'Mexico',498:'Moldova',504:'Morocco',528:'Netherlands',579:'Norway',604:'Peru',642:'Romania',643:'Russia',699:'India',710:'South Africa',724:'Spain',792:'Türkiye',804:'Ukraine',818:'Egypt',826:'United Kingdom',842:'United States'}

def hhi(v):
    v=np.asarray(v,dtype=float)
    assert np.all(v>=0) and v.sum()>0
    return float(np.sum((v/v.sum())**2))

def midpoint(v0,q0,v1,q1):
    assert q0>0 and q1>0
    p0,p1=v0/q0,v1/q1
    return (p0+p1)/2*(q1-q0),(q0+q1)/2*(p1-p0)

def group_shapley(v0,v1,mask):
    """Two groups; exactly average both update orders; fixed union support."""
    v0,v1=np.array(v0,float),np.array(v1,float);mask=np.array(mask,bool)
    a=np.where(mask,v1,v0);b=np.where(mask,v0,v1)
    return .5*((hhi(a)-hhi(v0))+(hhi(v1)-hhi(b))),.5*((hhi(b)-hhi(v0))+(hhi(v1)-hhi(a)))

def load():
    rows=[]
    for entry in json.loads((ROOT/'data/manifest.json').read_text()):
        p=ROOT/entry['file'];b=p.read_bytes()
        assert hashlib.sha256(b).hexdigest()==entry['sha256']
        payload=json.loads(b);assert payload['count']==len(payload['data'])<500
        rows.extend(payload['data'])
    d=pd.DataFrame(rows)
    assert not d.duplicated(['freqCode','period','reporterCode','flowCode','partnerCode','partner2Code','customsCode','motCode','cmdCode']).any()
    return d

def run():
    d=load(); a=d[(d.freqCode=='A')&(d.reporterCode==268)].copy()
    annual=[];quality=[]
    for y,g in a.groupby('refYear'):
        w=g[g.partnerCode==0].iloc[0];p=g[g.partnerCode!=0]
        assert (p.netWgt>0).all() and (p.primaryValue>0).all()
        quality.append(dict(year=int(y),partner_rows=len(p),value_residual=float(p.primaryValue.sum()-w.primaryValue),kg_residual=float(p.netWgt.sum()-w.netWgt),estimated_weights=int(p.isNetWgtEstimated.sum()),qty_net_max_difference=float((p.qty-p.netWgt).abs().max())))
        assert abs(quality[-1]['value_residual'])<0.01 and abs(quality[-1]['kg_residual'])<0.01
        annual.append(dict(year=int(y),value_usd=w.primaryValue,weight_kg=w.netWgt,unit_usd_kg=w.primaryValue/w.netWgt,hhi_value=hhi(p.primaryValue),hhi_weight=hhi(p.netWgt),effective_destinations_value=1/hhi(p.primaryValue),n_destinations=len(p),us_value_share=float(p.loc[p.partnerCode==842,'primaryValue'].sum()/w.primaryValue),turkey_value_share=float(p.loc[p.partnerCode==792,'primaryValue'].sum()/w.primaryValue)))
    annual=pd.DataFrame(annual).set_index('year');annual.to_csv(OUT/'annual.csv');pd.DataFrame(quality).to_csv(OUT/'quality.csv',index=False)
    baseline=[]
    for t in [2024,2025]:
        for b in range(2015,t):
            r=dict(base=b,target=t)
            for k in ['value_usd','weight_kg','unit_usd_kg','hhi_value','hhi_weight']:r[k+'_change_pct']=100*(annual.loc[t,k]/annual.loc[b,k]-1)
            baseline.append(r)
    pd.DataFrame(baseline).to_csv(OUT/'baseline_sensitivity.csv',index=False)
    dec=[];routed=[];groups=[]
    for b,t in [(2022,2023),(2022,2024),(2023,2024),(2024,2025),(2022,2025),(2019,2024)]:
        z0=a[(a.refYear==b)&(a.partnerCode!=0)].set_index('partnerCode');z1=a[(a.refYear==t)&(a.partnerCode!=0)].set_index('partnerCode'); codes=sorted(set(z0.index)|set(z1.index))
        c=0.;p=0.;entry=0.;exit=0.
        for code in codes:
            x0=z0.loc[code] if code in z0.index else None;x1=z1.loc[code] if code in z1.index else None
            v0=float(x0.primaryValue) if x0 is not None else 0.;v1=float(x1.primaryValue) if x1 is not None else 0.
            q0=float(x0.netWgt) if x0 is not None else 0.;q1=float(x1.netWgt) if x1 is not None else 0.
            c0=p0=e0=x0v=0.
            if q0 and q1:c0,p0=midpoint(v0,q0,v1,q1);c+=c0;p+=p0
            elif q1:e0=v1;entry+=v1
            elif q0:x0v=-v0;exit-=v0
            routed.append(dict(base=b,target=t,partner=code,name=NAMES.get(code,str(code)),value0=v0,value1=v1,weight0=q0,weight1=q1,value_change=v1-v0,quantity_effect=c0,unit_receipts_effect=p0,entry=e0,exit=x0v))
        aggq,aggp=midpoint(annual.loc[b,'value_usd'],annual.loc[b,'weight_kg'],annual.loc[t,'value_usd'],annual.loc[t,'weight_kg'])
        delta=annual.loc[t,'value_usd']-annual.loc[b,'value_usd']
        assert abs(c+p+entry+exit-delta)<.02
        dec.append(dict(base=b,target=t,delta_value=delta,quantity_effect_common=c,unit_receipts_effect_common=p,entry=entry,exit=exit,aggregate_quantity_effect=aggq,aggregate_unit_receipts_effect=aggp))
        v0=np.array([float(z0.loc[k,'primaryValue']) if k in z0.index else 0 for k in codes]);v1=np.array([float(z1.loc[k,'primaryValue']) if k in z1.index else 0 for k in codes]);mask=[k in [792,842] for k in codes]
        sh=group_shapley(v0,v1,mask);assert abs(sum(sh)-(hhi(v1)-hhi(v0)))<1e-12
        groups.append(dict(base=b,target=t,hhi0=hhi(v0),hhi1=hhi(v1),us_turkey_effect=sh[0],other_effect=sh[1],us_turkey_fraction=sh[0]/sum(sh)))
    pd.DataFrame(dec).to_csv(OUT/'decomposition.csv',index=False);pd.DataFrame(routed).to_csv(OUT/'route_changes.csv',index=False);pd.DataFrame(groups).to_csv(OUT/'hhi_attribution.csv',index=False)
    # Independent reporting system: preserve, never splice U.S. weights into Georgia.
    u=d[(d.freqCode=='A')&(d.reporterCode==842)&(d.partnerCode.isin([0,268]))].copy()
    u[['refYear','partnerCode','qty','netWgt','primaryValue','fobvalue','cifvalue']].to_csv(OUT/'us_mirror_diagnostic.csv',index=False)
    # Monthly checks; no zero imputation for wholly missing reporter-periods.
    m=d[(d.freqCode=='M')&(d.reporterCode==268)]
    checks=[]
    if len(m):
        monthly=m[m.partnerCode==0].copy();monthly['month']=monthly.period.astype(int)
        monthly[['month','primaryValue','netWgt']].to_csv(OUT/'monthly_world.csv',index=False)
        for y,g in monthly.groupby('refYear'):
            checks.append(dict(year=int(y),months=len(g),value_monthly=float(g.primaryValue.sum()),weight_monthly=float(g.netWgt.sum()),value_diff_from_annual=float(g.primaryValue.sum()-annual.loc[y,'value_usd']),weight_diff_from_annual=float(g.netWgt.sum()-annual.loc[y,'weight_kg'])))
        pd.DataFrame(checks).to_csv(OUT/'monthly_annual_check.csv',index=False)
        m[m.partnerCode!=0][['period','partnerCode','primaryValue','netWgt']].to_csv(OUT/'monthly_routes.csv',index=False)
    g=d[d.reporterCode==268]
    diffs=g[(g.qty-g.netWgt).abs()>.01][['freqCode','period','partnerCode','qty','netWgt']]
    diffs.to_csv(OUT/'quantity_field_discrepancies.csv',index=False)
    validation=dict(annual_partner_records=int(len(g[(g.freqCode=='A')&(g.partnerCode!=0)])),monthly_partner_records=int(len(g[(g.freqCode=='M')&(g.partnerCode!=0)])),monthly_world_records=int(len(g[(g.freqCode=='M')&(g.partnerCode==0)])),raw_responses=len(json.loads((ROOT/'data/manifest.json').read_text())),total_raw_records=len(d),annual_max_value_residual_usd=float(max(abs(x['value_residual']) for x in quality)),annual_max_weight_residual_kg=float(max(abs(x['kg_residual']) for x in quality)),annual_monthly_max_value_difference_usd=float(max(abs(x['value_diff_from_annual']) for x in checks)),annual_monthly_max_weight_difference_kg=float(max(abs(x['weight_diff_from_annual']) for x in checks)),quantity_field_discrepant_records=len(diffs))
    (OUT/'validation_summary.json').write_text(json.dumps(validation,indent=2)+'\n')
    sensitivity=[]
    for b,t in [(2022,2024),(2024,2025)]:
        z=dict(base=b,target=t,epsilon=.05)
        for k in ['weight_kg','value_usd']:
            ratio=annual.loc[t,k]/annual.loc[b,k]
            z[k+'_ratio_lower']=float(ratio*.95/1.05);z[k+'_ratio_upper']=float(ratio*1.05/.95)
        ratio=annual.loc[t,'hhi_value']/annual.loc[b,'hhi_value']
        z['hhi_value_ratio_lower']=float(ratio*(.95/1.05)**4);z['hhi_value_ratio_upper']=float(ratio*(1.05/.95)**4)
        sensitivity.append(z)
    pd.DataFrame(sensitivity).to_csv(OUT/'measurement_sensitivity.csv',index=False)
    print(annual.round(5).to_string()); print('\nDECOMPOSITION\n',pd.DataFrame(dec).to_string(index=False));print('\nHHI ATTRIBUTION\n',pd.DataFrame(groups).to_string(index=False));print('\nMONTHLY\n',checks)
    return annual
if __name__=='__main__':run()
