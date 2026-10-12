# PI Claude Md

## จุดประสงค์

repo นี้คือ **skills กลางของทีม PI ที่ติดตั้งง่าย** — เป็น Claude Code plugin marketplace ที่ 1 skill = 1 plugin
ให้คนในทีมเลือกติดตั้งเฉพาะตัวที่ต้องการ และอัปเดตได้จากที่เดียว

ทุกการเปลี่ยนแปลงต้องทำให้การติดตั้งหรือการใช้งาน **ง่ายขึ้น หรืออย่างน้อยไม่ยากขึ้น**
repo นี้เป็น **public** — ทุกไฟล์ที่ commit คนนอกอ่านได้

---

## กติกาของ repo (บังคับ)

1. **ไม่เขียน comment ในโค้ด** — สื่อความหมายด้วยชื่อตัวแปร/ฟังก์ชัน/ค่าคงที่ (เช่น `NGINX_SAFE_DOC_BYTES`) ข้อจำกัดที่ต้องอธิบายให้เขียนใน SKILL.md
2. **โค้ดกระชับตามหลัก software engineering** — ชื่อสื่อความหมาย ฟังก์ชันเล็กทำอย่างเดียว ไม่มี abstraction หรือ option ที่ยังไม่มีคนใช้ ใช้ Python stdlib เท่านั้น
3. **Test ก่อนบอกว่าเสร็จทุกครั้ง** — รัน `bash tests/run.sh` ต้องจบด้วย `ALL TESTS PASSED` ห้ามรายงานว่า "เสร็จ" หรือ "สำเร็จ" ถ้ายังไม่ได้รัน หรือรันแล้วไม่ผ่าน (ถ้าไม่ผ่านให้แสดง output จริง)
4. **ทุกการเปลี่ยนแปลงต้องคิด 3 เรื่อง**
   - **User friendly** — ข้อความถึงผู้ใช้เป็นภาษาไทย error ต้องบอกว่าต้องทำอะไรต่อ คำสั่งในเอกสาร copy ไปรันได้เลย
   - **Performance** — SKILL.md สั้นที่สุดเท่าที่ทำได้ เนื้อหายาวแยกไว้ใน `reference/` ให้อ่านเฉพาะตอนต้องใช้ ตรวจด้วย `claude plugin details <plugin>@pi-claude-md`
   - **Security** — ห้ามมี token, password, channel UUID จริง, IP ภายใน, path ส่วนตัว (`/home/<user>`, `C:\Users\<user>`) ใน repo · secret อยู่ใน `~/.config/pi-claude-md/` เท่านั้น · ห้ามให้ผู้ใช้วาง token ในแชท
5. **ทำตามหลักการทำงานด้านล่าง** (Think Before Coding → Design and UX Standards)

**ข้อยกเว้น — plugin `pi-commit`:** script ที่รันบนเครื่อง dev (`plugins/pi-commit/scripts/`) เขียนด้วย POSIX `sh` แทน Python
เพื่อไม่ต้องติดตั้ง Python (git hook รันผ่าน sh ที่มากับ git อยู่แล้ว ทั้ง Linux และ Git for Windows)
และข้อความ error ของ hook เป็นภาษาอังกฤษตามที่ทีมเลือก · test ยังเป็น Python (`tests/test_pi_commit.py`)

---

## โครงสร้าง

```
pi-claude-md/
├── .claude-plugin/marketplace.json     ← รายชื่อ plugin ทั้งหมด (source of truth)
├── .claude/skills/install-skills/      ← /install-skills (ใช้ได้เมื่อเปิด repo นี้เท่านั้น)
├── plugins/<name>/
│   ├── .claude-plugin/plugin.json      ← name + version (version อยู่ที่นี่ที่เดียว)
│   └── skills/<name>/SKILL.md          ← + reference/, script
├── scripts/install.py                  ← list / setup / install
├── templates/plugin-template/          ← copy ไปเริ่ม plugin ใหม่
├── tests/                              ← bash tests/run.sh
├── docs/external-skills.md             ← skills ของทีมอื่น (ติดตั้งผ่าน marketplace เขา)
├── README.md / README.en.md            ← สำหรับคนติดตั้ง/ใช้งาน
└── INDEX.md                            ← ค้นหาตาม tag
```

---

## การเพิ่ม skill ใหม่

```bash
cp -r templates/plugin-template plugins/<ชื่อ>
mv plugins/<ชื่อ>/skills/my-skill plugins/<ชื่อ>/skills/<ชื่อ>
```

1. แก้ `plugins/<ชื่อ>/.claude-plugin/plugin.json` (`name`, `description`, `author`)
2. แก้ `SKILL.md` — `name` ต้องตรงกับชื่อโฟลเดอร์ `description` ต้องมีคำที่ผู้ใช้จะพิมพ์จริง
3. เพิ่ม entry ใน `.claude-plugin/marketplace.json`
4. เพิ่มแถวในตาราง skill ของ `README.md`, `README.en.md` และ `INDEX.md` (ตาราง plugin + ตาราง tag)
5. ถ้า skill ต้องใช้ secret → อ่านจาก `~/.config/pi-claude-md/<ชื่อ>.env` มี `--init-env`/`--check-env` แบบ `plugins/ding` แล้วเพิ่มใน `SETUP_SCRIPTS` ของ `scripts/install.py`
6. รัน `bash tests/run.sh`

**แก้ skill ที่มีอยู่:** bump `version` ใน `plugin.json` ทุกครั้ง (semver) ไม่งั้นผู้ใช้จะไม่ได้อัปเดต

**Skills ของทีมอื่นห้าม copy เข้ามา** — บันทึกไว้ใน [`docs/external-skills.md`](./docs/external-skills.md) แทน

### กติกา SKILL.md

| Field | กติกา | ถ้าผิด |
|---|---|---|
| `name` | lowercase-kebab-case ตรงกับชื่อโฟลเดอร์ | skill ไม่โหลด |
| `description` | บังคับ มีคีย์เวิร์ดที่ผู้ใช้จะพิมพ์ ไม่เกิน 1024 ตัวอักษร | โหลดแต่ไม่เคยถูกเรียก |
| `metadata` | `author`, `created`, `updated`, `tags`, `status` (ไม่มี `version`) | test ไม่ผ่าน |

อ้างไฟล์ใน plugin จาก SKILL.md ด้วย `${CLAUDE_PLUGIN_ROOT}` ส่วนไฟล์ใน `reference/` อ้างแบบ relative กับโฟลเดอร์ของ SKILL.md

### Tags ที่ใช้อยู่

| Tag | ความหมาย |
|-----|---------|
| `documentation` | สร้างหรือจัดการเอกสาร |
| `guide` | คู่มือการใช้งาน |
| `html` | สร้าง HTML output |
| `capture` | Screenshot/Playwright automation |
| `bilingual` | รองรับหลายภาษา |
| `automation` | Automation scripts/flows |
| `notification` | ส่งแจ้งเตือน |
| `design-system` | ธีม / design token / UI convention |
| `git` | git hook / commit convention |

---

## หลักการทำงาน

Behavioral guidelines to reduce common LLM coding mistakes. These bias toward caution over speed; for trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused.

The test: every changed line should trace directly to the request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

- "Add validation" → write tests for invalid inputs, then make them pass
- "Fix the bug" → write a test that reproduces it, then make it pass
- "Refactor X" → ensure tests pass before and after

For multi-step tasks, state a brief plan with a verify step for each.

### 5. Design and UX Standards

**Solve the user's goal before decorating it.**

- Treat existing UI as a signal of intent, not a spec to preserve. For redesigns, state whether it's a structural redesign or a visual reskin.
- Resolve user goals, information hierarchy, and interaction friction first. Make the primary action obvious.
- Carry the design with typography, spacing, hierarchy, and composition — not gradients or decorative effects.
- Use progressive disclosure: essentials up front, detail on demand.
- Avoid the generic AI look: excessive rounded cards, glassmorphism, purple-blue gradients, repetitive dashboard grids, oversized hero text, unnecessary icons.
- Responsive and accessible by default: semantic HTML, keyboard navigation, visible focus, adequate contrast, touch-friendly targets.
- Ship complete states: loading, empty, error, disabled, success, hover, focus. Use realistic content, no lorem ipsum.
