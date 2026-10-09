# Start Here

This complete0.3.0 kit includes a local camera, the agent companion and separate GL4SS maintainer patches. Choose the route matching your work.

Paths on this page are relative to this complete kit. Publicv0.1.1 remains historical and does not contain the current camera.

## Open the camera

Open `../codex/omniview-looking-glass/workspace/Open.cmd` on Windows. On macOS, first make `Open.command` executable and open it; on Linux run `python3 host.py` in that workspace directory. Python3.10 or newer is required. Keep every workspace asset in place.

Enter Place and Time. With `OPENAI_API_KEY` configured in the launching environment, **Create image** sends one request to OpenAI and may incur a charge; this quick path does not research historical sources. **Plan with my agent instead** starts the source-grounded route without provider dispatch. Read [Open workspace](../OPEN-WORKSPACE.md) for configuration, saved moments, recovery and return work.

## Door one: upgrade GL4SS without changing GL4SS

Use the two files under `../gl4ss-dropins/` when you want Pliny’s existing application to observe and compose more effectively while preserving its architecture.

The patches:

1. replace the accumulated planner prohibition stack with a positive witness performance;
2. make the deterministic renderer weave the existing facts into one material photograph or cinematic scene.

They do not add a model call, provider, dependency, storage layer, UI, or public TypeScript field.

Read [GL4SS drop-ins](../docs/GL4SS-DROPINS.md) before applying them.

## Door two: give an agent an OmniView

Use the companion when you want Codex or Claude to operate a wormhole camera directly.

- Codex folder: `../codex/omniview-looking-glass/`
- Claude ZIP: `../claude/omniview-looking-glass.zip`

Install only the artifact for your host. Then ask naturally:

> Open a view onto Uruk around 3200 BC at first light. Text and prompt only.

Or:

> Compare the same street-level view in central Pripyat at 14:00 in 1985 and 2020.

Or:

> Build a five-stop traversal of this coastline. Tell me the render count before using any image tool.

Read [Installation](../docs/INSTALLATION.md), [Using OmniView](../docs/USING-OMNIVIEW.md), and the [Package reference](../docs/PACKAGE-REFERENCE.md).

## What a healthy first result looks like

A useful OmniView response should:

- identify the requested place, date precision, local hour, operation, and medium;
- declare how the optic can physically or virtually occupy the viewpoint;
- make habitation, emptiness, work, materials, depth, atmosphere, and light visible;
- distinguish source-backed conditions from bounded inference and future scenario;
- return a complete prompt even when no image tool is available;
- report `prompt-only`, `host-rendered`, `render-failed`, or `source-unavailable` truthfully.

It should not infer a famous event from a year, invent land beneath an ocean coordinate, promise that remote geography proves universal absence, or claim a render merely because one was requested.

## Read the evidence at the right altitude

[Verification summary](VERIFICATION-SUMMARY.md) separates what was observed from what remains untested.

The short version:

- static package, corpus, patch, build, lint, and 13-case prompt behavior have local receipts;
- live host installation and live image generation do not;
- the three retained behavioral, adversarial, and evidence-custody reviewers returned `PASS_WITH_RESIDUAL_RISK`;
- no model-specific qualification is claimed because the behavioral route did not expose observed model identity.

## Relationship and license

Inspired by The Looking Glass / GL4SS by Pliny the Liberator; composed by stunspot and Nova.

The companion is independent and unofficial. Original OmniView software uses MIT, authored Augment material uses CC BY-ND 4.0, and the GL4SS-derived drop-in pack remains AGPL-3.0-or-later.

Read [Provenance](PROVENANCE.md) and [Trust, privacy, and limits](../docs/TRUST-PRIVACY-AND-LIMITS.md) before redistribution. The [Accessibility statement](../docs/ACCESSIBILITY.md) gives the nonvisual workflow and the current testing boundary.
