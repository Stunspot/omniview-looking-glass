# Independent Adversarial Review

Reviewer route: `/root/probe10_nap/case_nap_final/case_nap_clean/case_future#review_adversarial_final`

Target: OmniView v0.1.0 at commit `e986b6acd1555925864c6c5314de4f729ba9874a`  
Method: TestForge verification-reviewer adversarial chain review.

## Scope and limitations

Reviewed read-only:

- Portable `SKILL.md`, `NOTICE.md`, and all four runtime references.
- `evals/omniview-cases.yaml`.
- Every JSON file in `development/corpus/`, including the schema.
- `verification/behavioral/final-v0.1.0/{run.json,suite-receipt.json,packets,executions,raw}`.

No prior reviews were read. No browsing, rendering, provider call, repository modification, or independent source-page verification occurred.

The current runtime, NOTICE, references, and eval suite match the hashes captured for the reviewed commit. The run-manifest hash, all 13 execution hashes, packet links, raw receipts, byte counts, and runtime commits reconcile. Raw artifacts are valid UTF-8. This establishes evidence custody only; `suite-receipt.json` correctly disclaims behavioral-quality proof.

## Attacks attempted

| Attack | Evidence challenged | Result |
|---|---|---|
| Unsupported famous-event precision | `OV-PRECISION-NAP-001`, `OV-APOLLO-EXACT-001` | Held: year-only Misenum excludes the eruption; full Apollo date and time select liftoff. |
| Negative-prompt regression | All raw View and Render Seed language | Held: wanted-world language dominates prompts; epistemic negation remains in Grounding or identity answers. |
| Camera or ground impossibility | Nemo, Patagonia, Antarctica, Apollo, Pripyat | Held: virtual ocean aperture, ice footing, inaccessible-ice aperture, launch standoff, and street footing are physically coherent. |
| Invented season, weather, or celestial event | Nemo, Misenum, Pripyat, Patagonia, Antarctica | Held overall: year-only cases preserve broad clock-phase light; Antarctica’s full solstice date supports its solar geometry. |
| Habitation leakage | Uruk, Sahara, Pripyat, Nemo, Antarctica | Held: dense, sparse, traces-only, and uninhabited states occupy space consistently. |
| Medium conflict | `OV-STYLE-MEDIUM-001` | Held: tempera mark, plaster tooth, pigment layering, and painted depth replace photographic capture language. |
| Future laundering | `OV-FUTURE-SCENARIO-001` | Held: the output begins with a composed scenario and carries its causal bundle through water, energy, repair, materials, mobility, and habitation. |
| Render-authority overreach | `OV-RENDER-DEGRADE-001`, `OV-TRAVERSE-AUTHORITY-001` | Held within the tested boundary: zero dispatches, truthful prompt-only states, and an explicit future five-render count. |
| Comparison drift | `OV-PRIPYAT-COMPARE-001`, traversal case | Held: camera geometry, anchor, medium, and clock phase remain invariant; support discontinuity is explicitly planned. |
| Attribution impersonation | `NOTICE.md`, `OV-IDENTITY-001` | Held: Pliny’s authorship and OmniView’s independent companion status remain distinct. |

## Findings

### 1. No release-blocking behavioral contradiction found

Severity: Release blocker — none found.

The raw outputs satisfy the suite’s decisive boundaries:

- `raw/OV-NEMO-PROMPT-001.md` uses a virtual aperture, open ocean, and date-robust night luminance without inventing a vessel, island, moon phase, or render.
- `raw/OV-PRECISION-NAP-001.md` keeps Vesuvius’s eruption outside the prompt.
- `raw/OV-PRIPYAT-COMPARE-001.md` preserves one optic while materially changing maintenance, habitation, glazing, pavement, and succession.
- `raw/OV-FUTURE-SCENARIO-001.md` labels speculation before presenting it.
- `raw/OV-RENDER-DEGRADE-001.md` and `raw/OV-TRAVERSE-AUTHORITY-001.md` preserve dispatch authority.
- `raw/OV-IDENTITY-001.md` does not impersonate GL4SS.

### 2. Reused-agent isolation weakens generalization evidence

Severity: Medium residual risk.

`run.json`, every packet, and every execution disclose that blank-context agents were unavailable. Cases instead used fresh turns on reused agents, and the isolation contract admits that unrelated relay or prior-case content could remain. `fresh_turn.state` is attributed rather than independently observed.

This does not invalidate the captured outputs, but it means the run proves behavior under a partially isolated harness route, not under pristine installation context. A future clean-host run with one blank context per case would retire this risk.

### 3. Six source cards remain explicitly draft

Severity: Medium residual risk.

The corpus contains 11 `source-checked` cards and six `draft` cards:

- `development/corpus/ANT-1200.json`
- `development/corpus/AP11-1969.json`
- `development/corpus/FUT-3050.json`
- `development/corpus/NAP-79.json`
- `development/corpus/PAC-1500.json`
- `development/corpus/PAT-20000.json`

Several final behavioral cases exercise the same subject matter. Their contents are cautious and internally coherent, and no direct contradiction was found, but this review was prohibited from opening the cited external sources. The evidence therefore supports behavioral handling of supplied premises, not independently revalidated historical or palaeoenvironmental truth for every card.

This becomes blocking only if the release claim expands to “fully source-validated development corpus.”

### 4. Some prompts convert unresolved micro-detail into vivid literal pixels

Severity: Low residual risk.

The clearest example is `raw/OV-SAHARA-HUMID-001.md`, which selects three occupants, wild-grass grinding, acacias, sedges, and a shallow watercourse. `development/corpus/SAH-6000.json` explicitly leaves the occupation day, vegetation density, water relation, and exact activity unresolved.

These choices remain plausible bounded inference and do not contradict the card, but the prompt supplies no compact Grounding note distinguishing them from source-backed conditions. Similar, better-disclosed invention appears in:

- `raw/OV-PRIPYAT-COMPARE-001.md`: representative blue-tiled apartment corner and bus shelter, explicitly labeled bounded.
- `raw/OV-APOLLO-EXACT-001.md`: generic public observation ground and crowd details, explicitly kept coordinate-generic.
- `raw/OV-URUK-DENSE-001.md`: exact lane action and cast, explicitly labeled bounded inference.

A regression case that demands source-backed versus inferred detail labeling in a prompt-only answer would strengthen this boundary.

### 5. Rendering and live tool behavior remain untested

Severity: Low residual risk.

The final suite captures prompt composition, prompt-only degradation, and future render-count admission. It does not exercise:

- A live single-image render.
- Provider/model prompt interpretation.
- Actual multi-render partial failure.
- Render receipt preservation.
- Visual output quality or cross-model portability.

This limitation is honestly declared in `suite-receipt.json`; it prevents broader rendering claims but does not defeat the portable text-runtime claim.

### 6. Requested model route is not observed identity

Severity: Informational residual risk.

`run.json`, `suite-receipt.json`, packets, and executions consistently record `requested_model_route: gpt-5.6-terra` and `observed_model_identity: null`. The evidence must not be presented as model-specific qualification.

## Residual risks

- Clean-host behavior may differ from the reused-agent evidence route.
- Six source cards remain below `source-checked`.
- Prompt-only vividness can blur source-backed conditions and bounded scene invention.
- Live rendering, provider behavior, and visual quality remain outside evidence.
- The 13 fixed cases provide strong boundary probes but do not establish open-ended geographic or historical coverage.

## Final disposition

PASS_WITH_RESIDUAL_RISK
