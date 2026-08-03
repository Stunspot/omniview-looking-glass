# Independent TestForge review — OmniView final v0.1.0

**Disposition: REVIEW_FAIL**

The captured text is intact, but the suite does not earn its stated behavioral claim. One indispensable behavior demonstrably fails (`OV-PRECISION-NAP-001`), two further cases miss their specified boundary behavior, and the evidence package cannot independently establish its asserted isolated executions.

Reviewed target: `omniview-looking-glass` v0.1.0, receipt revision `e1bf192da672e3d036228bbf2e45160ffdee628c`, captured `2026-08-02T18:24:38-05:00`.

## Verified custody

- All 13 receipt-listed raw-output SHA-256 values match their files.
- The current plugin `SKILL.md` SHA-256 matches the receipt: `e16cdc...d9ef10`.
- Current plugin and Claude-distribution copies of the SKILL, four runtime references, and both eval files match byte-for-byte.

That establishes present-byte parity and the integrity of the captured raw text. It does not independently establish that the text was produced by the recorded model, adapter, host, fresh-agent isolation, or exact case/reference bytes at execution time.

## Findings

### High — temporal-precision failure

**Case:** `OV-PRECISION-NAP-001`  
**Challenged claim:** A year plus local hour does not select a date or season.

The Render prompt says “**luminous summer haze**” for “AD 79, 12:03 local time.” The runtime and the NAP source card expressly require preserving year-level precision and not inventing a season. This is a direct failure of an indispensable `temporal_precision` dimension.

**Required revision:** Remove the seasonal assertion or label it as a bounded, optional visual choice outside the source-backed claim; then recapture this case.

### High — execution and revision custody is insufficient

The receipt hashes the raw outputs and `SKILL.md`, but not the case definition, runtime references, assets, source cards, exact episode input, adapter/host identity, or per-case execution receipt. `repository_head`, `episode_model`, isolation, allowed reads, and `READ_OK` headers are recorded assertions, not independently captured tool/runtime receipts.

The TestForge manifest validator also rejects `eval-manifest.yaml` as a TestForge evidence manifest: it lacks target/scope, claim custody, risks, scenarios, tests, executions, findings, residual risk, decision, and review. Its traceability validator returns “valid” only vacuously with zero risks, scenarios, tests, and executions.

**Required revision:** Add immutable per-case execution receipts binding exact prompt/case bytes, all runtime-reference hashes, model/adapter/host identity, timestamps, result bytes, and isolation evidence; supply a non-vacuous risk → scenario → execution → finding map.

### Medium — traversal omits the required past/future evidence boundary

**Case:** `OV-TRAVERSE-AUTHORITY-001`  
The output correctly asks for the missing coast, declares a world-fixed aperture, states zero renders and the later count of five. But it does not state that the past stops require source grounding once the coordinate is provided, while the AD 2200 stop is a declared scenario. The runtime requires that distinction in the load-bearing coordinate question.

**Required revision:** State “past stops source-grounded after the coordinate is supplied; AD 2200 is Scenario OV-1,” and identify per-stop uncertainty.

### Medium — useful refusal is incomplete

**Case:** `OV-GEOGRAPHY-CCTV-001`  
The refusal correctly rejects a guarantee of vessel absence. It does not, however, offer either the useful ordinary uninhabited view or an evidence question, both required by the case.

**Required revision:** After the refusal, offer a prompt-only ordinary open-ocean view or ask what evidence standard would be needed.

## Per-case result

| Case | Review result |
|---|---|
| OV-APOLLO-EXACT-001 | Pass: full date/time selects launch; standoff and prompt-only state are honest. |
| OV-FUTURE-SCENARIO-001 | Pass: named composed scenario visibly carries through water, maintenance, materials, mobility, ecology, and habitation. |
| OV-GEOGRAPHY-CCTV-001 | **Fail:** correct refusal, missing required useful follow-up. |
| OV-IDENTITY-001 | Pass: attribution and non-official status are accurate. |
| OV-NEMO-PROMPT-001 | Pass: virtual aperture, ordinary uninhabited frame, and no rendered-image claim. |
| OV-PATAGONIA-SUPPORT-001 | Pass: ice support is source-compatible and local texture/weather are correctly labeled bounded inference. |
| OV-PRECISION-NAP-001 | **Fail:** invents “summer” from year-plus-hour input. |
| OV-PRIPYAT-COMPARE-001 | Pass: invariant, changed maintenance/succession, and no categorical no-human claim. |
| OV-RENDER-DEGRADE-001 | Pass: complete seed and truthful prompt-only degradation. |
| OV-SAHARA-HUMID-001 | Pass with caution: sparse humid-phase scene fits the card; exact occupancy and water placement remain visual inference. |
| OV-STYLE-MEDIUM-001 | Pass: genuinely tempera-specific mark/surface behavior, without photographic contradiction. |
| OV-TRAVERSE-AUTHORITY-001 | **Fail:** count/authority boundary passes, but source-grounded-past versus declared-future boundary is omitted. |
| OV-URUK-DENSE-001 | Pass with caution: dense material world is strong; exact canal/precinct placement should remain understood as bounded inference. |

## Grounding and source-card assessment

No direct source-card contradiction was found in the successful Patagonia, Pripyat, Sahara, Uruk, Point Nemo, or Apollo outputs. The clear conflict is Naples: its card and runtime exclude seasonal selection at year-level precision, while the raw prompt asserts summer.

The raw outputs generally distinguish prompt-only from rendered correctly. Grounding is strongest where it explicitly separates source-backed condition from bounded visual inference (especially Patagonia); source-sensitive prompt-only outputs should preserve that distinction more consistently when local occupancy, street layout, water placement, or material placement is materially unresolved.

## Claim boundary

The suite currently supports only this narrower statement:

> Thirteen captured text artifacts, whose listed hashes match the receipt, are consistent with several intended OmniView behaviors for the current `SKILL.md` bytes.

It does **not** establish the full stated claim of isolated model-text behavior for the named revision/runtime, nor defect-free behavior, live installation/discovery, image rendering, external research, provider dispatch, or cross-model portability. Re-review is warranted after the three failing cases and the custody chain are repaired.
