# OmniView — The Looking Glass Companion

> A wormhole camera is not a subject with a year stapled to it. It is a place to stand, a world to read, and a moment made visible.

OmniView turns natural requests such as “open a view onto Uruk around 3200 BC at first light” into grounded scene interpretations and image-ready prompts. When a host exposes an authorized image tool, OmniView can hand the prompt to it. When no image tool is available, the prompt remains the complete product rather than a consolation prize.

This public repository contains two separate handoffs:

1. **Two bounded GL4SS drop-ins.** They replace the planner and render-language seams inside Pliny the Liberator’s existing application without adding a model call, changing a public TypeScript contract, or redesigning GL4SS.
2. **The OmniView companion Augment.** It gives Codex or Claude an agent-operated wormhole camera for single views, comparisons, and temporal traversals.

Inspired by The Looking Glass / GL4SS by Pliny the Liberator; composed by stunspot and Nova.

OmniView is an independent Collaborative Dynamics companion, not an official, endorsed, upstream, or replacement GL4SS release.

## The semantic engine

OmniView performs seven linked acts:

1. **Locate** the actual place, temporal precision, local hour, medium, and requested operation.
2. **Ground** the land, water, ice, ecology, habitation, built world, and datable matter that the inputs earn.
3. **Witness** from physical footing, an afloat optic, a safe standoff, or an explicitly virtual aperture.
4. **Compose** one focal event through foreground, middle distance, far distance, material evidence, atmosphere, and light.
5. **Provoke** the image model with medium-native visual language instead of generic quality tags.
6. **Render or hand off** through an available host tool, or return a complete copy-ready prompt.
7. **Account** for uncertainty, scenario assumptions, tool state, and actual dispatch without fictional receipts.

The prompts describe the world the model should make. They do not spend their attention naming a museum of forbidden mistakes.

## What it handles

- Dense, sparse, traces-only, and ordinarily uninhabited scenes.
- Year-only dates without smuggling in famous events, seasons, moon phases, or exact weather.
- Full dates and times when they genuinely select an event or solar condition.
- Ocean, ice, inaccessible, and hazardous viewpoints without inventing a beach, road, or camera crew.
- Fixed-view comparisons that preserve the optic while the world changes.
- Text-first traversals with explicit render counts and authority boundaries.
- Declared future scenarios whose causal assumptions become visible in the frame.
- Photography, painting, and other requested media whose marks and materials change the composition itself.

## Start here

- Private handoff orientation: [customer-kit/START-HERE.md](customer-kit/START-HERE.md)
- Install the companion: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- Use natural requests: [docs/USING-OMNIVIEW.md](docs/USING-OMNIVIEW.md)
- Apply the GL4SS patches: [docs/GL4SS-DROPINS.md](docs/GL4SS-DROPINS.md)
- Recover from failures: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Understand trust boundaries: [docs/TRUST-PRIVACY-AND-LIMITS.md](docs/TRUST-PRIVACY-AND-LIMITS.md)
- Inspect the package: [docs/PACKAGE-REFERENCE.md](docs/PACKAGE-REFERENCE.md)
- Use the nonvisual path: [docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md)
- Inspect verification: [customer-kit/VERIFICATION-SUMMARY.md](customer-kit/VERIFICATION-SUMMARY.md)

## Source layout

- `plugins/omniview-looking-glass/skills/omniview-looking-glass/` — Codex-oriented portable skill source.
- `dist/claude-code/omniview-looking-glass/` — byte-matched Claude/generic skill distribution.
- `dropins/` — two AGPL-derived patches against the named GL4SS baseline.
- `development/corpus/` — versioned source cards used to challenge grounding behavior.
- `verification/` — deterministic checks, behavioral receipts, reviews, and custody evidence.
- `customer-kit/` and `docs/` — reader-centered handoff documentation.

## Evidence state

Observed locally:

- both patches apply together to GL4SS commit `ab4984597ecf3afbd8ea66309be5ed68ce429146`;
- the patched candidate builds and lints;
- the package verifier passes with 12 portable files and byte parity between distributions;
- all 17 source cards pass schema and internal-link checks;
- all 13 final behavioral cases pass their frozen oracles;
- independent behavioral, adversarial, and evidence-custody reviewers return `PASS_WITH_RESIDUAL_RISK`;
- behavioral evidence is anchored at commit `8a11716736321ea835091828ecd77cbbffb8243c` and sealed in commit `0049fdf21910fff738d32f070adabf7ef1e49df4`.

Not established:

- live Codex or Claude installation, discovery, or invocation;
- live image-tool dispatch, returned image custody, or provider compatibility;
- rendered superiority or cross-model visual quality;
- blank-context isolation or observed model identity for the behavioral suite;
- live-host and rendered-quality qualification beyond the retained evidence boundary.

Public version 0.1.0 uses the standard Collaborative Dynamics split license for original OmniView material, while the GL4SS-derived drop-ins remain AGPL-3.0-or-later. Publication does not imply upstream acceptance, installation, provider execution, or endorsement by Pliny.
