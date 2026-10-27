"""Manifest, portable CSVs and complete ZIP. Run after validation and receipts update."""
from pathlib import Path
import json,csv,hashlib,zipfile
from model import ROOT

def read(name):return json.loads((ROOT/name).read_text())
def csvout(name,rows):
 if not rows:return
 with (ROOT/name).open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader()
  for row in rows:writer.writerow({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in row.items()})

def run():
 csvout('results/policy_comparison.csv',read('data/policies.json')['finalists'])
 csvout('results/heatmap.csv',read('data/heatmap.json')['cells'])
 csvout('geo/routes_matrix.csv',read('data/routes.json')['lanes'])
 csvout('evidence/source_register.csv',read('data/sources.json')['sources'])
 csvout('evidence/assumption_register.csv',read('data/assumptions.json')['assumptions'])
 files=[]
 for path in sorted(ROOT.rglob('*')):
  if not path.is_file() or '__pycache__' in path.parts or path.name in ['MANIFEST.json','workbook_contact.png'] or path.name.endswith('.inspect.ndjson'):continue
  rel=path.relative_to(ROOT).as_posix()
  role='reproducible code' if rel.startswith('code/') else 'prototype JSON' if rel.startswith('data/') else 'geographic evidence / labelled corridor fallback' if rel.startswith('geo/') else 'exhibit' if rel.startswith('exhibits/') else 'workbook / previews' if rel.startswith('outputs/') else 'evidence' if rel.startswith('evidence/') else 'analysis / validation result' if rel.startswith('results/') else 'report / context'
  files.append(dict(path=rel,size_bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),role=role))
 manifest=dict(schema_version='1.0.0',status='Analysis complete within access limits; detailed GIS PARTIAL; no eligible national rollout under central annual-growth gate',main_workbook='outputs/nexora_v1/Nexora_Logistics_Analysis.xlsx',master_pack='Nexora_Master_Context_Pack.md',files=files,manifest_checksum_note='Manifest and ZIP exclude their own hashes to avoid circular hashes. All listed file hashes are exact at packaging.')
 (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
 archive=ROOT.parent/'deliverables/Nexora_Analysis_Package.zip';archive.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
  for item in files:z.write(ROOT/item['path'],'Nexora_Analysis_Package/'+item['path'])
  z.write(ROOT/'MANIFEST.json','Nexora_Analysis_Package/MANIFEST.json')
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  for item in files:assert hashlib.sha256(z.read('Nexora_Analysis_Package/'+item['path'])).hexdigest()==item['sha256']
 receipt=dict(path=str(archive),size_bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),entries=len(files)+1,zip_crc_and_member_hashes='PASS')
 (archive.parent/'Package_Checksum.json').write_text(json.dumps(receipt,indent=2))
 print(json.dumps(receipt,indent=2))

if __name__=='__main__':run()
