---
name: ding
description: Use when the user wants to send a notification or message to DingTalk — "/ding", "แจ้งเตือน DingTalk", "ส่งเข้ากลุ่ม DingTalk", "notify the DingTalk group", "ping the team on DingTalk". Sends markdown, with optional image/file attachments, into a TYCTH dingtalk-notify channel.
metadata:
  author: ken1lnw
  created: 2026-09-03
  updated: 2026-10-12
  tags: [notification, automation]
  status: stable
---

# ding — ส่งแจ้งเตือนเข้ากลุ่ม DingTalk

ส่งข้อความ markdown เข้ากลุ่ม DingTalk ผ่าน API ภายในของ TYCTH
(`https://dingtalk.tycthailand.com` → `POST /api/notify/`)

Token อ่านจาก `SECRET_AUTH` ใน `~/.config/pi-claude-md/ding.env`
(Windows: `%USERPROFILE%\.config\pi-claude-md\ding.env`)
`send.py` อ่านเอง — **ห้าม cat, echo หรือแสดงค่า token ในบทสนทนา**

Script: `${CLAUDE_PLUGIN_ROOT}/skills/ding/send.py` (Windows ใช้ `python` แทน `python3` ถ้าไม่มี `python3`)

## 0. ตรวจ token ก่อนทุกครั้ง

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/ding/send.py" --check-env
```

- `OK: ...` → ไปขั้นตอนที่ 1
- ไม่ผ่าน → รัน `--init-env` (สร้างไฟล์ให้ ถ้ายังไม่มี และไม่ทับไฟล์เดิม) แล้วบอกผู้ใช้ path ที่ได้
  ให้ผู้ใช้เปิดไฟล์ด้วย editor ใส่ token เอง แล้วตอบกลับมา จากนั้นรัน `--check-env` ซ้ำ
  **ห้ามขอให้ผู้ใช้วาง token ในแชท และห้ามเขียน token ลงไฟล์ให้เอง**

## ขั้นตอน (ทำตามลำดับทุกครั้ง)

### 1. ถามว่าจะส่งไปห้องไหน

อ่าน `~/.config/pi-claude-md/ding-channels.json` ก่อน แล้วใช้ AskUserQuestion
ตั้งตัวเลือกเป็นห้องที่เคยใช้ + ตัวเลือก "ห้องใหม่ (ใส่ UUID เอง)"

- ถ้าไฟล์ยังไม่มี หรือว่างเปล่า → ถามตรง ๆ ว่าขอ **channel UUID** ของห้องปลายทาง
- ถ้าผู้ใช้เลือก "ห้องใหม่" → ขอ UUID แล้วเก็บ

**ต้องถามเสมอ** ต่อให้ข้อความของผู้ใช้ดูเหมือนบอกห้องมาแล้ว หรือเพิ่งส่งห้องนั้นไปเมื่อกี้
การส่งผิดห้อง = แจ้งเตือนคนผิดทั้งกลุ่ม และเรียกคืนไม่ได้

### 2. ถามว่าจะส่งอะไร

ต้องได้ 2 อย่าง:

| ค่า | ใช้ทำอะไร |
|---|---|
| `hashtag` | หัวข้อสั้น ๆ ที่โผล่บน lock screen มือถือ (**ไม่แสดงในตัวข้อความ**) |
| `markdown_msg` | เนื้อความ markdown ที่จะเห็นในกลุ่ม |

- ถ้าผู้ใช้บอกเนื้อความมาแล้วในคำสั่ง → ยังต้องถาม/ยืนยัน `hashtag` และให้ผู้ใช้เห็นข้อความสุดท้ายก่อนส่ง
- ถ้าผู้ใช้บอกแค่หัวข้อกว้าง ๆ → ร่างข้อความให้ แล้วให้ยืนยันก่อน
- ถ้าผู้ใช้วาง log ของ `deploy.sh` มา → ใช้เทมเพลตด้านล่าง

### 2.1 เทมเพลตแจ้ง deploy

ใช้เมื่อผู้ใช้วาง output ของ `./deploy.sh` มา — ดึงค่าจาก log ทุกช่อง **ยกเว้น `โดย`**

```markdown
## ✅ Deploy สำเร็จ — <service>

- **เวลา:** <YYYY-MM-DD HH:MM:SS> (+07)
- **Host:** <host> · **โดย:** <ชื่อคนที่ผู้ใช้กรอก>
- **URL:** <url>                        ← ใส่เมื่อ log มี url ที่ไม่ใช่ n/a
- **Commit:** `<commit 7 ตัวแรก>`        ← หลาย service: `frontend `abc1234` · backend `def5678``
- **Smoke test:** ผ่าน (<host:port/path>) · container Healthy
- ลบ image เก่าที่ถูกแทนที่ <n> รายการ (แอปอื่นไม่กระทบ)

### สิ่งที่ deploy ไป (เทียบกับ release ก่อนหน้า <วันที่>)

**<สรุปหนึ่งบรรทัดว่า release นี้คืออะไร>** — frontend <n> commits / backend <n> commits

| ส่วน | รายละเอียด |
|---|---|
| <หัวข้อ> | <รายละเอียด> |
```

ตัดบรรทัด `Image:` (digest) ออกได้ถ้าใส่ `Commit` แล้ว — คนอ่านใช้ commit มากกว่า digest
ส่วน "สิ่งที่ deploy ไป" ใส่เมื่อผู้ใช้ขอรายละเอียด หรือเมื่อหาข้อมูลได้ตามขั้นตอน 2.1.1

**`โดย` ต้องถามผู้ใช้ทุกครั้ง** ด้วย AskUserQuestion — ห้ามหยิบค่า `by:` จาก log มาใส่เอง
เพราะนั่นคือ user ที่ล็อกอิน SSH (เช่น `piteam`) ซึ่งเป็นบัญชีกลาง ไม่ใช่ชื่อคนที่ deploy จริง
ใส่ค่า `by:` จาก log เป็นตัวเลือกหนึ่งได้ แต่ต้องให้ผู้ใช้เลือก/พิมพ์ชื่อเอง

ที่ดึงจาก log: `service`/`host`/`โดย(by)` จากบรรทัด `deployed OK` · เวลาจาก timestamp บรรทัด
`✅ deploy OK` (เวลาไทย) · commit จากบรรทัด `pinned` · smoke test จากบรรทัด `🟢`
· จำนวน image ที่ลบจากบรรทัด `project-scoped image cleanup`

ถ้า deploy **ไม่สำเร็จ** ให้เปลี่ยนหัวเป็น `## ❌ Deploy ล้มเหลว — <service>` แล้วใส่บรรทัด error
ที่เจอใน log แทนบรรทัด smoke test — อย่าใช้คำว่าสำเร็จกับ log ที่ไม่มี `✅ deploy OK`
และตั้ง `hashtag` เป็น **`ชิบหายแล้วโว๊ยย`** เป็นค่าเริ่มต้น (ผู้ใช้เปลี่ยนได้ตอนยืนยัน)

### 2.1.1 หา "deploy อะไรไป" จาก commit hash

ใช้เมื่อผู้ใช้ขอให้ใส่รายละเอียดว่า release นี้มีอะไร — commit ที่ deploy.sh ใช้มักเป็น
**commit เปล่าชื่อ `deploy!` (0 ไฟล์)** ที่สร้างไว้ trigger CI เท่านั้น เนื้อหาจริงอยู่ใน commit ก่อนหน้า

```bash
# 1) repo ไหน — ชื่อ image ไม่ตรงชื่อ repo เสมอ
#    ghcr.io/tycthailand/rcs-frontend → repo tycthailand/rcs   (ไม่มี repo ชื่อ rcs-frontend)
#    ghcr.io/tycthailand/rcs-backend  → repo tycthailand/rcs-backend
gh api repos/<org>/<repo> --jq .full_name

# 2) หา deploy commit ก่อนหน้า = ขอบล่างของ release นี้
gh api "repos/<org>/<repo>/commits?sha=<commit>&per_page=100" \
  --jq '.[]|select(.commit.message|startswith("deploy"))|"\(.sha[0:7]) \(.commit.author.date)"' | head -5

# 3) diff ระหว่าง 2 deploy — ได้จำนวน commit/ไฟล์ และไฟล์ที่แตะ
gh api repos/<org>/<repo>/compare/<prev>...<commit> \
  --jq '{commits:(.commits|length), files:(.files|length), add:(.files|map(.additions)|add)}'
gh api "repos/<org>/<repo>/commits?sha=<commit>&per_page=30" \
  --jq '.[]|"\(.sha[0:7]) \(.commit.message|split("\n")[0])"'
```

สรุปเป็น "ผู้ใช้ได้อะไรเพิ่ม" (เมนู/หน้าจอ/ความสามารถ) ไม่ใช่รายชื่อไฟล์
route ที่ `added` ใน `src/app/` และโมดูลใหม่ใน `src/modules/` คือของใหม่ที่คนในกลุ่มจะเห็น

**อย่าเดา** ถ้าหา repo ไม่เจอหรือ `gh` ใช้ไม่ได้ — บอกผู้ใช้ตรง ๆ แล้วส่งแบบไม่มีหัวข้อนี้

### 2.2 markdown ที่ยืนยันแล้วว่าใช้ได้

ทดสอบยิงจริงเข้ากลุ่มเมื่อ 2026-09-03:

- **ตาราง markdown render เป็นตารางจริง** ใช้ได้ ไม่มีปัญหา — ใช้กับข้อมูลหลายคอลัมน์ได้เลย
- heading `##`, bullet, **bold**, `inline code`, blockquote `>`, emoji ใช้ได้ปกติ

### 3. ส่ง

เขียนข้อความลงไฟล์ชั่วคราวก่อน (เลี่ยงปัญหา quote/ขึ้นบรรทัดใหม่ในภาษาไทย) แล้ว:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/ding/send.py" \
  --channel "<uuid>" \
  --hashtag "รายงานประจำวัน" \
  --message-file /tmp/.../msg.md
```

ได้ `OK: ส่งเข้ากลุ่มแล้ว` = สำเร็จ · ได้ `FAILED <code>: ...` = ดูตารางด้านล่าง

**ก่อนส่งจริง ให้รันคำสั่งเดียวกันพร้อม `--dry-run` ก่อนเสมอ** แล้วเอา markdown ที่พิมพ์ออกมาให้ผู้ใช้ยืนยัน
— นั่นคือข้อความฉบับที่จะเข้ากลุ่มจริง รวมลิงก์ไฟล์แนบ (เป็น placeholder) และบรรทัดวันหมดอายุ
dry-run ไม่อ่าน token ไม่อัปโหลด ไม่ส่ง แต่ตรวจไฟล์และ tags แบบเดียวกับตอนส่งจริง

ถ้าได้ `ยังไม่ได้อัปโหลด/ส่งอะไร:` = ไฟล์หรือ tags ไม่ผ่านการตรวจ — แก้ตามรายการแล้วรันใหม่ (ยังไม่มีอะไรหลุดออกไป)

### 3.1 แนบรูป / ไฟล์ (`--file`)

ใส่ `--file <path>` ซ้ำได้หลายไฟล์ — `send.py` ตรวจ**ทุกไฟล์**ก่อน (มีอยู่จริง / นามสกุล / ชื่อไฟล์ / ขนาด)
ถ้าไม่ผ่านแม้ไฟล์เดียวจะไม่อัปโหลดอะไรเลย จากนั้นอัปโหลดทีละไฟล์แล้วต่อท้ายข้อความ:

| ชนิด | นามสกุล | ขนาดสูงสุด | ต่อท้ายเป็น |
|---|---|---|---|
| `images` | jpg jpeg png gif bmp svg webp tiff ico | 10 MB | `![ชื่อไฟล์](url)` — รูปขึ้นในกลุ่มเลย (ยืนยันแล้วกับ PNG; svg/tiff/ico ยังไม่ได้ลองว่า DingTalk แสดงไหม) |
| `docs` | xlsx xls doc docx pdf ppt pptx txt csv md html | 50 MB (ใช้จริง ≤ ~49 MB) | `- [ชื่อไฟล์](url)` — ลิงก์ดาวน์โหลด · .html/.md/.txt ≤2 MB ใช้ `view_url` แทน |

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/ding/send.py" \
  --channel "<uuid>" --hashtag "<hashtag>" --message-file /tmp/.../msg.md \
  --file shots/01-before.png --file shots/02-after.png
```

- API: `POST /api/upload/` (header `X-Authentication`) multipart = `kind` (`images`|`docs`) + `file`
  → `{file_id, filename, url, view_url}` · อ้างอิง: `~/Documents/API-DOC (1).html` (อัปเดต 2026-10-05)
- `url` เป็น **public** (Supabase storage `dingtalk-notify-image`) — ใครมีลิงก์ก็เปิดได้ ห้ามแนบ
  ไฟล์ที่มี token, รหัสผ่าน หรือข้อมูลที่ไม่ควรหลุดนอกกลุ่ม · เอกสาร API ไม่มี endpoint ลบไฟล์
- **ลิงก์หมดอายุใน 7 วัน** (ลบอัตโนมัติ 03:00 น. ทุกวัน) — ข้อความในกลุ่มยังอยู่แต่กดแล้วเจอ 404
  `send.py` ต่อท้าย `> ไฟล์แนบเปิดได้ถึง <YYYY-MM-DD>` ให้เองเมื่อมีไฟล์แนบ ไม่ต้องเขียนเองใน `msg.md`
  ถ้าเนื้อหาต้องเปิดย้อนหลังนานกว่านั้น บอกผู้ใช้ก่อนส่ง
- **ชื่อไฟล์** ต้องมีนามสกุล และห้ามมี `/ \ # ? % "` หรือขึ้นบรรทัดใหม่ — ไม่งั้นได้ 400 (เปลี่ยนชื่อไฟล์ก่อนแนบ)
- ไฟล์ถูกต่อท้ายข้อความเสมอ — ถ้าจะอธิบายรูป ให้เขียนหัวข้อ/คำบรรยายไว้ท้าย `msg.md`
- บรรทัด `uploaded <file> -> <url>` ที่พิมพ์ออกมาคือ upload ผ่านแล้ว แม้ notify จะ fail ทีหลัง —
  ถ้าต้องส่งใหม่ จะได้ไฟล์ซ้ำใน storage (ไม่มีผลกับกลุ่ม)
- ยิงจริงเข้า PI Team เมื่อ 2026-10-06: อัปโหลด PNG 2 รูปผ่าน, URL เปิดได้แบบไม่ต้อง auth, notify ตอบ 200
- ยิงจริงเข้า Test Room เมื่อ 2026-10-06: PNG + `.html` → ได้ `view_url` (`/v/<token>`) ตอบ `text/html`
  ผู้ใช้ยืนยันใน DingTalk แล้ว: รูปขึ้นในข้อความ, รายงาน HTML เปิดเป็นหน้าเว็บ, บรรทัดวันหมดอายุแสดงถูก

#### แนบรายงาน HTML ให้เปิดแล้วเห็นเป็นหน้าเว็บ (`view_url`)

`.html` ที่เปิดผ่าน `url` ตรง ๆ จะเห็นเป็นซอร์สโค้ด (Supabase ส่งเป็น `text/plain`)
API จึงคืน `view_url` (`https://dingtalk.tycthailand.com/v/<token>`) สำหรับ docs `.html/.md/.txt` ≤2 MB
— `send.py` ใช้ `view_url` ให้อัตโนมัติเมื่อมีค่า (ไฟล์อื่นได้ `null` → ใช้ `url`)

ไฟล์ HTML ต้อง **เป็นไฟล์เดียวจบ ไม่มี JavaScript**: ใช้ได้แค่ HTML + CSS inline (`<style>`/`style=""`)
+ รูปแบบ `data:` URI · ถูกบล็อก: JS ทุกชนิด (กราฟ Chart.js ไม่ขึ้น → export เป็น SVG inline หรือ PNG `data:`),
รูป/ฟอนต์/CSS จากเว็บอื่น, iframe, form · ต้องเป็น UTF-8 · `.md`/`.txt` แสดงเป็นข้อความธรรมดา (ไม่ render markdown)
เกิน 2 MB → ไม่มี `view_url` คนเปิดจะเห็นซอร์ส ให้ย่อไฟล์ (มักเป็นรูป base64) หรือแนบเป็น PDF แทน

### 4. ถ้าเป็นห้องใหม่ ให้ถามชื่อเล่นแล้วบันทึก

หลังส่งสำเร็จเท่านั้น ถามชื่อเล่นของห้อง แล้ว append เข้า `~/.config/pi-claude-md/ding-channels.json` (สร้างไฟล์ถ้ายังไม่มี):

```json
[{"name": "ทีม PI", "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}]
```

ห้องที่เคยบันทึกแล้วไม่ต้องถามชื่อซ้ำ

## การ mention (`--tags`)

| ค่า | ผล |
|---|---|
| `all` (ค่าเริ่มต้น) | @ทุกคนในกลุ่ม |
| `1007,1029` | แทนรหัสพนักงานในข้อความให้เป็น @mention จริง |

ใช้รายชื่อรหัสเมื่อผู้ใช้ระบุมาเท่านั้น และต้องระวัง 2 ข้อ:

1. **แทนที่แบบค้นข้อความตรง ๆ** — รหัส `1007` จะไปโดนเลขอื่นด้วย เช่น ออเดอร์ `21007`
   `send.py` ปฏิเสธให้เองถ้ารหัสโผล่ในรูปอื่นที่ไม่ใช่ `@1007` (เช็คซ้ำหลังอัปโหลด เพราะ URL ไฟล์อาจมีเลขตรงกัน)
   ถ้าเลี่ยงตัวเลขนั้นไม่ได้ ให้ใช้ `all` แทน · `--tags ""` ถูกปฏิเสธ เพราะ `[]` = ไม่ mention ใครเลย
2. **รหัสที่หาไม่เจอถูกข้ามเงียบ ๆ แต่ยังตอบ 200** — อย่าบอกผู้ใช้ว่า "ทุกคนได้รับแล้ว"
   ให้บอกแค่ว่า "ส่งเข้ากลุ่มแล้ว"

## อ่าน error

| Code | แปลว่า | ทำยังไง |
|---|---|---|
| 401 | token ผิด หรือไม่ได้ส่ง header | เช็ค `SECRET_AUTH` ใน `ding.env` ว่ามีช่องว่าง/newline ติดมาไหม — **ไม่ retry** |
| 404 `Channel ID ... does not exist` | ไม่มีห้องนี้ หรือถูกปิดใช้งาน | ขอ UUID ใหม่จากผู้ใช้ |
| 404 `Webhook URL or secret keys not found` | มีห้องอยู่ แต่ข้อมูลในฐานข้อมูลไม่ครบ | ปัญหาฝั่งผู้ดูแลระบบ ไม่ใช่ที่ request |
| 413 | ข้อความเกิน 1 MB | ย่อข้อความ |
| 422 | body ผิดรูปแบบ / UUID ไม่ถูกต้อง | อ่านข้อความที่ตามมา แล้วแก้ |
| 502 | DingTalk ปฏิเสธ — มักเพราะส่งเกิน ~20 ข้อความ/นาที | `send.py` ลองส่งให้แล้วสูงสุด 4 ครั้ง ถ้ายังไม่ผ่านให้รอสักพักค่อยลองใหม่ |
| 500 | ฐานข้อมูล/DingTalk มีปัญหา | ลองใหม่ได้ครั้งเดียว |

## Red flags — หยุดแล้วกลับไปทำตามขั้นตอน

- กำลังจะ `--file` ภาพหน้าจอที่ติด token / password / ข้อมูลลับ — URL ที่ได้เป็น public
- กำลังจะแนบรายงาน `.html` ที่มี JS / โหลด CDN / ใหญ่เกิน 2 MB — เปิดใน DingTalk แล้วจะพังหรือเห็นซอร์ส

- กำลังจะส่งโดยไม่ได้ถามห้อง เพราะ "ห้องเดิมกับเมื่อกี้"
- กำลังจะเดา `hashtag` ให้เอง โดยไม่ให้ผู้ใช้ยืนยัน
- กำลังจะใส่ `โดย:` จากค่า `by:` ใน log เพราะ "ก็เขียนไว้ใน log แล้วนี่" — ต้องถามคนกรอกเสมอ
- กำลังจะ `cat ding.env` หรือ echo ค่า token ออกมาดู หรือขอให้ผู้ใช้วาง token ในแชท
- กำลังจะรายงานว่า "แจ้งเตือนถึงทุกคนแล้ว" ทั้งที่ 200 แปลว่า "ส่งเข้ากลุ่มแล้ว" เท่านั้น
- กำลังจะ parse ข้อความใน response 200 (ถูกตัดเหลือ 15 ตัวอักษร โดยตั้งใจ)
