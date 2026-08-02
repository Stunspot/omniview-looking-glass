# Verification Scripts

Run from the repository root:

    python -X utf8 verification/scripts/verify_package.py
    python -X utf8 verification/scripts/verify_corpus.py
    node dropins/tests/verify-candidate.mjs --control E:\Github\GL4SS --candidate E:\Github\omniview-gl4ss-companion\.work\GL4SS

The first command validates plugin closure, manifests, runtime references, private-path exclusions, eval integrity, and byte parity between the canonical portable skill and the Claude/generic distribution.

The second validates every development source card against the Draft 2020-12 schema and checks that visible claims reference source identifiers present on the same card. It requires the Python jsonschema package.

The Node verifier checks the two GL4SS patches against the frozen pristine checkout and exercises the real candidate planner and compiler through the disposable clone. It requires that clone's locked npm dependencies.

These checks establish static package and candidate behavior only. They do not establish installation, discovery, implicit invocation, live Claude behavior, image-tool availability, provider compatibility, or rendered improvement.

