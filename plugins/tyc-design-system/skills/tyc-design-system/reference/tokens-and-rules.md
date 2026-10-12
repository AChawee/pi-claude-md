# TYC Thailand — Design Tokens & Hard Rules (quick reference)

Compact lookup so a fresh Claude session doesn't have to open the 4000-line
`theme-ui-guideline.html` just to check a hex value. Read that file only when
you need an exact component's markup (see `SKILL.md` § 3).

## Brand colors (light mode)

| Token | Hex | Use |
|---|---|---|
| `--color-primary` | `#0172E5` | PANTONE 2173C. Main brand blue, ~75% of UI. Buttons, header, links, table header bg. |
| `--color-primary-hover` | `#015BB7` | Hover/active of primary. |
| `--color-primary-soft` | `#E7F1FD` | Light tint — badges, active-nav bg, soft buttons. |
| `--color-secondary` | `#A5BBCB` | PANTONE 5435C grey-blue. Borders, secondary buttons. |
| `--color-accent` | `#E81F76` | PANTONE 213C pink. **Decorative accent only, ~25% max.** Badges, ribbons, stepper-active, chart series. **Never** on large text blocks or primary/CTA buttons. |
| `--color-dark` | `#22242D` | PANTONE 6C near-black. Sidebar background, toast bg, code blocks. |

## Neutrals & status (light)

| Token | Hex |
|---|---|
| `--color-background` | `#F4F5F7` |
| `--color-surface` | `#FFFFFF` |
| `--color-text-main` | `#1F2430` |
| `--color-text-muted` | `#6B7280` |
| `--color-border` | `#E3E6EB` |
| `--color-surface-subtle` | `#FAFBFC` (card-footer, striped rows) |
| `--color-surface-hover` | `#F3F4F6` (hover states) |
| `--color-success` / `-bg` / `-text` / `-border` | `#16A34A` / `#DCFCE7` / `#166534` / `#A8E5BE` |
| `--color-warning` / `-bg` / `-text` / `-border` | `#D97706` / `#FEF3C7` / `#92400E` / `#F6DFA1` |
| `--color-danger` / `-bg` / `-text` / `-border` | `#DC2626` / `#FEE2E2` / `#991B1B` / `#F5B8B8` |
| `--color-accent-tint` / `-strong` / `-text-strong` / `-border-soft` | `#FDF1F7` / `#FCE4EF` / `#A61558` / `#F6C4DD` |

## Dark mode — same token names, `:root[data-theme="dark"]` overrides

| Token | Dark value |
|---|---|
| `--color-primary` / `-hover` / `-soft` | `#3987E5` / `#5B9FEE` / `#16283F` |
| `--color-background` / `--color-surface` | `#14151A` / `#1C1E27` |
| `--color-text-main` / `--color-text-muted` | `#EDEEF2` / `#9AA1AC` |
| `--color-border` | `#33353E` |
| `--color-success` / `-bg` / `-text` | `#22C55E` / `#123422` / `#86EFAC` |
| `--color-warning` / `-bg` / `-text` | `#F59E0B` / `#3A2A08` / `#FCD34D` |
| `--color-danger` / `-bg` / `-text` | `#F87171` / `#3A1418` / `#FCA5A5` |

`--color-accent` and `--color-dark` (sidebar) stay the **same** hex in both
modes — they were picked to already work on both light and dark surfaces.
Shadows also get a dark override (`--shadow-sm/md/lg` → higher black opacity).
Full block: `theme-ui-guideline.html`, search `:root[data-theme="dark"]`.

## Chart palette (8-slot categorical — fixed order, never reassign/cycle)

Validated with the `dataviz` skill's `validate_palette.js` for both light and
dark surfaces — do not substitute ad-hoc colors here.

| Slot | Hue | Light | Dark |
|---|---|---|---|
| 1 | blue (brand) | `#0172E5` | `#3987E5` |
| 2 | aqua | `#1BAF7A` | `#199E70` |
| 3 | yellow ⚠ needs direct label | `#EDA100` | `#C98500` |
| 4 | green | `#008300` | `#008300` |
| 5 | violet | `#4A3AA7` | `#9085E9` |
| 6 | red | `#E34948` | `#E66767` |
| 7 | magenta (brand accent) | `#E81F76` | `#D9457F` |
| 8 | orange | `#EB6834` | `#D95926` |

## Radius scale

| Token | px | Use |
|---|---|---|
| `--radius-sm` | 4px | inputs, small chips |
| `--radius-md` | 6px | **default** — cards use `--radius-lg`, but most controls, icon-only buttons |
| `--radius-lg` | 10px | cards |
| `--radius-pill` | 999px | **all buttons** (except icon-only, which stay `--radius-md`) |

## Spacing (4pt grid)

`--space-1..6` = 4 / 8 / 12 / 16 / 24 / 32 px.

## Typography

`--font-main: 'Prompt', 'Inter', -apple-system, "Segoe UI", sans-serif`
(Sarabun is the production font in `frontend-mes`/`rcs-rmr-pm` — if the target
repo already has Sarabun loaded, keep it as the primary family instead of
Prompt; don't introduce a third font family.)

## Non-negotiable rules

1. **Buttons are pill-shaped** (`border-radius: var(--radius-pill)`) — always,
   except icon-only buttons, which stay square (`--radius-md`).
2. **Table header**: solid `--color-primary` background, white text, sort
   chevrons on sortable columns. Row actions are blue icon-square buttons.
3. **Pink (`--color-accent`) is decorative only, ~25% ceiling** — badges,
   ribbons, stepper-active state, one chart series slot. Never a primary
   button, never large/body text, never >25% of a screen's color weight.
4. **Never hardcode a hex color in new component CSS.** Every color goes
   through a `var(--color-*)` token, including hover/disabled/subtle states —
   this is what makes dark mode work automatically. If a needed shade doesn't
   have a token yet, add one to both the light `:root` block and the
   `:root[data-theme="dark"]` block, don't inline a one-off hex.
5. **Dark mode is not optional** — any new system built from this theme
   should ship the `[data-theme]` toggle pattern from the start (see
   `theme-ui-guideline.html`'s inline FOUC-prevention script + navbar toggle
   + `toggleColorScheme()`), not bolt it on later.
6. **Sidebar** may be dark (`--color-dark`, default) or light
   (`.sidebar.theme-light` override) — this is a separate, independent toggle
   from page dark/light mode. Don't conflate the two.
