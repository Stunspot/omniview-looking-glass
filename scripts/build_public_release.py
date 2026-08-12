"""Build the deterministic OmniView public release."""
import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = 'omniview-looking-glass'
VERSION = '0.1.1'
RUNTIME_VERSION = '0.1.0'
LABEL = f'{NAME}-{VERSION}'
RELEASE_ROOT = ROOT / 'release'
OUTPUT = RELEASE_ROOT / LABEL
ARCHIVE = RELEASE_ROOT / f'OmniView-v{VERSION}.zip'
FROZEN_GL4SS_COMMIT = 'ab4984597ecf3afbd8ea66309be5ed68ce429146'
FROZEN_GL4SS_LICENSE_SHA256 = (
    '1aa87fff0d0a5174f43259c320b7082de75698c6628bd5cdaa9c9fff533e126f'
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def copy_tree(source: Path, target: Path) -> None:
    if not source.is_dir():
        raise FileNotFoundError(source)
    for path in sorted(item for item in source.rglob('*') if item.is_file()):
        copy_file(path, target / path.relative_to(source))


def git_value(*args: str) -> str:
    completed = subprocess.run(
        ['git', *args],
        check=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
    )
    return completed.stdout.strip()


def prepare_output() -> None:
    resolved_release = RELEASE_ROOT.resolve()
    resolved_output = OUTPUT.resolve()
    if resolved_output.parent != resolved_release or resolved_output.name != LABEL:
        raise RuntimeError(resolved_output)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)


def assert_source_clean() -> None:
    status = git_value(
        '-C', str(ROOT), 'status', '--porcelain=v1', '--untracked-files=all'
    )
    outside_release = [
        line for line in status.splitlines() if not line[3:].startswith('release/')
    ]
    if outside_release:
        raise RuntimeError('commit source changes before building')


def build_claude_zip() -> None:
    source = ROOT / 'dist' / 'claude-code' / NAME
    target = OUTPUT / 'claude' / f'{NAME}.zip'
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(item for item in source.rglob('*') if item.is_file()):
            relative = Path(NAME) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def copy_payload(gl4ss_root: Path) -> None:
    license_path = gl4ss_root / 'LICENSE'
    if git_value('-C', str(gl4ss_root), 'rev-parse', 'HEAD') != FROZEN_GL4SS_COMMIT:
        raise RuntimeError('GL4SS checkout is not at the frozen commit')
    if sha256(license_path) != FROZEN_GL4SS_LICENSE_SHA256:
        raise RuntimeError('GL4SS license bytes do not match the frozen target')

    copy_file(ROOT / 'README.md', OUTPUT / 'README.md')
    copy_file(ROOT / 'RELEASE-NOTES.md', OUTPUT / 'RELEASE-NOTES.md')
    copy_file(ROOT / 'CONTRIBUTING.md', OUTPUT / 'CONTRIBUTING.md')
    copy_file(ROOT / 'LICENSE.md', OUTPUT / 'LICENSE.md')
    copy_file(ROOT / 'NOTICE.md', OUTPUT / 'NOTICE.md')
    copy_file(ROOT / 'SECURITY.md', OUTPUT / 'SECURITY.md')
    copy_file(ROOT / 'SUPPORT.md', OUTPUT / 'SUPPORT.md')
    copy_file(ROOT / 'TRADEMARKS.md', OUTPUT / 'TRADEMARKS.md')
    copy_tree(ROOT / 'customer-kit', OUTPUT / 'customer-kit')
    copy_tree(ROOT / 'docs', OUTPUT / 'docs')
    copy_tree(
        ROOT / 'plugins' / NAME / 'skills' / NAME,
        OUTPUT / 'codex' / NAME,
    )
    build_claude_zip()

    copy_file(ROOT / 'LICENSES' / 'README.md', OUTPUT / 'LICENSES' / 'README.md')
    copy_file(
        ROOT / 'LICENSE.md',
        OUTPUT / 'LICENSES' / 'OMNIVIEW-SPLIT-LICENSE.md',
    )
    copy_file(license_path, OUTPUT / 'LICENSES' / 'GL4SS-AGPL-3.0.txt')

    dropin_files = (
        'README.md',
        'integration/dropin-manifest.json',
        'integration/gl4ss-baseline.json',
        'planner/0001-witness-shot-relay.patch',
        'planner/README.md',
        'renderer/0002-material-photograph-relay.patch',
        'renderer/README.md',
        'tests/verify-candidate.mjs',
    )
    for relative in dropin_files:
        copy_file(
            ROOT / 'dropins' / relative,
            OUTPUT / 'gl4ss-dropins' / relative,
        )


def payload_entries() -> list[dict[str, object]]:
    entries = []
    for path in sorted(item for item in OUTPUT.rglob('*') if item.is_file()):
        entries.append(
            {
                'path': path.relative_to(OUTPUT).as_posix(),
                'bytes': path.stat().st_size,
                'sha256': sha256(path),
            }
        )
    return entries


def write_manifest() -> None:
    manifest = {
        'schema_version': '1.0',
        'product': NAME,
        'version': VERSION,
        'runtime_version': RUNTIME_VERSION,
        'channel': 'public-release',
        'source_commit': git_value('-C', str(ROOT), 'rev-parse', 'HEAD'),
        'runtime_evidence_commit': 'e986b6acd1555925864c6c5314de4f729ba9874a',
        'behavior_payload_commit': '8a11716736321ea835091828ecd77cbbffb8243c',
        'behavior_custody_commit': '0049fdf21910fff738d32f070adabf7ef1e49df4',
        'gl4ss_target_commit': FROZEN_GL4SS_COMMIT,
        'claim_boundary': (
            'Public release bytes; no live-host install, discovery, invocation, '
            'image dispatch, or rendered-quality claim.'
        ),
        'payload': payload_entries(),
    }
    target = OUTPUT / 'release-manifest.json'
    target.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
        newline='\n',
    )


def write_checksums() -> None:
    target = OUTPUT / 'SHA256SUMS.txt'
    lines = []
    for path in sorted(item for item in OUTPUT.rglob('*') if item.is_file()):
        if path == target:
            continue
        relative = path.relative_to(OUTPUT).as_posix()
        lines.append(f'{sha256(path)}  {relative}')
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')


def build_release_archive() -> None:
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(item for item in OUTPUT.rglob('*') if item.is_file()):
            relative = Path(LABEL) / path.relative_to(OUTPUT)
            info = zipfile.ZipInfo(relative.as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description='Build the OmniView public release')
    parser.add_argument('--gl4ss-root', type=Path, required=True)
    args = parser.parse_args()

    assert_source_clean()
    prepare_output()
    copy_payload(args.gl4ss_root.resolve())
    write_manifest()
    write_checksums()
    build_release_archive()

    files = [path for path in OUTPUT.rglob('*') if path.is_file()]
    print(
        json.dumps(
            {
                'status': 'PASS',
                'output': OUTPUT.as_posix(),
                'archive': ARCHIVE.as_posix(),
                'files': len(files),
                'source_commit': git_value('-C', str(ROOT), 'rev-parse', 'HEAD'),
            },
            indent=2,
        )
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
