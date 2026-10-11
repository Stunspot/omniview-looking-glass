"""Reproducibly assemble the current complete OmniView0.3.0 kit from maintained source."""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAME='omniview-looking-glass'
BASELINE_SHA='e669a17f0bd0ef1465f17f508d66a98c6a2d666ec1dd8aa559abaf4c23f8b14a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(root):return sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.lnk') and p.name!='desktop.ini')
def archive(root,dest):
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files(root):
   rel=p.relative_to(root).as_posix()
   item=zipfile.ZipInfo(root.name+'/'+rel,(2026,10,11,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.create_system=3
   executable=p.suffix=='.command' or rel.endswith('OmniView.app/Contents/MacOS/launch')
   item.external_attr=(0o100755 if executable else 0o100644)<<16
   z.writestr(item,p.read_bytes())
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();out=args.output.resolve()
 if out==ROOT or ROOT in out.parents or out.exists() or out.with_suffix('.zip').exists():raise ValueError('Choose a fresh output outside the maintained source.')
 out.mkdir(parents=True)
 for name in ['docs','customer-kit','delivery-sidecars','LICENSES']:
  shutil.copytree(ROOT/name,out/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.lnk','desktop.ini'))
 shutil.copytree(ROOT/'dropins',out/'gl4ss-dropins')
 for name in ['README.md','OPEN-WORKSPACE.md','RELEASE-NOTES.md','RELEASE-DECISION.md','DIRECT-RENDER-INSPECTION.md','INTERFACE-INSPECTION.md','CONTRIBUTING.md','LICENSE.md','NOTICE.md','SECURITY.md','SUPPORT.md','TRADEMARKS.md']:shutil.copyfile(ROOT/name,out/name)
 source=ROOT/'plugins'/NAME/'skills'/NAME
 for src,rel in [(source,'codex/'+NAME),(ROOT/'plugins'/NAME,'plugin/'+NAME)]:
  shutil.copytree(src,out/rel,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.lnk','desktop.ini'))
 (out/'claude').mkdir();archive(source,out/'claude'/(NAME+'.zip'))
 shutil.copyfile(ROOT/'scripts/verify_customer_kit.py',out/'VERIFY.py')
 payload=[{'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files(out)]
 manifest={'product':NAME,'version':'0.3.0','runtime_version':'0.3.0','channel':'complete-current-kit','release_treatment':'edit','baseline':'accepted0.3.0','baseline_archive_sha256':BASELINE_SHA,'claim_boundary':'Current Windows native/state workflows and mocked direct-provider orchestration; Mac device execution and paid Image API qualification remain unobserved','payload':payload}
 (out/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
 (out/'SHA256SUMS.txt').write_text('\n'.join(sha(p)+'  '+p.relative_to(out).as_posix() for p in files(out))+'\n',encoding='utf8',newline='\n')
 archive(out,out.with_suffix('.zip'));print(json.dumps({'output':str(out),'archive':str(out.with_suffix('.zip')),'members':len(files(out)),'sha256':sha(out.with_suffix('.zip'))}))
if __name__=='__main__':main()
