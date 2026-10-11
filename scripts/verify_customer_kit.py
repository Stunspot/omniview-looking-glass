"""Read-only verification of the complete OmniView customer kit."""
from pathlib import Path
import argparse,hashlib,io,json,plistlib,sys,zipfile
def sha(raw):return hashlib.sha256(raw).hexdigest()
def members(root):
 return {p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.lnk') and p.name!='desktop.ini'}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);parser.add_argument('--archive',type=Path);args=parser.parse_args();root=args.root.resolve()
 manifest=json.loads((root/'release-manifest.json').read_text(encoding='utf8'))
 assert (manifest['product'],manifest['version'],manifest['runtime_version'],manifest['release_treatment'])==('omniview-looking-glass','0.3.0','0.3.0','edit')
 actual=members(root);payload={x['path']:x for x in manifest['payload']}
 assert set(actual)-{'release-manifest.json','SHA256SUMS.txt'}==set(payload),'Manifest payload is not closed'
 for name,entry in payload.items():
  raw=actual[name].read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],'Changed payload: '+name
 sums={}
 for line in (root/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
  digest,name=line.split('  ',1);assert name not in sums;sums[name]=digest
 assert set(sums)==set(actual)-{'SHA256SUMS.txt'}
 for name,digest in sums.items():assert sha(actual[name].read_bytes())==digest,'Changed checksum: '+name
 skill='codex/omniview-looking-glass/'
 with zipfile.ZipFile(root/'claude/omniview-looking-glass.zip') as z:
  expanded={name.split('/',1)[1]:z.read(name) for name in z.namelist()}
  expected={name[len(skill):]:p.read_bytes() for name,p in actual.items() if name.startswith(skill)}
  assert set(expanded)==set(expected),'Claude payload closure differs'
  for name,raw in expected.items():
   assert expanded[name]==raw,'Claude bytes differ: '+name
   assert (root/'plugin/omniview-looking-glass/skills/omniview-looking-glass'/name).read_bytes()==raw,'Plugin bytes differ: '+name
  launcher='omniview-looking-glass/workspace/OmniView.app/Contents/MacOS/launch'
  assert z.getinfo(launcher).create_system==3 and ((z.getinfo(launcher).external_attr>>16)&0o777)==0o755,'Claude Mac launcher is not executable'
 for key in ('codex/omniview-looking-glass','plugin/omniview-looking-glass/skills/omniview-looking-glass'):
  workspace=root/key/'workspace';info=plistlib.loads((workspace/'OmniView.app/Contents/Info.plist').read_bytes())
  assert info['CFBundleExecutable']=='launch' and info['CFBundleIconFile']=='omniview.icns'
  assert info['CFBundleShortVersionString']=='0.3.0'
  assert (workspace/'OmniView.app/Contents/MacOS/launch').read_bytes().startswith(b'#!/bin/sh\n')
  assert (workspace/'OmniView.app/Contents/Resources/omniview.icns').read_bytes()==(workspace/'native/omniview.icns').read_bytes()
  assert (workspace/'native/omniview.icns').read_bytes().startswith(b'icns')
  assert (workspace/'native/omniview.ico').read_bytes().startswith(b'\x00\x00\x01\x00')
  assert '/native/omniview-32.png' in (workspace/'index.html').read_text(encoding='utf8')
  assert 'OmniView.NativeShortcut' in (workspace/'Setup Windows Launcher.ps1').read_text(encoding='utf-8-sig')
 if args.archive:
  with zipfile.ZipFile(args.archive) as z:
   names=z.namelist();roots={name.split('/')[0] for name in names};assert len(roots)==1
   prefix=next(iter(roots))+'/'
   assert {name[len(prefix):] for name in names}==set(actual),'Outer archive is not closed'
   for name,p in actual.items():assert z.read(prefix+name)==p.read_bytes(),'Outer archive bytes differ: '+name
   for name in names:
    if name.endswith('/OmniView.app/Contents/MacOS/launch') or name.endswith('/Open.command'):
     assert z.getinfo(name).create_system==3 and ((z.getinfo(name).external_attr>>16)&0o777)==0o755,'Outer native launcher is not executable'
 print(json.dumps({'status':'PASS','product':'omniview-looking-glass','version':'0.3.0','payload_files':len(payload),'portable_files':len(expected),'native_bindings':'Windows shortcut source, macOS plist/icon/launcher and executable archive mode','claim_boundary':'Exact package structure/bytes/static bindings; this check does not execute the Mac app or qualify paid providers'}))
if __name__=='__main__':
 try:main()
 except Exception as error:print('VERIFY FAIL: '+str(error),file=sys.stderr);raise SystemExit(1)
