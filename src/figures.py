from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
R=Path(__file__).resolve().parents[1];D=R/'data/derived';F=R/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#283846','text.color':'#283846','axes.edgecolor':'#8c9aa5','savefig.bbox':'tight','pdf.fonttype':42,'ps.fonttype':42})
C=['#006d77','#d17a22','#375a9e','#9b4966','#7e8d53','#a2adb5']
def save(fig,name):
 fig.savefig(F/(name+'.pdf'));fig.savefig(F/(name+'.png'),dpi=180);plt.close(fig)
a=pd.read_csv(D/'annual.csv').set_index('year'); years=a.index.to_numpy()
fig,ax=plt.subplots(1,2,figsize=(10,3.8))
for k,l,c in [('weight_kg','Export weight',C[0]),('value_usd','Export receipts',C[1])]:ax[0].plot(years,a[k]/a.loc[2022,k]*100,marker='o',lw=2,color=c,label=l)
ax[0].axhline(100,color='#aaaaaa',lw=.7,ls='--');ax[0].set(ylabel='Index (2022 = 100)',title='(a) Physical and monetary recovery');ax[0].legend(frameon=False,fontsize=9)
ax[1].plot(years,a.unit_usd_kg,color=C[2],marker='o',lw=2);ax[1].set(ylabel='Current USD per kg',title='(b) Aggregate unit export receipts')
for x in ax:x.set_xticks(years[::2]);x.grid(axis='y',alpha=.2);x.set_xlabel('Calendar year')
fig.tight_layout(w_pad=3);save(fig,'01_recovery')
# Destination structure using fixed classes, never double count World.
rows=[]
import json
for y in years:
 for x in json.loads((R/f'data/raw/A_{y}_268_X.json').read_text())['data']:
  if x['partnerCode']:rows.append(x)
r=pd.DataFrame(rows)
groups=[(842,'United States',C[2]),(643,'Russia',C[3]),(792,'Türkiye',C[1]),(380,'Italy',C[0]),(-1,'Other destinations',C[5])]
fig,ax=plt.subplots(2,1,figsize=(10,6),sharex=True)
for i,(k,unit) in enumerate([('primaryValue','Export receipts (million USD)'),('netWgt','Export weight (thousand tonnes)')]):
 bottom=np.zeros(len(years))
 for code,label,col in groups:
  mask=(~r.partnerCode.isin([842,643,792,380])) if code==-1 else (r.partnerCode==code)
  v=r[mask].groupby('refYear')[k].sum().reindex(years,fill_value=0).to_numpy()/1e6
  ax[i].bar(years,v,bottom=bottom,color=col,label=label,width=.7);bottom+=v
 ax[i].set_ylabel(unit);ax[i].grid(axis='y',alpha=.2);ax[i].set_axisbelow(True)
ax[0].legend(ncol=3,frameon=False,fontsize=9,loc='upper left');ax[1].set_xticks(years);ax[1].set_xlabel('Calendar year');fig.tight_layout();save(fig,'02_destinations')
fig,ax=plt.subplots(1,2,figsize=(10,3.7))
ax[0].plot(years,a.hhi_value,marker='o',color=C[1],label='Receipts shares');ax[0].plot(years,a.hhi_weight,marker='s',color=C[0],label='Weight shares');ax[0].set(ylabel='Herfindahl-Hirschman index',title='(a) Concentration');ax[0].legend(frameon=False)
ax[1].plot(years,a.effective_destinations_value,marker='o',color=C[2],label='Effective destinations (1/HHI)');ax[1].set(ylabel='Effective equally sized destinations',title='(b) Economic breadth');ax[1].set_ylim(0,11)
for x in ax:x.set_xticks(years[::2]);x.set_xlabel('Calendar year');x.grid(axis='y',alpha=.2)
fig.tight_layout(w_pad=3);save(fig,'03_concentration')
dec=pd.read_csv(D/'decomposition.csv');dec=dec[dec.apply(lambda r:(r.base,r.target) in [(2022,2024),(2023,2024),(2024,2025)],axis=1)]
fig,ax=plt.subplots(figsize=(10,4.2));xx=np.arange(len(dec));width=.18
keys=[('quantity_effect_common','Common routes: weight',C[0]),('unit_receipts_effect_common','Common routes: unit receipts',C[1]),('entry','Entry',C[2]),('exit','Exit',C[3])]
for i,(k,l,c) in enumerate(keys):ax.bar(xx+(i-1.5)*width,dec[k]/1e6,width,label=l,color=c)
ax.scatter(xx,dec.delta_value/1e6,color='#1b2730',marker='D',s=35,label='Total change',zorder=4)
ax.axhline(0,color='#333333',lw=.8);ax.set_xticks(xx,[f'{int(b)} to {int(t)}' for b,t in zip(dec.base,dec.target)]);ax.set_ylabel('Change in export receipts (million USD)');ax.legend(ncol=2,frameon=False,fontsize=9,loc='upper center',bbox_to_anchor=(.5,1.21));ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);fig.tight_layout();save(fig,'04_decomposition')
if (D/'monthly_world.csv').exists():
 m=pd.read_csv(D/'monthly_world.csv');m['date']=pd.to_datetime(m.month.astype(str),format='%Y%m')
 fig,ax=plt.subplots(2,1,figsize=(10,5.3),sharex=True)
 for x,k,l,col in [(ax[0],'primaryValue','Receipts (million USD)',C[1]),(ax[1],'netWgt','Weight (thousand tonnes)',C[0])]:
  x.plot(m.date,m[k]/1e6,lw=1,color=col,alpha=.6);x.plot(m.date,(m[k]/1e6).rolling(3,min_periods=3).mean(),lw=2,color=col,label='Trailing three-month mean');x.set_ylabel(l);x.grid(axis='y',alpha=.2);x.axvline(pd.Timestamp('2023-02-01'),ls=':',color='#666666');x.axvline(pd.Timestamp('2024-11-01'),ls=':',color='#666666')
 ax[0].legend(frameon=False,fontsize=9);ax[0].set_title('Monthly trade records; dotted lines mark documented suspension episodes',fontsize=10);ax[1].set_xlabel('Calendar month');ax[1].set_xlim(pd.Timestamp('2021-01-01'),pd.Timestamp('2025-12-01'));fig.tight_layout();save(fig,'05_monthly')
