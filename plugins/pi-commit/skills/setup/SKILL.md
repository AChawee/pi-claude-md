---
name: setup
description: ตั้งค่า pi-commit ครั้งแรกบนเครื่อง — ตั้ง git user.name เป็นรหัสพนักงาน 4 หลัก ติดตั้ง commit-msg hook และ commit template แบบ global ใช้เมื่อผู้ใช้พิมพ์ "/pi-commit:setup", "ตั้งค่า pi-commit", "ติดตั้ง hook commit", "เปลี่ยนรหัสพนักงานใน git", "ถอน pi-commit", "set up pi-commit", "uninstall pi-commit"
metadata:
  author: ken1lnw
  created: 2026-10-12
  updated: 2026-10-12
  tags: [git, automation]
  status: stable
---

# pi-commit setup

Script: `${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh` (รันด้วย `sh` ได้ทั้ง Linux, macOS และ Windows ผ่าน Git Bash)

## ขั้นตอน

1. ตรวจสถานะ: `sh "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" status`
   - ขึ้น `OK` และผู้ใช้ไม่ได้ขอเปลี่ยนรหัส → บอกว่าตั้งค่าไว้แล้ว จบ
2. ถามรหัสพนักงาน 4 หลักเป็นข้อความธรรมดา (ไม่ใช้ AskUserQuestion) ถ้าไม่ใช่ตัวเลข 4 หลักให้ถามซ้ำ
3. ติดตั้ง: `sh "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" install <รหัส>`
4. สรุปผลเป็นภาษาไทย: user.name ใหม่, hook ทำงานกับ repo ที่ remote เป็น `tycthailand` เท่านั้น,
   ใช้ `/pi-commit:commit` ช่วยเขียน message ได้
5. ถ้าอัปเดต plugin แล้ว ให้รันข้อ 3 ซ้ำด้วยรหัสเดิม เพื่อ copy hook ตัวใหม่

ถอนการติดตั้ง: `sh "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" uninstall` (คืน user.name เดิม)

## ถ้า script ไม่ผ่าน

- `core.hooksPath is already set` → มีเครื่องมืออื่นตั้ง global hook ไว้ อธิบายให้ผู้ใช้ฟังและให้ผู้ใช้ตัดสินใจเองว่าจะ unset หรือไม่ **ห้าม unset ให้เอง**
- `git not found` → ให้ติดตั้ง Git ก่อน (Windows ใช้ Git for Windows ซึ่งมี Git Bash)
