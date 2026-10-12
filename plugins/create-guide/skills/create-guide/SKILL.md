---
name: create-guide
description: สร้างคู่มือการใช้งาน (user guide / manual) เป็นไฟล์ HTML standalone สำหรับ module ในโปรเจค — รวม 4 แหล่งข้อมูล (CLAUDE.md + Source Code + Routes + Screenshot Vision) รองรับหลาย framework, ภาษา th / en / th+en, Playwright auto-capture (PC + mobile) และ auth แบบปลอดภัย ใช้เมื่อผู้ใช้ขอ "สร้างคู่มือ", "ทำ user guide", "create guide", "เขียนคู่มือ module"
metadata:
  author: Narawit
  created: 2026-06-26
  updated: 2026-10-12
  tags: [documentation, guide, html, capture, bilingual]
  status: stable
---

> **คำนำ — อ่านก่อนเริ่มทำงานทุกครั้ง**
>
> command นี้สร้างคู่มือการใช้งาน HTML แบบ standalone สำหรับ module ใดก็ได้ในโปรเจค
> โดยรวบรวมข้อมูลจาก **4 แหล่ง** พร้อมกัน ได้แก่ CLAUDE.md (สี/convention ของ module),
> Source Code (ปุ่ม/form/dialog ที่มีจริง), Route Structure (path และ menu label),
> และ Screenshot Vision (รูปหน้าจอจริงที่ capture ไว้)
>
> ผลลัพธ์คือ **ไฟล์ HTML ไฟล์เดียว** — รูปทุกรูป embed เป็น base64 แชร์ได้ทันที
> ไม่ต้องมี server ไม่ต้องติดตั้งอะไรเพิ่ม เปิดด้วย browser ได้เลย
>
> **โหมด `--capture`** จะให้ Playwright เข้าระบบและ screenshot ทุกหน้าให้อัตโนมัติ **2 viewport**
> — 🖥️ **PC** (1440×900) เพื่อเห็น layout เต็มจอ และ 📱 **Mobile** (390×844) เพื่อเห็นรายละเอียดชัดขึ้น
> ในคู่มือ HTML แต่ละหน้าจะมีปุ่ม `🖥️ PC` / `📱 Mobile` สลับดูได้ในคลิกเดียว
> credential จะไม่ถูกเก็บในโค้ด — ใช้ session token แทน เก็บที่ `~/docs/<projectName>/` นอก project directory
> ก่อน screenshot ทุกครั้ง script จะซ่อน **React Query DevTools / TanStack Query DevTools**
> โดยอัตโนมัติด้วย JavaScript inject เพื่อป้องกัน panel บัง form หรือเนื้อหาในหน้า
> ถ้าต้องการ PC เท่านั้น → เพิ่ม `--no-mobile`
>
> **ถ้าไม่ใส่ `--capture`** → ใช้รูปที่วางไว้ใน `~/docs/<projectName>/images/` แทน
> เหมาะกับกรณีที่ capture ไว้แล้ว หรือต้องการ update เนื้อหาโดยไม่ capture ใหม่

---

สร้างคู่มือการใช้งาน HTML สำหรับ module: **$ARGUMENTS**

**รูปแบบ argument:**
```
/create-guide <moduleName>                          → ภาษาไทยอย่างเดียว (default)
/create-guide <moduleName> en                       → ภาษาอังกฤษอย่างเดียว
/create-guide <moduleName> th+en                    → 2 ภาษา มี toggle ปุ่มสลับภาษาใน sidebar
/create-guide <moduleName> --capture                → ไทย + ถามแผน + Playwright auto-capture (PC + mobile)
/create-guide <moduleName> en --capture             → อังกฤษ + ถามแผน + auto-capture (PC + mobile)
/create-guide <moduleName> th+en --capture          → 2 ภาษา + toggle + ถามแผน + auto-capture (PC + mobile)
/create-guide <moduleName> --capture --no-mobile    → capture เฉพาะ PC (ข้าม mobile viewport)
/create-guide <moduleName> --capture --replan       → capture ใหม่ + ถามแผนใหม่ทั้งหมด
/create-guide <moduleName> --capture --recapture    → capture รูปใหม่ทุกรูป (ไม่ใช้ cache รูป)
/create-guide <moduleName> --fresh                  → ล้าง cache ทั้งหมด + capture ใหม่ทุกอย่าง
/create-guide <moduleName> --refresh-code           → อ่าน source code ใหม่ทุก slug
```

**Skip flags — ใช้ลด token เมื่อต้องการข้ามขั้นตอนบางส่วน:**
```
── ข้าม capture steps ──
--no-plan          → ข้ามการถามแผน ใช้ extraCaptures เดิม (หรือ overview only ถ้าไม่มี)
--overview-only    → capture overview PC+mobile เท่านั้น ไม่ capture dialog/extra ใดๆ

── ข้าม source reading ──
--no-code          → ข้ามการ Glob + อ่าน source code ทุก slug (ใช้ cache เดิม หรือ routes only)
--no-vision        → ข้าม vision analysis รูปทั้งหมด ใช้ filename pattern detect type แทน

── ข้ามเกือบทุกอย่าง ──
--html-only        → สร้าง HTML จาก cache ที่มีอยู่เท่านั้น ข้าม auth + capture + sources ทั้งหมด
                     (ถ้า cache ขาด → แจ้งและดำเนินการต่อด้วยข้อมูลที่มี)

── shorthand รวม ──
--lite             → ย่อ: --no-plan --overview-only --no-vision  (token น้อยที่สุด ยังคง capture)
```

**ตาราง token ที่ประหยัดได้ (โดยประมาณ):**
| flag | ข้ามขั้นตอน | token ที่ประหยัด |
|---|---|---|
| `--no-plan` | ถามแผน capture | ~500–1,000 |
| `--no-code` | Glob + read source code | ~2,000–5,000 |
| `--no-vision` | vision analysis รูป (ต่อรูป) | ~800–2,000 ต่อรูป |
| `--overview-only` | extra capture steps | ~200–500 |
| `--html-only` | auth + capture + 4 sources | ~80–95% ของทั้งหมด |
| `--lite` | plan + extra capture + vision | ~60–80% |

---

## ขั้นตอนที่ 0 — Parse Arguments + ตรวจสอบโปรเจค

### 0-A  Parse $ARGUMENTS
```
parts        = trim("$ARGUMENTS").split(/\s+/)
moduleName   = parts[0]                          # เช่น "basket-circulation"
langMode     = parts.find(p => ["th","en","th+en"].includes(p)) ?? "th"

# ── capture flags ──────────────────────────────────────────────
captureMode  = parts.includes("--capture")       # true | false
mobileMode   = !parts.includes("--no-mobile")   # false = PC only
replanMode   = parts.includes("--replan")        # ถามแผนใหม่ทั้งหมด
recaptureMode= parts.includes("--recapture")     # capture รูปใหม่ทุกรูป

# ── skip flags (ลด token) ──────────────────────────────────────
noPlanMode   = parts.includes("--no-plan")       # ข้ามการถามแผน
overviewOnly = parts.includes("--overview-only") # capture overview เท่านั้น
noCodeMode   = parts.includes("--no-code")       # ข้าม source code reading
noVisionMode = parts.includes("--no-vision")     # ข้าม vision analysis
htmlOnlyMode = parts.includes("--html-only")     # ข้ามทุกอย่าง สร้าง HTML จาก cache

# ── shorthand ─────────────────────────────────────────────────
if parts.includes("--lite"):
  noPlanMode = overviewOnly = noVisionMode = true  # ขยาย --lite เป็น 3 flags

# ── html-only implies no-capture ──────────────────────────────
if htmlOnlyMode:
  captureMode = false   # ไม่มีประโยชน์ capture เพราะต้องการแค่ HTML
```

**Decision tree ก่อนเริ่มงาน:**
```
htmlOnlyMode = true  → ข้าม Step 0-D, 0-E, 0-F, 1 ทั้งหมด → ไป Step 2 ทันที (ใช้ cache)
captureMode  = false → ข้าม Step 0-D, 0-E
noPlanMode   = true  → ข้าม Step 0-E.1 (planning dialog)
overviewOnly = true  → ใน capture loop: ข้าม extraCaptures ทุกหน้า
noCodeMode   = true  → ข้าม Source 3 (อ่านได้จาก cache ถ้ามี)
noVisionMode = true  → ข้าม Source 4 vision read (ใช้ filename-based type)
```

### 0-B  หา Project Name + Framework

อ่าน `package.json` (parallel กับ `composer.json` ถ้ามี):
- `projectName` = field `name`  (ถ้าไม่มี → ชื่อ folder ของ working directory)
- ตรวจ `dependencies` + `devDependencies` เพื่อ detect framework:

| dependency พบ | framework | routePattern |
|---|---|---|
| `"next"` | `nextjs` | `src/app/**/page.tsx`, `src/pages/**/*.tsx`, `src/constants/menu.ts` |
| `"nuxt"` / `"nuxt3"` | `nuxt` | `pages/**/*.vue`, `composables/`, `server/routes/` |
| `"vue"` + `"vue-router"` | `vue-spa` | `src/router/*.{js,ts}`, `src/views/**/*.vue` |
| `"@angular/core"` | `angular` | `src/app/**/*-routing.module.ts`, `src/app/**/*.routes.ts` |
| `"gatsby"` | `gatsby` | `src/pages/**/*.{tsx,jsx}` |
| ไม่ตรงใดเลย | `generic` | Glob `src/**/{page,route,screen,view,Page}*.{tsx,vue,jsx,py}` |

### 0-C  Docs Root

```
docsRoot      = ~/docs/<projectName>/
imagesDir     = ~/docs/<projectName>/images/
configFile    = ~/docs/<projectName>/guide.config.json
authFile      = ~/docs/<projectName>/auth.json        ← session เท่านั้น ไม่มี password
captureEnvFile = ~/docs/<projectName>/capture.env     ← CAPTURE_USER/CAPTURE_PASS นอก project dir
```

สร้าง folder ถ้ายังไม่มี:
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\docs\<projectName>\images"
```

---

## ขั้นตอนที่ 0-D — Auth Setup  *(รันเฉพาะเมื่อ captureMode = true)*

ถ้า `captureMode = false` → ข้ามขั้นตอนนี้ ไม่ต้องอ่านไฟล์ · ถ้า `true` → อ่าน `reference/auth.md` (ในโฟลเดอร์เดียวกับ SKILL.md นี้) แล้วทำตามทั้งหมด

---

## ขั้นตอนที่ 0-E — Auto Capture  *(รันเฉพาะเมื่อ captureMode = true)*

ถ้า `captureMode = false` → ข้ามขั้นตอนนี้ ไม่ต้องอ่านไฟล์ · ถ้า `true` → อ่าน `reference/capture.md` (ในโฟลเดอร์เดียวกับ SKILL.md นี้) แล้วทำตามทั้งหมด

---

## ขั้นตอนที่ 0-F — ตรวจสอบ Cache ก่อนทำงาน

> **เป้าหมาย:** ข้ามงานที่ทำแล้ว ทำเฉพาะที่ขาด — ยกเว้น HTML ที่ต้องสร้างใหม่เสมอ

ตรวจสอบทั้งหมดนี้ก่อนเริ่ม Step 1:

```
cacheState = {
  claudeMd:     มีข้อมูลใน guide.config.json → modules[moduleName].meta แล้วหรือไม่
  routes:       มี routes ใน guide.config.json → modules[moduleName].routes แล้วหรือไม่
  sourceCode:   มีข้อมูลใน guide.config.json → modules[moduleName].pages[slug] แล้วหรือไม่  (ต่อ slug)
  images:       ไฟล์รูปมีอยู่ใน ~/docs/<projectName>/images/ แล้วหรือไม่               (ต่อ slug)
  html:         ❌ ไม่ cache — สร้างใหม่เสมอ
}
```

แสดงสรุป cache status ก่อนเริ่ม (รวม skip flags ที่ active):

```
⚡ Cache check — basket-circulation
   Active flags: --no-vision --overview-only

  Source 1  CLAUDE.md meta     ✅ cached → ข้าม
  Source 2  Routes             ✅ cached → ข้าม
  Source 3  Source code
              bc-domains       ✅ cached → ข้าม
              bc-basket        ✅ cached → ข้าม
              bc-trade         ❌ ไม่มี  → อ่านใหม่
              bc-void          ❌ ไม่มี  → อ่านใหม่
  Source 4  Screenshots (vision)
              bc-domains.png               ✅ มีแล้ว → ข้าม (PC)
              bc-domains-mobile.png        ✅ มีแล้ว → ข้าม (📱)
              bc-domains-dialog-create.png ✅ มีแล้ว → ข้าม
              bc-trade.png                 ❌ ไม่มี  → capture ใหม่ (PC)
              bc-trade-mobile.png          ❌ ไม่มี  → capture ใหม่ (📱)
              bc-void.png                  ❌ ไม่มี  → capture ใหม่ (PC)
              bc-void-mobile.png           ❌ ไม่มี  → capture ใหม่ (📱)
              vision analysis              ⏭️  [--no-vision] ข้าม — ใช้ filename pattern
  Capture   extra steps                   ⏭️  [--overview-only] ข้าม — overview only
  HTML      <moduleName>-guide.html       🔄 สร้างใหม่เสมอ

ประหยัดได้: ~75% token (cache 2 slug + CLAUDE.md + routes + ข้าม vision + ข้าม extra)
```

> ถ้ารัน `--html-only` → แสดงแค่:
> ```
> ⚡ [--html-only] ข้ามทุก source step — ใช้ cache ทั้งหมด
>    meta✅  routes✅  pages(4/4)✅  images(12 ไฟล์)✅  → สร้าง HTML ทันที
> ```

**กฎแต่ละ source:**

| Source | cache ที่ไหน | invalidate เมื่อไหร่ |
|---|---|---|
| CLAUDE.md meta | `guide.config.json → modules[mod].meta` | ไม่มี `meta` key / รัน `--refresh-meta` |
| Routes | `guide.config.json → modules[mod].routes` | ไม่มี `routes` key / รัน `--refresh-routes` |
| Source code (ต่อ slug) | `guide.config.json → modules[mod].pages[slug]` | ไม่มี `pages[slug]` key / รัน `--refresh-code` |
| รูปภาพ (ต่อไฟล์) | ไฟล์มีอยู่ใน `images/` | ไฟล์ไม่มี / รัน `--recapture` |
| vision cache (ต่อไฟล์) | `imageCache[filename]` ใน guide.config.json | ไม่มี key / รัน `--refresh-images` |
| HTML | — | **สร้างใหม่เสมอ** |

**`--refresh-*` flags เพิ่มเติม:**
```
--refresh-meta    → ล้าง cache CLAUDE.md แล้วอ่านใหม่
--refresh-routes  → ล้าง cache routes แล้วอ่านใหม่
--refresh-code    → ล้าง cache source code ทุก slug แล้วอ่านใหม่
--refresh-images  → ล้าง imageCache ทุก entry แล้ว vision-อ่านรูปใหม่ทั้งหมด
                    ใช้เมื่อ: วางรูปทับด้วยรูปใหม่ (ชื่อเดิม เนื้อหาใหม่)
                    หรือ: เพิ่มรูปเองแล้วต้องการให้ HTML สะท้อนเนื้อหาในรูป
--recapture       → capture รูปใหม่ทุกรูป (ไม่สนว่ามีอยู่แล้ว) — ต้องใช้กับ --capture
--fresh           → ล้าง cache ทั้งหมด (เทียบเท่ารัน flags ทั้ง 5 พร้อมกัน)
```

**โครงสร้าง cache ใน `guide.config.json`:**
```json
{
  "baseUrl": "http://localhost:3000",
  "framework": "nextjs",
  "modules": {
    "basket-circulation": {
      "meta": {
        "color": "green",
        "description": "ระบบหมุนเวียนตะกร้า",
        "conventions": { "badge": "สีเขียว=active", "button": "outline style" },
        "routePrefix": "/api/bc",
        "cachedAt": "2025-06-10T10:00:00Z"
      },
      "routes": [
        { "slug": "bc-domains", "path": "/basket-circulation/domains", "title": "Domains" }
      ],
      "pages": {
        "bc-domains": {
          "buttons":    [{ "label": "Add Domain", "type": "dialog" }],
          "formFields": ["Domain Name", "Basket Size", "Quota Limit"],
          "dialogs":    ["Create Domain", "Update Quota"],
          "description": "จัดการ Domain ที่เป็นเจ้าของตะกร้า",
          "cachedAt": "2025-06-10T10:00:00Z"
        },
        "bc-trade": null
      },
      "extraCaptures": { }
    }
  }
}
```

> `pages[slug] = null` หมายถึง slug นี้ยังไม่ได้ scan source code
> ถ้า key ไม่มีเลย → ถือว่า null เช่นกัน

---

## ขั้นตอนที่ 1 — รวบรวม 4 Sources พร้อมกัน (parallel)

อ่านเฉพาะ source ที่ยังไม่มี cache (ดู Step 0-F):

### Source 1 — CLAUDE.md
**ข้าม** ถ้า `guide.config.json → modules[moduleName].meta` มีข้อมูลอยู่แล้ว

อ่าน `CLAUDE.md` จาก working directory (ถ้ามี) แล้ว extract:
- `moduleColor` — สีประจำ module
- `moduleDescription` — คำอธิบาย module
- `conventions` — UI conventions
- `routePrefix` — API/route prefix

บันทึกลง `guide.config.json → modules[moduleName].meta` พร้อม `cachedAt`

### Source 2 — Route Structure
**ข้าม** ถ้า `guide.config.json → modules[moduleName].routes` มีข้อมูลอยู่แล้ว

อ่านพร้อมกันตาม `framework` ที่ detect ได้จาก Step 0-B:

**Fallback chain (ลองตามลำดับ หยุดเมื่อพบ route):**
```
1. ~/docs/<projectName>/guide.config.json   → modules[moduleName].routes
2. Framework-specific route file            → ตาม routePattern ของ framework
3. Glob src/**/<moduleName>*/**/*.{tsx,vue} → infer จาก folder + filename
4. ถ้ายังไม่พบ → แจ้ง user ระบุ path เอง
```

**Next.js เพิ่มเติม:** อ่าน `src/constants/menu.ts` (ถ้ามี) → หา array ชื่อ `<moduleName>SubMenu`
**Vue SPA เพิ่มเติม:** อ่าน `src/router/*.{js,ts}` → หา children routes ของ module

สร้าง `routeList` แล้วบันทึกลง `guide.config.json → modules[moduleName].routes`:
```
[{ slug, path, title, menuLabel }, ...]
```

### Source 3 — Source Code

> **ข้ามทั้ง Source 3 ถ้า `noCodeMode = true` (`--no-code`)**
> → ใช้ `pages[slug]` จาก cache ที่มีอยู่ใน `guide.config.json`
> → slug ที่ cache ขาด (`null` / key ไม่มี) → ใส่ `pages[slug] = {}` (empty, ไม่มี action-map/steps จาก code)
> → แสดง: `⏭️  [--no-code] ข้าม source code reading — cache: bc-domains✅ bc-trade❌(empty)`
> → ในคู่มือ HTML: หน้าที่ไม่มี code data → ไม่แสดง action-map แต่ยังแสดง screenshot + steps จาก vision

**ข้าม slug ที่** `guide.config.json → modules[moduleName].pages[slug]` มีข้อมูลอยู่แล้ว
**อ่านเฉพาะ slug ที่** `pages[slug]` เป็น `null` หรือ key ไม่มี

Glob และอ่านพร้อมกันเฉพาะ slug ที่ขาด:
- `src/features/$ARGUMENTS/<slug>/**/*.tsx`
- `src/app/**/<slug>*/**/page.tsx`

Extract สำหรับแต่ละ slug:
- **buttons** — label + type (`nav | submit | dialog | delete`) + target slug
- **formFields** — ชื่อ field ที่ user กรอก
- **dialogs** — Sheet/Dialog ที่เปิดในหน้านี้
- **description** — หน้านี้ทำอะไร

บันทึกลง `guide.config.json → modules[moduleName].pages[slug]` พร้อม `cachedAt`

### Source 4 — Screenshot Vision

> **ข้ามทั้ง Source 4 ถ้า `noVisionMode = true` (`--no-vision`)**
> → ไม่ส่งรูปใด ๆ ให้ Claude วิเคราะห์ ประหยัด token ได้มากที่สุด
> → ใช้ **filename pattern** ตัดสิน `imageType` แทน:
> ```
> filename pattern          → imageType
> ───────────────────────────────────────
> slug.png                  → "overview-pc"
> slug-mobile.png           → "overview-mobile"
> slug-dialog-*.png         → "dialog"
> slug-zoom-*.png           → "zoom"
> slug-btn-*.png            → "btn"
> slug-step-N.png           → "step"
> ```
> → `visibleText = ""` / `uiElements = []` / `pageState = "unknown"`
> → ในคู่มือ HTML: ยังฝัง screenshot ครบ แต่ caption + step text มาจาก source code เท่านั้น
> → แสดง: `⏭️  [--no-vision] ข้าม vision analysis — ใช้ filename-based type (8 รูป)`

**ข้าม รูปที่** มี `imageCache[filename]` ใน `guide.config.json` อยู่แล้ว
**อ่าน vision เฉพาะ รูปที่ไม่มี cache** (ไฟล์ใหม่ หรือถูก invalidate)

Glob รูปใน `~/docs/<projectName>/images/<moduleName>-*.{png,jpg,jpeg}` แล้วแบ่ง:
```
ไฟล์ใหม่ (ไม่มี imageCache key)   → อ่าน vision → extract imageType, visibleText, uiElements, pageState
ไฟล์มี imageCache อยู่แล้ว        → ใช้ข้อมูล cache ← ข้ามอ่าน vision
--refresh-images                   → ล้าง imageCache ทุก entry แล้วอ่าน vision ใหม่ทั้งหมด
```

> **กรณีที่ต้อง `--refresh-images`:**
> - วางรูปทับด้วยรูปใหม่ (ชื่อไฟล์เดิม เนื้อหาใหม่) เช่น capture มาใหม่แทนรูปเดิมที่ฟีเจอร์ยังไม่ครบ
> - เพิ่มรูปเองหลายไฟล์แล้วต้องการให้ caption/steps ใน HTML สะท้อนเนื้อหาในรูปจริง
>
> **ถ้าแค่เพิ่มไฟล์ใหม่ (ชื่อใหม่):** รัน `/create-guide <moduleName>` ปกติ ไม่ต้อง `--refresh-images`

บันทึก vision result ลง `guide.config.json → modules[moduleName].imageCache[filename]`

**Naming convention:**

| Pattern | ตัวอย่าง | ความหมาย |
|---|---|---|
| `slug.png` | `bc-domains.png` | Overview ฝั่ง PC (1440×900) — หลัก |
| `slug-mobile.png` | `bc-domains-mobile.png` | Overview ฝั่ง mobile (390×844) — แท็บ 📱 |
| `slug-2.png` | `bc-domains-2.png` | Secondary overview PC |
| `slug-dialog-xxx.png` | `bc-domains-dialog-create.png` | Dialog ที่เปิดในหน้า |
| `slug-zoom-xxx.png` | `bc-domains-zoom-toolbar.png` | Zoom เฉพาะส่วน |
| `slug-btn-xxx.png` | `bc-trade-btn-scan.png` | ปุ่มเฉพาะชิ้น |
| `slug-step-N.png` | `bc-trade-step-2.png` | ภาพขั้นตอนที่ N |

สำหรับแต่ละรูป → อ่านด้วย vision แล้ว extract imageType, visibleText, uiElements, pageState, slug, context

---

## ขั้นตอนที่ 2 — Page Match

สร้าง `pageMap` โดย merge ข้อมูลจากทุก source แล้วแสดงสรุป:

```
📋 Page Match สำหรับ module: $ARGUMENTS

  slug             path                              รูป
  ──────────────── ─────────────────────────────── ─────────────────────────────────────
  ✅ bc-domains    /basket-circulation/domains      overview✅  dialog✅  zoom✅
  ✅ bc-basket     /basket-circulation/basket       overview✅
  ⚠️  bc-trade     /basket-circulation/trade        overview✅  btn❌
  ✅ bc-void       /basket-circulation/void         overview✅  dialog✅

CLAUDE.md : ✅ พบ  (color: green, conventions: ✅)
Capture   : ✅ auto-captured ด้วย Playwright  (หรือ "📁 ใช้รูปจาก images/ ที่มีอยู่")
```

**กฎ synthesis:**
- ถ้า Source 4 (vision) ขัดแย้งกับ Source 3 (code) → เชื่อ Source 4
- ถ้าไม่มีรูป overview → ใช้รูปแรกที่มีแทน
- ถ้าไม่มีรูปเลยสักหน้า → แสดงรายการที่ต้องเตรียมแล้วหยุด

**กฎ langMode:**
| langMode | สร้าง TH | สร้าง EN | HTML output |
|---|---|---|---|
| `th` | ✅ | ❌ | ข้อความไทย ไม่มี toggle |
| `en` | ❌ | ✅ | ข้อความอังกฤษ ไม่มี toggle |
| `th+en` | ✅ | ✅ | มี toggle ค่าเริ่มต้นไทย |

**กฎการใช้รูป multi-image:**
- `overview` → รูปหลักบนสุดของ section
- `dialog` → แสดงใน step ที่เกี่ยวกับการเปิด dialog ด้วย `.img-zoom`
- `zoom` → แสดงใน step หรือ action-map ด้วย `.img-zoom`
- `btn` → แสดง inline ใน step ด้วย `<img class="img-inline">`
- `step-N` → แสดงใน step ที่ N ตรงกัน

---

## ขั้นตอนที่ 3 — Encode รูปเป็น Base64

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$env:USERPROFILE\docs\<projectName>\images\<filename>"))
```

เก็บเป็น `imageData = { "<slug>": "data:image/png;base64,<encoded>" }`

---

## ขั้นตอนที่ 4 — สร้าง HTML Guide

อ่าน `reference/html.md` (ในโฟลเดอร์เดียวกับ SKILL.md นี้) แล้วทำตามทั้งหมด

---

## Output

| สิ่งที่สร้าง | Path |
|---|---|
| Config (ครั้งแรก) | `~/docs/<projectName>/guide.config.json` |
| Capture credential (ถ้าบันทึก) | `~/docs/<projectName>/capture.env` ← นอก project ปลอดภัย |
| Session (ถ้า capture) | `~/docs/<projectName>/auth.json` ← นอก project ปลอดภัย |
| Screenshots (ถ้า capture) | `~/docs/<projectName>/images/*.png` |
| HTML (th) | `~/docs/<projectName>/<moduleName>-guide.html` |
| HTML (en) | `~/docs/<projectName>/<moduleName>-guide-en.html` |
| HTML (th+en) | `~/docs/<projectName>/<moduleName>-guide-bilingual.html` |

HTML standalone — รูปทั้งหมด embed base64 แชร์ได้ทันที ไม่ต้องมี server

---

## ตัวอย่าง command

**Standard (ใช้ cache + สร้าง HTML ใหม่):**
```
/create-guide basket-circulation                          → ไทย (cache ทุก source, HTML ใหม่)
/create-guide basket-circulation en                       → อังกฤษ
/create-guide basket-circulation th+en                    → 2 ภาษา + toggle
```

**Capture (Playwright auto-screenshot):**
```
/create-guide basket-circulation --capture                → ถามแผน + capture PC+mobile เฉพาะที่ขาด
/create-guide basket-circulation --capture --no-mobile    → capture PC เท่านั้น
/create-guide basket-circulation --capture --replan       → capture + ถามแผนใหม่ทั้งหมด
/create-guide basket-circulation --capture --recapture    → capture รูปใหม่ทุกรูป
/create-guide basket-circulation th+en --capture          → 2 ภาษา + toggle + capture
```

**Skip flags (ลด token):**
```
/create-guide basket-circulation --capture --no-plan      → capture ไม่ถามแผน (ใช้ extraCaptures เดิม)
/create-guide basket-circulation --capture --overview-only → capture overview PC+mobile เท่านั้น
/create-guide basket-circulation --capture --no-vision    → capture แต่ข้าม vision analysis
/create-guide basket-circulation --no-code                → HTML จาก routes + cache (ไม่อ่าน source)
/create-guide basket-circulation --html-only              → HTML จาก cache ทั้งหมด (เร็วที่สุด)
```

**Shorthand / Combo:**
```
/create-guide basket-circulation --capture --lite         → capture + ข้ามแผน + overview + ข้าม vision
/create-guide basket-circulation --capture --no-plan --no-vision  → capture เงียบ ไม่ถาม ไม่ vision
/create-guide basket-circulation th+en --html-only        → 2 ภาษา สร้าง HTML จาก cache ทันที
```

**เพิ่มรูปเอง แล้วสร้าง HTML ใหม่:**
```
/create-guide basket-circulation                          → สร้าง HTML ใหม่ + auto-pick รูปใหม่ (ชื่อใหม่)
/create-guide basket-circulation --refresh-images         → vision-อ่านรูปใหม่ทั้งหมด + สร้าง HTML
                                                            (ใช้เมื่อวางรูปทับชื่อเดิม หรือแก้ไขรูปเดิม)
/create-guide basket-circulation --no-vision              → สร้าง HTML ใหม่เร็วที่สุด (ไม่ vision)
```

**Cache management:**
```
/create-guide basket-circulation --refresh-code           → อ่าน source code ใหม่ทุก slug
/create-guide basket-circulation --refresh-images         → vision-อ่านรูปใหม่ทุกรูป (ล้าง imageCache)
/create-guide basket-circulation --fresh                  → ล้าง cache ทั้งหมด + capture ใหม่ทุกอย่าง
/create-guide receiving --capture                         → module อื่น
```
