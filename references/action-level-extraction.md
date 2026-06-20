# Action-Level Extraction

## Problem

When users say "write like me", the request is usually vague:

- "more delicate"
- "less template-like"
- "more restrained"
- "more like something I would post"

These descriptions are emotionally accurate but not directly executable by a
language model. If the skill only stores them as adjectives, the generation step
will still drift back to generic internet writing.

## Design Choice

`style-distiller` translates soft descriptions into action-level rules.

The test is simple:

> Can this description answer what the model should do or avoid while writing?

If not, it is too abstract.

## Transformation Examples

| Vague description | Action-level version |
| --- | --- |
| The opening is engaging. | Start with a concrete scene, time anchor, or two-choice question. |
| The tone is restrained. | Avoid slogans, exclamation marks, forced emotional elevation, and direct preaching. |
| The writing feels personal. | Use small observable actions instead of abstract emotion labels. |
| The ending has aftertaste. | End on an image, question, or unfinished thought instead of a call to action. |
| The rhythm is clean. | Keep most sentences under a target length and insert short break sentences. |

## Seven Extraction Dimensions

The skill extracts style across seven dimensions:

1. `hook`: how the first one to three sentences attract attention.
2. `rhythm`: sentence length, paragraph length, pauses, and punctuation.
3. `voice`: speaker identity, temperature, sharpness, and self-reference.
4. `verve`: memorable lines, metaphors, reversals, and aphorisms.
5. `closing`: how the article ends and whether it leaves space.
6. `vocabulary`: preferred words, images, verbs, and forbidden words.
7. `format`: paragraphing, blank lines, emoji density, and layout.

An eighth file, `persona.md`, combines these dimensions into a readable writing
identity.

## Why This Matters

This is the difference between a prompt template and a learning system.

A prompt template says:

> Write in a restrained and delicate style.

`style-distiller` tries to say:

> Use a scene-based opening, keep the tone low-temperature, avoid emotional
> slogans, prefer concrete verbs, and end with image-based silence.

That second version is inspectable, testable, and easier to improve.

## Interview Talking Point

The important product decision was not to ask the model to "understand style" in
one step. I broke style into observable writing behaviors, because observable
behaviors can be stored, retrieved, verified, and corrected.
