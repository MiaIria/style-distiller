# Retrieval Strategy

## Problem

When the sample library grows, loading everything is noisy and expensive.
Choosing the wrong samples can be worse than choosing no samples at all.

Example:

> The user wants to write a reflective post about aging, but the system retrieves
> several workplace complaint samples. The tone, vocabulary, and structure may
> become mismatched even if those samples are valid parts of the profile.

## Design Goal

Retrieve a small set of samples that are most useful for the current writing
task.

The target number is usually three to five samples.

## Scoring Dimensions

### 1. Topic Similarity

Does the sample discuss a similar subject, scenario, or emotional territory?

This is the highest-weight signal because topic strongly affects vocabulary,
examples, and tone.

### 2. Dimension Match

Does the sample represent the dimension currently needed?

For example:

- if the user asks for a stronger opening, retrieve hook-heavy samples;
- if the user wants a better ending, retrieve closing-heavy samples;
- if the draft feels too generic, retrieve voice and vocabulary samples.

### 3. Recency

Recent samples receive higher weight because personal style changes.

Older samples are not discarded, but their influence decays unless they are
clearly marked as benchmark samples.

## Sample Feature Signatures

Each selected sample should contribute a feature signature, such as:

```yaml
hook: scene opening with time anchor
rhythm: short paragraphs, one break sentence every few lines
voice: restrained, mildly self-mocking
verve: concrete image instead of abstract slogan
closing: image-based silence
vocabulary: prefers concrete verbs and everyday objects
```

The feature signature makes the sample easier to verify later.

## Output Transparency

The skill should show a retrieval report when useful:

- which samples were selected,
- why they were selected,
- whether the current topic is under-covered,
- whether the user should feed more related samples.

This makes the system feel less like a black box.

## Failure Handling

If relevant samples are missing, the skill should say so.

Possible responses:

- continue with the general profile but warn that topic coverage is weak,
- suggest feeding one to three related samples,
- ask whether the user wants a more generic draft first.

## Interview Talking Point

The retrieval strategy turns the style archive from passive storage into active
context. The point is not to collect many examples, but to select the few that
should influence the current generation.
