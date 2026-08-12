# Troubleshooting

Start with the boundary that failed. Files present on disk, host discovery, skill invocation, source grounding, and image dispatch are different states.

## The host does not find OmniView

1. Confirm that `SKILL.md` sits directly inside the installed `omniview-looking-glass` folder.
2. Confirm that you installed the artifact for the intended host.
3. Start a new task; restart the host if it does not refresh skill discovery.
4. Request explicit selection before testing implicit selection.
5. Preserve the host's exact response or log when reporting the problem.

A plausible place-time answer does not prove that the installed skill was selected. This public release has no fresh-host discovery receipt.

## The answer needs a more exact place or time

Add the smallest fact that changes the world in frame:

- a coordinate or named site when a broad place contains several distinct environments;
- a full date and local time when season, solar geometry, or a dated event matters;
- an ordinary-day instruction when you want a representative year-level view;
- a scenario label and causal assumptions for a future view.

Year-only requests correctly leave calendar-specific weather, moon phase, exact shadow geometry, and season unresolved.

## The result says `source-unavailable`

A load-bearing claim could not be resolved responsibly. Choose one recovery:

- narrow the place, date, event, or requested detail;
- provide a source you want used;
- ask for the ordinary evidence-supported world class;
- ask for a clearly labeled composed scenario.

`source-unavailable` is useful when uncertainty would change the support, habitation, structure lifecycle, selected event, or world class. It is not a request to invent precision.

## No image appears

Read the reported state:

- `prompt-only` means no dispatch occurred and the complete Render Seed is the handoff;
- `render-failed` means dispatch occurred and the tool returned a failure;
- no reported state means the tool boundary still needs reconciliation;
- `host-rendered` is earned only when an image output was returned and can be referenced.

For `prompt-only`, copy the Render Seed into an image system you are authorized to use. For `render-failed`, preserve the seed and the host's exact error before retrying. Check tool availability, provider policy, account state, cost authority, and input limits outside OmniView.

Do not retry an external render while commit or billing state is uncertain.

## Comparison frames drift

Restate one invariant: coordinate, camera height, bearing, field of view, support relation, local-hour convention, and stable spatial anchor. Use a world-fixed virtual aperture when the physical support changes or disappears between dates.

## A traversal pauses before rendering

Supply the missing place or coordinate, confirm the ordered stops, and review the stated render count. Planning a traversal does not authorize an unspecified multi-render batch. Resume only after the host's ordinary authority boundary is satisfied.

## A GL4SS patch does not apply

Stop at `git apply --check`. Confirm the frozen commit and both patch hashes in [Apply the GL4SS drop-ins](GL4SS-DROPINS.md). Use a clean disposable checkout; do not force a context-mismatched patch.

## Report a reproducible defect

Include:

- OmniView version and host version;
- artifact used: Codex folder, Claude ZIP, or GL4SS drop-ins;
- installed topology without credentials or personal paths;
- exact request and returned state;
- exact error text or tool receipt;
- whether the problem is installation, discovery, invocation, grounding, prompt composition, or rendering;
- whether a retry could incur cost or duplicate an external action.

Share secrets, API keys, private coordinates, account identifiers, and unrelated host logs only through a channel you have deliberately chosen for that data.

Use [Support](SUPPORT.md) for the public reporting route, [Security policy](SECURITY.md) for sensitive defects, and [Lifecycle](LIFECYCLE.md) before removing installations or retained data.
