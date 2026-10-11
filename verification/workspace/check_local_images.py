"""Exercise authenticated local render preview against a disposable owner store."""
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
HOST = ROOT / 'plugins/omniview-looking-glass/skills/omniview-looking-glass/workspace/host.py'
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j1ioAAAAASUVORK5CYII=')

class LocalImageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='omniview-image-check-')
        cls.home = Path(cls.temporary.name)
        cls.process = subprocess.Popen([sys.executable, str(HOST), '--serve', '--port', '0', '--data-home', str(cls.home)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=(0x08000000 if os.name == 'nt' else 0))
        for _ in range(100):
            if (cls.home / 'instance.json').exists():
                cls.meta = json.loads((cls.home / 'instance.json').read_text())
                cls.base = 'http://127.0.0.1:' + str(cls.meta['port'])
                return
            if cls.process.poll() is not None:
                raise RuntimeError(cls.process.communicate()[1].decode())
            time.sleep(.05)
        raise RuntimeError('Image test host did not start.')

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.communicate(timeout=10)
        cls.temporary.cleanup()

    def request(self, route, value=None, authorized=True):
        headers = {'Content-Type': 'application/json'}
        if authorized:
            headers['X-Workspace-Token'] = self.meta['token']
        request = urllib.request.Request(self.base + route, data=json.dumps(value).encode() if value is not None else None, headers=headers)
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.headers.get('Content-Type'), response.read()
        except urllib.error.HTTPError as error:
            with error:
                return error.code, error.headers.get('Content-Type'), error.read()

    def save(self, reference='', state='host-rendered'):
        record = {'title': 'Local preview test', 'place': 'Test aperture', 'time': '1900', 'render_state': state, 'output_reference': str(reference), '_extension': {'preserved': True}}
        code, _, body = self.request('/api/record', {'record': record, 'revision': 0})
        self.assertEqual(code, 200, body)
        saved = json.loads(body)
        self.assertEqual(saved['_extension'], {'preserved': True})
        return saved['_id']

    def image(self, identity, authorized=True):
        return self.request('/api/image/' + identity, authorized=authorized)

    def test_png_round_trip_and_authentication(self):
        path = self.home / 'returned.png'
        path.write_bytes(PNG)
        identity = self.save(path)
        self.assertEqual(self.image(identity), (200, 'image/png', PNG))
        self.assertEqual(self.image(identity, authorized=False)[0], 403)

    def test_all_supported_raster_signatures(self):
        for suffix, data, mime in [('.jpg', b'\xff\xd8\xfffixture', 'image/jpeg'), ('.gif', b'GIF89afixture', 'image/gif'), ('.webp', b'RIFF0000WEBPfixture', 'image/webp')]:
            with self.subTest(suffix=suffix):
                path = self.home / ('returned' + suffix)
                path.write_bytes(data)
                self.assertEqual(self.image(self.save(path)), (200, mime, data))

    def test_unsaved_missing_and_invalid_identities(self):
        self.assertEqual(self.image('')[0], 400)
        self.assertEqual(self.image('f' * 24)[0], 404)
        for identity in ['../records/secret.json', 'x' * 24, 'a' * 24 + '?path=C:/secret.png']:
            with self.subTest(identity=identity):
                self.assertEqual(self.image(identity)[0], 400)

    def test_unrendered_and_missing_output(self):
        path = self.home / 'pending.png'
        path.write_bytes(PNG)
        for state in ['prompt-only', 'render-failed', 'source-unavailable']:
            self.assertEqual(self.image(self.save(path, state))[0], 409)
        self.assertEqual(self.image(self.save(''))[0], 409)
        self.assertEqual(self.image(self.save(self.home / 'missing.png'))[0], 404)

    def test_non_image_spoof_directory_remote_and_relative_paths(self):
        svg = self.home / 'returned.svg'
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        spoof = self.home / 'spoof.png'
        spoof.write_text('<script>bad()</script>')
        for reference in [svg, spoof, self.home, 'relative.png', 'https://example.com/image.png', r'\\localhost\share\image.png']:
            with self.subTest(reference=str(reference)):
                self.assertEqual(self.image(self.save(reference))[0], 422)

    def test_oversized_image(self):
        path = self.home / 'large.png'
        with path.open('wb') as stream:
            stream.write(PNG)
            stream.truncate(30 * 1024 * 1024 + 1)
        self.assertEqual(self.image(self.save(path))[0], 422)

if __name__ == '__main__':
    unittest.main(verbosity=2)
