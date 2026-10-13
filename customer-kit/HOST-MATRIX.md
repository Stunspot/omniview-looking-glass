# Current complete 0.3.1 host boundary

The current kit retains the accepted 0.3.0 camera and native launch mechanics with updated package/bundle metadata. Original Windows operation and static Mac icon/launcher evidence remain at their recorded scope; no fresh host/provider activation or Mac device result is claimed.

## Historical public portable-skill qualification

# Host Matrix

Public release: `v0.1.1`
Portable runtime under qualification: `v0.1.0` (unchanged)

This matrix keeps package construction separate from installation, discovery, invocation, and healthy live behavior.

| State | Codex | Claude Code | Evidence |
|---|---|---|---|
| Artifact created | Yes | Yes | Portable skill folders exist in the source repository. |
| Structurally verified | Yes | Yes | The package verifier reports 12 portable files and byte parity. |
| Included in public release | Yes | Yes | The release verifier checks both artifacts, the complete checksum set, and ZIP topology. |
| Installed on a fresh host | Not observed | Not observed | No customer or clean-host installation was performed. |
| Discoverable by the host | Not observed | Not observed | Filesystem presence is not discovery evidence. |
| Explicitly invoked | Not observed | Not observed | Behavioral cases exercised the runtime text in a harness, not an installed package. |
| Implicitly selected | Not observed | Not observed | Codex metadata permits implicit invocation; live selection remains untested. |
| Image tool available | Host-dependent; not observed here | Host-dependent; not observed here | No live host-image capability was exercised. |
| Prompt-only operation | Behaviorally observed in the bounded harness | Behaviorally observed against byte-matched runtime content | This is not a live-host claim. |
| Healthy end to end | Not established | Not established | Requires install, discovery, invocation, and result evidence on each host. |

## Codex artifact

Assembled-kit path:

    codex/omniview-looking-glass/

Source path:

    plugins/omniview-looking-glass/skills/omniview-looking-glass/

The package includes `agents/openai.yaml` for Codex-facing display and implicit-invocation metadata. The portable runtime remains rooted at `SKILL.md`.

## Claude artifact

Assembled-kit path:

    claude/omniview-looking-glass.zip

Source path:

    dist/claude-code/omniview-looking-glass/

The ZIP must contain exactly one top-level folder named `omniview-looking-glass`. Its 12 portable files must match the Codex portable files byte-for-byte. Codex-only `agents/openai.yaml` is not part of that parity set.

## State vocabulary

- **Created:** the artifact bytes exist.
- **Structurally verified:** deterministic checks accept topology, manifests, references, and parity.
- **Installed:** the artifact was copied into a host-recognized location.
- **Discoverable:** the host reports or demonstrates that it can find the capability.
- **Invoked:** an actual task caused the installed capability to run.
- **Healthy:** the observed result satisfies the public behavior and trust boundary.

Do not compress those six states into “active.”
