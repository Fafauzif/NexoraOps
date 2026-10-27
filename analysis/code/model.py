"""Nexora v1.0.0. Units: billion annual parcels, IDR/parcel, IDR trillion.
Authored planning model, not an empirical estimate. Run with bundled Python.
"""
from pathlib import Path
import json, time, platform, hashlib
import numpy as np
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
WEIGHTS=np.array([.35,.30,.25,.10])
SHARES=np.array([.8,.6,.16,0.])
AVG_I=np.array([7000.,8500.,12750.,18000.])
PRICE_E=np.array([10000.,11000.,12000.,14600.])
CAP=np.array([.64,.43,.13,.02])
Q0=2*WEIGHTS*SHARES
FIXED=Q0*2000/1000
OT=np.array([3500.,4500.,6500.,8000.])
MIX=np.array([3500.,6000.,10000.,14000.])
TYPES=['dense_urban','suburban','regional','difficult']
SEED_SCREEN=20261027
SEED_HOLDOUT=20261101
HORIZON=5
PACKAGES={
 'current':dict(soft=0.,physical=0.,add=[0,0,0,0],fixed=0.,recurring=0.,transition=0.,ramp=[1]*7,eff=False),
 'rules':dict(soft=0.,physical=0.,add=[0,0,0,0],fixed=0.,recurring=.008,transition=.015,ramp=[.85,1,1,1,1,1,1],eff=False),
 'software':dict(soft=.18,physical=0.,add=[0,0,0,0],fixed=0.,recurring=.045,transition=.06,ramp=[.55,.9,1,1,1,1,1],eff=True),
 'targeted':dict(soft=.18,physical=.85,add=[.08,.08,.03,0],fixed=.15,recurring=.045+.85*.03,transition=.10,ramp=[.35,.8,1,1,1,1,1],eff=True),
 'large':dict(soft=.18,physical=3.6,add=[.22,.22,.12,.04],fixed=.55,recurring=.045+3.6*.03,transition=.20,ramp=[.15,.6,.9,1,1,1,1],eff=True),
}

def write_json(path,obj):
 path=ROOT/path; path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,indent=2,allow_nan=False,default=lambda x:x.tolist() if hasattr(x,'tolist') else float(x)))

def central(n=1,years=5):
 return dict(demand=np.ones((n,years)),travel=np.ones((n,years)),input_cost=np.ones((n,years)),external=np.ones((n,years)),capacity=np.ones((n,years)),eff=np.full((n,1),.03),adoption=np.ones((n,1)),inflation=np.full((n,1),.025),overrun=np.ones((n,1)),daily_surge=np.ones((n,years)))

def draw(n,seed,years=5):
 """PCG64; export draws for cross-language parity. Persistent vs annual shocks separate."""
 r=np.random.default_rng(seed)
 # independent identities retained for every policy. Parameter uncertainty persists by world.
 g=r.normal(size=(n,1)); traffic=r.normal(size=(n,years)); c=r.normal(size=(n,1))
 demand=np.clip(np.exp(.06*g+.03*r.normal(size=(n,years))-.5*(.06**2+.03**2)),.70,1.40)
 travel=np.clip(np.exp(.08*g+.12*traffic-.5*(.08**2+.12**2)),.65,1.9)
 input_cost=np.clip(np.exp(.05*c+.035*r.normal(size=(n,years))-.5*(.05**2+.035**2)),.8,1.3)
 external=np.clip(np.exp(.025*c+.04*r.normal(size=(n,years))-.5*(.025**2+.04**2)),.8,1.3)
 capacity=np.clip(1-.035*np.maximum(travel-1,0)+.02*r.normal(size=(n,years)),.80,1.08)
 return dict(demand=demand,travel=travel,input_cost=input_cost,external=external,capacity=capacity,
  eff=r.triangular(0,.03,.07,(n,1)),adoption=r.triangular(.5,.9,1.05,(n,1)),
  inflation=r.triangular(0,.025,.06,(n,1)),overrun=r.triangular(.9,1,1.5,(n,1)),
  daily_surge=np.clip(np.exp(.08*r.normal(size=(n,years))-.5*.08**2),.75,1.40))

def penalty(q,k,ot=OT):
 return ot/2*np.maximum(q-.85*k,0)**2/(.15*k)/1000

def market_inputs(weights):
 weights=np.asarray(weights)
 scale=brentq(lambda a:np.dot(weights,np.minimum(SHARES*a,.999))-.5,.1,5)
 shares=np.minimum(SHARES*scale,.999)
 q0=2*weights*shares
 avg=AVG_I*(8000/(np.dot(q0,AVG_I)/q0.sum()))
 eq=2*weights-q0
 ext=PRICE_E*(12000/(np.dot(eq,PRICE_E)/eq.sum()))
 cap=np.maximum(CAP*weights/WEIGHTS,q0/.95)
 return shares,q0,avg,ext,cap

def calibration(weights=WEIGHTS,fixed_share=.25):
 shares,q0,avg,ext,cap=market_inputs(weights)
 f=q0*avg*fixed_share/1000
 # Remove baseline overtime from intercept, so the historical calibration includes it once.
 v=avg*(1-fixed_share)-np.divide(penalty(q0,cap)*1000,q0,out=np.zeros(4),where=q0>0)
 return q0,f,v

def operating(world,package,target=.60,buffer=.94,axis=1.,weights=WEIGHTS,fixed_share=.25,mix_mult=1.,eff_mult=1.,external_reprice=1.,capacity_mult=1.,ramp_override=None,allocation_style='adaptive'):
 w=world; n,y=w['demand'].shape; p=PACKAGES[package]
 weights=np.asarray(weights); shares,q0,avg,ext_base,base_cap=market_inputs(weights); q0,fixed,v=calibration(weights,fixed_share)
 d=(2*axis*w['demand'])[...,None]*weights
 idx=(1+w['inflation'])**np.arange(1,y+1)[None,:]
 # 45% of avoidable costs respond to traffic; these are assumptions, not observed coefficients.
 variable=v[None,None,:]*w['input_cost'][...,None]*(.55+.45*w['travel'][...,None])
 ext=ext_base[None,None,:]*w['external'][...,None]*external_reprice
 k0=base_cap[None,None,:]*w['capacity'][...,None]*capacity_mult
 qc=np.minimum(d*shares,k0)
 if package=='current':
  q=qc; k=k0; ve=variable; mix=MIX*mix_mult
 else:
  ramp=np.asarray((ramp_override or p['ramp'])[:y])[None,:]*np.minimum(w['adoption'],1)
  if ramp_override is not None: ramp=np.broadcast_to(np.array(ramp_override[:y])[None,:],(n,y))
  eff=np.clip(w['eff']*eff_mult,0,.15) if p['eff'] else np.zeros((n,1))
  k=k0+(np.array(p['add'])[None,None,:]*ramp[...,None])
  k=k*(1+(.02*eff/.03)[...,None]*ramp[...,None])
  ve=variable*(1-.65*eff[...,None]*ramp[...,None])
  mix=MIX*mix_mult
  # 24 tranches/type, ranked by midpoint avoidable saving; no hard-coded internal-share optimum.
  maximum=np.minimum(d,k*buffer)
  levels=(np.arange(24)+.5)/24
  mid=maximum[...,None]*levels
  mc=ve[...,None]+OT[None,None,:,None]*np.maximum(mid-.85*k[...,None],0)/(.15*k[...,None])
  mc+=mix[None,None,:,None]*np.maximum(mid-q0[None,None,:,None],0)/np.maximum(d-q0,1e-6)[...,None]
  saving=(ext[...,None]-mc).reshape(n,y,96)
  if allocation_style=='fixed_priority':
   # Rank tranches using central rates/traffic/productivity, rather than each sampled world's costs.
   cmid=np.minimum(2*weights,base_cap*buffer)[:,None]*levels
   cve=v*(1-.65*.03) if p['eff'] else v
   cmc=cve[:,None]+OT[:,None]*np.maximum(cmid-.85*base_cap[:,None],0)/(.15*base_cap[:,None])
   cmc+=mix[:,None]*np.maximum(cmid-q0[:,None],0)/np.maximum(2*weights-q0,1e-6)[:,None]
   saving=np.broadcast_to((ext_base[:,None]-cmc).reshape(1,1,96),(n,y,96))
  chunk=np.broadcast_to(maximum[...,None]/24,(n,y,4,24)).reshape(n,y,96)
  order=np.argsort(-saving,axis=-1,kind='stable')
  sav=np.take_along_axis(saving,order,-1); chunks=np.take_along_axis(chunk,order,-1)
  before=np.cumsum(chunks,-1)-chunks
  budget=(d.sum(-1)*target)[...,None]
  accepted=np.minimum(chunks,np.maximum(budget-before,0))*(sav>0)
  # Zero-value tranches cannot consume budget ahead of positive-value tranches (sorting guarantees).
  original=np.zeros_like(accepted); np.put_along_axis(original,order,accepted,-1)
  qo=original.reshape(n,y,4,24).sum(-1)
  q=qc+ramp[...,None]*(qo-qc)
  q=np.minimum(q,np.minimum(k,d))
 # Actual external availability is finite, even when contracts are assumed reservable.
 ext_capacity=(2*weights*(1-shares)*1.65+np.array([.04,.04,.03,.015]))[None,None,:]
 ext_capacity=ext_capacity*np.clip(1-.10*np.maximum(w['travel']-1,0),.7,1)[...,None]
 e=np.minimum(np.maximum(d-q,0),ext_capacity)
 unserved=np.maximum(d-q-e,0)
 # Deferred demand incurs emergency handling cost, no invented lost GMV or retention cost.
 deferred_cost=unserved.sum(-1)*18000/1000
 mix_cost=mix/2*np.maximum(q-q0,0)**2/np.maximum(d-q0,1e-6)/1000
 core=(fixed.sum()+(ve*q/1000+penalty(q,k)+mix_cost+ext*e/1000).sum(-1)+deferred_cost)*idx
 if package!='current':
  core+=(p['fixed']*ramp+p['recurring'])*idx
 # Peak-day feasibility uses a separate daily disturbance; annual parcels remain conserved above.
 peak_internal=q*w['daily_surge'][...,None]
 peak_ext=e*w['daily_surge'][...,None]
 peak_over=np.maximum(peak_internal-k,0).sum(-1)+np.maximum(peak_ext-ext_capacity,0).sum(-1)
 total=d.sum(-1)
 util=q/k
 planning_late=(np.maximum(util-.90,0)/.10*.06*q).sum(-1)
 feasible_fraction=np.clip(1-(unserved.sum(-1)+peak_over+planning_late)/total,0,1)
 violation=(unserved.sum(-1)/total>.005)|(feasible_fraction<.95)
 return dict(cost=core,q=q,e=e,d=d,k=k,unserved=unserved,share=q.sum(-1)/total,util=util,
  service=feasible_fraction,violation=violation,idx=idx,variable=ve,external_price=ext,peak_over=peak_over)

def finances(op,cf,package,w,rate=.14,tax=.22,cap_mult=1.,nonlog_drift=0.,salvage_factor=.35):
 p=PACKAGES[package]; n,y=op['cost'].shape
 year=np.arange(1,y+1)[None,:]
 over=w['overrun']*cap_mult
 soft=p['soft']*over; phys=p['physical']*over
 cap=soft+phys; wc=.01*soft+.02*phys
 # Economic lives: software4, vehicles5, sortation8, leasehold10, 50% first-year convention.
 dep=np.zeros((n,y)); replacement=np.zeros((n,y))
 assets=[(soft,4,1),(phys*.30,5,1),(phys*.40,8,1),(phys*.30,10,1)]
 if y>=5:
  refresh=.5*soft; replacement[:,4]=refresh[:,0]; assets.append((refresh,4,5))
 if y>=6:
  replvehicle=phys*.30; replacement[:,5]+=replvehicle[:,0]; assets.append((replvehicle,5,6))
 book=np.zeros((n,1))
 for amount,life,start in assets:
  factors=np.maximum(np.minimum(year-start+.5,life)-np.maximum(np.minimum(year-start-.5,life),0),0)/life
  dep+=amount*factors
  book+=amount*(1-factors.sum(-1,keepdims=True))
 # Software has no salvage. Exclude original and replacement software carrying amount.
 physical_book=np.zeros((n,1))
 for amount,life,start in [a for a in assets if a[1]!=4]:
  used=np.clip(y-start+.5,0,life)/life
  physical_book+=amount*(1-used)
 salvage=salvage_factor*physical_book
 transition=np.zeros((n,y)); transition[:,0]=p['transition']*over[:,0]
 benefit=cf['cost']-op['cost']
 ebitda=benefit-transition
 ebit=ebitda-dep
 taxes=np.maximum(ebit,0)*tax
 cash=ebitda-taxes-replacement
 cash[:,-1]+=salvage[:,0]+wc[:,0]
 flows=np.column_stack([-cap[:,0]-wc[:,0],cash])
 npv=(flows/(1+rate)**np.arange(y+1)[None,:]).sum(-1)
 cfprofit=5-(cf['cost']-20)+year*nonlog_drift
 profit=cfprofit+ebit
 growth=np.diff(np.column_stack([np.full(n,5.),profit]),axis=1)
 return dict(npv=npv,benefit=benefit,ebitda=ebitda,ebit=ebit,dep=dep,taxes=taxes,flows=flows,
  cfprofit=cfprofit,profit=profit,growth_amount=growth,growth_pass=np.all(growth>1e-10,axis=1),
  capex=cap[:,0],wc=wc[:,0],replacement=replacement,salvage=salvage[:,0],transition=transition)

def irr(flows):
 if not (np.any(flows<0) and np.any(flows>0)): return None
 signs=np.sign(flows[np.abs(flows)>1e-12])
 if np.sum(signs[1:]!=signs[:-1])!=1:return None
 try:return float(brentq(lambda r:sum(flows/(1+r)**np.arange(len(flows))),-.95,100))
 except ValueError:return None

def payback(flows,rate=0):
 cum=flows[0]
 if cum>=0:return 0.
 for y,f in enumerate(flows[1:],1):
  f=f/(1+rate)**y
  if cum+f>=0 and f>0:return float(y-1-cum/f)
  cum+=f
 return None

def summary(policy,op,fin):
 a=fin['npv']; ben=fin['ebit'][:,-1]
 return dict(**policy,expected_npv_tn=float(a.mean()),median_npv_tn=float(np.median(a)),p10_npv_tn=float(np.percentile(a,10)),
  p90_npv_tn=float(np.percentile(a,90)),prob_positive_npv=float(np.mean(a>0)),npv_mcse=float(a.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else 0.,
  expected_y1_ebit_tn=float(fin['ebit'][:,0].mean()),expected_y5_ebit_tn=float(ben.mean()),
  realised_internal_share=float(op['share'][:,-1].mean()),mean_planning_feasibility=float(op['service'].mean()),
  service_violation_world_fraction=float(np.any(op['violation'],axis=1).mean()),
  mean_unserved_parcels_annual=float((op['unserved'].sum(-1)*1e9).mean()),
  prob_positive_growth_all_years=float(fin['growth_pass'].mean()),initial_capex_tn=float(fin['capex'].mean()),
  mean_cost_per_parcel_y5=float((op['cost'][:,-1]/op['d'][:,-1].sum(-1)*1000).mean()))

def policy_list():
 policies=[dict(policy_id='P_CURRENT',package='current',target=.5,buffer=1.)]
 for package in ['rules','software','targeted','large']:
  for target in np.arange(.45,.951,.05):
   for buffer in [.88,.94,1.]:
    policies.append(dict(policy_id=f'P_{package.upper()}_{round(target*100):02}_{round(buffer*100)}',package=package,target=round(float(target),2),buffer=buffer))
 return policies

def run():
 start=time.perf_counter(); policies=policy_list()
 # Pilot/convergence execution, not a promised run count.
 pilot=[]
 for n in [250,500,1000]:
  w=draw(n,SEED_SCREEN); cf=operating(w,'current'); op=operating(w,'software',.65,.94)
  f=finances(op,cf,'software',w); pilot.append(dict(n=n,mean=float(f['npv'].mean()),se=float(f['npv'].std()/np.sqrt(n))))
 w=draw(1000,SEED_SCREEN); cf=operating(w,'current'); screen=[]
 for p in policies:
  op=operating(w,p['package'],p['target'],p['buffer']); f=finances(op,cf,p['package'],w)
  screen.append(summary(p,op,f))
 # One winner per family plus top five expected-NPV candidates; de-duplicate.
 selected={s['policy_id']:s for s in sorted(screen,key=lambda a:a['expected_npv_tn'],reverse=True)[:5]}
 for package in PACKAGES:
  a=max((s for s in screen if s['package']==package),key=lambda a:a['expected_npv_tn']);selected[a['policy_id']]=a
  feasible=[s for s in screen if s['package']==package and s['service_violation_world_fraction']<=.10]
  if feasible:
   a=max(feasible,key=lambda a:(a['expected_npv_tn']+a['p10_npv_tn'])/2);selected[a['policy_id']]=a
  reference=screen[0]
  no_worse=[s for s in screen if s['package']==package and s['mean_planning_feasibility']>=reference['mean_planning_feasibility'] and s['service_violation_world_fraction']<=reference['service_violation_world_fraction']]
  if no_worse:
   a=max(no_worse,key=lambda a:(a['expected_npv_tn']+a['p10_npv_tn'])/2);selected[a['policy_id']]=a
 selected=list(selected.values())
 held=draw(10000,SEED_HOLDOUT); cfh=operating(held,'current'); final=[]; held_npvs={}
 for ps in selected:
  p={k:ps[k] for k in ['policy_id','package','target','buffer']}
  op=operating(held,p['package'],p['target'],p['buffer']); f=finances(op,cfh,p['package'],held)
  s=summary(p,op,f); final.append(s); held_npvs[p['policy_id']]=f['npv']
 # Risk preference: E[NPV] - 0.5*(E[NPV]-p10); service violation limit 10% worlds.
 reference=next(s for s in final if s['package']=='current')
 acceptable=[s for s in final if s['service_violation_world_fraction']<=min(.10,reference['service_violation_world_fraction']) and s['mean_planning_feasibility']>=reference['mean_planning_feasibility']]
 if not acceptable: acceptable=[reference]
 for s in final:s['risk_score_tn']=s['expected_npv_tn']-.5*(s['expected_npv_tn']-s['p10_npv_tn'])
 recommended=max(acceptable,key=lambda s:s['risk_score_tn'])
 maxreturn=max(final,key=lambda s:s['expected_npv_tn'])
 ranking={s['policy_id']:float(np.mean(np.argmax(np.column_stack([held_npvs[f['policy_id']] for f in final]),axis=1)==i)) for i,s in enumerate(final)}
 central_results={}
 for s in final:
  p={k:s[k] for k in ['policy_id','package','target','buffer']}; z=central(); cf=operating(z,'current');op=operating(z,p['package'],p['target'],p['buffer']); f=finances(op,cf,p['package'],z)
  flows=f['flows'][0]; cum=np.cumsum(flows)
  central_results[p['policy_id']]=dict(policy=p,operating={k:v[0].tolist() for k,v in op.items()},financial={k:v[0].tolist() if hasattr(v[0],'tolist') else float(v[0]) for k,v in f.items()},
   irr=irr(flows),payback=payback(flows),discounted_payback=payback(flows,.14),peak_funding_tn=float(max(0,-cum.min())))
 # Numeric heatmap: held-out worlds (1000 subset), demand axis separate from random demand.
 cells=[]
 for target in np.arange(.45,.951,.05):
  for axis in [.8,.9,1.,1.1,1.2,1.4]:
   ws={k:v[:1000] for k,v in held.items()}; cf=operating(ws,'current',axis=axis)
   op=operating(ws,recommended['package'],float(target),recommended['buffer'],axis=axis);f=finances(op,cf,recommended['package'],ws)
   realised=float(op['share'][:,-1].mean());v=float(op['violation'][:,-1].mean())
   reasons=[]
   if realised+0.005<float(target):reasons.append('target_not_economic_or_capacity_limited')
   if v>.10:reasons.append('service_risk_above_10pct_worlds')
   cells.append(dict(cell_id=f'H_{round(target*100)}_{round(axis*100)}',target_share=round(float(target),2),demand_axis=axis,package=recommended['package'],expected_y5_ebit_tn=float(f['ebit'][:,-1].mean()),expected_npv_tn=float(f['npv'].mean()),realised_internal_share=realised,service_violation_probability=v,feasible=len(reasons)==0,reasons=reasons,worlds=1000))
 # Stress same central shocks for family winners, including deliberate unfavourable cases.
 stresses=[]
 stressdefs={
  'campaign_surge':dict(demand=1.35,daily_surge=1.25),
  'hub_capacity_loss':dict(capacity=.70),
  'corridor_disruption':dict(travel=1.60),
  'weak_productivity':dict(eff=0.,adoption=.50),
  'implementation_overrun':dict(overrun=1.60,adoption=.65),
  'carrier_price_up':dict(external=1.20),
  'carrier_price_cut':dict(external=.80),
  'combined_downside':dict(eff=0.,adoption=.5,overrun=1.6,external=.85,capacity=.85),
  'upside_execution':dict(eff=.06,adoption=1.0,external=1.08,overrun=.95),
 }
 for name,edits in stressdefs.items():
  z=central()
  for k,val in edits.items():z[k][:]=val
  cf=operating(z,'current')
  for s in final:
   op=operating(z,s['package'],s['target'],s['buffer']);f=finances(op,cf,s['package'],z)
   stresses.append(dict(scenario_id='S_'+name.upper(),policy_id=s['policy_id'],npv_tn=float(f['npv'][0]),y1_ebit_tn=float(f['ebit'][0,0]),y5_ebit_tn=float(f['ebit'][0,-1]),service_min=float(op['service'].min()),growth_pass=bool(f['growth_pass'][0])))
 # Structural comparison, using fresh held-out 2000 matched worlds; recalibrate anchors for alternative weights.
 structural=[]
 variants=[('central',{}),('low_fixed',dict(fixed_share=.10)),('high_fixed',dict(fixed_share=.40)),('flat_mix',dict(mix_mult=0.)),('steep_mix',dict(mix_mult=1.8)),('urban_heavy',dict(weights=np.array([.45,.25,.20,.10]))),('regional_heavy',dict(weights=np.array([.25,.25,.35,.15]))),('fixed_priority',dict(allocation_style='fixed_priority'))]
 for name,kw in variants:
  ws={k:v[:2000] for k,v in held.items()}
  cf=operating(ws,'current',**kw)
  for s in final:
   op=operating(ws,s['package'],s['target'],s['buffer'],**kw);f=finances(op,cf,s['package'],ws)
   structural.append(dict(variant=name,policy_id=s['policy_id'],expected_npv_tn=float(f['npv'].mean()),p10_npv_tn=float(np.percentile(f['npv'],10)),baseline_internal_share=float(np.dot(kw.get('weights',WEIGHTS),market_inputs(kw.get('weights',WEIGHTS))[0]))))
 # Tornado and economics thresholds for recommended evaluated policy.
 sensitivity=[]; s=recommended
 for name,key,low,high in [('software productivity','eff',0,.07),('carrier price','external',.85,1.15),('travel factor','travel',.8,1.5),('implementation multiplier','overrun',.9,1.6),('capacity availability','capacity',.8,1.05),('inflation','inflation',0,.06)]:
  vals=[]
  for val in [low,high]:
   z=central();z[key][:]=val;cf=operating(z,'current');op=operating(z,s['package'],s['target'],s['buffer']);f=finances(op,cf,s['package'],z);vals.append(float(f['npv'][0]))
  sensitivity.append(dict(driver=name,low=low,high=high,npv_at_low=vals[0],npv_at_high=vals[1]))
 horizons=[]
 for years in [3,5,7]:
  z=central(years=years);cf=operating(z,'current');op=operating(z,s['package'],s['target'],s['buffer'])
  for rate in [.11,.14,.18]:
   f=finances(op,cf,s['package'],z,rate=rate);horizons.append(dict(years=years,discount_rate=rate,npv_tn=float(f['npv'][0]),irr=irr(f['flows'][0]),growth_pass=bool(f['growth_pass'][0])))
 z=central();cf=operating(z,'current');op=operating(z,s['package'],s['target'],s['buffer'])
 def npvcap(m):return float(finances(op,cf,s['package'],z,cap_mult=m)['npv'][0])
 breakeven=None
 if PACKAGES[s['package']]['soft']+PACKAGES[s['package']]['physical']>0 and npvcap(0)*npvcap(30)<0:
  breakeven=brentq(npvcap,0,30)*(PACKAGES[s['package']]['soft']+PACKAGES[s['package']]['physical'])
 f=finances(op,cf,s['package'],z)
 # Minimum constant annual non-logistics EBIT increase needed for positive YoY growth.
 required=max(0,float(-f['growth_amount'].min()+1e-6))
 # Risk preference thresholds, do not resample or reselect on holdout outcomes in reporting.
 risk_alternatives=[]
 for penalty_weight in [0,.25,.5,1.]:
  pick=max(acceptable,key=lambda a:a['expected_npv_tn']-penalty_weight*(a['expected_npv_tn']-a['p10_npv_tn']))
  risk_alternatives.append(dict(risk_penalty=penalty_weight,policy_id=pick['policy_id']))
 for limit in [.05,.10,.20]:
  possible=[s for s in final if s['service_violation_world_fraction']<=limit]
  if possible:
   pick=max(possible,key=lambda a:a['risk_score_tn']);risk_alternatives.append(dict(absolute_service_violation_limit=limit,policy_id=pick['policy_id']))
 # Save all draws with column identities; JSON small subset for browser, compressed archive full.
 np.savez_compressed(ROOT/'results/worlds_holdout_10000.npz',**held)
 np.savez_compressed(ROOT/'results/finalist_npvs.npz',**held_npvs)
 write_json('data/worlds_reference.json',dict(schema_version='1.0.0',seed=SEED_HOLDOUT,worlds=[dict(world_id=f'W_{i:05}',**{k:v[i].tolist() for k,v in held.items()}) for i in range(200)]))
 write_json('data/policies.json',dict(schema_version='1.0.0',screening=screen,finalists=final,recommended_candidate=s['policy_id'],maximum_expected_return=maxreturn['policy_id'],recommendation_eligible_full_rollout=False))
 write_json('data/heatmap.json',dict(schema_version='1.0.0',cells=cells))
 write_json('data/selected_outcomes.json',dict(schema_version='1.0.0',outcomes=central_results))
 write_json('results/analysis.json',dict(screening_candidates=len(policies),screen_worlds=1000,finalists=len(final),heldout_worlds=10000,screen_seed=SEED_SCREEN,heldout_seed=SEED_HOLDOUT,pilot=pilot,
  recommended=s,maxreturn=maxreturn,ranking_win_fraction=ranking,stresses=stresses,structural=structural,sensitivity=sensitivity,horizons=horizons,break_even_initial_capex_tn=breakeven,minimum_annual_nonlogistics_ebit_increase_tn=required,risk_preferences=risk_alternatives,runtime_seconds=time.perf_counter()-start))
 write_json('data/config.json',dict(schema_version='1.0.0',status='hypothetical_planning_model',case_source='Supplied handoff extract; original casebook PDF not inspected',base_year=2025,annual_parcels=2000000000,group_operating_profit_idr=5e12,gmv_idr=600e12,revenue_idr=60e12,marketing_idr=24e12,weights=WEIGHTS,baseline_internal_shares=SHARES,internal_costs=AVG_I,external_costs=PRICE_E,capacity_bn=CAP,packages=PACKAGES,financial=dict(horizon=5,discount_rate=.14,tax_rate=.22,inflation=.025,nonlogistics_drift_tn=0.,salvage_book_recovery=.35),controls=dict(target_internal_share=[.45,.95,.05],demand_axis=[.8,1.4,.1],buffer=[.88,1,.06]),national_market_types=TYPES))
 print(json.dumps(dict(candidates=len(policies),finalists=len(final),recommended=s,maxreturn=maxreturn,required_nonlog_drift=required,runtime_seconds=time.perf_counter()-start),indent=2))

if __name__=='__main__':run()
