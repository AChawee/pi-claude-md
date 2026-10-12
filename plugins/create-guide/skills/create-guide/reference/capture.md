## ขั้นตอนที่ 0-E — Auto Capture  *(รันเฉพาะเมื่อ captureMode = true)*

> ถ้า `captureMode = false` → ข้ามขั้นตอนนี้ ไปที่ขั้นตอนที่ 1

> ⚠️ **คำเตือนด้านความปลอดภัย — แจ้งผู้ใช้ก่อน capture ทุกครั้ง:**
> รูปภาพที่ capture อาจมีข้อมูลจริงของผู้ใช้ปรากฏอยู่ (ชื่อ, รหัสออเดอร์, ยอดเงิน ฯลฯ)
> หากต้องการสร้างคู่มือเพื่อแชร์ภายนอก → ใช้ข้อมูล demo/staging แทน production
> HTML output ที่สร้างจะ embed รูปทั้งหมดเป็น base64 — การแชร์ไฟล์ HTML = แชร์รูปทั้งหมดด้วย

### 0-E.1 — Interactive Planning (ถามก่อน capture เสมอ)

> **ข้าม step นี้ถ้า:**
> - `noPlanMode = true` (`--no-plan`) → ใช้ `extraCaptures` ใน `guide.config.json` ที่มีอยู่
>   ถ้าหน้าใดยังไม่มี `extraCaptures` → capture overview only สำหรับหน้านั้น
>   แสดงข้อความ: `⏭️  [--no-plan] ข้ามการวางแผน — ใช้ extraCaptures เดิม (bc-domains✅ bc-trade⬜→overview)`
> - `overviewOnly = true` (`--overview-only`) → ข้ามทันที ไม่ถาม ไม่ใช้ extraCaptures ใด ๆ ทั้งสิ้น
>   แสดง: `⏭️  [--overview-only] ข้ามการวางแผน — capture overview PC+📱 เท่านั้น`
> - `replanMode = false` + ทุกหน้ามี `extraCaptures` อยู่แล้ว → ใช้ค่าเดิม ไม่ถามซ้ำ

ก่อนเริ่ม capture ให้ scan source code ของแต่ละหน้าใน module แล้ว **ถามผู้ใช้ทีละหน้า** ว่า dialog/ปุ่มไหนควรเปิดเพื่อถ่ายรูป

แสดงผลในรูปแบบนี้และรอคำตอบ:

```
╔══════════════════════════════════════════════════════════════════╗
║  🗂️  วางแผน capture สำหรับ: basket-circulation                  ║
║      พบ 4 หน้า — กรุณาตอบทีละหน้า                               ║
╚══════════════════════════════════════════════════════════════════╝

─────────────────────────────────────────
📄 หน้า 1/4: Domains  (/basket-circulation/domains)
─────────────────────────────────────────
พบ interactive elements ดังนี้:

  Dialogs / Sheets ที่เปิดได้:
    [A] "Add Domain"     → Sheet เพิ่ม Domain ใหม่        (trigger: button "Add Domain")
    [B] "Update Quota"   → Dialog แก้ไข Quota             (trigger: button "Edit" ในแถว)
    [C] "Domain Detail"  → Sheet รายละเอียด Domain        (trigger: button "Details" ในแถว)

  ปุ่มอื่น ๆ ที่พบ:
    [D] "Delete"         → ⚠️  submit/delete — ไม่แนะนำ capture
    [E] "Save"           → ⚠️  submit form — ไม่แนะนำ capture
    [F] filter dropdown  → dropdown เลือก filter (ดูได้ปลอดภัย)

เลือก elements ที่ต้องการ capture (เช่น: A C F)
หรือ [S] ข้ามหน้านี้ / [ALL-SAFE] เลือกทุกตัวที่ไม่ใช่ submit :
```

**กฎการจัดกลุ่ม** (scan จาก source code + label):

| สัญญาณที่พบใน code | จัดเป็น | แนะนำ |
|---|---|---|
| `onClick` → open Sheet/Dialog state | `nav-dialog` | ✅ capture ได้ |
| `href` / `router.push` | `nav-page` | ✅ capture ได้ |
| `mutation.mutate` / `form.handleSubmit` | `submit` | ⚠️ ไม่แนะนำ |
| `onDelete` / `method: DELETE` | `delete` | ⚠️ ไม่แนะนำ |
| dropdown/select ที่ไม่ submit | `nav-filter` | ✅ capture ได้ |
| tooltip / hover state | `nav-hover` | ✅ capture ได้ |

หลังผู้ใช้ตอบแต่ละหน้า → บันทึกเป็น `extraCaptures` ลง `guide.config.json` อัตโนมัติ แล้วถามหน้าถัดไป

เมื่อตอบครบทุกหน้าแล้ว แสดงสรุปก่อน capture จริง:

```
╔══════════════════════════════════════════════════════════════════╗
║  ✅  แผน capture สำหรับ basket-circulation                       ║
╚══════════════════════════════════════════════════════════════════╝

  bc-domains    overview (PC+📱) + [A] Add Domain sheet + [C] Domain Detail + [F] filter
  bc-basket     overview (PC+📱) เท่านั้น (ข้ามตามที่เลือก)
  bc-trade      overview (PC+📱) + [A] Scan dialog + [D] Status tooltip
  bc-void       overview (PC+📱) + [A] Void Reason dialog

  รวม: 4 หน้า / ~11 รูป PC + ~4 รูป mobile = ~15 รูป / ไม่มี submit action เลย ✅
  📱 mobile capture ทุกหน้า (390×844)  |  ปิดด้วย --no-mobile

[Enter] เริ่ม capture  |  [E] แก้ไขแผน :
```

> **สำคัญ:** ถ้า `guide.config.json` มี `extraCaptures` อยู่แล้วในหน้านั้น →
> ข้ามการถามและใช้ค่าที่มีอยู่ได้เลย ไม่ต้องถามซ้ำ
> เว้นแต่ผู้ใช้รัน `/create-guide <module> --capture --replan` → ถามใหม่ทั้งหมด

อ่าน `guide.config.json → modules[moduleName].routes` แล้ว capture แต่ละหน้า:

```typescript
// scripts/capture.ts
import { chromium } from 'playwright'
import * as path from 'path'
import * as fs from 'fs'

const AUTH_PATH = path.join(process.env.HOME!, 'docs', PROJECT_NAME, 'auth.json')
const IMG_DIR   = path.join(process.env.HOME!, 'docs', PROJECT_NAME, 'images')

// viewports ที่ใช้ capture — PC (1440×900) และ mobile (390×844 ≈ iPhone 14 Pro)
const VIEWPORTS = {
  pc:     { width: 1440, height: 900 },
  mobile: { width: 390,  height: 844 },
} as const

export async function captureModule(
  baseUrl: string,
  moduleName: string,
  routes: Array<{ slug: string; path: string; extraCaptures?: CaptureStep[] }>,
  options: { mobile?: boolean } = {}         // mobile=true by default (ปิดด้วย --no-mobile)
) {
  const withMobile = options.mobile !== false

  const browser = await chromium.launch({ headless: true })

  // PC context — overview + extra captures ทุกอย่าง
  const pcContext = await browser.newContext({
    storageState: AUTH_PATH,
    viewport: VIEWPORTS.pc,
  })
  const page = await pcContext.newPage()

  // Mobile context — overview อย่างเดียว (ถ้าไม่ได้ใส่ --no-mobile)
  const mobileContext = withMobile
    ? await browser.newContext({
        storageState: AUTH_PATH,
        viewport: VIEWPORTS.mobile,
        isMobile: true,
        hasTouch: true,
        deviceScaleFactor: 2,
      })
    : null
  const mobilePage = mobileContext ? await mobileContext.newPage() : null

  fs.mkdirSync(IMG_DIR, { recursive: true })

  // helper — ซ่อน React Query DevTools (และ dev panel อื่น ๆ) ก่อน screenshot ทุกครั้ง
  // ใช้ JS inject แทนการคลิก เพราะ DevTools panel อาจบัง element ที่ต้องการ
  async function hideDevTools(p = page) {
    await p.evaluate(() => {
      const DEVTOOL_SELECTORS = [
        // TanStack Query v5 (tsqd = TanStack Query Devtools)
        '.tsqd-parent-container',
        '.tsqd-main-panel',
        '.tsqd-open-btn-container',
        '#TanStackQueryDevtools',
        // React Query v4
        '.ReactQueryDevtools',
        '[class*="ReactQueryDevtools"]',
        '[data-testid="ReactQueryDevtoolsPanel"]',
        '[data-testid="ReactQueryDevtoolsToggleButton"]',
        '#react-query-devtools-portal',
        // React Query v5 data-testid
        '[data-testid="devtools-open-btn"]',
        '[data-testid="devtools-panel"]',
      ]
      DEVTOOL_SELECTORS.forEach(sel => {
        document.querySelectorAll<HTMLElement>(sel).forEach(el => {
          el.style.setProperty('display', 'none', 'important')
        })
      })
    })
  }

  for (const route of routes) {
    const pcOverviewPath     = path.join(IMG_DIR, `${route.slug}.png`)
    const mobileOverviewPath = path.join(IMG_DIR, `${route.slug}-mobile.png`)

    const pcSkip     = fs.existsSync(pcOverviewPath)     && !RECAPTURE_MODE
    const mobileSkip = fs.existsSync(mobileOverviewPath) && !RECAPTURE_MODE

    // ข้ามหน้าที่รูปครบทั้ง PC และ mobile แล้ว
    if (pcSkip && (!withMobile || mobileSkip) && !(route.extraCaptures?.length)) {
      console.log(`  ⏭️  [skip] ${route.slug} — รูปมีอยู่แล้ว (PC${withMobile ? '+mobile' : ''})`)
      continue
    }

    console.log(`  📸 Capturing ${route.slug}  (${route.path})`)

    // ─── PC overview ───────────────────────────────────────────────
    if (!pcSkip) {
      await page.goto(`${baseUrl}${route.path}`, { waitUntil: 'networkidle' })
      await page.waitForTimeout(800)           // รอ animation เสร็จ
      await hideDevTools()
      await page.screenshot({ path: pcOverviewPath, fullPage: false })
      console.log(`    ✅ overview (PC 1440×900) → ${route.slug}.png`)
    } else {
      console.log(`    ⏭️  skip PC overview — มีอยู่แล้ว`)
    }

    // ─── Mobile overview ──────────────────────────────────────────
    if (withMobile && mobilePage && !mobileSkip) {
      await mobilePage.goto(`${baseUrl}${route.path}`, { waitUntil: 'networkidle' })
      await mobilePage.waitForTimeout(800)
      await hideDevTools(mobilePage)
      await mobilePage.screenshot({ path: mobileOverviewPath, fullPage: false })
      console.log(`    ✅ overview (📱 390×844)  → ${route.slug}-mobile.png`)
    } else if (withMobile && mobileSkip) {
      console.log(`    ⏭️  skip mobile overview — มีอยู่แล้ว`)
    }

    // ─── Extra captures (PC เท่านั้น — dialog/zoom/btn/step) ─────
    // ข้ามทั้งหมดถ้า overviewOnly = true (--overview-only)
    if (OVERVIEW_ONLY) {
      if (route.extraCaptures?.length) {
        console.log(`    ⏭️  [--overview-only] ข้าม ${route.extraCaptures.length} extra step(s)`)
      }
    } else {
      // หน้าที่ PC skip แต่ต้องทำ extra → goto PC ก่อน
      if (route.extraCaptures?.length && pcSkip) {
        await page.goto(`${baseUrl}${route.path}`, { waitUntil: 'networkidle' })
        await page.waitForTimeout(800)
        await hideDevTools()
      }
      for (const step of route.extraCaptures ?? []) {
        await runCaptureStep(page, step, route.slug, IMG_DIR)
      }
    }
  }

  await pcContext.close()
  if (mobileContext) await mobileContext.close()
  await browser.close()
  console.log(`\n✅ Capture เสร็จทั้งหมด → ${IMG_DIR}\n`)
}

type CaptureStep =
  | { action: 'screenshot';         label: string }
  | { action: 'click';              selector: string }
  | { action: 'screenshot_element'; selector: string; label: string; padding?: number }
  | { action: 'wait';               ms: number }
  | { action: 'fill';               selector: string; value: string }
  | { action: 'hide_devtools' }
  // --- capture เฉพาะจุด ---
  | { action: 'highlight';   selector: string; label: string; color?: string; caption?: string; padding?: number }
  //    วาด box ล้อม element + label กำกับ แล้วถ่าย — ใช้อธิบายปุ่มสำคัญในคู่มือ
  | { action: 'hover';       selector: string; label: string }
  //    hover เพื่อให้ tooltip/dropdown โผล่ แล้วถ่ายทั้งหน้า — ใช้อธิบาย badge/status ที่มี tooltip
  | { action: 'wait_for';    selector: string; timeout?: number }
  //    รอ element ปรากฏก่อนทำ step ถัดไป — ใช้หลัง click ที่มี loading หรือ animation

async function runCaptureStep(page: any, step: CaptureStep, slug: string, dir: string) {
  switch (step.action) {

    case 'screenshot': {
      await hideDevTools()
      const p = path.join(dir, `${slug}-${step.label}.png`)
      await page.screenshot({ path: p, fullPage: false })
      console.log(`    ✅ ${step.label} → ${slug}-${step.label}.png`)
      break
    }

    case 'click':
      await page.click(step.selector)
      await page.waitForTimeout(400)
      break

    case 'screenshot_element': {
      await hideDevTools()
      const pad = step.padding ?? 0
      const el  = await page.$(step.selector)
      if (!el) { console.log(`    ⚠️  ไม่พบ element: ${step.selector}`); break }
      const box = await el.boundingBox()
      const p   = path.join(dir, `${slug}-${step.label}.png`)
      await page.screenshot({
        path: p,
        clip: { x: box.x - pad, y: box.y - pad, width: box.width + pad*2, height: box.height + pad*2 }
      })
      console.log(`    ✅ ${step.label} → ${slug}-${step.label}.png`)
      break
    }

    case 'wait':
      await page.waitForTimeout(step.ms)
      break

    case 'fill':
      await page.fill(step.selector, step.value)
      break

    case 'hide_devtools':
      await hideDevTools()
      console.log(`    🙈 ซ่อน DevTools แล้ว`)
      break

    // ─────────────────────────────────────────────────────────────
    // highlight — วาด box + label กำกับ element แล้วถ่าย
    //   ใช้: อธิบายปุ่มสำคัญ เช่น "ปุ่มนี้คือ Scan" ในคู่มือ
    // ─────────────────────────────────────────────────────────────
    case 'highlight': {
      await hideDevTools()
      const pad     = step.padding ?? 12
      const color   = step.color   ?? '#ef4444'   // แดง default
      const caption = step.caption ?? step.label

      const el = await page.$(step.selector)
      if (!el) { console.log(`    ⚠️  ไม่พบ element: ${step.selector}`); break }
      const box = await el.boundingBox()

      // inject overlay: box + label badge ด้านบน
      await page.evaluate(({ b, color, caption, pad }: any) => {
        const wrap = document.createElement('div')
        wrap.id    = '__guide_highlight__'
        wrap.style.cssText = `
          position:fixed; pointer-events:none; z-index:2147483647;
          left:${b.x - pad}px; top:${b.y - pad}px;
          width:${b.width + pad*2}px; height:${b.height + pad*2}px;
          outline: 3px solid ${color};
          border-radius: 6px;
          box-shadow: 0 0 0 2px white, 0 0 0 4px ${color};
        `
        const badge = document.createElement('div')
        badge.style.cssText = `
          position:absolute; top:-26px; left:0;
          background:${color}; color:white;
          font:700 12px/1 -apple-system,sans-serif;
          padding:4px 10px; border-radius:4px; white-space:nowrap;
        `
        badge.textContent = caption
        wrap.appendChild(badge)
        document.body.appendChild(wrap)
      }, { b: box, color, caption, pad })

      // ถ่ายแบบ crop รอบ element + พื้นที่ badge ด้านบน
      const p = path.join(dir, `${slug}-${step.label}.png`)
      await page.screenshot({
        path: p,
        clip: {
          x:      Math.max(0, box.x - pad - 20),
          y:      Math.max(0, box.y - pad - 40),  // เผื่อพื้นที่ badge
          width:  box.width  + pad*2 + 40,
          height: box.height + pad*2 + 60,
        }
      })

      // เอา overlay ออกหลังถ่ายเสร็จ
      await page.evaluate(() => {
        document.getElementById('__guide_highlight__')?.remove()
      })
      console.log(`    ✅ highlight → ${slug}-${step.label}.png  ("${caption}")`)
      break
    }

    // ─────────────────────────────────────────────────────────────
    // hover — hover element แล้วถ่ายทั้งหน้า (tooltip/dropdown โผล่)
    //   ใช้: อธิบาย badge status ที่มี tooltip, icon ที่มีคำอธิบาย
    // ─────────────────────────────────────────────────────────────
    case 'hover': {
      await page.hover(step.selector)
      await page.waitForTimeout(500)   // รอ tooltip animate เสร็จ
      await hideDevTools()
      const p = path.join(dir, `${slug}-${step.label}.png`)
      await page.screenshot({ path: p, fullPage: false })
      console.log(`    ✅ hover → ${slug}-${step.label}.png`)
      break
    }

    // ─────────────────────────────────────────────────────────────
    // wait_for — รอ selector ปรากฏใน DOM ก่อนทำ step ถัดไป
    //   ใช้: หลัง click ที่มี loading spinner, lazy render, animation
    // ─────────────────────────────────────────────────────────────
    case 'wait_for': {
      const timeout = step.timeout ?? 8_000
      await page.waitForSelector(step.selector, { state: 'visible', timeout })
      console.log(`    ⏳ wait_for พบ "${step.selector}"`)
      break
    }

  }
}
```

### กำหนด extraCaptures ใน `guide.config.json`

```json
{
  "baseUrl": "http://localhost:3000",
  "framework": "nextjs",
  "modules": {
    "basket-circulation": {
      "routes": [
        {
          "slug": "bc-domains",
          "path": "/basket-circulation/domains",
          "extraCaptures": [
            { "action": "screenshot_element",
              "selector": ".data-table-toolbar",
              "label": "zoom-toolbar",
              "padding": 8 },

            { "action": "highlight",
              "selector": "button:has-text('Add Domain')",
              "label": "btn-add-domain",
              "caption": "คลิกเพื่อเพิ่ม Domain ใหม่",
              "color": "#ef4444",
              "padding": 10 },

            { "action": "click",
              "selector": "button:has-text('Add Domain')" },
            { "action": "hide_devtools" },
            { "action": "screenshot", "label": "dialog-create" }
          ]
        },
        {
          "slug": "bc-trade",
          "path": "/basket-circulation/trade",
          "extraCaptures": [
            { "action": "highlight",
              "selector": "button:has-text('Scan')",
              "label": "btn-scan",
              "caption": "Scan QR เพื่อเริ่ม Trade",
              "color": "#2563eb",
              "padding": 8 },

            { "action": "hover",
              "selector": "[data-status='pending'] .status-badge",
              "label": "tooltip-status-pending" },

            { "action": "click",
              "selector": "button:has-text('Scan')" },
            { "action": "wait_for",
              "selector": ".scan-input",
              "timeout": 5000 },
            { "action": "hide_devtools" },
            { "action": "screenshot", "label": "scan-ready" }
          ]
        }
      ]
    }
  }
}
```

**naming convention ของรูปที่ได้:**

| action / รูปแบบ | ชื่อไฟล์ที่ได้ | ใช้ใน guide อย่างไร |
|---|---|---|
| overview PC | `bc-domains.png` | รูปหลัก PC (1440×900) ใน screenshot block |
| overview mobile | `bc-domains-mobile.png` | แท็บ 📱 mobile ใน screenshot block |
| `highlight` | `bc-trade-btn-scan.png` | `type:"btn"` → `<img class="img-inline">` ข้างคำอธิบายใน step |
| `hover` | `bc-trade-tooltip-status-pending.png` | `type:"zoom"` → `.img-zoom` อธิบาย tooltip ใน step |
| `wait_for` | *(ไม่สร้างรูป — แค่รอ)* | ใช้คู่กับ `screenshot` ถัดไป |

### แสดง progress ระหว่าง capture

```
🎬 เริ่ม capture module: basket-circulation
   URL: http://localhost:3000
   Session: ~/docs/wms/auth.json (อายุ 0.2 ชม.)
   Viewports: 🖥️ PC (1440×900) + 📱 mobile (390×844)

  ⏭️  [skip] bc-domains — รูปมีอยู่แล้ว (PC+mobile, 4 ไฟล์)
  ⏭️  [skip] bc-basket  — รูปมีอยู่แล้ว (PC+mobile, 2 ไฟล์)

  📸 [3/4] bc-trade     /basket-circulation/trade
    ✅ overview (PC 1440×900) → bc-trade.png
    ✅ overview (📱 390×844)  → bc-trade-mobile.png
    ✅ highlight              → bc-trade-btn-scan.png  ("Scan QR เพื่อเริ่ม Trade")
    ✅ hover                  → bc-trade-tooltip-status-pending.png
    ⏳ wait_for พบ ".scan-input"
    🙈 ซ่อน DevTools แล้ว
    ✅ scan-ready             → bc-trade-scan-ready.png

  📸 [4/4] bc-void      /basket-circulation/void
    ✅ overview (PC 1440×900) → bc-void.png
    ✅ overview (📱 390×844)  → bc-void-mobile.png

✅ Capture เสร็จ — ถ่ายใหม่ 2 หน้า (PC+mobile) / ข้าม 2 หน้า (มีอยู่แล้ว)
```
