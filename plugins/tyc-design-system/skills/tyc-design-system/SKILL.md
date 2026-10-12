---
name: tyc-design-system
description: Use whenever creating, restyling, or reviewing UI/frontend code for a TYC Thailand internal system (new project or existing one — e.g. frontend-mes, wms, rcs-rmr-pm, or any new internal tool). Enforces the org's single design system (brand colors, button/table/card conventions, radius/spacing scale, dark+light mode) instead of improvising a new look per project. Also use when asked about "TYC theme", "TYC brand guideline", "design tokens", or to make a system "match the design system". Supports full-reskin, partial (named-module), and extend-the-library modes.
metadata:
  author: Narawit
  created: 2026-07-15
  updated: 2026-10-12
  tags: [design-system, html]
  status: stable
---

# TYC Thailand — Design System

One visual language across every internal system. This skill exists so a new
project (or a redesign of an old one) pulls from the same tokens and
component conventions as everything else, instead of each Claude session
reinventing colors/radii/spacing from scratch.

**The canonical source is the reference file, not this document's memory of
it.** Always read the actual files under `reference/` for real values — do
not recall hex codes from a previous conversation, they may have been
refined since.

## 0. If you're unsure this skill applies

It applies to any UI work in a TYC Thailand internal system. It does **not**
apply to: external/customer-facing sites, one-off scripts, or projects the
user has explicitly said follow a different design system. If ambiguous,
ask rather than assume.

## 1. Pick a mode

This skill has three modes. Resolve which one applies from the skill's
`args` (if invoked as `/tyc-design-system <mode> ...`) or from the user's
wording — if neither is clear, ask with AskUserQuestion before doing any
work. The three modes touch very different amounts of code; picking wrong
means either a wasted full reskin or an under-delivered partial one.

| Mode | Triggers on wording like | What it does |
|---|---|---|
| `full` | "เปลี่ยน theme ทั้งหมด", "restyle the whole app", "apply the TYC theme", no scope mentioned at all | Full reskin — every module in the § "partial" menu below, across the whole project. |
| `partial` | "เปลี่ยน theme บางส่วน", "just update the buttons/colors/tables", any request naming specific components | Reskin only the named module(s). If "partial" was requested without naming which parts, present the module menu and ask (multiSelect) before touching code. |
| `extend` | "เพิ่ม pattern ใหม่เข้า theme", "เพิ่ม component ใน design system", "update the reference file/skill" | Not a target-project change — grows `theme-ui-guideline.html` itself (the master file) with a new token/component, then re-syncs this skill's `reference/` copies. |

### `full` — apply the whole theme

1. Inventory the target project first: existing global CSS/tokens file,
   component library in use (shadcn/ui? custom?), whether dark mode already
   exists. Don't reskin blind.
2. Install/align the token file (§ 2.4). **Then — before touching
   individual components — read `reference/tailwind-token-audit.md` and run
   its grep audit if the project is Tailwind/shadcn.** Installing the token
   file alone does not reskin components that use hardcoded Tailwind
   palette utilities (`bg-white`, `bg-gray-100`, `bg-blue-600`, `rounded-xl`,
   etc.) — this step is what actually makes existing components (navbar
   toggle, cards, anything not freshly built from this skill) pick up the
   new theme. Skipping it is the single most common reason a "full" reskin
   still leaves parts of the UI looking untouched.
3. Work through every module listed under `partial` below, in order —
   tokens first (everything else depends on them), then components.
4. If the project's existing pattern for something conflicts with this
   theme (see § 4), stop and ask before overwriting, rather than silently
   reskinning past a real prior product decision.
5. Run the § 5 checklist before reporting done.

### `partial` — apply named module(s) only

Fixed module menu — use these names, they map 1:1 to sections in
`theme-ui-guideline.html` so lookups in § 2 stay unambiguous:

1. **Colors & Tokens** — `--color-*` palette, chart palette
2. **Typography** — font-family, type scale
3. **Radius & Spacing** — the 4/6/10/999px scale, 4pt spacing grid
4. **Buttons**
5. **Tables**
6. **Cards & Layout** — cards, grid/box layout, stepper/order card, empty state
7. **Forms & Inputs** — form pattern, checkbox/radio, switch/progress, slider/input group/divider
8. **Navigation** — sidebar, navbar/header, footer, breadcrumb, tabs, dropdown/avatar
9. **Overlays** — dialog, alert/toast, drawer, accordion
10. **Charts**
11. **Dark/Light mode**

Rules for this mode:

- If the user named module(s) explicitly, touch **only** those — don't drift
  into neighboring modules "while you're in there."
- If they said "partial"/"บางส่วน" without naming any, ask via
  AskUserQuestion (multiSelect, options = the list above) before touching
  code — this is the concrete answer to "what inside the system should
  change," don't guess it.
- Modules 1–3 (Tokens, Typography, Radius/Spacing) are foundational: if a
  requested component module needs a token the target project doesn't have
  yet, add the minimum token(s) it needs rather than falling back to a
  hardcoded value.
- On a Tailwind/shadcn project, any module in **4–9** (Buttons through
  Overlays) can silently no-op on pre-existing components even after the
  right classes/tokens exist — run `reference/tailwind-token-audit.md`'s
  grep audit scoped to that module's components before calling it done, not
  just for `full` mode. A `partial` request for "Navigation" that doesn't
  check for hardcoded `hover:bg-gray-100` on the sidebar toggle button is an
  incomplete partial, not a correctly-scoped one.

### `extend` — add new theme material to the reference file

This mode edits the **master** `theme-ui-guideline.html` on the user's
Desktop (not a target project) to grow the org's design system with a new
token or component pattern.

1. Read the existing structure first — check `reference/tokens-and-rules.md`
   and grep the relevant section of `theme-ui-guideline.html` so the
   addition doesn't duplicate or contradict something that already exists.
2. Follow the file's established authoring pattern: numbered CSS section
   comment, component demo inside a `<section class="card">` with a
   `card-header`/`card-body`, a `.code-preview` block with HTML-escaped
   markup showing the copy-paste snippet — and if it's a new top-level
   section, a `sec-*` id plus an entry in the sidebar nav (match the pattern
   of existing sections exactly).
3. If adding colors: never hand-pick a hex. For chart/data-viz colors, run
   the `dataviz` skill's `validate_palette.js` the same way the existing
   `--chart-1..8` set was validated (both light and dark surfaces). For UI
   colors, check WCAG contrast against the surface(s) it'll sit on.
4. Verify structural balance after editing (open/close tag and brace counts
   should match) and smoke-test in a browser before calling it done — same
   as any edit to this file.
5. **After editing the Desktop master file, re-sync the copies** in the
   `pi-claude-md` repo at `plugins/tyc-design-system/skills/tyc-design-system/reference/`
   (`theme-ui-guideline.html`, plus the token CSS/JSON if tokens changed),
   bump `version` in that plugin's `.claude-plugin/plugin.json`, and open a PR
   so every installed copy picks it up on update. Never edit the installed
   plugin cache. Tell the user this happened — don't do it silently.

## 2. Read before you write

1. Open `reference/tokens-and-rules.md` first — it's the compact cheat sheet
   (colors, radius, spacing, dark-mode overrides, chart palette, the 6
   non-negotiable rules). This alone covers most token lookups.
2. **If the work touches status/state indicators, any action button/icon
   (view, edit, delete, add, refresh, approve, close, row actions, toolbar
   buttons), or the navbar/header — also open
   `reference/component-conventions.md` before writing anything.** Tokens
   alone (color hex) are not enough for these three areas: the *shape* and
   *structure* of the pattern matters as much as the color (badge
   dot-prefix structure, which exact icon, icon-only buttons staying square
   not circular/pill, navbar action order). This is the single most common
   source of "looks close but not quite right" results, and the navbar in
   particular is easy to skip entirely because it sits above the fold —
   don't assume § 3's rules already cover it.
3. If you need an exact component's HTML/CSS pattern for something *not*
   covered by `component-conventions.md` (e.g. "what does the stepper tabs
   markup look like", "how is the drawer built") — don't hand-roll it from
   memory. `Grep` for the component name inside
   `reference/theme-ui-guideline.html` (it's ~4000 lines; every component has
   a `.code-preview` block with the literal copy-paste-ready markup) and read
   just that section. Do not read the whole file into context.
4. For a Tailwind v4 project (CSS-first, `@import "tailwindcss"; @theme
   inline {...}`, no `tailwind.config.js`) — this is the stack used by
   `frontend-mes`, `rcs-rmr-pm`, and `wms` — match the schema in
   `reference/tyc-design-tokens.css`, don't reinvent the `@theme` block.
   **Installing this file is not the end of the job — immediately follow
   with `reference/tailwind-token-audit.md`.** That file's grep-based audit
   for hardcoded Tailwind palette utilities (`bg-white`, `bg-blue-600`,
   `rounded-xl`, etc.) is what actually makes pre-existing components adopt
   the new theme; the token file alone only affects components that already
   used semantic classes.
5. For a legacy Tailwind v3 project — use `reference/tailwind.config.js` as
   the starting config, adjusting only `content` paths, then run the same
   `tailwind-token-audit.md` check.
6. `reference/tyc-design-tokens.json` is the portable W3C-format token file,
   useful if the target isn't a Tailwind/CSS project at all (e.g. a design
   tool import, a non-Tailwind CSS-in-JS setup).

## 3. Non-negotiable rules (do not deviate without asking)

See `reference/tokens-and-rules.md` § "Non-negotiable rules" for the full
list with rationale. The short version:

- Buttons: pill-shaped, except icon-only buttons (stay square/`radius-md`).
- Table header: solid brand-blue background, white text.
- Pink accent: decorative only, ~25% ceiling, never a primary button or body
  text.
- No hardcoded hex in new component CSS — everything through a `var(--color-*)`
  token, so dark mode keeps working.
- Dark mode ships from day one on any new build, using the `[data-theme]`
  pattern already proven in `theme-ui-guideline.html`.
- Sidebar dark/light is a separate toggle from page dark/light — don't
  conflate them.

## 4. When the target project already has its own conventions

Real TYC repos (`frontend-mes`, `wms`, `rcs-rmr-pm`) were the actual source
for several of these conventions (soft buttons, table header color, sidebar
default) — they were cross-checked against this theme, not the other way
around. So:

- If a project's existing pattern **agrees** with this skill, keep it as-is;
  don't rewrite working code just to match this file byte-for-byte.
- If a project's existing pattern **conflicts** with this skill (e.g. a
  different button radius, a different blue), **stop and ask the user**
  which should win before changing it. Don't silently overwrite an
  established project convention, and don't silently deviate from the org
  theme either — surface the conflict.
- Never touch a project's database, auth, or business logic while doing
  theme work — this skill is presentation-layer only.

## 5. Before calling the work done

Run through this checklist — this is the concrete way to catch drift, since
there's no automated validator for "does the whole UI look right" (unlike
the `dataviz` skill's color-palette validator):

- [ ] Every new/changed color traces back to a `var(--color-*)` token — grep
      the diff for raw `#`/`rgb(` values you didn't get from
      `tokens-and-rules.md`.
- [ ] Buttons are pill-shaped except icon-only ones.
- [ ] If the page has tables: header is brand blue + white text.
- [ ] If pink is used: check it's ≤~25% of the visible color weight and
      never on a primary CTA or paragraph text.
- [ ] Dark mode: toggle `[data-theme="dark"]` (or the project's equivalent)
      and visually confirm nothing reads as unstyled/hardcoded-white-on-dark.
- [ ] Radius values used are from the scale (4/6/10/999px) — no one-off
      `border-radius` numbers.
- [ ] You did **not** invent a new brand color. If a genuinely new shade was
      needed, it was added as a named token in both light and dark blocks,
      not inlined once.
- [ ] If status badges, action icons, or the navbar were touched: they match
      `reference/component-conventions.md` exactly (same badge structure,
      same icon path data, icon-only buttons stayed square, navbar action
      order preserved) — not just "close in color."
- [ ] (`full` mode, or `partial` including Navigation) The navbar/header was
      explicitly checked, not left over from the target project's old
      styling — it's the one component easiest to scroll past.
- [ ] (Tailwind/shadcn project) Ran the `tailwind-token-audit.md` grep for
      hardcoded palette utilities — not just installed the token file and
      assumed existing components inherited it.
- [ ] (`partial` mode only) You touched only the requested module(s).
- [ ] (`extend` mode only) The Desktop master file and this skill's
      `reference/` copies are back in sync.

If anything on this list is uncertain or the visual result feels like a
guess rather than a lookup, stop and show the user before considering the
task finished — cheaper to confirm direction early than to redo a full
reskin.

## Reference files

| File | What it's for |
|---|---|
| `reference/tokens-and-rules.md` | Fast lookup: hex values, radius/spacing scale, dark-mode overrides, chart palette, the 6 hard rules. Read this first. |
| `reference/component-conventions.md` | Status badge structure + semantic mapping, the exact icon SVGs for every common action button (view/edit/delete/add/refresh/approve/close), and the navbar/header's fixed structure and action order. Read this before touching any status indicator, icon button, or navbar — token color alone isn't enough for these. |
| `reference/tailwind-token-audit.md` | **Read this for any Tailwind/shadcn project, `full` mode or not.** Explains why installing the token file alone leaves pre-existing components (navbar toggle, cards, etc.) unchanged, and gives the grep audit + hardcoded-class → semantic-class replacement table that actually fixes it. |
| `reference/theme-ui-guideline.html` | The full, browsable component library — every component with copy-paste markup in a `.code-preview` block. Open in a browser, or `Grep` for a component name inside it. |
| `reference/tyc-design-tokens.css` | Tailwind v4 `@theme inline` + `:root`/`.dark` token file — schema-matched to the real Next.js repos' `globals.css`. |
| `reference/tyc-design-tokens.json` | Portable W3C-format tokens (color/radius/spacing/typography/shadow), for non-Tailwind targets. |
| `reference/tailwind.config.js` | Tailwind v3-compatible config, for legacy projects without CSS-first Tailwind v4. |
| `tyc-design-system-skill-guide.html` | Human-facing install/usage manual (not read by Claude at runtime) — open in a browser. Covers installation via the `pi-claude-md` marketplace, the three modes with example prompts, and an FAQ. |

These reference files are **copies**, refreshed manually (or via `extend`
mode, step 5) — if `theme-ui-guideline.html` on the user's Desktop has moved
on since, the Desktop copy is the more current one; ask the user if the two
seem to have diverged.
