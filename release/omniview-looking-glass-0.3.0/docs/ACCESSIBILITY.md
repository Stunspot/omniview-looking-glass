# Accessibility

OmniView's core handoff is text. A reader can install, invoke, understand, verify, and recover the companion without depending on a generated image.

## Documentation design

The public documentation uses:

- one page title and ordered heading levels;
- persistent, descriptive navigation and a skip-to-content link;
- visible keyboard focus and non-color status words;
- copyable text for commands, prompts, paths, hashes, and tool states;
- tables only for compact mappings that surrounding prose also explains;
- responsive text, images, grids, code blocks, and tables;
- no color-only, animation-only, audio-only, or image-only instruction;
- reduced motion when the reader requests it.

All three product images include meaningful alternative text on their intended surfaces. The social card also carries the exact product title and identifying line in visible pixels; its metadata includes an equivalent text alternative.

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

## Review status and known gaps

The v0.1.1 documentation source received a separate accessibility review covering heading order, link purpose, alternative text, keyboard-visible focus, skip navigation, contrast calculations, responsive overflow, reduced motion, text-first task completion, and error-recovery language.

Not tested:

- screen-reader traversal in a browser;
- voice control;
- magnification or forced-color modes;
- browser accessibility-tree inspection;
- user completion of the install-to-first-value journey with assistive technology.

No WCAG conformance claim is made. Host interfaces, provider dialogs, and generated-image viewers are outside the package and require their own accessibility evaluation.

## Report an accessibility barrier

Include the document or operation, host and version, assistive technology when relevant, expected route, observed barrier, and a privacy-safe reproduction. State whether you need an alternative format immediately. Use [Support](SUPPORT.html) for the reporting route and [Troubleshooting](TROUBLESHOOTING.html) for the general defect fields.
