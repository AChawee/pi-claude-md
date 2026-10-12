# Commit format

```
type(scope): description

body (ไม่บังคับ)
```

## บรรทัดแรก (บังคับ)

- `type` ตัวพิมพ์เล็ก จากตารางด้านล่าง
- `(scope)` ไม่บังคับ — ส่วนของระบบที่แก้ เป็นคำอังกฤษตัวเล็กคำเดียว เช่น `auth`, `kpi`, `tasks`, `api`, `db`, `ui`
  ไม่ใช่ชื่อ task, รหัส task หรือชื่อคน
- เว้นวรรค 1 ช่องหลัง `:`
- `description` ไทยหรืออังกฤษ อย่างน้อย 10 ตัวอักษร บอกว่าทำอะไร ห้ามคำกว้าง ๆ เช่น `update code`, `minor changes`

| type | ใช้เมื่อ |
|---|---|
| `feat` | เพิ่มความสามารถใหม่ |
| `fix` | แก้บั๊ก |
| `perf` | ทำให้เร็วขึ้น |
| `refactor` | ปรับโครงโค้ด พฤติกรรมเหมือนเดิม |
| `docs` | เอกสาร |
| `test` | เทส |
| `style` | จัด format ไม่เปลี่ยน logic |
| `build` | dependency, Dockerfile, การ build |
| `ci` | GitHub Actions / pipeline |
| `chore` | งานดูแลทั่วไป |
| `security` | แก้ช่องโหว่ |
| `revert` | ย้อน commit |
| `etc` | งานที่ไม่เข้าหมวดไหน |

## ไม่ถูกตรวจ

commit ที่มีแค่ `deploy!`, merge (`Merge ...`), `Revert "..."`, `fixup!` / `squash!` / `amend!`
และ repo ที่ remote ไม่ใช่ `tycthailand`

## deploy!

บรรทัด `deploy!` ใน commit ไหนก็ได้ยังสั่ง build image เหมือนเดิม — วางเป็นบรรทัดแยกใต้บรรทัดแรก
ห้ามขึ้นต้นบรรทัดแรกด้วย `deploy!`

## ตัวอย่าง

```
feat(kpi): เพิ่มกราฟรายเดือนในหน้า KPI
fix: แก้ปุ่มบันทึกกดไม่ได้ตอนไม่มีไฟล์แนบ
perf(queries): add index for task list by assignee
etc: สรุป requirement ระบบ WMS เฟส 2
```
