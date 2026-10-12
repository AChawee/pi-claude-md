---
name: commit
description: เขียน commit message ตามมาตรฐานทีม "type(scope): description" จาก diff แล้ว commit ให้ แยก commit ถ้างานปนหลายเรื่อง ไม่ push ใช้ทุกครั้งที่ผู้ใช้ขอให้ commit — "/pi-commit:commit", "commit ให้หน่อย", "commit งาน", "ช่วยเขียน commit message", "commit this", "make a commit"
metadata:
  author: ken1lnw
  created: 2026-10-12
  updated: 2026-10-12
  tags: [git, automation]
  status: stable
---

# pi-commit commit

กติกา format อยู่ใน [reference/format.md](reference/format.md) — อ่านก่อนร่าง message ครั้งแรกของ session

## ขั้นตอน

1. ตรวจว่าตั้งค่าแล้ว: `sh "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" status`
   ไม่ขึ้น `OK` → บอกให้รัน `/pi-commit:setup` ก่อน แล้วหยุด
2. ดูงาน: `git status --short` และ `git diff --cached --stat`
   - ยังไม่มีไฟล์ staged → ถามด้วย AskUserQuestion: stage ทั้งหมด / เลือกไฟล์เอง / ยกเลิก
3. อ่าน `git diff --cached` (ไฟล์ใหญ่หรือ lock file ดูแค่ `--stat`)
4. ถ้างานปนหลายเรื่อง (เช่น fix + feat, หรือคนละ module ที่ไม่เกี่ยวกัน) → เสนอแบ่งเป็นกลุ่ม พร้อมรายชื่อไฟล์
   ถามด้วย AskUserQuestion: แยก commit (แนะนำ) / รวมเป็น commit เดียว
   ถ้าแยก ให้ `git reset -q` แล้ว `git add <ไฟล์ของกลุ่ม>` ทีละกลุ่ม ทำข้อ 5–7 ทีละ commit
5. ร่าง message: เลือก type, scope จาก path ที่แก้ (ไม่แน่ใจให้ละไว้), description บอกว่าทำอะไรที่ไหน
   ใช้ภาษาเดียวกับที่ผู้ใช้คุยด้วย ถ้างานมีหลายจุดให้เขียน body เป็น bullet สั้น ๆ
   ผู้ใช้บอกว่าจะ deploy → เพิ่มบรรทัด `deploy!` ท้าย body
6. แสดง message ให้ดู แล้วถามด้วย AskUserQuestion: commit / แก้ข้อความ / ยกเลิก
7. commit ด้วย heredoc:
   ```bash
   git commit -F - <<'EOF'
   <message>
   EOF
   ```
   hook ปฏิเสธ → อ่าน `Problem` แก้ message แล้วลองใหม่
8. สรุป `git log --oneline -n <จำนวนที่ commit>` และบอกว่ายังไม่ได้ push

## ข้อห้าม

- ห้ามใช้ `--no-verify`, `-n` หรือแก้ `core.hooksPath` เพื่อข้าม hook
- ห้าม push ให้เอง — push เข้า main อาจ trigger build และ push ซ้อนจะยกเลิก build ที่กำลังรัน
- ห้าม commit ไฟล์ที่ดูเหมือน secret (`.env`, `*.pem`, `id_*`) — เตือนผู้ใช้แทน
