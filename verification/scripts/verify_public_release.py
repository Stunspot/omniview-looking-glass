# Verify the assembled OmniView public release.

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
NAME = 'omniview-looking-glass'
VERSION = '0.1.1'
RUNTIME_VERSION = '0.1.0'
KIT = ROOT / 'release' / f'{NAME}-{VERSION}'
ARCHIVE = ROOT / 'release' / f'OmniView-v{VERSION}.zip'
CANONICAL = ROOT / 'plugins' / NAME / 'skills' / NAME
CLAUDE = ROOT / 'dist' / 'claude-code' / NAME
TEXT_SUFFIXES = {'.md', '.txt', '.json', '.yaml', '.yml', '.mjs', '.patch'}
PRIVATE_MARKERS = ('c:/users/', 'c:\\users\\', 'e:/github/', 'e:\\github\\',
                   'e:/indranet/', 'e:\\indranet\\')
LINK = re.compile(r'\[[^\]]+\]\(([^)]+)\)')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def files_under(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in sorted(item for item in root.rglob('*') if item.is_file())
    }


def verify_manifest(errors: list[str]) -> None:
    path = KIT / 'release-manifest.json'
    try:
        manifest = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f'unreadable release manifest: {exc}')
        return

    identity = (manifest.get('product'), manifest.get('version'), manifest.get('channel'))
    if identity != (NAME, VERSION, 'public-release'):
        errors.append(f'manifest identity mismatch: {identity}')
    if manifest.get('runtime_version') != RUNTIME_VERSION:
        errors.append('manifest runtime version mismatch')

    declared = {}
    for entry in manifest.get('payload', []):
        if not isinstance(entry, dict) or not isinstance(entry.get('path'), str):
            errors.append('manifest payload contains an invalid entry')
            continue
        declared[entry['path']] = entry

    actual = files_under(KIT)
    actual.pop('release-manifest.json', None)
    actual.pop('SHA256SUMS.txt', None)
    if set(declared) != set(actual):
        errors.append('manifest payload paths do not match the delivered payload')
        return

    for relative, path in actual.items():
        entry = declared[relative]
        if entry.get('bytes') != path.stat().st_size:
            errors.append(f'manifest byte count mismatch: {relative}')
        if entry.get('sha256') != sha256(path):
            errors.append(f'manifest digest mismatch: {relative}')


def verify_checksums(errors: list[str]) -> None:
    path = KIT / 'SHA256SUMS.txt'
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f'unreadable checksum file: {exc}')
        return

    declared = {}
    for line in lines:
        parts = line.split('  ', 1)
        if len(parts) != 2:
            errors.append(f'malformed checksum line: {line}')
            continue
        digest, relative = parts
        candidate = Path(relative)
        if candidate.is_absolute() or '..' in candidate.parts or '\\' in relative:
            errors.append(f'unsafe checksum path: {relative}')
            continue
        declared[relative] = digest

    actual = files_under(KIT)
    actual.pop('SHA256SUMS.txt', None)
    if set(declared) != set(actual):
        errors.append('checksum paths do not match delivered files')
        return
    for relative, path in actual.items():
        if declared[relative] != sha256(path):
            errors.append(f'checksum mismatch: {relative}')


def verify_host_artifacts(errors: list[str]) -> None:
    zip_path = KIT / 'claude' / f'{NAME}.zip'
    try:
        with zipfile.ZipFile(zip_path) as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                errors.append('Claude ZIP contains duplicate paths')
            for name in names:
                parts = Path(name).parts
                if not parts or parts[0] != NAME or '..' in parts or '\\' in name:
                    errors.append(f'unsafe or misplaced Claude ZIP path: {name}')
            zip_bytes = {
                Path(name).relative_to(NAME).as_posix(): archive.read(name)
                for name in names
                if Path(name).parts and Path(name).parts[0] == NAME
            }
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f'unreadable Claude ZIP: {exc}')
        return

    expected_paths = files_under(CLAUDE)
    expected = {relative: path.read_bytes() for relative, path in expected_paths.items()}
    if set(zip_bytes) != set(expected):
        errors.append('Claude ZIP paths do not match the portable distribution')
    else:
        for relative, data in expected.items():
            if zip_bytes[relative] != data:
                errors.append(f'Claude ZIP byte mismatch: {relative}')

    codex_paths = files_under(KIT / 'codex' / NAME)
    codex_portable = {
        relative: path.read_bytes()
        for relative, path in codex_paths.items()
        if not relative.startswith('agents/')
    }
    if set(codex_portable) != set(expected):
        errors.append('Codex portable paths do not match the Claude distribution')
    else:
        for relative, data in expected.items():
            if codex_portable[relative] != data:
                errors.append(f'Codex portable byte mismatch: {relative}')

    expected_top = {
        'CONTRIBUTING.md',
        'LICENSE.md',
        'LICENSES',
        'NOTICE.md',
        'SECURITY.md',
        'SUPPORT.md',
        'README.md',
        'RELEASE-NOTES.md',
        'SHA256SUMS.txt',
        'TRADEMARKS.md',
        'claude',
        'codex',
        'customer-kit',
        'docs',
        'gl4ss-dropins',
        'release-manifest.json',
    }
    actual_top = {path.name for path in KIT.iterdir()}
    if actual_top != expected_top:
        errors.append('public-release top-level layout mismatch')


def verify_text_boundaries(errors: list[str]) -> None:
    resolved_kit = KIT.resolve()
    for relative, path in files_under(KIT).items():
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f'unreadable delivered text {relative}: {exc}')
            continue

        lowered = text.lower()
        for marker in PRIVATE_MARKERS:
            if marker in lowered:
                errors.append(f'private path marker in {relative}: {marker}')

        if path.suffix.lower() != '.md':
            continue
        for raw in LINK.findall(text):
            destination = raw.strip().strip('<>')
            if not destination or destination.startswith('#'):
                continue
            if re.match(r'^[a-z][a-z0-9+.-]*:', destination, re.IGNORECASE):
                continue
            destination = unquote(destination.split('#', 1)[0])
            target = (path.parent / destination).resolve()
            try:
                target.relative_to(resolved_kit)
            except ValueError:
                errors.append(f'local link escapes kit in {relative}: {raw}')
                continue
            if not target.exists() and target.suffix.lower() == '.html':
                markdown_route = target.with_suffix('.md')
                if markdown_route.is_file():
                    target = markdown_route
            if not target.exists():
                errors.append(f'broken local link in {relative}: {raw}')


def verify_release_archive(errors: list[str]) -> None:
    try:
        with zipfile.ZipFile(ARCHIVE) as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                errors.append('release ZIP contains duplicate paths')
            archived = {}
            for name in names:
                path = Path(name)
                if not path.parts or path.parts[0] != KIT.name or '..' in path.parts or '\\' in name:
                    errors.append(f'unsafe or misplaced release ZIP path: {name}')
                    continue
                archived[path.relative_to(KIT.name).as_posix()] = archive.read(name)
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f'unreadable release ZIP: {exc}')
        return

    expected = {relative: path.read_bytes() for relative, path in files_under(KIT).items()}
    if set(archived) != set(expected):
        errors.append('release ZIP paths do not match the assembled release')
        return
    for relative, data in expected.items():
        if archived[relative] != data:
            errors.append(f'release ZIP byte mismatch: {relative}')

def main() -> int:
    errors = []
    if not KIT.is_dir():
        errors.append(f'public release is missing: {KIT}')
    else:
        verify_manifest(errors)
        verify_checksums(errors)
        verify_host_artifacts(errors)
        verify_text_boundaries(errors)
        verify_release_archive(errors)

    if errors:
        print(json.dumps({'check': 'public-release', 'status': 'FAIL', 'errors': errors}, indent=2))
        return 1
    print(
        json.dumps(
            {
                'check': 'public-release',
                'status': 'PASS',
                'files': len(files_under(KIT)),
                'claim_boundary': (
                    'Delivered-byte, topology, checksum, parity, privacy-marker, '
                    'and local-link checks only; no live-host or provider claim.'
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
