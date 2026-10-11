"""Exercise the local render boundary without making a provider call."""
import base64
import http.cookiejar
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import urllib.error
import urllib.request

HOST = Path(__file__).resolve().parents[2] / 'plugins/omniview-looking-glass/skills/omniview-looking-glass/workspace/host.py'
spec = importlib.util.spec_from_file_location('omniview_host', HOST)
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/uWQAAAAASUVORK5CYII=')
calls = []
def fake_generate(prompt, key):
    calls.append((prompt, key))
    return PNG
host.generate_openai_image = fake_generate
os.environ['OPENAI_API_KEY'] = 'qa-key-never-sent'

with tempfile.TemporaryDirectory() as folder:
    home = Path(folder)
    thread = threading.Thread(target=host.serve, args=(home, 0), daemon=True)
    thread.start()
    for _ in range(100):
        if (home / 'instance.json').exists():
            break
        time.sleep(.05)
    meta = json.loads((home / 'instance.json').read_text(encoding='utf-8'))
    base = 'http://127.0.0.1:' + str(meta['port'])
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    opener.open(base + '/open?token=' + meta['token'])
    def get(path):
        return opener.open(base + path).read()
    def post(path, body):
        request = urllib.request.Request(base + path, json.dumps(body).encode(), {'Content-Type':'application/json'}, method='POST')
        return json.load(opener.open(request))
    state = json.loads(get('/api/state'))
    assert state['render_ready'] is True
    record = {'title':'Venice · 1500', 'place':'Venice, Grand Canal', 'time':'1500', 'precision':'year', 'hour':'broad midday illumination'}
    first = post('/api/render', {'record':record, 'revision':0})
    assert first['render_state'] == 'host-rendered' and first['_revision'] == 1
    assert Path(first['output_reference']).exists() and first['render_seed'].find('Venice') >= 0
    assert 'no source research' in first['scenario']
    assert get('/api/image/' + first['_id']) == PNG
    assert len(calls) == 1 and calls[0][1] == 'qa-key-never-sent'
    try:
        post('/api/render', {'record':first, 'revision':0})
        raise AssertionError('Stale revision was accepted')
    except urllib.error.HTTPError as error:
        assert error.code == 409
    assert len(calls) == 1
    first['render_seed'] = 'A complete authored scene seed.'
    second = post('/api/render', {'record':first, 'revision':1})
    assert second['_revision'] == 2 and calls[-1][0] == first['render_seed']
    assert Path(second['output_reference']).exists()
    assert json.loads((home / 'history' / second['_id'] / '1.json').read_text(encoding='utf-8'))['_revision'] == 1
    del os.environ['OPENAI_API_KEY']
    state = json.loads(get('/api/state'))
    assert state['render_ready'] is False
    try:
        post('/api/render', {'record':record, 'revision':0})
        raise AssertionError('Unconfigured render was accepted')
    except urllib.error.HTTPError as error:
        assert error.code == 409
print('render flow PASS: configured, saved, served, stale blocked, authored seed, no-key blocked; provider mocked')
