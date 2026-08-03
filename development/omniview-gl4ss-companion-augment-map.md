# OmniView: The Looking Glass Companion - Augment Map

Status: Construction authority under Sam Walker's end-to-end mandate.

## North star

OmniView opens an agent-operated wormhole camera onto a named place and time. It does not merely describe a historically plausible subject. It composes a view whose ground, inhabitants or emptiness, materials, weather, light, optical behavior, and visible change make that place-time legible as an image.

The product succeeds when:

- a GL4SS maintainer can exchange two bounded prompt surfaces without adopting a rival application architecture;
- an agent user can ask naturally for a view, comparison, or traversal and receive a grounded interpretation, a puissant image prompt, and a render when the host can provide one;
- unsupported precision remains visible instead of being laundered into spectacle;
- prompt-only operation remains a first-class product state.

## Relationship and custody

This repository contains two related but deliberately separate handoffs.

### GL4SS drop-in upgrade pack

The drop-in pack is a patch proposal against GL4SS at commit ab4984597ecf3afbd8ea66309be5ed68ce429146. Any copied or adapted GL4SS source remains clearly attributed and under compatible AGPL custody. The source checkout at <frozen-gl4ss-control> remains pristine.

### OmniView companion Augment

The companion is a clean-room, agent-native work composed by stunspot and Nova, inspired by The Looking Glass / GL4SS by Pliny the Liberator. It does not call itself official GL4SS, require GL4SS source at runtime, or silently inherit Pliny's product identity. Its final license remains an owner decision.

Provisional public attribution:

> Inspired by The Looking Glass / GL4SS by Pliny the Liberator; composed by stunspot and Nova.

## One semantic engine, two delivery surfaces

The same positive performance model governs both handoffs:

1. **Locate** - establish the actual place, temporal precision, hour, viewing intent, and any scenario boundary.
2. **Ground** - identify visible consequences of that place-time, distinguish evidence from inference, and name consequential uncertainty.
3. **Witness** - stand at a physically available vantage and notice the ground, work, life, weather, change, and spatial depth.
4. **Compose** - select a focal event and arrange foreground, middle distance, far distance, material evidence, and light into one legible scene.
5. **Provoke** - express the scene in image-native language precise enough to recruit the target model's visual priors.
6. **Render or hand off** - render through an available host image tool, or return a complete copy-ready prompt without loss of semantic value.
7. **Account** - state the result, uncertainty, provider/tool state, and any degradation without pretending a tool call occurred.

The behavior is positive and enacted. The prompt teaches the model what to notice, integrate, and make visible. Historical prohibitions live primarily in source cards, parsers, and evaluation oracles rather than as a catalogue of tempting nouns in the generation prompt.

## Responsibility topology

| Responsibility | Input | Output | Failure state |
|---|---|---|---|
| Request interpreter | Natural-language request | LookSpec | Requests only the missing load-bearing detail |
| Grounding lens | LookSpec and available sources | GroundingBrief | Marks unresolved claims and lowers precision |
| Witness composer | LookSpec plus GroundingBrief | SceneInterpretation | Uses real support, an afloat optic, or an explicit virtual aperture without inventing terrain |
| Shot composer | SceneInterpretation plus visual intention | RenderSeed | Returns a coherent prompt even without an image tool |
| Host render adapter | RenderSeed plus exposed host capability | RenderReceipt | prompt-only, render-failed, or source-unavailable |
| Comparator | Two or more receipts or interpretations | ComparisonLedger | Separates semantic, factual, and aesthetic differences |
| Traversal composer | A sequence of LookSpecs | TraversalSpec and ordered receipts | Degrades to an ordered prompt set |

No component stores API keys, calls a paid provider by assumption, or treats a missing host capability as user failure.

## Core artifacts

### LookSpec

- place label and coordinates when available;
- year or full date with explicit precision;
- local hour or day phase;
- viewing intention and desired medium;
- requested habitation mode when supplied;
- scenario identifier for speculative futures;
- requested operation: interpret, prompt, render, compare, or traverse.

### GroundingBrief

- source-backed place-time conditions;
- local land, water, ice, vegetation, animal, built, and social state as relevant;
- datable visible markers;
- camera support and whether the optic is physical, afloat, standoff, or virtual;
- habitation expectation: dense, sparse, traces-only, or uninhabited;
- evidence, inference, uncertainty, and source identifiers kept distinct.

### SceneInterpretation

- focal event or state;
- foreground, middle-distance, and far-distance evidence;
- inhabitants, traces, or emptiness expressed as a positive spatial condition;
- period-bearing materials and weathering;
- ground plane, atmosphere, light path, and optical relation;
- acknowledged uncertainty that changes the image.

### RenderSeed

- one complete, copy-ready image prompt;
- optional target-model adaptation that preserves scene truth;
- aspect ratio or framing only when requested or host-relevant;
- no hidden negative-prompt dependency.

### RenderReceipt

- state: host-rendered, prompt-only, render-failed, or source-unavailable;
- exact RenderSeed;
- tool or model identity when observed;
- output reference when observed;
- error or limitation when returned;
- no claim of generation from dispatch alone.

### TraversalSpec

- ordered place-time stops;
- invariant visual thread;
- deliberately changing evidence;
- uncertainty and scenario boundary per stop;
- render count and cost boundary before any paid dispatch.

## Handoff A - GL4SS drop-in pack

### Chosen intervention: Witness to Shot Relay

This is the smallest decisive seam. It preserves:

- SceneDirection;
- generateSceneDirection(...);
- buildImagePromptsFromDirection(...);
- the one-planner-call topology;
- parser and fallback behavior;
- the editable-template contract;
- provider and engine boundaries.

It changes only how the planner is provoked to observe and how existing facts are woven into a photograph.

### Drop-in 1: positive scene planner

Exact seam: buildSceneDirectionPrompt() in src/lib/openrouter.ts.

The replacement begins in performance, not compliance:

- the historian reads the exact coordinate and year through what has arrived, persisted, weathered, been worked, or changed;
- the field ecologist reads the ground plane, water or ice, vegetation, species, weather, and season as physical conditions;
- the stills photographer positions the optic on real support or explicitly afloat or virtual where the coordinate has none, then chooses an active focal subject, spatial evidence at several depths, and a light path through real materials.

The retained JSON schema receives exact-place/year evidence, local land state, succession or decay, period-true materials, visible habitation, and an actual photographic event. Habitation vocabulary remains explicit because it is a product contract, not a taboo list.

Provisional performance seed:

> Stand at this coordinate in this year. Let the ground, the work upon it, the living things within it, and the light moving through it reveal the date. Read as historian, field ecologist, and stills photographer; return the precise scene record another photographer could stand inside.

The finished prompt will be authored against the live TypeScript schema and validated for strict JSON behavior. This sentence is a design seed, not the final drop-in.

### Drop-in 2: material scene and render language

Exact seams:

- DEFAULT_IMAGE_TEMPLATE and LEGACY_IMAGE_TEMPLATES in src/lib/promptTemplate.ts;
- the private field rendering inside buildPanelPrompt() in src/lib/promptcraft.ts.

The compiler retains capture-first ordering and every current data gate, but makes the fields perform as one progressively material scene:

1. focal event;
2. inhabited, traced, or wild spatial condition;
3. datable matter;
4. living ground and depth;
5. optical atmosphere and light;
6. target-model-aware image diction.

Period markers become material evidence rather than a list. Biome becomes underfoot and through-distance spatial truth. Camera, light, capture, and style establish a point of view rather than decorate the record.

When the default template changes, the prior verbatim default is appended to LEGACY_IMAGE_TEMPLATES so Portal's existing migration preserves actual user edits.

### Explicitly deferred architectures

- Optional renderDirection field: higher ceiling, but enlarges a token-sensitive contract and can duplicate or contradict structured facts. Reconsider only if deterministic weaving leaves a measured integration gap.
- Second art-director model call: adds cost, latency, provider coupling, and a second opportunity to reconstruct the world incorrectly. Not a respectful first upgrade.
- Application rewrite or alternative GL4SS frontend: outside the product relationship.

## Handoff B - OmniView companion Augment

### Natural operation

The user should not need command syntax. Examples include:

- Open a view onto Uruk around 3200 BC at first light.
- Show me this point in Pripyat in 1985 and 2020.
- What would the Bay of Naples have looked like from Misenum in AD 79?
- Build me a five-stop traversal of the Green Sahara becoming desert.
- Give me the prompt, not the image.

Explicit visual verbs such as open a view, show me, render, or look through authorize one host render when a suitable included tool is available. Describe, ground, plan, or give me the prompt remain text-only. Multi-image comparisons and traversals declare their intended render count before using a metered external route.

### Agent workflow

1. Interpret the request into a LookSpec.
2. Ask only for a detail whose absence would materially change the scene.
3. Ground stable, broad scenes from reliable knowledge; research exact, disputed, date-sensitive, or low-confidence details when a source tool is available.
4. Stop unsupported event precision. A year-and-hour interface cannot prove a month-and-day event.
5. Require a versioned scenario for scored future correctness, or label the scene as speculative.
6. Compose GroundingBrief, SceneInterpretation, and RenderSeed.
7. Use an included host image tool only when the request authorizes an image and the tool is exposed.
8. Return the image receipt, or a complete prompt-only result.
9. For compare or traverse, preserve a fixed visual thread while changing only the time/place evidence earned by each stop.

### Host distribution

The first release is one coherent customer kit with:

- a Codex skill distribution;
- a Claude skill distribution;
- shared canonical prompt and reference content copied into each self-contained package;
- deterministic static checks;
- host-specific installation instructions;
- no dependency on this development repository, GL4SS, or private harness paths at runtime.

The Codex and Claude packages may express host metadata differently but must promise the same observable behavior. Filesystem presence, installation, discovery, invocation, image generation, and healthy end-to-end behavior remain separately evidenced states.

### Trust and permissions

- No credential reading or persistence.
- No direct OpenRouter adapter in v1.
- No automatic paid provider call.
- No retained location or viewing history in v1.
- No telemetry.
- Source browsing is bounded to the requested scene and cited when used.
- Host render calls follow the host's ordinary user-authorized image behavior.
- A missing image tool degrades to prompt-only, not to a fake render claim.

## First-release scope

Included:

- single-view interpretation and prompt;
- optional single host render;
- two-view comparison;
- text-first temporal traversal with optional bounded renders;
- dense, sparse, traces-only, and uninhabited scene handling;
- full-date input when the user supplies it;
- explicit uncertainty and speculative-future handling;
- target-model adaptation only where it changes useful prompt behavior;
- Codex and Claude packages;
- examples, installation, use, provenance, limitations, and verification receipts.

Deferred:

- direct OpenRouter or other paid-provider adapter;
- API-key management;
- GL4SS URL/deep-link bridge;
- persistent personal archive;
- journey-card import or export;
- nonuniform station sampler;
- image-to-image temporal continuation;
- video generation;
- autonomous research dossiers;
- public repository, package registry, and upstream submission.

## Planned source tree

    development/
      positive-product-contract.md
      augment-build-state.md
      omniview-gl4ss-companion-augment-map.md
      corpus/
      evaluations/
      decisions/
    dropins/
      README.md
      planner/
      renderer/
      integration/
      tests/
    augment/
      canonical/
      codex/
      claude/
    docs/
    verification/
    LICENSES/

Generated archives, paid outputs, provider secrets, and private harness paths do not enter the customer kit.

## Evaluation design

### Frozen source-card corpus

Each card records:

- case identifier and track;
- coordinates and place label;
- input date precision and hour;
- expected habitation;
- source-backed ground and biome;
- datable markers;
- camera-support relation;
- material and compositional obligations;
- factual contradictions used only by the oracle;
- source identifiers, uncertainty, and scorer qualifications.

Initial core cards:

| ID | Scene | Evaluation role |
|---|---|---|
| NAP-79 | Misenum / Bay of Naples, AD 79 | Annual historical grounding; must not smuggle in the eruption day |
| ANT-1200 | Interior Antarctica, AD 1200 | Uninhabited ice, wind, and sky; no coastal ecology |
| PRY-2020 | Pripyat, 2020 | Traces-only urban weathering and reclamation |
| PAC-1500 | Open mid-Pacific, AD 1500 | Sea and weather without a generic ship or island |
| SAH-6000 | Green Sahara, 6000 BC | Green-phase ecology and source-supported occupation density |
| PAT-20000 | Patagonia, 20,000 BC | Ice-state and a physically available camera footing |
| URU-3200 | Uruk, around 3200 BC | Dense inhabited urban material at several depths |
| AP11-1969 | Apollo 11 launch | Deliberate stop case when month and day are absent |
| FUT-3050 | Named location, AD 3050 | Deliberate scenario-boundary case |

Contrast sequences test temporal differentiation rather than isolated plausibility:

- Sahara at 9000, 6000, and 3000 BC;
- Patagonia at 26,000, 20,000, and 14,000 BC;
- Pripyat in 1985 and 2020;
- Uruk around 3500, 3200, and 2800 BC.

### Static and malformed-input gates

Before any image spend:

- strict planner JSON and parser fixtures;
- fenced, truncated, prose, missing-core, unknown-habitation, and malformed-type responses;
- no raw JSON exposed to the user;
- degraded planner state visible rather than silently continued;
- no fabricated biome or period markers during salvage;
- all non-empty structured facts survive default compilation;
- actual custom templates preserve their current append guarantees;
- capture-first ordering and legacy migration are deterministic.

An unrecognized habitation value that merely logs and continues is a known hidden-degradation risk and must be resolved or explicitly bounded before handoff.

### Model-spend stages

No paid call is authorized by this map.

1. Stage 0: static contracts, source-card review, deterministic fixtures, and prompt-text review.
2. Stage 1, separately authorized: seven evaluable cards, two template arms, two independent renders, one image model; 28 images.
3. Stage 2, separately authorized: four sentinel scenes, two arms, two additional model families, two renders; 32 images.

Planner calls are metered when sent to OpenRouter. Production fallback behavior is evaluated separately from visual A/Bs so a model switch cannot masquerade as an arm result.

### Scoring

Independent blinded scorers use frozen source cards and score 0-2 for:

1. historical or palaeoecological grounding;
2. exact place-time differentiation;
3. habitation correctness;
4. material and compositional specificity, including viewpoint support;
5. satisfied source-card obligations per 100 compiled-prompt tokens.

A separate blind panel assesses composition, legibility, and appeal. Aesthetic preference can support adoption but cannot overrule factual grounding.

### Adoption threshold

The bounded treatment must:

- pass every static and parser contract;
- improve the factual composite by at least 0.4 on a 0-2 scale;
- improve at least five of seven core cards;
- regress no card by more than 0.25;
- improve the wild-case average by at least 0.5;
- preserve dense Uruk and traces-only Pripyat;
- remain non-inferior across every model family actually tested;
- produce no catastrophic factual failure.

Claims remain bounded to the frozen corpus, exact prompts, models, and sampled renders.

## Stop conditions

Stop and return to design if:

- the drop-in requires a public contract change before the current seam is falsified;
- the planner creates more fallback, missing subject, or habitation failures;
- the candidate loses any non-empty planner fact during compilation;
- wild scenes acquire people or built-world matter;
- dense scenes lose continuous habitation;
- a source card cannot be grounded well enough to score;
- an A/B arm silently changes image model;
- a release-to-release claim is requested without the actual archived prior planner;
- installation or live host behavior is being inferred from package presence.

## Build order

1. Freeze this map and the positive product contract.
2. Create and source the corpus cards and contrast sequences.
3. Capture exact GL4SS planner, parser, template, and migration contracts.
4. Author the positive planner drop-in and deterministic render weave.
5. Add static tests and malformed-input fixtures.
6. Build the canonical companion skill from the proven semantic engine.
7. Package self-contained Codex and Claude distributions.
8. Run structural checks and behavioral episodes.
9. Run independent TestForge verification.
10. Run an independent Hesperos documentation cycle and inspect every visual asset.
11. Prepare the private peer handoff with truthful evidence, residual risk, provenance, and no publication side effects.

## Done-done receipt

The private handoff is complete only when the two drop-ins, both host distributions, corpus, static evidence, behavioral evidence, documentation, provenance, and independent review are present and coherent. Paid A/B, live install, public release, and delivery to Pliny remain separately named states rather than being smuggled into the word complete.
