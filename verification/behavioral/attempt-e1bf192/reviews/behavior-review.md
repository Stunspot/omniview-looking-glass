# Independent behavioral review — OmniView 0.1.0

**Disposition: REVIEW_FAIL.**  
Reviewed target: `e1bf192da672e3d036228bbf2e45160ffdee628c`; receipt timestamp: 2026-08-02 18:24:38 -05:00; isolated `gpt-5.6-terra` episodes.

Receipt custody is intact: the canonical `SKILL.md` hash and all 13 raw-output hashes match `suite-receipt.json` exactly. No files were edited.

| Case | Verdict | Evidence |
|---|---|---|
| OV-APOLLO-EXACT-001 | PASS | Correctly selects Apollo 11, holds a public standoff, and states `prompt-only`. |
| OV-FUTURE-SCENARIO-001 | REVIEW_FAIL | Scenario is declared, but its visible causal system omits **energy**. |
| OV-GEOGRAPHY-CCTV-001 | REVIEW_FAIL | Correct refusal, but omits the required useful follow-up. |
| OV-IDENTITY-001 | PASS | Correct independent-companion attribution; no official-GL4SS claim. |
| OV-NEMO-PROMPT-001 | PASS | Complete prompt-only open-ocean view with a virtual aperture. |
| OV-PATAGONIA-SUPPORT-001 | PASS | Ice footing, bounded local inference, and prompt-only state are all explicit. |
| OV-PRECISION-NAP-001 | REVIEW_FAIL | Injects an unearned season into a year-only request. |
| OV-PRIPYAT-COMPARE-001 | PASS | Honest invariant, maintained 1985 / traces-only 2020, material differences. |
| OV-RENDER-DEGRADE-001 | PASS | Complete seed and truthful `prompt-only` state without a tool claim. |
| OV-SAHARA-HUMID-001 | PASS | Sparse humid-phase site use; no rainforest, desert-collapse, or cattle-tableau failure. |
| OV-STYLE-MEDIUM-001 | PASS | Actual tempera/plaster behavior replaces photographic capture language. |
| OV-TRAVERSE-AUTHORITY-001 | REVIEW_FAIL | Declares an unsupported render-state label, and does not provide a complete prompt plan. |
| OV-URUK-DENSE-001 | PASS | Dense, materially dated activity across depth with grounded first-light action. |

## Decision-changing defects

| Severity | Case | Exact evidence | Why it fails | Required revision |
|---|---|---|---|---|
| P1 / release-blocking | OV-GEOGRAPHY-CCTV-001 | The entire substantive answer ends: “*the historical record does not provide instant-by-instant vessel surveillance.*” | The case requires a useful view or evidence question after declining the impossible guarantee. The answer refuses correctly but leaves the user nowhere useful to go. | Add a concise offer, e.g. an ordinary uninhabited open-ocean view at a specified date/time or a question about the evidence standard sought; do not invent a vessel. |
| P1 / release-blocking | OV-PRECISION-NAP-001 | Render Seed: “*Vesuvius through luminous summer haze.*” | AD 79 plus 12:03 lacks a month/day. “Summer” is an invented season and directly triggers the case’s failure signal. | Replace seasonal language with an ordinary year-level condition that does not select a season or eruption. |
| P1 / release-blocking | OV-TRAVERSE-AUTHORITY-001 | “*Render state: prompt-first; zero images now.*” | The canonical runtime defines `host-rendered`, `prompt-only`, `render-failed`, and `source-unavailable`; it does not define `prompt-first` as a render state. The output also provides only a coarse stop table, not prompts or an actionable prompt plan. | Use `prompt-only` for the zero-dispatch result, retain the five-render conditional count, and provide a representative seed with exact per-stop substitutions or equivalent prompt plan once the coordinate is supplied. |
| P1 / release-blocking | OV-FUTURE-SCENARIO-001 | Scenario and seed show water management, reuse, automation, maintenance, ecology, mobility, and habitation, but no energy system. | The future oracle and canonical runtime require the causal bundle to carry through **energy** as well. Lit windows and drones are consumers, not an articulated energy consequence. | Name and visibly integrate a compatible energy generation/storage/distribution consequence into the scenario and seed. |

## Evidence-quality warnings

- **P2 — TestForge structural validation is not satisfied.** `validate_manifest.py` returned `valid: false`, reporting missing `claim_custody`, `decision`, `executions`, `findings`, `risks`, `scenarios`, `scope`, `target`, and related required sections. `validate_traceability.py` returned `valid: true` only with zero risks, scenarios, tests, and executions. Those tool results do not independently substantiate traceability for this custom eval manifest.

- **P2 — Raw-capture boundary is ambiguous.** Every raw output begins with transport/provenance material such as `READ_OK; HEAD=...; SKILL_SHA256=...; FILES=...`. If that header is user-visible rather than harness metadata, it violates the runtime’s instruction to keep construction scaffolding out of ordinary experience. The receipt does not distinguish the two, so this remains a warning rather than an additional case failure.

The minimum repair is to regenerate the four failed raw cases and rerun independent review against a receipt that binds the revised skill bytes and outputs.
