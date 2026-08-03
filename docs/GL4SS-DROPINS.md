# Apply the GL4SS Drop-ins

These two patches upgrade the planner-to-render relay inside Pliny the Liberator's existing GL4SS application. They are a maintainer handoff, not an agent skill and not a replacement application.

## Frozen target

| Field | Required value |
|---|---|
| Repository | `https://github.com/elder-plinius/GL4SS` |
| Commit | `ab4984597ecf3afbd8ea66309be5ed68ce429146` |
| License custody | `AGPL-3.0-or-later` |
| Planner patch SHA-256 | `7b6d98fe6755e77e0db6c731d1845236dc6eb6770aac90f90790bf016b51ff7f` |
| Renderer patch SHA-256 | `42936c0e11cbbe628a82525021dda3d5963d6987ac449daf813053f1d28565b1` |

The assembled private kit places the files under:

    gl4ss-dropins/planner/0001-witness-shot-relay.patch
    gl4ss-dropins/renderer/0002-material-photograph-relay.patch

Apply them only to a clean, disposable checkout of the frozen commit. Preserve your working branch before beginning.

## Check the target and patch bytes

From the GL4SS checkout:

    git status --short
    git rev-parse HEAD

The status output should be empty and the commit should match [Frozen target](#frozen-target).

On Windows PowerShell, inspect the patches with:

    Get-FileHash -Algorithm SHA256 -LiteralPath path\to\0001-witness-shot-relay.patch
    Get-FileHash -Algorithm SHA256 -LiteralPath path\to\0002-material-photograph-relay.patch

Compare both values with the frozen-target table before applying either patch.

## Check, then apply in order

Use the paths for your unpacked kit:

    git apply --check path/to/0001-witness-shot-relay.patch path/to/0002-material-photograph-relay.patch
    git apply path/to/0001-witness-shot-relay.patch
    git apply path/to/0002-material-photograph-relay.patch

`git apply --check` should exit successfully without changing files. If it reports a context mismatch, stop: the checkout or patch bytes differ from the frozen target.

Do not force the patches onto another commit. Rebase the proposal deliberately and requalify it instead.

If the first patch applies but the second patch fails or the process is interrupted, stop. Inspect `git status --short` and do not build from an uncertain partial state. Discard the disposable candidate, or reverse only the patch that actually applied before trying again.

## Build and lint the candidate

Use the package manager and lockfile already present in GL4SS:

    npm ci
    npm run build
    npm run lint

The qualified candidate passed both commands at the frozen commit. Its build retained the existing Vite warning for a minified chunk larger than 500 kB. Passing locally confirms integration on your checkout; it does not establish provider or rendered-image behavior.

## What changes

The planner patch replaces the accumulated instruction stack in `buildSceneDirectionPrompt` with six enacted observations:

1. support;
2. ground;
3. presence;
4. time;
5. scene;
6. light.

The renderer patch keeps GL4SS's deterministic compiler and editable-template contract. It weaves existing facts into one material photograph or cinematic scene through habitation, material time, biome, hour, viewpoint, and sound.

The patches preserve the existing provider, engine, storage, user interface, model-call count, dependencies, and public TypeScript contracts.

The existing unknown-habitation parser behavior also remains: it warns and continues without marking fallback. That residual is intentionally outside this two-patch proposal.

## Verify the bounded integration

The kit includes the same deterministic candidate verifier used for the retained local receipt:

    node gl4ss-dropins/tests/verify-candidate.mjs --control path/to/pristine/GL4SS --candidate path/to/patched/GL4SS

The control checkout must remain pristine at the frozen commit. The candidate must contain exactly the intended patch result. A passing verifier establishes the checked contracts and runtime cases; read [Verification summary](../customer-kit/VERIFICATION-SUMMARY.md) for its exact scope.

## Reverse the patches

If both patches applied cleanly and you have made no overlapping edits, reverse them in the opposite order:

    git apply --reverse path/to/0002-material-photograph-relay.patch
    git apply --reverse path/to/0001-witness-shot-relay.patch

Then inspect:

    git status --short

For the safest recovery, discard the disposable candidate and return to the preserved clean checkout. Do not use a broad reset against a checkout that contains work you need.

No image or video provider was called during qualification. Rendered improvement and cross-model portability remain hypotheses for a separately authorized A/B.
