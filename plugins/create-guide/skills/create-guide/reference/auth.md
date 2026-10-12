## ขั้นตอนที่ 0-D — Auth Setup  *(รันเฉพาะเมื่อ captureMode = true)*

> ถ้า `captureMode = false` → ข้ามขั้นตอนนี้ทั้งหมด ไปที่ขั้นตอนที่ 1 เลย
>
> ถ้า `htmlOnlyMode = true` → ข้าม Step 0-D, 0-E, 0-F ทั้งหมด ข้ามไป **Step 1** ทันที
> (source 1-4 จะอ่านจาก cache เท่านั้น ถ้า cache ขาด → แจ้ง user แต่ดำเนินการต่อด้วยข้อมูลที่มี)
>
> ```
> ⚡ [--html-only] ข้ามทุก capture/source step → ใช้ cache ที่มีอยู่สร้าง HTML
>    guide.config.json พบ: meta✅  routes✅  pages(3/4)✅  images(8 ไฟล์)✅
> ```

ตรวจสอบตามลำดับ **waterfall** นี้:

```
1. auth.json มีอยู่ + อายุ < 8 ชั่วโมง
       → ✅ ใช้ session เดิม ข้ามไป Step 0-E

2. ~/docs/<projectName>/capture.env มี CAPTURE_USER + CAPTURE_PASS
       → ✅ อ่าน credential จาก capture.env ไป login
          (ไฟล์นี้อยู่นอก project dir — ไม่เสี่ยง commit ขึ้น Git)

3. ไม่มีทั้งคู่
       → 🔐 ถามผู้ใช้ใน terminal (ดูด้านล่าง)
```

### กรณีที่ 3 — Prompt ใน terminal

แสดงข้อความนี้แล้วรอ input:

```
╔══════════════════════════════════════════════════════╗
║  🔐  Login เพื่อ capture หน้าจอ                      ║
║      URL: <baseUrl จาก guide.config.json>            ║
╚══════════════════════════════════════════════════════╝

  Username / Email : 
  Password         : (ตัวอักษรจะถูกซ่อน)

  [Enter] ดำเนินการต่อ   [S + Enter] บันทึกลง ~/docs/<projectName>/capture.env ด้วย
```

- password ต้องใช้ raw mode ซ่อนตัวอักษรขณะพิมพ์ (แสดงแค่ `*` หรือว่างเปล่า)
- ถ้าผู้ใช้กด `S` → บันทึก `CAPTURE_USER` / `CAPTURE_PASS` ลง `~/docs/<projectName>/capture.env`
  แล้วแจ้งว่า **"บันทึก capture.env ไว้ที่ ~/docs/<projectName>/ แล้ว (นอก project — ปลอดภัย)"**
- ไม่ต้องแก้ `.gitignore` เพราะไฟล์อยู่นอก project directory

### 0-D.1  Login ด้วย Playwright

```typescript
// scripts/capture-setup.ts
import { chromium } from 'playwright'
import * as fs from 'fs'
import * as path from 'path'
import * as readline from 'readline'

const AUTH_PATH        = path.join(process.env.HOME!, 'docs', PROJECT_NAME, 'auth.json')
const CAPTURE_ENV_PATH = path.join(process.env.HOME!, 'docs', PROJECT_NAME, 'capture.env')

async function getCredentials(): Promise<{ user: string; pass: string } | null> {
  // กรณี 1 — session ยังใช้ได้
  if (fs.existsSync(AUTH_PATH)) {
    const ageHours = (Date.now() - fs.statSync(AUTH_PATH).mtimeMs) / 3_600_000
    if (ageHours < 8) {
      console.log(`✅ ใช้ session เดิม (อายุ ${ageHours.toFixed(1)} ชม.)`)
      return null  // ไม่ต้อง login
    }
  }

  // กรณี 2 — ~/docs/<project>/capture.env (นอก project dir — ปลอดภัย)
  if (fs.existsSync(CAPTURE_ENV_PATH)) {
    const env = parseEnv(fs.readFileSync(CAPTURE_ENV_PATH, 'utf8'))
    if (env.CAPTURE_USER && env.CAPTURE_PASS) {
      console.log(`✅ อ่าน credential จาก ${CAPTURE_ENV_PATH}`)
      return { user: env.CAPTURE_USER, pass: env.CAPTURE_PASS }
    }
  }

  // กรณี 3 — ถามใน terminal
  return promptCredentials()
}

async function promptCredentials(): Promise<{ user: string; pass: string }> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout })
  const ask = (q: string) => new Promise<string>(res => rl.question(q, res))

  console.log('\n╔══════════════════════════════════════════════════════╗')
  console.log('║  🔐  Login เพื่อ capture หน้าจอ                      ║')
  console.log(`║      URL: ${BASE_URL.padEnd(42)}║`)
  console.log('╚══════════════════════════════════════════════════════╝\n')

  const user = await ask('  Username / Email : ')
  process.stdout.write('  Password         : ')
  const pass = await hiddenInput()
  const save = await ask(`\n  บันทึกลง ${CAPTURE_ENV_PATH} ด้วยไหม? (y/N) : `)

  rl.close()

  if (save.toLowerCase() === 'y') {
    fs.mkdirSync(path.dirname(CAPTURE_ENV_PATH), { recursive: true })
    fs.writeFileSync(CAPTURE_ENV_PATH, `CAPTURE_USER=${user}\nCAPTURE_PASS=${pass}\n`)
    console.log(`  💾 บันทึกลง ${CAPTURE_ENV_PATH} แล้ว (นอก project — ปลอดภัย)\n`)
  }

  return { user, pass }
}

function hiddenInput(): Promise<string> {
  return new Promise(resolve => {
    const chars: string[] = []
    process.stdin.setRawMode(true)
    process.stdin.resume()
    const handler = (buf: Buffer) => {
      const c = buf.toString()
      if (c === '\r' || c === '\n') {
        process.stdin.setRawMode(false)
        process.stdin.pause()
        process.stdin.removeListener('data', handler)
        resolve(chars.join(''))
      } else if (c === '\x7f') {
        chars.pop()
      } else if (c !== '\x03') {
        chars.push(c)
      }
    }
    process.stdin.on('data', handler)
  })
}

export async function setupAuth(baseUrl: string) {
  const creds = await getCredentials()
  if (!creds) return  // session ยังดีอยู่

  const browser = await chromium.launch({ headless: true })
  const context = await browser.newContext()
  const page    = await context.newPage()

  console.log('  🌐 กำลัง login...')
  await page.goto(`${baseUrl}/login`)

  // ปรับ selector ให้ตรงกับระบบ
  await page.fill('input[type="email"], input[name="username"], input[name="email"]', creds.user)
  await page.fill('input[type="password"]', creds.pass)
  await page.click('button[type="submit"], button:has-text("Login"), button:has-text("Sign in")')

  try {
    await page.waitForURL(url => !url.toString().includes('/login'), { timeout: 15_000 })
    console.log('  ✅ Login สำเร็จ\n')
  } catch {
    await browser.close()
    throw new Error('❌ Login ไม่สำเร็จ — ตรวจสอบ username/password แล้วลองใหม่')
  }

  // บันทึก session (cookie เท่านั้น — ไม่มี password)
  fs.mkdirSync(path.dirname(AUTH_PATH), { recursive: true })
  await context.storageState({ path: AUTH_PATH })
  console.log(`  💾 บันทึก session → ${AUTH_PATH}\n`)

  await browser.close()
}
```

### 0-D.2  ไฟล์ที่ไม่ควร Commit (ตรวจสอบและเพิ่มใน .gitignore อัตโนมัติ)

| ไฟล์ | เหตุผล |
|---|---|
| `~/docs/*/capture.env` | มี CAPTURE_USER/CAPTURE_PASS — อยู่นอก project dir อยู่แล้ว ไม่เสี่ยง commit |
| `~/docs/*/auth.json` | มี session token — อยู่นอก project dir อยู่แล้ว ไม่เสี่ยง commit |
| `~/docs/*/images/` | รูป screenshot (optional) |
