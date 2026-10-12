# Why "nothing changed" after installing the tokens — read this first for any Tailwind/shadcn project

This is very likely the actual root cause behind repeated "the navbar toggle
didn't change," "cards don't follow TYC theme" reports. Swapping in
`tyc-design-tokens.css` is **necessary but not sufficient**. It only
reskins components that already consume the *semantic* Tailwind classes
(`bg-primary`, `bg-card`, `border-border`, `text-muted-foreground`,
`rounded-md`). A component written with **literal Tailwind palette
utilities** (`bg-white`, `bg-gray-100`, `text-gray-500`, `border-gray-200`,
`bg-blue-600`, `rounded-xl`) is completely invisible to the token swap —
those classes hardcode their own color/radius independent of any CSS
variable, by design (that's what makes Tailwind's default palette work
without a theme at all). Installing the token file changes *what `bg-primary`
resolves to*; it does nothing for a class that was never `bg-primary` in the
first place.

**This is why a `full` or `partial` pass can install the token file
correctly, restyle the components built fresh from
`theme-ui-guideline.html`, and still leave the target project's *existing*
navbar toggle, cards, or other pre-existing components completely
unchanged** — those were written before the token swap, against literal
Tailwind colors, and nothing in a token-only change touches them.

## The fix: audit for hardcoded utilities, don't just install the token file

Treat this as a required step whenever `full` mode runs on a Tailwind/shadcn
project, or `partial` mode touches Navigation/Cards/Buttons/any visual
module on one — **after** confirming `tyc-design-tokens.css` (or the
project's already-aligned `globals.css`) is in place:

1. Grep the component source (not `node_modules`, not generated files) for
   hardcoded palette utilities:
   ```
   grep -rnE "\b(bg|text|border|ring|shadow)-(white|black|gray|slate|zinc|neutral|stone|blue|sky|red|rose|green|emerald|amber|yellow|pink)-?[0-9]*\b" src/components src/app
   ```
2. For every match, replace with the semantic equivalent it should have used:

   | Hardcoded (banned) | Replace with | Why |
   |---|---|---|
   | `bg-white`, `bg-gray-50` (page/card surfaces) | `bg-background` or `bg-card` | Routes through `--background`/`--card`, flips correctly in dark mode |
   | `bg-gray-100`, `bg-gray-200` (subtle fills, hover) | `bg-muted` or `bg-secondary` | Matches `--color-surface-hover`/`-subtle` intent |
   | `text-gray-500`, `text-gray-400` | `text-muted-foreground` | Routes through `--muted-foreground` |
   | `border-gray-200`, `border-gray-300` | `border-border` | Routes through `--border` |
   | `bg-blue-600`, `bg-blue-500`, `text-blue-600` | `bg-primary` / `text-primary` | Routes through `--primary` (the actual brand blue) |
   | `bg-red-*`, `text-red-*` (error/destructive) | `bg-destructive`, `text-destructive` | Routes through `--destructive` |
   | `bg-green-*` (success) | `bg-success`, `text-success-foreground` | This schema adds `--success` specifically because shadcn has no default — see `tyc-design-tokens.css` |
   | `rounded-xl`, `rounded-2xl`, arbitrary `rounded-[Npx]` | `rounded-md` (default) or `rounded-lg` (cards) or `rounded-full` (pills) | Only the scale in `tokens-and-rules.md` is legal — an arbitrary radius is exactly as much a violation as an arbitrary hex color |
   | `hover:bg-gray-100` on a nav/sidebar toggle button specifically | `hover:bg-sidebar-accent` (inside the sidebar) or `hover:bg-accent` (elsewhere) | This exact pattern is the most common cause of "the toggle button didn't change" — a hover-only override is easy to miss because the unstyled state looks fine at rest |

3. **Icon-only buttons** (the sidebar/navbar toggle included) are the
   easiest to miss because they're small and often styled inline rather than
   via a shared `Button` component. Explicitly check the toggle/hamburger
   button's className for hardcoded colors even if the rest of the navbar
   looks right — see `component-conventions.md` § 3 for what it should look
   like once correctly themed.
4. If the project uses shadcn's own `<Sidebar>` / `<SidebarTrigger>`
   components (`components/ui/sidebar.tsx`), they already consume
   `--sidebar*` variables from the schema — verify those variables are
   actually present in the project's `globals.css` (not just added
   alongside the old ones under different names). A common half-migration
   bug: someone pastes in TYC's `--primary`/`--card`/etc. but leaves the
   file's *own* pre-existing `--sidebar*` block untouched because it wasn't
   scrolled into view — check the whole file, not just the top.
5. Re-render and toggle both light and dark mode after the audit, not just
   after the token-file swap — a component can look correct in light mode by
   coincidence (default Tailwind gray often resembles the light-mode token
   value) and only reveal the hardcoding once dark mode exposes that it
   didn't move.

## Non-Tailwind / plain-CSS projects

This file is Tailwind/shadcn-specific. If the target project is plain
CSS/CSS-in-JS (no utility classes), the equivalent check is simpler but the
same principle applies: grep for raw hex codes and `rgb()`/`hsl()` literals
in component stylesheets and replace them with `var(--color-*)` — see
`tokens-and-rules.md`'s "never hardcode a hex" rule, which is this same
issue stated for plain CSS instead of Tailwind utilities.
