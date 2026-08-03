# Independent Evidence-Custody Review

Reviewer route: `/root/probe10_future/case_pripyat/pripyat_season_preflight#review_evidence_final`

## Command receipt

```text
python -B -X utf8 verification/scripts/verify_behavior_suite.py verify --run-dir verification/behavioral/final-v0.1.0
Exit code: 0
Status: PASS
Cases: 13
Claim boundary: Byte custody and declared isolation metadata only; no behavioral-quality claim.
```

The verifier was read from `verification/scripts/verify_behavior_suite.py`. Runtime commit and observed repository HEAD were both `e986b6acd1555925864c6c5314de4f729ba9874a`.

## Checks

- All 13 canonical case objects in `plugins/omniview-looking-glass/skills/omniview-looking-glass/evals/omniview-cases.yaml` matched the canonical JSON hashes recorded in `verification/behavioral/final-v0.1.0/run.json`, every `packets/*.json`, and every `executions/*.json`.
- Every `inputs/*.txt` file matched its canonical case input byte-for-byte. Recorded SHA-256 digests and byte counts matched.
- Every packet hash and execution hash matched `run.json` and `suite-receipt.json`.
- The six runtime files named across the packets matched their recorded hashes, current working-tree bytes, and their bytes at runtime commit `e986b6a…`:
  `SKILL.md`, `NOTICE.md`, `references/comparison-and-traversal.md`, `references/grounding-and-precision.md`, `references/render-language.md`, and `references/wormhole-optics.md`.
- All 13 raw receipts under `verification/behavioral/final-v0.1.0/raw/` had valid headers, the expected runtime commit, and exactly the permitted runtime-file hashes.
- All 13 turn labels were unique. Each execution’s turn label matched its raw header.
- Every normalized file under `outputs/` was exactly the raw receipt remainder after the first-line header. Raw, header, and output hashes and byte counts matched their execution records.
- Host and adapter labels were consistently marked attributed. `gpt-5.6-terra` remained a requested route, while observed model identity remained `null` throughout `run.json`, packets, executions, and `suite-receipt.json`.
- The aggregate projection and aggregate SHA-256 in `suite-receipt.json` recomputed successfully.

## Findings

### HIGH — No request-side transport receipt

The stored chain proves canonical input → input artifact → packet → execution reference, but it does not independently prove that the exact packet or input bytes were dispatched to the credited model turn. Each execution contains only a response-side raw receipt; there is no captured request envelope, dispatch receipt, or orchestration event. The `READ_OK` header is model-emitted self-attestation, and `executions/*.json` is derived from that header plus the prepared manifest.

Consequently, these artifacts support local byte custody and response normalization, but not end-to-end prompt-delivery custody. Any claim that the outputs demonstrably resulted from those exact inputs would exceed the receipts. This does not contradict the narrow boundary explicitly stated in `verification/behavioral/final-v0.1.0/suite-receipt.json`.

### MODERATE — Final evidence is internally hashed but not durably sealed

`verification/behavioral/final-v0.1.0/` was untracked in the observed working tree. Its receipt hashes the run, packets, and executions, but the receipt itself was not anchored by an evidence commit or `evidence-custody.json`. The suite is therefore a self-consistent local snapshot, not independently immutable release custody.

### LOW — Fresh-turn evidence is attribution, not blank-context isolation

Unique turn labels were mechanically verified, but they do not prove independent agents or blank contexts. `run.json` correctly discloses reused collaboration agents, retained unrelated context, and fresh turns assigned to cases different from retained prior cases. This is an honest residual limitation, not a hidden failure.

### INFORMATIONAL — Route and platform claims remain properly bounded

The suite does not convert the requested Terra route into observed model identity. Host and adapter labels remain explicitly attributed. It also disclaims behavioral quality, installation, discovery, invocation, provider, rendering, and observed-model-identity claims. No inspected claim crossed those boundaries.

## Residual risks

- Exact request delivery and model provenance remain unobserved.
- Reused-agent fresh turns may retain unrelated context.
- Internal hashes cannot establish creation time or non-tampering before an external custody anchor.
- The passing verifier establishes structural and byte integrity only; it does not establish behavioral correctness or source-grounding quality.
- Repository review files were intentionally not read, as instructed.

## Final disposition

PASS_WITH_RESIDUAL_RISK
