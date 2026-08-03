# Accessibility

OmniView's core handoff is text. A reader can install, invoke, understand, verify, and recover the companion without depending on a generated image.

## Documentation design

The private kit uses:

- plain Markdown with one page title and ordered heading levels;
- descriptive link text instead of bare destination labels;
- copyable text for commands, prompts, paths, hashes, and tool states;
- tables only for compact mappings that are also explained by surrounding headings;
- no color-only, animation-only, audio-only, or image-only instruction;
- explicit words for evidence classes and outcomes rather than icon-only status.

The documentation is usable as unstyled text. Line wrapping, font size, contrast, focus display, and Markdown rendering remain properties of the reader's chosen host.

## Nonvisual use

Ask for `text and prompt only` to keep the complete workflow textual. The response can provide:

- a compact description of the visible world;
- the optic and spatial relation;
- source-backed conditions, bounded inference, and scenario assumptions;
- the complete Render Seed when requested or useful;
- an explicit tool state.

When an image is returned, ask the host to describe that observed output separately. The prompt and pre-render view describe intended content; they are not evidence that every returned pixel matches the intention.

## Cognitive and motor access

Ordinary-language requests are the primary interface. Optional details can arrive in any natural order. OmniView asks one question only when the answer would materially change the world in frame; otherwise it chooses a defensible ordinary moment.

Installation and recovery procedures use short numbered steps, stable file names, exact commands, and explicit stop conditions. No timed interaction or precise pointer gesture is part of the package itself.

## Known gaps

This preview has not been tested with:

- screen readers;
- keyboard-only navigation in a rendered documentation site;
- voice control;
- magnification or high-contrast modes;
- browser accessibility inspection;
- users with disabilities completing the install-to-first-value journey.

No WCAG conformance claim is made. Host interfaces, provider dialogs, and generated-image viewers are outside the package and require their own accessibility evaluation.

## Report an accessibility barrier

Include the document or operation, host and version, assistive technology when relevant, expected route, observed barrier, and a privacy-safe reproduction. State whether you need an alternative format immediately. Use [Troubleshooting](TROUBLESHOOTING.md) for the general defect-report fields.
