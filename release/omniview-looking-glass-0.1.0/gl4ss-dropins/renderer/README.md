# Drop-in 2: Material Photograph Relay

Target seams:

- DEFAULT_IMAGE_TEMPLATE and LEGACY_IMAGE_TEMPLATES in src/lib/promptTemplate.ts;
- still-prompt field rendering inside buildPanelPrompt() in src/lib/promptcraft.ts;
- buildCinematicPromptFromDirection() in src/lib/promptcraft.ts.

Patch: 0002-material-photograph-relay.patch  
SHA-256: 42936c0e11cbbe628a82525021dda3d5963d6987ac449daf813053f1d28565b1

## What it changes

The deterministic compiler now turns existing SceneDirection facts into one progressively material image:

1. capture behavior and viewpoint;
2. focal material in action;
3. inhabited, traced, or wild spatial condition;
4. datable matter, craft, use, weathering, or environmental state;
5. ground and living depth;
6. air, surface response, and light.

Period markers are introduced as evidence carrying the date. Biome becomes an underfoot-to-distance spatial instruction. Photographic behavior is expressed through grain, highlight shoulder, focus falloff, and unforced composition instead of generic quality tags.

The cinematic path now shares the still path's habitation gate, material-time language, biome, fixed hour, viewpoint, and local diegetic sound. It no longer drifts into a separate prompt doctrine.

## Template compatibility

The public PromptFields set is unchanged.

The new default only reorders and joins existing fields. The previous default is appended verbatim to LEGACY_IMAGE_TEMPLATES, preserving Portal's byte-sensitive migration behavior. Genuine custom templates remain untouched; when they omit habitation or period, the compiler retains GL4SS's existing bounded append behavior.

## Evidence boundary

The patch builds and lints in the disposable candidate. It has not been sent to an image or video model, so aesthetic or grounding improvement is not yet claimed as rendered fact.

