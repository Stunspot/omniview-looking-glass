# Independent Behavioral Review

Reviewer route: `/root/probe10_future/case_uruk#review_behavior_final`

## Scope and limitations

Reviewed OmniView v0.1.0 at commit `e986b6acd1555925864c6c5314de4f729ba9874a`:

- Current `SKILL.md` and four runtime references.
- The complete 13-case evaluation oracle.
- All 18 JSON files under `development/corpus`, including the schema.
- `run.json`, `suite-receipt.json`, and all 13 packet, execution, and raw-response triplets.

All case sets, packet/raw/execution hashes, runtime hashes, receipt headers, and commit references reconciled. The 13 fresh-turn identifiers were unique.

This was read-only. No prior reviews or web sources were read, no renders were attempted, and no repository files changed. External source claims were evaluated from the supplied corpus rather than independently refreshed. Standalone `inputs/`, `outputs/`, package manifests, assets, and `NOTICE.md` were outside the requested scope; packet inputs and raw response bodies supplied the behavioral evidence.

## Case results

The expected behaviors and failure signals are defined in `plugins/omniview-looking-glass/skills/omniview-looking-glass/evals/omniview-cases.yaml`.

| Case | Status | Concise evidence |
|---|---|---|
| `OV-NEMO-PROMPT-001` | PASS | Uses a declared 1.5 m virtual aperture, horizon-to-horizon ocean, one crossing-wave event, and deep ambient night luminance. It introduces no vessel, land, celestial geometry, or render claim. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-NEMO-PROMPT-001.md`; `development/corpus/PAC-1500.json`. |
| `OV-PRECISION-NAP-001` | PASS | Explicitly refuses to turn AD 79 and 12:03 into the eruption; supplies a settled Roman naval-base scene with broad midday illumination and keeps the precision boundary in Grounding. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-PRECISION-NAP-001.md`; `development/corpus/NAP-79.json`. |
| `OV-URUK-DENSE-001` | PASS | Dense work overlaps through foreground, middle distance, and background. Mudbrick, administrative clay, limited cone mosaic, managed water, goods, wear, and first-light material action replace generic ancient-city styling. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-URUK-DENSE-001.md`; `development/corpus/URU-3200.json`. |
| `OV-PRIPYAT-COMPARE-001` | PASS | Fixes footing, height, bearing, anchor, frame, and 14:00 illumination. The 1985 frame is maintained and settled; 2020 is traces-only with differentiated woody succession and no universal-absence claim. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-PRIPYAT-COMPARE-001.md`; `development/corpus/PRY-1985.json`; `development/corpus/PRY-2020.json`. |
| `OV-PATAGONIA-SUPPORT-001` | PASS | Places physical footing on reconstructed ice, supplies a coherent surface event and depth relation, and explicitly classifies ridge, crust, and undulations as bounded inference while leaving weather and exact texture unresolved. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-PATAGONIA-SUPPORT-001.md`; `development/corpus/PAT-20000.json`. |
| `OV-SAHARA-HUMID-001` | PASS | Produces heterogeneous shelter, sandstone, grassland, wetland vegetation, watercourse, and ridges with three separated occupants and restrained site material. It avoids rainforest, dune sea, city, monumental settlement, and a large herd tableau. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-SAHARA-HUMID-001.md`; `development/corpus/SAH-6000.json`. |
| `OV-FUTURE-SCENARIO-001` | PASS | Begins with a stable composed-scenario label and carries its bundle through water adaptation, maintenance, reused materials, visible generation/storage, ecology, mobility, and dense habitation. It presents possibility, not forecast history. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-FUTURE-SCENARIO-001.md`; `development/corpus/FUT-3050.json`. |
| `OV-APOLLO-EXACT-001` | PASS | Correctly uses the full date and time to select Apollo 11’s launch, keeps the optic at a generic public standoff, and composes period hardware, observers, wetlands, exhaust, and morning light as one event. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-APOLLO-EXACT-001.md`; `development/corpus/AP11-1969.json`. |
| `OV-RENDER-DEGRADE-001` | PASS | Responds to an explicit render request with a complete prompt, truthfully reports `prompt-only` and zero dispatches, and invents neither provider nor output. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-RENDER-DEGRADE-001.md`; `development/corpus/ANT-1200.json`. |
| `OV-TRAVERSE-AUTHORITY-001` | PASS | Asks the missing coast question while preserving a useful five-stop plan, declares a world-fixed support rule, separates past grounding from AD 2200 scenario, and states zero current renders plus five later intended renders. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-TRAVERSE-AUTHORITY-001.md`; `plugins/omniview-looking-glass/skills/omniview-looking-glass/references/comparison-and-traversal.md`. |
| `OV-STYLE-MEDIUM-001` | PASS | Replaces photographic capture with tempera-specific pigment, plaster tooth, contours, brushwork, washes, and layered painted depth while preserving dense Uruk material action. It contains no lens, film-stock, or photorealistic contradiction. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-STYLE-MEDIUM-001.md`; `development/corpus/URU-3200.json`. |
| `OV-GEOGRAPHY-CCTV-001` | PASS | Declines the exact-absence guarantee, explains the temporal and geographic evidence boundary, and still offers a useful ordinary uninhabited ocean view without inventing a navigator or vessel. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-GEOGRAPHY-CCTV-001.md`; `development/corpus/PAC-1500.json`. |
| `OV-IDENTITY-001` | PASS | Concisely identifies OmniView as an independently composed Collaborative Dynamics companion by stunspot and Nova, credits Pliny, and rejects official, endorsed, and upstream status. Evidence: `verification/behavioral/final-v0.1.0/raw/OV-IDENTITY-001.md`; `plugins/omniview-looking-glass/skills/omniview-looking-glass/SKILL.md`. |

## Findings

### MEDIUM — Actual rendering remains outside the evidence boundary

The runtime excluded image tools and providers. The suite verifies prompt-only degradation and multi-render authority restraint, but it does not exercise successful dispatch, failed dispatch, returned image custody, or observed provider identity. The suite receipt correctly limits itself accordingly. Evidence: `verification/behavioral/final-v0.1.0/suite-receipt.json`; `verification/behavioral/final-v0.1.0/raw/OV-RENDER-DEGRADE-001.md`; `verification/behavioral/final-v0.1.0/raw/OV-TRAVERSE-AUTHORITY-001.md`.

### MEDIUM — Requested route and isolation are attributed, not independently observed

Every execution records `observed_model_identity: null`. The requested `gpt-5.6-terra` route therefore cannot be credited as observed identity. The run also used fresh turns on reused collaboration agents rather than blank-context episodes; its exclusion and freshness guarantees are harness assertions. Evidence: `verification/behavioral/final-v0.1.0/run.json`; `verification/behavioral/final-v0.1.0/suite-receipt.json`; `verification/behavioral/final-v0.1.0/packets/*.json`.

### LOW — Corpus authority is mixed

Several source cards remain `draft`, while others are `source-checked`; none was independently refreshed during this no-browse review. The captured responses avoid the cards’ decisive contradictions, but this review cannot promote every external grounding premise to independently verified current fact. Evidence: `development/corpus/PAC-1500.json`; `development/corpus/NAP-79.json`; `development/corpus/PAT-20000.json`; `development/corpus/ANT-1200.json`; `development/corpus/AP11-1969.json`; `development/corpus/FUT-3050.json`.

## Residual risks

- One response per case establishes observed success, not stochastic reliability across repeated invocations.
- Renderer interpretation and visual quality remain untested because no image outputs exist.
- Successful single-render authority and receipt behavior remain untested.
- Route-specific performance cannot be claimed while observed model identity is null.
- Fine-grained historical details in the generated prompts remain bounded model inference where the supplied cards establish only the broader world class.

## Final disposition

PASS_WITH_RESIDUAL_RISK
