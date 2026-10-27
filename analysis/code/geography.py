"""Coarse Greater Jakarta corridor fallback, NOT a downloaded street network.
Official corridor lengths + explicitly authored subdivision/access lengths.
The physical GIS acquisition gate remains open. No Euclidean routing distances.
"""
from pathlib import Path
import json,csv,heapq,time
import numpy as np
from scipy.optimize import linprog
from model import ROOT,write_json

BPJT='https://bpjt.pu.go.id/dirgahayu-kota-jakarta-ke-496-ini-dia-beragam-jalan-tol-yang-ada-di-jakarta/'
NODES={
 'CAW':('Cawang',106.873,-6.243),'TOM':('Tomang',106.793,-6.176),
 'PLU':('Pluit',106.794,-6.119),'KJ':('Kebon Jeruk',106.761,-6.190),
 'ULU':('Ulujami',106.764,-6.242),'PAR':('Pondok Aren',106.737,-6.263),
 'PPI':('Pondok Pinang',106.781,-6.291),'TMI':('Taman Mini',106.881,-6.307),
 'CIB':('Cibubur',106.895,-6.366),'CIM':('Cimanggis',106.897,-6.433),
 'BOG':('Bogor corridor',106.832,-6.604),'BIT':('Bitung / Tangerang corridor',106.560,-6.238),
 'BEK':('Bekasi corridor',106.991,-6.252),'ANT':('Antasari',106.814,-6.293),
 'DEP':('Depok corridor',106.800,-6.401),'KMU':('Kampung Melayu',106.868,-6.224)}
# These are corridor abstractions. Coordinates are approximate authored display anchors.
EDGES=[
 ('CAW','TOM',16.,'Cawang–Tomang','historical observation; current distance uncertain','https://bphn.go.id/data/documents/81kp038.pdf'),
 ('TOM','PLU',7.5,'Tomang–Pluit','derived 23.5 minus historical16; assumption of consistent alignment',BPJT),
 ('CAW','PLU',27.05,'Eastern inner ring via Tanjung Priok','external corridor length',BPJT),
 ('TOM','KJ',3.,'Jakarta–Tangerang east subsection','ASSUMPTION',BPJT),
 ('KJ','BIT',30.,'Jakarta–Tangerang west subsection','derived 33 minus assumed3; terminal anchor approximate',BPJT),
 ('KJ','ULU',7.87,'JORR W2 North','external corridor length',BPJT),
 ('ULU','PAR',5.55,'Pondok Aren–Ulujami','external corridor length',BPJT),
 ('ULU','PPI',5.,'JORR southwest connector','ASSUMPTION',BPJT),
 ('PPI','TMI',14.25,'JORR South','external corridor length',BPJT),
 ('CAW','TMI',7.,'Jagorawi northern subsection','ASSUMPTION',BPJT),
 ('TMI','CIB',8.,'Jagorawi middle north','ASSUMPTION',BPJT),
 ('CIB','CIM',10.,'Jagorawi middle','ASSUMPTION',BPJT),
 ('CIM','BOG',23.,'Jagorawi south to Bogor corridor','ASSUMPTION; not the full59km concession length',BPJT),
 ('PPI','ANT',3.,'TB Simatupang access abstraction','ASSUMPTION',BPJT),
 ('ANT','DEP',12.1,'Depok–Antasari corridor','external corridor length; approximate terminal anchors',BPJT),
 ('CAW','KMU',4.,'Cawang–Kampung Melayu access abstraction','ASSUMPTION',BPJT),
 ('KMU','BEK',15.28,'Bekasi–Cawang–Kampung Melayu corridor','external corridor length; terminal anchor approximate',BPJT)]
ZONES=[
 ('CAW','East Jakarta',3085058,1.10,'BPS2025 search-index table observation'),
 ('TOM','West Jakarta',2487199,1.25,'BPS2025 search-index table observation'),
 ('PLU','North Jakarta',1800000,1.15,'rounded population-proxy ASSUMPTION'),
 ('PPI','South Jakarta',2219220,1.30,'BPS2025 search-index table observation'),
 ('BIT','Tangerang corridor',1970000,.90,'rounded population-proxy ASSUMPTION'),
 ('PAR','South Tangerang corridor',1430000,1.05,'rounded population-proxy ASSUMPTION'),
 ('DEP','Depok',2167961,.85,'BPS2025 search-index table observation'),
 ('BOG','Bogor corridor',1100000,.80,'rounded population-proxy ASSUMPTION'),
 ('BEK','Bekasi',2648300,1.00,'BPS2025 search-index table observation')]
HUBS=[dict(hub_id='H_CAW',node='CAW',capacity_daily=240000,status='hypothetical_existing'),dict(hub_id='H_TOM',node='TOM',capacity_daily=210000,status='hypothetical_existing'),dict(hub_id='H_DEP',node='DEP',capacity_daily=160000,status='hypothetical_existing'),dict(hub_id='H_BEK_CAND',node='BEK',capacity_daily=120000,status='hypothetical_candidate')]

def graph():
 g={n:[] for n in NODES}
 for i,(a,b,km,*_) in enumerate(EDGES):
  g[a].append((b,km,f'C_{i:02}'));g[b].append((a,km,f'C_{i:02}'))
 return g

def shortest(g,source,target):
 todo=[(0.,source,[])];seen=set()
 while todo:
  dist,n,path=heapq.heappop(todo)
  if n in seen:continue
  seen.add(n)
  if n==target:return dist,path
  for v,km,e in g[n]:
   if v not in seen:heapq.heappush(todo,(dist+km,v,path+[e]))
 return None,[]

def solve(demand,cost,cap,external,external_capacity=None,emergency=0.,window='day',fixed_internal_fraction=None):
 """Transport LP. Shared hubs and shared 3PL reservation; backlog explicit."""
 h,z=cost.shape
 # Variables hub-zone, external-zone, emergency-zone, deferred-zone.
 c=np.r_[cost.ravel(),external,np.full(z,14000.),np.full(z,18000.)]
 Aeq=np.zeros((z,h*z+3*z))
 for j in range(z):
  for i in range(h):Aeq[j,i*z+j]=1
  for k in range(3):Aeq[j,h*z+k*z+j]=1
 beq=np.asarray(demand)
 if fixed_internal_fraction is not None:
  Afix=np.zeros_like(Aeq)
  for j in range(z):
   for i in range(h):Afix[j,i*z+j]=1
  Aeq=np.vstack([Aeq,Afix]);beq=np.r_[demand,np.asarray(demand)*fixed_internal_fraction]
 Aub=[];bub=[]
 for i in range(h):
  row=np.zeros_like(c);row[i*z:(i+1)*z]=1;Aub.append(row);bub.append(cap[i])
 row=np.zeros_like(c);row[h*z:h*z+z]=1;Aub.append(row);bub.append(external_capacity if external_capacity is not None else sum(demand))
 row=np.zeros_like(c);row[h*z+z:h*z+2*z]=1;Aub.append(row);bub.append(emergency)
 r=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs')
 if not r.success:raise RuntimeError(r.message)
 a=r.x[:h*z].reshape(h,z);e=r.x[h*z:h*z+z];em=r.x[h*z+z:h*z+2*z];u=r.x[-z:]
 return dict(internal=a,external=e,emergency=em,deferred=u,cost_idr=float(r.fun),hub_utilisation=a.sum(1)/np.maximum(cap,1),window=window,conservation_max_error=float(np.max(np.abs(a.sum(0)+e+em+u-demand))))

def json_result(r):return {k:v.tolist() if hasattr(v,'tolist') else v for k,v in r.items()}

def run():
 start=time.perf_counter();g=graph();z=len(ZONES);h=3;volume=2e9*.20/365
 pop=np.array([a[2] for a in ZONES],float);act=np.array([a[3] for a in ZONES]);proxy=.8*pop/pop.sum()+.2*(pop*act)/(pop*act).sum();d=volume*proxy
 matrices=[];dist=np.empty((4,z));paths={}
 for i,hub in enumerate(HUBS):
  for j,(node,*_) in enumerate(ZONES):
   km,path=shortest(g,hub['node'],node);dist[i,j]=km if km is not None else np.inf;paths[(i,j)]=path
   matrices.append(dict(lane_id=f'L_{hub["hub_id"]}_{j:02}',hub_id=hub['hub_id'],zone_id=f'Z_{j:02}',corridor_network_km=km,estimated_one_way_minutes=km/30*60 if km is not None else None,reachable=km is not None,corridor_ids=path,distance_status='coarse_corridor_estimate_not_street_routing',local_access_distance_km=None))
 # Local delivery costs are authored; no claim that a corridor is a last-mile road network.
 stops=np.array([14,14,12,13,10,11,10,9,11],float)
 local=2400+35000/stops+1900+.04*3500
 cost=local[None,:]+(2*dist/30*55000+2*dist*900)/180
 ext=np.array([10000]*4+[11000]*5,float)
 caps=np.array([a['capacity_daily'] for a in HUBS[:h]],float)
 national=json.loads((ROOT/'data/policies.json').read_text())
 configs=[(s['policy_id'],s['target'],s['buffer'],s['package']=='large',s['package']) for s in national['finalists']]
 results={};features=[]
 for pid,target,buffer,candidate,package in configs:
  hc=4 if candidate else h; cp=np.r_[caps,120000] if candidate else caps.copy()
  if package=='targeted':cp*=1.18
  if package=='large':cp*=1.35
  physical_cp=cp.copy()
  # One shared internal-volume limit implemented as an additional virtual capacity scaling.
  cp=cp*buffer; cp*=min(1,volume*target/cp.sum())
  co=cost[:hc]*(.985 if package in ['software','targeted','large'] else 1.)
  co=np.where(dist[:hc]/30*60<=120,co,1e6)
  rr=solve(d,co,cp,ext,volume*.70,fixed_internal_fraction=.5 if package=='current' else None)
  results[pid]=dict(policy_id=pid,package=package,target_internal_share_ceiling=target,buffer=buffer,**json_result(rr),capacity_daily_available=physical_cp.tolist(),capacity_daily_planning=cp.tolist(),unused_capacity_daily=(physical_cp-rr['internal'].sum(1)).tolist(),physical_hub_utilisation=(rr['internal'].sum(1)/physical_cp).tolist(),daily_demand=float(d.sum()),realised_internal_share=float(rr['internal'].sum()/d.sum()),daily_committed_cost_idr=1.2e9,full_daily_cost_idr=rr['cost_idr']+1.2e9)
  for j,(node,name,population,activity,status) in enumerate(ZONES):
   alloc=float(rr['internal'][:,j].sum()/d[j]);adv=float(ext[j]-np.min(co[:,j]));preferred='internal' if alloc>=.75 else 'external' if alloc<=.25 else 'mixed'
   x,y=NODES[node][1:];rad=.025
   geometry=dict(type='Polygon',coordinates=[[[x-rad,y-rad],[x+rad,y-rad],[x+rad,y+rad],[x-rad,y+rad],[x-rad,y-rad]]])
   features.append(dict(type='Feature',geometry=geometry,properties=dict(zone_id=f'Z_{j:02}',policy_id=pid,name=name,preferred_mode=preferred,internal_fraction=alloc,marginal_advantage_idr=adv,daily_parcels=float(d[j]),population_proxy=population,population_status=status,max_shared_hub_pressure=float(rr['hub_utilisation'].max()),geography_status='authored_analytical_square_not_administrative_boundary',routing_status='coarse_corridor_only')))
 # Monte Carlo switching at 200 worlds with persistent travel/cost variation; provenance is assumptions.
 r=np.random.default_rng(73027);modes=[]
 for i in range(200):
  traffic=r.lognormal(-.5*.2**2,.2);im=r.lognormal(-.5*.06**2,.06)
  co=cost[:3]*im+2*dist[:3]/30*55000/180*(traffic-1)
  rr=solve(d,co,caps*.88,ext,volume*.70)
  modes.append(rr['internal'].sum(0)/d>=.5)
 modes=np.asarray(modes)
 for f in features:
  j=int(f['properties']['zone_id'][2:]);f['properties']['internal_majority_fraction_of_200_worlds']=float(modes[:,j].mean())
  f['properties']['switching_simulation_policy_id']='P_RULES_70_88'
 # Alternative proxy and resolution comparisons; 18 children inherit the same corridor terminal.
 alternatives=[]
 for name,pr in [('population_only',pop/pop.sum()),('activity_only',(pop*act)/(pop*act).sum()),('uniform',np.ones(z)/z)]:
  rr=solve(volume*pr,cost[:3],caps*.88,ext,volume*.70)
  alternatives.append(dict(variant=name,zones=9,internal_share=float(rr['internal'].sum()/volume),avoidable_daily_cost_idr=rr['cost_idr']))
 rr=solve(np.repeat(d/2,2),np.repeat(cost[:3],2,axis=1)+np.tile([-150,150],z),caps*.88,np.repeat(ext,2),volume*.70)
 alternatives.append(dict(variant='18_subzones_same_corridor_terminals',zones=18,internal_share=float(rr['internal'].sum()/volume),avoidable_daily_cost_idr=rr['cost_idr'],limitation='local cost heterogeneity assumed; no extra observed streets'))
 # Four-hour dispatch incident; the other eight hours retain their normal plan.
 base=solve(d/3,cost[:3],caps*.88/3,ext,volume*.70/3,window='4h')
 outagecap=caps*.88/3;outagecap[0]*=.5
 fixed=base['internal'].copy();lost=fixed[0]*.5;fixed[0]*=.5
 frozen=dict(internal=fixed,external=base['external'],emergency=base['emergency'],deferred=base['deferred']+lost,cost_idr=float((fixed*cost[:3]).sum()+np.dot(base['external'],ext)+18000*(base['deferred']+lost).sum()),window='4h',hub_utilisation=fixed.sum(1)/outagecap,conservation_max_error=0.)
 reallocate=solve(d/3,cost[:3],outagecap,ext,volume*.70/3,window='4h')
 emergency=solve(d/3,cost[:3],outagecap,ext,volume*.70/3,emergency=40000,window='4h')
 incident=dict(schema_version='1.0.0',scenario_id='S_HUB_CAW_4H_LOSS',base_policy_id='P_RULES_70_88',world_id='central',scope='regional',hub_id='H_CAW',capacity_loss_fraction=.5,duration_hours=4,planning_day_hours=12,daily_capacity_loss_fraction=.5*4/12,base_window=json_result(base),actions=[dict(action_id='A_FREEZE',label='Freeze original routes; defer displaced parcels',**json_result(frozen)),dict(action_id='A_REALLOCATE',label='Reallocate within existing hubs and carrier reservations',**json_result(reallocate)),dict(action_id='A_EMERGENCY',label='Add up to 40,000 emergency 3PL parcels at Rp14,000',**json_result(emergency))],other_8h_cost_idr=base['cost_idr']*2,daily_reconciliation='Daily variable cost = other_8h_cost_idr + selected 4h action cost. Add fixed daily committed cost once. Deferred in the 4h window is reported as backlog; no automatic same-day clearance assumed.',assessment_status='scripted_demo_no_AI_calls')
 # Display lines are endpoint sketches; cost distances derive from edge attributes, never chord geometry.
 roadfeatures=[]
 for i,(a,b,km,name,status,url) in enumerate(EDGES):
  roadfeatures.append(dict(type='Feature',geometry=dict(type='LineString',coordinates=[NODES[a][1:],NODES[b][1:]]),properties=dict(corridor_id=f'C_{i:02}',from_node=a,to_node=b,network_length_km=km,name=name,provenance=status,source_url=url,geometry_status='schematic_endpoint_line_only',access='van_or_truck; no motorcycle toll access',direction='two_directed_corridor_arcs; ramps/turn restrictions unresolved')))
 facilities=[dict(type='Feature',geometry=dict(type='Point',coordinates=NODES[a['node']][1:]),properties=a) for a in HUBS]
 write_json('geo/corridors.geojson',dict(type='FeatureCollection',features=roadfeatures))
 write_json('geo/decision_zones.geojson',dict(type='FeatureCollection',features=features))
 write_json('geo/facilities.geojson',dict(type='FeatureCollection',features=facilities))
 write_json('data/routes.json',dict(schema_version='1.0.0',lanes=matrices))
 write_json('data/regional_outcomes.json',dict(schema_version='1.0.0',national_volume_fraction_assumption=.20,annual_parcels=400000000,days_per_year=365,region='Selected Greater Jakarta corridor markets, not a complete administrative union',results=results,alternative_proxies=alternatives,geospatial_validation_gate='PARTIAL: road geometry, detailed topology, actual access restrictions and last-mile routing not acquired'))
 write_json('data/incidents.json',incident)
 write_json('geo/qa.json',dict(nodes=len(NODES),corridor_edges=len(EDGES),directed_arcs=len(EDGES)*2,weak_components=1,zones=9,policy_zone_features=len(features),facilities=len(HUBS),matrix_entries=len(matrices),unreachable_pairs=int(np.isinf(dist).sum()),crs='OGC:CRS84 longitude,latitude; schematic geometry',distance_method='Dijkstra on coarse corridor attributes; includes authored lengths, not shortest paths on observed streets',source_full_resolution_acquired=False,retained_source_layer='No downloaded road/building source layer; official textual corridor observations retained instead',runtime_seconds=time.perf_counter()-start))
 print('Regional corridor model executed; detailed road acquisition remains PARTIAL.')

if __name__=='__main__':run()
