# Agent UI/UX Baseline

This repository uses a three-skill design baseline for any task that changes UI, frontend, interaction, visual identity, animation, or UX.

## Mandatory skill stack
1. `.agents/skills/ui-ux-pro-max/SKILL.md` — system-level UI/UX, accessibility, responsive behavior, typography, color, interaction, charts, and stack-aware implementation.
2. `.agents/skills/emil-design-eng/SKILL.md` — design-engineering craft, motion quality, interaction details, component polish, and perceived quality.
3. `.agents/skills/design-taste-frontend/SKILL.md` — anti-slop visual direction, layout/typography/spacing discipline, redesign audit, and intentional design variance.

## Precedence
Product/domain correctness > usability/accessibility > product identity > visual polish.
These skills must never override repository rules, source-of-truth requirements, engineering constraints, or factual correctness.

## Working rule
When a task touches UI/UX:
- Audit the existing experience before redesigning.
- Choose one coherent visual direction; do not mix styles randomly.
- Use motion only when it communicates state, hierarchy, continuity, or feedback.
- Prefer real content and real product visuals over decorative placeholders.
- Check desktop, mobile, keyboard/focus, reduced motion, loading/error states, and performance.
- Reject generic AI-template patterns unless explicitly justified by the product.
- Finish the implementation completely; no placeholder TODOs or knowingly fake interactions.

For pure backend/infrastructure work these skills are not required unless the change affects the user-facing experience.
