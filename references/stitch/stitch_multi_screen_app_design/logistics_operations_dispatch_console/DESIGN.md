---
name: Logistics Operations & Dispatch Console
colors:
  surface: '#f8f9ff'
  surface-dim: '#d2dae9'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eefd'
  surface-container-high: '#e1e9f8'
  surface-container-highest: '#dbe3f2'
  on-surface: '#141c27'
  on-surface-variant: '#584239'
  inverse-surface: '#29313c'
  inverse-on-surface: '#eaf1ff'
  outline: '#8b7267'
  outline-variant: '#dfc0b4'
  surface-tint: '#a43d00'
  primary: '#a33d00'
  on-primary: '#ffffff'
  primary-container: '#c65317'
  on-primary-container: '#ffffff'
  inverse-primary: '#ffb597'
  secondary: '#53606f'
  on-secondary: '#ffffff'
  secondary-container: '#d3e1f3'
  on-secondary-container: '#576473'
  tertiary: '#675c55'
  on-tertiary: '#ffffff'
  tertiary-container: '#80756d'
  on-tertiary-container: '#090402'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbcd'
  primary-fixed-dim: '#ffb597'
  on-primary-fixed: '#360f00'
  on-primary-fixed-variant: '#7d2d00'
  secondary-fixed: '#d6e4f6'
  secondary-fixed-dim: '#bac8da'
  on-secondary-fixed: '#0f1d2a'
  on-secondary-fixed-variant: '#3b4857'
  tertiary-fixed: '#eee0d6'
  tertiary-fixed-dim: '#d2c4bb'
  on-tertiary-fixed: '#211a14'
  on-tertiary-fixed-variant: '#4e453e'
  background: '#f8f9ff'
  on-background: '#141c27'
  surface-variant: '#dbe3f2'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  title-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-semibold:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style
The design system establishes a focused, calm, and analytical environment for enterprise logistics planners, supply chain orchestrators, and fleet dispatchers. Its core personality is measured, exact, and structurally transparent. High-density supply network decisions demand cognitive clarity: visual noise is stripped down so operators can rapidly detect schedule deltas, capacity bottlenecks, and freight exceptions.

The design movement combines **Minimalism** with structural **Enterprise Precision**. White modular panels rest against a muted canvas, avoiding dramatic decorative elements, gradients, or heavy fills. High-impact color is strictly utilitarian—reserved for primary calls-to-action, active network states, and clear operational anomalies.

## Colors
The palette balances low-fatigue background surfaces with deliberate, high-legibility accents.

### Core Canvas & Surfaces
- **Canvas / App Shell:** `#F6F7F9` (Soft grey workspace background)
- **Surfaces & Cards:** `#FFFFFF` (Pure white interior cards, tables, panels)
- **Dividers & Borders:** `#E3E7EC` (Subtle boundary separation)

### Typography & Content
- **Primary / Headers:** `#202833` (Deep charcoal, ensuring crisp contrast without the harshness of pure black)
- **Secondary / Supporting:** `#637080` (Muted slate for metadata, table headers, breadcrumbs, and helper text)

### Accent & Interaction
- **Primary Action & Active States:** `#C65317` (Burnt orange for key buttons, active navigation markers, and selected policy proposals)
- **Hover & Pressed States:** `#A94010` (Deepened burnt orange)
- **Selection Tint:** `#FFF0E6` (Pale peach tint for row highlights, selected card backgrounds, and active pill surfaces)
- *Constraint:* Orange must never be applied as broad full-card background fills or body text.

### Semantic Triage
- **Critical / Overload / Error:** `#DC2626` (Coral red)
- **Warning / Operational Risk:** `#D97706` (Amber)
- **Healthy / Optimal / Confirmed:** `#16A34A` (Muted forest green)
- **Baseline / Dormant:** `#64748B` (Neutral slate)

## Typography
Plus Jakarta Sans provides geometric balance and clear numeral delineation for data-dense tables, shipping manifests, and route schedules.

- **Primary Headings (`display-lg`, `display-md`):** Scaled between 28px and 32px with tight tracking (`-0.02em`) to ground operational dashboards without dominating vertical real estate.
- **Reading Hierarchy (`body-lg`, `body-md`):** 16px is used for primary summaries, modals, and long-form configurations; 14px serves as the default enterprise table cell, form control, and sidebar label font.
- **Micro-labels (`label-sm`):** Set at 11px uppercase with `0.04em` tracking for status pills, table column headers, and telemetry units.

## Layout & Spacing
The layout follows a fluid 12-column grid system paired with strict 8pt modular component spacing.

- **Canvas Organization:** The outer workspace uses `#F6F7F9` background canvas with an application shell layout (persistent collapsible 240px rail, sticky contextual toolbar, and a dynamic 12-column content area).
- **Responsive Adaptations:**
  - **Desktop (1280px+):** 12-column fluid grid, 24px (`1.5rem`) gutters, and 32px (`2rem`) outer margin. Data tables and split-pane dispatch views can span side-by-side.
  - **Tablet (768px - 1279px):** 8-column layout, 16px (`1rem`) gutters and margins. Side panels collapse into modal drawers.
  - **Mobile (<768px):** 4-column layout, 16px outer margin. Fleet maps and shipment tables stack vertically.

## Elevation & Depth
Elevation in this system uses clean structural borders and shallow ambient shadows rather than dramatic drop-shadows.

1. **Base Flat Surface (Level 0):** Pure white `#FFFFFF` cards and table shells set directly on `#F6F7F9` canvas, framed by a crisp 1px solid border (`#E3E7EC`).
2. **Interactive Hover (Level 1):** `0 2px 6px -1px rgba(32, 40, 51, 0.05), 0 1px 3px -1px rgba(32, 40, 51, 0.03)`. Used for hovered cards and floating table rows.
3. **Overlays & Drawers (Level 2):** `0 8px 24px -4px rgba(32, 40, 51, 0.08), 0 4px 12px -2px rgba(32, 40, 51, 0.04)`. Applied to flyouts, route-detail drawers, filter dropdowns, and context menus.
4. **Modal Dialogs (Level 3):** `0 20px 40px -8px rgba(32, 40, 51, 0.12)`. Supported by a semi-transparent slate scrim (`rgba(32, 40, 51, 0.4)`).

## Shapes
A subtle corner radius preserves the pragmatic, structured nature of enterprise tools.

- **Base Radius (`0.25rem` / 4px):** Standard controls, inputs, data grid cells, table check triggers, and status badge containers.
- **Card & Container Radius (`rounded-lg` / `0.5rem` / 8px):** Primary modules, filter bars, split cards, and dialog containers.
- **Capsule / Full Radius (`9999px`):** Reserved exclusively for standalone metric badges and active transport status pills.

## Components

### Buttons & Trigger Controls
- **Primary Button:** Background `#C65317`, text `#FFFFFF`, 0.25rem border-radius. Padding: 8px 16px. Hover state switches to `#A94010`. Focused state adds a 2px offset ring in `#FFF0E6` with a `#C65317` outline.
- **Secondary Button:** White `#FFFFFF` background, 1px solid `#E3E7EC` border, text `#202833`. Hover: background `#F6F7F9`, border `#D1D7DE`.
- **Tertiary / Ghost Button:** Transparent background, text `#637080`. Hover: background `#F6F7F9`, text `#202833`.

### Inputs & Select Fields
- **Container:** Height 36px, background `#FFFFFF`, border 1px solid `#E3E7EC`, radius 4px, font 14px (`body-md`), text `#202833`.
- **Placeholder:** `#637080`.
- **Focus State:** Border `#C65317`, box-shadow `0 0 0 3px #FFF0E6`.
- **Error State:** Border `#DC2626`, box-shadow `0 0 0 3px rgba(220, 38, 38, 0.12)`.

### Cards & Data Panels
- Surface `#FFFFFF`, border 1px solid `#E3E7EC`, radius 8px (`rounded-lg`), padding 16px or 24px.
- **Proposed Policy / Selected Card:** Retains white surface, adds 1.5px solid `#C65317` border and an optional inner wash of `#FFF0E6` for header highlights.

### Status Chips & Badges
- Compact height (22px), font 11px uppercase bold (`label-sm`), radius 9999px, padding: 2px 8px.
- **Nominal / Delivered:** Background `#ECFDF5`, text `#16A34A`, border 1px solid `#A7F3D0`.
- **Risk / Delayed:** Background `#FFFBEB`, text `#D97706`, border 1px solid `#FDE68A`.
- **Critical / Overload:** Background `#FEF2F2`, text `#DC2626`, border 1px solid `#FECACA`.
- **Baseline / Staged:** Background `#F1F5F9`, text `#64748B`, border 1px solid `#E2E8F0`.

### Data Grids & Lists
- **Header Row:** Background `#F6F7F9`, text `#637080`, 11px uppercase, border-bottom 1px solid `#E3E7EC`.
- **Body Rows:** Background `#FFFFFF`, 44px height, text `#202833`, border-bottom 1px solid `#E3E7EC`.
- **Row Selected State:** Background `#FFF0E6`, with a 3px vertical accent indicator in `#C65317` on the far left edge.

### Checkboxes & Radios
- Size 16px × 16px, border 1px solid `#637080`, radius 3px (checkbox) or circular (radio).
- **Checked State:** Background `#C65317`, border `#C65317`, white check/dot icon.