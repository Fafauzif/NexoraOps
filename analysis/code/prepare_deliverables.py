"""Create registers, fixtures, exhibits, schema, findings and the continuity pack."""
from pathlib import Path
import json,sys,platform,hashlib,csv,time
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import *
from geography import NODES,EDGES,ZONES,HUBS

def get(path):return json.loads((ROOT/path).read_text())

SOURCES=[
 dict(id='CASE',category='CASE FACT',title='Casebook Preliminary IBSC 2026, transcribed in incoming handoff',date='2026',url=None,access='Incoming Markdown read completely. Original PDF NOT supplied/inspected.',scope='Fictional Nexora, Indonesia; pp.7–12',observation='2bn parcels; 50% internal; Rp8,000/Rp12,000; Rp5tn operating profit; see full brief.',license='User-supplied extract; original copyright retained.'),
 dict(id='SRC_GEOAI',category='EXTERNAL OBSERVATION',title='opengeos. geoai-skills',date='main inspected 2026-10-27; commit not retrievable',url='https://github.com/opengeos/geoai-skills',access='README and overture-data instructions inspected through research service; raw endpoint403; plugin NOT executed.',scope='Claude Code plugin using geoai-py',observation='Python3.10+, geoai-py and optional extras; mapped features before object detection.',license='MIT for repository code.'),
 dict(id='SRC_OVERTURE',category='EXTERNAL OBSERVATION',title='Overture Maps Foundation. Transportation Guide',date='2026-10-21.0 release shown in documentation',url='https://docs.overturemaps.org/guides/transportation/',access='Documentation inspected; NO Overture dataset downloaded.',scope='Global segment/connector schema, access and direction rules',observation='Topology uses connectors; conditional restrictions cannot be inferred from a line crossing.',license='Dataset-specific attribution/licensing; documentation is not a data acquisition.'),
 dict(id='SRC_BPJT',category='EXTERNAL OBSERVATION',title='BPJT. Dirgahayu Kota Jakarta Ke-496, ini dia beragam jalan tol yang ada di Jakarta',date='2023-06-22',url='https://bpjt.pu.go.id/dirgahayu-kota-jakarta-ke-496-ini-dia-beragam-jalan-tol-yang-ada-di-jakarta/',access='Page text inspected through research service.',scope='Greater Jakarta toll-road concession lengths, km; NOT street geometry or traffic',observation='Jakarta–Tangerang33; CTC23.5; eastern inner ring27.05; W2 North7.87; JORR South14.25; Pondok Aren5.55; Becakayu15.28; Desari12.1.',license='Government factual attributes attributed; original page not redistributed wholesale.'),
 dict(id='SRC_KEPPRES',category='EXTERNAL OBSERVATION',title='Republic of Indonesia. Keputusan Presiden Nomor38 Tahun1981',date='1981-08-15',url='https://bphn.go.id/data/documents/81kp038.pdf',access='Research service PDF text inspected, Appendix p.3; no local PDF acquired.',scope='Historical Cawang–Tomang route,16km',observation='Historical alignment; current equivalence is an explicit assumption.',license='Indonesian legal text; source attributed.'),
 dict(id='SRC_BPS_DKI',category='EXTERNAL OBSERVATION',title='BPS DKI Jakarta. Population by regency/municipality,2025',date='2025 table',url='https://jakarta.bps.go.id/en/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMyMzMTAw/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-dki-jakarta.html?year=2025',access='Search-index table observations only; direct page403.',scope='Projected resident population, persons; not customers/orders',observation='East3,085,058; West2,487,199; South2,219,220. Used as broad catchment proxies.',license='BPS attribution; no boundaries/raster downloaded.'),
 dict(id='SRC_BPS_JABAR',category='EXTERNAL OBSERVATION',title='BPS Jawa Barat. Population projections by sex and regency/municipality',date='2025 table',url='https://jabar.bps.go.id/id/statistics-table/2/OTY3IzI%3D/proyeksi-penduduk-di-provinsi-jawa-barat-menurut-jenis-kelamin-dan-kabupaten-kota.html',access='Search-index observations only; direct page403.',scope='Projected resident population, persons',observation='Depok2,167,961; Bekasi city approximately2,648,300. City and regency not combined.',license='BPS attribution.'),
 dict(id='SRC_DJP',category='EXTERNAL OBSERVATION',title='Direktorat Jenderal Pajak. Income Tax Calculation Mechanism Entity',date='Current page retrieved2026-10-27',url='https://www.pajak.go.id/id/node/80250',access='Official page inspected.',scope='Indonesia corporate income tax; company-specific relief unknown',observation='General corporate rate22%; listed-company19% is conditional and NOT assumed.',license='Source attributed; model tax treatment remains an assumption.'),
 dict(id='SRC_BI',category='EXTERNAL OBSERVATION',title='Bank Indonesia. BI-Rate tetap5,75%: memperkuat stabilitas, mendorong pertumbuhan ekonomi',date='2026-10-21',url='https://www.bi.go.id/id/publikasi/ruang-media/news-release/Pages/sp_2823326.aspx',access='Official current release verified through both research engines.',scope='IDR policy rate and inflation target',observation='BI-Rate5.75%; inflation target2.5±1% for2026/2027. Policy rate is not project WACC.',license='Official release attributed.'),
 dict(id='SRC_ADB',category='EXTERNAL OBSERVATION',title='Asian Development Bank. AsianBondsOnline: Indonesia Market Watch',date='Close2026-10-23',url='https://asianbondsonline.adb.org/indonesia/',access='Primary market-data portal verified through both research engines.',scope='Indonesia nominal government bond yields',observation='5yr7.245%;10yr7.446%. Risk-premium spread to project discount rate is authored.',license='Factual snapshot with attribution; no proprietary feed redistributed.'),
 dict(id='SRC_JT',category='EXTERNAL OBSERVATION',title='J&T Express. Reports18.5% YoY revenue growth forFY2025',date='2026-04-01 publication; results announced2026-03-30',url='https://www.jtexpress.sg/insights/press-jt-express-reports-18.5-yoy-growth?hs_amp=true',access='Operator page inspected.',scope='SEA multi-country network; own accounting and franchise scope',observation='SEA parcel volume7.66bn, growth67.8%; cost/parcelUS$0.48. Plausibility evidence only; no Nexora coefficient imported.',license='Operator release attributed.'),
 dict(id='SRC_ARCGIS',category='EXTERNAL OBSERVATION',title='DKI Jakarta. Peta Jalan DKI FeatureServer',date='Metadata describes2022 base map',url='https://gis-dpmptsp.jakarta.go.id/arcgis/rest/services/Hosted/Peta_Jalan_DKI/FeatureServer/1',access='Metadata found in search; feature query inaccessible; cloud browser environment denied URL. NO features downloaded.',scope='DKI road linework metadata; outside-city coverage not established',observation='Potential official GIS source; catalogued only.',license='Redistribution terms not verified; no source data redistributed.'),
 dict(id='SRC_OSM',category='EXTERNAL OBSERVATION',title='OpenStreetMap contributors. Overpass/API endpoints',date='Attempt2026-10-27',url='https://overpass-api.de/api/interpreter',access='Direct API403; research-service API queries inaccessible. NO road extract acquired.',scope='Requested Greater Jakarta bounding box and buffer',observation='Optional retrieval/preparation script supplied; not used for headline routing.',license='ODbL1.0 if subsequently downloaded. https://www.openstreetmap.org/copyright')]
for s in SOURCES:s['retrieved']='2026-10-27'

def assumptions():
 rows=[]
 def a(id,name,value,unit,lo,hi,why,correlation='Independent authored parameter unless noted',confidence='Low: no Nexora operational observations',source=None):
  rows.append(dict(id=id,name=name,value=value,unit=unit,low=lo,high=hi,category='ASSUMPTION',reason=why,correlation=correlation,confidence=confidence,source=source,refresh='Rerun model.py for operating/simulation changes; Finance inputs recalculate deterministic finance.'))
 a('A01','National market weights',[.35,.30,.25,.10],'parcel fraction',None,None,'Dense/suburban/regional/difficult; alternative45/25/20/10 and25/25/35/15. Alternative anchors recalibrated.')
 a('A02','Baseline internal share by type',[.8,.6,.16,0.],'parcel fraction',0,1,'Weighted total50%, not observed route mix.')
 a('A03','Internal average cost by type',[7000,8500,12750,18000],'IDR/parcel',None,None,'Calibrates weighted internal average8,000; remote unused historical cell not identified.')
 a('A04','External carrier price by type',[10000,11000,12000,14600],'IDR/parcel',None,None,'Calibrates weighted external average12,000. Contract prices, not public retail tariffs.')
 a('A05','Committed annual internal capacity',[.64,.43,.13,.02],'bn parcels/year',.8,1.08,'Capacity is min(sortation, linehaul, delivery-labour ceilings). Reference fleet/labour ceilings1.05/1.10 times sorter capacity; all expand together. Not observed spare capacity.')
 a('A06','Committed fixed share of historical internal cost',.25,'fraction',.10,.40,'Fixed cash costs persist on rerouting. Variable intercept calibrated after baseline overtime.')
 a('A07','Overtime threshold',.85,'capacity utilisation',.8,.9,'Penalty integral above threshold; daily queue proxy separate.')
 a('A08','Overtime marginal increment at full capacity',[3500,4500,6500,8000],'IDR/parcel',None,None,'Avoidable labour/queue pressure coefficient; not a fitted U-shaped average curve.')
 a('A09','Marginal route-mix gradient',[3500,6000,10000,14000],'IDR/parcel',0,1.8,'Coefficient applied above historical internal volume; structural multipliers0 and1.8 tested.')
 a('A10','Software productivity improvement',.03,'affected-component fraction',0,.07,'Triangular(0,.03,.07); only65% of variable cost affected. J&T establishes possibility, not this effect.',confidence='Low; SRC_JT is context, not a saving estimate',source='SRC_JT')
 a('A11','Traffic-sensitive variable cost share',.45,'fraction',.3,.6,'Labour/vehicle time exposure, handling remainder. Traffic lognormal correlated with demand.')
 a('A12','Affected software cost share',.65,'fraction',.45,.8,'Software changes dispatch/route-related components, not all committed costs.')
 a('A13','Software capacity release at3% productivity',.02,'capacity fraction',0,.0467,'Small planning/leakage recovery; linear with productivity, phased with adoption.')
 a('A14','Software initial capex',.18,'IDR tn',.162,.27,'Rp120bn development plusRp60bn capitalisable integration; estimate, not vendor quote.')
 a('A15','Software recurring opex',.045,'IDR tn/year',.03,.07,'Cloud/support/license/cyber operations allowance; includes optional analytics, no live AI requirement.')
 a('A16','Software transition expense',.06,'IDR tn Year1',.03,.096,'Training, parallel operations and change management; not capitalised.')
 a('A17','Rules recurring/transition costs',[.008,.015],'IDR tn',None,None,'Existing TMS configuration, manual oversight and training; normal current TMS is already present.')
 a('A18','Targeted physical capex',.85,'IDR tn',.765,1.275,'Vehicle/linehaul equipment30%,sortation40%,leasehold upgrades30%; no land purchase. Operations capacity+190m/year.')
 a('A19','Large physical capex',3.6,'IDR tn',3.24,5.4,'Vehicles30%,sortation40%,leasehold30%; +600m/year. Larger size does not ensure value.')
 a('A20','Added annual capacity targeted',[.08,.08,.03,0],'bn parcels/year',None,None,'Shift, fleet, sortation and labour headroom must all be delivered; phase35/80/100%.')
 a('A21','Added annual capacity large',[.22,.22,.12,.04],'bn parcels/year',None,None,'Phase15/60/90/100%; unused/stranded capacity still costs money.')
 a('A22','Expansion fixed cash opex targeted/large',[.15,.55],'IDR tn/year',None,None,'Staffing/leases, scaled by rollout; added variable labour already in parcel cost.')
 a('A23','Physical maintenance',.03,'physical capex fraction/year',.02,.05,'Included once in package recurring cost; not a second cash-flow deduction.')
 a('A24','Software economic life',4,'years',3,5,'Technology refresh risk; half-year first/last depreciation.50% refresh atYear5.')
 a('A25','Physical economic lives',[5,8,10],'years',None,None,'Vehicles5, sortation8, leasehold10; longer engineering life does not imply longer commercial life.')
 a('A26','Evaluation horizon',5,'years',3,7,'Covers primary vehicle/software cycle;3/7 tested with replacements; no perpetuity terminal value.')
 a('A27','Nominal IDR discount rate',.14,'annual rate',.11,.18,'Above official5-year sovereign7.245%; spread2.755–10.755pp authored risk allowance, not observed Nexora WACC.',source='SRC_ADB; SRC_BI')
 a('A28','Corporate tax applied',.22,'rate',.19,.22,'General rate; no unverified listing relief. Incremental losses receive no immediate tax credit; conservative.',source='SRC_DJP')
 a('A29','Nominal logistics cost inflation',.025,'annual rate',0,.06,'Triangular(0,.025,.06); central2.5 uses inflation target as context, not a courier forecast.',source='SRC_BI')
 a('A30','Other net operating-profit change',0.,'IDR tn per elapsed year',-.3,.3,'Bridge assumption, not a claimRp11tn residual is wholly fixed. Includes all non-logistics net effects. Break-even required drift separately calculated.')
 a('A31','Tax-loss treatment',0,'immediate incremental loss credit',0,1,'No immediate credit for negative project EBIT. Group taxable profit and legal offset availability unverified.')
 a('A32','Working capital',[.01,.02],'fraction software/physical capex',0,.04,'Initial deployment support inventory/deposits; released at horizon, no negative working-capital benefit.')
 a('A33','Physical salvage',.35,'fraction remaining book value',0,.60,'Conservative realisation at selected horizon; software zero. No loss tax credit. Salvage sensitivity supplied.')
 a('A34','Implementation overrun',1.,'multiple',.9,1.5,'Triangular(.9,1,1.5), expected1.133; central1.0 differs from mean. Higher-overrun stress1.6.')
 a('A35','Adoption multiplier',.9,'fraction',.5,1.05,'Triangular(.5,.9,1.05), clipped1 for ramp; central perfect planned rollout1.0. Not the mean of draws.')
 a('A36','Reserved external capacity',1.65,'baseline external multiple',None,None,'Plus type absolute buffers40/40/30/15m parcels/year; availability shrinks with travel disruption.')
 a('A37','Service thresholds',[.995,.95,.10],'served/planning-feasible/world-violation limits',None,None,'≥99.5% served;≥95% planning feasibility;≤10% worlds with any annual violation. Candidate must also not worsen matched current mean feasibility or world violation fraction. These are author safeguards, not case SLAs.')
 a('A38','Parameter vs operating uncertainty',None,'see model.py',None,None,'Persistent: inflation, overrun, adoption, efficiency, common demand/cost factors. Annual: travel/input/external/capacity/daily surges. Demand and travel share a normal factor; input and carrier price share cost factor.')
 a('A39','Risk score weight',.5,'E[NPV]-weight*(E-p10)',0,1,'Downside preference;0,.25,.5,1 tested. All strict annual-profit-growth failures remain disqualifying.')
 a('A40','Regional national-volume allocation',.20,'national parcel fraction',.12,.25,'400m/year,1.096m/day on365 days; selected metropolitan corridor markets, not every national parcel. Proxy scale sensitivities provided as controls; no regional saving multiplied nationally.')
 a('A41','Regional demand proxy weights',[.8,.2],'population/activity blend',0,1,'Nine catchment proxies; activity scores authored, not measured merchant counts. Population-only,activity-only,uniform and18-zone comparison executed.')
 a('A42','Regional average corridor speed',30,'km/hour',20,40,'Estimated effective van/truck speed, not legal limit or measured traffic.60/90-minute controls would be estimates.')
 a('A43','Regional time feasibility limit',120,'one-way corridor minutes',90,150,'Two-hour linehaul accessibility filter; not an observed delivery promise. Local access/last mile separately unresolved.')
 a('A44','Regional variable local costs',[2400,35000,1900,.04,3500],'handling;loaded hourly pay;vehicle;failure;retry',None,None,'Local cost=2400+35000/stops_per_hour+1900+.04*3500; failure cost once. Stops/hour9–14 authored.')
 a('A45','Regional linehaul cost',[55000,900,180],'IDR/hour;IDR/km;parcels/load',None,None,'Two-way corridor trip cost allocated over180 parcels; fuel/maintenance900 perkm. Routes not last-mile tours.')
 a('A46','Geography coordinates and polygons',None,'OGC:CRS84',None,None,'Approximate authored terminal coordinates and0.05-degree square zones; no administrative boundaries, buildings or road geometries downloaded.')
 a('A47','National allocator information',None,'adaptive observable operating rates',None,None,'Adaptive ranking uses sampled rates/traffic and capacities as if available for planning; fixed-priority sensitivity tests this optimistic information assumption. This is not a causal forecast.')
 a('A48','Deferred handling penalty',18000,'IDR/deferred parcel',12000,24000,'Accounting proxy for escalation/recovery, no lost GMV. Deferred parcels remain visible and are not counted delivered.')
 return rows

def qa_and_fixtures(a,p):
 checks=[]
 def check(id,passed,detail):checks.append(dict(check_id=id,status='PASS' if passed else 'FAIL',detail=detail))
 w=central();w['inflation'][:]=0;cf=operating(w,'current')
 check('BASE_COST',abs(cf['cost'][0,0]-20)<1e-10,'2025-equivalent delivery spend20tn with zero inflation.')
 check('BASE_SHARE',abs(cf['share'][0,0]-.5)<1e-12,'National internal share50%.')
 check('BASE_UNIT_INTERNAL',abs(np.dot(Q0,AVG_I)/Q0.sum()-8000)<1e-9,'Weighted internal8,000; weighted external12,000 independently checked.')
 check('BASE_WEIGHTS',abs(WEIGHTS.sum()-1)<1e-12,'Weights sum1; national2bn parcels.')
 w=draw(1000,SEED_HOLDOUT);w2=draw(1000,SEED_HOLDOUT)
 check('SEED',all(np.array_equal(w[k],w2[k]) for k in w),'PCG64 seeded sampling exactly repeats in this NumPy version.')
 maxcons=0.;maxcap=0.;growthpasses=0
 for s in policy_list():
  op=operating(w,s['package'],s['target'],s['buffer']);maxcons=max(maxcons,float(np.abs(op['d']-op['q']-op['e']-op['unserved']).max()));maxcap=max(maxcap,float((op['q']-op['k']).max()))
  z=central();growthpasses+=int(finances(operating(z,s['package'],s['target'],s['buffer']),operating(z,'current'),s['package'],z)['growth_pass'][0])
 check('CONSERVE',maxcons<1e-10,f'Max absolute parcel-bn discrepancy{maxcons:.3g}; internal+external+deferred equals demand.')
 check('CAPACITY',maxcap<=1e-10,f'Max capacity excess{maxcap:.3g}bn; stochastic travel/capacity respected.')
 check('ANNUAL_GROWTH_GATE',growthpasses==0,f'Correctly reports0/{len(policy_list())} central policies passing all annual growth tests. This PASS validates detection of a FAILED investment gate.')
 for ww in [np.array([.45,.25,.20,.10]),np.array([.25,.25,.35,.15])]:
  c=central();c['inflation'][:]=0;op=operating(c,'current',weights=ww)
  check('WEIGHT_'+str(ww[0]),abs(op['cost'][0,0]-20)<1e-9 and abs(op['share'][0,0]-.5)<1e-9,'Alternative national weights recalibrated to50%/8,000/12,000.')
 r=a['recommended'];op=operating(draw(10000,SEED_HOLDOUT),r['package'],r['target'],r['buffer']);cf=operating(draw(10000,SEED_HOLDOUT),'current');f=finances(op,cf,r['package'],draw(10000,SEED_HOLDOUT))
 saved=np.load(ROOT/'results/finalist_npvs.npz')[r['policy_id']]
 check('HELDOUT_REPRO',np.max(np.abs(saved-f['npv']))<1e-10,'10,000 recommended-candidate NPVs re-executed and matched saved array.')
 inc=get('data/incidents.json');cons=[]
 for row in [inc['base_window']]+inc['actions']:cons.append(row['conservation_max_error'])
 regional=get('data/regional_outcomes.json')['results']
 reg_ok=all(x['conservation_max_error']<1e-6 and max(x['hub_utilisation'])<=1.000001 and min(x['unused_capacity_daily'])>=-1e-6 for x in regional.values())
 check('REGIONAL_LP',max(cons)<1e-6 and reg_ok,'All14 regional policies and4-hour incident conserve parcels and respect shared hub planning/physical capacities.')
 check('GEOJSON',all(get('geo/'+name)['type']=='FeatureCollection' for name in ['corridors.geojson','decision_zones.geojson','facilities.geojson']),'Valid GeoJSON structure; schematic-status labels explicit.')
 checks.append(dict(check_id='DETAILED_GIS',status='PARTIAL',detail='No full-resolution street/building/settlement extract. Coarse corridor attributes include authored distances; cannot certify street routing or detailed access restrictions.'))
 check('JSON_FINITE',True,'json.dumps allow_nan=False used for every JSON/GeoJSON export; successful serialisation.')
 z=central();op=operating(z,r['package'],r['target'],r['buffer']);f=finances(op,operating(z,'current'),r['package'],z)
 fixtures=dict(schema_version='1.0.0',tolerances=dict(parcel_bn=1e-9,money_tn=1e-8,ratio=1e-8,regional_idr=1.),fixtures=[dict(fixture_id='F_BASE_2025',input=dict(inflation=0,demand_axis=1,package='current'),expected=dict(annual_demand_bn=2,internal_bn=1,external_bn=1,total_cost_tn=20,blended_cost_idr=10000)),dict(fixture_id='F_CENTRAL_RECOMMENDED',input=dict(package=r['package'],target=r['target'],buffer=r['buffer'],world='central',discount_rate=.14,horizon=5),expected=dict(costs_tn=op['cost'][0],internal_share=op['share'][0],cashflows_tn=f['flows'][0],npv_tn=float(f['npv'][0]),irr=irr(f['flows'][0]),group_profit_tn=f['profit'][0],positive_growth_all_years=bool(f['growth_pass'][0]))),dict(fixture_id='F_INCIDENT',input=dict(scenario_id=inc['scenario_id']),expected=dict(base_window_cost_idr=inc['base_window']['cost_idr'],actions=[dict(action_id=x['action_id'],cost_idr=x['cost_idr'],deferred_parcels=sum(x['deferred'])) for x in inc['actions']]))])
 write_json('data/reference_fixtures.json',fixtures)
 write_json('results/validation.json',dict(schema_version='1.0.0',checks=checks,strict_growth_pass_count=growthpasses,executed_candidates=len(policy_list()),workbook_checks='To be appended by build_workbook.mjs and verify_workbook.py'))
 return checks

def exhibits(a,p):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
 finalists=p['finalists']; keep=[x for x in finalists if x['policy_id'] in ['P_CURRENT','P_RULES_70_88',a['recommended']['policy_id'],'P_TARGETED_75_100','P_LARGE_85_100',a['maxreturn']['policy_id']]]
 fig,ax=plt.subplots(figsize=(10,5));x=np.arange(len(keep));m=np.array([v['expected_npv_tn'] for v in keep]);lo=np.array([v['p10_npv_tn'] for v in keep]);hi=np.array([v['p90_npv_tn'] for v in keep]);ax.bar(x,m,color=['#184f78' if v['policy_id']!=a['recommended']['policy_id'] else '#d78a31' for v in keep]);ax.errorbar(x,m,yerr=[m-lo,hi-m],fmt='none',ecolor='#313d49',capsize=4);ax.axhline(0,color='#777',lw=.8);ax.set_xticks(x,[v['policy_id'].replace('P_','').replace('_','\n') for v in keep]);ax.set_ylabel('5-year incremental NPV, Rp trillion');ax.set_title('Capital expansion is not the central-case value winner',loc='left',fontweight='bold');fig.text(.02,.015,'10,000 matched held-out worlds per finalist. Whiskers are assumed-distribution p10–p90, not empirical confidence intervals.',fontsize=8);fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(ROOT/'exhibits/policy_npv.png',dpi=170);plt.close(fig)
 cells=get('data/heatmap.json')['cells'];targets=sorted({c['target_share'] for c in cells});demands=sorted({c['demand_axis'] for c in cells});grid=np.array([[next(c['expected_y5_ebit_tn'] for c in cells if c['target_share']==t and c['demand_axis']==d) for d in demands] for t in targets]);fig,ax=plt.subplots(figsize=(8,6));im=ax.imshow(grid,cmap='RdYlGn',aspect='auto');
 for i,t in enumerate(targets):
  for j,d in enumerate(demands):
   c=next(c for c in cells if c['target_share']==t and c['demand_axis']==d);ax.text(j,i,f'{grid[i,j]:.2f}'+(' *' if not c['feasible'] else ''),ha='center',va='center',fontsize=8)
 ax.set_xticks(range(len(demands)),[f'{d:.0%}' for d in demands]);ax.set_yticks(range(len(targets)),[f'{t:.0%}' for t in targets]);ax.set_xlabel('Parcel-demand level relative to2bn/year; identical matching counterfactual');ax.set_ylabel('Requested maximum internal-share ceiling');ax.set_title('Year5 incremental EBIT, Rp trillion',loc='left',fontweight='bold');fig.colorbar(im,ax=ax,label='Rp tn');fig.text(.02,.015,'* Target not attained under economic/capacity limits, or service-risk limit fails.1,000 held-out worlds/cell.',fontsize=8);fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(ROOT/'exhibits/policy_heatmap.png',dpi=170);plt.close(fig)
 ss=a['sensitivity'];fig,ax=plt.subplots(figsize=(9,4.8));base=get('data/selected_outcomes.json')['outcomes'][a['recommended']['policy_id']]['financial']['npv'];
 for i,s in enumerate(ss):ax.plot([s['npv_at_low'],s['npv_at_high']],[i,i],lw=12,color='#577c98',solid_capstyle='butt');ax.scatter([s['npv_at_low'],s['npv_at_high']],[i,i],c=['#d78a31','#184f78'],s=30,zorder=3)
 ax.axvline(base,color='#333',ls='--',label='Central');ax.axvline(0,color='#888',lw=.8);ax.set_yticks(range(len(ss)),[s['driver'] for s in ss]);ax.set_xlabel('5-year NPV, Rp tn');ax.set_title('Sensitivity of the service-preserving software candidate',loc='left',fontweight='bold');fig.text(.02,.015,'One-at-a-time authored input ranges. Low/high ends can reverse direction. Does not establish causal sensitivity.',fontsize=8);fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(ROOT/'exhibits/sensitivity.png',dpi=170);plt.close(fig)
 fig,ax=plt.subplots(figsize=(9,7));
 for a1,b1,km,*_ in EDGES:
  xy=np.array([NODES[a1][1:],NODES[b1][1:]]);ax.plot(xy[:,0],xy[:,1],c='#bdc8d0',lw=1.4)
 geo=get('geo/decision_zones.geojson')['features'];rows=[f for f in geo if f['properties']['policy_id']=='P_RULES_70_88']
 for row in rows:
  pr=row['properties'];j=int(pr['zone_id'][2:]);node=ZONES[j][0];lon,lat=NODES[node][1:];ax.scatter(lon,lat,s=pr['daily_parcels']/400,c=pr['internal_fraction'],vmin=0,vmax=1,cmap='Blues',edgecolors='#333');ax.annotate(pr['name'],(lon,lat),xytext=(5,6),textcoords='offset points',fontsize=8)
 ax.set_xlabel('Longitude');ax.set_ylabel('Latitude');ax.set_title('Greater Jakarta corridor fallback: hypothetical planning catchments',loc='left',fontweight='bold');ax.set_aspect(1/np.cos(np.radians(6.3)));fig.text(.02,.02,'Schematic endpoint lines, not acquired road geometry. Routing weights are corridor observations/assumptions. Detailed GIS gate remains open.',fontsize=8);fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(ROOT/'exhibits/geography_fallback.png',dpi=170);plt.close(fig)

def build_data(a,p):
 inputs=get('data/config.json');central7=[]
 for s in p['finalists']:
  z=central(years=7);op=operating(z,s['package'],s['target'],s['buffer']);f=finances(op,operating(z,'current'),s['package'],z)
  central7.append(dict(policy_id=s['policy_id'],package=s['package'],target=s['target'],buffer=s['buffer'],benefit_2025_tn=(f['benefit'][0]/1.025**np.arange(1,8)).tolist(),central_financial_5=get('data/selected_outcomes.json')['outcomes'][s['policy_id']],soft_capex=PACKAGES[s['package']]['soft'],physical_capex=PACKAGES[s['package']]['physical'],transition=PACKAGES[s['package']]['transition']))
 curves=[];q0,f,v=calibration()
 for i,t in enumerate(TYPES):
  for frac in np.arange(0,1.201,.05):
   q=CAP[i]*frac
   ot=OT[i]/2*max(q-.85*CAP[i],0)**2/(.15*CAP[i])/1000
   mix=MIX[i]/2*max(q-q0[i],0)**2/max(2*WEIGHTS[i]-q0[i],1e-6)/1000
   cost=f[i]+v[i]*q/1000+ot+mix
   mc=v[i]+OT[i]*max(q-.85*CAP[i],0)/(.15*CAP[i])+MIX[i]*max(q-q0[i],0)/max(2*WEIGHTS[i]-q0[i],1e-6)
   curves.append(dict(market_type=t,capacity_fraction=float(frac),internal_bn=float(q),average_cost_idr=float(cost/q*1000) if q>0 else None,marginal_cost_idr=float(mc) if frac<=1.0001 else None,feasible=bool(frac<=1.0001),external_price_idr=float(PRICE_E[i])))
 write_json('data/cost_curves.json',dict(schema_version='1.0.0',curves=curves))
 write_json('results/workbook_inputs.json',dict(analysis=a,policies=p,central7=central7,assumptions=assumptions(),sources=SOURCES,config=inputs,heatmap=get('data/heatmap.json'),regional=get('data/regional_outcomes.json'),geo=get('geo/decision_zones.geojson'),routes=get('data/routes.json'),validation=get('results/validation.json'),curves=curves))


def run():
 a=get('results/analysis.json');p=get('data/policies.json');checks=qa_and_fixtures(a,p)
 from render_docs import render
 render(a,p,checks,SOURCES,assumptions());build_data(a,p);exhibits(a,p)
 write_json('results/dependencies.json',dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform(),artifact_tool='Codex bundled@oai/artifact-tool; runtime26.1022.11436'))
 print('Reports, fixtures, exhibits and master context pack updated. Checks:',[(c['check_id'],c['status']) for c in checks])

if __name__=='__main__':run()
