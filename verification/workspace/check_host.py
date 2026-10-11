"""Exercise save, stale-save rejection, launcher reuse and restart against a disposable owner store."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
parser=argparse.ArgumentParser(); parser.add_argument('workspace',type=Path); args=parser.parse_args()
home=Path(tempfile.mkdtemp(prefix='cd-workspace-check-'))
def launch():
    return json.loads(subprocess.check_output([sys.executable,str(args.workspace/'host.py'),'--no-browser','--data-home',str(home)],text=True))
def api(meta, route, value=None):
    instance=json.loads((home/'instance.json').read_text())
    request=urllib.request.Request('http://127.0.0.1:'+str(instance['port'])+route,data=json.dumps(value).encode() if value else None,headers={'X-Workspace-Token':instance['token'],'Content-Type':'application/json'})
    with urllib.request.urlopen(request) as response:return json.load(response)
def stop(pid):
    if os.name=='nt': subprocess.run(['taskkill','/PID',str(pid),'/F'],capture_output=True,check=True)
    else: os.kill(pid,15)
meta=launch(); second=launch(); assert meta['pid']==second['pid']
record=api(meta,'/api/state')['config']['example']; record['_extra_preserved']={'owner':'example'}
saved=api(meta,'/api/record',{'record':record,'revision':0}); assert saved['_revision']==1
saved['title']+=' edited'; updated=api(meta,'/api/record',{'record':saved,'revision':1}); assert updated['_revision']==2
try: api(meta,'/api/record',{'record':saved,'revision':1}); raise AssertionError('Stale write accepted')
except urllib.error.HTTPError as error: assert error.code==409
stop(meta['pid']); time.sleep(.3); restarted=launch(); state=api(restarted,'/api/state'); assert state['records'][0]['_extra_preserved']=={'owner':'example'}; assert state['records'][0]['_revision']==2
assert (home/'history'/saved['_id']/'1.json').is_file()
stop(restarted['pid'])
print(json.dumps({'save':'pass','edit':'pass','stale_conflict':'pass','unknown_fields':'pass','launcher_reuse':'pass','restart_persistence':'pass','history':'pass','test_store':str(home)},indent=2))
