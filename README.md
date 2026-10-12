**ภาษาไทย** · [English](./README.en.md)

# PI Claude Md

Skills กลางของทีม PI สำหรับ [Claude Code](https://code.claude.com) — เลือกติดตั้งเฉพาะตัวที่ต้องการ ได้ทุกเครื่องเหมือนกัน และอัปเดตได้จากที่เดียว

## เริ่มต้นเร็ว

**ทาง A — เลือกหลายตัวพร้อมกัน (แนะนำ)**

```bash
git clone https://github.com/ken1lnw/pi-claude-md.git
cd pi-claude-md
claude
```

แล้วพิมพ์ใน Claude Code:

```
/install-skills
```

**ทาง B — ติดตั้งทีละตัว ไม่ต้อง clone**

```
/plugin marketplace add ken1lnw/pi-claude-md
/plugin install tyc-design-system@pi-claude-md
```

## Skills ที่มี

| Plugin | ทำอะไร | ต้องตั้งค่าก่อน |
|---|---|---|
| [tyc-design-system](./plugins/tyc-design-system/skills/tyc-design-system/SKILL.md) | ใช้ design system กลางของ TYC กับงาน UI | ไม่ต้อง |
| [create-guide](./plugins/create-guide/skills/create-guide/SKILL.md) | สร้างคู่มือการใช้งานเป็น HTML ไฟล์เดียว | ไม่ต้อง |
| [ding](./plugins/ding/skills/ding/SKILL.md) | ส่งแจ้งเตือนเข้ากลุ่ม DingTalk | ต้องกรอก `ding.env` |

### tyc-design-system

- **ทำอะไร:** บังคับให้ UI ทุกระบบภายในใช้สี ปุ่ม ตาราง การ์ด radius/spacing และ dark/light mode ชุดเดียวกัน โดยอ่านจาก design token จริง ไม่เดาค่าเอง
- **ใช้เมื่อ:** สร้างหน้าใหม่ restyle ระบบเดิม review UI หรือถามเรื่อง TYC theme / brand guideline
- **ตัวอย่าง:** `ทำหน้า login ของ wms ให้ตรง TYC theme` · `reskin โมดูล receiving ให้ match design system`
- **มี 3 โหมด:** `full` (ทั้งระบบ) · `partial` (เฉพาะโมดูลที่ระบุ) · `extend` (เพิ่ม pattern ใหม่เข้า design system)

### create-guide

- **ทำอะไร:** สร้างคู่มือการใช้งาน module เป็น HTML ไฟล์เดียว (รูป embed เป็น base64 แชร์ได้ทันที) จาก CLAUDE.md, source code, routes และ screenshot
- **ใช้เมื่อ:** ต้องการคู่มือให้ผู้ใช้ระบบ หรืออัปเดตคู่มือหลังแก้หน้าจอ
- **ตัวอย่าง:** `/create-guide:create-guide basket-circulation` · `/create-guide:create-guide receiving th+en --capture`
- **ภาษา:** `th` (ค่าเริ่มต้น) · `en` · `th+en` (มีปุ่มสลับภาษา)
- **ต้องมีเพิ่ม (เฉพาะ `--capture`):** Node.js + Playwright · บัญชีทดสอบของระบบนั้น

### ding

- **ทำอะไร:** ส่งข้อความ markdown พร้อมรูปหรือไฟล์แนบเข้ากลุ่ม DingTalk ผ่าน dingtalk-notify ของ TYCTH
- **ใช้เมื่อ:** แจ้ง deploy แจ้งรายงาน หรือแจ้งทีม
- **ตัวอย่าง:** `/ding:ding แจ้งทีมว่า deploy wms เสร็จแล้ว` · `ส่งรูปนี้เข้ากลุ่ม DingTalk`
- **ความปลอดภัย:** ถามห้องปลายทางทุกครั้ง และให้ยืนยันข้อความก่อนส่งเสมอ
- **ต้องมีเพิ่ม:** Python 3.9+ · token ของ dingtalk-notify · เครื่องต้องเข้า `dingtalk.tycthailand.com` ได้

## สิ่งที่ต้องมี

| อะไร | ใช้กับ | ตรวจด้วย |
|---|---|---|
| Claude Code (ทดสอบกับ 2.1.296) | ทุก skill | `claude --version` |
| git | ทาง A | `git --version` |
| Python 3.9+ | `/install-skills` และ ding | `python3 --version` (Windows: `python --version`) |

ใช้ได้บน Linux, macOS และ Windows

## วิธีติดตั้งแบบละเอียด

### ทาง A — `/install-skills` (เลือกได้หลายตัว)

1. Clone repo แล้วเปิด Claude Code **ที่ root ของ repo**

   ```bash
   git clone https://github.com/ken1lnw/pi-claude-md.git
   cd pi-claude-md
   claude
   ```

2. พิมพ์ `/install-skills` → จะเห็นรายการ plugin ที่ยังไม่ได้ติดตั้ง พร้อมคำอธิบาย
3. ติ๊กเลือกตัวที่ต้องการ (เลือกได้หลายตัว)
4. ถ้าเลือก **ding** → Claude จะสร้างไฟล์ `ding.env` ให้แล้วบอก path ให้เปิดไฟล์ด้วย editor ใส่ token (ดู [ตั้งค่า ding](#ตั้งค่า-ding)) แล้วตอบ Claude ว่าเสร็จ
5. Claude ติดตั้งให้ แล้วแสดงตาราง `ติดตั้งแล้ว` / `ข้าม` / `ล้มเหลว` พร้อมเหตุผล
6. รัน `/reload-plugins` หรือเปิด session ใหม่

รัน `/install-skills` ซ้ำได้ตลอด ตัวที่ติดตั้งแล้วจะถูกข้าม

### ทาง B — `/plugin` (ทีละตัว)

1. เพิ่ม marketplace (ครั้งเดียวต่อเครื่อง)

   ```
   /plugin marketplace add ken1lnw/pi-claude-md
   ```

2. พิมพ์ `/plugin` → แท็บ **Discover** → เลือก plugin → **Install** → เลือก scope **user** (ใช้ได้ทุกโปรเจค)
3. ถ้าเป็น **ding** → ทำ [ตั้งค่า ding](#ตั้งค่า-ding) ให้เสร็จก่อนใช้งาน

แบบใช้คำสั่งใน terminal (ไม่ต้องตอบคำถาม):

```bash
claude plugin marketplace add ken1lnw/pi-claude-md
claude plugin install tyc-design-system@pi-claude-md --scope user
claude plugin install create-guide@pi-claude-md --scope user
claude plugin install ding@pi-claude-md --scope user
```

## ตั้งค่า ding

ding อ่าน token จากไฟล์ในเครื่องคุณเท่านั้น ไฟล์นี้ไม่ได้อยู่ใน repo

| OS | ไฟล์ |
|---|---|
| Linux / macOS | `~/.config/pi-claude-md/ding.env` |
| Windows | `%USERPROFILE%\.config\pi-claude-md\ding.env` |

1. `/install-skills` สร้างไฟล์ให้อัตโนมัติ หรือสร้างเองด้วย (Windows ใช้ `python` แทน `python3`):

   ```bash
   python3 plugins/ding/skills/ding/send.py --init-env
   ```

2. เปิดไฟล์ด้วย editor แล้วแทน `paste-token-here` ด้วย token จริง:

   ```
   SECRET_AUTH=paste-token-here
   ```

3. ตรวจว่าไฟล์ถูกต้อง (ไม่แสดงค่า token):

   ```bash
   python3 plugins/ding/skills/ding/send.py --check-env
   ```

ขอ token ได้จากผู้ดูแลระบบ dingtalk-notify ของ TYCTH
**ห้ามวาง token ในแชทของ Claude** — ถ้าเผลอวางไปแล้ว ให้ขอ token ใหม่

## ตรวจว่าติดตั้งสำเร็จ

พิมพ์ `/` ใน Claude Code ต้องเห็นชื่อแบบ `<plugin>:<skill>` เช่น `tyc-design-system:tyc-design-system`, `create-guide:create-guide`, `ding:ding`

หรือใช้คำสั่งใน terminal:

```bash
claude plugin list
```

## อัปเดต

- **อัตโนมัติ (แนะนำ):** `/plugin` → แท็บ **Marketplaces** → `pi-claude-md` → **Enable auto-update** (ค่าเริ่มต้นของ marketplace ภายนอกคือปิด)
- **อัปเดตเอง:**

  ```bash
  claude plugin marketplace update pi-claude-md
  claude plugin update ding@pi-claude-md
  ```

session ที่เปิดอยู่จะยังใช้เวอร์ชันเดิม จนกว่าจะรัน `/reload-plugins` หรือเปิด session ใหม่

## ถอนการติดตั้ง

```bash
claude plugin uninstall ding@pi-claude-md
```

ไฟล์ใน `~/.config/pi-claude-md/` (token และรายชื่อห้องของ ding) **ไม่ถูกลบ** ถ้าไม่ใช้แล้วให้ลบเอง

## ย้ายจากวิธี symlink เดิม

ถ้าเคย symlink skill ไว้ใน `~/.claude/skills/` ตามวิธีเก่า ให้ลบ symlink ของตัวที่ติดตั้งเป็น plugin แล้ว ไม่งั้น skill จะขึ้นสองชุด:

```bash
rm ~/.claude/skills/tyc-design-system ~/.claude/skills/create-guide
```

ห้ามใส่ `/` ต่อท้ายชื่อ และห้ามใช้ `-r` — ถ้าใช้ `rm -r ชื่อ/` จะลบไฟล์ต้นฉบับใน repo ไปด้วย

ถ้าเคยใช้ ding เวอร์ชันเก่า (เป็นโฟลเดอร์ `~/.claude/skills/ding/`):

1. ย้าย `SECRET_AUTH` ไปไว้ใน `ding.env` ตาม [ตั้งค่า ding](#ตั้งค่า-ding)
2. ย้ายรายชื่อห้อง `~/.claude/skills/ding/channels.json` ไปเป็น `~/.config/pi-claude-md/ding-channels.json`
3. ลบโฟลเดอร์ `~/.claude/skills/ding/` เดิมทิ้ง

## แก้ปัญหา

| อาการ | สาเหตุ | วิธีแก้ |
|---|---|---|
| พิมพ์ `/` แล้วไม่เห็น skill | session ยังไม่โหลด plugin ใหม่ | `/reload-plugins` หรือเปิด session ใหม่ |
| `/install-skills` ไม่มีในรายการ | ไม่ได้เปิด Claude Code ที่ root ของ repo | `cd pi-claude-md` แล้วรัน `claude` ใหม่ |
| ding ขึ้น "ข้าม — ยังไม่ได้ตั้งค่า" | ยังไม่ได้กรอก `ding.env` หรือยังเป็น `paste-token-here` | ทำ [ตั้งค่า ding](#ตั้งค่า-ding) แล้วรัน `/install-skills` ซ้ำ |
| ding ส่งแล้วได้ `FAILED 401` | token ผิด หรือมีช่องว่าง/ขึ้นบรรทัดใหม่ติดมา | แก้ `ding.env` ให้เหลือแค่ `SECRET_AUTH=<token>` บรรทัดเดียว |
| `claude: command not found` | ยังไม่ได้ติดตั้ง Claude Code หรือไม่อยู่ใน PATH | ติดตั้งตาม [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup) |
| `python3: command not found` (Windows) | Windows ใช้ชื่อ `python` | ใช้ `python` แทน `python3` |
| อัปเดตแล้วยังได้ของเก่า | session เดิมยังใช้เวอร์ชันเก่า | `/reload-plugins` |
| skill ขึ้นสองชุด | มี symlink เดิมค้างอยู่ | ดู [ย้ายจากวิธี symlink เดิม](#ย้ายจากวิธี-symlink-เดิม) |

## ความปลอดภัย

- **Secret อยู่ที่ไหน:** อยู่ใน `~/.config/pi-claude-md/` ในเครื่องคุณเท่านั้น และไฟล์ถูกตั้ง permission ให้คุณอ่านได้คนเดียว (`600`)
- **ห้าม commit (repo นี้เป็น public):** token, password, channel UUID จริง, IP ภายใน, path ส่วนตัว — `bash tests/run.sh` สแกนหาสิ่งเหล่านี้ให้ และ CI จะไม่ผ่านถ้าเจอ
- **ไฟล์ที่ ding อัปโหลดเป็น URL สาธารณะ อายุ 7 วัน:** ห้ามแนบภาพหน้าจอหรือไฟล์ที่มีข้อมูลลับ
- **ถ้าเผลอ commit secret:** ขอ token ใหม่ทันที (token เดิมต้องถือว่ารั่วแล้ว แม้จะลบ commit ไปแล้วก็ตาม) แล้วแจ้งเจ้าของ repo

## Skills จากภายนอก

ชุด .NET / Akka / Aspire (35 skills) ติดตั้งจาก marketplace ของเจ้าของโดยตรง:

```
/plugin marketplace add Aaronontheweb/dotnet-skills
```

รายละเอียด: [`docs/external-skills.md`](./docs/external-skills.md)

## เพิ่ม skill ใหม่

1. `cp -r templates/plugin-template plugins/<ชื่อ>` แล้วแก้ชื่อ
2. เขียน `SKILL.md` และ `plugin.json`
3. เพิ่ม entry ใน `.claude-plugin/marketplace.json` และเพิ่มแถวในตารางของ `README.md`, `README.en.md`, `INDEX.md`
4. รัน `bash tests/run.sh` ให้ผ่าน แล้วเปิด Pull Request

กติกาเต็ม (ไม่เขียน comment, ต้อง test ก่อน, security): [CLAUDE.md](./CLAUDE.md)

## โครงสร้าง repo

| Path | เก็บอะไร |
|---|---|
| `.claude-plugin/marketplace.json` | รายชื่อ plugin ทั้งหมด |
| `plugins/<ชื่อ>/` | plugin แต่ละตัว (manifest + skill) |
| `.claude/skills/install-skills/` | `/install-skills` |
| `scripts/install.py` | script ที่ `/install-skills` เรียกใช้ |
| `templates/plugin-template/` | template สำหรับ plugin ใหม่ |
| `tests/` | ชุด test (`bash tests/run.sh`) |
| `docs/` | เอกสารอื่น ๆ |
| [`INDEX.md`](./INDEX.md) | ค้นหาตาม tag |

## License

repo นี้ยังไม่มีไฟล์ LICENSE ตามกฎหมายจึงยังไม่อนุญาตให้นำไปใช้ซ้ำนอกทีม จนกว่าเจ้าของ repo จะเพิ่ม LICENSE
