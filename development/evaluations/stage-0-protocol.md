# Stage 0 - Static and Prompt-Text Protocol

Status: Authorized; no provider or image spend.

## Purpose

Stage 0 establishes that the candidate is a genuine drop-in, preserves degraded behavior, and makes better use of available scene evidence before any image model can obscure cause.

## Frozen control

- Source checkout: E:\Github\GL4SS
- Commit: ab4984597ecf3afbd8ea66309be5ed68ce429146
- Control planner: the exact buildSceneDirectionPrompt implementation at that commit
- Control renderer: the exact DEFAULT_IMAGE_TEMPLATE and buildPanelPrompt implementation at that commit
- Claim boundary: current control versus candidate, not release-to-release improvement

Record the source commit, candidate patch hash, template bytes, fixture hash, and every command receipt.

## Gate 1 - Source-card custody

Every scored case validates against source-card.schema.json and has:

- an exact coordinate meaning;
- a temporal precision boundary;
- source-backed visible consequences;
- habitation qualification;
- a compatible camera relation;
- generation obligations separated from oracle-only contradictions;
- reviewed source URLs.

AP11-1969 and FUT-3050 are stop cases. They are not scored as ordinary scene successes.

## Gate 2 - Patch and TypeScript contract

- git apply --check succeeds against the frozen commit.
- generateSceneDirection retains its positional signature, default model, abort signal, timeout path, response format, max-token behavior, and Promise<SceneDirection> return.
- SceneDirection fields and required parser core remain unchanged.
- buildImagePromptsFromDirection returns three prompts and keeps chrono-selfie behavior.
- DEFAULT_IMAGE_TEMPLATE continues to use only known PromptFields placeholders.
- The prior exact default is appended, not rewritten, in LEGACY_IMAGE_TEMPLATES.
- Portal migration remains byte-sensitive and leaves genuine user edits intact.

Integration build runs only in a disposable verification checkout, never in E:\Github\GL4SS.

## Gate 3 - Planner prompt structure

Deterministic inspection confirms that every mode includes:

- quoted location input and coordinates;
- exact formatted year and neighbour contrast;
- the era hint as subordinate context;
- the fixed day phase when supplied;
- visual style integration when supplied;
- the exact JSON keys required for that mode;
- all three panel subjects;
- the five canonical habitation labels;
- positive ground, lifecycle, camera-support, and conflict behavior;
- no schema drift.

Measure prompt characters and tokens with the same tokenizer where available. Density is evidence-bearing scene obligations per 100 tokens, not brevity alone.

## Gate 4 - Parser and degradation fixtures

Fixtures:

1. valid JSON;
2. fenced valid JSON;
3. valid JSON with every habitation level;
4. valid JSON with an unknown habitation value;
5. valid JSON missing each optional field;
6. valid JSON missing each required core field;
7. truncated JSON with salvageable habitation and narrative;
8. truncated JSON with salvageable habitation only;
9. structured malformed output;
10. plain prose;
11. empty output;
12. malformed biome and marker types.

Assertions:

- raw structured output never becomes user prose;
- missing core fields produce isFallback;
- safely salvageable habitation and narrative survive;
- unsalvageable biome and period markers are not invented;
- the engine-visible degraded state appears for fallback;
- unknown habitation is either made user-visible or explicitly retained as a documented residual risk.

## Gate 5 - Render compiler fixtures

Use frozen hand-validated SceneDirection fixtures for dense, sparse, traces-only, uninhabited, and unknown habitation.

For every default prompt:

- subject, habitation, markers, period, biome, light, style, and aspect survive when non-empty;
- capture remains first;
- period markers read as material evidence rather than a detached tag list;
- biome reads as ground and depth rather than a category label;
- wild cases contain none of the oracle-only human or built-world contradiction nouns;
- dense cases retain people at several distances;
- traces-only cases retain made things in their dated state;
- the prompt remains grammatical after empty optional fields.

For custom templates:

- omission of habitation appends its clause;
- omission of period appends its clause;
- omission of both appends both in stable order;
- unknown placeholders remain visible;
- genuine user text remains byte-preserved by migration;
- the old current default migrates to the candidate default.

## Gate 6 - Prompt-text comparison

Blind reviewers receive control and candidate prompts without labels. They score:

1. visible place-time specificity;
2. habitation and structural lifecycle;
3. physically compatible viewpoint;
4. material and surface specificity;
5. spatial composition and light behavior;
6. image-model attention efficiency;
7. contradiction or ambiguity risk.

Reviewers see the positive source-card obligations, but not the candidate's design rationale. Oracle-only contradiction facts are used for scoring and leakage checks, never pasted into generation prompts.

## Advancement

Stage 0 passes only when every deterministic gate passes and no sentinel regression remains unresolved. A pass authorizes preparation for a separately approved paid A/B; it does not authorize provider dispatch, prove rendered improvement, establish portability, or establish live host behavior.
