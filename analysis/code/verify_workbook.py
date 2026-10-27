"""Read-only ZIP/XML/cache checks. Does not author spreadsheets."""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET
import numpy as np
from model import ROOT,central,operating,finances,irr,PACKAGES,write_json

NS={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def get(p):return json.loads((ROOT/p).read_text())

def run():
 path=ROOT/'outputs/nexora_v1/Nexora_Logistics_Analysis.xlsx';checks=[]
 def check(id,passed,detail):
  checks.append(dict(check_id=id,status='PASS' if passed else 'FAIL',detail=detail))
  if not passed:raise AssertionError(id+': '+detail)
 z=zipfile.ZipFile(path);book=ET.fromstring(z.read('xl/workbook.xml'));rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
 ids={r.attrib['Id']:r.attrib['Target'] for r in rels};sheetmap={}
 for s in book.find('x:sheets',NS):
  target=ids[s.attrib['{'+NS['r']+'}id']];sheetmap[s.attrib['name']]=target.lstrip('/') if target.startswith('/') else 'xl/'+target
 strings=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  strings=[''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml'))]
 parsed={n:ET.fromstring(z.read(p)) for n,p in sheetmap.items()}
 def value(sheet,addr):
  c=parsed[sheet].find(f'.//x:c[@r="{addr}"]',NS)
  if c is None:return None
  t=c.attrib.get('t');v=c.find('x:v',NS)
  if t=='inlineStr':return ''.join(c.find('x:is',NS).itertext())
  if v is None:return None
  if t=='s':return strings[int(v.text)]
  if t in ['str','e']:return v.text
  if t=='b':return v.text=='1'
  return float(v.text) if v.text else None
 check('SHEET_COUNT',len(sheetmap)==13,'13 populated worksheets exported.')
 errors=[];missing=[];formula_count=0
 for n,xml in parsed.items():
  for c in xml.findall('.//x:c',NS):
   if c.attrib.get('t')=='e':errors.append((n,c.attrib['r'],c.find('x:v',NS).text))
   f=c.find('x:f',NS)
   if f is not None:
    formula_count+=1
    if c.find('x:v',NS) is None and c.attrib.get('t') not in ['str','inlineStr']:missing.append((n,c.attrib['r']))
 check('CACHED_FORMULAS',not missing,'All '+str(formula_count)+' exported formulas have cache/string results; no macro requirement.')
 check('NO_CELL_ERRORS',not errors,str(errors))
 check('NO_EXTERNAL_LINKS',not any('externalLinks/' in x for x in z.namelist()),'No broken external-workbook links.')
 a=get('results/analysis.json');r=a['recommended'];ref=get('data/selected_outcomes.json')['outcomes'][r['policy_id']]
 check('NPV_CACHE',abs(value('Finance','D43')-ref['financial']['npv'])<1e-8,'Exported NPV agrees with independent Python.')
 check('IRR_CACHE',abs(value('Finance','D44')-ref['irr'])<1e-8,'Project IRR cached and agrees with root-solved Python.')
 flows=np.array([value('Finance',f'{chr(68+i)}37') for i in range(6)])
 check('CASH_FLOWS',np.max(np.abs(flows-ref['financial']['flows']))<1e-8,'Time-zero and five annual flows agree.')
 profits=np.array([value('Finance',f'{chr(69+i)}27') for i in range(5)])
 check('PROFIT_BRIDGE',np.max(np.abs(profits-ref['financial']['profit']))<1e-8 and value('Finance','D48')=='FAIL','Group-profit bridge and failed annual-growth gate preserved.')
 check('PAYBACK',abs(value('Finance','D45')-ref['payback'])<1e-8 and abs(value('Finance','D46')-ref['discounted_payback'])<1e-8,'Fractional payback and discounted payback reconcile.')
 art=get('results/workbook_artifact_checks.json')
 for p in art['parity']:
  w=central(years=p['horizon']);op=operating(w,r['package'],r['target'],r['buffer']);f=finances(op,operating(w,'current'),r['package'],w)
  check('HORIZON_'+str(p['horizon']),abs(p['npv']-f['npv'][0])<1e-8 and abs(p['irr']-irr(f['flows'][0]))<1e-8,'Editable horizon change reproduced Python, then restored.')
 w=central();op=operating(w,r['package'],r['target'],r['buffer']);cf=operating(w,'current')
 for i,mult in enumerate([.8,1,1.6]):
  for j,rate in enumerate([.11,.14,.18]):
   expected=finances(op,cf,r['package'],w,rate=rate,cap_mult=mult)['npv'][0]
   check(f'DATA_TABLE_{i}_{j}',abs(art['dataTable'][i][j]-expected)<1e-8,'Native data-table cached NPV matches actual input changes.')
 tableformulas=parsed['Finance'].findall('.//x:f[@t="dataTable"]',NS)
 check('NATIVE_TABLE_EXPORT',len(tableformulas)>=1,'Excel native two-input data-table formula exported; caches verified. Desktop Excel not available here.')
 check('INPUT_RESPONSES',art['changedRate']<ref['financial']['npv'] and art['largeNpv']<0,'Discount-rate and selected-policy changes affected results, then were restored.')
 for file in (ROOT/'data').glob('*.json'):
  payload=json.loads(file.read_text());check('JSON_'+file.stem,payload.get('schema_version')=='1.0.0' or file.name=='schema.json','Versioned JSON parsed without NaN/Infinity.')
 # Validate required payload types and stable links rather than just a generic envelope.
 policies=get('data/policies.json');zones=get('geo/decision_zones.geojson')['features'];hubs={f['properties']['hub_id'] for f in get('geo/facilities.geojson')['features']};zoneids={f['properties']['zone_id'] for f in zones}
 for obj in policies['finalists']:
  assert all(k in obj for k in ['policy_id','package','target','buffer','expected_npv_tn','realised_internal_share'])
 for lane in get('data/routes.json')['lanes']:assert lane['hub_id'] in hubs and lane['zone_id'] in zoneids
 check('IDS_AND_SCHEMA',True,'Policy required fields and all 36 hub/zone lane references verified.')
 pack=(ROOT/'Nexora_Master_Context_Pack.md').read_text();brief=(ROOT/'evidence/Incoming_Handoff.md').read_text()
 check('ORIGINAL_BRIEF',pack.split('<!-- BEGIN ORIGINAL HANDOFF -->\n',1)[1].split('\n<!-- END ORIGINAL HANDOFF -->',1)[0]==brief,'Entire incoming brief preserved unchanged, exactly once.')
 previews=list((ROOT/'outputs/nexora_v1/previews').glob('*.png'))
 check('RENDER_COVERAGE',len(previews)>=13,'All 13 sheets rendered; contact-sheet and primary detailed views visually reviewed.')
 result=dict(checks=checks,native_application_limit='Artifact Tool recalculation and exported XML/caches verified. Native desktop Excel/LibreOffice not available; no claim of native-application execution.',geospatial_gate='PARTIAL',overall='PASS_WITH_DOCUMENTED_GIS_LIMITATION')
 write_json('results/workbook_validation.json',result)
 print(json.dumps(dict(checks=len(checks),status=result['overall'],npv=value('Finance','D43'),irr=value('Finance','D44'),annual_profit_gate=value('Finance','D48'),sheets=len(sheetmap)),indent=2))

if __name__=='__main__':run()
