# TYC Thailand — Structural Pattern Conventions

Status badges, action icons, and the navbar are the most common source of
"looks close but not quite right" results — these are **structural
conventions**, not just color tokens. Matching the hex alone isn't enough:
the *shape* of the pattern (dot-prefix badge, square icon button, which
exact icon, navbar layout order) has to match too. Copy the markup below
verbatim; don't recreate it from a description or from memory of a similar
component elsewhere.

Source of truth for everything here: `theme-ui-guideline.html` — the
`.main-header` block for the navbar, "Card — Buttons" for action icons, and
the table pattern's `.action-group` markup for row actions. Grep those if
you need more surrounding context than what's copied below.

## 1. Status badges

### The rule

A status is **always** `<span class="badge badge-{variant}">ข้อความ</span>`
— nothing else. Never build a status indicator out of a plain colored
`<div>`, a Tailwind utility soup, or an icon+text pair you assemble by hand.
The 6px leading dot is automatic — it comes from `.badge::before` in the
stylesheet (`content: ""`, a circle filled with `currentColor`). **Do not**
add your own SVG checkmark/dot/icon inside a badge; if one shows up, the
badge is being built wrong.

```html
<span class="badge badge-success">ทำงานปกติ</span>
<span class="badge badge-warning">ลาพัก</span>
<span class="badge badge-danger">พ้นสภาพ</span>
<span class="badge badge-accent">พนักงานใหม่</span>
<span class="badge badge-neutral">ไม่ระบุ</span>
```

Renders as a pill-shaped, dot-prefixed, tinted-background label — e.g.
`● ทำงานปกติ` in green-on-light-green. All four color variants share
**identical structure**; only the class suffix changes.

### Semantic mapping — which variant for which real-world status

Don't invent a new mapping per project. If the target system's status names
differ from the examples, map by **meaning**, not by literal string:

| Meaning | Variant | Example labels seen so far |
|---|---|---|
| Active / normal / healthy / approved | `badge-success` | ทำงานปกติ, อนุมัติแล้ว, เสร็จสมบูรณ์, พร้อมใช้งาน |
| Pending / paused / needs attention, not yet failed | `badge-warning` | ลาพัก, รอดำเนินการ, รอตรวจสอบ |
| Inactive / failed / rejected / expired | `badge-danger` | พ้นสภาพ, ถูกปฏิเสธ, หมดอายุ, ยกเลิก |
| New / highlighted, not a health state | `badge-accent` | พนักงานใหม่, สินค้าใหม่, เพิ่งเข้าระบบ |
| Unknown / not categorized / archived | `badge-neutral` | ไม่ระบุ, ปิดการใช้งานถาวร |

If a status genuinely doesn't fit any of these five, ask before inventing a
sixth badge color — a new status color needs a matching light **and** dark
token pair added to both `:root` blocks (see `tokens-and-rules.md`), it's
not a one-line change.

### CSS classes involved (for context, don't rewrite these)

`.badge` (base shape/dot) + one of `.badge-success` / `.badge-warning` /
`.badge-danger` / `.badge-accent` / `.badge-neutral` (background/text/border
color only — do not add a sixth ad-hoc class).

## 2. Row / toolbar action icons

### The rule

Every action button in this system maps to **one specific icon**, always at
the same stroke width, always the same shape. If a target project shows a
"view details" action, an "edit" action, or a "delete" action, reuse the
exact `<svg>` below — don't pick a different glyph from a different icon set
(no filled icons, no Material Symbols, no emoji). All icons here share:
**24×24 viewBox, `fill="none"`, `stroke="currentColor"`, round linecap/
linejoin.** The stroke width and pixel size scale slightly by context (table
row = smaller, standalone toolbar button = larger) but the path data itself
never changes.

**View / open details** (row action — icon-only, primary, small):

```html
<button type="button" class="btn btn-icon btn-sm btn-primary" data-tooltip="เปิดดูรายละเอียด" aria-label="เปิดดูรายละเอียด">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>
```

**Edit** (two accepted forms — icon-only for toolbars, text button for
table rows next to the view-details icon button):

```html
<!-- icon-only (toolbar / card actions) -->
<button type="button" class="btn btn-icon btn-secondary" aria-label="แก้ไข">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 20h9M16.5 3.5a2.12 2.12 0 013 3L7 19l-4 1 1-4 12.5-12.5z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>

<!-- text button (paired with the view-details icon button in a table row) -->
<button type="button" class="btn btn-secondary btn-sm">แก้ไข</button>
```

**Delete** (icon-only, danger-outline — never solid danger for a row-level
delete, solid `.btn-danger` is reserved for a confirm-dialog's final action):

```html
<button type="button" class="btn btn-icon btn-danger-outline" aria-label="ลบ">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0l-1 14a2 2 0 01-2 2H7a2 2 0 01-2-2L4 6h16z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>
```

**Add / create** (leading icon inside a solid primary button, not icon-only):

```html
<button type="button" class="btn btn-primary btn-sm">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  เพิ่มรายการ
</button>
```

**Refresh**, **search**, **approve/confirm**, **close/dismiss** — same
family, reuse verbatim:

```html
<!-- refresh -->
<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 12a9 9 0 11-3-6.7M21 4v5h-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>

<!-- search (leading icon inside a search input) -->
<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M21 21l-4.3-4.3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>

<!-- approve / confirm -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>

<!-- close / dismiss (dialog close button, toast dismiss) -->
<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
```

### Sizing quick-reference

| Context | Icon px | stroke-width |
|---|---|---|
| Table row action (icon-only button) | 14px | 1.7–1.8 |
| Standalone icon-only button (toolbar/card) | 16px | 1.6–1.8 |
| Navbar / sidebar icon | 18px | 1.6–1.8 |
| Large standalone (dialog close, toast dismiss) | 20px | 2 |
| Small inline (add/plus inside a text button) | 14–15px | 2 |

### Icon-only button shape — the one rule most often missed

`.btn-icon` stays **square** (`--radius-md`, 6px corners) — it is the single
named exception to "all buttons are pill-shaped." If a "view details" or
"delete" button in a target project renders as a circle or a full pill, that
is the bug: it needs `class="btn btn-icon ..."` specifically, not just a
small square `.btn`. Never build an icon button by putting `border-radius:
50%` or `border-radius: 999px` directly on it.

## 3. Navbar / header

### The rule

The navbar is the single most visible element on every screen, so it's also
the element most often left half-converted — a project reskin that changes
buttons and tables but leaves the old header bar is an incomplete job, not a
partial one (unless the user explicitly scoped the request to skip
Navigation). The navbar is **one fixed structure**, not a layout to improvise
per project:

- Fixed height: `--header-height` (64px), full width of the content area
  (not the sidebar).
- Background: solid `var(--color-primary)` — the brand blue, **not** white,
  not a neutral/gray bar, not the dark sidebar color. This is one of the few
  places brand blue covers a large area on purpose.
- Left-to-right order, always: **hamburger/sidebar-toggle → system title
  (+ optional subtitle) → spacer → action icons, in this exact sequence:
  dark/light toggle, refresh, language dropdown, profile dropdown.**
  Don't reorder, and don't drop the hamburger even if the target project's
  sidebar can't collapse yet — add the behavior rather than removing the
  control.
- All icons/text inside the navbar are white (`color: #FFFFFF` or
  `rgba(255,255,255,.7-.85)` for secondary text) regardless of light/dark
  page mode — the navbar itself doesn't re-theme with dark mode, only its
  blue shifts slightly lighter (`--color-primary` already carries that via
  the dark-mode token override, nothing extra needed).

### Structure (copy verbatim, adjust only text/labels)

```html
<header class="main-header">
  <button type="button" class="navbar-toggle" aria-label="เปิด/ปิดเมนู" onclick="document.querySelector('.app-shell').classList.toggle('is-sidebar-collapsed')">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
  </button>

  <div class="system-title">
    ชื่อระบบ
    <span>คำอธิบายสั้นๆ ใต้ชื่อระบบ (ไม่บังคับ)</span>
  </div>

  <div class="navbar-actions">
    <button type="button" class="navbar-icon-btn" id="colorSchemeToggle" onclick="toggleColorScheme()" data-tooltip="สลับโหมดสว่าง/มืด" aria-label="สลับโหมดสว่าง/มืด">
      <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
    <button type="button" class="navbar-icon-btn" data-tooltip="รีเฟรชหน้า" aria-label="รีเฟรชหน้า">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 12a9 9 0 11-3-6.7M21 4v5h-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>

    <div class="dropdown" id="navLangDropdown">
      <button type="button" class="navbar-select" onclick="toggleDropdown('navLangDropdown')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18" stroke="currentColor" stroke-width="1.6"/></svg>
        TH
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="dropdown-menu">
        <button type="button" class="dropdown-item">ไทย (TH)</button>
        <button type="button" class="dropdown-item">English (EN)</button>
      </div>
    </div>

    <div class="dropdown navbar-profile-wrap" id="navProfileDropdown">
      <button type="button" class="header-profile" onclick="toggleDropdown('navProfileDropdown')">
        <div class="who">
          <div class="u-name">ชื่อผู้ใช้</div>
          <div class="u-role">ตำแหน่ง</div>
        </div>
        <div class="avatar">XX</div>
        <svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="dropdown-menu"><!-- profile menu items --></div>
    </div>
  </div>
</header>
```

### What "the navbar didn't change" usually means in practice

- The target project already had its own header component (often a
  different height, a white/neutral background, or icons in a different
  order) and it was left as-is while other components were reskinned. Check
  `.main-header`-equivalent explicitly — it's easy to scroll past because it
  sits above the fold and isn't scrolled into view while working on the
  page body.
- The color-scheme toggle button (`#colorSchemeToggle`) was omitted — this
  is new (added when dark/light mode shipped) and easy to forget if the
  target project's header was reskinned before dark mode was added; go back
  and add it if the project has dark mode at all.
- CSS classes were renamed/rewritten instead of reused verbatim, so the
  `--color-primary` background silently fell back to a default and the
  header rendered in the framework's own default color instead of brand
  blue.

## 4. Before finishing a badge/icon-button/navbar change

- [ ] Every status uses `<span class="badge badge-{variant}">`, no hand-built
      alternative, no icon added inside a badge.
- [ ] Status → variant mapping follows § 1's meaning table, not a guess.
- [ ] Every row/toolbar action icon matches one of the exact SVGs in § 2 —
      same path data, same stroke-linecap/linejoin, no swapped icon set.
- [ ] Every icon-only button has `class="btn btn-icon ..."` and stays square
      — never circular, never pill.
- [ ] The navbar/header was actually checked, not skipped — background is
      brand blue, action order matches § 3, and the dark/light toggle button
      is present if the project has dark mode.
