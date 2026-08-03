## REVIEW_FAIL

The final evidence is internally byte-consistent but does not support the behavioral release claim. Two credited cases violate explicit runtime/case invariants; one more omits required useful completion.

Scope reviewed: canonical runtime byte set `e16cdc…9ef10`, evaluation manifests/cases, final receipt, and 13 final raw outputs only. All 13 raw SHA-256 values match the receipt. The receipt reports isolated `gpt-5.6-terra` episodes at revision `e1bf192…628c`; I did not independently verify that Git state or re-execute the suite.

### Release-blocking findings

1. **P1 — Year-only temporal precision silently becomes a season.**

   - Challenged claim: AD 79 plus local hour selects an ordinary year-level view, not a calendar day or season.
   - Evidence: [OV-PRECISION-NAP-001.md](E:/Github/omniview-gl4ss-companion/verification/behavioral/final-v0.1.0/raw/OV-PRECISION-NAP-001.md:9) puts Vesuvius in “luminous **summer** haze.” The case explicitly lists invented season as a failure signal.
   - Why it matters: the response correctly excludes the eruption, then reintroduces unearned temporal specificity inside renderer-facing language—the silent failure this case exists to catch.
   - Required revision: remove season-specific language unless the request supplies it; rerun this case in a fresh isolated episode and replace its receipt hash.
   - Status consequence: blocker.

2. **P1 — The future scenario does not carry an energy system.**

   - Challenged claim: a composed future scenario carries its causal bundle through water, climate adaptation, energy, maintenance, materials, ecology, mobility, and habitation.
   - Evidence: [OV-FUTURE-SCENARIO-001.md](E:/Github/omniview-gl4ss-companion/verification/behavioral/final-v0.1.0/raw/OV-FUTURE-SCENARIO-001.md:4) renders water management, reuse, maintenance, ecology, mobility, and dense habitation. “Warm transit windows and pedestrian lamps” show consumption, but no visible energy source, storage, distribution, or maintenance relation carries the scenario’s energy claim.
   - Required revision: choose one coherent energy consequence for the declared scenario and make it visible/materially integrated, then fresh-run the case.
   - Status consequence: blocker; the only credited future-scenario case does not demonstrate the full claimed boundary.

3. **P2 — The anti-CCTV answer stops at refusal rather than providing the promised useful next move.**

   - Challenged claim: decline omniscient absence while offering an ordinary view or an evidence question.
   - Evidence: [OV-GEOGRAPHY-CCTV-001.md](E:/Github/omniview-gl4ss-companion/verification/behavioral/final-v0.1.0/raw/OV-GEOGRAPHY-CCTV-001.md:3) correctly refuses the guarantee, but offers neither an ordinary-view prompt nor a focused evidence question.
   - Required revision: after the refusal, offer a bounded open-ocean view or ask for evidence that could narrow the vessel question.
   - Status consequence: not independently blocking, but must be repaired before a clean pass.

### Case scores

`2` = critical case behavior demonstrated; `1` = authority boundary correct but required completion missing; `0` = direct semantic/case failure. Scores are not averaged.

| Case | Score | Case-level evidence |
|---|---:|---|
| OV-APOLLO-EXACT-001 | 2 | Full date/time selects Apollo 11; public standoff and prompt-only state are honest. |
| OV-FUTURE-SCENARIO-001 | 0 | Named composed scenario, but no causal energy system appears in the scene. |
| OV-GEOGRAPHY-CCTV-001 | 1 | Correctly rejects guaranteed absence; provides no useful view/evidence continuation. |
| OV-IDENTITY-001 | 2 | Correct independent-companion attribution; no official/upstream claim. |
| OV-NEMO-PROMPT-001 | 2 | Prompt-only open-ocean frame uses an explicit virtual aperture and positive uninhabited geometry. |
| OV-PATAGONIA-SUPPORT-001 | 2 | Ice is physical support; local weather/texture remain bounded inference. |
| OV-PRECISION-NAP-001 | 0 | Year-only prompt injects “summer haze.” |
| OV-PRIPYAT-COMPARE-001 | 2 | Maintains a physical-footing invariant and materially distinguishes maintenance from succession without universal-absence language. |
| OV-RENDER-DEGRADE-001 | 2 | No-image-tool condition produces a complete seed and truthful prompt-only state. |
| OV-SAHARA-HUMID-001 | 2 | Sparse site use, heterogeneous humid-phase terrain, and morning material/light behavior are present. |
| OV-STYLE-MEDIUM-001 | 2 | Tempera/plaster mark behavior replaces photographic capture while retaining density, depth, and material action. |
| OV-TRAVERSE-AUTHORITY-001 | 2 | Missing coordinate is handled with a five-stop, world-fixed, zero-render plan and declared future scenario. |
| OV-URUK-DENSE-001 | 2 | Dense activity occupies depth with Late Uruk materials, managed water, and a first-light event. |

The receipt is sound as an integrity binding for the captured text, not proof of installation, discovery, image generation, live-provider behavior, or fresh-host invocation—consistent with its own stated boundary. Repair and independently rerun the two P1 cases, then the P2 completeness case, before reopening release disposition.
