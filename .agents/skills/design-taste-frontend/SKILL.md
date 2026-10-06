---
name: design-taste-frontend
description: Anti-slop frontend design baseline inspired by the current Taste Skill. Use for new frontends, visual redesigns, layout/typography/spacing decisions, and design-direction audits.
---

# Taste — Anti-Slop Frontend Project Adapter

Source: https://github.com/Leonxlnx/taste-skill

This is the project's anti-generic-design layer. It is not a replacement for domain UX or engineering correctness.

## Core rules
- Read the brief first and infer a design direction instead of defaulting to a familiar template.
- Establish a clear visual hierarchy before adding effects.
- Make spacing, typography, density, and alignment intentional.
- Avoid generic AI tells: repetitive rounded cards, default gradients, arbitrary glassmorphism, excessive pills, random shadows, placeholder copy, and identical section structures.
- Use asymmetry, restraint, contrast, or density intentionally; do not add variance merely to look different.
- Treat motion as part of the design language, not decoration.
- On redesigns, audit the existing product first and fix the biggest perceptual problems before rebuilding.
- Use real imagery/reference assets where they improve product understanding.
- Keep components coherent: repeated patterns should have a system, not one-off styling.
- A premium result should feel authored, not assembled from fashionable defaults.

## Design dials
Tune three independent dimensions per product: DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY. Choose them deliberately for the product and viewport.

## Delivery gate
Before calling a frontend finished, inspect visual hierarchy, spacing, typography, responsive behavior, motion, accessibility, and whether the result still looks like an intentional product rather than generated UI.
