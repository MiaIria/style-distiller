# Style Distiller References

This folder contains interview-facing reference notes for `style-distiller`.

The goal is to make the design decisions behind the skill explicit: not only
what the skill does, but why it is structured this way and how quality is
controlled.

## Files

| File | What it explains |
| --- | --- |
| `action-level-extraction.md` | How vague style descriptions are translated into executable writing actions. |
| `quality-guardrails.md` | The five quality guardrails that prevent "training samples" from becoming unused context. |
| `retrieval-strategy.md` | How relevant writing samples are selected before generation. |
| `verification-rubric.md` | How generated drafts are checked against the style profile. |
| `feedback-loop.md` | How user feedback updates the style profile over time. |

## Interview Summary

`style-distiller` is designed as a lightweight personal writing style system.
It does not fine-tune a model. Instead, it simulates a training loop through:

1. local style profiles,
2. positive and negative samples,
3. retrieval-augmented prompting,
4. rule-based verification,
5. user feedback.

The key product idea is:

> The user does not want "an article written by AI". The user wants an AI that
> can gradually learn what "sounds like me" means.

## Folder Relationship

These reference files are not runtime prompts. They are product and method
documentation extracted from the skill design.

Runtime logic lives in the actual skill package:

```text
style-feed/
style-reject/
style-write/
style-feedback/
style-review/
style-lib/prompts/
```

These references explain the reasoning behind that structure.
