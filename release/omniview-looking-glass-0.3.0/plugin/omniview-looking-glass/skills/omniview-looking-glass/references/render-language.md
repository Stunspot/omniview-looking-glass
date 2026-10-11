# Render Language

Use this reference when the user wants a copy-ready prompt, a host render, a named image model, a non-photographic medium, a cinematic shot, or a scene whose first draft feels generic.

## The prompt is the image's attentional path

Write in the order the renderer should care:

1. medium and capture behavior;
2. focal event;
3. place and time;
4. positive habitation and spatial activity;
5. time-bearing materials and their state;
6. ground, ecology, and depth;
7. light through atmosphere and surfaces;
8. style and frame geometry.

The prompt is neither a database dump nor a bag of aesthetic tags. It is a controlled attentional path through one world.

Keep grounding notes outside the Render Seed. Sources can establish that the optic is on ice; the seed should say what the ice does under the camera and light. An oracle can know that a modern road is impossible; the seed should fill the frame with the period-correct surface that is actually there.

## Increase semantic resolution

Generic nouns invite the renderer's most common prior. Add the distinctions that change pixels:

- identity or type;
- material;
- construction;
- condition and wear;
- action;
- relation to another material;
- light response;
- spatial role.

Weak:

> Red-haired woman in historical clothes, cinematic, detailed.

Image-bearing:

> A Titian-haired Venetian dyer draws a length of madder-red silk from a steaming copper vat, linen sleeves twisted above the elbow, wet fibres blazing translucent where window light cuts through the workshop haze.

Weak:

> Ancient city market, busy, photorealistic.

Image-bearing:

> Porters pivot reed baskets around a fresh-plastered mudbrick corner while seal cutters and carriers converge beneath one cone-mosaic facade; packed earth shows dark wheelless drag marks, bodies overlap through the lane, and low morning sun turns suspended dust luminous between the walls.

The stronger versions do more than contain rarer words. Material, action, relation, depth, and light reinforce the same scene.

## Compose complete worlds

When a visual behavior matters, state the complete world that carries it.

Treat the user's correction as a private design signal. Resolve it into the positive objective below before drafting, then compose from the objective and its world.

| Visual objective | Positive world |
|---|---|
| Uninhabited frame | Wind, water, ice, terrain, sky, and the local life that enters the optic carry the complete frame |
| Date-bearing material world | Every visible material, joint, tool, garment, and maintained surface carries the craft and use of the requested date |
| Contemporary maintained structure | Fresh repair, intact rooflines, swept thresholds, active doors, stocked work surfaces, and ordinary use make the structure contemporary |
| Caught-in-motion composition | An unforced off-centre composition catches action already under way, with partial occlusion and uneven depth |
| Habitat-specific vegetation | Named plant forms occupy moisture, shade, bank, canopy, or disturbed ground according to the local habitat |
| Tension through relation | Held motion, watchfulness, crowd anticipation, guarded distance, and environmental consequence carry the tension |
| Open-ocean extent | Horizon-to-horizon water, open sky, cross-swell geometry, spray, and atmospheric distance fill every depth |
| Ordinary year-level moment | Intact landform, ongoing work, maintained structures, ordinary traffic, and date-robust clock-phase illumination carry the selected date |

The renderer receives wanted nouns and relations. Evaluator knowledge stays in Grounding.

Run the pixel test over the View and Render Seed: every world-object noun instantiates visible pixels, while camera and capture terms govern how those pixels appear. Each clause paints wanted matter, action, space, light, or capture behavior.

At the final affirmative-language gate, convert grammatical negation and comparative rejection into the visible incompatible world. Rerun the pixel test before returning the View or Render Seed.

## Photographic language

Use camera and capture language as physics, not status jewelry.

Useful controls include:

- viewpoint support, camera height, distance, and angle;
- depth relation and focal falloff;
- shutter consequence when motion matters;
- highlight shoulder, shadow grain, flare, halation, diffusion, or clean digital separation when the medium earns them;
- framing pressure, occlusion, horizon placement, and off-centre balance;
- aspect ratio when the host needs it.

Name a camera body, stock, process, or lens only when it recruits a useful and compatible image prior. The visual behavior matters more than the logo.

Example:

> A wide documentary photograph from a virtual aperture 1.5 metres above the swell. Fine grain sits in the dark water; deep ambient night luminance catches spray along a subdued highlight shoulder; focus loosens toward the atmospheric horizon; the crossing wave ridge lands left of centre as if caught in one unrepeatable lift.

For a drawn, painted, diagrammatic, collage, or print medium, replace photographic capture with the medium's actual mark, edge, layering, surface, and color behavior.

## Light is a verb

Connect source, atmosphere, material, and consequence.

Flat:

> Golden-hour cinematic lighting.

Operative:

> Low sun enters from camera right, skims the reed impressions in fresh plaster, fires the suspended dust between the walls, and leaves the packed lane in a long blue-violet shadow.

Useful light verbs include graze, transmit, rake, flare, pool, scatter, veil, silhouette, flash, bloom, glint, stain, and fall away. Choose the verb the surface and atmosphere can perform.

## Habitation must reach the edges

At **dense**, activity overlaps at several distances and built surroundings continue to the frame edges.

At **settled**, maintenance and ordinary use appear across near and middle distance.

At **sparse**, separated figures each perform a specific local task while ground and air remain visually dominant.

At **traces-only**, made matter and what time, weather, plants, animals, or sediment are doing to it become the action.

At **uninhabited**, terrain, water or ice, atmosphere, and genuinely present life form the complete event.

## Cinematic language

A cinematic seed adds time while preserving the same world:

- one focal event that can develop over the requested duration;
- one camera move physically compatible with the support;
- one change in occlusion, parallax, material stress, weather, work, or behavior;
- diegetic sound belonging to the habitation state.

At uninhabited, sound comes from wind, water, ice, weather, and present species. At traces-only, weather can act on made matter. Human task and crowd sounds arrive with sparse, settled, or dense habitation.

Keep the move readable:

> A slow lateral drift just above the swell reveals the second wave train crossing beneath the first; spray tears downwind past the aperture while the horizon remains level.

The clip is one developing physical relation, not a list of shots.

## Adapt to the target without losing the world

Default to portable natural language. When the user names a target model or host:

1. verify current prompt behavior when it is load-bearing and current documentation is available;
2. change syntax, weighting, length, aspect phrasing, or tool parameters only where the target benefits;
3. preserve the same support, ground, habitation, materials, event, and light;
4. label any unverified dialect choice as provisional.

Model portability is demonstrated only by observed outputs from the named versions. A prompt that reads well across vendors is a portable candidate, not proof of equal rendering.

## Final seed check

Before handoff, ask:

- Can the camera relation exist as declared?
- Does the first sentence carry the focal image?
- Does every named person, species, structure, and object belong to this place-time?
- Do two to four materials visibly carry the date?
- Does habitation occupy space rather than merely appear as a label?
- Do foreground, middle distance, and horizon share one event?
- Does light act through actual atmosphere and surfaces?
- Does every renderer-facing noun earn a wanted pixel?

Repair the first failed answer. Extra style words are the last move, not the first aid kit.
