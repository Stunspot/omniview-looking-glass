Target: OmniView 0.1.0; receipt `OV-ISOLATED-20260802-01`, dated 2026-08-02. I reviewed only the four supplied receipt-referenced raw outputs (under `verification/behavioral/raw/`), not a live rerun or host installation. Current `SKILL.md` SHA-256 matches the receipt: `7ce4…641c`.

- `OV-SAHARA-HUMID-001` — PARTIAL: sparse, heterogeneous humid-phase scene and spatially cautious water pass; the prompt does not clearly establish the expected wadi/wetland/wider-water system, leaving the humid hydrology under-specified.
- `OV-FUTURE-SCENARIO-001` — PASS: explicit scenario and coherent consequences across adaptation, water, repair/materials, transit, energy, ecology, and habitation.
- `OV-APOLLO-EXACT-001` — PASS: correctly selects Apollo 11, holds an access-compatible public standoff, and composes a period-compatible launch event.
- `OV-RENDER-DEGRADE-001` — PASS: complete seed, explicit `prompt-only` state, and no fabricated render dispatch, provider, or image.

Decision-changing findings:

1. `PRODUCT_BEHAVIOR_GAP`, P2 — challenged claim: the Sahara case fully demonstrates humid-phase hydrology. Evidence: “shallow runoff toward a green basin” is compatible with the scene, but does not make the required wadi/wetland/wider-water system perceptible. Discriminating rerun: same case, require a spatially plausible drainage/wetland/broader-water relation while retaining no unsupported lake at the shelter mouth. Required revision: strengthen the hydrology grounding/prompt behavior, then capture a replacement isolated output. Status consequence: this four-case slice cannot be reported all-pass until rerun.

2. `EVIDENCE_CUSTODY`, P2 — challenged claim: the receipt independently establishes fresh isolated `gpt-5.6-terra` behavior. Evidence: it identifies run, route, context boundary, and output paths, but records neither immutable raw-output hashes nor per-subagent execution/task receipts. I verified the current skill hash only. Discriminating rerun: capture per-case task/result identity, exact runtime hash, raw-output SHA-256, and terminal receipt. Required revision: bind those artifacts into the behavioral receipt. Status consequence: describe freshness/isolation as receipt-reported, not independently verified, pending that capture.

`REVIEW_PASS_WITH_CONDITIONS` for this bounded four-case slice.
