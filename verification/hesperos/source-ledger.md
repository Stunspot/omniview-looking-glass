# Source ledger

| Claim or behavior | Source and version | State | Scope | What changes if wrong |
|---|---|---|---|---|
| OmniView identity, authorship, and unofficial relationship to GL4SS | `NOTICE.md`, `LICENSE.md`, `customer-kit/PROVENANCE.md`, version 0.1.0 | reported | Owner-controlled identity and public split-license status | Attribution, redistribution, and handoff language must change. |
| GL4SS target commit, patch order, and patch hashes | `dropins/integration/dropin-manifest.json`; frozen commit `ab4984597ecf3afbd8ea66309be5ed68ce429146` | source-verified | Two bounded AGPL-derived patches | Application instructions and all integration evidence become stale. |
| Planner, renderer, and public-contract behavior | `dropins/tests/verify-candidate.mjs` and retained candidate execution receipts | source-verified | Frozen control and bounded candidate only | Drop-in claims and public-release readiness must be downgraded. |
| Portable skill topology and Codex-Claude parity | `verification/scripts/verify_package.py` and package execution receipt | source-verified | Static package bytes only | Install instructions, inventory, or parity claim must be repaired. |
| Thirteen final behavior cases and three independent reviews | `verification/behavioral/final-v0.1.0/` at payload commit `8a11716736321ea835091828ecd77cbbffb8243c` and custody commit `0049fdf21910fff738d32f070adabf7ef1e49df4` | source-verified | Captured outputs and declared reused-agent fresh-turn route | Behavioral claim boundary or readiness status must narrow. |
| Host installation paths and upload topology | Codex local installer contract; current official Anthropic skill guidance linked from `docs/INSTALLATION.md` | source-verified | Intended host route, not a live install receipt | Installation procedure must change and be requalified. |
| No package-owned telemetry, keys, location history, or default durable profile | sealed runtime `SKILL.md` and package inventory | source-verified | OmniView package itself | Privacy documentation and security posture must change. |
| Host or provider may retain task, tool, or render data | host/provider boundary analysis | inferred | External systems outside the package | Trust guidance may need a narrower or host-specific statement. |
| Text-first route, explicit tool states, and multi-render authority | sealed runtime and behavioral cases | source-verified | Bounded model-harness behavior; no live provider | Usage and recovery procedures must change. |
| Documentation has no Hesperos lint findings | one linter execution per 13 customer-facing Markdown files | source-verified | Static Markdown inspection | Accessibility state returns to review-needed. |
| Screen-reader, keyboard, browser, and representative-user usability | `docs/ACCESSIBILITY.md` and verification summary | not tested | Customer journey and host interfaces | No conformance or user-tested claim is available. |
| Public release topology, checksums, ZIP safety, parity, local links, licensing surfaces, and deterministic rebuild | `verification/scripts/verify_public_release.py` and retained build evidence | source-verified | assembled public release only | Kit inclusion and delivery-readiness claim must be withdrawn. |

States: source-verified, reported, inferred, conflicted, not examined, not tested.
