# Trust, Privacy, and Limits

OmniView composes a grounded place-time view inside the host that invokes it. The package contains prompts, references, templates, eval cases, notices, and metadata. It does not contain an image model, provider account, telemetry client, or API key. The optional local workspace can call the OpenAI Images API when its host has `OPENAI_API_KEY` and the user presses **Create image**.

## Data boundaries

The OmniView package itself keeps no API keys, telemetry, location history, or durable user profile. The local workspace reads an API key from the host environment and does not put it in browser code or records.

Your host may still retain task text, tool calls, logs, uploaded files, or generated outputs under its own settings. Research tools may send search terms to their configured services. An authorized host image dispatch may send the Render Seed, including its place and time, to its provider. Pressing **Create image** in the local workspace sends the place, time, optional light and scene, or authored seed to OpenAI and may incur an API charge. Directly generated PNGs are saved in the workspace data folder.

The workspace render boundary uses OpenAI; agent-host rendering has its own provider boundary. Review them before supplying private coordinates, unpublished research, personal data, sensitive sites, or confidential scenario assumptions.

`prompt-only` avoids an OmniView-initiated image dispatch. It is not a claim that the surrounding host keeps no logs or sends no task data elsewhere.

## Persistence

OmniView creates no durable view record by default. When you ask for one, the included `view-record.template.md` provides an inspectable structure. Storage occurs only through an authorized host path and remains subject to that host's custody.

## Evidence classes

OmniView keeps three kinds of statement distinct:

1. source-backed condition;
2. bounded visual inference needed for a coherent ordinary scene;
3. declared scenario choice.

The resulting image prompt is a visual reconstruction, not a primary source or proof that an exact instant looked that way. A future view is a composed possibility, not a forecast. Remoteness or geography can support an ordinary uninhabited frame; it cannot prove universal absence at every instant.

## Source limits

The development corpus contains 17 structured source cards. Their schemas and internal visible-claim links passed deterministic checks. Six cards remain marked `draft`, and this release did not freshly revalidate every external claim.

Exact, disputed, unfamiliar, or load-bearing claims should use suitable current sources. Source availability can narrow the warranted detail. `source-unavailable` is an honest terminal state when missing evidence would change the world class, optic support, habitation, lifecycle, or selected event.

## Render limits

The retained behavioral evidence contains no live image or video provider call and no rendered A/B. The local workspace render path has been exercised with a mock image response, not a paid provider call. It therefore establishes neither provider compatibility nor aesthetic superiority.

One-render requests may use an exposed host image tool when the request authorizes it. Comparisons and traversals remain text-first; OmniView states the intended render count before any multi-render route that could be metered or external.

Dispatch is not the same as a returned image. The truthful states are `prompt-only`, `host-rendered`, `render-failed`, and `source-unavailable`.

## Host limits

Codex and Claude artifacts were created and structurally verified. Fresh-host installation, discovery, explicit invocation, implicit selection, and healthy end-to-end behavior were not observed for this release. Read the [Host matrix](../customer-kit/HOST-MATRIX.md) before describing the package as active.

## License and relationship

OmniView is an independent Collaborative Dynamics companion inspired by The Looking Glass / GL4SS by Pliny the Liberator. It is not an official, endorsed, upstream, or replacement GL4SS release.

Original OmniView deterministic software is available under MIT, authored Augment material under CC BY-ND 4.0, and the separate GL4SS-derived drop-in pack under AGPL-3.0-or-later. These licenses do not imply endorsement or upstream status; read [Provenance](../customer-kit/PROVENANCE.md).

## Security posture

Inspect package bytes and `SHA256SUMS.txt` before installation. Preserve any existing skill of the same name. Keep provider credentials in host-approved secret storage, never in the package or a Render Seed. Do not retry a paid or state-changing tool call while its prior commit state is unknown.

For update, removal, rollback, and cleanup of saved prompts, view records, images, host logs, provider history, downloads, and GL4SS candidates, read [Lifecycle](LIFECYCLE.md).
