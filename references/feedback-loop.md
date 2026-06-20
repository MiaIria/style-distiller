# Feedback Loop

## Goal

`style-distiller` should improve from use.

The user should not need to perfectly describe their style in advance. Instead,
the system learns from:

- positive samples,
- negative samples,
- generated drafts,
- user ratings,
- user corrections.

## Feedback Types

### 1. Positive Sample Feedback

When the user feeds a liked article, the skill extracts transferable style
features and updates the profile.

This teaches the system what to move toward.

### 2. Negative Sample Feedback

When the user feeds a disliked article, the skill extracts anti-features and
updates the forbidden zone.

This teaches the system what to avoid.

### 3. Draft Rating

When the user rates a generated draft, the system adjusts profile weights:

- liked features become stronger,
- disliked features become weaker,
- repeated issues can become negative constraints.

### 4. Direct Profile Correction

The user may directly correct the profile:

- "I do not actually use this word."
- "The tone should be warmer."
- "The ending is too neat."

This correction should override weaker inferred signals.

## Rating Interpretation

| Rating | Meaning | System response |
| --- | --- | --- |
| 9-10 | benchmark draft | optionally archive as a positive sample |
| 7-8 | mostly correct | strengthen accepted traits |
| 4-6 | partially correct | record mixed feedback and ask for specifics |
| 1-3 | mismatch | back up profile and inspect failure causes |

## State Progression

The profile can be described in stages:

| State | Sample count | Meaning |
| --- | --- | --- |
| cold start | 0-2 | mostly generic baseline |
| sprout | 3-9 | visible but unstable style |
| learning | 10-29 | usable style profile |
| mature | 30+ | stronger style restoration |

Self-written samples have higher value than external liked samples because they
show how the user actually writes, not only what the user appreciates.

## Why Feedback Matters

Users often discover their preferences only after seeing a draft.

They may not know in advance that:

- the opening is too dramatic,
- the ending is too inspirational,
- a phrase feels unlike them,
- a certain example structure works well.

The feedback loop turns those reactions into profile updates.

## Interview Talking Point

The product is designed around progressive clarification. Instead of requiring
the user to define their style perfectly upfront, it lets the user react, score,
reject, and correct. That makes the system more realistic for everyday use.
