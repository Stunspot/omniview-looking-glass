# GL4SS Witness-to-Shot Upgrade Pack

Two patches, one relay.

This pack is a bounded proposal for The Looking Glass / GL4SS by Pliny the Liberator. It changes how the existing planner observes a place-time and how the existing compiler turns that observation into still and cinematic language. It does not replace Pliny's application, add a model call, or alter its provider, engine, storage, UI, or public TypeScript contracts.

## Frozen target

- Repository: https://github.com/elder-plinius/GL4SS
- Commit: ab4984597ecf3afbd8ea66309be5ed68ce429146
- License: AGPL-3.0-or-later

Apply the patches in order:

1. planner/0001-witness-shot-relay.patch
2. renderer/0002-material-photograph-relay.patch

From a clean checkout of the frozen target:

    git apply --check /path/to/0001-witness-shot-relay.patch /path/to/0002-material-photograph-relay.patch
    git apply /path/to/0001-witness-shot-relay.patch
    git apply /path/to/0002-material-photograph-relay.patch
    npm ci
    npm run build
    npm run lint

The first patch replaces the accumulated prohibition stack inside buildSceneDirectionPrompt with an enacted observation sequence: support, ground, presence, time, scene, and light.

The second patch keeps GL4SS's deterministic compiler and editable-template contract while making its facts perform as one photograph. It also brings cinematic assembly back onto the same habitation, material-time, biome, hour, viewpoint, and sound logic as the still path.

## Evidence boundary

Observed against the frozen target in an ignored disposable clone:

- both patches apply together;
- extracted patch bytes exactly match the built candidate diff;
- TypeScript plus Vite production build passes;
- ESLint passes;
- the previous default image template is present byte-for-byte in LEGACY_IMAGE_TEMPLATES.

No provider, image, or video call was made. Rendered superiority and cross-model portability remain hypotheses until a separately authorized A/B.

The existing unknown-habitation parser behavior is intentionally unchanged: it warns and continues without marking fallback. That is a documented residual in this minimal two-patch treatment, not a silently claimed fix.

## Custody

These patches are derived from AGPL-covered GL4SS source and are kept under compatible custody. The companion Augment is a separate, agent-native work; this pack does not present it as an official GL4SS replacement.

