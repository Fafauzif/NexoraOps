# NexoraOps design system

## Visual direction

A white, spacious operations platform with restrained burnt orange. The primary visual occupies most of each page: a twin, a large time-series chart, a decision matrix, or a financial comparison. Details follow selection or appear below the main result. Vertical scrolling is deliberate.

Lintara informs the large scene, slim metrics strip, replay controls and clean business summaries. JakCool informs the app shell, grouped navigation, chart priority and contextual inspector. The warehouse reference informs the cutaway's open roof, racks, pallets, conveyors, docks and small animated vehicles. NexoraOps uses its own identity and logistics content.

## Tokens

| Role | Value |
| --- | --- |
| Surface | `#FFFFFF` |
| Workspace | `#F6F7F9` |
| Primary | `#C65317` |
| Hover | `#A94010` |
| Selected surface | `#FFF0E6` |
| Main text | `#202833` |
| Supporting text | `#637080` |
| Border | `#E3E7EC` |
| Positive operating result | Muted forest green |
| Negative result | Muted rust |

Use system sans-serif fonts, avoiding runtime font requests. Body text is about 15px, page headings about 29px, section headings 17–19px, and main metric values 27–32px. Small captions remain secondary; they do not carry the central argument.

## Layout

The desktop sidebar is 224px wide. The top bar is 76px high. Main content has 24–32px spacing. Use no more than two major columns, with a 272px contextual inspector beside the scene. The scene height is 525px on ordinary desktop and 620px on large screens. Tables have generous row heights, consistent number alignment and quiet dividers.

At narrower widths, major columns stack. On phones, the navigation becomes a drawer, metrics use two columns, and the initial network view is 2D. Tables retain their column widths inside a horizontal scrolling container. A user can still inspect facilities and run calculations.

## Motion and rendering

Use orthographic camera projection, soft colors and diffuse directional lighting. Roads follow schematic corridor geometry; buildings remain procedural. Trucks and parcels are small relative to buildings. Actor count follows regional demand and selected-facility activity, with explicit aggregation. Canvas fallback uses the same camera and geometry when WebGL2 cannot be created.

Respect reduced-motion preferences by starting replay paused. Keep camera controls, pause, speed and timeline accessible independently of drag gestures. Low-quality mode reduces decorative building count, leaving numerical results unchanged.

## Copy and evidence

The app describes operating actions and consequences. It does not include “planned,” “needs validation,” “further justification needed,” reviewer scores, prompts, AI-tool descriptions, or offers of help. Team assumptions remain identified where they affect interpretation. Evidence citations use meaningful source titles, not upload paths or internal tool identifiers.
