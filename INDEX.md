# PI Claude Md — Index

ค้นหา plugin ตามชื่อหรือ tag · วิธีติดตั้งแบบละเอียดอยู่ใน [README.md](./README.md)

ทุก plugin ติดตั้งได้ด้วย `/install-skills` (เมื่อเปิด repo นี้ใน Claude Code) หรือ `/plugin install <ชื่อ>@pi-claude-md`

---

## Plugins

| ชื่อ | ทำอะไร | Tags | ต้องตั้งค่าก่อน | Author |
|------|--------|------|-----------------|--------|
| [tyc-design-system](./plugins/tyc-design-system/skills/tyc-design-system/SKILL.md) | ใช้ design system กลางของ TYC (สี ปุ่ม ตาราง การ์ด dark/light) กับงาน UI | `design-system` `html` | ไม่ต้อง | Narawit |
| [create-guide](./plugins/create-guide/skills/create-guide/SKILL.md) | สร้างคู่มือการใช้งาน HTML ไฟล์เดียว พร้อม auto-capture | `documentation` `guide` `html` `capture` `bilingual` | ไม่ต้อง | Narawit |
| [ding](./plugins/ding/skills/ding/SKILL.md) | ส่งข้อความ markdown พร้อมไฟล์แนบเข้ากลุ่ม DingTalk | `notification` `automation` | ต้องกรอก `ding.env` | ken1lnw |
| [pi-commit](./plugins/pi-commit/skills/commit/SKILL.md) | มาตรฐาน commit: user.name = รหัสพนักงาน + hook ตรวจ `type(scope): description` | `git` `automation` | ต้องรัน `/pi-commit:setup` | ken1lnw |

---

## ค้นหาตาม Tag

| Tag | Plugins |
|-----|---------|
| `design-system` | tyc-design-system |
| `html` | tyc-design-system, create-guide |
| `documentation` | create-guide |
| `guide` | create-guide |
| `capture` | create-guide |
| `bilingual` | create-guide |
| `notification` | ding |
| `automation` | ding, pi-commit |
| `git` | pi-commit |

---

## External Skills (ติดตั้งผ่าน marketplace ของเจ้าของ — ไม่เก็บไฟล์ใน repo)

| ชุด | มีอะไร | ที่มา | License | ติดตั้ง |
|-----|--------|-------|---------|---------|
| [.NET / Akka / Aspire](./docs/external-skills.md) | 35 skills — C#, Akka.NET, Aspire, EF Core, testing, OpenTelemetry | [Aaronontheweb/dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) | MIT | `/plugin marketplace add Aaronontheweb/dotnet-skills` |

> ห้าม copy ไฟล์ skill ของทีมอื่นเข้า repo นี้ — ใช้ marketplace ของเขา แล้วบันทึกไว้ใน [`docs/external-skills.md`](./docs/external-skills.md)

---

เพิ่ม plugin ใหม่ → ทำตาม "การเพิ่ม skill ใหม่" ใน [CLAUDE.md](./CLAUDE.md) (test จะไม่ผ่านถ้าตารางนี้ไม่ตรงกับ marketplace)
