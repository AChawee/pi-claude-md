## ประเภทของการเปลี่ยนแปลง

- [ ] Plugin / skill ใหม่
- [ ] แก้ skill ที่มีอยู่ (bump `version` ใน `plugin.json` แล้ว)
- [ ] อัปเดตเอกสาร
- [ ] แก้ไข bug

## รายละเอียด

อธิบายสั้นๆ ว่าทำอะไร และทำไม

## Checklist

- [ ] ชื่อโฟลเดอร์ plugin และ skill เป็น `kebab-case` และ `name` ตรงกับชื่อโฟลเดอร์
- [ ] `SKILL.md` มี `description` และ `metadata` ครบ
- [ ] เพิ่มหรืออัปเดต entry ใน `.claude-plugin/marketplace.json`
- [ ] อัปเดต `README.md`, `README.en.md` และ `INDEX.md` แล้ว
- [ ] ไม่มี token, UUID จริง, IP ภายใน หรือ path ส่วนตัวในไฟล์
- [ ] รัน `bash tests/run.sh` แล้วจบด้วย `ALL TESTS PASSED`
