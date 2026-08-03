# Rebuild the guarded private kit and compare every delivered byte.

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAME = 'omniview-looking-glass'
VERSION = '0.1.0'
KIT = ROOT / 'release' / f'{NAME}-{VERSION}-private-preview'
BUILDER = ROOT / 'scripts' / 'build_private_kit.py'


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot() -> dict[str, str]:
    return {
        path.relative_to(KIT).as_posix(): sha256(path)
        for path in sorted(item for item in KIT.rglob('*') if item.is_file())
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify deterministic private-kit output')
    parser.add_argument('--gl4ss-root', type=Path, required=True)
    args = parser.parse_args()

    if not KIT.is_dir():
        print(json.dumps({'check': 'private-kit-determinism', 'status': 'FAIL', 'error': 'initial kit is missing'}))
        return 1
    before = snapshot()
    completed = subprocess.run(
        [sys.executable, '-X', 'utf8', str(BUILDER), '--gl4ss-root', str(args.gl4ss_root)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding='utf-8',
        check=False,
    )
    after = snapshot() if KIT.is_dir() else {}
    changed = sorted(set(before) ^ set(after))
    changed.extend(
        relative for relative in sorted(set(before) & set(after))
        if before[relative] != after[relative]
    )
    status = 'PASS' if completed.returncode == 0 and not changed else 'FAIL'
    print(
        json.dumps(
            {
                'check': 'private-kit-determinism',
                'status': status,
                'files': len(after),
                'changed': changed,
                'builder_exit_code': completed.returncode,
                'builder_stdout': completed.stdout,
                'builder_stderr': completed.stderr,
            },
            indent=2,
        )
    )
    return 0 if status == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
