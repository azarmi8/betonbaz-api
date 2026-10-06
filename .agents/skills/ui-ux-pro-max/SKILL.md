---
name: ui-ux-pro-max
description: UI/UX design intelligence baseline for professional web, mobile, and desktop interfaces, adapted from the public UI/UX Pro Max skill.
---

# UI/UX Pro Max — Project Adapter

Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

Use for UI structure, visual systems, accessibility, interaction patterns, responsive behavior, typography, color, charts, and stack-aware implementation.

## Priority order
1. Accessibility: readable contrast, alt text, keyboard navigation, visible focus, meaningful labels.
2. Touch and interaction: comfortable target sizes, spacing, feedback, no hover-only critical behavior.
3. Performance: optimized images, lazy loading where appropriate, reserved layout space, avoid jank.
4. Style selection: choose a coherent style that matches the product; avoid random style mixing and emoji-as-icons.
5. Layout/responsive: mobile-first thinking, predictable breakpoints, no horizontal overflow.
6. Typography/color: readable body text, sensible line-height, semantic tokens, no gray-on-gray ambiguity.
7. Animation: context-aware timing, meaningful motion, reduced-motion equivalent.
8. Forms/feedback: visible labels, local error guidance, progressive disclosure.
9. Navigation: predictable hierarchy, back behavior, deep links where relevant.
10. Data visualization: clear legends, accessible semantics, responsive presentation.

## Required workflow
For a new page or system-wide visual direction, define the product type, audience, style intent, stack, layout, typography, color, interaction and anti-patterns before implementation.
For a focused fix, identify the specific UX outcome first, then the implementation/stack concern.
Never fabricate a recommendation from a search/database result. Treat guidance as input, not as authority over product requirements.

## Product-quality gate
A UI is not done when it merely renders. It must survive responsive, accessibility, reduced-motion, interaction, and perceived-quality review.
