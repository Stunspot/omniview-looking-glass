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
actual_provider = host.generate_openai_image
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
    before_images = list((home / 'images').glob('*.png'))
    def concurrent_generate(prompt, key):
        updated = dict(first)
        updated['view'] = 'Newer owner edit while generation is in progress'
        post('/api/record', {'record': updated, 'revision': first['_revision']})
        calls.append((prompt, key))
        return PNG
    host.generate_openai_image = concurrent_generate
    recovered = post('/api/render', {'record': dict(first), 'revision': first['_revision']})
    assert recovered['_id'] != first['_id'] and recovered['_revision'] == 1
    assert recovered['render_recovery']['source_record_id'] == first['_id']
    assert recovered['render_recovery']['reason'] == 'changed-during-render'
    assert get('/api/image/' + recovered['_id']) == PNG
    outcome = {'http_status':200, 'recovered_id_is_separate':True, 'returned_image_served':True}
    state = json.loads(get('/api/state'))
    saved = next(x for x in state['records'] if x['_id'] == first['_id'])
    after_images = list((home / 'images').glob('*.png'))
    result = {'provider':'mocked; no paid request', 'provider_calls':len(calls), 'outcome':outcome, 'newer_view_preserved':saved.get('view'), 'record_revision':saved['_revision'], 'returned_second_image_retained':len(after_images)>len(before_images), 'image_files_before':len(before_images), 'image_files_after':len(after_images)}
    assert result['returned_second_image_retained'] and saved['_revision'] == 2
    assert saved['view'] == 'Newer owner edit while generation is in progress'
    print(json.dumps(result))

from unittest.mock import patch
with patch.object(host.urllib.request, 'urlopen', side_effect=urllib.error.URLError('simulated connection loss')):
    try:
        actual_provider('A fictional complete seed', 'qa-key-never-sent')
        raise AssertionError('Expected unknown-outcome error')
    except ValueError as error:
        message = str(error)
        assert 'outcome is unknown' in message and 'Do not immediately repeat' in message
        print('unknown provider outcome PASS: no automatic request retry or invented rejection')
