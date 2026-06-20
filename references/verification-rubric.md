# Verification Rubric

## Goal

The model should not be trusted just because it says it followed the style
profile.

`style-distiller` verifies drafts after generation so that the system can catch
style drift before showing the final result as successful.

## Verification Areas

### 1. Hook

Check whether the opening matches the profile's stable hook patterns.

Examples:

- scene opening,
- question opening,
- reversal opening,
- direct claim,
- self-mocking opening.

### 2. Rhythm

Check sentence and paragraph behavior:

- average sentence length,
- proportion of short sentences,
- paragraph length,
- break sentences,
- punctuation habits.

### 3. Voice

Check whether the speaker identity and emotional temperature match.

Signals include:

- directness,
- warmth,
- sharpness,
- self-reference frequency,
- whether the draft becomes preachy or over-explained.

### 4. Verve

Check whether memorable lines match the user's preferred types.

Examples:

- concrete image,
- reversal,
- understated line,
- question instead of answer,
- life-object metaphor.

### 5. Closing

Check whether the ending follows the profile.

Common ending types:

- image freeze,
- open question,
- callback,
- short punch line,
- silence,
- action call.

### 6. Vocabulary

Scan for:

- preferred words,
- preferred images,
- concrete verbs,
- forbidden words,
- cliches,
- words imported from negative samples.

### 7. Format

Check:

- paragraphing,
- blank lines,
- emoji density,
- headings,
- list usage,
- punctuation style.

## Negative Sample Avoidance

Negative samples are treated as constraints, not suggestions.

The system checks whether the draft triggers:

- forbidden vocabulary,
- forbidden sentence patterns,
- unwanted endings,
- unwanted tone,
- platform-template phrasing.

## Sample Restoration Check

For each retrieved sample, verify whether its feature signature is actually
visible in the generated draft.

If selected sample features do not appear in the draft, retrieval did not help.

## Deviation Handling

Suggested handling:

| Deviation | Meaning | Action |
| --- | --- | --- |
| 0-10% | strong match | deliver draft |
| 10-25% | minor drift | repair locally |
| 25-50% | visible drift | flag and consider rewrite |
| over 50% | serious failure | regenerate or ask for more samples |

## Interview Talking Point

The verification step is what separates this from a normal prompt. A normal
prompt only asks the model to write in a style. This system checks whether the
style was actually used.
