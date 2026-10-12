---
name: install-skills
description: ติดตั้ง skills จาก marketplace pi-claude-md แบบเลือกได้หลายตัว — ใช้เมื่อผู้ใช้พิมพ์ "/install-skills", "ติดตั้ง skill", "ลง skill", "install skills", "เลือก skill ที่จะติดตั้ง" ขณะเปิด repo pi-claude-md
metadata:
  author: ken1lnw
  created: 2026-10-12
  updated: 2026-10-12
  tags: [automation]
  status: stable
---

# install-skills

ติดตั้ง plugin จาก marketplace `pi-claude-md` ให้ผู้ใช้ โดยให้ผู้ใช้เลือกเองว่าจะเอาตัวไหน

Script: `scripts/install.py` ที่ root ของ repo — ใช้ `python3` (Windows: ถ้าไม่มี `python3` ให้ใช้ `python`)

## ขั้นตอน

### 1. ดูรายการ

```bash
python3 scripts/install.py list
```

ได้ JSON ของ plugin ทุกตัว: `name`, `description`, `installed`, `needs_setup`, `setup_ok`
ถ้าคำสั่งบอกว่าไม่พบ `claude` → ส่งลิงก์ในข้อความ error ให้ผู้ใช้ติดตั้ง Claude Code ก่อน แล้วหยุด

### 2. ให้ผู้ใช้เลือก

ใช้ AskUserQuestion แบบ `multiSelect: true` หนึ่งคำถาม ตัวเลือกละหนึ่ง plugin ที่ `installed = false`
(AskUserQuestion รับได้ 2–4 ตัวเลือกต่อคำถาม ถ้ามีมากกว่า 4 ให้แบ่งเป็นหลายคำถามในการเรียกครั้งเดียว)

- `label` = ชื่อ plugin · `description` = `description` จาก JSON
- ถ้า `needs_setup = true` ต่อท้าย description ว่า "(ต้องกรอก .env ก่อน)"
- ถ้าทุกตัว `installed = true` แล้ว → บอกผู้ใช้ว่าติดตั้งครบแล้ว และวิธีอัปเดต (ข้อ 5) แล้วจบ

### 3. ตั้งค่าตัวที่ต้องตั้งค่า

ทำเฉพาะตัวที่เลือก และมี `needs_setup = true` และ `setup_ok = false`:

```bash
python3 scripts/install.py setup <name>
```

คำสั่งจะสร้างไฟล์ตั้งค่า (ถ้ายังไม่มี) แล้วพิมพ์ path ออกมา
บอก path ให้ผู้ใช้ไปเปิดด้วย editor ใส่ค่าเอง แล้วตอบกลับเมื่อเสร็จ

**ห้ามขอให้ผู้ใช้วาง token ในแชท ห้ามเขียน token ลงไฟล์ให้ และห้าม cat / Read ไฟล์ .env**
ถ้าผู้ใช้วาง token มาในแชทเอง → อย่าเอาไปใช้ บอกให้ใส่ในไฟล์ และแนะนำให้ขอ token ใหม่ เพราะ token เดิมอยู่ใน log แล้ว

### 4. ติดตั้ง

```bash
python3 scripts/install.py install <name> [<name> ...]
```

ใส่ทุกตัวที่เลือกในคำสั่งเดียว script จะ:
- เพิ่ม marketplace ให้ถ้ายังไม่มี
- ข้ามตัวที่ติดตั้งแล้ว หรือยังตั้งค่าไม่เสร็จ (บอกเหตุผล)
- ตัวที่ล้มเหลวไม่ทำให้ตัวอื่นหยุด

แสดงตาราง markdown ที่ script พิมพ์ออกมาให้ผู้ใช้ตรง ๆ อย่าสรุปว่า "สำเร็จทั้งหมด" ถ้าในตารางมี "ข้าม" หรือ "ล้มเหลว"

ถ้ามี "ข้าม — ยังไม่ได้ตั้งค่า" → ถามว่าจะกลับไปทำข้อ 3 ให้เสร็จแล้วรันข้อ 4 ซ้ำไหม (รันซ้ำได้ปลอดภัย)

### 5. ปิดท้าย

บอกผู้ใช้ 3 อย่าง:
1. รัน `/reload-plugins` หรือเปิด session ใหม่ แล้วพิมพ์ `/` จะเห็น skill เป็น `<plugin>:<skill>`
2. เปิด auto-update: `/plugin` → แท็บ Marketplaces → `pi-claude-md` → Enable auto-update
3. ถ้าเคย symlink skill เดิมไว้ใน `~/.claude/skills/` ให้ลบ symlink ของตัวที่เพิ่งติดตั้งออก ไม่งั้น skill จะขึ้นสองชุด
4. ถ้าติดตั้ง `pi-commit` → หลัง reload ให้รัน `/pi-commit:setup` เพื่อกรอกรหัสพนักงาน (ไม่งั้น hook ยังไม่ทำงาน)
