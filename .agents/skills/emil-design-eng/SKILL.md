---
name: emil-design-eng
description: Design-engineering quality baseline inspired by Emil Kowalski's public design-engineering skill. Use for UI polish, component craft, interaction details, and animation decisions.
---

# Emil Design Engineering — Project Adapter

Source: https://github.com/emilkowalski/skills/tree/main/skills/emil-design-eng

Use this skill when the UI needs to feel intentional, refined, and production-ready.

## Core principles
- Taste is trained: study strong interfaces and reverse-engineer why they work.
- Small invisible details compound: focus states, hover behavior, spacing, easing, timing, disabled states, loading feedback, and continuity matter.
- Do not animate by habit. First ask what the motion communicates.
- Enter/appear motion should usually feel controlled and easy; exits should not linger unnecessarily.
- Prefer transforms/opacity for animation; avoid layout-thrashing animation.
- Interaction feedback must be immediate but not abrupt.
- Components should have deliberate states: default, hover, active, focus-visible, disabled, loading, error, success where relevant.
- Never rely on decorative particles, gratuitous gradients, or random effects to make a UI feel premium.
- Use the product's real content and visual language.
- Review motion critically instead of accepting the first easing/duration that merely works.

## Review lens
Before shipping UI, inspect hierarchy, spacing, typography, interaction states, motion continuity, responsive behavior, and the small details users may not consciously notice.
