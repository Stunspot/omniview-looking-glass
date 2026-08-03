# Trust, Privacy, and Limits

OmniView composes a grounded place-time view inside the host that invokes it. The package contains prompts, references, templates, eval cases, notices, and metadata. It does not contain an image model, provider account, hidden network service, telemetry client, or API key.

## Data boundaries

The OmniView package itself keeps no API keys, telemetry, location history, or durable user profile.

Your host may still retain task text, tool calls, logs, uploaded files, or generated outputs under its own settings. Research tools may send search terms to their configured services. An authorized image dispatch may send the Render Seed, including its place and time, to the host tool and its provider.

Those host and provider boundaries are outside this package. Review them before supplying private coordinates, unpublished research, personal data, sensitive sites, or confidential scenario assumptions.

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

The retained evidence contains no live image or video provider call, no returned image custody, and no rendered A/B. It therefore establishes neither provider compatibility nor aesthetic superiority.

One-render requests may use an exposed host image tool when the request authorizes it. Comparisons and traversals remain text-first; OmniView states the intended render count before any multi-render route that could be metered or external.

Dispatch is not the same as a returned image. The truthful states are `prompt-only`, `host-rendered`, `render-failed`, and `source-unavailable`.

## Host limits

Codex and Claude artifacts were created and structurally verified. Fresh-host installation, discovery, explicit invocation, implicit selection, and healthy end-to-end behavior were not observed for this preview. Read the [Host matrix](../customer-kit/HOST-MATRIX.md) before describing the package as active.

## License and relationship

OmniView is an independent Collaborative Dynamics companion inspired by The Looking Glass / GL4SS by Pliny the Liberator. It is not an official, endorsed, upstream, or replacement GL4SS release.

The GL4SS-derived patches remain under compatible AGPL custody. Original OmniView companion materials are private preview materials with no public license grant yet. Private receipt does not authorize public redistribution; read [Provenance](../customer-kit/PROVENANCE.md).

## Security posture

Inspect package bytes and `SHA256SUMS.txt` before installation. Preserve any existing skill of the same name. Keep provider credentials in host-approved secret storage, never in the package or a Render Seed. Do not retry a paid or state-changing tool call while its prior commit state is unknown.
