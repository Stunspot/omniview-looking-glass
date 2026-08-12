# Run the installed Hesperos Markdown linter once per customer document.

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = (
    'README.md',
    'CONTRIBUTING.md',
    'NOTICE.md',
    'SECURITY.md',
    'SUPPORT.md',
    'TRADEMARKS.md',
    'LICENSES/README.md',
    'customer-kit/HOST-MATRIX.md',
    'customer-kit/PROVENANCE.md',
    'customer-kit/START-HERE.md',
    'customer-kit/VERIFICATION-SUMMARY.md',
    'docs/ACCESSIBILITY.md',
    'docs/GL4SS-DROPINS.md',
    'docs/INSTALLATION.md',
    'docs/LIFECYCLE.md',
    'docs/PACKAGE-REFERENCE.md',
    'docs/TROUBLESHOOTING.md',
    'docs/TRUST-PRIVACY-AND-LIMITS.md',
    'docs/USING-OMNIVIEW.md',
)


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify customer Markdown')
    parser.add_argument('--linter', type=Path, required=True)
    args = parser.parse_args()

    results = []
    for relative in DOCUMENTS:
        path = ROOT / relative
        completed = subprocess.run(
            [sys.executable, '-X', 'utf8', str(args.linter), str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
        )
        results.append(
            {
                'path': relative,
                'status': 'passed' if completed.returncode == 0 else 'failed',
                'exit_code': completed.returncode,
                'stdout': completed.stdout,
                'stderr': completed.stderr,
            }
        )

    failed = [result['path'] for result in results if result['status'] != 'passed']
    print(
        json.dumps(
            {
                'check': 'documentation-lint',
                'status': 'PASS' if not failed else 'FAIL',
                'files': len(results),
                'failed': failed,
                'results': results,
                'claim_boundary': 'Static Markdown lint only; no assistive-technology or user outcome claim.',
            },
            indent=2,
        )
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
