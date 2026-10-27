"""Optional detailed OSM acquisition/preparation. NOT successful in this session.
Run after network access is available. Default only describes requested scope.
No GeoAI plugin execution is implied. OSM attribution/ODbL applies to downloaded data.
"""
import argparse,json,urllib.request,urllib.parse,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STUDY=[106.50,-6.65,107.05,-6.09]
BUFFER_DEGREES=.08

def hav(a,b):
 x1,y1,x2,y2=map(math.radians,[a[0],a[1],b[0],b[1]])
 return 6371008.8*2*math.asin(math.sqrt(math.sin((y2-y1)/2)**2+math.cos(y1)*math.cos(y2)*math.sin((x2-x1)/2)**2))

def prepare(data):
 nodes={e['id']:(e['lon'],e['lat']) for e in data['elements'] if e['type']=='node'}
 arcs=[];rejected=0
 allowed={'motorway','trunk','primary','secondary','tertiary','residential','unclassified','service','motorway_link','trunk_link','primary_link','secondary_link','tertiary_link','living_street'}
 for way in data['elements']:
  if way['type']!='way':continue
  tags=way.get('tags',{})
  if tags.get('highway') not in allowed or tags.get('access') in ['no','private'] or tags.get('motor_vehicle') in ['no','private'] or tags.get('motorcar')=='no':rejected+=1;continue
  oneway=tags.get('oneway','yes' if tags.get('junction')=='roundabout' else 'no')
  ids=way.get('nodes',[])
  for a,b in zip(ids,ids[1:]):
   if a not in nodes or b not in nodes:continue
   length=hav(nodes[a],nodes[b])
   if length<=0:continue
   if oneway!='-1':arcs.append([a,b,length,way['id']])
   if oneway not in ['yes','1','true']:arcs.append([b,a,length,way['id']])
 return dict(crs='OGC:CRS84',distance_unit='metres',nodes=nodes,arcs=arcs,rejected_ways=rejected,limitations=['Conditional access and turn-restriction relations require a subsequent edge-state graph.','Do not join geometric crossings without shared OSM node IDs.','Disconnected/unreachable destinations must remain null.','Nearest-node snap is not a verified local access route.','Speeds/congestion remain assumptions.'])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--download',action='store_true');args=ap.parse_args()
 x1,y1,x2,y2=STUDY;b=BUFFER_DEGREES
 query=f'[out:json][timeout:180];way[highway]({y1-b},{x1-b},{y2+b},{x2+b});(._;>;);out body;'
 plan=dict(study_bbox=STUDY,buffer_degrees=b,url='https://overpass-api.de/api/interpreter',query=query,license='OpenStreetMap contributors, ODbL 1.0',executed_download=False)
 if not args.download:print(json.dumps(plan,indent=2))
 else:
  try:
   request=urllib.request.Request(plan['url'],data=urllib.parse.urlencode({'data':query}).encode(),headers={'User-Agent':'NexoraCompetitionResearch/1.0'})
   raw=urllib.request.urlopen(request,timeout=200).read();data=json.loads(raw)
   (ROOT/'geo/osm_full_source.json').write_bytes(raw)
   (ROOT/'geo/osm_detailed_graph.json').write_text(json.dumps(prepare(data)))
   plan['executed_download']=True;plan['retrieved_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
  except Exception as e:plan['error']=str(e)
  (ROOT/'geo/osm_access_attempt.json').write_text(json.dumps(plan,indent=2));print(json.dumps(plan,indent=2))
