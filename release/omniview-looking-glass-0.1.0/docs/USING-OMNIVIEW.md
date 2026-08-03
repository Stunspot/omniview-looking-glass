# Using OmniView

Ask for a view in ordinary language. Give the place and time you care about; add the operation, viewpoint, or medium only when they matter to you.

## Open one view

Try requests such as:

> Open a view onto Uruk around 3200 BC at first light. Text and prompt only.

> Show me Misenum during the opening phase of Vesuvius on 24 August AD 79, from a shoreline witness position.

> Paint the eastern Patagonian steppe around 1900 as cold-weather watercolor on rough paper.

OmniView resolves the location, temporal precision, local hour, physical support for the optic, habitation state, visible world, and requested medium. It then returns a grounded interpretation and a complete image-ready prompt.

## Choose text or images

| Request | Expected behavior |
|---|---|
| Describe, interpret, ground, or plan | Stay text-only; include a Render Seed when requested or useful. |
| Give me the prompt, or prompt only | Return the complete copy-ready Render Seed without dispatch. |
| Open, show, render, or look through | Prepare one view; use an image tool only when the host exposes one and the request authorizes it. |
| Compare two or more moments | Preserve the optic, explain the comparison, and state the render count before any multi-image dispatch. |
| Traverse a route or timeline | Plan the stops first, state the render count, and obtain authority before multiple renders. |

When no usable image tool is available, the prompt is the finished handoff. OmniView should report `prompt-only`; it should not imitate a render receipt.

## Read the answer

A complete response normally identifies:

- the interpreted place, date precision, local hour, operation, and medium;
- the optic and how it occupies the viewpoint;
- the visible conditions and the evidence class supporting them;
- the scene composition and medium-native render language;
- the complete prompt;
- the tool outcome: `prompt-only`, `host-rendered`, `render-failed`, or `source-unavailable`.

The exact headings may change to fit the request. The evidence and tool-state distinctions should not.

## Let the date earn the detail

A year usually selects a period, not a particular day. OmniView can infer a plausible local hour when you request dawn, noon, or night, but it keeps season, weather, moon phase, and famous events open unless your input or sources select them.

Compare these requests:

> Open Naples in AD 79.

This calls for a representative, uncertainty-aware view. It does not automatically call for an eruption.

> Open Misenum at 13:00 on 24 August AD 79 during the opening phase of the eruption.

This selects a much narrower event frame. The answer can make the declared event conditions visible while separating documented facts from bounded scene inference.

## Hold the camera still for comparisons

Ask:

> Compare the same street-level view in central Pripyat at 14:00 in 1985 and 2020. Text and prompts only.

OmniView should establish one comparison invariant before describing change:

- one coordinate or clearly named place;
- one optic height, bearing, field of view, and support condition;
- one local-hour convention where the dates permit it;
- one stable foreground or horizon anchor.

The world changes between frames. The camera does not quietly wander to improve the composition.

## Plan traversals before rendering

Ask:

> Build a five-stop traversal of this coastline from the river mouth to the headland. Tell me the render count before using any image tool.

The response should define the route, order the stops, preserve a meaningful optic rule, and say `5 renders requested` before any tool dispatch. A request for a traversal authorizes planning. It does not automatically authorize an unspecified batch of paid or state-changing render calls.

## Name a medium when its marks matter

OmniView treats medium as part of the scene logic, not as a style sticker.

> Render this as egg tempera on a gessoed panel, with shallow modeled light and visible brush-laid color transitions.

That request should change surface, edge, color, depth, and mark-making language. If you do not name a medium, OmniView chooses a defensible visual treatment and says what it chose.

## Declare future scenarios

Future views are scenarios rather than recovered facts. Give the causal frame you want examined:

> Open lower Manhattan in 2080 under a managed-retreat scenario with two meters of mean sea-level rise. Show the infrastructure choices that follow from that premise.

OmniView should label the scenario, keep its assumptions visible, and make consequences legible in the frame. It should not present the result as a forecast or documentary record.

## Ask for grounding

Add any of these phrases when you want more visible evidence work:

- `Show your source classes.`
- `Separate sourced conditions from scene inference.`
- `Tell me what the date does not determine.`
- `Give me the prompt without rendering.`

If available sources cannot support the requested specificity, a useful answer narrows the claim, offers a scenario label, or returns `source-unavailable`. It does not fill the gap with false precision.

For failures and recovery steps, read [Troubleshooting](TROUBLESHOOTING.md). For the evidence boundary, read [Trust, privacy, and limits](TRUST-PRIVACY-AND-LIMITS.md).
