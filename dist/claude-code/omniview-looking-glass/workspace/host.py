"""Loopback workspace host. Records belong to the user, outside the installation."""
import argparse
import base64
import binascii
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE / 'domain.json').read_text(encoding='utf-8'))
PRODUCT = CONFIG['product']
MAX_IMAGE_BYTES = 30 * 1024 * 1024
IMAGE_MODEL = os.environ.get('OMNIVIEW_IMAGE_MODEL', 'gpt-image-2.5-flare')
IMAGE_TYPES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}

def read_local_image(reference):
    # Only an explicit absolute local file named by a saved record is eligible.
    # Avoid network paths, executable formats and arbitrary path query parameters.
    if not isinstance(reference, str) or reference.startswith(('\\\\', '//')):
        raise ValueError('The returned image must name an absolute local raster file.')
    path = Path(reference).expanduser()
    if not path.is_absolute():
        raise ValueError('The returned image must name an absolute local raster file.')
    path = path.resolve(strict=True)
    if str(path).startswith(('\\\\', '//')) or not path.is_file():
        raise ValueError('The returned image must name a local file, not a directory or network path.')
    kind = IMAGE_TYPES.get(path.suffix.lower())
    if not kind:
        raise ValueError('Only PNG, JPEG, GIF and WebP returned images can be displayed.')
    if path.stat().st_size > MAX_IMAGE_BYTES:
        raise ValueError('The returned image exceeds the 30 MB display limit.')
    with path.open('rb') as stream:
        data = stream.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError('The returned image exceeds the 30 MB display limit.')
    signatures = {
        'image/png': data.startswith(b'\x89PNG\r\n\x1a\n'),
        'image/jpeg': data.startswith(b'\xff\xd8\xff'),
        'image/gif': data.startswith((b'GIF87a', b'GIF89a')),
        'image/webp': len(data) >= 12 and data[:4] == b'RIFF' and data[8:12] == b'WEBP',
    }
    if not signatures[kind]:
        raise ValueError('The returned file content does not match its raster image type.')
    return data, kind

def render_prompt(record):
    seed = str(record.get('render_seed') or '').strip()
    if seed:
        return seed
    place = str(record['place']).strip()
    moment = str(record['time']).strip()
    light = str(record.get('hour') or '').strip()
    view = str(record.get('view') or '').strip()
    parts = [
        'Create one compelling, visually coherent landscape-format image: an imagined reconstruction of',
        f'{place} at {moment}.',
        'Show the actual place as it could plausibly have appeared then, with a clear foreground, middle distance, and horizon.',
        'Use physically convincing terrain, structures, material wear, human activity, and atmosphere appropriate to the stated place and period.',
        'Use an eye-level camera unless the scene requires another honest vantage.',
        'Avoid labels, captions, maps, split panels, and anachronistic spectacle.',
        'This is a visual interpretation, not a documentary photograph.'
    ]
    if light:
        parts.append('Local light: ' + light + '.')
    if view:
        parts.append('Requested scene: ' + view)
    if record.get('precision') == 'year':
        parts.append('The year alone does not establish season or exact weather; choose an ordinary plausible day.')
    return ' '.join(parts)


def generate_openai_image(prompt, key):
    payload = json.dumps({
        'model': IMAGE_MODEL, 'prompt': prompt, 'n': 1,
        'size': '1536x1024', 'quality': 'low', 'output_format': 'png'
    }).encode('utf-8')
    request = urllib.request.Request(
        'https://api.openai.com/v1/images/generations', data=payload,
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
        method='POST')
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read(43 * 1024 * 1024)
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read(4096)).get('error', {}).get('message', '')
        except (ValueError, AttributeError, TypeError):
            detail = ''
        raise ValueError('Image provider rejected the request' + (': ' + str(detail)[:400] if detail else '.') + ' (HTTP ' + str(error.code) + ').') from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise ValueError('The image request outcome is unknown after a connection failure. Do not immediately repeat it: inspect your collection and provider activity first; a request may have been processed.') from error
    try:
        encoded = json.loads(raw)['data'][0]['b64_json']
        image = base64.b64decode(encoded, validate=True)
    except (ValueError, KeyError, IndexError, TypeError, binascii.Error) as error:
        raise ValueError('Image provider returned no usable image.') from error
    if not image.startswith(b'\x89PNG\r\n\x1a\n') or len(image) > MAX_IMAGE_BYTES:
        raise ValueError('Image provider returned an unsupported or oversized image.')
    return image


def data_home():
    override = os.environ.get(CONFIG['home_env'])
    if override:
        return Path(override).expanduser().resolve()
    base = Path(os.environ.get('LOCALAPPDATA', str(Path.home() / ('Library/Application Support' if sys.platform == 'darwin' else '.local/share'))))
    return (base / 'Collaborative Dynamics' / PRODUCT).resolve()

def validate_data_home(home, root=None):
    home = Path(home).expanduser().resolve()
    root = Path(root or HERE.parent).resolve()
    boundaries = [root]
    for parent in root.parents:
        if parent == parent.parent:
            break
        repository = (parent / '.git').exists()
        release = any((parent / name).is_file() for name in ('RELEASE-MANIFEST.json', 'release-manifest.json'))
        plugin = any((parent / name / 'plugin.json').is_file() for name in ('.codex-plugin', '.claude-plugin'))
        if repository or release or plugin:
            boundaries.append(parent)
        if repository or release:
            break
    if any(home == boundary or boundary in home.parents for boundary in boundaries):
        raise ValueError('Choose a persistent data folder outside this source or installation. No folder was created.')
    return home

def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8') + b'\n'
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.write-', suffix='.tmp')
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def identity(home):
    return hashlib.sha256(str(home).encode()).hexdigest()

def validate(record):
    if not isinstance(record, dict):
        raise ValueError('A record must be a JSON object.')
    if not isinstance(record.get('title'), str) or not record['title'].strip():
        raise ValueError('Give the record a title.')
    if len(record['title']) > 500:
        raise ValueError('Title is too long.')
    for field in CONFIG['fields']:
        value = record.get(field['key'], '')
        if field.get('required') and not str(value).strip():
            raise ValueError(field['label'] + ' is required.')
        if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
            raise ValueError('Unsupported field value: ' + field['key'])
        if field.get('options') and value and value not in field['options']:
            raise ValueError('Invalid ' + field['label'])
    if len(json.dumps(record)) > 2_000_000:
        raise ValueError('Record exceeds the 2 MB limit.')

def serve(home, port):
    home.mkdir(parents=True, exist_ok=True)
    records = home / 'records'
    records.mkdir(exist_ok=True)
    token = secrets.token_urlsafe(32)
    instance_id = secrets.token_hex(16)
    lock = threading.RLock()
    rendering = set()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def reply(self, status, value, content_type='application/json'):
            data = json.dumps(value, ensure_ascii=False).encode() if content_type == 'application/json' else value
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)
        def auth(self):
            origin = self.headers.get('Origin')
            if origin and origin != f'http://127.0.0.1:{self.server.server_port}':
                self.reply(403, {'error': 'Foreign origin rejected.'})
                return False
            cookies = self.headers.get('Cookie', '')
            authorized = self.headers.get('X-Workspace-Token') == token or f'workspace={token}' in cookies.split('; ')
            if not authorized:
                self.reply(403, {'error': 'Open this workspace through its Open launcher.'})
            return authorized
        def do_GET(self):
            if self.path == '/health':
                return self.reply(200, {'product': PRODUCT, 'data_id': identity(home), 'instance': instance_id, 'pid': os.getpid()})
            if self.path.startswith('/open?token='):
                if not secrets.compare_digest(self.path.split('=', 1)[1], token):
                    return self.reply(403, {'error':'Invalid launch token.'})
                self.send_response(303)
                self.send_header('Set-Cookie', f'workspace={token}; HttpOnly; SameSite=Strict; Path=/')
                self.send_header('Location', '/')
                self.end_headers()
                return
            if not self.auth():
                return
            if self.path.startswith('/api/image/'):
                key = self.path[len('/api/image/'):]
                if len(key) != 24 or any(c not in '0123456789abcdef' for c in key):
                    return self.reply(400, {'error': 'Invalid saved view identity.'})
                try:
                    with lock:
                        record = json.loads((records / (key + '.json')).read_text(encoding='utf-8'))
                    if record.get('render_state') != 'host-rendered' or not record.get('output_reference'):
                        return self.reply(409, {'error': 'This saved view has no registered returned image.'})
                    data, kind = read_local_image(record['output_reference'])
                    return self.reply(200, data, kind)
                except FileNotFoundError:
                    return self.reply(404, {'error': 'The saved view or its returned image is unavailable.'})
                except (ValueError, OSError, RuntimeError) as error:
                    return self.reply(422, {'error': str(error)})
            if self.path == '/api/state':
                with lock:
                    values = []
                    for path in sorted(records.glob('*.json')):
                        try:
                            value = json.loads(path.read_text(encoding='utf-8'))
                            values.append(value)
                        except (ValueError, OSError):
                            return self.reply(500, {'error': 'Unreadable record: ' + path.name + '. Preserve it and repair the JSON.'})
                    return self.reply(200, {'records': values, 'config': CONFIG, 'data_home': str(home), 'render_ready': bool(os.environ.get('OPENAI_API_KEY')), 'render_model': IMAGE_MODEL})
            names = {'/native/omniview-32.png':'native/omniview-32.png', '/native/omniview-256.png':'native/omniview-256.png', '/':'index.html', '/app.js':'app.js', '/style.css':'style.css', '/assets/chronoscope.png':'assets/chronoscope.png', '/assets/pocket.png':'assets/pocket.png', '/assets/cinema.png':'assets/cinema.png'}
            if self.path not in names:
                return self.reply(404, {'error':'Not found'})
            path = HERE / names[self.path]
            kind = {'html':'text/html; charset=utf-8','js':'text/javascript; charset=utf-8','css':'text/css; charset=utf-8','png':'image/png'}[path.suffix[1:]]
            return self.reply(200, path.read_bytes(), kind)
        def do_POST(self):
            if not self.auth():
                return
            if self.path not in ('/api/record', '/api/render'):
                return self.reply(404, {'error':'Not found'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > 2_100_000:
                    raise ValueError('Request size must be between 1 byte and 2 MB.')
                request = json.loads(self.rfile.read(length))
                record = request['record']
                validate(record)
                if self.path == '/api/render':
                    key_secret = os.environ.get('OPENAI_API_KEY', '').strip()
                    if not key_secret:
                        return self.reply(409, {'error': 'Image rendering is not configured. Set OPENAI_API_KEY in the local host environment, restart OmniView, and try again.'})
                    prompt = render_prompt(record)
                    render_key = record.get('_id') or secrets.token_hex(12)
                    if not isinstance(render_key, str) or len(render_key) != 24 or any(c not in '0123456789abcdef' for c in render_key):
                        raise ValueError('Invalid record identity.')
                    with lock:
                        if render_key in rendering:
                            return self.reply(409, {'error': 'An image for this view is already rendering.'})
                        if record.get('_id'):
                            saved_path = records / (render_key + '.json')
                            previous = json.loads(saved_path.read_text(encoding='utf-8')) if saved_path.exists() else None
                            if not previous or request.get('revision') != previous['_revision']:
                                return self.reply(409, {'error': 'The view changed since you opened it. Reload before rendering.'})
                        rendering.add(render_key)
                    try:
                        image = generate_openai_image(prompt, key_secret)
                        with lock:
                            path = records / (render_key + '.json')
                            previous = json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
                            save_key = render_key
                            changed = previous and request.get('revision') != previous['_revision']
                            removed = not previous and record.get('_id')
                            if changed or removed:
                                # Retain the returned result without rewriting the owner's newer record.
                                record['render_recovery'] = {
                                    'source_record_id': render_key,
                                    'submitted_revision': request.get('revision'),
                                    'current_revision': previous['_revision'] if previous else None,
                                    'reason': 'changed-during-render' if changed else 'removed-during-render'
                                }
                                record['title'] = str(record.get('title') or 'Untitled view') + ' (recovered image)'
                                save_key = secrets.token_hex(12)
                                path = records / (save_key + '.json')
                                previous = None
                            images = home / 'images'
                            images.mkdir(exist_ok=True)
                            image_path = images / (save_key + '-' + secrets.token_hex(8) + '.png')
                            with image_path.open('xb') as stream:
                                stream.write(image)
                                stream.flush()
                                os.fsync(stream.fileno())
                            try:
                                record['render_seed'] = prompt
                                record['render_state'] = 'host-rendered'
                                record['render_host'] = 'OpenAI / ' + IMAGE_MODEL
                                record['output_reference'] = str(image_path)
                                record['operation'] = 'render'
                                if not record.get('evidence') and not record.get('scenario'):
                                    record['scenario'] = 'Quick image from place and time; no source research was performed by this workspace.'
                                record['_id'] = save_key
                                record['_revision'] = (previous['_revision'] if previous else 0) + 1
                                record['_updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                                record['_product'] = PRODUCT
                                validate(record)
                                if previous:
                                    atomic(home / 'history' / save_key / f'{previous["_revision"]}.json', previous)
                                atomic(path, record)
                            except Exception:
                                # Provider success is not undone by collection metadata failure.
                                return self.reply(500, {
                                    'error': 'The image was returned and retained at ' + str(image_path) +
                                             '. Saving its collection record failed. Preserve this file; after storage recovers, register it in Render handoff. Do not regenerate to recover this image.',
                                    'collection_saved': False,
                                    'render_state': 'host-rendered',
                                    'output_reference': str(image_path),
                                    'render_seed': prompt,
                                    'render_host': 'OpenAI / ' + IMAGE_MODEL
                                })
                            return self.reply(200, record)
                    finally:
                        with lock:
                            rendering.discard(render_key)
                with lock:
                    key = record.get('_id') or secrets.token_hex(12)
                    if not isinstance(key, str) or len(key) != 24 or any(c not in '0123456789abcdef' for c in key):
                        raise ValueError('Invalid record identity.')
                    path = records / (key + '.json')
                    previous = json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
                    if previous and request.get('revision') != previous['_revision']:
                        return self.reply(409, {'error':'The record changed since you opened it. Reload before saving.', 'current':previous})
                    if not previous and record.get('_id'):
                        raise ValueError('This record no longer exists. Import as a new record.')
                    record['_id'] = key
                    record['_revision'] = (previous['_revision'] if previous else 0) + 1
                    record['_updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    record['_product'] = PRODUCT
                    if previous:
                        atomic(home / 'history' / key / f'{previous["_revision"]}.json', previous)
                    atomic(path, record)
                    return self.reply(200, record)
            except (ValueError, KeyError, TypeError, OSError) as error:
                return self.reply(400, {'error': str(error)})
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    atomic(home / 'instance.json', {'product':PRODUCT, 'data_id':identity(home), 'port':server.server_port, 'token':token, 'instance':instance_id, 'pid':os.getpid()})
    try:
        server.serve_forever()
    finally:
        server.server_close()

def existing(home):
    try:
        meta = json.loads((home / 'instance.json').read_text(encoding='utf-8'))
        response = urllib.request.urlopen(f'http://127.0.0.1:{meta["port"]}/health', timeout=1)
        observed = json.load(response)
        if meta['product'] == PRODUCT and observed['product'] == PRODUCT and observed['data_id'] == identity(home) and observed['instance'] == meta['instance']:
            return meta
    except (OSError, ValueError, KeyError, urllib.error.URLError):
        pass
    return None

def launch(home, no_browser=False):
    home.mkdir(parents=True, exist_ok=True)
    meta = existing(home)
    if not meta:
        gate = home / 'launch.lock'
        for attempt in range(120):
            try:
                descriptor = os.open(gate, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(descriptor)
                break
            except FileExistsError:
                meta = existing(home)
                if meta:
                    break
                if time.time() - gate.stat().st_mtime > 30:
                    gate.unlink(missing_ok=True)
                time.sleep(.1)
        else:
            raise RuntimeError('Another launch is taking too long. Inspect workspace.log in the data folder.')
        if not meta:
            try:
                with (home / 'workspace.log').open('ab') as log:
                    subprocess.Popen([sys.executable, str(HERE / 'host.py'), '--serve', '--port', '0', '--data-home', str(home)], stdout=log, stderr=log, creationflags=(0x08000000 if os.name == 'nt' else 0), start_new_session=(os.name != 'nt'))
                for attempt in range(100):
                    meta = existing(home)
                    if meta:
                        break
                    time.sleep(.1)
                if not meta:
                    raise RuntimeError('Workspace did not start. Inspect workspace.log in the data folder.')
            finally:
                gate.unlink(missing_ok=True)
    url = f'http://127.0.0.1:{meta["port"]}/open?token={meta["token"]}'
    if not no_browser:
        webbrowser.open(url)
    print(json.dumps({'product':PRODUCT, 'url':url, 'data_home':str(home), 'pid':meta['pid']}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--data-home', type=Path)
    args = parser.parse_args()
    try:
        home = validate_data_home(args.data_home if args.data_home else data_home())
        serve(home, args.port) if args.serve else launch(home, args.no_browser)
    except Exception as error:
        print('Unable to open ' + PRODUCT + ': ' + str(error), file=sys.stderr)
        sys.exit(1)
