# Quality Guardrails

## Goal

The core promise of `style-distiller` is:

> Training samples should not be wasted.

If a user feeds 30 or 50 examples into the system, generation must actually use
that information. Otherwise the product becomes a dressed-up prompt template.

## The Five Guardrails

### 1. Accurate Retrieval

Before writing, the skill retrieves three to five relevant samples instead of
loading every sample or choosing randomly.

Selection considers:

- topic similarity,
- dimension relevance,
- recency.

This prevents unrelated samples from pushing the draft in the wrong direction.

### 2. Hard Translation Of The Profile

The style profile is translated into layered constraints:

- hard constraints: forbidden words, forbidden sentence patterns, strong negative samples,
- strong constraints: hook type, voice, closing style,
- soft constraints: rhythm, imagery, paragraphing, punctuation.

This prevents the model from treating the profile as optional decoration.

### 3. Full Prompt Assembly

Generation should include:

- profile summaries,
- selected sample originals,
- feature signatures,
- negative sample constraints,
- topic requirements.

Only using summaries is too weak. The model needs enough concrete evidence to
imitate behavior rather than labels.

### 4. Post-Generation Verification

Every draft is checked after generation.

The check covers:

- seven style dimensions,
- negative sample avoidance,
- selected sample feature restoration,
- topic completion,
- length and platform fit.

This handles the common failure where the model claims it followed the profile
but the draft does not actually match.

### 5. Automatic Repair Or Honest Failure

If deviation is small, the skill can repair the draft.

If deviation is high, the skill should regenerate. If repeated attempts still
fail, the user should be told the profile is not strong enough yet.

The product should not pretend a weak draft is good.

## Why These Guardrails Exist

LLMs have strong default writing priors. In Chinese short-form writing, they
often drift toward:

- inspirational endings,
- platform templates,
- exaggerated emotional language,
- generic internet slang,
- neat but empty aphorisms.

The guardrails exist to fight that default drift.

## Interview Talking Point

I treated writing style as a quality-control problem, not just a generation
problem. The key risk was not "can the model write", but "can the model keep
using the user's accumulated style data after many turns".
